// 3D 축구 5 — 박지성 · 루니 · 호날두 역습 (2009-05-05 챔피언스리그 준결승 2차전 아스널 1−3 맨유, 61분)
// 2D 장면(scenes/soc-counter.jsx)과 같은 수(facts-soccer.js 의 COUNTER). 박지성 O(0, 0) · 루니 R(48, 36) · 호날두 슈팅 C(63, 16).
// 공 O → R → C(60 + 25 = 85 m), 호날두 O → C(65 m) — 공이 20 m 더 움직였어도 패스가 달리기보다 빨랐다.
// 세계 좌표: 2D 의 x(상대 골대 쪽) → +X, y(2D 그림의 위) → −Z, O 를 (−21.5, 12)에 둔다 — 골문(74, 12)이 오른쪽 골대 가운데.
// 흐름: 호날두 → 박지성(눈높이) → 함께 달리는 카메라 → 루니의 패스, 호날두의 슈팅 순간 멈춤(설명 1: 길이)
//       → 골 → 멈춤(설명 2: 오각형의 넓이) → 관중석에서 역습 전체 다시 보기 → 정리
import { timeline, ballPath, shots, makeWorld, smooth } from "../script.js";
import { frameCam, projectPath } from "../persp.js";
import { Labels, Trail, GLine, GLabel, GSegLbl, GRight, GTape, Explain, Lower, Tag, GoalBurst, DK } from "../overlay.jsx";
import { ENTER, player, lerp3, drift, showO, dribble } from "../kit3d.js";
import { seg, win, E, lerp, clamp } from "../../core.js";
import { COUNTER as CT } from "../../facts-soccer.js";

const WC = ([x, y]) => [-21.5 + x, 12 - y];
const O = WC(CT.O), R = WC(CT.R), C = WC(CT.C), Hh = WC(CT.H), K = WC(CT.K), T = WC(CT.T);

/* ── 세계 시각(ms) ── */
const GIVE = -700, CARRY = 3000, AT_R = 5000, PASS2 = 5400, AT_C = 6900, SHOT = 7050, IN = 7560, NET = 7720;
const P1 = [lerp(O[0], R[0], 22 / 60), lerp(O[1], R[1], 22 / 60)];            // 박지성이 몰고 간 곳(패스 길 위)

const MU = "semi2009United", AR = "semi2009Arsenal";
const PARK = player(MU, "박지성", "united", "main", O, {
  keys: [[-9e4, -24.0, 13.6], [-1600, -24.0, 13.6], [-200, ...O], [CARRY, ...P1], [4200, -0.2, -2.6], [6500, 4.5, -4.0]],
  look: (tw, c) => (tw < 0 ? [c.ball[0], c.ball[2]] : R), acts: [{ kind: "pass", at: CARRY, power: 1 }], seed: 0.4 });
const RON = player(MU, "호날두", "united", "main", WC([1.4, -2.4]), {
  keys: [[-9e4, -22.6, 16.8], [-1400, -21.6, 15.6], [GIVE, -20.4, 14.6], [0, -19.6, 14.0], [2500, 2.6, 7.6], [5000, 25.4, 0.6], [AT_C, ...C], [7600, 45.8, -2.6], [8800, 46.5, 4.5], [10000, 44, 10]],
  acts: [{ kind: "pass", at: GIVE, power: 0.4, foot: "L" }, { kind: "kick", at: SHOT, power: 1.05 }, { kind: "cheer", from: 8000, to: 10800 }], seed: 2.2 });
const ROO = player(MU, "루니", "united", "main", [14, -30], {
  keys: [[-9e4, 6, -26], [1500, 9, -27.5], [3500, 18.5, -27.5], [AT_R, ...R], [6200, 30.5, -21], [7400, 34, -16], [9000, 40, -6]],
  acts: [{ kind: "pass", at: PASS2, power: 0.85 }, { kind: "cheer", from: 8200, to: 10800 }], seed: 1.4 });
const ALM = player(AR, "알무니아", "rivalKeeper", "rival", [51.4, 0], { deep: 0.75,
  keys: [[-9e4, 50.6, 0.2], [5200, 50.6, 0.2], [6500, 49.4, -1.6], [6950, 49.0, -2.0], [8000, 49.0, -2.0]],
  acts: [{ kind: "dive", at: 7180, dir: -1, h: 0.4 }] });
