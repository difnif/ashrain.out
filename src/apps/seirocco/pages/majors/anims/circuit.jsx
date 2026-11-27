// 회로 · 제어 그림 — 직렬 · 병렬(키르히호프) · 최대 전력 전달 · RC 충전과 방전 · 페이저 · 보드 선도 · 다이오드 동작점(뉴턴법) · 4비트 가산기 · PID 제어 · 극점과 계단 응답 · 근궤적
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, fmt, clamp, useClock } from "./kit.jsx";
import { rk4 } from "./ode.jsx";

/** 저항 지그재그 — 두 점 사이 */
function zig(x1, y1, x2, y2, n = 5, amp = 5) {
  const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L;
  let d = `M${x1} ${y1}`;
  for (let i = 1; i < 2 * n; i++) { const s = i / (2 * n), k = i % 2 ? amp : -amp; d += `L${(x1 + dx * s + nx * k).toFixed(1)} ${(y1 + dy * s + ny * k).toFixed(1)}`; }
  return d + `L${x2} ${y2}`;
}
/** 전지(세로) — 긴 판이 +, 짧고 굵은 판이 − */
function Battery({ x, y }) {
  return (
    <g>
      <line x1={x - 12} x2={x + 12} y1={y - 4} y2={y - 4} stroke={C.ink} strokeWidth="2" />
      <line x1={x - 6} x2={x + 6} y1={y + 4} y2={y + 4} stroke={C.ink} strokeWidth="4" />
      <text x={x + 15} y={y - 2} fontSize="10" fill={C.red}>+</text>
    </g>
  );
}
/** 꺾은선을 따라 같은 간격의 점 — 전류의 흐름(빠르기 ∝ 전류) */
function along(pts, gap, off) {
  const segs = []; let tot = 0;
  for (let i = 1; i < pts.length; i++) { const L = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); segs.push([tot, L, pts[i - 1], pts[i]]); tot += L; }
  const out = [];
  for (let s = ((off % gap) + gap) % gap; s < tot; s += gap) {
    const sg = segs.find(([a, L]) => s >= a && s <= a + L) || segs[segs.length - 1];
    const u = (s - sg[0]) / (sg[1] || 1);
    out.push([sg[2][0] + (sg[3][0] - sg[2][0]) * u, sg[2][1] + (sg[3][1] - sg[2][1]) * u]);
  }
  return out;
}
const pline = (pts) => pts.map(([x, y], i) => (i ? "L" : "M") + x + " " + y).join("");

/* ── 직렬과 병렬: 전류는 갈림길에서 나뉘고(KCL), 전압은 한 바퀴 돌면 0(KVL) ── */
export function DCircuit({ p = {} }) {
  const [mode, setMode] = useState(p.mode || "series");
  const [R1, setR1] = useState(p.R1 ?? 2);
  const [R2, setR2] = useState(p.R2 ?? 4);
  const clock = useClock({ period: 60 });
  const V = 12, t = clock.t;
  const pc = (v) => `hsl(${(220 - (220 * v) / V).toFixed(0)} 62% 46%)`;
  const wire = (pts, v) => <path d={pline(pts)} fill="none" stroke={pc(v)} strokeWidth="3" strokeLinejoin="round" />;
  const dots = (pts, I, k) => along(pts, 16, t * 10 * I).map(([x, y], i) => <circle key={k + i} cx={x} cy={y} r="2.3" fill={C.ink} />);
  const ser = mode === "series";
  const Rs = R1 + R2, I = V / Rs, V1 = I * R1, V2 = I * R2;
  const I1 = V / R1, I2 = V / R2, Ip = I1 + I2, Rp = (R1 * R2) / (R1 + R2);
  return (
    <Frame clock={clock} title={ser ? "직렬 회로" : "병렬 회로"}
      read={ser
        ? <>직렬: R = R₁ + R₂ = {fmt(Rs, 1)} Ω → I = V/R = <b>{fmt(I, 2)} A</b>(어디서나 같다) · V₁ = IR₁ = <b>{fmt(V1, 2)} V</b>, V₂ = IR₂ = <b>{fmt(V2, 2)} V</b> — 합이 전지의 12 V(KVL) · 전선 색 = 전위(빨강 12 V → 파랑 0 V), 점의 빠르기 = 전류</>
        : <>병렬: 두 가지에 똑같이 12 V → I₁ = 12/R₁ = <b>{fmt(I1, 2)} A</b>, I₂ = 12/R₂ = <b>{fmt(I2, 2)} A</b>, 전지로 드나드는 I = <b>{fmt(Ip, 2)} A</b>(KCL: 갈림길에서 나뉜 전류의 합) · 합성저항 R₁R₂/(R₁ + R₂) = {fmt(Rp, 2)} Ω — 어느 하나보다도 작다</>}
      controls={<>
        <Seg value={mode} onChange={setMode} options={[["series", "직렬"], ["parallel", "병렬"]]} />
        <Slider label="R₁" min={1} max={10} step={0.5} value={R1} onChange={setR1} show={(v) => fmt(v, 1) + " Ω"} />
        <Slider label="R₂" min={1} max={10} step={0.5} value={R2} onChange={setR2} show={(v) => fmt(v, 1) + " Ω"} />
      </>}>
      <Battery x={40} y={105} />
      <text x="26" y="109" fontSize="10" textAnchor="end" fill={C.ink}>12 V</text>
      {ser ? <>
        {wire([[40, 101], [40, 40], [96, 40]], 12)}
        <path d={zig(96, 40, 156, 40)} fill="none" stroke={C.ink} strokeWidth="1.8" />
        {wire([[156, 40], [214, 40]], 12 - V1)}
        <path d={zig(214, 40, 274, 40)} fill="none" stroke={C.ink} strokeWidth="1.8" />
        {wire([[274, 40], [320, 40], [320, 170], [40, 170], [40, 109]], 0)}
        {dots([[40, 101], [40, 40], [320, 40], [320, 170], [40, 170], [40, 109]], I, "s")}
        <text x="126" y="27" textAnchor="middle" fontSize="10" fill={C.ink}>R₁ = {fmt(R1, 1)} Ω</text>
        <text x="244" y="27" textAnchor="middle" fontSize="10" fill={C.ink}>R₂ = {fmt(R2, 1)} Ω</text>
        <text x="126" y="60" textAnchor="middle" fontSize="10" fill={C.red}>−{fmt(V1, 1)} V</text>
        <text x="244" y="60" textAnchor="middle" fontSize="10" fill={C.red}>−{fmt(V2, 1)} V</text>
        <Label x={62} y={84} size={10} color={pc(12)} bg>12 V</Label>
        <Label x={185} y={60} anchor="middle" size={10} color={pc(12 - V1)} bg>{fmt(12 - V1, 1)} V</Label>
        <Label x={180} y={190} anchor="middle" size={10} color={pc(0)} bg>0 V</Label>
        <text x="180" y="110" textAnchor="middle" fontSize="12" fill={C.ink}>I = {fmt(I, 2)} A</text>
      </> : <>
        {wire([[40, 101], [40, 40], [300, 40], [300, 78]], 12)}
        {wire([[200, 40], [200, 78]], 12)}
        <path d={zig(200, 78, 200, 132)} fill="none" stroke={C.ink} strokeWidth="1.8" />
        <path d={zig(300, 78, 300, 132)} fill="none" stroke={C.ink} strokeWidth="1.8" />
        {wire([[200, 132], [200, 170]], 0)}
        {wire([[300, 132], [300, 170], [40, 170], [40, 109]], 0)}
        {dots([[40, 101], [40, 40], [200, 40]], Ip, "m")}
        {dots([[200, 40], [200, 170]], I1, "a")}
        {dots([[200, 40], [300, 40], [300, 170], [200, 170]], I2, "b")}
        {dots([[200, 170], [40, 170], [40, 109]], Ip, "r")}
        <circle cx="200" cy="40" r="3.5" fill={C.ink} /><circle cx="200" cy="170" r="3.5" fill={C.ink} />
        <text x="210" y="102" fontSize="10" fill={C.ink}>R₁ {fmt(R1, 1)} Ω</text>
        <text x="210" y="116" fontSize="10" fill={C.blue}>I₁ = {fmt(I1, 2)} A</text>
        <text x="308" y="102" fontSize="10" fill={C.ink}>R₂ {fmt(R2, 1)} Ω</text>
        <text x="308" y="116" fontSize="10" fill={C.blue}>I₂ = {fmt(I2, 2)} A</text>
        <Label x={120} y={32} anchor="middle" size={10} color={pc(12)} bg>12 V</Label>
        <Label x={120} y={190} anchor="middle" size={10} color={pc(0)} bg>0 V</Label>
        <text x="58" y="140" fontSize="11" fill={C.ink}>I = {fmt(Ip, 2)} A</text>
      </>}
    </Frame>
  );
}

