// 초등 개념 찾기 — 관리자가 앱을 열면 기본 제공 초등 개념이 DB 에 들어가고(lib/elemSeed.js),
// 학생은 공부하기 › 개념 › 「초등」 → 학기(초1-1 …) → 개념으로 들어간다.
//   node tests/smoke/elem-find.smoke.mjs   (dist 필요 · playwright 전역 + Chromium · Supabase 는 모의 응답)
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
const ELEM_DIR = path.join(ROOT, "public/concepts/elem");
const IDX = JSON.parse(fs.readFileSync(path.join(ELEM_DIR, "index.json"), "utf8"));
const ELEM = IDX.units.flatMap((u) => JSON.parse(fs.readFileSync(path.join(ELEM_DIR, u + ".json"), "utf8")));
const MID = [
  { id: "m1-1-01", unit_id: "m1-1", title: "소인수분해", subtitle: "", sort_order: 1, blocks: [{ id: "b1", type: "text", label: "본문", style: { size: "md", tone: "slate" }, lines: ["소수의 곱으로 나타내기"] }], cover: null },
  { id: "h1-1-01", unit_id: "h1-1", title: "다항식의 연산", subtitle: "", sort_order: 1, blocks: [], cover: null },
];

let pass = 0, fail = 0;
const ok = (c, m) => { if (c) { pass++; console.log("ok   - " + m); } else { fail++; console.log("FAIL - " + m); } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".webp": "image/webp" };
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

const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
function session(role) {
  const USER = { id: "00000000-0000-4000-8000-0000000000e1", aud: "authenticated", role: "authenticated", email: "elem@example.com",
    app_metadata: { provider: "email" }, user_metadata: { last_role: "student" }, factors: [], created_at: "2026-01-01T00:00:00Z" };
  const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", exp: 9999999999, iat: 1700000000, aal: "aal1", session_id: "s1" })}.sig`;
  return { USER, SESSION: { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r1", user: USER },
    PROFILE: { id: USER.id, role, member_code: "ELEM", phone_verified: true, is_minor: false, birth_date: "2016-03-01", settings: {} } };
}

/** db: id → 행. inserts: 받은 POST 기록 */
async function open(browser, base, { role, db, inserts, keepSeed = null }) {
  const { USER, SESSION, PROFILE } = session(role);
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, locale: "ko-KR" });
  await ctx.route("https://placeholder.supabase.co/**", async (route) => {
    const req = route.request(); const u = new URL(req.url()); const accept = req.headers()["accept"] || "";
    const json = (o, h = {}) => route.fulfill({ status: 200, contentType: "application/json", headers: h, body: JSON.stringify(o) });
    if (u.pathname.startsWith("/auth/v1/user")) return json(USER);
    if (u.pathname.startsWith("/auth/v1/")) return json(SESSION);
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0];
      const one = accept.includes("pgrst.object");
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0" }, body: "" });
      if (table === "concepts") {
        if (req.method() === "POST") {
          const rows = JSON.parse(req.postData() || "[]");
          inserts.push({ n: rows.length, prefer: req.headers()["prefer"] || "" });
          for (const r of rows) if (!db.has(r.id)) db.set(r.id, r);
          return route.fulfill({ status: 201, contentType: "application/json", body: "[]" });
        }
        const idq = u.searchParams.get("id");
        if (idq?.startsWith("eq.")) { const r = db.get(idq.slice(3)); return r ? json(one ? r : [r]) : route.fulfill({ status: 406, contentType: "application/json", body: '{"code":"PGRST116"}' }); }
        if (idq?.startsWith("like.")) { const pre = idq.slice(5).replace(/[%*]/g, ""); return json([...db.values()].filter((r) => r.id.startsWith(pre)).map((r) => ({ id: r.id }))); }
        return json([...db.values()].map(({ id, unit_id, title, subtitle, sort_order }) => ({ id, unit_id, title, subtitle, sort_order })));
      }
      if (table === "profiles") return json(one ? PROFILE : [PROFILE]);
      return json(one ? null : []);
    }
    return json({});
  });
  await ctx.route("**/api/**", (r) => r.fulfill({ status: 200, contentType: "application/json", body: "{}" }));
  await ctx.route(/https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net)\//, (r) => r.abort());
  await ctx.addInitScript(([s, k]) => {
    try {
      localStorage.setItem("sb-placeholder-auth-token", JSON.stringify(s));
      localStorage.setItem("ashrain-theme", "dark");
      if (k) localStorage.setItem("ash.elemSeed", k); else localStorage.removeItem("ash.elemSeed");
    } catch { /* */ }
  }, [SESSION, keepSeed]);
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  return { ctx, page, errors };
}

