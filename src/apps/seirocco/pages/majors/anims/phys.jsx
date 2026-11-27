// 물리 그림 — 포물선 운동(공기 저항) · 단진자(큰 진폭) · 1차원 충돌 · 진행파와 정상파 · 전하의 전기장 · 기체 분자의 속력 분포 · 상자 속 입자 · 빛 시계(시간 지연)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, fmt, clamp, rng, gauss, useClock } from "./kit.jsx";
import { rk4 } from "./ode.jsx";
import { contourPath } from "./mvc.jsx";

const G = 9.8;

/** 던진 물체 — b 는 선형 공기 저항(가속도 = −b × 속도). 저항이 있어도 닫힌 꼴로 풀린다 */
function flight(v0, th, b) {
  const vx0 = v0 * Math.cos(th), vy0 = v0 * Math.sin(th);
  if (!b) return { T: (2 * vy0) / G, top: (vy0 * vy0) / (2 * G), x: (t) => vx0 * t, y: (t) => vy0 * t - 0.5 * G * t * t, vx: () => vx0, vy: (t) => vy0 - G * t };
  const vt = G / b; // 종단 속력
  const x = (t) => (vx0 / b) * (1 - Math.exp(-b * t));
  const y = (t) => ((vy0 + vt) / b) * (1 - Math.exp(-b * t)) - vt * t;
  const vy = (t) => (vy0 + vt) * Math.exp(-b * t) - vt;
  let T = (2 * vy0) / G;
  for (let i = 0; i < 40; i++) T -= y(T) / vy(T); // 뉴턴법 — 진공의 비행시간에서 왼쪽으로 다가간다
  return { T, top: y(Math.log(1 + vy0 / vt) / b), x, y, vx: (t) => vx0 * Math.exp(-b * t), vy };
}

/* ── 포물선 운동: 가로는 등속, 세로는 등가속 — 공기 저항이 있으면 비대칭 ── */
export function Projectile({ p = {} }) {
  const [deg, setDeg] = useState(p.deg ?? 45);
  const [v0, setV0] = useState(p.v0 ?? 20);
  const [air, setAir] = useState(p.air ? "air" : "vac");
  const clock = useClock({ period: 5 });
  const b = air === "air" ? 0.3 : 0;
  const th = (deg * Math.PI) / 180;
  const F = flight(v0, th, b), V = flight(v0, th, 0), Cp = flight(v0, Math.PI / 2 - th, 0);
  const span = (v0 * v0) / G;
  const P = plot({ x0: 0, x1: 1.08 * span, y0: 0, y1: 0.56 * span, pad: [12, 12, 22, 30] });
  const path = (Fl, upto = Fl.T) => { const o = []; for (let i = 0; i <= 90; i++) { const s = (upto * i) / 90; o.push([Fl.x(s), Math.max(0, Fl.y(s))]); } return P.poly(o); };
  const tau = clamp(clock.t / 3.6, 0, 1) * F.T;
  const bx = P.X(F.x(tau)), by = P.Y(Math.max(0, F.y(tau)));
  const k = 44 / v0, vx = F.vx(tau), vy = F.vy(tau);
  const best = useMemo(() => {
    if (!b) return 45;
    let bd = 45, br = 0;
    for (let d = 10; d <= 80; d += 0.5) { const f = flight(v0, (d * Math.PI) / 180, b); const r = f.x(f.T); if (r > br) { br = r; bd = d; } }
    return bd;
  }, [v0, b]);
  const R = F.x(F.T), Rv = V.x(V.T);
  return (
    <Frame clock={clock} title="포물선 운동"
      read={b
        ? <>공기 저항(가속도 −0.3 × 속도)이 있으면 사거리 <b>{fmt(R, 1)} m</b> — 진공(점선) {fmt(Rv, 1)} m 의 {fmt((100 * R) / Rv, 0)} % · 올라갈 때보다 내려올 때가 가파르고, 가장 멀리 가는 각은 45° 보다 작은 <b>{fmt(best, 1)}°</b></>
        : <>비행시간 2v₀sin θ ÷ g = <b>{fmt(F.T, 2)} s</b> · 최고 높이 (v₀sin θ)² ÷ 2g = <b>{fmt(F.top, 1)} m</b> · 사거리 v₀²sin 2θ ÷ g = <b>{fmt(R, 1)} m</b> — 점선({90 - deg}°)도 사거리가 같다 · 가로 속도(파랑)는 그대로, 세로 속도(빨강)만 1 초에 9.8 m/s 씩 준다</>}
      controls={<>
        <Slider label="각도 θ" min={10} max={80} step={5} value={deg} onChange={setDeg} show={(v) => v + "°"} />
        <Slider label="v₀" min={10} max={25} step={1} value={v0} onChange={setV0} show={(v) => v + " m/s"} />
        <Seg value={air} onChange={setAir} options={[["vac", "진공"], ["air", "공기 저항"]]} />
      </>}>
      <Axes p={P} xl="x (m)" yl="y (m)" />
      <path d={path(b ? V : Cp)} fill="none" stroke={C.mut} strokeDasharray="4 4" strokeWidth="1.3" />
      <path d={path(F)} fill="none" stroke={C.sp} strokeWidth="1.2" opacity="0.4" />
      <path d={path(F, tau)} fill="none" stroke={C.sp} strokeWidth="2.6" />
      <Arrow x1={bx} y1={by} x2={bx + k * vx} y2={by} color={C.blue} w={1.6} />
      <Arrow x1={bx} y1={by} x2={bx} y2={by - k * vy} color={C.red} w={1.6} />
      <Arrow x1={bx} y1={by} x2={bx + k * vx} y2={by - k * vy} color={C.ink} w={2} />
      <circle cx={bx} cy={by} r="5.5" fill={C.gold} stroke={C.ink} strokeWidth="1" />
    </Frame>
  );
}

