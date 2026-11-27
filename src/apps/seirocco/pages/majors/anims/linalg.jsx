// 선형대수 그림 — 일차결합과 생성(span) · 행렬이 평면을 바꾸는 모습 · 행렬식 = 넓이 배율 · 고유벡터 · 두 직선(해의 개수) · 가우스 소거 · SVD(원 → 타원)
import { useState } from "react";
import { C, Frame, Slider, Seg, plot, Arrow, Label, Mat, fmt, ease, lerp, useClock } from "./kit.jsx";

const P0 = () => plot({ x0: -4, x1: 4, y0: -2.6, y1: 2.6, pad: [6, 6, 6, 6] });
function Grid({ P, M = [1, 0, 0, 1], color = C.bd, n = 4, w = 0.8 }) {
  const out = [];
  const T = (x, y) => [M[0] * x + M[1] * y, M[2] * x + M[3] * y];
  for (let k = -n; k <= n; k++) {
    const [a, b] = T(k, -n), [c, d] = T(k, n), [e, f] = T(-n, k), [g, h] = T(n, k);
    out.push(<line key={"v" + k} x1={P.X(a)} y1={P.Y(b)} x2={P.X(c)} y2={P.Y(d)} stroke={color} strokeWidth={k === 0 ? w * 1.8 : w} />);
    out.push(<line key={"h" + k} x1={P.X(e)} y1={P.Y(f)} x2={P.X(g)} y2={P.Y(h)} stroke={color} strokeWidth={k === 0 ? w * 1.8 : w} />);
  }
  return <g>{out}</g>;
}

/* ── 일차결합 a·u + b·v — 두 벡터가 나란하지 않으면 평면 전체를 덮는다 ── */
export function Span({ p = {} }) {
  const [dep, setDep] = useState(!!p.dep);
  const clock = useClock({ period: 12 });
  const P = P0();
  const u = [1.6, 0.5], v = dep ? [-0.8, -0.25] : [0.4, 1.3];
  const t = (clock.t / 12) * 2 * Math.PI;
  const a = 1.3 * Math.cos(t) + 0.5 * Math.sin(2 * t), b = 1.2 * Math.sin(t);
  const w = [a * u[0] + b * v[0], a * u[1] + b * v[1]];
  const trail = [];
  for (let k = 0; k <= 120; k++) {
    const s = (k / 120) * 2 * Math.PI * (clock.t / 12);
    const aa = 1.3 * Math.cos(s) + 0.5 * Math.sin(2 * s), bb = 1.2 * Math.sin(s);
    trail.push([aa * u[0] + bb * v[0], aa * u[1] + bb * v[1]]);
  }
  return (
    <Frame clock={clock} title="일차결합과 생성"
      read={<>w = a·u + b·v, a = <b>{fmt(a, 2)}</b>, b = <b>{fmt(b, 2)}</b> · {dep ? <b>u 와 v 가 나란하면(일차종속) 아무리 섞어도 한 직선 위 — 생성 공간은 1차원</b> : "u, v 가 나란하지 않으면(일차독립) 어떤 점이든 만들 수 있다 — 생성 공간은 평면 전체"}</>}
      controls={<Seg value={dep} onChange={setDep} options={[[false, "독립"], [true, "종속"]]} />}>
      <Grid P={P} />
      {dep && <line x1={P.X(-4 * u[0])} y1={P.Y(-4 * u[1])} x2={P.X(4 * u[0])} y2={P.Y(4 * u[1])} stroke={C.gold} strokeWidth="6" opacity="0.25" />}
      <path d={P.poly(trail)} fill="none" stroke={C.sp} strokeWidth="1.2" opacity="0.5" />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(a * u[0])} y2={P.Y(a * u[1])} color={C.red} w={1.6} dash="4 3" />
      <Arrow x1={P.X(a * u[0])} y1={P.Y(a * u[1])} x2={P.X(w[0])} y2={P.Y(w[1])} color={C.blue} w={1.6} dash="4 3" />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(u[0])} y2={P.Y(u[1])} color={C.red} w={2.4} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(v[0])} y2={P.Y(v[1])} color={C.blue} w={2.4} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(w[0])} y2={P.Y(w[1])} color={C.ink} w={2.4} />
      <Label x={P.X(u[0]) + 3} y={P.Y(u[1]) + 12} color={C.red} bold>u</Label>
      <Label x={P.X(v[0]) + 4} y={P.Y(v[1])} color={C.blue} bold>v</Label>
      <Label x={P.X(w[0]) + 4} y={P.Y(w[1]) - 4} bold>w</Label>
    </Frame>
  );
}

