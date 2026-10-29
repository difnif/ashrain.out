// 3D 축구 4 — 맨유 삼각패스: 패스 삼각형의 넓이
// 2D 장면(scenes/soc-triangle.jsx)과 같은 수(facts-soccer.js 의 TRIANGLE). 터치라인이 x축, 하프라인이 y축(단위 m).
// A(3, 2) → B(12, 14) → C(28, 2) → A 로 공을 두 바퀴 돌리고, 회색 세 선수가 끼어들려 한다.
// 세계 좌표: 하프라인(X = 0)과 가까운 터치라인(Z = 34)이 만나는 곳이 원점. (x, y) → 세계 (x, 34 − y).
//   터치라인 밖에서 −Z 쪽을 보면 x 가 화면 오른쪽, y 가 화면 위 — 수학 그림과 같은 방향이다.
// 흐름: 터치라인 밖 눈높이에서 한 바퀴 → 멈춤(설명 1: 꼭짓점 · 밑변 · 높이) → 한 바퀴 더(다른 눈높이) → 멈춤(설명 2: 넓이) → 정리
import { timeline, actor, ballPath, shots, makeWorld, smooth } from "../script.js";
import { frameCam } from "../persp.js";
import { Labels, GLine, GLabel, GSegLbl, GRight, Explain, Lower, Tag, DK } from "../overlay.jsx";
import { ENTER, lerp3, drift, showO, extra } from "../kit3d.js";
import { seg, E, lerp, clamp } from "../../core.js";
import { projectPath } from "../persp.js";
import { TRIANGLE as TR } from "../../facts-soccer.js";

const WT = ([x, y]) => [x, 34 - y];
const A = WT(TR.A), B = WT(TR.B), C = WT(TR.C);
const R1 = WT([TR.A[0], TR.B[1]]), R2 = WT([TR.C[0], TR.B[1]]), FOOT = WT([TR.B[0], TR.C[1]]);

/* ── 패스 일정(세계 시각 ms): [보내는 쪽, 받는 쪽, 출발, 도착] ── */
const VX = { A, B, C };
const LEG = { AB: 1100, BC: 1400, CA: 1800 };
const PASSES = [];
{
  let t = 1000;
  const order = ["A", "B", "C", "A", "B", "C", "A"];
  for (let i = 0; i < 6; i++) { const f = order[i], g = order[i + 1], d = LEG[f + g]; PASSES.push([f, g, t, t + d]); t += d + 600; }
}
const LOOP1 = PASSES[2][3], LOOP2 = PASSES[5][3];             // 공이 A 로 돌아온 순간(첫 바퀴 · 둘째 바퀴)

/** 꼭짓점 선수: 받을 때 공 쪽으로 반걸음, 줄 때 차기 */
function vertex(id, P, side) {
  const acts = PASSES.filter((p) => p[0] === id).map((p) => ({ kind: "pass", at: p[2], power: 0.6 }));
  const keys = [[-9e4, ...P]];
  for (const p of PASSES) if (p[1] === id) { const f = VX[p[0]]; const dx = f[0] - P[0], dz = f[1] - P[1], L = Math.hypot(dx, dz); keys.push([p[3] - 500, ...P], [p[3], P[0] + (dx / L) * 0.6, P[1] + (dz / L) * 0.6], [p[3] + 900, ...P]); }
  keys.push([9e4, ...P]);
  keys.sort((a, b) => a[0] - b[0]);
  return actor({ id, kit: "united", n: id, name: "", role: "main", keys, acts, seed: side });
}
const ACTORS = [vertex("A", A, 0.3), vertex("B", B, 1.7), vertex("C", C, 2.9)];
// 회색 셋 — 공을 따라 끼어들려 한다(조금 늦게)
const ballLag = (lag, f) => (tw) => f(BALL.at(tw - lag));
const presser = (id, home, pull, lag) => {
  const keys = [];
  for (let tw = -2000; tw <= LOOP2 + 3000; tw += 400) {
    const b = BALL.at(tw - lag);
    keys.push([tw, lerp(home[0], b[0], pull), lerp(home[1], b[2], pull)]);
  }
  return extra(id, "rival", home, { keys, deep: 0.5, look: (tw, c) => [c.ball[0], c.ball[2]] });
};

