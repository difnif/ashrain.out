// 미적분 그림 — 극한(ε-δ) · 할선 → 접선 · 리만 합 · 테일러 근사 · 급수의 부분합 · 뉴턴 방법 · 평균값 정리 · 누적(넓이 함수) · 상자 최적화 · 이분법
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, ease, clamp, useClock } from "./kit.jsx";

/* ── 극한 ε-δ: 상대가 ε 띠를 주면, 나는 그 안에 들어가는 δ 띠를 찾는다 ── */
const LIMS = {
  lin: { f: (x) => 3 * x - 1, a: 2, L: 5, name: "f(x) = 3x − 1,  x → 2", box: [0.5, 3.5, 0, 9] },
  sq: { f: (x) => x * x, a: 1, L: 1, name: "f(x) = x²,  x → 1", box: [-0.2, 2.2, -0.3, 3.2] },
  sinc: { f: (x) => (Math.abs(x) < 1e-9 ? NaN : Math.sin(x) / x), a: 0, L: 1, name: "f(x) = sin x / x,  x → 0 (0 에서 값 없음)", box: [-6, 6, -0.4, 1.3] },
  hole: { f: (x) => (Math.abs(x - 1) < 1e-9 ? NaN : (x * x - 1) / (x - 1)), a: 1, L: 2, name: "f(x) = (x² − 1)/(x − 1),  x → 1 (구멍)", box: [-1, 3, -0.5, 4.5] },
};
function bestDelta(f, a, L, eps, span) {
  // 0 < |x − a| < δ 이면 |f(x) − L| < ε 이 되는 가장 큰 δ(촘촘히 훑어 찾는다)
  let d = span;
  for (let i = 1; i <= 600; i++) {
    const h = (span * i) / 600;
    for (const x of [a - h, a + h]) {
      const y = f(x);
      if (Number.isFinite(y) && Math.abs(y - L) >= eps) { d = Math.min(d, h); }
    }
    if (d < span) break;
  }
  return d * 0.98;
}
export function Limit({ p = {} }) {
  const L0 = LIMS[p.fn] || LIMS.lin;
  const [eps, setEps] = useState(p.eps || (L0.L > 2 ? 1.5 : 0.4));
  const clock = useClock({ period: 6 });
  const [x0, x1, y0, y1] = L0.box;
  const P = plot({ x0, x1, y0, y1 });
  const del = useMemo(() => bestDelta(L0.f, L0.a, L0.L, eps, (x1 - x0) / 2), [L0, eps, x0, x1]);
  // 움직이는 점: 양쪽에서 a 로 다가간다
  const ph = clock.t / 6, side = ph < 0.5 ? -1 : 1, k = ease((ph % 0.5) * 2);
  const xm = L0.a + side * (1 - k) * del * 1.9 + side * 0.02 * del;
  const ym = L0.f(xm);
  const inside = Math.abs(xm - L0.a) < del && Number.isFinite(ym) && Math.abs(ym - L0.L) < eps;
  return (
    <Frame clock={clock} title="극한의 ε-δ 정의"
      read={<>ε = <b>{fmt(eps, 3)}</b> 를 주면 δ ≈ <b>{fmt(del, 3)}</b> — a 주변 δ 안의 모든 x(a 자신은 빼고)는 L 주변 ε 안으로 간다. ε 을 줄여 보세요. δ 도 따라 줄지만 <b>언제나 찾아진다</b>.</>}
      controls={<Slider label="ε" min={0.02} max={(y1 - y0) / 4} step={0.01} value={eps} onChange={setEps} show={(v) => fmt(v, 2)} />}>
      <rect x={P.l} y={P.Y(L0.L + eps)} width={P.r - P.l} height={Math.max(0, P.Y(L0.L - eps) - P.Y(L0.L + eps))} fill={C.gold} opacity="0.16" />
      <rect x={P.X(L0.a - del)} y={P.t} width={Math.max(0, P.X(L0.a + del) - P.X(L0.a - del))} height={P.b - P.t} fill={C.blue} opacity="0.12" />
      <Axes p={P} />
      <path d={P.path(L0.f)} fill="none" stroke={C.sp} strokeWidth="2.2" />
      <circle cx={P.X(L0.a)} cy={P.Y(L0.L)} r="4" fill={C.card} stroke={C.sp} strokeWidth="2" />
      <line x1={P.l} x2={P.r} y1={P.Y(L0.L)} y2={P.Y(L0.L)} stroke={C.gold} strokeDasharray="4 3" />
      <line y1={P.t} y2={P.b} x1={P.X(L0.a)} x2={P.X(L0.a)} stroke={C.blue} strokeDasharray="4 3" />
      {Number.isFinite(ym) && (
        <g>
          <line x1={P.X(xm)} x2={P.X(xm)} y1={P.Y(0) > P.b ? P.b : P.Y(0)} y2={P.Y(ym)} stroke={C.mut} strokeDasharray="2 3" />
          <circle cx={P.X(xm)} cy={P.Y(ym)} r="4.5" fill={inside ? C.green : C.red} />
        </g>
      )}
      <Label x={P.l + 4} y={P.Y(L0.L + eps) - 4} color={C.gold} size={10}>L ± ε</Label>
      <Label x={P.X(L0.a + del) + 3} y={P.b - 4} color={C.blue} size={10}>a ± δ</Label>
      <Label x={P.l + 4} y={P.t + 12} size={10.5} bg>{L0.name}</Label>
    </Frame>
  );
}

