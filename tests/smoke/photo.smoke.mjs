// 촬영 모듈 화면 스모크 — dist/ 를 띄우고 /api/photo 와 Supabase 를 모의 응답으로 대체해 네 흐름을 끝까지 눌러 본다.
//   node tests/smoke/photo.smoke.mjs [--headed]
// 준비: `npx vite build` (dist/ 필요) · playwright(전역) + Chromium.  시험용 사진은 tests/smoke/img/*.png 를 Node 가 그린다(저장소에 넣지 않음).
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
const IMG = process.env.SMOKE_IMG || path.join(HERE, "img");
const HEADED = process.argv.includes("--headed");

// ── 모의 /api/photo ──────────────────────────────────────────────────────────
const Q = "둘레가 54cm인 직사각형의 가로의 길이가 세로의 길이보다 3cm 길 때, 이 직사각형의 넓이를 구하시오.";
const STD = { elements: { 발문: "S", 조건제시: "S", 소재맥락: "M", 도형자료: "-", 지문: "-" }, item_grade: "M", sub_type: "단순 소재 대입형", reason: "정형 상황" };
const RET = { where: "device", reason: "labels 정책 — 라벨만 저장", policy: "labels", overlap: { score: 14, level: "low", sentences: 0, words: 2, nums: 1 }, saved: true, central: false };
const calls = [];
function mockPhoto(body) {
  calls.push(body.task + (body.mode ? ":" + body.mode : ""));
  const { task, mode } = body;
  if (task === "scan" && mode === "problem") return { mode, question: Q, choices: null, qtype: "short", figure_note: null, unit_guess: "m1-1", unreadable: false, warnings: [], std: STD, policy: "labels", model: "mock" };
  if (task === "scan" && mode === "answer") return { mode, answer: "x = 세로\n2(x+3+x) = 54\n4x + 6 = 54\nx = 12\n넓이 = 15 × 12 = 180", lines: [{ text: "x = 세로", kind: "text" }, { text: "2(x+3+x) = 54", kind: "eq" }, { text: "4x + 6 = 54", kind: "eq" }, { text: "x = 12", kind: "eq" }, { text: "넓이 = 15 × 12 = 180", kind: "answer" }], final_answer: "180", legibility: { score: 3, issues: [{ kind: "glyph", note: "7을 1처럼 씀" }] }, unreadable: false, model: "mock" };
  if (task === "scan" && mode === "page") return { mode, problems: [{ no: 1, box: { x: 0.04, y: 0.04, w: 0.45, h: 0.4 } }, { no: 2, box: { x: 0.04, y: 0.5, w: 0.45, h: 0.4 } }], answers: [{ no: 1, box: { x: 0.52, y: 0.04, w: 0.44, h: 0.4 } }, { no: 2, box: { x: 0.52, y: 0.5, w: 0.44, h: 0.4 } }], model: "mock" };
  if (task === "approach") return { asking: "직사각형의 넓이", clues: [{ text: "둘레가 54cm", why: "둘레로 가로+세로의 합을 알 수 있어요" }, { text: "가로의 길이가 세로의 길이보다 3cm 길", why: "가로를 세로로 나타낼 수 있어요" }], concept: "직사각형의 둘레 = 2 × (가로 + 세로)", first_step: "세로를 x cm 라고 두기", setup: ["2(x + 3 + x) = 54"], traps: ["구하는대상혼동", "단위"], reading: "쉼표에서 한 번 끊고, 마지막 문장에서 무엇을 구하는지 확인해요.", model: "mock" };
  if (task === "essay") return { result: { rubric: [{ no: 1, element: "식 세우기", points: 3, criterion: "세로를 x로 두고 둘레 식을 세운다" }, { no: 2, element: "해 구하기", points: 3, criterion: "x = 12 를 구한다" }, { no: 3, element: "답 구하기", points: 2, criterion: "넓이 180 cm² 를 단위와 함께 쓴다" }], marks: [{ no: 1, level: "full", got: 3, comment: "식이 정확해요" }, { no: 2, level: "full", got: 3, comment: "풀이 과정이 이어져요" }, { no: 3, level: "partial", got: 1, comment: "단위가 빠졌어요" }], total: 7, max: 8, verdict: "good", final_answer_ok: true, corrections: [{ where: "마지막 줄", wrong: "180", fix: "180 cm²", why: "넓이는 단위까지 써야 해요" }], feedback: ["가로를 x+3 이라고 쓴 이유를 한 줄 적으면 더 좋아요"], pitfall_tags: ["단위"], praise: "둘레 식을 바로 세운 점이 좋아요" }, std: STD, retention: RET, model: "mock" };
  if (task === "process") return { result: { chain: [{ i: 1, text: "x = 세로", role: "setup", ok: true, note: "변수 두기" }, { i: 2, text: "2(x+3+x) = 54", role: "setup", ok: true, note: "둘레 식" }, { i: 3, text: "4x + 6 = 54", role: "transform", ok: true, note: "전개" }, { i: 4, text: "x = 12", role: "compute", ok: true, note: "이항과 나눗셈을 한 번에 — 암산" }, { i: 5, text: "넓이 = 15 × 12 = 180", role: "answer", ok: true, note: "가로 15 를 대입" }], mental_load: "mid", mental_note: "4x = 48 을 건너뛰었어요", habits: [{ kind: "glyph", note: "7을 1처럼 써요", tip: "7에 가로획을 살짝 더해요" }], error: { found: false, line: null, kind: "none", hypothesis: "", fix: "" }, criteria: { 충실성: { light: "yellow", why: "단위가 빠졌어요" }, 논리성: { light: "green", why: "단계가 이어져요" }, 명료성: { light: "green", why: "" }, 간결성: { light: "yellow", why: "암산이 한 곳" }, 독창성: { light: "green", why: "" } }, final_answer_ok: true, summary: "식은 잘 이어졌어요. 단위와 4x = 48 한 줄만 더 쓰면 완벽해요.", pitfall_tags: ["단위"] }, std: STD, retention: RET, model: "mock" };
  return { error: "unknown " + task };
}

