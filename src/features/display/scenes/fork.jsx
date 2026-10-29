// 장면 — 두 갈래 길과 가능성(초등) ↔ 두 갈래 길과 확률: 합의 법칙·곱의 법칙(중2)
// 갈림길을 두 번 지나는 길(왼·오)은 4가지. 구멍 A·B·C 로 가는 길은 1·2·1 가지.
//   길 하나씩: 구슬이 네 길을 차례로 굴러가고, 오른쪽에 (중등) 확률 나무 / (초등) 길 목록이 채워진다.
//   구멍마다: 중등 — A = {1/2}×{1/2} = {1/4}(곱), B = {1/4}+{1/4} = {1/2}(합) · 초등 — 4가지 중 1·2·1가지 → 가능성의 말
//   구슬 4개: B·A·C·B 로 들어간다.
//     중등 — A·B·C 에 모두 들어갈 확률: 모양 AABC·ABBC·ABCC (순서 12가지씩) → {3/32}+{3/16}+{3/32} = {3/8}
//     초등 — 40개를 굴려 보면 A 9 · B 21 · C 10: B 에 절반쯤
import { beats, seg, win, E, partial, along } from "../core";
import { Board, Caption, MText, Path, Table } from "../draw";
import { FORK } from "../branch.js";
import { CHANCE } from "../facts";

