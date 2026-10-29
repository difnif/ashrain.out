// ashrain.out — 교실 모니터 「몬티홀」 실험 액자 — 계산 (montylab.js) — JSX 없음
// 문 n개 가운데 하나 뒤에 자동차, 나머지는 염소. 도전자가 문 하나를 고르면 사회자가 고르지 않은 문 가운데 k개를 연다.
//   사회자가 안다: 염소 문만 연다 → 고른 문은 그대로 1/n, 열린 문의 몫은 고르지 않은 닫힌 문으로 옮겨 간다.
//                 남은 닫힌 문(n − 1 − k개)은 하나에 (n − 1)/(n(n − 1 − k)) — k = n − 2 이면 (n − 1)/n.
//   사회자도 모른다: 아무 문이나 연다. 자동차가 나오면 그 판은 세지 않는다 → 닫힌 문은 모두 1/(n − k)(바꿔도 같다).
// 바꾸기 = 남은 닫힌 문 가운데 하나(직접 하면 누른 문, 저절로 하면 아무렇게나).
// 진행: 직접(hand) = 반 아이들이 문을 눌러 고르고, 그대로/바꾸기도 눌러 정한다(누를 때까지 기다린다).
//       저절로(auto) = 컴퓨터가 한 바퀴 G판을 쉬지 않고 한다. 판마다 그대로·바꾸기 두 가지 결과를 함께 센다.
//       저절로는 벽시계로 흐르는 시간표(판 길이가 늘 같다)라 어느 순간이든 계산으로 다시 그릴 수 있다.
// 검산: tests/display-labs.test.mjs — 이론값을 모든 경우를 늘어놓아 센 값과 맞춰 본다.
import { rng } from "./core.js";

export const MLAB = {
  NS: [3, 4, 5, 6, 7, 8, 9, 10], NDEF: 3, KDEF: 1,
  GAMES: { natural: 30, fast: 300 },        // 저절로: 한 바퀴에 하는 판 수
  SUM: { natural: 7600, fast: 7600 },       // 한 바퀴를 마치고 정리해 보여 주는 시간(ms)
};
const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
export const red = (a, b) => { const g = gcd(a, b) || 1; return [a / g, b / g]; };
/** 사회자가 열 수 있는 문 수: 0 ~ n − 2 */
export const KS = (n) => Array.from({ length: n - 1 }, (_, i) => i);

/** 고를 수 있는 값으로 고친 설정 */
export function fixPrm(p = {}) {
  const n = MLAB.NS.includes(p.n) ? p.n : MLAB.NDEF;
  const k = Number.isInteger(p.k) ? Math.max(0, Math.min(n - 2, p.k)) : Math.min(MLAB.KDEF, n - 2);
  return { n, k, know: p.know !== false, play: p.play === "auto" ? "auto" : "hand", speed: p.speed === "fast" ? "fast" : "natural" };
}

/** 이론값(기약분수 [분자, 분모]): stay 그대로 · sw 바꾸기 · each 남은 닫힌 문 하나의 몫 · rest 고르지 않은 닫힌 문 모두의 몫
 *  · pick 고른 문의 몫(사회자가 연 뒤) · ok 판이 성립할 확률(모르는 사회자가 자동차를 열지 않을 확률) */
export function theory(n, k, know) {
  if (know) return { stay: red(1, n), sw: red(n - 1, n * (n - 1 - k)), each: red(n - 1, n * (n - 1 - k)), rest: red(n - 1, n), pick: red(1, n), ok: [1, 1] };
  return { stay: red(1, n - k), sw: red(1, n - k), each: red(1, n - k), rest: red(n - 1 - k, n - k), pick: red(1, n - k), ok: red(n - k, n) };
}
export const val = ([a, b]) => a / b;
/** 분수 글자 {a/b} · 정수면 그대로 */
export const ftx = ([a, b]) => (b === 1 ? String(a) : `{${a}/${b}}`);
/** 백분율(소수 첫째 자리까지, .0 은 지움) */
export const pct = (v) => `${(Math.round(v * 1000) / 10).toFixed(1).replace(/\.0$/, "")}%`;
/** 몇 배인지: 2/3 ÷ 1/3 → "2배" · 0.75 ÷ 0.25 → "3배" · 소수면 "약 1.5배" */
export function times([a, b], [c, d]) {
  const r = (a * d) / (b * c);
  return Number.isInteger(r) ? `${r}배` : `약 ${Math.round(r * 10) / 10}배`;
}

