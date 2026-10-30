// 3D 축구 6 — 맨시티 vs 첼시: 적어도 한 골 (기대 득점 xG)
// 2D 장면(scenes/soc-xg.jsx)과 같은 수(facts-soccer.js 의 XG). 골대 가운데 O, 슈팅한 곳 S1(3, 4) · S2(−8, 6) · S3(16, 12).
// 세 슈팅은 모두 빗나간다(선방 · 골대 · 크로스바 위) — 「그래도 적어도 한 골이 들어갈 확률은?」. 기록표는 가상의 자료.
// 세계 좌표: 오른쪽 골대(X = 52.5). 2D 의 (옆 x, 골라인에서 앞 y) → 세계 (52.5 − y, x).
// 흐름: 슈팅 1 · 2 · 3(컷마다 다른 눈높이) → 멈춤(설명 1: 거리) → 설명 2(기록표의 칸 · 골 확률) → 골대 뒤에서 세 슈팅 다시 보기
//       → 설명 3(800경기로 생각하기 · 1 − 모두 빗나갈 확률)
import { timeline, actor, ballPath, shots, makeWorld, smooth } from "../script.js";
import { frameCam } from "../persp.js";
import { Labels, Trail, GLine, GLabel, GSegLbl, GRight, GTape, Explain, Lower, Tag, Panel, DK } from "../overlay.jsx";
import { ENTER, lerp3, drift, showO, extra, dribble } from "../kit3d.js";
import { UText, UTable, RowHi, Chain, chainW } from "../../kit-story.jsx";
import { seg, E } from "../../core.js";
import { XG } from "../../facts-soccer.js";

const WX = ([x, y]) => [52.5 - y, x];
const O = WX([0, 0]);
const SP = XG.SHOTS.map(WX);                                       // S1 · S2 · S3
const COL = ["gold", "teal", "coral"];

/* ── 세계 시각(ms): 세 슈팅은 따로 떨어진 장면(컷으로 잇는다) ── */
const SHOT = [1000, 5700, 10300];
const TABLEAU = 16000;                                             // 설명 구간: 세 선수가 저마다 슈팅한 자리에 선 한 장면
const ACTORS = [
  // 슈팅한 셋 — 공을 받아 차고, 아쉬워한다
  actor({ id: "S1", kit: "city", n: "S1", name: "", role: "main", keys: [[-9e4, 47.0, 4.4], [200, 47.0, 4.4], [900, SP[0][0] - 0.5, SP[0][1] + 0.3], [1800, 49.6, 2.4], [3000, 49.8, 2.2], [TABLEAU - 2000, 49.8, 2.2], [TABLEAU, SP[0][0] - 0.6, SP[0][1] + 0.4]],
    acts: [{ kind: "kick", at: SHOT[0], power: 0.9 }], seed: 0.2 }),
  actor({ id: "S2", kit: "city", n: "S2", name: "", role: "main", keys: [[-9e4, 41.5, -11.5], [4200, 41.5, -11.5], [5600, SP[1][0] - 0.6, SP[1][1] - 0.2], [6400, 48.2, -6.4], [7400, 48.4, -6.2], [TABLEAU - 2000, 48.4, -6.2], [TABLEAU, SP[1][0] - 0.7, SP[1][1] - 0.3]],
    acts: [{ kind: "kick", at: SHOT[1], power: 1 }], seed: 1.1 }),
  actor({ id: "S3", kit: "city", n: "S3", name: "", role: "main", keys: [[-9e4, 36.0, 18.0], [8800, 36.0, 18.0], [10200, SP[2][0] - 0.6, SP[2][1] + 0.1], [11000, 41.8, 15.4], [12400, 42.0, 15.2], [TABLEAU - 2000, 42.0, 15.2], [TABLEAU, SP[2][0] - 0.7, SP[2][1] + 0.4]],
    acts: [{ kind: "kick", at: SHOT[2], power: 1.1 }], seed: 2.3 }),
  extra("m1", "city", [44.5, -14.5], { role: "mate", keys: [[-9e4, 45.5, 13.5], [0, 45.5, 13.5], [600, 46, 12.5], [4000, 41, -16], [4900, 41.2, -15.5], [9000, 30, 20], [12000, 31, 19]] }),
  extra("m2", "city", [38.5, 4], { role: "mate", keys: [[-9e4, 39, 3.5], [12000, 39, 3.5]] }),
  // 상대(회색) — 막으러 다가간다
  extra("k", "rivalKeeper", [51.5, 0], { deep: 0.8, keys: [[-9e4, 51.4, 0.6], [0, 51.4, 0.6], [900, 51.3, 1.0], [3000, 51.4, 0], [5300, 51.4, -1.6], [7500, 51.4, -1.0], [9800, 51.4, 1.0], [12500, 51.4, 0.8]],
    acts: [{ kind: "dive", at: SHOT[0] + 120, dir: -1, h: 0.25 }, { kind: "dive", at: SHOT[1] + 150, dir: 1, h: 0.4 }], look: (tw, c) => [c.ball[0], c.ball[2]] }),
  extra("d1", "rival", [47, 6], { keys: [[-9e4, 46.6, 6.4], [600, 46.6, 6.4], [1300, 48.0, 4.6], [3000, 47.5, 4.0], [5000, 45.8, -5.4], [6000, 46.9, -6.8], [9000, 43, 12], [10600, 41.8, 14.2]] }),
  extra("d2", "rival", [45.5, -3], { keys: [[-9e4, 45.5, -3], [5000, 45.0, -5.0], [6000, 45.6, -7.2], [9000, 42.5, 6], [12000, 43, 9]] }),
  extra("d3", "rival", [44, 10], { keys: [[-9e4, 43.6, 10.4], [9200, 41.5, 13.5], [10400, 40.4, 15.0], [12000, 40.6, 14.8]], acts: [{ kind: "lunge", at: SHOT[2] - 80, dir: 1 }] }),
  extra("d4", "rival", [41, -7]),
];

