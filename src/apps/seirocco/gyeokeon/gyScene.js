// 시록고 · 격언 도우미 — 격언 그림 (GY-2 그림 엔진)
// 격언 하나의 고사를 붓으로 그린다. 가운데 원이 그달 코드이고, 장면은 항목의 scene에서 조립한다.
//   scene.circle   원이 무엇인가(해 · 우물 · 수레바퀴 …) → 원 둘레 꾸밈
//   scene.figures  [{who, pose, clock}] → 사람 · 동물, 시계 방향 자리
//   scene.props    소품 · 배경(산 · 강 · 구름 …)
//   scene.grows    아이가 해낸 만큼 늘어나는 표시 — 그달 유형 색은 여기에만 쓴다
// 정답률은 그림 어디에도 넣지 않는다(HANDOFF-격언그림-시록고-v1). 같은 항목 · 같은 코드면 같은 그림.
//
//   drawScene(entry)                                   찾아보기: 코드 없는 그림
//   drawScene(entry, {months, cum, R, name, label, nth}) 코드로 고르기: 그 아이의 지난 달 결이 원 안에 든다
//   옵션 theme: 'light'(한지 · 먹) | 'dark'(감지 · 금니)
//
// 붓획 도구(ease · cr · outline · bl …)와 여섯 장면(우공이산 · 각주구검 · 알묘조장 · 숙능생교 · 화사첨족 · 독서백편)은
// 격언 그림 시안(gy.js)에서 옮겼다. 나머지는 scene 낱말을 그리기 갈래로 묶어 조립한다.

import { TYPES, dominantType } from "./gyPick.js";

export const PALETTE = {
  light: { paper: "#EFE6D2", ink: "#2A2520", gold: "#9C6F12", ju: "#A8321F" },
  dark: { paper: "#1B2340", ink: "#D8B865", gold: "#EBCB6E", ju: "#E26A4C" },
};
/** 유형 색(옛 안료). 갈림길은 앱 칩과 같은 #B8901F */
export const TYPE_COLOR = {
  rush: "#C8452D", shadow: "#CF7F2A", cross: "#B8901F", steady: "#5E8C4A", stubborn: "#2E897D",
  cue: "#3A7DB0", evap: "#3B4F9A", shrink: "#6C4E9E", auto: "#9A4A8E",
};

const PI = Math.PI, rad = (d) => (d * PI) / 180;
const f1 = (x) => (Math.round(x * 10) / 10).toString();
const seedOf = (str) => { let h = 2166136261; for (const c of str) { h ^= c.codePointAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
const rng = (seed) => { let x = seed || 1; return () => { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return (x >>> 0) / 4294967296; }; };
const pol = (a, q) => [Math.cos(a) * q, Math.sin(a) * q];
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/* ───────────── 붓 ───────────── */
const LINE = [[0, .55], [.12, 1], [.75, .8], [1, .3]], TAPER = [[0, .2], [.2, 1], [.7, .7], [1, 0]];
const EVEN = [[0, .8], [.5, 1], [1, .8]], SOFT = [[0, .1], [.3, 1], [.7, 1], [1, .1]], DAB = [[0, .3], [.4, 1], [1, .2]];
const ease = (pts, t) => { for (let j = 1; j < pts.length; j++) if (t <= pts[j][0]) { const [t0, v0] = pts[j - 1], [t1, v1] = pts[j], u = (t - t0) / ((t1 - t0) || 1); return v0 + (v1 - v0) * (1 - Math.cos(PI * u)) / 2; } return pts[pts.length - 1][1]; };
const walk = (x, y, a0, len, turn, n) => { const c = [], ds = len / n; for (let j = 0; j <= n; j++) { const t = j / n; c.push([x, y, a0 + turn(t)]); const am = a0 + turn(Math.min(1, t + .5 / n)); x += Math.cos(am) * ds; y += Math.sin(am) * ds; } return c; };
const P2 = (x, y) => f1(x) + " " + f1(y);
const outline = (c, h) => { const A = [], B = []; c.forEach(([x, y, a], j) => { const nx = -Math.sin(a), ny = Math.cos(a), w = h[j]; A.push(P2(x + nx * w, y + ny * w)); B.push(P2(x - nx * w, y - ny * w)); }); return "M" + A.join("L") + "L" + B.reverse().join("L") + "Z"; };
const cr = (pts, closed, k) => {
  const n = pts.length, out = [], g = (j) => closed ? pts[(j + n) % n] : pts[Math.max(0, Math.min(n - 1, j))];
  if (n < 2) return pts.map((p) => [p[0], p[1], 0]);
  for (let j = 0; j < (closed ? n : n - 1); j++) {
    const p0 = g(j - 1), p1 = g(j), p2 = g(j + 1), p3 = g(j + 2);
    for (let u = 0; u < k; u++) { const t = u / k, t2 = t * t, t3 = t2 * t, f = (q) => .5 * (2 * p1[q] + (-p0[q] + p2[q]) * t + (2 * p0[q] - 5 * p1[q] + 4 * p2[q] - p3[q]) * t2 + (-p0[q] + 3 * p1[q] - 3 * p2[q] + p3[q]) * t3); out.push([f(0), f(1)]); }
  }
  out.push(closed ? out[0].slice() : pts[n - 1].slice());
  return out.map((p, j) => { const a = out[Math.min(out.length - 1, j + 1)], b = out[Math.max(0, j - 1)]; return [p[0], p[1], Math.atan2(a[1] - b[1], a[0] - b[0])]; });
};

/** 그리기 도구 한 벌. 색은 글자 그대로 넣는다(CSS 변수 없이도 그려지게). */
function pen(pal, rs) {
  const C = (c) => c === "paper" ? pal.paper : c === "gold" ? pal.gold : c === "ju" ? pal.ju : (c || pal.ink);
  const fa = (c, op) => `fill="${C(c)}"` + (op == null || op >= 1 ? "" : ` fill-opacity="${f1(op * 100) / 100}"`);
  const st = (c, w, op) => `fill="none" stroke="${C(c)}" stroke-width="${f1(w * 10) / 10}"` + (op == null || op >= 1 ? "" : ` stroke-opacity="${Math.round(op * 100) / 100}"`);
  const p = {
    rs, pal, C, fa, st,
    /** 붓획: 점들을 지나는 획, 굵기 W, 굵기 모양 prof */
    bl(pts, W, col, op, prof) {
      if (!pts || pts.length < 2) return "";
      const c = cr(pts, false, 6);
      return `<path d="${outline(c, c.map((_, j) => W * ease(prof || LINE, j / (c.length - 1)) * (1 + .14 * (rs() - .5))))}" ${fa(col, op == null ? .9 : op)}/>`;
    },
    area(pts, fill, fop) { const c = cr(pts, true, 6); return `<path d="M${c.map((q) => P2(q[0], q[1])).join("L")}Z" ${fa(fill, fop)}/>`; },
    /** 곧은 다각형(네모 · 판자) */
    poly(pts, fill, fop) { return `<path d="M${pts.map((q) => P2(q[0], q[1])).join("L")}Z" ${fa(fill, fop)}/>`; },
    shape(pts, fill, fop, W, col) { return p.area(pts, fill, fop) + p.bl([...pts, pts[0], pts[1]], W, col, .9, EVEN); },
    blob(cx, cy, rx, ry, rot, jag) { const out = []; for (let u = 0; u < 10; u++) { const a = u / 10 * 2 * PI, q = 1 + jag * (rs() - .5); out.push([cx + (Math.cos(a) * rx * Math.cos(rot) - Math.sin(a) * ry * Math.sin(rot)) * q, cy + (Math.cos(a) * rx * Math.sin(rot) + Math.sin(a) * ry * Math.cos(rot)) * q]); } return out; },
    /** 가는 먹선(붓 맛 없이) */
    line(pts, w, col, op, extra) { return `<path d="M${pts.map((q) => P2(q[0], q[1])).join("L")}" ${st(col, w, op)} stroke-linecap="round" stroke-linejoin="round"${extra || ""}/>`; },
    dot(x, y, r, col, op) { return `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(Math.max(.1, r) * 10) / 10}" ${fa(col, op)}/>`; },
    ring(x, y, r, w, col, op, extra) { return `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(Math.max(.1, r))}" ${st(col, w, op)}${extra || ""}/>`; },
    disc(x, y, r, col, op, sw, scol) { return `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(Math.max(.1, r))}" ${fa(col, op)}` + (sw ? ` stroke="${C(scol)}" stroke-width="${f1(sw * 10) / 10}"` : "") + "/>"; },
    arc(cx, cy, r, a0, a1, n) { const out = []; n = n || Math.max(4, Math.round(Math.abs(a1 - a0) * r / 6)); for (let k = 0; k <= n; k++) { const a = a0 + (a1 - a0) * k / n; out.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } return out; },
    /** 짧은 붓 점(잎 · 이끼 · 풀) */
    tick(x, y, a, l, W, col, op) { return p.bl([[x, y], [x + Math.cos(a) * l, y + Math.sin(a) * l]], W, col, op == null ? .7 : op, TAPER); },
    leaf(x, y, a, l, W, col, op) { const c = walk(x, y, a, l, (t) => .35 * t, 6); return `<path d="${outline(c, c.map((_, j) => W * Math.sin(PI * Math.min(1, .08 + j / 6 * .92))))}" ${fa(col, op == null ? .75 : op)}/>`; },
  };
  return p;
}

/* ───────────── 사람 ───────────── */
/* 붓 인물: 발 = (0,0), 오른쪽을 본다. near 팔은 몸 앞, far 팔은 몸 뒤. 시안의 손그림 자세 아홉 개 */
const FIG = {
  carry: { head: [2.5, -33], body: [[-3.5, -28.6], [4, -28.6], [6.6, -17], [4.6, -14.4], [-4.4, -14.4], [-5.4, -17]], legs: [[[-2, -14.8], [-4.4, -7.6], [-6.4, -.6]], [[2.4, -14.8], [5.2, -7.8], [7.4, 0]]], near: [[3.2, -27], [7.2, -22.2], [6.6, -17.6]], far: [[-1.6, -27], [-4.4, -21.2], [-2.2, -17.4]] },
  dig: { head: [7.5, -28], body: [[0, -24.6], [7.2, -25.2], [8.8, -15], [5.6, -12.8], [-3.6, -12.8], [-3.8, -15.8]], legs: [[[-1.8, -13], [-5, -6.8], [-7.2, 0]], [[3.2, -13], [6.4, -6.8], [7.6, 0]]], near: [[6.4, -23.4], [11.4, -19.4], [14.6, -17.2]], far: [[2.2, -23.4], [8.4, -20.6], [13.4, -18.2]] },
  pull: { head: [12.5, -17], body: [[0, -20.2], [9.2, -19.2], [10.4, -13.2], [7.2, -11.2], [-2.4, -11.8], [-3.2, -15.4]], legs: [[[-1, -12], [-3.2, -6], [-4.4, 0]], [[3.2, -12], [4.6, -6], [5.6, 0]]], near: [[8.4, -18.2], [12.4, -11.2], [14.4, -5.6]], far: [[6.2, -18.4], [10.2, -12.2], [13.2, -6.6]], hand: [14.4, -5.6] },
  pour: { head: [.8, -33], body: [[-4, -28.6], [4, -28.6], [6.2, -9], [4.2, -6.8], [-4.2, -6.8], [-6.2, -9]], legs: [[[-2, -7], [-2.6, 0]], [[2.2, -7], [3.2, 0]]], near: [[3.4, -27.2], [8.4, -32.2], [12.4, -37.4]], far: [[-3, -27.2], [-5.4, -20.2], [-4.2, -14.6]], hand: [12.4, -37.4] },
  kneel: { head: [6.6, -21.4], body: [[-2, -18.2], [5.2, -18.2], [7.2, -9], [4.2, -6], [-4.2, -6], [-5.2, -9]], legs: [[[-4, -6], [-7.2, -2], [-3, 0]], [[3, -6], [6.4, -2], [9.6, -.8]]], near: [[4.4, -17.2], [9.4, -12.2], [12.2, -8]], far: [[.4, -17.2], [4.4, -12.2], [8.4, -10.2]], hand: [12.2, -8] },
  pole: { head: [0, -33], body: [[-3.6, -28.6], [3.8, -28.6], [5.6, -16.6], [3.6, -14.4], [-3.6, -14.4], [-5.6, -16.6]], legs: [[[-1.6, -14.8], [-3.6, -7.4], [-4.8, 0]], [[1.8, -14.8], [4.4, -7.6], [5.6, 0]]], near: [[3, -27.2], [6.4, -23.4], [6.4, -19.4]], far: [[-2, -27.2], [2, -22.4], [7.4, -17.2]] },
  crouch: { head: [5.4, -20.2], body: [[-2, -17], [5.2, -17], [6.2, -9], [3.2, -7], [-4, -7], [-4.4, -10]], legs: [[[-3, -7], [-7, -3.4], [-4, 0]], [[2, -7], [6.2, -4.2], [5.4, 0]]], near: [[4.2, -15.8], [9.2, -10.2], [13.2, -5.2]], far: [[.4, -15.8], [5.2, -11.2], [9.6, -8.4]], hand: [13.2, -5.2] },
  read: { head: [1.4, -24.2], body: [[-4, -19.6], [4.2, -19.6], [7, -6], [9.4, -1.6], [-9.4, -1.6], [-7, -6]], legs: [], near: [[3.2, -18.4], [7.2, -13.4], [9.4, -11.2]], far: [[-1.4, -18.4], [2.4, -13.2], [7.4, -11.4]], hand: [9.4, -11.2] },
  cup: { head: [.8, -33], body: [[-4, -28.6], [4, -28.6], [6.2, -9], [4.2, -6.8], [-4.2, -6.8], [-6.2, -9]], legs: [[[-2, -7], [-2.6, 0]], [[2.2, -7], [3.2, 0]]], near: [[3.4, -27.2], [7.6, -29.4], [6.2, -34.6]], far: [[-3, -27.2], [-5.4, -20.2], [-4.2, -14.6]], hand: [6.2, -34.6] },
};

/** 두 마디 팔다리: a에서 b로, 마디 길이 l1 · l2. bend +1이면 굽은 마디가 진행 방향의 시계 쪽 */
function ik(a, b, l1, l2, bend) {
  const dx = b[0] - a[0], dy = b[1] - a[1], d = Math.hypot(dx, dy) || 1e-6, ang = Math.atan2(dy, dx);
  if (d >= l1 + l2 - .05) { const L = l1 + l2 - .05; return [[a[0] + Math.cos(ang) * l1, a[1] + Math.sin(ang) * l1], [a[0] + Math.cos(ang) * L, a[1] + Math.sin(ang) * L]]; }
  const A = Math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1)), e = ang + bend * A;
  return [[a[0] + Math.cos(e) * l1, a[1] + Math.sin(e) * l1], b];
}

/** 자세 정의 → 손그림 자세와 같은 꼴 {head, body, legs, near, far, hand}.
 *  hip 골반, lean 몸 기울기(앞 +), tilt 고개(숙임 +), legs [[발x,발y,굽힘]…], near/far [손x,손y,굽힘], robe long|short|skirt
 *  base: 'sit'(책상다리) · 'kneel' · 'crouch'이면 그 몸통을 쓰고 팔만 새로 뻗는다 */
function genPose(d, female) {
  const arm = (sh, t) => { const [el, hd] = ik(sh, t, 6.4, 6.2, t[2] ?? 1); return [sh, el, hd]; };
  if (d.base === "kneel" || d.base === "crouch") {
    const b = FIG[d.base];
    const near = arm(b.near[0], d.near), far = arm(b.far[0], d.far);
    return { head: b.head, body: b.body, legs: b.legs, near, far, hand: near[2], fhand: far[2] };
  }
  const sit = d.base === "sit";
  const [hx, hy] = sit ? [0, -6.2] : d.hip, th = d.lean || 0, TL = sit ? 13.4 : 14;
  const u = [Math.sin(th), -Math.cos(th)], v = [Math.cos(th), Math.sin(th)];
  const TF = (a, s) => [hx + u[0] * s + v[0] * a, hy + u[1] * s + v[1] * a];
  const neck = TF(.5, TL), ht = th + (d.tilt || 0);
  const head = [neck[0] + Math.sin(ht) * 4.6 + .3, neck[1] - Math.cos(ht) * 4.6];
  const near = arm(TF(2.6, TL - 1.4), d.near), far = arm(TF(-1.6, TL - 1.4), d.far);
  let legs = [], body;
  const shL = TF(-3.8, TL), shR = TF(4, TL);
  if (sit) {
    body = [shL, shR, [7 + th * 6, -6], [9.4, -1.6], [-9.4, -1.6], [-7, -6]];
  } else {
    legs = (d.legs || []).map((t, i) => { const hp = i ? TF(1.4, .6) : TF(-1.8, .6), [kn, ft] = ik(hp, t, 7.8, 7.6, t[2] ?? -1); return [hp, kn, ft]; });
    const wR = TF(5.4, 5.2), wL = TF(-5.2, 5.2);
    const robe = female && d.robe !== "short" ? "skirt" : d.robe || "long";
    if (robe === "short") body = [shL, shR, wR, TF(4.8, -.2), TF(-4.6, -.2), wL];
    else {
      const kx = legs.map((l) => l[1][0]), ky = legs.map((l) => l[1][1]);
      const cx = (Math.min(...kx) + Math.max(...kx)) / 2;
      const cy = robe === "skirt" ? Math.max(...legs.map((l) => l[2][1])) - .8 : Math.max(...ky) + 1.6;
      const w0 = robe === "skirt" ? 7.4 : 5.6;
      const L = Math.min(Math.min(...kx) - 2.6, cx - w0), Rr = Math.max(Math.max(...kx) + 2.8, cx + w0 + .2);
      body = [shL, shR, wR, [Rr, cy - 1.8], [Rr - 1.6, cy], [L + 1.6, cy], [L, cy - 1.8], wL];
    }
  }
  return { head, body, legs, near, far, hand: near[2], fhand: far[2] };
}

const SL = [[-2.2, 0], [2.6, 0]];
/** 사람 자세(scene.figures[].pose). 시안 아홉 개는 손그림 그대로 */
const POSE = {
  stand: { hip: [0, -14.6], tilt: .05, legs: SL, near: [5.8, -20.4], far: [5, -21.2] },
  walk: { hip: [.6, -14.2], lean: .06, legs: [[-5.4, 0], [6.2, 0]], near: [7, -18.4], far: [-3.6, -17.2] },
  run: { hip: [1.4, -13.4], lean: .34, robe: "short", legs: [[-8.6, -2.4], [7.6, -5.4]], near: [9.8, -23.2], far: [-6.2, -19.6] },
  chase: { hip: [1.4, -13.4], lean: .34, robe: "short", legs: [[-8.6, -2.4], [7.6, -5.4]], near: [12.4, -24.6], far: [10.8, -22.8] },
  leap: { hip: [.4, -24], lean: .12, robe: "short", legs: [[-6.4, -11.6], [5.4, -13.6]], near: [7.8, -41], far: [-4.6, -39.6] },
  bow: { hip: [-1, -14.6], lean: .62, tilt: .25, legs: [[-2.6, 0], [1.8, 0]], near: [8.4, -17.6], far: [7.6, -18.2] },
  point: { hip: [0, -14.6], legs: SL, near: [15.4, -27.6, -1], far: [-2.8, -17.2] },
  gaze: { hip: [0, -14.6], lean: -.05, tilt: -.5, legs: SL, near: [-3.4, -19.6, -1], far: [-4.2, -20, -1] },
  hold: { hip: [0, -14.6], legs: SL, near: [8.8, -22.2], far: [8, -21.6] },
  hug: { hip: [0, -14.6], legs: SL, near: [6.6, -21.2], far: [5.8, -22.4] },
  offer: { base: "kneel", near: [12.6, -18.6], far: [11.8, -18] },
  shoot: { hip: [-.4, -14.6], robe: "short", legs: [[-5.4, 0], [5.6, 0]], near: [.4, -29.8, -1], far: [15.2, -28.8, -1] },
  throw: { hip: [-.6, -14.4], lean: -.12, robe: "short", legs: [[-5.6, 0], [5.4, 0]], near: [-5.8, -37.4, -1], far: [9.8, -25.4] },
  plow: { hip: [-1, -13.8], lean: .42, robe: "short", legs: [[-7.4, 0], [3.4, 0]], near: [11, -15.2], far: [10.2, -16] },
  sweep: { hip: [-.6, -14.4], lean: .32, robe: "short", legs: [[-4.8, 0], [4.4, 0]], near: [9.8, -15.4], far: [6, -22.4] },
  sprinkle: { hip: [0, -14.6], lean: .1, legs: SL, near: [11.6, -18.2], far: [-2.6, -17.6] },
  cut: { hip: [0, -14.6], lean: .05, robe: "short", legs: [[-4.4, 0], [4.8, 0]], near: [3.6, -40.6, -1], far: [2.2, -39.8, -1] },
  climb: { hip: [2.4, -17.4], lean: .44, robe: "short", legs: [[-3.6, -1.4], [7, -10]], near: [13.2, -36.8, -1], far: [9.8, -33.8, -1] },
  dance: { hip: [0, -14.8], lean: -.1, legs: [[-3.6, 0], [5.6, -4.8]], near: [12, -35, -1], far: [-10, -35.6] },
  guide: { hip: [.6, -14.2], lean: .04, legs: [[-5.4, 0], [6.2, 0]], near: [14, -25.6, -1], far: [-7.2, -17] },
  carryload: { hip: [.6, -14.2], lean: .14, robe: "short", legs: [[-5.2, 0], [6.2, 0]], near: [3.8, -26.4], far: [-1.4, -27] },
  sit: { base: "sit", near: [6.8, -8.8], far: [5.2, -9.4] },
  think: { base: "sit", tilt: .22, near: [4.6, -23.4, -1], far: [6.6, -9.2] },
  write: { base: "sit", lean: .22, tilt: .4, near: [12.8, -6.6], far: [9.4, -6.8] },
  count: { base: "sit", lean: .18, tilt: .35, near: [12.2, -3.8], far: [9.8, -3.6] },
  fish: { base: "sit", near: [9.2, -13], far: [7.8, -12] },
  play: { base: "sit", lean: .1, tilt: .25, near: [11.2, -5.4], far: [16, -4.8] },
  carve: { base: "kneel", near: [7.8, -25.2, -1], far: [12.8, -10.4] },
  grind: { base: "kneel", near: [13.6, -7.8], far: [12, -8.2] },
  wash: { base: "crouch", near: [13.2, -3.4], far: [10.8, -3.8] },
  // 서서 부는 피리 · 치는 북 (play의 갈래)
  flute: { hip: [0, -14.6], tilt: .05, legs: SL, near: [9.2, -30.8, -1], far: [6.4, -31.4, -1] },
  strike: { hip: [-.4, -14.6], lean: .08, legs: [[-3.6, 0], [3.8, 0]], near: [9.6, -31.4, -1], far: [9.8, -19.4] },
  ...Object.fromEntries(Object.entries(FIG).map(([k, f]) => [k, { fig: f }])),
};
POSE.drive = POSE.sit; POSE.ride = { base: "sit", near: [10.4, -12.6], far: [9.4, -13.4] };

/* 누구인가 → 모자 · 수염 · 크기, 동물이면 동물 갈래 */
const RE_CHILD = /아이|어린|소년|동자|학생|아들|조카|손자|아기|자제|새끼|심부름/;
const RE_FEMALE = /아낙|어머니|아내|공주|서시|설씨녀|사도온|공손대랑|여왕|덕만|경강|할미(?!새)|누이|딸|며느리|부인|낭자|여인|과부/;
const RE_KING = /임금|왕(?!수인|안석|충|융|발|상|밀|술|정백|유|자기|량|패)|제$|태종|태조|고조|고종|세종|무왕|문왕|성왕|탕|^순$|^우$|^요$|태갑|^익$|환공|경공|영공|목공|장공|문공|평공|^노공|소공|군$|광무제|명제|원제|혜제|구천|중이|^선왕|^소왕|^위왕|^장왕|^오왕/;
const RE_HELM = /장수|병사|장군|군사|한신|항우|악비|이순신|을지문덕|강감찬|최영|이광|염파|마원|경엄|풍이|반초|조충국|악의|이사부|귀산|조괄|양유기|궁수|오자서|손빈/;
const RE_CAP = /관리|신하|대부|사신|재상|정승|관원|아전|벼슬/;
const RE_STRAW = /농부|사공|어부|뱃사람|나무꾼|사냥꾼|일꾼|목동|정원사|곽탁타|마부|수레꾼|나그네|사금꾼|시골|빨래|장사꾼|상인|백성|사람들|심는|뽑는|도롱이/;
const RE_MONK = /원광|월명|스님|중$|승려|대사/;
const RE_PLAIN = /장인|목수|대장장이|도공|석공|옥공|옥장이|갖바치|요리사|포정|윤편|수레장이|장석|의원|악사|화가|점쟁이|사내|젊은이|벗|친구|이웃|손님|불량배|구경꾼|사람|검객|조각가|염색공|약사|기술자|복두장이|광대|떠드는|여러|주인|식구|형|아우|이들$/;
const RE_ELDER = /노인|늙은|어른|스승|선생|옹$|할아버지|노공|공자|맹자|노자|장자|순자|묵자|주희|정이|정호|왕수인|소옹|장재|증자|백두옹|우공|저공|꼽추/;
const ANIMAL = [
  [/학|두루미/, "crane"], [/수탉|닭/, "rooster"], [/봉황/, "phoenix"], [/붕새|큰 새/, "roc"], [/기러기|고니/, "goose"],
  [/솔개|새매|물수리|매$/, "hawk"], [/오리/, "duck"], [/올빼미|부엉이/, "owl"], [/까투리|꿩/, "pheasant"],
  [/새|까치|제비|참새|꾀꼬리|비둘기|뻐꾸기|할미새|바닷새/, "bird"],
  [/천리마|망아지|말$|말들|큰 말|어린 말/, "horse"], [/^소$|송아지|황소|끌려가는 소/, "ox"], [/개$|강아지|큰 개/, "dog"],
  [/기린/, "qilin"], [/사슴|노루/, "deer"], [/양$|숫양|염소/, "sheep"], [/여우/, "fox"], [/토끼/, "rabbit"],
  [/원숭이/, "monkey"], [/날다람쥐|다람쥐/, "squirrel"], [/범$|호랑이/, "tiger"],
  [/물고기|잉어|붕어/, "fish"], [/자라|거북/, "turtle"], [/개구리|두꺼비/, "frog"], [/^용$|용$/, "dragon"],
  [/개미/, "ant"], [/사마귀/, "mantis"], [/매미/, "cicada"], [/잠자리/, "dragonfly"], [/나비/, "butterfly"],
  [/자벌레|지렁이|노래기|벌레/, "worm"], [/나나니|벌$/, "bee"], [/^기$/, "worm"],
];
export function whoOf(name) {
  const n = String(name || "").replace(/\(.*\)/, "").trim();
  for (const [re, k] of ANIMAL) if (re.test(n)) return { animal: k, name: n };
  const child = RE_CHILD.test(n) && !/어린 여우/.test(n), female = RE_FEMALE.test(n);
  const hat = child ? "child" : female ? "bun" : RE_MONK.test(n) ? "monk" : RE_KING.test(n) ? "crown" : RE_HELM.test(n) ? "helm" :
    RE_CAP.test(n) ? "cap" : RE_STRAW.test(n) ? "satgat" : RE_PLAIN.test(n) ? "top" : "gat";
  const named = !RE_PLAIN.test(n) && !RE_STRAW.test(n) && !RE_CAP.test(n) && !/선비|군자|제자|병사|궁수|배우는|책 읽는|시인|학자|생각하는|묻는|가리는|행하는|지혜로운|어진|용감한|신중한|내달리는|고집쟁이|앞서|먼저|봇짐|관복|마음 모은|고니 보는|이긴|우물 안|고른|천문가|산을 낀/.test(n);
  const beard = !child && !female && (RE_ELDER.test(n) || (named && hat !== "helm") || /군자|스승|임금/.test(n));
  return { name: n, child, female, hat, beard, scale: child ? 1.02 : 1.42 };
}

