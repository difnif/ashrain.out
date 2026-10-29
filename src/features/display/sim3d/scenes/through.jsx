// 3D 축구 3 — 마운트 → 하베르츠 쓰루패스 (2021-05-29 챔피언스리그 결승 맨시티 0−1 첼시, 42분)
// 2D 장면(scenes/soc-through.jsx)과 같은 수(facts-soccer.js 의 THROUGH). 패스한 곳 O(0, 0) · 하베르츠 출발 S(8, 19) · 만난 곳 M(24, 7).
// 공 1초에 12.5 m(2초), 하베르츠 1초에 8 m(2.5초) — 하베르츠가 0.5초 먼저 출발한다.
// 세계 좌표: O 를 (8, 6)에 두고 2D 의 x(상대 골대 쪽) → +X, y(2D 그림의 위) → −Z. 하베르츠는 그대로 에데르송을 제치고 빈 골문에 넣는다.
// 흐름: 마운트 뒤 눈높이 → 패스 순간 멈춤(설명 1: 줄자 · 두 직선의 교점) → 공과 하베르츠가 M 에서 만나는 순간 멈춤(설명 2: 시간)
//       → 에데르송을 제치고 골 → 옆에서 따라 달리며 다시 보기(초시계 둘) → 정리
import { timeline, ballPath, shots, makeWorld, smooth } from "../script.js";
import { frameCam } from "../persp.js";
import { Labels, Trail, GLine, GDot, GLabel, GSegLbl, GRight, GTape, Explain, Lower, Tag, GoalBurst, Panel, DK } from "../overlay.jsx";
import { ENTER, player, lerp3, drift, showO, mapKeys, dribble } from "../kit3d.js";
import { Stopwatch } from "../../kit-story.jsx";
import { seg, win, E, lerp, clamp, fmt } from "../../core.js";
import { THROUGH as TH } from "../../facts-soccer.js";

const W3 = ([x, y]) => [8 + x, 6 - y];
const O = W3(TH.pts.O), S = W3(TH.pts.S), M = W3(TH.pts.M);
const mv = (keys) => mapKeys(keys, W3);

/* ── 세계 시각(ms) ── */
const RUN0 = 2000, PASS = RUN0 + TH.lead * 1000, MEET = RUN0 + TH.tRun * 1000;   // 2000 · 2500 · 4500
const TOUCH = 5850, SHOT = 6320, IN = 6800, NET = 6960;

const CH = "final2021Chelsea", MC = "final2021City";
const MOUNT = player(CH, "마운트", "chelsea", "main", O, {
  keys: [[-9e4, 3.6, 9.6], [-1500, 3.6, 9.6], [1200, 6.4, 7.4], [2300, 7.6, 6.3], [PASS, ...O], [3400, 9.6, 5.6], [5200, 13.5, 4.8]],
  look: (tw, c) => (tw < PASS - 300 ? M : [c.ball[0], c.ball[2]]), acts: [{ kind: "pass", at: PASS, power: 0.8 }] });
const HAV = player(CH, "하베르츠", "chelsea", "main", S, {
  keys: [[-9e4, 13.0, -14.6], [0, 13.0, -14.6], [1200, 14.6, -13.8], [RUN0, ...S], [MEET, ...M],
    [5300, 38.6, -0.7], [TOUCH, 41.8, -0.6], [6050, 43.6, -2.1], [SHOT, 46.2, -3.1], [6900, 48.6, -2.6], [8200, 50.2, -1.0], [9800, 47.0, 6.0]],
  acts: [{ kind: "pass", at: TOUCH, power: 0.4, foot: "L" }, { kind: "pass", at: SHOT, power: 0.55 }, { kind: "cheer", from: 7300, to: 10400 }], seed: 1.1 });
