// 장면 — 다섯 개 중에 고르기(초등 · 가능성) ↔ 5지선다, 어떻게 찍을까?(중2 · 확률)
// 보기 다섯 개(①~⑤) 아래 막대 = 그 보기가 답일 확률. 확실히 틀린 보기를 지울수록 남은 보기가 몫을 나눠 갖는다.
//   아무거나 {1/5} → 둘 지우면 {1/3} → 하나 더 지우면 {1/2}. 지울 때마다: 20 → 25 → 33.3 → 50 %
//   몬티홀과 다른 점: 시험지에는 답을 알고 지워 주는 사회자가 없다 → 처음 찍은 답을 바꿔도 {1/2} 그대로
//   4점짜리 5문제를 모두 찍으면: 학생 200명(결정적)의 맞힌 수 — 평균 5 × (확률) 문제
import { beats, seg, win, E, lerp } from "../core";
import { Board, Caption, MText, Path } from "../draw";
import { PICK5, fracS, pctS } from "../guess.js";

const B = beats([
  ["intro", 3000], ["p5", 4200], ["p3", 5400], ["p2", 5000], ["ladder", 5600], ["monty", 8800], ["many", 10400], ["sum", 6200], ["hold", 1800],
]);
const OPT = ["1", "2", "3", "4", "5"];
const BX = (i) => 150 + i * 132, BY = 318, BR = 46;
const BAR = { base: 680, h: 360 };                            // 확률 1 → 360px(막대는 {1/2}까지)
// 지우는 차례: ④ ⑤ (둘) → ① (하나 더). 남는 보기 ② ③
const CROSS = [[3, B.a.p3 + 900], [4, B.a.p3 + 1700], [0, B.a.p2 + 900]];

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const o = seg(t, 200, 1100);
  const dimL = 1 - 0.65 * seg(t, B.a.many, B.a.many + 600) * (1 - seg(t, B.a.sum, B.a.sum + 600));
  const crossed = (i) => { const c = CROSS.find(([k]) => k === i); return c ? seg(t, c[1], c[1] + 450, E.out) : 0; };
  // 그 보기가 답일 확률 — 하나 지울 때마다 0.9초에 걸쳐 남은 보기들이 몫을 나눠 갖는다
  const pOf = (i) => {
    let v = 1 / 5;
    const alive = [true, true, true, true, true];
    for (const [k, ct] of CROSS) {
      const a = ct + 450;
      if (t < a) break;
      const before = alive[i] ? 1 / alive.filter(Boolean).length : 0;
      alive[k] = false;
      const after = alive[i] ? 1 / alive.filter(Boolean).length : 0;
      v = lerp(before, after, seg(t, a, a + 900, E.io));
    }
    return v;
  };
  const barsO = seg(t, B.a.p5 + 300, B.a.p5 + 900);
  const firstPick = win(t, B.a.monty + 600, B.a.many, 400, 500);
  const swapA = seg(t, B.a.monty + 3000, B.a.monty + 3900);
  return (
    <g>
      <g opacity={o * dimL}>
        {/* 문제 카드 */}
        <rect x={70} y={146} width={690} height={84} rx={14} fill={C.card} stroke={C.cardEdge} strokeWidth={2} />
        <MText x={98} y={200} s={isM ? "문제 7. 다음 중 옳은 것은? [4점]" : "문제 7. 알맞은 것을 고르세요."} size={30} weight={700} C={C} />
        {OPT.map((s, i) => {
          const x = BX(i), cr = crossed(i), v = pOf(i), h = v * BAR.h;
          const pick = i === 1 ? firstPick : 0;
          return (
            <g key={i}>
              <circle cx={x} cy={BY} r={BR} fill={C.card} stroke={pick > 0.01 ? C.sky : C.ink} strokeWidth={pick > 0.01 ? 5 : 3} opacity={1 - 0.55 * cr} />
              <text x={x} y={BY + 15} fontSize={42} fontWeight={800} textAnchor="middle" fill={C.ink} opacity={1 - 0.55 * cr}>{s}</text>
              {cr > 0 && <g opacity={0.95}>
                <Path pts={[[x - 34, BY - 34], [x - 34 + 68 * Math.min(1, cr * 2), BY - 34 + 68 * Math.min(1, cr * 2)]]} stroke={C.coral} sw={7} />
                {cr > 0.5 && <Path pts={[[x + 34, BY - 34], [x + 34 - 68 * (cr * 2 - 1), BY - 34 + 68 * (cr * 2 - 1)]]} stroke={C.coral} sw={7} />}
              </g>}
              {pick > 0.01 && <MText x={x} y={BY - BR - 10} s={isM ? "처음 찍은 답" : "처음 고른 것"} size={22} weight={800} anchor="middle" fill={C.sky} opacity={pick} C={C} />}
              {/* 확률 막대 */}
              <g opacity={barsO}>
                <line x1={x - 50} x2={x + 50} y1={BAR.base} y2={BAR.base} stroke={C.ink} strokeWidth={2.4} opacity={0.8} />
                {h > 0.5 && <rect x={x - 30} y={BAR.base - h} width={60} height={h} rx={4} fill={C.gold} fillOpacity={0.85} />}
                <MText x={x} y={BAR.base - h - 12} s={v > 0.001 ? labelOf(v) : "0"} size={30} weight={800} anchor="middle" fill={C.gold} halo={C.halo} C={C} />
              </g>
            </g>
          );
        })}
        {/* 바꾸기 화살표(몬티홀 장면) */}
        {swapA > 0.01 && <g opacity={win(t, B.a.monty + 3000, B.a.many, 400, 500)}>
          <Path pts={[[BX(1) + 20, BY + BR + 18], [BX(1) + 66, BY + BR + 46], [BX(2) - 20, BY + BR + 18]]} stroke={C.sky} sw={4} dash="8 6" />
          <MText x={(BX(1) + BX(2)) / 2} y={BY + BR + 84} s="바꿀까?" size={24} weight={800} anchor="middle" fill={C.sky} C={C} />
        </g>}
      </g>
      <MText x={100} y={BAR.base + 38} s={isM ? "↑ 그 보기가 답일 확률" : "↑ 답일 가능성"} size={22} weight={700} fill={C.soft} opacity={barsO * dimL} C={C} />
      {/* 오른쪽 */}
      <Ladder t={t} C={C} isM={isM} />
      <MontyNote t={t} C={C} isM={isM} />
      <Many t={t} C={C} isM={isM} />
      <Board x={900} y={isM ? 690 : 690} t={t} C={C} size={29} lh={50} lines={isM ? [
        { t: B.a.sum + 300, s: "확실히 틀린 보기를 하나라도 더 지우기", row: 0 },
        { t: B.a.sum + 1500, s: "남은 보기끼리는 어느 것을 골라도 같은 확률", row: 1 },
      ] : [
        { t: B.a.sum + 300, s: "틀린 보기를 하나라도 더 지우기", row: 0 },
        { t: B.a.sum + 1500, s: "남은 것끼리는 가능성이 똑같아요", row: 1 },
      ]} />
      <Caption t={t} C={C} y={862} size={33} caps={isM ? [
        { t: 300, s: "5지선다, 답을 모를 때 어떻게 찍는 것이 좋을까요?" },
        { t: B.a.p5 + 300, s: "아무것도 모르면 다섯 보기 모두 {1/5} — 20%" },
        { t: B.a.p3 + 400, s: "확실히 틀린 보기 둘을 지우면 남은 셋이 몫을 나눠 {1/3}" },
        { t: B.a.p2 + 400, s: "하나 더 지우면 둘 중 하나 — {1/2}" },
        { t: B.a.ladder + 300, s: "보기를 하나 지울 때마다 맞힐 확률이 커져요" },
        { t: B.a.monty + 300, s: "그럼 몬티홀처럼, 처음 찍은 답을 바꾸면 더 좋을까요?" },
        { t: B.a.monty + 4400, s: "시험지에는 답을 알고 지워 준 사회자가 없어요 — 바꿔도 {1/2}" },
        { t: B.a.many + 300, s: `4점짜리 ${PICK5.Q}문제를 모두 찍는다면? 학생 ${PICK5.STUDENTS}명이 해 보면` },
        { t: B.a.many + 5600, s: "평균적으로 맞히는 문제 수 = 문제 수 × 확률" },
        { t: B.a.sum + 300, s: "찍기의 핵심은 '고르기'보다 '지우기'예요" },
      ] : [
        { t: 300, s: "다섯 개 중에서 답을 골라야 할 때" },
        { t: B.a.p5 + 300, s: "아무거나 고르면 5개 중 1개 — 맞힐 가능성이 작아요" },
        { t: B.a.p3 + 400, s: "확실히 아닌 것 두 개를 지우면 3개 중 1개" },
        { t: B.a.p2 + 400, s: "하나 더 지우면 2개 중 1개 — 반반이에요" },
        { t: B.a.ladder + 300, s: "하나씩 지울수록 맞힐 가능성이 커져요" },
        { t: B.a.monty + 300, s: "처음 고른 것을 바꾸면 더 좋을까요?" },
        { t: B.a.monty + 4400, s: "남은 두 개는 가능성이 똑같아요 — 바꿔도 반반" },
        { t: B.a.many + 300, s: `${PICK5.Q}문제를 모두 고른다면? ${PICK5.STUDENTS}명이 해 보면` },
        { t: B.a.many + 5600, s: "두 개로 줄여서 고른 사람들이 가장 많이 맞혔어요" },
        { t: B.a.sum + 300, s: "고르기 전에 지우기!" },
      ]} />
    </g>
  );
}
/** 확률 글자: 1/5 · 1/3 · 1/2 · 1/4 */
function labelOf(v) {
  for (const k of [2, 3, 4, 5]) if (Math.abs(v - 1 / k) < 1e-6) return `{1/${k}}`;
  return "";
}

