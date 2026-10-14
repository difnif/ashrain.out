// node tests/assessApi.test.mjs — 서술형 평가 서버(api/photo.js → api/_lib/assess.js)를 가짜 Supabase(PostgREST 흉내) + 가짜 Anthropic 으로 끝까지.
// 실제 키·네트워크 없음. 검사: 등록(관리자)·열람(공개 분리)·비로그인 시작/이어 하기·쪽 판독/채점·재시도 한도·호출 한도·2쪽 확인·제출·공개 시점·이의·로그인 담기·관리자 조회
//   + 리뷰 반영: 사진 id(shot) 중복·늦은 옛 사진 무시·채점 원자적 맡기·채점 호출도 셈·제출 전 점수 비공개·빈 제출로 정답 보기 막기·
//     열리기 전 문제 비공개·이어 하기 주인 확인·담기에 명부 안 붙임·관리자 1000행 넘게.
// DB 함수(assess_charge·assess_reserve_page)는 SQL 과 같은 규칙을 JS 로 흉내 낸다 — 진짜 SQL 은 scratch Postgres 로 따로 검사(supabase 폴더 SQL 그대로).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { checkOf } from "../src/lib/assess/sheet.js";
process.env.SUPABASE_URL = "http://sb.local";
process.env.SUPABASE_ANON_KEY = "anon";
process.env.SUPABASE_SERVICE_ROLE_KEY = "service";
process.env.ANTHROPIC_API_KEY = "sk-test";
const { default: handler } = await import("../api/photo.js");
const HERE = path.dirname(fileURLToPath(import.meta.url));
const SPEC = JSON.parse(fs.readFileSync(path.join(HERE, "fixtures/assess-SAMPLE01.json"), "utf8"));
const clone = (o) => JSON.parse(JSON.stringify(o));
const quiet = console.error;
console.error = () => {};                // 서버 로그(의도한 실패) 숨김

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };

// ── 가짜 DB ───────────────────────────────────────────────────────────────────
const USERS = { "tok-admin": { id: "a0000000-0000-4000-8000-00000000000a" }, "tok-stu": { id: "b0000000-0000-4000-8000-00000000000b" }, "tok-stu2": { id: "c0000000-0000-4000-8000-00000000000c" } };
const db = {
  profiles: [{ id: USERS["tok-admin"].id, role: "admin", username: "원장", name: "박선생" }, { id: USERS["tok-stu"].id, role: "student", username: "민준이", name: "김민준", grade: "중2" },
    { id: USERS["tok-stu2"].id, role: "student", username: "서연", name: "이서연" }],
  app_settings: [], assess_sets: [], assess_people: [], assess_sessions: [], assess_pages: [], assess_calls: [],
};
const PK = { assess_pages: ["session_id", "page_no"], app_settings: ["key"] };
const MAX_ROWS = 1000;                  // PostgREST(Supabase) 한 번에 최대 행
let missing = false;                    // true 면 assess_* 표가 없는 척(마이그레이션 전)
const storage = [];
const ai = [];                          // [{model, sys}]
let onAi = null;                        // AI 호출 중에 끼워 넣을 일(한 번)
const uuid = () => "xxxxxxxx-xxxx-4xxx-8xxx-xxxxxxxxxxxx".replace(/x/g, () => "0123456789abcdef"[Math.floor(Math.random() * 16)]);
const nowIso = () => new Date().toISOString();

function filterRows(rows, sp) {
  let out = rows;
  for (const [k, v] of sp.entries()) {
    if (["select", "order", "limit", "on_conflict", "columns", "offset"].includes(k)) continue;
    const m = v.match(/^(eq|in|gte|lte|neq|is)\.(.*)$/s);
    if (!m) continue;
    const [, op, val] = m;
    if (op === "eq") out = out.filter((r) => String(r[k]) === val);
    if (op === "neq") out = out.filter((r) => String(r[k]) !== val);
    if (op === "gte") out = out.filter((r) => r[k] != null && String(r[k]) >= val);
    if (op === "lte") out = out.filter((r) => r[k] != null && String(r[k]) <= val);
    if (op === "is") out = out.filter((r) => (val === "null" ? r[k] == null : String(!!r[k]) === val));
    if (op === "in") { const set = new Set(val.replace(/^\(|\)$/g, "").split(",").map((x) => x.replace(/^"|"$/g, ""))); out = out.filter((r) => set.has(String(r[k]))); }
  }
  return out;
}
/** 거르기 + 정렬 + offset/limit (한 번에 최대 MAX_ROWS) */
function applyFilters(rows, sp) {
  let out = filterRows(rows, sp);
  const ord = sp.get("order");
  if (ord) {
    const keys = ord.split(",").map((o) => { const [col, dir] = o.split("."); return [col, dir === "desc" ? -1 : 1]; });
    out = [...out].sort((a, b) => { for (const [c, d] of keys) { const x = String(a[c] ?? ""), y = String(b[c] ?? ""); if (x !== y) return (x < y ? -1 : 1) * d; } return 0; });
  }
  const off = +sp.get("offset") || 0;
  const lim = Math.min(+sp.get("limit") || MAX_ROWS, MAX_ROWS);
  return out.slice(off, off + lim);
}
const pick = (row, sel) => { if (!sel || sel === "*") return { ...row }; const o = {}; for (const c of sel.split(",")) o[c.trim()] = row[c.trim()]; return o; };
const DEFAULTS = {
  assess_sets: () => ({ id: uuid(), status: "live", reveal: "after_close", created_at: nowIso(), updated_at: nowIso() }),
  assess_sessions: () => ({ id: uuid(), status: "open", started_at: new Date(Date.now() + db.assess_sessions.length).toISOString() }),
  assess_people: () => ({ id: uuid(), n_sessions: 0 }),
  assess_pages: () => ({ attempts: 1, flagged: false, grade_tries: 0, status: "read", updated_at: nowIso() }),
  assess_calls: () => ({ created_at: nowIso() }),
};

