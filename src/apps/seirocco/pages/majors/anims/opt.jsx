// 최적화 그림 — 임계점(극소 · 안장 · 극대) · 볼록 함수와 현 · 선 탐색(아르미호)과 지그재그 · 경사하강 · 뉴턴 · BFGS 비교 · KKT 조건 · 장벽법과 중심 경로 · 분지한정 · 담금질 기법
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, fmt, clamp, sup, rng, gauss, useClock } from "./kit.jsx";
import { contourPath } from "./mvc.jsx";

const star = (X, Y, R) => Array.from({ length: 10 }, (_, k) => { const a = -Math.PI / 2 + (k * Math.PI) / 5, r = k % 2 ? R * 0.43 : R; return `${(X + r * Math.cos(a)).toFixed(1)},${(Y + r * Math.sin(a)).toFixed(1)}`; }).join(" ");
const eig2 = (H) => { const m = (H[0][0] + H[1][1]) / 2, r = Math.hypot((H[0][0] - H[1][1]) / 2, H[0][1]); return [m - r, m + r]; };
const sci = (v) => {
  if (!Number.isFinite(v)) return "—";
  if (v === 0) return "0";
  const e = Math.floor(Math.log10(Math.abs(v)));
  if (e >= -2 && e <= 3) return fmt(v, 3);
  return `${fmt(v / 10 ** e, 2)} × 10${sup(e)}`;
};

/* ── 임계점: 기울기가 0 인 점을 헤세 행렬의 고윳값으로 가른다 ── */
const HB = { f: (x, y) => (x * x + y - 11) ** 2 + (x + y * y - 7) ** 2 };
HB.g = (x, y) => [4 * x * (x * x + y - 11) + 2 * (x + y * y - 7), 2 * (x * x + y - 11) + 4 * y * (x + y * y - 7)];
HB.H = (x, y) => [[12 * x * x + 4 * y - 42, 4 * x + 4 * y], [4 * x + 4 * y, 4 * x + 12 * y * y - 26]];
const polish = (S, p) => { let [x, y] = p; for (let i = 0; i < 25; i++) { const g = S.g(x, y), H = S.H(x, y), D = H[0][0] * H[1][1] - H[0][1] * H[1][0]; x -= (H[1][1] * g[0] - H[0][1] * g[1]) / D; y -= (H[0][0] * g[1] - H[1][0] * g[0]) / D; } return [x, y]; };
const CPF = {
  mixed: { name: "f = x³ − 3x + y²", f: (x, y) => x ** 3 - 3 * x + y * y, g: (x, y) => [3 * x * x - 3, 2 * y], H: (x) => [[6 * x, 0], [0, 2]],
    box: [-2.4, 2.4, -2.26, 2.26], lv: [-3, -1.6, -1, 0, 1, 2, 3, 4.5, 6], pts: [[1, 0], [-1, 0]], path: (u) => [1.9 * Math.cos(u), 1.15 * Math.sin(2 * u)],
    note: "(1, 0) 은 극소지만 전역 최소는 아니다 — 왼쪽으로 가면 f 가 끝없이 작아진다" },
  himmel: { name: "힘멜블라우 함수", ...HB, box: [-5, 5, -4.7, 4.7], lv: [2, 10, 30, 60, 100, 150, 220, 320],
    pts: [[3, 2], [-2.8, 3.1], [-3.78, -3.28], [3.58, -1.85], [-0.27, -0.92], [0.09, 2.88], [-3.07, -0.08], [3.39, 0.07], [-0.13, -1.95]].map((p) => polish(HB, p)),
    path: (u) => [3.55 * Math.cos(u), 3.3 * Math.sin(u)], note: "극소가 넷(모두 f = 0 — 전역 최소가 여럿), 극대 하나, 안장점 넷" },
};
const kindOf = (ev) => (ev[0] > 0 ? "min" : ev[1] < 0 ? "max" : "saddle");
const KNAME = { min: "극소", max: "극대", saddle: "안장점" };
export function CritPt({ p = {} }) {
  const [k, setK] = useState(CPF[p.fn] ? p.fn : "mixed");
  const S = CPF[k];
  const clock = useClock({ period: 16, rest: 3.2 });
  const P = plot({ x0: S.box[0], x1: S.box[1], y0: S.box[2], y1: S.box[3], W: 360, H: 220, pad: [10, 132, 18, 24] });
  const lines = useMemo(() => S.lv.map((c) => contourPath(P, S.f, c, 56)), [k]);
  const crit = useMemo(() => S.pts.map((q) => { const ev = eig2(S.H(q[0], q[1])); return { q, ev, kind: kindOf(ev) }; }), [k]);
  const [px, py] = S.path((clock.t / 16) * 2 * Math.PI + 0.4);
  const g = S.g(px, py), gn = Math.hypot(g[0], g[1]) || 1;
  const near = crit.reduce((b, c) => (Math.hypot(c.q[0] - px, c.q[1] - py) < Math.hypot(b.q[0] - px, b.q[1] - py) ? c : b), crit[0]);
  const fp = S.f(px, py);
  const lvl = contourPath(P, S.f, fp, 56);
  const cnt = { min: 0, saddle: 0, max: 0 }; crit.forEach((c) => { cnt[c.kind] += 1; });
  const mark = (c, i) => {
    const X = P.X(c.q[0]), Y = P.Y(c.q[1]);
    if (c.kind === "min") return <circle key={i} cx={X} cy={Y} r="4.2" fill={C.green} stroke={C.card} strokeWidth="1" />;
    if (c.kind === "max") return <polygon key={i} points={`${X},${Y - 5} ${X - 4.6},${Y + 3.6} ${X + 4.6},${Y + 3.6}`} fill={C.red} />;
    return <g key={i} stroke={C.gold} strokeWidth="2.2"><line x1={X - 4} y1={Y - 4} x2={X + 4} y2={Y + 4} /><line x1={X - 4} y1={Y + 4} x2={X + 4} y2={Y - 4} /></g>;
  };
  const lx = P.r + 12;
  return (
    <Frame clock={clock} title="임계점 — 극소 · 안장 · 극대"
      read={<>{S.name} · 탐침 점 ({fmt(px, 2)}, {fmt(py, 2)}) 에서 |∇f| = {fmt(gn, 2)} — 화살표 −∇f 는 가장 빨리 내려가는 쪽이고, 그 점을 지나는 등위선(노란 점선)과 직각이다 · 임계점(∇f = 0)은 헤세 행렬의 고윳값으로 가른다: 둘 다 양수면 극소, 둘 다 음수면 극대, 부호가 다르면 안장점 · 가장 가까운 임계점 ({fmt(near.q[0], 2)}, {fmt(near.q[1], 2)}): 고윳값 {fmt(near.ev[0], 1)}, {fmt(near.ev[1], 1)} → <b>{KNAME[near.kind]}</b> · {S.note}</>}
      controls={<Seg value={k} onChange={setK} options={[["mixed", "x³ − 3x + y²"], ["himmel", "힘멜블라우"]]} />}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill="none" stroke={C.bd} />
      {lines.map((d, i) => <path key={i} d={d} fill="none" stroke={C.sp} strokeWidth="1.1" opacity={0.35 + (0.5 * i) / lines.length} />)}
      <path d={lvl} fill="none" stroke={C.gold} strokeWidth="1.4" strokeDasharray="4 3" />
      {crit.map(mark)}
      <Arrow x1={P.X(px)} y1={P.Y(py)} x2={P.X(px) - (24 * g[0]) / gn} y2={P.Y(py) + (24 * g[1]) / gn} color={C.red} w={2} />
      <circle cx={P.X(px)} cy={P.Y(py)} r="3.6" fill={C.ink} />
      <g fontSize="10" fill={C.ink}>
        <circle cx={lx + 5} cy={30} r="4" fill={C.green} /><text x={lx + 14} y={34}>극소 {cnt.min}</text>
        <g stroke={C.gold} strokeWidth="2"><line x1={lx + 1.5} y1={47.5} x2={lx + 8.5} y2={54.5} /><line x1={lx + 1.5} y1={54.5} x2={lx + 8.5} y2={47.5} /></g><text x={lx + 14} y={55}>안장점 {cnt.saddle}</text>
        <polygon points={`${lx + 5},${67} ${lx + 0.8},${75} ${lx + 9.2},${75}`} fill={C.red} /><text x={lx + 14} y={76}>극대 {cnt.max}</text>
        <line x1={lx} x2={lx + 10} y1={93} y2={93} stroke={C.gold} strokeDasharray="4 3" strokeWidth="1.4" /><text x={lx + 14} y={97}>지금 높이의 등위선</text>
        <line x1={lx} x2={lx + 10} y1={113} y2={113} stroke={C.red} strokeWidth="2" /><text x={lx + 14} y={117}>−∇f (내리막)</text>
        <text x={lx} y={146} fill={C.mut}>f(탐침) = {fmt(fp, 2)}</text>
        <text x={lx} y={162} fill={C.mut}>가까운 임계점:</text>
        <text x={lx} y={178} fontWeight="800" fill={near.kind === "min" ? C.green : near.kind === "max" ? C.red : C.gold}>{KNAME[near.kind]} (λ {fmt(near.ev[0], 1)}, {fmt(near.ev[1], 1)})</text>
      </g>
    </Frame>
  );
}

