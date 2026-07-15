// ashrain.out — 연산 AI 생성 서버리스 함수 (v0.2.3)
// 위치: 레포 "최상단"의 api/genCalc.js  (src 안 아님! GitHub 웹에서 파일명을 api/genCalc.js 로 만들면 폴더가 생깁니다)
// 필요 환경변수(Vercel → Settings → Environment Variables):
//   ANTHROPIC_API_KEY  (필수)
//   CALC_GEN_MODEL     (선택, 기본 claude-sonnet-4-6)
// Supabase URL/키는 앱이 이미 쓰는 VITE_SUPABASE_URL / VITE_SUPABASE_ANON_KEY 를 그대로 읽습니다.

import { createClient } from "@supabase/supabase-js";

const MODEL = process.env.CALC_GEN_MODEL || "claude-sonnet-4-6";
const MAX_PAGES = 3;
const MAX_COUNT = 40;

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST만 지원해요" });

  try {
    // ── 1) 로그인 + 관리자 확인 ──
    const auth = req.headers.authorization || "";
    const token = auth.startsWith("Bearer ") ? auth.slice(7) : null;
    if (!token) return res.status(401).json({ error: "로그인이 필요해요" });

    const url = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
    const anon = process.env.VITE_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY;
    if (!url || !anon) return res.status(500).json({ error: "Supabase 환경변수가 없어요" });

    const sb = createClient(url, anon, { global: { headers: { Authorization: `Bearer ${token}` } } });
    const { data: userData, error: uErr } = await sb.auth.getUser(token);
    if (uErr || !userData?.user) return res.status(401).json({ error: "인증 실패" });

    const { data: prof } = await sb.from("profiles").select("role").eq("id", userData.user.id).single();
    if (prof?.role !== "admin") return res.status(403).json({ error: "관리자만 사용할 수 있어요" });

    if (!process.env.ANTHROPIC_API_KEY)
      return res.status(500).json({ error: "ANTHROPIC_API_KEY가 Vercel에 설정되지 않았어요" });

    // ── 2) 입력 검사 ──
    const { pages, unitId, unitName, count } = req.body || {};
    if (!Array.isArray(pages) || pages.length < 1 || pages.length > MAX_PAGES)
      return res.status(400).json({ error: `페이지 이미지는 1~${MAX_PAGES}장이어야 해요` });
    const n = Math.min(Math.max(parseInt(count, 10) || 20, 5), MAX_COUNT);
    if (!unitId) return res.status(400).json({ error: "대상 유닛이 없어요" });

    // ── 3) 프롬프트 ──
    const prompt = `너는 한국 중·고등 수학 학원의 연산 문제 출제 도우미다.
첨부한 이미지는 원장님이 직접 만든 연산 문제지의 일부다. 이 문제지의 "유형"만 분석해서
(문장 형식, 수의 범위, 답의 형식, 함정 설계) 완전히 "새로운" 문제 ${n}개를 만들어라.

절대 규칙:
1. 원본 문제를 그대로 베끼거나 숫자만 바꾸는 것 금지 — 유형만 따르고 전부 새로 출제.
2. 수식 표기는 유니코드만: 곱셈 ×, 나눗셈 ÷, 음수·빼기 −, 거듭제곱은 위첨자(x², 2³), 분수는 a/b. 백슬래시·LaTeX 금지.
3. 답(answer)은 학생이 키보드로 입력 가능한 ASCII: 정수(-6), 기약분수(3/4), 간단한 식(2x+1), 부등식 해(x>4, x>=4). 유니코드 − 금지.
4. type은 calc(단답 입력) / ox(O·X) / choice(5지선다) 중 하나.
   choice는 choices 배열에 보기 5개(문자열), answer는 그 중 정답과 "정확히 같은 문자열".
   ox의 answer는 "O" 또는 "X".
5. difficulty는 1(암산)·2(한 줄 계산)·3(여러 단계), timeLimit은 문제당 제한 초(8~30).
6. 대상 학생은 혼자 공부하는 하위권 — 문장은 짧고 명확하게, 해요체 불필요(문제체).
7. 계산이 필요한 문제는 스스로 검산해서 answer가 정확한지 확인한 뒤 출력.

출력은 아래 JSON "만" — 설명·마크다운·코드펜스 금지:
{"problems":[{"type":"calc","question":"…","answer":"…","choices":null,"difficulty":1,"timeLimit":10}, …]}

대상 유닛: ${unitName || unitId}`;

    const content = [
      ...pages.map((data) => ({
        type: "image",
        source: { type: "base64", media_type: "image/jpeg", data },
      })),
      { type: "text", text: prompt },
    ];

    // ── 4) Anthropic 호출 ──
    const aiRes = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": process.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 8000,
        messages: [{ role: "user", content }],
      }),
    });
    const aiJson = await aiRes.json();
    if (!aiRes.ok) {
      return res.status(502).json({ error: "AI 호출 실패: " + (aiJson?.error?.message || aiRes.status) });
    }

    const text = (aiJson.content || []).filter((b) => b.type === "text").map((b) => b.text).join("\n");
    const clean = text.replace(/```json|```/g, "").trim();
    let parsed;
    try { parsed = JSON.parse(clean); }
    catch { return res.status(502).json({ error: "AI 응답을 JSON으로 해석하지 못했어요 — 다시 시도해 주세요" }); }

    // ── 5) 서버 측 1차 정리 ──
    const okTypes = new Set(["calc", "ox", "choice"]);
    const problems = (parsed.problems || []).filter((p) =>
      p && okTypes.has(p.type) && p.question && p.answer != null && String(p.answer) !== "" &&
      (p.type !== "choice" || (Array.isArray(p.choices) && p.choices.length === 5)) &&
      (p.type !== "ox" || ["O", "X"].includes(String(p.answer)))
    ).slice(0, MAX_COUNT).map((p) => ({
      type: p.type,
      question: String(p.question),
      answer: String(p.answer),
      choices: p.type === "choice" ? p.choices.map(String) : null,
      difficulty: [1, 2, 3].includes(p.difficulty) ? p.difficulty : 2,
      timeLimit: p.timeLimit > 0 && p.timeLimit <= 120 ? Math.round(p.timeLimit) : 15,
    }));

    return res.status(200).json({ problems, model: MODEL, dropped: (parsed.problems || []).length - problems.length });
  } catch (err) {
    return res.status(500).json({ error: "서버 오류: " + (err?.message || String(err)) });
  }
}
