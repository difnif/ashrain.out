// 금융수학 그림 — 단리 · 복리 · 연속복리 · 현재가치와 NPV · IRR · 대출 상환표 · 채권 값과 듀레이션 · 두 자산 포트폴리오(효율적 투자선 · 자본시장선) · 주가의 기하 브라운 운동 · 옵션 값(블랙-숄즈) · 이항 나무
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, ease, rng, gauss, useClock } from "./kit.jsx";
import { Phi } from "./prob.jsx";

const comma = (v) => fmt(Math.round(v), 0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");

/* ── 복리: 이자에도 이자가 붙는다 — 단리 · 해마다 복리 · 연속복리, 72 의 법칙 ── */
export function Compound({ p = {} }) {
  const [r, setR] = useState(p.r ?? 7);
  const clock = useClock({ period: 12, rest: 10.5 });
  const rr = r / 100, Y = 30 * clamp(clock.t / 10, 0, 1);
  const simple = (t) => 100 * (1 + rr * t), yearly = (t) => 100 * Math.pow(1 + rr, t), cont = (t) => 100 * Math.exp(rr * t);
  const top = cont(30) * 1.06, t2 = Math.log(2) / Math.log(1 + rr);
  const P = plot({ x0: 0, x1: 30, y0: 0, y1: top, pad: [12, 14, 24, 40] });
  return (
    <Frame clock={clock} title="단리와 복리"
      read={<>100 을 연 {fmt(r, 1)} % 로 {fmt(Y, 1)} 년: 단리 {fmt(simple(Y), 0)} · 해마다 복리 <b>{fmt(yearly(Y), 0)}</b> · 연속복리 {fmt(cont(Y), 0)} · 두 배가 되는 때: 72 ÷ {fmt(r, 1)} ≈ {fmt(72 / r, 1)} 년 (정확히 ln 2 ÷ ln(1 + r) = <b>{fmt(t2, 2)}</b> 년) · 단리는 직선, 복리는 지수곡선 — 시간이 길수록 크게 벌어진다</>}
      controls={<Slider label="연 이자율" min={1} max={15} step={0.5} value={r} onChange={(v) => { setR(v); clock.reset(); }} show={(v) => fmt(v, 1) + " %"} />}>
      <Axes p={P} xl="년" yl="" xt={[10, 20, 30]} yfmt={(v) => fmt(v, 0)} />
      <path d={P.path(simple, 0, 30)} fill="none" stroke={C.mut} strokeWidth="1.8" strokeDasharray="5 3" />
      <path d={P.path(cont, 0, 30)} fill="none" stroke={C.gold} strokeWidth="1.6" />
      <path d={P.path(yearly, 0, 30)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      {t2 <= 30 && <><line x1={P.X(t2)} x2={P.X(t2)} y1={P.Y(200)} y2={P.Y(0)} stroke={C.red} strokeDasharray="3 3" /><Label x={P.X(t2) + 4} y={P.Y(200) - 5} size={9.5} color={C.red} bg>두 배</Label></>}
      <circle cx={P.X(Y)} cy={P.Y(yearly(Y))} r="5" fill={C.red} />
      <circle cx={P.X(Y)} cy={P.Y(simple(Y))} r="3.5" fill={C.mut} />
      <Label x={P.X(29.5)} y={P.Y(simple(29.5)) - 5} size={9.5} color={C.mut} anchor="end" bg>단리</Label>
      <Label x={P.X(25)} y={P.Y(yearly(25)) - 6} size={9.5} color={C.sp} anchor="end" bg>복리</Label>
    </Frame>
  );
}

/* ── 현재가치와 NPV: 미래의 돈을 (1 + r)ᵗ 로 나눠 오늘로 — NPV = 0 인 할인율이 IRR ── */
const FLOWS = { even: [-1000, 300, 300, 300, 300, 300], late: [-1000, 50, 100, 250, 450, 650] };
export function NPV({ p = {} }) {
  const [r, setR] = useState(p.r ?? 10);
  const [kind, setKind] = useState(p.flow === "late" ? "late" : "even");
  const clock = useClock({ period: 9, rest: 7 });
  const cf = FLOWS[kind];
  const npv = (x) => cf.reduce((s, c, t) => s + c / Math.pow(1 + x, t), 0);
  const irr = useMemo(() => { let lo = 0, hi = 1; for (let i = 0; i < 60; i++) { const m = (lo + hi) / 2; if (npv(m) > 0) lo = m; else hi = m; } return (lo + hi) / 2; }, [kind]); // eslint-disable-line react-hooks/exhaustive-deps
  const rr = r / 100, v = npv(rr);
  const shrink = (t) => ease(clamp((clock.t - 0.4 - t * 0.9) / 0.9, 0, 1));
  const P = plot({ x0: -0.6, x1: 5.6, y0: -1100, y1: 700, pad: [12, 136, 24, 40] });
  const R = plot({ x0: 0, x1: 30, y0: -500, y1: 700, pad: [24, 10, 24, 258] });
  return (
    <Frame clock={clock} title="현재가치와 NPV"
      read={<>할인율 {fmt(r, 1)} %: t 년 뒤의 돈 C 는 오늘 C/(1 + r)ᵗ (회색 → 색 막대) · 합 NPV = <b>{fmt(v, 1)}</b> {v > 0 ? "> 0 → 할 만한 사업" : "< 0 → 하지 않는다"} · IRR(NPV = 0 이 되는 할인율) = <b>{fmt(irr * 100, 2)} %</b> — 돈을 빌리는 비용이 이보다 낮으면 채택 · 오른쪽 = 할인율에 따른 NPV</>}
      controls={<>
        <Slider label="할인율 r" min={0} max={25} step={0.5} value={r} onChange={setR} show={(x) => fmt(x, 1) + " %"} />
        <Seg value={kind} onChange={(x) => { setKind(x); clock.reset(); }} options={[["even", "고른 흐름"], ["late", "뒤에 몰린 흐름"]]} />
      </>}>
      <Axes p={P} xl="" yl="" xt={[0, 1, 2, 3, 4, 5]} yt={[-1000, -500, 500]} yfmt={(x) => fmt(x, 0)} xfmt={(x) => fmt(x, 0) + "년"} />
      {cf.map((c, t) => { const pv = c / Math.pow(1 + rr, t), h = c + (pv - c) * (t ? shrink(t) : 1);
        return (<g key={t}>
          <rect x={P.X(t - 0.32)} y={P.Y(Math.max(c, 0))} width={P.X(t + 0.32) - P.X(t - 0.32)} height={Math.abs(P.Y(c) - P.Y(0))} fill="none" stroke={C.mut} strokeDasharray="3 2" />
          <rect x={P.X(t - 0.32)} y={P.Y(Math.max(h, 0))} width={P.X(t + 0.32) - P.X(t - 0.32)} height={Math.abs(P.Y(h) - P.Y(0))} fill={c < 0 ? C.red : C.sp} opacity="0.75" />
        </g>); })}
      <Axes p={R} xl="r %" yl="NPV" grid={false} xt={[10, 20, 30]} yt={[-500, 500]} xfmt={(x) => fmt(x, 0)} yfmt={(x) => fmt(x, 0)} />
      <path d={R.path((x) => npv(x / 100), 0, 30)} fill="none" stroke={C.sp} strokeWidth="2" />
      <circle cx={R.X(irr * 100)} cy={R.Y(0)} r="3.5" fill="none" stroke={C.green} strokeWidth="1.6" />
      <circle cx={R.X(r)} cy={R.Y(clamp(v, -500, 700))} r="4" fill={C.red} />
      <text x={R.X(irr * 100)} y={R.Y(0) + 14} textAnchor="middle" fontSize="9" fill={C.green}>IRR</text>
    </Frame>
  );
}

/* ── 대출 상환: 원리금 균등은 이자가 점점 줄고 원금이 는다 — 원금 균등과 견주기 ── */
export function Amort({ p = {} }) {
  const [r, setR] = useState(p.r ?? 5);
  const [N, setN] = useState(p.N ?? 20);
  const [mode, setMode] = useState(p.mode === "prin" ? "prin" : "pay");
  const clock = useClock({ period: 11, rest: 5 });
  const L = 10000, rr = r / 100;
  const rows = useMemo(() => {
    const A = (L * rr) / (1 - Math.pow(1 + rr, -N)), out = []; let B = L;
    for (let k = 1; k <= N; k++) { const I = B * rr, Pp = mode === "pay" ? A - I : L / N; B -= Pp; out.push({ I, Pp, pay: I + Pp, B: Math.max(0, B) }); }
    return out;
  }, [r, N, mode]); // eslint-disable-line react-hooks/exhaustive-deps
  const k = Math.min(N, 1 + Math.floor((clamp(clock.t, 0, 9.99) / 10) * N)), row = rows[k - 1];
  const totI = rows.reduce((s, x) => s + x.I, 0), top = Math.max(...rows.map((x) => x.pay)) * 1.15;
  const P = plot({ x0: 0.3, x1: N + 0.7, y0: 0, y1: top, pad: [12, 14, 24, 40] });
  const w = (P.X(1) - P.X(0)) * 0.72;
  return (
    <Frame clock={clock} title="대출 상환표"
      read={<>1 억 원 · 연 {fmt(r, 1)} % · {N} 년 · {mode === "pay" ? "원리금 균등(해마다 같은 돈)" : "원금 균등(원금을 똑같이 나눔)"}: <b>{k}</b> 년째 낸 돈 {comma(row.pay)} 만 원 = 이자 <b>{comma(row.I)}</b>(빨강) + 원금 <b>{comma(row.Pp)}</b>(파랑) · 남은 빚 {comma(row.B)} 만 원 · 총이자 <b>{comma(totI)}</b> 만 원 — 이자는 남은 빚에만 붙어서 갈수록 준다{mode === "pay" ? " · 원리금 균등 A = L·r/(1 − (1 + r)⁻ᴺ)" : " · 원금 균등은 처음이 무겁지만 총이자가 적다"}</>}
      controls={<>
        <Slider label="연 이자율" min={1} max={10} step={0.5} value={r} onChange={setR} show={(x) => fmt(x, 1) + " %"} />
        <Slider label="기간" min={5} max={30} step={1} value={N} onChange={setN} show={(x) => x + " 년"} />
        <Seg value={mode} onChange={setMode} options={[["pay", "원리금 균등"], ["prin", "원금 균등"]]} />
      </>}>
      <Axes p={P} xl="년" yl="만 원" grid={false} xfmt={(x) => fmt(x, 0)} yfmt={(x) => fmt(x, 0)} />
      {rows.map((x, i) => (
        <g key={i} opacity={i + 1 === k ? 1 : 0.6}>
          <rect x={P.X(i + 1) - w / 2} y={P.Y(x.Pp)} width={w} height={P.Y(0) - P.Y(x.Pp)} fill={C.blue} />
          <rect x={P.X(i + 1) - w / 2} y={P.Y(x.pay)} width={w} height={P.Y(x.Pp) - P.Y(x.pay)} fill={C.red} />
        </g>
      ))}
      <path d={P.poly([[0.5, top * 0.92], ...rows.map((x, i) => [i + 1, (x.B / L) * top * 0.92])])} fill="none" stroke={C.mut} strokeWidth="1.4" strokeDasharray="4 3" />
      <Label x={P.X(N * 0.25)} y={P.Y(top * 0.92 * 0.78) - 4} size={9.5} color={C.mut} bg>남은 빚</Label>
      <line x1={P.X(k)} x2={P.X(k)} y1={P.t} y2={P.b} stroke={C.ink} strokeWidth="0.8" strokeDasharray="2 3" />
    </Frame>
  );
}

/* ── 채권: 수익률이 오르면 값이 내린다 — 접선(듀레이션)과 휘어짐(볼록성) ── */
export function Bond({ p = {} }) {
  const [cr, setCr] = useState(p.coupon ?? 3);
  const [T, setT] = useState(p.T ?? 10);
  const clock = useClock({ period: 12 });
  const y = 0.01 + 0.11 * (0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 12));
  const price = (yy) => { let s = 0; for (let t = 1; t <= T; t++) s += cr / Math.pow(1 + yy, t); return s + 100 / Math.pow(1 + yy, T); };
  const Pv = price(y);
  let D = 0; for (let t = 1; t <= T; t++) D += (t * (cr + (t === T ? 100 : 0))) / Math.pow(1 + y, t); D /= Pv;
  const Dm = D / (1 + y);
  const P = plot({ x0: 0, x1: 0.14, y0: 0, y1: price(0) * 1.08, pad: [12, 14, 24, 36] });
  const tan = (yy) => Pv * (1 - Dm * (yy - y));
  return (
    <Frame clock={clock} title="채권 값과 듀레이션"
      read={<>액면 100, 표면이자 {cr} %, 만기 {T} 년 · 시장 수익률 {fmt(y * 100, 2)} %: 값 = 이자와 원금을 그 수익률로 할인한 합 = <b>{fmt(Pv, 2)}</b> · 듀레이션 {fmt(D, 2)} 년(현금이 들어오는 평균 시점), 수정 듀레이션 <b>{fmt(Dm, 2)}</b> → 수익률이 1 %p 오르면 값이 약 {fmt(Dm, 1)} % 내린다(접선) — 실제 곡선은 볼록해서 덜 내리고 더 오른다 · 만기가 길고 표면이자가 낮을수록 금리에 민감</>}
      controls={<>
        <Seg value={cr} onChange={setCr} options={[[0, "이자 0 %"], [3, "3 %"], [6, "6 %"]]} />
        <Slider label="만기" min={1} max={30} step={1} value={T} onChange={setT} show={(x) => x + " 년"} />
      </>}>
      <Axes p={P} xl="수익률" yl="값" xt={[0.04, 0.08, 0.12]} xfmt={(x) => fmt(x * 100, 0) + " %"} yfmt={(x) => fmt(x, 0)} />
      <path d={P.path(price, 0, 0.14)} fill="none" stroke={C.sp} strokeWidth="2.5" />
      <path d={P.path(tan, Math.max(0, y - 0.04), Math.min(0.14, y + 0.04))} fill="none" stroke={C.red} strokeWidth="1.6" strokeDasharray="5 3" />
      <line x1={P.X(y)} x2={P.X(y)} y1={P.Y(Pv)} y2={P.Y(0)} stroke={C.mut} strokeDasharray="2 3" />
      <circle cx={P.X(y)} cy={P.Y(Pv)} r="5" fill={C.red} />
      <line x1={P.l} x2={P.r} y1={P.Y(100)} y2={P.Y(100)} stroke={C.mut} strokeWidth="0.8" />
      <Label x={P.r - 4} y={P.Y(100) - 4} size={9.5} color={C.mut} anchor="end" bg>액면 100</Label>
      <Label x={P.X(Math.min(0.13, y + 0.035))} y={P.Y(tan(Math.min(0.13, y + 0.035))) + 14} size={9.5} color={C.red} anchor="end" bg>접선(듀레이션)</Label>
    </Frame>
  );
}

/* ── 두 자산 포트폴리오: 섞으면 위험이 줄어든다(상관이 낮을수록) — 효율적 투자선과 자본시장선 ── */
export function Frontier({ p = {} }) {
  const [rho, setRho] = useState(p.rho ?? 0.2);
  const clock = useClock({ period: 10 });
  const mA = 6, sA = 10, mB = 12, sB = 20, rf = 3;
  const sd = (w) => Math.sqrt(Math.max(0, (1 - w) ** 2 * sA * sA + w * w * sB * sB + 2 * w * (1 - w) * rho * sA * sB)), mu = (w) => (1 - w) * mA + w * mB;
  const wNow = 0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10);
  const { wmv, wt } = useMemo(() => {
    let wmv = 0, wt = 0, best = Infinity, sh = -Infinity;
    for (let w = 0; w <= 1.0001; w += 0.002) { const s = sd(w); if (s < best) { best = s; wmv = w; } const q = (mu(w) - rf) / s; if (q > sh) { sh = q; wt = w; } }
    return { wmv, wt };
  }, [rho]); // eslint-disable-line react-hooks/exhaustive-deps
  const P = plot({ x0: 0, x1: 24, y0: 0, y1: 14, pad: [12, 14, 24, 30] });
  const sharpe = (mu(wt) - rf) / sd(wt);
  return (
    <Frame clock={clock} title="분산투자와 효율적 투자선"
      read={<>A(수익 6 %, 위험 10 %)와 B(12 %, 20 %), 상관 ρ = <b>{fmt(rho, 2)}</b> · B 를 {fmt(wNow * 100, 0)} % 섞으면 기대수익 {fmt(mu(wNow), 2)} %, 위험(표준편차) <b>{fmt(sd(wNow), 2)} %</b> — 기대수익은 평균대로지만 위험은 평균보다 작다 · 상관이 낮을수록 곡선이 왼쪽으로 휜다(ρ = −1 이면 위험 0 도 가능) · 최소분산 B {fmt(wmv * 100, 0)} % · 무위험 3 % 에서 그은 접선(자본시장선)의 접점 B {fmt(wt * 100, 0)} % — 샤프 비율 {fmt(sharpe, 2)} 이 가장 크다</>}
      controls={<Slider label="상관 ρ" min={-1} max={1} step={0.05} value={rho} onChange={setRho} />}>
      <Axes p={P} xl="위험 σ (%)" yl="수익 (%)" />
      <path d={P.curve(sd, mu, 0, 1, 120)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <path d={P.path((s) => rf + sharpe * s, 0, 24)} fill="none" stroke={C.green} strokeWidth="1.6" strokeDasharray="5 3" />
      <circle cx={P.X(0)} cy={P.Y(rf)} r="3.5" fill={C.green} />
      <circle cx={P.X(sA)} cy={P.Y(mA)} r="4.5" fill={C.blue} />
      <circle cx={P.X(sB)} cy={P.Y(mB)} r="4.5" fill={C.gold} />
      <circle cx={P.X(sd(wmv))} cy={P.Y(mu(wmv))} r="3.5" fill="none" stroke={C.ink} strokeWidth="1.5" />
      <circle cx={P.X(sd(wt))} cy={P.Y(mu(wt))} r="4" fill="none" stroke={C.green} strokeWidth="2" />
      <circle cx={P.X(sd(wNow))} cy={P.Y(mu(wNow))} r="5" fill={C.red} />
      <Label x={P.X(sA) + 7} y={P.Y(mA) + 4} size={10} color={C.blue} bg>A</Label>
      <Label x={P.X(sB) + 7} y={P.Y(mB) + 4} size={10} color={C.gold} bg>B</Label>
      <Label x={P.X(0) + 6} y={P.Y(rf) - 5} size={9.5} color={C.green} bg>무위험</Label>
    </Frame>
  );
}

/* ── 주가의 기하 브라운 운동: 길은 제멋대로, 1 년 뒤 값은 로그정규 — 평균 > 가운데값 ── */
export function GBM({ p = {} }) {
  const [mu, setMu] = useState(p.mu ?? 8);
  const [sg, setSg] = useState(p.sigma ?? 30);
  const clock = useClock({ period: 10, rest: 9.5 });
  const m = mu / 100, s = sg / 100, S0 = 100, n = 120;
  const sim = useMemo(() => {
    const r = rng(23), paths = [];
    for (let j = 0; j < 6; j++) { let x = S0; const pts = [x]; for (let i = 0; i < n; i++) { x *= Math.exp((m - (s * s) / 2) / n + (s / Math.sqrt(n)) * gauss(r)); pts.push(x); } paths.push(pts); }
    const ends = []; for (let j = 0; j < 600; j++) ends.push(S0 * Math.exp(m - (s * s) / 2 + s * gauss(r)));
    return { paths, ends };
  }, [mu, sg]); // eslint-disable-line react-hooks/exhaustive-deps
  const lo = S0 * Math.exp(m - (s * s) / 2 - 2.6 * s), hi = S0 * Math.exp(m - (s * s) / 2 + 2.6 * s);
  const P = plot({ x0: 0, x1: 1, y0: lo, y1: hi, pad: [12, 104, 24, 36] });
  const k = Math.min(n, Math.round(clamp(clock.t / 8, 0, 1) * n));
  const nb = 24, bins = Array(nb).fill(0);
  for (const e of sim.ends) { const b = Math.floor(((e - lo) / (hi - lo)) * nb); if (b >= 0 && b < nb) bins[b]++; }
  const bmax = Math.max(...bins), mean = S0 * Math.exp(m), med = S0 * Math.exp(m - (s * s) / 2);
  const hx = 262, hw = 88;
  return (
    <Frame clock={clock} title="주가의 기하 브라운 운동"
      read={<>기대수익 μ = {fmt(mu, 0)} %, 변동성 σ = {fmt(sg, 0)} %: 1 년 뒤 평균 S₀e<sup>μ</sup> = <b>{fmt(mean, 1)}</b>, 가운데값 S₀e<sup>μ − σ²/2</sup> = <b>{fmt(med, 1)}</b> — 변동성이 크면 가운데값이 평균보다 더 낮다(오른쪽으로 긴 로그정규 꼬리) · 오른쪽 = 600 번 뽑은 1 년 뒤 값 · 수익률(로그)은 정규, 값은 로그정규</>}
      controls={<>
        <Slider label="기대수익 μ" min={-10} max={25} step={1} value={mu} onChange={setMu} show={(x) => x + " %"} />
        <Slider label="변동성 σ" min={5} max={60} step={1} value={sg} onChange={setSg} show={(x) => x + " %"} />
      </>}>
      <Axes p={P} xl="년" yl="값" xt={[0.5, 1]} yfmt={(x) => fmt(x, 0)} />
      <line x1={P.l} x2={P.r} y1={P.Y(S0)} y2={P.Y(S0)} stroke={C.mut} strokeDasharray="3 3" />
      {sim.paths.map((pts, j) => <path key={j} d={P.poly(pts.slice(0, k + 1).map((v, i) => [i / n, clamp(v, lo, hi)]))} fill="none" stroke={[C.sp, C.red, C.gold, C.green, C.violet, C.blue][j]} strokeWidth="1.5" opacity="0.9" />)}
      {bins.map((c, b) => <rect key={b} x={hx} y={P.Y(lo + ((b + 1) / nb) * (hi - lo))} width={(c / bmax) * hw} height={Math.max(0.5, P.Y(lo + (b / nb) * (hi - lo)) - P.Y(lo + ((b + 1) / nb) * (hi - lo)) - 0.6)} fill={C.sp} opacity="0.55" />)}
      <line x1={hx} x2={hx + hw} y1={P.Y(mean)} y2={P.Y(mean)} stroke={C.red} strokeWidth="1.5" />
      <line x1={hx} x2={hx + hw} y1={P.Y(med)} y2={P.Y(med)} stroke={C.ink} strokeWidth="1.2" strokeDasharray="3 2" />
      <text x={hx + hw} y={P.Y(mean) - 3} textAnchor="end" fontSize="9" fill={C.red}>평균</text>
      <text x={hx + hw} y={Math.max(P.Y(med) + 10, P.Y(mean) + 12)} textAnchor="end" fontSize="9" fill={C.ink}>가운데값</text>
    </Frame>
  );
}

/* ── 옵션 값: 만기가 다가오면 블랙-숄즈 곡선이 만기 수익(꺾은선)으로 내려앉는다 ── */
export function bsPrice(S, K, r, sg, tau, call = true) {
  if (tau <= 1e-6) return call ? Math.max(S - K, 0) : Math.max(K - S, 0);
  const d1 = (Math.log(S / K) + (r + (sg * sg) / 2) * tau) / (sg * Math.sqrt(tau)), d2 = d1 - sg * Math.sqrt(tau);
  return call ? S * Phi(d1) - K * Math.exp(-r * tau) * Phi(d2) : K * Math.exp(-r * tau) * Phi(-d2) - S * Phi(-d1);
}
export function Option({ p = {} }) {
  const [sg, setSg] = useState(p.sigma ?? 25);
  const [kind, setKind] = useState(p.put ? "put" : "call");
  const clock = useClock({ period: 11 });
  const K = 100, r = 0.03, call = kind === "call", s = sg / 100;
  const tau = Math.max(0, 1 - clock.t / 9);
  const V = (S) => bsPrice(S, K, r, s, tau, call), pay = (S) => (call ? Math.max(S - K, 0) : Math.max(K - S, 0));
  const v100 = V(100), intr = pay(100);
  const P = plot({ x0: 50, x1: 150, y0: 0, y1: 55, pad: [12, 14, 24, 32] });
  return (
    <Frame clock={clock} title="옵션 값과 시간가치"
      read={<>행사가 100, 이자 3 %, 변동성 {sg} % · 만기까지 <b>{fmt(tau, 2)}</b> 년: 주가 100 일 때 {call ? "콜" : "풋"} 값 <b>{fmt(v100, 2)}</b> = 내재가치 {fmt(intr, 2)} + 시간가치 {fmt(v100 - intr, 2)} · 곡선(블랙-숄즈) − 꺾은선(만기 수익) = 아직 남은 기회의 값 — 만기가 다가올수록 녹는다(세타) · 변동성이 크면 값도 크다(베가)</>}
      controls={<>
        <Slider label="변동성 σ" min={10} max={60} step={1} value={sg} onChange={setSg} show={(x) => x + " %"} />
        <Seg value={kind} onChange={setKind} options={[["call", "콜(살 권리)"], ["put", "풋(팔 권리)"]]} />
      </>}>
      <Axes p={P} xl="주가 S" yl="값" xt={[75, 100, 125, 150]} xfmt={(x) => fmt(x, 0)} yfmt={(x) => fmt(x, 0)} />
      <path d={P.path(pay, 50, 150)} fill="none" stroke={C.ink} strokeWidth="1.6" strokeDasharray="5 3" />
      <path d={P.path(V, 50, 150)} fill="none" stroke={C.sp} strokeWidth="2.5" />
      <line x1={P.X(100)} x2={P.X(100)} y1={P.Y(v100)} y2={P.Y(intr)} stroke={C.red} strokeWidth="3" />
      <circle cx={P.X(100)} cy={P.Y(v100)} r="4.5" fill={C.red} />
      <Label x={P.X(100) + 7} y={P.Y((v100 + intr) / 2) + 4} size={9.5} color={C.red} bg>시간가치</Label>
      <Label x={P.X(call ? 140 : 60)} y={P.Y(pay(call ? 140 : 60)) + 15} size={9.5} color={C.ink} anchor={call ? "end" : "start"} bg>만기 수익</Label>
    </Frame>
  );
}

/* ── 이항 나무: 위험중립 확률로 만기 수익을 평균하며 뒤로 — 옵션 값 ── */
export function BinTree({ p = {} }) {
  const [n, setN] = useState(p.n ?? 3);
  const clock = useClock({ period: 10, rest: 9.5 });
  const S0 = 100, u = 1.15, d = 1 / 1.15, r = 0.01, K = 100;
  const q = (1 + r - d) / (u - d);
  const val = useMemo(() => {
    const V = []; V[n] = []; for (let j = 0; j <= n; j++) V[n][j] = Math.max(S0 * u ** j * d ** (n - j) - K, 0);
    for (let i = n - 1; i >= 0; i--) { V[i] = []; for (let j = 0; j <= i; j++) V[i][j] = (q * V[i + 1][j + 1] + (1 - q) * V[i + 1][j]) / (1 + r); }
    return V;
  }, [n]); // eslint-disable-line react-hooks/exhaustive-deps
  const tt = clock.t, fw = Math.min(n, Math.floor(tt / (2 / n))), back = tt < 2.4 ? -1 : n - Math.min(n, Math.floor((tt - 2.4) / 0.9));
  const X = (i) => 30 + (i * 290) / n, Y = (i, j) => 104 - (2 * j - i) * (78 / n);
  return (
    <Frame clock={clock} title="이항 나무로 옵션 값 매기기"
      read={<>한 걸음에 주가가 ×{u} 이나 ×{fmt(d, 3)}, 한 걸음 이자 1 % → 위험중립 확률 q = (1 + r − d)/(u − d) = <b>{fmt(q, 3)}</b> · 끝 마디의 만기 수익 max(S − 100, 0) 을 q 로 평균하고 1 + r 로 나누며 한 칸씩 뒤로 — {back >= 0 && back <= 0 ? <>지금 콜 값 <b>{fmt(val[0][0], 2)}</b></> : "뒤로 계산하는 중 …"} · 진짜 오를 확률을 몰라도 되는 까닭: 주식과 채권으로 옵션을 그대로 따라 만들 수 있기 때문(복제)</>}
      controls={<Slider label="걸음 수" min={1} max={5} step={1} value={n} onChange={(v) => { setN(v); clock.reset(); }} />}>
      {Array.from({ length: n }, (_, i) => Array.from({ length: i + 1 }, (_, j) => (
        <g key={i + "-" + j} opacity={i < fw ? 1 : 0.3}>
          <line x1={X(i)} y1={Y(i, j)} x2={X(i + 1)} y2={Y(i + 1, j + 1)} stroke={C.green} strokeWidth="1.2" />
          <line x1={X(i)} y1={Y(i, j)} x2={X(i + 1)} y2={Y(i + 1, j)} stroke={C.red} strokeWidth="1.2" />
        </g>
      )))}
      {Array.from({ length: n + 1 }, (_, i) => Array.from({ length: i + 1 }, (_, j) => {
        const S = S0 * u ** j * d ** (i - j), shown = i <= fw, vShow = back >= 0 && i >= back;
        return (
          <g key={"n" + i + "-" + j} opacity={shown ? 1 : 0.35}>
            <circle cx={X(i)} cy={Y(i, j)} r={n > 3 ? 13 : 16} fill={C.card} stroke={vShow ? C.sp : C.bd} strokeWidth={vShow ? 2 : 1} />
            <text x={X(i)} y={Y(i, j) - (vShow ? 2 : -3)} textAnchor="middle" fontSize={n > 3 ? 8 : 9} fill={C.mut}>{fmt(S, 0)}</text>
            {vShow && <text x={X(i)} y={Y(i, j) + 9} textAnchor="middle" fontSize={n > 3 ? 8.5 : 9.5} fontWeight="800" fill={C.sp}>{fmt(val[i][j], 1)}</text>}
          </g>
        );
      }))}
      <text x="8" y="212" fontSize="9.5" fill={C.mut}>마디: 회색 = 주가, 색 = 옵션 값 · 초록 = 오름, 빨강 = 내림</text>
    </Frame>
  );
}