/* ── 할선 → 접선: h 를 0 으로 ── */
const FNS = {
  sq: { f: (x) => x * x, d: (x) => 2 * x, name: "y = x²", box: [-2.4, 2.4, -0.6, 5.2], a: 1 },
  cube: { f: (x) => x * x * x - 2 * x, d: (x) => 3 * x * x - 2, name: "y = x³ − 2x", box: [-2.3, 2.3, -3.5, 3.5], a: 1.2 },
  sin: { f: Math.sin, d: Math.cos, name: "y = sin x", box: [-3.4, 3.4, -1.5, 1.5], a: 0.8 },
  exp: { f: Math.exp, d: Math.exp, name: "y = eˣ", box: [-2.5, 2, -0.4, 6.5], a: 0.5 },
  ln: { f: (x) => (x > 0 ? Math.log(x) : NaN), d: (x) => 1 / x, name: "y = ln x", box: [0, 5, -2.5, 2], a: 1.5 },
};
export function Tangent({ p = {} }) {
  const F = FNS[p.fn] || FNS.sq;
  const [a, setA] = useState(p.a ?? F.a);
  const clock = useClock({ period: 7 });
  const [x0, x1, y0, y1] = F.box;
  const P = plot({ x0, x1, y0, y1 });
  const ph = clock.t / 7;
  const hMax = (x1 - x0) / 3;
  const h = ph < 0.8 ? hMax * Math.pow(0.02, ease(ph / 0.8)) : 0.02 * hMax;
  const fa = F.f(a), fb = F.f(a + h), m = (fb - fa) / h, mt = F.d(a);
  const line = (s) => (x) => fa + s * (x - a);
  return (
    <Frame clock={clock} title="할선이 접선으로"
      read={<>h = <b>{fmt(h, 3)}</b> · 할선 기울기 <b>{fmt(m, 4)}</b> → 접선 기울기 f′({fmt(a, 2)}) = <b>{fmt(mt, 4)}</b></>}
      controls={<Slider label="a" min={x0 + 0.3} max={x1 - 0.3 - hMax * 0.1} step={0.05} value={a} onChange={setA} />}>
      <Axes p={P} />
      <path d={P.path(F.f)} fill="none" stroke={C.sp} strokeWidth="2.2" />
      <path d={P.path(line(mt))} fill="none" stroke={C.green} strokeWidth="1.4" strokeDasharray="5 4" />
      <path d={P.path(line(m))} fill="none" stroke={C.red} strokeWidth="1.8" />
      <circle cx={P.X(a)} cy={P.Y(fa)} r="4.5" fill={C.ink} />
      <circle cx={P.X(a + h)} cy={P.Y(fb)} r="4.5" fill={C.red} />
      <line x1={P.X(a)} x2={P.X(a + h)} y1={P.Y(fa)} y2={P.Y(fa)} stroke={C.mut} strokeDasharray="2 2" />
      <line x1={P.X(a + h)} x2={P.X(a + h)} y1={P.Y(fa)} y2={P.Y(fb)} stroke={C.mut} strokeDasharray="2 2" />
      <Label x={P.l + 4} y={P.t + 12} size={10.5}>{F.name}</Label>
      <Label x={P.r - 4} y={P.t + 12} anchor="end" size={10} color={C.red}>할선</Label>
      <Label x={P.r - 4} y={P.t + 25} anchor="end" size={10} color={C.green}>접선</Label>
    </Frame>
  );
}

