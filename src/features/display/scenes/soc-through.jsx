// 축구 3 — 마운트 → 하베르츠 쓰루패스 (2021-05-29 챔피언스리그 결승 첼시 1−0 맨시티, 42분)
// 마운트가 패스한 곳 O, 하베르츠가 출발한 곳 S(8, 19), 공을 받은 곳 M. 공 1초에 12.5 m, 하베르츠 1초에 8 m.
//   초등: 줄자 25 m · 20 m → 25 ÷ 12.5 = 2초, 20 ÷ 8 = 2.5초 → 0.5초 먼저 출발
//   중등: 두 직선 y = 7/24 x, y = −3/4 x + 25 의 교점 M(24, 7) → OM 25, SM 20(피타고라스) → 0.5초
// 달리기는 2배 느린 그림으로 보여 준다(1초 = 2초). 초시계는 실제 초를 센다.
import { beats, seg, win, E, mix2, fmt, clamp } from "../core";
import { Path, RightMark } from "../draw";
import { UText, UBoard, UCaption, Tape, Chip, SegLbl, Stopwatch } from "../kit-story";
import { mapper, Grass, Player, Rival, Ball, DirNote } from "../kit-soccer";
import { THROUGH as TH, who } from "../facts-soccer";

const B = beats([["intro", 2400], ["play", 6800], ["lines", 6400], ["dist", 5600], ["time", 6600], ["replay", 6600], ["hold", 2200]]);
const MP = mapper({ ox: 130, oy: 680, s: 20, flipY: true });
const GR = [-3, -4, 33, 25];
const O = MP.p(TH.pts.O), S = MP.p(TH.pts.S), M = MP.p(TH.pts.M);
const MOUNT = MP.p([-1.3, -0.9]);                    // 공(O) 바로 뒤
const SLOW = 2000;                                     // 실제 1초 = 그림 2초
const GOALWARD = MP.p([31, 7.6]);
// 회색 = 맨시티 수비(그날 선발): 하베르츠를 늦게 따라간 진첸코, 베르너에게 끌려 나간 스톤스·디아스 — 자리는 다듬은 값
const DEF = TH.defenders.map((q, i) => ({ p: MP.p(q), id: who("final2021City", ["스톤스", "디아스", "진첸코"][i]), lp: ["r", "r", "r"][i] }));
const RUNS = [B.a.play + 700, B.a.replay + 500];       // 하베르츠가 달리기 시작하는 시각