/** 모자: kind, 머리 가운데 (hx,hy), 머리 반지름 hr, m = 보는 쪽(1 오른쪽) */
function hat(p, kind, hx, hy, hr, m, sw) {
  const ink = p.pal.ink;
  const cap = `<path d="M${P2(hx - hr, hy - hr * .05)}A${f1(hr)} ${f1(hr)} 0 0 1 ${P2(hx + hr, hy - hr * .05)}Q${P2(hx, hy - hr * .5)} ${P2(hx - hr, hy - hr * .05)}Z" ${p.fa(null, .9)}/>`;
  if (kind === "gat") return cap + `<ellipse cx="${f1(hx)}" cy="${f1(hy - hr * .62)}" rx="${f1(hr * 2.2)}" ry="${f1(hr * .32)}" ${p.fa(null, .78)}/><rect x="${f1(hx - hr * .62)}" y="${f1(hy - hr * 1.8)}" width="${f1(hr * 1.24)}" height="${f1(hr * 1.2)}" rx="${f1(hr * .3)}" ${p.fa(null, .82)}/>`;
  if (kind === "satgat") return `<path d="M${P2(hx - hr * 2, hy - hr * .15)}Q${P2(hx, hy - hr * .55)} ${P2(hx + hr * 2, hy - hr * .15)}L${P2(hx, hy - hr * 2.1)}Z" fill="${p.pal.paper}" stroke="${ink}" stroke-width="${f1(sw)}" stroke-linejoin="round"/><path d="M${P2(hx - hr * .9, hy - hr * .9)}L${P2(hx, hy - hr * 2)}M${P2(hx + hr * .9, hy - hr * .9)}L${P2(hx, hy - hr * 2)}" stroke="${ink}" stroke-opacity=".45" stroke-width=".5"/>`;
  if (kind === "child") return cap + `<path d="M${P2(hx - m * hr * .9, hy - hr * .2)}q${f1(-m * hr * .9)} ${f1(hr * .6)} ${f1(-m * hr * 1.1)} ${f1(hr * 2)}" fill="none" stroke="${ink}" stroke-width="${f1(1.1)}" stroke-linecap="round"/>`;
  if (kind === "bun") return cap + p.dot(hx - m * hr * .78, hy + hr * .02, hr * .5, null, .9) + p.line([[hx - m * hr * 1.5, hy - hr * .25], [hx - m * hr * .1, hy + hr * .25]], .55, null, .8);
  if (kind === "crown") return cap + `<rect x="${f1(hx - hr * .78)}" y="${f1(hy - hr * 1.75)}" width="${f1(hr * 1.56)}" height="${f1(hr * 1.1)}" rx="${f1(hr * .2)}" ${p.fa(null, .85)}/>` + p.line([[hx - hr * 1.7, hy - hr * 1.86], [hx + hr * 1.7, hy - hr * 1.86]], 1.1, null, .9) + [-1.5, -.9, .9, 1.5].map((k) => p.line([[hx + k * hr, hy - hr * 1.8], [hx + k * hr, hy - hr * .9]], .35, null, .7) + p.dot(hx + k * hr, hy - hr * .85, .45, null, .8)).join("");
  if (kind === "helm") return `<path d="M${P2(hx - hr * 1.08, hy + hr * .25)}A${f1(hr * 1.1)} ${f1(hr * 1.15)} 0 0 1 ${P2(hx + hr * 1.08, hy + hr * .05)}L${P2(hx + hr * .7, hy - hr * .05)}Q${P2(hx, hy - hr * .35)} ${P2(hx - hr * .5, hy + hr * .1)}Z" ${p.fa(null, .9)}/>` + p.line([[hx - m * hr * .9, hy + hr * .1], [hx - m * hr * 1.25, hy + hr * 1.05]], 1.4, null, .85) + p.bl([[hx, hy - hr * 1.05], [hx - m * hr * .2, hy - hr * 2], [hx - m * hr * 1.1, hy - hr * 2.5]], .9, null, .85, TAPER);
  if (kind === "cap") return cap + `<rect x="${f1(hx - hr * .72)}" y="${f1(hy - hr * 1.5)}" width="${f1(hr * 1.44)}" height="${f1(hr * .95)}" rx="${f1(hr * .45)}" ${p.fa(null, .88)}/>` + [-1, 1].map((k) => `<ellipse cx="${f1(hx + k * hr * 1.25)}" cy="${f1(hy - hr * 1.05)}" rx="${f1(hr * .62)}" ry="${f1(hr * .22)}" ${p.fa(null, .72)}/>`).join("");
  if (kind === "monk") return p.bl([[hx - hr * .8, hy - hr * .65], [hx, hy - hr * .95], [hx + hr * .8, hy - hr * .65]], .35, null, .35);
  return cap + p.dot(hx + m * hr * .15, hy - hr * 1.08, hr * .42, null, 1);
}

/** 사람 그리기. pose = 자세 이름 또는 {fig}, (x,y) 발, s 크기, flip이면 왼쪽을 본다.
 *  opt: who(whoOf 결과), back(T,m) 몸 뒤에 그릴 것, front(T,m) 몸 앞에 그릴 것 */
function figure(p, pose, x, y, s, flip, opt) {
  opt = opt || {};
  const w = opt.who || { hat: "top" }, def = typeof pose === "string" ? POSE[pose] || POSE.stand : pose;
  const f = def.fig || genPose(def, w.female);
  const m = flip ? -1 : 1, T = ([px, py]) => [x + m * px * s, y + py * s];
  let o = "";
  if (f.far) o += p.bl(f.far.map(T), 1.05 * s, null, .85);
  (f.legs || []).forEach((l) => { o += p.bl(l.map(T), 1.25 * s, null, .9); const e = l[l.length - 1]; o += p.bl([T(e), T([e[0] + 2.4, e[1] + .3])], 1.1 * s, null, .9, [[0, 1], [1, .6]]); });
  o += p.shape(f.body.map(T), "paper", 1, .85 * s);
  if (opt.back) o += opt.back(T, m, f);
  o += p.bl(f.near.map(T), 1.15 * s, null, .92);
  const [hx, hy] = T(f.head), hr = 4.2 * s;
  o += p.disc(hx, hy, hr, "paper", 1, .8 * s) + hat(p, w.hat || "top", hx, hy, hr, m, .8 * s);
  if (w.beard) o += [-1, 0, 1].map((k) => p.bl([[hx + m * hr * .5 + k * .9, hy + hr * .55], [hx + m * hr * .65 + k * 1.1, hy + hr * 1.6], [hx + m * hr * .4 + k * 1.3, hy + hr * 2.3]], .45 * s, null, .7, TAPER)).join("");
  if (opt.front) o += opt.front(T, m, f);
  return { svg: o, T, f, m, hand: T(f.hand || f.near[2]), fhand: T(f.fhand || f.far[2]), head: [hx, hy], hr };
}


/* ───────────── 동물 ───────────── */
/** 새. kind: bird · crane · rooster · phoenix · roc · goose · hawk · duck · owl · pheasant, pose: stand · perch · fly · crow · swim */
function bird(p, kind, pose, x, y, s, flip) {
  const m = flip ? -1 : 1, T = ([px, py]) => [x + m * px * s, y + py * s], TT = (a) => a.map(T);
  let o = "";
  const fly = pose === "fly" || kind === "roc" || (kind === "goose" && pose !== "stand" && pose !== "swim") || (kind === "hawk" && pose !== "perch");
  if (fly) {
    const k = kind === "roc" ? 2.3 : ["goose", "hawk", "crane", "phoenix", "pheasant"].includes(kind) ? 1.35 : 1, K = (a) => a.map(([px, py]) => [px * k, py * k]);
    const neck = kind === "crane" || kind === "goose" ? 4.4 : 0;
    o += p.area(TT(K([[1.6, -7.8], [3.6, -11.6], [6.6, -16.6], [4.6, -12.6], [3.4, -9.4]])), null, .42);
    if (kind === "phoenix" || kind === "pheasant") for (let j = 0; j < (kind === "phoenix" ? 3 : 1); j++) o += p.bl(TT(K([[-5, -6.2], [-11, -5 + j * 2.4], [-18, -7 + j * 3.6], [-24, -3 + j * 3]])), .9 * s * k, null, .7, TAPER);
    o += p.bl(TT(K([[-4.6, -6.2], [-7.6, -5.8], [-9.6, -4.6]])), 1.2 * s * k, null, .8, TAPER) + p.bl(TT(K([[-4.6, -6.6], [-8, -7], [-10, -6.8]])), 1 * s * k, null, .7, TAPER);
    o += p.shape(TT(K([[-5.6, -6.4], [-1.6, -8.6], [3.6, -8.4], [5.6, -7], [3, -5], [-2.6, -4.8]])), "paper", 1, .55 * s * k);
    if (kind === "crane") o += p.line(TT(K([[-4, -5.4], [-11, -4.2], [-13, -4]])), .45 * s * k, null, .85);
    const hd = [5.4 + neck, -7.4 - neck * .1];
    if (neck) o += p.bl(TT(K([[4.4, -7.4], hd])), .8 * s * k, null, .9, EVEN);
    o += p.dot(...T([hd[0] * k, hd[1] * k]), 1.5 * s * Math.sqrt(k), null, .9) + p.area(TT(K([[hd[0] + 1, hd[1] - .6], [hd[0] + (neck ? 5 : 3.2), hd[1] + .2], [hd[0] + 1, hd[1] + .6]])), null, .9);
    o += p.area(TT(K([[1.8, -7.6], [-.6, -11], [-4.6, -15.8], [-9.6, -19.4], [-8.2, -16.2], [-11, -16.6], [-7.6, -13.2], [-9, -12.4], [-4.6, -9.4], [-1.4, -7.2]])), null, .85);
    return { svg: o, T, top: T([0, -18 * k]) };
  }
  if (kind === "crane") {
    const up = pose === "crow";
    o += p.line(TT([[0, -17], [.4, 0]]), .65 * s, null, .9) + p.line(TT([[-1.6, -17], [-3, 0]]), .65 * s, null, .9);
    o += p.bl(TT([[-5.4, -21.4], [-9.4, -19.4], [-11, -16.4]]), 2.4 * s, null, .9, DAB);
    o += p.shape(TT([[-6.6, -21], [-1, -25], [5.4, -23.6], [7.2, -21.4], [2.6, -18], [-4.6, -17.6]]), "paper", 1, .7 * s);
    const hd = up ? [3.6, -40.6] : [7.4, -36.4];
    o += p.bl(TT([[5.4, -23.4], [7.8, -29], up ? [4.6, -36] : [6.4, -34], hd]), 1.15 * s, null, .9, EVEN) + p.dot(...T(hd), 1.6 * s, null, .9);
    o += up ? p.line(TT([hd, [hd[0] + 3, hd[1] - 5.4]]), .55 * s, null, .9) + p.line(TT([hd, [hd[0] + 4.4, hd[1] - 3.6]]), .5 * s, null, .9) + [1, 2, 3].map((j) => p.line(TT(p.arc(hd[0] + 3, hd[1] - 5, 2.6 + j * 2.4, -1.4, -.4, 4)), .4 * s, null, .45)).join("")
      : p.bl(TT([hd, [hd[0] + 6.6, hd[1] + 1.2]]), .75 * s, null, .9, [[0, 1], [1, .3]]);
    return { svg: o, T, top: T([4, -40]) };
  }
  if (kind === "owl") {
    o += p.shape(TT([[-3.6, -2.4], [-4.2, -8], [-2.6, -13], [2.6, -13], [4.2, -8], [3.6, -2.4]]), "paper", 1, .7 * s);
    o += p.disc(...T([0, -14.4]), 3.8 * s, "paper", 1, .7 * s) + p.bl(TT([[-3.2, -16.8], [-3.8, -19.4]]), .9 * s, null, .9, TAPER) + p.bl(TT([[3.2, -16.8], [3.8, -19.4]]), .9 * s, null, .9, TAPER);
    o += p.ring(...T([-1.5, -14.8]), 1.2 * s, .5 * s) + p.ring(...T([1.5, -14.8]), 1.2 * s, .5 * s) + p.dot(...T([-1.5, -14.8]), .45 * s) + p.dot(...T([1.5, -14.8]), .45 * s);
    o += p.bl(TT([[-3.4, -9.6], [-2.4, -5], [-.6, -3]]), 1.4 * s, null, .7, DAB);
    return { svg: o, T, top: T([0, -19]) };
  }
  if (kind === "duck" || pose === "swim") {
    o += p.shape(TT([[-6.4, -3.4], [-3, -5.2], [3, -5], [5.2, -3.6], [3.6, -.8], [-4.6, -.8]]), "paper", 1, .7 * s);
    o += p.bl(TT([[3.6, -4.4], [5, -7.4], [5.4, -9.2]]), 1.3 * s, null, .9) + p.dot(...T([5.6, -9.4]), 1.9 * s, null, .9) + p.bl(TT([[7, -9.2], [9.6, -8.6]]), .9 * s, null, .9, [[0, 1], [1, .7]]);
    o += p.bl(TT([[-3.6, -3.4], [0, -4.2], [2.6, -3.6]]), 1.5 * s, null, .75, DAB);
    o += p.line(TT([[-9, .4], [-4, .2]]), .4 * s, null, .5) + p.line(TT([[4.6, .4], [9, .6]]), .4 * s, null, .5);
    return { svg: o, T, top: T([4, -11]) };
  }
  const tall = kind === "rooster" || kind === "phoenix" || kind === "pheasant";
  if (tall) {
    const up = pose === "crow";
    o += p.line(TT([[-.4, -5.6], [-.8, 0]]), .7 * s, null, .9) + p.line(TT([[1.4, -5.6], [2, 0]]), .7 * s, null, .9);
    if (kind === "pheasant") o += p.bl(TT([[-5, -9], [-12, -8], [-19, -6.4]]), 1.3 * s, null, .85, TAPER);
    else if (kind === "phoenix") for (let j = 0; j < 4; j++) o += p.bl(TT([[-4.6, -10.6], [-11 - j, -15 + j * 2.6], [-17 - j * 2, -8 + j * 2.4], [-22 - j * 2, -12 + j * 4.4]]), (1.2 - j * .15) * s, null, .75, TAPER);
    else for (let j = 0; j < 3; j++) o += p.bl(TT([[-4.6, -11.4], [-8.4 - j, -18.4 + j * 1.6], [-11.6 - j * 1.4, -13 + j * 2], [-10.6 - j * 1.4, -7 + j * 1.2]]), (1.5 - j * .3) * s, null, .85, TAPER);
    o += p.shape(TT([[-5.4, -10.6], [-1.6, -13.6], [4, -13], [5.4, -9.4], [2.4, -5.4], [-3.6, -6.2]]), "paper", 1, .75 * s);
    o += p.bl(TT([[-2.4, -10], [1, -10.8], [3.2, -8.4]]), 1.5 * s, null, .7, DAB);
    const hd = up ? [5.2, -20.4] : [5.8, -18.2];
    o += p.bl(TT([[3, -12.6], [4.6, -15.6], hd]), 2.4 * s, null, .65, EVEN) + p.disc(...T(hd), 2.1 * s, "paper", 1, .6 * s);
    o += p.bl(TT([[hd[0] - 1.6, hd[1] - 1.8], [hd[0] - .2, hd[1] - 3.4], [hd[0] + 1.4, hd[1] - 2]]), .9 * s, null, .85, EVEN);
    o += p.dot(...T([hd[0] + .7, hd[1] - .3]), .45 * s);
    o += up ? p.line(TT([[hd[0] + 1.8, hd[1] - .4], [hd[0] + 4.4, hd[1] - 2.2]]), .5 * s) + p.line(TT([[hd[0] + 1.8, hd[1] + .2], [hd[0] + 4.4, hd[1] + .6]]), .5 * s) + [1, 2, 3].map((j) => p.line(TT(p.arc(hd[0] + 4, hd[1] - .8, 2 + j * 2.4, -1, .5, 4)), .4 * s, null, .45)).join("")
      : p.bl(TT([[hd[0] + 1.6, hd[1]], [hd[0] + 3.6, hd[1] + .4]]), .7 * s, null, .9, [[0, 1], [1, .4]]);
    if (kind === "phoenix") o += [0, 1, 2].map((j) => p.bl(TT([[hd[0] - 1, hd[1] - 2], [hd[0] - 2 - j * 1.6, hd[1] - 5 - j * .6]]), .5 * s, null, .8, TAPER)).join("");
    return { svg: o, T, top: T([4, -22]) };
  }
  // 작은 새(앉음 · 섬)
  o += p.line(TT([[-.4, -2.4], [-.6, 0]]), .45 * s) + p.line(TT([[1.2, -2.4], [1.6, 0]]), .45 * s);
  o += p.bl(TT([[-4, -4.4], [-8.6, -2]]), 1.2 * s, null, .85, TAPER) + p.bl(TT([[-4, -4.8], [-8.8, -3.6]]), 1, null, .7, TAPER);
  o += p.shape(TT([[-4.6, -4.4], [-1.4, -7.2], [3.4, -7.6], [4.6, -5], [2.4, -2.6], [-2.6, -2.6]]), "paper", 1, .6 * s);
  o += p.bl(TT([[2.6, -7], [-1, -6.4], [-4.6, -4.6]]), 1.9 * s, null, .82, DAB);
  o += p.dot(...T([4.4, -8.4]), 2.2 * s, null, .88) + p.dot(...T([5, -8.8]), .4 * s, "paper");
  o += p.area(TT([[6.2, -9], [8.8, -8.4], [6.2, -7.8]]), null, .9);
  return { svg: o, T, top: T([3, -11]) };
}

/** 네발짐승. kind: horse · ox · dog · deer · qilin · sheep · fox · tiger · rabbit · monkey · squirrel, pose: stand · walk · run · graze · leap · sit */
const QUAD = {
  horse: { L: 20, H: 8.4, G: 12.6, neck: 1, head: [5.6, 2.4], tail: "flow" },
  ox: { L: 21, H: 10.2, G: 8.4, neck: .45, head: [4.4, 3.4], tail: "thin", horn: "ox" },
  tiger: { L: 19, H: 7.6, G: 8, neck: .4, head: [3.6, 3.2], tail: "long", stripe: 1 },
  dog: { L: 12.6, H: 5.8, G: 6.6, neck: .55, head: [3.6, 2.4], tail: "curl", ear: 1 },
  fox: { L: 12.6, H: 5, G: 5.4, neck: .5, head: [4.2, 2.2], tail: "bush", ear: 1 },
  deer: { L: 15, H: 6.4, G: 11, neck: .9, head: [3.8, 2], tail: "stub", horn: "antler" },
  qilin: { L: 16, H: 7, G: 11, neck: .9, head: [4, 2.2], tail: "flow", horn: "one" },
  sheep: { L: 13, H: 7.4, G: 5.8, neck: .45, head: [3.2, 2.6], tail: "stub", horn: "curl", wool: 1 },
};
function quad(p, kind, pose, x, y, s, flip) {
  const m = flip ? -1 : 1, T = ([px, py]) => [x + m * px * s, y + py * s], TT = (a) => a.map(T);
  let o = "";
  if (kind === "rabbit" || kind === "monkey" || kind === "squirrel") return small(p, kind, pose, x, y, s, flip);
  const q = QUAD[kind] || QUAD.dog, { L, H, G } = q, lift = pose === "leap" ? 7 : 0, by = -G - lift;
  const tilt = pose === "leap" ? -.2 : pose === "run" ? -.04 : 0, R2 = ([px, py]) => [px, py + px * tilt];
  const bodyPts = [[-L / 2, by - H * .2], [-L / 2 - 1, by - H * .62], [-L * .3, by - H], [L * .22, by - H * 1.02], [L / 2 + 1, by - H * .74], [L / 2, by - H * .2], [L * .16, by + .4], [-L * .26, by + .6]].map(R2);
  // 다리: 뒷다리 쌍, 앞다리 쌍(먼 다리 먼저)
  const legX = [-L * .36, -L * .24, L * .26, L * .38], ph = { stand: [0, 0, 0, 0], graze: [0, 0, 0, 0], walk: [-2.6, 2, -2, 2.6], run: [-6.4, -4.4, 6, 8.4], leap: [-7, -5.6, 6.4, 8] }[pose] || [0, 0, 0, 0];
  const legs = legX.map((lx, i) => { const top = R2([lx, by - .4]), ft = pose === "leap" ? [lx + ph[i], by + G * .62] : [lx + ph[i], 0], kn = [(top[0] + ft[0]) / 2 + (i < 2 ? -1.2 : 1.2) * (pose === "run" || pose === "leap" ? 1.6 : .4), (top[1] + ft[1]) / 2]; return [top, kn, ft]; });
  [1, 3].forEach((i) => { o += p.bl(TT(legs[i]), .95 * s, null, .65); });
  // 꼬리
  const rump = R2([-L / 2 - .6, by - H * .6]);
  if (q.tail === "flow") o += p.bl(TT([rump, [rump[0] - 4, rump[1] + 2], [rump[0] - 5.4, rump[1] + 8], [rump[0] - 4.4, rump[1] + 12]]), 1.8 * s, null, .8, TAPER);
  else if (q.tail === "bush") o += p.area(TT([rump, [rump[0] - 6, rump[1] - 1], [rump[0] - 11, rump[1] + 3], [rump[0] - 7, rump[1] + 4.4], [rump[0] - 2, rump[1] + 2]]), null, .7);
  else if (q.tail === "curl") o += p.bl(TT([rump, [rump[0] - 2.6, rump[1] - 3.4], [rump[0] - .6, rump[1] - 6]]), .9 * s, null, .85, TAPER);
  else if (q.tail === "long") o += p.bl(TT([rump, [rump[0] - 5, rump[1] + 4], [rump[0] - 8, rump[1] + 2], [rump[0] - 10.6, rump[1] - 2]]), 1.1 * s, null, .85, LINE);
  else if (q.tail === "thin") o += p.line(TT([rump, [rump[0] - 2, rump[1] + 5], [rump[0] - 2.4, rump[1] + 9]]), .5 * s) + p.bl(TT([[rump[0] - 2.4, rump[1] + 8.4], [rump[0] - 2.6, rump[1] + 11]]), 1.1 * s, null, .85, TAPER);
  else o += p.tick(...T(rump), m > 0 ? rad(200) : rad(-20), 2.4 * s, 1.1 * s);
  // 몸
  o += p.shape(TT(bodyPts), "paper", 1, .8 * s);
  if (q.wool) for (let j = 0; j < 7; j++) { const a = rad(200 + j * 22); o += p.line(TT(p.arc(-L * .02 + Math.cos(a) * L * .38, by - H * .5 + Math.sin(a) * H * .42, 1.6, a - 1.2, a + 1.2, 4)), .45 * s, null, .5); }
  if (q.stripe) for (let j = 0; j < 5; j++) { const sx = -L * .3 + j * L * .14; o += p.bl(TT([R2([sx, by - H * .95]), R2([sx + 1.2, by - H * .5]), R2([sx + .4, by - H * .2])]), .8 * s, null, .7, TAPER); }
  [0, 2].forEach((i) => { o += p.bl(TT(legs[i]), 1.1 * s, null, .9); o += p.bl(TT([legs[i][2], [legs[i][2][0] + 1.4, legs[i][2][1]]]), 1.2 * s, null, .9, [[0, 1], [1, .7]]); });
  // 목 · 머리
  const graze = pose === "graze";
  const hd = graze ? [L / 2 + 4.6, by + G * .55] : R2([L / 2 + 2 + q.neck * 3, by - H - q.neck * 9]);
  const hl = q.head[0], hh = q.head[1], ha = graze ? rad(70) : rad(kind === "horse" || kind === "qilin" ? 38 : 18);
  const nT = R2([L / 2 - 2.6, by - H * 1.02]), nB = R2([L / 2 + 1.2, by - H * .38]), hT = [hd[0] - hh * .45, hd[1] - hh * .55], hB = [hd[0] + hh * .3, hd[1] + hh * .5];
  o += p.area([nT, [(nT[0] + hT[0]) / 2, (nT[1] + hT[1]) / 2 - .4], hT, hB, [(nB[0] + hB[0]) / 2 + .4, (nB[1] + hB[1]) / 2], nB].map(T), "paper", 1) + p.bl(TT([nT, [(nT[0] + hT[0]) / 2, (nT[1] + hT[1]) / 2 - .4], hT]), .8 * s, null, .9, EVEN) + p.bl(TT([nB, [(nB[0] + hB[0]) / 2 + .4, (nB[1] + hB[1]) / 2], hB]), .7 * s, null, .85, EVEN);
  const tip = [hd[0] + Math.cos(ha) * hl, hd[1] + Math.sin(ha) * hl];
  o += p.shape(TT([[hd[0] - hh * .5, hd[1] - hh * .5], [hd[0] + hh * .4, hd[1] - hh * .6], [tip[0] + .4, tip[1] - hh * .25], [tip[0], tip[1] + hh * .3], [hd[0] + hh * .2, hd[1] + hh * .55]]), "paper", 1, .7 * s);
  o += p.dot(...T([hd[0] + hh * .2, hd[1] - hh * .15]), .45 * s);
  if (kind === "horse" || kind === "qilin") o += [0, 1, 2, 3].map((j) => p.tick(...T([nT[0] + (hT[0] - nT[0]) * j / 4, nT[1] + (hT[1] - nT[1]) * j / 4]), m > 0 ? rad(205) : rad(-25), 2.8 * s, .8 * s, null, .75)).join("");
  if (q.ear || kind === "horse" || kind === "deer" || kind === "qilin") o += p.bl(TT([[hd[0] - hh * .2, hd[1] - hh * .5], [hd[0] - hh * .5, hd[1] - hh * 1.3]]), .9 * s, null, .9, TAPER);
  if (q.horn === "ox") o += [[-1, .6], [1, 1]].map(([k, w]) => p.bl(TT([[hd[0] - .4 + k * .4, hd[1] - hh * .5], [hd[0] - 2.4 + k * .4, hd[1] - hh * 1.2], [hd[0] - 1 + k, hd[1] - hh * 1.8]]), .8 * s * w, null, .9, TAPER)).join("");
  if (q.horn === "curl") o += p.bl(TT(p.arc(hd[0] - .4, hd[1] - .4, 2.2, rad(-160), rad(120), 7)), .9 * s, null, .85, TAPER);
  if (q.horn === "one") o += p.bl(TT([[hd[0], hd[1] - hh * .5], [hd[0] + 1, hd[1] - hh * 2.2]]), .8 * s, null, .9, TAPER);
  if (q.horn === "antler") { const b0 = [hd[0] - .4, hd[1] - hh * .5]; o += p.bl(TT([b0, [b0[0] - 1.6, b0[1] - 4], [b0[0] - 1, b0[1] - 8]]), .6 * s, null, .9, TAPER) + p.bl(TT([[b0[0] - 1.4, b0[1] - 3.4], [b0[0] + 1.6, b0[1] - 5.6]]), .5 * s, null, .9, TAPER) + p.bl(TT([[b0[0] - 1.2, b0[1] - 6], [b0[0] - 4, b0[1] - 7.6]]), .45 * s, null, .9, TAPER); }
  return { svg: o, T, top: T([hd[0], hd[1] - 6]) };
}
function small(p, kind, pose, x, y, s, flip) {
  const m = flip ? -1 : 1, T = ([px, py]) => [x + m * px * s, y + py * s], TT = (a) => a.map(T);
  let o = "";
  if (kind === "rabbit") {
    const lp = pose === "leap" || pose === "run";
    if (lp) {
      o += p.bl(TT([[-4, -5], [-8.6, -2.4], [-10.4, -.6]]), 1 * s, null, .85, TAPER);
      o += p.shape(TT([[-5.6, -5.6], [-1, -8.6], [4.6, -8], [5.4, -5.6], [1, -3.4], [-4.4, -3.4]]), "paper", 1, .7 * s);
      o += p.bl(TT([[3.4, -5], [7.4, -3.4], [9.4, -2.2]]), .8 * s, null, .85, TAPER);
      o += p.disc(...T([6, -9.4]), 2.4 * s, "paper", 1, .65 * s) + p.bl(TT([[5, -11.2], [2, -15.6]]), 1 * s, null, .85, TAPER) + p.bl(TT([[6, -11.4], [4.6, -16.2]]), 1 * s, null, .85, TAPER);
      return { svg: o, T, top: T([4, -16]) };
    }
    o += p.dot(...T([-5, -3.4]), 1.3 * s, null, .7);
    o += p.shape(TT([[-5, -1], [-5.4, -5.4], [-1.4, -8.6], [3, -7.4], [3.8, -3], [1.4, -.4]]), "paper", 1, .7 * s);
    o += p.disc(...T([3.8, -9]), 2.6 * s, "paper", 1, .65 * s) + p.dot(...T([4.8, -9.4]), .4 * s);
    o += p.bl(TT([[2.8, -10.8], [-.4, -16.2]]), 1.1 * s, null, .85, TAPER) + p.bl(TT([[3.8, -11.2], [2.4, -16.8]]), 1.1 * s, null, .85, TAPER);
    return { svg: o, T, top: T([2, -17]) };
  }
  if (kind === "monkey") {
    o += p.bl(TT([[-3, -2], [-8, -1], [-9.4, -5], [-7.4, -7.4]]), .8 * s, null, .85, LINE);
    o += p.shape(TT([[-3.4, -.6], [-4, -6.4], [-1.4, -10.6], [2.4, -10], [3.4, -5], [2, -.6]]), "paper", 1, .7 * s);
    o += p.bl(TT([[1.4, -9.6], [5.6, -10.4], [8.4, -13.6]]), .95 * s, null, .9) + p.bl(TT([[-.4, -6], [3, -3.4], [5, -1.4]]), .95 * s, null, .9);
    o += p.disc(...T([1, -13.4]), 3 * s, null, .85) + p.disc(...T([1.8, -13]), 1.8 * s, "paper", 1);
    o += p.dot(...T([1.3, -13.6]), .35 * s) + p.dot(...T([2.5, -13.6]), .35 * s);
    return { svg: o, T, top: T([1, -17]) };
  }
  // 날다람쥐: 막을 펴고 미끄러진다
  o += p.bl(TT([[-4, -10], [-9, -8.4], [-12.4, -10.6]]), 1.8 * s, null, .8, TAPER);
  o += p.shape(TT([[-4.6, -13.4], [3.6, -14.6], [5, -10.2], [3.4, -6.4], [-3.4, -6.6], [-5.4, -10]]), "paper", 1, .7 * s);
  o += p.disc(...T([5.8, -11]), 2.2 * s, "paper", 1, .6 * s) + p.dot(...T([6.6, -11.4]), .4 * s) + p.bl(TT([[5, -12.8], [4.4, -14.6]]), .7 * s, null, .9, TAPER);
  return { svg: o, T, top: T([0, -15]) };
}
/** 물고기 · 거북 · 개구리 · 벌레 */
function critter(p, kind, pose, x, y, s, flip) {
  const m = flip ? -1 : 1, T = ([px, py]) => [x + m * px * s, y + py * s], TT = (a) => a.map(T);
  let o = "";
  if (kind === "fish") {
    o += p.area(TT([[-6, -3], [-9.6, -5.6], [-8.6, -3], [-9.6, -.4]]), null, .8);
    o += p.shape(TT([[-6.4, -3], [-2, -5.6], [3.6, -5.2], [6.4, -3.2], [3.4, -1], [-2, -.8]]), "paper", 1, .65 * s);
    o += p.bl(TT([[-1.6, -5.4], [.6, -7], [2.2, -5.4]]), .8 * s, null, .8, EVEN) + p.dot(...T([4, -3.6]), .5 * s) + p.line(TT(p.arc(0, -3, 2.6, rad(-60), rad(60), 4)), .35 * s, null, .5);
    return { svg: o, T, top: T([0, -7]) };
  }
  if (kind === "turtle") {
    o += [[-4, 0], [-1.4, 0], [2.4, 0], [4.6, 0]].map(([lx], i) => p.bl(TT([[lx, -2], [lx + (i < 2 ? -1.4 : 1.4), -.2]]), 1.1 * s, null, .85, EVEN)).join("");
    o += p.bl(TT([[4.6, -2.4], [7.4, -3.2], [8.6, -2.6]]), 1.5 * s, null, .85, EVEN) + p.tick(...T([-5.4, -2]), m > 0 ? PI : 0, 2 * s, .6 * s);
    o += p.shape(TT([[-6.4, -1.4], [-4.6, -5.4], [0, -7], [4.6, -5.4], [6.4, -1.4]]), "paper", 1, .8 * s);
    o += p.line(TT([[-3.4, -2], [-2, -5.2]]), .4 * s, null, .6) + p.line(TT([[0, -1.6], [0, -6.6]]), .4 * s, null, .6) + p.line(TT([[3.4, -2], [2, -5.2]]), .4 * s, null, .6) + p.line(TT([[-5.4, -3.4], [5.4, -3.4]]), .4 * s, null, .5);
    return { svg: o, T, top: T([0, -8]) };
  }
  if (kind === "frog") {
    const lp = pose === "leap";
    if (lp) o += p.bl(TT([[-3, -4], [-8, -1], [-10, .2]]), 1 * s, null, .85) + p.bl(TT([[-3, -3.4], [-7, -.2]]), .8 * s, null, .7);
    else o += p.bl(TT([[-3.4, -2], [-6, -.6], [-3, 0]]), 1 * s, null, .85) + p.bl(TT([[2.4, -2], [4.4, 0]]), .9 * s, null, .85);
    o += p.shape(TT([[-4.6, -1.6], [-4, -4.6], [0, -6], [4, -4.4], [4.8, -1.6], [0, -.6]]), "paper", 1, .7 * s);
    o += p.disc(...T([1.4, -6]), 1.3 * s, "paper", 1, .55 * s) + p.disc(...T([3.4, -5.6]), 1.3 * s, "paper", 1, .55 * s) + p.dot(...T([1.6, -6]), .45 * s) + p.dot(...T([3.6, -5.6]), .45 * s);
    return { svg: o, T, top: T([0, -8]) };
  }
  if (kind === "dragon") return dragon(p, x, y, s, flip);
  // 벌레: 작게
  if (kind === "butterfly") {
    o += [[-1, -3.6, 2.6, 2.2, -.5], [-1, -1, 1.8, 1.5, .4], [.6, -4, 2.8, 2.3, .4], [.6, -1.2, 1.9, 1.5, -.4]].map(([cx, cy, rx, ry, r]) => p.area(p.blob(...T([cx, cy]), rx * s, ry * s, r * m, .05), "paper", 1) + p.ring(...T([cx, cy]), Math.min(rx, ry) * s, .4 * s)).join("");
    o += p.line(TT([[-.2, -5], [-.2, .6]]), .7 * s) + p.line(TT([[-.2, -5], [-1.6, -7.4]]), .3 * s) + p.line(TT([[-.2, -5], [1.2, -7.4]]), .3 * s);
    return { svg: o, T, top: T([0, -8]) };
  }
  if (kind === "dragonfly") {
    o += p.line(TT([[-7, -3], [3, -3.4]]), .8 * s) + p.dot(...T([3.6, -3.4]), .9 * s);
    o += [[-1, -5.6], [-1, -.6], [1, -5.4], [1, -1]].map(([cx, cy]) => p.ring(...T([cx + (cx < 0 ? -1.4 : 1.4), cy]), 1.4 * s, .35 * s, null, .7)).join("");
    return { svg: o, T, top: T([0, -7]) };
  }
  if (kind === "cicada") {
    o += p.area(p.blob(...T([0, -3]), 3 * s, 1.6 * s, 0, .05), null, .8) + p.area(TT([[1, -4.2], [-5.6, -6], [-6, -3.4], [1, -3.2]]), "paper", .9) + p.line(TT([[1, -4.2], [-5.6, -6], [-6, -3.4], [1, -3.2]]), .35 * s, null, .7);
    return { svg: o, T, top: T([0, -7]) };
  }
  if (kind === "mantis") {
    o += p.line(TT([[-6, -2], [0, -5.4], [2.6, -8.4]]), .7 * s) + p.dot(...T([3, -9]), .9 * s) + p.line(TT([[1, -6.4], [3.6, -5], [3, -7.8]]), .5 * s) + p.line(TT([[-3, -3.6], [-4, 0]]), .35 * s) + p.line(TT([[-1, -4.6], [0, 0]]), .35 * s);
    return { svg: o, T, top: T([0, -10]) };
  }
  if (kind === "ant" || kind === "bee") {
    o += [[-2, -1.2, 1], [0, -1.4, .8], [1.8, -1.6, .9]].map(([cx, cy, r]) => p.dot(...T([cx, cy]), r * s, null, .9)).join("");
    o += [-1.4, 0, 1.4].map((lx) => p.line(TT([[lx, -1.4], [lx - .6, 0]]), .3 * s) + p.line(TT([[lx, -1.4], [lx + .4, -2.8]]), .3 * s)).join("");
    if (kind === "bee") o += p.ring(...T([0, -3.2]), 1.4 * s, .35 * s, null, .7);
    return { svg: o, T, top: T([0, -4]) };
  }
  // 지렁이 · 자벌레 · 노래기
  const pts = []; for (let j = 0; j <= 8; j++) pts.push([-6 + j * 1.5, -1 - Math.abs(Math.sin(j * .8)) * 2.4]);
  o += p.bl(TT(pts), .9 * s, null, .85, EVEN);
  return { svg: o, T, top: T([0, -4]) };
}
/** 용: 원 위를 감도는 긴 몸 */
function dragon(p, x, y, s, flip) {
  const m = flip ? -1 : 1, T = ([px, py]) => [x + m * px * s, y + py * s];
  const pts = []; for (let j = 0; j <= 30; j++) { const t = j / 30; pts.push(T([-34 + 68 * t, -12 - 10 * Math.sin(t * PI * 2.2) * (1 - t * .3)])); }
  const c = cr(pts, false, 3), W = [[0, .1], [.2, .7], [.6, 1], [.92, .85], [1, .6]];
  let o = `<path d="${outline(c, c.map((_, j) => 3.2 * s * ease(W, j / (c.length - 1))))}" ${p.fa(null, .8)}/>`;
  for (let u = 2; u < 16; u++) { const [px, py, a] = c[Math.round((c.length - 1) * u / 17)]; o += p.line([[px - Math.sin(a) * 2, py + Math.cos(a) * 2], [px + Math.sin(a) * 2, py - Math.cos(a) * 2]], .45, "paper", .55); if (u % 3 === 0) o += p.tick(px, py, a - PI / 2, 4 * s, .7 * s, null, .8); }
  const [hx, hy, ha] = c[c.length - 1];
  o += p.area(p.blob(hx + Math.cos(ha) * 3 * s, hy + Math.sin(ha) * 3 * s, 4.6 * s, 3.2 * s, ha, .1), null, .9);
  o += p.bl([[hx, hy - 2 * s], [hx - Math.cos(ha) * 4 * s, hy - 7 * s]], .7 * s, null, .9, TAPER) + p.bl([[hx + 1, hy - 2 * s], [hx - Math.cos(ha) * 1 * s, hy - 8 * s]], .6 * s, null, .9, TAPER);
  o += p.bl([[hx + Math.cos(ha) * 6 * s, hy + Math.sin(ha) * 6 * s], [hx + Math.cos(ha) * 12 * s, hy + 3 * s], [hx + Math.cos(ha) * 16 * s, hy + 8 * s]], .4 * s, null, .7, TAPER);
  return { svg: o, T, top: [hx, hy - 8] };
}
/** 동물 하나: 갈래에 따라 */
function animal(p, kind, pose, x, y, s, flip) {
  if (["crane", "rooster", "phoenix", "roc", "goose", "hawk", "duck", "owl", "pheasant", "bird"].includes(kind)) return bird(p, kind, pose, x, y, s, flip);
  if (QUAD[kind] || ["rabbit", "monkey", "squirrel"].includes(kind)) return quad(p, kind, pose, x, y, s, flip);
  return critter(p, kind, pose, x, y, s, flip);
}