// SQL 함수와 같은 규칙 (supabase/2026-10_assess.sql 5-1 · 5-2)
const RPC = {
  assess_charge({ p_keys, p_caps, p_since }) {
    for (let i = 0; i < p_keys.length; i++) {
      if (db.assess_calls.filter((r) => r.key === p_keys[i] && r.created_at >= p_since).length >= p_caps[i]) return p_keys[i];
    }
    for (const key of p_keys) db.assess_calls.push({ key, created_at: nowIso() });
    return null;
  },
  assess_reserve_page({ p_session, p_page, p_kind, p_item, p_shot, p_max }) {
    let r = db.assess_pages.find((x) => x.session_id === p_session && x.page_no === p_page);
    if (!r) { r = { session_id: p_session, page_no: p_page, kind: p_kind, item_no: p_item, attempts: 0, status: "reading", shot: null, grade_tries: 0, flagged: false, updated_at: nowIso() }; db.assess_pages.push(r); }
    if (p_shot != null && r.shot === p_shot) {
      if (["read", "grading", "graded", "ok"].includes(r.status)) return [{ o_state: "done", o_attempts: r.attempts }];
      if (r.status === "reading" && Date.parse(r.updated_at) > Date.now() - 70_000) return [{ o_state: "busy", o_attempts: r.attempts }];
      r.status = "reading"; r.updated_at = nowIso();
      return [{ o_state: "retry", o_attempts: r.attempts }];
    }
    if (r.attempts >= p_max) return [{ o_state: "over", o_attempts: r.attempts }];
    Object.assign(r, { attempts: r.attempts + 1, shot: p_shot, status: "reading", kind: p_kind, item_no: p_item, read: null, grade: null, grade_tries: 0,
      flagged: false, flag_note: null, model_read: null, model_grade: null, image_path: null, updated_at: nowIso() });
    return [{ o_state: "fresh", o_attempts: r.attempts }];
  },
};

globalThis.fetch = async (url, init = {}) => {
  const u = new URL(String(url));
  const method = (init.method || "GET").toUpperCase();
  const H = new Headers(init.headers || {});
  const json = (obj, status = 200, headers = {}) => new Response(method === "HEAD" ? null : JSON.stringify(obj), { status, headers: { "content-type": "application/json", ...headers } });
  if (u.host === "api.anthropic.com") {
    const body = JSON.parse(init.body);
    ai.push({ model: body.model, sys: body.system.slice(0, 24) });
    if (onAi) { const f = onAi; onAi = null; await f(body); }
    const rep = aiReply(body);
    return json({ content: [{ type: "text", text: typeof rep === "string" ? rep : "```json\n" + JSON.stringify(rep) + "\n```" }] });
  }
  if (u.pathname === "/auth/v1/user") {
    const tok = (H.get("authorization") || "").replace(/^Bearer /, "");
    return USERS[tok] ? json({ ...USERS[tok], aud: "authenticated", role: "authenticated" }) : json({ message: "bad jwt" }, 401);
  }
  if (u.pathname.startsWith("/storage/v1/object/sign/")) return json({ signedURL: "/object/sign/x?token=t" });
  if (u.pathname.startsWith("/storage/v1/object/")) { storage.push(u.pathname); return json({ Key: u.pathname }); }
  const rp = u.pathname.match(/^\/rest\/v1\/rpc\/(\w+)$/);
  if (rp) {
    if (missing) return json({ code: "PGRST202", message: "Could not find the function" }, 404);
    if (!RPC[rp[1]]) return json({ code: "PGRST202", message: "no fn" }, 404);
    return json(RPC[rp[1]](JSON.parse(init.body || "{}")));
  }
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
    // count=exact(HEAD) 는 행 제한과 상관없이 전체 수
    if (method === "HEAD") return new Response(null, { status: 200, headers: { "content-range": `0-0/${filterRows(db[table], sp).length}` } });
    return reply(applyFilters(db[table], sp));
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
    const rows = filterRows(db[table], sp);
    for (const r of rows) Object.assign(r, patch);
    return prefer.includes("return=representation") ? reply(rows) : new Response(null, { status: 204 });
  }
  return json({ message: "method" }, 405);
};
// ── 가짜 Claude ───────────────────────────────────────────────────────────────
const aiMode = { item: "normal", grade: "normal" };
function aiReply(body) {
  const sys = body.system;
  if (sys.startsWith("너는 시험지 2쪽")) return { grade: "2", name: "홍 길동", nickname: "길동이", phrase: ["여름에 코끼리와 해마가", "짝꿍처럼", "(41 + 59) × 30 − 78 ÷ 6 = 2987", "y = −2x + 5"], confidence: { grade: 0.9, name: 0.8, nickname: 0.6 }, legibility: { score: 4 } };
  if (sys.startsWith("너는 학생 손글씨 수학 풀이")) {
    if (aiMode.item === "blank") return { s1: { lines: [], empty: true }, s2: { lines: [], empty: true }, s3: { lines: [], empty: true }, legibility: { score: 3 } };
    if (aiMode.item === "messy" && body.model === "claude-sonnet-4-6") return { s1: { lines: [{ t: "x⍰y⍰12" }] }, s2: { lines: [{ t: "⍰⍰ = 4" }] }, s3: { lines: [{ t: "7⍰" }] }, legibility: { score: 1 } };
    return { s1: { lines: [{ t: "x + y = 12" }, { t: "3000x + 2000y = 29000" }] }, s2: { lines: [{ t: "3x + 2y = 29", struck: false }, { t: "x = 6", struck: true }, { t: "x = 5, y = 7" }] }, s3: { lines: [{ t: "7명" }] }, outside: [], legibility: { score: 4, issues: ["7을 1처럼 씀"] } };
  }
  if (sys.startsWith("너는 한국 수학 학원의 서술형 채점자")) {
    if (aiMode.grade === "bad") return "죄송해요, 채점할 수 없어요";
    return { marks: [{ no: 1, got: 4, reason: "정답 7명과 같은 두 식" }, { no: 2, got: 9, reason: "풀이" }, { no: 3, got: 3, reason: "답" }], final_answer: "7명", final_ok: true, needs_review: false, feedback: ["식을 잘 세웠어요.", "검산도 해 봐요.", "세 번째 말은 잘려야 해요"], tags: ["없음", "이상한태그"] };
  }
  return {};
}

