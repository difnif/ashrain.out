// 서술형 평가 화면 스모크 — dist/ 를 띄우고 /api/photo(task:"assess")와 Supabase 를 모의 응답으로 바꿔 흐름을 끝까지 눌러 본다.
//   node tests/smoke/assess.smoke.mjs [--headed] [--light]
// 준비: `npx vite build` (dist/ 필요) · playwright + Chromium.
// 시험 사진: 브라우저로 시험지 한 쪽(마커·방향 막대·쪽 번호 띠·칸·글줄·손글씨 흉내)을 기울여 그린 뒤 찍는다 — 앱의 실제 촬영 처리(마커 → 펴기 → 띠 → 품질)를 그대로 통과시킨다.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { publicView, answerKey } from "../../src/lib/assess/spec.js";
import { encodePage, codeCells, markerRects, ORIENT } from "../../src/lib/assess/sheet.js";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); }
catch { ({ chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright")); }

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "../..");
const DIST = path.join(ROOT, "dist");
const HEADED = process.argv.includes("--headed");
const THEME = process.argv.includes("--light") ? "light" : "dark";
const SHOTS = process.env.SMOKE_SHOTS || path.join(HERE, "shots");
const SPEC = JSON.parse(fs.readFileSync(path.join(ROOT, "tests/fixtures/assess-SAMPLE01.json"), "utf8"));
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "assess-smoke-"));

