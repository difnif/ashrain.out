// ashrain.out — 수학 호기심 「일렬로 세우기」 계산 (curio/lineup.js)
// n명을 한 줄로 세우는 경우 가운데 조건(이웃 · 양 끝 · 이웃하지 않음)을 지키는 것을 사전식(이름 가나다순)으로 모두 늘어놓는다.
//   이웃 k명: 그 k명이 붙어 선다(묶음) · 양 끝 e명: e = 2 면 두 사람이 양 끝, e = 1 이면 한 사람이 어느 한쪽 끝
//   이웃하지 않음 m명: 그 m명은 서로 붙지 않는다
// 경우의 수 = (양 끝 2가지 · e ≥ 1) × (U − m)! × (U − m + 1)P(m) × k!   — U = (n − e)명을 묶음은 하나로 센 덩어리 수
// tests/display-curio.test.mjs 가 모든 경우를 직접 늘어놓아 센 값과 맞춘다.
import { namesOf, hashSeed, rng, shuffle } from "./kit.js";

export const LINE = { NS: [3, 4, 5, 6, 7, 8], KS: [0, 2, 3, 4], ES: [0, 1, 2], MS: [0, 2, 3], RATES: [0.5, 1, 2, 4], SUM: 4500 };
export const LINE_DEF = { n: 5, k: 2, e: 0, m: 0, rate: 1, seed: 1 };

const fact = (x) => { let f = 1; for (let i = 2; i <= x; i++) f *= i; return f; };
const perm = (a, b) => { let f = 1; for (let i = 0; i < b; i++) f *= a - i; return b < 0 || b > a ? 0 : f; };
/** 덩어리 수 U */
export const unitsOf = (n, k, e) => { const L = n - e; return k >= 2 ? L - k + 1 : L; };
/** 조건이 성립하는지 */
export function feasible(n, k, e, m) {
  if (k + e + m > n) return false;
  if (k === 1 || m === 1) return false;
  const U = unitsOf(n, k, e);
  if (U < 1) return false;
  if (m >= 2 && U - m + 1 < m) return false;
  if (e === 2 && n < 2) return false;
  return true;
}
export function fixLine(p = {}) {
  const pick = (v, list, d) => (list.includes(v) ? v : d);
  const n = pick(p.n, LINE.NS, LINE_DEF.n);
  let k = pick(p.k, LINE.KS, 0), e = pick(p.e, LINE.ES, 0), m = pick(p.m, LINE.MS, 0);
  if (!feasible(n, k, e, m)) m = 0;
  if (!feasible(n, k, e, m)) e = 0;
  if (!feasible(n, k, e, m)) k = 0;
  return { n, k, e, m, rate: pick(p.rate, LINE.RATES, 1), seed: Number.isInteger(p.seed) && p.seed > 0 ? p.seed : 1 };
}

/** 공식으로 센 경우의 수 */
export function countLine(n, k, e, m) {
  const U = unitsOf(n, k, e);
  const ends = e >= 1 ? 2 : 1;
  return ends * fact(U - m) * perm(U - m + 1, m) * (k >= 2 ? fact(k) : 1);
}

/** 사람(가나다순) · 맡은 조건 */
export function peopleOf(P, cycle) {
  const names = namesOf(hashSeed("line", P.seed, cycle), P.n).sort((a, b) => a.localeCompare(b, "ko"));
  const R = rng(hashSeed("line-role", P.seed, cycle, P.n, P.k, P.e, P.m));
  const idx = shuffle([...Array(P.n).keys()], R);
  const block = idx.slice(0, P.k >= 2 ? P.k : 0).sort((a, b) => a - b);
  const ends = idx.slice(block.length, block.length + P.e).sort((a, b) => a - b);
  const apart = idx.slice(block.length + ends.length, block.length + ends.length + P.m).sort((a, b) => a - b);
  const role = Array(P.n).fill(null);
  block.forEach((i) => { role[i] = "block"; }); ends.forEach((i) => { role[i] = "end"; }); apart.forEach((i) => { role[i] = "apart"; });
  return { names, block, ends, apart, role };
}

/** 줄(사람 번호 배열)이 조건을 지키는지 */
export function okLine(perm, who, n) {
  const pos = new Array(n);
  perm.forEach((p, i) => { pos[p] = i; });
  if (who.block.length >= 2) {
    const ps = who.block.map((p) => pos[p]);
    if (Math.max(...ps) - Math.min(...ps) !== who.block.length - 1) return false;
  }
  if (who.ends.length === 2) { const a = pos[who.ends[0]], b = pos[who.ends[1]]; if (!((a === 0 && b === n - 1) || (a === n - 1 && b === 0))) return false; }
  if (who.ends.length === 1) { const a = pos[who.ends[0]]; if (a !== 0 && a !== n - 1) return false; }
  for (let i = 0; i < who.apart.length; i++) for (let j = i + 1; j < who.apart.length; j++) if (Math.abs(pos[who.apart[i]] - pos[who.apart[j]]) < 2) return false;
  return true;
}

