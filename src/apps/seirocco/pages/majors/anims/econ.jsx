// 경제학 그림 — 수요와 공급(잉여) · 세금(사중손실 · 부담) · 탄력성과 총수입 · 효용 극대화(수요곡선) · 비용 곡선과 조업 · 독점 · 거미집 · 솔로 성장 · 케인스 승수 · 로렌츠 곡선
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, fmt, clamp, lerp, ease, useClock } from "./kit.jsx";

const fill = (P, pts) => P.poly(pts) + "Z";

/* ── 수요와 공급: 곡선이 옮겨 가면 균형이 움직인다 — 소비자 잉여 · 생산자 잉여 ── */
const MK = {
  base: { a: 10, c: 2 },
  dplus: { a: 13, c: 2, say: "수요 증가(소득 ↑ · 유행) → 값 ↑ · 거래량 ↑" },
  dminus: { a: 7.5, c: 2, say: "수요 감소(대체재 값 ↓ · 인기 ↓) → 값 ↓ · 거래량 ↓" },
  splus: { a: 10, c: -0.5, say: "공급 증가(기술 발전 · 원가 ↓) → 값 ↓ · 거래량 ↑" },
  sminus: { a: 10, c: 4.5, say: "공급 감소(원자재 값 ↑ · 흉작) → 값 ↑ · 거래량 ↓" },
};
export function Market({ p = {} }) {
  const [sh, setSh] = useState(MK[p.shift] ? p.shift : "dplus");
  const clock = useClock({ period: 9, rest: 6 });
  const B = MK.base, N = MK[sh];
  const s = ease(clamp((clock.t - 1.5) / 3, 0, 1));
  const a = lerp(B.a, N.a, s), c = lerp(B.c, N.c, s);
  const D = (q) => a - q, S = (q) => c + q;
  const q = (a - c) / 2, pr = a - q, q0 = (B.a - B.c) / 2, p0 = B.a - q0;
  const cs = 0.5 * q * (a - pr);
  const qz = Math.max(0, -c);
  const ps = pr * q - (c >= 0 ? c * q + (q * q) / 2 : c * (q - qz) + (q * q - qz * qz) / 2);
  const P = plot({ x0: 0, x1: 12, y0: 0, y1: 14, pad: [12, 14, 24, 32] });
  const psPts = c >= 0 ? [[0, c], [0, pr], [q, pr]] : [[0, 0], [0, pr], [q, pr], [qz, 0]];
  const xs = Math.min(11.2, 13 - c);
  return (
    <Frame clock={clock} title="수요와 공급"
      read={<>{N.say} · 균형 Q* = <b>{fmt(q, 2)}</b>, P* = <b>{fmt(pr, 2)}</b> (처음 {fmt(q0, 1)}, {fmt(p0, 1)}) · 소비자 잉여(파랑) {fmt(cs, 1)} = 낼 마음이 있던 값 − 낸 값 · 생산자 잉여(노랑) {fmt(ps, 1)} = 받은 값 − 받아도 됐던 값</>}
      controls={<Seg value={sh} onChange={(v) => { setSh(v); clock.reset(); }} options={[["dplus", "수요 ↑"], ["dminus", "수요 ↓"], ["splus", "공급 ↑"], ["sminus", "공급 ↓"]]} />}>
      <Axes p={P} xl="Q (양)" yl="P (값)" />
      <path d={fill(P, [[0, a], [0, pr], [q, pr]])} fill={C.blue} opacity="0.18" />
      <path d={fill(P, psPts)} fill={C.gold} opacity="0.22" />
      {s > 0 && <>
        <path d={P.path((x) => B.a - x, 0, B.a)} fill="none" stroke={C.mut} strokeWidth="1.1" strokeDasharray="4 3" opacity="0.7" />
        <path d={P.path((x) => B.c + x, Math.max(0, -B.c), 12)} fill="none" stroke={C.mut} strokeWidth="1.1" strokeDasharray="4 3" opacity="0.7" />
        <circle cx={P.X(q0)} cy={P.Y(p0)} r="4" fill="none" stroke={C.mut} strokeWidth="1.5" />
      </>}
      <path d={P.path(D, 0, Math.min(12, a))} fill="none" stroke={C.blue} strokeWidth="2.4" />
      <path d={P.path(S, qz, 12)} fill="none" stroke={C.gold} strokeWidth="2.4" />
      <line x1={P.X(0)} x2={P.X(q)} y1={P.Y(pr)} y2={P.Y(pr)} stroke={C.ink} strokeDasharray="3 3" />
      <line x1={P.X(q)} x2={P.X(q)} y1={P.Y(pr)} y2={P.Y(0)} stroke={C.ink} strokeDasharray="3 3" />
      <circle cx={P.X(q)} cy={P.Y(pr)} r="5" fill={C.red} />
      <Label x={P.X(0.4) + 6} y={P.Y(D(0.4)) + 2} size={11} color={C.blue} bold>D</Label>
      <Label x={P.X(xs) - 10} y={P.Y(S(xs)) + 2} size={11} color={C.gold} bold anchor="end">S</Label>
      {s > 0.95 && Math.abs(q - q0) > 0.2 && <Arrow x1={P.X(q0)} y1={P.Y(p0)} x2={P.X(q) + (q > q0 ? -6 : 6)} y2={P.Y(pr) + (pr > p0 ? 6 : -6)} color={C.red} w={1.3} head={5} />}
    </Frame>
  );
}

