// 복소해석 그림 — 곱은 회전 · 확대 · n 제곱근 · 등각 사상 격자 · 코시–리만(작은 정사각형) · 다가함수와 가지 · 감김수 · 코시 적분 공식 · 수렴 반지름과 극 · 유수 정리
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, fmt, clamp, lerp, ease, useClock } from "./kit.jsx";

/* 복소수 [실수부, 허수부] */
const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const mul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
const div = (a, b) => { const d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; };
const cabs = (a) => Math.hypot(a[0], a[1]);
const carg = (a) => Math.atan2(a[1], a[0]);
const polar = (r, t) => [r * Math.cos(t), r * Math.sin(t)];
const cexp = (a) => polar(Math.exp(a[0]), a[1]);
const deg = (t) => (t * 180) / Math.PI;
const cfmt = (z, d = 3) => `${fmt(z[0], d)} ${z[1] < 0 ? "−" : "+"} ${fmt(Math.abs(z[1]), d)}i`;
const plane = (ox, oy, s) => ({ X: (z) => ox + z[0] * s, Y: (z) => oy - z[1] * s, s, ox, oy });
const pathOf = (P, pts) => pts.map((z, i) => (i ? "L" : "M") + P.X(z).toFixed(1) + " " + P.Y(z).toFixed(1)).join("") || "M0 0";
function AxesC({ P, w = 360, h = 220, lab = true }) {
  return (
    <g>
      <line x1="4" x2={w - 4} y1={P.oy} y2={P.oy} stroke={C.bd} />
      <line x1={P.ox} x2={P.ox} y1="4" y2={h - 4} stroke={C.bd} />
      {lab && <text x={w - 6} y={P.oy - 4} textAnchor="end" fontSize="9" fill={C.mut}>실수축</text>}
      {lab && <text x={P.ox + 4} y="13" fontSize="9" fill={C.mut}>허수축</text>}
    </g>
  );
}
const arcPath = (P, r, a0, a1) => {
  const n = Math.max(2, Math.ceil(Math.abs(a1 - a0) / 0.08));
  return pathOf(P, Array.from({ length: n + 1 }, (_, i) => polar(r, a0 + ((a1 - a0) * i) / n)));
};

