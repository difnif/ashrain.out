// 미분방정식 그림 — 방향장 · 지수 성장과 감쇠(반감기) · 로지스틱 · 감쇠 진동 · 강제 진동과 공명 · 상평면 · 오일러 방법 · 포식자-피식자 · 감염병(SIR) · 약물 반복 투여
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, Mat, fmt, clamp, useClock } from "./kit.jsx";

/** 룽게-쿠타 4단 — y′ = f(t, y) (y 는 배열) */
export function rk4(f, y0, t0, t1, n) {
  const out = [[t0, ...y0]];
  let y = y0.slice(), t = t0;
  const h = (t1 - t0) / n;
  for (let i = 0; i < n; i++) {
    const k1 = f(t, y), k2 = f(t + h / 2, y.map((v, j) => v + (h / 2) * k1[j])), k3 = f(t + h / 2, y.map((v, j) => v + (h / 2) * k2[j])), k4 = f(t + h, y.map((v, j) => v + h * k3[j]));
    y = y.map((v, j) => v + (h / 6) * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]));
    t += h;
    out.push([t, ...y]);
  }
  return out;
}

/* ── 방향장: 점마다 기울기 f(x, y) 의 짧은 선 — 해곡선은 그 선을 따라 흐른다 ── */
const SF = {
  decay: { f: (x, y) => -0.8 * y, name: "y′ = −0.8y (감쇠)", box: [0, 5, -2.5, 2.5], y0: [-2, -1, 0.6, 1.4, 2.2] },
  logis: { f: (x, y) => y * (2 - y), name: "y′ = y(2 − y) (로지스틱)", box: [0, 4, -0.5, 3], y0: [0.05, 0.3, 1, 2.6] },
  mix: { f: (x, y) => x - y, name: "y′ = x − y", box: [-2, 3, -2, 3], y0: [-1.8, -0.5, 1, 2.5] },
  wave: { f: (x, y) => Math.sin(x) - 0.5 * y, name: "y′ = sin x − 0.5y", box: [0, 10, -2, 2], y0: [-1.8, 0, 1.8] },
};
export function SlopeField({ p = {} }) {
  const [k, setK] = useState(p.fn || "logis");
  const S = SF[k] || SF.logis;
  const clock = useClock({ period: 7 });
  const [x0, x1, y0, y1] = S.box;
  const P = plot({ x0, x1, y0, y1 });
  const segs = [];
  const nx = 18, ny = 11;
  for (let i = 0; i <= nx; i++) for (let j = 0; j <= ny; j++) {
    const x = x0 + ((x1 - x0) * i) / nx, y = y0 + ((y1 - y0) * j) / ny, m = S.f(x, y);
    const sx = (P.r - P.l) / (x1 - x0), sy = (P.b - P.t) / (y1 - y0);
    const ang = Math.atan2(m * sy, sx), L = 6;
    segs.push(<line key={i + "," + j} x1={P.X(x) - L * Math.cos(ang)} y1={P.Y(y) + L * Math.sin(ang)} x2={P.X(x) + L * Math.cos(ang)} y2={P.Y(y) - L * Math.sin(ang)} stroke={C.mut} strokeWidth="1" />);
  }
  const tEnd = x0 + (x1 - x0) * clamp(clock.t / 6, 0, 1);
  const sols = S.y0.map((yy) => rk4((t, y) => [S.f(t, y[0])], [yy], x0, tEnd, 120));
  return (
    <Frame clock={clock} title="방향장과 해곡선"
      read={<>{S.name} · 짧은 선 = 그 점에서 해가 가야 할 기울기. 출발점(초깃값)이 다르면 다른 해가 되지만 모두 같은 흐름을 탄다</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["decay", "감쇠"], ["logis", "로지스틱"], ["mix", "y′ = x − y"], ["wave", "강제"]]} />}>
      <Axes p={P} grid={false} />
      {segs}
      {sols.map((s, i) => <path key={i} d={P.poly(s.map(([t, y]) => [t, clamp(y, y0 - 1, y1 + 1)]))} fill="none" stroke={C.sp} strokeWidth="2.2" />)}
    </Frame>
  );
}

