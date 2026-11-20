// node tests/display-curio2.test.mjs — 수학 호기심 공 운동 아홉(배드민턴 · 테니스 · 탁구 · 배구 · 족구 · 세팍타크로 · 골프 · 당구 · 볼링)과
// 「풀이: 상세 | 최소화」 검산. 실패 시 exit 1.
//   네트 운동: 가상 경기의 점수 흐름(이긴 쪽 +1, 세트 끝 규칙) · 공 자리가 그림 안 · 결정구가 네트를 넘거나 걸린 공 ·
//             네트를 지난 자리(y절편)를 유리수로 다시 셈 · 초등 칸 셈(비례)이 같은 자리를 가리키는지.
//   배드민턴(ShuttleSet 실제 경기 — 세트마다 고른 랠리): 랠리마다 이긴 쪽 +1, 점수는 세트 안에서 늘기만 하고 기록된 결승 점수를 넘지 않는다.
//   골프: 홀마다 마지막 샷은 홀컵, 타수 = 샷 + 벌타, 합계 · 포물선 y = a(x − p)² + q 가 (0, 0) · (날아간 거리, 0)을 지나는지.
//   당구: 꺾이는 점은 쿠션 위, 반사(쿠션에 비친 점 · 꺾이는 점 · 다음 점이 한 직선), H 는 직선 CR′ 위(유리수), 노란 공이 직선 CR 을 막는지.
//   볼링: 점수를 따로 다시 셈(스트라이크 10 + 다음 두 번 · 스페어 10 + 다음 한 번 · 10프레임), 핀은 서 있던 것만 쓰러짐, 핀 보드 = 4c − 3b.
//   그리기: 새 액자 넷(네트 여섯 종목 포함)을 상세 · 최소화 × 초등 · 중등 × 두 테마로, 기존 일곱은 최소화로 훑어 오류 · NaN 이 없는지.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { lineOf, fs as fsx, frac } from "../src/features/display/curio/kit.js";
import { NETS, netY, crosses, setDone, genMatch, badmintonMatches, keyShot, netSteps, scheduleOf, rallyAt, tennisPts } from "../src/features/display/curio/net.js";
import BD from "../src/features/display/curio/data-badminton.js";
import { HOLES, roundOf, parabola, golfSteps, golfAt, holeInfo } from "../src/features/display/curio/golf.js";
import { TBL, CUSH, reflect, cueShot, pathOf, cueSteps, cueSummary, cueAt, CUE_D } from "../src/features/display/curio/cue.js";
import { bowlGame, bowlAt, bowlSteps, frameCalc, entryOf, ALL, BT } from "../src/features/display/curio/bowl.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
let n = 0, failed = 0;
async function test(name, fn) {
  n++;
  try { await fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}
const BAD = /NaN|undefined|Infinity|\[object Object\]/;
const RU = { tabletennis: [3, () => [11, 0]], volleyball: [3, (i) => (i < 4 ? [25, 0] : [15, 0])], jokgu: [2, () => [15, 19]], sepak: [2, (i) => (i < 2 ? [21, 25] : [15, 17])], badminton: [2, () => [21, 30]] };

/* ══════════ 네트 운동 ══════════ */
await test("네트 운동 가상 경기(탁구 · 배구 · 족구 · 세팍 × 씨앗 6): 이긴 쪽 +1 · 세트 끝 규칙 · 최종 세트 · 공 자리가 그림 안", () => {
  for (const sport of ["tabletennis", "volleyball", "jokgu", "sepak"]) for (let seed = 1; seed <= 6; seed++) {
    const M = genMatch(sport, seed), [win, setRule] = RU[sport], V = NETS[sport].view;
    assert.ok(M.rallies.length > 20, `${sport} ${seed}: 랠리 ${M.rallies.length}`);
    for (const r of M.rallies) {
      assert.ok(r.win === 0 || r.win === 1);
      assert.ok(r.shots.length >= 1);
      for (const s of r.shots) for (const q of [s.a, s.b]) assert.ok(Math.abs(q[0]) <= V[0] && Math.abs(q[1]) <= V[1], `${sport} ${seed}: 그림 밖 ${q}`);
      const { pre, post } = r.sc;
      if (post.sets.length === pre.sets.length) {
        assert.equal(post.cur[r.win], pre.cur[r.win] + 1, `${sport} ${seed}: 이긴 쪽 +1`);
        assert.equal(post.cur[1 - r.win], pre.cur[1 - r.win]);
        const [to, cap] = setRule(pre.sets.length);
        assert.ok(!setDone(post.cur[0], post.cur[1], to, cap), `${sport}: 끝났어야 할 세트가 이어짐`);
      } else {
        const last = post.sets[post.sets.length - 1], exp = pre.cur.slice(); exp[r.win]++;
        assert.deepEqual(last, exp, `${sport} ${seed}: 끝난 세트 점수`);
        const [to, cap] = setRule(pre.sets.length);
        assert.ok(setDone(last[0], last[1], to, cap), `${sport} ${seed}: 세트 끝 규칙 ${last}`);
        assert.deepEqual(post.cur, [0, 0]);
      }
      const k = keyShot(r.shots), ks = r.shots[k];
      assert.ok(k >= 0 && k < r.shots.length);
      assert.ok(ks.r === "net" || crosses(ks) || k === r.shots.length - 1);
    }
    const wins = [0, 1].map((t) => M.final.filter((s) => (t ? s[1] > s[0] : s[0] > s[1])).length);
    assert.equal(Math.max(...wins), win, `${sport} ${seed}: 이긴 세트 수 ${wins}`);
  }
});
await test("테니스 가상 경기: 끝난 세트는 6게임 2게임 차 또는 7 : 5 · 7 : 6, 게임 점수 글자", () => {
  for (let seed = 1; seed <= 6; seed++) {
    const M = genMatch("tennis", seed);
    for (const s of M.final) {
      const [a, b] = [Math.max(...s), Math.min(...s)];
      assert.ok((a === 6 && b <= 4) || (a === 7 && (b === 5 || b === 6)), `세트 ${s}`);
    }
    assert.equal(Math.max(M.final.filter((s) => s[0] > s[1]).length, M.final.filter((s) => s[1] > s[0]).length), 2);
  }
  assert.deepEqual(tennisPts([2, 1]), ["30", "15"]);
  assert.deepEqual(tennisPts([3, 3]), ["듀스", "듀스"]);
  assert.deepEqual(tennisPts([4, 3]), ["AD", ""]);
  assert.deepEqual(tennisPts([5, 3], true), ["5", "3"]);
});
await test("배드민턴 실제 경기(ShuttleSet 결승 여섯): 세트 점수 = 기록 · 랠리마다 이긴 쪽 +1 · 이긴 선수가 왼쪽", () => {
  const L = badmintonMatches(BD);
  assert.equal(L.length, 6);
  L.forEach((m, mi) => {
    assert.deepEqual(m.final, BD.matches[mi].sets, `${mi}: 세트 점수`);
    // 실제 경기에서 고른 랠리들(세트마다 일부) — 점수는 세트 안에서 늘기만 하고 그 세트 최종 점수를 넘지 않는다
    m.rallies.forEach((r, j) => {
      const { pre, post } = r.sc, fin = m.final[r.set - 1];
      assert.equal(post.cur[r.win] - pre.cur[r.win], 1, `${mi}: 랠리 ${j} 이긴 쪽 +1`);
      assert.equal(post.cur[1 - r.win], pre.cur[1 - r.win]);
      assert.deepEqual(pre.sets, m.final.slice(0, r.set - 1));
      assert.ok(post.cur[0] <= fin[0] && post.cur[1] <= fin[1], `${mi}: ${r.set}세트 점수 ${post.cur} > ${fin}`);
      const prev = m.rallies[j - 1];
      if (prev && prev.set === r.set) assert.ok(pre.cur[0] >= prev.sc.post.cur[0] && pre.cur[1] >= prev.sc.post.cur[1], `${mi}: 점수가 줄어듦`);
      if (prev) assert.ok(r.set >= prev.set);
    });
    assert.equal(new Set(m.rallies.map((r) => r.set)).size, m.final.length);
    for (const fin of m.final) assert.ok(setDone(fin[0], fin[1], 21, 30), `최종 세트 ${fin}`);
    assert.ok(m.final.filter((s) => s[0] > s[1]).length === 2, `${mi}: 왼쪽(이긴 선수)이 두 세트`);
  });
});
await test("네트를 지난 자리 = y절편(유리수로 다시) · 초등 칸 셈이 같은 자리 · 판서에 같은 수", () => {
  let cnt = 0;
  const all = [...badmintonMatches(BD), ...["tennis", "tabletennis", "volleyball", "jokgu", "sepak"].map((s) => genMatch(s, 2))];
  for (const M of all) {
    const V = NETS[M.sport].view;
    for (const r of M.rallies) for (const s of r.shots) {
      if (!(crosses(s) || s.r === "net")) continue;
      const L = lineOf(s.a, s.b);
      if (L.kind !== "f" && L.kind !== "h") continue;
      const y = netY(s.a, s.b);
      if (y == null) continue;                    // 네트 앞에 떨어진 공(실제 기록) — 그림에 네트 점을 찍지 않는다
      cnt++;
      assert.ok(Math.abs(y - L.b[0] / L.b[1]) < 1e-9, `netY ${s.a} ${s.b}`);
      // 정확한 유리수: b = (a_y b_x − b_y a_x) / (b_x − a_x)
      const bx = frac(s.a[1] * s.b[0] - s.b[1] * s.a[0], s.b[0] - s.a[0]);
      assert.ok(L.b[0] === bx[0] && L.b[1] === bx[1], `y절편 ${L.b} / ${bx}`);
      const m = netSteps(s, "m", V).lines.map((q) => q.s).join("\n");
      assert.ok(m.includes(`(0, ${fsx(bx[0], bx[1])})`), `판서(중등): ${m}`);
      if (s.r !== "net" && s.b[0] !== s.a[0]) {
        const e = netSteps(s, "e", V).lines.map((q) => q.s).join("\n");
        const ye = frac(bx[0] + V[1] * bx[1], bx[1]);
        assert.ok(e.includes(`아래에서 ${fsx(ye[0], ye[1])}칸`), `판서(초등): ${e} / ${ye}`);
      }
      for (const L2 of netSteps(s, "m", V).lines) assert.ok(!BAD.test(L2.s));
    }
  }
  assert.ok(cnt > 1500, `${cnt}`);
});
await test("네트 운동 시간표: 경과 → 랠리가 앞으로만, 바퀴가 돌아도 같은 장면", () => {
  const L = badmintonMatches(BD), S = scheduleOf(L, "some");
  let last = -1;
  for (let e = 0; e < S.total; e += 7919) { const a = rallyAt(S, e); assert.ok(a.idx >= last); last = a.idx; }
  const a1 = rallyAt(S, 123456), a2 = rallyAt(S, 123456 + S.total);
  assert.equal(a1.idx, a2.idx); assert.equal(a1.t, a2.t); assert.equal(a2.k, 1);
});

/* ══════════ 골프 ══════════ */
await test("골프 가상 라운드(씨앗 120): 마지막 샷은 홀컵 · 타수 = 샷 + 벌타 · 합계 · 파 36", () => {
  assert.equal(HOLES.reduce((s, h) => s + h.par, 0), 36);
  for (let seed = 1; seed <= 120; seed++) {
    const R = roundOf(seed);
    let tot = 0;
    for (const h of R.holes) {
      const last = h.shots.at(-1);
      assert.ok(last.kind === "putt" && last.made, `${seed}: 홀 ${h.i + 1} 마지막 샷`);
      const strokes = h.shots.length + h.shots.filter((s) => s.pen).length;
      assert.equal(h.strokes, strokes);
      tot += h.strokes - h.par;
      assert.equal(h.total, tot);
      for (const s of h.shots) {
        if (s.kind !== "putt") { assert.ok(s.carry > 0 && s.carry % 2 === 0, `날아간 거리 ${s.carry}`); assert.ok(s.apex > 0); }
        for (const L of golfSteps(s, "m").concat(golfSteps(s, "e"))) assert.ok(!BAD.test(L.s), L.s);
      }
    }
  }
});
await test("골프 포물선: y = a(x − p)² + q 가 (0, 0) · (날아간 거리, 0) 을 지나고 꼭짓점이 (p, q)", () => {
  for (const [c, h] of [[238, 32], [222, 30], [6, 6], [12, 3], [154, 30], [86, 25]]) {
    const { p, q, a } = parabola(c, h);
    assert.equal(p * 2, c); assert.equal(q, h);
    // a·p² + q = 0 (유리수)
    assert.equal(a[0] * p * p + q * a[1], 0);
    const m = golfSteps({ kind: "full", carry: c, apex: h, d0: 300, d1: 100 }, "m").map((L) => L.s).join("\n");
    assert.ok(m.includes(`y = ${fsx(a[0], a[1])}(x − ${p})² + ${q}`), m);
  }
  const at = golfAt(1, 3600 * 1000);
  assert.ok(at.round && at.T && at.t >= 0);
});

/* ══════════ 당구 ══════════ */
await test("당구 빈쿠션(씨앗 3 × 300): 꺾이는 점은 쿠션 위 · 반사 · H 는 직선 CR′ 위 · 노란 공이 CR 을 막음 · 쿠션 한 번은 H 가 정수 칸", () => {
  let one = 0, two = 0;
  const segD = (p, a, b) => { const vx = b[0] - a[0], vy = b[1] - a[1], L = vx * vx + vy * vy; const t = Math.max(0, Math.min(1, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L)); return Math.hypot(p[0] - a[0] - vx * t, p[1] - a[1] - vy * t); };
  for (let seed = 1; seed <= 3; seed++) for (let k = 0; k < 300; k++) {
    const s = cueShot(seed, k);
    s.two ? two++ : one++;
    const P = pathOf(s);
    for (const q of P) assert.ok(q[0] >= -1e-9 && q[0] <= TBL.w + 1e-9 && q[1] >= -1e-9 && q[1] <= TBL.h + 1e-9);
    s.cush.forEach((c, i) => {
      const H = P[i + 1], a = P[i], b = P[i + 2];
      assert.ok(Math.abs((CUSH[c].axis === "y" ? H[1] : H[0]) - CUSH[c].v) < 1e-9, "쿠션 위");
      const ar = reflect(a, c);
      assert.ok(Math.abs((H[0] - ar[0]) * (b[1] - ar[1]) - (H[1] - ar[1]) * (b[0] - ar[0])) < 1e-6, "반사");
    });
    // H(분수)가 직선 C → R′(R″) 위: (H − C) × (img − C) = 0 (유리수)
    const hf = s.hf[0], [hx, hy] = [hf[0], hf[1]];
    const cross = (hx[0] - s.C[0] * hx[1]) * hy[1] * (s.img[1] - s.C[1]) - (hy[0] - s.C[1] * hy[1]) * hx[1] * (s.img[0] - s.C[0]);
    assert.equal(cross, 0, "H 가 직선 위");
    if (!s.two) { const along = CUSH[s.cush[0]].axis === "y" ? hx : hy; assert.equal(along[1], 1, "H 정수 칸"); }
    assert.ok(segD(s.Y, s.C, s.R) < 0.1, "노란 공이 막음");
    for (let i = 1; i < P.length; i++) assert.ok(segD(s.Y, P[i - 1], P[i]) >= 1.05, "노란 공이 길에서 떨어짐");
    for (const mode of ["m", "e"]) {
      const L = cueSteps(s, mode);
      for (const q of L) assert.ok(!BAD.test(q.s), q.s);
      assert.ok(!BAD.test(cueSummary(s, mode, 0) + cueSummary(s, mode, 1) + cueSummary(s, mode, 2)));
    }
    const m = cueSteps(s, "m").map((q) => q.s).join("\n");
    assert.ok(m.includes(`(${fsx(hx[0], hx[1])}, ${fsx(hy[0], hy[1])})`), m);
  }
  assert.ok(one > 500 && two > 120, `${one} ${two}`);
  const at = cueAt(1, CUE_D * 5 + 100);
  assert.equal(at.k, 5); assert.equal(at.t, 100);
});

/* ══════════ 볼링 ══════════ */
/** 점수를 따로 다시 센다(투구마다 쓰러진 핀 수 목록 → 프레임 누계) */
function score(pins) {
  const out = []; let i = 0, tot = 0;
  for (let f = 0; f < 10; f++) {
    if (f === 9) { tot += pins.slice(i).reduce((a, v) => a + v, 0); out.push(tot); break; }
    if (pins[i] === 10) { tot += 10 + pins[i + 1] + pins[i + 2]; i += 1; }
    else if (pins[i] + pins[i + 1] === 10) { tot += 10 + pins[i + 2]; i += 2; }
    else { tot += pins[i] + pins[i + 1]; i += 2; }
    out.push(tot);
  }
  return out;
}
await test("볼링 가상 게임(씨앗 400): 점수 다시 셈 · 표시(X / −) · 10프레임 투구 수 · 핀은 서 있던 것만 · 4c − 3b", () => {
  let strikes = 0, frames = 0;
  for (let seed = 1; seed <= 400; seed++) {
    const g = bowlGame(seed);
    assert.equal(g.frames.length, 10);
    const pins = g.rolls.map((o) => o.n);
    assert.deepEqual(g.frames.map((F) => F.total), score(pins), `${seed}: 점수`);
    assert.equal(g.total, g.frames[9].total);
    assert.ok(g.total >= 0 && g.total <= 300);
    for (const o of g.rolls) {
      assert.equal(o.entry, entryOf(o.b, o.c));
      assert.equal(o.entry, 4 * o.c - 3 * o.b);
      const dn = o.down.map((d) => d.n);
      assert.equal(new Set(dn).size, dn.length);
      for (const p of dn) assert.ok(o.before.includes(p), "서 있던 핀만");
      assert.deepEqual(o.after, o.before.filter((p) => !dn.includes(p)));
      if (o.mark === "X") assert.ok(o.before.length === 10 && o.n === 10);
      if (o.mark === "/") assert.ok(o.before.length < 10 && o.after.length === 0);
      for (const mode of ["m", "e"]) for (const L of bowlSteps(o, mode)) assert.ok(!BAD.test(L.s), L.s);
    }
    const F10 = g.frames[9], r10 = F10.rolls.map((j) => g.rolls[j]);
    const bonus = r10[0].n === 10 || r10[0].n + r10[1].n === 10;
    assert.equal(r10.length, bonus ? 3 : 2, `${seed}: 10프레임 투구 수`);
    g.frames.forEach((F, f) => { frames++; if (F.kind === "strike") strikes++; assert.ok(!BAD.test(frameCalc(g, f))); });
  }
  const rate = strikes / frames;
  assert.ok(rate > 0.25 && rate < 0.65, `스트라이크 비율 ${rate}`);
});
await test("볼링 시간표: 게임이 끝나면 다음 게임, 투구 번호가 앞으로만", () => {
  let last = { k: 0, i: -1 };
  for (let e = 0; e < 3 * 200000; e += 3001) {
    const a = bowlAt(1, e);
    assert.ok(a.k > last.k || (a.k === last.k && a.i >= last.i), `${e}`);
    assert.ok(a.i <= a.g.rolls.length && a.t >= 0);
    last = a;
  }
  assert.ok(last.k >= 2);
});

/* ══════════ 그리기 ══════════ */
await test("그리기: 새 액자(네트 여섯 · 골프 · 당구 · 볼링)를 상세 · 최소화 × 초등 · 중등 × 두 테마로, 기존 일곱은 최소화로 — 오류 · NaN 없음", async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "curio2-"));
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { NetArt } from ${F("frames/netfn.jsx")};
import { GolfArt } from ${F("frames/golffn.jsx")};
import { CueArt } from ${F("frames/cuefn.jsx")};
import { BowlArt } from ${F("frames/bowlfn.jsx")};
import { SoccerArt } from ${F("frames/soccerfn.jsx")};
import { HoopArt } from ${F("frames/hoopfn.jsx")};
import { BatArt } from ${F("frames/batfn.jsx")};
import { PouchArt } from ${F("frames/pouch.jsx")};
import { LexiArt } from ${F("frames/lexi.jsx")};
import { LineupArt } from ${F("frames/lineup.jsx")};
import { CrowdArt, crowdAt } from ${F("frames/crowd.jsx")};
import { genMatch, badmintonMatches, scheduleOf, rallyAt } from ${F("curio/net.js")};
import { golfAt } from ${F("curio/golf.js")};
import { cueAt, CUE_D } from ${F("curio/cue.js")};
import { bowlGame, BT } from ${F("curio/bowl.js")};
import { fixPouch, pouchAt } from ${F("curio/pouch.js")};
import { fixLexi, lexiAt } from ${F("curio/lexi.js")};
import { fixLine, lineAt } from ${F("curio/lineup.js")};
import { fixCrowd } from ${F("curio/crowd.js")};
import BD from ${F("curio/data-badminton.js")};
import SOCCER from ${F("curio/data-soccer.js")};
import NBA from ${F("curio/data-nba.js")};
import MLB from ${F("curio/data-mlb.js")};
import { DICT, SEEDS } from ${F("curio/data-dict.js")};
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
const LISTS = {};
const listOf = (sport) => LISTS[sport] || (LISTS[sport] = sport === "badminton" ? badmintonMatches(BD) : [genMatch(sport, 1), genMatch(sport, 1001)]);
export function sweep(mode, th, ex) {
  const C = PALETTE[th], out = [];
  for (const sport of ["badminton", "tennis", "tabletennis", "volleyball", "jokgu", "sepak"]) {
    const L = listOf(sport), S = scheduleOf(L, "all");
    for (const j of [0, 3, 11, 40, S.items.length - 1]) {
      const it = S.items[Math.min(j, S.items.length - 1)];
      for (const dt of [200, it.T.shotsAt[Math.min(1, it.T.shotsAt.length - 1)] + 300, it.T.endAt + 400, it.T.replayAt + 2500, it.T.replayAt + 7000, it.T.dur - 100]) {
        const a = rallyAt(S, it.at + dt);
        out.push(svg(<NetArt C={C} mode={mode} sport={sport} ex={ex} matches={L} at={{ ...a, n: S.items.length }} credit="시험" />));
      }
    }
  }
  for (const seed of [1, 2, 7]) for (const e of [0, 2600, 9000, 21000, 60000, 140000, 400000]) out.push(svg(<GolfArt C={C} mode={mode} ex={ex} at={golfAt(seed, e)} />));
  for (const k of [0, 1, 2, 3, 4, 9, 17]) for (const t of [100, 1500, 3500, 5000, 6900, 9000, 12000, 16900]) { const a = cueAt(1, k * CUE_D); out.push(svg(<CueArt C={C} mode={mode} ex={ex} at={{ ...a, t }} />)); }
  for (const seed of [1, 4]) { const g = bowlGame(seed); for (const i of [0, 1, 5, 9, g.rolls.length - 1, g.rolls.length]) for (const t of [100, 1800, BT.fall[0] + 500, BT.math + 1500, 7700]) out.push(svg(<BowlArt C={C} mode={mode} ex={ex} at={{ g, k: 0, i, t }} />)); }
  if (ex === "mini") {
    for (const [i, t] of [[0, 0], [37, 500], [120, 3500], [250, 5200], [402, 9600]]) out.push(svg(<SoccerArt C={C} mode={mode} P={{ match: -1, kind: "all", sp: 1 }} data={SOCCER} at={{ i, k: i, t }} ex="mini" />));
    for (const [i, t] of [[0, 300], [45, 1800], [46, 5200], [600, 4200]]) out.push(svg(<HoopArt C={C} mode={mode} P={{ game: -1, who: "all", sp: 1 }} data={NBA} at={{ i, k: i, t }} ex="mini" />));
    for (const [i, t] of [[0, 300], [12, 2000], [60, 4300], [150, 5100], [210, 8800]]) out.push(svg(<BatArt C={C} mode={mode} P={{ game: -1, sp: 1 }} data={MLB} at={{ i, k: i, t }} ex="mini" />));
    { const P = fixPouch({ n: 24, k: 2, b: 3, c: 4, seed: 2 }); for (const e of [0, 4000, 9000, 40000]) out.push(svg(<PouchArt C={C} mode={mode} P={P} at={pouchAt(P, e)} ex="mini" />)); }
    { const P = fixLexi({ src: "abc", n: 6, r: 3 }); for (const e of [0, 5000, 60000]) out.push(svg(<LexiArt C={C} mode={mode} P={P} at={lexiAt(P, e, { DICT, SEEDS })} D={{ DICT, SEEDS }} ex="mini" />)); }
    for (const cfg of [{ n: 5, k: 2 }, { n: 8, k: 3, e: 2 }, { n: 3 }]) { const P = fixLine(cfg); for (const e of [0, 12000, 400000]) out.push(svg(<LineupArt C={C} mode={mode} P={P} at={lineAt(P, e)} ex="mini" />)); }
    { const P = fixCrowd({ seed: 5 }); for (const e of [0, 3000, 5000, 7900]) out.push(svg(<CrowdArt C={C} mode={mode} P={P} at={crowdAt(P, e)} ex="mini" />)); }
  }
  return out;
}
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const bad = (s) => (s.match(/.{60}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];
  let cnt = 0;
  for (const ex of ["full", "mini"]) for (const mode of ["e", "m"]) for (const th of ["dark", "light"]) {
    for (const s of m.sweep(mode, th, ex)) { assert.ok(s.length > 1500 && !BAD.test(s), `${ex}/${mode}/${th}: ${bad(s)}`); cnt++; }
  }
  assert.ok(cnt > 2000, `${cnt}`);
});

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
