// 게임(#/admin/games) 스모크 — 기울기 샷(포켓볼 · 사구 · 컬링)을 실제 브라우저로 쳐 본다.
//   node tests/smoke/games.smoke.mjs [--headed]     빌드 후(dist/ 필요): 관리자 확인 · iframe · 테마 전달 + 게임 검사
//   node tests/smoke/games.smoke.mjs --game-only    빌드 없이 게임 HTML 만 바로 열어 게임 검사
// 준비: playwright + Chromium. 게임 검사에 찬스 풍선을 기다리는 몫(최대 25초)이 있어 1분 남짓 걸린다.
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
const GAME = path.join(ROOT, "src/features/games/slope-shot.html");
const HEADED = process.argv.includes("--headed");
const GAME_ONLY = process.argv.includes("--game-only");
const SHOTS = process.env.SMOKE_SHOTS || path.join(HERE, "shots");

// ── 정적 서버 (dist/ 또는 게임 HTML 하나) ──
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ico": "image/x-icon", ".webmanifest": "application/manifest+json" };
function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, "http://x");
      let f;
      if (GAME_ONLY) f = GAME;
      else {
        f = path.join(DIST, decodeURIComponent(u.pathname));
        if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f = path.join(DIST, "index.html");
      }
      res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(0, "127.0.0.1", () => resolve({ srv, port: srv.address().port }));
  });
}