/* ── 볼록 함수: 두 점을 잇는 현이 늘 그래프 위에 있다 ── */
const CVF = {
  sq: { name: "f = x²", f: (x) => x * x, y: [-0.5, 3.4], convex: true, mins: [0] },
  w: { name: "f = x⁴ − 2x² + 0.5x", f: (x) => x ** 4 - 2 * x * x + 0.5 * x, y: [-1.9, 4.4], convex: false, mins: [-1.0578, 0.9297] },
  abs: { name: "f = |x| + 0.3x", f: (x) => Math.abs(x) + 0.3 * x, y: [-0.4, 2.6], convex: true, mins: [0] },
};
export function Convex({ p = {} }) {
  const [k, setK] = useState(CVF[p.fn] ? p.fn : "w");
  const S = CVF[k];
  const clock = useClock({ period: 14, rest: 0.3 });
  const P = plot({ x0: -1.75, x1: 1.75, y0: S.y[0], y1: S.y[1], pad: [12, 12, 22, 30] });
  const u = (clock.t / 14) * 2 * Math.PI;
  const m = 0.95 * Math.sin(u), w = 0.62 + 0.22 * Math.cos(2 * u + 0.5);
  const a = clamp(m - w, -1.7, 1.7), b = clamp(m + w, -1.7, 1.7);
  const fa = S.f(a), fb = S.f(b), ch = (x) => fa + ((fb - fa) * (x - a)) / (b - a);
  const N = 60, xs = Array.from({ length: N + 1 }, (_, i) => a + ((b - a) * i) / N);
  const runs = []; let cur = null;
  xs.forEach((x) => { if (S.f(x) > ch(x) + 1e-9) { if (!cur) { cur = []; runs.push(cur); } cur.push(x); } else cur = null; });
  const bad = runs.length > 0;
  const xm = (a + b) / 2, fm = S.f(xm), cm = (fa + fb) / 2;
  const region = [...xs.map((x) => [x, ch(x)]), ...xs.slice().reverse().map((x) => [x, S.f(x)])];
  return (
    <Frame clock={clock} title="볼록 함수 — 현은 늘 그래프 위에"
      read={<>{S.name} · 두 점 a = {fmt(a, 2)}, b = {fmt(b, 2)} 를 잇는 현(노랑) · 가운데에서 현의 높이 (f(a) + f(b)) ÷ 2 = {fmt(cm, 3)}, 그래프의 높이 f((a + b) ÷ 2) = {fmt(fm, 3)} — {bad ? <b>현이 그래프 아래로 들어간 곳이 있다(빨강)</b> : "현이 그래프 위에 있다"} · {S.convex ? "어느 두 점을 골라도 현이 위에 있으면 볼록 — 볼록 함수는 극소가 곧 최소라, 내리막만 따라가도 최솟값에 닿는다" : "볼록이 아니어서 극소가 둘(초록) — 내리막만 따라가면 출발점에 따라 다른 골짜기에 갇힌다"}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["sq", "x²"], ["w", "x⁴ − 2x² + 0.5x"], ["abs", "|x| + 0.3x"]]} />}>
      <Axes p={P} grid={false} xt={[-1, 1]} yt={S.y[1] > 4 ? [2, 4] : [1, 2, 3].filter((v) => v < S.y[1])} />
      <path d={P.poly(region)} fill={C.green} opacity="0.14" />
      {runs.map((r, i) => <path key={i} d={P.poly([...r.map((x) => [x, S.f(x)]), ...r.slice().reverse().map((x) => [x, ch(x)])])} fill={C.red} opacity="0.35" />)}
      <path d={P.path(S.f, -1.75, 1.75, 240)} fill="none" stroke={C.blue} strokeWidth="2.2" />
      <line x1={P.X(a)} y1={P.Y(fa)} x2={P.X(b)} y2={P.Y(fb)} stroke={C.gold} strokeWidth="2" />
      {[[a, fa], [b, fb]].map(([x, y], i) => <circle key={i} cx={P.X(x)} cy={P.Y(y)} r="3.6" fill={C.gold} />)}
      <line x1={P.X(xm)} x2={P.X(xm)} y1={P.Y(cm)} y2={P.Y(fm)} stroke={bad && fm > cm ? C.red : C.mut} strokeWidth="1.2" strokeDasharray="3 2" />
      <circle cx={P.X(xm)} cy={P.Y(cm)} r="3" fill={C.gold} stroke={C.card} />
      <circle cx={P.X(xm)} cy={P.Y(fm)} r="3" fill={C.blue} stroke={C.card} />
      {S.mins.map((x) => <circle key={x} cx={P.X(x)} cy={P.Y(S.f(x))} r="4.2" fill="none" stroke={C.green} strokeWidth="2" />)}
      <Label x={P.l + 6} y={P.t + 10} color={S.convex ? C.green : C.red} size={10.5} bold bg>{S.convex ? "볼록" : "볼록 아님"}</Label>
    </Frame>
  );
}

