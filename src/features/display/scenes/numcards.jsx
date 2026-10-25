// 장면 15 — 수 카드로 두 자리 수 만들기(초등 · 분류해서 빠짐없이) ↔ 자연수 만들기의 경우의 수(중2)
// 같은 4×4 표(십의 자리 × 일의 자리)를 두 판이 함께 쓴다 — 지울 칸을 지우고, 남은 칸에 수를 채운다.
//   초등: 십의 자리에 0 ×, 같은 카드 × → 십의 자리끼리 나누어 세기 → 9개 · 가장 큰 수/작은 수
//   중등: 규칙 파악(포지티브 · 네거티브) → 전략(십의 자리부터) → 식 3 × 3 = 9 · 세 자리면 3 × 3 × 2 = 18
import { beats, seg, win, E, lerp } from "../core";
import { Board, Caption, MText, Table } from "../draw";
import { NUMCARDS } from "../facts";

const { DIGITS, GRID } = NUMCARDS;
const B = beats([["intro", 2400], ["rule", 4200], ["grid", 2400], ["cross", 4400], ["fill", 4200], ["count", 4600], ["extra", 5800], ["hold", 2600]]);
const KW = 90, KH = 118, KY = 236, KX = (i) => 160 + i * 112;
const TX = 110, TY = 362, COLS = [120, 96, 96, 96, 96], RH = [48, 70, 70, 70, 70];
const rowY = (d) => TY + RH[0] + d * 70 + 35;                       // 십의 자리 d 행의 가운데

const crossT = (c) => (c.zero ? B.a.cross + 300 + c.o * 200 : c.same ? B.a.cross + 2300 + (c.t - 1) * 250 : null);
const OKS = GRID.flat().filter((c) => c.ok);
const fillT = (c) => B.a.fill + 300 + OKS.indexOf(c) * 360;