const chase = (name, a, b, t1 = 7200, extra = {}) => player(AR, name, "rival", "rival", a, { keys: [[-9e4, ...a], [300, ...a], [t1, ...b], [t1 + 3000, b[0] + 2, b[1]]], stance: undefined, ...extra });
const ACTORS = [
  PARK, RON, ROO, ALM,
  chase("주루", [-6, 4], [37.5, -3.2], 7000), chase("투레", [2, -12], [33.5, -15]), chase("깁스", [-8, -24], [22, -24.5]),
  chase("사냐", [-12, 22], [24, 12]), chase("송", [-17, 4], [8, -1]), chase("파브레가스", [-29, -4], [-4, -8]),
  chase("나스리", [-33, 18], [-9, 12]), chase("판 페르시", [-37, 8], [-22, 6]), chase("아데바요르", [-40, -2], [-28, -2]),
  chase("월컷", [-31, 26], [-12, 20]),
  player(MU, "플레처", "united", "mate", [-30, 6], { keys: [[-9e4, -30, 6], [0, -30, 6], [7000, -2, 2]] }),
  player(MU, "캐릭", "united", "mate", [-34, -6], { keys: [[-9e4, -34, -6], [0, -34, -6], [7000, -8, -8]] }),
  player(MU, "안데르송", "united", "mate", [-36, 16], { keys: [[-9e4, -36, 16], [0, -36, 16], [7000, -12, 14]] }),
  player(MU, "에브라", "united", "mate", [-40, -20]),
  player(MU, "비디치", "united", "mate", [-44, -4]),
  player(MU, "퍼디낸드", "united", "mate", [-44, 8]),
  player(MU, "오셰이", "united", "mate", [-40, 24]),
];

/* ── 공 ── */
const BALL = ballPath([
  { t0: -2600, t1: GIVE, kind: "fn", f: dribble(RON, 0.6) },
  { t0: GIVE, t1: -150, kind: "ground", a: [-20.0, 14.3], b: [O[0] + 0.5, O[1] - 0.3] },
  { t0: -150, t1: CARRY, kind: "fn", f: dribble(PARK, 0.65) },
  { t0: CARRY, t1: AT_R, kind: "air", a: [P1[0] + 0.5, 0.2, P1[1] - 0.4], b: [R[0], 0.25, R[1]], h: 3.2, ease: "drag" },
  { t0: AT_R, t1: PASS2, kind: "fn", f: dribble(ROO, 0.6) },
  { t0: PASS2, t1: AT_C, kind: "ground", a: [R[0] + 0.6, R[1] + 0.4], b: [C[0] - 0.4, C[1] - 0.2] },
  { t0: AT_C, t1: SHOT, kind: "fn", f: dribble(RON, 0.55) },
  { t0: SHOT, t1: IN, kind: "air", a: [C[0] + 0.5, 0.2, C[1] + 0.3], b: [52.5, 0.95, 1.6], h: 0.4 },
  { t0: IN, t1: NET, kind: "air", a: [52.5, 0.95, 1.6], b: [54.3, 0.7, 2.0], ease: "net" },
  { t0: NET, t1: NET + 400, kind: "air", a: [54.3, 0.7, 2.0], b: [54.1, 0.2, 2.1], ease: "fall" },
]);
const net = (tw) => (tw >= NET - 50 ? { side: 1, y: 0.8, z: 2.0, k: tw - (NET - 50) } : null);

/* ── 박자표 ── */
const TL = timeline([
  { name: "intro", kind: "play", tw: [-3200, 0], dur: 3600 },
  { name: "run", kind: "play", tw: [0, AT_R], dur: 5400 },
  { name: "cross", kind: "play", tw: [AT_R, AT_C + 100], dur: 2900, speed: "into" },
  { name: "ex1", kind: "hold", dur: 14000, spot: [RON.id, PARK.id, ROO.id, "ball"] },
  { name: "goal", kind: "play", tw: [AT_C + 100, 10200], dur: 3800, speed: "outof" },
  { name: "ex2", kind: "hold", dur: 12000, spot: [RON.id, PARK.id, ROO.id] },
  { name: "replay", kind: "play", tw: [-1200, 8000], dur: 8200 },
  { name: "wrap", kind: "hold", dur: 7400, spot: [RON.id, PARK.id, ROO.id, "ball"] },
]);
const A = TL.a, Bd = TL.b;
const twAt = (t) => TL.at(t).tw;

