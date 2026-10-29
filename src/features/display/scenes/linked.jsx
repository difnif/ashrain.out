// 장면 — 이어진 문제 함께 고르기(초등 · 가능성) ↔ 이게 맞으면 저것도: 맞물린 답 찍기(중2 · 확률)
// 3번은 ②·④, 7번은 ①·③ 가운데 고민. 7번 보기를 보니 "3번이 ②면 7번은 ①, ④면 ③" — 답이 맞물려 있다.
//   고를 수 있는 짝 4가지 중 말이 되는 짝(맞물린 짝)은 2가지. 어긋난 짝을 고르면 늘 "딱 한 문제" 맞는다.
//   따로 찍기: 둘 다 {1/4} · 하나 {1/2} · 0 {1/4} → 평균 1문제
//   맞물려 찍기: 둘 다 {1/2} · 0 {1/2} → 평균 1문제(같다) — 모 아니면 도
//   3번 ②에 70% 확신: 따로 평균 1.2(둘 다 35%) · 맞물려 1.4(둘 다 70%) — 확신이 7번으로 옮겨 간다
import { beats, seg, win, E, lerp } from "../core";
import { Board, Caption, MText, Path } from "../draw";
import { LINKED, fracS, pctS } from "../guess.js";

const B = beats([
  ["intro", 3400], ["link", 5400], ["grid", 7200], ["indep", 6800], ["linked", 6800], ["compare", 6600], ["conf", 9600], ["sum", 5600], ["hold", 1800],
]);
const Q3 = { x0: 70, title: "3번", opts: LINKED.Q3, bx: 232 };
const Q7 = { x0: 450, title: "7번", opts: LINKED.Q7, bx: 612 };
const ROWY = [318, 440];
const plain = (s) => String("①②③④⑤".indexOf(s) + 1);           // 동그라미 안에는 숫자만
const GR = { x0: 1010, y0: 180, cw: 150, rh: 84, hw: 96 };       // 짝 표(머리 칸 너비 hw)
const CH = { base: 712, h: 230, gx: [960, 1270], bw: 54, gap: 22 };

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const o = seg(t, 200, 1100);
  const linkO = seg(t, B.a.link + 800, B.a.link + 1800);
  const confO = seg(t, B.a.conf + 400, B.a.conf + 1000);
  return (
    <g>
      {/* 두 문제 카드 */}
      {[Q3, Q7].map((q, qi) => (
        <g key={qi} opacity={o}>
          <rect x={q.x0} y={166} width={324} height={344} rx={16} fill={C.card} stroke={C.cardEdge} strokeWidth={2} />
          <MText x={q.x0 + 26} y={222} s={q.title} size={34} weight={800} C={C} />
          <MText x={q.x0 + 26} y={256} s={isM ? "둘 중 고민" : "둘 중에 고민"} size={22} weight={700} fill={C.soft} C={C} />
          {q.opts.map((s, i) => {
            const conf = qi === 0 && i === 0 ? confO : 0;
            return (
              <g key={i}>
                <circle cx={q.bx} cy={ROWY[i]} r={40} fill={C.paper} stroke={C.ink} strokeWidth={3} />
                <text x={q.bx} y={ROWY[i] + 15} fontSize={42} fontWeight={800} textAnchor="middle" fill={C.ink}>{plain(s)}</text>
                {conf > 0.01 && <g opacity={conf}>
                  <circle cx={q.bx} cy={ROWY[i]} r={48} fill="none" stroke={C.gold} strokeWidth={5} />
                  <MText x={q.bx - 70} y={ROWY[i] + 10} s="70%" size={30} weight={800} anchor="end" fill={C.gold} C={C} />
                </g>}
              </g>
            );
          })}
        </g>
      ))}
      {/* 맞물림: ②—① · ④—③ */}
      {[0, 1].map((i) => (
        <g key={i} opacity={linkO}>
          <Path pts={[[Q3.bx + 44, ROWY[i]], [Q7.bx - 44, ROWY[i]]]} stroke={C.coral} sw={5} dash="10 7" />
          <circle cx={Q3.bx + 44} cy={ROWY[i]} r={6} fill={C.coral} /><circle cx={Q7.bx - 44} cy={ROWY[i]} r={6} fill={C.coral} />
        </g>
      ))}
      <MText x={422} y={ROWY[1] + 62} s={isM ? "맞물린 답" : "이어진 답"} size={24} weight={800} anchor="middle" fill={C.coral} opacity={linkO} C={C} />
      <Pairs t={t} C={C} isM={isM} />
      <Chart t={t} C={C} isM={isM} />
      <Board x={86} y={594} t={t} C={C} size={28} lh={48} lines={isM ? [
        { t: B.a.link + 1400, s: `맞물린 짝: (${LINKED.Q3[0]}, ${LINKED.Q7[0]}) · (${LINKED.Q3[1]}, ${LINKED.Q7[1]})`, u: B.a.grid + 200 },
        { t: B.a.grid + 2600, s: "맞물린 짝 → 두 문제 맞거나, 둘 다 틀림", row: 0, u: B.a.indep },
        { t: B.a.grid + 4200, s: "어긋난 짝 → 늘 딱 한 문제만 맞음", row: 1, u: B.a.indep },
        { t: B.a.indep + 400, s: "따로 찍기: 4가지 중 하나 → 둘 다 ‹{1/4}›", row: 0, u: B.a.conf },
        { t: B.a.linked + 400, s: "맞물려 찍기: 2가지 중 하나 → 둘 다 ‹{1/2}›", row: 1, u: B.a.conf },
        { t: B.a.compare + 600, s: "평균은 둘 다 1문제 — 맞물리면 '모 아니면 도'", row: 2, u: B.a.conf, size: 26 },
        { t: B.a.conf + 1200, s: "3번 ②가 70%쯤 맞는 것 같다면", k: "h", row: 0 },
        { t: B.a.conf + 2600, s: `따로: 0.7 + 0.5 = ‹${LINKED.meanP(LINKED.pIndep).toFixed(1)}›문제`, row: 1 },
        { t: B.a.conf + 4400, s: `맞물려: 0.7 × 2 = ‹${LINKED.meanP(LINKED.pLinked).toFixed(1)}›문제`, row: 2 },
      ] : [
        { t: B.a.link + 1400, s: `이어진 짝: (${LINKED.Q3[0]}, ${LINKED.Q7[0]}) · (${LINKED.Q3[1]}, ${LINKED.Q7[1]})`, u: B.a.grid + 200 },
        { t: B.a.grid + 2600, s: "이어진 짝 → 둘 다 맞거나 둘 다 틀려요", row: 0, u: B.a.indep },
        { t: B.a.grid + 4200, s: "어긋난 짝 → 늘 하나만 맞아요", row: 1, u: B.a.indep },
        { t: B.a.indep + 400, s: "따로 고르면 둘 다 맞을 가능성: 4가지 중 1가지", row: 0, u: B.a.conf, size: 25 },
        { t: B.a.linked + 400, s: "이어서 고르면: 2가지 중 1가지(반반)", row: 1, u: B.a.conf },
        { t: B.a.compare + 600, s: "대신 둘 다 틀릴 가능성도 반반", row: 2, u: B.a.conf },
        { t: B.a.conf + 1200, s: "3번이 거의 확실하다면", k: "h", row: 0 },
        { t: B.a.conf + 2600, s: "7번도 이어진 답을 고르면", row: 1 },
        { t: B.a.conf + 4400, s: "둘 다 맞힐 가능성이 훨씬 커져요", row: 2 },
      ]} />
      <Caption t={t} C={C} y={862} size={32} caps={isM ? [
        { t: 300, s: `3번은 ${LINKED.Q3.join("와 ")}, 7번은 ${LINKED.Q7.join("과 ")} 사이에서 고민 중` },
        { t: B.a.link + 300, s: `7번 보기를 보니 — 3번이 ${LINKED.Q3[0]}면 7번은 ${LINKED.Q7[0]}, ${LINKED.Q3[1]}면 ${LINKED.Q7[1]}이어야 말이 돼요` },
        { t: B.a.grid + 300, s: "고를 수 있는 짝은 2 × 2 = 4가지 — 말이 되는 짝은 2가지" },
        { t: B.a.indep + 300, s: "맞물림을 생각하지 않고 따로 찍으면?" },
        { t: B.a.linked + 300, s: "말이 되는 짝으로만 찍으면?" },
        { t: B.a.compare + 300, s: "둘 다 맞힐 확률은 2배({1/4} → {1/2}), 평균 맞히는 수는 똑같이 1문제" },
        { t: B.a.conf + 300, s: "3번에 확신이 조금 있다면? — 맞물림이 그 확신을 7번으로 옮겨 줘요" },
        { t: B.a.sum + 300, s: "맞물린 답은 확신을 옮겨 줘요 — 확신이 없으면 모 아니면 도" },
      ] : [
        { t: 300, s: `3번은 ${LINKED.Q3.join("와 ")}, 7번은 ${LINKED.Q7.join("과 ")} 가운데 고민 중이에요` },
        { t: B.a.link + 300, s: `7번 보기를 보니 3번이 ${LINKED.Q3[0]}면 7번은 ${LINKED.Q7[0]}이에요` },
        { t: B.a.grid + 300, s: "짝은 4가지 — 그중 말이 되는 짝은 2가지" },
        { t: B.a.indep + 300, s: "따로따로 고르면 둘 다 맞을 가능성은 4가지 중 1가지" },
        { t: B.a.linked + 300, s: "말이 되는 짝으로 고르면 2가지 중 1가지 — 반반" },
        { t: B.a.compare + 300, s: "둘 다 맞을 가능성은 커지지만, 둘 다 틀릴 가능성도 커져요" },
        { t: B.a.conf + 300, s: "3번 답이 거의 확실하면 7번도 함께 맞힐 수 있어요" },
        { t: B.a.sum + 300, s: "서로 이어진 문제는 함께 생각해요" },
      ]} />
    </g>
  );
}