// ── 정적 서버 (dist + SPA fallback + /api/photo) ─────────────────────────────
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ico": "image/x-icon", ".webmanifest": "application/manifest+json" };
function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, "http://x");
      if (u.pathname === "/api/photo") {
        let raw = ""; req.on("data", (c) => (raw += c)); req.on("end", () => {
          if (!/^Bearer /.test(req.headers.authorization || "")) { res.writeHead(401, { "content-type": "application/json" }); res.end(JSON.stringify({ error: "로그인이 필요해요" })); return; }
          let body = {}; try { body = JSON.parse(raw); } catch { /* 빈 몸 */ }
          setTimeout(() => { res.writeHead(200, { "content-type": "application/json" }); res.end(JSON.stringify(mockPhoto(body))); }, 120);
        });
        return;
      }
      let f = path.join(DIST, decodeURIComponent(u.pathname));
      if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f = path.join(DIST, "index.html");
      res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(0, "127.0.0.1", () => resolve({ srv, port: srv.address().port }));
  });
}

// ── Supabase 모의 (auth · rest) ───────────────────────────────────────────────
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
    if (u.pathname.startsWith("/auth/v1/factors")) return json([]);
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0];
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0" }, body: "" });
      const wantObj = accept.includes("pgrst.object");
      if (table === "profiles") return json(wantObj ? { id: USER.id, ...PROFILE } : [{ id: USER.id, ...PROFILE }]);
      if (table === "app_settings") return json([]);
      if (req.method() === "POST") return json(wantObj ? {} : []);
      return json(wantObj ? null : [], { "content-range": "0-0/0" });
    }
    return json({});
  });
  await page.addInitScript(([key, sess]) => { localStorage.setItem(key, JSON.stringify(sess)); }, ["sb-placeholder-auth-token", SESSION]);
}

