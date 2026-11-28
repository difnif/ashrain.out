// 화학 그림 — 한계 반응물 · 반데르발스 등온선 · 깁스 자유 에너지 · 평형과 르샤틀리에 · 적정 곡선 · 활성화 에너지 · 네른스트 식 · 수소 원자 스펙트럼
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, lerp, sup, useClock } from "./kit.jsx";

/* ── 한계 반응물: 2H₂ + O₂ → 2H₂O ── */
export function Limiting({ p = {} }) {
  const [o2, setO2] = useState(clamp(p.o2 ?? 4, 1, 9));
  const clock = useClock({ period: 9, rest: 8 });
  const h2 = 10, maxW = Math.min(h2, 2 * o2), prog = clamp((clock.t - 1) / 5, 0, 1), w = 2 * Math.round((maxW / 2) * prog);
  const leftH = h2 - w, leftO = o2 - w / 2;
  const lim = 2 * o2 < h2 ? "O₂" : 2 * o2 > h2 ? "H₂" : "없음(딱 맞음)";
  const mol = (x, y, kind, k) => {
    if (kind === "H2") return <g key={k}><circle cx={x - 3.2} cy={y} r="3.6" fill={C.blue} /><circle cx={x + 3.2} cy={y} r="3.6" fill={C.blue} /></g>;
    if (kind === "O2") return <g key={k}><circle cx={x - 4.4} cy={y} r="5" fill={C.red} /><circle cx={x + 4.4} cy={y} r="5" fill={C.red} /></g>;
    return <g key={k}><circle cx={x} cy={y} r="5.4" fill={C.red} /><circle cx={x - 5.6} cy={y + 3.8} r="3.2" fill={C.blue} /><circle cx={x + 5.6} cy={y + 3.8} r="3.2" fill={C.blue} /></g>;
  };
  const grid = (n, x0, y0, cols, dx, dy, kind, pre) => Array.from({ length: n }, (_, i) => mol(x0 + (i % cols) * dx, y0 + Math.floor(i / cols) * dy, kind, pre + i));
  const massL = leftH * 2 + leftO * 32 + w * 18;
  return (
    <Frame clock={clock} title="한계 반응물 — 먼저 떨어지는 쪽이 양을 정한다"
      read={<>2H₂ + O₂ → 2H₂O · H₂ {h2} 개와 O₂ {o2} 개 · 물은 최대 {maxW} 개 생긴다 — 한계 반응물 <b>{lim}</b>{leftH > 0 && prog >= 1 ? `, H₂ ${leftH} 개가 남는다` : ""}{leftO > 0 && prog >= 1 ? `, O₂ ${fmt(leftO, 1)} 개가 남는다` : ""} · 지금 물 {w} 개 · 전체 질량(g/mol 단위) {fmt(massL, 0)} 은 반응 내내 그대로(질량 보존)</>}
      controls={<Slider label="O₂ 개수" min={1} max={9} step={1} value={o2} onChange={(v) => { setO2(v); clock.reset(); }} />}>
      <rect x="8" y="14" width="168" height="196" rx="10" fill="none" stroke={C.bd} />
      <rect x="184" y="14" width="168" height="196" rx="10" fill="none" stroke={C.bd} />
      <text x="92" y="30" textAnchor="middle" fontSize="10.5" fill={C.mut}>남은 반응물</text>
      <text x="268" y="30" textAnchor="middle" fontSize="10.5" fill={C.mut}>생성물 H₂O</text>
      {grid(leftH, 34, 52, 4, 36, 24, "H2", "h")}
      {grid(Math.ceil(leftO), 34, 52 + Math.ceil(leftH / 4) * 24 + 6, 4, 36, 26, "O2", "o")}
      {grid(w, 210, 54, 4, 38, 30, "W", "w")}
      <text x="92" y="202" textAnchor="middle" fontSize="10" fill={C.blue}>H₂ {leftH}</text>
      <text x="140" y="202" textAnchor="middle" fontSize="10" fill={C.red}>O₂ {fmt(leftO, 1)}</text>
      <text x="268" y="202" textAnchor="middle" fontSize="10" fill={C.ink}>H₂O {w}</text>
    </Frame>
  );
}

