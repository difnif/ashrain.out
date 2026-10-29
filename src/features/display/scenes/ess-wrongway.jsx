// 서술형 2 — 「경로」 역주행 차 앞의 선택 · 세 번째 길(점프)
// 왕복 2차로에서 역주행 차가 내 차로로 마주 온다. 멈춤·직진 → 역주행 차와 부딪힘(모두 무사 0), 왼쪽 → 반대 차로의 차 두 대가
// 각각 0.9로 나를 피함, 오른쪽 → 인도의 사람 두 명이 각각 0.7로 피함. 어느 쪽으로 비켜도 역주행 차는 뒷차와 마주치고 뒷차는 0.8로 피한다.
//   초등: 같은 순간이 1000번 온다면 — 왼쪽 1000 → 900 → 810 → 648번, 오른쪽 1000 → 700 → 490 → 392번 → 왼쪽.
//         점프(상상): 1000 → 900 → 720번, 720 > 648 → 가장 좋은 선택이 바뀐다.
//   중등: 0.9 × 0.9 × 0.8 = 0.648, 0.7 × 0.7 × 0.8 = 0.392, 점프 0.9 × 0.8 = 0.72 > 0.648
// 부딪히는 장면은 그리지 않는다. 점프로 사고를 피하는 장면은 상상이라고 자막에 밝힌다.
import { beats, seg, win, E, clamp } from "../core";
import { Arrow } from "../draw";
import { UText, UCaption, Chip, Chain, chainW, Person } from "../kit-story";
import { Car, Road, PathArrow, SideCar, bez, polyInfo } from "../kit-essay";
import { WRONGWAY as WW } from "../facts-essay";

const B = beats([["intro", 2800], ["who", 5200], ["stop", 3600], ["left", 7200], ["right", 7000], ["best", 3400], ["jump", 8800], ["hold", 2600]]);
const RD = { x0: 24, x1: 1576, top: 182, mid: 254, bot: 326, walk: 396 };
const UY = 218, LY = 290, SY = 354, PEDY = 388;        // 위 차로 · 아래 차로 · 인도로 올라선 차 · 사람의 발
const ME0 = [520, LY], REAR0 = [270, LY], WRONG0 = [1010, LY];
const OPP0 = [900, 1260], PED0 = [820, 1060];
const VM = 0.3, VW = 0.2, VR = 0.05, VO = 0.1;          // 1 ms 에 움직이는 px : 나 · 역주행 차 · 뒷차 · 반대 차로의 차
const GO = { left: 400, right: 400, jump: 1800 };        // 장면이 시작되고 차가 움직이기까지
const PATH = {
  left: [...bez(ME0, [610, LY], [610, UY + 8], [700, UY + 8], 18), [1500, UY + 8]],
  right: [...bez(ME0, [610, LY], [610, SY], [700, SY], 18), [1500, SY]],
  jump: [ME0, [1500, LY]],
};
const INFO = Object.fromEntries(Object.entries(PATH).map(([k, v]) => [k, polyInfo(v)]));
const near = (dx, a = 70, b = 200) => E.io(1 - clamp((Math.abs(dx) - a) / (b - a)));

/** 처음 달려오는 모습 → k = 1 에서 그 순간에 멈춘다 */
function intro(t) {
  const r = 1 - E.out(seg(t, 0, 2300, E.lin));
  return {
    me: { x: ME0[0] - 300 * r, y: LY, ang: 0, lift: 0 },
    rear: { x: REAR0[0] - 300 * r, y: LY },
    wrong: { x: WRONG0[0] + 240 * r, y: LY },
    opp: OPP0.map((x0) => ({ x: x0 + 100 * r, y: UY })),
    ped: PED0.map((x0, i) => ({ x: x0 + (i ? 20 : -20) * r, y: PEDY })),
  };
}
const FREEZE = intro(1e9);

