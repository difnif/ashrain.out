// node tests/assessApi.test.mjs — 서술형 평가 서버(api/photo.js → api/_lib/assess.js)를 가짜 Supabase(PostgREST 흉내) + 가짜 Anthropic 으로 끝까지.
// 실제 키·네트워크 없음. 검사: 등록(관리자)·열람(공개 분리)·비로그인 시작/이어 하기·쪽 판독/채점·재시도 한도·호출 한도·2쪽 확인·제출·공개 시점·이의·로그인 담기·관리자 조회.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
process.env.SUPABASE_URL = "http://sb.local";
process.env.SUPABASE_ANON_KEY = "anon";
process.env.SUPABASE_SERVICE_ROLE_KEY = "service";
process.env.ANTHROPIC_API_KEY = "sk-test";
const { default: handler } = await import("../api/photo.js");
const HERE = path.dirname(fileURLToPath(import.meta.url));
const SPEC = JSON.parse(fs.readFileSync(path.join(HERE, "fixtures/assess-SAMPLE01.json"), "utf8"));

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };

// ── 가짜 DB ───────────────────────────────────────────────────────────────────
const USERS = { "tok-admin": { id: "a0000000-0000-4000-8000-00000000000a" }, "tok-stu": { id: "b0000000-0000-4000-8000-00000000000b" } };
const db = {
  profiles: [{ id: USERS["tok-admin"].id, role: "admin", username: "원장", name: "박선생" }, { id: USERS["tok-stu"].id, role: "student", username: "민준이", name: "김민준", grade: "중2" }],
  app_settings: [], assess_sets: [], assess_people: [], assess_sessions: [], assess_pages: [], assess_calls: [],
};
const PK = { assess_pages: ["session_id", "page_no"], app_settings: ["key"] };
let missing = false;                    // true 면 assess_* 표가 없는 척(마이그레이션 전)
const storage = [];
const ai = [];                          // [{model, sys}]
const uuid = () => "xxxxxxxx-xxxx-4xxx-8xxx-xxxxxxxxxxxx".replace(/x/g, () => "0123456789abcdef"[Math.floor(Math.random() * 16)]);

function applyFilters(rows, sp) {
  let out = rows;
  for (const [k, v] of sp.entries()) {
    if (["select", "order", "limit", "on_conflict", "columns", "offset"].includes(k)) continue;
    const m = v.match(/^(eq|in|gte|lte|neq)\.(.*)$/s);
    if (!m) continue;
    const [, op, val] = m;
    if (op === "eq") out = out.filter((r) => String(r[k]) === val);
    if (op === "neq") out = out.filter((r) => String(r[k]) !== val);
    if (op === "gte") out = out.filter((r) => r[k] != null && String(r[k]) >= val);
    if (op === "lte") out = out.filter((r) => r[k] != null && String(r[k]) <= val);
    if (op === "in") { const set = new Set(val.replace(/^\(|\)$/g, "").split(",").map((x) => x.replace(/^"|"$/g, ""))); out = out.filter((r) => set.has(String(r[k]))); }
  }
  const ord = sp.get("order");
  if (ord) { const [col, dir] = ord.split("."); out = [...out].sort((a, b) => (String(a[col]) < String(b[col]) ? -1 : String(a[col]) > String(b[col]) ? 1 : 0) * (dir === "desc" ? -1 : 1)); }
  const lim = sp.get("limit");
  if (lim) out = out.slice(0, +lim);
  return out;
}
const pick = (row, sel) => { if (!sel || sel === "*") return { ...row }; const o = {}; for (const c of sel.split(",")) o[c.trim()] = row[c.trim()]; return o; };
const DEFAULTS = {
  assess_sets: () => ({ id: uuid(), status: "live", reveal: "after_close", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }),
  assess_sessions: () => ({ id: uuid(), status: "open", started_at: new Date(Date.now() + db.assess_sessions.length).toISOString() }),
  assess_people: () => ({ id: uuid(), n_sessions: 0 }),
  assess_pages: () => ({ attempts: 1, flagged: false }),
  assess_calls: () => ({ created_at: new Date().toISOString() }),
};