/* ── 반데르발스 기체: 임계 온도 아래의 고리와 맥스웰 등면적 ── */
const VA = 3.64, VB = 0.04267, RL = 0.08314;
const PV = (V, T) => (RL * T) / (V - VB) - VA / (V * V);
function maxwell(T) {
  const Vs = Array.from({ length: 1200 }, (_, i) => 0.05 + (i / 1199) * 0.75), Ps = Vs.map((v) => PV(v, T));
  let mn = null, mx = null;
  for (let i = 1; i < Vs.length - 1; i++) {
    if (Ps[i] < Ps[i - 1] && Ps[i] < Ps[i + 1] && mn === null) mn = i;
    if (Ps[i] > Ps[i - 1] && Ps[i] > Ps[i + 1] && mn !== null && mx === null) mx = i;
  }
  if (mn === null || mx === null) return null;
  const roots = (Ps0) => { const r = []; for (let i = 1; i < Vs.length; i++) if ((Ps[i - 1] - Ps0) * (Ps[i] - Ps0) <= 0) { const t = (Ps0 - Ps[i - 1]) / (Ps[i] - Ps[i - 1]); r.push(Vs[i - 1] + t * (Vs[i] - Vs[i - 1])); } return r; };
  const area = (Ps0) => { const r = roots(Ps0); if (r.length < 3) return null; const a = r[0], c = r[r.length - 1]; let s = 0; const n = 400; for (let i = 0; i < n; i++) { const v = a + ((c - a) * (i + 0.5)) / n; s += (PV(v, T) - Ps0) * ((c - a) / n); } return { s, a, c }; };
  let lo = Math.max(0.5, Ps[mn] + 1e-6), hi = Ps[mx] - 1e-6;
  for (let k = 0; k < 50; k++) { const m = (lo + hi) / 2, A = area(m); if (!A) break; if (A.s > 0) lo = m; else hi = m; }
  const P0 = (lo + hi) / 2, A = area(P0);
  return A ? { P: P0, Vl: A.a, Vg: A.c } : null;
}
export function VdW() {
  const clock = useClock({ period: 14, rest: 3.5 });
  const T = Math.round(255 + 85 * (0.5 - 0.5 * Math.cos((clock.t / 14) * 2 * Math.PI)));
  const M = useMemo(() => maxwell(T), [T]);
  const P = plot({ x0: 0.05, x1: 0.6, y0: 0, y1: 130, pad: [12, 12, 26, 34] });
  const below = T < 304;
  const v0 = (() => { for (let v = 0.045; v < 0.6; v += 0.0005) if (PV(v, T) <= 128) return v; return 0.1; })(), vi = (RL * T) / 128;
  return (
    <Frame clock={clock} title="실제 기체 — 반데르발스 등온선"
      read={<>이산화 탄소, T = <b>{T} K</b> · 반데르발스 식 P = RT ÷ (V − b) − a ÷ V² (빨강)과 이상기체 P = RT ÷ V (회색 점선) · {below && M ? <>임계 온도 304 K 아래 — 곡선이 구불거리는 구간은 실제로는 일어나지 않고, 압력 {fmt(M.P, 1)} bar 의 수평선(맥스웰 등면적 — 위아래 넓이가 같다)을 따라 액체와 기체가 함께 있다(V = {fmt(M.Vl, 3)} ~ {fmt(M.Vg, 3)} L/mol)</> : "임계 온도 304 K 위에서는 아무리 눌러도 액체가 되지 않는다(초임계 유체)"} · 분자의 크기(b)와 끌림(a)이 이상기체와의 차이를 만든다</>}>
      <Axes p={P} xl="V (L/mol)" yl="P (bar)" grid={false} xt={[0.1, 0.2, 0.3, 0.4, 0.5]} yt={[40, 80, 120]} />
      <path d={P.path((v) => (RL * T) / v, vi, 0.6, 200)} fill="none" stroke={C.mut} strokeWidth="1.2" strokeDasharray="4 3" />
      {below && M && <path d={P.poly([[M.Vl, M.P], [M.Vg, M.P]])} fill="none" stroke={C.green} strokeWidth="2.2" />}
      {below && M && <path d={P.path((v) => PV(v, T), M.Vl, M.Vg, 160)} fill="none" stroke={C.red} strokeWidth="1.3" strokeDasharray="3 3" />}
      <path d={P.path((v) => PV(v, T), v0, below && M ? M.Vl : 0.6, 200)} fill="none" stroke={C.red} strokeWidth="2.2" />
      {below && M && <path d={P.path((v) => PV(v, T), M.Vg, 0.6, 200)} fill="none" stroke={C.red} strokeWidth="2.2" />}
      <circle cx={P.X(0.128)} cy={P.Y(74)} r="3.4" fill={C.gold} />
      <Label x={P.X(0.128) + 6} y={P.Y(74) - 6} size={9.5} color={C.gold} bg>임계점</Label>
    </Frame>
  );
}