/** 선택 하나를 다시 보기: u = 장면 안의 시각 */
function demo(kind, u) {
  const s = Math.max(0, u - GO[kind]), I = INFO[kind];
  const at = I.at(Math.min(1, (VM * s) / I.L));
  const me = { x: at.p[0], y: at.p[1], ang: s > 0 ? at.ang : 0, lift: 0 };
  const wx = Math.max(60, WRONG0[0] - VW * s), rx = REAR0[0] + VR * s;
  const rb = near(wx - rx, 40, 220);
  const wrong = { x: wx, y: LY - 8 * rb }, rear = { x: rx, y: LY + 30 * rb };
  const opp = OPP0.map((x0) => ({ x: x0 - VO * s, y: UY }));
  const ped = PED0.map((x0) => ({ x: x0, y: PEDY }));
  if (kind === "left") { let m = 0; for (const o of opp) { const k = near(me.x - o.x); o.y = UY - 24 * k; m = Math.max(m, k); } me.y += 8 * m; }
  if (kind === "right") { let m = 0; for (const p of ped) { const k = near(me.x - p.x, 60, 180); p.y = PEDY + 30 * k; m = Math.max(m, k); } me.y -= 6 * m; }
  if (kind === "jump") me.lift = Math.max(0, 1 - ((me.x - wrong.x) / 300) ** 2);     // 포물선으로 뛰어넘는다
  return { me, wrong, rear, opp, ped };
}
/** 처음으로 cond 가 참이 되는 시각(10 ms 간격) */
const first = (kind, cond) => { for (let u = 0; u < 9000; u += 10) if (cond(demo(kind, u))) return u; return 9000; };
const CROSS = {
  left: [first("left", (d) => d.me.x >= d.opp[0].x), first("left", (d) => d.me.x >= d.opp[1].x), first("left", (d) => d.wrong.x <= d.rear.x)],
  right: [first("right", (d) => d.me.x >= d.ped[0].x), first("right", (d) => d.me.x >= d.ped[1].x), first("right", (d) => d.wrong.x <= d.rear.x)],
  jump: [first("jump", (d) => d.me.x >= d.wrong.x), first("jump", (d) => d.wrong.x <= d.rear.x)],
};
// 수의 사슬이 한 칸씩 나아가는 시각(전체 시각)
const AT = {
  stop: [B.a.stop + 500, B.a.stop + 1500],
  left: [B.a.left + 300, ...CROSS.left.map((c) => B.a.left + c + 250)],
  right: [B.a.right + 300, ...CROSS.right.map((c) => B.a.right + c + 250)],
  jump: [B.a.jump + 900, B.a.jump + CROSS.jump[0] + 700, B.a.jump + CROSS.jump[1] + 250],
};
// 옆에서 본 점프의 자취
const TRAIL = Array.from({ length: 70 }, (_, i) => demo("jump", GO.jump + i * 40)).filter((d) => d.me.lift > 0.004).map((d) => [d.me.x, d.me.lift]);

function stateAt(t) {
  if (t < B.a.left) return { st: t < B.b.intro ? intro(t) : FREEZE, o: 1, kind: null };
  if (t < B.a.right) return { st: demo("left", t - B.a.left), o: 1 - seg(t, B.b.left - 600, B.b.left - 100), kind: "left" };
  if (t < B.a.best) return { st: demo("right", t - B.a.right), o: seg(t, B.a.right, B.a.right + 400) * (1 - seg(t, B.b.right - 600, B.b.right - 100)), kind: "right" };
  if (t < B.a.jump) return { st: FREEZE, o: seg(t, B.a.best, B.a.best + 400), kind: null };
  return { st: demo("jump", t - B.a.jump), o: 1, kind: "jump" };
}

