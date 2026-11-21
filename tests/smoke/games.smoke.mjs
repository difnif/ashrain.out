// 게임(#/admin/games) 스모크 — 기울기 샷(포켓볼 · 사구 · 컬링)을 실제 브라우저로 쳐 본다.
//   node tests/smoke/games.smoke.mjs [--headed]     빌드 후(dist/ 필요): 관리자 확인 · iframe · 테마 전달 + 게임 검사
//   node tests/smoke/games.smoke.mjs --game-only    빌드 없이 게임 HTML 만 바로 열어 게임 검사
// 준비: playwright + Chromium. 1 ~ 2분 걸린다(공이 실제로 굴러간다).
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
  const setD = async (k, v) => { const el = fr.locator(`#${k}In`); await el.fill(String(v)); await el.press("Enter"); };
  const setIcpt = (v) => fr.locator("#icpt").fill(typeof v === "number" ? num(v) : v);
  async function live() { if ((await S()).over) await fr.locator("#newGame").click(); }
  async function shoot() {
    const n = (await S()).shots;
    await fr.locator("#shoot").click();
    await fr.waitForFunction((k) => { const s = window.__slopeShot(); return s.shots === k && !s.moving; }, n + 1, { timeout: 30000, polling: 100 });
    return report();
  }
  const predNow = async () => { await fr.waitForTimeout(160); return (await S()).pred; };
  const back = async () => { await fr.locator("#back").click(); await fr.locator("#lobby").waitFor(); };
  const level = async (lv) => fr.locator(`.lv[data-level="${lv}"]`).click();
  const open = async (g, p) => { await fr.locator(`.open[data-game="${g}"][data-players="${p}"]`).click(); await fr.locator("#game").waitFor(); };
  const onGrid = (bodies, step) => bodies.every((b) => Math.abs(b.x / step - Math.round(b.x / step)) < 1e-9 && Math.abs(b.y / step - Math.round(b.y / step)) < 1e-9);
  // 다른 공(스톤)이 (x0, y0)에서 x 방향으로 [y0 + lo, y0 + hi] 띠를 지나는 길에 있는가
  const inBand = (bodies, me, x0, x1, y0, lo, hi) => bodies.some((o) => o.id !== me && o.x > x0 - 1.4 && o.x < x1 + 1.4 && o.y > y0 + lo - 1.4 && o.y < y0 + hi + 1.4);

  // G. 게임 목록 — 난이도 · 소리 · 전체 화면
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  ok((await fr.locator(".card").count()) === 3 && (await fr.locator(".open").count()) === 6, "G1 게임 목록 — 카드 3장 · 단추 6개(혼자 · 둘이)");
  ok((await fr.locator(".lv").count()) === 3 && (await fr.locator('.lv[aria-checked="true"]').getAttribute("data-level")) === "basic", "G2 난이도 3단계(입문 · 기본 · 도전), 기본이 골라져 있다");
  const drawn = await fr.evaluate(() => [...document.querySelectorAll(".card canvas")].every((c) => {
    const d = c.getContext("2d").getImageData(c.width / 2 | 0, c.height / 2 | 0, 1, 1).data; return c.width > 0 && d[3] > 0;
  }));
  ok(drawn, "G3 카드마다 경기장 그림");
  await fr.locator("#lobby .js-snd").click();
  ok((await S()).sound === false && (await fr.locator("#lobby .js-snd").getAttribute("aria-pressed")) === "false", "G4 소리 끄기");
  await fr.locator("#lobby .js-snd").click();
  ok((await S()).sound === true, "G5 소리 다시 켜기");
  await shot("games-lobby");

  // P. 포켓볼 혼자 · 기본
  await open("pool", 1);
  let s = await S();
  ok(/포켓볼/.test(await txt("#gameName")) && /혼자/.test(await txt("#modeTag")) && /기본/.test(await txt("#levelTag")) && await fr.locator("#turn").isHidden(), "P1 포켓볼 · 혼자 · 기본");
  ok(/샷 0 \/ 12/.test(await txt("#pills")) && /남은 공 3/.test(await txt("#pills")) && s.inv[0] === 1, "P2 샷 0 / 12 · 남은 공 3 · 절편 찬스 1개");
  ok((await txt("#eq")) === "y = 2/3x + 14", "P3 예시 식 = 흰 공 (−12, 6)을 지나는 y = 2/3x + 14");
  ok(/세기 6² \+ 4² = 52 → 거리 26/.test(await txt("#powerTxt")), "P4 세기 6² + 4² = 52 → 거리 26 (세기 ÷ 2)");
  let pr = await predNow();
  ok(pr && pr.cue === 2 && pr.cueNotes.includes("분수 기울기") && pr.cueNotes.includes("절편이 정수"), "P5 타점 난이도 ★2 — 격자점 · 분수 기울기 · 정수 절편");
  await setD("dx", 10); await setD("dy", 1.2);
  ok(/기울기 0\.12/.test(await txt("#dirHint")) && /세기 10² \+ 1\.2² = 101\.44 → 거리 50\.72/.test(await txt("#powerTxt")), "P6 소수 증가량 10 · 1.2 → 기울기 0.12 · 세기 101.44");
  await setIcpt("7.44");
  ok((await txt("#eq")) === "y = 0.12x + 7.44", "P7 식 y = 0.12x + 7.44");
  pr = await predNow();
  ok(pr && pr.cue === 3 && pr.cueNotes.includes("소수 기울기"), "P8 소수 기울기 · 소수 절편 → 타점 ★3");
  await setD("dx", 30);
  ok((await S()).dx === 12 && (await fr.locator("#dxIn").inputValue()) === "12", "P9 상한 12 — 30을 넣으면 12");
  await fr.locator('[data-step="dy"][data-d="0.1"]').click();
  await fr.locator('[data-step="dx"][data-d="-1"]').click();
  await fr.locator('[data-step="dx"][data-d="flip"]').click();
  s = await S();
  ok(Math.abs(s.dy - 1.3) < 1e-9 && s.dx === -11, "P10 +.1 · −1 · ± 단추 (dy 1.3, dx −11)");
  await setD("dx", 6); await setD("dy", 4); await setIcpt("14");
  // 목표 공을 똑바로 겨누면 목표 난이도가 나온다
  {
    s = await S();
    const c = s.shooter, t = s.bodies.find((b) => b.id !== "cue");
    const D = Math.hypot(t.x - c.x, t.y - c.y);
    const k = Math.sqrt(2 * (D + 3)) / D;            // 세기 ≥ 2 × (거리 + 3)
    let dx = (t.x - c.x) * k, dy = (t.y - c.y) * k; const big = Math.max(Math.abs(dx), Math.abs(dy)); if (big > 12) { dx *= 12 / big; dy *= 12 / big; }
    await setD("dx", Math.round(dx * 100) / 100); await setD("dy", Math.round(dy * 100) / 100);
    pr = await predNow();
    ok(pr && pr.tgt >= 1 && /번 공/.test(pr.tgtWho), `P11 목표 공을 겨누면 목표 난이도 ★${pr && pr.tgt} (${pr && pr.tgtWho})`);
    await setD("dx", 6); await setD("dy", 4);
  }
  let r = await shoot();
  ok(/정타/.test(r) && /입력: y = 2\/3x \+ 14/.test(r) && /예측 난이도/.test(r), "P12 예시 식으로 치면 정타 · 결과에 예측 난이도");
  s = await S();
  ok(onGrid(s.bodies, 0.5), "P13 기본 — 멈춘 공은 반 칸(0.5) 격자로 옮겨진다");
  await shot("games-pool");
  await setIcpt("7/3");
  ok((await txt("#eq")) === "y = 2/3x + 7/3", "P14 분수 절편은 분수 그대로");
  await setIcpt("−7/3");
  ok((await txt("#eq")) === "y = 2/3x − 7/3", "P15 음의 분수");
  await setIcpt("abc");
  ok(/수로 읽을 수 없어요/.test(await txt("#err")) && await fr.locator("#shoot").isDisabled(), "P16 읽을 수 없는 절편 → 안내 · 치기 잠김");

  await live();
  let c = (await S()).shooter;
  await setD("dx", 0); await setD("dy", 6);
  ok((await txt("#icptLabel")) === "x = a 의 a", "P17 x 증가량 0 → x = a 꼴");
  await setIcpt(c.x);
  pr = await predNow();
  ok(/^x = /.test(await txt("#eq")) && /세기 0² \+ 6² = 36/.test(await txt("#powerTxt")) && pr && pr.cueNotes.some((n) => /x = a 꼴/.test(n)), "P18 x = a · 세기는 y 증가량 · 타점 메모");
  r = await shoot();
  ok(/정타/.test(r) && /입력: x = /.test(r), "P19 수직선 x = a 로 정타");

  await live();
  c = (await S()).shooter;
  await setD("dx", 6); await setD("dy", 0);
  ok((await txt("#icptLabel")) === "y = b 의 b", "P20 y 증가량 0 → y = b 꼴");
  await setIcpt(c.y);
  r = await shoot();
  ok(/정타/.test(r), "P21 수평선 y = b 로 정타");

  await live();
  c = (await S()).shooter;
  await setD("dx", 4);
  await setIcpt(c.y + 0.3);                  // 오른쪽으로 갈 때 직선이 공 중심 위(진행 방향 왼쪽)로 0.3 — 반지름 0.6의 절반
  r = await shoot();
  ok(/왼쪽 스핀 50%/.test(r) && /평행한 직선/.test(r), "P22 중심에서 0.3 비껴 → 왼쪽 스핀 50% · 평행선 식");

  await live();
  c = (await S()).shooter;
  await setIcpt(c.y + 2);
  r = await shoot();
  ok(/헛스윙/.test(r), "P23 반지름 밖 → 헛스윙");

  await live();
  s = await S();
  const inv0 = s.inv[0];
  ok(inv0 >= 1 && await fr.locator("#chanceBtn").isEnabled(), "P24 절편 찬스 단추");
  await fr.locator("#chanceBtn").click();
  ok(await fr.locator("#chancePick").isVisible(), "P25 찬스를 누르면 x절편 · y절편 고르기");
  await setD("dx", 4); await setD("dy", 2);
  await fr.locator('[data-pick="x"]').click();
  ok((await S()).chance === "x" && await fr.locator("#calcBox").isVisible() && /x절편 = /.test(await txt("#calcText")) && await fr.locator("#icptField").isHidden(), "P26 x절편으로 — 계산 과정과 함께 채움, 입력 칸은 숨김");
  await fr.locator("#chanceBtn").click();
  ok((await S()).chance === null && (await S()).inv[0] === inv0, "P27 찬스 취소 — 쓰지 않으면 줄지 않는다");
  await fr.locator("#chanceBtn").click(); await fr.locator('[data-pick="y"]').click();
  ok(/b = /.test(await txt("#calcText")), "P28 y절편으로 — b = y₀ − m × x₀");
  pr = await predNow();
  ok(pr && pr.cue === 1, "P29 찬스를 쓰면 타점 난이도 ★1");
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && /절편 찬스\(y절편\) 사용/.test(r) && s.inv[0] === inv0 - 1 && s.chance === null, "P30 찬스로 치면 정타 · 하나 씀");
  if (s.inv[0] === 0) ok(await fr.locator("#chanceBtn").isDisabled(), "P31 찬스 0개 → 잠김");

  // Q. 포켓볼 둘이 — 찬스는 사람마다
  await back();
  await open("pool", 2);
  s = await S();
  ok(await fr.locator("#turn").isVisible() && /1P 차례/.test(await txt("#turnName")), "Q1 둘이 — 1P 차례");
  ok(/1P 0 : 0 2P/.test(await txt("#pills")) && /남은 공 5/.test(await txt("#pills")) && /샷 0 \/ 30/.test(await txt("#pills")) && s.bodies.length === 6 && s.inv.join() === "1,1", "Q2 공 5개 · 샷 0 / 30 · 찬스 1개씩");
  await setIcpt(100);
  r = await shoot();
  s = await S();
  ok(/헛스윙/.test(r) && s.turn === 1 && /→ 2P 차례/.test(r), "Q3 1P 헛스윙 → 2P 차례");
  await fr.locator("#chanceBtn").click(); await fr.locator('[data-pick="y"]').click();
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && s.inv.join() === "1,0", "Q4 2P가 쓴 찬스는 2P 것만 준다");

  // C. 사구 둘이 — 1P 흰 공 · 2P 노란 공
  await back();
  await open("carom", 2);
  s = await S();
  ok(/1P 차례/.test(await txt("#turnName")) && /흰 공/.test(await txt("#turnTag")) && s.shooter.id === "cue", "C1 사구 둘이 — 1P는 흰 공");
  await setIcpt(100);
  await shoot();
  s = await S();
  ok(s.turn === 1 && s.shooter.id === "y" && /노란 공/.test(await txt("#turnTag")), "C2 2P는 노란 공");
  c = s.shooter;
  await setIcpt(c.y - c.x / 3);              // 기본 기울기 2/6 = 1/3
  r = await shoot();
  s = await S();
  ok(/정타/.test(r) && (/득점: \+1점/.test(r) ? s.turn === 1 && /한 번 더/.test(r) : s.turn === 0 && /→ 1P 차례/.test(r)), "C3 2P 정타 — 득점하면 한 번 더, 아니면 1P");

  // K. 컬링 혼자 — 똑바로 · 휨
  await back();
  await open("curling", 1);
  s = await S();
  ok(/스톤 0 \/ 6/.test(await txt("#pills")) && s.bodies.filter((b) => b.team === 1).length === 2 && s.shooter.x === -16 && s.bodies.find((b) => b.id === s.shooter.id).waiting, "K1 상대 스톤 2개 · 내 스톤은 투구선(x = −16)");
  ok((await txt("#eq")) === `y = ${String(s.shooter.y).replace("-", "−")}` && /던지기/.test(await txt("#shoot")) && /7\.2² \+ 0² = 51\.84 → 거리 25\.92/.test(await txt("#powerTxt")), "K2 예시 — x 증가량 7.2 · 세기 51.84 → 거리 25.92");
  pr = await predNow();
  ok(pr && pr.cue === 1 && pr.tgt >= 1 && pr.tgtWho === "스톤 → 버튼", `K3 예측 — 타점 ★1(y = b) · 목표 ★${pr && pr.tgt}`);
  let st0 = s.shooter, clear = !inBand(s.bodies, st0.id, -16, 9.92, st0.y, 0, 0);
  r = await shoot();
  s = await S();
  ok(/회전 없이 똑바로/.test(r), "K4 정타 → 회전 없이");
  const f0 = s.bodies.find((b) => b.id === st0.id);
  if (clear) ok(f0 && Math.abs(f0.x - 9.92) < 0.3 && Math.abs(f0.y - st0.y) < 0.01, `K5 막힘이 없으면 −16 + 25.92 = 9.92 근처에 멈춘다 (${f0 && f0.x.toFixed(2)})`);
  else console.log("skip - K5 (길에 다른 스톤)");
  ok(s.shooter.id === "s0-2" && s.shooter.x === -16 && /스톤 1 \/ 6/.test(await txt("#pills")), "K6 다음 스톤(2번)이 투구선에");
  let curled = null;
  for (let tries = 0; tries < 10 && !curled; tries++) {
    await fr.locator("#newGame").click();
    s = await S(); st0 = s.shooter;
    if (inBand(s.bodies, st0.id, -16, 10, st0.y, -0.4, 3)) continue;
    await setIcpt(st0.y + 0.4);              // 직선이 중심 위(진행 방향 왼쪽)로 0.4 → 반시계 회전 67% → 왼쪽(+y)으로 휜다
    r = await shoot();
    curled = { r, y0: st0.y, f: (await S()).bodies.find((b) => b.id === st0.id) };
  }
  if (curled) {
    ok(/반시계 방향 회전 67%/.test(curled.r) && /왼쪽으로 휨/.test(curled.r), "K7 중심에서 0.4 비껴 → 반시계 회전 67% · 왼쪽으로 휨");
    ok(curled.f && curled.f.y > curled.y0 + 0.8 && curled.f.x > 6, `K8 진행 방향 왼쪽(+y)으로 휘었다 (y ${curled.y0} → ${curled.f && curled.f.y.toFixed(2)})`);
  } else ok(false, "K7 10판 안에 길이 빈 배치가 나와야 한다");
  await shot("games-curling");

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

  // I. 입문 — 격자점 · 좌표 표시 · 찬스 3
  await back();
  await level("intro");
  await open("pool", 1);
  s = await S();
  ok(s.level === "intro" && s.inv[0] === 3 && /입문/.test(await txt("#levelTag")) && onGrid(s.bodies, 1), "I1 입문 — 찬스 3개 · 공이 모두 격자점");
  await setD("dx", 7.3);                     // 일부러 어긋나게
  await setIcpt(5.1);
  await shoot();
  s = await S();
  ok(onGrid(s.bodies, 1), "I2 입문 — 친 뒤에도 공은 격자점으로");

  // D. 도전 — 찬스 없이 · 옮기지 않음
  await back();
  await level("pro");
  await open("pool", 1);
  s = await S();
  ok(s.level === "pro" && s.inv[0] === 0 && await fr.locator("#chanceBtn").isDisabled(), "D1 도전 — 찬스 0개");

  // Z. 찬스 구슬 → 문제 → 찬스 +1
  const before = (await S()).inv[0];
  ok(await fr.evaluate(() => window.__slopeShotDebug.spawnOrb()), "Z1 찬스 구슬이 뜬다");
  await fr.locator(".orb").waitFor({ state: "attached" });
  await fr.waitForTimeout(500);
  await shot("games-orb");
  await fr.locator(".orb").dispatchEvent("click");
  await fr.locator("#overlay").waitFor();
  const q = (await S()).quiz;
  ok(!!q && (await txt("#qText")) === q.text && /절편 찬스 문제/.test(await txt("#qTitle")), "Z2 구슬을 누르면 절편 찬스 문제");
  await fr.locator("#qAns").fill(String(q.ans).replace("-", "−"));
  await fr.locator("#qSubmit").click();
  ok(/정답!/.test(await txt("#qMsg")) && (await S()).inv[0] === before + 1, "Z3 맞히면 절편 찬스 +1");
  await fr.locator("#qClose").click();
  ok(await fr.locator("#overlay").isHidden(), "Z4 닫기");

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
