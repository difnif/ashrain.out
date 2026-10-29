// 축구 6 — 맨시티 vs 첼시: 적어도 한 골 (기대 득점 xG)
// 골대 가운데 O, 슈팅한 곳 S1(옆 3 · 앞 4) · S2(옆 8 · 앞 6) · S3(옆 16 · 앞 12). 슈팅 기록표는 가상의 자료.
//   초등: 줄자 5 · 10 · 20 m → 표에서 4번에 1번 · 8번에 1번 · 25번에 1번 → 800경기로 생각하기 800 → 600 → 525 → 504 → 296경기 = 100경기마다 37경기
//   중등: 피타고라스 5 · 10 · 20 → 계급의 골 상대도수 {1/4} · {1/8} · {1/25} → 1 − {3/4} × {7/8} × {24/25} = {37/100}
import { beats, seg, win, E, mix2 } from "../core";
import { Path, RightMark } from "../draw";
import { UText, UBoard, UCaption, UTable, RowHi, Tape, SegLbl, Chain, chainW, uWidth } from "../kit-story";
import { mapper, Grass, PLines, boxLines, Goal, Player, Ball } from "../kit-soccer";
import { XG } from "../facts-soccer";

const B = beats([["intro", 2400], ["shots", 4800], ["dist", 6600], ["table", 6800], ["chain", 9000], ["hold", 2600]]);
const MP = mapper({ ox: 352, oy: 209, s: 13 });
const GR = [-22, -3, 22, 18];
const O = MP.p([0, 0]);
const SP = XG.SHOTS.map(MP.p);
const TX = 676, TY = 204, TCOL = [170, 76, 76], TRH = [42, 42, 42, 42];
const SHOT_T = [B.a.shots + 300, B.a.shots + 1700, B.a.shots + 3100];
const MISS = [[4.6, -0.6], [-2.6, -0.4], [2.2, -0.2]].map(MP.p);   // 슈팅이 향한 곳(그림만)

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const pitchO = seg(t, 0, 700), playersO = seg(t, 400, 1200);
  const tabO = seg(t, B.a.table, B.a.table + 600);
  const rowHi = (i) => seg(t, B.a.table + 800 + i * 1500, B.a.table + 1300 + i * 1500);
  const rows = [
    ["골대 가운데에서 (m)", "슈팅", "골"].map((h) => ({ s: h, size: 18, weight: 750, fill: "ink", fo: 0.08 })),
    ...XG.TAB.map((r, i) => [
      { s: `${r[0]} 이상 ~ ${r[1]} 미만`, size: 20, weight: rowHi(i) > 0 ? 800 : 600, color: rowHi(i) > 0 ? "gold" : undefined },
      { s: String(r[2]), size: 22, t: B.a.table + 200 + i * 120 },
      { s: String(r[3]), size: 22, t: B.a.table + 200 + i * 120, weight: rowHi(i) > 0 ? 800 : 600, color: rowHi(i) > 0 ? "gold" : undefined },
    ]),
  ];
  return (
    <g>
      <g opacity={pitchO}>
        <Grass M={MP} rect={GR} C={C} band={4} along="y" />
        <Goal M={MP} C={C} cx={0} dir={-1} />
        <PLines M={MP} C={C} lines={[[[-22, 0], [22, 0]], ...boxLines(0)]} clip={GR} w={2.2} />
        <circle cx={O[0]} cy={O[1]} r={4} fill={C.ink} />
        <UText x={O[0] - 10} y={O[1] + 24} s="O" size={22} weight={800} anchor="end" fill={C.ink} halo={C.halo} C={C} />
      </g>
      {/* 슈팅 */}
      {SP.map((p, i) => {
        const k = seg(t, SHOT_T[i], SHOT_T[i] + 600, E.out);
        const o = k > 0 && t < SHOT_T[i] + 1100 ? 1 - seg(t, SHOT_T[i] + 700, SHOT_T[i] + 1100) : 0;
        return o > 0 && <Ball key={i} x={mix2(p, MISS[i], k)[0]} y={mix2(p, MISS[i], k)[1]} h={0.3 * Math.sin(Math.PI * k)} r={8} C={C} o={o} />;
      })}
      {isM ? <MidFig t={t} C={C} /> : <ElemFig t={t} C={C} />}
      {SP.map((p, i) => <Player key={i} x={p[0]} y={p[1]} n={`S${i + 1}`} team="city" C={C} r={18} o={playersO}
        ring={win(t, SHOT_T[i] - 150, SHOT_T[i] + 400, 120, 300)} />)}

      {/* 기록표 */}
      <g opacity={tabO}>
        <UText x={TX} y={TY - 12} s="맨시티의 슈팅 기록 (가상의 자료)" size={20} weight={700} fill={C.soft} C={C} />
        {[0, 1, 2].map((i) => <RowHi key={i} x={TX} y={TY} cols={TCOL} rh={TRH} r={1 + i} C={C} o={rowHi(i) * 0.9} col={["gold", "teal", "coral"][i]} />)}
        <UTable x={TX} y={TY} cols={TCOL} rh={TRH} C={C} t={t} rows={rows} />
        {[0, 1, 2].map((i) => {
          const a = rowHi(i);
          return a > 0 && <UText key={i} x={TX + 334} y={TY + 42 * (i + 1) + 29} s={`← S${i + 1} ${XG.D[i]} m${isM ? `   ${XG.M.side[i]}` : ""}`} size={20} weight={750}
            fill={C[["gold", "teal", "coral"][i]]} opacity={a} C={C} />;
        })}
      </g>

      {isM ? <MidChain t={t} C={C} /> : <ElemChain t={t} C={C} />}
      <UCaption t={t} C={C} caps={[
        { t: 300, s: "맨시티가 첼시와의 경기에서 슈팅을 세 번 했어요" },
        { t: B.a.shots, s: "슈팅 하나하나가 골이 될 확률 — 기대 득점(xG)" },
        ...(isM ? [
          { t: B.a.dist, s: "골라인 방향과 앞 방향은 수직 — 피타고라스 정리" },
          { t: B.a.table, s: `거리가 속한 계급의 골 상대도수 — ${XG.D[1]}, ${XG.D[2]}는 경계값` },
          { t: B.a.chain, s: "‘적어도 한 골’ = 1 − (모두 안 들어갈 확률)" },
          { t: B.a.chain + 5600, s: `적어도 한 골이 들어갈 확률은 {${XG.atLeast[0]}/${XG.atLeast[1]}}` },
        ] : [
          { t: B.a.dist, s: "골대 가운데 O에서 슈팅한 곳까지 줄자로 재요" },
          { t: B.a.table, s: `기록표에서 거리가 들어가는 칸 — ${XG.D[1]}, ${XG.D[2]}는 ‘이상’ 쪽` },
          { t: B.a.chain, s: `${XG.N}경기로 생각해요 — 세 슈팅이 모두 빗나간 경기는?` },
          { t: B.a.chain + 5600, s: `100경기마다 ${XG.per100}경기쯤은 적어도 한 골이 들어가요` },
        ]),
      ]} />
    </g>
  );
}

