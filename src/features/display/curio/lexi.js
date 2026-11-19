// ashrain.out — 수학 호기심 「알파벳 카드 사전식 배열」 계산 (curio/lexi.js)
// 카드 n장(같은 글자가 있어도 된다) 가운데 r장을 한 줄로 늘어놓는 모든 경우를 사전식(오름차순) 또는 그 거꾸로(내림차순)
// 차례로 만든다. 늘어놓은 글자가 영어 낱말이면(사전 ./data-dict.js) 멈춰서 뜻 · 발음기호를 보인다.
// 시간: 배열 하나 = 1000/빠르기 ms, 낱말이면 HOLD ms 더 머문다. 한 벌을 다 돌면 SUM ms 정리 후 다음 벌(단어 섞기는 새 카드).
import { hashSeed, rng, rint, comma } from "./kit.js";

export const LEXI = { NS: [3, 4, 5, 6, 7, 8], RATES: [0.5, 1, 2, 4, 8, 16], HOLD: 3800, SUM: 4200, MAXLIST: 45000 };
export const LEXI_DEF = { src: "word", n: 5, r: 0, ord: "asc", rate: 2, hid: true, text: "LISTEN", seed: 1 };
export function fixLexi(p = {}) {
  const n = LEXI.NS.includes(p.n) ? p.n : LEXI_DEF.n;
  const text = String(p.text || "").toUpperCase().replace(/[^A-Z]/g, "").slice(0, 8);
  const src = ["word", "abc", "mine"].includes(p.src) ? p.src : "word";
  const nn = src === "mine" ? Math.max(2, text.length || 2) : n;
  const r = Number.isInteger(p.r) && p.r >= 2 && p.r < nn ? p.r : 0;   // 0 = 모두
  return { src, n, r, ord: p.ord === "desc" ? "desc" : "asc", rate: LEXI.RATES.includes(p.rate) ? p.rate : LEXI_DEF.rate,
    hid: p.hid !== false, text: text.length >= 2 ? text : "LISTEN", seed: Number.isInteger(p.seed) && p.seed > 0 ? p.seed : 1 };
}

/** s 번째 벌의 카드(정렬된 글자) */
export function cardsOf(P, s, D) {
  if (P.src === "abc") return "ABCDEFGH".slice(0, P.n).split("");
  if (P.src === "mine") return P.text.split("").sort();
  const R = rng(hashSeed("lexi", P.seed, P.n, s));
  const pool = D.SEEDS.filter((w) => w.length === P.n);
  const list = pool.length ? pool : Object.keys(D.DICT).filter((w) => w.length === P.n && D.DICT[w].length === 2);
  return list[rint(R, list.length)].toUpperCase().split("").sort();
}

/** 여러 글자(같은 글자 포함) 가운데 r개를 늘어놓는 모든 경우 — 사전식 순서. desc 면 거꾸로 */
export function arrangements(cards, r, desc = false) {
  const letters = [...new Set(cards)].sort();
  if (desc) letters.reverse();
  const cnt = Object.fromEntries(letters.map((c) => [c, cards.filter((x) => x === c).length]));
  const out = [], cur = [];
  const rec = () => {
    if (out.length >= LEXI.MAXLIST) return;
    if (cur.length === r) { out.push(cur.join("")); return; }
    for (const c of letters) {
      if (!cnt[c]) continue;
      cnt[c]--; cur.push(c); rec(); cur.pop(); cnt[c]++;
    }
  };
  rec();
  return out;
}

/** 경우의 수(글자 수 세기로 따로 계산 — 검산용): 같은 것이 있는 순열 */
export function countArr(cards, r) {
  const counts = Object.values(cards.reduce((m, c) => ((m[c] = (m[c] || 0) + 1), m), {}));
  // r개 고르기: 다항 계수 합(지수 생성함수) — 작은 수라 직접
  const fact = (k) => { let f = 1; for (let i = 2; i <= k; i++) f *= i; return f; };
  let total = 0;
  const rec = (i, left, denom) => {
    if (i === counts.length) { if (left === 0) total += fact(r) / denom; return; }
    for (let k = 0; k <= Math.min(counts[i], left); k++) rec(i + 1, left - k, denom * fact(k));
  };
  rec(0, r, 1);
  return Math.round(total);
}

/** 한 벌: 배열 목록 · 낱말인 것 · 시작 시각 */
const SETS = new Map();
export function setOf(P, s, D) {
  const cards = cardsOf(P, s, D);
  const r = P.r || cards.length;
  const key = `${cards.join("")}|${r}|${P.ord}|${P.rate}`;
  if (SETS.has(key)) return SETS.get(key);
  const list = arrangements(cards, r, P.ord === "desc");
  const d = 1000 / P.rate;
  const hit = new Uint8Array(list.length);
  const start = new Float64Array(list.length + 1);
  let t = 0, nh = 0;
  for (let i = 0; i < list.length; i++) {
    start[i] = t;
    const w = list[i].toLowerCase();
    if (D.DICT[w]) { hit[i] = 1; nh++; }
    t += d + (hit[i] ? LEXI.HOLD : 0);
  }
  start[list.length] = t;
  const hitIdx = [];
  for (let i = 0; i < list.length; i++) if (hit[i]) hitIdx.push(i);
  const out = { cards, r, list, hit, hitIdx, start, nh, d, dur: t + LEXI.SUM, words: hitIdx.map((i) => list[i]) };
  SETS.set(key, out);
  if (SETS.size > 60) SETS.delete(SETS.keys().next().value);
  return out;
}

/** 경과 e(ms) → { s(몇 번째 벌), set, i(배열 번호), t(그 배열 안 시각), sum(정리 중?) } */
export function lexiAt(P, e, D) {
  let x = Math.max(0, e), s = 0;
  for (;;) {
    const set = setOf(P, s, D);
    if (x < set.dur || s > 2000) {
      if (x >= set.start[set.list.length]) return { s, set, i: set.list.length - 1, t: x - set.start[set.list.length - 1], sum: x - set.start[set.list.length] };
      let lo = 0, hi = set.list.length - 1;
      while (lo < hi) { const mid = (lo + hi + 1) >> 1; if (set.start[mid] <= x) lo = mid; else hi = mid - 1; }
      return { s, set, i: lo, t: x - set.start[lo], sum: -1 };
    }
    x -= set.dur; s++;
  }
}

/** 경우의 수 글자: 5 × 4 × 3 × 2 × 1 = 120 (같은 글자가 있으면 그 수로 나눈다) */
export function countText(cards, r, mode) {
  const n = cards.length;
  const total = countArr(cards, r);
  const dup = Object.values(cards.reduce((m, c) => ((m[c] = (m[c] || 0) + 1), m), {})).filter((v) => v > 1);
  const prod = Array.from({ length: r }, (_, i) => n - i).join(" × ");
  if (!dup.length) return `${prod} = ${comma(total)}가지${mode === "m" && r === n ? ` (${n}!)` : ""}`;
  if (r === n) {
    const div = dup.map((v) => Array.from({ length: v }, (_, i) => v - i).join(" × ")).map((s) => (s.includes("×") ? `(${s})` : s)).join(" ÷ ");
    return `${prod} ÷ ${div} = ${comma(total)}가지`;
  }
  return `${comma(total)}가지 (같은 글자가 있어요)`;
}
