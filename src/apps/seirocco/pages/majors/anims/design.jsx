// 디자인 그림 — 황금비와 종이 비율 · 띠 무늬 7 가지 · 쪽매맞춤(정다각형 · 에셔) · 베지에 곡선 · 명도 대비 · 원근(소실점) · 피츠 법칙 · 프랙탈
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Label, fmt, clamp, useClock } from "./kit.jsx";

const TAU = 2 * Math.PI, PHI = (1 + Math.sqrt(5)) / 2;
const pth = (pts) => pts.map(([x, y], i) => (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1)).join("") || "M0 0";

/* ── 비율: 황금 직사각형 · 종이(√2) · 피보나치 ── */
function goldenSquares(x, y, w, h, n) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const d = i % 4;
    if (d === 0) { const s = h; out.push({ x, y, s, cx: x + s, cy: y + s, a: [x, y + s], b: [x + s, y] }); x += s; w -= s; }
    else if (d === 1) { const s = w; out.push({ x, y, s, cx: x, cy: y + s, a: [x, y], b: [x + s, y + s] }); y += s; h -= s; }
    else if (d === 2) { const s = h; const sx = x + w - s; out.push({ x: sx, y, s, cx: sx, cy: y, a: [x + w, y], b: [sx, y + s] }); w -= s; }
    else { const s = w; const sy = y + h - s; out.push({ x, y: sy, s, cx: x + s, cy: sy, a: [x + s, y + h], b: [x, sy] }); h -= s; }
  }
  return out;
}
const FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987];
export function Ratio({ p = {} }) {
  const [m, setM] = useState(["golden", "paper", "fib"].includes(p.m) ? p.m : "golden");
  const clock = useClock({ period: 11, rest: 9.5 });
  let body, read;
  if (m === "golden") {
    const k = clamp(1 + Math.floor(clock.t / 0.9), 1, 10), W = 300, H = W / PHI, x0 = 30, y0 = 18;
    const sq = goldenSquares(x0, y0, W, H, k);
    body = (
      <g>
        <rect x={x0} y={y0} width={W} height={H} fill="none" stroke={C.ink} strokeWidth="1.4" />
        {sq.map((q, i) => <rect key={i} x={q.x} y={q.y} width={q.s} height={q.s} fill={i % 2 ? C.gold : C.teal} fillOpacity="0.13" stroke={C.mut} strokeWidth="0.8" />)}
        <path d={sq.map((q, i) => `${i ? "L" : "M"} ${q.a[0].toFixed(1)} ${q.a[1].toFixed(1)} A ${q.s.toFixed(1)} ${q.s.toFixed(1)} 0 0 1 ${q.b[0].toFixed(1)} ${q.b[1].toFixed(1)}`).join(" ")} fill="none" stroke={C.red} strokeWidth="2" />
        <text x={x0 + W / 2} y={y0 + H + 16} textAnchor="middle" fontSize="9.5" fill={C.mut}>가로 : 세로 = φ : 1 ≈ 1.618 : 1</text>
      </g>
    );
    read = <>황금비 φ = (1 + √5) ÷ 2 ≈ 1.618 · 가로 : 세로가 φ : 1 인 직사각형에서 정사각형을 떼어 내면 남은 직사각형이 처음과 닮은꼴이다 — φ = 1 + 1 ÷ φ · 이것을 되풀이해(지금 정사각형 {k} 개) 각 정사각형에 사분원을 그리면 황금 나선이 된다 · 앵무조개 껍데기가 황금 나선이라는 말은 흔한 오해다(실제 비율은 대개 다르다)</>;
  } else if (m === "paper") {
    const k = clamp(1 + Math.floor(clock.t / 1.2), 1, 7), sc = 0.205, x0 = 24, y0 = 20;
    const rects = [];
    let w = 1189, h = 841, x = 0, y = 0;
    for (let i = 0; i <= k; i++) {
      rects.push({ x, y, w, h, i });
      if (w >= h) { w /= 2; } else { h /= 2; }
    }
    body = (
      <g>
        {rects.map((r) => <rect key={r.i} x={x0 + r.x * sc} y={y0 + r.y * sc} width={r.w * sc} height={r.h * sc} fill={r.i === 4 ? C.blue : C.card} fillOpacity={r.i === 4 ? 0.12 : 1} stroke={r.i === k ? C.red : C.mut} strokeWidth={r.i === k ? 1.8 : 1} />)}
        {rects.map((r) => r.i >= 1 && r.i <= 6 && <text key={"t" + r.i} x={x0 + (r.x + r.w / 2) * sc} y={y0 + (r.y + r.h / 2) * sc + 4} textAnchor="middle" fontSize={Math.max(7, 15 - r.i * 1.6)} fill={r.i === 4 ? C.blue : C.ink}>A{r.i}</text>)}
        <text x={x0 + 1189 * sc + 6} y={y0 + 12} fontSize="9.5" fill={C.ink}>A0</text>
        <text x={x0 + 1189 * sc + 6} y={y0 + 28} fontSize="9" fill={C.mut}>841 × 1189</text>
        <text x={x0 + 1189 * sc + 6} y={y0 + 44} fontSize="9" fill={C.mut}>= 1 m²</text>
        <text x={x0 + 1189 * sc + 6} y={y0 + 76} fontSize="9" fill={C.blue}>A4</text>
        <text x={x0 + 1189 * sc + 6} y={y0 + 92} fontSize="9" fill={C.blue}>210 × 297</text>
      </g>
    );
    read = <>A 판 종이는 가로 : 세로 = 1 : √2 ≈ 1 : 1.414 — 긴 변을 반으로 접어도 비가 그대로다: 1 : x = (x ÷ 2) : 1 에서 x² = 2 · A0 는 넓이 1 m²(841 × 1189 mm), 한 번 접을 때마다 A1, A2, … (지금 A{k} 까지) · A4 는 210 × 297 mm · 그래서 A4 두 장을 A3 한 장에, A4 를 A5 두 장에 확대 · 축소해도 여백이 생기지 않는다(복사기 배율 141 % · 71 %)</>;
  } else {
    const n = clamp(2 + Math.floor(clock.t / 0.7), 2, 15);
    const P = plot({ x0: 0.5, x1: 15.5, y0: 0.9, y1: 2.1, pad: [14, 12, 40, 36] });
    const pts = Array.from({ length: n }, (_, i) => [i + 1, FIB[i + 1] / FIB[i]]);
    body = (
      <g>
        <line x1={P.l} x2={P.r} y1={P.Y(PHI)} y2={P.Y(PHI)} stroke={C.gold} strokeDasharray="5 3" strokeWidth="1.4" />
        <Label x={P.r} y={P.Y(PHI) - 6} size={9.5} color={C.gold} anchor="end">φ ≈ 1.618</Label>
        {[1, 1.5, 2].map((v) => <text key={v} x={P.l - 4} y={P.Y(v) + 3.5} textAnchor="end" fontSize="9" fill={C.mut}>{fmt(v, 1)}</text>)}
        <line x1={P.l} x2={P.l} y1={P.t} y2={P.b} stroke={C.mut} />
        <line x1={P.l} x2={P.r} y1={P.b} y2={P.b} stroke={C.mut} />
        <path d={P.poly(pts)} fill="none" stroke={C.red} strokeWidth="1.4" />
        {pts.map(([x, y]) => <circle key={x} cx={P.X(x)} cy={P.Y(y)} r="3.4" fill={C.red} />)}
        {pts.slice(0, 7).map(([x, y]) => <text key={"l" + x} x={P.X(x)} y={P.Y(y) + (x % 2 ? -8 : 15)} textAnchor="middle" fontSize="8.5" fill={C.ink}>{`${FIB[x]}/${FIB[x - 1]}`}</text>)}
        <text x={P.l} y={P.b + 16} fontSize="9" fill={C.mut}>{FIB.slice(0, Math.min(n + 1, 13)).join(", ")} …</text>
        <text x={P.r} y={P.b + 30} textAnchor="end" fontSize="9" fill={C.mut}>n →</text>
      </g>
    );
    read = <>피보나치 수 1, 1, 2, 3, 5, 8, 13 … 에서 이웃한 두 수의 비(뒤 ÷ 앞)는 φ 를 사이에 두고 번갈아 넘나들며 다가간다 — 지금 {FIB[n]} ÷ {FIB[n - 1]} = {fmt(FIB[n] / FIB[n - 1], 5)} · φ 의 연분수는 [1; 1, 1, 1, …] 로 1 만 이어져, 분수로 가장 느리게 다가가는 ‘가장 무리한’ 무리수다 · 해바라기 씨가 φ 와 관련된 각(약 137.5°)으로 놓여 나선의 수가 피보나치 수가 된다</>;
  }
  return (
    <Frame clock={clock} title="비율 — 황금비와 종이의 √2" read={read}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["golden", "황금 직사각형"], ["paper", "종이(√2)"], ["fib", "피보나치"]]} />}>
      {body}
    </Frame>
  );
}

