// 서술형 1 — 「경로」 두 갈래 선로: 갈림목 네 곳이 제멋대로 움직일 때 빈 선로로 들어갈 확률
// 갈림목 A → B(위) · C(아래), B → ①(작업자 5명) · ②(빈 선로), C → ③(1명) · D, D → ④(빈 선로) · ⑤(2명). 갈림목마다 반반.
//   초등: 전차 8대를 보내 보면 ①②③ 2대씩, ④⑤ 1대씩 → 빈 선로 2 + 1 = 3대 → {3/8} (다섯 갈래라서 {2/5} 가 아니다)
//   중등: ② {1/2} × {1/2} = {1/4}, ④ {1/2} × {1/2} × {1/2} = {1/8} → {3/8}, 가능성이 같지 않으므로 {2/5} ✗
// 전차는 선로 끝 멈춤 표시 앞에서 선다(작업자에게 닿는 장면은 그리지 않는다).
import { beats, seg, win, E } from "../core";
import { Path } from "../draw";
import { UText, UBoard, UCaption, Chip, CircNum, Person } from "../kit-story";
import { Track, Tram, sCurve, polyInfo } from "../kit-essay";
import { RAILS as RL } from "../facts-essay";
import { ftxt } from "../facts-soccer";

const WRONG = ftxt(...RL.wrong);                          // {2/5}

const B = beats([["intro", 2400], ["rule", 4600], ["run", 9400], ["count", 6600], ["trap", 6800], ["hold", 2400]]);
const S0 = [64, 430], A = [214, 430], Bj = [400, 266], Cj = [400, 548], Dj = [586, 670];
const END = { 1: [790, 206], 2: [790, 330], 3: [790, 470], 4: [790, 610], 5: [790, 730] };
const STOP = 852;                                         // 멈춤 표시
const seg2 = (p, q) => [p, q];
const LEG = {
  SA: seg2(S0, A), AB: sCurve(A, Bj), AC: sCurve(A, Cj),
  B1: sCurve(Bj, END[1]), B2: sCurve(Bj, END[2]), C3: sCurve(Cj, END[3]), CD: sCurve(Cj, Dj),
  D4: sCurve(Dj, END[4]), D5: sCurve(Dj, END[5]),
};
const TAIL = (e) => [END[e], [STOP, END[e][1]]];
const join = (...parts) => parts.reduce((a, p) => (a.length ? [...a, ...p.slice(1)] : [...p]), []);
const ROUTE = { 1: join(LEG.SA, LEG.AB, LEG.B1, TAIL(1)), 2: join(LEG.SA, LEG.AB, LEG.B2, TAIL(2)), 3: join(LEG.SA, LEG.AC, LEG.C3, TAIL(3)),
  4: join(LEG.SA, LEG.AC, LEG.CD, LEG.D4, TAIL(4)), 5: join(LEG.SA, LEG.AC, LEG.CD, LEG.D5, TAIL(5)) };
