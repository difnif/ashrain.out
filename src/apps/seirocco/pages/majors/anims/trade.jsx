// 무역 그림 — 비교우위(리카도) · 볼록한 생산가능곡선과 무역 삼각형(립친스키) · 관세의 후생 · 이자율 평형 · 인코텀즈(위험과 비용이 넘어가는 곳)
import { useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, lerp, ease, useClock } from "./kit.jsx";

const fill = (P, pts) => P.poly(pts) + "Z";

/* ── 비교우위: 기회비용이 다르면 둘 다 이익 — 특화하고 교역하면 생산가능선 밖에서 소비 ── */
export function Comparative({ p = {} }) {
  const [tt, setTt] = useState(p.p ?? 1.6);
  const clock = useClock({ period: 10, rest: 9 });
  const ok = tt > 4 / 3 + 1e-9 && tt < 2 - 1e-9;
  const s = ease(clamp((clock.t - 1.5) / 2, 0, 1)), m = ease(clamp((clock.t - 4) / 3, 0, 1));
  // 한국: 노동 120, 옷감 1 시간, 와인 2 시간 · 외국: 옷감 3 시간, 와인 4 시간
  const H = plot({ x0: 0, x1: 80, y0: 0, y1: 130, pad: [24, 194, 24, 34] });
  const F = plot({ x0: 0, x1: 36, y0: 0, y1: 60, pad: [24, 12, 24, 214] });
  const hAut = [20, 80], fAut = [15, 20];
  const hPro = ok ? [lerp(20, 0, s), lerp(80, 120, s)] : hAut, fPro = ok ? [lerp(15, 30, s), lerp(20, 0, s)] : fAut;
  const W = 18 * m;
  const hCon = ok ? [W, 120 - tt * W] : hAut, fCon = ok ? [30 - W, tt * W] : fAut;
  return (
    <Frame clock={clock} title="비교우위"
      read={<>와인 1 = 옷감 <b>{fmt(tt, 2)}</b> 로 바꾼다면 · 와인 1 의 기회비용: 한국 옷감 2, 외국 옷감 4/3 → 한국은 옷감, 외국은 와인에 비교우위 · {ok
        ? <>4/3 &lt; {fmt(tt, 2)} &lt; 2 라 둘 다 이익 — 각자 잘하는 것만 만들고(특화) 바꾸면, 무역선(점선)이 생산가능선 밖이라 혼자서는 못 가는 곳에서 소비한다 · 외국은 둘 다 더 못 만들어도(절대열위) 이익</>
        : <>이 교역조건은 한 나라의 기회비용 바깥 — 그 나라는 혼자 만드는 편이 나아 교역이 일어나지 않는다(교역조건은 두 기회비용 사이)</>}</>}
      controls={<Slider label="교역조건 (와인 1 = 옷감)" min={1} max={2.4} step={0.05} value={tt} onChange={(v) => { setTt(v); clock.reset(); }} />}>
      <Axes p={H} xl="와인" yl="옷감" grid={false} xt={[20, 40, 60]} yt={[40, 80, 120]} />
      <path d={H.poly([[0, 120], [60, 0]])} fill="none" stroke={C.blue} strokeWidth="2.2" />
      {ok && m > 0 && <path d={H.poly([[0, 120], [120 / tt, 0]])} fill="none" stroke={C.green} strokeWidth="1.8" strokeDasharray="5 3" />}
      <circle cx={H.X(hAut[0])} cy={H.Y(hAut[1])} r="3.5" fill="none" stroke={C.mut} strokeWidth="1.5" />
      <circle cx={H.X(hPro[0])} cy={H.Y(hPro[1])} r="4.5" fill={C.blue} />
      {ok && m > 0 && <circle cx={H.X(hCon[0])} cy={H.Y(hCon[1])} r="5" fill={C.red} />}
      <text x={H.r - 2} y={H.t + 4} textAnchor="end" fontSize="11" fontWeight="800" fill={C.blue}>한국</text>
      <Axes p={F} xl="와인" yl="옷감" grid={false} xt={[10, 20, 30]} yt={[20, 40]} />
      <path d={F.poly([[0, 40], [30, 0]])} fill="none" stroke={C.gold} strokeWidth="2.2" />
      {ok && m > 0 && <path d={F.poly([[30, 0], [Math.max(0, 30 - 60 / tt), Math.min(60, 30 * tt)]])} fill="none" stroke={C.green} strokeWidth="1.8" strokeDasharray="5 3" />}
      <circle cx={F.X(fAut[0])} cy={F.Y(fAut[1])} r="3.5" fill="none" stroke={C.mut} strokeWidth="1.5" />
      <circle cx={F.X(fPro[0])} cy={F.Y(fPro[1])} r="4.5" fill={C.gold} />
      {ok && m > 0 && <circle cx={F.X(fCon[0])} cy={F.Y(fCon[1])} r="5" fill={C.red} />}
      <text x={F.r - 2} y={F.t + 4} textAnchor="end" fontSize="11" fontWeight="800" fill={C.gold}>외국</text>
      <text x="180" y="11" textAnchor="middle" fontSize="9.5" fill={C.mut}>○ 혼자일 때 · ● 생산 · <tspan fill={C.red}>●</tspan> 교역 뒤 소비 · 점선 = 무역선</text>
    </Frame>
  );
}

