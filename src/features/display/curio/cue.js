// ashrain.out — 수학 호기심 액자: 당구로 보는 대칭(빈쿠션 치기) 계산 (curio/cue.js)
// 당구대(가상 배치): 가로 0~16, 세로 0~8 — 1칸 = 다이아몬드 반 칸(약 17.75 cm), 다이아몬드는 짝수 칸마다.
// 흰 공(C)으로 빨간 공(R)을 맞히고 싶은데 노란 공(Y)이 길을 막았다 → 쿠션을 거울로 보고 거울 속 빨간 공(R′)을 곧게 겨냥한다.
//   중등: 직선 CR′ 의 식 → 쿠션(y = 8 등)과 만나는 점 H. 튕긴 뒤 기울기는 부호만 바뀐다.
//   초등: 쿠션까지의 칸 수 a : b 로 가로(세로) 거리를 나눈 곳이 H — 들어간 각 = 나온 각.
// 쿠션 두 번(모서리 쪽)은 거울을 두 번: R″ = 두 쿠션에 차례로 비친 빨간 공.
// 공은 점(가운데)으로 본다 — 실제 당구에서는 공의 반지름만큼 쿠션 안쪽 선에서 튕긴다.
import { rng, rint, hashSeed, frac, fs, fsRaw, num, paren, pt, lineOf, eqText, MINUS } from "./kit.js";

export const TBL = { w: 16, h: 8 };
/** 쿠션: 그 쿠션이 놓인 축과 값 · 이름 */
export const CUSH = {
  top: { axis: "y", v: 8, name: "위쪽 쿠션" },
  bottom: { axis: "y", v: 0, name: "아래쪽 쿠션" },
  left: { axis: "x", v: 0, name: "왼쪽 쿠션" },
  right: { axis: "x", v: 16, name: "오른쪽 쿠션" },
};
/** 쿠션 c 에 비친 점 */
export const reflect = (p, c) => (CUSH[c].axis === "y" ? [p[0], 2 * CUSH[c].v - p[1]] : [2 * CUSH[c].v - p[0], p[1]]);
/** 쿠션 c 의 식 글자 */
export const cushEq = (c) => `${CUSH[c].axis} = ${CUSH[c].v}`;
/** 쿠션까지 거리 */
const away = (p, c) => Math.abs((CUSH[c].axis === "y" ? p[1] : p[0]) - CUSH[c].v);
/** 분수 [n, d] 의 실수 */
const fv = (f) => f[0] / f[1];

/** 직선 C → Q 가 축 axis = v 와 만나는 점(분수 좌표): [[xn, xd], [yn, yd]] */
function meetAt(Cp, Q, axis, v) {
  const dx = Q[0] - Cp[0], dy = Q[1] - Cp[1];
  if (axis === "y") {
    // x = Cx + dx (v − Cy) / dy
    return [frac(Cp[0] * dy + dx * (v - Cp[1]), dy), [v, 1]];
  }
  return [[v, 1], frac(Cp[1] * dx + dy * (v - Cp[0]), dx)];
}
/** 점 p 와 선분 ab 사이 거리 */
function segDist(p, a, b) {
  const vx = b[0] - a[0], vy = b[1] - a[1], L = vx * vx + vy * vy;
  const k = L ? Math.max(0, Math.min(1, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L)) : 0;
  return Math.hypot(p[0] - a[0] - vx * k, p[1] - a[1] - vy * k);
}
/** 쿠션과 이루는 각(도) — 0 이면 쿠션과 나란히 */
function angleTo(a, b, c) {
  const dx = Math.abs(b[0] - a[0]), dy = Math.abs(b[1] - a[1]);
  return (Math.atan2(CUSH[c].axis === "y" ? dy : dx, CUSH[c].axis === "y" ? dx : dy) * 180) / Math.PI;
}
const inTable = (p, m = 0) => p[0] >= m && p[0] <= TBL.w - m && p[1] >= m && p[1] <= TBL.h - m;
const pick = (R, arr) => arr[rint(R, arr.length)];

/**
 * 한 공 배치(씨앗 seed 의 k 번째):
 *   { k, two, cush: [c] | [c1, c2], C, R, Y, img(R′ 또는 R″), hits: [H] | [P, Q] (실수 좌표), hf: 분수 좌표, legs(경로 점들) }
 */