/* ── 세금: 사는 값과 파는 값 사이에 쐐기 — 세수(직사각형)와 사중손실(삼각형), 부담은 기울기가 나눈다 ── */
export function Tax({ p = {} }) {
  const [tax, setTax] = useState(p.t ?? 3);
  const [b, setB] = useState(p.b ?? 1);
  const clock = useClock({ period: 8, rest: 5 });
  const a = 10, c = 1, d = 1;
  const tt = tax * ease(clamp(clock.t / 3, 0, 1));
  const q0 = (a - c) / (b + d), p0 = a - b * q0;
  const qt = Math.max(0, (a - c - tt) / (b + d)), pb = a - b * qt, ps = pb - tt;
  const rev = tt * qt, dwl = 0.5 * tt * (q0 - qt), share = b / (b + d);
  const P = plot({ x0: 0, x1: 10, y0: 0, y1: 12, pad: [12, 14, 24, 32] });
  return (
    <Frame clock={clock} title="세금과 사중손실"
      read={<>물건 하나에 세금 t = <b>{fmt(tt, 2)}</b>: 거래량 {fmt(q0, 2)} → {fmt(qt, 2)} · 사는 사람이 내는 값 Pb = <b>{fmt(pb, 2)}</b>, 파는 사람이 받는 값 Ps = <b>{fmt(ps, 2)}</b> · 세수(초록) = t × Q = {fmt(rev, 2)} · 사중손실(빨강) = ½ t ΔQ = <b>{fmt(dwl, 2)}</b> — 아무도 갖지 못하고 사라진 잉여 · 부담: 사는 사람 {fmt(share * 100, 0)} %, 파는 사람 {fmt(100 - share * 100, 0)} % — 덜 탄력적인(가파른) 쪽이 더 진다</>}
      controls={<>
        <Slider label="세금 t" min={0} max={6} step={0.5} value={tax} onChange={(v) => { setTax(v); clock.reset(); }} />
        <Slider label="수요 기울기" min={0.3} max={3} step={0.1} value={b} onChange={setB} />
      </>}>
      <Axes p={P} xl="Q" yl="P" />
      <path d={fill(P, [[0, ps], [0, pb], [qt, pb], [qt, ps]])} fill={C.green} opacity="0.22" />
      <path d={fill(P, [[qt, pb], [qt, ps], [q0, p0]])} fill={C.red} opacity="0.35" />
      <path d={P.path((x) => a - b * x, 0, a / b)} fill="none" stroke={C.blue} strokeWidth="2.3" />
      <path d={P.path((x) => c + d * x, 0, 10)} fill="none" stroke={C.gold} strokeWidth="2.3" />
      {tt > 0.05 && <path d={P.path((x) => c + tt + d * x, 0, 10)} fill="none" stroke={C.red} strokeWidth="1.5" strokeDasharray="5 3" />}
      <line x1={P.X(0)} x2={P.X(qt)} y1={P.Y(pb)} y2={P.Y(pb)} stroke={C.ink} strokeDasharray="3 3" />
      <line x1={P.X(0)} x2={P.X(qt)} y1={P.Y(ps)} y2={P.Y(ps)} stroke={C.ink} strokeDasharray="3 3" />
      <line x1={P.X(qt)} x2={P.X(qt)} y1={P.Y(pb)} y2={P.Y(0)} stroke={C.ink} strokeDasharray="3 3" />
      <circle cx={P.X(q0)} cy={P.Y(p0)} r="3.5" fill="none" stroke={C.mut} strokeWidth="1.5" />
      <circle cx={P.X(qt)} cy={P.Y(pb)} r="4" fill={C.blue} />
      <circle cx={P.X(qt)} cy={P.Y(ps)} r="4" fill={C.gold} />
      <Label x={P.X(0) + 4} y={P.Y(pb) - 4} size={10} color={C.blue} bg>Pb</Label>
      <Label x={P.X(0) + 4} y={P.Y(ps) + 13} size={10} color={C.gold} bg>Ps</Label>
      {tt > 0.4 && <Label x={P.X(clamp((11 - c - tt) / d, 0.5, 9.3)) + 6} y={P.Y(c + tt + d * clamp((11 - c - tt) / d, 0.5, 9.3)) + 12} size={10} color={C.red} bg>공급 + 세금</Label>}
    </Frame>
  );
}

