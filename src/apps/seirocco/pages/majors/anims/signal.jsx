// 신호처리 그림 — 푸리에 급수(깁스) · 표본화와 에일리어싱(바퀴) · 합성곱(뒤집어 밀기) · 진폭 · 주파수 변조 · 이산 푸리에 변환(누설) · DCT 압축
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, rng, gauss, useClock } from "./kit.jsx";

/* ── 푸리에 급수: 사인파를 하나씩 더해 모양을 만든다 ── */
const FW = {
  square: { name: "사각파", f: (x) => (Math.sin(x) >= 0 ? 1 : -1), b: (k) => (k % 2 ? 4 / (Math.PI * k) : 0), formula: "(4/π)(sin x + sin 3x ÷ 3 + sin 5x ÷ 5 + ⋯)", jump: true },
  saw: { name: "톱니파", f: (x) => { const u = ((((x + Math.PI) % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)) - Math.PI; return u / Math.PI; }, b: (k) => (2 * (k % 2 ? 1 : -1)) / (Math.PI * k), formula: "(2/π)(sin x − sin 2x ÷ 2 + sin 3x ÷ 3 − ⋯)", jump: true },
  tri: { name: "삼각파", f: (x) => (2 / Math.PI) * Math.asin(Math.sin(x)), b: (k) => (k % 2 ? (8 / (Math.PI * Math.PI * k * k)) * (((k - 1) / 2) % 2 ? -1 : 1) : 0), formula: "(8/π²)(sin x − sin 3x ÷ 9 + sin 5x ÷ 25 − ⋯)", jump: false },
};
export function Fourier({ p = {} }) {
  const [w, setW] = useState(p.wave || "square");
  const [N, setN] = useState(p.N ?? 9);
  const W = FW[w] || FW.square;
  const ks = Array.from({ length: N }, (_, i) => i + 1).filter((k) => Math.abs(W.b(k)) > 1e-12);
  const clock = useClock({ period: 0.7 * ks.length + 3 });
  const m = clock.playing || clock.t > 0 ? Math.min(ks.length, 1 + Math.floor(clock.t / 0.7)) : ks.length;
  const use = ks.slice(0, m), last = use[use.length - 1];
  const S = (x) => use.reduce((s, k) => s + W.b(k) * Math.sin(k * x), 0);
  const P = plot({ x0: 0, x1: 4 * Math.PI, y0: -1.45, y1: 1.45, pad: [10, 10, 78, 26] });
  const Q = plot({ x0: 0, x1: 26, y0: 0, y1: 1.4, pad: [156, 10, 16, 26] });
  return (
    <Frame clock={clock} title="푸리에 급수"
      read={<>{W.name} = {W.formula} · 지금 항 <b>{m}</b>개 (k ≤ {last}) · {W.jump ? <>항을 늘리면 모양에 다가가지만, 끊긴 곳 옆에서 <b>약 9 % 넘치는 깁스 현상</b>은 없어지지 않고 좁아질 뿐</> : <>끊긴 곳이 없어 계수가 1/k² 로 빨리 줄고, 몇 항만으로도 거의 같다</>} · 아래 막대 = 스펙트럼(주파수마다의 세기), 가는 선 = 마지막에 더한 사인파</>}
      controls={<>
        <Seg value={w} onChange={(v) => { setW(v); clock.reset(); }} options={[["square", "사각파"], ["saw", "톱니파"], ["tri", "삼각파"]]} />
        <Slider label="최고 k" min={1} max={25} value={N} onChange={(v) => { setN(v); clock.reset(); }} />
      </>}>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.bd} />
      <path d={P.path(W.f, 0, 4 * Math.PI, 400)} fill="none" stroke={C.mut} strokeWidth="1.3" strokeDasharray="4 3" />
      {last && <path d={P.path((x) => W.b(last) * Math.sin(last * x), 0, 4 * Math.PI, 400)} fill="none" stroke={C.gold} strokeWidth="1" opacity="0.8" />}
      <path d={P.path(S, 0, 4 * Math.PI, 600)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <line x1={Q.l} x2={Q.r} y1={Q.Y(0)} y2={Q.Y(0)} stroke={C.mut} />
      {Array.from({ length: 25 }, (_, i) => i + 1).map((k) => {
        const b = Math.abs(W.b(k)), on = use.includes(k);
        return b > 1e-12 ? <rect key={k} x={Q.X(k) - 3} y={Q.Y(b)} width="6" height={Q.Y(0) - Q.Y(b)} fill={on ? C.sp : C.bd} /> : null;
      })}
      {[1, 5, 10, 15, 20, 25].map((k) => <text key={k} x={Q.X(k)} y={Q.b + 11} textAnchor="middle" fontSize="9" fill={C.mut}>{k}</text>)}
      <text x={Q.l - 2} y={Q.t + 6} fontSize="9" fill={C.mut}>|bₖ|</text>
    </Frame>
  );
}

/* ── 표본화와 에일리어싱: 너무 드물게 재면 빠른 신호가 느린 신호로 둔갑한다 ── */
export function Alias({ p = {} }) {
  const [f, setF] = useState(p.f ?? 7);
  const [fs, setFs] = useState(p.fs ?? 10);
  const clock = useClock({ period: 40 });
  const tau = clock.t * 0.08; // 바퀴는 천천히(12.5 배 느리게) 보여 준다
  const m = Math.round(f / fs), fa = f - m * fs;
  const P = plot({ x0: 0, x1: 1, y0: -1.35, y1: 1.35, pad: [14, 10, 22, 152] });
  const samples = []; for (let n = 0; n / fs <= 1 + 1e-9; n++) samples.push([n / fs, Math.sin((2 * Math.PI * f * n) / fs)]);
  const cx = 74, cy = 88, R = 50, nNow = Math.floor(tau * fs);
  const spoke = (ang, op, col, wd) => <line x1={cx} y1={cy} x2={cx + R * Math.cos(ang)} y2={cy - R * Math.sin(ang)} stroke={col} strokeWidth={wd} opacity={op} strokeLinecap="round" />;
  const alias = f > fs / 2 + 1e-9;
  return (
    <Frame clock={clock} title="표본화와 에일리어싱"
      read={<>표본화 fₛ = {fs} Hz → 나이퀴스트 주파수 fₛ/2 = <b>{fmt(fs / 2, 1)} Hz</b> · 신호 {fmt(f, 1)} Hz {alias ? <>→ 점(표본)만 보면 <b>{fmt(Math.abs(fa), 1)} Hz</b> 로 보인다 — 에일리어싱(빨간 점선){fa < 0 ? ", 바퀴는 거꾸로 도는 것처럼" : ""}</> : <>— fₛ/2 보다 낮아 표본으로 원래 신호를 되살릴 수 있다</>} · 왼쪽: 같은 일이 영화 속 바퀴에서(흐린 바큇살 = 실제, 진한 바큇살 = 카메라에 찍힌 모습)</>}
      controls={<>
        <Slider label="신호 f" min={1} max={15} step={0.5} value={f} onChange={setF} show={(v) => fmt(v, 1) + " Hz"} />
        <Slider label="fₛ" min={4} max={30} step={1} value={fs} onChange={setFs} show={(v) => v + " Hz"} />
      </>}>
      <circle cx={cx} cy={cy} r={R + 4} fill={C.card} stroke={C.ink} strokeWidth="2" />
      {spoke(2 * Math.PI * f * tau, 0.25, C.mut, 2)}
      {[3, 2, 1].map((k) => (nNow - k >= 0 ? <g key={k}>{spoke((2 * Math.PI * f * (nNow - k)) / fs, 0.15 * (4 - k), C.sp, 3)}</g> : null))}
      {spoke((2 * Math.PI * f * nNow) / fs, 1, C.sp, 4)}
      <circle cx={cx} cy={cy} r="4" fill={C.ink} />
      <text x={cx} y="168" textAnchor="middle" fontSize="10" fill={C.mut}>실제 {fmt(f, 1)} 바퀴/초</text>
      <text x={cx} y="184" textAnchor="middle" fontSize="10" fill={alias ? C.red : C.green}>찍힌 모습 {fmt(Math.abs(fa), 1)} 바퀴/초{fa < 0 ? " (거꾸로)" : ""}</text>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.bd} />
      <path d={P.path((t) => Math.sin(2 * Math.PI * f * t), 0, 1, 500)} fill="none" stroke={C.mut} strokeWidth="1.2" />
      {alias && <path d={P.path((t) => Math.sin(2 * Math.PI * fa * t), 0, 1, 300)} fill="none" stroke={C.red} strokeWidth="1.8" strokeDasharray="5 3" />}
      {samples.map(([t, v], i) => (
        <g key={i}>
          <line x1={P.X(t)} x2={P.X(t)} y1={P.Y(0)} y2={P.Y(v)} stroke={C.sp} strokeWidth="1.2" />
          <circle cx={P.X(t)} cy={P.Y(v)} r="3.2" fill={C.sp} />
        </g>
      ))}
      <text x={P.r} y={P.b + 14} textAnchor="end" fontSize="10" fill={C.mut}>t (1 초)</text>
    </Frame>
  );
}

