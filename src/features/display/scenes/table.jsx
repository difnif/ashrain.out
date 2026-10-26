// 장면 14 — 표와 ○그래프(초등 2-2) ↔ 두 주사위의 합 · 곱의 법칙 · 확률(중2)
// 같은 흐름: 하나씩 모으기 → 나누어 세어 표로 → ○로 그래프 → 가장 많은 것 읽기.
//   초등: 16명이 좋아하는 계절 쪽지 → 표(합계) → ○ 그래프 → 봄
//   중등: 두 주사위 36가지(6 × 6) → 두 눈의 합으로 분류한 표 → ○ 그래프(산 모양) → 합 7 = {6/36} = {1/6}
import { beats, seg, win, E } from "../core";
import { Board, Caption, MText, ShapeIcon, Check, DieFace, Table } from "../draw";
import { SEASON, DICE2 } from "../facts";

const B = beats([["intro", 2400], ["collect", 5200], ["tally", 5600], ["graph", 4800], ["read", 6400], ["hold", 2600]]);
const SEASON_COL = { 봄: "coral", 여름: "leaf", 가을: "gold", 겨울: "sky" };

/* ── 초등: 쪽지 4×4 ── */
const NW = 82, NH = 56, NG = 12, NX = 116, NY = 180;
const notePos = (i) => [NX + (i % 4) * (NW + NG) + NW / 2, NY + Math.floor(i / 4) * (NH + NG) + NH / 2];
/* ── 중등: 6×6 칸 ── */
const DC = 44, DX = 150, DY = 204;                     // 칸 크기 · 첫 칸 왼쪽 위
const cellPos = (a, b) => [DX + (b - 1) * DC + DC / 2, DY + (a - 1) * DC + DC / 2];
/* ── 표(오른쪽 위) ── */
const TX = 640, TY = 170, TRH = 56;
/* ── ○ 그래프(왼쪽 아래) ── */
const GBASE = 740;

function Elem({ t, C }) {
  const { NOTES, NAMES, COUNTS } = SEASON;
  const noteT = (i) => B.a.collect + 200 + i * 300;
  const tallyT = (i) => B.a.tally + 300 + i * 300;
  const counted = (name) => NOTES.filter((n, i) => n === name && t >= tallyT(i) + 150).length;
  // ○ 그래프: 계절 차례로 아래에서 위로
  const GW = 74, GH = 40, GX = 140, ROWS = 5;
  const dots = [];
  let k = 0;
  NAMES.forEach((nm, c) => { for (let j = 0; j < COUNTS[c]; j++) dots.push({ c, j, t: B.a.graph + 300 + (k++) * 260 }); });
  const gridO = seg(t, B.a.graph, B.a.graph + 500);
  const hiCol = NAMES.indexOf(SEASON.most);
  const hi = seg(t, B.a.read + 200, B.a.read + 700);
  const sumT = B.b.tally - 400;
  return (
    <g>
      {/* 쪽지 */}
      {NOTES.map((nm, i) => {
        const [x, y] = notePos(i);
        const a = seg(t, noteT(i), noteT(i) + 300, E.back);
        if (a <= 0) return null;
        const ck = seg(t, tallyT(i), tallyT(i) + 260);
        return (
          <g key={i} transform={`translate(${x} ${y}) scale(${a}) rotate(${(i % 3 - 1) * 2})`}>
            <rect x={-NW / 2} y={-NH / 2} width={NW} height={NH} rx={6} fill={C[SEASON_COL[nm]]} fillOpacity={0.9} />
            <MText x={0} y={9} s={nm} size={26} weight={700} anchor="middle" fill={C.paper} C={C} />
            {ck > 0 && <g><circle cx={NW / 2 - 4} cy={-NH / 2 + 4} r={13} fill={C.paper} stroke={C.ink} strokeWidth={2} opacity={Math.min(1, ck * 2)} />
              <Check cx={NW / 2 - 4} cy={-NH / 2 + 4} r={9} color={C.ink} sw={3} p={ck} /></g>}
          </g>
        );
      })}
      {/* 표 */}
      <Table x={TX} y={TY} cols={[170, 100, 100, 100, 100, 110]} rh={TRH} C={C} t={t} size={30}
        o={seg(t, B.a.tally - 200, B.a.tally + 300)} rows={[
          [{ s: "계절", fill: "ink", fo: 0.08, size: 26 }, ...NAMES.map((n) => ({ s: n, color: SEASON_COL[n], weight: 700 })), { s: "합계", fill: "ink", fo: 0.08, size: 26 }],
          [{ s: "학생 수(명)", fill: "ink", fo: 0.08, size: 24 }, ...NAMES.map((n, c) => ({ s: counted(n) ? String(counted(n)) : "", hi: c === hiCol ? B.a.read + 200 : undefined })),
            { s: String(SEASON.TOTAL), t: sumT, color: "gold", weight: 800 }],
        ]} />
      {/* ○ 그래프 */}
      <g opacity={gridO}>
        {Array.from({ length: ROWS }, (_, r) => NAMES.map((_, c) => (
          <rect key={`${r}-${c}`} x={GX + c * GW} y={GBASE - (r + 1) * GH} width={GW} height={GH} fill="none" stroke={C.faint} strokeWidth={1.4} />
        )))}
        {NAMES.map((n, c) => <MText key={n} x={GX + c * GW + GW / 2} y={GBASE + 32} s={n} size={26} weight={700} anchor="middle"
          fill={c === hiCol && hi > 0 ? C.gold : C.ink} C={C} />)}
        {hi > 0 && <rect x={GX + hiCol * GW + 3} y={GBASE - ROWS * GH + 3} width={GW - 6} height={ROWS * GH - 6} rx={8} fill="none" stroke={C.gold} strokeWidth={4} opacity={hi} />}
      </g>
      {dots.map((d, i) => {
        const a = seg(t, d.t, d.t + 260, E.back);
        return a > 0 && <ShapeIcon key={i} kind="circle" cx={GX + d.c * GW + GW / 2} cy={GBASE - d.j * GH - GH / 2} r={15 * a}
          stroke={C[SEASON_COL[NAMES[d.c]]]} sw={4} C={C} />;
      })}
      <Board x={680} y={372} t={t} C={C} size={34} lh={58} lines={[
        { t: B.a.tally + 200, s: "표로 나타내기", k: "h" },
        { t: sumT, s: SEASON.sumLine },
        { t: B.a.graph + 200, s: "⟪○⟫를 이용한 그래프", k: "h" },
        { t: B.a.read + 300, s: SEASON.mostLine },
        { t: B.a.read + 2000, s: "표 : 전체 수를 알아보기 편리해요" },
        { t: B.a.read + 3600, s: "그래프 : 많고 적음을 한눈에 비교해요" },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: "우리 반 16명이 좋아하는 계절을 조사했어요" },
        { t: B.a.collect, s: "한 명씩 붙임쪽지를 붙여요" },
        { t: B.a.tally, s: "계절별로 하나씩 표시하며 세어 표로 나타내요" },
        { t: B.a.graph, s: "표를 보고 ⟪○⟫로 그래프를 그려요" },
        { t: B.a.read, s: `가장 많은 학생이 좋아하는 계절은 ${SEASON.most}` },
      ]} />
    </g>
  );
}