/* ── 곱 = 늘이고 돌리기 ── */
export function CMul({ p = {} }) {
  const [m, setM] = useState(p.mode === "pow" ? "pow" : "mul");
  const [r, setR] = useState(clamp(p.r ?? 1, 0.5, 1.6));
  const clock = useClock({ period: 10, rest: 6.2 });
  const P = plane(180, 112, 46);
  if (m === "mul") {
    const z = polar(1.3, Math.PI / 6), th = (2 * Math.PI * clock.t) / 10, w = polar(r, th), zw = mul(z, w);
    const az = carg(z), aw = ((th % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
    return (
      <Frame clock={clock} title="복소수의 곱 — 늘이고 돌리기"
        read={<>z: 길이 1.3 · 각 30° / w: 길이 {fmt(r, 2)} · 각 {fmt(deg(aw), 0)}° → <b>zw</b>: 길이 1.3 × {fmt(r, 2)} = {fmt(1.3 * r, 3)} · 각 30° + {fmt(deg(aw), 0)}° = {fmt(deg(az + aw) % 360, 0)}° — 곱하면 길이는 곱해지고 각은 더해진다 · i 를 곱하면 90° 회전(i² = −1 은 180° 회전)</>}
        controls={<>
          <Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["mul", "z × w"], ["pow", "z 의 거듭제곱"]]} />
          <Slider label="w 의 길이" min={0.5} max={1.6} step={0.05} value={r} onChange={setR} show={(v) => fmt(v, 2)} />
        </>}>
        <AxesC P={P} />
        <circle cx={P.ox} cy={P.oy} r={P.s} fill="none" stroke={C.bd} strokeDasharray="3 3" />
        <path d={arcPath(P, 0.45, 0, az)} fill="none" stroke={C.blue} strokeWidth="2" />
        <path d={arcPath(P, 0.62, 0, aw)} fill="none" stroke={C.gold} strokeWidth="2" />
        <path d={arcPath(P, 0.8, 0, az + aw)} fill="none" stroke={C.red} strokeWidth="1.4" strokeDasharray="3 2" />
        {[[z, C.blue, "z"], [w, C.gold, "w"], [zw, C.red, "zw"]].map(([q, col, lb]) => (
          <g key={lb}>
            <line x1={P.ox} y1={P.oy} x2={P.X(q)} y2={P.Y(q)} stroke={col} strokeWidth="2.2" />
            <circle cx={P.X(q)} cy={P.Y(q)} r="4.2" fill={col} />
            <text x={P.X(q) + 6} y={P.Y(q) - 6} fontSize="12" fontWeight="800" fill={col}>{lb}</text>
          </g>
        ))}
      </Frame>
    );
  }
  const rz = clamp(r, 0.85, 1.15), a = (40 * Math.PI) / 180;
  const N = Math.min(18, Math.floor(clock.t * 2));
  const pts = Array.from({ length: N + 1 }, (_, n) => polar(rz ** n, a * n));
  const vis = pts.filter((q) => cabs(q) <= 2.5);
  return (
    <Frame clock={clock} title="복소수의 곱 — 거듭제곱은 나선"
      read={<>z = 길이 {fmt(rz, 2)} · 각 40° 일 때 zⁿ 은 길이 {fmt(rz, 2)} 의 n 제곱, 각 n × 40° — 지금 n = {N} · {rz > 1.001 ? "길이가 1 보다 크면 바깥으로 풀리는 나선" : rz < 0.999 ? "길이가 1 보다 작으면 안으로 감기는 나선" : "길이가 1 이면 원 위를 돈다 — 드무아브르 공식 (cos θ + i sin θ)ⁿ = cos nθ + i sin nθ"}</>}
      controls={<>
        <Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["mul", "z × w"], ["pow", "z 의 거듭제곱"]]} />
        <Slider label="z 의 길이" min={0.85} max={1.15} step={0.01} value={rz} onChange={setR} show={(v) => fmt(v, 2)} />
      </>}>
      <AxesC P={P} />
      <circle cx={P.ox} cy={P.oy} r={P.s} fill="none" stroke={C.bd} strokeDasharray="3 3" />
      <path d={pathOf(P, vis)} fill="none" stroke={C.sp} strokeWidth="1.6" />
      {vis.map((q, n) => <circle key={n} cx={P.X(q)} cy={P.Y(q)} r={n === vis.length - 1 ? 4.4 : 2.8} fill={n === vis.length - 1 ? C.red : C.sp} />)}
      {vis.length > 1 && <text x={P.X(vis[vis.length - 1]) + 6} y={P.Y(vis[vis.length - 1]) - 6} fontSize="11" fontWeight="800" fill={C.red}>z{["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "¹⁰", "¹¹", "¹²", "¹³", "¹⁴", "¹⁵", "¹⁶", "¹⁷", "¹⁸"][vis.length - 1]}</text>}
    </Frame>
  );
}

/* ── n 제곱근: 정 n 각형, w 가 한 바퀴 돌면 해는 한 칸 ── */
export function Roots({ p = {} }) {
  const [n, setN] = useState(clamp(p.n ?? 5, 2, 12));
  const clock = useClock({ period: 12, rest: 3 });
  const R = 1.6, phi = (2 * Math.PI * clock.t) / 12, rr = R ** (1 / n);
  const P = plane(180, 112, 58);
  const roots = Array.from({ length: n }, (_, k) => polar(rr, (phi + 2 * Math.PI * k) / n));
  const w = polar(R, phi);
  const trail = Array.from({ length: 40 }, (_, i) => polar(rr, (phi * i) / 39 / n));
  return (
    <Frame clock={clock} title="n 제곱근 — 원 위의 정다각형"
      read={<>zⁿ = w (n = {n}) 의 해 {n} 개는 반지름 {fmt(rr, 3)}(= 1.6 의 {n} 제곱근)인 원 위에 정 {n} 각형으로 놓인다 · w 가 지금까지 {fmt(deg(phi), 0)}° 도는 동안 파란 해는 그 1/{n} 인 {fmt(deg(phi) / n, 1)}° 만 돌았다 — w 가 한 바퀴를 다 돌면 파란 해는 이웃 해의 자리로 옮겨 간다: ‘n 제곱근’을 연속해서 한 값으로 정할 수 없는 까닭</>}
      controls={<Slider label="n" min={2} max={12} step={1} value={n} onChange={(v) => { setN(v); clock.reset(); }} show={(v) => String(v)} />}>
      <AxesC P={P} />
      <circle cx={P.ox} cy={P.oy} r={R * P.s} fill="none" stroke={C.gold} strokeDasharray="3 3" opacity="0.7" />
      <circle cx={P.ox} cy={P.oy} r={rr * P.s} fill="none" stroke={C.bd} />
      <path d={pathOf(P, [...roots, roots[0]])} fill="none" stroke={C.red} strokeWidth="1.2" opacity="0.6" />
      <path d={pathOf(P, trail)} fill="none" stroke={C.blue} strokeWidth="2.6" opacity="0.5" />
      {roots.map((q, k) => <circle key={k} cx={P.X(q)} cy={P.Y(q)} r={k ? 4 : 5.5} fill={k ? C.red : C.blue} />)}
      <line x1={P.ox} y1={P.oy} x2={P.X(w)} y2={P.Y(w)} stroke={C.gold} strokeWidth="1.6" />
      <circle cx={P.X(w)} cy={P.Y(w)} r="5" fill={C.gold} />
      <text x={P.X(w) + 7} y={P.Y(w) - 5} fontSize="12" fontWeight="800" fill={C.gold}>w</text>
    </Frame>
  );
}

/* ── 복소함수는 평면을 평면으로 — 격자가 휘어도 직각은 그대로 ── */
const C0 = [-0.08, 0.08], RJ = Math.hypot(1 - C0[0], C0[1]);
const MAPS = {
  sq: { f: (z) => mul(z, z), name: "w = z²",
    lines: () => [...[0.25, 0.5, 0.75, 1, 1.25, 1.5].map((c) => [0, Array.from({ length: 61 }, (_, i) => [c, (1.5 * i) / 60])]), ...[0.25, 0.5, 0.75, 1, 1.25, 1.5].map((c) => [1, Array.from({ length: 61 }, (_, i) => [(1.5 * i) / 60, c])])],
    read: "w = z²: 첫째 사분면의 격자가 위쪽 반평면으로 펴진다 — 사각형은 휘지만 선끼리 만나는 각은 90° 그대로다(z = 0 만 예외: 도함수가 0 이라 각이 두 배로 벌어진다)" },
  inv: { f: (z) => div([1, 0], z), name: "w = 1/z",
    lines: () => [...[0.3, 0.5, 0.8, 1.2, 1.8].map((c) => [0, Array.from({ length: 81 }, (_, i) => [c, -1.2 + (2.4 * i) / 80])]), ...[-1.2, -0.6, 0, 0.6, 1.2].map((c) => [1, Array.from({ length: 81 }, (_, i) => [0.3 + (1.5 * i) / 80, c])])],
    read: "w = 1/z: 원점을 지나지 않는 직선은 원점을 지나는 원이 된다 — 뫼비우스 변환은 ‘원과 직선’을 ‘원과 직선’으로 보낸다" },
  exp: { f: cexp, name: "w = eᶻ",
    lines: () => [...[-1, -0.5, 0, 0.5, 1].map((c) => [0, Array.from({ length: 81 }, (_, i) => [c, -Math.PI + (2 * Math.PI * i) / 80])]), ...[-3, -2, -1, 0, 1, 2, 3].map((k) => [1, Array.from({ length: 41 }, (_, i) => [-1 + (2 * i) / 40, (k * Math.PI) / 4])])],
    read: "w = eᶻ: 세로선 x = c 는 반지름 e 의 c 제곱인 원, 가로선은 원점에서 뻗는 반직선 — 띠가 고리로 감긴다. y 가 2π 늘면 같은 점에 오므로 거꾸로 가는 로그는 값이 여럿이다" },
  jouk: { f: (z) => add(z, div([1, 0], z)), name: "w = z + 1/z (주코프스키)",
    lines: () => [...[1, 1.25, 1.6, 2.1].map((k) => [0, Array.from({ length: 97 }, (_, i) => add(C0, polar(RJ * k, (2 * Math.PI * i) / 96)))]), ...Array.from({ length: 12 }, (_, j) => [1, Array.from({ length: 31 }, (_, i) => add(C0, polar(RJ * (1 + (1.1 * i) / 30), (2 * Math.PI * j) / 12)))])],
    read: "주코프스키 변환 w = z + 1/z: 원점에서 살짝 비켜난 원(굵은 선)이 비행기 날개 단면이 된다 — 원 둘레의 흐름은 쉽게 계산되므로, 그 흐름을 옮기면 날개 둘레의 흐름과 양력을 안다" },
};
export function CMap({ p = {} }) {
  const [k, setK] = useState(MAPS[p.map] ? p.map : "sq");
  const M = MAPS[k];
  const L = useMemo(() => M.lines().map(([fam, pts]) => [fam, pts, pts.map(M.f)]), [k]);
  const fit = useMemo(() => {
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    for (const [, a, b] of L) for (const q of [...a, ...b]) { x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]); }
    const s = Math.min(330 / (x1 - x0), 196 / (y1 - y0));
    return plane(180 - ((x0 + x1) / 2) * s, 112 + ((y0 + y1) / 2) * s, s);
  }, [L]);
  const clock = useClock({ period: 9, rest: 7 });
  const sv = ease(clamp((clock.t - 1) / 4, 0, 1));
  return (
    <Frame clock={clock} title="복소함수 — 평면을 평면으로"
      read={<>{M.read} · 지금 {sv < 0.01 ? "원래 격자(z 평면)" : sv > 0.99 ? "옮겨진 격자(w 평면)" : `옮겨 가는 중 ${fmt(sv * 100, 0)} %`}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["sq", "z²"], ["inv", "1/z"], ["exp", "eᶻ"], ["jouk", "날개(주코프스키)"]]} />}>
      <AxesC P={fit} lab={false} />
      {L.map(([fam, a, b], i) => {
        const pts = a.map((q, j) => [lerp(q[0], b[j][0], sv), lerp(q[1], b[j][1], sv)]);
        const wing = k === "jouk" && fam === 0 && i === 0;
        return <path key={i} d={pathOf(fit, pts)} fill={wing ? "color-mix(in srgb, var(--sp, var(--ac)) 18%, transparent)" : "none"} stroke={fam ? C.red : C.blue} strokeWidth={wing ? 2.6 : 1.3} opacity={wing ? 1 : 0.85} />;
      })}
      <text x="12" y="16" fontSize="10.5" fontWeight="800" fill={C.ink}>{M.name}</text>
    </Frame>
  );
}