/* ── 깁스 자유 에너지: ΔG = ΔH − TΔS ── */
const GB = {
  melt: { name: "얼음 → 물", dH: 6.01, dS: 22.0, eq: "H₂O(s) → H₂O(l)" },
  nh3: { name: "암모니아 합성", dH: -92.2, dS: -198.7, eq: "N₂ + 3H₂ → 2NH₃" },
  h2o2: { name: "과산화 수소 분해", dH: -196.0, dS: 125.8, eq: "2H₂O₂ → 2H₂O + O₂" },
  o3: { name: "오존 만들기", dH: 285.4, dS: -137.8, eq: "3O₂ → 2O₃" },
};
export function Gibbs({ p = {} }) {
  const [k, setK] = useState(GB[p.rx] ? p.rx : "nh3");
  const S = GB[k];
  const clock = useClock({ period: 10, rest: 6 });
  const T = 100 + 800 * (0.5 - 0.5 * Math.cos((clock.t / 10) * 2 * Math.PI));
  const G = (t) => S.dH - (t * S.dS) / 1000;
  const lo = Math.min(G(0), G(1000)), hi = Math.max(G(0), G(1000));
  const pad = Math.max(20, (hi - lo) * 0.12);
  const P = plot({ x0: 0, x1: 1000, y0: Math.min(-pad, lo - pad), y1: Math.max(pad, hi + pad), pad: [12, 12, 26, 40] });
  const Ts = S.dH / (S.dS / 1000), cross = Ts > 0 && Ts < 1000;
  const g = G(T);
  return (
    <Frame clock={clock} title="깁스 자유 에너지 — 반응은 언제 저절로 일어날까"
      read={<>{S.eq} ({S.name}) · ΔH = {fmt(S.dH, 1)} kJ, ΔS = {fmt(S.dS, 1)} J/K · ΔG = ΔH − TΔS 가 음수면 저절로 일어난다(초록 영역) · T = {fmt(T, 0)} K 에서 ΔG = <b>{fmt(g, 1)} kJ</b> → {g < 0 ? "저절로 일어난다" : "저절로 일어나지 않는다"} · {cross ? <>경계 온도 T = ΔH ÷ ΔS = {fmt(Ts, 0)} K {S.dS > 0 ? "보다 높으면 일어난다(엔트로피가 이긴다)" : "보다 낮으면 일어난다(엔탈피가 이긴다)"}</> : S.dH < 0 ? "ΔH < 0, ΔS > 0 — 어떤 온도에서도 저절로 일어난다" : "ΔH > 0, ΔS < 0 — 어떤 온도에서도 저절로 일어나지 않는다"}</>}
      controls={<Seg value={k} onChange={setK} options={[["melt", "얼음 녹기"], ["nh3", "NH₃ 합성"], ["h2o2", "H₂O₂ 분해"], ["o3", "O₃ 생성"]]} />}>
      <rect x={P.l} y={P.Y(0)} width={P.r - P.l} height={P.b - P.Y(0)} fill={C.green} opacity="0.1" />
      <Axes p={P} xl="T (K)" yl="ΔG (kJ)" grid={false} xt={[200, 400, 600, 800]} yfmt={(v) => fmt(v, 0)} />
      <path d={P.path(G, 0, 1000, 2)} fill="none" stroke={C.blue} strokeWidth="2.4" />
      {cross && <line x1={P.X(Ts)} x2={P.X(Ts)} y1={P.t} y2={P.b} stroke={C.gold} strokeWidth="1.2" strokeDasharray="4 3" />}
      {cross && <Label x={P.X(Ts) + 4} y={P.t + 12} size={9.5} color={C.gold} bg>{fmt(Ts, 0)} K</Label>}
      <line x1={P.X(T)} x2={P.X(T)} y1={P.Y(0)} y2={P.Y(g)} stroke={g < 0 ? C.green : C.red} strokeWidth="1.4" />
      <circle cx={P.X(T)} cy={P.Y(g)} r="4.6" fill={g < 0 ? C.green : C.red} />
      <Label x={P.r - 4} y={P.b - 6} size={9.5} color={C.green} anchor="end">ΔG &lt; 0 : 저절로</Label>
    </Frame>
  );
}

