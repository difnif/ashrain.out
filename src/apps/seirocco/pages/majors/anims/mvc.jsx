// 다변수 · 벡터 그림 — 등위선 · 경사(그레이디언트)와 경사하강 · 라그랑주 승수 · 이중적분(칸 나누기) · 벡터장(흐름 · 발산 · 회전) · 내적과 정사영
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, fmt, clamp, useClock, lerp } from "./kit.jsx";

/** 등위선(마칭 스퀘어) — f(x,y) = c 인 선분 묶음을 path 하나로 */
export function contourPath(P, f, c, n = 48) {
  const dx = (P.x1 - P.x0) / n, dy = (P.y1 - P.y0) / n;
  let d = "";
  const v = [];
  for (let j = 0; j <= n; j++) { v[j] = []; for (let i = 0; i <= n; i++) v[j][i] = f(P.x0 + i * dx, P.y0 + j * dy) - c; }
  const ip = (x0, y0, a, x1, y1, b) => { const t = a / (a - b); return [x0 + (x1 - x0) * t, y0 + (y1 - y0) * t]; };
  for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
    const x = P.x0 + i * dx, y = P.y0 + j * dy;
    const a = v[j][i], b = v[j][i + 1], cc = v[j + 1][i + 1], dd = v[j + 1][i];
    const pts = [];
    if ((a > 0) !== (b > 0)) pts.push(ip(x, y, a, x + dx, y, b));
    if ((b > 0) !== (cc > 0)) pts.push(ip(x + dx, y, b, x + dx, y + dy, cc));
    if ((cc > 0) !== (dd > 0)) pts.push(ip(x + dx, y + dy, cc, x, y + dy, dd));
    if ((dd > 0) !== (a > 0)) pts.push(ip(x, y + dy, dd, x, y, a));
    for (let k = 0; k + 1 < pts.length; k += 2)
      d += `M${P.X(pts[k][0]).toFixed(1)} ${P.Y(pts[k][1]).toFixed(1)}L${P.X(pts[k + 1][0]).toFixed(1)} ${P.Y(pts[k + 1][1]).toFixed(1)}`;
  }
  return d || "M0 0";
}

const SURF = {
  bowl: { f: (x, y) => x * x + 2 * y * y, gx: (x) => 2 * x, gy: (x, y) => 4 * y, lv: [0.5, 1.5, 3, 5, 8], name: "f = x² + 2y² (그릇)", st: [2.6, 1.6] },
  saddle: { f: (x, y) => x * x - y * y, gx: (x) => 2 * x, gy: (x, y) => -2 * y, lv: [-4, -2, -0.8, 0.8, 2, 4], name: "f = x² − y² (안장)", st: [0.15, 2.4] },
  hills: { f: (x, y) => Math.exp(-((x - 1) ** 2 + y * y)) + 0.8 * Math.exp(-((x + 1.3) ** 2 + (y - 1) ** 2) / 0.6),
    gx: (x, y) => -2 * (x - 1) * Math.exp(-((x - 1) ** 2 + y * y)) - 0.8 * (2 * (x + 1.3) / 0.6) * Math.exp(-((x + 1.3) ** 2 + (y - 1) ** 2) / 0.6),
    gy: (x, y) => -2 * y * Math.exp(-((x - 1) ** 2 + y * y)) - 0.8 * (2 * (y - 1) / 0.6) * Math.exp(-((x + 1.3) ** 2 + (y - 1) ** 2) / 0.6),
    lv: [0.1, 0.25, 0.45, 0.65, 0.85], name: "언덕 둘 — 높이 f(x, y)", st: [-0.2, -1.6] },
  rosen: { f: (x, y) => (1 - x) ** 2 + 5 * (y - x * x) ** 2, gx: (x, y) => -2 * (1 - x) - 20 * x * (y - x * x), gy: (x, y) => 10 * (y - x * x),
    lv: [0.2, 1, 3, 8, 16, 30], name: "로젠브록 골짜기 (1 − x)² + 5(y − x²)²", st: [-1.6, 2.2] },
};
const box = (W = 360, H = 220) => plot({ x0: -3, x1: 3, y0: -2.6, y1: 2.6, W, H, pad: [10, 10, 18, 26] });