/* ── 탄력성과 총수입: 직선 수요 위를 움직이면 |e| 가 바뀐다 — 가운데에서 총수입 최대 ── */
export function Elastic({ p = {} }) {
  const [mode, setMode] = useState(p.mode === "unit" ? "unit" : "lin");
  const clock = useClock({ period: 10 });
  const u = 0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10);
  const lin = mode === "lin";
  const q = lin ? 0.6 + 8.8 * u : 2 + 8 * u;
  const Pf = (x) => (lin ? 10 - x : 20 / x);
  const pr = Pf(q), tr = pr * q, e = lin ? pr / q : 1;
  const P = plot({ x0: 0, x1: 11, y0: 0, y1: 11, pad: [12, 142, 24, 30] });
  const R = plot({ x0: 0, x1: 11, y0: 0, y1: 30, pad: [24, 10, 24, 246] });
  return (
    <Frame clock={clock} title="탄력성과 총수입"
      read={lin
        ? <>Q = {fmt(q, 2)}, P = {fmt(pr, 2)}: |e| = (P/Q) × (1/기울기) = <b>{fmt(e, 2)}</b> {e > 1.02 ? "> 1 탄력적 — 값을 내리면 판매가 더 크게 늘어 총수입 ↑" : e < 0.98 ? "< 1 비탄력적 — 값을 올려도 판매가 조금만 줄어 총수입 ↑" : "≈ 1 — 총수입이 가장 크다"} · 총수입 P × Q = <b>{fmt(tr, 1)}</b>(색 사각형, 오른쪽 그래프) — 직선 위 가운데(|e| = 1)에서 최대 · 같은 직선이라도 위쪽은 탄력적, 아래쪽은 비탄력적</>
        : <>P = 20/Q — 어디서나 |e| = 1: 값을 1 % 내리면 판매가 1 % 늘어 총수입은 늘 <b>20</b> 으로 같다(사각형 넓이가 그대로) · 지금 Q = {fmt(q, 2)}, P = {fmt(pr, 2)}</>}
      controls={<Seg value={mode} onChange={setMode} options={[["lin", "직선 수요"], ["unit", "단위탄력 P = 20/Q"]]} />}>
      <Axes p={P} xl="Q" yl="P" />
      <rect x={P.X(0)} y={P.Y(pr)} width={P.X(q) - P.X(0)} height={P.Y(0) - P.Y(pr)} fill={C.sp} opacity="0.2" />
      {lin
        ? <>
          <path d={P.path((x) => 10 - x, 0, 5)} fill="none" stroke={C.green} strokeWidth="2.6" />
          <path d={P.path((x) => 10 - x, 5, 10)} fill="none" stroke={C.red} strokeWidth="2.6" />
          <circle cx={P.X(5)} cy={P.Y(5)} r="3" fill={C.ink} />
          <Label x={P.X(5) + 6} y={P.Y(5) - 4} size={9.5} color={C.ink} bg>|e| = 1</Label>
          <Label x={P.X(1.2) + 8} y={P.Y(8.8) - 6} size={9.5} color={C.green} bg>탄력적</Label>
          <Label x={P.X(7.4) + 4} y={P.Y(2.6) - 8} size={9.5} color={C.red} bg>비탄력적</Label>
        </>
        : <path d={P.path((x) => 20 / x, 1.85, 11)} fill="none" stroke={C.sp} strokeWidth="2.6" />}
      <circle cx={P.X(q)} cy={P.Y(pr)} r="5" fill={C.ink} />
      <Axes p={R} xl="Q" yl="총수입" grid={false} yt={[10, 20, 30]} xt={[5, 10]} />
      <path d={R.path((x) => (lin ? x * (10 - x) : 20), lin ? 0 : 2, lin ? 10 : 10)} fill="none" stroke={C.sp} strokeWidth="2" />
      <circle cx={R.X(q)} cy={R.Y(tr)} r="4" fill={C.red} />
    </Frame>
  );
}