/** 제1종 완전 타원적분 K(k) — 산술기하평균 */
function ellipK(k) {
  let a = 1, g = Math.sqrt(1 - k * k);
  for (let i = 0; i < 24; i++) { const a1 = (a + g) / 2; g = Math.sqrt(a * g); a = a1; }
  return Math.PI / (2 * a);
}

/* ── 단진자: 진폭이 크면 주기가 길어진다 — 에너지는 그대로 ── */
export function Pendulum({ p = {} }) {
  const [amp, setAmp] = useState(p.amp ?? 30);
  const clock = useClock({ period: 10 });
  const w0 = 2.5, T0 = (2 * Math.PI) / w0, th0 = (amp * Math.PI) / 180;
  const sol = useMemo(() => rk4((t, [q, w]) => [w, -w0 * w0 * Math.sin(q)], [th0, 0], 0, 10, 1000), [th0]);
  const i = Math.min(1000, Math.round((clock.t / 10) * 1000));
  const q = sol[i][1];
  const T = (4 / w0) * ellipK(Math.sin(th0 / 2));
  const E = 1 - Math.cos(th0), Kf = E > 0 ? clamp((Math.cos(q) - Math.cos(th0)) / E, 0, 1) : 0;
  const px = 100, py = 22, L = 84;
  const bx = px + L * Math.sin(q), by = py + L * Math.cos(q);
  const P = plot({ x0: 0, x1: 10, y0: -100, y1: 100, pad: [14, 10, 22, 224] });
  const dg = (r) => (r * 180) / Math.PI;
  const arc = `M${(px - L * Math.sin(th0)).toFixed(1)} ${(py + L * Math.cos(th0)).toFixed(1)}A${L} ${L} 0 0 0 ${(px + L * Math.sin(th0)).toFixed(1)} ${(py + L * Math.cos(th0)).toFixed(1)}`;
  const BW = 120;
  return (
    <Frame clock={clock} title="단진자"
      read={<>θ″ = −(g/L) sin θ · 진폭 <b>{amp}°</b> 의 주기 <b>{fmt(T, 3)} s</b> — 작은 각 근사 2π√(L/g) = {fmt(T0, 3)} s 보다 <b>{fmt((T / T0 - 1) * 100, 1)} %</b> 길다 · 그래프: 실제 θ(실선)와 근사 θ₀cos ω₀t(점선) · 막대: 운동에너지 + 위치에너지 = 일정</>}
      controls={<Slider label="진폭 θ₀" min={5} max={90} step={5} value={amp} onChange={setAmp} show={(v) => v + "°"} />}>
      <line x1={px - 44} x2={px + 44} y1={py} y2={py} stroke={C.ink} strokeWidth="3" />
      <path d={arc} fill="none" stroke={C.bd} strokeWidth="1.3" strokeDasharray="3 3" />
      <line x1={px} y1={py} x2={px} y2={py + L + 12} stroke={C.bd} strokeDasharray="2 3" />
      <line x1={px} y1={py} x2={bx} y2={by} stroke={C.ink} strokeWidth="1.6" />
      <circle cx={bx} cy={by} r="8" fill={C.sp} />
      <text x="14" y="150" fontSize="10" fill={C.mut}>운동 K</text>
      <rect x="62" y="141" width={BW} height="11" rx="2" fill="none" stroke={C.bd} />
      <rect x="62" y="141" width={BW * Kf} height="11" rx="2" fill={C.red} opacity="0.8" />
      <text x="14" y="172" fontSize="10" fill={C.mut}>위치 U</text>
      <rect x="62" y="163" width={BW} height="11" rx="2" fill="none" stroke={C.bd} />
      <rect x="62" y="163" width={BW * (1 - Kf)} height="11" rx="2" fill={C.blue} opacity="0.8" />
      <text x="62" y="192" fontSize="10" fill={C.mut}>K + U = 늘 같은 길이</text>
      <Axes p={P} xl="t" yl="θ" yt={[-90, -45, 45, 90]} yfmt={(v) => v + "°"} />
      <path d={P.path((t) => amp * Math.cos(w0 * t))} fill="none" stroke={C.mut} strokeWidth="1.2" strokeDasharray="4 3" />
      <path d={P.poly(sol.slice(0, i + 1).map(([t, a]) => [t, dg(a)]))} fill="none" stroke={C.sp} strokeWidth="2.2" />
      <circle cx={P.X(sol[i][0])} cy={P.Y(dg(q))} r="3.5" fill={C.red} />
    </Frame>
  );
}

