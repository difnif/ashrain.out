// ashrain.out — 촬영 학습 서버리스 함수 (api/photo.js · v1.0, 2026-09-20)
// 학생이 찍은 문항·답안 사진을 인식하고(전사), 문장 이해·표시 연습·서술형 채점·풀이과정 검사를 돕는다.
// 원칙
//   · 사진과 문항 전사 텍스트는 서버에 저장하지 않는다(응답 뒤 버림). Storage 업로드 없음.
//   · 답안 원문은 보관 게이트(src/lib/retention.js)가 'central' 이라 할 때만 DB 에 남고, 기본 정책(labels)에서는 라벨만 남는다.
//   · 문항 표현 등급(S/M/C)은 발문표준성 검토 v2 기준으로 판정한다. 등급·겹침·정책 → 보관 위치.
//   · 정답을 대신 풀어 주지 않는다(approach). 채점·검사는 학생 답안에 대한 첨삭이다.
// 환경변수: ANTHROPIC_API_KEY (필수) · SUPABASE_URL/VITE_SUPABASE_URL · SUPABASE_ANON_KEY/VITE_SUPABASE_ANON_KEY · SUPABASE_SERVICE_ROLE_KEY
// app_settings: photo_model(기본 claude-sonnet-4-6 · 전사/등급/방침) · photo_model_grade(기본 claude-opus-4-8 · 채점/검사)
//               · photo_model_fallback(전사 실패 시 강한 모델 — 없으면 grade 모델) · photo_retention(labels|gated|all)
// task: scan(problem|answer|page) · approach · essay · process   — 전부 로그인 필수, 학생 자격 게이트, 일일 한도(ai_calls)
// scan 은 retry_strong:true 를 받으면 폴백(강한) 모델로 읽는다 — 클라이언트가 1차 실패 때만 보낸다(한도 1회 추가 차감).

import { createClient } from "@supabase/supabase-js";
import { parseText } from "../src/lib/mathir.js";
import { overlapScore, decideRetention, buildLabels, normalizePolicy, GRADES } from "../src/lib/retention.js";

export const config = { maxDuration: 60 };

const DEFAULT_MODEL = "claude-sonnet-4-6";
const DEFAULT_GRADE_MODEL = "claude-opus-4-8";
const DAILY_CAP = { photo_scan: 40, photo_approach: 20, photo_essay: 10, photo_process: 10 };
const MAX_IMAGE_B64 = 4_000_000;    // ≈ 3 MB (Vercel 본문 한도 4.5 MB 안쪽 · 클라이언트는 긴 변 1600px 로 줄여 보낸다)
const MAX_TEXT = 3000;
const MAX_LINES = 60, MAX_CHOICES = 8;
const TRAPS = ["구하는대상혼동", "부호", "단위", "단위환산", "조건누락", "역연산", "평균오용", "제곱누락", "계산실수"];
const EL_KEYS = ["발문", "조건제시", "소재맥락", "도형자료", "지문"];
const TIME_BUDGET_MS = 50_000;      // maxDuration 60s 안에서 재시도·등급 판정을 건너뛰는 기준

// ─────────────────────────────────────────────────────────────── 공용
function svcClient() {
  const url = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
  if (!url || !key) return null;
  return createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } });
}
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
  await sb.from("ai_calls").insert({ user_id: uid, task });
  return null;
}
async function callClaude({ model, system, content, maxTokens = 2500 }) {
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "content-type": "application/json", "x-api-key": process.env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01" },
    body: JSON.stringify({ model, max_tokens: maxTokens, system, messages: [{ role: "user", content }] }),
  });
  const j = await r.json();
  if (!r.ok) throw new Error("AI 호출 실패: " + (j?.error?.message || r.status));
  return (j.content || []).filter((b) => b.type === "text").map((b) => b.text).join("\n");
}
const img = (data) => ({ type: "image", source: { type: "base64", media_type: "image/jpeg", data } });
const txt = (text) => ({ type: "text", text });
function parseObj(text) {
  const m = String(text || "").replace(/```json|```/g, "").match(/\{[\s\S]*\}/);
  if (!m) throw new Error("AI 응답을 JSON으로 해석하지 못했어요 — 다시 시도해 주세요");
  try { return JSON.parse(m[0]); } catch { throw new Error("AI 응답을 JSON으로 해석하지 못했어요 — 다시 시도해 주세요"); }
}
const str = (v, n = MAX_TEXT) => (typeof v === "string" ? v.trim().slice(0, n) : "");
const arr = (v) => (Array.isArray(v) ? v : []);
const clamp01 = (v) => Math.min(Math.max(+v || 0, 0), 1);
const light = (v) => (["green", "yellow", "red"].includes(v) ? v : "yellow");
async function settings(sb, keys) {
  const { data } = await sb.from("app_settings").select("key, value").in("key", keys);
  const out = {};
  for (const r of data || []) out[r.key] = r.value;
  return out;
}
/** 테이블이 아직 없을 때(마이그레이션 미적용) 나는 오류인가 */
const missingRel = (e) => e && ["42P01", "42703", "PGRST202", "PGRST204", "PGRST205"].includes(String(e.code || ""));