/* ── 행렬은 평면을 바꾼다: 격자 · 단위 정사각형 · 기저 e₁ e₂ 가 어디로 가나 ── */
const MATS = {
  rot: { M: [Math.cos(0.7), -Math.sin(0.7), Math.sin(0.7), Math.cos(0.7)], name: "회전(40°)", s: "회전" },
  shear: { M: [1, 1, 0, 1], name: "층밀림", s: "층밀림" },
  scale: { M: [2, 0, 0, 0.6], name: "늘이기 · 줄이기", s: "늘이기" },
  refl: { M: [0, 1, 1, 0], name: "y = x 대칭(뒤집기)", s: "대칭" },
  proj: { M: [1, 0, 0, 0], name: "x축 정사영(납작)", s: "정사영" },
  gen: { M: [1.4, 0.7, -0.4, 1.1], name: "일반 행렬", s: "일반" },
};
export function LinMap({ p = {} }) {
  const [k, setK] = useState(p.m || "shear");
  const clock = useClock({ period: 5 });
  const P = P0();
  const A = (MATS[k] || MATS.shear).M;
  const s = ease(Math.min(1, (clock.t % 5) / 3.2));
  const M = [lerp(1, A[0], s), lerp(0, A[1], s), lerp(0, A[2], s), lerp(1, A[3], s)];
  const T = (x, y) => [M[0] * x + M[1] * y, M[2] * x + M[3] * y];
  const sq = [T(0, 0), T(1, 0), T(1, 1), T(0, 1)];
  const det = M[0] * M[3] - M[1] * M[2];
  return (
    <Frame clock={clock} title="행렬과 선형변환"
      read={<>{(MATS[k] || MATS.shear).name} A = <Mat m={A} /> · e₁ → A의 1열, e₂ → A의 2열 · 격자선은 곧고 나란하며 원점은 그대로(선형) · 넓이 배율 det = <b>{fmt(det, 3)}</b></>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={Object.entries(MATS).map(([id, m]) => [id, m.s])} />}>
      <Grid P={P} color={C.bd} />
      <Grid P={P} M={M} color={C.sp} w={0.9} />
      <path d={P.poly([...sq, sq[0]])} fill={C.gold} opacity="0.3" stroke={C.gold} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(M[0])} y2={P.Y(M[2])} color={C.red} w={2.6} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(M[1])} y2={P.Y(M[3])} color={C.blue} w={2.6} />
      <Label x={P.X(M[0]) + 4} y={P.Y(M[2]) + 12} color={C.red} bold>Ae₁</Label>
      <Label x={P.X(M[1]) + 4} y={P.Y(M[3]) - 4} color={C.blue} bold>Ae₂</Label>
    </Frame>
  );
}

