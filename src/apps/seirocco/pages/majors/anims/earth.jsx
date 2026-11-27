// 지구과학 그림 — 대권 항로(메르카토르) · 진앙 찾기 · 코리올리 효과 · 조석(대조 · 소조) · 에너지 균형과 눈덩이 지구 · 등시선 연대 · 밀란코비치 주기 · 데이지 세계
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, useClock } from "./kit.jsx";

const RAD = Math.PI / 180, RE = 6371, SIG = 5.67e-8;
const pth = (pts) => pts.map(([x, y], i) => (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1)).join("") || "M0 0";

/* ── 대권 항로: 지구에서 가장 짧은 길은 지도에서 휘어 보인다 ── */
const CITY = { sel: [37.57, 126.98, "서울"], ny: [40.71, -74.01, "뉴욕"], lon: [51.51, -0.13, "런던"], syd: [-33.87, 151.21, "시드니"] };
const vec = (p) => [Math.cos(p[0] * RAD) * Math.cos(p[1] * RAD), Math.cos(p[0] * RAD) * Math.sin(p[1] * RAD), Math.sin(p[0] * RAD)];
function gcPts(a, b, n = 120) {
  const A = vec(a), B = vec(b), om = Math.acos(clamp(A[0] * B[0] + A[1] * B[1] + A[2] * B[2], -1, 1)), s = Math.sin(om);
  return Array.from({ length: n + 1 }, (_, i) => {
    const t = i / n, P = A.map((x, k) => (Math.sin((1 - t) * om) / s) * x + (Math.sin(t * om) / s) * B[k]);
    return [Math.asin(P[2]) / RAD, Math.atan2(P[1], P[0]) / RAD];
  });
}
const hav = (a, b) => {
  const h = Math.sin(((b[0] - a[0]) * RAD) / 2) ** 2 + Math.cos(a[0] * RAD) * Math.cos(b[0] * RAD) * Math.sin(((b[1] - a[1]) * RAD) / 2) ** 2;
  return 2 * RE * Math.asin(Math.sqrt(h));
};
const merc = (lat) => Math.log(Math.tan(Math.PI / 4 + (clamp(lat, -85, 85) * RAD) / 2));
function rhumb(a, b) {
  const p1 = a[0] * RAD, p2 = b[0] * RAD;
  let dl = (b[1] - a[1]) * RAD;
  if (Math.abs(dl) > Math.PI) dl = dl > 0 ? dl - 2 * Math.PI : dl + 2 * Math.PI;
  const dpsi = merc(b[0]) - merc(a[0]), qq = Math.abs(dpsi) > 1e-12 ? (p2 - p1) / dpsi : Math.cos(p1);
  return { d: RE * Math.sqrt((p2 - p1) ** 2 + qq * qq * dl * dl), dl: dl / RAD };
}
const MX = (lon) => { let d = lon - 160; while (d < -180) d += 360; while (d > 180) d -= 360; return 180 + d * (340 / 360); };
const MY = (lat) => 112 - merc(lat) * 44;
function splitWrap(pts) {
  const segs = [];
  let cur = [];
  pts.forEach((q, i) => { if (i && Math.abs(q[0] - pts[i - 1][0]) > 170) { segs.push(cur); cur = []; } cur.push(q); });
  segs.push(cur);
  return segs;
}
export function GreatCircle({ p = {} }) {
  const [to, setTo] = useState(["ny", "lon", "syd"].includes(p.to) ? p.to : "ny");
  const A = CITY.sel, B = CITY[to];
  const G = useMemo(() => gcPts(A, B), [to]);
  const clock = useClock({ period: 10, rest: 6 });
  const k = Math.min(G.length - 1, Math.floor((clock.t / 8) * G.length));
  const R = rhumb(A, B), d = hav(A, B), maxLat = Math.max(...G.map((q) => q[0])), extra = (R.d / d - 1) * 100;
  const psiA = merc(A[0]), psiB = merc(B[0]);
  const rl = Array.from({ length: 61 }, (_, i) => { const t = i / 60; return [MX(A[1] + R.dl * t), 112 - (psiA + (psiB - psiA) * t) * 44]; });
  const gc = G.map(([la, lo]) => [MX(lo), MY(la)]), pl = gc[k];
  return (
    <Frame clock={clock} title="대권 항로 — 가장 짧은 길은 지도에서 휘어 보인다"
      read={<>메르카토르 지도(경선과 위선이 직각, 높은 위도일수록 크게 늘어남) · 서울 → {B[2]}: 대권(지구 중심을 지나는 평면이 지구 겉면과 만나는 원, 빨강) <b>{fmt(d, 0)} km</b>, 나침반 방위를 일정하게 지키는 항정선(파랑 점선) {fmt(R.d, 0)} km · {extra > 1
        ? <>항정선이 {fmt(extra, 0)} % 더 길다 — 대권은 지도에서 극 쪽으로 휘어(북위 {fmt(maxLat, 0)}° 까지) 보이지만 실제로는 가장 짧은 길이라, 비행기는 북극 가까이로 돌아간다</>
        : <>거의 남북으로 가는 길이라 두 선이 거의 겹친다 — 경선은 대권이면서 항정선이기도 하다</>}</>}
      controls={<Seg value={to} onChange={(v) => { setTo(v); clock.reset(); }} options={[["ny", "뉴욕"], ["lon", "런던"], ["syd", "시드니"]]} />}>
      <rect x="10" y="8" width="340" height="208" fill={C.blue} fillOpacity="0.07" stroke={C.bd} />
      {[-60, -30, 0, 30, 60].map((la) => (
        <g key={la}>
          <line x1="10" x2="350" y1={MY(la)} y2={MY(la)} stroke={C.bd} strokeWidth={la === 0 ? 1.3 : 0.7} />
          <text x="14" y={MY(la) - 3} fontSize="8.5" fill={C.mut}>{la > 0 ? `${la}°N` : la < 0 ? `${-la}°S` : "적도"}</text>
        </g>
      ))}
      {[-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180].map((lo) => <line key={lo} x1={MX(lo)} x2={MX(lo)} y1="8" y2="216" stroke={C.bd} strokeWidth="0.7" />)}
      {splitWrap(rl).map((s, i) => <path key={"r" + i} d={pth(s)} fill="none" stroke={C.blue} strokeWidth="1.8" strokeDasharray="5 3" />)}
      {splitWrap(gc).map((s, i) => <path key={"g" + i} d={pth(s)} fill="none" stroke={C.red} strokeWidth="2.2" />)}
      {[A, B].map((c) => (
        <g key={c[2]}>
          <circle cx={MX(c[1])} cy={MY(c[0])} r="4" fill={C.ink} />
          <Label x={MX(c[1]) + 6} y={MY(c[0]) + 4} size={10} bold bg>{c[2]}</Label>
        </g>
      ))}
      <circle cx={pl[0]} cy={pl[1]} r="5" fill={C.red} stroke={C.card} strokeWidth="1.5" />
    </Frame>
  );
}