// ─────────────────────────────────────────────────────────────── 프롬프트
const MATHIR_SPEC = `■ 수식 표기 — MathIR 닫힌 문법 (이 목록 밖 토큰 금지)
- 문장 속 수식은 [[ ... ]]로 감싸고 그 안은 MathIR만. 단순 숫자·단위(3 cm, 40개)는 평문.
- 기본: 숫자, 변수(x,a,...), + - * / = != < > <= >=, 괄호, 병치곱(2x, 3(x+1)). 유니코드 수식문자·LaTeX 금지.
- 함수: frac(a,b) mixed(w,a,b) pow(b,e) sqrt(x) root(n,x) abs(x) recdec(pre,rep) floor(x) fact(n)
  max min ratio(a,b[,c]) pct(x) deg(x) dms(d,m[,s]) pm | seg line ray arc angle tri quad par perp cong sim
  point(x,y) point3 vec vcomp dot | set setb in notin subset nsubset union inter comp card imp iff neg itv(a,b,cc|co|oc|oo) conj
  | log([b,]x) ln sin cos tan csc sec cot | sub(a,n) sum(k,a,b,f) lim(x,a,f[,+|-]) prime(f[,2]) dydx integ dinteg(a,b,f,x) inv
  | perm comb pperm hcomb prob cprob ev var sd binomd normald | 상수 pi e i inf empty
예: "일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오."
자주 틀리는 치환 — 반드시 이렇게: √x→sqrt(x), ³√x→root(3,x), Σ→sum(...), π→pi, ×→*, ÷→/, ≤→<=, ≥→>=, ≠→!=, x²→pow(x,2). 유니코드 수학기호가 하나라도 남으면 실패다.
JSON 문자열 안 백슬래시는 \\\\ 로 이스케이프.`;

const SYS_SCAN_PROBLEM = `너는 수학 문항 전사기다. 학생이 찍은 사진 속 "문항 하나"를 원문 그대로 옮긴다(오탈자 포함). 머리말·페이지 번호·배점 표기([3점] 등)·문항 번호는 뺀다.
사진에 문항이 여러 개면 가장 크게·가운데에 나온 하나만 옮기고, 잘려서 읽을 수 없으면 unreadable 을 true 로 한다.
${MATHIR_SPEC}

■ 출력 — 아래 JSON 하나만, 설명·마크다운 금지:
{"question":"문항 본문(마커 포함)", "choices":["①의 내용","②","③","④","⑤"] 또는 null,
 "qtype":"choice|short|essay", "figure_note":"그림·표·그래프가 있으면 그 구성을 수치까지 말로 짧게(없으면 null)",
 "unit_guess":"m1-1|m1-2|m2-1|m2-2|m3-1|m3-2|h1-1|h1-2|h2-1|h2-2|h3-1|h3-2|h3-3 중 하나 또는 null", "unreadable":false}
표는 figure_note 에 "표: 계급 0~10·10~20…, 도수 3·5·…" 처럼 수치를 다 적는다(풀이에 필요하다). 선택지는 있는 그대로, 없으면 null.`;

const SYS_SCAN_ANSWER = `너는 학생 손글씨 풀이(답안)를 옮겨 적는 전사기다. 사진 속 학생이 쓴 것만 줄 단위로 옮긴다. 인쇄된 문항 문장은 답안이 아니다 — 빼라.
수식은 평문으로(√ ² ³ / × ∠ △ π 등 사용, LaTeX 금지). 줄바꿈은 학생이 줄을 바꾼 대로. 지운 흔적은 [지움]으로.
글씨 상태도 본다(이 학생의 습관 진단·교정에 쓴다): 크기가 너무 작은가, 헷갈리는 글자(1과 7, 6과 0, x와 ×, b와 6, z와 2, 9와 q, +와 t 등), 줄 간격·정렬, 지운 흔적.
학생 책임의 필기 문제는 반드시 별도 kind 로 짚는다 —
 · messy: 글씨체가 엉망이라 알아보기 힘든 부분 · faint: 필압이 약해 너무 연한 부분
 · scribble: 한두 단으로 가지런하지 않고 끄적거려 풀이 흐름을 따라가기 어려움 · two_column: 풀이가 좌우 두 단으로 나뉨(단 사이를 잇는 화살표가 이미 있으면 제외)
이 네 종류는 해당 부분의 대략적 위치를 box(사진 기준 비율 좌표, 왼쪽 위 0,0 ~ 오른쪽 아래 1,1)로 함께 준다. 사진 전체가 그러면 box 는 전체를 덮게.

■ 출력 — 아래 JSON 하나만:
{"answer":"답안 전문(줄바꿈 \\n)", "lines":[{"text":"줄 내용","kind":"eq|text|answer|other"}], "final_answer":"학생이 최종 답으로 쓴 것(없으면 null)",
 "legibility":{"score":1~5, "issues":[{"kind":"size|messy|faint|glyph|spacing|crossout|scribble|two_column|other","note":"한 줄(예: 7 을 1 처럼 씀)","box":{"x":0.1,"y":0.2,"w":0.3,"h":0.1} 또는 null}]}, "unreadable":false}
읽기 불확실한 글자는 그대로 두되 물음표를 붙이지 말고 가장 그럴듯하게 읽는다. 학생 답안이 사진에 없으면 unreadable true.`;

