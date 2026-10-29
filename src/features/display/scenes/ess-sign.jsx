// 서술형 5 — 「축제 서술형」 5번 불이 켜지는 간판
// 가로 100 cm, 세로 60 cm 인 직사각형 ABCD 간판(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래). 처음에는 대각선 AC 를 경계로
// 삼각형 ACD 에만 불이 켜져 있다. 불빛 P 가 C 를 출발해 변 CB 를 따라 1초에 4 cm 씩 움직이면 사각형 APCD 에 불이 켜지고,
// 그 넓이가 4800 cm² 가 되는 순간 음악이 나온다. 그때 P 와 B 사이의 거리는?
//   초등: 직사각형에서 빼기 — 6000 − 4800 = 1200 (불 꺼진 삼각형 ABP) → PB × 60 ÷ 2 = 1200 → PB = 40 cm,
//         CP = 60 cm 를 1초에 4 cm 씩 → 15초 (초시계와 맞춰 본다)
//   중등: CP = 4x, y = {1/2} × (4x + 100) × 60 = 120x + 3000 → 120x + 3000 = 4800 → x = 15 → PB = 100 − 60 = 40 cm
//   함정: CP = 60 cm 를 답으로 쓰기
import { beats, seg, win, E, clamp } from "../core";
import { Path } from "../draw";
import { UText, UBoard, UCaption, Chip, chipW, UDim, UTable, RowHi, Tape, Stopwatch } from "../kit-story";
import { ClubIcon } from "../kit-essay";
import { SIGN as SG } from "../facts-essay";

