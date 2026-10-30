// 3D 축구 2 — 루크 쇼 프리킥 → 카세미루 헤더 (2023-02-26 리그컵 결승 맨유 2−0 뉴캐슬, 33분)
// 2D 장면(scenes/soc-setpiece.jsx)과 같은 수(facts-soccer.js 의 SETPIECE). 골대 가운데 G(0, 0) · 프리킥 F(26, 23) · 헤더 H(6, 8).
// 세계 좌표: 오른쪽 골대(X = 52.5). 2D 의 (옆 x, 골라인에서 앞 y) → 세계 (52.5 − y, x).
// 흐름: 박스 안 눈높이 → 키커 뒤 → 박스 안에서 카세미루의 헤더 순간 멈춤(설명 1: 거리 — 줄자 · 피타고라스)
//       → 골 · 세리머니에서 멈춤(설명 2: 기록표의 칸 · 상대도수) → 다시 보기 → 정리(100번 → 40번 → 4번 · 확률의 곱)
import { timeline, ballPath, shots, makeWorld, smooth } from "../script.js";
import { frameCam } from "../persp.js";
import { Labels, Trail, GLine, GLabel, GSegLbl, GRight, GTape, Explain, Lower, Tag, GoalBurst, Panel, DK } from "../overlay.jsx";
import { ENTER, player, lerp3, drift, showO, mapKeys } from "../kit3d.js";
import { UText, UTable, RowHi, IconGrid } from "../../kit-story.jsx";
import { seg, win, E, lerp } from "../../core.js";
import { SETPIECE as S } from "../../facts-soccer.js";

const W2 = ([x, y]) => [52.5 - y, x];
const G = W2(S.G), F = W2(S.F), H = W2(S.H);
const Q1 = W2([S.H[0], S.F[1]]), Q2 = W2([S.H[0], 0]);            // 직각의 꼭짓점(FH · HG)
const mv = (keys) => mapKeys(keys, W2);

/* ── 세계 시각(ms) ── */
const KICK = 3000, HEAD = 4550, LINE = 5350, NET = 5520;
const BALL0 = [F[0], 0.2, F[1]], HEADP = [H[0], 2.45, H[1]], IN = [52.5, 1.55, 0.7];

