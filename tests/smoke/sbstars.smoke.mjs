// 선빵스타즈(#/admin/games/sb) 스모크 — 관리자 게임 자리와 게임을 실제 브라우저로 해 본다.
//   node tests/smoke/sbstars.smoke.mjs [--headed]     빌드 후(dist/ 필요): 비관리자 막힘 · 관리자 iframe · 상단 바 · 전투 중 상단 바 숨김 · 진행 저장 + 게임 검사
//   node tests/smoke/sbstars.smoke.mjs --game-only    빌드 없이 게임 HTML 한 장만 바로 열어 게임 검사
// 준비: playwright + Chromium. 30초 ~ 1분. 키패드 · 조이스틱 · 단추는 진짜 클릭 · 터치(PointerEvent)로, 필살기 게이지와 시간 끝은 갈고리(__sbstars)로.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); }
catch { try { ({ chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright")); } catch { ({ chromium } = require("/opt/npm-tools/node_modules/playwright")); } }

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "../..");
const DIST = path.join(ROOT, "dist");
const GAME = path.join(ROOT, "src/features/games/sbstars.html");
const HEADED = process.argv.includes("--headed");
const GAME_ONLY = process.argv.includes("--game-only");
const SHOTS = process.env.SMOKE_SHOTS || path.join(HERE, "shots");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

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
      res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(0, "127.0.0.1", () => resolve({ srv, port: srv.address().port }));
  });
}

// ── Supabase 모의 — 역할만 바꿔 가며(games.smoke.mjs 와 같은 꼴) ──
const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const USER = { id: "00000000-0000-4000-8000-000000000001", aud: "authenticated", role: "authenticated", email: "smoke@example.com", app_metadata: { provider: "email", providers: ["email"] }, user_metadata: {}, factors: [], created_at: "2026-01-01T00:00:00Z" };
const JWT = `${b64u({ alg: "HS256", typ: "JWT" })}.${b64u({ sub: USER.id, aud: "authenticated", role: "authenticated", email: USER.email, exp: 9999999999, iat: 1700000000, aal: "aal1", amr: [{ method: "password", timestamp: 1700000000 }], session_id: "s1" })}.sig`;
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
    if (u.pathname.startsWith("/storage/v1/object/list")) return json([]);
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
    if (window.top !== window) return;
    localStorage.setItem(key, JSON.stringify(sess));
    if (!localStorage.getItem("ashrain-theme")) localStorage.setItem("ashrain-theme", "light");
  }, ["sb-placeholder-auth-token", SESSION]);
}

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };
const typeAns = async (fr, s) => { for (const ch of String(s).replace(/-/g, "−")) await fr.locator(`#kp button[data-key="${ch}"]`).click(); };
const touch = (fr, type, id, x, y) => fr.evaluate(([type, id, x, y]) => document.getElementById("cv").dispatchEvent(
  new PointerEvent(type, { pointerId: id, pointerType: "touch", clientX: x, clientY: y, bubbles: true, isPrimary: true, button: 0 })), [type, id, x, y]);
const drag = async (fr, id, x, y, dx, dy, holdMs = 120) => { await touch(fr, "pointerdown", id, x, y); await touch(fr, "pointermove", id, x + dx, y + dy); await sleep(holdMs); await touch(fr, "pointerup", id, x + dx, y + dy); };