/* ── 합성곱: g 를 뒤집어(τ → −τ) t 만큼 밀고, f 와 곱한 넓이 ── */
const NOISE = (() => { const r = rng(17); return Array.from({ length: 401 }, () => 0.35 * gauss(r)); })();
const noisy = (t) => (t >= 0 && t <= 4 ? 1 + 0.6 * Math.sin(2 * Math.PI * 0.4 * t) + NOISE[Math.min(400, Math.max(0, Math.round(t * 100)))] : 0);
const CV = {
  rectrect: { name: "상자 ∗ 상자 = 세모", f: (t) => (t >= 0 && t <= 1 ? 1 : 0), g: (t) => (t >= 0 && t <= 1 ? 1 : 0), top: 1.25, ytop: 1.15 },
  rectexp: { name: "1 초 동안 켠 입력 ∗ RC 회로의 충격응답(지수로 줄어드는 꼴)", f: (t) => (t >= 0 && t <= 1 ? 1 : 0), g: (t) => (t >= 0 ? 2 * Math.exp(-2 * t) : 0), top: 2.2, ytop: 1.1 },
  smooth: { name: "잡음 섞인 신호 ∗ 폭 0.5 의 상자 = 이동평균", f: noisy, g: (t) => (t >= 0 && t <= 0.5 ? 2 : 0), top: 2.4, ytop: 2.2 },
};
export function Convolve({ p = {} }) {
  const [k, setK] = useState(p.pair || "rectrect");
  const Cv = CV[k] || CV.rectrect;
  const clock = useClock({ period: 10 });
  const dtau = 0.01, taus = Array.from({ length: 601 }, (_, i) => -1 + i * dtau);
  const conv = useMemo(() => {
    const out = [];
    for (let i = 0; i <= 250; i++) { const t = -0.5 + i * 0.02; let s = 0; for (const tau of taus) s += Cv.f(tau) * Cv.g(t - tau) * dtau; out.push([t, s]); }
    return out;
  }, [k]); // eslint-disable-line react-hooks/exhaustive-deps
  const t = -0.5 + 5 * clamp(clock.t / 8, 0, 1), it = Math.min(250, Math.round((t + 0.5) / 0.02));
  const P = plot({ x0: -1, x1: 5, y0: -0.25, y1: Cv.top, pad: [10, 10, 112, 26] });
  const Q = plot({ x0: -1, x1: 5, y0: -0.1, y1: Cv.ytop, pad: [122, 10, 18, 26] });
  const prod = taus.map((tau) => [tau, Cv.f(tau) * Cv.g(t - tau)]);
  const say = { rectrect: "두 상자가 겹치는 길이만큼 — 그래서 세모", rectexp: "회로의 출력: 켜져 있는 동안 차오르고 끄면 지수로 빠진다 — RC 회로를 미분방정식으로 푼 답과 같다", smooth: "빠른 떨림(잡음)은 상자 안에서 평균되어 깎이고 느린 물결만 남는다 — 저역통과 필터" }[k];
  return (
    <Frame clock={clock} title="합성곱 — 뒤집어 밀기"
      read={<>{Cv.name} · (f ∗ g)(t) = ∫ f(τ)g(t − τ)dτ — 위: f(τ)(파랑) 위로 뒤집은 g(t − τ)(주황)를 t 만큼 민다, 겹친 곱의 넓이(빨강)가 아래 그래프의 높이 · t = {fmt(t, 2)}: <b>{fmt(conv[it][1], 3)}</b> · {say}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["rectrect", "상자 ∗ 상자"], ["rectexp", "입력 ∗ RC"], ["smooth", "이동평균"]]} />}>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.mut} />
      <path d={P.poly(prod) + `L${P.X(5)} ${P.Y(0)}L${P.X(-1)} ${P.Y(0)}Z`} fill={C.red} opacity="0.3" />
      <path d={P.poly(taus.map((tau) => [tau, Cv.f(tau)]))} fill="none" stroke={C.blue} strokeWidth="1.8" />
      <path d={P.poly(taus.map((tau) => [tau, Cv.g(t - tau)]))} fill="none" stroke={C.gold} strokeWidth="1.8" />
      <line x1={P.X(t)} x2={P.X(t)} y1={P.t} y2={P.b} stroke={C.gold} strokeDasharray="2 3" />
      <text x={P.X(t) + 3} y={P.t + 9} fontSize="9.5" fill={C.gold}>t</text>
      <text x={P.l + 2} y={P.t + 9} fontSize="9.5" fill={C.mut} fontStyle="italic">τ</text>
      <Axes p={Q} xl="t" yl="f ∗ g" />
      <path d={Q.poly(conv)} fill="none" stroke={C.sp} strokeWidth="1.3" opacity="0.25" />
      <path d={Q.poly(conv.slice(0, it + 1))} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <circle cx={Q.X(conv[it][0])} cy={Q.Y(conv[it][1])} r="4" fill={C.red} />
    </Frame>
  );
}

