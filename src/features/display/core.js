// ashrain.out — 교실 모니터 장면 엔진: 순수 계산부 (core.js)
// 위치: src/features/display/core.js — JSX 없음. 장면(.jsx)과 검산 테스트(tests/display.test.mjs)가 함께 쓴다.
//
// 원칙
//   · 장면은 "시간 t(ms) → 그림" 의 순수 함수다. 같은 t 면 같은 그림 — 그래서 초등/중등 두 판을
//     같은 시각에 겹쳐 그릴 수 있고(토글 오버랩), 어느 순간이든 다시 그릴 수 있다.
//   · 입체는 직교 투영(평행선이 평행하게 보인다 — 교과서 그림과 같은 규약).
//   · 좌표: 세계 x(오른쪽) · y(안쪽) · z(위). 화면은 SVG(아래로 +y).

export const TAU = Math.PI * 2;
export const rad = (d) => (d * Math.PI) / 180;
export const deg = (r) => (r * 180) / Math.PI;
export const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
export const lerp = (a, b, k) => a + (b - a) * k;
export const mix2 = (p, q, k) => [lerp(p[0], q[0], k), lerp(p[1], q[1], k)];
export const mix3 = (p, q, k) => [lerp(p[0], q[0], k), lerp(p[1], q[1], k), lerp(p[2], q[2], k)];

/* ══════════ 이징 ══════════ */
export const E = {
  lin: (k) => k,
  in: (k) => k * k * k,
  out: (k) => 1 - Math.pow(1 - k, 3),
  io: (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
  sine: (k) => 0.5 - 0.5 * Math.cos(Math.PI * k),
  back: (k) => { const c = 1.6; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); },
  drop: (k) => { // 떨어져 살짝 튀었다 멈춤
    if (k < 0.72) return Math.pow(k / 0.72, 2);
    const u = (k - 0.72) / 0.28; return 1 - 0.07 * Math.sin(Math.PI * u);
  },
};

/** t 가 [a, b] 구간에서 0→1 로 가는 진행도 (이징 적용) */
export function seg(t, a, b, ease = E.io) {
  if (t <= a) return 0;
  if (t >= b) return 1;
  return ease((t - a) / (b - a));
}
/** 나타났다 사라지기: [a, a+fi] 페이드 인, [b-fo, b] 페이드 아웃 */
export function win(t, a, b = Infinity, fi = 450, fo = 450) {
  if (t < a || t > b) return 0;
  return Math.min(seg(t, a, a + fi, E.sine), b === Infinity ? 1 : 1 - seg(t, b - fo, b, E.sine));
}

/**
 * 박자표 — 초등·중등 두 판이 같은 박자를 공유해 장면이 맞물린다.
 *   const B = beats([["intro", 2500], ["build", 9000], ...]);
 *   B.a.build (시작) · B.b.build (끝) · B.p("build", t) (진행도) · B.dur
 */
export function beats(list) {
  const a = {}, b = {};
  let acc = 0;
  for (const [name, ms] of list) { a[name] = acc; acc += ms; b[name] = acc; }
  return {
    a, b, dur: acc,
    p: (name, t, ease = E.io) => seg(t, a[name], b[name], ease),
    in: (name, t) => t >= a[name] && t < b[name],
  };
}

/* ══════════ 수 표기 ══════════ */
/** 소수 둘째 자리까지, 끝의 0 은 지움: 31.40 → 31.4, 207.24 → 207.24, 57.00 → 57 */
export function fmt(n, dp = 2) {
  const s = (Math.round(n * 10 ** dp) / 10 ** dp).toFixed(dp);
  return s.replace(/\.?0+$/, "");
}

/* ══════════ 2D 벡터·경로 ══════════ */
export const add2 = (p, q) => [p[0] + q[0], p[1] + q[1]];
export const sub2 = (p, q) => [p[0] - q[0], p[1] - q[1]];
export const mul2 = (p, k) => [p[0] * k, p[1] * k];
export const len2 = (p) => Math.hypot(p[0], p[1]);
export const dist2 = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]);
export const rot2 = (p, a, c = [0, 0]) => {
  const s = Math.sin(a), k = Math.cos(a), x = p[0] - c[0], y = p[1] - c[1];
  return [c[0] + x * k - y * s, c[1] + x * s + y * k];
};
/** 원 위의 점 — 수학 각도(도, 반시계)를 SVG(아래 +y) 화면에 */
export const polar = (c, r, aDeg) => [c[0] + r * Math.cos(rad(aDeg)), c[1] - r * Math.sin(rad(aDeg))];

