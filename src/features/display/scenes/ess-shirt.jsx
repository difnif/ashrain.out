// 서술형 6 — 「축제 서술형」 3번 반티 두 업체
// A 업체는 디자인비 24000원을 한 번만 받고 한 벌에 6000원, B 업체는 디자인비 없이 한 벌에 8000원.
// A 에 주문하는 것이 B 보다 저렴하려면 적어도 몇 벌?
//   초등: 한 벌씩 쌓아 보기 — 처음 차이 24000원이 한 벌마다 8000 − 6000 = 2000원씩 줄어 24000 ÷ 2000 = 12벌에서 같고,
//         13벌부터 A 가 싸다.
//   중등: A : y = 6000x + 24000, B : y = 8000x → 8000x = 6000x + 24000 → x = 12, P(12, 96000) → x > 12 에서 A 가 아래 → 13벌
//   함정: 12벌(두 업체가 같은 값)
import { beats, seg, win, clamp } from "../core";
import { Path } from "../draw";
import { UText, UBoard, UCaption, Chip, UTable, RowHi } from "../kit-story";
import { Shirt } from "../kit-essay";
import { SHIRT as SH } from "../facts-essay";

const B = beats([["intro", 2800], ["grow", 8800], ["diff", 5800], ["ans", 6000], ["trap", 5200], ["hold", 2400]]);
const NMAX = SH.ROWS.at(-1)[0], PER = 520, GROW0 = B.a.grow + 500;
const nAt = (t) => clamp((t - GROW0) / PER, 0, NMAX);
const COL = { a: "sky", b: "coral" };
const strip = (s) => s.replace(/[‹›]/g, "");

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const nf = nAt(t), n = Math.floor(nf + 1e-9);
  return (
    <g>
      <Cards t={t} C={C} />
      {isM ? <Graph t={t} nf={nf} C={C} /> : <>
        <Shirts t={t} nf={nf} n={n} C={C} />
        <Columns t={t} nf={nf} n={n} C={C} />
        <PriceTable t={t} C={C} />
      </>}
      <UBoard x={isM ? 84 : 1022} y={isM ? 410 : 480} t={t} C={C} size={isM ? 28 : 26} lh={isM ? 52 : 48} lines={isM ? [
        { t: B.a.grow + 300, s: SH.M.a },
        { t: B.a.grow + 1200, s: SH.M.b },
        { t: B.a.diff + 300, s: SH.M.solve, size: 26 },
        { t: B.a.diff + 2600, s: SH.M.p },
        { t: B.a.ans + 1600, s: SH.M.ans, size: 26 },
        { t: B.a.trap + 1200, s: SH.M.trap },
      ] : [
        { t: B.a.diff + 300, s: SH.E.diff },
        { t: B.a.diff + 2000, s: SH.E.meet1 },
        { t: B.a.diff + 3400, s: SH.E.meet },
        { t: B.a.ans + 1600, s: SH.E.ans },
        { t: B.a.trap + 1200, s: SH.E.trap },
      ]} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: "축제 반티 — 두 업체 가운데 어디에 주문할까요?" },
        { t: B.a.grow, s: isM ? `반티 x벌의 값 y원 — 두 업체를 그래프로` : "한 벌씩 주문을 늘려 볼까요" },
        { t: GROW0 + SH.x * PER + 200, s: `${SH.x}벌에서 두 업체 값이 ${SH.y}원으로 같아져요` },
        ...(isM ? [
          { t: B.a.diff, s: "두 그래프가 만나는 점 P — 두 식의 값이 같은 x" },
          { t: B.a.diff + 2600, s: `${strip(SH.M.p)} — 두 업체 모두 ${SH.y}원` },
          { t: B.a.ans, s: `x > ${SH.x}이면 A의 그래프가 B보다 아래 — A가 싸요` },
        ] : [
          { t: B.a.diff, s: `처음에는 A가 ${SH.FEE}원 비싸지만 한 벌마다 ${SH.B1 - SH.A1}원씩 따라잡혀요` },
          { t: B.a.diff + 2000, s: `${SH.FEE}원 차이가 없어지려면 ${SH.FEE} ÷ ${SH.B1 - SH.A1} = ${SH.x}벌` },
          { t: B.a.ans, s: `${SH.x + 1}벌째부터 A가 ${SH.B1 - SH.A1}원씩 더 싸져요` },
        ]),
        { t: B.a.trap, s: `‘${SH.x}벌’이라고 하면 틀려요 — ${SH.x}벌은 두 업체가 같은 값이에요` },
        { t: B.a.trap + 2600, s: `A가 더 싸려면 적어도 ${SH.ans}벌` },
      ]} />
    </g>
  );
}

