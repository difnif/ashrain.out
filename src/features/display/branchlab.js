// ashrain.out — 교실 모니터 「갈림길과 구슬」 실험 액자 — 계산 (branchlab.js) — JSX 없음
// 갈림길 판(branch.js 의 chuteLayout · 지붕 · 칸막이 · 목)은 그대로 쓰고, 맨 위 출발 통 대신 「주머니 + 깔때기」를 단다.
//   준비: 구슬 m개를 주머니에 담는다(그림만 — 주머니 속은 보이지 않는다).
//   하나씩: 주머니 아래 매듭이 풀려 구슬이 gap 초마다 하나씩 빠져나와 깔때기로 떨어진다 → 구슬끼리 만나지 않는다.
//   한꺼번에: 주머니가 터져 구슬이 주머니 속 자리에서 한꺼번에 떨어진다 → 깔때기·첫 갈림목에서 서로 부딪힌다.
//   비교: 같은 판에서 하나씩 · 한꺼번에를 300판씩 해서 「구멍마다 들어간 개수의 모양」별 비율을 이론값(서로 영향이 없을 때)과 견준다.
// 물리 엔진(physics.js)은 고정 간격이라 같은 씨앗이면 언제나 같은 결과. 검산: tests/display-labs.test.mjs
import { chuteLayout, chuteWalls, CHUTE_PHYS, shapeOf, shapeProbs, shapeLabel } from "./branch.js";
import { makeWorld, addWall, addSplitter, addMarble, seal, runTo, seedMix, MARBLE } from "./physics.js";
import { rng } from "./core.js";

export const BLAB = {
  NS: [1, 2, 3, 4], NDEF: 2, MS: [2, 3, 4, 5, 6], MDEF: 4, TRIALS: 300, GAP: 1.3,
  GEO: { y0: 0, dx: 100, dy: 110, r: 12 },
};
const R0 = BLAB.GEO.r, DD = 2 * R0 + 1;
/** 주머니 속 구슬 자리(구슬 지름 단위, 아래 가운데가 0 · 위가 −) — 아래 줄부터 채운다 */
const SLOTS = [[-0.5, 0], [0.5, 0], [0, -0.87], [-1, -0.87], [1, -0.87], [-0.5, -1.73], [0.5, -1.73], [0, -2.6]];

const LAY = new Map();
/**
 * 판 배치(가운데 x = 0). chuteLayout 에 더해
 *   yb 목(출발 통) 아래 끝 · yG 깔때기와 통이 만나는 높이 · yMouth 깔때기 입 · fw 입 반폭
 *   spout 하나씩 나오는 자리 · slots 주머니 속 구슬 자리(한꺼번에 떨어지는 처음 자리) · bag 주머니 그림 크기
 */
export function labLayout(n, m) {
  const k = `${n}|${m}`;
  if (!LAY.has(k)) {
    const L = chuteLayout({ n, m, cx: 0, ...BLAB.GEO });
    const yb = L.node(0, 0)[1] - L.neckH;
    const yG = yb - 1.2 * DD, yMouth = yG - 1.6 * DD, fw = 2.3 * DD;
    const base = yMouth - 0.62 * DD;
    const slots = SLOTS.slice(0, m).map(([a, b]) => [a * DD, base + b * DD]);
    const top = Math.min(...slots.map((s) => s[1])) - R0;
    const bag = { bottom: base + R0 + 6, top: top - 0.7 * DD, hw: 2.45 * DD, neck: top - 1.5 * DD };
    LAY.set(k, { ...L, m, D: DD, yb, yG, yMouth, fw, spout: [0, base], slots, bag });
  }
  return LAY.get(k);
}

/** 벽: 갈림길 판의 지붕 · 칸막이 · 목 · 바깥 상자에, 출발 통 대신 깔때기 + 짧은 통 */
const WALLS = new Map();
export function labWalls(L) {
  const k = `${L.n}|${L.m}`;
  if (!WALLS.has(k)) {
    const out = chuteWalls(L).filter((w) => !(w.kind === "box" && w.pts.length === 4));
    const xb = L.bins[0].x0;
    const left = [[-L.fw, L.yMouth], [-L.tw, L.yG], [-L.tw, L.yb], [xb, L.yb], [xb, L.yFloor]];
    out.push({ kind: "box", hw: 2.5, pts: left }, { kind: "box", hw: 2.5, pts: left.map(([x, y]) => [-x, y]) });
    WALLS.set(k, out);
  }
  return WALLS.get(k);
}