/** 지울수록: 남은 보기 5 · 4 · 3 · 2 → 20 · 25 · 33.3 · 50 % (계단) */
function Ladder({ t, C, isM }) {
  const o = win(t, B.a.ladder + 200, B.a.monty, 500, 500);
  if (o <= 0.01) return null;
  const x0 = 930, base = 560;
  return (
    <g opacity={o}>
      <MText x={x0} y={196} s={isM ? "남은 보기 수와 맞힐 확률" : "남은 개수와 맞힐 가능성"} size={28} weight={800} C={C} />
      <Path pts={[[x0, base], [x0 + 560, base]]} stroke={C.ink} sw={2.6} />
      {PICK5.LEFT.map((k, i) => {
        const v = 1 / k, h = v * 600, x = x0 + 30 + i * 135, a = seg(t, B.a.ladder + 500 + i * 600, B.a.ladder + 900 + i * 600);
        return (
          <g key={k} opacity={a}>
            <rect x={x} y={base - h} width={90} height={h} rx={4} fill={C.gold} fillOpacity={0.35 + 0.15 * i} />
            <MText x={x + 45} y={base - h - 46} s={fracS(PICK5.P[i])} size={28} weight={800} anchor="middle" C={C} />
            <MText x={x + 45} y={base - h - 12} s={pctS(v)} size={22} weight={700} anchor="middle" fill={C.gold} C={C} />
            <MText x={x + 45} y={base + 32} s={`${k}개`} size={24} weight={700} anchor="middle" fill={C.soft} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 몬티홀과 다른 점 */
function MontyNote({ t, C, isM }) {
  const o = win(t, B.a.monty + 200, B.a.many, 500, 500);
  if (o <= 0.01) return null;
  const card = (y, head, lines, col, at) => (
    <g opacity={seg(t, at, at + 500)}>
      <rect x={910} y={y} width={620} height={176} rx={16} fill={col} fillOpacity={0.12} stroke={col} strokeWidth={2.5} />
      <MText x={936} y={y + 46} s={head} size={28} weight={800} fill={col} C={C} />
      {lines.map((s, i) => <MText key={i} x={936} y={y + 94 + i * 44} s={s} size={26} weight={600} C={C} />)}
    </g>
  );
  return (
    <g opacity={o}>
      {card(170, "몬티홀", isM ? ["답을 아는 사회자가 염소 문만 골라 연다", "→ 남은 문으로 정보가 모인다: 바꾸면 유리"] : ["답을 아는 사회자가 문을 열어 줘요", "→ 바꾸면 유리해요"], C.coral, B.a.monty + 1200)}
      {card(380, "시험지", isM ? ["내가 모르는 채로 지웠다 — 2번과 3번은 같은 처지", "→ 바꿔도 {1/2}, 그대로도 {1/2}"] : ["내가 지웠어요 — 남은 둘은 똑같아요", "→ 바꿔도 반반, 그대로도 반반"], C.sky, B.a.monty + 4200)}
    </g>
  );
}

/** 5문제를 모두 찍는다면 — 방법마다 학생 200명의 맞힌 수(막대)와 평균 */
function Many({ t, C, isM }) {
  const o = win(t, B.a.many + 200, B.a.sum + 300, 500, 500);
  if (o <= 0.01) return null;
  const names = isM ? ["아무거나({1/5})", "셋 중 하나({1/3})", "둘 중 하나({1/2})"] : ["아무거나", "셋 중 하나", "둘 중 하나"];
  const cols = [C.soft, C.teal, C.gold];
  return (
    <g opacity={o}>
      <MText x={900} y={190} s={`${PICK5.Q}문제를 모두 찍은 학생 ${PICK5.STUDENTS}명 — 맞힌 문제 수`} size={26} weight={800} C={C} />
      {PICK5.sims.map((sim, si) => {
        const y0 = 230 + si * 150, base = y0 + 104, a = seg(t, B.a.many + 700 + si * 1300, B.a.many + 1500 + si * 1300);
        const grow = seg(t, B.a.many + 700 + si * 1300, B.a.many + 2300 + si * 1300, E.out);
        const mx = Math.max(...sim.hist);
        return (
          <g key={si} opacity={a}>
            <MText x={900} y={y0 + 40} s={names[si]} size={23} weight={800} fill={cols[si]} C={C} />
            <Path pts={[[1100, base], [1440, base]]} stroke={C.ink} sw={2} />
            {sim.hist.map((v, j) => {
              const h = (v / mx) * 88 * grow;
              return (
                <g key={j}>
                  {h > 0.5 && <rect x={1108 + j * 56} y={base - h} width={42} height={h} rx={3} fill={cols[si]} fillOpacity={0.8} />}
                  <MText x={1129 + j * 56} y={base + 22} s={String(j)} size={17} weight={600} anchor="middle" fill={C.soft} C={C} />
                </g>
              );
            })}
            <MText x={1460} y={y0 + 56} s={`평균`} size={19} weight={700} fill={C.soft} C={C} />
            <MText x={1460} y={y0 + 90} s={`‹${sim.avg.toFixed(1)}›`} size={30} weight={800} C={C} />
            {isM && <MText x={1460} y={y0 + 118} s={`≈ ${Math.round(sim.avg * PICK5.PTS * 10) / 10}점`} size={18} weight={600} fill={C.soft} C={C} />}
          </g>
        );
      })}
      {isM && <MText x={900} y={712} s={`이론 평균: 5 × {1/5} = 1 · 5 × {1/3} ≈ 1.7 · 5 × {1/2} = 2.5`} size={22} weight={700} fill={C.soft}
        opacity={seg(t, B.a.many + 5600, B.a.many + 6200)} C={C} />}
    </g>
  );
}

export default {
  key: "pick5",
  dur: B.dur,
  title: { e: "다섯 개 중에서 고르기", m: "5지선다, 어떻게 찍을까?" },
  sub: { e: "초등 · 일이 일어날 가능성", m: "중2 · 확률의 뜻과 계산" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