/* ── 공 ── */
const BALL = ballPath([
  // 슈팅 1: 옆에서 내준 공 → 골키퍼가 막는다
  { t0: -200, t1: 850, kind: "ground", a: [45.6, 12.6], b: [SP[0][0], SP[0][1]] },
  { t0: SHOT[0], t1: SHOT[0] + 260, kind: "air", a: [SP[0][0], 0.2, SP[0][1]], b: [51.6, 0.55, 1.6] },
  { t0: SHOT[0] + 260, t1: SHOT[0] + 1200, kind: "air", a: [51.6, 0.55, 1.6], b: [47.2, 0.2, 6.4], h: 1.1 },
  // 슈팅 2: 몰고 들어가 찬 공이 골대(왼쪽 기둥)를 맞는다
  { t0: 4300, t1: SHOT[1], kind: "fn", f: dribble(ACTORS[1], 0.6) },
  { t0: SHOT[1], t1: SHOT[1] + 420, kind: "air", a: [SP[1][0], 0.2, SP[1][1]], b: [52.45, 1.25, -3.6] },
  { t0: SHOT[1] + 420, t1: SHOT[1] + 1300, kind: "air", a: [52.45, 1.25, -3.6], b: [47.2, 0.2, -9.6], h: 0.6 },
  // 슈팅 3: 먼 거리 — 크로스바 위로
  { t0: 8900, t1: SHOT[2], kind: "fn", f: dribble(ACTORS[2], 0.6) },
  { t0: SHOT[2], t1: SHOT[2] + 800, kind: "air", a: [SP[2][0], 0.2, SP[2][1]], b: [53.5, 3.5, 1.4], h: 1.2 },
  { t0: SHOT[2] + 800, t1: SHOT[2] + 1500, kind: "air", a: [53.5, 3.5, 1.4], b: [62, 5.2, 0.2], h: 0.6 },
  // 설명 때의 한 장면(세 선수가 슈팅한 자리에 함께 선다) — 공은 골대 가운데 O 에
  { t0: TABLEAU - 10, t1: TABLEAU + 9e4, kind: "fn", f: () => [O[0] - 0.3, 0.2, O[1]] },
]);

/* ── 박자표 ── */
const TL = timeline([
  { name: "intro", kind: "play", tw: [-3000, 300], dur: 3300 },
  { name: "shot1", kind: "play", tw: [300, 2400], dur: 2700 },
  { name: "shot2", kind: "play", tw: [4500, 7300], dur: 3100 },
  { name: "shot3", kind: "play", tw: [9000, 11900], dur: 3400 },
  { name: "ex1", kind: "hold", tw: TABLEAU, dur: 12600, spot: ["S1", "S2", "S3"] },
  { name: "ex2", kind: "hold", tw: TABLEAU, dur: 12000, spot: ["S1", "S2", "S3"] },
  { name: "replay", kind: "play", tw: [500, 1800], dur: 1900 },
  { name: "replay2", kind: "play", tw: [5300, 6600], dur: 1900 },
  { name: "replay3", kind: "play", tw: [9900, 11500], dur: 2200 },
  { name: "ex3", kind: "hold", tw: TABLEAU, dur: 14400, spot: ["S1", "S2", "S3"] },
]);
const A = TL.a, Bd = TL.b;
const twAt = (t) => TL.at(t).tw;