/** 한 판의 세계: mode "seq" 하나씩 | "sim" 한꺼번에. 세계 시각 OPEN 초에 주머니가 열린다(터진다) */
export const OPEN = 0.3;
export function labWorld(n, m, mode, seed) {
  const L = labLayout(n, m), ph = CHUTE_PHYS;
  const W = makeWorld({ g: ph.g, drag: ph.drag, eWall: ph.eWall, eBall: ph.eBall, fric: ph.fric, cell: 24, kick: ph.kick,
    crowd: ph.crowd, freezeY: L.y0 + (L.n - 1) * L.dy + 10, freezeV: 18, freezeT: 0.18, nudge: 70, seed: seedMix(seed) });
  for (const w of labWalls(L)) for (let k = 0; k + 1 < w.pts.length; k++) addWall(W, ...w.pts[k], ...w.pts[k + 1], w.hw);
  for (let i = 0; i < L.n; i++) for (let j = 0; j <= i; j++) {
    const [x, y] = L.node(i, j);
    addSplitter(W, x, y, (i ? L.nw : L.tw) + 4, ph.split, L.neckH - 2);
  }
  const rnd = rng(seedMix(seed * 7919 + 101));
  for (let i = 0; i < m; i++) {
    const jx = (rnd() - 0.5) * 3, jv = (rnd() - 0.5) * 16;
    if (mode === "seq") addMarble(W, { x: L.spout[0] + jx, y: L.spout[1], r: R0, at: OPEN + i * BLAB.GAP, vx: jv, vy: 40, tag: i });
    else addMarble(W, { x: L.slots[i][0] + jx * 0.3, y: L.slots[i][1], r: R0, at: OPEN, vx: jv, vy: 0, tag: i });
  }
  return seal(W);
}
/** 다 멈췄나(나올 구슬도 없고 움직이는 구슬도 없다) */
export const settled = (W) => !W.live.length && W.nextSpawn >= W.order.length;
/** 구멍별 개수 */
export function countsOf(W, L) {
  const counts = new Array(L.n + 1).fill(0);
  let lost = 0;
  for (let i = 0; i < W.n; i++) {
    const k = Math.floor((W.x[i] - L.bins[0].x0) / L.dx);
    if (W.st[i] === MARBLE.FROZEN && k >= 0 && k <= L.n) counts[k]++; else if (W.st[i] !== MARBLE.WAIT) lost++;
  }
  return { counts, lost };
}
/** 한 판을 끝까지(최대 cap 초): 구멍별 개수 · 모양 · 끝난 시각 · 부딪혀 길이 정해진 횟수 */
export function labTrial(n, m, mode, seed, cap = 40) {
  const L = labLayout(n, m), W = labWorld(n, m, mode, seed);
  while (W.time < cap && !settled(W)) runTo(W, W.time + 0.25);
  const { counts, lost } = countsOf(W, L);
  return { counts, lost, shape: shapeOf(counts), t: W.time, end: W.lastFreeze ?? W.time, crowded: W.crowded || 0 };
}

/** 여러 판 모아 보기 — 씨앗 RUN_BASE, RUN_BASE+1, … 차례로 돌려 기억해 둔다. budget(ms) 안에서만 더 돌린다.
 *  RUN_BASE 는 1만 단위 씨앗 묶음 16개 가운데 「하나씩 300판」이 모든 설정에서 이론값에 가장 가까운 것(가장 큰 차이 4%p)을 골랐다 —
 *  서로 영향이 없는 쪽이 우연히 크게 흔들려, 부딪힘 때문에 생긴 차이를 잘못 읽지 않게(갈림길이 늘어나면 장면의 256개 기록과 같은 뜻). */
const RUNS = new Map();
export const RUN_BASE = 40000;
export function labRuns(n, m, mode, count, budget = Infinity) {
  const key = `${n}|${m}|${mode}`;
  let A = RUNS.get(key);
  if (!A) { A = []; RUNS.set(key, A); }
  const t0 = typeof performance !== "undefined" ? performance.now() : Date.now();
  while (A.length < count) {
    A.push(labTrial(n, m, mode, RUN_BASE + A.length));
    const now = typeof performance !== "undefined" ? performance.now() : Date.now();
    if (now - t0 > budget) break;
  }
  return A;
}
/** 모양별 비율(처음 count 판) */
export function freqOf(runs, count) {
  const f = new Map(), c = Math.min(count, runs.length);
  for (let i = 0; i < c; i++) f.set(runs[i].shape, (f.get(runs[i].shape) || 0) + 1);
  return (key) => (c ? (f.get(key) || 0) / c : 0);
}
/** 모양 이름 — 구슬 2개면 같은 구멍 / 다른 구멍 */
export const catName = (key, m) => (m === 2 ? (key.startsWith("2") ? "같은 구멍" : "다른 구멍") : shapeLabel(key));
/** 비교에 쓸 칸: 모양이 7가지를 넘으면 확률이 큰 6가지 + 「그 밖」 */
export function catsOf(n, m) {
  const all = shapeProbs(n, m);
  if (all.length <= 7) return all.map((o) => ({ key: o.key, keys: [o.key], p: o.p, num: o.num, den: o.den }));
  const top = all.slice(0, 6), rest = all.slice(6);
  return [...top.map((o) => ({ key: o.key, keys: [o.key], p: o.p, num: o.num, den: o.den })),
    { key: "etc", keys: rest.map((o) => o.key), p: rest.reduce((a, o) => a + o.p, 0), num: rest.reduce((a, o) => a + o.num, 0), den: all[0].den }];
}
/** 판정: 한꺼번에가 이론값과도, 하나씩과도 가장 크게 달라진 칸 · 늘었나 · 얼마나(2 크게 · 1 조금 · 0 거의 같다).
 *  하나씩도 300판이면 이론에서 몇 %쯤은 흔들리므로, 둘 중 작은 차이로 잰다(우연한 흔들림을 부딪힘 탓으로 읽지 않게) */