/* ── 최대 전력 전달: 부하 = 내부저항일 때 가장 많이 받는다(효율은 50 %) ── */
export function MaxPower({ p = {} }) {
  const [Rth, setRth] = useState(p.Rth ?? 5);
  const clock = useClock({ period: 12 });
  const Vth = 10;
  const RL = 0.3 + 24.7 * Math.pow(0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 12), 1.6);
  const Pw = (r) => (Vth * Vth * r) / (Rth + r) ** 2, eta = (r) => r / (Rth + r), Pmax = (Vth * Vth) / (4 * Rth);
  const P = plot({ x0: 0, x1: 25, y0: 0, y1: Pmax * 1.25, pad: [14, 12, 24, 162] });
  return (
    <Frame clock={clock} title="최대 전력 전달"
      read={<>부하 Rʟ = <b>{fmt(RL, 1)} Ω</b>: 받는 전력 P = V²Rʟ/(Rₜₕ + Rʟ)² = <b>{fmt(Pw(RL), 2)} W</b>, 효율 {fmt(eta(RL) * 100, 0)} % · 최대는 Rʟ = Rₜₕ = {fmt(Rth, 1)} Ω 일 때 V²/(4Rₜₕ) = <b>{fmt(Pmax, 2)} W</b> — 그때 효율은 꼭 50 % (점선 = 효율, 맨 위가 100 %)</>}
      controls={<Slider label="내부저항 Rₜₕ" min={1} max={10} step={0.5} value={Rth} onChange={setRth} show={(v) => fmt(v, 1) + " Ω"} />}>
      <circle cx="26" cy="112" r="13" fill="none" stroke={C.ink} strokeWidth="1.6" />
      <text x="26" y="108" textAnchor="middle" fontSize="10" fill={C.red}>+</text>
      <text x="26" y="122" textAnchor="middle" fontSize="11" fill={C.ink}>−</text>
      <text x="44" y="116" fontSize="10" fill={C.ink}>10 V</text>
      <path d={pline([[26, 99], [26, 44], [50, 44]])} fill="none" stroke={C.ink} strokeWidth="1.6" />
      <path d={zig(50, 44, 96, 44)} fill="none" stroke={C.ink} strokeWidth="1.6" />
      <text x="73" y="32" textAnchor="middle" fontSize="10" fill={C.ink}>Rₜₕ</text>
      <path d={pline([[96, 44], [122, 44], [122, 80]])} fill="none" stroke={C.ink} strokeWidth="1.6" />
      <path d={zig(122, 80, 122, 140)} fill="none" stroke={C.red} strokeWidth="1.8" />
      <Arrow x1={108} y1={136} x2={138} y2={86} color={C.red} w={1.2} head={5} />
      <text x="128" y="160" fontSize="10" fill={C.red}>Rʟ</text>
      <path d={pline([[122, 140], [122, 176], [26, 176], [26, 125]])} fill="none" stroke={C.ink} strokeWidth="1.6" />
      <Axes p={P} xl="Rʟ (Ω)" yl="P (W)" />
      <path d={P.path((r) => eta(r) * P.y1, 0, 25)} fill="none" stroke={C.gold} strokeWidth="1.4" strokeDasharray="4 3" />
      <line x1={P.X(Rth)} x2={P.X(Rth)} y1={P.Y(0)} y2={P.Y(Pmax)} stroke={C.green} strokeDasharray="3 3" />
      <path d={P.path(Pw, 0, 25)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <circle cx={P.X(RL)} cy={P.Y(Pw(RL))} r="5" fill={C.red} />
      <circle cx={P.X(RL)} cy={P.Y(eta(RL) * P.y1)} r="3.5" fill={C.gold} />
      <Label x={P.X(Rth) + 4} y={P.Y(Pmax) - 6} size={10} color={C.green} bg>Rʟ = Rₜₕ</Label>
    </Frame>
  );
}