/* ── 1차원 충돌: 운동량은 언제나 보존, 운동에너지는 반발계수에 따라 ── */
export function Collision({ p = {} }) {
  const [m1, setM1] = useState(p.m1 ?? 2);
  const [m2, setM2] = useState(p.m2 ?? 1);
  const [e, setE] = useState(p.e ?? 1);
  const clock = useClock({ period: 6 });
  const u1 = 3, M = m1 + m2, pT = m1 * u1;
  const v1 = (pT - m2 * e * u1) / M, v2 = (pT + m1 * e * u1) / M;
  const w1 = 0.5 + 0.3 * m1, w2 = 0.5 + 0.3 * m2;
  const x1s = 0.3 + w1 / 2, x2s = 5.6;
  const tc = (x2s - w2 / 2 - (x1s + w1 / 2)) / u1;
  const tp = clock.t * 0.5, after = tp >= tc;
  const x1 = after ? x1s + u1 * tc + v1 * (tp - tc) : x1s + u1 * tp;
  const x2 = after ? x2s + v2 * (tp - tc) : x2s;
  const X = (x) => 10 + (x / 12) * 340, sc = 340 / 12;
  const K0 = 0.5 * m1 * u1 * u1, K1 = 0.5 * m1 * v1 * v1 + 0.5 * m2 * v2 * v2, lost = K0 - K1;
  const p1a = m1 * v1, p2a = m2 * v2;
  const z = 128, pPx = Math.min(180 / Math.max(pT, p2a + Math.max(0, p1a)), p1a < 0 ? 110 / -p1a : 1e9), kPx = 200 / K0;
  const blk = (x, w, m, col, v, name) => {
    const h = 16 + 6 * m, y = 84 - h;
    return (
      <g>
        <rect x={X(x - w / 2)} y={y} width={w * sc} height={h} rx="3" fill={col} opacity="0.85" />
        <text x={X(x)} y={y + h / 2 + 4} textAnchor="middle" fontSize="10" fill="#fff" fontWeight="800">{name}</text>
        {Math.abs(v) > 0.01 && <Arrow x1={X(x)} y1={y - 8} x2={X(x) + v * 10} y2={y - 8} color={col} w={1.8} />}
        <text x={X(x)} y={y - 14} textAnchor="middle" fontSize="9.5" fill={C.ink}>{fmt(v, 2)} m/s</text>
      </g>
    );
  };
  const row = (y, label, on, kids) => (
    <g opacity={on ? 1 : 0.35}>
      <text x="8" y={y + 8} fontSize="10" fill={C.mut}>{label}</text>
      <line x1={z} x2={z} y1={y - 3} y2={y + 13} stroke={C.mut} />
      {kids}
    </g>
  );
  return (
    <Frame clock={clock} title="1차원 충돌"
      read={<>운동량 합 m₁v₁ + m₂v₂ = <b>{fmt(pT, 2)} kg·m/s</b> — 충돌 전후 그대로 · 운동에너지 {fmt(K0, 2)} J → <b>{fmt(K1, 2)} J</b>{lost > 0.005 ? <> ({fmt(lost, 2)} J 이 열 · 소리 · 변형으로)</> : " (그대로 — 탄성 충돌)"} · 반발계수 e = {fmt(e, 1)}: 1 이면 탄성, 0 이면 붙어 버린다</>}
      controls={<>
        <Slider label="m₁" min={0.5} max={4} step={0.5} value={m1} onChange={(v) => { setM1(v); clock.reset(); }} show={(v) => fmt(v, 1) + " kg"} />
        <Slider label="m₂" min={0.5} max={4} step={0.5} value={m2} onChange={(v) => { setM2(v); clock.reset(); }} show={(v) => fmt(v, 1) + " kg"} />
        <Slider label="e" min={0} max={1} step={0.1} value={e} onChange={(v) => { setE(v); clock.reset(); }} />
      </>}>
      <line x1="10" x2="350" y1="85" y2="85" stroke={C.ink} strokeWidth="1.6" />
      {blk(x1, w1, m1, C.blue, after ? v1 : u1, "m₁")}
      {blk(x2, w2, m2, C.gold, after ? v2 : 0, "m₂")}
      {row(104, "운동량 · 전", !after, <>
        <rect x={z} y={104} width={pT * pPx} height="10" fill={C.blue} opacity="0.8" />
        <text x={z + pT * pPx + 4} y={113} fontSize="9.5" fill={C.ink}>{fmt(pT, 2)}</text>
      </>)}
      {row(124, "운동량 · 후", after, <>
        <rect x={Math.min(z, z + p1a * pPx)} y={124} width={Math.abs(p1a) * pPx} height="10" fill={C.blue} opacity="0.8" />
        <rect x={z + Math.max(0, p1a) * pPx} y={124} width={p2a * pPx} height="10" fill={C.gold} opacity="0.85" />
        <line x1={z + pT * pPx} x2={z + pT * pPx} y1={120} y2={138} stroke={C.ink} strokeWidth="2" />
        <text x={z + Math.max(pT, Math.max(0, p1a) + p2a) * pPx + 4} y={133} fontSize="9.5" fill={C.ink}>합 {fmt(pT, 2)}</text>
      </>)}
      {row(158, "에너지 · 전", !after, <>
        <rect x={z} y={158} width={K0 * kPx} height="10" fill={C.blue} opacity="0.8" />
        <text x={z + K0 * kPx - 2} y={155} fontSize="9.5" fill={C.ink} textAnchor="end">{fmt(K0, 2)} J</text>
      </>)}
      {row(178, "에너지 · 후", after, <>
        <rect x={z} y={178} width={0.5 * m1 * v1 * v1 * kPx} height="10" fill={C.blue} opacity="0.8" />
        <rect x={z + 0.5 * m1 * v1 * v1 * kPx} y={178} width={0.5 * m2 * v2 * v2 * kPx} height="10" fill={C.gold} opacity="0.85" />
        {lost > 0.005 && <rect x={z + K1 * kPx} y={178} width={lost * kPx} height="10" fill="none" stroke={C.red} strokeDasharray="3 2" />}
        {lost > 0.005 && <text x={z + K0 * kPx - 2} y={200} fontSize="9.5" fill={C.red} textAnchor="end">잃음 {fmt(lost, 2)} J</text>}
      </>)}
    </Frame>
  );
}