/* ── 선 탐색: 아르미호 조건으로 걸음을 반씩 줄이기 · 길쭉한 골짜기의 지그재그 ── */
const PHI = (a) => 1 - 2 * a + 2.5 * a * a + 0.8 * a ** 3;
const TRY = [1, 0.5, 0.25];
const ZZ = (kap) => {
  let x = [kap, 1]; const f = (q) => 0.5 * (q[0] * q[0] + kap * q[1] * q[1]); const f0 = f(x); const pts = [x], fs = [1];
  for (let i = 0; i < 140 && f(x) > 1e-7 * f0; i++) {
    const g = [x[0], kap * x[1]], gg = g[0] * g[0] + g[1] * g[1], gAg = g[0] * g[0] + kap * g[1] * g[1];
    const al = gg / gAg; x = [x[0] - al * g[0], x[1] - al * g[1]]; pts.push(x); fs.push(f(x) / f0);
  }
  return { pts, fs };
};
export function LineSearch({ p = {} }) {
  const [mode, setMode] = useState(["armijo", "zigzag"].includes(p.mode) ? p.mode : "armijo");
  const [kap, setKap] = useState(clamp(p.kap ?? 10, 1, 30));
  const Z = useMemo(() => ZZ(kap), [kap]);
  const clock = useClock({ period: mode === "armijo" ? 9 : 13, rest: mode === "armijo" ? 6 : 10 });
  if (mode === "armijo") {
    const P = plot({ x0: 0, x1: 1.08, y0: 0, y1: 2.6, pad: [12, 14, 26, 30] });
    const step = Math.min(TRY.length, Math.floor(clock.t / 1.6));
    const arm = (a) => 1 - 0.6 * a;
    const rows = TRY.slice(0, step).map((a) => ({ a, phi: PHI(a), lim: arm(a), ok: PHI(a) <= arm(a) }));
    return (
      <Frame clock={clock} title="선 탐색 — 아르미호 조건과 되돌아가기"
        read={<>φ(α) = f(x + αd) — 내리막 방향 d 로 α 만큼 갔을 때의 값(파랑) · 아르미호 조건: φ(α) ≤ φ(0) + c α φ′(0), c = 0.3 (노란 선 아래면 ‘충분히 내려갔다’) · {rows.length ? rows.map((r) => `α = ${fmt(r.a, 2)}: φ = ${fmt(r.phi, 3)} ${r.ok ? "≤" : ">"} ${fmt(r.lim, 2)} ${r.ok ? "✓ 받아들인다" : "✗ 반으로"}`).join(" · ") : "α = 1 부터 시험한다"} · 큰 걸음은 되레 올라가고(✗), 조건을 만족하는 첫 걸음에서 멈추면 너무 작은 걸음도 피한다</>}
        controls={<Seg value={mode} onChange={(v) => { setMode(v); clock.reset(); }} options={[["armijo", "아르미호"], ["zigzag", "지그재그"]]} />}>
        <Axes p={P} xl="α" yl="φ" grid={false} xt={[0.25, 0.5, 1]} yt={[1, 2]} />
        <path d={P.poly([[0, 1], [0.5, 0]])} fill="none" stroke={C.mut} strokeWidth="1.1" strokeDasharray="4 3" />
        <path d={P.poly([[0, 1], [1.08, 1 - 0.6 * 1.08], [1.08, 0], [0, 0]])} fill={C.gold} opacity="0.1" />
        <line x1={P.X(0)} y1={P.Y(1)} x2={P.X(1.08)} y2={P.Y(arm(1.08))} stroke={C.gold} strokeWidth="1.8" />
        <path d={P.path(PHI, 0, 1.08, 160)} fill="none" stroke={C.blue} strokeWidth="2.2" />
        {rows.map((r) => (
          <g key={r.a}>
            <line x1={P.X(r.a)} x2={P.X(r.a)} y1={P.Y(0)} y2={P.Y(Math.min(2.6, r.phi))} stroke={r.ok ? C.green : C.red} strokeWidth="1.2" strokeDasharray="3 2" />
            <circle cx={P.X(r.a)} cy={P.Y(Math.min(2.6, r.phi))} r="4.5" fill={r.ok ? C.green : C.red} />
            <text x={P.X(r.a) + 7} y={P.Y(Math.min(2.6, r.phi)) + 4} fontSize="11" fontWeight="800" fill={r.ok ? C.green : C.red}>{r.ok ? "✓" : "✗"}</text>
          </g>
        ))}
        <Label x={P.X(0.5) + 2} y={P.Y(0.06)} color={C.mut} size={9.5}>접선 φ(0) + αφ′(0)</Label>
        <Label x={P.X(0.66)} y={P.Y(arm(0.66)) - 6} color={C.gold} size={9.5} bg>φ(0) + 0.3αφ′(0)</Label>
      </Frame>
    );
  }
  const n = Math.min(Z.pts.length - 1, Math.floor(clock.t / 0.28));
  const R = 1.08 * Math.sqrt(kap * kap + kap), wl = 200, hl = 196, Ry = (R * hl) / wl;
  const P = plot({ x0: -R, x1: R, y0: -Ry, y1: Ry, W: 360, H: 220, pad: [10, 360 - 10 - wl, 14, 10] });
  const f0 = 0.5 * (kap * kap + kap), lv = [1, 0.45, 0.18, 0.06, 0.015].map((r) => r * f0);
  const G = plot({ x0: 0, x1: Math.max(10, Z.fs.length - 1), y0: -7, y1: 0.3, W: 360, H: 220, pad: [18, 10, 30, 248] });
  const r = ((kap - 1) / (kap + 1)) ** 2, need = r > 0 ? Math.ceil(Math.log(1e-6) / Math.log(r)) : 1;
  return (
    <Frame clock={clock} title="선 탐색 — 길쭉한 골짜기의 지그재그"
      read={<>f = ½(x² + κy²), κ = {kap} — 등위선이 길쭉할수록 내리막 방향 −∇f 가 골짜기의 바닥(원점)을 비껴간다 · 걸음마다 정확한 선 탐색을 해도 이웃한 두 걸음이 늘 직각으로 꺾여 지그재그 · 매 걸음 f 가 ((κ − 1) ÷ (κ + 1))² = <b>{fmt(r, 3)}</b> 배 → f 를 10⁻⁶ 배로 줄이는 데 <b>{need}</b> 걸음 · κ = 1(동그란 등위선)이면 한 걸음에 끝난다 — 뉴턴법과 전처리는 등위선을 둥글게 만드는 일이다</>}
      controls={<>
        <Seg value={mode} onChange={(v) => { setMode(v); clock.reset(); }} options={[["armijo", "아르미호"], ["zigzag", "지그재그"]]} />
        <Slider label="κ" min={1} max={30} step={1} value={kap} onChange={(v) => { setKap(v); clock.reset(); }} />
      </>}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill="none" stroke={C.bd} />
      {lv.map((c) => <ellipse key={c} cx={P.X(0)} cy={P.Y(0)} rx={P.X(Math.sqrt(2 * c)) - P.X(0)} ry={P.Y(0) - P.Y(Math.sqrt((2 * c) / kap))} fill="none" stroke={C.sp} strokeWidth="1" opacity="0.6" />)}
      <path d={P.poly(Z.pts.slice(0, n + 1))} fill="none" stroke={C.red} strokeWidth="1.6" />
      {Z.pts.slice(0, n + 1).map((q, i) => <circle key={i} cx={P.X(q[0])} cy={P.Y(q[1])} r={i === n ? 3.6 : 2} fill={C.red} />)}
      <circle cx={P.X(0)} cy={P.Y(0)} r="3" fill={C.green} />
      <g fontSize="9.5" fill={C.mut}>
        <line x1={G.l} x2={G.r} y1={G.b} y2={G.b} stroke={C.mut} strokeWidth="1.1" />
        <line x1={G.l} x2={G.l} y1={G.t} y2={G.b} stroke={C.mut} strokeWidth="1.1" />
        {[0, -3, -6].map((v) => <g key={v}><line x1={G.l} x2={G.r} y1={G.Y(v)} y2={G.Y(v)} stroke={C.bd} strokeWidth="0.7" /><text x={G.l - 3} y={G.Y(v) + 3.5} textAnchor="end">{v === 0 ? "1" : "10" + sup(v)}</text></g>)}
        {[0, G.x1].map((v) => <text key={v} x={G.X(v)} y={G.b + 12} textAnchor="middle">{fmt(v, 0)}</text>)}
        <text x={G.r} y={G.b + 22} textAnchor="end" fill={C.ink} fontStyle="italic">걸음</text>
        <text x={G.l + 2} y={G.t - 5} fill={C.ink}>f ÷ f₀ (로그 눈금)</text>
      </g>
      <path d={G.poly(Z.fs.slice(0, n + 1).map((v, i) => [i, Math.max(-7, Math.log10(Math.max(1e-12, v)))]))} fill="none" stroke={C.red} strokeWidth="1.8" />
    </Frame>
  );
}

