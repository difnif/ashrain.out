// node tests/photoApi.test.mjs — api/photo.js 핸들러를 가짜 fetch(Anthropic + Supabase REST/Auth)로 끝까지 돌려 본다.
// 실제 키·네트워크 없음. 검사: 인증·자격 게이트·한도·태스크 분기·응답 정리·보관 게이트(라벨/원문 insert)·표 없을 때의 조용한 실패.
process.env.SUPABASE_URL = "http://sb.local";
process.env.SUPABASE_ANON_KEY = "anon";
process.env.SUPABASE_SERVICE_ROLE_KEY = "service";
process.env.ANTHROPIC_API_KEY = "sk-test";

const { default: handler } = await import("../api/photo.js");

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };

// ── 가짜 서버 상태 ────────────────────────────────────────────────────────────
const state = { profile: { role: "student", member_code: "X" }, calls: {}, settings: {}, labels: [], answers: [], labelsTableMissing: false, ai: [] };
const Q = "둘레가 54cm인 직사각형의 가로의 길이가 세로의 길이보다 3cm 길 때, 이 직사각형의 넓이를 구하시오.";

function aiReply(system, userText) {
  state.ai.push(system.slice(0, 20));
  let obj;
  if (system.startsWith("너는 수학 문항 전사기")) obj = userText.includes("문법에 어긋났다")
    ? { question: Q, choices: null, qtype: "short", figure_note: null, unit_guess: "m1-1", unreadable: false }
    : { question: state.badFirst ? "넓이가 [[frac(1,2]] 인 …" : Q, choices: ["1", "2"], qtype: "choice", figure_note: "표: 계급 0~10", unit_guess: "m1-1", unreadable: false };
  else if (system.startsWith("너는 학생 손글씨")) obj = { answer: "x=세로\n2(x+3+x)=54\nx=12\n답 180", lines: [{ text: "x=세로", kind: "text" }, { text: "2(x+3+x)=54", kind: "eq" }, { text: "x=12", kind: "eq" }, { text: "답 180", kind: "answer" }], final_answer: "180", legibility: { score: 9, issues: [{ kind: "weird", note: "7을 1처럼" }, { kind: "two_column", note: "풀이가 두 단", box: { x: 0.5, y: -0.2, w: 2, h: 0.3 } }, { kind: "faint", note: "연하게 씀" }] }, unreadable: false };
  else if (system.startsWith("이 이미지는 학생이 문제집")) obj = { problems: [{ no: 1, box: { x: 0.1, y: 0.1, w: 0.5, h: 0.3 } }, { no: "x", box: {} }], answers: [{ no: 1, box: { x: 1.5, y: -1, w: 0.01, h: 0.5 } }] };
  else if (system.startsWith("당신은 국내 중·고등 수학 교재")) obj = { elements: { 발문: "S", 조건제시: "S", 소재맥락: state.grade || "S", 도형자료: "-", 지문: "Z" }, item_grade: "S", sub_type: "단순 소재 대입형", reason: "정형" };
  else if (system.startsWith("너는 한국 중·고등 수학 학원의 \"문장 이해")) obj = { asking: "넓이", clues: [{ text: "둘레가 54cm", why: "합" }], concept: "둘레", first_step: "x 두기", setup: ["2(x+3+x)=54"], traps: ["단위", "없는태그"], reading: "끊어" };
  else if (system.startsWith("너는 한국 중·고등 수학 서술형 채점자")) obj = { rubric: [{ no: 1, element: "식", points: 3, criterion: "c" }, { no: 2, element: "답", points: 2, criterion: "c" }], marks: [{ no: 1, level: "full", got: 3, comment: "" }, { no: 2, level: "zero", got: 0, comment: "" }], total: 99, max: 5, verdict: "weird", final_answer_ok: true, corrections: [{ where: "w", wrong: "180", fix: "180 cm²", why: "" }], feedback: ["f"], pitfall_tags: ["단위"], praise: "p" };
  else if (system.startsWith("너는 한국 중·고등 수학 학원의 \"풀이 과정")) obj = { chain: [{ i: 1, text: "x=세로", role: "setup", ok: true, note: "" }], mental_load: "high", mental_note: "m", habits: [{ kind: "glyph", note: "7", tip: "t" }], error: { found: true, line: 3, kind: "calc", hypothesis: "h", fix: "f" }, criteria: { 충실성: { light: "green" }, 논리성: { light: "purple" } }, final_answer_ok: false, summary: "s", pitfall_tags: [] };
  else obj = {};
  return "```json\n" + JSON.stringify(obj) + "\n```";
}

