// 3D 축구 1 — 맨시티 코너킥 → 콤파니 헤더 (2012-04-30 맨체스터 더비 1−0, 전반 추가 시간)
// 2D 장면(scenes/soc-corner.jsx)과 같은 수(facts-soccer.js 의 CORNER). 코너 K(0, 0) · 헤더 H(24, 10) · 수선의 발 F(24, 0) · 골문 T(31.5, 0).
// 세계 좌표: 오른쪽 골대(X = 52.5)의 왼쪽 코너. 2D 의 (골라인을 따라 x, 골라인에서 앞으로 y) → 세계 (52.5 − y, −34 + x).
// 흐름: 경기장 안 눈높이 → 코너 키커 뒤 → 공을 따라가다 헤더 순간 멈춤(설명 ①: 직각삼각형 KFH)
//       → 헤더가 골라인을 넘는 순간 멈춤(설명 ②: 직각삼각형 HFT) → 그물 · 세리머니 → 골키퍼 눈높이로 다시 보기 → 정리
import { timeline, actor, ballPath, shots, makeWorld, smooth } from "../script.js";
import { frameCam } from "../persp.js";
import { ENTER, showO, drift, lerp3 } from "../kit3d.js";
import { Labels, Trail, GLine, GLabel, GSegLbl, GRight, GTape, Explain, Lower, Tag, GoalBurst, DK } from "../overlay.jsx";
import { seg, win, E, lerp } from "../../core.js";
import { CORNER, who } from "../../facts-soccer.js";

const { E: TE, M: TM, KH, HF, KF, FT, HT, KT } = CORNER;
const W2 = ([x, y]) => [52.5 - y, -34 + x];
const K = W2(CORNER.P.K), H = W2(CORNER.P.H), F = W2(CORNER.P.F), T = W2(CORNER.P.T);

/* ── 세계 시각(ms): 실바가 차는 순간 KICK, 콤파니 머리에 닿는 순간 HEAD, 공이 골라인을 넘는 순간 LINE ── */
const KICK = 3000, HEAD = 4600, LINE = 5430, NET = 5600;
const BALL0 = [K[0] - 0.35, 0.2, K[1] + 0.35];
const HEADP = [H[0], 2.42, H[1]];

/* ── 선수 ── */
const U = (nm) => who("derby2012United", nm);
const mate = (id, name, at, extra = {}) => { const [n] = who("derby2012City", name); return actor({ id, kit: "city", n, name, role: "mate", keys: [[-9000, ...W2(at)], [9e4, ...W2(at)]], ...extra }); };
const rival = (id, name, at, extra = {}) => { const [n] = U(name); return actor({ id, kit: "rival", n, name, role: "rival", keys: [[-9000, ...W2(at)], [9e4, ...W2(at)]], stance: "ready", ...extra }); };
/** 서 있다가 공이 오면 조금 움직이는 선수: keys 는 2D 좌표 */
const mv = (keys) => keys.map(([tw, x, y]) => [tw, ...W2([x, y])]);