// ── 스모크 ──────────────────────────────────────────────────────────────────
let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ── 시험용 사진 — 흰 바탕에 검은 선 몇 개 (내용은 상관없다, 서버가 모의이므로). 외부 의존 없이 PNG 를 직접 만든다.
function png(w, h, draw) {
  const zlib = require("node:zlib");
  const px = Buffer.alloc(w * h * 3, 255);
  draw((x, y) => { if (x >= 0 && y >= 0 && x < w && y < h) { const i = (y * w + x) * 3; px[i] = px[i + 1] = px[i + 2] = 0; } });
  const raw = Buffer.alloc((w * 3 + 1) * h);
  for (let y = 0; y < h; y++) { raw[y * (w * 3 + 1)] = 0; px.copy(raw, y * (w * 3 + 1) + 1, y * w * 3, (y + 1) * w * 3); }
  const crcTable = [...Array(256)].map((_, n) => { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; return c >>> 0; });
  const crc = (buf) => { let c = 0xffffffff; for (const b of buf) c = crcTable[(c ^ b) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
  const chunk = (type, data) => { const len = Buffer.alloc(4); len.writeUInt32BE(data.length); const td = Buffer.concat([Buffer.from(type), data]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([len, td, c]); };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 2; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  return Buffer.concat([Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]), chunk("IHDR", ihdr), chunk("IDAT", zlib.deflateSync(raw)), chunk("IEND", Buffer.alloc(0))]);
}
function ensureImages() {
  fs.mkdirSync(IMG, { recursive: true });
  const specs = { problem: [900, 500, 3], answer: [900, 700, 5], page: [1200, 1600, 12] };
  for (const [n, [w, h, lines]] of Object.entries(specs)) {
    const f = path.join(IMG, n + ".png");
    if (fs.existsSync(f)) continue;
    fs.writeFileSync(f, png(w, h, (dot) => {
      for (let x = 10; x < w - 10; x++) { dot(x, 10); dot(x, h - 11); }
      for (let y = 10; y < h - 10; y++) { dot(10, y); dot(w - 11, y); }
      for (let l = 0; l < lines; l++) { const y = 40 + l * Math.floor((h - 80) / lines); for (let x = 30; x < w * 0.6; x++) for (let t = 0; t < 3; t++) dot(x, y + t); }   // 글줄 흉내
    }));
  }
}

(async () => {
  ensureImages();
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}/`;
  const browser = await chromium.launch({ headless: !HEADED });
  const ctx = await browser.newContext({ viewport: { width: 420, height: 860 }, deviceScaleFactor: 2, hasTouch: false });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push("console: " + m.text()); });
  await mockSupabase(page);
  await page.route(/https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)\//, (r) => r.abort());   // 외부 폰트·CDN 은 스모크와 무관
  const shot = async (name) => { try { await page.screenshot({ path: path.join(HERE, "shots", name + ".png"), fullPage: true }); } catch { /* */ } };
  fs.mkdirSync(path.join(HERE, "shots"), { recursive: true });
  const go = async (h) => { await page.goto(base + h); await page.waitForLoadState("networkidle"); };
  const text = async () => (await page.locator("body").innerText()).replace(/\s+/g, " ");

  try {
    // A. 허브
    await go("#/solve");
    ok((await text()).includes("찍어서 배우기"), "허브: 문제풀이 허브에 '찍어서 배우기' 타일");
    await page.getByText("찍어서 배우기", { exact: false }).first().click();
    await page.waitForURL(/#\/solve\/photo$/);
    await page.locator(".sv-h1", { hasText: "찍어서 배우기" }).waitFor({ timeout: 10000 });   // 지연 로딩 청크가 그려질 때까지
    let t = await text();
    ok(["문장 이해하기", "표시 연습하기", "서술형 채점·첨삭", "풀이과정 검사", "내 기록"].every((s) => t.includes(s)), "허브: 촬영 모듈 타일 4 + 내 기록");
    await shot("00-hub");

    // B. 문장 이해하기 — 영역 잡기(드래그) → 인식 → 방침
    await go("#/solve/photo/read");
    await page.locator('input[type=file]').first().setInputFiles(path.join(IMG, "problem.png"));
    await page.getByRole("button", { name: /일부만 읽기/ }).click();
    const stage = page.locator(".ph-stage");
    const bb = await stage.boundingBox();
    await page.mouse.move(bb.x + bb.width * 0.1, bb.y + bb.height * 0.1);
    await page.mouse.down();
    await page.mouse.move(bb.x + bb.width * 0.8, bb.y + bb.height * 0.6, { steps: 8 });
    await page.mouse.up();
    ok(await page.locator(".ph-box").count() === 1, "읽기: 드래그로 영역 상자 1개");
    await page.getByRole("button", { name: "인식하기" }).click();
    await page.getByText("세울 식").waitFor({ timeout: 15000 });
    t = await text();
    ok(t.includes("구하는 것") && t.includes("직사각형의 넓이"), "읽기: 구하는 것");
    ok(t.includes("2(x + 3 + x) = 54"), "읽기: 세울 식(식 세우기까지)");
    ok(t.includes("끊어 읽기") && t.includes("／"), "읽기: 끊어 읽기에 빗금");
    ok(await page.locator(".sm-hilite").count() > 0, "읽기: 단서 형광펜이 문장 위에 칠해짐");
    ok(await page.locator(".sm-bound").count() > 0, "읽기: 빗금(/) 표시");
    ok(t.includes("여기서부터는 직접"), "읽기: 정답 대신 멈춤 안내");
    ok(!/\b180\b/.test(t), "읽기: 정답(180)이 화면에 없음");
    await shot("01-read");

    // C. 표시 연습 — 방금 찍은 문제로 → 차례대로 → 넘어갈까요 → 직접 표시(MarkView)
    await page.getByRole("button", { name: "이 문장으로 표시 연습" }).click();
    await page.waitForURL(/photo\/mark\?cur=1/);
    await page.getByRole("button", { name: "첫 표시 보기" }).click();
    let guard = 0;
    while (await page.getByRole("button", { name: "다음 ▶" }).count() && guard++ < 30) await page.getByRole("button", { name: "다음 ▶" }).click();
    t = await text();
    ok(t.includes("문장 이해하기로 넘어갈까요?"), "표시: 차례대로 다 보면 '문장 이해하기로 넘어갈까요?'");
    ok(await page.locator(".sm-dist").count() > 0, "표시: 구하는 것에 물결");
    await shot("02-mark");
    await page.getByRole("button", { name: "아니요, 직접 표시해 볼래요" }).click();
    ok(await page.getByRole("button", { name: "채점" }).count() === 1, "표시: 직접 표시(연습 탭)로 전환");
    await page.getByRole("button", { name: "채점" }).click();
    t = await text();
    ok(/\d+점/.test(t) && !t.includes("다른 문항") && !t.includes("이 문제 풀기"), "표시: 채점 뒤 DB 문항용 버튼 없음(사진 문항)");
    ok(t.includes("문장 이해하기로"), "표시: 채점 뒤 문장 이해하기 버튼");
    await page.getByRole("button", { name: "문장 이해하기로" }).click();
    await page.waitForURL(/photo\/read\?cur=1/);
    await page.getByText("세울 식").waitFor({ timeout: 15000 });
    ok(true, "표시→읽기: 방금 찍은 문제로 바로 이어짐(재촬영 없음)");

    // D. 서술형 채점·첨삭 — 방금 찍은 문제 → 답안 촬영 → 채점
    await go("#/solve/photo/essay?cur=1");
    t = await text();
    ok(t.includes("내 답안") && t.includes("2. 답안 찍기"), "서술형: 문제 단계 건너뛰고 답안 단계");
    await page.locator('input[type=file]').first().setInputFiles(path.join(IMG, "answer.png"));
    await page.getByRole("button", { name: "인식하기" }).click();
    await page.locator("textarea.ph-ta").waitFor({ timeout: 15000 });
    ok((await page.locator("textarea.ph-ta").inputValue()).includes("2(x+3+x) = 54"), "서술형: 전사된 답안이 편집칸에");
    await page.locator("textarea.ph-ta").fill((await page.locator("textarea.ph-ta").inputValue()) + " cm²");
    await page.getByRole("button", { name: "채점·첨삭 받기" }).click();
    await page.getByText("채점 기준표").waitFor({ timeout: 15000 });
    t = await text();
    ok(t.includes("7") && t.includes("/ 8점"), "서술형: 점수 7/8");
    ok(t.includes("첨삭") && t.includes("180 cm²"), "서술형: 첨삭(고친 것)");
    ok(t.includes("이 기기에만 저장했어요"), "서술형: 보관 안내(기기)");
    await shot("03-essay");

    // E. 풀이과정 검사 — 페이지 → 자동 상자 → 검사 → 신호등 → 첨삭 선택
    await go("#/solve/photo/check");
    await page.locator('input[type=file]').first().setInputFiles(path.join(IMG, "page.png"));
    await page.getByText("검사하기 (2문항)").waitFor({ timeout: 15000 });
    ok(await page.locator(".ph-box").count() === 4, "검사: 자동 탐지 상자 4개(문제 2 + 풀이 2)");
    // 상자 하나를 탭해 번호 조정 UI 가 뜨는지
    await page.locator(".ph-box").first().click();
    ok(await page.getByRole("button", { name: "문제↔풀이" }).count() === 1, "검사: 상자 선택 시 번호·종류 도구");
    await page.getByRole("button", { name: "문제↔풀이" }).click();
    ok((await text()).includes("검사하기 (1문항)"), "검사: 종류를 바꾸면 짝이 줄어듦(1문항)");
    await page.getByRole("button", { name: "문제↔풀이" }).click();
    ok((await text()).includes("검사하기 (2문항)"), "검사: 되돌리면 2문항");
    // 수동으로 상자 하나 더 그리기(3번 문제) → 풀이 없으면 건너뜀 안내
    await page.getByRole("button", { name: "+ 문제 영역" }).click();
    const st2 = page.locator(".ph-stage"); const b2 = await st2.boundingBox();
    await page.mouse.move(b2.x + 10, b2.y + b2.height * 0.92); await page.mouse.down();
    await page.mouse.move(b2.x + b2.width * 0.5, b2.y + b2.height * 0.99, { steps: 6 }); await page.mouse.up();
    t = await text();
    ok(await page.locator(".ph-box").count() === 5 && t.includes("풀이가 없는 문항 1개는 건너뛰어요"), "검사: 수동 상자 추가 + 짝 없는 문항 안내");
    await shot("04-check-edit");
    await page.getByRole("button", { name: /검사하기 \(2문항\)/ }).click();
    await page.getByText("서술형 첨삭으로 더 볼 문항이 있나요?").waitFor({ timeout: 30000 });
    t = await text();
    ok(t.includes("문서 전체") && (await page.locator(".ph-light.yellow").count()) >= 2, "검사: 문서 전체 신호등(노랑 포함)");
    ok(t.includes("1번") && t.includes("2번") && t.includes("암산 부담"), "검사: 문항별 카드");
    ok(t.includes("7을 1처럼"), "검사: 글씨 습관");
    await page.locator(".ph-check input").first().check();
    await page.getByRole("button", { name: "선택한 문항 첨삭받기" }).click();
    await page.locator(".ph-item .ph-rub").first().waitFor({ timeout: 15000 });
    t = await text();
    ok(t.includes("/ 8점") && t.includes("서술형 채점·첨삭"), "검사→첨삭: 선택 문항 서술형 첨삭 결과");
    ok((await page.locator(".ph-check input").count()) === 1, "검사→첨삭: 첨삭 끝난 문항은 체크칸이 사라짐");
    await shot("05-check-result");

    // F. 내 기록 — 기기 보관소
    await go("#/solve/photo/mine");
    await page.locator(".ph-rec").first().waitFor({ timeout: 10000 });
    const n = await page.locator(".ph-rec").count();
    ok(n >= 5, `기록: 기기 보관소에 ${n}건 (읽기·표시·서술형·검사2·첨삭)`);
    await page.getByRole("button", { name: "서술형", exact: true }).click();
    await sleep(400);
    const nEssay = await page.locator(".ph-rec").count();
    ok(nEssay === 2, `기록: 서술형 필터 ${nEssay}건 (서술형 화면 1 + 검사→첨삭 1)`);
    await page.locator(".ph-rec").first().click();
    await page.getByRole("button", { name: "이 기록 지우기" }).waitFor({ timeout: 5000 });
    t = await text();
    ok(t.includes("내 답안") && t.includes("채점 기준표") && t.includes("이 기기에만 저장했어요"), "기록: 서술형 상세(답안 + 기준표 + 보관 안내)");
    await page.getByRole("button", { name: "이 기록 지우기" }).click();
    await sleep(400);
    ok((await page.locator(".ph-rec").count()) === nEssay - 1, "기록: 삭제");
    await shot("06-mine");

    // G. 서버 호출 순서 확인 — 사진은 scan 에만, 문항 텍스트는 그 뒤 호출에만
    ok(calls.filter((c) => c.startsWith("scan")).length >= 6, `호출: scan ${calls.filter((c) => c.startsWith("scan")).length}회`);
    ok(calls.includes("approach") && calls.includes("essay") && calls.includes("process"), "호출: approach·essay·process 모두 사용");
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e?.message || e);
    await shot("99-error");
  }

  const realErrors = errors.filter((e) => !/favicon|manifest|\.env|VITE_SUPABASE|Failed to load resource|ERR_TUNNEL|ERR_FAILED|net::/.test(e));
  ok(realErrors.length === 0, `콘솔 오류 0건${realErrors.length ? " — " + realErrors.slice(0, 3).join(" | ") : ""}`);
  await browser.close(); srv.close();
  console.log(`\n${pass}/${pass + fail} passed`);
  process.exit(fail ? 1 : 0);
})();
