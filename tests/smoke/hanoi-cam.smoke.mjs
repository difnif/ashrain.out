// 스모크: 하노이의 탑 — 로봇 모드(입체 · 세트 5개) 카메라. npx vite build 뒤 node tests/smoke/hanoi-cam.smoke.mjs
//   오른쪽 카메라 단추 → 원샷 ① → ⑤(로봇 하나가 옮기는 탑을 정면에서) → 전체 · C 키
//   두 손가락(CDP 터치): 벌리면 가까이(전체 → 손가락 가운데 로봇의 투샷 → 원샷) · 옆으로 밀면 옆 로봇 · 모으면 멀리(→ 투샷 → 전체)
//   휠: 위로 가까이 · 아래로 멀리 · 가로로 옆 로봇. 샷은 저장(새로고침해도 그 샷) · 세트를 줄이면 전체로.
//   헤드리스 크롬(SwiftShader)은 느리다 — 품질 「낮음」 고정, 한 장마다 몇 프레임 기다린다. 샷 화면은 shots/hn-*.png
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); }
catch { ({ chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright")); }

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "../..");
const DIST = path.join(ROOT, "dist");
const SHOTS = process.env.SMOKE_SHOTS || path.join(HERE, "shots");
fs.mkdirSync(SHOTS, { recursive: true });
const MIME = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2" };
function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, "http://x");
      let f = path.join(DIST, decodeURIComponent(u.pathname));
      if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f = path.join(DIST, "index.html");
      res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(0, "127.0.0.1", () => resolve({ srv, port: srv.address().port }));
  });
}
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const USER = { id: "00000000-0000-4000-8000-000000000001", aud: "authenticated", role: "authenticated", email: "smoke@example.com", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: {}, factors: [], created_at: "2026-01-01T00:00:00Z" };
const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], app_metadata: USER.app_metadata, user_metadata: {}, session_id: "s1" })}.sig`;
const SESSION = { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r1", user: USER };
const profile = { role: "student", member_code: "SMOKE", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "2011-03-01", settings: {} };

let n = 0;
const step = (s) => console.log(`✓ ${++n}. ${s}`);
const { srv, port } = await serve();
const browser = await chromium.launch({ headless: !process.argv.includes("--headed"), args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
try {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, hasTouch: true });
  const page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", (e) => errs.push(String(e)));
  await page.route("https://placeholder.supabase.co/**", (route) => {
    const req = route.request(), u = new URL(req.url()), accept = req.headers()["accept"] || "";
    const json = (o, h = {}) => route.fulfill({ status: 200, contentType: "application/json", headers: h, body: JSON.stringify(o) });
    if (u.pathname.startsWith("/auth/v1/user")) return json(USER);
    if (u.pathname.startsWith("/auth/v1/token")) return json(SESSION);
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0], obj = accept.includes("pgrst.object");
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0", "access-control-expose-headers": "content-range" }, body: "" });
      if (table === "profiles") return json(obj ? { id: USER.id, ...profile } : [{ id: USER.id, ...profile }]);
      return json(obj ? null : [], { "content-range": "0-0/0" });
    }
    return json({});
  });
  await ctx.addInitScript(([k, s]) => {
    if (sessionStorage.getItem("smoke-init")) return;            // 처음 한 번만(새로고침 뒤에는 저장된 샷을 본다)
    sessionStorage.setItem("smoke-init", "1");
    localStorage.setItem(k, JSON.stringify(s));
    localStorage.setItem("ashrain-theme", "dark");
    localStorage.setItem("ash.display.hanoi3d.q", "low");
    localStorage.setItem("ash.display.hanoi", JSON.stringify({ n: 6, pegs: 3, sets: 5, sp: "x1", view: "3d", t0: Date.now() - 4000, held: null }));
  }, ["sb-placeholder-auth-token", SESSION]);

  const shotNow = () => page.evaluate(() => (window.__hanoi3d ? window.__hanoi3d.shot : "none"));
  const frames = async (k = 3) => {                                // 엔진이 k 장 더 그릴 때까지
    const c0 = await page.evaluate(() => window.__hanoi3d?.stats?.calls ?? 0);
    await page.waitForTimeout(400);
    for (let i = 0; i < k; i++) await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
    return c0;
  };
  const shoot = async (name) => { await frames(4); await page.waitForTimeout(1200); await page.screenshot({ path: path.join(SHOTS, name) }); };
  const label = async () => (await page.locator(".hn-cam-lab").textContent()).trim();

  await page.goto(`http://127.0.0.1:${port}/#/av/hanoi`);
  await page.locator(".dsp-root").waitFor();
  await page.waitForFunction(() => !!window.__hanoi3d, null, { timeout: 60000 });
  await page.locator(".hn-cam-btn").waitFor({ timeout: 90000 });
  await page.locator(".hn-touch").waitFor();
  assert.equal(await page.locator(".hn-touch").evaluate((el) => getComputedStyle(el).touchAction), "none", "두 손가락은 브라우저 확대 대신 카메라로");
  assert.equal(await shotNow(), null);
  await shoot("hn-0-all.png");
  step("로봇 모드(입체 · 세트 5) — 오른쪽 가운데 카메라 단추 · 두 손가락 막(touch-action: none) · 처음은 전체");

  // ── 카메라 단추: ① → ⑤ → 전체 ──
  const names = ["산업용 팔", "로봇 개", "휴머노이드", "두 바퀴", "드론"];
  for (let i = 0; i < 5; i++) {
    await page.locator(".hn-cam-btn").click();
    assert.deepEqual(await shotNow(), { n: 1, i }, `원샷 ${i + 1}`);
    assert.ok((await label()).includes(names[i]), await label());
    assert.ok((await page.locator(".dsp-tags").textContent()).includes(`원샷`));
    await shoot(`hn-1-one-${i + 1}.png`);
  }
  const hid = await page.evaluate(() => window.__hanoi3d.stats.hide);
  assert.ok(hid.includes(3), `⑤ 원샷 — 앞을 가리는 ④ 세트는 그 샷 동안 뺀다 ${JSON.stringify(hid)}`);
  await page.locator(".hn-cam-btn").click();
  assert.equal(await shotNow(), null);
  assert.deepEqual(await page.evaluate(() => window.__hanoi3d.stats.hide), [], "전체로 오면 다시 다섯 대");
  step(`카메라 단추: 원샷 ① 산업용 팔 → ② 로봇 개 → ③ 휴머노이드 → ④ 두 바퀴 → ⑤ 드론(겹치는 세트 ${JSON.stringify(hid)} 는 뺌) → 전체`);

  // ── 두 손가락(CDP 터치) ──
  const cdp = await ctx.newCDPSession(page);
  const touch = async (type, pts) => cdp.send("Input.dispatchTouchEvent", { type, touchPoints: pts.map(([x, y], id) => ({ x, y, id, radiusX: 4, radiusY: 4, force: 1 })) });
  const gesture = async (from, to, steps = 8) => {
    await touch("touchStart", from);
    for (let s = 1; s <= steps; s++) {
      const k = s / steps;
      await touch("touchMove", from.map(([x, y], j) => [x + (to[j][0] - x) * k, y + (to[j][1] - y) * k]));
      await page.waitForTimeout(30);
    }
    await touch("touchEnd", []);
    await page.waitForTimeout(250);
  };
  const spread = (cx, cy, a, b) => gesture([[cx - a, cy], [cx + a, cy]], [[cx - b, cy], [cx + b, cy]]);
  // 전체에서 오른쪽 로봇들 위를 벌리면 — 그쪽 투샷
  for (const [x, y] of [[1000, 380], [1180, 500], [640, 400]]) {
    assert.equal(await page.evaluate(([px, py]) => document.elementFromPoint(px, py)?.className, [x, y]), "hn-touch", `${x},${y} 는 두 손가락 막`);
  }
  const near = await page.evaluate(() => window.__hanoi3d.pick(1000, 380));
  const k0 = near.indexOf(Math.min(...near));
  await spread(1000, 380, 60, 140);
  const s1 = await shotNow();
  assert.equal(s1?.n, 2, JSON.stringify(s1));
  assert.ok(s1.i === k0 || s1.i + 1 === k0, `손가락 가운데 로봇 ${k0} 이 든 투샷: ${JSON.stringify(s1)}`);
  await shoot(`hn-2-two-${s1.i + 1}${s1.i + 2}.png`);
  await spread(640, 400, 60, 140);
  const s2 = await shotNow();
  assert.equal(s2?.n, 1);
  assert.ok(s2.i === s1.i || s2.i === s1.i + 1);
  step(`두 손가락 벌리기: 전체 → 투샷 ${s1.i + 1}·${s1.i + 2}(손가락 가운데 로봇) → 원샷 ${s2.i + 1}`);
  // 옆으로 밀기 — 왼쪽으로 밀면 다음(오른쪽) 로봇
  const dir = s2.i < 4 ? 1 : -1;
  await gesture([[700, 300], [700, 460]], [[700 - dir * 260, 300], [700 - dir * 260, 460]]);
  assert.deepEqual((await shotNow()).i, s2.i + dir);
  await shoot(`hn-3-one-swipe-${s2.i + dir + 1}.png`);
  // 모으기 — 원샷 → 투샷 → 전체
  await spread(640, 400, 160, 60);
  assert.equal((await shotNow())?.n, 2);
  await spread(640, 400, 160, 60);
  assert.equal(await shotNow(), null);
  step(`두 손가락 옆으로: 원샷 ${s2.i + 1} → ${s2.i + dir + 1} · 모으기: 원샷 → 투샷 → 전체`);

  // ── 휠 ──
  await page.mouse.move(400, 420);
  await page.mouse.wheel(0, -120);
  await page.waitForTimeout(600);
  assert.equal((await shotNow())?.n, 2, "휠 위 → 투샷");
  await page.mouse.wheel(150, 0);
  await page.waitForTimeout(600);
  const s3 = await shotNow();
  assert.equal(s3?.n, 2);
  await shoot(`hn-4-two-wheel-${s3.i + 1}${s3.i + 2}.png`);
  await page.mouse.wheel(0, 120);
  await page.waitForTimeout(600);
  assert.equal(await shotNow(), null, "휠 아래 → 전체");
  step("휠: 위로 가까이(투샷) · 가로로 옆 짝 · 아래로 멀리(전체)");

  // ── 투샷 넷 모두 그려 보기 · C 키 · 저장 ──
  for (let i = 0; i < 4; i++) {
    await page.evaluate((k) => window.__hanoi3d.setShot({ n: 2, i: k }, "cut"), i);
    await shoot(`hn-5-two-${i + 1}${i + 2}.png`);
  }
  await page.evaluate(() => window.__hanoi3d.setShot(null, "cut"));
  await page.keyboard.press("c");
  await page.keyboard.press("c");
  assert.deepEqual(await shotNow(), { n: 1, i: 1 });
  await page.waitForTimeout(500);
  await page.reload();
  await page.waitForFunction(() => !!window.__hanoi3d, null, { timeout: 60000 });
  await page.locator(".hn-cam-btn").waitFor({ timeout: 90000 });
  assert.deepEqual(await shotNow(), { n: 1, i: 1 }, "새로고침해도 그 샷");
  step("투샷 넷을 그려 봄 · C 키 두 번 → 원샷 ② · 새로고침해도 그 샷");
  await page.keyboard.press("3");
  await page.waitForTimeout(400);
  assert.equal(await page.locator(".hn-cam-btn").count(), 0, "세트 3 — 카메라 단추 없음");
  assert.equal(await shotNow(), null);
  await page.keyboard.press("5");
  await page.waitForTimeout(400);
  assert.equal(await shotNow(), null, "다시 5 — 전체부터");
  step("세트를 줄이면 카메라 단추가 사라지고 전체로 · 다시 5세트면 전체부터");
  assert.deepEqual(errs, []);
  console.log(`\n스모크 ${n}단계 통과`);
} finally {
  await browser.close();
  srv.close();
}