/* ── 효용 극대화: 예산선과 무차별곡선의 접점 — 값이 바뀌면 그 자취가 수요곡선 ── */
export function Utility({ p = {} }) {
  const [al, setAl] = useState(p.alpha ?? 0.5);
  const clock = useClock({ period: 12 });
  const M = 12, py = 1;
  const px = 0.6 * Math.pow(4, 0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 12));
  const xs = (al * M) / px, ys = ((1 - al) * M) / py, U = Math.pow(xs, al) * Math.pow(ys, 1 - al);
  const ic = (u) => (x) => Math.pow(u / Math.pow(x, al), 1 / (1 - al));
  const P = plot({ x0: 0, x1: 21, y0: 0, y1: 14, pad: [12, 128, 24, 28] });
  const Dm = plot({ x0: 0, x1: 16, y0: 0, y1: 2.6, pad: [24, 10, 24, 258] });
  return (
    <Frame clock={clock} title="효용 극대화와 수요곡선"
      read={<>x 의 값 px = <b>{fmt(px, 2)}</b> (y 의 값 1, 소득 12): 예산선이 무차별곡선에 닿는 점 — 기울기가 같다(MRS = px/py) → x* = αM/px = <b>{fmt(xs, 2)}</b>, y* = (1 − α)M/py = <b>{fmt(ys, 2)}</b> · 값이 오르면 예산선이 안쪽으로 돌고 x 가 준다 — 그 자취가 오른쪽 수요곡선 · 코브-더글러스는 소득의 α = {fmt(al * 100, 0)} % 를 늘 x 에 쓴다</>}
      controls={<Slider label="α (x 몫)" min={0.2} max={0.8} step={0.05} value={al} onChange={setAl} />}>
      <Axes p={P} xl="x" yl="y" />
      {[0.6, 1.45].map((k) => <path key={k} d={P.path(ic(U * k), 0.05, 21, 240)} fill="none" stroke={C.mut} strokeWidth="1" opacity="0.6" />)}
      <path d={P.path(ic(U), 0.05, 21, 240)} fill="none" stroke={C.violet} strokeWidth="2" />
      <path d={P.path((x) => (M - px * x) / py, 0, M / px)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <line x1={P.X(xs)} x2={P.X(xs)} y1={P.Y(ys)} y2={P.Y(0)} stroke={C.ink} strokeDasharray="3 3" />
      <circle cx={P.X(xs)} cy={P.Y(ys)} r="5" fill={C.red} />
      <Label x={P.X(xs) + 7} y={P.Y(ys) - 6} size={10} color={C.red} bg>최적</Label>
      <Label x={P.X(Math.min(19.5, M / px)) - 2} y={P.Y(0) - 6} size={9.5} color={C.sp} anchor="end" bg>예산선</Label>
      <Axes p={Dm} xl="x" yl="px" grid={false} xt={[5, 10, 15]} yt={[1, 2]} />
      <path d={Dm.path((x) => (al * M) / x, (al * M) / 2.55, 16)} fill="none" stroke={C.sp} strokeWidth="2" />
      <circle cx={Dm.X(xs)} cy={Dm.Y(px)} r="4" fill={C.red} />
      <text x={Dm.r} y={Dm.t - 8} textAnchor="end" fontSize="9.5" fill={C.mut}>수요곡선</text>
    </Frame>
  );
}

/* ── 비용 곡선과 이윤: P = MC 로 생산량, AVC 바닥 아래면 문을 닫는다 ── */
const VC = (q) => (q * q * q) / 3 - 4 * q * q + 20 * q;
const MCf = (q) => q * q - 8 * q + 20;
const AVC = (q) => (q * q) / 3 - 4 * q + 20;
export function Costs({ p = {} }) {
  const [F, setF] = useState(p.F ?? 18);
  const clock = useClock({ period: 12 });
  const Pr = 5 + 15 * (0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 12));
  const ATC = (q) => AVC(q) + F / q;
  const be = useMemo(() => { let m = Infinity; for (let q = 0.5; q <= 12; q += 0.01) m = Math.min(m, AVC(q) + F / q); return m; }, [F]);
  const q = Pr >= 8 ? 4 + Math.sqrt(Pr - 4) : 0;
  const prof = q > 0 ? Pr * q - VC(q) - F : -F;
  const P = plot({ x0: 0, x1: 10, y0: 0, y1: 30, pad: [12, 14, 24, 30] });
  const at = q > 0 ? ATC(q) : 0;
  return (
    <Frame clock={clock} title="비용 곡선과 이윤 극대화"
      read={<>값 P = <b>{fmt(Pr, 1)}</b>: {q > 0
        ? <>P = MC 인 q = <b>{fmt(q, 2)}</b> — 이윤 (P − ATC) × q = <b>{fmt(prof, 1)}</b>{prof < 0 ? " (손실이지만 값이 AVC 보다 높아 만드는 쪽이 덜 손해)" : ""}</>
        : <>AVC 바닥(8)보다 싸서 <b>문을 닫는다</b>(q = 0, 손실 = 고정비 {F})</>} · 손익분기 값 = ATC 바닥 {fmt(be, 2)}, 조업중단 값 = AVC 바닥 8 — 기업의 공급곡선은 MC 의 AVC 위쪽 부분</>}
      controls={<Slider label="고정비 F" min={0} max={40} step={2} value={F} onChange={setF} />}>
      <Axes p={P} xl="q" yl="원" />
      {q > 0 && <rect x={P.X(0)} y={P.Y(Math.max(Pr, at))} width={P.X(q) - P.X(0)} height={Math.abs(P.Y(at) - P.Y(Pr))} fill={prof >= 0 ? C.green : C.red} opacity="0.25" />}
      <path d={P.path(MCf, 0.3, 9.8)} fill="none" stroke={C.red} strokeWidth="2.3" />
      <path d={P.path(ATC, 0.75, 9.8)} fill="none" stroke={C.blue} strokeWidth="2.3" />
      <path d={P.path(AVC, 0.3, 9.8)} fill="none" stroke={C.gold} strokeWidth="1.8" strokeDasharray="5 3" />
      <line x1={P.X(0)} x2={P.X(10)} y1={P.Y(Pr)} y2={P.Y(Pr)} stroke={C.green} strokeWidth="1.6" />
      {q > 0 && <line x1={P.X(q)} x2={P.X(q)} y1={P.Y(Pr)} y2={P.Y(0)} stroke={C.ink} strokeDasharray="3 3" />}
      {q > 0 && <circle cx={P.X(q)} cy={P.Y(Pr)} r="5" fill={C.ink} />}
      <Label x={P.X(9.7)} y={P.Y(MCf(9.7)) - 4} size={10} color={C.red} anchor="end" bg>MC</Label>
      <Label x={P.X(9.7)} y={P.Y(ATC(9.7)) + 14} size={10} color={C.blue} anchor="end" bg>ATC</Label>
      <Label x={P.X(2)} y={P.Y(AVC(2)) + 15} size={10} color={C.gold} bg>AVC</Label>
      <Label x={P.X(0) + 4} y={P.Y(Pr) - 4} size={10} color={C.green} bg>P</Label>
    </Frame>
  );
}