/* ── RC 회로: 시간상수 τ = RC — 지수로 차고 지수로 빠진다 ── */
export function RC({ p = {} }) {
  const [tau, setTau] = useState(p.tau ?? 0.5);
  const [mode, setMode] = useState(p.mode || "step");
  const clock = useClock({ period: 7.5 });
  const V0 = 5, T = 6, n = 600, dt = T / n;
  const vin = (t) => (mode === "step" ? (t < 3 ? V0 : 0) : Math.floor(t + 1e-9) % 2 === 0 ? V0 : 0);
  const sim = useMemo(() => {
    const out = [[0, 0]]; let v = 0;
    for (let i = 0; i < n; i++) { const u = vin(i * dt + dt / 2); v = u + (v - u) * Math.exp(-dt / tau); out.push([(i + 1) * dt, v]); }
    return out;
  }, [tau, mode]); // eslint-disable-line react-hooks/exhaustive-deps
  const tc = Math.min(T, clock.t), ic = Math.min(n, Math.round(tc / dt));
  const vc = sim[ic][1], iR = vin(Math.min(tc, T - 1e-6)) - vc;
  const P = plot({ x0: 0, x1: T, y0: -5.4, y1: 5.8, pad: [12, 10, 22, 138] });
  const inp = []; for (let i = 0; i <= n; i++) inp.push([i * dt, vin(Math.min(i * dt, T - 1e-6))]);
  const nq = Math.round((5 * vc) / V0);
  return (
    <Frame clock={clock} title="RC 회로의 충전과 방전"
      read={mode === "step"
        ? <>τ = RC = <b>{fmt(tau, 2)} s</b> · 켜면 v = V(1 − e<sup>−t/τ</sup>): τ 에서 63 %, 5τ 면 99 % · 3 초에 끄면 v₀e<sup>−t/τ</sup> 로 빠진다 · 지금 t = {fmt(tc, 2)} s: vᴄ = <b>{fmt(vc, 2)} V</b>, 초록 점선 = 전류 × R = {fmt(iR, 2)} V — 처음이 가장 세다</>
        : <>사각파 입력(1 초마다 뒤집힘) · τ = <b>{fmt(tau, 2)} s</b> — τ 가 반주기보다 짧으면 입력을 따라가고, 길면 다 차기 전에 뒤집혀 평균 2.5 V 둘레의 작은 세모꼴이 된다: 빠른 변화를 깎는 <b>저역통과 필터</b></>}
      controls={<>
        <Seg value={mode} onChange={(v) => { setMode(v); clock.reset(); }} options={[["step", "켰다 끄기"], ["square", "사각파"]]} />
        <Slider label="τ = RC" min={0.1} max={2} step={0.05} value={tau} onChange={setTau} show={(v) => fmt(v, 2) + " s"} />
      </>}>
      <circle cx="22" cy="112" r="13" fill="none" stroke={C.ink} strokeWidth="1.5" />
      <path d="M14 116 L18 116 L18 107 L26 107 L26 116 L30 116" fill="none" stroke={C.ink} strokeWidth="1.3" />
      <path d={pline([[22, 99], [22, 46], [38, 46]])} fill="none" stroke={C.ink} strokeWidth="1.5" />
      <path d={zig(38, 46, 82, 46)} fill="none" stroke={C.ink} strokeWidth="1.7" />
      <text x="60" y="66" textAnchor="middle" fontSize="10" fill={C.ink}>R</text>
      <path d={pline([[82, 46], [104, 46], [104, 101]])} fill="none" stroke={C.ink} strokeWidth="1.5" />
      <line x1="90" x2="118" y1="101" y2="101" stroke={C.ink} strokeWidth="2.6" />
      <line x1="90" x2="118" y1="111" y2="111" stroke={C.ink} strokeWidth="2.6" />
      <text x="124" y="110" fontSize="10" fill={C.ink}>C</text>
      {Array.from({ length: Math.max(0, nq) }, (_, i) => <text key={"p" + i} x={92 + i * 6} y="97" fontSize="9" fill={C.red}>+</text>)}
      {Array.from({ length: Math.max(0, nq) }, (_, i) => <text key={"m" + i} x={92 + i * 6} y="121" fontSize="9" fill={C.blue}>−</text>)}
      <path d={pline([[104, 111], [104, 176], [22, 176], [22, 125]])} fill="none" stroke={C.ink} strokeWidth="1.5" />
      {Math.abs(iR) > 0.05 && <Arrow x1={60 - Math.sign(iR) * 3} y1={30} x2={60 + Math.sign(iR) * (6 + 5 * Math.abs(iR))} y2={30} color={C.green} w={1.8} />}
      <Axes p={P} xl="t (s)" yl="V" />
      <path d={P.poly(inp)} fill="none" stroke={C.mut} strokeWidth="1.4" />
      {mode === "step" && tau <= 2.9 && <><line x1={P.X(tau)} x2={P.X(tau)} y1={P.Y(0)} y2={P.Y(V0 * (1 - Math.exp(-1)))} stroke={C.gold} strokeDasharray="3 3" /><Label x={P.X(tau) + 3} y={P.Y(1.6)} size={9.5} color={C.gold} bg>τ → 63 %</Label></>}
      {mode === "step" && 5 * tau <= 2.95 && <><line x1={P.X(5 * tau)} x2={P.X(5 * tau)} y1={P.Y(0)} y2={P.Y(V0 * (1 - Math.exp(-5)))} stroke={C.gold} strokeDasharray="3 3" /><Label x={P.X(5 * tau) + 3} y={P.Y(0.6)} size={9.5} color={C.gold} bg>5τ → 99 %</Label></>}
      <path d={P.poly(sim)} fill="none" stroke={C.sp} strokeWidth="1.3" opacity="0.25" />
      <path d={P.poly(sim.slice(0, ic + 1).map(([t, v]) => [t, vin(Math.min(t, T - 1e-6)) - v]))} fill="none" stroke={C.green} strokeWidth="1.3" strokeDasharray="3 2" />
      <path d={P.poly(sim.slice(0, ic + 1))} fill="none" stroke={C.sp} strokeWidth="2.5" />
      <circle cx={P.X(tc)} cy={P.Y(vc)} r="4.5" fill={C.red} />
    </Frame>
  );
}