/* ───────────── 원: 무엇인가 ───────────── */
const CIRCLE_FIRST = [[/우물/, "well"], [/반딧불/, "lamp"], [/엽전/, "coin"], [/해시계/, "sundial"], [/저울/, "scale"], [/나이테|그루터기|밑동/, "rings"], [/화씨벽/, "jade"], [/논배미/, "paddy"], [/베틀/, "loom"], [/바둑판|산판|활자판/, "board"], [/그림쇠/, "drawcompass"], [/나침반/, "compass"], [/돋보기 같은 해/, "sun"], [/물레방아|물레바퀴/, "wheel"]];
const CIRCLE = [
  ["coin", /엽전/], ["inkstone", /벼루/], ["whet", /숫돌/], ["sieve", /조리|뜨는 둥근 발/], ["lens", /돋보기/], ["target", /과녁/], ["bowarc", /활의|활시위/],
  ["wheel", /바퀴|물레|굴렁쇠|팽이/], ["well", /우물/], ["spring", /샘/], ["vortex", /소용돌이/],
  ["pond", /연못|못(?!하)|호수|웅덩이|늪|동정호/], ["sea", /바다|북해/], ["river", /강물|강(?!남|수)|시내|냇물|여울|물길|흐르는 물|울돌목/],
  ["water", /물결|물(?!레|들|고기|감|방울|독|그릇|을 머금)|물거울/],
  ["lamp", /등잔|등불|촛불|화로|풀무|불(?!어)|아궁이/], ["tree", /나무|소나무|귤나무|오동|매화|꽃가지|솔가지|수관|꽃그늘|그늘|숲/],
  ["flower", /꽃(?!가지|그늘)|모란|철쭉|유채/], ["sprout", /새싹|싹/], ["mirror", /거울/], ["jade", /옥|구슬|원석|보배|금덩이|보물/],
  ["drum", /북(?!해)/], ["bell", /종(?!이)|편경/],
  ["vessel", /그릇|사발|대야|솥|항아리|독(?!서)|단지|표주박|(?<!잔)잔(?!잔)|소반|밥상|쟁반|광주리|바구니|곡식 되|구유|약탕관|주머니|곳간|제사상|가마/],
  ["nest", /둥지/], ["egg", /알(?!맞)|달걀|고치/], ["fruit", /귤|오얏|참외|과일|열매/],
  ["gate", /문|창(?!고)|홍예|구멍|입구|동굴|(?<!얼)굴|구덩이/], ["fort", /성곽|성(?!인)|망루|목탑/], ["altar", /단$|대$|영대|무우/],
  ["yard", /마당|터$|땅|들판|화단|자리|방석|섬|개밋둑|우리|울타리/], ["net", /그물/], ["thread", /실타래|끈|허리띠|고리|천$/], ["tent", /장막|군막/],
  ["mountain", /산(?!판)|봉우리|산마루/], ["sky", /하늘|별|천하도|지도/], ["stone", /바위|돌(?!아)|주춧돌|비석|모루|징검/], ["shield", /방패/],
  ["scroll", /두루마리|죽간/], ["letter", /이응/], ["boat", /배$/], ["box", /상자|갑$/],
  ["moon", /달(?!걀|군)/], ["sun", /(?<![북남동서황])해(?!시계)|햇|볕|일식/],
];
/** 원 낱말 → 갈래. 앞말(— 앞)에서 가장 뒤에서 끝나는 낱말이 원이다("산 위의 해" → 해). 같은 데서 끝나면 긴 낱말 */
export function circleKind(text) {
  const head = String(text || "").split(" — ")[0].replace(/\([^()]*\)/g, "").trim();
  for (const [re, k] of CIRCLE_FIRST) if (re.test(head)) return { kind: k, head };
  let best = null;
  for (const [k, re] of CIRCLE) {
    const g = new RegExp(re.source, "g"); let mm, end = -1, len = 0;
    while ((mm = g.exec(head))) { const e2 = mm.index + mm[0].length; if (e2 >= end) { end = e2; len = mm[0].length; } if (!mm[0]) g.lastIndex++; }
    if (end >= 0 && (!best || end > best.end || (end === best.end && len > best.len))) best = { k, end, len };
  }
  return { kind: best ? best.k : "plain", head };
}