const B = beats([
  ["intro", 2600], ["p0", 2500], ["p1", 2500], ["p2", 2500], ["p3", 2500], ["holes", 6200],
  ["four", 10600], ["calc", 13200], ["hold", 2400],
]);
const ENT = [450, 196], N0 = [450, 296], N1 = [[320, 440], [580, 440]], HOLES = [[190, 600], [450, 600], [710, 600]];
const HR = 42, MR = 15;
const pathPts = (d) => [ENT, N0, N1[d[0]], HOLES[d[0] + d[1]]];
const NAMES = ["A", "B", "C"];
const LR = (v) => (v ? "오" : "왼");
// 구슬 4개(네 번째 장): 놓는 시각·도착 시각
const F0 = (k) => B.a.four + 2200 + k * 1900;
const ROLL = 1500;
// 초등 40개
const E0 = (i) => B.a.calc + 1400 + i * 150, EROLL = 900;

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const cols = [C.gold, C.coral, C.teal, C.sky];
  const roadO = seg(t, 150, 1200);
  const pathP = (k) => seg(t, B.a[`p${k}`] + 250, B.a[`p${k}`] + 250 + ROLL, E.io);       // 길 k 의 구슬 진행
  const treeO = isM ? 1 - seg(t, B.a.four, B.a.four + 600) : 0;
  const listO = !isM ? 1 - seg(t, B.a.four, B.a.four + 600) : 0;
  const pathsFade = 1 - 0.6 * seg(t, B.a.four, B.a.four + 600);
  // 구멍에 든 구슬(네 번째 장) — 도착한 것만
  const landed4 = FORK.SEQ.map((pk, k) => ({ k, pk, at: F0(k) + ROLL })).filter((o) => t >= o.at);
  return (
    <g>
      <Roads C={C} o={roadO} t={t} isM={isM} />
      {/* 네 길(색) — 그 길의 구슬이 지나간 만큼 */}
      {FORK.PATHS.map((d, k) => {
        const p = pathP(k);
        return p > 0 && <Path key={k} pts={partial(pathPts(d), p)} stroke={cols[k]} sw={7} o={0.9 * pathsFade * (isM || t < B.a.calc ? 1 : 0.4)} />;
      })}
      {/* 길을 따라가는 구슬(길마다 하나) */}
      {FORK.PATHS.map((d, k) => {
        const p = pathP(k), o = win(t, B.a[`p${k}`] + 150, B.a.four, 200, 500);
        if (p <= 0 || o <= 0) return null;
        const [x, y] = along(pathPts(d), p);
        return <circle key={k} cx={x} cy={y} r={MR} fill={cols[k]} opacity={o} />;
      })}
      {/* 구슬 4개를 하나씩 */}
      {FORK.SEQ.map((pk, k) => {
        const p = seg(t, F0(k), F0(k) + ROLL, E.io);
        if (p <= 0) return null;
        const h = FORK.holeOf2(FORK.PATHS[pk]);
        const sameBefore = FORK.SEQ.slice(0, k).filter((q) => FORK.holeOf2(FORK.PATHS[q]) === h).length;
        const rest = [HOLES[h][0] + (sameBefore ? 15 : FORK.SEQ.filter((q) => FORK.holeOf2(FORK.PATHS[q]) === h).length > 1 ? -15 : 0), HOLES[h][1]];
        const [x, y] = p < 1 ? along([...pathPts(FORK.PATHS[pk]).slice(0, 3), rest], p) : rest;
        const o = !isM ? 1 - seg(t, B.a.calc + 300, B.a.calc + 900) : 1;
        return (
          <g key={"f" + k} opacity={o}>
            <circle cx={x} cy={y} r={MR} fill={cols[k]} />
            <text x={x} y={y + 6} fontSize={17} fontWeight={800} textAnchor="middle" fill={C.halo}>{k + 1}</text>
          </g>
        );
      })}
      {/* 초등: 40개를 굴려 보면 */}
      {!isM && <Forty t={t} C={C} cols={cols} />}
      {/* 오른쪽 */}
      {isM ? <Tree t={t} C={C} cols={cols} o={treeO} /> : <PathList t={t} C={C} cols={cols} o={listO} />}
      <Question t={t} C={C} isM={isM} landed={landed4} cols={cols} />
      {isM ? <Calc t={t} C={C} /> : <Bars t={t} C={C} />}
      <Board x={880} y={isM ? 548 : 560} t={t} C={C} size={30} lh={52} lines={isM ? [
        { t: B.a.holes + 300, s: "곱의 법칙 · 합의 법칙", k: "h", u: B.a.four },
        { t: B.a.holes + 900, s: "A : {1/2} × {1/2} = ‹{1/4}›", u: B.a.four },
        { t: B.a.holes + 2300, s: "B : {1/4} + {1/4} = ‹{1/2}›", u: B.a.four },
        { t: B.a.holes + 3700, s: "C : {1/2} × {1/2} = ‹{1/4}›", u: B.a.four },
        { t: B.a.calc + 5200, s: "세 모양은 함께 일어나지 않으니 더해요", k: "h", row: 0 },
        { t: B.a.calc + 6000, s: `{3/32} + {3/16} + {3/32} = ‹{${FORK.PALL[0]}/${FORK.PALL[1]}}›`, row: 1 },
        { t: B.a.calc + 8600, s: "순서 12가지 = A 두 개의 자리 6 × B·C 2", row: 2, size: 25 },
      ] : [
        { t: B.a.holes + 300, s: "4가지 길 가운데", k: "h", u: B.a.four },
        { t: B.a.holes + 900, s: `A · C : 1가지씩 → ‹${CHANCE.WORDS[1]}›`, u: B.a.four },
        { t: B.a.holes + 2300, s: `B : 2가지 → ‹${CHANCE.WORDS[2]}›`, u: B.a.four },
        { t: B.a.holes + 3700, s: "B로 갈 가능성이 가장 커요", u: B.a.four },
        { t: B.a.calc + 8200, s: `B에 ‹${FORK.E40C[1]}›개 — 40개의 절반쯤`, row: 1 },
        { t: B.a.calc + 9400, s: `A ${FORK.E40C[0]}개 · C ${FORK.E40C[2]}개 — 4개 중 1개꼴`, row: 2 },
      ]} />
      <Caption t={t} C={C} y={862} size={33} caps={isM ? [
        { t: 300, s: "갈림길에서 왼쪽·오른쪽으로 갈 확률은 각각 {1/2}" },
        { t: B.a.p0 + 200, s: "갈림길을 두 번 지나는 길은 모두 몇 가지일까요?" },
        { t: B.a.p3 + 1200, s: "2 × 2 = 4가지 — 구멍 A·B·C 로 가는 길은 1·2·1가지" },
        { t: B.a.holes + 400, s: "한 길의 확률은 곱하고(곱의 법칙), B 로 가는 두 길은 더해요(합의 법칙)" },
        { t: B.a.four + 300, s: "이번엔 구슬 4개를 하나씩 굴려요" },
        { t: B.a.four + 2200 + 4 * 1900, s: "A·B·C 에 모두 들어갔어요 — 이렇게 될 확률은?" },
        { t: B.a.calc + 300, s: "개수의 모양은 AABC · ABBC · ABCC 세 가지" },
        { t: B.a.calc + 6000, s: `세 구멍에 모두 들어갈 확률은 {${FORK.PALL[0]}/${FORK.PALL[1]}}` },
      ] : [
        { t: 300, s: "갈림길에서 왼쪽·오른쪽으로 갈 가능성은 반반이에요" },
        { t: B.a.p0 + 200, s: "갈림길을 두 번 지나는 길은 모두 몇 가지일까요?" },
        { t: B.a.p3 + 1200, s: "길은 4가지 — A로 1가지, B로 2가지, C로 1가지" },
        { t: B.a.holes + 400, s: "길이 많은 B로 갈 가능성이 가장 커요" },
        { t: B.a.four + 300, s: "구슬 4개를 하나씩 굴리면 B에 몇 개쯤 들어갈까요?" },
        { t: B.a.four + 2200 + 4 * 1900, s: "이번엔 B에 2개 — 4개의 반이에요" },
        { t: B.a.calc + 300, s: "40개를 굴려 보면?" },
        { t: B.a.calc + 8200, s: "B에 절반쯤, A와 C에 4분의 1쯤 들어갔어요" },
      ]} />
    </g>
  );
}

