// 서술형 3 — 「게임의 규칙」 마지막 한 자리: 동아리 추가 모집
// 네 동아리에 한 자리씩. 한 사람은 한 곳에만 지원하고, 한 동아리에 두 명 이상 지원하면 그 동아리는 아무도 받지 않는다.
// 서아 · 도윤 · 지민이 상의 없이 네 곳 중 하나를 같은 가능성으로 고를 때 셋 다 붙을 확률.
//   초등: 고르는 방법을 모두 칸으로 — 서아의 선택마다 16칸, 모두 64칸 → 서아가 고른 곳의 가로줄 · 세로줄, 둘이 같은 대각선을 지우면
//         6칸씩 남는다 → 6 + 6 + 6 + 6 = 24 → 64번 중 24번 → {3/8}
//   중등: 모든 경우 4 × 4 × 4 = 64, 셋이 서로 다른 곳 4 × 3 × 2 = 24 → {24/64} = {3/8} · 4 + 4 + 4 = 12 ✗(함께 고르니 곱의 법칙)
// 끝: "너는 어디 지원할 거야?" — 상의하면 {3/8} 이 1 이 된다.
import { beats, seg, win } from "../core";
import { Arrow, Path } from "../draw";
import { UText, UBoard, UCaption, Chip, CircNum, Person } from "../kit-story";
import { ClubIcon } from "../kit-essay";
import { CLUB as CB } from "../facts-essay";