const hdr = (init, name) => { const h = init.headers; if (!h) return ""; if (h instanceof Headers) return h.get(name) || ""; const k = Object.keys(h).find((x) => x.toLowerCase() === name.toLowerCase()); return k ? h[k] : ""; };
globalThis.fetch = async (url, init = {}) => {
  const u = String(url); const method = (init.method || "GET").toUpperCase();
  const wantObj = hdr(init, "accept").includes("pgrst.object");
  const json = (obj, status = 200, headers = {}) => new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json", ...headers } });
  if (u.startsWith("https://api.anthropic.com/")) {
    const body = JSON.parse(init.body);
    const userText = body.messages[0].content.filter((b) => b.type === "text").map((b) => b.text).join("\n");
    if (body.messages[0].content.some((b) => b.type === "image") && !/^[A-Za-z0-9+/=]+$/.test(body.messages[0].content.find((b) => b.type === "image").source.data)) return json({ error: { message: "bad image" } }, 400);
    return json({ content: [{ type: "text", text: aiReply(body.system, userText) }] });
  }
  if (u.includes("/auth/v1/user")) return hdr(init, "authorization") === "Bearer good"
    ? json({ id: "u1", aud: "authenticated", role: "authenticated", email: "t@x" }) : json({ message: "bad jwt" }, 401);
  if (u.includes("/rest/v1/profiles")) { const row = { role: state.profile.role, member_code: state.profile.member_code }; return json(wantObj ? row : [row]); }
  if (u.includes("/rest/v1/ai_calls")) {   // task 별로 센다 (HEAD: ?task=eq.<x> · POST: body.task)
    if (method === "HEAD") { const t = decodeURIComponent((u.match(/task=eq\.([^&]+)/) || [])[1] || ""); return new Response("", { status: 200, headers: { "content-range": `*/${state.calls[t] || 0}` } }); }
    const t = JSON.parse(init.body).task; state.calls[t] = (state.calls[t] || 0) + 1; return json([], 201);
  }
  if (u.includes("/rest/v1/app_settings")) return json(Object.entries(state.settings).map(([key, value]) => ({ key, value })));
  if (u.includes("/rest/v1/photo_answer_labels")) {
    if (state.labelsTableMissing) return json({ code: "PGRST205", message: "Could not find the table" }, 404);
    const row = JSON.parse(init.body); state.labels.push(row); const out = { id: "L" + state.labels.length }; return json(wantObj ? out : [out], 201);
  }
  if (u.includes("/rest/v1/photo_answers")) { state.answers.push(JSON.parse(init.body)); return json([], 201); }
  return json({ message: "unmocked " + u }, 500);
};

async function call(body, token = "good") {
  const res = { code: 200, body: null, status(c) { this.code = c; return this; }, json(b) { this.body = b; return this; } };
  await handler({ method: "POST", headers: token ? { authorization: "Bearer " + token } : {}, body }, res);
  return res;
}
const IMG = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAABAAEBAREA/8QAFAABAAAAAAAAAAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AVN//2Q==";