/** 원 둘레 꾸밈 → {b: 원 뒤, f: 원 위, wash: 원 안 바탕색} */
function dressCircle(S, kind, text) {
  const { p, R } = S, rs = p.rs;
  let b = "", f = "", wash = null;
  const t = text;
  const rays = (n, r0, r1, col, op, a0, a1) => { let o = ""; for (let u = 0; u < n; u++) { const a = (a0 ?? 0) + ((a1 ?? 2 * PI) - (a0 ?? 0)) * (u + .5) / n + (rs() - .5) * .08; o += p.bl([pol(a, r0), pol(a, r1 + (u % 2) * (r1 - r0) * .35)], .9, col, op, TAPER); } return o; };
  const waves = (r, a0, a1, op, k) => { const pts = []; for (let j = 0; j <= 10; j++) { const a = a0 + (a1 - a0) * j / 10; pts.push(pol(a, r + Math.sin(j * 1.7 + (k || 0)) * 1.2)); } return p.bl(pts, .8, null, op, SOFT); };
  const ripples = (n, op) => { let o = ""; for (let u = 0; u < n; u++) { const q = R + 6 + u * 6, a0 = rad(150 + u * 7 + rs() * 10), a1 = rad(390 - u * 9 - rs() * 10); o += waves(q, a0, a1, op - u * .05, u); } return o; };
  switch (kind) {
    case "sun": {
      wash = ["gold", .13];
      const rise = /새벽|떠오르|동트|아침|처음 솟|솟는/.test(t), set = /지는|저녁|노을/.test(t);
      if (/일식|가려진/.test(t)) { f += `<path d="M0 ${f1(-R)}A${f1(R)} ${f1(R)} 0 0 1 0 ${f1(R)}A${f1(R * .55)} ${f1(R)} 0 0 0 0 ${f1(-R)}Z" ${p.fa(null, .22)}/>`; b += rays(16, R + 4, R + 9, "gold", .5); break; }
      if (rise || set) { b += rays(9, R + 4, R + 12, "gold", .6, rad(set ? 200 : 190), rad(set ? 340 : 350)); b += p.bl([[-R - 26, R * .45], [0, R * .5], [R + 26, R * .42]], 1.1, null, .5, SOFT); b += waves(R * .62, rad(160), rad(20), .25); }
      else b += rays(/가을|겨울|희미|눈 내리/.test(t) ? 10 : 14, R + 4, R + 11, "gold", /희미/.test(t) ? .35 : .62);
      if (/달/.test(t)) S.sky.push("moon");
      break;
    }
    case "moon": {
      wash = ["gold", .08];
      b += p.ring(0, 0, R + 6, .6, "gold", .25) + p.ring(0, 0, R + 11, .4, "gold", .14);
      if (/반은|반쯤|차오르|초승|새벽|지는/.test(t)) f += `<path d="M0 ${f1(-R)}A${f1(R)} ${f1(R)} 0 0 0 0 ${f1(R)}A${f1(R * .45)} ${f1(R)} 0 0 1 0 ${f1(-R)}Z" ${p.fa(null, .13)}/>`;
      if (/해/.test(t)) S.sky.push("sun");
      break;
    }
    case "wheel": {
      const water = /물레방아|물레바퀴/.test(t), top = /팽이/.test(t), hoop = /굴렁쇠/.test(t);
      if (top) { f += p.bl(p.arc(0, 0, R + 5, rad(200), rad(320)), .8, null, .45, SOFT) + p.bl(p.arc(0, 0, R + 9, rad(215), rad(305)), .6, null, .3, SOFT) + p.area([[-6, R], [6, R], [0, R + 12]], null, .8); break; }
      b += p.ring(0, 0, R + 3.4, 3.4, null, .85);
      if (!hoop) { for (let u = 0; u < 10; u++) { const a = u / 10 * 2 * PI + .2; f += p.line([pol(a, R * .2), pol(a, R + 1.6)], .9, null, .28); } f += p.disc(0, 0, R * .17, "paper", 1, 1.2); }
      if (water) for (let u = 0; u < 12; u++) { const a = u / 12 * 2 * PI; b += p.area([pol(a - .07, R + 4), pol(a - .05, R + 11), pol(a + .05, R + 11), pol(a + .05, R + 4)], "paper", 1) + p.line([pol(a - .05, R + 11), pol(a + .05, R + 11)], .9, null, .8); }
      else if (!hoop) for (let u = 0; u < 24; u++) { const a = u / 24 * 2 * PI; b += p.line([pol(a, R + 5), pol(a, R + 6.6)], .5, null, .4); }
      if (water) b += [0, 1, 2].map((k) => p.bl([[-R - 30, -R * .5 + k * 4], [-R * .7, -R * .7 + k * 3], [-R * .2, -R - 6 + k * 2]], .8, null, .4, SOFT)).join("");
      if (hoop) f += p.line([[R * .7, R * .7], [R + 16, R + 30]], 1, null, .8);
      break;
    }
    case "target": {
      b += p.ring(0, 0, R + 4.6, 3.2, null, .82) + p.ring(0, 0, R + 9, .8, null, .5);
      b += p.line([[0, R + 10], [0, S.gy]], 1.4, null, .7) + p.line([[-8, S.gy], [8, S.gy]], 1.4, null, .7);
      if (/버들/.test(t)) f += p.leaf(R * .15, -R - 12, rad(80), 12, 1.8, null, .7);
      break;
    }
    case "bowarc": {
      b += p.bl(p.arc(0, 0, R + 7, rad(110), rad(250), 16), 2.2, null, .85, [[0, .3], [.5, 1], [1, .3]]);
      const e1 = pol(rad(110), R + 7), e2 = pol(rad(250), R + 7);
      b += p.line([e2, [R + 18, 0], e1], .5, null, .8) + p.bl([[R + 18, 0], [-R - 22, 0]], .7, null, .0001);
      f += p.line([[R + 18, 0], [R + 30, 0]], .7, null, .85) + p.area([[R + 30, -2], [R + 36, 0], [R + 30, 2]], null, .9);
      break;
    }
    case "well": {
      wash = [null, .07];
      const q = R + 6, w = 3.4;
      b += p.poly([[-q - w, -q - w], [q + w, -q - w], [q + w, q + w], [-q - w, q + w]], "paper", 1);
      b += [[-q - w, -q - w, q + w, -q - w], [q + w, -q - w, q + w, q + w], [q + w, q + w, -q - w, q + w], [-q - w, q + w, -q - w, -q - w]].map(([x0, y0, x1, y1]) => p.bl([[x0, y0], [x1, y1]], 1.3, null, .85, EVEN)).join("");
      for (let u = -2; u <= 2; u++) b += p.line([[u * q * .42, -q - w], [u * q * .42, -q - w + 3.4]], .5, null, .5) + p.line([[u * q * .42, q + w], [u * q * .42, q + w - 3.4]], .5, null, .5);
      b += [-1, 1].map((k) => p.bl([[k * (q * .62), -q - w - 10], [k * (q * .62), q + w + 10]], 1.8, null, .85, EVEN) + p.bl([[-q - w - 10, k * (q * .62)], [q + w + 10, k * (q * .62)]], 1.8, null, .85, EVEN)).join("");
      break;
    }
    case "spring": {
      wash = [null, .06];
      b += ripples(2, .35);
      for (let u = 0; u < 3; u++) f += p.bl(p.arc(0, -R * .35, 4 + u * 3.2, rad(200), rad(340), 5), .6, null, .45, SOFT);
      b += p.bl([[R * .4, R - 2], [R * .9, R + 14], [R * .6, R + 26], [R + 10, S.gy - 4]], 2.6, null, .25, SOFT);
      break;
    }
    case "pond": case "water": case "vortex": {
      wash = [null, kind === "pond" ? .08 : .06];
      if (kind === "vortex") { for (let u = 0; u < 4; u++) b += p.bl(p.arc(0, 0, R + 5 + u * 5, rad(u * 50), rad(u * 50 + 230)), .9, null, .5 - u * .08, SOFT); break; }
      b += ripples(/고요|잔잔|맑은|얼어|먹빛/.test(t) ? 2 : 3, .42);
      if (kind === "pond") {
        if (!/얼어/.test(t)) for (let u = 0; u < 5; u++) { const x = -R - 2 + u * 3.6, y = R * .5 + 2; b += p.leaf(x, y + 8, rad(-90 - 12 + u * 6), 14 + u * 2, .9, null, .55); }
        for (let u = 0; u < 4; u++) { const a = rad(30 + u * 22); b += p.area(p.blob(...pol(a, R + 4), 3.2, 2, a, .3), null, .5); }
      }
      if (/얼어|언 /.test(t)) for (let u = 0; u < 3; u++) f += p.line([pol(rad(200 + u * 40), R * .3), pol(rad(210 + u * 40), R * .9)], .5, "paper", .7);
      break;
    }
    case "sea": case "river": {
      wash = [null, .07];
      for (let u = 0; u < 4; u++) { const y = R * (.3 + u * .3) + 4; b += p.bl([[-R - 60 + u * 8, y], [-R - 20, y - 3], [0, y + 1], [R + 30, y - 2], [R + 64 - u * 6, y]], .8, null, .32 - u * .05, SOFT); }
      if (kind === "sea") for (let u = 0; u < 3; u++) { const x = -R - 30 + u * (R + 30), y = R + 14; b += p.bl([[x - 8, y], [x, y - 6], [x + 4, y - 5], [x + 3, y - 2]], 1, null, .45, TAPER); }
      break;
    }
    case "lamp": {
      wash = ["gold", .12];
      const fire = /화로|풀무|아궁이|불 속/.test(t), candle = /촛불|초$|촛대/.test(t), fly = /반딧불/.test(t), lantern = /등불/.test(t);
      if (fly) { f += `<path d="M${P2(-R * .9, -R * .45)}Q0 ${f1(-R - 10)} ${P2(R * .9, -R * .45)}" ${p.st(null, 1.2, .8)}/>` + p.line([[-R * .9, -R * .45], [-R * .6, -R - 4]], .6, null, .7) + p.line([[R * .9, -R * .45], [R * .6, -R - 4]], .6, null, .7); for (let u = 0; u < 9; u++) f += p.dot(...pol(rs() * 2 * PI, rs() * R * .7), 1.2, "gold", .9); break; }
      if (fire) { b += p.area([[-R - 6, R * .2], [R + 6, R * .2], [R * .7, R + 8], [-R * .7, R + 8]], null, .78) + p.line([[-R - 8, R * .2], [R + 8, R * .2]], 1.6, null, .9); for (let u = 0; u < 3; u++) b += p.bl([[-8 + u * 8, -R - 4], [-11 + u * 8, -R - 12], [-7 + u * 8, -R - 20]], .7, null, .4, SOFT); break; }
      const fy = R - 6;
      f += `<path d="M${P2(0, fy - 8)}C${P2(3.8, fy - 2)} ${P2(2.8, fy + 2)} ${P2(0, fy + 2.6)}C${P2(-2.8, fy + 2)} ${P2(-3.8, fy - 2)} ${P2(0, fy - 8)}Z" ${p.fa("gold", .95)}/>`;
      if (candle) b += p.poly([[-3, R - 3], [3, R - 3], [3, R + 22], [-3, R + 22]], "paper", 1) + p.line([[-3, R - 3], [-3, R + 22], [3, R + 22], [3, R - 3]], .9, null, .85) + p.bl([[0, R + 22], [0, S.gy - 2]], 1.3, null, .85) + p.area([[-8, S.gy - 3], [8, S.gy - 3], [6, S.gy], [-6, S.gy]], null, .8);
      else if (lantern) { b += p.line([[0, -R - 4], [0, -R - 16]], .8, null, .8) + [-1, 1].map((k) => p.line([[k * R * .5, -R * .9], [k * R * .7, 0], [k * R * .5, R * .9]], .6, null, .45)).join("") + p.area([[-R * .45, -R - 5], [R * .45, -R - 5], [R * .35, -R - 1], [-R * .35, -R - 1]], null, .85) + p.area([[-R * .45, R + 5], [R * .45, R + 5], [R * .35, R + 1], [-R * .35, R + 1]], null, .85); }
      else { f += p.area([[-7, fy + 2.8], [7, fy + 2.8], [4.6, fy + 5.8], [-4.6, fy + 5.8]], null, .85); b += p.bl([[0, R + 4], [0, S.gy - 3]], 1.3, null, .85) + p.area([[-9, S.gy - 4], [9, S.gy - 4], [7, S.gy], [-7, S.gy]], null, .8); }
      b += rays(12, R + 4, R + 9, "gold", .5, rad(190), rad(350));
      break;
    }
    case "rings": {
      const gy = S.gy, tl = [-R - 1, 4], tr = [R + 1, 4], bl2 = [-R - 6, gy], br = [R + 6, gy];
      b += p.poly([tl, tr, [R + 3, gy * .6], br, bl2, [-R - 3, gy * .6]], null, .1) + p.bl([tl, [-R - 3, gy * .6], bl2], 1.6, null, .8, EVEN) + p.bl([tr, [R + 3, gy * .6], br], 1.6, null, .8, EVEN);
      for (let u = 0; u < 7; u++) { const x = -R + 6 + u * (2 * R - 12) / 6 + (rs() - .5) * 3; b += p.bl([[x, R + 4 + rs() * 8], [x + (rs() - .5) * 2, gy - 6 - rs() * 10]], .6, null, .35, TAPER); }
      for (const k of [-1, 1]) b += p.bl([[k * (R + 4), gy - 4], [k * (R + 14), gy - 1], [k * (R + 24), gy + 1]], 2, null, .7, TAPER) + p.bl([[k * (R * .3), gy - 2], [k * (R * .5), gy + 3], [k * (R * .7), gy + 6]], 1.4, null, .5, TAPER);
      const bark = []; for (let u = 0; u <= 40; u++) { const a = u / 40 * 2 * PI; bark.push(pol(a, R + 3 + (u % 3 === 0 ? 1.4 : 0) + rs() * .6)); }
      b += p.area(bark, null, .72) + p.disc(0, 0, R + 1.6, "paper", 1);
      f += p.line([pol(rad(-60), R * .15), pol(rad(-60), R * .95)], .5, null, .35);
      break;
    }
    case "tree": case "flower": case "sprout": {
      if (kind === "tree") {
        const plum = /매화|꽃가지|철쭉/.test(t), pine = /소나무|솔/.test(t);
        b += p.bl([[3, R + 2], [1, R + 18], [4, S.gy]], 5, null, .8, [[0, .6], [1, 1]]);
        for (let u = 0; u < 22; u++) { const a = rs() * 2 * PI, q = R + 2 + rs() * 9; b += pine ? p.tick(...pol(a, q), a + rad(90), 6, 1.1, null, .55) : p.leaf(...pol(a, q - 3), a + (rs() - .5), 7 + rs() * 4, 1.6, null, .45); }
        if (plum) for (let u = 0; u < 10; u++) { const a = rs() * 2 * PI, [x, y] = pol(a, R + 4 + rs() * 6); b += p.disc(x, y, 1.8, "paper", 1, .5) + p.dot(x, y, .5, "ju", .9); }
      } else if (kind === "flower") {
        for (let u = 0; u < 8; u++) { const a = u / 8 * 2 * PI + .2, [x, y] = pol(a, R + 6); b += p.area(p.blob(x, y, 7, 4.4, a, .1), "paper", 1) + p.bl(p.blob(x, y, 7, 4.4, a, .05).concat([p.blob(x, y, 7, 4.4, a, .05)[0]]), .7, null, .7, EVEN); }
        b += p.bl([[0, R + 8], [-2, R + 22], [0, S.gy]], 1.4, null, .8) + p.leaf(-1, R + 20, rad(200), 12, 2, null, .6) + p.leaf(0, R + 26, rad(-20), 11, 2, null, .6);
      } else { b += p.bl([[0, R + 2], [0, S.gy]], 1.2, null, .8) + p.leaf(0, -R - 2, rad(-130), 14, 2.2, null, .7) + p.leaf(0, -R - 2, rad(-50), 14, 2.2, null, .7); }
      break;
    }
    case "mirror": {
      b += p.ring(0, 0, R + 4, 3, null, .85) + p.ring(0, 0, R + 7.6, .6, null, .5);
      b += p.area([[-4, R + 6], [4, R + 6], [6, S.gy - 8], [-6, S.gy - 8]], null, .75) + p.area([[-12, S.gy - 8], [12, S.gy - 8], [9, S.gy], [-9, S.gy]], null, .8);
      f += p.line(p.arc(0, 0, R * .82, rad(200), rad(240), 4), 1.4, "paper", .5);
      if (/반으로/.test(t)) f += p.line([[0, -R - 3], [2, -R * .3], [-1, R * .3], [0, R + 3]], .9, null, .7);
      break;
    }
    case "jade": case "coin": case "shield": {
      if (kind === "coin") {
        const q = R * .34;
        f += `<rect x="${f1(-q / 2 - 3)}" y="${f1(-q / 2 - 3)}" width="${f1(q + 6)}" height="${f1(q + 6)}" ${p.st(null, 1.1, .55)}/>` + p.area([[-q / 2, -q / 2], [q / 2, -q / 2], [q / 2, q / 2], [-q / 2, q / 2]], "paper", 1) + `<rect x="${f1(-q / 2)}" y="${f1(-q / 2)}" width="${f1(q)}" height="${f1(q)}" ${p.st(null, 1.2)}/>`;
        b += p.ring(0, 0, R + 3.4, 2.4, null, .8);
        if (/꾸러미|고리/.test(t)) b += p.bl([[-R - 30, -R * .2], [-R - 6, 0]], 1.1, null, .7) + p.bl([[R + 6, 0], [R + 30, R * .3], [R + 26, R + 10]], 1.1, null, .7);
        break;
      }
      b += p.ring(0, 0, R + 3.6, 2.6, null, .82) + p.ring(0, 0, R + 7.4, .6, null, .45);
      if (kind === "shield") { for (let u = 0; u < 12; u++) b += p.dot(...pol(u / 12 * 2 * PI, R + 3.6), 1, "paper", 1); f += p.disc(0, 0, R * .16, "paper", 1, 1.2); break; }
      if (/화씨벽|구멍|원반|벽$/.test(t)) f += p.disc(0, 0, R * .17, "paper", 1, 1.1) + p.bl([[0, -R - 5], [-3, -R - 14], [0, -R - 22]], .8, null, .8) + p.bl([[-1, -R - 22], [-4, -R - 30]], 1.6, null, .7, TAPER) + p.bl([[1, -R - 22], [3, -R - 31]], 1.6, null, .7, TAPER);
      if (/원석|금덩이|돌처럼|흰 옥을|쪼고|갈아/.test(t)) for (let u = 0; u < 8; u++) { const a = u / 8 * 2 * PI + .3; b += p.tick(...pol(a, R + 9), a, 4, .9, null, .4); }
      f += p.line(p.arc(0, 0, R * .78, rad(205), rad(245), 4), 1.4, "paper", .45);
      break;
    }
    case "inkstone": case "whet": case "box": case "loom": case "sieve": case "board": {
      const q = R + 10;
      if (kind === "board") { for (let u = -4; u <= 4; u++) { const v = u * (R + 18) / 4; b += p.line([[v, -R - 20], [v, R + 20]], .5, null, .45) + p.line([[-R - 20, v], [R + 20, v]], .5, null, .45); } for (let u = 0; u < 6; u++) { const x = (Math.round(rs() * 8) - 4) * (R + 18) / 4, y = (Math.round(rs() * 8) - 4) * (R + 18) / 4; if (Math.hypot(x, y) > R + 3) b += p.disc(x, y, 3, u % 2 ? "paper" : null, 1, .7); } break; }
      if (kind === "sieve") { b += p.ring(0, 0, R + 3, 2.2, null, .8) + p.line([[R + 4, R * .2], [R + 34, R * .8]], 1.4, null, .8); for (let u = -3; u <= 3; u++) f += p.line([[u * R / 3.5, -Math.sqrt(R * R - (u * R / 3.5) ** 2)], [u * R / 3.5, Math.sqrt(R * R - (u * R / 3.5) ** 2)]], .3, null, .25); break; }
      if (kind === "loom") { b += p.bl([[-q - 8, -q - 6], [-q - 8, S.gy]], 2, null, .8) + p.bl([[q + 8, -q - 6], [q + 8, S.gy]], 2, null, .8) + p.bl([[-q - 12, -q - 6], [q + 12, -q - 6]], 2, null, .8) + p.bl([[-q - 12, R + 8], [q + 12, R + 8]], 1.6, null, .7); for (let u = -6; u <= 6; u++) b += p.line([[u * 5, -q - 6], [u * 5, -R - 2]], .35, null, .45) + p.line([[u * 5, R + 2], [u * 5, R + 8]], .35, null, .45); break; }
      const h = kind === "whet" ? q * .55 : q;
      b += p.poly([[-q - 4, -h], [q + 4, -h], [q + 4, h], [-q - 4, h]], kind === "box" ? "paper" : null, kind === "box" ? 1 : .16) + p.line([[-q - 4, -h], [q + 4, -h], [q + 4, h], [-q - 4, h], [-q - 4, -h]], 1.3, null, .8);
      if (kind === "inkstone") b += p.bl([[q + 12, -h - 14], [q + 18, h - 4]], 4, null, .85, EVEN);
      break;
    }
    case "drum": case "bell": {
      if (kind === "bell" && /편경/.test(t)) { b += p.bl([[-R - 18, -R - 14], [R + 18, -R - 14]], 2, null, .85) + p.bl([[-R - 16, -R - 14], [-R - 16, S.gy]], 1.8, null, .85) + p.bl([[R + 16, -R - 14], [R + 16, S.gy]], 1.8, null, .85); break; }
      b += p.ring(0, 0, R + 3.6, 3, null, .85);
      if (kind === "drum") { for (let u = 0; u < 16; u++) b += p.dot(...pol(u / 16 * 2 * PI, R + 3.6), .9, "paper", 1); b += p.bl([[-R * .5, R + 4], [-R * .8, S.gy]], 1.6, null, .8) + p.bl([[R * .5, R + 4], [R * .8, S.gy]], 1.6, null, .8) + p.bl([[-R * .8, S.gy - R * .2], [R * .8, S.gy - R * .2]], 1, null, .5); f += p.bl([[R + 4, -R - 14], [R * .62, -R * .62]], 1.3, null, .9) + p.dot(R * .62, -R * .62, 2, null, .9); }
      else { b += p.bl([[0, -R - 4], [0, -R - 14]], 1.6, null, .85) + p.bl([[-R - 20, -R - 14], [R + 20, -R - 14]], 2, null, .85) + p.bl([[R + 8, -R * .2], [R + 30, -R * .1]], 3, null, .8, EVEN) + p.line([[R + 20, -R * .15], [R + 20, -R - 14]], .5, null, .7); }
      break;
    }
    case "vessel": {
      wash = /물|국|밥|약|쌀|여물/.test(t) ? [null, .06] : null;
      const cauldron = /솥|약탕관/.test(t), jar = /항아리|독|단지/.test(t), table = /소반|밥상|제사상/.test(t), basket = /광주리|바구니/.test(t), bag = /주머니/.test(t), cup = /잔$|술잔/.test(t), barn = /곳간/.test(t);
      b += p.ring(0, 0, R + 3, 2.4, null, .85) + p.ring(0, 0, R + 6.6, .7, null, .5);
      if (cauldron) { b += [-1, 1].map((k) => p.bl([[k * (R + 2), -R * .2], [k * (R + 9), -R * .3], [k * (R + 9), R * .1], [k * (R + 2), 0]], 1.4, null, .8)).join("") + [-1, 0, 1].map((k) => p.bl([[k * R * .6, R + 2], [k * R * .75, S.gy]], 2.2, null, .8)).join(""); if (/김|아궁이|가마솥|국솥/.test(t)) for (let u = 0; u < 3; u++) b += p.bl([[-8 + u * 8, -R - 6], [-11 + u * 8, -R - 14], [-7 + u * 8, -R - 22]], .7, null, .4, SOFT); if (/깨진/.test(t)) f += p.line([[R * .3, -R - 3], [R * .1, -R * .4], [R * .4, 0]], .9, null, .8); }
      else if (jar) { b += p.area([[-R - 16, R * .1], [R + 16, R * .1], [R + 10, R + 18], [-R - 10, R + 18]], null, .14) + p.bl([[-R - 16, R * .1], [-R - 10, R + 18], [R + 10, R + 18], [R + 16, R * .1]], 1.2, null, .7); }
      else if (table) { b += [-1, 1].map((k) => p.bl([[k * R * .7, R + 4], [k * R * .9, S.gy]], 2, null, .8)).join("") + p.bl([[-R * .9, S.gy - 6], [R * .9, S.gy - 6]], 1.1, null, .6); if (/제사상|나뉨|나눈/.test(t)) for (let u = 0; u < 6; u++) f += p.line([[0, 0], pol(u / 6 * 2 * PI, R)], .5, null, .4); }
      else if (basket) { for (let u = 0; u < 30; u++) { const a = u / 30 * 2 * PI; b += p.line([pol(a, R + 3), pol(a + .12, R + 7)], .5, null, .55); } }
      else if (bag) { b += p.bl([[-R * .5, -R - 2], [0, -R - 8], [R * .5, -R - 2]], 1.4, null, .85) + p.bl([[0, -R - 8], [-4, -R - 16]], 1, null, .8, TAPER) + p.bl([[0, -R - 8], [5, -R - 15]], 1, null, .8, TAPER); }
      else if (cup) { b += p.bl([[0, R + 4], [0, R + 16]], 2.4, null, .8) + p.area([[-10, R + 16], [10, R + 16], [7, R + 20], [-7, R + 20]], null, .8); }
      else if (barn) { b += p.area([[-R - 18, -R - 2], [0, -R - 22], [R + 18, -R - 2]], null, .8); }
      else b += p.bl([[-R * .65, R + 4], [-R * .5, R + 10], [R * .5, R + 10], [R * .65, R + 4]], 1.3, null, .75);
      if (/기울어진/.test(t)) f += p.bl([[-R - 10, -R * .6], [R + 10, R * .3]], .0001, null, 0);
      break;
    }
    case "scale": {
      for (const k of [-1, 0, 1]) b += p.line([pol(rad(-90 + k * 55), R + 2), [0, -R - 26]], .5, null, .7);
      b += p.bl([[-R - 34, -R - 26], [R + 34, -R - 26]], 1.8, null, .85) + p.bl([[0, -R - 26], [0, -R - 36]], 1.1, null, .8) + p.line([[R + 30, -R - 26], [R + 30, -R - 10]], .5, null, .7) + p.area(p.blob(R + 30, -R - 6, 3.6, 4, 0, .1), null, .85);
      b += p.ring(0, 0, R + 2.6, 1.6, null, .8);
      break;
    }
    case "sundial": case "compass": case "drawcompass": case "sky": {
      if (kind === "sky") { wash = [null, .05]; for (let u = 0; u < 18; u++) { const [x, y] = pol(rs() * 2 * PI, R + 6 + rs() * 22); b += p.dot(x, y, .6 + rs() * .8, null, .7); } for (let u = 0; u < 3; u++) { const a = rs() * 2 * PI, q = R + 10; b += p.line([pol(a, q), pol(a + .25, q + 8), pol(a + .45, q + 4)], .35, null, .5); } if (/지도|천하도/.test(t)) b += p.ring(0, 0, R + 4, 1.4, null, .7); break; }
      if (kind === "drawcompass") { b += p.bl([[0, -R - 30], [-R * .1, 0]], 1.2, null, .85) + p.bl([[0, -R - 30], [R + .5, -2]], 1.2, null, .85) + p.disc(0, -R - 30, 2, null, .9); break; }
      for (let u = 0; u < 24; u++) { const a = u / 24 * 2 * PI; b += p.line([pol(a, R + 3), pol(a, R + (u % 6 === 0 ? 9 : u % 2 ? 5 : 6.6))], u % 6 === 0 ? .9 : .5, null, .6); }
      b += p.ring(0, 0, R + 2.4, 1.2, null, .7);
      if (kind === "sundial") b += p.area([[-R * .9, R + 6], [R * .9, R + 6], [R * .6, S.gy], [-R * .6, S.gy]], null, .2) + p.line([[-R * .9, R + 6], [-R * .6, S.gy]], .9, null, .7) + p.line([[R * .9, R + 6], [R * .6, S.gy]], .9, null, .7);
      if (kind === "compass") f += p.area([[0, -R * .8], [2.6, 0], [0, R * .8], [-2.6, 0]], null, .35);
      break;
    }
    case "nest": case "egg": case "fruit": {
      if (kind === "nest") { for (let u = 0; u < 34; u++) { const a = rs() * 2 * PI, q = R + 2 + rs() * 6; b += p.line([pol(a, q), pol(a + .3 + rs() * .3, q + (rs() - .5) * 4)], .6, null, .6); } if (/갈대/.test(t)) b += [-1, 1].map((k) => p.bl([[k * R * .6, S.gy], [k * R * .7, -R - 30]], .9, null, .7) + p.leaf(k * R * .7, -R - 28, rad(-90 + k * 30), 14, 1.4, null, .5)).join(""); break; }
      if (kind === "egg") { b += p.ring(0, 0, R + 2.6, 1.4, null, .8); if (/굴러/.test(t)) for (let u = 0; u < 3; u++) b += p.line([[-R - 8 - u * 6, -R * .3 + u * 8], [-R - 22 - u * 6, -R * .3 + u * 8]], .7, null, .45); if (/고치/.test(t)) for (let u = 0; u < 7; u++) f += p.line(p.arc(0, 0, R * (.35 + u * .09), rad(200 + u * 15), rad(300 + u * 15), 6), .3, null, .3); break; }
      b += p.ring(0, 0, R + 2.6, 1.6, null, .8) + p.bl([[0, -R - 1], [2, -R - 9]], 1.4, null, .85) + p.leaf(1.6, -R - 6, rad(-20), 13, 2.6, null, .7);
      if (/참외/.test(t)) for (let u = -2; u <= 2; u++) f += p.line(p.arc(-u * R * 2.2, 0, Math.hypot(R, u * R * 2.2), rad(u > 0 ? 170 : -10) - .4, rad(u > 0 ? 170 : -10) + .4, 6), .4, null, .25);
      break;
    }
    case "gate": case "fort": {
      if (kind === "fort") { b += p.ring(0, 0, R + 5, 6, null, .2) + p.ring(0, 0, R + 2.4, 1.2, null, .8) + p.ring(0, 0, R + 8, 1.2, null, .8); for (let u = 0; u < 16; u++) { const a = u / 16 * 2 * PI; b += p.area([pol(a - .07, R + 8), pol(a - .07, R + 12), pol(a + .07, R + 12), pol(a + .07, R + 8)], null, .75); } if (/목탑|망루/.test(t)) for (let u = 0; u < 3; u++) b += p.area([[-R * .7 + u * 6, -R - 10 - u * 10], [R * .7 - u * 6, -R - 10 - u * 10], [0, -R - 18 - u * 10]], null, .75); break; }
      const rock = /동굴|굴 입구|바위 구멍|구덩이|굴$/.test(t), arch = /홍예|성문|관/.test(t);
      if (rock) { const pts = []; for (let u = 0; u <= 22; u++) { const a = rad(180 + u / 22 * 360); pts.push(pol(a, R + 14 + rs() * 12)); } b += p.area(pts, null, .16) + p.bl(pts.slice(0, 14), 1.6, null, .7, SOFT); b += p.disc(0, 0, R + 2, "paper", 1); for (let u = 0; u < 8; u++) { const a = rs() * 2 * PI; b += p.tick(...pol(a, R + 6 + rs() * 10), a + 1, 4, .8, null, .4); } break; }
      const W = R + 30, top = -R - 22;
      b += p.poly([[-W, top], [W, top], [W, S.gy], [-W, S.gy]], null, .1);
      for (let y = top + 8, k = 0; y < S.gy; y += 8, k++) { b += p.line([[-W, y], [W, y]], .4, null, .25); for (let x = -W + (k % 2) * 7; x < W; x += 14) b += p.line([[x, y - 8], [x, y]], .35, null, .2); }
      b += p.disc(0, 0, R + 1.6, "paper", 1) + p.line([[-W, top], [-W, S.gy]], 1.2, null, .7) + p.line([[W, top], [W, S.gy]], 1.2, null, .7);
      b += p.area([[-W - 8, top + 2], [-W + 4, top - 8], [W - 4, top - 8], [W + 8, top + 2]], null, .82);
      if (arch) for (let u = 0; u < 13; u++) { const a = rad(180 + u * 15); b += p.line([pol(a, R + 2), pol(a, R + 9)], .7, null, .7); }
      b += p.ring(0, 0, R + 2.2, 1.6, null, .8);
      if (/창/.test(t)) { b += p.ring(0, 0, R + 5.4, .7, null, .5); if (/불빛|비침/.test(t)) wash = ["gold", .14]; }
      if (/반쯤 열린|월동/.test(t)) f += p.area([[R * .1, -R + 2], [R * .5, -R * .85], [R * .5, R * .85], [R * .1, R - 2]], "paper", .75) + p.line([[R * .1, -R + 2], [R * .1, R - 2]], .9, null, .8);
      break;
    }
    case "altar": case "yard": case "paddy": {
      if (kind === "paddy") {
        b += p.ring(0, 0, R + 3.8, 5.6, null, .12) + p.bl(p.arc(0, 0, R + 5.5, rad(20), rad(160), 16), .7, null, .45, SOFT) + p.bl(p.arc(0, 0, R + 5.5, rad(200), rad(340), 16), .7, null, .4, SOFT);
        for (let u = 0; u < 26; u++) { const a = u / 26 * 2 * PI, [x, y] = pol(a, R + 12); b += [-14, -2, 11].map((d) => p.leaf(x, y, rad(-90 + d), 6.4, .55, null, .55)).join(""); }
        wash = [null, .06];
        break;
      }
      if (kind === "altar") { for (let u = 0; u < 3; u++) { const w = R + 10 + u * 9, y = R + 4 + u * 7; b += p.poly([[-w, y], [w, y], [w, y + 7], [-w, y + 7]], "paper", 1) + p.line([[-w, y], [w, y], [w, y + 7], [-w, y + 7], [-w, y]], .9, null, .75); } break; }
      const fence = /울타리|우리/.test(t), mat = /자리|방석/.test(t), isl = /섬/.test(t), mound = /개밋둑|흙/.test(t), bed = /화단/.test(t);
      if (fence) { for (let u = 0; u < 20; u++) { const a = u / 20 * 2 * PI, [x, y] = pol(a, R + 7); b += p.bl([[x, y + 5], [x, y - 6]], 1.3, null, .8); } b += p.ring(0, 0, R + 5, .8, null, .6) + p.ring(0, 0, R + 9, .8, null, .6); break; }
      if (mat) { b += p.ring(0, 0, R + 3, 3.4, null, .55); for (let u = 0; u < 28; u++) { const a = u / 28 * 2 * PI; b += p.line([pol(a, R + 5), pol(a, R + 8.6)], .45, null, .5); } if (/네모/.test(t)) b += p.line([[-R - 14, -R - 14], [R + 14, -R - 14], [R + 14, R + 14], [-R - 14, R + 14], [-R - 14, -R - 14]], 1.2, null, .7); break; }
      if (isl) { wash = [null, .05]; b += ripples(3, .4); b += p.ring(0, 0, R + 2.4, 1.4, null, .75); break; }
      if (mound) { b += p.area([[-R - 18, R + 6], [-R * .6, -R * .2], [0, -R - 8], [R * .6, -R * .2], [R + 18, R + 6]], null, .14) + p.bl([[-R - 18, R + 6], [-R * .6, -R * .2], [0, -R - 8], [R * .6, -R * .2], [R + 18, R + 6]], 1, null, .6, SOFT); break; }
      if (bed) { for (let u = 0; u < 14; u++) { const [x, y] = pol(u / 14 * 2 * PI, R + 7); b += p.disc(x, y, 2.4, "paper", 1, .6) + p.dot(x, y, .8, null, .8); } break; }
      b += p.ring(0, 0, R + 3, 1.2, null, .6);
      for (let u = 0; u < 10; u++) { const a = rs() * 2 * PI; b += p.tick(...pol(a, R + 6 + rs() * 8), a + 1.6, 5, .7, null, .3); }
      break;
    }
    case "net": case "thread": case "tent": {
      if (kind === "net") { for (let u = 0; u < 16; u++) { const a = u / 16 * 2 * PI; b += p.line([pol(a, R + 2), pol(a, R + 22)], .45, null, .5); } for (let k = 1; k <= 3; k++) b += p.ring(0, 0, R + 2 + k * 6, .45, null, .5); for (let u = 0; u < 8; u++) b += p.dot(...pol(u / 8 * 2 * PI + .2, R + 22), 1.6, null, .7); break; }
      if (kind === "tent") { for (let u = 0; u < 12; u++) { const a = u / 12 * 2 * PI; b += p.line([pol(a, R + 2), pol(a, R + 9)], .6, null, .5); } b += p.ring(0, 0, R + 9, 1.4, null, .8) + p.ring(0, 0, R + 2.4, 1, null, .7); break; }
      for (let u = 0; u < 9; u++) { const q = R + 2 + rs() * 5, a0 = rs() * 2 * PI; b += p.line(p.arc(0, 0, q, a0, a0 + 2 + rs() * 2), .5, null, .6); }
      b += p.bl([pol(rad(40), R + 4), [R + 14, R + 18], [R + 6, R + 30], [R + 18, S.gy - 6]], .8, null, .8, LINE);
      break;
    }
    case "mountain": {
      const ridge = [[-R - 44, S.gy], [-R - 20, R * .3], [-R * .9, -R * .5], [-R * .3, -R - 8], [R * .3, -R - 12], [R * .9, -R * .4], [R + 22, R * .4], [R + 46, S.gy]];
      b += p.area([...ridge, [0, S.gy]], null, .08) + p.bl(ridge.slice(1, 7), 2, null, .8);
      for (let u = 0; u < 12; u++) { const x = (rs() - .5) * (R * 2 + 70), y = R * .2 + rs() * (S.gy - R * .4); if (Math.hypot(x, y) > R + 5 && y < S.gy - 5) b += p.bl([[x, y], [x - 3, y + 5]], .9, null, .4, TAPER); }
      if (/구름/.test(t)) b += cloud(p, -R - 6, -R * .2, 1.2) + cloud(p, R + 10, R * .1, 1);
      if (/아래|숨은/.test(t)) b += p.line([[-R - 40, 0], [R + 40, 0]], 1, null, .6);
      break;
    }
    case "stone": {
      if (/비석/.test(t)) { b += p.poly([[-R - 8, -R - 6], [-R * .7, -R - 18], [R * .7, -R - 18], [R + 8, -R - 6], [R + 8, S.gy - 6], [-R - 8, S.gy - 6]], "paper", 1) + p.line([[-R - 8, S.gy - 6], [-R - 8, -R - 6], [-R * .7, -R - 18], [R * .7, -R - 18], [R + 8, -R - 6], [R + 8, S.gy - 6]], 1.3, null, .8) + p.area([[-R - 14, S.gy - 6], [R + 14, S.gy - 6], [R + 12, S.gy], [-R - 12, S.gy]], null, .7); break; }
      if (/모루/.test(t)) { b += p.area([[-R - 14, -2], [R + 20, -2], [R + 8, 8], [R * .5, R + 6], [-R * .5, R + 6], [-R - 4, 6]], null, .75); break; }
      const pts = []; for (let u = 0; u < 9; u++) pts.push(pol(u / 9 * 2 * PI, R + 4 + rs() * 4));
      b += p.area(pts, null, .2) + p.bl([...pts, pts[0], pts[1]], 1.2, null, .7, EVEN);
      for (let u = 0; u < 6; u++) { const a = rs() * 2 * PI; b += p.tick(...pol(a, R + 6), a + 2, 4, .8, null, .45); }
      break;
    }
    case "scroll": { b += p.ring(0, 0, R + 2.8, 2.2, null, .8) + p.poly([[R * .2, -R - 2], [R + 44, -R + 4], [R + 44, R - 4], [R * .2, R + 2]], "paper", 1) + p.line([[R * .2, -R - 2], [R + 44, -R + 4], [R + 44, R - 4], [R * .2, R + 2]], .9, null, .7); for (let u = 0; u < 6; u++) b += p.line([[R + 8 + u * 6, -R + 6], [R + 8 + u * 6, R - 6]], .35, null, .35); f += p.line(p.arc(0, 0, R * .5, 0, 2 * PI, 24), .35, null, .3); break; }
    case "letter": { b += p.bl(p.arc(0, 0, R + 3, rad(-80), rad(270), 20), 3.6, null, .85, LINE); break; }
    case "boat": { const y = R + 8; b += p.area([[-R - 40, y - 4], [-R * .4, y], [R * .4, y], [R + 40, y - 6], [R + 30, y + 9], [-R - 30, y + 10]], null, .55) + p.bl([[-R - 40, y - 4], [0, y + .6], [R + 40, y - 6]], 1.2, null, .9) + p.bl([[R + 26, y + 2], [R + 36, y + 16]], 1.4, null, .85); break; }
    case "plain": default: break;
  }
  return { b, f, wash };
}