/* ── 진앙 찾기: S − P 시간으로 거리를, 세 원으로 위치를 ── */
const VP = 6, VS = 3.5, EPI = [44, 58], STA = [[20, 22, "가"], [112, 40, "나"], [100, 125, "다"]];
export function Quake() {
  const clock = useClock({ period: 14, rest: 13 });
  const t = clamp(0.8 + clock.t * 2.2, 0, 26);
  const P = plot({ x0: 0, x1: 130, y0: 0, y1: 142.6, W: 360, H: 220, pad: [8, 166, 8, 8] });
  const s = P.X(1) - P.X(0);
  const dist = STA.map(([x, y]) => Math.hypot(x - EPI[0], y - EPI[1]));
  const sp = dist.map((d) => d / VS - d / VP);
  const showC = t > Math.max(...dist.map((d) => d / VS)) + 0.8;
  const tx0 = 206, tw = 146, TT = (tt) => tx0 + (tt / 26) * tw;
  const wig = (i) => {
    const pts = [], ar = dist[i] / VP, as = dist[i] / VS, end = Math.min(t, 26);
    for (let k = 0; k <= 300; k++) {
      const tt = (k / 300) * end;
      let a = 0;
      if (tt > ar) a += 4 * Math.exp(-(tt - ar) * 0.6) * Math.sin((tt - ar) * 9);
      if (tt > as) a += 10 * Math.exp(-(tt - as) * 0.45) * Math.sin((tt - as) * 6);
      pts.push([TT(tt), 52 + i * 62 - a]);
    }
    return pth(pts);
  };
  return (
    <Frame clock={clock} title="진앙 찾기 — P 파와 S 파의 시간 차"
      read={<>지진이 나면 빠른 P 파(초속 {VP} km, 파랑)와 느린 S 파(초속 {VS} km, 빨강)가 함께 퍼진다 · 관측소마다 두 파가 도착한 시간 차 Δt 를 재면 거리 = Δt × VP × VS ÷ (VP − VS) = Δt × 8.4 km · 관측소 가 · 나 · 다의 S − P 시간 {sp.map((v) => fmt(v, 1)).join(" · ")} 초 → 거리 {dist.map((v) => fmt(v, 0)).join(" · ")} km · 세 관측소를 중심으로 그 거리만큼의 원을 그리면 한 점에서 만난다{showC ? " — 그 점(노란 별)이 진앙" : ""}</>}>
      <defs><clipPath id="ma-quake-map"><rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} /></clipPath></defs>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill={C.gold} fillOpacity="0.06" stroke={C.bd} />
      <g clipPath="url(#ma-quake-map)">
        <circle cx={P.X(EPI[0])} cy={P.Y(EPI[1])} r={t * VP * s} fill="none" stroke={C.blue} strokeWidth="1.4" opacity="0.75" />
        <circle cx={P.X(EPI[0])} cy={P.Y(EPI[1])} r={t * VS * s} fill="none" stroke={C.red} strokeWidth="1.7" opacity="0.75" />
        {showC && STA.map(([x, y], i) => <circle key={i} cx={P.X(x)} cy={P.Y(y)} r={dist[i] * s} fill="none" stroke={C.gold} strokeWidth="1.3" strokeDasharray="4 3" />)}
      </g>
      {STA.map(([x, y, n]) => (
        <g key={n}>
          <polygon points={`${P.X(x)},${P.Y(y) - 6} ${P.X(x) - 5},${P.Y(y) + 4} ${P.X(x) + 5},${P.Y(y) + 4}`} fill={C.ink} />
          <text x={P.X(x) + 7} y={P.Y(y) + 4} fontSize="10" fill={C.ink}>{n}</text>
        </g>
      ))}
      {showC && <text x={P.X(EPI[0])} y={P.Y(EPI[1]) + 5} textAnchor="middle" fontSize="15" fill={C.gold}>★</text>}
      {STA.map((st, i) => (
        <g key={"w" + i}>
          <text x={tx0} y={28 + i * 62} fontSize="9.5" fill={C.ink}>관측소 {st[2]}</text>
          <line x1={tx0} x2={tx0 + tw} y1={52 + i * 62} y2={52 + i * 62} stroke={C.bd} />
          <path d={wig(i)} fill="none" stroke={C.ink} strokeWidth="1" />
          {t > dist[i] / VP && <line x1={TT(dist[i] / VP)} x2={TT(dist[i] / VP)} y1={38 + i * 62} y2={68 + i * 62} stroke={C.blue} strokeWidth="1.3" />}
          {t > dist[i] / VS && <line x1={TT(dist[i] / VS)} x2={TT(dist[i] / VS)} y1={38 + i * 62} y2={68 + i * 62} stroke={C.red} strokeWidth="1.3" />}
          {t > dist[i] / VS && <text x={(TT(dist[i] / VP) + TT(dist[i] / VS)) / 2} y={78 + i * 62} textAnchor="middle" fontSize="8.5" fill={C.gold}>{fmt(sp[i], 1)} 초</text>}
        </g>
      ))}
      <text x={tx0 + tw} y="214" textAnchor="end" fontSize="9" fill={C.mut}>시간 →</text>
    </Frame>
  );
}

