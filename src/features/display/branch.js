// ashrain.out — 교실 모니터: 두 갈래 길과 구슬 (branch.js) — JSX 없음
// 갈림목마다 왼쪽·오른쪽 1/2. 단계 n 이면 구멍 n + 1 개, 구멍 k 로 가는 길 C(n, k)가지.
//   ② 구슬 m 개가 구멍에 나뉘는 모양(4-0-0 · 3-1-0 · 2-2-0 · 2-1-1 …)의 확률 — 모든 경우를 늘어놓아 센다.
//   ③ 물리 판(physics.js): 같은 판에 구슬을 하나씩 / 동시에 굴려, 구슬끼리 부딪힐 때 확률이 어떻게 달라지는지 본다.
//   ④ 여러 판 모아 보기 · ⑤ 두 갈래 길 2번(장면 fork) · ⑥ 갈림길이 늘어나면(장면 forkn)
import { makeWorld, addWall, addMarble, addSplitter, seal, runTo, seedMix, MARBLE } from "./physics.js";
import { rng } from "./core.js";
import { comb } from "./galton.js";

export const HOLE_NAMES = "ABCDEFGH";

/* ══════════ ② 구슬 m 개가 구멍에 나뉘는 모양 ══════════ */
/** 모양 이름: 개수를 큰 것부터 — [1,2,1] → "2-1-1" */
export const shapeOf = (counts) => [...counts].sort((a, b) => b - a).join("-");
/** 단계 n, 구슬 m 개 — 모양마다 확률(정확한 분수: [분자, 분모]) · 각 구슬은 2^n 가지 길이 똑같이 */
export function shapeProbs(n, m) {
  const holes = n + 1, ways = Array.from({ length: holes }, (_, k) => comb(n, k)), total = (2 ** n) ** m;
  const out = new Map();
  const counts = new Array(holes).fill(0);
  // 구슬마다 구멍을 고르는 모든 경우(구멍 수^m) — 그 경우의 길의 수 = 고른 구멍들의 길의 수의 곱
  const rec = (d, w) => {
    if (d === m) { const key = shapeOf(counts); out.set(key, (out.get(key) || 0) + w); return; }
    for (let k = 0; k < holes; k++) { counts[k]++; rec(d + 1, w * ways[k]); counts[k]--; }
  };
  rec(0, 1);
  const g = (a, b) => (b ? g(b, a % b) : a);
  return [...out.entries()].sort((a, b) => b[1] - a[1]).map(([key, num]) => {
    const d = g(num, total);
    return { key, num, den: total, n: num / d, d: total / d, p: num / total };
  });
}