/* ───────────── 배경 ───────────── */
function cloud(p, x, y, s) { let o = ""; [[0, 0, 7], [6, -2, 5], [-6, 1, 5], [11, 2, 3.4]].forEach(([dx, dy, r]) => { o += p.bl(p.arc(x + dx * s, y + dy * s, r * s, rad(190), rad(350), 6), .7, null, .5, SOFT); }); return o + p.bl([[x - 10 * s, y + 3 * s], [x + 15 * s, y + 3.4 * s]], .5, null, .35, SOFT); }
function tree(p, x, y, s, kind, flip) {
  const m = flip ? -1 : 1; let o = "";
  if (kind === "willow") { o += p.bl([[x, y], [x + m * 1, y - 26 * s], [x - m * 2, y - 46 * s]], 3.2 * s, null, .82, [[0, 1], [1, .4]]); for (let u = 0; u < 9; u++) { const bx = x + (u - 4) * 4 * s, by = y - (40 + Math.abs(u - 4) * -1.2) * s; o += p.bl([[x - m * 1, y - 44 * s], [bx, by - 2 * s], [bx + m * 1.4 * s, by + 18 * s], [bx + m * 1 * s, by + 30 * s]], .5 * s, null, .55, TAPER); } return o; }
  if (kind === "bamboo") { for (let k = 0; k < 3; k++) { const bx = x + (k - 1) * 6 * s, h = (54 - k * 9) * s; o += p.bl([[bx, y], [bx + m * 1.4 * s, y - h]], 1.4 * s, null, .82, EVEN); for (let j = 1; j < 5; j++) o += p.line([[bx - 1.6 * s + m * j * .3, y - h * j / 5], [bx + 1.6 * s + m * j * .3, y - h * j / 5]], .5 * s, null, .9); for (let j = 0; j < 3; j++) o += p.leaf(bx + m * 1.4 * s, y - h * (.55 + j * .16), rad(m > 0 ? -20 - j * 30 : 200 + j * 30), 9 * s, 1.4 * s, null, .65); } return o; }
  if (kind === "pine") { o += p.bl([[x, y], [x - m * 3 * s, y - 20 * s], [x + m * 2 * s, y - 40 * s], [x - m * 1 * s, y - 52 * s]], 3 * s, null, .85, [[0, 1], [1, .5]]); [[-8, -48, 14], [6, -38, 16], [-6, -28, 13]].forEach(([dx, dy, w]) => { o += p.area([[x + m * (dx - w / 2) * s, y + dy * s], [x + m * (dx + w / 2) * s, y + dy * s], [x + m * (dx + w * .3) * s, y + (dy - 4) * s], [x + m * (dx - w * .3) * s, y + (dy - 4.6) * s]], null, .55); }); return o; }
  if (kind === "plum") { o += p.bl([[x, y], [x + m * 4 * s, y - 18 * s], [x - m * 3 * s, y - 32 * s], [x + m * 6 * s, y - 46 * s]], 2.6 * s, null, .85, [[0, 1], [1, .3]]) + p.bl([[x + m * 1 * s, y - 24 * s], [x + m * 12 * s, y - 30 * s], [x + m * 16 * s, y - 40 * s]], 1.2 * s, null, .8, TAPER); for (let u = 0; u < 12; u++) { const bx = x + m * (-6 + p.rs() * 22) * s, by = y - (22 + p.rs() * 26) * s; o += p.disc(bx, by, 1.6 * s, "paper", 1, .5) + p.dot(bx, by, .5 * s, "ju", .85); } return o; }
  o += p.bl([[x, y], [x - m * 1 * s, y - 22 * s], [x + m * 1.6 * s, y - 34 * s]], 3 * s, null, .85, [[0, 1], [1, .5]]) + p.bl([[x, y - 20 * s], [x + m * 9 * s, y - 30 * s]], 1.4 * s, null, .8, TAPER) + p.bl([[x, y - 24 * s], [x - m * 9 * s, y - 32 * s]], 1.2 * s, null, .8, TAPER);
  for (let u = 0; u < 16; u++) { const a = p.rs() * 2 * PI, q = p.rs() * 13 * s; o += p.leaf(x + Math.cos(a) * q * 1.2, y - 38 * s + Math.sin(a) * q * .8, a, 6 * s, 1.5 * s, null, .42); }
  return o;
}
function hut(p, x, y, s, tile, flip) {
  const m = flip ? -1 : 1, w = 15 * s, h = 12 * s;
  let o = p.poly([[x - w, y], [x + w, y], [x + w, y - h], [x - w, y - h]], "paper", 1) + p.line([[x - w, y], [x - w, y - h]], .9, null, .8) + p.line([[x + w, y], [x + w, y - h]], .9, null, .8);
  o += p.area([[x - w * 1.35, y - h + 1], [x - w * .8, y - h - 9 * s], [x + w * .8, y - h - 9 * s], [x + w * 1.35, y - h + 1]], null, tile ? .85 : .6);
  if (!tile) for (let u = 0; u < 6; u++) o += p.line([[x - w + u * w * .4, y - h - 8 * s], [x - w * 1.2 + u * w * .44, y - h]], .4, "paper", .5);
  o += p.area([[x + m * w * .1, y], [x + m * w * .1, y - h * .7], [x + m * w * .55, y - h * .7], [x + m * w * .55, y]], null, .5);
  return o;
}
function hills(p, x0, x1, y, h, op) { const pts = []; for (let u = 0; u <= 8; u++) { const t = u / 8; pts.push([x0 + (x1 - x0) * t, y - h * Math.sin(PI * t) * (.7 + .3 * Math.sin(t * 7 + x0))]); } return p.area([...pts, [x1, y + 1], [x0, y + 1]], null, op * .18) + p.bl(pts, 1.2, null, op, SOFT); }
function mountains(p, x0, x1, base, top, n) { let o = ""; for (let k = 0; k < n; k++) { const cx = x0 + (x1 - x0) * (k + .5) / n, w = (x1 - x0) / n * .9, h = top * (.7 + .3 * ((k * 7) % 3) / 2); const pts = [[cx - w, base], [cx - w * .4, base - h * .7], [cx - w * .1, base - h], [cx + w * .3, base - h * .8], [cx + w, base]]; o += p.area(pts, null, .07 + k * .02) + p.bl(pts.slice(1, 4), 1.3, null, .5, SOFT); } return o; }
function water(p, x0, x1, y0, y1, op, sea) { let o = ""; const n = Math.max(2, Math.round((y1 - y0) / 7)); for (let k = 0; k < n; k++) { const y = y0 + (y1 - y0) * (k + .5) / n; for (let u = 0; u < 3; u++) { const a = x0 + (x1 - x0) * (u / 3 + (k % 2) * .12) + p.rs() * 6, b = a + (x1 - x0) * .22; if (b > x1) continue; o += p.bl([[a, y], [(a + b) / 2, y - 1.6], [b, y]], .7, null, op - k * .03, SOFT); } } if (sea) for (let u = 0; u < 3; u++) { const x = x0 + (x1 - x0) * (u + .5) / 3, y = y0 + 4; o += p.bl([[x - 8, y + 2], [x, y - 4], [x + 4, y - 3], [x + 3, y]], .9, null, .45, TAPER); } return o; }

/* ───────────── 소품 ───────────── */
/* 그리기 갈래: [이름, 낱말]. 앞에서 먼저 맞는 것을 쓴다. scenery = 배경으로 그린다 */
const PROP = [
  ["fork", /갈림길|갈래 길|갈라지는 두 길|두 갈래/, 1], ["road", /길|이정표|팻말|골목|거리$/, 1], ["stairs", /계단|사다리|발판/, 1], ["bridge", /징검|다리|디딤돌/, 1],
  ["mountain", /(?<!산)산(?!가지|길|판)|봉우리|태산|여산|태항산|남산|초산|먼 산|높은 산/, 1], ["hill", /언덕|둑|벼랑|절벽|골짜기|비탈|두렁|두둑/, 1],
  ["sea", /바다|파도|물보라|회오리/, 1], ["fall", /폭포/, 1], ["river", /강|냇물|시내|물길|황하|여울|물가|물결|시냇물|샘물|샘$|못$|연못|늪|개울|호수|물줄기|^물$|웅덩이/, 1],
  ["cloud", /구름/, 1], ["rain", /비바람|봄비|빗방울|빗줄기|^비$|비와|우레/, 1], ["snow", /눈$|눈송이|서리|이슬|얼음/, 1], ["wind", /바람/, 1], ["moonsky", /^달$|달빛/, 1], ["sunsky", /^해$|해그림자/, 1],
  ["willow", /버들|버드나무/, 1], ["bamboo", /대나무|대숲/, 1], ["pine", /소나무|잣나무|솔/, 1], ["plum", /매화|복사꽃|꽃나무/, 1], ["tree", /나무$|높은 나무|큰 나무|숲|뽕나무|오동|나무(?!껍질|뿌리)/, 1],
  ["house", /초가|집|처마|지붕|정자|향교|서당|누각|서재|책방|절$|곳간|마을|저잣거리|공방|마구간|탑$|악양루|새 도읍|고요한 방/, 1], ["palace", /궁|기와/, 1], ["wall", /성벽|성문|성$|담장|담$|벽$|관문|대문|사립문|울타리|문$|성터|새 성/, 1], ["camp", /진영|장막|군막|막사|큰 군대|군사/, 1],
  ["field", /밭|들판|논|벌판|들길|고랑|월나라 들판|넓은 들/, 1], ["rocks", /바위|돌$|돌무더기|너럭바위|돌탑|동굴|굴$|굴 셋|무덤/, 1], ["reeds", /갈대|풀숲|강아지풀|마름풀|도꼬마리|풀$/, 1],
  ["flowers", /꽃|국화|난초|철쭉|유채|지초|쑥|이끼/, 1], ["sprout", /싹|묘목|어린 모|^모$|시든 모|화분|어린나무|새싹/, 0], ["roots", /뿌리|덩굴|오이/, 0], ["grain", /볏단|곡식|이삭|벼|돌피|콩/, 0],
  ["desk", /서안|책상|탁자|소반|밥상/, 0], ["bookpile", /책 더미|책 상자|쌓인 책|책보|책 보따리|책 꾸러미|죽간 더미|옛 책 더미|외운 죽간|두툼한 책/, 0],
  ["book", /책|논어|효경|경전|시집|법전|병법서|『|문집|근사록|삼자경|춘추/, 0], ["scroll", /두루마리|죽간|지도|기록|상소문|간언|그림$|뱀 그림/, 0],
  ["paper", /종이|공책|편지|쪽지|화폭|서판|칠판|본보기|풀이|고친|글$|글자|글줄|말풍선|노트|달력|계획표|수첩|^식$|부적|문제/, 0], ["brush", /붓|연필/, 0], ["inkstone", /벼루|먹$/, 0],
  ["lamp", /등잔|등불|촛불|촛대|^초$|횃불|등롱|불씨|들불/, 0], ["bow", /활|쇠뇌/, 0], ["arrow", /화살/, 0], ["sword", /칼|검$/, 0], ["spear", /창$|당목/, 0], ["staff", /지팡이|장대|막대|삿대|노$|채찍/, 0],
  ["flag", /깃발|^기$|홰$|횃대/, 0], ["cart", /수레|바퀴살|바퀴/, 0], ["boat", /배$|^배|나룻배|돛/, 0], ["plow", /쟁기/, 0], ["hoe", /호미|삽|괭이|거름/, 0],
  ["basket", /삼태기|광주리|바구니|키$|흙짐|꼴짐|통발/, 0], ["axe", /도끼/, 0], ["hammer", /망치|달구/, 0], ["chisel", /끌|^정$|새김칼|대패|조각/, 0], ["whet", /숫돌/, 0],
  ["net", /그물|매듭|벼리|덫/, 0], ["rod", /낚싯대|낚싯줄/, 0], ["broom", /빗자루|싸리비/, 0], ["can", /물뿌리개|물바가지|국자|숟가락|바가지/, 0],
  ["jar", /물동이|항아리|독$|단지|호리병|병$|약사발/, 0], ["bucket", /두레박/, 0], ["bowl", /그릇|사발|대야|잔$|찻잔|술잔|접시|제기|고기|쟁반|됫박|여물통|안주|여물/, 0], ["pot", /솥|약탕관|화로|가마$|방아/, 0],
  ["zither", /거문고|가야금|^금$|^슬|금\)/, 0], ["flute", /피리|퉁소/, 0], ["drum", /북$|큰북/, 0], ["chime", /경쇠|편경|종$|종틀/, 0], ["loom", /베틀|물레/, 0],
  ["scale", /저울/, 0], ["ruler", /자$|곱자|그림쇠|먹줄|장부/, 0], ["fan", /부채/, 0], ["lens", /돋보기/, 0], ["rods", /산가지|주판|점대|젓가락/, 0], ["baduk", /바둑/, 0],
  ["hourglass", /모래시계/, 0], ["tablet", /홀$|옥홀/, 0], ["coins", /엽전|노잣돈|황금|금덩이|금$/, 0], ["jade", /옥|구슬|보석/, 0], ["mirror", /거울/, 0],
  ["firewood", /장작|땔나무|땔감|나뭇가지|자를|가지$|옹이/, 0], ["soil", /흙(?!담)|모래/, 0], ["bricks", /벽돌|성돌|석회/, 0], ["timber", /재목|통나무|기둥|말뚝|부목|들보|서까래|나무껍질/, 0],
  ["shield", /방패/, 0], ["bag", /자루|주머니|보따리|봇짐|꾸러미|짐$/, 0], ["box", /상자|함$|궤짝/, 0], ["cradle", /요람/, 0], ["herb", /약초|질경이|잎$/, 0],
  ["fruit", /복숭아|자두|열매|매실|밤$|귤|도토리|참외/, 0], ["needle", /바늘|침$/, 0], ["cloth", /옷|천$|빨래|솜|가죽|털$|머리채|자리$|돗자리|멍석|거적|도롱이|헝겊|휘장|가림막|앞자락/, 0], ["shoes", /짚신|신$/, 0],
  ["horse", /말$|말들|좋은 말|네 필|천리마|지친 말|세 쌍의 말|나귀/, 0], ["ox", /^소$|끌려가는 소|돼지/, 0], ["fowl", /^닭$/, 0], ["birdp", /^새$|새매|물수리|고니|기러기|꾀꼬리|^매$|둥지/, 0],
  ["fishp", /물고기|큰 물고기|피라미/, 0], ["butterfly", /나비/, 0], ["insect", /매미|나나니벌|반딧불이|허물/, 0], ["deerp", /사슴/, 0], ["sheepp", /^양$/, 0], ["dogp", /큰 개|^개$/, 0], ["tigerp", /^범$|호랑이/, 0], ["monkeyp", /원숭이/, 0], ["dragonp", /교룡/, 0],
];
export function propKind(name) { const n = String(name || "").replace(/\([^()]*\)/g, "").trim(); for (const [k, re, sc] of PROP) if (re.test(n)) return { kind: k, scenery: !!sc, name: n, hint: (String(name).match(/\(([^()]*)\)/) || [])[1] || "" }; return null; }

/** 땅에 놓는 소품. (x,y) = 바닥 가운데, s 크기, m 보는 쪽. 그린 폭(반)도 돌려준다 */
function prop(S, kind, x, y, s, m) {
  const p = S.p; let o = "", w = 8 * s;
  const box = (x0, y0, x1, y1, fill, op, W) => p.poly([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], fill, op) + (W ? p.line([[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]], W, null, .8) : "");
  switch (kind) {
    case "desk": o += box(x - 11 * s, y - 8 * s, x + 11 * s, y - 6.4 * s, null, .85) + p.bl([[x - 9 * s, y - 6.6 * s], [x - 9.4 * s, y]], 1.2 * s, null, .85) + p.bl([[x + 9 * s, y - 6.6 * s], [x + 9.4 * s, y]], 1.2 * s, null, .85); w = 11 * s; break;
    case "book": o += box(x - 5 * s, y - 2.6 * s, x + 5 * s, y, "paper", 1, .7 * s) + p.line([[x - 5 * s, y - 1.3 * s], [x + 5 * s, y - 1.3 * s]], .3 * s, null, .5); w = 5 * s; break;
    case "bookpile": for (let k = 0; k < 3; k++) { const ww = (5 - k * .6) * s, yy = y - k * 2.6 * s; o += box(x - ww + k * .4 * s, yy - 2.6 * s, x + ww + k * .4 * s, yy, "paper", 1, .65 * s); } w = 5 * s; break;
    case "scroll": o += box(x - 6 * s, y - 2.6 * s, x + 6 * s, y, "paper", 1, .7 * s) + p.ring(x - 6 * s, y - 1.3 * s, 1.3 * s, .5 * s) + p.ring(x + 6 * s, y - 1.3 * s, 1.3 * s, .5 * s) + p.line([[x - 1 * s, y - 2.8 * s], [x - 1 * s, y + .2 * s]], .6 * s, null, .8); w = 7 * s; break;
    case "paper": o += p.area([[x - 6 * s, y - .4 * s], [x + 5 * s, y - 1.4 * s], [x + 6 * s, y], [x - 5 * s, y + .8 * s]], "paper", 1) + p.line([[x - 6 * s, y - .4 * s], [x + 5 * s, y - 1.4 * s], [x + 6 * s, y], [x - 5 * s, y + .8 * s], [x - 6 * s, y - .4 * s]], .5 * s, null, .7); w = 6 * s; break;
    case "brush": o += p.line([[x - 6 * s, y - 1 * s], [x + 4 * s, y - 2.4 * s]], .7 * s, null, .9) + p.bl([[x + 4 * s, y - 2.4 * s], [x + 7.4 * s, y - 2.8 * s]], 1.1 * s, null, .9, [[0, 1], [1, .1]]); w = 7 * s; break;
    case "inkstone": o += box(x - 5 * s, y - 2.4 * s, x + 5 * s, y, null, .75) + p.disc(x - 2 * s, y - 2.6 * s, 1.6 * s, "paper", .4); w = 5 * s; break;
    case "lamp": { const h = 20 * s; o += p.bl([[x, y], [x, y - h]], 1.1 * s, null, .85) + box(x - 5 * s, y - 2 * s, x + 5 * s, y, null, .8) + p.area([[x - 4.4 * s, y - h], [x + 4.4 * s, y - h], [x + 2.8 * s, y - h + 2.4 * s], [x - 2.8 * s, y - h + 2.4 * s]], null, .85); o += `<path d="M${P2(x, y - h - 7 * s)}C${P2(x + 3 * s, y - h - 2 * s)} ${P2(x + 2.4 * s, y - h + .6 * s)} ${P2(x, y - h + .8 * s)}C${P2(x - 2.4 * s, y - h + .6 * s)} ${P2(x - 3 * s, y - h - 2 * s)} ${P2(x, y - h - 7 * s)}Z" ${p.fa("gold", .95)}/>` + p.disc(x, y - h - 3 * s, 9 * s, "gold", .1); w = 6 * s; break; }
    case "bow": o += p.bl(p.arc(x - 4 * s, y - 14 * s, 14 * s, rad(-60), rad(60), 8), 1.3 * s, null, .85, [[0, .3], [.5, 1], [1, .3]]) + p.line([pol(rad(-60), 14 * s).map((v, i) => v + (i ? y - 14 * s : x - 4 * s)), pol(rad(60), 14 * s).map((v, i) => v + (i ? y - 14 * s : x - 4 * s))], .35 * s, null, .8); w = 6 * s; break;
    case "arrow": for (let k = 0; k < 3; k++) o += p.line([[x - 2 * s + k * 1.6 * s, y], [x + k * 2.4 * s, y - 16 * s]], .5 * s, null, .85) + p.tick(x + k * 2.4 * s, y - 16 * s, rad(-110), 2.4 * s, .8 * s, null, .8); w = 5 * s; break;
    case "sword": o += p.line([[x - 9 * s, y - 1 * s], [x + 7 * s, y - 1.6 * s]], 1.1 * s, null, .9) + p.line([[x - 6 * s, y - 3 * s], [x - 6 * s, y + .8 * s]], .9 * s, null, .9); w = 9 * s; break;
    case "spear": case "staff": o += p.line([[x - 2 * s, y], [x + 2 * s, y - 34 * s]], .8 * s, null, .85) + (kind === "spear" ? p.area([[x + 2 * s, y - 34 * s], [x + 3.4 * s, y - 39 * s], [x + 1 * s, y - 34 * s]], null, .9) : ""); w = 3 * s; break;
    case "flag": { const h = 44 * s; o += p.bl([[x, y], [x + 1 * s, y - h]], 1 * s, null, .85, EVEN); const fl = [[x + 1 * s, y - h], [x + m * 16 * s, y - h + 2 * s], [x + m * 13 * s, y - h + 7 * s], [x + m * 17 * s, y - h + 12 * s], [x + 1 * s, y - h + 11 * s]]; o += p.area(fl, null, .7) + p.bl(fl.slice(0, 4), .6 * s, null, .8, EVEN); w = 10 * s; break; }
    case "cart": { const r = 8 * s; o += p.area([[x - 13 * s, y - r - 7 * s], [x + 9 * s, y - r - 7 * s], [x + 9 * s, y - r + 1 * s], [x - 13 * s, y - r + 1 * s]], "paper", 1) + p.line([[x - 13 * s, y - r - 7 * s], [x + 9 * s, y - r - 7 * s], [x + 9 * s, y - r + 1 * s], [x - 13 * s, y - r + 1 * s], [x - 13 * s, y - r - 7 * s]], .9 * s, null, .8); o += p.bl([[x + 9 * s, y - r - 2 * s], [x + m * 26 * s, y - r - 4 * s]], .9 * s, null, .8); o += p.ring(x - 3 * s, y - r, r, 1.4 * s, null, .85); for (let u = 0; u < 8; u++) { const a = u / 8 * 2 * PI; o += p.line([[x - 3 * s, y - r], [x - 3 * s + Math.cos(a) * r, y - r + Math.sin(a) * r]], .4 * s, null, .6); } w = 14 * s; break; }
    case "boat": { const hull = [[x - 22 * s, y - 5 * s], [x - 12 * s, y - 1 * s], [x + 12 * s, y - 1 * s], [x + 22 * s, y - 6 * s], [x + 16 * s, y + 5 * s], [x - 16 * s, y + 6 * s]]; o += p.area(hull, null, .78) + p.bl([[x - 22 * s, y - 5 * s], [x, y - .6 * s], [x + 22 * s, y - 6 * s]], 1.1 * s, null, .9); w = 22 * s; break; }
    case "plow": o += p.bl([[x - 6 * s, y - 14 * s], [x + 2 * s, y - 2 * s], [x + 10 * s, y]], 1.2 * s, null, .85) + p.area([[x + 6 * s, y - 2 * s], [x + 13 * s, y], [x + 6 * s, y + .6 * s]], null, .9); w = 10 * s; break;
    case "hoe": o += p.line([[x - 6 * s, y - 14 * s], [x + 4 * s, y - 1 * s]], .8 * s, null, .85) + p.area([[x + 3 * s, y - 3 * s], [x + 7 * s, y - 1 * s], [x + 3 * s, y]], null, .9); w = 6 * s; break;
    case "basket": o += p.area([[x - 6 * s, y - 6 * s], [x + 6 * s, y - 6 * s], [x + 4 * s, y], [x - 4 * s, y]], "paper", 1) + p.line([[x - 6 * s, y - 6 * s], [x - 4 * s, y], [x + 4 * s, y], [x + 6 * s, y - 6 * s]], .8 * s, null, .8) + p.line([[x - 5 * s, y - 3 * s], [x + 5 * s, y - 3 * s]], .35 * s, null, .5) + p.area(p.blob(x, y - 6.5 * s, 5 * s, 2 * s, 0, .2), null, .55); w = 6 * s; break;
    case "axe": o += p.line([[x - 6 * s, y - .6 * s], [x + 6 * s, y - 1.6 * s]], .9 * s, null, .85) + p.area([[x + 4 * s, y - 4 * s], [x + 7.4 * s, y - 3.6 * s], [x + 7 * s, y + .4 * s], [x + 4.4 * s, y]], null, .9); w = 7 * s; break;
    case "hammer": o += p.line([[x - 5 * s, y - .6 * s], [x + 4 * s, y - 1.4 * s]], .8 * s, null, .85) + box(x + 3 * s, y - 3.4 * s, x + 6 * s, y + .4 * s, null, .9); w = 6 * s; break;
    case "chisel": o += p.line([[x - 4 * s, y - .6 * s], [x + 4 * s, y - 1 * s]], .9 * s, null, .9) + p.line([[x + 4 * s, y - 1 * s], [x + 6.6 * s, y - 1.1 * s]], .5 * s, null, .9); w = 6 * s; break;
    case "whet": o += box(x - 7 * s, y - 3.4 * s, x + 7 * s, y, null, .55) + p.line([[x - 7 * s, y - 3.4 * s], [x + 7 * s, y - 3.4 * s]], .7 * s, null, .9); w = 7 * s; break;
    case "net": for (let k = 0; k < 5; k++) o += p.line([[x - 10 * s + k * 5 * s, y], [x - 8 * s + k * 4 * s, y - 14 * s]], .35 * s, null, .55) + p.line([[x - 10 * s, y - k * 3.4 * s], [x + 10 * s, y - k * 3.4 * s - 1 * s]], .35 * s, null, .55); o += p.line([[x - 8 * s, y - 14 * s], [x + 8 * s, y - 15 * s]], .9 * s, null, .8); w = 10 * s; break;
    case "rod": o += p.line([[x - 4 * s, y], [x + m * 26 * s, y - 26 * s]], .5 * s, null, .8) + p.line([[x + m * 26 * s, y - 26 * s], [x + m * 28 * s, y - 4 * s]], .25 * s, null, .6); w = 6 * s; break;
    case "broom": o += p.line([[x - 1 * s, y - 24 * s], [x + 1 * s, y - 6 * s]], .8 * s, null, .85) + p.area([[x - 1 * s, y - 7 * s], [x + 2 * s, y - 7 * s], [x + 5 * s, y], [x - 4 * s, y]], null, .7); w = 5 * s; break;
    case "can": o += p.area([[x - 4 * s, y - 7 * s], [x + 4 * s, y - 7 * s], [x + 4 * s, y], [x - 4 * s, y]], "paper", 1) + p.line([[x - 4 * s, y - 7 * s], [x - 4 * s, y], [x + 4 * s, y], [x + 4 * s, y - 7 * s]], .8 * s, null, .8) + p.line([[x + 4 * s, y - 3 * s], [x + 10 * s, y - 8 * s]], .7 * s, null, .8); w = 6 * s; break;
    case "jar": case "pot": case "bucket": { const pts = kind === "pot" ? [[x - 7 * s, y - 8 * s], [x + 7 * s, y - 8 * s], [x + 6 * s, y - 2 * s], [x - 6 * s, y - 2 * s]] : [[x - 3 * s, y - 11 * s], [x + 3 * s, y - 11 * s], [x + 6 * s, y - 6 * s], [x + 4 * s, y], [x - 4 * s, y], [x - 6 * s, y - 6 * s]]; o += p.shape(pts, kind === "jar" ? null : "paper", kind === "jar" ? .25 : 1, .7 * s); if (kind === "pot") o += [-1, 1].map((k) => p.line([[x + k * 4 * s, y - 2 * s], [x + k * 5 * s, y]], .8 * s, null, .8)).join(""); if (kind === "bucket") o += p.line([[x - 3 * s, y - 11 * s], [x, y - 16 * s], [x + 3 * s, y - 11 * s]], .5 * s, null, .7) + p.line([[x, y - 16 * s], [x, y - 30 * s]], .4 * s, null, .6); w = 6 * s; break; }
    case "bowl": o += p.area([[x - 5 * s, y - 4 * s], [x + 5 * s, y - 4 * s], [x + 3 * s, y], [x - 3 * s, y]], "paper", 1) + p.bl([[x - 5 * s, y - 4 * s], [x - 3 * s, y], [x + 3 * s, y], [x + 5 * s, y - 4 * s]], .8 * s, null, .85) + p.line([[x - 5 * s, y - 4 * s], [x + 5 * s, y - 4 * s]], .6 * s, null, .8); w = 5 * s; break;
    case "zither": o += p.area([[x - 16 * s, y - 3.4 * s], [x + 16 * s, y - 4.4 * s], [x + 16 * s, y - 1.6 * s], [x - 16 * s, y - .6 * s]], null, .75) + [1, 2, 3].map((k) => p.line([[x - 14 * s, y - 2.6 * s - k * .5 * s], [x + 14 * s, y - 3.4 * s - k * .5 * s]], .2 * s, "paper", .7)).join("") + p.line([[x - 14 * s, y - .6 * s], [x - 14 * s, y + .2 * s]], .8 * s) + p.line([[x + 14 * s, y - 1.6 * s], [x + 14 * s, y + .2 * s]], .8 * s); w = 16 * s; break;
    case "flute": o += p.line([[x - 6 * s, y - .8 * s], [x + 6 * s, y - 1.4 * s]], .9 * s, null, .85); w = 6 * s; break;
    case "drum": o += p.area(p.blob(x, y - 10 * s, 6 * s, 6 * s, 0, .05), "paper", 1) + p.ring(x, y - 10 * s, 6 * s, 1.3 * s, null, .85) + p.line([[x - 4 * s, y - 5 * s], [x - 6 * s, y]], .9 * s) + p.line([[x + 4 * s, y - 5 * s], [x + 6 * s, y]], .9 * s); w = 7 * s; break;
    case "chime": o += p.bl([[x - 9 * s, y - 22 * s], [x + 9 * s, y - 22 * s]], 1.2 * s, null, .85) + p.line([[x - 8 * s, y - 22 * s], [x - 8 * s, y]], .9 * s, null, .85) + p.line([[x + 8 * s, y - 22 * s], [x + 8 * s, y]], .9 * s, null, .85) + [-1, 1].map((k) => p.line([[x + k * 3 * s, y - 22 * s], [x + k * 3 * s, y - 18 * s]], .3 * s) + p.area([[x + k * 3 * s - 3 * s, y - 18 * s], [x + k * 3 * s, y - 19 * s], [x + k * 3 * s + 2 * s, y - 14 * s]], null, .8)).join(""); w = 9 * s; break;
    case "loom": o += p.bl([[x - 9 * s, y], [x - 9 * s, y - 20 * s]], 1.2 * s, null, .85) + p.bl([[x + 9 * s, y], [x + 9 * s, y - 20 * s]], 1.2 * s, null, .85) + p.bl([[x - 10 * s, y - 20 * s], [x + 10 * s, y - 20 * s]], 1.2 * s, null, .85) + p.bl([[x - 10 * s, y - 8 * s], [x + 10 * s, y - 8 * s]], 1 * s, null, .75); for (let k = -3; k <= 3; k++) o += p.line([[x + k * 2.2 * s, y - 20 * s], [x + k * 2.2 * s, y - 8 * s]], .25 * s, null, .5); w = 10 * s; break;
    case "scale": o += p.line([[x, y], [x, y - 20 * s]], .9 * s, null, .85) + p.bl([[x - 10 * s, y - 18 * s], [x + 10 * s, y - 19 * s]], .9 * s, null, .85) + [-1, 1].map((k) => p.line([[x + k * 9 * s, y - 18.5 * s], [x + k * 9 * s, y - 10 * s]], .3 * s) + p.area([[x + k * 9 * s - 3.4 * s, y - 10 * s], [x + k * 9 * s + 3.4 * s, y - 10 * s], [x + k * 9 * s + 2 * s, y - 8 * s], [x + k * 9 * s - 2 * s, y - 8 * s]], null, .8)).join(""); w = 10 * s; break;
    case "coins": for (let k = 0; k < 3; k++) o += p.disc(x - 3 * s + k * 3 * s, y - 1.6 * s - (k % 2) * 1.6 * s, 2 * s, "gold", .7, .5 * s); w = 5 * s; break;
    case "jade": o += p.disc(x, y - 3 * s, 3 * s, "paper", 1, .7 * s) + p.disc(x, y - 3 * s, 1 * s, null, .3); w = 3 * s; break;
    case "mirror": o += p.disc(x, y - 9 * s, 5 * s, "paper", 1, 1 * s) + p.line([[x, y - 4 * s], [x, y]], 1.2 * s, null, .8); w = 5 * s; break;
    case "firewood": for (let k = 0; k < 5; k++) o += p.bl([[x - 8 * s, y - k * 1.6 * s - .8 * s], [x + 8 * s, y - k * 1.6 * s - 1.4 * s]], 1.1 * s, null, .75, EVEN); w = 8 * s; break;
    case "soil": o += p.area([[x - 9 * s, y], [x - 4 * s, y - 4 * s], [x + 1 * s, y - 6 * s], [x + 6 * s, y - 3.4 * s], [x + 9 * s, y]], null, .3) + p.bl([[x - 9 * s, y], [x - 4 * s, y - 4 * s], [x + 1 * s, y - 6 * s], [x + 6 * s, y - 3.4 * s], [x + 9 * s, y]], .7 * s, null, .6, SOFT); w = 9 * s; break;
    case "bricks": for (let k = 0; k < 3; k++) for (let j = 0; j < 3 - k; j++) o += box(x - 9 * s + j * 6 * s + k * 3 * s, y - (k + 1) * 3 * s, x - 3.6 * s + j * 6 * s + k * 3 * s, y - k * 3 * s, "paper", 1, .5 * s); w = 9 * s; break;
    case "timber": for (let k = 0; k < 3; k++) { const yy = y - 2 * s - k * 3.4 * s; o += box(x - 10 * s + k * 1.4 * s, yy - 1.6 * s, x + 10 * s - k * 1.4 * s, yy + 1.6 * s, "paper", 1, .55 * s) + p.ring(x + 10 * s - k * 1.4 * s, yy, 1.6 * s, .4 * s); } w = 10 * s; break;
    case "shield": o += p.disc(x, y - 8 * s, 7 * s, "paper", 1, 1.2 * s) + p.dot(x, y - 8 * s, 1.4 * s); w = 7 * s; break;
    case "bag": case "cloth": o += p.shape([[x - 6 * s, y], [x - 6 * s, y - 5 * s], [x - 2 * s, y - 8 * s], [x + 3 * s, y - 8 * s], [x + 6 * s, y - 4 * s], [x + 6 * s, y]], "paper", 1, .7 * s) + p.line([[x - 2 * s, y - 8 * s], [x, y - 10 * s], [x + 3 * s, y - 8 * s]], .5 * s, null, .8); w = 6 * s; break;
    case "box": o += box(x - 7 * s, y - 7 * s, x + 7 * s, y, "paper", 1, .8 * s) + p.line([[x - 7 * s, y - 5 * s], [x + 7 * s, y - 5 * s]], .5 * s, null, .7); w = 7 * s; break;
    case "cradle": o += p.area([[x - 8 * s, y - 6 * s], [x + 8 * s, y - 6 * s], [x + 6 * s, y - 1 * s], [x - 6 * s, y - 1 * s]], "paper", 1) + p.bl(p.arc(x, y - 6 * s, 8 * s, 0, PI, 8), .9 * s, null, .8) + p.disc(x + 3 * s, y - 7 * s, 2 * s, "paper", 1, .5 * s); w = 8 * s; break;
    case "sprout": case "herb": case "grain": case "roots": case "flowers": case "reeds": {
      const n = kind === "grain" ? 1 : 3;
      for (let k = 0; k < n; k++) { const bx = x + (k - (n - 1) / 2) * 6 * s; if (kind === "grain") { for (let j = -3; j <= 3; j++) o += p.line([[bx + j * .8 * s, y], [bx + j * .5 * s, y - 16 * s], [bx + j * 1.4 * s + 1.6 * s, y - 20 * s]], .45 * s, null, .75); o += p.line([[bx - 3 * s, y - 8 * s], [bx + 3 * s, y - 8 * s]], .9 * s, null, .8); } else if (kind === "reeds") { o += p.bl([[bx, y], [bx + 2 * s, y - 22 * s]], .5 * s, null, .7) + p.leaf(bx + 2 * s, y - 22 * s, rad(-70), 5 * s, 1.2 * s, null, .6) + p.leaf(bx, y - 6 * s, rad(-40), 9 * s, .9 * s, null, .5); } else if (kind === "roots") { o += p.bl([[bx, y - 6 * s], [bx, y]], .9 * s, null, .8); for (let j = -1; j <= 1; j++) o += p.line([[bx, y], [bx + j * 3 * s, y + 4 * s], [bx + j * 5 * s, y + 6 * s]], .4 * s, null, .6); o += p.leaf(bx, y - 6 * s, rad(-130), 5 * s, 1.2 * s, null, .7) + p.leaf(bx, y - 6 * s, rad(-50), 5 * s, 1.2 * s, null, .7); } else { const h = (kind === "flowers" ? 12 : 7) * s; o += p.bl([[bx, y], [bx + .6 * s, y - h]], .5 * s, null, .8) + p.leaf(bx, y - h * .5, rad(-140), 5 * s, 1.3 * s, null, .65) + p.leaf(bx, y - h * .4, rad(-40), 5 * s, 1.3 * s, null, .65); if (kind === "flowers") o += p.disc(bx + .6 * s, y - h, 2 * s, "paper", 1, .5 * s) + p.dot(bx + .6 * s, y - h, .7 * s, null, .8); } }
      w = (n * 3 + 3) * s; break;
    }
    case "fruit": for (let k = 0; k < 3; k++) o += p.disc(x - 3 * s + k * 3 * s, y - 2 * s - (k % 2) * 2 * s, 2 * s, "paper", 1, .6 * s); o += p.line([[x - 6 * s, y], [x + 6 * s, y]], .6 * s, null, .6); w = 6 * s; break;
    case "tablet": case "ruler": case "fan": case "needle": case "eraser": case "rods": case "hourglass": case "lens": case "shoes": case "baduk": {
      if (kind === "baduk") { o += box(x - 9 * s, y - 4 * s, x + 9 * s, y, null, .7); for (let k = 0; k < 4; k++) o += p.dot(x - 6 * s + k * 4 * s, y - 5 * s, 1.2 * s, k % 2 ? "paper" : null, 1); w = 9 * s; break; }
      if (kind === "rods") { for (let k = 0; k < 6; k++) o += p.line([[x - 6 * s + k * 2 * s, y], [x - 4 * s + k * 2 * s, y - 2 * s]], .35 * s, null, .8); o += p.line([[x - 7 * s, y - .6 * s], [x + 7 * s, y - 1 * s]], .35 * s, null, .8); w = 7 * s; break; }
      if (kind === "hourglass") { o += p.area([[x - 4 * s, y - 12 * s], [x + 4 * s, y - 12 * s], [x, y - 6 * s], [x + 4 * s, y], [x - 4 * s, y], [x, y - 6 * s]], "paper", 1) + p.line([[x - 4 * s, y - 12 * s], [x + 4 * s, y - 12 * s], [x - 4 * s, y], [x + 4 * s, y], [x - 4 * s, y - 12 * s]], .6 * s, null, .8); w = 4 * s; break; }
      if (kind === "lens") { o += p.ring(x + 2 * s, y - 6 * s, 3.6 * s, .8 * s) + p.line([[x - 1 * s, y - 3 * s], [x - 5 * s, y]], 1 * s); w = 5 * s; break; }
      if (kind === "fan") { o += p.area([[x, y], [x - 8 * s, y - 10 * s], [x + 8 * s, y - 10 * s]], "paper", 1) + p.bl(p.arc(x, y, 12.8 * s, rad(-129), rad(-51), 6), .7 * s, null, .8) + p.line([[x - 8 * s, y - 10 * s], [x, y], [x + 8 * s, y - 10 * s]], .5 * s, null, .7); w = 8 * s; break; }
      o += p.line([[x - 5 * s, y - .6 * s], [x + 5 * s, y - 1.2 * s]], 1 * s, null, .8); w = 5 * s; break;
    }
    case "horse": case "ox": case "fowl": case "birdp": case "fishp": case "butterfly": case "insect": case "deerp": case "sheepp": case "dogp": case "tigerp": case "monkeyp": case "dragonp": {
      const k = { horse: "horse", ox: "ox", fowl: "rooster", birdp: "bird", fishp: "fish", butterfly: "butterfly", insect: "cicada", deerp: "deer", sheepp: "sheep", dogp: "dog", tigerp: "tiger", monkeyp: "monkey", dragonp: "turtle" }[kind];
      const sz = ["horse", "ox", "deer"].includes(k) ? 1.2 * s : ["butterfly", "cicada", "fish", "bird"].includes(k) ? 1 * s : 1.1 * s;
      o += animal(p, k, "stand", x, ["butterfly", "cicada", "bird"].includes(k) ? y - 14 * s : y, sz, m < 0).svg; w = ["horse", "ox"].includes(k) ? 16 * s : 8 * s; break;
    }
    default: return null;
  }
  return { svg: o, w };
}