function NumCard({ x, y, d, C, o = 1, ring, tag, sc = 1 }) {
  return (
    <g transform={`translate(${x} ${y})${sc !== 1 ? ` scale(${sc})` : ""}`} opacity={o}>
      <rect x={-KW / 2} y={-KH / 2} width={KW} height={KH} rx={12} fill={C.card} stroke={C.cardEdge} strokeWidth={2.6} />
      <MText x={0} y={22} s={String(d)} size={64} weight={800} anchor="middle" fill={C.ink} C={C} />
      {ring && ring.o > 0 && <rect x={-KW / 2 - 5} y={-KH / 2 - 5} width={KW + 10} height={KH + 10} rx={15} fill="none" stroke={C[ring.col]} strokeWidth={4.5} opacity={ring.o} />}
      {tag > 0 && <g opacity={tag}>
        <rect x={-58} y={-KH / 2 - 46} width={116} height={34} rx={17} fill={C.coral} />
        <MText x={0} y={-KH / 2 - 21} s="십의 자리 ×" size={20} weight={700} anchor="middle" fill={C.paper} C={C} />
      </g>}
    </g>
  );
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const T = isM ? NUMCARDS.M : NUMCARDS.E;
  const cardsO = seg(t, 200, 1200) * (isM ? 1 - seg(t, B.a.extra, B.a.extra + 600) : 1);
  // 1·3 두 장이 모여 "13" — 두 자리 수를 만드는 모습
  const pair = win(t, B.a.rule + 600, B.a.rule + 3600, 700, 700);
  const posRing = isM ? win(t, B.a.rule + 700, B.a.grid + 600, 300, 400) : 0;
  const zeroTag = isM ? win(t, B.a.rule + 2800, B.b.cross, 300, 400) : 0;
  const tableO = seg(t, B.a.grid, B.a.grid + 700);
  const hiMax = !isM ? B.a.extra + 400 : undefined, hiMin = !isM ? B.a.extra + 1000 : undefined;
  const rows = [
    [{ s: "", fill: "ink", fo: 0.08 }, ...DIGITS.map((d) => ({ s: String(d), weight: 800, fill: "ink", fo: 0.08 }))],
    ...DIGITS.map((d) => [
      { s: String(d), weight: 800, fill: "ink", fo: 0.08, color: d === 0 ? "coral" : undefined },
      ...DIGITS.map((o) => {
        const c = GRID[d][o];
        if (!c.ok) return { s: "", cross: crossT(c), fill: c.zero || c.same ? "coral" : undefined, fo: 0.08, fillT: crossT(c) };
        return { s: String(c.v), t: fillT(c), size: 32, weight: 700,
          hi: c.v === NUMCARDS.max ? hiMax : c.v === NUMCARDS.min ? hiMin : undefined, hiCol: c.v === NUMCARDS.min ? "teal" : "gold" };
      }),
    ]),
  ];
  const rowCnt = (d) => seg(t, B.a.count + 300 + (d - 1) * 500, B.a.count + 700 + (d - 1) * 500);
  // 중등: 세 자리 — 자리 세 칸
  const slots = isM ? seg(t, B.a.extra + 500, B.a.extra + 1200) : 0;
  const SLOT = [["백", NUMCARDS.tens], ["십", NUMCARDS.ones], ["일", NUMCARDS.ones - 1]];
  return (
    <g>
      {/* 수 카드 — 고른 두 장(1·3)에 금빛 테, 옆에 만든 수 "13" */}
      {DIGITS.map((d, i) => {
        const inPair = d === 1 || d === 3;
        const ring = inPair && pair > posRing ? { col: "gold", o: pair } : posRing > 0 ? { col: "teal", o: posRing } : null;
        return <NumCard key={d} x={KX(i)} y={KY} d={d} C={C} o={cardsO * (inPair ? 1 : 1 - 0.45 * pair)}
          ring={ring} tag={d === 0 ? zeroTag : 0} />;
      })}
      {pair > 0.01 && <g opacity={pair * cardsO}>
        <MText x={600} y={KY + 16} s="→" size={44} weight={700} anchor="middle" fill={C.gold} C={C} />
        <NumCard x={lerp(560, 668, pair)} y={KY} d={1} C={C} sc={0.8} />
        <NumCard x={lerp(560, 744, pair)} y={KY} d={3} C={C} sc={0.8} />
      </g>}
      {/* 세 자리 정수(중등) */}
      {slots > 0 && <g opacity={slots}>
        {SLOT.map(([nm, n], i) => {
          const x = 170 + i * 150;
          const a = seg(t, B.a.extra + 900 + i * 500, B.a.extra + 1300 + i * 500);
          return <g key={nm}>
            <MText x={x} y={KY - 82} s={`${nm}의 자리`} size={24} weight={700} anchor="middle" fill={C.soft} C={C} />
            <rect x={x - 48} y={KY - 64} width={96} height={96} rx={12} fill="none" stroke={C.ink} strokeWidth={3} strokeDasharray="10 8" />
            <MText x={x} y={KY + 2} s={`${n}`} size={52} weight={800} anchor="middle" fill={C.gold} opacity={a} C={C} />
            <MText x={x} y={KY + 64} s={i === 0 ? "0 빼고" : i === 1 ? "남은 카드" : "또 남은 카드"} size={22} weight={600} anchor="middle"
              fill={C.soft} opacity={a} C={C} />
            {i < 2 && <MText x={x + 75} y={KY + 2} s="×" size={44} weight={700} anchor="middle" fill={C.ink} opacity={a} C={C} />}
          </g>;
        })}
      </g>}
      {/* 표 */}
      <MText x={TX + COLS[0] + 192} y={TY - 14} s="일의 자리" size={24} weight={700} anchor="middle" fill={C.soft} opacity={tableO} C={C} />
      <Table x={TX} y={TY} cols={COLS} rh={RH} rows={rows} C={C} t={t} size={30} o={tableO} />
      {/* 모서리 칸: 대각선 + 십·일 */}
      <g opacity={tableO}>
        <line x1={TX} y1={TY} x2={TX + COLS[0]} y2={TY + RH[0]} stroke={C.soft} strokeWidth={1.6} />
        <MText x={TX + 12} y={TY + RH[0] - 8} s="십" size={20} weight={700} fill={C.soft} C={C} />
        <MText x={TX + COLS[0] - 12} y={TY + 22} s="일" size={20} weight={700} anchor="end" fill={C.soft} C={C} />
      </g>
      {/* 행마다 개수(십의 자리로 분류) */}
      {[1, 2, 3].map((d) => rowCnt(d) > 0 && (
        <MText key={d} x={TX + COLS.reduce((a, b) => a + b, 0) + 22} y={rowY(d) + 11} s={isM ? "3가지" : "3개"} size={30} weight={800}
          fill={C.gold} opacity={rowCnt(d)} C={C} />
      ))}
      {rowCnt(1) > 0 && <MText x={TX + COLS.reduce((a, b) => a + b, 0) + 22} y={rowY(0) + 11} s={isM ? "×" : "0개"} size={30} weight={800}
        fill={C.coral} opacity={rowCnt(1)} C={C} />}
      <Board x={820} y={232} t={t} C={C} size={34} lh={isM ? 56 : 62} lines={isM ? [
        { t: B.a.rule + 200, s: "규칙 파악", k: "h" },
        { t: B.a.rule + 700, s: T.pos, dot: "teal" },
        { t: B.a.rule + 1800, s: T.neg1, dot: "coral" },
        { t: B.a.rule + 2800, s: T.neg2, dot: "coral" },
        { t: B.a.fill + 200, s: "전략 → 식 세우기", k: "h" },
        { t: B.a.fill + 900, s: T.strat },
        { t: B.a.count + 1900, s: T.two },
        { t: B.a.extra + 2600, s: T.three },
      ] : [
        { t: B.a.rule + 200, s: "수 카드 2장으로 두 자리 수", k: "h" },
        { t: B.a.cross + 300, s: "십의 자리에 0은 올 수 없어요", dot: "coral" },
        { t: B.a.cross + 2300, s: "같은 카드는 한 번만 써요", dot: "coral" },
        { t: B.a.fill + 200, s: "십의 자리로 나누어 세기", k: "h" },
        { t: B.a.count + 1900, s: T.count },
        { t: B.a.extra + 1500, s: T.maxmin },
      ]} />
      <Caption t={t} C={C} caps={isM ? [
        { t: 300, s: "0, 1, 2, 3 카드 중 2장으로 두 자리 정수를 만들어요" },
        { t: B.a.rule, s: "먼저 규칙 파악 — 해도 되는 것과 안 되는 것" },
        { t: B.a.grid, s: "표로 모든 짝을 펼쳐 보면" },
        { t: B.a.cross, s: "네거티브 규칙에 걸리는 칸을 지워요" },
        { t: B.a.fill, s: "전략: 십의 자리부터 정해요" },
        { t: B.a.count, s: "십의 자리 3가지 × 일의 자리 3가지 = 9" },
        { t: B.a.extra, s: "세 자리 정수는? 3 × 3 × 2 = 18" },
      ] : [
        { t: 300, s: "수 카드 0, 1, 2, 3" },
        { t: B.a.rule, s: "2장을 골라 두 자리 수를 만들어요" },
        { t: B.a.grid, s: "표로 정리하면 빠짐없이 셀 수 있어요" },
        { t: B.a.cross, s: "십의 자리에 0이 오면 두 자리 수가 아니에요" },
        { t: B.a.cross + 2000, s: "같은 카드는 두 번 쓸 수 없어요" },
        { t: B.a.fill, s: "십의 자리가 같은 수끼리 모아요" },
        { t: B.a.count, s: "모두 9개" },
        { t: B.a.extra, s: `가장 큰 수는 ${NUMCARDS.max}, 가장 작은 수는 ${NUMCARDS.min}` },
      ]} />
    </g>
  );
}

export default {
  key: "numcards",
  dur: B.dur,
  title: { e: "수 카드로 수 만들기", m: "자연수 만들기의 경우의 수" },
  sub: { e: "초등 · 빠짐없이 세기", m: "중2 · 경우의 수" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
