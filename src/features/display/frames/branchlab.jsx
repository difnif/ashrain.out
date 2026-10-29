// ashrain.out — 교실 모니터 「액자」: 갈림길과 구슬 — 하나씩, 한꺼번에 (frames/branchlab.jsx)
// 해 보기(먼저): 단계(갈림길 수)와 구슬 수를 고르면 한 바퀴를 돈다.
//   ① 준비 — 구슬이 하나씩 주머니로 들어간다(주머니가 불룩해지고 개수가 오른다)
//   ② 하나씩 — 주머니 아래가 풀려 구슬이 하나씩 빠져나와 떨어진다(물리 엔진)
//   ③ 다시 준비 — 칸에 들어간 구슬이 주머니로 돌아간다
//   ④ 한꺼번에 — 주머니가 터지며 구슬이 우르르 떨어진다. 부딪혀 길이 정해진 곳에 번쩍 표시
//   ⑤ 비교 — 하나씩 · 한꺼번에를 300판씩 해서 모양별 비율을 이론값(서로 영향이 없을 때)과 견준다(예전 장면처럼)
//   주머니를 누르면(키보드 Enter) 기다리지 않고 바로 떨어뜨린다. 바퀴마다 시범 판이 바뀐다.
//   판 아래에는 구멍마다 그 구멍으로 가는 길의 수(초등) · 확률(중등)이, 첫 갈림목에는 「왼쪽·오른쪽 반반」이 붙어 있다.
// 풀이 보기: 두 갈래 길 · 갈림길이 늘어나면 · 구슬이 부딪히면 장면(../stories.js EXPLAIN.branch).
// 계산: ../branchlab.js · 물리: ../physics.js
import { memo, useCallback } from "react";
import { W, H, MText, Caption, SceneTitle, Path } from "../draw.jsx";
import { seg, E, clamp, fmt } from "../core.js";
import { EXPLAIN } from "../stories.js";
import { HOLE_NAMES, POST, shapeProbs, shapeOf } from "../branch.js";
import { comb } from "../galton.js";
import { simAt, runTo, MARBLE } from "../physics.js";
import {
  BLAB, OPEN, STAGE, labLayout, labWalls, labWorld, labRuns, freqOf, catName, catsOf, verdictOf, labTimeline, labAt, demoSeed, settled, countsOf,
} from "../branchlab.js";
import { LabShell, LabChrome, Stepper, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";

const LSK = "ash.display.lab.branch";
const DEF = { n: BLAB.NDEF, m: BLAB.MDEF };
const fixPrm = (p = {}) => ({ n: BLAB.NS.includes(p.n) ? p.n : BLAB.NDEF, m: BLAB.MS.includes(p.m) ? p.m : BLAB.MDEF });
const FIT = { top: 176, bottom: 706 };
const LIST = { x: 70, y: 300, lh: 66 };
const CARD = { x: 1090, w: 420, y: [262, 482], h: 186 };
const CH = { x0: 640, x1: 1440, yTop: 300, yBase: 566 };
const T = BLAB.TRIALS;
const pct = (p) => `${fmt(p * 100, 1)}%`;

/** 판을 화면에 놓는 자리: 주머니 목 ~ 바닥이 FIT 안에(너무 크지 않게) */
const PLACE = new Map();
function placeOf(L) {
  const k = `${L.n}|${L.m}`;
  if (!PLACE.has(k)) {
    const top = L.bag.neck - 0.4 * L.D, bot = L.yFloor;
    const s = Math.min(1.6, (FIT.bottom - FIT.top) / (bot - top));
    const X = 800, Y = FIT.top - s * top;
    PLACE.set(k, { s, X, Y, tf: (x, y) => [X + s * x, Y + s * y], tr: `translate(${X} ${Y}) scale(${s})` });
  }
  return PLACE.get(k);
}
const colsOf = (C) => [C.gold, C.coral, C.teal, C.sky, C.lilac, C.leaf];

/** 시범 판(바퀴 c)을 끝까지 돌린 결과 — 칸에 멈춘 자리 · 개수 · 부딪힌 곳 · 끝난 시각(세계 초) */
const FINAL = new Map();
export function demoFinal(n, m, mode, c) {
  const k = `${n}|${m}|${mode}|${c}`;
  if (!FINAL.has(k)) {
    const L = labLayout(n, m), Wd = labWorld(n, m, mode, demoSeed(c, mode));
    while (Wd.time < 40 && !settled(Wd)) runTo(Wd, Wd.time + 0.25);
    const { counts } = countsOf(Wd, L);
    FINAL.set(k, { x: [...Wd.x], y: [...Wd.y], counts, shape: shapeOf(counts), crowds: Wd.crowded || 0, end: Wd.lastFreeze ?? Wd.time });
    while (FINAL.size > 24) FINAL.delete(FINAL.keys().next().value);
  }
  return FINAL.get(k);
}
/** 모양의 이론 확률 — 기약분수(분모가 크면 백분율) */
function shapeFrac(n, m, key) {
  const o = shapeProbs(n, m).find((q) => q.key === key);
  if (!o) return "";
  return o.d <= 256 ? `{${o.n}/${o.d}}` : `약 ${pct(o.p)}`;
}

/* ══════════ 그리기 ══════════ */
export function BranchArt({ C, mode, P, at, onBag }) {
  const isM = mode === "m";
  const { n, m } = P;
  const L = labLayout(n, m), PL = placeOf(L), TL = at.TL, t = at.t, ts = at.ts, st = at.stage;
  const cols = colsOf(C);
  const cmp = st === "tally" || st === "verdict";
  const boardO = cmp ? 1 - seg(ts, 0, 700) : st === "prepA" ? seg(ts, 0, 700) : 1;
  const fA = demoFinal(n, m, "seq", at.c), fB = demoFinal(n, m, "sim", at.c);
  // 주머니 속 개수 · 날아드는 구슬 · 세계
  let bagCount = 0, bagState = "closed", burstK = 0, wob = 0, flies = [], world = null, worldMode = null;
  if (st === "prepA" || st === "prepB") {
    const per = st === "prepA" ? STAGE.prepPer : STAGE.prepBPer, t0 = st === "prepA" ? 900 : 700;
    for (let i = 0; i < m; i++) {
      const a = t0 + i * per, k = seg(ts, a, a + 640, E.io);
      if (k >= 1) { bagCount++; continue; }
      let from;
      if (st === "prepA") from = [(i - (m - 1) / 2) * 1.25 * L.D, (60 - PL.Y) / PL.s];
      else from = [fA.x[i], fA.y[i]];
      flies.push({ i, from, k });
    }
  } else if (st === "dropA" || st === "dropB") {
    const mode2 = st === "dropA" ? "seq" : "sim";
    const wms = Math.max(0, ts - STAGE.lead);
    world = simAt(`blab|${n}|${m}|${mode2}|${at.c}`, () => labWorld(n, m, mode2, demoSeed(at.c, mode2)), wms);
    worldMode = mode2;
    const wt = world.time;
    if (mode2 === "seq") { bagCount = m - world.nextSpawn; bagState = wt >= OPEN - 0.12 ? "open" : "closed"; }
    else { bagCount = wt >= OPEN ? 0 : m; bagState = wt >= OPEN ? "burst" : "closed"; burstK = clamp((wt - OPEN) / 0.55); }
    if (ts < STAGE.lead) wob = Math.sin(ts / 55) * 3.2 * seg(ts, 0, 200) * (1 - seg(ts, STAGE.lead - 150, STAGE.lead));
  } else bagCount = 0;
  const canTap = !!onBag && (st === "prepA" || st === "prepB");
  const doneA = st !== "prepA" && !(st === "dropA" && (!world || !settled(world))) && !cmp;
  const doneB = st === "dropB" && world && settled(world);
  return (
    <g>
      {/* ── 판 ── */}
      {boardO > 0.01 && (
        <g opacity={boardO}>
          <g transform={PL.tr}>
            <BoardWalls L={L} C={C} />
            {world && <WorldMarbles W={world} L={L} C={C} cols={cols} />}
            {world && worldMode === "sim" && <Sparks W={world} C={C} />}
            <Bag L={L} C={C} count={bagCount} m={m} state={bagState} k={burstK} wob={wob} uid={`${n}-${m}`} />
            {flies.map((q) => <FlyIn key={q.i} q={q} L={L} C={C} col={cols[q.i % cols.length]} />)}
          </g>
          <BagBadge L={L} PL={PL} C={C} count={bagState === "burst" ? m : bagCount} m={m} state={bagState} k={burstK} />
          <HoleLabels L={L} PL={PL} C={C} isM={isM} />
          <ForkNote L={L} PL={PL} C={C} isM={isM} o={st === "prepA" || st === "prepB" ? seg(ts, 400, 900) : 0} />
          {canTap && <BagHit L={L} PL={PL} onBag={onBag} />}
          {canTap && <TapHint L={L} PL={PL} C={C} ts={ts} s={st === "prepA" ? "← 눌러서 바로 떨어뜨리기" : "← 눌러서 바로 터뜨리기"} />}
        </g>
      )}
      {/* ── 왼쪽: 한 바퀴의 차례 ── */}
      <StageList C={C} st={st} m={m} isM={isM} />
      {/* ── 오른쪽: 이번 바퀴의 두 결과 ── */}
      {!cmp && doneA && <ResultCard i={0} C={C} title="하나씩" col={C.sky} f={fA} n={n} m={m} isM={isM} o={st === "dropA" ? seg(world ? world.time - (world.lastFreeze || 0) : 0, 0.2, 0.6) : 1} />}
      {!cmp && (doneB) && <ResultCard i={1} C={C} title={isM ? "한꺼번에(동시에)" : "한꺼번에"} col={C.coral} f={fB} n={n} m={m} isM={isM} sim
        o={seg(world.time - (world.lastFreeze || 0), 0.2, 0.6)} />}
      {/* ── 비교 ── */}
      {cmp && <Compare C={C} n={n} m={m} isM={isM} st={st} ts={ts} TL={TL} />}
      <Caption t={t} C={C} y={862} size={31} caps={capsOf(isM, n, m, TL, fA, fB, st === "verdict" ? verdictOf(n, m) : null)} />
    </g>
  );
}

function capsOf(isM, n, m, TL, fA, fB, V) {
  const a = TL.a, lead = STAGE.lead;
  const resA = Math.min(a.prepB - 200, a.dropA + lead + Math.round(fA.end * 1000) + 300);
  const resB = Math.min(a.tally - 200, a.dropB + lead + Math.round(fB.end * 1000) + 300);
  const holes = (f) => f.counts.map((c, k) => `${HOLE_NAMES[k]} ${c}개`).join(" · ");
  return [
    { t: 200, s: isM ? `구슬 ${m}개를 주머니에 담아요 — 먼저 하나씩 떨어뜨려 볼게요` : `구슬 ${m}개를 주머니에 담아요 — 먼저 하나씩 떨어뜨려 봐요` },
    { t: a.dropA + 150, s: isM ? "하나씩: 앞 구슬이 다 내려간 뒤에 다음 구슬 — 서로 만나지 않아요" : "하나씩: 앞 구슬이 다 내려간 뒤에 다음 구슬이 나와요" },
    { t: resA, s: isM ? `하나씩 결과 — ${catName(fA.shape, m)} (이 모양이 나올 확률 ${shapeFrac(n, m, fA.shape)})` : `하나씩 결과 — ${holes(fA)}` },
    { t: a.prepB + 150, s: isM ? "다시 주머니에 담아요 — 이번엔 주머니를 터뜨려 한꺼번에!" : "다시 주머니에 담아요 — 이번엔 주머니를 터뜨려요!" },
    { t: a.dropB + 150, s: isM ? "한꺼번에: 우르르 — 깔때기와 첫 갈림목에서 서로 밀어내요" : "한꺼번에: 우르르 — 구슬끼리 부딪혀요" },
    { t: resB, s: isM ? `한꺼번에 결과 — ${catName(fB.shape, m)}${fB.crowds ? ` · 부딪혀 길이 정해진 곳 ${fB.crowds}번` : ""}`
      : `한꺼번에 결과 — ${holes(fB)}${fB.crowds ? ` · 부딪힘 ${fB.crowds}번` : ""}` },
    { t: a.tally + 150, s: isM ? `같은 판에서 ${T}판씩 — 이론값(서로 영향이 없을 때)과 견주어 봐요` : `하나씩 ${T}번, 한꺼번에 ${T}번 해 보면?` },
    ...(V ? [{ t: a.verdict + 150, s: verdictText(V, m, isM) }] : []),
    { t: a.verdict + 5200, s: isM ? "곱의 법칙은 서로 영향을 주지 않을 때(독립)에만 쓸 수 있어요" : "구슬끼리 부딪히면 가능성이 달라질 수 있어요" },
  ].filter((q, i, arr) => i === 0 || q.t > arr[i - 1].t);
}
function verdictText(V, m, isM) {
  const lab = catName(V.best.key === "etc" ? V.best.key : V.best.key, m), dir = V.up ? "늘어요" : "줄어요";
  const name = V.best.key === "etc" ? "그 밖의 모양" : lab;
  const who = isM ? "동시에" : "한꺼번에";
  if (V.tier === 2) return isM ? `${who} 굴리면 ‹${name}›인 판이 크게 ${dir} — 부딪힘 때문이에요` : `${who} 굴리면 ‹${name}›인 판이 많이 ${dir}`;
  if (V.tier === 1) return `${who} 굴리면 ‹${name}›인 판이 조금 ${dir}`;
  return isM ? "이번엔 거의 같아요 — 갈림길을 여러 번 지나며 부딪힌 영향이 흐려졌어요" : "이번엔 거의 비슷해요 — 여러 번 갈라지며 영향이 흐려졌어요";
}

/** 벽: 갈림목 지붕은 살짝 채우고, 칸막이는 뾰족한 기둥, 깔때기 · 상자는 굵은 선 */
function BoardWalls({ L, C }) {
  return (
    <g>
      {labWalls(L).map((w, i) => {
        if (w.kind === "tip") return null;
        if (w.kind === "post") {
          const [[x, y], [, y1]] = w.pts, h = w.hw, tip = POST.tip;
          return <Path key={i} pts={[[x - h, y1], [x - h, y], [x, y - tip - 2], [x + h, y], [x + h, y1]]} closed stroke={C.ink} sw={1.5} fill={C.ink} fo={0.85} o={0.9} />;
        }
        return <Path key={i} pts={w.pts} closed={w.kind === "roof"} stroke={C.ink} sw={2 * w.hw} fill={w.kind === "roof" ? C.ink : "none"} fo={0.22} o={0.85} />;
      })}
    </g>
  );
}
function Marble({ x, y, r, col, num, C }) {
  return (
    <g>
      <circle cx={x} cy={y} r={r} fill={col} />
      <circle cx={x - r * 0.32} cy={y - r * 0.34} r={r * 0.3} fill="#fff" opacity={0.28} />
      <text x={x} y={y + r * 0.42} fontSize={r * 1.15} fontWeight={800} textAnchor="middle" fill={C.halo}>{num}</text>
    </g>
  );
}
function WorldMarbles({ W: Wd, L, C, cols }) {
  const out = [];
  for (let i = 0; i < Wd.n; i++) {
    if (Wd.st[i] === MARBLE.WAIT) continue;
    out.push(<Marble key={i} x={Wd.x[i]} y={Wd.y[i]} r={L.r} col={cols[i % cols.length]} num={i + 1} C={C} />);
  }
  return <g>{out}</g>;
}
/** 주머니로 날아드는 구슬(포물선) */
function FlyIn({ q, L, C, col }) {
  if (q.k <= 0 && q.from[1] < L.bag.neck - 200) return null;
  const to = [0, L.bag.neck + 0.3 * L.D];
  const x = q.from[0] + (to[0] - q.from[0]) * q.k;
  const lift = Math.min(160, Math.abs(q.from[1] - to[1]) * 0.35 + 40);
  const y = q.from[1] + (to[1] - q.from[1]) * q.k - lift * 4 * q.k * (1 - q.k) * (q.from[1] > to[1] ? 1 : 0.15);
  const o = 1 - seg(q.k, 0.86, 1);
  return <g opacity={o}><Marble x={x} y={y} r={L.r} col={col} num={q.i + 1} C={C} /></g>;
}

/** 주머니: 목을 묶은 자루. 개수만큼 불룩하고(목을 기준으로 줄어든다), 하나씩이면 아래가 열리고, 한꺼번에면 터진다 */
function Bag({ L, C, count, m, state, k, wob, uid }) {
  const D = L.D, b = L.bag;
  const f = state === "burst" ? 1 : 0.5 + 0.5 * (count / m);
  const neckY = b.neck;
  const mid = (b.top + b.bottom) / 2 + 0.2 * D, hw = b.hw;
  const body = `M${-0.36 * D} ${neckY} C${-0.36 * D} ${neckY + 0.5 * D} ${-hw} ${b.top + 0.1 * D} ${-hw} ${mid}`
    + ` C${-hw} ${b.bottom - 0.25 * D} ${-0.75 * D} ${b.bottom} 0 ${b.bottom} C${0.75 * D} ${b.bottom} ${hw} ${b.bottom - 0.25 * D} ${hw} ${mid}`
    + ` C${hw} ${b.top + 0.1 * D} ${0.36 * D} ${neckY + 0.5 * D} ${0.36 * D} ${neckY} Z`;
  const hook = <g>
    <line x1={0} y1={neckY - 2.2 * D} x2={0} y2={neckY - 0.25 * D} stroke={C.soft} strokeWidth={2.4} />
    <circle cx={0} cy={neckY - 2.2 * D} r={4} fill={C.soft} />
  </g>;
  if (state === "burst" && k >= 1) return hook;
  const tr = `rotate(${wob} 0 ${neckY - 2.2 * D}) translate(0 ${neckY}) scale(${f}) translate(0 ${-neckY})`;
  const fabric = (
    <g>
      <path d={body} fill={C.wood} stroke={C.woodEdge} strokeWidth={3} strokeLinejoin="round" />
      <path d={`M${-hw * 0.62} ${mid - 0.2 * D} Q0 ${mid + 0.35 * D} ${hw * 0.62} ${mid - 0.2 * D}`} fill="none" stroke={C.woodEdge} strokeWidth={1.6} strokeDasharray="5 5" opacity={0.6} />
      <path d={`M${-hw * 0.4} ${b.bottom - 0.45 * D} Q0 ${b.bottom - 0.1 * D} ${hw * 0.4} ${b.bottom - 0.45 * D}`} fill="none" stroke={C.woodEdge} strokeWidth={1.4} strokeDasharray="4 5" opacity={0.45} />
      <rect x={-0.5 * D} y={neckY - 0.08 * D} width={D} height={0.32 * D} rx={0.12 * D} fill={C.coral} stroke={C.woodEdge} strokeWidth={1.6} />
      {state === "open" && <ellipse cx={0} cy={b.bottom - 0.05 * D} rx={0.62 * D} ry={0.2 * D} fill={C.ink} opacity={0.75} />}
    </g>
  );
  if (state === "burst") {
    // 터짐: 천 조각 셋이 바깥으로 날아가며 사라진다 + 금빛 고리
    const pieces = [
      { clip: `M${-hw - 20} ${neckY - 10} L0 ${neckY - 10} L0 ${b.bottom + 20} L${-hw - 20} ${b.bottom + 20} Z`, dx: -1, dy: -0.4, rot: -28 },
      { clip: `M0 ${neckY - 10} L${hw + 20} ${neckY - 10} L${hw + 20} ${b.bottom + 20} L0 ${b.bottom + 20} Z`, dx: 1, dy: -0.4, rot: 28 },
    ];
    return (
      <g>
        {hook}
        <circle cx={0} cy={mid} r={(0.8 + 2.4 * E.out(k)) * D} fill="none" stroke={C.gold} strokeWidth={4} opacity={0.9 * (1 - k)} />
        {pieces.map((pc, i) => (
          <g key={i} opacity={1 - E.in(k)} transform={`translate(${pc.dx * 70 * E.out(k)} ${pc.dy * 50 * E.out(k)}) rotate(${pc.rot * k} 0 ${mid})`}>
            <clipPath id={`bagclip-${uid}-${i}`}><path d={pc.clip} /></clipPath>
            <g clipPath={`url(#bagclip-${uid}-${i})`}>{fabric}</g>
          </g>
        ))}
      </g>
    );
  }
  return <g>{hook}<g transform={tr}>{fabric}</g></g>;
}
/** 주머니 속 개수(화면 글자 크기로) */
function BagBadge({ L, PL, C, count, m, state, k }) {
  if ((state === "burst" && k > 0.25) || (state === "open" && count === 0)) return null;
  const f = state === "burst" ? 1 : 0.5 + 0.5 * (count / m);
  const yMid = L.bag.neck + (((L.bag.top + L.bag.bottom) / 2 + 0.2 * L.D) - L.bag.neck) * f;
  const [x, y] = PL.tf(0, yMid);
  const r = 24;
  return (
    <g opacity={state === "burst" ? 1 - k * 4 : 1} pointerEvents="none">
      <circle cx={x} cy={y} r={r} fill={C.paper} stroke={C.woodEdge} strokeWidth={2.5} />
      <text x={x} y={y + 9} fontSize={26} fontWeight={800} textAnchor="middle" fill={C.ink}>{count}</text>
    </g>
  );
}
function BagHit({ L, PL, onBag }) {
  const [x, y] = PL.tf(0, (L.bag.neck + L.bag.bottom) / 2);
  return <circle cx={x} cy={y} r={Math.max(70, PL.s * (L.bag.bottom - L.bag.neck) * 0.75)} fill="transparent" style={{ cursor: "pointer" }}
    onPointerDown={(e) => e.stopPropagation()} onClick={onBag} />;
}
function TapHint({ L, PL, C, ts, s }) {
  const [x, y] = PL.tf(L.bag.hw + 0.4 * L.D, (L.bag.neck + L.bag.bottom) / 2);
  const o = seg(ts, 1600, 2200) * (0.65 + 0.35 * Math.sin(ts / 280));
  return <MText x={x + 18} y={y + 8} s={s} size={20} weight={700} fill={C.soft} opacity={o} C={C} />;
}

/** 부딪혀 길이 정해진 자리에 잠깐 번쩍(세계 시각 0.7초) */
function Sparks({ W: Wd, C }) {
  if (!Wd.crowds) return null;
  return (
    <g>
      {Wd.crowds.map((c, k) => {
        const a = Wd.time - c.t;
        if (a < 0 || a > 0.7) return null;
        const p = a / 0.7, rr = 16 + 22 * E.out(p);
        return (
          <g key={k} opacity={1 - p}>
            {[0, 1, 2, 3, 4, 5, 6, 7].map((j) => {
              const an = (j / 8) * Math.PI * 2 + 0.3;
              return <line key={j} x1={c.x + Math.cos(an) * rr * 0.55} y1={c.y - 18 + Math.sin(an) * rr * 0.55}
                x2={c.x + Math.cos(an) * rr} y2={c.y - 18 + Math.sin(an) * rr} stroke={C.gold} strokeWidth={3.5} strokeLinecap="round" />;
            })}
          </g>
        );
      })}
    </g>
  );
}

/** 구멍 이름과 그 구멍으로 가는 길의 수(초등) · 확률(중등) */
function HoleLabels({ L, PL, C, isM }) {
  const y = PL.tf(0, L.yFloor)[1] + 34;
  const g = (a, b) => (b ? g(b, a % b) : a);
  return (
    <g pointerEvents="none">
      {L.bins.map((b, k) => {
        const x = PL.tf(b.xc, 0)[0], w = comb(L.n, k), tot = 2 ** L.n, d = g(w, tot);
        return (
          <g key={k}>
            <MText x={x} y={y} s={HOLE_NAMES[k]} size={26} weight={800} anchor="middle" fill={C.ink} C={C} />
            <MText x={x} y={y + 34} s={isM ? `{${w / d}/${tot / d}}` : `${w}가지`} size={isM ? 22 : 19} weight={700} anchor="middle" fill={C.teal} C={C} />
          </g>
        );
      })}
      <MText x={PL.tf(L.bins[0].x0, 0)[0] - 14} y={y + 34} s={isM ? "확률" : "길"} size={18} weight={700} anchor="end" fill={C.soft} C={C} />
    </g>
  );
}
/** 첫 갈림목: 왼쪽 · 오른쪽 반반 */
function ForkNote({ L, PL, C, isM, o }) {
  if (o <= 0.01) return null;
  const [x, y] = PL.tf(L.node(0, 0)[0], L.node(0, 0)[1]);
  const w = PL.s * L.dx * 0.5;
  return (
    <g opacity={o} pointerEvents="none">
      <MText x={x - w - 10} y={y + 10} s="{1/2}" size={24} weight={800} anchor="end" fill={C.teal} halo={C.halo} C={C} />
      <MText x={x + w + 10} y={y + 10} s="{1/2}" size={24} weight={800} fill={C.teal} halo={C.halo} C={C} />
    </g>
  );
}

/** 왼쪽: 한 바퀴의 차례 — 지금 차례는 금빛, 지난 차례는 ✓ */
function StageList({ C, st, m, isM }) {
  const items = [
    ["prepA", `주머니에 구슬 ${m}개`], ["dropA", "하나씩 떨어뜨리기"], ["prepB", "다시 주머니에"],
    ["dropB", "한꺼번에 — 주머니 터뜨리기"], ["cmp", `${T}${isM ? "판" : "번"}씩 모아 비교`],
  ];
  const cur = st === "tally" || st === "verdict" ? "cmp" : st;
  const ci = items.findIndex(([k]) => k === cur);
  return (
    <g pointerEvents="none">
      {items.map(([k, s], i) => {
        const y = LIST.y + i * LIST.lh, on = i === ci, done = i < ci;
        return (
          <g key={k} opacity={on ? 1 : done ? 0.55 : 0.4}>
            {on && <rect x={LIST.x - 16} y={y - 34} width={6} height={44} rx={3} fill={C.bar} />}
            <circle cx={LIST.x + 18} cy={y - 12} r={17} fill={on ? C.gold : "none"} stroke={on ? C.gold : C.soft} strokeWidth={2.4} />
            {done ? <MText x={LIST.x + 18} y={y - 3} s="⟪✓⟫" size={22} anchor="middle" fill={C.soft} C={C} />
              : <text x={LIST.x + 18} y={y - 4} fontSize={21} fontWeight={800} textAnchor="middle" fill={on ? C.halo : C.soft}>{i + 1}</text>}
            <MText x={LIST.x + 48} y={y - 3} s={s} size={on ? 27 : 24} weight={on ? 800 : 650} fill={on ? C.ink : C.soft} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 오른쪽: 이번 바퀴의 결과 — 구멍마다 개수 막대 · 모양 · (중등) 그 모양이 나올 이론 확률 · (한꺼번에) 부딪힌 횟수 */
function ResultCard({ i, C, title, col, f, n, m, isM, sim, o }) {
  if (o <= 0.01) return null;
  const x = CARD.x, y = CARD.y[i], w = CARD.w;
  const bx0 = x + 20, bx1 = x + 236, slot = (bx1 - bx0) / (n + 1);
  const bw = Math.min(38, slot - 12), base = y + 136, hMax = 66;
  const tx = x + w - 20;
  const notes = [];
  if (sim) notes.push([`부딪힘 ${f.crowds}번`, 22, C.ink, 760]);
  if (isM) { notes.push([sim ? "서로 영향이 없다면" : "이 모양이 나올 확률", 17, C.soft, 650]); notes.push([shapeFrac(n, m, f.shape), 22, C.ink, 760]); }
  return (
    <g opacity={o} pointerEvents="none">
      <rect x={x} y={y} width={w} height={CARD.h} rx={18} fill={C.halo} fillOpacity={0.55} stroke={col} strokeWidth={2.5} />
      <MText x={x + 22} y={y + 38} s={title} size={26} weight={800} fill={col} C={C} />
      <MText x={tx} y={y + 38} s={catName(f.shape, m)} size={26} weight={800} anchor="end" fill={C.ink} C={C} />
      {f.counts.map((c, k) => {
        const cx = bx0 + (k + 0.5) * slot, h = (c / m) * hMax;
        return (
          <g key={k}>
            {h > 0 && <rect x={cx - bw / 2} y={base - h} width={bw} height={h} rx={4} fill={col} fillOpacity={0.8} />}
            <line x1={cx - bw / 2 - 4} x2={cx + bw / 2 + 4} y1={base} y2={base} stroke={C.ink} strokeWidth={2} opacity={0.7} />
            <MText x={cx} y={base - h - 8} s={String(c)} size={19} weight={800} anchor="middle" fill={C.ink} C={C} />
            <MText x={cx} y={base + 24} s={HOLE_NAMES[k]} size={17} weight={700} anchor="middle" fill={C.soft} C={C} />
          </g>
        );
      })}
      {notes.map(([s2, sz, c2, wt], j) => <MText key={j} x={tx} y={y + 84 + j * 30} s={s2} size={sz} weight={wt} anchor="end" fill={c2} C={C} />)}
    </g>
  );
}

/** 비교: 모양별 비율 — 하나씩 · 한꺼번에 막대, 이론값(점선) · 판정 */
function Compare({ C, n, m, isM, st, ts, TL }) {
  const { x0, x1, yTop, yBase } = CH;
  const cats = catsOf(n, m);
  const o = seg(st === "tally" ? ts : 1e9, 300, 1000);
  const cnt = st === "tally" ? Math.round(T * seg(ts, 600, STAGE.tally - 700, E.sine)) : T;
  const rs = cnt > 0 ? labRuns(n, m, "seq", cnt) : [], rm = cnt > 0 ? labRuns(n, m, "sim", cnt) : [];
  const fs = freqOf(rs, cnt), fm = freqOf(rm, cnt);
  const V = st === "verdict" ? verdictOf(n, m) : null;
  const hiO = st === "verdict" ? seg(ts, 200, 800) : 0;
  const slot = (x1 - x0) / cats.length, bw = Math.min(54, slot * 0.3);
  const hh = (v) => v * (yBase - yTop);
  const lab = (c) => (c.key === "etc" ? "그 밖" : catName(c.key, m));
  return (
    <g opacity={o} pointerEvents="none">
      <MText x={x0} y={228} s={`‹${Math.min(cnt, T)}›${isM ? "판" : "번"}씩 해 보면`} size={32} weight={800} C={C} />
      <g>
        <rect x={x0} y={250} width={20} height={20} rx={4} fill={C.sky} opacity={0.85} />
        <MText x={x0 + 28} y={267} s="하나씩" size={21} weight={700} fill={C.soft} C={C} />
        <rect x={x0 + 120} y={250} width={20} height={20} rx={4} fill={C.coral} opacity={0.85} />
        <MText x={x0 + 148} y={267} s={isM ? "한꺼번에(동시에)" : "한꺼번에"} size={21} weight={700} fill={C.soft} C={C} />
        <line x1={x0 + 340} x2={x0 + 372} y1={260} y2={260} stroke={C.gold} strokeWidth={3} strokeDasharray="6 4" />
        <MText x={x0 + 380} y={267} s={isM ? "이론값(서로 영향이 없을 때)" : "계산값(부딪히지 않을 때)"} size={21} weight={700} fill={C.soft} C={C} />
      </g>
      {[0.25, 0.5, 0.75, 1].map((v) => (
        <g key={v}>
          <line x1={x0} x2={x1} y1={yBase - hh(v)} y2={yBase - hh(v)} stroke={C.grid} strokeWidth={1.5} />
          <MText x={x1 + 6} y={yBase - hh(v) + 6} s={`${v * 100}%`} size={15} weight={600} fill={C.soft} opacity={0.8} C={C} />
        </g>
      ))}
      <Path pts={[[x0 - 4, yBase], [x1 + 4, yBase]]} stroke={C.ink} sw={2.6} />
      {cats.map((c, k) => {
        const xc = x0 + slot * (k + 0.5);
        const vs = c.keys.reduce((a, q) => a + fs(q), 0), vm = c.keys.reduce((a, q) => a + fm(q), 0);
        const hiK = V && V.best.key === c.key ? hiO : 0;
        return (
          <g key={c.key}>
            {hiK > 0.01 && <rect x={xc - bw - 14} y={yTop - 30} width={2 * bw + 28} height={yBase - yTop + 30 + 64} rx={12} fill="none" stroke={C.gold} strokeWidth={3} opacity={hiK} />}
            {vs > 0 && <rect x={xc - bw - 3} y={yBase - hh(vs)} width={bw} height={hh(vs)} rx={3} fill={C.sky} fillOpacity={0.82} />}
            {vm > 0 && <rect x={xc + 3} y={yBase - hh(vm)} width={bw} height={hh(vm)} rx={3} fill={C.coral} fillOpacity={0.82} />}
            <line x1={xc - bw - 10} x2={xc + bw + 10} y1={yBase - hh(c.p)} y2={yBase - hh(c.p)} stroke={C.gold} strokeWidth={3.2} strokeDasharray="7 5" />
            {st === "verdict" && <>
              <MText x={xc - bw / 2 - 3} y={yBase - hh(vs) - 8} s={`${Math.round(vs * 100)}`} size={17} weight={700} anchor="middle" fill={C.sky} C={C} />
              <MText x={xc + bw / 2 + 3} y={yBase - hh(vm) - 8} s={`${Math.round(vm * 100)}`} size={17} weight={700} anchor="middle" fill={C.coral} C={C} />
            </>}
            <MText x={xc} y={yBase + 30} s={lab(c)} size={cats.length > 5 ? 19 : 22} weight={700} anchor="middle" C={C} />
            <MText x={xc} y={yBase + 56} s={pct(c.p)} size={17} weight={600} anchor="middle" fill={C.gold} C={C} />
          </g>
        );
      })}
      {V && <g opacity={seg(ts, 300, 900)}>
        <MText x={x0} y={700} s={`‹${V.best.key === "etc" ? "그 밖의 모양" : catName(V.best.key, m)}›인 판`} size={26} weight={700} fill={C.soft} C={C} />
        <MText x={x0} y={744} s={`${isM ? "이론" : "계산"} ${pct(V.best.p)} · 하나씩 ${pct(V.best.seq)} · ${isM ? "동시에" : "한꺼번에"} ‹${pct(V.best.sim)}›`} size={29} weight={700} C={C} />
      </g>}
    </g>
  );
}

/* ══════════ 해 보기 ══════════ */
function BranchTry({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui, viewSeg }) {
  const lab = useLabClock(LSK, DEF, fixPrm);
  const P = lab.prm;
  const layers = useModeLayers(mode);
  useTicker(() => {
    // 비교에 쓸 300판씩을 미리 조금씩 돌려 둔다(한 번에 몇 ms 씩)
    labRuns(P.n, P.m, "seq", T, 3);
    labRuns(P.n, P.m, "sim", T, 3);
    return !(lab.clk.current.held != null && layers.length < 2);
  });
  const e = lab.elapsed();
  const at = labAt(P.n, P.m, e);
  /** 준비 중이면 바로 떨어뜨리기 */
  const skip = useCallback(() => {
    const A = labAt(P.n, P.m, lab.elapsed()), base = A.c * A.TL.dur;
    if (A.stage === "prepA") lab.jump(base + A.TL.a.dropA);
    else if (A.stage === "prepB") lab.jump(base + A.TL.a.dropB);
    else { const i = A.TL.list.indexOf(A.stage); lab.jump(i < A.TL.list.length - 1 ? base + A.TL.a[A.TL.list[i + 1]] : base + A.TL.dur); }
  }, [P, lab]);
  const step = (key, list, d) => { const i = list.indexOf(P[key]); const j = clamp(i + d, 0, list.length - 1); if (j !== i) lab.setPrm({ [key]: list[j] }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: lab.restart, toggleFs, onMode, poke }),
    ArrowUp: () => step("n", BLAB.NS, 1), ArrowDown: () => step("n", BLAB.NS, -1),
    ArrowRight: () => step("m", BLAB.MS, 1), ArrowLeft: () => step("m", BLAB.MS, -1),
    Enter: () => { skip(); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="단계"><Stepper ui={ui} label="단계" value={P.n} options={BLAB.NS} unit="번" onChange={(v) => lab.setPrm({ n: v })} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="구슬" sep><Stepper ui={ui} label="구슬" value={P.m} options={BLAB.MS} unit="개" onChange={(v) => lab.setPrm({ m: v })} poke={poke} keyHint={["←", "→"]} /></Setting>
    </>
  );
  const title = { e: "갈림길과 구슬", m: "갈림길과 구슬" };
  const sub = `해 보기 · 갈림길 ${P.n}단계 · 구슬 ${P.m}개 · ${at.c + 1}바퀴째`;
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img"
        aria-label={`갈림길과 구슬 — ${P.n}단계, 구슬 ${P.m}개`}>
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <BranchArt C={C} mode={Ly.mode} P={P} at={at} onBag={Ly.top ? () => { skip(); } : null} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={lab.restart}
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} view={viewSeg} settings={settings}
        prog={at.t / at.TL.dur} />
    </>
  );
}

/** 갈림길과 구슬 액자 — 해 보기(먼저) · 풀이 보기 */
export function BranchFrame(props) {
  return <LabShell fkey="branch" label="갈림길과 구슬" explain={EXPLAIN.branch} renderTry={({ viewSeg }) => <BranchTry {...props} viewSeg={viewSeg} />} {...props} />;
}

/** 액자 목록의 작은 그림 — 주머니가 터져 구슬이 우르르 떨어지는 순간 */
export const BranchThumb = memo(function BranchThumb({ C, mode = "e" }) {
  const P = { n: 2, m: 4 };
  const TL = labTimeline(P.n, P.m);
  const at = labAt(P.n, P.m, TL.a.dropB + STAGE.lead + 620);
  return <BranchArt C={C} mode={mode} P={P} at={at} />;
});
