// 축구 2 — 루크 쇼 프리킥 → 카세미루 헤더 (2023-02-26 리그컵 결승 맨유 2−0 뉴캐슬, 33분)
// 골대 가운데 G, 프리킥 F(옆 26 · 앞 23), 헤더 H(옆 6 · 앞 8). 두 기록표(가상의 자료)에서 거리의 칸을 찾는다.
//   초등: 줄자 25 m · 10 m → 표에서 칸 찾기(10은 ‘10 이상’) → 100번 찬다고 생각하기: 머리에 40번 → 골 4번
//   중등: FH² = 20² + 15², HG² = 6² + 8² → 계급의 상대도수 {2/5}, {1/10} → 곱 {1/25}
import { beats, seg, win, E, mix2 } from "../core";
import { Path, RightMark } from "../draw";
import { UText, UBoard, UCaption, UTable, RowHi, Tape, SegLbl, IconGrid } from "../kit-story";
import { mapper, Grass, PLines, boxLines, Goal, Player, Rival, Ball, GoalFlash, DirNote } from "../kit-soccer";
import { SETPIECE as S, who } from "../facts-soccer";

const B = beats([["intro", 2400], ["kick", 3600], ["dist", 6400], ["table", 7200], ["freq", 8800], ["hold", 2600]]);
const MP = mapper({ ox: 312, oy: 214, s: 11 });
const GR = [-22, -3, 30, 26];
const G = MP.p(S.G), F = MP.p(S.F), H = MP.p(S.H), NET = MP.p([0.6, -1.5]);
const Q1 = MP.p([S.H[0], S.F[1]]), Q2 = MP.p([S.H[0], 0]);          // 직각의 꼭짓점(FH · HG)
// 회색 = 뉴캐슬, 옅은 빨강 = 맨유(그날 선발). 골키퍼는 카리우스 — 나머지 자리는 명단으로 짐작
const RIVALS = [[[-5, 6.5], "보트만", "l"], [[-9.5, 3.4], "번", "l"], [[10.6, 4.0], "셰어", "r"], [[-2.6, 12.6], "조엘린통", "b"], [[16.6, 9.4], "트리피어", "r"]]
  .map(([q, nm, lp]) => ({ p: MP.p(q), id: who("cup2023Newcastle", nm), lp }));
const MATES = [[[-12, 10], "바란", "l"], [[21, 6.5], "마르티네스", "r"]].map(([q, nm, lp]) => ({ p: MP.p(q), id: who("cup2023United", nm), lp }));
const KEEPER = { p: MP.p([-2.2, 0.9]), id: who("cup2023Newcastle", "카리우스"), lp: "l" };

const KA = B.a.kick + 300, KB = KA + 1500, KC = KB + 650, KD = KC + 300;
function ballAt(t) {
  if (t < KA) return { p: F, h: 0 };
  if (t < KB) { const k = seg(t, KA, KB, E.lin); return { p: mix2(F, H, k), h: 1.1 * 4 * k * (1 - k) + 0.4 * k }; }
  if (t < KC) { const k = seg(t, KB, KC, E.lin); return { p: mix2(H, G, k), h: 0.4 * (1 - k) }; }
  return { p: mix2(G, NET, seg(t, KC, KD, E.out)), h: 0 };
}

/* 표 */
const TX = 668, TCOL = [178, 82, 104], TRH = [42, 40, 40, 40], TY1 = 196;
const HCOL = [178, 82, 104], HRH = [42, 40, 40, 40, 40], TY2 = 410;
const rowsOf = (tab, head, fromT, t, hiRow) => [
  head.map((h) => ({ s: h, size: 19, weight: 750, fill: "ink", fo: 0.08 })),
  ...tab.map((r, i) => [
    { s: S.range(r), size: 19, weight: i === hiRow ? 800 : 600, color: i === hiRow ? "gold" : undefined },
    { s: String(r[2]), size: 22, t: fromT + i * 120 },
    { s: String(r[3]), size: 22, t: fromT + i * 120, weight: i === hiRow ? 800 : 600, color: i === hiRow ? "gold" : undefined },
  ]),
];