/** 호를 꺾은선으로 (수학 각도, 도) */
export function arcPts(c, r, a0, a1, n) {
  const N = n || Math.max(8, Math.ceil(Math.abs(a1 - a0) / 3));
  const out = [];
  for (let i = 0; i <= N; i++) out.push(polar(c, r, a0 + ((a1 - a0) * i) / N));
  return out;
}
export function polyLen(pts, closed = false) {
  let L = 0;
  for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  if (closed && pts.length > 1) L += Math.hypot(pts[0][0] - pts.at(-1)[0], pts[0][1] - pts.at(-1)[1]);
  return L;
}
/** 꺾은선의 앞쪽 p(0~1) 만큼 — 선이 그려지는 연출 */
export function partial(pts, p, closed = false) {
  const P = closed ? [...pts, pts[0]] : pts;
  if (p >= 1) return P;
  if (p <= 0 || P.length < 2) return [P[0]];
  const total = polyLen(P);
  let need = total * p;
  const out = [P[0]];
  for (let i = 1; i < P.length; i++) {
    const d = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]);
    if (need <= d) { out.push(mix2(P[i - 1], P[i], d ? need / d : 0)); return out; }
    out.push(P[i]); need -= d;
  }
  return out;
}
/** 꺾은선 위 비율 p 지점 */
export function along(pts, p) {
  const q = partial(pts, clamp(p));
  return q.at(-1);
}
const r1 = (v) => Math.round(v * 10) / 10;
export function pathOf(pts, closed = false) {
  if (!pts || !pts.length) return "";
  let d = `M${r1(pts[0][0])} ${r1(pts[0][1])}`;
  for (let i = 1; i < pts.length; i++) d += `L${r1(pts[i][0])} ${r1(pts[i][1])}`;
  return closed ? d + "Z" : d;
}
/** 부채꼴 꺾은선 (중심 포함, 닫힘) */
export function sectorPts(c, r, a0, a1, n) {
  return [c, ...arcPts(c, r, a0, a1, n)];
}
/** 다각형 무게중심(꼭짓점 평균) */
export const centroid2 = (pts) => mul2(pts.reduce((s, p) => add2(s, p), [0, 0]), 1 / pts.length);

/* ══════════ 3D ══════════ */
export const add3 = (p, q) => [p[0] + q[0], p[1] + q[1], p[2] + q[2]];
export const sub3 = (p, q) => [p[0] - q[0], p[1] - q[1], p[2] - q[2]];
export const mul3 = (p, k) => [p[0] * k, p[1] * k, p[2] * k];
export const dot3 = (p, q) => p[0] * q[0] + p[1] * q[1] + p[2] * q[2];
export const cross3 = (p, q) => [p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0]];
export const norm3 = (p) => { const L = Math.hypot(p[0], p[1], p[2]) || 1; return [p[0] / L, p[1] / L, p[2] / L]; };
export const centroid3 = (pts) => mul3(pts.reduce((s, p) => add3(s, p), [0, 0, 0]), 1 / pts.length);
/** 면의 법선(꼭짓점 순서의 오른손 방향) */
export function normal3(pts) {
  // 뉴웰 방법 — 오목·약간 휜 면에도 안정적
  let nx = 0, ny = 0, nz = 0;
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i], b = pts[(i + 1) % pts.length];
    nx += (a[1] - b[1]) * (a[2] + b[2]);
    ny += (a[2] - b[2]) * (a[0] + b[0]);
    nz += (a[0] - b[0]) * (a[1] + b[1]);
  }
  return norm3([nx, ny, nz]);
}

/**
 * 직교 카메라. yaw = z축 둘레 회전(도), pitch = 내려다보는 각(0 정면 ~ 90 바로 위).
 *   cam.p([x,y,z]) → [화면x, 화면y, 깊이(클수록 멂)]
 *   cam.v(방향) → [오른쪽, 위, 깊이] 성분 — 면이 카메라를 향하면 깊이 성분 < 0
 */
export function camera({ yaw = -35, pitch = 30, scale = 100, cx = 800, cy = 450, target = [0, 0, 0] } = {}) {
  const cY = Math.cos(rad(yaw)), sY = Math.sin(rad(yaw));
  const cP = Math.cos(rad(pitch)), sP = Math.sin(rad(pitch));
  const v = (n) => {
    const x1 = n[0] * cY - n[1] * sY, y1 = n[0] * sY + n[1] * cY, z1 = n[2];
    return [x1, z1 * cP + y1 * sP, y1 * cP - z1 * sP];
  };
  const p = (q) => {
    const r = v([q[0] - target[0], q[1] - target[1], q[2] - target[2]]);
    return [cx + scale * r[0], cy - scale * r[1], r[2]];
  };
  return { p, v, yaw, pitch, scale, cx, cy, target };
}
const LIGHT = norm3([-0.42, 0.78, -0.46]);   // 화면 기준: 왼쪽 위 앞에서 오는 빛
/** 법선(세계) → 밝기 0.55~1.08 */
export function lambert(cam, n) {
  const w = cam.v(n);
  const d = w[0] * LIGHT[0] + w[1] * LIGHT[1] + w[2] * LIGHT[2];
  return 0.6 + 0.48 * Math.max(0, Math.abs(d));
}
/** 면이 카메라를 향하는가 (바깥 법선 기준) */
export const facing = (cam, n) => cam.v(n)[2] < 0;