/** 길(넓은 홈) · 갈림목 · 구멍 · 갈림목의 반반 표시 */
function Roads({ C, o, t, isM }) {
  const edges = [[ENT, N0], [N0, N1[0]], [N0, N1[1]], [N1[0], HOLES[0]], [N1[0], HOLES[1]], [N1[1], HOLES[1]], [N1[1], HOLES[2]]];
  const halfO = seg(t, 1200, 1900) * o;
  const forks = [[N0, N1[0], N1[1]], [N1[0], HOLES[0], HOLES[1]], [N1[1], HOLES[1], HOLES[2]]];
  return (
    <g opacity={o}>
      {edges.map(([p, q], i) => <Path key={"w" + i} pts={[p, q]} stroke={C.ink} sw={34} o={0.1} />)}
      {edges.map(([p, q], i) => <Path key={"l" + i} pts={[p, q]} stroke={C.soft} sw={3} o={0.7} dash="2 9" />)}
      <Path pts={[[ENT[0] - 34, ENT[1] - 40], [ENT[0] - 16, ENT[1]], [ENT[0] + 16, ENT[1]], [ENT[0] + 34, ENT[1] - 40]]} stroke={C.ink} sw={4} o={0.8} />
      {[N0, ...N1].map((p, i) => <circle key={"n" + i} cx={p[0]} cy={p[1]} r={9} fill={C.soft} />)}
      {HOLES.map((h, k) => (
        <g key={"h" + k}>
          <circle cx={h[0]} cy={h[1]} r={HR} fill={C.ink} fillOpacity={0.1} stroke={C.ink} strokeWidth={3.5} />
          <MText x={h[0]} y={h[1] + HR + 46} s={NAMES[k]} size={38} weight={800} anchor="middle" C={C} />
        </g>
      ))}
      {/* 갈림목마다 반반 */}
      {forks.map(([p, a, b], i) => [a, b].map((q, j) => {
        const m = [p[0] + (q[0] - p[0]) * 0.42 + (j ? 26 : -26), p[1] + (q[1] - p[1]) * 0.42 - 6];
        return <MText key={`${i}-${j}`} x={m[0]} y={m[1]} s={isM ? "{1/2}" : "반"} size={isM ? 24 : 24} weight={700} anchor="middle"
          fill={C.teal} halo={C.halo} opacity={halfO} C={C} />;
      }))}
    </g>
  );
}