/** 조건을 지키는 줄을 사전식으로 모두 */
const CASES = new Map();
export function casesOf(P, cycle) {
  const key = `${P.n}|${P.k}|${P.e}|${P.m}|${P.seed}|${cycle}`;
  if (CASES.has(key)) return CASES.get(key);
  const who = peopleOf(P, cycle);
  const out = [];
  const a = [...Array(P.n).keys()];
  // 사전식 다음 순열
  for (;;) {
    if (okLine(a, who, P.n)) out.push(a.slice());
    let i = a.length - 2;
    while (i >= 0 && a[i] > a[i + 1]) i--;
    if (i < 0) break;
    let j = a.length - 1;
    while (a[j] < a[i]) j--;
    [a[i], a[j]] = [a[j], a[i]];
    for (let l = i + 1, r = a.length - 1; l < r; l++, r--) [a[l], a[r]] = [a[r], a[l]];
  }
  const res = { who, cases: out };
  CASES.set(key, res);
  if (CASES.size > 40) CASES.delete(CASES.keys().next().value);
  return res;
}

/** 경과 e(ms) → { cycle, who, cases, j(지금 나오는 경우 번호), t, sum } — 한 바퀴 = 경우 수 × (1000/빠르기) + SUM */
export function lineAt(P, e) {
  const d = 1000 / P.rate;
  let x = Math.max(0, e), cycle = 0;
  for (;;) {
    const C = casesOf(P, cycle);
    const D = C.cases.length * d + LINE.SUM;
    if (x < D || cycle > 5000) {
      const j = Math.min(C.cases.length - 1, Math.floor(x / d));
      const sum = x >= C.cases.length * d ? x - C.cases.length * d : -1;
      return { cycle, ...C, j, t: x - j * d, sum, d, D };
    }
    x -= D; cycle++;
  }
}

/** 판서: 전략 → 식 (mode m: 4! 같은 기호도 곁들인다) */
export function strategyLines(P, who, mode) {
  const nm = (arr) => arr.map((i) => who.names[i].slice(1)).join(" · ");
  const U = unitsOf(P.n, P.k, P.e);
  const out = [];
  const prodTo = (x) => (x <= 1 ? "1" : Array.from({ length: x }, (_, i) => x - i).join(" × "));
  const facts = [];
  if (P.e === 2) { out.push({ s: `① ${nm(who.ends)}: 양 끝에 서는 방법 2 × 1 = 2가지` }); facts.push(["2", 2]); }
  if (P.e === 1) { out.push({ s: `① ${nm(who.ends)}: 왼쪽 끝 또는 오른쪽 끝 → 2가지` }); facts.push(["2", 2]); }
  if (P.k >= 2) out.push({ s: `${P.e ? "②" : "①"} ${nm(who.block)}: 한 덩어리로 묶어요` });
  const free = U - P.m;
  const step = (P.e ? 1 : 0) + (P.k >= 2 ? 1 : 0);
  const mark = ["①", "②", "③", "④", "⑤"];
  out.push({ s: `${mark[step]} ${P.e ? "나머지 " : ""}덩어리 ${free}개를 한 줄로: ${prodTo(free)} = ${fact(free)}가지${mode === "m" && free > 1 ? ` (${free}!)` : ""}` });
  facts.push([free > 1 ? `${fact(free)}` : "1", fact(free)]);
  if (P.m >= 2) {
    const slots = free + 1;
    out.push({ s: `${mark[step + 1]} ${nm(who.apart)}: 덩어리 사이사이 · 양 끝에 끼우기` });
    out.push({ s: `${slots}자리 중 ${P.m}자리 → ${Array.from({ length: P.m }, (_, i) => slots - i).join(" × ")} = ${perm(slots, P.m)}가지`, small: true });
    facts.push([`${perm(slots, P.m)}`, perm(slots, P.m)]);
  }
  if (P.k >= 2) {
    out.push({ s: `${mark[step + (P.m >= 2 ? 2 : 1)]} 묶음 안에서 자리 바꾸기: ${prodTo(P.k)} = ${fact(P.k)}가지` });
    facts.push([`${fact(P.k)}`, fact(P.k)]);
  }
  const total = facts.reduce((a, [, v]) => a * v, 1);
  out.push({ s: `모두 ${facts.map(([s]) => s).join(" × ")} = ${total}가지`, hi: true });
  return { lines: out, total };
}