const ACTORS = [
  // 맨시티 — 주인공 둘
  actor({ id: "silva", kit: "city", n: 21, name: "실바", role: "main",
    keys: mv([[-9000, -2.9, -2.5], [1700, -2.9, -2.5], [2350, -2.0, -1.55], [2950, -0.85, -0.45], [3500, 0.2, 0.5], [4400, 0.9, 1.2]]),
    look: (tw, c) => (tw < KICK ? W2([24, 12]) : [c.ball[0], c.ball[2]]),
    acts: [{ kind: "kick", at: KICK, power: 1.05 }] }),
  actor({ id: "kompany", kit: "city", n: 4, name: "콤파니", role: "main",
    keys: mv([[-9000, 30.6, 16.6], [2500, 30.2, 17.0], [3000, 29.6, 16.4], [3700, 27.6, 14.2], [4250, 25.4, 11.6], [HEAD, 24, 10], [5100, 23.0, 8.6], [5800, 22.0, 6.4], [6500, 19.5, 4.2], [7600, 13.5, 2.2], [9000, 9.5, 1.6]]),
    acts: [{ kind: "head", at: HEAD, h: 0.72 }, { kind: "cheer", from: 6300, to: 9400 }], seed: 1.3 }),
  // 맨시티 — 같이 들어간 선수(옅게)
  mate("lescott", "레스콧", [37.5, 7.2], { keys: mv([[-9000, 37.5, 7.2], [3200, 37.5, 7.2], [4300, 36.4, 5.6], [5600, 36.0, 5.0]]) }),
  mate("toure", "투레", [36.4, 12.2], { keys: mv([[-9000, 36.4, 12.2], [3200, 36.4, 12.2], [4300, 34.6, 10.4], [5600, 34.0, 9.6]]) }),
  mate("aguero", "아구에로", [32.4, 4.6], { keys: mv([[-9000, 32.4, 4.6], [3300, 32.4, 4.6], [4300, 31.2, 3.4], [5600, 31.0, 3.0]]) }),
  mate("tevez", "테베스", [41.2, 5.4], { keys: mv([[-9000, 41.2, 5.4], [3400, 41.2, 5.4], [4500, 39.6, 4.8], [5600, 39.4, 4.6]]) }),
  mate("nasri", "나스리", [22.6, 21.4]),
  mate("barry", "배리", [40.4, 24.6]),
  mate("zabaleta", "사발레타", [17.0, 41.0]),
  mate("clichy", "클리시", [52.0, 43.0]),
  // 맨유(회색) — 2D 와 같은 자리(그날 선발 · 자리는 짐작)
  rival("smalling", "스몰링", [26.2, 17.4], { keys: mv([[-9000, 26.2, 17.4], [2600, 26.6, 17.6], [3100, 27.2, 16.8], [3800, 26.2, 14.6], [4350, 25.0, 12.3], [HEAD, 24.6, 11.6], [5300, 24.0, 10.2], [6400, 23.4, 9.4]]),
    acts: [{ kind: "head", at: HEAD + 140, h: 0.45 }], seed: 2.2 }),
  rival("ferdinand", "퍼디낸드", [35.4, 6.4], { keys: mv([[-9000, 35.4, 6.4], [3300, 35.4, 6.4], [4300, 34.2, 6.0], [5400, 33.8, 5.4]]) }),
  rival("evra", "에브라", [39.6, 9.4], { keys: mv([[-9000, 39.6, 9.4], [3300, 39.6, 9.4], [4400, 38.4, 8.6], [5400, 38.0, 8.0]]) }),
  rival("jones", "존스", [31.2, 14.2], { keys: mv([[-9000, 31.2, 14.2], [3200, 31.2, 14.2], [4200, 29.6, 12.4], [5400, 29.2, 11.6]]) }),
  rival("degea", "데 헤아", [34.6, 0.9], { kit: "rivalKeeper", deep: 0.75,
    keys: mv([[-9000, 34.6, 0.9], [3200, 34.6, 0.9], [4300, 33.6, 1.0], [4800, 33.4, 1.0], [5500, 32.6, 0.7], [6400, 32.6, 0.7]]),
    acts: [{ kind: "dive", at: 5050, dir: 1, h: 0.45 }] }),
  rival("nani", "나니", [29.0, 1.0]),
  rival("park", "박지성", [27.4, 6.2], { keys: mv([[-9000, 27.4, 6.2], [3300, 27.4, 6.2], [4300, 26.0, 7.0], [5400, 25.6, 7.2]]) }),
  rival("carrick", "캐릭", [37.0, 13.6]),
  rival("scholes", "스콜스", [38.8, 20.0]),
  rival("giggs", "긱스", [29.6, 21.6]),
  rival("rooney", "루니", [33.0, 27.5]),
];

