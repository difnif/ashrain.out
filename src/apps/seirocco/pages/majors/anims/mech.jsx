// 기계공학 그림 — 보의 반력 · 전단력 · 굽힘모멘트 · 처짐 · 응력-변형률 곡선 · 막대의 열전도 · P-V 순환(카르노 · 오토) · 벤투리관(연속 · 베르누이) · 경사면 굴림 경주
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, fmt, clamp, rng, useClock } from "./kit.jsx";

/* ── 단순보: 반력 → 전단력 V(x) → 굽힘모멘트 M(x) (dM/dx = V) → 처짐 ── */
export function Beam({ p = {} }) {
  const [load, setLoad] = useState(p.load || "point");
  const [a, setA] = useState(p.a ?? 2);
  const clock = useClock({ period: 9 });
  const L = 6, P0 = 900, w = 300, pt = load === "point";
  const RA = pt ? (P0 * (L - a)) / L : (w * L) / 2, RB = pt ? (P0 * a) / L : (w * L) / 2;
  const V = (x) => (pt ? (x < a ? RA : RA - P0) : RA - w * x);
  const M = (x) => (pt ? (x < a ? RA * x : RB * (L - x)) : (w * x * (L - x)) / 2);
  const Mmax = pt ? (P0 * a * (L - a)) / L : (w * L * L) / 8;
  const xc = L * (0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 9));
  const X = (x) => 40 + (x / L) * 280;
  const defl = useMemo(() => {
    // EI y″ = M 를 두 번 적분하고 y(0) = y(L) = 0 을 맞춘다 — 모양만(크게 과장)
    const n = 120, h = L / n, s1 = [0], s2 = [0];
    for (let i = 1; i <= n; i++) { const xm = (i - 0.5) * h; s1.push(s1[i - 1] + M(xm) * h); s2.push(s2[i - 1] + 0.5 * (s1[i - 1] + s1[i]) * h); }
    const y = s2.map((v, i) => v - (s2[n] * i) / n), mx = Math.max(...y.map(Math.abs)) || 1;
    return y.map((v, i) => [X(i * h), 40 - (13 * v) / mx]);
  }, [load, a]); // eslint-disable-line react-hooks/exhaustive-deps
  const vy = (v) => 116 - (v / 900) * 21, my = (m) => 204 - (m / 1350) * 46;
  const shear = pt ? [[0, 0], [0, RA], [a, RA], [a, RA - P0], [L, RA - P0], [L, 0]] : [[0, 0], [0, RA], [L, RA - w * L], [L, 0]];
  const mom = [[0, 0], ...Array.from({ length: 61 }, (_, i) => [(i / 60) * L, M((i / 60) * L)]), [L, 0]];
  const poly = (pts, f) => pts.map(([x, v], i) => (i ? "L" : "M") + X(x).toFixed(1) + " " + f(v).toFixed(1)).join("") + "Z";
  return (
    <Frame clock={clock} title="단순보의 반력 · 전단력 · 굽힘모멘트"
      read={pt
        ? <>반력 Rᴀ = Pb/L = <b>{fmt(RA, 0)} N</b>, Rʙ = Pa/L = <b>{fmt(RB, 0)} N</b> (하중에 가까운 받침이 더 받는다) · 최대 굽힘모멘트 Pab/L = <b>{fmt(Mmax, 0)} N·m</b> — 하중 바로 아래, 전단력이 부호를 바꾸는 곳 · 커서 x = {fmt(xc, 2)} m: V = {fmt(V(xc), 0)} N, M = {fmt(M(xc), 0)} N·m · 점선 = 처진 모양(크게 과장)</>
        : <>반력 각각 wL/2 = <b>900 N</b> · V = wL/2 − wx (기울기 −w), M = wx(L − x)/2 · 최대 wL²/8 = <b>1350 N·m</b> 는 가운데(V = 0 인 곳) · 커서 x = {fmt(xc, 2)} m: V = {fmt(V(xc), 0)} N, M = {fmt(M(xc), 0)} N·m · 점선 = 처진 모양(크게 과장)</>}
      controls={<>
        <Seg value={load} onChange={setLoad} options={[["point", "집중하중 900 N"], ["udl", "등분포 300 N/m"]]} />
        {pt && <Slider label="하중 위치 a" min={0.5} max={5.5} step={0.25} value={a} onChange={setA} show={(v) => fmt(v, 2) + " m"} />}
      </>}>
      {pt
        ? <><Arrow x1={X(a)} y1={6} x2={X(a)} y2={34} color={C.red} w={2.2} /><Label x={X(a) + 6} y={14} size={10} color={C.red}>P = 900 N</Label></>
        : <>
          <line x1={X(0)} x2={X(L)} y1={14} y2={14} stroke={C.red} strokeWidth="1.4" />
          {Array.from({ length: 13 }, (_, i) => <Arrow key={i} x1={X(i * 0.5)} y1={14} x2={X(i * 0.5)} y2={34} color={C.red} w={1.2} head={5} />)}
          <Label x={X(L / 2)} y={10} anchor="middle" size={10} color={C.red} bg>w = 300 N/m</Label>
        </>}
      <rect x={X(0)} y="36" width={X(L) - X(0)} height="8" rx="2" fill={C.sp} opacity="0.75" />
      <path d={defl.map(([x, y], i) => (i ? "L" : "M") + x.toFixed(1) + " " + (y + 4).toFixed(1)).join("")} fill="none" stroke={C.ink} strokeDasharray="3 3" />
      <polygon points={`${X(0)},44 ${X(0) - 8},57 ${X(0) + 8},57`} fill={C.mut} />
      <circle cx={X(L)} cy="50.5" r="6" fill="none" stroke={C.mut} strokeWidth="1.6" />
      <line x1={X(L) - 10} x2={X(L) + 10} y1="57.5" y2="57.5" stroke={C.mut} strokeWidth="1.6" />
      <Arrow x1={X(0)} y1={62 + (RA / 900) * 22} x2={X(0)} y2={60} color={C.green} w={2} />
      <Arrow x1={X(L)} y1={62 + (RB / 900) * 22} x2={X(L)} y2={60} color={C.green} w={2} />
      <text x={X(0) + 8} y="80" fontSize="9.5" fill={C.green}>Rᴀ {fmt(RA, 0)} N</text>
      <text x={X(L) - 8} y="80" fontSize="9.5" fill={C.green} textAnchor="end">Rʙ {fmt(RB, 0)} N</text>
      <text x="12" y="119" fontSize="10" fill={C.mut} fontStyle="italic">V</text>
      <line x1={X(0)} x2={X(L)} y1={vy(0)} y2={vy(0)} stroke={C.mut} />
      <path d={poly(shear, vy)} fill={C.blue} opacity="0.3" stroke={C.blue} strokeWidth="1.4" />
      <text x="12" y="180" fontSize="10" fill={C.mut} fontStyle="italic">M</text>
      <line x1={X(0)} x2={X(L)} y1={my(0)} y2={my(0)} stroke={C.mut} />
      <path d={poly(mom, my)} fill={C.gold} opacity="0.3" stroke={C.gold} strokeWidth="1.4" />
      <line x1={X(xc)} x2={X(xc)} y1="28" y2="206" stroke={C.red} strokeDasharray="3 3" opacity="0.8" />
      <circle cx={X(xc)} cy={vy(V(xc))} r="3.5" fill={C.blue} />
      <circle cx={X(xc)} cy={my(M(xc))} r="3.5" fill={C.gold} />
    </Frame>
  );
}