/* ── 행렬식 = 넓이 배율(부호는 방향) ── */
export function DetArea({ p = {} }) {
  const [b, setB] = useState(0.8);
  const clock = useClock({ period: 10 });
  const P = P0();
  const th = (clock.t / 10) * 2 * Math.PI;
  const c1 = [1.8, 0.3], c2 = [b + 1.4 * Math.cos(th), 0.2 + 1.4 * Math.sin(th)];
  const det = c1[0] * c2[1] - c2[0] * c1[1];
  const poly = [[0, 0], c1, [c1[0] + c2[0], c1[1] + c2[1]], c2];
  return (
    <Frame clock={clock} title="행렬식과 넓이"
      read={<>열벡터 두 개가 만드는 평행사변형 넓이 = |det| = <b>{fmt(Math.abs(det), 3)}</b> · det = <b>{fmt(det, 3)}</b> {Math.abs(det) < 0.08 ? "— 두 열이 나란해 납작해졌다: det = 0, 역행렬 없음" : det < 0 ? "— 음수: 방향이 뒤집혔다(거울상)" : "— 양수: 방향 그대로"}</>}
      controls={<Slider label="둘째 열 밀기" min={-1.5} max={1.5} step={0.05} value={b} onChange={setB} />}>
      <Grid P={P} />
      <path d={P.poly([...poly, poly[0]])} fill={det < 0 ? C.red : C.sp} opacity="0.3" stroke={det < 0 ? C.red : C.sp} strokeWidth="1.5" />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(c1[0])} y2={P.Y(c1[1])} color={C.ink} w={2.4} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(c2[0])} y2={P.Y(c2[1])} color={C.blue} w={2.4} />
    </Frame>
  );
}

/* ── 고유벡터: v 를 돌려 가며 Av 를 본다 — 둘이 한 직선 위에 서는 방향 ── */
const EIG = {
  sym: { M: [2, 1, 1, 2], name: "λ = 3, 1" },
  shear: { M: [1, 1, 0, 1], name: "λ = 1 (방향 하나뿐)" },
  rot: { M: [0.6, -0.8, 0.8, 0.6], name: "회전 — 실수 고유벡터 없음" },
  flip: { M: [1.5, 0, 0, -0.7], name: "λ = 1.5, −0.7" },
};
export function Eigen({ p = {} }) {
  const [k, setK] = useState(p.m || "sym");
  const E = EIG[k] || EIG.sym;
  const clock = useClock({ period: 12 });
  const P = plot({ x0: -3.6, x1: 3.6, y0: -2.3, y1: 2.3, pad: [6, 6, 6, 6] });
  const M = E.M;
  const th = (clock.t / 12) * 2 * Math.PI;
  const v = [Math.cos(th), Math.sin(th)], Av = [M[0] * v[0] + M[1] * v[1], M[2] * v[0] + M[3] * v[1]];
  const cr = v[0] * Av[1] - v[1] * Av[0], par = Math.abs(cr) < 0.06 * Math.hypot(...Av);
  const ell = [];
  for (let i = 0; i <= 80; i++) { const a = (i / 80) * 2 * Math.PI; ell.push([M[0] * Math.cos(a) + M[1] * Math.sin(a), M[2] * Math.cos(a) + M[3] * Math.sin(a)]); }
  const lam = par ? (Av[0] * v[0] + Av[1] * v[1]) : null;
  return (
    <Frame clock={clock} title="고윳값과 고유벡터"
      read={<>A = <Mat m={E.M} /> — {E.name} · 단위벡터 v(파랑)를 돌리면 Av(붉음)는 타원을 그린다. {par ? <b>지금 Av = λv — 고유벡터! λ ≈ {fmt(lam, 2)}</b> : "보통은 방향이 바뀐다. 방향이 그대로인(나란한) 순간을 찾아보세요."}</>}
      controls={<Seg value={k} onChange={setK} options={[["sym", "대칭"], ["flip", "대각"], ["shear", "층밀림"], ["rot", "회전"]]} />}>
      <circle cx={P.X(0)} cy={P.Y(0)} r={P.X(1) - P.X(0)} fill="none" stroke={C.bd} strokeWidth="1.2" />
      <path d={P.poly([...ell])} fill="none" stroke={C.sp} strokeDasharray="4 3" />
      <line x1={P.X(-3 * v[0])} y1={P.Y(-3 * v[1])} x2={P.X(3 * v[0])} y2={P.Y(3 * v[1])} stroke={par ? C.green : C.bd} strokeWidth={par ? 3 : 1} opacity={par ? 0.6 : 1} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(Av[0])} y2={P.Y(Av[1])} color={C.red} w={2.6} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(v[0])} y2={P.Y(v[1])} color={C.blue} w={2.6} />
      <Label x={P.X(Av[0]) + 4} y={P.Y(Av[1])} color={C.red} bold>Av</Label>
      <Label x={P.X(v[0]) + 4} y={P.Y(v[1]) + 12} color={C.blue} bold>v</Label>
    </Frame>
  );
}