const UN = "cup2023United", NC = "cup2023Newcastle";
const ACTORS = [
  player(UN, "루크 쇼", "united", "main", W2([28.4, 25.6]), {
    keys: mv([[-9e4, 28.4, 25.6], [1800, 28.4, 25.6], [2400, 27.4, 24.5], [2950, 26.5, 23.6], [3500, 25.6, 22.6], [4400, 25.2, 21.8]]),
    look: (tw, c) => (tw < KICK ? H : [c.ball[0], c.ball[2]]), acts: [{ kind: "kick", at: KICK, power: 1 }] }),
  player(UN, "카세미루", "united", "main", W2([8.6, 13.6]), {
    keys: mv([[-9e4, 8.6, 13.6], [2400, 8.6, 13.4], [3000, 8.2, 12.6], [3700, 7.3, 10.6], [4200, 6.5, 9.0], [HEAD, 6, 8], [5000, 5.4, 7.0], [5600, 4.8, 6.2], [6400, 7.5, 7.4], [7600, 13.5, 9.6], [8600, 17.5, 11.0]]),
    acts: [{ kind: "head", at: HEAD, h: 0.7 }, { kind: "cheer", from: 6000, to: 9000 }], seed: 0.7 }),
  // 맨유(옅게) — 2D 에 있던 바란 · 마르티네스 + 그날 선발
  player(UN, "바란", "united", "mate", W2([-12, 10]), { keys: mv([[-9e4, -12, 10], [3200, -12, 10], [4300, -10.5, 8.4], [5400, -10, 7.8]]) }),
  player(UN, "마르티네스", "united", "mate", W2([21, 6.5])),
  player(UN, "베호르스트", "united", "mate", W2([1.5, 6.2]), { keys: mv([[-9e4, 1.5, 6.2], [3200, 1.5, 6.2], [4300, 0.6, 4.6], [5400, 0.4, 4.0]]) }),
  player(UN, "래시포드", "united", "mate", W2([-6.5, 9.2]), { keys: mv([[-9e4, -6.5, 9.2], [3200, -6.5, 9.2], [4300, -5.8, 7.4], [5400, -5.6, 6.8]]) }),
  player(UN, "페르난데스", "united", "mate", W2([20.5, 19.5])),
  player(UN, "프레드", "united", "mate", W2([4.0, 22.5])),
  player(UN, "안토니", "united", "mate", W2([-14.5, 21.0])),
  player(UN, "달로트", "united", "mate", W2([-2, 39])),
  // 뉴캐슬(회색) — 2D 와 같은 자리 + 그날 선발
  player(NC, "보트만", "rival", "rival", W2([-5, 6.5]), { keys: mv([[-9e4, -5, 6.5], [3300, -5, 6.5], [4300, -4.2, 5.6], [5400, -4.0, 5.2]]) }),
  player(NC, "번", "rival", "rival", W2([-9.5, 3.4])),
  player(NC, "셰어", "rival", "rival", W2([10.6, 4.0]), { keys: mv([[-9e4, 10.6, 4.0], [3300, 10.6, 4.0], [4300, 9.0, 4.4], [5400, 8.6, 4.6]]) }),
  player(NC, "조엘린통", "rival", "rival", W2([-2.6, 12.6])),
  player(NC, "트리피어", "rival", "rival", W2([16.6, 9.4]), { keys: mv([[-9e4, 16.6, 9.4], [3300, 16.6, 9.4], [4400, 14.0, 9.0], [5400, 13.2, 8.8]]) }),
  player(NC, "롱스태프", "rival", "rival", W2([5.4, 10.9]), {
    keys: mv([[-9e4, 5.4, 10.9], [3000, 5.4, 10.9], [3800, 5.9, 10.0], [HEAD, 6.8, 9.3], [5200, 6.6, 8.6]]), acts: [{ kind: "head", at: HEAD + 140, h: 0.35 }], seed: 2.4 }),
  player(NC, "기마랑이스", "rival", "rival", W2([1.8, 15.2])),
  player(NC, "알미론", "rival", "rival", W2([22.5, 17.5])),
  player(NC, "생막시맹", "rival", "rival", W2([-12, 24.5])),
  player(NC, "윌슨", "rival", "rival", W2([0, 36])),
  player(NC, "카리우스", "rivalKeeper", "rival", W2([-2.2, 0.9]), { deep: 0.75,
    keys: mv([[-9e4, -2.2, 0.9], [3200, -2.2, 0.9], [4300, -0.6, 1.0], [4800, -0.2, 1.0], [5500, 0.6, 0.7], [6400, 0.6, 0.7]]),
    acts: [{ kind: "dive", at: 5000, dir: -1, h: 0.55 }] }),
];
const CASE = ACTORS[1];

/* ── 공 ── */
const BALL = ballPath([
  { t0: KICK, t1: HEAD, kind: "air", a: BALL0, b: HEADP, h: 4.6, bend: 1.6, ease: "drag" },
  { t0: HEAD, t1: LINE, kind: "air", a: HEADP, b: IN, h: 0.15, ease: "drag" },
  { t0: LINE, t1: NET, kind: "air", a: IN, b: [54.3, 1.35, 0.85], ease: "net" },
  { t0: NET, t1: NET + 420, kind: "air", a: [54.3, 1.35, 0.85], b: [54.1, 0.2, 0.9], ease: "fall" },
]);
const net = (tw) => (tw >= NET - 60 ? { side: 1, y: 1.4, z: 0.85, k: tw - (NET - 60) } : null);