const INFO = Object.fromEntries(Object.entries(ROUTE).map(([k, v]) => [k, polyInfo(v)]));
// 전차 i 가 가는 선로는 facts 에서(갈림목마다 정확히 반씩 나뉘게)
const TRAMS = Array.from({ length: RL.N }, (_, i) => {
  const e = RL.TRAM_ENDS[i];
  const k = RL.TRAM_ENDS.slice(0, i).filter((x) => x === e).length;   // 그 선로에 몇 번째로 들어오나
  return { i, e, k, t0: B.a.run + 300 + i * 760 };
});
const SPEED = 0.46;                                        // px/ms
const tramAt = (tr, t) => {
  const I = INFO[tr.e], stopAt = (I.L - 30 - tr.k * 52) / I.L;
  const k = Math.min(stopAt, ((t - tr.t0) * SPEED) / I.L);
  return k < 0 ? null : { ...I.at(E.out(Math.min(1, k / stopAt)) * stopAt), done: k >= stopAt };
};

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const netO = seg(t, 0, 800);
  const rule = win(t, B.a.rule + 200, B.b.rule + 200, 400, 400);
  const emptyHi = seg(t, B.a.count + 300, B.a.count + 900);
  const arrived = (e) => TRAMS.filter((tr) => tr.e === e && (tramAt(tr, t)?.done)).length;
  const probO = isM ? seg(t, B.a.run + 400, B.a.run + 1200) : 0;
  const endProb = (e) => (isM ? seg(t, B.a.run + 2200 + Number(e) * 500, B.a.run + 2700 + Number(e) * 500) : 0);
  return (
    <g>
      {/* 선로 */}
      <g opacity={netO}>
        {Object.entries(LEG).map(([k, pts]) => <Track key={k} pts={pts} C={C} />)}
        {Object.keys(END).map((e) => <Track key={"t" + e} pts={TAIL(e)} C={C}
          hi={RL.EMPTY.includes(e) && emptyHi > 0 ? C.gold : undefined} />)}
        {/* 빈 선로 강조 경로 */}
        {emptyHi > 0 && RL.EMPTY.map((e) => <Path key={"h" + e} pts={ROUTE[e]} stroke={C.gold} sw={24} o={0.16 * emptyHi} />)}
        {/* 멈춤 표시 */}
        {Object.values(END).map(([, y], i) => <g key={i}>
          <rect x={STOP + 4} y={y - 18} width={8} height={36} rx={3} fill={C.coral} />
        </g>)}
      </g>
      {/* 갈림목 */}
      {[["A", A], ["B", Bj], ["C", Cj], ["D", Dj]].map(([n, p]) => (
        <g key={n} opacity={netO}>
          <circle cx={p[0]} cy={p[1]} r={21} fill={C.paper} stroke={rule > 0 && n === "A" ? C.gold : C.ink} strokeWidth={rule > 0 && n === "A" ? 4 : 2.6} />
          <text x={p[0]} y={p[1] + 8} textAnchor="middle" fontSize={22} fontWeight={800} fill={C.ink} fontFamily="'Pretendard Variable', Pretendard, sans-serif">{n}</text>
        </g>
      ))}
      {/* 갈림목 규칙: 반반 */}
      {rule > 0 && <g opacity={rule}>
        <Chip x={A[0] + 74} y={A[1] - 92} s={isM ? "{1/2}" : "반반"} size={24} C={C} fill={C.gold} color={C.paper} />
        <Chip x={A[0] + 74} y={A[1] + 92} s={isM ? "{1/2}" : "반반"} size={24} C={C} fill={C.gold} color={C.paper} />
      </g>}
      {/* 중등: 갈래마다 1/2 */}
      {probO > 0 && <g opacity={probO}>
        {[[A, Bj], [A, Cj], [Bj, END[1]], [Bj, END[2]], [Cj, END[3]], [Cj, Dj], [Dj, END[4]], [Dj, END[5]]].map(([p, q], i) => {
          const m = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + (q[1] < p[1] ? -18 : 18)];
          return <UText key={i} x={m[0]} y={m[1] + 9} s="{1/2}" size={22} weight={700} anchor="middle" fill={C.teal} halo={C.halo} C={C} />;
        })}
      </g>}
      {/* 선로 끝: 번호 · 작업자 · 전차 수(초등) / 확률(중등) */}
      {Object.entries(END).map(([e, [, y]]) => {
        const n = RL.PEOPLE[e];
        const cnt = arrived(e);
        return (
          <g key={e} opacity={netO}>
            <CircNum x={STOP + 44} y={y} n={e} r={17} C={C} fill={RL.EMPTY.includes(e) && emptyHi > 0 ? C.gold : C.paper} />
            {n > 0 ? Array.from({ length: n }, (_, j) => <Person key={j} x={STOP + 96 + j * 22} y={y + 17} h={36} col={C.soft} C={C} />)
              : <UText x={STOP + 84} y={y + 8} s="빈 선로" size={22} weight={700} fill={C.soft} C={C} />}
            {n > 0 && <UText x={STOP + 96 + n * 22} y={y + 8} s={`${n}명`} size={20} weight={700} fill={C.soft} C={C} />}
            {!isM && cnt > 0 && <Chip x={END[e][0] - 40} y={y - 32} s={`${cnt}대`} size={22} C={C} fill={C.gold} color={C.paper} />}
            {isM && endProb(e) > 0 && <Chip x={END[e][0] - 40} y={y - 32} s={RL.M.prob(e)} size={22} C={C} o={endProb(e)} fill={C.teal} color={C.paper} />}
          </g>
        );
      })}
      {/* 전차 */}
      {TRAMS.map((tr) => {
        const s = tramAt(tr, t);
        return s && <Tram key={tr.i} x={s.p[0]} y={s.p[1]} ang={s.ang} C={C} col={C.gold} o={seg(t, tr.t0, tr.t0 + 200)} />;
      })}
      {/* 2/5 함정 */}
      <Trap t={t} C={C} isM={isM} />
      <UBoard x={1130} y={250} t={t} C={C} size={30} lh={56} lines={isM ? [
        { t: B.a.rule + 900, s: RL.M.half },
        { t: B.a.count + 900, s: RL.M.p[0] },
        { t: B.a.count + 2400, s: RL.M.p[1] },
        { t: B.a.count + 4000, s: RL.M.sum },
        { t: B.a.trap + 1200, s: RL.M.trap, size: 26 },
        { t: B.a.trap + 3400, s: RL.M.each },
      ] : [
        { t: B.a.run + 2600, s: RL.E.split },
        { t: B.b.run - 600, s: RL.E.ends },
        { t: B.a.count + 1200, s: RL.E.empty },
        { t: B.a.count + 3000, s: RL.E.ans },
        { t: B.a.trap + 1200, s: RL.E.trap },
        { t: B.a.trap + 3000, s: RL.E.why },
      ]} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: "브레이크가 고장 난 전차 — 갈림목 네 곳의 전환기도 모두 고장 났어요" },
        { t: B.a.rule, s: "갈림목마다 왼쪽과 오른쪽으로 같은 가능성으로 들어가요" },
        ...(isM ? [
          { t: B.a.run, s: "갈림목을 하나 지날 때마다 {1/2}씩 곱해요" },
          { t: B.a.count, s: `빈 선로로 들어갈 확률은 ${RL.M.sum.replace(/[‹›]/g, "")}` },
          { t: B.a.trap, s: `선로가 다섯 갈래니까 ${WRONG}? — 갈래마다 가능성이 달라요` },
          { t: B.a.trap + 3600, s: "경우의 수로 확률을 셀 때는 가능성이 같은 경우로 세어야 해요" },
        ] : [
          { t: B.a.run, s: `전차 ${RL.N}대를 차례로 보내 볼까요` },
          { t: B.a.count, s: `빈 선로로 들어간 전차는 ${RL.N}대 중 ${RL.nEmpty}대` },
          { t: B.a.trap, s: "선로가 다섯 갈래니까 5번 중 2번일까요?" },
          { t: B.a.trap + 3600, s: "갈래 수가 아니라 들어간 전차 수로 세어요" },
        ]),
      ]} />
    </g>
  );
}