function Mid({ t, C }) {
  const { CELLS, SUMS, BY_SUM } = DICE2;
  const cellT = (i) => B.a.collect + 200 + i * 130;
  const sumT = (s) => B.a.tally + 300 + (s - 2) * 460;
  const GW = 44, GH = 36, GX = 120, ROWS = 6;
  const order = [];
  SUMS.forEach((s) => CELLS.forEach((c, i) => { if (c.s === s) order.push({ i, s }); }));
  const dotT = {}; order.forEach((o, k) => (dotT[o.i] = B.a.graph + 300 + k * 115));
  const rowOfSum = {}; const cnt = {};
  order.forEach(({ i, s }) => { cnt[s] = (cnt[s] || 0); rowOfSum[i] = cnt[s]++; });
  const gridO = seg(t, B.a.graph, B.a.graph + 500);
  const hi = seg(t, B.a.read + 200, B.a.read + 700);
  const hdr = seg(t, 300, 1200);
  return (
    <g>
      {/* 머리: A의 눈(행) · B의 눈(열) */}
      <g opacity={hdr}>
        <MText x={DX - 22} y={DY - 14} s="+" size={30} weight={800} anchor="middle" fill={C.soft} C={C} />
        {[1, 2, 3, 4, 5, 6].map((n) => <DieFace key={"b" + n} cx={DX + (n - 1) * DC + DC / 2} cy={DY - 24} s={32} n={n} C={C} />)}
        {[1, 2, 3, 4, 5, 6].map((n) => <DieFace key={"a" + n} cx={DX - 24} cy={DY + (n - 1) * DC + DC / 2} s={32} n={n} C={C} />)}
        <MText x={DX + 3 * DC} y={DY - 52} s="B의 눈" size={24} weight={700} anchor="middle" fill={C.soft} C={C} />
        <MText x={DX - 50} y={DY + 3 * DC + 8} s="A" size={26} weight={700} anchor="end" fill={C.soft} C={C} />
        <rect x={DX} y={DY} width={6 * DC} height={6 * DC} fill="none" stroke={C.soft} strokeWidth={2.4} />
      </g>
      {CELLS.map((c, i) => {
        const [x, y] = cellPos(c.a, c.b);
        const a = seg(t, cellT(i), cellT(i) + 220);
        if (a <= 0) return null;
        const flash = win(t, sumT(c.s), sumT(c.s) + 700, 120, 300);
        const is7 = c.s === 7 && hi > 0;
        return (
          <g key={i} opacity={a}>
            <rect x={x - DC / 2} y={y - DC / 2} width={DC} height={DC} fill={C.gold} fillOpacity={0.12 + 0.4 * Math.max(flash, is7 ? hi : 0)}
              stroke={C.faint} strokeWidth={1.2} />
            <MText x={x} y={y + 9} s={String(c.s)} size={24} weight={is7 ? 800 : 600} anchor="middle" fill={is7 ? C.gold : C.ink} C={C} />
          </g>
        );
      })}
      {/* 표 */}
      <Table x={TX} y={TY} cols={[124, ...SUMS.map(() => 50)]} rh={TRH} C={C} t={t} size={26}
        o={seg(t, B.a.tally - 200, B.a.tally + 300)} rows={[
          [{ s: "두 눈의 합", fill: "ink", fo: 0.08, size: 22 }, ...SUMS.map((s) => ({ s: String(s), weight: 700, color: s === 7 && hi > 0 ? "gold" : undefined }))],
          [{ s: "경우의 수", fill: "ink", fo: 0.08, size: 22 }, ...SUMS.map((s, k) => ({ s: String(BY_SUM[k]), t: sumT(s) + 200, hi: s === 7 ? B.a.read + 200 : undefined }))],
        ]} />
      {/* ○ 그래프 */}
      <g opacity={gridO}>
        {Array.from({ length: ROWS }, (_, r) => SUMS.map((_, c) => (
          <rect key={`${r}-${c}`} x={GX + c * GW} y={GBASE - (r + 1) * GH} width={GW} height={GH} fill="none" stroke={C.faint} strokeWidth={1.2} />
        )))}
        {SUMS.map((s, c) => <MText key={s} x={GX + c * GW + GW / 2} y={GBASE + 30} s={String(s)} size={24} weight={700} anchor="middle"
          fill={s === 7 && hi > 0 ? C.gold : C.ink} C={C} />)}
        {hi > 0 && <rect x={GX + 5 * GW + 2} y={GBASE - ROWS * GH + 2} width={GW - 4} height={ROWS * GH - 4} rx={8} fill="none" stroke={C.gold} strokeWidth={4} opacity={hi} />}
      </g>
      {CELLS.map((c, i) => {
        const a = seg(t, dotT[i], dotT[i] + 240, E.back);
        return a > 0 && <ShapeIcon key={i} kind="circle" cx={GX + (c.s - 2) * GW + GW / 2} cy={GBASE - rowOfSum[i] * GH - GH / 2} r={12 * a}
          stroke={c.s === 7 && hi > 0 ? C.gold : C.sky} sw={3.6} C={C} />;
      })}
      <Board x={680} y={372} t={t} C={C} size={34} lh={58} lines={[
        { t: B.a.collect + 200, s: "두 주사위를 동시에 던질 때 — 곱의 법칙", k: "h" },
        { t: B.b.collect - 500, s: DICE2.mulLine },
        { t: B.a.tally + 200, s: "두 눈의 수의 합으로 분류", k: "h" },
        { t: B.a.read + 300, s: DICE2.n7Line },
        { t: B.a.read + 1800, s: DICE2.p7Line },
        { t: B.a.read + 3600, s: DICE2.bestLine },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: "두 주사위 A, B를 동시에 던져요" },
        { t: B.a.collect, s: "A의 눈 6가지 × B의 눈 6가지 = 36가지" },
        { t: B.a.tally, s: "두 눈의 수의 합으로 나누어 세어 표로 나타내요" },
        { t: B.a.graph, s: "⟪○⟫로 그래프를 그리면 합 7이 가장 많아요" },
        { t: B.a.read, s: "합이 7일 확률은 {6/36} = {1/6}" },
      ]} />
    </g>
  );
}

export default {
  key: "table",
  dur: B.dur,
  title: { e: "표와 그래프", m: "두 주사위의 합과 확률" },
  sub: { e: "초등 · 표와 그래프", m: "중2 · 곱의 법칙과 확률" },
  render: (mode, t, C) => (mode === "m" ? <Mid t={t} C={C} /> : <Elem t={t} C={C} />),
};