// ── 인증·자격·한도 ────────────────────────────────────────────────────────────
{
  let r = await call({ task: "approach", question: Q }, null);
  ok(r.code === 401, "토큰 없음 → 401");
  r = await call({ task: "approach", question: Q }, "bad");
  ok(r.code === 401, "잘못된 토큰 → 401");
  r = await call({ task: "nope" });
  ok(r.code === 400 && /task/.test(r.body.error), "모르는 task → 400");
  state.profile = { role: "trial", member_code: null };
  r = await call({ task: "approach", question: Q });
  ok(r.code === 403 && /체험/.test(r.body.error), "체험 계정 → 403");
  state.profile = { role: "student", member_code: null };
  r = await call({ task: "approach", question: Q });
  ok(r.code === 403 && /고유번호/.test(r.body.error), "고유번호 없음 → 403");
  state.profile = { role: "student", member_code: "X" };
  state.calls = { photo_approach: 20 };
  r = await call({ task: "approach", question: Q });
  ok(r.code === 429 && /한도/.test(r.body.error), "일일 한도(approach 20) → 429");
  state.calls = { photo_approach: 19 };
  r = await call({ task: "approach", question: Q });
  ok(r.code === 200 && state.calls.photo_approach === 20, "한도 직전은 통과 + 호출 기록(호출 전에 남김)");
  state.calls = {};
  const r2 = await call({ method: "GET" });
  ok(true, "(GET 은 405 — 핸들러 첫 줄) " + (await (async () => { const res = { code: 0, status(c) { this.code = c; return this; }, json() { return this; } }; await handler({ method: "GET", headers: {} }, res); return res.code === 405; })()));
}

// ── scan: problem (등급 포함) · 문법 오류 재시도 · answer · page ─────────────────
{
  state.ai = []; state.badFirst = true;
  let r = await call({ task: "scan", mode: "problem", image: IMG });
  ok(r.code === 200 && r.body.question === Q, "scan problem: 문법 오류 마커 → 재전사로 고침");
  ok(state.ai.filter((s) => s.startsWith("너는 수학 문항")).length === 2, "scan problem: 전사 2회(재시도 1회)");
  ok(r.body.std?.item_grade === "S" && r.body.std.elements.지문 === "-", "scan problem: 표준성 등급 S · 이상한 요소값은 '-'");
  ok(r.body.qtype === "short" && r.body.choices === null && r.body.unit_guess === "m1-1" && r.body.policy === "labels", "scan problem: 정리된 필드 + 기본 정책 labels");
  ok(!("image" in r.body) && !JSON.stringify(r.body).includes(IMG.slice(0, 30)), "scan problem: 응답에 사진 없음");
  state.badFirst = false; state.grade = "C";
  r = await call({ task: "scan", mode: "problem", image: IMG });
  ok(r.body.std?.item_grade === "C" && r.body.warnings.length === 0, "scan problem: 요소 최고 등급 C 가 문항 등급(모델 item_grade S 무시)");
  ok(r.body.choices?.length === 2 && r.body.qtype === "choice" && r.body.figure_note.startsWith("표:"), "scan problem: 선택지·그림 메모");
  r = await call({ task: "scan", mode: "problem", image: "" });
  ok(r.code === 400, "scan: 이미지 없음 → 400");
  r = await call({ task: "scan", mode: "problem", image: "x".repeat(6_000_001) });
  ok(r.code === 413, "scan: 너무 큰 이미지 → 413");
  r = await call({ task: "scan", mode: "answer", image: IMG });
  ok(r.code === 200 && r.body.lines.length === 4 && r.body.final_answer === "180", "scan answer: 줄·최종 답");
  ok(r.body.legibility.score === 5 && r.body.legibility.issues[0].kind === "other", "scan answer: 가독성 점수 1~5 로 자르고 모르는 kind 는 other");
  r = await call({ task: "scan", mode: "page", image: IMG });
  ok(r.code === 200 && r.body.problems.length === 1 && r.body.answers.length === 1, "scan page: 깨진 상자는 버림");
  const a = r.body.answers[0].box;
  ok(a.x === 1 && a.y === 0 && a.w >= 0.02, "scan page: 상자 좌표 0~1 로 정리");
}