/* ── 페이저: 사인파 = 도는 화살표의 그림자 — R · L · C 의 위상차 ── */
export function Phasor({ p = {} }) {
  const [el, setEl] = useState(p.el || "L");
  const [u, setU] = useState(p.u ?? 1.6);
  const clock = useClock({ period: 8 });
  const th = (2 * Math.PI * clock.t) / 4, Q = 2;
  const X = el === "RLC" ? Q * (u - 1 / u) : 0;
  const phi = el === "R" ? 0 : el === "L" ? Math.PI / 2 : el === "C" ? -Math.PI / 2 : Math.atan(X);
  const Im = el === "RLC" ? 1 / Math.sqrt(1 + X * X) : 0.72;
  const cx = 72, cyy = 108, R = 52;
  const P = plot({ x0: 0, x1: 4 * Math.PI, y0: -1.25, y1: 1.25, pad: [43, 10, 47, 150] });
  const tv = [cx + R * Math.cos(th + phi), cyy - R * Math.sin(th + phi)], ti = [cx + R * Im * Math.cos(th), cyy - R * Im * Math.sin(th)];
  const tc = th % (4 * Math.PI), dg = (phi * 180) / Math.PI;
  const say = {
    R: <>저항: v = Ri — 전압(파랑)과 전류(빨강)가 함께 오르내린다(위상차 0°) · 도는 화살표(페이저)의 세로 그림자가 오른쪽 파형이다</>,
    L: <>인덕터: v = L di/dt — 전류가 가장 빨리 변하는 순간(0 을 지날 때) 전압이 가장 크다 → <b>전압이 90° 앞선다</b> · 임피던스 jωL</>,
    C: <>커패시터: i = C dv/dt — 전압이 가장 빨리 변할 때 전류가 가장 크다 → <b>전류가 90° 앞선다</b> · 임피던스 1/(jωC)</>,
    RLC: <>RLC 직렬(Q = 2), ω/ω₀ = {fmt(u, 2)}: tan φ = (Xʟ − Xᴄ)/R → φ = <b>{fmt(dg, 1)}°</b> ({Math.abs(dg) < 0.5 ? "공진 — 위상차 없음" : dg > 0 ? "유도성: 전압이 앞섬" : "용량성: 전류가 앞섬"}) · 전류 크기는 공진 때의 {fmt(Im, 2)} 배 — ω = ω₀ 에서 |Z| = R 로 가장 작다</>,
  }[el];
  return (
    <Frame clock={clock} title="페이저 — 도는 화살표"
      read={say}
      controls={<>
        <Seg value={el} onChange={setEl} options={[["R", "R"], ["L", "L"], ["C", "C"], ["RLC", "RLC"]]} />
        {el === "RLC" && <Slider label="ω/ω₀" min={0.3} max={3} step={0.05} value={u} onChange={setU} />}
      </>}>
      <circle cx={cx} cy={cyy} r={R} fill="none" stroke={C.bd} />
      <line x1={cx - R - 6} x2={cx + R + 6} y1={cyy} y2={cyy} stroke={C.mut} />
      <line x1={cx} x2={cx} y1={cyy - R - 6} y2={cyy + R + 6} stroke={C.mut} />
      <Arrow x1={cx} y1={cyy} x2={tv[0]} y2={tv[1]} color={C.blue} w={2.4} />
      <Arrow x1={cx} y1={cyy} x2={ti[0]} y2={ti[1]} color={C.red} w={2.4} />
      <text x={tv[0] + 5 * Math.cos(th + phi)} y={tv[1] - 6 * Math.sin(th + phi) + 4} fontSize="11" fontWeight="800" fill={C.blue}>V</text>
      <text x={ti[0] + 5 * Math.cos(th)} y={ti[1] - 6 * Math.sin(th) + 4} fontSize="11" fontWeight="800" fill={C.red}>I</text>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.mut} />
      <path d={P.path((x) => Math.sin(x + phi), 0, 4 * Math.PI, 200)} fill="none" stroke={C.blue} strokeWidth="2" />
      <path d={P.path((x) => Im * Math.sin(x), 0, 4 * Math.PI, 200)} fill="none" stroke={C.red} strokeWidth="2" />
      <line x1={P.X(tc)} x2={P.X(tc)} y1={P.t} y2={P.b} stroke={C.mut} strokeDasharray="2 3" />
      <line x1={tv[0]} x2={P.X(tc)} y1={tv[1]} y2={tv[1]} stroke={C.blue} strokeDasharray="3 3" opacity="0.6" />
      <line x1={ti[0]} x2={P.X(tc)} y1={ti[1]} y2={ti[1]} stroke={C.red} strokeDasharray="3 3" opacity="0.6" />
      <circle cx={P.X(tc)} cy={tv[1]} r="3.5" fill={C.blue} />
      <circle cx={P.X(tc)} cy={ti[1]} r="3.5" fill={C.red} />
      <text x={P.r} y={P.b + 14} textAnchor="end" fontSize="10" fill={C.mut} fontStyle="italic">ωt</text>
    </Frame>
  );
}