/* ───────────── 손에 든 것 · 자세가 부르는 것 ───────────── */
const POSE_TOOL = {
  read: ["book", "scroll", "paper"], write: ["brush"], shoot: ["bow"], cut: ["axe", "sword"], carve: ["hammer", "chisel"], dig: ["hoe"], plow: ["plow"],
  sweep: ["broom"], sprinkle: ["can", "jar", "bucket", "bowl"], pour: ["jar", "can", "bowl", "bucket"], cup: ["bowl"], fish: ["rod", "net"], pole: ["staff"],
  hold: ["book", "scroll", "jade", "bowl", "jar", "fruit", "bag", "tablet", "mirror", "coins", "spear", "flag", "staff", "sword", "shield", "cradle", "paper", "fan", "lamp", "bricks", "box", "herb", "grain"],
  hug: ["jade", "cradle", "book", "bag", "box", "fruit"], offer: ["bowl", "book", "scroll", "fruit", "herb", "jade", "coins", "paper", "box", "tablet"],
  walk: ["staff", "flag", "lamp", "sword"], stand: ["staff", "sword", "tablet", "fan", "flag", "scroll", "book"], gaze: ["staff"], guide: ["staff", "lamp"],
  carry: ["basket", "bag", "bookpile", "soil", "bricks", "firewood", "jar", "box", "timber", "grain"], carryload: ["bag", "bookpile", "box", "bricks", "basket", "firewood", "jar", "soil", "timber", "cloth"],
  play: ["zither", "flute", "drum", "chime"], count: ["rods", "baduk", "coins", "scale", "basket"], grind: ["whet", "inkstone", "herb"], wash: ["bowl", "jar", "pot"],
  climb: [], dance: ["sword", "fan"], throw: [], run: ["flag"], chase: [], think: [], sit: ["fan"], point: [], bow: ["tablet"], kneel: ["bowl", "book"], crouch: [], pull: ["sprout", "grain"],
};
/** 손에 든 것을 그린다. hd 손, m 보는 쪽, s 크기 */
function held(S, kind, fg, s) {
  const p = S.p, [hx, hy] = fg.hand, m = fg.m;
  switch (kind) {
    case "book": case "paper": return p.area([[hx - m * 1 * s, hy - 3 * s], [hx - m * 9 * s, hy - 1.6 * s], [hx - m * 9 * s, hy + 2.2 * s], [hx - m * 1 * s, hy + 1 * s]], "paper", 1) + p.line([[hx - m * 1 * s, hy - 3 * s], [hx - m * 9 * s, hy - 1.6 * s], [hx - m * 9 * s, hy + 2.2 * s], [hx - m * 1 * s, hy + 1 * s], [hx - m * 1 * s, hy - 3 * s]], .5 * s, null, .9) + p.line([[hx - m * 5 * s, hy - 2.4 * s], [hx - m * 5 * s, hy + 1.6 * s]], .3 * s, null, .6);
    case "scroll": return p.area([[hx - m * 1 * s, hy - 4 * s], [hx + m * 7 * s, hy - 3 * s], [hx + m * 7 * s, hy + 2 * s], [hx - m * 1 * s, hy + 1 * s]], "paper", 1) + p.line([[hx - m * 1 * s, hy - 4 * s], [hx - m * 1 * s, hy + 1 * s]], 1 * s) + p.line([[hx + m * 7 * s, hy - 3 * s], [hx + m * 7 * s, hy + 2 * s]], 1 * s) + [0, 1, 2].map((k) => p.line([[hx + m * (1.4 + k * 1.8) * s, hy - 2.4 * s], [hx + m * (1.4 + k * 1.8) * s, hy + .6 * s]], .25 * s, null, .6)).join("");
    case "brush": return p.line([[hx, hy - 7 * s], [hx + m * .6 * s, hy + .6 * s]], .55 * s, null, .9) + p.bl([[hx + m * .6 * s, hy + .2 * s], [hx + m * .8 * s, hy + 2.4 * s]], .9 * s, null, .9, [[0, 1], [1, .1]]);
    case "bow": { const [fx, fy] = fg.fhand, [dx, dy] = fg.hand, top = [fx - m * 2 * s, fy - 13 * s], bot = [fx - m * 2 * s, fy + 13 * s]; return p.bl([top, [fx + m * 2.6 * s, fy], bot], 1.2 * s, null, .9, [[0, .3], [.5, 1], [1, .3]]) + p.line([top, [dx, dy], bot], .3 * s, null, .85) + p.line([[dx, dy], [fx + m * 9 * s, fy - .4 * s]], .45 * s, null, .9) + p.area([[fx + m * 9 * s, fy - 1.4 * s], [fx + m * 12 * s, fy - .4 * s], [fx + m * 9 * s, fy + .6 * s]], null, .9); }
    case "axe": return p.line([[hx - m * 2 * s, hy + 3 * s], [hx + m * 4 * s, hy - 9 * s]], .9 * s, null, .9) + p.area([[hx + m * 2 * s, hy - 11 * s], [hx + m * 7 * s, hy - 12 * s], [hx + m * 7 * s, hy - 7 * s], [hx + m * 3.4 * s, hy - 7.6 * s]], null, .9);
    case "sword": return p.line([[hx - m * 1 * s, hy + 2 * s], [hx + m * 12 * s, hy - 8 * s]], .9 * s, null, .9) + p.line([[hx - m * .6 * s, hy - 1.6 * s], [hx + m * 1.6 * s, hy + 1.2 * s]], .9 * s, null, .9);
    case "hammer": return p.line([[hx, hy + 1 * s], [hx - m * 2 * s, hy - 6 * s]], .8 * s, null, .9) + p.area([[hx - m * 4.6 * s, hy - 8.6 * s], [hx + m * .6 * s, hy - 7 * s], [hx - m * .2 * s, hy - 4.6 * s], [hx - m * 5.4 * s, hy - 6.2 * s]], null, .9);
    case "chisel": return p.line([[hx - m * 1 * s, hy - 3 * s], [hx + m * 2 * s, hy + 4 * s]], .8 * s, null, .9);
    case "hoe": return p.bl([[hx - m * 3 * s, hy - 6 * s], [hx + m * 6 * s, hy + 12 * s]], .8 * s, null, .9) + p.area([[hx + m * 5 * s, hy + 11 * s], [hx + m * 9.4 * s, hy + 12.4 * s], [hx + m * 7 * s, hy + 14.6 * s]], null, .9);
    case "plow": return p.bl([[hx, hy], [hx + m * 8 * s, hy + 12 * s], [hx + m * 18 * s, hy + 15 * s]], 1.1 * s, null, .85) + p.area([[hx + m * 14 * s, hy + 13 * s], [hx + m * 21 * s, hy + 15.4 * s], [hx + m * 14 * s, hy + 16 * s]], null, .9);
    case "broom": return p.line([[hx - m * 4 * s, hy - 10 * s], [hx + m * 6 * s, hy + 12 * s]], .8 * s, null, .85) + p.area([[hx + m * 4.6 * s, hy + 10 * s], [hx + m * 7.6 * s, hy + 10.6 * s], [hx + m * 11 * s, hy + 16 * s], [hx + m * 2.6 * s, hy + 16 * s]], null, .7);
    case "can": case "jar": case "bucket": case "bowl": {
      const o = p.shape([[hx - 2.6 * s, hy - 1 * s], [hx + 2.6 * s, hy - 1 * s], [hx + 3.4 * s, hy + 3 * s], [hx + 2 * s, hy + 5 * s], [hx - 2 * s, hy + 5 * s], [hx - 3.4 * s, hy + 3 * s]], kind === "jar" ? null : "paper", kind === "jar" ? .3 : 1, .5 * s);
      if (S.pose === "sprinkle" || S.pose === "pour") { let d = ""; for (let k = 0; k < 4; k++) d += p.dot(hx + m * (4 + k * 1.6) * s, hy + (5 + k * 3.4) * s, .55 * s, null, .6); return o + d; }
      return o;
    }
    case "rod": return p.line([[hx, hy], [hx + m * 34 * s, hy - 22 * s]], .45 * s, null, .85) + p.line([[hx + m * 34 * s, hy - 22 * s], [hx + m * 36 * s, hy + (S.gy - hy) / 1 + 8]], .22, null, .6);
    case "staff": case "spear": return p.line([[hx + m * 1.4 * s, hy - 12 * s], [hx - m * .6 * s, hy + (S.ground - hy)]], .7 * s, null, .9) + (kind === "spear" ? p.area([[hx + m * 1.4 * s, hy - 12 * s], [hx + m * 2.4 * s, hy - 17 * s], [hx + m * .4 * s, hy - 12 * s]], null, .9) : "");
    case "flag": { const top = [hx + m * 1 * s, hy - 22 * s]; const fl = [top, [top[0] + m * 13 * s, top[1] + 2 * s], [top[0] + m * 10 * s, top[1] + 6 * s], [top[0] + m * 14 * s, top[1] + 10 * s], [top[0], top[1] + 9 * s]]; return p.line([top, [hx - m * .6 * s, S.ground]], .7 * s, null, .9) + p.area(fl, null, .7); }
    case "lamp": return p.line([[hx, hy], [hx, hy + 4 * s]], .4 * s) + p.area(p.blob(hx, hy + 7 * s, 2.6 * s, 3.4 * s, 0, .1), "gold", .8) + p.ring(hx, hy + 7 * s, 3 * s, .5 * s) + p.disc(hx, hy + 7 * s, 7 * s, "gold", .1);
    case "zither": return "";
    case "flute": return p.line([[fg.head[0] + m * fg.hr * .6, fg.head[1] + fg.hr * .5], [hx + m * 4 * s, hy + 1 * s]], .8 * s, null, .9);
    case "drum": return p.line([[hx, hy], [hx + m * 4 * s, hy - 5 * s]], .7 * s, null, .9);
    case "jade": case "coins": case "fruit": return p.disc(hx + m * 1 * s, hy - 1.6 * s, 2.6 * s, kind === "coins" ? "gold" : "paper", kind === "coins" ? .75 : 1, .6 * s);
    case "tablet": return p.line([[hx, hy + 2 * s], [hx + m * 1.6 * s, hy - 9 * s]], 1.3 * s, null, .85);
    case "fan": return p.area([[hx, hy], [hx + m * 6 * s, hy - 8 * s], [hx + m * 10 * s, hy - 3 * s]], "paper", 1) + p.line([[hx, hy], [hx + m * 6 * s, hy - 8 * s], [hx + m * 10 * s, hy - 3 * s], [hx, hy]], .45 * s, null, .8);
    default: { const r = prop(S, kind, hx + m * 2 * s, hy + 3 * s, s * .55, m); return r ? r.svg : ""; }
  }
}

/* ───────────── 늘어나는 표시(grows) — 유형 색은 여기에만 ───────────── */
const GROW = [
  ["arrow", /화살/], ["foot", /발자국|걸음|디딘|밟아|따라간|돌아온|건너간/], ["step", /계단|층$|발판|디딤|징검|올라선|오른 계단|한 칸/],
  ["ray", /빛|햇살|밝|등불 둘레|이치|깨친|깨달|떠오른/], ["page", /책장|넘긴|베껴|읽은|외운|죽간|쌓인 책|쌓은 책|장$/], ["char", /글자|글줄|글$|구절|문제|풀이|적은|쓴|받아 적|설명한|간추린|물음|답$|말$|줄$/],
  ["ripple", /물결|결$|소리|울림|가락|숨|울음|노랫|파문|물줄기|기운/], ["drop", /물방울|빗방울|방울|땀|이슬|물 잔|물바가지|기름|적신/],
  ["flower", /꽃/], ["grain", /이삭|볏단|곡식|열매|과일|밤$|과일|모은 볏단/], ["leaf", /잎|가지|뿌리|덩굴|싹|나무|마디/],
  ["stone", /돌|벽돌|성돌|흙|삼태기|흙알/], ["star", /별/], ["cloud", /구름/], ["feather", /깃털|깃$|날갯짓|새끼 새|깃/],
  ["thread", /실$|매듭|그물코|끈|실/], ["post", /말뚝|기둥|깃발|망루|이정표/], ["bowl", /그릇|두레박|항아리|잔$/],
  ["person", /사람|벗|스승|아이 수|병사|제자|무리|친구|천리마/], ["furrow", /고랑|이랑|밭/], ["wheel", /바퀴/], ["coin", /엽전|돈|기름/],
  ["tick", /눈금|표시|점$|날$|하루|별점|지킨|약속|횟수|자리|날의|칸/],
];
const ON_GROUND = new Set(["foot", "step", "stone", "post", "person", "furrow", "grain", "flower"]);
function growMarks(S, figs) {
  const { p, R, gy, N, ACC } = S, text = String(S.e.scene?.grows || "").replace(/\([^()]*\)/g, "");
  let kind = "dot"; for (const [k, re] of GROW) if (re.test(text)) { kind = k; break; }
  const n = clamp(Math.round(N), 1, 12), c = ACC, rs = p.rs;
  let o = "";
  const mk = (x, y, a, u) => {
    switch (kind) {
      case "arrow": return p.line([[x + Math.cos(a) * 9, y + Math.sin(a) * 9], [x - Math.cos(a) * 3, y - Math.sin(a) * 3]], .7, c, .95) + p.tick(x + Math.cos(a) * 9, y + Math.sin(a) * 9, a + .5, 2.6, .8, c, .9) + p.tick(x + Math.cos(a) * 9, y + Math.sin(a) * 9, a - .5, 2.6, .8, c, .9);
      case "ray": return p.bl([[x - Math.cos(a) * 3, y - Math.sin(a) * 3], [x + Math.cos(a) * 6, y + Math.sin(a) * 6]], 1.1, c, .85, TAPER);
      case "page": return p.poly([[x - 4, y - 1.4], [x, y + .2], [x, y + 3], [x - 4, y + 1.6]], c, .3) + p.poly([[x + 4, y - 1.4], [x, y + .2], [x, y + 3], [x + 4, y + 1.6]], c, .3) + p.line([[x - 4, y - 1.4], [x, y + .2], [x + 4, y - 1.4]], .55, c, .9) + p.line([[x, y + .2], [x, y + 3]], .35, c, .8);
      case "char": { const s3 = 3.2; return [[[-s3, -s3], [s3, -s3]], [[0, -s3], [0, s3]], [[0, 0], [s3 * .8, 0]], [[-s3 * .6, -s3 * .1], [-s3 * .6, s3]], [[-s3 * 1.1, s3], [s3 * 1.1, s3]]].map(([a0, a1]) => p.bl([[x + a0[0], y + a0[1]], [x + a1[0], y + a1[1]]], .55, c, .9, [[0, .8], [1, .6]])).join(""); }
      case "ripple": return p.bl([[x - Math.sin(a) * 5, y + Math.cos(a) * 5], [x + Math.cos(a) * 1.4, y + Math.sin(a) * 1.4], [x + Math.sin(a) * 5, y - Math.cos(a) * 5]], .8, c, .85, SOFT);
      case "drop": return `<path d="M${P2(x, y - 3.6)}C${P2(x + 2.4, y - .4)} ${P2(x + 2, y + 2)} ${P2(x, y + 2.2)}C${P2(x - 2, y + 2)} ${P2(x - 2.4, y - .4)} ${P2(x, y - 3.6)}Z" ${p.fa(c, .85)}/>`;
      case "leaf": return p.leaf(x - Math.cos(a) * 3, y - Math.sin(a) * 3, a + (u % 2 ? .3 : -.3), 7, 1.6, c, .85);
      case "star": return p.line([[x - 2.6, y], [x + 2.6, y]], .6, c, .9) + p.line([[x, y - 2.6], [x, y + 2.6]], .6, c, .9) + p.dot(x, y, .9, c, .9);
      case "cloud": return p.bl(p.arc(x, y, 2.6, rad(180), rad(360), 5), .6, c, .9, SOFT) + p.bl(p.arc(x + 3, y + .6, 1.8, rad(200), rad(360), 4), .5, c, .9, SOFT);
      case "feather": return p.bl([[x - Math.cos(a + .6) * 3.6, y - Math.sin(a + .6) * 3.6], [x + Math.cos(a + .6) * 3.6, y + Math.sin(a + .6) * 3.6]], 1.4, c, .85, DAB);
      case "thread": return p.ring(x, y, 2.2, .6, c, .9) + p.line([[x + 2, y + 1], [x + 4, y + 3]], .5, c, .9);
      case "bowl": return p.area([[x - 3, y - 1.4], [x + 3, y - 1.4], [x + 1.8, y + 1.6], [x - 1.8, y + 1.6]], c, .8);
      case "wheel": return p.ring(x, y, 2.6, .7, c, .9) + p.line([[x - 2.6, y], [x + 2.6, y]], .35, c, .8) + p.line([[x, y - 2.6], [x, y + 2.6]], .35, c, .8);
      case "coin": return p.disc(x, y, 2.4, c, .8) + `<rect x="${f1(x - .8)}" y="${f1(y - .8)}" width="1.6" height="1.6" fill="${p.pal.paper}"/>`;
      case "tick": return p.bl([[x - Math.cos(a) * 3, y - Math.sin(a) * 3], [x + Math.cos(a) * 3, y + Math.sin(a) * 3]], .9, c, .9, EVEN);
      default: return p.dot(x, y, 1.6, c, .85);
    }
  };
  if (ON_GROUND.has(kind)) {
    // 땅 위: 원 아래 앞쪽에 한 줄(물이 있으면 원 바로 아래 땅에)
    const sp = Math.min(kind === "person" ? 10 : 8.6, (S.wet ? 2 * R + 6 : 150) / Math.max(1, n)), y0 = S.wet ? gy : gy + 14;
    const f0 = figs.find((f) => !f.w.animal) || figs[0], dir = kind === "foot" && f0 ? -(f0.m || 1) : 1;
    for (let u = 0; u < n; u++) {
      const x = (u - (n - 1) / 2) * sp * dir, y = y0 + (kind === "foot" ? (u % 2) * 2.2 : 0), side = dir;
      if (kind === "foot") o += p.area(p.blob(x, y, 2.2, 1.1, .1, .1), c, .7) + p.area(p.blob(x - side * 2.8, y + .2, .8, .7, 0, .1), c, .7);
      else if (kind === "step") o += p.area(p.blob(x, y, 3.6, 1.5, 0, .15), c, .6);
      else if (kind === "stone") o += p.area(p.blob(x, y - 2.6 - (u % 3) * .6, 3.4, 2.6, 0, .2), c, .7);
      else if (kind === "post") o += p.bl([[x, y], [x, y - 10 - (u % 2) * 2]], 1.2, c, .85, EVEN);
      else if (kind === "person") o += p.dot(x, y - 8.6, 1.5, c, .9) + p.poly([[x - 1.6, y - 6.8], [x + 1.6, y - 6.8], [x + 2.6, y], [x - 2.6, y]], c, .75);
      else if (kind === "furrow") o += p.bl([[x - 3, y + 2], [x + 3, y + 1]], .8, c, .8, SOFT) + p.leaf(x, y + 1, rad(-90), 4, .8, c, .7);
      else if (kind === "grain") { for (let j = -1; j <= 1; j++) o += p.line([[x + j, y], [x + j * .6, y - 9], [x + j * 1.4 + 1.2, y - 11]], .45, c, .85); }
      else if (kind === "flower") o += p.line([[x, y], [x, y - 7]], .45, c, .8) + p.disc(x, y - 8, 1.8, c, .75);
    }
    return o;
  }
  // 원 위쪽 둘레
  const q = R + (S.ck === "sun" ? 21 : S.ck === "lamp" ? 19 : 15), a0 = rad(-152), a1 = rad(-28);
  for (let u = 0; u < n; u++) { const a = n === 1 ? rad(-90) : a0 + (a1 - a0) * u / (n - 1), [x, y] = pol(a, q); o += mk(x, y, a, u); }
  return o;
}

