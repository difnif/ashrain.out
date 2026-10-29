// node tests/display-labs.test.mjs — 교실 모니터 실험 액자(몬티홀 · 갈림길과 구슬 · 구슬 낙하 실험) 검산. 실패 시 exit 1.
// 몬티홀: 이론값을 모든 경우(자동차 · 고른 문 · 사회자가 여는 문들 · 바꿀 문)를 늘어놓아 센 값과 맞춘다. 판 고르기 · 시간표 · 기록.
// 갈림길과 구슬: 주머니 + 깔때기 물리 판에서 잃어버린 구슬 없음 · 시범 판이 정해 둔 시간 안에 끝남 · 하나씩은 이론과 가깝고
//               한꺼번에(1단계 · 2개)는 같은 구멍이 거의 없다.
// 그리기: 세 액자를 여러 설정 · 여러 순간 · 두 판 · 두 테마로 그려 오류 · NaN 이 없는지 훑는다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  MLAB, KS, fixPrm, theory, val, red, luck, hostOpens, restOf, playRound, shares, PACE, phases, autoAt, cycleRuns, remapAuto,
  handDur, cycleLen,
} from "../src/features/display/montylab.js";
import {
  BLAB, STAGE, OPEN, labLayout, labWalls, labTrial, labRuns, freqOf, catsOf, verdictOf, labTimeline, labAt, dropSec, demoSeed,
} from "../src/features/display/branchlab.js";
import { shapeProbs } from "../src/features/display/branch.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}
const close = (a, b, eps = 1e-9) => Math.abs(a - b) <= eps;

/* ══════════ 몬티홀 ══════════ */
/** k개 고르기(모든 조합) */
function combos(arr, k) {
  const out = [];
  const rec = (s, cur) => { if (cur.length === k) { out.push(cur.slice()); return; } for (let i = s; i < arr.length; i++) { cur.push(arr[i]); rec(i + 1, cur); cur.pop(); } };
  rec(0, []);
  return out;
}
/** 모든 경우를 늘어놓아: 판이 성립할 확률 · 그대로 / 바꾸기 이길 확률(성립한 판 가운데) */
function enumerate(n, k, know) {
  let ok = 0, stay = 0, sw = 0;
  for (let car = 0; car < n; car++) for (let pick = 0; pick < n; pick++) {
    const pBase = (1 / n) * (1 / n);
    const allowed = []; for (let d = 0; d < n; d++) if (d !== pick && (!know || d !== car)) allowed.push(d);
    const sets = combos(allowed, k);
    for (const S of sets) {
      const p = pBase / sets.length;
      if (!know && S.includes(car)) continue;            // 모르는 사회자가 자동차를 열었다 → 세지 않는다
      ok += p;
      if (pick === car) stay += p;
      const rest = []; for (let d = 0; d < n; d++) if (d !== pick && !S.includes(d)) rest.push(d);
      for (const d of rest) if (d === car) sw += p / rest.length;
    }
  }
  return { ok, stay: stay / ok, sw: sw / ok };
}

test("몬티홀 이론값 = 모든 경우를 늘어놓아 센 값 (문 3~10 · 여는 문 0~n−2 · 사회자가 안다/모른다)", () => {
  for (const n of MLAB.NS) for (const k of KS(n)) for (const know of [true, false]) {
    const T = theory(n, k, know), E = enumerate(n, k, know), tag = `n${n} k${k} ${know ? "안다" : "모른다"}`;
    assert.ok(close(E.stay, val(T.stay)), `${tag} 그대로 ${E.stay} ≠ ${val(T.stay)}`);
    assert.ok(close(E.sw, val(T.sw)), `${tag} 바꾸기 ${E.sw} ≠ ${val(T.sw)}`);
    assert.ok(close(E.ok, val(T.ok)), `${tag} 성립 ${E.ok} ≠ ${val(T.ok)}`);
    // 몫: 내 문 + 남은 닫힌 문 모두 = 1, 하나에 = 모두 ÷ 남은 문 수
    assert.ok(close(val(T.pick) + val(T.rest), 1), tag);
    assert.ok(close(val(T.each) * (n - 1 - k), val(T.rest)), tag);
  }
  // 대표값: 문 3 · 1개 → {1/3} · {2/3}, 문 10 · 8개 → {9/10}, 모르면 반반
  assert.deepEqual(theory(3, 1, true).sw, [2, 3]); assert.deepEqual(theory(10, 8, true).sw, [9, 10]);
  assert.deepEqual(theory(3, 1, false).sw, [1, 2]); assert.deepEqual(theory(5, 1, true).sw, [4, 15]);
  assert.deepEqual(red(6, 8), [3, 4]);
});

