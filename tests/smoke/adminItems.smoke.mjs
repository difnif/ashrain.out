// 문항 검토(#/admin/items) 스모크 — 가벼운 목록 조회 · 펼칠 때 해설 받기 · 학생과 같은 표시(괄호 규칙) · 1,000건씩 일괄 전환.
//   node tests/smoke/adminItems.smoke.mjs [--headed]
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

// ── 모의 데이터: draft 2,300건(1,000건씩 세 번 전환되도록) + live 5건 ──
const ITEMS = [];
const SOL = { levels: [
  { level: 1, title: "방침", text: "두 근이 p, q 이면 (x − p)(x − q) = 0 이다." },
  { level: 2, title: "전개", steps: ["(x − (-3))(x − (-1)) = 0", "전개하면 x² − (-4)x + 3 = 0", "따라서 b = [[frac(4, 1)]]"] },
  { level: 3, title: "확인", text: "x = -3을 대입하면 (-3)² + 4 × (-3) + 3 = 0" },
], rubric: { total: 7, items: [{ element: "인수 만들기", points: 3, criterion: "(x − (-3))(x − (-1)) = 0 꼴로 세웠다." }] } };
for (let i = 0; i < 2305; i++) ITEMS.push({
  id: `00000000-0000-4000-8000-${String(i).padStart(12, "0")}`, test_type: "concept_set", unit_id: "m3-1", concept_ids: ["m3-1-20"], qtype: "short", difficulty: 3,
  question: `이차방정식 문제 ${i}: 두 근이 -3, -1인 이차방정식 x² + bx + c = 0 에서 b는?`, choices: null, answer: "4", answer_alt: [], tags: [], source: "seed",
  status: i < 2300 ? "draft" : "live", gen_meta: { tpl: "m3-1-quad-build-t1", idx: i }, created_at: `2026-09-21T14:${String(i % 60).padStart(2, "0")}:00Z`,
  template_id: "m3-1-quad-build-t1", param_index: i, content_key: `ck${i}`, struct_key: "sk", solution: SOL,
  figure: i === 0 ? [{ fn: "steps", args: { lines: [{ text: "(x − (-3))(x − (-1)) = 0" }] } }] : null,
});
for (let i = 0; i < 7; i++) ITEMS.push({                            // 다른 개념·틀: live 만 7건
  id: `00000000-0000-4000-8000-1${String(i).padStart(11, "0")}`, test_type: "concept_set", unit_id: "m1-1", concept_ids: ["m1-1-02"], qtype: "short", difficulty: 2,
  question: `거듭제곱 문제 ${i}: 2³의 값은?`, choices: null, answer: "8", answer_alt: [], tags: [], source: "seed", status: "live",
  gen_meta: { tpl: "m1-1-power-t1", idx: i }, created_at: "2026-09-21T14:00:00Z", template_id: "m1-1-power-t1", param_index: i, content_key: `pk${i}`, struct_key: "sk2",
  solution: SOL, figure: null, labels: { L43_discriminates: "거듭제곱을 곱셈으로 풀어 계산하는가", geometry: false },
});
ITEMS.forEach((it) => { if (!it.labels) it.labels = { L43_discriminates: "근이 p 이면 인수가 (x − p) 임을 아는가", geometry: false }; });
const CONCEPTS = [{ id: "m3-1-20", unit_id: "m3-1", title: "이차방정식 구하기", sort_order: 20 }, { id: "m1-1-02", unit_id: "m1-1", title: "거듭제곱", sort_order: 2 }];
function templateStats() {                                            // admin_template_stats() 모의
  const by = new Map();
  for (const it of ITEMS) {
    if (!by.has(it.template_id)) by.set(it.template_id, { template_id: it.template_id, seed: it.template_id.replace(/-t\d+$/, ""), n_draft: 0, n_live: 0, sample_id: it.id, unit_id: it.unit_id, concept_id: it.concept_ids[0], qtype: it.qtype, difficulty: it.difficulty, made_at: it.created_at, sample_q: it.question, discriminates: it.labels.L43_discriminates, geometry: false, has_figure: !!it.figure });
    const r = by.get(it.template_id); if (it.status === "draft") r.n_draft++; else r.n_live++;
  }
  return [...by.values()];
}
const log = [];                                                       // 요청 기록

