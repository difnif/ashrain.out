// 게임(#/admin/games · #/admin/games/po) 스모크 — 기울기 샷(포켓볼 · 사구 · 컬링)과 포의 민족(이차함수 포격전)을 실제 브라우저로 해 본다.
//   node tests/smoke/games.smoke.mjs [--headed]     빌드 후(dist/ 필요): 관리자 확인 · iframe · 테마 전달 · 진행 저장 + 게임 검사
//   node tests/smoke/games.smoke.mjs --game-only    빌드 없이 게임 HTML 두 장만 바로 열어 게임 검사
// 준비: playwright + Chromium. 4 ~ 6분 걸린다(공이 실제로 굴러가고 포탄이 실제로 날아간다).
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
const PO = path.join(ROOT, "src/features/games/po-minjok.html");
const HEADED = process.argv.includes("--headed");
const GAME_ONLY = process.argv.includes("--game-only");
const SHOTS = process.env.SMOKE_SHOTS || path.join(HERE, "shots");

// ── 정적 서버 (dist/ 또는 게임 HTML 두 장: / = 기울기 샷, /po = 포의 민족) ──
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ico": "image/x-icon", ".webmanifest": "application/manifest+json" };
function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, "http://x");
      let f;
      if (GAME_ONLY) f = u.pathname.startsWith("/po") ? PO : GAME;
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
const skip = (name) => console.log("skip -", name);