/* ── 등위선과 단면: y 를 고정한 단면의 기울기가 편미분 ── */
export function Contour({ p = {} }) {
  const S = SURF[p.fn] || SURF.bowl;
  const [yc, setY] = useState(p.y ?? 0.8);
  const clock = useClock({ period: 8 });
  const P = plot({ x0: -3, x1: 3, y0: -2.6, y1: 2.6, W: 200, H: 220, pad: [10, 8, 18, 24] });
  const xm = -2.5 + 5 * (0.5 - 0.5 * Math.cos((clock.t / 8) * 2 * Math.PI));
  const zs = [];
  for (let i = 0; i <= 120; i++) zs.push(S.f(-3 + i * 0.05, yc));
  const zmin = Math.min(...zs), zmax = Math.max(...zs);
  const Q = plot({ x0: -3, x1: 3, y0: zmin - 0.1 * (zmax - zmin + 0.2), y1: zmax + 0.1 * (zmax - zmin + 0.2), W: 360, H: 220, pad: [14, 10, 20, 236] });
  const slope = S.gx(xm, yc);
  return (
    <Frame clock={clock} title="등위선과 편미분"
      read={<>{S.name} · 왼쪽은 위에서 내려다본 등위선, 오른쪽은 y = {fmt(yc, 2)} 로 자른 단면. 단면의 접선 기울기가 ∂f/∂x = <b>{fmt(slope, 3)}</b> (x = {fmt(xm, 2)})</>}
      controls={<Slider label="단면 y" min={-2.4} max={2.4} step={0.05} value={yc} onChange={setY} />}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill={C.card} />
      {S.lv.map((c, i) => <path key={c} d={contourPath(P, S.f, c)} fill="none" stroke={C.sp} strokeWidth="1.3" opacity={0.45 + 0.1 * i} />)}
      <line x1={P.l} x2={P.r} y1={P.Y(yc)} y2={P.Y(yc)} stroke={C.red} strokeWidth="1.6" />
      <circle cx={P.X(xm)} cy={P.Y(yc)} r="4" fill={C.red} />
      <Axes p={Q} xl="x" yl="f" grid={false} />
      <path d={Q.path((x) => S.f(x, yc))} fill="none" stroke={C.red} strokeWidth="2" />
      <path d={Q.path((x) => S.f(xm, yc) + slope * (x - xm), xm - 0.8, xm + 0.8)} fill="none" stroke={C.green} strokeWidth="1.8" />
      <circle cx={Q.X(xm)} cy={Q.Y(S.f(xm, yc))} r="4" fill={C.red} />
    </Frame>
  );
}

