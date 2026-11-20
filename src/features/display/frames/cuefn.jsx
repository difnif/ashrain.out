// ashrain.out — 수학 호기심 액자: 당구로 보는 대칭(빈쿠션 치기) (frames/cuefn.jsx)
// 노란 공이 가로막아 흰 공을 빨간 공에 곧장 보낼 수 없다 → 쿠션을 거울로 보고, 거울 속 빨간 공(R′)을 곧게 겨냥한다.
// 장면: 막힘 → 거울 당구대 → R′ → 직선 CR′ → 쿠션과 만나는 점 H → 접기(거울 속 길이 당구대 안으로) → 흰 공이 굴러 맞힘.
//   중등: 직선의 식 · 쿠션(y = 8 등)과 만나는 점 · 튕긴 뒤 기울기의 부호.  초등: 쿠션까지 칸 수의 비로 나누기 · 들어간 각 = 나온 각.
// 쿠션 두 번(모서리 쪽)은 거울을 두 번 비춘 R″를 겨냥한다. 풀이 상세: 오른쪽 설명 판 · 최소화: 당구대를 크게, 칩 하나. 계산: ../curio/cue.js
import { memo } from "react";
import { W, H, MText, SceneTitle, Path, Draw, SANS } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, Chip, chipW } from "../kit-story.jsx";
import { SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx, pt, num, lineOf, eqText, fs } from "../curio/kit.js";
import { TBL, CUSH, reflect, cushEq, cueAt, cueTimes, cueSteps, cueSummary, pathOf, CUE_D } from "../curio/cue.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { FitText, Lines, Panel, Small, clipLine, BigChip, bigW, besideLine, pickSpot } from "./curio-kit.jsx";

const LSK = "ash.display.curio.cue";
const AREA = { full: [40, 150, 1140, 870], mini: [36, 150, 1564, 872] };
const PANEL = { x: 1162, y: 150, w: 400, h: 720 };
const BR = 0.3;   // 공 반지름(칸) — 그림용

/* ══════════ 카메라 ══════════ */
const CAMS = new WeakMap();
/** 그 공 배치의 카메라: 당구대 + 거울 속 빨간 공이 다 들어오게(가로 · 세로 같은 비율) */
export function cueCam(s, ex) {
  let m = CAMS.get(s);
  if (!m) { m = {}; CAMS.set(s, m); }
  if (m[ex]) return m[ex];
  const im = s.img;
  const x0 = Math.min(-1.7, im[0] - 1.5), x1 = Math.max(TBL.w + 1.3, im[0] + 1.5);
  const y0 = Math.min(-1.7, im[1] - 1.5), y1 = Math.max(TBL.h + 1.3, im[1] + 1.5);
  const A = AREA[ex], aw = A[2] - A[0], ah = A[3] - A[1] - (ex === "mini" ? 56 : 0);
  const sc = Math.min(aw / (x1 - x0), ah / (y1 - y0));
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, mx = (A[0] + A[2]) / 2, my = (A[1] + A[3]) / 2 + (ex === "mini" ? 28 : 0);
  const cam = { s: sc, p: (q) => [mx + (q[0] - cx) * sc, my - (q[1] - cy) * sc], box: A,
    u: (px, py) => [cx + (px - mx) / sc, cy - (py - my) / sc] };
  m[ex] = cam;
  return cam;
}

/* ══════════ 색 ══════════ */
const COL = {
  dark: { felt: "#1d5596", feltEdge: "#164679", wood: "#5b3520", woodEdge: "#7a4a2c", dia: "#f1e6d0", grid: "#ffffff" },
  light: { felt: "#3a7fc4", feltEdge: "#2d6aa8", wood: "#8a5733", woodEdge: "#a8724a", dia: "#fff7e6", grid: "#ffffff" },
};
const BALL = { w: "#f7f6f0", r: "#d8343a", y: "#f3c22f" };

/** 당구대(사각형 rect = [x0, y0, x1, y1] 칸) — real 이면 나무 테와 다이아몬드까지 */
function Table({ cam, C, rect, real, o = 1, railO = 1 }) {
  const K = COL[C.name === "light" ? "light" : "dark"];
  const [a, b] = [cam.p([rect[0], rect[3]]), cam.p([rect[2], rect[1]])];
  const w = b[0] - a[0], h = b[1] - a[1], r = 0.9 * cam.s;
  if (o <= 0.001) return null;
  if (!real) {
    return <rect x={a[0]} y={a[1]} width={w} height={h} fill={K.felt} fillOpacity={0.42 * o} stroke="#ffffff" strokeOpacity={0.55 * o} strokeWidth={1.6} strokeDasharray="8 7" />;
  }
  const dias = [];
  for (let x = 2; x < TBL.w; x += 2) { dias.push([x, -0.45]); dias.push([x, TBL.h + 0.45]); }
  for (let y = 2; y < TBL.h; y += 2) { dias.push([-0.45, y]); dias.push([TBL.w + 0.45, y]); }
  return (
    <g opacity={o}>
      <g opacity={railO}>
        <rect x={a[0] - r} y={a[1] - r} width={w + 2 * r} height={h + 2 * r} rx={r * 0.6} fill={K.wood} stroke={K.woodEdge} strokeWidth={2} />
        {dias.map((q, i) => { const p = cam.p(q); return <circle key={i} cx={p[0]} cy={p[1]} r={Math.max(2.6, cam.s * 0.075)} fill={K.dia} />; })}
      </g>
      <rect x={a[0]} y={a[1]} width={w} height={h} fill={K.felt} stroke={K.feltEdge} strokeWidth={Math.max(3, cam.s * 0.12)} />
    </g>
  );
}

