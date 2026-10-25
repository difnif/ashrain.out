// 장면 7 — 삼각형의 세 각 (초등: 수 ↔ 중등: 일차식)
// ∠A·∠B 를 오려 C 로 옮기면(B는 미끄러지듯, A는 반 바퀴 돌아) 세 각이 일직선 = 180°.
// 그 일직선 위에서 바깥쪽 각(외각)이 ∠A + ∠B 라는 것도 그대로 보인다.
import { beats, seg, E, rot2, polar, arcPts } from "../core";
import { Board, Caption, Path, Lbl } from "../draw";
import { TRI3 } from "../facts";

const B_ = beats([["intro", 2600], ["move", 6200], ["sum", 2800], ["eq", 6400], ["ext", 6000], ["hold", 2600]]);
const PB = [190, 640], PC = [610, 640], PD = [930, 640];
const LBA = (420 * Math.sin((60 * Math.PI) / 180)) / Math.sin((50 * Math.PI) / 180);
const PA = polar(PB, LBA, 70);
const PE = polar(PC, 300, 70);
const MAC = [(PA[0] + PC[0]) / 2, (PA[1] + PC[1]) / 2];
const WR = 74;

function Wedge({ V, a0, a1, col, C, label, o = 1, xf = (p) => p, lsize = 32, r = WR }) {
  if (o <= 0.001) return null;
  const pts = [V, ...arcPts(V, r, a0, a1, 24)].map(xf);
  const lp = xf(polar(V, r + 30, (a0 + a1) / 2));
  return <g opacity={o}>
    <Path pts={pts} closed fill={col} fo={0.42} stroke={col} sw={2.6} />
    {label && <Lbl x={lp[0]} y={lp[1]} s={label} size={lsize} fill={col} C={C} />}
  </g>;
}

function Scene({ t, C, mode }) {
  const T = mode === "m" ? TRI3.M : TRI3.E;
  const B = B_;
  const draw = seg(t, 200, 1600, E.out);
  const wO = seg(t, 1200, 2100);
  const mB = seg(t, B.a.move + 500, B.a.move + 2700, E.io);
  const mA = seg(t, B.a.move + 2900, B.a.move + 5400, E.io);
  const movedO = seg(t, B.a.move + 300, B.a.move + 700);
  const solved = mode === "m" ? seg(t, B.a.eq + 4200, B.a.eq + 5000) : 0;
  const lab = (k) => (solved > 0.5 && T.solved?.[k] ? T.solved[k] : T.lab[k]);
  const sumO = seg(t, B.a.sum, B.a.sum + 700);
  const extO = seg(t, B.a.ext, B.a.ext + 800);
  // 옮겨지는 사본
  const xfB = (p) => [p[0] + (PC[0] - PB[0]) * mB, p[1]];
  const xfA = (p) => rot2(p, Math.PI * mA, MAC);
  return (
    <g>
      {/* 직선 BD · 평행선 */}
      <Path pts={[PC, PD]} stroke={C.ink} sw={3} dash="12 9" o={seg(t, B.a.move, B.a.move + 600)} />
      <Path pts={[PC, PE]} stroke={C.soft} sw={2.6} dash="10 9" o={seg(t, B.a.move + 2700, B.a.move + 3300) * (1 - 0.6 * extO)} />
      {/* 삼각형 */}
      <Path pts={[PA, PB, PC]} closed stroke={C.ink} sw={3.6} fill={C.ink} fo={0.04} o={draw} />
      <Wedge V={PA} a0={250} a1={300} col={C.coral} C={C} label={lab("A")} o={wO * (1 - 0.6 * movedO)} />
      <Wedge V={PB} a0={0} a1={70} col={C.sky} C={C} label={lab("B")} o={wO * (1 - 0.6 * movedO)} />
      <Wedge V={PC} a0={120} a1={180} col={C.leaf} C={C} label={lab("C")} o={wO} />
      {/* 옮긴 각 */}
      <Wedge V={PB} a0={0} a1={70} col={C.sky} C={C} o={movedO} xf={xfB} label={mB >= 1 ? lab("B") : null} lsize={28} r={WR + 2} />
      <Wedge V={PA} a0={250} a1={300} col={C.coral} C={C} o={movedO * seg(t, B.a.move + 2600, B.a.move + 2900)} xf={xfA}
        label={mA >= 1 ? lab("A") : null} lsize={28} r={WR + 2} />
      {/* 일직선 180° */}
      {sumO > 0 && <g opacity={sumO * (1 - extO)}>
        <Path pts={arcPts(PC, WR + 52, 0, 180, 60)} stroke={C.gold} sw={4} />
        <Lbl x={PC[0]} y={PC[1] - WR - 82} s="180°" size={36} fill={C.gold} C={C} />
      </g>}
      {/* 외각 */}
      {extO > 0 && <g opacity={extO}>
        <Path pts={arcPts(PC, WR + 48, 0, 120, 50)} stroke={C.gold} sw={6} />
        <Lbl x={polar(PC, WR + 92, 60)[0]} y={polar(PC, WR + 92, 60)[1]} s={T.ext} size={34} fill={C.gold} C={C} />
      </g>}
      {/* 꼭짓점 이름 */}
      <g opacity={draw}>
        <Lbl x={PA[0] - 6} y={PA[1] - 34} s="A" size={34} C={C} />
        <Lbl x={PB[0] - 30} y={PB[1] + 26} s="B" size={34} C={C} />
        <Lbl x={PC[0] + 4} y={PC[1] + 38} s="C" size={34} C={C} />
        <Lbl x={PD[0] + 26} y={PD[1] + 4} s="D" size={34} C={C} o={seg(t, B.a.move, B.a.move + 600)} />
      </g>
      <Board x={1010} y={250} t={t} C={C} size={38} lh={62} lines={[
        { ...T.board[0], t: B.a.sum + 300 },
        { ...T.board[1], t: B.a.eq + 300 },
        { ...T.board[2], t: B.a.eq + 2600 },
        { ...T.board[3], t: B.a.ext + 300 },
        { ...T.board[4], t: B.a.ext + 1800 },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: "삼각형의 세 각" },
        { t: B.a.move, s: "두 각을 오려서 꼭짓점 C로 옮기면" },
        { t: B.a.sum, s: "세 각이 모여 일직선 — 180°" },
        { t: B.a.eq, s: mode === "m" ? "세 내각의 합으로 식을 세워요" : "180°에서 아는 두 각을 빼요" },
        { t: B.a.ext, s: mode === "m" ? "외각은 이웃하지 않은 두 내각의 합" : "일직선 180°에서 한 각을 빼면 바깥쪽 각" },
      ]} />
    </g>
  );
}

export default {
  key: "tri3",
  dur: B_.dur,
  title: { e: "삼각형의 세 각", m: "삼각형의 내각과 외각" },
  sub: { e: "초등 · 각도", m: "중등 · 일차방정식으로 각 구하기" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};

