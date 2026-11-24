// 공부하기 › 시청각 학습 · 컨셉 문제 강사 모드(문제지 그대로 + 필기 도구 창) 스모크
//   시청각 학습: 서브탭 → 범주 폴더 2개 → 항목 목록 → 하노이의 탑 · 도형 애니메이션 · 해설 액자 → 무대 안 목록은 같은 범주만 → 나가기
//   강사 모드: 학생에겐 단추 · 토글 없음 · 관리자에겐 「바로 풀기」 옆 → 문제지 그대로 화면 + 도구 창 → 펜 · 터치 동시 필기 → 손 받침 잠금 · 해제 →
//             두 손가락 확대 → 되돌리기 → 학생 모드(도구 창 나감 · 답 시트) ↔ 강사 모드 → 손가락 넘기기 → 왼손잡이 배치
//   node tests/smoke/board-av.smoke.mjs [--headed] [--only av|board]   (준비: npx vite build)
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
const ONLY = (process.argv.find((a, i, all) => all[i - 1] === "--only") || "").trim();
const want = (part) => !ONLY || ONLY === part;

const { srv, port } = await serve();
const browser = await chromium.launch({ headless: !process.argv.includes("--headed") });
try {
  // ── 시청각 학습 (학생) ──
  if (want("av")) {
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
    assert.equal(await page.getByText("✍ 강사 모드").count(), 0);
    step("학생 화면엔 강사 모드 단추가 없다");
    await ctx.close();
  }
  // ── 강사 모드 (관리자) — 문제지 그대로 화면 위 학생 | 강사 토글 ──
  if (want("board")) {
    const { page, errs, go, ctx } = await open(browser, "admin", port);
    await go("#/sets/prob/01");
    await page.getByText("✍ 강사 모드").waitFor();
    step("관리자 — 「바로 풀기」 옆에 강사 모드");
    await page.getByText("✍ 강사 모드").click();
    await page.waitForFunction(() => location.hash.endsWith("/board"));
    await page.locator(".pb-panel.in").waitFor();
    await page.locator(".pb-touch").waitFor();
    await page.waitForTimeout(900);
    const geo = () => page.evaluate(() => {
      const host = document.querySelector(".cs-paperhost"), pg = host.shadowRoot.querySelector(".pg"), r = pg.getBoundingClientRect();
      const t = document.querySelector(".pb-touch")?.getBoundingClientRect() || { top: 0 }, pn = document.querySelector(".pb-panel").getBoundingClientRect();
      return { l: r.left, r: r.right, t: r.top, w: r.width, W: innerWidth, H: innerHeight, top: t.top, panelR: pn.right, panelL: pn.left, y: scrollY,
        bar: getComputedStyle(document.querySelector(".cs-pbar2")).transform, zl: document.querySelector('.pb-panel button[title="폭 맞춤"]')?.textContent || "" };
    });
    let g = await geo();
    assert.ok(g.l >= 84 && g.l <= 92 && Math.abs(g.w - (g.W - 84 - 44 - 8)) < 3, JSON.stringify(g));
    assert.ok(g.bar !== "none" && g.panelL >= 0 && g.panelR <= 90, JSON.stringify(g));
    assert.equal(await page.locator(".pb-zone.hint").count(), 1);
    await page.screenshot({ path: path.join(SHOTS, "bd-1-teacher.png") });
    step(`강사 모드 — 같은 폭 맞춤 화면(쪽 너비 ${Math.round(g.w)}px), 도구 창이 왼쪽에서 들어오고 풀기 막대는 내려감 · 손 받침 안내`);

    // 합성 포인터 — 화면(뷰포트) 좌표
    const fire = (evs) => page.evaluate((evs) => {
      const st = document.querySelector(".pb-touch");
      for (const [type, kind, id, x, y, w] of evs) {
        st.dispatchEvent(new PointerEvent(type, { bubbles: true, cancelable: true, pointerId: id, pointerType: kind, clientX: x, clientY: y,
          width: w || 1, height: w || 1, buttons: type === "pointerup" ? 0 : 1, isPrimary: id === 1 }));
      }
    }, evs);
    const L = 84, R = g.W - 44, T = g.top, mid = (L + R) / 2;
    await fire([["pointerdown", "touch", 20, R - 90, g.H - 160, 10]]);
    await page.waitForTimeout(450);
    await page.locator(".pb-zone.lock").waitFor();
    step("오른쪽 단에 손바닥 0.3초 → 그 단 잠금(옅은 음영)");
    const evs = [["pointerdown", "pen", 1, L + 60, T + 200], ["pointerdown", "touch", 2, L + 80, T + 460, 8]];
    for (let i = 1; i <= 24; i++) {
      evs.push(["pointermove", "pen", 1, L + 60 + i * 9, T + 200 + Math.sin(i / 3) * 14]);
      evs.push(["pointermove", "touch", 2, L + 80 + i * 8, T + 460 + Math.cos(i / 3) * 12, 8]);
    }
    await fire(evs.slice(0, 2));
    for (let i = 2; i < evs.length; i += 2) { await fire(evs.slice(i, i + 2)); await page.waitForTimeout(8); }
    await fire([["pointerup", "pen", 1, L + 280, T + 200], ["pointerup", "touch", 2, L + 272, T + 460]]);
    await fire([["pointerdown", "touch", 3, mid + 80, T + 300, 8], ["pointermove", "touch", 3, mid + 140, T + 320, 8]]);
    await page.waitForTimeout(260);
    await fire([["pointermove", "touch", 3, mid + 200, T + 330, 8], ["pointerup", "touch", 3, mid + 200, T + 330, 8]]);
    await page.waitForTimeout(600);
    const saved = () => page.evaluate(() => JSON.parse(localStorage.getItem("ash.cs.board.prob.01") || "null"));
    let st = (await saved())?.pages?.["0"] || [];
    assert.equal(st.filter((s) => s.s === "pen").length, 1, JSON.stringify(st.map((s) => s.s)));
    assert.equal(st.filter((s) => s.s === "touch").length, 1);
    assert.ok(st.find((s) => s.s === "pen").c === "#d42a3c" && st.find((s) => s.s === "touch").c === "#1d5fd6");
    await page.screenshot({ path: path.join(SHOTS, "bd-2-both.png") });
    step("펜(빨강)과 터치(파랑) 동시 필기 · 잠긴 단에서 시작한 터치는 안 그림 · 저장");
    await fire([["pointerup", "touch", 20, R - 90, g.H - 160, 10], ["pointerdown", "touch", 21, R + 20, T + 400, 10]]);
    await page.waitForTimeout(450);
    assert.equal(await page.locator(".pb-zone").count(), 0);
    await fire([["pointerup", "touch", 21, R + 20, T + 400, 10]]);
    step("손 받침 띠(쪽 밖 손 쪽)에 0.3초 → 잠금 해제");

    // 두 손가락 확대 — 필기는 안 생기고 확대가 확정된다(가운데 아래 내용은 제자리)
    const before = await geo();
    const anchor = await page.evaluate(([x, y]) => {
      const pg = document.querySelector(".cs-paperhost").shadowRoot.querySelector(".pg").getBoundingClientRect();
      return { u: (x - pg.left) / pg.width, v: (y - pg.top) / pg.width };
    }, [mid, T + 300]);
    await fire([["pointerdown", "touch", 30, mid - 100, T + 300, 8]]);
    await page.waitForTimeout(40);
    await fire([["pointerdown", "touch", 31, mid + 100, T + 300, 8]]);
    for (let i = 1; i <= 10; i++) { await fire([["pointermove", "touch", 30, mid - 100 - i * 10, T + 300, 8], ["pointermove", "touch", 31, mid + 100 + i * 10, T + 300, 8]]); await page.waitForTimeout(16); }
    await fire([["pointerup", "touch", 30, mid - 200, T + 300, 8], ["pointerup", "touch", 31, mid + 200, T + 300, 8]]);
    await page.waitForTimeout(400);
    g = await geo();
    assert.ok(Math.abs(g.w / before.w - 2) < 0.02, `${before.w} → ${g.w}`);
    assert.equal(g.zl.trim(), "200%");
    const after = await page.evaluate(([x, y, u, v]) => {
      const pg = document.querySelector(".cs-paperhost").shadowRoot.querySelector(".pg").getBoundingClientRect();
      return { x: pg.left + u * pg.width, y: pg.top + v * pg.width, x0: x, y0: y };
    }, [mid, T + 300, anchor.u, anchor.v]);
    assert.ok(Math.abs(after.x - after.x0) < 4 && Math.abs(after.y - after.y0) < 4, JSON.stringify(after));
    st = (await saved())?.pages?.["0"] || [];
    assert.equal(st.length, 2);
    await page.screenshot({ path: path.join(SHOTS, "bd-3-pinch.png") });
    step("두 손가락으로 벌리면 2배 확대(손가락 가운데 아래 내용은 제자리) · 필기는 안 생김");
    await page.locator('.pb-panel button[title="폭 맞춤"]').click();
    await page.waitForTimeout(300);
    g = await geo();
    assert.ok(Math.abs(g.w - (g.W - 84 - 44 - 8)) < 3);
    await page.locator('button[title="학생 되돌리기"]').click();
    await page.waitForTimeout(500);
    assert.deepEqual(((await saved()).pages["0"] || []).map((s) => s.s), ["pen"]);
    step("폭 맞춤으로 되돌리기 · 학생 되돌리기는 학생 획만");

    // 학생 모드로 — 도구 창은 나가고 풀기 막대가 올라온다. 필기는 그대로 보이고 칸을 누르면 답 시트
    await page.locator('.pb-panel .pb-mode button', { hasText: "학생" }).click();
    await page.waitForFunction(() => location.hash.endsWith("/paper"));
    await page.waitForTimeout(450);
    assert.equal(await page.locator(".pb-panel.in").count(), 0);
    assert.equal(await page.locator(".pb-touch").count(), 0);
    assert.equal(await page.locator(".cs-pbar2.pb-out").count(), 0);
    g = await geo();
    assert.ok(Math.abs(g.w - (g.W - 8)) < 3, JSON.stringify(g));
    const inkPx = await page.evaluate(() => {
      const cv = document.querySelector(".pb-cv"), c = cv.getContext("2d"), d = c.getImageData(0, 0, cv.width, cv.height).data;
      let n = 0; for (let i = 3; i < d.length; i += 4 * 7) if (d[i] > 0) n++;
      return n;
    });
    assert.ok(inkPx > 20, `ink pixels ${inkPx}`);
    await page.screenshot({ path: path.join(SHOTS, "bd-4-student.png") });
    await page.evaluate(() => document.querySelector(".cs-paperhost").shadowRoot.querySelector(".q").click());
    await page.locator(".cs-sheet").waitFor();
    step("학생 모드 — 도구 창이 나가고 풀기 막대 · 폭 맞춤이 돌아옴, 필기는 그대로 보이고 칸을 누르면 답 시트");
    await page.locator(".cs-sheet .sv-btn", { hasText: "확인" }).click();
    await page.locator('.cs-pbar2 .pb-mode button', { hasText: "강사" }).click();
    await page.waitForFunction(() => location.hash.endsWith("/board"));
    await page.locator(".pb-panel.in").waitFor();
    step("풀다가도 막대의 토글로 다시 강사 모드");

    // 넘기기 — 한 손가락은 이동만
    await page.locator('button[title="손가락으로 넘기기(쓰지 않고 이동만)"]').click();
    const y0 = await page.evaluate(() => scrollY);
    await fire([["pointerdown", "touch", 40, mid, T + 500, 8]]);
    for (let i = 1; i <= 8; i++) { await fire([["pointermove", "touch", 40, mid, T + 500 - i * 40, 8]]); await page.waitForTimeout(12); }
    await fire([["pointerup", "touch", 40, mid, T + 180, 8]]);
    await page.waitForTimeout(300);
    const y1 = await page.evaluate(() => scrollY);
    assert.ok(y1 - y0 > 250, `${y0} → ${y1}`);
    assert.deepEqual(((await saved()).pages["0"] || []).map((s) => s.s), ["pen"]);
    step(`손가락 넘기기 — 한 손가락으로 끌면 이동(${Math.round(y1 - y0)}px) · 필기 없음`);
    await page.locator('button[title="손가락으로 넘기기(쓰지 않고 이동만)"]').click();

    await page.locator('.pb-panel button[title="설정"]').click();
    await page.getByText("강사 모드 설정").waitFor();
    await page.locator(".pb-set .seg button", { hasText: "켬" }).click();
    await page.locator(".pb-set .seg button", { hasText: "왼손" }).click();
    await page.waitForTimeout(500);
    assert.equal(await page.locator(".pb-panel.R.in").count(), 1);
    g = await geo();
    assert.ok(g.l >= 44 && g.l <= 52 && g.panelL >= g.W - 90, JSON.stringify(g));
    await page.screenshot({ path: path.join(SHOTS, "bd-5-left.png") });
    step("설정 — 왼손잡이면 도구 창은 오른쪽, 손 받침 띠는 왼쪽 · 진단 표시");
    assert.deepEqual(errs, []);
    await ctx.close();
  }
  // ── 학생 계정: 토글 없음 · …/board 로 와도 학생 모드 ──
  if (want("board")) {
    const { page, errs, go, ctx } = await open(browser, "student", port);
    await go("#/sets/prob/01/board");
    await page.locator(".cs-pbar2").waitFor();
    await page.waitForTimeout(700);
    assert.equal(await page.locator(".pb-mode").count(), 0);
    assert.equal(await page.locator(".pb-panel").count(), 0);
    assert.equal(await page.locator(".pb-touch").count(), 0);
    step("학생 계정 — 학생 | 강사 토글 없음, …/board 로 열어도 학생 모드");
    assert.deepEqual(errs, []);
    await ctx.close();
  }
  console.log(`\n${n}단계 통과`);
} finally {
  await browser.close();
  srv.close();
}
