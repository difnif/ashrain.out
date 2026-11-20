// ashrain.out — 수학 호기심 액자: 농구로 보는 정비례 (frames/hoopfn.jsx)
// NBA 명경기 다섯(코비 81점 · 클레이 한 쿼터 37점 · 커리 12 3점슛 · 부커 70점 · 돈치치 73점)의 야투를 차례로:
//   슛한 자리 → 공이 림으로(위에서 내려다본 길) → 들어갔나 → 슛한 자리와 림을 지나는 직선 → 설명.
//   중등: 림 = 원점 — 모든 슛 직선이 원점을 지나 y = ax(정비례). 점이 림에 붙으면(레이업 · 덩크) 직선이 하나로 안 정해진다.
//   초등: 왼쪽 아래 구석(엔드라인 · 사이드라인)이 원점 — 좌표가 모두 양수, 림까지 가로 · 세로로 몇 칸.
// 경기 동안 슛 자리는 쌓이고(성공 ● · 실패 ×), 지난 직선은 옅게 남아 림을 중심으로 별처럼 퍼진다.
// 1칸 = 1피트. 자료: ../curio/data-nba.js(늦게 들여온다) — 자유투는 자료에 없어 점수 대신 야투 기록만 보인다.
import { memo, useEffect, useState } from "react";
import { W, H, MText, SceneTitle, Path } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, Chip, chipW, uWidth } from "../kit-story.jsx";
import { lineOf, lineSteps, runRiseSteps, pt, num, eqText, cycleAt, SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx, hashSeed, rng, fs } from "../curio/kit.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { FitText, Lines, Panel, Small, clipLine, BigChip, bigW, besideLine, pickSpot } from "./curio-kit.jsx";

const LSK = "ash.display.curio.hoopfn";
const GAMES = [-1, 0, 1, 2, 3, 4];
const GAME_SHORT = ["코비 81점", "클레이 37점", "커리 12개", "부커 70점", "돈치치 73점"];
const DEF = { game: -1, who: "all", sp: 1, ex: "full" };
const fixPrm = (p = {}) => ({
  game: GAMES.includes(p.game) ? p.game : -1,
  who: ["all", "star"].includes(p.who) ? p.who : "all",
  sp: SPEEDS.includes(p.sp) ? p.sp : 1,
  ex: fixEx(p.ex),
});

/* ── 무대: 하프 코트(림 왼쪽) · 설명 판(오른쪽) ── */
const S = 14.2, CX0 = 66, CY = 515;                  // 1피트 = 14.2px
const BX = -5.25, HX = 41.75;                        // 엔드라인 · 하프라인(림 기준 피트)
const px = (q) => [CX0 + (q[0] - BX) * S, CY - q[1] * S];
const COURT = [BX, -25, HX, 25];
/** 반코트 안에서 쏜 슛(하프라인 너머에서 던진 것은 그림 밖이라 뺀다 — 기록에는 남는다) */
const onCourt = (q) => q.X >= BX && q.X <= HX - 0.5 && Math.abs(q.Y) <= 25;
/** 이름표가 코트 밖(오른쪽 판 · 위 제목 · 아래 끝)으로 나가지 않게 */
const KB = { l: 66 + 4, r: 66 + (HX - BX) * S - 4, t: CY - 25 * S + 16, b: CY + 25 * S - 16 };
const fitX = (x, w) => clamp(x, KB.l + w / 2, KB.r - w / 2);
const PANEL = { x: 790, y: 150, w: 772, h: 720 };
/*
 * 최소화: 코트 전체(94 × 50 피트). 슛하는 반 코트를 180° 돌려 오른쪽에 두고, 나머지 반 코트를 왼쪽에 붙인다.
 * 180° 돌리면 점 (x, y) → (−x, −y) 라 원점(림)을 지나는 직선의 기울기 · 식은 상세와 같다.
 *   중등: 림 = 원점, 슛한 자리 (−X, −Y).  초등: 코트 왼쪽 아래 구석이 원점 — 림 (89, 25), 슛한 자리 (89 − X, 25 − Y).
 */
const FX = 88.75;                                    // 먼 쪽 엔드라인(림 기준 피트)
const MS = 12.6, MTOP = 236, MRY = MTOP + 25 * MS, MRX = 800 - (94 * MS) / 2 + FX * MS;   // 1피트 = 12.6px, 림의 화면 자리(코트 가운데 정렬)
const VFULL = { px, KB, mini: false, court: COURT, P0: (s, isM) => (isM ? [s.X, s.Y] : cornerOf([s.X, s.Y])), rim: (isM) => (isM ? [0, 0] : RIM_E) };
const VMINI = (() => {
  const p = (q) => [MRX - q[0] * MS, MRY + q[1] * MS];
  const l = MRX - FX * MS, r = MRX + 5.25 * MS;
  return { px: p, KB: { l: l + 4, r: r - 4, t: MRY - 25 * MS + 16, b: MRY + 25 * MS - 16 }, mini: true, court: [BX, -25, FX, 25],
    P0: (s, isM) => (isM ? [-s.X || 0, -s.Y || 0] : [89 - s.X, 25 - s.Y]), rim: (isM) => (isM ? [0, 0] : [89, 25]) };
})();