/* ── 볼록한 생산가능곡선: 값이 바뀌면 생산은 곡선 위를 미끄러지고, 소비는 무역선 위 — 무역 삼각형 ── */
export function PPF({ p = {} }) {
  const [pw, setPw] = useState(p.pw ?? 1.5);
  const [mode, setMode] = useState(p.mode === "ryb" ? "ryb" : "base");
  const clock = useClock({ period: 9, rest: 5 });
  const a = mode === "ryb" ? 12.5 : 10, b = 8;
  const pA = b / a;
  const pr = lerp(pA, pw, ease(clamp(clock.t / 3, 0, 1)));
  const th = Math.atan(b / (a * pr)), x = a * Math.cos(th), y = b * Math.sin(th);
  const I = y + pr * x, cx = I / (2 * pr), cy = I / 2;
  const P = plot({ x0: 0, x1: 17, y0: 0, y1: 15, pad: [12, 14, 24, 30] });
  const ex = x - cx, im = cy - y;
  return (
    <Frame clock={clock} title="생산가능곡선과 무역 삼각형"
      read={<>혼자일 때의 값 {fmt(pA, 2)}(X 1 = Y {fmt(pA, 2)}) → 세계 값 <b>{fmt(pr, 2)}</b>: 생산은 곡선 위를 미끄러져 기울기가 값과 같은 점(파랑)으로, 소비는 그 점을 지나는 무역선 위(빨강) · {Math.abs(ex) < 0.05 ? "아직 교역 없음" : ex > 0 ? <>X <b>{fmt(ex, 2)}</b> 수출, Y <b>{fmt(im, 2)}</b> 수입</> : <>Y <b>{fmt(-im, 2)}</b> 수출, X <b>{fmt(-ex, 2)}</b> 수입</>} (점선 삼각형) · 곡선이 볼록(기회비용 증가)해서 끝까지 특화하지는 않는다{mode === "ryb" ? " · X 에 쓰는 요소가 늘면 같은 값에서 X 는 늘고 Y 는 오히려 준다(립친스키)" : ""}</>}
      controls={<>
        <Slider label="세계 값 (X 1 = Y)" min={0.3} max={2.5} step={0.05} value={pw} onChange={(v) => { setPw(v); clock.reset(); }} />
        <Seg value={mode} onChange={(v) => { setMode(v); clock.reset(); }} options={[["base", "기본"], ["ryb", "X 쪽 요소 ↑"]]} />
      </>}>
      <Axes p={P} xl="X" yl="Y" />
      {mode === "ryb" && <path d={P.curve((t) => 10 * Math.cos(t), (t) => 8 * Math.sin(t), 0, Math.PI / 2, 90)} fill="none" stroke={C.mut} strokeWidth="1.2" strokeDasharray="4 3" />}
      <path d={P.curve((t) => a * Math.cos(t), (t) => b * Math.sin(t), 0, Math.PI / 2, 90)} fill="none" stroke={C.blue} strokeWidth="2.4" />
      <path d={P.path((u) => I - pr * u, 0, I / pr)} fill="none" stroke={C.green} strokeWidth="1.8" />
      <path d={P.path((u) => (I * I) / (4 * pr * u), (I * I) / (4 * pr * 15), 17)} fill="none" stroke={C.violet} strokeWidth="1.1" opacity="0.6" />
      <path d={P.poly([[x, y], [cx, y], [cx, cy]])} fill="none" stroke={C.red} strokeWidth="1.4" strokeDasharray="4 3" />
      <circle cx={P.X(x)} cy={P.Y(y)} r="5" fill={C.blue} />
      <circle cx={P.X(cx)} cy={P.Y(cy)} r="5" fill={C.red} />
      <Label x={P.X(x) + 7} y={P.Y(y) + 4} size={10} color={C.blue} bg>생산</Label>
      <Label x={P.X(cx) + 7} y={P.Y(cy) - 4} size={10} color={C.red} bg>소비</Label>
    </Frame>
  );
}