test("몬티홀 판 하나: 사회자는 고른 문을 열지 않고 k개를 연다(알면 자동차도 피한다) · 같은 씨앗이면 같은 판", () => {
  for (const n of [3, 5, 10]) for (const k of KS(n)) for (const know of [true, false]) for (let r = 0; r < 60; r++) {
    const L = luck(777, r, n);
    for (const pick of [0, n - 1, L.autoPick]) {
      const op = hostOpens(L, n, k, know, pick);
      assert.equal(op.length, k);
      assert.ok(!op.includes(pick));
      if (know) assert.ok(!op.includes(L.car));
      assert.deepEqual(op, [...op].sort((a, b) => a - b));
      assert.equal(restOf(n, pick, op).length, n - 1 - k);
    }
    assert.deepEqual(playRound(777, r, n, k, know), playRound(777, r, n, k, know));
  }
});

test("몬티홀 문마다의 몫: 고른 뒤 모두 1/n → 연 뒤 열린 문 0 · 내 문 · 닫힌 다른 문, 합 1", () => {
  for (const n of [3, 6, 10]) for (const k of KS(n)) for (const know of [true, false]) {
    const opened = Array.from({ length: k }, (_, i) => i + 1), pick = 0, T = theory(n, k, know);
    const b = shares(n, k, know, pick, opened, "before"), a = shares(n, k, know, pick, opened, "after");
    assert.ok(close(b.reduce((x, y) => x + y, 0), 1)); assert.ok(close(a.reduce((x, y) => x + y, 0), 1), `n${n} k${k}`);
    for (const d of opened) assert.equal(a[d], 0);
    assert.ok(close(a[pick], val(T.pick)));
  }
});

test("몬티홀 저절로 3000판(문 3 · 1개 · 안다): 바꾸기 ≈ {2/3} · 그대로 ≈ {1/3}, 모르면 세지 않는 판 ≈ {1/3} · 둘 다 ≈ {1/2}", () => {
  const run = (n, k, know, N = 3000) => {
    let s = 0, w = 0, v = 0;
    for (let r = 0; r < N; r++) { const R = playRound(4242, r, n, k, know); if (R.void) v++; if (R.stayWin) s++; if (R.swWin) w++; }
    return { stay: s / (N - v), sw: w / (N - v), voids: v / N };
  };
  const A = run(3, 1, true); assert.ok(Math.abs(A.sw - 2 / 3) < 0.03 && Math.abs(A.stay - 1 / 3) < 0.03, JSON.stringify(A));
  const B = run(3, 1, false); assert.ok(Math.abs(B.voids - 1 / 3) < 0.03 && Math.abs(B.sw - 0.5) < 0.04 && Math.abs(B.stay - 0.5) < 0.04, JSON.stringify(B));
  const Cc = run(10, 8, true); assert.ok(Math.abs(Cc.sw - 0.9) < 0.02, JSON.stringify(Cc));
});

test("몬티홀 시간표: 구간이 이어지고 판 길이가 같다 · 기록은 결과가 열릴 때 더한다 · 한 바퀴 정리 = 판마다 센 합", () => {
  for (const speed of ["natural", "fast"]) for (const k of [0, 1, 3]) {
    const PH = phases(k, speed);
    let a = 0;
    for (const [, s, e] of PH.list) { assert.equal(s, a); assert.ok(e > s); a = e; }
    assert.equal(a, PH.dur);
    assert.equal(PH.list.some(([nm]) => nm === "flow"), k > 0);
  }
  const P = fixPrm({ n: 4, k: 1, know: false, play: "auto", speed: "natural" });
  const D = phases(P.k, P.speed).dur, G = MLAB.GAMES.natural, runs = cycleRuns(P.n, P.k, P.know, 0, G);
  for (let r = 0; r < 6; r++) {
    const R = runs.rounds[r], before = autoAt(P, r * D + 10), last = autoAt(P, (r + 1) * D - 10);
    assert.equal(before.phase, "pick"); assert.equal(before.tally.rounds, r);
    assert.equal(last.tally.rounds, r + 1);
    assert.equal(last.phase, R.void ? "void" : "done");
  }
  const S = autoAt(P, G * D + 100);
  assert.equal(S.phase, "sum");
  let s = 0, w = 0, v = 0;
  for (const R of runs.rounds) { s += R.stayWin; w += R.swWin; v += R.void; }
  assert.deepEqual([S.tally.stayW, S.tally.swW, S.tally.voids, S.tally.stayN], [s, w, v, G - v]);
  assert.equal(autoAt(P, cycleLen(P) + 10).c, 1);
  // 빠르기를 바꾸면 같은 바퀴 · 같은 판 · 같은 진행 비율
  const Pf = { ...P, speed: "fast" }, e = 7 * D + D * 0.4, e2 = remapAuto(P, Pf, e);
  const Df = phases(P.k, "fast").dur;
  assert.equal(Math.floor(e2 / Df), 7); assert.ok(close((e2 - 7 * Df) / Df, 0.4, 1e-9));
  const back = remapAuto(Pf, P, 250 * Df);                 // 빠르게 250판째 → 자연스럽게(30판)면 정리부터
  assert.equal(autoAt(P, back).phase, "sum");
});