const MEMO = new Map();
export function cueShot(seed, k) {
  const key = seed * 100003 + k;
  if (MEMO.has(key)) return MEMO.get(key);
  const R = rng(hashSeed("cue", seed, k));
  const two = hashSeed("cue2", seed, k) % 4 === 0;
  let out = null;
  for (let tries = 0; tries < 3000 && !out; tries++) out = two ? tryTwo(R) : tryOne(R);
  if (!out) out = FALLBACK;
  out = { k, ...out };
  MEMO.set(key, out);
  if (MEMO.size > 40) MEMO.delete(MEMO.keys().next().value);
  return out;
}
const FALLBACK = (() => {
  const C = [2, 3], Rr = [14, 6], c = "top";
  const img = reflect(Rr, c);
  const H = meetAt(C, img, "y", 8);
  return { two: false, cush: [c], C, R: Rr, Y: [8, 4.5], img, hf: [H], hits: [[fv(H[0]), fv(H[1])]] };
})();

/** 노란 공 자리: 선분 CR 위(가운데쯤) — 쿠션으로 돌아가는 길과는 떨어져야 한다 */
function blocker(R, C, Rr, path) {
  for (let t = 0; t < 12; t++) {
    const f = 0.38 + R() * 0.24;
    const Y = [Math.round((C[0] + (Rr[0] - C[0]) * f) * 10) / 10, Math.round((C[1] + (Rr[1] - C[1]) * f) * 10) / 10];
    if (!inTable(Y, 0.6)) continue;
    if (Math.hypot(Y[0] - C[0], Y[1] - C[1]) < 1.6 || Math.hypot(Y[0] - Rr[0], Y[1] - Rr[1]) < 1.6) continue;
    let ok = true;
    for (let i = 1; i < path.length; i++) if (segDist(Y, path[i - 1], path[i]) < 1.1) ok = false;
    if (ok) return Y;
  }
  return null;
}
function tryOne(R) {
  const c = pick(R, ["top", "bottom", "top", "bottom", "left", "right"]);
  const ax = CUSH[c].axis;
  const C = [1 + rint(R, 15), 1 + rint(R, 7)];
  const Rr = [1 + rint(R, 15), 1 + rint(R, 7)];
  const dC = away(C, c), dR = away(Rr, c);
  if (dC < 2 || dR < 1 || dR > 4) return null;
  if (Math.hypot(C[0] - Rr[0], C[1] - Rr[1]) < 5) return null;
  const img = reflect(Rr, c);
  if ((ax === "y" && C[0] === img[0]) || (ax === "x" && C[1] === img[1])) return null;
  const H = meetAt(C, img, ax, CUSH[c].v);
  const along = ax === "y" ? H[0] : H[1];
  if (along[1] !== 1) return null;                         // 쿠션의 칸 위(정수)에 닿게
  const Hp = [fv(H[0]), fv(H[1])];
  const lim = ax === "y" ? TBL.w : TBL.h;
  if (along[0] < 1 || along[0] > lim - 1) return null;
  const ang = angleTo(C, Hp, c);
  if (ang < 22 || ang > 72) return null;
  const Y = blocker(R, C, Rr, [C, Hp, Rr]);
  if (!Y) return null;
  return { two: false, cush: [c], C, R: Rr, Y, img, hf: [H], hits: [Hp] };
}
function tryTwo(R) {
  const cy = pick(R, ["top", "bottom"]), cx = pick(R, ["left", "right"]);
  const C = [1 + rint(R, 15), 1 + rint(R, 7)];
  const Rr = [1 + rint(R, 15), 1 + rint(R, 7)];
  if (away(Rr, cy) < 1 || away(Rr, cy) > 3 || away(Rr, cx) < 1 || away(Rr, cx) > 4) return null;
  if (away(C, cy) < 2 || away(C, cx) < 3) return null;
  if (Math.hypot(C[0] - Rr[0], C[1] - Rr[1]) < 4) return null;
  const img = reflect(reflect(Rr, cx), cy);                // 두 쿠션에 차례로 비친 자리 R″ (순서와 상관없이 같다)
  if (C[0] === img[0] || C[1] === img[1]) return null;
  // 어느 쿠션을 먼저 만나나: 직선이 y = cy 와 x = cx 를 지나는 때(매개변수)
  const ty = (CUSH[cy].v - C[1]) / (img[1] - C[1]), tx = (CUSH[cx].v - C[0]) / (img[0] - C[0]);
  if (!(ty > 0 && ty < 1 && tx > 0 && tx < 1) || Math.abs(ty - tx) < 0.12) return null;
  const first = ty < tx ? cy : cx, second = first === cy ? cx : cy;
  const P = meetAt(C, img, CUSH[first].axis, CUSH[first].v);
  // 둘째 쿠션: 첫 거울 속에 비친 둘째 쿠션 — 같은 축이라 값이 그대로(모서리 쪽 두 쿠션은 서로 수직)
  const Q2 = meetAt(C, img, CUSH[second].axis, CUSH[second].v);
  const Pp = [fv(P[0]), fv(P[1])], Q2p = [fv(Q2[0]), fv(Q2[1])];
  const Qp = reflect(Q2p, first);
  const Qf = CUSH[first].axis === "y" ? [Q2[0], frac(2 * CUSH[first].v * Q2[1][1] - Q2[1][0], Q2[1][1])] : [frac(2 * CUSH[first].v * Q2[0][1] - Q2[0][0], Q2[0][1]), Q2[1]];
  const onRail = (p, c) => (CUSH[c].axis === "y" ? p[0] >= 0.8 && p[0] <= TBL.w - 0.8 : p[1] >= 0.8 && p[1] <= TBL.h - 0.8);
  if (!onRail(Pp, first) || !onRail(Qp, second)) return null;
  // 분모가 너무 크면 판서가 어려우니 6 이하
  for (const f of [...P, ...Qf]) if (f[1] > 6) return null;
  const a1 = angleTo(C, Pp, first);
  if (a1 < 20 || a1 > 70) return null;
  if (Math.hypot(Pp[0] - Qp[0], Pp[1] - Qp[1]) < 2) return null;
  const Y = blocker(R, C, Rr, [C, Pp, Qp, Rr]);
  if (!Y) return null;
  return { two: true, cush: [first, second], C, R: Rr, Y, img, hf: [P, Qf], q2: Q2, hits: [Pp, Qp] };
}