// ── Supabase 모의 — 역할만 바꿔 가며 ──
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const USER = { id: "00000000-0000-4000-8000-000000000001", aud: "authenticated", role: "authenticated", email: "smoke@example.com", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: {}, factors: [], created_at: "2026-01-01T00:00:00Z" };
const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], app_metadata: USER.app_metadata, user_metadata: {}, session_id: "s1" })}.sig`;
const SESSION = { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r1", user: USER };
let ROLE = "student";
const profile = () => ({ id: USER.id, role: ROLE, member_code: "SMOKE", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "1990-03-01", settings: {} });

async function mockSupabase(page) {
  await page.route("https://placeholder.supabase.co/**", (route) => {
    const req = route.request(); const u = new URL(req.url()); const accept = req.headers()["accept"] || "";
    const json = (obj, headers = {}) => route.fulfill({ status: 200, contentType: "application/json", headers, body: JSON.stringify(obj) });
    if (u.pathname.startsWith("/auth/v1/user")) return json(USER);
    if (u.pathname.startsWith("/auth/v1/token")) return json(SESSION);
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/storage/v1/object/list")) return json([]);   // 대시보드 우물 이미지 목록
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0];
      const wantObj = accept.includes("pgrst.object");
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0", "access-control-expose-headers": "content-range" }, body: "" });
      if (table === "profiles") return json(wantObj ? profile() : [profile()]);
      if (req.method() === "POST") return json(wantObj ? {} : []);
      return json(wantObj ? null : [], { "content-range": "0-0/0" });
    }
    return json({});
  });
  await page.addInitScript(([key, sess]) => {
    if (window.top !== window) return;        // 게임 iframe(샌드박스)에서는 저장소가 막혀 있다
    localStorage.setItem(key, JSON.stringify(sess));
    if (!localStorage.getItem("ashrain-theme")) localStorage.setItem("ashrain-theme", "light");
  }, ["sb-placeholder-auth-token", SESSION]);
}

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };

// ── 게임 검사 — fr: 게임 문서가 든 프레임 ──
async function gameChecks(fr, shot) {
  const S = () => fr.evaluate(() => window.__slopeShot());
  const txt = async (sel) => ((await fr.locator(sel).innerText()) || "").replace(/\s+/g, " ").trim();
  const report = () => txt("#report");
  const num = (v) => String(Math.round(v * 10000) / 10000);
  async function setStep(k, target) {
    for (let i = 0; i < 20; i++) {
      const cur = (await S())[k];
      if (cur === target) return;
      await fr.locator(`[data-step="${k}"][data-d="${cur < target ? 1 : -1}"]`).click();
    }
  }
  const setIcpt = (v) => fr.locator("#icpt").fill(typeof v === "number" ? num(v) : v);
  async function live() { if ((await S()).over) await fr.locator("#newGame").click(); }
  async function shoot() {
    const n = (await S()).shots;
    await fr.locator("#shoot").click();
    await fr.waitForFunction((k) => { const s = window.__slopeShot(); return s.shots === k && !s.moving; }, n + 1, { timeout: 30000, polling: 100 });
    return report();
  }
  const back = async () => { await fr.locator("#back").click(); await fr.locator("#lobby").waitFor(); };
  const open = async (g, p) => { await fr.locator(`.open[data-game="${g}"][data-players="${p}"]`).click(); await fr.locator("#game").waitFor(); };
  // 공(스톤) o 가 (x0, y0)에서 x 방향으로 [y0 + lo, y0 + hi] 띠를 지나는 길에 있는가
  const inBand = (bodies, me, x0, x1, y0, lo, hi) => bodies.some((o) => o.id !== me && o.x > x0 - 0.7 && o.x < x1 + 0.7 && o.y > y0 + lo - 0.7 && o.y < y0 + hi + 0.7);

  // G. 게임 목록
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  ok((await fr.locator(".card").count()) === 3 && (await fr.locator(".open").count()) === 6, "G1 게임 목록 — 카드 3장 · 단추 6개(혼자 · 둘이)");
  const drawn = await fr.evaluate(() => [...document.querySelectorAll(".card canvas")].every((c) => {
    const d = c.getContext("2d").getImageData(c.width / 2 | 0, c.height / 2 | 0, 1, 1).data; return c.width > 0 && d[3] > 0;
  }));
  ok(drawn, "G2 카드마다 경기장 그림이 그려진다");
  await shot("games-lobby");

  // P. 포켓볼 혼자
  await open("pool", 1);
  ok(/포켓볼/.test(await txt("#gameName")) && /혼자/.test(await txt("#modeTag")) && await fr.locator("#turn").isHidden(), "P1 포켓볼 · 혼자 — 차례 표시 없음");
  ok(/샷 0 \/ 12/.test(await txt("#pills")) && /남은 공 3/.test(await txt("#pills")), "P2 샷 0 / 12 · 남은 공 3");
  ok((await txt("#eq")) === "y = 2/3x + 7", "P3 예시 식 = 흰 공 (−6, 3)을 지나는 y = 2/3x + 7");
  ok(/세기 3² \+ 2² = 13 · 거리 10\.4/.test(await txt("#powerTxt")), "P4 세기 = 3² + 2² = 13, 거리 0.8 × 13 = 10.4");
  let r = await shoot();
  ok(/정타/.test(r) && /입력: y = 2\/3x \+ 7/.test(r), "P5 예시 식으로 치면 정타");
  await shot("games-pool");
  await setIcpt("7/3");
  ok((await txt("#eq")) === "y = 2/3x + 7/3", "P6 분수 절편은 분수 그대로 식에");
  await setIcpt("−7/3");
  ok((await txt("#eq")) === "y = 2/3x − 7/3", "P7 음의 분수(−7/3)");
  await setIcpt("abc");
  ok(/수로 읽을 수 없어요/.test(await txt("#err")) && await fr.locator("#shoot").isDisabled(), "P8 읽을 수 없는 절편 → 안내 · 치기 잠김");

  await live();
  let c = (await S()).shooter;
  await setStep("dx", 0); await setStep("dy", 3);
  ok((await txt("#icptLabel")) === "x = a 의 a", "P9 x 증가량 0 → x = a 꼴");
  await setIcpt(c.x);
  ok(/^x = /.test(await txt("#eq")) && /y축에 평행/.test(await txt("#eqSub")) && /세기 0² \+ 3² = 9/.test(await txt("#powerTxt")), "P10 x = a · 세기는 y 증가량(0² + 3²)");
  r = await shoot();
  ok(/정타/.test(r) && /입력: x = /.test(r), "P11 수직선 x = a 로 정타");

  await live();
  c = (await S()).shooter;
  await setStep("dx", 3); await setStep("dy", 0);
  await setIcpt(c.y);
  ok(/^y = [−\d.]+$/.test(await txt("#eq")) && /x축에 평행/.test(await txt("#eqSub")), "P12 y 증가량 0 → y = b 꼴");
  r = await shoot();
  ok(/정타/.test(r), "P13 수평선 y = b 로 정타");

  await live();
  c = (await S()).shooter;
  await setStep("dx", 2);
  await setIcpt(c.y + 0.15);                 // 오른쪽으로 갈 때 직선이 공 중심 위(진행 방향 왼쪽)로 지나간다
  r = await shoot();
  ok(/왼쪽 스핀 50%/.test(r) && /평행한 직선/.test(r), "P14 중심에서 0.15 비껴 → 왼쪽 스핀 50% · 평행선 식 보고");

  await live();
  c = (await S()).shooter;
  await setIcpt(c.y + 1);
  r = await shoot();
  ok(/헛스윙/.test(r), "P15 반지름 밖 → 헛스윙");

  await live();
  let s = await S();
  ok(s.inv[0].xint >= 1, "P16 연습용 x절편 찬스 1개");
  const x0 = s.inv[0].xint;
  await fr.locator('.mode[data-mode="xint"]').click();
  ok(/x절편이 없어요/.test(await txt("#err")) && await fr.locator("#shoot").isDisabled(), "P17 x절편 찬스 + 기울기 0 → x절편 없음 안내");
  await setStep("dy", 1);
  c = (await S()).shooter;
  await setIcpt(c.x - 2 * c.y);              // 기울기 1/2 직선이 흰 공 중심을 지나는 x절편
  ok(/x절편 .* → y절편/.test(await txt("#eqSub")), "P18 x절편 → y절편 환산 표시");
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && /x절편 찬스 사용/.test(r) && s.inv[0].xint === x0 - 1 && s.mode === "base", "P19 x절편 찬스로 정타 · 찬스 1개 씀 · 기본 입력으로 돌아옴");
  ok(await fr.locator('.mode[data-mode="coord"]').isDisabled(), "P20 좌표 찬스 0개 → 잠김");

  // Q. 포켓볼 둘이 — 찬스는 사람마다
  await back();
  await open("pool", 2);
  s = await S();
  ok(await fr.locator("#turn").isVisible() && /1P 차례/.test(await txt("#turnName")), "Q1 둘이 — 1P 차례 표시");
  ok(/1P 0 : 0 2P/.test(await txt("#pills")) && /남은 공 5/.test(await txt("#pills")) && /샷 0 \/ 30/.test(await txt("#pills")) && s.bodies.length === 6, "Q2 목표 공 5개 · 샷 0 / 30");
  await fr.locator('.mode[data-mode="xint"]').click();
  await setIcpt(100);
  r = await shoot();
  s = await S();
  ok(/헛스윙/.test(r) && s.turn === 1 && /→ 2P 차례/.test(r) && /2P 차례/.test(await txt("#turnName")), "Q3 1P 헛스윙 → 2P 차례");
  ok(s.inv[0].xint === 0 && s.inv[1].xint === 1 && (await txt("#nX")) === "1", "Q4 1P가 쓴 찬스는 1P 것만 줄고, 화면엔 2P 찬스(1개)");
  await setIcpt(100);
  r = await shoot();
  ok((await S()).turn === 0 && (await txt("#nX")) === "0", "Q5 2P 헛스윙 → 다시 1P · 1P 찬스(0개)");

  // C. 사구 둘이 — 1P 흰 공 · 2P 노란 공
  await back();
  await open("carom", 2);
  s = await S();
  ok(/1P 차례/.test(await txt("#turnName")) && /흰 공/.test(await txt("#turnTag")) && s.shooter.id === "cue", "C1 사구 둘이 — 1P는 흰 공");
  await setIcpt(100);
  await shoot();
  s = await S();
  ok(s.turn === 1 && s.shooter.id === "y" && /노란 공/.test(await txt("#turnTag")), "C2 차례가 넘어가면 2P는 노란 공을 친다");
  c = s.shooter;
  await setIcpt(c.y - c.x / 3);              // 기본 기울기 1/3 직선이 노란 공 중심을 지나게
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && (/득점: \+1점/.test(r) ? s.turn === 1 && /한 번 더/.test(r) : s.turn === 0 && /→ 1P 차례/.test(r)), "C3 2P 정타 — 득점하면 한 번 더, 아니면 1P 차례");

  // K. 컬링 혼자 — 똑바로 · 휨
  await back();
  await open("curling", 1);
  s = await S();
  ok(/스톤 0 \/ 6/.test(await txt("#pills")) && s.bodies.filter((b) => b.team === 1).length === 2 && s.shooter.x === -8 && s.bodies.find((b) => b.id === s.shooter.id).waiting, "K1 컬링 혼자 — 상대 스톤 2개 · 내 스톤은 투구선(x = −8)");
  ok((await txt("#eq")) === `y = ${String(s.shooter.y).replace("-", "−")}` && /던지기/.test(await txt("#shoot")), "K2 예시 식 y = (스톤의 y) · 던지기 단추");
  let st0 = s.shooter, clear = !inBand(s.bodies, st0.id, -8, 4.8, st0.y, 0, 0);
  r = await shoot();
  s = await S();
  ok(/회전 없이 똑바로/.test(r) && /세기 16 → 거리 12\.8/.test(r), "K3 정타 → 회전 없이 · 세기 16 → 거리 12.8");
  const f0 = s.bodies.find((b) => b.id === st0.id);
  if (clear) ok(f0 && Math.abs(f0.x - 4.8) < 0.15 && Math.abs(f0.y - st0.y) < 0.01, "K4 막힘이 없으면 (4.8, y)에 멈춘다 — −8 + 12.8");
  else console.log("skip - K4 (길에 다른 스톤)");
  ok(s.shooter.id === "s0-2" && s.shooter.x === -8 && /스톤 1 \/ 6/.test(await txt("#pills")), "K5 다음 스톤(2번)이 투구선에");
  // 휨 — 길이 빈 배치가 나올 때까지 새 게임(첫 스톤으로 시험)
  let curled = null;
  for (let tries = 0; tries < 8 && !curled; tries++) {
    await fr.locator("#newGame").click();
    s = await S(); st0 = s.shooter;
    if (inBand(s.bodies, st0.id, -8, 5, st0.y, -0.2, 2.2)) continue;
    await setIcpt(st0.y + 0.2);              // 직선이 중심 위(진행 방향 왼쪽)로 → 반시계 회전 → 왼쪽(+y)으로 휜다
    r = await shoot();
    curled = { r, y0: st0.y, f: (await S()).bodies.find((b) => b.id === st0.id) };
  }
  if (curled) {
    ok(/반시계 방향 회전 67%/.test(curled.r) && /왼쪽으로 휨/.test(curled.r), "K6 중심에서 0.2 비껴 → 반시계 회전 67% · 왼쪽으로 휨");
    ok(curled.f && curled.f.y > curled.y0 + 0.4 && curled.f.x > 3.5, `K7 진행 방향 왼쪽(+y)으로 휘었다 (y ${curled.y0} → ${curled.f && curled.f.y.toFixed(2)}, x → ${curled.f && curled.f.x.toFixed(2)})`);
  } else ok(false, "K6 8판 안에 길이 빈 배치가 나와야 한다");
  await shot("games-curling");

  // L. 컬링 둘이 — 8번 모두 놓치면 블랭크 엔드
  await back();
  await open("curling", 2);
  s = await S();
  ok(/1P 차례/.test(await txt("#turnName")) && /빨간 스톤/.test(await txt("#turnTag")) && s.bodies.length === 1, "L1 컬링 둘이 — 미리 놓인 스톤 없이 1P(빨간 스톤)부터");
  let alt = true;
  for (let i = 0; i < 8; i++) {
    s = await S();
    if (s.turn !== i % 2 || s.shooter.id !== `s${i % 2}-${(i >> 1) + 1}`) alt = false;
    await setIcpt(100);
    await shoot();
  }
  ok(alt, "L2 4개씩 번갈아 던지고 마지막(8번째)은 2P");
  ok(/블랭크 엔드/.test(await txt("#toast")) && await fr.locator("#turn").isHidden() && await fr.locator("#shoot").isDisabled(), "L3 하우스가 비면 블랭크 엔드 · 끝나면 치기 잠김");

  // Z. 찬스 문제 — 풍선 잡기 → 맞히기 → 찬스 적립
  await back();
  await open("pool", 1);
  const before = (await S()).inv[0];
  const bub = fr.locator(".bubble");
  try { await bub.waitFor({ state: "attached", timeout: 25000 }); } catch { /* 아래에서 실패로 */ }
  if (await bub.count()) {
    const type = await bub.getAttribute("data-type");
    await bub.dispatchEvent("click");
    await fr.locator("#overlay").waitFor();
    const q = (await S()).quiz;
    ok(!!q && (await txt("#qText")) === q.text, "Z1 풍선을 누르면 찬스 문제");
    await fr.locator("#qAns").fill(String(q.ans).replace("-", "−"));
    await fr.locator("#qSubmit").click();
    const after = (await S()).inv[0];
    ok(/정답!/.test(await txt("#qMsg")) && after[type] === before[type] + 1, `Z2 맞히면 ${type === "xint" ? "x절편" : "좌표"} 찬스 +1`);
    await fr.locator("#qClose").click();
    ok(await fr.locator("#overlay").isHidden(), "Z3 닫기");
    if (type === "coord") {
      await fr.locator('.mode[data-mode="coord"]').click();
      ok(/좌표/.test(await txt("#coordInfo")) && await fr.locator("#icptField").isHidden(), "Z4 좌표 찬스 — 좌표를 알려 주고 절편 칸은 숨김");
      r = await shoot();
      ok(/정타/.test(r) && /좌표 찬스 사용/.test(r), "Z5 좌표 찬스로 치면 언제나 정타");
    }
  } else ok(false, "Z1 25초 안에 찬스 풍선이 떠야 한다");
}

(async () => {
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}/`;
  const browser = await chromium.launch({ headless: !HEADED });
  const ctx = await browser.newContext({ viewport: { width: 1180, height: 820 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [], urls = [];
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
  page.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource|ERR_FAILED/.test(m.text())) errors.push("console: " + m.text()); });
  page.on("request", (q) => urls.push(q.url()));
  await page.route(/https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)\//, (r) => r.abort());
  fs.mkdirSync(SHOTS, { recursive: true });
  const shot = async (name) => { try { await page.screenshot({ path: path.join(SHOTS, name + ".png") }); } catch { /* */ } };

  try {
    if (GAME_ONLY) {
      await page.goto(base);
      await gameChecks(page.mainFrame(), shot);
    } else {
      await mockSupabase(page);

      // A. 비관리자 — 막히고, 게임 파일은 내려받지 않는다
      ROLE = "student";
      await page.goto(base + "#/admin/games");
      await page.getByText("관리자만 들어올 수 있는 곳이에요.").waitFor({ timeout: 20000 });
      ok((await page.locator("iframe").count()) === 0, "A1 비관리자 — 안내만, iframe 없음");
      ok(!urls.some((u) => /slope-shot/.test(u)), "A2 비관리자 — 게임 파일을 받지 않는다");

      // B. 관리자 — 상단 관리자 줄의 「🎱 게임」 → 샌드박스 iframe
      ROLE = "admin";
      await page.goto(base + "#/");
      await page.reload();
      const chip = page.locator(".sh-abtn", { hasText: "🎱 게임" });
      await chip.waitFor({ timeout: 20000 });
      ok(true, "B1 관리자 줄에 「🎱 게임」");
      await chip.click();
      const el = page.locator("iframe.ag-frame");
      await el.waitFor({ timeout: 20000 });
      ok((await el.getAttribute("sandbox")) === "allow-scripts", "B2 iframe 은 sandbox=allow-scripts (앱 저장소 · 세션 접근 불가)");
      ok(urls.some((u) => /slope-shot/.test(u)), "B3 관리자 — 그때 게임 파일을 받는다(따로 나뉜 파일)");
      const fr = await (await el.elementHandle()).contentFrame();
      await fr.locator("#lobby").waitFor({ timeout: 20000 });
      ok((await fr.evaluate(() => document.documentElement.dataset.theme)) === "light", "B4 앱 테마(라이트)를 문서에 심어 연다");
      const box = await el.boundingBox();
      ok(box && box.height > 600 && box.y < 80, "B5 iframe 이 상단 바 아래 화면을 채운다");
      ok(await fr.evaluate(() => { try { localStorage.getItem("x"); return false; } catch { return true; } }), "B6 게임 안에서는 앱 저장소에 닿지 않는다");

      await gameChecks(fr, shot);

      // T. 테마 — 판을 새로 열지 않고 바꾼다
      await fr.locator("#game").waitFor();
      const shots0 = await fr.evaluate(() => window.__slopeShot().shots);
      await page.evaluate(() => window.dispatchEvent(new StorageEvent("storage", { key: "ashrain-theme", newValue: "dark" })));
      await fr.waitForFunction(() => document.documentElement.dataset.theme === "dark", null, { timeout: 5000 }).catch(() => {});
      ok((await fr.evaluate(() => document.documentElement.dataset.theme)) === "dark"
        && await fr.locator("#game").isVisible() && (await fr.evaluate(() => window.__slopeShot().shots)) === shots0, "T1 앱 테마를 바꾸면 게임도 다크로 — 판은 그대로");
      await shot("games-dark");
    }
    ok(errors.length === 0, "E1 콘솔 오류 없음" + (errors.length ? " — " + errors.slice(0, 3).join(" | ") : ""));
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e.message);
    await shot("games-fail");
  } finally {
    await browser.close(); srv.close();
  }
  console.log(`\n${pass} passed · ${fail} failed`);
  process.exit(fail ? 1 : 0);
})();