/* ── 카메라 ── */
const EX = frameCam([O, ...SP, WX([-10, 0]), WX([18, 0])], { yaw: 0, pitch: 62, fov: 34, box: [880, 200, 1480, 720] });
const BACK = (k, t) => ({ pos: lerp3([55.8, 1.72, -7.4], [55.9, 1.72, -6.6], E.sine(k)), at: [43.5, 1.3, 4.5], fov: 50 });
const RET = 1300;
const CAM = shots([
  // 1. 골대 뒤 눈높이 — 세 선수가 어디 있는지
  { t0: 0, t1: A.shot1, cam: BACK },   // 골대 옆, 골라인 뒤 눈높이
  // 2. 슈팅 1 — S1 옆, 골키퍼와 마주
  { t0: A.shot1, t1: A.shot2, cam: (k) => ({ pos: lerp3([42.6, 1.7, 3.2], [43.2, 1.7, 3.6], E.sine(k)), at: [51.5, 1.1, 1.0], fov: 42 }) },
  // 3. 슈팅 2 — 골라인 옆 눈높이(왼쪽 기둥 쪽)
  { t0: A.shot2, t1: A.shot3, cam: (k) => ({ pos: lerp3([55.2, 1.6, -9.4], [55.4, 1.6, -9.0], E.sine(k)), at: [45.5, 1.3, -6.0], fov: 46 }) },
  // 4. 슈팅 3 — S3 뒤 눈높이
  { t0: A.shot3, t1: A.ex1, cam: (k, t) => {
    const b = BALL.at(twAt(t));
    return { pos: lerp3([35.5, 1.75, 21.5], [36.2, 1.75, 21.0], E.sine(k)), at: lerp3([52, 1.6, 0], [b[0], Math.max(1.2, b[1]), b[2]], smooth(SHOT[2] + 100, SHOT[2] + 700, twAt(t)) * 0.6), fov: 38 };
  } },
  // 5. 설명 1 · 2 — 위에서(골대 가운데 O 와 세 자리)
  { t0: A.ex1, t1: Bd.ex2 - RET, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k, 0.03) },
  // 6. 다시 보기 — 골대 뒤 눈높이에서 세 슈팅을 이어서
  { t0: Bd.ex2 - RET, t1: A.ex3, blend: RET, cam: BACK },
  { t0: A.ex3, t1: TL.dur, blend: ENTER, ease: E.out, cam: (k) => drift(EX, k, 0.03) },
]);

export const world = makeWorld({ tl: TL, actors: ACTORS, ball: BALL, cam: CAM });

/* ══════════ 글자 ══════════ */
const MISS = ["골키퍼가 막았어요", "골대를 맞혔어요", "크로스바 위로"];
const LOWER = [
  { t0: 500, t1: A.shot1 - 150, a: "맨시티 vs 첼시 (가상의 경기)", b: "맨시티가 슈팅을 세 번 했어요" },
  { t0: A.shot1 + 1300, t1: A.shot2 - 150, a: "슈팅 1 · S1", b: MISS[0] },
  { t0: A.shot2 + 1500, t1: A.shot3 - 150, a: "슈팅 2 · S2", b: MISS[1] },
  { t0: A.shot3 + 1700, t1: A.ex1 - 100, a: "슈팅 3 · S3", b: MISS[2] },
  { t0: A.replay + 200, t1: A.ex3 - 150, a: "다시 보기 · 골대 뒤에서", b: "세 슈팅 모두 빗나갔어요 — 그래도 한 골쯤은?" },
];