const B = beats([["intro", 2800], ["run", 7800], ["rect", 6400], ["solve", 6400], ["time", 5800], ["trap", 5400], ["hold", 2400]]);
const S = 6.4;                                              // 1 cm = 6.4 px
const X0 = 120, Y0 = 230;
const A = [X0, Y0], D = [X0 + SG.W * S, Y0], Bv = [X0, Y0 + SG.H * S], Cv = [X0 + SG.W * S, Y0 + SG.H * S];
const RUN0 = B.a.run + 600, MSPS = 400;                     // 이야기 속 1초 = 화면 0.4초
const STOP = RUN0 + SG.x * MSPS;
const secAt = (t) => clamp((t - RUN0) / MSPS, 0, SG.x);
const Pat = (x) => [Cv[0] - SG.V * x * S, Cv[1]];
const BOOTH = "별빛 카페";
// 중등 그래프
const GR = { x0: 1040, x1: 1480, y0: 428, y1: 180, X: SG.full, Y: SG.rect };
const gx = (x) => GR.x0 + (x / GR.X) * (GR.x1 - GR.x0), gy = (y) => GR.y0 - (y / GR.Y) * (GR.y0 - GR.y1);

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const x = secAt(t), P = Pat(x);
  const signO = seg(t, 0, 700), litO = seg(t, 700, 1400), lblO = seg(t, 1100, 1800);
  const dk = C.name === "light" ? { fill: "#5c5345", fo: 0.24, txt: "#8a7d68" } : { fill: "#060a1a", fo: 0.6, txt: "#59607a" };
  const lit = [A, P, Cv, D], unlit = [A, Bv, P];
  const id = `sg${Math.round(P[0])}`;
  const music = seg(t, STOP + 100, STOP + 600);
  const runO = seg(t, B.a.run, B.a.run + 400);
  const rectHi = win(t, B.a.rect + 200, B.a.solve + 200, 400, 400);
  const darkHi = seg(t, B.a.rect + 2400, B.a.rect + 2900);
  const tapeP = seg(t, B.a.solve + 900, B.a.solve + 2200, E.io);
  const cpO = isM ? seg(t, B.a.rect + 300, B.a.rect + 800) : seg(t, B.a.time + 300, B.a.time + 800);
  const trapO = win(t, B.a.trap + 300, Infinity, 400, 400);
  return (
    <g>
      {/* 간판 */}
      <g opacity={signO}>
        <rect x={A[0] - 12} y={A[1] - 12} width={D[0] - A[0] + 24} height={Bv[1] - A[1] + 24} rx={16} fill={C.wood} stroke={C.woodEdge} strokeWidth={3} />
        <rect x={A[0]} y={A[1]} width={D[0] - A[0]} height={Bv[1] - A[1]} fill={dk.fill} fillOpacity={dk.fo + 0.25} />
        <text x={(A[0] + D[0]) / 2} y={(A[1] + Bv[1]) / 2 + 26} textAnchor="middle" fontFamily="'Pretendard Variable', Pretendard, sans-serif"
          fontSize={70} fontWeight={850} fill={dk.txt} opacity={0.75}>{BOOTH}</text>
      </g>
      {litO > 0 && <g opacity={litO}>
        <defs><clipPath id={id}><path d={"M" + lit.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join("L") + "Z"} /></clipPath></defs>
        <Path pts={lit} closed fill={C.gold} fo={C.name === "light" ? 0.42 : 0.5} stroke="none" />
        <g clipPath={`url(#${id})`}>
          <text x={(A[0] + D[0]) / 2} y={(A[1] + Bv[1]) / 2 + 26} textAnchor="middle" fontFamily="'Pretendard Variable', Pretendard, sans-serif"
            fontSize={70} fontWeight={850} fill={C.name === "light" ? "#fffaf0" : "#fff6dc"}>{BOOTH}</text>
        </g>
        <Path pts={[A, P]} stroke={C.gold} sw={3} />
      </g>}
      {/* 처음 경계(대각선 AC) */}
      <Path pts={[A, Cv]} stroke={C.ink} sw={2} dash="9 7" o={0.55 * lblO * (1 - 0.6 * seg(t, B.a.rect, B.a.rect + 500))} />
      {/* 전체 직사각형 · 불 꺼진 삼각형 강조 */}
      {rectHi > 0 && <Path pts={[A, D, Cv, Bv]} closed stroke={C.gold} sw={5} dash="14 9" o={rectHi} />}
      {darkHi > 0 && <Path pts={unlit} closed stroke={C.coral} sw={4.5} fill={C.coral} fo={0.14} o={darkHi * (1 - 0.5 * seg(t, B.a.trap, B.a.trap + 400))} />}
      {/* 꼭짓점 · 치수 */}
      <g opacity={lblO}>
        {[["A", A, -1, -1], ["D", D, 1, -1], ["B", Bv, -1, 1], ["C", Cv, 1, 1]].map(([n, p, sx, sy]) => (
          <UText key={n} x={p[0] + sx * 32} y={p[1] + sy * 30 + 10} s={n} size={30} weight={800} anchor="middle" fill={C.ink} C={C} />
        ))}
        <UDim A={A} B={D} off={46} s={`${SG.W} cm`} C={C} size={26} />
        <UDim A={D} B={Cv} off={48} s={`${SG.H} cm`} C={C} size={26} lofs={44} />
      </g>
      {/* 불빛 P */}
      {t >= 1400 && <g>
        <circle cx={P[0]} cy={P[1]} r={20} fill={C.gold} opacity={0.25 + 0.15 * Math.sin(t / 160)} />
        <circle cx={P[0]} cy={P[1]} r={10} fill={C.gold} stroke={C.paper} strokeWidth={2.5} />
        <UText x={P[0]} y={P[1] + 46} s="P" size={30} weight={800} anchor="middle" fill={C.gold} halo={C.halo} C={C} />
      </g>}
      {/* 초시계 · 넓이 */}
      {runO > 0 && <g opacity={runO}>
        <Stopwatch x={884} y={190} r={32} sec={x} full={60} C={C} col={C.ink} label={`${Math.floor(x + 1e-9)}초`} />
        <Chip x={640} y={318} s={`${Math.round(SG.area(x))} cm²`} size={26} C={C} />
      </g>}
      {music > 0 && <g opacity={music * (1 - seg(t, B.a.rect + 600, B.a.rect + 1100))}>
        {[[700, 166], [762, 146]].map(([nx, ny], i) => (
          <ClubIcon key={i} kind={0} x={nx} y={ny - 6 * Math.abs(Math.sin((t - STOP) / 220 + i))} C={{ ...C, ink: C.gold }} s={1.2} />
        ))}
      </g>}
      {/* 전체 · 불 꺼진 넓이 */}
      {rectHi > 0 && <Chip x={440} y={280} s={`전체 ${SG.rect} cm²`} size={24} C={C} o={rectHi} fill={C.gold} color={C.paper} />}
      {darkHi > 0 && <Chip x={204} y={530} s={`${SG.tri} cm²`} size={24} C={C} o={darkHi} fill={C.coral} color={C.paper} />}
      {/* 밑변 PB(줄자) · CP */}
      {tapeP > 0 && <Tape a={[P[0], P[1] + 72]} b={[Bv[0], Bv[1] + 72]} p={tapeP} pxPerM={S} C={C} read={`PB = ${SG.PB} cm`} rs={24} side={-1} />}
      {cpO > 0 && <g opacity={cpO}>
        <Path pts={[[P[0], P[1] + 8], [P[0], P[1] + 96]]} stroke={C.soft} sw={2} dash="5 5" />
        <Path pts={[[Cv[0], Cv[1] + 8], [Cv[0], Cv[1] + 96]]} stroke={C.soft} sw={2} dash="5 5" />
        <Path pts={[[P[0] + 6, Cv[1] + 86], [Cv[0] - 6, Cv[1] + 86]]} stroke={C.teal} sw={3} />
        <Chip x={(P[0] + Cv[0]) / 2} y={Cv[1] + 86} s={isM ? (t < B.a.time ? "CP = 4x" : `CP = ${SG.CP} cm`) : `CP = ${SG.CP} cm`} size={24} C={C} fill={C.teal} color={C.paper} />
      </g>}
      {/* 함정: CP 를 답으로 */}
      {trapO > 0 && <g opacity={trapO}>
        <UText x={(P[0] + Cv[0]) / 2 + chipW(`CP = ${SG.CP} cm`, 24) / 2 + 26} y={Cv[1] + 98} s="⟪×r⟫" size={34} anchor="middle" C={C} />
        <UText x={(P[0] + Bv[0]) / 2 - chipW(`PB = ${SG.PB} cm`, 24) / 2 - 26} y={Cv[1] + 54} s="⟪✓t⟫" size={34} anchor="middle" C={C} />
      </g>}
      {isM ? <Graph t={t} x={x} C={C} /> : <RateTable t={t} C={C} />}
      <UBoard x={984} y={isM ? 532 : 520} t={t} C={C} size={isM ? 29 : 27} lh={isM ? 48 : 46} lines={isM ? [
        { t: B.a.rect + 1900, s: SG.M.y },
        { t: B.a.rect + 3600, s: SG.M.y2 },
        { t: B.a.solve + 400, s: SG.M.solve },
        { t: B.a.time + 400, s: SG.M.cp2 },
        { t: B.a.time + 1600, s: SG.M.pb },
        { t: B.a.trap + 1200, s: SG.M.trap, size: 25 },
      ] : [
        { t: B.a.rect + 300, s: SG.E.rect },
        { t: B.a.rect + 2600, s: SG.E.dark },
        { t: B.a.solve + 400, s: SG.E.pb1 },
        { t: B.a.solve + 1800, s: SG.E.pb },
        { t: B.a.time + 400, s: SG.E.time },
        { t: B.a.trap + 1200, s: SG.E.trap },
      ]} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: `${BOOTH} 부스의 간판 — 가로 ${SG.W} cm, 세로 ${SG.H} cm` },
        { t: 1600, s: "처음에는 대각선 AC 위쪽, 삼각형 ACD에만 불이 켜져 있어요" },
        { t: B.a.run, s: `불빛 P가 C를 떠나 1초에 ${SG.V} cm씩 B 쪽으로 — 사각형 APCD에 불이 켜져요` },
        { t: STOP + 200, s: `넓이가 ${SG.target} cm²가 되는 순간 음악! — 이때 P와 B 사이는?` },
        ...(isM ? [
          { t: B.a.rect, s: `x초 뒤 CP = ${SG.V}x — 사각형 APCD는 사다리꼴이에요` },
          { t: B.a.rect + 3600, s: `처음 넓이 ${SG.start}, 1초마다 ${SG.rate}씩 — y는 x의 일차함수` },
          { t: B.a.solve, s: `y = ${SG.target}이 되는 x를 구해요 — 그래프에서는 두 직선이 만나는 곳` },
          { t: B.a.time, s: `CP = ${SG.CP} cm, 그러니 PB = ${SG.W} − ${SG.CP} = ${SG.PB} cm` },
        ] : [
          { t: B.a.rect, s: "간판 전체에서 불 꺼진 부분을 빼면 불 켜진 넓이예요" },
          { t: B.a.rect + 2600, s: `불 꺼진 삼각형 ABP는 ${SG.rect} − ${SG.target} = ${SG.tri} cm²` },
          { t: B.a.solve, s: `삼각형 ABP의 높이는 ${SG.H} cm — 밑변 PB를 거꾸로 셈해요` },
          { t: B.a.time, s: `P는 ${SG.CP} cm를 1초에 ${SG.V} cm씩 — ${SG.x}초 만에 왔어요` },
        ]),
        { t: B.a.trap, s: `CP = ${SG.CP} cm를 답으로 쓰면 틀려요 — 묻는 것은 P와 B 사이의 거리` },
      ]} />
    </g>
  );
}