/* ───────────── 장면 조립 ───────────── */
const CMOD = [["mountain", /산(?!판)|봉우리|태산|여산|석종산|산마루/], ["sea", /바다/], ["river", /강(?!남)|시내|냇물|여울|물가|살수|오강|동정호|폭포/], ["cloud", /구름/], ["rain", /비구름|보슬비|비 오는|먹구름|비와/], ["snow", /눈 덮인|눈 쌓인|눈 내리|서리|겨울/], ["wind", /바람/], ["tree", /나무 위|오동나무 위|대숲/], ["house", /집 위|초가|궁궐|책방|고향 집|마을 가운데/], ["wall", /담 위|담장 위|성 위/], ["field", /밭 가운데|들판|벌판/], ["road", /길(?! 끝의 둥근 문)/], ["fork", /갈림길/], ["hill", /언덕|둑 위|절벽|벼랑/]];

function compose(S) {
  const { p, R, gy, e } = S, rs = p.rs, sc = e.scene || {};
  const ck = circleKind(sc.circle); S.ck = ck.kind;
  const ctext = String(sc.circle || "");
  let back = "", far = "", front = "", objs = "";
  const ground = (y, x0, x1, op) => p.bl([[x0, y + 1], [(x0 + x1) / 2, y - 1.5], [x1, y + .5]], 1.1, null, op ?? .45, [[0, .2], [.3, 1], [.7, 1], [1, .2]]);

  // 사람 · 동물 자리
  const figs = (sc.figures || []).slice(0, 6).map((f, i) => {
    const w = whoOf(f.who), clock = f.clock ?? (i ? 4 : 8);
    const side = clock >= 7 && clock <= 11 ? -1 : clock >= 1 && clock <= 5 ? 1 : clock === 6 ? 0 : (i % 2 ? 1 : -1);
    return { ...f, w, clock, side, up: [10, 11, 12, 1, 2].includes(clock), i };
  });
  const bySide = { "-1": [], "0": [], "1": [] };
  figs.forEach((f) => bySide[f.side].push(f));
  figs.forEach((f) => {
    const list = bySide[f.side], k = list.indexOf(f), crowd = list.length;
    const kid = f.w.child, base = (f.w.animal ? 1 : f.w.scale) * 1.2;
    let s2 = base * (crowd > 2 ? .82 : 1) * (k > 0 ? .92 : 1);
    if (f.side === 0) { f.x = (k - (crowd - 1) / 2) * 22; f.y = gy; s2 *= .78; }
    else { const step = crowd > 2 ? 27 : 36; f.x = f.side * (R + 38 + k * step + (kid && k === 0 ? -6 : 0)); f.y = gy; }
    if (f.up && !f.w.animal) { f.y = gy - 30; s2 *= .72; f.x = f.side * (R + 30 + k * 18); f.raised = true; }
    f.s = s2; f.m = f.side === 0 ? 1 : -f.side; // 원 쪽을 본다
    f.x = clamp(f.x, -148, 148);
  });

  // 소품 나누기
  const props = (sc.props || []).map(propKind).filter(Boolean);
  const scen = props.filter((q) => q.scenery), items = props.filter((q) => !q.scenery);
  const used = new Set();
  const take = (kinds) => { for (const k of kinds) { const q = items.find((it) => it.kind === k && !used.has(it)); if (q) { used.add(q); return q.kind; } } return null; };
  figs.forEach((f) => {
    if (f.w.animal) return;
    const pose = f.pose;
    f.tool = take(POSE_TOOL[pose] || []);
    const must = { read: "book", write: "brush", shoot: "bow", dig: "hoe", plow: "plow", sweep: "broom", sprinkle: "can", fish: "rod", pole: "staff", carve: "hammer", pour: "jar", cup: "bowl", carry: "basket", carryload: "bag", cut: "axe", play: "zither", count: "rods", grind: "whet", wash: "bowl" }[pose];
    if (!f.tool && must) f.tool = must;
    if (pose === "play") { const inst = f.tool; f.drawPose = inst === "flute" ? "flute" : inst === "drum" || inst === "chime" ? "strike" : "play"; }
    if (pose === "crow" || pose === "fly" || pose === "perch" || pose === "graze") f.drawPose = pose === "crow" ? "flute" : "stand";
    if (pose === "swim" || pose === "sleep") f.drawPose = pose;
    if (pose === "hold" && !f.tool) f.tool = null;
    // 곁에 두는 것
    f.near = [];
    if (["read", "write", "sit", "think", "count", "kneel"].includes(pose)) { const d = take(["desk"]); if (d || pose === "write") f.near.push("desk"); const l = take(["lamp"]); if (l) f.near.push("lamp"); const bp = take(["bookpile", "inkstone"]); if (bp) f.near.push(bp); }
    if (pose === "plow" || (pose === "drive" && !take(["ox"]))) f.beast = take(["ox"]) ? "ox" : pose === "plow" ? "ox" : "horse";
    if (pose === "drive") { take(["cart"]); f.cart = true; f.beast = f.beast || "horse"; take(["horse"]); }
    if (pose === "ride") { f.mount = take(["horse", "ox"]) || "horse"; }
    if (pose === "pole") { take(["boat"]); f.boat = true; }
    if (pose === "fish" || pose === "wash") f.water = true;
  });
  const rest = items.filter((q) => !used.has(q)).slice(0, 3);

  // 배경: 원 낱말의 곁말 → 가운데, 소품의 배경 → 빈 쪽
  const mods = new Set();
  for (const [k, re] of CMOD) if (re.test(ctext) && !(k === "mountain" && ck.kind === "mountain") && !(["sea", "river"].includes(k) && ["sea", "river", "pond", "water", "vortex"].includes(ck.kind))) mods.add(k);
  const sk = new Set(scen.map((q) => q.kind));
  const free = figs.some((f) => f.side === 1 && !f.raised) && !figs.some((f) => f.side === -1 && !f.raised) ? -1 : 1; // 사람이 없는 쪽
  const fx = free * (R + 78);
  const boatProp = rest.some((q) => q.kind === "boat");
  const wet = S.wet = mods.has("sea") || mods.has("river") || sk.has("sea") || sk.has("river") || sk.has("fall") || boatProp || figs.some((f) => f.boat || f.water || f.pose === "swim");
  const seaish = mods.has("sea") || sk.has("sea");

  // 먼 배경
  if (mods.has("mountain")) far += mountains(p, -R - 70, R + 70, gy - 4, R + 22, 3);
  if (sk.has("mountain")) far += mountains(p, free > 0 ? R + 20 : -152, free > 0 ? 152 : -R - 20, gy - 6, 46, 2);
  if (mods.has("hill")) far += hills(p, -R - 46, R + 46, gy, R * .7 + 10, .5);
  if (sk.has("hill")) far += hills(p, fx - 40, fx + 40, gy, 20, .5);
  if (mods.has("field") || sk.has("field")) { const x0 = mods.has("field") ? -R - 40 : fx - 34, x1 = mods.has("field") ? R + 40 : fx + 34; for (let u = 0; u < 4; u++) far += p.bl([[x0 + u * 3, gy - 4 - u * 4], [x1 - u * 3, gy - 4 - u * 4]], .6, null, .3, SOFT); }
  if (mods.has("house")) far += /궁궐/.test(ctext) ? hut(p, 0, gy, 2.2, true) : hut(p, 0, gy, 1.5, false);
  if (mods.has("wall")) far += p.poly([[-R - 50, gy - 18], [R + 50, gy - 18], [R + 50, gy], [-R - 50, gy]], "paper", 1) + p.line([[-R - 50, gy - 18], [R + 50, gy - 18]], 1.2, null, .7) + p.area([[-R - 54, gy - 17], [-R - 46, gy - 23], [R + 46, gy - 23], [R + 54, gy - 17]], null, .8);
  if (mods.has("tree")) far += tree(p, 0, gy, 1.5, /대숲/.test(ctext) ? "bamboo" : /소나무/.test(ctext) ? "pine" : "tree", false);
  const treeK = ["willow", "bamboo", "pine", "plum", "tree"].find((k) => sk.has(k));
  if (treeK && !figs.some((f) => f.pose === "climb" || f.pose === "perch")) far += tree(p, fx + free * 8, gy, 1.3, treeK, free < 0);
  if (sk.has("house") || sk.has("palace")) far += hut(p, fx - free * (treeK ? 26 : 0), gy - (treeK ? 8 : 0), treeK ? .9 : 1.2, sk.has("palace"), free > 0);
  if (sk.has("wall") && !mods.has("wall")) { far += p.poly([[fx - 30, gy - 26], [fx + 30, gy - 26], [fx + 30, gy], [fx - 30, gy]], "paper", 1) + p.line([[fx - 30, gy], [fx - 30, gy - 26], [fx + 30, gy - 26], [fx + 30, gy]], 1, null, .75); for (let y = gy - 18, k = 0; y < gy; y += 7, k++) { far += p.line([[fx - 30, y], [fx + 30, y]], .35, null, .3); for (let x = fx - 30 + (k % 2) * 6; x < fx + 30; x += 12) far += p.line([[x, y - 7], [x, y]], .3, null, .25); } far += p.poly([[fx - 36, gy - 24], [fx - 28, gy - 31], [fx + 28, gy - 31], [fx + 36, gy - 24]], null, .82); }
  if (sk.has("camp")) for (let u = 0; u < 3; u++) far += p.area([[fx - 30 + u * 22, gy - 2], [fx - 22 + u * 22, gy - 16], [fx - 14 + u * 22, gy - 2]], null, .25) + p.line([[fx - 30 + u * 22, gy - 2], [fx - 22 + u * 22, gy - 16], [fx - 14 + u * 22, gy - 2]], .9, null, .7);
  if (mods.has("cloud") || sk.has("cloud")) far += cloud(p, -R - 24, -R - 22, 1.3) + cloud(p, R + 30, -R - 40, 1.1);
  if (sk.has("moonsky") && S.ck !== "moon") S.sky.push("moon");
  if (sk.has("sunsky") && S.ck !== "sun") S.sky.push("sun");
  S.sky.forEach((k, i) => { const x = -free * 112, y = -108; if (k === "moon") far += p.disc(x, y, 9, "gold", .35) + p.disc(x + 4, y - 2, 8, "paper", 1); else far += p.disc(x, y, 8, "gold", .4) + p.ring(x, y, 11, .5, "gold", .4); });

  // 원 꾸밈
  const dc = dressCircle(S, ck.kind, ctext);
  back += far + dc.b;

  // 땅 · 물 · 길
  let gnd = "";
  if (wet) { gnd += water(p, -156, 156, gy + 8, 150, .42, seaish); gnd += ground(gy, -156, 156, .4); }
  else gnd += ground(gy, -156, 156, .22);
  if (mods.has("road") || mods.has("fork") || sk.has("road") || sk.has("fork")) {
    const fork = mods.has("fork") || sk.has("fork");
    gnd += p.bl([[-6, gy + 1], [-18, gy + 30], [-44, 156]], .9, null, .5, SOFT) + p.bl([[6, gy + 1], [18, gy + 30], [44, 156]], .9, null, .5, SOFT);
    if (fork) gnd += p.bl([[16, gy + 24], [60, gy + 40], [120, gy + 52]], .9, null, .45, SOFT) + p.bl([[24, gy + 40], [70, gy + 56], [130, gy + 66]], .9, null, .45, SOFT);
  }
  if (sk.has("fall")) gnd += [0, 1, 2, 3].map((k) => p.bl([[fx - 6 + k * 4, -R - 30], [fx - 6 + k * 4, gy + 6]], .7, null, .4, SOFT)).join("") + hills(p, fx - 24, fx + 24, -R - 26, 12, .6);
  if (sk.has("stairs") && !figs.some((f) => f.pose === "climb")) for (let u = 0; u < 5; u++) gnd += p.line([[fx - 20 + u * 8, gy - u * 6], [fx - 12 + u * 8, gy - u * 6], [fx - 12 + u * 8, gy - u * 6 - 6]], 1, null, .7);
  if (sk.has("bridge")) for (let u = 0; u < 4; u++) gnd += p.area(p.blob(-20 + u * 14, gy + 14 + u * 5, 5, 2, 0, .2), null, .55);
  if (sk.has("rocks")) gnd += p.area(p.blob(fx, gy - 5, 11, 6, 0, .25), null, .25) + p.bl(p.blob(fx, gy - 5, 11, 6, 0, .2).slice(5, 10), 1, null, .7);
  if (sk.has("reeds")) gnd += prop(S, "reeds", fx - free * 20, gy, 1.2, 1).svg;
  if (sk.has("flowers")) gnd += prop(S, "flowers", fx + free * 18, gy, 1.2, 1).svg;
  if (mods.has("rain") || sk.has("rain")) for (let u = 0; u < 22; u++) { const x = -150 + rs() * 290, y = -140 + rs() * 200; gnd += p.line([[x, y], [x - 3, y + 9]], .4, null, .3); }
  if (mods.has("snow") || sk.has("snow")) for (let u = 0; u < 26; u++) gnd += p.dot(-150 + rs() * 290, -140 + rs() * 280, .7 + rs() * .6, null, .35);
  if (mods.has("wind") || sk.has("wind")) for (let u = 0; u < 3; u++) { const y = -R - 30 + u * 18, x = -free * 90; gnd += p.bl([[x - 26, y], [x - 6, y - 3], [x + 10, y + 1], [x + 14, y - 4], [x + 9, y - 7]], .7, null, .4, SOFT); }

  // 사람 · 동물
  let figsSvg = "";
  figs.forEach((f) => {
    const s2 = f.s, flip = f.m < 0;
    if (f.raised) figsSvg += ground(f.y, f.x - 18, f.x + 18, .5) + hills(p, f.x - 26, f.x + 26, f.y + 30, 30, .35);
    if (f.w.animal) {
      const k = f.w.animal;
      let x = f.x, y = f.y, pose = f.pose;
      const flyer = ["bird", "crane", "goose", "hawk", "roc", "phoenix", "pheasant", "owl", "butterfly", "dragonfly", "dragon"].includes(k);
      if (pose === "fly" || (k === "dragon" && pose !== "swim") || (k === "roc")) { const a = rad(f.clock * 30 - 90); [x, y] = f.side === 0 ? [0, -R - 40] : pol(a, R + 44); if (f.clock === 8 || f.clock === 4 || f.clock === 7 || f.clock === 5) { x = f.side * (R + 46); y = -R - 8; } }
      if (pose === "perch" && flyer) {
        const a = rad(f.clock * 30 - 90), sd = f.side >= 0 ? 1 : -1; let [px, py] = f.up ? pol(a, R + 36) : [sd * (R + 44), gy - 44]; px = clamp(px, -132, 132);
        const tx = sd * 146; figsSvg += p.bl([[tx, gy], [tx - sd * 2, py + 10], [tx + sd * 1, py - 30]], 4, null, .8, [[0, 1], [1, .5]]);
        for (let j = 0; j < 12; j++) figsSvg += p.leaf(tx + (p.rs() - .5) * 22, py - 30 + (p.rs() - .5) * 16, p.rs() * 2 * PI, 6.4, 1.5, null, .45);
        figsSvg += p.bl([[tx - sd * 1, py + 6], [(tx + px) / 2, py - 2], [px - sd * 10, py + 1]], 1.7, null, .85, [[0, 1], [1, .25]]);
        for (let j = 0; j < 4; j++) figsSvg += p.leaf((tx + px) / 2 + sd * (j * 9 - 12), py - 3 - (j % 2) * 3, rad(sd > 0 ? -120 + j * 20 : -60 - j * 20), 7, 1.5, null, .55);
        x = px; y = py + 1; f.m = -sd;
      }
      if (pose === "swim") { y = k === "dragon" ? gy + 46 : gy + 14; if (k === "dragon") x = 0; }
      const sz = { horse: 1.5, ox: 1.45, tiger: 1.5, deer: 1.45, qilin: 1.45, crane: 1.35, phoenix: 1.4, roc: 1.6, dog: 1.35, fox: 1.35, sheep: 1.35, rooster: 1.45, pheasant: 1.4, bird: 1.35, goose: 1.2, hawk: 1.2, duck: 1.4, owl: 1.4, rabbit: 1.4, monkey: 1.4, squirrel: 1.3, fish: 1.5, turtle: 1.6, frog: 1.6, dragon: 1.5 }[k] || 2.2;
      const ap = pose === "run" || pose === "chase" ? "run" : pose === "leap" ? "leap" : pose === "graze" ? "graze" : pose === "walk" ? "walk" : pose === "crow" ? "crow" : pose === "fly" ? "fly" : pose === "swim" ? "swim" : "stand";
      const a = animal(p, k, ap, x, y, sz * f.s, flip);
      figsSvg += k === "dragon" && pose === "swim" ? `<g opacity=".42">${a.svg}</g>` : a.svg;
      if (!["fly"].includes(pose) && k !== "dragon" && pose !== "perch" && pose !== "swim") figsSvg += ground(y, x - 18, x + 18, .3);
      return;
    }
    const pose = f.drawPose || f.pose;
    const opt = { who: f.w };
    if (pose === "carry" || pose === "carryload") { const t = f.tool || "basket"; opt.back = (T) => { const [bx, by] = T([-8.6, -24]); const r = prop(S, t === "bag" || t === "cloth" ? "bag" : t, bx, by + 8 * s2, s2 * .85, f.m); return r ? r.svg : ""; }; }
    // 탈것 · 배 · 수레
    let fy = f.y, under = "", over = "";
    if (f.boat) { under += prop(S, "boat", f.x - f.m * 4, f.y + 4, s2 * .95, f.m).svg; fy = f.y - 1; }
    if (f.mount) { const hz = animal(p, f.mount, "walk", f.x, f.y, 1.5 * (s2 / 1.42), flip); under += hz.svg; fy = f.y - (QUAD[f.mount].G + QUAD[f.mount].H * .9) * 1.5 * (s2 / 1.42); }
    if (f.cart) { const cs = s2 * .95, r = prop(S, "cart", f.x, f.y, cs, f.m); under += r.svg; fy = f.y - (8 + 7) * cs; const hz = animal(p, f.beast || "horse", "walk", f.x + f.m * 34 * cs, f.y, 1.3 * cs, flip); under += hz.svg; }
    if (f.beast && f.pose === "plow") { over += animal(p, f.beast, "walk", f.x + f.m * 40 * (s2 / 1.42), f.y, 1.35 * (s2 / 1.42), flip).svg; }
    const treeClimb = f.pose === "climb" && (sk.has("tree") || sk.has("pine") || sk.has("willow") || /나무/.test(ctext));
    if (treeClimb) { const tx = f.x + f.m * 9, top = f.y - 52; under += p.bl([[tx, gy], [tx - f.m * 2, (gy + top) / 2], [tx + f.m * 1, top]], 4.4, null, .85, [[0, 1], [1, .45]]) + p.bl([[tx, top + 14], [tx - f.m * 14, top + 4]], 1.4, null, .8, TAPER) + p.bl([[tx, top + 6], [tx + f.m * 12, top - 6]], 1.2, null, .8, TAPER); for (let j = 0; j < 10; j++) under += p.leaf(tx + (rs() - .5) * 30, top + (rs() - .5) * 18, rs() * 2 * PI, 6, 1.4, null, .45); }
    else if (f.pose === "climb") under += p.bl([[f.x - f.m * 16, f.y + 1], [f.x + f.m * 8, f.y - 10], [f.x + f.m * 26, f.y - 24]], 1.2, null, .7, SOFT) + p.area([[f.x - f.m * 16, f.y + 1], [f.x + f.m * 8, f.y - 10], [f.x + f.m * 26, f.y - 24], [f.x + f.m * 26, f.y + 1]], null, .1);
    let fg;
    if (pose === "sleep") {
      const x = f.x, y = f.y, m = f.m;
      fg = { svg: p.shape([[x - m * 14, y - 1], [x - m * 12, y - 7], [x + m * 8, y - 8], [x + m * 12, y - 3], [x + m * 10, y]], "paper", 1, .9) + p.disc(x + m * 15, y - 5, 4.6, "paper", 1, 1) + hat(p, f.w.hat, x + m * 15, y - 5, 4.6, m, 1) + p.area([[x + m * 11, y - 2], [x + m * 22, y - 2], [x + m * 22, y], [x + m * 11, y]], null, .5), hand: [x, y - 6], head: [x + m * 15, y - 5], m, hr: 4.6 };
    } else if (pose === "swim") {
      const x = f.x, y = gy + 12, m = f.m;
      fg = { svg: p.disc(x, y - 4, 4.4, "paper", 1, 1) + hat(p, f.w.hat, x, y - 4, 4.4, m, 1) + p.bl([[x - m * 3, y], [x + m * 6, y - 6], [x + m * 12, y - 2]], 1.3, null, .85) + p.bl([[x - m * 10, y + 1], [x + m * 14, y + 1]], .7, null, .5, SOFT), hand: [x + m * 12, y - 2], head: [x, y - 4], m, hr: 4.4 };
    } else fg = figure(p, pose, f.x, fy, s2, flip, opt);
    S.pose = f.pose;
    let hand = "";
    if (f.tool && !["carry", "carryload", "play"].includes(f.pose)) hand = held(S, f.tool, fg, s2 / 1.42);
    if (f.pose === "play") { const t = f.tool; if (t === "flute") hand = held(S, "flute", fg, s2 / 1.42); else if (t === "drum" || t === "chime") { hand = held(S, "drum", fg, s2 / 1.42); objs += prop(S, t, f.x + f.m * 16 * (s2 / 1.42), f.y, s2 / 1.42 * 1.1, f.m).svg; } else objs += prop(S, "zither", f.x + f.m * 13 * (s2 / 1.42), f.y, s2 / 1.42 * .85, f.m).svg; }
    if (f.pose === "carve") hand += held(S, "chisel", { ...fg, hand: fg.fhand }, s2 / 1.42) + prop(S, "timber", f.x + f.m * 20 * (s2 / 1.42), f.y, s2 / 1.42 * .7, f.m).svg;
    if (f.pose === "grind") objs += prop(S, f.tool === "inkstone" ? "inkstone" : "whet", f.x + f.m * 16 * (s2 / 1.42), f.y, s2 / 1.42 * .9, f.m).svg;
    if (f.pose === "wash" || f.pose === "count") objs += prop(S, f.pose === "count" ? (f.tool === "rods" ? "rods" : f.tool || "rods") : "bowl", f.x + f.m * 17 * (s2 / 1.42), f.y, s2 / 1.42 * 1.1, f.m).svg;
    if (f.pose === "sprinkle") objs += prop(S, "sprout", f.x + f.m * 26 * (s2 / 1.42), f.y, s2 / 1.42, f.m).svg;
    if (f.pose === "throw") hand += p.bl([[fg.hand[0], fg.hand[1]], [fg.hand[0] + f.m * 30, fg.hand[1] - 16], [fg.hand[0] + f.m * 52, fg.hand[1] + 4]], .5, null, .35, SOFT) + p.dot(fg.hand[0] + f.m * 52, fg.hand[1] + 4, 1.6, null, .8);
    if (f.pose === "dance") hand += p.bl([fg.hand, [fg.hand[0] + f.m * 8, fg.hand[1] + 4], [fg.hand[0] + f.m * 4, fg.hand[1] + 14]], 1.4, null, .45, TAPER) + p.bl([fg.fhand, [fg.fhand[0] - f.m * 8, fg.fhand[1] + 6], [fg.fhand[0] - f.m * 3, fg.fhand[1] + 16]], 1.4, null, .4, TAPER);
    // 곁 소품: 앞(원 쪽)에 책상, 뒤에 등잔 · 책 더미
    let nearSvg = "";
    f.near.forEach((k, j) => {
      const sc2 = s2 / 1.42;
      if (k === "desk") { const dx = f.x + f.m * 17 * sc2, r = prop(S, "desk", dx, f.y, sc2, f.m); nearSvg += r.svg; if (f.pose === "write") nearSvg += prop(S, "paper", dx, f.y - 8.4 * sc2, sc2 * .8, f.m).svg; else nearSvg += prop(S, "book", dx + f.m * 3 * sc2, f.y - 8.2 * sc2, sc2 * .8, f.m).svg; }
      else { const r = prop(S, k, f.x - f.m * (18 + j * 8) * sc2, f.y, sc2 * (k === "lamp" ? 1 : .9), f.m); if (r) nearSvg += r.svg; }
    });
    if (f.pose === "write" && !f.near.includes("desk")) nearSvg += prop(S, "paper", f.x + f.m * 14, f.y, s2 / 1.42, f.m).svg;
    figsSvg += under + nearSvg + fg.svg + hand + over + (f.raised || f.boat || f.pose === "swim" ? "" : ground(f.y, f.x - 20 * (s2 / 1.42), f.x + 20 * (s2 / 1.42), .45));
  });

  // 남은 소품: 빈 땅에
  const slots = [];
  const occ = figs.filter((f) => !f.raised && !(f.w.animal && ["fly", "perch"].includes(f.pose))).map((f) => [f.x - 22, f.x + 22]);
  for (const x of [free * (R + 36), free * (R + 62), -free * (R + 14), free * (R + 92), free * (R + 116), -free * 142]) if (!occ.some(([a, b]) => x > a - 8 && x < b + 8) && Math.abs(x) <= 146) slots.push(x);
  rest.forEach((q, j) => { let x = slots[j]; if (x == null) return; if (["horse", "ox", "cart", "boat", "deerp", "tigerp"].includes(q.kind)) x = clamp(x, -124, 124); const boat = q.kind === "boat", r = prop(S, q.kind, x, boat ? gy + 16 : gy, ["horse", "ox"].includes(q.kind) ? 1.3 : boat ? 1.2 : 1.5, -Math.sign(x) || 1); if (r) objs += r.svg + (boat ? "" : ground(gy, x - r.w - 4, x + r.w + 4, .35)); });

  const marks = growMarks(S, figs);
  return { b: back, f: dc.f, g: gnd + objs + figsSvg + marks, wash: dc.wash };
}