/* ══════════ ③ 물리 판: 하나씩 / 동시에 ══════════ */
// 갈림목 = 뾰족한 지붕(Λ). 구슬은 좁은 목(세로 벽 두 개)을 지나 지붕 꼭대기에 떨어져 왼쪽·오른쪽으로 갈린다.
// 지붕의 두 비탈은 그대로 다음 단계의 목으로 이어진다(목에서 옆으로 가던 힘이 사라져, 갈림목마다 새로 반반).
// 마지막 갈림목은 칸막이(뾰족한 기둥) 꼭대기다. 맨 위에는 구슬 두 개 너비의 출발 통이 있다.
//   하나씩: 통 가운데로 gap 초마다 하나씩 떨어뜨린다 — 구슬끼리 만나지 않는다.
//   동시에: 두 개씩 나란히 한꺼번에 떨어뜨린다 — 첫 갈림목에 함께 닿아 서로 밀어낸다.
/** 물리 판 배치. n 단계 · 구슬 m 개 · (cx, y0) 첫 갈림목 · 갈림목 사이 가로 dx · 세로 dy · 구슬 반지름 r */
export function chuteLayout({ n = 2, m = 4, cx = 400, y0 = 330, dx = 150, dy = 128, r = 13 } = {}) {
  const node = (i, j) => [cx + (j - i / 2) * dx, y0 + i * dy];
  const nw = r + 3.5, neckH = r * 2.4, hn = r * 1.6;             // 목: 반폭 · 갈림목 위 높이 · 목 길이
  const tw = 2 * r + 2;                                           // 출발 통 반폭(구슬 두 개 + 틈)
  const yFloor = y0 + (n - 1) * dy + dy * 1.25;
  const gateY = y0 - neckH - r - 2;                               // 출발 통 맨 아래 구슬의 중심
  const pitch = 2 * r + 1;
  const rows = Math.ceil(m / 2);
  return { n, m, cx, y0, dx, dy, r, nw, neckH, hn, tw, yFloor, gateY, pitch, node,
    yTube: gateY - (Math.max(rows, m) - 1) * pitch - r - 10,      // 통 위 끝(하나씩: 한 줄로 m 개가 들어갈 높이)
    /** 하나씩: 통 가운데 한 줄의 k 번째 자리(0 = 맨 아래) */
    slotSeq: (k) => [cx, gateY - k * pitch],
    /** 동시에: 두 개씩 나란히 — k 번째 구슬의 자리(마지막 줄이 한 개면 가운데) */
    slotSim: (k) => {
      const row = Math.floor(k / 2), alone = row === rows - 1 && m % 2 === 1;
      return [alone ? cx : cx + (k % 2 ? 1 : -1) * (r + 1), gateY - row * pitch];
    },
    bins: Array.from({ length: n + 1 }, (_, k) => { const x = node(n, k)[0]; return { xc: x, x0: x - dx / 2, x1: x + dx / 2 }; }) };
}
/** 벽 목록 [{ pts(꺾은선), hw(반두께), kind }] — kind: roof 갈림목 지붕 · post 칸막이(뾰족한 기둥) · neck 목 · box 바깥 상자·출발 통 */
export const POST = { hw: 5, tip: 7 };
export function chuteWalls(L) {
  const { n, node, nw, neckH, hn, yFloor, cx, tw } = L;
  const out = [];
  const neckTop = (i, j) => node(i, j)[1] - neckH - hn, neckBot = (i, j) => node(i, j)[1] - neckH;
  // 갈림목(지붕): 왼쪽 비탈은 (i+1, j)의 목 오른쪽 위로, 오른쪽 비탈은 (i+1, j+1)의 목 왼쪽 위로
  for (let i = 0; i < n - 1; i++) for (let j = 0; j <= i; j++) {
    const [x, y] = node(i, j), [xl] = node(i + 1, j), [xr] = node(i + 1, j + 1);
    out.push({ kind: "roof", hw: 2.5, pts: [[xl + nw, neckTop(i + 1, j)], [x, y], [xr - nw, neckTop(i + 1, j + 1)]] });
  }
  // 칸막이 — 굵은 기둥, 꼭대기는 뾰족하게(다른 갈림목처럼 구슬이 얹혀 멈추지 않게)
  for (let j = 0; j < n; j++) {
    const [x, y] = node(n - 1, j);
    out.push({ kind: "post", hw: POST.hw, pts: [[x, y + POST.tip], [x, yFloor]] });
    out.push({ kind: "tip", hw: 2.5, pts: [[x - POST.hw + 1, y + POST.tip], [x, y], [x + POST.hw - 1, y + POST.tip]] });
  }
  // 목(세로 벽 두 개) — 첫 갈림목은 출발 통이 대신한다
  for (let i = 1; i < n; i++) for (let j = 0; j <= i; j++) {
    const [x] = node(i, j);
    out.push({ kind: "neck", hw: 2.5, pts: [[x - nw, neckTop(i, j)], [x - nw, neckBot(i, j)]] });
    out.push({ kind: "neck", hw: 2.5, pts: [[x + nw, neckTop(i, j)], [x + nw, neckBot(i, j)]] });
  }
  // 바깥 상자(왼쪽) — 출발 통 · 통 옆 천장 · 상자 벽 · 단계마다 상자 벽에서 맨 왼쪽 목으로 내려가는 바깥 지붕
  const xb = L.bins[0].x0, x00 = node(0, 0)[0], yb = neckBot(0, 0);
  const left = [[[x00 - tw, L.yTube], [x00 - tw, yb], [xb, yb], [xb, yFloor]]];
  for (let i = 1; i < n; i++) {
    const xt = node(i, 0)[0] - nw, yt = neckTop(i, 0);
    left.push([[xb, yt - (xt - xb) * 0.62], [xt, yt]]);
  }
  for (const w of left) {
    out.push({ kind: "box", hw: 2.5, pts: w });
    out.push({ kind: "box", hw: 2.5, pts: w.map(([x, y]) => [2 * cx - x, y]) });
  }
  out.push({ kind: "box", hw: 2.5, pts: [[xb, yFloor], [2 * cx - xb, yFloor]] });
  return out;
}
/** 물리 값(판) — fric 은 한 걸음(1/240초)마다 닿은 면을 따라 줄어드는 비율 · crowd 붙어 있다고 볼 틈(px) */
export const CHUTE_PHYS = { g: 1500, drag: 0.8, eWall: 0.3, eBall: 0.35, fric: 0.05, kick: 40, split: 130, crowd: 8 };
/** 구슬 m 개의 한 판: "seq" 하나씩(gap 초 간격) | "sim" 동시에(출발 통을 한꺼번에 연다) */
export function chuteWorld(L, mode, seed, { gap = 1.3, phys = CHUTE_PHYS } = {}) {
  const W = makeWorld({ g: phys.g, drag: phys.drag, eWall: phys.eWall, eBall: phys.eBall, fric: phys.fric, cell: 24, kick: phys.kick,
    crowd: phys.crowd, freezeY: L.y0 + (L.n - 1) * L.dy + 10, freezeV: 18, freezeT: 0.18, nudge: 70, seed: seedMix(seed) });
  for (const w of chuteWalls(L)) for (let k = 0; k + 1 < w.pts.length; k++) addWall(W, ...w.pts[k], ...w.pts[k + 1], w.hw);
  // 동전은 목을 빠져나온 뒤(목 아래 끝 ~ 꼭대기 사이)에 던진다 — 목 안에서 밀면 벽에 튕겨 거꾸로 간다
  for (let i = 0; i < L.n; i++) for (let j = 0; j <= i; j++) {
    const [x, y] = L.node(i, j);
    addSplitter(W, x, y, (i ? L.nw : L.tw) + 4, phys.split, L.neckH - 2);
  }
  const rnd = rng(seedMix(seed * 104729 + 17));
  for (let i = 0; i < L.m; i++) {
    const jx = (rnd() - 0.5) * 3, jv = (rnd() - 0.5) * 16;
    if (mode === "seq") { const [x, y] = L.slotSeq(0); addMarble(W, { x: x + jx, y, r: L.r, at: 0.1 + i * gap, vx: jv, vy: 60, tag: i }); }
    else { const [x, y] = L.slotSim(i); addMarble(W, { x: x + jx, y, r: L.r, at: 0.1, vx: jv, vy: 60, tag: i }); }
  }
  return seal(W);
}
/** 한 판을 모든 구슬이 칸에 멈출 때까지(최대 cap 초) 돌려 구멍별 개수 */
export function chuteTrial(L, mode, seed, opt = {}, cap = 40) {
  const W = chuteWorld(L, mode, seed, opt);
  while (W.time < cap && (W.live.length || W.nextSpawn < W.order.length)) runTo(W, W.time + 0.25);
  const counts = new Array(L.n + 1).fill(0);
  let lost = 0;
  for (let i = 0; i < W.n; i++) {
    const k = Math.floor((W.x[i] - L.bins[0].x0) / L.dx);
    if (W.st[i] === MARBLE.FROZEN && k >= 0 && k <= L.n) counts[k]++; else lost++;
  }
  return { counts, lost, W, t: W.time };
}
/* ══════════ ④ 하나씩 · 동시에 — 여러 판 모아 보기 ══════════ */
// 물리 판은 cx = 0 인 한 가지 배치로만 돌리고(같은 설정이면 같은 결과), 그릴 때 옮겨 그린다.
export const BUMP = { NS: [1, 2, 3], NDEF: 2, MS: [2, 3, 4], MDEF: 2, TRIALS: 300, GAP: 1.3, BASE: 1000,
  GEO: { y0: 330, dx: 100, dy: 110, r: 12 } };