/* ── 로젠브록 골짜기: 경사하강 · 뉴턴 · BFGS ── */
const RF = (x, y) => (1 - x) ** 2 + 100 * (y - x * x) ** 2;
const RG = (x, y) => [-2 * (1 - x) - 400 * x * (y - x * x), 200 * (y - x * x)];
const RH = (x, y) => [[2 - 400 * (y - x * x) + 800 * x * x, -400 * x], [-400 * x, 200]];
const solve2 = (H, g) => { const D = H[0][0] * H[1][1] - H[0][1] * H[1][0]; return [(H[1][1] * g[0] - H[0][1] * g[1]) / D, (H[0][0] * g[1] - H[1][0] * g[0]) / D]; };
function rosenRun(kind, K = 40) {
  let x = [-1.2, 1], Hi = [[1, 0], [0, 1]]; const out = [x];
  for (let k = 0; k < K; k++) {
    const g = RG(x[0], x[1]), f0 = RF(x[0], x[1]);
    let d;
    if (kind === "gd") d = [-g[0], -g[1]];
    else if (kind === "newton") {
      const H = RH(x[0], x[1]), lo = eig2(H)[0], s = lo <= 1e-6 ? 1e-3 - lo : 0;
      const q = solve2([[H[0][0] + s, H[0][1]], [H[1][0], H[1][1] + s]], g); d = [-q[0], -q[1]];
    } else d = [-(Hi[0][0] * g[0] + Hi[0][1] * g[1]), -(Hi[1][0] * g[0] + Hi[1][1] * g[1])];
    const gd = g[0] * d[0] + g[1] * d[1];
    let a = 1, xn = x;
    if (kind === "gd") xn = [x[0] + 0.001 * d[0], x[1] + 0.001 * d[1]];   // 경사하강은 안정한 고정 걸음(곡률 최대 약 1000 → 걸음 < 0.002)
    else for (let j = 0; j < 60; j++) { const z = [x[0] + a * d[0], x[1] + a * d[1]]; if (RF(z[0], z[1]) <= f0 + 1e-4 * a * gd) { xn = z; break; } a *= 0.5; }
    if (kind === "bfgs") {
      const s = [xn[0] - x[0], xn[1] - x[1]], gn = RG(xn[0], xn[1]), y = [gn[0] - g[0], gn[1] - g[1]], sy = s[0] * y[0] + s[1] * y[1];
      if (sy > 1e-12) {
        const r = 1 / sy;
        if (k === 0) { const c = sy / (y[0] * y[0] + y[1] * y[1]); Hi = [[c, 0], [0, c]]; }
        const Hy = [Hi[0][0] * y[0] + Hi[0][1] * y[1], Hi[1][0] * y[0] + Hi[1][1] * y[1]], yHy = y[0] * Hy[0] + y[1] * Hy[1];
        Hi = [0, 1].map((i) => [0, 1].map((j) => Hi[i][j] - r * (Hy[i] * s[j] + s[i] * Hy[j]) + (r * r * yHy + r) * s[i] * s[j]));
      }
    }
    x = xn; out.push(x);
  }
  return out;
}
const RUNS = { gd: rosenRun("gd"), bfgs: rosenRun("bfgs"), newton: rosenRun("newton") };
const RCOL = { gd: C.gold, bfgs: C.violet, newton: C.red };
const RNAME = { gd: "경사하강", bfgs: "BFGS", newton: "뉴턴" };
export function NewtonOpt({ p = {} }) {
  const [hl, setHl] = useState(["all", "gd", "bfgs", "newton"].includes(p.show) ? p.show : "all");
  const clock = useClock({ period: 16, rest: 13 });
  const k = Math.min(40, Math.floor(clock.t / 0.34));
  const P = plot({ x0: -1.7, x1: 1.5, y0: -0.45, y1: 1.75, W: 360, H: 220, pad: [10, 150, 18, 24] });
  const lines = useMemo(() => [0.05, 0.4, 2, 8, 30, 100, 300].map((c) => contourPath(P, RF, c, 64)), []);
  const G = plot({ x0: 0, x1: 40, y0: -16, y1: 2, W: 360, H: 220, pad: [18, 10, 30, 244] });
  const lf = (q) => clamp(Math.log10(Math.max(1e-16, RF(q[0], q[1]))), -16, 2);
  const on = (m) => hl === "all" || hl === m;
  return (
    <Frame clock={clock} title="경사하강 · 뉴턴 · BFGS — 로젠브록 골짜기"
      read={<>f = (1 − x)² + 100(y − x²)², 출발 (−1.2, 1), 최솟값 (1, 1) 에서 0 · {k} 번 반복 뒤 f: 경사하강 {sci(RF(...RUNS.gd[k]))}, BFGS {sci(RF(...RUNS.bfgs[k]))}, 뉴턴 {sci(RF(...RUNS.newton[k]))} · 경사하강(걸음 0.001)은 휘어진 좁은 골짜기를 따라 기어가 10⁻⁸ 에 닿는 데 약 2 만 번이 걸리고, 뉴턴은 곡률(헤세 행렬)을 써서 약 20 번, BFGS 는 기울기의 변화만으로 곡률을 배워 약 35 번 만에 10⁻¹⁰ 아래로 내려간다(오른쪽 = 반복마다 f, 로그 눈금)</>}
      controls={<Seg value={hl} onChange={setHl} options={[["all", "모두"], ["gd", "경사하강"], ["bfgs", "BFGS"], ["newton", "뉴턴"]]} />}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill="none" stroke={C.bd} />
      {lines.map((d, i) => <path key={i} d={d} fill="none" stroke={C.sp} strokeWidth="1" opacity={0.3 + 0.08 * i} />)}
      <circle cx={P.X(1)} cy={P.Y(1)} r="4" fill="none" stroke={C.green} strokeWidth="2" />
      <circle cx={P.X(-1.2)} cy={P.Y(1)} r="3" fill={C.ink} />
      {["gd", "bfgs", "newton"].map((m) => <path key={"g" + m} d={P.poly(RUNS[m])} fill="none" stroke={RCOL[m]} strokeWidth="1" opacity={on(m) ? 0.22 : 0.08} />)}
      {["gd", "bfgs", "newton"].map((m) => (
        <g key={m} opacity={on(m) ? 1 : 0.18}>
          <path d={P.poly(RUNS[m].slice(0, k + 1))} fill="none" stroke={RCOL[m]} strokeWidth="1.6" />
          <circle cx={P.X(RUNS[m][k][0])} cy={P.Y(RUNS[m][k][1])} r="3.4" fill={RCOL[m]} />
        </g>
      ))}
      <g fontSize="9.5" fill={C.mut}>
        <line x1={G.l} x2={G.r} y1={G.b} y2={G.b} stroke={C.mut} strokeWidth="1.1" />
        <line x1={G.l} x2={G.l} y1={G.t} y2={G.b} stroke={C.mut} strokeWidth="1.1" />
        {[0, -5, -10, -15].map((v) => <g key={v}><line x1={G.l} x2={G.r} y1={G.Y(v)} y2={G.Y(v)} stroke={C.bd} strokeWidth="0.7" /><text x={G.l - 3} y={G.Y(v) + 3.5} textAnchor="end">{v === 0 ? "1" : "10" + sup(v)}</text></g>)}
        {[0, 20, 40].map((v) => <text key={v} x={G.X(v)} y={G.b + 12} textAnchor="middle">{v}</text>)}
        <text x={G.r} y={G.b + 22} textAnchor="end" fill={C.ink} fontStyle="italic">반복</text>
        <text x={G.l + 2} y={G.t - 5} fill={C.ink}>f (로그 눈금)</text>
      </g>
      {["gd", "bfgs", "newton"].map((m) => <path key={"h" + m} d={G.poly(RUNS[m].map((q, j) => [j, lf(q)]))} fill="none" stroke={RCOL[m]} strokeWidth="1" opacity={on(m) ? 0.22 : 0.08} />)}
      {["gd", "bfgs", "newton"].map((m, i) => (
        <g key={m} opacity={on(m) ? 1 : 0.18}>
          <path d={G.poly(RUNS[m].slice(0, k + 1).map((q, j) => [j, lf(q)]))} fill="none" stroke={RCOL[m]} strokeWidth="1.8" />
          <text x={G.l + 6} y={G.Y(-9.5) + 12 * i} fontSize="9.5" fontWeight="800" fill={RCOL[m]}>{RNAME[m]}</text>
        </g>
      ))}
    </Frame>
  );
}