/* ── 파동: 진행파는 모양이 나아가고 매질은 제자리, 정상파는 두 진행파의 합 ── */
export function Wave({ p = {} }) {
  const [mode, setMode] = useState(p.mode || "stand");
  const [n, setN] = useState(p.n ?? 3);
  const clock = useClock({ period: 8 });
  const t = clock.t;
  const P = plot({ x0: 0, x1: 1, y0: -2.4, y1: 2.4, pad: [18, 16, 16, 16] });
  if (mode === "travel") {
    const lam = 0.4, f = 0.5, y = (x) => 1.4 * Math.sin(2 * Math.PI * (x / lam - f * t));
    const xc = lam * (((0.25 + f * t) % 1) + 1), ym = y(0.5), vm = -1.4 * 2 * Math.PI * f * Math.cos(2 * Math.PI * (0.5 / lam - f * t));
    return (
      <Frame clock={clock} title="진행파"
        read={<>y = A sin(kx − ωt) · 마루(초록 점)는 속력 v = fλ 로 오른쪽으로 가지만, 줄의 한 점(빨강)은 제자리에서 위아래로만 움직인다 — 파동이 나르는 것은 물질이 아니라 <b>에너지와 모양</b></>}
        controls={<Seg value={mode} onChange={setMode} options={[["travel", "진행파"], ["stand", "정상파"]]} />}>
        <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.bd} />
        <path d={P.path(y, 0, 1, 240)} fill="none" stroke={C.sp} strokeWidth="2.4" />
        <line x1={P.X(xc)} x2={P.X(Math.min(1, xc + lam))} y1={P.Y(2.05)} y2={P.Y(2.05)} stroke={C.mut} />
        <line x1={P.X(xc)} x2={P.X(xc)} y1={P.Y(1.6)} y2={P.Y(2.2)} stroke={C.mut} />
        {xc + lam <= 1 && <line x1={P.X(xc + lam)} x2={P.X(xc + lam)} y1={P.Y(1.6)} y2={P.Y(2.2)} stroke={C.mut} />}
        <Label x={P.X(Math.min(xc + lam / 2, 0.96))} y={P.Y(2.05) - 4} anchor="middle" size={11} color={C.ink} bg>λ</Label>
        <circle cx={P.X(xc)} cy={P.Y(1.4)} r="5" fill={C.green} />
        <line x1={P.X(0.5)} x2={P.X(0.5)} y1={P.Y(-1.9)} y2={P.Y(1.9)} stroke={C.red} strokeDasharray="2 3" opacity="0.6" />
        <circle cx={P.X(0.5)} cy={P.Y(ym)} r="5" fill={C.red} />
        <Arrow x1={P.X(0.5) + 10} y1={P.Y(ym)} x2={P.X(0.5) + 10} y2={P.Y(ym) - vm * 6} color={C.red} w={1.4} />
      </Frame>
    );
  }
  const k = n * Math.PI, w = 2 * Math.PI * 0.25 * n;
  const yr = (x) => Math.sin(k * x - w * t), yl = (x) => Math.sin(k * x + w * t);
  return (
    <Frame clock={clock} title="정상파와 배음"
      read={<>양 끝이 묶인 줄에는 반파장이 n 개 들어간다 → λₙ = 2L/n, fₙ = n × v/2L = <b>{n}f₁</b> · 마디(●) {n + 1}개, 배 {n}개 · 가는 점선 = 반대로 가는 두 진행파, 굵은 선 = 그 합 2A sin kx cos ωt — 제자리에서 흔들린다</>}
      controls={<>
        <Seg value={mode} onChange={setMode} options={[["travel", "진행파"], ["stand", "정상파"]]} />
        <Slider label="배음 n" min={1} max={6} value={n} onChange={setN} />
      </>}>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.bd} />
      <path d={P.path((x) => 2 * Math.sin(k * x), 0, 1, 240)} fill="none" stroke={C.bd} strokeDasharray="2 3" />
      <path d={P.path((x) => -2 * Math.sin(k * x), 0, 1, 240)} fill="none" stroke={C.bd} strokeDasharray="2 3" />
      <path d={P.path(yr, 0, 1, 240)} fill="none" stroke={C.blue} strokeWidth="1" strokeDasharray="4 3" opacity="0.7" />
      <path d={P.path(yl, 0, 1, 240)} fill="none" stroke={C.gold} strokeWidth="1" strokeDasharray="4 3" opacity="0.8" />
      <path d={P.path((x) => yr(x) + yl(x), 0, 1, 240)} fill="none" stroke={C.sp} strokeWidth="2.6" />
      {Array.from({ length: n + 1 }, (_, m) => <circle key={m} cx={P.X(m / n)} cy={P.Y(0)} r="4" fill={C.ink} />)}
      <rect x={P.X(0) - 6} y={P.Y(1)} width="6" height={P.Y(-1) - P.Y(1)} fill={C.mut} />
      <rect x={P.X(1)} y={P.Y(1)} width="6" height={P.Y(-1) - P.Y(1)} fill={C.mut} />
    </Frame>
  );
}