/* ── 두 직선: 해가 하나 · 없음 · 무수히 ── */
export function Lines2({ p = {} }) {
  const [m2, setM2] = useState(0.5);
  const [c2, setC2] = useState(0);
  const clock = useClock({ period: 6 });
  const P = plot({ x0: -4, x1: 4, y0: -3, y1: 3, pad: [8, 8, 16, 22] });
  const m1 = 0.5, c1 = 1;           // y = 0.5x + 1  ⇔  x − 2y = −2
  const par = Math.abs(m1 - m2) < 1e-6, same = par && Math.abs(c1 - c2) < 1e-6;
  const xi = par ? null : (c2 - c1) / (m1 - m2), yi = par ? null : m1 * xi + c1;
  const pulse = 4 + 1.5 * Math.sin(clock.t * 3);
  return (
    <Frame clock={clock} title="연립방정식과 두 직선"
      read={<>{same ? <b>두 식이 같은 직선 — 해가 무수히 많다(행렬식 0, 계수가 비례)</b> : par ? <b>나란한데 다른 직선 — 해가 없다(행렬식 0)</b> : <>교점 하나 ({fmt(xi, 2)}, {fmt(yi, 2)}) — 해가 오직 하나(행렬식 ≠ 0)</>}</>}
      controls={<>
        <Slider label="둘째 기울기" min={-2} max={2} step={0.25} value={m2} onChange={setM2} />
        <Slider label="둘째 절편" min={-2} max={2} step={0.5} value={c2} onChange={setC2} />
      </>}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill={C.card} />
      <path d={P.path((x) => m1 * x + c1)} stroke={C.blue} strokeWidth={same ? 5 : 2.2} opacity={same ? 0.5 : 1} fill="none" />
      <path d={P.path((x) => m2 * x + c2)} stroke={C.red} strokeWidth="2.2" fill="none" />
      {!par && Math.abs(xi) < 4 && Math.abs(yi) < 3 && <circle cx={P.X(xi)} cy={P.Y(yi)} r={pulse} fill={C.green} />}
      <Label x={P.l + 4} y={P.t + 12} color={C.blue} size={10.5}>y = 0.5x + 1</Label>
      <Label x={P.l + 4} y={P.t + 25} color={C.red} size={10.5}>y = {fmt(m2, 2)}x + {fmt(c2, 2)}</Label>
    </Frame>
  );
}

/* ── 가우스 소거: 첨가행렬을 한 단계씩 ── */
const GS = [
  { M: [[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]], say: "첨가행렬 [A | b] — 식 셋, 미지수 셋", hl: [] },
  { M: [[2, 1, -1, 8], [0, 0.5, 0.5, 1], [-2, 1, 2, -3]], say: "R₂ ← R₂ + (3/2)R₁ — 둘째 줄의 x 를 없앤다", hl: [1] },
  { M: [[2, 1, -1, 8], [0, 0.5, 0.5, 1], [0, 2, 1, 5]], say: "R₃ ← R₃ + R₁ — 셋째 줄의 x 를 없앤다", hl: [2] },
  { M: [[2, 1, -1, 8], [0, 0.5, 0.5, 1], [0, 0, -1, 1]], say: "R₃ ← R₃ − 4R₂ — 셋째 줄의 y 를 없앤다: 사다리꼴 완성", hl: [2] },
  { M: [[2, 1, -1, 8], [0, 0.5, 0.5, 1], [0, 0, -1, 1]], say: "뒤에서부터 대입: z = −1 → y = 3 → x = 2", hl: [0, 1, 2], sol: true },
];
export function RowReduce() {
  const clock = useClock({ period: GS.length * 2.4 });
  const k = Math.min(GS.length - 1, Math.floor(clock.t / 2.4));
  const S = GS[k];
  const cell = (v) => (Number.isInteger(v) ? String(v) : fmt(v, 2)).replace("-", "−");
  return (
    <Frame clock={clock} title="가우스 소거" vb="0 0 360 200"
      read={<>{k + 1}/{GS.length} · {S.say}{S.sol ? " — 해 (x, y, z) = (2, 3, −1)" : ""}</>}>
      <text x="180" y="22" textAnchor="middle" fontSize="11" fill={C.mut}>2x + y − z = 8 · −3x − y + 2z = −11 · −2x + y + 2z = −3</text>
      <path d="M78 36 q-10 0 -10 10 v108 q0 10 10 10 M282 36 q10 0 10 10 v108 q0 10 -10 10" fill="none" stroke={C.ink} strokeWidth="1.6" />
      <line x1="232" y1="40" x2="232" y2="152" stroke={C.mut} strokeDasharray="3 3" />
      {S.M.map((row, i) => (
        <g key={i}>
          {S.hl.includes(i) && <rect x="72" y={44 + i * 38} width="216" height="30" rx="6" fill={C.sp} opacity="0.16" />}
          {row.map((v, j) => (
            <text key={j} x={j < 3 ? 104 + j * 50 : 260} y={65 + i * 38} textAnchor="middle" fontSize="15" fontWeight={i === j && v !== 0 ? 800 : 500}
              fill={i > j && v === 0 ? C.green : C.ink}>{cell(v)}</text>
          ))}
        </g>
      ))}
    </Frame>
  );
}