/* ── KKT: 원판과 반평면 안에서 목표점에 가장 가까운 점 ── */
const feas = (q) => q[0] * q[0] + q[1] * q[1] <= 1 + 1e-12 && q[0] + q[1] <= 1 + 1e-12;
function kktSolve(T) {
  if (feas(T)) return { x: T, act: [], mu: [0, 0] };
  const cand = [];
  const r = Math.hypot(T[0], T[1]), d1 = [T[0] / r, T[1] / r];
  if (d1[0] + d1[1] <= 1 + 1e-12) cand.push({ x: d1, act: [1] });
  const s = (T[0] + T[1] - 1) / 2, q = [T[0] - s, T[1] - s];
  if (q[0] * q[0] + q[1] * q[1] <= 1 + 1e-12) cand.push({ x: q, act: [2] });
  cand.push({ x: [1, 0], act: [1, 2] }, { x: [0, 1], act: [1, 2] });
  const best = cand.reduce((b, c) => (Math.hypot(c.x[0] - T[0], c.x[1] - T[1]) < Math.hypot(b.x[0] - T[0], b.x[1] - T[1]) - 1e-12 ? c : b), cand[0]);
  const g = [2 * (T[0] - best.x[0]), 2 * (T[1] - best.x[1])];
  let mu = [0, 0];
  if (best.act.length === 2) { const a = 2 * best.x[0], c = 2 * best.x[1], D = a - c; mu = [(g[0] - g[1]) / D, (a * g[1] - c * g[0]) / D]; }
  else if (best.act[0] === 1) mu = [(g[0] * best.x[0] + g[1] * best.x[1]) / 2, 0];
  else mu = [0, (g[0] + g[1]) / 2];
  return { ...best, mu };
}
export function KKT() {
  const clock = useClock({ period: 18, rest: 1.26 });
  const u = (clock.t / 18) * 2 * Math.PI, th = u - 0.6 * Math.sin(u), rr = 1.05 + 0.62 * Math.sin(2 * th + 0.9);
  const T = [rr * Math.cos(th), rr * Math.sin(th)];
  const S = kktSolve(T);
  const P = plot({ x0: -1.9, x1: 1.9, y0: -2.02, y1: 2.02, W: 360, H: 220, pad: [8, 160, 8, 8] });
  const arc = Array.from({ length: 91 }, (_, i) => { const a = Math.PI / 2 + (i / 90) * 1.5 * Math.PI; return [Math.cos(a), Math.sin(a)]; });
  const sc = 0.32, X0 = P.X(S.x[0]), Y0 = P.Y(S.x[1]);
  const v = (w) => [X0 + (w[0] * sc * (P.X(1) - P.X(0))), Y0 - (w[1] * sc * (P.X(1) - P.X(0)))];
  const nf = [2 * (T[0] - S.x[0]), 2 * (T[1] - S.x[1])], n1 = [S.mu[0] * 2 * S.x[0], S.mu[0] * 2 * S.x[1]], n2 = [S.mu[1], S.mu[1]];
  const rad = Math.hypot(T[0] - S.x[0], T[1] - S.x[1]);
  const act = S.act.length === 0 ? "활성 제약 없음 — 목표가 영역 안이라 그 점이 바로 답(∇f = 0)" : S.act.length === 2 ? "두 제약이 모두 활성 — 모서리 (꼭짓점)" : S.act[0] === 1 ? "원 g₁ 만 활성" : "직선 g₂ 만 활성";
  const lx = P.r + 12;
  return (
    <Frame clock={clock} title="KKT 조건 — 제약이 있는 최솟값"
      read={<>목표점 T(✕)에 가장 가까운 점 찾기: f = |x − T|² 를 원판 g₁ = x² + y² − 1 ≤ 0 과 반평면 g₂ = x + y − 1 ≤ 0 안에서 최소로 · 지금: {act} · 승수 μ₁ = {fmt(S.mu[0], 3)}, μ₂ = {fmt(S.mu[1], 3)} (늘 0 이상) · 정상 조건 −∇f = μ₁∇g₁ + μ₂∇g₂ — 빨간 화살표가 파랑과 보라 화살표의 합과 같다 · 상보 여유성: 활성이 아닌 제약의 승수는 0 · 승수는 그 제약을 조금 풀어 줄 때 f 가 줄어드는 빠르기다</>}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill="none" stroke={C.bd} />
      <path d={P.poly(arc) + "Z"} fill={C.blue} fillOpacity="0.13" stroke={C.blue} strokeWidth="1.3" />
      <line x1={P.X(-0.5)} y1={P.Y(1.5)} x2={P.X(1.5)} y2={P.Y(-0.5)} stroke={C.violet} strokeWidth="1" strokeDasharray="4 3" opacity="0.7" />
      {rad > 0.02 && <circle cx={P.X(T[0])} cy={P.Y(T[1])} r={rad * (P.X(1) - P.X(0))} fill="none" stroke={C.red} strokeWidth="1" strokeDasharray="3 3" opacity="0.6" />}
      <g stroke={C.red} strokeWidth="2"><line x1={P.X(T[0]) - 4} y1={P.Y(T[1]) - 4} x2={P.X(T[0]) + 4} y2={P.Y(T[1]) + 4} /><line x1={P.X(T[0]) - 4} y1={P.Y(T[1]) + 4} x2={P.X(T[0]) + 4} y2={P.Y(T[1]) - 4} /></g>
      {S.mu[0] > 1e-6 && <Arrow x1={X0} y1={Y0} x2={v(n1)[0]} y2={v(n1)[1]} color={C.blue} w={1.8} />}
      {S.mu[1] > 1e-6 && <Arrow x1={X0} y1={Y0} x2={v(n2)[0]} y2={v(n2)[1]} color={C.violet} w={1.8} />}
      {rad > 0.02 && <Arrow x1={X0} y1={Y0} x2={v(nf)[0]} y2={v(nf)[1]} color={C.red} w={1.4} dash="4 2" />}
      <circle cx={X0} cy={Y0} r="4" fill={C.ink} />
      <g fontSize="10" fill={C.ink}>
        <text x={lx} y={26} fontWeight="800">{S.act.length === 0 ? "내부 해" : S.act.length === 2 ? "모서리 해" : "경계 해"}</text>
        <line x1={lx} x2={lx + 12} y1={44} y2={44} stroke={C.red} strokeWidth="1.6" strokeDasharray="4 2" /><text x={lx + 16} y={48}>−∇f</text>
        <line x1={lx} x2={lx + 12} y1={62} y2={62} stroke={C.blue} strokeWidth="1.8" /><text x={lx + 16} y={66}>μ₁∇g₁ (원)</text>
        <line x1={lx} x2={lx + 12} y1={80} y2={80} stroke={C.violet} strokeWidth="1.8" /><text x={lx + 16} y={84}>μ₂∇g₂ (직선)</text>
        <text x={lx} y={112} fill={S.mu[0] > 1e-6 ? C.blue : C.mut}>μ₁ = {fmt(S.mu[0], 3)}</text>
        <text x={lx} y={128} fill={S.mu[1] > 1e-6 ? C.violet : C.mut}>μ₂ = {fmt(S.mu[1], 3)}</text>
        <text x={lx} y={156} fill={C.mut}>g₁ = {fmt(S.x[0] ** 2 + S.x[1] ** 2 - 1, 3)}</text>
        <text x={lx} y={172} fill={C.mut}>g₂ = {fmt(S.x[0] + S.x[1] - 1, 3)}</text>
        <text x={lx} y={196} fill={C.mut}>μᵢ × gᵢ = 0</text>
      </g>
    </Frame>
  );
}