/* ── 회전 (축 위의 점 P, 방향 u, 각 a 라디안) — 3×4 아핀 행렬 ── */
export function axisRot(P, u, a) {
  const [x, y, z] = norm3(u), c = Math.cos(a), s = Math.sin(a), C = 1 - c;
  const R = [
    [c + x * x * C, x * y * C - z * s, x * z * C + y * s],
    [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
    [z * x * C - y * s, z * y * C + x * s, c + z * z * C],
  ];
  const t = [0, 1, 2].map((i) => P[i] - (R[i][0] * P[0] + R[i][1] * P[1] + R[i][2] * P[2]));
  return { R, t };
}
export const IDENT = { R: [[1, 0, 0], [0, 1, 0], [0, 0, 1]], t: [0, 0, 0] };
export function apply(M, p) {
  const { R, t } = M;
  return [
    R[0][0] * p[0] + R[0][1] * p[1] + R[0][2] * p[2] + t[0],
    R[1][0] * p[0] + R[1][1] * p[1] + R[1][2] * p[2] + t[1],
    R[2][0] * p[0] + R[2][1] * p[1] + R[2][2] * p[2] + t[2],
  ];
}
/** A 다음에 B 를 적용하는 변환 (B∘A) */
export function compose(B, A) {
  const R = [0, 1, 2].map((i) => [0, 1, 2].map((j) =>
    B.R[i][0] * A.R[0][j] + B.R[i][1] * A.R[1][j] + B.R[i][2] * A.R[2][j]));
  const t = apply({ R: B.R, t: B.t }, A.t);
  return { R, t };
}
export const rotZ = (p, a, c = [0, 0, 0]) => apply(axisRot(c, [0, 0, 1], a), p);

/**
 * 전개도 접기.
 *   faces: [{ id, poly: [[x,y],…](전개도 평면 좌표), parent, hinge: [[x,y],[x,y]], angle(도) }]
 *   amt(face) → 0(펼침)~1(접힘). 접으면 면이 바닥(z=0)에서 위(+z)로 일어선다.
 *   반환: { id: [[x,y,z],…] }
 */
export function foldNet(faces, amt) {
  const byId = Object.fromEntries(faces.map((f) => [f.id, f]));
  const M = {};
  const get = (id) => {
    if (M[id]) return M[id];
    const f = byId[id];
    if (!f.parent) return (M[id] = IDENT);
    let [P, Q] = f.hinge;
    // 자식 면이 경첩 P→Q 의 왼쪽에 있도록 방향을 맞추면 +각 회전이 위로 일으킨다
    const c = centroid2(f.poly);
    const cr = (Q[0] - P[0]) * (c[1] - P[1]) - (Q[1] - P[1]) * (c[0] - P[0]);
    if (cr < 0) [P, Q] = [Q, P];
    const A = axisRot([P[0], P[1], 0], [Q[0] - P[0], Q[1] - P[1], 0], rad(f.angle * amt(f)));
    return (M[id] = compose(get(f.parent), A));
  };
  const out = {};
  for (const f of faces) out[f.id] = f.poly.map((p) => apply(get(f.id), [p[0], p[1], 0]));
  return out;
}

/* ══════════ 색 ══════════ */
function hexRgb(h) {
  const s = h.replace("#", "");
  const n = parseInt(s.length === 3 ? s.split("").map((c) => c + c).join("") : s, 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
/** 밝기 k 배 (1 = 그대로, <1 어둡게, >1 밝게 — 흰색 쪽으로) */
export function shade(hex, k) {
  const [r, g, b] = hexRgb(hex);
  const f = (v) => Math.round(k <= 1 ? v * k : v + (255 - v) * (k - 1));
  return `rgb(${clamp(f(r), 0, 255)},${clamp(f(g), 0, 255)},${clamp(f(b), 0, 255)})`;
}
/** 두 색 섞기 */
export function blend(h1, h2, k) {
  const a = hexRgb(h1), b = hexRgb(h2);
  return `rgb(${[0, 1, 2].map((i) => Math.round(lerp(a[i], b[i], k))).join(",")})`;
}

/* ══════════ 결정적 난수 (장면이 매번 같게) ══════════ */
export function rng(seed = 1) {
  let s = seed >>> 0 || 1;
  return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
}
