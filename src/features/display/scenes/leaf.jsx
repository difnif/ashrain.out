// 장면 3 — 색칠한 부분의 넓이와 둘레: 은행잎 (초등 3.14 ↔ 중등 π)
// 그림·움직임은 두 판이 똑같고 수만 바뀐다 — 토글하면 3.14 로 계산한 값이 π 식으로 겹쳐 바뀐다.
import { beats, seg, E, lerp, arcPts, mix2 } from "../core";
import { Board, Caption, Path, Lbl, Dot, Dim, Glow } from "../draw";
import { LEAF } from "../facts";

const B = beats([["intro", 2400], ["arcs", 4200], ["ask", 2200], ["half", 6400], ["dbl", 2600], ["perim", 6800], ["hold", 3600]]);
const K = 30, O = [170, 590];
const P = (x, y) => [O[0] + K * x, O[1] - K * y];
const S = LEAF.SIDE;
const BL = P(0, 0), BR = P(S, 0), TR = P(S, S), TL = P(0, S), MID = P(S / 2, S / 2);
const R = K * S;
const ARC1 = arcPts(BL, R, 0, 90, 60);       // 아래 왼쪽 꼭짓점이 중심 — BR → TL
const ARC2 = arcPts(TR, R, 180, 270, 60);    // 위 오른쪽 꼭짓점이 중심 — TL → BR
const LEAFP = [...ARC1, ...ARC2.slice(1)];
const SEG1 = [...ARC1];                      // 현 TL–BR 과 ARC1 사이(오른쪽 위 반쪽)
const SEG2 = [...ARC2];
// 오른쪽 풀이 자리: 원의 1/4 를 0.75 배로
const Q0 = [610, 562], QR = R * 0.75;
const QARC = arcPts(Q0, QR, 0, 90, 48);
const QTRI = [Q0, [Q0[0] + QR, Q0[1]], [Q0[0], Q0[1] - QR]];
const ARC_L = (Math.PI / 2) * R;             // 호 하나의 길이(px)
const BAR = (i) => [O[0], 660 + i * 44];