/* ── 경사와 경사하강: 화살표는 가장 가파르게 오르는 방향, 등위선과 직각 ── */
export function Gradient({ p = {} }) {
  const S = SURF[p.fn] || SURF.bowl;
  const [lr, setLr] = useState(p.lr ?? (p.fn === "rosen" ? 0.02 : 0.12));
  const clock = useClock({ period: 9 });
  const P = box();
  const path = useMemo(() => {
    const pts = [[S.st[0], S.st[1]]];
    for (let i = 0; i < 160; i++) {
      const [x, y] = pts[pts.length - 1];
      const nx = x - lr * S.gx(x, y), ny = y - lr * S.gy(x, y);
      if (!Number.isFinite(nx) || Math.abs(nx) > 9 || Math.abs(ny) > 9) break;
      pts.push([nx, ny]);
    }
    return pts;
  }, [S, lr]);
  const k = Math.min(path.length - 1, Math.floor((clock.t / 8) * path.length));
  const arrows = [];
  for (let i = -2.5; i <= 2.51; i += 0.83) for (let j = -2.2; j <= 2.21; j += 0.73) {
    const gx = S.gx(i, j), gy = S.gy(i, j), L = Math.hypot(gx, gy) || 1, s = 0.32;
    arrows.push(<Arrow key={i + "," + j} x1={P.X(i)} y1={P.Y(j)} x2={P.X(i + (s * gx) / L)} y2={P.Y(j + (s * gy) / L)} color={C.mut} w={1} head={4} />);
  }
  const [cx, cy] = path[k];
  return (
    <Frame clock={clock} title="경사와 경사하강"
      read={<>{S.name} · 회색 화살표 = ∇f(오르막 방향, 등위선과 직각) · 붉은 점은 −∇f 쪽으로 한 걸음씩: 걸음 {k}번째 f = <b>{fmt(S.f(cx, cy), 4)}</b>{lr > 0.24 && p.fn !== "rosen" ? " — 걸음이 너무 크면 골짜기를 넘나들며 튄다" : ""}</>}
      controls={<Slider label="걸음 크기 η" min={0.005} max={p.fn === "rosen" ? 0.06 : 0.5} step={0.005} value={lr} onChange={setLr} show={(v) => fmt(v, 3)} />}>
      {S.lv.map((c, i) => <path key={c} d={contourPath(P, S.f, c)} fill="none" stroke={C.sp} strokeWidth="1.2" opacity={0.4 + 0.1 * i} />)}
      {arrows}
      <path d={P.poly(path.slice(0, k + 1))} fill="none" stroke={C.red} strokeWidth="1.8" />
      <circle cx={P.X(cx)} cy={P.Y(cy)} r="5" fill={C.red} />
    </Frame>
  );
}

/* ── 라그랑주: 원 g = x² + y² = 1 위에서 f 를 최대로 — 등위선이 원에 닿는 곳 ── */
const LG = {
  sum: { f: (x, y) => x + 2 * y, gx: () => 1, gy: () => 2, name: "f = x + 2y", lv: [-2.2, -1.5, -0.8, 0, 0.8, 1.5, 2.2] },
  prod: { f: (x, y) => x * y, gx: (x, y) => y, gy: (x) => x, name: "f = xy", lv: [-0.9, -0.5, -0.2, 0.2, 0.5, 0.9] },
};
export function Lagrange({ p = {} }) {
  const G = LG[p.fn] || LG.sum;
  const clock = useClock({ period: 10 });
  const P = plot({ x0: -2.2, x1: 2.2, y0: -1.5, y1: 1.5, pad: [8, 8, 16, 22] });
  const th = (clock.t / 10) * 2 * Math.PI;
  const x = Math.cos(th), y = Math.sin(th);
  const gfx = G.gx(x, y), gfy = G.gy(x, y), ggx = 2 * x, ggy = 2 * y;
  const cross = (gfx * ggy - gfy * ggx) / (Math.hypot(gfx, gfy) * Math.hypot(ggx, ggy) || 1);
  const tang = Math.abs(cross) < 0.05;
  const sc = 0.35;
  const Lf = Math.hypot(gfx, gfy) || 1, Lg = Math.hypot(ggx, ggy) || 1;
  return (
    <Frame clock={clock} title="라그랑주 승수"
      read={<>{G.name}, 조건 x² + y² = 1 · 점 ({fmt(x, 2)}, {fmt(y, 2)}) 에서 f = <b>{fmt(G.f(x, y), 3)}</b> · ∇f(파랑)와 ∇g(붉음)가 {tang ? <b>나란하다 → 극값 후보 (∇f = λ∇g)</b> : "나란하지 않으면 원을 따라 더 갈 여지가 있다"}</>}>
      {G.lv.map((c, i) => <path key={c} d={contourPath(P, G.f, c)} fill="none" stroke={C.sp} strokeWidth="1.2" opacity={0.35 + 0.08 * i} />)}
      <circle cx={P.X(0)} cy={P.Y(0)} r={P.X(1) - P.X(0)} fill="none" stroke={C.ink} strokeWidth="2" />
      <Arrow x1={P.X(x)} y1={P.Y(y)} x2={P.X(x + (sc * gfx) / Lf)} y2={P.Y(y + (sc * gfy) / Lf)} color={C.blue} w={2} />
      <Arrow x1={P.X(x)} y1={P.Y(y)} x2={P.X(x + (sc * ggx) / Lg)} y2={P.Y(y + (sc * ggy) / Lg)} color={C.red} w={2} />
      <circle cx={P.X(x)} cy={P.Y(y)} r="5" fill={tang ? C.green : C.ink} />
      <Label x={P.l + 4} y={P.t + 12} size={10.5}>등위선(색) · 조건 원(검정)</Label>
    </Frame>
  );
}

