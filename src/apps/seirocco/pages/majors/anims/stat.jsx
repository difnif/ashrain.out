// 통계 그림 — 평균과 중앙값(이상치) · 표본분포와 표준오차 · 신뢰구간의 포함률 · 가설검정(기각역 · p값 · 검정력) · 최소제곱 회귀 · 분산분석 · 베이즈 갱신(베타) · 붓스트랩
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, rng, gauss, useClock } from "./kit.jsx";
import { phi, Phi } from "./prob.jsx";

/* ── 평균은 이상치에 끌려가고 중앙값은 버틴다 ── */
export function Summary({ p = {} }) {
  const clock = useClock({ period: 8 });
  const base = [3.1, 3.6, 4.0, 4.2, 4.5, 4.8, 5.0, 5.3, 5.7, 6.2, 6.6];
  const out = 6.6 + 13 * (0.5 - 0.5 * Math.cos((clock.t / 8) * 2 * Math.PI));
  const xs = [...base.slice(0, -1), out].sort((a, b) => a - b);
  const mean = xs.reduce((a, b) => a + b, 0) / xs.length, med = xs[(xs.length - 1) / 2];
  const sd = Math.sqrt(xs.reduce((s, x) => s + (x - mean) ** 2, 0) / (xs.length - 1));
  const q1 = xs[2], q3 = xs[8], iqr = q3 - q1;
  const P = plot({ x0: 2, x1: 21, y0: 0, y1: 4, pad: [10, 12, 24, 12] });
  return (
    <Frame clock={clock} title="평균과 중앙값"
      read={<>가장 큰 값을 <b>{fmt(out, 1)}</b> 까지 끌어올리면 — 평균 <b>{fmt(mean, 2)}</b>(붉음)은 따라가고, 중앙값 <b>{fmt(med, 2)}</b>(초록)은 그대로 · 표준편차 {fmt(sd, 2)} · 사분위범위 IQR {fmt(iqr, 2)}(버틴다){out > q3 + 1.5 * iqr ? " · 이상치(Q3 + 1.5 IQR 바깥)" : ""}</>}>
      <line x1={P.l} x2={P.r} y1={P.Y(1)} y2={P.Y(1)} stroke={C.mut} />
      {xs.map((x, i) => <circle key={i} cx={P.X(x)} cy={P.Y(1.6 + (i % 2) * 0.5)} r="6" fill={x === out ? C.red : C.sp} opacity="0.8" />)}
      <rect x={P.X(q1)} y={P.Y(3.6)} width={P.X(q3) - P.X(q1)} height={P.Y(3.0) - P.Y(3.6)} fill={C.card} stroke={C.ink} />
      <line x1={P.X(xs[0])} x2={P.X(q1)} y1={P.Y(3.3)} y2={P.Y(3.3)} stroke={C.ink} />
      <line x1={P.X(q3)} x2={P.X(Math.min(xs[10], q3 + 1.5 * iqr))} y1={P.Y(3.3)} y2={P.Y(3.3)} stroke={C.ink} />
      <line x1={P.X(med)} x2={P.X(med)} y1={P.Y(3.7)} y2={P.Y(0.4)} stroke={C.green} strokeWidth="2.4" />
      <line x1={P.X(mean)} x2={P.X(mean)} y1={P.Y(3.7)} y2={P.Y(0.4)} stroke={C.red} strokeWidth="2.4" strokeDasharray="5 3" />
      <Label x={P.X(med)} y={P.Y(0.1)} anchor="middle" color={C.green} size={10}>중앙값</Label>
      <Label x={P.X(mean)} y={P.Y(0.1) + 0.1} anchor="middle" color={C.red} size={10}>{Math.abs(P.X(mean) - P.X(med)) > 30 ? "평균" : ""}</Label>
    </Frame>
  );
}