/* ── 공 ── */
const BALL = ballPath([
  { t0: KICK, t1: HEAD, kind: "air", a: BALL0, b: HEADP, h: 6.6, bend: -2.2, ease: "drag" },
  { t0: HEAD, t1: LINE, kind: "air", a: HEADP, b: [T[0], 1.05, T[1]], h: 0.25, ease: "drag" },
  { t0: LINE, t1: NET, kind: "air", a: [T[0], 1.05, T[1]], b: [T[0] + 1.85, 0.92, T[1] + 0.1], ease: "net" },
  { t0: NET, t1: NET + 420, kind: "air", a: [T[0] + 1.85, 0.92, T[1] + 0.1], b: [T[0] + 1.7, 0.2, T[1] + 0.2], ease: "fall" },
]);
const net = (tw) => (tw >= NET - 60 ? { side: 1, y: 0.95, z: T[1] + 0.1, k: tw - (NET - 60) } : null);

/* ── 박자표 ── */
const TL = timeline([
  { name: "intro", kind: "play", tw: [-3800, 1700], dur: 5500 },
  { name: "kick", kind: "play", tw: [1700, HEAD], dur: 3400, speed: "into" },
  { name: "ex1", kind: "hold", dur: 11200, spot: ["kompany", "silva", "ball"] },
  { name: "head", kind: "play", tw: [HEAD, LINE], dur: 1900, speed: "both" },
  { name: "ex2", kind: "hold", dur: 10400, spot: ["kompany", "ball"] },
  { name: "goal", kind: "play", tw: [LINE, 8600], dur: 3600, speed: "outof" },
  { name: "replay", kind: "play", tw: [2600, 5900], dur: 6000, hide: ["degea"] },
  { name: "wrap", kind: "hold", dur: 7600, spot: ["kompany", "silva", "ball"] },
]);
const A = TL.a, Bd = TL.b;

/* ── 카메라 ── */
const twAt = (t) => TL.at(t).tw;
// 설명 컷: 점들이 화면 오른쪽(글씨는 왼쪽)에 꽉 차게 — 머무는 동안 아주 조금 다가간다
const BOX = [900, 200, 1490, 740];
const EX1 = frameCam([K, F, H], { yaw: 0, pitch: 66, fov: 34, box: BOX });
const EX2 = frameCam([H, F, T, [T[0] + 2, T[1]]], { yaw: 0, pitch: 62, fov: 34, box: BOX });
const WRAP = frameCam([K, H, T, F], { yaw: 0, pitch: 64, fov: 34, box: BOX });
const RET = 1300;                                    // 설명이 끝나기 전에 눈높이로 내려오는 시간
const T_CUT = TL.tAt("kick", KICK + 320);            // 공이 뜨자마자 박스 안으로 컷
const CAM = shots([
  // 1. 경기장 안, 페널티 박스 눈높이 — 선수들 사이에서 코너 쪽을 본다
  { t0: 0, t1: 2900, cam: (k) => ({ pos: lerp3([33.6, 1.7, 9.5], [35.8, 1.7, 5.2], E.sine(k)), at: [50, 1.3, -26], fov: 42 }) },
  // 2. 터치라인 밖 눈높이 — 옆에서 본 실바의 도움닫기와 차기(공이 뜨면 박스 안으로 컷)
  { t0: 2900, t1: T_CUT, cam: (k) => ({ pos: lerp3([44.0, 1.7, -37.3], [44.8, 1.7, -37.1], E.sine(k)), at: [52.2, 1.0, -32.8], fov: 34 }) },
  // 3. 박스 안(먼 쪽 골대 앞) 눈높이 — 콤파니가 달려 들어와 뛰어오른다
  { t0: T_CUT, t1: A.ex1, cam: (k, t) => {
    const tw = twAt(t), kp = ACTORS[1].tr.at(tw);
    return { pos: lerp3([50.2, 1.7, 3.4], [49.6, 1.75, 2.6], E.sine(k)), at: [lerp(kp[0], H[0], 0.5), 2.1, lerp(kp[1], H[1], 0.5)], fov: 40 };
  } },
  // 4. 설명 1 — 위로 올라가 직각삼각형 KFH 가 보이게
  { t0: A.ex1, t1: Bd.ex1 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX1, k) },
  // 5. 헤더 — 골대 옆 골라인 뒤 눈높이에서 콤파니를 본다(설명이 끝나기 전에 내려온다)
  { t0: Bd.ex1 - RET, t1: A.ex2, blend: RET, cam: (k) => ({ pos: lerp3([55.6, 1.6, -8.6], [55.4, 1.55, -8.2], k), at: [44, 1.9, -6.2], fov: 44 }) },
  // 6. 설명 2 — 직각삼각형 HFT
  { t0: A.ex2, t1: Bd.ex2 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX2, k) },
  // 7. 골 — 골대 뒤 눈높이: 그물이 출렁이고 콤파니가 달려 나간다
  { t0: Bd.ex2 - RET, t1: A.replay, blend: RET, cam: (k, t) => {
    const tw = twAt(t), kp = ACTORS[1].tr.at(tw);
    return { pos: lerp3([56.4, 1.7, 5.6], [57.0, 1.75, 3.4], E.sine(k)), at: lerp3([52.6, 1.1, -2.6], [kp[0], 1.4, kp[1]], smooth(0.35, 0.8, k)), fov: 46 };
  } },
  // 8. 다시 보기 — 골문 안, 골키퍼 데 헤아 자리의 눈높이(데 헤아는 감춘다)
  { t0: A.replay, t1: A.wrap, cam: (k, t) => {
    const tw = twAt(t), b = BALL.at(tw);
    const at = lerp3([46, 1.5, -18], [b[0], Math.max(1.1, b[1] * 0.8), b[2]], smooth(KICK - 200, KICK + 500, tw) * 0.8);
    return { pos: [53.4, 1.62, 0.8], at, fov: 50 };
  } },
  // 9. 정리 — 코너 쪽 전체
  { t0: A.wrap, t1: TL.dur, blend: ENTER, ease: E.out, cam: (k) => drift(WRAP, k) },
]);