/** 눈금: 중등은 보이는 칸 전체(거울 속까지), 초등은 당구대 위만 */
function Grid({ cam, C, mode, o = 1, top = 0 }) {
  const [bx0, by0, bx1, by1] = cam.box;
  const isM = mode === "m";
  const ink = "#ffffff", lab = C.name === "light" ? "#1f2a33" : "#e8eef8", hal = C.name === "light" ? "#f6efe0" : "#141c33";
  const u0 = cam.u(bx0, by1), u1 = cam.u(bx1, by0);
  const xs = isM ? [Math.ceil(u0[0]), Math.floor(u1[0])] : [0, TBL.w], ys = isM ? [Math.ceil(u0[1]), Math.floor(u1[1])] : [0, TBL.h];
  const out = [];
  for (let x = xs[0]; x <= xs[1]; x++) {
    const p = cam.p([x, isM ? u0[1] : 0]), q = cam.p([x, isM ? u1[1] : TBL.h]);
    out.push(<line key={"x" + x} x1={p[0]} x2={q[0]} y1={p[1]} y2={q[1]} stroke={ink} strokeOpacity={x % 2 === 0 ? 0.13 : 0.06} strokeWidth={1} />);
  }
  for (let y = ys[0]; y <= ys[1]; y++) {
    const p = cam.p([isM ? u0[0] : 0, y]), q = cam.p([isM ? u1[0] : TBL.w, y]);
    out.push(<line key={"y" + y} x1={p[0]} x2={q[0]} y1={p[1]} y2={q[1]} stroke={ink} strokeOpacity={y % 2 === 0 ? 0.13 : 0.06} strokeWidth={1} />);
  }
  // 숫자: 중등은 판 아래 · 왼쪽 가장자리, 초등은 당구대 바깥 테 밖
  const labs = [];
  const fsz = 14;
  if (isM) {
    for (let x = xs[0]; x <= xs[1]; x++) if (x % 2 === 0) { const p = cam.p([x, 0]); if (p[0] > bx0 + 26 && p[0] < bx1 - 12) labs.push(<MText key={"lx" + x} x={p[0]} y={by1 - 8} s={num(x)} size={fsz} weight={700} anchor="middle" fill={lab} halo={hal} opacity={0.75} C={C} />); }
    for (let y = ys[0]; y <= ys[1]; y++) if (y % 2 === 0) { const p = cam.p([0, y]); if (p[1] < by1 - 24 && p[1] > by0 + 14 + top) labs.push(<MText key={"ly" + y} x={bx0 + 8} y={p[1] + 5} s={num(y)} size={fsz} weight={700} anchor="start" fill={lab} halo={hal} opacity={0.75} C={C} />); }
    const O = cam.p([0, 0]), X = cam.p([u1[0], 0]), Y = cam.p([0, u1[1]]);
    labs.push(<line key="ax" x1={cam.p([u0[0], 0])[0]} x2={X[0] - 6} y1={O[1]} y2={O[1]} stroke={lab} strokeOpacity={0.5} strokeWidth={1.6} />);
    labs.push(<line key="ay" x1={O[0]} x2={O[0]} y1={cam.p([0, u0[1]])[1]} y2={Y[1] + 6} stroke={lab} strokeOpacity={0.5} strokeWidth={1.6} />);
    labs.push(<MText key="xl" x={X[0] - 18} y={O[1] - 10} s="x" size={20} fill={lab} halo={hal} C={C} />);
    labs.push(<MText key="yl" x={O[0] + 10} y={Y[1] + 22} s="y" size={20} fill={lab} halo={hal} C={C} />);
    labs.push(<MText key="o" x={O[0] - 8} y={O[1] + 22} s="O" size={15} weight={700} anchor="end" fill={lab} halo={hal} C={C} />);
  } else {
    for (let x = 0; x <= TBL.w; x += 2) { const p = cam.p([x, -1.25]); labs.push(<MText key={"lx" + x} x={p[0]} y={p[1] + 5} s={String(x)} size={fsz} weight={700} anchor="middle" fill={lab} halo={hal} opacity={0.8} C={C} />); }
    for (let y = 0; y <= TBL.h; y += 2) { const p = cam.p([-1.2, y]); labs.push(<MText key={"ly" + y} x={p[0]} y={p[1] + 5} s={String(y)} size={fsz} weight={700} anchor="middle" fill={lab} halo={hal} opacity={0.8} C={C} />); }
  }
  return <g opacity={o}><g>{out}</g>{labs}</g>;
}

