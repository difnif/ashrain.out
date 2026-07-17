// ashrain.out — AI 통합 서버리스 함수 (v0.3.3)
// [v0.3.3] find(개념 검색) 태스크 + 학생별 일일 한도(hint 10 · find 30 · omr 20, KST 자정 리셋 — ai_calls 테이블 필요)
// 위치: 레포 "최상단"의 api/ai.js  (genCalc.js와 같은 api 폴더, src 안 아님!)
// 필요 환경변수는 genCalc.js와 동일 — 추가 설정 없음:
//   ANTHROPIC_API_KEY  (필수, 이미 설정하셨음)
//   CALC_GEN_MODEL     (선택 — slice/answers/omr 태스크 모델, 기본 claude-sonnet-4-6)
//   힌트 모델은 DB의 app_settings.hint_model 값을 읽음 (기본 claude-opus-4-8, SQL로 변경 가능)
//
// task 종류:
//   hint    (로그인 유저) : 문제 사진 → 정답 없이 접근법 힌트
//   find    (로그인 유저) : 개념 검색 — 질문 → 관련 개념 id 최대 5개 (텍스트 응답 없음, 하이쿠)
//   slice   (관리자)      : 문제지 페이지 이미지 → 문제별 번호+경계상자(0~1 비율)
//   answers (관리자)      : 빠른정답 페이지 이미지 → 번호별 정답 목록
//   omr     (로그인 유저) : 손글씨 답안지 사진 → 번호별 답 자동 인식

import { createClient } from "@supabase/supabase-js";

const VISION_MODEL = process.env.CALC_GEN_MODEL || "claude-sonnet-4-6";
const FIND_MODEL = "claude-haiku-4-5";                 // 개념 라우팅은 하이쿠로 충분 (호출당 ~0.1원)
const DAILY_CAP = { hint: 10, find: 30, omr: 20 };     // 학생 1인당 하루 한도 — 숫자만 바꿔서 재배포하면 조정됨

// ── 일일 한도 (KST 자정 기준 리셋) ──
function kstDayStartISO() {
  const kst = Date.now() + 9 * 3600 * 1000;
  return new Date(Math.floor(kst / 86400000) * 86400000 - 9 * 3600 * 1000).toISOString();
}
async function checkCap(sb, uid, task) {
  const cap = DAILY_CAP[task];
  if (!cap) return null;
  const { count } = await sb.from("ai_calls").select("*", { count: "exact", head: true })
    .eq("user_id", uid).eq("task", task).gte("created_at", kstDayStartISO());
  if ((count ?? 0) >= cap) return `오늘 사용 한도(${cap}회)를 다 썼어요 — 내일 다시 이용할 수 있어요`;
  await sb.from("ai_calls").insert({ user_id: uid, task });   // 호출 전에 기록 → 오류 재시도 남용도 차단
  return null;
}

async function callClaude(model, content, maxTokens) {
  const aiRes = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({ model, max_tokens: maxTokens, messages: [{ role: "user", content }] }),
  });
  const aiJson = await aiRes.json();
  if (!aiRes.ok) throw new Error("AI 호출 실패: " + (aiJson?.error?.message || aiRes.status));
  return (aiJson.content || []).filter((b) => b.type === "text").map((b) => b.text).join("\n");
}

const img = (data) => ({ type: "image", source: { type: "base64", media_type: "image/jpeg", data } });