/* ── 코시–리만: 정칙 함수는 아주 작은 정사각형을 정사각형으로 ── */
const CRF = {
  sq: { f: (z) => mul(z, z), name: "f(z) = z²", ok: true },
  exp: { f: cexp, name: "f(z) = eᶻ", ok: true },
  conj: { f: (z) => [z[0], -z[1]], name: "f(z) = z̄ (켤레)", ok: false },
  str: { f: (z) => [z[0] + 0.3 * z[1] * z[1], 2 * z[1]], name: "f = (x + 0.3y²) + 2yi", ok: false },
};
export function CR({ p = {} }) {
  const [k, setK] = useState(CRF[p.f] ? p.f : "sq");
  const F = CRF[k];
  const clock = useClock({ period: 10, rest: 2 });
  const th = (2 * Math.PI * clock.t) / 10, z0 = [0.6 + 0.45 * Math.cos(th), 0.5 + 0.45 * Math.sin(th)];
  const e = 1e-5, fz = F.f(z0);
  const fx = sub(F.f([z0[0] + e, z0[1]]), F.f([z0[0] - e, z0[1]])).map((v) => v / (2 * e));
  const fy = sub(F.f([z0[0], z0[1] + e]), F.f([z0[0], z0[1] - e])).map((v) => v / (2 * e));
  const [ux, vx, uy, vy] = [fx[0], fx[1], fy[0], fy[1]];
  const cr = Math.abs(ux - vy) < 1e-4 && Math.abs(uy + vx) < 1e-4;
  const h = 0.08, n = 5;
  const nrm = Math.max(1e-9, Math.hypot(ux, vx), Math.hypot(uy, vy));
  const L = plane(90, 112, 62 / h / 1.2), R = plane(270, 112, 62 / (h * nrm) / 1.2);
  const grid = [];
  for (let i = 0; i <= n; i++) {
    const c = -h + (2 * h * i) / n;
    grid.push([0, Array.from({ length: 21 }, (_, j) => [c, -h + (2 * h * j) / 20])]);
    grid.push([1, Array.from({ length: 21 }, (_, j) => [-h + (2 * h * j) / 20, c])]);
  }
  const img = (d) => sub(F.f(add(z0, d)), fz);
  const fp = cr ? [ux, vx] : null;
  return (
    <Frame clock={clock} title="코시–리만 방정식 — 작은 정사각형의 운명"
      read={<>{F.name}, z₀ = {cfmt(z0, 2)} · 편미분: ∂u/∂x = {fmt(ux, 2)}, ∂v/∂y = {fmt(vy, 2)}, ∂u/∂y = {fmt(uy, 2)}, ∂v/∂x = {fmt(vx, 2)} · {cr ? <><b>코시–리만 성립</b>(∂u/∂x = ∂v/∂y, ∂u/∂y = −∂v/∂x) — 작은 정사각형이 정사각형 그대로 {fmt(deg(carg(fp)), 0)}° 돌고 {fmt(cabs(fp), 2)} 배 커진다: f′(z₀) = {cfmt(fp, 2)}</> : <><b>코시–리만이 깨진다</b> — 작은 정사각형이 {k === "conj" ? "뒤집힌다(거울상)" : "찌그러진다"}: 복소수 하나를 곱하는 것으로 나타낼 수 없어 복소 미분이 없다</>}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["sq", "z²"], ["exp", "eᶻ"], ["conj", "켤레 z̄"], ["str", "찌그러뜨리기"]]} />}>
      <rect x="10" y="20" width="160" height="184" rx="6" fill="none" stroke={C.bd} />
      <rect x="190" y="20" width="160" height="184" rx="6" fill="none" stroke={C.bd} />
      <text x="16" y="34" fontSize="9.5" fill={C.mut}>z₀ 둘레(확대)</text>
      <text x="196" y="34" fontSize="9.5" fill={C.mut}>f 로 옮긴 모양(확대)</text>
      <text x="180" y="116" textAnchor="middle" fontSize="16" fill={C.mut}>→</text>
      {grid.map(([fam, pts], i) => (
        <g key={i}>
          <path d={pathOf(L, pts)} fill="none" stroke={fam ? C.red : C.blue} strokeWidth="1.2" />
          <path d={pathOf(R, pts.map(img))} fill="none" stroke={fam ? C.red : C.blue} strokeWidth="1.2" />
        </g>
      ))}
      {(() => { const q = [[-h, -h], [-h + (2 * h) / n, -h], [-h + (2 * h) / n, -h + (2 * h) / n], [-h, -h + (2 * h) / n]]; return (<>
        <path d={pathOf(L, q) + "Z"} fill={C.gold} opacity="0.55" />
        <path d={pathOf(R, q.map(img)) + "Z"} fill={C.gold} opacity="0.55" />
      </>); })()}
    </Frame>
  );
}