/* ── 리만 합 ── */
const RF = {
  sq: { f: (x) => x * x, a: 0, b: 2, F: (x) => (x * x * x) / 3, name: "∫₀² x² dx", y: [0, 4.3] },
  sin: { f: Math.sin, a: 0, b: Math.PI, F: (x) => -Math.cos(x), name: "∫₀^π sin x dx", y: [0, 1.15] },
  inv: { f: (x) => 1 / x, a: 1, b: 4, F: Math.log, name: "∫₁⁴ (1/x) dx", y: [0, 1.1] },
  bell: { f: (x) => Math.exp(-x * x), a: -2, b: 2, F: null, name: "∫ e^(−x²) dx (원시함수가 식으로 안 나온다)", y: [0, 1.1] },
};
export function Riemann({ p = {} }) {
  const R0 = RF[p.fn] || RF.sq;
  const [mode, setMode] = useState(p.mode || "mid");
  const [auto, setAuto] = useState(true);
  const [nFix, setN] = useState(8);
  const clock = useClock({ period: 9 });
  const n = auto ? [2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64][Math.min(10, Math.floor((clock.t / 9) * 11))] : nFix;
  const pad = (R0.b - R0.a) * 0.08;
  const P = plot({ x0: R0.a - pad, x1: R0.b + pad, y0: R0.y[0] - 0.05 * R0.y[1], y1: R0.y[1] });
  const dx = (R0.b - R0.a) / n;
  let sum = 0;
  const rects = [];
  for (let i = 0; i < n; i++) {
    const xl = R0.a + i * dx, xs = mode === "left" ? xl : mode === "right" ? xl + dx : xl + dx / 2;
    const h = R0.f(xs);
    sum += h * dx;
    rects.push(<rect key={i} x={P.X(xl)} y={Math.min(P.Y(h), P.Y(0))} width={Math.max(0.5, P.X(xl + dx) - P.X(xl) - (n > 40 ? 0 : 0.6))}
      height={Math.abs(P.Y(0) - P.Y(h))} fill={C.sp} opacity="0.28" stroke={n > 40 ? "none" : C.sp} strokeWidth="0.7" />);
  }
  let exact = R0.F ? R0.F(R0.b) - R0.F(R0.a) : null;
  if (!R0.F) { exact = 0; const N = 4000; for (let i = 0; i < N; i++) exact += R0.f(R0.a + (i + 0.5) * ((R0.b - R0.a) / N)) * ((R0.b - R0.a) / N); }
  return (
    <Frame clock={clock} title="리만 합"
      read={<>{R0.name} · 칸 <b>{n}</b>개 · 직사각형 넓이의 합 <b>{fmt(sum, 5)}</b> · 참값 <b>{fmt(exact, 5)}</b> · 오차 <b>{fmt(Math.abs(sum - exact), 5)}</b></>}
      controls={<>
        <Seg value={mode} onChange={setMode} options={[["left", "왼끝"], ["mid", "가운데"], ["right", "오른끝"]]} />
        <Seg value={auto} onChange={setAuto} options={[[true, "저절로"], [false, "직접"]]} />
        {!auto && <Slider label="n" min={1} max={80} value={nFix} onChange={setN} />}
      </>}>
      {rects}
      <Axes p={P} />
      <path d={P.path(R0.f, R0.a - pad, R0.b + pad)} fill="none" stroke={C.ink} strokeWidth="2" />
    </Frame>
  );
}

