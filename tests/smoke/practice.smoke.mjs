// 예제·유제(#/p/<개념>) 흐름 스모크 — 예제는 해설 먼저(답 입력 없음), 유제는 답 먼저 → 해설. dist/ 를 띄우고 Supabase 를 모의 응답으로 대체한다.
//   node tests/smoke/practice.smoke.mjs [--headed]
// 준비: `npx vite build` (dist/ 필요) · playwright(전역) + Chromium.
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
const HEADED = process.argv.includes("--headed");
const SHOTS = process.env.SMOKE_SHOTS || path.join(HERE, "shots");

// ── 모의 세트: 예제 1 · 유제(단답) · 유제(객관식) · 유제(분수) ──
const SET = {
  concept_id: "m1-1-01", title: "소수와 합성수 · 예제·유제",
  problems: [
    { id: "p01", level: "기본", kind: "예제", text: [{ t: "10 이하의 " }, { t: "소수" }, { t: "의 개수를 구하시오." }],
      steps: [{ hl: [1], note: "소수는 1과 자기 자신만을 약수로 갖는 수예요.", expr: "2, 3, 5, 7" }, { hl: [0], note: "10 이하만 세요.", expr: "개수 = 4" }],
      answer: { label: "개수", accept: ["4개"], placeholder: "예: 4개", unit: "개" } },
    { id: "p02", level: "기본", kind: "유제", text: [{ t: "20 이하의 " }, { t: "소수" }, { t: "의 개수를 구하시오." }],
      steps: [{ hl: [1], note: "소수를 나열해요.", expr: "2, 3, 5, 7, 11, 13, 17, 19" }, { hl: [0], note: "세어 보면", expr: "8" }],
      answer: { label: "개수", accept: ["8개"], placeholder: "예: 8개", unit: "개" } },
    { id: "p03", level: "표준", kind: "유제", text: [{ t: "다음 중 " }, { t: "합성수" }, { t: "인 것은?" }],
      choices: ["7", "9", "11", "13", "17"],
      steps: [{ hl: [1], note: "약수가 3개 이상인 수", expr: "9 = 3 × 3" }],
      answer: { label: "정답 번호", accept: ["2"], placeholder: "번호만 입력 (예: 2)" } },
    { id: "p04", level: "표준", kind: "유제", text: [{ t: "10 이하의 자연수 중 소수인 것의 비율을 기약분수로 나타내시오." }],
      steps: [{ hl: [0], note: "소수 4개 / 전체 10개", expr: "4/10 = 2/5" }],
      answer: { label: "비율", accept: ["2/5"], placeholder: "예: 2/5", format: "fraction" } },
  ],
};
const upserts = [];                                                   // practice_progress upsert 기록

// ── 정적 서버 (dist + SPA fallback) ──────────────────────────────────────────
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ico": "image/x-icon", ".webmanifest": "application/manifest+json" };
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

