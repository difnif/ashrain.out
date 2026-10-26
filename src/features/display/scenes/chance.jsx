// 장면 17 — 일이 일어날 가능성(초등) ↔ 확률의 뜻과 성질 · 어떤 사건이 일어나지 않을 확률(중2)
// 같은 주머니(구슬 4개)의 빨간 구슬이 0개 → 4개로 늘고, 같은 수직선 위의 점이 오른쪽으로 간다.
//   초등: 불가능하다 · ~아닐 것 같다 · 반반이다 · ~일 것 같다 · 확실하다 → 수로 0, {1/2}, 1
//   중등: p = 0, {1/4}, {1/2}, {3/4}, 1 → 0 ≤ p ≤ 1 → 일어나지 않을 확률 1 − p
import { beats, seg, win, E, lerp } from "../core";
import { Board, Caption, MText, Path } from "../draw";
import { CHANCE } from "../facts";

const { WORDS, REDS, P, PRAW, comp } = CHANCE;
const B = beats([["intro", 2400], ["b0", 3400], ["b1", 3400], ["b2", 3400], ["b3", 3400], ["b4", 3400], ["prop", 5000], ["comp", 5600], ["hold", 2400]]);
const BAGS = ["b0", "b1", "b2", "b3", "b4"];
const MARB = [[290, 410], [392, 410], [290, 508], [392, 508]];
const LX0 = 140, LX1 = 1040, LY = 700;
const lx = (p) => LX0 + (LX1 - LX0) * p;

/** 지금 주머니의 빨간 구슬 수(소수: 바뀌는 중) */
function redsAt(t) {
  let r = 0;
  for (let k = 1; k < BAGS.length; k++) r += seg(t, B.a[BAGS[k]] + 200, B.a[BAGS[k]] + 900, E.io);
  r -= (REDS[4] - comp) * seg(t, B.a.comp + 200, B.a.comp + 900, E.io);
  return r;
}