/* ── 독점: MR = MC 에서 생산, 값은 수요곡선에서 — 경쟁과 비교한 사중손실 ── */
export function Monopoly({ p = {} }) {
  const [c, setC] = useState(p.mc ?? 2);
  const clock = useClock({ period: 10 });
  const a = 12, Qm = (a - c) / 2, Pm = (a + c) / 2, Qc = a - c;
  const prof = (Pm - c) * Qm, dwl = 0.5 * (Pm - c) * (Qc - Qm), lerner = (Pm - c) / Pm;
  const qt = (a - c) * (0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10));
  const pi = (q) => (a - q - c) * q;
  const P = plot({ x0: 0, x1: 13, y0: 0, y1: 13, pad: [12, 124, 24, 28] });
  const R = plot({ x0: 0, x1: 13, y0: 0, y1: 40, pad: [24, 10, 24, 262] });
  return (
    <Frame clock={clock} title="독점"
      read={<>독점 기업은 MR = MC 인 Q = <b>{fmt(Qm, 2)}</b> 를 만들고, 값은 수요곡선에서 P = <b>{fmt(Pm, 2)}</b> · 경쟁이라면 P = MC = {fmt(c, 1)} 에서 Q = {fmt(Qc, 1)} · 독점 이윤(초록) {fmt(prof, 1)} · 사중손실(빨강) <b>{fmt(dwl, 1)}</b> · 러너 지수 (P − MC)/P = {fmt(lerner, 2)} = 1/|e| · 오른쪽 = 생산량을 바꿔 보며 잰 이윤 — 꼭대기가 MR = MC</>}
      controls={<Slider label="한계비용 MC" min={0} max={8} step={0.5} value={c} onChange={setC} />}>
      <Axes p={P} xl="Q" yl="P" />
      <path d={fill(P, [[0, c], [0, Pm], [Qm, Pm], [Qm, c]])} fill={C.green} opacity="0.2" />
      <path d={fill(P, [[Qm, Pm], [Qm, c], [Qc, c]])} fill={C.red} opacity="0.32" />
      <path d={P.path((x) => a - x, 0, 12)} fill="none" stroke={C.blue} strokeWidth="2.3" />
      <path d={P.path((x) => a - 2 * x, 0, 6)} fill="none" stroke={C.violet} strokeWidth="1.8" strokeDasharray="5 3" />
      <line x1={P.X(0)} x2={P.X(13)} y1={P.Y(c)} y2={P.Y(c)} stroke={C.red} strokeWidth="2" />
      <line x1={P.X(Qm)} x2={P.X(Qm)} y1={P.Y(Pm)} y2={P.Y(0)} stroke={C.ink} strokeDasharray="3 3" />
      <line x1={P.X(qt)} x2={P.X(qt)} y1={P.Y(13)} y2={P.Y(0)} stroke={C.mut} strokeWidth="0.8" opacity="0.7" />
      <circle cx={P.X(Qm)} cy={P.Y(Pm)} r="5" fill={C.ink} />
      <circle cx={P.X(Qc)} cy={P.Y(c)} r="4" fill="none" stroke={C.ink} strokeWidth="1.6" />
      <Label x={P.X(1)} y={P.Y(11) - 4} size={10} color={C.blue} bg>D</Label>
      <Label x={P.X(4.6) + 5} y={P.Y(a - 9.2) + 2} size={10} color={C.violet} bg>MR</Label>
      <Label x={P.X(12.8)} y={P.Y(c) - 5} size={10} color={C.red} anchor="end" bg>MC</Label>
      <Axes p={R} xl="Q" yl="이윤" grid={false} xt={[6, 12]} yt={[20, 40]} />
      <path d={R.path((x) => Math.max(0, pi(x)), 0, a - c)} fill="none" stroke={C.green} strokeWidth="2" />
      <circle cx={R.X(qt)} cy={R.Y(Math.max(0, pi(qt)))} r="4" fill={C.red} />
      <line x1={R.X(Qm)} x2={R.X(Qm)} y1={R.Y(prof)} y2={R.Y(0)} stroke={C.ink} strokeDasharray="2 3" />
    </Frame>
  );
}