const BLAY = new Map();
export function bumpLayout(n, m) {
  const k = `${n}|${m}`;
  if (!BLAY.has(k)) BLAY.set(k, chuteLayout({ n, m, cx: 0, ...BUMP.GEO }));
  return BLAY.get(k);
}
export const bumpWorld = (n, m, mode, seed) => chuteWorld(bumpLayout(n, m), mode, seed, { gap: BUMP.GAP });
const BRUNS = new Map();
/** 씨앗 base, base+1, … 로 count 판까지 — 앞에서부터 차례로 돌려 기억해 둔다. [{ counts, shape, t }] */
export function bumpRuns(n, m, mode, count, base = BUMP.BASE) {
  const key = `${n}|${m}|${mode}|${base}`;
  let A = BRUNS.get(key);
  if (!A) { A = []; BRUNS.set(key, A); }
  const L = bumpLayout(n, m);
  while (A.length < count) {
    const o = chuteTrial(L, mode, base + A.length, { gap: BUMP.GAP });
    A.push({ counts: o.counts, shape: shapeOf(o.counts), t: o.t, lost: o.lost });
  }
  return A;
}
/** 모양별 비율(처음 count 판) */
export function shapeFreq(runs, count) {
  const f = new Map();
  for (let i = 0; i < count; i++) f.set(runs[i].shape, (f.get(runs[i].shape) || 0) + 1);
  return (key) => (count ? (f.get(key) || 0) / count : 0);
}
/** 모양 이름: "2-1-1-0" → "2+1+1" (0 은 뺀다) */
export const shapeLabel = (key) => key.split("-").filter((x) => x !== "0").join("+");