function shuffled(a, R) {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(R() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; }
  return b;
}
export const mix = (s, r) => {
  let h = Math.imul((s >>> 0) ^ Math.imul((r + 1) >>> 0, 0x9e3779b1), 0x85ebca6b);
  h = Math.imul(h ^ (h >>> 13), 0xc2b2ae35);
  return ((h ^ (h >>> 16)) >>> 0) || 1;
};
/** 판 하나의 운: 자동차 자리 · (저절로일 때) 고를 문 · 사회자가 문을 고르는 순서 · 바꿀 문을 고를 수 — 씨앗과 판 번호로 정해진다 */
export function luck(seed, r, n) {
  const R = rng(mix(seed, r));
  R(); R();
  return { car: Math.floor(R() * n), autoPick: Math.floor(R() * n), order: shuffled(Array.from({ length: n }, (_, i) => i), R), u: R() };
}
/** 사회자가 여는 문: pick 을 뺀 문 가운데 order 순으로 k개(안다: 자동차 문은 빼고) — 여는 차례(왼쪽부터)로 */
export function hostOpens(L, n, k, know, pick) {
  return L.order.filter((d) => d !== pick && (!know || d !== L.car)).slice(0, k).sort((a, b) => a - b);
}
/** 남은 닫힌 문(고른 문 · 열린 문 빼고) */
export const restOf = (n, pick, opened) => Array.from({ length: n }, (_, d) => d).filter((d) => d !== pick && !opened.includes(d));
/** 저절로 바꿀 문 */
export const autoSwitch = (L, rest) => rest[Math.floor(L.u * rest.length)];

/** 판 하나(고른 문 pick): 열린 문 · 남은 문 · 저절로 바꿀 문 · 세지 않는 판(모르는 사회자가 자동차를 열었다) · 이긴 쪽 */
export function playRound(seed, r, n, k, know, pick = null) {
  const L = luck(seed, r, n);
  const p = pick == null ? L.autoPick : pick;
  const opened = hostOpens(L, n, k, know, p);
  const vd = !know && opened.includes(L.car);
  const rest = restOf(n, p, opened);
  const sw = autoSwitch(L, rest);
  return { car: L.car, pick: p, opened, rest, sw, void: vd, stayWin: !vd && p === L.car, swWin: !vd && sw === L.car };
}

/** 문마다의 몫(확률) — stage "before" 고른 뒤 · "after" 사회자가 연 뒤(판이 성립했을 때) */
export function shares(n, k, know, pick, opened, stage) {
  const out = new Array(n).fill(1 / n);
  if (stage !== "after") return out;
  const T = theory(n, k, know);
  for (let d = 0; d < n; d++) out[d] = opened.includes(d) ? 0 : d === pick ? val(T.pick) : val(T.each);
  return out;
}

/* ══════════ 박자 ══════════ */
/** 박자(ms) — natural 자연스럽게 · fast 빠르게 · doneHand 직접 하기에서 결과를 보여 주는 시간 */
export const PACE = {
  natural: { pick: 1500, door: 560, gap: 260, settle: 300, flow: 2200, decide: 1700, reveal: 1500, done: 1900, doneHand: 4200, void: 3600 },
  fast: { pick: 160, door: 150, gap: 30, settle: 40, flow: 200, decide: 140, reveal: 200, done: 240, doneHand: 1400, void: 600 },
};
/** 사회자가 k개를 여는 데 걸리는 시간(문마다 조금씩 늦게) */
export const openGap = (k, pace) => Math.min(pace.gap, 1400 / Math.max(1, k));
export const openDur = (k, pace) => (k ? pace.door + (k - 1) * openGap(k, pace) : 0);
/** 한 판의 구간 [이름, 시작, 끝] — 자동차가 나와 세지 않는 판은 open 뒤가 모두 void */
export function phasesOf(k, pace) {
  const out = [];
  let a = 0;
  const add = (name, d) => { out.push([name, a, a + d]); a += d; };
  add("pick", pace.pick); add("open", openDur(k, pace) + pace.settle);
  if (k) add("flow", pace.flow);
  add("decide", pace.decide); add("reveal", pace.reveal); add("done", pace.done);
  return { list: out, dur: a };
}
const PH = new Map();
export function phases(k, speed) {
  const key = `${k}|${speed}`;
  if (!PH.has(key)) PH.set(key, phasesOf(k, PACE[speed]));
  return PH.get(key);
}