// ── 호출 도우미 ───────────────────────────────────────────────────────────────
async function call(body, { tok = null, ip = "10.0.0.1" } = {}) {
  const req = { method: "POST", headers: { "x-forwarded-for": ip, "user-agent": "test", ...(tok ? { authorization: `Bearer ${tok}` } : {}) }, body: { task: "assess", ...body } };
  let status = 200, out = null;
  const res = { status(s) { status = s; return this; }, json(o) { out = o; return this; } };
  await handler(req, res);
  return { status, body: out };
}
const CROP = "A".repeat(2000);
const row = (sid, no) => db.assess_pages.find((p) => p.session_id === sid && p.page_no === no);
const callsOf = (key) => db.assess_calls.filter((c) => c.key === key).length;

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
const clashSpec = clone(SPEC); clashSpec.code = "CLASH033"; clashSpec.sheet.pagecode.check = checkOf("CLASH033");
r = await call({ op: "admin_register", spec: clashSpec }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.warnings.some((w) => w.includes("SAMPLE01") && w.includes("확인값")), "확인값이 같은 열린 평가가 있으면 경고");
await call({ op: "admin_update", code: "CLASH033", status: "closed" }, { tok: "tok-admin" });

// ── 3. 목록 · 열람 ────────────────────────────────────────────────────────────
r = await call({ op: "list", device: "d1" });
ok(r.body.open.some((s) => s.code === "SAMPLE01" && s.n_items === 3) && !r.body.open.some((s) => s.code === "CLASH033"), "열린 평가 목록 (마감은 빠짐)");
r = await call({ op: "get", code: "sample01" });
const pubText = JSON.stringify(r.body);
ok(r.status === 200 && r.body.set.state === "open" && r.body.set.items.length === 3 && r.body.set.n_items === 3 && r.body.set.max === 30 && r.body.me === null, "열람(소문자 코드도) — 공개용 + 문항 수·만점");
ok(!pubText.includes("7명") && !pubText.includes('"solution"') && !pubText.includes("criterion") && !pubText.includes('"answer"'), "정답·풀이·기준 문장이 새지 않음");
r = await call({ op: "get", code: "NOPE1" });
ok(r.status === 404, "없는 평가 → 404");
// 열리기 전: 문제를 주지 않는다
const soonSpec = clone(SPEC); soonSpec.code = "SOON01"; soonSpec.sheet.pagecode.check = checkOf("SOON01"); soonSpec.opens_at = "2099-01-01T00:00:00Z";
await call({ op: "admin_register", spec: soonSpec }, { tok: "tok-admin" });
r = await call({ op: "get", code: "SOON01" });
ok(r.status === 200 && r.body.set.state === "soon" && r.body.set.items.length === 0 && r.body.set.pages.length === 0 && r.body.set.n_items === 3 && !JSON.stringify(r.body).includes("story"), "열리기 전 평가 → 제목·문항 수만(문제 없음)");
r = await call({ op: "start", code: "SOON01", device: "dev-soon" });
ok(r.status === 403, "열리기 전에는 시작 불가");