/* ── 응력-변형률 곡선: 탄성 → 항복 → 변형 경화 → 넥킹 → 파단 ── */
const MATS = {
  steel: { name: "연강", E: 200, sy: 250, su: 420, sf: 330, ep: 250 / 200000, esh: 0.015, eu: 0.18, ef: 0.28 },
  al: { name: "알루미늄 합금", E: 69, sy: 255, sp: 240, su: 310, sf: 285, ep: 240 / 69000, eu: 0.08, ef: 0.12 },
};
function sigma(m, e) {
  if (e <= m.ep) return m.E * 1000 * e;
  if (m.esh) {
    if (e <= m.esh) return m.sy;
    if (e <= m.eu) return m.sy + (m.su - m.sy) * (1 - ((m.eu - e) / (m.eu - m.esh)) ** 2);
  } else if (e <= m.eu) return m.sp + (m.su - m.sp) * (1 - Math.exp(-(e - m.ep) / 0.01));
  return m.su - (m.su - m.sf) * ((e - m.eu) / (m.ef - m.eu)) ** 2;
}
export function StressStrain({ p = {} }) {
  const [mk, setMk] = useState(p.mat || "steel");
  const m = MATS[mk] || MATS.steel;
  const clock = useClock({ period: 10 });
  const e = m.ef * Math.pow(clamp(clock.t / 8, 0, 1), 2.3), s = sigma(m, e);
  const P = plot({ x0: 0, x1: 30, y0: 0, y1: 460, pad: [12, 12, 24, 40] });
  const Q = plot({ x0: 0, x1: 0.6, y0: 0, y1: 300, pad: [128, 18, 30, 206] });
  const stage = e <= m.ep ? "탄성 — 힘을 빼면 원래대로 (σ = Eε)" : m.esh && e <= m.esh ? "항복 — 힘은 그대로인데 계속 늘어난다" : e <= m.eu ? "변형 경화 — 더 늘이려면 더 큰 힘" : "넥킹 — 한 곳이 가늘어지며 끊어지기 직전";
  const plastic = e > m.ep, perm = e - s / (m.E * 1000);
  const pts = (f, a, b, n = 200) => Array.from({ length: n + 1 }, (_, i) => { const x = a + ((b - a) * i) / n; return [x * 100, f(x)]; });
  const full = pts((x) => sigma(m, x), 0, m.ef, 260);
  return (
    <Frame clock={clock} title="응력-변형률 곡선"
      read={<>{m.name} · 영률 E = {m.E} GPa · 항복 {m.sy} MPa · 인장강도 {m.su} MPa · 지금 ε = <b>{fmt(e * 100, 2)} %</b>, σ = <b>{fmt(s, 0)} MPa</b> — {stage}{plastic ? <> · 하중을 빼면 E 기울기로 내려와 <b>{fmt(perm * 100, 2)} %</b> 가 영구 변형으로 남는다</> : ""}</>}
      controls={<Seg value={mk} onChange={(v) => { setMk(v); clock.reset(); }} options={[["steel", "연강"], ["al", "알루미늄 합금"]]} />}>
      <Axes p={P} xl="ε (%)" yl="σ (MPa)" />
      <path d={P.poly(full)} fill="none" stroke={C.sp} strokeWidth="1.2" opacity="0.4" />
      <path d={P.poly(full.filter(([x]) => x <= e * 100 + 1e-9).concat([[e * 100, s]]))} fill="none" stroke={C.sp} strokeWidth="2.6" />
      {plastic && <line x1={P.X(e * 100)} y1={P.Y(s)} x2={P.X(perm * 100)} y2={P.Y(0)} stroke={C.red} strokeDasharray="4 3" />}
      <circle cx={P.X(e * 100)} cy={P.Y(s)} r="4.5" fill={C.red} />
      <rect x={Q.l - 18} y={Q.t - 16} width={Q.r - Q.l + 30} height={Q.b - Q.t + 30} rx="6" fill={C.card} stroke={C.bd} />
      <text x={Q.l - 12} y={Q.t - 5} fontSize="9.5" fill={C.mut}>처음 0.6 % 확대 — 기울기 = 영률 E</text>
      <line x1={Q.l} x2={Q.r} y1={Q.b} y2={Q.b} stroke={C.mut} />
      <line x1={Q.l} x2={Q.l} y1={Q.t} y2={Q.b} stroke={C.mut} />
      <path d={Q.poly(pts((x) => Math.min(300, sigma(m, x)), 0, 0.006, 80))} fill="none" stroke={C.sp} strokeWidth="2" />
      {e <= 0.006 && <circle cx={Q.X(e * 100)} cy={Q.Y(Math.min(300, s))} r="3.5" fill={C.red} />}
      <text x={Q.r} y={Q.b + 11} fontSize="9" fill={C.mut} textAnchor="end">0.6 %</text>
    </Frame>
  );
}