/* ── 장벽법: 중심 경로를 따라 안쪽에서 꼭짓점으로 ── */
const LA = [[1, 1], [1, 3], [1, 0], [-1, 0], [0, -1]], LB = [4, 6, 3.5, 0, 0], LC = [-3, -2];
const slack = (x) => LA.map((r, i) => LB[i] - (r[0] * x[0] + r[1] * x[1]));
const CPATH = (() => {
  let x = [1, 0.5]; const out = [];
  for (let i = 0; i <= 150; i++) {
    const t = 10 ** (-2 + (5 * i) / 150);
    for (let it = 0; it < 60; it++) {
      const s = slack(x), g = [t * LC[0], t * LC[1]], H = [[0, 0], [0, 0]];
      LA.forEach((r, k) => { for (let a = 0; a < 2; a++) { g[a] += r[a] / s[k]; for (let b = 0; b < 2; b++) H[a][b] += (r[a] * r[b]) / (s[k] * s[k]); } });
      const q = solve2(H, g); let al = 1;
      while (slack([x[0] - al * q[0], x[1] - al * q[1]]).some((v) => v <= 0)) al *= 0.5;
      x = [x[0] - al * q[0], x[1] - al * q[1]];
      if (Math.hypot(q[0], q[1]) < 1e-11) break;
    }
    out.push({ t, x });
  }
  return out;
})();
const POLY = [[0, 0], [3.5, 0], [3.5, 0.5], [3, 1], [0, 2]];
export function Barrier() {
  const clock = useClock({ period: 12, rest: 7.5 });
  const i = Math.min(CPATH.length - 1, Math.floor((clock.t / 10) * (CPATH.length - 1)));
  const { t, x } = CPATH[i];
  const P = plot({ x0: -0.35, x1: 4.15, y0: -0.3, y1: 2.45, W: 360, H: 220, pad: [10, 12, 22, 26] });
  const F = (a, b) => { const s = slack([a, b]); if (s.some((v) => v <= 0)) return 1e6; return t * (LC[0] * a + LC[1] * b) - s.reduce((acc, v) => acc + Math.log(v), 0); };
  const fmin = F(x[0], x[1]);
  const lv = [0.4, 1.2, 2.6, 4.6].map((d) => contourPath(P, F, fmin + d, 52));
  const z = 3 * x[0] + 2 * x[1];
  return (
    <Frame clock={clock} title="내점법 — 장벽과 중심 경로"
      read={<>선형계획: 오각형 안에서 3x + 2y 를 최대로(최적 꼭짓점 (3.5, 0.5), 값 11.5) · 내점법은 경계에 닿지 않도록 장벽 −Σ log(여유)를 더해 t × (목적) + 장벽 을 최소로 한다(노란 등위선) · t = <b>{sci(t)}</b>: 중심 경로 위의 점 ({fmt(x[0], 3)}, {fmt(x[1], 3)}), 목적값 {fmt(z, 3)} · 최적값과의 차 ≤ m ÷ t = 5 ÷ t = {sci(5 / t)} · t 를 키울수록 점이 안쪽에서 최적 꼭짓점으로 다가간다 — 심플렉스(회색 점선)는 꼭짓점을 따라 걷는다</>}>
      <Axes p={P} grid={false} xt={[1, 2, 3, 4]} yt={[1, 2]} />
      <path d={P.poly(POLY) + "Z"} fill={C.blue} fillOpacity="0.1" stroke={C.blue} strokeWidth="1.3" />
      {lv.map((d, j) => <path key={j} d={d} fill="none" stroke={C.gold} strokeWidth="1" opacity={0.85 - 0.15 * j} />)}
      <path d={P.poly([[0, 0], [3.5, 0], [3.5, 0.5]])} fill="none" stroke={C.mut} strokeWidth="1.6" strokeDasharray="5 3" />
      <path d={P.poly(CPATH.slice(0, i + 1).map((q) => q.x))} fill="none" stroke={C.red} strokeWidth="2" />
      <circle cx={P.X(CPATH[0].x[0])} cy={P.Y(CPATH[0].x[1])} r="3" fill={C.mut} />
      <circle cx={P.X(x[0])} cy={P.Y(x[1])} r="4.2" fill={C.red} />
      <polygon points={star(P.X(3.5), P.Y(0.5), 6.5)} fill={C.green} />
      <Arrow x1={P.X(0.3)} y1={P.Y(1.25)} x2={P.X(0.3) + 27} y2={P.Y(1.25) - 18} color={C.ink} w={1.4} />
      <Label x={P.X(0.3) + 30} y={P.Y(1.25) - 14} size={9.5} color={C.ink} bg>3x + 2y 증가</Label>
      <Label x={P.X(CPATH[0].x[0]) - 4} y={P.Y(CPATH[0].x[1]) + 14} size={9} color={C.mut} anchor="middle">해석적 중심</Label>
    </Frame>
  );
}