/* ── 박자표 ── */
const TL = timeline([
  { name: "intro", kind: "play", tw: [-3500, 1600], dur: 5100 },
  { name: "kick", kind: "play", tw: [1600, HEAD], dur: 3300, speed: "into" },
  { name: "ex1", kind: "hold", dur: 11500, spot: ["cup2023United:카세미루", "cup2023United:루크 쇼", "ball"] },
  { name: "head", kind: "play", tw: [HEAD, LINE], dur: 1800, speed: "both" },
  { name: "goal", kind: "play", tw: [LINE, 8200], dur: 3400, speed: "outof" },
  { name: "ex2", kind: "hold", dur: 12600, spot: ["cup2023United:카세미루"] },
  { name: "replay", kind: "play", tw: [2300, 5500], dur: 5800, hide: [] },
  { name: "wrap", kind: "hold", dur: 11000, spot: ["cup2023United:카세미루", "ball"] },
]);
const A = TL.a, Bd = TL.b;
const twAt = (t) => TL.at(t).tw;

/* ── 카메라 ── */
const BOX = [900, 200, 1490, 740];
const EX1 = frameCam([F, Q1, H, G, Q2], { yaw: 0, pitch: 64, fov: 34, box: BOX });
const RET = 1300;
const T_CUT = TL.tAt("kick", KICK + 380);
const CAM = shots([
  // 1. 박스 안 눈높이 — 프리킥 자리를 본다
  { t0: 0, t1: 2700, cam: (k) => ({ pos: lerp3([47.6, 1.7, -19.5], [46.9, 1.7, -18.2], E.sine(k)), at: [32, 1.4, 22], fov: 40 }) },
  // 2. 키커 뒤 눈높이 — 루크 쇼의 도움닫기와 차기
  { t0: 2700, t1: T_CUT, cam: (k) => ({ pos: lerp3([22.6, 1.74, 34.2], [23.4, 1.74, 33.4], E.sine(k)), at: [39.5, 1.3, 12.5], fov: 32 }) },
  // 3. 골키퍼 옆 눈높이 — 카세미루가 달려 들어와 뛰어오른다
  { t0: T_CUT, t1: A.ex1, cam: (k, t) => {
    const kp = CASE.tr.at(twAt(t));
    return { pos: lerp3([51.0, 1.66, -6.4], [50.6, 1.7, -5.6], E.sine(k)), at: [lerp(kp[0], H[0], 0.5), 2.0, lerp(kp[1], H[1], 0.5)], fov: 42 };
  } },
  // 4. 설명 1 — 두 직각삼각형이 보이게 위로
  { t0: A.ex1, t1: Bd.ex1 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX1, k) },
  // 5. 헤더 → 골 — 골대 옆 골라인 뒤 눈높이
  { t0: Bd.ex1 - RET, t1: A.ex2, blend: RET, cam: (k, t) => {
    const tw = twAt(t), kp = CASE.tr.at(tw);
    const look = lerp3([46.5, 1.7, 4.5], [kp[0], 1.4, kp[1]], smooth(LINE + 600, LINE + 2400, tw));
    return { pos: lerp3([55.4, 1.6, -6.2], [55.6, 1.62, -5.6], E.sine(k)), at: look, fov: 44 };
  } },
  // 6. 설명 2 — 세리머니에 멈춘 카세미루를 낮게(표는 오른쪽)
  { t0: A.ex2, t1: Bd.ex2 - RET, blend: 1600, cam: (k) => {
    const kp = CASE.tr.at(8200);
    return { pos: lerp3([kp[0] + 9.5, 1.3, kp[1] - 4.5], [kp[0] + 8.8, 1.25, kp[1] - 4.1], E.sine(k)), at: [kp[0] - 1.5, 1.6, kp[1] + 2.6], fov: 40 };
  } },
  // 7. 다시 보기 — 카세미루 뒤를 따라 달리는 눈높이
  { t0: Bd.ex2 - RET, t1: A.wrap, blend: RET, cam: (k, t) => {
    const tw = twAt(t), kp = CASE.tr.at(tw), b = BALL.at(tw);
    return { pos: [kp[0] - 6.2, 1.75, kp[1] + 4.2], at: lerp3([kp[0] + 4, 1.6, kp[1] - 2], [b[0], Math.max(1.2, b[1]), b[2]], smooth(KICK + 300, HEAD - 200, tw) * 0.6), fov: 44 };
  } },
  // 8. 정리 — 경기장 위에서(점 그림은 오른쪽)
  { t0: A.wrap, t1: TL.dur, blend: ENTER, ease: E.out, cam: (k) => drift(frameCam([F, H, G], { yaw: 0, pitch: 70, fov: 34, box: [140, 240, 760, 700] }), k) },
]);