/* ── 평형과 르샤틀리에: A ⇌ B, K = 2 ── */
const KF = 1, KB = 0.5;
function eqRun(kind) {
  const out = []; let A = 1, B = 0, kb = KB; const dt = 0.02;
  for (let i = 0; i <= 600; i++) {
    const t = i * dt;
    if (i === 300) { if (kind === "addA") A += 0.6; else if (kind === "remB") B *= 0.3; else kb = 1.5; }
    out.push({ t, A, B, K: KF / kb });
    const r = KF * A - kb * B; A -= r * dt; B += r * dt;
  }
  return out;
}
export function Equil({ p = {} }) {
  const [k, setK] = useState(["addA", "remB", "heat"].includes(p.kind) ? p.kind : "addA");
  const R = useMemo(() => eqRun(k), [k]);
  const clock = useClock({ period: 13, rest: 12 });
  const i = Math.min(R.length - 1, Math.floor((clock.t / 12) * (R.length - 1)));
  const s = R[i], Q = s.B / Math.max(1e-9, s.A);
  const P = plot({ x0: 0, x1: 12, y0: 0, y1: 1.7, pad: [12, 12, 26, 32] });
  const msg = { addA: "A 를 더하면 Q < K 가 되어 정반응이 빨라지고, 새 평형에서는 B 도 늘어난다", remB: "B 를 빼면 Q < K 가 되어 A 가 B 로 바뀌며 빈자리를 메운다", heat: "온도를 바꾸면 K 자체가 바뀐다(이 반응은 역반응이 빨라져 K = 2 → 0.67) — 새 K 에 맞춰 A 쪽으로 옮겨 간다" }[k];
  return (
    <Frame clock={clock} title="화학 평형 — 르샤틀리에의 원리"
      read={<>A ⇌ B · 정반응 속도 k₁[A], 역반응 속도 k₋₁[B] — 두 속도가 같아지면 평형 · t = {fmt(s.t, 1)}: [A] = {fmt(s.A, 3)}, [B] = {fmt(s.B, 3)}, 반응 지수 Q = [B] ÷ [A] = <b>{fmt(Q, 2)}</b>, 평형 상수 K = {fmt(s.K, 2)} · t = 6 에서 흔든다: {msg} — 평형은 방해를 줄이는 쪽으로 움직인다</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["addA", "A 더하기"], ["remB", "B 빼기"], ["heat", "온도 바꾸기"]]} />}>
      <Axes p={P} xl="시간" yl="농도" grid={false} xt={[3, 6, 9]} yt={[0.5, 1, 1.5]} />
      <line x1={P.X(6)} x2={P.X(6)} y1={P.t} y2={P.b} stroke={C.gold} strokeWidth="1" strokeDasharray="4 3" />
      <path d={P.poly(R.slice(0, i + 1).map((q) => [q.t, q.A]))} fill="none" stroke={C.blue} strokeWidth="2.2" />
      <path d={P.poly(R.slice(0, i + 1).map((q) => [q.t, q.B]))} fill="none" stroke={C.red} strokeWidth="2.2" />
      <Label x={P.X(Math.min(s.t, 11)) + 4} y={P.Y(s.A) + (s.A > s.B ? -6 : 14)} size={10} color={C.blue} bold>[A]</Label>
      <Label x={P.X(Math.min(s.t, 11)) + 4} y={P.Y(s.B) + (s.B >= s.A ? -6 : 14)} size={10} color={C.red} bold>[B]</Label>
      <Label x={P.X(6) + 4} y={P.t + 12} size={9.5} color={C.gold} bg>흔들기</Label>
    </Frame>
  );
}