// ── 게임 검사 — fr: 게임 문서가 든 프레임 ──
async function sbChecks(fr, shot, app) {
  await fr.locator("#lobby").waitFor({ timeout: 20000 });
  await fr.waitForFunction(() => !!window.__sbstars, null, { timeout: 20000 });
  await fr.waitForFunction(() => document.getElementById("help").classList.contains("open"), null, { timeout: 5000 }).catch(() => {});
  ok(await fr.evaluate(() => document.getElementById("help").classList.contains("open")), "G1 처음 열면 게임 방법을 보여 준다");
  await fr.locator("#help [data-close]").click();
  const st = await fr.evaluate(() => { const S = __sbstars.S; return { lines: S.lines.length, fuel: S.lines.reduce((s, L) => s + L.fuel, 0), slopes: new Set(S.lines.map((L) => L.n + "/" + L.d)).size, ammo: S.ammo, lobs: S.lobs.length, shocks: S.shocks, cnt: S.cnt.length, prb: S.prb.length }; });
  ok(st.lines > 400 && st.slopes === 22 && st.ammo >= 200 && st.lobs >= 16 && st.shocks >= 6 && st.cnt >= 3 && st.prb >= 3,
    `G2 문제를 많이 푼 상태로 시작 — 직선 ${st.lines}개(기울기 ${st.slopes}가지) · 탄환 ${st.ammo} · 투척 ${st.lobs} · 충격파 ${st.shocks} · 부스터 ${st.cnt + st.prb}`);
  ok((await fr.locator(".ch").count()) === 5, "G3 캐릭터 다섯(탱커 · 원딜러 · 근접 · 힐러 · 투척)");
  await fr.locator('.ch[data-c="1"]').click();
  const chd = await fr.locator("#chd").innerText();
  ok(/솔/.test(chd) && /데카르트 저격/.test(chd) && /가우스의 합/.test(chd), "G3 고른 캐릭터(솔)의 기본 공격 · 필살기 설명");

  const ans = await fr.evaluate(() => { const p = __sbstars.cur.lin; return { a: SB.fs(p.ans.a), b: String(p.ans.b), lock: !!p.blanks[0].lock }; });
  if (!ans.lock) { await fr.locator("#bl-a").click(); await typeAns(fr, ans.a); }
  await fr.locator("#bl-b").click(); await typeAns(fr, ans.b); await fr.locator("#okKey").click();
  const g4 = await fr.evaluate(() => ({ fb: document.getElementById("fb").textContent, log: document.querySelector("#log .li").textContent, fuel: __sbstars.S.lines.reduce((s, L) => s + L.fuel, 0), cnt: __sbstars.S.cnt.length }));
  ok(/정답/.test(g4.fb) && /획득/.test(g4.log) && g4.fuel > st.fuel && g4.cnt === st.cnt - 1, `G4 일차함수를 키패드로 맞히면 길이 늘고 파스칼 부스터 하나를 쓴다(+${Math.round(g4.fuel - st.fuel)}칸)`);
  await fr.locator("#tab-cnt").click(); await fr.locator("#bl-n").click(); await typeAns(fr, "999"); await fr.locator("#okKey").click();
  ok(/다시/.test(await fr.locator("#fb").innerText()), "G5 틀리면 「다시」 — 보상 없음");
  await fr.locator("#tab-eq2").click();
  const q = await fr.evaluate(() => ({ r: __sbstars.cur.eq2.ans.map(String), dbl: __sbstars.cur.eq2.dbl, lobs: __sbstars.S.lobs.length, shocks: __sbstars.S.shocks }));
  await fr.locator("#bl-r1").click(); await typeAns(fr, q.r[1]); await fr.locator("#bl-r2").click(); await typeAns(fr, q.r[0]); await fr.locator("#okKey").click();
  const q2 = await fr.evaluate(() => ({ lobs: __sbstars.S.lobs.length, shocks: __sbstars.S.shocks }));
  ok(q.dbl ? q2.shocks === q.shocks + 1 : q2.lobs === q.lobs + 1, `G6 이차방정식(두 근 순서를 바꿔 넣어도) → ${q.dbl ? "알콰리즈미 충격파" : "브라마굽타 투척"} +1`);
  await fr.locator("#tab-lin").click();
  await sleep(300); await shot("sbstars-lobby");

  await fr.locator("#go").click();
  await fr.waitForFunction(() => __sbstars.B.on && __sbstars.B.cd <= 0, null, { timeout: 8000 });
  const b0 = await fr.evaluate(() => ({ units: __sbstars.U.length, mine: __sbstars.U.filter((u) => u.team === 0).length, ch: __sbstars.P.ch.name }));
  ok(b0.units === 6 && b0.mine === 3 && b0.ch === "솔", "G7 3대3 — 내 캐릭터 솔 + 아군 AI 둘 · 적 AI 셋");
  if (app) ok((await app.page.locator(".ag-root.ag-imm").count()) === 1, "G7 전투 중에는 앱 상단 바를 숨긴다(ash-immersive)");

  const [W, H] = await fr.evaluate(() => [innerWidth, innerHeight]);
  const before = await fr.evaluate(() => ({ x: __sbstars.P.x, y: __sbstars.P.y }));
  const mx = Math.round(W * 0.15), my = H - 140;
  await touch(fr, "pointerdown", 11, mx, my); await touch(fr, "pointermove", 11, mx + 60, my - 45);
  const onLine = [];
  for (let i = 0; i < 6; i++) { await sleep(150); onLine.push(await fr.evaluate(() => { const P = __sbstars.P, L = P.line; if (!L) return P.snap ? "snap" : "none"; const a = L.n / L.d; return P.snap ? "snap" : Math.abs(a * P.x - P.y + L.b) / Math.hypot(1, a) < 0.02 ? "on" : "off"; })); }
  const g8 = await fr.evaluate(() => { const P = __sbstars.P, L = P.line; return { x: P.x, y: P.y, line: L && [L.n, L.d, L.b], fuel: L && L.fuel, dist: __sbstars.B.stats.dist, eqn: document.getElementById("eqn").textContent }; });
  ok(Math.hypot(g8.x - before.x, g8.y - before.y) > 1 && !onLine.includes("off") && onLine.includes("on") && /y =/.test(g8.eqn),
    `G8 왼쪽 조이스틱 — 가진 직선 위로만 달린다(${g8.line && g8.line.join(",")} · ${g8.dist.toFixed(1)}칸 · 표본 ${onLine.join(" ")})`);
  ok(g8.fuel < 40, `G8 달린 만큼 그 직선의 이동값이 준다(남은 ${g8.fuel && g8.fuel.toFixed(1)}칸)`);
  await shot("sbstars-move");
  await touch(fr, "pointerup", 11, mx + 60, my - 45);

  const ammo0 = await fr.evaluate(() => __sbstars.S.ammo);
  await drag(fr, 12, W - 130, H - 140, -10, -70);
  ok((await fr.evaluate(() => __sbstars.S.ammo)) === ammo0 - 1 && (await fr.evaluate(() => __sbstars.B.stats.atk)) >= 1, "G9 오른쪽 조이스틱을 끌었다 놓으면 탄환 1발로 기본 공격");
  await fr.evaluate(() => { const P = __sbstars.P; P.sup = P.ch.sup.need; });
  const bp = await fr.evaluate(() => __sbstars.btnPos());
  await sleep(350);
  const n0 = await fr.evaluate(() => __sbstars.shotN);
  await drag(fr, 13, bp.sup.x, bp.sup.y, 0, -60);
  await sleep(1000);
  const g10 = await fr.evaluate(() => ({ sup: __sbstars.P.sup, fired: __sbstars.shotN }));
  ok(g10.sup === 0 && g10.fired - n0 >= 10, `G10 필살기 단추 — 가우스의 합 10연사(1초 동안 쏜 탄 ${g10.fired - n0}발 — 아군 · 적 AI 탄 포함)`);
  await shot("sbstars-super");
  const gl = await fr.evaluate(() => ({ lobs: __sbstars.S.lobs.length, shocks: __sbstars.S.shocks }));
  await drag(fr, 14, bp.bra.x, bp.bra.y, 0, -60);
  await touch(fr, "pointerdown", 15, bp.shk.x, bp.shk.y); await touch(fr, "pointerup", 15, bp.shk.x, bp.shk.y);
  const gl2 = await fr.evaluate(() => ({ lobs: __sbstars.S.lobs.length, shocks: __sbstars.S.shocks, flying: __sbstars.lobs }));
  ok(gl2.lobs === gl.lobs - 1 && gl2.flying >= 1 && gl2.shocks === gl.shocks - 1, "G11 브라마굽타 투척(끌어 겨누기) · 알콰리즈미 충격파(톡) 단추");
  await sleep(2500);
  await fr.evaluate(() => { __sbstars.B.left = 0.05; });
  await fr.waitForFunction(() => document.getElementById("result").classList.contains("open"), null, { timeout: 6000 }).catch(() => {});
  ok(await fr.evaluate(() => document.getElementById("result").classList.contains("open")), "G12 시간이 끝나면 결과(처치 · 준 피해 · 달린 거리 · 남은 길)");
  await shot("sbstars-result");
  await fr.locator("#toLobbyBtn").click();
  await sleep(200);
  ok(await fr.locator("#lobby").isVisible(), "G12 로비로 돌아온다");
  if (app) ok((await app.page.locator(".ag-root.ag-imm").count()) === 0, "G12 로비에서는 앱 상단 바가 다시 보인다");
  return fr.evaluate(() => __sbstars.S.ammo);
}