/* ── 다가함수: 원점을 한 바퀴 돌면 값이 바뀐다 ── */
const BR = {
  sqrt: { loops: 2, name: "√z", w: (r, t) => polar(Math.sqrt(r), t / 2) },
  cbrt: { loops: 3, name: "∛z", w: (r, t) => polar(Math.cbrt(r), t / 3) },
  log: { loops: 2, name: "log z", w: (r, t) => [Math.log(r), t] },
};
export function Branch({ p = {} }) {
  const [k, setK] = useState(BR[p.f] ? p.f : "sqrt");
  const B = BR[k], per = 4;
  const clock = useClock({ period: B.loops * per + 2, rest: per + 0.4 });
  const th = Math.min(B.loops * 2 * Math.PI, (2 * Math.PI * clock.t) / per), rz = 1.25;
  const loop = Math.floor(th / (2 * Math.PI) + 1e-9);
  const Lp = plane(90, 112, 56);
  const zs = Array.from({ length: 81 }, (_, i) => polar(rz, (th * i) / 80));
  const ws = Array.from({ length: 121 }, (_, i) => B.w(rz, (th * i) / 120));
  const isLog = k === "log";
  const Rp = isLog ? plane(270, 196, 13.5) : plane(270, 112, 62);
  const w = B.w(rz, th), w0 = B.w(rz, 0);
  const others = isLog ? [] : Array.from({ length: B.loops }, (_, j) => B.w(rz, 2 * Math.PI * j));
  return (
    <Frame clock={clock} title="다가함수와 가지 자르기"
      read={<>z 가 원점 둘레를 {fmt(deg(th), 0)}° 돌았다({loop} 바퀴) · {k === "sqrt" ? "한 바퀴(360°) 돌면 √z 는 180° 만 돌아 처음 값의 반대(−√z₀)에 닿고, 두 바퀴를 돌아야 돌아온다 — 같은 z 에 값이 둘" : k === "cbrt" ? "한 바퀴마다 ∛z 는 120° 씩 돌아 세 값을 차례로 지나고, 세 바퀴 만에 돌아온다" : "log z = ln|z| + i × (각) — 한 바퀴마다 허수부가 2π 씩 늘어 끝없이 많은 값을 갖는다(나선 계단)"} · 음의 실수축(빨간 점선)을 넘지 않기로 약속하면 값을 하나만 고를 수 있다(주가지)</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["sqrt", "√z"], ["cbrt", "∛z"], ["log", "log z"]]} />}>
      <rect x="10" y="20" width="160" height="184" rx="6" fill="none" stroke={C.bd} />
      <rect x="190" y="20" width="160" height="184" rx="6" fill="none" stroke={C.bd} />
      <text x="16" y="34" fontSize="9.5" fill={C.mut}>z 평면</text>
      <text x="196" y="34" fontSize="9.5" fill={C.mut}>{B.name} 의 값</text>
      <line x1="14" x2={Lp.ox} y1={Lp.oy} y2={Lp.oy} stroke={C.red} strokeWidth="1.6" strokeDasharray="5 3" />
      <line x1={Lp.ox} x2="166" y1={Lp.oy} y2={Lp.oy} stroke={C.bd} />
      <line x1={Lp.ox} x2={Lp.ox} y1="40" y2="200" stroke={C.bd} />
      <circle cx={Lp.ox} cy={Lp.oy} r="2.5" fill={C.ink} />
      <path d={pathOf(Lp, zs)} fill="none" stroke={C.sp} strokeWidth="1.8" />
      <circle cx={Lp.X(zs[80])} cy={Lp.Y(zs[80])} r="4.5" fill={C.red} />
      {isLog ? <line x1={Rp.X([-6, 0])} x2={Rp.X([6, 0])} y1={Rp.oy} y2={Rp.oy} stroke={C.bd} /> : <><line x1="194" x2="346" y1={Rp.oy} y2={Rp.oy} stroke={C.bd} /><line x1={Rp.ox} x2={Rp.ox} y1="40" y2="200" stroke={C.bd} /></>}
      {isLog && [1, 2].map((j) => <g key={j}><line x1="200" x2="340" y1={Rp.Y([0, 2 * Math.PI * j])} y2={Rp.Y([0, 2 * Math.PI * j])} stroke={C.bd} strokeDasharray="3 3" /><text x="342" y={Rp.Y([0, 2 * Math.PI * j]) + 3} textAnchor="end" fontSize="9" fill={C.mut}>{j === 1 ? "2π" : "4π"}</text></g>)}
      {others.map((q, j) => <circle key={j} cx={Rp.X(q)} cy={Rp.Y(q)} r="5.5" fill="none" stroke={C.gold} strokeWidth="1.4" />)}
      <path d={pathOf(Rp, ws)} fill="none" stroke={C.sp} strokeWidth="1.8" />
      <circle cx={Rp.X(w0)} cy={Rp.Y(w0)} r="3" fill={C.ink} />
      <circle cx={Rp.X(w)} cy={Rp.Y(w)} r="4.5" fill={C.red} />
    </Frame>
  );
}