/* ── 표본분포: 표본이 클수록 표본평균이 덜 흔들린다(표준오차 σ/√n) ── */
export function Sampling({ p = {} }) {
  const [n, setN] = useState(p.n ?? 4);
  const clock = useClock({ period: 9 });
  const mu = 170, sd = 8;
  const draws = useMemo(() => { const r = rng(31 + n); return Array.from({ length: 400 }, () => { let s = 0; for (let i = 0; i < n; i++) s += mu + sd * gauss(r); return s / n; }); }, [n]);
  const k = Math.max(5, Math.floor((clock.t / 8.5) * draws.length));
  const P = plot({ x0: 140, x1: 200, y0: 0, y1: 0.36 });
  const se = sd / Math.sqrt(n), B = 40, w = 60 / B, cnt = new Array(B).fill(0);
  for (let i = 0; i < Math.min(k, draws.length); i++) { const b = Math.floor((draws[i] - 140) / w); if (b >= 0 && b < B) cnt[b]++; }
  const used = Math.min(k, draws.length);
  return (
    <Frame clock={clock} title="표본분포와 표준오차"
      read={<>키 N(170, 8²) 에서 {n}명씩 뽑은 평균 {used}개 · 회색 곡선 = 한 사람의 키 분포 · 막대 · 색 곡선 = 표본평균의 분포, 표준오차 8/√{n} = <b>{fmt(se, 2)}</b></>}
      controls={<Slider label="n" min={1} max={64} value={n} onChange={(v) => { setN(v); clock.reset(); }} />}>
      <Axes p={P} xl="cm" yl="" yfmt={() => ""} />
      {cnt.map((c, i) => { const d = c / (used * w); return <rect key={i} x={P.X(140 + i * w) + 0.5} width={Math.max(0.5, P.X(140 + (i + 1) * w) - P.X(140 + i * w) - 1)} y={P.Y(Math.min(d, 0.36))} height={P.Y(0) - P.Y(Math.min(d, 0.36))} fill={C.sp} opacity="0.55" />; })}
      <path d={P.path((x) => phi((x - mu) / sd) / sd)} fill="none" stroke={C.mut} strokeWidth="1.6" />
      <path d={P.path((x) => Math.min(0.36, phi((x - mu) / se) / se))} fill="none" stroke={C.red} strokeWidth="2" />
    </Frame>
  );
}

/* ── 신뢰구간: 「95%」는 구간 하나의 확률이 아니라 방법의 적중률 ── */
export function ConfInt({ p = {} }) {
  const [lev, setLev] = useState(p.level ?? 0.95);
  const [n, setN] = useState(p.n ?? 25);
  const clock = useClock({ period: 10 });
  const mu = 50, sd = 10, M = 50;
  const z = lev === 0.9 ? 1.645 : lev === 0.99 ? 2.576 : 1.96;
  const ints = useMemo(() => { const r = rng(77 + n); return Array.from({ length: 300 }, () => { let s = 0; for (let i = 0; i < n; i++) s += mu + sd * gauss(r); return s / n; }); }, [n]);
  const k = Math.min(300, Math.max(1, Math.floor((clock.t / 9.5) * 300)));
  const half = (z * sd) / Math.sqrt(n);
  const hit = ints.slice(0, k).filter((m) => Math.abs(m - mu) <= half).length;
  const P = plot({ x0: 38, x1: 62, y0: 0, y1: M + 1, pad: [8, 10, 18, 10] });
  const shown = ints.slice(Math.max(0, k - M), k);
  return (
    <Frame clock={clock} title="신뢰구간의 뜻"
      read={<>표본 {n}개로 만든 {fmt(lev * 100, 0)}% 구간 x̄ ± {z}·σ/√n 을 {k}번 — μ = 50 을 품은 구간 <b>{hit}</b>개(<b>{fmt((100 * hit) / k, 1)}%</b>) · 붉은 것이 놓친 구간</>}
      controls={<>
        <Seg value={lev} onChange={(v) => { setLev(v); clock.reset(); }} options={[[0.9, "90%"], [0.95, "95%"], [0.99, "99%"]]} />
        <Slider label="n" min={4} max={100} value={n} onChange={(v) => { setN(v); clock.reset(); }} />
      </>}>
      <line x1={P.X(mu)} x2={P.X(mu)} y1={P.t} y2={P.b} stroke={C.ink} strokeWidth="1.5" />
      {shown.map((m, i) => {
        const ok = Math.abs(m - mu) <= half;
        return <g key={i}><line x1={P.X(m - half)} x2={P.X(m + half)} y1={P.Y(i + 1)} y2={P.Y(i + 1)} stroke={ok ? C.sp : C.red} strokeWidth={ok ? 1.6 : 2.4} /><circle cx={P.X(m)} cy={P.Y(i + 1)} r="1.8" fill={ok ? C.sp : C.red} /></g>;
      })}
      <Label x={P.X(mu) + 4} y={P.b + 13} size={10}>μ = 50</Label>
    </Frame>
  );
}