/* ── 공 ── */
const BALL = ballPath(PASSES.map(([f, g, t0, t1]) => ({ t0, t1, kind: "ground", a: off(VX[f], VX[g], 0.55), b: off(VX[g], VX[f], 0.55), ease: "slow" })));
function off(P, Q, d) { const dx = Q[0] - P[0], dz = Q[1] - P[1], L = Math.hypot(dx, dz); return [P[0] + (dx / L) * d, P[1] + (dz / L) * d]; }
ACTORS.push(presser("d1", WT([8, 9]), 0.42, 700), presser("d2", WT([17, 7]), 0.38, 900), presser("d3", WT([22, 11]), 0.4, 800));
ACTORS.push(extra("far1", "united", WT([-14, 22]), { role: "mate" }), extra("far2", "rival", WT([-8, 30])), extra("far3", "rival", WT([40, 24])),
  extra("far4", "united", WT([44, 9]), { role: "mate" }));

/* ── 박자표 ── */
const TL = timeline([
  { name: "intro", kind: "play", tw: [-2500, 1000], dur: 3500 },
  { name: "loop1", kind: "play", tw: [1000, LOOP1], dur: LOOP1 - 1000 + 300, speed: "into" },
  { name: "ex1", kind: "hold", dur: 13800, spot: ["A", "B", "C", "ball"] },
  { name: "loop2", kind: "play", tw: [LOOP1, LOOP2], dur: LOOP2 - LOOP1 + 300, speed: "both" },
  { name: "ex2", kind: "hold", dur: 13200, spot: ["A", "B", "C", "ball"] },
  { name: "wrap", kind: "hold", dur: 6800, spot: ["A", "B", "C", "ball"] },
]);
const Aa = TL.a, Bb = TL.b;
const twAt = (t) => TL.at(t).tw;

/* ── 카메라 ── */
const EX = frameCam([WT([0, 0]), WT([33, 0]), WT([0, 19]), WT([33, 19])], { yaw: -90, pitch: 66, fov: 34, box: [880, 190, 1500, 730] });
const RET = 1300;
const CAM = shots([
  // 1. 경기장 안 눈높이 — 삼각형 건너편에서 터치라인 쪽을 본다(A · B · C 가 모두 보인다)
  { t0: 0, t1: Aa.ex1, cam: (k, t) => {
    const b = BALL.at(twAt(t));
    return { pos: lerp3([17.0, 1.72, 8.5], [13.8, 1.72, 9.6], E.sine(clamp(t / Aa.ex1))), at: [lerp(15.5, b[0], 0.3), 1.0, 28], fov: 48 };
  } },
  { t0: Aa.ex1, t1: Bb.ex1 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k) },
  // 2. 둘째 바퀴 — 삼각형 안쪽(B 뒤) 눈높이에서 A · C 를 본다
  { t0: Bb.ex1 - RET, t1: Aa.ex2, blend: RET, cam: (k, t) => {
    const b = BALL.at(twAt(t));
    return { pos: lerp3([13.5, 1.72, 10.5], [15.5, 1.72, 10.8], E.sine(k)), at: [lerp(15, b[0], 0.5), 1.0, lerp(31, b[2], 0.3)], fov: 50 };
  } },
  { t0: Aa.ex2, t1: TL.dur, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k, 0.04) },
]);

export const world = makeWorld({ tl: TL, actors: ACTORS, ball: BALL, cam: CAM });

/* ══════════ 글자 ══════════ */
const LOWER = [
  { t0: 600, t1: 5600, a: "맨유의 삼각패스", b: "A → B → C → A, 세 선수가 공을 돌려요" },
  { t0: Bb.ex1 + 300, t1: Aa.ex2 - 300, b: "삼각형 안쪽에서 — 회색 선수가 끼어들 틈이 있을까?" },
];