/* ── 전기장: 전기력선은 +에서 나와 −로, 등전위선과 늘 수직 ── */
const QS = {
  dipole: { q: [[-1, 0, 1], [1, 0, -1]], lv: [-1.6, -0.9, -0.45, 0, 0.45, 0.9, 1.6], name: "쌍극자 (+q 와 −q)" },
  like: { q: [[-1, 0, 1], [1, 0, 1]], lv: [1.35, 1.7, 2.1, 2.7, 3.5], name: "같은 부호 (+q 와 +q)" },
  single: { q: [[0, 0, 1]], lv: [0.45, 0.65, 1, 1.6], name: "점전하 하나 (+q)" },
};
const potAt = (Q, x, y) => Q.reduce((s, [a, b, q]) => s + q / Math.max(0.05, Math.hypot(x - a, y - b)), 0);
function eAt(Q, x, y) {
  let ex = 0, ey = 0;
  for (const [a, b, q] of Q) { const dx = x - a, dy = y - b, r2 = Math.max(0.0025, dx * dx + dy * dy), r3 = r2 * Math.sqrt(r2); ex += (q * dx) / r3; ey += (q * dy) / r3; }
  return [ex, ey];
}
function fieldLines(Q, P) {
  const out = [];
  for (const [a, b, q] of Q) {
    if (q < 0) continue;
    for (let k = 0; k < 14; k++) {
      const ang = (2 * Math.PI * (k + 0.5)) / 14;
      let x = a + 0.08 * Math.cos(ang), y = b + 0.08 * Math.sin(ang);
      const pts = [[x, y]];
      for (let s = 0; s < 420; s++) {
        const [ex, ey] = eAt(Q, x, y), m = Math.hypot(ex, ey) || 1;
        const [fx, fy] = eAt(Q, x + (0.015 * ex) / m, y + (0.015 * ey) / m), fm = Math.hypot(fx, fy) || 1;
        x += (0.03 * fx) / fm; y += (0.03 * fy) / fm;
        pts.push([x, y]);
        if (x < P.x0 - 0.3 || x > P.x1 + 0.3 || y < P.y0 - 0.3 || y > P.y1 + 0.3) break;
        if (Q.some(([c, d, qq]) => qq < 0 && Math.hypot(x - c, y - d) < 0.07)) break;
      }
      out.push(P.poly(pts));
    }
  }
  return out;
}
export function EField({ p = {} }) {
  const [cfg, setCfg] = useState(p.cfg || "dipole");
  const S = QS[cfg] || QS.dipole;
  const clock = useClock({ period: 6 });
  const P = plot({ x0: -2.6, x1: 2.6, y0: -1.52, y1: 1.52, pad: [12, 12, 12, 12] });
  const art = useMemo(() => ({
    lines: fieldLines(S.q, P),
    eq: S.lv.map((c) => contourPath(P, (x, y) => potAt(S.q, x, y), c, 64)),
  }), [cfg]); // eslint-disable-line react-hooks/exhaustive-deps
  const off = -((clock.t * 16) % 12);
  return (
    <Frame clock={clock} title="전하가 만드는 전기장"
      read={<>{S.name} · 실선 = 전기력선(흐르는 점선 방향 = 양전하가 받는 힘), 촘촘할수록 전기장이 세다 · 점선 = 등전위선(kq/r 의 합이 같은 곳) — 전기력선과 늘 직각, 그 위로 전하를 옮길 때는 일이 들지 않는다</>}
      controls={<Seg value={cfg} onChange={setCfg} options={[["dipole", "쌍극자"], ["like", "같은 부호"], ["single", "하나"]]} />}>
      {art.eq.map((d, i) => <path key={"e" + i} d={d} fill="none" stroke={C.green} strokeWidth="1" strokeDasharray="3 3" opacity="0.75" />)}
      {art.lines.map((d, i) => <path key={"l" + i} d={d} fill="none" stroke={C.mut} strokeWidth="1.1" />)}
      {art.lines.map((d, i) => <path key={"f" + i} d={d} fill="none" stroke={C.sp} strokeWidth="1.6" strokeDasharray="5 7" strokeDashoffset={off} />)}
      {S.q.map(([a, b, q], i) => (
        <g key={i}>
          <circle cx={P.X(a)} cy={P.Y(b)} r="10" fill={q > 0 ? C.red : C.blue} />
          <text x={P.X(a)} y={P.Y(b) + 4.5} textAnchor="middle" fontSize="14" fontWeight="800" fill="#fff">{q > 0 ? "+" : "−"}</text>
        </g>
      ))}
    </Frame>
  );
}

