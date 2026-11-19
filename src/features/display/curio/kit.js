// ashrain.out — 수학 호기심 액자 공용 계산 (curio/kit.js)
// 축구 · 농구 · 야구 직선 액자, 공 꺼내기 · 알파벳 카드 · 일렬로 세우기 · 학년별 뽑기 액자가 함께 쓴다.
//   · 분수 · 직선(두 점을 지나는 직선의 식, 판서 글자) — 글자는 draw.jsx 의 MText 문법({분자/분모}, 소문자 한 글자는 기울임)
//   · 씨앗 난수(벽시계로 흐르는 액자라 같은 씨앗 → 같은 장면) · 한국 이름 짓기 · 빠르기
// 화면에 나오는 수는 모두 여기서 계산한다. tests/display-curio.test.mjs 가 따로 다시 계산해 맞춘다.

export const MINUS = "−";

/* ══════════ 수 ══════════ */
export const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
/** 기약분수 [분자, 분모] — 분모는 양수 */
export function frac(n, d) {
  if (d < 0) { n = -n; d = -d; }
  const g = gcd(n, d) || 1;
  return [n / g, d / g];
}
/** 정수 글자(음수는 수학 빼기 기호) */
export const num = (v) => (v < 0 ? MINUS + Math.abs(v) : String(v));
/** 음수면 괄호로 */
export const paren = (v) => (v < 0 ? `(${num(v)})` : String(v));
/** 기약분수 글자 — 정수면 정수, 음수면 앞에 − */
export function fs(n, d = 1) {
  const [a, b] = frac(n, d);
  if (b === 1) return num(a);
  return (a < 0 ? MINUS : "") + `{${Math.abs(a)}/${b}}`;
}
/** 약분하지 않은 분수 글자(부호는 앞으로) */
export function fsRaw(n, d) {
  if (d === 1) return num(n);
  const neg = (n < 0) !== (d < 0) && n !== 0;
  return (neg ? MINUS : "") + `{${Math.abs(n)}/${Math.abs(d)}}`;
}
export const pt = (p) => `(${num(p[0])}, ${num(p[1])})`;
/** 수 뒤의 을/를 — 끝자리 읽기(2 이 · 4 사 · 5 오 · 9 구 → 를, 나머지 → 을) */
export const eul = (v) => (/[2459]$/.test(String(Math.abs(Math.round(v)))) ? "를" : "을");
/** 천 단위 쉼표 */
export const comma = (v) => String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ",");

/* ══════════ 직선 ══════════ */
/**
 * 두 점 p, q 를 지나는 직선.
 *   kind: "pt"(같은 점) | "v"(세로선 x = k, 함수 아님) | "h"(가로선 y = k, 상수함수) | "f"(일차함수 y = ax + b)
 *   m = 기울기 [분자, 분모] · b = y절편 [분자, 분모] (기약분수)
 */
export function lineOf(p, q) {
  const dx = q[0] - p[0], dy = q[1] - p[1];
  if (dx === 0 && dy === 0) return { kind: "pt", dx, dy };
  if (dx === 0) return { kind: "v", x: p[0], dx, dy };
  const m = frac(dy, dx);
  const b = frac(p[1] * m[1] - m[0] * p[0], m[1]);
  return { kind: dy === 0 ? "h" : "f", m, b, dx, dy };
}
/** 직선 위 x 에서의 y (그리기용 실수) */
export const lineY = (L, x) => (L.m[0] / L.m[1]) * x + L.b[0] / L.b[1];
/** 기울기 a 의 글자(x 앞에 붙는 꼴): 1 → "", −1 → "−" */
function coef(mn, md) {
  if (md === 1 && mn === 1) return "";
  if (md === 1 && mn === -1) return MINUS;
  return fs(mn, md);
}
/** 직선의 식 글자 — y = ax + b · x = k · y = k */
export function eqText(L) {
  if (L.kind === "v") return `x = ${num(L.x)}`;
  if (L.kind === "h") return `y = ${fs(L.b[0], L.b[1])}`;
  if (L.kind === "pt") return "";
  const [bn, bd] = L.b;
  let s = `y = ${coef(L.m[0], L.m[1])}x`;
  if (bn !== 0) s += (bn < 0 ? ` ${MINUS} ` : " + ") + fs(Math.abs(bn), bd);
  return s;
}
/** 원점을 지나는 직선 y = ax 의 식(정비례) — 점 q */
export function propText(q) {
  const L = lineOf([0, 0], q);
  return eqText(L);
}

/**
 * 판서 줄(중등): 두 점 p(출발) · q(도착) → 기울기 → 대입 → 식. 반환 { L, lines: [{ s, hi?, small? }] }
 *   origin: true 면 p 가 원점 — 정비례(y = ax), 대입 줄 없이
 */