globalThis.fetch = async (url, init = {}) => {
  const u = new URL(String(url));
  const method = (init.method || "GET").toUpperCase();
  const H = new Headers(init.headers || {});
  const json = (obj, status = 200, headers = {}) => new Response(method === "HEAD" ? null : JSON.stringify(obj), { status, headers: { "content-type": "application/json", ...headers } });
  if (u.host === "api.anthropic.com") {
    const body = JSON.parse(init.body);
    ai.push({ model: body.model, sys: body.system.slice(0, 24) });
    return json({ content: [{ type: "text", text: "```json\n" + JSON.stringify(aiReply(body)) + "\n```" }] });
  }
  if (u.pathname === "/auth/v1/user") {
    const tok = (H.get("authorization") || "").replace(/^Bearer /, "");
    return USERS[tok] ? json({ ...USERS[tok], aud: "authenticated", role: "authenticated" }) : json({ message: "bad jwt" }, 401);
  }
  if (u.pathname.startsWith("/storage/v1/object/sign/")) return json({ signedURL: "/object/sign/x?token=t" });
  if (u.pathname.startsWith("/storage/v1/object/")) { storage.push(u.pathname); return json({ Key: u.pathname }); }
  const m = u.pathname.match(/^\/rest\/v1\/(\w+)$/);
  if (!m) return json({ message: "no route " + u.pathname }, 404);
  const table = m[1];
  if (missing && table.startsWith("assess_")) return json({ code: "PGRST205", message: "Could not find the table" }, 404);
  if (!db[table]) return json({ code: "42P01", message: "no table" }, 404);
  const sp = u.searchParams;
  const sel = sp.get("select");
  const wantObj = (H.get("accept") || "").includes("pgrst.object");
  const prefer = H.get("prefer") || "";
  const reply = (rows) => {
    const extra = prefer.includes("count=exact") ? { "content-range": `0-${Math.max(0, rows.length - 1)}/${rows.length}` } : {};
    if (wantObj) { if (rows.length !== 1) return json({ code: "PGRST116", message: "JSON object requested, multiple (or no) rows returned" }, 406); return json(pick(rows[0], sel), 200, extra); }
    return json(rows.map((r) => pick(r, sel)), 200, extra);
  };
  if (method === "GET" || method === "HEAD") {
    const all = applyFilters(db[table], new URLSearchParams([...sp.entries()].filter(([k]) => k !== "limit" && k !== "order")));
    const rows = applyFilters(db[table], sp);
    if (method === "HEAD") return new Response(null, { status: 200, headers: { "content-range": `0-0/${all.length}` } });
    return reply(rows);
  }
  if (method === "POST") {
    const body = JSON.parse(init.body);
    const list = Array.isArray(body) ? body : [body];
    const conflict = sp.get("on_conflict");
    const out = [];
    for (const r of list) {
      const keys = conflict ? conflict.split(",") : PK[table];
      const ex = keys && prefer.includes("merge-duplicates") ? db[table].find((x) => keys.every((k) => String(x[k]) === String(r[k]))) : null;
      if (ex) { Object.assign(ex, r); out.push(ex); continue; }
      if (table === "assess_people" && db.assess_people.some((x) => x.person_key === r.person_key)) return json({ code: "23505", message: "duplicate" }, 409);
      const row = { ...(DEFAULTS[table]?.() || {}), ...r };
      db[table].push(row); out.push(row);
    }
    return prefer.includes("return=representation") ? reply(out) : new Response(null, { status: 201 });
  }
  if (method === "PATCH") {
    const patch = JSON.parse(init.body);
    const rows = applyFilters(db[table], sp);
    for (const r of rows) Object.assign(r, patch);
    return prefer.includes("return=representation") ? reply(rows) : new Response(null, { status: 204 });
  }
  return json({ message: "method" }, 405);
};

