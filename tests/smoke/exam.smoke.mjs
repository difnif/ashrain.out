// 시험 보기 — 범위 고르기(학기 → 단원/학기 전체) 스모크. dist/ 를 띄우고 Supabase 를 모의 응답으로 대체한다.
//   node tests/smoke/exam.smoke.mjs [--headed]
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

// ── 모의 데이터: 중1-1 개념 34개(단원 4개) · 문항은 단원 1(정수와 유리수)에만 없다 ──
const CONCEPTS = [];
for (let i = 1; i <= 34; i++) CONCEPTS.push({ id: `m1-1-${String(i).padStart(2, "0")}`, unit_id: "m1-1", title: `개념 ${i}`, subtitle: null, sort_order: i });
for (let i = 1; i <= 21; i++) CONCEPTS.push({ id: `m1-2-${String(i).padStart(2, "0")}`, unit_id: "m1-2", title: `도형 ${i}`, subtitle: null, sort_order: i });
const EMPTY_RANGE = [9, 18];                                           // m1-1~1 = 준비 중
const inRange = (n) => n >= EMPTY_RANGE[0] && n <= EMPTY_RANGE[1];
const ITEMS = [];
for (let i = 1; i <= 34; i++) {
  if (inRange(i)) continue;
  for (let k = 0; k < 3; k++) ITEMS.push({
    id: 1000 + i * 10 + k, unit_id: "m1-1", concept_ids: [`m1-1-${String(i).padStart(2, "0")}`], qtype: "short", difficulty: 2,
    question: `개념 ${i} 문제 ${k + 1}: 3 + ${i} 은?`, choices: null, answer: String(3 + i), answer_alt: null, points: 4, time_limit: 60, tags: [], solution: null,
    figure: null, labels: {}, template_id: `t${i}`, math_key: null, created_at: "2026-01-01T00:00:00Z", param_index: k,
  });
}
for (let i = 1; i <= 21; i++) for (let k = 0; k < 2; k++) ITEMS.push({          // 중1-2 는 모든 개념에 2문항
  id: 5000 + i * 10 + k, unit_id: "m1-2", concept_ids: [`m1-2-${String(i).padStart(2, "0")}`], qtype: "choice", difficulty: 2,
  question: `도형 ${i} 문제 ${k + 1}`, choices: ["1", "2", "3", "4", "5"], answer: "2", answer_alt: null, points: 4, time_limit: 60, tags: [], solution: null,
  figure: null, labels: {}, template_id: `d${i}`, math_key: null, created_at: "2026-01-01T00:00:00Z", param_index: k,
});
const inserted = [];                                                  // test_runs insert 기록