// ── 모의 서버 상태 ────────────────────────────────────────────────────────────
const calls = [];                 // [{op, page_no, hasCrop, hasImage}]
const st = { sets: [], sessions: {}, adminCalls: [] };
const PUB = { ...publicView(SPEC), status: "live", opens_at: null, closes_at: null, reveal: "after_submit", state: "open" };
function itemRead(no) {
  return { s1: { lines: [{ t: no === 1 ? "x + y = 12" : "y = 200 − 8x", struck: false }], empty: false }, s2: { lines: [{ t: "x = 6", struck: true }, { t: "x = 5, y = 7", struck: false }], empty: false }, s3: { lines: [{ t: "7명", struck: false }], empty: false }, outside: [], legibility: { score: 4, issues: [] }, unreadable: 0 };
}
const itemGrade = (no) => ({ marks: [{ no: 1, got: 4, reason: "두 식을 세움" }, { no: 2, got: no === 2 ? 1 : 3, reason: "계산" }, { no: 3, got: 3, reason: "답" }], total: no === 2 ? 8 : 10, max: 10, final_answer: "7명", final_ok: true, needs_review: false, feedback: ["식을 잘 세웠어요."], tags: ["없음"] });
function mockAssess(body, authed) {
  const { op } = body;
  calls.push({ op, page_no: body.page_no, hasCrop: typeof body.crop === "string" && body.crop.length > 1000, hasImage: !!body.image, authed });
  if (op === "list") return { open: [{ code: "SAMPLE01", title: SPEC.title, level: "mid", grade_label: "중2", date: SPEC.date, n_items: 3, closes_at: null }], mine: [], ready: true };
  if (op === "get") return { set: PUB, store_images: false, anon: true, me: authed ? { name: "김민준", nick: "민준이" } : null };
  if (op === "start") { const sid = "5e55e55e-0000-4000-8000-00000000000" + (Object.keys(st.sessions).length + 1); st.sessions[sid] = { pages: {}, info: null }; return { sid, secret: "sec-" + sid.slice(-1), resumed: false, status: "open", pages: [] }; }
  const s = st.sessions[body.sid];
  if (!s) return { __status: 404, error: "응시 기록을 찾을 수 없어요" };
  if (op === "page") {
    const pg = SPEC.pages.find((p) => p.no === body.page_no);
    s.pages[pg.no] = true;
    if (pg.kind === "guide") return { kind: "guide", page_no: pg.no, status: "ok" };
    if (pg.kind === "info") return { kind: "info", page_no: pg.no, status: "read", read: { grade: "2", name: "홍길동", nickname: null, phrase: [] }, suggestion: { name: "홍길동", grade: "m2", nickname: null } };
    if (pg.item === 3) return { kind: "item", page_no: pg.no, item: 3, status: "read", read: itemRead(3), grade: null };      // 채점은 grade 로 따로
    return { kind: "item", page_no: pg.no, item: pg.item, status: "graded", read: itemRead(pg.item), grade: itemGrade(pg.item) };
  }
  if (op === "grade") return { page_no: body.page_no, status: "graded", grade: itemGrade(3) };
  if (op === "info") { s.info = { name: body.name, grade: "m" + body.grade, nickname: body.nickname || null, by: "ocr" }; return { info: s.info, person_id: "p1" }; }
  if (op === "finish" || op === "result") {
    const key = answerKey(SPEC);
    const items = SPEC.items.map((it, i) => ({ no: it.no, page: it.page, topic: it.topic, got: itemGrade(it.no).total, max: 10, graded: true,
      elements: it.rubric.map((r) => ({ no: r.no, element: r.element, points: r.points, got: itemGrade(it.no).marks[r.no - 1].got, reason: itemGrade(it.no).marks[r.no - 1].reason })),
      read: itemRead(it.no), feedback: ["식을 잘 세웠어요."], final_answer: "7명", final_ok: true, needs_review: false, flagged: false, captured: true, answer: key[i] }));
    return { result: { sid: body.sid, code: "SAMPLE01", title: SPEC.title, status: "submitted", total: 28, max: 30, graded: 3, n_items: 3, info: s.info, submitted_at: new Date().toISOString(), reveal: true, reveal_policy: "after_submit", items } };
  }
  if (op === "flag") return { page_no: body.page_no, flagged: true };
  if (op === "claim") return { claimed: true };
  return { __status: 400, error: "unknown " + op };
}
function mockAdmin(body) {
  st.adminCalls.push(body.op);
  if (body.op === "admin_sets") return { ready: true, sets: st.sets };
  if (body.op === "admin_register") {
    const spec = typeof body.spec === "string" ? JSON.parse(body.spec) : body.spec;
    st.sets = [{ id: "x", code: spec.code, title: spec.title, level: spec.level, grade_label: spec.grade_label, test_date: spec.date, status: "live", reveal: spec.reveal, n_items: spec.items.length, n_pages: spec.pages.length, state: "open", sessions: 0, submitted: 0, avg: null, max: null }];
    return { set: { id: "x", code: spec.code, status: "live" }, summary: {}, warnings: [], updated: false };
  }
  if (body.op === "admin_sessions") return { set: { code: body.code }, sessions: [] };
  return { ok: true };
}

// ── 정적 서버 (dist + SPA + /api/photo) ──────────────────────────────────────
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".webp": "image/webp" };
function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, "http://x");
      if (u.pathname === "/api/photo") {
        let raw = ""; req.on("data", (c) => (raw += c)); req.on("end", () => {
          let body = {}; try { body = JSON.parse(raw); } catch { /* */ }
          const authed = /^Bearer /.test(req.headers.authorization || "");
          const out = body.op?.startsWith("admin_") ? mockAdmin(body) : mockAssess(body, authed);
          const status = out.__status || 200; delete out.__status;
          setTimeout(() => { res.writeHead(status, { "content-type": "application/json" }); res.end(JSON.stringify(out)); }, body.op === "page" ? 250 : 60);
        });
        return;
      }
      let f = path.join(DIST, decodeURIComponent(u.pathname));
      if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f = path.join(DIST, "index.html");
      res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(0, "127.0.0.1", () => resolve({ srv, port: srv.address().port }));
  });
}