/* ── 띠 무늬 7 가지 ── */
const MOTIF = [[0.12, 0.14], [0.22, 0.14], [0.22, 0.52], [0.41, 0.72], [0.34, 0.86], [0.16, 0.62], [0.12, 0.62]];
const FRIEZE = [
  { nm: "깡충", code: "p1", d: "평행이동만 — 같은 모양이 한 방향으로 줄지어 간다", T: [(u, v) => [u, v]], mv: [], mh: false, rot: [], gl: false },
  { nm: "걸음", code: "p11g", d: "미끄럼 반사 — 뒤집으며 반 칸씩 나아간다(모래 위의 발자국)", T: [(u, v) => [u, v], (u, v) => [u + 0.5, -v]], mv: [], mh: false, rot: [], gl: true },
  { nm: "옆걸음", code: "p1m1", d: "세로 거울 — 좌우가 맞비친다", T: [(u, v) => [u, v], (u, v) => [-u, v]], mv: [0, 0.5], mh: false, rot: [], gl: false },
  { nm: "점프", code: "p11m", d: "가로 거울 — 위아래가 맞비친다", T: [(u, v) => [u, v], (u, v) => [u, -v]], mv: [], mh: true, rot: [], gl: false },
  { nm: "회전 깡충", code: "p2", d: "반 바퀴 돌림 — 거꾸로 돌려도 같다", T: [(u, v) => [u, v], (u, v) => [-u, -v]], mv: [], mh: false, rot: [0, 0.5], gl: false },
  { nm: "회전 옆걸음", code: "p2mg", d: "세로 거울과 미끄럼 반사 — 반 바퀴 돌림이 저절로 따라 나온다", T: [(u, v) => [u, v], (u, v) => [-u, v], (u, v) => [u + 0.5, -v], (u, v) => [0.5 - u, -v]], mv: [0, 0.5], mh: false, rot: [0.25, 0.75], gl: true },
  { nm: "회전 점프", code: "p2mm", d: "세로 거울과 가로 거울 — 둘이 만나는 곳마다 반 바퀴 돌림", T: [(u, v) => [u, v], (u, v) => [-u, v], (u, v) => [u, -v], (u, v) => [-u, -v]], mv: [0, 0.5], mh: true, rot: [0, 0.5], gl: false },
];
export function Frieze({ p = {} }) {
  const [k, setK] = useState(clamp(p.k ?? 6, 1, 7));
  const clock = useClock({ period: 12, rest: 1.2 });
  const F = FRIEZE[k - 1], P = 64, x0 = 10, cy = 110, V = 52;
  const off = ((clock.t / 3) % 1) * P;
  const X = (u) => x0 + u * P - off, Y = (v) => cy - v * V;
  const shapes = [];
  for (let c = -1; c <= 6; c++) F.T.forEach((f, j) => shapes.push({ key: c + "_" + j, pts: MOTIF.map(([u, v]) => { const [a, b] = f(u, v); return [X(a + c), Y(b)]; }), dot: (() => { const [a, b] = f(0.33, 0.3); return [X(a + c), Y(b)]; })() }));
  return (
    <Frame clock={clock} title="띠 무늬 — 대칭의 조합은 7 가지뿐"
      read={<>한 방향으로 끝없이 되풀이되는 띠 무늬에 쓸 수 있는 대칭의 조합은 정확히 7 가지뿐이다 · 지금 {k}. {F.nm}({F.code}): {F.d} · 무늬는 한 칸만큼 밀어도 똑같다(평행이동 대칭) — 그래서 끝없이 흘러가는 것처럼 보인다 · 점선 = 거울, ◆ = 반 바퀴 돌림의 중심, 긴 점선 = 미끄럼 반사의 축 · 단청과 기와의 무늬, 그리스 건축의 띠 장식에서 7 가지를 모두 찾을 수 있다</>}
      controls={<Slider label="무늬 번호" min={1} max={7} step={1} value={k} onChange={setK} show={(v) => `${v}. ${FRIEZE[v - 1].nm}`} />}>
      <defs><clipPath id="ma-frieze-band"><rect x={x0} y={cy - V - 8} width={340} height={2 * V + 16} /></clipPath></defs>
      <text x={x0} y="30" fontSize="11" fill={C.ink}>{k}. {F.nm}</text>
      <text x={350} y="30" textAnchor="end" fontSize="10" fill={C.mut}>{F.code}</text>
      <rect x={x0} y={cy - V - 8} width={340} height={2 * V + 16} fill={C.gold} fillOpacity="0.06" stroke={C.bd} />
      <g clipPath="url(#ma-frieze-band)">
        {shapes.map((s) => <g key={s.key}><path d={pth(s.pts) + "Z"} fill={C.blue} fillOpacity="0.75" stroke={C.blue} /><circle cx={s.dot[0]} cy={s.dot[1]} r="3.2" fill={C.red} /></g>)}
        {[-1, 0, 1, 2, 3, 4, 5, 6].flatMap((c) => F.mv.map((u) => <line key={"m" + c + u} x1={X(c + u)} x2={X(c + u)} y1={cy - V - 8} y2={cy + V + 8} stroke={C.red} strokeWidth="1.2" strokeDasharray="4 3" />))}
        {F.mh && <line x1={x0} x2={x0 + 340} y1={cy} y2={cy} stroke={C.red} strokeWidth="1.2" strokeDasharray="4 3" />}
        {F.gl && !F.mh && <line x1={x0} x2={x0 + 340} y1={cy} y2={cy} stroke={C.violet} strokeWidth="1.4" strokeDasharray="10 4 2 4" />}
        {[-1, 0, 1, 2, 3, 4, 5, 6].flatMap((c) => F.rot.map((u) => <path key={"r" + c + u} d={`M ${X(c + u)} ${cy - 6} L ${X(c + u) + 5} ${cy} L ${X(c + u)} ${cy + 6} L ${X(c + u) - 5} ${cy} Z`} fill={C.gold} stroke={C.ink} strokeWidth="0.6" />))}
      </g>
      <text x={x0} y="196" fontSize="9" fill={C.red}>┆ 거울</text>
      <text x={x0 + 58} y="196" fontSize="9" fill={C.gold}>◆ 반 바퀴 돌림</text>
      <text x={x0 + 150} y="196" fontSize="9" fill={C.violet}>─ · ─ 미끄럼 반사</text>
    </Frame>
  );
}