const SYS_SCAN_PAGE = `이 이미지는 학생이 문제집 페이지에 풀이를 손으로 쓴 사진이다. 페이지 안의 "문항"과 각 문항 옆·아래의 "손글씨 풀이 영역"을 찾아 경계상자로 보고해라.
규칙: box 는 페이지 기준 비율 좌표 — 왼쪽 위 (0,0), 오른쪽 아래 (1,1). {"x":왼쪽,"y":위,"w":너비,"h":높이}. 문항 상자에는 번호·문장·수식·그림·보기가 전부 들어가게 넉넉히. 풀이 상자에는 그 문항의 손글씨만.
no 는 인쇄된 문항 번호(정수), 없으면 위에서부터. 2단이면 왼쪽 위→아래, 오른쪽 위→아래 순. 머리말·페이지 번호 제외.
출력은 아래 JSON 만: {"problems":[{"no":1,"box":{"x":0.05,"y":0.08,"w":0.42,"h":0.18}}], "answers":[{"no":1,"box":{...}}]}`;

const SYS_STD = `당신은 국내 중·고등 수학 교재 관행을 잘 아는 판정자다. 문항의 "표현에 저작자의 선택의 여지가 있는가"를 다섯 요소로 나누어 등급을 매긴다. 단원·수치·아이디어의 새로움은 판정 대상이 아니다.
요소: 발문(묻는 방식) · 조건제시(값·관계를 서술하는 방식과 순서) · 소재맥락(실생활 사물·인물·상황) · 도형자료(그림·표·그래프 구성) · 지문(앞에 붙은 서술·안내문·서사). 없는 요소는 "-".
등급: S 표준 = 이렇게밖에 쓸 수 없는 관용 표현 / M 소폭 선택 = 구조는 표준, 소재·명칭만 교체 가능(교재가 공유하는 정형 상황: 농도·속력·요금제·나이·과부족·일의 양·톱니바퀴 등, 관용 도형에 라벨 배치) / C 창작적 = 저작자 고유의 설정·서사·단계 절차 지문, 직접 구성한 표·그래프·패턴·도식, 조건을 지문 속에 분산.
주의: 관용 장치(번호 카드·주머니 속 공·주사위·동전·정n각형 꼭짓점·수직선 위 점)는 소재맥락 S. 경계가 애매하면 상위 등급. 문항 등급 = 요소 최고 등급.
세부 유형(실생활 소재나 자료가 있을 때만): 단순 소재 대입형 / 상황 설정형 / 자료 해석형, 아니면 "해당 없음".
출력은 아래 JSON 만: {"elements":{"발문":"S","조건제시":"S","소재맥락":"M","도형자료":"-","지문":"-"},"item_grade":"M","sub_type":"단순 소재 대입형","reason":"한 줄(문항 문장 인용 금지)"}`;

const SYS_APPROACH = `너는 한국 중·고등 수학 학원의 "문장 이해 선생님"이다. 학생이 찍은 문항의 문장을 함께 읽고 "식을 세우는 데까지만" 돕는다.
절대 규칙: 정답·최종 계산 결과·마지막 단계는 어떤 경우에도 쓰지 마라. 세운 식을 풀지 마라. 수식은 평문(× ÷ − ² √ a/b). 하위권 학생 대상 — 짧은 문장, 다정한 해요체.
아래 JSON 만 출력:
{"asking":"무엇을 구하라는지 한 문장", "clues":[{"text":"단서(문항 속 조건 그대로 짧게)","why":"이 단서가 왜 열쇠인지 한 문장"}],
 "concept":"떠올릴 개념·공식 이름(대입 결과 금지)", "first_step":"지금 종이에 쓸 첫 한 줄(변수 두기 등)",
 "setup":["세워야 할 식 1~2개(풀지 않음)"], "traps":["구하는대상혼동|부호|단위|단위환산|조건누락|역연산|평균오용|제곱누락|계산실수 중 이 문항에 해당하는 것만"],
 "reading":"문장을 끊어 읽는 요령 한두 문장"}`;