const EDER = player(MC, "에데르송", "rivalKeeper", "rival", [51.2, 0], { deep: 0.7,
  keys: [[-9e4, 50.6, 0.4], [3200, 50.6, 0.4], [4600, 48.4, 0.0], [5500, 44.6, -0.4], [5800, 43.4, -0.6], [6600, 43.0, -0.8]],
  acts: [{ kind: "dive", at: 5900, dir: 1, h: 0.2 }] });
const ACTORS = [
  MOUNT, HAV,
  player(CH, "베르너", "chelsea", "mate", [27, 10], { keys: [[-9e4, 25, 8], [1000, 26.5, 9.5], [3500, 33.5, 13.5], [5200, 38, 15], [7000, 40, 14]] }),
  player(CH, "캉테", "chelsea", "mate", [-2, 4], { keys: [[-9e4, -4, 3], [3000, 0, 4], [6000, 6, 5]] }),
  player(CH, "조르지뉴", "chelsea", "mate", [-9, 11]),
  player(CH, "제임스", "chelsea", "mate", [11, 27], { keys: [[-9e4, 9, 27], [3000, 14, 27], [6000, 21, 26]] }),
  player(CH, "칠웰", "chelsea", "mate", [6, -27], { keys: [[-9e4, 4, -27], [3000, 9, -27], [6000, 15, -26]] }),
  player(CH, "아스필리쿠에타", "chelsea", "mate", [-20, 17]),
  player(CH, "크리스텐센", "chelsea", "mate", [-27, 3]),
  player(CH, "뤼디거", "chelsea", "mate", [-25, -9]),
  // 맨시티(회색): 2D 의 세 수비(진첸코 · 스톤스 · 디아스) + 그날 선발 — 자리는 짐작
  player(MC, "진첸코", "rival", "rival", W3([20.5, 15.6]), { keys: [[-9e4, ...W3([20.5, 15.6])], [2400, ...W3([20.5, 15.6])], [3400, ...W3([22.6, 12.8])], [MEET, ...W3([25.6, 10.4])], [5800, 38.6, -4.4], [7000, 44.5, -5.2]] }),
  player(MC, "스톤스", "rival", "rival", W3([15, 9.5]), { keys: [[-9e4, ...W3([15, 9.5])], [1800, ...W3([15, 9.5])], [3600, 28.4, 6.2], [5200, 34.5, 9.4], [7000, 39, 6.5]] }),
  player(MC, "디아스", "rival", "rival", W3([17.5, 1.8]), { keys: [[-9e4, ...W3([17.5, 1.8])], [1800, ...W3([17.5, 1.8])], [3600, 30.8, 9.8], [5200, 36.4, 11.4], [7000, 41, 8.2]] }),
  player(MC, "워커", "rival", "rival", [31, 19], { keys: [[-9e4, 31, 19], [3000, 32, 18], [6000, 38, 14]] }),
  player(MC, "귄도안", "rival", "rival", [12, -3], { keys: [[-9e4, 11, -2], [3000, 14, -4], [6000, 22, -6]] }),
  player(MC, "베르나르두", "rival", "rival", [4, 15], { keys: [[-9e4, 3, 15], [3000, 6, 13], [6000, 13, 11]] }),
  player(MC, "더브라위너", "rival", "rival", [-5, -8]),
  player(MC, "포든", "rival", "rival", [-3, 21]),
  player(MC, "마레즈", "rival", "rival", [-13, 27]),
  player(MC, "스털링", "rival", "rival", [-11, -22]),
  EDER,
];

/* ── 공 ── */
const BALL = ballPath([
  { t0: -1500, t1: PASS, kind: "fn", f: dribble(MOUNT, 0.6) },
  { t0: PASS, t1: MEET, kind: "ground", a: O, b: M },
  { t0: MEET, t1: TOUCH, kind: "fn", f: dribble(HAV, 0.7) },
  { t0: TOUCH, t1: SHOT, kind: "ground", a: [42.4, -0.7], b: [46.9, -3.3], ease: "slow" },
  { t0: SHOT, t1: IN, kind: "ground", a: [46.9, -3.3], b: [52.5, -0.8] },
  { t0: IN, t1: NET, kind: "ground", a: [52.5, -0.8], b: [54.25, -0.4], ease: "slow" },
]);
const net = (tw) => (tw >= NET - 50 ? { side: 1, y: 0.3, z: -0.4, k: tw - (NET - 50) } : null);