// ── 가짜 Claude ───────────────────────────────────────────────────────────────
const aiMode = { item: "normal" };
function aiReply(body) {
  const sys = body.system;
  if (sys.startsWith("너는 시험지 2쪽")) return { grade: "2", name: "홍 길동", nickname: "길동이", phrase: ["여름에 코끼리와 해마가", "짝꿍처럼", "(41 + 59) × 30 − 78 ÷ 6 = 2987", "y = −2x + 5"], confidence: { grade: 0.9, name: 0.8, nickname: 0.6 }, legibility: { score: 4 } };
  if (sys.startsWith("너는 학생 손글씨 수학 풀이")) {
    if (aiMode.item === "blank") return { s1: { lines: [], empty: true }, s2: { lines: [], empty: true }, s3: { lines: [], empty: true }, legibility: { score: 3 } };
    if (aiMode.item === "messy" && body.model === "claude-sonnet-4-6") return { s1: { lines: [{ t: "x⍰y⍰12" }] }, s2: { lines: [{ t: "⍰⍰ = 4" }] }, s3: { lines: [{ t: "7⍰" }] }, legibility: { score: 1 } };
    return { s1: { lines: [{ t: "x + y = 12" }, { t: "3000x + 2000y = 29000" }] }, s2: { lines: [{ t: "3x + 2y = 29", struck: false }, { t: "x = 6", struck: true }, { t: "x = 5, y = 7" }] }, s3: { lines: [{ t: "7명" }] }, outside: [], legibility: { score: 4, issues: ["7을 1처럼 씀"] } };
  }
  if (sys.startsWith("너는 한국 수학 학원의 서술형 채점자")) return { marks: [{ no: 1, got: 4, reason: "두 식" }, { no: 2, got: 9, reason: "풀이" }, { no: 3, got: 3, reason: "답" }], final_answer: "7명", final_ok: true, needs_review: false, feedback: ["식을 잘 세웠어요.", "검산도 해 봐요.", "세 번째 말은 잘려야 해요"], tags: ["없음", "이상한태그"] };
  return {};
}

// ── 호출 도우미 ───────────────────────────────────────────────────────────────
let ipSeq = 1;
async function call(body, { tok = null, ip = "10.0.0.1" } = {}) {
  const req = { method: "POST", headers: { "x-forwarded-for": ip, "user-agent": "test", ...(tok ? { authorization: `Bearer ${tok}` } : {}) }, body: { task: "assess", ...body } };
  let status = 200, out = null;
  const res = { status(s) { status = s; return this; }, json(o) { out = o; return this; } };
  await handler(req, res);
  return { status, body: out };
}
const CROP = "A".repeat(2000);

// ── 1. 마이그레이션 전 ────────────────────────────────────────────────────────
missing = true;
let r = await call({ op: "list", device: "d1" });
ok(r.status === 200 && r.body.ready === false && r.body.open.length === 0, "표가 없으면 목록은 빈 채로(ready:false)");
r = await call({ op: "get", code: "SAMPLE01" });
ok(r.status === 503, "표가 없으면 열람은 503(준비 전)");
missing = false;

// ── 2. 등록(관리자) ───────────────────────────────────────────────────────────
r = await call({ op: "admin_register", spec: SPEC });
ok(r.status === 401, "비로그인 등록 → 401");
r = await call({ op: "admin_register", spec: SPEC }, { tok: "tok-stu" });
ok(r.status === 403, "학생 등록 → 403");
r = await call({ op: "admin_register", spec: { ...SPEC, code: "SAMPLE99" } }, { tok: "tok-admin" });
ok(r.status === 400 && r.body.errors?.some((e) => e.includes("확인값")), "검사 실패 JSON → 400 + 오류 목록");
r = await call({ op: "admin_register", spec: JSON.stringify(SPEC) }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.set.code === "SAMPLE01" && !r.body.updated && db.assess_sets.length === 1, "관리자 등록 (문자열 JSON)");
r = await call({ op: "admin_register", spec: SPEC }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.updated && db.assess_sets.length === 1, "응시 전 다시 올리면 갱신");

// ── 3. 목록 · 열람 ────────────────────────────────────────────────────────────
r = await call({ op: "list", device: "d1" });
ok(r.body.open.some((s) => s.code === "SAMPLE01" && s.n_items === 3), "열린 평가 목록");
r = await call({ op: "get", code: "sample01" });
const pubText = JSON.stringify(r.body);
ok(r.status === 200 && r.body.set.state === "open" && r.body.set.items.length === 3 && r.body.me === null, "열람(소문자 코드도) — 공개용");
ok(!pubText.includes("29000원을 냈습니다") || !pubText.includes('"answer"'), "열람 응답에 정답 필드 없음");
ok(!pubText.includes("7명") && !pubText.includes('"solution"') && !pubText.includes("criterion"), "정답·풀이·기준 문장이 새지 않음");
r = await call({ op: "get", code: "NOPE1" });
ok(r.status === 404, "없는 평가 → 404");