export const HC = { D: 7600, in: [0, 500], a: [400, 800], ball: [1000, 2200], res: [2200, 2700], line: [2700, 3600], out: [6900, 7600] };
const STEP_AT = [900, 1500, 2900, 3600, 4300, 5000];

/** 고른 경기 · 슈터의 슛 목록 [{ gi, s, n(그 경기 안 순번) }] */
const LIST = new WeakMap();
export function shotsOf(data, P) {
  const key = `${P.game}|${P.who}`;
  if (!LIST.has(data)) LIST.set(data, new Map());
  const memo = LIST.get(data);
  if (memo.has(key)) return memo.get(key);
  const out = [];
  data.games.forEach((g, gi) => {
    if (P.game >= 0 && P.game !== gi) return;
    g.shots.forEach((s, n) => { if (onCourt(s) && (P.who === "all" || s.pl === g.star)) out.push({ gi, s, n }); });
  });
  memo.set(key, out);
  return out;
}
/** 초등 좌표: 왼쪽 아래 구석이 원점(림 = (5, 25)) */
const cornerOf = (p) => [p[0] + 5, p[1] + 25];
export const RIM_E = [5, 25];
const near = (s) => Math.abs(s.X) <= 1 && Math.abs(s.Y) <= 1;

/** 최소화 화면의 한 줄: 중등은 식, 초등은 가파른 정도 */
export function hoopMiniLine(s, mode) {
  if (s.X === 0 && s.Y === 0) return mode === "m" ? "림 바로 밑 — 직선이 하나로 안 정해져요" : "림 바로 밑 — 점 하나";
  if (mode === "m") return eqText(lineOf([0, 0], [s.X, s.Y]));
  const L = runRiseSteps([89 - s.X, 25 - s.Y], [89, 25], { unit: "칸" });
  return ([...L].reverse().find((q) => q.hi) || L[L.length - 1]).s;
}
export function hoopSteps(s, mode) {
  if (mode === "m") {
    if (s.X === 0 && s.Y === 0) {
      return [{ s: "림 = 원점 O(0, 0)" }, { s: `슛한 자리 ${pt([0, 0])} — 림 바로 밑` }, { s: "점이 원점과 같아 직선이 하나로 안 정해져요", small: true },
        { s: "(한 점을 지나는 직선은 셀 수 없이 많다)", small: true }];
    }
    const { lines } = lineSteps([0, 0], [s.X, s.Y], { origin: true });
    return [{ s: "림 = 원점 O(0, 0)" }, { s: `슛한 자리 ${pt([s.X, s.Y])}` }, ...lines];
  }
  const A = cornerOf([s.X, s.Y]);
  if (s.X === 0 && s.Y === 0) return [{ s: `림 ${pt(RIM_E)}` }, { s: `슛한 자리 ${pt(A)} — 림 바로 밑` }, { s: "림과 같은 점 — 직선 대신 점 하나", small: true }];
  return [{ s: `림 ${pt(RIM_E)}` }, { s: `슛한 자리 ${pt(A)}` }, ...runRiseSteps(A, RIM_E, { unit: "칸" })];
}