/* ── 적정 곡선: 0.1 M 산 25 mL 를 0.1 M NaOH 로 ── */
const KA = 1.8e-5;
function pHof(vb, weak) {
  const C0 = (0.1 * 25) / (25 + vb), Na = (0.1 * vb) / (25 + vb);
  let lo = -14, hi = 0;
  for (let k = 0; k < 80; k++) {
    const m = (lo + hi) / 2, h = 10 ** m, A = weak ? (C0 * KA) / (KA + h) : C0;
    if (Na + h - 1e-14 / h - A > 0) hi = m; else lo = m;
  }
  return -(lo + hi) / 2;
}
const TCURVE = { weak: Array.from({ length: 251 }, (_, i) => pHof(i / 5, true)), strong: Array.from({ length: 251 }, (_, i) => pHof(i / 5, false)) };
export function Titration({ p = {} }) {
  const [k, setK] = useState(p.acid === "strong" ? "strong" : "weak");
  const clock = useClock({ period: 13, rest: 12 });
  const vb = clamp((clock.t / 11.5) * 50, 0, 50), i = Math.round(vb * 5), ph = TCURVE[k][i];
  const P = plot({ x0: 0, x1: 50, y0: 0, y1: 14, pad: [12, 70, 26, 30] });
  const pink = clamp((ph - 8.2) / 1.8, 0, 1);
  return (
    <Frame clock={clock} title="중화 적정 — pH 가 갑자기 뛰는 곳"
      read={<>{k === "weak" ? "아세트산(약산, Ka = 1.8 × 10⁻⁵)" : "염산(강산)"} 0.1 M 25 mL 에 0.1 M NaOH 를 넣는다 · 넣은 양 {fmt(vb, 1)} mL, pH = <b>{fmt(ph, 2)}</b> · 당량점 25 mL 에서 pH 가 {k === "weak" ? "8.7 근처로" : "7 을 지나"} 가파르게 뛴다 · {k === "weak" ? "반쯤 중화된 12.5 mL 에서 pH = pKa = 4.74 — 그 둘레는 pH 가 잘 변하지 않는 완충 구간(헨더슨–하셀바흐 식)" : "강산은 처음 pH 가 1 로 낮고 완충 구간이 없다"} · 페놀프탈레인은 pH 8.2 ~ 10 에서 분홍으로 바뀐다</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["weak", "약산(아세트산)"], ["strong", "강산(염산)"]]} />}>
      <Axes p={P} xl="NaOH (mL)" yl="pH" grid={false} xt={[12.5, 25, 37.5, 50]} yt={[4, 7, 10, 14]} xfmt={(v) => fmt(v, 1)} />
      {k === "weak" && <rect x={P.X(5)} y={P.t} width={P.X(20) - P.X(5)} height={P.b - P.t} fill={C.gold} opacity="0.1" />}
      <line x1={P.X(25)} x2={P.X(25)} y1={P.t} y2={P.b} stroke={C.mut} strokeWidth="1" strokeDasharray="4 3" />
      <path d={P.poly(TCURVE[k].map((v, j) => [j / 5, v]))} fill="none" stroke={C.mut} strokeWidth="1" opacity="0.4" />
      <path d={P.poly(TCURVE[k].slice(0, i + 1).map((v, j) => [j / 5, v]))} fill="none" stroke={C.blue} strokeWidth="2.4" />
      <circle cx={P.X(vb)} cy={P.Y(ph)} r="4.4" fill={C.red} />
      {k === "weak" && <circle cx={P.X(12.5)} cy={P.Y(4.74)} r="3" fill={C.gold} />}
      {k === "weak" && <Label x={P.X(12.5)} y={P.Y(4.74) - 8} size={9} color={C.gold} anchor="middle" bg>pH = pKa</Label>}
      <g>
        <path d="M 308 70 L 308 176 Q 308 192 324 192 L 334 192 Q 350 192 350 176 L 350 70" fill="none" stroke={C.mut} strokeWidth="1.6" />
        <rect x="309.5" y={176 - 70 * (0.5 + vb / 100)} width="39" height={70 * (0.5 + vb / 100) + 14} rx="6" fill="#9fb8cf" fillOpacity="0.18" />
        <rect x="309.5" y={176 - 70 * (0.5 + vb / 100)} width="39" height={70 * (0.5 + vb / 100) + 14} rx="6" fill="#d63384" fillOpacity={0.6 * pink} />
        <text x="329" y="62" textAnchor="middle" fontSize="9.5" fill={C.mut}>페놀프탈레인</text>
      </g>
    </Frame>
  );
}

