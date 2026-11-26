// 굴뚝새(시록고 #/games) 스모크 — 게임과 시록고의 게임 자리를 실제 브라우저로 해 본다.
//   node tests/smoke/gulttuksae.smoke.mjs [--headed]     빌드 후(dist/ 필요): 강사 권한 · 더보기 → 게임 · iframe · 테마 · 저장 · 전체 화면 + 게임 검사
//   node tests/smoke/gulttuksae.smoke.mjs --game-only    빌드 없이 게임 HTML 한 장만 바로 열어 게임 검사
// 준비: playwright + Chromium(없으면 설치된 Chrome). 1 ~ 2분 걸린다. 시간은 게임의 시험 갈고리(__gtDebug.jump)로 앞당기고,
//   표지 · 책장 · 길 긋기 · 손잡이 · 둥지 끌기는 진짜 마우스로, 장치 속 손놀림은 갈고리(pull · drill · flick · lever)로 한다.
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
const GAME = path.join(ROOT, "src/features/games/gulttuksae.html");
const HEADED = process.argv.includes("--headed");
const GAME_ONLY = process.argv.includes("--game-only");
const SHOTS = process.env.SMOKE_SHOTS || path.join(HERE, "shots");

const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".ico": "image/x-icon", ".webmanifest": "application/manifest+json" };
function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = new URL(req.url, "http://x");
      let f = GAME;
      if (!GAME_ONLY) {
        f = path.join(DIST, decodeURIComponent(u.pathname));
        if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f = path.join(DIST, "index.html");
      }
      res.writeHead(200, { "content-type": (MIME[path.extname(f)] || "application/octet-stream") + (f.endsWith(".html") ? "; charset=utf-8" : "") });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(0, "127.0.0.1", () => resolve({ srv, port: srv.address().port }));
  });
}