/* 점 그림 100 */
const GX = 92, GY = 536, GSTEP = 25;

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const pitchO = seg(t, 0, 700), playersO = seg(t, 400, 1200);
  const ball = ballAt(t);
  const flash = win(t, KC, B.b.kick + 300, 120, 600);
  const jump = win(t, KB - 260, KB + 260, 200, 260);
  const trail = seg(t, KB, KB + 500);
  const dist1 = seg(t, B.a.dist + 200, B.a.dist + 1400, E.io), dist2 = seg(t, B.a.dist + 2600, B.a.dist + 3500, E.io);
  const tabO = seg(t, B.a.table, B.a.table + 600);
  const hi1 = seg(t, B.a.table + 900, B.a.table + 1400), hi2 = seg(t, B.a.table + 2400, B.a.table + 2900);
  const gridO = seg(t, B.a.freq, B.a.freq + 600);
  const head = (k) => seg(t, B.a.freq + 1000 + Math.floor(k / 10) * 260, B.a.freq + 1300 + Math.floor(k / 10) * 260);
  const goal = (k) => seg(t, B.a.freq + 3600 + (k / 10) * 280, B.a.freq + 3900 + (k / 10) * 280);
  return (
    <g>
      {/* 경기장 */}
      <g opacity={pitchO}>
        <Grass M={MP} rect={GR} C={C} band={4} along="y" />
        <DirNote x={MP.p([GR[0], 0])[0] + 2} y={MP.p([0, GR[1]])[1] - 12} s="위치는 실제 장면을 바탕으로 다듬은 값 · 흐린 선수는 그날 선발, 자리는 짐작" anchor="start" size={18} C={C} />
        <Goal M={MP} C={C} cx={0} dir={-1} />
        <PLines M={MP} C={C} lines={[[[-22, 0], [30, 0]], ...boxLines(0)]} clip={GR} w={2.2} />
      </g>
      {trail > 0 && <g opacity={trail * 0.75}>
        <Path pts={[F, H]} stroke={C.ink} sw={3} dash={isM ? undefined : "10 9"} />
        {t > KC && <Path pts={[H, G]} stroke={C.ink} sw={3} dash={isM ? undefined : "10 9"} />}
      </g>}
      {/* 중등: 옆 · 앞 거리 */}
      {isM && dist1 > 0 && <g opacity={dist1}>
        <Path pts={[F, Q1, H]} stroke={C.gold} sw={2.6} dash="8 7" />
        <RightMark V={Q1} A={F} B={H} s={13} C={C} color={C.gold} />
        <SegLbl P={F} Q={Q1} s={S.M.lab.dx} side={-1} off={18} C={C} size={26} fill={C.gold} />
        <SegLbl P={Q1} Q={H} s={S.M.lab.dy} side={-1} off={20} C={C} size={26} fill={C.gold} />
      </g>}
      {isM && dist2 > 0 && <g opacity={dist2}>
        <Path pts={[H, Q2, G]} stroke={C.teal} sw={2.6} dash="8 7" />
        <RightMark V={Q2} A={H} B={G} s={11} C={C} color={C.teal} />
        <SegLbl P={H} Q={Q2} s={S.M.lab.hy} side={-1} off={16} C={C} size={24} fill={C.teal} />
        <SegLbl P={Q2} Q={G} s={S.M.lab.hx} side={-1} off={16} C={C} size={24} fill={C.teal} />
      </g>}
      {/* 선수 */}
      {RIVALS.map((q, i) => <Rival key={i} x={q.p[0]} y={q.p[1]} C={C} o={playersO} r={14} n={q.id[0]} name={q.id[1]} lp={q.lp} lsize={14} />)}
      <Rival x={KEEPER.p[0]} y={KEEPER.p[1]} C={C} o={playersO} r={13} n={KEEPER.id[0]} name={KEEPER.id[1]} lp={KEEPER.lp} lsize={14} />
      {MATES.map((q, i) => <Player key={i} x={q.p[0]} y={q.p[1]} team="united" C={C} o={playersO * 0.7} r={14} n={q.id[0]} label={q.id[1]} lp={q.lp} lsize={14} faint />)}
      <Player x={F[0]} y={F[1]} n={23} team="united" C={C} o={playersO} r={19} label="루크 쇼" lp="b" lsize={20} />
      <Player x={H[0]} y={H[1]} n={18} team="united" C={C} o={playersO} r={19 + 3 * jump} ring={jump} label="카세미루" lp="l" lsize={20} />
      <Ball x={ball.p[0]} y={ball.p[1]} h={ball.h} r={9} C={C} o={playersO} />
      <GoalFlash x={G[0] + 120} y={G[1] - 6} k={flash} C={C} />
      {/* 초등: 줄자 */}
      {!isM && <Tape a={F} b={H} p={dist1} pxPerM={MP.s} C={C} read={S.E.tapeFH} side={1} rs={22} w={11} />}
      {!isM && <Tape a={H} b={G} p={dist2} pxPerM={MP.s} C={C} read={S.E.tapeHG} side={-1} rs={22} w={11} />}
      {/* 중등: 길이 */}
      {isM && <SegLbl P={F} Q={H} s="25 m" side={1} off={26} C={C} size={26} o={seg(t, B.a.dist + 2000, B.a.dist + 2500)} />}

      {/* 기록표(가상의 자료) */}
      <g opacity={tabO}>
        <UText x={TX} y={TY1 - 12} s="프리킥 크로스 기록 (가상의 자료)" size={20} weight={700} fill={C.soft} C={C} />
        <RowHi x={TX} y={TY1} cols={TCOL} rh={TRH} r={1 + S.ci} C={C} o={hi1} />
        <UTable x={TX} y={TY1} cols={TCOL} rh={TRH} C={C} t={t} rows={rowsOf(S.CROSS, ["F → H (m)", "크로스", "머리에 닿음"], B.a.table + 100, t, hi1 > 0 ? S.ci : -1)} />
        <UText x={TX} y={TY2 - 12} s="헤더 기록 (가상의 자료)" size={20} weight={700} fill={C.soft} C={C} />
        <RowHi x={TX} y={TY2} cols={HCOL} rh={HRH} r={1 + S.hi} C={C} o={hi2} col="teal" />
        <UTable x={TX} y={TY2} cols={HCOL} rh={HRH} C={C} t={t} rows={rowsOf(S.HEAD, ["H → G (m)", "헤더", "골"], B.a.table + 300, t, hi2 > 0 ? S.hi : -1)} />
      </g>

      {/* 100번 찬다고 생각하기 */}
      {gridO > 0 && <g opacity={gridO}>
        <IconGrid x={GX} y={GY} cols={10} rows={10} step={GSTEP} r={8.5} C={C} paint={(k) => {
          const g = k < S.nHead ? goal(k) : 0;
          const hd = k < S.nHead ? head(k) : 0;
          if (k % 10 === 0 && g > 0 && Math.floor(k / 10) < S.nGoal) return { fill: C.gold, stroke: C.gold, scale: 1.1 + 0.25 * (1 - g) };
          if (hd > 0) return { fill: isM ? C.teal : C.sky, fo: 0.35 + 0.55 * hd, stroke: isM ? C.teal : C.sky };
          return { stroke: C.soft, o: 0.75 };
        }} />
        <Legend t={t} C={C} isM={isM} />
      </g>}

      <UBoard x={1070} y={232} t={t} C={C} size={28} lh={52} lines={isM ? [
        { t: B.a.dist + 1500, s: S.M.fh },
        { t: B.a.dist + 3600, s: S.M.hg },
        { t: B.a.table + 1400, s: S.M.p1 },
        { t: B.a.table + 2900, s: S.M.p2 },
        { t: B.a.table + 4200, s: S.M.edge, c: "soft" },
        { t: B.a.freq + 4200, s: S.M.prod },
      ] : [
        { t: B.a.dist + 1400, s: S.E.fh },
        { t: B.a.dist + 3500, s: S.E.hg },
        { t: B.a.table + 1400, s: S.E.cls1 },
        { t: B.a.table + 2900, s: S.E.cls2 },
        { t: B.a.table + 4200, s: S.E.edge, c: "soft" },
        { t: B.a.freq + 2400, s: S.E.n1 },
        { t: B.a.freq + 4600, s: S.E.n2 },
        { t: B.a.freq + 6400, s: S.E.n3 },
      ]} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: "2023년 2월 26일 리그컵 결승 — 맨유 2−0 뉴캐슬" },
        { t: B.a.kick, s: "전반 33분, 루크 쇼의 프리킥을 카세미루가 헤더로 넣었어요" },
        ...(isM ? [
          { t: B.a.dist, s: "옆 · 앞으로 떨어진 거리로 직각삼각형 — 피타고라스 정리" },
          { t: B.a.table, s: "거리가 속한 계급의 상대도수를 확률로 써요" },
          { t: B.a.table + 4000, s: `HG = ${S.HG} m는 경계값 — ‘${S.HEAD[S.hi][0]} 이상 ${S.HEAD[S.hi][1]} 미만’ 계급` },
          { t: B.a.freq, s: "머리에 닿고, 그 헤더가 골이 되어야 하니 두 확률을 곱해요" },
          { t: B.a.freq + 5200, s: `${S.M.prod} — ${S.N}번 중 ${S.nGoal}번꼴` },
        ] : [
          { t: B.a.dist, s: "프리킥과 헤더의 거리를 줄자로 재요" },
          { t: B.a.table, s: "기록표에서 그 거리가 들어가는 칸을 찾아요" },
          { t: B.a.table + 4000, s: `${S.HG} m는 ‘${S.HEAD[S.hi][0]} 이상 ${S.HEAD[S.hi][1]} 미만’ 칸 — 이상은 그 수를 포함해요` },
          { t: B.a.freq, s: `이런 프리킥을 ${S.N}번 찬다고 생각해 봐요` },
          { t: B.a.freq + 5600, s: `${S.N}번 중 ${S.nGoal}번쯤 골 — ${S.N / S.nGoal}번에 1번꼴이에요` },
        ]),
      ]} />
    </g>
  );
}