/* ── 막대의 열전도: ∂T/∂t = α ∂²T/∂x² (차분법으로 푼다) ── */
function heatFrames(kind) {
  const N = 61, r = 0.4, dx = 1 / (N - 1), dt = r * dx * dx;
  const tauMax = kind === "pulse" ? 0.12 : 0.35;
  const steps = Math.round(tauMax / dt), every = Math.max(1, Math.round(steps / 240));
  let u = Array.from({ length: N }, (_, i) => {
    const x = i * dx;
    return kind === "pulse" ? 20 + 80 * Math.exp(-((x - 0.5) ** 2) / 0.003) : kind === "ends" ? (i === 0 ? 100 : 20) : 20 + 50 * Math.sin(Math.PI * x) + 25 * Math.sin(5 * Math.PI * x);
  });
  const frames = [u.slice()];
  for (let s = 1; s <= steps; s++) {
    const v = u.slice();
    for (let i = 1; i < N - 1; i++) v[i] = u[i] + r * (u[i - 1] - 2 * u[i] + u[i + 1]);
    if (kind === "pulse") { v[0] = u[0] + 2 * r * (u[1] - u[0]); v[N - 1] = u[N - 1] + 2 * r * (u[N - 2] - u[N - 1]); }
    else if (kind === "ends") { v[0] = 100; v[N - 1] = 20; }
    else { v[0] = 20; v[N - 1] = 20; }
    u = v;
    if (s % every === 0) frames.push(u.slice());
  }
  return { frames, dtF: dt * every };
}
const heatColor = (T) => `hsl(${(220 - 2.2 * clamp(T, 0, 100)).toFixed(0)} 72% 52%)`;
export function Heat({ p = {} }) {
  const [kind, setKind] = useState(p.init || "pulse");
  const clock = useClock({ period: 12 });
  const H = useMemo(() => heatFrames(kind), [kind]);
  const F = H.frames, prog = clamp(clock.t / 10, 0, 1), fi = Math.min(F.length - 1, Math.floor((kind === "pulse" ? prog * prog : prog) * F.length)), u = F[fi];
  const P = plot({ x0: 0, x1: 1, y0: 0, y1: 110, pad: [58, 12, 22, 34] });
  const N = u.length, cw = 300 / N;
  const prof = (arr) => P.poly(arr.map((v, i) => [i / (N - 1), v]));
  const avg = u.reduce((s, v, i) => s + v * (i === 0 || i === N - 1 ? 0.5 : 1), 0) / (N - 1);
  const say = kind === "pulse"
    ? <>양 끝이 막혀 열이 나가지 않으면 뾰족한 봉우리가 낮고 넓게 퍼져 고르게(평균 <b>{fmt(avg, 1)}°</b>) 된다 — 곡선 아래 넓이(열의 양)는 그대로</>
    : kind === "ends"
      ? <>왼쪽 끝 100°, 오른쪽 끝 20° 로 고정 — 결국 곧은 직선(정상상태, ∂²T/∂x² = 0)이 된다. 그때 흐르는 열은 어디서나 같다(푸리에 법칙 q = −k dT/dx)</>
      : <>sin πx 와 sin 5πx 를 섞은 처음 모양 — 잔물결 sin 5πx 는 e<sup>−25π²αt</sup> 로 25 배 빨리 사라진다: 뾰족한 것부터 평평해진다</>;
  return (
    <Frame clock={clock} title="막대의 열전도"
      read={<>∂T/∂t = α ∂²T/∂x² — 위로 볼록한 곳(∂²T/∂x² &lt; 0)은 식고 아래로 볼록한 곳은 데워진다 · {say} · 시간 αt/L² = {fmt(fi * H.dtF, 3)}</>}
      controls={<Seg value={kind} onChange={(v) => { setKind(v); clock.reset(); }} options={[["pulse", "가운데 뜨거움"], ["ends", "양 끝 고정"], ["modes", "잔물결"]]} />}>
      {u.map((v, i) => <rect key={i} x={34 + i * cw} y="16" width={cw + 0.6} height="22" fill={heatColor(v)} />)}
      <rect x="34" y="16" width="300" height="22" fill="none" stroke={C.ink} strokeWidth="1.2" />
      {kind === "ends" && <><text x="30" y="31" fontSize="10" textAnchor="end" fill={C.red}>100°</text><text x="338" y="31" fontSize="10" fill={C.blue}>20°</text></>}
      <Axes p={P} xl="x" yl="T" />
      <path d={prof(F[0])} fill="none" stroke={C.mut} strokeDasharray="4 3" />
      <path d={prof(u)} fill="none" stroke={C.red} strokeWidth="2.6" />
    </Frame>
  );
}