/* ── 지수 성장 · 감쇠와 반감기 ── */
export function Growth({ p = {} }) {
  const [k, setK] = useState(p.k ?? -0.35);
  const clock = useClock({ period: 8 });
  const T = 8, y0 = 1;
  const y = (t) => y0 * Math.exp(k * t);
  const top = Math.max(1.2, y(T) * 1.1);
  const P = plot({ x0: 0, x1: T, y0: 0, y1: Math.min(top, 20) });
  const tNow = clamp(clock.t, 0, T);
  const half = k < 0 ? Math.log(2) / -k : Math.log(2) / k;
  const marks = [];
  for (let i = 1; i * half <= T && i < 8; i++) marks.push(i * half);
  return (
    <Frame clock={clock} title="지수 성장과 감쇠"
      read={<>y′ = ky, y(0) = 1 → y = e<sup>kt</sup>, k = <b>{fmt(k, 2)}</b> · {k < 0 ? <>반감기 ln 2 / |k| = <b>{fmt(half, 2)}</b> — 그만큼 지날 때마다 <b>절반</b></> : k > 0 ? <>배가 시간 ln 2 / k = <b>{fmt(half, 2)}</b> — 그만큼 지날 때마다 <b>두 배</b></> : "k = 0 — 그대로"}</>}
      controls={<Slider label="k" min={-1} max={0.6} step={0.05} value={k} onChange={setK} />}>
      <Axes p={P} xl="t" />
      {k !== 0 && marks.map((m, i) => (
        <g key={i}>
          <line x1={P.X(m)} x2={P.X(m)} y1={P.Y(0)} y2={P.Y(y(m))} stroke={C.gold} strokeDasharray="3 3" />
          <circle cx={P.X(m)} cy={P.Y(y(m))} r="3" fill={C.gold} />
        </g>
      ))}
      <path d={P.path(y, 0, T)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <circle cx={P.X(tNow)} cy={P.Y(Math.min(y(tNow), P.y1))} r="5" fill={C.red} />
    </Frame>
  );
}

/* ── 로지스틱: 처음엔 지수처럼, 수용력 K 에 가까우면 멈춘다 ── */
export function Logistic({ p = {} }) {
  const [r, setR] = useState(p.r ?? 0.9);
  const [K, setK] = useState(p.K ?? 100);
  const clock = useClock({ period: 9 });
  const N0 = 4, T = 14;
  const N = (t) => K / (1 + ((K - N0) / N0) * Math.exp(-r * t));
  const E = (t) => N0 * Math.exp(r * t);
  const P = plot({ x0: 0, x1: T, y0: 0, y1: 150 });
  const tNow = clamp((clock.t / 8) * T, 0, T);
  return (
    <Frame clock={clock} title="로지스틱 성장"
      read={<>dN/dt = rN(1 − N/K) · 지금 t = {fmt(tNow, 1)}: N = <b>{fmt(N(tNow), 1)}</b> · 가장 빨리 느는 때는 N = K/2 = <b>{fmt(K / 2, 0)}</b> 일 때(변곡점) · 점선 = 제한이 없을 때의 지수 성장</>}
      controls={<>
        <Slider label="r" min={0.2} max={2} step={0.05} value={r} onChange={setR} />
        <Slider label="K" min={40} max={140} step={5} value={K} onChange={setK} />
      </>}>
      <Axes p={P} xl="t" yl="N" />
      <line x1={P.l} x2={P.r} y1={P.Y(K)} y2={P.Y(K)} stroke={C.green} strokeDasharray="5 4" />
      <line x1={P.l} x2={P.r} y1={P.Y(K / 2)} y2={P.Y(K / 2)} stroke={C.bd} strokeDasharray="2 3" />
      <path d={P.path(E, 0, T)} fill="none" stroke={C.mut} strokeDasharray="4 3" />
      <path d={P.path(N, 0, tNow)} fill="none" stroke={C.sp} strokeWidth="2.6" />
      <circle cx={P.X(tNow)} cy={P.Y(N(tNow))} r="5" fill={C.red} />
      <Label x={P.r - 4} y={P.Y(K) - 5} anchor="end" color={C.green} size={10}>수용력 K</Label>
    </Frame>
  );
}

/* ── 감쇠 진동: mx″ + cx′ + kx = 0 — 덜 감쇠 · 임계 · 과감쇠 ── */
export function Oscillator({ p = {} }) {
  const [zeta, setZ] = useState(p.zeta ?? 0.15);
  const clock = useClock({ period: 12 });
  const w0 = 2.2, T = 12;
  const sol = useMemo(() => rk4((t, [x, v]) => [v, -2 * zeta * w0 * v - w0 * w0 * x], [1, 0], 0, T, 600), [zeta]);
  const P = plot({ x0: 0, x1: T, y0: -1.15, y1: 1.15, W: 360, H: 220, pad: [12, 12, 22, 92] });
  const i = Math.min(600, Math.floor((clock.t / T) * 600));
  const x = sol[i][1];
  const kind = zeta < 0.999 ? "덜 감쇠 — 흔들리며 잦아든다" : zeta < 1.001 ? "임계 감쇠 — 가장 빨리, 넘치지 않고 멈춘다" : "과감쇠 — 넘치지 않지만 느리게 돌아온다";
  const my = 110 - x * 70;
  let coil = "M40 20";
  for (let k = 1; k <= 10; k++) coil += `L${k % 2 ? 28 : 52} ${20 + ((my - 20 - 14) * k) / 10}`;
  coil += `L40 ${my - 14}`;
  return (
    <Frame clock={clock} title="감쇠 진동"
      read={<>x″ + 2ζω₀x′ + ω₀²x = 0, 감쇠비 ζ = <b>{fmt(zeta, 2)}</b> — {kind}</>}
      controls={<Slider label="감쇠비 ζ" min={0} max={2} step={0.05} value={zeta} onChange={setZ} />}>
      <line x1="16" y1="18" x2="64" y2="18" stroke={C.ink} strokeWidth="3" />
      <path d={coil} fill="none" stroke={C.mut} strokeWidth="1.6" />
      <rect x="24" y={my - 14} width="32" height="28" rx="4" fill={C.sp} />
      <line x1="16" y1="110" x2="64" y2="110" stroke={C.bd} strokeDasharray="3 3" />
      <Axes p={P} xl="t" yl="x" grid={false} />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, xx]) => [t, xx]))} fill="none" stroke={C.sp} strokeWidth="2.2" />
      {zeta < 1 && <path d={P.path((t) => Math.exp(-zeta * w0 * t))} fill="none" stroke={C.gold} strokeDasharray="3 3" />}
      {zeta < 1 && <path d={P.path((t) => -Math.exp(-zeta * w0 * t))} fill="none" stroke={C.gold} strokeDasharray="3 3" />}
      <circle cx={P.X(sol[i][0])} cy={P.Y(x)} r="4" fill={C.red} />
    </Frame>
  );
}

