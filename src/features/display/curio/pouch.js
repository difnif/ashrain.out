// ashrain.out — 수학 호기심 「주머니 공 꺼내기」 계산 (curio/pouch.js)
// 전체 공 수 · 한 번에 꺼내는 수 · 주머니 수 · 색 가짓수 · 다시 넣기/빼 두기를 고르면, 씨앗으로 주머니마다 공을 나눠 담고
// 차례마다 ① 꺼낼 수 있는 주머니 가운데 하나를 고르고(같은 가능성) ② 그 주머니에서 공을 한꺼번에 꺼낸다.
// 그 결과(주머니 · 색 조합)가 나올 확률 = 1/(고를 수 있는 주머니 수) × Π C(그 색 개수, 꺼낸 그 색 수) / C(주머니 공 수, 꺼낸 수).
// 빼 두기는 꺼낼 수 있는 주머니가 없을 때까지가 한 판, 다시 넣기는 정해진 차례 수가 한 판 — 판이 끝나면 새로 섞는다.
// 벽시계로 흐르는 액자라 판 · 차례는 씨앗에서 늘 똑같이 다시 계산된다(같은 씨앗 → 같은 판).
import { hashSeed, rng, rint, combBig, comb, fracBig } from "./kit.js";

export const POUCH = {
  NS: [6, 8, 10, 12, 15, 18, 20, 24, 30, 36, 40, 50, 60],
  KS: [1, 2, 3, 4],
  BS: [1, 2, 3, 4, 5, 6],
  CS: [2, 3, 4, 5, 6],
  REP_TURNS: 24,                      // 다시 넣기 한 판의 차례 수
  COLORS: [["빨강", "red"], ["파랑", "blue"], ["노랑", "yellow"], ["초록", "leaf"], ["보라", "lilac"], ["주황", "coral"]],
};
export const POUCH_DEF = { n: 24, k: 2, b: 3, c: 4, rep: false, seed: 1, sp: 1 };
export function fixPouch(p = {}) {
  const pick = (v, list, d) => (list.includes(v) ? v : d);
  const k = pick(p.k, POUCH.KS, POUCH_DEF.k), b = pick(p.b, POUCH.BS, POUCH_DEF.b), c = pick(p.c, POUCH.CS, POUCH_DEF.c);
  let n = pick(p.n, POUCH.NS, POUCH_DEF.n);
  // 주머니마다 적어도 k개는 들어가야 꺼낼 수 있다 → 모자라면 전체 공 수를 늘린다
  while (n < b * k && POUCH.NS.indexOf(n) < POUCH.NS.length - 1) n = POUCH.NS[POUCH.NS.indexOf(n) + 1];
  return { n, k, b, c, rep: !!p.rep, seed: Number.isInteger(p.seed) && p.seed > 0 ? p.seed : 1, sp: [0.5, 1, 1.5, 2].includes(p.sp) ? p.sp : 1 };
}

/** 한 판의 처음 상태: bags[b][c] = 개수 */
export function setupOf(P, round) {
  const R = rng(hashSeed("pouch", P.seed, P.n, P.k, P.b, P.c, P.rep ? 1 : 0, round));
  const B = P.b, C = P.c;
  // 주머니마다 k개씩 먼저, 나머지는 주머니마다 다른 무게로
  const size = new Array(B).fill(P.k);
  const w = Array.from({ length: B }, () => 0.35 + R());
  const ws = w.reduce((a, v) => a + v, 0);
  for (let i = B * P.k; i < P.n; i++) {
    let r = R() * ws, j = 0;
    for (; j < B - 1; j++) { r -= w[j]; if (r <= 0) break; }
    size[j]++;
  }
  // 주머니마다 색 무게를 달리해 색 섞기
  const bags = size.map((s) => {
    const cw = Array.from({ length: C }, () => 0.15 + R() ** 1.4);
    const cs = cw.reduce((a, v) => a + v, 0);
    const cnt = new Array(C).fill(0);
    for (let i = 0; i < s; i++) {
      let r = R() * cs, j = 0;
      for (; j < C - 1; j++) { r -= cw[j]; if (r <= 0) break; }
      cnt[j]++;
    }
    return cnt;
  });
  // 모든 색이 적어도 한 번은 나오게(공이 색보다 많을 때)
  if (P.n >= C) {
    for (let c = 0; c < C; c++) {
      if (bags.some((bg) => bg[c] > 0)) continue;
      // 가장 많은 색 하나를 바꾼다
      let best = null;
      bags.forEach((bg, bi) => bg.forEach((v, ci) => { if (v > 1 && (!best || v > best[2])) best = [bi, ci, v]; }));
      if (best) { bags[best[0]][best[1]]--; bags[best[0]][c]++; }
    }
  }
  return bags;
}

