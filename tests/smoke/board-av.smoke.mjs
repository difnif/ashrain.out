// 공부하기 › 시청각 학습 · 컨셉 문제 판서 모드 스모크
//   시청각 학습: 서브탭 → 범주 폴더 2개 → 항목 목록 → 하노이의 탑 · 도형 애니메이션 · 해설 액자 → 무대 안 목록은 같은 범주만 → 나가기
//   판서 모드: 학생에겐 단추 없음 · 관리자에겐 「바로 풀기」 옆 → 문제지 한 쪽 → 펜 · 터치 동시 필기 → 손 받침 잠금 → 쪽 넘기기 → 저장 · 되돌리기
//   node tests/smoke/board-av.smoke.mjs [--headed]   (준비: npx vite build)
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

const { srv, port } = await serve();
const browser = await chromium.launch({ headless: !process.argv.includes("--headed") });
try {
  // ── 시청각 학습 (학생) ──
  {
    const { page, errs, go, ctx } = await open(browser, "student", port, { width: 420, height: 860 });
    await go("#/study/av");
    await page.getByText("시청각 학습", { exact: true }).first().waitFor();
    await page.locator(".st-folder").first().waitFor();
    assert.equal(await page.locator(".st-folder").count(), 2);
    step("공부하기 서브탭에 시청각 학습 · 범주 폴더 2개(수학 호기심 · 문제 풀이 해설)");
    await page.screenshot({ path: path.join(SHOTS, "av-1-folders.png") });
    await page.locator(".st-folder").first().click();
    await page.waitForFunction(() => location.hash === "#/study/av/fun");
    assert.equal(await page.locator(".st-item").count(), avOfCat("fun").length);
    await page.screenshot({ path: path.join(SHOTS, "av-2-fun.png"), fullPage: true });
    step(`수학 호기심 ${avOfCat("fun").length}가지 목록`);
    await page.locator(".st-item", { hasText: "하노이의 탑" }).click();
    await page.waitForFunction(() => location.hash === "#/av/hanoi");
    await page.locator(".dsp-root").waitFor();
    await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(SHOTS, "av-3-hanoi.png") });
    step("하노이의 탑 — 관리자 확인 없이 무대가 돈다");
    await page.locator(".dsp-root").click({ position: { x: 200, y: 400 } });
    await page.locator('button[title="액자 목록"]').click();
    await page.locator(".dsp-fcard").first().waitFor();
    assert.equal(await page.locator(".dsp-fcard").count(), avOfCat("fun").length);
    assert.equal(await page.locator(".dsp-fcard", { hasText: "10단계 계산 해설" }).count(), 0);
    step("무대 안 목록은 같은 범주(수학 호기심)만");
    await page.locator(".dsp-fcard", { hasText: "도형 애니메이션" }).click();
    await page.waitForFunction(() => location.hash === "#/av/scenes-geo");
    await page.locator(".dsp-dots i").first().waitFor();
    const dots = await page.locator(".dsp-dots i").count();
    assert.ok(dots > 0);
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(SHOTS, "av-4-scenes.png") });
    step(`도형 애니메이션 — 도형 묶음 장면 ${dots}개가 돈다`);
    await page.locator(".dsp-root").click({ position: { x: 200, y: 400 } });
    await page.locator('.dsp-ctl button[title="나가기"]').click();
    await page.waitForFunction(() => location.hash === "#/study/av/fun");
    step("나가기 → 공부하기 › 시청각 학습 › 수학 호기심");
    await go("#/study/av/sol");
    await page.locator(".st-item").first().waitFor();
    assert.equal(await page.locator(".st-item").count(), avOfCat("sol").length);
    await page.locator(".st-item", { hasText: "경우의 수와 확률 100제" }).click();
    await page.locator(".dsp-root").waitFor();
    await page.waitForTimeout(900);
    await page.screenshot({ path: path.join(SHOTS, "av-5-cnt100.png") });
    step(`문제 풀이 해설 ${avOfCat("sol").length}가지 · 경우의 수와 확률 100제 해설 재생`);
    assert.deepEqual(errs, []);
    await go("#/sets/prob/01");
    await page.locator(".cs-go").first().waitFor();
    assert.equal(await page.getByText("✍ 판서 모드").count(), 0);
    step("학생 화면엔 판서 모드 단추가 없다");
    await ctx.close();
  }
  // ── 판서 모드 (관리자) ──
  {
    const { page, errs, go, ctx } = await open(browser, "admin", port);
    await go("#/sets/prob/01");
    await page.getByText("✍ 판서 모드").waitFor();
    await page.screenshot({ path: path.join(SHOTS, "bd-1-home.png") });
    step("관리자 — 「바로 풀기」 옆에 판서 모드");
    await page.getByText("✍ 판서 모드").click();
    await page.waitForFunction(() => location.hash.endsWith("/board"));
    await page.locator(".bd-pg", { hasText: "1 /" }).waitFor();
    await page.waitForTimeout(800);
    const pages = await page.locator(".bd-pg").textContent();
    const box = await page.evaluate(() => {
      const st = document.querySelector(".bd-stage"), host = document.querySelector(".bd-host");
      const pg = host.shadowRoot.querySelector(".pg.bd-cur"), sr = st.getBoundingClientRect(), r = pg.getBoundingClientRect();
      return { l: r.left - sr.left, t: r.top - sr.top, r: r.right - sr.left, b: r.bottom - sr.top, shown: [...host.shadowRoot.querySelectorAll(".pg")].filter((e) => getComputedStyle(e).display !== "none").length };
    });
    assert.equal(box.shown, 1);
    assert.ok(box.b - box.t > 700 && box.r - box.l > 500, JSON.stringify(box));
    assert.ok(await page.locator(".bd-zone.hint").count() === 1);
    step(`문제지 한 쪽이 화면 가득(${pages.trim()}) · 손 받침 안내`);
    await page.screenshot({ path: path.join(SHOTS, "bd-2-hint.png") });

    // 합성 포인터 — 펜(선생님)과 터치(학생)를 섞어 동시에
    const fire = (evs) => page.evaluate((evs) => {
      const st = document.querySelector(".bd-stage"), sr = st.getBoundingClientRect();
      for (const [type, kind, id, x, y, w] of evs) {
        st.dispatchEvent(new PointerEvent(type, { bubbles: true, cancelable: true, pointerId: id, pointerType: kind, clientX: sr.left + x, clientY: sr.top + y,
          width: w || 1, height: w || 1, buttons: type === "pointerup" ? 0 : 1, isPrimary: id === 1 }));
      }
    }, evs);
    const mid = (box.l + box.r) / 2, R = box.r;
    // 학생 손바닥을 오른쪽 단에 대고 있기 → 잠금
    await fire([["pointerdown", "touch", 20, R - 80, box.b - 160, 10]]);
    await page.waitForTimeout(450);
    await page.locator(".bd-zone.lock").waitFor();
    step("오른쪽 단에 손바닥 0.3초 → 그 단 잠금(옅은 음영)");
    // 펜과 터치를 번갈아 동시에
    const evs = [["pointerdown", "pen", 1, box.l + 60, box.t + 200], ["pointerdown", "touch", 2, box.l + 80, box.t + 520, 8]];
    for (let i = 1; i <= 24; i++) {
      evs.push(["pointermove", "pen", 1, box.l + 60 + i * 9, box.t + 200 + Math.sin(i / 3) * 14]);
      evs.push(["pointermove", "touch", 2, box.l + 80 + i * 8, box.t + 520 + Math.cos(i / 3) * 12, 8]);
    }
    await fire(evs.slice(0, 2));
    for (let i = 2; i < evs.length; i += 2) { await fire(evs.slice(i, i + 2)); await page.waitForTimeout(8); }
    await fire([["pointerup", "pen", 1, box.l + 280, box.t + 200], ["pointerup", "touch", 2, box.l + 272, box.t + 520]]);
    // 잠긴 단에서 시작한 터치는 버려진다
    await fire([["pointerdown", "touch", 3, mid + 80, box.t + 300, 8], ["pointermove", "touch", 3, mid + 140, box.t + 320, 8]]);
    await page.waitForTimeout(120);
    await fire([["pointermove", "touch", 3, mid + 200, box.t + 330, 8], ["pointerup", "touch", 3, mid + 200, box.t + 330, 8]]);
    await page.waitForTimeout(600);
    const saved = await page.evaluate(() => JSON.parse(localStorage.getItem("ash.cs.board.prob.01") || "null"));
    const st = saved?.pages?.["0"] || [];
    assert.equal(st.filter((s) => s.s === "pen").length, 1, JSON.stringify(st.map((s) => s.s)));
    assert.equal(st.filter((s) => s.s === "touch").length, 1);
    assert.ok(st.find((s) => s.s === "pen").c === "#d42a3c" && st.find((s) => s.s === "touch").c === "#1d5fd6");
    await page.screenshot({ path: path.join(SHOTS, "bd-3-both.png") });
    step("펜(빨강)과 터치(파랑) 동시 필기 · 잠긴 단에서 시작한 터치는 안 그림 · 저장");
    // 쪽 오른쪽 바깥으로 손바닥이 걸치면 해제
    await fire([["pointerup", "touch", 20, R - 80, box.b - 160, 10], ["pointerdown", "touch", 21, R + 40, box.t + 400, 10]]);
    await page.waitForTimeout(450);
    assert.equal(await page.locator(".bd-zone").count(), 0);
    await fire([["pointerup", "touch", 21, R + 40, box.t + 400, 10]]);
    step("쪽 밖 손 쪽에 0.3초 → 잠금 해제");
    // 학생 되돌리기
    await page.locator('button[title="학생 되돌리기"]').click();
    await page.waitForTimeout(500);
    const saved2 = await page.evaluate(() => JSON.parse(localStorage.getItem("ash.cs.board.prob.01") || "null"));
    assert.deepEqual((saved2.pages["0"] || []).map((s) => s.s), ["pen"]);
    step("학생 되돌리기는 학생 획만");
    await page.locator('button[title="다음 쪽"]').click();
    await page.locator(".bd-pg", { hasText: "2 /" }).waitFor();
    assert.equal(await page.locator(".bd-zone.hint").count(), 1);
    await page.locator('button[title="앞 쪽"]').click();
    await page.locator(".bd-pg", { hasText: "1 /" }).waitFor();
    step("쪽 넘기기 → 새 쪽은 손 받침 안내부터");
    await page.locator('button[title="설정"]').click();
    await page.getByText("판서 설정").waitFor();
    await page.locator(".bd-set .seg button", { hasText: "켬" }).click();
    await page.locator(".bd-set .seg button", { hasText: "왼손" }).click();
    await page.waitForTimeout(300);
    assert.equal(await page.locator(".bd-bar.R").count(), 1);
    await page.screenshot({ path: path.join(SHOTS, "bd-4-settings-left.png") });
    step("설정 — 왼손잡이면 도구 막대가 오른쪽 · 진단 표시");
    assert.deepEqual(errs, []);
    await ctx.close();
  }
  console.log(`\n${n}단계 통과`);
} finally {
  await browser.close();
  srv.close();
}