// ── 4. 비로그인 시작 · 이어 하기 · 응시 한도 ──────────────────────────────────
r = await call({ op: "start", code: "SAMPLE01" });
ok(r.status === 400, "기기 토큰 없으면 시작 불가");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1" });
const S1 = r.body;
ok(r.status === 200 && S1.sid && S1.secret && !S1.resumed && S1.user_bound === false, "비로그인 시작 → sid + 비밀값 (계정 없음 표시)");
ok(db.assess_sessions[0].secret_hash !== S1.secret && db.assess_sessions[0].device_hash && !JSON.stringify(db.assess_sessions[0]).includes("dev-1"), "비밀값·기기 토큰은 해시로만 저장");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1", sid: S1.sid, secret: S1.secret });
ok(r.body.sid === S1.sid && r.body.resumed, "같은 비밀값으로 이어 하기");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1", sid: S1.sid, secret: "wrong" });
ok(r.body.sid !== S1.sid, "비밀값이 틀리면 이어 하지 않고 새 응시");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1", sid: S1.sid, secret: S1.secret }, { tok: "tok-stu2" });
ok(r.status === 200 && r.body.sid !== S1.sid && r.body.user_bound, "로그인한 다른 사람은 이 기기의 비로그인 응시를 이어 받지 않음(새 계정 응시)");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1" });
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1" });
ok(r.status === 429, "한 기기에서 같은 평가 3번 넘게 시작 → 429");

// ── 5. 쪽: 안내 · 2쪽 · 문제 ──────────────────────────────────────────────────
const A = { sid: S1.sid, secret: S1.secret };
let n0 = ai.length;
r = await call({ op: "page", ...A, page_no: 1, shot: "g-0000001", quality: { sharp: 120, paper: 240, contrast: 160, margin: 0.4 } });
ok(r.status === 200 && r.body.kind === "guide" && ai.length === n0, "1쪽(안내) — AI 호출 없음");
r = await call({ op: "page", sid: S1.sid, secret: "nope", page_no: 2, crop: CROP });
ok(r.status === 403, "비밀값 틀리면 403");
r = await call({ op: "page", ...A, page_no: 2 });
ok(r.status === 400, "2쪽에 사진이 없으면 400");
r = await call({ op: "page", ...A, page_no: 2, crop: CROP, shot: "info-0001" });
ok(r.status === 200 && r.body.kind === "info" && r.body.suggestion.name === "홍길동" && r.body.suggestion.grade === "m2" && r.body.suggestion.nickname === "길동이" && !("read" in r.body), "2쪽 판독 → 이름·학년 제안(정리됨, 원문은 안 보냄)");
ok(db.assess_sessions.find((s) => s.id === S1.sid).ocr_info?.phrase?.length === 4, "2쪽 판독 원본(필적 줄)이 응시 기록에");
n0 = ai.length; let c0 = callsOf("anon");
r = await call({ op: "page", ...A, page_no: 3, crop: CROP, shot: "shot-3-aaaa", quality: { sharp: 111 } });
ok(r.status === 200 && r.body.status === "graded" && ai.length === n0 + 2 && callsOf("anon") === c0 + 1, "문제 쪽: 판독 + 바로 채점 (AI 2번, 한도는 1단위)");
ok(!("grade" in r.body) && !JSON.stringify(r.body).includes("feedback"), "제출 전 쪽 응답에 점수·피드백 없음");
const g3 = row(S1.sid, 3).grade;
ok(g3.marks[1].got === 3 && g3.total === 10 && g3.feedback.length === 2 && g3.tags.join() === "없음", "채점 정리(DB): 배점 상한·피드백 2개·태그 화이트리스트");
ok(r.body.read.s2.lines.some((l) => l.struck) && !("legibility" in (r.body.read.s1 || {})), "판독: 그은 줄 표시 유지");
// 같은 사진을 다시 보냄(응답이 끊겨 브라우저가 다시 보낸 경우) → AI 다시 안 부르고 시도 수도 그대로
n0 = ai.length; c0 = callsOf("anon");
r = await call({ op: "page", ...A, page_no: 3, crop: CROP, shot: "shot-3-aaaa" });
ok(r.status === 200 && r.body.status === "graded" && ai.length === n0 && callsOf("anon") === c0 && row(S1.sid, 3).attempts === 1, "같은 사진 다시 보내기 → 저장된 결과(AI·한도·시도 수 그대로)");
// 같은 사진을 다른 요청이 읽는 중 → busy
row(S1.sid, 3).status = "reading"; row(S1.sid, 3).updated_at = nowIso();
r = await call({ op: "page", ...A, page_no: 3, crop: CROP, shot: "shot-3-aaaa" });
ok(r.status === 409 && r.body.busy, "같은 사진을 읽는 중이면 409 busy (두 번 읽지 않음)");
row(S1.sid, 3).updated_at = new Date(Date.now() - 80_000).toISOString();
n0 = ai.length;
r = await call({ op: "page", ...A, page_no: 3, crop: CROP, shot: "shot-3-aaaa" });
ok(r.status === 200 && r.body.status === "graded" && ai.length === n0 + 2 && row(S1.sid, 3).attempts === 1, "읽던 요청이 멈췄으면(70초) 같은 사진으로 다시 — 시도 수는 그대로");
aiMode.item = "blank"; n0 = ai.length;
r = await call({ op: "page", ...A, page_no: 4, crop: CROP, shot: "shot-4-aaaa" });
ok(r.body.status === "graded" && row(S1.sid, 4).grade.total === 0 && ai.length === n0 + 1 && row(S1.sid, 4).model_grade === "rule:blank", "빈 답안 → 채점 AI 없이 0점");
aiMode.item = "messy"; n0 = ai.length; c0 = callsOf("anon");
r = await call({ op: "page", ...A, page_no: 5, crop: CROP, shot: "shot-5-aaaa" });
const models = ai.slice(n0).map((x) => x.model);
ok(r.body.status === "graded" && models[0] === "claude-sonnet-4-6" && models[1] !== "claude-sonnet-4-6" && models.length === 3 && callsOf("anon") === c0 + 2, "알아보기 힘든 글씨 → 강한 모델로 한 번 더(한도 +1) 읽고 채점");
aiMode.item = "normal";
r = await call({ op: "page", ...A, page_no: 9, crop: CROP });
ok(r.status === 400, "없는 쪽 → 400");
r = await call({ op: "page", ...A, page_no: 3, crop: "A".repeat(3_000_000) });
ok(r.status === 413, "너무 큰 사진 → 413");

