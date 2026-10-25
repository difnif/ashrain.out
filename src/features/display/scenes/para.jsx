// 장면 11 — 평행사변형 (초등: 각·변 구하기 ↔ 중등: 일차식 대각·대변, 대각선의 이등분)
// 복사본이 대각선의 교점 O 를 중심으로 반 바퀴 돌아 제자리에 겹친다 — 마주 보는 각·변이 같다는 것이 보인다.
import { beats, seg, E, rot2, add2, sub2, mul2, len2 } from "../core";
import { Board, Caption, Path, Lbl, Angle, Ticks, Dot } from "../draw";
import { PARA } from "../facts";

const B = beats([["intro", 2600], ["rot", 4800], ["ang", 6200], ["side", 5200], ["last", 5000], ["hold", 2600]]);
const K = 54;
const PB = [150, 640], PC = [PB[0] + PARA.BC * K, 640];
const PA = [PB[0] + PARA.AB * K * Math.cos((PARA.angB * Math.PI) / 180), PB[1] - PARA.AB * K * Math.sin((PARA.angB * Math.PI) / 180)];
const PD = [PA[0] + PARA.BC * K, PA[1]];
const O = [(PA[0] + PC[0]) / 2, (PA[1] + PC[1]) / 2];
const QUAD = [PA, PB, PC, PD];