test("몬티홀 설정 고치기 · 직접 하기 구간 길이", () => {
  assert.deepEqual(fixPrm({}), { n: 3, k: 1, know: true, play: "hand", speed: "natural" });
  assert.deepEqual(fixPrm({ n: 99, k: 5 }), { n: 3, k: 1, know: true, play: "hand", speed: "natural" });
  assert.equal(fixPrm({ n: 10, k: -1 }).k, 0); assert.equal(fixPrm({ n: 4, k: 9 }).k, 2);
  assert.equal(fixPrm({ know: false }).know, false); assert.equal(fixPrm({ play: "auto", speed: "fast" }).speed, "fast");
  assert.equal(handDur("pick", 1), Infinity); assert.equal(handDur("decide", 1), Infinity);
  for (const ph of ["open", "flow", "reveal", "done", "void"]) assert.ok(handDur(ph, 2) > 0 && Number.isFinite(handDur(ph, 2)), ph);
  assert.ok(PACE.natural.doneHand > PACE.natural.done);
});

/* ══════════ 갈림길과 구슬 ══════════ */
test("갈림길과 구슬 배치: 주머니 속 자리가 깔때기 입 위 · 서로 겹치지 않음 · 벽 좌우 대칭", () => {
  for (const nn of BLAB.NS) for (const m of BLAB.MS) {
    const L = labLayout(nn, m);
    assert.equal(L.slots.length, m);
    for (const [x, y] of L.slots) { assert.ok(y < L.yMouth, `n${nn} m${m}`); assert.ok(Math.abs(x) + L.r < L.fw); assert.ok(y > L.bag.neck && y < L.bag.bottom); }
    for (let i = 0; i < m; i++) for (let j = i + 1; j < m; j++) {
      const d = Math.hypot(L.slots[i][0] - L.slots[j][0], L.slots[i][1] - L.slots[j][1]);
      assert.ok(d >= 2 * L.r - 0.5, `겹침 n${nn} m${m} ${i}-${j} ${d}`);
    }
    assert.ok(L.yMouth < L.yG && L.yG < L.yb && L.spout[1] < L.yMouth);
    const W = labWalls(L), key = (pts) => pts.map(([x, y]) => `${Math.round(x * 10)}:${Math.round(y * 10)}`).join("|");
    const set = new Set(W.map((w) => key(w.pts)));
    for (const w of W) assert.ok(set.has(key(w.pts.map(([x, y]) => [-x, y]))) || set.has(key([...w.pts].reverse().map(([x, y]) => [-x, y]))), `대칭 n${nn} m${m}`);
  }
});

test("갈림길과 구슬 시범 판(바퀴 0~4): 잃어버린 구슬 없음 · 모두 칸에 · 정해 둔 떨어뜨리기 시간 안에 끝남", () => {
  for (const nn of BLAB.NS) for (const m of BLAB.MS) for (const mode of ["seq", "sim"]) for (let c = 0; c < 5; c++) {
    const o = labTrial(nn, m, mode, demoSeed(c, mode));
    assert.equal(o.lost, 0, `n${nn} m${m} ${mode} c${c}`);
    assert.equal(o.counts.reduce((a, b) => a + b, 0), m);
    assert.ok(o.end <= dropSec(nn, m, mode) + STAGE.hold / 1000 - 0.6, `n${nn} m${m} ${mode} c${c}: ${o.end.toFixed(2)}s`);
  }
});