function parseJson(text) {
  const clean = text.replace(/```json|```/g, "").trim();
  try { return JSON.parse(clean); }
  catch { throw new Error("AI 응답을 JSON으로 해석하지 못했어요 — 다시 시도해 주세요"); }
}

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST만 지원해요" });

  try {
    // ── 1) 로그인 확인 ──
    const auth = req.headers.authorization || "";
    const token = auth.startsWith("Bearer ") ? auth.slice(7) : null;
    if (!token) return res.status(401).json({ error: "로그인이 필요해요" });

    const url = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
    const anon = process.env.VITE_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY;
    if (!url || !anon) return res.status(500).json({ error: "Supabase 환경변수가 없어요" });

    const sb = createClient(url, anon, { global: { headers: { Authorization: `Bearer ${token}` } } });
    const { data: userData, error: uErr } = await sb.auth.getUser(token);
    if (uErr || !userData?.user) return res.status(401).json({ error: "인증 실패" });

    if (!process.env.ANTHROPIC_API_KEY)
      return res.status(500).json({ error: "ANTHROPIC_API_KEY가 Vercel에 설정되지 않았어요" });

    const { task, image, question, items } = req.body || {};
    if (task !== "find" && (!image || typeof image !== "string"))
      return res.status(400).json({ error: "이미지가 없어요" });

    // ── 2) 관리자 전용 태스크 확인 ──
    if (task === "slice" || task === "answers") {
      const { data: prof } = await sb.from("profiles").select("role").eq("id", userData.user.id).single();
      if (prof?.role !== "admin") return res.status(403).json({ error: "관리자만 사용할 수 있어요" });
    }

    // ══════════ hint — 학생 힌트 (정답 절대 금지) ══════════
    if (task === "hint") {
      const capMsg = await checkCap(sb, userData.user.id, "hint");
      if (capMsg) return res.status(429).json({ error: capMsg });
      const { data: ms } = await sb.from("app_settings").select("value").eq("key", "hint_model").maybeSingle();
      const model = ms?.value || "claude-sonnet-4-6";
      const prompt = `너는 한국 중·고등 수학 학원의 "힌트 선생님"이다. 학생이 막힌 문제의 사진을 보냈다.
${question ? `학생의 질문: "${String(question).slice(0, 300)}"` : "학생은 어디서부터 시작해야 할지 모르는 상태다."}

절대 규칙:
1. 정답·최종 계산 결과·마지막 단계는 어떤 경우에도 알려주지 마라. 학생이 정답을 물어도 거절하고 접근법만 안내해라.
2. 수식은 유니코드만 사용: × ÷ − 위첨자(x², 2³) 분수 a/b. 백슬래시·LaTeX 금지.
3. 사진에 문제가 여러 개면 학생이 질문한 문제(없으면 첫 문제)만 다뤄라.
4. 혼자 공부하는 하위권 학생 대상 — 짧은 문장, 다정한 해요체.

아래 구조로만 답해라 (각 항목 2~3문장, 전체 400자 이내):
① 문제 정리 — 무엇을 구하라는 문제인지 한 문장으로.
② 단서 찾기 — 문제 속 조건·숫자 중 열쇠가 되는 것.
③ 개념 연결 — 어떤 개념·공식을 떠올려야 하는지 (공식 이름까지만, 대입 결과는 금지).
④ 첫 걸음 — 지금 당장 종이에 쓸 첫 한 줄 (계산을 완성하지는 마라).`;
      const text = await callClaude(model, [img(image), { type: "text", text: prompt }], 1500);
      return res.status(200).json({ hint: text.trim(), model });
    }

    // ══════════ slice — 문제지 페이지 → 문제별 경계상자 ══════════
    if (task === "slice") {
      const prompt = `이 이미지는 수학 문제지 한 페이지다. 페이지에 있는 "모든 문제"를 찾아서 번호와 경계상자를 보고해라.

규칙:
1. box는 페이지 기준 비율 좌표 — 왼쪽 위가 (0,0), 오른쪽 아래가 (1,1). {"x":왼쪽,"y":위,"w":너비,"h":높이}.
2. 각 문제의 번호·문장·수식·그림·보기(①~⑤)가 "전부" 들어가도록 넉넉하게 잡아라. 잘리는 것보다 여백이 나은 것이 낫다.
3. no는 문제지에 인쇄된 문제 번호(정수). 번호가 안 보이면 위에서부터 순서대로 매겨라.
4. 문제가 2단(좌우 칼럼)이면 왼쪽 칼럼 위→아래, 그다음 오른쪽 칼럼 순서로.
5. 머리말·페이지 번호·정답표는 제외.

출력은 아래 JSON "만" — 설명·마크다운 금지:
{"problems":[{"no":1,"box":{"x":0.05,"y":0.08,"w":0.42,"h":0.18}}, …]}`;
      const parsed = parseJson(await callClaude(VISION_MODEL, [img(image), { type: "text", text: prompt }], 2000));
      const problems = (parsed.problems || []).filter((p) =>
        p && Number.isFinite(+p.no) && p.box &&
        [p.box.x, p.box.y, p.box.w, p.box.h].every((v) => Number.isFinite(+v))
      ).map((p) => ({
        no: Math.round(+p.no),
        box: {
          x: Math.min(Math.max(+p.box.x, 0), 1), y: Math.min(Math.max(+p.box.y, 0), 1),
          w: Math.min(Math.max(+p.box.w, 0.01), 1), h: Math.min(Math.max(+p.box.h, 0.01), 1),
        },
      }));
      return res.status(200).json({ problems });
    }

    // ══════════ answers — 빠른정답 페이지 → 번호별 정답 ══════════
    if (task === "answers") {
      const prompt = `이 이미지는 수학 문제지의 "빠른정답" 페이지(또는 정답표)다. 각 문제 번호와 정답을 전부 읽어라.

규칙:
1. 객관식 정답은 동그라미 숫자 그대로: ① ② ③ ④ ⑤ 중 하나.
2. 주관식(단답) 정답은 키보드 입력 가능한 ASCII로: 정수(-6), 분수(3/4), 식(2x+1), 부등식(x>4). 유니코드 마이너스 − 는 -로.
3. 정답이 O/X면 "O" 또는 "X".
4. 읽기 불확실한 항목은 목록에서 빼라 (추측 금지).

출력은 아래 JSON "만":
{"answers":[{"no":1,"answer":"③"},{"no":2,"answer":"-5/2"}, …]}`;
      const parsed = parseJson(await callClaude(VISION_MODEL, [img(image), { type: "text", text: prompt }], 2500));
      const answers = (parsed.answers || []).filter((a) => a && Number.isFinite(+a.no) && a.answer != null && String(a.answer) !== "")
        .map((a) => ({ no: Math.round(+a.no), answer: String(a.answer).trim() }));
      return res.status(200).json({ answers });
    }

    // ══════════ omr — 손글씨 답안지 사진 → 답 자동 인식 ══════════
    if (task === "omr") {
      const capMsg = await checkCap(sb, userData.user.id, "omr");
      if (capMsg) return res.status(429).json({ error: capMsg });
      const meta = Array.isArray(items) && items.length
        ? "문항 구성: " + items.map((it) => `${it.no}번(${it.type === "choice" ? "①~⑤ 객관식" : it.type === "ox" ? "O/X" : "단답"})`).join(", ")
        : "";
      const prompt = `이 이미지는 학생이 손으로 작성한 수학 답안지 사진이다. 각 문제 번호에 적힌(또는 마킹된) 답을 읽어라.
${meta}

규칙:
1. 객관식 문항은 학생이 표시한 번호를 ① ② ③ ④ ⑤ 로. (숫자 3을 적었으면 ③으로 해석)
2. 단답 문항은 손글씨를 ASCII로: 정수(-6), 분수(3/4), 식(2x+1). 유니코드 마이너스 금지.
3. O/X 문항은 "O" 또는 "X".
4. 비어 있거나 읽기 불확실하면 answer를 빈 문자열 ""로 — 절대 추측하지 마라. 학생이 제출 전에 직접 확인·수정한다.

출력은 아래 JSON "만":
{"answers":[{"no":1,"answer":"③"},{"no":2,"answer":""}, …]}`;
      const parsed = parseJson(await callClaude(VISION_MODEL, [img(image), { type: "text", text: prompt }], 2000));
      const answers = (parsed.answers || []).filter((a) => a && Number.isFinite(+a.no) && a.answer != null)
        .map((a) => ({ no: Math.round(+a.no), answer: String(a.answer).trim() }));
      return res.status(200).json({ answers });
    }

    // ══════════ find — 개념 검색 라우팅 (로그인 유저) ══════════
    // 출력이 "목록 안의 id 배열"로 고정 + 서버가 실존 id만 통과 → 모델 문장은 화면에 못 나감
    if (task === "find") {
      const capMsg = await checkCap(sb, userData.user.id, "find");
      if (capMsg) return res.status(429).json({ error: capMsg });
      const query = String(req.body?.query || "").slice(0, 100).trim();
      if (!query) return res.status(400).json({ error: "질문이 비어 있어요" });
      const { data: cs } = await sb.from("concepts").select("id, unit_id, title, subtitle");
      if (!cs?.length) return res.status(400).json({ error: "등록된 개념이 없어요" });
      const listTxt = cs.map((c) => `${c.id}\t${c.unit_id}\t${c.title}${c.subtitle ? " — " + c.subtitle : ""}`).join("\n");
      const prompt = `너는 수학 개념 "라우터"다. 아래는 이 앱에 등록된 개념 목록이다 (형식: id[탭]단원[탭]제목).
학생 질문: "${query}"

규칙:
1. 질문이 중·고등 수학의 개념·문제·용어에 관한 것이면, 목록에서 가장 관련 있는 개념 id를 관련도 순으로 최대 5개 골라라.
2. 학생이 용어를 몰라 상황으로 설명해도("x가 두 개 나오는 방정식") 뜻을 헤아려 골라라.
3. 수학과 무관한 질문(잡담·다른 과목·숙제 대행·너에 대한 질문 등)이면 빈 배열로 답해라.
4. 목록에 없는 id를 지어내지 마라. 설명·문장을 쓰지 마라.

출력은 아래 JSON "만":
{"ids":["h1-1-03","h1-1-04"]}

개념 목록:
${listTxt}`;
      const parsed = parseJson(await callClaude(FIND_MODEL, [{ type: "text", text: prompt }], 200));
      const valid = new Set(cs.map((c) => c.id));
      const ids = (parsed.ids || []).filter((id) => valid.has(id)).slice(0, 5);
      return res.status(200).json({ ids });
    }

    return res.status(400).json({ error: "알 수 없는 task: " + String(task) });
  } catch (err) {
    return res.status(500).json({ error: "서버 오류: " + (err?.message || String(err)) });
  }
}