// ── 4. 비로그인 시작 · 이어 하기 · 응시 한도 ──────────────────────────────────
r = await call({ op: "start", code: "SAMPLE01" });
ok(r.status === 400, "기기 토큰 없으면 시작 불가");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1" });
const S1 = r.body;
ok(r.status === 200 && S1.sid && S1.secret && !S1.resumed, "비로그인 시작 → sid + 비밀값");
ok(db.assess_sessions[0].secret_hash !== S1.secret && db.assess_sessions[0].device_hash && !JSON.stringify(db.assess_sessions[0]).includes("dev-1"), "비밀값·기기 토큰은 해시로만 저장");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1", sid: S1.sid, secret: S1.secret });
ok(r.body.sid === S1.sid && r.body.resumed, "같은 비밀값으로 이어 하기");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1", sid: S1.sid, secret: "wrong" });
ok(r.body.sid !== S1.sid, "비밀값이 틀리면 이어 하지 않고 새 응시");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1" });
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1" });
ok(r.status === 429, "한 기기에서 같은 평가 3번 넘게 시작 → 429");

// ── 5. 쪽: 안내 · 2쪽 · 문제 ──────────────────────────────────────────────────
const A = { sid: S1.sid, secret: S1.secret };
let n0 = ai.length;
r = await call({ op: "page", ...A, page_no: 1, quality: { sharp: 120, paper: 240, contrast: 160, margin: 0.4 } });
ok(r.status === 200 && r.body.kind === "guide" && ai.length === n0, "1쪽(안내) — AI 호출 없음");
r = await call({ op: "page", sid: S1.sid, secret: "nope", page_no: 2, crop: CROP });
ok(r.status === 403, "비밀값 틀리면 403");
r = await call({ op: "page", ...A, page_no: 2 });
ok(r.status === 400, "2쪽에 사진이 없으면 400");
r = await call({ op: "page", ...A, page_no: 2, crop: CROP });
ok(r.status === 200 && r.body.kind === "info" && r.body.suggestion.name === "홍길동" && r.body.suggestion.grade === "m2" && r.body.suggestion.nickname === "길동이", "2쪽 판독 → 이름·학년 제안(정리됨)");
ok(db.assess_sessions.find((s) => s.id === S1.sid).ocr_info?.phrase?.length === 4, "2쪽 판독 원본(필적 줄)이 응시 기록에");
n0 = ai.length;
r = await call({ op: "page", ...A, page_no: 3, crop: CROP, quality: { sharp: 111 } });
ok(r.status === 200 && r.body.status === "graded" && ai.length === n0 + 2, "문제 쪽: 판독 + 채점 (호출 2번)");
ok(r.body.grade.marks[1].got === 3 && r.body.grade.total === 10 && r.body.grade.feedback.length === 2 && r.body.grade.tags.join() === "없음", "채점 정리: 배점 상한·피드백 2개·태그 화이트리스트");
ok(r.body.read.s2.lines.some((l) => l.struck) && !("legibility" in (r.body.read.s1 || {})), "판독: 그은 줄 표시 유지");
aiMode.item = "blank"; n0 = ai.length;
r = await call({ op: "page", ...A, page_no: 4, crop: CROP });
ok(r.body.status === "graded" && r.body.grade.total === 0 && ai.length === n0 + 1, "빈 답안 → 채점 AI 없이 0점");
aiMode.item = "messy"; n0 = ai.length;
r = await call({ op: "page", ...A, page_no: 5, crop: CROP });
const models = ai.slice(n0).map((x) => x.model);
ok(r.body.status === "graded" && models[0] === "claude-sonnet-4-6" && models[1] !== "claude-sonnet-4-6" && models.length === 3, "알아보기 힘든 글씨 → 강한 모델로 한 번 더 읽고 채점");
aiMode.item = "normal";
r = await call({ op: "page", ...A, page_no: 9, crop: CROP });
ok(r.status === 400, "없는 쪽 → 400");
r = await call({ op: "page", ...A, page_no: 3, crop: "A".repeat(3_000_000) });
ok(r.status === 413, "너무 큰 사진 → 413");

// 다시 찍기 한도 (쪽당 4번)
for (let i = 0; i < 3; i++) r = await call({ op: "page", ...A, page_no: 3, crop: CROP });
ok(r.status === 200 && db.assess_pages.find((p) => p.session_id === S1.sid && p.page_no === 3).attempts === 4, "3쪽 4번째까지 받음");
r = await call({ op: "page", ...A, page_no: 3, crop: CROP });
ok(r.status === 429, "5번째 다시 찍기 → 429");