/* ── 쪽매맞춤: 꼭짓점에 정다각형 모으기 · 에셔식 변 바꾸기 ── */
const PNAME = { 3: "정삼각형", 4: "정사각형", 5: "정오각형", 6: "정육각형", 7: "정칠각형", 8: "정팔각형", 9: "정구각형", 10: "정십각형" };
export function Tiling({ p = {} }) {
  const [m, setM] = useState(p.m === "escher" ? "escher" : "around");
  const [n, setN] = useState(clamp(p.n ?? 5, 3, 10));
  const clock = useClock({ period: 10, rest: 6 });
  if (m === "around") {
    const a = (180 * (n - 2)) / n, ext = 360 / n, c = Math.floor(360 / a + 1e-9), gap = 360 - c * a, s = 44, cx = 120, cy = 112;
    const shown = clamp(1 + Math.floor(clock.t / 0.8), 1, c);
    const poly = (j) => { let x = 0, y = 0, d = j * a; const out = [[x, y]]; for (let i = 0; i < n - 1; i++) { x += s * Math.cos((d * Math.PI) / 180); y += s * Math.sin((d * Math.PI) / 180); out.push([x, y]); d += ext; } return out.map(([u, v]) => [cx + u, cy - v]); };
    const wedge = gap > 0.01 && shown === c ? (() => { const r = 34, a0 = (c * a * Math.PI) / 180, a1 = TAU; const pts = [[cx, cy]]; for (let i = 0; i <= 24; i++) { const t = a0 + ((a1 - a0) * i) / 24; pts.push([cx + r * Math.cos(t), cy - r * Math.sin(t)]); } return pth(pts) + "Z"; })() : null;
    return (
      <Frame clock={clock} title="쪽매맞춤 — 한 꼭짓점에 360°"
        read={<>한 꼭짓점에 {PNAME[n]}을 모은다 — 내각 {fmt(a, 2)}° 가 {c} 개, 합 {fmt(c * a, 1)}° · {gap > 0.01 ? <>{fmt(gap, 1)}° 의 틈이 남아 바닥을 빈틈없이 덮지 못한다</> : <b>딱 360° — 빈틈없이 깔린다</b>} · 정n각형의 내각은 180(n − 2) ÷ n 이고, 이것이 360 의 약수여야 하므로 정다각형 한 가지로 바닥을 까는 방법은 정삼각형 · 정사각형 · 정육각형 셋뿐이다(벌집이 육각형인 것도 이 가운데 같은 넓이를 가장 짧은 둘레로 나누는 모양이기 때문)</>}
        controls={<>
          <Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["around", "꼭짓점에 모으기"], ["escher", "에셔 쪽매"]]} />
          <Slider label="변의 수 n" min={3} max={10} step={1} value={n} onChange={(v) => { setN(v); clock.reset(); }} />
        </>}>
        {Array.from({ length: shown }, (_, j) => <path key={j} d={pth(poly(j)) + "Z"} fill={[C.teal, C.gold, C.blue, C.violet, C.green, C.red][j % 6]} fillOpacity="0.3" stroke={C.ink} strokeWidth="1.2" />)}
        {wedge && <path d={wedge} fill={C.red} fillOpacity="0.45" stroke={C.red} />}
        <circle cx={cx} cy={cy} r="3" fill={C.ink} />
        <text x="250" y="50" fontSize="10.5" fill={C.ink}>{PNAME[n]}</text>
        <text x="250" y="72" fontSize="10" fill={C.mut}>내각 {fmt(a, 1)}°</text>
        <text x="250" y="92" fontSize="10" fill={C.mut}>{c} 개 → {fmt(c * a, 1)}°</text>
        <text x="250" y="116" fontSize="10.5" fill={gap > 0.01 ? C.red : C.green}>{gap > 0.01 ? `틈 ${fmt(gap, 1)}°` : "딱 맞는다"}</text>
      </Frame>
    );
  }
  const A = 0.5 - 0.5 * Math.cos(Math.PI * clamp(clock.t / 5, 0, 1));
  const f = (u) => A * (0.2 * Math.sin(TAU * u) + 0.07 * Math.sin(2 * TAU * u));
  const g = (v) => A * (0.18 * Math.sin(TAU * v) - 0.06 * Math.sin(3 * TAU * v));
  const S = 46, ox = 22, oy = 196;
  const tile = (i, j) => {
    const pts = [];
    for (let k = 0; k <= 16; k++) { const u = k / 16; pts.push([u, f(u)]); }
    for (let k = 1; k <= 16; k++) { const v = k / 16; pts.push([1 + g(v), v]); }
    for (let k = 15; k >= 0; k--) { const u = k / 16; pts.push([u, 1 + f(u)]); }
    for (let k = 15; k >= 1; k--) { const v = k / 16; pts.push([g(v), v]); }
    return pts.map(([u, v]) => [ox + (i + u) * S, oy - (j + v) * S]);
  };
  return (
    <Frame clock={clock} title="쪽매맞춤 — 에셔처럼 변을 바꾸기"
      read={<>정사각형의 아래 변을 구부린 만큼 위 변도 똑같이 구부리고, 왼쪽 변을 구부린 만큼 오른쪽 변도 똑같이 구부린다 — 모양은 달라져도 이웃한 조각이 평행이동으로 딱 맞물려 틈 없이 깔린다 · 지금 구부린 정도 {fmt(A * 100, 0)} % · 에셔가 새 · 물고기 · 도마뱀 쪽매를 만든 방법이고, 돌림이나 미끄럼 반사로 짝을 지으면 더 많은 모양이 나온다</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["around", "꼭짓점에 모으기"], ["escher", "에셔 쪽매"]]} />}>
      {Array.from({ length: 7 }, (_, i) => Array.from({ length: 4 }, (_, j) => (
        <g key={i + "_" + j}>
          <path d={pth(tile(i, j)) + "Z"} fill={(i + j) % 2 ? C.gold : C.teal} fillOpacity="0.4" stroke={C.ink} strokeWidth="0.9" />
          <circle cx={ox + (i + 0.68) * S} cy={oy - (j + 0.62) * S} r="2.4" fill={C.ink} />
        </g>
      )))}
    </Frame>
  );
}