/** 흰 공이 지나는 길(점들) */
export const pathOf = (s) => [s.C, ...s.hits, s.R];

/* ══════════ 박자 ══════════ */
export const CUE_D = 17000;
/** 한 공의 박자(ms) */
export function cueTimes(s) {
  if (!s.two) {
    return { intro: [0, 900], block: [900, 2300], mirror: [2300, 3300], image: [3300, 4200], line: [4200, 5400], hit: [5400, 6200],
      fold: [6200, 7600], roll: [7600, 10200], knock: [10200, 11000], fade: [CUE_D - 800, CUE_D] };
  }
  return { intro: [0, 900], block: [900, 2300], mirror: [2300, 3300], image: [3300, 4200], line: [4200, 5600], hit: [5600, 6300],
    hit2: [6300, 7000], fold: [7000, 8200], roll: [8200, 11400], knock: [11400, 12200], fade: [CUE_D - 800, CUE_D] };
}
/** 경과 e → { s(이 공), k, t(공 안 시각), T(박자) } */
export function cueAt(seed, e) {
  const k = Math.floor(Math.max(0, e) / CUE_D);
  const s = cueShot(seed, k);
  return { s, k, t: Math.max(0, e) - k * CUE_D, T: cueTimes(s) };
}

/* ══════════ 판서 ══════════ */
const fpt = (f) => `(${fs(f[0][0], f[0][1])}, ${fs(f[1][0], f[1][1])})`;
/** 쿠션 c 에 비친 좌표 계산 글자: y = 8 → 8 + (8 − 6) = 10 */
function mirrorCalc(p, c) {
  const v = CUSH[c].v, u = CUSH[c].axis === "y" ? p[1] : p[0];
  const r = 2 * v - u;
  return `${CUSH[c].axis}좌표: ${num(v)} + (${num(v)} ${MINUS} ${paren(u)}) = ${num(r)}`;
}
/**
 * 판서 줄 — [{ s, at(박자 이름), hi?, small?, col? }]
 */