/* ── 거미집 모형: 작년 값을 보고 올해 생산 — 기울기 비가 1 보다 작으면 모이고, 크면 벌어진다 ── */
export function Cobweb({ p = {} }) {
  const [b, setB] = useState(p.b ?? 0.8);
  const clock = useClock({ period: 12, rest: 11 });
  const a = 10, c = 1;
  const qs = (a - c) / (b + 1), ps = a - b * qs;
  const path = useMemo(() => {
    const pts = []; let pr = ps + 2.4;
    const ser = [pr];
    for (let k = 0; k < 12; k++) { const q = pr - c; const np = a - b * q; pts.push([q, pr], [q, np]); pr = np; ser.push(pr); }
    return { pts, ser };
  }, [b]); // eslint-disable-line react-hooks/exhaustive-deps
  const k = Math.min(12, Math.floor(clock.t / 0.85));
  const P = plot({ x0: 0, x1: 10, y0: 0, y1: 12, pad: [12, 136, 24, 28] });
  const T = plot({ x0: 0, x1: 12, y0: 0, y1: 12, pad: [24, 10, 24, 252] });
  const cl = (y) => clamp(y, -1, 13);
  const shown = path.pts.slice(0, 2 * k + 1).map(([q, y]) => [clamp(q, -1, 11), cl(y)]);
  return (
    <Frame clock={clock} title="거미집 모형"
      read={<>농부는 작년 값을 보고 올해 심고(공급), 올해 값은 그 양을 다 팔 수 있는 값(수요)으로 정해진다 · 기울기 비 b/d = <b>{fmt(b, 2)}</b> {b < 0.99 ? "< 1 → 출렁임이 줄어 균형으로(안정)" : b > 1.01 ? "> 1 → 출렁임이 점점 커진다(불안정)" : "= 1 → 같은 폭으로 끝없이 출렁"} · 값과 균형의 차이가 해마다 −b/d 배: Pₜ − P* = (−b/d)(Pₜ₋₁ − P*) — 1 계 차분방정식 · 오른쪽 = 해마다의 값</>}
      controls={<Slider label="수요 기울기 b (공급 d = 1)" min={0.5} max={1.4} step={0.05} value={b} onChange={(v) => { setB(v); clock.reset(); }} />}>
      <Axes p={P} xl="Q" yl="P" />
      <path d={P.path((x) => a - b * x, 0, 10)} fill="none" stroke={C.blue} strokeWidth="2" />
      <path d={P.path((x) => c + x, 0, 10)} fill="none" stroke={C.gold} strokeWidth="2" />
      <path d={P.poly(shown)} fill="none" stroke={C.red} strokeWidth="1.6" />
      <circle cx={P.X(qs)} cy={P.Y(ps)} r="3.5" fill={C.ink} />
      <Label x={P.X(9.6)} y={P.Y(a - b * 9.6) - 4} size={10} color={C.blue} anchor="end" bg>수요</Label>
      <Label x={P.X(9.6)} y={P.Y(c + 9.6) + 14} size={10} color={C.gold} anchor="end" bg>공급</Label>
      <Axes p={T} xl="해" yl="값" grid={false} xt={[4, 8, 12]} yt={[5, 10]} />
      <line x1={T.l} x2={T.r} y1={T.Y(ps)} y2={T.Y(ps)} stroke={C.mut} strokeDasharray="3 3" />
      <path d={T.poly(path.ser.slice(0, k + 1).map((y, i) => [i, cl(y)]))} fill="none" stroke={C.red} strokeWidth="1.6" />
      {path.ser.slice(0, k + 1).map((y, i) => <circle key={i} cx={T.X(i)} cy={T.Y(cl(y))} r="2.4" fill={C.red} />)}
    </Frame>
  );
}