/* ── 초등: 줄자 ── */
function ElemFig({ t, C }) {
  return (
    <g>
      {SP.map((p, i) => <Tape key={i} a={p} b={O} p={seg(t, B.a.dist + 300 + i * 1700, B.a.dist + 1300 + i * 1700, E.io)} pxPerM={MP.s} C={C}
        read={XG.E.tape[i]} side={i === 1 ? -1 : 1} rs={20} w={10} />)}
    </g>
  );
}
/* ── 중등: 옆 · 앞 다리 ── */
function MidFig({ t, C }) {
  return (
    <g>
      {XG.SHOTS.map(([x, y], i) => {
        const a = seg(t, B.a.dist + 300 + i * 1700, B.a.dist + 900 + i * 1700);
        if (a <= 0) return null;
        const F = MP.p([x, 0]), S = SP[i], col = C[["gold", "teal", "coral"][i]];
        return (
          <g key={i} opacity={a}>
            <Path pts={[O, F, S]} stroke={col} sw={2.4} dash="7 6" />
            <Path pts={[O, S]} stroke={col} sw={3.4} />
            <RightMark V={F} A={O} B={S} s={10} C={C} color={col} />
            <SegLbl P={O} Q={F} s={String(Math.abs(x))} side={x > 0 ? 1 : -1} off={14} C={C} size={20} fill={col} />
            <SegLbl P={F} Q={S} s={String(y)} side={x > 0 ? 1 : -1} off={14} C={C} size={20} fill={col} />
          </g>
        );
      })}
    </g>
  );
}