/* ── 테일러 근사 ── */
const TY = {
  sin: { f: Math.sin, c: (k) => (k % 2 === 0 ? 0 : (k % 4 === 1 ? 1 : -1)), name: "sin x", box: [-7, 7, -2.2, 2.2] },
  cos: { f: Math.cos, c: (k) => (k % 2 === 1 ? 0 : (k % 4 === 0 ? 1 : -1)), name: "cos x", box: [-7, 7, -2.2, 2.2] },
  exp: { f: Math.exp, c: () => 1, name: "eˣ", box: [-4, 3, -1.5, 12] },
  ln: { f: (x) => (x > -1 ? Math.log(1 + x) : NaN), c: (k) => (k === 0 ? 0 : (k % 2 ? 1 : -1) * fact(k - 1)), name: "ln(1 + x)", box: [-1.2, 2.5, -2.5, 1.8] },
};
function fact(n) { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; }
export function Taylor({ p = {} }) {
  const T = TY[p.fn] || TY.sin;
  const maxN = p.max || 11;
  const [auto, setAuto] = useState(true);
  const [nFix, setN] = useState(3);
  const clock = useClock({ period: maxN * 1.1 });
  const n = auto ? Math.min(maxN, Math.floor(clock.t / 1.1)) : nFix;
  const [x0, x1, y0, y1] = T.box;
  const P = plot({ x0, x1, y0, y1 });
  const poly = (x) => { let s = 0; for (let k = 0; k <= n; k++) s += (T.c(k) / fact(k)) * Math.pow(x, k); return s; };
  const terms = [];
  for (let k = 0; k <= n && terms.length < 6; k++) if (T.c(k)) terms.push(k);
  return (
    <Frame clock={clock} title="테일러 다항식"
      read={<>{T.name} 을 0 근처에서 <b>{n}</b>차 다항식으로 — 차수가 오를수록 맞는 구간이 넓어진다{p.fn === "ln" ? " (ln(1 + x) 는 |x| < 1 너머로는 아무리 차수를 올려도 안 맞는다 — 수렴 반지름 1)" : ""}.</>}
      controls={<>
        <Seg value={auto} onChange={setAuto} options={[[true, "저절로"], [false, "직접"]]} />
        {!auto && <Slider label="차수" min={0} max={maxN} value={nFix} onChange={setN} />}
      </>}>
      <Axes p={P} />
      <path d={P.path(T.f)} fill="none" stroke={C.ink} strokeWidth="2.4" opacity="0.55" />
      <path d={P.path(poly)} fill="none" stroke={C.sp} strokeWidth="2.2" />
      <Label x={P.l + 4} y={P.t + 12} size={10.5}>{T.name}(회색) · {n}차 근사(색)</Label>
    </Frame>
  );
}

