// 공부하기 › 컨셉 문제 흐름 스모크 — 목록(폴더 · 아이콘) → 세트 → 풀기 · 3단 해설(움직임) → 해설지 바로 보기 → 바로 인쇄 → 다운로드(ZIP · 각각) → OMR 사진 채점(분수 손글씨는 AI 모의)
//   → 종이처럼 풀기(타자 · 손글씨 · 보기 체크 · 빈칸 제출 · 자동 채점) → 해설 영상(조작 막대 · 목록 · 이어 보기)
//   → 일차함수 범주(폴더 · 세트 · 수 · 식 · 점 입력 · 「주어진 것 · 구할 것」 해설 · 해설지 · 손글씨 한 줄 OMR 카드 사진 채점)
//   node tests/smoke/conceptsets.smoke.mjs [--headed]
// 준비: `npx vite build` (dist/ 필요) · playwright(전역) + Chromium.
//   다운로드 확인에 쓸 PDF 가 .concept-files/prob/01/ 에 있으면(scripts/concept-files.mjs --only 01) 그걸 Storage 응답으로 쓰고, 없으면 가짜 PDF.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { layoutCard, cardHtml } from "../../src/lib/omr/grid.js";
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
let storageMode = "ok";        // ok | missing | nocors(CORS 헤더 없음 → 앱이 ?download= 링크로)
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
    // nocors: 앱의 fetch 가 막힌 상황(브라우저가 CORS 로 막으면 fetch 는 네트워크 오류) — route.fulfill 은 CORS 를 검사하지 않아 abort 로 흉내
    if (storageMode === "nocors" && !u.searchParams.has("download")) return route.abort("failed");
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
    if (b.kind === "pick") { const on = String(f).match(/[ㄱ-ㅎ]/gu) || []; for (const q of b.picks) if (on.includes(q.label)) dot(q.x, q.y, q.r - 0.8); continue; }
    if (b.kind === "line") {                                              // 일차함수: 한 줄 칸에 손글씨(식은 「y =」가 칸 밖에 인쇄돼 있다)
      const r = b.hand.num, t = String(f).replace(/^y = /, "");
      out.push(`<text x="${r.x + 10}" y="${r.y + r.h * 0.7}" font-family="cursive,sans-serif" font-style="italic" font-size="36" fill="#333" stroke="#333" stroke-width=".9">${t.replace(/&/g, "&amp;").replace(/</g, "&lt;")}</text>`);
      continue;
    }
    if (b.hand) {                                                         // 분수: 칸에 손글씨(분자 위 · 분모 아래)
      const [n, d] = String(f).split("/");
      const w = (r, t) => out.push(`<text x="${r.x + r.w / 2}" y="${r.y + r.h * 0.72}" text-anchor="middle" font-family="cursive,sans-serif" font-style="italic" font-size="${t.length > 2 ? 52 : 66}" fill="#333" stroke="#333" stroke-width="1.2">${t}</text>`);
      if (n) w(b.hand.num, n);
      if (d) w(b.hand.den, d);
      continue;
    }
    const parts = b.kind === "frac" ? (String(f).includes("/") ? String(f).split("/") : [String(f), ""]) : b.kind === "pair" ? String(f).split(/,\s*/) : [String(f)];
    b.grids.forEach((g, gi) => {
      const d = String(parts[gi] ?? "").split("");
      g.bubbles.forEach((col, ci) => { const dg = d[ci - (g.cols - d.length)]; if (dg != null && dg !== "") dot(col[+dg].x, col[+dg].y, g.r - 0.8); });
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
      .ph{transform:perspective(1600px) rotateX(${p.index % 2 ? 7 : -5}deg) rotateY(${p.index % 2 ? -4 : 3}deg) rotateZ(${p.index % 2 ? 182 : -2.5}deg);background:#fff;box-shadow:0 8px 30px rgba(0,0,0,.4)}
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
    // A. 공부하기 › 컨셉 문제 › 경우의 수와 확률 — 아이콘 120개
    await page.goto(base + "#/study/sets");
    await page.locator(".st-folder").first().waitFor({ timeout: 20000 });
    ok(await page.locator(".sh-stab.on", { hasText: "컨셉 문제" }).count() === 1, "A1 서브탭 「컨셉 문제」 활성");
    await page.locator(".st-folder", { hasText: "종 ·" }).first().waitFor({ timeout: 10000 }).catch(() => {});
    const folder = (await page.locator(".st-folder").first().innerText()).replace(/\s+/g, " ");
    ok(/경우의 수와 확률/.test(folder) && /120종 · 6,000문항/.test(folder), `A2 범주 폴더 · 세트 수는 index 에서 (${folder})`);
    await page.locator(".st-folder").first().click();
    await page.locator(".st-ic").first().waitFor({ timeout: 10000 });
    ok(await page.locator(".st-ic").count() === 120, "A3 세트 아이콘 120개");
    const groups = await page.locator(".st-sec").allInnerTexts();
    ok(groups.length === 12 && ["스포츠", "한국사", "유럽사", "중국사", "일본사", "사회", "과학", "애니메이션", "웹툰"].every((w) => groups.some((g) => g.includes(w))), `A4 묶음 12개 — 역사는 지역별 (${groups.join(" | ")})`);
    await shot("cs-icons");

    // B. 세트 화면
    await page.locator(".st-ic", { hasText: "야구" }).click();
    await page.locator(".cs-hero").waitFor({ timeout: 10000 });
    let t = await text();
    ok(/야구로 익히는 경우의 수와 확률/.test(t) && (await page.locator(".cs-row").count()) === 50, "B1 세트 머리 · 문항 50");
    const omrChip = (await page.locator(".cs-dchip", { hasText: "OMR" }).innerText()).replace(/\s+/g, " ");
    ok((await page.locator(".cs-dchip").count()) === 3 && /9쪽/.test(t) && /19쪽/.test(t) && /3쪽/.test(omrChip), `B2 자료 칩 3개 + 쪽 수(문제 · 해설은 files.json, OMR 은 카드 배치) (${omrChip})`);
    ok(/OMR 카드\(3쪽\)/.test(t) && /분수는 칸에 손으로/.test(t), "B2b OMR 채점 안내: 3쪽 · 분수는 손으로");
    await page.locator(".cs-chip", { hasText: /^상$/ }).click();
    ok((await page.locator(".cs-row").count()) === 10, "B3 「상」 거르기 → 10");
    await page.locator(".cs-chip", { hasText: "전체" }).click();
    await shot("cs-set");

    // C. 풀기 — 오답 → 해설(3단 + 움직임) → 다시 풀기 → 정답
    await page.locator(".cs-go2 .sv-btn", { hasText: "한 문제씩" }).click();
    await page.locator(".cs-q").waitFor({ timeout: 10000 });
    ok(/#\/sets\/prob\/01\/q\/1$/.test(page.url()), "C1 한 문제씩 풀기 → 1번");
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
    ok((await page.locator(".cs-vlink", { hasText: "해설 영상" }).count()) === 1, "C6b 해설 아래 「이 문제 해설 영상으로 보기」");
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

    // S. 해설지 바로 보기 — 빠른 정답 50칸 · 번호 칸 누르면 그 해설로 · 번호로 가기
    await page.locator(".cs-go2 .sv-btn", { hasText: "해설지 보기" }).click();
    await page.locator(".cs-paperhost .keyt td.n").first().waitFor({ timeout: 15000 });
    ok(/#\/sets\/prob\/01\/sol$/.test(page.url()) && (await page.locator(".cs-paperhost .keyt td.n").count()) === 50, `S1 해설지 화면 · 빠른 정답 50칸 (${await page.locator(".cs-paperhost .keyt td.n").count()})`);
    const keyFit = await page.evaluate(() => { const t = document.querySelector(".cs-paperhost").shadowRoot.querySelector(".keyt"); const r = t.getBoundingClientRect(); return r.right <= innerWidth + 1 && r.left >= -1; });
    ok(keyFit, "S2 휴대폰 폭에서 빠른 정답 표가 화면 안에(폭 맞춤)");
    await shot("cs-sol-view");
    const inView = (no) => page.evaluate((id) => { const el = document.querySelector(".cs-paperhost").shadowRoot.getElementById("s-" + id); if (!el) return null; const r = el.getBoundingClientRect(); return r.top > -40 && r.top < innerHeight * 0.6; }, SET.items[no - 1].id);
    await page.locator(".cs-paperhost .keyt td.n", { hasText: /^37$/ }).click();
    await sleep(1200);
    ok(await inView(37), "S3 빠른 정답의 37 → 37번 해설로");
    await page.locator(".cs-pbar2 .cs-tb", { hasText: "번호로 가기" }).click();
    await page.locator(".cs-jump .cs-jn").first().waitFor({ timeout: 5000 });
    ok((await page.locator(".cs-jump .cs-jn").count()) === 50, "S4 번호로 가기 50칸");
    await page.locator(".cs-jump .cs-jn", { hasText: /^12$/ }).click();
    await sleep(1200);
    ok(await inView(12), "S5 번호로 가기 12 → 12번 해설");
    await page.goto(base + "#/sets/prob/01");
    await page.locator(".cs-hero").waitFor({ timeout: 10000 });

    // F. 바로 인쇄 — 문제지 + 해설지 + OMR 한 창
    const chip = (l) => page.locator(".cs-dchip", { hasText: l });
    if (!(await chip("해설지").getAttribute("aria-pressed")).includes("true")) await chip("해설지").click();
    if (!(await chip("문제지").getAttribute("aria-pressed")).includes("true")) await chip("문제지").click();
    if (!(await chip("OMR").getAttribute("aria-pressed")).includes("true")) await chip("OMR").click();
    const [pop] = await Promise.all([ctx.waitForEvent("page"), page.locator(".cs-dbtns .sv-btn", { hasText: "바로 인쇄" }).click()]);
    // window.open("") 빈 창에는 초기화 스크립트가 늦게 붙을 수 있어 바로 덮는다(document.open 뒤에도 같은 window)
    await pop.evaluate(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; }).catch(() => {});
    await pop.waitForFunction(() => document.querySelectorAll(".omr-pg").length === 3 && document.querySelector(".cs-doc"), null, { timeout: 15000 });
    const info = await pop.evaluate(() => ({ pg: document.querySelectorAll(".csx-p .pg").length, spg: document.querySelectorAll(".csx-s .spg").length, omr: document.querySelectorAll(".omr-pg").length, title: document.title }));
    ok(info.pg === 9 && info.spg === 19 && info.omr === 3, `F1 인쇄 창: 문제 ${info.pg}쪽 · 해설 ${info.spg}쪽 · OMR ${info.omr}쪽`);
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
    {
      // 받는 방식 「파일 각각」 — PDF 두 개가 따로
      await page.locator(".cs-dlmode .cs-modes button", { hasText: "파일 각각" }).click();
      const got = [];
      const on = (d) => got.push(d.suggestedFilename());
      page.on("download", on);
      await page.locator(".cs-dbtns .sv-btn", { hasText: "다운로드" }).click();
      for (let i = 0; i < 40 && got.length < 2; i++) await sleep(150);
      await sleep(300);
      page.off("download", on);
      ok(got.join("|") === "01-야구-문제.pdf|01-야구-OMR.pdf", `G2b 받는 방식 「파일 각각」 → PDF ${got.length}개 (${got.join(", ")})`);
      await page.locator(".cs-dlmode .cs-modes button", { hasText: "ZIP" }).click();
    }
    storageMode = "missing";
    await page.locator(".cs-dbtns .sv-btn", { hasText: "다운로드" }).click();
    // 앞 단계의 안내(토스트)가 아직 떠 있을 수 있어 이 안내 글자가 뜰 때까지 기다린다
    const g3 = await page.locator(".cs-toast", { hasText: "아직 올라가지 않았어요" }).waitFor({ timeout: 12000 }).then(() => true).catch(() => false);
    ok(g3, "G3 파일이 없으면 안내(바로 인쇄로 PDF 저장)");
    storageMode = "nocors";
    await chip("OMR").click();                                           // 문제지만
    [dl] = await Promise.all([page.waitForEvent("download", { timeout: 10000 }), page.locator(".cs-dbtns .sv-btn", { hasText: "다운로드" }).click()]);
    ok(dl.suggestedFilename() === "01-야구-문제.pdf" && /download=/.test(dl.url()), `G4 받아 오기가 막히면 서버 링크(?download=)로 → ${dl.suggestedFilename()} ${dl.url().slice(0, 50)}`);
    storageMode = "ok";

    // H. OMR 사진 채점 — 정답대로 칠하되 3문항 틀리게 · 분수 1문항 비움. 분수는 손글씨 칸 → 그 칸만 잘라 AI(모의)가 읽는다
    const card = layoutCard({ cat: "prob", no: SET.no, title: SET.title, items: SET.items });
    const fills = Object.fromEntries(SET.items.map((it) => [it.no, rawOf(it)]));
    const ints = SET.items.filter((it) => it.a.k === "int" && it.a.v < 900).slice(2, 5);
    for (const it of ints) fills[it.no] = String(it.a.v + 1);
    const blankNo = SET.items.find((it) => it.a.k === "frac" && it.no > 30).no;
    fills[blankNo] = "";
    const photos = await cardPhotos(browser, card, fills);
    const omrCalls = [];
    const omrAi = async (r) => {
      const body = JSON.parse(r.request().postData() || "{}");
      const nos = (body.items || []).map((it) => it.no);
      omrCalls.push({ nos, img: typeof body.image === "string" ? body.image.length : 0, task: body.task });
      // 모의 AI: 보낸 번호의 손글씨를 「쓴 대로」 돌려준다(실제로는 잘라 보낸 조각을 읽는다)
      r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ answers: nos.map((no) => ({ no, answer: fills[no] || "" })) }) });
    };
    await page.route("**/api/ai", omrAi);
    await page.goto(base + "#/sets/prob/01/omr");
    await page.locator(".cs-shot").waitFor({ timeout: 10000 });
    await page.locator('input[type=file][multiple]').setInputFiles(photos);
    await page.locator(".cs-pg.on").nth(2).waitFor({ timeout: 40000 });
    for (let i = 0; i < 60 && (await page.locator('.cs-orow input[placeholder="읽는 중…"]').count()); i++) await sleep(200);
    await page.locator(".cs-busy").waitFor({ state: "detached", timeout: 20000 }).catch(() => {});
    ok((await page.locator(".cs-pg.on").count()) === 3 && (await page.locator(".cs-prv img").count()) === 3, "H1 세 쪽 모두 읽음(2쪽은 거꾸로 찍음) + 미리보기");
    const vals = await page.locator(".cs-orow input").evaluateAll((els) => els.map((e) => e.value));
    const want = SET.items.map((it) => fills[it.no]);
    const diff = want.map((w, i) => (w === vals[i] ? null : `${i + 1}:${vals[i]}≠${w}`)).filter(Boolean);
    ok(diff.length === 0, `H2 읽은 답 = 칠하고 쓴 답 50/50 ${diff.length ? diff.slice(0, 6).join(" ") : ""}`);
    const handNos = SET.items.filter((it) => it.a.k === "frac" && fills[it.no]).map((it) => it.no);
    const sent = omrCalls.flatMap((c) => c.nos).sort((a, b) => a - b);
    ok(omrCalls.length === 3 && omrCalls.every((c) => c.task === "omr" && c.img > 2000) && JSON.stringify(sent) === JSON.stringify(handNos),
      `H2b 손글씨 분수만 쪽마다 한 번씩 AI로(빈 분수 칸 ${blankNo}번은 안 보냄) — ${omrCalls.length}번 · ${sent.length}칸`);
    ok((await page.locator(".cs-orow.ai").count()) === handNos.length && (await page.locator(".cs-ainote").count()) === 1, "H2c AI가 읽은 칸 표시 · 안내");
    await shot("cs-omr-confirm");
    await page.unroute("**/api/ai", omrAi);
    await page.locator(".cs-gradebtn").click();
    await page.locator(".cs-score").waitFor({ timeout: 10000 });
    const score = await page.locator(".cs-score .big b").innerText();
    ok(score === "46", `H3 채점 46/50 (${score})`);
    ok((await page.locator(".cs-rrow").count()) === 4, "H4 틀린 문항 4개 목록");
    await shot("cs-omr-result");
    await page.locator(".cs-rrow").first().click();
    await page.locator(".cs-q").waitFor({ timeout: 10000 });
    ok(/지난 기록/.test(await text()), "H5 틀린 문항 → 문항 화면(지난 기록 표시)");

    // P. 종이처럼 풀기 — 문제지 그대로 · 타자 · 손글씨(분수) · 보기 체크(여러 개 · 다시 누르면 해제) · 빈칸 그냥 제출 → 자동 채점
    let aiCalls = 0, aiItems = [];
    await page.route("**/api/ai", async (r) => {
      aiCalls++;
      const body = JSON.parse(r.request().postData() || "{}");
      aiItems = body.items || [];
      const okImg = body.task === "omr" && typeof body.image === "string" && body.image.length > 1000;
      r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ answers: aiItems.map((it) => ({ no: it.no, answer: okImg && it.no === 6 ? "5/12" : "" })) }) });
    });
    await page.goto(base + "#/sets/prob/01");
    await page.locator(".cs-go").waitFor({ timeout: 10000 });
    ok(/바로 풀기 · 문제지 그대로/.test(await page.locator(".cs-go").innerText()), "P1 세트 첫 단추 = 바로 풀기(문제지 그대로)");
    await page.locator(".cs-go").click();
    await page.locator(".cs-paperhost .pg").first().waitFor({ timeout: 20000 });
    ok((await page.locator(".cs-paperhost .pg").count()) === 9 && /\/paper$/.test(page.url()), "P2 문제지 9쪽을 그대로 펼침");
    // 1번: 타자
    await page.locator(".q#H1").click();
    await page.locator(".cs-sheet").waitFor();
    await page.locator(".cs-modes button", { hasText: "타자" }).click();
    await page.locator(".cs-sheet .cs-ii").fill("12");
    await page.locator(".cs-sheet .sv-btn.pri", { hasText: "확인" }).click();
    await sleep(300);
    ok(/12/.test(await page.locator(".q#H1 .ans i").innerText()), "P3 타자 답이 문제지 괄호 안에");
    // 6번: 손글씨(분수 5/12)
    await page.locator(".q#H6").click();
    await page.locator(".cs-sheet").waitFor();
    await page.locator(".cs-modes button", { hasText: "손글씨" }).click();
    const pad = page.locator(".cs-pad"); const bb = await pad.boundingBox();
    const stroke = async (pts) => { await page.mouse.move(bb.x + pts[0][0], bb.y + pts[0][1]); await page.mouse.down(); for (const q of pts.slice(1)) await page.mouse.move(bb.x + q[0], bb.y + q[1], { steps: 4 }); await page.mouse.up(); };
    const cx = bb.width / 2;
    await stroke([[cx + 14, 30], [cx - 6, 30], [cx - 8, 56], [cx + 10, 54], [cx + 16, 70], [cx + 8, 90], [cx - 10, 88]]);
    await stroke([[cx - 22, 140], [cx - 16, 132], [cx - 16, 200]]);
    await stroke([[cx + 2, 145], [cx + 14, 134], [cx + 26, 142], [cx + 22, 162], [cx + 2, 198], [cx + 30, 198]]);
    await page.locator(".cs-sheet .sv-btn.pri", { hasText: "확인" }).click();
    await sleep(300);
    ok((await page.locator(".q#H6 .ans i svg.cs-ink path").count()) === 3, "P4 손글씨(획 3개)가 괄호 안에 연필 글씨로");
    // 31번: 보기 — 셋을 체크, 하나 해제, 다시 체크
    // 체크는 다음 그리기에서 문제지에 얹힌다 — 개수가 맞을 때까지 잠깐 기다려 센다
    const checks = async (n) => { for (let i = 0; i < 20; i++) { const c = await page.locator(".q#M16 .cs-check").count(); if (c === n) return c; await sleep(100); } return page.locator(".q#M16 .cs-check").count(); };
    for (const lab of ["ㄱ", "ㄴ", "ㄷ"]) await page.locator(`.q#M16 p.cs-pk[data-pk="${lab}"]`).click();
    const c3 = await checks(3);
    await page.locator(`.q#M16 p.cs-pk[data-pk="ㄴ"]`).click();
    const c2 = await checks(2);
    await page.locator(`.q#M16 p.cs-pk[data-pk="ㄴ"]`).click();
    const c3b = await checks(3);
    ok(c3 === 3 && c2 === 2 && c3b === 3, `P5 보기 여러 개 체크 · 다시 누르면 해제 (${c3} → ${c2} → ${c3b})`);
    // 빈칸 47개인 채로 제출 → 손글씨는 AI 로 읽고 채점
    await page.locator(".cs-submit").click();
    await page.locator(".cs-gsum").waitFor({ timeout: 15000 });
    await sleep(500);
    ok((await page.locator(".cs-gsum > b").innerText()) === "3/50" && aiCalls === 1 && JSON.stringify(aiItems) === JSON.stringify([{ no: 6, type: "short" }]),
      `P6 빈칸이 있어도 제출 → 3/50 · 손글씨만 판독 1번 (${aiCalls}, ${JSON.stringify(aiItems)})`);
    const marks = await page.locator(".cs-paperhost .cs-mark").count(), keys = await page.locator(".cs-paperhost .cs-key").count();
    ok(marks === 50 && keys === 47 && (await page.locator(".cs-paperhost .cs-score").count()) === 1, `P7 동그라미 · 빗금 50 · 정답 글씨 47 · 점수 (${marks}, ${keys})`);
    await page.evaluate(() => window.scrollTo(0, 0));
    await shot("cs-paper-graded");
    await page.locator(".q#H2").click();
    await page.locator(".cs-solsheet").waitFor({ timeout: 5000 });
    ok(/틀렸어요/.test(await page.locator(".cs-solsheet .iv-verdict").innerText()) && (await page.locator(".cs-solsheet .cs-tg").count()) === 3, "P8 채점 뒤 문항을 누르면 해설 시트(3단)");
    await page.locator(".cs-solsheet .sv-btn", { hasText: "영상" }).click();

    // V. 해설 영상 — 그 문항부터 · 조작 막대 · 다음 · 목록 · 이어 보기 · 나가기
    await page.locator(".dsp-svg").waitFor({ timeout: 15000 });
    const aria = async () => (await page.locator(".dsp-svg").getAttribute("aria-label")) || "";
    ok(/— 2\. /.test(await aria()) && (await page.evaluate(() => location.hash)) === "#/sets/prob/01/video", `V1 해설 시트 → 영상 2번부터 · 주소의 ?no 는 지움 (${await aria()})`);
    ok((await page.locator(".dsp-ctl.show .dsp-btn").count()) === 8, "V2 조작 막대(이전 · 멈춤 · 다음 · 반복 · 밝기 · 전체 화면 · 목록 · 나가기)");
    await shot("cs-video");
    const prog0 = await page.locator(".dsp-prog i").getAttribute("style");
    await sleep(4300);
    const prog1 = await page.locator(".dsp-prog i").getAttribute("style");
    const sx = (st) => Number((String(st).match(/scaleX\(([\d.e-]+)\)/) || [])[1] || 0);
    ok((await page.locator(".dsp-ctl.show").count()) === 0 && sx(prog1) > sx(prog0), `V3 가만히 두면 막대가 숨고 영상은 흐른다 (${sx(prog0).toFixed(3)} → ${sx(prog1).toFixed(3)})`);
    await page.mouse.move(200, 300);
    await page.locator(".dsp-ctl.show").waitFor({ timeout: 3000 });
    await page.locator(".dsp-ctl .dsp-btn[title^='다음']").click();
    await sleep(300);
    ok(/— 3\. /.test(await aria()), "V4 다음 → 3번");
    await page.keyboard.press("l");
    await page.locator(".dsp-list .dsp-card").first().waitFor({ timeout: 3000 });
    ok((await page.locator(".dsp-list .dsp-card").count()) === 50 && (await page.locator(".dsp-list .dsp-card.on .n").innerText()) === "3", "V5 목록(L) 50문항 · 지금 문항 표시");
    await page.locator(".dsp-list .dsp-card").nth(19).click();
    await sleep(300);
    ok(/— 20\. /.test(await aria()) && (await page.locator(".dsp-list").count()) === 0, "V6 목록에서 고르면 그 문항부터");
    await page.reload();
    await page.locator(".dsp-svg").waitFor({ timeout: 15000 });
    ok(/— 20\. /.test(await aria()), "V7 새로고침해도 그 자리에서 이어서(벽시계)");
    await page.mouse.move(220, 320);
    await page.locator(".dsp-ctl .dsp-btn[title^='나가기']").click();
    await page.locator(".cs-hero").waitFor({ timeout: 10000 });
    ok(/#\/sets\/prob\/01$/.test(page.url()) && /채점한 문제지 보기 · 3\/50/.test(await page.locator(".cs-go").innerText()), "V8 나가기 → 세트 화면(문제지 채점 기록 유지)");

    // L. 일차함수와 그래프(lin) — 범주 폴더 · 세트 · 한 문제씩(수 · 식 · 점) · 해설 이름표 · 해설지 · 손글씨 한 줄 OMR
    {
      const LDIR = path.join(DIST, "concept-sets/lin");
      const LCAT = JSON.parse(fs.readFileSync(path.join(LDIR, "index.json"), "utf8")).categories[0];
      const nn = String(LCAT.sets[0].no).padStart(2, "0");
      const LS = JSON.parse(fs.readFileSync(path.join(LDIR, `${nn}.json`), "utf8"));
      const nItems = LCAT.sets.reduce((a, x) => a + x.n, 0);
      await page.goto(base + "#/study/sets");
      await page.locator(".st-folder").nth(1).waitFor({ timeout: 10000 });
      await page.locator(".st-folder", { hasText: "종 ·" }).nth(1).waitFor({ timeout: 10000 }).catch(() => {});
      const lf = (await page.locator(".st-folder").nth(1).innerText()).replace(/\s+/g, " ");
      ok((await page.locator(".st-folder").count()) === 2 && /일차함수와 그래프/.test(lf) && lf.includes(`${LCAT.sets.length}종 · ${nItems.toLocaleString("ko-KR")}문항`), `L1 두 번째 범주 폴더 「일차함수와 그래프」 (${lf})`);
      await page.locator(".st-folder").nth(1).click();
      await page.locator(".st-ic").first().waitFor({ timeout: 10000 });
      const lg = await page.locator(".st-sec").allInnerTexts();
      ok((await page.locator(".st-ic").count()) === LCAT.sets.length && lg.length === LCAT.groups.length && lg.every((g) => /과학 [12]-[12]/.test(g)), `L2 세트 아이콘 ${LCAT.sets.length}개 · 묶음 ${lg.join(" | ")}`);
      await shot("cs-lin-icons");
      await page.locator(".st-ic").first().click();
      await page.locator(".cs-hero").waitFor({ timeout: 10000 });
      const lcard = layoutCard({ cat: "lin", no: LS.no, title: LS.title, items: LS.items });
      const lt = await text();
      ok(lt.includes(LS.title) && (await page.locator(".cs-row").count()) === 50 && lt.includes(`OMR 카드(${lcard.pages.length}쪽)`) && /수 · 식 · 점/.test(lt), `L3 세트 화면 · 문항 50 · OMR ${lcard.pages.length}쪽 안내`);
      await shot("cs-lin-set");
      // 식 답: 오답 → 해설(주어진 것 · 구할 것) → 다시 → 정답(ASCII · y= 없이)
      const LI = LS.items.find((it) => it.a.k === "lin");
      const asc = (x) => String(x).replace(/−/g, "-").replace(/\s+/g, "");
      await page.goto(base + `#/sets/lin/${nn}/q/${LI.no}`);
      await page.locator(".cs-xi").waitFor({ timeout: 10000 });
      ok((await page.locator(".cs-xkeys button").count()) === 6, "L4 식 입력 칸 · 기호 단추 6개");
      await page.locator(".cs-xkeys button", { hasText: /^y =$/ }).click();
      await page.locator(".cs-xi").type("100x+1");
      ok(/읽은 꼴\s*y = 100x \+ 1/.test(await page.locator(".cs-xprev").innerText()), "L5 기호 단추로 「y =」 넣기 · 읽은 꼴 미리 보기");
      await page.locator(".cs-sub").click();
      await page.locator(".iv-banner.bad").waitFor({ timeout: 5000 });
      await page.locator(".iv-row .sv-btn", { hasText: "해설 보기" }).click();
      await page.locator(".cs-sol").waitFor({ timeout: 5000 });
      const solT = await page.locator(".cs-sol").innerText();
      ok(/주어진 것/.test(solT) && /구할 것/.test(solT) && !/포지티브/.test(solT), "L6 해설 방침 = 주어진 것 · 구할 것");
      await shot("cs-lin-solution");
      await page.locator(".cs-retry").click();
      await page.locator(".cs-xi:not([disabled])").fill(asc(rawOf(LI)).replace(/^y=/, ""));
      await page.locator(".cs-sub").click();
      await page.locator(".iv-banner.ok").waitFor({ timeout: 5000 });
      ok(true, `L7 식 ${asc(rawOf(LI)).replace(/^y=/, "")} (y = 없이 · - 마이너스) → 정답`);
      // 수 · 점 답
      for (const k of ["num", "pt"]) {
        const it = LS.items.find((x) => x.a.k === k);
        if (!it) continue;
        await page.goto(base + `#/sets/lin/${nn}/q/${it.no}`);
        await page.locator(".cs-xi").waitFor({ timeout: 10000 });
        await page.locator(".cs-xi").fill(asc(rawOf(it)) + (k === "num" && it.a.u ? it.a.u : ""));
        await page.locator(".cs-sub").click();
        const okb = await page.locator(".iv-banner.ok").waitFor({ timeout: 5000 }).then(() => true).catch(() => false);
        ok(okb, `L8 ${k === "num" ? "수" : "점"} ${asc(rawOf(it))}${k === "num" && it.a.u ? it.a.u : ""} → 정답`);
      }
      // 해설지 바로 보기
      await page.goto(base + `#/sets/lin/${nn}/sol`);
      await page.locator(".cs-paperhost .keyt td.n").first().waitFor({ timeout: 15000 });
      ok((await page.locator(".cs-paperhost .keyt td.n").count()) === 50, "L9 일차함수 해설지 · 빠른 정답 50칸");
      // OMR: 정답대로 쓰되 식 하나 · 수 하나는 틀리게, 보기 하나는 비움
      const lf2 = Object.fromEntries(LS.items.map((it) => [it.no, rawOf(it)]));
      const wrongL = LS.items.find((it) => it.a.k === "lin" && it.no !== LI.no), wrongN = LS.items.find((it) => it.a.k === "num");
      lf2[wrongL.no] = "y = 100x + 1"; lf2[wrongN.no] = "9999";
      const blankP = LS.items.find((it) => it.a.k === "pick");
      if (blankP) lf2[blankP.no] = "";
      const lphotos = await cardPhotos(browser, lcard, lf2);
      const lcalls = [];
      const linAi = async (r) => {
        const body = JSON.parse(r.request().postData() || "{}");
        const nos = (body.items || []).map((it) => it.no);
        lcalls.push(nos);
        r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ answers: nos.map((no) => ({ no, answer: asc(lf2[no] || "").replace(/^y=/, "") })) }) });
      };
      await page.route("**/api/ai", linAi);
      await page.goto(base + `#/sets/lin/${nn}/omr`);
      await page.locator(".cs-shot").waitFor({ timeout: 10000 });
      await page.locator('input[type=file][multiple]').setInputFiles(lphotos);
      await page.locator(".cs-pg.on").nth(lcard.pages.length - 1).waitFor({ timeout: 40000 });
      for (let i = 0; i < 60 && (await page.locator('.cs-orow input[placeholder="읽는 중…"]').count()); i++) await sleep(200);
      await page.locator(".cs-busy").waitFor({ state: "detached", timeout: 20000 }).catch(() => {});
      const lv = await page.locator(".cs-orow input").evaluateAll((els) => els.map((e) => e.value));
      const lwant = LS.items.map((it) => (it.a.k === "pick" ? lf2[it.no] : asc(lf2[it.no] || "").replace(/^y=/, "")));
      const ldiff = lwant.map((w, i) => (w === lv[i] ? null : `${i + 1}:${lv[i]}≠${w}`)).filter(Boolean);
      const handN = LS.items.filter((it) => it.a.k !== "pick" && lf2[it.no]).length;
      ok((await page.locator(".cs-pg.on").count()) === lcard.pages.length && ldiff.length === 0 && lcalls.flat().length === handN && lcalls.length >= lcard.pages.length,
        `L10 손글씨 한 줄 칸은 쪽마다 한 번 AI로 · 보기는 기기에서 — 50/50 (${ldiff.slice(0, 4).join(" ")}) · AI ${lcalls.length}번 ${lcalls.flat().length}칸`);
      await shot("cs-lin-omr-confirm");
      await page.unroute("**/api/ai", linAi);
      await page.locator(".cs-gradebtn").click();
      await page.locator(".cs-score").waitFor({ timeout: 10000 });
      const ls = await page.locator(".cs-score .big b").innerText();
      const lexp = 50 - 2 - (blankP ? 1 : 0);
      ok(ls === String(lexp), `L11 채점 ${lexp}/50 (${ls})`);
      // 종이처럼 풀기 — 일차함수 문제지 · 식 답을 타자로(ASCII) → 빈칸이 있어도 제출 → 1/50
      const noAi = (r) => r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ answers: [] }) });
      await page.route("**/api/ai", noAi);
      await page.goto(base + `#/sets/lin/${nn}/paper`);
      await page.locator(".cs-paperhost .pg").first().waitFor({ timeout: 20000 });
      const lpg = await page.locator(".cs-paperhost .pg").count();
      ok(lpg === LCAT.sets[0].pages.problems, `L12 일차함수 문제지 ${lpg}쪽을 그대로 펼침`);
      const hid = `#${LI.id}`;
      await page.locator(`.q${hid}`).click();
      await page.locator(".cs-sheet").waitFor();
      if (await page.locator(".cs-modes button", { hasText: "타자" }).count()) await page.locator(".cs-modes button", { hasText: "타자" }).click();
      await page.locator(".cs-sheet .cs-xi").fill(asc(rawOf(LI)));
      await page.locator(".cs-sheet .sv-btn.pri", { hasText: "확인" }).click();
      await sleep(300);
      await page.locator(".cs-submit").click();
      await page.locator(".cs-gsum").waitFor({ timeout: 15000 });
      await sleep(400);
      ok((await page.locator(".cs-gsum > b").innerText()) === "1/50", `L13 식 답을 타자로 써서 제출 → 1/50 (${await page.locator(".cs-gsum > b").innerText()})`);
      await page.unroute("**/api/ai", noAi);
    }

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