/* ── 기체 분자 운동: 온도 = 분자 운동에너지의 평균, 속력은 맥스웰-볼츠만 분포 ── */
const tri = (u, L) => L - Math.abs((((u % (2 * L)) + 2 * L) % (2 * L)) - L);
export function Maxwell({ p = {} }) {
  const [T, setT] = useState(p.T ?? 300);
  const clock = useClock({ period: 30 });
  const m = 4.65e-26, kB = 1.380649e-23;
  const a = Math.sqrt((kB * T) / m);
  const base = useMemo(() => { const r = rng(11); const o = []; for (let i = 0; i < 400; i++) o.push([gauss(r), gauss(r), gauss(r), r(), r()]); return o; }, []);
  const vp = Math.SQRT2 * a, vm = Math.sqrt(8 / Math.PI) * a, vr = Math.sqrt(3) * a;
  const nb = 40, bw = 2000 / nb, cnt = new Array(nb).fill(0);
  base.forEach(([x, y, z]) => { const i = Math.floor((a * Math.hypot(x, y, z)) / bw); if (i < nb) cnt[i]++; });
  const fmb = (v, s) => 4 * Math.PI * v * v * Math.pow(1 / (2 * Math.PI * s * s), 1.5) * Math.exp((-v * v) / (2 * s * s));
  const a100 = Math.sqrt((kB * 100) / m), top = 1.1 * fmb(Math.SQRT2 * a100, a100);
  const P = plot({ x0: 0, x1: 2000, y0: 0, y1: top, pad: [14, 10, 24, 176] });
  const bx = 10, by = 14, BW = 150, BH = 160, s = 0.07;
  return (
    <Frame clock={clock} title="기체 분자의 속력 분포"
      read={<>질소 분자, T = <b>{T} K</b> · 막대 = 분자 400 개의 속력, 곡선 = 맥스웰-볼츠만 분포 · 가장 흔한 속력 √(2kT/m) = <b style={{ color: C.green }}>{fmt(vp, 0)}</b> · 평균 √(8kT/πm) = <b style={{ color: C.gold }}>{fmt(vm, 0)}</b> · 제곱평균제곱근 √(3kT/m) = <b style={{ color: C.red }}>{fmt(vr, 0)}</b> m/s — 온도를 올리면 분포가 오른쪽으로 납작하게 퍼진다</>}
      controls={<Slider label="온도 T" min={100} max={1000} step={50} value={T} onChange={setT} show={(v) => v + " K"} />}>
      <rect x={bx} y={by} width={BW} height={BH} rx="4" fill={C.card} stroke={C.ink} strokeWidth="1.4" />
      {base.slice(0, 64).map(([gx, gy, gz, rx, ry], i) => {
        const sp = a * Math.hypot(gx, gy, gz), hue = 220 - 220 * clamp(sp / (2.2 * vp), 0, 1);
        return <circle key={i} cx={bx + 4 + tri(rx * (BW - 8) + a * gx * s * clock.t, BW - 8)} cy={by + 4 + tri(ry * (BH - 8) + a * gy * s * clock.t, BH - 8)} r="3" fill={`hsl(${hue.toFixed(0)} 70% 50%)`} />;
      })}
      <Axes p={P} xl="속력 (m/s)" yl="" yt={[]} xt={[500, 1000, 1500, 2000]} xfmt={(v) => fmt(v, 0)} />
      {cnt.map((c, i) => { const d = Math.min(top, c / (400 * bw)); return <rect key={i} x={P.X(i * bw) + 0.4} width={Math.max(0.5, P.X(bw) - P.X(0) - 0.8)} y={P.Y(d)} height={P.Y(0) - P.Y(d)} fill={C.sp} opacity="0.5" />; })}
      <path d={P.path((v) => fmb(v, a), 0, 2000, 200)} fill="none" stroke={C.ink} strokeWidth="2" />
      {[[vp, C.green], [vm, C.gold], [vr, C.red]].map(([v, c]) => <line key={c} x1={P.X(v)} x2={P.X(v)} y1={P.Y(0)} y2={P.Y(fmb(v, a))} stroke={c} strokeWidth="2" />)}
    </Frame>
  );
}