function applyFilters(u) {
  let list = ITEMS.slice();
  for (const [k, v] of u.searchParams) {
    if (["select", "order", "limit", "offset"].includes(k)) continue;
    if (v.startsWith("eq.")) list = list.filter((it) => String(it[k]) === v.slice(3));
    else if (v.startsWith("in.")) { const set = v.slice(4, -1).split(",").map((s) => s.replace(/^"|"$/g, "")); list = list.filter((it) => set.includes(String(it[k]))); }
    else if (v.startsWith("cs.")) { const one = v.replace(/^cs\.\{"?|"?\}$/g, ""); list = list.filter((it) => (it[k] || []).includes(one)); }
  }
  const order = u.searchParams.get("order");
  if (order) {
    const keys = order.split(",").map((o) => { const [c, d] = o.split("."); return [c, d === "desc" ? -1 : 1]; });
    list.sort((a, b) => { for (const [c, d] of keys) { if (a[c] < b[c]) return -d; if (a[c] > b[c]) return d; } return 0; });
  }
  return list;
}
function project(row, select) {
  if (!select || select === "*") return row;
  const out = {};
  for (const c of select.split(",")) if (c in row) out[c] = row[c];
  return out;
}

// ── 정적 서버 ──
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

// ── Supabase 모의 (관리자) ──
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const USER = { id: "00000000-0000-4000-8000-000000000001", aud: "authenticated", role: "authenticated", email: "smoke@example.com", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: {}, factors: [], created_at: "2026-01-01T00:00:00Z" };
const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], app_metadata: USER.app_metadata, user_metadata: {}, session_id: "s1" })}.sig`;
const SESSION = { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r1", user: USER };
const PROFILE = { role: "admin", member_code: "SMOKE", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "1990-03-01", settings: {} };

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
      if (u.pathname === "/rest/v1/rpc/admin_template_stats") { log.push({ m: "RPC", q: "admin_template_stats" }); return json(templateStats()); }
      if (table === "test_items") {
        log.push({ m: req.method(), q: u.search });
        const list = applyFilters(u);
        if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": `*/${list.length}`, "access-control-expose-headers": "content-range" }, body: "" });
        if (req.method() === "PATCH") {
          let body = {}; try { body = JSON.parse(req.postData() || "{}"); } catch { /* */ }
          for (const it of list) Object.assign(it, body);
          return json([]);
        }
        const off = Number(u.searchParams.get("offset") || 0), lim = Number(u.searchParams.get("limit") || 1000);
        const sel = u.searchParams.get("select");
        const rows = list.slice(off, off + lim).map((r) => project(r, sel));
        return json(wantObj ? rows[0] ?? null : rows, { "content-range": `${off}-${off + rows.length}/${list.length}` });
      }
      if (table === "concepts") return json(CONCEPTS);
      if (table === "item_templates") return json([]);
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

(async () => {
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}/`;
  const browser = await chromium.launch({ headless: !HEADED });
  const ctx = await browser.newContext({ viewport: { width: 420, height: 900 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
  page.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) errors.push("console: " + m.text()); });   // 막아 둔 외부 폰트·CDN 은 제외
  page.on("dialog", (d) => d.accept());
  await mockSupabase(page);
  await page.route(/https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)\//, (r) => r.abort());
  fs.mkdirSync(SHOTS, { recursive: true });
  const shot = async (name) => { try { await page.screenshot({ path: path.join(SHOTS, name + ".png"), fullPage: true }); } catch { /* */ } };
  const text = async () => (await page.locator("body").innerText()).replace(/\s+/g, " ");

  try {
    // A. 목록 — 가벼운 열만 · 틀 순서 · 넓은 필터에서는 건수를 세지 않는다(RLS 시간 초과 회피)
    await page.goto(base + "#/admin/items");
    await page.locator(".irv-item").first().waitFor({ timeout: 20000 });
    await page.waitForFunction(() => /틀 \d+개 · draft \d+/.test(document.querySelector(".irv-sub")?.textContent || ""), null, { timeout: 15000 });
    let t = await text();
    ok(/전체 틀 2개 · draft 2300 \/ live 12/.test(t), "A1 머리말은 틀별 집계에서 — 전체 틀 2개 · draft 2300 / live 12");
    ok(!/불러오기 실패/.test(t), "A2 실패 문구 없음");
    const listReq = log.find((l) => l.m === "GET" && /select=/.test(l.q) && /offset=/.test(l.q));
    ok(listReq && !/solution|figure/.test(decodeURIComponent(listReq.q)) && /limit=51/.test(listReq.q), "A3 목록 조회는 해설·그림 열 없이 51건(다음 쪽 유무 확인용)");
    ok(listReq && /order=template_id[.,]/.test(decodeURIComponent(listReq.q)), "A4a 정렬은 틀 순서(template_id, param_index)");
    ok(log.filter((l) => l.m === "HEAD").length === 0, "A4b 넓은 필터에서는 건수 질의를 하지 않는다");
    ok((await page.locator(".irv-item").count()) === 50, "A5 한 쪽 50건");
    ok(/이차방정식 문제/.test(t) && !/\[\[/.test(await page.locator(".irv-q").first().innerText()), "A6 목록 제목에 마커 기호 없음");

    // B. 펼치기 — 해설·그림을 그때 받고, 학생과 같은 표시(괄호 규칙 · 분수)
    const before = log.length;
    await page.locator(".irv-row").first().click();
    await page.locator(".irv-detail .isol .lv").first().waitFor({ timeout: 15000 });
    const solReq = log.slice(before).find((l) => l.m === "GET" && /select=solution/.test(l.q));
    ok(!!solReq && /id=eq\./.test(solReq.q), "B1 펼치면 그 문항의 solution·figure 만 받는다");
    const det = page.locator(".irv-detail");
    const dt = (await det.innerText()).replace(/\s+/g, " ");
    ok(/\{x − \(-3\)\}\{x − \(-1\)\} = 0/.test(dt), "B2 해설의 겹괄호가 { } 로 (괄호 규칙)");
    ok((await det.locator(".mf").count()) >= 1, "B3 [[frac]] 마커는 상하 분수로");
    ok(/채점기준 · 7점/.test(dt) && /인수 만들기/.test(dt), "B4 채점기준표 표시");
    ok((await det.locator(".iq").count()) === 1 && /거듭제곱 문제 0/.test(dt), "B5 문항 본문은 ItemQuestion 으로 (틀 순서상 첫 줄은 m1-1-power-t1)");
    ok(/정답: 8/.test(dt), "B6 정답 표시");
    await shot("admin-items-open");

    // D. 틀별 보기 — 집계 함수로 틀 목록, draft 있는 틀만, 문항 보기 → 틀 필터, 틀 하나 전환
    await page.locator("button.irv-chip", { hasText: "틀별" }).click();
    await page.locator(".irv-tpl").first().waitFor({ timeout: 15000 });
    ok(log.some((l) => l.m === "RPC"), "D1 틀별 집계는 admin_template_stats RPC 로");
    let tt = await text();
    ok(/틀 1개 · draft 2300 \/ live 5/.test(tt), "D2 머리말 — draft 있는 틀 1개 (live 만 있는 틀은 숨김)");
    ok(/이차방정식 구하기/.test(tt) && /재는 것: 근이 p 이면/.test(tt) && /draft 2300 · live 5/.test(tt), "D3 개념 제목 · 재는 것 · 건수");
    await page.locator("button.irv-chip", { hasText: "draft 있는 틀만" }).click();
    ok((await page.locator(".irv-tpl").count()) === 2 && /거듭제곱/.test(await text()), "D4 토글을 끄면 live 만 있는 틀도 보인다");
    await page.locator("button.irv-chip", { hasText: "draft 있는 틀만" }).click();
    const before3 = log.length;
    await page.locator(".irv-tpl button.irv-btn", { hasText: "문항 보기" }).first().click();
    await page.locator(".irv-item").first().waitFor({ timeout: 15000 });
    await page.waitForFunction(() => /\d+건 · draft/.test(document.querySelector(".irv-sub")?.textContent || ""), null, { timeout: 15000 });
    const filt = log.slice(before3).find((l) => l.m === "GET" && /offset=/.test(l.q));
    ok(filt && /template_id=eq\.m3-1-quad-build-t1/.test(filt.q) && /concept_ids=cs\./.test(filt.q), "D5 문항 보기 → 개념·틀 필터로 목록 조회");
    ok(/틀 m3-1-quad-build-t1 ×/.test(await text()), "D6 틀 필터 칩 표시");
    ok(log.slice(before3).some((l) => l.m === "HEAD"), "D6a 좁은 필터(틀 지정)에서는 정확한 건수를 센다");
    await page.locator("button.irv-chip", { hasText: "틀별" }).click();
    await page.locator(".irv-tpl").first().waitFor({ timeout: 15000 });
    ok(!log.slice(before3).some((l) => l.m === "RPC"), "D7 다시 열어도 집계는 다시 세지 않는다(캐시)");
    // 틀 하나 전환은 소량으로 시험: live 7건짜리 틀을 draft 로
    await page.locator("button.irv-chip", { hasText: "draft 있는 틀만" }).click();
    const before4 = log.length;
    await page.locator(".irv-tpl", { hasText: "거듭제곱" }).locator("button.irv-btn", { hasText: "live → draft" }).click();
    await page.waitForFunction(() => /m1-1-power-t1: 7건 → draft/.test(document.querySelector(".irv-msg")?.textContent || ""), null, { timeout: 15000 });
    const tp = log.slice(before4).filter((l) => l.m === "PATCH");
    ok(tp.length === 1 && /id=in\./.test(tp[0].q) && ITEMS.filter((it) => it.template_id === "m1-1-power-t1" && it.status === "draft").length === 7, "D8 틀 하나 전환 — id 목록 PATCH 한 번, 7건 draft");
    ok(/draft 7 · live 0/.test(await text()), "D9 틀 카드 건수 즉시 갱신");
    await shot("admin-items-tpls");
    await page.locator("button.irv-chip", { hasText: "문항" }).first().click();
    await page.locator(".irv-item").first().waitFor({ timeout: 15000 });
    await page.locator("button.irv-chip.on", { hasText: "틀 m3-1-quad-build-t1 ×" }).click();
    await page.locator("select").nth(1).selectOption("all");
    await page.locator("select").nth(0).selectOption("all");
    await page.waitForFunction(() => /전체 틀 2개 · draft 2307/.test(document.querySelector(".irv-sub")?.textContent || ""), null, { timeout: 15000 });

    // C. 일괄 전환 — 1,000건씩 세 번, 완료 문구 (draft 2307 = 2300 + 7)
    const before2 = log.length;
    await page.locator("button.irv-btn.go", { hasText: "필터 전체 draft → live" }).click();
    await page.waitForFunction(() => /→ live 완료/.test(document.querySelector(".irv-msg")?.textContent || ""), null, { timeout: 30000 });
    const patches = log.slice(before2).filter((l) => l.m === "PATCH");
    ok(patches.length === 3, `C1 PATCH 세 번(1,000·1,000·307) — ${patches.length}번`);
    ok(patches.every((l) => /id=in\./.test(l.q)), "C2 전환은 id 목록으로");
    ok(ITEMS.filter((it) => it.status === "live").length === 2312, "C3 모의 DB 에서 2307건이 live 로");
    t = await text();
    ok(/2307건 → live 완료/.test(t), "C4 완료 문구");
    await page.waitForFunction(() => /draft 0 \/ live 2312/.test(document.querySelector(".irv-sub")?.textContent || ""), null, { timeout: 15000 });
    ok(/전체 틀 2개 · draft 0 \/ live 2312/.test(await text()), "C5 머리말 건수 갱신(집계 다시 셈)");

    ok(errors.length === 0, "Z 콘솔·페이지 오류 없음" + (errors.length ? ` — ${errors.slice(0, 3).join(" | ")}` : ""));
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e.message);
    await shot("admin-items-error");
  } finally {
    await browser.close(); srv.close();
  }
  console.log(`\n${pass}/${pass + fail} 통과`);
  process.exit(fail ? 1 : 0);
})();