/* ── P-V 순환: 둘러싼 넓이 = 한 바퀴의 일, 효율 = 일 ÷ 받은 열 ── */
function cycleOf(kind, par) {
  if (kind === "otto") {
    const g = 1.4, r = par, P2 = Math.pow(r, g), P3 = 2.5 * P2;
    const adi = (K, a, b) => (s) => { const V = a + (b - a) * s; return [V, K / Math.pow(V, g)]; };
    const iv = (V, a, b) => (s) => [V, a + (b - a) * s];
    return {
      segs: [
        { f: adi(P2, r, 1), name: "1 → 2 단열 압축 — 피스톤이 혼합기를 누른다", q: 0 },
        { f: iv(1, P2, P3), name: "2 → 3 연소 — 부피 일정, 열 Q₁ 이 들어온다", q: 1 },
        { f: adi(P3, 1, r), name: "3 → 4 단열 팽창 — 힘 행정, 일을 한다", q: 0 },
        { f: iv(r, P3 / Math.pow(r, g), 1), name: "4 → 1 배기 — 부피 일정, 열 Q₂ 를 버린다", q: -1 },
      ],
      eta: 1 - Math.pow(r, 1 - g), vmax: r, pmax: P3,
    };
  }
  const g = 5 / 3, Th = 600, tc = par, V1 = 1, V2 = 2.2, f = Math.pow(Th / tc, 1 / (g - 1)), V3 = V2 * f, V4 = V1 * f;
  const iso = (T, a, b) => (s) => { const V = a + (b - a) * s; return [V, T / V]; };
  const adi = (K, a, b) => (s) => { const V = a + (b - a) * s; return [V, K / Math.pow(V, g)]; };
  return {
    segs: [
      { f: iso(Th, V1, V2), name: "1 → 2 등온 팽창 — 고열원에서 열 Q₁ 을 받으며 밀어낸다", q: 1 },
      { f: adi((Th / V2) * Math.pow(V2, g), V2, V3), name: "2 → 3 단열 팽창 — 열 출입 없이 팽창하며 식는다", q: 0 },
      { f: iso(tc, V3, V4), name: "3 → 4 등온 압축 — 저열원으로 열 Q₂ 를 버린다", q: -1 },
      { f: adi((tc / V4) * Math.pow(V4, g), V4, V1), name: "4 → 1 단열 압축 — 다시 데워져 처음으로", q: 0 },
    ],
    eta: 1 - tc / Th, vmax: V3, pmax: Th / V1,
  };
}
export function PVCycle({ p = {} }) {
  const [kind, setKind] = useState(p.cyc || "carnot");
  const [tc, setTc] = useState(p.tc ?? 300);
  const [r, setR] = useState(p.r ?? 8);
  const clock = useClock({ period: 8 });
  const cy = cycleOf(kind, kind === "otto" ? r : tc);
  const P = plot({ x0: 0, x1: cy.vmax * (kind === "otto" ? 1.2 : 1.12), y0: 0, y1: cy.pmax * 1.1, pad: [14, 12, 24, 40] });
  const segPts = cy.segs.map((sg) => Array.from({ length: 41 }, (_, i) => sg.f(i / 40)));
  const k = Math.floor(clock.t / 2) % 4, s = (clock.t % 2) / 2;
  const [vx, py] = cy.segs[k].f(s);
  const all = segPts.flat();
  // 열 화살표 자리 — 순환 바깥쪽에서 곡선을 가리키도록(들어오는 열) · 곡선에서 바깥으로(나가는 열)
  const heat = kind === "otto"
    ? [{ i: 1, s: 0.5, dx: -1, dy: 0, inn: true }, { i: 3, s: 0.5, dx: 1, dy: 0, inn: false }]
    : [{ i: 0, s: 0.5, dx: 0, dy: -1, inn: true }, { i: 2, s: 0, dx: 1, dy: 0, inn: false }];
  return (
    <Frame clock={clock} title={kind === "otto" ? "오토 순환" : "카르노 순환"}
      read={kind === "otto"
        ? <>오토 순환(가솔린 엔진, γ = 1.4) — 지금 <b>{cy.segs[k].name}</b> · 압축비 r = {fmt(r, 1)}: η = 1 − r<sup>1 − γ</sup> = <b>{fmt(cy.eta * 100, 1)} %</b> · 둘러싼 넓이 = 한 바퀴에 한 일 W = Q₁ − Q₂</>
        : <>카르노 순환(이상기체) — 지금 <b>{cy.segs[k].name}</b> · 효율 η = 1 − T₂/T₁ = 1 − {tc}/600 = <b>{fmt(cy.eta * 100, 1)} %</b> · 둘러싼 넓이 = 한 바퀴에 한 일 W = Q₁ − Q₂</>}
      controls={<>
        <Seg value={kind} onChange={(v) => { setKind(v); clock.reset(); }} options={[["carnot", "카르노"], ["otto", "오토"]]} />
        {kind === "otto"
          ? <Slider label="압축비 r" min={3} max={12} step={0.5} value={r} onChange={setR} />
          : <Slider label="저열원 T₂" min={240} max={540} step={20} value={tc} onChange={setTc} show={(v) => v + " K"} />}
      </>}>
      <Axes p={P} xl="V" yl="P" />
      <path d={P.poly(all) + "Z"} fill={C.sp} opacity="0.16" />
      {segPts.map((pts, i) => <path key={i} d={P.poly(pts)} fill="none" stroke={cy.segs[i].q > 0 ? C.red : cy.segs[i].q < 0 ? C.blue : C.ink} strokeWidth={i === k ? 3.2 : 1.6} />)}
      {heat.map(({ i, s: hs, dx, dy, inn }) => {
        const [mv, mp] = cy.segs[i].f(hs), X0 = P.X(mv), Y0 = P.Y(mp), L = 26;
        return (
          <g key={"q" + i}>
            <Arrow x1={inn ? X0 + dx * L : X0 + dx * 3} y1={inn ? Y0 + dy * L : Y0} x2={inn ? X0 - dx * 2 : X0 + dx * L} y2={inn ? Y0 - dy * 2 : Y0 + dy * L} color={inn ? C.red : C.blue} w={2} />
            <Label x={X0 + dx * (L + 10)} y={Y0 + dy * (L + 8) + 4} anchor="middle" size={11} color={inn ? C.red : C.blue} bold bg>{inn ? "Q₁" : "Q₂"}</Label>
          </g>
        );
      })}
      <Label x={P.X(all.reduce((s2, q) => s2 + q[0], 0) / all.length)} y={P.Y(all.reduce((s2, q) => s2 + q[1], 0) / all.length) + 4} anchor="middle" size={11} color={C.sp} bold>W</Label>
      <circle cx={P.X(vx)} cy={P.Y(py)} r="5" fill={C.gold} stroke={C.ink} />
    </Frame>
  );
}

