// ashrain.out — 교실 모니터: 몬티홀 · 찍기의 확률 (guess.js) — JSX 없음
// 화면에 나오는 확률(정확한 분수)과 여러 판 해 본 기록(결정적 난수)을 여기서 계산한다. tests/display.test.mjs 가 다시 검산한다.
import { rng } from "./core.js";
import { seedMix } from "./physics.js";

const gcd = (a, b) => (b ? gcd(b, a % b) : a);
/** 기약분수 [분자, 분모] */
export const red = (n, d) => { const g = gcd(n, d); return [n / g, d / g]; };
/** 분수 글자: [1, 3] → "{1/3}", [2, 1] → "2" */
export const fracS = (p) => (p[1] === 1 ? String(p[0]) : `{${p[0]}/${p[1]}}`);
/** 백분율 글자(소수 첫째 자리까지, .0 은 지움) */
export const pctS = (v) => `${(Math.round(v * 1000) / 10).toFixed(1).replace(/\.0$/, "")}%`;

/* ══════════ 몬티홀 — 문 n 개 ══════════ */
// 처음엔 늘 1번 문을 고른다(어느 문을 골라도 같다). 사회자는 자동차가 어디 있는지 알고, 염소 문만 연다.
//   그대로: 1/n — 처음 고를 때 이미 정해진다(사회자가 문을 열어도 바뀌지 않는다)
//   염소 문 하나만 열고 바꾸기: 처음이 염소일 확률 (n−1)/n × 남은 n−2 개 중 자동차 1/(n−2) = (n−1)/(n(n−2))
//   하나만 남기고 다 연 뒤 바꾸기: 처음이 염소이면 남은 한 문이 반드시 자동차 → (n−1)/n
export const MONTY = (() => {
  const NS = [3, 4, 5], NDEF = 3, GAMES = 300;
  const probs = (n) => ({ stay: red(1, n), sw1: red(n - 1, n * (n - 2)), swAll: red(n - 1, n) });
  const make = (n) => {
    const r = rng(seedMix(700 + n)), out = [];
    for (let g = 0; g < GAMES; g++) {
      const car = Math.floor(r() * n), pick = 0;
      const goats = [];
      for (let d = 1; d < n; d++) if (d !== car) goats.push(d);
      const open = goats[Math.floor(r() * goats.length)];
      const closed = [];
      for (let d = 1; d < n; d++) if (d !== open) closed.push(d);
      const sw = closed[Math.floor(r() * closed.length)];
      out.push({ car, open, sw, stay: car === pick, sw1: sw === car, swAll: car !== pick });
    }
    return out;
  };
  const cache = new Map();
  const games = (n) => { if (!cache.has(n)) cache.set(n, make(n)); return cache.get(n); };
  /** 처음 k 판의 이긴 횟수 */
  const wins = (n, k, key) => { let c = 0; const G = games(n); for (let i = 0; i < k; i++) if (G[i][key]) c++; return c; };
  return { NS, NDEF, GAMES, probs, games, wins };
})();

/* ══════════ 5지선다 — 지우고 찍기 ══════════ */
// 남은 보기가 k 개면 맞힐 확률 1/k. 지울수록 커진다: 5 → 4 → 3 → 2 개 = 20 · 25 · 33.3 · 50 %.
// 시험지에는 정답을 알고 지워 주는 사회자가 없다 → 둘 중 처음 찍은 것을 바꿔도 1/2 그대로.
// 4점짜리 5문제를 모두 찍을 때(같은 방법으로): 맞힌 수의 평균 = 5 × 1/k. 학생 200명(결정적)이 해 본 기록.
export const PICK5 = (() => {
  const LEFT = [5, 4, 3, 2];
  const P = LEFT.map((k) => red(1, k));
  const Q = 5, PTS = 4, STUDENTS = 200;
  const STRATS = [5, 3, 2];                                // 아무거나 · 셋 중 · 둘 중
  const mean = (k) => Q / k;
  // 맞힌 수 분포(정확): 이항분포 B(5, 1/k)
  const C5 = [1, 5, 10, 10, 5, 1];
  const dist = (k) => C5.map((c, j) => (c * (k - 1) ** (Q - j)) / k ** Q);
  const sims = STRATS.map((k, si) => {
    const r = rng(seedMix(900 + si)), hist = new Array(Q + 1).fill(0);
    let tot = 0;
    for (let s = 0; s < STUDENTS; s++) {
      let c = 0;
      for (let q = 0; q < Q; q++) if (r() < 1 / k) c++;
      hist[c]++; tot += c;
    }
    return { k, hist, avg: tot / STUDENTS };
  });
  return { LEFT, P, Q, PTS, STUDENTS, STRATS, mean, dist, sims };
})();

/* ══════════ 이게 맞으면 저것도 — 연결된 답 ══════════ */
// 3번은 ②·④ 중, 7번은 ①·③ 중 고민. 7번 보기를 보니 "3번이 ②면 7번은 ①, ④면 ③"(답끼리 맞물림).
// 참인 답은 맞물린 두 짝 (②,①)·(④,③) 가운데 하나라고 보자(확신이 없으면 반반).
//   따로 찍기(맞물림 무시): 4가지 짝 중 하나 → 둘 다 1/4 · 하나만 1/2 · 둘 다 틀림 1/4 → 평균 1문제
//   맞물려 찍기: 2가지 짝 중 하나 → 둘 다 1/2 · 둘 다 틀림 1/2 → 평균 1문제(같다!) — 모 아니면 도
//   3번에 70% 확신이 있으면: 따로 0.7 + 0.5 = 1.2문제(둘 다 35%) · 맞물려 1.4문제(둘 다 70%) — 확신이 7번으로 옮겨 간다
export const LINKED = (() => {
  const Q3 = ["②", "④"], Q7 = ["①", "③"];                // 맞물림: Q3[i] ↔ Q7[i]
  const indep = [red(1, 4), red(1, 2), red(1, 4)];        // 맞힌 수 0 · 1 · 2
  const linked = [red(1, 2), red(0, 1), red(1, 2)];
  const mean = (d) => d.reduce((a, p, j) => a + (j * p[0]) / p[1], 0);
  const CONF = 0.7;
  const pIndep = [(1 - CONF) * 0.5, CONF * 0.5 + (1 - CONF) * 0.5, CONF * 0.5];
  const pLinked = [1 - CONF, 0, CONF];
  const meanP = (d) => d.reduce((a, p, j) => a + j * p, 0);
  // 셋 중 고민인 두 문제(3 × 3): 둘 다 맞힐 확률 1/9 → 1/3, 평균은 둘 다 2/3
  const three = { indepBoth: red(1, 9), linkedBoth: red(1, 3), mean: red(2, 3) };
  return { Q3, Q7, indep, linked, mean, CONF, pIndep, pLinked, meanP, three };
})();