/** 초등: 5초마다 잰 넓이 */
function RateTable({ t, C }) {
  const X = 990, Y = 150, cols = [160, 250], rh = 48;
  const o = seg(t, B.a.run, B.a.run + 500);
  if (o <= 0) return null;
  const rows = [
    [{ s: "지난 시간", color: "soft", size: 24 }, { s: "불 켜진 넓이", color: "soft", size: 24 }],
    ...SG.TABLE.map(([s, a]) => {
      const tt = RUN0 + s * MSPS;
      return [{ s: `${s}초`, t: tt }, { s: `${a} cm²`, t: tt }];
    }),
  ];
  const hiO = win(t, STOP + 200, B.a.rect + 600, 300, 400);
  const rateO = seg(t, STOP + 1400, STOP + 1900);
  return (
    <g opacity={o}>
      <UTable x={X} y={Y} cols={cols} rh={rh} rows={rows} C={C} t={t} size={26} />
      <RowHi x={X} y={Y} cols={cols} rh={rh} r={SG.TABLE.length} C={C} o={hiO} />
      {rateO > 0 && <UText x={X + 4} y={Y + rh * 5 + 44} s={SG.E.rate} size={22} weight={650} fill={C.soft} opacity={rateO} C={C} />}
    </g>
  );
}