/* ── 박자표 ── */
const TL = timeline([
  { name: "intro", kind: "play", tw: [-3400, 1500], dur: 4900 },
  { name: "run", kind: "play", tw: [1500, PASS], dur: 1500, speed: "into" },
  { name: "ex1", kind: "hold", dur: 12600, spot: [MOUNT.id, HAV.id, "ball"] },
  { name: "meet", kind: "play", tw: [PASS, MEET], dur: 3000, speed: "both" },
  { name: "ex2", kind: "hold", dur: 12400, spot: [HAV.id, "ball"] },
  { name: "finish", kind: "play", tw: [MEET, 8600], dur: 4600, speed: "outof" },
  { name: "replay", kind: "play", tw: [1500, 4900], dur: 6600 },
  { name: "wrap", kind: "hold", dur: 7600, spot: [HAV.id, MOUNT.id, "ball"] },
]);
const A = TL.a, Bd = TL.b;
const twAt = (t) => TL.at(t).tw;

/* ── 카메라 ── */
// 설명 컷은 수학 그림처럼: x(상대 골대 쪽)가 화면 오른쪽, y 가 화면 위 — −Z 쪽을 내려다본다
const BOX = [900, 190, 1500, 740];
const EX = frameCam([O, S, M, W3([0, 25]), W3([32, 0])], { yaw: -90, pitch: 68, fov: 34, box: BOX });
const RET = 1300;
const CAM = shots([
  // 1. 마운트 뒤 눈높이 — 상대 골대 쪽을 본다
  { t0: 0, t1: A.ex1, cam: (k, t) => {
    const mp = MOUNT.tr.at(twAt(t));
    return { pos: [mp[0] - 4.2, 1.75, mp[1] + 3.0], at: lerp3([30, 1.2, -9], [29, 1.2, -9.5], E.sine(k)), fov: 42 };
  } },
  // 2. 설명 1
  { t0: A.ex1, t1: Bd.ex1 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k) },
  // 3. 패스 → 만남: 마운트 자리 뒤 눈높이(공은 멀어지고 하베르츠가 왼쪽에서 들어온다)
  { t0: Bd.ex1 - RET, t1: A.ex2, blend: RET, cam: (k) => ({ pos: lerp3([3.6, 1.75, 7.6], [5.0, 1.75, 7.0], E.sine(k)), at: [31, 1.1, -2.2], fov: 40 }) },
  // 4. 설명 2
  { t0: A.ex2, t1: Bd.ex2 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k, 0.04) },
  // 5. 마무리 — 골대 옆 눈높이: 에데르송을 제치고 빈 골문에
  { t0: Bd.ex2 - RET, t1: A.replay, blend: RET, cam: (k, t) => {
    const hp = HAV.tr.at(twAt(t));
    return { pos: lerp3([54.8, 1.62, 7.6], [55.0, 1.62, 6.8], E.sine(k)), at: [lerp(hp[0], 50, 0.25), 1.2, lerp(hp[1], -1, 0.3)], fov: 48 };
  } },
  // 6. 다시 보기 — 옆에서 함께 달리는 눈높이(왼쪽 터치라인 쪽)
  { t0: A.replay, t1: A.wrap, cam: (k, t) => {
    const tw = twAt(t), hp = HAV.tr.at(tw), b = BALL.at(tw);
    const cx = lerp(hp[0], b[0], 0.5);
    return { pos: [cx - 3, 1.75, -27.5], at: [cx + 1.5, 1.1, -4.5], fov: 32 };
  } },
  // 7. 정리
  { t0: A.wrap, t1: TL.dur, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k) },
]);