/** 중등: 확률 나무 — 길이 지나갈 때마다 가지가 생긴다 */
const TR = { root: [1090, 196], l1: [[970, 292], [1210, 292]], leaf: [[910, 396], [1030, 396], [1150, 396], [1270, 396]] };
function Tree({ t, C, cols, o }) {
  if (o <= 0.01) return null;
  const startO = seg(t, B.a.p0, B.a.p0 + 400);
  return (
    <g opacity={o}>
      <MText x={880} y={176} s="확률 나무" size={24} weight={700} fill={C.soft} opacity={startO} C={C} />
      <circle cx={TR.root[0]} cy={TR.root[1]} r={7} fill={C.ink} opacity={startO} />
      {FORK.PATHS.map((d, k) => {
        const a = B.a[`p${k}`] + 250, p1 = seg(t, a, a + 700), p2 = seg(t, a + 700, a + ROLL);
        const L1 = TR.l1[d[0]], lf = TR.leaf[k];
        const h = FORK.holeOf2(d);
        return (
          <g key={k}>
            {p1 > 0 && <Path pts={partial([TR.root, L1], p1)} stroke={cols[k]} sw={4} o={0.9} />}
            {p2 > 0 && <Path pts={partial([L1, lf], p2)} stroke={cols[k]} sw={4} o={0.9} />}
            {p1 >= 1 && <circle cx={L1[0]} cy={L1[1]} r={6} fill={C.ink} />}
            <MText x={(TR.root[0] + L1[0]) / 2 + (d[0] ? 30 : -30)} y={(TR.root[1] + L1[1]) / 2 + 4} s={`${LR(d[0])} {1/2}`} size={20} weight={700}
              anchor="middle" fill={C.teal} opacity={seg(t, a + 300, a + 700)} C={C} />
            <MText x={(L1[0] + lf[0]) / 2 + (d[1] ? 22 : -22)} y={(L1[1] + lf[1]) / 2 + 4} s={`${LR(d[1])} {1/2}`} size={20} weight={700}
              anchor="middle" fill={C.teal} opacity={seg(t, a + 1000, a + 1400)} C={C} />
            <MText x={lf[0]} y={lf[1] + 40} s={NAMES[h]} size={30} weight={800} anchor="middle" fill={cols[k]} opacity={seg(t, a + ROLL - 100, a + ROLL + 300)} C={C} />
            <MText x={lf[0]} y={lf[1] + 86} s="{1/4}" size={26} weight={700} anchor="middle" opacity={seg(t, a + ROLL + 200, a + ROLL + 600)} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 초등: 길 목록 */
function PathList({ t, C, cols, o }) {
  if (o <= 0.01) return null;
  return (
    <g opacity={o}>
      <MText x={880} y={190} s="길을 하나씩 찾아봐요" size={26} weight={700} fill={C.soft} opacity={seg(t, B.a.p0, B.a.p0 + 400)} C={C} />
      {FORK.PATHS.map((d, k) => {
        const a = B.a[`p${k}`] + 250, y = 250 + k * 62;
        return (
          <g key={k} opacity={seg(t, a, a + 400)}>
            <circle cx={896} cy={y - 10} r={12} fill={cols[k]} />
            <MText x={924} y={y} s={`${LR(d[0])}쪽 → ${LR(d[1])}쪽`} size={32} weight={700} C={C} />
            <MText x={1130} y={y} s={`⇒ ‹${NAMES[FORK.holeOf2(d)]}›`} size={32} weight={800} opacity={seg(t, a + ROLL - 100, a + ROLL + 300)} C={C} />
          </g>
        );
      })}
      <MText x={880} y={520} s={`A ${FORK.WAYS[0]}가지 · B ‹${FORK.WAYS[1]}›가지 · C ${FORK.WAYS[2]}가지`} size={30} weight={700}
        opacity={seg(t, B.a.p3 + 1400, B.a.p3 + 2000) * (1 - seg(t, B.a.holes, B.a.holes + 400))} C={C} />
    </g>
  );
}

/** 구슬 4개 장: 물음 + 들어간 구멍 차례 */
function Question({ t, C, isM, landed, cols }) {
  const o = win(t, B.a.four + 200, B.a.calc + 400, 500, 500);
  if (o <= 0.01) return null;
  return (
    <g opacity={o}>
      <MText x={880} y={210} s="구슬 4개를 하나씩 굴릴 때" size={32} weight={800} C={C} />
      <MText x={880} y={262} s={isM ? "A·B·C에 모두 들어갈 확률은?" : "B에는 몇 개쯤 들어갈까요?"} size={32} weight={800} fill={C.gold} C={C} />
      {landed.map(({ k, pk, at }) => {
        const h = FORK.holeOf2(FORK.PATHS[pk]), x = 900 + k * 96;
        return (
          <g key={k} opacity={seg(t, at, at + 300)}>
            <circle cx={x + 22} cy={340} r={22} fill={cols[k]} />
            <text x={x + 22} y={348} fontSize={22} fontWeight={800} textAnchor="middle" fill={C.halo}>{k + 1}</text>
            <MText x={x + 22} y={412} s={NAMES[h]} size={40} weight={800} anchor="middle" fill={h === 1 && !isM ? C.gold : C.ink} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 중등: 모양 셋의 확률(표) */
function Calc({ t, C }) {
  const a = B.a.calc, o = seg(t, a + 300, a + 900);
  if (o <= 0.01) return null;
  const f = (p) => `{${p[0]}/${p[1]}}`;
  const pf = ["{1/4}", "{1/2}", "{1/4}"];
  const rows = [
    [{ s: "모양", color: "soft" }, { s: "순서", color: "soft" }, { s: "확률", color: "soft" }],
    ...FORK.SHAPES.map((sh, i) => {
      const tt = a + 1200 + i * 1300;
      const factors = sh.word.split("").map((ch) => pf["ABC".indexOf(ch)]).join("×");
      return [{ s: sh.word, t: tt, weight: 800 }, { s: `${sh.ord}가지`, t: tt + 300 }, { s: `${sh.ord} × ${factors} = ‹${f(sh.p)}›`, t: tt + 600, size: 25 }];
    }),
  ];
  return <Table x={872} y={170} cols={[136, 118, 420]} rh={[50, 74, 74, 74]} rows={rows} C={C} t={t} size={28} o={o} />;
}

/** 초등: 40개 막대 */
function Bars({ t, C }) {
  const o = seg(t, B.a.calc + 300, B.a.calc + 900);
  if (o <= 0.01) return null;
  const cnt = [0, 0, 0];
  FORK.E40.forEach((pk, i) => { if (t >= E0(i) + EROLL) cnt[FORK.holeOf2(FORK.PATHS[pk])]++; });
  const base = 470, px = 12;
  return (
    <g opacity={o}>
      <MText x={880} y={196} s="40개를 굴려 보면" size={30} weight={800} C={C} />
      <Path pts={[[900, base], [1440, base]]} stroke={C.ink} sw={2.6} />
      {cnt.map((v, k) => {
        const x = 960 + k * 170;
        return (
          <g key={k}>
            {v > 0 && <rect x={x} y={base - v * px} width={90} height={v * px} rx={4} fill={k === 1 ? C.gold : C.sky} fillOpacity={0.8} />}
            <MText x={x + 45} y={base - v * px - 10} s={`${v}개`} size={24} weight={800} anchor="middle" C={C} />
            <MText x={x + 45} y={base + 36} s={NAMES[k]} size={30} weight={800} anchor="middle" fill={C.soft} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 초등: 40개가 빠르게 굴러 구멍에 쌓인다(구멍 안 숫자) */
function Forty({ t, C, cols }) {
  if (t < B.a.calc + 1000) return null;
  const cnt = [0, 0, 0], out = [];
  FORK.E40.forEach((pk, i) => {
    const p = seg(t, E0(i), E0(i) + EROLL, E.lin);
    if (p <= 0) return;
    const h = FORK.holeOf2(FORK.PATHS[pk]);
    if (p >= 1) { cnt[h]++; return; }
    const [x, y] = along(pathPts(FORK.PATHS[pk]), p);
    out.push(<circle key={i} cx={x} cy={y} r={11} fill={cols[i % 4]} />);
  });
  return (
    <g>
      {out}
      {cnt.map((v, k) => v > 0 && (
        <MText key={k} x={HOLES[k][0]} y={HOLES[k][1] + 13} s={String(v)} size={36} weight={800} anchor="middle" fill={k === 1 ? C.gold : C.ink} C={C} />
      ))}
    </g>
  );
}

export default {
  key: "fork",
  dur: B.dur,
  title: { e: "두 갈래 길과 가능성", m: "두 갈래 길과 확률" },
  sub: { e: "초등 · 일이 일어날 가능성", m: "중2 · 확률의 계산(합의 법칙·곱의 법칙)" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