function overlay(mode, t, C, P, W) {
  const isM = mode === "m";
  const { seg: Sg, local } = TL.at(t);
  const hold = Sg.kind === "hold";
  const dimK = smooth(0.05, 0.6, W.dim);
  return (
    <g>
      {!hold && <PassLines W={W} />}
      <Labels W={W} o={1 - dimK} />
      {hold && <Labels W={W} o={dimK} only={Sg.spot} />}
      {Sg.name === "ex1" && <Ex1 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "ex2" && <Ex2 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "wrap" && <Wrap W={W} l={local} d={Sg.dur} />}
      <Lower t={t} items={LOWER} />
      <Tag o={1 - dimK} s="재구성 화면 · 맨유가 자주 쓰는 삼각패스를 단순하게 다시 만든 그림" />
    </g>
  );
}
/** 지나간 패스 길 — 바닥에 빨간 선(지금 패스는 그려지는 중) */
function PassLines({ W }) {
  const tw = W.tw, out = [];
  PASSES.forEach(([f, g, t0, t1], i) => {
    if (tw < t0) return;
    const k = clamp((tw - t0) / (t1 - t0));
    const fade = i < 3 && tw > LOOP1 + 400 ? 0.35 : 1;
    out.push(<GLine key={i} W={W} pts={[VX[f], VX[g]]} p={k} col={DK.red} sw={4} o={0.8 * fade} glow={false} />);
  });
  return <g>{out}</g>;
}
function Tri({ W, o, fill = 0 }) {
  if (o <= 0.01) return null;
  const S = projectPath(W.cam, [A, B, C].map((p) => [p[0], 0.03, p[1]]));
  return (
    <g opacity={o}>
      {fill > 0 && S.length === 3 && <path d={"M" + S.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join("L") + "Z"} fill={DK.teal} fillOpacity={0.3 * fill} />}
      <GLine W={W} pts={[A, B, C, A]} col={DK.teal} sw={5} />
    </g>
  );
}
function Pts({ W, o, m }) {
  return (
    <g opacity={o}>
      <GLabel W={W} p={A} s={m ? TR.M.labA : "A"} size={26} dx={m ? -40 : -26} dy={34} col="#F7F1E1" />
      <GLabel W={W} p={B} s={m ? TR.M.labB : "B"} size={26} dx={0} dy={-36} col="#F7F1E1" />
      <GLabel W={W} p={C} s={m ? TR.M.labC : "C"} size={26} dx={m ? 40 : 26} dy={34} col="#F7F1E1" />
    </g>
  );
}
/** 모눈(1 m) — 5 m 마다 굵게, 눈금 수 */
function Grid({ W, o, isM }) {
  if (o <= 0.01) return null;
  const out = [];
  for (let x = 0; x <= 32; x++) out.push(<GLine key={"x" + x} W={W} pts={[WT([x, 0]), WT([x, 19])]} col="#F7F1E1" sw={x % 5 ? 0.9 : 1.8} o={x % 5 ? 0.14 : 0.3} glow={false} n={4} />);
  for (let y = 0; y <= 19; y++) out.push(<GLine key={"y" + y} W={W} pts={[WT([0, y]), WT([32.5, y])]} col="#F7F1E1" sw={y % 5 ? 0.9 : 1.8} o={y % 5 ? 0.14 : 0.3} glow={false} n={4} />);
  const nums = [];
  for (let x = 0; x <= 30; x += 5) nums.push(<GLabel key={"nx" + x} W={W} p={WT([x, -1.2])} s={String(x)} size={22} chip={false} col={DK.soft} />);
  for (let y = 5; y <= 15; y += 5) nums.push(<GLabel key={"ny" + y} W={W} p={WT([-1.4, y])} s={String(y)} size={22} chip={false} col={DK.soft} />);
  return (
    <g opacity={o}>
      {out}{nums}
      {isM && <GLabel W={W} p={WT([34.2, 0])} s="x" size={32} chip={false} col="#F7F1E1" />}
      {isM && <GLabel W={W} p={WT([0, 20.4])} s="y" size={32} chip={false} col="#F7F1E1" />}
    </g>
  );
}
/* ── 설명 1: 꼭짓점 · 밑변 · 높이 ── */
function Ex1({ W, l, d, isM }) {
  const o = showO(l, d);
  if (!isM) return (
    <g>
      <g opacity={o}>
        <Grid W={W} o={seg(l, 300, 1000)} />
        <Tri W={W} o={seg(l, 600, 1200)} />
        <GLine W={W} pts={[A, WT([TR.A[0], 0])]} col={DK.gold} sw={3} dash="6 7" o={seg(l, 1600, 2100)} glow={false} />
        <GLine W={W} pts={[C, WT([TR.C[0], 0])]} col={DK.gold} sw={3} dash="6 7" o={seg(l, 2400, 2900)} glow={false} />
        <GLine W={W} pts={[WT([TR.A[0], -0.6]), WT([TR.C[0], -0.6])]} col={DK.gold} sw={5} p={seg(l, 2900, 3700)} />
        <GSegLbl W={W} a={WT([TR.A[0], -0.6])} b={WT([TR.C[0], -0.6])} s={TR.E.lab.w} side={1} off={26} size={28} col={DK.gold} o={seg(l, 3500, 3900)} chip ink="#10162a" />
        <GLine W={W} pts={[WT([TR.C[0] + 2, TR.C[1]]), WT([TR.C[0] + 2, TR.B[1]])]} col={DK.gold} sw={5} p={seg(l, 5600, 6400)} />
        <GLine W={W} pts={[B, WT([TR.C[0] + 2, TR.B[1]])]} col={DK.gold} sw={2.5} dash="6 7" o={seg(l, 5200, 5700)} glow={false} />
        <GSegLbl W={W} a={WT([TR.C[0] + 2, TR.C[1]])} b={WT([TR.C[0] + 2, TR.B[1]])} s={TR.E.lab.h} side={-1} off={40} size={28} col={DK.gold} o={seg(l, 6200, 6600)} chip ink="#10162a" />
        <Pts W={W} o={seg(l, 500, 1000)} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  모눈으로 읽기" head="패스 삼각형의 가로와 세로" w={700}
        lines={[{ t: 3900, s: TR.E.w, size: 50 }, { t: 6600, s: TR.E.h, size: 50 }]}
        foot="터치라인과 하프라인에서 잰 거리로 자리를 나타내요" />
    </g>
  );
  const ln = (f, x0, x1) => [WT([x0, f(x0)]), WT([x1, f(x1)])];
  return (
    <g>
      <g opacity={o}>
        <Grid W={W} o={seg(l, 300, 1000) * 0.6} isM />
        <GLine W={W} pts={ln((x) => (4 / 3) * x - 2, 1.5, 15)} col="#F7F1E1" sw={3} o={0.75} p={seg(l, 900, 1600)} glow={false} />
        <GLine W={W} pts={ln((x) => -(3 / 4) * x + TR.bcB, 8.2, 30.6)} col="#F7F1E1" sw={3} o={0.75} p={seg(l, 1400, 2100)} glow={false} />
        <GLine W={W} pts={[WT([0, TR.C[1]]), WT([32.5, TR.C[1]])]} col="#F7F1E1" sw={3} o={0.75} p={seg(l, 1900, 2600)} glow={false} />
        <GLabel W={W} p={WT([5.2, 9.8])} s={TR.M.lineAB} size={24} col="#F7F1E1" ink="#10162a" o={seg(l, 1500, 1900)} dx={-60} />
        <GLabel W={W} p={WT([23.5, 11.5])} s={TR.M.lineBC} size={24} col="#F7F1E1" ink="#10162a" o={seg(l, 2000, 2400)} dx={60} />
        <GLabel W={W} p={WT([31, TR.C[1]])} s={TR.M.lineCA} size={24} col="#F7F1E1" ink="#10162a" o={seg(l, 2500, 2900)} dy={-30} />
        <Tri W={W} o={seg(l, 8800, 9400)} />
        <Pts W={W} o={seg(l, 300, 800)} m={l > 3400} />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  직선과 교점" head="세 패스가 지나간 직선의 꼭짓점" w={700}
        lines={[{ t: 3400, s: TR.M.b, size: 40 }, { t: 5600, s: TR.M.a, size: 40 }, { t: 7800, s: TR.M.bb, size: 40 }]} lh={78}
        foot="C(28, 2)를 넣으면 b가 나오고, 두 직선이 만나는 곳이 꼭짓점" />
    </g>
  );
}
/* ── 설명 2: 넓이 ── */
function Ex2({ W, l, d, isM }) {
  const o = showO(l, d);
  if (!isM) {
    const rect = seg(l, 600, 1300), lt = seg(l, 2600, 3300), rt = seg(l, 4600, 5300), cut = seg(l, 6800, 7500);
    const poly = (pts, col, fo, k) => { const S = projectPath(W.cam, pts.map((p) => [p[0], 0.03, p[1]])); return S.length > 2 && <path d={"M" + S.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join("L") + "Z"} fill={col} fillOpacity={fo} stroke={col} strokeWidth={3} opacity={k} />; };
    return (
      <g>
        <g opacity={o}>
          <Grid W={W} o={0.5} />
          {poly([A, R1, R2, C], DK.gold, 0.08, rect * (1 - 0.6 * cut))}
          {poly([A, R1, B], DK.coral, 0.3, lt * (1 - 0.75 * cut))}
          {poly([B, R2, C], DK.coral, 0.3, rt * (1 - 0.75 * cut))}
          <GLabel W={W} p={[(A[0] + R1[0] + B[0]) / 3, (A[1] + R1[1] + B[1]) / 3]} s={TR.E.lab.left} size={30} chip={false} col={DK.coral} o={lt * (1 - 0.75 * cut)} />
          <GLabel W={W} p={[(B[0] + R2[0] + C[0]) / 3, (B[1] + R2[1] + C[1]) / 3]} s={TR.E.lab.right} size={30} chip={false} col={DK.coral} o={rt * (1 - 0.75 * cut)} />
          <Tri W={W} o={1} fill={cut} />
          <Pts W={W} o={1} />
        </g>
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  직사각형에서 빼기" head="패스 삼각형의 넓이" w={700}
          lines={[{ t: 1300, s: TR.E.rect, size: 44 }, { t: 3300, s: TR.E.left, size: 40 }, { t: 5300, s: TR.E.right, size: 40 },
            { t: 7500, s: TR.E.area, size: 50 }, { t: 9400, s: TR.E.check, size: 34, c: "soft" }]} lh={78} />
      </g>
    );
  }
  return (
    <g>
      <g opacity={o}>
        <Grid W={W} o={0.4} isM />
        <Tri W={W} o={1} fill={seg(l, 4800, 5600)} />
        <GLine W={W} pts={[A, C]} col={DK.gold} sw={8} o={seg(l, 600, 1200) * 0.7} />
        <GSegLbl W={W} a={A} b={C} s={`밑변 ${TR.base}`} side={1} off={34} size={28} col={DK.gold} at={0.62} o={seg(l, 1000, 1400)} chip ink="#10162a" />
        <GLine W={W} pts={[B, FOOT]} col={DK.gold} sw={4} dash="10 8" p={seg(l, 1800, 2600)} />
        <GRight W={W} V={FOOT} A={C} B={B} s={1.0} col={DK.gold} o={seg(l, 2400, 2800)} />
        <GSegLbl W={W} a={B} b={FOOT} s={`높이 ${TR.height}`} side={-1} off={46} size={28} col={DK.gold} o={seg(l, 2600, 3000)} chip ink="#10162a" />
        <GLine W={W} pts={[B, WT([TR.B[0], 0])]} col={DK.red} sw={3} dash="3 8" o={seg(l, 7800, 8400) * 0.9} glow={false} />
        <GLabel W={W} p={WT([TR.B[0] + 1.6, 0.8])} s={`${TR.B[1]} ✗`} size={26} chip={false} col={DK.red} o={seg(l, 7800, 8400)} />
        <Pts W={W} o={1} m />
      </g>
      <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  밑변과 높이" head="밑변 AC는 직선 y = 2 위" w={700}
        lines={[{ t: 3000, s: TR.M.bh, size: 36 }, { t: 5000, s: TR.M.area, size: 50 }, { t: 8200, s: TR.M.trap, size: 36, c: "soft" }]} lh={80}
        foot="높이는 B에서 밑변까지 — 터치라인까지(14)가 아니에요" />
    </g>
  );
}
/* ── 정리 ── */
function Wrap({ W, l, d }) {
  const o = Math.min(seg(l, 300, 900), 1 - seg(l, d - 900, d - 300));
  return (
    <g>
      <g opacity={o}>
        <Tri W={W} o={1} fill={1} />
        <Pts W={W} o={1} />
      </g>
      <Explain local={l} dur={d} kicker="정리" head={`패스 삼각형의 넓이 ${TR.area} m²`} w={700}
        lines={[{ t: 1300, s: "삼각형이 넓을수록", size: 50 }, { t: 2600, s: "상대가 공을 빼앗기 어려워요", size: 50 }]} />
    </g>
  );
}

export default { key: "soc-triangle", dur: TL.dur, world, overlay, tl: TL };