/* ── 가설검정: 기각역 α · 관찰값 → p값 · 참 효과가 있을 때의 검정력 ── */
export function HypTest({ p = {} }) {
  const [alpha, setAlpha] = useState(p.alpha ?? 0.05);
  const [eff, setEff] = useState(p.eff ?? 2);
  const clock = useClock({ period: 8 });
  const zc = alpha === 0.01 ? 2.326 : alpha === 0.1 ? 1.282 : 1.645;
  const P = plot({ x0: -4, x1: 6.5, y0: 0, y1: 0.45 });
  const zobs = -1 + 5 * (0.5 - 0.5 * Math.cos((clock.t / 8) * 2 * Math.PI));
  const pval = 1 - Phi(zobs);
  const power = 1 - Phi(zc - eff);
  const shade = (f, a, b, col, op) => {
    let d = `M${P.X(a)} ${P.Y(0)}`;
    for (let i = 0; i <= 60; i++) { const x = a + ((b - a) * i) / 60; d += `L${P.X(x).toFixed(1)} ${P.Y(f(x)).toFixed(1)}`; }
    return <path d={d + `L${P.X(b)} ${P.Y(0)}Z`} fill={col} opacity={op} />;
  };
  return (
    <Frame clock={clock} title="가설검정"
      read={<>단측 z검정 · 유의수준 α = <b>{alpha}</b> → 기각역 z &gt; <b>{zc}</b> · 관찰 z = <b>{fmt(zobs, 2)}</b> → p값 <b>{fmt(pval, 4)}</b>{pval < alpha ? " — 기각" : " — 기각 못 함"} · 참 효과 {fmt(eff, 1)} 일 때 검정력 1 − β = <b>{fmt(power * 100, 1)}%</b></>}
      controls={<>
        <Seg value={alpha} onChange={setAlpha} options={[[0.1, "α 0.10"], [0.05, "0.05"], [0.01, "0.01"]]} />
        <Slider label="효과" min={0} max={4} step={0.1} value={eff} onChange={setEff} />
      </>}>
      <Axes p={P} xl="z" yl="" yfmt={() => ""} />
      {shade((x) => phi(x - eff), zc, 6.5, C.green, 0.25)}
      {shade(phi, zc, 6.5, C.red, 0.45)}
      {shade(phi, zobs, 6.5, C.gold, 0.35)}
      <path d={P.path(phi)} fill="none" stroke={C.ink} strokeWidth="2" />
      <path d={P.path((x) => phi(x - eff))} fill="none" stroke={C.green} strokeWidth="2" strokeDasharray="5 3" />
      <line x1={P.X(zc)} x2={P.X(zc)} y1={P.t} y2={P.b} stroke={C.red} />
      <line x1={P.X(zobs)} x2={P.X(zobs)} y1={P.t + 10} y2={P.b} stroke={C.gold} strokeWidth="2" />
      <Label x={P.X(0)} y={P.t + 12} anchor="middle" size={10}>H₀ 아래 분포</Label>
      <Label x={P.X(eff) + 8} y={P.t + 26} size={10} color={C.green} bg>참 효과 분포</Label>
    </Frame>
  );
}