/* ══════════ 코트 ══════════ */
function courtColors(C) {
  return C.name === "light"
    ? { floor: "#e8cfa2", floor2: "#e2c592", paint: "#d9b47e", line: "#fffaf0", lineO: 0.95, edge: "#b98d55", ink: "#3b2a16", halo: "#f1dcb5" }
    : { floor: "#3a2b22", floor2: "#352720", paint: "#46332a", line: "#efe2cc", lineO: 0.7, edge: "#5a4232", ink: "#f3e6cf", halo: "#2a1f19" };
}
const arc = (c, r, a0, a1, n = 40) => Array.from({ length: n + 1 }, (_, i) => { const a = ((a0 + ((a1 - a0) * i) / n) * Math.PI) / 180; return [c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)]; });
const pathD = (pts, P = px) => "M" + pts.map((q) => P(q).map((v) => v.toFixed(1)).join(" ")).join("L");
const COURT_LINES = (() => {
  const L = [];
  L.push([[BX, -25], [HX, -25], [HX, 25], [BX, 25], [BX, -25]]);
  L.push([[BX, -8], [13.75, -8], [13.75, 8], [BX, 8]]);
  L.push(arc([13.75, 0], 6, -90, 90, 24));
  const a3 = (Math.atan2(22, 8.95) * 180) / Math.PI;
  L.push([[BX, -22], [8.95, -22], ...arc([0, 0], 23.75, -a3, a3, 48), [8.95, 22], [BX, 22]]);
  L.push(arc([0, 0], 4, -90, 90, 20));
  L.push(arc([HX, 0], 6, 90, 270, 24));
  return L;
})();
/** 반 코트 하나(림 기준 좌표 → 화면 P) — far 면 먼 쪽 반 코트(하프라인에 대칭) */
function HalfCourt({ C, P, far }) {
  const K = courtColors(C);
  const T = far ? (q) => P([2 * HX - q[0], q[1]]) : P;
  const c1 = T([BX, 25]), c2 = T([HX, -25]);
  const a = [Math.min(c1[0], c2[0]), Math.min(c1[1], c2[1])], b = [Math.max(c1[0], c2[0]), Math.max(c1[1], c2[1])];
  const boards = [];
  for (let x = BX; x < HX; x += 3.2) { const p0 = T([x, 25]), p1 = T([x + 1.6, 25]); boards.push(<rect key={x} x={Math.min(p0[0], p1[0])} y={a[1]} width={Math.abs(p1[0] - p0[0])} height={b[1] - a[1]} fill={K.floor2} />); }
  const q1 = T([BX, 8]), q2 = T([13.75, -8]);
  const rim = T([0, 0]), bb = [T([-1.25, -3]), T([-1.25, 3])];
  return (
    <g>
      <rect x={a[0]} y={a[1]} width={b[0] - a[0]} height={b[1] - a[1]} fill={K.floor} />
      <g opacity={0.6}>{boards}</g>
      <rect x={Math.min(q1[0], q2[0])} y={Math.min(q1[1], q2[1])} width={Math.abs(q2[0] - q1[0])} height={Math.abs(q2[1] - q1[1])} fill={K.paint} />
      <g opacity={K.lineO}>{COURT_LINES.map((q, i) => <path key={i} d={pathD(q, T)} fill="none" stroke={K.line} strokeWidth={2.6} strokeLinejoin="round" />)}</g>
      <line x1={bb[0][0]} x2={bb[1][0]} y1={bb[0][1]} y2={bb[1][1]} stroke={K.line} strokeWidth={5} opacity={0.9} />
      <line x1={bb[0][0]} x2={rim[0]} y1={rim[1]} y2={rim[1]} stroke={K.line} strokeWidth={3} opacity={0.8} />
      <circle cx={rim[0]} cy={rim[1]} r={0.75 * Math.abs(P([1, 0])[0] - P([0, 0])[0])} fill="none" stroke="#f06a2b" strokeWidth={3.4} opacity={far ? 0.6 : 1} />
    </g>
  );
}
const Court = memo(function Court({ C, V = VFULL }) {
  const K = courtColors(C);
  if (V.mini) {
    const a = V.px([FX, 25]), b = V.px([BX, -25]);
    return (
      <g>
        <HalfCourt C={C} P={V.px} far />
        <HalfCourt C={C} P={V.px} />
        <rect x={Math.min(a[0], b[0])} y={Math.min(a[1], b[1])} width={Math.abs(b[0] - a[0])} height={Math.abs(b[1] - a[1])} rx={10} fill="none" stroke={K.edge} strokeWidth={2} />
      </g>
    );
  }
  return <HalfCourt C={C} P={px} />;
});