const B = beats([["intro", 2600], ["try1", 5600], ["try2", 4600], ["grid", 7000], ["cut", 7800], ["ans", 5800], ["talk", 5200], ["hold", 2400]]);
const N = CB.n;
const FR_X = 118, FR_Y = [262, 392, 522], FR_COL = ["gold", "teal", "blue"];
const CARD = { x: 250, w: 268, h: 84, y0: 166, gap: 10 };
const cardY = (c) => CARD.y0 + c * (CARD.h + CARD.gap);
const CLUB_COL = ["coral", "sky", "leaf", "lilac"];
const TALK = (() => { const c = CB.CELLS.find((x) => x.ok); return [c.s, c.d, c.j]; })();
const PH = [
  { tri: CB.TRIES[0], a: B.a.try1 + 700, b: B.b.try1 },
  { tri: CB.TRIES[1], a: B.a.try2 + 300, b: B.b.try2 },
  { tri: TALK, a: B.a.talk + 1800, b: Infinity },
];
// 64칸: 서아의 선택(블록) × 도윤(가로줄) × 지민(세로줄)
const GX = 640, CELL = 40, CG = 6, GBW = N * CELL + (N - 1) * CG, GGAP = 62, GY = 232;
const bx = (s) => GX + s * (GBW + GGAP);
const cxy = (s, d, j) => [bx(s) + j * (CELL + CG), GY + d * (CELL + CG)];
const CUT0 = B.a.cut + 300, cutAt = (s) => (s === 0 ? CUT0 : CUT0 + 3500 + (s - 1) * 350);

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const boardO = seg(t, 0, 600);
  const ph = PH.find((p) => t >= p.a - 200 && t < p.b);
  const gridO = seg(t, B.a.grid, B.a.grid + 500);
  return (
    <g>
      {/* 게시판 */}
      <g opacity={boardO}>
        <rect x={CARD.x - 16} y={124} width={CARD.w + 32} height={cardY(N - 1) + CARD.h + 16 - 124} rx={18} fill={C.card} fillOpacity={0.5} stroke={C.cardEdge} strokeWidth={1.5} />
        <UText x={CARD.x} y={152} s="추가 모집 · 남은 자리" size={20} weight={700} fill={C.soft} C={C} />
        {CB.CLUBS.map((name, c) => <Card key={c} c={c} name={name} t={t} C={C} ph={ph} />)}
      </g>
      {/* 친구 셋 */}
      {CB.FRIENDS.map((nm, i) => {
        const o = seg(t, B.a.try1 + i * 200, B.a.try1 + 400 + i * 200);
        const res = ph && ph.tri && t >= ph.a + 1900 ? CB.admitted(ph.tri)[i] : null;
        const ro = res == null ? 0 : seg(t, ph.a + 1900, ph.a + 2300) * (1 - seg(t, ph.b - 400, ph.b));
        return o > 0 && (
          <g key={nm} opacity={o}>
            <Person x={FR_X} y={FR_Y[i]} h={56} col={C[FR_COL[i]]} C={C} />
            <UText x={FR_X} y={FR_Y[i] + 26} s={nm} size={22} weight={750} anchor="middle" fill={C[FR_COL[i]]} C={C} />
            {ro > 0 && <UText x={FR_X - 54} y={FR_Y[i] - 16} s={res ? "⟪✓t⟫" : "⟪×r⟫"} size={34} anchor="middle" opacity={ro} C={C} />}
          </g>
        );
      })}
      {/* 지원 화살표 */}
      {ph && ph.tri.map((c, i) => {
        const o = seg(t, ph.a + i * 450, ph.a + i * 450 + 350) * (1 - seg(t, ph.b - 400, ph.b));
        return o > 0 && <Arrow key={i} p={[FR_X + 34, FR_Y[i] - 28]} q={[CARD.x - 8, cardY(c) + CARD.h / 2 + (i - 1) * 10]} stroke={C[FR_COL[i]]} sw={3.6} h={14} o={o} />;
      })}
      {/* 상의 */}
      {t >= B.a.talk && <g opacity={seg(t, B.a.talk + 300, B.a.talk + 800)}>
        <path d={`M${FR_X - 8} ${FR_Y[2] + 44}L${FR_X + 4} ${FR_Y[2] + 66}L${FR_X + 22} ${FR_Y[2] + 66}Z`} fill={C.gold} />
        <Chip x={56} y={FR_Y[2] + 84} s="너는 어디 지원할 거야?" size={24} C={C} anchor="start" fill={C.gold} color={C.paper} />
      </g>}
      {/* 64칸 */}
      {gridO > 0 && <g opacity={gridO}>
        <UText x={GX - 24} y={GY - 10} s={CB.FRIENDS[2]} size={18} weight={700} anchor="end" fill={C.soft} C={C} />
        <UText x={GX - 24} y={GY + GBW / 2 + 7} s={CB.FRIENDS[1]} size={18} weight={700} anchor="end" fill={C.soft} C={C} />
        {Array.from({ length: N }, (_, s) => <Block key={s} s={s} t={t} C={C} isM={isM} />)}
        <Examples t={t} C={C} />
      </g>}
      <UBoard x={GX} y={540} t={t} C={C} size={32} lh={58} lines={isM ? [
        { t: B.a.grid + 3400, s: CB.M.all },
        { t: CUT0 + 2900, s: CB.M.ok },
        { t: B.a.ans + 300, s: CB.M.ans },
        { t: B.a.ans + 2600, s: CB.M.trap, size: 28 },
        { t: B.a.talk + 3000, s: CB.M.talk },
      ] : [
        { t: B.a.grid + 3400, s: CB.E.all },
        { t: CUT0 + 2900, s: CB.E.block },
        { t: B.a.ans + 300, s: CB.E.sum },
        { t: B.a.ans + 2000, s: CB.E.ans },
        { t: B.a.talk + 3000, s: CB.E.talk },
      ]} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: `동아리 추가 모집 마감 10분 전 — ${N}곳에 한 자리씩 남았어요` },
        { t: B.a.try1, s: "한 동아리에 두 명 이상 지원하면 그 동아리는 아무도 받지 않아요" },
        { t: B.a.try1 + 2600, s: `${CB.CLUBS[CB.TRIES[0][0]]}에 둘이 몰려 둘 다 떨어졌어요` },
        { t: B.a.try2, s: "셋이 서로 다른 곳에 지원하면 — 셋 다 붙어요" },
        { t: B.a.grid + 4800, s: `아까의 두 번도 이 ${CB.total}칸 가운데 한 칸씩이에요`, u: CUT0 },
        ...(isM ? [
          { t: B.a.grid, s: "세 사람이 한 곳씩 고르는 경우 — 곱의 법칙" },
          { t: B.a.grid + 3400, s: `모든 경우 ${N * N * N}가지 — 하나하나 가능성이 같아요` },
          { t: CUT0, s: `도윤은 서아가 고른 곳을 뺀 ${N - 1}곳 중 하나` },
          { t: CUT0 + 1800, s: `지민은 두 사람이 고른 곳을 뺀 ${N - 2}곳 중 하나` },
          { t: CUT0 + 2900, s: strip(CB.M.ok) },
          { t: B.a.ans, s: `셋 다 붙을 확률 ${strip(CB.M.ans)}` },
          { t: B.a.ans + 2600, s: "따로따로가 아니라 함께 고르니 더하지 않고 곱해요" },
        ] : [
          { t: B.a.grid, s: `서아가 고르는 곳마다 도윤 · 지민이 고르는 칸이 ${N * N}개씩` },
          { t: B.a.grid + 3400, s: `모두 ${CB.total}칸 — 하나하나 가능성이 같아요` },
          { t: CUT0, s: `서아가 ${CB.CLUBS[0]}라면 — 도윤은 ${CB.CLUBS[0]}를 고르면 안 돼요` },
          { t: CUT0 + 900, s: `지민도 ${CB.CLUBS[0]}를 고르면 안 돼요` },
          { t: CUT0 + 1800, s: "도윤과 지민이 같은 곳을 골라도 안 돼요" },
          { t: CUT0 + 2900, s: `남는 칸은 ${CB.perBlock}개 — 서아가 어디를 고르든 같아요` },
          { t: B.a.ans, s: `${CB.total}번 중 ${CB.ok}번 — 셋 다 붙어요` },
        ]),
        { t: B.a.talk, s: "그런데 서로 물어본다면?" },
        { t: B.a.talk + 3000, s: `‘너는 어디 지원할 거야?’ — 그 물음 하나로 ${fr(CB.p)}이 1이 돼요` },
      ].sort(byT)} />
    </g>
  );
}
const strip = (s) => s.replace(/[‹›]/g, "");
const byT = (a, b) => a.t - b.t;
const fr = ([a, b]) => (b === 1 ? String(a) : `{${a}/${b}}`);