/* ── 감김수: ∮ dz ÷ (z − a) = 2πi × (감은 횟수) ── */
const CONT = {
  circ: { z: (s) => polar(1.5, s), name: "원" },
  eight: { z: (s) => [1.8 * Math.sin(s), 0.9 * Math.sin(2 * s)], name: "8 자" },
};
export function Winding({ p = {} }) {
  const [k, setK] = useState(CONT[p.c] ? p.c : "circ");
  const [ax, setAx] = useState(clamp(p.a ?? 0.6, -2.4, 2.4));
  const Cn = CONT[k], a = [ax, 0.25];
  const clock = useClock({ period: 10, rest: 8.6 });
  const s = Math.min(2 * Math.PI, (2 * Math.PI * clock.t) / 8);
  const N = 400, pts = Array.from({ length: N + 1 }, (_, i) => Cn.z((2 * Math.PI * i) / N));
  const near = Math.min(...pts.map((q) => cabs(sub(q, a)))) < 0.04;
  const steps = Math.max(1, Math.round((N * s) / (2 * Math.PI)));
  let ang = 0;
  for (let i = 1; i <= steps; i++) { let d = carg(sub(pts[i], a)) - carg(sub(pts[i - 1], a)); if (d > Math.PI) d -= 2 * Math.PI; if (d < -Math.PI) d += 2 * Math.PI; ang += d; }
  const zc = Cn.z(s), wind = Math.round(ang / (2 * Math.PI));
  const P = plane(180, 112, 52);
  const done = s >= 2 * Math.PI - 1e-9;
  return (
    <Frame clock={clock} title="감김수와 ∮ dz ÷ (z − a)"
      read={<>{near ? "a 가 곡선 위에 있어 적분이 정의되지 않는다 — a 를 옮겨 보자" : <>a 에서 본 z 의 방향이 지금까지 돈 각 = <b>{fmt(deg(ang), 0)}°</b> · ∮ dz ÷ (z − a) = i × (돈 각) {done ? <>= 2πi × <b>{wind}</b> — 곡선이 a 를 감은 횟수(감김수)만 남는다</> : "— 한 바퀴를 다 돌면 2π 의 정수배만 남는다"}{k === "eight" ? " · 8 자의 왼쪽 고리는 +1, 오른쪽 고리는 −1, 바깥은 0" : ""}</>}</>}
      controls={<>
        <Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["circ", "원"], ["eight", "8 자"]]} />
        <Slider label="a 의 위치" min={-2.4} max={2.4} step={0.1} value={ax} onChange={(v) => { setAx(v); clock.reset(); }} show={(v) => fmt(v, 1)} />
      </>}>
      <AxesC P={P} />
      <path d={pathOf(P, pts)} fill="none" stroke={C.bd} strokeWidth="1.4" />
      <path d={pathOf(P, pts.slice(0, steps + 1))} fill="none" stroke={C.sp} strokeWidth="2.2" />
      {!near && <line x1={P.X(a)} y1={P.Y(a)} x2={P.X(zc)} y2={P.Y(zc)} stroke={C.gold} strokeWidth="1.4" />}
      {!near && Math.abs(ang) > 0.02 && <path d={pathOf(P, Array.from({ length: 60 }, (_, i) => add(a, polar(0.28 + (0.07 * i) / 59 * Math.abs(ang) / (2 * Math.PI), carg(sub(pts[0], a)) + (ang * i) / 59))))} fill="none" stroke={C.red} strokeWidth="2" />}
      <circle cx={P.X(a)} cy={P.Y(a)} r="5" fill={near ? C.mut : C.red} />
      <text x={P.X(a) + 7} y={P.Y(a) + 14} fontSize="12" fontWeight="800" fill={C.red}>a</text>
      <circle cx={P.X(zc)} cy={P.Y(zc)} r="4.2" fill={C.sp} />
      <text x={P.X(zc) + 6} y={P.Y(zc) - 6} fontSize="11" fontWeight="800" fill={C.sp}>z</text>
    </Frame>
  );
}