const SYS_ESSAY = `너는 한국 중·고등 수학 서술형 채점자다. 문항과 학생 답안을 보고 (1) 이 문항의 채점 기준표를 세우고 (2) 답안을 채점하고 (3) 첨삭한다.
채점 기준표 규격: 총점 5~8점, 핵심 요소 2~3개(활용 문항은 식 세우기 3 · 해 구하기 3 · 답 구하기 2 = 8점이 표준형), 요소마다 수행 수준 full(정확)/partial(부분)/zero. "실수거리"는 감점표가 아니라 이 문항에서 조심해야 할 것(빠지면 논리가 끊기는 진술, 선후를 바꿔 적기 쉬운 성질, 단위·부호).
첨삭: 틀린 곳은 어디가 왜 틀렸고 어떻게 고치는지 구체적으로. 맞았으면 더 좋게 쓰는 법 한 가지. 정답 자체를 통째로 새로 풀어 주지 말고 학생 답안을 기준으로 고쳐라. 다정한 해요체, 수식은 평문.
아래 JSON 만 출력:
{"rubric":[{"no":1,"element":"요소 이름","points":3,"criterion":"무엇을 쓰면 만점인지"}],
 "marks":[{"no":1,"level":"full|partial|zero","got":3,"comment":"근거 한 줄"}],
 "total":6,"max":8,"verdict":"excellent|good|partial|weak","final_answer_ok":true,
 "corrections":[{"where":"답안의 어느 줄/어느 식","wrong":"학생이 쓴 것","fix":"이렇게","why":"이유"}],
 "feedback":["한 줄 첨삭 1~3개"], "pitfall_tags":["구하는대상혼동|부호|단위|단위환산|조건누락|역연산|평균오용|제곱누락|계산실수 중 해당"], "praise":"잘한 점 한 줄"}`;

const SYS_PROCESS = `너는 한국 중·고등 수학 학원의 "풀이 과정 검사관"이다. 학생이 문제 옆에 쓴 풀이(한글 설명 없이 식만 이어질 수도 있다)를 보고 식과 식 사이의 연결고리를 검사한다.
검사 항목:
1) 연결고리: 줄마다 앞 줄에서 어떻게 왔는지(전개·이항·대입·계산). 건너뛴 곳은 "암산"으로 본다.
2) 암산 부담: 한 줄에서 다음 줄로 갈 때 머릿속에서 처리한 연산의 양(low/mid/high). high 면 실수 위험을 경고한다.
3) 습관: 글씨 크기·난잡함·헷갈리는 글자(전사 시 legibility 참고)·정렬·등호 맞추기·단위 누락 같은, 실수를 부르는 습관.
4) 오답이면 어디서 잘못됐는지 가장 그럴듯한 가설 한 줄(줄 번호 + 종류: 계산·개념·문제 해석·옮겨 적기·부호·단위)과 고치는 법.
5) 다섯 지표를 신호등(green/yellow/red)으로: 충실성(조건·단위·근거를 빠짐없이 썼나) · 논리성(단계 연결이 타당한가) · 명료성(남이 읽어도 따라갈 수 있게 정리됐나) · 간결성(군더더기 없이 — 단, 너무 간결해 암산이 과하면 오히려 yellow/red) · 독창성(관습적 풀이 대신 나름의 접근이 있는가 — 낮아도 나쁜 게 아니니 green/yellow 만).
다정한 해요체, 수식은 평문. 정답을 새로 풀어 주지 말고 학생 풀이를 기준으로 말해라.
아래 JSON 만 출력:
{"chain":[{"i":1,"text":"줄 내용 요약","role":"setup|transform|compute|answer|other","ok":true|false|null,"note":"앞 줄과의 연결 한 줄"}],
 "mental_load":"low|mid|high","mental_note":"암산에 대한 한 줄",
 "habits":[{"kind":"size|messy|glyph|align|unit|skip|other","note":"관찰","tip":"이렇게 고쳐요"}],
 "error":{"found":false,"line":null,"kind":"calc|concept|reading|transcription|sign|unit|none","hypothesis":"","fix":""},
 "criteria":{"충실성":{"light":"green","why":""},"논리성":{"light":"green","why":""},"명료성":{"light":"green","why":""},"간결성":{"light":"green","why":""},"독창성":{"light":"green","why":""}},
 "final_answer_ok":true,"summary":"두 문장 총평","pitfall_tags":["…"]}`;