/* ── 베지에 곡선과 드 카스텔조 ── */
const BEZ = { cubic: [[30, 176], [92, 22], [168, 210], [236, 40]], quad: [[30, 176], [132, 8], [236, 160]] };
const lerp2 = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
function casteljau(P, t) { const lv = [P]; while (lv[lv.length - 1].length > 1) { const q = lv[lv.length - 1]; lv.push(q.slice(1).map((b, i) => lerp2(q[i], b, t))); } return lv; }
const binom = (n, k) => { let r = 1; for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i; return r; };
export function Bezier({ p = {} }) {
  const [m, setM] = useState(p.m === "quad" ? "quad" : "cubic");
  const clock = useClock({ period: 9, rest: 4.3 });
  const t = clamp(clock.t / 7, 0, 1), P = BEZ[m], n = P.length - 1;
  const lv = casteljau(P, t), pt = lv[lv.length - 1][0];
  const curve = (a, b) => Array.from({ length: 81 }, (_, i) => casteljau(P, a + ((b - a) * i) / 80).slice(-1)[0][0]);
  const cols = [C.mut, C.blue, C.green, C.red];
  const w = Array.from({ length: n + 1 }, (_, i) => binom(n, i) * (1 - t) ** (n - i) * t ** i);
  return (
    <Frame clock={clock} title="베지에 곡선 — 나누기를 되풀이해 곡선을 그린다"
      read={m === "cubic"
        ? <>B(t) = (1 − t)³P₀ + 3(1 − t)²t P₁ + 3(1 − t)t² P₂ + t³P₃ · 지금 t = {fmt(t, 2)} · 드 카스텔조의 방법: 이웃한 두 점 사이를 t : (1 − t) 로 나누는 일을 세 번 되풀이하면(파랑 → 초록 → 빨강) 곡선 위의 점이 나온다 · 오른쪽 막대 = 네 조절점의 무게(번스타인 다항식, 합은 늘 1) · 곡선은 P₀ 에서 P₁ 쪽으로 떠나 P₂ 쪽에서 P₃ 로 들어온다 — 펜 도구 · 글꼴(포스트스크립트) · 로고의 곡선</>
        : <>B(t) = (1 − t)²P₀ + 2(1 − t)t P₁ + t²P₂ · 지금 t = {fmt(t, 2)} · 두 번 나누면(파랑 → 빨강) 곡선 위의 점 — 조절점이 셋인 2차 곡선은 포물선의 한 조각이다 · 트루타입 글꼴은 이 2차 곡선을 이어 글자의 윤곽을 만든다</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["cubic", "3차(점 4 개)"], ["quad", "2차(점 3 개)"]]} />}>
      <path d={pth(curve(0, 1))} fill="none" stroke={C.red} strokeWidth="1.2" opacity="0.25" />
      <path d={pth(curve(0, t))} fill="none" stroke={C.red} strokeWidth="2.6" />
      {lv.slice(0, -1).map((q, L) => (
        <g key={L}>
          <path d={pth(q)} fill="none" stroke={cols[L]} strokeWidth={L ? 1.3 : 1} strokeDasharray={L ? undefined : "4 3"} />
          {q.map(([x, y], i) => <circle key={i} cx={x} cy={y} r={L ? 3 : 5} fill={L ? cols[L] : C.card} stroke={cols[L]} strokeWidth="1.5" />)}
        </g>
      ))}
      {P.map(([x, y], i) => <text key={"p" + i} x={x + (i === 0 ? -6 : 8)} y={y + (y > 110 ? 16 : -6)} fontSize="10" fill={C.ink} textAnchor={i === 0 ? "end" : "start"}>{`P${"₀₁₂₃"[i]}`}</text>)}
      <circle cx={pt[0]} cy={pt[1]} r="5.5" fill={C.red} />
      {w.map((v, i) => (
        <g key={"w" + i}>
          <rect x={270 + i * 20} y={190 - v * 150} width="14" height={v * 150} fill={C.violet} fillOpacity="0.75" />
          <text x={277 + i * 20} y="204" textAnchor="middle" fontSize="9" fill={C.ink}>{`P${"₀₁₂₃"[i]}`}</text>
        </g>
      ))}
      <line x1="266" x2="350" y1="190" y2="190" stroke={C.mut} />
      <text x="266" y="28" fontSize="9" fill={C.violet}>무게</text>
    </Frame>
  );
}