/* ── 이중적분: 칸을 잘게 → 부피의 합이 참값으로 ── */
export function DoubleInt({ p = {} }) {
  const f = (x, y) => 1 + x * y + 0.3 * x * x;          // [0,2] × [0,1]
  const exact = 2 + 1 + 0.8;                              // ∫₀² ∫₀¹ (1 + xy + 0.3x²) dy dx = 2 + 1 + 0.8
  const [auto, setAuto] = useState(true);
  const [nFix, setN] = useState(4);
  const clock = useClock({ period: 8 });
  const n = auto ? [1, 2, 3, 4, 6, 8, 12, 16, 24][Math.min(8, Math.floor((clock.t / 8) * 9))] : nFix;
  const P = plot({ x0: -0.1, x1: 2.1, y0: -0.1, y1: 1.1, pad: [10, 10, 18, 24] });
  const cells = [];
  let sum = 0, mx = 0;
  for (let i = 0; i < 2 * n; i++) for (let j = 0; j < n; j++) mx = Math.max(mx, f((i + 0.5) / n, (j + 0.5) / n));
  for (let i = 0; i < 2 * n; i++) for (let j = 0; j < n; j++) {
    const x = i / n, y = j / n, v = f(x + 0.5 / n, y + 0.5 / n);
    sum += v / (n * n);
    cells.push(<rect key={i + "-" + j} x={P.X(x)} y={P.Y(y + 1 / n)} width={P.X(x + 1 / n) - P.X(x)} height={P.Y(y) - P.Y(y + 1 / n)} fill={C.sp} opacity={0.12 + 0.75 * (v / mx)} stroke={C.card} strokeWidth={n > 12 ? 0 : 0.8} />);
  }
  return (
    <Frame clock={clock} title="이중적분과 칸 나누기"
      read={<>영역 [0, 2] × [0, 1] 을 {2 * n} × {n} 칸으로 — 칸마다 (가운데 높이 f) × (칸 넓이) 를 더하면 <b>{fmt(sum, 5)}</b> → 참값 <b>{fmt(exact, 5)}</b> · 진할수록 높다</>}
      controls={<>
        <Seg value={auto} onChange={setAuto} options={[[true, "저절로"], [false, "직접"]]} />
        {!auto && <Slider label="n" min={1} max={30} value={nFix} onChange={setN} />}
      </>}>
      {cells}
      <Axes p={P} grid={false} />
      <Label x={P.r - 4} y={P.t + 12} anchor="end" size={10.5}>f(x, y) = 1 + xy + 0.3x²</Label>
    </Frame>
  );
}