export const world = makeWorld({ tl: TL, actors: ACTORS, ball: BALL, cam: CAM, net });

/* ══════════ 글자 ══════════ */
const LOWER = [
  { t0: 700, t1: 4900, a: "2023. 2. 26. · 리그컵 결승", b: "맨유 2−0 뉴캐슬 — 전반 33분" },
  { t0: 5300, t1: A.ex1 - 200, b: "루크 쇼의 프리킥 → 카세미루의 헤더" },
  { t0: Bd.ex2 + 200, t1: A.wrap - 200, a: "다시 보기", b: "카세미루 뒤에서 — 달려 들어가는 길" },
];
const cross = (tab, hiRow, t0, l, isM, head) => [
  head.map((h) => ({ s: h, size: 25, weight: 750, fill: "ink", fo: 0.1 })),
  ...tab.map((r, i) => [
    { s: S.range(r), size: 26, weight: i === hiRow ? 800 : 600, color: i === hiRow ? "gold" : undefined },
    { s: String(r[2]), size: 30, t: t0 + i * 120 },
    { s: String(r[3]), size: 30, t: t0 + i * 120, weight: i === hiRow ? 800 : 600, color: i === hiRow ? "gold" : undefined },
  ]),
];

function overlay(mode, t, C, P, W) {
  const isM = mode === "m";
  const { seg: Sg, local } = TL.at(t);
  const hold = Sg.kind === "hold";
  const dimK = smooth(0.05, 0.6, W.dim);
  const trailO = !hold && W.tw > KICK && W.tw < NET + 200 ? 1 : 0;
  const goalK = Sg.name === "goal" ? win(t, A.goal + 250, A.goal + 2700, 160, 600) : 0;
  return (
    <g>
      <Trail W={W} pts={BALL.trail(W.tw, 520)} o={trailO} />
      <Labels W={W} o={1 - dimK} />
      {hold && <Labels W={W} o={dimK} only={Sg.spot} />}
      {Sg.name === "ex1" && <Ex1 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "ex2" && <Ex2 l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "wrap" && <Wrap l={local} d={Sg.dur} isM={isM} />}
      <GoalBurst k={goalK} y={330} />
      <Lower t={t} items={LOWER} />
      <Tag o={1 - dimK} />
    </g>
  );
}