function parseOv(v) { const m = /^ov\.\{(.*)\}$/.exec(v || ""); return m ? m[1].split(",").map((s) => s.replace(/^"|"$/g, "")).filter(Boolean) : null; }
function filterItems(u) {
  let list = ITEMS.slice();
  const unit = u.searchParams.get("unit_id"); if (unit) list = list.filter((it) => `eq.${it.unit_id}` === unit);
  const ov = parseOv(u.searchParams.get("concept_ids"));
  if (ov) list = list.filter((it) => it.concept_ids.some((c) => ov.includes(c)));
  const cs = u.searchParams.get("concept_ids");
  if (cs && cs.startsWith("cs.")) { const one = cs.replace(/^cs\.\{"?|"?\}$/g, ""); list = list.filter((it) => it.concept_ids.includes(one)); }
  const qt = u.searchParams.get("qtype"); if (qt && qt.startsWith("in.")) { const set = qt.slice(4, -1).split(","); list = list.filter((it) => set.includes(it.qtype)); }
  return list;
}

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
      if (table === "test_items") {
        const list = filterItems(u);
        if (process.env.SMOKE_DEBUG) console.log("  ↳", req.method(), u.search, "→", list.length);
        if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": `*/${list.length}`, "access-control-expose-headers": "content-range" }, body: "" });   // CORS 로 노출해야 count 를 읽는다
        return json(list.slice(0, Number(u.searchParams.get("limit") || 100)), { "content-range": `0-${list.length}/${list.length}` });
      }
      if (table === "concepts") return json(CONCEPTS);
      if (table === "test_runs") {
        if (req.method() === "POST") { try { inserted.push(JSON.parse(req.postData() || "{}")); } catch { /* */ } return json(wantObj ? {} : []); }
        return json([]);
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
    localStorage.setItem("ashrain-theme", "dark");
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
  const go = async (h) => { await page.goto(base + h); await page.waitForLoadState("networkidle"); };
  const text = async () => (await page.locator("body").innerText()).replace(/\s+/g, " ");

  try {
    // A. 단원 테스트 범위 고르기 — 학기 칩만 보이고 단원 목록은 아직 없다 (기억한 학기가 없을 때)
    await go("#/solve/test/unit");
    await page.locator(".ex-units .sv-chip").first().waitFor({ timeout: 15000 });
    let t = await text();
    ok(/학기를 고른 다음 단원 하나/.test(t), "A1 안내 문구 — 학기 → 단원");
    ok((await page.locator(".ex-chapters").count()) === 0, "A2 학기를 고르기 전에는 단원 목록이 없다");
    const m11 = page.locator(".ex-units .sv-chip", { hasText: "중1-1" });
    await m11.waitFor();
    await page.waitForFunction(() => [...document.querySelectorAll(".ex-units .sv-chip")].some((b) => /중1-1\s*\d+/.test(b.textContent)), null, { timeout: 15000 });
    ok(/중1-1\s*72/.test(await m11.innerText()), "A3 학기 칩에 공개 문항 수 (중1-1 72)");
    ok(await page.locator(".ex-units .sv-chip", { hasText: "고3-1" }).isDisabled(), "A4 문항 없는 학기 칩은 비활성");

    // B. 학기 → 단원 목록 (수·준비 중·학기 전체)
    await m11.click();
    await page.locator(".ex-chapters .sv-item").first().waitFor({ timeout: 15000 });
    await page.waitForFunction(() => ![...document.querySelectorAll(".ex-chapters .sv-item .rt")].some((e) => e.textContent.trim() === "…"), null, { timeout: 15000 });
    await shot("exam-scope-chapters");
    const rows = page.locator(".ex-chapters .sv-item");
    ok((await rows.count()) === 5, "B1 중1-1 단원 4개 + 학기 전체 = 5줄");
    t = await text();
    ok(/소인수분해.*개념 1~8.*24문항/.test(t), "B2 1단원 소인수분해 24문항 (개념 1~8)");
    ok(/정수와 유리수.*준비 중/.test(t), "B3 문항 없는 단원은 준비 중");
    ok(await rows.nth(1).isDisabled(), "B4 준비 중 단원은 누를 수 없다");
    ok(/중1-1 전체.*72문항/.test(t), "B5 학기 전체 줄 72문항");
    ok(await m11.evaluate((b) => b.classList.contains("on")), "B6 고른 학기 칩 강조");

    // C. 단원 고르기 → 확인 카드 (주소에 단원 id) → 시작 → 러너
    await rows.nth(2).click();                                                  // 문자와 식 (m1-1~2)
    await page.waitForFunction(() => location.hash === "#/solve/test/unit/m1-1~2", null, { timeout: 15000 });
    await page.locator(".sv-btn.pri", { hasText: "시작" }).waitFor({ timeout: 15000 });
    t = await text();
    ok(/중1-1 · 문자와 식/.test(t), "C1 확인 카드에 학기 · 단원 제목");
    ok(/고른 단원\(또는 학기 전체\)/.test(t), "C2 규칙 문구");
    await shot("exam-confirm-chapter");
    await page.locator(".sv-btn.pri", { hasText: "시작" }).click();
    await page.locator(".ex-head").waitFor({ timeout: 15000 });
    await sleep(300);
    t = await text();
    ok(/중1-1 · 문자와 식/.test(t), "C3 러너 머리에 범위");
    ok(/준비된 문항이 20개뿐|1 \/ 20/.test(t), "C4 20문항 (단원 문항 30개 중 템플릿 분산으로 20)");
    const qs = await page.locator(".sv-card").first().innerText();
    const m = /개념 (\d+) 문제/.exec(qs);
    ok(m && Number(m[1]) >= 19 && Number(m[1]) <= 28, `C5 첫 문항이 단원 범위(개념 19~28)의 것 — ${m ? m[1] : "?"}`);
    await shot("exam-runner-chapter");

    // D. 제출 → test_runs 행의 meta.scope 가 chapter
    await page.locator(".sv-btn.pri.full.ex-submit").click();
    const modalBtn = page.locator(".ex-modal .sv-btn.pri", { hasText: "지금 제출하기" });
    if (await modalBtn.count()) await modalBtn.click();
    await page.locator(".ex-score").waitFor({ timeout: 15000 });
    await page.waitForFunction(() => /응시 기록을 저장했어요|기기에만 기록/.test(document.body.innerText), null, { timeout: 15000 });
    const row = inserted[inserted.length - 1];
    ok(row && row.test_type === "unit" && row.unit_id === "m1-1", "D1 test_runs 행 — unit 테스트 · m1-1");
    ok(row && row.meta?.scope?.kind === "chapter" && row.meta.scope.id === "m1-1~2" && row.meta.scope.unit_id === "m1-1" && row.meta.scope.title === "중1-1 · 문자와 식", "D2 meta.scope = chapter m1-1~2");
    ok(row && row.item_ids.length === 20 && row.concept_ids.every((c) => { const n = Number(c.split("-")[2]); return n >= 19 && n <= 28; }), "D3 문항 20개, 개념이 전부 단원 안");
    await shot("exam-result-chapter");

    // E. 최근 응시 → 단원 링크로 확인 카드 (딥링크 복원)
    await go("#/solve/test/unit/m1-1~2");
    await page.locator(".sv-btn.pri", { hasText: "시작" }).waitFor({ timeout: 15000 });
    ok(/중1-1 · 문자와 식/.test(await text()), "E1 단원 딥링크 → 확인 카드");
    // 없는 단원 id → 범위 고르기로
    await go("#/solve/test/unit/m1-1~7");
    await page.locator(".ex-units .sv-chip").first().waitFor({ timeout: 15000 });
    ok(/학기를 고른 다음/.test(await text()), "E2 없는 단원 id 는 범위 고르기");
    // 학기 전체 딥링크는 그대로
    await go("#/solve/test/unit/m1-2");
    await page.locator(".sv-btn.pri", { hasText: "시작" }).waitFor({ timeout: 15000 });
    ok(/중1-2/.test(await text()), "E3 학기 id 딥링크 = 학기 전체 확인 카드");

    // F. 범위 다시 고르기 → 마지막 학기가 골라진 채로 단원 목록
    await page.locator(".sv-btn.ghost", { hasText: "범위 다시 고르기" }).click();
    await page.locator(".ex-chapters .sv-item").first().waitFor({ timeout: 15000 });
    ok(await page.locator(".ex-units .sv-chip", { hasText: "중1-2" }).evaluate((b) => b.classList.contains("on")), "F1 다시 고르기 — 학기 기억");
    await page.locator(".ex-chapters .sv-item").last().click();                 // 중1-2 전체
    await page.waitForFunction(() => location.hash === "#/solve/test/unit/m1-2", null, { timeout: 15000 });
    ok(true, "F2 학기 전체 줄 → 학기 id 주소");

    // G. 다른 유형(ash·mock)도 같은 범위 고르기
    await go("#/solve/test/mock");
    await page.locator(".ex-units .sv-chip", { hasText: "중1-1" }).waitFor({ timeout: 15000 });
    await page.waitForFunction(() => [...document.querySelectorAll(".ex-units .sv-chip")].some((b) => /중1-1\s*\d+/.test(b.textContent)), null, { timeout: 15000 });
    await page.locator(".ex-units .sv-chip", { hasText: "중1-1" }).click();
    await page.locator(".ex-chapters .sv-item").first().waitFor({ timeout: 15000 });
    ok((await page.locator(".ex-chapters .sv-item").count()) === 5, "G1 모의고사도 학기 → 단원 목록");
    await page.locator(".ex-chapters .sv-item").first().click();                // 소인수분해 (m1-1~0)
    await page.waitForFunction(() => location.hash === "#/solve/test/mock/m1-1~0", null, { timeout: 15000 });
    await page.locator(".sv-btn.pri", { hasText: "시작" }).waitFor({ timeout: 15000 });
    ok(/중1-1 · 소인수분해/.test(await text()), "G2 모의고사 확인 카드에 단원");

    // H. 개념 묶음은 그대로 개념 고르기
    await go("#/solve/test/concept_set");
    await page.locator(".sv-item").first().waitFor({ timeout: 15000 });
    ok((await page.locator(".ex-chapters").count()) === 0 && /개념을 고르면/.test(await text()), "H1 개념 묶음은 개념 고르기");

    const realErrors = errors.filter((e) => !/favicon|manifest|\.env|VITE_SUPABASE|Failed to load resource|ERR_TUNNEL|ERR_FAILED|net::/.test(e));   // 막아 둔 외부 폰트·CDN 은 제외
    ok(!realErrors.length, "Z 콘솔·페이지 오류 없음" + (realErrors.length ? " — " + realErrors.slice(0, 3).join(" | ") : ""));
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e?.message || e);
    await shot("exam-smoke-error");
  } finally {
    await browser.close(); srv.close();
  }
  console.log(`\n${pass}/${pass + fail} 통과`);
  process.exit(fail ? 1 : 0);
})();