/* ── 명도 대비: 상대 휘도와 대비비 ── */
const lin = (v) => { const c = v / 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
const ratio = (a, b) => { const A = lum(a), B = lum(b); return (Math.max(A, B) + 0.05) / (Math.min(A, B) + 0.05); };
const BGS = { white: [[255, 255, 255], "흰 바탕"], black: [[0, 0, 0], "검은 바탕"], blue: [[47, 109, 176], "파란 바탕"] };
const hex = ([r, g, b]) => "#" + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, "0")).join("");
export function Contrast({ p = {} }) {
  const [bg, setBg] = useState(BGS[p.bg] ? p.bg : "white");
  const [gv, setGv] = useState(null);
  const clock = useClock({ period: 12, rest: 5.2 });
  const sweep = Math.round(255 * (0.5 - 0.5 * Math.cos((Math.PI * clock.t) / 6)));
  const g = gv ?? sweep, B = BGS[bg][0], fg = [g, g, g], r = ratio(fg, B);
  const curve = useMemo(() => Array.from({ length: 256 }, (_, i) => ratio([i, i, i], B)), [bg]);
  const X = (v) => 196 + (v / 255) * 150, Y = (q) => 176 - (Math.log(q) / Math.log(21)) * 150;
  const verdict = r >= 7 ? "AAA 통과(아주 잘 읽힘)" : r >= 4.5 ? "AA 통과(본문 글씨 가능)" : r >= 3 ? "큰 글씨만 AA" : "기준 미달(읽기 어려움)";
  return (
    <Frame clock={clock} title="명도 대비 — 글씨가 잘 읽히는 수"
      read={<>상대 휘도 L = 0.2126R + 0.7152G + 0.0722B(감마를 풀어 빛의 양으로 바꾼 값) · 대비비 = (밝은 쪽 L + 0.05) ÷ (어두운 쪽 L + 0.05) — 1 에서 21 사이 · 지금 글자 밝기 {g} → 대비비 <b>{fmt(r, 2)} : 1</b>, {verdict} · 웹 접근성 기준(WCAG): 본문 4.5 : 1, 큰 글씨 3 : 1 이상(AAA 는 7 : 1) · 같은 밝기 값이라도 초록은 밝게, 파랑은 어둡게 보인다</>}
      controls={<>
        <Seg value={bg} onChange={(v) => { setBg(v); clock.reset(); }} options={[["white", "흰 바탕"], ["black", "검은 바탕"], ["blue", "파란 바탕"]]} />
        <Slider label="글자 밝기" min={0} max={255} step={1} value={g} onChange={setGv} />
      </>}>
      <rect x="12" y="20" width="166" height="156" rx="8" fill={hex(B)} stroke={C.bd} />
      <text x="95" y="74" textAnchor="middle" fontSize="26" fontWeight="700" fill={hex(fg)}>가나다 Aa</text>
      <text x="95" y="104" textAnchor="middle" fontSize="12" fill={hex(fg)}>본문 크기의 글씨는</text>
      <text x="95" y="122" textAnchor="middle" fontSize="12" fill={hex(fg)}>대비가 4.5 : 1 은 되어야</text>
      <text x="95" y="140" textAnchor="middle" fontSize="12" fill={hex(fg)}>편하게 읽힌다</text>
      <text x="95" y="196" textAnchor="middle" fontSize="10" fill={C.ink}>{BGS[bg][1]} · 글자 {hex(fg)}</text>
      {[[3, "3"], [4.5, "4.5"], [7, "7"]].map(([q, s]) => <g key={s}><line x1={X(0)} x2={X(255)} y1={Y(q)} y2={Y(q)} stroke={q === 4.5 ? C.green : C.bd} strokeDasharray="4 3" /><text x={X(0) - 4} y={Y(q) + 3.5} textAnchor="end" fontSize="8.5" fill={C.mut}>{s}</text></g>)}
      {[1, 21].map((q) => <text key={q} x={X(0) - 4} y={Y(q) + 3.5} textAnchor="end" fontSize="8.5" fill={C.mut}>{q}</text>)}
      <line x1={X(0)} x2={X(0)} y1={Y(21)} y2={Y(1)} stroke={C.mut} />
      <line x1={X(0)} x2={X(255)} y1={Y(1)} y2={Y(1)} stroke={C.mut} />
      <path d={pth(curve.map((q, i) => [X(i), Y(q)]))} fill="none" stroke={C.blue} strokeWidth="2" />
      <circle cx={X(g)} cy={Y(r)} r="4.5" fill={r >= 4.5 ? C.green : C.red} />
      <text x={X(0)} y="198" fontSize="8.5" fill={C.mut}>검정</text>
      <text x={X(255)} y="198" textAnchor="end" fontSize="8.5" fill={C.mut}>흰색</text>
      <text x={X(128)} y="212" textAnchor="middle" fontSize="8.5" fill={C.mut}>글자 밝기 →</text>
      <text x={X(0) + 4} y={Y(21) + 2} fontSize="9" fill={C.ink}>대비비(로그 눈금)</text>
    </Frame>
  );
}