/* ── 벤투리관: 좁은 곳이 빠르고(연속방정식), 빠른 곳이 압력이 낮다(베르누이) ── */
export function Venturi({ p = {} }) {
  const [ratio, setRatio] = useState(p.ratio ?? 0.5);
  const [v1, setV1] = useState(p.v1 ?? 2);
  const clock = useClock({ period: 60 });
  const R1 = 30, cy = 160, X = (x) => 10 + x * 34;
  const Rx = (x) => {
    const s = x < 3 ? 0 : x < 4.2 ? 0.5 - 0.5 * Math.cos((Math.PI * (x - 3)) / 1.2) : x < 5.8 ? 1 : x < 7.6 ? 0.5 + 0.5 * Math.cos((Math.PI * (x - 5.8)) / 1.8) : 0;
    return R1 * (1 - (1 - ratio) * s);
  };
  const flow = useMemo(() => {
    const n = 500, tab = [0];
    for (let i = 1; i <= n; i++) { const x = (10 * (i - 0.5)) / n, sp = 14 * v1 * (R1 / Rx(x)) ** 2; tab.push(tab[i - 1] + (34 * (10 / n)) / sp); }
    const r = rng(3), parts = Array.from({ length: 70 }, (_, j) => [((j * 0.6180339) % 1) * tab[n], r() * 1.7 - 0.85]);
    return { tab, parts, n };
  }, [ratio, v1]); // eslint-disable-line react-hooks/exhaustive-deps
  const xAt = (tau) => { const { tab, n } = flow; let lo = 0, hi = n; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (tab[m] <= tau) lo = m; else hi = m; } return (10 * (lo + (tau - tab[lo]) / (tab[hi] - tab[lo] || 1))) / n; };
  const top = [], bot = [];
  for (let i = 0; i <= 100; i++) { const x = i / 10; top.push([X(x), cy - Rx(x)]); bot.push([X(x), cy + Rx(x)]); }
  const v2 = v1 / (ratio * ratio), dh = (v2 * v2 - v1 * v1) / (2 * 9.8), dp = (0.5 * 1000 * (v2 * v2 - v1 * v1)) / 1000;
  const wl1 = 54, wl2 = Math.min(cy - Rx(5) - 4, wl1 + dh * 10);
  const tube = (x, wl) => (
    <g>
      <rect x={X(x) - 5} y="14" width="10" height={cy - Rx(x) - 14} fill={C.card} stroke={C.ink} strokeWidth="1" />
      <rect x={X(x) - 4} y={wl} width="8" height={cy - Rx(x) - wl} fill={C.blue} opacity="0.55" />
    </g>
  );
  const T = flow.tab[flow.n];
  return (
    <Frame clock={clock} title="벤투리관 — 연속방정식과 베르누이"
      read={<>A₁v₁ = A₂v₂: 지름이 {fmt(ratio, 2)} 배면 넓이는 {fmt(ratio * ratio, 2)} 배, 속력은 <b>{fmt(1 / (ratio * ratio), 2)} 배</b> → v₂ = {fmt(v2, 1)} m/s · 베르누이: p₁ − p₂ = ½ρ(v₂² − v₁²) = <b>{fmt(dp, 1)} kPa</b> — 물기둥 높이 차 {fmt(dh, 2)} m · <b>빠른 곳이 압력이 낮다</b></>}
      controls={<>
        <Slider label="지름비 d₂/d₁" min={0.4} max={1} step={0.05} value={ratio} onChange={setRatio} />
        <Slider label="v₁" min={0.5} max={2.5} step={0.25} value={v1} onChange={setV1} show={(v) => fmt(v, 2) + " m/s"} />
      </>}>
      <path d={"M" + top.map(([x, y]) => x.toFixed(1) + " " + y.toFixed(1)).join("L") + "L" + bot.slice().reverse().map(([x, y]) => x.toFixed(1) + " " + y.toFixed(1)).join("L") + "Z"} fill={C.blue} opacity="0.12" />
      <path d={"M" + top.map(([x, y]) => x.toFixed(1) + " " + y.toFixed(1)).join("L")} fill="none" stroke={C.ink} strokeWidth="2" />
      <path d={"M" + bot.map(([x, y]) => x.toFixed(1) + " " + y.toFixed(1)).join("L")} fill="none" stroke={C.ink} strokeWidth="2" />
      {tube(1.5, wl1)}{tube(5, wl2)}
      <line x1={X(1.5) + 5} x2={X(5) + 14} y1={wl1} y2={wl1} stroke={C.mut} strokeDasharray="3 3" />
      {dh > 0.05 && <><Arrow x1={X(5) + 12} y1={wl1} x2={X(5) + 12} y2={wl2} color={C.red} w={1.4} head={5} /><Label x={X(5) + 18} y={(wl1 + wl2) / 2 + 4} size={10} color={C.red} bg>Δh = {fmt(dh, 2)} m</Label></>}
      <text x={X(1.5)} y="214" textAnchor="middle" fontSize="10" fill={C.mut}>넓은 곳 p₁</text>
      <text x={X(5)} y="214" textAnchor="middle" fontSize="10" fill={C.mut}>좁은 곳 p₂</text>
      {flow.parts.map(([ph, f], j) => { const x = xAt((((clock.t + ph) % T) + T) % T); return <circle key={j} cx={X(x)} cy={cy + f * Rx(x)} r="2" fill={C.sp} />; })}
    </Frame>
  );
}