/* ── 카메라 ── */
// 설명 컷: x(상대 골대 쪽)가 화면 오른쪽, y 가 화면 위(−Z 쪽을 내려다본다)
const EX = frameCam([O, Hh, T, K, R, C], { yaw: -90, pitch: 64, fov: 42, box: [880, 220, 1420, 710] });
const RET = 1300;
const CAM = shots([
  // 1. 박지성 뒤 눈높이 — 호날두가 공을 내준다
  { t0: 0, t1: A.run + 600, cam: (k) => ({ pos: lerp3([-29.5, 1.75, 17.5], [-28.0, 1.75, 16.8], E.sine(k)), at: [-8, 1.2, 4], fov: 40 }) },
  // 2. 함께 달리는 카메라 — 호날두 뒤 옆에서
  { t0: A.run + 600, t1: A.cross + 900, blend: 900, cam: (k, t) => {
    const tw = twAt(t), rp = RON.tr.at(tw - 250), rn = RON.tr.at(tw), b = BALL.at(tw);
    return { pos: [rp[0] - 7.5, 1.9, rp[1] + 6.5], at: lerp3([rn[0] + 12, 1.2, rn[1] - 5], [b[0], Math.max(1.0, b[1]), b[2]], 0.35), fov: 46 };
  } },
  // 3. 골대 옆 눈높이 — 루니의 패스가 오고 호날두가 찬다
  { t0: A.cross + 900, t1: A.ex1, blend: 700, cam: (k) => ({ pos: lerp3([55.6, 1.62, -9.5], [55.4, 1.62, -9.0], E.sine(k)), at: [36, 1.2, -10.5], fov: 44 }) },
  { t0: A.ex1, t1: Bd.ex1 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k) },
  // 4. 골 — 골대 뒤 눈높이
  { t0: Bd.ex1 - RET, t1: A.ex2, blend: RET, cam: (k, t) => {
    const rp = RON.tr.at(twAt(t));
    return { pos: lerp3([54.8, 1.62, 8.2], [55.0, 1.65, 7.4], E.sine(k)), at: lerp3([42, 1.2, -3], [rp[0], 1.3, rp[1]], smooth(0.3, 0.8, k)), fov: 48 };
  } },
  { t0: A.ex2, t1: Bd.ex2 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k, 0.04) },
  // 5. 다시 보기 — 본부석 관중의 눈높이에서 역습 전체를 따라간다
  { t0: Bd.ex2 - RET, t1: A.wrap, blend: RET, cam: (k, t) => {
    const tw = twAt(t), b = BALL.at(tw), rn = RON.tr.at(tw);
    const cx = clamp(lerp(b[0], rn[0], 0.4), -24, 40);
    return { pos: [cx - 5, 7.5, 50.5], at: [cx + 2, 0.5, -4], fov: 27 };
  } },
  { t0: A.wrap, t1: TL.dur, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k) },
]);

export const world = makeWorld({ tl: TL, actors: ACTORS, ball: BALL, cam: CAM, net });

/* ══════════ 글자 ══════════ */
const LOWER = [
  { t0: 700, t1: A.run + 2400, a: "2009. 5. 5. · 챔피언스리그 준결승 2차전", b: "아스널 1−3 맨유 — 61분, 역습" },
  { t0: A.run + 2700, t1: A.ex1 - 200, b: "호날두 → 박지성 → 루니 → 호날두" },
  { t0: Bd.ex2 + 300, t1: A.wrap - 300, a: "다시 보기 · 본부석 관중의 눈높이에서", b: "공은 박지성과 루니를 거쳐 가고, 호날두는 곧장 달려요" },
];