function Ball({ cam, q, kind, o = 1, ghost }) {
  if (o <= 0.001) return null;
  const p = cam.p(q), r = BR * cam.s;
  if (ghost) return <circle cx={p[0]} cy={p[1]} r={r} fill={BALL[kind]} fillOpacity={0.35} stroke={BALL[kind]} strokeWidth={2.4} strokeDasharray="5 4" opacity={o} />;
  return (
    <g opacity={o}>
      <ellipse cx={p[0] + r * 0.18} cy={p[1] + r * 0.32} rx={r} ry={r * 0.8} fill="#000" opacity={0.28} />
      <circle cx={p[0]} cy={p[1]} r={r} fill={BALL[kind]} stroke="#1b1b1b" strokeOpacity={0.45} strokeWidth={1.4} />
      <circle cx={p[0] - r * 0.35} cy={p[1] - r * 0.38} r={r * 0.28} fill="#fff" opacity={0.55} />
    </g>
  );
}

/* ══════════ 길 ══════════ */
const plen = (P) => { let L = 0; for (let i = 1; i < P.length; i++) L += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); return L; };
/** 길 P 를 따라 거리 d 만큼 간 점과 그때까지의 점들 */
function walk(P, d) {
  const out = [P[0]];
  let left = d;
  for (let i = 1; i < P.length; i++) {
    const L = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]);
    if (left <= L) { const k = L ? left / L : 1; const q = [lerp(P[i - 1][0], P[i][0], k), lerp(P[i - 1][1], P[i][1], k)]; out.push(q); return { q, pts: out }; }
    left -= L; out.push(P[i]);
  }
  return { q: P[P.length - 1], pts: out };
}
/** 점 a 를 중심 o 로 각 th(라디안)만큼 돌린 점 */
const rot = (a, o, th) => { const c = Math.cos(th), s = Math.sin(th), x = a[0] - o[0], y = a[1] - o[1]; return [o[0] + x * c - y * s, o[1] + x * s + y * c]; };

/** 장면 상태(그림과 판이 같이 쓴다) */
function stateOf(s, t) {
  const T = cueTimes(s);
  const P = pathOf(s);
  const last = P[P.length - 2], R = s.R;
  const u = (() => { const dx = R[0] - last[0], dy = R[1] - last[1], n = Math.hypot(dx, dy) || 1; return [dx / n, dy / n]; })();
  const stop = [R[0] - u[0] * 2 * BR, R[1] - u[1] * 2 * BR];
  const route = [...P.slice(0, -1), stop];
  const kr = seg(t, T.roll[0], T.roll[1], E.io);
  const W1 = walk(route, plen(route) * kr);
  const kk = seg(t, T.knock[0], T.knock[1] + 600, E.out);
  const red = [clamp(R[0] + u[0] * 1.7 * kk, BR + 0.05, TBL.w - BR - 0.05), clamp(R[1] + u[1] * 1.7 * kk, BR + 0.05, TBL.h - BR - 0.05)];
  return { T, P, route, white: W1.q, trail: kr > 0 ? W1.pts.concat([W1.q]) : null, red, kr };
}