/** 최소화 눈금: 돌린 코트 위 격자(5피트) · 아래 · 왼쪽 가장자리에 숫자, 축(중등: 림을 지나는 x축 · y축) */
function MiniAxes({ C, mode, o, V }) {
  const K = courtColors(C), isM = mode === "m";
  const grid = [], lab = [];
  // 화면 좌표로 바로: 코트 왼쪽 아래 구석(먼 엔드라인 · 아래 사이드라인)
  const p = V.px, L0 = p([FX, 25]), R0 = p([BX, -25]);
  const x0 = Math.min(L0[0], R0[0]), x1 = Math.max(L0[0], R0[0]), y0 = Math.min(L0[1], R0[1]), y1 = Math.max(L0[1], R0[1]);
  // 중등 좌표(돌린 것): u = −X, v = −Y  → 화면 x = MRX + u MS, 화면 y = MRY − v MS
  const U = (u) => MRX + u * MS, Vv = (v) => MRY - v * MS;
  for (let u = -85; u <= 5; u += 5) grid.push(<line key={"gx" + u} x1={U(u)} x2={U(u)} y1={y0} y2={y1} stroke={K.ink} strokeOpacity={0.07} />);
  for (let v = -25; v <= 25; v += 5) grid.push(<line key={"gy" + v} x1={x0} x2={x1} y1={Vv(v)} y2={Vv(v)} stroke={K.ink} strokeOpacity={0.07} />);
  if (isM) {
    for (let u = -80; u <= 0; u += 10) if (u) lab.push(<MText key={"nx" + u} x={U(u)} y={MRY + 22} s={num(u)} size={15} weight={700} anchor="middle" fill={K.ink} halo={K.halo} opacity={0.8} C={C} />);
    for (let v = -20; v <= 20; v += 10) if (v) lab.push(<MText key={"ny" + v} x={MRX - 10} y={Vv(v) + 5} s={num(v)} size={15} weight={700} anchor="end" fill={K.ink} halo={K.halo} opacity={0.8} C={C} />);
  } else {
    for (let e = 10; e <= 90; e += 10) lab.push(<MText key={"nx" + e} x={x0 + e * MS} y={y1 - 8} s={String(e)} size={15} weight={700} anchor="middle" fill={K.ink} halo={K.halo} opacity={0.8} C={C} />);
    for (let e = 10; e <= 40; e += 10) lab.push(<MText key={"ny" + e} x={x0 + 8} y={y1 - e * MS + 5} s={String(e)} size={15} weight={700} anchor="start" fill={K.ink} halo={K.halo} opacity={0.8} C={C} />);
  }
  const ax = isM ? [x0, MRY, x1, MRY] : [x0, y1, x1, y1], ay = isM ? [MRX, y1, MRX, y0] : [x0, y1, x0, y0];
  const Op = isM ? [MRX, MRY] : [x0, y1];
  return (
    <g opacity={o}>
      {grid}
      <line x1={ax[0]} x2={ax[2] + 10} y1={ax[1]} y2={ax[3]} stroke={K.ink} strokeWidth={2.2} opacity={0.75} />
      <line x1={ay[0]} x2={ay[2]} y1={ay[1]} y2={ay[3] - 10} stroke={K.ink} strokeWidth={2.2} opacity={0.75} />
      <path d={`M${ax[2] + 18} ${ax[3]}l-11 -5.5v11z`} fill={K.ink} opacity={0.85} />
      <path d={`M${ay[2]} ${ay[3] - 18}l-5.5 11h11z`} fill={K.ink} opacity={0.85} />
      <MText x={ax[2] + 16} y={ax[3] - 12} s="x" size={22} anchor="end" fill={K.ink} halo={K.halo} C={C} />
      <MText x={ay[2] + 10} y={ay[3] - 4} s="y" size={22} fill={K.ink} halo={K.halo} C={C} />
      <MText x={Op[0] - 8} y={Op[1] + (isM ? 24 : -8)} s="O" size={17} weight={700} anchor="end" fill={K.ink} halo={K.halo} C={C} />
      {lab}
    </g>
  );
}
function HoopAxes({ C, mode, o, V = VFULL }) {
  if (o <= 0.001) return null;
  if (V.mini) return <MiniAxes C={C} mode={mode} o={o} V={V} />;
  const K = courtColors(C), isM = mode === "m";
  const O = isM ? [0, 0] : [-5, -25];
  const grid = [], lab = [];
  for (let x = -5; x <= 40; x += 5) { const p0 = px([x, -25]), p1 = px([x, 25]); grid.push(<line key={"gx" + x} x1={p0[0]} x2={p1[0]} y1={p0[1]} y2={p1[1]} stroke={K.ink} strokeOpacity={0.07} />); }
  for (let y = -25; y <= 25; y += 5) { const p0 = px([BX, y]), p1 = px([HX, y]); grid.push(<line key={"gy" + y} x1={p0[0]} x2={p1[0]} y1={p0[1]} y2={p1[1]} stroke={K.ink} strokeOpacity={0.07} />); }
  const X0 = px([isM ? BX : -5, O[1]]), X1 = px([HX, O[1]]), Y0 = px([O[0], -25]), Y1 = px([O[0], 25]);
  for (let x = -5; x <= 40; x += 10) {
    if (x === O[0]) continue;
    const q = px([x, O[1]]);
    lab.push(<MText key={"nx" + x} x={q[0]} y={q[1] + (isM ? 22 : -10)} s={num(isM ? x : x + 5)} size={15} weight={700} anchor="middle" fill={K.ink} halo={K.halo} opacity={0.8} C={C} />);
  }
  for (let y = -20; y <= 20; y += 10) {
    if (isM ? y === 0 : false) continue;
    const yy = isM ? y : y;
    const q = px([O[0], yy]);
    lab.push(<MText key={"ny" + y} x={q[0] + (isM ? -10 : 10)} y={q[1] + 5} s={num(isM ? y : y + 25)} size={15} weight={700} anchor={isM ? "end" : "start"} fill={K.ink} halo={K.halo} opacity={0.8} C={C} />);
  }
  const Op = px(O);
  return (
    <g opacity={o}>
      {grid}
      <line x1={X0[0]} x2={X1[0] + 10} y1={X0[1]} y2={X1[1]} stroke={K.ink} strokeWidth={2.2} opacity={0.75} />
      <line x1={Y0[0]} x2={Y1[0]} y1={Y0[1]} y2={Y1[1] - 10} stroke={K.ink} strokeWidth={2.2} opacity={0.75} />
      <path d={`M${X1[0] + 18} ${X1[1]}l-11 -5.5v11z`} fill={K.ink} opacity={0.85} />
      <path d={`M${Y1[0]} ${Y1[1] - 18}l-5.5 11h11z`} fill={K.ink} opacity={0.85} />
      <MText x={X1[0] + 24} y={X1[1] + 8} s="x" size={22} fill={K.ink} halo={K.halo} C={C} />
      <MText x={Y1[0] + 10} y={Y1[1] - 22} s="y" size={22} fill={K.ink} halo={K.halo} C={C} />
      <MText x={Op[0] - 8} y={Op[1] + (isM ? 24 : 22)} s="O" size={17} weight={700} anchor="end" fill={K.ink} halo={K.halo} C={C} />
      {lab}
    </g>
  );
}