// ─────────────────────────────────────────────────────────────── 태스크
function itemContext({ question, figure_note, choices }) {
  const parts = [`[문항]\n${str(question)}`];
  if (str(figure_note)) parts.push(`[그림·표]\n${str(figure_note, 1200)}`);
  const ch = arr(choices).slice(0, MAX_CHOICES).map((c, i) => `${["①", "②", "③", "④", "⑤"][i] || i + 1} ${str(c, 200)}`).filter(Boolean);
  if (ch.length) parts.push(`[선택지]\n${ch.join("\n")}`);
  return parts.join("\n\n");
}

/** 요소 등급 객체를 다섯 키 · S/M/C/- 값으로만 (클라이언트·모델 어느 쪽에서 와도 본문이 섞이지 않게) */
function cleanElements(src) {
  const el = {};
  for (const k of EL_KEYS) { const v = String(src?.[k] || "-"); el[k] = GRADES.includes(v) ? v : "-"; }
  return el;
}
const cleanTags = (v) => arr(v).map(String).filter((t) => TRAPS.includes(t)).slice(0, 6);

async function gradeStd(model, question, figure_note) {
  const text = await callClaude({ model, system: SYS_STD, content: [txt(itemContext({ question, figure_note }))], maxTokens: 400 });
  const p = parseObj(text);
  const el = cleanElements(p?.elements);
  let item_grade = GRADES.includes(p?.item_grade) ? p.item_grade : null;
  const top = Object.values(el).filter((v) => GRADES.includes(v)).sort((a, b) => GRADES.indexOf(b) - GRADES.indexOf(a))[0] || null;
  if (top && (!item_grade || GRADES.indexOf(top) > GRADES.indexOf(item_grade))) item_grade = top;   // 문항 등급 = 요소 최고 등급
  return { elements: el, item_grade, sub_type: str(p?.sub_type, 30) || "해당 없음", reason: str(p?.reason, 200) };
}

async function scanProblem(model, image, t0 = Date.now()) {
  let text = await callClaude({ model, system: SYS_SCAN_PROBLEM, content: [img(image), txt("이 사진의 문항을 전사해라.")], maxTokens: 2000 });
  let p = parseObj(text);
  let question = str(p?.question);
  const warnings = [];
  if (question) {
    const v = parseText(question);
    if (v.errs.length && Date.now() - t0 < TIME_BUDGET_MS * 0.5) {
      // 문법 오류 마커만 고쳐 달라고 한 번 더
      const bad = v.errs.slice(0, 6).map((e) => `[[${e.src}]] (${e.code}${e.msg ? ": " + String(e.msg).slice(0, 80) : ""})`).join("\n");
      try {
        text = await callClaude({ model, system: SYS_SCAN_PROBLEM,
          content: [img(image), txt(`앞선 전사에서 다음 마커가 MathIR 문법에 어긋났다:\n${bad}\n\n같은 문항을 문법에 맞게 다시 전사해 JSON 으로만 답해라.`)], maxTokens: 2000 });
        const p2 = parseObj(text);
        const q2 = str(p2?.question);
        if (q2 && parseText(q2).errs.length < v.errs.length) { p = p2; question = q2; }
      } catch { /* 재시도 실패는 무시 — 첫 결과를 쓴다 */ }
    }
    if (parseText(question).errs.length) warnings.push("수식 일부를 정확히 읽지 못했을 수 있어요");
  }
  const choices = arr(p?.choices).map((c) => str(c, 300)).filter(Boolean);
  return {
    question, choices: choices.length ? choices : null,
    qtype: ["choice", "short", "essay"].includes(p?.qtype) ? p.qtype : (choices.length ? "choice" : "short"),
    figure_note: str(p?.figure_note, 1200) || null,
    unit_guess: /^[mh]\d-\d$/.test(String(p?.unit_guess || "")) ? p.unit_guess : null,
    unreadable: !!p?.unreadable || !question,
    warnings,
  };
}