/** 점 그림 옆 설명 */
function Legend({ t, C, isM }) {
  const x = GX + 10 * GSTEP + 34;
  const rows = isM
    ? [[B.a.freq + 400, S.M.grid[0] + "번", C.soft, "none"], [B.a.freq + 2400, S.M.grid[1], C.teal, C.teal], [B.a.freq + 4600, S.M.grid[2], C.gold, C.gold]]
    : [[B.a.freq + 400, "프리킥 " + S.E.grid[0], C.soft, "none"], [B.a.freq + 2400, S.E.grid[1], C.sky, C.sky], [B.a.freq + 4600, S.E.grid[2], C.gold, C.gold]];
  return (
    <g>
      {rows.map(([t0, s, col, fill], i) => {
        const a = seg(t, t0, t0 + 400);
        return a > 0 && <g key={i} opacity={a}>
          <circle cx={x + 10} cy={GY + 44 + i * 78} r={10} fill={fill} stroke={col} strokeWidth={2.4} />
          <UText x={x + 32} y={GY + 54 + i * 78} s={s} size={28} weight={700} fill={i ? col : C.ink} C={C} />
        </g>;
      })}
    </g>
  );
}

export default {
  key: "soc-setpiece",
  dur: B.dur,
  title: { e: "프리킥이 골이 될 가능성", m: "프리킥이 골이 될 확률" },
  sub: { e: "초등 · 100번으로 생각하기 · 2023 리그컵 결승", m: "중2 · 상대도수와 확률의 곱 · 2023 리그컵 결승" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