/* ───────────── 시안 여섯 장면(손그림) ───────────── */
const BESPOKE = {
  LI01(S) { // 愚公移山: 원 = 옮겨지는 산
    const { p, R, N, ACC } = S, rs = p.rs; let b = "", f = "";
    const gy = R + 40, ground = (y, x0, x1) => p.bl([[x0, y + 1], [(x0 + x1) / 2, y - 1.5], [x1, y + .5]], 1.1, null, .45, [[0, .2], [.3, 1], [.7, 1], [1, .2]]);
    const mound = (cx, cy, w, h) => { const pts = [[cx - w, cy], [cx - w * .7, cy - h * .55], [cx - w * .25, cy - h], [cx + w * .3, cy - h * .9], [cx + w * .75, cy - h * .45], [cx + w, cy]]; let o = p.area([...pts, [cx, cy + .6]], null, .24) + p.bl(pts, .75, null, .7, [[0, .3], [.25, 1], [.75, 1], [1, .3]]); for (let k = 0; k < 2; k++) o += p.dot(cx + (rs() - .5) * w * .9, cy - h * (.3 + rs() * .35), .45 + rs() * .35, null, .7); return o; };
    const basket = (T, x, y, w, h, s2) => { const a = T([x - w, y - h * .85]), b2 = T([x + w, y - h * .85]), c2 = T([x + w * .55, y]), d2 = T([x - w * .55, y]); const [mx, my] = T([x, y - h * .85]); return p.area([a, b2, c2, d2], "paper", 1) + p.bl([a, d2, c2, b2], .8, null, .85, EVEN) + mound(mx, my + .3, w * s2 * 1.2, h * s2 * 1.05); };
    const ridge = [[-R - 44, gy], pol(rad(168), R + 1), pol(rad(196), R + 1), [-R * .62, -R - 34], [-R * .2, -R - 16], [R * .38, -R - 46], [R * .86, -R - 12], pol(rad(-14), R + 1), pol(rad(14), R + 1), [R + 40, gy]];
    b += p.area([...ridge, [0, gy]], null, .07) + p.bl(ridge.slice(2, 8), 2.3, null, .85) + p.bl(ridge.slice(0, 3), 1.6, null, .7) + p.bl(ridge.slice(7), 1.6, null, .7);
    for (let u = 0; u < 14; u++) { const j = 1 + Math.min(7, Math.floor(rs() * 8)), [x0, y0] = ridge[j], [x1, y1] = ridge[j + 1], x = x0 + (x1 - x0) * rs(), y = y0 + (y1 - y0) * rs() + 5 + rs() * 9; if (Math.hypot(x, y) > R + 4 && y < gy - 4) b += p.bl([[x, y], [x - 3, y + 5]], .9, null, .45, TAPER); }
    b += ground(gy, -152, 152);
    const dg = figure(p, "dig", -R - 58, gy, 1.45, false, { who: { hat: "top" } });
    f += dg.svg + p.bl([dg.T([8, -24]), dg.T([20, -4])], .9, null, .9) + p.bl([dg.T([19.6, -4.4]), dg.T([21.4, .4]), dg.T([25, .6])], 1.5, null, .95, [[0, 1], [1, .8]]);
    f += mound(-R - 30, gy - .5, 7, 4.2);
    const jige = (T) => p.bl([T([-6, -41]), T([-4.6, -4])], .8, null, .9) + p.bl([T([-9.6, -39]), T([-8.2, -6])], .8, null, .9) + p.bl([T([-9.6, -29]), T([-5.4, -29.6])], .7, null, .9) + basket(T, -9.6, -30.5, 5.4, 6.4, 1.5);
    const ug = figure(p, "carry", R + 34, gy, 1.5, false, { who: { hat: "top", beard: true }, back: jige });
    const kid = figure(p, "carry", R + 4, gy, 1.02, false, { who: { hat: "child" }, back: (T) => basket(T, -6.6, -17.6, 4.6, 5.2, 1.02) });
    f += kid.svg + ug.svg;
    for (let r2 = 0; r2 < 3; r2++) for (let u = 0; u < 4 - (r2 === 0 ? 1 : 0); u++) { const x = 104 + u * 12 + r2 * 5, y = gy - 13 + r2 * 4.2; b += p.bl([[x, y + 1.2], [x + 3, y - 1], [x + 6.4, y - 1.4], [x + 9.4, y + .6]], .8, ACC, .78 - r2 * .14, [[0, .2], [.4, 1], [1, .2]]); }
    const heaps = Math.min(4, Math.max(1, Math.round(N / 2)));
    for (let u = 0; u < heaps; u++) f += mound(112 + u * 12.5, gy - .4, 7.4, 4.4 + (u % 2) * 1.4);
    return { b, f };
  },
  LS01(S) { // 刻舟求劍: 원 = 칼이 가라앉은 물
    const { p, R, N, ACC } = S, rs = p.rs; let b = "", f = "";
    [[R + 12, 205, 335], [R + 22, 215, 325], [R + 12, 28, 152], [R + 24, 18, 162], [R + 36, 30, 120]].forEach(([q, a0, a1], u) => { const pts = []; for (let k = 0; k <= 8; k++) { const a = rad(a0 + (a1 - a0) * k / 8); pts.push([Math.cos(a) * q, Math.sin(a) * q + Math.sin(k * 1.7) * 1.4]); } b += p.bl(pts, .9, null, .38 - u * .04, SOFT); });
    for (let u = 0; u < N; u++) { const a = rad(60 + 230 * rs()), q = R + 8 + rs() * 34; b += p.bl([pol(a, q), pol(a + .12, q + 1)], .6, null, .35, TAPER); }
    const sw = [[-R * .3, -R * .26], [R * .26, R * .24]], sa = Math.atan2(sw[1][1] - sw[0][1], sw[1][0] - sw[0][0]);
    f += p.bl([sw[0], sw[1]], 1.5, null, .9, [[0, .9], [.85, 1], [1, .2]]) + p.bl([[sw[0][0] - Math.sin(sa) * 4, sw[0][1] + Math.cos(sa) * 4], [sw[0][0] + Math.sin(sa) * 4, sw[0][1] - Math.cos(sa) * 4]], 1.2, null, .95) + p.bl([sw[0], [sw[0][0] - Math.cos(sa) * 7, sw[0][1] - Math.sin(sa) * 7]], 1.8, null, .95) + p.bl([[sw[0][0] - Math.cos(sa) * 7, sw[0][1] - Math.sin(sa) * 7], [sw[0][0] - Math.cos(sa) * 10 - 2, sw[0][1] - Math.sin(sa) * 7 + 6]], 1.2, ACC, .9, TAPER);
    const bx = R + 36, by = R + 34, hull = [[bx - 46, by - 5], [bx - 24, by - 1], [bx + 14, by - 1], [bx + 44, by - 8], [bx + 34, by + 8], [bx - 26, by + 10]];
    f += p.area(hull, null, .78) + p.bl([[bx - 46, by - 5], [bx, by - .8], [bx + 44, by - 8]], 1.3, null, .95);
    const sc = figure(p, "kneel", bx - 17, by - 1.2, 1.3, true, { who: { hat: "gat" } });
    f += sc.svg + p.bl([sc.T([12.2, -8]), sc.T([13.6, -4.6])], 1, null, .95);
    f += p.bl([[bx - 36, by - 3.4], [bx - 34.4, by + 1.8]], 1.2, ACC, .95, [[0, 1], [1, .6]]);
    const pm = figure(p, "pole", bx + 23, by - 4, 1.3, true, { who: { hat: "satgat" } });
    f += pm.svg + p.bl([pm.T([3, -36]), pm.T([-14, 14])], .85, null, .9);
    return { b, f };
  },
  MZ01(S) { // 揠苗助長: 원 = 둥근 논
    const { p, R, N, ACC } = S, rs = p.rs; let b = "", f = "";
    const dk = []; for (let k = 0; k <= 48; k++) { const a = 2 * PI * k / 48; dk.push(pol(a, R + 5.5 + Math.sin(k * 1.3) * .6)); }
    b += p.ring(0, 0, R + 3.8, 5.6, null, .12) + p.bl(dk.slice(4, 22), .7, null, .45, SOFT) + p.bl(dk.slice(27, 45), .7, null, .4, SOFT);
    const clump = (x, y, h, op) => { let o = ""; [-14, -2, 11].forEach((d, k) => { const a0 = rad(-90 + d + (rs() - .5) * 8), c = walk(x + (k - 1) * 1.1, y, a0, h * (k === 1 ? 1 : .82), (t) => rad(d * .35) * t, 6); o += `<path d="${outline(c, c.map((_, j) => .55 * Math.sin(PI * Math.min(1, .18 + j / 6 * .82))))}" ${p.fa(null, op)}/>`; }); return o + p.bl([[x - 3.2, y + .6], [x + 3.2, y + .4]], .45, null, op * .55, [[0, .2], [.5, 1], [1, .2]]); };
    [[R + 11, 1, .62], [R + 21, .86, .5]].forEach(([q, hs, op], row) => { const n = Math.round(PI * q / 11.5); for (let u = 0; u <= n; u++) { const a = rad(-8 + 196 * (u + row * .5) / n); if (a > rad(188)) continue; if (a < rad(70) && a > rad(-10)) continue; const [x, y] = pol(a, q), sy = Math.sin(a); b += clump(x, y, (7 + rs() * 2.5) * hs * (.78 + .22 * sy), op); } });
    const pulled = Math.min(6, N);
    for (let u = 0; u < pulled; u++) {
      const a = rad(34 + 62 * (u + .5) / pulled), [x0, y0] = pol(a, R + 12), lift = 3.6 + (u % 2) * 2, y1 = y0 - lift;
      b += p.bl([[x0 - 3, y0 + .6], [x0 + 3, y0 + .4]], .45, null, .35, [[0, .2], [.5, 1], [1, .2]]);
      [-1.6, -.4, .9, 1.9].forEach((dx) => { f += p.bl([[x0 + dx * .5, y1], [x0 + dx, y1 + 2.4 + rs() * 1.4]], .3, null, .6, TAPER); });
      const c = walk(x0, y1, rad(-90 + 14 + (rs() - .5) * 10), 9 + rs() * 2.4, (t) => rad(22) * t * t, 7), [tx, ty, ta] = c[c.length - 1];
      f += `<path d="${outline(c, c.map((_, j) => .72 * (1 - .35 * j / 7)))}" ${p.fa(null, .8)}/>`;
      [-1, 1].forEach((sd) => { const lc = walk(tx, ty, ta + sd * rad(58), 7.4, (t) => sd * rad(48) * t * t, 7); f += `<path d="${outline(lc, lc.map((_, j) => 1.15 * Math.sin(PI * Math.min(1, .1 + j / 7 * .9))))}" ${p.fa(null, .55)}/>` + `<path d="${outline(lc.slice(4), lc.slice(4).map((_, j) => .95 * Math.sin(PI * Math.min(1, .35 + j / 3 * .65))))}" ${p.fa(ACC, .62)}/>`; });
    }
    const [hx, hy] = pol(rad(24), R + 15), s2 = 1.6, X = hx + 14.4 * s2, Y = hy + 5.6 * s2;
    f += p.bl([[X - 24, Y + 1], [X - 1, Y - 1.5], [X + 22, Y + .5]], 1.1, null, .45, [[0, .2], [.3, 1], [.7, 1], [1, .2]]) + figure(p, "pull", X, Y, s2, true, { who: { hat: "satgat" } }).svg;
    return { b, f };
  },
  GT01(S) { // 惟手熟爾(숙능생교): 원 = 엽전
    const { p, R, N, ACC } = S; let b = "", f = "";
    const q = R * .34;
    f += `<rect x="${f1(-q / 2 - 3)}" y="${f1(-q / 2 - 3)}" width="${f1(q + 6)}" height="${f1(q + 6)}" ${p.st(null, 1.1, .55)}/>` + p.area([[-q / 2, -q / 2], [q / 2, -q / 2], [q / 2, q / 2], [-q / 2, q / 2]], "paper", 1) + `<rect x="${f1(-q / 2)}" y="${f1(-q / 2)}" width="${f1(q)}" height="${f1(q)}" ${p.st(null, 1.2)}/>`;
    const gx = 0, gy = R + 30;
    b += p.area([[gx - 2.6, R + 3], [gx + 2.6, R + 3], [gx + 3.4, R + 9], [gx + 8.6, R + 15], [gx + 6.4, R + 21], [gx + 14, gy + 4], [gx + 10, gy + 16], [gx - 10, gy + 16], [gx - 14, gy + 4], [gx - 6.4, R + 21], [gx - 8.6, R + 15], [gx - 3.4, R + 9]], ACC, .22);
    b += p.bl([[gx - 2.6, R + 3], [gx - 3.4, R + 9], [gx - 8.6, R + 15], [gx - 6.4, R + 21], [gx - 14, gy + 4], [gx - 10, gy + 16], [gx + 10, gy + 16], [gx + 14, gy + 4], [gx + 6.4, R + 21], [gx + 8.6, R + 15], [gx + 3.4, R + 9], [gx + 2.6, R + 3]], 1.1, null, .9, EVEN);
    b += p.bl([[-60, gy + 17.5], [0, gy + 15], [60, gy + 17]], 1.1, null, .45, [[0, .2], [.3, 1], [.7, 1], [1, .2]]);
    const plat = -R - 14, px0 = Math.max(R + 6, 30);
    b += p.bl([[px0, plat], [px0 + 70, plat - 1]], 1.6, null, .85, [[0, .8], [1, .9]]) + p.bl([[px0 + 6, plat], [px0 + 6, plat + 14]], 1, null, .7) + p.bl([[px0 + 62, plat - 1], [px0 + 62, plat + 13]], 1, null, .7);
    const om = figure(p, "pour", px0 + 30, plat, 1.6, true, { who: { hat: "top", beard: true } });
    const [lx, ly] = om.T([12.4, -37.4]), tip = [lx - 9, ly - 1];
    f += om.svg + p.bl([[lx, ly], tip], .8, null, .95) + `<path d="M${P2(tip[0] - 2.6, tip[1] - 1)}q2.6 4 5.2 0z" ${p.fa(null)}/>`;
    f += p.bl([[tip[0] - 1, tip[1] + 2], [tip[0] * .5, tip[1] * .4], [0, -q / 2], [0, 0]], .7, ACC, .95, [[0, 1], [1, .7]]) + p.bl([[0, R + 2], [0, R + 5]], .6, ACC, .95);
    const jars = Math.min(5, Math.max(1, Math.round(N / 2)));
    for (let u = 0; u < jars; u++) { const jx = px0 + 48 + u * 9 - (jars > 3 ? 8 : 0); f += p.area(p.blob(jx, plat - 5, 4, 5, 0, .12), null, .55) + p.bl([[jx - 2, plat - 10], [jx + 2, plat - 10]], .8, null, .9); }
    return { b, f };
  },
  ZG01(S) { // 畫蛇添足: 원을 감은 뱀 그림
    const { p, R, N, ACC } = S; let b = "", f = "";
    const pts = [], n = 40;
    for (let u = 0; u <= n; u++) { const t = u / n, a = rad(150 - 300 * t), q = R + 8 + 5 * t + Math.sin(t * 22) * 1.6; pts.push([Math.cos(a) * q, Math.sin(a) * q]); }
    const c = cr(pts, false, 3), W = [[0, .1], [.12, .65], [.5, 1], [.9, .75], [.96, .55], [1, .3]];
    b += `<path d="${outline(c, c.map((_, j) => 3.4 * ease(W, j / (c.length - 1))))}" ${p.fa(null, .82)}/>`;
    for (let u = 2; u < 14; u++) { const [x, y, a] = c[Math.round(c.length * u / 15)]; b += p.line([[x - Math.sin(a) * 2, y + Math.cos(a) * 2], [x + Math.sin(a) * 2, y - Math.cos(a) * 2]], .5, "paper", .6); }
    const [hx, hy, ha] = c[c.length - 1];
    b += p.area(p.blob(hx + Math.cos(ha) * 3, hy + Math.sin(ha) * 3, 5.6, 3.8, ha, .1), null, .9) + p.bl([[hx + Math.cos(ha) * 8, hy + Math.sin(ha) * 8], [hx + Math.cos(ha) * 13, hy + Math.sin(ha) * 13 - 1]], .5, ACC, .95, [[0, 1], [1, .5]]);
    const legs = Math.min(8, N + 1);
    for (let u = 0; u < legs; u++) { const [x, y, a] = c[Math.round(c.length * (.18 + .62 * u / Math.max(1, legs - 1)))], o2 = a - PI / 2, k = [x + Math.cos(o2) * 3, y + Math.sin(o2) * 3], e2 = [k[0] + Math.cos(o2 + .5) * 6, k[1] + Math.sin(o2 + .5) * 6]; f += p.bl([k, e2], 1, ACC, .9) + [-.6, 0, .6].map((d) => p.bl([e2, [e2[0] + Math.cos(o2 + .5 + d) * 2.6, e2[1] + Math.sin(o2 + .5 + d) * 2.6]], .5, ACC, .9, TAPER)).join(""); }
    const [cx, cy] = pol(rad(38), R + 22), s2 = 1.5, X = cx + 13.2 * s2, Y = cy + 5.2 * s2 + 2;
    const dr = figure(p, "crouch", X, Y, s2, true, { who: { hat: "top" } });
    const gnd = (y, x0, x1) => p.bl([[x0, y + 1], [(x0 + x1) / 2, y - 1.5], [x1, y + .5]], 1.1, null, .45, [[0, .2], [.3, 1], [.7, 1], [1, .2]]);
    f += gnd(Y, X - 20, X + 18) + dr.svg + p.bl([dr.T([13.2, -5.2]), dr.T([16.4, -1.4])], .7, null, .95);
    const wx = -R - 44, wy = R + 40, wn = figure(p, "cup", wx, wy, 1.5, false, { who: { hat: "top" } });
    const [ux, uy] = wn.T([6.2, -34.6]);
    f += gnd(wy, wx - 20, wx + 20) + wn.svg + p.area([[ux - 3.4, uy - 2.6], [ux + 3.4, uy - 2.6], [ux + 2.2, uy + 2], [ux - 2.2, uy + 2]], ACC, .85);
    return { b, f };
  },
  SN01(S) { // 讀書百遍: 원 = 등잔 불빛
    const { p, R, N, ACC } = S; let b = "", f = "";
    const fy = R - 5;
    f += `<path d="M${P2(0, fy - 7)}C${P2(3.4, fy - 2)} ${P2(2.6, fy + 2)} ${P2(0, fy + 2.4)}C${P2(-2.6, fy + 2)} ${P2(-3.4, fy - 2)} ${P2(0, fy - 7)}Z" ${p.fa("gold", .95)}/>`;
    f += p.area([[-7, fy + 2.6], [7, fy + 2.6], [4.6, fy + 5.6], [-4.6, fy + 5.6]], null, .85);
    b += p.bl([[0, R + 4], [0, R + 40]], 1.3, null, .85) + p.area([[-9, R + 40], [9, R + 40], [7, R + 44], [-7, R + 44]], null, .8);
    for (let u = 0; u < 12; u++) { const a = rad(-170 + 160 * u / 11); f += p.bl([pol(a, R + 4), pol(a, R + 9 + (u % 2) * 3)], .6, "gold", .55, TAPER); }
    const groups = Math.min(9, N + 2);
    for (let u = 0; u < groups; u++) { const a = rad(-160 + 140 * (u + .5) / groups), [cx, cy] = pol(a, R + 19), s3 = 3.6; [[[-s3, -s3], [s3, -s3]], [[0, -s3], [0, s3]], [[0, 0], [s3 * .8, 0]], [[-s3 * .6, -s3 * .1], [-s3 * .6, s3]], [[-s3 * 1.1, s3], [s3 * 1.1, s3]]].forEach(([p0, p1]) => { f += p.bl([[cx + p0[0], cy + p0[1]], [cx + p1[0], cy + p1[1]]], .55, ACC, .9, [[0, .8], [1, .6]]); }); }
    const fl = R + 46, X = 40, sch = figure(p, "read", X, fl, 1.6, true, { who: { hat: "gat" } });
    const [bx, by] = sch.T([9.4, -11.2]);
    f += p.bl([[-60, fl + 1], [10, fl - 1.5], [80, fl + .5]], 1.1, null, .45, [[0, .2], [.3, 1], [.7, 1], [1, .2]]) + sch.svg + p.area([[bx - 1, by - 3], [bx - 9, by - 1.6], [bx - 9, by + 2.2], [bx - 1, by + 1]], "paper", 1) + p.bl([[bx - 1, by - 3], [bx - 9, by - 1.6], [bx - 9, by + 2.2], [bx - 1, by + 1], [bx - 1, by - 3]], .5, null, .9);
    f += p.bl([[bx - 22, fl - 9], [bx - 6, fl - 9]], 1.4, null, .85) + p.bl([[bx - 20, fl - 9], [bx - 20, fl]], .9, null, .8) + p.bl([[bx - 8, fl - 9], [bx - 8, fl]], .9, null, .8);
    return { b, f };
  },
};

/* ───────────── 그림 한 장 ───────────── */
const FONT = "'Noto Serif KR','Noto Serif CJK KR','Gowun Batang',serif";
/**
 * 격언 그림 SVG 문자열.
 * @param {object} e   격언 항목(gyeokeon.v2.json의 entries[i])
 * @param {object} [o] theme 'light'|'dark' · months [{S, who, seen}](처음 달부터 그달까지, 코드로 고르기) · cum 그달 누적 문항 ·
 *                     R 그달 비율 밴드(1~5) · name 아이 짧은 이름(도장) · label 'YYYY.M' · nth 몇 번째 달 · N 표시 개수(직접)
 */
export function drawScene(e, o = {}) {
  const pal = PALETTE[o.theme === "dark" ? "dark" : "light"];
  const months = Array.isArray(o.months) && o.months.length ? o.months : null;
  const cur = months ? months[months.length - 1] : null;
  const cum = Number(o.cum ?? cur?.cum ?? 0) || 0;
  const R = months ? Math.min(44, 20 + 5 * Math.log2(1 + Math.max(0, cum) / 400)) : 32;
  const band = clamp(Math.round(Number(o.R ?? cur?.R ?? 3)) || 3, 1, 5);
  const N = o.N != null ? clamp(Math.round(o.N), 1, 12) : months ? [3, 4, 5, 7, 9][band - 1] : 5;
  const dom = months ? dominantType(cur.S || {}) : TYPES.includes(e.primary) ? e.primary : null;
  const ACC = dom ? TYPE_COLOR[dom] : null;
  const seed = (o.name || "") + "|" + e.id + (months ? "|" + (o.label || "") : "");
  const p = pen(pal, rng(seedOf(seed + "장면")));
  const gy = BESPOKE[e.id] ? R + 40 : R + 46;
  const S = { p, R, gy, ground: gy, N, ACC, sky: [], e, pose: null, ck: null, wet: false };

  // 종이
  const rp = rng(seedOf(seed + "종이"));
  let fib = ""; for (let u = 0; u < 46; u++) { const x = rp() * 320 - 160, y = rp() * 320 - 160, b2 = rp() * PI, l = 6 + rp() * 16; fib += `M${P2(x, y)}q${f1(Math.cos(b2) * l / 2 + (rp() - .5) * 4)} ${f1(Math.sin(b2) * l / 2 + (rp() - .5) * 4)} ${f1(Math.cos(b2) * l)} ${f1(Math.sin(b2) * l)}`; }
  const paper = `<rect x="-160" y="-160" width="320" height="320" fill="${pal.paper}"/><path d="${fib}" fill="none" stroke="${pal.ink}" stroke-opacity=".07" stroke-width=".5"/>`;

  // 장면
  let sc;
  if (BESPOKE[e.id]) { const r = BESPOKE[e.id](S); sc = { b: r.b, f: r.f, g: "", wash: e.id === "SN01" ? ["gold", .12] : e.id === "LS01" ? [null, .07] : null }; }
  else sc = compose(S);

  // 원: 지나온 달의 결 + 붓으로 그은 바깥 원
  const ro = rng(seedOf(seed + "원"));
  let ring = p.disc(0, 0, R + 1, "paper", 1);
  if (sc.wash) ring += p.disc(0, 0, R, sc.wash[0], sc.wash[1]);
  if (months) {
    const i = months.length - 1, pa = ro() * 2 * PI, pox = Math.cos(pa) * R * .2, poy = Math.sin(pa) * R * .2;
    months.forEach((m, j) => {
      const fq = (j + 1) / (i + 1), q = R * (.1 + .8 * fq), h = R * .8 / (i + 1), mk = dominantType(m.S || {}), op = (m.seen ? .85 : .3) * (mk ? 1 : .5);
      const ox = pox * (1 - fq), oy = poy * (1 - fq), sw = Math.max(.45, h * (m.who === "P" ? .55 : m.who === "E" ? .3 : .42));
      const dash = m.who === "P" ? "" : m.who === "E" ? ` stroke-dasharray=".3 2.2"` : ` stroke-dasharray="2.6 1.4"`;
      const ph = ro() * 2 * PI, amp = Math.min(.6, h * .25);
      let d = ""; for (let u = 0; u <= 60; u++) { const a = u / 60 * 2 * PI, qq = q + amp * Math.sin(3 * a + ph) + amp * .6 * Math.sin(5 * a + ph * 2); d += (u ? "L" : "M") + P2(ox + Math.cos(a) * qq, oy + Math.sin(a) * qq); }
      ring += `<path d="${d}Z" fill="none" stroke="${mk ? TYPE_COLOR[mk] : pal.ink}" stroke-opacity="${f1(op * 100) / 100}" stroke-width="${f1(sw * 10) / 10}" stroke-linecap="round"${dash}/>`;
    });
  }
  const a0 = rad(-150 + ro() * 60), nE = 72, ec = [];
  for (let u = 0; u <= nE; u++) { const t = u / nE, a = a0 + rad(318) * t, q = R + 2.4 + (ro() - .5) * .5 + Math.sin(t * 7 + a0) * .35; ec.push([Math.cos(a) * q, Math.sin(a) * q, a + PI / 2]); }
  const eh = ec.map((_, u) => { const t = u / nE; return 1.6 * (.3 + 1.1 * Math.pow(1 - t, 1.4) + .14 * Math.sin(t * 13)) * Math.min(1, (1 - t) / .12) * Math.min(1, .7 + t * 14) * (.9 + .2 * ro()); });
  ring += `<path d="${outline(ec, eh)}" ${p.fa(null, .88)}/>`;

  // 표제(세로) · 도장 · 날짜
  const lab = [...String(e.label || "")].slice(0, 8), n = lab.length, step = n <= 4 ? 16 : n === 5 ? 14.6 : n === 6 ? 13 : 11.4, fs = n <= 4 ? 13 : n <= 6 ? 12 : 10.6;
  let words = lab.map((ch, u) => `<text x="148" y="${f1(-134 + u * step)}" font-family="${FONT}" font-weight="700" font-size="${fs}" fill="${pal.ink}" fill-opacity=".88" text-anchor="middle">${esc(ch)}</text>`).join("");
  if (o.name) {
    const nm = [...String(o.name)].slice(0, 4), y0 = -134 + (n - 1) * step + 8;
    words += `<g transform="translate(148 ${f1(y0)})"><rect x="-8" y="0" width="16" height="${nm.length * 10 + 5}" rx="1.5" fill="${pal.ju}"/>` + nm.map((ch, u) => `<text x="0" y="${10 + u * 10}" font-family="${FONT}" font-weight="700" font-size="8" fill="${pal.paper}" text-anchor="middle">${esc(ch)}</text>`).join("") + "</g>";
  }
  if (o.label) words += `<text x="151" y="150" font-family="${FONT}" font-size="8.5" fill="${pal.ink}" fill-opacity=".7" text-anchor="end">${esc(o.label)}${o.nth ? ` · ${esc(o.nth)}번째 달` : ""}</text>`;

  const seen = cur ? cur.seen !== 0 && cur.seen !== false : true;
  const title = esc(`${e.label_eum || e.label || ""}`);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-160 -160 320 320" role="img" aria-label="${title}">` + paper + `<g opacity="${seen ? 1 : .55}">` + sc.b + ring + sc.f + (sc.g || "") + `</g>` + words + `</svg>`;
}

/** 시험용: 장면을 어떻게 읽었는지 */
export function sceneInfo(e) {
  const sc = e.scene || {};
  return { circle: circleKind(sc.circle).kind, figures: (sc.figures || []).map((f) => ({ ...whoOf(f.who), pose: f.pose })), props: (sc.props || []).map((q) => propKind(q)?.kind || null), bespoke: !!BESPOKE[e.id] };
}
export const _internal = { POSE, FIG, genPose, figure, pen, rng, seedOf, whoOf, hat, animal, prop };
