// 게임(#/admin/games) 스모크 — 기울기 샷(포켓볼 · 사구 · 컬링)을 실제 브라우저로 쳐 본다.
//   node tests/smoke/games.smoke.mjs [--headed]     빌드 후(dist/ 필요): 관리자 확인 · iframe · 테마 전달 + 게임 검사
//   node tests/smoke/games.smoke.mjs --game-only    빌드 없이 게임 HTML 만 바로 열어 게임 검사
// 준비: playwright + Chromium. 2 ~ 3분 걸린다(공이 실제로 굴러간다).
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
  const num = (v) => String(Math.round(v * 1e6) / 1e6);
  const setD = async (k, v) => { const el = fr.locator(`#${k}In`); await el.fill(String(v)); await el.press("Enter"); };
  const setIcpt = (v) => fr.locator("#icpt").fill(typeof v === "number" ? num(v) : v);
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
  // 추천 샷 그대로 — 증가량은 추천대로, 절편은 공 중심을 지나게
  async function useRec(r) { await setD("dx", r.dx); await setD("dy", r.dy); await setIcpt(centerB(await S())); }
  const predNow = async () => { await fr.waitForTimeout(160); return (await S()).pred; };
  const back = async () => { await fr.locator("#back").click(); await fr.locator("#lobby").waitFor(); };
  const level = async (lv) => fr.locator(`.lv[data-level="${lv}"]`).click();
  const open = async (g, p) => { await fr.locator(`.open[data-game="${g}"][data-players="${p}"]`).click(); await fr.locator("#game").waitFor(); };
  const onGrid = (bodies, step) => bodies.every((b) => Math.abs(b.x / step - Math.round(b.x / step)) < 1e-9 && Math.abs(b.y / step - Math.round(b.y / step)) < 1e-9);
  // 다른 공(스톤)이 (x0, y0)에서 x 방향으로 [y0 + lo, y0 + hi] 띠를 지나는 길에 있는가
  const inBand = (bodies, me, x0, x1, y0, lo, hi) => bodies.some((o) => o.id !== me && o.x > x0 - 1.4 && o.x < x1 + 1.4 && o.y > y0 + lo - 1.4 && o.y < y0 + hi + 1.4);
  async function catchOrb(kind) {
    ok(await fr.evaluate((k) => window.__slopeShotDebug.spawnOrb(k), kind) === kind, `찬스 구슬(${kind === "r" ? "추천" : "x절편"})이 뜬다`);
    await fr.locator(".orb").waitFor({ state: "attached" });
    await fr.waitForTimeout(400);
    await fr.locator(".orb").dispatchEvent("click");
    await fr.locator("#overlay").waitFor();
    const q = (await S()).quiz;
    await fr.locator("#qAns").fill(String(q.ans).replace("-", "−"));
    await fr.locator("#qSubmit").click();
    const msg = await txt("#qMsg");
    await fr.locator("#qClose").click();
    return { q, msg };
  }

  // G. 게임 목록 — 난이도 · 소리
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  await fr.evaluate(() => window.__slopeShotDebug.quiet(true));      // 저절로 뜨는 구슬은 끈다(클릭이 구슬에 걸리지 않게) — 구슬은 Z에서 따로
  ok((await fr.locator(".card").count()) === 3 && (await fr.locator(".open").count()) === 6, "G1 게임 목록 — 카드 3장 · 단추 6개(혼자 · 둘이)");
  ok((await fr.locator(".lv").count()) === 3 && (await fr.locator('.lv[aria-checked="true"]').getAttribute("data-level")) === "basic", "G2 난이도 3단계(입문 · 기본 · 도전), 기본이 골라져 있다");
  const drawn = await fr.evaluate(() => [...document.querySelectorAll(".card canvas")].every((c) => {
    const d = c.getContext("2d").getImageData(c.width / 2 | 0, c.height / 2 | 0, 1, 1).data; return c.width > 0 && d[3] > 0;
  }));
  ok(drawn, "G3 카드마다 경기장 그림");
  ok(/횟수 무제한/.test(await txt('.card[data-game="pool"]')) && /몇 번이든/.test(await txt('.card[data-game="curling"]')), "G4 혼자 하기는 횟수 무제한(카드 안내)");
  await fr.locator("#lobby .js-snd").click();
  ok((await S()).sound === false && (await fr.locator("#lobby .js-snd").getAttribute("aria-pressed")) === "false", "G5 소리 끄기");
  await fr.locator("#lobby .js-snd").click();
  ok((await S()).sound === true, "G6 소리 다시 켜기");
  await shot("games-lobby");

  // P. 포켓볼 혼자 · 기본
  await open("pool", 1);
  let s = await S();
  ok(/포켓볼/.test(await txt("#gameName")) && /혼자/.test(await txt("#modeTag")) && /기본/.test(await txt("#levelTag")) && await fr.locator("#turn").isHidden(), "P1 포켓볼 · 혼자 · 기본");
  const pills = await txt("#pills");
  ok(/샷 0/.test(pills) && !/\//.test(pills) && /남은 공 3/.test(pills) && s.cap === "none" && s.inv[0].x === 1 && s.inv[0].r === 1, "P2 혼자는 횟수 무제한(샷 0, 상한 없음) · 남은 공 3 · x절편 찬스 1 · 추천 찬스 1");
  ok((await txt("#eq")) === "y = 2/3x + 14", "P3 예시 식 = 흰 공 (−12, 6)을 지나는 y = 2/3x + 14");
  ok(/세기 6² \+ 4² = 52 \/ 120 → 거리 26/.test(await txt("#powerTxt")), "P4 세기 6² + 4² = 52 / 상한 120 → 거리 26 (세기 ÷ 2)");
  ok(/오른쪽 위로/.test(await txt("#dirText")) && /큐는 반대쪽\(↙\)/.test(await txt("#dirText")) && (await txt("#flipDir")) === "↗", "P5 방향 안내 — 오른쪽 위로 · 큐는 반대쪽(↙)에서");
  let pr = await predNow();
  ok(pr && pr.cue === 2 && pr.cueNotes.includes("분수 기울기") && pr.cueNotes.includes("절편이 정수"), "P6 타점 난이도 ★2 — 격자점 · 분수 기울기 · 정수 절편");
  await setD("dx", 10); await setD("dy", 1.2);
  ok(/세기 10² \+ 1\.2² = 101\.44 \/ 120 → 거리 50\.72/.test(await txt("#powerTxt")), "P7 소수 증가량 10 · 1.2 → 세기 101.44");
  await setIcpt("7.44");
  ok((await txt("#eq")) === "y = 0.12x + 7.44", "P8 식 y = 0.12x + 7.44 (기울기 0.12)");
  pr = await predNow();
  ok(pr && pr.cue === 3 && pr.cueNotes.includes("소수 기울기"), "P9 소수 기울기 · 소수 절편 → 타점 ★3");
  await setD("dx", 30);
  s = await S();
  ok(s.dx === 30 && (await fr.locator("#dxIn").inputValue()) === "30" && /세기 30² \+ 1\.2² = 901\.44 → 상한 120 → 거리 60/.test(await txt("#powerTxt"))
    && await fr.locator("#powerBarWrap.max").count() === 1, "P10 증가량은 자유롭게(30도 그대로), 세기는 상한 120에서 멈춘다 → 거리 60");
  await fr.locator('[data-step="dy"][data-d="0.1"]').click();
  await fr.locator('[data-step="dx"][data-d="-1"]').click();
  await fr.locator('[data-step="dx"][data-d="flip"]').click();
  s = await S();
  ok(Math.abs(s.dy - 1.3) < 1e-9 && s.dx === -29, "P11 +0.1 · −1 · ± 부호 단추 (dy 1.3, dx −29)");
  await fr.locator("#flipDir").click();
  s = await S();
  ok(s.dx === 29 && Math.abs(s.dy + 1.3) < 1e-9 && /오른쪽 아래로/.test(await txt("#dirText")) && (await txt("#flipDir")) === "↘", "P12 화살표 단추 — 두 부호를 함께 바꿔 반대 방향(기울기 그대로)");
  await setIcpt("14");
  await fr.locator('[data-ib="1"]').click();
  ok((await fr.locator("#icpt").inputValue()) === "15", "P13 y절편 ▲1 → 15");
  await fr.locator('[data-ib="-0.1"]').click();
  ok((await fr.locator("#icpt").inputValue()) === "14.9", "P14 y절편 ▼0.1 → 14.9");
  // 경기장을 누르면 그쪽으로 — 쉬운 증가량, 세기는 비슷하게
  await setD("dx", 6); await setD("dy", 4);
  {
    s = await S();
    const c = s.shooter, t = s.bodies.find((b) => b.id !== "cue");
    const pos = await fr.evaluate(([x, y]) => window.__slopeShotDebug.toCanvas(x, y), [t.x, t.y]);
    await fr.locator("#cv").click({ position: pos });
    s = await S();
    const want = Math.atan2(t.y - c.y, t.x - c.x), got = Math.atan2(s.dy, s.dx);
    let da = Math.abs(want - got); if (da > Math.PI) da = 2 * Math.PI - da;
    const p = s.dx * s.dx + s.dy * s.dy;
    ok(da < 0.035 && p > 52 * 0.7 && p < 52 * 1.35 && [s.dx, s.dy].every((v) => Math.abs(v * 10 - Math.round(v * 10)) < 1e-9), `P15 경기장을 누르면 그쪽으로 방향(Δ ${s.dx}, ${s.dy} · 오차 ${(da * 180 / Math.PI).toFixed(2)}°) · 세기는 비슷하게`);
  }
  // 도움 보기 — 추천 샷
  const rec0 = await solve();
  ok(rec0 && rec0.ok && /번 공 → .+ 구멍/.test(rec0.text), `P16 추천 샷을 찾는다 (${rec0 && rec0.text} · Δ ${rec0 && rec0.dx}, ${rec0 && rec0.dy})`);
  ok(await fr.locator("#hintCard").isVisible() && /추천 샷/.test(await txt("#hintCard")) && /기울기 약/.test(await txt("#hintCard")) && /세기 약/.test(await txt("#hintCard")), "P17 도움 카드 — 무엇을 노릴지 · 기울기 · 세기");
  await fr.locator("#hints").uncheck();
  ok(await fr.locator("#hintCard").isHidden() && (await S()).hints === false, "P18 도움 보기 끄기");
  await fr.locator("#hints").check();
  await setD("dx", 6); await setD("dy", 4); await setIcpt("14");
  let r = await shoot();
  ok(/정타/.test(r) && /입력: y = 2\/3x \+ 14/.test(r) && /예측 난이도/.test(r), "P19 예시 식으로 치면 정타 · 결과에 예측 난이도");
  s = await S();
  ok(onGrid(s.bodies, 0.5), "P20 기본 — 멈춘 공은 반 칸(0.5) 격자로 옮겨진다");
  ok(await fr.evaluate(() => document.getElementById("report").parentElement.id === "outBelow"), "P21 자리가 넉넉하면 샷 결과는 테이블 아래에");
  await shot("games-pool");
  await setIcpt("7/3");
  ok((await txt("#eq")) === "y = 2/3x + 7/3", "P22 분수 절편은 분수 그대로");
  await setIcpt("−7/3");
  ok((await txt("#eq")) === "y = 2/3x − 7/3", "P23 음의 분수");
  await setIcpt("abc");
  ok(/수로 읽을 수 없어요/.test(await txt("#err")) && await fr.locator("#shoot").isDisabled(), "P24 읽을 수 없는 절편 → 안내 · 치기 잠김");

  await live();
  let c = (await S()).shooter;
  await setD("dx", 0); await setD("dy", 6);
  ok((await txt("#icptLabel")) === "x = a 의 a", "P25 x 증가량 0 → x = a 꼴");
  await setIcpt(c.x);
  pr = await predNow();
  ok(/^x = /.test(await txt("#eq")) && /세기 0² \+ 6² = 36/.test(await txt("#powerTxt")) && pr && pr.cueNotes.some((n) => /x = a 꼴/.test(n)), "P26 x = a · 세기는 y 증가량 · 타점 메모");
  r = await shoot();
  ok(/정타/.test(r) && /입력: x = /.test(r), "P27 수직선 x = a 로 정타");

  await live();
  c = (await S()).shooter;
  await setD("dx", 6); await setD("dy", 0);
  ok((await txt("#icptLabel")) === "y = b 의 b", "P28 y 증가량 0 → y = b 꼴");
  await setIcpt(c.y);
  r = await shoot();
  ok(/정타/.test(r), "P29 수평선 y = b 로 정타");

  await live();
  c = (await S()).shooter;
  await setD("dx", 4);
  await setIcpt(c.y + 0.3);                  // 오른쪽으로 갈 때 직선이 공 중심 위(진행 방향 왼쪽)로 0.3 — 반지름 0.6의 절반
  r = await shoot();
  ok(/왼쪽 스핀 50%/.test(r) && /평행한 직선/.test(r), "P30 중심에서 0.3 비껴 → 왼쪽 스핀 50% · 평행선 식");

  await live();
  c = (await S()).shooter;
  await setIcpt(c.y + 2);
  r = await shoot();
  ok(/헛스윙/.test(r), "P31 반지름 밖 → 헛스윙");

  // 추천 찬스(강함) — 증가량 추천 → (구슬로 하나 더) → y절편 추천 → 그대로 치면 들어간다
  await live();
  s = await S();
  ok(s.inv[0].r === 1 && await fr.locator("#cR").isEnabled(), "P32 추천 찬스 1개");
  await fr.locator("#cR").click();
  ok(await fr.locator("#rPick").isVisible(), "P33 추천 찬스를 누르면 증가량 추천 · y절편 추천 고르기");
  await fr.locator('[data-rp="delta"]').click();
  await fr.waitForFunction(() => { const s = window.__slopeShot(); return s.recInfo && s.recInfo.kind !== "wait"; }, null, { timeout: 15000 });
  s = await S();
  const rec1 = s.rec;
  ok(s.recInfo.kind === "delta" && rec1 && rec1.ok && s.dx === rec1.dx && s.dy === rec1.dy && s.inv[0].r === 0 && /추천 찬스 · 증가량/.test(await txt("#calcBox")), `P34 증가량 추천 — Δ ${s.dx}, ${s.dy}로 채우고 찬스 하나 씀`);
  ok(await fr.locator("#cR").isDisabled(), "P35 추천 찬스 0개 → 잠김");
  {
    const { q, msg } = await catchOrb("r");
    ok(q.kind === "r" && /정답!/.test(msg) && (await S()).inv[0].r === 1, "P36 금빛 구슬 문제를 맞히면 추천 찬스 +1");
  }
  await fr.locator("#cR").click(); await fr.locator('[data-rp="icpt"]').click();
  s = await S();
  ok(s.recInfo.kind === "icpt" && /b = y₀ − 기울기 × x₀|가로선이라|세로선이라/.test(await txt("#calcText")) && s.inv[0].r === 0, "P37 y절편 추천 — 공 중심을 지나는 b를 계산 과정과 함께");
  pr = await predNow();
  ok(pr && pr.cue === 1, "P38 추천 y절편을 쓰면 타점 난이도 ★1");
  const left0 = (await txt("#pills")).match(/남은 공 (\d)/)[1];
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && /목표 공 \d개 성공/.test(r) && /추천 찬스\(y절편\) 사용/.test(r), `P39 추천대로 치면 그대로 들어간다(미리 굴려 본 것 = 실제) · 남은 공 ${left0} → ${(await txt("#pills")).match(/남은 공 (\d)/)[1]}`);

  // x절편 찬스(약함) — y절편 대신 x절편을 직접 계산해 넣는다
  await live();
  s = await S();
  ok(s.inv[0].x === 1, "P40 x절편 찬스 1개");
  await setD("dx", 4); await setD("dy", 2);
  await fr.locator("#cX").click();
  s = await S();
  ok(s.xmode && (await txt("#icptLabel")) === "x절편 a (x절편 찬스)" && /x절편 = x₀ − y₀ ÷ 기울기/.test(await txt("#calcText")), "P41 x절편 찬스 — 입력 칸이 x절편으로(계산은 직접)");
  await fr.locator("#cX").click();
  s = await S();
  ok(!s.xmode && s.inv[0].x === 1 && (await txt("#icptLabel")) === "y절편 b", "P42 다시 누르면 취소 — 쓰지 않으면 줄지 않는다");
  await fr.locator("#cX").click();
  c = (await S()).shooter;
  await setIcpt(c.x - c.y * 2);              // 기울기 1/2 → x절편 = x₀ − y₀ ÷ (1/2)
  ok(/x절편 .+ → y절편/.test(await txt("#eqSub")), "P43 x절편을 넣으면 y절편으로 바꿔 식을 보여 준다");
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && /x절편 찬스 사용/.test(r) && s.inv[0].x === 0 && !s.xmode, "P44 x절편으로 정타 · 찬스는 칠 때 하나 씀");
  ok(await fr.locator("#cX").isDisabled(), "P45 x절편 찬스 0개 → 잠김");

  // Q. 포켓볼 둘이 — 찬스는 사람마다
  await back();
  await open("pool", 2);
  s = await S();
  ok(await fr.locator("#turn").isVisible() && /1P 차례/.test(await txt("#turnName")), "Q1 둘이 — 1P 차례");
  ok(/1P 0 : 0 2P/.test(await txt("#pills")) && /남은 공 5/.test(await txt("#pills")) && /샷 0 \/ 30/.test(await txt("#pills")) && s.bodies.length === 6
    && s.inv.map((i) => `${i.x}${i.r}`).join() === "11,11", "Q2 공 5개 · 샷 0 / 30 · 찬스는 사람마다(x절편 1 · 추천 1)");
  await setIcpt(100);
  r = await shoot();
  s = await S();
  ok(/헛스윙/.test(r) && s.turn === 1 && /→ 2P 차례/.test(r), "Q3 1P 헛스윙 → 2P 차례");
  await fr.locator("#cR").click(); await fr.locator('[data-rp="icpt"]').click();
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && s.inv.map((i) => `${i.x}${i.r}`).join() === "11,10", "Q4 2P가 쓴 추천 찬스는 2P 것만 준다");

  // C. 사구 — 둘이(1P 흰 공 · 2P 노란 공), 혼자(추천대로 치면 득점)
  await back();
  await open("carom", 2);
  s = await S();
  ok(/1P 차례/.test(await txt("#turnName")) && /흰 공/.test(await txt("#turnTag")) && s.shooter.id === "cue" && /\/ 150/.test(await txt("#powerTxt")), "C1 사구 둘이 — 1P는 흰 공 · 세기 상한 150");
  await setIcpt(100);
  await shoot();
  s = await S();
  ok(s.turn === 1 && s.shooter.id === "y" && /노란 공/.test(await txt("#turnTag")), "C2 2P는 노란 공");
  c = s.shooter;
  await setIcpt(c.y - c.x / 3);              // 기본 기울기 2/6 = 1/3
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && (/득점: \+1점/.test(r) ? s.turn === 1 && /한 번 더/.test(r) : s.turn === 0 && /→ 1P 차례/.test(r)), "C3 2P 정타 — 득점하면 한 번 더, 아니면 1P");
  await back();
  await open("carom", 1);
  {
    const rc = await solve();
    ok(rc && rc.ok && /빨간 공 2개/.test(rc.text), `C4 사구 추천 샷 (${rc && rc.text} · Δ ${rc && rc.dx}, ${rc && rc.dy})`);
    if (rc && rc.ok) {
      await useRec(rc);
      r = await shoot();
      ok(/정타/.test(r) && /득점: \+1점/.test(r) && /점수 1 \/ 3/.test(await txt("#pills")), "C5 추천대로 치면 빨간 공 2개 — 득점");
    }
    await shot("games-carom");
  }

  // K. 컬링 혼자 · 입문 — 단계 · 몇 번이든 다시
  await back();
  await level("intro");
  await open("curling", 1);
  s = await S();
  const opp0 = s.bodies.filter((b) => b.team === 1);
  ok(/단계 1/.test(await txt("#pills")) && /1번째 시도/.test(await txt("#pills")) && opp0.length === 1 && s.shooter.x === -16 && s.shooter.y === 10
    && s.bodies.find((b) => b.id === s.shooter.id).waiting, "K1 단계 1 — 상대 스톤 1개 · 내 스톤은 (−16, 10)");
  ok((await txt("#eq")) === "y = 10" && /던지기/.test(await txt("#shoot")) && /7\.2² \+ 0² = 51\.84 \/ 100 → 거리 25\.92/.test(await txt("#powerTxt")), "K2 예시 y = 10 · 세기 51.84 / 상한 100 → 거리 25.92");
  pr = await predNow();
  ok(pr && pr.cue === 1 && pr.tgtWho === "스톤 → 버튼" && s.rec && s.rec.ok, `K3 예측 — 타점 ★1 · 목표 ★${pr && pr.tgt} · 추천 샷이 미리 준비됨`);
  await shot("games-curling");
  r = await shoot();
  s = await S();
  ok(/회전 없이 똑바로/.test(r) && /단계 1 통과/.test(r) && s.waitStage, "K4 입문 단계 1 — 곧게 던지면 통과(입문 판은 y = b 로 이길 수 있게 놓인다)");
  await ready();
  s = await S();
  ok(s.stage === 2 && s.tries === 0 && s.shooter.x === -16 && Number.isInteger(s.shooter.y) && s.shooter.y >= 8 && s.shooter.y <= 12 && /단계 2/.test(await txt("#pills")), `K5 다음 단계 — 단계 2 · 내 스톤 (−16, ${s.shooter.y})`);
  // 일부러 짧게(호그 라인 전에 멈춤) → 같은 판으로 다시
  const opp2 = s.bodies.filter((b) => b.team === 1).map((b) => `${b.id}:${b.x},${b.y}`).join();
  await setD("dx", 3); await setIcpt(s.shooter.y);
  r = await shoot();
  ok(/호그 라인/.test(r) && /같은 판으로 다시/.test(r), "K6 짧으면 호그 라인 전에 제거 · 같은 판으로 다시");
  await ready();
  s = await S();
  ok(s.stage === 2 && s.tries === 1 && /2번째 시도/.test(await txt("#pills")) && s.bodies.filter((b) => b.team === 1).map((b) => `${b.id}:${b.x},${b.y}`).join() === opp2
    && s.bodies.filter((b) => b.team === 0).length === 1, "K7 다시 — 단계 그대로 · 2번째 시도 · 상대 스톤은 제자리 · 내 스톤 1개");
  // 휨: 중심에서 0.4 비껴 → 반시계 회전 → 진행 방향 왼쪽(+y)으로
  {
    const st0 = s.shooter;
    await setD("dx", 7.2); await setD("dy", 0);
    await setIcpt(st0.y + 0.4);
    const blocked = inBand(s.bodies, st0.id, -16, 10, st0.y, -0.4, 3);
    r = await shoot();
    const f = (await S()).bodies.find((b) => b.id === st0.id);
    ok(/반시계 방향 회전 67%/.test(r) && /왼쪽으로 휨/.test(r), "K8 중심에서 0.4 비껴 → 반시계 회전 67% · 왼쪽으로 휨");
    if (!blocked) ok(f && f.y > st0.y + 0.8 && f.x > 6, `K9 진행 방향 왼쪽(+y)으로 휘었다 (y ${st0.y} → ${f && f.y.toFixed(2)})`);
    else console.log("skip - K9 (길에 다른 스톤)");
    await ready();
  }
  // 기본 — 추천대로 던지면 통과
  await back();
  await level("basic");
  await open("curling", 1);
  {
    s = await S();
    ok(s.bodies.filter((b) => b.team === 1).length >= 1 && Number.isInteger(s.shooter.y) && s.shooter.y >= 7 && s.shooter.y <= 13, "K10 기본 — 투구 자리 높이가 바뀐다(7 ~ 13)");
    const rc = await solve();
    ok(rc && rc.ok, `K11 기본 판 추천 (${rc && rc.text} · Δ ${rc && rc.dx}, ${rc && rc.dy})`);
    await useRec(rc);
    r = await shoot();
    ok(/단계 1 통과/.test(r), "K12 추천대로 던지면 통과(미리 굴려 본 것 = 실제)");
    await ready();
    ok((await S()).stage === 2, "K13 단계 2로");
  }

  // L. 컬링 둘이 — 8번 모두 놓치면 블랭크 엔드
  await back();
  await open("curling", 2);
  s = await S();
  ok(/1P 차례/.test(await txt("#turnName")) && /빨간 스톤/.test(await txt("#turnTag")) && s.bodies.length === 1, "L1 컬링 둘이 — 1P(빨간 스톤)부터");
  let alt = true;
  for (let i = 0; i < 8; i++) {
    s = await S();
    if (s.turn !== i % 2 || s.shooter.id !== `s${i % 2}-${(i >> 1) + 1}`) alt = false;
    await setIcpt(100);
    await shoot();
  }
  ok(alt, "L2 4개씩 번갈아 · 마지막은 2P");
  ok(/블랭크 엔드/.test(await txt("#toast")) && await fr.locator("#turn").isHidden() && await fr.locator("#shoot").isDisabled(), "L3 하우스가 비면 블랭크 엔드 · 치기 잠김");

  // I. 입문 — 격자점 · 찬스 많이 · 도움 켬
  await back();
  await level("intro");
  await open("pool", 1);
  s = await S();
  ok(s.level === "intro" && s.inv[0].x === 2 && s.inv[0].r === 2 && s.hints && /입문/.test(await txt("#levelTag")) && onGrid(s.bodies, 1), "I1 입문 — x절편 찬스 2 · 추천 찬스 2 · 도움 켬 · 공이 모두 격자점");
  await setD("dx", 7.3);                     // 일부러 어긋나게
  await setIcpt(5.1);
  await shoot();
  s = await S();
  ok(onGrid(s.bodies, 1), "I2 입문 — 친 뒤에도 공은 격자점으로");

  // D. 도전 — 찬스 없이 · 도움 끔
  await back();
  await level("pro");
  await open("pool", 1);
  s = await S();
  ok(s.level === "pro" && s.inv[0].x === 0 && s.inv[0].r === 0 && await fr.locator("#cX").isDisabled() && await fr.locator("#cR").isDisabled(), "D1 도전 — 찬스 0개");
  ok(!s.hints && await fr.locator("#hintCard").isHidden() && !(await fr.locator("#hints").isChecked()), "D2 도전 — 도움 보기는 꺼진 채로 시작");

  // Z. 찬스 구슬 — 공보다 작게, 은빛(x절편) · 금빛(추천)
  {
    ok(await fr.evaluate(() => window.__slopeShotDebug.spawnOrb("x")) === "x", "Z1 은빛 구슬(x절편 찬스)이 뜬다");
    await fr.locator(".orb").waitFor({ state: "attached" });
    await fr.waitForTimeout(500);
    const box = await fr.locator(".orb .core").boundingBox(), u = (await S()).unit;
    ok(box && box.width < 1.2 * u && box.width > 8, `Z2 구슬은 공보다 작다 (구슬 ${box && box.width.toFixed(1)}px < 공 지름 ${(1.2 * u).toFixed(1)}px)`);
    await shot("games-orb");
    await fr.locator(".orb").dispatchEvent("click");
    await fr.locator("#overlay").waitFor();
    const q = (await S()).quiz;
    ok(!!q && q.kind === "x" && (await txt("#qText")) === q.text && /x절편 찬스 문제/.test(await txt("#qTitle")), "Z3 구슬을 누르면 x절편 찬스 문제(사칙 계산)");
    await fr.locator("#qAns").fill(String(q.ans).replace("-", "−"));
    await fr.locator("#qSubmit").click();
    ok(/정답!/.test(await txt("#qMsg")) && (await S()).inv[0].x === 1, "Z4 맞히면 x절편 찬스 +1");
    await fr.locator("#qClose").click();
    ok(await fr.locator("#overlay").isHidden(), "Z5 닫기");
    const g = await catchOrb("r");
    ok(g.q.kind === "r" && /기울기|절편/.test(g.q.text) && /정답!/.test(g.msg) && (await S()).inv[0].r === 1, "Z6 금빛 구슬 — 일차함수 문제 · 맞히면 추천 찬스 +1");
  }

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
      ok((await el.getAttribute("sandbox")) === "allow-scripts" && /fullscreen/.test(await el.getAttribute("allow") || ""), "B2 iframe — sandbox=allow-scripts(앱 저장소 · 세션 접근 불가) · 전체 화면 허용");
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