/* ── 분지한정: LP 완화의 상한으로 가지를 쳐 낸다 ── */
const BBN = [
  { par: -1, tx: 272, ty: 30, poly: [[0, 0], [4, 0], [3, 1.5], [0, 3]], lp: [3, 1.5], z: 21, st: "branch", edge: "",
    msg: "뿌리: 정수 조건을 빼고 푼 LP(완화)의 해 (3, 1.5), z = 21 — 어떤 정수해도 21 을 넘지 못한다(상한) · y 가 정수가 아니니 y ≤ 1 과 y ≥ 2 로 나눈다(분지)" },
  { par: 0, tx: 236, ty: 90, poly: [[0, 0], [4, 0], [10 / 3, 1], [0, 1]], lp: [10 / 3, 1], z: 62 / 3, st: "branch", edge: "y ≤ 1",
    msg: "y ≤ 1: LP 해 (3.33, 1), z = 20.67 — x 가 정수가 아니니 x ≤ 3 과 x ≥ 4 로 다시 나눈다" },
  { par: 1, tx: 206, ty: 150, poly: [[0, 0], [3, 0], [3, 1], [0, 1]], lp: [3, 1], z: 19, st: "int", edge: "x ≤ 3",
    msg: "y ≤ 1, x ≤ 3: LP 해 (3, 1) 이 정수다 — 첫 정수해, 지금까지 최선 z = 19" },
  { par: 1, tx: 270, ty: 150, poly: [[4, 0]], lp: [4, 0], z: 20, st: "best", edge: "x ≥ 4",
    msg: "y ≤ 1, x ≥ 4: LP 해 (4, 0) 도 정수, z = 20 > 19 — 최선을 바꾼다" },
  { par: 0, tx: 314, ty: 90, poly: [[0, 2], [2, 2], [0, 3]], lp: [2, 2], z: 18, st: "prune", edge: "y ≥ 2",
    msg: "y ≥ 2: 이 가지의 상한이 z = 18 < 20 — 여기서는 20 보다 좋은 해가 나올 수 없으니 더 나누지 않고 잘라 낸다(한정)" },
];
const BCOL = { branch: C.mut, int: C.blue, best: C.green, prune: C.red };
const BLAB = { branch: "분지", int: "정수해", best: "최선", prune: "가지치기" };
export function BnB() {
  const clock = useClock({ period: 14, rest: 12.5 });
  const step = Math.min(5, Math.floor(clock.t / 2.2));
  const cur = Math.min(4, step), N = BBN[step >= 5 ? 3 : cur];
  const P = plot({ x0: -0.35, x1: 5.0, y0: -0.35, y1: 3.4, W: 360, H: 220, pad: [10, 190, 20, 22] });
  const ok = (x, y) => 6 * x + 4 * y <= 24 && x + 2 * y <= 6;
  const lat = []; for (let x = 0; x <= 4; x++) for (let y = 0; y <= 3; y++) lat.push([x, y]);
  const msg = step === 5 ? "끝: 최적 정수해 (4, 0), z = 20 · LP 해 (3, 1.5) 를 반올림한 (3, 2) 는 제약을 어기고(6 × 3 + 4 × 2 = 26 > 24), 내림한 (3, 1) 은 z = 19 로 최적이 아니다 — 반올림이 아니라 분지와 한정이 답을 보장한다" : N.msg;
  return (
    <Frame clock={clock} title="분지한정 — 정수 계획"
      read={<>최대화 z = 5x + 4y, 제약 6x + 4y ≤ 24, x + 2y ≤ 6, x · y 는 0 이상의 정수 · {msg}</>}>
      <Axes p={P} grid={false} xt={[1, 2, 3, 4]} yt={[1, 2, 3]} />
      <path d={P.poly([[0, 0], [4, 0], [3, 1.5], [0, 3]]) + "Z"} fill="none" stroke={C.mut} strokeWidth="1" strokeDasharray="4 3" />
      {N.poly.length > 1 ? <path d={P.poly(N.poly) + "Z"} fill={BCOL[N.st]} fillOpacity="0.16" stroke={BCOL[N.st]} strokeWidth="1.4" /> : <circle cx={P.X(N.poly[0][0])} cy={P.Y(N.poly[0][1])} r="7" fill={BCOL[N.st]} opacity="0.2" />}
      {lat.map(([x, y]) => <circle key={x + "," + y} cx={P.X(x)} cy={P.Y(y)} r="2.2" fill={ok(x, y) ? C.ink : C.bd} />)}
      <line x1={P.X(N.lp[0] - 1.2)} y1={P.Y(N.lp[1] + 1.5)} x2={P.X(N.lp[0] + 1.2)} y2={P.Y(N.lp[1] - 1.5)} stroke={C.gold} strokeWidth="1" strokeDasharray="3 2" />
      <rect x={P.X(N.lp[0]) - 4} y={P.Y(N.lp[1]) - 4} width="8" height="8" transform={`rotate(45 ${P.X(N.lp[0])} ${P.Y(N.lp[1])})`} fill={C.red} />
      <Label x={P.X(N.lp[0]) + 8} y={P.Y(N.lp[1]) - 6} size={9.5} color={C.red} bg>z = {fmt(N.z, 2)}</Label>
      {BBN.slice(0, step >= 5 ? 5 : cur + 1).map((n, i) => (
        <g key={i}>
          {n.par >= 0 && <line x1={BBN[n.par].tx} y1={BBN[n.par].ty + 11} x2={n.tx} y2={n.ty - 11} stroke={C.mut} strokeWidth="1" />}
          {n.par >= 0 && <text x={(BBN[n.par].tx + n.tx) / 2 + (n.tx < BBN[n.par].tx ? -4 : 4)} y={(BBN[n.par].ty + n.ty) / 2 + 2} fontSize="9" textAnchor={n.tx < BBN[n.par].tx ? "end" : "start"} fill={C.ink}>{n.edge}</text>}
        </g>
      ))}
      {BBN.slice(0, step >= 5 ? 5 : cur + 1).map((n, i) => (
        <g key={"n" + i}>
          <rect x={n.tx - 27} y={n.ty - 11} width="54" height="22" rx="6" fill={C.card} stroke={BCOL[n.st]} strokeWidth={i === cur && step < 5 ? 2.4 : 1.4} />
          <text x={n.tx} y={n.ty - 1} textAnchor="middle" fontSize="9.5" fontWeight="800" fill={BCOL[n.st]}>z ≤ {fmt(n.z, 2)}</text>
          <text x={n.tx} y={n.ty + 8.5} textAnchor="middle" fontSize="7.5" fill={BCOL[n.st]}>{BLAB[n.st]}</text>
        </g>
      ))}
    </Frame>
  );
}