// ── 6. 2쪽 확인 · 제출 · 결과 ─────────────────────────────────────────────────
r = await call({ op: "finish", ...A });
ok(r.status === 400, "이름 확인 전 제출 불가(비로그인)");
r = await call({ op: "info", ...A, name: "!!", grade: "2" });
ok(r.status === 400, "이상한 이름 → 400");
r = await call({ op: "info", ...A, name: "홍길동", grade: "2", nickname: "길동이" });
ok(r.status === 200 && r.body.info.by === "ocr" && r.body.info.grade === "m2" && db.assess_people.some((p) => p.person_key === "n:홍길동|m2"), "판독대로 확인 → by:ocr, 명부 n:홍길동|m2");
r = await call({ op: "info", ...A, name: "홍길돈", grade: "2" });
ok(r.body.info.by === "user" && db.assess_people.length === 2, "학생이 고치면 by:user (다른 키 → 새 명부)");
r = await call({ op: "info", ...A, name: "홍길동", grade: "2", nickname: "길동이" });
r = await call({ op: "finish", ...A });
const res = r.body.result;
ok(r.status === 200 && res.status === "submitted" && res.total === 20 && res.max === 30 && res.graded === 3, "제출: 10 + 0 + 10 = 20/30");
ok(res.reveal === true && res.items[0].answer?.answer === "7명" && res.items[0].read.s3.lines[0].t === "7명", "reveal after_submit → 정답·모범 풀이 + 내 판독");
ok(db.assess_people.find((p) => p.person_key === "n:홍길동|m2").n_sessions === 1, "명부 제출 수 +1");
r = await call({ op: "finish", ...A });
ok(r.status === 200 && db.assess_people.find((p) => p.person_key === "n:홍길동|m2").n_sessions === 1, "두 번 제출해도 한 번만 센다");
r = await call({ op: "page", ...A, page_no: 3, crop: CROP });
ok(r.status === 409, "제출 뒤에는 쪽을 더 받지 않음");
r = await call({ op: "flag", ...A, page_no: 3, note: "7을 1로 읽음" });
ok(r.status === 200 && db.assess_pages.find((p) => p.session_id === S1.sid && p.page_no === 3).flagged, "잘못 읽었어요 표시");

// ── 7. 로그인해서 담기 ────────────────────────────────────────────────────────
r = await call({ op: "claim", ...A });
ok(r.status === 401, "로그인 없이 담기 → 401");
r = await call({ op: "claim", ...A }, { tok: "tok-stu" });
ok(r.status === 200 && db.assess_sessions.find((s) => s.id === S1.sid).user_id === USERS["tok-stu"].id && db.assess_people.find((p) => p.person_key === "n:홍길동|m2").user_id === USERS["tok-stu"].id, "담기 → 응시·명부에 계정 연결");
r = await call({ op: "list" }, { tok: "tok-stu" });
ok(r.body.mine.some((m) => m.sid === S1.sid && m.status === "submitted" && m.code === "SAMPLE01"), "로그인 목록에 내 응시");

// ── 8. 로그인 응시 ────────────────────────────────────────────────────────────
r = await call({ op: "start", code: "SAMPLE01", device: "dev-9" }, { tok: "tok-stu" });
const L = r.body;
ok(r.status === 200 && L.secret && db.assess_sessions.find((s) => s.id === L.sid).user_id === USERS["tok-stu"].id, "로그인 시작 → 계정 응시");
r = await call({ op: "start", code: "SAMPLE01" }, { tok: "tok-stu" });
ok(r.body.sid === L.sid && r.body.resumed, "로그인은 열린 응시를 자동으로 이어 감");
r = await call({ op: "page", sid: L.sid, page_no: 3, crop: CROP }, { tok: "tok-stu" });
ok(r.status === 200, "로그인 응시는 토큰만으로 쪽 보내기");
r = await call({ op: "page", sid: L.sid, page_no: 3, crop: CROP }, { tok: "tok-admin" });
ok(r.status === 403, "남의 응시(다른 계정) → 403");
r = await call({ op: "finish", sid: L.sid }, { tok: "tok-stu" });
ok(r.status === 200 && r.body.result.info.name === "김민준" && r.body.result.info.by === "profile", "로그인 제출: 2쪽 확인 없으면 프로필 이름");