/* ── 급수의 부분합 ── */
const SER = {
  geo: { a: (k, r) => Math.pow(r, k), name: (r) => <>Σ {fmt(r, 2)}<sup>k</sup> (k = 0, 1, 2, …)</>, lim: (r) => (Math.abs(r) < 1 ? 1 / (1 - r) : NaN), param: true },
  harm: { a: (k) => 1 / (k + 1), name: () => "1 + 1/2 + 1/3 + ⋯ (조화급수)", lim: () => NaN },
  alt: { a: (k) => (k % 2 ? -1 : 1) / (k + 1), name: () => "1 − 1/2 + 1/3 − ⋯", lim: () => Math.log(2) },
  basel: { a: (k) => 1 / ((k + 1) * (k + 1)), name: () => "1 + 1/4 + 1/9 + ⋯", lim: () => (Math.PI * Math.PI) / 6 },
};
export function Series({ p = {} }) {
  const Sx = SER[p.fn] || SER.geo;
  const [r, setR] = useState(p.r ?? 0.6);
  const N = 40;
  const clock = useClock({ period: 10 });
  const shown = Math.max(1, Math.min(N, Math.floor((clock.t / 9) * N) + 1));
  const parts = [];
  let s = 0;
  for (let k = 0; k < N; k++) { s += Sx.a(k, r); parts.push(s); }
  const L = Sx.lim(r);
  const top = Math.max(...parts.slice(0, shown).map(Math.abs), Number.isFinite(L) ? L : 0, 1) * 1.15;
  const bot = Math.min(0, ...parts.slice(0, shown));
  const P = plot({ x0: 0, x1: N + 1, y0: bot, y1: top });
  const bw = (P.r - P.l) / (N + 1) * 0.7;
  return (
    <Frame clock={clock} title="급수의 부분합"
      read={<>{Sx.name(r)} · 부분합 S<sub>{shown}</sub> = <b>{fmt(parts[shown - 1], 4)}</b>{Number.isFinite(L) ? <> → 극한 <b>{fmt(L, 4)}</b></> : <> → <b>수렴하지 않는다</b>(끝없이 커지거나 흔들린다)</>}</>}
      controls={Sx.param ? <Slider label="r" min={-1.2} max={1.2} step={0.05} value={r} onChange={setR} /> : null}>
      <Axes p={P} xl="n" yl="Sₙ" />
      {Number.isFinite(L) && <line x1={P.l} x2={P.r} y1={P.Y(L)} y2={P.Y(L)} stroke={C.green} strokeDasharray="5 4" />}
      {parts.slice(0, shown).map((v, k) => (
        <rect key={k} x={P.X(k + 1) - bw / 2} width={bw} y={Math.min(P.Y(v), P.Y(0))} height={Math.abs(P.Y(0) - P.Y(v))} fill={C.sp} opacity={k === shown - 1 ? 0.95 : 0.45} />
      ))}
    </Frame>
  );
}

/* ── 뉴턴 방법 ── */
const NW = {
  sqrt2: { f: (x) => x * x - 2, d: (x) => 2 * x, x0: 3, name: "f(x) = x² − 2 (해 √2)", box: [-0.5, 3.6, -3, 11] },
  cosx: { f: (x) => Math.cos(x) - x, d: (x) => -Math.sin(x) - 1, x0: 2.5, name: "f(x) = cos x − x", box: [-1, 3, -3.8, 1.6] },
  cube: { f: (x) => x * x * x - 2 * x - 5, d: (x) => 3 * x * x - 2, x0: 3.2, name: "f(x) = x³ − 2x − 5", box: [1, 3.6, -6, 30] },
};
export function Newton({ p = {} }) {
  const N0 = NW[p.fn] || NW.sqrt2;
  const clock = useClock({ period: 8 });
  const [x0, x1, y0, y1] = N0.box;
  const P = plot({ x0, x1, y0, y1 });
  const xs = [N0.x0];
  for (let i = 0; i < 6; i++) { const x = xs[i]; xs.push(x - N0.f(x) / N0.d(x)); }
  const step = Math.min(5, Math.floor(clock.t / 1.3));
  const segs = [];
  for (let i = 0; i <= step; i++) {
    const x = xs[i], y = N0.f(x), nx = xs[i + 1];
    segs.push(
      <g key={i}>
        <line x1={P.X(x)} x2={P.X(x)} y1={P.Y(0)} y2={P.Y(y)} stroke={C.mut} strokeDasharray="2 3" />
        <line x1={P.X(x)} y1={P.Y(y)} x2={P.X(nx)} y2={P.Y(0)} stroke={C.red} strokeWidth="1.6" />
        <circle cx={P.X(x)} cy={P.Y(y)} r="3.5" fill={C.red} />
        <circle cx={P.X(nx)} cy={P.Y(0)} r="3" fill={C.ink} />
      </g>,
    );
  }
  return (
    <Frame clock={clock} title="뉴턴 방법"
      read={<>{N0.name} · x₀ = {fmt(xs[0], 3)} → {xs.slice(1, step + 2).map((v, i) => <span key={i}> x{"₁₂₃₄₅₆₇"[i]} = <b>{fmt(v, 7)}</b></span>)} — 맞는 자릿수가 거의 두 배씩 는다</>}>
      <Axes p={P} />
      <path d={P.path(N0.f)} fill="none" stroke={C.sp} strokeWidth="2.2" />
      {segs}
    </Frame>
  );
}