test("갈림길과 구슬 300판씩: 하나씩은 이론과 5%p 안 · 1단계 2개를 한꺼번에 굴리면 같은 구멍이 거의 없다(판정: 크게 줄어요)", () => {
  for (const [nn, m] of [[1, 2], [2, 4], [3, 3], [4, 6]]) {
    const f = freqOf(labRuns(nn, m, "seq", BLAB.TRIALS), BLAB.TRIALS);
    for (const c of catsOf(nn, m)) {
      const v = c.keys.reduce((a, k) => a + f(k), 0);
      assert.ok(Math.abs(v - c.p) <= 0.05, `n${nn} m${m} ${c.key}: ${v} vs ${c.p}`);
    }
  }
  const fm = freqOf(labRuns(1, 2, "sim", BLAB.TRIALS), BLAB.TRIALS);
  assert.ok(fm("2-0") < 0.1, `같은 구멍 ${fm("2-0")}`);
  const V = verdictOf(1, 2);
  assert.equal(V.best.key, "2-0"); assert.equal(V.tier, 2); assert.equal(V.up, false);
});

test("갈림길과 구슬 비교 칸: 확률의 합 1 · 7칸 이하(많으면 「그 밖」으로 묶음) · 시간표 차례 · 바퀴 넘김", () => {
  for (const nn of BLAB.NS) for (const m of BLAB.MS) {
    const cats = catsOf(nn, m);
    assert.ok(cats.length <= 7);
    assert.ok(close(cats.reduce((a, c) => a + c.p, 0), 1, 1e-12), `n${nn} m${m}`);
    assert.equal(cats.reduce((a, c) => a + c.keys.length, 0), shapeProbs(nn, m).length);
    const TL = labTimeline(nn, m);
    assert.deepEqual(TL.list, ["prepA", "dropA", "prepB", "dropB", "tally", "verdict"]);
    let a = 0;
    for (const nm of TL.list) { assert.equal(TL.a[nm], a); a = TL.b[nm]; }
    assert.equal(a, TL.dur);
    assert.ok(TL.b.dropA - TL.a.dropA >= STAGE.lead + dropSec(nn, m, "seq") * 1000);
    assert.equal(labAt(nn, m, TL.a.dropB + 5).stage, "dropB");
    const nx = labAt(nn, m, TL.dur * 3 + 10);
    assert.equal(nx.c, 3); assert.equal(nx.stage, "prepA");
  }
  assert.equal(OPEN > 0, true);
});