export function lineSteps(p, q, { origin = false } = {}) {
  const L = lineOf(p, q);
  const out = [];
  if (L.kind === "pt") return { L, lines: [{ s: "두 점이 같아요 — 직선이 하나로 정해지지 않아요" }] };
  if (L.kind === "v") {
    out.push({ s: `두 점의 x좌표가 같아요(${num(p[0])})` });
    out.push({ s: `x = ${num(p[0])}`, hi: true });
    out.push({ s: "세로로 선 직선 — y가 하나로 정해지지 않아 함수가 아니에요", small: true });
    return { L, lines: out };
  }
  const sl = origin ? `{${num(q[1])}/${num(q[0])}}` : `{${num(q[1])} ${MINUS} ${paren(p[1])}/${num(q[0])} ${MINUS} ${paren(p[0])}}`;
  const raw = fsRaw(L.dy, L.dx), red = fs(L.m[0], L.m[1]);
  const chain = [sl];
  if (!origin) chain.push(raw);
  if (red !== chain[chain.length - 1] && !(origin && raw === red)) chain.push(red);
  out.push({ s: `기울기 = ${chain.join(" = ")}` });
  if (L.kind === "h") {
    out.push({ s: `y = ${fs(L.b[0], L.b[1])}`, hi: true });
    out.push({ s: "기울기가 0 — 일차함수가 아닌 상수함수", small: true });
    return { L, lines: out };
  }
  if (origin) {
    out.push({ s: "원점을 지나므로 y = ax 꼴(정비례)", small: true });
  } else {
    out.push({ s: `x = ${num(p[0])}, y = ${num(p[1])}${eul(p[1])} 대입하면`, small: true });
    out.push({ s: `${num(p[1])} = ${fs(L.m[0], L.m[1])} × ${paren(p[0])} + b` });
    out.push({ s: `b = ${fs(L.b[0], L.b[1])}` });
  }
  out.push({ s: eqText(L), hi: true });
  return { L, lines: out };
}

/** 판서 줄(초등): 가로 · 세로 칸 수 → 세로 ÷ 가로 */
export function runRiseSteps(p, q, { unit = "칸", right = "오른쪽", left = "왼쪽", up = "위", down = "아래" } = {}) {
  const dx = q[0] - p[0], dy = q[1] - p[1];
  const lines = [];
  lines.push({ s: dx === 0 ? "가로로는 그대로" : `${dx > 0 ? right : left}으로 ${Math.abs(dx)}${unit}` });
  lines.push({ s: dy === 0 ? "세로로는 그대로" : `${dy > 0 ? up : down}로 ${Math.abs(dy)}${unit}` });
  if (dx !== 0 && dy !== 0) {
    lines.push({ s: "가파른 정도 = 세로 ÷ 가로", small: true });
    lines.push({ s: `${Math.abs(dy)} ÷ ${Math.abs(dx)} = ${fs(Math.abs(dy), Math.abs(dx))}`, hi: true });
    lines.push({ s: `가로 1${unit}에 ${fs(Math.abs(dy), Math.abs(dx))}${unit}씩 ${(dy > 0) === (dx > 0) ? "올라가요" : "내려가요"}`, small: true });
  } else if (dx === 0) {
    lines.push({ s: "똑바로 세로로 선 직선", hi: true });
  } else {
    lines.push({ s: "가로로 누운 직선 — 가파른 정도 0", hi: true });
  }
  return lines;
}