/* ── 평균값 정리 ── */
export function MeanValue({ p = {} }) {
  const f = (x) => 0.18 * x * x * x - 0.9 * x * x + 0.6 * x + 2.2, d = (x) => 0.54 * x * x - 1.8 * x + 0.6;
  const a = p.a ?? 0.2, b = p.b ?? 4.4;
  const clock = useClock({ period: 8 });
  const P = plot({ x0: -0.3, x1: 5, y0: -0.4, y1: 4.2 });
  const m = (f(b) - f(a)) / (b - a);
  // f′(c) = m 인 c (근의 공식)
  const A = 0.54, B = -1.8, Cc = 0.6 - m, disc = B * B - 4 * A * Cc;
  const cs = disc >= 0 ? [(-B - Math.sqrt(disc)) / (2 * A), (-B + Math.sqrt(disc)) / (2 * A)].filter((c) => c > a && c < b) : [];
  const ph = (clock.t / 8);
  const xc = a + (b - a) * (0.5 - 0.5 * Math.cos(ph * 2 * Math.PI));
  const tan = (c) => (x) => f(c) + d(c) * (x - c);
  const near = cs.some((c) => Math.abs(d(xc) - m) < 0.06);
  return (
    <Frame clock={clock} title="평균값 정리"
      read={<>평균 변화율(할선 기울기) <b>{fmt(m, 3)}</b> · 움직이는 접선 기울기 <b>{fmt(d(xc), 3)}</b>{near ? " — 지금 나란해졌다!" : ""} · 나란해지는 곳 c = {cs.map((c) => fmt(c, 3)).join(", ")}</>}>
      <Axes p={P} />
      <path d={P.path(f)} fill="none" stroke={C.sp} strokeWidth="2.2" />
      <line x1={P.X(a)} y1={P.Y(f(a))} x2={P.X(b)} y2={P.Y(f(b))} stroke={C.ink} strokeWidth="1.6" />
      {cs.map((c) => <path key={c} d={P.path(tan(c), c - 1.2, c + 1.2)} fill="none" stroke={C.green} strokeDasharray="5 4" />)}
      <path d={P.path(tan(xc), xc - 1, xc + 1)} fill="none" stroke={near ? C.green : C.red} strokeWidth="2" />
      <circle cx={P.X(xc)} cy={P.Y(f(xc))} r="4.5" fill={near ? C.green : C.red} />
      <circle cx={P.X(a)} cy={P.Y(f(a))} r="3.5" fill={C.ink} /><circle cx={P.X(b)} cy={P.Y(f(b))} r="3.5" fill={C.ink} />
      <Label x={P.X(a)} y={P.Y(f(a)) + 15} anchor="middle" size={10}>a</Label>
      <Label x={P.X(b)} y={P.Y(f(b)) - 8} anchor="middle" size={10}>b</Label>
    </Frame>
  );
}