/* ── 최소제곱 회귀: 잔차 제곱의 합이 가장 작은 직선 ── */
export function Regression({ p = {} }) {
  const clock = useClock({ period: 10 });
  const pts = useMemo(() => { const r = rng(3); return Array.from({ length: 14 }, (_, i) => { const x = 0.5 + i * 0.7; return [x, 1.2 + 0.55 * x + 0.9 * gauss(r)]; }); }, []);
  const n = pts.length, mx = pts.reduce((s, q) => s + q[0], 0) / n, my = pts.reduce((s, q) => s + q[1], 0) / n;
  let sxy = 0, sxx = 0;
  for (const [x, y] of pts) { sxy += (x - mx) * (y - my); sxx += (x - mx) ** 2; }
  const b1 = sxy / sxx, b0 = my - b1 * mx;
  // 직선이 기울기를 바꿔 가며 흔들리다 최소제곱 직선에 멈춘다
  const ph = clock.t / 10, wob = ph < 0.75 ? Math.sin(ph * 4 * Math.PI) * (1 - ph / 0.75) : 0;
  const m = b1 + 0.6 * wob, c = my - m * mx;
  const sse = pts.reduce((s, [x, y]) => s + (y - (c + m * x)) ** 2, 0), sseMin = pts.reduce((s, [x, y]) => s + (y - (b0 + b1 * x)) ** 2, 0);
  const sst = pts.reduce((s, [, y]) => s + (y - my) ** 2, 0);
  const P = plot({ x0: 0, x1: 10, y0: 0, y1: 8.5 });
  const px = (P.r - P.l) / 10, py = (P.b - P.t) / 8.5;
  return (
    <Frame clock={clock} title="최소제곱 회귀"
      read={<>잔차 제곱합 SSE = <b>{fmt(sse, 2)}</b> (최소 {fmt(sseMin, 2)}) · 최소제곱 직선 ŷ = <b>{fmt(b0, 2)} + {fmt(b1, 3)}x</b> · 결정계수 R² = 1 − SSE/SST = <b>{fmt(1 - sseMin / sst, 3)}</b> · 사각형 = 잔차²</>}>
      <Axes p={P} />
      {pts.map(([x, y], i) => {
        const yh = c + m * x, e = y - yh, side = Math.abs(e) * py;
        return (
          <g key={i}>
            <rect x={P.X(x)} y={Math.min(P.Y(y), P.Y(yh))} width={Math.min(side * (px / py), 60)} height={side} fill={C.gold} opacity="0.18" stroke={C.gold} strokeWidth="0.6" />
            <line x1={P.X(x)} x2={P.X(x)} y1={P.Y(y)} y2={P.Y(yh)} stroke={C.red} strokeWidth="1.2" />
            <circle cx={P.X(x)} cy={P.Y(y)} r="3.8" fill={C.sp} />
          </g>
        );
      })}
      <path d={P.path((x) => c + m * x)} fill="none" stroke={C.ink} strokeWidth="2.2" />
      <circle cx={P.X(mx)} cy={P.Y(my)} r="4" fill={C.card} stroke={C.ink} strokeWidth="1.5" />
      <Label x={P.X(mx) + 6} y={P.Y(my) + 14} size={10}>(x̄, ȳ) 를 꼭 지난다</Label>
    </Frame>
  );
}

