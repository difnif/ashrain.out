// 천문우주 그림 — 케플러 제2법칙 · 뉴턴의 대포(원궤도 · 탈출) · 호만 전이 · 로켓 방정식과 다단 · 연주시차 · 흑체복사 · 행성 통과 · 팽창하는 우주
import { useId, useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, fmt, clamp, rng, useClock } from "./kit.jsx";
import { rk4 } from "./ode.jsx";

/** 케플러 방정식 M = E − e sin E 를 뉴턴법으로 */
export function keplerE(M, e) {
  let E = e < 0.8 ? M : Math.PI;
  for (let i = 0; i < 40; i++) E -= (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
  return E;
}

/* ── 케플러 제2법칙: 같은 시간에 같은 넓이 — 가까울 때 빠르다 ── */
export function Kepler({ p = {} }) {
  const [e, setE] = useState(p.e ?? 0.5);
  const clock = useClock({ period: 12 });
  const A = 104, B = A * Math.sqrt(1 - e * e), sx = 180 + A * e, sy = 110;
  const at = (M) => { const E = keplerE(M, e); return [sx + A * (Math.cos(E) - e), sy - B * Math.sin(E), E]; };
  const M = ((2 * Math.PI * clock.t) / 12) % (2 * Math.PI), seg = (2 * Math.PI) / 12, kNow = Math.floor(M / seg);
  const sector = (m0, m1) => { let d = `M${sx} ${sy}`; for (let i = 0; i <= 16; i++) { const [x, y] = at(m0 + ((m1 - m0) * i) / 16); d += `L${x.toFixed(1)} ${y.toFixed(1)}`; } return d + "Z"; };
  const [px, py, E] = at(M);
  const r = 1 - e * Math.cos(E), v = Math.sqrt(2 / r - 1);
  const tx = -A * Math.sin(E), ty = -B * Math.cos(E), tl = Math.hypot(tx, ty) || 1;
  return (
    <Frame clock={clock} title="케플러 제2법칙"
      read={<>같은 시간(주기의 1/12)마다 태양과 행성을 잇는 선이 쓸고 가는 넓이(부채꼴)가 모두 같다 — 각운동량 보존 · 이심률 e = <b>{fmt(e, 2)}</b>: 근일점 속력 ÷ 원일점 속력 = (1 + e)/(1 − e) = <b>{fmt((1 + e) / (1 - e), 2)}</b> · 지금 거리 {fmt(r, 2)}a, 속력 {fmt(v, 2)} (긴반지름 a 인 원궤도의 속력을 1 로)</>}
      controls={<Slider label="이심률 e" min={0} max={0.85} step={0.05} value={e} onChange={setE} />}>
      {Array.from({ length: 12 }, (_, k) => <path key={k} d={sector(k * seg, (k + 1) * seg)} fill={k % 2 ? C.sp : C.gold} opacity={k === kNow ? 0.12 : 0.16} />)}
      <path d={sector(kNow * seg, M)} fill={C.red} opacity="0.35" />
      <ellipse cx={180} cy={sy} rx={A} ry={B} fill="none" stroke={C.ink} strokeWidth="1.4" />
      <circle cx={sx} cy={sy} r="9" fill={C.gold} />
      <circle cx={180 - A * e} cy={sy} r="2" fill={C.mut} />
      <text x={180 + A + 4} y={sy + 4} fontSize="10" fill={C.mut}>근일점</text>
      <text x={180 - A - 4} y={sy + 4} fontSize="10" fill={C.mut} textAnchor="end">원일점</text>
      <line x1={sx} y1={sy} x2={px} y2={py} stroke={C.red} strokeWidth="1.2" />
      <Arrow x1={px} y1={py} x2={px + (tx / tl) * 26 * v} y2={py + (ty / tl) * 26 * v} color={C.blue} w={1.8} />
      <circle cx={px} cy={py} r="6" fill={C.blue} />
    </Frame>
  );
}

/* ── 뉴턴의 대포: 충분히 빠르면 떨어지면서도 땅에 닿지 않는다 ── */
export function Cannon({ p = {} }) {
  const [v, setV] = useState(p.v ?? 1);
  const clock = useClock({ period: 12 });
  const r0 = 1.12, vc = Math.sqrt(1 / r0), Tc = 2 * Math.PI * Math.pow(r0, 1.5);
  const tr = useMemo(() => {
    const dt = 0.01, pts = [[-r0, 0]]; let s = [-r0, 0, 0, v * vc], hit = false, t = 0;
    const f = (tt, [x, y, u, w]) => { const rr = Math.hypot(x, y), r3 = rr * rr * rr; return [u, w, -x / r3, -y / r3]; };
    while (t < 2.4 * Tc) {
      s = rk4(f, s, t, t + dt, 1)[1].slice(1); t += dt;
      pts.push([s[0], s[1]]);
      const rr = Math.hypot(s[0], s[1]);
      if (rr < 1) { hit = true; break; }
      if (rr > 12) break;
    }
    return { pts, hit, dt };
  }, [v]); // eslint-disable-line react-hooks/exhaustive-deps
  const cx = 100, cy = 110, S = 56;
  const k = Math.min(tr.pts.length - 1, Math.floor(((clock.t * Tc) / 5) / tr.dt));
  const [bx, by] = tr.pts[k];
  const kind = tr.hit ? "땅에 떨어진다 — 그래도 타원 궤도의 일부를 따라 떨어지는 중" : Math.abs(v - 1) < 0.001 ? "원궤도 — 떨어지는 만큼 땅이 둥글게 멀어진다" : v < 1 ? "타원 궤도 — 쏜 곳이 가장 먼 점(원지점)" : v < Math.SQRT2 - 1e-9 ? "타원 궤도 — 쏜 곳이 가장 가까운 점(근지점)" : "탈출 — 돌아오지 않는다(포물선 · 쌍곡선)";
  return (
    <Frame clock={clock} title="뉴턴의 대포"
      read={<>산꼭대기에서 수평으로 쏜 대포알(뉴턴의 사고 실험) · 속력 = 그 높이의 원궤도 속력 √(GM/r) 의 <b>{fmt(v, 2)} 배</b> → <b>{kind}</b> · √2 배(약 1.41)를 넘으면 탈출 — 지표 근처에서 원궤도 7.9 km/s, 탈출 11.2 km/s</>}
      controls={<Slider label="속력 ÷ 원궤도 속력" min={0.5} max={1.5} step={0.02} value={v} onChange={(x) => { setV(x); clock.reset(); }} />}>
      <circle cx={cx} cy={cy} r={S} fill={C.blue} opacity="0.22" stroke={C.blue} strokeWidth="1.4" />
      <polygon points={`${cx - S - 1},${cy - 9} ${cx - S - 1},${cy + 9} ${cx - r0 * S + 1},${cy}`} fill={C.mut} />
      <circle cx={cx} cy={cy} r={r0 * S} fill="none" stroke={C.bd} strokeDasharray="2 4" />
      <path d={tr.pts.map(([x, y], i) => (i % 3 && i !== tr.pts.length - 1 ? "" : (i ? "L" : "M") + (cx + x * S).toFixed(1) + " " + (cy - y * S).toFixed(1))).join("")} fill="none" stroke={C.sp} strokeWidth="1.3" opacity="0.5" />
      <path d={tr.pts.slice(0, k + 1).map(([x, y], i) => (i % 2 && i !== k ? "" : (i ? "L" : "M") + (cx + x * S).toFixed(1) + " " + (cy - y * S).toFixed(1))).join("")} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <circle cx={cx + bx * S} cy={cy - by * S} r="4.5" fill={tr.hit && k === tr.pts.length - 1 ? C.red : C.ink} />
      <text x={cx} y={cy + 4} textAnchor="middle" fontSize="11" fill={C.blue}>지구</text>
    </Frame>
  );
}

/* ── 호만 전이: 두 번 가속하고 반 바퀴 타원을 탄다 ── */
export function Hohmann({ p = {} }) {
  const [k, setK] = useState(p.k ?? 3);
  const clock = useClock({ period: 11 });
  const R2 = 92, R1 = R2 / k, cx = 116, cy = 110;
  const a = (R1 + R2) / 2, e = (R2 - R1) / (R2 + R1), b = a * Math.sqrt(1 - e * e);
  const t = clock.t;
  let x, y, phase;
  if (t < 2.5) { const th = (2 * Math.PI * t) / 2.5; x = cx + R1 * Math.cos(th); y = cy - R1 * Math.sin(th); phase = 0; }
  else if (t < 7.5) { const E = keplerE((Math.PI * (t - 2.5)) / 5, e); x = cx + a * (Math.cos(E) - e); y = cy - b * Math.sin(E); phase = 1; }
  else { const th = Math.PI + (Math.PI / 5) * Math.pow(a / R2, 1.5) * (t - 7.5); x = cx + R2 * Math.cos(th); y = cy - R2 * Math.sin(th); phase = 2; }
  const d1 = Math.sqrt((2 * k) / (1 + k)) - 1, d2 = Math.sqrt(1 / k) * (1 - Math.sqrt(2 / (1 + k))), tr = 0.5 * Math.pow((1 + k) / 2, 1.5);
  let half = ""; for (let i = 0; i <= 60; i++) { const E = (Math.PI * i) / 60; half += (i ? "L" : "M") + (cx + a * (Math.cos(E) - e)).toFixed(1) + " " + (cy - b * Math.sin(E)).toFixed(1); }
  return (
    <Frame clock={clock} title="호만 전이 궤도"
      read={<>안쪽 원(r₁)에서 한 번 가속 → 반 바퀴 타원(긴반지름 (r₁ + r₂)/2) → 바깥 원(r₂)에서 한 번 더 가속 · r₂/r₁ = <b>{fmt(k, 2)}</b>: Δv₁ = {fmt(d1, 3)}v₁, Δv₂ = {fmt(d2, 3)}v₁, 합 <b>{fmt(d1 + d2, 3)}v₁</b> (고도 300 km 의 v₁ = 7.73 km/s 로 치면 {fmt(7.726 * (d1 + d2), 2)} km/s) · 걸리는 시간 = 안쪽 궤도 주기의 {fmt(tr, 2)} 배</>}
      controls={<Slider label="r₂/r₁" min={1.5} max={8} step={0.1} value={k} onChange={(v) => { setK(v); clock.reset(); }} />}>
      <circle cx={cx} cy={cy} r={Math.max(3, R1 * 0.45)} fill={C.blue} opacity="0.5" />
      <circle cx={cx} cy={cy} r={R1} fill="none" stroke={C.mut} strokeWidth="1.3" />
      <circle cx={cx} cy={cy} r={R2} fill="none" stroke={C.mut} strokeWidth="1.3" />
      <path d={half} fill="none" stroke={C.gold} strokeWidth="1.6" strokeDasharray="5 3" />
      <Arrow x1={cx + R1} y1={cy + 6} x2={cx + R1} y2={cy - 18} color={phase === 0 && t > 2.1 ? C.red : C.mut} w={2} />
      <text x={cx + R1 + 5} y={cy - 8} fontSize="10" fill={C.red}>Δv₁</text>
      <Arrow x1={cx - R2} y1={cy - 6} x2={cx - R2} y2={cy + 18} color={phase === 1 && t > 7.1 ? C.red : C.mut} w={2} />
      <text x={cx - R2 + 5} y={cy + 16} fontSize="10" fill={C.red}>Δv₂</text>
      <circle cx={x} cy={y} r="5" fill={C.red} stroke={C.ink} />
      <text x="232" y="40" fontSize="11" fill={C.ink}>{["① 안쪽 원궤도", "② 전이 타원 (반 바퀴)", "③ 바깥 원궤도"][phase]}</text>
      <text x="232" y="60" fontSize="10" fill={C.mut}>점화 두 번이면 끝 —</text>
      <text x="232" y="74" fontSize="10" fill={C.mut}>나머지는 중력이 데려다준다</text>
    </Frame>
  );
}

/* ── 로켓 방정식: Δv = vₑ ln(m₀/m₁) — 빈 통을 버리면(다단) 더 멀리 ── */
export function Rocket({ p = {} }) {
  const [st, setSt] = useState(p.stages === 1 ? "one" : "two");
  const [ve, setVe] = useState(p.ve ?? 3);
  const clock = useClock({ period: 10 });
  const dv1 = (b) => ve * Math.log(100 / (100 - b));
  const dv2 = (b) => (b <= 63 ? ve * Math.log(100 / (100 - b)) : ve * (Math.log(100 / 37) + Math.log(30 / (30 - (b - 63)))));
  const fin1 = ve * Math.log(100 / 15), fin2 = ve * (Math.log(100 / 37) + Math.log(30 / 8));
  const burn = 85 * clamp(clock.t / 8, 0, 1), two = st === "two";
  const P = plot({ x0: 0, x1: 85, y0: 0, y1: 4.8 * 2.4, pad: [14, 12, 24, 130] });
  // 로켓 그림(세로 막대) — 질량을 높이로
  const hpx = 1.6, X0 = 28, W = 34;
  const parts = two
    ? [["탑재체", 5, C.ink], ["2단 구조", 3, C.mut], ["2단 연료", burn > 63 ? 22 - (burn - 63) : 22, C.gold], ["1단 구조", burn > 63 ? 0 : 7, C.mut], ["1단 연료", burn > 63 ? 0 : 63 - burn, C.red]]
    : [["탑재체", 5, C.ink], ["구조", 10, C.mut], ["연료", 85 - burn, C.red]];
  let yy = 18;
  const bars = parts.map(([n, m, col]) => { const h = m * hpx, el = m > 0.01 ? <rect key={n} x={X0} y={yy} width={W} height={h} fill={col} opacity="0.85" stroke={C.card} strokeWidth="0.6" /> : null; yy += h; return el; });
  const cur = two ? dv2(burn) : dv1(burn);
  return (
    <Frame clock={clock} title="로켓 방정식과 다단 로켓"
      read={<>Δv = vₑ ln(m₀/m₁) · 1단: 100 t → 15 t, 최종 Δv = <b>{fmt(fin1, 2)} km/s</b> · 2단: 100 → 37 t 에서 빈 1단(7 t)을 버리고 30 → 8 t, 최종 Δv = <b>{fmt(fin2, 2)} km/s</b> ({fmt((fin2 / fin1 - 1) * 100, 0)} % 더) · 지금 {fmt(burn, 0)} t 태움: Δv = {fmt(cur, 2)} km/s · 저궤도에는 약 9.4 km/s 가 든다</>}
      controls={<>
        <Seg value={st} onChange={(v) => { setSt(v); clock.reset(); }} options={[["one", "1단"], ["two", "2단"]]} />
        <Slider label="배기 속도 vₑ" min={2} max={4.5} step={0.1} value={ve} onChange={setVe} show={(v) => fmt(v, 1) + " km/s"} />
      </>}>
      <polygon points={`${X0},18 ${X0 + W / 2},4 ${X0 + W},18`} fill={C.ink} />
      {bars}
      {two && burn > 63 && <rect x={X0 + 6} y={yy + 12 + (burn - 63) * 2} width={W - 12} height={7 * hpx} fill={C.mut} opacity={Math.max(0, 0.7 - (burn - 63) / 30)} />}
      <text x="8" y="196" fontSize="9" fill={C.mut}>{two ? "탑재 5 · 구조 3+7 t" : "탑재 5 · 구조 10 t"}</text>
      <text x="8" y="208" fontSize="9" fill={C.mut}>연료 {two ? "22+63" : "85"} t</text>
      <Axes p={P} xl="태운 연료 (t)" yl="Δv (km/s)" />
      <line x1={P.l} x2={P.r} y1={P.Y(9.4)} y2={P.Y(9.4)} stroke={C.green} strokeDasharray="4 3" />
      <Label x={P.l + 4} y={P.Y(9.4) - 4} size={9.5} color={C.green} bg>저궤도 9.4</Label>
      <path d={P.path(dv1, 0, 85, 120)} fill="none" stroke={two ? C.bd : C.sp} strokeWidth={two ? 1.4 : 2.4} strokeDasharray={two ? "4 3" : undefined} />
      <path d={P.path(dv2, 0, 85, 200)} fill="none" stroke={two ? C.sp : C.bd} strokeWidth={two ? 2.4 : 1.4} strokeDasharray={two ? undefined : "4 3"} />
      <circle cx={P.X(burn)} cy={P.Y(cur)} r="4.5" fill={C.red} />
      {two && <line x1={P.X(63)} x2={P.X(63)} y1={P.Y(0)} y2={P.Y(dv2(63))} stroke={C.mut} strokeDasharray="2 3" />}
    </Frame>
  );
}

/* ── 연주시차: 지구가 돌면 가까운 별이 먼 별을 배경으로 오간다 ── */
export function Parallax({ p = {} }) {
  const [d, setD] = useState(p.d ?? 4);
  const clock = useClock({ period: 8 });
  const th = (2 * Math.PI * clock.t) / 8, sx = 44, syy = 110, R = 26;
  const ex = sx + R * Math.cos(th), ey = syy - R * Math.sin(th);
  const stx = sx + 50 + 15 * d, sty = syy, bgx = 252, G = 150;
  // 보이는 방향(기울기) → 하늘 그림의 높이. 먼 별들은 무한히 멀어 방향이 바뀌지 않는다
  const sky = (xE, yE) => 110 + (G * (sty - yE)) / (stx - xE);
  const ys = sky(ex, ey), yTop = sky(sx, syy - R), yBot = sky(sx, syy + R);
  const ray = ey + ((sty - ey) * (bgx - ex)) / (stx - ex);
  const bg = rng(9), stars = Array.from({ length: 9 }, () => [272 + bg() * 76, 34 + bg() * 164]);
  return (
    <Frame clock={clock} title="연주시차"
      read={<>지구가 태양을 한 바퀴 도는 동안 가까운 별이 먼 별들을 배경으로 오간다 — 오가는 폭의 절반이 <b>연주시차 p</b> · 거리 d = <b>{fmt(d, 1)} pc</b> → p = 1/d = <b>{fmt(1 / d, 3)}″</b> (그림은 크게 과장 — 실제로는 가장 가까운 별도 1″ 가 안 된다) · 1 pc ≈ 3.26 광년 ≈ 206 265 AU</>}
      controls={<Slider label="별까지 거리" min={1} max={10} step={0.5} value={d} onChange={setD} show={(v) => fmt(v, 1) + " pc"} />}>
      <circle cx={sx} cy={syy} r={R} fill="none" stroke={C.bd} strokeDasharray="3 3" />
      <circle cx={sx} cy={syy} r="7" fill={C.gold} />
      <circle cx={ex} cy={ey} r="4.5" fill={C.blue} />
      <line x1={ex} y1={ey} x2={bgx} y2={ray} stroke={C.blue} strokeWidth="1" opacity="0.6" />
      <circle cx={stx} cy={sty} r="5" fill={C.red} />
      <text x={stx} y={sty - 10} textAnchor="middle" fontSize="10" fill={C.red}>가까운 별</text>
      <rect x="262" y="14" width="94" height="192" rx="6" fill={C.card} stroke={C.bd} />
      <text x="309" y="28" textAnchor="middle" fontSize="9.5" fill={C.mut}>하늘에서 본 모습</text>
      {stars.map(([x, y], i) => <circle key={i} cx={x} cy={y} r="1.6" fill={C.mut} />)}
      <line x1="309" x2="309" y1={yTop} y2={yBot} stroke={C.red} strokeWidth="1" strokeDasharray="2 2" />
      <circle cx="309" cy={ys} r="5" fill={C.red} />
      <text x="8" y="160" fontSize="9.5" fill={C.mut}>태양 · 지구 궤도(1 AU)</text>
    </Frame>
  );
}

/* ── 흑체복사: 뜨거울수록 봉우리가 짧은 파장으로(빈), 전체 세기는 T⁴(슈테판-볼츠만) ── */
function kelvinRGB(T) {
  const t = T / 100; let r, g, b;
  if (t <= 66) { r = 255; g = 99.4708025861 * Math.log(t) - 161.1195681661; b = t <= 19 ? 0 : 138.5177312231 * Math.log(t - 10) - 305.0447927307; }
  else { r = 329.698727446 * Math.pow(t - 60, -0.1332047592); g = 288.1221695283 * Math.pow(t - 60, -0.0755148492); b = 255; }
  const c = (v) => Math.round(clamp(v, 0, 255));
  return `rgb(${c(r)},${c(g)},${c(b)})`;
}
export function Blackbody({ p = {} }) {
  const [T, setT] = useState(p.T ?? 3500);
  const clock = useClock({ period: 10 });
  const gid = "bb" + useId().replace(/[^a-zA-Z0-9]/g, "");
  const B = (l, TT) => 1 / (Math.pow(l / 1000, 5) * (Math.exp(1.4388e7 / (l * TT)) - 1)); // l: nm
  const Ts = 5778, peak = (TT) => 2.898e6 / TT;
  const top = Math.max(B(peak(T), T), B(peak(Ts), Ts)) * 1.12;
  const P = plot({ x0: 100, x1: 2500, y0: 0, y1: top, pad: [14, 12, 34, 22] });
  const lm = peak(T), sweep = 100 + 2400 * (0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10));
  const rr = B(sweep, T) / B(sweep, Ts);
  const rtxt = rr < 0.001 ? "1/1000 도 안 된다" : fmt(rr, rr < 0.1 ? 3 : rr < 10 ? 2 : 0) + " 배";
  const vis = [[380, "#7b4fc9"], [450, "#3b6fd8"], [500, "#2fa3b8"], [550, "#4cae4c"], [580, "#e0c33b"], [610, "#e8892f"], [700, "#c9372c"]];
  return (
    <Frame clock={clock} title="흑체복사"
      read={<>플랑크 곡선, T = <b>{T} K</b> · 빈 법칙 λₘₐₓ = 2.898 × 10⁶ nm·K ÷ T = <b>{fmt(lm, 0)} nm</b> · 슈테판-볼츠만: 표면 1 m² 가 내는 세기는 T⁴ 에 비례 — 태양(점선, 5778 K)의 <b>{fmt((T / Ts) ** 4, 2)} 배</b> · 오른쪽 위 = 이 온도의 별 색 · 세로선 파장 {fmt(sweep, 0)} nm 에서 이 별의 세기는 태양의 {rtxt} — 뜨거울수록 모든 파장에서 더 밝다(곡선끼리 만나지 않는다)</>}
      controls={<Slider label="온도 T" min={2500} max={12000} step={100} value={T} onChange={setT} show={(v) => v + " K"} />}>
      <defs>
        <linearGradient id={gid} x1="0" x2="1" y1="0" y2="0">
          {vis.map(([l, c]) => <stop key={l} offset={(l - 380) / 320} stopColor={c} />)}
        </linearGradient>
      </defs>
      <rect x={P.X(380)} y={P.b + 17} width={P.X(700) - P.X(380)} height="6" fill={`url(#${gid})`} />
      <text x={P.X(700) + 5} y={P.b + 23.5} fontSize="9" fill={C.mut}>보이는 빛</text>
      <Axes p={P} xl="파장 (nm)" yl="" yt={[]} xt={[500, 1000, 1500, 2000, 2500]} xfmt={(v) => fmt(v, 0)} />
      <path d={P.path((l) => B(l, Ts), 100, 2500, 300)} fill="none" stroke={C.gold} strokeWidth="1.4" strokeDasharray="4 3" />
      <path d={P.path((l) => B(l, T), 100, 2500, 300)} fill="none" stroke={C.red} strokeWidth="2.6" />
      <line x1={P.X(lm)} x2={P.X(lm)} y1={P.Y(0)} y2={P.Y(B(lm, T))} stroke={C.red} strokeDasharray="2 3" />
      <line x1={P.X(sweep)} x2={P.X(sweep)} y1={P.t} y2={P.b} stroke={C.mut} strokeWidth="0.8" opacity="0.6" />
      <circle cx={P.X(sweep)} cy={P.Y(B(sweep, T))} r="3.5" fill={C.red} />
      <circle cx="326" cy="40" r="18" fill={kelvinRGB(T)} stroke={C.bd} />
      <Label x={P.X(lm) + 4} y={P.Y(B(lm, T)) - 6} size={10} color={C.red} bg>λₘₐₓ</Label>
    </Frame>
  );
}