/* ── 코시 적분 공식: 원 위의 값이 안쪽을 정한다 ── */
const CIF = {
  exp: { f: cexp, name: "eᶻ" },
  cub: { f: (z) => sub(mul(z, mul(z, z)), z), name: "z³ − z" },
  rat: { f: (z) => div([1, 0], sub(z, [2, 0.5])), name: "1 ÷ (z − 2 − 0.5i)" },
};
export function CauchyInt({ p = {} }) {
  const [k, setK] = useState(CIF[p.f] ? p.f : "exp");
  const [ax, setAx] = useState(clamp(p.a ?? 0.4, -0.8, 0.8));
  const F = CIF[k], a = [ax, 0.2];
  const per = 0.8, Ns = [3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32];
  const clock = useClock({ period: Ns.length * per + 2, rest: 6 * per + 0.3 });
  const idx = Math.min(Ns.length - 1, Math.floor(clock.t / per)), N = Ns[idx];
  const approx = (M) => { let s = [0, 0]; for (let j = 0; j < M; j++) { const z = polar(1, (2 * Math.PI * j) / M); s = add(s, div(mul(F.f(z), z), sub(z, a))); } return [s[0] / M, s[1] / M]; };
  const exact = F.f(a), cur = approx(N), errs = Ns.map((M) => cabs(sub(approx(M), exact)));
  const P = plane(96, 112, 74), G = plot({ x0: 0, x1: 34, y0: 0, y1: 16, pad: [26, 12, 24, 214] });
  const ac = cabs(a) < 1e-9;
  return (
    <Frame clock={clock} title="코시 적분 공식"
      read={<>f(z) = {F.name} 를 단위원 위의 {N} 곳에서만 재어 (1 ÷ 2πi) ∮ f(z) ÷ (z − a) dz 를 계산하면 {cfmt(cur, 5)} · 참값 f(a) = {cfmt(exact, 5)} · 오차 {errs[idx] < 1e-12 ? "10 의 −12 제곱 아래" : errs[idx] >= 0.01 ? fmt(errs[idx], 3) : errs[idx].toExponential(1).replace("e-", " × 10⁻").replace(/⁻(\d+)$/, (m, g) => "⁻" + g.split("").map((d) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[+d]).join(""))} — 정칙 함수는 경계의 값이 안쪽의 값을 모두 정한다 · 오른쪽: 잴 곳을 늘리면 오차가 지수적으로 준다{ac ? " · a = 0 이면 이 식은 원 위의 평균 = 중심의 값(평균값 성질)" : ""}</>}
      controls={<>
        <Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["exp", "eᶻ"], ["cub", "z³ − z"], ["rat", "1 ÷ (z − 2 − 0.5i)"]]} />
        <Slider label="a 의 실수부" min={-0.8} max={0.8} step={0.1} value={ax} onChange={setAx} show={(v) => fmt(v, 1)} />
      </>}>
      <line x1="10" x2="182" y1={P.oy} y2={P.oy} stroke={C.bd} />
      <line x1={P.ox} x2={P.ox} y1="22" y2="206" stroke={C.bd} />
      <circle cx={P.ox} cy={P.oy} r={P.s} fill="none" stroke={C.sp} strokeWidth="1.6" />
      {Array.from({ length: N }, (_, j) => { const z = polar(1, (2 * Math.PI * j) / N), v = F.f(z), m = Math.max(0.6, cabs(v)), d = [(v[0] / m) * 0.28, (v[1] / m) * 0.28];
        return <g key={j}><line x1={P.X(z)} y1={P.Y(z)} x2={P.X(add(z, d))} y2={P.Y(add(z, d))} stroke={C.gold} strokeWidth="1.6" /><circle cx={P.X(z)} cy={P.Y(z)} r="3" fill={C.sp} /></g>; })}
      <circle cx={P.X(a)} cy={P.Y(a)} r="4.6" fill={C.red} />
      <text x={P.X(a) + 6} y={P.Y(a) - 6} fontSize="11" fontWeight="800" fill={C.red}>a</text>
      <Axes p={G} xl="잴 곳 N" yl="" grid={false} xt={[8, 16, 24, 32]} yt={[4, 8, 12, 16]} yfmt={(v) => "10⁻" + String(v).split("").map((d) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[+d]).join("")} />
      <path d={G.poly(Ns.slice(0, idx + 1).map((M, i) => [M, clamp(-Math.log10(Math.max(1e-17, errs[i])), 0, 16)]))} fill="none" stroke={C.red} strokeWidth="1.6" />
      {Ns.slice(0, idx + 1).map((M, i) => <circle key={M} cx={G.X(M)} cy={G.Y(clamp(-Math.log10(Math.max(1e-17, errs[i])), 0, 16))} r="2.4" fill={C.red} />)}
      <text x={G.l + 4} y={G.t - 8} fontSize="9" fill={C.mut}>오차(위로 갈수록 작다)</text>
    </Frame>
  );
}