/* ── SVD: 원 → (회전 Vᵀ) → (늘이기 Σ) → (회전 U) → 타원 ── */
export function SVD({ p = {} }) {
  const clock = useClock({ period: 10 });
  const P = plot({ x0: -3.4, x1: 3.4, y0: -2.2, y1: 2.2, pad: [6, 6, 6, 6] });
  const a1 = -0.5, s1 = 2.2, s2 = 0.7, a2 = 0.9;
  const ph = (clock.t % 10) / 10;
  const st = ph < 0.15 ? 0 : ph < 0.4 ? 1 : ph < 0.65 ? 2 : ph < 0.9 ? 3 : 3;
  const pr = (lo, hi) => ease(Math.min(1, Math.max(0, (ph - lo) / (hi - lo))));
  const r1 = a1 * pr(0.15, 0.35), sx = lerp(1, s1, pr(0.4, 0.6)), sy = lerp(1, s2, pr(0.4, 0.6)), r2 = a2 * pr(0.65, 0.85);
  const T = ([x, y]) => {
    let u = [Math.cos(r1) * x - Math.sin(r1) * y, Math.sin(r1) * x + Math.cos(r1) * y];
    u = [sx * u[0], sy * u[1]];
    return [Math.cos(r2) * u[0] - Math.sin(r2) * u[1], Math.sin(r2) * u[0] + Math.cos(r2) * u[1]];
  };
  const circ = [];
  for (let i = 0; i <= 90; i++) { const t = (i / 90) * 2 * Math.PI; circ.push(T([Math.cos(t), Math.sin(t)])); }
  const v1 = T([Math.cos(-a1), Math.sin(-a1)]), v2 = T([-Math.sin(-a1), Math.cos(-a1)]);
  const names = ["단위원", "① Vᵀ — 돌리기", "② Σ — 축 따라 늘이기 σ₁ = 2.2, σ₂ = 0.7", "③ U — 다시 돌리기 → A 가 만든 타원"];
  return (
    <Frame clock={clock} title="특잇값 분해" read={<>A = UΣVᵀ · {names[st]} — 어떤 행렬이든 「돌리기 · 늘이기 · 돌리기」 셋으로 쪼개진다. 긴 반지름 σ₁ 이 가장 센 방향</>}>
      <path d={P.poly(circ)} fill={C.sp} opacity="0.2" stroke={C.sp} strokeWidth="1.8" />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(v1[0])} y2={P.Y(v1[1])} color={C.red} w={2.2} />
      <Arrow x1={P.X(0)} y1={P.Y(0)} x2={P.X(v2[0])} y2={P.Y(v2[1])} color={C.blue} w={2.2} />
    </Frame>
  );
}