/* ── 분산분석: 집단 사이 흩어짐 / 집단 안 흩어짐 = F ── */
export function Anova({ p = {} }) {
  const [gap, setGap] = useState(p.gap ?? 1.2);
  const [noise, setNoise] = useState(p.noise ?? 1);
  const clock = useClock({ period: 6 });
  const k = 3, m = 10;
  const data = useMemo(() => { const r = rng(12); return Array.from({ length: k }, () => Array.from({ length: m }, () => gauss(r))); }, []);
  const groups = data.map((g, i) => g.map((z) => 5 + (i - 1) * gap + noise * z));
  const means = groups.map((g) => g.reduce((a, b) => a + b, 0) / m), grand = means.reduce((a, b) => a + b, 0) / k;
  const ssb = m * means.reduce((s, x) => s + (x - grand) ** 2, 0), ssw = groups.reduce((s, g, i) => s + g.reduce((t, x) => t + (x - means[i]) ** 2, 0), 0);
  const F = (ssb / (k - 1)) / (ssw / (k * m - k));
  const P = plot({ x0: 0.3, x1: 3.7, y0: 0, y1: 10, pad: [8, 10, 18, 26] });   // 집단은 1 · 2 · 3 자리(세로축과 겹치지 않게)
  const jit = (j) => ((j * 37) % 11) / 11 - 0.5;
  return (
    <Frame clock={clock} title="분산분석"
      read={<>집단 평균의 차이(사이) 대 집단 안의 흩어짐(안) · F = (SSB/(k − 1)) ÷ (SSW/(N − k)) = <b>{fmt(F, 2)}</b>{F > 3.35 ? " — 5% 기준값 3.35 를 넘는다: 평균이 모두 같다고 보기 어렵다" : " — 기준값 3.35 보다 작다: 우연으로도 이만큼은 흔하다"}</>}
      controls={<>
        <Slider label="평균 차" min={0} max={3} step={0.1} value={gap} onChange={setGap} />
        <Slider label="흩어짐" min={0.3} max={2.5} step={0.1} value={noise} onChange={setNoise} />
      </>}>
      <Axes p={P} xl="" yl="값" xt={[1, 2, 3]} xfmt={(v) => "집단 " + "ABC"[v - 1]} grid={false} />
      <line x1={P.l} x2={P.r} y1={P.Y(grand)} y2={P.Y(grand)} stroke={C.mut} strokeDasharray="4 3" />
      {groups.map((g, i) => (
        <g key={i}>
          {g.map((y, j) => <circle key={j} cx={P.X(i + 1 + 0.35 * jit(j))} cy={P.Y(clamp(y, 0, 10))} r="3.2" fill={[C.sp, C.red, C.blue][i]} opacity="0.65" />)}
          <line x1={P.X(i + 0.7)} x2={P.X(i + 1.3)} y1={P.Y(means[i])} y2={P.Y(means[i])} stroke={C.ink} strokeWidth="2.6" />
        </g>
      ))}
    </Frame>
  );
}