/* ── 수렴 반지름은 복소평면의 극이 정한다 ── */
function coef(c, n) { // 1/(1 + z²) 의 c 둘레 테일러 계수 — (1/(2i))(1/(z − i) − 1/(z + i))
  const term = (pp) => { let q = [1, 0]; const d = sub(pp, [c, 0]); for (let j = 0; j <= n; j++) q = div(q, d); return [-q[0], -q[1]]; };
  const v = sub(term([0, 1]), term([0, -1]));
  return div(v, [0, 2])[0];
}
export function PSeries({ p = {} }) {
  const [c, setC] = useState(clamp(p.c ?? 0, -1, 1));
  const R = Math.hypot(1, c);
  const cs = useMemo(() => Array.from({ length: 41 }, (_, n) => coef(c, n)), [c]);
  const clock = useClock({ period: 11, rest: 8.5 });
  const Nn = Math.min(40, Math.floor(clock.t * 5));
  const S = (x) => { let s = 0, pw = 1; for (let n = 0; n <= Nn; n++) { s += cs[n] * pw; pw *= x - c; } return s; };
  const P = plot({ x0: -2.6, x1: 2.6, y0: -0.45, y1: 1.45, pad: [14, 12, 24, 30] });
  const I = plane(306, 52, 17);
  return (
    <Frame clock={clock} title="수렴 반지름과 복소평면의 극"
      read={<>f(x) = 1 ÷ (1 + x²) 의 테일러 급수를 중심 c = {fmt(c, 1)} 에서 {Nn} 차까지 더했다(빨강) · 수렴 반지름 R = (c 에서 가장 가까운 극 ±i 까지의 거리) = √(1 + c²) = <b>{fmt(R, 3)}</b> · 초록 구간 안에서는 f(파랑)에 붙고, 밖에서는 차수가 높을수록 더 크게 벗어난다 — 실수축에서는 f 가 어디서나 매끈한데도: 오른쪽 위 작은 그림처럼 복소평면의 극 ±i 가 원을 가로막기 때문이다</>}
      controls={<Slider label="중심 c" min={-1} max={1} step={0.1} value={c} onChange={(v) => { setC(v); clock.reset(); }} show={(v) => fmt(v, 1)} />}>
      <rect x={P.X(c - R)} y={P.t} width={P.X(c + R) - P.X(c - R)} height={P.b - P.t} fill={C.green} opacity="0.12" />
      <Axes p={P} xl="x" yl="" grid={false} xt={[-2, -1, 1, 2]} yt={[0.5, 1]} />
      <path d={P.path((x) => 1 / (1 + x * x), -2.6, 2.6, 300)} fill="none" stroke={C.blue} strokeWidth="2" />
      <path d={P.path(S, -2.6, 2.6, 400)} fill="none" stroke={C.red} strokeWidth="1.6" />
      <circle cx={P.X(c)} cy={P.Y(0)} r="3.5" fill={C.ink} />
      <rect x={I.ox - 50} y="10" width="100" height="84" rx="5" fill={C.card} stroke={C.bd} />
      <line x1={I.ox - 48} x2={I.ox + 48} y1={I.oy} y2={I.oy} stroke={C.bd} />
      <line x1={I.ox} x2={I.ox} y1="12" y2="92" stroke={C.bd} />
      <circle cx={I.X([c, 0])} cy={I.Y([c, 0])} r={R * I.s} fill={C.green} opacity="0.18" stroke={C.green} />
      {[1, -1].map((s2) => <text key={s2} x={I.X([0, s2])} y={I.Y([0, s2]) + 4} textAnchor="middle" fontSize="12" fontWeight="800" fill={C.red}>×</text>)}
      <text x={I.X([0, 1]) + 7} y={I.Y([0, 1]) + 4} fontSize="8.5" fill={C.red}>i</text>
      <text x={I.X([0, -1]) + 7} y={I.Y([0, -1]) + 4} fontSize="8.5" fill={C.red}>−i</text>
      <circle cx={I.X([c, 0])} cy={I.Y([c, 0])} r="2" fill={C.ink} />
    </Frame>
  );
}