/* ── 변조: 진폭에 싣기(AM) · 주파수에 싣기(FM) — 스펙트럼의 옆띠 ── */
function besselJ(n, x) {
  const an = Math.abs(n); let s = 0, fk = 1, fkn = 1;
  for (let i = 2; i <= an; i++) fkn *= i;
  for (let k = 0; k < 30; k++) { if (k > 0) { fk *= k; fkn *= k + an; } s += ((k % 2 ? -1 : 1) * Math.pow(x / 2, 2 * k + an)) / (fk * fkn); }
  return n < 0 && an % 2 ? -s : s;
}
export function Modulation({ p = {} }) {
  const [mode, setMode] = useState(p.mode || "am");
  const [m, setM] = useState(p.m ?? 0.6);
  const [beta, setBeta] = useState(p.beta ?? 2);
  const clock = useClock({ period: 20 });
  const fm = 1, fc = 10, off = clock.t * 0.4;
  const A = (tt) => Math.cos(2 * Math.PI * fm * tt);
  const sig = mode === "am" ? (tt) => (1 + m * A(tt)) * Math.cos(2 * Math.PI * fc * tt) : (tt) => Math.cos(2 * Math.PI * fc * tt + beta * Math.sin(2 * Math.PI * fm * tt));
  const P1 = plot({ x0: 0, x1: 3, y0: -1.3, y1: 1.3, pad: [8, 10, 170, 26] });
  const yr = mode === "am" ? 1 + Math.max(m, 0.2) + 0.15 : 1.3;
  const P2 = plot({ x0: 0, x1: 3, y0: -yr, y1: yr, pad: [60, 10, 70, 26] });
  const Q = plot({ x0: 0, x1: 20, y0: 0, y1: 1.1, pad: [162, 10, 16, 26] });
  const bars = mode === "am" ? [[fc, 1], [fc - fm, m / 2], [fc + fm, m / 2]] : Array.from({ length: 17 }, (_, i) => [fc + (i - 8) * fm, Math.abs(besselJ(i - 8, beta))]);
  return (
    <Frame clock={clock} title={mode === "am" ? "진폭 변조(AM)" : "주파수 변조(FM)"}
      read={mode === "am"
        ? <>(1 + m cos ωₘ t) cos ωc t — 위: 보낼 신호, 가운데: 반송파(10 Hz)의 진폭에 실은 모양(점선 = 덮개), 아래: 스펙트럼 · 변조 지수 m = <b>{fmt(m, 2)}</b>{m > 1 ? <> — <b>1 을 넘으면 덮개가 0 아래로 뒤집혀</b> 받는 쪽에서 신호가 일그러진다(과변조)</> : " — 반송파 양옆에 크기 m/2 의 옆띠 둘"}</>
        : <>cos(ωc t + β sin ωₘ t) — 진폭은 그대로, 촘촘함(순간 주파수)이 신호를 따라 바뀐다 · 변조 지수 β = <b>{fmt(beta, 1)}</b>: 옆띠 크기 = 베셀 함수 |Jₙ(β)|, 대역폭 ≈ 2(β + 1)fₘ = <b>{fmt(2 * (beta + 1) * fm, 1)} Hz</b> (카슨 규칙) — 잡음에 강한 대신 넓은 대역을 쓴다</>}
      controls={<>
        <Seg value={mode} onChange={setMode} options={[["am", "AM"], ["fm", "FM"]]} />
        {mode === "am" ? <Slider label="m" min={0} max={1.5} step={0.05} value={m} onChange={setM} /> : <Slider label="β" min={0} max={5} step={0.1} value={beta} onChange={setBeta} />}
      </>}>
      <line x1={P1.l} x2={P1.r} y1={P1.Y(0)} y2={P1.Y(0)} stroke={C.bd} />
      <path d={P1.path((x) => A(x + off), 0, 3, 200)} fill="none" stroke={C.gold} strokeWidth="1.8" />
      <text x={P1.l - 2} y={P1.t + 8} fontSize="9" fill={C.mut} textAnchor="end">신호</text>
      <line x1={P2.l} x2={P2.r} y1={P2.Y(0)} y2={P2.Y(0)} stroke={C.bd} />
      <path d={P2.path((x) => sig(x + off), 0, 3, 900)} fill="none" stroke={C.sp} strokeWidth="1.2" />
      {mode === "am" && <>
        <path d={P2.path((x) => 1 + m * A(x + off), 0, 3, 200)} fill="none" stroke={C.gold} strokeDasharray="3 3" />
        <path d={P2.path((x) => -(1 + m * A(x + off)), 0, 3, 200)} fill="none" stroke={C.gold} strokeDasharray="3 3" />
      </>}
      <line x1={Q.l} x2={Q.r} y1={Q.Y(0)} y2={Q.Y(0)} stroke={C.mut} />
      {bars.map(([fq, a], i) => (fq >= 0 && fq <= 20 ? <rect key={i} x={Q.X(fq) - 3} y={Q.Y(Math.min(1.1, a))} width="6" height={Q.Y(0) - Q.Y(Math.min(1.1, a))} fill={fq === fc ? C.sp : C.gold} /> : null))}
      {[0, 5, 10, 15, 20].map((v) => <text key={v} x={Q.X(v)} y={Q.b + 11} textAnchor="middle" fontSize="9" fill={C.mut}>{v}</text>)}
      <text x={Q.r} y={Q.t + 4} textAnchor="end" fontSize="9" fill={C.mut}>주파수 (Hz)</text>
    </Frame>
  );
}