const HW_KINDS = ["size", "messy", "faint", "glyph", "spacing", "crossout", "scribble", "two_column", "other"];
function cleanBox(b) {
  if (!b || ![b.x, b.y, b.w, b.h].every((v) => Number.isFinite(+v))) return null;
  return { x: clamp01(b.x), y: clamp01(b.y), w: Math.max(0.02, clamp01(b.w)), h: Math.max(0.02, clamp01(b.h)) };
}
async function scanAnswer(model, image) {
  const text = await callClaude({ model, system: SYS_SCAN_ANSWER, content: [img(image), txt("이 사진의 학생 풀이를 전사해라.")], maxTokens: 2000 });
  const p = parseObj(text);
  const lines = arr(p?.lines).map((l) => ({ text: str(l?.text, 300), kind: ["eq", "text", "answer", "other"].includes(l?.kind) ? l.kind : "other" })).filter((l) => l.text);
  const answer = str(p?.answer) || lines.map((l) => l.text).join("\n");
  const issues = arr(p?.legibility?.issues)
    .map((i) => ({ kind: HW_KINDS.includes(i?.kind) ? i.kind : "other", note: str(i?.note, 120), box: cleanBox(i?.box) }))
    .filter((i) => i.note).slice(0, 8);
  const score = Math.min(5, Math.max(1, Math.round(+p?.legibility?.score || 3)));
  return { answer, lines, final_answer: str(p?.final_answer, 120) || null, legibility: { score, issues }, unreadable: !!p?.unreadable || !answer };
}

async function scanPage(model, image) {
  const text = await callClaude({ model, system: SYS_SCAN_PAGE, content: [img(image), txt("문항과 풀이 영역의 경계상자를 보고해라.")], maxTokens: 1500 });
  const p = parseObj(text);
  const fix = (list) => {
    const rows = arr(list).filter((x) => x && Number.isFinite(+x.no) && x.box && [x.box.x, x.box.y, x.box.w, x.box.h].every((v) => Number.isFinite(+v)))
      .map((x) => ({ no: Math.round(+x.no), box: { x: clamp01(x.box.x), y: clamp01(x.box.y), w: Math.max(0.02, clamp01(x.box.w)), h: Math.max(0.02, clamp01(x.box.h)) } }));
    const byNo = new Map();                                   // 같은 번호가 둘이면 넓은 상자만
    for (const r of rows) { const o = byNo.get(r.no); if (!o || r.box.w * r.box.h > o.box.w * o.box.h) byNo.set(r.no, r); }
    return [...byNo.values()].sort((a, b) => a.no - b.no).slice(0, 30);
  };
  return { problems: fix(p?.problems), answers: fix(p?.answers) };
}

async function approach(model, body) {
  const text = await callClaude({ model, system: SYS_APPROACH, content: [txt(itemContext(body))], maxTokens: 1200 });
  const p = parseObj(text);
  return {
    asking: str(p?.asking, 200), clues: arr(p?.clues).map((c) => ({ text: str(c?.text, 160), why: str(c?.why, 200) })).filter((c) => c.text).slice(0, 6),
    concept: str(p?.concept, 200), first_step: str(p?.first_step, 300), setup: arr(p?.setup).map((s) => str(s, 200)).filter(Boolean).slice(0, 3),
    traps: cleanTags(p?.traps), reading: str(p?.reading, 300),
  };
}

async function essay(model, body) {
  const content = [txt(itemContext(body) + `\n\n[학생 답안]\n${str(body.answer)}`)];
  const text = await callClaude({ model, system: SYS_ESSAY, content, maxTokens: 2200 });
  const p = parseObj(text);
  const rubric = arr(p?.rubric).map((r, i) => ({ no: Number.isFinite(+r?.no) ? +r.no : i + 1, element: str(r?.element, 60), points: Math.max(0, Math.round(+r?.points || 0)), criterion: str(r?.criterion, 300) })).filter((r) => r.element).slice(0, 5);
  const marks = arr(p?.marks).map((m, i) => ({ no: Number.isFinite(+m?.no) ? +m.no : i + 1, level: ["full", "partial", "zero"].includes(m?.level) ? m.level : "partial", got: Math.max(0, +m?.got || 0), comment: str(m?.comment, 300) })).slice(0, 5);
  const max = rubric.reduce((s, r) => s + r.points, 0) || Math.max(0, Math.round(+p?.max || 0));
  const total = Math.min(max, marks.reduce((s, m) => s + m.got, 0) || Math.max(0, Math.round(+p?.total || 0)));
  return {
    rubric, marks, total, max,
    verdict: ["excellent", "good", "partial", "weak"].includes(p?.verdict) ? p.verdict : (max && total / max >= 0.9 ? "excellent" : max && total / max >= 0.6 ? "good" : total ? "partial" : "weak"),
    final_answer_ok: !!p?.final_answer_ok,
    corrections: arr(p?.corrections).map((c) => ({ where: str(c?.where, 120), wrong: str(c?.wrong, 200), fix: str(c?.fix, 300), why: str(c?.why, 300) })).filter((c) => c.fix).slice(0, 6),
    feedback: arr(p?.feedback).map((f) => str(f, 300)).filter(Boolean).slice(0, 4),
    pitfall_tags: cleanTags(p?.pitfall_tags), praise: str(p?.praise, 200),
  };
}

