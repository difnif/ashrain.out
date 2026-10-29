// 공부하기 › 컨셉 문제 흐름 스모크 — 목록(폴더 · 아이콘) → 세트 → 풀기 · 3단 해설(움직임) → 바로 인쇄 → 다운로드 → OMR 사진 채점
//   node tests/smoke/conceptsets.smoke.mjs [--headed]
// 준비: `npx vite build` (dist/ 필요) · playwright(전역) + Chromium.
//   다운로드 확인에 쓸 PDF 가 .concept-files/prob/01/ 에 있으면(scripts/concept-files.mjs --only 01) 그걸 Storage 응답으로 쓰고, 없으면 가짜 PDF.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { layoutCard, cardHtml, BUB_R } from "../../src/lib/omr/grid.js";
import { rawOf } from "../../src/lib/conceptsets.js";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); }
catch { ({ chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright")); }

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "../..");
const DIST = path.join(ROOT, "dist");
const HEADED = process.argv.includes("--headed");
const THEME = process.env.SMOKE_THEME === "dark" ? "dark" : "light";   // SMOKE_THEME=dark 로 어두운 테마 화면도 찍어 본다
const SHOTS = process.env.SMOKE_SHOTS || path.join(HERE, "shots");
const TMP = fs.mkdtempSync(path.join(process.env.TMPDIR || "/tmp", "cs-smoke-"));
const SET = JSON.parse(fs.readFileSync(path.join(ROOT, "public/concept-sets/prob/01.json"), "utf8"));
const FILES = "https://ueohwmjtfmvqunjgfrhx.supabase.co/storage/v1/object/public/concept-sets/";

// ── 정적 서버 (dist + SPA fallback) ──────────────────────────────────────────
const MIME = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ico": "image/x-icon", ".webmanifest": "application/manifest+json" };
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

// ── Supabase 모의 (practice.smoke 와 같은 꼴) ────────────────────────────────
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const USER = { id: "00000000-0000-4000-8000-000000000001", aud: "authenticated", role: "authenticated", email: "smoke@example.com", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: {}, factors: [], created_at: "2026-01-01T00:00:00Z" };
const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], app_metadata: USER.app_metadata, user_metadata: {}, session_id: "s1" })}.sig`;
const SESSION = { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r1", user: USER };
const PROFILE = { role: "student", member_code: "SMOKE", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "2011-03-01", settings: {} };
let storageMode = "ok";        // ok | missing
const PDF = (doc) => {
  const p = path.join(ROOT, ".concept-files/prob/01", `${doc}.pdf`);
  return fs.existsSync(p) ? fs.readFileSync(p) : Buffer.from(`%PDF-1.4\n% fake ${doc}\n%%EOF\n`);
};

async function mockAll(ctx, page) {
  // 가로채기는 첫 화면(page)에만 — 컨텍스트에 걸면 window.open("") 인쇄 창의 하위 자원이 Playwright 에서 멈춘다
  await page.route("https://placeholder.supabase.co/**", (route) => {
    const req = route.request(); const u = new URL(req.url()); const accept = req.headers()["accept"] || "";
    const json = (obj, headers = {}) => route.fulfill({ status: 200, contentType: "application/json", headers, body: JSON.stringify(obj) });
    if (u.pathname.startsWith("/auth/v1/user")) return json(USER);
    if (u.pathname.startsWith("/auth/v1/token")) return json(SESSION);
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0];
      const wantObj = accept.includes("pgrst.object");
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0", "access-control-expose-headers": "content-range" }, body: "" });
      if (table === "profiles") return json(wantObj ? { id: USER.id, ...PROFILE } : [{ id: USER.id, ...PROFILE }]);
      if (req.method() === "POST") return json(wantObj ? {} : []);
      return json(wantObj ? null : [], { "content-range": "0-0/0" });
    }
    return json({});
  });
  await page.route(FILES + "**", (route) => {
    const u = new URL(route.request().url());
    const doc = (u.pathname.match(/\/(problems|solutions|omr)\.pdf$/) || [])[1];
    const cors = { "access-control-allow-origin": "*" };
    if (storageMode === "missing" || !doc) return route.fulfill({ status: 400, contentType: "application/json", headers: cors, body: JSON.stringify({ statusCode: "404", error: "not_found" }) });
    const h = { ...cors, "content-type": "application/pdf" };
    if (u.searchParams.has("download")) h["content-disposition"] = `attachment; filename*=UTF-8''${encodeURIComponent(u.searchParams.get("download"))}`;
    return route.fulfill({ status: 200, headers: h, body: PDF(doc) });
  });
  await ctx.addInitScript(([key, sess, theme]) => {
    localStorage.setItem(key, JSON.stringify(sess));
    localStorage.setItem("ashrain-theme", theme);
  }, ["sb-placeholder-auth-token", SESSION, THEME]);
  // 인쇄 대화상자 대신 횟수만 센다 (새 창에도 적용)
  await ctx.addInitScript(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; });
}

// ── OMR 카드 사진 만들기: 실제 카드 SVG 위에 연필 자국을 그리고 비스듬히 찍는다 ─────
function marks(card, p, fills) {
  const out = [];
  const dot = (x, y, r) => out.push(`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r}" fill="#262626" opacity=".93"/>`);
  for (const b of p.blocks) {
    const f = fills[b.no];
    if (f == null || f === "") continue;
    if (b.kind === "pick") { const on = String(f).match(/[ㄱ-ㅎ]/gu) || []; for (const q of b.picks) if (on.includes(q.label)) dot(q.x, q.y, BUB_R + 2.2); continue; }
    const parts = b.kind === "frac" ? (String(f).includes("/") ? String(f).split("/") : [String(f), ""]) : b.kind === "pair" ? String(f).split(/,\s*/) : [String(f)];
    b.grids.forEach((g, gi) => {
      const d = String(parts[gi] ?? "").split("");
      g.bubbles.forEach((col, ci) => { const dg = d[ci - (g.cols - d.length)]; if (dg != null && dg !== "") dot(col[+dg].x, col[+dg].y, BUB_R - 0.8); });
    });
  }
  return out.join("");
}
async function cardPhotos(browser, card, fills) {
  const page = await browser.newPage({ viewport: { width: 1200, height: 1600 } });
  const files = [];
  for (const p of card.pages) {
    const svg = cardHtml({ ...card, pages: [p] }).replace(/<\/svg>/, `${marks(card, p, fills)}</svg>`);
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>
      body{margin:0;background:#7a756d;display:flex;align-items:center;justify-content:center;height:1600px;overflow:hidden}
      .ph{transform:perspective(1600px) rotateX(${p.index ? 7 : -5}deg) rotateY(${p.index ? -4 : 3}deg) rotateZ(${p.index ? 182 : -2.5}deg);background:#fff;box-shadow:0 8px 30px rgba(0,0,0,.4)}
      .ph .omr-pg{width:${1000 * 0.9}px!important;height:${1478 * 0.9}px!important}.ph svg{width:100%!important;height:100%!important}
      .shade{position:fixed;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.18),rgba(0,0,0,.16));pointer-events:none}
      </style></head><body><div class="ph">${svg}</div><div class="shade"></div></body></html>`);
    const f = path.join(TMP, `omr-p${p.index + 1}.jpg`);
    await page.screenshot({ path: f, type: "jpeg", quality: 88 });
    files.push(f);
  }
  await page.close();
  return files;
}

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  if (!fs.existsSync(path.join(DIST, "index.html"))) { console.error("dist/ 가 없다 — npx vite build 먼저"); process.exit(2); }
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}/`;
  // 컨테이너에 로캘이 없으면 Chromium 이 한글 파일 이름을 「download」로 바꾼다 — 실제 기기처럼 UTF-8 로
  const browser = await chromium.launch({ headless: !HEADED, env: { ...process.env, LANG: "C.UTF-8", LC_ALL: "C.UTF-8" } });
  const ctx = await browser.newContext({ viewport: { width: 420, height: 860 }, deviceScaleFactor: 2, acceptDownloads: true });
  const page = await ctx.newPage();
  await mockAll(ctx, page);
  // 글꼴은 첫 화면에서만 막는다 — window.open("") 빈 창의 요청을 가로채면 Playwright 에서 하위 자원이 멈춰 load 가 안 온다
  // (실제 브라우저와 무관한 시험 도구 문제). 인쇄 창의 글꼴 요청은 그대로 두면 이 환경에선 곧바로 실패한다.
  await page.route(/https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)\//, (r) => r.abort());
  const errors = [];
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
  page.on("console", (m) => { if (m.type() === "error" && !/net::ERR_FAILED|Failed to load resource/.test(m.text())) errors.push("console: " + m.text()); });
  fs.mkdirSync(SHOTS, { recursive: true });
  const shot = async (name, p = page) => { try { await p.screenshot({ path: path.join(SHOTS, name + (THEME === "dark" ? "-dark" : "") + ".png"), fullPage: true }); } catch { /* */ } };
  const text = async () => (await page.locator("body").innerText()).replace(/\s+/g, " ");

  try {
    // A. 공부하기 › 컨셉 문제 › 경우의 수와 확률 — 아이콘 38개
    await page.goto(base + "#/study/sets");
    await page.locator(".st-folder").first().waitFor({ timeout: 20000 });
    ok(await page.locator(".sh-stab.on", { hasText: "컨셉 문제" }).count() === 1, "A1 서브탭 「컨셉 문제」 활성");
    ok(/경우의 수와 확률/.test(await page.locator(".st-folder").first().innerText()), "A2 범주 폴더");
    await page.locator(".st-folder").first().click();
    await page.locator(".st-ic").first().waitFor({ timeout: 10000 });
    ok(await page.locator(".st-ic").count() === 38, "A3 세트 아이콘 38개");
    const groups = await page.locator(".st-sec").allInnerTexts();
    ok(groups.length === 6 && groups.some((g) => /스포츠/.test(g)) && groups.some((g) => /사회/.test(g)), `A4 묶음 6개 (${groups.join(" | ")})`);
    await shot("cs-icons");

    // B. 세트 화면
    await page.locator(".st-ic", { hasText: "야구" }).click();
    await page.locator(".cs-hero").waitFor({ timeout: 10000 });
    let t = await text();
    ok(/야구로 익히는 경우의 수와 확률/.test(t) && (await page.locator(".cs-row").count()) === 50, "B1 세트 머리 · 문항 50");
    ok((await page.locator(".cs-dchip").count()) === 3 && /9쪽/.test(t) && /19쪽/.test(t) && /2쪽/.test(t), "B2 자료 칩 3개 + 쪽 수(files.json)");
    await page.locator(".cs-chip", { hasText: /^상$/ }).click();
    ok((await page.locator(".cs-row").count()) === 10, "B3 「상」 거르기 → 10");
    await page.locator(".cs-chip", { hasText: "전체" }).click();
    await shot("cs-set");

    // C. 풀기 — 오답 → 해설(3단 + 움직임) → 다시 풀기 → 정답
    await page.locator(".cs-go").click();
    await page.locator(".cs-q").waitFor({ timeout: 10000 });
    ok(/#\/sets\/prob\/01\/q\/1$/.test(page.url()), "C1 바로 풀기 → 1번");
    await page.locator(".cs-ii").fill("13");
    await page.locator(".cs-sub").click();
    await page.locator(".iv-banner.bad").waitFor({ timeout: 5000 });
    t = await text();
    ok(/아쉬워요/.test(t) && !/정답\s*12가지/.test(t), "C2 오답 — 정답은 아직 안 보임");
    await page.locator(".iv-row .sv-btn", { hasText: "해설 보기" }).click();
    await page.locator(".cs-sol").waitFor({ timeout: 5000 });
    ok((await page.locator(".cs-tg").count()) === 3 && /포지티브/.test(await text()) && /모범 답안/.test(await text()), "C3 3단 해설(방침 · 전개 · 확인) + 모범 답안");
    ok((await page.locator(".cs-sol .anim-level .anim-seek").count()) === 1, "C4 전개 판 애니메이션 플레이어 붙음");
    await page.locator(".cs-stage").scrollIntoViewIfNeeded();
    await sleep(3200);
    const hl = await page.locator(".cs-stage .anim-hl").count();
    const lineHl = await page.locator(".cs-stage .fig-line.anim-hl").count();
    ok(hl >= 2 && lineHl === 1, `C5 움직임 — 판서 한 줄 + 도식 강조 (${hl}, ${lineHl})`);
    ok(/정답\s*12가지/.test(await text()), "C6 해설을 열면 정답 표시");
    await shot("cs-solution");
    await page.locator(".cs-retry").click();
    await page.locator(".cs-ii:not([disabled])").fill("12");
    await page.locator(".cs-sub").click();
    await page.locator(".iv-banner.ok").waitFor({ timeout: 5000 });
    ok(/정답!/.test(await text()) && (await page.locator(".cs-sol").count()) === 1, "C7 재도전 정답 → 해설 바로 열림");

    // D. 분수(약분 안내) · 보기 고르기
    const frac = SET.items.find((it) => it.a.k === "frac" && it.a.d > 3 && it.a.n > 0);
    await page.goto(base + `#/sets/prob/01/q/${frac.no}`);
    await page.locator(".cs-fin").waitFor({ timeout: 10000 });
    await page.locator(".cs-fi").nth(0).fill(String(frac.a.n * 2));
    await page.locator(".cs-fi").nth(1).fill(String(frac.a.d * 2));
    await page.locator(".cs-sub").click();
    await page.locator(".iv-banner.ok").waitFor({ timeout: 5000 });
    ok(new RegExp(`기약분수로 쓰면 ${frac.a.n}/${frac.a.d}`).test(await text()), `D1 분수 ${frac.a.n * 2}/${frac.a.d * 2} → 정답 + 기약분수 안내`);
    const pick = SET.items.find((it) => it.a.k === "pick");
    await page.goto(base + `#/sets/prob/01/q/${pick.no}`);
    await page.locator(".cs-pick").first().waitFor({ timeout: 10000 });
    for (const o of pick.a.v) await page.locator(".cs-pick", { hasText: o }).click();
    await page.locator(".cs-sub").click();
    await page.locator(".iv-banner.ok").waitFor({ timeout: 5000 });
    ok(true, `D2 보기 고르기 ${pick.a.v.join("")} → 정답`);

    // E. 세트 화면 진도
    await page.goto(base + "#/sets/prob/01");
    await page.locator(".cs-hero").waitFor();
    t = await text();
    ok(/푼 문항 3\/50/.test(t) && (await page.locator(".cs-row .st.ok").count()) === 3, "E1 진도 3/50 · ✓ 3");

    // F. 바로 인쇄 — 문제지 + 해설지 + OMR 한 창
    const chip = (l) => page.locator(".cs-dchip", { hasText: l });
    if (!(await chip("해설지").getAttribute("aria-pressed")).includes("true")) await chip("해설지").click();
    if (!(await chip("문제지").getAttribute("aria-pressed")).includes("true")) await chip("문제지").click();
    if (!(await chip("OMR").getAttribute("aria-pressed")).includes("true")) await chip("OMR").click();
    const [pop] = await Promise.all([ctx.waitForEvent("page"), page.locator(".cs-dbtns .sv-btn", { hasText: "바로 인쇄" }).click()]);
    // window.open("") 빈 창에는 초기화 스크립트가 늦게 붙을 수 있어 바로 덮는다(document.open 뒤에도 같은 window)
    await pop.evaluate(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; }).catch(() => {});
    await pop.waitForFunction(() => document.querySelectorAll(".omr-pg").length === 2 && document.querySelector(".cs-doc"), null, { timeout: 15000 });
    const info = await pop.evaluate(() => ({ pg: document.querySelectorAll(".csx-p .pg").length, spg: document.querySelectorAll(".csx-s .spg").length, omr: document.querySelectorAll(".omr-pg").length, title: document.title }));
    ok(info.pg === 9 && info.spg === 19 && info.omr === 2, `F1 인쇄 창: 문제 ${info.pg}쪽 · 해설 ${info.spg}쪽 · OMR ${info.omr}쪽`);
    // 자동 인쇄: Playwright 는 가로채기(route)가 하나라도 있으면 window.open("") 창의 하위 자원을 멈춰 load 가 오지 않는다(도구 문제).
    // 그래서 인쇄 창에 쓰인 문서를 그대로 꺼내, 가로채기 없는 새 컨텍스트에서 같은 방식(window.open + document.write)으로 다시 연다.
    const written = await pop.evaluate(() => "<!doctype html>" + document.documentElement.outerHTML);
    ok(/id="cs-print-btn"/.test(written) && /window\.print\(\)/.test(written), "F2 인쇄 창에 인쇄 버튼 · 자동 인쇄 스크립트");
    {
      const ctx2 = await browser.newContext();
      await ctx2.addInitScript(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; });
      const p2 = await ctx2.newPage();
      await p2.goto(base + "favicon-none");
      await p2.evaluate(() => { document.body.innerHTML = '<button id="go">go</button>'; });
      await p2.evaluate((H) => { document.getElementById("go").onclick = () => { const w = window.open("", "_blank"); setTimeout(() => { w.document.open(); w.document.write(H); w.document.close(); }, 30); }; }, written);
      const [w2] = await Promise.all([ctx2.waitForEvent("page"), p2.click("#go")]);
      await w2.evaluate(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; }).catch(() => {});
      await w2.waitForFunction(() => window.__printed >= 1, null, { timeout: 12000 }).catch(() => {});
      await sleep(800);
      const n = await w2.evaluate(() => window.__printed || 0);
      ok(n === 1, `F3 글꼴 준비 뒤 인쇄가 한 번 자동으로 열림 (${n})`);
      await ctx2.close();
    }
    await shot("cs-print", pop);
    await pop.close();

    // G. 다운로드 — 하나(한글 이름) · 여럿(ZIP) · 아직 안 올라감
    await chip("해설지").click(); await chip("OMR").click();           // 문제지만
    let [dl] = await Promise.all([page.waitForEvent("download", { timeout: 10000 }), page.locator(".cs-dbtns .sv-btn", { hasText: "다운로드" }).click()]);
    ok(dl.suggestedFilename() === "01-야구-문제.pdf", `G1 하나 → ${dl.suggestedFilename()} (${dl.url().slice(0, 60)})`);
    await chip("OMR").click();
    [dl] = await Promise.all([page.waitForEvent("download", { timeout: 15000 }), page.locator(".cs-dbtns .sv-btn", { hasText: "다운로드" }).click()]);
    const zf = path.join(TMP, "dl.zip"); await dl.saveAs(zf);
    const names = execFileSync("python3", ["-c", "import zipfile,sys;z=zipfile.ZipFile(sys.argv[1]);assert z.testzip() is None;print('|'.join(i.filename for i in z.infolist()))", zf]).toString().trim();
    ok(dl.suggestedFilename() === "01-야구.zip" && names === "01-야구-문제.pdf|01-야구-OMR.pdf", `G2 여럿 → ZIP (${names})`);
    storageMode = "missing";
    await page.locator(".cs-dbtns .sv-btn", { hasText: "다운로드" }).click();
    await page.locator(".cs-toast").waitFor({ timeout: 8000 });
    ok(/아직 올라가지 않았어요/.test(await page.locator(".cs-toast").innerText()), "G3 파일이 없으면 안내(바로 인쇄로 PDF 저장)");
    storageMode = "ok";

    // H. OMR 사진 채점 — 정답대로 칠하되 3문항 틀리게 · 1문항 비움
    const card = layoutCard({ cat: "prob", no: SET.no, title: SET.title, items: SET.items });
    const fills = Object.fromEntries(SET.items.map((it) => [it.no, rawOf(it)]));
    const ints = SET.items.filter((it) => it.a.k === "int" && it.a.v < 900).slice(2, 5);
    for (const it of ints) fills[it.no] = String(it.a.v + 1);
    const blankNo = SET.items.find((it) => it.a.k === "frac" && it.no > 30).no;
    fills[blankNo] = "";
    const photos = await cardPhotos(browser, card, fills);
    await page.goto(base + "#/sets/prob/01/omr");
    await page.locator(".cs-shot").waitFor({ timeout: 10000 });
    await page.locator('input[type=file][multiple]').setInputFiles(photos);
    await page.locator(".cs-pg.on").nth(1).waitFor({ timeout: 30000 });
    ok((await page.locator(".cs-pg.on").count()) === 2 && (await page.locator(".cs-prv img").count()) === 2, "H1 두 쪽 모두 읽음(2쪽은 거꾸로 찍음) + 미리보기");
    const vals = await page.locator(".cs-orow input").evaluateAll((els) => els.map((e) => e.value));
    const want = SET.items.map((it) => fills[it.no]);
    const diff = want.map((w, i) => (w === vals[i] ? null : `${i + 1}:${vals[i]}≠${w}`)).filter(Boolean);
    ok(diff.length === 0, `H2 읽은 답 = 칠한 답 50/50 ${diff.length ? diff.slice(0, 6).join(" ") : ""}`);
    await shot("cs-omr-confirm");
    await page.locator(".cs-gradebtn").click();
    await page.locator(".cs-score").waitFor({ timeout: 10000 });
    const score = await page.locator(".cs-score .big b").innerText();
    ok(score === "46", `H3 채점 46/50 (${score})`);
    ok((await page.locator(".cs-rrow").count()) === 4, "H4 틀린 문항 4개 목록");
    await shot("cs-omr-result");
    await page.locator(".cs-rrow").first().click();
    await page.locator(".cs-q").waitFor({ timeout: 10000 });
    ok(/지난 기록/.test(await text()), "H5 틀린 문항 → 문항 화면(지난 기록 표시)");

    ok(errors.length === 0, "Z 콘솔 오류 없음" + (errors.length ? ": " + errors.slice(0, 3).join(" / ") : ""));
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e.message);
    await shot("cs-fail");
  } finally {
    await browser.close(); srv.close();
    fs.rmSync(TMP, { recursive: true, force: true });
  }
  console.log(`\n${pass} passed, ${fail} failed`);
  process.exit(fail ? 1 : 0);
})();