/* ══════════ 장면 ══════════ */
/** 실패한 공이 튀어 나가는 자리(슛마다 정해진 씨앗) */
function bounceOf(gi, n) {
  const R = rng(hashSeed("hoop", gi, n));
  const a = (R() * 2 - 1) * Math.PI * 0.8, r = 3 + R() * 4;
  return [Math.max(BX + 1, r * Math.cos(a)), r * Math.sin(a)];
}
function Mark({ q, made, col, o = 1, r = 6.5, P = px }) {
  const p = P(q);
  if (made) return <circle cx={p[0]} cy={p[1]} r={r} fill={col} stroke="#0b0b0b" strokeOpacity={0.45} strokeWidth={1.2} opacity={o} />;
  const d = r * 0.8;
  return <path d={`M${p[0] - d} ${p[1] - d}L${p[0] + d} ${p[1] + d}M${p[0] + d} ${p[1] - d}L${p[0] - d} ${p[1] + d}`} stroke={col} strokeWidth={2.6} strokeLinecap="round" opacity={o} />;
}

export function HoopArt({ C, mode, P, data, at, ex = "full" }) {
  if (!data) return <MText x={420} y={500} s="경기 자료를 불러오는 중…" size={34} anchor="middle" fill={C.soft} C={C} />;
  const list = shotsOf(data, P);
  if (!list.length) return null;
  const { i, t } = at;
  const { gi, s, n } = list[i];
  const game = data.games[gi], teams = game.teams;
  const isM = mode === "m", mini = ex === "mini", V = mini ? VMINI : VFULL;
  const px = V.px, KB = V.KB, COURT = V.court;
  const fitX = (x, w) => clamp(x, KB.l + w / 2, KB.r - w / 2);
  const K = courtColors(C);
  const oOut = 1 - seg(t, HC.out[0], HC.out[1]);
  const col = teams[s.t].c;
  const shooter = [s.X, s.Y], sp = px(shooter), rim = px([0, 0]);
  // 지난 슛(이 경기에서 이번 슛 앞) — 자리 · 옅은 직선
  const prev = game.shots.slice(0, n);
  const marks = prev.map((q, j) => onCourt(q) ? <Mark key={j} q={[q.X, q.Y]} made={q.mk} col={teams[q.t].c} o={0.55} r={5} P={px} /> : null);
  const star = prev.slice(-60).map((q, j, arr) => {
    if (near(q) || !onCourt(q)) return null;
    const sg = clipLine([0, 0], [q.X, q.Y], COURT);
    if (!sg) return null;
    return <Path key={j} pts={[px(sg[0]), px(sg[1])]} stroke={teams[q.t].c} sw={1.6} o={0.05 + 0.1 * ((j + 1) / arr.length)} />;
  });
  // 공 — 슛한 자리 → 림(포물선은 크기와 그림자로)
  const kb = seg(t, HC.ball[0], HC.ball[1], E.io);
  const bpos = [lerp(sp[0], rim[0], kb), lerp(sp[1], rim[1], kb)];
  const hgt = 4 * kb * (1 - kb) * clamp(s.d / 25, 0.35, 1.2);
  const kr = seg(t, HC.res[0], HC.res[1], E.out);
  let ballEl = null;
  if (kb > 0 && oOut > 0.01) {
    let q = bpos, hh = hgt;
    if (kb >= 1) {
      if (s.mk) { q = rim; hh = 0; }
      else { const bo = px(bounceOf(gi, n)); q = [lerp(rim[0], bo[0], kr), lerp(rim[1], bo[1], kr)]; hh = 0.5 * 4 * kr * (1 - kr); }
    }
    const R = 9 * (1 + 0.9 * hh);
    ballEl = (
      <g opacity={kb >= 1 && s.mk ? 1 - kr : oOut}>
        <ellipse cx={q[0] + hh * 30} cy={q[1] + 6 + hh * 26} rx={9} ry={3.5} fill="#000" opacity={0.25} />
        <circle cx={q[0]} cy={q[1] - hh * 40} r={R} fill="#e8762c" stroke="#5a2a0c" strokeWidth={1.6} />
        <path d={`M${q[0] - R} ${q[1] - hh * 40}H${q[0] + R}M${q[0]} ${q[1] - hh * 40 - R}V${q[1] - hh * 40 + R}`} stroke="#5a2a0c" strokeWidth={1.2} opacity={0.7} />
      </g>
    );
  }
  const swish = s.mk && kb >= 1 ? kr : 0;
  // 직선
  const L = lineOf([0, 0], [s.X, s.Y]);
  const kl = seg(t, HC.line[0], HC.line[1], E.out);
  let lineEl = null;
  if (L.kind !== "pt" && kl > 0) {
    const sg = clipLine([0, 0], [s.X, s.Y], COURT);
    if (sg) {
      const A = px(sg[0]), B = px(sg[1]), mid = [(sp[0] + rim[0]) / 2, (sp[1] + rim[1]) / 2];
      const ext = (q) => [lerp(mid[0], q[0], kl), lerp(mid[1], q[1], kl)];
      lineEl = <Path pts={[ext(A), ext(B)]} stroke={C.name === "light" ? "#0f766e" : "#7fe3d3"} sw={3.2} dash="12 9" o={0.95 * oOut} />;
    }
  }
  const trail = kb > 0 ? <Path pts={[sp, [lerp(sp[0], rim[0], Math.min(1, kb)), lerp(sp[1], rim[1], Math.min(1, kb))]]} stroke={C.gold} sw={3.6} o={0.9 * oOut} /> : null;
  const kin = seg(t, HC.in[0], HC.in[1]), ka = seg(t, HC.a[0], HC.a[1]);
  const P0 = V.P0(s, isM);
  let up = sp[1] <= rim[1], chipY = sp[1] + (up ? -34 : 38);
  if (chipY < KB.t) { up = false; chipY = sp[1] + 38; }
  else if (chipY > KB.b) { up = true; chipY = sp[1] - 34; }
  let nameY = sp[1] + (up ? 38 : -22);
  if (nameY < KB.t - 4 || nameY > KB.b + 12) nameY = up ? chipY - 30 : chipY + 34;
  const CS = mini ? 26 : 24;   // 좌표 칩 — 그림에서 눈에 띄게
  const chipX = fitX(sp[0], chipW(pt(P0), CS)), nameX = fitX(sp[0], uWidth(s.pl, 19, 800));
  // 기울기 칩(금테 · 크게) — 슛 직선 옆, 슛 자리 · 림 · 이름표를 피해서
  const bs = mini ? 38 : 34;
  const slopeTxt = L.kind === "pt" || L.kind === "v" ? "" : isM ? `기울기 ${fs(L.m[0], L.m[1])}` : s.X && s.Y ? `세로 ÷ 가로 = ${fs(Math.abs(s.Y), Math.abs(s.X))}` : "";
  const sbw = slopeTxt ? bigW(slopeTxt, bs) : 0;
  const avoid0 = [{ x: sp[0], y: sp[1], w: 40, h: 40 }, { x: rim[0], y: rim[1], w: 34, h: 34 }, { x: chipX, y: chipY, w: chipW(pt(P0), CS), h: CS * 1.5 }, { x: nameX, y: nameY - 6, w: uWidth(s.pl, 19, 800), h: 24 }];
  const slopeAt = slopeTxt ? pickSpot([0.5, 0.35, 0.65, 0.25, 0.75].flatMap((f) => [besideLine(sp, rim, sbw, bs * 1.5, f, 1), besideLine(sp, rim, sbw, bs * 1.5, f, -1)]), sbw, bs * 1.5, avoid0, [KB.l, KB.t, KB.r, KB.b]) : null;
  const eq = isM ? eqText(L) : "";
  const eqPos = (() => {
    const sg = eq ? clipLine([0, 0], [s.X, s.Y], COURT) : null;
    if (!sg) return null;
    const A = px(sg[0]), B = px(sg[1]), w = chipW(eq, 24);
    const len = Math.hypot(B[0] - A[0], B[1] - A[1]) || 1, nx = -(B[1] - A[1]) / len, ny = (B[0] - A[0]) / len;
    const avoid = [sp, rim, [chipX, chipY], [nameX, nameY], ...(slopeAt ? [slopeAt, [slopeAt[0] - sbw / 3, slopeAt[1]], [slopeAt[0] + sbw / 3, slopeAt[1]]] : [])];
    let best = null, bd = -1;
    for (const u of [0.12, 0.25, 0.38, 0.5, 0.62, 0.75, 0.88]) for (const sd of [1, -1]) {
      const q = [fitX(lerp(A[0], B[0], u) + sd * nx * 30, w), clamp(lerp(A[1], B[1], u) + sd * ny * 30, KB.t, KB.b)];
      const d = Math.min(...avoid.map((v) => Math.hypot((v[0] - q[0]) / (w / 2 + 40), (v[1] - q[1]) / 40)));
      if (d > bd) { bd = d; best = q; }
    }
    return best;
  })();
  return (
    <g>
      <Court C={C} V={V} />
      <HoopAxes C={C} mode={mode} o={1} V={V} />
      {star}
      {marks}
      {lineEl}
      {trail}
      <g opacity={kin * oOut}>
        <circle cx={sp[0]} cy={sp[1]} r={16} fill="none" stroke={C.gold} strokeWidth={3} />
        <circle cx={sp[0]} cy={sp[1]} r={10} fill={col} stroke={teams[s.t].k} strokeWidth={2.4} />
        <UText x={nameX} y={nameY} s={s.pl} size={19} weight={800} anchor="middle" fill={K.ink} halo={K.halo} C={C} />
      </g>
      <Chip x={chipX} y={chipY} s={pt(P0)} size={CS} C={C} o={ka * oOut} />
      {slopeAt && <BigChip x={slopeAt[0]} y={slopeAt[1]} s={slopeTxt} size={bs} C={C} o={seg(t, HC.line[0] + 300, HC.line[1]) * oOut} />}
      {swish > 0 && <circle cx={rim[0]} cy={rim[1]} r={12 + 26 * swish} fill="none" stroke={C.gold} strokeWidth={3} opacity={1 - swish} />}
      {ballEl}
      {eq && eqPos && !mini && <Chip x={eqPos[0]} y={eqPos[1]} s={eq} size={24} C={C} o={seg(t, HC.line[1] - 300, HC.line[1] + 300) * oOut} />}
      {!mini && <HoopPanel C={C} mode={mode} game={game} s={s} n={n} t={t} idx={i} total={list.length} oOut={oOut} />}
      {mini && <HoopMini C={C} mode={mode} game={game} s={s} t={t} oOut={oOut} />}
    </g>
  );
}