/* ── 이산 푸리에 변환: 신호와 k 번 도는 사인의 닮은 정도 — 칸에 안 맞으면 샌다 ── */
export function DFT({ p = {} }) {
  const [sig, setSig] = useState(p.sig || "two");
  const [f, setF] = useState(p.f ?? 5.5);
  const clock = useClock({ period: 20 });
  const N = 64;
  const x = useMemo(() => {
    const r = rng(23);
    return Array.from({ length: N }, (_, n) => (sig === "two" ? Math.sin((2 * Math.PI * 5 * n) / N) + 0.5 * Math.sin((2 * Math.PI * 12 * n) / N) : sig === "leak" ? Math.sin((2 * Math.PI * f * n) / N) : Math.sin((2 * Math.PI * 6 * n) / N) + 0.9 * gauss(r)));
  }, [sig, f]);
  const X = useMemo(() => Array.from({ length: N / 2 + 1 }, (_, k) => {
    let re = 0, im = 0;
    for (let n = 0; n < N; n++) { const a = (-2 * Math.PI * k * n) / N; re += x[n] * Math.cos(a); im += x[n] * Math.sin(a); }
    return Math.hypot(re, im) / (k === 0 || k === N / 2 ? N : N / 2);
  }), [x]);
  const k = Math.min(N / 2, Math.floor(clock.t / 0.55));
  const P = plot({ x0: 0, x1: N, y0: -2.6, y1: 2.6, pad: [10, 10, 108, 26] });
  const Q = plot({ x0: -0.5, x1: N / 2 + 0.5, y0: 0, y1: 1.15, pad: [124, 10, 18, 26] });
  return (
    <Frame clock={clock} title="이산 푸리에 변환"
      read={<>X[k] = Σ x[n]e<sup>−2πikn/N</sup> (N = 64) — 신호와 「k 번 도는 사인」(주황)을 곱해 더한 값, 곧 <b>닮은 정도</b> · 지금 k = {k}: |X[k]| = <b>{fmt(X[k], 3)}</b> · {sig === "two" ? "두 사인(5 번, 12 번)이 막대 둘로 갈라진다" : sig === "leak" ? <>f = {fmt(f, 1)}: {Math.abs(f - Math.round(f)) < 1e-9 ? "칸(정수)에 딱 맞으면 막대 하나" : <>칸에 맞지 않으면 에너지가 옆 칸으로 <b>샌다(누설)</b> — 창 함수로 줄인다</>}</> : "잡음에 묻혀 눈으로는 안 보이던 6 번 사인이 막대 하나로 솟는다"}</>}
      controls={<>
        <Seg value={sig} onChange={setSig} options={[["two", "두 사인"], ["leak", "누설"], ["noise", "잡음 속"]]} />
        {sig === "leak" && <Slider label="f" min={3} max={10} step={0.1} value={f} onChange={setF} />}
      </>}>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.bd} />
      <path d={P.path((n) => 1.2 * Math.cos((2 * Math.PI * k * n) / N), 0, N, 400)} fill="none" stroke={C.gold} strokeWidth="1.2" opacity="0.8" />
      {x.map((v, n) => <g key={n}><line x1={P.X(n)} x2={P.X(n)} y1={P.Y(0)} y2={P.Y(clamp(v, -2.6, 2.6))} stroke={C.sp} strokeWidth="1" /><circle cx={P.X(n)} cy={P.Y(clamp(v, -2.6, 2.6))} r="1.8" fill={C.sp} /></g>)}
      <line x1={Q.l} x2={Q.r} y1={Q.Y(0)} y2={Q.Y(0)} stroke={C.mut} />
      {X.map((v, kk) => <rect key={kk} x={Q.X(kk) - 2.6} y={Q.Y(Math.min(1.15, v))} width="5.2" height={Q.Y(0) - Q.Y(Math.min(1.15, v))} fill={kk === k ? C.red : kk < k ? C.sp : C.bd} />)}
      {[0, 8, 16, 24, 32].map((v) => <text key={v} x={Q.X(v)} y={Q.b + 11} textAnchor="middle" fontSize="9" fill={C.mut}>{v}</text>)}
      <text x={Q.r} y={Q.t + 6} textAnchor="end" fontSize="9" fill={C.mut}>k (주파수 칸)</text>
    </Frame>
  );
}