/** 하베르츠 · 공 위치와 지난 실제 초 */
function state(t) {
  let base = null;
  for (const r of RUNS) if (t >= r - 700 && t < r + TH.tRun * SLOW + 1300) base = r;
  if (base == null) return { hv: S, ball: O, run: false, sb: t >= B.a.time + 3000 ? TH.tBall : 0, sh: t >= B.a.time + 3000 ? TH.tRun : 0 };
  const sec = (t - base) / SLOW;
  const end = TH.tRun;
  let hv, ball;
  if (sec <= 0) hv = S;
  else if (sec < end) hv = mix2(S, M, sec / end);
  else hv = mix2(M, GOALWARD, clamp((sec - end) / 0.55));
  if (sec < TH.lead) ball = O;
  else if (sec < end) ball = mix2(O, M, (sec - TH.lead) / TH.tBall);
  else ball = [hv[0] + 14, hv[1] + 6];
  return { hv, ball, run: true, sec, sb: clamp(sec - TH.lead, 0, TH.tBall), sh: clamp(sec, 0, TH.tRun) };
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const pitchO = seg(t, 0, 700);
  const st = state(t);
  // 재생이 끝나면 잠깐 사라졌다가 출발 자리에 다시
  const resetO = 1 - win(t, B.b.play - 400, B.a.lines + 300, 300, 300) * 0.999;
  const playersO = seg(t, 400, 1200) * (st.run ? 1 : resetO);
  const mDot = seg(t, B.a.lines + 200, B.a.lines + 700);
  const axesO = isM ? seg(t, B.a.lines, B.a.lines + 700) : 0;
  const lineO = isM ? seg(t, B.a.lines + 600, B.a.lines + 1600) : 0;
  const tape1 = seg(t, B.a.lines + 500, B.a.lines + 1700, E.io), tape2 = seg(t, B.a.lines + 2600, B.a.lines + 3600, E.io);
  const legs1 = isM ? seg(t, B.a.dist + 200, B.a.dist + 900) : 0, legs2 = isM ? seg(t, B.a.dist + 2400, B.a.dist + 3100) : 0;
  const watchO = seg(t, B.a.play + 300, B.a.play + 900);
  const pathsO = seg(t, B.a.lines, B.a.lines + 600);
  return (
    <g>
      <g opacity={pitchO}>
        <Grass M={MP} rect={GR} C={C} band={4} along="x" />
        <DirNote x={MP.p([GR[0], 0])[0] + 2} y={MP.p([0, GR[3]])[1] - 12} s="위치는 실제 장면을 바탕으로 다듬은 값 · 흐린 선수는 그날 선발, 자리는 짐작" anchor="start" size={18} C={C} />
        <DirNote x={MP.p([31.6, -2.6])[0]} y={MP.p([31.6, -2.6])[1]} s="상대 골대 쪽 →" anchor="end" C={C} />
      </g>
      {/* 중등: 좌표축과 두 직선 */}
      {axesO > 0 && <g opacity={axesO}>
        {Array.from({ length: 8 }, (_, i) => (i + 1) * 4).map((x) => <Path key={"gx" + x} pts={[MP.p([x, -3]), MP.p([x, 24])]} stroke={C.ink} sw={1} o={0.12} />)}
        {Array.from({ length: 6 }, (_, i) => (i + 1) * 4).map((y) => <Path key={"gy" + y} pts={[MP.p([-2, y]), MP.p([32, y])]} stroke={C.ink} sw={1} o={0.12} />)}
        <Path pts={[MP.p([-2, 0]), MP.p([32.4, 0])]} stroke={C.ink} sw={2.4} />
        <Path pts={[MP.p([0, -3]), MP.p([0, 24.4])]} stroke={C.ink} sw={2.4} />
        <UText x={MP.p([32.6, 0])[0] + 4} y={MP.p([32.6, 0])[1] + 9} s="x" size={28} C={C} />
        <UText x={MP.p([0, 24.4])[0] + 10} y={MP.p([0, 24.4])[1] + 8} s="y" size={28} C={C} />
        <UText x={O[0] - 14} y={O[1] + 30} s="O" size={24} weight={700} anchor="end" C={C} />
      </g>}
      {lineO > 0 && <g opacity={lineO}>
        <Path pts={[MP.p([0, 0]), MP.p([32, (32 * 7) / 24])]} stroke={C.blue} sw={2.6} o={0.8} />
        <Path pts={[MP.p([0, 25]), MP.p([32, 1])]} stroke={C.coral} sw={2.6} o={0.8} />
        <Chip x={MP.p([28.6, 10.6])[0]} y={MP.p([28.6, 10.6])[1]} s={TH.M.linePass} size={24} C={C} fill={C.paper} color={C.blue} stroke={C.blue} />
        <Chip x={MP.p([18.8, 13.0])[0]} y={MP.p([18.8, 13.0])[1]} s={TH.M.lineRun} size={24} C={C} fill={C.paper} color={C.coral} stroke={C.coral} />
      </g>}
      {/* 지나간 길 */}
      {pathsO > 0 && <g opacity={pathsO}>
        <Path pts={[O, M]} stroke={C.ink} sw={3} dash="10 9" o={0.7} />
        <Path pts={[S, M]} stroke={C.ink} sw={3} dash="4 8" o={0.7} />
      </g>}
      {/* 중등: 직각삼각형 다리 */}
      {legs1 > 0 && <g opacity={legs1}>
        <Path pts={[O, MP.p([TH.pts.M[0], 0]), M]} stroke={C.gold} sw={2.6} dash="8 7" />
        <RightMark V={MP.p([TH.pts.M[0], 0])} A={O} B={M} s={14} C={C} color={C.gold} />
        <SegLbl P={O} Q={MP.p([TH.pts.M[0], 0])} s={TH.M.legs.om[0]} side={-1} off={20} C={C} size={26} fill={C.gold} />
        <SegLbl P={MP.p([TH.pts.M[0], 0])} Q={M} s={TH.M.legs.om[1]} side={-1} off={20} C={C} size={26} fill={C.gold} />
      </g>}
      {legs2 > 0 && <g opacity={legs2}>
        <Path pts={[S, MP.p([TH.pts.M[0], TH.pts.S[1]]), M]} stroke={C.teal} sw={2.6} dash="8 7" />
        <RightMark V={MP.p([TH.pts.M[0], TH.pts.S[1]])} A={S} B={M} s={14} C={C} color={C.teal} />
        <SegLbl P={S} Q={MP.p([TH.pts.M[0], TH.pts.S[1]])} s={TH.M.legs.sm[0]} side={1} off={20} C={C} size={26} fill={C.teal} />
        <SegLbl P={MP.p([TH.pts.M[0], TH.pts.S[1]])} Q={M} s={TH.M.legs.sm[1]} side={1} off={22} C={C} size={26} fill={C.teal} />
      </g>}
      {/* M 표시 */}
      {mDot > 0 && <g opacity={mDot}>
        <circle cx={M[0]} cy={M[1]} r={9} fill="none" stroke={C.gold} strokeWidth={3.4} />
        <Chip x={M[0] + 48} y={M[1] + 38} s={isM ? TH.M.mLab : "M"} size={24} C={C} fill={C.paper} color={C.ink} stroke={C.gold} />
      </g>}
      {isM && mDot > 0 && <Chip x={S[0] - 84} y={S[1] + 2} s={TH.M.sLab} size={22} C={C} o={mDot} fill={C.paper} color={C.ink} stroke={C.ink} />}
      {/* 선수 */}
      {DEF.map((q, i) => <Rival key={i} x={q.p[0]} y={q.p[1]} C={C} o={seg(t, 400, 1200)} n={q.id[0]} name={q.id[1]} lp={q.lp} />)}
      <Player x={MOUNT[0]} y={MOUNT[1]} n={19} team="chelsea" C={C} o={seg(t, 400, 1200)} label="마운트" lp="b" lsize={22} r={21} />
      <Player x={st.hv[0]} y={st.hv[1]} n={29} team="chelsea" C={C} o={playersO} label="하베르츠" lp="r" lsize={22} r={21} />
      <Ball x={st.ball[0]} y={st.ball[1]} h={0} C={C} o={playersO} />
      {/* 초등: 줄자 */}
      {!isM && <Tape a={O} b={M} p={tape1} pxPerM={MP.s} C={C} read={TH.E.tapeOM} side={1} />}
      {!isM && <Tape a={S} b={M} p={tape2} pxPerM={MP.s} C={C} read={TH.E.tapeSM} side={-1} />}
      {/* 초시계(실제 초) */}
      <g opacity={watchO}>
        <Stopwatch x={936} y={700} r={34} sec={st.sb} C={C} col={C.blue} label={`공 ${fmt(Math.round(st.sb * 10) / 10)}초`} />
        <Stopwatch x={1146} y={700} r={34} sec={st.sh} C={C} col={C.coral} label={`하베르츠 ${fmt(Math.round(st.sh * 10) / 10)}초`} />
      </g>
      <UBoard x={880} y={232} t={t} C={C} size={30} lh={54} lines={isM ? [
        { t: B.a.lines + 1700, s: TH.M.eq },
        { t: B.a.lines + 3400, s: TH.M.sol },
        { t: B.a.dist + 1000, s: TH.M.om },
        { t: B.a.dist + 3200, s: TH.M.sm },
        { t: B.a.time + 600, s: TH.M.t },
        { t: B.a.time + 3000, s: TH.M.lead },
      ] : [
        { t: B.a.lines + 1700, s: TH.E.om },
        { t: B.a.lines + 3600, s: TH.E.sm },
        { t: B.a.dist + 600, s: TH.E.v },
        { t: B.a.time + 600, s: TH.E.tb },
        { t: B.a.time + 1800, s: TH.E.tr },
        { t: B.a.time + 3000, s: TH.E.lead },
      ]} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: "2021년 5월 29일 챔피언스리그 결승 — 첼시 1−0 맨시티" },
        { t: B.a.play, s: "전반 42분, 마운트의 쓰루패스를 하베르츠가 달려 들어가 받았어요" },
        { t: B.a.play + 3600, s: "하베르츠는 공보다 먼저 달리기 시작했어요 — 얼마나 먼저?" },
        ...(isM ? [
          { t: B.a.lines, s: "공을 받은 곳 M은 두 직선의 교점 — 연립방정식으로 찾아요" },
          { t: B.a.dist, s: "O와 S에서 M까지의 거리 — 피타고라스 정리" },
          { t: B.a.time, s: "(시간) = (거리) ÷ (속력)" },
        ] : [
          { t: B.a.lines, s: "공과 하베르츠가 지나간 길을 줄자로 재요" },
          { t: B.a.dist, s: `공은 1초에 ${fmt(TH.vBall)} m, 하베르츠는 1초에 ${fmt(TH.vRun)} m를 가요` },
          { t: B.a.time, s: "걸린 시간 = 간 거리 ÷ 1초에 가는 거리" },
        ]),
        { t: B.a.replay, s: `하베르츠가 ${fmt(TH.lead)}초 먼저 출발해야 공과 M에서 만나요` },
      ]} />
    </g>
  );
}

export default {
  key: "soc-through",
  dur: B.dur,
  title: { e: "쓰루패스 — 누가 먼저 달려야 할까", m: "쓰루패스 — 두 직선의 교점" },
  sub: { e: "초등 · 속력과 시간 · 2021 챔피언스리그 결승", m: "중2 · 일차함수의 교점과 피타고라스 정리 · 2021 챔피언스리그 결승" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