async function processCheck(model, body) {
  const lines = arr(body.lines).slice(0, MAX_LINES).map((l, i) => `${i + 1}) ${str(l?.text, 300)}`).join("\n");
  const leg = body.legibility ? `\n\n[글씨 상태(전사기 관찰)] 점수 ${body.legibility.score}/5 · ${arr(body.legibility.issues).map((i) => `${i.kind}: ${i.note}`).join(" · ") || "특이점 없음"}` : "";
  const content = [txt(itemContext(body) + `\n\n[학생 풀이 — 줄 번호 순]\n${lines || str(body.answer)}${leg}`)];
  const text = await callClaude({ model, system: SYS_PROCESS, content, maxTokens: 2500 });
  const p = parseObj(text);
  const CR = ["충실성", "논리성", "명료성", "간결성", "독창성"];
  const criteria = {};
  for (const k of CR) criteria[k] = { light: light(p?.criteria?.[k]?.light), why: str(p?.criteria?.[k]?.why, 200) };
  return {
    chain: arr(p?.chain).map((c, i) => ({ i: Number.isFinite(+c?.i) ? +c.i : i + 1, text: str(c?.text, 200), role: ["setup", "transform", "compute", "answer", "other"].includes(c?.role) ? c.role : "other", ok: c?.ok === true ? true : c?.ok === false ? false : null, note: str(c?.note, 200) })).slice(0, 40),
    mental_load: ["low", "mid", "high"].includes(p?.mental_load) ? p.mental_load : "mid", mental_note: str(p?.mental_note, 300),
    habits: arr(p?.habits).map((h) => ({ kind: ["size", "messy", "glyph", "align", "unit", "skip", "other"].includes(h?.kind) ? h.kind : "other", note: str(h?.note, 200), tip: str(h?.tip, 200) })).filter((h) => h.note).slice(0, 6),
    error: { found: !!p?.error?.found, line: Number.isFinite(+p?.error?.line) ? +p.error.line : null, kind: ["calc", "concept", "reading", "transcription", "sign", "unit", "none"].includes(p?.error?.kind) ? p.error.kind : (p?.error?.found ? "calc" : "none"), hypothesis: str(p?.error?.hypothesis, 300), fix: str(p?.error?.fix, 300) },
    criteria, final_answer_ok: !!p?.final_answer_ok, summary: str(p?.summary, 400), pitfall_tags: cleanTags(p?.pitfall_tags),
  };
}

/** 보관 게이트: 라벨은 항상, 원문은 결정이 central 일 때만. 표가 없으면(마이그레이션 전) saved:false 로 조용히 */
async function retain({ uid, feature, question, answer, std, result, policy, unit }) {
  const overlap = overlapScore(question, answer);
  const decision = decideRetention({ grade: std?.item_grade || null, overlap, policy });
  const labels = buildLabels({ feature, std, overlap, result, unit });
  const out = { where: decision.where, reason: decision.reason, policy, overlap: { score: overlap.score, level: overlap.level, sentences: overlap.sentences, words: overlap.words, nums: overlap.nums }, saved: false, central: false };
  const db = svcClient();
  if (!db) return out;
  try {
    const { data, error } = await db.from("photo_answer_labels").insert({ ...labels, user_id: uid, retention: decision.where, policy }).select("id").single();
    if (error) throw error;
    out.saved = true;
    if (decision.where === "central") {
      const { error: e2 } = await db.from("photo_answers").insert({ label_id: data.id, user_id: uid, answer_text: str(answer) });
      if (!e2) out.central = true;
    }
  } catch (e) {
    if (!missingRel(e)) out.error = "기록 저장 실패";
  }
  return out;
}

