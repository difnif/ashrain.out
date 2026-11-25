// 굴뚝새(시록고 #/games) 스모크 — 게임과 시록고의 게임 자리를 실제 브라우저로 해 본다.
//   node tests/smoke/gulttuksae.smoke.mjs [--headed]     빌드 후(dist/ 필요): 강사 권한 · 더보기 → 게임 · iframe · 테마 · 저장 · 전체 화면 + 게임 검사
//   node tests/smoke/gulttuksae.smoke.mjs --game-only    빌드 없이 게임 HTML 한 장만 바로 열어 게임 검사
// 준비: playwright + Chromium(없으면 설치된 Chrome). 1 ~ 2분 걸린다. 시간은 게임의 시험 갈고리(__gtDebug.jump)로 앞당긴다.
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

// ── 게임 검사 — fr: 게임 문서가 든 프레임 ──
async function gameChecks(fr, shot) {
  const S = () => fr.evaluate(() => window.__gulttuksae());
  const dbg = (fn, ...a) => fr.evaluate(([fn, a]) => window.__gtDebug[fn](...a), [fn, a]);
  const until = async (pred, ms = 6000) => { const t0 = Date.now(); let s; while (Date.now() - t0 < ms) { s = await S(); if (pred(s)) return s; await fr.waitForTimeout(60); } return s; };
  const answer = async (good) => { await dbg("answer", good); await fr.waitForTimeout(40); await dbg("next"); };
  const firstLens = (s) => Object.keys(s.enc.lenses)[0];

  // G. 시작 화면
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  let s = await S();
  ok((await fr.locator('#levelSeg [data-level]').count()) === 3 && (await fr.locator('#levelSeg [aria-checked="true"]').getAttribute("data-level")) === "ace", "G1 난이도 3단계(뉴비 · 에이스 · 마스터), 에이스가 골라져 있다");
  ok(s.self.name === "wren" && /굴뚝새/.test(await fr.locator("#selfCard").innerText()), "G2 처음 자아는 가운데 — 굴뚝새");
  await fr.locator('[data-level="newbie"]').click();
  ok(/30초/.test(await fr.locator("#lvDesc").innerText()), "G3 뉴비 설명 — 하루 30초 · 친절한 근거");
  await fr.locator('[data-level="ace"]').click();

  // N. 새 겨울 — 도움말(시계 멈춤) → 벌판 입구의 첫 물음
  await fr.locator("#btnNew").click();
  await fr.locator("#helpOv").waitFor({ state: "visible", timeout: 5000 });
  ok((await S()).paused === true, "N1 첫 겨울엔 도움말이 열리고 시계가 멈춘다");
  await fr.locator("#hClose").click();
  s = await S();
  ok(s.mode === "enc" && s.enc.type === "start" && s.enc.pieces.length === 3
    && new Set(s.enc.pieces.map((p) => p.lens)).size === 3 && new Set(s.enc.pieces.map((p) => p.form)).size === 3, "N2 벌판 입구 — 서로 다른 렌즈 · 형식의 문제 조각 셋");
  const drawn = await fr.evaluate(() => { const c = document.getElementById("map"), g = c.getContext("2d"); const d = g.getImageData(c.width / 2 | 0, c.height / 2 | 0, 1, 1).data; return c.width > 100 && d[3] > 0; });
  ok(drawn, "N3 지도(스페이스)를 그린다");
  const d0 = s.day; await fr.waitForTimeout(900); s = await S();
  ok(s.day > d0, `N4 시계는 저절로 흐른다(${d0} → ${s.day}일)`);
  await fr.locator("#btnPause").click(); const dp = (await S()).day; await fr.waitForTimeout(500);
  s = await S();
  ok(s.paused && Math.abs(s.day - dp) < 0.001 && await fr.locator("#pauseCover").isVisible(), "N5 멈추면 시계가 서고 근거 · 문항이 가려진다");
  await fr.locator("#btnResumeClock").click();
  const iHow = s.enc.pieces.findIndex((p) => p.form === "how"), iBad = s.enc.pieces.findIndex((p) => p.form !== "how");
  await fr.locator(`[data-act="start"][data-i="${iHow}"]`).click();
  await fr.locator("#probOv").waitFor({ state: "visible" });
  // 입력 검사 — 빈칸 · 잘못된 값은 넘어가지 않는다
  const kind = (await S()).problem.type;
  await fr.locator("#pOk").click();
  ok((await fr.locator("#pErr").innerText()).length > 0 && (await S()).problem.done === false, "V1 빈 답은 넘어가지 않고 알려 준다");
  if (kind !== "choice") {
    await fr.locator("#pA").fill("abc"); await fr.locator("#pOk").click();
    ok(/숫자/.test(await fr.locator("#pErr").innerText()) && (await S()).problem.done === false, "V2 숫자가 아니면 알려 준다");
  } else ok(true, "V2 (고르기 문항이라 건너뜀)");
  ok(await fr.evaluate(() => [window.__gtDebug.parse("2/3"), window.__gtDebug.parse("−6"), window.__gtDebug.parse("7.5"), window.__gtDebug.parse("x")]).then((v) => Math.abs(v[0] - 2 / 3) < 1e-9 && v[1] === -6 && v[2] === 7.5 && Number.isNaN(v[3])), "V3 분수 2/3 · 음수 −6 · 소수 7.5 를 읽는다");
  const jeong0 = (await S()).res.jeong;
  await answer(true);
  s = await S();
  ok(s.enc.pieces[iHow].done === "ok" && s.self.A < 0 && s.res.jeong > jeong0 + 1.2, `N6 첫 물음(어떻게?)을 맞히면 씨앗 — 자아가 '어떻게' 쪽(A ${s.self.A}) · 정성 +1.5`);
  await fr.locator(`[data-act="start"][data-i="${iBad}"]`).click();
  await answer(false);
  s = await S();
  ok(s.weathers.length === 1, "N7 첫 오답은 첫 날씨가 된다");
  await shot("gt-start");
  await fr.locator('[data-act="decide"][data-opt="go"]').click();
  s = await until((x) => x.mode === "route");
  ok(s.mode === "route" && s.next.length >= 2 && s.next.length <= 3, `N8 길을 나서면 갈 곳을 고른다(${s.next.length}곳)`);

  // T. 이동 → 조우
  const pick = s.next.find((n) => n.type === "sea") || s.next[0];
  const pos = await dbg("nodeRel", pick.id);
  await fr.locator("#map").click({ position: pos });
  s = await S();
  ok(s.mode === "travel" && s.travel.days >= 1, "T1 지도에서 자리를 누르면 그쪽으로 떠난다");
  await dbg("jump", s.travel.days + 0.05);
  s = await until((x) => x.mode === "enc");
  ok(s.mode === "enc" && s.enc.type === pick.type && Object.values(s.enc.lenses).every((l) => l.E === 0), `T2 도착 — ${pick.type} 조우, 에이스는 근거가 날것부터`);
  await shot("gt-enc");
  const L0 = firstLens(s), opt0 = s.enc.opts.find((o) => o.lo < 1 && o.hi - o.lo > 0.1) || s.enc.opts[0];
  ok(opt0.lo <= opt0.p && opt0.p <= opt0.hi, "T3 결정의 성공률은 폭으로 보인다(참값은 그 안)");
  const w0 = opt0.hi - opt0.lo, p0 = opt0.p;
  await fr.locator(`[data-act="ask"][data-lens="${L0}"][data-form="how"]`).click();
  await answer(true);
  s = await S();
  const opt1 = s.enc.opts.find((o) => o.id === opt0.id);
  ok(s.enc.lenses[L0].I > 0 && s.roads >= 1, "T4 맞히면 읽어 낸 만큼 근거가 단단해지고 길이 난다");
  ok(opt1.hi - opt1.lo < w0 - 0.01 || p0 >= 0.96, `T5 근거가 단단해지면 폭이 좁아진다(${Math.round(w0 * 100)} → ${Math.round((opt1.hi - opt1.lo) * 100)}%p)`);
  const L1 = Object.keys(s.enc.lenses)[1];
  const j1 = s.res.jeong;
  await fr.locator(`[data-act="up"][data-lens="${L1}"]`).click();
  s = await S();
  ok(s.enc.lenses[L1].up && s.res.jeong < j1, "T6 다듬기 — 정성을 쓰고 시간이 걸린다");
  await dbg("jump", 0.6);
  s = await until((x) => x.enc && x.enc.lenses[L1].E === 1);
  ok(s.enc.lenses[L1].E === 1, "T7 시간이 지나면 근거가 '정리'로 친절해진다");
  const pBefore = s.enc.opts.find((o) => o.id === opt0.id).p;
  const L2 = Object.keys(s.enc.lenses)[2];
  await fr.locator(`[data-act="ask"][data-lens="${L2}"][data-form="what"]`).click();
  await answer(false);
  s = await S();
  ok(s.weathers.some((w) => w.type === pick.type && w.lens === L2), "T8 틀리면 그 조우 · 렌즈의 날씨(오개념 돌풍)가 생긴다");
  const u0 = s.res.unique;
  await fr.locator(`[data-act="ai"][data-lens="${L2}"]`).click();
  s = await S();
  ok(s.enc.lenses[L2].E === 3 && s.enc.lenses[L2].ai && s.res.unique < u0 - 5 && s.self.C < 0, "T9 독수리 — 가장 친절한 근거를 바로, 대신 고유함이 닳고 자아가 '기대기' 쪽으로");
  await shot("gt-enc2");
  ok(pBefore > 0, "T10 결정 막대가 계속 계산된다");

  // S. 자아 — 이름 · 질문 값의 종류
  ok((await dbg("setSelf", 0, 0, 0)) === "wren" && (await dbg("setSelf", 0.3, 0.3)) === "wren" && (await dbg("setSelf", 0.35, 0.35)) === "olppaemi" && (await dbg("setSelf", 0.3, 0.3)) === "olppaemi",
    "S1 자아 이름은 문턱을 두 겹으로 — 들어갈 땐 높게, 나올 땐 낮게");
  await dbg("setSelf", -1, -1, 0); s = await S();
  ok(s.self.name === "jebi" && s.enc.costs.how.cur === "food", "S2 제비 — 질문 값을 식량으로 치른다");
  await dbg("setSelf", 1, -1, 0); s = await S();
  ok(s.self.name === "kkachi" && s.enc.costs.how.cur === "morale", "S3 까치 — 질문 값을 사기로 치른다");
  await dbg("setSelf", 1, 1, 0); s = await S();
  ok(s.self.name === "olppaemi" && s.enc.costs.why.cur === "jeong" && s.enc.costs.why.amt < 2, `S4 올빼미 — 왜?가 싸다(정성 ${s.enc.costs.why.amt})`);
  await dbg("setSelf", -1, 1, 0); s = await S();
  ok(s.self.name === "durumi" && s.enc.costs.how.cur === "days", "S5 두루미 — 질문 값을 날짜로 치른다");
  const free = Object.entries(s.enc.lenses).find(([, l]) => !l.ai && !l.asked.why);
  if (free) {
    await fr.locator(`[data-act="ask"][data-lens="${free[0]}"][data-form="why"]`).click();
    s = await S();
    ok(s.prep === true && !s.problem, "S6 두루미가 물으면 먼저 시간이 흐른다(천천히 물음을 고른다)");
    await dbg("jump", 1.2);
    s = await until((x) => !!x.problem);
    ok(!!s.problem && s.problem.form === "why", "S7 날짜를 치르고 나면 문항이 열린다");
    await answer(true);
  } else { ok(true, "S6 (건너뜀)"); ok(true, "S7 (건너뜀)"); }
  await dbg("setSelf", 0, 0, 0);

  // P. 질문 트리 — 정답 셋마다 하나
  s = await S();
  if (s.polya.points < 1) {
    for (const p of [...Array(3)]) {
      const e = await S(); const lz = Object.entries(e.enc.lenses).find(([, l]) => !l.ai && ["what", "how", "why"].some((f) => !l.asked[f]));
      if (!lz) break;
      const f = ["what", "how", "why"].find((x) => !lz[1].asked[x]);
      await fr.locator(`[data-act="ask"][data-lens="${lz[0]}"][data-form="${f}"]`).click().catch(() => {});
      if ((await S()).problem) await answer(true);
      if ((await S()).polya.points >= 1) break;
    }
  }
  s = await S();
  if (s.polya.points >= 1) {
    await fr.locator('[data-act="polya"][data-id="part"]').click();
    s = await S();
    ok(s.polya.open.includes("part"), "P1 질문 트리 — 정답이 쌓이면 폴리아의 물음을 연다");
  } else ok(false, "P1 질문 트리 점수가 쌓이지 않았다");

  // D. 결정 → 다음 길
  const dec = await fr.locator('[data-act="decide"]:not([disabled])').first();
  await dec.click();
  s = await until((x) => x.mode === "route" || x.mode === "busy");
  ok(s.mode === "route" || s.mode === "busy", `D1 정하면 결과가 나고 다음 길로(${s.mode})`);
  if (s.mode === "busy") { await dbg("jump", s.busy.left + 0.1); s = await until((x) => x.mode === "route"); }

  // SG. 징조 — 눌러서 잡는다
  await dbg("spawnSign", "winter");
  const sp = await dbg("signRel");
  await fr.locator("#map").click({ position: sp });
  s = await S();
  ok(s.winter.warned === true && s.stats.signs >= 1, "SG1 ❄️ 징조를 잡으면 한겨울을 미리 안다(前知)");

  // W. 한겨울 — 이동 · 결정이 멈추고 되돌아보기만
  await fr.locator('[data-act="route"]').first().click();
  s = await S(); const travelDone = s.travel.done;
  await dbg("forceWinter"); await dbg("jump", 0.05);
  s = await until((x) => x.winter.on);
  ok(s.winter.on && await fr.locator("#banner").isVisible(), "W1 한겨울이 오면 배너 — 땅은 쇠처럼, 물은 돌처럼");
  await dbg("jump", 1);
  s = await S();
  ok(s.travel && Math.abs(s.travel.done - travelDone) < 0.2, "W2 한겨울엔 길 위에서도 멈춘다");
  ok(s.rates.fuel > s.params.fuelPerDay * 1.1, `W3 한겨울엔 연료가 더 든다(미리 알아 ×${s.params.winterFuelKnown})`);
  const reflect = fr.locator('[data-act="reflect"]').first();
  ok(await reflect.count() > 0 || await fr.locator('[data-act="wx"]').count() > 0, "W4 남는 동사는 질문 — 날씨 다시 묻기 · 되돌아보기");
  if (await reflect.count()) { const f0 = (await S()).res.fuel; await reflect.click(); await answer(true); s = await S(); ok(s.res.fuel > f0 + 0.5, "W5 되돌아보기를 맞히면 연료 · 사기로 버틴다"); }
  else ok(true, "W5 (되돌아보기 없음)");
  const wx = fr.locator('[data-act="wx"]').first();
  if (await wx.count()) { const n0 = (await S()).weathers.length; await wx.click(); await answer(true); s = await S(); ok(s.weathers.length === n0 - 1, "W6 날씨를 다시 물어 맞히면 걷힌다"); }
  else ok(true, "W6 (날씨 없음)");
  await shot("gt-winter");
  await dbg("jump", s.params.winterLen + 0.5);
  s = await until((x) => !x.winter.on);
  ok(!s.winter.on && s.winter.done, "W7 한겨울이 지나간다");

  // F. 독수리가 앞자리를 굳힌다
  await dbg("fossilNext"); await dbg("jump", 0.05);
  s = await S();
  ok(await fr.evaluate(() => Object.values(window.__gtDebug.state().map.nodes).some((n) => n.fossil)), "F1 독수리가 앞의 자리를 먼저 굳힌다(화석)");

  // R. 저장하고 나가기 → 이어 하기
  const dayR = (await S()).day;
  await fr.locator("#btnLeave").click(); await fr.locator("#leaveYes").click();
  await fr.locator("#lobby").waitFor();
  ok(await fr.locator("#btnResume").isVisible(), "R1 저장하고 나가면 '이어 하기'");
  await fr.locator("#btnResume").click();
  s = await S();
  ok(s.screen === "game" && s.paused && Math.abs(s.day - dayR) < 0.3, "R2 이어 하면 멈춘 채로 그 날에서 다시");
  await fr.locator("#btnResumeClock").click();

  // E. 겨울 끝내기 → 결산(자아 일지 · 스페이스)
  await fr.locator("#btnLeave").click(); await fr.locator("#leaveEnd").click();
  await fr.locator("#sumOv").waitFor({ state: "visible" });
  ok((await fr.locator(".journal li").count()) >= 4 && /y = /.test(await fr.locator("#spaceNote").innerText()), "E1 결산 — 자아 일지 · 내 스페이스 곡선");
  ok(JSON.parse(await fr.locator("#sumJson").inputValue()).stats.forms.how >= 1, "E2 다듬을 때 쓸 기록(JSON)");
  await shot("gt-summary");
  await fr.locator("#sumAgain").click();
  await fr.locator("#btnLeave").click(); await fr.locator("#leaveEnd").click();
  await fr.locator("#sumOv").waitFor({ state: "visible" });
  ok(/만나는 점/.test(await fr.locator("#spaceNote").innerText()), "E3 두 번째 겨울부터 지난 곡선과 만나는 점(2막의 문)을 센다");
  await fr.locator("#sumLobby").click();
  s = await S();
  ok(s.runs >= 2 && (await fr.locator("#runsList .run").count()) >= 2, "E4 지난 겨울들이 시작 화면에 쌓인다");

  // TU. 다듬기 패널
  await fr.locator("#btnTune").click();
  await fr.locator('#tuneBody [data-k="dayAce"]').fill("25");
  await fr.locator("#tApply").click();
  s = await S();
  ok(s.params.dayAce === 25 && (await fr.locator(".trow.chg").count()) >= 1, "TU1 다듬기 — 값을 바꿔 적용하면 저장되고 금빛으로 표시");
  await fr.locator("#tReset").click();
  s = await S();
  ok(s.params.dayAce === 20, "TU2 기본값으로 되돌린다");
  await fr.locator("#tClose").click();
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
      await gameChecks(page.mainFrame(), shot);
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

      await gameChecks(fr, shot);

      // M. 저장 — 앱이 이 기기에 맡아 두고, 새로고침하면 돌려준다
      const saved = await page.evaluate(() => { try { return JSON.parse(localStorage.getItem("ashrain.games.gulttuksae") || "null"); } catch { return null; } });
      ok(saved && saved.v === 1 && saved.runs.length >= 2 && saved.self, `M1 기록은 앱이 맡아 둔다(ashrain.games.gulttuksae · 지난 겨울 ${saved && saved.runs.length})`);
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