/* ── DCT 압축: 큰 계수 몇 개만 남겨도 모양이 산다 — JPEG 의 원리 ── */
const DN = 32;
const DSIG = Array.from({ length: DN }, (_, n) => 0.7 * Math.sin((2 * Math.PI * 1.5 * n) / DN) + (n > 20 ? 0.8 : 0) + 0.15 * Math.cos((2 * Math.PI * 5 * n) / DN));
const dsc = (k) => (k === 0 ? Math.sqrt(1 / DN) : Math.sqrt(2 / DN));
const DCO = Array.from({ length: DN }, (_, k) => dsc(k) * DSIG.reduce((s, v, n) => s + v * Math.cos((Math.PI * (n + 0.5) * k) / DN), 0));
const DORD = DCO.map((v, k) => [Math.abs(v), k]).sort((a, b) => b[0] - a[0]).map(([, k]) => k);
export function DCT({ p = {} }) {
  const [K, setK] = useState(p.K ?? 6);
  const clock = useClock({ period: 0.6 * K + 3 });
  const shown = clock.playing || clock.t > 0 ? Math.min(K, 1 + Math.floor(clock.t / 0.6)) : K;
  const keep = new Set(DORD.slice(0, shown));
  const rec = (t) => DCO.reduce((s, c, k) => (keep.has(k) ? s + dsc(k) * c * Math.cos((Math.PI * (t + 0.5) * k) / DN) : s), 0);
  const err = Math.sqrt(DSIG.reduce((s, v, n) => s + (v - rec(n)) ** 2, 0) / DN);
  const P = plot({ x0: -0.5, x1: DN - 0.5, y0: -1, y1: 1.8, pad: [10, 10, 100, 26] });
  const cmax = Math.max(...DCO.map(Math.abs));
  const Q = plot({ x0: -0.5, x1: DN - 0.5, y0: -cmax * 1.1, y1: cmax * 1.1, pad: [132, 10, 16, 26] });
  return (
    <Frame clock={clock} title="DCT 압축"
      read={<>표본 32 개를 코사인 32 개의 합으로 바꾼 뒤(DCT) 큰 계수 <b>{shown}</b> 개만 남기면 {fmt(DN / shown, 1)} : 1 압축, 오차(RMS) <b>{fmt(err, 3)}</b> · 매끈한 곳은 계수 몇 개로 충분하지만 계단(모서리)에는 높은 주파수가 많이 필요해 물결(링잉)이 남는다 — JPEG 가 8 × 8 칸마다 하는 일 · 아래 = 계수(색 = 남긴 것)</>}
      controls={<Slider label="남길 계수" min={1} max={32} value={K} onChange={(v) => { setK(v); clock.reset(); }} />}>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.bd} />
      {DSIG.map((v, n) => <circle key={n} cx={P.X(n)} cy={P.Y(v)} r="2.8" fill={C.mut} />)}
      <path d={P.path(rec, -0.5, DN - 0.5, 400)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <line x1={Q.l} x2={Q.r} y1={Q.Y(0)} y2={Q.Y(0)} stroke={C.mut} />
      {DCO.map((c, k) => <rect key={k} x={Q.X(k) - 3} y={Math.min(Q.Y(c), Q.Y(0))} width="6" height={Math.abs(Q.Y(c) - Q.Y(0))} fill={keep.has(k) ? C.sp : C.bd} />)}
      {[0, 8, 16, 24, 31].map((v) => <text key={v} x={Q.X(v)} y={Q.b + 11} textAnchor="middle" fontSize="9" fill={C.mut}>{v}</text>)}
      <Label x={P.l + 4} y={P.b - 3} size={10} color={C.mut} bg>점 = 원래 표본, 선 = 남긴 계수로 되살린 것</Label>
    </Frame>
  );
}
