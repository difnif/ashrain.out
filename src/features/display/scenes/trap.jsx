// 장면 12 — 사다리꼴·마름모의 넓이 (초등: 넓이 계산 ↔ 중등: 넓이를 알고 x 구하기)
// 사다리꼴은 똑같은 것을 반 바퀴 돌려 붙이면 평행사변형(밑변 = 윗변 + 아랫변).
// 마름모는 두 대각선으로 만든 직사각형의 절반 — 안쪽 삼각형과 바깥 삼각형이 짝을 이룬다.
import { beats, seg, E, rot2 } from "../core";
import { Board, Caption, Path, Lbl, Dim, Dot } from "../draw";
import { TRAP } from "../facts";

const B = beats([["t_in", 2200], ["t_copy", 4400], ["t_calc", 5800], ["r_in", 1800], ["r_rect", 4400], ["r_calc", 5600], ["hold", 2400]]);
const K = 40, OX = 160, OY = 640;
const P = (x, y) => [OX + K * x, OY - K * y];
const T4 = [P(0, 0), P(TRAP.bot, 0), P(TRAP.top + 1, TRAP.h), P(1, TRAP.h)];   // 아랫변 9, 윗변 5(1~6), 높이 6
const MID = [(T4[1][0] + T4[2][0]) / 2, (T4[1][1] + T4[2][1]) / 2];
const RC = [450, 450], RK = 52;
const RH = (TRAP.d1 / 2) * RK, RV = (TRAP.d2 / 2) * RK;
const RL = [RC[0] - RH, RC[1]], RT = [RC[0], RC[1] - RV], RR = [RC[0] + RH, RC[1]], RB = [RC[0], RC[1] + RV];
const TRI_COL = ["coral", "sky", "leaf", "lilac"];

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const T = isM ? TRAP.M : TRAP.E;
  const tO = 1 - seg(t, B.a.r_in, B.a.r_in + 800);
  const rO = seg(t, B.a.r_in + 500, B.b.r_in);
  const draw = seg(t, 200, 1500, E.out);
  const cp = seg(t, B.a.t_copy + 500, B.a.t_copy + 3200, E.io);
  const cpO = seg(t, B.a.t_copy, B.a.t_copy + 500);
  const R = (p) => rot2(p, Math.PI * cp, MID);
  const baseO = seg(t, B.a.t_copy + 3300, B.a.t_copy + 3900);
  const rectO = seg(t, B.a.r_rect + 200, B.a.r_rect + 1000);
  const pairO = seg(t, B.a.r_rect + 1400, B.a.r_rect + 2600);
  const inner = [[RC, RL, RT], [RC, RT, RR], [RC, RR, RB], [RC, RB, RL]];
  const outer = [[RL, RT, [RL[0], RT[1]]], [RT, RR, [RR[0], RT[1]]], [RR, RB, [RR[0], RB[1]]], [RB, RL, [RL[0], RB[1]]]];
  const rowT = [B.a.t_copy + 3600, B.a.t_calc + 300, B.a.t_calc + 2400, B.a.r_rect + 2800, B.a.r_calc + 300, B.a.r_calc + 2400];
  const rowTE = [B.a.t_in + 400, B.a.t_copy + 3600, B.a.t_calc + 1200, B.a.r_in + 400, B.a.r_rect + 2800, B.a.r_calc + 1200];
  return (
    <g>
      {/* 사다리꼴 */}
      <g opacity={tO}>
        <Path pts={T4} closed fill={C.coral} fo={0.3} stroke={C.ink} sw={3.6} o={draw} />
        <Path pts={[T4[3], P(1, 0)]} stroke={C.soft} sw={2.4} dash="9 7" o={seg(t, 1000, 1700)} />
        <g opacity={seg(t, 1200, 2000) * (1 - 0.7 * baseO)}>
          <Lbl x={(T4[2][0] + T4[3][0]) / 2} y={T4[3][1] - 30} s={T.tLab.top} size={30} C={C} />
          <Lbl x={(T4[0][0] + T4[1][0]) / 2} y={T4[0][1] + 34} s={T.tLab.bot} size={30} C={C} />
        </g>
        <Lbl x={T4[3][0] + 14} y={(T4[3][1] + OY) / 2} s={T.tLab.h} size={30} anchor="start" C={C} o={seg(t, 1200, 2000)} />
        {cpO > 0 && <g opacity={cpO}>
          <Path pts={T4.map(R)} closed fill={C.sky} fo={0.3} stroke={C.ink} sw={3} dash={cp < 1 ? "10 7" : undefined} />
        </g>}
        {baseO > 0 && <g opacity={baseO}>
          <Dim A={P(0, 0)} B={P(TRAP.top + TRAP.bot, 0)} off={-42} lofs={-34} s={isM ? "*x* + (*x* + 4)" : `${TRAP.bot} + ${TRAP.top} = ${TRAP.top + TRAP.bot} (cm)`} C={C} color={C.gold} size={30} />
          <Lbl x={(P(TRAP.bot, 0)[0] + P(15, 6)[0]) / 2 + 40} y={P(0, 6)[1] - 30} s="평행사변형 ÷ 2" size={30} fill={C.gold} C={C} />
        </g>}
      </g>
      {/* 마름모 */}
      {rO > 0 && <g opacity={rO}>
        <Path pts={[[RL[0], RT[1]], [RR[0], RT[1]], [RR[0], RB[1]], [RL[0], RB[1]]]} closed stroke={C.soft} sw={2.6} dash="10 8" o={rectO} />
        {inner.map((tri, i) => <Path key={"i" + i} pts={tri} closed fill={C[TRI_COL[i]]} fo={0.18 + 0.22 * pairO} stroke="none" />)}
        {outer.map((tri, i) => <Path key={"o" + i} pts={tri} closed fill={C[TRI_COL[i]]} fo={0.32 * pairO} stroke="none" />)}
        <Path pts={[RL, RT, RR, RB]} closed stroke={C.ink} sw={3.6} />
        <Path pts={[RL, RR]} stroke={C.ink} sw={2.4} dash="9 7" />
        <Path pts={[RT, RB]} stroke={C.ink} sw={2.4} dash="9 7" />
        <Dot p={RC} r={5} fill={C.ink} />
        <Dim A={[RL[0], RB[1]]} B={[RR[0], RB[1]]} off={-36} lofs={-32} s={T.rLab.d1} C={C} color={C.gold} size={30} />
        <Dim A={[RR[0], RB[1]]} B={[RR[0], RT[1]]} off={-36} lofs={-44} s={T.rLab.d2} C={C} color={C.gold} size={30} />
        <Lbl x={RC[0]} y={RT[1] - 34} s="직사각형 ÷ 2" size={30} fill={C.gold} C={C} o={pairO} />
      </g>}
      <Board x={980} y={232} t={t} C={C} size={36} lh={60} lines={T.board.map((L, i) => ({ ...L, t: (isM ? rowT : rowTE)[i], row: i }))} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: isM ? `넓이가 ${TRAP.area} cm²인 사다리꼴` : "사다리꼴의 넓이는?" },
        { t: B.a.t_copy, s: "똑같은 사다리꼴을 반 바퀴 돌려 붙이면 평행사변형" },
        { t: B.a.t_calc, s: isM ? "넓이 공식에 넣고 일차방정식" : "평행사변형 넓이의 절반" },
        { t: B.a.r_in, s: isM ? `넓이가 ${TRAP.rArea} cm²인 마름모` : "마름모의 넓이는?" },
        { t: B.a.r_rect, s: "두 대각선으로 직사각형을 그리면 마름모는 그 절반" },
        { t: B.a.r_calc, s: isM ? "대각선의 길이를 x로 두고 풀어요" : "대각선 × 대각선 ÷ 2" },
      ]} />
    </g>
  );
}

export default {
  key: "trap",
  dur: B.dur,
  title: { e: "사다리꼴·마름모의 넓이", m: "넓이로 길이 구하기" },
  sub: { e: "초등 · 다각형의 넓이", m: "중등 · 일차방정식의 활용" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