/* ── 솔로 성장 모형: 투자 s f(k) 와 깎임 (n + δ)k 가 같아지는 곳으로 모인다 ── */
export function Solow({ p = {} }) {
  const [s, setS] = useState(p.s ?? 0.3);
  const clock = useClock({ period: 12, rest: 11 });
  const al = 0.33, nd = 0.08, f = (k) => Math.pow(k, al);
  const ks = Math.pow(s / nd, 1 / (1 - al));
  const sim = useMemo(() => {
    const out = []; let k = 1;
    for (let i = 0; i <= 1600; i++) { out.push(k); k += 0.05 * (s * f(k) - nd * k); }
    return out;
  }, [s]); // eslint-disable-line react-hooks/exhaustive-deps
  const tau = clamp(clock.t / 10, 0, 1) * 80, i = Math.min(1600, Math.round(tau / 0.05)), k = sim[i];
  const ys = f(ks), cs = (1 - s) * ys;
  const P = plot({ x0: 0, x1: 24, y0: 0, y1: 3.2, pad: [12, 120, 24, 30] });
  const T = plot({ x0: 0, x1: 80, y0: 0, y1: 3, pad: [24, 10, 24, 266] });
  return (
    <Frame clock={clock} title="솔로 성장 모형"
      read={<>저축률 s = <b>{fmt(s, 2)}</b>: 1 인당 자본 k 는 투자 s f(k)(파랑)가 깎임 (n + δ)k(빨강)보다 크면 늘고 작으면 준다 → k* = (s/(n + δ))<sup>1/(1 − α)</sup> = <b>{fmt(ks, 2)}</b> 로 모인다 · 지금 k = {fmt(k, 2)} · 정상상태 소득 y* = {fmt(ys, 2)}, 소비 (1 − s)y* = {fmt(cs, 2)} — 저축률을 올리면 소득은 늘지만 소비는 황금률 s = α = 0.33 에서 가장 크다</>}
      controls={<Slider label="저축률 s" min={0.1} max={0.6} step={0.02} value={s} onChange={(v) => { setS(v); clock.reset(); }} />}>
      <Axes p={P} xl="k" yl="y" />
      <path d={P.path(f, 0, 24)} fill="none" stroke={C.mut} strokeWidth="1.3" />
      <path d={P.path((x) => s * f(x), 0, 24)} fill="none" stroke={C.blue} strokeWidth="2.3" />
      <path d={P.path((x) => nd * x, 0, 24)} fill="none" stroke={C.red} strokeWidth="2" />
      <line x1={P.X(ks)} x2={P.X(ks)} y1={P.Y(s * f(ks))} y2={P.Y(0)} stroke={C.ink} strokeDasharray="3 3" />
      <line x1={P.X(k)} x2={P.X(k)} y1={P.Y(s * f(k))} y2={P.Y(nd * k)} stroke={C.green} strokeWidth="3" />
      <circle cx={P.X(k)} cy={P.Y(0)} r="5" fill={C.green} />
      {Math.abs(ks - k) > 0.3 && <Arrow x1={P.X(k)} y1={P.Y(0) - 10} x2={P.X(k) + (ks > k ? 16 : -16)} y2={P.Y(0) - 10} color={C.green} w={1.6} head={5} />}
      <Label x={P.X(22)} y={P.Y(f(22)) - 4} size={9.5} color={C.mut} anchor="end" bg>f(k)</Label>
      <Label x={P.X(22)} y={P.Y(s * f(22)) + 13} size={9.5} color={C.blue} anchor="end" bg>s f(k)</Label>
      <Label x={P.X(Math.min(22, 2.9 / nd))} y={P.Y(Math.min(2.9, nd * 22)) - 4} size={9.5} color={C.red} anchor="end" bg>(n + δ)k</Label>
      <Axes p={T} xl="시간" yl="y" grid={false} xt={[40, 80]} yt={[1, 2, 3]} />
      <line x1={T.l} x2={T.r} y1={T.Y(ys)} y2={T.Y(ys)} stroke={C.mut} strokeDasharray="3 3" />
      <path d={T.poly(sim.slice(0, i + 1).filter((_, j) => j % 10 === 0 || j === i).map((kk, j, arr) => [j === arr.length - 1 ? tau : j * 0.5, f(kk)]))} fill="none" stroke={C.sp} strokeWidth="2" />
    </Frame>
  );
}

/* ── 케인스 승수: 지출이 늘면 소득이 늘고, 늘어난 소득이 다시 지출 — 1/(1 − c) 배 ── */
export function Keynes({ p = {} }) {
  const [c, setC] = useState(p.c ?? 0.75);
  const clock = useClock({ period: 13, rest: 12.5 });
  const A0 = 80, dG = 20, Y0 = A0 / (1 - c), Y1 = (A0 + dG) / (1 - c);
  const sh = ease(clamp((clock.t - 1.5) / 1, 0, 1));
  const AE = (y) => A0 + dG * sh + c * y;
  const k = clock.t < 2.6 ? -1 : Math.min(14, Math.floor((clock.t - 2.6) / 0.65));
  const stairs = useMemo(() => {
    const pts = [[Y0, Y0]]; let y = Y0;
    for (let j = 0; j < 15; j++) { const ae = A0 + dG + c * y; pts.push([y, ae], [ae, ae]); y = ae; }
    return pts;
  }, [c]); // eslint-disable-line react-hooks/exhaustive-deps
  const cum = k < 0 ? 0 : (dG * (1 - Math.pow(c, k + 1))) / (1 - c);
  const P = plot({ x0: 0, x1: 560, y0: 0, y1: 560, pad: [12, 14, 24, 34] });
  return (
    <Frame clock={clock} title="케인스 승수"
      read={<>한계소비성향 c = <b>{fmt(c, 2)}</b> → 승수 1/(1 − c) = <b>{fmt(1 / (1 - c), 2)}</b> · 정부지출이 20 늘면 그 20 이 누군가의 소득이 되고, 그중 c 만큼 다시 쓰이고 … → 소득 {fmt(Y0, 0)} → {fmt(Y1, 0)} (+{fmt(Y1 - Y0, 0)}) · {k < 0 ? "지출선이 위로 옮겨 간다" : <>지금 {k + 1} 번째 돌림까지: 20 + 20c + 20c² + … = <b>{fmt(cum, 1)}</b></>} · 45° 선 = 생산(소득)이 지출과 같은 곳</>}
      controls={<Slider label="한계소비성향 c" min={0.5} max={0.8} step={0.05} value={c} onChange={(v) => { setC(v); clock.reset(); }} />}>
      <Axes p={P} xl="소득 Y" yl="지출" xt={[100, 200, 300, 400, 500]} yt={[100, 200, 300, 400, 500]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v, 0)} />
      <path d={P.path((y) => y, 0, 560)} fill="none" stroke={C.ink} strokeWidth="1.4" />
      {sh > 0 && <path d={P.path((y) => A0 + c * y, 0, 560)} fill="none" stroke={C.mut} strokeWidth="1.2" strokeDasharray="4 3" />}
      <path d={P.path(AE, 0, 560)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      {k >= 0 && <path d={P.poly(stairs.slice(0, 2 * k + 3))} fill="none" stroke={C.red} strokeWidth="1.6" />}
      <circle cx={P.X(Y0)} cy={P.Y(Y0)} r="4" fill={C.ink} />
      {k >= 0 && <circle cx={P.X(Y1)} cy={P.Y(Y1)} r="4" fill="none" stroke={C.red} strokeWidth="1.6" />}
      <Label x={P.X(520)} y={P.Y(520) - 6} size={10} color={C.ink} anchor="end" bg>45°</Label>
      <Label x={P.X(40)} y={P.Y(AE(40)) - 6} size={10} color={C.sp} bg>지출 = C + I + G</Label>
    </Frame>
  );
}