// ── 9. 호출 한도(비로그인 IP) ─────────────────────────────────────────────────
db.app_settings.push({ key: "assess_limits", value: JSON.stringify({ anon_ip_day: 2 }) });
r = await call({ op: "start", code: "SAMPLE01", device: "dev-ip" }, { ip: "7.7.7.7" });
const B = { sid: r.body.sid, secret: r.body.secret };
let codes = [];
for (const pg of [2, 3, 4]) codes.push((await call({ op: "page", ...B, page_no: pg, crop: CROP }, { ip: "7.7.7.7" })).status);
ok(JSON.stringify(codes) === "[200,200,429]", "IP 하루 한도(2) 넘으면 429");
db.app_settings.length = 0;

// ── 10. 공개 시점 · 마감 ──────────────────────────────────────────────────────
r = await call({ op: "admin_update", code: "SAMPLE01", reveal: "after_close" }, { tok: "tok-admin" });
r = await call({ op: "result", ...A });
ok(r.status === 200 && r.body.result.reveal === false && r.body.result.items[0].answer === null, "after_close + 응시 중 → 정답 숨김");
r = await call({ op: "admin_update", code: "SAMPLE01", status: "closed" }, { tok: "tok-admin" });
r = await call({ op: "result", ...A });
ok(r.body.result.reveal === true && r.body.result.items[0].answer?.answer === "7명", "마감 뒤 → 정답 공개");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-new" });
ok(r.status === 403, "마감된 평가는 새로 시작 불가");
r = await call({ op: "get", code: "SAMPLE01" });
ok(r.status === 200 && r.body.set.state === "closed", "마감된 평가도 열람(결과 보기용)");
r = await call({ op: "list", device: "x" });
ok(!r.body.open.some((s) => s.code === "SAMPLE01"), "마감되면 열린 목록에서 빠짐");

// ── 11. 관리자 조회 ───────────────────────────────────────────────────────────
r = await call({ op: "admin_sets" }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.sets[0].sessions >= 4 && r.body.sets[0].submitted === 2 && r.body.sets[0].avg != null, "관리자 목록: 응시·제출·평균");
r = await call({ op: "admin_sessions", code: "SAMPLE01" }, { tok: "tok-admin" });
const row = r.body.sessions.find((s) => s.sid === S1.sid);
ok(r.status === 200 && row.info.name === "홍길동" && row.person.person_key === "n:홍길동|m2" && row.pages.some((p) => p.flagged), "관리자 응시 기록: 응시자·명부·이의");
r = await call({ op: "admin_session", sid: S1.sid }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.pages.length === 5 && r.body.session.ocr_info.name === "홍 길동" && r.body.result.total === 20, "관리자 상세: 쪽별 판독·2쪽 원본");
r = await call({ op: "admin_export", code: "SAMPLE01" }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.sessions.length >= 4 && r.body.sessions.every((s) => s.user_id === undefined), "내보내기 (계정 id 제외)");
r = await call({ op: "admin_sets" }, { tok: "tok-stu" });
ok(r.status === 403, "학생은 관리자 조회 불가");
r = await call({ op: "admin_register", spec: SPEC }, { tok: "tok-admin" });
ok(r.status === 409 && r.body.sessions >= 4, "응시 기록이 있으면 덮어쓰기 전에 409");
r = await call({ op: "admin_register", spec: SPEC, overwrite: true }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.updated, "overwrite:true 면 갱신");
r = await call({ op: "nope" });
ok(r.status === 400, "모르는 op → 400");
ok(storage.length === 0, "사진 저장 꺼짐(기본) → 버킷에 아무것도 안 올림");

// ── 12. 사진 저장 켜면 버킷에 ─────────────────────────────────────────────────
db.app_settings.push({ key: "assess_store_images", value: "on" });
await call({ op: "admin_update", code: "SAMPLE01", status: "live" }, { tok: "tok-admin" });
r = await call({ op: "start", code: "SAMPLE01", device: "dev-img" });
const C = { sid: r.body.sid, secret: r.body.secret };
r = await call({ op: "page", ...C, page_no: 3, crop: CROP, image: "QUJD" });
ok(r.status === 200 && storage.some((p) => p.includes(`/assess-pages/SAMPLE01/${C.sid}/p3.jpg`)) && db.assess_pages.find((p) => p.session_id === C.sid).image_path, "저장 켜면 펴진 쪽 사진을 비공개 버킷에");

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