// 늦게 끝난 옛 사진은 새 사진을 덮지 않는다
onAi = async () => { await call({ op: "page", ...A, page_no: 3, crop: CROP, shot: "shot-3-newer" }); };
r = await call({ op: "page", ...A, page_no: 3, crop: CROP, shot: "shot-3-older" });
ok(r.status === 409 && r.body.superseded && row(S1.sid, 3).shot === "shot-3-newer" && row(S1.sid, 3).status === "graded", "읽는 동안 다시 찍으면 옛 사진 결과는 버림(새 사진이 남음)");
ok(row(S1.sid, 3).attempts === 3, "시도 수: 첫 사진·옛 사진·새 사진 = 3");
r = await call({ op: "page", ...A, page_no: 3, crop: CROP, shot: "shot-3-four" });
ok(r.status === 200 && row(S1.sid, 3).attempts === 4, "3쪽 4번째 사진까지 받음");
r = await call({ op: "page", ...A, page_no: 3, crop: CROP, shot: "shot-3-five" });
ok(r.status === 429 && row(S1.sid, 3).shot === "shot-3-four", "5번째 다른 사진 → 429 (마지막 사진 그대로)");

// ── 6. 결과: 제출 전엔 점수 없음 · 2쪽 확인 · 제출 · 공개 ─────────────────────
r = await call({ op: "result", ...A });
ok(r.status === 200 && r.body.result.total === null && r.body.result.items.every((i) => i.got === null && !i.feedback.length && i.elements.every((e) => e.got === null && !e.reason)) && r.body.result.items[0].read, "제출 전 결과: 점수·근거·피드백 없이 읽힌 글씨만");
r = await call({ op: "finish", ...A });
ok(r.status === 400, "이름 확인 전 제출 불가(비로그인)");
r = await call({ op: "info", ...A, name: "!!", grade: "2" });
ok(r.status === 400, "이상한 이름 → 400");
r = await call({ op: "info", ...A, name: "홍길동", grade: "x7" });
ok(r.status === 400, "학년이 범위 밖 → 400 (느슨한 값 안 받음)");
r = await call({ op: "info", ...A, name: "홍길동", grade: "2", nickname: "길동이" });
ok(r.status === 200 && r.body.info.by === "ocr" && r.body.info.grade === "m2" && db.assess_people.some((p) => p.person_key === "n:홍길동|m2"), "판독대로 확인 → by:ocr, 명부 n:홍길동|m2");
r = await call({ op: "info", ...A, name: "홍길돈", grade: "2" });
ok(r.body.info.by === "user" && db.assess_people.length === 2, "학생이 고치면 by:user (다른 키 → 새 명부)");
r = await call({ op: "info", ...A, name: "홍길동", grade: "2", nickname: "길동이" });
// 채점 중인 쪽이 있으면 기다리게
row(S1.sid, 5).status = "grading"; row(S1.sid, 5).updated_at = nowIso();
r = await call({ op: "finish", ...A });
ok(r.status === 409 && r.body.busy && r.body.pages.includes(5), "채점 중인 쪽이 있으면 제출 409(잠시 뒤)");
row(S1.sid, 5).status = "graded";
r = await call({ op: "claim", ...A }, { tok: "tok-stu" });
ok(r.status === 409, "제출 전에는 계정에 담기 불가");
r = await call({ op: "finish", ...A });
const res = r.body.result;
ok(r.status === 200 && res.status === "submitted" && res.total === 20 && res.max === 30 && res.graded === 3 && res.complete, "제출: 10 + 0 + 10 = 20/30");
ok(res.reveal === true && res.items[0].answer?.answer === "7명" && res.items[0].elements[0].reason.includes("7명") && res.items[0].read.s3.lines[0].t === "7명", "after_submit + 다 채점 → 정답·모범 풀이·근거 공개");
ok(db.assess_people.find((p) => p.person_key === "n:홍길동|m2").n_sessions === 1, "명부 제출 수 = 1");
r = await call({ op: "finish", ...A });
ok(r.status === 200 && db.assess_people.find((p) => p.person_key === "n:홍길동|m2").n_sessions === 1, "두 번 제출해도 한 번만 센다");
r = await call({ op: "page", ...A, page_no: 3, crop: CROP });
ok(r.status === 409, "제출 뒤에는 쪽을 더 받지 않음");
r = await call({ op: "info", ...A, name: "김철수", grade: "2" });
ok(r.status === 409, "제출 뒤에는 이름을 바꾸지 못함");
r = await call({ op: "flag", ...A, page_no: 3, note: "7을 1로 읽음" });
ok(r.status === 200 && row(S1.sid, 3).flagged, "잘못 읽었어요 표시");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-1", sid: S1.sid, secret: S1.secret });
ok(r.status === 200 && r.body.sid === S1.sid && r.body.status === "submitted", "제출한 응시로 다시 시작하면 새로 만들지 않고 '제출됨'을 알려 줌(결과 응답을 놓쳤을 때)");