export const world = makeWorld({ tl: TL, actors: ACTORS, ball: BALL, cam: CAM, net });

/* ══════════ 글자 ══════════ */
const LOWER = [
  { t0: 700, t1: 4700, a: "2021. 5. 29. · 챔피언스리그 결승", b: "맨시티 0−1 첼시 — 전반 42분" },
  { t0: 5000, t1: A.ex1 - 200, b: "마운트의 쓰루패스 — 하베르츠는 벌써 달리고 있어요" },
  { t0: Bd.ex2 + 300, t1: A.replay - 300, b: "에데르송을 제치고 빈 골문에" },
  { t0: A.replay + 300, t1: A.wrap - 200, a: "다시 보기 · 옆에서 함께 달리며", b: "공은 1초에 12.5 m, 하베르츠는 1초에 8 m" },
];

function overlay(mode, t, C, P, W) {
  const isM = mode === "m";
  const { seg: Sg, local } = TL.at(t);
  const hold = Sg.kind === "hold";
  const dimK = smooth(0.05, 0.6, W.dim);
  const trailO = !hold && W.tw > PASS && W.tw < NET + 300 ? 0.8 : 0;
  const goalK = Sg.name === "finish" ? win(t, TL.tAt("finish", IN) + 100, TL.tAt("finish", IN) + 2400, 160, 600) : 0;
  const watch = Sg.name === "replay" ? win(t, A.replay + 200, A.wrap - 100, 400, 400) : 0;
  const sb = clamp((W.tw - PASS) / 1000, 0, TH.tBall), sh = clamp((W.tw - RUN0) / 1000, 0, TH.tRun);
  return (
    <g>
      <Trail W={W} pts={BALL.trail(W.tw, 420)} o={trailO} sw={4} />
      <Labels W={W} o={1 - dimK} />
      {hold && <Labels W={W} o={dimK} only={Sg.spot} />}
      {Sg.name === "ex1" && <Ex1 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "ex2" && <Ex2 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "wrap" && <Wrap W={W} l={local} d={Sg.dur} isM={isM} />}
      {watch > 0 && <g opacity={watch}>
        <Panel x={560} y={176} w={480} h={128} />
        <Stopwatch x={660} y={240} r={40} sec={sb} C={DK} col={DK.blue} label={`공 ${fmt(Math.round(sb * 10) / 10)}초`} />
        <Stopwatch x={900} y={240} r={40} sec={sh} C={DK} col={DK.coral} label={`하베르츠 ${fmt(Math.round(sh * 10) / 10)}초`} />
      </g>}
      <GoalBurst k={goalK} y={320} />
      <Lower t={t} items={LOWER} />
      <Tag o={1 - dimK} />
    </g>
  );
}