/** 두 업체 카드 */
function Cards({ t, C }) {
  const rows = [["a", "A 업체", SH.E.a], ["b", "B 업체", SH.E.b]];
  return (
    <g>
      {rows.map(([k, nm, s], i) => {
        const o = seg(t, 200 + i * 400, 700 + i * 400);
        const y = 146 + i * 98;
        return o > 0 && (
          <g key={k} opacity={o}>
            <rect x={60} y={y} width={474} height={84} rx={14} fill={C.paper} stroke={C[COL[k]]} strokeWidth={2.4} />
            <Shirt x={110} y={y + 44} s={52} col={C[COL[k]]} C={C} />
            <UText x={158} y={y + 36} s={nm} size={26} weight={800} fill={C[COL[k]]} C={C} />
            <UText x={158} y={y + 68} s={s} size={21} weight={600} fill={C.ink} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 초등: 주문한 반티 */
function Shirts({ t, nf, n, C }) {
  const o = seg(t, B.a.grow, B.a.grow + 400);
  if (o <= 0) return null;
  return (
    <g opacity={o}>
      <UText x={64} y={386} s="주문한 반티" size={22} weight={700} fill={C.soft} C={C} />
      <Chip x={214} y={378} s={`${n}벌`} size={24} C={C} anchor="start" fill={C.lilac} color={C.paper} />
      {Array.from({ length: NMAX }, (_, i) => {
        const a = clamp((nf - i) / 0.4);
        return a > 0 && <Shirt key={i} x={96 + (i % 7) * 62} y={440 + Math.floor(i / 7) * 66} s={46} col={C.lilac} C={C} o={a} />;
      })}
    </g>
  );
}

/** 초등: 값을 쌓은 기둥 두 개 */
const BASE = 640, CW = 120, CX = { a: 640, b: 800 }, KY = 380 / (SH.B1 * NMAX);
function Columns({ t, nf, n, C }) {
  const o = seg(t, B.a.grow, B.a.grow + 400);
  if (o <= 0) return null;
  const blocks = (k, base0, each) => {
    const out = [];
    const x = CX[k];
    if (base0 > 0) out.push(<g key="f">
      <rect x={x} y={BASE - base0 * KY} width={CW} height={base0 * KY} fill={C[COL[k]]} fillOpacity={0.28} stroke={C[COL[k]]} strokeWidth={2} strokeDasharray="7 5" />
      <UText x={x + CW / 2} y={BASE - (base0 * KY) / 2 + 8} s="디자인비" size={20} weight={700} anchor="middle" fill={C[COL[k]]} C={C} />
    </g>);
    for (let i = 0; i < Math.ceil(nf - 1e-9); i++) {
      const fr = clamp(nf - i), h = each * KY * fr, y0 = BASE - (base0 + each * i) * KY;
      out.push(<rect key={i} x={x} y={y0 - h} width={CW} height={h} fill={C[COL[k]]} fillOpacity={0.8} stroke={C.paper} strokeWidth={1.4} />);
    }
    return out;
  };
  const top = { a: BASE - SH.A(n) * KY, b: BASE - SH.B(n) * KY };
  const gap = SH.E.gap(n);
  const gapS = gap > 0 ? `A가 ${gap}원 비싸요` : gap === 0 ? "같아요!" : `A가 ${-gap}원 싸요`;
  return (
    <g opacity={o}>
      <Path pts={[[CX.a - 24, BASE], [CX.b + CW + 24, BASE]]} stroke={C.soft} sw={2.4} />
      {blocks("a", SH.FEE, SH.A1)}
      {blocks("b", 0, SH.B1)}
      {["a", "b"].map((k) => <g key={k}>
        <UText x={CX[k] + CW / 2} y={BASE + 34} s={k === "a" ? "A 업체" : "B 업체"} size={24} weight={800} anchor="middle" fill={C[COL[k]]} C={C} />
        <UText x={CX[k] + CW / 2} y={top[k] - 14} s={`${k === "a" ? SH.A(n) : SH.B(n)}원`} size={22} weight={750} anchor="middle" fill={C.ink} halo={C.halo} C={C} />
      </g>)}
      <Chip x={CX.a + (CX.b + CW - CX.a) / 2} y={Math.min(top.a, top.b) - 62} s={gapS} size={24} C={C}
        fill={gap === 0 ? C.gold : gap < 0 ? C.teal : C.capBg} color={gap > 0 ? C.capInk : C.paper} />
    </g>
  );
}

/** 초등: 10벌 ~ 14벌의 값 */
function PriceTable({ t, C }) {
  const X = 1022, Y = 146, cols = [100, 180, 180], rh = 50;
  const o = seg(t, GROW0 + (SH.ROWS[0][0] - 1) * PER, GROW0 + SH.ROWS[0][0] * PER);
  if (o <= 0) return null;
  const rows = [
    [{ s: "벌", color: "soft", size: 22 }, { s: "A 업체", color: COL.a, size: 22 }, { s: "B 업체", color: COL.b, size: 22 }],
    ...SH.ROWS.map(([k, a, b]) => {
      const tt = GROW0 + k * PER;
      return [{ s: `${k}벌`, t: tt }, { s: `${a}원`, t: tt, weight: a < b ? 800 : 600, color: a < b ? "teal" : undefined }, { s: `${b}원`, t: tt }];
    }),
  ];
  const rEq = SH.ROWS.findIndex(([k]) => k === SH.x) + 1, rAns = SH.ROWS.findIndex(([k]) => k === SH.ans) + 1;
  return (
    <g opacity={o}>
      <UTable x={X} y={Y} cols={cols} rh={rh} rows={rows} C={C} t={t} size={24} />
      <RowHi x={X} y={Y} cols={cols} rh={rh} r={rEq} C={C} o={win(t, GROW0 + SH.x * PER + 100, B.a.ans + 400, 300, 400)} col="gold" />
      <RowHi x={X} y={Y} cols={cols} rh={rh} r={rAns} C={C} o={seg(t, B.a.ans + 400, B.a.ans + 900)} col="teal" />
      <RowHi x={X} y={Y} cols={cols} rh={rh} r={rEq} C={C} o={win(t, B.a.trap + 300, Infinity, 300, 300)} col="red" />
    </g>
  );
}

/** 중등: 두 일차함수의 그래프 */
const G = { x0: 660, x1: 1520, y0: 640, y1: 196, X: 15, Y: 120000 };
const gx = (x) => G.x0 + (x / G.X) * (G.x1 - G.x0), gy = (y) => G.y0 - (y / G.Y) * (G.y0 - G.y1);
function Graph({ t, nf, C }) {
  const o = seg(t, B.a.grow, B.a.grow + 500);
  if (o <= 0) return null;
  const pO = seg(t, GROW0 + SH.x * PER, GROW0 + SH.x * PER + 400);
  const guide = seg(t, B.a.diff + 2400, B.a.diff + 2900);
  const shade = seg(t, B.a.ans + 300, B.a.ans + 900);
  const trap = win(t, B.a.trap + 300, Infinity, 300, 300);
  const lineA = [[gx(0), gy(SH.A(0))], [gx(nf), gy(SH.A(nf))]], lineB = [[gx(0), gy(SH.B(0))], [gx(nf), gy(SH.B(nf))]];
  const reg = [];
  for (let k = 0; k <= 20; k++) { const x = SH.x + ((NMAX - SH.x) * k) / 20; reg.push([gx(x), gy(SH.A(x))]); }
  for (let k = 20; k >= 0; k--) { const x = SH.x + ((NMAX - SH.x) * k) / 20; reg.push([gx(x), gy(SH.B(x))]); }
  return (
    <g opacity={o}>
      <Path pts={[[G.x0, G.y0], [G.x1 + 30, G.y0]]} stroke={C.soft} sw={2.4} />
      <Path pts={[[G.x0, G.y0], [G.x0, G.y1 - 26]]} stroke={C.soft} sw={2.4} />
      <UText x={G.x1 + 38} y={G.y0 + 8} s="x" size={28} C={C} />
      <UText x={G.x1 + 30} y={G.y0 + 40} s="(벌)" size={20} anchor="middle" fill={C.soft} C={C} />
      <UText x={G.x0} y={G.y1 - 36} s="y" size={28} anchor="middle" C={C} />
      <UText x={G.x0 + 44} y={G.y1 - 36} s="(원)" size={20} anchor="middle" fill={C.soft} C={C} />
      {Array.from({ length: G.X + 1 }, (_, v) => <g key={v}>
        <Path pts={[[gx(v), G.y0], [gx(v), G.y0 + (v % 4 ? 5 : 8)]]} stroke={C.soft} sw={2} />
        {(v % 4 === 0 || (v === SH.ans && shade > 0)) && <UText x={gx(v)} y={G.y0 + 32} s={String(v)} size={21} anchor="middle"
          fill={v === SH.ans ? C.teal : v === SH.x && trap > 0 ? C.red : C.soft} weight={v === SH.ans || (v === SH.x && trap > 0) ? 800 : 500} C={C} />}
      </g>)}
      {[SH.FEE, 48000, 72000, SH.y, G.Y].map((v) => <g key={v}>
        <Path pts={[[G.x0 - 7, gy(v)], [G.x0, gy(v)]]} stroke={C.soft} sw={2} />
        <UText x={G.x0 - 12} y={gy(v) + 7} s={String(v)} size={19} anchor="end" fill={C.soft} C={C} />
      </g>)}
      {shade > 0 && <Path pts={reg} closed fill={C.teal} fo={0.2 * shade} stroke="none" />}
      <Path pts={lineB} stroke={C[COL.b]} sw={4} />
      <Path pts={lineA} stroke={C[COL.a]} sw={4} />
      <circle cx={lineA[1][0]} cy={lineA[1][1]} r={6} fill={C[COL.a]} />
      <circle cx={lineB[1][0]} cy={lineB[1][1]} r={6} fill={C[COL.b]} />
      {nf > 1 && <>
        <UText x={lineA[1][0] + 14} y={lineA[1][1] + 26} s="A" size={26} weight={800} fill={C[COL.a]} halo={C.halo} C={C} />
        <UText x={lineB[1][0] - 14} y={lineB[1][1] - 10} s="B" size={26} weight={800} anchor="end" fill={C[COL.b]} halo={C.halo} C={C} />
      </>}
      {guide > 0 && <g opacity={guide}>
        <Path pts={[[G.x0, gy(SH.y)], [gx(SH.x), gy(SH.y)]]} stroke={C.gold} sw={2} dash="6 6" />
        <Path pts={[[gx(SH.x), gy(SH.y)], [gx(SH.x), G.y0]]} stroke={C.gold} sw={2} dash="6 6" />
      </g>}
      {pO > 0 && <g opacity={pO}>
        <circle cx={gx(SH.x)} cy={gy(SH.y)} r={9} fill={C.gold} stroke={C.paper} strokeWidth={2.4} />
        <Chip x={gx(SH.x) - 16} y={gy(SH.y) - 40} s={SH.M.p} size={22} C={C} anchor="end" fill={C.gold} color={C.paper} />
      </g>}
      {shade > 0 && <Chip x={gx(13.5)} y={gy(SH.A(13.5)) + 46} s="A가 아래" size={21} C={C} o={shade} fill={C.teal} color={C.paper} />}
      {trap > 0 && <UText x={gx(SH.x)} y={G.y0 + 66} s="⟪×r⟫" size={30} anchor="middle" opacity={trap} C={C} />}
    </g>
  );
}

export default {
  key: "ess-shirt",
  dur: B.dur,
  title: { e: "반티 두 업체 — 한 벌씩 쌓아 보기", m: "반티 두 업체 — 두 그래프가 만나는 점" },
  sub: { e: "초등 · 규칙과 대응 · 「축제 서술형」 3번", m: "중2 · 연립방정식과 그래프 · 「축제 서술형」 3번" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