// ── 7. 로그인해서 담기 (명부는 계정에 붙이지 않음) ────────────────────────────
r = await call({ op: "claim", ...A });
ok(r.status === 401, "로그인 없이 담기 → 401");
r = await call({ op: "claim", ...A }, { tok: "tok-stu" });
ok(r.status === 200 && db.assess_sessions.find((s) => s.id === S1.sid).user_id === USERS["tok-stu"].id, "담기 → 응시에 계정 연결");
ok(!db.assess_people.find((p) => p.person_key === "n:홍길동|m2").user_id, "명부(이름|학년)는 계정에 붙이지 않음 — 동명이인 가능");
r = await call({ op: "claim", ...A }, { tok: "tok-stu" });
ok(r.status === 200, "같은 계정이 두 번 담기 → 괜찮음");
r = await call({ op: "claim", ...A }, { tok: "tok-stu2" });
ok(r.status === 409, "다른 계정이 담기 → 409");
r = await call({ op: "list" }, { tok: "tok-stu" });
ok(r.body.mine.some((m) => m.sid === S1.sid && m.status === "submitted" && m.code === "SAMPLE01"), "로그인 목록에 내 응시");

// ── 8. 로그인 응시 ────────────────────────────────────────────────────────────
r = await call({ op: "start", code: "SAMPLE01", device: "dev-9" }, { tok: "tok-stu" });
const L = r.body;
ok(r.status === 200 && L.secret && L.user_bound && db.assess_sessions.find((s) => s.id === L.sid).user_id === USERS["tok-stu"].id, "로그인 시작 → 계정 응시");
r = await call({ op: "start", code: "SAMPLE01" }, { tok: "tok-stu" });
ok(r.body.sid === L.sid && r.body.resumed, "로그인은 열린 응시를 자동으로 이어 감");
r = await call({ op: "start", code: "SAMPLE01", sid: L.sid, secret: r.body.secret });
ok(r.body.sid !== L.sid, "로그아웃 상태로는 계정 응시를 비밀값으로 이어 받지 않음");
r = await call({ op: "get", code: "SAMPLE01" }, { tok: "tok-stu" });
ok(r.body.mine?.sid === L.sid && r.body.mine.status === "open", "열람에 내 마지막 응시(로그인)");
r = await call({ op: "page", sid: L.sid, page_no: 3, crop: CROP, shot: "L-shot-3" }, { tok: "tok-stu" });
ok(r.status === 200 && callsOf(`u:${USERS["tok-stu"].id}`) === 1, "로그인 응시는 토큰만으로 쪽 보내기 (계정 한도로 셈)");
r = await call({ op: "page", sid: L.sid, page_no: 3, crop: CROP }, { tok: "tok-admin" });
ok(r.status === 403, "남의 응시(다른 계정) → 403");