const ROWY = { stop: 552, left: 618, right: 684, jump: 750 };
const LX = 72, CX = 268, CS = 32, GAP = 128, BH = 50;
const ORDER = ["stop", "left", "right", "jump"];
const strip = (s) => s.replace(/[‹›]/g, "");

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const { st, o, kind } = stateAt(t);
  const roadO = seg(t, 0, 600);
  const VALS = isM
    ? { stop: ["1", String(WW.p.stop)], left: WW.M.vals.left, right: WW.M.vals.right, jump: WW.M.vals.jump }
    : { stop: [String(WW.N), String(WW.p.stop)], left: WW.LEFT.map(String), right: WW.RIGHT.map(String), jump: WW.JMP.map(String) };
  const OPS = isM ? { stop: ["부딪힘"], ...WW.M.ops } : { stop: ["부딪힘"], ...WW.E.ops };
  const end = (k) => CX + chainW(VALS[k], CS, GAP, BH);
  const chipTxt = isM
    ? { opp: `피할 확률 ${WW.chips.opp}`, ped: `피할 확률 ${WW.chips.ped}`, rear: `피할 확률 ${WW.chips.rear}` }
    : { opp: `${WW.E.ops.left[0]} 피함`, ped: `${WW.E.ops.right[0]} 피함`, rear: `${WW.E.ops.left[2]} 피함` };
  // 「누가 피해야 하나」 이름표 — 멈춘 장면에서만
  const chipO = (t0) => seg(t, t0, t0 + 400) * (1 - seg(t, B.a.left, B.a.left + 400));
  // 세 갈래 화살표
  const arrO = seg(t, B.a.who + 3400, B.a.who + 4000) * (1 - seg(t, B.a.left, B.a.left + 400));
  const sideDim = 1 - 0.7 * seg(t, B.a.stop, B.a.stop + 500);
  const xO = seg(t, B.a.stop + 400, B.a.stop + 900);
  // 가장 좋은 선택 표시
  const bestL = seg(t, B.a.best + 200, B.a.best + 700) * (1 - seg(t, B.a.jump + 5600, B.a.jump + 6100));
  const bestJ = seg(t, B.a.jump + 5600, B.a.jump + 6100);
  const { me, wrong, rear, opp, ped } = st;
  const jumpArcO = seg(t, B.a.jump + 500, B.a.jump + 1100) * (1 - seg(t, B.a.jump + GO.jump - 200, B.a.jump + GO.jump + 300));
  const ringAt = (p, t0) => <Ring key={t0} p={p} t={t} t0={t0} C={C} />;
  return (
    <g>
      <Road {...RD} C={C} o={roadO} />
      {/* 사람 · 차 */}
      <g opacity={o * roadO}>
        {ped.map((p, i) => <Person key={i} x={p.x} y={p.y} h={40} col={C.lilac} C={C} />)}
        {opp.map((c, i) => <Car key={i} x={c.x} y={c.y} ang={180} C={C} col={i ? C.leaf : C.teal} />)}
        <Car x={rear.x} y={rear.y} ang={0} C={C} col={C.sky} label="뒷차" />
        <Car x={wrong.x} y={wrong.y} ang={180} C={C} col={C.red} label="역주행" />
        {me.lift > 0.01 && <ellipse cx={me.x + 8 * me.lift} cy={me.y + 12 * me.lift} rx={34} ry={17} fill="#000" opacity={0.28 * me.lift} />}
        <Car x={me.x} y={me.y - 18 * me.lift} ang={me.ang} C={C} col={C.gold} label="나" len={70 * (1 + 0.4 * me.lift)} wid={34 * (1 + 0.4 * me.lift)} />
        {kind === "left" && [ringAt([opp[0].x, opp[0].y], AT.left[1] - 250), ringAt([opp[1].x, opp[1].y], AT.left[2] - 250), ringAt([rear.x, rear.y], AT.left[3] - 250)]}
        {kind === "right" && [ringAt([ped[0].x, ped[0].y - 20], AT.right[1] - 250), ringAt([ped[1].x, ped[1].y - 20], AT.right[2] - 250), ringAt([rear.x, rear.y], AT.right[3] - 250)]}
        {kind === "jump" && [ringAt([me.x, me.y - 18 * me.lift], AT.jump[1] - 600), ringAt([rear.x, rear.y], AT.jump[2] - 250)]}
      </g>
      {/* 이름표: 누가 몇 번 피하나 */}
      {OPP0.map((x, i) => <Chip key={"o" + i} x={x} y={160} s={chipTxt.opp} size={22} C={C} o={chipO(B.a.who + 200 + i * 400)} />)}
      {PED0.map((x, i) => <Chip key={"p" + i} x={x} y={424} s={chipTxt.ped} size={22} C={C} o={chipO(B.a.who + 1300 + i * 400)} />)}
      <Chip x={REAR0[0]} y={362} s={chipTxt.rear} size={22} C={C} o={chipO(B.a.who + 2700)} />
      {/* 세 갈래 */}
      {arrO > 0 && <g opacity={arrO}>
        <g opacity={sideDim}>
          <PathArrow pts={bez([566, LY - 10], [630, LY - 10], [620, UY + 8], [690, UY + 8], 16)} stroke={C.ink} sw={4} />
          <PathArrow pts={bez([566, LY + 10], [630, LY + 10], [620, SY], [690, SY], 16)} stroke={C.ink} sw={4} />
          <Chip x={704} y={UY + 8} s={WW.word.left} size={22} C={C} anchor="start" />
          <Chip x={704} y={SY} s={WW.word.right} size={22} C={C} anchor="start" />
        </g>
        <Arrow p={[566, LY]} q={[930, LY]} stroke={C.red} sw={4} dash="12 9" />
        <Chip x={760} y={LY} s={WW.word.stop} size={22} C={C} fill={C.red} color={C.paper} />
        {xO > 0 && <UText x={956} y={LY + 12} s="⟪×r⟫" size={36} anchor="middle" opacity={xO} C={C} />}
      </g>}
      {/* 점프: 위로 */}
      {jumpArcO > 0 && <g opacity={jumpArcO}>
        <PathArrow pts={bez([560, LY - 8], [700, LY - 60], [880, LY - 60], [1062, LY - 8], 24)} stroke={C.gold} sw={4} dash="10 8" />
        <Chip x={810} y={LY - 46} s="위로" size={22} C={C} fill={C.gold} color={C.paper} />
      </g>}
      {/* 수의 사슬 */}
      <UText x={LX} y={490} s={isM ? WW.M.head : WW.E.head} size={24} weight={650} fill={C.soft} opacity={seg(t, B.a.stop, B.a.stop + 500)} C={C} />
      {bestL > 0 && <Best k="left" o={bestL} end={end("left")} C={C} s={isM ? "가장 높아요" : "가장 많아요"} />}
      {bestJ > 0 && <Best k="jump" o={bestJ} end={end("jump")} C={C}
        s={isM ? `${WW.M.vals.jump.at(-1)} > ${WW.M.vals.left.at(-1)}` : `${WW.JMP.at(-1)} > ${WW.LEFT.at(-1)}`} />}
      {ORDER.map((k) => {
        const a = seg(t, AT[k][0] - 200, AT[k][0] + 300);
        return a > 0 && (
          <g key={k}>
            <UText x={LX} y={ROWY[k] + 10} s={WW.word[k]} size={28} weight={750} fill={k === "stop" ? C.red : C.ink} opacity={a} C={C} />
            <Chain x={CX} y={ROWY[k]} vals={VALS[k]} ops={OPS[k]} at={AT[k]} t={t} C={C} size={CS} gap={GAP} bh={BH} opSize={21}
              last={k === "stop" ? "red" : "gold"} />
          </g>
        );
      })}
      <SideView t={t} C={C} st={kind === "jump" ? st : null} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: "왕복 2차로 — 역주행 차가 내 차로로 마주 달려와요" },
        { t: 2300, s: "그 순간을 멈춰 놓고 생각해 봐요" },
        ...(isM ? [
          { t: B.a.who, s: `반대 차로의 차는 ${WW.chips.opp}, 인도의 사람은 ${WW.chips.ped}의 확률로 나를 피해요` },
          { t: B.a.who + 2700, s: `내가 비키면 뒷차가 ${WW.chips.rear}의 확률로 역주행 차를 피해야 해요` },
          { t: B.a.stop, s: `멈추거나 직진하면 역주행 차와 부딪혀요 → 모두 무사할 확률 ${WW.p.stop}` },
          { t: B.a.left, s: "왼쪽으로 꺾으면 반대 차로의 두 차와 뒷차가 모두 피해야 해요" },
          { t: B.a.left + 3900, s: strip(WW.M.left) },
          { t: B.a.right, s: "오른쪽으로 꺾으면 인도의 두 사람과 뒷차가 모두 피해야 해요" },
          { t: B.a.right + 3900, s: strip(WW.M.right) },
          { t: B.a.best, s: `모두 무사할 확률이 가장 높은 선택 → ${WW.word[WW.best2]}` },
          { t: B.a.jump, s: "상상해 볼까요 — 차가 위로 뛰어올라 역주행 차를 넘는다면" },
          { t: B.a.jump + 2200, s: `점프 성공 ${WW.chips.jump} — 그래도 뒷차가 ${WW.chips.rear}의 확률로 피해야 해요` },
          { t: B.a.jump + 5600, s: strip(WW.M.jump) },
          { t: B.a.jump + 7600, s: WW.M.change.replace(/^→\s*/, "") },
        ] : [
          { t: B.a.who, s: `반대 차로의 차는 ${WW.E.ops.left[0]}, 인도의 사람은 ${WW.E.ops.right[0]} 나를 피해요` },
          { t: B.a.who + 2700, s: `내가 비키면 역주행 차는 뒷차와 마주쳐요 — 뒷차는 ${WW.E.ops.left[2]} 피해요` },
          { t: B.a.stop, s: `멈추거나 직진하면 역주행 차와 부딪혀요 → 모두 무사 ${WW.p.stop}번` },
          { t: B.a.left, s: `같은 순간이 ${WW.N}번 온다면 — 왼쪽으로 꺾으면?` },
          { t: B.a.left + 3900, s: strip(WW.E.left) },
          { t: B.a.right, s: "오른쪽으로 꺾으면 인도의 두 사람과 뒷차가 피해야 해요" },
          { t: B.a.right + 3900, s: strip(WW.E.right) },
          { t: B.a.best, s: `모두 무사한 횟수가 가장 많은 선택 → ${WW.word[WW.best2]}` },
          { t: B.a.jump, s: "상상해 볼까요 — 차가 위로 뛰어올라 역주행 차를 넘는다면" },
          { t: B.a.jump + 2200, s: `점프는 ${WW.E.ops.jump[0]} 성공 — 그래도 역주행 차는 뒷차 쪽으로 달려가요` },
          { t: B.a.jump + 5600, s: strip(WW.E.change) },
        ]),
        { t: B.a.jump + (isM ? 9600 : 7800), s: "점프로 피하는 건 상상 — 길이 하나 늘면 가장 좋은 선택이 달라져요" },
      ]} />
    </g>
  );
}