/* ── 누적: 넓이 함수 F(x) = ∫ₐˣ f ── */
const AC = {
  wave: { f: (x) => Math.sin(x) + 0.3, a: 0, b: 2 * Math.PI, name: "f(t) = sin t + 0.3", box: [-1, 1.6] },
  speed: { f: (t) => 2 * t * Math.exp(-0.35 * t), a: 0, b: 10, name: "속도 v(t) — 넓이 = 간 거리", box: [-0.2, 2.4] },
  rate: { f: (t) => 3 - t, a: 0, b: 6, name: "f(t) = 3 − t (음수 넓이는 빼진다)", box: [-3.2, 3.2] },
};
export function Accumulate({ p = {} }) {
  const A = AC[p.fn] || AC.wave;
  const clock = useClock({ period: 8 });
  const xNow = A.a + (A.b - A.a) * clamp(clock.t / 7, 0, 1);
  const N = 400, xs = [], Fs = [];
  let acc = 0;
  for (let i = 0; i <= N; i++) { const x = A.a + ((A.b - A.a) * i) / N; if (i) acc += A.f(x - (A.b - A.a) / N / 2) * ((A.b - A.a) / N); xs.push(x); Fs.push(acc); }
  const Fmax = Math.max(...Fs, 0.1), Fmin = Math.min(...Fs, 0);
  const top = plot({ x0: A.a, x1: A.b, y0: A.box[0], y1: A.box[1], H: 120, pad: [10, 12, 14, 32] });
  const bot = plot({ x0: A.a, x1: A.b, y0: Fmin - 0.1 * (Fmax - Fmin + 0.1), y1: Fmax * 1.1 + 0.05, H: 110, pad: [8, 12, 18, 32] });
  const iNow = Math.round(((xNow - A.a) / (A.b - A.a)) * N);
  let area = "";
  for (let i = 0; i <= iNow; i++) area += (i ? "L" : "M") + top.X(xs[i]).toFixed(1) + " " + top.Y(A.f(xs[i])).toFixed(1);
  area += `L${top.X(xNow).toFixed(1)} ${top.Y(0).toFixed(1)}L${top.X(A.a).toFixed(1)} ${top.Y(0).toFixed(1)}Z`;
  let fp = "";
  for (let i = 0; i <= iNow; i++) fp += (i ? "L" : "M") + bot.X(xs[i]).toFixed(1) + " " + bot.Y(Fs[i]).toFixed(1);
  return (
    <Frame clock={clock} title="넓이 함수" vb="0 0 360 230"
      read={<>{A.name} · x = <b>{fmt(xNow, 2)}</b> 까지 쌓인 양 F(x) = <b>{fmt(Fs[iNow], 3)}</b> · 아래 곡선의 기울기 = 위 곡선의 높이(기본정리)</>}>
      <g>
        <Axes p={top} xl="t" yl="f" />
        <path d={area} fill={C.sp} opacity="0.3" />
        <path d={top.path(A.f)} fill="none" stroke={C.sp} strokeWidth="2" />
        <line x1={top.X(xNow)} x2={top.X(xNow)} y1={top.t} y2={top.b} stroke={C.red} />
      </g>
      <g transform="translate(0,118)">
        <Axes p={bot} xl="x" yl="F" />
        <path d={bot.path((x) => { const i = Math.round(((x - A.a) / (A.b - A.a)) * N); return Fs[clamp(i, 0, N)]; })} fill="none" stroke={C.mut} strokeDasharray="3 3" />
        <path d={fp || "M0 0"} fill="none" stroke={C.red} strokeWidth="2.2" />
        <circle cx={bot.X(xNow)} cy={bot.Y(Fs[iNow])} r="4" fill={C.red} />
      </g>
    </Frame>
  );
}

