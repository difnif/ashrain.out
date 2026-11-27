// 개념 화면 레이아웃 점검 — 휴대폰 세로·가로, 태블릿, 데스크톱에서 오른쪽이 잘리거나 튀어나오는 곳을 찾는다.
//   node tests/smoke/concept-layout.smoke.mjs [--quick] [--shots] [--only=stress|elem|list|practice|majors|theme]
// 준비: `npx vite build` (dist/ 필요) · playwright(전역) + Chromium. Supabase 는 모의 응답으로 바꾼다.
// 재는 것
//   page   문서 가로 넘침(document.scrollWidth > clientWidth) — 화면이 옆으로 밀리는 것
//   out    화면 밖으로 나간 요소(가로 스크롤 칸 안·잘라 내는 부모 안은 빼고)
//   clip   overflow:hidden 칸이 안의 내용을 잘라 먹는 것(말줄임 … 은 의도라 뺀다)
//   hscr   의도하지 않은 가로 스크롤 칸(표 · 칩 줄 같은 의도된 칸은 뺀다)
// 테마 단추: 모든 화면 맨 위에 다크/라이트 단추가 하나 보이는지, 다른 단추를 가리지 않는지도 본다(--only=theme).
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); }
catch { ({ chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright")); }

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "../..");
const DIST = path.join(ROOT, "dist");
const QUICK = process.argv.includes("--quick");
const SHOTS = process.argv.includes("--shots");
const ONLY = (process.argv.find((a) => a.startsWith("--only=")) || "").slice(7).split(",").filter(Boolean);
const want = (k) => !ONLY.length || ONLY.includes(k);
const SHOT_DIR = process.env.SMOKE_SHOTS || path.join(HERE, "shots", "layout");

const FX = JSON.parse(fs.readFileSync(path.join(ROOT, "tests/fixtures/concept-layout.json"), "utf8"));
const STRESS = FX.concept;
const ELEM = fs.readdirSync(path.join(ROOT, "public/concepts/elem")).filter((f) => f.endsWith(".json")).sort()
  .flatMap((f) => JSON.parse(fs.readFileSync(path.join(ROOT, "public/concepts/elem", f), "utf8")))
  .map((c) => ({ id: c.id, unit_id: c.unitId, title: c.title, subtitle: c.subtitle || "", sort_order: c.order, blocks: c.blocks,
    cover: null, ext_panels: null, ext_figure: null }));
const ROWS = new Map([[STRESS.id, STRESS], ...ELEM.map((c) => [c.id, c])]);
const LIST = [STRESS, ...FX.siblings, ...ELEM].map(({ id, unit_id, title, subtitle, sort_order }) => ({ id, unit_id, title, subtitle, sort_order }));

// 예제·유제 — 긴 낱말 · 긴 보기
const PSET = {
  concept_id: STRESS.id, title: "예제·유제 — combinations_with_replacement · 3602879701896397/36028797018963968",
  problems: [
    { id: "p01", level: "기본", kind: "예제", text: [{ t: "y = 3602879701896397/36028797018963968x 는 " }, { t: "정비례" }, { t: "인가? combinations_with_replacement 로 세어 보자." }],
      steps: [{ hl: [1], note: "비율 y/x 가 일정한지 본다 — Science·Technology·Engineering·Math", expr: "y/x = 3602879701896397/36028797018963968" }],
      answer: { label: "판정", accept: ["정비례"], placeholder: "예: 정비례" } },
    { id: "p02", level: "표준", kind: "유제", text: [{ t: "다음 중 " }, { t: "항등식" }, { t: "인 것은?" }],
      choices: ["ax+b = 0 이 x에 대한 항등식 → a = 0, b = 0", "(x−1)(x²+x+1)(x+1)(x²−x+1)=x⁶−1", "combinations_with_replacement", "1a⃗ = a⃗ · 0a⃗ = 0⃗ · (−1)a⃗ = −a⃗", "x = 4503599627370496/1501199875790165"],
      steps: [{ hl: [1], note: "어떤 x 에도 참", expr: "(x³−1)(x³+1) = x⁶−1" }],
      answer: { label: "정답 번호", accept: ["2"], placeholder: "번호만 입력 (예: 2)" } },
  ],
};

// ── 화면 크기 ──
const PHONE_P = [[280, 653], [320, 568], [360, 740], [375, 667], [390, 844], [393, 852], [412, 915], [430, 932]];
const PHONE_L = [[653, 280], [568, 320], [667, 375], [740, 360], [844, 390], [915, 412], [932, 430]];
const TABLET = [[768, 1024], [1024, 768], [800, 1280], [1280, 800]];
const DESK = [[1366, 768]];
const VIEWS = (QUICK ? [[280, 653], [320, 568], [375, 667], [390, 844], [667, 375], [844, 390], [768, 1024], [1366, 768]]
  : [...PHONE_P, ...PHONE_L, ...TABLET, ...DESK]).map(([w, h]) => ({ w, h, mobile: w < 1100 || h < 500 }));

// ── 정적 서버 (dist + SPA fallback) ──
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ttf": "font/ttf", ".ico": "image/x-icon", ".webmanifest": "application/manifest+json", ".webp": "image/webp", ".jpg": "image/jpeg" };
function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, "http://x");
      let f = path.join(DIST, decodeURIComponent(u.pathname));
      if (!f.startsWith(DIST)) { res.writeHead(403); return res.end(); }
      if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f = path.join(DIST, "index.html");
      res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(0, "127.0.0.1", () => resolve({ srv, port: srv.address().port }));
  });
}

