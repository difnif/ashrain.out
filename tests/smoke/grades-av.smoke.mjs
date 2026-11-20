// 학년별 기본기 해설(초1 ~ 고3) 스모크 — 학생앱 › 시청각 학습 › 문제 풀이 해설 · 📄 문서 받기
//   목록: 초등 · 중등 · 고등 묶음 · 학년 꼬리표 → 초1 해설 재생 → 세트 바꾸기(B) → 번호 · 단계 목록
//   📄 문서: 문제지 · 해설지 · 빠른 정답 · OMR 고르기 → 확인 → 개별 다운 | 압축 다운
//     · PDF 가 아직 없으면(Storage 404) → 「인쇄 창으로 열기」 → 새 창에 같은 문서(코드 · 100문항 · 흑백 그림)
//     · PDF 가 있으면 → 압축 다운 = 「초1-10만들기.zip」 하나, 개별 다운 = 고른 수만큼 PDF
//   고3 해설도 연다(그림 · 수식이 가장 많은 학년).
//   node tests/smoke/grades-av.smoke.mjs [--headed]   (준비: npx vite build)
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { avOfCat } from "../../src/lib/av.js";
import { FRAMES } from "../../src/features/display/frames/index.js";

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
const FAKE_PDF = Buffer.from("%PDF-1.4\n1 0 obj << /Type /Catalog >> endobj\ntrailer << /Root 1 0 R >>\n%%EOF\n");