/* ══════════ 씨앗 난수 ══════════ */
/** 정수 여러 개 → 32비트 씨앗 */
export function hashSeed(...xs) {
  let h = 2166136261 >>> 0;
  for (const x of xs) {
    const s = String(x);
    for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    h ^= 0x9e37; h = Math.imul(h, 16777619) >>> 0;
  }
  return h >>> 0;
}
/** mulberry32 — () => [0, 1) */
export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export const rint = (R, n) => Math.floor(R() * n);
export function shuffle(arr, R) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) { const j = rint(R, i + 1); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

/* ══════════ 이름 ══════════ */
// 성(흔한 순, 무게) · 이름(요즘 학생들에게 흔한 두 글자 이름) — 가나다 정렬은 localeCompare("ko")
const SUR = [["김", 21], ["이", 15], ["박", 8], ["최", 5], ["정", 5], ["강", 2.4], ["조", 2.1], ["윤", 2.1], ["장", 2], ["임", 1.8],
  ["한", 1.5], ["오", 1.5], ["서", 1.4], ["신", 1.4], ["권", 1.4], ["황", 1.4], ["안", 1.3], ["송", 1.3], ["류", 1.2], ["전", 1.1],
  ["홍", 1], ["고", 0.9], ["문", 0.9], ["양", 0.9], ["손", 0.9], ["배", 0.8], ["백", 0.7], ["허", 0.6], ["남", 0.5], ["노", 0.5],
  ["하", 0.4], ["곽", 0.4], ["성", 0.4], ["차", 0.4], ["주", 0.4], ["우", 0.4], ["구", 0.4], ["민", 0.3], ["진", 0.3], ["나", 0.3]];
const SUR_W = SUR.reduce((s, [, w]) => s + w, 0);
export const GIVEN = ("민준 서준 도윤 예준 시우 하준 주원 지호 지후 준우 준서 도현 건우 현우 우진 선우 서진 연우 유준 정우 " +
  "승우 승현 시윤 준혁 은우 지환 승민 지우 유찬 윤우 이준 민재 시후 진우 지훈 은찬 수호 태윤 재윤 로운 " +
  "서연 서윤 지우 서현 하은 하윤 민서 지유 윤서 채원 지민 수아 지아 지윤 다은 은서 예은 수빈 소율 예린 " +
  "지원 소윤 유나 채은 하린 시은 예원 서영 유진 아린 나은 다인 가은 서아 하율 연서 수민 윤아 지안 시아 " +
  "태민 동현 재민 현준 민규 성민 예찬 하람 다온 이안 라온 한결 지성 주안 하진 도경 은호 시원 준영 유빈").split(" ");
/** 씨앗으로 서로 다른 이름 n개 */
export function namesOf(seed, n) {
  const R = rng(hashSeed("names", seed));
  const out = [], seen = new Set(), given = new Set();
  let guard = 0;
  while (out.length < n && guard++ < 5000) {
    let r = R() * SUR_W, s = SUR[0][0];
    for (const [k, w] of SUR) { if ((r -= w) <= 0) { s = k; break; } }
    const g = GIVEN[rint(R, GIVEN.length)];
    if (g[0] === s) continue;                     // 이이안 · 윤윤서처럼 성과 이름 첫 글자가 같으면 다시
    const full = s + g;
    // 한 화면에 같은 이름(성만 다른 것 포함)이 겹치면 헷갈리니 이름 글자도 겹치지 않게(사람이 많으면 허용)
    if (seen.has(full) || (n <= GIVEN.length * 0.7 && given.has(g))) continue;
    seen.add(full); given.add(g); out.push(full);
  }
  return out;
}

/* ══════════ 빠르기 ══════════ */
export const SPEEDS = [0.5, 1, 1.5, 2];
export const spFmt = (v) => `${v}×`;
/** 빠르기를 바꿔도 그 자리에서 이어지게(경과 × 옛 빠르기 = 새 경과 × 새 빠르기) */
export const keepSpeed = (o, n, el) => (el * (o.sp || 1)) / (n.sp || 1);

/* ══════════ 조합 · 큰 분수 ══════════ */
export function comb(n, k) {
  if (k < 0 || k > n) return 0;
  k = Math.min(k, n - k);
  let r = 1;
  for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i;
  return Math.round(r);
}
export function combBig(n, k) {
  if (k < 0 || k > n) return 0n;
  k = Math.min(k, n - k);
  let r = 1n;
  for (let i = 1; i <= k; i++) r = (r * BigInt(n - k + i)) / BigInt(i);
  return r;
}
const gcdB = (a, b) => { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) [a, b] = [b, a % b]; return a; };
export function fracBig(n, d) { const g = gcdB(n, d) || 1n; return [n / g, d / g]; }
const SUP = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
/** 1/분모 꼴이 너무 길면 약 a × 10⁻ⁿ */
export function sciOf(nB, dB) {
  const n = Number(nB), d = Number(dB);
  if (!(d > 0)) return "";
  const v = n / d;
  if (v === 0) return "0";
  const e = Math.floor(Math.log10(v));
  const m = v / 10 ** e;
  return `약 ${m.toFixed(1)} × 10${String(e).split("").map((c) => SUP[c]).join("")}`;
}
/** 큰 분수를 MText 글자로: 자릿수가 많으면 약 … 꼴 */
export function bigFracText(nB, dB, maxDigits = 9) {
  const [a, b] = fracBig(nB, dB);
  if (b === 1n) return String(a);
  if (String(b).length > maxDigits) return sciOf(a, b);
  return `{${a}/${b}}`;
}
/** 확률 백분율(작으면 소수 둘째 자리까지) */
export function pctText(n, d) {
  const v = (100 * Number(n)) / Number(d);
  if (v >= 10) return `${v.toFixed(1)}%`;
  if (v >= 0.1) return `${v.toFixed(2)}%`;
  if (v >= 0.001) return `${v.toFixed(3)}%`;
  return "";
}

/* ══════════ 시간 ══════════ */
/** 같은 길이 D 장면 N개를 끝없이: [몇 번째(전체), 그 장면 안 시각] */
export function cycleAt(e, D, N) {
  const k = Math.floor(Math.max(0, e) / D);
  return { k, i: N ? k % N : 0, t: Math.max(0, e) - k * D };
}