/** 최소화 — 위 왼쪽: 경기 · 쿼터 · 시계, 위 오른쪽: 누가 · 무슨 슛 → 결과, 아래 가운데: 식(중등) 또는 가파른 정도(초등) */
function HoopMini({ C, mode, game, s, t, oOut }) {
  const qtr = s.q <= 4 ? `${s.q}쿼터` : "연장";
  const done = t >= HC.res[0];
  const a = `${game.title} · ${qtr} ${s.ml}:${String(s.sl).padStart(2, "0")} 남기고`;
  const b = `${s.pl} — ${s.pt}점 슛 · ${s.d}피트${done ? (s.mk ? " → 성공!" : " → 실패") : ""}`;
  const kin = seg(t, 0, 500) * oOut;
  const y0 = 176, hi = hoopMiniLine(s, mode);
  // 식 칩: 두 칩 사이에 들어가면 가운데, 아니면 둘째 줄 왼쪽
  const wa = chipW(a, 20), wb = chipW(b, 20), wh = chipW(hi, 24);
  const fits = 48 + wa + 24 + wh + 24 + wb + 48 < 1528;
  const hx = fits ? clamp(800, 48 + wa + 24 + wh / 2, 1552 - wb - 24 - wh / 2) : 48;
  return (
    <g>
      <Chip x={48} y={y0} s={a} size={20} C={C} anchor="start" o={kin} />
      <Chip x={1552} y={y0} s={b} size={20} C={C} anchor="end" color={done && s.mk ? C.gold : undefined} o={kin} />
      <Chip x={hx} y={fits ? y0 : 214} s={hi} size={24} C={C} color={C.gold} anchor={fits ? "middle" : "start"} o={seg(t, HC.line[1] - 200, HC.line[1] + 400) * oOut} />
    </g>
  );
}
function HoopPanel({ C, mode, game, s, n, t, idx, total, oOut }) {
  const { x, y, w, h } = PANEL, x0 = x + 26, mw = w - 52;
  const teams = game.teams;
  const done = t >= HC.res[0];
  // 야투 기록(이번 슛은 결과가 나온 뒤에 더한다)
  const fg = teams.map(() => [0, 0]); let st = [0, 0, 0, 0];
  game.shots.slice(0, n + (done ? 1 : 0)).forEach((q) => {
    fg[q.t][1]++; if (q.mk) fg[q.t][0]++;
    if (q.pl === game.star) { st[1]++; if (q.mk) st[0]++; if (q.pt === 3) { st[3]++; if (q.mk) st[2]++; } }
  });
  const qtr = s.q <= 4 ? `${s.q}쿼터` : "연장";
  const res = done ? (s.mk ? `성공! +${s.pt}` : "실패") : "";
  const lines = hoopSteps(s, mode).map((L, j) => ({ ...L, at: STEP_AT[Math.min(j, STEP_AT.length - 1)] + Math.max(0, j - STEP_AT.length + 1) * 700 }));
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <Small x={x0} y={y + 36} s={`${game.date} · ${teams[0].n} vs ${teams[1].n} · NBA 정규 시즌`} size={17} C={C} />
      <UText x={x0} y={y + 78} s={game.title} size={30} weight={800} C={C} />
      {teams.map((tm, j) => (
        <g key={j}>
          <circle cx={x0 + 9} cy={y + 112 + j * 32} r={8} fill={tm.c} stroke={tm.k} strokeWidth={1.6} />
          <UText x={x0 + 26} y={y + 119 + j * 32} s={`${tm.n}  야투 ${fg[j][0]} / ${fg[j][1]}`} size={20} weight={700} fill={C.ink} C={C} />
        </g>
      ))}
      <UText x={x0 + 410} y={y + 119} s={`${game.star}`} size={20} weight={800} fill={C.gold} C={C} />
      <UText x={x0 + 410} y={y + 151} s={`야투 ${st[0]}/${st[1]} · 3점 ${st[2]}/${st[3]}`} size={20} weight={700} fill={C.ink} C={C} />
      <line x1={x0} x2={x + w - 26} y1={y + 176} y2={y + 176} stroke={C.cardEdge} strokeWidth={1.2} />
      <UText x={x0} y={y + 214} s={`${qtr} ${s.ml}:${String(s.sl).padStart(2, "0")} 남기고`} size={22} weight={700} fill={mode === "m" ? C.teal : C.coral} C={C} />
      <g opacity={seg(t, 0, 400) * oOut}>
        <circle cx={x0 + 10} cy={y + 248} r={10} fill={teams[s.t].c} stroke={teams[s.t].k} strokeWidth={1.8} />
        <UText x={x0 + 30} y={y + 258} s={s.pl} size={28} weight={800} C={C} />
        <UText x={x0 + 30 + uWidth(s.pl, 28, 800) + 16} y={y + 257} s={`${s.ac} · ${s.pt}점 슛 · ${s.d}피트`} size={20} weight={650} fill={C.soft} C={C} />
        <UText x={x0} y={y + 300} s={res} size={26} weight={800} fill={s.mk ? C.gold : C.soft} opacity={seg(t, HC.res[0], HC.res[0] + 300)} C={C} />
      </g>
      <line x1={x0} x2={x + w - 26} y1={y + 326} y2={y + 326} stroke={C.cardEdge} strokeWidth={1.2} />
      <Lines x={x0} y={y + 374} lines={lines} t={t} C={C} size={28} lh={56} maxW={mw} o={oOut} hiSize={38} />
      <Small x={x0} y={y + h - 20} s={`슛 ${idx + 1} / ${total} · 이 경기 ${n + 1}번째 야투`} size={15} C={C} />
      <Small x={x + w - 26} y={y + h - 20} s="데이터: NBA.com 슛 위치 기록" size={14} C={C} anchor="end" />
    </g>
  );
}