let pdfMode = "none";       // none: Storage 에 아직 없음(404) · ok: 있음
async function open(browser, role, port, viewport = { width: 1280, height: 800 }) {
  const ctx = await browser.newContext({ viewport, hasTouch: true, acceptDownloads: true });
  const page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", (e) => errs.push(String(e)));
  await ctx.route("https://placeholder.supabase.co/**", (route) => {
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
  await ctx.route("https://*.supabase.co/storage/v1/object/public/concept-sets/av/**", (route) => {
    if (pdfMode === "ok") return route.fulfill({ status: 200, contentType: "application/pdf", headers: { "access-control-allow-origin": "*" }, body: FAKE_PDF });
    return route.fulfill({ status: 400, contentType: "application/json", headers: { "access-control-allow-origin": "*" }, body: '{"statusCode":"404","error":"not_found"}' });
  });
  await ctx.route("https://cdn.jsdelivr.net/**", (route) => route.fulfill({ status: 200, contentType: "text/css", body: "" }));
  await ctx.addInitScript(([k, s]) => { localStorage.setItem(k, JSON.stringify(s)); localStorage.setItem("ashrain-theme", "light"); }, ["sb-placeholder-auth-token", SESSION]);
  return { ctx, page, errs, go: (h) => page.goto(`http://127.0.0.1:${port}/${h}`) };
}
let n = 0;
const step = (s) => console.log(`✓ ${++n}. ${s}`);
const wake = (page) => page.locator(".dsp-root").click({ position: { x: 300, y: 420 } });

const { srv, port } = await serve();
// 컨테이너에 로캘이 없으면 Chromium 이 한글 파일 이름을 「download」로 바꾼다 — 실제 기기처럼 UTF-8 로
const browser = await chromium.launch({ headless: !process.argv.includes("--headed"), env: { ...process.env, LANG: "C.UTF-8", LC_ALL: "C.UTF-8" } });
try {
  const { page, errs, go, ctx } = await open(browser, "student", port, { width: 1280, height: 760 });
  await go("#/study/av/sol");
  await page.locator(".st-item").first().waitFor();
  const sol = avOfCat("sol");
  assert.equal(await page.locator(".st-item").count(), sol.length);
  for (const lv of ["초등", "중등", "고등"]) assert.equal(await page.locator(".st-sec", { hasText: lv }).count(), 1, lv);
  assert.equal(await page.locator(".st-item .tag", { hasText: "초1" }).count(), 1);
  await page.screenshot({ path: path.join(SHOTS, "gr-1-list.png"), fullPage: true });
  step(`문제 풀이 해설 ${sol.length}가지 — 초등 · 중등 · 고등으로 묶이고 학년 꼬리표`);

  await page.locator(".st-item", { hasText: "초1 ·" }).click();
  await page.waitForFunction(() => location.hash === "#/av/e1");
  await page.locator(".dsp-root").waitFor();
  await page.locator(".dsp-svg").first().waitFor();
  await page.waitForTimeout(2600);
  await page.screenshot({ path: path.join(SHOTS, "gr-2-e1.png") });
  step("초1 해설 — 문항을 늦게 들여와 첫 장면이 돈다");

  await wake(page);
  await page.locator('button[title^="번호 · 단계 목록"]').click();
  await page.locator(".dsp-list").first().waitFor();
  await page.screenshot({ path: path.join(SHOTS, "gr-3-list.png") });
  await page.keyboard.press("Escape");
  step("번호 · 단계 목록이 열린다");

  // 📄 문서 — PDF 가 아직 없을 때
  await wake(page);
  await page.locator('button[aria-label="문서"]').click();
  await page.locator(".gdoc-pop").waitFor();
  for (const w of ["문제지", "해설지", "빠른 정답", "OMR"]) assert.ok(await page.locator(".gdoc-pop", { hasText: w }).count(), w);
  await page.screenshot({ path: path.join(SHOTS, "gr-4-docs.png") });
  const boxes = page.locator('.gdoc-pop [role="checkbox"]');
  const nb = await boxes.count();
  assert.equal(nb, 4);
  const setBox = async (i, on) => { if ((await boxes.nth(i).getAttribute("aria-checked")) !== String(on)) await boxes.nth(i).click(); };
  for (let i = 0; i < nb; i++) await setBox(i, true);
  await page.locator(".gdoc-pop button", { hasText: "확인" }).click();
  await page.locator(".gdoc-pop button", { hasText: "개별 다운" }).waitFor();
  assert.ok(await page.locator(".gdoc-pop button", { hasText: "압축 다운" }).count());
  step("📄 문서 → 네 가지 고르기 → 확인 → 개별 다운 | 압축 다운");
  await page.locator(".gdoc-pop button", { hasText: "개별 다운" }).click();
  await page.locator(".gdoc-pop button", { hasText: "인쇄 창으로 열기" }).waitFor();
  const [win] = await Promise.all([ctx.waitForEvent("page"), page.locator(".gdoc-pop button", { hasText: "인쇄 창으로 열기" }).click()]);
  await win.waitForFunction(() => document.querySelectorAll(".q").length >= 100, null, { timeout: 30000 });
  const doc = await win.evaluate(() => ({ q: document.querySelectorAll(".q").length, s: document.querySelectorAll(".s").length, ak: document.querySelectorAll(".ak .no").length,
    omr: document.querySelectorAll(".cs-omr svg, .omr-pg").length, code: /코드 [0-9A-Z]{3}-[0-9A-Z]{3}/.test(document.body.innerText), svg: document.querySelectorAll(".sf svg").length, text: document.body.innerText.slice(0, 200) }));
  assert.equal(doc.q, 100, "문제지 100칸");
  assert.equal(doc.s, 100, "해설 100칸");
  assert.equal(doc.ak, 100, "빠른 정답 100칸");
  assert.ok(doc.omr >= 1, "OMR 카드");
  assert.ok(doc.code, "코드");
  assert.ok(doc.svg > 50, `해설 그림 ${doc.svg}`);
  await win.screenshot({ path: path.join(SHOTS, "gr-5-print.png") });
  await win.close();
  step(`PDF 가 없으면 → 인쇄 창: 문제지 · 해설지(그림 ${doc.svg}장) · 빠른 정답 · OMR, 코드가 찍힌다`);

  // 📄 문서 — PDF 가 있을 때
  pdfMode = "ok";
  await page.locator(".gdoc-pop button", { hasText: "다시 고르기" }).click();
  await page.locator(".gdoc-pop button", { hasText: "확인" }).click();
  await page.locator(".gdoc-pop button", { hasText: "압축 다운" }).waitFor();
  const [zip] = await Promise.all([page.waitForEvent("download"), page.locator(".gdoc-pop button", { hasText: "압축 다운" }).click()]);
  assert.equal(zip.suggestedFilename(), "초1-10만들기.zip");
  const zp = path.join(SHOTS, "gr-docs.zip");
  await zip.saveAs(zp);
  const zb = fs.readFileSync(zp);
  assert.equal(zb.readUInt32LE(0), 0x04034b50, "ZIP 머리");
  for (const nm of ["문제지", "해설지", "빠른정답", "OMR"]) assert.ok(zb.includes(Buffer.from(`초1-10만들기-${nm}.pdf`)), nm);
  step("PDF 가 있으면 → 압축 다운: 「초1-10만들기.zip」 안에 네 문서(한글 이름)");
  await page.locator(".gdoc-pop button", { hasText: "다른 문서 받기" }).click();
  await setBox(2, false);
  await setBox(3, false);
  await page.locator(".gdoc-pop button", { hasText: "확인" }).click();
  await page.locator(".gdoc-pop button", { hasText: "개별 다운" }).waitFor();
  const got = [];
  page.on("download", (d) => got.push(d.suggestedFilename()));
  await page.locator(".gdoc-pop button", { hasText: "개별 다운" }).click();
  await page.waitForTimeout(2500);
  assert.deepEqual(got.sort(), ["초1-10만들기-문제지.pdf", "초1-10만들기-해설지.pdf"].sort());
  step("개별 다운: 고른 두 문서가 하나씩(초1-10만들기-문제지.pdf · 해설지.pdf)");
  await page.keyboard.press("Escape");

  await go("#/av/h3");
  await page.locator(".dsp-svg").first().waitFor();
  await page.waitForTimeout(2600);
  await page.screenshot({ path: path.join(SHOTS, "gr-6-h3.png") });
  step("고3 해설도 돈다");
  assert.deepEqual(errs, []);
  await ctx.close();

  // ── 교실 모니터(관리자): 액자 목록에 학년별 해설 열둘이 목록 그림과 함께 ──
  {
    const A = await open(browser, "admin", port, { width: 1600, height: 900 });
    await A.go("#/admin/display");
    await A.page.locator(".dsp-root").waitFor();
    await A.page.waitForTimeout(800);
    await A.page.locator(".dsp-root").click({ position: { x: 400, y: 450 } });
    await A.page.locator('button[aria-label="액자"]').click();
    await A.page.locator(".dsp-fcard").first().waitFor();
    const cards = await A.page.locator(".dsp-fcard").count();
    assert.equal(cards, FRAMES.length, `액자 ${cards}개 ≠ ${FRAMES.length}`);
    const g = A.page.locator(".dsp-fcard", { hasText: "고2 · 지수와 로그 · 미분" });
    assert.equal(await g.count(), 1);
    assert.ok((await g.locator("svg").innerHTML()).length > 1500, "목록 그림");
    await A.page.screenshot({ path: path.join(SHOTS, "gr-7-gallery.png") });
    await g.click();
    await A.page.waitForTimeout(2600);
    await A.page.screenshot({ path: path.join(SHOTS, "gr-8-monitor-h2.png") });
    assert.deepEqual(A.errs, []);
    step(`교실 모니터 — 액자 목록 ${cards}개(학년별 해설 열둘 · 목록 그림) → 고2 해설이 돈다`);
    await A.ctx.close();
  }
} finally {
  await browser.close();
  srv.close();
}
console.log(`\n스모크 ${n}단계 통과`);