// ── Supabase 모의 ──
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
function makeSession(role) {
  const USER = { id: "00000000-0000-4000-8000-000000000001", aud: "authenticated", role: "authenticated", email: "layout@example.com",
    app_metadata: { provider: "email", providers: ["email"] }, user_metadata: { last_role: role === "admin" ? "instructor" : "student" }, factors: [], created_at: "2026-01-01T00:00:00Z" };
  const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], app_metadata: USER.app_metadata, user_metadata: USER.user_metadata, session_id: "s1" })}.sig`;
  const SESSION = { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r1", user: USER };
  const PROFILE = { id: USER.id, role, member_code: "LAYOUT", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "2011-03-01", settings: {}, honor_path: false };
  return { USER, SESSION, PROFILE };
}

async function mockAll(ctx, { role = "student", theme = "dark", login = true } = {}) {
  const { USER, SESSION, PROFILE } = makeSession(role);
  await ctx.route("https://placeholder.supabase.co/**", (route) => {
    const req = route.request(); const u = new URL(req.url()); const accept = req.headers()["accept"] || "";
    const json = (obj, headers = {}) => route.fulfill({ status: 200, contentType: "application/json", headers, body: JSON.stringify(obj) });
    if (u.pathname.startsWith("/auth/v1/user")) return login ? json(USER) : route.fulfill({ status: 401, contentType: "application/json", body: "{}" });
    if (u.pathname.startsWith("/auth/v1/token")) return json(SESSION);
    if (u.pathname.startsWith("/auth/v1/factors") || u.pathname.includes("/mfa")) return json({ all: [], totp: [] });
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/storage/v1/")) {
      if (u.pathname.includes("/object/list/")) return json([]);
      return route.fulfill({ status: 404, body: "" });
    }
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0];
      const wantObj = accept.includes("pgrst.object");
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0", "access-control-expose-headers": "content-range" }, body: "" });
      if (table === "concepts") {
        const idq = u.searchParams.get("id");
        if (idq && idq.startsWith("eq.")) {
          const row = ROWS.get(idq.slice(3)) || null;
          return row ? json(wantObj ? row : [row]) : route.fulfill({ status: 406, contentType: "application/json", body: JSON.stringify({ code: "PGRST116", message: "no rows" }) });
        }
        return json(LIST);
      }
      if (table === "practice_sets") return json(wantObj ? PSET : [PSET]);
      if (table === "events") {   // 상단 D-day 배지까지 그려지게(가장 좁은 화면에서 상단 줄이 넘치지 않는지)
        const d = new Date(Date.now() + 7 * 86400000).toISOString().slice(0, 10);
        return json([{ date: d, title: "2학기 기말고사" }]);
      }
      if (table === "profiles") return json(wantObj ? PROFILE : [PROFILE]);
      if (table === "memberships" || table === "academy_members" || table === "members")
        return json(role === "admin" ? [{ role: "instructor", academy_id: "a1", status: "active" }] : []);
      if (req.method() === "POST" || req.method() === "PATCH") return json(wantObj ? {} : []);
      return json(wantObj ? null : [], { "content-range": "0-0/0" });
    }
    return json({});
  });
  await ctx.route("**/api/**", (route) => {
    const u = new URL(route.request().url());
    let body = {};
    try { body = JSON.parse(route.request().postData() || "{}"); } catch { /* */ }
    if (u.pathname === "/api/review") {
      if (body.action === "status") return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ready: true, concepts: [{ concept_id: STRESS.id, rank: 1, cap: 5, done: 0, remaining: 5 }], today_done: 0, today_cap: 10, reward: 5 }) });
      if (body.action === "start") return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ review_id: "r1", items: [], rank: 1, cap: 5, done: 0, remaining: 5, today_done: 0, today_cap: 10, rewardable: true, reward: 5, ready: true }) });
    }
    if (u.pathname === "/api/photo" && body.task === "assess") return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ open: [], mine: [] }) });
    return route.fulfill({ status: 200, contentType: "application/json", body: "{}" });
  });
  await ctx.route(/https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com|unpkg\.com)\//, (r) => r.abort());
  await ctx.addInitScript(([key, sess, th, login]) => {
    try {
      if (login) localStorage.setItem(key, JSON.stringify(sess));
      localStorage.setItem("ashrain-theme", th);
    } catch { /* */ }
  }, ["sb-placeholder-auth-token", SESSION, theme, login]);
}

// ── 재기(브라우저 안) ──
function auditInPage(opts) {
  const INTENDED_HSCROLL = opts.hscroll;   // 의도된 가로 스크롤 칸(클래스 앞부분)
  const CLIP_OK = opts.clipOk;             // 잘라 내는 것이 의도인 칸(무대 · 그림 액자 · 표지 등)
  const de = document.documentElement;
  const vw = de.clientWidth;
  const res = { vw, docSW: de.scrollWidth, out: [], clip: [], hscr: [] };
  const cls = (el) => (typeof el.className === "string" ? el.className : (el.className && el.className.baseVal) || "").trim();
  const name = (el) => {
    const c = cls(el).split(/\s+/).filter(Boolean).slice(0, 2).join(".");
    return el.tagName.toLowerCase() + (c ? "." + c : "");
  };
  const where = (el) => { const parts = []; let e = el; for (let i = 0; e && e !== document.body && i < 3; i++, e = e.parentElement) parts.unshift(name(e)); return parts.join(">"); };
  const matches = (el, list) => { const c = " " + cls(el) + " "; return list.some((p) => c.includes(" " + p) || cls(el).split(/\s+/).some((k) => k.startsWith(p))); };
  for (const el of document.querySelectorAll("body *")) {
    const tag = el.tagName.toLowerCase();
    if (tag === "style" || tag === "script") continue;
    if (el.closest("svg") && tag !== "svg") continue;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden" || cs.display === "contents") continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    // 조상 중 잘라 내거나 스크롤하는 칸이 있으면 화면 밖 판정은 그 칸이 맡는다
    let p = el.parentElement, boxed = false;
    while (p && p !== document.body) {
      const pcs = getComputedStyle(p);
      if (pcs.overflowX !== "visible") { boxed = true; break; }
      p = p.parentElement;
    }
    if (!boxed && cs.position !== "fixed" && (r.right > vw + 1 || r.left < -1))
      res.out.push({ at: where(el), l: Math.round(r.left), r: Math.round(r.right), w: Math.round(r.width), t: (el.innerText || "").replace(/\s+/g, " ").slice(0, 36) });
    if (cs.position === "fixed" && (r.right > vw + 1 || r.left < -1) && r.width < vw * 3)
      res.out.push({ at: where(el) + "(fixed)", l: Math.round(r.left), r: Math.round(r.right), w: Math.round(r.width), t: (el.innerText || "").replace(/\s+/g, " ").slice(0, 36) });
    const over = el.scrollWidth > el.clientWidth + 1;
    if (!over) continue;
    if (/(hidden|clip)/.test(cs.overflowX)) {
      if (cs.textOverflow === "ellipsis" || matches(el, CLIP_OK)) continue;
      res.clip.push({ at: where(el), sw: el.scrollWidth, cw: el.clientWidth, t: (el.innerText || "").replace(/\s+/g, " ").slice(0, 36) });
    } else if (/(auto|scroll)/.test(cs.overflowX) && tag !== "textarea" && tag !== "input") {
      if (matches(el, INTENDED_HSCROLL)) continue;
      res.hscr.push({ at: where(el), sw: el.scrollWidth, cw: el.clientWidth });
    }
  }
  return res;
}
const AUDIT_OPTS = {
  hscroll: ["cv-twrap", "st-chips", "st-gk", "st-uchips", "sh-subtabs", "sh-admin", "fig-stage", "mm-eq", "sg-tabs", "pv-expr", "mm-tw", "mm-code"],
  clipOk: ["sf3-", "afs-", "cv-cover", "cav-stage", "st-ic", "pg", "sh-", "rv-drop"],
};

// ── 실행 ──
const findings = [];
let checks = 0;
const record = (scope, view, theme, state, a) => {
  checks++;
  const bad = [];
  if (a.docSW > a.vw + 1) bad.push(`page ${a.docSW}>${a.vw}`);
  for (const o of a.out.slice(0, 4)) bad.push(`out ${o.at} [${o.l}..${o.r}] «${o.t}»`);
  for (const c of a.clip.slice(0, 4)) bad.push(`clip ${c.at} ${c.sw}>${c.cw} «${c.t}»`);
  for (const h of a.hscr.slice(0, 3)) bad.push(`hscr ${h.at} ${h.sw}>${h.cw}`);
  if (bad.length) findings.push({ scope, view: `${view.w}x${view.h}`, theme, state, bad, n: a.out.length + a.clip.length + a.hscr.length });
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function openAll(page) {
  // 접기 칸을 모두 펼치고, 정답 보기를 누르고, 끝까지 내려 움직이는 예시 카드를 다 받는다
  await page.evaluate(() => { document.querySelectorAll(".cv-pbtn").forEach((b) => { if (!b.classList.contains("on")) b.click(); }); });
  await page.evaluate(() => { document.querySelectorAll(".cv-btn").forEach((b) => { if (/정답 보기/.test(b.textContent)) b.click(); }); });
  for (let i = 0; i < 40; i++) {
    const done = await page.evaluate(() => { window.scrollBy(0, Math.round(innerHeight * 0.8)); return innerHeight + scrollY >= document.documentElement.scrollHeight - 4; });
    await sleep(60);
    if (done) break;
  }
  await page.waitForFunction(() => !document.querySelector(".cav-wait, .cv-avwait"), null, { timeout: 8000 }).catch(() => {});
  await sleep(250);
}

async function shot(page, name) {
  if (!SHOTS) return;
  fs.mkdirSync(SHOT_DIR, { recursive: true });
  await page.screenshot({ path: path.join(SHOT_DIR, name + ".png"), fullPage: true }).catch(() => {});
}

(async () => {
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}`;
  const browser = await chromium.launch({ headless: true });
  const errors = [];
  const t0 = Date.now();

  const newPage = async (view, theme, role = "student", login = true) => {
    const ctx = await browser.newContext({ viewport: { width: view.w, height: view.h }, deviceScaleFactor: 2, isMobile: view.mobile, hasTouch: view.mobile, locale: "ko-KR" });
    await mockAll(ctx, { role, theme, login });
    const page = await ctx.newPage();
    page.on("pageerror", (e) => errors.push(`${view.w}x${view.h} pageerror: ${e.message}`));
    return { ctx, page };
  };
  const audit = (page) => page.evaluate(auditInPage, AUDIT_OPTS);

  try {
    // 0) 확인용 — --probe=<주소> [--role=admin] [--w=360] : 한 화면을 열어 글과 사진만 남긴다
    const probe = (process.argv.find((a) => a.startsWith("--probe=")) || "").slice(8);
    if (probe) {
      const role = (process.argv.find((a) => a.startsWith("--role=")) || "--role=student").slice(7);
      const w = +((process.argv.find((a) => a.startsWith("--w=")) || "--w=360").slice(4));
      const h = +((process.argv.find((a) => a.startsWith("--h=")) || "--h=740").slice(4));
      const theme = (process.argv.find((a) => a.startsWith("--theme=")) || "--theme=dark").slice(8);
      const { page } = await newPage({ w, h, mobile: true }, theme, role);
      await page.goto(base + probe);
      await sleep(2500);
      console.log((await page.locator("body").innerText()).replace(/\s*\n\s*/g, " | ").slice(0, 900));
      console.log(JSON.stringify(await audit(page)).slice(0, 1500));
      console.log("테마 단추:", JSON.stringify(await page.evaluate(() => [...document.querySelectorAll("[data-theme-toggle]")].map((b) => { const q = b.getBoundingClientRect(); return { cls: b.className, x: Math.round(q.left), y: Math.round(q.top), w: Math.round(q.width) }; }))));
      fs.mkdirSync(SHOT_DIR, { recursive: true });
      await page.screenshot({ path: path.join(SHOT_DIR, "probe.png"), fullPage: false });
      console.log("사진:", path.join(SHOT_DIR, "probe.png"));
      return;
    }
    // 1) 점검용 개념 — 전 화면 크기 × 두 테마 × (본문 · 질문창 · 복습 소개 · 복습 읽기)
    if (want("stress")) for (const theme of ["dark", "light"]) for (const view of VIEWS) {
      const { ctx, page } = await newPage(view, theme);
      await page.goto(`${base}/walking#/c/${STRESS.id}`);
      await page.locator(".cv-main section").first().waitFor({ timeout: 20000 });
      await openAll(page);
      record("stress", view, theme, "본문", await audit(page));
      await shot(page, `stress-${theme}-${view.w}x${view.h}`);
      // 질문창
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.evaluate(() => document.querySelector(".cv-qmark")?.click());   // 화면 밖으로 밀려나 있어도 연다(밀려난 것은 위 본문 점검이 잡는다)
      await page.locator(".qch-sheet").waitFor({ timeout: 5000 }).catch(() => {});
      await sleep(250);
      record("stress", view, theme, "질문창", await audit(page));
      await page.evaluate(() => document.querySelector(".qch-x")?.click());
      // 복습 모드
      await page.evaluate((id) => { location.hash = `#/c/${id}?review=1`; }, STRESS.id);
      await page.locator(".rv-actions").waitFor({ timeout: 8000 }).catch(() => {});
      await sleep(200);
      record("stress", view, theme, "복습 소개", await audit(page));
      await page.evaluate(() => document.querySelector(".rv-actions .sv-btn.pri")?.click());
      await page.locator(".rv-bar").waitFor({ timeout: 5000 }).catch(() => {});
      await sleep(300);
      record("stress", view, theme, "복습 읽기", await audit(page));
      await ctx.close();
    }

    // 2) 기본 제공 초등 개념 전부 — 좁은 세로 · 가로
    if (want("elem")) {
      const ev = (QUICK ? [[280, 653], [667, 375]] : [[280, 653], [320, 568], [375, 667], [667, 375]]).map(([w, h]) => ({ w, h, mobile: true }));
      for (const view of ev) {
        const { ctx, page } = await newPage(view, "dark");
        await page.goto(`${base}/walking#/c/${ELEM[0].id}`);
        for (const c of ELEM) {
          await page.evaluate((id) => { location.hash = `#/c/${id}`; }, c.id);
          await page.waitForFunction((t) => document.querySelector(".cv-title")?.textContent === t, c.title, { timeout: 10000 }).catch(() => {});
          await openAll(page);
          record("elem:" + c.id, view, "dark", "본문", await audit(page));
        }
        await ctx.close();
      }
    }

    // 3) 개념 목록 · 4) 예제·유제
    if (want("list") || want("practice")) for (const theme of ["dark", "light"]) for (const view of VIEWS) {
      const { ctx, page } = await newPage(view, theme);
      if (want("list")) {
        await page.goto(`${base}/walking#/study/concept`);
        await page.locator(".st-root").first().waitFor({ timeout: 15000 }).catch(() => {});
        await sleep(600);
        record("list", view, theme, "개념 목록", await audit(page));
        await shot(page, `list-${theme}-${view.w}x${view.h}`);
      }
      if (want("practice")) {
        await page.goto(`${base}/walking#/p/${STRESS.id}`);
        await page.locator(".pv-card").waitFor({ timeout: 15000 }).catch(() => {});
        await sleep(200);
        record("practice", view, theme, "예제", await audit(page));
        const start = page.locator(".pv-btn-main", { hasText: "해설 시작하기" });
        if (await start.count()) { await start.click(); await sleep(250); record("practice", view, theme, "예제 해설", await audit(page)); }
        const next = page.locator(".pv-chip").nth(1);
        if (await next.count()) { await next.click().catch(() => {}); await sleep(250); record("practice", view, theme, "유제 보기", await audit(page)); }
      }
      await ctx.close();
    }

    // 5) 시록고 「전공 수학」(강사앱) — 서가 · 책마다 차례 · 모든 장(풀이 모두 펼침)
    if (want("majors")) {
      const idx = JSON.parse(fs.readFileSync(path.join(ROOT, "public/majors/index.json"), "utf8"));
      const books = idx.books.map((b) => ({ id: b.id, n: JSON.parse(fs.readFileSync(path.join(ROOT, "public/majors", b.id + ".json"), "utf8")).chapters.length }));
      const mv = (QUICK ? [[280, 653], [360, 740], [740, 360]] : [[280, 653], [320, 568], [360, 740], [390, 844], [667, 375], [844, 390], [768, 1024]]).map(([w, h]) => ({ w, h, mobile: true }));
      for (const view of mv) {
        const { ctx, page } = await newPage(view, "light", "admin");
        await page.goto(`${base}/seirocco#/seogo/jeon`);
        await page.locator(".mm-book").first().waitFor({ timeout: 15000 });
        record("majors", view, "light", "서가", await audit(page));
        for (const b of books) {
          await page.evaluate((id) => { location.hash = `#/seogo/jeon/${id}`; }, b.id);
          await page.locator(".mm-ch").first().waitFor({ timeout: 10000 }).catch(() => {});
          record("majors:" + b.id, view, "light", "차례", await audit(page));
          for (let n = 1; n <= b.n; n++) {
            await page.evaluate(([id, k]) => { location.hash = `#/seogo/jeon/${id}/${k}`; }, [b.id, n]);
            await page.waitForFunction((k) => document.querySelector(".mm-hd h3")?.textContent.startsWith(k + "."), n, { timeout: 10000 }).catch(() => {});
            await page.evaluate(() => { document.querySelectorAll(".d-btn").forEach((x) => { if (/풀이 모두 보기|답 보기|정답/.test(x.textContent)) x.click(); }); });
            await sleep(120);
            record(`majors:${b.id}`, view, "light", `${n}장`, await audit(page));
          }
        }
        await shot(page, `majors-${view.w}x${view.h}`);
        await ctx.close();
      }
    }

    // 6) 테마 단추 — 화면마다 맨 위에 하나, 누르면 바뀌고, 다른 단추를 가리지 않는다
    if (want("theme")) {
      const S = { role: "student", login: true }, A = { role: "admin", login: true }, N = { role: "student", login: false };
      const ROUTES = [
        ["/walking#/", "대시보드", S], ["/walking#/study/concept", "개념 목록", S], ["/walking#/study/practice", "연습문제", S],
        ["/walking#/tools", "학습 도구", S], ["/walking#/records", "기록", S],
        [`/walking#/c/${STRESS.id}`, "개념 보기", S], [`/walking#/c/${STRESS.id}?review=1`, "복습", S], [`/walking#/p/${STRESS.id}`, "예제·유제", S],
        ["/walking#/me", "마이페이지", S], ["/walking#/learn/wrong", "오답노트", S], ["/walking#/solve/photo", "사진 풀이", S],
        ["/walking#/library", "서재", S], ["/walking#/news", "신문", S], ["/walking#/duty", "조교", S], ["/walking#/philosophy", "철학", S],
        ["/walking#/guardian", "보호자 동의", S], ["/walking#/onboarding", "온보딩", S], ["/walking#/portrait", "초상화", S],
        ["/walking#/board/notice", "게시판", S], ["/walking#/av/cnt100", "시청각", S],
        ["/answers", "빠른 정답지", S], ["/e", "서술형 평가", S],
        ["/walking#/", "로그인", N], ["/walking#/signup", "가입", N], ["/walking#/find", "계정 찾기", N], ["/walking#/qr", "QR 로그인", N], ["/", "관문", N],
        ["/walking#/admin/concepts", "관리·개념", A], ["/walking#/admin/qna", "관리·질문", A], ["/walking#/admin/chats", "관리·대화", A],
        ["/walking#/admin/display", "교실 모니터", A], ["/walking#/admin/users", "관리·회원", A],
      ];
      const tv = (QUICK ? [[320, 568], [844, 390]] : [[280, 653], [320, 568], [390, 844], [844, 390], [1366, 768]]).map(([w, h]) => ({ w, h, mobile: w < 1100 }));
      for (const view of tv) {
        const pages = {};
        for (const [route, label, o] of ROUTES) {
          const k = o.role + (o.login ? "" : "-out");
          pages[k] = pages[k] || await newPage(view, "dark", o.role, o.login);
          const { page } = pages[k];
          await page.goto("about:blank");                 // 주소의 # 만 바뀌면 다시 읽지 않으니 매번 새로 연다
          await page.goto(base + route);
          await sleep(1300);
          const r = await page.evaluate(() => {
            const visible = (b) => { const q = b.getBoundingClientRect(); const cs = getComputedStyle(b); return q.width > 0 && q.height > 0 && cs.visibility !== "hidden" && cs.display !== "none" && q.bottom > 0 && q.top < 90; };
            const vis = [...document.querySelectorAll("[data-theme-toggle]")].filter(visible);
            const b = vis[0];
            let hit = null;
            if (b) {
              const q = b.getBoundingClientRect();
              const pts = [[q.left + 4, q.top + 4], [q.right - 4, q.top + 4], [q.left + 4, q.bottom - 4], [q.right - 4, q.bottom - 4], [q.left + q.width / 2, q.top + q.height / 2]];
              for (const [x, y] of pts) {
                for (const e of document.elementsFromPoint(x, y)) {
                  if (b.contains(e) || e.contains(b)) continue;
                  const it = e.closest("button, a, input, select, textarea, label, [role=button], [role=tab], [role=radio]");
                  if (it && !it.contains(b) && !b.contains(it)) { hit = (it.tagName.toLowerCase() + "." + String(it.className || "").split(" ")[0]) + " «" + (it.textContent || "").trim().slice(0, 14) + "»"; break; }
                }
                if (hit) break;
              }
            }
            let covered = null;
            if (b) {
              const q = b.getBoundingClientRect();
              const e = document.elementFromPoint(q.left + q.width / 2, q.top + q.height / 2);
              if (e && !b.contains(e)) covered = e.tagName.toLowerCase() + "." + String(e.className || "").split(" ")[0];
            }
            return { n: vis.length, top: b ? Math.round(b.getBoundingClientRect().top) : null, hit, covered, theme: document.documentElement.dataset.theme, app: document.documentElement.dataset.app };
          });
          checks++;
          const bad = [];
          const own = /admin\/display|#\/av\//.test(route);   // 무대(교실 모니터 · 시청각) — 제 밝기 단추가 조작 막대에 있다
          if (own ? r.n !== 0 : r.n !== 1) bad.push(`테마 단추 ${r.n}개`);
          if (r.hit) bad.push(`가림: ${r.hit}`);
          if (r.covered) bad.push(`단추가 덮임: ${r.covered}`);
          if (r.n >= 1) {
            await page.evaluate(() => document.querySelector("[data-theme-toggle]")?.click());
            await sleep(150);
            const th = await page.evaluate(() => document.documentElement.dataset.theme);
            if (th === r.theme) bad.push("눌러도 테마가 안 바뀜");
            await page.evaluate(() => document.querySelector("[data-theme-toggle]")?.click());
            await sleep(100);
          }
          if (route === "/answers") {
            await page.evaluate(() => { [...document.querySelectorAll(".ak-chips button")].find((x) => /서술형/.test(x.textContent))?.click(); });
            await sleep(300);
            await page.evaluate(() => document.querySelector(".ak-pop-card button")?.click());   // 서술형 첫 안내 팝업 닫기
            await sleep(200);
            await page.evaluate(() => document.querySelector(".ak-cell")?.click());
            await sleep(400);
            const x = await page.evaluate(() => {
              const c = document.querySelector(".ak-sheet .ak-back");
              if (!c) return "no-sheet";
              const q = c.getBoundingClientRect();
              const e = document.elementFromPoint(q.left + q.width / 2, q.top + q.height / 2);
              return e && c.contains(e) ? null : (e ? e.tagName.toLowerCase() + "." + String(e.className || "").split(" ")[0] : "none");
            });
            if (x) bad.push(`해설 시트 ✕ 가림: ${x}`);
          }
          if (bad.length) findings.push({ scope: "theme:" + label, view: `${view.w}x${view.h}`, theme: "dark", state: route, bad, n: bad.length });
          await shot(page, `theme-${label}-${view.w}x${view.h}`);
        }
        for (const v of Object.values(pages)) await v.ctx.close();
      }
      // 강사앱 · 학부모앱 — 다크가 없는 한지 테마라 단추를 두지 않는다
      for (const app of ["/seirocco#/", "/jongseong#/"]) {
        const { ctx, page } = await newPage({ w: 390, h: 844, mobile: true }, "dark", "admin");
        await page.goto(base + app);
        await sleep(1500);
        const n = await page.evaluate(() => [...document.querySelectorAll("[data-theme-toggle]")].filter((b) => b.getBoundingClientRect().width > 0).length);
        checks++;
        if (n !== 0) findings.push({ scope: "theme:" + app, view: "390x844", theme: "dark", state: app, bad: [`한지 단일 테마 앱에 테마 단추 ${n}개`], n });
        await ctx.close();
      }
    }
  } finally {
    await browser.close();
    srv.close();
  }

  // ── 보고 ──
  const byKey = new Map();
  for (const f of findings) for (const b of f.bad) {
    const k = f.scope.split(":")[0] + " | " + f.state + " | " + b.replace(/\[\-?\d+\.\.\d+\]|\d+>\d+/g, "#").replace(/«.*»/, "");
    const e = byKey.get(k) || { k, views: new Set(), sample: b, scopes: new Set() };
    e.views.add(f.view + (f.theme === "light" ? "L" : "")); e.scopes.add(f.scope); byKey.set(k, e);
  }
  console.log(`\n점검 ${checks}회 · 문제 있는 경우 ${findings.length} · ${Math.round((Date.now() - t0) / 1000)}초`);
  for (const e of [...byKey.values()].sort((a, b) => b.views.size - a.views.size)) {
    console.log(`- ${e.k}\n    예: ${e.sample}\n    크기: ${[...e.views].slice(0, 12).join(" ")}${e.views.size > 12 ? ` …(+${e.views.size - 12})` : ""}${e.scopes.size > 1 ? `\n    개념: ${[...e.scopes].slice(0, 6).join(" ")}${e.scopes.size > 6 ? " …" : ""}` : ""}`);
  }
  const errs = [...new Set(errors)].filter((e) => !/Failed to load resource|net::ERR|favicon/.test(e));
  if (errs.length) console.log("\n페이지 오류:\n" + errs.slice(0, 10).join("\n"));
  process.exit(findings.length ? 1 : 0);
})();