/** 짝 표(2 × 2): 칸마다 짝 · 맞물림 여부 · (따로) {1/4} · (맞물려) {1/2} 또는 지움 */
function Pairs({ t, C, isM }) {
  const o = win(t, B.a.grid + 200, B.a.conf, 500, 500);
  if (o <= 0.01) return null;
  const { x0, y0, cw, rh, hw } = GR;
  const cells = [];
  for (let r = 0; r < 2; r++) for (let c = 0; c < 2; c++) {
    const ok = r === c, x = x0 + hw + c * cw, y = y0 + 44 + r * rh;
    const a = seg(t, B.a.grid + 700 + (2 * r + c) * 300, B.a.grid + 1100 + (2 * r + c) * 300);
    const tagO = seg(t, B.a.grid + (ok ? 2600 : 4200), B.a.grid + (ok ? 3000 : 4600));
    const quarter = seg(t, B.a.indep + 1000, B.a.indep + 1500);
    const crossO = ok ? 0 : seg(t, B.a.linked + 1000, B.a.linked + 1500);
    const half = ok ? seg(t, B.a.linked + 1600, B.a.linked + 2100) : 0;
    cells.push(
      <g key={`${r}${c}`} opacity={a}>
        <rect x={x + 4} y={y + 4} width={cw - 8} height={rh - 8} rx={10} fill={ok ? C.gold : C.ink} fillOpacity={ok ? 0.16 * tagO + 0.04 : 0.06}
          stroke={ok ? C.gold : C.soft} strokeWidth={ok ? 3 * tagO + 1 : 1.5} opacity={1 - 0.6 * crossO} />
        <MText x={x + cw / 2} y={y + 36} s={`${LINKED.Q3[r]} · ${LINKED.Q7[c]}`} size={28} weight={800} anchor="middle" opacity={1 - 0.6 * crossO} C={C} />
        <MText x={x + cw / 2} y={y + 66} s={ok ? (isM ? "2 또는 0" : "둘 다/0") : (isM ? "딱 1" : "하나만")} size={19} weight={700} anchor="middle"
          fill={ok ? C.gold : C.soft} opacity={tagO * (1 - 0.6 * crossO) * (1 - Math.max(quarter, half))} C={C} />
        <MText x={x + cw / 2} y={y + 72} s={half > 0 ? "{1/2}" : "{1/4}"} size={24} weight={800} anchor="middle" fill={half > 0 ? C.gold : C.teal}
          opacity={Math.max(quarter * (1 - crossO) * (1 - half), half)} C={C} />
        {crossO > 0.01 && <Path pts={[[x + 18, y + 18], [x + cw - 18, y + rh - 18]]} stroke={C.coral} sw={5} o={crossO} />}
      </g>,
    );
  }
  return (
    <g opacity={o}>
      <MText x={x0 + hw + cw} y={y0 + 26} s="7번" size={24} weight={800} anchor="middle" fill={C.soft} C={C} />
      <MText x={x0 + hw / 2} y={y0 + 44 + rh + 8} s="3번" size={24} weight={800} anchor="middle" fill={C.soft} C={C} />
      {cells}
    </g>
  );
}