/* ── 상자 속 입자: 벽에서 ψ = 0 이라 정상파만 — 에너지가 n² 로 띄엄띄엄 ── */
export function QBox({ p = {} }) {
  const [n, setN] = useState(p.n ?? 2);
  const [mix, setMix] = useState(p.mix ? "mix" : "one");
  const clock = useClock({ period: 12 });
  const t = clock.t, om = (k) => (2 * Math.PI * k * k) / 12;
  const ps = (k, x) => Math.SQRT2 * Math.sin(k * Math.PI * x);
  const P = plot({ x0: 0, x1: 1, y0: -1.7, y1: 2.3, pad: [12, 14, 14, 140] });
  const re = mix === "mix" ? (x) => (ps(1, x) * Math.cos(om(1) * t) + ps(2, x) * Math.cos(om(2) * t)) / Math.SQRT2 : (x) => ps(n, x) * Math.cos(om(n) * t);
  const dens = mix === "mix"
    ? (x) => 0.5 * (ps(1, x) ** 2 + ps(2, x) ** 2 + 2 * ps(1, x) * ps(2, x) * Math.cos((om(2) - om(1)) * t))
    : (x) => ps(n, x) ** 2;
  const area = P.poly([[0, 0], ...Array.from({ length: 121 }, (_, i) => [i / 120, dens(i / 120)]), [1, 0]]);
  const EY = (E) => 204 - E * 7.1;
  const on = (k) => (mix === "mix" ? k <= 2 : k === n);
  return (
    <Frame clock={clock} title="상자 속 입자"
      read={mix === "mix"
        ? <>n = 1 과 2 를 반씩 겹친 상태 — 칠한 |ψ|² (찾을 확률 밀도)가 (E₂ − E₁)/h 의 진동수로 왼쪽 · 오른쪽을 오간다. 정해진 에너지 상태 하나는 멈춰 있고, <b>겹친 상태만 움직인다</b></>
        : <>Eₙ = n²h² ÷ 8mL² → n = {n}: <b>E₁ 의 {n * n} 배</b> · 벽에서 ψ = 0 이라 반파장 n 개 — 마디 {n - 1}개 · 칠한 |ψ|² 는 시간에 따라 변하지 않는다(정상상태), 가는 선은 출렁이는 ψ 의 실수부</>}
      controls={<>
        <Seg value={mix} onChange={setMix} options={[["one", "한 상태"], ["mix", "1 + 2 겹침"]]} />
        {mix === "one" && <Slider label="n" min={1} max={5} value={n} onChange={setN} />}
      </>}>
      <text x="10" y="16" fontSize="10" fill={C.mut}>에너지 Eₙ = n²E₁</text>
      <line x1="38" x2="38" y1="22" y2="206" stroke={C.mut} />
      {[1, 2, 3, 4, 5].map((k) => (
        <g key={k}>
          <line x1="40" x2="100" y1={EY(k * k)} y2={EY(k * k)} stroke={on(k) ? C.sp : C.bd} strokeWidth={on(k) ? 3 : 1.6} />
          <text x="32" y={EY(k * k) + 3.5} fontSize="10" textAnchor="end" fill={C.mut}>{k}</text>
          <text x="104" y={EY(k * k) + 3.5} fontSize="9.5" fill={on(k) ? C.ink : C.mut}>{k * k}E₁</text>
        </g>
      ))}
      <rect x={P.X(0) - 5} y={P.t} width="5" height={P.b - P.t} fill={C.mut} />
      <rect x={P.X(1)} y={P.t} width="5" height={P.b - P.t} fill={C.mut} />
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.bd} />
      <path d={area} fill={C.sp} opacity="0.28" />
      <path d={P.path(dens, 0, 1, 160)} fill="none" stroke={C.sp} strokeWidth="1.6" />
      <path d={P.path(re, 0, 1, 160)} fill="none" stroke={C.red} strokeWidth="1.4" />
      <Label x={P.r - 4} y={P.t + 12} anchor="end" size={10} color={C.sp} bg>칠한 곳 = |ψ|²</Label>
    </Frame>
  );
}