(async () => {
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}`;
  const browser = await chromium.launch({ headless: true });
  try {
    // 1) 관리자 — 초등 개념이 DB 에 하나도 없을 때 앱을 열면 69개가 들어간다
    const db = new Map(MID.map((r) => [r.id, r]));
    const inserts = [];
    const A = await open(browser, base, { role: "admin", db, inserts });
    await A.page.goto(`${base}/walking#/study/concept`);
    await A.page.locator(".st-lv").waitFor({ timeout: 20000 });
    for (let i = 0; i < 40 && !inserts.length; i++) await sleep(150);
    await sleep(600);
    const added = inserts.reduce((n, x) => n + x.n, 0);
    ok(added === IDX.count, `관리자가 열면 기본 제공 초등 개념 ${IDX.count}개를 넣는다 (받은 ${added})`);
    ok(inserts.every((x) => /ignore-duplicates/.test(x.prefer)), "이미 있는 개념은 덮어쓰지 않는다(ignore-duplicates)");
    ok([...db.keys()].filter((k) => k.startsWith("e")).length === IDX.count, "DB 에 초등 개념 69개");
    // 목록이 새로 받아져 「초등」 칸 수가 바로 바뀐다
    await A.page.locator(".st-lv button", { hasText: "초등" }).click();
    await A.page.waitForFunction((n) => /초등\s*\d+/.test(document.querySelector(".st-lv")?.textContent || "") && document.querySelector(".st-lv button.on small")?.textContent === String(n), IDX.count, { timeout: 8000 }).catch(() => {});
    ok((await A.page.locator(".st-lv button.on small").textContent()) === String(IDX.count), "「초등」 칸에 개념 수가 바로 뜬다");
    const chips = await A.page.locator(".st-chips .st-chip").allTextContents();
    ok(chips[0]?.startsWith("초1-1") && chips.some((t) => t.startsWith("초6-2")), `학기 칩 초1-1 … 초6-2 (${chips.length}개)`);
    const first = ELEM.find((c) => c.unitId === "e1-1" && c.order === 1) || ELEM[0];
    ok((await A.page.locator(".st-list .st-item b").first().textContent()) === first.title, `초1-1 첫 개념 「${first.title}」`);
    await A.ctx.close();

    // 2) 같은 기기에서 다시 열면 다시 넣지 않는다(판 기록) — 관리자가 일부러 지운 개념이 되살아나지 않게
    const inserts2 = [];
    const db2 = new Map([...db].filter(([k]) => k !== first.id));
    const B = await open(browser, base, { role: "admin", db: db2, inserts: inserts2, keepSeed: `${IDX.v}:${IDX.count}` });
    await B.page.goto(`${base}/walking#/study/concept`);
    await B.page.locator(".st-lv").waitFor({ timeout: 20000 });
    await sleep(1500);
    ok(inserts2.length === 0, "같은 판을 맞춘 기기에서는 다시 넣지 않는다");
    await B.ctx.close();

    // 3) 학생 — 넣지 않고, 「초등」 → 초3-1 → 개념 열기 → 위 막대에 「초3-1」
    const inserts3 = [];
    const S = await open(browser, base, { role: "student", db: new Map(db), inserts: inserts3 });
    await S.page.goto(`${base}/walking#/study/concept`);
    await S.page.locator(".st-lv").waitFor({ timeout: 20000 });
    await S.page.locator(".st-lv button", { hasText: "초등" }).click();
    await S.page.locator(".st-chip", { hasText: "초3-1" }).click();
    const c31 = ELEM.filter((c) => c.unitId === "e3-1").sort((a, b) => a.order - b.order);
    const names = await S.page.locator(".st-list .st-item b").allTextContents();
    ok(names.join("|") === c31.map((c) => c.title).join("|"), `초3-1 개념 ${c31.length}개 차례대로`);
    await S.page.locator(".st-list .st-item").first().click();
    await S.page.locator(".cv-title").waitFor({ timeout: 15000 });
    ok((await S.page.locator(".cv-title").textContent()) === c31[0].title, "개념 화면이 열린다");
    ok(/초3-1/.test(await S.page.locator(".fb").first().textContent()), "위 막대 학기 표시 「초3-1」");
    // 뒤로 → 학교급 · 학기 기억
    await S.page.evaluate(() => { location.hash = "#/study/concept"; });
    await S.page.locator(".st-lv").waitFor({ timeout: 10000 });
    await sleep(300);
    ok((await S.page.locator(".st-lv button.on").textContent()).startsWith("초등") && (await S.page.locator(".st-chip.on").textContent()).startsWith("초3-1"), "돌아오면 「초등 · 초3-1」 그대로");
    // 중등으로 갔다 와도 학교급마다 학기를 따로 기억
    await S.page.locator(".st-lv button", { hasText: "중등" }).click();
    ok((await S.page.locator(".st-chip.on").textContent()).startsWith("중1-1"), "중등은 중등 학기(중1-1)");
    await S.page.locator(".st-lv button", { hasText: "초등" }).click();
    ok((await S.page.locator(".st-chip.on").textContent()).startsWith("초3-1"), "다시 초등 — 초3-1 그대로");
    // 검색은 학교급과 상관없이
    await S.page.fill(".sv-search", c31[0].title.slice(0, 3));
    await sleep(200);
    ok(/초3-1/.test(await S.page.locator(".st-list").textContent()), "검색 결과에 학기 「초3-1」 표시");
    ok(inserts3.length === 0, "학생은 넣지 않는다");
    ok(!A.errors.length && !B.errors.length && !S.errors.length, "페이지 오류 없음 " + [...A.errors, ...B.errors, ...S.errors].slice(0, 2).join(" / "));
    await S.ctx.close();
  } finally {
    await browser.close();
    srv.close();
  }
  console.log(`\n${pass}/${pass + fail} 통과`);
  process.exit(fail ? 1 : 0);
})();