/* ── 벡터장: 알갱이가 흐름을 따라 간다 — 발산(퍼짐) · 회전(소용돌이) ── */
const FIELDS = {
  rot: { F: (x, y) => [-y, x], name: "F = (−y, x) — 회전 2, 발산 0", div: 0, curl: 2 },
  src: { F: (x, y) => [x, y], name: "F = (x, y) — 발산 2, 회전 0", div: 2, curl: 0 },
  shear: { F: (x, y) => [y, 0], name: "F = (y, 0) — 발산 0, 회전 −1 (층마다 속도가 다르다)", div: 0, curl: -1 },
  saddle: { F: (x, y) => [x, -y], name: "F = (x, −y) — 발산 0, 회전 0", div: 0, curl: 0 },
  sink: { F: (x, y) => [-x - y, x - y], name: "F = (−x − y, x − y) — 빨려 들며 돈다", div: -2, curl: 2 },
};
export function Field({ p = {} }) {
  const [kind, setKind] = useState(p.fn || "rot");
  const Fd = FIELDS[kind] || FIELDS.rot;
  const clock = useClock({ period: 6 });
  const P = plot({ x0: -3, x1: 3, y0: -2, y1: 2, pad: [8, 8, 8, 8] });
  const arrows = [];
  for (let i = -2.75; i <= 2.76; i += 0.5) for (let j = -1.75; j <= 1.76; j += 0.5) {
    const [u, v] = Fd.F(i, j), L = Math.hypot(u, v) || 1, s = 0.22 * Math.min(1.4, 0.5 + L / 3);
    arrows.push(<Arrow key={i + "," + j} x1={P.X(i)} y1={P.Y(j)} x2={P.X(i + (s * u) / L)} y2={P.Y(j + (s * v) / L)} color={C.mut} w={1} head={3.5} />);
  }
  // 알갱이: 격자에서 출발해 시간 t 만큼 흐른 자리(룽게-쿠타)
  const dots = [];
  const T = (clock.t % 6) * 0.35;
  for (let i = -2.5; i <= 2.51; i += 1) for (let j = -1.5; j <= 1.51; j += 1) {
    let x = i * 0.6, y = j * 0.6;
    const h = 0.02, N = Math.floor(T / h);
    for (let k = 0; k < N; k++) {
      const [a1, b1] = Fd.F(x, y), [a2, b2] = Fd.F(x + (h * a1) / 2, y + (h * b1) / 2);
      x += h * a2; y += h * b2;
      if (Math.abs(x) > 4 || Math.abs(y) > 3) break;
    }
    if (Math.abs(x) < 3 && Math.abs(y) < 2) dots.push(<circle key={i + "," + j} cx={P.X(x)} cy={P.Y(y)} r="3.5" fill={C.red} />);
  }
  return (
    <Frame clock={clock} title="벡터장의 흐름"
      read={<>{Fd.name} · 발산 div F = <b>{Fd.div}</b>(알갱이 무리가 퍼지면 +, 모이면 −) · 회전 curl F = <b>{Fd.curl}</b>(작은 바람개비가 도는 세기)</>}
      controls={<Seg value={kind} onChange={(k) => { setKind(k); clock.reset(); }} options={[["rot", "회전"], ["src", "샘"], ["sink", "소용돌이"], ["shear", "층밀림"], ["saddle", "안장"]]} />}>
      {arrows}
      {dots}
    </Frame>
  );
}