/* ── 베이즈 갱신: 베타 사전분포 + 동전 자료 → 사후분포 ── */
function betaPdf(x, a, b) {
  if (x <= 0 || x >= 1) return 0;
  const lg = (z) => { // 스털링 로그감마
    const c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
    let y = z, t = z + 5.5; t -= (z + 0.5) * Math.log(t); let s = 1.000000000190015; for (const v of c) s += v / ++y; return -t + Math.log(2.5066282746310005 * s / z);
  };
  return Math.exp((a - 1) * Math.log(x) + (b - 1) * Math.log(1 - x) - (lg(a) + lg(b) - lg(a + b)));
}
export function BetaUpdate({ p = {} }) {
  const [a0, setA] = useState(p.a ?? 2);
  const [b0, setB] = useState(p.b ?? 2);
  const clock = useClock({ period: 12 });
  const flips = useMemo(() => { const r = rng(21); return Array.from({ length: 60 }, () => (r() < 0.7 ? 1 : 0)); }, []);
  const k = Math.min(60, Math.floor((clock.t / 11) * 61));
  const h = flips.slice(0, k).reduce((s, v) => s + v, 0);
  const a = a0 + h, b = b0 + (k - h);
  const top = Math.max(3, betaPdf(Math.min(0.999, Math.max(0.001, (a - 1) / (a + b - 2 || 1))), a, b) * 1.1);
  const P = plot({ x0: 0, x1: 1, y0: 0, y1: top });
  return (
    <Frame clock={clock} title="베이즈 갱신"
      read={<>사전 Beta({a0}, {b0}) · 던진 {k}번 중 앞 {h}번 → 사후 Beta({a}, {b}), 평균 <b>{fmt(a / (a + b), 3)}</b> · 자료가 쌓일수록 사전 믿음보다 자료가 이기고, 분포가 좁아진다(참값 0.7)</>}
      controls={<>
        <Slider label="사전 α" min={0.5} max={20} step={0.5} value={a0} onChange={setA} />
        <Slider label="사전 β" min={0.5} max={20} step={0.5} value={b0} onChange={setB} />
      </>}>
      <Axes p={P} xl="θ" yl="" yfmt={() => ""} />
      <line x1={P.X(0.7)} x2={P.X(0.7)} y1={P.t} y2={P.b} stroke={C.green} strokeDasharray="4 3" />
      <path d={P.path((x) => betaPdf(x, a0, b0), 0.001, 0.999)} fill="none" stroke={C.mut} strokeWidth="1.6" strokeDasharray="4 3" />
      <path d={P.path((x) => Math.min(top, betaPdf(x, a, b)), 0.001, 0.999)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <g>{flips.slice(0, k).map((v, i) => <circle key={i} cx={P.l + 6 + (i % 30) * 9.2} cy={P.t + 6 + Math.floor(i / 30) * 9} r="3.2" fill={v ? C.gold : C.mut} />)}</g>
    </Frame>
  );
}

/* ── 붓스트랩: 가진 표본에서 다시 뽑아(복원) 통계량의 흔들림을 잰다 ── */
export function Bootstrap({ p = {} }) {
  const clock = useClock({ period: 10 });
  const data = useMemo(() => { const r = rng(55); return Array.from({ length: 20 }, () => Math.round((-Math.log(Math.max(1e-9, r())) * 30 + 10) * 10) / 10); }, []);
  const boots = useMemo(() => { const r = rng(8); return Array.from({ length: 600 }, () => { const s = Array.from({ length: 20 }, () => data[Math.floor(r() * 20)]).sort((a, b) => a - b); return (s[9] + s[10]) / 2; }); }, [data]);
  const k = Math.max(10, Math.floor((clock.t / 9.5) * 600));
  const sorted = boots.slice(0, k).sort((a, b) => a - b);
  const lo = sorted[Math.floor(0.025 * sorted.length)], hi = sorted[Math.min(sorted.length - 1, Math.floor(0.975 * sorted.length))];
  const P = plot({ x0: 10, x1: 70, y0: 0, y1: 1 });
  const B = 30, w = 2, cnt = new Array(B).fill(0);
  for (const v of sorted) { const b = Math.floor((v - 10) / w); if (b >= 0 && b < B) cnt[b]++; }
  const mx = Math.max(...cnt, 1);
  const med0 = [...data].sort((a, b) => a - b);
  return (
    <Frame clock={clock} title="붓스트랩"
      read={<>대기 시간 20개의 중앙값 <b>{fmt((med0[9] + med0[10]) / 2, 1)}</b>분 · 같은 20개에서 복원추출로 {k}번 다시 뽑아 중앙값을 구하면 — 가운데 95% 가 [<b>{fmt(lo, 1)}</b>, <b>{fmt(hi, 1)}</b>] (공식 없이 얻는 신뢰구간)</>}>
      <Axes p={P} xl="분" yl="" yfmt={() => ""} />
      {cnt.map((c, i) => <rect key={i} x={P.X(10 + i * w) + 0.5} width={P.X(10 + (i + 1) * w) - P.X(10 + i * w) - 1} y={P.Y((0.85 * c) / mx)} height={P.Y(0) - P.Y((0.85 * c) / mx)} fill={C.sp} opacity="0.55" />)}
      <rect x={P.X(lo)} width={Math.max(1, P.X(hi) - P.X(lo))} y={P.Y(0.97)} height="6" fill={C.red} opacity="0.7" />
      {data.map((v, i) => <circle key={i} cx={P.X(Math.min(69, v))} cy={P.Y(0.06)} r="2.6" fill={C.ink} opacity="0.7" />)}
    </Frame>
  );
}