/** 중등: y = 120x + 3000 의 그래프와 y = 4800 */
function Graph({ t, x, C }) {
  const o = seg(t, B.a.run, B.a.run + 500);
  if (o <= 0) return null;
  const pts = [[0, SG.area(0)], [x, SG.area(x)]].map(([a, b]) => [gx(a), gy(b)]);
  const dots = [];
  for (let s = 0; s <= Math.floor(x + 1e-9); s += 1) dots.push(<circle key={s} cx={gx(s)} cy={gy(SG.area(s))} r={s % 5 ? 3 : 5} fill={C.gold} />);
  const tgO = seg(t, STOP - 200, STOP + 300);
  const hit = seg(t, B.a.solve + 1200, B.a.solve + 1800);
  const ext = seg(t, B.a.solve + 300, B.a.solve + 1100);
  const full = [[gx(0), gy(SG.area(0))], [gx(SG.full), gy(SG.area(SG.full))]];
  return (
    <g opacity={o}>
      <Path pts={[[GR.x0, GR.y0], [GR.x1 + 22, GR.y0]]} stroke={C.soft} sw={2.4} />
      <Path pts={[[GR.x0, GR.y0], [GR.x0, GR.y1 - 22]]} stroke={C.soft} sw={2.4} />
      <UText x={GR.x1 + 30} y={GR.y0 + 8} s="x" size={26} C={C} />
      <UText x={GR.x0 - 8} y={GR.y1 - 32} s="y" size={26} anchor="middle" C={C} />
      {[0, 5, 10, 15, 20, 25].map((v) => <g key={v}>
        <Path pts={[[gx(v), GR.y0], [gx(v), GR.y0 + 7]]} stroke={C.soft} sw={2} />
        <UText x={gx(v)} y={GR.y0 + 32} s={String(v)} size={20} anchor="middle" fill={v === SG.x && hit > 0 ? C.gold : C.soft} weight={v === SG.x && hit > 0 ? 800 : 500} C={C} />
      </g>)}
      {[SG.start, SG.target, SG.rect].map((v) => <g key={v}>
        <Path pts={[[GR.x0 - 7, gy(v)], [GR.x0, gy(v)]]} stroke={C.soft} sw={2} />
        <UText x={GR.x0 - 12} y={gy(v) + 7} s={String(v)} size={20} anchor="end" fill={v === SG.target ? C.coral : C.soft} C={C} />
      </g>)}
      {ext > 0 && <Path pts={full} stroke={C.gold} sw={2} dash="6 6" o={0.5 * ext} />}
      <Path pts={pts} stroke={C.gold} sw={4} />
      {dots}
      {tgO > 0 && <Path pts={[[GR.x0, gy(SG.target)], [GR.x1, gy(SG.target)]]} stroke={C.coral} sw={2.4} dash="8 6" o={tgO} />}
      {hit > 0 && <g opacity={hit}>
        <Path pts={[[gx(SG.x), gy(SG.target)], [gx(SG.x), GR.y0]]} stroke={C.gold} sw={2.4} dash="6 5" />
        <circle cx={gx(SG.x)} cy={gy(SG.target)} r={8} fill={C.gold} stroke={C.paper} strokeWidth={2} />
        <Chip x={gx(SG.x) + 14} y={gy(SG.target) - 34} s={`(${SG.x}, ${SG.target})`} size={22} C={C} anchor="start" fill={C.gold} color={C.paper} />
      </g>}
    </g>
  );
}

export default {
  key: "ess-sign",
  dur: B.dur,
  title: { e: "불이 켜지는 간판 — 직사각형에서 빼기", m: "불이 켜지는 간판 — 움직이는 점과 일차함수" },
  sub: { e: "초등 · 넓이와 빠르기 · 「축제 서술형」 5번", m: "중2 · 일차함수의 활용 · 「축제 서술형」 5번" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