/* ══════════ 장면 ══════════ */
export function CueArt({ C, mode, ex, at }) {
  const { s, t } = at;
  const cam = cueCam(s, ex), isM = mode === "m", mini = ex === "mini";
  const st = stateOf(s, t), T = st.T;
  const fade = 1 - seg(t, T.fade[0], T.fade[1], E.sine);
  const intro = seg(t, T.intro[0], T.intro[1], E.out);
  const kb = seg(t, T.block[0], T.block[0] + 500) * (1 - seg(t, T.mirror[0], T.mirror[1]));
  const km = seg(t, T.mirror[0], T.mirror[1]) * (1 - seg(t, T.roll[0] + 600, T.roll[1]));
  const ki = seg(t, T.image[0], T.image[1]);
  const kl = seg(t, T.line[0], T.line[1], E.out);
  const kh = seg(t, T.hit[0], T.hit[0] + 500);
  const kh2 = s.two ? seg(t, T.hit2[0], T.hit2[0] + 500) : 0;
  const kf = seg(t, T.fold[0], T.fold[1], E.io);
  const fin = seg(t, T.knock[1], T.knock[1] + 700);
  const tc = C.name === "light" ? "#0f766e" : "#7fe3d3";
  // 거울 당구대들
  const mirrors = s.cush.map((c) => mirRect([c]));
  if (s.two) mirrors.push(mirRect(s.cush));
  const clipId = `cue-clip-${ex}`;
  const [bx0, by0, bx1, by1] = cam.box;
  // 직선 C → 거울 속 빨간 공
  const lineEnd = [lerp(s.C[0], s.img[0], kl), lerp(s.C[1], s.img[1], kl)];
  // 접기(쿠션 한 번): H → R′ 를 H 를 중심으로 돌려 H → R 로
  let foldEl = null;
  const H0 = s.hits[0];
  if (!s.two && kh > 0) {
    const a0 = Math.atan2(s.img[1] - H0[1], s.img[0] - H0[0]), a1 = Math.atan2(s.R[1] - H0[1], s.R[0] - H0[0]);
    let da = a1 - a0;
    while (da > Math.PI) da -= 2 * Math.PI;
    while (da < -Math.PI) da += 2 * Math.PI;
    const tip = rot(s.img, H0, da * kf);
    foldEl = kf > 0 ? <Path pts={[cam.p(H0), cam.p(tip)]} stroke={C.gold} sw={4} o={1 - st.kr * 0.6} /> : null;
  }
  // 쿠션 두 번: 실제 길이 그려지며 나타남
  const revealEl = s.two && kf > 0 ? <Draw pts={st.P.map((q) => cam.p(q))} p={kf} stroke={C.gold} sw={4} o={1 - st.kr * 0.6} /> : null;
  const goldPath = (!s.two && kf >= 1) || (s.two && kf >= 1);
  // 각 표시(초등): 꺾이는 점마다 쿠션과 두 다리 사이의 같은 각
  const arcs = !isM && kf > 0.6 ? s.hits.map((Hq, i) => <AngleMarks key={i} cam={cam} H={Hq} a={st.P[i]} b={st.P[i + 2]} c={s.cush[i]} C={C} o={seg(kf, 0.6, 1, (u) => u) * (1 - fin * 0.3)} />) : null;
  const eq = eqText(lineOf(s.C, s.img));
  // 식 칩: 직선 CR′ 옆 여러 자리 가운데 공 · 점에서 가장 먼 곳
  const eqPos = (() => {
    const w = chipW(eq, 22), hgt = 34, avoid = [s.C, s.R, s.Y, s.img, ...s.hits].map((q) => cam.p(q));
    const A = cam.p(s.C), B = cam.p(s.img), n = Math.hypot(B[0] - A[0], B[1] - A[1]) || 1, nx = -(B[1] - A[1]) / n, ny = (B[0] - A[0]) / n;
    let best = null, bs = -1;
    for (const f of [0.18, 0.3, 0.42, 0.58, 0.7, 0.82]) for (const sd of [1, -1]) {
      const cx = clamp(lerp(A[0], B[0], f) + nx * sd * (hgt + 6), bx0 + w / 2 + 8, bx1 - w / 2 - 8), cy = clamp(lerp(A[1], B[1], f) + ny * sd * (hgt + 6), by0 + 24, by1 - 36);
      const sc = Math.min(...avoid.map((q) => Math.hypot(Math.max(0, Math.abs(q[0] - cx) - w / 2), Math.max(0, Math.abs(q[1] - cy) - hgt / 2))));
      if (sc > bs + 0.5) { bs = sc; best = [cx, cy]; }
    }
    return best;
  })();
  const lblSz = mini ? 26 : 23;   // 좌표 칩 — 그림에서 눈에 띄게
  const fitX = (x, w) => clamp(x, bx0 + w / 2 + 6, bx1 - w / 2 - 6), fitY = (y) => clamp(y, by0 + 22, by1 - 34);
  const label = (q, str, dy, col, o, dx = 0) => { const p = cam.p(q), w = chipW(str, lblSz); return <Chip x={fitX(p[0] + (dx ? Math.sign(dx) * (Math.abs(dx) + w / 2) : 0), w)} y={fitY(p[1] + dy)} s={str} size={lblSz} C={C} color={col} o={o} />; };
  /** 쿠션 위 점의 이름표: 그 쿠션 바깥(나무 테) 쪽으로 */
  const hitLbl = (i, str, k) => { const c = CUSH[s.cush[i]], Hq = s.hits[i]; return c.axis === "y" ? label(Hq, str, c.v > 0 ? -40 : 42, C.gold, k) : label(Hq, str, 0, C.gold, k, c.v > 0 ? 18 : -18); };
  const above = (q) => (q[1] > TBL.h / 2 && q[1] <= TBL.h ? 42 : -42) * (q[1] > TBL.h ? -1 : 1);
  // 기울기 칩(중등, 금테 · 크게): 첫 다리 C → H 옆, 접은 뒤에는 튕긴 다리 옆에 「튕긴 뒤 기울기」
  const Lm = lineOf(s.C, s.img), bs = mini ? 36 : 30;
  const P0 = cam.p(s.C), P1 = cam.p(s.hits[0]), P2 = cam.p(s.two ? s.hits[1] : s.R);
  const avoidC = [s.C, s.R, s.Y, s.img, ...s.hits].map((q) => { const p = cam.p(q); return { x: p[0], y: p[1], w: 30, h: 30 }; })
    .concat([[s.C, `C${pt(s.C)}`], [s.R, `R${pt(s.R)}`]].map(([q, t2]) => { const p = cam.p(q); return { x: p[0], y: p[1] + above(q), w: chipW(t2, lblSz), h: lblSz * 1.5 }; }))
    .concat(s.hits.map((q) => { const p = cam.p(q); return { x: p[0], y: p[1] + (CUSH[s.cush[0]].axis === "y" ? (q[1] > 4 ? -40 : 42) : 0), w: 170, h: lblSz * 1.5 }; }))
    .concat(eqPos ? [{ x: eqPos[0], y: eqPos[1], w: chipW(eq, 22), h: 33 }] : []);
  const s1 = isM && Lm.kind === "f" ? `기울기 ${fs(Lm.m[0], Lm.m[1])}` : "", s2 = isM && Lm.kind === "f" ? `튕긴 뒤 기울기 ${fs(-Lm.m[0], Lm.m[1])}` : "";
  const box2 = [bx0, by0, bx1, by1];
  /** 다리 P→Q 옆 빈자리: 큰 글자로 안 되면 작게, 그래도 안 되면 빼기(설명 판에 있다) */
  const place = (txt, P, Q, av) => {
    if (!txt) return null;
    for (const sz of [bs, Math.round(bs * 0.8)]) {
      const w = bigW(txt, sz), h = sz * 1.5;
      const c = [0.5, 0.35, 0.65, 0.2, 0.8].flatMap((f) => [besideLine(P, Q, w, h, f, 1), besideLine(P, Q, w, h, f, -1)]);
      const at = pickSpot(c, w, h, av, box2);
      const room = Math.min(...av.map((r) => Math.hypot(Math.max(0, Math.abs(r.x - at[0]) - (r.w + w) / 2), Math.max(0, Math.abs(r.y - at[1]) - (r.h + h) / 2))));
      if (room >= 3) return { at, sz, w, h };
    }
    return mini ? (() => { const w = bigW(txt, bs), h = bs * 1.5; return { at: pickSpot([besideLine(P, Q, w, h, 0.5, 1)], w, h, av, box2), sz: bs, w, h }; })() : null;
  };
  const sAt1 = place(s1, P0, P1, avoidC);
  const sAt2 = place(s2, P1, P2, sAt1 ? [...avoidC, { x: sAt1.at[0], y: sAt1.at[1], w: sAt1.w, h: sAt1.h }] : avoidC);
  return (
    <g opacity={fade}>
      <defs><clipPath id={clipId}><rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} /></clipPath></defs>
      <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} fill={C.name === "light" ? "#e9dfc9" : "#121a30"} opacity={0.55} />
      <g clipPath={`url(#${clipId})`}>
        <Table cam={cam} C={C} rect={[0, 0, TBL.w, TBL.h]} real railO={1 - 0.7 * km} />
        {mirrors.map((r, i) => <Table key={i} cam={cam} C={C} rect={r} o={km * (i === 2 ? 0.75 : 1)} />)}
        <Grid cam={cam} C={C} mode={mode} top={mini ? 64 : 0} />
        {/* 거울(쿠션) 선 */}
        {s.cush.map((c, i) => <Mirror key={c} cam={cam} c={c} C={C} o={km} isM={isM} col={tc} idx={i} two={s.two} />)}
        {/* 막힘 */}
        {kb > 0 && <Path pts={[cam.p(s.C), cam.p(s.R)]} stroke="#ffffff" sw={2.4} dash="7 7" o={0.85 * kb} />}
        {/* 거울 속 빨간 공과 수직 점선 */}
        {ki > 0 && km > 0.01 && (
          <g opacity={ki * Math.min(1, km * 1.5)}>
            <Path pts={[cam.p(s.R), cam.p(s.two ? reflect(s.R, s.cush[0]) : s.img)]} stroke={BALL.r} sw={2} dash="3 5" o={0.8} />
            {s.two && <Path pts={[cam.p(reflect(s.R, s.cush[0])), cam.p(s.img)]} stroke={BALL.r} sw={2} dash="3 5" o={0.8} />}
            {s.two && <Ball cam={cam} q={reflect(s.R, s.cush[0])} kind="r" ghost o={0.6} />}
            <Ball cam={cam} q={s.img} kind="r" ghost />
          </g>
        )}
        {/* 직선 C → R′ */}
        {kl > 0 && <Path pts={[cam.p(s.C), cam.p(lineEnd)]} stroke={tc} sw={3} dash="11 8" o={0.95 * (1 - 0.55 * st.kr)} />}
        {revealEl}
        {foldEl}
        {/* 굴러간 길 */}
        {st.trail && <Path pts={st.trail.map((q) => cam.p(q))} stroke={C.gold} sw={4.6} />}
        {goldPath && !st.trail && <Path pts={st.P.map((q) => cam.p(q))} stroke={C.gold} sw={4} o={0.4} />}
        {arcs}
        {/* 꺾이는 점 */}
        {s.hits.map((Hq, i) => { const k = i === 0 ? kh : kh2; if (k <= 0) return null; const p = cam.p(Hq); return <g key={i} opacity={k}><circle cx={p[0]} cy={p[1]} r={16 * (1.5 - 0.5 * k)} fill={C.gold} opacity={0.22} /><circle cx={p[0]} cy={p[1]} r={7.5} fill={C.gold} stroke="#fff" strokeWidth={2.2} /></g>; })}
        {/* 공 */}
        <Ball cam={cam} q={s.Y} kind="y" o={intro} />
        <Ball cam={cam} q={st.red} kind="r" o={intro} />
        <Ball cam={cam} q={st.white} kind="w" o={intro} />
        {kb > 0 && <g opacity={kb}><Cross cam={cam} q={s.Y} C={C} /></g>}
      </g>
      <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} fill="none" stroke={C.cardEdge} strokeWidth={1.4} />
      {/* 이름표 */}
      {isM ? (
        <g>
          {label(s.C, `C${pt(s.C)}`, above(s.C), undefined, intro * (1 - st.kr))}
          {label(s.R, `R${pt(s.R)}`, above(s.R), undefined, intro * (1 - st.kr * 0.4))}
          {ki > 0 && km > 0.01 && label(s.img, `${s.two ? "R″" : "R′"}${pt(s.img)}`, s.img[1] > TBL.h ? -38 : s.img[1] < 0 ? 38 : -38, C.coral, ki * Math.min(1, km * 1.5))}
          {s.hits.map((Hq, i) => { const k = i === 0 ? kh : kh2; if (k <= 0) return null; return <g key={i}>{hitLbl(i, `${s.two ? (i ? "Q" : "P") : "H"}${fpt(s.hf[i])}`, k)}</g>; })}
          {!mini && kl > 0.6 && <Chip x={eqPos[0]} y={eqPos[1]} s={eq} size={22} C={C} o={seg(kl, 0.6, 1, (u) => u) * (1 - st.kr * 0.5)} />}
          {sAt1 && <BigChip x={sAt1.at[0]} y={sAt1.at[1]} s={s1} size={sAt1.sz} C={C} o={seg(kl, 0.5, 1, (u) => u) * (1 - fin * 0.2)} />}
          {sAt2 && <BigChip x={sAt2.at[0]} y={sAt2.at[1]} s={s2} size={sAt2.sz} C={C} color={C.name === "light" ? "#0f766e" : "#7fe3d3"} edge={C.name === "light" ? "#0f766e" : "#7fe3d3"} o={seg(kf, 0.7, 1, (u) => u)} />}
        </g>
      ) : (
        <g>
          {label(s.C, "흰 공", above(s.C), undefined, intro * (1 - st.kr))}
          {label(s.R, "빨간 공", above(s.R), undefined, intro * (1 - st.kr * 0.4))}
          {label(s.Y, "노란 공", above(s.Y), undefined, intro * (1 - ki))}
          {ki > 0 && km > 0.01 && label(s.img, s.two ? "두 번 비친 빨간 공" : "거울 속 빨간 공", s.img[1] > TBL.h ? -38 : 38, C.coral, ki * Math.min(1, km * 1.5))}
          {s.hits.map((Hq, i) => { const k = i === 0 ? kh : kh2; if (k <= 0) return null; const along = CUSH[s.cush[i]].axis === "y" ? Hq[0] : Hq[1]; return <g key={i}>{hitLbl(i, s.two ? (i ? "Q" : "P") : `쿠션 ${fmtN(along)}칸`, k)}</g>; })}
        </g>
      )}
      {mini && <CueMini C={C} mode={mode} s={s} k={at.k} o={intro} t={t} />}
      {!mini && <CuePanel C={C} mode={mode} s={s} t={t} k={at.k} />}
    </g>
  );
}
const fpt = (f) => `(${fs(f[0][0], f[0][1])}, ${fs(f[1][0], f[1][1])})`;
const fmtN = (v) => (Math.abs(v - Math.round(v)) < 1e-9 ? String(Math.round(v)) : v.toFixed(1));
/** 쿠션 c(들)에 비친 당구대의 사각형 */
function mirRect(cs) {
  let r = [0, 0, TBL.w, TBL.h];
  for (const c of cs) {
    const a = reflect([r[0], r[1]], c), b = reflect([r[2], r[3]], c);
    r = [Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.max(a[0], b[0]), Math.max(a[1], b[1])];
  }
  return r;
}
/** 거울(쿠션) 선 — 빛나는 선과 이름 */
function Mirror({ cam, c, C, o, isM, col, idx, two }) {
  if (o <= 0.01) return null;
  const K = CUSH[c];
  const a = K.axis === "y" ? [0, K.v] : [K.v, 0], b = K.axis === "y" ? [TBL.w, K.v] : [K.v, TBL.h];
  const A = cam.p(a), B = cam.p(b);
  const mid = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2];
  const lbl = isM ? cushEq(c) : two ? `거울 ${idx + 1}` : "거울";
  // 이름은 쿠션 바깥(나무 테) 쪽에
  const lx = mid[0] + (K.axis === "x" ? (K.v > 0 ? 30 : -30) : 0), ly = mid[1] + (K.axis === "y" ? (K.v > 0 ? -24 : 30) : 0);
  return (
    <g opacity={o}>
      <line x1={A[0]} y1={A[1]} x2={B[0]} y2={B[1]} stroke={col} strokeWidth={9} strokeOpacity={0.22} strokeLinecap="round" />
      <line x1={A[0]} y1={A[1]} x2={B[0]} y2={B[1]} stroke={col} strokeWidth={3} strokeLinecap="round" />
      <g transform={K.axis === "x" ? `rotate(-90 ${lx} ${ly})` : undefined}>
        <MText x={lx} y={ly + 6} s={lbl} size={18} weight={800} anchor="middle" fill={col} halo={C.halo} C={C} />
      </g>
    </g>
  );
}
function Cross({ cam, q, C }) {
  const p = cam.p(q), r = BR * cam.s + 8;
  return (
    <g>
      <circle cx={p[0]} cy={p[1]} r={r} fill="none" stroke={C.coral} strokeWidth={3} />
      <path d={`M${p[0] - r * 0.7} ${p[1] - r * 0.7}L${p[0] + r * 0.7} ${p[1] + r * 0.7}M${p[0] + r * 0.7} ${p[1] - r * 0.7}L${p[0] - r * 0.7} ${p[1] + r * 0.7}`} stroke={C.coral} strokeWidth={3.4} strokeLinecap="round" />
    </g>
  );
}
/** 들어간 각 = 나온 각: 쿠션과 두 다리 사이에 같은 크기의 호 */
function AngleMarks({ cam, H, a, b, c, C, o }) {
  const K = CUSH[c], p = cam.p(H), r = Math.max(26, cam.s * 0.9);
  const dirA = Math.atan2(a[1] - H[1], a[0] - H[0]), dirB = Math.atan2(b[1] - H[1], b[0] - H[0]);   // 수학 각(y 위로) — 화면에는 y 를 뒤집어 그린다
  // 쿠션 방향: 두 다리 쪽으로 각각
  const along = K.axis === "y" ? [0, Math.PI] : [Math.PI / 2, -Math.PI / 2];
  const near = (d) => along.reduce((best, v) => (Math.abs(angDiff(v, d)) < Math.abs(angDiff(best, d)) ? v : best), along[0]);
  const arc = (d) => {
    const base = near(d), d0 = base, d1 = base + angDiff(base, d);
    const x0 = p[0] + r * Math.cos(d0), y0 = p[1] - r * Math.sin(d0), x1 = p[0] + r * Math.cos(d1), y1 = p[1] - r * Math.sin(d1);
    const sweep = angDiff(base, d) > 0 ? 0 : 1;
    return `M${x0} ${y0}A${r} ${r} 0 0 ${sweep} ${x1} ${y1}`;
  };
  const col = C.name === "light" ? "#0f766e" : "#7fe3d3";
  return (
    <g opacity={o}>
      <path d={arc(dirA)} fill="none" stroke={col} strokeWidth={3.2} />
      <path d={arc(dirB)} fill="none" stroke={col} strokeWidth={3.2} />
    </g>
  );
}
const angDiff = (a, b) => { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };

/* ══════════ 설명 판 ══════════ */
function CuePanel({ C, mode, s, t, k }) {
  const { x, y, w, h } = PANEL, x0 = x + 22, mw = w - 44;
  const T = cueTimes(s);
  const lines = cueSteps(s, mode).map((L) => ({ ...L, col: L.col ? C[L.col] : undefined }));
  const head = s.two ? `쿠션 두 번 — ${CUSH[s.cush[0]].name} → ${CUSH[s.cush[1]].name}` : `쿠션 한 번 — ${CUSH[s.cush[0]].name}`;
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <FitText x={x0} y={y + 34} s={`당구 · 빈쿠션 치기 · 가상 배치 · ${k + 1}번째 공`} size={15} maxW={mw} minSize={10} weight={650} fill={C.soft} C={C} />
      <FitText x={x0} y={y + 74} s={head} size={24} maxW={mw} minSize={15} weight={800} fill={C.ink} C={C} />
      <line x1={x0} x2={x + w - 22} y1={y + 98} y2={y + 98} stroke={C.cardEdge} strokeWidth={1.2} />
      <Lines x={x0} y={y + 142} lines={lines} t={t} C={C} size={21} lh={50} maxW={mw} hiSize={25} />
      <Legend x={x0} y={y + h - 92} C={C} mode={mode} />
      <Small x={x0} y={y + h - 22} s="1칸 = 다이아몬드 반 칸(약 17.75 cm)" size={14} C={C} />
    </g>
  );
}
function Legend({ x, y, C, mode }) {
  const items = mode === "m" ? [["w", "흰 공 C(치는 공)"], ["r", "빨간 공 R"], ["y", "노란 공(가로막음)"]] : [["w", "흰 공(치는 공)"], ["r", "빨간 공(맞힐 공)"], ["y", "노란 공(가로막음)"]];
  return (
    <g>
      {items.map(([k, s], i) => (
        <g key={k}>
          <circle cx={x + 9} cy={y + i * 24 - 5} r={8} fill={BALL[k]} stroke="#1b1b1b" strokeOpacity={0.4} />
          <text x={x + 26} y={y + i * 24} fontFamily={SANS} fontSize={15} fontWeight={650} fill={C.soft}>{s}</text>
        </g>
      ))}
    </g>
  );
}
function CueMini({ C, mode, s, k, o, t }) {
  const [x0, y0, x1] = AREA.mini;
  const T = cueTimes(s);
  const a = cueSummary(s, mode, t >= T.line[0] + 600 ? (t >= (s.two ? T.hit2[0] : T.hit[0]) ? 2 : 1) : 0), b = `${k + 1}번째 공 · 가상 배치`;
  return (
    <g opacity={o}>
      <Chip x={x0 + 14} y={y0 + 30} s={a} size={22} C={C} anchor="start" />
      <Chip x={x1 - 14} y={y0 + 30} s={b} size={18} C={C} anchor="end" color={C.gold} />
    </g>
  );
}