// ─────────────────────────────────────────────────────────────── 핸들러
export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST만 지원해요" });
  const t0 = Date.now();
  try {
    const auth = req.headers.authorization || "";
    const token = auth.startsWith("Bearer ") ? auth.slice(7) : null;
    if (!token) return res.status(401).json({ error: "로그인이 필요해요" });
    const url = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
    const anon = process.env.VITE_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY;
    if (!url || !anon) return res.status(500).json({ error: "Supabase 환경변수가 없어요" });
    const sb = createClient(url, anon, { global: { headers: { Authorization: `Bearer ${token}` } } });
    const { data: userData, error: uErr } = await sb.auth.getUser(token);
    if (uErr || !userData?.user) return res.status(401).json({ error: "인증 실패" });
    const uid = userData.user.id;
    if (!process.env.ANTHROPIC_API_KEY) return res.status(500).json({ error: "ANTHROPIC_API_KEY가 Vercel에 설정되지 않았어요" });

    const body = req.body || {};
    const task = String(body.task || "");
    if (!["scan", "approach", "essay", "process"].includes(task)) return res.status(400).json({ error: "알 수 없는 task: " + task });

    // 학생 자격 게이트 (ai.js 와 동일)
    const { data: prof } = await sb.from("profiles").select("role, member_code").eq("id", uid).single();
    if (prof?.role !== "admin") {
      if (prof?.role === "trial") return res.status(403).json({ error: "체험 계정은 개념 열람만 가능해요 — 정식 가입 후 이용할 수 있어요" });
      if (!prof?.member_code) return res.status(403).json({ error: "AI 기능은 학원 고유번호 등록 후 열려요 — 학원에서 고유번호를 받아 등록해주세요" });
    }
    // 입력 검증은 한도 차감보다 먼저 (잘못된 요청이 하루치 호출을 갉아먹지 않게)
    const image = typeof body.image === "string" ? body.image : "";
    const question = str(body.question);
    const answer = str(body.answer);
    if (task === "scan") {
      if (!image) return res.status(400).json({ error: "이미지가 없어요" });
      if (image.length > MAX_IMAGE_B64) return res.status(413).json({ error: "사진이 너무 커요 — 다시 찍어 주세요" });
    } else {
      if (!question) return res.status(400).json({ error: "문항 텍스트가 없어요 — 먼저 문항을 찍어 주세요" });
      if (task !== "approach" && !answer) return res.status(400).json({ error: "답안 텍스트가 없어요 — 먼저 답안을 찍어 주세요" });
    }

    const capMsg = await checkCap(sb, uid, "photo_" + task);
    if (capMsg) return res.status(429).json({ error: capMsg });

    const st = await settings(sb, ["photo_model", "photo_model_grade", "photo_model_fallback", "photo_retention"]);
    let model = st.photo_model || DEFAULT_MODEL;
    const gradeModel = st.photo_model_grade || DEFAULT_GRADE_MODEL;
    const policy = normalizePolicy(st.photo_retention);

    if (task === "scan") {
      // 1차 전사가 실패했을 때만 클라이언트가 retry_strong 을 보낸다 → 강한(폴백) 모델로 다시 읽는다
      if (body.retry_strong === true) model = st.photo_model_fallback || gradeModel;
      const mode = ["problem", "answer", "page"].includes(body.mode) ? body.mode : "problem";
      if (mode === "page") return res.status(200).json({ mode, ...(await scanPage(model, image)), model });
      if (mode === "answer") return res.status(200).json({ mode, ...(await scanAnswer(model, image)), model });
      const scanned = await scanProblem(model, image, t0);
      let std = null;   // 등급 판정은 시간이 남을 때만 — 없으면 게이트가 device(안전한 쪽)로 둔다
      if (!scanned.unreadable && Date.now() - t0 < TIME_BUDGET_MS * 0.7) { try { std = await gradeStd(model, scanned.question, scanned.figure_note); } catch { std = null; } }
      return res.status(200).json({ mode, ...scanned, std, policy, model });
    }

    const ctx = { question, figure_note: str(body.figure_note, 1200), choices: arr(body.choices).slice(0, MAX_CHOICES).map((c) => str(c, 300)) };

    if (task === "approach") return res.status(200).json({ ...(await approach(model, ctx)), model });

    // 클라이언트가 보낸 등급은 값만 받는다(요소 객체도 다섯 키·S/M/C 로만) — 라벨 표에 본문이 섞이지 않게
    let std = body.std && GRADES.includes(body.std.item_grade)
      ? { item_grade: body.std.item_grade, sub_type: str(body.std.sub_type, 30), elements: cleanElements(body.std.elements) }
      : null;
    if (!std) { try { std = await gradeStd(model, question, ctx.figure_note); } catch { std = null; } }
    const unit = /^[mh]\d-\d$/.test(String(body.unit || "")) ? body.unit : null;

    if (task === "essay") {
      const result = await essay(gradeModel, { ...ctx, answer });
      const retention = await retain({ uid, feature: "essay", question, answer, std, result, policy, unit });
      return res.status(200).json({ result, std, retention, model: gradeModel });
    }
    if (task === "process") {
      const result = await processCheck(gradeModel, { ...ctx, answer, lines: body.lines, legibility: body.legibility });
      const retention = await retain({ uid, feature: "check", question, answer, std, result, policy, unit });
      return res.status(200).json({ result, std, retention, model: gradeModel });
    }
    return res.status(400).json({ error: "알 수 없는 task" });
  } catch (err) {
    // 우리가 만든 메시지(AI 호출·해석 실패)만 그대로, 나머지(DB·라이브러리 오류)는 일반 문구로 — 내부 이름이 새지 않게
    const m = String(err?.message || "");
    return res.status(500).json({ error: /^AI /.test(m) ? m : "서버 오류가 났어요 — 잠시 뒤 다시 시도해 주세요" });
  }
}