(async () => {
  const { srv, port } = await serve();
  const base = `http://127.0.0.1:${port}/`;
  const browser = await chromium.launch({ headless: !HEADED, ...(fs.existsSync("/usr/bin/google-chrome") && !process.env.PW_BUNDLED ? { executablePath: "/usr/bin/google-chrome" } : {}) });
  const ctx = await browser.newContext({ viewport: { width: 1180, height: 820 }, deviceScaleFactor: 1, hasTouch: true });
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
      await sbChecks(page.mainFrame(), shot, null);
    } else {
      await mockSupabase(page);
      ROLE = "student";
      await page.goto(base + "#/admin/games/sb");
      await page.getByText("관리자만 들어올 수 있는 곳이에요.").waitFor({ timeout: 20000 });
      ok((await page.locator("iframe").count()) === 0 && !urls.some((u) => /sbstars/.test(u)), "A1 비관리자 — 안내만, 게임 파일을 받지 않는다");

      ROLE = "admin";
      await page.goto(base + "#/");
      await page.reload();
      await page.locator(".sh-abtn", { hasText: "🎱 게임" }).waitFor({ timeout: 20000 });
      await page.evaluate(() => { location.hash = "#/admin/games/sb"; });
      const el = page.locator('iframe.ag-frame[title="선빵스타즈"]');
      await el.waitFor({ timeout: 20000 });
      ok((await el.getAttribute("sandbox")) === "allow-scripts" && urls.some((u) => /sbstars/.test(u)) && !urls.some((u) => /slope-shot|po-minjok/.test(u)),
        "B1 #/admin/games/sb — 고른 게임 파일만 받아 샌드박스(allow-scripts) iframe 에 띄운다");
      ok((await page.locator(".fb-act").count()) === 3 && /선빵스타즈/.test(await page.locator(".fb-act.pri").innerText()), "B2 상단 바에 세 게임 — 지금은 선빵스타즈");
      const fr = await (await el.elementHandle()).contentFrame();
      await fr.locator("#lobby").waitFor({ timeout: 20000 });
      await fr.waitForFunction(() => !!window.__sbstars, null, { timeout: 20000 });
      const h = await fr.evaluate(() => __sbstars.host());
      ok(h.inFrame && !h.canLocal, "B3 게임 안에서는 앱 저장소에 닿지 않는다 — 저장은 부모에게 맡긴다");
      const ammo = await sbChecks(fr, shot, { page });
      const saved = await page.evaluate(() => { const t = localStorage.getItem("ashrain.games.sbstars"); return t ? { len: t.length, d: JSON.parse(t) } : null; });
      ok(saved && saved.len < 20000 && Array.isArray(saved.d.L) && saved.d.L.length > 400 && saved.d.ammo === ammo && saved.d.help === true && saved.d.ch === 1,
        `S1 진행은 앱이 이 기기에 맡아 둔다(ashrain.games.sbstars · ${saved && saved.len}자 · 직선 ${saved && saved.d.L.length}개 · 탄환 ${saved && saved.d.ammo})`);
      await page.reload();
      const el2 = page.locator('iframe.ag-frame[title="선빵스타즈"]');
      await el2.waitFor({ timeout: 20000 });
      const fr2 = await (await el2.elementHandle()).contentFrame();
      await fr2.locator("#lobby").waitFor({ timeout: 20000 });
      await fr2.waitForFunction((a) => window.__sbstars && __sbstars.S.ammo === a, ammo, { timeout: 5000 }).catch(() => {});
      await sleep(1000);
      const back = await fr2.evaluate(() => ({ ammo: __sbstars.S.ammo, ch: __sbstars.S.ch, help: document.getElementById("help").classList.contains("open") }));
      ok(back.ammo === ammo && back.ch === 1 && !back.help, "S2 새로고침해도 자원 · 고른 캐릭터가 돌아오고, 게임 방법은 다시 뜨지 않는다");
    }
    ok(errors.length === 0, "E1 콘솔 오류 없음" + (errors.length ? " — " + errors.slice(0, 3).join(" | ") : ""));
  } catch (e) {
    fail++; console.log("FAIL - 예외:", e.message);
    await shot("sbstars-fail");
  } finally {
    await browser.close(); srv.close();
  }
  console.log(`\n${pass} passed · ${fail} failed`);
  process.exit(fail ? 1 : 0);
})();