/* ── 행성 통과: 가린 넓이만큼 어두워진다 — 깊이 ≈ (Rₚ/Rₛ)² ── */
function overlap(d, R, r) {
  if (d >= R + r) return 0;
  if (d <= R - r) return Math.PI * r * r;
  const a = r * r * Math.acos(clamp((d * d + r * r - R * R) / (2 * d * r), -1, 1));
  const b = R * R * Math.acos(clamp((d * d + R * R - r * r) / (2 * d * R), -1, 1));
  return a + b - 0.5 * Math.sqrt(Math.max(0, (-d + r + R) * (d + r - R) * (d - r + R) * (d + r + R)));
}
export function Transit({ p = {} }) {
  const [k, setK] = useState(p.k ?? 0.1);
  const clock = useClock({ period: 9 });
  const scx = 180, scy = 58, Rs = 44, rp = k * Rs, by = scy + 0.3 * Rs;
  const xa = scx - Rs - rp - 50, xb = scx + Rs + rp + 50;
  const xp = xa + (xb - xa) * clamp(clock.t / 8, 0, 1);
  const flux = (x) => 1 - overlap(Math.hypot(x - scx, by - scy), Rs, rp) / (Math.PI * Rs * Rs);
  const depth = k * k;
  const P = plot({ x0: xa, x1: xb, y0: 1 - depth * 1.5 - 0.002, y1: 1 + depth * 0.25 + 0.001, pad: [122, 12, 18, 52] });
  return (
    <Frame clock={clock} title="행성 통과(트랜짓)"
      read={<>행성이 별 앞을 지나면 가린 넓이만큼 어두워진다 — 깊이 ≈ (Rₚ/Rₛ)² = <b>{fmt(depth * 100, 3)} %</b> · 목성 크기(0.1)면 1 %, 지구 크기(0.009)면 0.008 % — 그래서 지구형 행성은 우주망원경으로 찾는다 · 통과가 되풀이되는 간격이 공전주기, 케플러 제3법칙으로 궤도 크기까지 나온다</>}
      controls={<Slider label="Rₚ/Rₛ" min={0.03} max={0.25} step={0.01} value={k} onChange={(v) => { setK(v); clock.reset(); }} />}>
      <circle cx={scx} cy={scy} r={Rs} fill={C.gold} opacity="0.85" />
      <circle cx={scx} cy={scy} r={Rs} fill="none" stroke={C.gold} strokeWidth="3" opacity="0.4" />
      <line x1={xa} x2={xb} y1={by} y2={by} stroke={C.mut} strokeDasharray="2 4" opacity="0.6" />
      <circle cx={xp} cy={by} r={Math.max(1.5, rp)} fill={C.ink} />
      <line x1={P.l} x2={P.r} y1={P.Y(1)} y2={P.Y(1)} stroke={C.bd} />
      <path d={P.path(flux, xa, xb, 300)} fill="none" stroke={C.sp} strokeWidth="1.2" opacity="0.4" />
      <path d={P.path(flux, xa, xp, 300)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <circle cx={P.X(xp)} cy={P.Y(flux(xp))} r="4" fill={C.red} />
      <text x={P.l - 4} y={P.Y(1) + 3} textAnchor="end" fontSize="9" fill={C.mut}>1</text>
      <text x={P.l - 4} y={P.Y(1 - depth) + 3} textAnchor="end" fontSize="9" fill={C.mut}>{fmt(1 - depth, 4)}</text>
      <line x1={P.l} x2={P.r} y1={P.Y(1 - depth)} y2={P.Y(1 - depth)} stroke={C.red} strokeDasharray="2 3" opacity="0.5" />
      <text x={P.r} y={P.b + 14} textAnchor="end" fontSize="9.5" fill={C.mut}>시간 → (밝기)</text>
    </Frame>
  );
}

/* ── 팽창하는 우주: 모든 거리가 같은 비율로 늘면 v = Hd — 어디서 봐도 같다 ── */
export function Hubble({ p = {} }) {
  const [home, setHome] = useState(p.home || "a");
  const clock = useClock({ period: 10 });
  const gal = useMemo(() => { const r = rng(5); return Array.from({ length: 30 }, () => [r() * 2.4 - 1.2, r() * 2.4 - 1.2]); }, []);
  const a = 1 + 0.07 * clock.t, H = 0.07 / a;
  const hi = home === "a" ? 0 : 7, [hx, hy] = gal[hi];
  const cx = 108, cy = 110, S = 62;
  const rel = gal.map(([x, y]) => [(x - hx) * a, (y - hy) * a]);
  const P = plot({ x0: 0, x1: 2.6, y0: 0, y1: 0.2, pad: [16, 12, 26, 236] });
  return (
    <Frame clock={clock} title="팽창하는 우주"
      read={<>척도 인자 a(t) = <b>{fmt(a, 2)}</b> — 모든 거리가 같은 비율로 늘어난다 · {home === "a" ? "우리 은하" : "다른 은하"}(가운데)에서 보면 모든 은하가 <b>거리에 비례하는 속도</b>로 멀어진다: v = Hd (오른쪽 그래프가 직선) · 기준을 바꿔도 똑같다 — 우주에 중심은 없다 · 지금 우주의 H₀ ≈ 70 km/s/Mpc, 1/H₀ ≈ 140 억 년</>}
      controls={<Seg value={home} onChange={setHome} options={[["a", "우리 은하에서"], ["b", "다른 은하에서"]]} />}>
      <rect x={cx - 100} y={cy - 98} width="200" height="196" rx="6" fill={C.card} stroke={C.bd} />
      {rel.map(([x, y], i) => {
        const X = cx + x * S, Y = cy - y * S;
        if (Math.abs(x * S) > 82 || Math.abs(y * S) > 80) return null;
        const vx = H * x * S * 5, vy = -H * y * S * 5;
        return (
          <g key={i}>
            {i !== hi && <Arrow x1={X} y1={Y} x2={X + vx} y2={Y + vy} color={C.red} w={1.1} head={4} />}
            <ellipse cx={X} cy={Y} rx={i === hi ? 5 : 3.4} ry={i === hi ? 3.4 : 2.2} fill={i === hi ? C.blue : C.ink} opacity={i === hi ? 1 : 0.75} />
          </g>
        );
      })}
      <Axes p={P} xl="거리 d" yl="v" xt={[]} yt={[]} />
      {rel.map(([x, y], i) => { const dd = Math.hypot(x, y); return i === hi || dd > 2.6 ? null : <circle key={i} cx={P.X(dd)} cy={P.Y(H * dd)} r="2.8" fill={C.red} />; })}
      <path d={P.path((dd) => H * dd, 0, 2.6, 10)} fill="none" stroke={C.mut} strokeDasharray="4 3" />
      <Label x={P.l + 6} y={P.t + 10} size={10} color={C.ink} bg>v = Hd</Label>
    </Frame>
  );
}