/* ══════════ 액자 ══════════ */
let CACHE = null;
function useHoopData() {
  const [d, setD] = useState(CACHE);
  useEffect(() => {
    if (CACHE) return;
    let live = true;
    import("../curio/data-nba.js").then((m) => { CACHE = m.default; if (live) setD(m.default); }).catch(() => {});
    return () => { live = false; };
  }, []);
  return d;
}

export function HoopFnFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, DEF, fixPrm);
  const P = lab.prm;
  const data = useHoopData();
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const list = data ? shotsOf(data, P) : [];
  const at = cycleAt(lab.elapsed() * P.sp, HC.D, list.length || 1);
  const jumpShot = (d) => { const k = Math.max(0, at.k + d); lab.jump((k * HC.D) / P.sp); poke(); };
  const stepIn = (key, opts, d) => { const i = opts.indexOf(P[key]); const j = clamp(i + d, 0, opts.length - 1); if (j !== i) lab.setPrm({ [key]: opts[j] }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: lab.restart, toggleFs, onMode, poke }),
    ArrowRight: () => jumpShot(1), ArrowLeft: () => jumpShot(-1),
    ArrowUp: () => stepIn("game", GAMES, 1), ArrowDown: () => stepIn("game", GAMES, -1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="경기"><Stepper ui={ui} label="경기" value={P.game} options={GAMES} fmt={(v) => (v < 0 ? "전체" : GAME_SHORT[v])} onChange={(v) => lab.setPrm({ game: v })} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="슛" sep><Seg label="슛" value={P.who} options={[["all", "모두"], ["star", "주인공만"]]} onChange={(v) => lab.setPrm({ who: v })} poke={poke} /></Setting>
      <Setting label="풀이" sep><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
      <span className="dsp-sep" />
      <ui.Btn title="이전 슛 (←)" onClick={() => jumpShot(-1)}><ui.Ic d="M15 5 8 12l7 7" /></ui.Btn>
      <ui.Btn title="다음 슛 (→)" onClick={() => jumpShot(1)}><ui.Ic d="m9 5 7 7-7 7" /></ui.Btn>
    </>
  );
  const title = { e: "농구로 보는 좌표와 직선", m: "농구로 보는 정비례" };
  const sub = mode === "m" ? "림을 원점으로 — 슛 직선은 모두 원점을 지나는 y = ax" : "슛한 자리에서 림까지, 가로 · 세로로 몇 칸?";
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="농구 슛으로 보는 정비례">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={Ly.mode === mode ? sub : ""} C={C} mode={Ly.mode} />
            <HoopArt C={C} mode={Ly.mode} P={P} data={data} at={at} ex={P.ex} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={lab.restart}
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings}
        prog={list.length ? (at.i + at.t / HC.D) / list.length : 0} />
    </>
  );
}