function Bag({ C, o }) {
  const body = "M250 262 C 150 330, 140 560, 340 590 C 540 560, 530 330, 450 262 Z";
  const frill = "M262 258 Q 246 222 280 212 Q 304 236 340 218 Q 376 236 400 212 Q 434 222 438 258";
  return (
    <g opacity={o}>
      <path d={body} fill={C.wood} fillOpacity={0.22} stroke={C.ink} strokeOpacity={0.6} strokeWidth={3} strokeLinejoin="round" />
      <path d={frill} fill={C.wood} fillOpacity={0.3} stroke={C.ink} strokeOpacity={0.6} strokeWidth={3} strokeLinejoin="round" />
      <rect x={252} y={252} width={196} height={14} rx={7} fill={C.gold} opacity={0.85} />
    </g>
  );
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const intro = seg(t, 200, 1200);
  const reds = redsAt(t);
  const p = reds / 4;
  const ptO = seg(t, B.a.b0 + 200, B.a.b0 + 700);
  const numO = isM ? seg(t, B.a.b0 + 400, B.a.b0 + 1000) : seg(t, B.a.prop + 600, B.a.prop + 1200);
  const compO = seg(t, B.a.comp + 1000, B.a.comp + 1600);
  const near = (k) => Math.max(0, 1 - Math.abs(p - k / 4) * 8);           // 점이 가까운 낱말을 밝힌다
  const redNow = Math.round(reds);
  // 기약분수가 아니면 약분한 값까지: {2/4} = {1/2}
  const rowText = (k) => (isM ? (P[k] === PRAW[k] ? `*p* = ‹${P[k]}›` : `*p* = ${PRAW[k]} = ‹${P[k]}›`)
    : `빨강 ${REDS[k]}개 / 4개 → ‹${WORDS[k]}›`);
  const rowLines = [
    ...BAGS.map((b, k) => ({ t: B.a[b] + 900, u: k < 4 ? B.a[BAGS[k + 1]] + 900 : B.a.comp + 900, row: 1, s: rowText(k) })),
    { t: B.a.comp + 900, row: 1, s: rowText(comp) },                     // 여사건을 볼 주머니(빨강 3개)
  ];
  return (
    <g>
      <g transform="translate(0 -24)">
      <Bag C={C} o={intro} />
      {/* 구슬 — j번째 구슬은 빨간 구슬 수가 j보다 크면 빨강 */}
      {MARB.map(([x, y], j) => {
        const drop = seg(t, 400 + j * 240, 900 + j * 240, E.drop);
        const k = Math.max(0, Math.min(1, reds - j));                       // 0 파랑 → 1 빨강
        const sw = Math.abs(k - 0.5) < 0.5 ? 1 - 0.35 * Math.sin(Math.PI * k) : 1; // 바뀔 때 잠깐 작아진다
        return drop > 0 && (
          <g key={j} transform={`translate(${x} ${lerp(y - 260, y, drop)}) scale(${sw})`}>
            <circle r={42} fill={C.blue} opacity={1 - k} />
            <circle r={42} fill={C.red} opacity={k} />
            <circle cx={-13} cy={-14} r={11} fill="#fff" opacity={0.35} />
          </g>
        );
      })}
      </g>
      <MText x={340} y={606} s={isM ? `빨간 구슬 ${redNow}개 / 전체 4개` : `빨간 구슬 ${redNow}개`} size={28}
        weight={700} anchor="middle" fill={C.soft} opacity={seg(t, B.a.b0, B.a.b0 + 500) * (1 - seg(t, B.a.prop, B.a.prop + 400)) + seg(t, B.a.comp + 900, B.a.comp + 1300)} C={C} />
      {/* 수직선 */}
      <g opacity={intro}>
        <Path pts={[[LX0 - 20, LY], [LX1 + 20, LY]]} stroke={C.ink} sw={3.4} />
        {WORDS.map((w, k) => (
          <g key={w}>
            <line x1={lx(k / 4)} x2={lx(k / 4)} y1={LY - 12} y2={LY + 12} stroke={C.ink} strokeWidth={3} />
            <MText x={lx(k / 4)} y={LY + 50} s={w} size={24} weight={700} anchor="middle"
              fill={near(k) > 0.4 && ptO > 0 ? C.gold : C.soft} opacity={isM ? 0.55 : 1} C={C} />
          </g>
        ))}
        {/* 수: 중등은 다섯 곳 모두, 초등은 0 · 1/2 · 1 */}
        {P.map((s, k) => (isM || k % 2 === 0) && (
          <MText key={"n" + k} x={lx(k / 4)} y={LY - 30} s={s} size={isM ? 30 : 30} weight={800} anchor="middle"
            fill={isM ? C.teal : C.gold} opacity={numO} C={C} />
        ))}
      </g>
      {/* 여사건: 빨강 3/4 ↔ 나머지 1/4 */}
      {compO > 0 && <g opacity={compO}>
        <Path pts={[[lx(comp / 4), LY], [lx(1), LY]]} stroke={C.red} sw={9} o={isM ? 0.85 : 0} />
        <Path pts={[[lx(0), LY], [lx(1 - comp / 4), LY]]} stroke={C.blue} sw={9} o={0.85} />
        <circle cx={lx(1 - comp / 4)} cy={LY} r={17} fill={C.blue} stroke={C.paper} strokeWidth={3} />
      </g>}
      {/* 빨간 구슬 점 */}
      {ptO > 0 && <g opacity={ptO}>
        <circle cx={lx(p)} cy={LY} r={18} fill={C.red} stroke={C.paper} strokeWidth={3} />
      </g>}
      <Board x={700} y={232} t={t} C={C} size={34} lh={60} lines={isM ? [
        { t: B.a.b0 + 200, s: "빨간 구슬이 나올 확률 *p*", k: "h", row: 0 },
        ...rowLines,
        { t: B.a.prop + 200, s: "확률의 성질", k: "h", row: 2 },
        { t: B.a.prop + 900, s: "‹0 ≤ *p* ≤ 1›", row: 3 },
        { t: B.a.prop + 2400, s: "절대 일어나지 않으면 ‹0›, 반드시 일어나면 ‹1›", row: 4 },
        { t: B.a.comp + 200, s: "빨간 구슬이 나오지 않을 확률", k: "h", row: 5 },
        { t: B.a.comp + 1800, s: `1 − *p* = ${CHANCE.compLine}`, row: 6 },
      ] : [
        { t: B.a.b0 + 200, s: "빨간 구슬을 꺼낼 가능성", k: "h", row: 0 },
        ...rowLines,
        { t: B.a.prop + 200, s: "가능성을 수로 나타내면", k: "h", row: 2 },
        { t: B.a.prop + 900, s: "불가능하다 ‹0› · 반반이다 ‹{1/2}› · 확실하다 ‹1›", row: 3 },
        { t: B.a.comp + 200, s: "파란 구슬을 꺼낼 가능성은?", k: "h", row: 4 },
        { t: B.a.comp + 1800, s: "빨강이 ‘~일 것 같다’면 파랑은 ‘~아닐 것 같다’", row: 5 },
      ]} />
      <Caption t={t} C={C} caps={isM ? [
        { t: 300, s: "구슬 4개가 든 주머니에서 한 개를 꺼내요" },
        { t: B.a.b0, s: "빨간 구슬이 하나도 없으면 — 절대 일어나지 않는 사건" },
        { t: B.a.b1, s: "확률 = (빨간 구슬의 수) ÷ (전체 구슬의 수)" },
        { t: B.a.b4, s: "모두 빨간 구슬이면 — 반드시 일어나는 사건" },
        { t: B.a.prop, s: "확률은 0부터 1까지" },
        { t: B.a.comp, s: "빨간 구슬이 나오지 않을 확률은 1에서 빼요" },
      ] : [
        { t: 300, s: "주머니에서 구슬 한 개를 꺼내요" },
        { t: B.a.b0, s: "빨간 구슬이 하나도 없으면 꺼낼 수 없어요" },
        { t: B.a.b2, s: "빨강과 파랑이 같은 수면 — 반반" },
        { t: B.a.b4, s: "모두 빨간 구슬이면 반드시 빨강" },
        { t: B.a.prop, s: "가능성을 수로: 불가능 0, 반반 {1/2}, 확실 1" },
        { t: B.a.comp, s: "빨강이 나올 것 같으면, 파랑은 나오지 않을 것 같아요" },
      ]} />
    </g>
  );
}

export default {
  key: "chance",
  dur: B.dur,
  title: { e: "일이 일어날 가능성", m: "확률의 뜻과 성질" },
  sub: { e: "초등 · 가능성", m: "중2 · 확률" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