/** 변 바깥쪽 이름표 자리 */
const sideLbl = (P, Q, off = 34) => {
  const m = mul2(add2(P, Q), 0.5), d = sub2(Q, P), n = [d[1] / len2(d), -d[0] / len2(d)];
  const toO = sub2(O, m), sgn = toO[0] * n[0] + toO[1] * n[1] > 0 ? -1 : 1;
  return add2(m, mul2(n, off * sgn));
};
/** 평행 표시(꺾쇠) */
function Chev({ P, Q, n = 1, C, col }) {
  const m = mul2(add2(P, Q), 0.5), d = sub2(Q, P), u = mul2(d, 1 / len2(d)), w = [-u[1], u[0]];
  return <g>{Array.from({ length: n }, (_, i) => {
    const c = add2(m, mul2(u, (i - (n - 1) / 2) * 14));
    return <Path key={i} pts={[add2(sub2(c, mul2(u, 9)), mul2(w, 9)), add2(c, mul2(u, 3)), sub2(sub2(c, mul2(u, 9)), mul2(w, 9))]} stroke={col || C.gold} sw={3} />;
  })}</g>;
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const T = isM ? PARA.M : PARA.E;
  const draw = seg(t, 200, 1600, E.out);
  const angO = seg(t, 1200, 2200);
  const rk = seg(t, B.a.rot + 400, B.b.rot - 600, E.io);
  const ghostO = seg(t, B.a.rot, B.a.rot + 400) * (1 - seg(t, B.b.rot - 200, B.b.rot + 400));
  const R = (p) => rot2(p, Math.PI * rk, O);
  const solvedA = isM && t > B.a.ang + 3600, solvedS = isM && t > B.a.side + 3000;
  const lab = (k) => {
    if (isM && T.solved[k] && ((k === "AD" && solvedS) || (k !== "AD" && solvedA))) return T.solved[k];
    if (!isM && t > B.a.ang + 1400 && k === "D") return `${PARA.angB}°`;
    if (!isM && t > B.a.ang + 4000 && k === "A") return `${PARA.angA}°`;
    if (!isM && t > B.a.side + 1600 && k === "AD") return `${PARA.BC} cm`;
    return T.lab[k];
  };
  const lastO = seg(t, B.a.last, B.a.last + 700);
  const rowT = isM
    ? [B.a.ang + 200, B.a.ang + 2000, B.a.side + 200, B.a.side + 1500, B.a.last + 200, B.a.last + 1800]
    : [B.a.ang + 200, B.a.ang + 1300, B.a.ang + 2600, B.a.ang + 3900, B.a.side + 200, B.a.side + 1500, B.a.last + 300];
  const AL = [["A", PA, PD, PB], ["B", PB, PA, PC], ["C", PC, PB, PD], ["D", PD, PC, PA]];
  const angCol = { A: C.coral, B: C.sky, C: C.coral, D: C.sky };
  return (
    <g>
      <Path pts={QUAD} closed fill={C.ink} fo={0.05} stroke={C.ink} sw={3.6} o={draw} />
      {AL.map(([k, V, A, Bp]) => (
        <g key={k} opacity={angO}>
          <Angle V={V} A={A} B={Bp} r={46} C={C} color={angCol[k]} label={lab(k) || null} lsize={30} lr={lab(k) && lab(k).length > 6 ? 118 : 88} />
        </g>
      ))}
      {/* 변 이름표 */}
      {[["AD", PA, PD, C.coral], ["BC", PB, PC, C.ink], ["AB", PA, PB, C.ink]].map(([k, P, Q, col]) => {
        const s = lab(k);
        if (!s) return null;
        const q = sideLbl(P, Q, 36);
        return <Lbl key={k} x={q[0]} y={q[1]} s={s} size={30} fill={k === "AD" ? C.gold : col} C={C} o={angO} />;
      })}
      {/* 반 바퀴 도는 복사본 */}
      {ghostO > 0 && <g opacity={ghostO}>
        <Path pts={QUAD.map(R)} closed stroke={C.gold} sw={4} dash="12 8" />
        <Path pts={[PB, PC].map(R)} stroke={C.gold} sw={8} o={0.8} />
        <Angle V={R(PB)} A={R(PA)} B={R(PC)} r={46} C={C} color={C.gold} fillO={0.35} />
        <Dot p={O} r={7} fill={C.gold} />
      </g>}
      {/* 마지막: 초등 = 평행 표시, 중등 = 대각선 이등분 */}
      {lastO > 0 && (isM ? <g opacity={lastO}>
        <Path pts={[PA, PC]} stroke={C.teal} sw={2.8} />
        <Path pts={[PB, PD]} stroke={C.teal} sw={2.8} />
        <Ticks A={PA} B={O} n={1} C={C} color={C.gold} />
        <Ticks A={O} B={PC} n={1} C={C} color={C.gold} />
        <Ticks A={PB} B={O} n={2} C={C} color={C.coral} />
        <Ticks A={O} B={PD} n={2} C={C} color={C.coral} />
        <Dot p={O} r={7} fill={C.ink} />
        <Lbl x={O[0]} y={O[1] + 34} s="O" size={30} C={C} />
      </g> : <g opacity={lastO}>
        <Chev P={PA} Q={PD} n={2} C={C} />
        <Chev P={PB} Q={PC} n={2} C={C} />
        <Chev P={PB} Q={PA} n={1} C={C} col={C.teal} />
        <Chev P={PC} Q={PD} n={1} C={C} col={C.teal} />
      </g>)}
      <g opacity={draw}>
        <Lbl x={PA[0] - 18} y={PA[1] - 32} s="A" size={34} C={C} />
        <Lbl x={PB[0] - 30} y={PB[1] + 22} s="B" size={34} C={C} />
        <Lbl x={PC[0] + 26} y={PC[1] + 26} s="C" size={34} C={C} />
        <Lbl x={PD[0] + 26} y={PD[1] - 24} s="D" size={34} C={C} />
      </g>
      <Board x={900} y={222} t={t} C={C} size={36} lh={58} lines={T.board.map((L, i) => ({ ...L, t: rowT[i], row: i }))} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: "평행사변형 ABCD" },
        { t: B.a.rot, s: "똑같은 모양을 가운데 점 O 를 중심으로 반 바퀴 돌리면" },
        { t: B.b.rot - 900, s: "제자리에 꼭 겹쳐요 — 마주 보는 각·변이 같아요" },
        { t: B.a.ang, s: isM ? "대각의 크기가 같다 → 일차방정식" : "이웃한 두 각의 합은 180°" },
        { t: B.a.side, s: isM ? "대변의 길이가 같다 → 일차방정식" : "마주 보는 변의 길이가 같아요" },
        { t: B.a.last, s: isM ? "두 대각선은 서로를 이등분해요" : "마주 보는 두 쌍의 변이 서로 평행" },
      ]} />
    </g>
  );
}

export default {
  key: "para",
  dur: B.dur,
  title: { e: "평행사변형", m: "평행사변형의 성질" },
  sub: { e: "초등 · 사각형", m: "중등 · 사각형의 성질" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