/** 동아리 카드: 지원한 사람 수에 따라 ✓ / ✗ */
function Card({ c, name, t, C, ph }) {
  const y = cardY(c);
  const n = ph ? ph.tri.filter((x) => x === c).length : 0;
  const ro = ph && n > 0 ? seg(t, ph.a + 1500, ph.a + 1900) * (1 - seg(t, ph.b - 400, ph.b)) : 0;
  const col = n >= 2 ? C.red : C.teal;
  return (
    <g>
      <rect x={CARD.x} y={y} width={CARD.w} height={CARD.h} rx={12} fill={C.paper} stroke={ro > 0 ? col : C.cardEdge} strokeWidth={ro > 0 ? 2 + 2 * ro : 1.5} />
      <rect x={CARD.x} y={y} width={10} height={CARD.h} rx={5} fill={C[CLUB_COL[c]]} />
      <ClubIcon kind={c} x={CARD.x + 48} y={y + CARD.h / 2} C={C} s={1.25} />
      <UText x={CARD.x + 84} y={y + 38} s={name} size={25} weight={750} fill={C.ink} C={C} />
      <UText x={CARD.x + 84} y={y + 68} s="남은 자리 1" size={18} weight={600} fill={C.soft} C={C} />
      {ro > 0 && <UText x={CARD.x + CARD.w - 36} y={y + CARD.h / 2 + 14} s={n >= 2 ? "⟪×r⟫" : "⟪✓t⟫"} size={40} anchor="middle" opacity={ro} C={C} />}
    </g>
  );
}