/** 한 번 꺼내기: 상태 bags 에서 씨앗 R 로 → { bag, elig(고를 수 있는 주머니 번호들), before(그 주머니 색별 개수), draw(꺼낸 색 순서), kc(색별 꺼낸 수), num, den } */
export function drawOnce(bags, P, R) {
  const elig = bags.map((bg, i) => [i, bg.reduce((a, v) => a + v, 0)]).filter(([, s]) => s >= P.k).map(([i]) => i);
  if (!elig.length) return null;
  const bag = elig[rint(R, elig.length)];
  const before = bags[bag].slice();
  const left = before.slice();
  const draw = [];
  for (let i = 0; i < P.k; i++) {
    const tot = left.reduce((a, v) => a + v, 0);
    let r = rint(R, tot), c = 0;
    for (; c < left.length; c++) { if (r < left[c]) break; r -= left[c]; }
    draw.push(c); left[c]--;
  }
  const kc = new Array(before.length).fill(0);
  draw.forEach((c) => kc[c]++);
  const Nb = before.reduce((a, v) => a + v, 0);
  let fav = 1n;
  kc.forEach((k, c) => { if (k) fav *= combBig(before[c], k); });
  const tot = combBig(Nb, P.k);
  const [num, den] = fracBig(fav, tot * BigInt(elig.length));
  return { bag, elig, before, draw: draw.slice().sort((a, b) => a - b), kc, fav, tot, num, den, Nb };
}

/** 한 판 전체(씨앗으로 정해진다) — turns: 차례 목록(누적 확률 포함) */
const ROUNDS = new Map();
export function roundOf(P, round) {
  const key = `${P.n}|${P.k}|${P.b}|${P.c}|${P.rep}|${P.seed}|${round}`;
  if (ROUNDS.has(key)) return ROUNDS.get(key);
  const start = setupOf(P, round);
  const bags = start.map((b) => b.slice());
  const R = rng(hashSeed("pouch-draw", P.seed, round, P.n, P.k, P.b, P.c, P.rep ? 1 : 0));
  const turns = [];
  let cn = 1n, cd = 1n;
  const tubes = new Array(P.c).fill(0);
  const max = P.rep ? POUCH.REP_TURNS : 1000;
  while (turns.length < max) {
    const d = drawOnce(bags, P, R);
    if (!d) break;
    cn *= d.num; cd *= d.den;
    const [a, b] = fracBig(cn, cd); cn = a; cd = b;
    d.kc.forEach((k, c) => { tubes[c] += k; });
    if (!P.rep) d.kc.forEach((k, c) => { bags[d.bag][c] -= k; });
    turns.push({ ...d, after: bags.map((b) => b.slice()), cum: [cn, cd], tubes: tubes.slice() });
  }
  // 기대 개수(다시 넣기): 차례마다 Σ_주머니 (1/B) · k · (그 색 비율)
  let expect = null;
  if (P.rep) {
    expect = new Array(P.c).fill(0);
    const elig = start.filter((bg) => bg.reduce((a, v) => a + v, 0) >= P.k);
    for (const bg of elig) {
      const s = bg.reduce((a, v) => a + v, 0);
      bg.forEach((v, c) => { expect[c] += (turns.length * P.k * v) / s / elig.length; });
    }
  }
  const out = { start, turns, expect };
  ROUNDS.set(key, out);
  if (ROUNDS.size > 400) ROUNDS.delete(ROUNDS.keys().next().value);
  return out;
}

/* ── 박자(1× 기준 ms) ── */
export const PT = { SETUP: 2600, TURN: 6800, SUM: 4200 };
export const roundDur = (RD) => PT.SETUP + RD.turns.length * PT.TURN + PT.SUM;
/** 경과 e(빠르기 곱한 ms) → { round, RD, stage: "setup" | "turn" | "sum", ti, t } */
export function pouchAt(P, e) {
  let x = Math.max(0, e), round = 0;
  for (;;) {
    const RD = roundOf(P, round), D = roundDur(RD);
    if (x < D || round > 5000) {
      if (x < PT.SETUP) return { round, RD, stage: "setup", ti: -1, t: x, D };
      const y = x - PT.SETUP;
      if (y < RD.turns.length * PT.TURN) { const ti = Math.floor(y / PT.TURN); return { round, RD, stage: "turn", ti, t: y - ti * PT.TURN, D }; }
      return { round, RD, stage: "sum", ti: RD.turns.length, t: y - RD.turns.length * PT.TURN, D };
    }
    x -= D; round++;
  }
}

/* ── 판서 글자 ── */
/** C(n, k) 를 중학교 꼴로: k=1 → "n", k=2 → "n × (n−1) ÷ 2", k=3 → "n × (n−1) × (n−2) ÷ (3 × 2 × 1)" */
export function combExpr(n, k) {
  if (k === 0) return "1";
  if (k === 1) return String(n);
  if (k >= n) return "1";
  const top = Array.from({ length: k }, (_, i) => n - i).join(" × ");
  const bot = k === 2 ? "2" : `(${Array.from({ length: k }, (_, i) => k - i).join(" × ")})`;
  return `${top} ÷ ${bot}`;
}
export const combVal = comb;