// ── 기울기 샷 검사 — fr: 게임 문서가 든 프레임 ──
async function gameChecks(fr, shot) {
  const S = () => fr.evaluate(() => window.__slopeShot());
  const txt = async (sel) => ((await fr.locator(sel).innerText()) || "").replace(/\s+/g, " ").trim();
  const report = () => txt("#report");
  const num = (v) => String(Math.round(v * 1e6) / 1e6);
  const setD = async (k, v) => { const el = fr.locator(`#${k}In`); await el.fill(String(v)); await el.press("Enter"); };
  const setIcpt = (v) => fr.locator("#icpt").fill(typeof v === "number" ? num(v) : v);
  const setSlope = async (v) => { const el = fr.locator("#slopeIn"); await el.fill(String(v)); await el.press("Enter"); };
  const centerB = (s) => { const c = s.shooter; return s.dx === 0 ? c.x : s.dy === 0 ? c.y : c.y - (s.dy / s.dx) * c.x; };
  async function live() { if ((await S()).over) await fr.locator("#newGame").click(); }
  async function shoot() {
    const n = (await S()).shots;
    await fr.locator("#shoot").click();
    await fr.waitForFunction((k) => { const s = window.__slopeShot(); return s.shots === k && !s.moving; }, n + 1, { timeout: 40000, polling: 100 });
    return report();
  }
  const ready = () => fr.waitForFunction(() => !window.__slopeShot().waitStage, null, { timeout: 10000, polling: 100 });
  const solve = () => fr.evaluate(() => window.__slopeShotDebug.solve());
  const waitRec = () => fr.waitForFunction(() => { const s = window.__slopeShot(); return s.recInfo && s.recInfo.kind !== "wait"; }, null, { timeout: 20000, polling: 100 });
  const waitAuto = () => fr.waitForFunction(() => window.__slopeShot().autoRec, null, { timeout: 20000, polling: 100 }).catch(() => {});
  // 추천 샷 그대로 — 마스터: 증가량은 추천대로, 절편은 공 중심을 지나게 / 에이스: 증가량만(절편은 자동)
  async function useRec(r) { await setD("dx", r.dx); await setD("dy", r.dy); await setIcpt(centerB(await S())); }
  async function useRecD(r) { await setD("dx", r.dx); await setD("dy", r.dy); }
  const predNow = async () => { await fr.waitForTimeout(160); return (await S()).pred; };
  const back = async () => { await fr.locator("#back").click(); await fr.locator("#lobby").waitFor(); };
  const level = async (lv) => fr.locator(`.lv[data-level="${lv}"]`).click();
  const open = async (g, p) => { await fr.locator(`.open[data-game="${g}"][data-players="${p}"]`).click(); await fr.locator("#game").waitFor(); };
  const onGrid = (bodies, step) => bodies.every((b) => Math.abs(b.x / step - Math.round(b.x / step)) < 1e-9 && Math.abs(b.y / step - Math.round(b.y / step)) < 1e-9);
  // 다른 공(스톤)이 (x0, y0)에서 x 방향으로 [y0 + lo, y0 + hi] 띠를 지나는 길에 있는가
  const inBand = (bodies, me, x0, x1, y0, lo, hi) => bodies.some((o) => o.id !== me && o.x > x0 - 1.4 && o.x < x1 + 1.4 && o.y > y0 + lo - 1.4 && o.y < y0 + hi + 1.4);
  async function catchOrb(kind) {
    ok(await fr.evaluate((k) => window.__slopeShotDebug.spawnOrb(k), kind) === kind, `찬스 구슬(${kind === "r" ? "추천" : "은빛"})이 뜬다`);
    await fr.locator(".orb").waitFor({ state: "attached" });
    await fr.waitForTimeout(400);
    await fr.locator(".orb").dispatchEvent("click");
    await fr.locator("#overlay").waitFor();
    const q = (await S()).quiz, title = await txt("#qTitle");
    await fr.locator("#qAns").fill(String(q.ans).replace("-", "−"));
    await fr.locator("#qSubmit").click();
    const msg = await txt("#qMsg");
    await fr.locator("#qClose").click();
    return { q, msg, title };
  }

  // G. 게임 목록 — 조작 난이도 · 소리
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  await fr.evaluate(() => window.__slopeShotDebug.quiet(true));      // 저절로 뜨는 구슬은 끈다(클릭이 구슬에 걸리지 않게) — 구슬은 따로
  ok((await fr.locator(".card").count()) === 3 && (await fr.locator(".open").count()) === 6, "G1 게임 목록 — 카드 3장 · 단추 6개(혼자 · 둘이)");
  ok((await fr.locator(".lv").count()) === 3 && (await fr.locator(".lv").evaluateAll((els) => els.map((e) => e.dataset.level).join())) === "newbie,ace,master"
    && (await fr.locator('.lv[aria-checked="true"]').getAttribute("data-level")) === "ace", "G2 조작 난이도 3단계(뉴비 · 에이스 · 마스터), 에이스가 골라져 있다");
  const drawn = await fr.evaluate(() => [...document.querySelectorAll(".card canvas")].every((c) => {
    const d = c.getContext("2d").getImageData(c.width / 2 | 0, c.height / 2 | 0, 1, 1).data; return c.width > 0 && d[3] > 0;
  }));
  ok(drawn, "G3 카드마다 경기장 그림");
  ok(/횟수 무제한/.test(await txt('.card[data-game="pool"]')) && /삼각형/.test(await txt('.card[data-game="pool"]')) && /몇 번이든/.test(await txt('.card[data-game="curling"]')), "G4 포켓볼 카드 — 삼각형 랙 · 혼자는 횟수 무제한");
  await fr.locator("#lobby .js-snd").click();
  ok((await S()).sound === false && (await fr.locator("#lobby .js-snd").getAttribute("aria-pressed")) === "false", "G5 소리 끄기");
  await fr.locator("#lobby .js-snd").click();
  ok((await S()).sound === true, "G6 소리 다시 켜기");
  await shot("games-lobby");

  // P. 포켓볼 혼자 · 마스터 — 증가량 · y절편 모두 직접(삼각형 랙 · 브레이크)
  await level("master");
  await open("pool", 1);
  let s = await S();
  ok(/포켓볼/.test(await txt("#gameName")) && /혼자/.test(await txt("#modeTag")) && /마스터/.test(await txt("#levelTag")) && await fr.locator("#turn").isHidden() && s.ctl === "full", "P1 포켓볼 · 혼자 · 마스터(모두 직접)");
  const pills = await txt("#pills");
  ok(/샷 0/.test(pills) && !/\//.test(pills) && /남은 공 15/.test(pills) && s.cap === "none" && s.inv[0].x === 0 && s.inv[0].r === 0, "P2 혼자는 횟수 무제한 · 마스터는 공 15개 · 찬스 없이 시작");
  {
    const t = s.bodies.filter((b) => b.id !== "cue"), apex = t.find((b) => b.id === "t1"), eight = t.find((b) => b.id === "t8");
    const rows = new Set(t.map((b) => b.x.toFixed(3))).size;
    ok(t.length === 15 && apex && apex.x === 10 && apex.y === 10 && rows === 5 && t.filter((b) => b.stripe).length === 7 && eight && Math.abs(eight.y - 10) < 1e-9,
      "P3 삼각형 랙 — 15개 · 5줄 · 맨 앞 1번 (10, 10) · 8번은 셋째 줄 가운데 · 줄무늬 공 7개");
  }
  const c0 = s.shooter;
  ok((await txt("#eq")) === "—" && /x 증가량과 y 증가량을 넣으세요/.test(await txt("#err")) && await fr.locator("#shoot").isDisabled()
    && (await fr.locator("#dxIn").inputValue()) === "" && (await fr.locator("#dyIn").inputValue()) === "" && (await fr.locator("#icpt").inputValue()) === "" && c0.x === -12,
    "P4 처음엔 빈 칸 — 값을 넣기 전엔 식 · 방향이 없고 치기 잠김(예시 값을 채워 두지 않는다)");
  await setD("dx", 6); await setD("dy", 4); await setIcpt(String(c0.y + 8));
  ok((await txt("#eq")) === `y = 2/3x + ${c0.y + 8}`, `P4b 직접 넣은 값으로 식 — 흰 공 (−12, ${c0.y})을 지나는 y = 2/3x + ${c0.y + 8}`);
  ok(/세기 6² \+ 4² = 52 \/ 120 → 거리 26/.test(await txt("#powerTxt")), "P5 세기 6² + 4² = 52 / 상한 120 → 거리 26 (세기 ÷ 2)");
  ok(/오른쪽 위로/.test(await txt("#dirText")) && /큐는 반대쪽\(↙\)/.test(await txt("#dirText")) && (await txt("#flipDir")) === "↗", "P6 방향 안내 — 오른쪽 위로 · 큐는 반대쪽(↙)에서");
  let pr = await predNow();
  ok(pr && pr.cue === 2 && pr.cueNotes.includes("분수 기울기") && pr.cueNotes.includes("절편이 정수"), "P7 타점 난이도 ★2 — 격자점 · 분수 기울기 · 정수 절편");
  await setD("dx", 10); await setD("dy", 1.2);
  ok(/세기 10² \+ 1\.2² = 101\.44 \/ 120 → 거리 50\.72/.test(await txt("#powerTxt")), "P8 소수 증가량 10 · 1.2 → 세기 101.44");
  await setIcpt("7.44");
  ok((await txt("#eq")) === "y = 0.12x + 7.44", "P9 식 y = 0.12x + 7.44 (기울기 0.12)");
  pr = await predNow();
  ok(pr && pr.cue === 3 && pr.cueNotes.includes("소수 기울기"), "P10 소수 기울기 · 소수 절편 → 타점 ★3");
  await setD("dx", 30);
  s = await S();
  ok(s.dx === 30 && (await fr.locator("#dxIn").inputValue()) === "30" && /세기 30² \+ 1\.2² = 901\.44 → 상한 120 → 거리 60/.test(await txt("#powerTxt"))
    && await fr.locator("#powerBarWrap.max").count() === 1, "P11 증가량은 자유롭게(30도 그대로), 세기는 상한 120에서 멈춘다 → 거리 60");
  await fr.locator('[data-step="dy"][data-d="0.1"]').click();
  await fr.locator('[data-step="dx"][data-d="-1"]').click();
  await fr.locator('[data-step="dx"][data-d="flip"]').click();
  s = await S();
  ok(Math.abs(s.dy - 1.3) < 1e-9 && s.dx === -29, "P12 +0.1 · −1 · ± 부호 단추 (dy 1.3, dx −29)");
  await fr.locator("#flipDir").click();
  s = await S();
  ok(s.dx === 29 && Math.abs(s.dy + 1.3) < 1e-9 && /오른쪽 아래로/.test(await txt("#dirText")) && (await txt("#flipDir")) === "↘", "P13 화살표 단추 — 두 부호를 함께 바꿔 반대 방향(기울기 그대로)");
  await setIcpt("14");
  await fr.locator('[data-ib="1"]').click();
  ok((await fr.locator("#icpt").inputValue()) === "15", "P14 y절편 ▲1 → 15");
  await fr.locator('[data-ib="-0.1"]').click();
  ok((await fr.locator("#icpt").inputValue()) === "14.9", "P15 y절편 ▼0.1 → 14.9");
  // 경기장을 누르면 그 점(공)의 좌표만 — 값은 그대로(늘 직접 넣는다)
  await setD("dx", 6); await setD("dy", 4);
  {
    s = await S();
    const t = s.bodies.find((b) => b.id === "t1"), icpt0 = await fr.locator("#icpt").inputValue();
    const pos = await fr.evaluate(([x, y]) => window.__slopeShotDebug.toCanvas(x, y), [t.x, t.y]);
    await fr.locator("#cv").click({ position: pos });
    s = await S();
    ok(s.dx === 6 && s.dy === 4 && (await fr.locator("#icpt").inputValue()) === icpt0 && s.probe && s.probe.x === t.x && s.probe.y === t.y && /중심 \(10, 10\)/.test(s.probe.label),
      `P16 경기장을 누르면 그 공의 중심 좌표만 보여 준다(${s.probe && s.probe.label}) — 증가량 · 절편은 그대로`);
  }
  // 첫 샷은 브레이크 — 도움 보기(마스터는 꺼진 채로 시작)
  ok(!s.hints && await fr.locator("#hintCard").isHidden() && !(await fr.locator("#hints").isChecked()), "P17 마스터 — 도움 보기는 꺼진 채로 시작");
  const brk = await solve();
  ok(brk && brk.ok && /브레이크/.test(brk.text) && (await S()).rec.brk, `P18 첫 샷은 브레이크 추천 (${brk && brk.text} · Δ ${brk && brk.dx}, ${brk && brk.dy})`);
  await fr.locator("#hints").check();
  ok(await fr.locator("#hintCard").isVisible() && (await S()).hints === true, "P19 도움 보기 켜기 — 추천 카드");
  await fr.locator("#hints").uncheck();
  ok(await fr.locator("#hintCard").isHidden(), "P20 도움 보기 끄기");
  await useRec(brk);
  let r = await shoot();
  s = await S();
  const t1 = s.bodies.find((b) => b.id === "t1");
  ok(/정타/.test(r) && /입력: y = /.test(r) && /예측 난이도/.test(r) && (!t1 || t1.x !== 10 || t1.y !== 10), "P21 브레이크 — 추천대로 치면 정타 · 삼각형이 흩어진다 · 결과에 예측 난이도");
  ok(s.bodies.some((b) => !onGrid([b], 0.5)), "P22 마스터 — 공은 멈춘 자리 그대로(소수 좌표, 격자로 옮기지 않음)");
  ok(await fr.evaluate(() => document.getElementById("report").parentElement.id === "outBelow"), "P23 자리가 넉넉하면 샷 결과는 테이블 아래에");
  await shot("games-pool");
  {
    const rec = await solve();
    ok(rec && !rec.brk && (rec.ok ? /번 공 → .+ 구멍/.test(rec.text) : /넣을 길/.test(rec.text)), `P24 브레이크 뒤에는 넣을 공을 찾는다 (${rec && rec.text})`);
  }
  await setD("dx", 6); await setD("dy", 4);
  await setIcpt("7/3");
  ok((await txt("#eq")) === "y = 2/3x + 7/3", "P25 분수 절편은 분수 그대로");
  await setIcpt("−7/3");
  ok((await txt("#eq")) === "y = 2/3x − 7/3", "P26 음의 분수");
  await setIcpt("abc");
  ok(/수로 읽을 수 없어요/.test(await txt("#err")) && await fr.locator("#shoot").isDisabled(), "P27 읽을 수 없는 절편 → 안내 · 치기 잠김");

  await live();
  let c = (await S()).shooter;
  await setD("dx", 0); await setD("dy", 6);
  ok((await txt("#icptLabel")) === "x = a 의 a", "P28 x 증가량 0 → x = a 꼴");
  await setIcpt(c.x);
  pr = await predNow();
  ok(/^x = /.test(await txt("#eq")) && /세기 0² \+ 6² = 36/.test(await txt("#powerTxt")) && pr && pr.cueNotes.some((n) => /x = a 꼴/.test(n)), "P29 x = a · 세기는 y 증가량 · 타점 메모");
  r = await shoot();
  ok(/정타/.test(r) && /입력: x = /.test(r), "P30 수직선 x = a 로 정타");

  await live();
  c = (await S()).shooter;
  await setD("dx", 6); await setD("dy", 0);
  ok((await txt("#icptLabel")) === "y = b 의 b", "P31 y 증가량 0 → y = b 꼴");
  await setIcpt(c.y);
  r = await shoot();
  ok(/정타/.test(r), "P32 수평선 y = b 로 정타");

  await live();
  c = (await S()).shooter;
  await setD("dx", 4);
  await setIcpt(c.y + 0.3);                  // 오른쪽으로 갈 때 직선이 공 중심 위(진행 방향 왼쪽)로 0.3 — 반지름 0.6의 절반
  r = await shoot();
  ok(/왼쪽 스핀 50%/.test(r) && /평행한 직선/.test(r), "P33 중심에서 0.3 비껴 → 왼쪽 스핀 50% · 평행선 식");

  await live();
  c = (await S()).shooter;
  await setIcpt(c.y + 2);
  r = await shoot();
  ok(/헛스윙/.test(r), "P34 반지름 밖 → 헛스윙");

  // 추천 찬스 — 마스터는 0개로 시작, 금빛 구슬로 얻는다 → 증가량 추천 → (하나 더) → y절편 추천 → 그대로 치면 들어간다
  await live();
  ok(await fr.locator("#cR").isDisabled(), "P35 마스터 — 추천 찬스 0개 → 잠김");
  {
    const { q, msg } = await catchOrb("r");
    ok(q.kind === "r" && /정답!/.test(msg) && (await S()).inv[0].r === 1, "P36 금빛 구슬 문제를 맞히면 추천 찬스 +1");
  }
  await fr.locator("#cR").click();
  ok(await fr.locator("#rPick").isVisible(), "P37 마스터의 추천 찬스 — 증가량 추천 · y절편 추천 고르기");
  const d0 = { dx: (await S()).dx, dy: (await S()).dy, ic: await fr.locator("#icpt").inputValue() };
  await fr.locator('[data-rp="delta"]').click();
  await waitRec();
  s = await S();
  const rec1 = s.rec;
  if (s.recInfo.kind === "delta") {
    ok(rec1 && rec1.ok && s.recInfo.dx === rec1.dx && s.recInfo.dy === rec1.dy && s.dx === d0.dx && s.dy === d0.dy && s.inv[0].r === 0 && /추천 찬스 · 증가량/.test(await txt("#calcBox")) && /직접 넣으세요/.test(await txt("#calcText")),
      `P38 증가량 추천 — Δ ${rec1.dx}, ${rec1.dy}를 알려만 주고(칸은 그대로) 찬스 하나 씀`);
    await useRecD(rec1);
    await catchOrb("r");
    await fr.locator("#cR").click(); await fr.locator('[data-rp="icpt"]').click();
    s = await S();
    ok(s.recInfo.kind === "icpt" && /b = y₀ − 기울기 × x₀|가로선이라|세로선이라/.test(await txt("#calcText")) && s.inv[0].r === 0 && (await fr.locator("#icpt").inputValue()) === d0.ic,
      "P39 y절편 추천 — 공 중심을 지나는 b를 계산 과정과 함께 알려만 준다(칸은 그대로)");
    await setIcpt(s.recInfo.text);
    pr = await predNow();
    ok(pr && pr.cue === 1, "P40 추천 y절편을 쓰면 타점 난이도 ★1");
    const left0 = (await txt("#pills")).match(/남은 공 (\d+)/)[1];
    r = await shoot();
    ok(/정타/.test(r) && /목표 공 \d+개 성공/.test(r) && /추천 찬스\(y절편\) 사용/.test(r), `P41 추천대로 치면 그대로 들어간다(미리 굴려 본 것 = 실제) · 남은 공 ${left0} → ${(await txt("#pills")).match(/남은 공 (\d+)/)[1]}`);
  } else skip(`P38 ~ P41 — 이번 판엔 확실한 추천 샷이 없었다(${s.recInfo.kind}) · 찬스 그대로 ${s.inv[0].r}`);

  // x절편 찬스(은빛) — y절편 대신 x절편을 직접 계산해 넣는다
  await live();
  {
    const g = await catchOrb("x");
    ok(/x절편 찬스 문제/.test(g.title) && (await S()).inv[0].x === 1, "P42 은빛 구슬 — 마스터에선 x절편 찬스 +1");
  }
  await setD("dx", 4); await setD("dy", 2);
  await fr.locator("#cX").click();
  s = await S();
  ok(s.xmode && (await txt("#icptLabel")) === "x절편 a (x절편 찬스)" && /x절편 = x₀ − y₀ ÷ 기울기/.test(await txt("#calcText")), "P43 x절편 찬스 — 입력 칸이 x절편으로(계산은 직접)");
  await fr.locator("#cX").click();
  s = await S();
  ok(!s.xmode && s.inv[0].x === 1 && (await txt("#icptLabel")) === "y절편 b", "P44 다시 누르면 취소 — 쓰지 않으면 줄지 않는다");
  await fr.locator("#cX").click();
  c = (await S()).shooter;
  await setIcpt(c.x - c.y * 2);              // 기울기 1/2 → x절편 = x₀ − y₀ ÷ (1/2)
  ok(/x절편 .+ → y절편/.test(await txt("#eqSub")), "P45 x절편을 넣으면 y절편으로 바꿔 식을 보여 준다");
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && /x절편 찬스 사용/.test(r) && s.inv[0].x === 0 && !s.xmode, "P46 x절편으로 정타 · 찬스는 칠 때 하나 씀");
  ok(await fr.locator("#cX").isDisabled(), "P47 x절편 찬스 0개 → 잠김");

  // Z. 찬스 구슬 — 공보다 작게
  {
    ok(await fr.evaluate(() => window.__slopeShotDebug.spawnOrb("x")) === "x", "Z1 은빛 구슬이 뜬다");
    await fr.locator(".orb").waitFor({ state: "attached" });
    await fr.waitForTimeout(500);
    const box = await fr.locator(".orb .core").boundingBox(), u = (await S()).unit;
    ok(box && box.width < 1.2 * u && box.width > 8, `Z2 구슬은 공보다 작다 (구슬 ${box && box.width.toFixed(1)}px < 공 지름 ${(1.2 * u).toFixed(1)}px)`);
    await shot("games-orb");
    await fr.locator(".orb").dispatchEvent("click");
    await fr.locator("#overlay").waitFor();
    const q = (await S()).quiz;
    ok(!!q && q.kind === "x" && (await txt("#qText")) === q.text, "Z3 구슬을 누르면 찬스 문제(사칙 계산)");
    await fr.locator("#qAns").fill(String(q.ans).replace("-", "−"));
    await fr.locator("#qSubmit").click();
    ok(/정답!/.test(await txt("#qMsg")), "Z4 맞히면 정답!");
    await fr.locator("#qClose").click();
    ok(await fr.locator("#overlay").isHidden(), "Z5 닫기");
  }

  // N. 뉴비 — 기울기만 넣으면 갈 쪽 · 세기 · 타점은 추천대로
  await back();
  await level("newbie");
  await open("pool", 1);
  s = await S();
  ok(s.ctl === "slope" && await fr.locator("#slopeCtl").isVisible() && await fr.locator("#dxCtl").isHidden() && await fr.locator("#icptCtl").isHidden() && await fr.locator("#autoBox").isVisible()
    && /남은 공 6/.test(await txt("#pills")) && s.inv[0].x === 2 && s.inv[0].r === 2 && s.hints && /뉴비/.test(await txt("#levelTag")), "N1 뉴비 — 기울기 칸만(증가량 · y절편 칸 없음) · 공 6개 · 어림 2 · 추천 2 · 도움 켬");
  await waitAuto();
  s = await S();
  {
    const ab = await txt("#autoBox");
    ok(s.autoRec && /자동/.test(ab) && /갈 쪽/.test(ab) && /\(추천대로\)/.test(ab) && /흰 공 중심/.test(ab) && /세기 .+ \(자동\)/.test(await txt("#powerTxt")), "N2 갈 쪽 · 세기 · 타점은 추천대로 자동(계산 과정도 보여 줌)");
  }
  {
    const y0 = s.shooter.y, want = Math.atan2(10 - y0, 22), got = s.rec ? Math.atan2(s.rec.dy, s.rec.dx) : 9;
    ok(s.rec && s.rec.brk && Math.abs(want - got) < 0.04, `N3 첫 샷 추천은 브레이크 — 1번 공 (10, 10)을 정면으로 (Δ ${s.rec && s.rec.dx}, ${s.rec && s.rec.dy})`);
  }
  await setSlope(String(Math.round(s.rec.dy / s.rec.dx * 10000) / 10000).replace("-", "−"));
  r = await shoot();
  s = await S();
  {
    const t = s.bodies.find((b) => b.id === "t1");
    ok(/정타/.test(r) && (!t || t.x !== 10 || t.y !== 10), "N4 추천 기울기만 넣고 치면 정타(갈 쪽 · 세기 · 타점은 자동) — 삼각형이 흩어진다");
  }
  ok(onGrid(s.bodies, 1), "N5 뉴비 — 친 뒤 공은 격자점으로");
  {
    await waitAuto();
    const rec = (await S()).rec;
    if (rec && rec.ok && Math.abs(rec.dx) > 1e-9) {
      const v0 = await fr.locator("#slopeIn").inputValue();
      await fr.locator("#cR").click();
      await waitRec();
      s = await S();
      const v = String(s.recInfo.text || "").replace("−", "-"), m = /\//.test(v) ? Number(v.split("/")[0]) / Number(v.split("/")[1]) : Number(v);
      ok(s.recInfo.kind === "slope" && Math.abs(m - rec.dy / rec.dx) < 1e-6 && s.inv[0].r === 1 && (await fr.locator("#slopeIn").inputValue()) === v0, `N6 추천 찬스 — 추천 기울기 ${s.recInfo.text}를 알려만 준다(칸은 그대로 · 찬스 2 → 1)`);
      await setSlope(s.recInfo.text);
      const left0 = Number((await txt("#pills")).match(/남은 공 (\d+)/)[1]);
      r = await shoot();
      const left1 = Number((await txt("#pills")).match(/남은 공 (\d+)/)[1]);
      ok(/정타/.test(r) && /목표 공 \d+개 성공/.test(r) && left1 < left0, `N7 그대로 치면 들어간다 — 남은 공 ${left0} → ${left1}`);
    } else skip(`N6 · N7 — 이번 판엔 확실한 추천 샷이 없었다(${rec && rec.text})`);
  }
  await live();
  await waitAuto();
  {
    const x0 = (await S()).inv[0].x;
    await fr.locator("#cX").click();
    await waitRec();
    s = await S();
    if (s.recInfo.kind === "hint") ok(/기울기 약/.test(await txt("#calcText")) && s.inv[0].x === x0 - 1, "N8 어림 찬스 — 추천 기울기를 어림해 알려 준다(찬스 하나 씀)");
    else skip("N8 — 어림할 샷이 없었다");
  }
  {
    s = await S();
    const t = s.bodies.filter((b) => b.kind !== "cue" && b.id !== "cue")[0], v0 = await fr.locator("#slopeIn").inputValue();
    const pos = await fr.evaluate(([x, y]) => window.__slopeShotDebug.toCanvas(x, y), [t.x, t.y]);
    await fr.locator("#cv").click({ position: pos });
    s = await S();
    ok((await fr.locator("#slopeIn").inputValue()) === v0 && s.probe && Math.abs(s.probe.x - t.x) < 1e-9 && Math.abs(s.probe.y - t.y) < 1e-9, `N9 뉴비도 경기장을 누르면 좌표만(${s.probe && s.probe.label}) — 기울기 칸은 그대로`);
  }

  // AC. 에이스 — 증가량으로 방향 · 세기, y절편은 공 중심을 지나게 자동
  await back();
  await level("ace");
  await open("pool", 1);
  s = await S();
  ok(s.ctl === "delta" && await fr.locator("#dxCtl").isVisible() && await fr.locator("#dyCtl").isVisible() && await fr.locator("#icptCtl").isHidden()
    && /타점: 흰 공 중심/.test(await txt("#autoBox")) && /남은 공 10/.test(await txt("#pills")) && s.inv[0].x === 1 && s.inv[0].r === 1, "AC1 에이스 — 증가량 칸만(y절편 자동) · 공 10개 · 어림 1 · 추천 1");
  ok((await txt("#eq")) === "—" && /x 증가량과 y 증가량을 넣으세요/.test(await txt("#err")) && await fr.locator("#shoot").isDisabled(), "AC2a 에이스도 처음엔 빈 칸 — 증가량을 넣어야 친다");
  await setD("dx", 6); await setD("dy", 4);
  ok((await txt("#eq")) === `y = 2/3x + ${s.shooter.y + 8}`, "AC2 식은 늘 흰 공 중심을 지난다");
  await fr.locator("#cR").click();
  await waitRec();
  s = await S();
  ok(s.recInfo.kind === "delta" && s.rec && s.rec.brk && s.recInfo.dx === s.rec.dx && s.recInfo.dy === s.rec.dy && s.dx === 6 && s.dy === 4 && s.inv[0].r === 0 && await fr.locator("#rPick").isHidden(),
    "AC3 추천 찬스 — 고를 것 없이 바로 추천 증가량(브레이크)을 알려 준다(칸은 그대로)");
  await useRecD({ dx: s.recInfo.dx, dy: s.recInfo.dy });
  r = await shoot();
  ok(/정타/.test(r), "AC4 그대로 치면 정타");
  await live();
  {
    await fr.locator("#cX").click();
    await waitRec();
    s = await S();
    if (s.recInfo.kind === "hint") ok(/기울기 약/.test(await txt("#calcText")) && /세기 약/.test(await txt("#calcText")) && s.inv[0].x === 0, "AC5 어림 찬스 — 기울기 · 세기를 어림해 알려 준다");
    else skip("AC5 — 어림할 샷이 없었다");
  }
  {
    const g = await catchOrb("x");
    ok(/어림 찬스 문제/.test(g.title), "AC6 에이스의 은빛 구슬은 어림 찬스");
  }

  // Q. 포켓볼 둘이(에이스) — 찬스는 사람마다
  await back();
  await open("pool", 2);
  s = await S();
  ok(await fr.locator("#turn").isVisible() && /1P 차례/.test(await txt("#turnName")), "Q1 둘이 — 1P 차례");
  ok(/1P 0 : 0 2P/.test(await txt("#pills")) && /남은 공 15/.test(await txt("#pills")) && /샷 0 \/ 60/.test(await txt("#pills")) && s.bodies.length === 16
    && s.inv.map((i) => `${i.x}${i.r}`).join() === "11,11", "Q2 둘이 — 공 15개 · 샷 0 / 60 · 찬스는 사람마다(어림 1 · 추천 1)");
  await fr.locator("#cR").click();
  await waitRec();
  s = await S();
  ok(s.inv.map((i) => `${i.x}${i.r}`).join() === "10,11", "Q3 1P가 쓴 추천 찬스는 1P 것만 준다");
  if (s.recInfo && s.recInfo.kind === "delta") await useRecD({ dx: s.recInfo.dx, dy: s.recInfo.dy }); else { await setD("dx", 6); await setD("dy", 0); }
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && (s.pts[0] > 0 ? s.turn === 0 : s.turn === 1 && /→ 2P 차례/.test(r)), `Q4 넣으면 한 번 더, 못 넣으면 2P 차례 (1P ${s.pts[0]}점 · ${s.turn + 1}P 차례)`);

  // C. 사구(에이스) — 둘이(1P 흰 공 · 2P 노란 공), 혼자(추천대로 치면 득점)
  await back();
  await open("carom", 2);
  s = await S();
  ok(/1P 차례/.test(await txt("#turnName")) && /흰 공/.test(await txt("#turnTag")) && s.shooter.id === "cue" && /\/ 150/.test(await txt("#powerTxt")), "C1 사구 둘이 — 1P는 흰 공 · 세기 상한 150");
  {
    const sh = s.shooter;
    await setD("dx", sh.x > 0 ? 1 : -1); await setD("dy", 0);   // 가까운 쿠션 쪽으로 살짝 — 득점 없이
    await shoot();
  }
  s = await S();
  ok(s.turn === 1 && s.shooter.id === "y" && /노란 공/.test(await txt("#turnTag")), "C2 득점 못 하면 2P — 노란 공");
  await setD("dx", 6); await setD("dy", 2);
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && (/득점: \+1점/.test(r) ? s.turn === 1 && /한 번 더/.test(r) : s.turn === 0 && /→ 1P 차례/.test(r)), "C3 2P 정타(타점 자동) — 득점하면 한 번 더, 아니면 1P");
  await back();
  await open("carom", 1);
  {
    let rc = await solve();
    for (let k = 0; k < 4 && !(rc && rc.ok); k++) { await fr.locator("#newGame").click(); rc = await solve(); }   // 판이 무작위라 길이 없으면 새 판
    ok(rc && rc.ok && /빨간 공 2개/.test(rc.text), `C4 사구 추천 샷 (${rc && rc.text} · Δ ${rc && rc.dx}, ${rc && rc.dy})`);
    if (rc && rc.ok) {
      await useRecD(rc);
      r = await shoot();
      ok(/정타/.test(r) && /득점: \+1점/.test(r) && /점수 1 \/ 3/.test(await txt("#pills")), "C5 추천 증가량대로 치면 빨간 공 2개 — 득점");
    }
    await shot("games-carom");
  }

  // K. 컬링 혼자 · 뉴비 — 단계 · 몇 번이든 다시
  await back();
  await level("newbie");
  await open("curling", 1);
  s = await S();
  const opp0 = s.bodies.filter((b) => b.team === 1);
  ok(/단계 1/.test(await txt("#pills")) && /1번째 시도/.test(await txt("#pills")) && opp0.length === 1 && s.shooter.x === -16 && s.shooter.y === 10
    && s.bodies.find((b) => b.id === s.shooter.id).waiting, "K1 단계 1 — 상대 스톤 1개 · 내 스톤은 (−16, 10)");
  await waitAuto();
  ok((await txt("#eq")) === "—" && /기울기를 입력하세요/.test(await txt("#err")) && await fr.locator("#shoot").isDisabled(), "K2a 뉴비 — 처음엔 기울기 칸이 비어 있어 던질 수 없다");
  await setSlope("0");
  ok((await txt("#eq")) === "y = 10" && /던지기/.test(await txt("#shoot")) && /세기 .+ \(자동\)/.test(await txt("#powerTxt")), "K2 기울기 0을 넣으면 y = 10 · 세기는 추천대로 자동");
  pr = await predNow();
  s = await S();
  ok(pr && pr.cue === 1 && pr.tgtWho === "스톤 → 버튼" && s.rec && s.rec.ok, `K3 예측 — 타점 ★1(자동) · 목표 ★${pr && pr.tgt} · 추천 샷이 미리 준비됨`);
  await shot("games-curling");
  r = await shoot();
  s = await S();
  ok(/회전 없이 똑바로/.test(r) && /단계 1 통과/.test(r) && s.waitStage, "K4 뉴비 단계 1 — 기울기 0으로 던지면 통과(뉴비 판은 y = b 로 이길 수 있게 놓인다)");
  await ready();
  s = await S();
  ok(s.stage === 2 && s.tries === 0 && s.shooter.x === -16 && Number.isInteger(s.shooter.y) && s.shooter.y >= 8 && s.shooter.y <= 12 && /단계 2/.test(await txt("#pills")), `K5 다음 단계 — 단계 2 · 내 스톤 (−16, ${s.shooter.y})`);
  // 마스터 — 일부러 짧게(호그 라인 전에 멈춤) → 같은 판으로 다시, 비껴 던지면 휜다
  await back();
  await level("master");
  await open("curling", 1);
  s = await S();
  const st1 = s.stage, opp2 = s.bodies.filter((b) => b.team === 1).map((b) => `${b.id}:${b.x},${b.y}`).join();
  await setD("dx", 3); await setD("dy", 0); await setIcpt(s.shooter.y);
  r = await shoot();
  ok(/호그 라인/.test(r) && /같은 판으로 다시/.test(r), "K6 짧으면 호그 라인 전에 제거 · 같은 판으로 다시");
  await ready();
  s = await S();
  ok(s.stage === st1 && s.tries === 1 && /2번째 시도/.test(await txt("#pills")) && s.bodies.filter((b) => b.team === 1).map((b) => `${b.id}:${b.x},${b.y}`).join() === opp2
    && s.bodies.filter((b) => b.team === 0).length === 1, "K7 다시 — 단계 그대로 · 2번째 시도 · 상대 스톤은 제자리 · 내 스톤 1개");
  {
    const st0 = s.shooter;
    await setD("dx", 7.2); await setD("dy", 0);
    await setIcpt(st0.y + 0.4);
    const blocked = inBand(s.bodies, st0.id, -16, 10, st0.y, -0.4, 3);
    r = await shoot();
    const f = (await S()).bodies.find((b) => b.id === st0.id);
    ok(/반시계 방향 회전 67%/.test(r) && /왼쪽으로 휨/.test(r), "K8 중심에서 0.4 비껴 → 반시계 회전 67% · 왼쪽으로 휨");
    if (!blocked) ok(f && f.y > st0.y + 0.8 && f.x > 6, `K9 진행 방향 왼쪽(+y)으로 휘었다 (y ${st0.y} → ${f && f.y.toFixed(2)})`);
    else skip("K9 (길에 다른 스톤)");
    await ready();
  }
  // 에이스 — 추천 증가량대로 던지면 통과
  await back();
  await level("ace");
  await open("curling", 1);
  {
    s = await S();
    ok(s.bodies.filter((b) => b.team === 1).length >= 1 && Number.isInteger(s.shooter.y) && s.shooter.y >= 7 && s.shooter.y <= 13, "K10 에이스 — 투구 자리 높이가 바뀐다(7 ~ 13)");
    const rc = await solve();
    ok(rc && rc.ok, `K11 에이스 판 추천 (${rc && rc.text} · Δ ${rc && rc.dx}, ${rc && rc.dy})`);
    await useRecD(rc);
    r = await shoot();
    ok(/단계 1 통과/.test(r), "K12 추천대로 던지면 통과(미리 굴려 본 것 = 실제)");
    await ready();
    ok((await S()).stage === 2, "K13 단계 2로");
  }

  // L. 컬링 둘이(마스터) — 8번 모두 놓치면 블랭크 엔드
  await back();
  await level("master");
  await open("curling", 2);
  s = await S();
  ok(/1P 차례/.test(await txt("#turnName")) && /빨간 스톤/.test(await txt("#turnTag")) && s.bodies.length === 1, "L1 컬링 둘이 — 1P(빨간 스톤)부터");
  let alt = true;
  await setD("dx", 7.2); await setD("dy", 0);           // 둘이 번갈아도 넣은 증가량은 남는다
  for (let i = 0; i < 8; i++) {
    s = await S();
    if (s.turn !== i % 2 || s.shooter.id !== `s${i % 2}-${(i >> 1) + 1}`) alt = false;
    await setIcpt(100);
    await shoot();
  }
  ok(alt, "L2 4개씩 번갈아 · 마지막은 2P");
  ok(/블랭크 엔드/.test(await txt("#toast")) && await fr.locator("#turn").isHidden() && await fr.locator("#shoot").isDisabled(), "L3 하우스가 비면 블랭크 엔드 · 치기 잠김");

  // X. 성공 효과 — 단계별
  ok(await fr.evaluate(() => window.__slopeShotDebug.celebrate(5)), "X1 성공 효과 5단계");
  await fr.waitForTimeout(900);
  ok(await fr.locator("#banner").isVisible() && /전설의 샷!/.test(await txt("#banner")), "X2 5단계 — 「전설의 샷!」");
  await shot("games-tier5");

  // F. 전체 화면
  await fr.locator("#gameHead .js-fs").click();
  await fr.waitForFunction(() => window.__slopeShot().fs === true, null, { timeout: 3000 }).catch(() => {});
  s = await S();
  ok(s.fs && await fr.evaluate(() => document.body.classList.contains("fs")) && /전체 화면 끝/.test(await txt("#gameHead .js-fs")), `F1 전체 화면 켜기 (${s.immersive ? "앱 상단 바 숨김" : "Fullscreen API"})`);
  await shot("games-fullscreen");
  await fr.locator("#gameHead .js-fs").click();
  await fr.waitForFunction(() => window.__slopeShot().fs === false, null, { timeout: 3000 }).catch(() => {});
  ok((await S()).fs === false && !(await fr.evaluate(() => document.body.classList.contains("fs"))), "F2 전체 화면 끄기");
}