function overlay(mode, t, C_, P, W) {
  const isM = mode === "m";
  const { seg: Sg, local } = TL.at(t);
  const hold = Sg.kind === "hold";
  const dimK = smooth(0.05, 0.6, W.dim);
  const goalK = Sg.name === "goal" ? win(t, TL.tAt("goal", IN) + 100, TL.tAt("goal", IN) + 2400, 160, 600) : 0;
  const trailO = !hold && W.tw > CARRY && W.tw < NET + 200 ? 0.8 : 0;
  return (
    <g>
      <Trail W={W} pts={BALL.trail(W.tw, 480)} o={trailO} sw={4} />
      <Labels W={W} o={1 - dimK} />
      {hold && <Labels W={W} o={dimK} only={Sg.spot} />}
      {Sg.name === "ex1" && <Ex1 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "ex2" && <Ex2 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "wrap" && <Wrap W={W} l={local} d={Sg.dur} />}
      <GoalBurst k={goalK} y={320} />
      <Lower t={t} items={LOWER} />
      <Tag o={1 - dimK} s="재구성 화면 · 위치는 실제 장면을 바탕으로 다듬은 값 · 회색 선수는 그날 선발, 자리는 짐작" />
    </g>
  );
}
function Pts({ W, o, m, extra }) {
  return (
    <g opacity={o}>
      <GLabel W={W} p={O} s="O" size={28} dx={-30} dy={26} col="#F7F1E1" />
      <GLabel W={W} p={R} s={m ? CT.M.labR : "R"} size={26} dx={0} dy={-34} col="#F7F1E1" />
      <GLabel W={W} p={C} s={m ? CT.M.labC : "C"} size={26} dx={m ? 10 : 30} dy={m ? 40 : -4} col="#F7F1E1" />
      {extra && <GLabel W={W} p={Hh} s="H" size={26} dx={26} dy={24} col={DK.gold} />}
      {extra && <GLabel W={W} p={K} s="K" size={26} dx={-28} dy={-8} col={DK.gold} />}
      {extra && <GLabel W={W} p={T} s="T" size={26} dx={26} dy={-14} col={DK.gold} />}
    </g>
  );
}
/* ── 설명 1: 길이 ── */
function Ex1({ W, l, d, isM }) {
  const o = showO(l, d);
  if (!isM) return (
    <g>
      <g opacity={o}>
        <GTape W={W} a={O} b={R} p={seg(l, 900, 2500, E.io)} s={CT.E.tape.or} side={-1} col={DK.red} size={28} />
        <GTape W={W} a={R} b={C} p={seg(l, 3000, 4000, E.io)} s={CT.E.tape.rc} side={-1} col={DK.coral} size={28} />
        <GTape W={W} a={O} b={C} p={seg(l, 4600, 6200, E.io)} s={CT.E.tape.oc} side={1} col="#F7F1E1" size={28} />
        <Pts W={W} o={seg(l, 400, 900)} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  줄자로 재기" head="공이 간 길과 호날두가 달린 길" w={700}
        lines={[{ t: 2500, s: CT.E.or, size: 44 }, { t: 4000, s: CT.E.rc, size: 44 }, { t: 6200, s: CT.E.oc, size: 44 },
          { t: 8000, s: CT.E.ball, size: 36 }, { t: 9800, s: CT.E.more, size: 50 }]} lh={78} />
    </g>
  );
  const ln = (f, x0, x1) => [WC([x0, f(x0)]), WC([x1, f(x1)])];
  const F48 = WC([CT.R[0], 0]);
  return (
    <g>
      <g opacity={o}>
        <GLine W={W} pts={ln((x) => (3 / 4) * x, 0, 54)} col="#F7F1E1" sw={2.4} o={0.6} p={seg(l, 600, 1300)} glow={false} />
        <GLine W={W} pts={ln((x) => -(4 / 3) * x + 100, 44.5, 70)} col="#F7F1E1" sw={2.4} o={0.6} p={seg(l, 1100, 1800)} glow={false} />
        <GLine W={W} pts={ln((x) => (16 / 63) * x, 0, 72)} col="#F7F1E1" sw={2.4} o={0.6} p={seg(l, 1600, 2300)} glow={false} />
        <GLabel W={W} p={WC([20, 15])} s={CT.M.lines.or} size={24} col="#F7F1E1" ink="#10162a" dx={-50} dy={-24} o={seg(l, 1300, 1700) * (1 - seg(l, 5800, 6300))} />
        <GLabel W={W} p={WC([58, 22.7])} s={CT.M.lines.rc} size={24} col="#F7F1E1" ink="#10162a" dx={60} o={seg(l, 1800, 2200) * (1 - seg(l, 5800, 6300))} />
        <GLabel W={W} p={WC([36, 9.1])} s={CT.M.lines.oc} size={24} col="#F7F1E1" ink="#10162a" dy={30} o={seg(l, 2300, 2700) * (1 - seg(l, 5800, 6300))} />
        <GLine W={W} pts={[O, F48, R]} col={DK.gold} sw={3} dash="10 8" p={seg(l, 6200, 7000)} glow={false} />
        <GRight W={W} V={F48} A={O} B={R} s={2.2} col={DK.gold} o={seg(l, 6800, 7200)} />
        <GSegLbl W={W} a={O} b={F48} s="48" side={-1} off={24} size={26} col={DK.gold} o={seg(l, 6800, 7200)} />
        <GSegLbl W={W} a={F48} b={R} s="36" side={-1} off={24} size={26} col={DK.gold} o={seg(l, 6800, 7200)} />
        <GLine W={W} pts={[R, T, C]} col={DK.coral} sw={3} dash="10 8" p={seg(l, 7800, 8500)} glow={false} />
        <GRight W={W} V={T} A={R} B={C} s={2.2} col={DK.coral} o={seg(l, 8300, 8700)} />
        <GLine W={W} pts={[O, Hh, C]} col={DK.teal} sw={3} dash="10 8" p={seg(l, 9300, 10000)} glow={false} />
        <GRight W={W} V={Hh} A={O} B={C} s={2.2} col={DK.teal} o={seg(l, 9800, 10200)} />
        <GLine W={W} pts={[O, R, C]} col={DK.red} sw={5} />
        <GLine W={W} pts={[O, C]} col="#F7F1E1" sw={3.5} dash="12 10" />
        <Pts W={W} o={seg(l, 400, 900)} m={l > 3800} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  교점과 피타고라스" head="R과 C는 두 직선의 교점" w={720}
        lines={[{ t: 3000, s: CT.M.r, size: 36 }, { t: 4800, s: CT.M.c, size: 36 }, { t: 7200, s: CT.M.or, size: 38 },
          { t: 8700, s: `RC² = 15² + 20² = 25²`, size: 38 }, { t: 10200, s: `OC² = 63² + 16² = 65²`, size: 38 }, { t: 11600, s: CT.M.more, size: 46 }]} lh={68} />
    </g>
  );
}
/* ── 설명 2: 오각형의 넓이 ── */
function Ex2({ W, l, d, isM }) {
  const o = showO(l, d);
  const area = (pts, col, fo, k, sw = 3) => {
    const S = projectPath(W.cam, pts.map((p) => [p[0], 0.03, p[1]]));
    return S.length > 2 && <path d={"M" + S.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join("L") + "Z"} fill={col} fillOpacity={fo} stroke={col} strokeWidth={sw} opacity={k} />;
  };
  const rect = seg(l, 600, 1300), tri = seg(l, 2600, 3300), pent = seg(l, 4800, 5600);
  return (
    <g>
      <g opacity={o}>
        {area([O, Hh, T, K], DK.gold, 0.1, rect * (1 - 0.55 * pent))}
        <GSegLbl W={W} a={K} b={T} s={CT.E.lab.w} side={-1} off={30} size={28} col={DK.gold} o={rect} chip ink="#10162a" />
        <GSegLbl W={W} a={O} b={K} s={CT.E.lab.h} side={1} off={44} size={28} col={DK.gold} o={rect} chip ink="#10162a" />
        {area([C, T, R], DK.coral, 0.32, tri)}
        <GSegLbl W={W} a={R} b={T} s={CT.E.lab.tw} side={-1} off={24} size={26} col={DK.coral} o={tri} />
        <GSegLbl W={W} a={T} b={C} s={CT.E.lab.th} side={-1} off={24} size={26} col={DK.coral} o={tri} />
        {area([O, Hh, C, R, K], DK.teal, 0.3, pent, 4)}
        <Pts W={W} o={1} extra />
      </g>
      {isM ? (
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  넓이" head="오각형 = 직사각형 − 직각삼각형" w={720}
          lines={[{ t: 1300, s: `직사각형 OHTK  ${CT.C[0]} × ${CT.R[1]}`, size: 42 }, { t: 3300, s: `직각삼각형 CTR  {1/2} × 15 × 20`, size: 42 },
            { t: 5600, s: `${CT.C[0]} × ${CT.R[1]} − {1/2} × 15 × 20`, size: 42 }, { t: 7000, s: `= ‹${CT.penta} m²›`, size: 56 }]} lh={82} />
      ) : (
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  넓이" head="역습이 만든 오각형 OHCRK" w={720}
          lines={[{ t: 1300, s: CT.E.rect, size: 42 }, { t: 3300, s: CT.E.tri, size: 42 }, { t: 5600, s: CT.E.penta, size: 48 }]} lh={84} />
      )}
    </g>
  );
}
/* ── 정리 ── */
function Wrap({ W, l, d }) {
  const o = Math.min(seg(l, 300, 900), 1 - seg(l, d - 900, d - 300));
  return (
    <g>
      <g opacity={o}>
        <GLine W={W} pts={[O, R, C]} col={DK.red} sw={5} p={seg(l, 400, 1400)} />
        <GLine W={W} pts={[O, C]} col="#F7F1E1" sw={3.5} dash="12 10" p={seg(l, 400, 1400)} />
        <Pts W={W} o={seg(l, 300, 800)} />
      </g>
      <Explain local={l} dur={d} kicker="정리" head="공 85 m · 호날두 65 m" w={720}
        lines={[{ t: 1400, s: "공이 20 m 더 먼 길을 돌아도", size: 46 }, { t: 2800, s: "패스가 달리기보다 빨라 골이 되었어요", size: 46 }]} />
    </g>
  );
}

export default { key: "soc-counter", dur: TL.dur, world, overlay, tl: TL };