/* ── 활성화 에너지: 볼츠만 분포의 꼬리와 아레니우스 그림 ── */
const RG = 8.314e-3;
const MB = (E, T) => { const kT = RG * T; return 2 * Math.sqrt(E / Math.PI) * kT ** -1.5 * Math.exp(-E / kT); };
const tailFrac = (Ea, T) => { const kT = RG * T, x = Ea / kT; let s = 0; const n = 400, top = Ea + 30 * kT; for (let i = 0; i < n; i++) { const E = Ea + ((top - Ea) * (i + 0.5)) / n; s += MB(E, T) * ((top - Ea) / n); } return s; };
export function Arrhenius({ p = {} }) {
  const [mode, setMode] = useState(p.mode === "plot" ? "plot" : "dist");
  const [cat, setCat] = useState(!!p.cat);
  const clock = useClock({ period: 12, rest: 9 });
  const Ea = cat ? 10 : 16, T1 = 300, T2 = 300 + 60 * (0.5 - 0.5 * Math.cos((clock.t / 12) * 2 * Math.PI));
  if (mode === "dist") {
    const P = plot({ x0: 0, x1: 26, y0: 0, y1: 0.22, pad: [12, 12, 26, 34] });
    const f1 = tailFrac(Ea, T1), f2 = tailFrac(Ea, T2);
    return (
      <Frame clock={clock} title="활성화 에너지 — 문턱을 넘는 분자의 비율"
        read={<>분자 운동 에너지의 분포(볼츠만) — 파랑 T = 300 K, 빨강 T = {fmt(T2, 0)} K · 활성화 에너지 Ea = {Ea} kJ/mol{cat ? "(촉매가 낮춘 값)" : ""} 를 넘는 비율: {fmt(100 * f1, 2)} % → <b>{fmt(100 * f2, 2)} %</b>({fmt(f2 / f1, 2)} 배) · 온도를 조금만 올려도 꼬리가 크게 두꺼워진다 — 실제 반응(Ea ≈ 50 kJ/mol)은 25 ℃ 에서 10 ℃ 올리면 속도가 약 두 배 · 촉매는 문턱 자체를 낮춘다</>}
        controls={<><Seg value={mode} onChange={setMode} options={[["dist", "에너지 분포"], ["plot", "아레니우스 그림"]]} /><Seg value={cat ? "on" : "off"} onChange={(v) => setCat(v === "on")} options={[["off", "촉매 없음"], ["on", "촉매"]]} /></>}>
        <Axes p={P} xl="E (kJ/mol)" yl="" grid={false} xt={[5, 10, 15, 20, 25]} yt={[]} />
        <path d={P.poly([[Ea, 0], ...Array.from({ length: 60 }, (_, j) => { const E = Ea + ((26 - Ea) * j) / 59; return [E, MB(E, T2)]; }), [26, 0]])} fill={C.red} opacity="0.25" />
        <path d={P.path((E) => MB(E, T1), 0.001, 26, 220)} fill="none" stroke={C.blue} strokeWidth="2.2" />
        <path d={P.path((E) => MB(E, T2), 0.001, 26, 220)} fill="none" stroke={C.red} strokeWidth="2.2" />
        <path d={P.path((E) => 20 * MB(E, T2), Ea, 26, 80)} fill="none" stroke={C.red} strokeWidth="1.2" strokeDasharray="4 3" />
        <line x1={P.X(Ea)} x2={P.X(Ea)} y1={P.t} y2={P.b} stroke={C.gold} strokeWidth="1.6" />
        <Label x={P.X(Ea) + 4} y={P.t + 12} size={10} color={C.gold} bold bg>Ea = {Ea}</Label>
        <Label x={P.X(Ea) + 4} y={P.Y(20 * MB(Ea + 1.5, T2)) - 4} size={9} color={C.red}>꼬리 × 20</Label>
      </Frame>
    );
  }
  const P = plot({ x0: 2.6, x1: 3.5, y0: -1.5, y1: 4.8, pad: [14, 14, 30, 34] });
  const lnk = (invT, ea) => -(ea / RG) * (invT / 1000 - 1 / 300);
  const cur = 1000 / T2;
  return (
    <Frame clock={clock} title="아레니우스 그림 — ln k 와 1/T 는 직선"
      read={<>k = A × exp(−Ea ÷ RT) 의 로그를 잡으면 ln k = ln A − (Ea ÷ R)(1 ÷ T) — 가로 1000 ÷ T, 세로 ln k(300 K 기준)로 그리면 직선이고 기울기가 −Ea ÷ R · 지금 T = {fmt(T2, 0)} K: k 가 300 K 의 <b>{fmt(Math.exp(lnk(cur, Ea)), 2)}</b> 배 · 기울기가 가파를수록(Ea 큼) 온도에 민감하다 — 측정한 두 온도의 속도로 Ea 를 구하는 방법</>}
      controls={<><Seg value={mode} onChange={setMode} options={[["dist", "에너지 분포"], ["plot", "아레니우스 그림"]]} /><Seg value={cat ? "on" : "off"} onChange={(v) => setCat(v === "on")} options={[["off", "촉매 없음"], ["on", "촉매"]]} /></>}>
      <Axes p={P} xl="1000 ÷ T" yl="ln k" grid={false} xt={[2.8, 3.0, 3.2, 3.4]} yt={[2, 4]} xfmt={(v) => fmt(v, 1)} />
      <path d={P.path((x) => lnk(x, 50), 2.6, 3.5, 2)} fill="none" stroke={C.mut} strokeWidth="1.2" strokeDasharray="4 3" />
      <path d={P.path((x) => lnk(x, Ea), 2.6, 3.5, 2)} fill="none" stroke={C.red} strokeWidth="2.2" />
      <circle cx={P.X(cur)} cy={P.Y(lnk(cur, Ea))} r="4.4" fill={C.red} />
      <Label x={P.X(2.65)} y={P.Y(lnk(2.65, 50)) + 14} size={9} color={C.mut}>Ea = 50 (보통 반응)</Label>
    </Frame>
  );
}