/* ── 강제 진동과 공명: 진폭 A(ω) 는 ω ≈ ω₀ 에서 솟는다 ── */
export function Resonance({ p = {} }) {
  const [w, setW] = useState(p.w ?? 1.6);
  const [zeta, setZ] = useState(p.zeta ?? 0.1);
  const clock = useClock({ period: 1e9 });
  const w0 = 2;
  const A = (om) => 1 / Math.sqrt((w0 * w0 - om * om) ** 2 + (2 * zeta * w0 * om) ** 2);
  const top = A(w0 * Math.sqrt(Math.max(0.01, 1 - 2 * zeta * zeta))) * 1.1;
  const P = plot({ x0: 0, x1: 4, y0: 0, y1: top, W: 360, H: 120, pad: [10, 10, 18, 34] });
  const Q = plot({ x0: 0, x1: 12, y0: -top, y1: top, W: 360, H: 100, pad: [6, 10, 14, 34] });
  const ph = Math.atan2(2 * zeta * w0 * w, w0 * w0 - w * w);
  const t0 = clock.t % 12;
  return (
    <Frame clock={clock} title="강제 진동과 공명" vb="0 0 360 220"
      read={<>x″ + 2ζω₀x′ + ω₀²x = cos ωt, ω₀ = 2 · 미는 진동수 ω = <b>{fmt(w, 2)}</b> → 정상 상태 진폭 <b>{fmt(A(w), 2)}</b>{Math.abs(w - w0) < 0.15 ? " — 공명! 감쇠가 작을수록 더 높이 솟는다" : ""}</>}
      controls={<>
        <Slider label="ω" min={0.2} max={4} step={0.05} value={w} onChange={setW} />
        <Slider label="ζ" min={0.03} max={0.7} step={0.01} value={zeta} onChange={setZ} />
      </>}>
      <Axes p={P} xl="ω" yl="A" grid={false} />
      <path d={P.path(A, 0.01, 4)} fill="none" stroke={C.sp} strokeWidth="2.2" />
      <line x1={P.X(w)} x2={P.X(w)} y1={P.b} y2={P.Y(A(w))} stroke={C.red} />
      <circle cx={P.X(w)} cy={P.Y(A(w))} r="4" fill={C.red} />
      <g transform="translate(0,120)">
        <line x1={Q.l} x2={Q.r} y1={Q.Y(0)} y2={Q.Y(0)} stroke={C.bd} />
        <path d={Q.path((t) => A(w) * Math.cos(w * t - ph), 0, 12)} fill="none" stroke={C.red} strokeWidth="1.8" />
        <path d={Q.path((t) => (top * 0.25) * Math.cos(w * t), 0, 12)} fill="none" stroke={C.mut} strokeDasharray="3 3" />
        <line x1={Q.X(t0)} x2={Q.X(t0)} y1={Q.t} y2={Q.b} stroke={C.gold} />
        <Label x={Q.l + 2} y={Q.t + 10} size={9.5} color={C.mut}>미는 힘(점선) · 응답(붉음)</Label>
      </g>
    </Frame>
  );
}