/** 점 이름 */
function Pts({ W, o, m }) {
  return (
    <g opacity={o}>
      <GLabel W={W} p={O} s="O" size={30} dx={-30} dy={24} col="#F7F1E1" />
      <GLabel W={W} p={S} s="S" size={30} dx={-30} dy={-10} col={DK.coral} />
      <GLabel W={W} p={M} s={m ? TH.M.mLab : "M"} size={28} dx={m ? 92 : 34} dy={22} />
    </g>
  );
}
/** 좌표평면(경기장 바닥) — O 가 원점, 4 m 눈금 */
function Axes({ W, o }) {
  if (o <= 0.01) return null;
  const out = [];
  for (let x = 4; x <= 32; x += 4) out.push(<GLine key={"x" + x} W={W} pts={[W3([x, -2]), W3([x, 25])]} col="#F7F1E1" sw={1.2} o={0.22} glow={false} n={6} />);
  for (let y = 4; y <= 24; y += 4) out.push(<GLine key={"y" + y} W={W} pts={[W3([-2, y]), W3([33, y])]} col="#F7F1E1" sw={1.2} o={0.22} glow={false} n={6} />);
  return (
    <g opacity={o}>
      {out}
      <GLine W={W} pts={[W3([-2, 0]), W3([34, 0])]} col="#F7F1E1" sw={3} glow={false} />
      <GLine W={W} pts={[W3([0, -2]), W3([0, 26])]} col="#F7F1E1" sw={3} glow={false} />
      <GLabel W={W} p={W3([34.6, 0])} s="x" size={34} chip={false} col="#F7F1E1" />
      <GLabel W={W} p={W3([0, 26.8])} s="y" size={34} chip={false} col="#F7F1E1" />
    </g>
  );
}
/* ── 설명 1: 줄자 · 두 직선의 교점 ── */
function Ex1({ W, l, d, isM }) {
  const o = showO(l, d);
  if (!isM) return (
    <g>
      <g opacity={o}>
        <GTape W={W} a={O} b={M} p={seg(l, 1000, 2600, E.io)} s={TH.E.tapeOM} side={1} col={DK.blue} />
        <GTape W={W} a={S} b={M} p={seg(l, 3800, 5200, E.io)} s={TH.E.tapeSM} side={-1} col={DK.coral} />
        <GDot W={W} p={M} col={DK.gold} r={0.7} fill={false} o={seg(l, 600, 1000)} sw={4} />
        <Pts W={W} o={seg(l, 400, 900)} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  줄자로 재기" head="공과 하베르츠는 M에서 만나요"
        lines={[{ t: 2600, s: TH.E.om }, { t: 5200, s: TH.E.sm }, { t: 7600, s: TH.E.v, size: 40 }]}
        foot="공이 떠나는 지금, 하베르츠는 벌써 S에서 달리고 있어요" />
    </g>
  );
  const ln = (f, x0, x1) => [W3([x0, f(x0)]), W3([x1, f(x1)])];
  return (
    <g>
      <g opacity={o}>
        <Axes W={W} o={seg(l, 300, 1000)} />
        <GLine W={W} pts={ln((x) => (7 / 24) * x, 0, 33)} p={seg(l, 1200, 2200)} col={DK.blue} sw={4} />
        <GLine W={W} pts={ln((x) => -(3 / 4) * x + 25, 0, 33)} p={seg(l, 2600, 3600)} col={DK.coral} sw={4} />
        <GLabel W={W} p={W3([30, 30 * 7 / 24])} s={TH.M.linePass} size={28} col={DK.blue} ink="#0b1430" dy={-34} o={seg(l, 2000, 2400)} />
        <GLabel W={W} p={W3([10, -0.75 * 10 + 25])} s={TH.M.lineRun} size={28} col={DK.coral} ink="#2a0e0a" dx={60} dy={-26} o={seg(l, 3400, 3800)} />
        <GDot W={W} p={M} col={DK.gold} r={0.7} fill={false} o={seg(l, 7400, 7900)} sw={4} />
        <Pts W={W} o={seg(l, 400, 900)} m={l > 8200} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  두 직선의 교점" head="패스 길과 달리는 길이 만나는 곳 M"
        lines={[{ t: 4600, s: TH.M.eq, size: 54 }, { t: 6400, s: `양변 × 24 : 7x = −18x + ${TH.run.b * 24}`, size: 46 }, { t: 8200, s: `x = 24,  y = 7  →  ‹${TH.M.mLab}›`, size: 50 }]}
        foot="O를 원점으로, 상대 골대 쪽이 x축 (단위 m)" />
    </g>
  );
}
/* ── 설명 2: 걸린 시간 ── */
function Ex2({ W, l, d, isM }) {
  const o = showO(l, d);
  const legs = isM;
  const F1 = W3([TH.pts.M[0], 0]), F2 = W3([TH.pts.M[0], TH.pts.S[1]]);
  return (
    <g>
      <g opacity={o}>
        <GLine W={W} pts={[O, M]} col={DK.blue} sw={5} />
        <GLine W={W} pts={[S, M]} col={DK.coral} sw={5} />
        {legs && <g>
          <GLine W={W} pts={[O, F1, M]} col={DK.gold} sw={3} dash="10 9" p={seg(l, 600, 1500)} glow={false} />
          <GRight W={W} V={F1} A={O} B={M} s={1.3} col={DK.gold} o={seg(l, 1300, 1700)} />
          <GSegLbl W={W} a={O} b={F1} s={TH.M.legs.om[0]} side={1} off={26} size={28} col={DK.gold} o={seg(l, 1300, 1700)} />
          <GSegLbl W={W} a={F1} b={M} s={TH.M.legs.om[1]} side={1} off={26} size={28} col={DK.gold} o={seg(l, 1300, 1700)} />
          <GLine W={W} pts={[S, F2, M]} col={DK.teal} sw={3} dash="10 9" p={seg(l, 2900, 3800)} glow={false} />
          <GRight W={W} V={F2} A={S} B={M} s={1.3} col={DK.teal} o={seg(l, 3600, 4000)} />
          <GSegLbl W={W} a={S} b={F2} s={TH.M.legs.sm[0]} side={-1} off={26} size={28} col={DK.teal} o={seg(l, 3600, 4000)} />
          <GSegLbl W={W} a={F2} b={M} s={TH.M.legs.sm[1]} side={-1} off={26} size={28} col={DK.teal} o={seg(l, 3600, 4000)} />
        </g>}
        <GSegLbl W={W} a={O} b={M} s={TH.E.tapeOM} side={-1} off={30} size={30} col={DK.blue} o={legs ? seg(l, 1900, 2300) : 1} />
        <GSegLbl W={W} a={S} b={M} s={TH.E.tapeSM} side={1} off={30} size={30} col={DK.coral} o={legs ? seg(l, 4100, 4500) : 1} />
        <Pts W={W} o={1} />
      </g>
      {isM ? (
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  피타고라스 → 시간" head="(시간) = (거리) ÷ (속력)"
          lines={[{ t: 1900, s: TH.M.om, size: 46 }, { t: 4100, s: TH.M.sm, size: 46 },
            { t: 6300, s: `공 ${fmt(TH.OM)} ÷ ${fmt(TH.vBall)} = ${fmt(TH.tBall)}(초)`, size: 46 },
            { t: 7600, s: `하베르츠 ${fmt(TH.SM)} ÷ ${fmt(TH.vRun)} = ${fmt(TH.tRun)}(초)`, size: 46 },
            { t: 9200, s: TH.M.lead, size: 52 }]} lh={80} />
      ) : (
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  걸린 시간" head="누가 얼마나 먼저 달려야 했을까?"
          lines={[{ t: 1600, s: TH.E.tb, size: 50 }, { t: 3800, s: TH.E.tr, size: 50 }, { t: 6400, s: TH.E.lead, size: 50 }]}
          foot="걸린 시간 = 간 거리 ÷ 1초에 가는 거리" />
      )}
    </g>
  );
}
/* ── 정리 ── */
function Wrap({ W, l, d, isM }) {
  const o = showO(l, d);
  return (
    <g>
      <g opacity={o}>
        <GLine W={W} pts={[O, M]} col={DK.blue} sw={5} p={seg(l, 400, 1200)} />
        <GLine W={W} pts={[S, M]} col={DK.coral} sw={5} p={seg(l, 400, 1200)} />
        <Pts W={W} o={seg(l, 300, 800)} m={isM} />
      </g>
      <Explain local={l} dur={d} kicker="정리" head="0.5초 먼저 달려야 M에서 만나요"
        lines={[{ t: 1400, s: `공 ‹${fmt(TH.tBall)}초›  ·  하베르츠 ‹${fmt(TH.tRun)}초›`, size: 54 },
          { t: 3000, s: "패스보다 먼저 시작한 달리기 — 오프 더 볼", size: 40, c: "soft" }]} />
    </g>
  );
}

export default { key: "soc-through", dur: TL.dur, world, overlay, tl: TL };