function Ring({ p, t, t0, C, r = 50 }) {
  const a = win(t, t0, t0 + 1300, 160, 600);
  if (a <= 0) return null;
  const k = seg(t, t0, t0 + 500, E.out);
  return <circle cx={p[0]} cy={p[1]} r={r * (0.7 + 0.3 * k)} fill="none" stroke={C.gold} strokeWidth={4} opacity={a} />;
}

function Best({ k, o, end, C, s }) {
  return (
    <g opacity={o}>
      <rect x={LX - 16} y={ROWY[k] - 27} width={end - LX + 32} height={56} rx={16} fill={C.gold} fillOpacity={0.14} />
      <rect x={LX - 26} y={ROWY[k] - 24} width={6} height={50} rx={3} fill={C.gold} />
      <Chip x={end + 30} y={ROWY[k]} s={s} size={24} C={C} anchor="start" fill={C.gold} color={C.paper} />
    </g>
  );
}

/** 옆에서 본 점프(점프 장면에서만) */
function SideView({ t, C, st }) {
  const a = seg(t, B.a.jump + 200, B.a.jump + 800);
  if (a <= 0 || !st) return null;
  const X0 = 1244, Y0 = 506, W = 326, H = 250, G = Y0 + H - 50;
  const ix = (x) => X0 + 24 + ((x - 150) / 1400) * (W - 48);
  const lift = (l) => G - 84 * l;
  const { me, wrong, rear } = st;
  const trail = TRAIL.map(([x, l]) => [ix(x), lift(l)]);
  return (
    <g opacity={a}>
      <rect x={X0} y={Y0} width={W} height={H} rx={18} fill={C.card} fillOpacity={0.55} stroke={C.cardEdge} strokeWidth={1.5} />
      <UText x={X0 + 20} y={Y0 + 38} s="옆에서 보면" size={22} weight={650} fill={C.soft} C={C} />
      <line x1={X0 + 16} x2={X0 + W - 16} y1={G} y2={G} stroke={C.soft} strokeWidth={2.4} />
      {trail.length > 1 && <path d={"M" + trail.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join("L")} fill="none" stroke={C.gold} strokeWidth={2.4} strokeDasharray="7 6" opacity={0.7} />}
      <SideCar x={ix(rear.x)} y={G} C={C} col={C.sky} dir={1} />
      <SideCar x={ix(wrong.x)} y={G} C={C} col={C.red} dir={-1} />
      {me.lift > 0.01 && <ellipse cx={ix(me.x)} cy={G + 2} rx={20 * (1 - 0.3 * me.lift)} ry={4} fill="#000" opacity={0.3 * me.lift} />}
      <SideCar x={ix(me.x)} y={lift(me.lift)} C={C} col={C.gold} dir={1} />
      <UText x={ix(me.x)} y={lift(me.lift) - 28} s="나" size={18} weight={750} anchor="middle" fill={C.gold} halo={C.halo} C={C} />
      <UText x={ix(wrong.x)} y={G + 28} s="역주행" size={18} weight={700} anchor="middle" fill={C.red} C={C} />
      <UText x={ix(rear.x)} y={G + 28} s="뒷차" size={18} weight={700} anchor="middle" fill={C.sky} C={C} />
    </g>
  );
}

export default {
  key: "ess-wrongway",
  dur: B.dur,
  title: { e: "역주행 차 앞에서 — 1000번 온다면", m: "역주행 차 앞에서 — 모두 무사할 확률" },
  sub: { e: "초등 · 일이 일어날 가능성 · 「경로」", m: "중2 · 확률의 곱 · 「경로」" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