/* ── 상평면: x′ = Ax 의 궤적 — 고윳값이 모양을 정한다 ── */
const PH = {
  center: { M: [0, 1, -1, 0], name: "중심(순허수 고윳값 ±i) — 닫힌 궤도" },
  spiralIn: { M: [-0.3, 1, -1, -0.3], name: "안정 나선(실수부 음) — 돌며 빨려 든다" },
  spiralOut: { M: [0.15, 1, -1, 0.15], name: "불안정 나선(실수부 양) — 돌며 멀어진다" },
  saddle: { M: [1, 0, 0, -1], name: "안장(부호가 다른 실근) — 한쪽으로만 다가온다" },
  node: { M: [-1, 0.3, 0.2, -0.5], name: "안정 마디(음의 실근 둘) — 곧장 빨려 든다" },
};
export function PhasePlane({ p = {} }) {
  const [k, setK] = useState(p.m || "spiralIn");
  const Ph = PH[k] || PH.spiralIn;
  const clock = useClock({ period: 8 });
  const P = plot({ x0: -3, x1: 3, y0: -2, y1: 2, pad: [6, 6, 6, 6] });
  const M = Ph.M;
  const F = (t, [x, y]) => [M[0] * x + M[1] * y, M[2] * x + M[3] * y];
  const starts = [[2.5, 0], [-2.5, 0.5], [0.5, 1.8], [-1, -1.8], [1.8, -1.5], [-2.2, 1.6], [0.2, -0.3]];
  const T = 1.2 + (clock.t / 8) * 7;
  const arrows = [];
  for (let i = -2.5; i <= 2.51; i += 0.62) for (let j = -1.7; j <= 1.71; j += 0.56) {
    const [u, v] = F(0, [i, j]), L = Math.hypot(u, v) || 1;
    arrows.push(<Arrow key={i + "," + j} x1={P.X(i)} y1={P.Y(j)} x2={P.X(i + (0.2 * u) / L)} y2={P.Y(j + (0.2 * v) / L)} color={C.bd} w={1} head={3.5} />);
  }
  return (
    <Frame clock={clock} title="상평면"
      read={<>x′ = Ax, A = <Mat m={M} /> — {Ph.name}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["center", "중심"], ["spiralIn", "안정 나선"], ["spiralOut", "불안정"], ["saddle", "안장"], ["node", "마디"]]} />}>
      {arrows}
      {starts.map((s, i) => {
        const tr = rk4(F, s, 0, T, 220).filter(([, x, y]) => Math.abs(x) < 3.4 && Math.abs(y) < 2.4);
        const last = tr[tr.length - 1];
        return (
          <g key={i}>
            <path d={P.poly(tr.map(([, x, y]) => [x, y]))} fill="none" stroke={C.sp} strokeWidth="1.8" />
            {last && <circle cx={P.X(last[1])} cy={P.Y(last[2])} r="3.5" fill={C.red} />}
          </g>
        );
      })}
    </Frame>
  );
}