function overlay(mode, t, C, P, W) {
  const isM = mode === "m";
  const { seg: Sg, local } = TL.at(t);
  const hold = Sg.kind === "hold";
  const dimK = smooth(0.05, 0.6, W.dim);
  const shotTw = SHOT.find((s) => W.tw > s && W.tw < s + 1500);
  return (
    <g>
      {!hold && shotTw && <Trail W={W} pts={BALL.trail(W.tw, 420)} o={1} sw={4} />}
      <Labels W={W} o={1 - dimK} />
      {hold && <Labels W={W} o={dimK * (Sg.name === "ex1" ? 1 : 0.85)} only={Sg.spot} />}
      {Sg.name === "ex1" && <Ex1 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "ex2" && <Ex2 W={W} l={local} d={Sg.dur} isM={isM} />}
      {Sg.name === "ex3" && <Ex3 W={W} l={local} d={Sg.dur} isM={isM} />}
      <Lower t={t} items={LOWER} />
      <Tag o={1 - dimK} s="재구성 화면 · 가상의 경기와 기록표(2D 장면과 같은 수)" />
    </g>
  );
}
function Pts({ W, o }) {
  return (
    <g opacity={o}>
      <GLabel W={W} p={O} s="O" size={28} dx={0} dy={-36} col="#F7F1E1" />
    </g>
  );
}
/* ── 설명 1: 거리 ── */
function Ex1({ W, l, d, isM }) {
  const o = showO(l, d);
  return (
    <g>
      <g opacity={o}>
        {XG.SHOTS.map(([x, y], i) => {
          const t0 = 1500 + i * 2400, col = DK[COL[i]], S = SP[i], F = WX([x, 0]);
          return isM ? (
            <g key={i}>
              <GLine W={W} pts={[O, F, S]} col={col} sw={3} dash="9 8" p={seg(l, t0, t0 + 700)} glow={false} />
              <GRight W={W} V={F} A={O} B={S} s={0.9} col={col} o={seg(l, t0 + 500, t0 + 900)} />
              <GSegLbl W={W} a={O} b={F} s={String(Math.abs(x))} side={x > 0 ? -1 : 1} off={22} size={26} col={col} o={seg(l, t0 + 500, t0 + 900)} />
              <GSegLbl W={W} a={F} b={S} s={String(y)} side={x > 0 ? -1 : 1} off={22} size={26} col={col} o={seg(l, t0 + 500, t0 + 900)} />
              <GLine W={W} pts={[O, S]} col={col} sw={5} p={seg(l, t0 + 900, t0 + 1500)} />
            </g>
          ) : (
            <GTape key={i} W={W} a={S} b={O} p={seg(l, t0, t0 + 1200, E.io)} s={XG.E.tape[i]} side={i === 1 ? -1 : 1} col={col} size={28} />
          );
        })}
        <Pts W={W} o={1} />
      </g>
      {isM ? (
        <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  피타고라스 정리" head="골대 가운데 O에서 슈팅한 곳까지" w={720}
          lines={[{ t: 3000, s: XG.M.d1, size: 34 }, { t: 7900, s: XG.M.d2, size: 40 }, { t: 9200, s: XG.E.d, size: 44 }]} lh={80}
          foot="골라인 방향(옆)과 앞쪽은 서로 수직" />
      ) : (
        <Explain local={l} dur={d} kicker="멈춰서 보기 1  ·  줄자로 재기" head="골대 가운데 O에서 슈팅한 곳까지" w={720}
          lines={[{ t: 2700, s: `S1  ‹${XG.D[0]} m›`, size: 50 }, { t: 5100, s: `S2  ‹${XG.D[1]} m›`, size: 50 }, { t: 7500, s: `S3  ‹${XG.D[2]} m›`, size: 50 }]} lh={82} />
      )}
    </g>
  );
}
/* ── 설명 2: 기록표 → 골 확률 ── */
const TX = 880, TCOL = [270, 120, 120], TRH = [56, 58, 58, 58], TY = 260;
function Ex2({ l, d, isM }) {
  const o = Math.min(seg(l, 300, 900), 1 - seg(l, d - 1650, d - 1250));
  const rowHi = (i) => seg(l, 1600 + i * 2300, 2100 + i * 2300);
  const rows = [
    ["골대 가운데에서 (m)", "슈팅", "골"].map((h) => ({ s: h, size: 24, weight: 750, fill: "ink", fo: 0.1 })),
    ...XG.TAB.map((r, i) => [
      { s: `${r[0]} 이상 ~ ${r[1]} 미만`, size: 26, weight: rowHi(i) > 0 ? 800 : 600, color: rowHi(i) > 0 ? COL[i] : undefined },
      { s: String(r[2]), size: 30, t: 500 + i * 120 },
      { s: String(r[3]), size: 30, t: 500 + i * 120, weight: rowHi(i) > 0 ? 800 : 600, color: rowHi(i) > 0 ? COL[i] : undefined },
    ]),
  ];
  return (
    <g>
      <g opacity={o}>
        <Panel x={TX - 34} y={TY - 70} w={600} h={330} />
        <UText x={TX} y={TY - 24} s="맨시티의 슈팅 기록 (가상의 자료)" size={24} weight={700} fill={DK.soft} C={DK} />
        {[0, 1, 2].map((i) => <RowHi key={i} x={TX} y={TY} cols={TCOL} rh={TRH} r={1 + i} C={DK} o={rowHi(i) * 0.9} col={COL[i]} />)}
        <UTable x={TX} y={TY} cols={TCOL} rh={TRH} C={DK} t={l} rows={rows} />
        {[0, 1, 2].map((i) => <UText key={i} x={TX} y={TY + 290 + i * 54} s={`S${i + 1}  ${XG.D[i]} m  →  ${isM ? XG.M.side[i] : XG.E.s[i].split("→")[1].trim()}`} size={30} weight={750}
          fill={DK[COL[i]]} opacity={rowHi(i)} C={DK} />)}
      </g>
      {isM ? (
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  계급의 상대도수" head="거리가 속한 계급의 골 확률" w={700}
          lines={[{ t: 7800, s: XG.M.p, size: 40 }, { t: 9200, s: XG.M.edge, size: 32, c: "soft" }]} lh={78}
          foot="10, 20은 경계값 — ‘이상’ 쪽 계급에 들어가요" />
      ) : (
        <Explain local={l} dur={d} kicker="멈춰서 보기 2  ·  기록표에서 칸 찾기" head="거리가 들어가는 칸의 골" w={700}
          lines={[{ t: 7800, s: "4번에 1번 · 8번에 1번 · 25번에 1번", size: 40 }, { t: 9200, s: `${XG.D[1]} m, ${XG.D[2]} m는 ‘이상’ 쪽 칸`, size: 36, c: "soft" }]} lh={78} />
      )}
    </g>
  );
}
/* ── 설명 3: 적어도 한 골 ── */
function Ex3({ l, d, isM }) {
  const o = Math.min(seg(l, 300, 900), 1 - seg(l, d - 1000, d - 500));
  const at = [0, 1, 2, 3].map((i) => 2600 + i * 1700);
  const vals = isM ? XG.M.chain : XG.E.chain.map((v, i) => (i === 0 ? `${v}경기` : v));
  const ops = isM ? XG.M.ops : XG.E.ops;
  const size = 40, gap = 150, bh = 70;
  const Wd = chainW(vals, size, gap, bh), x0 = 800 - Wd / 2, cy = 560;
  return (
    <g>
      <g opacity={o}>
        <Panel x={x0 - 50} y={cy - 130} w={Wd + 100} h={isM ? 210 : 290} />
        <UText x={x0} y={cy - 82} s={isM ? "모두 빗나갈 확률을 차례로 곱하면" : `${XG.N}경기로 생각하면 — 세 슈팅이 모두 빗나간 경기`} size={30} weight={700} fill={DK.soft} C={DK} />
        <Chain x={x0} y={cy} vals={vals} ops={ops} at={at} t={l} C={DK} size={size} gap={gap} bh={bh} last="teal" opSize={26} />
        {!isM && XG.E.goals.map((g, i) => {
          const a = seg(l, at[i + 1] - 200, at[i + 1] + 300);
          const ws = vals.map((v) => Math.max(bh * 1.4, measure(v, size) + size * 0.9));
          let x = x0; for (let k = 0; k <= i; k++) x += ws[k] + (k < i ? gap : 0);
          const mx = x + gap / 2;
          return a > 0 && <g key={i} opacity={a}>
            <GLineScreen x={mx} y0={cy + 14} y1={cy + 70} />
            <UText x={mx} y={cy + 110} s={`${["S1", "S2", "S3"][i]} ${g}`} size={30} weight={750} anchor="middle" fill={DK.gold} C={DK} />
          </g>;
        })}
      </g>
      {isM ? (
        <Explain local={l} dur={d} kicker="멈춰서 보기 3  ·  여사건" head="‘적어도 한 골’ = 1 − (모두 안 들어갈 확률)" side="center" y={170} w={1200}
          lines={[{ t: 9800, s: XG.M.none, size: 46, gap: 70 }, { t: 11200, s: XG.M.ans, size: 58 }]} lh={84} />
      ) : (
        <Explain local={l} dur={d} kicker="멈춰서 보기 3  ·  800경기로 생각하기" head="세 슈팅 중 적어도 한 골이 들어갈 가능성" side="center" y={170} w={1200}
          lines={[{ t: 9800, s: XG.E.hit, size: 46, gap: 70 }, { t: 11200, s: XG.E.per, size: 54 }]} lh={84} />
      )}
    </g>
  );
}
const measure = (s, size) => chainW([s], size, 0, 0) - size * 0.9;
function GLineScreen({ x, y0, y1 }) {
  return <line x1={x} x2={x} y1={y0} y2={y1} stroke={DK.gold} strokeWidth={2.6} strokeDasharray="5 5" />;
}

export default { key: "soc-xg", dur: TL.dur, world, overlay, tl: TL };