/* ── 빛 시계: 움직이는 시계의 빛은 비스듬히 더 먼 길 — 시간 지연 γ ── */
export function LightClock({ p = {} }) {
  const [beta, setB] = useState(p.beta ?? 0.6);
  const clock = useClock({ period: 24 });
  const g = 1 / Math.sqrt(1 - beta * beta), t = clock.t, H = 50, c = 50;
  const ph = (tt, per) => { const u = (((tt % per) + per) % per) / per; return u < 0.5 ? u * 2 : 2 - u * 2; };
  const top1 = 26, top2 = 124, rx = 62;
  const run = 270, xs = (s) => 40 + beta * c * s, wrap = Math.floor((beta * c * t) / run);
  const mx = xs(t) - wrap * run;
  const trail = [];
  for (let s = Math.max(0, t - 2.4 * g); s <= t + 1e-9; s += 0.04) {
    if (Math.floor((beta * c * s) / run) !== wrap) continue;
    trail.push([xs(s) - wrap * run, top2 + H - H * ph(s, 2 * g)]);
  }
  const mirror = (x, y) => <rect x={x - 16} y={y - 3} width="32" height="4" rx="1" fill={C.ink} />;
  return (
    <Frame clock={clock} title="빛 시계와 시간 지연"
      read={<>움직이는 시계(아래)의 빛은 비스듬히 더 먼 길을 간다 — 빛의 속력은 누구에게나 c 이므로 한 번 똑딱이 γ 배 길다 · β = v/c = <b>{fmt(beta, 2)}</b>: γ = 1/√(1 − β²) = <b>{fmt(g, 3)}</b> · 정지 시계가 10 번 똑딱일 때 움직이는 시계는 {fmt(10 / g, 1)} 번</>}
      controls={<Slider label="β = v/c" min={0.1} max={0.95} step={0.05} value={beta} onChange={(v) => { setB(v); clock.reset(); }} />}>
      <text x="10" y="16" fontSize="10" fill={C.mut}>정지한 시계</text>
      {mirror(rx, top1)}{mirror(rx, top1 + H)}
      <line x1={rx} x2={rx} y1={top1} y2={top1 + H} stroke={C.gold} strokeDasharray="2 3" />
      <circle cx={rx} cy={top1 + H - H * ph(t, 2)} r="4.5" fill={C.gold} />
      <text x="140" y="56" fontSize="12" fill={C.ink}>똑딱 <tspan fontWeight="800">{Math.floor(t / 2)}</tspan> 번</text>
      <line x1="8" x2="352" y1="96" y2="96" stroke={C.bd} />
      <text x="10" y="114" fontSize="10" fill={C.mut}>v = βc 로 움직이는 시계 →</text>
      <path d={trail.length > 1 ? trail.map(([x, y], i) => (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1)).join("") : "M0 0"} fill="none" stroke={C.gold} strokeWidth="1.3" strokeDasharray="2 2" />
      {mirror(mx, top2)}{mirror(mx, top2 + H)}
      <circle cx={mx} cy={top2 + H - H * ph(t, 2 * g)} r="4.5" fill={C.gold} />
      <text x="140" y="204" fontSize="12" fill={C.ink}>똑딱 <tspan fontWeight="800">{Math.floor(t / (2 * g))}</tspan> 번</text>
    </Frame>
  );
}