/* ── 오일러 방법: 기울기를 따라 h 만큼씩 — h 가 작을수록 참해에 가깝다 ── */
export function Euler({ p = {} }) {
  const [h, setH] = useState(p.h ?? 0.5);
  const clock = useClock({ period: 8 });
  const T = 3;
  const P = plot({ x0: 0, x1: T, y0: 0, y1: 21 });
  const pts = [[0, 1]];
  for (let t = 0; t < T - 1e-9; t += h) { const [tt, y] = pts[pts.length - 1]; pts.push([tt + h, y + h * y]); }
  const k = Math.min(pts.length - 1, Math.floor((clock.t / 6) * pts.length));
  const end = pts[pts.length - 1];
  return (
    <Frame clock={clock} title="오일러 방법"
      read={<>y′ = y, y(0) = 1 · 걸음 h = <b>{fmt(h, 2)}</b> → y(3) ≈ <b>{fmt(end[1], 3)}</b>, 참값 e³ = <b>{fmt(Math.exp(3), 3)}</b> · 오차 <b>{fmt(Math.exp(3) - end[1], 3)}</b>(h 를 반으로 줄이면 오차도 거의 반 — 1차 방법)</>}
      controls={<Slider label="h" min={0.05} max={1} step={0.05} value={h} onChange={setH} />}>
      <Axes p={P} xl="t" />
      <path d={P.path(Math.exp, 0, T)} fill="none" stroke={C.green} strokeWidth="2" />
      <path d={P.poly(pts.slice(0, k + 1))} fill="none" stroke={C.red} strokeWidth="2" />
      {pts.slice(0, k + 1).map(([t, y], i) => <circle key={i} cx={P.X(t)} cy={P.Y(y)} r="3" fill={C.red} />)}
      <Label x={P.l + 4} y={P.t + 12} color={C.green} size={10}>참해 e<tspan baselineShift="super" fontSize="0.72em">t</tspan></Label>
      <Label x={P.l + 4} y={P.t + 25} color={C.red} size={10}>오일러 근사</Label>
    </Frame>
  );
}

/* ── 포식자-피식자(로트카-볼테라) ── */
export function PredPrey({ p = {} }) {
  const clock = useClock({ period: 10 });
  const a = 1, b = 0.1, c = 1.5, d = 0.075;
  const T = 30;
  const sol = useMemo(() => rk4((t, [x, y]) => [a * x - b * x * y, -c * y + d * x * y], [10, 5], 0, T, 900), []);
  const i = Math.min(900, Math.floor((clock.t / 10) * 900));
  const P = plot({ x0: 0, x1: T, y0: 0, y1: 50, W: 220, H: 220, pad: [12, 8, 22, 30] });
  const Q = plot({ x0: 0, x1: 50, y0: 0, y1: 32, W: 360, H: 220, pad: [12, 10, 22, 248] });
  return (
    <Frame clock={clock} title="포식자와 피식자"
      read={<>x′ = x − 0.1xy(토끼), y′ = −1.5y + 0.075xy(여우) · 토끼가 늘면 여우가 따라 늘고, 여우가 늘면 토끼가 준다 — 오른쪽 상평면에서 닫힌 고리를 돈다</>}>
      <Axes p={P} xl="t" yl="수" grid={false} />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, x]) => [t, x]))} fill="none" stroke={C.gold} strokeWidth="2" />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, , y]) => [t, y]))} fill="none" stroke={C.red} strokeWidth="2" />
      <Axes p={Q} xl="토끼" yl="여우" grid={false} />
      <path d={Q.poly(sol.map(([, x, y]) => [x, y]))} fill="none" stroke={C.bd} />
      <path d={Q.poly(sol.slice(0, i + 1).map(([, x, y]) => [x, y]))} fill="none" stroke={C.sp} strokeWidth="2" />
      <circle cx={Q.X(sol[i][1])} cy={Q.Y(sol[i][2])} r="4.5" fill={C.red} />
      <Label x={P.l + 4} y={P.t + 10} color={C.gold} size={9.5}>토끼</Label>
      <Label x={P.l + 36} y={P.t + 10} color={C.red} size={9.5}>여우</Label>
    </Frame>
  );
}