/* ══════════ 액자 ══════════ */
const DEF = { ex: "full", sp: 1, seed: 1 };
const fixPrm = (p = {}) => ({ ex: fixEx(p.ex), sp: SPEEDS.includes(p.sp) ? p.sp : 1, seed: Number.isInteger(p.seed) && p.seed > 0 && p.seed < 1e6 ? p.seed : 1 });
export function CueFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, DEF, fixPrm);
  const P = lab.prm;
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const e = lab.elapsed() * P.sp;
  const at = cueAt(P.seed, e);
  const jump = (d) => {
    const base = e - at.t;
    const target = d > 0 ? base + CUE_D : at.t > 1500 || base <= 0 ? base : base - CUE_D;
    lab.jump(Math.max(0, target) / P.sp); poke();
  };
  const fresh = () => { lab.setPrm({ seed: P.seed + 1 }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: fresh, toggleFs, onMode, poke }),
    ArrowRight: () => jump(1), ArrowLeft: () => jump(-1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="풀이"><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
      <span className="dsp-sep" />
      <ui.Btn title="이전 공 (←)" onClick={() => jump(-1)}><ui.Ic d="M15 5 8 12l7 7" /></ui.Btn>
      <ui.Btn title="다음 공 (→)" onClick={() => jump(1)}><ui.Ic d="m9 5 7 7-7 7" /></ui.Btn>
    </>
  );
  const title = { e: "당구로 보는 대칭 — 쿠션은 거울", m: "당구로 보는 대칭과 일차함수" };
  const sub = at.s.two ? "쿠션 두 번 — 거울을 두 번 비춘 빨간 공을 곧게 겨냥" : "빈쿠션 치기 — 거울 속 빨간 공을 곧게 겨냥";
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="당구 빈쿠션 치기로 보는 대칭">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <CueArt C={C} mode={Ly.mode} ex={P.ex} at={at} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={fresh}
        restartTitle="새 배치" isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings} prog={at.t / CUE_D} />
    </>
  );
}
export const CueThumb = memo(function CueThumb({ C, mode = "m" }) {
  const at = cueAt(1, 0);
  return <CueArt C={C} mode={mode} ex="full" at={{ ...at, t: at.T.fold[1] + 200 }} />;
});