/* ── 관세: 국내 값이 오르면 생산자는 얻고 소비자는 잃는다 — 정부 수입과 사중손실 두 삼각형 ── */
export function Tariff({ p = {} }) {
  const [tf, setTf] = useState(p.t ?? 3);
  const clock = useClock({ period: 8, rest: 5 });
  const Pw = 5, t = tf * ease(clamp(clock.t / 3, 0, 1)), Pd = Pw + t;
  const Qs0 = Pw - 2, Qd0 = 20 - Pw, Qs = Pd - 2, Qd = 20 - Pd, M = Qd - Qs;
  const A = ((Qs0 + Qs) / 2) * t, Bt = 0.5 * t * (Qs - Qs0), Cr = t * M, Dt = 0.5 * t * (Qd0 - Qd);
  const P = plot({ x0: 0, x1: 20, y0: 0, y1: 16, pad: [12, 14, 24, 30] });
  const lab = (x, y, s) => <text x={P.X(x)} y={P.Y(y) + 4} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{s}</text>;
  return (
    <Frame clock={clock} title="관세의 후생 효과"
      read={<>세계 값 5 에 관세 t = <b>{fmt(t, 2)}</b>: 국내 값 {fmt(Pd, 2)} · 국내 생산 {fmt(Qs0, 1)} → {fmt(Qs, 2)}, 수입 {fmt(Qd0 - Qs0, 1)} → <b>{fmt(M, 2)}</b> · 생산자 이익 a = {fmt(A, 2)} · 정부 관세 수입 c = {fmt(Cr, 2)} · 사중손실 b + d = <b>{fmt(Bt + Dt, 2)}</b> · 소비자 손실 a + b + c + d = {fmt(A + Bt + Cr + Dt, 2)} — 나라 전체로는 b(비싼 국내 생산) + d(덜 사 먹음)만큼 손해</>}
      controls={<Slider label="관세 t" min={0} max={6} step={0.5} value={tf} onChange={(v) => { setTf(v); clock.reset(); }} />}>
      <Axes p={P} xl="Q" yl="P" />
      {t > 0.05 && <>
        <path d={fill(P, [[0, Pw], [0, Pd], [Qs, Pd], [Qs0, Pw]])} fill={C.gold} opacity="0.3" />
        <path d={fill(P, [[Qs0, Pw], [Qs, Pd], [Qs, Pw]])} fill={C.red} opacity="0.35" />
        <path d={fill(P, [[Qs, Pw], [Qs, Pd], [Qd, Pd], [Qd, Pw]])} fill={C.green} opacity="0.25" />
        <path d={fill(P, [[Qd, Pd], [Qd0, Pw], [Qd, Pw]])} fill={C.red} opacity="0.35" />
      </>}
      <path d={P.path((q) => 20 - q, 4, 20)} fill="none" stroke={C.blue} strokeWidth="2.3" />
      <path d={P.path((q) => 2 + q, 0, 14)} fill="none" stroke={C.gold} strokeWidth="2.3" />
      <line x1={P.X(0)} x2={P.X(20)} y1={P.Y(Pw)} y2={P.Y(Pw)} stroke={C.ink} strokeWidth="1.3" />
      {t > 0.05 && <line x1={P.X(0)} x2={P.X(20)} y1={P.Y(Pd)} y2={P.Y(Pd)} stroke={C.red} strokeWidth="1.3" strokeDasharray="5 3" />}
      {t > 1.2 && <>{lab(Qs0 / 2 + 0.6, Pw + t / 2, "a")}{lab(Qs - (Qs - Qs0) / 3, Pw + t / 3, "b")}{lab((Qs + Qd) / 2, Pw + t / 2, "c")}{lab(Qd + (Qd0 - Qd) / 3, Pw + t / 3, "d")}</>}
      <Label x={P.X(19.6)} y={P.Y(Pw) - 4} size={10} color={C.ink} anchor="end" bg>세계 값</Label>
      {t > 0.05 && <Label x={P.X(19.6)} y={P.Y(Pd) - 4} size={10} color={C.red} anchor="end" bg>세계 값 + 관세</Label>}
      <Label x={P.X(4.4)} y={P.Y(15.6) + 10} size={10} color={C.blue} bg>국내 수요</Label>
      <Label x={P.X(13.6)} y={P.Y(15.6) + 10} size={10} color={C.gold} anchor="end" bg>국내 공급</Label>
      {t > 0.05 && <path d={`M${P.X(Qs)} ${P.Y(0) - 5}L${P.X(Qd)} ${P.Y(0) - 5}`} stroke={C.green} strokeWidth="2" />}
      {t > 0.05 && <text x={(P.X(Qs) + P.X(Qd)) / 2} y={P.Y(0) - 9} textAnchor="middle" fontSize="9.5" fill={C.green}>수입</text>}
    </Frame>
  );
}