export function cueSteps(s, mode) {
  const T = cueTimes(s);
  const L = lineOf(s.C, s.img);
  const sl = `{${num(s.img[1])} ${MINUS} ${paren(s.C[1])}/${num(s.img[0])} ${MINUS} ${paren(s.C[0])}}`;
  const red = fs(L.m[0], L.m[1]), raw = fsRaw(L.dy, L.dx);
  const slope = `기울기 = ${[sl, raw, red].filter((v, i, a) => i === 0 || v !== a[i - 1]).join(" = ")}`;
  const negSlope = fs(-L.m[0], L.m[1]);
  if (!s.two) {
    const c = s.cush[0], H = s.hf[0];
    if (mode === "m") {
      return [
        { s: `흰 공 C${pt(s.C)} · 빨간 공 R${pt(s.R)}`, at: T.intro[1] - 300 },
        { s: `${CUSH[c].name} ${cushEq(c)}에 비친 R′${pt(s.img)}`, at: T.image[0] + 200 },
        { s: mirrorCalc(s.R, c), at: T.image[0] + 500, small: true },
        { s: slope, at: T.line[0] + 200 },
        { s: `직선 CR′: ${eqText(L)}`, at: T.line[0] + 800 },
        { s: `${cushEq(c)}과 만나는 점 H${fpt(H)}`, at: T.hit[0] + 100, hi: true },
        { s: `튕긴 뒤 기울기 ${negSlope} — 부호만 바뀌어요`, at: T.fold[0] + 400, small: true, col: "teal" },
      ];
    }
    // 초등: 쿠션까지 칸 수의 비로 나누기
    const ax = CUSH[c].axis, dC = away(s.C, c), dR = away(s.R, c);
    const i = ax === "y" ? 0 : 1, run = s.R[i] - s.C[i], Hd = (fv(ax === "y" ? H[0] : H[1]) - s.C[i]);
    const dir = ax === "y" ? (run > 0 ? "오른쪽으로" : "왼쪽으로") : (run > 0 ? "위로" : "아래로");
    const pos = fv(ax === "y" ? H[0] : H[1]);
    return [
      { s: "노란 공이 길을 막았어요 — 쿠션으로 돌아가요", at: T.block[0] + 300 },
      { s: "쿠션을 거울로 보면 거울 속 빨간 공까지 곧은 길", at: T.image[0] + 200 },
      { s: `쿠션까지 흰 공 ${dC}칸, 빨간 공 ${dR}칸 → ${dC} : ${dR}`, at: T.line[0] + 300 },
      { s: `${ax === "y" ? "가로" : "세로"} ${Math.abs(run)}칸을 ${dC} : ${dR}로 나누면 ${Math.abs(run)} × ${dC} ÷ ${dC + dR} = ${Math.abs(Hd)}`, at: T.line[0] + 900 },
      { s: `흰 공에서 ${dir} ${Math.abs(Hd)}칸 — 쿠션의 ${num(pos)}칸 자리`, at: T.hit[0] + 100, hi: true },
      { s: "들어간 각 = 나온 각", at: T.fold[0] + 400, small: true, col: "teal" },
    ];
  }
  const [c1, c2] = s.cush, [P, Q] = s.hf;
  if (mode === "m") {
    const Q2 = s.q2;
    return [
      { s: `흰 공 C${pt(s.C)} · 빨간 공 R${pt(s.R)}`, at: T.intro[1] - 300 },
      { s: `쿠션 ${cushEq(c2)}, ${cushEq(c1)}에 차례로 비친 R″${pt(s.img)}`, at: T.image[0] + 200 },
      { s: slope, at: T.line[0] + 200 },
      { s: `직선 CR″: ${eqText(L)}`, at: T.line[0] + 800 },
      { s: `${cushEq(c1)}과 만나는 점 P${fpt(P)}`, at: T.hit[0] + 100 },
      { s: `${cushEq(c2)}과 만나는 점 ${fpt(Q2)} → 접으면 Q${fpt(Q)}`, at: T.hit2[0] + 100, hi: true },
      { s: `기울기 ${red} → ${negSlope} → ${red} — 튕길 때마다 부호가 바뀌어요`, at: T.fold[0] + 400, small: true, col: "teal" },
    ];
  }
  return [
    { s: "노란 공이 길을 막았어요 — 쿠션 두 번!", at: T.block[0] + 300 },
    { s: "거울을 두 번 비춰요: 빨간 공 → R″", at: T.image[0] + 200 },
    { s: "R″를 곧게 겨냥하면 길이 두 번 꺾여요", at: T.line[0] + 400 },
    { s: `첫 쿠션 P, 둘째 쿠션 Q`, at: T.hit[0] + 100 },
    { s: "튕길 때마다 들어간 각 = 나온 각", at: T.fold[0] + 400, hi: true },
  ];
}
/** 최소화 화면의 한 줄 요약 — stage 0: 쿠션만 · 1: 직선의 식까지 · 2: 만나는 점까지 */
export function cueSummary(s, mode, stage = 2) {
  const eq = eqText(lineOf(s.C, s.img));
  if (!s.two) {
    const c = s.cush[0];
    if (mode !== "m") return `${CUSH[c].name} · 들어간 각 = 나온 각`;
    return stage === 0 ? `${CUSH[c].name} ${cushEq(c)}` : stage === 1 ? `직선 CR′: ${eq}` : `${eq} · H${fpt(s.hf[0])}`;
  }
  if (mode !== "m") return "쿠션 두 번 · 거울을 두 번";
  return stage === 0 ? `쿠션 ${cushEq(s.cush[0])} → ${cushEq(s.cush[1])}` : stage === 1 ? `직선 CR″: ${eq}` : `${eq} · P${fpt(s.hf[0])} · Q${fpt(s.hf[1])}`;
}