/* ── 보드 선도: 주파수마다 이득(dB)과 위상 — 로그 눈금 ── */
const H2 = (u, z) => { const re = 1 - u * u, im = 2 * z * u, m = re * re + im * im; return [re / m, -im / m]; };
const BS = {
  lp1: { name: "1차 저역통과 1/(1 + jω/ωc)", H: (u) => [1 / (1 + u * u), -u / (1 + u * u)], asym: (l) => (l < 0 ? 0 : -20 * l) },
  hp1: { name: "1차 고역통과 (jω/ωc)/(1 + jω/ωc)", H: (u) => [(u * u) / (1 + u * u), u / (1 + u * u)], asym: (l) => (l < 0 ? 20 * l : 0) },
  lp2: { name: "2차 저역통과 1/(1 − u² + 2jζu)", H: null, asym: (l) => (l < 0 ? 0 : -40 * l) },
};
function LogAx({ P, yt, yfmt, xl = true, label }) {
  return (
    <g fontSize="9.5" fill={C.mut}>
      {[-2, -1, 0, 1, 2].map((v) => <line key={"x" + v} x1={P.X(v)} x2={P.X(v)} y1={P.t} y2={P.b} stroke={C.bd} strokeWidth="0.7" />)}
      {yt.map((v) => <line key={"y" + v} x1={P.l} x2={P.r} y1={P.Y(v)} y2={P.Y(v)} stroke={v === 0 ? C.mut : C.bd} strokeWidth={v === 0 ? 1 : 0.7} />)}
      {yt.map((v) => <text key={"t" + v} x={P.l - 3} y={P.Y(v) + 3} textAnchor="end">{yfmt(v)}</text>)}
      {xl && [-2, -1, 0, 1, 2].map((v) => <text key={"l" + v} x={P.X(v)} y={P.b + 11} textAnchor="middle">{["0.01", "0.1", "1", "10", "100"][v + 2]}</text>)}
      <text x={P.l + 3} y={P.t + 10} fill={C.ink} fontSize="10">{label}</text>
    </g>
  );
}
export function Bode({ p = {} }) {
  const [sys, setSys] = useState(p.sys || "lp1");
  const [z, setZ] = useState(p.zeta ?? 0.2);
  const clock = useClock({ period: 12 });
  const S = BS[sys] || BS.lp1;
  const H = (u) => (sys === "lp2" ? H2(u, z) : S.H(u));
  const mag = (u) => Math.hypot(...H(u)), ph = (u) => (Math.atan2(H(u)[1], H(u)[0]) * 180) / Math.PI;
  const db = (u) => 20 * Math.log10(mag(u));
  const P1 = plot({ x0: -2, x1: 2, y0: -60, y1: 25, pad: [10, 132, 116, 34] });
  const P2 = plot({ x0: -2, x1: 2, y0: -190, y1: 100, pad: [120, 132, 18, 34] });
  const lu = -2 + 4 * clamp(clock.t / 10, 0, 1), um = Math.pow(10, lu), M = mag(um), F = ph(um);
  const yr = Math.max(1.3, 1.15 * M);
  const P3 = plot({ x0: 0, x1: 2, y0: -yr, y1: yr, pad: [46, 6, 62, 246] });
  const lg = (f) => (l) => f(Math.pow(10, l));
  return (
    <Frame clock={clock} title="보드 선도"
      read={<>{S.name} · ω = <b>{fmt(um, um < 0.1 ? 3 : 2)}</b> ωc: 이득 {fmt(M, 3)} = <b>{fmt(20 * Math.log10(M), 1)} dB</b>, 위상 <b>{fmt(F, 0)}°</b> · 오른쪽 = 그 주파수의 입력(회색)과 출력(색) — 높이 비가 이득, 어긋남이 위상 · 점선 = 꺾인 직선 근사(10 배마다 {sys === "lp2" ? "−40" : sys === "hp1" ? "+20 → 0" : "−20"} dB){sys === "lp2" && z < 0.5 ? <> · ζ 가 작으면 ωₙ 근처에서 봉우리(공진) {fmt(-20 * Math.log10(2 * z * Math.sqrt(1 - z * z)), 1)} dB</> : ""}</>}
      controls={<>
        <Seg value={sys} onChange={(v) => { setSys(v); clock.reset(); }} options={[["lp1", "1차 저역"], ["hp1", "1차 고역"], ["lp2", "2차 저역"]]} />
        {sys === "lp2" && <Slider label="ζ" min={0.05} max={1.5} step={0.05} value={z} onChange={setZ} />}
      </>}>
      <LogAx P={P1} yt={[20, 0, -20, -40, -60]} yfmt={(v) => v} xl={false} label="이득 (dB)" />
      <path d={P1.path(S.asym, -2, 2, 80)} fill="none" stroke={C.mut} strokeDasharray="4 3" />
      <path d={P1.path(lg(db), -2, 2, 240)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <LogAx P={P2} yt={[90, 0, -90, -180]} yfmt={(v) => v + "°"} label="위상" />
      <path d={P2.path(lg(ph), -2, 2, 240)} fill="none" stroke={C.violet} strokeWidth="2.2" />
      <line x1={P1.X(lu)} x2={P1.X(lu)} y1={P1.t} y2={P2.b} stroke={C.red} strokeDasharray="3 3" />
      <circle cx={P1.X(lu)} cy={P1.Y(clamp(db(um), -60, 25))} r="4" fill={C.red} />
      <circle cx={P2.X(lu)} cy={P2.Y(F)} r="4" fill={C.red} />
      <text x={P2.r + 12} y={P2.b + 11} fontSize="9.5" fill={C.mut} fontStyle="italic">ω/ωc</text>
      <text x={P3.l} y={P3.t - 8} fontSize="10" fill={C.ink}>입력 · 출력</text>
      <line x1={P3.l} x2={P3.r} y1={P3.Y(0)} y2={P3.Y(0)} stroke={C.bd} />
      <path d={P3.path((x) => Math.sin(2 * Math.PI * x), 0, 2, 120)} fill="none" stroke={C.mut} strokeWidth="1.4" />
      <path d={P3.path((x) => M * Math.sin(2 * Math.PI * x + (F * Math.PI) / 180), 0, 2, 120)} fill="none" stroke={C.sp} strokeWidth="2.2" />
    </Frame>
  );
}

/* ── 다이오드 동작점: 지수 곡선과 부하선의 만남 — 손으로는 못 풀어 뉴턴법으로 ── */
export function Diode({ p = {} }) {
  const [vs, setVs] = useState(p.vs ?? 3);
  const [R, setR] = useState(p.R ?? 500);
  const clock = useClock({ period: 10 });
  const Is = 1e-14, Vt = 0.02585, Id = (v) => Is * (Math.exp(v / Vt) - 1);
  const it = useMemo(() => {
    const f = (v) => Id(v) - (vs - v) / R, fp = (v) => (Is / Vt) * Math.exp(v / Vt) + 1 / R;
    const out = [0.4]; let v = 0.4;
    for (let k = 0; k < 14; k++) { v += clamp(-f(v) / fp(v), -0.1, 0.1); out.push(v); }
    return out;
  }, [vs, R]); // eslint-disable-line react-hooks/exhaustive-deps
  const vq = it[it.length - 1], iq = ((vs - vq) / R) * 1000;
  const k = Math.min(it.length - 1, Math.floor(clock.t / 1.1)), vk = it[k];
  const x1 = Math.max(1, vs), y1 = (vs / R) * 1000 * 1.15;
  const P = plot({ x0: 0, x1, y0: 0, y1, pad: [14, 12, 24, 40] });
  const ll = (v) => ((vs - v) / R) * 1000;
  const conv = k >= 6;
  return (
    <Frame clock={clock} title="다이오드의 동작점"
      read={<>다이오드 I = Iₛ(e<sup>V/Vₜ</sup> − 1) 와 부하선 I = (Vₛ − V)/R 이 만나는 곳 = 동작점: 다이오드 전압 ≈ <b>{fmt(vq, 3)} V</b>, I ≈ <b>{fmt(iq, 2)} mA</b> · 지수와 직선이 섞인 방정식이라 식으로 풀 수 없다 — 뉴턴법 {k}번째 어림 V = <b>{fmt(vk, 4)} V</b>{conv ? " (수렴)" : ""} · 전압이 0.1 V 늘 때마다 전류는 약 47 배</>}
      controls={<>
        <Slider label="Vₛ" min={1} max={5} step={0.25} value={vs} onChange={(v) => { setVs(v); clock.reset(); }} show={(v) => fmt(v, 2) + " V"} />
        <Slider label="R" min={100} max={2000} step={50} value={R} onChange={(v) => { setR(v); clock.reset(); }} show={(v) => v + " Ω"} />
      </>}>
      <Axes p={P} xl="V (V)" yl="I (mA)" />
      <path d={P.path((v) => Id(v) * 1000, 0, x1, 400)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <path d={P.path(ll, 0, vs, 20)} fill="none" stroke={C.gold} strokeWidth="2" />
      <line x1={P.X(vk)} x2={P.X(vk)} y1={P.t} y2={P.b} stroke={C.red} strokeDasharray="3 3" />
      <circle cx={P.X(vk)} cy={P.Y(ll(vk))} r="3.5" fill={C.gold} />
      {Id(vk) * 1000 < y1 && <circle cx={P.X(vk)} cy={P.Y(Id(vk) * 1000)} r="3.5" fill={C.sp} />}
      {conv && <circle cx={P.X(vq)} cy={P.Y(iq)} r="6" fill="none" stroke={C.red} strokeWidth="2" />}
      <Label x={P.X(vq + 0.55 * (vs - vq)) + 4} y={P.Y(ll(vq + 0.55 * (vs - vq))) - 8} size={10} color={C.gold} bg>부하선</Label>
      <Label x={P.X(Math.min(x1, vq + 0.04))} y={P.t + 12} size={10} color={C.sp} bg>다이오드</Label>
    </Frame>
  );
}

/* ── 4비트 가산기: 전가산기 넷을 잇고, 올림이 낮은 자리부터 퍼진다 ── */
export function Adder({ p = {} }) {
  const [A, setA] = useState(p.A ?? 11);
  const [B, setB] = useState(p.B ?? 6);
  const [mode, setMode] = useState(p.signed ? "s" : "u");
  const clock = useClock({ period: 6 });
  const bit = (x, i) => (x >> i) & 1, sgn = (x) => (x >= 8 ? x - 16 : x), bin = (x) => x.toString(2).padStart(4, "0");
  const st = []; let c = 0;
  for (let i = 0; i < 4; i++) { const a = bit(A, i), b = bit(B, i), s = a ^ b ^ c, co = (a & b) | (c & (a ^ b)); st.push({ a, b, cin: c, s, co }); c = co; }
  const done = Math.min(4, Math.floor(clock.t / 0.9));
  const xs = [286, 214, 142, 70];
  const S = (A + B) & 15, C4 = (A + B) >> 4, ov = st[3].cin !== st[3].co, sig = mode === "s";
  const dec = (x) => (sig ? sgn(x) : x);
  return (
    <Frame clock={clock} title="4비트 덧셈 회로"
      read={sig
        ? <>2의 보수로 읽으면 {sgn(A)} + {sgn(B)} = <b>{done >= 4 ? sgn(S) : "…"}</b>{done >= 4 && ov ? <> — <b>넘침!</b> 참값 {sgn(A) + sgn(B)} 이 −8 ~ 7 을 벗어나 부호가 뒤집혔다(맨 앞 칸에 들어온 올림 ≠ 나간 올림)</> : " — 같은 덧셈 회로가 음수 덧셈까지 해 준다"} · 맨 앞 자리의 무게는 −8</>
        : <>{A} + {B} = <b>{done >= 4 ? A + B : "…"}</b>{done >= 4 && C4 ? <> — 4 비트를 넘쳐 올림 C₄ = 1 (남은 4 비트는 {S})</> : ""} · 전가산기: 합 S = a ⊕ b ⊕ c, 올림 = ab + c(a ⊕ b) — 올림이 오른쪽에서 왼쪽으로 한 칸씩 퍼져서(초록) 자리가 많으면 기다림이 길다</>}
      controls={<>
        <Slider label="A" min={0} max={15} value={A} onChange={(v) => { setA(v); clock.reset(); }} show={(v) => bin(v) + " (" + dec(v) + ")"} />
        <Slider label="B" min={0} max={15} value={B} onChange={(v) => { setB(v); clock.reset(); }} show={(v) => bin(v) + " (" + dec(v) + ")"} />
        <Seg value={mode} onChange={setMode} options={[["u", "부호 없음"], ["s", "2의 보수"]]} />
      </>}>
      {xs.map((x, i) => (
        <g key={i}>
          <text x={x} y="12" textAnchor="middle" fontSize="9" fill={C.mut}>{sig && i === 3 ? "−8" : 1 << i}</text>
          <text x={x - 9} y="30" textAnchor="middle" fontSize="13" fontWeight="800" fill={C.blue}>{st[i].a}</text>
          <text x={x + 9} y="30" textAnchor="middle" fontSize="13" fontWeight="800" fill={C.gold}>{st[i].b}</text>
          <rect x={x - 24} y="40" width="48" height="36" rx="5" fill={C.card} stroke={i < done ? C.green : i === done ? C.gold : C.bd} strokeWidth={i <= done ? 2 : 1} />
          <text x={x} y="62" textAnchor="middle" fontSize="9.5" fill={C.mut}>전가산기</text>
          <Arrow x1={x} y1={78} x2={x} y2={92} color={i < done ? C.ink : C.bd} w={1.3} head={4} />
          <text x={x} y="110" textAnchor="middle" fontSize="15" fontWeight="800" fill={i < done ? C.sp : C.bd}>{i < done ? st[i].s : "?"}</text>
          <Arrow x1={x - 24} y1={66} x2={i < 3 ? xs[i + 1] + 24 : 30} y2={66} color={i < done ? C.green : C.bd} w={1.4} head={4} />
          {i < done && <text x={(x - 24 + (i < 3 ? xs[i + 1] + 24 : 30)) / 2} y="60" textAnchor="middle" fontSize="10" fontWeight="800" fill={C.green}>{st[i].co}</text>}
        </g>
      ))}
      <Arrow x1={344} y1={66} x2={312} y2={66} color={C.green} w={1.4} head={4} />
      <text x="330" y="60" textAnchor="middle" fontSize="10" fill={C.green}>0</text>
      <text x="22" y="62" textAnchor="middle" fontSize="10" fill={C.mut}>C₄</text>
      <text x="8" y="30" fontSize="10" fill={C.mut}>a b</text>
      <text x="8" y="110" fontSize="10" fill={C.mut}>S</text>
      <text x="12" y="140" fontSize="11" fill={C.blue}>A = {bin(A)}₂ = {dec(A)}</text>
      <text x="12" y="158" fontSize="11" fill={C.gold}>B = {bin(B)}₂ = {dec(B)}</text>
      <text x="12" y="176" fontSize="11" fill={C.sp}>{done >= 4 ? `S = ${C4 && !sig ? "1 " : ""}${bin(S)}₂ = ${sig ? sgn(S) : A + B}` : "S = 계산 중 …"}</text>
      {done >= 4 && sig && ov && <text x="12" y="196" fontSize="11" fill={C.red}>넘침(overflow) — 부호 칸의 올림이 들어온 것과 나간 것이 다르다</text>}
    </Frame>
  );
}

/* ── PID 제어: 비례 · 적분 · 미분 — 플랜트 1/(s + 1)² 의 계단 응답 ── */
export function PID({ p = {} }) {
  const [kp, setKp] = useState(p.kp ?? 4);
  const [ki, setKi] = useState(p.ki ?? 0);
  const [kd, setKd] = useState(p.kd ?? 0);
  const clock = useClock({ period: 10 });
  const sol = useMemo(() => rk4((t, [y, yd, ie]) => { const e = 1 - y, u = kp * e + ki * ie - kd * yd; return [yd, u - 2 * yd - y, e]; }, [0, 0, 0], 0, 12, 1200), [kp, ki, kd]);
  const stable = ki === 0 || (2 + kd) * (1 + kp) > ki;
  const ys = ki > 0 ? 1 : kp / (1 + kp);
  const peak = Math.max(...sol.map((r) => r[1]));
  const os = stable && ys > 1e-6 && peak > ys ? ((peak - ys) / ys) * 100 : 0;
  let ts = 0;
  if (ys > 1e-6) for (const r of sol) if (Math.abs(r[1] - ys) > 0.02 * ys) ts = r[0];
  const ess = ki > 0 ? 0 : 100 / (1 + kp);
  const i = Math.min(1200, Math.floor((clock.t / 8) * 1200));
  const P = plot({ x0: 0, x1: 12, y0: -0.2, y1: 1.8, pad: [14, 12, 24, 32] });
  const cl = (y) => clamp(y, -0.2, 1.8);
  return (
    <Frame clock={clock} title="PID 제어"
      read={stable
        ? <>목표 1 로 가라는 명령(계단)에 플랜트 1/(s + 1)² 이 따라가는 모습 · 넘침 <b>{fmt(os, 1)} %</b> · 정착 시간(±2 %) <b>{ts > 11.9 ? "12 s 넘게" : fmt(ts, 1) + " s"}</b> · 정상상태 오차 <b>{fmt(ess, 1)} %</b> — P 는 빠르게(오차는 남는다), I 는 오차를 지우고(대신 출렁인다), D 는 출렁임을 누른다</>
        : <><b>불안정!</b> (2 + Kd)(1 + Kp) = {fmt((2 + kd) * (1 + kp), 1)} 이 Ki = {fmt(ki, 1)} 보다 작다 — 루스-후르비츠 조건이 깨져 출렁임이 점점 커진다. 적분을 줄이거나 미분을 늘려 보라</>}
      controls={<>
        <Slider label="Kp" min={0} max={20} step={0.5} value={kp} onChange={setKp} />
        <Slider label="Ki" min={0} max={10} step={0.5} value={ki} onChange={setKi} />
        <Slider label="Kd" min={0} max={6} step={0.25} value={kd} onChange={setKd} />
      </>}>
      <Axes p={P} xl="t (s)" yl="y" />
      {stable && ys > 1e-6 && <rect x={P.l} y={P.Y(ys * 1.02)} width={P.r - P.l} height={P.Y(ys * 0.98) - P.Y(ys * 1.02)} fill={C.green} opacity="0.15" />}
      <line x1={P.l} x2={P.r} y1={P.Y(1)} y2={P.Y(1)} stroke={C.ink} strokeDasharray="5 4" />
      {ki === 0 && <><line x1={P.l} x2={P.r} y1={P.Y(ys)} y2={P.Y(ys)} stroke={C.gold} strokeDasharray="2 3" /><Label x={P.r - 4} y={P.Y(ys) + 13} anchor="end" size={10} color={C.gold} bg>남는 오차 {fmt(ess, 1)} %</Label></>}
      <path d={P.poly(sol.map(([t, y]) => [t, cl(y)]))} fill="none" stroke={stable ? C.sp : C.red} strokeWidth="1.3" opacity="0.25" />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, y]) => [t, cl(y)]))} fill="none" stroke={stable ? C.sp : C.red} strokeWidth="2.4" />
      <circle cx={P.X(sol[i][0])} cy={P.Y(cl(sol[i][1]))} r="4" fill={C.red} />
      <Label x={P.l + 6} y={P.Y(1) - 5} size={10} color={C.ink} bg>목표</Label>
    </Frame>
  );
}