/* ── 유수 정리: 원 안의 극의 유수만 더하면 된다 ── */
const POLES = [{ z: [0.6, 0.4], r: 1 }, { z: [-0.9, -0.5], r: 2 }, { z: [0.3, 1.6], r: -1 }];
const fres = (z) => POLES.reduce((s, q) => add(s, div([q.r, 0], sub(z, q.z))), [0, 0]);
export function Residue({ p = {} }) {
  const [m, setM] = useState(p.mode === "semi" ? "semi" : "circ");
  const clock = useClock({ period: 11, rest: 9.4 });
  const u = clamp(clock.t / 9, 0, 1);
  if (m === "circ") {
    const R = 0.3 + 1.9 * ease(u);
    const nearPole = POLES.some((q) => Math.abs(cabs(q.z) - R) < 0.05);
    let I = [0, 0];
    if (!nearPole) { const M = 720; for (let j = 0; j < M; j++) { const z = polar(R, (2 * Math.PI * j) / M), dz = mul([0, (2 * Math.PI) / M], z); I = add(I, mul(fres(z), dz)); } }
    const inside = POLES.filter((q) => cabs(q.z) < R), sr = inside.reduce((s, q) => s + q.r, 0);
    const P = plane(180, 112, 46);
    return (
      <Frame clock={clock} title="유수 정리"
        read={<>f(z) = 1 ÷ (z − a) + 2 ÷ (z − b) − 1 ÷ (z − c) · 반지름 {fmt(R, 2)} 인 원 안의 극: {inside.length ? inside.map((q) => `유수 ${fmt(q.r, 0)}`).join(", ") : "없음"} → 2πi × (유수의 합 {fmt(sr, 0)}) = {sr === 0 ? "0" : `${fmt(2 * Math.PI * sr, 4)}i`} · 원을 따라 수치 적분한 값: {nearPole ? "원이 극을 지나 정의되지 않음" : cabs(I) < 1e-9 ? "0" : cfmt(I, 4)} — 원 안의 극의 유수만 더하면 적분이 나온다</>}
        controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["circ", "원과 극 셋"], ["semi", "반원 — 실적분"]]} />}>
        <AxesC P={P} />
        <circle cx={P.ox} cy={P.oy} r={R * P.s} fill="color-mix(in srgb, var(--sp, var(--ac)) 8%, transparent)" stroke={C.sp} strokeWidth="2" />
        {POLES.map((q, i) => { const ins = cabs(q.z) < R; return (
          <g key={i}>
            <text x={P.X(q.z)} y={P.Y(q.z) + 5} textAnchor="middle" fontSize="15" fontWeight="800" fill={ins ? C.red : C.mut}>×</text>
            <text x={P.X(q.z) + 9} y={P.Y(q.z) - 6} fontSize="10" fontWeight={ins ? 800 : 500} fill={ins ? C.red : C.mut}>{"abc"[i]} · 유수 {q.r > 0 ? q.r : "−" + -q.r}</text>
          </g>); })}
      </Frame>
    );
  }
  const R = 0.6 + 5.4 * ease(u), line = 2 * Math.atan(R), tot = R > 1 ? Math.PI : 0, arc = tot - line;
  const sc = Math.min(150 / R, 70), P = plane(180, 190, sc);
  const semi = Array.from({ length: 61 }, (_, i) => polar(R, (Math.PI * i) / 60));
  return (
    <Frame clock={clock} title="유수 정리로 실적분"
      read={<>∫ dx ÷ (1 + x²) 을 구하려고 [−R, R] 과 위쪽 반원을 잇는다(R = {fmt(R, 2)}) · 안의 극은 i 하나(유수 1 ÷ 2i), 전체 = 2πi × 1 ÷ 2i = {R > 1 ? "π" : "0(아직 극이 밖)"} · 실수축 위 = 2 arctan R = <b>{fmt(line, 4)}</b>, 반원 위 = {fmt(arc, 4)} → R 이 커지면 반원 쪽이 0 으로 사라져 ∫ dx ÷ (1 + x²) = π ≈ 3.1416</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["circ", "원과 극 셋"], ["semi", "반원 — 실적분"]]} />}>
      <line x1="6" x2="354" y1={P.oy} y2={P.oy} stroke={C.bd} />
      <line x1={P.ox} x2={P.ox} y1="6" y2="214" stroke={C.bd} />
      <path d={pathOf(P, semi) + `L${P.X([-R, 0]).toFixed(1)} ${P.oy}`} fill="color-mix(in srgb, var(--sp, var(--ac)) 8%, transparent)" stroke={C.sp} strokeWidth="2" />
      <line x1={P.X([-R, 0])} x2={P.X([R, 0])} y1={P.oy} y2={P.oy} stroke={C.red} strokeWidth="2.6" />
      {[1, -1].map((s2) => <text key={s2} x={P.X([0, s2])} y={P.Y([0, s2]) + 5} textAnchor="middle" fontSize="15" fontWeight="800" fill={s2 > 0 && R > 1 ? C.red : C.mut}>×</text>)}
      <text x={P.X([0, 1]) + 9} y={P.Y([0, 1]) - 4} fontSize="10" fill={C.red}>i</text>
    </Frame>
  );
}
