// 무제(예전 굴뚝새 · 시록고 #/games) 스모크 — 게임과 시록고의 게임 자리를 실제 브라우저로 해 본다.
//   node tests/smoke/gulttuksae.smoke.mjs [--headed]     빌드 후(dist/ 필요): 강사 권한 · 더보기 → 게임 · iframe · 테마 · 저장 · 전체 화면 + 게임 검사
//   node tests/smoke/gulttuksae.smoke.mjs --game-only    빌드 없이 게임 HTML 한 장만 바로 열어 게임 검사
// 준비: playwright + Chromium(없으면 설치된 Chrome). 1 ~ 2분 걸린다. 시간은 게임의 시험 갈고리(__gtDebug.jump)로 앞당기고,
//   표지 · 이름 · 볼거리 누르기 · 쪽지에 적기 · 걷기 · 장면 들어가기 · 끌기 · 휠 · 두 손가락(CDP 터치) · 바람막이 끌기는 진짜 손으로,
//   장면 속 몇몇 손놀림(뽑기 · 뚫기 · 낚기 · 재기 · 던지기 · 오르기)은 갈고리로 한다.
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
  const click = async (p, wait = 120) => { await page.mouse.click(off.x + p.x, off.y + p.y); await fr.waitForTimeout(wait); };
  const drag = async (pts, wait = 16) => { await page.mouse.move(off.x + pts[0].x, off.y + pts[0].y); await page.mouse.down(); for (const q of pts.slice(1)) { await page.mouse.move(off.x + q.x, off.y + q.y); await fr.waitForTimeout(wait); } await page.mouse.up(); await fr.waitForTimeout(80); };
  const line = (a, b, n = 12) => Array.from({ length: n + 1 }, (_, i) => ({ x: a.x + (b.x - a.x) * i / n, y: a.y + (b.y - a.y) * i / n }));
  const words = () => fr.evaluate(() => document.body.innerText.replace(/\s+/g, ""));
  const vp = await fr.evaluate(() => ({ w: innerWidth, h: innerHeight }));
  const mid = { x: vp.w / 2, y: vp.h / 2 };
  // 떠 있는 쪽지에 적기 — 연필을 누르고, 적고, Enter(진짜 손으로)
  const write = async (text) => { const pen = await dbg("lookPen"); if (!pen) return null; await click(pen); await fr.locator("#nbIn").fill(text); await fr.locator("#nbIn").press("Enter"); await fr.waitForTimeout(80); return true; };
  const shut = async () => { const s0 = await S(); if (s0.look) { await click({ x: 6, y: vp.h - 6 }); } };   // 쪽지 밖을 누르면 접힌다

  // G. 표지 — 천 공책, 쪽지에 '무제'
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  await fr.waitForTimeout(300);
  let s = await S();
  ok(s.v === 5 && s.scene === "cover" && (await words()) === "" && s.cover === "무제", "G1 표지 — 글자 없는 천 공책 한 권, 쪽지엔 '무제'(이름은 캔버스에만)");
  ok(s.params.dayLen === 15 && s.self.name === "wren" && !s.cur, "G2 하루 15초 · 처음의 나는 가운데(굴뚝새)");
  ok((await dbg("lum", vp.w * 0.4, vp.h * 0.4, vp.w * 0.6, vp.h * 0.6)) > 8, "G3 캔버스에 표지 그림이 그려진다");

  // N. 이름 — 닉네임처럼 적는 한 줄(사실은 이 땅의 이름)
  await click(mid, 0);
  s = await S();
  ok(s.turning === true, "N1 표지를 누르면 책장이 넘어간다");
  s = await until((x) => x.scene === "name" && !x.turning, 4000);
  ok(s.scene === "name" && s.nameBox && (await words()) === "" && (await fr.locator("#nameIn").getAttribute("placeholder")) === "무제", "N2 첫 장 — '이름' 한 줄(그림)과 적는 칸 하나, 비우면 '무제'");
  await fr.waitForTimeout(400); await shot("gt-name");
  await click(mid, 100);
  ok((await S()).scene === "name", "N3 종이를 눌러도 넘어가지 않는다 — 이름을 적어야(✓ · Enter)");
  await fr.locator("#nameIn").fill("하늘이"); await fr.locator("#nameIn").press("Enter");
  s = await until((x) => x.scene === "world" && !x.turning, 4000);
  ok(s.scene === "world" && s.name === "하늘이" && s.forming < 0.7 && s.hud.length === 0 && !s.nameBox, "N4 적고 넘기면 빈 종이에서 내 움막과 내가 생긴다");
  s = await until((x) => x.forming >= 1, 8000);
  ok(["leave", "sound"].every((k) => s.hud.includes(k)) && !["note", "wood", "food", "pause", "speed", "ribbon"].some((k) => s.hud.includes(k)), `N5 처음엔 아무것도 알려 주지 않는다 — 덮기 · 소리뿐, 공책 단추 · 멈춤 · 빠르기는 없다 [${s.hud.join(",")}]`);
  const d0 = s.day; await fr.waitForTimeout(800); s = await S();
  ok(s.day > d0 && !s.walking && s.paths === 0 && s.res.wood > 6, `N6 시계는 노는 동안 저절로 흐른다(${d0} → ${s.day}일)`);
  ok(s.lee === false && s.fences === 0 && s.signs === 0 && s.notes.memos === 0, "N7 처음 움막은 바람을 맞는다 · 나 혼자 · 공책은 비어 있다");

  // C. 보는 눈 — 처음엔 터전 가까이, 휠 · 두 손가락으로 당겨 보고, 빈 곳을 끌면 옮긴다
  ok(s.cam.z >= 1.5, `C1 처음엔 터전을 가까이(×${s.cam.z})`);
  await page.mouse.move(off.x + mid.x, off.y + mid.y); await page.mouse.wheel(0, -500); await fr.waitForTimeout(150);
  const zIn = (await S()).cam.z;
  await page.mouse.wheel(0, 3000); await fr.waitForTimeout(150);
  const zOut = (await S()).cam;
  ok(zIn > s.cam.z + 0.3 && zOut.z === 1 && zOut.ox === 0 && zOut.oy === 0, `C2 휠로 당겨 보고(×${zIn}) 물리면 땅 전체(×${zOut.z})`);
  await dbg("cam", 2.2); const c0 = (await S()).cam;
  await drag(line({ x: vp.w * 0.82, y: vp.h * 0.8 }, { x: vp.w * 0.62, y: vp.h * 0.62 }, 8));
  s = await S();
  ok((s.cam.ox !== c0.ox || s.cam.oy !== c0.oy) && s.paths === 0 && !s.walking, `C3 빈 곳을 끌면 지도가 옮겨진다(길은 생기지 않는다)`);
  const cdp = await page.context().newCDPSession(page);
  await dbg("cam", 1.6); const z0 = (await S()).cam.z, px = off.x + mid.x, py = off.y + mid.y;
  await cdp.send("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x: px - 40, y: py, id: 1 }, { x: px + 40, y: py, id: 2 }] });
  for (let i = 1; i <= 8; i++) { await cdp.send("Input.dispatchTouchEvent", { type: "touchMove", touchPoints: [{ x: px - 40 - i * 7, y: py - i * 2, id: 1 }, { x: px + 40 + i * 7, y: py - i * 2, id: 2 }] }); await fr.waitForTimeout(16); }
  await cdp.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] }); await fr.waitForTimeout(150);
  s = await S();
  ok(s.cam.z > z0 * 1.4 && s.paths === 0 && !s.walking, `C4 두 손가락으로 벌리면 당겨 보인다(×${z0} → ×${s.cam.z}) — 걷지 않는다`);
  await cdp.detach().catch(() => {});

  // V. 밤낮은 실제 시각(이 세상이 놓인 비밀의 자리), 날짜는 노는 동안만
  const geo = await st(() => window.__gtDebug.state().geo);
  ok(geo && geo.lat >= -56 && geo.lat <= 64 && geo.lon >= -180 && geo.lon < 180 && !(await fr.evaluate(() => /\d/.test(document.body.innerText))), `V0 세상이 생길 때 실제 위도 · 경도가 정해진다 — 화면엔 어디에도 없다`);
  await dbg("cam", 1.6, s.me.u, s.me.v);
  const VR = (await dbg("layout")).VR, box = [VR.x, VR.y, VR.x + VR.w, VR.y + VR.h];
  await dbg("geo", 37.5, 127);   // 시험은 늘 같은 자리에서
  await dbg("solar", 0); await fr.waitForTimeout(250); const night = await dbg("lum", ...box); const todN = (await S()).tod;
  await dbg("solar", 12.3); await fr.waitForTimeout(250); const noon = await dbg("lum", ...box);
  ok(night < noon * 0.85 && todN === "night" && (await S()).tod === "day", `V1 그 자리가 밤이면 그림이 어둡고 한낮이면 밝다(밝기 ${Math.round(noon)} · ${Math.round(night)})`);
  const dV = (await S()).day; await dbg("jump", 0.6); await fr.waitForTimeout(250); const noon2 = await dbg("lum", ...box); s = await S();
  ok(Math.abs(noon2 - noon) < noon * 0.05 && s.tod === "day" && s.day >= dV + 0.6, `V2 날짜가 흘러도 해는 실제 시각대로 — 빛은 그대로(${Math.round(noon)} → ${Math.round(noon2)})`);
  await dbg("solar", 6.6); await fr.waitForTimeout(150); const dawn = (await S()).tod; await dbg("solar", 17.2); const dusk = (await S()).tod;
  ok(dawn === "dawn" && dusk === "dusk", `V3 해 뜰 무렵 · 질 무렵은 새벽빛 · 노을빛(${dawn} · ${dusk})`);
  await dbg("solar", 12.3); await fr.waitForTimeout(150);

  // O. 볼거리 — 적을 수 있는 것을 누르면 쪽지가 뜬다(덤불처럼 볼거리가 아닌 것은 안 뜬다)
  const bp = await dbg("bushPx"); await click(bp);
  s = await S();
  ok(!s.look && s.fx.includes("wren") && !s.walking, "O1 덤불을 누르면 굴뚝새만 튀어나온다 — 쪽지는 뜨지 않는다(볼거리가 아님)");
  let H = await dbg("spots"); await click(H.smoke);
  s = await S();
  ok(s.look && s.look.subj === "wind" && !s.look.writing && s.looked === 1, "O2 움막의 연기를 누르면 그것을 그린 쪽지가 뜬다(연필과 함께)");
  await click(await dbg("lookPen")); const dw = (await S()).day; await fr.waitForTimeout(400); s = await S();
  ok(s.look.writing && Math.abs(s.day - dw) < 1e-6 && (await fr.locator("#nbIn").isVisible()), "O3 연필을 누르면 적는 칸 — 적는 동안 시계가 선다");
  await fr.locator("#nbIn").fill("연기가 왜 옆으로 누울까?"); await fr.locator("#nbIn").press("Enter"); await fr.waitForTimeout(80);
  s = await S();
  ok(!s.look && s.notes.noted.includes("wind") && s.notes.asked.includes("wind") && s.fx.includes("tonote") && (await dbg("ragPx")), `O4 적으면 쪽지가 내게 날아가고(공책), 그것을 눈여겨본다 — 물음이면 풀어 보기까지 · 움막 곁에 헝겊 [${s.notes.noted}]`);
  await shot("gt-noted");
  H = await dbg("spots"); await click(H.pile); s = await S();
  ok(s.look && s.look.subj === "fire", "O5 장작더미를 누르면 쪽지");
  await write("장작");
  s = await until((x) => x.fx.includes("hudnote"), 1500);
  ok(s.hud.includes("wood") && !s.hud.includes("food") && s.fx.includes("hudnote"), "O6 장작을 적으면 땔감 숫자가 연필 동그라미와 함께(양식은 아직)");
  await click(await dbg("skyPx")); s = await S();
  ok(s.look && s.look.subj === "time", "O7 해(달)를 누르면 쪽지");
  await write("봄까지 며칠 남았지?");
  s = await S();
  ok(s.hud.includes("ribbon") && s.notes.asked.includes("time") && !["pause", "speed"].some((k) => s.hud.includes(k)), "O8 해를 적으면 책갈피 끈(걸릴 날) — 멈춤 · 빠르기 단추는 없다");

  // K. 공책 — 나를 누르면 펼쳐진다
  await click(await dbg("mePx"));
  const dk = (await S()).day; await fr.waitForTimeout(400); s = await S();
  ok(s.nb && Math.abs(s.day - dk) < 1e-6, "K1 나를 누르면 내 공책이 펼쳐지고 시계가 선다");
  const tWind = await dbg("tabPx", "wind"), tSea = await dbg("tabPx", "sea");
  await click(tWind); const tab1 = (await S()).notes.tab; await click(tSea); s = await S();
  ok(tab1 === "wind" && s.notes.tab === "wind", "K2 아홉 칸 — 적은 것은 먹으로(눌러 그 쪽으로), 아직인 것은 흐린 빈칸(눌러도 열리지 않는다)");
  await click(await dbg("nbPenPx")); s = await S();
  ok(s.look && s.look.subj === "wind" && s.look.writing, "K3 공책의 연필로도 그 쪽에 적는다");
  await fr.locator("#nbIn").fill("바람은 늘 같은 쪽에서 불까?"); await fr.locator("#nbIn").press("Enter"); await fr.waitForTimeout(80);
  s = await S();
  ok(s.nb && !s.look && s.notes.memos === 4, "K4 적으면 공책에 한 줄 더");
  await shot("gt-notebook");
  await click(await dbg("nbClosePx")); ok(!(await S()).nb, "K5 덮는다");

  // P. 걷기 — 누르면 그리로(빠르게), 걸은 만큼 땅이 그려지고, 지나간 자취는 곧 사라진다
  const fa = await dbg("site", "forestA");
  await dbg("cam", 1.3, (fa.u + 0.36) / 2, (fa.v + 0.6) / 2); await fr.waitForTimeout(120);
  ok(!fa.found, "P0 숲은 아직 보이지 않는다(걸어가야 그려진다)");
  const rv0 = (await S()).reveal, t0 = Date.now();
  await click(await dbg("px", fa.u, fa.v + 0.03), 0);
  s = await S();
  ok(s.walking && s.paths === 1, "P1 땅을 누르면 그리로 걷는다");
  s = await until((x) => !x.walking, 9000); const took = Date.now() - t0;
  ok(!s.walking && took < 6500 && s.sites.forestA.found && s.reveal > rv0 && s.sites.forestA.open, `P2 몇 초면 닿는다(${(took / 1000).toFixed(1)}초) — 걸은 만큼 땅이 드러나고 숲 어귀에 서면 들어갈 수 있다(공책과 상관없이)`);
  await shot("gt-walk");
  s = await until((x) => x.paths === 0, 7000);
  ok(s.paths === 0 && s.reveal > rv0, "P3 지나간 자취는 곧 사라진다(그려진 땅은 남는다)");

  // D. 숲 — 눈 속 가지(털어 보기 → 뽑기, 숨은 규칙: 비율 · 끝 빛깔)
  await click(await dbg("sitePx", "forestA"), 0);
  s = await until((x) => x.dev === "forestA" && !x.turning, 3000);
  ok(s.dev === "forestA", "D1 숲 어귀를 누르면 책장이 넘어가 숲 장면으로 들어간다");
  const dd = s.day; await fr.waitForTimeout(400);
  ok(Math.abs((await S()).day - dd) < 1e-6, "D2 장면 속에선 바깥 시계가 서고, 손을 쓸 때만 시간이 든다");
  const w0 = (await S()).res.wood; await dbg("pull", 0, true);
  ok((await S()).res.wood === w0, "D3 털어 보기 전엔 뽑히지 않는다(살펴보기가 먼저)");
  await dbg("brush", 0); s = await S();
  ok(s.stats.brushes === 1 && s.day > dd && s.look && s.look.subj === "wood", "D4 끝을 누르면 눈이 털린다 — 처음 본 가지 끝은 쪽지로");
  await write("끝이 노란 가지가 잘 마른 걸까?");
  ok((await S()).notes.noted.includes("wood"), "D5 적으면 오른쪽 공책 쪽이 그 더미들을 기록한다");
  await dbg("pull", 0, true); s = await S();
  ok(s.res.wood > w0 + 0.4 && s.stats.pulls === 1, "D6 끝까지 끌면 뽑혀 땔감이 된다");
  const lowCup = (await dbg("cups")).findIndex((c) => c.ratio <= 0.62);
  await st(([ci]) => { const c = window.__gtDebug.state().sites.forestA.data.cups[ci]; c.sticks = c.sticks.map((k, i) => ({ good: i < 7, sh: k.sh, seen: true })); c.streak = 0; }, [lowCup]);
  for (let i = 0; i < 5; i++) await dbg("pull", lowCup, true);
  ok((await S()).stars.includes("forest"), "D7 숨은 규칙 — 덜 나오는 더미에서 다섯 번 내리 마른 가지면 별");
  await shot("gt-forest");
  await click(await dbg("sceneClose"), 0);
  s = await until((x) => !x.dev && !x.turning, 3000);
  ok(!s.dev && s.scene === "world", "D8 닫으면 책장이 넘어가 땅으로");

  // L. 바람 — 헝겊(살펴보기) · 바람막이(해 보기)
  const home = await st(() => { const H0 = window.__gtDebug.state().home; return { u: H0.u, v: H0.v }; });
  await dbg("teleport", home.u, home.v); await dbg("cam", 2, home.u, home.v); await fr.waitForTimeout(150);
  await click(await dbg("ragPx")); s = await S();
  ok(s.looked === 2 && s.look && s.look.subj === "wind", "L1 헝겊을 누르면 바람을 살핀다(쪽지)");
  await shut();
  await dbg("setRes", "wood", 12);
  await click(await dbg("homePx")); s = await S();
  ok(s.fence, "L2 움막을 누르면 바람막이가 손에 들린다");
  const spot = await dbg("fenceSpot", true), tokp = await dbg("px", home.u + 0.04, home.v + 0.006);
  await drag(line(tokp, await dbg("px", spot.u, spot.v), 8));
  s = await S();
  ok(s.fences === 1 && s.lee && s.res.wood <= 10.1 && s.stars.includes("lee"), `L3 바람이 불어 오는 쪽에 세우면 그늘(연기가 곧게) — 바람을 적고 살핀 뒤라 별 [${s.fences} · ${s.lee}]`);
  await shot("gt-fence");

  // B. 새 떼 — 처음엔 흩어지고 쪽지. 새를 적으면 그다음부터 잡힌다
  await st(() => { const D = window.__gtDebug.state(); Object.assign(D.mw, { on: false, done: false, known: false, start: D.day + 40 }); D.signs = []; D.nextSign = D.day + 40; });   // 한겨울 · 새 떼는 멀리 — 시험이 고른 때에만
  await dbg("spawnSign", "crow"); await fr.waitForTimeout(60); await click(await dbg("signPx")); s = await S();
  ok(s.signs === 0 && s.look && s.look.subj === "birds" && s.stats.signs === 0 && !s.mw.known, "B1 처음 보는 새 떼는 흩어지고 쪽지만 남는다");
  await write("까마귀가 남쪽으로 가네");
  s = await S();
  ok(s.stats.signs === 1 && s.mw.known && s.notes.noted.includes("birds"), "B2 적으면 그 새 떼가 알리던 것을 안다 — 까마귀는 한겨울(책갈피에 푸른 띠)");
  await dbg("spawnSign", "gull"); await fr.waitForTimeout(60); await click(await dbg("signPx")); s = await S();
  ok(s.stats.signs === 2 && !s.look, "B3 새를 적은 뒤로는 누르면 바로 잡힌다");

  // R. 강 — 걸음이 강가에서 멈추고 그 자리가 여울이 된다. 얼음 위에서: 돌 · 뚫기 · 낚시 · 건너기
  await dbg("teleport", home.u, home.v); await dbg("cam", 1);
  const across = await st(() => { const D = window.__gtDebug.state(), v = D.home.v + 0.02, r = D.world.river; const ru = r.c + r.a1 * Math.sin(v * Math.PI * 1.6 + r.p1) + r.a2 * Math.sin(v * Math.PI * 4.3 + r.p2); return { u: ru + (D.home.u < ru ? 0.06 : -0.06), v }; });
  await click(await dbg("px", across.u, across.v), 0);
  s = await until((x) => !x.walking, 9000);
  const fordAt = await dbg("site", "ford"), meAt = await st(() => window.__gtDebug.state().me);
  ok(s.blocked && s.sites.ford.placed && s.sites.ford.open && Math.hypot(fordAt.u - meAt.u, (fordAt.v - meAt.v) / 1.45) > 0.015, "R1 강을 건너려 하면 강가에서 멈추고, 얼음 위 그 자리(여울)가 생긴다");
  await shot("gt-ford");
  await click(await dbg("sitePx", "ford"), 0);
  s = await until((x) => x.dev === "ford" && !x.turning, 3000);
  ok(s.dev === "ford", "R2 여울을 누르면 얼음 위 장면으로");
  let rv = await dbg("river");
  const thin = await st(() => { const g = window.__gtDebug; let best = null; for (let x = 0.05; x <= 0.95; x += 0.05) for (let iy = 0.1; iy <= 0.9; iy += 0.05) { const t = g.thAt(x, iy); if (!best || t < best.t) best = { x, iy, t }; } return best; });
  const thick = await st(() => { const g = window.__gtDebug; let best = null; for (let x = 0.05; x <= 0.95; x += 0.05) for (let iy = 0.1; iy <= 0.9; iy += 0.05) { const t = g.thAt(x, iy); if (!best || t > best.t) best = { x, iy, t }; } return best; });
  await click(await dbg("icePx", thick.x, thick.iy)); rv = await dbg("river"); const stoneK = await st(() => window.__gtDebug.state().sites.ford.data.stones.slice(-1)[0].k);
  ok(rv.stones === 1 && ["clack", "crack", "plop"].includes(stoneK), `R3 얼음을 누르면 돌을 던진다 — 소리로만(${stoneK})`);
  const R0 = await dbg("riverPx");
  await drag(line(R0.auger, await dbg("icePx", thick.x, thick.iy), 10)); await fr.waitForTimeout(100);
  rv = await dbg("river"); s = await S();
  ok(rv.holes.length === 1 && rv.fails === 0 && s.look && s.look.subj === "ice", "R4 송곳을 끌어다 놓으면 뚫어 잰다 — 얼음 기둥은 쪽지로");
  await write("얼음은 하루에 얼마나 두꺼워질까?");
  if (thin.t < 7) {
    const fd0 = (await S()).res.food; await dbg("drill", thin.x, thin.iy); rv = await dbg("river"); s = await S();
    ok(rv.fails === 1 && s.res.food < fd0, `R5 서 있기에도 얇은 곳(${thin.t.toFixed(1)}cm)을 뚫으면 빠진다 — 양식 · 땔감을 잃는다`);
    await st(() => { window.__gtDebug.state().sites.ford.data.fails = 0; });   // (별 시험을 위해 시험이 지운다)
    await fr.waitForTimeout(1500);
  } else ok(true, "R5 (얇은 곳이 없어 건너뜀)");
  const dW = (await S()).day; await dbg("wait", 4); s = await until((x) => x.day >= dW + 1.9, 4000);
  await dbg("drill", thick.x, thick.iy); rv = await dbg("river");
  ok(s.day >= dW + 1.9 && rv.holes[0].n === 2, "R6 모래시계로 이틀을 기다렸다가 같은 구멍을 다시 잰다(공책에 줄)");
  const fd1 = (await S()).res.food; await dbg("fish", 0); await dbg("bite"); const hooked = await dbg("hook"); rv = await dbg("river"); s = await S();
  ok(hooked && rv.catches === 1 && s.res.food > fd1 - 0.05, "R7 낚싯대를 구멍에 — 찌가 잠길 때 누르면 한 마리");
  await shot("gt-river");
  const best = await dbg("bestX"); if ((await S()).day < best.safe + 0.1) await dbg("setDay", best.safe + 0.1);
  ok(await dbg("cross", best.x), "R8 내게서 건너편 둑까지 길을 그으면 건넌다");
  await dbg("runDev", 6000);
  s = await until((x) => !x.dev && !x.turning, 4000);
  ok(s.riverCrossed && s.stars.includes("river"), "R9 숨은 규칙 — 다른 날 두 번 잰 구멍이 있고, 빠지지 않고, 버티게 된 날 곧바로 건너면 별");
  s = await until((x) => x.walking, 3000);
  ok(s.walking && !s.blocked, "R10 건너고 나면 멈췄던 길이 이어진다");
  await dbg("arrive");

  // S. 바다 — 물가에서 멈추고 그 자리(배)가 생긴다. 물결 재기 · 낚시(숨은 규칙: 주기)
  const sh = await dbg("site", "shore"), seaEdge = await st(([u]) => { const D = window.__gtDebug.state(), q = D.world.sea; return q.b + 0.03 * Math.sin(u * Math.PI * 2.4 + q.p) + 0.016 * Math.sin(u * Math.PI * 6.5 + q.q); }, [sh.u]);
  await dbg("teleport", sh.u, seaEdge - 0.14); await dbg("cam", 1.4, sh.u, seaEdge - 0.05); await fr.waitForTimeout(100);
  await click(await dbg("px", sh.u, seaEdge + 0.05), 0);
  s = await until((x) => !x.walking, 9000);
  ok(s.sites.shore.placed && s.sites.shore.open && s.me.v < seaEdge, "S1 바다 앞에서 걸음이 멈추고 물가 자리가 생긴다");
  await click(await dbg("sitePx", "shore"), 0);
  s = await until((x) => x.dev === "shore" && !x.turning, 3000);
  ok(s.dev === "shore" && (await dbg("cast")) === null, "S2 물가 장면 — 재 보기 전엔 던질 수 없다");
  await dbg("read"); s = await S();
  ok(s.look && s.look.subj === "sea", "S3 눈금 막대를 재면 물결 높이가 쪽지로");
  await write("바다는 언제 잔잔할까?");
  for (let i = 0; i < 3; i++) { await dbg("read"); await dbg("jump", 1); }
  const sea = await dbg("sea");
  await st(([P]) => { const D = window.__gtDebug.state(); D.world.waves.phase = D.day - P / 2 + 0.45; D.mw.on = false; }, [sea.period]);
  const f0 = (await S()).res.food, k1 = await dbg("cast"), k2 = await dbg("cast"), k3 = await dbg("cast"); s = await S();
  ok(k1 === "calm" && k2 === "calm" && k3 === "calm" && s.res.food > f0 && s.stars.includes("sea"), `S4 숨은 규칙 — 여러 날 재고 잔잔할 때 세 번 내리 던지면 별(${k1},${k2},${k3})`);
  await shot("gt-shore");
  await dbg("leave"); await until((x) => !x.dev && !x.turning, 3000);

  // M. 산 — 산기슭에서 멈추고 돌무더기가 생긴다. 등고선을 따라 비스듬히 오르면 빠르다(토블러)
  const sm = await dbg("site", "summit");
  await dbg("teleport", sm.u, Math.min(0.75, sm.v + 0.45)); await dbg("cam", 1, sm.u, sm.v + 0.3); await fr.waitForTimeout(100);
  await click(await dbg("px", sm.u, sm.v + 0.05), 0);
  s = await until((x) => !x.walking, 9000);
  ok(s.sites.trail.placed && s.sites.trail.open && !s.sites.summit.linked, "M1 산에 닿으면 걸음이 멈추고 산기슭 돌무더기(오르는 자리)가 생긴다");
  await click(await dbg("sitePx", "trail"), 0);
  s = await until((x) => x.dev === "trail" && !x.turning, 3000);
  ok(s.dev === "trail", "M2 돌무더기를 누르면 등고선 지도 장면으로");
  const m0 = await dbg("mtn");
  await dbg("climb", [[m0.at.x, m0.at.y - 0.25]]); await dbg("runDev", 20000); let m1 = await dbg("mtn"); s = await S();
  ok(m1.t.mt > 0 && m1.t.dh > 0.03 && s.look && s.look.subj === "mount", `M3 곧장 오르면 가파를수록 느리다 — 처음 오른 길은 쪽지로(${m1.t.mt.toFixed(2)}일)`);
  await write("가파르면 왜 이렇게 느리지?");
  await dbg("climb", await dbg("mtnRoute")); await dbg("runDev", 120000); m1 = await dbg("mtn"); s = await S();
  ok(m1.reached && s.stars.includes("mount") && s.mw.known, `M4 숨은 규칙 — 등고선을 비스듬히(가파름 0.29쯤) 오르면 곧장보다 빨라 별(${m1.t.mt.toFixed(2)} / ${m1.t.ms.toFixed(2)}일)`);
  await fr.waitForTimeout(600); await shot("gt-summit");
  await dbg("leave"); s = await until((x) => !x.dev && !x.turning && x.titled, 6000);
  ok(!s.dev && s.titled && s.sites.summit.linked, "M5 내려오면 땅 전체가 지도에 그려지고, 바다 위에 처음 적은 그 이름이 — 이 땅의 이름이었다");

  // E. 독수리 — 지나간 뒤로 깃털이 있다(답을 보여 주는 대가로 덤불이 돌이 된다)
  ok(await dbg("eagleFly"), "E1 독수리가 산에서 하늘을 지나간다");
  await dbg("teleport", fa.u, fa.v + 0.03); ok(await dbg("enter", "forestA"), "E2 숲으로 다시"); await until((x) => !x.turning, 3000);
  const c0s = (await S()).self.C, stones0 = (await S()).stones;
  await dbg("eagle"); s = await S();
  ok(s.stones === stones0 + 1 && s.self.C < c0s && await st(() => !!window.__gtDebug.state().sites.forestA.data.eagle), "E3 깃털을 누르면 답이 보이고, 덤불 하나가 돌로 굳고, 나는 '기대기' 쪽으로");
  await dbg("leave"); await until((x) => !x.dev && !x.turning, 3000);

  // SE. 자아 — 문턱 두 겹
  ok((await dbg("setSelf", 0, 0, 0)) === "wren" && (await dbg("setSelf", 0.2, 0.2, 0)) === "wren" && (await dbg("setSelf", 0.3, 0.3, 0)) === "owl" && (await dbg("setSelf", 0.2, 0.2, 0)) === "owl" && (await dbg("setSelf", 0.1, 0.1, 0)) === "wren",
    "SE1 자아 이름은 문턱을 두 겹으로 — 들어갈 땐 높게, 나올 땐 낮게");
  ok((await dbg("setSelf", -0.4, -0.4, 0)) === "swallow" && (await dbg("setSelf", 0.4, -0.4, 0)) === "magpie" && (await dbg("setSelf", -0.4, 0.4, 0)) === "crane", "SE2 제비 · 까치 · 두루미 — 네 갈래");
  await dbg("setSelf", 0, 0, 0);

  // RS. 덮어 두기 → 표지에 그 이름 → 이어 하기
  await dbg("teleport", home.u, home.v); await dbg("cam", 1.6, home.u, home.v);
  const dayR = (await S()).day, starsR = (await S()).stars.join(), memosR = (await S()).notes.memos;
  await click(await dbg("hudPx", "leave"));
  ok((await S()).scene === "world", "RS1 덮기는 한 번 누르면 붉은 고리 — 두 번 눌러야 덮인다");
  await click(await dbg("hudPx", "leave"), 0);
  s = await until((x) => x.scene === "cover" && !x.turning, 4000);
  ok(s.scene === "cover" && s.cur && s.cover === "하늘이", `RS2 덮으면 표지 쪽지에 그 이름 · 책갈피 끈(${s.cover})`);
  await shot("gt-cover-named");
  const dC = s.day; await fr.waitForTimeout(1200);
  ok((await S()).day === dC, "RS3 덮어 둔 동안엔 날짜가 흐르지 않는다");
  await click(mid, 0);
  s = await until((x) => x.scene === "world" && !x.turning, 4000);
  ok(s.scene === "world" && s.name === "하늘이" && Math.abs(s.day - dayR) < 0.3 && s.lee && s.stars.join() === starsR && s.notes.memos === memosR && s.riverCrossed, "RS4 표지를 누르면 그 날 그 자리에서 다시(공책 · 바람막이 · 별 · 건넌 강 그대로)");

  // W. 한겨울
  await dbg("forceMw"); await dbg("jump", 0.1);
  s = await until((x) => x.mw.on, 2000);
  ok(s.mw.on, "W1 한겨울 — 서리가 끼고, 땔감이 더 든다");
  await shot("gt-midwinter");

  // END. 봄 → 끝 장(이 땅의 이름이 제목) → 표지('무제')
  await dbg("setRes", "food", 40); await dbg("setRes", "wood", 40);
  await dbg("jump", 30);
  s = await S();
  ok(s.over && s.over.kind === "spring", "END1 버티면 봄이 온다(꽃 · 제비)");
  s = await until((x) => x.scene === "keep" && !x.turning, 8000);
  ok(s.scene === "keep" && s.runs === 1 && s.keepName === "하늘이" && s.keepMeets === 0, "END2 끝 장 — 제목은 처음 적은 그 이름, 그림 한 장 · 별 · 메모 두 줄 · 내 곡선");
  await shot("gt-keep");
  await click(mid, 0);
  s = await until((x) => x.scene === "cover" && !x.turning, 4000);
  ok(s.scene === "cover" && !s.cur && s.cover === "무제", "END3 끝 장을 누르면 표지로 — 새 공책은 다시 '무제'");
  // 두 번째 겨울 — 이름을 비우면 '무제', 지난 곡선과 만나는 점(2막의 문)
  await click(mid, 0); s = await until((x) => x.scene === "name" && !x.turning, 4000);
  await fr.locator("#nameIn").press("Enter");
  s = await until((x) => x.scene === "world" && !x.turning, 4000);
  ok(s.name === "무제" && s.notes.memos === 0, "END4 이름을 비워 두면 이 땅은 '무제' — 새 공책은 비어 있다");
  await dbg("setSelf", 0.6, -0.6, 0.3);
  await dbg("end", "cold");
  s = await until((x) => x.scene === "keep" && !x.turning, 8000);
  ok(s.runs === 2 && typeof s.keepMeets === "number", `END5 두 번째 겨울부터 지난 곡선과 만나는 점을 센다(${s.keepMeets})`);
  await click(mid, 0);
  s = await until((x) => x.scene === "cover" && !x.turning, 4000);

  // TU. 다듬기(강사용)
  await fr.locator("#btnTune").click();
  const memo = await fr.locator("#tuneMemo").innerText();
  ok(/숨은 규칙/.test(memo) && /이 땅의 이름/.test(memo) && /볼거리/.test(memo) && /토블러/.test(memo) && !/"geo"|"lat"|"lon"/.test(await fr.locator("#tuneJson").inputValue()), "TU1 다듬기 — 강사에게만 숨은 규칙 · 이름 · 볼거리 메모(세상의 자리는 기록에도 보이지 않는다)");
  await fr.locator('#tuneBody [data-k="dayLen"]').fill("20");
  await fr.locator("#tApply").click();
  s = await S();
  ok(s.params.dayLen === 20 && (await fr.locator(".trow.chg").count()) >= 1, "TU2 하루 길이를 바꿔 적용하면 저장되고 금빛으로 표시");
  await fr.locator("#tReset").click();
  s = await S();
  ok(s.params.dayLen === 15 && (await fr.locator("#tNew").isDisabled()), "TU3 기본값으로 되돌린다 · 이어 하던 공책이 없으면 버리기는 잠긴다");
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
      ok(/무제/.test(await row.innerText()), "B1 시록고 더보기에 「게임 — 무제」");
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
      ok(saved && saved.v === 4 && saved.runs.length >= 2 && saved.self, `M1 기록은 앱이 맡아 둔다(ashrain.games.gulttuksae · 지난 겨울 ${saved && saved.runs.length})`);
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