// ── Supabase 모의 ─────────────────────────────────────────────────────────────
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const USER = { id: "00000000-0000-4000-8000-000000000001", aud: "authenticated", role: "authenticated", email: "smoke@example.com", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: {}, factors: [], created_at: "2026-01-01T00:00:00Z" };
const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], app_metadata: USER.app_metadata, user_metadata: {}, session_id: "s1" })}.sig`;
const SESSION = { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r1", user: USER };
const PROFILE = { role: "student", member_code: "SMOKE", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "2011-03-01", username: "민준이", name: "김민준", honor_path: false };
async function mockSupabase(page, { session = false, role = "student" } = {}) {
  await page.route("https://placeholder.supabase.co/**", (route) => {
    const req = route.request(); const u = new URL(req.url()); const accept = req.headers()["accept"] || "";
    const json = (obj, headers = {}) => route.fulfill({ status: 200, contentType: "application/json", headers, body: JSON.stringify(obj) });
    if (u.pathname.startsWith("/auth/v1/user")) return session ? json(USER) : route.fulfill({ status: 401, contentType: "application/json", body: "{}" });
    if (u.pathname.startsWith("/auth/v1/token")) return json(SESSION);
    if (u.pathname.startsWith("/auth/v1/factors")) return json([]);
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/storage/v1/")) return json([]);
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0];
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0" }, body: "" });
      const wantObj = accept.includes("pgrst.object");
      if (table === "profiles") { const p = { id: USER.id, ...PROFILE, role }; return json(wantObj ? p : [p]); }
      if (req.method() === "POST") return json(wantObj ? {} : []);
      return json(wantObj ? null : [], { "content-range": "0-0/0" });
    }
    return json({});
  });
  await page.addInitScript(([key, sess, theme, withSession]) => {
    if (withSession) localStorage.setItem(key, JSON.stringify(sess)); else localStorage.removeItem(key);
    localStorage.setItem("ashrain-theme", theme);
  }, ["sb-placeholder-auth-token", SESSION, THEME, session]);
}

// ── 시험 사진: 시험지 한 쪽을 기울여 그려 PNG 로 ─────────────────────────────
function sheetHtml(pageNo, check, { blur = 0, tilt = true } = {}) {
  const pg = SPEC.pages.find((p) => p.no === pageNo) || { no: pageNo, kind: "item", regions: SPEC.pages[2].regions };
  const PX = 900 / 210;                      // 종이 1mm = PX px
  const U = 0.19 * PX;                       // 1단위
  const off = 10 * PX;                       // 카드 원점(10mm)
  const box = (x, y, w, h, style) => `<div style="position:absolute;left:${(off + x * U).toFixed(2)}px;top:${(off + y * U).toFixed(2)}px;width:${(w * U).toFixed(2)}px;height:${(h * U).toFixed(2)}px;${style}"></div>`;
  let inner = "";
  for (const m of markerRects()) inner += box(m.x, m.y, m.size, m.size, "background:#000");
  inner += box(ORIENT.x, ORIENT.y, ORIENT.w, ORIENT.h, "background:#000");
  const bits = encodePage(pageNo, check);
  codeCells().forEach((c, i) => { inner += box(c.x, c.y, c.w, c.h, bits[i] ? "background:#000" : "outline:1px solid #bbb"); });
  for (let y = 70; y < 120; y += 22) inner += box(300, y, 400, 6, "background:#444");            // 제목 줄
  for (const [k, r] of Object.entries(pg.regions || {})) inner += box(r[0], r[1], r[2] - r[0], r[3] - r[1], "border:2px solid #111;border-radius:6px;box-sizing:border-box");
  for (let y = 150; y < 1270; y += 30) inner += box(30 + (y % 90), y, 360 + ((y * 37) % 420), 5, "background:#333");   // 글줄
  const scrib = [];
  for (let i = 0; i < 18; i++) { const y = (off + (520 + i * 40) * U).toFixed(1); scrib.push(`<path d="M${(off + 60 * U).toFixed(1)} ${y} q 30 -14 60 0 t 60 0 t 60 0 t 60 0" stroke="#1b1b1b" stroke-width="3" fill="none"/>`); }
  return `<!doctype html><html><body style="margin:0;background:#5d5a55;width:1200px;height:1600px;overflow:hidden">
    <div style="position:absolute;left:150px;top:110px;width:900px;height:1273px;background:#f7f6f1;${tilt ? "transform:perspective(2200px) rotateX(7deg) rotateZ(-3.5deg);" : ""}${blur ? `filter:blur(${blur}px);` : ""}box-shadow:0 12px 40px rgba(0,0,0,.45)">
      ${inner}<svg width="900" height="1273" style="position:absolute;left:0;top:0">${scrib.join("")}</svg>
    </div></body></html>`;
}
async function makePhotos(browser) {
  const ctx = await browser.newContext({ viewport: { width: 1200, height: 1600 } });
  const p = await ctx.newPage();
  const out = {};
  const check = SPEC.sheet.pagecode.check;
  const jobs = [...SPEC.pages.map((pg) => [`p${pg.no}`, pg.no, check, {}]), ["blur3", 3, check, { blur: 5 }], ["other3", 3, (check + 7) % 32, {}]];
  for (const [name, no, ck, opt] of jobs) {
    await p.setContent(sheetHtml(no, ck, opt));
    const f = path.join(TMP, name + ".png");
    await p.screenshot({ path: f });
    out[name] = f;
  }
  await ctx.close();
  return out;
}

// ── 스모크 ──────────────────────────────────────────────────────────────────
let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}`;
  const browser = await chromium.launch({ headless: !HEADED });
  const photos = await makePhotos(browser);
  fs.mkdirSync(SHOTS, { recursive: true });
  const errors = [];
  const newPage = async (opts) => {
    const ctx = await browser.newContext({ viewport: { width: 420, height: 880 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
    page.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) errors.push("console: " + m.text()); });
    await mockSupabase(page, opts);
    await page.route(/https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com|api\.open-meteo\.com)\//, (r) => r.abort());
    return page;
  };
  const text = async (page) => (await page.locator("body").innerText()).replace(/\s+/g, " ");
  const shot = async (page, name) => { try { await page.screenshot({ path: path.join(SHOTS, "assess-" + name + ".png"), fullPage: true }); } catch { /* */ } };
  const upload = async (page, key) => { await page.locator('input[type=file][capture]').setInputFiles(photos[key]); };

  try {
    // A. 비로그인 — QR 로 연 평가
    let page = await newPage({ session: false });
    await page.goto(`${base}/e/SAMPLE01`);
    await page.getByRole("button", { name: "문제 보고 시작하기" }).waitFor({ timeout: 15000 });
    let t = await text(page);
    ok(t.includes(SPEC.title) && t.includes("3문제 · 30점") && t.includes("로그인 없이 응시"), "표지: 제목·문제 수·비로그인 안내");
    await shot(page, "00-cover");
    await page.getByRole("button", { name: "문제 보고 시작하기" }).click();
    await page.getByText("내 시험지와 같은지 확인해요").waitFor();
    t = await text(page);
    ok((await page.locator(".as-q").count()) === 3 && t.includes("과학관 입장료") && (await page.locator(".as-fig img").count()) === 1, "열람: 문제 3개·그림 1개");
    ok(await page.locator(".as-q .mf").count() >= 0 && !t.includes("[["), "열람: MathIR 마커가 그대로 보이지 않음");
    ok(await page.getByRole("button", { name: /촬영 시작/ }).isDisabled(), "열람: 대조 확인 전에는 촬영 시작 잠김");
    await page.getByText("내 시험지와 문제가 같아요").click();
    await shot(page, "01-view");
    await page.getByRole("button", { name: /촬영 시작/ }).click();
    await page.getByText("1쪽 찍기").waitFor();
    t = await text(page);
    ok(t.includes("학생 확인 사항") && t.includes("네 귀퉁이의 ■"), "촬영: 1쪽 안내(카메라 연습)");
    await shot(page, "02-shoot-p1");

    // 흐린 사진 → 다시 찍기 + '이대로 보내기'
    await upload(page, "blur3");
    await page.locator(".as-note.bad").waitFor({ timeout: 15000 });
    t = await text(page);
    ok(/흔들렸어요|흐리게/.test(t) && (await page.getByRole("button", { name: "이대로 보내기" }).count()) === 1, "흐린 사진 → 다시 찍기 안내 + '이대로 보내기'");
    // 다른 평가 시험지 → 거절
    await upload(page, "other3");
    await page.getByText("이 평가의 시험지가 아니에요").waitFor({ timeout: 15000 });
    ok(true, "다른 평가 시험지 → '이 평가의 시험지가 아니에요'");

    await upload(page, "p1");
    await page.getByText("1쪽을 받았어요").waitFor({ timeout: 15000 });
    await page.getByText("2쪽 찍기").waitFor({ timeout: 5000 });
    ok(true, "1쪽 → 받음 → 2쪽 안내로");
    await upload(page, "p2");
    await page.getByText("2쪽을 받았어요").waitFor({ timeout: 15000 });
    await page.getByText("3쪽 찍기").waitFor({ timeout: 5000 });
    // 순서를 바꿔 4쪽을 먼저 찍는다
    await upload(page, "p4");
    await page.getByText(/3쪽이 아니라 4쪽이었어요/).waitFor({ timeout: 15000 });
    t = await text(page);
    ok(t.includes("3쪽 찍기"), "순서가 바뀐 쪽(4쪽) → 4쪽으로 받고 3쪽 안내 유지");
    await shot(page, "03-shoot-swap");
    await upload(page, "p3");
    await page.getByText("3쪽을 받았어요").waitFor({ timeout: 15000 });
    await upload(page, "p5");
    await page.getByText(/2쪽에 쓴 이름이 맞나요|채점이 끝났어요|채점하는 중/).first().waitFor({ timeout: 20000 });
    ok((await text(page)).includes("채점") , "마지막 쪽 뒤 → 채점 기다리기 화면");
    await page.getByText("✅ 채점이 끝났어요").waitFor({ timeout: 20000 });
    const pageCalls = calls.filter((c) => c.op === "page");
    ok(JSON.stringify(pageCalls.map((c) => c.page_no)) === "[1,2,4,3,5]", `서버로 간 쪽 번호 = 사진에서 읽은 쪽 (${pageCalls.map((c) => c.page_no).join(",")})`);
    ok(!pageCalls[0].hasCrop && pageCalls.slice(1).every((c) => c.hasCrop) && pageCalls.every((c) => !c.hasImage), "1쪽은 사진 없이, 2~5쪽은 판독 영역만(저장 꺼짐 → 전체 사진 안 보냄)");
    ok(calls.some((c) => c.op === "grade" && c.page_no === 5), "판독만 된 쪽(문제 3)은 채점을 따로 요청");
    t = await text(page);
    ok(t.includes("홍길동") && t.includes("중2"), "2쪽 판독 이름 확인 카드");
    ok(await page.getByRole("button", { name: "제출하고 결과 보기" }).isDisabled(), "이름 확인 전에는 제출 잠김(비로그인)");
    await shot(page, "04-wrap");
    await page.getByRole("button", { name: "맞아요" }).click();
    await page.getByText("👤 응시자").waitFor();
    await page.getByRole("button", { name: "제출하고 결과 보기" }).click();
    await page.locator(".as-score").waitFor({ timeout: 10000 });
    t = await text(page);
    ok(t.includes("28") && t.includes("/ 30점") && (await page.locator(".as-res").count()) === 3, "결과: 28/30 · 문제 3개");
    ok(t.includes("정답") && t.includes("7명"), "결과: 정답 공개(after_submit)");
    await page.locator("summary", { hasText: "AI가 읽은 내 풀이" }).first().click();
    ok((await page.locator(".as-read .st").count()) >= 1, "결과: 판독문에 그은 줄(취소선)");
    await page.getByRole("button", { name: /잘못 읽었어요/ }).first().click();
    await page.locator(".as-flag input").fill("7을 1로 읽었어요");
    await page.getByRole("button", { name: "보내기" }).click();
    await page.getByText("알려 줬어요").waitFor();
    ok(calls.some((c) => c.op === "flag"), "결과: '잘못 읽었어요' 보내기");
    ok(t.includes("로그인하고 담기"), "결과: 비로그인 → 로그인하고 담기");
    await shot(page, "05-result");
    // 다시 열면 결과로 바로
    await page.goto(`${base}/e/SAMPLE01`);
    await page.locator(".as-score").waitFor({ timeout: 10000 });
    ok(true, "같은 기기에서 다시 열면 결과 화면");
    await page.context().close();

    // B. 로그인 학생 — 대시보드 알림 카드 · 토스트 · 학습 도구 · 목록
    page = await newPage({ session: true });
    await page.goto(`${base}/walking`);
    await page.getByText("📝 서술형 평가").first().waitFor({ timeout: 15000 });
    t = await text(page);
    ok(t.includes(SPEC.title) && t.includes("NEW"), "대시보드: 서술형 평가 카드 + NEW");
    await page.getByText("새 서술형 평가가 열렸어요").waitFor({ timeout: 5000 });
    ok(true, "대시보드: 새 평가 토스트");
    await shot(page, "06-dash");
    await page.getByText("새 서술형 평가가 열렸어요").click();
    await page.getByText("김민준").first().waitFor({ timeout: 10000 });
    ok(page.url().endsWith("/e/SAMPLE01"), "토스트 → /e/SAMPLE01 (로그인 이름으로 응시)");
    await page.goto(`${base}/walking#/tools`);
    await page.getByText("선생님이 낸 서술형 시험지를").waitFor({ timeout: 10000 });
    ok(true, "학습 도구: 서술형 평가 카드");
    await page.goto(`${base}/e`);
    await page.getByText("지금 열린 평가").waitFor({ timeout: 10000 });
    ok((await text(page)).includes(SPEC.title), "/e 목록: 열린 평가");
    await page.context().close();

    // C. 관리자 — JSON 등록
    page = await newPage({ session: true, role: "admin" });
    await page.goto(`${base}/walking#/admin/assess`);
    await page.getByText("① 평가 등록").waitFor({ timeout: 15000 });
    await page.locator('input[type=file][accept*=json]').setInputFiles(path.join(ROOT, "tests/fixtures/assess-SAMPLE01.json"));
    await page.getByRole("button", { name: "등록하기" }).waitFor();
    t = await text(page);
    ok(t.includes("SAMPLE01") && t.includes("3문제 · 30점"), "관리자: JSON 검사 통과 → 미리보기");
    await page.getByRole("button", { name: "등록하기" }).click();
    await page.getByText("SAMPLE01 등록 완료").waitFor({ timeout: 10000 });
    await page.locator(".aa-set").first().waitFor();
    ok(st.adminCalls.includes("admin_register") && (await text(page)).includes("응시 중"), "관리자: 등록 → 목록에 '응시 중'");
    await shot(page, "07-admin");
    await page.context().close();
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e.message.split("\n")[0]);
    try { const pgs = browser.contexts().flatMap((c) => c.pages()); for (const pg of pgs) { console.log("  화면:", (await pg.locator("body").innerText()).replace(/\s+/g, " ").slice(0, 600)); await pg.screenshot({ path: path.join(SHOTS, "assess-fail.png"), fullPage: true }); } } catch { /* */ }
  } finally {
    ok(errors.length === 0, "콘솔 오류 0" + (errors.length ? ` — ${errors.slice(0, 3).join(" | ")}` : ""));
    await browser.close();
    srv.close();
    fs.rmSync(TMP, { recursive: true, force: true });
    console.log(`\n${pass} passed, ${fail} failed`);
    process.exit(fail ? 1 : 0);
  }
})();