// ── Supabase 모의 — 프로필 역할 · 소속(memberships) 역할을 바꿔 가며 ──
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const USER = { id: "00000000-0000-4000-8000-000000000002", aud: "authenticated", role: "authenticated", email: "teacher@example.com", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: { last_role: "instructor" }, factors: [], created_at: "2026-01-01T00:00:00Z" };
const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], app_metadata: USER.app_metadata, user_metadata: USER.user_metadata, session_id: "s2" })}.sig`;
const SESSION = { access_token: JWT, token_type: "bearer", expires_in: 3600, expires_at: 9999999999, refresh_token: "r2", user: USER };
let ROLE = "student", MEMBER = null;
const profile = () => ({ id: USER.id, role: ROLE, member_code: "SMOKE2", trial_expires_at: null, merged_into: null, phone_verified: true, is_minor: false, birth_date: "1985-03-01", settings: {} });
async function mockSupabase(page) {
  await page.route("https://placeholder.supabase.co/**", (route) => {
    const req = route.request(); const u = new URL(req.url()); const accept = req.headers()["accept"] || "";
    const json = (obj, headers = {}) => route.fulfill({ status: 200, contentType: "application/json", headers, body: JSON.stringify(obj) });
    if (u.pathname.startsWith("/auth/v1/user")) return json(USER);
    if (u.pathname.startsWith("/auth/v1/token")) return json(SESSION);
    if (u.pathname.startsWith("/auth/v1/")) return json({});
    if (u.pathname.startsWith("/storage/v1/")) return json([]);
    if (u.pathname.startsWith("/rest/v1/")) {
      const table = u.pathname.replace("/rest/v1/", "").split("/")[0];
      const wantObj = accept.includes("pgrst.object");
      if (req.method() === "HEAD") return route.fulfill({ status: 200, headers: { "content-range": "*/0", "access-control-expose-headers": "content-range" }, body: "" });
      if (table === "profiles") return json(wantObj ? profile() : [profile()]);
      if (table === "memberships") return json(MEMBER ? [{ role: MEMBER, academy_code: "SMK", rank: null, status: "active" }] : []);
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

// ── 게임 검사 — fr: 게임 문서가 든 프레임, page: 마우스를 쥔 쪽, off: 프레임의 자리 ──
async function gameChecks(fr, shot, page, off) {
  const S = () => fr.evaluate(() => window.__gulttuksae());
  const dbg = (fn, ...a) => fr.evaluate(([fn, a]) => window.__gtDebug[fn](...a), [fn, a]);
  const st = (expr, arg) => fr.evaluate(expr, arg);
  const until = async (pred, ms = 6000) => { const t0 = Date.now(); let s; while (Date.now() - t0 < ms) { s = await S(); if (pred(s)) return s; await fr.waitForTimeout(60); } return s; };
  const click = (p) => page.mouse.click(off.x + p.x, off.y + p.y);
  const drag = async (pts, wait = 16) => { await page.mouse.move(off.x + pts[0].x, off.y + pts[0].y); await page.mouse.down(); for (const q of pts.slice(1)) { await page.mouse.move(off.x + q.x, off.y + q.y); await fr.waitForTimeout(wait); } await page.mouse.up(); };
  const line = (a, b, n = 12) => Array.from({ length: n + 1 }, (_, i) => ({ x: a.x + (b.x - a.x) * i / n, y: a.y + (b.y - a.y) * i / n }));
  const vp = await fr.evaluate(() => ({ w: innerWidth, h: innerHeight }));
  const mid = { x: vp.w / 2, y: vp.h / 2 };

  // G. 표지 — 글자 없는 그림 한 장
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  await fr.waitForTimeout(300);
  let s = await S();
  const words = await fr.evaluate(() => document.body.innerText.replace(/\s+/g, ""));
  ok(s.v === 3 && s.scene === "cover" && words === "" && (await fr.locator("#levelSeg, [data-level], #btnNew, #helpOv").count()) === 0, "G1 표지 — 글자 · 난이도 · 설명 없이 책 한 권");
  ok(s.params.dayLen === 15 && s.self.name === "wren" && !s.cur, "G2 하루 15초 · 처음의 나는 가운데(굴뚝새)");
  ok((await dbg("lum", vp.w * 0.4, vp.h * 0.4, vp.w * 0.6, vp.h * 0.6)) > 8, "G3 캔버스에 표지 그림이 그려진다");

  // N. 책장을 넘기면 — 노래의 터전 → 빈 종이에서 세상이 생긴다
  await click(mid);
  s = await S();
  ok(s.turning === true, "N1 표지를 누르면 책장이 넘어간다");
  s = await until((x) => x.scene === "legend" && !x.turning, 4000);
  ok(s.scene === "legend" && (await fr.evaluate(() => document.body.innerText.replace(/\s+/g, ""))) === "", "N2 첫 장 — 글 없이 굴뚝새의 터전(지평선 · 덤불 · 눈)을 그린다");
  await fr.waitForTimeout(500); await shot("gt-legend");
  await click(mid); await fr.waitForTimeout(150); await click(mid);
  s = await until((x) => x.scene === "world" && !x.turning, 4000);
  ok(s.scene === "world" && s.forming < 0.7 && s.hud.length === 0, "N3 한 장 더 — 빈 종이에서 세상이 번져 나온다(손잡이도 아직 없다)");
  s = await until((x) => x.forming >= 1, 8000);
  ok(s.forming >= 1 && ["wood", "food", "hope", "people", "pause", "leave"].every((k) => s.hud.includes(k)), "N4 세 사람이 둥지를 지으면 살림(그림 + 숫자)과 손잡이가 떠오른다");
  const d0 = s.day; await fr.waitForTimeout(800); s = await S();
  ok(s.day > d0 && !s.walking && s.paths === 0, `N5 시계는 저절로 흐른다(${d0} → ${s.day}일)`);
  await click(await dbg("hudPx", "pause")); const dp = (await S()).day; await fr.waitForTimeout(400); s = await S();
  ok(s.paused && Math.abs(s.day - dp) < 1e-3, "N6 멈춤 — 시계가 선다");
  await click(await dbg("hudPx", "pause"));
  s = await S();
  ok(!s.paused, "N7 다시 누르면 흐른다");

  // V. 밤낮은 실제 시각(이 세상이 놓인 비밀의 자리), 날짜는 노는 동안만
  const geo = await st(() => window.__gtDebug.state().geo);
  ok(geo && geo.lat >= -56 && geo.lat <= 64 && geo.lon >= -180 && geo.lon < 180 && !(await fr.evaluate(() => /\d/.test(document.body.innerText))), `V0 세상이 생길 때 실제 위도 · 경도가 정해진다 — 화면엔 어디에도 없다`);
  const Wr = (await dbg("layout")).Wr, box = [Wr.x, Wr.y, Wr.x + Wr.w, Wr.y + Wr.h];
  await dbg("geo", 37.5, 127);   // 시험은 늘 같은 자리에서
  await dbg("solar", 0); await fr.waitForTimeout(250); const night = await dbg("lum", ...box); const todN = (await S()).tod;
  await dbg("solar", 12.3); await fr.waitForTimeout(250); const noon = await dbg("lum", ...box);
  ok(night < noon * 0.85 && todN === "night" && (await S()).tod === "day", `V1 그 자리가 밤이면 그림이 어둡고 한낮이면 밝다(밝기 ${Math.round(noon)} · ${Math.round(night)})`);
  const dV = (await S()).day; await dbg("jump", 0.6); await fr.waitForTimeout(250); const noon2 = await dbg("lum", ...box); s = await S();
  ok(Math.abs(noon2 - noon) < noon * 0.04 && s.tod === "day" && s.day >= dV + 0.6, `V2 날짜가 흘러도 해는 실제 시각대로 — 빛은 그대로(${Math.round(noon)} → ${Math.round(noon2)})`);
  await dbg("solar", 6.6); await fr.waitForTimeout(150); const dawn = (await S()).tod; await dbg("solar", 17.2); const dusk = (await S()).tod;
  ok(dawn === "dawn" && dusk === "dusk", `V3 해 뜰 무렵 · 질 무렵은 새벽빛 · 노을빛(${dawn} · ${dusk})`);
  await dbg("solar", 12.3);

  // P. 길 — 손가락으로 선을 긋는다
  const hp = await dbg("homePx"), fp = await dbg("sitePx", "forestA");
  await drag(line(hp, fp));
  s = await S();
  ok(s.paths === 1 && s.walking, "P1 집에서 선을 그으면 그 길을 걷는다(입력 칸 없이)");
  const rv0 = s.reveal;
  await dbg("arrive"); s = await S();
  ok(s.sites.forestA.linked && s.reveal > rv0, `P2 걸은 만큼 세상이 드러나고(${rv0} → ${s.reveal}) 숲에 닿으면 이어진다`);
  await dbg("jump", 3);
  ok(await st(() => { const g = window.__gtDebug.state().lastGain; return !!g && g.kind === "wood"; }), "P3 이어진 숲에서 장작이 길을 따라 흘러온다");
  await shot("gt-path");

  // D1. 숲 — 뽑기 통(숨은 규칙: 끝 빛깔)
  await click(fp); await fr.waitForTimeout(400);
  s = await S();
  ok(s.dev === "forestA", "D1 숲을 누르면 장치가 펼쳐진다(뽑기 통 둘)");
  const dd = s.day; await fr.waitForTimeout(500);
  ok(Math.abs((await S()).day - dd) < 1e-6, "D2 장치를 펼치면 바깥 시계는 서고, 손을 쓸 때만 시간이 든다");
  const w0 = (await S()).res.wood;
  await dbg("pull", 0, true); s = await S();
  ok(s.res.wood > w0 + 0.4 && s.day > dd, "D3 막대를 끝까지 뽑으면 장작 — 뽑는 데도 시간이 든다");
  ok(await st(() => { const D = window.__gtDebug.state(); const c = D.sites.forestA.data.cups[0]; return c.log.length >= 1; }), "D4 뽑은 것은 여백에 표로 쌓인다");
  const lowCup = (await dbg("cups")).findIndex((c) => c.ratio <= 0.62);
  await st(([ci]) => { const c = window.__gtDebug.state().sites.forestA.data.cups[ci]; c.sticks = c.sticks.map((k, i) => ({ good: i < 7, sh: k.sh })); c.streak = 0; }, [lowCup]);
  for (let i = 0; i < 5; i++) await dbg("pull", lowCup, true);
  s = await S();
  ok(s.stars.includes("forest"), "D5 숨은 규칙 — 덜 나오는 통에서 끝 빛깔만 보고 다섯 번 내리 뽑으면 별");
  await shot("gt-forest");
  await dbg("close");

  // D2. 바다 — 돌림판(숨은 규칙: 같은 세기는 같은 자리)
  ok(await dbg("drawTo", "shore") && await dbg("arrive") && (await S()).sites.shore.linked, "D6 바다까지 선을 긋는다");
  await dbg("dev", "shore"); await fr.waitForTimeout(300);
  const fog0 = (await dbg("wheel")).fog; await dbg("gull");
  ok((await dbg("wheel")).fog < fog0, "D7 갈매기를 쫓으면 돌림판의 안개가 걷힌다");
  const k6 = await dbg("landing", 6), r6 = await dbg("flick", 6), k11 = await dbg("landing", 11), r11 = await dbg("flick", 11);
  ok(k6 === r6 && k11 === r11, `D8 돌림판은 운처럼 보여도 같은 세기면 같은 자리(${r6} · ${r11})`);
  ok(await dbg("launch"), "D9 배를 띄운다");
  const f0 = (await S()).res.food; const kk = await dbg("flick", 6); s = await S();
  ok((kk === "calm" && s.res.food > f0) || (kk === "swell" && s.res.food > f0) || (kk === "storm" && s.res.food <= f0), `D10 띄운 배는 돌림판이 멈춘 자리대로(${kk})`);
  await dbg("close");

  // D3. 강 — 얼음 뚫기(숨은 규칙: 두 번 재면 언제 건널지 보인다)
  await dbg("drawTo", "village"); await dbg("arrive");
  s = await S();
  ok(s.blocked && s.sites.ford.placed, "D11 강가에서 길이 멈추고 그 자리에 여울이 생긴다");
  await dbg("dev", "ford"); await fr.waitForTimeout(300);
  await dbg("drill"); await dbg("wait", 2); const probes = await dbg("drill");
  const ice = await dbg("ice");
  ok(probes >= 2 && ice.th > 0 && ice.safe > (await S()).day - 3, `D12 두 번 뚫어 두께를 재면 여백에 점이 찍힌다(${ice.th.toFixed(1)} / ${ice.need})`);
  if (ice.th < ice.need) {
    const food0 = (await S()).res.food; await dbg("cross"); s = await S();
    ok(!s.riverCrossed && s.res.food < food0, "D13 얼음이 얇을 때 건너면 깨진다(식량 · 희망을 잃는다)");
    await dbg("jump", ice.safe - (await S()).day + 0.1);
  } else ok(true, "D13 (이미 두꺼워 건너뜀)");
  ok(await dbg("cross"), "D14 두꺼워지면 건넌다");
  s = await S();
  ok(s.stars.includes("river"), "D15 숨은 규칙 — 재 보고 알맞은 날에 건너면 별");
  s = await until((x) => x.walking && !x.dev, 3000);
  ok(s.walking && !s.blocked, "D16 건너고 나면 멈췄던 길이 이어진다");
  await dbg("arrive"); s = await S();
  ok(s.sites.village.linked, "D17 마을에 닿는다");

  // D4. 장터 — 머신(숨은 규칙: 당긴 횟수와 하루의 때)
  await dbg("dev", "village"); await fr.waitForTimeout(300);
  await dbg("setRes", "wood", 30); await dbg("setRes", "food", 30);
  let sl = await dbg("slot");
  await dbg("lever");
  ok((await dbg("slot")).n === sl.n, "D18 값을 넣지 않으면 손잡이가 덜컥 — 돌지 않는다");
  await dbg("pay", "log"); const row = await dbg("lever");
  ok(row && row.r.length === 3 && (await dbg("slot")).n === sl.n + 1, "D19 장작 하나를 넣고 손잡이를 당기면 세 칸이 돈다 — 장부(여백)에 남는다");
  const other = sl.jk === "log" ? "grain" : "log";
  for (const k of ["log", "grain", "log", "grain"]) { if ((await dbg("slot")).n % 3 === 2) break; await dbg("pay", k); await dbg("lever"); }
  const led = await st(() => window.__gtDebug.state().sites.village.data.ledger);
  const third = {}; let same = true; led.forEach((r) => { if (!r.pay) return; if (third[r.pay] && third[r.pay] !== r.r[2]) same = false; third[r.pay] = r.r[2]; });
  ok(same && led.every((r) => r.pay), "D20 셋째 칸은 넣은 것을 따른다 — 장부엔 넣은 것 | 그림 셋");
  for (let i = 0; i < 3 && (await dbg("slot")).n % 3 !== 2; i++) { await dbg("pay", other); await dbg("lever"); }
  sl = await dbg("slot");
  ok(sl.next[0] === sl.next[1] && sl.next[1] === sl.next[2] && !(sl.nextOther[1] === sl.nextOther[2]), `D20b 둘이 맞는 차례에 맞는 것을 넣으면 세 칸이 같다(${sl.next.join(",")}) — 다른 것이면 아니다`);
  await dbg("pay", sl.jk); await dbg("lever");
  s = await S();
  ok((await dbg("slot")).jack >= 1 && s.stars.includes("village"), "D21 숨은 규칙 — 세 칸이 맞으면 큰 몫 · 별");
  // 독수리 깃털 — 답을 바로 보여 주는 대신 덤불 하나가 돌이 된다
  const c0 = (await S()).self.C, stones0 = (await S()).stones;
  await dbg("eagle"); s = await S();
  ok(s.stones === stones0 + 1 && s.self.C < c0 && await st(() => !!window.__gtDebug.state().sites.village.data.eagle), "D22 독수리 깃털 — 다음 판과 넣을 것을 바로 보여 주고, 덤불이 돌로 굳고, 나는 '기대기' 쪽으로");
  await shot("gt-village");
  await dbg("close");

  // M. 산 — 곧장 오르기보다 비스듬히 갈지자로 오르면 빠르다(기울기)
  const top = await dbg("site", "summit"), y0 = 0.5, zig = [[0.36, 0.6], [top.u, y0]];
  for (let i = 1; i <= 4; i++) zig.push([top.u + (i % 2 ? 0.026 : -0.026), y0 + (top.v - y0) * i / 4]);
  zig.push([top.u, top.v]);
  await dbg("drawPts", zig); await dbg("arrive");
  s = await S();
  const mtry = await st(() => window.__gtDebug.state().mountTry);
  ok(s.sites.summit.linked && s.stars.includes("mount"), `MT1 숨은 규칙 — 갈지자로 산마루에 오르면 곧장 오를 때보다 빨라 별(${mtry && mtry.mt} / ${mtry && mtry.ms}일)`);

  // H. 둥지 · 떠돌이 · 징조 — 한겨울은 며칠 뒤로, 지나가던 새 떼 · 떠돌이는 치우고 시작
  await st(() => { const D = window.__gtDebug.state(); Object.assign(D.mw, { on: false, done: false, known: false, start: D.day + 4 }); D.signs = []; D.wand = []; D.nextSign = D.day + 5; });
  await dbg("setRes", "wood", 12);
  const spot = await dbg("leeSpot");
  await click(hp); s = await S();
  ok(s.nestTok, "H1 집을 누르면 둥지 하나가 손에 들린다");
  const tok = await dbg("px", (await st(() => window.__gtDebug.state().nestTok.u)), (await st(() => window.__gtDebug.state().nestTok.v)));
  const sp1 = await dbg("px", spot.u, spot.v);
  await drag(line(tok, sp1, 8));
  s = await S();
  ok(s.nests === 2 && s.lee === 1, `H2 끌어다 놓으면 둥지 — 덤불 바람 그늘이면 연기가 곧게(장작이 덜 든다) [둥지 ${s.nests} · 그늘 ${s.lee}]`);
  const spot2 = await dbg("leeSpot"); if (spot2) await dbg("nest", spot2.u, spot2.v);
  s = await S();
  ok(s.lee >= 2 && s.stars.includes("nest"), "H3 숨은 규칙 — 바람 그늘 둥지 둘이면 별");
  const wp = await dbg("wanderer"); await click({ x: wp.x, y: wp.y - 4 }); s = await S();
  ok(s.wand.includes("join"), "H4 기다리는 떠돌이를 누르면 맞아들인다(등불)");
  const sgp = await dbg("spawnSign", "crow"); await click(sgp); s = await S();
  ok(s.mw.known && s.stats.signs >= 1, "H5 남쪽으로 가는 까마귀 떼를 잡으면 한겨울을 미리 안다(책갈피 끈에 푸른 띠)");
  await shot("gt-busy");

  // S. 자아 — 문턱 두 겹
  ok((await dbg("setSelf", 0, 0, 0)) === "wren" && (await dbg("setSelf", 0.2, 0.2, 0)) === "wren" && (await dbg("setSelf", 0.3, 0.3, 0)) === "owl" && (await dbg("setSelf", 0.2, 0.2, 0)) === "owl" && (await dbg("setSelf", 0.1, 0.1, 0)) === "wren",
    "S1 자아 이름은 문턱을 두 겹으로 — 들어갈 땐 높게, 나올 땐 낮게");
  ok((await dbg("setSelf", -0.4, -0.4, 0)) === "swallow" && (await dbg("setSelf", 0.4, -0.4, 0)) === "magpie" && (await dbg("setSelf", -0.4, 0.4, 0)) === "crane", "S2 제비 · 까치 · 두루미 — 네 갈래");
  await dbg("setSelf", 0, 0, 0);

  // R. 덮어 두기 → 이어 하기(책갈피 끈)
  const dayR = (await S()).day;
  await click(await dbg("hudPx", "leave")); await fr.waitForTimeout(120);
  ok((await S()).scene === "world", "R1 덮기는 한 번 누르면 붉은 고리 — 두 번 눌러야 덮인다");
  await click(await dbg("hudPx", "leave"));
  s = await until((x) => x.scene === "cover" && !x.turning, 4000);
  ok(s.scene === "cover" && s.cur, "R2 덮으면 표지에 책갈피 끈이 걸린다");
  const dC = s.day; await fr.waitForTimeout(1500);
  ok((await S()).day === dC, "R2b 덮어 둔 동안엔 날짜가 흐르지 않는다(노는 동안만)");
  await click(await dbg("ribbonPx"));
  s = await until((x) => x.scene === "world" && !x.turning, 4000);
  ok(s.scene === "world" && Math.abs(s.day - dayR) < 0.3 && s.lee >= 2 && s.stars.length >= 4, "R3 끈을 당기면 그 날 그 자리에서 다시");

  // W. 한겨울
  await dbg("forceMw"); await dbg("jump", 0.1);
  s = await until((x) => x.mw.on, 2000);
  ok(s.mw.on, "W1 한겨울 — 서리가 끼고, 둥지를 지을 수 없고, 장작이 더 든다");
  await shot("gt-midwinter");

  // E. 봄 → 끝 장 → 표지
  await dbg("setRes", "food", 40); await dbg("setRes", "wood", 40); await dbg("setRes", "hope", 9);
  await dbg("jump", 30);
  s = await S();
  ok(s.over && s.over.kind === "spring", "E1 버티면 봄이 온다(꽃 · 제비)");
  s = await until((x) => x.scene === "keep" && !x.turning, 7000);
  ok(s.scene === "keep" && s.runs === 1 && s.keepMeets === 0, "E2 끝 장 — 이 겨울의 그림 한 장 · 별 · 사람 · 돌, 내 곡선");
  await shot("gt-keep");
  await click(mid);
  s = await until((x) => x.scene === "cover" && !x.turning, 4000);
  ok(s.scene === "cover" && !s.cur, "E3 끝 장을 누르면 표지로");
  // 두 번째 겨울 — 지난 곡선과 만나는 점(2막의 문)
  await dbg("open"); await dbg("skip");
  await dbg("setSelf", 0.6, -0.6, 0.3);
  await dbg("end", "scatter");
  s = await until((x) => x.scene === "keep" && !x.turning, 7000);
  ok(s.runs === 2 && typeof s.keepMeets === "number", `E4 두 번째 겨울부터 지난 곡선과 만나는 점을 센다(${s.keepMeets})`);
  await click(mid);
  s = await until((x) => x.scene === "cover" && !x.turning, 4000);

  // TU. 다듬기(강사용)
  await fr.locator("#btnTune").click();
  ok(/숨은 규칙|규칙/.test(await fr.locator("#tuneMemo").innerText()) && !/"geo"|"lat"|"lon"/.test(await fr.locator("#tuneJson").inputValue()), "TU1 다듬기 — 강사에게만 숨은 규칙 메모(세상의 자리는 기록에도 보이지 않는다)");
  await fr.locator('#tuneBody [data-k="dayLen"]').fill("20");
  await fr.locator("#tApply").click();
  s = await S();
  ok(s.params.dayLen === 20 && (await fr.locator(".trow.chg").count()) >= 1, "TU2 하루 길이를 바꿔 적용하면 저장되고 금빛으로 표시");
  await fr.locator("#tReset").click();
  s = await S();
  ok(s.params.dayLen === 15, "TU3 기본값으로 되돌린다");
  await fr.locator("#tClose").click();
  await dbg("setSelf", 0, 0, 0);
  await dbg("solar", null);   // 시험 시계를 풀어 실제 시각으로
}

(async () => {
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}/`;
  let browser;
  try { browser = await chromium.launch({ headless: !HEADED }); }
  catch { browser = await chromium.launch({ headless: !HEADED, channel: "chrome" }); }
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
      await gameChecks(page.mainFrame(), shot, page, { x: 0, y: 0 });
    } else {
      await mockSupabase(page);

      // A. 강사 권한이 없으면 — 시록고가 열리지 않고 게임 파일도 받지 않는다
      ROLE = "student"; MEMBER = null;
      await page.goto(base + "seirocco#/games");
      await page.getByText("강사 권한이 아직 없어요").waitFor({ timeout: 20000 });
      ok((await page.locator("iframe").count()) === 0 && !urls.some((u) => /gulttuksae/.test(u)), "A1 강사 권한이 없으면 안내만 — iframe · 게임 파일 없음");

      // B. 강사 — 더보기 → 게임 → 샌드박스 iframe
      MEMBER = "instructor";
      await page.goto(base + "seirocco#/more");
      await page.reload();
      const row = page.locator(".d-row", { hasText: "게임" });
      await row.waitFor({ timeout: 20000 });
      ok(/굴뚝새/.test(await row.innerText()), "B1 시록고 더보기에 「게임 — 굴뚝새」");
      ok(!urls.some((u) => /gulttuksae/.test(u)), "B2 게임 화면을 열기 전엔 게임 파일을 받지 않는다");
      await row.click();
      await page.waitForFunction(() => location.hash === "#/games", null, { timeout: 5000 });
      const el = page.locator("iframe.sg-frame");
      await el.waitFor({ timeout: 20000 });
      ok((await el.getAttribute("sandbox")) === "allow-scripts" && /fullscreen/.test(await el.getAttribute("allow") || ""), "B3 iframe — sandbox=allow-scripts(앱 저장소 · 세션 접근 불가) · 전체 화면 허용");
      ok(urls.some((u) => /gulttuksae/.test(u)), "B4 그때 게임 파일을 받는다(따로 나뉜 파일)");
      ok(await page.locator(".d-tab.on", { hasText: "더보기" }).count() === 1, "B5 탭은 「더보기」에 불이 들어온다");
      const box = await el.boundingBox();
      ok(box && box.height >= 560 && box.width > 900, `B6 넓은 화면 — iframe ${box && Math.round(box.width)} × ${box && Math.round(box.height)}`);
      const fr = await (await el.elementHandle()).contentFrame();
      await fr.locator("#lobby").waitFor({ timeout: 20000 });
      ok((await fr.evaluate(() => document.documentElement.dataset.theme)) === "light", "B7 앱 테마(라이트)를 문서에 심어 연다");
      ok(await fr.evaluate(() => { try { localStorage.getItem("x"); return false; } catch { return true; } }), "B8 게임 안에서는 앱 저장소에 닿지 않는다");

      const fb = await el.boundingBox();
      await gameChecks(fr, shot, page, { x: fb.x, y: fb.y });

      // M. 저장 — 앱이 이 기기에 맡아 두고, 새로고침하면 돌려준다
      const saved = await page.evaluate(() => { try { return JSON.parse(localStorage.getItem("ashrain.games.gulttuksae") || "null"); } catch { return null; } });
      ok(saved && saved.v === 3 && saved.runs.length >= 2 && saved.self, `M1 기록은 앱이 맡아 둔다(ashrain.games.gulttuksae · 지난 겨울 ${saved && saved.runs.length})`);
      await page.reload();
      const el2 = page.locator("iframe.sg-frame");
      await el2.waitFor({ timeout: 20000 });
      const fr2 = await (await el2.elementHandle()).contentFrame();
      await fr2.locator("#lobby").waitFor({ timeout: 20000 });
      await fr2.waitForFunction(() => window.__gulttuksae().runs >= 2, null, { timeout: 5000 }).catch(() => {});
      ok((await fr2.evaluate(() => window.__gulttuksae().runs)) >= 2, "M2 새로고침해도 지난 겨울 · 자아가 돌아온다(앱이 돌려줌)");

      // T. 테마 — 판을 새로 열지 않고 바꾼다
      await page.evaluate(() => window.dispatchEvent(new StorageEvent("storage", { key: "ashrain-theme", newValue: "dark" })));
      await fr2.waitForFunction(() => document.documentElement.dataset.theme === "dark", null, { timeout: 5000 }).catch(() => {});
      ok((await fr2.evaluate(() => document.documentElement.dataset.theme)) === "dark", "T1 앱 테마를 바꾸면 게임도 다크로");

      // I. 전체 화면이 막힌 기기 — 게임이 부탁하면 iframe 을 화면 가득
      await fr2.evaluate(() => window.parent.postMessage({ type: "ash-immersive", on: true }, "*"));
      await page.waitForSelector(".sg-imm", { timeout: 3000 }).catch(() => {});
      const fbox = await el2.boundingBox();
      ok(fbox && Math.round(fbox.width) === 1180 && Math.round(fbox.height) === 820, "I1 몰입 모드 — iframe 이 화면을 가득 채운다");
      await fr2.evaluate(() => window.parent.postMessage({ type: "ash-immersive", on: false }, "*"));
      await page.waitForFunction(() => !document.querySelector(".sg-imm"), null, { timeout: 3000 }).catch(() => {});
      ok(await page.locator(".sg-imm").count() === 0, "I2 다시 누르면 원래대로");
      await shot("gt-app");
    }
    ok(errors.length === 0, "X1 콘솔 오류 없음" + (errors.length ? " — " + errors.slice(0, 3).join(" | ") : ""));
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e.message);
    await shot("gt-fail");
  } finally {
    await browser.close(); srv.close();
  }
  console.log(`\n${pass} passed · ${fail} failed`);
  process.exit(fail ? 1 : 0);
})();