/* ── 네른스트 식: 다니엘 전지가 방전하며 전압이 준다 ── */
export function Nernst() {
  const clock = useClock({ period: 14, rest: 10 });
  const x = 0.999 * (1 - Math.cos((clock.t / 14) * Math.PI)) * 0.5;
  const zn = 1 + x, cu = 1 - x, Q = zn / cu, E = 1.1 - (0.05916 / 2) * Math.log10(Q);
  const P = plot({ x0: 0, x1: 1, y0: 0.95, y1: 1.14, pad: [14, 150, 28, 40] });
  const Ex = (u) => 1.1 - (0.05916 / 2) * Math.log10((1 + u) / Math.max(1e-6, 1 - u));
  return (
    <Frame clock={clock} title="전지의 전압 — 네른스트 식"
      read={<>다니엘 전지 Zn | Zn²⁺ ‖ Cu²⁺ | Cu, 표준 전압 E° = 1.10 V · 방전하면 Cu²⁺ 가 줄고 Zn²⁺ 가 는다: [Zn²⁺] = {fmt(zn, 3)} M, [Cu²⁺] = {fmt(cu, 3)} M · E = E° − (0.0592 ÷ 2) log₁₀ Q = <b>{fmt(E, 3)} V</b> · 농도가 열 배 바뀌어도 전압은 0.03 V 쯤만 변하다가, Cu²⁺ 가 바닥날 때 급히 떨어진다 · E = 0 이 되는 평형 상수 K = 10³⁷ — 반응이 거의 끝까지 간다</>}>
      <Axes p={P} xl="방전한 정도" yl="E (V)" grid={false} xt={[0.25, 0.5, 0.75]} yt={[1.0, 1.05, 1.1]} xfmt={(v) => fmt(v, 2)} />
      <path d={P.path(Ex, 0, 0.999, 300)} fill="none" stroke={C.mut} strokeWidth="1" opacity="0.4" />
      <path d={P.path(Ex, 0, x, 200)} fill="none" stroke={C.blue} strokeWidth="2.4" />
      <circle cx={P.X(x)} cy={P.Y(clamp(E, 0.95, 1.14))} r="4.4" fill={C.red} />
      <g>
        <rect x="226" y="80" width="56" height="110" rx="6" fill="#8fa3b8" fillOpacity={0.15 + 0.5 * (zn - 1)} stroke={C.mut} />
        <rect x="296" y="80" width="56" height="110" rx="6" fill="#2f6db0" fillOpacity={0.05 + 0.55 * cu} stroke={C.mut} />
        <rect x="248" y="56" width="12" height="96" fill="#9aa0a6" />
        <rect x="318" y="56" width="12" height="96" fill="#c46a2b" />
        <path d="M 270 98 Q 289 70 308 98" fill="none" stroke={C.mut} strokeWidth="5" strokeLinecap="round" />
        <text x="254" y="204" textAnchor="middle" fontSize="9.5" fill={C.ink}>Zn²⁺ {fmt(zn, 2)}</text>
        <text x="324" y="204" textAnchor="middle" fontSize="9.5" fill={C.ink}>Cu²⁺ {fmt(cu, 2)}</text>
        <text x="289" y="40" textAnchor="middle" fontSize="11" fontWeight="800" fill={C.red}>{fmt(E, 3)} V</text>
        <text x="289" y="66" textAnchor="middle" fontSize="8.5" fill={C.mut}>염다리</text>
      </g>
    </Frame>
  );
}