/* ── 사슬: 골 없이 이어진 경기 ── */
const CY = 650;
function ElemChain({ t, C }) {
  const at = [0, 1, 2, 3].map((i) => B.a.chain + 600 + i * 1500);
  const W = chainW(XG.E.chain, 30, 150, 52);
  const x0 = 540 - W / 2;
  const head = seg(t, B.a.chain + 200, B.a.chain + 700);
  // 화살표 아래로 빠지는 골(경기 수)
  return (
    <g>
      {head > 0 && <UText x={x0} y={CY - 70} s={`${XG.E.head} — 세 슈팅이 모두 빗나간 경기`} size={24} weight={700} fill={C.soft} opacity={head} C={C} />}
      <Chain x={x0} y={CY} vals={XG.E.chain.map((v, i) => (i === 0 ? `${v}경기` : v))} ops={XG.E.ops} at={at} t={t} C={C} size={30} gap={150} bh={52} last="teal" opSize={20} />
      {XG.E.goals.map((g, i) => {
        const a = seg(t, at[i + 1] - 200, at[i + 1] + 300);
        return a > 0 && <ChainOut key={i} t={t} i={i} a={a} s={`${XG.E.opHead[i].slice(0, 2)} ${g}`} C={C} x0={x0} />;
      })}
      <UBoard x={1046} y={420} t={t} C={C} size={26} lh={50} lines={[
        { t: B.a.dist + 5200, s: XG.E.d, row: 0 },
        { t: B.a.table + 1300, s: XG.E.s[0], row: 1 },
        { t: B.a.table + 2800, s: XG.E.s[1], row: 2 },
        { t: B.a.table + 4300, s: XG.E.s[2], row: 3 },
        { t: B.a.chain + 5200, s: XG.E.hit, row: 4 },
        { t: B.a.chain + 6600, s: XG.E.per, row: 5 },
      ]} />
    </g>
  );
}
/** 사슬 i 번째 화살표 아래로 빠지는 골 */
function ChainOut({ i, a, s, C, x0 }) {
  // Chain 과 같은 배치 계산(상자 폭)
  const vals = XG.E.chain.map((v, k) => (k === 0 ? `${v}경기` : v));
  const ws = vals.map((v) => Math.max(52 * 1.4, uW(v)));
  let x = x0; for (let k = 0; k <= i; k++) x += ws[k] + (k < i ? 150 : 0);
  const mx = x + 75;
  return (
    <g opacity={a}>
      <Path pts={[[mx, CY + 8], [mx, CY + 52]]} stroke={C.gold} sw={2.6} dash="5 5" />
      <UText x={mx} y={CY + 84} s={s} size={22} weight={750} anchor="middle" fill={C.gold} C={C} />
    </g>
  );
}
const uW = (v) => uWidth(v, 30, 750) + 30 * 0.9;

function MidChain({ t, C }) {
  const at = [0, 1, 2, 3].map((i) => B.a.chain + 600 + i * 1500);
  const W = chainW(XG.M.chain, 30, 120, 60);
  const x0 = 540 - W / 2;
  const head = seg(t, B.a.chain + 200, B.a.chain + 700);
  return (
    <g>
      {head > 0 && <UText x={x0} y={CY - 72} s="모두 빗나갈 확률을 차례로 곱하면" size={24} weight={700} fill={C.soft} opacity={head} C={C} />}
      <Chain x={x0} y={CY} vals={XG.M.chain} ops={XG.M.ops} at={at} t={t} C={C} size={30} gap={120} bh={60} last="teal" opSize={22} />
      <UBoard x={1046} y={420} t={t} C={C} size={26} lh={50} lines={[
        { t: B.a.dist + 1200, s: XG.M.d1, row: 0, size: 24 },
        { t: B.a.dist + 4600, s: XG.M.d2, row: 1 },
        { t: B.a.table + 4400, s: XG.M.p, row: 2 },
        { t: B.a.table + 5600, s: XG.M.edge, row: 3, c: "soft", size: 24 },
        { t: B.a.chain + 5200, s: XG.M.none, row: 4 },
        { t: B.a.chain + 6400, s: XG.M.ans, row: 5 },
        { t: B.a.chain + 7600, s: XG.M.trap, row: 6, c: "soft", size: 24 },
      ]} />
    </g>
  );
}

export default {
  key: "soc-xg",
  dur: B.dur,
  title: { e: "슈팅 세 번, 골이 들어갈 가능성", m: "적어도 한 골이 들어갈 확률" },
  sub: { e: "초등 · 800경기로 생각하기 · 맨시티 슈팅 기록", m: "중2 · 여사건의 확률 · 맨시티 슈팅 기록" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