/* ══════════ 저절로: 벽시계 시간표 ══════════ */
/** 한 바퀴(c번째)의 씨앗 — 설정마다 다르게 */
export const cycleSeed = (n, k, know, c) => mix(mix(n * 131 + k * 17 + (know ? 7 : 3), 4242), c);
/** 한 바퀴 G판의 누적 기록: cum[i] = 처음 i판의 { stayW, swW, voids } (i = 0 … G) */
const RUNS = new Map();
export function cycleRuns(n, k, know, c, G) {
  const key = `${n}|${k}|${know ? 1 : 0}|${c}|${G}`;
  let o = RUNS.get(key);
  if (!o) {
    const seed = cycleSeed(n, k, know, c), rounds = [], cum = [{ stayW: 0, swW: 0, voids: 0 }];
    for (let r = 0; r < G; r++) {
      const R = playRound(seed, r, n, k, know);
      rounds.push(R);
      const p = cum[r];
      cum.push({ stayW: p.stayW + (R.stayWin ? 1 : 0), swW: p.swW + (R.swWin ? 1 : 0), voids: p.voids + (R.void ? 1 : 0) });
    }
    o = { seed, rounds, cum };
    RUNS.set(key, o);
    while (RUNS.size > 12) RUNS.delete(RUNS.keys().next().value);
  }
  return o;
}
/** 저절로 한 바퀴의 길이 */
export function cycleLen(P) {
  const G = MLAB.GAMES[P.speed];
  return G * phases(P.k, P.speed).dur + MLAB.SUM[P.speed];
}
/**
 * 저절로: 경과 e(ms)에서 보여 줄 판.
 *   { c 바퀴 · r 판(0부터, 정리 중이면 G) · G · R 판 · phase · p(구간 진행 0~1) · te(판 안의 시각) · ps(구간 시작 시각) · D(판 길이)
 *     · tally(지금까지 센 기록) · prev(이번 판을 세기 전) · sum(정리 진행 0~1 | null) }
 *   기록 = { stayN, stayW, swN, swW, voids, rounds } — 판마다 그대로·바꾸기를 함께 세므로 stayN = swN = 센 판 수.
 *   tally 는 결과가 열리는 순간(reveal, 세지 않는 판은 void)에 이번 판을 더한다.
 */
export function autoAt(P, e) {
  const G = MLAB.GAMES[P.speed], PHS = phases(P.k, P.speed), D = PHS.dur, cyc = G * D + MLAB.SUM[P.speed];
  const c = Math.floor(Math.max(0, e) / cyc), ec = Math.max(0, e) - c * cyc;
  const runs = cycleRuns(P.n, P.k, P.know, c, G);
  const view = (i) => { const cm = runs.cum[i]; return { stayN: i - cm.voids, stayW: cm.stayW, swN: i - cm.voids, swW: cm.swW, voids: cm.voids, rounds: i }; };
  if (ec >= G * D) {
    return { c, r: G, G, R: runs.rounds[G - 1], phase: "sum", p: 1, te: D, ps: D, D, tally: view(G), prev: view(G), sum: (ec - G * D) / MLAB.SUM[P.speed] };
  }
  const r = Math.floor(ec / D), te = ec - r * D, R = runs.rounds[r];
  let phase = "done", p = 1, ps = PHS.list[PHS.list.length - 1][1];
  for (const [name, a, b] of PHS.list) if (te >= a && te < b) { phase = name; p = (te - a) / (b - a); ps = a; break; }
  if (R.void && phase !== "pick" && phase !== "open") { const a = PHS.list[1][2]; phase = "void"; p = (te - a) / (D - a); ps = a; }
  const counted = phase === "reveal" || phase === "done" || (phase === "void" && p > 0.15);
  return { c, r, G, R, phase, p, te, ps, D, tally: view(r + (counted ? 1 : 0)), prev: view(r), sum: null };
}
/** 빠르기를 바꿀 때: 같은 바퀴 · 같은 판 · 판 안의 같은 진행 비율에서 이어 간다(새 빠르기의 판 수를 넘으면 정리부터) */
export function remapAuto(P1, P2, e) {
  const D1 = phases(P1.k, P1.speed).dur, D2 = phases(P2.k, P2.speed).dur;
  const G1 = MLAB.GAMES[P1.speed], G2 = MLAB.GAMES[P2.speed];
  const cyc1 = cycleLen(P1), cyc2 = cycleLen(P2);
  const c = Math.floor(e / cyc1), ec = e - c * cyc1;
  if (ec >= G1 * D1) return c * cyc2 + G2 * D2 + Math.min(MLAB.SUM[P2.speed] - 1, ec - G1 * D1);
  const r = Math.floor(ec / D1), f = (ec - r * D1) / D1;
  if (r >= G2) return c * cyc2 + G2 * D2;
  return c * cyc2 + (r + f) * D2;
}

/* ══════════ 직접: 반 기록 ══════════ */
/** 기록 한 칸: 그대로 · 바꾸기 판 수와 이긴 수, 세지 않은 판 */
export const emptyTally = () => ({ stayN: 0, stayW: 0, swN: 0, swW: 0, voids: 0 });
export const tallyKey = (P) => `${P.n}|${P.k}|${P.know ? 1 : 0}`;
/** 직접 하기의 구간 길이(ms) — 누를 때까지 기다리는 구간(pick · decide)은 Infinity */
export function handDur(phase, k) {
  const pc = PACE.natural;
  return { pick: Infinity, open: openDur(k, pc) + pc.settle, flow: pc.flow, decide: Infinity, reveal: pc.reveal, done: pc.doneHand, void: pc.void }[phase];
}