/* ── 수소 원자: 에너지 준위와 선 스펙트럼 ── */
const SER = { lyman: { nf: 1, name: "라이먼 계열(자외선)" }, balmer: { nf: 2, name: "발머 계열(가시광)" }, paschen: { nf: 3, name: "파셴 계열(적외선)" } };
const lam = (nf, ni) => 1239.84 / (13.6 * (1 / (nf * nf) - 1 / (ni * ni)));
const wl2rgb = (w) => {
  let r = 0, g = 0, b = 0;
  if (w >= 380 && w < 440) { r = (440 - w) / 60; b = 1; } else if (w < 490) { g = (w - 440) / 50; b = 1; } else if (w < 510) { g = 1; b = (510 - w) / 20; } else if (w < 580) { r = (w - 510) / 70; g = 1; } else if (w < 645) { r = 1; g = (645 - w) / 65; } else if (w <= 750) { r = 1; }
  return `rgb(${Math.round(255 * r)}, ${Math.round(255 * g)}, ${Math.round(255 * b)})`;
};
export function HLines({ p = {} }) {
  const [s, setS] = useState(SER[p.series] ? p.series : "balmer");
  const nf = SER[s].nf;
  const clock = useClock({ period: 12, rest: 11 });
  const k = Math.min(4, Math.floor(clock.t / 2.2)), ni = nf + 1 + Math.min(3, k), ph = clamp((clock.t % 2.2) / 1.4, 0, 1);
  const shown = Array.from({ length: Math.min(4, k + (ph >= 1 ? 1 : 0)) }, (_, j) => nf + 1 + j);
  const Ey = (n) => 30 + 150 * (1 - (nf * nf) / (n * n));
  const lv = Array.from({ length: 6 }, (_, j) => nf + j);
  const lab = []; lv.forEach((n) => { const y = 210 - Ey(n); if (!lab.length || lab[lab.length - 1][1] - y >= 9) lab.push([n, y]); });
  const sx0 = 168, sx1 = 350, wmin = s === "lyman" ? 80 : s === "balmer" ? 380 : 800, wmax = s === "lyman" ? 130 : s === "balmer" ? 700 : 1900;
  const SX = (w) => sx0 + ((w - wmin) / (wmax - wmin)) * (sx1 - sx0);
  const cur = lam(nf, ni);
  return (
    <Frame clock={clock} title="수소 원자 — 에너지 준위와 선 스펙트럼"
      read={<>에너지 준위 Eₙ = −13.6 ÷ n² eV · 전자가 n = {ni} 에서 n = {nf} 로 내려오며 차이만큼의 빛을 낸다: λ = hc ÷ ΔE = <b>{fmt(cur, 1)} nm</b> · {SER[s].name} — 리드베리 식 1 ÷ λ = R(1 ÷ {nf}² − 1 ÷ n²) · 준위가 띄엄띄엄(양자화)하니 빛도 정해진 색의 선으로만 나온다 — 별빛의 선으로 별의 성분을 안다</>}
      controls={<Seg value={s} onChange={(v) => { setS(v); clock.reset(); }} options={[["lyman", "라이먼"], ["balmer", "발머"], ["paschen", "파셴"]]} />}>
      {lv.map((n) => <line key={n} x1="18" x2="150" y1={210 - Ey(n)} y2={210 - Ey(n)} stroke={n === nf ? C.ink : C.mut} strokeWidth={n === nf ? 1.6 : 1} />)}
      {lab.map(([n, y]) => <text key={"l" + n} x="14" y={y + 3.5} textAnchor="end" fontSize="9" fill={C.mut}>{n}</text>)}
      <text x="18" y="204" fontSize="8.5" fill={C.mut}>n = {nf} 위의 준위만(에너지 눈금 그대로)</text>
      <line x1="18" x2="150" y1={210 - 180} y2={210 - 180} stroke={C.mut} strokeDasharray="3 3" />
      <text x="152" y={210 - 180 + 3.5} fontSize="8.5" fill={C.mut}>∞</text>
      {shown.map((n, j) => <line key={n} x1={30 + 26 * j} x2={30 + 26 * j} y1={210 - Ey(n)} y2={210 - Ey(nf)} stroke={C.violet} strokeWidth="1" opacity="0.35" />)}
      {(() => { const xa = 30 + 26 * Math.min(3, k), y0 = 210 - Ey(ni), y1 = 210 - Ey(nf), y = y0 + (y1 - y0) * ph; return <g><line x1={xa} x2={xa} y1={y0} y2={y} stroke={C.red} strokeWidth="2" /><circle cx={xa} cy={y} r="4.2" fill={C.red} /></g>; })()}
      <rect x={sx0} y="150" width={sx1 - sx0} height="34" fill="#111" rx="3" />
      {s === "balmer" && Array.from({ length: 64 }, (_, j) => { const w = 380 + (j * 320) / 63; return <rect key={j} x={SX(w)} y="186" width={(sx1 - sx0) / 63 + 0.5} height="5" fill={wl2rgb(w)} />; })}
      {shown.map((n) => { const w = lam(nf, n); return <line key={n} x1={SX(w)} x2={SX(w)} y1="152" y2="182" stroke={s === "balmer" ? wl2rgb(w) : "#ddd"} strokeWidth="2.4" />; })}
      {shown.map((n, j) => { const w = lam(nf, n); return <text key={"t" + n} x={SX(w)} y={146 - (j % 2) * 10} textAnchor="middle" fontSize="8.5" fill={C.ink}>{fmt(w, 0)}</text>; })}
      <text x={sx0} y="204" fontSize="8.5" fill={C.mut}>{wmin} nm</text>
      <text x={sx1} y="204" textAnchor="end" fontSize="8.5" fill={C.mut}>{wmax} nm</text>
      <text x={(sx0 + sx1) / 2} y="30" textAnchor="middle" fontSize="10" fill={C.ink}>n = {ni} → {nf}</text>
      <text x={(sx0 + sx1) / 2} y="48" textAnchor="middle" fontSize="13" fontWeight="800" fill={s === "balmer" ? wl2rgb(cur) : C.red}>{fmt(cur, 1)} nm</text>
    </Frame>
  );
}