/* ══════════ ⑤ 두 갈래 길 2번 — 구슬 4개(장면 fork) ══════════ */
const gcd = (a, b) => (b ? gcd(b, a % b) : a);
const red = (n, d) => { const g = gcd(n, d); return [n / g, d / g]; };
const fact = (k) => (k <= 1 ? 1 : k * fact(k - 1));
export const FORK = (() => {
  // 길: 갈림길 두 번(왼 0 · 오 1). 길 번호 = 2 × 첫 갈림 + 둘째 갈림 → 구멍 = 두 수의 합(A 0 · B 1 · C 2)
  const PATHS = [[0, 0], [0, 1], [1, 0], [1, 1]];
  const holeOf2 = (d) => d[0] + d[1];
  const WAYS = [0, 1, 2].map((h) => PATHS.filter((d) => holeOf2(d) === h).length);   // 1 · 2 · 1
  const P = WAYS.map((w) => red(w, 4));                                                // 1/4 · 1/2 · 1/4
  const SEQ = [1, 0, 3, 2];                       // 구슬 4개가 간 길 → B · A · C · B (세 구멍에 모두)
  // 세 구멍에 모두 들어가는 모양: 개수 (2,1,1) · (1,2,1) · (1,1,2)
  const SHAPES = [[2, 1, 1], [1, 2, 1], [1, 1, 2]].map((c) => {
    const ord = fact(4) / (fact(c[0]) * fact(c[1]) * fact(c[2]));                     // 늘어놓는 순서
    const num = ord * WAYS[0] ** c[0] * WAYS[1] ** c[1] * WAYS[2] ** c[2];             // 길로 센 경우의 수(256가지 중)
    return { c, word: "ABC".split("").map((h, k) => h.repeat(c[k])).join(""), ord, num, p: red(num, 256) };
  });
  const ALL = SHAPES.reduce((a, o) => a + o.num, 0);                                  // 96
  // 초등: 구슬 40개를 굴려 본 기록(결정적 난수)
  const r = rng(seedMix(11)), E40 = [];
  for (let i = 0; i < 40; i++) { const a = r() < 0.5 ? 0 : 1, b = r() < 0.5 ? 0 : 1; E40.push(2 * a + b); }
  const E40C = [0, 1, 2].map((h) => E40.filter((k) => holeOf2(PATHS[k]) === h).length);
  return { PATHS, WAYS, P, SEQ, SHAPES, ALL, PALL: red(ALL, 256), E40, E40C, holeOf2 };
})();

/* ══════════ ⑥ 갈림길이 늘어나면(장면 forkn) ══════════ */
export const FORKN = (() => {
  const NS = [2, 3, 4, 5, 6], NDEF = 4, ROLLN = 256;
  /** 가운데 칸이 가장 많고 양쪽으로 갈수록 줄어드나(같으면 괜찮다) */
  const bell = (c) => {
    const mid = (c.length - 1) / 2;
    for (let k = 0; k < c.length - 1; k++) {
      if (k + 1 <= mid && c[k] > c[k + 1]) return false;
      if (k >= mid && c[k] < c[k + 1]) return false;
    }
    return true;
  };
  /** 단계 n: 구멍 k 로 가는 길 C(n, k) · 확률(기약분수) · 구슬 256개를 굴린 기록(결정적).
   *  기록은 씨앗 500 + n 부터 차례로 보아 "가운데가 가장 많은" 첫 기록을 쓴다 — 우연히 들쭉날쭉한 기록으로
   *  규칙을 잘못 읽지 않게(256개면 대부분 첫 씨앗에서 된다). */
  const of = (n) => {
    const ways = Array.from({ length: n + 1 }, (_, k) => comb(n, k));
    const P = ways.map((w) => red(w, 2 ** n));
    let seed = 500 + n, rolls, counts;
    for (;; seed += 1000) {
      const r = rng(seedMix(seed));
      rolls = [];
      for (let i = 0; i < ROLLN; i++) rolls.push(Array.from({ length: n }, () => (r() < 0.5 ? 0 : 1)));
      counts = ways.map((_, k) => rolls.filter((w) => w.reduce((a, b) => a + b, 0) === k).length);
      if (bell(counts)) break;
    }
    const expect = ways.map((w) => (ROLLN * w) / 2 ** n);
    return { n, ways, P, rolls, counts, expect, seed, total: 2 ** n };
  };
  const cache = new Map();
  return { NS, NDEF, ROLLN, bell, of: (n) => { if (!cache.has(n)) cache.set(n, of(n)); return cache.get(n); } };
})();

export { MARBLE };
