// 공부하기 › 시청각 학습 › 수학 호기심 — 수학멍 액자 일곱 스모크
//   목록에 일곱이 다 있는지 → 하나씩 열어(#/av/<key>) 자료를 늦게 들여온 뒤 그림이 그려지는지(NaN · 「불러오는 중」 없음)
//   → 조작 막대 · 중등 전환 → 무대 안 목록. 화면은 tests/smoke/shots/curio-*.png
//   node tests/smoke/curio.smoke.mjs [--headed]   (준비: npx vite build)
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { avOfCat } from "../../src/lib/av.js";

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
const profile = (role) => ({ role, member_code: "SMOKE", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "2011-03-01", settings: {} });

async function open(browser, role, port, viewport = { width: 1280, height: 800 }) {
  const ctx = await browser.newContext({ viewport, hasTouch: true });
  const page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", (e) => errs.push(String(e)));
  await page.route("https://placeholder.supabase.co/**", (route) => {
    const req = route.request(); const u = new URL(req.url()); const accept = req.headers()["accept"] || "";
    const json = (o, h = {}) => route.fulfill({ status: 200, contentType: "application/json", headers: h, body: JSON.stringify(o) });
    if (u.pathname.startsWith("/auth/v1/user")) return json(USER);
    if (u.pathname.startsWith("/auth/v1/token")) return json(SESSION);
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0], obj = accept.includes("pgrst.object");
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0", "access-control-expose-headers": "content-range" }, body: "" });
      if (table === "profiles") return json(obj ? { id: USER.id, ...profile(role) } : [{ id: USER.id, ...profile(role) }]);
      return json(obj ? null : [], { "content-range": "0-0/0" });
    }
    return json({});
  });
  await ctx.addInitScript(([k, s]) => { localStorage.setItem(k, JSON.stringify(s)); localStorage.setItem("ashrain-theme", "light"); }, ["sb-placeholder-auth-token", SESSION]);
  return { ctx, page, errs, go: (h) => page.goto(`http://127.0.0.1:${port}/${h}`) };
}
let n = 0;
const step = (s) => console.log(`✓ ${++n}. ${s}`);
const KEYS = ["soccerfn", "hoopfn", "batfn", "pouch", "lexi", "lineup", "crowd"];

const { srv, port } = await serve();
const browser = await chromium.launch({ headless: !process.argv.includes("--headed") });
try {
  const { page, errs, go } = await open(browser, "student", port, { width: 1280, height: 800 });
  // ── 목록: 수학 호기심에 일곱이 다 있다 ──
  await go("#/study/av/fun");
  await page.locator(".st-item").first().waitFor();
  const fun = avOfCat("fun");
  assert.equal(await page.locator(".st-item").count(), fun.length);
  for (const key of KEYS) {
    const it = fun.find((x) => x.key === key);
    assert.ok(it, `수학 호기심에 ${key} 없음`);
    await page.getByText(it.title, { exact: true }).first().waitFor();
  }
  await page.screenshot({ path: path.join(SHOTS, "curio-list.png"), fullPage: true });
  step(`수학 호기심 목록 ${fun.length}가지 — 일곱 모두 있음`);
  // ── 하나씩 열기 ──
  for (const key of KEYS) {
    await go(`#/av/${key}`);
    await page.locator(".dsp-root").waitFor();
    await page.waitForFunction(() => {
      const s = document.querySelector(".dsp-svg");
      return s && s.querySelectorAll("*").length > 60 && !s.textContent.includes("불러오는 중");
    }, null, { timeout: 15000 });
    await page.waitForTimeout(3500);
    const st = await page.evaluate(() => { const s = document.querySelector(".dsp-svg"); return { nodes: s.querySelectorAll("*").length, bad: /NaN|undefined|Infinity/.test(s.innerHTML) }; });
    assert.ok(!st.bad, `${key}: 그림에 NaN · undefined`);
    await page.mouse.move(640, 420);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(SHOTS, `curio-${key}.png`) });
    step(`${key}: SVG 요소 ${st.nodes}`);
  }
  // ── 중등으로 바꿔도 이어진다 ──
  await page.getByRole("radio", { name: "중등" }).click();
  await page.waitForTimeout(1500);
  assert.ok(!(await page.evaluate(() => /NaN|undefined/.test(document.querySelector(".dsp-svg").innerHTML))));
  await page.screenshot({ path: path.join(SHOTS, "curio-crowd-m.png") });
  step("중등 전환");
  // ── 무대 안 목록 = 같은 범주 ──
  await page.locator(".dsp-root").click({ position: { x: 300, y: 400 } });
  await page.locator('button[title="액자 목록"]').click();
  await page.locator(".dsp-fcard").first().waitFor();
  assert.equal(await page.locator(".dsp-fcard").count(), fun.length);
  step(`무대 안 목록 ${fun.length}가지`);
  assert.deepEqual(errs, []);
  step("페이지 오류 없음");
} finally { await browser.close(); srv.close(); }