/* ── 상자 최적화: 정사각형 판의 네 귀를 x 씩 잘라 접는다 ── */
export function BoxOpt({ p = {} }) {
  const L = p.L || 12;
  const clock = useClock({ period: 8 });
  const x = 0.3 + (L / 2 - 0.6) * (0.5 - 0.5 * Math.cos((clock.t / 8) * 2 * Math.PI));
  const V = (t) => t * (L - 2 * t) * (L - 2 * t);
  const xs = L / 6, Vmax = V(xs);
  const P = plot({ x0: 0, x1: L / 2, y0: 0, y1: Vmax * 1.15, W: 210, H: 220, pad: [14, 10, 24, 40] });
  const s = 130 / L, ox = 222, oy = 40;
  return (
    <Frame clock={clock} title="뚜껑 없는 상자의 부피"
      read={<>한 변 {L} 인 판에서 귀를 x = <b>{fmt(x, 2)}</b> 씩 자르면 부피 V = x(L − 2x)² = <b>{fmt(V(x), 1)}</b> · 최대는 x = L/6 = <b>{fmt(xs, 2)}</b> 에서 <b>{fmt(Vmax, 1)}</b>(V′(x) = 0)</>}>
      <Axes p={P} yl="V" />
      <path d={P.path(V)} fill="none" stroke={C.sp} strokeWidth="2.2" />
      <line x1={P.X(xs)} x2={P.X(xs)} y1={P.Y(0)} y2={P.Y(Vmax)} stroke={C.green} strokeDasharray="4 3" />
      <circle cx={P.X(x)} cy={P.Y(V(x))} r="4.5" fill={C.red} />
      <g>
        <rect x={ox} y={oy} width={L * s} height={L * s} fill={C.card} stroke={C.mut} />
        {[[0, 0], [L - x, 0], [0, L - x], [L - x, L - x]].map(([a, b], i) => (
          <rect key={i} x={ox + a * s} y={oy + b * s} width={x * s} height={x * s} fill={C.red} opacity="0.35" />
        ))}
        <rect x={ox + x * s} y={oy + x * s} width={(L - 2 * x) * s} height={(L - 2 * x) * s} fill={C.sp} opacity="0.22" stroke={C.sp} strokeDasharray="3 2" />
        <Label x={ox + (L * s) / 2} y={oy + L * s + 16} anchor="middle" size={10}>잘라 낸 귀(붉은 칸)를 접어 올린다</Label>
      </g>
    </Frame>
  );
}

/* ── 이분법(중간값 정리) ── */
export function Bisection({ p = {} }) {
  const f = (x) => x * x * x + x - 1;
  const clock = useClock({ period: 10 });
  const P = plot({ x0: -0.2, x1: 1.25, y0: -1.4, y1: 1.4 });
  let a = 0, b = 1;
  const steps = Math.min(8, Math.floor(clock.t / 1.1));
  const hist = [[a, b]];
  for (let i = 0; i < steps; i++) { const m = (a + b) / 2; if (f(a) * f(m) <= 0) b = m; else a = m; hist.push([a, b]); }
  return (
    <Frame clock={clock} title="이분법"
      read={<>f(x) = x³ + x − 1 · f(0) &lt; 0 &lt; f(1) 이니 그 사이에 해가 있다(중간값 정리). 반으로 가르기 {steps}번 → 해는 [<b>{fmt(a, 5)}</b>, <b>{fmt(b, 5)}</b>] 안 — 폭이 매번 절반</>}>
      <Axes p={P} />
      {hist.map(([u, v], i) => (
        <rect key={i} x={P.X(u)} width={Math.max(0.5, P.X(v) - P.X(u))} y={P.Y(0) + 4 + i * 6} height="4" fill={i === hist.length - 1 ? C.red : C.sp} opacity={0.35 + 0.08 * i} />
      ))}
      <path d={P.path(f)} fill="none" stroke={C.sp} strokeWidth="2.2" />
      <circle cx={P.X(a)} cy={P.Y(f(a))} r="3.5" fill={C.blue} /><circle cx={P.X(b)} cy={P.Y(f(b))} r="3.5" fill={C.red} />
    </Frame>
  );
}