/* ── 코리올리 효과: 회전하는 원판 위로 굴린 공 ── */
export function Coriolis() {
  const clock = useClock({ period: 8, rest: 6.5 });
  const t = clamp(clock.t, 0, 6), om = (2 * Math.PI) / 16, v = 0.15;
  const R = 70, cxL = 92, cxR = 268, cy = 112;
  const rot = (q, a) => [q[0] * Math.cos(a) - q[1] * Math.sin(a), q[0] * Math.sin(a) + q[1] * Math.cos(a)];
  const ballI = [v * t, 0], tgtI = rot([1, 0], om * t);
  const trailR = Array.from({ length: 41 }, (_, i) => { const tt = (i / 40) * t; return rot([v * tt, 0], -om * tt); });
  const spokes = (cx, a) => [0, 1, 2, 3].map((j) => { const q = rot([1, 0], a + (j * Math.PI) / 2); return <line key={j} x1={cx} y1={cy} x2={cx + q[0] * R} y2={cy - q[1] * R} stroke={C.bd} />; });
  const end = trailR[40];
  return (
    <Frame clock={clock} title="코리올리 효과 — 도는 땅 위에서 보면 휘어 간다"
      read={<>반시계 방향으로 도는 원판(북반구를 북극 위에서 본 모습)의 가운데에서 가장자리의 표적(노랑)을 향해 공을 굴린다 · 왼쪽(밖에서 본 모습): 공은 곧게 가지만 그사이 원판이 돌아 표적이 비켜 간다 · 오른쪽(원판 위의 사람이 본 모습): 공이 <b>오른쪽으로 휘어</b> 가는 것처럼 보인다 — 도는 좌표계에만 나타나는 겉보기 힘, 코리올리 가속도 −2Ω × v · 그래서 북반구의 태풍은 반시계 방향으로, 남반구의 태풍은 시계 방향으로 돈다</>}>
      <text x={cxL} y="20" textAnchor="middle" fontSize="10" fill={C.ink}>밖에서 본 모습</text>
      <text x={cxR} y="20" textAnchor="middle" fontSize="10" fill={C.ink}>원판 위에서 본 모습</text>
      <circle cx={cxL} cy={cy} r={R} fill={C.blue} fillOpacity="0.08" stroke={C.mut} />
      {spokes(cxL, om * t)}
      <path d={`M ${cxL + 46} ${cy - 62} A 77 77 0 0 0 ${cxL - 10} ${cy - 76}`} fill="none" stroke={C.mut} strokeWidth="1.2" />
      <polygon points={`${cxL - 10},${cy - 76} ${cxL - 2},${cy - 81} ${cxL - 1},${cy - 72}`} fill={C.mut} />
      <line x1={cxL} y1={cy} x2={cxL + ballI[0] * R} y2={cy} stroke={C.red} strokeWidth="1.6" strokeDasharray="3 2" />
      <circle cx={cxL + tgtI[0] * R} cy={cy - tgtI[1] * R} r="5" fill={C.gold} />
      <circle cx={cxL + ballI[0] * R} cy={cy} r="4.6" fill={C.red} />
      <circle cx={cxR} cy={cy} r={R} fill={C.blue} fillOpacity="0.08" stroke={C.mut} />
      {spokes(cxR, 0)}
      <line x1={cxR} y1={cy} x2={cxR + R} y2={cy} stroke={C.gold} strokeWidth="1" strokeDasharray="4 3" />
      <path d={pth(trailR.map((q) => [cxR + q[0] * R, cy - q[1] * R]))} fill="none" stroke={C.red} strokeWidth="2" />
      <circle cx={cxR + R} cy={cy} r="5" fill={C.gold} />
      <circle cx={cxR + end[0] * R} cy={cy - end[1] * R} r="4.6" fill={C.red} />
      <text x={cxL} y="206" textAnchor="middle" fontSize="9.5" fill={C.mut}>공은 곧게, 땅이 돈다</text>
      <text x={cxR} y="206" textAnchor="middle" fontSize="9.5" fill={C.red}>공이 오른쪽으로 휜다</text>
    </Frame>
  );
}