/* ── 원근: 소실점 ── */
const BOXES = [[-1.5, 1.5, -1.5, 1.5, 2.4], [2.6, 3.6, -3.8, -2.8, 1.0]];
export function Persp({ p = {} }) {
  const [m, setM] = useState(p.m === "one" ? "one" : "two");
  const clock = useClock({ period: 12, rest: 6 });
  const th = m === "one" ? 0 : ((45 + 3 * Math.sin((TAU * clock.t) / 12)) * Math.PI) / 180;
  const R = m === "one" ? 10 - 3 * (0.5 - 0.5 * Math.cos((TAU * clock.t) / 12)) : 9;
  const fw = [Math.sin(th), Math.cos(th)], rt = [Math.cos(th), -Math.sin(th)], cp = [-R * fw[0], -R * fw[1]];
  const h = 1.6, Fo = 150, sx0 = 180, sy0 = 92;
  const cam = ([X, Y, Z]) => { const dx = X - cp[0], dz = Z - cp[1]; return [dx * rt[0] + dz * rt[1], Y - h, dx * fw[0] + dz * fw[1]]; };
  const proj = ([x, y, z]) => [sx0 + (Fo * x) / z, sy0 - (Fo * y) / z];
  const seg = (A, B) => {
    let a = cam(A), b = cam(B);
    const nz = 0.3;
    if (a[2] < nz && b[2] < nz) return null;
    if (a[2] < nz) { const t = (nz - a[2]) / (b[2] - a[2]); a = a.map((v, i) => v + (b[i] - v) * t); }
    if (b[2] < nz) { const t = (nz - b[2]) / (a[2] - b[2]); b = b.map((v, i) => v + (a[i] - v) * t); }
    const p1 = proj(a), p2 = proj(b);
    return `M ${p1[0].toFixed(1)} ${p1[1].toFixed(1)} L ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  };
  const floor = [];
  for (let k = -4; k <= 4; k++) { floor.push(seg([k * 1.5, 0, -6], [k * 1.5, 0, 6])); floor.push(seg([-6, 0, k * 1.5], [6, 0, k * 1.5])); }
  const boxEdges = BOXES.flatMap(([x0, x1, z0, z1, H]) => {
    const c = [[x0, 0, z0], [x1, 0, z0], [x1, 0, z1], [x0, 0, z1]], top = c.map(([x, , z]) => [x, H, z]);
    return [0, 1, 2, 3].flatMap((i) => [seg(c[i], c[(i + 1) % 4]), seg(top[i], top[(i + 1) % 4]), seg(c[i], top[i])]);
  });
  const vpZ = [sx0 - Fo * Math.tan(th), sy0], vpX = th > 0.01 ? [sx0 + Fo / Math.tan(th), sy0] : null;
  const inV = (q) => q && q[0] > 4 && q[0] < 356;
  const [x0, x1, z0, z1, H] = BOXES[0];
  const zc = [[x0, H, z0], [x1, H, z0], [x0, 0, z0], [x1, 0, z0]], xc = [[x0, H, z0], [x0, H, z1], [x0, 0, z0], [x0, 0, z1]];
  return (
    <Frame clock={clock} title="원근 — 평행선은 소실점에서 만난다"
      read={<>눈에서 본 점 (X, Y, Z) 는 화면의 (F × X ÷ Z, F × Y ÷ Z) 에 그려진다 — 멀수록(Z 가 클수록) 작게 · 그래서 바닥의 평행한 선들은 눈높이의 지평선(점선) 위 한 점, 소실점으로 모인다 · {m === "one" ? "한 점 투시: 정면을 보면 깊이 방향의 선만 가운데 소실점으로 모이고, 가로선은 수평 그대로다 — 앞으로 다가가도 소실점은 제자리" : "두 점 투시: 모서리를 보면 두 방향의 선이 지평선 위의 두 소실점(빨강 · 파랑)으로 각각 모이고, 세로선은 세로 그대로다"} · 눈높이보다 높은 모서리는 내려가며, 낮은 모서리는 올라가며 모인다 · 15 세기 브루넬레스키와 알베르티가 화가를 위해 정리했다</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["one", "한 점 투시"], ["two", "두 점 투시"]]} />}>
      <defs><clipPath id="ma-persp-view"><rect x="4" y="6" width="352" height="210" /></clipPath></defs>
      <g clipPath="url(#ma-persp-view)">
        {floor.map((d, i) => d && <path key={"f" + i} d={d} stroke={C.mut} strokeWidth="0.8" opacity="0.55" />)}
        <line x1="4" x2="356" y1={sy0} y2={sy0} stroke={C.gold} strokeDasharray="5 4" />
        {inV(vpZ) && (m === "one" ? [[x0, H, z0], [x1, H, z0], [x0, 0, z0], [x1, 0, z0]] : zc.map(([x, y, z]) => [x1 - x + x0, y, z])).map((q, i) => { const s = proj(cam(q)); return <line key={"vz" + i} x1={s[0]} y1={s[1]} x2={vpZ[0]} y2={vpZ[1]} stroke={C.red} strokeWidth="0.8" strokeDasharray="3 3" />; })}
        {inV(vpX) && xc.map((q, i) => { const s = proj(cam(q)); return <line key={"vx" + i} x1={s[0]} y1={s[1]} x2={vpX[0]} y2={vpX[1]} stroke={C.blue} strokeWidth="0.8" strokeDasharray="3 3" />; })}
        {boxEdges.map((d, i) => d && <path key={"b" + i} d={d} stroke={C.ink} strokeWidth="1.6" />)}
        {inV(vpZ) && <circle cx={vpZ[0]} cy={vpZ[1]} r="4.5" fill={C.red} />}
        {inV(vpX) && <circle cx={vpX[0]} cy={vpX[1]} r="4.5" fill={C.blue} />}
      </g>
      <text x="8" y={sy0 + 14} fontSize="9" fill={C.gold}>지평선(눈높이)</text>
      {inV(vpZ) && <Label x={vpZ[0]} y={vpZ[1] - 10} size={9} color={C.red} anchor="middle" bg>소실점</Label>}
      {inV(vpX) && <Label x={vpX[0]} y={vpX[1] - 10} size={9} color={C.blue} anchor="middle" bg>소실점 2</Label>}
    </Frame>
  );
}

/* ── 피츠 법칙 ── */
export function Fitts({ p = {} }) {
  const [m, setM] = useState(p.m === "edge" ? "edge" : "mid");
  const [D, setD] = useState(clamp(p.D ?? 240, 60, 300));
  const [W, setW] = useState(clamp(p.W ?? 20, 8, 80));
  const clock = useClock({ period: 30, rest: 0.55 });
  const We = m === "edge" ? 200 : W, ID = Math.log2(D / We + 1), MT = 0.1 + 0.15 * ID;
  const cyc = MT + 0.9, ph = clock.t % cyc, tau = clamp(ph / MT, 0, 1), s = 10 * tau ** 3 - 15 * tau ** 4 + 6 * tau ** 5;
  const x0 = 28, tx = m === "edge" ? 346 : x0 + D, cxp = x0 + s * (tx - x0);
  const P = plot({ x0: 0, x1: 6, y0: 0, y1: 1.1, pad: [130, 14, 22, 40] });
  return (
    <Frame clock={clock} title="피츠 법칙 — 멀고 작을수록 오래 걸린다"
      read={<>목표를 가리키는 시간 T = a + b × log₂(D ÷ W + 1)(피츠, 1954) · {m === "edge" ? <>화면 모서리의 목표는 커서가 넘어가지 않으니 너비가 끝없이 큰 것과 같다 — 여기서는 W = 200 으로 어림 · 어려움 {fmt(ID, 2)} 비트</> : <>거리 D = {D}, 너비 W = {W} → 어려움 {fmt(ID, 2)} 비트</>}, 예상 시간 <b>{fmt(MT, 2)} 초</b>(a = 0.1 초, b = 0.15 초/비트로 어림) · 거리를 두 배로 하거나 너비를 절반으로 하면 약 1 비트 어려워진다 · 자주 누르는 단추는 크게, 가까이 — 운영 체제가 메뉴 막대를 화면 가장자리에 붙이는 까닭</>}
      controls={<>
        <Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["mid", "가운데 목표"], ["edge", "모서리 목표"]]} />
        {m === "mid" && <Slider label="거리 D" min={60} max={300} step={10} value={D} onChange={setD} />}
        {m === "mid" && <Slider label="너비 W" min={8} max={80} step={2} value={W} onChange={setW} />}
      </>}>
      <rect x="10" y="10" width="340" height="100" rx="6" fill={C.blue} fillOpacity="0.05" stroke={C.bd} />
      {m === "edge"
        ? <rect x="342" y="10" width="8" height="100" fill={C.green} fillOpacity="0.6" />
        : <rect x={tx - W / 2} y="30" width={W} height="60" rx="3" fill={C.green} fillOpacity="0.6" stroke={C.green} />}
      <circle cx={x0} cy="60" r="4" fill={C.mut} />
      <line x1={x0} x2={tx} y1="100" y2="100" stroke={C.mut} strokeDasharray="3 3" />
      <text x={(x0 + tx) / 2} y="97" textAnchor="middle" fontSize="9" fill={C.mut}>D</text>
      <path d={`M ${cxp} 52 l 0 14 l 4 -4 l 3 7 l 2.4 -1 l -3 -7 l 5.6 0 z`} fill={C.ink} stroke={C.card} strokeWidth="0.8" />
      <line x1={P.l} x2={P.r} y1={P.b} y2={P.b} stroke={C.mut} />
      <line x1={P.l} x2={P.l} y1={P.t} y2={P.b} stroke={C.mut} />
      {[0, 2, 4, 6].map((v) => <text key={v} x={P.X(v)} y={P.b + 12} textAnchor="middle" fontSize="8.5" fill={C.mut}>{v}</text>)}
      {[0.5, 1].map((v) => <text key={v} x={P.l - 4} y={P.Y(v) + 3} textAnchor="end" fontSize="8.5" fill={C.mut}>{fmt(v, 1)} 초</text>)}
      <path d={P.path((x) => 0.1 + 0.15 * x, 0, 6, 2)} fill="none" stroke={C.blue} strokeWidth="1.6" />
      <circle cx={P.X(ID)} cy={P.Y(MT)} r="4.5" fill={C.red} />
      <text x={P.r} y={P.b - 4} textAnchor="end" fontSize="9" fill={C.mut}>어려움 log₂(D ÷ W + 1) 비트 →</text>
    </Frame>
  );
}

/* ── 프랙탈: 코흐 눈송이 · 시에르핀스키 삼각형 · 나무 ── */
function koch(n) {
  const s = 150, h = (s * Math.sqrt(3)) / 2, cx = 112, cy = 120;
  let pts = [[cx - s / 2, cy + h / 3], [cx, cy - (2 * h) / 3], [cx + s / 2, cy + h / 3], [cx - s / 2, cy + h / 3]];
  for (let k = 0; k < n; k++) {
    const out = [pts[0]];
    for (let i = 0; i < pts.length - 1; i++) {
      const [ax, ay] = pts[i], [bx, by] = pts[i + 1], dx = (bx - ax) / 3, dy = (by - ay) / 3;
      const p1 = [ax + dx, ay + dy], p3 = [ax + 2 * dx, ay + 2 * dy];
      const p2 = [p1[0] + dx * 0.5 + dy * (Math.sqrt(3) / 2), p1[1] + dy * 0.5 - dx * (Math.sqrt(3) / 2)];
      out.push(p1, p2, p3, [bx, by]);
    }
    pts = out;
  }
  return pts;
}
function sierp(n) {
  let tris = [[[37, 190], [187, 190], [112, 190 - 150 * (Math.sqrt(3) / 2)]]];
  for (let k = 0; k < n; k++) tris = tris.flatMap(([a, b, c]) => { const m = (p, q) => [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; const ab = m(a, b), bc = m(b, c), ca = m(c, a); return [[a, ab, ca], [ab, b, bc], [ca, bc, c]]; });
  return tris;
}
function tree(n) {
  const segs = [];
  const go = (x, y, a, L, d) => { const x2 = x + L * Math.cos(a), y2 = y - L * Math.sin(a); segs.push([x, y, x2, y2, d]); if (d < n) { go(x2, y2, a + 0.44, L * 0.7, d + 1); go(x2, y2, a - 0.44, L * 0.7, d + 1); } };
  go(112, 204, Math.PI / 2, 52, 0);
  return segs;
}
export function LSystem({ p = {} }) {
  const [m, setM] = useState(["koch", "sierp", "tree"].includes(p.m) ? p.m : "koch");
  const clock = useClock({ period: 12, rest: 7 });
  const maxN = m === "tree" ? 8 : 5, n = clamp(Math.floor(clock.t / 1.4), 0, maxN);
  const shapes = useMemo(() => Array.from({ length: maxN + 1 }, (_, k) => (m === "koch" ? koch(k) : m === "sierp" ? sierp(k) : tree(k))), [m]);
  const sh = shapes[n];
  let stats, read;
  if (m === "koch") {
    stats = [["단계", `${n}`], ["변의 수", `${3 * 4 ** n}`], ["둘레", `× ${fmt((4 / 3) ** n, 3)}`], ["넓이", `× ${fmt(1.6 - 0.6 * (4 / 9) ** n, 4)}`], ["차원", "≈ 1.262"]];
    read = <>코흐 눈송이: 정삼각형의 각 변을 세 등분해 가운데에 작은 정삼각형을 붙이기를 되풀이한다 · 한 번마다 둘레가 4/3 배 — 끝없이 길어진다 · 넓이는 처음의 8/5 배로 수렴 — 유한한 넓이를 무한한 둘레가 감싼다 · 크기를 3 분의 1 로 줄인 닮은꼴 4 개로 이루어지므로 프랙탈 차원 = log 4 ÷ log 3 ≈ 1.262 — 선(1 차원)과 면(2 차원) 사이</>;
  } else if (m === "sierp") {
    stats = [["단계", `${n}`], ["삼각형", `${3 ** n} 개`], ["넓이", `× ${fmt(0.75 ** n, 4)}`], ["차원", "≈ 1.585"]];
    read = <>시에르핀스키 삼각형: 삼각형을 넷으로 나눠 가운데를 빼는 일을 되풀이한다 · 단계마다 남는 넓이가 3/4 배 — 끝내 0 으로 간다 · 크기를 절반으로 줄인 닮은꼴 3 개로 이루어지므로 차원 = log 3 ÷ log 2 ≈ 1.585 · 파스칼 삼각형의 홀수만 칠해도 같은 무늬가 나온다</>;
  } else {
    const tot = Array.from({ length: n + 1 }, (_, k) => 1.4 ** k).reduce((a, b) => a + b, 0);
    stats = [["단계", `${n}`], ["가지", `${2 ** (n + 1) - 1} 개`], ["줄기 비", "0.7"], ["총 길이", `× ${fmt(tot, 2)}`]];
    read = <>나무: 줄기 끝에서 0.7 배 길이의 가지 두 개를 ±25° 로 뻗기를 되풀이한다(L-시스템의 규칙 하나) · 가지 수는 2ⁿ⁺¹ − 1 개, 총 길이는 1 + 1.4 + 1.4² + … 로 끝없이 늘지만 나무 전체는 정해진 상자 안에 머문다 · 규칙 몇 줄로 식물 · 번개 · 강줄기 같은 복잡한 모양을 만드는 생성 디자인의 기본</>;
  }
  return (
    <Frame clock={clock} title="프랙탈 — 규칙 하나를 되풀이하면" read={read}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["koch", "코흐 눈송이"], ["sierp", "시에르핀스키"], ["tree", "나무"]]} />}>
      {m === "koch" && <path d={pth(sh) + "Z"} fill={C.blue} fillOpacity="0.15" stroke={C.blue} strokeWidth="1.2" />}
      {m === "sierp" && sh.map((t, i) => <path key={i} d={pth(t) + "Z"} fill={C.violet} fillOpacity="0.7" stroke="none" />)}
      {m === "tree" && sh.map(([x1, y1, x2, y2, d], i) => <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={d > 5 ? C.green : C.ink} strokeWidth={Math.max(0.6, 4 - d * 0.5)} strokeLinecap="round" />)}
      {stats.map(([a, b], i) => (
        <g key={a}>
          <text x="242" y={46 + i * 26} fontSize="9.5" fill={C.mut}>{a}</text>
          <text x="352" y={46 + i * 26} textAnchor="end" fontSize="11" fill={C.ink}>{b}</text>
        </g>
      ))}
    </Frame>
  );
}