/* 목록 그림 — 2016. 2. 27. 커리, 연장 위닝 3점슛(38피트) */
const THUMB = {
  games: [{ title: "스테픈 커리 3점슛 12개", date: "2016. 2. 27.", star: "스테픈 커리",
    teams: [{ n: "골든스테이트 워리어스", c: "#FFC72C", k: "#1D428A" }, { n: "오클라호마시티 썬더", c: "#2f9be0", k: "#ffffff" }],
    shots: [{ q: 1, ml: 9, sl: 31, t: 0, pl: "스테픈 커리", mk: 1, pt: 3, ac: "점프슛", X: 21, Y: -14, x: 21, y: -14, d: 25 },
      { q: 2, ml: 5, sl: 2, t: 1, pl: "러셀 웨스트브룩", mk: 0, pt: 2, ac: "풀업 점프슛", X: 12, Y: 9, x: 12, y: 9, d: 15 },
      { q: 3, ml: 1, sl: 12, t: 0, pl: "스테픈 커리", mk: 1, pt: 3, ac: "점프슛", X: 6, Y: 22, x: 6, y: 22, d: 23 },
      { q: 5, ml: 0, sl: 2, t: 0, pl: "스테픈 커리", mk: 1, pt: 3, ac: "점프슛", X: 37, Y: -6, x: 37, y: -6, d: 38 }] }],
};
export const HoopFnThumb = memo(function HoopFnThumb({ C, mode = "m" }) {
  return <HoopArt C={C} mode={mode} P={{ game: -1, who: "all", sp: 1 }} data={THUMB} at={{ i: 3, k: 3, t: 4600 }} />;
});