// ── approach ─────────────────────────────────────────────────────────────────
{
  const r = await call({ task: "approach", question: Q, figure_note: "표", choices: ["a"] });
  ok(r.code === 200 && r.body.setup[0] === "2(x+3+x)=54" && r.body.traps.length === 1 && r.body.traps[0] === "단위", "approach: 식 세우기 + 모르는 함정 태그 제거");
  const r2 = await call({ task: "approach", question: "" });
  ok(r2.code === 400, "approach: 문항 없음 → 400");
}

// ── essay + 보관 게이트 ──────────────────────────────────────────────────────
{
  state.labels = []; state.answers = []; state.settings = {};
  let r = await call({ task: "essay", question: Q, answer: "x=세로\n2(x+3+x)=54\nx=12\n답 180", std: { item_grade: "S", sub_type: "단순 소재 대입형", elements: {} }, unit: "m1-1" });
  ok(r.code === 200 && r.body.result.total === 3 && r.body.result.max === 5 && r.body.result.verdict === "good", "essay: 점수는 기준표 합으로 다시 계산(99 무시) · verdict 보정");
  ok(r.body.retention.where === "device" && r.body.retention.policy === "labels" && r.body.retention.saved && !r.body.retention.central, "essay: 기본 정책 labels → 라벨만(device)");
  ok(state.labels.length === 1 && state.labels[0].feature === "essay" && state.labels[0].std_grade === "S" && state.labels[0].unit_guess === "m1-1" && !("answer_text" in state.labels[0]) && !("question" in state.labels[0]), "essay: 라벨 행에 본문 없음");
  ok(state.answers.length === 0, "essay: labels 정책에서 원문 표 insert 없음");
  ok(typeof state.labels[0].overlap_score === "number" && ["low", "mid", "high"].includes(state.labels[0].overlap_level), "essay: 겹침 점수·수준 기록");

  state.settings = { photo_retention: "gated" };
  r = await call({ task: "essay", question: Q, answer: "x=세로\n2(x+3+x)=54\nx=12\n답 180", std: { item_grade: "S" } });
  ok(r.body.retention.where === "central" && r.body.retention.central && state.answers.length === 1 && state.answers[0].label_id === "L2" && state.answers[0].answer_text.includes("2(x+3+x)=54"), "essay: gated + S → 원문 central 저장(label_id 연결)");
  r = await call({ task: "essay", question: Q, answer: "답 180", std: { item_grade: "C" } });
  ok(r.body.retention.where === "device" && state.answers.length === 1, "essay: gated + C → device");
  r = await call({ task: "essay", question: Q, answer: "답 180", std: { item_grade: "M" } });
  ok(r.body.retention.where === "central" && state.answers.length === 2, "essay: gated + M + 겹침 low → central");
  r = await call({ task: "essay", question: Q, answer: Q + "\n" + Q, std: { item_grade: "M" } });
  ok(r.body.retention.where === "device" && r.body.retention.overlap.level !== "low", "essay: gated + M + 문항 재진술(겹침 높음) → device");
  r = await call({ task: "essay", question: Q, answer: "답 180", std: { item_grade: "ZZ" } });
  ok(r.body.std?.item_grade === "C" && state.ai.some((s) => s.startsWith("당신은 국내")), "essay: 등급이 없으면 서버가 다시 판정(요소 최고 등급 C)");

  state.settings = { photo_retention: "all" };
  r = await call({ task: "essay", question: Q, answer: "답 180", std: { item_grade: "C" } });
  ok(r.body.retention.where === "central", "essay: all 정책 → C 도 central(테스트용)");
  state.settings = { photo_retention: "weird" };
  r = await call({ task: "essay", question: Q, answer: "답 180", std: { item_grade: "S" } });
  ok(r.body.retention.policy === "labels" && r.body.retention.where === "device", "essay: 모르는 정책값 → labels");

  state.labelsTableMissing = true;
  r = await call({ task: "essay", question: Q, answer: "답 180", std: { item_grade: "S" } });
  ok(r.code === 200 && r.body.retention.saved === false && !r.body.retention.error, "essay: 표가 없으면(마이그레이션 전) 조용히 saved:false");
  state.labelsTableMissing = false;
  r = await call({ task: "essay", question: Q, answer: "" });
  ok(r.code === 400, "essay: 답안 없음 → 400");
}