/* ── 경사면 굴림 경주: 가속도 = g sin θ ÷ (1 + I/mR²) — 모양만이 순서를 정한다 ── */
const ROLL = [["미끄러짐 (마찰 없음)", 0, "block", C.mut], ["속이 찬 공 (2/5)", 0.4, "ball", C.red], ["원판 · 원기둥 (1/2)", 0.5, "disk", C.blue], ["고리 · 빈 원통 (1)", 1, "ring", C.gold]];
export function Rolling({ p = {} }) {
  const [deg, setDeg] = useState(p.deg ?? 20);
  const clock = useClock({ period: 7 });
  const th = (deg * Math.PI) / 180, Ls = 3, tp = clock.t * 0.55;
  const dx = 222, dy = 34, len = Math.hypot(dx, dy), ux = dx / len, uy = dy / len, nx = uy, ny = -ux, rr = 9;
  return (
    <Frame clock={clock} title="경사면 굴림 경주"
      read={<>a = g sin θ ÷ (1 + I/mR²), θ = <b>{deg}°</b> · 도착 순서: 미끄러짐 → 공 → 원판 → 고리 — 질량 · 반지름과 상관없이 <b>모양(I/mR²)</b> 만 정한다 · 구르는 물체는 위치에너지의 일부를 회전에 나눠 준다 (그림은 경사를 눕혀 그렸다)</>}
      controls={<Slider label="경사각 θ" min={5} max={45} step={5} value={deg} onChange={(v) => { setDeg(v); clock.reset(); }} show={(v) => v + "°"} />}>
      {ROLL.map(([name, c, kind, col], i) => {
        const a = (9.8 * Math.sin(th)) / (1 + c), tf = Math.sqrt((2 * Ls) / a), s = Math.min(Ls, 0.5 * a * tp * tp);
        const y0 = 22 + i * 50, x0 = 124, u = (s / Ls) * (len - 2 * rr) + rr;
        const cx = x0 + ux * u + nx * rr, cyy = y0 + uy * u + ny * rr, ang = u / rr;
        const done = s >= Ls;
        return (
          <g key={i}>
            <text x="6" y={y0 + 12} fontSize="10" fill={C.ink}>{name}</text>
            <text x="6" y={y0 + 26} fontSize="9.5" fill={C.mut}>a = {fmt(a, 2)} m/s²</text>
            <line x1={x0} y1={y0} x2={x0 + dx} y2={y0 + dy} stroke={C.ink} strokeWidth="1.6" />
            <line x1={x0 + dx} y1={y0 + dy - 22} x2={x0 + dx} y2={y0 + dy + 4} stroke={C.green} strokeWidth="1.6" strokeDasharray="2 2" />
            {kind === "block"
              ? <rect x={cx - rr} y={cyy - rr} width={2 * rr} height={2 * rr} rx="2" fill={col} transform={`rotate(${((Math.atan2(dy, dx) * 180) / Math.PI).toFixed(1)} ${cx.toFixed(1)} ${cyy.toFixed(1)})`} />
              : <g>
                <circle cx={cx} cy={cyy} r={rr} fill={kind === "ring" ? "none" : col} stroke={col} strokeWidth={kind === "ring" ? 3.2 : 1} opacity={kind === "ball" ? 0.9 : 1} />
                <line x1={cx} y1={cyy} x2={cx + rr * Math.cos(ang)} y2={cyy + rr * Math.sin(ang)} stroke={kind === "ring" ? col : "#fff"} strokeWidth="1.6" />
              </g>}
            {done && <Label x={x0 + dx - 4} y={y0 + dy - 26} anchor="end" size={10} color={col} bold bg>{fmt(tf, 2)} s</Label>}
          </g>
        );
      })}
    </Frame>
  );
}