function Trap({ t, C, isM }) {
  const a = seg(t, B.a.trap + 200, B.a.trap + 800) * (1 - seg(t, B.b.trap - 300, B.b.trap + 300));
  if (a <= 0) return null;
  const x = STOP + 44, y0 = END[1][1] - 34, y1 = END[5][1] + 34;
  const cross = seg(t, B.a.trap + 3000, B.a.trap + 3500);
  const s = isM ? `다섯 갈래 → ${WRONG}?` : "5갈래 중 2갈래?";
  return (
    <g opacity={a}>
      <rect x={x - 26} y={y0} width={52} height={y1 - y0} rx={26} fill="none" stroke={C.red} strokeWidth={3} strokeDasharray="10 8" />
      <UText x={x} y={y0 - 18} s={s} size={24} weight={750} anchor="middle" fill={C.red} halo={C.halo} C={C} />
      {cross > 0 && <Path pts={[[x - 96, y0 - 40], [x + 96, y0 - 14]]} stroke={C.red} sw={4} o={cross} />}
    </g>
  );
}

export default {
  key: "ess-rails",
  dur: B.dur,
  title: { e: "두 갈래 선로 — 8대를 보내 보면", m: "두 갈래 선로 — 빈 선로로 갈 확률" },
  sub: { e: "초등 · 일이 일어날 가능성 · 「경로」", m: "중2 · 확률의 곱과 합 · 「경로」" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
