// ashrain.out — 연산 규칙 생성기 (v0.2.2b)
// src/lib/calcGen.js — AdminCalc.jsx의 🎲 규칙 생성 탭이 사용합니다.
// gen_m1.mjs + gen_m2.mjs(검증 완료본)를 브라우저 모듈로 병합한 것.
// 역설계 방식이라 생성 문제의 정답은 계산상 보장됩니다.

// ── 유틸 ──
let seed = 20260714;
function rand() {  // mulberry32 — 정수 연산 PRNG (정밀도 안전)
  seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const ri = (a, b) => a + Math.floor(rand() * (b - a + 1));
const pick = (arr) => arr[Math.floor(rand() * arr.length)];
const shuffle = (arr) => { const a = [...arr]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
const SUP = { "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹" };
const sup = (n) => (n === 1 ? "" : String(n).split("").map((d) => SUP[d]).join(""));
const M = "−"; // 유니코드 마이너스 (문제 표기용)
const BATCHIM = { "0": 1, "1": 1, "3": 1, "6": 1, "7": 1, "8": 1, "2": 0, "4": 0, "5": 0, "9": 0 };
function eul(s) {  // 식 끝 문자의 발음 받침으로 을/를 결정
  const t = String(s).replace(/[)°\s]+$/g, "");
  const c = t[t.length - 1];
  if (c in BATCHIM) return BATCHIM[c] ? "을" : "를";
  const code = c ? c.charCodeAt(0) : 0;
  if (code >= 0xAC00 && code <= 0xD7A3) return (code - 0xAC00) % 28 ? "을" : "를";  // 한글 받침
  return "를";  // x, a, b, y 등 (엑스·에이…받침 없음)
}
const sgn = (n) => (n < 0 ? M : "+");
const wrap = (n) => (n < 0 ? `(${M}${-n})` : `(+${n})`);          // (−9), (+7)
const num = (n) => (n < 0 ? `${M}${-n}` : `${n}`);                 // 표기용
const ansN = (n) => String(n);                                      // 답(ASCII)
function fracStr(p, q, forAnswer = false) {                         // 기약분수 문자열
  if (q < 0) { p = -p; q = -q; }
  const g = gcd(Math.abs(p), q) || 1; p /= g; q /= g;
  if (q === 1) return forAnswer ? String(p) : num(p);
  return forAnswer ? `${p}/${q}` : `${p < 0 ? M : ""}${Math.abs(p)}/${q}`;
}
function facStr(fac) {                                              // {2:3,5:1} → "2³×5"
  return Object.keys(fac).map(Number).sort((a, b) => a - b)
    .map((p) => `${p}${sup(fac[p])}`).join("×");
}
const facVal = (fac) => Object.entries(fac).reduce((v, [p, e]) => v * Math.pow(+p, +e), 1);
function monoStr(coef, vars) {                                      // 계수+변수부 → "−32x²y⁶"
  let v = Object.entries(vars).filter(([, e]) => e > 0).map(([x, e]) => x + sup(e)).join("");
  if (coef === 1 && v) return v;
  if (coef === -1 && v) return M + v;
  return num(coef) + v;
}
// 일차식 문자열: ax+b (답용 ASCII)
function linAns(a, b, x = "x") {
  let s = a === 1 ? x : a === -1 ? `-${x}` : `${a}${x}`;
  if (b > 0) s += `+${b}`; else if (b < 0) s += `${b}`;
  return a === 0 ? String(b) : s;
}
const linQ = (a, b, x = "x") => {                                   // 표기용 (유니코드 −)
  let s = a === 1 ? x : a === -1 ? M + x : `${num(a)}${x}`;
  if (b > 0) s += ` + ${b}`; else if (b < 0) s += ` ${M} ${-b}`;
  return s;
};

// 유형별 생성 프레임: 중복 제거하며 정확히 500개
const P = (type, question, answer, diff, tl, choices = null) =>
  ({ type, question, answer: String(answer), choices, difficulty: diff, timeLimit: tl });
// choice 보기 조립: 정답 + 오답들(중복·정답충돌 제거) → 5개
function opts(ans, wrongs) {
  const set = [String(ans)];
  for (const w of wrongs) { const s = String(w); if (s && !set.includes(s)) set.push(s); if (set.length === 5) break; }
  return set.length === 5 ? shuffle(set) : null;
}

// ═══════════ 1. m1-int 정수와 유리수의 계산 ═══════════
const intBuilders = [
  () => { const a = ri(-48, 48) || 3, b = ri(-48, 48) || -5;        // 덧셈 2항
    return P("calc", `${wrap(a)} + ${wrap(b)}${eul(b)} 계산하시오.`, a + b, 1, 8); },
  () => { const a = ri(-20, 20) || 2, b = ri(-20, 20) || -3, c = ri(-20, 20) || 7;  // 덧셈 3항
    return P("calc", `${wrap(a)} + ${wrap(b)} + ${wrap(c)}${eul(c)} 계산하시오.`, a + b + c, 2, 12); },
  () => { const a = ri(-30, 30) || 4, b = ri(-30, 30) || -6;        // 뺄셈 2항
    return P("calc", `${wrap(a)} ${M} ${wrap(b)}${eul(b)} 계산하시오.`, a - b, 1, 8); },
  () => { const a = ri(-15, 15) || 2, b = ri(-15, 15) || 3, c = ri(-15, 15) || -4;  // 덧뺄셈 혼합
    return P("calc", `${num(a)} ${M} ${wrap(b)} + ${wrap(c)}${eul(c)} 계산하시오.`, a - b + c, 2, 12); },
  () => { const m = ri(2, 11), n = ri(2, 11); if (m === n) return null;             // 절댓값 최대·최소
    const kind = pick([["a + b", "큰", m + n], ["a + b", "작은", -(m + n)], ["a ${M} b", "큰", m + n], ["a ${M} b", "작은", -(m + n)]]);
    const expr = kind[0].includes("$") ? `a ${M} b` : "a + b";
    return P("calc", `|a| = ${m}, |b| = ${n}일 때, ${expr}의 값 중 가장 ${kind[1]} 값을 구하시오.`, kind[2], 2, 15); },
  () => { const m = ri(2, 9), n = ri(2, 9); if (m === n) return null;               // 절댓값 최대·최소 choice
    const ans = m + n, ch = opts(ans, [-(m + n), Math.abs(m - n), -Math.abs(m - n), m * n, m + n + 1]);
    return ch && P("choice", `두 정수 a, b에 대하여 |a| = ${m}, |b| = ${n}일 때, a ${M} b의 값 중 가장 큰 값은?`, ans, 2, 15, ch); },
  () => { const a = ri(2, 12) * pick([1, -1]), b = ri(2, 12) * pick([1, -1]);       // 정수 곱셈
    return P("calc", `${wrap(a)} × ${wrap(b)}${eul(b)} 계산하시오.`, a * b, 1, 8); },
  () => { const q1 = pick([2, 3, 4, 5, 7]), p1 = ri(1, q1 * 3) * pick([1, -1]);     // 분수 × 분수
    const q2 = pick([2, 3, 5, 6, 7, 9]); let p2 = ri(1, q2 * 2) * pick([1, -1]);
    if (Math.abs(p1) % q1 === 0 || Math.abs(p2) % q2 === 0) return null;
    return P("calc", `(${fracStr(p1, q1)}) × (${fracStr(p2, q2)})${eul(q2)} 계산하시오.`, fracStr(p1 * p2, q1 * q2, true), 2, 15); },
  () => { const d = pick([2, 4, 5, 6, 8]), k = ri(2, 12) * pick([1, -1]);           // 소수 × 정수 (정수 결과)
    if ((d * Math.abs(k)) % 10 !== 0) return null;
    const dec = (d / 10) * pick([1, -1]);
    const prod = Math.round(dec * k * 10) / 10;
    return P("calc", `(${num(dec)}) × ${wrap(k)}${eul(k)} 계산하시오.`, prod, 2, 12); },
  () => { const b = ri(2, 12) * pick([1, -1]), q = ri(2, 20) * pick([1, -1]);       // 나눗셈 (나누어떨어짐)
    return P("calc", `${wrap(b * q)} ÷ ${wrap(b)}${eul(b)} 계산하시오.`, q, 1, 8); },
  () => { const b = ri(2, 6) * pick([1, -1]), c = ri(2, 4) * pick([1, -1]), q = ri(2, 8) * pick([1, -1]); // 나눗셈 3항
    return P("calc", `${wrap(b * c * q)} ÷ ${wrap(b)} ÷ ${wrap(c)}${eul(c)} 계산하시오.`, q, 2, 12); },
  () => { const t = ri(-9, 9) || -5, b0 = ri(2, 8) * pick([1, -1]);                 // 같은 결과 choice
    const ans = `${wrap(t * b0)} ÷ ${wrap(b0)}`;
    const mk = (v) => { const bb = ri(2, 9) * pick([1, -1]); return `${wrap(v * bb)} ÷ ${wrap(bb)}`; };
    const ch = opts(ans, [mk(t + 1), mk(t - 1), mk(-t || 4), mk(t + 2), mk(t - 3)]);
    return ch && P("choice", `다음 중 계산 결과가 ${num(t)}인 것은?`, ans, 2, 15, ch); },
  () => { const a = pick([2, 3, 4, 5, 10]), n = ri(2, 4);                            // 거듭제곱
    const form = pick(["neg-in", "neg-out", "one"]);
    if (form === "one") { const k = ri(11, 199); return P("calc", `(${M}1)${sup(k)}을 계산하시오.`, k % 2 ? -1 : 1, 2, 10); }
    if (form === "neg-in") return P("calc", `(${M}${a})${sup(n)}을 계산하시오.`, Math.pow(-a, n), 2, 10);
    return P("calc", `${M}${a}${sup(n)}을 계산하시오.`, -Math.pow(a, n), 2, 10); },
  () => { const a = ri(-9, 9) || 2, b = ri(2, 6) * pick([1, -1]), c = ri(2, 6) * pick([1, -1]); // 혼합 (곱 우선)
    return P("calc", `${num(a)} ${M} ${wrap(b)} × ${wrap(c)}${eul(c)} 계산하시오.`, a - b * c, 3, 20); },
  () => { const b = ri(2, 6) * pick([1, -1]), q = ri(2, 6) * pick([1, -1]), a = ri(-9, 9) || 3; // 혼합 (÷ 우선)
    return P("calc", `${wrap(b * q)} ÷ ${wrap(b)} + ${wrap(a)}${eul(a)} 계산하시오.`, q + a, 3, 20); },
];

// ═══════════ 2. m1-fac 소인수분해 ═══════════
const PRIMES = [2, 3, 5, 7, 11, 13];
function randFac(minP = 2, maxP = 3, maxE = 3, maxVal = 500, minVal = 24) {
  for (let t = 0; t < 60; t++) {
    const ps = shuffle(PRIMES).slice(0, ri(minP, maxP)).sort((a, b) => a - b);
    const fac = {}; ps.forEach((p) => (fac[p] = ri(1, p <= 3 ? maxE : 2)));
    const v = facVal(fac);
    if (v >= minVal && v <= maxVal && ps.some((p) => fac[p] >= 2)) return fac;
  }
  return null;
}
function perturb(fac) {                                             // 값이 달라지는 지수 교란
  const f = { ...fac }; const p = +pick(Object.keys(f));
  f[p] = Math.max(1, f[p] + pick([1, -1, 1]));
  if (facVal(f) === facVal(fac)) f[p] += 1;
  return f;
}
function compositeSplit(fac) {                                      // 값은 같지만 소인수분해 아님 (2²×15 꼴)
  const v = facVal(fac);
  for (let t = 0; t < 40; t++) {
    const d = ri(4, 30);
    if (v % d === 0 && v / d > 1) {
      const rest = v / d;
      const dIsPrime = PRIMES.includes(d) || [17, 19, 23].includes(d);
      if (!dIsPrime && rest > 1) return `${rest}×${d}`;
    }
  }
  return null;
}
const facBuilders = [
  () => { const fac = randFac(); if (!fac) return null; const v = facVal(fac);      // N을 소인수분해하면
    const w = [facStr(perturb(fac)), facStr(perturb(fac)), facStr(perturb(fac))];
    const cs = compositeSplit(fac); if (cs) w.push(cs);
    const ch = opts(facStr(fac), shuffle(w));
    return ch && P("choice", `${v}${eul(v)} 소인수분해 하면?`, facStr(fac), 2, 15, ch); },
  () => { const wrongIdx = ri(0, 4); const eqs = []; let ansEq = "";                // 옳지 않은 것
    for (let i = 0; i < 5; i++) { const fac = randFac(2, 3, 3, 300); if (!fac) return null;
      const v = facVal(fac);
      if (i === wrongIdx) { const bad = perturb(fac); eqs.push(`${v} = ${facStr(bad)}`); ansEq = eqs[i]; }
      else eqs.push(`${v} = ${facStr(fac)}`); }
    if (new Set(eqs).size !== 5) return null;
    return P("choice", "다음 중 소인수분해 한 것으로 옳지 않은 것은?", ansEq, 2, 20, eqs); },
  () => { const okIdx = ri(0, 4); const eqs = []; let ansEq = "";                    // 바르게 된 것
    for (let i = 0; i < 5; i++) { const fac = randFac(2, 3, 3, 300); if (!fac) return null;
      const v = facVal(fac);
      if (i === okIdx) { eqs.push(`${v} = ${facStr(fac)}`); ansEq = eqs[i]; }
      else { const style = rand() < 0.5 ? compositeSplit(fac) : facStr(perturb(fac));
        if (!style) return null; eqs.push(`${v} = ${style}`); } }
    if (new Set(eqs).size !== 5) return null;
    return P("choice", "다음 중 소인수분해가 바르게 된 것은?", ansEq, 2, 20, eqs); },
];

// ═══════════ 3. m1-div 약수의 개수 ═══════════
const DPRIMES = [2, 3, 5, 7, 11, 13, 17];
const divBuilders = [
  () => { const k = ri(1, 4); const ps = shuffle(DPRIMES).slice(0, k).sort((a, b) => a - b);
    const fac = {}; ps.forEach((p) => (fac[p] = ri(1, k === 1 ? 7 : k === 2 ? 5 : 3)));
    const cnt = Object.values(fac).reduce((s, e) => s * (e + 1), 1);
    const diff = k <= 2 ? 1 : k === 3 ? 2 : 3;
    if (rand() < 0.8) return P("calc", `${facStr(fac)}의 약수의 개수를 구하시오.`, cnt, diff, diff === 1 ? 10 : 15);
    const ch = opts(cnt, [cnt - 1, cnt + 2, Object.values(fac).reduce((s, e) => s * e, 1), cnt + 4, cnt - 3].filter((x) => x > 0));
    return ch && P("choice", `${facStr(fac)}의 약수의 개수는?`, cnt, diff, 15, ch); },
  () => { const fac = randFac(2, 3, 3, 200, 12); if (!fac) return null;             // 자연수 제시형
    const v = facVal(fac); const cnt = Object.values(fac).reduce((s, e) => s * (e + 1), 1);
    return P("calc", `${v}의 약수의 개수를 구하시오.`, cnt, 2, 20); },
];

// ═══════════ 4·5. m1-gcd / m1-lcm ═══════════
function gcdLcmPair(nNums = 2) {
  const base = shuffle(PRIMES).slice(0, ri(2, 3)).sort((a, b) => a - b);
  const facs = [];
  for (let i = 0; i < nNums; i++) {
    const f = {}; base.forEach((p) => { if (rand() < 0.85) f[p] = ri(1, 4); });
    if (rand() < 0.3) { const extra = pick(PRIMES.filter((p) => !base.includes(p))); f[extra] = ri(1, 2); }
    if (Object.keys(f).length === 0) f[base[0]] = ri(1, 3);
    facs.push(f);
  }
  const all = [...new Set(facs.flatMap((f) => Object.keys(f).map(Number)))].sort((a, b) => a - b);
  const g = {}, l = {};
  all.forEach((p) => {
    const es = facs.map((f) => f[p] || 0);
    const mn = Math.min(...es), mx = Math.max(...es);
    if (mn > 0) g[p] = mn;
    l[p] = mx;
  });
  return { facs, g, l };
}
function gcdWrongs(g, l) {
  const w = [];
  if (Object.keys(l).length) w.push(facStr(l));                     // 반대 연산 혼동
  for (let i = 0; i < 6; i++) w.push(facStr(perturb(g)));           // 지수 교란 다수
  const mix = { ...g }; const extra = Object.keys(l).find((p) => !(p in g));
  if (extra) { mix[extra] = 1; w.push(facStr(mix)); }
  const swap = { ...g }; const ks = Object.keys(swap);
  if (ks.length >= 2) { const t = swap[ks[0]]; swap[ks[0]] = swap[ks[1]]; swap[ks[1]] = t; w.push(facStr(swap)); }
  return w;
}
function mkGL(kind) {
  return () => {
    const nNums = rand() < 0.25 ? 3 : 2;
    const { facs, g, l } = gcdLcmPair(nNums);
    const target = kind === "gcd" ? g : l;
    if (Object.keys(target).length === 0) return null;
    if (facVal(target) > 99999) return null;
    const plain = rand() < 0.2;                                                     // 자연수 하나 섞기
    const nums = facs.map((f, i) => (plain && i === 0 && facVal(f) <= 300 ? String(facVal(f)) : facStr(f)));
    const label = kind === "gcd" ? "최대공약수" : "최소공배수";
    const head = `${nNums === 3 ? "세" : "두"} 수 ${nums.join(", ")}의 ${label}`;
    if (rand() < 0.3) return P("calc", `${head}를 구하시오.`, facVal(target), nNums === 3 ? 3 : 2, nNums === 3 ? 25 : 18);
    const wrongs = kind === "gcd" ? gcdWrongs(g, l) : gcdWrongs(l, g);
    const ch = opts(facStr(target), wrongs);
    return ch && P("choice", `${head}는?`, facStr(target), nNums === 3 ? 3 : 2, nNums === 3 ? 25 : 18, ch);
  };
}

// ═══════════ 6. m1-expr 문자의 사용과 식의 계산 ═══════════
const VARS = ["x", "a", "b", "y"];
const exprBuilders = [
  () => { const v = pick(VARS), k = ri(2, 9) * pick([1, -1]), n = ri(2, 9) * pick([1, -1]); // 단항식×수
    return P("calc", `(${num(k)}${v}) × ${wrap(n)}${eul(n)} 계산하시오.`, linAns(k * n, 0, v), 1, 8); },
  () => { const v = pick(VARS), q = ri(2, 7), n = ri(2, 5), coefN = q * ri(1, 4);   // 분수x × 정수
    const p = ri(1, q - 1) * pick([1, -1]); const res = p * coefN / q;
    if (!Number.isInteger(res)) return null;
    return P("calc", `(${fracStr(p, q)})${v} × ${coefN}${eul(coefN)} 계산하시오.`, linAns(res, 0, v), 2, 12); },
  () => { const v = pick(VARS), q = ri(2, 7), p = ri(1, q * 2) * pick([1, -1]);     // 단항식 ÷ 분수
    if (Math.abs(p) % q === 0) return null;
    const k = p * ri(1, 3) * pick([1, -1]); if (k === 0) return null;
    const res = k * q / p; if (!Number.isInteger(res)) return null;
    return P("calc", `(${num(k)}${v}) ÷ (${fracStr(p, q)})${eul(q)} 계산하시오.`, linAns(res, 0, v), 2, 15); },
  () => { const v = pick(VARS), n = ri(2, 9), q = ri(2, 9) * n;                     // 단항식 ÷ 정수
    return P("calc", `${q}${v} ÷ ${n}${eul(n)} 계산하시오.`, linAns(q / n, 0, v), 1, 8); },
  () => { const a = ri(2, 6) * pick([1, -1]), b = ri(1, 9) * pick([1, -1]), k = ri(2, 5) * pick([1, -1]); // k(ax+b)
    return P("calc", `${num(k)}(${linQ(a, b)})${eul(b)} 계산하시오.`, linAns(k * a, k * b), 2, 12); },
  () => { const a = ri(2, 8) * pick([1, -1]), b = ri(1, 12) * pick([1, -1]), d = pick([2, 3, 4]); // (ax+b)÷정수
    const A = a * d, B = b * d;
    const ch = opts(linAns(a, b), [linAns(a, -b), linAns(-a, b), linAns(a * d, b), linAns(a, b * d)]);
    return ch && P("choice", `(${linQ(A, B)}) ÷ ${d}${eul(d)} 간단히 하면?`, linAns(a, b), 2, 15, ch); },
  () => { const k = ri(2, 4) * pick([1, -1]), m = ri(2, 4) * pick([1, -1]);          // 일차식 덧뺄셈
    const a = ri(1, 5) * pick([1, -1]), b = ri(1, 6) * pick([1, -1]);
    const c = ri(1, 5) * pick([1, -1]), d = ri(1, 6) * pick([1, -1]);
    const X = k * a + m * c, C = k * b + m * d; if (X === 0) return null;
    return P("calc", `${num(k)}(${linQ(a, b)}) ${m < 0 ? "−" : "+"} ${num(Math.abs(m))}(${linQ(c, d)})를 계산하시오.`, linAns(X, C), 3, 20); },
  () => { const a = ri(1, 6) * pick([1, -1]), b = ri(1, 8) * pick([1, -1]);          // (…) − (…)
    const c = ri(1, 6) * pick([1, -1]), d = ri(1, 8) * pick([1, -1]);
    const X = a - c, C = b - d; if (X === 0) return null;
    return P("calc", `(${linQ(a, b)}) ${M} (${linQ(c, d)})를 계산하시오.`, linAns(X, C), 2, 15); },
  () => { const a = ri(2, 9) * pick([1, -1]), b = ri(1, 9) * pick([1, -1]);          // 계수·상수항
    const what = pick([["x의 계수", a], ["상수항", b], ["x의 계수와 상수항의 합", a + b]]);
    return P("calc", `일차식 ${linQ(a, b)}에서 ${what[0]}${eul(what[0])} 구하시오.`, what[1], 1, 10); },
];

// ═══════════ 7. m1-eq1 일차방정식 (등식·성질) ═══════════
const eq1Builders = [
  () => { const A = ri(2, 5), B = ri(1, 9), C = ri(2, 9), D = ri(2, 4);              // 문장→등식
    const ans = `${A}x + ${B} = ${D}(${C} ${M} x)`;
    const ch = opts(ans, [`${A}x + ${B} = ${C} ${M} ${D}x`, `${A}(x + ${B}) = ${D}(${C} ${M} x)`,
      `${A}x ${M} ${B} = ${D}(${C} ${M} x)`, `${A}x + ${B} = ${C}(${D} ${M} x)`]);
    return ch && P("choice", `'x의 ${A}배에 ${B}${eul(B)} 더한 수는 ${C}에서 x를 뺀 수의 ${D}배와 같다.'를 등식으로 바르게 나타낸 것은?`, ans, 2, 20, ch); },
  () => { const a = ri(3, 9), L = 2 * (a + ri(3, 12));                                // 둘레→등식
    const ans = `2(${a} + x) = ${L}`;
    const ch = opts(ans, [`${a} + x = ${L}`, `${a}x = ${L}`, `2${a} + x = ${L}`, `${a} + 2x = ${L}`]);
    return ch && P("choice", `'가로의 길이가 ${a} cm, 세로의 길이가 x cm인 직사각형의 둘레의 길이는 ${L} cm이다.'를 등식으로 나타내면?`, ans, 2, 18, ch); },
  () => { const a = ri(3, 9), S = a * ri(3, 12);                                      // 넓이→등식
    const ans = `${a}x = ${S}`;
    const ch = opts(ans, [`${a} + x = ${S}`, `2(${a} + x) = ${S}`, `x/${a} = ${S}`, `${a}x + ${a} = ${S}`]);
    return ch && P("choice", `'가로의 길이가 ${a}, 세로의 길이가 x인 직사각형의 넓이는 ${S}이다.'를 등식으로 나타내면?`, ans, 1, 15, ch); },
  () => { const A = ri(3, 8), B = ri(1, 9), C = A + ri(1, 3), D = ri(1, 9);          // 나누어주기
    const ans = `${A}x + ${B} = ${C}x ${M} ${D}`;
    const ch = opts(ans, [`${A}x ${M} ${B} = ${C}x + ${D}`, `${A}x + ${B} = ${C}x + ${D}`,
      `${A}x ${M} ${B} = ${C}x ${M} ${D}`, `${C}x + ${B} = ${A}x ${M} ${D}`]);
    return ch && P("choice", `'x명의 학생들에게 사탕을 나누어 주는 데 한 명에게 ${A}개씩 나누어 주면 ${B}개가 남고, ${C}개씩 나누어 주면 ${D}개가 부족하다.'를 등식으로 나타내면?`, ans, 3, 25, ch); },
  () => { const a = ri(2, 9), b = ri(1, 9) * pick([1, -1]), x0 = ri(-5, 5);          // 해 판별 OX
    const isSol = rand() < 0.5;
    const rhs = isSol ? a * x0 + b : a * x0 + b + pick([1, -1, 2, -2]);
    return P("ox", `x = ${num(x0)}은 방정식 ${linQ(a, b)} = ${num(rhs)}의 해이다.`, isSol ? "O" : "X", 1, 12); },
  () => { const stmts = [                                                             // 등식의 성질 OX
      ["a = b이면 a + c = b + c이다.", "O"], ["a = b이면 a − c = b − c이다.", "O"],
      ["a = b이면 ac = bc이다.", "O"], ["a = b이면 a/c = b/c이다. (c는 0이 아님)", "O"],
      ["a + c = b + c이면 a = b이다.", "O"], ["ac = bc이면 항상 a = b이다.", "X"],
      ["a = b이면 a + 1 = b − 1이다.", "X"], ["a/2 = b/3이면 3a = 2b이다.", "O"],
      ["2a = 3b이면 a/3 = b/2이다.", "O"], ["a − 5 = b − 5이면 a = b이다.", "O"],
      ["a = 2b이면 a − 2 = 2(b − 1)이다.", "O"], ["a = b이면 −a = −b이다.", "O"],
    ]; const s = pick(stmts);
    return P("ox", s[0].replaceAll("−", M), s[1], 2, 12); },
  () => { const p = ri(2, 6), q = ri(1, 9) * pick([1, -1]);                           // 항등식 조건
    return P("calc", `등식 ax + b = ${linQ(p, q)}가 x에 대한 항등식일 때, a + b의 값을 구하시오.`, p + q, 2, 15); },
];

// ═══════════ 8. m1-eq2 일차방정식의 풀이 ═══════════
function solStr(n, d) { return fracStr(n, d, true); }
const eq2Builders = [
  () => { const a = ri(2, 9) * pick([1, -1]), x0 = ri(-9, 9) || 3, b = ri(-12, 12);  // ax+b=c (정수해)
    return P("calc", `방정식 ${linQ(a, b)} = ${num(a * x0 + b)}의 해를 구하시오.`, ansN(x0), 1, 10); },
  () => { const a = ri(2, 9), d = pick([2, 3, 4, 5]);                                 // ax+b=c (분수해)
    const n = ri(1, d * 3) * pick([1, -1]); if (n % d === 0) return null;
    const b = ri(-9, 9); const c = a * n + b * d;                                    // a(n/d)+b = c/d → 양변 d배 꼴 회피: ax+b=c with c 분수 금지
    if (c % d !== 0) { // (a x0 + b) 가 정수가 아니면 스킵
      return null; }
    return P("calc", `방정식 ${linQ(a, b)} = ${num(c / d)}의 해를 구하시오.`, solStr(n, d), 2, 15); },
  () => { const x0 = ri(-8, 8) || 2, a = ri(2, 9) * pick([1, -1]);                    // ax+b=cx+d
    let c = ri(-9, 9); if (c === a || c === 0) c = a - ri(1, 3);
    const b = ri(-12, 12), d = (a - c) * x0 + b;
    if (Math.abs(d) > 40) return null;
    return P("calc", `방정식 ${linQ(a, b)} = ${linQ(c, d)}의 해를 구하시오.`, ansN(x0), 2, 12); },
  () => { const den = pick([2, 3, 4, 5, 6]), nu = ri(1, den * 4) * pick([1, -1]);     // 분수해 양변형
    if (nu % den === 0) return null;
    const a = den * ri(1, 2), c = a - den;                                            // (a−c) = den → x0 = (d−b)/den
    const b = ri(-9, 9), d = nu + b;
    if (c === 0 || Math.abs(d) > 30) return null;
    return P("calc", `방정식 ${linQ(a, b)} = ${linQ(c, d)}의 해를 구하시오.`, solStr(nu, den), 2, 15); },
  () => { const x0 = ri(-7, 7) || 2, k = ri(2, 5) * pick([1, -1]), a = ri(1, 6) * pick([1, -1]); // k(x+a)+m=c
    const m = ri(-9, 9), c = k * (x0 + a) + m;
    if (Math.abs(c) > 60) return null;
    return P("calc", `방정식 ${num(k)}(x ${a >= 0 ? "+ " + a : M + " " + -a}) ${m >= 0 ? "+ " + m : M + " " + -m} = ${num(c)}의 해를 구하시오.`, ansN(x0), 2, 15); },
  () => { const x0 = ri(-6, 6) || 1, k = ri(2, 4), a = ri(1, 5) * pick([1, -1]);      // 양변 괄호
    const m2 = ri(2, 4), b = ri(1, 5) * pick([1, -1]);
    const L = k * (x0 + a), R = m2 * (x0 + b), diff = L - R;                           // k(x+a) − m(x+b) = diff
    if (k === m2) return null;
    return P("calc", `방정식 ${k}(x ${a >= 0 ? "+ " + a : M + " " + -a}) ${M} ${m2}(x ${b >= 0 ? "+ " + b : M + " " + -b}) = ${num(diff)}의 해를 구하시오.`, ansN(x0), 3, 20); },
  () => { const p = pick([2, 3, 4, 5]), b = ri(1, 6) * pick([1, -1]), c = ri(-6, 6);  // x/p + b = c
    const x0 = p * (c - b); if (x0 === 0 || Math.abs(x0) > 40) return null;
    return P("calc", `방정식 x/${p} ${b >= 0 ? "+ " + b : M + " " + -b} = ${num(c)}의 해를 구하시오.`, ansN(x0), 2, 15); },
  () => { const p = pick([2, 3, 4]), a = ri(1, 6) * pick([1, -1]), r = ri(-5, 5);     // (x−a)/p = r
    const x0 = p * r + a;
    return P("calc", `방정식 (x ${a >= 0 ? M + " " + a : "+ " + -a})/${p} = ${num(r)}의 해를 구하시오.`, ansN(x0), 2, 15); },
  () => { let A = ri(2, 8), C = ri(1, 8); if (A === C) C = A - 1; if (C === 0) C = 1; // 소수 계수
    const x0 = ri(-6, 6) || 2;
    const Bt = ri(-9, 9), Dt = (A - C) * x0 + Bt; if (Math.abs(Dt) > 9 || Math.abs(Bt) > 9) return null;
    return P("calc", `방정식 0.${A}x ${Bt >= 0 ? "+ 0." + Bt : M + " 0." + -Bt} = 0.${C}x ${Dt >= 0 ? "+ 0." + Dt : M + " 0." + -Dt}의 해를 구하시오.`.replaceAll("0.-", "0."), ansN(x0), 3, 20); },
  () => { const x0 = ri(-6, 6) || -2, a = ri(2, 7) * pick([1, -1]), b = ri(-9, 9);    // 해 고르기 choice
    let c = a - ri(1, 4) * pick([1, -1]); if (c === a) c = a - 2; if (c === 0) c = 1;
    const d = (a - c) * x0 + b; if (Math.abs(d) > 40) return null;
    const ch = opts(`x = ${x0}`, [`x = ${x0 + 1}`, `x = ${x0 - 1}`, `x = ${-x0 || 5}`, `x = ${x0 + 2}`]);
    return ch && P("choice", `일차방정식 ${linQ(a, b)} = ${linQ(c, d)}의 해는?`, `x = ${x0}`, 2, 15, ch); },
];

// ═══════════ 9. m1-prop1 정비례·반비례 식 구하기 (좌표형) ═══════════
function niceSlope() { const t = pick([1, 1, 2, 3]), s = ri(1, 5) * pick([1, -1]); const g = gcd(Math.abs(s), t); return [s / g, t / g]; }
const prop1Builders = [
  () => { const [s, t] = niceSlope(); const p = t * ri(1, 4), q = s * (p / t);        // 원점+두 점 → k
    const k = t * ri(1, 5) * pick([1, -1]); if (k === p) return null;
    const r = s * k / t;
    return P("calc", `점 (${num(p)}, ${num(q)})과 원점을 지나는 직선이 점 (k, ${num(r)})를 지날 때, k의 값을 구하시오.`, ansN(k), 2, 18); },
  () => { const [s, t] = niceSlope(); const p = t * ri(1, 4) * pick([1, -1]), q = s * p / t; // a+b 조합
    const x1 = t * ri(1, 4) * pick([1, -1]), y2 = s * ri(1, 4) * pick([1, -1]);
    const aVal = s * x1 / t, bVal = y2 * t / s;
    if (!Number.isInteger(aVal) || !Number.isInteger(bVal)) return null;
    const kind = pick([["a + b", aVal + bVal], ["a − b", aVal - bVal], ["ab", aVal * bVal]]);
    return P("calc", `원점과 점 (${num(p)}, ${num(q)})를 지나는 직선이 두 점 (${num(x1)}, a), (b, ${num(y2)})를 지날 때, ${kind[0].replace("−", M)}의 값을 구하시오.`, kind[1], 3, 25); },
  () => { const [s, t] = niceSlope(); const p = t * ri(1, 4) * pick([1, -1]), q = s * p / t; // 세 점 일직선
    const r = t * ri(1, 5) * pick([1, -1]); if (r === p) return null;
    const k = s * r / t;
    return P("calc", `세 점 O(0, 0), A(${num(p)}, ${num(q)}), B(${num(r)}, k)가 한 직선 위에 있을 때, k의 값을 구하시오.`, ansN(k), 2, 18); },
  () => { const a = ri(2, 5) * pick([1, -1]); const p = ri(1, 4), q = a * p;          // 관계식 choice
    const ans = `y = ${num(a)}x`;
    const alt = [a + 1, a - 1, -a, a + 2, a + 3, a - 3].filter((v) => Math.abs(v) >= 2 && v !== a);
    const ch = opts(ans, alt.map((v) => `y = ${num(v)}x`));
    return ch && P("choice", `그래프가 원점을 지나는 직선인 x와 y 사이의 관계식이 있다. 그래프가 점 (${p}, ${num(q)})을 지날 때, x와 y 사이의 관계식은?`, ans, 1, 15, ch); },
  () => { const [s, t0] = niceSlope(); if (Math.abs(s) === t0) return null;           // 조건 박스형 choice
    const p = t0 * ri(1, 4) * pick([1, -1]), q = s * p / t0;
    const slope = fracStr(s, t0);
    const px = (f) => (f.includes("/") ? `(${f})` : f === "1" ? "" : f === M + "1" ? M : f);
    const ans = `y = ${px(slope)}x`;
    const ch = opts(ans, [`y = ${px(fracStr(-s, t0))}x`, `y = ${px(fracStr(t0, s))}x`, `y = ${px(fracStr(s, t0 + 1))}x`, `xy = ${num(p * q)}`]);
    return ch && P("choice", `다음 조건을 모두 만족하는 x와 y 사이의 관계식은?\n(가) y는 x에 정비례한다.\n(나) 그래프가 점 (${num(p)}, ${num(q)})를 지난다.`, ans, 2, 20, ch); },
  () => { const A = ri(2, 6) * pick([1, -1]) * ri(1, 4);                              // 반비례: 상수 구하기
    const p = pick([1, 2, 3, 4, 6].filter((d) => A % d === 0)) * pick([1, -1]);
    const q = A / p; const r = pick([1, 2, 3, 4, 6, 8, 12].filter((d) => A % d === 0)) * pick([1, -1]);
    if (r === p) return null;
    return P("calc", `점 (${num(p)}, ${num(q)})를 지나는 반비례 관계 y = a/x의 그래프가 점 (${num(r)}, k)를 지날 때, k의 값을 구하시오.`, ansN(A / r), 2, 20); },
];

// ═══════════ 10. m1-prop2 정비례·반비례 관계식 (서술형) ═══════════
const prop2Builders = [
  () => { const [s, t] = niceSlope(); const p = t * ri(1, 4) * pick([1, -1]), q = s * p / t; // 정비례 값
    const r = ri(1, 12) * pick([1, -1]); if (r === p || r === 0) return null;
    const y = fracStr(s * r, t, true);
    return P("calc", `y가 x에 정비례하고 x = ${num(p)}일 때 y = ${num(q)}이다. x = ${num(r)}일 때, y의 값을 구하시오.`, y, 2, 18); },
  () => { const a = ri(2, 5) * pick([1, -1]); const p = ri(1, 4) * pick([1, -1]), q = a * p; // 관계식 choice (동치식 혼란지)
    const ans = `y = ${num(a)}x`;
    const inv = fracStr(1, a);
    const ch = opts(ans, [`xy = ${num(p * q)}`, `y = ${inv.includes("/") ? `(${inv})` : inv}x`, `y = ${num(a)}/x`, `y = ${num(-a)}x`]);
    return ch && P("choice", `y는 x에 정비례하고 x = ${num(p)}일 때 y = ${num(q)}이다. x와 y 사이의 관계식은?`, ans, 2, 18, ch); },
  () => { const A = pick([6, 8, 12, 12, 18, 24, 36]) * pick([1, -1]);                 // 반비례 값
    const p = pick([1, 2, 3, 4, 6].filter((d) => Math.abs(A) % d === 0)) * pick([1, -1]);
    const q = A / p; const r = pick([2, 3, 4, 6, 8, 9, 12].filter((d) => Math.abs(A) % d === 0)) * pick([1, -1]);
    if (r === p) return null;
    return P("calc", `y가 x에 반비례하고 x = ${num(p)}일 때 y = ${num(q)}이다. x = ${num(r)}일 때, y의 값을 구하시오.`, ansN(A / r), 2, 18); },
  () => { const A = pick([6, 8, 10, 12, 18, 20, 24]) * pick([1, -1]);                 // 반비례 관계식 choice
    const p = pick([1, 2, 3, 4].filter((d) => Math.abs(A) % d === 0)) * pick([1, -1]);
    const q = A / p;
    const ans = `y = ${num(A)}/x`;
    const alt2 = Math.abs(p) >= 2 ? `y = ${num(p)}x` : `y = ${num(A + 2)}/x`;
    const ch = opts(ans, [`y = ${num(A)}x`, `y = ${num(-A)}/x`, `y = x/${Math.abs(A)}`, alt2]);
    return ch && P("choice", `y는 x에 반비례하고 x = ${num(p)}일 때 y = ${num(q)}이다. x와 y 사이의 관계식은?`, ans, 2, 18, ch); },
  () => { const a = ri(2, 6), p = ri(2, 6), q = a * p, r2 = a * ri(7, 12);            // 배수 서술형
    return P("calc", `x의 값이 2배, 3배, 4배, …가 될 때 y의 값도 2배, 3배, 4배, …가 되고, x = ${p}일 때 y = ${q}이다. y = ${r2}일 때, x의 값을 구하시오.`, ansN(r2 / a), 2, 20); },
  () => { const kind = pick([["정비례", "y/x"], ["반비례", "xy"]]);                    // 개념 빈칸
    return P("calc", `두 변수 x, y에 대하여 y가 x에 ${kind[0]}하면 ${kind[1]} (x ≠ 0)의 값은 항상 일정하다. 이때 빈칸에 알맞은 식을 쓰시오.`.replace(kind[1], "(빈칸)"), kind[1], 1, 10); },
  () => { const a = ri(2, 4) * pick([1, -1]);                                          // A+B+C 조합
    const xs = shuffle([1, 2, 3, 4, 5]).slice(0, 3);
    const vals = xs.map((x) => a * x);
    return P("calc", `y = ${num(a)}x에서 x = ${xs[0]}일 때 y = A, x = ${xs[1]}일 때 y = B, x = ${xs[2]}일 때 y = C이다. A + B + C의 값을 구하시오.`, vals[0] + vals[1] + vals[2], 2, 20); },
];

// ═══════════ 11. mono-op 단항식의 곱셈과 나눗셈 (지수법칙) ═══════════
const monoBuilders = [
  () => { const p1 = ri(1, 4), P1 = p1 + ri(1, 5);                                     // 미지수 지수 x+y
    const t1 = ri(1, 4), T1 = t1 + ri(1, 6);
    const x = T1 - t1, y = P1 - p1; const ans = x + y;
    const q = `a${sup(p1)}bˣ × aʸb${sup(t1)} = a${sup(P1)}b${sup(T1)}일 때, x + y의 값은?`;
    const ch = opts(ans, [ans + 1, ans - 1, ans + 2, ans - 2, ans + 3].filter((v) => v > 0));
    return ch && P("choice", q, ans, 2, 15, ch); },
  () => { const p = ri(2, 4), q = ri(2, 3), r = ri(2, 3), s = ri(1, 3), t = ri(1, 4);  // 성립 조건 a+b
    const a = p + s, b = q * r + t;
    return P("calc", `x${sup(p)} × (y${sup(q)})${sup(r)} × x${sup(s)} × y${sup(t)} = xᵃyᵇ이 성립할 때, 두 자연수 a, b에 대하여 a + b의 값을 구하시오.`, a + b, 2, 15); },
  () => { const e = pick([3, 5, 7]), c = pick([2, 3]), r = pick([2, 3]), s = pick([2, 3]); // 복합 정리 choice
    const p = ri(1, 3), q = ri(1, 3);
    const coef = Math.pow(-1, e) * Math.pow(-c, r) * Math.pow(-2, s);
    const xE = p, yE = q * r;
    const ans = monoStr(coef, { x: xE, y: yE });
    const w = [monoStr(-coef, { x: xE, y: yE }), monoStr(coef, { x: xE, y: q + r }),
      monoStr(Math.pow(-1, e) * (-c * r) * Math.pow(-2, s), { x: xE, y: yE }), monoStr(coef * 2, { x: xE, y: yE })];
    const ch = opts(ans, w);
    return ch && P("choice", `(${M}1)${sup(e)} × x${sup(p)}(${M}${c}y${sup(q)})${sup(r)} × (${M}2)${sup(s)}을 계산하면?`, ans, 3, 25, ch); },
  () => { const c = pick([2, 3]), p = ri(1, 3), q = ri(1, 2), k = pick([2, 3]);        // 계수 묻기
    const d = pick([2, 3]), rr = ri(1, 2), ss = ri(1, 2), m2 = 2;
    const coef = Math.pow(c, k) * Math.pow(-d, m2);
    return P("calc", `(${c}x${sup(p)}y${sup(q)})${sup(k)} × (${M}${d}xy${sup(rr)})${sup(m2)}을 간단히 했을 때, 계수를 구하시오.`, coef, 2, 18); },
  () => { const c = pick([2, 3]), p = ri(2, 4), q = ri(1, 3), k = pick([2, 3]), m2 = ri(1, 2), r2 = ri(1, 3); // 지수 묻기
    const which = pick(["x", "y"]);
    const xE = p * k + m2, yE = q * k + r2 * m2;
    return P("calc", `(${c}x${sup(p)}y${sup(q)})${sup(k)} × (xy${sup(r2)})${sup(m2)}을 간단히 했을 때, ${which}의 지수를 구하시오.`, which === "x" ? xE : yE, 2, 15); },
  () => { const b0 = pick([2, 3, 5]), s = ri(2, 6), t = ri(2, 5);                       // aˢ×aᵗ=aⁿ → n
    return P("calc", `${b0}${sup(s)} × ${b0}${sup(t)} = ${b0}ⁿ일 때, 자연수 n의 값을 구하시오.`, s + t, 1, 10); },
  () => { const v = pick(["a", "x"]), c1 = ri(2, 6), e1 = ri(3, 6), c2 = pick([2, 3]), e2 = ri(1, e1 - 2); // 나눗셈 (답 지수≤1)
    if (c1 % c2 !== 0) return null;
    const rc = c1 / c2, re = e1 - e2; if (re > 1) return null;
    return P("calc", `${c1}${v}${sup(e1)} ÷ ${c2}${v}${sup(e2)}을 계산하시오.`, linAns(rc, 0, v), 2, 12); },
];


// 이변수(+상수) 식: X·v1 + Y·v2 + C
function lin2Q(X, Y, C, v1, v2) {
  const parts = [];
  if (X) parts.push(X === 1 ? v1 : X === -1 ? M + v1 : `${num(X)}${v1}`);
  if (Y) parts.push((Y > 0 && parts.length ? "+ " : Y < 0 ? M + " " : "") + (Math.abs(Y) === 1 ? v2 : `${Math.abs(Y)}${v2}`));
  if (C) parts.push((C > 0 && parts.length ? "+ " : C < 0 ? M + " " : "") + Math.abs(C));
  return parts.join(" ") || "0";
}
function lin2A(X, Y, C, v1, v2) {
  let s = "";
  if (X) s += (X === 1 ? "" : X === -1 ? "-" : X) + v1;
  if (Y) s += (Y > 0 ? "+" : "-") + (Math.abs(Y) === 1 ? "" : Math.abs(Y)) + v2;
  if (C) s += (C > 0 ? "+" : "") + C;
  return s || "0";
}

// ═══════════ 1. m2-poly1 다항식의 덧셈과 뺄셈 ═══════════
const VPAIRS = [["a", "b"], ["x", "y"]];
const poly1Builders = [
  () => { const [v1, v2] = pick(VPAIRS);                                       // (pa+qb) − (ra+sb) choice
    const p = ri(1, 6) * pick([1, -1]), q = ri(1, 6) * pick([1, -1]);
    const r = ri(1, 6) * pick([1, -1]), s = ri(1, 6) * pick([1, -1]);
    const X = p - r, Y = q - s; if (!X || !Y) return null;
    const ans = lin2Q(X, Y, 0, v1, v2);
    const ch = opts(ans, [lin2Q(p + r, q + s, 0, v1, v2), lin2Q(X, -Y, 0, v1, v2),
      lin2Q(-X, Y, 0, v1, v2), lin2Q(X, q + s, 0, v1, v2), lin2Q(p + r, Y, 0, v1, v2)]);
    return ch && P("choice", `(${lin2Q(p, q, 0, v1, v2)}) ${M} (${lin2Q(r, s, 0, v1, v2)})${eul(v2)} 간단히 하면?`, ans, 2, 15, ch); },
  () => { const [v1, v2] = pick(VPAIRS);                                       // 덧셈 calc
    const p = ri(1, 7) * pick([1, -1]), q = ri(1, 7) * pick([1, -1]);
    const r = ri(1, 7) * pick([1, -1]), s = ri(1, 7) * pick([1, -1]);
    const X = p + r, Y = q + s; if (!X || !Y) return null;
    return P("calc", `(${lin2Q(p, q, 0, v1, v2)}) + (${lin2Q(r, s, 0, v1, v2)})${eul(v2)} 간단히 하시오.`, lin2A(X, Y, 0, v1, v2), 1, 12); },
  () => { const k = ri(2, 3), m = ri(2, 3);                                    // k(…)−m(…) 상수 포함 choice
    const [v1, v2] = pick(VPAIRS);
    const p = ri(1, 5) * pick([1, -1]), q = ri(1, 5) * pick([1, -1]), c = ri(1, 4) * pick([1, -1]);
    const r = ri(1, 5) * pick([1, -1]), s = ri(1, 5) * pick([1, -1]), d = ri(1, 4) * pick([1, -1]);
    const X = k * p - m * r, Y = k * q - m * s, C = k * c - m * d;
    if (!X || !Y) return null;
    const ans = lin2Q(X, Y, C, v1, v2);
    const ch = opts(ans, [lin2Q(X, Y, -C, v1, v2), lin2Q(-X, Y, C, v1, v2),
      lin2Q(X, -Y, C, v1, v2), lin2Q(k * p + m * r, Y, C, v1, v2), lin2Q(X, k * q + m * s, C, v1, v2)]);
    return ch && P("choice", `${k}(${lin2Q(p, q, c, v1, v2)}) ${M} ${m}(${lin2Q(r, s, d, v1, v2)})${eul(Math.abs(d))} 간단히 한 것은?`, ans, 3, 20, ch); },
  () => { const a1 = ri(1, 6) * pick([1, -1]), b1 = ri(1, 9) * pick([1, -1]);  // 일변수 calc (5x−4)+(2x−3)
    const a2 = ri(1, 6) * pick([1, -1]), b2 = ri(1, 9) * pick([1, -1]);
    const op = pick(["+", M]);
    const X = op === "+" ? a1 + a2 : a1 - a2, C = op === "+" ? b1 + b2 : b1 - b2;
    if (!X) return null;
    return P("calc", `(${linQ(a1, b1)}) ${op} (${linQ(a2, b2)})${eul(Math.abs(b2))} 계산하시오.`, linA(X, C), 1, 10); },
  () => { const k = ri(2, 3), m = ri(2, 4);                                    // 3(−2x+1)−4(x+3) 일변수 choice
    const a = ri(1, 4) * pick([1, -1]), b = ri(1, 4) * pick([1, -1]);
    const c = ri(1, 4) * pick([1, -1]), d = ri(1, 4) * pick([1, -1]);
    const X = k * a - m * c, C = k * b - m * d; if (!X) return null;
    const ans = linQ(X, C);
    const ch = opts(ans, [linQ(X, -C), linQ(-X, C), linQ(k * a + m * c, C), linQ(X, k * b + m * d)]);
    return ch && P("choice", `${k}(${linQ(a, b)}) ${M} ${m}(${linQ(c, d)})${eul(Math.abs(d))} 간단히 하면?`, ans, 2, 15, ch); },
];

// ═══════════ 2. m2-poly2 다항식의 곱셈과 나눗셈 ═══════════
// 전개식 표기: c1·x² + c2·xy + c3·x  등 — 항 배열 [[계수, "x²"], …] 로 처리
function termsQ(ts) {
  const parts = [];
  for (const [c, v] of ts) {
    if (!c) continue;
    const body = Math.abs(c) === 1 && v ? v : `${Math.abs(c)}${v}`;
    parts.push(parts.length === 0 ? (c < 0 ? M : "") + body : (c < 0 ? M + " " : "+ ") + body);
  }
  return parts.join(" ") || "0";
}
const poly2Builders = [
  () => { const k = ri(2, 4) * pick([1, -1]);                                  // kx(ax+by+c) 전개 choice
    const a = ri(1, 4) * pick([1, -1]), b = ri(1, 4) * pick([1, -1]), c = ri(1, 5) * pick([1, -1]);
    const T = [[k * a, "x²"], [k * b, "xy"], [k * c, "x"]];
    const ans = termsQ(T);
    const ch = opts(ans, [termsQ([[k * a, "x²"], [-k * b, "xy"], [k * c, "x"]]),
      termsQ([[-k * a, "x²"], [k * b, "xy"], [-k * c, "x"]]),
      termsQ([[k * a, "x²"], [k * b, "xy"], [-k * c, "x"]]),
      termsQ([[k * a, "x²"], [k * b, "y"], [k * c, "x"]])]);
    return ch && P("choice", `${num(k)}x(${lin2Q(a, b, c, "x", "y")})${eul(Math.abs(c))} 전개하면?`, ans, 2, 18, ch); },
  () => { const q = pick([2, 3]), p = ri(1, q * 2 - 1) * pick([1, -1]);        // −(p/q)x(ax²−bx+c) choice
    if (Math.abs(p) % q === 0) return null;
    const a = q * ri(1, 2), b = q * ri(1, 3), c = q * 1;                       // q의 배수로 계수 정수화
    const s1 = -p * a / q, s2 = p * b / q, s3 = -p * c / q;                    // (−p/q)x × (ax² − bx + c)
    const T = [[s1, "x³"], [s2, "x²"], [s3, "x"]];
    const ans = termsQ(T);
    const ch = opts(ans, [termsQ([[-s1, "x³"], [s2, "x²"], [-s3, "x"]]),
      termsQ([[s1, "x³"], [-s2, "x²"], [s3, "x"]]),
      termsQ([[-s1, "x³"], [-s2, "x²"], [-s3, "x"]]),
      termsQ([[s1, "x²"], [s2, "x"], [s3, ""]])]);
    return ch && P("choice", `${M}${Math.abs(p)}/${q}x(${termsQ([[a, "x²"], [-b, "x"], [c, ""]])})${eul(c)} 간단히 하면?`.replace("−" + Math.abs(p), (p < 0 ? "" : M) + Math.abs(p)), ans, 3, 22, ch); },
  () => { const k = ri(2, 4) * pick([1, -1]);                                  // 전개식의 계수 calc
    const a = ri(1, 4) * pick([1, -1]), b = ri(1, 4) * pick([1, -1]), c = ri(1, 5) * pick([1, -1]);
    const which = pick([["x²", k * a], ["xy", k * b], ["x", k * c]]);
    return P("calc", `${num(k)}x(${lin2Q(a, b, c, "x", "y")})${eul(Math.abs(c))} 전개한 식에서 ${which[0]}의 계수를 구하시오.`, which[1], 2, 15); },
  () => { const m = ri(2, 3) * pick([1, -1]);                                  // −2a(a−4b+3) 전개 choice
    const a = 1, b = ri(1, 5) * pick([1, -1]), c = ri(1, 5) * pick([1, -1]);
    const T = [[m * a, "a²"], [m * b, "ab"], [m * c, "a"]];
    const ans = termsQ(T);
    const ch = opts(ans, [termsQ([[m * a, "a²"], [-m * b, "ab"], [m * c, "a"]]),
      termsQ([[m * a, "a²"], [m * b, "ab"], [-m * c, "a"]]),
      termsQ([[-m * a, "a²"], [m * b, "ab"], [m * c, "a"]]),
      termsQ([[m * a, "a²"], [-m * b, "ab"], [-m * c, "a"]])]);
    return ch && P("choice", `${num(m)}a(${lin2Q(a, b, c, "a", "b")})${eul(Math.abs(c))} 간단히 하면?`, ans, 2, 18, ch); },
  () => { const k = ri(2, 4), a = ri(1, 5) * pick([1, -1]), b = ri(1, 6) * pick([1, -1]); // (다항식)÷단항식 calc
    const v = pick(["x", "a"]);
    return P("calc", `(${termsQ([[k * a, v + "²"], [k * b, v]])}) ÷ ${k}${v}${eul(v)} 계산하시오.`, linA(a, b, v), 2, 15); },
  () => { const wrongCnt = 4;                                                   // 옳은 것 choice
    const mk = (correct) => { const m2 = ri(2, 3) * pick([1, -1]);
      const b = ri(1, 4) * pick([1, -1]), c = ri(1, 4);
      const L = `${num(m2)}a(${lin2Q(1, b, c, "a", "b")})`;
      const R = correct ? termsQ([[m2, "a²"], [m2 * b, "ab"], [m2 * c, "a"]])
        : termsQ([[m2, "a²"], [m2 * b, "ab"], [-m2 * c, "a"]]);
      return `${L} = ${R}`; };
    const okIdx = ri(0, 4); const eqs = [];
    for (let i = 0; i < 5; i++) eqs.push(mk(i === okIdx));
    if (new Set(eqs).size !== 5) return null;
    return P("choice", "다음 중 옳은 것은?", eqs[okIdx], 3, 25, eqs); },
];

// ═══════════ 3. m2-ineq1 부등식의 기본 성질 ═══════════
// 계수 p: [분자, 분모] — 음수면 부등호 반전
const PCOEF = [[2, 1], [3, 1], [5, 1], [-2, 1], [-3, 1], [-5, 1], [1, 2], [-1, 2], [1, 3], [-1, 3], [-1, 1]];
function coefTerm(pn, pd, v) {
  if (pd === 1) return pn === 1 ? v : pn === -1 ? M + v : `${num(pn)}${v}`;
  return `${pn < 0 ? M : ""}${v}/${pd}`;
}
function transQ(pn, pd, q, v) {
  let s = coefTerm(pn, pd, v);
  if (q > 0) s += ` + ${q}`; else if (q < 0) s += ` ${M} ${-q}`;
  return s;
}
const INEQS = ["<", "≤"];
const ineq1Builders = [
  () => { const base = pick(INEQS);                                            // □ 부등호 choice
    const [pn, pd] = pick(PCOEF), q = ri(-9, 9);
    const flip = pn < 0;
    const ans = flip ? (base === "<" ? ">" : "≥") : base;
    const q1 = `a ${base} b일 때, ${transQ(pn, pd, q, "a")} □ ${transQ(pn, pd, q, "b")}에서 □ 안에 알맞은 부등호는?`;
    const ch = opts(ans, ["<", "≤", "=", "≥", ">"].filter((s) => s !== ans));
    return ch && P("choice", q1, ans, 2, 15, ch); },
  () => { const base = pick(INEQS);                                            // 옳지 않은 것 choice
    const mkT = () => { const [pn, pd] = pick(PCOEF), q = ri(-8, 8);
      const rel = pn < 0 ? (base === "<" ? ">" : "≥") : base;
      return { s: `${transQ(pn, pd, q, "a")} ${rel} ${transQ(pn, pd, q, "b")}`, key: `${pn}/${pd}/${q}` }; };
    const wrongIdx = ri(0, 4); const items = []; const keys = new Set();
    for (let i = 0; i < 5; i++) {
      const t = mkT(); if (keys.has(t.key)) return null; keys.add(t.key);
      if (i === wrongIdx) {                                                    // 방향만 뒤집은 오답
        const [pn, pd] = pick(PCOEF.filter(([n]) => n < 0)), q = ri(-8, 8);
        const badRel = base;                                                   // 음수 곱인데 반전 안 함
        items.push(`${transQ(pn, pd, q, "a")} ${badRel} ${transQ(pn, pd, q, "b")}`);
      } else items.push(t.s);
    }
    if (new Set(items).size !== 5) return null;
    return P("choice", `a ${base} b일 때, 다음 중 옳지 않은 것은?`, items[wrongIdx], 2, 20, items); },
  () => { const base = pick(INEQS);                                            // OX
    const [pn, pd] = pick(PCOEF), q = ri(-9, 9);
    const correctRel = pn < 0 ? (base === "<" ? ">" : "≥") : base;
    const shownRel = rand() < 0.5 ? correctRel : pick(["<", ">", "≤", "≥"].filter((r) => r !== correctRel));
    return P("ox", `a ${base} b이면 ${transQ(pn, pd, q, "a")} ${shownRel} ${transQ(pn, pd, q, "b")}이다.`, shownRel === correctRel ? "O" : "X", 2, 12); },
  () => { const [pn, pd] = pick(PCOEF), q = ri(-8, 8);                          // 두 수의 대소 관계 choice
    const rel = pn < 0 ? ">" : "<";
    const L = transQ(pn, pd, q, "a"), R = transQ(pn, pd, q, "b");
    const ans = `${L} ${rel} ${R}`;
    const ch = opts(ans, [`${L} ${rel === "<" ? ">" : "<"} ${R}`, `${L} ≤ ${R}`, `${L} ≥ ${R}`, `${L} = ${R}`]);
    return ch && P("choice", `a < b일 때, 두 수 ${L}, ${R}의 대소 관계를 부등식으로 나타낸 것은?`, ans, 2, 18, ch); },
];

// ═══════════ 4. m2-ineq2 식의 값의 범위 ═══════════
const REL = { "<": "<", "≤": "≤" };
const ineq2Builders = [
  () => { const k = ri(-5, 6), incl = rand() < 0.4;                             // x<k → px+q 범위 choice
    const p = ri(2, 4) * pick([1, -1]), q = ri(-7, 7);
    const B = p * k + q;
    const baseRel = incl ? "≤" : "<";
    const dir = pick([true, false]);                                            // x < k  또는 x > k
    const given = `x ${dir ? baseRel : (incl ? "≥" : ">")} ${num(k)}`;
    // p>0이면 방향 유지, p<0이면 반전
    const resDirLess = (dir && p > 0) || (!dir && p < 0);
    const rel = incl ? (resDirLess ? "≤" : "≥") : (resDirLess ? "<" : ">");
    const E = linQ(p, q);
    const ans = `${E} ${rel} ${num(B)}`;
    const flipRel = incl ? (resDirLess ? "≥" : "≤") : (resDirLess ? ">" : "<");
    const ch = opts(ans, [`${E} ${flipRel} ${num(B)}`, `${E} ${rel} ${num(-B)}`,
      `${E} ${flipRel} ${num(-B)}`, `${E} ${rel} ${num(B + p)}`]);
    return ch && P("choice", `${given}일 때, ${E}의 값의 범위는?`, ans, 2, 18, ch); },
  () => { const k = ri(-5, 6), p = ri(2, 5) * pick([1, -1]), q = ri(-8, 8);     // 경계값 a 구하기 calc
    const B = p * k + q;
    const dirGE = rand() < 0.5;                                                 // x ≥ k / x ≤ k
    const resGE = (dirGE && p > 0) || (!dirGE && p < 0);
    const E = linQ(p, q);
    return P("calc", `x ${dirGE ? "≥" : "≤"} ${num(k)}일 때, ${E}의 값의 범위는 ${E} ${resGE ? "≥" : "≤"} a이다. 이때 a의 값을 구하시오.`, B, 2, 15); },
  () => { const m2 = ri(-4, 2), w = ri(1, 5), n = m2 + w;                       // m<x<n → A 범위 choice
    const p = ri(2, 4) * pick([1, -1]), q = ri(-7, 7);
    const lo = p > 0 ? p * m2 + q : p * n + q, hi = p > 0 ? p * n + q : p * m2 + q;
    const ans = `${num(lo)} < A < ${num(hi)}`;
    const ch = opts(ans, [`${num(-lo)} < A < ${num(hi)}`, `${num(lo)} ≤ A ≤ ${num(hi)}`,
      `${num(lo)} < A < ${num(hi + Math.abs(p))}`, `${num(hi)} < A < ${num(lo)}`, `${num(lo - Math.abs(p))} < A < ${num(hi)}`]);
    return ch && P("choice", `${num(m2)} < x < ${num(n)}일 때, A = ${linQ(p, q)}의 값의 범위는?`, ans, 3, 22, ch); },
  () => { const al = ri(-4, 2), w = ri(1, 4), be = al + w;                      // 겹부등식 → x 범위 choice
    const p = ri(2, 4), q = ri(-6, 6);
    const mm = p * al + q, nn = p * be + q;
    const ans = `${num(al)} < x < ${num(be)}`;
    const ch = opts(ans, [`${num(-al)} < x < ${num(be)}`, `${num(al)} ≤ x ≤ ${num(be)}`,
      `${num(al - 1)} < x < ${num(be)}`, `${num(al)} < x < ${num(be + 1)}`, `${num(be)} < x < ${num(al)}`]);
    return ch && P("choice", `${num(mm)} < ${linQ(p, q)} < ${num(nn)}일 때, x의 값의 범위는?`, ans, 3, 22, ch); },
];

// ═══════════ 5. m2-ineq3 일차부등식의 풀이 ═══════════
const ineq3Builders = [
  () => { const x0 = ri(-8, 8), a = ri(1, 5) * pick([1, -1]);                   // 풀면 choice
    let c = ri(-4, 4); if (c === a) c = a - 1;
    const b = ri(-9, 9), d = (a - c) * x0 + b;
    if (Math.abs(d) > 30) return null;
    const strict = rand() < 0.6;
    const baseRel = strict ? "<" : "≤";
    const solLess = a - c > 0;                                                  // ax+b < cx+d → (a−c)x < d−b
    const rel = strict ? (solLess ? "<" : ">") : (solLess ? "≤" : "≥");
    const ans = `x ${rel} ${num(x0)}`;
    const flip = strict ? (solLess ? ">" : "<") : (solLess ? "≥" : "≤");
    const ch = opts(ans, [`x ${flip} ${num(x0)}`, `x ${rel} ${num(-x0 || 1)}`,
      `x ${flip} ${num(-x0 || 1)}`, `x ${rel} ${num(x0 + 1)}`]);
    return ch && P("choice", `일차부등식 ${linQ(a, b)} ${baseRel} ${linQ(c, d)}${eul(d === 0 ? "x" : Math.abs(d))} 풀면?`, ans, 2, 15, ch); },
  () => { const x0 = ri(-6, 6), a = ri(2, 5) * pick([1, -1]);                   // 해 calc (답: x>4 꼴)
    let c = ri(-4, 4); if (c === a) c = a - 1;
    const b = ri(-9, 9), d = (a - c) * x0 + b;
    if (Math.abs(d) > 30) return null;
    const strict = rand() < 0.7;
    const baseRel = strict ? ">" : "≥";
    const solGreater = a - c > 0;                                               // ax+b > cx+d
    const rel = strict ? (solGreater ? ">" : "<") : (solGreater ? ">=" : "<=");
    const relQ = strict ? (solGreater ? ">" : "<") : (solGreater ? "≥" : "≤");
    return P("calc", `부등식 ${linQ(a, b)} ${baseRel} ${linQ(c, d)}${eul(d === 0 ? "x" : Math.abs(d))} 풀어 해를 나타내시오. (입력 예: x > 2 또는 x >= 2)`, `x${rel}${x0}`, 2, 15); },
  () => { const N = ri(3, 12);                                                  // 자연수 해 개수 calc
    const a = ri(2, 4), b = ri(-6, 6);
    const strict = rand() < 0.5;
    const c2 = strict ? a * (N + 1) + b : a * N + b;
    return P("calc", `부등식 ${linQ(a, b)} ${strict ? "<" : "≤"} ${num(c2)}${eul(c2)} 만족시키는 자연수 x의 개수를 구하시오.`, N, 2, 18); },
  () => { const x0 = ri(-5, 5), a = ri(2, 6);                                   // 보기 부등식의 해 choice
    const b = ri(-8, 8);
    const cc = a * x0 + b;
    const strict = rand() < 0.5;
    const rel = strict ? ">" : "≥";
    const ans = `x ${rel} ${num(x0)}`;
    const ch = opts(ans, [`x ${strict ? "<" : "≤"} ${num(x0)}`, `x ${rel} ${num(x0 + 1)}`,
      `x ${rel} ${num(-x0 || 2)}`, `x ${strict ? "<" : "≤"} ${num(-x0 || 2)}`]);
    return ch && P("choice", `부등식 ${linQ(a, b)} ${rel} ${num(cc)}의 해를 바르게 나타낸 것은?`, ans, 1, 12, ch); },
];

// ═══════════ 6. m2-para1 평행사변형 성질 및 증명 ═══════════
const PARA_TRUE = [
  "두 쌍의 대변의 길이가 각각 같다",
  "두 쌍의 대각의 크기가 각각 같다",
  "두 대각선은 서로 다른 것을 이등분한다",
  "이웃하는 두 내각의 크기의 합은 180°이다",
  "두 쌍의 대변이 각각 평행하다",
];
const PARA_FALSE = [
  "두 대각선의 길이가 서로 같다",
  "두 대각선은 서로 수직이다",
  "네 변의 길이가 모두 같다",
  "네 내각의 크기가 모두 같다",
  "이웃하는 두 내각의 크기가 서로 같다",
];
const CONG = [
  ["두 대각선이 서로 다른 것을 이등분함을 증명할 때, 대각선의 교점을 O라 하면 △OAB ≡ △OCD임을 보인다. 이때 이용되는 합동조건은?", "ASA 합동"],
  ["두 쌍의 대변의 길이가 각각 같음을 증명할 때, 대각선 BD를 그어 △ABD ≡ △CDB임을 보인다. 이때 이용되는 합동조건은?", "ASA 합동"],
  ["한 쌍의 대변이 평행하고 길이가 같은 사각형이 평행사변형임을 증명할 때, 대각선 AC를 그어 △ABC ≡ △CDA임을 보인다. 이때 이용되는 합동조건은?", "SAS 합동"],
];
const CONG_OPTS = ["SSS 합동", "SAS 합동", "ASA 합동", "RHA 합동", "RHS 합동"];
const para1Builders = [
  () => { const wrongIdx = ri(0, 4);
    const trues = shuffle(PARA_TRUE).slice(0, 4);
    const falseOne = pick(PARA_FALSE);
    const items = [...trues]; items.splice(wrongIdx, 0, falseOne);
    return P("choice", "다음 중 평행사변형의 성질이 아닌 것은?", falseOne, 2, 18, items); },
  () => { const okIdx = ri(0, 4);
    const falses = shuffle(PARA_FALSE).slice(0, 4);
    const trueOne = pick(PARA_TRUE);
    const items = [...falses]; items.splice(okIdx, 0, trueOne);
    return P("choice", "다음 중 평행사변형의 성질인 것은?", trueOne, 2, 18, items); },
  () => { const [q, a] = pick(CONG);
    return P("choice", `평행사변형 ABCD에서 ${q}`, a, 2, 20, [...CONG_OPTS]); },
  () => { const s = pick([...PARA_TRUE.map((t) => [t, "O"]), ...PARA_FALSE.map((t) => [t, "X"])]);
    return P("ox", `평행사변형에서 ${s[0]}.`, s[1], 1, 10); },
  () => { const th = ri(35, 145);
    const which = pick([["B", 180 - th], ["C", th], ["D", 180 - th]]);
    return P("calc", `평행사변형 ABCD에서 ∠A = ${th}°일 때, ∠${which[0]}의 크기는 몇 도인지 구하시오.`, which[1], 1, 10); },
  () => { const p = ri(3, 12), q = ri(3, 12);
    return P("calc", `평행사변형 ABCD에서 AB = ${p} cm, BC = ${q} cm일 때, 둘레의 길이는 몇 cm인지 구하시오.`, 2 * (p + q), 1, 10); },
  () => { const t = ri(3, 12);
    const which = pick([["AO", "AC"], ["BO", "BD"]]);
    return P("calc", `평행사변형 ABCD의 두 대각선의 교점을 O라 하자. ${which[0]} = ${t} cm일 때, ${which[1]}의 길이는 몇 cm인지 구하시오.`, 2 * t, 1, 10); },
  () => { const d = ri(1, 6) * 2;
    const A = (180 + d) / 2; if (!Number.isInteger(A)) return null;
    return P("calc", `평행사변형 ABCD에서 ∠A ${M} ∠B = ${d}°일 때, ∠A의 크기는 몇 도인지 구하시오.`, A, 2, 18); },
  () => { const m2 = ri(1, 5), n2 = ri(1, 5); if (m2 === n2) return null;
    if ((180 * m2) % (m2 + n2) !== 0) return null;
    return P("calc", `평행사변형 ABCD에서 ∠A : ∠B = ${m2} : ${n2}일 때, ∠A의 크기는 몇 도인지 구하시오.`, 180 * m2 / (m2 + n2), 2, 18); },
];

// ═══════════ 7. m2-para2 평행사변형이 되는 조건 ═══════════
const COND_TRUE = [
  "두 쌍의 대변이 각각 평행하다",
  "두 쌍의 대변의 길이가 각각 같다",
  "두 쌍의 대각의 크기가 각각 같다",
  "두 대각선이 서로 다른 것을 이등분한다",
  "한 쌍의 대변이 평행하고 그 길이가 같다",
];
const COND_FALSE = [
  "한 쌍의 대변의 길이가 같다",
  "두 대각선의 길이가 같다",
  "두 대각선이 서로 수직이다",
  "한 쌍의 대변이 평행하고 다른 한 쌍의 대변의 길이가 같다",
  "이웃하는 두 변의 길이가 같다",
  "한 쌍의 대각의 크기가 같다",
];
const para2Builders = [
  () => { const okIdx = ri(0, 4);
    const falses = shuffle(COND_FALSE).slice(0, 4);
    const trueOne = pick(COND_TRUE);
    const items = [...falses]; items.splice(okIdx, 0, trueOne);
    return P("choice", "다음 중 사각형이 평행사변형이 되기 위한 조건으로 알맞은 것은?", trueOne, 2, 20, items); },
  () => { const wrongIdx = ri(0, 4);
    const trues = shuffle(COND_TRUE).slice(0, 4);
    const falseOne = pick(COND_FALSE);
    const items = [...trues]; items.splice(wrongIdx, 0, falseOne);
    return P("choice", "다음 중 사각형이 평행사변형이 되는 조건으로 옳지 않은 것은?", falseOne, 2, 20, items); },
  () => { const A = ri(60, 120), B = 180 - A;
    const isP = rand() < 0.5;
    const C = isP ? A : A + pick([10, -10, 20, -20]);
    const D = 360 - A - B - C;
    if (D <= 0 || D >= 180) return null;
    return P("ox", `사각형 ABCD에서 ∠A = ${A}°, ∠B = ${B}°, ∠C = ${C}°, ∠D = ${D}°이면 이 사각형은 평행사변형이다.`, isP ? "O" : "X", 2, 18); },
  () => { const s = pick([
      ["두 대각선의 교점을 O라 할 때 OA = OC, OB = OD인 사각형", "O"],
      ["AB = DC, AD = BC인 사각형 ABCD", "O"],
      ["AB ∥ DC이고 AB = DC인 사각형 ABCD", "O"],
      ["AB ∥ DC이고 AD = BC인 사각형 ABCD", "X"],
      ["AB = BC, CD = DA인 사각형 ABCD", "X"],
      ["두 대각선의 길이가 같은 사각형", "X"],
    ]);
    return P("ox", `${s[0]}은 항상 평행사변형이다.`, s[1], 2, 18); },
  () => { const t = ri(3, 10), k = ri(2, 4);
    const c = k * ri(1, 3);
    const x = (t + c) / k; if (!Number.isInteger(x)) return null;
    return P("calc", `사각형 ABCD의 두 대각선의 교점을 O라 하자. OA = ${t}, OC = ${linQ(k, -c)}이고 OB = OD일 때, 이 사각형이 평행사변형이 되도록 하는 x의 값을 구하시오.`, x, 2, 18); },
  () => { const A = ri(70, 130), B = 180 - A;                                    // ∠D 구하기 calc
    return P("calc", `사각형 ABCD에서 ∠A = ${A}°, ∠B = ${B}°, ∠C = ${A}°이다. 이 사각형이 평행사변형이 되려면 ∠D의 크기는 몇 도이어야 하는지 구하시오.`, B, 2, 15); },
  () => { const p = ri(3, 9), k = ri(2, 3);                                      // 변 길이 x calc
    const c = k * ri(1, 3) - p; const x = (p + Math.abs(c)) / k;
    const cc = k * ri(1, 4); const xx = (p + cc) / k; if (!Number.isInteger(xx)) return null;
    return P("calc", `사각형 ABCD에서 AB ∥ DC이고 AB = ${p}, DC = ${linQ(k, -cc)}이다. 이 사각형이 평행사변형이 되도록 하는 x의 값을 구하시오.`, xx, 2, 18); },
];

// ═══════════ 8. m2-quad 여러 가지 사각형 ═══════════
// 진리표: [대각선 길이 같음, 대각선 수직, 대각선 이등분, 네 변 같음, 네 각 직각]
const SHAPES = {
  "평행사변형": [0, 0, 1, 0, 0],
  "직사각형": [1, 0, 1, 0, 1],
  "마름모": [0, 1, 1, 1, 0],
  "정사각형": [1, 1, 1, 1, 1],
  "등변사다리꼴": [1, 0, 0, 0, 0],
};
const PROPS = [
  "두 대각선의 길이가 같다",
  "두 대각선이 서로 수직이다",
  "두 대각선이 서로 다른 것을 이등분한다",
  "네 변의 길이가 모두 같다",
  "네 내각의 크기가 모두 같다",
];
const quadBuilders = [
  () => { const name = pick(Object.keys(SHAPES));                                // 성질 OX (진리표)
    const pi = ri(0, 4);
    return P("ox", `${name}에서 ${PROPS[pi]}.`, SHAPES[name][pi] ? "O" : "X", 1, 10); },
  () => { const sig = pick([                                                     // 유일 판별 choice
      [["두 대각선의 길이가 같고 서로 수직이등분한다"], "정사각형"],
      [["두 대각선이 서로 수직이등분하지만 길이는 같지 않다"], "마름모"],
      [["두 대각선의 길이가 같고 서로 다른 것을 이등분하지만 수직은 아니다"], "직사각형"],
      [["두 대각선의 길이는 같지만 서로 다른 것을 이등분하지 않는다"], "등변사다리꼴"],
    ]);
    const items = shuffle(["평행사변형", "직사각형", "마름모", "정사각형", "등변사다리꼴"]);
    return P("choice", `다음 조건을 만족하는 사각형은? — ${sig[0][0]}`, sig[1], 2, 18, items); },
  () => { const from = pick([["직사각형", "마름모"], ["마름모", "직사각형"], ["평행사변형", "직사각형"], ["평행사변형", "마름모"]]); // 되기 위한 조건 choice
    const BANK = {
      "직사각형→마름모": ["이웃하는 두 변의 길이가 같다", ["두 대각선의 길이가 같다", "한 내각이 직각이다", "두 쌍의 대변이 각각 평행하다", "이웃하는 두 내각의 크기가 같다"]],
      "마름모→직사각형": ["한 내각이 직각이다", ["네 변의 길이가 모두 같다", "두 대각선이 서로 수직이다", "이웃하는 두 변의 길이가 같다", "두 대각선이 서로 다른 것을 이등분한다"]],
      "평행사변형→직사각형": ["두 대각선의 길이가 같다", ["두 대각선이 서로 수직이다", "네 변의 길이가 모두 같다", "이웃하는 두 변의 길이가 같다", "두 쌍의 대변이 각각 평행하다"]],
      "평행사변형→마름모": ["두 대각선이 서로 수직이다", ["두 대각선의 길이가 같다", "네 내각의 크기가 모두 같다", "한 내각이 직각이다", "두 쌍의 대각의 크기가 각각 같다"]],
    };
    const key = `${from[0]}→${from[1]}`;
    const [ans, wrongs] = BANK[key];
    const items = shuffle([ans, ...wrongs]);
    return P("choice", `${from[0]}이 ${from[1]}이 되기 위한 조건으로 알맞은 것은?`, ans, 2, 20, items); },
  () => { const A = pick([["직사각형", "∠A", 90]]);                              // 조건 빈칸 calc: 각
    const th = 90;
    return P("calc", `평행사변형 ABCD가 직사각형이 되려면 ∠A의 크기는 몇 도이어야 하는지 구하시오.`, th, 1, 8); },
  () => { const L = ri(6, 20);                                                   // 대각선 조건 calc
    return P("calc", `평행사변형 ABCD에서 AC = ${L} cm이다. 이 평행사변형이 직사각형이 되려면 BD의 길이는 몇 cm이어야 하는지 구하시오.`, L, 1, 10); },
  () => { const k = ri(2, 3), c = k * ri(1, 4), L = ri(5, 15);                   // 대각선 x calc
    const x = (L + c) / k; if (!Number.isInteger(x)) return null;
    return P("calc", `평행사변형 ABCD에서 AC = ${L}, BD = ${linQ(k, -c)}이다. 이 평행사변형이 직사각형이 되도록 하는 x의 값을 구하시오.`, x, 2, 15); },
  () => { const p = ri(4, 12), k = ri(2, 3), c = k * ri(1, 3);                   // 마름모 변 x calc
    const x = (p + c) / k; if (!Number.isInteger(x)) return null;
    return P("calc", `평행사변형 ABCD에서 AB = ${p}, BC = ${linQ(k, -c)}이다. 이 평행사변형이 마름모가 되도록 하는 x의 값을 구하시오.`, x, 2, 15); },
  () => { const s = ri(3, 15);                                                   // 마름모 둘레 calc
    return P("calc", `마름모 ABCD에서 AB = ${s} cm일 때, 둘레의 길이는 몇 cm인지 구하시오.`, 4 * s, 1, 8); },
  () => { const th = ri(40, 85);                                                 // 등변사다리꼴 각 calc
    const which = pick([["C", th], ["A", 180 - th]]);
    return P("calc", `AD ∥ BC인 등변사다리꼴 ABCD에서 ∠B = ${th}°일 때, ∠${which[0]}의 크기는 몇 도인지 구하시오.`, which[1], 2, 15); },
  () => { const wrongIdx = ri(0, 4);                                             // 옳지 않은 것 choice (진리표)
    const items = []; let ansS = "";
    const combos = [];
    for (const name of Object.keys(SHAPES)) for (let pi = 0; pi < 5; pi++) combos.push([name, pi]);
    const sel = shuffle(combos).slice(0, 5);
    for (let i = 0; i < 5; i++) {
      const [name, pi] = sel[i];
      const truth = SHAPES[name][pi];
      if (i === wrongIdx) { const st = `${name}은 ${PROPS[pi].replace("다", "다")}`;
        items.push(`${name} — ${PROPS[pi]}`); if (truth) return null; ansS = items[i]; }
      else { if (!truth) return null; items.push(`${name} — ${PROPS[pi]}`); }
    }
    if (new Set(items).size !== 5) return null;
    return P("choice", "다음 중 사각형과 그 성질이 옳게 짝지어지지 않은 것은?", ansS, 2, 22, items); },
];


// ═══════════ 브라우저용 래퍼 ═══════════
const linA = linAns;   // m2 빌더 호환 별칭

function makeProblems(unitId, builders, count, startNo, seen) {
  const out = [];
  let no = startNo, guard = 0;
  const limit = Math.max(count * 1500, 60000);
  while (out.length < count && guard++ < limit) {
    const b = pick(builders);
    const p = b();
    if (!p) continue;
    const key = p.question + "|" + (p.choices || []).join("|");
    if (seen.has(key)) continue;
    if (p.type === "choice") {
      if (!p.choices || p.choices.length !== 5) continue;
      if (new Set(p.choices).size !== 5) continue;
      if (p.choices.filter((c) => c === p.answer).length !== 1) continue;
    }
    if (!p.answer && p.answer !== "0") continue;
    seen.add(key);
    out.push({ id: `${unitId}-${String(no++).padStart(3, "0")}`, unitId, ...p });
  }
  return out;
}

export const GEN_UNITS = [
  { id: "m1-int", name: "정수와 유리수의 계산", grade: "중1" },
  { id: "m1-fac", name: "소인수분해 하기", grade: "중1" },
  { id: "m1-div", name: "약수의 개수 구하기", grade: "중1" },
  { id: "m1-gcd", name: "최대공약수 구하기", grade: "중1" },
  { id: "m1-lcm", name: "최소공배수 구하기", grade: "중1" },
  { id: "m1-expr", name: "문자의 사용과 식의 계산", grade: "중1" },
  { id: "m1-eq1", name: "일차방정식 (등식 세우기·성질)", grade: "중1" },
  { id: "m1-eq2", name: "일차방정식의 풀이", grade: "중1" },
  { id: "m1-prop1", name: "정비례와 반비례 — 식 구하기", grade: "중1" },
  { id: "m1-prop2", name: "정비례와 반비례 — 관계식 구하기", grade: "중1" },
  { id: "mono-op", name: "단항식의 곱셈과 나눗셈", grade: "중2" },
  { id: "m2-poly1", name: "다항식의 덧셈과 뺄셈", grade: "중2" },
  { id: "m2-poly2", name: "다항식의 곱셈과 나눗셈", grade: "중2" },
  { id: "m2-ineq1", name: "부등식의 기본 성질", grade: "중2" },
  { id: "m2-ineq2", name: "식의 값의 범위 구하기", grade: "중2" },
  { id: "m2-ineq3", name: "일차부등식의 풀이", grade: "중2" },
  { id: "m2-para1", name: "평행사변형 성질 및 증명", grade: "중2" },
  { id: "m2-para2", name: "평행사변형이 되는 조건", grade: "중2" },
  { id: "m2-quad", name: "여러 가지 사각형", grade: "중2" },
];

const BUILDERS = {
  "m1-int": intBuilders, "m1-fac": facBuilders, "m1-div": divBuilders,
  "m1-gcd": [mkGL("gcd")], "m1-lcm": [mkGL("lcm")],
  "m1-expr": exprBuilders, "m1-eq1": eq1Builders, "m1-eq2": eq2Builders,
  "m1-prop1": prop1Builders, "m1-prop2": prop2Builders, "mono-op": monoBuilders,
  "m2-poly1": poly1Builders, "m2-poly2": poly2Builders,
  "m2-ineq1": ineq1Builders, "m2-ineq2": ineq2Builders, "m2-ineq3": ineq3Builders,
  "m2-para1": para1Builders, "m2-para2": para2Builders, "m2-quad": quadBuilders,
};

// existing: [{id, question, choices}] — DB에 이미 있는 문제 (중복 회피 + id 이어붙이기)
export function generateProblems(unitId, count, seedVal, existing = []) {
  seed = (seedVal ?? Date.now()) % 2147483647;
  const builders = BUILDERS[unitId];
  if (!builders) return { problems: [], requested: count, error: "이 유닛은 규칙 생성을 지원하지 않아요" };
  const seen = new Set(existing.map((r) => r.question + "|" + (r.choices || []).join("|")));
  let maxNo = 0;
  const re = new RegExp("^" + unitId + "-(\\d+)$");
  for (const r of existing) {
    const m = String(r.id || "").match(re);
    if (m) maxNo = Math.max(maxNo, +m[1]);
  }
  const problems = makeProblems(unitId, builders, count, maxNo + 1, seen);
  return { problems, requested: count };
}