/* ── 로렌츠 곡선과 지니 계수: 대각선(완전 평등)에서 멀수록 불평등 ── */
export function Lorenz({ p = {} }) {
  const [k, setK] = useState(p.k ?? 3);
  const clock = useClock({ period: 10 });
  const L = (x) => Math.pow(x, k), G = (k - 1) / (k + 1);
  const pp = 0.05 + 0.9 * (0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10));
  const dec = Array.from({ length: 10 }, (_, i) => (L((i + 1) / 10) - L(i / 10)) * 100);
  const P = plot({ x0: 0, x1: 1, y0: 0, y1: 1, pad: [12, 150, 24, 32] });
  const B = plot({ x0: 0.5, x1: 10.5, y0: 0, y1: Math.max(40, dec[9] * 1.1), pad: [24, 10, 24, 240] });
  const pc = (x) => fmt(x * 100, 0) + " %";
  return (
    <Frame clock={clock} title="로렌츠 곡선과 지니 계수"
      read={<>사람을 소득 순서로 세워 아래부터 모은 소득의 몫 — 하위 <b>{pc(pp)}</b> 가 전체 소득의 <b>{pc(L(pp))}</b> 를 가진다 · 지니 계수 = 2 × (대각선과 곡선 사이 넓이) = (k − 1)/(k + 1) = <b>{fmt(G, 2)}</b> (0 = 완전 평등, 1 = 한 사람이 다 가짐) · 맨 위 10 % 의 몫 {fmt(dec[9], 1)} %, 맨 아래 10 % 의 몫 {fmt(dec[0], 2)} % (오른쪽 = 10 분위 몫)</>}
      controls={<Slider label="불평등 k (L = pᵏ)" min={1} max={6} step={0.25} value={k} onChange={setK} />}>
      <Axes p={P} xl="사람 몫" yl="소득 몫" xt={[0.5, 1]} yt={[0.5, 1]} />
      <path d={P.poly([[0, 0], [1, 1]]) + P.path(L, 1, 0, 120).replace(/^M/, "L") + "Z"} fill={C.sp} opacity="0.18" />
      <path d={P.poly([[0, 0], [1, 1]])} fill="none" stroke={C.ink} strokeWidth="1.3" strokeDasharray="4 3" />
      <path d={P.path(L, 0, 1)} fill="none" stroke={C.sp} strokeWidth="2.5" />
      <line x1={P.X(pp)} x2={P.X(pp)} y1={P.Y(L(pp))} y2={P.Y(0)} stroke={C.mut} strokeDasharray="2 3" />
      <line x1={P.X(0)} x2={P.X(pp)} y1={P.Y(L(pp))} y2={P.Y(L(pp))} stroke={C.mut} strokeDasharray="2 3" />
      <circle cx={P.X(pp)} cy={P.Y(L(pp))} r="5" fill={C.red} />
      <Label x={P.X(0.46)} y={P.Y(0.6)} size={9.5} color={C.ink} anchor="end" bg>완전 평등</Label>
      <Axes p={B} xl="" yl="%" grid={false} xt={[1, 5, 10]} yt={[10, 20, 30]} xfmt={(v) => fmt(v, 0)} />
      <text x={(B.l + B.r) / 2} y={B.b + 22} textAnchor="middle" fontSize="9" fill={C.mut}>10 분위(아래 → 위)</text>
      {dec.map((v, i) => <rect key={i} x={B.X(i + 0.62)} y={B.Y(v)} width={B.X(i + 1.38) - B.X(i + 0.62)} height={B.Y(0) - B.Y(v)} fill={i === Math.min(9, Math.floor(pp * 10)) ? C.red : C.sp} opacity="0.75" />)}
    </Frame>
  );
}