/* ══════════ 그리기 훑기(번들) ══════════ */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-labs-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { FRAMES } from ${F("frames/index.js")};
import { EXPLAIN } from ${F("stories.js")};
import { MontyArt, MontyThumb, autoVm } from ${F("frames/monty.jsx")};
import { BranchArt, BranchThumb } from ${F("frames/branchlab.jsx")};
import { GaltonArt, GaltonThumb, glTimeline, glAt, glLayout } from ${F("frames/galtonlab.jsx")};
import { autoAt, fixPrm } from ${F("montylab.js")};
import { labAt } from ${F("branchlab.js")};
export { FRAMES, EXPLAIN, autoVm, autoAt, fixPrm, glTimeline, glAt, glLayout, labAt };
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const monty = (P, vm, mode, th) => svg(<MontyArt C={PALETTE[th]} mode={mode} P={P} vm={vm} />);
export const branch = (P, at, mode, th) => svg(<BranchArt C={PALETTE[th]} mode={mode} P={P} at={at} />);
export const galton = (P, at, mode, th) => svg(<GaltonArt C={PALETTE[th]} mode={mode} P={P} at={at} />);
export const thumbs = (mode, th) => [MontyThumb, BranchThumb, GaltonThumb].map((T) => svg(<T C={PALETTE[th]} mode={mode} />));
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{50}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];

  test("액자 목록: 하노이 · 실험 셋(풀이 보기 장면 있음) · 장면 묶음 둘 — 키 중복 없음", () => {
    assert.deepEqual(m.FRAMES.map((f) => f.key), ["hanoi", "monty", "branch", "galton", "soccer", "essay"]);
    for (const f of m.FRAMES.filter((x) => x.lab)) { assert.ok(m.EXPLAIN[f.key]?.length >= 1, f.key); assert.ok(f.title && f.desc); }
    assert.equal(new Set(m.FRAMES.map((f) => f.key)).size, 6);
  });
  test("액자 목록 그림(실험 셋): 두 판 × 두 테마 — 오류 · NaN 없음", () => {
    for (const mode of ["e", "m"]) for (const th of ["dark", "light"]) for (const s of m.thumbs(mode, th)) {
      assert.ok(s.length > 3000 && !BAD.test(s), `${mode}/${th}: ${bad(s)}`);
    }
  });
  test("그리기 훑기: 몬티홀 저절로 — 문 3 · 6 · 10, 여는 문 0 · 1 · n−2, 안다/모른다, 자연스럽게/빠르게 · 한 바퀴 내내", () => {
    for (const nn of [3, 6, 10]) for (const k of [...new Set([0, 1, nn - 2])]) for (const know of [true, false]) for (const speed of ["natural", "fast"]) {
      const P = m.fixPrm({ n: nn, k, know, play: "auto", speed });
      const D = m.autoAt(P, 0).D, G = m.autoAt(P, 0).G;
      const times = [];
      for (let r = 0; r < 2; r++) for (let x = 0; x < D; x += D / 23) times.push(r * D + x);
      times.push(G * D + 50, G * D + 3000, G * D + 7500);
      for (const t of times) for (const mode of ["e", "m"]) {
        const s = m.monty(P, m.autoVm(P, m.autoAt(P, t)), mode, mode === "e" ? "dark" : "light");
        assert.ok(!BAD.test(s), `n${nn} k${k} ${know} ${speed} t=${Math.round(t)} ${mode}: ${bad(s)}`);
      }
    }
  });
  test("그리기 훑기: 몬티홀 직접 — 고르기 전 · 여는 중 · 옮겨 가는 중 · 고르는 중 · 그대로/바꾸기 결과 · 세지 않는 판", () => {
    const P = m.fixPrm({ n: 5, k: 2, know: true }), P2 = m.fixPrm({ n: 5, k: 2, know: false });
    const T0 = { stayN: 3, stayW: 1, swN: 4, swW: 3, voids: 0 }, T1 = { ...T0, swN: 5, swW: 4 };
    const base = { auto: false, n: 5, pick: 1, opened: [2, 4], car: 3, void: false, choice: null, sw: null, r: 7, tally: T0, prev: null, tw: 1 };
    const states = [
      { ...base, phase: "pick", ms: 1200, p: 0, pick: null, opened: [], car: null },
      { ...base, phase: "open", ms: 400, p: 0.4 }, { ...base, phase: "flow", ms: 900, p: 0.45 }, { ...base, phase: "decide", ms: 2000, p: 0 },
      { ...base, phase: "reveal", ms: 600, p: 0.4, choice: 3, tally: T1, prev: T0, tw: 0.5 }, { ...base, phase: "done", ms: 900, p: 0.2, choice: 1 },
    ];
    for (const vm of states) for (const mode of ["e", "m"]) for (const th of ["dark", "light"]) {
      const s = m.monty(P, vm, mode, th);
      assert.ok(!BAD.test(s), `${vm.phase} ${mode}/${th}: ${bad(s)}`);
    }
    const vd = { ...base, phase: "void", ms: 800, p: 0.2, car: 2, void: true, tally: { ...T0, voids: 1 }, prev: T0 };
    assert.ok(!BAD.test(m.monty(P2, vd, "e", "dark")));
    const empty = { ...base, phase: "pick", ms: 0, p: 0, pick: null, opened: [], car: null, tally: { stayN: 0, stayW: 0, swN: 0, swW: 0, voids: 0 } };
    assert.ok(!BAD.test(m.monty(P, empty, "m", "dark")));
  });
  test("그리기 훑기: 갈림길과 구슬 — 1단계 2개 · 2단계 4개 · 4단계 6개, 한 바퀴 내내(준비 · 하나씩 · 다시 준비 · 한꺼번에 · 비교)", () => {
    for (const [nn, mm] of [[1, 2], [2, 4], [4, 6]]) {
      const P = { n: nn, m: mm }, TL = m.labAt(nn, mm, 0).TL;
      for (let t = 0; t < TL.dur; t += 230) for (const mode of ["e", "m"]) {
        const s = m.branch(P, m.labAt(nn, mm, t), mode, t % 460 < 230 ? "dark" : "light");
        assert.ok(!BAD.test(s), `n${nn} m${mm} t=${t} ${mode}: ${bad(s)}`);
      }
    }
  });
  test("그리기 훑기: 구슬 낙하 실험 — 못 6줄 · 구슬 100개, 못 12줄 · 구슬 200개 — 준비 · 낙하 · 정리", () => {
    for (const [R, N] of [[6, 100], [12, 200]]) {
      const P = { rows: R, n: N }, TL = m.glTimeline(N);
      for (let t = 0; t < TL.dur; t += 300) for (const mode of ["e", "m"]) {
        const s = m.galton(P, m.glAt(N, t), mode, t % 600 < 300 ? "dark" : "light");
        assert.ok(!BAD.test(s), `R${R} N${N} t=${t} ${mode}: ${bad(s)}`);
      }
      const L = m.glLayout(R, N);
      assert.ok(L.walls.left[0][1] - 52 >= 0 && L.yFloor <= 800 && L.half <= 360, `R${R}`);
      const at = m.glAt(N, TL.dur + 10);
      assert.equal(at.c, 1); assert.equal(at.stage, "prep");
    }
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
