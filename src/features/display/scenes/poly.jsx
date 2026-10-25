// 장면 8 — 다각형의 각의 합 (초등: 삼각형으로 나눠 빈 각 ↔ 중등: 180°×(n−2), 일차식 각)
// 한 꼭짓점에서 대각선을 그어 삼각형으로 나누는 같은 그림 위에서, 초등은 ㉠ 을 빼기로, 중등은 x 를 방정식으로.
import { beats, seg, E, lerp, centroid2 } from "../core";
import { Board, Caption, Path, Lbl, Angle, Dot } from "../draw";
import { POLY } from "../facts";

const B = beats([["q_in", 2000], ["q_split", 2600], ["q_calc", 4600], ["p_in", 1600], ["p_split", 2800], ["p_calc", 5600],
  ["h_in", 1400], ["h_split", 2600], ["gen", 3400], ["hold", 2400]]);
const S = 54, CX = 500, CY = 438;
const fit = (pts) => {
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  const mx = (Math.min(...xs) + Math.max(...xs)) / 2, my = (Math.min(...ys) + Math.max(...ys)) / 2;
  return pts.map(([x, y]) => [CX + S * (x - mx), CY - S * (y - my)]);
};
const Q = fit(POLY.quad), P5 = fit(POLY.pent), P6 = fit(POLY.hex);
const TRI_COL = ["coral", "sky", "leaf", "lilac"];

function Shape({ pts, t, t0, tSplit, labels, C, o, angleO = 1 }) {
  if (o <= 0.001) return null;
  const n = pts.length;
  const draw = seg(t, t0, t0 + 1100, E.out);
  const diag = (k) => seg(t, tSplit + 200 + (k - 2) * 600, tSplit + 800 + (k - 2) * 600, E.io);
  const triO = (k) => seg(t, tSplit + 500 + (k - 1) * 600, tSplit + 1000 + (k - 1) * 600);
  return (
    <g opacity={o}>
      {Array.from({ length: n - 2 }, (_, i) => i + 1).map((k) => {
        const tri = [pts[0], pts[k], pts[k + 1]];
        const c = centroid2(tri);
        const a = triO(k);
        return a > 0 && <g key={k} opacity={a}>
          <Path pts={tri} closed fill={C[TRI_COL[(k - 1) % 4]]} fo={0.26} stroke="none" />
          <Lbl x={c[0]} y={c[1]} s={String(k)} size={30} fill={C[TRI_COL[(k - 1) % 4]]} C={C} />
        </g>;
      })}
      <Path pts={pts} closed stroke={C.ink} sw={3.6} o={draw} />
      {Array.from({ length: n - 3 }, (_, i) => i + 2).map((k) => {
        const d = diag(k);
        return d > 0 && <Path key={k} pts={[pts[0], [lerp(pts[0][0], pts[k][0], d), lerp(pts[0][1], pts[k][1], d)]]} stroke={C.ink} sw={2.6} dash="10 8" />;
      })}
      {labels && pts.map((V, i) => (
        <g key={i} opacity={seg(t, t0 + 600 + i * 120, t0 + 1100 + i * 120) * angleO}>
          <Angle V={V} A={pts[(i - 1 + n) % n]} B={pts[(i + 1) % n]} r={38} C={C} color={labels[i].hi ? C.gold : C.ink}
            label={labels[i].s} lsize={28} lr={labels[i].far ? 104 : 76} fillO={labels[i].hi ? 0.25 : 0.1} sw={2.6} />
        </g>
      ))}
      <Dot p={pts[0]} r={6} fill={C.ink} o={draw} />
    </g>
  );
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const T = isM ? POLY.M : POLY.E;
  const qO = 1 - seg(t, B.a.p_in, B.a.p_in + 900);
  const pO = seg(t, B.a.p_in + 500, B.b.p_in) * (1 - seg(t, B.a.h_in, B.a.h_in + 800));
  const hO = seg(t, B.a.h_in + 400, B.b.h_in);
  const qSolved = isM && t > B.a.q_calc + 3000;
  const pSolved = isM && t > B.a.p_calc + 4200;
  const qLab = T.qLab.map((s, i) => ({ s: i === 3 && qSolved ? T.qSolved : s, hi: i === 3, far: false }));
  const pLab = T.pLab.map((s, i) => ({
    s: isM && pSolved && i >= 3 ? T.pSolved[i - 3] : s,
    hi: isM ? i >= 3 : i === 4, far: isM && i >= 3 && !pSolved,
  }));
  const rowT = isM
    ? [B.a.q_split + 300, B.a.q_calc + 300, B.a.q_calc + 2000, B.a.p_split + 300, B.a.p_calc + 300, B.a.p_calc + 1800, B.a.p_calc + 3600, B.a.gen, B.a.gen + 900]
    : [B.a.q_split + 300, B.a.q_calc + 300, B.a.q_calc + 2000, B.a.p_split + 300, B.a.p_calc + 300, B.a.p_calc + 2400, B.a.h_split + 300, B.a.gen + 300];
  return (
    <g>
      <Shape pts={Q} t={t} t0={300} tSplit={B.a.q_split} labels={qLab} C={C} o={qO} />
      <Shape pts={P5} t={t} t0={B.a.p_in + 400} tSplit={B.a.p_split} labels={pLab} C={C} o={pO} />
      <Shape pts={P6} t={t} t0={B.a.h_in + 300} tSplit={B.a.h_split} labels={null} C={C} o={hO} />
      <Board x={980} y={222} t={t} C={C} size={36} lh={54} lines={T.board.map((L, i) => ({ ...L, t: rowT[i], row: i }))} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: "사각형의 네 각" },
        { t: B.a.q_split, s: "한 꼭짓점에서 대각선을 그으면 삼각형 2개" },
        { t: B.a.q_calc, s: isM ? "내각의 합으로 식을 세워 x를 구해요" : "네 각의 합 360°에서 아는 세 각을 빼요" },
        { t: B.a.p_in, s: "오각형은?" },
        { t: B.a.p_split, s: "삼각형 3개 → 180° × 3" },
        { t: B.a.p_calc, s: isM ? "두 각이 x에 대한 식 — 일차방정식" : "다섯 각의 합 540°에서 아는 네 각을 빼요" },
        { t: B.a.h_in, s: "육각형은 삼각형 4개" },
        { t: B.a.gen, s: isM ? "n각형은 삼각형 (n − 2)개 → 180° × (n − 2)" : "꼭짓점이 하나 늘 때마다 180°씩 늘어나요" },
      ]} />
    </g>
  );
}

export default {
  key: "poly",
  dur: B.dur,
  title: { e: "사각형·다각형의 각", m: "다각형의 내각의 크기의 합" },
  sub: { e: "초등 · 각도", m: "중등 · 다각형" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