/* ── 조석: 달과 해의 기조력, 대조와 소조 ── */
export function Tide() {
  const clock = useClock({ period: 14, rest: 3.5 });
  const thM = (clock.t / 14) * 2 * Math.PI, thS = Math.PI, Am = 1, As = 0.46;
  const h = (th) => Am * Math.cos(2 * (th - thM)) + As * Math.cos(2 * (th - thS));
  const range = (dd) => Math.sqrt(Am * Am + As * As + 2 * Am * As * Math.cos(2 * dd));
  const cx = 118, cy = 112, R = 46, k = 9, orb = 84;
  const water = Array.from({ length: 181 }, (_, i) => { const th = (i / 180) * 2 * Math.PI, r = R + k * h(th); return [cx + r * Math.cos(th), cy - r * Math.sin(th)]; });
  const mx = cx + orb * Math.cos(thM), my = cy - orb * Math.sin(thM);
  const P = plot({ x0: 0, x1: 2 * Math.PI, y0: 0, y1: 1.6, W: 360, H: 220, pad: [26, 12, 30, 236] });
  const cur = range(thM - thS), wrapped = ((thM % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
  const phase = cur > 1.35 ? (Math.cos(thM - thS) > 0 ? "그믐 무렵 · 대조(사리)" : "보름 무렵 · 대조(사리)") : cur < 0.62 ? "반달 무렵 · 소조(조금)" : "대조와 소조 사이";
  return (
    <Frame clock={clock} title="조석 — 달과 해가 바닷물을 당긴다"
      read={<>기조력은 거리의 세제곱에 반비례해(1 ÷ r³) 지구의 달 쪽과 그 반대쪽 두 곳에 바닷물이 부푼다 — 지구가 하루 한 바퀴 돌며 두 부풂을 지나가므로 밀물 · 썰물이 하루 두 번 · 해의 기조력은 달의 약 0.46 배 · 달(회색)이 해(왼쪽)와 일직선이면 두 부풂이 겹쳐 조차가 크고(대조), 직각이면 서로 깎여 작다(소조) · 지금 조차는 대조 때의 {fmt((cur / (Am + As)) * 100, 0)} % — <b>{phase}</b></>}>
      <circle cx="14" cy={cy} r="9" fill={C.gold} />
      <text x="14" y={cy + 22} textAnchor="middle" fontSize="9" fill={C.mut}>해</text>
      <circle cx={cx} cy={cy} r={orb} fill="none" stroke={C.bd} strokeDasharray="3 3" />
      <path d={pth(water) + "Z"} fill={C.blue} fillOpacity="0.35" stroke={C.blue} />
      <circle cx={cx} cy={cy} r="34" fill={C.green} fillOpacity="0.45" stroke={C.green} strokeWidth="0.8" />
      <circle cx={mx} cy={my} r="8" fill={C.mut} fillOpacity="0.55" stroke={C.mut} />
      <text x={mx} y={Math.sin(thM) > 0 ? my - 12 : my + 20} textAnchor="middle" fontSize="9" fill={C.mut}>달</text>
      <text x={P.l} y={P.t - 12} fontSize="9.5" fill={C.ink}>한 달 동안의 조차</text>
      <Axes p={P} xl="" yl="" grid={false} xt={[]} yt={[]} />
      <path d={P.path((x) => range(x - thS), 0, 2 * Math.PI, 120)} fill="none" stroke={C.blue} strokeWidth="2" />
      <circle cx={P.X(wrapped)} cy={P.Y(cur)} r="4" fill={C.red} />
      {[[0, "보름"], [Math.PI / 2, "반달"], [Math.PI, "그믐"], [2 * Math.PI, "보름"]].map(([x, nm], i) => <text key={i} x={P.X(x)} y={P.b + 13} fontSize="8.5" fill={C.mut} textAnchor={i === 3 ? "end" : i === 0 ? "start" : "middle"}>{nm}</text>)}
    </Frame>
  );
}

/* ── 에너지 균형 모형: 얼음–반사율 되먹임과 눈덩이 지구 ── */
const S0 = 1361, EPS = 0.612;
const alb = (T) => 0.3 + 0.32 / (1 + Math.exp((T - 262) / 4));
export function EBM({ p = {} }) {
  const [mu, setMu] = useState(clamp(p.mu ?? 1, 0.75, 1.25));
  const clock = useClock({ period: 10, rest: 9.5 });
  const absorb = (T) => (mu * S0 * (1 - alb(T))) / 4, emit = (T) => EPS * SIG * T ** 4;
  const eq = useMemo(() => {
    const r = [];
    for (let T = 200; T < 320; T += 0.05) { const a = absorb(T) - emit(T), b = absorb(T + 0.05) - emit(T + 0.05); if (a * b <= 0 && a !== b) r.push({ T: T + 0.025, stable: a > b }); }
    return r;
  }, [mu]);
  const P = plot({ x0: 200, x1: 320, y0: 40, y1: 380, pad: [12, 12, 26, 38] });
  const steps = Math.floor(clock.t * 30);
  const balls = [215, 252, 260, 310].map((T0) => { let T = T0; for (let i = 0; i < steps; i++) T += 0.01 * (absorb(T) - emit(T)); return T; });
  return (
    <Frame clock={clock} title="에너지 균형 — 얼음이 얼음을 부른다"
      read={<>지구가 받는 햇빛(빨강) = 태양 상수 × {mu.toFixed(2)} × (1 − 반사율) ÷ 4, 내보내는 열복사(파랑) = εσT⁴ · 얼음이 덮이면 햇빛을 더 많이 반사하므로(반사율 0.3 → 0.62) 빨간 곡선이 계단 모양이다 · 두 곡선이 만나는 곳이 평형 온도: {eq.map((e) => `${fmt(e.T, 0)} K(${e.stable ? "안정" : "불안정"})`).join(", ")} · 보라 점 = 처음 온도가 다른 네 지구 — {eq.length > 2 ? "불안정한 평형을 사이에 두고 운명이 갈린다" : "평형이 하나뿐이라 모두 그곳으로 간다"} · 햇빛을 줄이면 따뜻한 평형이 사라져 눈덩이 지구로 떨어지고, 다시 늘려도 한참 더 늘려야 녹는다(이력 현상)</>}
      controls={<Slider label="햇빛 배율" min={0.75} max={1.25} step={0.01} value={mu} onChange={(v) => { setMu(v); clock.reset(); }} show={(v) => v.toFixed(2)} />}>
      <Axes p={P} xl="T (K)" yl="W/m²" grid={false} xt={[220, 260, 300]} yt={[100, 200, 300]} />
      <path d={P.path(absorb, 200, 320, 240)} fill="none" stroke={C.red} strokeWidth="2.2" />
      <path d={P.path(emit, 200, 320, 240)} fill="none" stroke={C.blue} strokeWidth="2.2" />
      {eq.map((e, i) => <circle key={i} cx={P.X(e.T)} cy={P.Y(emit(e.T))} r="4.6" fill={e.stable ? C.green : C.card} stroke={e.stable ? C.green : C.gold} strokeWidth="2" />)}
      {balls.map((T, i) => <circle key={"b" + i} cx={P.X(clamp(T, 200, 320))} cy={P.b - 7} r="4" fill={C.violet} fillOpacity="0.85" />)}
      <Label x={P.X(204)} y={P.Y(absorb(204)) - 8} size={9.5} color={C.red} bg>받는 햇빛</Label>
      <Label x={P.X(314)} y={P.Y(emit(314)) + 14} size={9.5} color={C.blue} anchor="end" bg>내보내는 열</Label>
    </Frame>
  );
}

/* ── 등시선 연대 측정: Rb–Sr ── */
const LAMB = 1.42e-11, XS = [0.15, 0.6, 1.1, 1.7, 2.3, 2.9];
export function Isochron() {
  const clock = useClock({ period: 12, rest: 11 });
  const age = clamp(clock.t / 10, 0, 1) * 4.5e9, g = Math.exp(LAMB * age), slope = g - 1;
  const pts = XS.map((x0) => [x0 / g, 0.7 + x0 * (1 - 1 / g)]);
  const P = plot({ x0: 0, x1: 3.1, y0: 0.68, y1: 0.92, pad: [12, 12, 26, 42] });
  return (
    <Frame clock={clock} title="등시선 — 바위의 나이를 직선의 기울기로"
      read={<>같은 마그마에서 굳은 광물들은 처음의 ⁸⁷Sr/⁸⁶Sr 비가 같고(0.7) 루비듐의 양만 다르다 · ⁸⁷Rb 는 반감기 488 억 년으로 붕괴해 ⁸⁷Sr 이 되므로, 루비듐이 많은 광물일수록 ⁸⁷Sr 이 더 많이 쌓인다 · 점들은 언제나 한 직선(등시선) 위에 있고 그 기울기는 exp(λt) − 1 · 지금 {fmt(age / 1e8, 1)} 억 년, 기울기 <b>{fmt(slope, 4)}</b> → 나이 t = ln(1 + 기울기) ÷ λ · 처음 비(세로 절편)를 몰라도 나이가 나온다 — 운석으로 잰 태양계의 나이 약 46 억 년도 이렇게 구했다</>}>
      <Axes p={P} xl="⁸⁷Rb / ⁸⁶Sr" yl="⁸⁷Sr / ⁸⁶Sr" grid={false} xt={[1, 2, 3]} yt={[0.7, 0.75, 0.8, 0.85, 0.9]} />
      <line x1={P.X(0)} x2={P.X(3.1)} y1={P.Y(0.7)} y2={P.Y(0.7)} stroke={C.mut} strokeDasharray="4 3" />
      <line x1={P.X(0)} x2={P.X(3.1)} y1={P.Y(0.7)} y2={P.Y(0.7 + 3.1 * slope)} stroke={C.red} strokeWidth="1.8" />
      {XS.map((x0, i) => <line key={"t" + i} x1={P.X(x0)} y1={P.Y(0.7)} x2={P.X(pts[i][0])} y2={P.Y(pts[i][1])} stroke={C.mut} strokeDasharray="2 2" />)}
      {pts.map(([x, y], i) => <circle key={i} cx={P.X(x)} cy={P.Y(y)} r="4.4" fill={C.blue} stroke={C.card} />)}
      <Label x={P.X(1.6)} y={P.Y(0.7 + 1.6 * slope) - 12} size={10} color={C.red} bold bg>{`기울기 ${fmt(slope, 4)}`}</Label>
    </Frame>
  );
}

/* ── 밀란코비치 주기 (단순화한 합성) ── */
const ecc = (t) => 0.028 + 0.012 * Math.cos((2 * Math.PI * t) / 100) + 0.009 * Math.cos((2 * Math.PI * t) / 405 + 1) + 0.004 * Math.cos((2 * Math.PI * t) / 95 + 2);
const obl = (t) => 23.3 + 1.0 * Math.cos((2 * Math.PI * t) / 41 + 0.5);
const prec = (t) => ecc(t) * Math.sin((2 * Math.PI * t) / 23 + 0.3);
export function Milank({ p = {} }) {
  const [on, setOn] = useState(["all", "obl", "prec"].includes(p.on) ? p.on : "all");
  const clock = useClock({ period: 12, rest: 11.5 });
  const tm = Math.floor(clamp(clock.t / 11, 0, 1) * 800);
  const ins = (t) => 480 + (on !== "prec" ? 10 * (obl(t) - 23.3) : 0) + (on !== "obl" ? 520 * prec(t) : 0);
  const X = (ka) => 34 + ((800 - ka) / 800) * 316;
  const rows = [["이심률(약 10 만 · 40 만 년)", ecc, 0, 0.055, C.gold], ["자전축 기울기(4.1 만 년)", obl, 22.1, 24.5, C.green], ["세차(약 2.3 만 년)", prec, -0.056, 0.056, C.violet]];
  const lane = (f, lo, hi, y0, hh, n) => Array.from({ length: n + 1 }, (_, j) => [X(800 - j), y0 + hh - ((f(800 - j) - lo) / (hi - lo)) * hh]);
  const insPts = (n) => Array.from({ length: n + 1 }, (_, j) => [X(800 - j), 195 - ((ins(800 - j) - 440) / 80) * 50]);
  const lit = (i) => on === "all" || (on === "obl" && i === 1) || (on === "prec" && i !== 1);
  return (
    <Frame clock={clock} title="밀란코비치 주기 — 궤도의 흔들림이 빙하기를 부른다"
      read={<>지구 궤도의 세 가지 느린 흔들림 — 이심률(궤도가 얼마나 찌그러졌나), 자전축 기울기(22.1° ~ 24.5°), 세차(자전축이 팽이처럼 도는 것) · 세 가지가 겹쳐 북위 65° 의 여름 햇빛(맨 아래, 단순화한 합성)이 오르내린다 — 세차의 흔들림 폭은 이심률이 클 때 커진다 · 여름이 서늘해 겨울 눈이 다 녹지 않고 쌓이면 빙하기가 온다 · 지난 80 만 년 동안 빙하기는 약 10 만 년마다 되풀이되었다(오른쪽 끝이 지금)</>}
      controls={<Seg value={on} onChange={setOn} options={[["all", "모두 합치기"], ["obl", "기울기만"], ["prec", "세차만"]]} />}>
      {rows.map(([nm, f, lo, hi, col], i) => (
        <g key={nm} opacity={lit(i) ? 1 : 0.35}>
          <text x="34" y={11 + i * 42} fontSize="9" fill={col}>{nm}</text>
          <path d={pth(lane(f, lo, hi, 15 + i * 42, 24, 800))} fill="none" stroke={col} strokeWidth="1.2" opacity="0.2" />
          <path d={pth(lane(f, lo, hi, 15 + i * 42, 24, tm))} fill="none" stroke={col} strokeWidth="1.4" />
        </g>
      ))}
      <text x="34" y="140" fontSize="9" fill={C.red}>북위 65° 의 여름 햇빛</text>
      <path d={pth(insPts(800))} fill="none" stroke={C.red} strokeWidth="1.4" opacity="0.2" />
      <path d={pth(insPts(tm))} fill="none" stroke={C.red} strokeWidth="1.8" />
      <line x1="34" x2="350" y1="199" y2="199" stroke={C.mut} />
      {[800, 600, 400, 200, 0].map((ka) => <line key={ka} x1={X(ka)} x2={X(ka)} y1="199" y2="203" stroke={C.mut} />)}
      {[800, 600, 400, 200, 0].map((ka) => <text key={"l" + ka} x={X(ka)} y="213" textAnchor={ka === 0 ? "end" : ka === 800 ? "start" : "middle"} fontSize="8.5" fill={C.mut}>{ka === 0 ? "지금" : `${ka / 10} 만 년 전`}</text>)}
    </Frame>
  );
}

/* ── 데이지 세계: 생명이 행성의 온도를 맞춘다 (왓슨 · 러브록 1983) ── */
const DW = (() => {
  const S = 917, q = 2.06e9, Ag = 0.5, Aw = 0.75, Ab = 0.25, gam = 0.3, beta = (T) => Math.max(0, 1 - 0.003265 * (295.65 - T) ** 2);
  let aw = 0.01, ab = 0.01;
  const rows = [];
  for (let i = 0; i <= 110; i++) {
    const L = 0.6 + i * 0.01;
    aw = Math.max(aw, 0.01); ab = Math.max(ab, 0.01);
    let Te = 0;
    for (let it = 0; it < 1500; it++) {
      const x = Math.max(0, 1 - aw - ab), A = x * Ag + aw * Aw + ab * Ab, Te4 = (S * L * (1 - A)) / SIG;
      Te = Te4 ** 0.25;
      const Tw = Math.max(0, q * (A - Aw) + Te4) ** 0.25, Tb = Math.max(0, q * (A - Ab) + Te4) ** 0.25;
      aw = Math.max(0.001, aw + 0.05 * aw * (x * beta(Tw) - gam));
      ab = Math.max(0.001, ab + 0.05 * ab * (x * beta(Tb) - gam));
    }
    rows.push({ L, T: Te - 273.15, bare: ((S * L * (1 - Ag)) / SIG) ** 0.25 - 273.15, aw: aw < 0.005 ? 0 : aw, ab: ab < 0.005 ? 0 : ab });
  }
  return rows;
})();
export function Daisy() {
  const clock = useClock({ period: 13, rest: 6 });
  const i = Math.min(DW.length - 1, Math.floor((clock.t / 12) * (DW.length - 1))), r = DW[i];
  const P = plot({ x0: 0.6, x1: 1.7, y0: -15, y1: 75, W: 360, H: 220, pad: [12, 12, 92, 34] });
  const Q = plot({ x0: 0.6, x1: 1.7, y0: 0, y1: 1, W: 360, H: 220, pad: [148, 12, 24, 34] });
  const seen = DW.slice(0, i + 1), b15 = DW[90];
  return (
    <Frame clock={clock} title="데이지 세계 — 생명이 행성의 온도를 맞춘다"
      read={<>태양이 점점 밝아지는 행성에 흰 데이지(햇빛을 반사)와 검은 데이지(햇빛을 흡수)가 산다 — 둘 다 22.5 ℃ 에서 가장 잘 자란다 · 햇빛 {fmt(r.L, 2)} 배: 행성 온도 <b>{fmt(r.T, 1)} ℃</b>(데이지가 없다면 {fmt(r.bare, 1)} ℃) · 흰 데이지 {fmt(r.aw * 100, 0)} %, 검은 데이지 {fmt(r.ab * 100, 0)} % · 추울 때는 검은 데이지가 퍼져 열을 모으고 더울 때는 흰 데이지가 퍼져 식힌다 — 햇빛이 두 배 넘게 바뀌는 동안 온도가 좁은 범위에 머무는 되먹임(러브록의 가이아 가설을 보이려고 만든 모형) · 너무 밝아지면 흰 데이지도 버티지 못하고 한꺼번에 무너진다</>}>
      <Axes p={P} xl="" yl="℃" grid={false} xt={[]} yt={[25, 50]} />
      <text x={P.l - 4} y={P.Y(0) + 3.5} textAnchor="end" fontSize="10" fill={C.mut}>0</text>
      <line x1={P.l} x2={P.r} y1={P.Y(22.5)} y2={P.Y(22.5)} stroke={C.green} strokeDasharray="4 3" strokeWidth="1" />
      <path d={P.poly(DW.map((q) => [q.L, q.bare]))} fill="none" stroke={C.mut} strokeWidth="1.4" strokeDasharray="5 3" />
      <path d={P.poly(DW.map((q) => [q.L, q.T]))} fill="none" stroke={C.red} strokeWidth="1.6" opacity="0.2" />
      <path d={P.poly(seen.map((q) => [q.L, q.T]))} fill="none" stroke={C.red} strokeWidth="2.2" />
      <circle cx={P.X(r.L)} cy={P.Y(r.T)} r="4" fill={C.red} />
      <Label x={P.X(b15.L) - 4} y={P.Y(b15.bare) - 7} size={9} color={C.mut} anchor="end">데이지가 없다면</Label>
      <Label x={P.X(1.12)} y={P.Y(22.5) - 4} size={9} color={C.green}>가장 좋은 22.5 ℃</Label>
      <rect x={Q.l} y={Q.t} width={Q.r - Q.l} height={Q.b - Q.t} fill="none" stroke={C.bd} />
      {i > 0 && <path d={Q.poly([...seen.map((q) => [q.L, q.ab]), ...seen.slice().reverse().map((q) => [q.L, 0])])} fill="#3a3a3a" fillOpacity="0.8" stroke={C.mut} strokeWidth="0.5" />}
      {i > 0 && <path d={Q.poly([...seen.map((q) => [q.L, q.ab + q.aw]), ...seen.slice().reverse().map((q) => [q.L, q.ab])])} fill="#ffffff" stroke={C.mut} strokeWidth="0.8" />}
      <text x={Q.l} y={Q.t - 5} fontSize="9" fill={C.mut}>데이지가 덮은 넓이(아래 검은 데이지 · 위 흰 데이지)</text>
      {[0.6, 1, 1.4].map((v) => <text key={v} x={Q.X(v)} y={Q.b + 12} textAnchor="middle" fontSize="8.5" fill={C.mut}>{fmt(v, 1)}</text>)}
      <text x={Q.r} y={Q.b + 12} textAnchor="end" fontSize="8.5" fill={C.ink}>햇빛 배율 →</text>
    </Frame>
  );
}