// 채점 실패 → 다시 채점(셈) → 3번 넘으면 멈춤
aiMode.grade = "bad"; c0 = callsOf(`u:${USERS["tok-stu"].id}`);
r = await call({ op: "page", sid: L.sid, page_no: 4, crop: CROP, shot: "L-shot-4" }, { tok: "tok-stu" });
ok(r.status === 200 && r.body.status === "read" && row(L.sid, 4).grade_tries === 1 && row(L.sid, 4).status === "read", "바로 채점이 실패해도 판독은 남음(read)");
r = await call({ op: "grade", sid: L.sid, page_no: 4 }, { tok: "tok-stu" });
ok(r.status === 500 && row(L.sid, 4).status === "read" && row(L.sid, 4).grade_tries === 2, "채점만 다시 → 실패하면 read 로 되돌림");
r = await call({ op: "grade", sid: L.sid, page_no: 4 }, { tok: "tok-stu" });
r = await call({ op: "grade", sid: L.sid, page_no: 4 }, { tok: "tok-stu" });
ok(r.status === 429 && row(L.sid, 4).grade_tries === 3, "채점 맡기 3번 넘으면 429 (끝없이 부르지 않음)");
ok(callsOf(`u:${USERS["tok-stu"].id}`) === c0 + 3, "채점만 다시도 한도로 셈 (쪽 1 + 채점 2)");
aiMode.grade = "normal";
// 동시에 채점 → 하나만 맡는다
r = await call({ op: "page", sid: L.sid, page_no: 5, crop: CROP, shot: "L-shot-5" }, { tok: "tok-stu" });
row(L.sid, 5).status = "read"; row(L.sid, 5).grade = null; row(L.sid, 5).grade_tries = 1;
n0 = ai.length;
const both = await Promise.all([call({ op: "grade", sid: L.sid, page_no: 5 }, { tok: "tok-stu" }), call({ op: "grade", sid: L.sid, page_no: 5 }, { tok: "tok-stu" })]);
ok(both.filter((x) => x.status === 200).length === 1 && both.some((x) => x.status === 409 && x.body.busy) && ai.length === n0 + 1, "동시에 두 번 채점 요청 → 한 번만 채점(나머지 busy)");
r = await call({ op: "grade", sid: L.sid, page_no: 5 }, { tok: "tok-stu" });
ok(r.status === 200 && r.body.status === "graded" && !("grade" in r.body), "채점 끝난 쪽 다시 → graded (점수는 안 보냄)");
r = await call({ op: "finish", sid: L.sid }, { tok: "tok-stu" });
ok(r.status === 200 && r.body.result.info.name === "김민준" && r.body.result.info.by === "profile", "로그인 제출: 2쪽 확인 없으면 프로필 이름");
ok(r.body.result.reveal === false && r.body.result.complete === false && r.body.result.items.every((i) => i.answer === null && i.elements.every((e) => !e.reason)) && r.body.result.total === 20, "after_submit 이라도 채점 안 된 문제가 있으면 마감 전엔 정답·근거 비공개(점수는 보임)");

// ── 9. 호출 한도(비로그인 IP) · 응시 시작 한도 ────────────────────────────────
db.app_settings.push({ key: "assess_limits", value: JSON.stringify({ anon_ip_day: 2, anon_ip_sessions_day: 2 }) });
r = await call({ op: "start", code: "SAMPLE01", device: "dev-ip" }, { ip: "7.7.7.7" });
const B = { sid: r.body.sid, secret: r.body.secret };
let codes = [];
for (const pg of [2, 3, 4]) codes.push((await call({ op: "page", ...B, page_no: pg, crop: CROP }, { ip: "7.7.7.7" })).status);
ok(JSON.stringify(codes) === "[200,200,429]", "IP 하루 한도(2) 넘으면 429");
ok(row(B.sid, 4).status === "error", "한도에 걸린 쪽은 error 로 남음(같은 사진으로 내일 다시)");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-ip2" }, { ip: "7.7.7.7" });
ok(r.status === 200, "같은 IP 두 번째 응시 시작");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-ip3" }, { ip: "7.7.7.7" });
ok(r.status === 429, "같은 IP 하루 응시 시작 한도(2) 넘으면 429 — 기기 토큰을 바꿔도");
db.app_settings.length = 0;

// ── 10. 공개 시점 · 마감 ──────────────────────────────────────────────────────
r = await call({ op: "admin_update", code: "SAMPLE01", reveal: "after_close" }, { tok: "tok-admin" });
r = await call({ op: "result", ...A });
ok(r.status === 200 && r.body.result.reveal === false && r.body.result.items[0].answer === null && !r.body.result.items[0].elements[0].reason && r.body.result.total === 20, "after_close + 응시 중 → 정답·근거 숨김 (점수는 보임)");
r = await call({ op: "admin_update", code: "SAMPLE01", status: "closed" }, { tok: "tok-admin" });
r = await call({ op: "result", ...A });
ok(r.body.result.reveal === true && r.body.result.items[0].answer?.answer === "7명", "마감 뒤 → 정답 공개");
r = await call({ op: "result", sid: L.sid }, { tok: "tok-stu" });
ok(r.body.result.reveal === true, "마감 뒤에는 빠진 쪽이 있던 제출도 공개");
r = await call({ op: "start", code: "SAMPLE01", device: "dev-new" });
ok(r.status === 403, "마감된 평가는 새로 시작 불가");
r = await call({ op: "get", code: "SAMPLE01" });
ok(r.status === 200 && r.body.set.state === "closed" && r.body.set.items.length === 3, "마감된 평가도 열람(결과 보기용)");
r = await call({ op: "list", device: "x" });
ok(!r.body.open.some((s) => s.code === "SAMPLE01"), "마감되면 열린 목록에서 빠짐");

