// 장면 9 — 다각형의 대각선 (초등: 하나씩 그으며 세기 ↔ 중등: n(n−3)/2, 대각선 20개인 다각형 찾기)
// 같은 육각형 → 같은 팔각형. 초등은 꼭짓점마다 새로 생기는 대각선을 세고, 중등은 꼭짓점마다 (n−3)개씩 두 번 세어 ÷2.
import { beats, seg, E, lerp, polar } from "../core";
import { Board, Caption, Path, Dot, MText } from "../draw";
import { DIAG } from "../facts";

const B = beats([["hex_in", 1600], ["hex", 7600], ["hex_sum", 2400], ["oct_in", 1600], ["oct", 9200], ["oct_sum", 2600], ["hold", 2400]]);
const CEN = [480, 440];
const poly = (n, r) => Array.from({ length: n }, (_, i) => polar(CEN, r, 90 - (i * 360) / n));
const HEX = poly(6, 250), OCT = poly(8, 262);
/** 초등 순서: 꼭짓점 0 부터, 새로 생기는 대각선 */
const orderE = (n) => { const out = []; for (let i = 0; i < n; i++) for (let j = i + 2; j < n; j++) if (!(i === 0 && j === n - 1)) out.push([i, j]); return out; };
/** 중등 순서: 꼭짓점마다 (n−3)개 — 같은 대각선을 두 번 만난다 */
const orderM = (n) => Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => j).filter((j) => j !== i && j !== (i + 1) % n && j !== (i - 1 + n) % n).map((j) => [i, j]));

function Fig({ pts, t, t0, tD, durD, C, mode, o }) {
  if (o <= 0.001) return null;
  const n = pts.length;
  const draw = seg(t, t0, t0 + 1000, E.out);
  const out = [];
  let shown = 0, cur = null;
  if (mode === "e") {
    const L = orderE(n), step = durD / L.length;
    L.forEach(([i, j], k) => {
      const a = tD + k * step, p = seg(t, a, a + step * 0.8, E.io);
      if (p <= 0) return;
      shown = k + 1;
      const hot = t < a + step * 1.4;
      if (hot) cur = i;
      out.push(<Path key={k} pts={[pts[i], [lerp(pts[i][0], pts[j][0], p), lerp(pts[i][1], pts[j][1], p)]]}
        stroke={hot ? C.gold : C.ink} sw={hot ? 5 : 2.6} o={hot ? 1 : 0.75} />);
    });
  } else {
    const G = orderM(n), step = durD / n;
    const seen = new Set();
    G.forEach((grp, i) => {
      const a = tD + i * step, p = seg(t, a, a + step * 0.55, E.io);
      if (p <= 0) return;
      const hot = t < a + step;
      if (hot) cur = i;
      grp.forEach(([u, v], k) => {
        const key = Math.min(u, v) + "-" + Math.max(u, v);
        const twice = seen.has(key);
        seen.add(key);
        out.push(<Path key={`${i}-${k}`} pts={[pts[u], [lerp(pts[u][0], pts[v][0], p), lerp(pts[u][1], pts[v][1], p)]]}
          stroke={hot ? C.teal : twice ? C.lilac : C.ink} sw={hot ? 5 : twice ? 3.4 : 2.6} o={hot ? 1 : 0.75} />);
      });
      shown = (i + 1) * (n - 3);
    });
  }
  return (
    <g opacity={o}>
      <Path pts={pts} closed stroke={C.ink} sw={3.6} fill={C.ink} fo={0.04} o={draw} />
      {out}
      {pts.map((p, i) => <Dot key={i} p={p} r={cur === i ? 12 : 7} fill={cur === i ? (mode === "e" ? C.gold : C.teal) : C.ink} o={draw} />)}
      {shown > 0 && <MText x={CEN[0] + (n === 6 ? 330 : 340)} y={CEN[1] + 250}
        s={mode === "e" ? `${shown}개` : t > tD + durD + 300 ? `${shown} ÷ 2 = ${shown / 2}개` : `${shown}번`} size={46} weight={800}
        anchor="start" fill={mode === "e" ? C.gold : C.teal} C={C} />}
    </g>
  );
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const T = isM ? DIAG.M : DIAG.E;
  const hexO = 1 - seg(t, B.a.oct_in, B.a.oct_in + 900);
  const octO = seg(t, B.a.oct_in + 500, B.b.oct_in);
  const rowT = isM
    ? [B.a.hex + 200, B.a.hex + 1200, B.a.hex_sum + 200, B.a.hex_sum + 1100, B.a.hex_sum + 1700, B.a.oct_in, B.a.oct + 700, B.a.oct + 3200]
    : [400, 1000, B.a.hex, B.a.hex_sum + 200, B.a.oct_in + 200, B.a.oct_sum + 200];
  return (
    <g>
      <Fig pts={HEX} t={t} t0={200} tD={B.a.hex + 300} durD={6800} C={C} mode={mode} o={hexO} />
      <Fig pts={OCT} t={t} t0={B.a.oct_in + 400} tD={B.a.oct + (isM ? 4200 : 300)} durD={isM ? 4600 : 8600} C={C} mode={mode} o={octO} />
      <Board x={980} y={222} t={t} C={C} size={36} lh={58} lines={T.board.map((L, i) => ({ ...L, t: rowT[i], row: i }))} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: "육각형의 대각선은 몇 개일까?" },
        { t: B.a.hex, s: isM ? "한 꼭짓점에서 (6 − 3)개씩, 모든 꼭짓점에서" : "꼭짓점 차례로, 새로 생기는 대각선을 세요" },
        { t: B.a.hex_sum, s: isM ? "같은 대각선을 두 번씩 세었으니 ÷ 2" : `육각형의 대각선은 ${DIAG.count(6)}개` },
        { t: B.a.oct_in, s: isM ? `대각선이 ${DIAG.target}개인 다각형은?` : "팔각형은?" },
        { t: B.a.oct_sum, s: isM ? `n = ${DIAG.nFor}, 팔각형 — 대각선 ${DIAG.target}개` : `팔각형의 대각선은 ${DIAG.count(8)}개` },
      ]} />
    </g>
  );
}

export default {
  key: "diag",
  dur: B.dur,
  title: { e: "다각형의 대각선", m: "대각선의 개수" },
  sub: { e: "초등 · 다각형", m: "중등 · 다각형" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