/* ── 극점과 계단 응답: s 평면의 자리가 응답의 모양을 정한다 ── */
export function Poles({ p = {} }) {
  const [z, setZ] = useState(p.zeta ?? 0.3);
  const [wn, setW] = useState(p.wn ?? 2);
  const clock = useClock({ period: 9 });
  const S = plot({ x0: -4.4, x1: 1.2, y0: -3.8, y1: 3.8, pad: [10, 196, 18, 12] });
  const P = plot({ x0: 0, x1: 10, y0: -0.6, y1: 2.2, pad: [14, 10, 22, 196] });
  const sol = useMemo(() => rk4((t, [y, v]) => [v, wn * wn * (1 - y) - 2 * z * wn * v], [0, 0], 0, 10, 800), [z, wn]);
  const under = Math.abs(z) < 1;
  const re = -z * wn, im = under ? wn * Math.sqrt(1 - z * z) : 0;
  const d = under ? 0 : wn * Math.sqrt(z * z - 1);
  const poles = under ? [[re, im], [re, -im]] : [[re + d, 0], [re - d, 0]];
  const os = z > 0 && z < 1 ? Math.exp((-Math.PI * z) / Math.sqrt(1 - z * z)) * 100 : 0;
  const i = Math.min(800, Math.floor((clock.t / 7) * 800));
  const cl = (y) => clamp(y, -0.6, 2.2);
  const X0 = S.X(0), Y0 = S.Y(0);
  return (
    <Frame clock={clock} title="극점과 계단 응답"
      read={z < 0
        ? <>ζ = {fmt(z, 2)} &lt; 0 → 극점이 <b>오른쪽 반평면</b>: 응답이 점점 커진다(불안정)</>
        : under
          ? <>극점 s = {fmt(re, 2)} ± {fmt(im, 2)}j · 실수부 −ζωₙ 이 왼쪽으로 멀수록 빨리 가라앉고(포락선 e<sup>−ζωₙ t</sup>), 허수부 ωd = ωₙ√(1 − ζ²) 이 클수록 빨리 흔들린다 · 넘침 <b>{fmt(os, 1)} %</b>{z === 0 ? " — ζ = 0: 허수축 위, 끝없이 흔들림" : ""}</>
          : <>극점 둘 다 실수 {fmt(poles[0][0], 2)}, {fmt(poles[1][0], 2)} — 흔들림 없이 다가간다({Math.abs(z - 1) < 1e-9 ? "임계 감쇠: 넘치지 않는 가장 빠른 응답" : "과감쇠: 원점에 가까운 극점 때문에 느리다"})</>}
      controls={<>
        <Slider label="ζ" min={-0.3} max={1.6} step={0.05} value={z} onChange={setZ} />
        <Slider label="ωₙ" min={0.5} max={3} step={0.1} value={wn} onChange={setW} />
      </>}>
      <rect x={X0} y={S.t} width={S.r - X0} height={S.b - S.t} fill={C.red} opacity="0.08" />
      <text x={S.r - 2} y={S.b - 4} textAnchor="end" fontSize="9" fill={C.red}>불안정</text>
      <line x1={S.l} x2={S.r} y1={Y0} y2={Y0} stroke={C.mut} />
      <line x1={X0} x2={X0} y1={S.t} y2={S.b} stroke={C.mut} />
      <text x={S.r - 2} y={Y0 - 4} textAnchor="end" fontSize="9" fill={C.mut} fontStyle="italic">Re</text>
      <text x={X0 + 3} y={S.t + 20} fontSize="9" fill={C.mut} fontStyle="italic">Im</text>
      {under && <circle cx={X0} cy={Y0} r={wn * (S.X(1) - S.X(0))} fill="none" stroke={C.bd} strokeDasharray="3 3" />}
      {under && poles.map(([x, y], k) => <line key={"l" + k} x1={X0} y1={Y0} x2={S.X(x)} y2={S.Y(y)} stroke={C.bd} />)}
      {poles.map(([x, y], k) => (
        <g key={k} stroke={C.sp} strokeWidth="2.6">
          <line x1={S.X(x) - 5} y1={S.Y(y) - 5} x2={S.X(x) + 5} y2={S.Y(y) + 5} />
          <line x1={S.X(x) - 5} y1={S.Y(y) + 5} x2={S.X(x) + 5} y2={S.Y(y) - 5} />
        </g>
      ))}
      <text x={S.l} y={S.b + 14} fontSize="10" fill={C.mut}>s 평면 (× = 극점)</text>
      <Axes p={P} xl="t" yl="y" />
      <line x1={P.l} x2={P.r} y1={P.Y(1)} y2={P.Y(1)} stroke={C.ink} strokeDasharray="5 4" />
      <path d={P.poly(sol.map(([t, y]) => [t, cl(y)]))} fill="none" stroke={z < 0 ? C.red : C.sp} strokeWidth="1.3" opacity="0.25" />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, y]) => [t, cl(y)]))} fill="none" stroke={z < 0 ? C.red : C.sp} strokeWidth="2.4" />
      <circle cx={P.X(sol[i][0])} cy={P.Y(cl(sol[i][1]))} r="4" fill={C.red} />
    </Frame>
  );
}