/** 서아의 선택 하나에 딸린 16칸 */
function Block({ s, t, C, isM }) {
  const a0 = B.a.grid + 300 + s * 650;
  const c0 = cutAt(s), fast = s > 0;
  const kRow = seg(t, c0, c0 + (fast ? 400 : 600));
  const kCol = seg(t, c0 + (fast ? 150 : 900), c0 + (fast ? 550 : 1500));
  const kDia = seg(t, c0 + (fast ? 300 : 1800), c0 + (fast ? 700 : 2400));
  const kOk = seg(t, c0 + (fast ? 650 : 2600), c0 + (fast ? 1050 : 3000));
  const lineO = 1 - 0.75 * seg(t, B.a.ans, B.a.ans + 600);
  const pulse = win(t, B.a.ans + 300, B.a.ans + 2600, 300, 600);
  const x0 = bx(s), y1 = GY + GBW;
  const mid = (i) => i * (CELL + CG) + CELL / 2;
  const cells = [];
  for (let d = 0; d < N; d++) for (let j = 0; j < N; j++) {
    const a = seg(t, a0 + (d * N + j) * 22, a0 + (d * N + j) * 22 + 260);
    if (a <= 0) continue;
    const ok = d !== s && j !== s && d !== j;
    const cut = Math.max(d === s ? kRow : 0, j === s ? kCol : 0, d === j ? kDia : 0);
    const [x, y] = cxy(s, d, j);
    cells.push(<rect key={d * N + j} x={x} y={y} width={CELL} height={CELL} rx={8} opacity={a * (1 - 0.6 * cut)}
      fill={ok ? C.gold : C.faint} fillOpacity={ok ? 0.12 + 0.6 * kOk + 0.2 * pulse : 1}
      stroke={ok && kOk > 0 ? C.gold : C.soft} strokeWidth={ok && kOk > 0 ? 2.4 : 1.2} />);
  }
  const ho = seg(t, a0, a0 + 400);
  return (
    <g>
      <g opacity={ho}>
        <UText x={x0 + GBW / 2} y={GY - 54} s={`${CB.FRIENDS[0]} → ${CB.CLUBS[s]}`} size={21} weight={750} anchor="middle" fill={C.ink} C={C} />
        <rect x={x0 + 6} y={GY - 44} width={GBW - 12} height={5} rx={2.5} fill={C[CLUB_COL[s]]} />
        {Array.from({ length: N }, (_, i) => <circle key={"c" + i} cx={x0 + mid(i)} cy={GY - 18} r={7} fill={C[CLUB_COL[i]]} />)}
        {Array.from({ length: N }, (_, i) => <circle key={"r" + i} cx={x0 - 16} cy={GY + mid(i)} r={7} fill={C[CLUB_COL[i]]} />)}
      </g>
      {cells}
      {/* 지우는 줄: 서아가 고른 곳의 가로줄 · 세로줄, 도윤 = 지민 인 대각선 */}
      <g opacity={lineO}>
        {kRow > 0 && <Path pts={[[x0 - 6, GY + mid(s)], [x0 - 6 + (GBW + 12) * kRow, GY + mid(s)]]} stroke={C.red} sw={4} />}
        {kCol > 0 && <Path pts={[[x0 + mid(s), GY - 6], [x0 + mid(s), GY - 6 + (GBW + 12) * kCol]]} stroke={C.red} sw={4} />}
        {kDia > 0 && <Path pts={[[x0 - 4, GY - 4], [x0 - 4 + (GBW + 8) * kDia, GY - 4 + (GBW + 8) * kDia]]} stroke={C.red} sw={4} />}
      </g>
      {kOk > 0 && <Chip x={x0 + GBW / 2} y={y1 + 34} s={isM ? `${N - 1} × ${N - 2} = ${CB.perBlock}` : `${CB.perBlock}칸`} size={22} C={C}
        o={seg(t, c0 + (fast ? 800 : 2800), c0 + (fast ? 1200 : 3200))} fill={C.gold} color={C.paper} />}
    </g>
  );
}

/** 앞의 두 번 지원이 64칸 가운데 어디인지 */
function Examples({ t, C }) {
  const a = win(t, B.a.grid + 4800, B.a.cut - 100, 400, 400);
  if (a <= 0) return null;
  return (
    <g opacity={a}>
      {CB.TRIES.map((tr, i) => {
        const [x, y] = cxy(...tr), ok = CB.admitted(tr).every(Boolean);
        return (
          <g key={i}>
            <rect x={x - 5} y={y - 5} width={CELL + 10} height={CELL + 10} rx={11} fill="none" stroke={ok ? C.gold : C.red} strokeWidth={4} />
            <CircNum x={x + CELL / 2} y={y + CELL / 2} n={i + 1} r={14} C={C} fill={ok ? C.gold : C.red} color={C.paper} stroke={ok ? C.gold : C.red} />
          </g>
        );
      })}
    </g>
  );
}

export default {
  key: "ess-club",
  dur: B.dur,
  title: { e: "마지막 한 자리 — 64칸으로 세기", m: "마지막 한 자리 — 셋 다 붙을 확률" },
  sub: { e: "초등 · 일이 일어날 가능성 · 「게임의 규칙」", m: "중2 · 경우의 수와 확률 · 「게임의 규칙」" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