// ── Supabase 모의 ────────────────────────────────────────────────────────────
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const USER = { id: "00000000-0000-4000-8000-000000000001", aud: "authenticated", role: "authenticated", email: "smoke@example.com", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: {}, factors: [], created_at: "2026-01-01T00:00:00Z" };
const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], app_metadata: USER.app_metadata, user_metadata: {}, session_id: "s1" })}.sig`;
const SESSION = { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r1", user: USER };
const PROFILE = { role: "student", member_code: "SMOKE", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "2011-03-01", settings: {} };

async function mockSupabase(page) {
  await page.route("https://placeholder.supabase.co/**", (route) => {
    const req = route.request(); const u = new URL(req.url()); const accept = req.headers()["accept"] || "";
    const json = (obj, headers = {}) => route.fulfill({ status: 200, contentType: "application/json", headers, body: JSON.stringify(obj) });
    if (u.pathname.startsWith("/auth/v1/user")) return json(USER);
    if (u.pathname.startsWith("/auth/v1/token")) return json(SESSION);
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0];
      const wantObj = accept.includes("pgrst.object");
      if (table === "practice_sets") return json(wantObj ? SET : [SET]);
      if (table === "practice_progress") {
        if (req.method() === "POST") { try { upserts.push(JSON.parse(req.postData() || "{}")); } catch { /* */ } return json(wantObj ? {} : []); }
        return json(wantObj ? null : []);
      }
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0", "access-control-expose-headers": "content-range" }, body: "" });
      if (table === "profiles") return json(wantObj ? { id: USER.id, ...PROFILE } : [{ id: USER.id, ...PROFILE }]);
      if (table === "app_settings") return json([]);
      if (req.method() === "POST") return json(wantObj ? {} : []);
      return json(wantObj ? null : [], { "content-range": "0-0/0" });
    }
    return json({});
  });
  await page.addInitScript(([key, sess]) => {
    localStorage.setItem(key, JSON.stringify(sess));
    localStorage.setItem("ashrain-theme", "light");
  }, ["sb-placeholder-auth-token", SESSION]);
}

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}/`;
  const browser = await chromium.launch({ headless: !HEADED });
  const ctx = await browser.newContext({ viewport: { width: 420, height: 860 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push("console: " + m.text()); });
  await mockSupabase(page);
  await page.route(/https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)\//, (r) => r.abort());
  fs.mkdirSync(SHOTS, { recursive: true });
  const shot = async (name) => { try { await page.screenshot({ path: path.join(SHOTS, name + ".png"), fullPage: true }); } catch { /* */ } };
  const text = async () => (await page.locator("body").innerText()).replace(/\s+/g, " ");
  const card = () => page.locator(".pv-card");

  try {
    await page.goto(base + "#/p/m1-1-01");
    await card().waitFor({ timeout: 20000 });

    // A. 예제 — 답 입력 없음, 해설 먼저, 끝나면 답 표시 + 해결 기록
    let t = await text();
    ok(/예제 1/.test(t) && (await page.locator(".pv-input").count()) === 0, "A1 예제: 답 입력 칸이 없다");
    ok(/해설 시작하기/.test(t), "A2 예제: 해설 시작 버튼");
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).click();
    await page.locator(".pv-step").first().waitFor();
    ok((await page.locator(".pv-step").count()) === 1 && !/개수 4개|4개/.test(await page.locator(".pv-final").innerText().catch(() => "")), "A3 단계 1 공개, 답은 아직");
    await page.locator(".pv-btn-main", { hasText: "다음 단계" }).click();
    await page.locator(".pv-final").waitFor({ timeout: 5000 });
    t = await text();
    ok(/개수\s*4개/.test(t) && /풀이를 끝까지 봤어요/.test(t), "A4 해설 끝 → 답 표시(4개)");
    await sleep(300);
    ok(upserts.length >= 1 && upserts[upserts.length - 1].solved.includes("p01"), "A5 예제 해결 기록(practice_progress)");
    ok(await page.locator(".pv-chip").nth(0).evaluate((b) => b.classList.contains("done")), "A6 칩 ✓");
    await shot("practice-example-done");

    // B. 유제(단답) — 답 먼저. 힌트는 표기 방식만. 틀리면 해설 → 답 → 다시 풀기
    await page.locator(".pv-btn-main", { hasText: "다음 문제" }).click();
    await page.locator(".pv-input").waitFor({ timeout: 5000 });
    t = await text();
    ok(/유제 2/.test(t) && !/해설 시작하기/.test(t), "B1 유제: 답 칸이 먼저, 해설은 아직");
    const ph = await page.locator(".pv-input").getAttribute("placeholder");
    ok(ph === "□개 꼴로 입력", `B2 힌트는 표기 방식만 (${ph})`);
    ok(!(await page.locator(".pv-step").count()), "B3 해설 단계 숨김");
    await page.locator(".pv-input").fill("8");
    await page.locator(".pv-btn-main", { hasText: "확인" }).click();
    await sleep(200);
    t = await text();
    ok(/단위가 빠졌어요/.test(t) && !/해설 시작하기/.test(t), "B4 단위 누락 → 경고만, 시도로 안 침");
    await sleep(900);
    await page.locator(".pv-input").fill("7개");
    await page.waitForSelector(".pv-flash", { state: "detached", timeout: 3000 });
    await page.locator(".pv-btn-main", { hasText: "확인" }).click();
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).waitFor({ timeout: 5000 });
    t = await text();
    ok(/아쉬워요/.test(t) && (await page.locator(".pv-input").isDisabled()), "B5 오답 → 입력 잠금 + 해설 버튼");
    ok(!/개수\s*8개/.test(t), "B6 오답 직후엔 답이 안 보인다");
    ok(await page.locator(".pv-chip").nth(1).evaluate((b) => b.classList.contains("miss")), "B7 칩 ✗");
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).click();
    await page.locator(".pv-btn-main", { hasText: "다음 단계" }).click();
    await page.locator(".pv-final").waitFor({ timeout: 5000 });
    t = await text();
    ok(/개수\s*8개/.test(t) && /내 답\s*7개/.test(t) && /다시 풀어 보기/.test(t), "B8 해설 끝 → 정답·내 답·다시 풀기");
    ok(!upserts.some((u) => u.solved.includes("p02")), "B9 오답은 해결로 기록 안 됨");
    await shot("practice-yuje-wrong");
    await page.locator(".pv-btn", { hasText: "다시 풀어 보기" }).click();
    await page.locator(".pv-input:not([disabled])").waitFor({ timeout: 5000 });
    ok(!(await page.locator(".pv-step").count()) && !(await page.locator(".pv-final").count()), "B10 다시 풀기 → 해설 접힘, 입력 열림");
    await page.locator(".pv-input").fill("8개");
    await page.waitForSelector(".pv-flash", { state: "detached", timeout: 3000 });   // 오답 번쩍임(550ms)이 끝나야 확인이 먹는다 — 사람은 이보다 느리다
    await page.locator(".pv-btn-main", { hasText: "확인" }).click();
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).waitFor({ timeout: 5000 });
    t = await text();
    ok(/정답!/.test(t), "B11 재도전 정답");
    await sleep(300);
    ok(upserts[upserts.length - 1].solved.includes("p02"), "B12 정답 → 해결 기록");
    ok(!/다음 문제/.test(t), "B13 정답이어도 해설을 봐야 다음으로");
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).click();
    await page.locator(".pv-btn-main", { hasText: "다음 단계" }).click();
    await page.locator(".pv-final").waitFor({ timeout: 5000 });

    // C. 유제(객관식) — 보기를 눌러 고르기, 힌트 "번호로 입력 (1~5)"
    await page.locator(".pv-btn-main", { hasText: "다음 문제" }).click();
    await page.locator(".pv-choices.pick").waitFor({ timeout: 5000 });
    ok((await page.locator(".pv-input").getAttribute("placeholder")) === "번호로 입력 (1~5)", "C1 객관식 힌트에 예시 없음");
    await page.locator(".pv-choices.pick .pv-choice").nth(1).click();
    ok((await page.locator(".pv-input").inputValue()) === "2" && (await page.locator(".pv-choice.on").count()) === 1, "C2 보기 누르면 번호가 들어간다");
    await page.waitForSelector(".pv-flash", { state: "detached", timeout: 3000 });
    await page.locator(".pv-btn-main", { hasText: "확인" }).click();
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).waitFor({ timeout: 5000 });
    ok(/정답!/.test(await text()), "C3 객관식 정답");
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).click();
    await page.locator(".pv-final").waitFor({ timeout: 5000 });
    ok((await page.locator(".pv-choice.ok").count()) === 1 && /정답 번호\s*②/.test(await text()), "C4 해설 끝 → 정답 보기 표시 ②");
    await shot("practice-choice-done");

    // D. 유제(분수) — 두 칸, 정확 일치
    await page.locator(".pv-btn-main", { hasText: "다음 문제" }).click();
    await page.locator(".pv-fracin").waitFor({ timeout: 5000 });
    await page.locator(".pv-fr-in").nth(0).fill("4");
    await page.locator(".pv-fr-in").nth(1).fill("10");
    await page.waitForSelector(".pv-flash", { state: "detached", timeout: 3000 });
    await page.locator(".pv-btn-main", { hasText: "확인" }).click();
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).waitFor({ timeout: 5000 });
    ok(/아쉬워요/.test(await text()), "D1 4/10 은 기약분수가 아니라 오답(정확 일치)");
    await page.locator(".pv-btn-main", { hasText: "해설 시작하기" }).click();
    await page.locator(".pv-final").waitFor({ timeout: 5000 });
    t = await text();
    ok(/비율\s*2\s*5/.test(t) && /학습 완료/.test(t), "D2 마지막 문제 → 답(2/5) + 학습 완료 버튼");
    ok(!/챕터 클리어/.test(t), "D3 하나 틀렸으니 클리어 아님");

    const realErrors = errors.filter((e) => !/favicon|manifest|\.env|VITE_SUPABASE|Failed to load resource|ERR_TUNNEL|ERR_FAILED|net::/.test(e));
    ok(!realErrors.length, "Z 콘솔·페이지 오류 없음" + (realErrors.length ? " — " + realErrors.slice(0, 3).join(" | ") : ""));
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e?.message || e);
    await shot("practice-smoke-error");
  } finally {
    await browser.close(); srv.close();
  }
  console.log(`\n${pass}/${pass + fail} 통과`);
  process.exit(fail ? 1 : 0);
})();