// ── 포의 민족 검사 ──
async function poChecks(fr, shot) {
  const S = () => fr.evaluate(() => window.__poMinjok());
  const D = (fn, ...a) => fr.evaluate(([fn, a]) => window.__poDebug[fn](...a), [fn, a]);
  const txt = async (sel) => ((await fr.locator(sel).innerText()) || "").replace(/\s+/g, " ").trim();
  const until = async (pred, ms = 15000) => { const t0 = Date.now(); for (;;) { const s = await S(); if (pred(s)) return s; if (Date.now() - t0 > ms) return s; await fr.waitForTimeout(60); } };
  const myAim = (s) => s.battle && !s.battle.over && s.battle.phase === "aim" && s.battle.sides[s.battle.turn.side].human;
  const active = (b) => b.sides[b.turn.side].units[b.turn.unit];
  const nearFoe = (b, u) => b.sides[1 - b.turn.side].units.filter((t) => t.alive).sort((p, q) => Math.abs(p.x - u.x) - Math.abs(q.x - u.x))[0];
  const ids = () => fr.locator("#inputs input").evaluateAll((els) => els.map((e) => e.id).join());
  // 정답 입력으로 쏘기 — 지금 자리에서 닿는 길이 없으면 조금 다가가서
  async function fireSolved() {
    let sol = await D("solve");
    for (let k = 0; !sol && k < 4; k++) {
      const b = (await S()).battle, u = active(b), t = nearFoe(b, u);
      await D("setMp", 100);
      await D("moveBy", Math.sign(t.x - u.x) || 1, 1.5);
      sol = await D("solve");
    }
    if (sol) await D("setInputs", sol);
    await fr.locator("#fire").click();
    return sol;
  }
  async function catchOrb(kind) {
    ok(await D("spawnOrb", kind), `${kind === "math" ? "금빛" : "보랏빛"} 구슬이 뜬다`);
    await fr.locator(".orb").dispatchEvent("click");
    await fr.locator("#quizOv").waitFor();
    return (await S()).quiz;
  }

  // W. 시작 화면
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  ok((await fr.locator(".lv").count()) === 3 && (await fr.locator('.lv[aria-checked="true"]').getAttribute("data-level")) === "newbie"
    && (await fr.locator(".mode").count()) === 3 && (await fr.locator(".zcard").count()) === 12, "W1 시작 화면 — 조작 난이도 3(뉴비 · 에이스 · 마스터) · 방식 3 · 십이지신 12");
  ok(/a만/.test(await txt('.lv[data-level="newbie"]')) && /a, b/.test(await txt('.lv[data-level="ace"]')) && /a, b, c/.test(await txt('.lv[data-level="master"]')), "W1b 난이도 = 넣는 값의 수 — 뉴비 a · 에이스 a, b · 마스터 a, b, c");
  let s = await S();
  const catches0 = s.save.catches;
  ok(!s.freeOpen && await fr.locator("#freeLock").isVisible(), "W2 프리 모드는 마스터 12장을 깨기 전엔 잠겨 있다");
  await fr.locator("#goFree").click();
  ok((await S()).screen === "lobby", "W3 잠긴 프리 모드를 누르면 안내만(들어가지 않음)");
  await shot("po-lobby");
  await fr.locator("#goStory").click();
  ok((await fr.locator(".chap").count()) === 12 && await fr.locator('.chap[data-ch="0"]').isEnabled() && (s.save.cleared.newbie[0] || await fr.locator('.chap[data-ch="1"]').isDisabled()), "W4 스토리 12장 — 앞 장을 깨야 다음 장이 열린다");
  await fr.locator('.chap[data-ch="0"]').click();
  ok(/진포 대첩/.test(await txt("#sTitle")) && /1380/.test(await txt("#sYear")) && /최무선/.test(await txt("#sText")) && /가로 170칸/.test(await txt("#sMeta")), "W5 1장 이야기 — 1380 진포 대첩 · 최무선 · 바다 가로 170칸");
  await fr.locator("#sGo").click();
  s = await until(myAim);
  await D("noOrb");
  const b0 = s.battle;
  ok(s.screen === "battle" && b0.mode === "story" && b0.kind === "sea" && b0.world.w === 170 && b0.sides[0].units[0].shipType === "pan" && b0.sides[1].units.length === 2 && b0.sides[1].units.every((u) => u.shipType === "jp") && b0.sides[0].tier === b0.sides[1].tier
    && (await ids()) === "in_a", "W6 전투 — 판옥선 vs 왜구 안택선 2척 · 같은 시대 · 바다 가로 170 · 뉴비는 a만 입력");
  ok((await fr.locator("#in_a").inputValue()) === "" && /a를 넣으세요/.test(await txt("#err")) && !b0.shot.ok, "W6b 처음엔 빈 칸 — 값을 넣기 전엔 포탄 길이 없다");
  // 뉴비: a만 — 쏘는 기울기 · 방향은 자동, 꼭짓점은 b = 포구 x ± s ÷ 2|a|, c = 포구 y + s² ÷ 4|a|
  await D("sea", { wind: 0 });
  await D("setInputs", { a: "-4/3" });
  s = await S();
  {
    const sh = s.battle.shot, u = active(s.battle), m = u.muzzleD, A = s.battle.autoAim;
    const eb = m.x + A.dir * A.s * 3 / 8, ec = m.y + A.s * A.s * 3 / 16;
    ok(sh.ok && Math.abs(sh.b - eb) < 1e-6 && Math.abs(sh.c - ec) < 1e-6 && /^y = −4\/3\(x − [\d.]+\)² \+ [\d.]+$/.test(sh.eq) && /b = 포구 x/.test(await txt("#ro")) && /2b − 포구 x/.test(await txt("#ro")),
      `W7 뉴비 a = −4/3 → 기울기 ${A.s}(자동) · 꼭짓점 (${sh.b}, ${sh.c}) = (포구 x ± s ÷ 2|a|, 포구 y + s² ÷ 4|a|) · ${sh.eq}`);
    ok(Math.abs(m.x - u.muzzle.x / 10) < 1e-9 && m.y === u.muzzle.y && (await txt("#ro")).includes(`포구 (${Math.round(m.x * 1000) / 1000}, ${m.y})`),
      `W7b 좌표 단위 — 가로 눈금 1 = 10칸: 포구 ${u.muzzle.x}칸 → x ${m.x}, 높이는 칸 그대로 ${m.y}`);
    const as = [];
    for (const a of ["-1", "-2", "-3"]) { const r = await D("setInputs", { a }); as.push(r.ok && !r.clipped); }
    ok(as.filter(Boolean).length >= 2, `W7c a = −1 · −2 · −3 같은 교과서 값으로 힘 안에서 쏠 수 있다 (${as.join(" · ")})`);
  }
  await D("setInputs", { a: "-0.05" });
  s = await S();
  ok(/힘이 모자라요/.test(await txt("#err")) && await fr.locator("#pwBar.max").count() === 1 && s.battle.shot.clipped && s.battle.shot.k < 1, `W8 꼭짓점까지 X + Y 가 힘 ${s.battle.shot.P}를 넘으면 경고 — 같은 각도로 ${Math.round(s.battle.shot.k * 100)}% 크기`);
  {
    await D("camSnap"); await D("noOrb");
    s = await S();
    const m = active(s.battle).muzzle, A = s.battle.autoAim, before = await fr.locator("#in_a").inputValue(), pos = await D("toCanvasRel", m.x + A.dir * 20, m.y + 10);
    await fr.locator("#cv").click({ position: pos });
    s = await S();
    const p = s.battle.probe;
    ok((await fr.locator("#in_a").inputValue()) === before && p && Math.abs(p.x - (m.x + A.dir * 20)) < 0.6 && Math.abs(p.y - (m.y + 10)) < 0.6 && /^\([\d.]+, [\d.]+\)$/.test(p.label),
      `W9 전장을 누르면 그 점의 좌표만 보여 준다(${p && p.label}) — a는 그대로(값은 늘 직접)`);
  }
  await shot("po-aim");
  // 카메라 — 전장이 화면보다 넓다
  {
    s = await S();
    const c0 = s.battle.cam;
    const box = await fr.locator("#cv").boundingBox();
    await fr.locator("#cv").hover({ position: { x: box.width * 0.62, y: box.height * 0.62 } });
    const page = fr.page();
    await page.mouse.down(); await page.mouse.move(box.x + box.width * 0.3, box.y + box.height * 0.62, { steps: 6 }); await page.mouse.up();
    const c1 = (await S()).battle.cam;
    await fr.locator('[data-cam="all"]').click();
    const c2 = (await S()).battle.cam;
    await fr.locator('[data-cam="me"]').click();
    const c3 = (await S()).battle.cam;
    ok(c0.vw < s.battle.world.w && c1.manual && c1.x > c0.x + 5 && c2.all && c2.vw >= s.battle.world.w && !c3.all && !c3.manual, `W37 카메라 — 전장 ${s.battle.world.w}칸 중 ${Math.round(c0.vw)}칸만 보임 · 끌면 둘러보기 · 「전체」 · 「내 부대」`);
  }
  // 이동 — 차례마다 이동 기운
  {
    s = await S();
    const u0 = active(s.battle), dir = Math.sign(nearFoe(s.battle, u0).x - u0.x) || 1;
    const r = await D("moveBy", dir, 0.6);
    const btn = fr.locator(dir > 0 ? "#mvR" : "#mvL");
    await btn.scrollIntoViewIfNeeded();
    const bb = await btn.boundingBox(), page = fr.page();
    const x1 = active((await S()).battle).x;
    await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await page.mouse.down(); await fr.waitForTimeout(450); await page.mouse.up();
    await fr.waitForTimeout(120);
    const u2 = active((await S()).battle);
    ok(u0.mpMax === 100 && r && (r.to - r.from) * dir > 1 && r.used > 0 && (u2.x - x1) * dir > 0.4 && u2.mp < r.mp && !(await S()).battle.moving && /\d+ \/ 100/.test(await txt("#mpNum")),
      `W38 이동 — 이동 기운 100 · 배가 ${r && r.from} → ${u2.x}(◀ ▶ 누르고 있기) · 남은 기운 ${Math.floor(u2.mp)}`);
  }
  // 바다 — 바람 · 조류 · 파도
  {
    ok(await fr.locator("#seaHud").isVisible() && /바람/.test(await txt("#seaHud")) && /조류/.test(await txt("#seaHud")) && /파도/.test(await txt("#seaHud")), "W39 바다 맵 — 바람 · 조류 · 파도 표시");
    s = await S();
    const before = s.battle.sides.map((sd) => sd.units.map((u) => u.x));
    await D("sea", { cur: 2, wave: 0 });
    const sr = await D("seaRound");
    s = await S();
    const dMe = s.battle.sides[0].units[0].x - before[0][0], dJp = Math.max(...s.battle.sides[1].units.map((u, i) => u.x - before[1][i]));
    ok(sr.cur > 0 && dMe > 0 && dJp > dMe, `W40 조류 → ${sr.cur} — 배가 떠밀린다(판옥선 +${dMe} · 잘 흔들리는 안택선 +${dJp})`);
    await D("sea", { wind: 0.2, cur: 0, wave: 0 });
    await D("setInputs", { a: "-2" });
    s = await S();
    const sh = s.battle.shot;
    ok(Math.abs(sh.f - (1 + 0.2 * sh.dir)) < 1e-9 && /바람/.test(await txt("#ro")) && new RegExp(String(1 + 0.2 * sh.dir).replace(".", "\\.") + "배").test(await txt("#ro")), `W41 바람 ${sh.dir > 0 ? "순풍" : "역풍"} 20% — 포탄 길이 가로로 ${sh.f}배`);
    await D("sea", { wind: 0 });
  }
  // 포마다 힘(X + Y 한도) · 고도 한도 · 반동
  {
    s = await S();
    const me = active(s.battle), Ps = me.spec.map((p) => p.P);
    ok(new Set(Ps).size >= 3 && me.spec.every((p) => p.H > 0 && p.H <= p.P) && /힘\(꼭짓점까지 가로 \+ 높이, 칸\)/.test(await txt("#wepInfo")) && /고도 한도/.test(await txt("#wepInfo")), `W42 포마다 힘이 달라요 — ${Ps.join(" · ")} · 고도 한도 ${me.spec.map((p) => p.H).join(" · ")}`);
    const rPan = await D("recoil", "0-0", 0), rJp = await D("recoil", "1-0", 1);
    ok(rPan > 0 && rJp > 0 && rJp < rPan, `W43 반동 — 판옥선 ${rPan.toFixed(2)}칸 · 줄에 매단 왜구 대포 ${rJp.toFixed(2)}칸(적음)`);
  }
  await D("fast", 3);
  await D("forceAI", "miss");
  const foeHp0 = (await S()).battle.sides[1].units.reduce((a, u) => a + u.hp, 0);
  const xFire = active((await S()).battle).x;
  const solW = await fireSolved();
  s = await until((s) => s.battle.phase !== "aim");
  await fr.waitForTimeout(250);
  const xRec = (await S()).battle.sides[0].units[0].x;
  s = await until((s) => s.battle.phase === "aim" || s.battle.over, 25000);
  const foeHp1 = s.battle.sides[1].units.reduce((a, u) => a + u.hp, 0);
  ok(solW && foeHp1 < foeHp0 && /명중/.test(await txt("#report")), `W10 정답 a로 쏘면 명중 — 적 체력 ${foeHp0} → ${foeHp1}`);
  ok(xRec !== xFire, `W45 쏘면 반동으로 밀린다 — x ${xFire} → ${xRec}`);
  ok(/적 포격/.test(await txt("#report")) && /y = −[\d.\/]*\(x [−+] [\d.]+\)² [+−] [\d.]+/.test(await txt("#report")), "W11 적의 포탄도 같은 꼴 y = a(x − b)² + c 로 보여 준다");
  // 찬스 구슬
  await D("fast", 1);
  s = await until(myAim);
  let e0 = s.battle.sides[0].energy;
  let q = await catchOrb("math");
  ok(q && q.kind === "math" && /\?$/.test(q.text), "W12 금빛 구슬 — 이차함수 문제: " + (q && q.text));
  await fr.locator("#qAns").fill(String(q.ans).replace("-", "−"));
  await fr.locator("#qSubmit").click();
  s = await S();
  ok(/정답/.test(await txt("#qMsg")) && Math.abs(s.battle.sides[0].energy - Math.min(100, e0 + 25)) < 0.01 && s.save.catches === catches0 + 1, "W13 맞히면 기운 +25 · 찬스 +1(십이지신 두루마리)");
  await fr.locator("#qClose").click();
  q = await catchOrb("hist");
  ok(q && q.kind === "hist" && q.opts.length === 4, "W14 보랏빛 구슬 — 역사 문제(보기 4): " + (q && q.text));
  await fr.locator(`#qChoices [data-o="${q.opts.indexOf(q.ans)}"]`).click();
  ok(/정답/.test(await txt("#qMsg")) && (await S()).save.catches === catches0 + 2, "W15 맞히면 기운 +20 · 찬스 +1");
  await shot("po-quiz");
  await fr.locator("#qClose").click();
  s = await S();
  {
    const sk = await fr.locator("#skills .sk").evaluateAll((els) => els.map((b) => ({ id: b.dataset.sk, locked: b.classList.contains("locked") })));
    const open = sk.filter((k) => !k.locked).map((k) => k.id);
    ok(sk.length === 12 && open.length === s.unlocked && (s.preview || open.join() === ["rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse", "sheep", "monkey", "rooster", "dog", "pig"].slice(0, s.unlocked).join()), `W16 모은 찬스 ${s.save.catches}개 → 십이지신 ${s.unlocked}개 열림(${open.join(", ")})`);
  }
  await D("setEnergy", 0, 100);
  await fr.locator('[data-sk="rat"]').click();
  s = await S();
  ok(s.battle.mods.rat === true && s.battle.sides[0].energy === 75, "W17 쥐 · 땅굴탄 — 기운 25를 쓰고 이번 포탄에 걸린다");
  await fr.locator('[data-sk="rat"]').click();
  ok((await S()).battle.sides[0].energy === 100, "W18 다시 누르면 취소 · 기운을 돌려받는다");
  // 애쉬래인 바람 — 상대가 조준할 때 누르면 포탄을 밀어낸다
  await D("giveGust", 0, 1);
  await D("forceAI", "hit");
  await D("setInputs", { a: "-50" });
  await fr.locator("#fire").click();
  s = await until((s) => s.battle.phase === "ai" || s.battle.over, 15000);
  if (s.battle.phase === "ai") {
    ok(await fr.locator("#gustBtn").isEnabled(), "W19 상대가 조준하는 동안 바람 단추가 켜진다");
    await fr.evaluate(() => document.getElementById("gustBtn").click());
    s = await S();
    ok(s.battle.gustArmed && s.battle.sides[0].gust === 0, "W20 누르면 애쉬래인이 숨을 모은다(바람 하나 씀)");
    s = await until((s) => s.battle.phase === "fly", 6000);
    await fr.waitForTimeout(500);
    await shot("po-gust");
    s = await until((s) => s.battle.phase === "aim" || s.battle.over, 15000);
    ok(/바람에 밀림/.test(await txt("#report")), "W21 적 포탄이 애쉬래인 바람에 밀린다(결과에 표시)");
  } else skip("W19 ~ W21 — 전투가 먼저 끝났다");
  // 끝까지 — 이기면 기록 · 다음 장이 열린다
  await D("forceAI", "miss");
  await D("fast", 4);
  for (let k = 0; k < 40; k++) {
    s = await until((s) => myAim(s) || !s.battle || s.battle.over, 25000);
    if (!s.battle || s.battle.over) break;
    if (s.quiz) await fr.locator("#qClose").click();
    await fireSolved();
    await until((s) => !s.battle || s.battle.phase !== "aim" || s.battle.over, 5000);
  }
  await fr.locator("#resultOv").waitFor({ timeout: 25000 });
  s = await S();
  ok(/승리/.test(await txt("#rTitle")) && s.save.cleared.newbie[0] === true, "W22 이기면 승리 · 뉴비 1장 기록");
  await shot("po-result");
  await fr.locator("#rActions .btn", { hasText: "장 목록" }).click();
  ok(await fr.locator('.chap[data-ch="1"]').isEnabled(), "W23 다음 장(대마도 정벌)이 열린다");
  await D("fast", 1);
  // 에이스 · 마스터 — 넣는 값이 늘어난다
  await fr.locator("#story [data-back]").click();
  await fr.locator("#unlockAll").click();
  s = await S();
  ok(s.preview && s.freeOpen && s.unlocked === 12, "W24 관리자 미리보기 — 모든 잠금 풀기(이번 접속에만)");
  await fr.locator('.lv[data-level="ace"]').click();
  await D("story", 4);
  s = await until(myAim);
  {
    const u = active(s.battle), md = u.muzzleD, dir = Math.sign(nearFoe(s.battle, u).x - u.x) || 1;
    ok((await ids()) === "in_a,in_b" && (await fr.locator("#in_a").inputValue()) === "" && (await fr.locator("#in_b").inputValue()) === "" && !s.battle.shot.ok, "W25a 에이스 — 처음엔 a, b 빈 칸");
    const sh = await D("setInputs", { a: "-2", b: String(Math.round((md.x + dir * 2.5) * 10) / 10) });
    const m = active((await S()).battle).muzzleD;
    ok(sh && sh.ok && Math.abs(sh.c - (m.y - sh.a * (m.x - sh.b) ** 2)) < 1e-9 && /c = 포구 y − a\(포구 x − b\)²/.test(await txt("#ro")) && /^y = −2\(x [−+] [\d.]+\)² [+−] [\d.]+$/.test(sh.eq),
      `W25 에이스 — a, b를 넣으면 c는 포구를 지나게 자동 (${sh && sh.eq})`);
  }
  await fr.locator("#battle #leave").click();
  await fr.locator("#story [data-back]").click();
  await fr.locator('.lv[data-level="master"]').click();
  await D("story", 7);
  s = await until(myAim);
  ok((await ids()) === "in_a,in_b,in_c" && await fr.locator("#hints").isDisabled(), "W26 마스터 — a, b, c 모두 · 도움 선 꺼짐");
  ok(s.battle.kind === "land" && s.battle.world.w === 150 && s.battle.world.h === 56 && await fr.locator("#seaHud").isHidden(), "W46 뭍 맵(남한산성) — 가로 150 · 높이 56, 바다 표시 없음");
  {
    const m = active(s.battle).muzzleD, dir = Math.sign(nearFoe(s.battle, active(s.battle)).x - active(s.battle).x) || 1;
    await D("setInputs", { a: "-0.1", b: String(Math.round((m.x + dir) * 10) / 10), c: String(m.y + 25) });
    await fr.locator("#fire").click();
    s = await S();
    ok(s.battle.phase === "aim" && /포구 .+를 지나지 않아요/.test(await txt("#err")), "W27 마스터 — 그래프가 포구를 지나지 않으면 발사되지 않는다");
  }
  {
    const sol = await D("solve");
    const r = await D("setInputs", sol);
    ok(r && r.ok, `W28 포구를 지나는 식이면 발사 준비 (a ${sol.a} · b ${sol.b} · c ${sol.c})`);
  }
  // 🐰 달토끼 도약 — 옮길 곳도 x좌표를 직접 넣는다
  {
    await D("setEnergy", 0, 100);
    s = await S();
    const u = active(s.battle), dir = Math.sign(nearFoe(s.battle, u).x - u.x) || 1;
    await fr.locator('[data-sk="rabbit"]').click();
    const vis = await fr.locator("#jumpBox").isVisible();
    let x1 = u.x;
    for (const d of [1.2, 0.8, 1.6, -1.2, -0.8]) {
      await fr.locator("#in_jump").fill(String(Math.round((u.x / 10 + dir * d) * 10) / 10));
      await fr.locator("#jumpGo").click();
      x1 = active((await S()).battle).x;
      if (x1 !== u.x) break;
    }
    ok(vis && x1 !== u.x && await fr.locator("#jumpBox").isHidden() && !(await S()).battle.moveMode, `W49 달토끼 도약 — 옮길 곳의 x좌표를 직접 넣어 옮긴다(x ${u.x / 10} → ${x1 / 10})`);
  }
  await shot("po-master");
  await fr.locator("#battle #leave").click();
  // 2인 대전 · 프리
  await fr.locator("#story [data-back]").click();
  await fr.locator('.lv[data-level="newbie"]').click();
  await fr.locator("#goVersus").click();
  ok((await fr.locator("#facs0 .fac").count()) === 15 && (await fr.locator("#maps .mapbtn").count()) === 30 && await fr.locator("#oppSeg").isHidden(), "W29 2인 대전 — 스토리 세력 15 가운데 고르기 · 맵 30");
  await fr.locator('#facs0 [data-fac="joseon5"]').click();
  await fr.locator('#facs1 [data-fac="goryeo"]').click();
  ok(/시대 차이 4단계/.test(await txt("#gapNote")) && /포의 힘 74 : 44/.test(await txt("#gapNote")), "W30 시대가 다르면 화력 차이 안내(4단계 · 포의 힘 74 : 44)");
  await fr.locator('#maps [data-map="plain"]').click();
  await fr.locator("#startSetup").click();
  s = await until(myAim);
  ok(s.battle.mode === "versus" && s.battle.sides[1].human && s.battle.sides[1].energy >= 80 && s.battle.sides[0].tier === 5 && s.battle.sides[1].tier === 1, "W31 2인 대전 시작 — 낮은 시대(고려)가 기운을 받고 시작");
  await fireSolved();
  s = await until((s) => s.battle.phase === "aim" && s.battle.turn.side === 1, 20000);
  ok(s.battle.turn.side === 1 && /2P 차례/.test(await txt("#turnName")), "W32 1P가 쏘면 2P 차례");
  await fr.locator("#battle #leave").click();
  await fr.locator("#setup [data-back]").click();
  await fr.locator("#goFree").click();
  ok((await fr.locator("#facs0 .fac").count()) === 31 && await fr.locator("#oppSeg").isVisible(), "W33 프리 모드 — 세계 31개 세력(2차 세계 대전까지) · 컴퓨터와 / 둘이서");
  await fr.locator('#facs0 [data-fac="goryeo"]').click();
  await fr.locator('#facs1 [data-fac="germany1944"]').click();
  await fr.locator("#startSetup").click();
  s = await until(myAim);
  ok(s.battle.mode === "free" && !s.battle.sides[1].human && s.battle.sides[0].energy >= 99 && s.battle.sides[1].tier === 7, "W34 프리 — 고려 vs 2차 대전 독일 · 낮은 시대가 보루 · 기운 100으로 시작");
  await shot("po-free");
  // 전체 화면
  await fr.locator("#battle .js-fs").click();
  await until((s) => s.fs === true, 3000);
  s = await S();
  ok(s.fs && await fr.evaluate(() => document.body.classList.contains("fs")), `W35 전체 화면 켜기 (${s.immersive ? "앱 상단 바 숨김" : "Fullscreen API"})`);
  await fr.locator("#battle .js-fs").click();
  await until((s) => s.fs === false, 3000);
  ok((await S()).fs === false, "W36 전체 화면 끄기");
  // 컴퓨터가 닿지 않으면 다가온다 · 체력이 줄면 이동 기운도 준다
  await D("start", { mode: "free", fac: ["goryeo", "wokou"], map: "plain", human: [true, false] });
  s = await until(myAim);
  {
    const me = s.battle.sides[0].units[0];
    ok(await D("place", "1-0", s.battle.world.w - 5), "적을 멀리 둔다");
    const far = (await S()).battle.sides[1].units[0].x;
    await D("setHp", "0-0", Math.round(me.maxHp / 2));
    await D("fast", 3);
    await D("forceAI", "miss");
    await D("setInputs", { a: "-50" });
    await fr.locator("#fire").click();
    let saw = false;
    s = await until((s) => { if (s.battle && s.battle.phase === "aimove") saw = true; return myAim(s) && s.battle.round > 1; }, 30000);
    const fx = s.battle.sides[1].units[0].x, mu = s.battle.sides[0].units[0];
    ok(saw && fx < far - 3, `W47 컴퓨터는 닿지 않으면 다가온다 — x ${far} → ${fx}`);
    ok(mu.mpMax === Math.round(100 * (0.4 + 0.6 * mu.hp / mu.maxHp)) && mu.mpMax < 100, `W48 체력(병력) ${Math.round(100 * mu.hp / mu.maxHp)}% → 이동 기운 ${mu.mpMax}`);
    await D("fast", 1);
    await D("forceAI", null);
  }
  // 안택선 — 체력이 낮을 때 맞으면 뒤집혀 가라앉을 수 있다 · 거북선(판옥선 계열)은 그렇지 않다
  await D("story", 4);
  s = await until(myAim);
  {
    const jp = s.battle.sides[1].units[1], me = s.battle.sides[0].units[0];
    let caps = null, tries = 0;
    for (; tries < 80 && !caps; tries++) {
      await D("setHp", jp.id, Math.round(jp.maxHp * 0.25));
      const r = await D("hurtUnit", jp.id, 1);
      if (r.capsized) caps = r;
    }
    let panCaps = false;
    for (let k = 0; k < 30; k++) { await D("setHp", me.id, Math.round(me.maxHp * 0.25)); const r = await D("hurtUnit", me.id, 1); if (r.capsized) panCaps = true; }
    await D("setHp", me.id, me.maxHp);
    ok(caps && !caps.alive && !panCaps, `W44 안택선은 체력 25%에서 맞으면 뒤집혀 침몰(${tries}번째) · 거북선은 안 뒤집힘`);
  }
  await fr.locator("#battle #leave").click();
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
      await page.goto(base + "po");
      await poChecks(page.mainFrame(), shot);
    } else {
      await mockSupabase(page);

      // A. 비관리자 — 막히고, 게임 파일은 내려받지 않는다
      ROLE = "student";
      await page.goto(base + "#/admin/games");
      await page.getByText("관리자만 들어올 수 있는 곳이에요.").waitFor({ timeout: 20000 });
      ok((await page.locator("iframe").count()) === 0, "A1 비관리자 — 안내만, iframe 없음");
      ok(!urls.some((u) => /slope-shot|po-minjok|sbstars/.test(u)), "A2 비관리자 — 게임 파일을 받지 않는다");

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
      ok((await el.getAttribute("sandbox")) === "allow-scripts" && /fullscreen/.test(await el.getAttribute("allow") || ""), "B2 iframe — sandbox=allow-scripts(앱 저장소 · 세션 접근 불가) · 전체 화면 허용");
      ok(urls.some((u) => /slope-shot/.test(u)) && !urls.some((u) => /po-minjok|sbstars/.test(u)), "B3 관리자 — 그때 고른 게임 파일만 받는다(따로 나뉜 파일)");
      ok((await page.locator(".fb-act").count()) === 3 && /기울기 샷/.test(await page.locator(".fb-act.pri").innerText()), "B4 상단 바에 게임 고르기 — 기울기 샷 · 포의 민족 · 선빵스타즈");
      const fr = await (await el.elementHandle()).contentFrame();
      await fr.locator("#lobby").waitFor({ timeout: 20000 });
      ok((await fr.evaluate(() => document.documentElement.dataset.theme)) === "light", "B5 앱 테마(라이트)를 문서에 심어 연다");
      const box = await el.boundingBox();
      ok(box && box.height > 600 && box.y < 80, "B6 iframe 이 상단 바 아래 화면을 채운다");
      ok(await fr.evaluate(() => { try { localStorage.getItem("x"); return false; } catch { return true; } }), "B7 게임 안에서는 앱 저장소에 닿지 않는다");

      await gameChecks(fr, shot);

      // T. 테마 — 판을 새로 열지 않고 바꾼다
      await fr.locator("#game").waitFor();
      const shots0 = await fr.evaluate(() => window.__slopeShot().shots);
      await page.evaluate(() => window.dispatchEvent(new StorageEvent("storage", { key: "ashrain-theme", newValue: "dark" })));
      await fr.waitForFunction(() => document.documentElement.dataset.theme === "dark", null, { timeout: 5000 }).catch(() => {});
      ok((await fr.evaluate(() => document.documentElement.dataset.theme)) === "dark"
        && await fr.locator("#game").isVisible() && (await fr.evaluate(() => window.__slopeShot().shots)) === shots0, "T1 앱 테마를 바꾸면 게임도 다크로 — 판은 그대로");
      await shot("games-dark");

      // M. 포의 민족 — 상단 바에서 바꾸면 그 게임 파일을 받고, 진행은 앱이 이 기기에 맡아 둔다
      await page.locator(".fb-act", { hasText: "포의 민족" }).click();
      await page.waitForFunction(() => location.hash === "#/admin/games/po", null, { timeout: 5000 });
      const el2 = page.locator('iframe.ag-frame[title="포의 민족"]');
      await el2.waitFor({ timeout: 20000 });
      ok(urls.some((u) => /po-minjok/.test(u)) && (await el2.getAttribute("sandbox")) === "allow-scripts", "M1 포의 민족 — 고를 때 파일을 받고, 같은 샌드박스에 띄운다");
      const fr2 = await (await el2.elementHandle()).contentFrame();
      await fr2.locator("#lobby").waitFor({ timeout: 20000 });
      ok((await fr2.evaluate(() => document.documentElement.dataset.theme)) === "dark", "M2 지금 앱 테마(다크)로 연다");
      await poChecks(fr2, shot);
      const saved = await page.evaluate(() => { try { return JSON.parse(localStorage.getItem("ashrain.games.po-minjok") || "null"); } catch { return null; } });
      ok(saved && saved.catches >= 2 && saved.cleared && saved.cleared.newbie[0] === true, `M3 진행은 앱이 이 기기에 맡아 둔다(ashrain.games.po-minjok · 찬스 ${saved && saved.catches} · 뉴비 1장)`);
      await page.reload();
      const el3 = page.locator('iframe.ag-frame[title="포의 민족"]');
      await el3.waitFor({ timeout: 20000 });
      const fr3 = await (await el3.elementHandle()).contentFrame();
      await fr3.locator("#lobby").waitFor({ timeout: 20000 });
      await fr3.waitForFunction(() => window.__poMinjok().save.cleared.newbie[0] === true, null, { timeout: 5000 }).catch(() => {});
      const back3 = await fr3.evaluate(() => window.__poMinjok().save);
      ok(back3.cleared.newbie[0] === true && back3.catches === saved.catches, "M4 새로고침해도 기록이 돌아온다(앱이 돌려줌)");
      await shot("po-app");
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