function Pts({ W, o }) {
  return (
    <g opacity={o}>
      <GLabel W={W} p={F} s="F" size={30} dx={-36} dy={6} />
      <GLabel W={W} p={H} s="H" size={30} dx={36} dy={-4} />
      <GLabel W={W} p={G} s="G" size={30} dx={0} dy={-38} col={DK.teal} />
    </g>
  );
}
/* ── 설명 1: 거리 ── */
function Ex1({ W, l, d, isM }) {
  const o = showO(l, d);
  if (!isM) return (
    <g>
      <g opacity={o}>
        <GTape W={W} a={F} b={H} p={seg(l, 900, 2500, E.io)} s={`${S.FH} m`} side={1} off={40} />
        <GTape W={W} a={H} b={G} p={seg(l, 4200, 5600, E.io)} s={`${S.HG} m`} side={1} col={DK.teal} />
        <Pts W={W} o={seg(l, 500, 1000)} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  줄자로 재기" head="공은 몇 m를 날아왔을까?"
        lines={[{ t: 2500, s: S.E.fh }, { t: 5600, s: S.E.hg }]}
        foot="F 프리킥 · H 헤더한 곳 · G 골대 가운데" />
    </g>
  );
  return (
    <g>
      <g opacity={o}>
        <GLine W={W} pts={[F, Q1, H]} p={seg(l, 700, 1700)} col={DK.gold} sw={4} dash="12 10" />
        <GRight W={W} V={Q1} A={F} B={H} s={1.6} col={DK.gold} o={seg(l, 1500, 2000)} />
        <GSegLbl W={W} a={F} b={Q1} s={S.M.lab.dx} side={1} off={30} size={32} col={DK.gold} o={seg(l, 1500, 2000)} />
        <GSegLbl W={W} a={Q1} b={H} s={S.M.lab.dy} side={1} off={30} size={32} col={DK.gold} o={seg(l, 1500, 2000)} />
        <GLine W={W} pts={[F, H]} p={seg(l, 2400, 3200)} col={DK.gold} sw={6} />
        <GSegLbl W={W} a={F} b={H} s={l < 3400 ? "?" : `${S.FH} m`} side={-1} off={34} size={34} col={DK.gold} o={seg(l, 3000, 3400)} />
        <GLine W={W} pts={[H, Q2, G]} p={seg(l, 4700, 5600)} col={DK.teal} sw={4} dash="12 10" />
        <GRight W={W} V={Q2} A={H} B={G} s={1.1} col={DK.teal} o={seg(l, 5400, 5900)} />
        <GSegLbl W={W} a={H} b={Q2} s={S.M.lab.hy} side={-1} off={28} size={30} col={DK.teal} o={seg(l, 5400, 5900)} />
        <GSegLbl W={W} a={Q2} b={G} s={S.M.lab.hx} side={-1} off={28} size={30} col={DK.teal} o={seg(l, 5400, 5900)} />
        <GLine W={W} pts={[H, G]} p={seg(l, 6200, 6900)} col={DK.teal} sw={6} />
        <GSegLbl W={W} a={H} b={G} s={l < 7200 ? "?" : `${S.HG} m`} side={1} off={30} size={32} col={DK.teal} o={seg(l, 6800, 7200)} />
        <Pts W={W} o={seg(l, 500, 1000)} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  피타고라스 정리" head="옆 · 앞으로 떨어진 거리로 직각삼각형"
        lines={[{ t: 3300, s: S.M.fh, size: 54 }, { t: 7200, s: S.M.hg, size: 54 }]}
        foot="골라인 방향(옆)과 골라인에서 앞쪽은 서로 수직" />
    </g>
  );
}
/* ── 설명 2: 기록표 ── */
const TX = 860, TCOL = [250, 130, 150], TRH = [52, 54, 54, 54], TY1 = 238, HRH = [52, 54, 54, 54, 54], TY2 = 520;
function Ex2({ l, d, isM }) {
  const o = showO(l, d);
  const hi1 = seg(l, 1800, 2300), hi2 = seg(l, 4600, 5100);
  return (
    <g>
      <g opacity={o}>
        <Panel x={TX - 34} y={TY1 - 66} w={600} h={TY2 + 330 - TY1} />
        <UText x={TX} y={TY1 - 22} s="프리킥 크로스 기록 (가상의 자료)" size={24} weight={700} fill={DK.soft} C={DK} />
        <RowHi x={TX} y={TY1} cols={TCOL} rh={TRH} r={1 + S.ci} C={DK} o={hi1} />
        <UTable x={TX} y={TY1} cols={TCOL} rh={TRH} C={DK} t={l} rows={cross(S.CROSS, hi1 > 0 ? S.ci : -1, 400, l, isM, ["F → H (m)", "크로스", "머리에"])} />
        <UText x={TX} y={TY2 - 22} s="헤더 기록 (가상의 자료)" size={24} weight={700} fill={DK.soft} C={DK} />
        <RowHi x={TX} y={TY2} cols={TCOL} rh={HRH} r={1 + S.hi} C={DK} o={hi2} col="teal" />
        <UTable x={TX} y={TY2} cols={TCOL} rh={HRH} C={DK} t={l} rows={cross(S.HEAD, hi2 > 0 ? S.hi : -1, 700, l, isM, ["H → G (m)", "헤더", "골"])} />
      </g>
      {isM ? (
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  상대도수 → 확률" head="거리가 속한 계급의 상대도수" w={700}
          lines={[{ t: 2300, s: S.M.p1, size: 46 }, { t: 5100, s: S.M.p2, size: 46 }, { t: 7600, s: S.M.edge, size: 34, c: "soft" }]} />
      ) : (
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  기록표에서 칸 찾기" head="그 거리가 들어가는 칸은?" w={700}
          lines={[{ t: 2300, s: S.E.cls1, size: 44 }, { t: 5100, s: S.E.cls2, size: 44 }, { t: 7600, s: S.E.edge, size: 36, c: "soft" }]}
          foot="‘이상’은 그 수를 포함, ‘미만’은 포함하지 않아요" />
      )}
    </g>
  );
}
/* ── 정리: 100번으로 생각하기 · 확률의 곱 ── */
const GX = 1000, GY = 230, GSTEP = 46;
function Wrap({ l, d, isM }) {
  const o = showO(l, d);
  const head = (k) => seg(l, 1800 + Math.floor(k / 10) * 260, 2100 + Math.floor(k / 10) * 260);
  const goal = (k) => seg(l, 4800 + (k / 10) * 280, 5100 + (k / 10) * 280);
  return (
    <g>
      <g opacity={o}>
        <Panel x={GX - 30} y={GY - 30} w={10 * GSTEP + 60} h={10 * GSTEP + 60} />
        <IconGrid x={GX} y={GY} cols={10} rows={10} step={GSTEP} r={15} C={DK} paint={(k) => {
          const g = k < S.nHead ? goal(k) : 0, hd = k < S.nHead ? head(k) : 0;
          if (k % 10 === 0 && g > 0 && Math.floor(k / 10) < S.nGoal) return { fill: DK.gold, stroke: DK.gold, scale: 1.1 + 0.25 * (1 - g), sw: 2 };
          if (hd > 0) return { fill: isM ? DK.teal : DK.sky, fo: 0.3 + 0.6 * hd, stroke: isM ? DK.teal : DK.sky, sw: 2 };
          return { stroke: DK.soft, o: 0.7, sw: 2 };
        }} />
      </g>
      {isM ? (
        <Explain local={l} dur={d} kicker="정리  ·  두 확률의 곱" head="머리에 닿고, 그 헤더가 골이 되어야" w={760}
          lines={[{ t: 1600, s: `${S.N} ${S.M.grid[1]}`, size: 54, c: "teal" }, { t: 4600, s: `${S.nHead} ${S.M.grid[2]}`, size: 54, c: "gold" },
            { t: 7000, s: S.M.prod, size: 64 }]} />
      ) : (
        <Explain local={l} dur={d} kicker="정리  ·  100번 찬다고 생각하기" head="이런 프리킥을 100번 차면" w={760}
          lines={[{ t: 1600, s: S.E.n1, size: 46 }, { t: 4600, s: S.E.n2, size: 46 }, { t: 7000, s: S.E.n3, size: 46 }]} />
      )}
    </g>
  );
}

export default { key: "soc-setpiece", dur: TL.dur, world, overlay, tl: TL };