/* ── 내적과 정사영: a · b = |a||b| cos θ = (b 위로 드리운 a 의 그림자) × |b| ── */
export function DotProj({ p = {} }) {
  const clock = useClock({ period: 10 });
  const P = plot({ x0: -3.2, x1: 3.2, y0: -1.2, y1: 2.6, pad: [8, 8, 8, 8] });
  const th = (clock.t / 10) * 2 * Math.PI;
  const a = [2.2 * Math.cos(th), 2.2 * Math.sin(th)], b = [2.6, 0.6];
  const lb = Math.hypot(...b), dot = a[0] * b[0] + a[1] * b[1], k = dot / (lb * lb);
  const pr = [k * b[0], k * b[1]];
  const ang = (Math.acos(clamp(dot / (2.2 * lb), -1, 1)) * 180) / Math.PI;
  return (
    <Frame clock={clock} title="내적과 정사영"
      read={<>a · b = <b>{fmt(dot, 3)}</b> = |a||b| cos θ, θ = <b>{fmt(ang, 1)}°</b> — 90° 면 0(수직), 90° 보다 크면 음수. 초록 막대 = a 의 b 방향 그림자(정사영)</>}>
      <line x1={P.X(-3 * b[0] / lb)} y1={P.Y(-3 * b[1] / lb)} x2={P.X(3 * b[0] / lb)} y2={P.Y(3 * b[1] / lb)} stroke={C.bd} />
      <line x1={P.X(a[0])} y1={P.Y(a[1])} x2={P.X(pr[0])} y2={P.Y(pr[1])} stroke={C.mut} strokeDasharray="3 3" />
      <line x1={P.X(0)} y1={P.Y(0)} x2={P.X(pr[0])} y2={P.Y(pr[1])} stroke={C.green} strokeWidth="5" opacity="0.6" />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(b[0])} y2={P.Y(b[1])} color={C.blue} w={2.2} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(a[0])} y2={P.Y(a[1])} color={C.red} w={2.2} />
      <Label x={P.X(b[0]) + 4} y={P.Y(b[1])} color={C.blue} bold>b</Label>
      <Label x={P.X(a[0]) + 4} y={P.Y(a[1]) - 4} color={C.red} bold>a</Label>
    </Frame>
  );
}

/* ── 극좌표 넓이 요소: 작은 부채꼴 ≈ r Δr Δθ ── */
export function PolarArea({ p = {} }) {
  const clock = useClock({ period: 8 });
  const n = [2, 3, 4, 6, 8, 12, 16][Math.min(6, Math.floor((clock.t / 8) * 7))];
  const P = plot({ x0: -1.6, x1: 1.6, y0: -1.15, y1: 1.15, pad: [6, 6, 6, 6] });
  const R = 1, cells = [];
  const arc = (r, a0, a1) => `M${P.X(r * Math.cos(a0))} ${P.Y(r * Math.sin(a0))}A${(P.X(r) - P.X(0)).toFixed(1)} ${(P.X(r) - P.X(0)).toFixed(1)} 0 0 0 ${P.X(r * Math.cos(a1))} ${P.Y(r * Math.sin(a1))}`;
  let sum = 0;
  for (let i = 0; i < n; i++) for (let j = 0; j < 2 * n; j++) {
    const r0 = (i * R) / n, r1 = ((i + 1) * R) / n, a0 = (j * Math.PI) / n, a1 = ((j + 1) * Math.PI) / n;
    const rm = (r0 + r1) / 2;
    sum += rm * (R / n) * (Math.PI / n);
    cells.push(<path key={i + "-" + j} d={`${arc(r1, a0, a1)}L${P.X(r0 * Math.cos(a1))} ${P.Y(r0 * Math.sin(a1))}${r0 > 0 ? `A${(P.X(r0) - P.X(0)).toFixed(1)} ${(P.X(r0) - P.X(0)).toFixed(1)} 0 0 1 ${P.X(r0 * Math.cos(a0))} ${P.Y(r0 * Math.sin(a0))}` : ""}Z`}
      fill={C.sp} opacity={0.15 + 0.5 * ((i + 1) / n) * (0.6 + 0.4 * ((i + j) % 2))} stroke={C.card} strokeWidth="0.8" />);
  }
  return (
    <Frame clock={clock} title="극좌표의 넓이 요소"
      read={<>반지름을 {n}칸, 각을 {2 * n}칸으로 — 조각 넓이 ≈ r · Δr · Δθ(바깥 조각일수록 크다). 다 더하면 <b>{fmt(sum, 5)}</b> → 원 넓이 π = <b>{fmt(Math.PI, 5)}</b>. 그래서 dA = r dr dθ</>}>
      {cells}
      <circle cx={P.X(0)} cy={P.Y(0)} r={P.X(1) - P.X(0)} fill="none" stroke={C.ink} strokeWidth="1.5" />
      <line x1={P.X(0)} y1={P.Y(0)} x2={P.X(lerp(0, 1, 1))} y2={P.Y(0)} stroke={C.ink} />
    </Frame>
  );
}