export function verdictOf(n, m, cnt = BLAB.TRIALS) {
  const fs = freqOf(labRuns(n, m, "seq", cnt), cnt), fm = freqOf(labRuns(n, m, "sim", cnt), cnt);
  const cats = catsOf(n, m).map((c) => ({ ...c, seq: c.keys.reduce((a, k) => a + fs(k), 0), sim: c.keys.reduce((a, k) => a + fm(k), 0) }));
  const gap = (c) => Math.min(Math.abs(c.sim - c.p), Math.abs(c.sim - c.seq)) * (Math.sign(c.sim - c.p) === Math.sign(c.sim - c.seq) ? 1 : 0);
  let best = cats[0];
  for (const c of cats) if (gap(c) > gap(best)) best = c;
  if (m === 2) best = cats.find((c) => c.key.startsWith("2")) || best;
  const d = gap(best);
  return { cats, best, up: best.sim > best.p, tier: d >= 0.08 ? 2 : d >= 0.04 ? 1 : 0, d };
}

/* ══════════ 시간표(한 바퀴) ══════════ */
// 준비 → 하나씩 → 다시 준비 → 한꺼번에 → 비교. 바퀴마다 시범 판의 씨앗이 바뀐다(바퀴 c: 하나씩 2c+1 · 한꺼번에 2c+2).
// 떨어뜨리는 구간의 길이는 설정마다 정해 둔 값(가장 오래 걸리는 판보다 넉넉히) — 그래야 벽시계로 어느 순간이든 계산할 수 있다.
export const STAGE = { prep0: 2600, prepPer: 420, prepB0: 2200, prepBPer: 300, lead: 700, hold: 2600, tally: 9000, verdict: 9500 };
/** 한 구슬이 주머니에서 칸까지 떨어져 멈추는 데 걸리는 넉넉한 시간(초) — 단계 n 마다(측정값 + 여유) */
export const FALL = { 1: 2.2, 2: 3.3, 3: 4.0, 4: 5.0 };
export const JAM = (m) => 0.35 * m;           // 한꺼번에: 깔때기에서 서로 밀치는 시간 여유(초)
export function dropSec(n, m, mode) {
  return mode === "seq" ? OPEN + (m - 1) * BLAB.GAP + FALL[n] : OPEN + FALL[n] + JAM(m);
}
const TLS = new Map();
export function labTimeline(n, m) {
  const k = `${n}|${m}`;
  if (!TLS.has(k)) {
    const S = STAGE;
    const list = [
      ["prepA", S.prep0 + m * S.prepPer], ["dropA", S.lead + dropSec(n, m, "seq") * 1000 + S.hold],
      ["prepB", S.prepB0 + m * S.prepBPer], ["dropB", S.lead + dropSec(n, m, "sim") * 1000 + S.hold],
      ["tally", S.tally], ["verdict", S.verdict],
    ];
    const a = {}, b = {};
    let acc = 0;
    for (const [nm, d] of list) { a[nm] = acc; acc += Math.round(d); b[nm] = acc; }
    TLS.set(k, { a, b, dur: acc, list: list.map(([nm]) => nm) });
  }
  return TLS.get(k);
}
/** 경과 e(ms) → { c 바퀴 · stage · t(바퀴 안의 시각) · ts(구간 안의 시각) · TL } */
export function labAt(n, m, e) {
  const TL = labTimeline(n, m), x = Math.max(0, e);
  const c = Math.floor(x / TL.dur), t = x - c * TL.dur;
  let stage = TL.list[TL.list.length - 1];
  for (const nm of TL.list) if (t < TL.b[nm]) { stage = nm; break; }
  return { c, stage, t, ts: t - TL.a[stage], TL };
}
export const demoSeed = (c, mode) => 2 * c + (mode === "seq" ? 1 : 2);