export const world = makeWorld({ tl: TL, actors: ACTORS, ball: BALL, cam: CAM, net });

/* ══════════ 글자 ══════════ */
const LOWER = [
  { t0: 700, t1: 5300, a: "2012. 4. 30. · 맨체스터 더비", b: "맨시티 1−0 맨유 — 전반 추가 시간" },
  { t0: 5600, t1: A.ex1 - 200, b: "실바의 코너킥 → 콤파니의 헤더" },
  { t0: A.replay + 300, t1: A.wrap - 200, a: "다시 보기", b: "골문 안 — 골키퍼 데 헤아의 자리에서" },
];

function overlay(mode, t, C, P, W) {
  const isM = mode === "m";
  const { seg: S, local } = TL.at(t);
  const hold = S.kind === "hold";
  const dimK = smooth(0.05, 0.6, W.dim);
  const labelsO = 1 - dimK;
  const trailO = !hold && W.tw > KICK && W.tw < NET + 200 ? 1 : 0;
  const goalK = S.name === "goal" ? win(t, A.goal + 200, A.goal + 2600, 160, 600) : 0;
  return (
    <g>
      <Trail W={W} pts={BALL.trail(W.tw, 520)} o={trailO} />
      <Labels W={W} o={labelsO} />
      {hold && <Labels W={W} o={dimK} only={S.spot} />}
      {S.name === "ex1" && (isM ? <Ex1M W={W} l={local} d={S.dur} /> : <Ex1E W={W} l={local} d={S.dur} />)}
      {S.name === "ex2" && (isM ? <Ex2M W={W} l={local} d={S.dur} /> : <Ex2E W={W} l={local} d={S.dur} />)}
      {S.name === "wrap" && <Wrap W={W} l={local} d={S.dur} isM={isM} />}
      <GoalBurst k={goalK} y={330} />
      <Lower t={t} items={LOWER} />
      <Tag o={1 - dimK} />
    </g>
  );
}