// ── 11. 관리자 조회 ───────────────────────────────────────────────────────────
r = await call({ op: "admin_sets" }, { tok: "tok-admin" });
const sRow = r.body.sets.find((x) => x.code === "SAMPLE01");
ok(r.status === 200 && sRow.sessions >= 5 && sRow.submitted === 2 && sRow.avg === 20, "관리자 목록: 응시·제출·평균");
r = await call({ op: "admin_sessions", code: "SAMPLE01" }, { tok: "tok-admin" });
const srow = r.body.sessions.find((s) => s.sid === S1.sid);
ok(r.status === 200 && srow.info.name === "홍길동" && srow.person.person_key === "n:홍길동|m2" && srow.pages.some((p) => p.flagged), "관리자 응시 기록: 응시자·명부·이의");
r = await call({ op: "admin_session", sid: S1.sid }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.pages.length === 5 && r.body.session.ocr_info.name === "홍 길동" && r.body.result.total === 20 && r.body.result.items[0].elements[0].reason, "관리자 상세: 쪽별 판독·2쪽 원본·근거");
r = await call({ op: "admin_export", code: "SAMPLE01" }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.sessions.length >= 5 && r.body.sessions.every((s) => s.user_id === undefined), "내보내기 (계정 id 제외)");
r = await call({ op: "admin_sets" }, { tok: "tok-stu" });
ok(r.status === 403, "학생은 관리자 조회 불가");
r = await call({ op: "admin_register", spec: SPEC }, { tok: "tok-admin" });
ok(r.status === 409 && r.body.sessions >= 5, "응시 기록이 있으면 덮어쓰기 전에 409");
r = await call({ op: "admin_register", spec: SPEC, overwrite: true }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.updated, "overwrite:true 면 갱신");
r = await call({ op: "nope" });
ok(r.status === 400, "모르는 op → 400");
ok(storage.length === 0, "사진 저장 꺼짐(기본) → 버킷에 아무것도 안 올림");

// 1000행 넘는 응시(한 번에 1000행 제한) — 쪼개 받아 전부
const big = clone(SPEC); big.code = "BIG01"; big.sheet.pagecode.check = checkOf("BIG01");
await call({ op: "admin_register", spec: big }, { tok: "tok-admin" });
const bigSet = db.assess_sets.find((x) => x.code === "BIG01");
for (let i = 0; i < 1150; i++) {
  const id = uuid();
  db.assess_sessions.push({ id, set_id: bigSet.id, status: i % 2 ? "submitted" : "open", total: 10, max: 30, started_at: new Date(Date.now() - i * 1000).toISOString() });
  db.assess_pages.push({ session_id: id, page_no: 3, kind: "item", item_no: 1, status: "graded", attempts: 1, flagged: false });
  db.assess_pages.push({ session_id: id, page_no: 4, kind: "item", item_no: 2, status: "read", attempts: 1, flagged: false });
}
r = await call({ op: "admin_sessions", code: "BIG01" }, { tok: "tok-admin" });
ok(r.status === 200 && r.body.sessions.length === 1150 && r.body.sessions.every((s) => s.pages.length === 2), "관리자 응시 기록 1150건 전부(쪽 2300행도)");
r = await call({ op: "admin_sets" }, { tok: "tok-admin" });
ok(r.body.sets.find((x) => x.code === "BIG01").sessions === 1150 && r.body.sets.find((x) => x.code === "BIG01").submitted === 575, "관리자 목록 통계도 1000건 넘게");
r = await call({ op: "admin_export", code: "BIG01" }, { tok: "tok-admin" });
ok(r.body.sessions.length === 1150, "내보내기도 1150건");

// ── 12. 사진 저장 켜면 버킷에 ─────────────────────────────────────────────────
db.app_settings.push({ key: "assess_store_images", value: "on" });
await call({ op: "admin_update", code: "SAMPLE01", status: "live" }, { tok: "tok-admin" });
r = await call({ op: "start", code: "SAMPLE01", device: "dev-img" });
const C = { sid: r.body.sid, secret: r.body.secret };
r = await call({ op: "page", ...C, page_no: 3, crop: CROP, image: "QUJD", shot: "img-shot-001" });
ok(r.status === 200 && storage.some((p) => p.includes(`/assess-pages/SAMPLE01/${C.sid}/p3-img-shot-00`)) && row(C.sid, 3).image_path, "저장 켜면 펴진 쪽 사진을 비공개 버킷에 (사진마다 다른 이름)");

// ── 13. AI 오류는 학생 화면에 내부 사유를 보이지 않는다 ───────────────────────
const realFetch = globalThis.fetch;
globalThis.fetch = async (url, init) => (String(url).includes("api.anthropic.com")
  ? new Response(JSON.stringify({ error: { type: "invalid_request_error", message: "Your credit balance is too low (org-123)" } }), { status: 400, headers: { "content-type": "application/json" } })
  : realFetch(url, init));
r = await call({ op: "page", ...C, page_no: 4, crop: CROP, shot: "err-shot-001" });
ok(r.status === 500 && /^AI 호출 실패/.test(r.body.error) && !r.body.error.includes("credit") && row(C.sid, 4).status === "error", "AI 오류 → 일반 문구(크레딧·조직 정보 숨김), 쪽은 error");
globalThis.fetch = realFetch;
r = await call({ op: "page", ...C, page_no: 4, crop: CROP, shot: "err-shot-001" });
ok(r.status === 200 && r.body.status === "graded" && row(C.sid, 4).attempts === 1, "같은 사진으로 다시 보내면 이어서 (시도 수 그대로)");

console.error = quiet;
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