/* ── 이자율 평형: 원화로 굴리기 vs 달러로 바꿔 굴리고 선물환으로 되바꾸기 — 같아야 차익이 없다 ── */
export function Parity({ p = {} }) {
  const [i, setI] = useState(p.i ?? 3.5);
  const [F, setF] = useState(p.F ?? 1281);
  const clock = useClock({ period: 9, rest: 7 });
  const S = 1300, istar = 5, K = 1300000;
  const Fp = (S * (1 + i / 100)) / (1 + istar / 100);
  const A = K * (1 + i / 100), usd = K / S, usd1 = usd * (1 + istar / 100), Bv = usd1 * F, diff = Bv - A;
  const u = clamp(clock.t / 6, 0, 1);
  const wonFmt = (v) => fmt(Math.round(v), 0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return (
    <Frame clock={clock} title="이자율 평형"
      read={<>원화 이자 i = {fmt(i, 2)} %, 달러 이자 i* = 5 %, 지금 환율 S = 1,300 원/달러 · 차익이 없으려면 F = S × (1 + i)/(1 + i*) = <b>{fmt(Fp, 1)}</b> · 지금 선물환 F = {F}: 길 A {wonFmt(A)} 원, 길 B {wonFmt(Bv)} 원 → {Math.abs(diff) < 650 ? "거의 같다 — 차익 없음" : diff > 0 ? <><b>B 가 {wonFmt(diff)} 원 더</b> — 원화를 빌려 달러로 굴리고 선물환으로 되파는 차익거래가 생긴다</> : <><b>A 가 {wonFmt(-diff)} 원 더</b> — 달러를 빌려 원화로 굴리는 반대 차익거래</>} · 이자가 높은 통화(달러)는 선물환에서 그만큼 싸게(할인) 거래된다</>}
      controls={<>
        <Slider label="원화 이자 i" min={0} max={8} step={0.25} value={i} onChange={setI} show={(v) => fmt(v, 2) + " %"} />
        <Slider label="선물환 F" min={1240} max={1340} step={1} value={F} onChange={setF} show={(v) => v + " 원"} />
      </>}>
      <rect x="6" y="88" width="56" height="44" rx="8" fill={C.in} stroke={C.bd} />
      <text x="34" y="106" textAnchor="middle" fontSize="10" fill={C.ink}>오늘</text>
      <text x="34" y="122" textAnchor="middle" fontSize="9.5" fill={C.mut}>130 만 원</text>
      <rect x="298" y="88" width="56" height="44" rx="8" fill={C.in} stroke={C.bd} />
      <text x="326" y="106" textAnchor="middle" fontSize="10" fill={C.ink}>1 년 뒤</text>
      <text x="326" y="122" textAnchor="middle" fontSize="9.5" fill={C.mut}>원화로</text>
      <path d="M62 96 C 110 40, 250 40, 298 96" fill="none" stroke={C.blue} strokeWidth="2" />
      <text x="180" y="40" textAnchor="middle" fontSize="10" fill={C.blue}>길 A — 한국 예금 (1 + i)</text>
      <path d="M62 124 C 90 170, 120 172, 130 172 L 230 172 C 250 172, 280 170, 298 124" fill="none" stroke={C.gold} strokeWidth="2" />
      {[[110, "달러로 바꿈", "÷ S"], [180, "미국 예금", "× (1 + i*)"], [250, "선물환으로", "× F"]].map(([x, a1, b1]) => (
        <g key={x}><circle cx={x} cy="172" r="4" fill={C.gold} /><text x={x} y="192" textAnchor="middle" fontSize="9.5" fill={C.ink}>{a1}</text><text x={x} y="205" textAnchor="middle" fontSize="9" fill={C.mut}>{b1}</text></g>
      ))}
      <text x="180" y="160" textAnchor="middle" fontSize="10" fill={C.gold}>길 B</text>
      <circle cx={lerp(62, 298, u)} cy={96 - Math.sin(Math.PI * u) * 42} r="6" fill={C.blue} />
      <circle cx={u < 0.25 ? lerp(62, 130, u / 0.25) : u < 0.75 ? lerp(130, 230, (u - 0.25) / 0.5) : lerp(230, 298, (u - 0.75) / 0.25)} cy={u < 0.25 ? lerp(124, 172, u / 0.25) : u < 0.75 ? 172 : lerp(172, 124, (u - 0.75) / 0.25)} r="6" fill={C.gold} />
      <text x="180" y="72" textAnchor="middle" fontSize="11" fontWeight="800" fill={C.blue}>{u > 0.98 ? wonFmt(A) + " 원" : ""}</text>
      <text x="180" y="146" textAnchor="middle" fontSize="11" fontWeight="800" fill={C.gold}>{u < 0.25 ? "" : u < 0.5 ? "$" + fmt(usd, 0) : u < 0.98 ? "$" + fmt(usd1, 0) : wonFmt(Bv) + " 원"}</text>
    </Frame>
  );
}

/* ── 인코텀즈: 위험이 넘어가는 곳과 비용을 누가 내는지 — 조건마다 값이 쌓인다 ── */
const LEGS = [
  ["공장도", 100], ["내륙 운송", 6], ["수출 통관", 2], ["선적", 3], ["해상 운임", 12], ["보험", 1], ["도착항 처리", 3], ["내륙 운송", 5], ["수입 통관 · 관세", 8],
];
const TERMS = {
  EXW: { pay: 1, risk: 0, say: "공장 인도 — 판매자 공장에서 물건을 넘기면 끝. 싣는 일부터 모든 비용 · 위험은 사는 사람" },
  FOB: { pay: 4, risk: 2, say: "본선 인도 — 선적항에서 배에 실리는 순간 위험이 넘어간다. 운임 · 보험은 사는 사람" },
  CFR: { pay: 5, risk: 2, say: "운임 포함 — 판매자가 운임을 내지만 위험은 FOB 처럼 선적항에서 넘어간다(비용과 위험의 갈림이 다르다)" },
  CIF: { pay: 6, risk: 2, say: "운임 · 보험 포함 — CFR 에 판매자가 드는 보험(최소 조건)까지. 위험은 여전히 선적항에서" },
  DAP: { pay: 8, risk: 5, say: "도착지 인도 — 판매자가 도착지까지 위험 · 운송비를 진다. 수입 통관 · 관세는 사는 사람" },
  DDP: { pay: 9, risk: 5, say: "관세 지급 인도 — 판매자가 수입 관세까지 다 내고 사는 사람 문 앞까지" },
};
const STOPS = [["공장", 22], ["수출 통관", 74], ["선적항", 124], ["도착항", 236], ["수입 통관", 288], ["사는 사람", 338]];
export function Incoterms({ p = {} }) {
  const [term, setTerm] = useState(TERMS[p.term] ? p.term : "FOB");
  const clock = useClock({ period: 10, rest: 6 });
  const T = TERMS[term];
  const riskX = STOPS[T.risk][1];
  const x = 22 + 316 * clamp(clock.t / 8, 0, 1);
  const price = LEGS.slice(0, T.pay).reduce((s, l) => s + l[1], 0), total = LEGS.reduce((s, l) => s + l[1], 0);
  let acc = 0;
  const W = 300 / total;
  return (
    <Frame clock={clock} title="인코텀즈 — 위험과 비용의 갈림"
      read={<><b>{term}</b>: {T.say} · 판매자가 부르는 값 = {LEGS.slice(0, T.pay).map((l) => l[1]).join(" + ")} = <b>{price}</b> (파랑 = 값에 들어간 비용, 노랑 = 사는 사람이 따로 내는 비용) · 짐 색이 바뀌는 곳 = 위험이 사는 사람에게 넘어가는 곳</>}
      controls={<Seg value={term} onChange={(v) => { setTerm(v); clock.reset(); }} options={Object.keys(TERMS).map((k) => [k, k])} />}>
      <path d="M22 70 L124 70" stroke={C.mut} strokeWidth="3" />
      <path d="M124 70 C 160 92, 200 92, 236 70" stroke={C.blue} strokeWidth="3" fill="none" strokeDasharray="6 4" opacity="0.6" />
      <path d="M236 70 L338 70" stroke={C.mut} strokeWidth="3" />
      <text x="180" y="100" textAnchor="middle" fontSize="9.5" fill={C.mut}>바다</text>
      {STOPS.map(([n, sx]) => <g key={n}><circle cx={sx} cy="70" r="5" fill={C.card} stroke={C.ink} strokeWidth="1.5" /><text x={sx} y="54" textAnchor="middle" fontSize="9.5" fill={C.ink}>{n}</text></g>)}
      <line x1={riskX} x2={riskX} y1="40" y2="112" stroke={C.red} strokeWidth="1.6" strokeDasharray="4 3" />
      <text x={clamp(riskX, 34, 326)} y="122" textAnchor="middle" fontSize="9.5" fontWeight="800" fill={C.red}>위험이 넘어감</text>
      <rect x={x - 11} y={x > 124 && x < 236 ? 72 + Math.sin(((x - 124) / 112) * Math.PI) * 14 - 22 : 58} width="22" height="14" rx="2" fill={x < riskX ? C.blue : C.gold} stroke={C.ink} strokeWidth="1" />
      {LEGS.map(([n, v], k) => { const x0 = 30 + acc * W; acc += v; const seller = k < T.pay; return (
        <g key={k}>
          <rect x={x0} y="150" width={v * W - 1} height="22" fill={seller ? C.blue : C.gold} opacity={seller ? 0.75 : 0.45} />
          {v * W > 26 && <text x={x0 + (v * W) / 2} y="165" textAnchor="middle" fontSize="9" fill="#fff">{v}</text>}
        </g>); })}
      <text x="30" y="144" fontSize="9" fill={C.mut}>쌓이는 비용: 공장도 · 내륙 · 통관 · 선적 · 운임 · 보험 · 도착항 · 내륙 · 관세</text>
      <line x1={30 + price * W} x2={30 + price * W} y1="146" y2="182" stroke={C.ink} strokeWidth="1.6" />
      <text x={clamp(30 + price * W, 40, 320)} y="196" textAnchor="middle" fontSize="10.5" fontWeight="800" fill={C.ink}>{term} 값 {price}</text>
    </Frame>
  );
}