/* ── 설명 ①: 직각삼각형 KFH ── */
function Pts({ W, o, show = "KHF" }) {
  return (
    <g opacity={o}>
      {show.includes("K") && <GLabel W={W} p={K} s="K" size={30} dx={-34} dy={8} />}
      {show.includes("H") && <GLabel W={W} p={H} s="H" size={30} dx={40} dy={-6} />}
      {show.includes("F") && <GLabel W={W} p={F} s="F" size={30} dx={0} dy={-40} col="#F7F1E1" />}
      {show.includes("T") && <GLabel W={W} p={T} s="T" size={30} dx={30} dy={-34} col={DK.teal} />}
    </g>
  );
}
function Ex1M({ W, l, d }) {
  const o = showO(l, d);
  const kh = seg(l, 700, 1700), hf = seg(l, 1700, 2500), kf = seg(l, 4400, 5400);
  return (
    <g>
      <g opacity={o}>
        <GLine W={W} pts={[K, H]} p={kh} col={DK.gold} sw={6} />
        <GLine W={W} pts={[H, F]} p={hf} col="#F7F1E1" sw={4} dash="12 10" />
        <GRight W={W} V={F} A={K} B={H} s={1.6} col="#F7F1E1" o={seg(l, 2400, 2900)} />
        <GLine W={W} pts={[K, F]} p={kf} col={DK.teal} sw={6} />
        <GSegLbl W={W} a={K} b={H} s={`${TM.lab.KH} m`} side={1} off={34} size={34} col={DK.gold} o={seg(l, 1500, 2000)} />
        <GSegLbl W={W} a={H} b={F} s={`${TM.lab.HF} m`} side={1} off={30} size={32} col="#F7F1E1" o={seg(l, 2400, 2900)} />
        <GSegLbl W={W} a={K} b={F} s={l < 7400 ? "?" : `${TM.lab.KF} m`} side={-1} off={34} size={34} col={DK.teal} o={seg(l, 5200, 5700)} />
        <Pts W={W} o={seg(l, 600, 1100)} show={l > 2400 ? "KHF" : "KH"} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  직각삼각형 KFH" head="골라인을 따라 K → F 는 몇 m?"
        lines={[
          { t: 1300, s: `KH = ${KH} m,  HF = ${HF} m`, size: 52 },
          { t: 3200, s: TM.eq1 },
          { t: 5200, s: TM.kf2, size: 54 },
          { t: 7400, s: `KF = ‹${KF} m›`, size: 70 },
        ]}
        foot="공이 날아간 K → H 가 빗변인 직각삼각형 — 피타고라스 정리" />
    </g>
  );
}
function Ex1E({ W, l, d }) {
  const o = showO(l, d);
  return (
    <g>
      <g opacity={o}>
        <GTape W={W} a={K} b={H} p={seg(l, 800, 2400, E.io)} s={`${KH} m`} side={1} off={40} />
        <GTape W={W} a={H} b={F} p={seg(l, 3200, 4400, E.io)} s={`${HF} m`} side={1} col="#F7F1E1" />
        <GTape W={W} a={K} b={F} p={seg(l, 5600, 7400, E.io)} s={`${KF} m`} side={-1} col={DK.teal} />
        <GRight W={W} V={F} A={K} B={H} s={1.6} col="#F7F1E1" o={seg(l, 4200, 4700)} />
        <Pts W={W} o={seg(l, 600, 1100)} show={l > 3400 ? "KHF" : "KH"} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  줄자로 재기" head="코너킥은 몇 m를 날아갔을까?"
        lines={[
          { t: 2400, s: TE.kh },
          { t: 4400, s: TE.hf },
          { t: 7400, s: TE.kf },
        ]}
        foot="H 에서 골라인에 똑바로 내린 곳이 F" />
    </g>
  );
}
/* ── 설명 ②: 직각삼각형 HFT ── */
function Ex2M({ W, l, d }) {
  const o = showO(l, d);
  return (
    <g>
      <g opacity={o}>
        <GLine W={W} pts={[F, T]} p={seg(l, 2000, 2800)} col={DK.teal} sw={7} />
        <GLine W={W} pts={[H, F]} p={seg(l, 600, 1300)} col="#F7F1E1" sw={4} dash="12 10" />
        <GRight W={W} V={F} A={T} B={H} s={1.1} col="#F7F1E1" o={seg(l, 1200, 1700)} />
        <GLine W={W} pts={[H, T]} p={seg(l, 4400, 5400)} col={DK.teal} sw={6} />
        <GSegLbl W={W} a={H} b={F} s={`${TM.lab.HF}`} side={1} off={28} size={32} col="#F7F1E1" o={seg(l, 1200, 1700)} />
        <GSegLbl W={W} a={F} b={T} s={TM.lab.FT} side={1} off={30} size={32} col={DK.teal} o={seg(l, 2700, 3200)} />
        <GSegLbl W={W} a={H} b={T} s={l < 6800 ? "?" : `${TM.lab.HT} m`} side={-1} off={34} size={34} col={DK.teal} o={seg(l, 5200, 5700)} />
        <Pts W={W} o={seg(l, 400, 900)} show="HFT" />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  직각삼각형 HFT" head="헤더가 날아간 거리 H → T 는?"
        lines={[
          { t: 1000, s: `골라인을 따라 KT = ${KT} m`, size: 50 },
          { t: 2800, s: `FT = ${KT} − ${KF} = ‹${FT}›`, size: 58 },
          { t: 4800, s: TM.eq2, size: 56 },
          { t: 6800, s: TM.ht, size: 62 },
        ]} />
    </g>
  );
}
function Ex2E({ W, l, d }) {
  const o = showO(l, d);
  return (
    <g>
      <g opacity={o}>
        <GTape W={W} a={F} b={T} p={seg(l, 2600, 3600, E.io)} s={`${FT} m`} side={1} col={DK.gold} />
        <GTape W={W} a={H} b={T} p={seg(l, 5200, 6600, E.io)} s={`${HT} m`} side={-1} col={DK.teal} />
        <Pts W={W} o={seg(l, 400, 900)} show="HFT" />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  빼기와 줄자" head="F에서 골문 T까지는?"
        lines={[
          { t: 1100, s: TE.kt },
          { t: 3400, s: TE.ft },
          { t: 6600, s: TE.ht },
        ]} />
    </g>
  );
}
/* ── 정리 ── */
function Wrap({ W, l, d, isM }) {
  const o = showO(l, d);
  return (
    <g>
      <g opacity={o}>
        <GLine W={W} pts={[K, H]} col={DK.gold} sw={6} p={seg(l, 500, 1400)} />
        <GLine W={W} pts={[H, T]} col={DK.teal} sw={6} p={seg(l, 1300, 1900)} />
        {isM && <GLine W={W} pts={[H, F]} col="#F7F1E1" sw={3.5} dash="10 9" p={seg(l, 1800, 2400)} />}
        {isM && <GLine W={W} pts={[K, T]} col="#F7F1E1" sw={3.5} p={seg(l, 1800, 2400)} o={0.7} />}
        <Pts W={W} o={seg(l, 400, 900)} show={isM ? "KHFT" : "KHT"} />
      </g>
      {isM ? (
        <Explain local={l} dur={d} kicker="정리" head="두 직각삼각형의 세 변" side="left"
          lines={[{ t: 1500, s: `${HF} : ${KF} : ${KH}  =  5 : 12 : 13`, size: 50, gap: 58 },
            { t: 2400, s: "모두 × 2", size: 34, c: "soft", gap: 104 },
            { t: 3400, s: `${FT} : ${HF} : ${HT}  =  3 : 4 : 5`, size: 50, gap: 58 },
            { t: 4300, s: "모두 × 2.5", size: 34, c: "soft" }]} />
      ) : (
        <Explain local={l} dur={d} kicker="정리" head="공이 날아간 길 K → H → T" side="left"
          lines={[{ t: 1500, s: `${KH} + ${HT} = ‹${KH + HT} m›`, size: 72 }]} />
      )}
    </g>
  );
}

export default { key: "soc-corner", dur: TL.dur, world, overlay, tl: TL };