/* ── 근궤적: 이득 K 를 키우면 닫힌 고리 극점이 움직인다 — 허수축을 넘으면 불안정 ── */
function cubicRoots(a, b, c) {
  // 뒤랑-케르너 — s³ + a s² + b s + c 의 세 근(복소수)
  const mul = ([x, y], [u, v]) => [x * u - y * v, x * v + y * u];
  const sub = ([x, y], [u, v]) => [x - u, y - v];
  const div = ([x, y], [u, v]) => { const m = u * u + v * v || 1e-30; return [(x * u + y * v) / m, (y * u - x * v) / m]; };
  const f = (zz) => { const z2 = mul(zz, zz), z3 = mul(z2, zz); return [z3[0] + a * z2[0] + b * zz[0] + c, z3[1] + a * z2[1] + b * zz[1]]; };
  let r = [[0.4, 0.9], [-0.65, 0.72], [-0.8, -0.6]].map(([x, y]) => [x * 4, y * 4]);
  for (let it = 0; it < 300; it++) {
    r = r.map((zz, i) => { let den = [1, 0]; r.forEach((w, j) => { if (j !== i) den = mul(den, sub(zz, w)); }); return sub(zz, div(f(zz), den)); });
  }
  return r.map(([x, y]) => [x, Math.abs(y) < 1e-3 ? 0 : y]);
}
let LOCUS = null;
function locus() {
  if (!LOCUS) { LOCUS = []; for (let K = 0; K <= 160; K += 0.5) cubicRoots(6, 8, K).forEach((q) => LOCUS.push(q)); }
  return LOCUS;
}
export function RootLocus({ p = {} }) {
  const [K, setK] = useState(p.K ?? 20);
  const clock = useClock({ period: 9 });
  const roots = useMemo(() => cubicRoots(6, 8, K), [K]);
  const S = plot({ x0: -7.5, x1: 2, y0: -5.8, y1: 5.8, pad: [10, 192, 18, 10] });
  const P = plot({ x0: 0, x1: 15, y0: -0.6, y1: 2.2, pad: [14, 10, 22, 196] });
  const sol = useMemo(() => rk4((t, [y, v, w]) => [v, w, K * (1 - y) - 8 * v - 6 * w], [0, 0, 0], 0, 15, 1500), [K]);
  const i = Math.min(1500, Math.floor((clock.t / 7) * 1500));
  const cl = (y) => clamp(y, -0.6, 2.2);
  const st = K < 48 ? "모두 왼쪽 반평면 — 안정" : K === 48 ? "둘이 허수축 위 — 끝없이 흔들린다" : "둘이 오른쪽 반평면 — 불안정";
  const txt = roots.slice().sort((a, b) => a[0] - b[0]).filter(([, y]) => y >= 0).map(([x, y]) => (y > 0 ? `${fmt(x, 2)} ± ${fmt(y, 2)}j` : fmt(x, 2))).join(", ");
  const X0 = S.X(0), Y0 = S.Y(0);
  return (
    <Frame clock={clock} title="근궤적"
      read={<>열린 고리 K/(s(s + 2)(s + 4)) 를 되먹임 · K = <b>{K}</b>: 닫힌 고리 극점 {txt} — {st} · 루스-후르비츠: 6 × 8 &gt; K 이어야 안정 → 경계 K = 48 에서 ±2.83j 를 지난다 · 점 = K 를 0 에서 160 까지 키울 때 극점이 지나는 길</>}
      controls={<Slider label="이득 K" min={1} max={100} value={K} onChange={setK} />}>
      <rect x={X0} y={S.t} width={S.r - X0} height={S.b - S.t} fill={C.red} opacity="0.08" />
      <line x1={S.l} x2={S.r} y1={Y0} y2={Y0} stroke={C.mut} />
      <line x1={X0} x2={X0} y1={S.t} y2={S.b} stroke={C.mut} />
      {locus().map(([x, y], k) => (x >= S.x0 && x <= S.x1 && y >= S.y0 && y <= S.y1 ? <circle key={k} cx={S.X(x)} cy={S.Y(y)} r="0.9" fill={C.mut} /> : null))}
      {[0, -2, -4].map((x) => (
        <g key={x} stroke={C.ink} strokeWidth="1.6">
          <line x1={S.X(x) - 4} y1={Y0 - 4} x2={S.X(x) + 4} y2={Y0 + 4} />
          <line x1={S.X(x) - 4} y1={Y0 + 4} x2={S.X(x) + 4} y2={Y0 - 4} />
        </g>
      ))}
      <circle cx={X0} cy={S.Y(Math.sqrt(8))} r="3" fill="none" stroke={C.red} />
      <circle cx={X0} cy={S.Y(-Math.sqrt(8))} r="3" fill="none" stroke={C.red} />
      <text x={X0 + 5} y={S.Y(Math.sqrt(8)) - 4} fontSize="9" fill={C.red}>K = 48</text>
      {roots.map(([x, y], k) => <circle key={"r" + k} cx={S.X(clamp(x, S.x0, S.x1))} cy={S.Y(clamp(y, S.y0, S.y1))} r="5" fill={C.sp} />)}
      <text x={S.l} y={S.b + 14} fontSize="10" fill={C.mut}>s 평면 (× = 열린 고리 극점)</text>
      <Axes p={P} xl="t" yl="y" />
      <line x1={P.l} x2={P.r} y1={P.Y(1)} y2={P.Y(1)} stroke={C.ink} strokeDasharray="5 4" />
      <path d={P.poly(sol.map(([t, y]) => [t, cl(y)]))} fill="none" stroke={K < 48 ? C.sp : C.red} strokeWidth="1.3" opacity="0.25" />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, y]) => [t, cl(y)]))} fill="none" stroke={K < 48 ? C.sp : C.red} strokeWidth="2.4" />
      <circle cx={P.X(sol[i][0])} cy={P.Y(cl(sol[i][1]))} r="4" fill={C.red} />
    </Frame>
  );
}