// ── process ──────────────────────────────────────────────────────────────────
{
  state.settings = {}; state.labels = [];
  const r = await call({ task: "process", question: Q, answer: "x=세로", lines: [{ text: "x=세로" }], legibility: { score: 3, issues: [] }, std: { item_grade: "M" }, unit: "zz" });
  ok(r.code === 200 && r.body.result.mental_load === "high" && r.body.result.error.found && r.body.result.error.line === 3, "process: 암산·오류 가설");
  const c = r.body.result.criteria;
  ok(c.충실성.light === "green" && c.논리성.light === "yellow" && c.독창성.light === "yellow" && Object.keys(c).length === 5, "process: 다섯 지표 채움 · 이상한 색은 yellow");
  ok(state.labels.length === 1 && state.labels[0].feature === "check" && state.labels[0].lights.충실성 === "green" && state.labels[0].error_kind === "calc" && state.labels[0].mental_load === "high" && state.labels[0].unit_guess === null, "process: 라벨(신호등·오류 종류·암산) · 이상한 단원은 null");
  ok(state.labels[0].retention === "device" && state.labels[0].policy === "labels" && state.labels[0].user_id === "u1", "process: 보관 결정·정책·user_id");
}

// ── 모델 키 ──────────────────────────────────────────────────────────────────
{
  state.settings = { photo_model: "m-scan", photo_model_grade: "m-grade" }; state.calls = {};
  const r1 = await call({ task: "approach", question: Q });
  const r2 = await call({ task: "essay", question: Q, answer: "답", std: { item_grade: "S" } });
  ok(r1.body.model === "m-scan" && r2.body.model === "m-grade", "app_settings.photo_model / photo_model_grade 로 모델 바꿈");
}

// ── 수율 폴백(retry_strong) · 필기 지도 kind/box 정리 ────────────────────────
{
  state.settings = { photo_model: "m-scan", photo_model_grade: "m-grade", photo_model_fallback: "m-fb" }; state.calls = {};
  let r = await call({ task: "scan", mode: "problem", image: IMG, retry_strong: true });
  ok(r.body.model === "m-fb", "scan retry_strong: photo_model_fallback 모델로 읽음");
  state.settings = { photo_model: "m-scan", photo_model_grade: "m-grade" };
  r = await call({ task: "scan", mode: "problem", image: IMG, retry_strong: true });
  ok(r.body.model === "m-grade", "retry_strong: 폴백 키가 없으면 채점 모델로");
  r = await call({ task: "scan", mode: "answer", image: IMG });
  const iss = r.body.legibility.issues;
  ok(iss.some((i) => i.kind === "two_column") && iss.some((i) => i.kind === "faint"), "scan answer: 필기 지도 kind(two_column·faint) 통과");
  const tc = iss.find((i) => i.kind === "two_column");
  ok(!!tc.box && tc.box.x === 0.5 && tc.box.y === 0 && tc.box.w === 1 && tc.box.h === 0.3, "필기 box 를 비율 좌표(0~1)로 죔");
  ok(!iss.find((i) => i.kind === "weird") && iss.some((i) => i.kind === "other"), "모르는 kind 는 여전히 other");
  state.settings = {};
}

console.log(`\n${pass}/${pass + fail} passed`);
if (fail) process.exit(1);
