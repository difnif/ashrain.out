// 장면 10 — 이등변삼각형 (초등: 접어서 두 각이 같음 ↔ 중등: 일차식 밑각, 꼭지각의 이등분선)
// 왼쪽 반을 꼭짓점 A 에서 밑변으로 내린 선을 따라 접어 넘기면 ∠B 가 ∠C 에 꼭 겹친다(두 판 공통).
import { beats, seg, E } from "../core";
import { Board, Caption, Path, Lbl, Angle, Ticks, RightMark, Dim } from "../draw";
import { ISO } from "../facts";

const B = beats([["intro", 2600], ["fold", 3600], ["folded", 1300], ["unfold", 2400], ["eq", 6400], ["prop", 6400], ["hold", 2600]]);
const K = 34;                                       // 1 cm = 34 px
const D = [450, 652], HB = (ISO.BC / 2) * K, HT = (ISO.BC / 2 / Math.tan((ISO.apex / 2) * Math.PI / 180)) * K;
const PB = [D[0] - HB, D[1]], PC = [D[0] + HB, D[1]], PA = [D[0], D[1] - HT];

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const T = isM ? ISO.M : ISO.E;
  const draw = seg(t, 200, 1600, E.out);
  const angO = seg(t, 1200, 2200);
  const fold = seg(t, B.a.fold, B.b.fold, E.io) - seg(t, B.a.unfold, B.b.unfold, E.io);
  const cs = Math.cos(Math.PI * fold);
  const fx = (p) => [D[0] + (p[0] - D[0]) * cs, p[1]];
  const solved = isM && t > B.a.eq + 4200;
  const lab = (k) => (solved && T.solved?.[k] != null ? T.solved[k] : T.lab[k]);
  const axisO = seg(t, B.a.fold - 600, B.a.fold);
  const propO = seg(t, B.a.prop, B.a.prop + 700);
  const tickO = seg(t, 1600, 2400);
  // 초등은 길이(㉠ 아래 반으로), 중등은 수직이등분 표시
  const rowT = isM
    ? [400, B.a.folded + 200, B.a.eq + 200, B.a.eq + 800, B.a.eq + 3400, B.a.prop + 300, B.a.prop + 1800]
    : [400, 2000, B.a.folded + 200, B.a.eq + 200, B.a.eq + 900, B.a.eq + 3400, B.a.prop + 300, B.a.prop + 1200];
  return (
    <g>
      {/* 오른쪽 반(고정) */}
      <Path pts={[PA, D, PC]} closed fill={C.sky} fo={0.22} stroke="none" o={draw} />
      <Path pts={[PA, PB, PC]} closed stroke={C.ink} sw={3.6} o={draw} />
      <g opacity={angO}>
        <Angle V={PA} A={PB} B={PC} r={56} C={C} color={C.gold} label={lab("A")} lsize={30} lr={isM ? 150 : 104} />
        <Angle V={PC} A={PA} B={PB} r={52} C={C} color={C.coral} label={lab("C")} lsize={30} lr={isM ? 110 : 92} />
      </g>
      {/* 접히는 왼쪽 반 */}
      <g>
        <Path pts={[PA, PB, D].map(fx)} closed fill={cs >= 0 ? C.coral : C.lilac} fo={0.3} stroke={C.ink} sw={cs >= 0 ? 0 : 2.6} o={draw} />
        <g opacity={angO}>
          <Angle V={fx(PB)} A={fx(PA)} B={fx(D)} r={52} C={C} color={C.coral} label={Math.abs(cs) > 0.6 ? lab("B") : null} lsize={30} lr={isM ? 110 : 92} />
        </g>
      </g>
      {/* 접는 선 AD */}
      <Path pts={[PA, D]} stroke={C.ink} sw={2.6} dash="10 8" o={Math.max(axisO, propO)} />
      {/* 같은 길이 */}
      <g opacity={tickO}>
        <Ticks A={PA} B={PB} n={1} C={C} color={C.gold} />
        <Ticks A={PA} B={PC} n={1} C={C} color={C.gold} />
      </g>
      {/* 밑변 이등분·수직 */}
      {propO > 0 && <g opacity={propO}>
        <RightMark V={D} A={PA} B={PC} s={22} C={C} color={C.gold} />
        <Ticks A={PB} B={D} n={2} C={C} color={C.teal} />
        <Ticks A={D} B={PC} n={2} C={C} color={C.teal} />
        <Dim A={PB} B={D} off={-34} lofs={-30} s={`${ISO.BC / 2} cm`} C={C} size={28} />
        <Dim A={D} B={PC} off={-34} lofs={-30} s={`${ISO.BC / 2} cm`} C={C} size={28} />
      </g>}
      <g opacity={draw}>
        <Lbl x={PA[0]} y={PA[1] - 34} s="A" size={34} C={C} />
        <Lbl x={PB[0] - 30} y={PB[1] + 22} s="B" size={34} C={C} />
        <Lbl x={PC[0] + 30} y={PC[1] + 22} s="C" size={34} C={C} />
        <Lbl x={D[0] + 22} y={D[1] + 30} s="D" size={30} C={C} o={Math.max(axisO, propO)} />
      </g>
      <Board x={900} y={222} t={t} C={C} size={36} lh={58} lines={T.board.map((L, i) => ({ ...L, t: rowT[i], row: i }))} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: isM ? "AB = AC 인 이등변삼각형" : "두 변의 길이가 같은 이등변삼각형" },
        { t: B.a.fold, s: "꼭짓점 A에서 반으로 접으면" },
        { t: B.a.folded, s: isM ? "두 밑각이 꼭 겹쳐요 — ∠B = ∠C" : "두 각이 꼭 겹쳐요" },
        { t: B.a.eq, s: isM ? "세 내각의 합으로 일차방정식" : "180°에서 꼭지각을 빼고 둘로 나눠요" },
        { t: B.a.prop, s: isM ? "꼭지각의 이등분선은 밑변을 수직이등분" : "접은 선은 밑변과 수직이고 밑변을 반으로 나눠요" },
      ]} />
    </g>
  );
}

export default {
  key: "iso",
  dur: B.dur,
  title: { e: "이등변삼각형", m: "이등변삼각형의 성질" },
  sub: { e: "초등 · 삼각형", m: "중등 · 삼각형의 성질" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};