function Scene({ t, C, mode }) {
  const T = mode === "m" ? LEAF.M : LEAF.E;
  const sq = seg(t, 200, 1700, E.out);
  const a1 = seg(t, B.a.arcs + 200, B.a.arcs + 1900, E.io);
  const a2 = seg(t, B.a.arcs + 2000, B.a.arcs + 3700, E.io);
  const fillO = seg(t, B.b.arcs - 500, B.b.arcs + 200);
  // 반쪽: 원의 1/4 − 삼각형
  const qIn = seg(t, B.a.half + 200, B.a.half + 1300, E.io);
  const triIn = seg(t, B.a.half + 1900, B.a.half + 2600);
  const triOut = seg(t, B.a.half + 3600, B.a.half + 4800, E.io);
  const qOut = seg(t, B.a.perim - 400, B.a.perim + 400);
  // × 2 : 반쪽이 가운데를 중심으로 반 바퀴 돌아 다른 반쪽에 포개진다
  const dblK = seg(t, B.a.dbl + 200, B.a.dbl + 1800, E.io);
  const dblO = 1 - seg(t, B.b.dbl, B.b.dbl + 600);
  // 둘레: 두 호가 펴진다
  const per = seg(t, B.a.perim + 400, B.a.perim + 1200);
  const st = [0, 1].map((i) => seg(t, B.a.perim + 1300 + i * 1500, B.a.perim + 2800 + i * 1500, E.io));
  const straight = (arc, i) => arc.map((p, j) => mix2(p, [BAR(i)[0] + (j / (arc.length - 1)) * ARC_L, BAR(i)[1]], st[i]));
  const rot = (p) => {
    const a = Math.PI * dblK, c = Math.cos(a), s = Math.sin(a), x = p[0] - MID[0], y = p[1] - MID[1];
    return [MID[0] + x * c - y * s, MID[1] + x * s + y * c];
  };
  return (
    <g>
      {/* 정사각형 */}
      <Path pts={[BL, BR, TR, TL]} closed stroke={C.ink} sw={3.4} o={sq} />
      <Dim A={TL} B={TR} off={30} lofs={26} s={`${S} cm`} C={C} o={seg(t, 900, 1600)} size={30} />
      <Dim A={BL} B={TL} off={30} lofs={54} s={`${S} cm`} C={C} o={seg(t, 900, 1600)} size={30} />
      {/* 색칠한 부분 */}
      <Path pts={LEAFP} closed fill={C.leaf} fo={0.5 * fillO} stroke="none" />
      {/* 컴퍼스로 호 긋기 */}
      {a1 > 0 && <Path pts={ARC1.slice(0, Math.max(2, Math.ceil(ARC1.length * a1)))} stroke={per > 0 ? C.coral : C.ink} sw={per > 0 ? 6 : 3.4} o={1 - st[0] * 0.999} />}
      {a1 > 0 && a1 < 1 && <Path pts={[BL, ARC1[Math.min(ARC1.length - 1, Math.ceil((ARC1.length - 1) * a1))]]} stroke={C.soft} sw={2} dash="8 7" />}
      {a2 > 0 && <Path pts={ARC2.slice(0, Math.max(2, Math.ceil(ARC2.length * a2)))} stroke={per > 0 ? C.coral : C.ink} sw={per > 0 ? 6 : 3.4} o={1 - st[1] * 0.999} />}
      {a2 > 0 && a2 < 1 && <Path pts={[TR, ARC2[Math.min(ARC2.length - 1, Math.ceil((ARC2.length - 1) * a2))]]} stroke={C.soft} sw={2} dash="8 7" />}
      <Dot p={BL} r={6} fill={C.ink} o={a1 > 0 ? 1 - fillO * 0.6 : 0} />
      <Dot p={TR} r={6} fill={C.ink} o={a2 > 0 ? 1 - fillO * 0.6 : 0} />
      {/* 현(대각선) */}
      <Path pts={[TL, BR]} stroke={C.ink} sw={2.4} dash="10 8" o={seg(t, B.a.half, B.a.half + 500) * (1 - per)} />
      {/* × 2 */}
      {dblK > 0 && <g opacity={dblO}>
        <Glow pts={SEG1} closed C={C} o={1} sw={14} />
        <Path pts={SEG1.map(rot)} closed fill={C.gold} fo={0.55} stroke={C.gold} sw={3} />
        <Lbl x={MID[0] + 60} y={MID[1] - 60} s="× 2" size={44} fill={C.gold} C={C} o={seg(t, B.a.dbl + 1500, B.a.dbl + 1900)} />
      </g>}
      {/* 오른쪽: 원의 1/4 − 삼각형 */}
      <g opacity={qIn * (1 - qOut)}>
        <g transform={`translate(${lerp(-(Q0[0] - BL[0]), 0, qIn)} ${lerp(-(Q0[1] - BL[1]), 0, qIn)})`}>
          <Path pts={[Q0, ...QARC]} closed fill={C.gold} fo={0.36} stroke={C.gold} sw={3} />
          <Lbl x={Q0[0] + QR * 0.62} y={Q0[1] - QR * 0.66} s={T.quarter} size={34} fill={C.gold} C={C} o={seg(t, B.a.half + 1100, B.a.half + 1500) * (1 - triOut)} />
          <g opacity={triIn * (1 - triOut)} transform={`translate(${-70 * triOut} ${70 * triOut})`}>
            <Path pts={QTRI} closed fill={C.coral} fo={0.55} stroke={C.coral} sw={3} />
            <Lbl x={Q0[0] + QR * 0.3} y={Q0[1] - QR * 0.26} s={T.tri} size={34} fill={C.ink} C={C} />
          </g>
          {triOut > 0 && <g opacity={triOut}>
            <Path pts={QARC} stroke={C.gold} sw={5} />
            <Path pts={[QTRI[1], QTRI[2]]} stroke={C.gold} sw={3} dash="9 7" />
            <Lbl x={Q0[0] + QR * 0.83} y={Q0[1] - QR * 0.86} s={T.halfLeaf} size={34} fill={C.gold} C={C} />
          </g>}
        </g>
        <Lbl x={Q0[0] + QR / 2} y={Q0[1] + 46} s={triOut > 0.5 ? "반쪽" : triIn > 0.5 ? "원의 {1/4} − 삼각형" : "원의 {1/4}"} size={30} fill={C.soft} C={C} />
      </g>
      {/* 펴진 호 */}
      {[0, 1].map((i) => st[i] > 0 && (
        <g key={i}>
          <Path pts={straight(i ? ARC2 : ARC1, i)} stroke={C.coral} sw={6} />
          {st[i] >= 1 && <Lbl x={BAR(i)[0] + ARC_L + 18} y={BAR(i)[1]} s={T.arc} size={30} anchor="start" fill={C.coral} C={C} />}
        </g>
      ))}
      <Board x={1066} y={232} t={t} C={C} lines={[
        { t: B.a.half + 500, s: "넓이", k: "h" },
        { t: B.a.half + 1200, s: T.qLine, dot: "gold" },
        { t: B.a.half + 2700, s: T.tLine, dot: "coral" },
        { t: B.a.dbl + 1500, s: T.areaLine1 },
        { t: B.a.dbl + 2200, s: T.areaLine2 },
        { t: B.a.perim + 400, s: "둘레", k: "h" },
        { t: B.a.perim + 3000, s: T.arcLine, dot: "coral" },
        { t: B.a.perim + 4600, s: T.perLine },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: `한 변이 ${S} cm인 정사각형` },
        { t: B.a.arcs, s: "두 꼭짓점을 중심으로 원의 {1/4}을 그려요" },
        { t: B.a.ask, s: "색칠한 부분의 넓이와 둘레는?" },
        { t: B.a.half, s: "반쪽은 원의 {1/4}에서 삼각형을 뺀 모양" },
        { t: B.a.dbl, s: "똑같은 반쪽이 2개" },
        { t: B.a.perim, s: "둘레는 원의 {1/4}인 호 2개" },
        { t: B.a.hold, s: mode === "m" ? `넓이 ${LEAF.M.area} cm², 둘레 ${LEAF.M.per} cm` : `넓이 ${LEAF.E.area} cm², 둘레 ${LEAF.E.per} cm` },
      ]} />
    </g>
  );
}

export default {
  key: "leaf",
  dur: B.dur,
  title: { e: "색칠한 부분의 넓이와 둘레", m: "색칠한 부분의 넓이와 둘레" },
  sub: { e: "초등 · 원주율 3.14", m: "중등 · 원주율 π" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};