/** 맞힌 문제 수(0 · 1 · 2)의 확률 — 따로 · 맞물려. 확신 장면에서는 70% 값으로 바뀐다 */
function Chart({ t, C, isM }) {
  const o = seg(t, B.a.indep + 300, B.a.indep + 900);
  if (o <= 0.01) return null;
  const k = seg(t, B.a.conf + 2000, B.a.conf + 3400, E.io);
  const v = (d) => d.map((p) => p[0] / p[1]);
  const groups = [
    { name: isM ? "따로 찍기" : "따로 고르기", vals: v(LINKED.indep).map((x, j) => lerp(x, LINKED.pIndep[j], k)), at: B.a.indep + 1400, col: C.teal,
      mean: lerp(LINKED.mean(LINKED.indep), LINKED.meanP(LINKED.pIndep), k) },
    { name: isM ? "맞물려 찍기" : "이어서 고르기", vals: v(LINKED.linked).map((x, j) => lerp(x, LINKED.pLinked[j], k)), at: B.a.linked + 2200, col: C.gold,
      mean: lerp(LINKED.mean(LINKED.linked), LINKED.meanP(LINKED.pLinked), k) },
  ];
  const lab = (x) => {
    if (k > 0 && k < 1) return "";
    if (k >= 1) return pctS(x);
    for (const [n, d] of [[0, 1], [1, 4], [1, 2]]) if (Math.abs(x - n / d) < 1e-9) return fracS([n, d]);
    return pctS(x);
  };
  return (
    <g opacity={o}>
      <MText x={940} y={CH.base - CH.h - 46} s={isM ? "맞힌 문제 수의 확률" : "맞힌 문제 수"} size={24} weight={800} fill={C.soft} C={C} />
      {groups.map((g, gi) => {
        const a = seg(t, g.at, g.at + 600), grow = seg(t, g.at, g.at + 1100, E.out);
        const X = CH.gx[gi];
        return (
          <g key={gi} opacity={a}>
            <Path pts={[[X - 10, CH.base], [X + 3 * (CH.bw + CH.gap) - CH.gap + 10, CH.base]]} stroke={C.ink} sw={2.4} />
            {g.vals.map((x, j) => {
              const h = x * CH.h * grow, bx = X + j * (CH.bw + CH.gap);
              return (
                <g key={j}>
                  {h > 0.5 && <rect x={bx} y={CH.base - h} width={CH.bw} height={h} rx={4} fill={g.col} fillOpacity={0.82} />}
                  <MText x={bx + CH.bw / 2} y={CH.base - h - 12} s={lab(x)} size={22} weight={800} anchor="middle" fill={g.col} opacity={grow} C={C} />
                  <MText x={bx + CH.bw / 2} y={CH.base + 24} s={`${j}`} size={20} weight={700} anchor="middle" fill={C.soft} C={C} />
                </g>
              );
            })}
            <MText x={X + (3 * (CH.bw + CH.gap) - CH.gap) / 2} y={CH.base + 56} s={g.name} size={24} weight={800} anchor="middle" fill={g.col} C={C} />
            <MText x={X + (3 * (CH.bw + CH.gap) - CH.gap) / 2} y={CH.base + 88} s={`평균 ‹${(Math.round(g.mean * 10) / 10).toFixed(1)}›문제`} size={22} weight={700}
              anchor="middle" opacity={seg(t, B.a.compare + 600, B.a.compare + 1200)} C={C} />
          </g>
        );
      })}
    </g>
  );
}

export default {
  key: "linked",
  dur: B.dur,
  title: { e: "이어진 문제 함께 고르기", m: "이게 맞으면 저것도 — 맞물린 답 찍기" },
  sub: { e: "초등 · 일이 일어날 가능성", m: "중2 · 확률의 계산" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