/* ── 감염병 SIR: R₀ = β/γ 가 1 을 넘으면 퍼진다 ── */
export function SIR({ p = {} }) {
  const [R0, setR0] = useState(p.R0 ?? 2.5);
  const [vac, setVac] = useState(0);
  const clock = useClock({ period: 9 });
  const g = 0.2, b = R0 * g, T = 120;
  const sol = useMemo(() => rk4((t, [S, I, R]) => [-b * S * I, b * S * I - g * I, g * I], [0.999 - vac, 0.001, vac], 0, T, 600), [b, vac]);
  const i = Math.min(600, Math.floor((clock.t / 8) * 600));
  const P = plot({ x0: 0, x1: T, y0: 0, y1: 1 });
  const peak = sol.reduce((m, r) => Math.max(m, r[2]), 0);
  const herd = 1 - 1 / R0;
  return (
    <Frame clock={clock} title="감염병 SIR 모형"
      read={<>R₀ = β/γ = <b>{fmt(R0, 1)}</b> · 백신 <b>{fmt(vac * 100, 0)}%</b> · 감염 정점 <b>{fmt(peak * 100, 1)}%</b> · 집단면역 문턱 1 − 1/R₀ = <b>{fmt(Math.max(0, herd) * 100, 0)}%</b>{vac >= herd ? " — 넘었다: 퍼지지 못한다" : ""}</>}
      controls={<>
        <Slider label="R₀" min={0.6} max={5} step={0.1} value={R0} onChange={setR0} />
        <Slider label="백신" min={0} max={0.9} step={0.05} value={vac} onChange={setVac} show={(v) => fmt(v * 100, 0) + "%"} />
      </>}>
      <Axes p={P} xl="일" yl="비율" />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, S]) => [t, S]))} fill="none" stroke={C.blue} strokeWidth="2" />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, , I]) => [t, I]))} fill="none" stroke={C.red} strokeWidth="2.4" />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, , , R]) => [t, R]))} fill="none" stroke={C.green} strokeWidth="2" />
      <Label x={P.r - 4} y={P.t + 12} anchor="end" color={C.blue} size={10}>S 감수성</Label>
      <Label x={P.r - 4} y={P.t + 25} anchor="end" color={C.red} size={10}>I 감염</Label>
      <Label x={P.r - 4} y={P.t + 38} anchor="end" color={C.green} size={10}>R 회복</Label>
    </Frame>
  );
}

/* ── 약물 반복 투여: 반감기마다 절반 — 정해진 간격으로 먹으면 정상 상태로 쌓인다 ── */
export function Dosing({ p = {} }) {
  const [tau, setTau] = useState(p.tau ?? 8);
  const [half, setHalf] = useState(p.half ?? 6);
  const clock = useClock({ period: 10 });
  const k = Math.log(2) / half, D = 100, T = 72;
  const c = (t) => { let s = 0; for (let n = 0; n * tau <= t; n++) s += D * Math.exp(-k * (t - n * tau)); return s; };
  const css = D / (1 - Math.exp(-k * tau));
  const P = plot({ x0: 0, x1: T, y0: 0, y1: Math.max(css * 1.1, 120) });
  const tNow = clamp((clock.t / 9) * T, 0, T);
  return (
    <Frame clock={clock} title="반복 투여와 정상 상태"
      read={<>반감기 {half}시간 · {tau}시간마다 100 씩 · 먹은 직후 최고치는 D/(1 − e<sup>−kτ</sup>) = <b>{fmt(css, 0)}</b> 으로 다가간다(등비급수) · 정상 상태까지 대략 반감기의 4 ~ 5배</>}
      controls={<>
        <Slider label="간격 τ" min={2} max={24} step={1} value={tau} onChange={setTau} show={(v) => v + "시간"} />
        <Slider label="반감기" min={2} max={24} step={1} value={half} onChange={setHalf} show={(v) => v + "시간"} />
      </>}>
      <Axes p={P} xl="시간" yl="농도" />
      <line x1={P.l} x2={P.r} y1={P.Y(css)} y2={P.Y(css)} stroke={C.green} strokeDasharray="5 4" />
      <path d={P.path(c, 0, tNow, 600)} fill="none" stroke={C.sp} strokeWidth="2.2" />
    </Frame>
  );
}