/* ── 담금질 기법: 뜨거울 때는 오르막도 받아들인다 ── */
const AF = (x) => 0.08 * (x - 7) ** 2 + 0.9 * Math.cos(2.6 * x) + 0.5 * Math.cos(5.1 * x + 1);
const ANN = (greedy) => {
  const r = rng(1), N = 400; let x = 1.2, fx = AF(x), best = x, fb = fx, up = 0; const tr = [];
  for (let k = 0; k < N; k++) {
    const T = greedy ? 0 : 2.5 * (0.004 / 2.5) ** (k / (N - 1));
    const xn = clamp(x + 0.45 * gauss(r), 0, 10), fn = AF(xn), dl = fn - fx;
    const acc = dl <= 0 || (!greedy && r() < Math.exp(-dl / T));
    if (acc) { if (dl > 0) up += 1; x = xn; fx = fn; if (fx < fb) { fb = fx; best = x; } }
    tr.push({ x, T, best, up });
  }
  return tr;
};
const TRS = { anneal: ANN(false), greedy: ANN(true) };
export function Anneal({ p = {} }) {
  const [m, setM] = useState(p.mode === "greedy" ? "greedy" : "anneal");
  const clock = useClock({ period: 15, rest: 14.5 });
  const tr = TRS[m], k = Math.min(tr.length - 1, Math.floor((clock.t / 13.5) * (tr.length - 1)));
  const s = tr[k];
  const P = plot({ x0: 0, x1: 10, y0: -1.75, y1: 5.4, pad: [14, 12, 22, 28] });
  const tail = tr.slice(Math.max(0, k - 24), k + 1);
  const tb = m === "anneal" ? clamp(Math.log10(Math.max(s.T, 1e-3) / 0.004) / Math.log10(2.5 / 0.004), 0, 1) : 0;
  return (
    <Frame clock={clock} title="담금질 기법 — 오르막도 받아들이기"
      read={<>{m === "anneal" ? <>온도 T = <b>{fmt(s.T, 3)}</b> — 내리막은 늘 받아들이고, 오르막(Δ &gt; 0)도 확률 exp(−Δ ÷ T) 로 받아들인다 · 지금까지 받아들인 오르막 {s.up} 번 · 지금 x = {fmt(s.x, 2)}, f = {fmt(AF(s.x), 3)} · 최선 x = {fmt(s.best, 2)}, f = {fmt(AF(s.best), 3)} · 뜨거울 때는 골짜기를 넘나들며 둘러보고, 식으면서 가장 깊은 골짜기(x ≈ 6.4)에 자리 잡는다</> : <>내리막만(T = 0) — 더 낮은 곳으로만 옮긴다 · 지금 x = {fmt(s.x, 2)}, f = {fmt(AF(s.x), 3)} · 출발점 근처의 얕은 골짜기(x ≈ 1.6)에 갇혀, 더 깊은 골짜기가 있는 줄 모른다</>}</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["anneal", "담금질"], ["greedy", "내리막만"]]} />}>
      <Axes p={P} grid={false} xt={[2, 4, 8]} yt={[2, 4]} />
      <path d={P.path(AF, 0, 10, 300)} fill="none" stroke={C.blue} strokeWidth="2" />
      <line x1={P.X(6.42)} x2={P.X(6.42)} y1={P.Y(-0.81) + 6} y2={P.b} stroke={C.green} strokeWidth="1" strokeDasharray="3 2" />
      {tail.map((q, i) => <circle key={i} cx={P.X(q.x)} cy={P.Y(AF(q.x))} r="2.2" fill={C.red} opacity={0.08 + (0.5 * i) / tail.length} />)}
      <polygon points={star(P.X(s.best), P.Y(AF(s.best)) - 11, 5.5)} fill={C.gold} />
      <circle cx={P.X(s.x)} cy={P.Y(AF(s.x))} r="4.6" fill={C.red} stroke={C.card} strokeWidth="1" />
      <g>
        <rect x={P.r - 96} y={P.t + 2} width="90" height="8" rx="4" fill="none" stroke={C.bd} />
        <rect x={P.r - 96} y={P.t + 2} width={90 * tb} height="8" rx="4" fill={C.red} opacity="0.7" />
        <text x={P.r - 100} y={P.t + 9.5} textAnchor="end" fontSize="9.5" fill={C.mut}>온도</text>
      </g>
      <Label x={P.X(6.42)} y={P.b - 4} size={9} color={C.green} anchor="middle" bg>가장 깊은 곳</Label>
    </Frame>
  );
}
