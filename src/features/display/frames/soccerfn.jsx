// ashrain.out — 수학 호기심 액자: 축구로 보는 일차함수 (frames/soccerfn.jsx)
// 2022 FIFA 월드컵 실제 경기(StatsBomb 오픈 데이터 — 대한민국 네 경기 · 8강 네덜란드–아르헨티나 · 결승)의 슈팅 · 패스를
// 한 장면씩: 경기 · 전후반 · 시계 → 그 순간 선수 자리 → 출발점 → 공이 날아가 도착점 → 기울기 삼각형 → 두 점을 지나는 직선 → 설명.
//   중등: 경기장 가운데가 원점(사분면 넷) — 두 점을 지나는 직선의 식 y = ax + b 를 기울기 → 대입 → 식으로.
//   초등: 왼쪽 아래 구석이 원점(좌표가 모두 양수) — 가로 · 세로로 몇 칸, 가파른 정도 = 세로 ÷ 가로.
// 지난 장면의 직선은 옅게 남았다가 사라진다. 1칸 = 1야드(StatsBomb 경기장 120 × 80). 자료: ../curio/data-soccer.js(늦게 들여온다)
import { memo, useEffect, useState } from "react";
import { W, H, MText, SceneTitle, Path } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { mapper, Grass, PLines, arcW, Ball, GoalFlash } from "../kit-soccer.jsx";
import { UText, Chip, chipW, uWidth } from "../kit-story.jsx";
import { lineOf, lineSteps, runRiseSteps, pt, num, eqText, cycleAt, SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx, fs } from "../curio/kit.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { FitText, Lines, Panel, Small, clipLine, BigChip, bigW, besideLine, pickSpot, chipRect } from "./curio-kit.jsx";

const LSK = "ash.display.curio.soccerfn";
const MATCH_SHORT = ["우루과이전", "가나전", "포르투갈전", "브라질전", "네덜·아르", "결승"];
const MATCHES = [-1, 0, 1, 2, 3, 4, 5];
const DEF = { match: -1, kind: "all", sp: 1, ex: "full" };
const fixPrm = (p = {}) => ({
  match: MATCHES.includes(p.match) ? p.match : -1,
  kind: ["all", "s", "p"].includes(p.kind) ? p.kind : "all",
  sp: SPEEDS.includes(p.sp) ? p.sp : 1,
  ex: fixEx(p.ex),
});

/* ── 무대 자리: 상세 = 경기장 전체(왼쪽) · 설명 판(오른쪽) / 최소화 = 장면 쪽으로 다가간 카메라(판 없음) ── */
const S = 9, PX0 = 52, PY0 = 150;                  // 1야드 = 9px, 경기장 1080 × 720
const M = mapper({ ox: PX0 + 60 * S, oy: PY0 + 40 * S, s: S, flipY: true });
/** 그림 자리(V): 지도 M · 이름표가 나가면 안 되는 테두리 XL XR YT YB · 최소화면 판 box */
const VFULL = { M, XL: PX0 + 6, XR: PX0 + 120 * S - 6, YT: PY0 + 16, YB: PY0 + 80 * S - 16, mini: false };
const MBOX = [36, 150, 1564, 872];
/** 최소화 카메라: 출발점 · 도착점을 넉넉히(가로 40야드 · 세로 26야드 이상) 담는 확대 — 경기장 밖으로 너무 나가지 않게 */
const ZC = new WeakMap();
function zoomOf(sc) {
  if (ZC.has(sc)) return ZC.get(sc);
  const [bx0, by0, bx1, by1] = MBOX, aw = bx1 - bx0, ah = by1 - by0 - 100;   // 위 칩 두 줄 자리 100px
  const mg = 9;
  let x0 = Math.min(sc.a[0], sc.b[0]) - mg, x1 = Math.max(sc.a[0], sc.b[0]) + mg;
  let y0 = Math.min(sc.a[1], sc.b[1]) - mg, y1 = Math.max(sc.a[1], sc.b[1]) + mg;
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  const w = Math.max(40, x1 - x0), h = Math.max(26, y1 - y0);
  const s = clamp(Math.min(aw / w, ah / h), 8.4, 21);
  const vw = aw / s, vh = ah / s;
  const kx = vw >= 128 ? 0 : clamp(cx, -64 + vw / 2, 64 - vw / 2), ky = vh >= 88 ? 0 : clamp(cy, -44 + vh / 2, 44 - vh / 2);
  const z = { s, cx: kx, cy: ky };
  ZC.set(sc, z);
  return z;
}
function viewOf(z) {
  const [bx0, by0, bx1, by1] = MBOX, mx = (bx0 + bx1) / 2, my = (by0 + 100 + by1) / 2;
  const Mz = mapper({ ox: mx - z.cx * z.s, oy: my + z.cy * z.s, s: z.s, flipY: true });
  return { M: Mz, XL: bx0 + 8, XR: bx1 - 8, YT: by0 + 112, YB: by1 - 40, mini: true, box: MBOX };
}
const fitV = (V, x, w) => clamp(x, V.XL + w / 2, V.XR - w / 2);
const fitC = (x, w) => fitV(VFULL, x, w);
/** 좌표 이름표 자리: 상대 점의 반대쪽 옆 · 위아래, 판 밖으로 나가면 뒤집는다 */
function ptSpot(V, q, other, s, first, size = 19) {
  const w = chipW(s, size);
  let side = q[0] < other[0] ? -1 : q[0] > other[0] ? 1 : first ? -1 : 1;
  if (side > 0 && q[0] + 12 + w > V.XR) side = -1;
  else if (side < 0 && q[0] - 12 - w < V.XL) side = 1;
  const dy = size * 1.4;
  let y = q[1] + (q[1] <= other[1] ? -dy : dy + 4);
  if (y < V.YT) y = q[1] + dy + 4;
  else if (y > V.YB) y = q[1] - dy;
  return { x: q[0] + side * 12, y, anchor: side < 0 ? "end" : "start" };
}
const RECT = [-60, -40, 60, 40];
const PANEL = { x: 1162, y: 150, w: 400, h: 720 };

/* ── 한 장면의 박자(1× 기준 ms) ── */
export const SC = { D: 10000, in: [0, 600], a: [450, 850], ball: [1100, 2300], b: [2300, 2700], tri: [2700, 3300], line: [3300, 4300], out: [9200, 10000] };
const STEP_AT = [1000, 2400, 3600, 4500, 5300, 6100, 6900];

const PERIOD = { 1: "전반", 2: "후반", 3: "연장 전반", 4: "연장 후반", 5: "승부차기" };
const clock = (m, s) => `${m}:${String(s).padStart(2, "0")}`;

/** 고른 경기 · 장면 종류의 장면 목록 [{ mi, sc }] */
const LIST = new WeakMap();
export function scenesOf(data, P) {
  const key = `${P.match}|${P.kind}`;
  if (!LIST.has(data)) LIST.set(data, new Map());
  const memo = LIST.get(data);
  if (memo.has(key)) return memo.get(key);
  const out = [];
  data.matches.forEach((m, mi) => {
    if (P.match >= 0 && P.match !== mi) return;
    for (const sc of m.scenes) if (P.kind === "all" || sc.k === P.kind) out.push({ mi, sc });
  });
  memo.set(key, out);
  return out;
}

/** 초등 좌표(왼쪽 아래 구석이 원점) */
const corner = (p) => [p[0] + 60, p[1] + 40];

/** 그 장면의 설명 줄 */
export function soccerSteps(sc, mode) {
  const a = sc.a, b = sc.b;
  if (mode === "m") {
    const { L, lines } = lineSteps(a, b);
    return { L, lines: [{ s: `출발 ${pt(a)}` }, { s: `도착 ${pt(b)}` }, ...lines] };
  }
  const A = corner(a), B = corner(b);
  return { L: lineOf(a, b), lines: [{ s: `출발 ${pt(A)}` }, { s: `도착 ${pt(B)}` }, ...runRiseSteps(A, B)] };
}

/* ══════════ 경기장 ══════════ */
const PITCH_LINES = (() => {
  const L = [];
  L.push([[-60, -40], [60, -40], [60, 40], [-60, 40], [-60, -40]]);
  L.push([[0, -40], [0, 40]]);
  L.push(arcW([0, 0], 10, 0, 360, 48));
  for (const sx of [-1, 1]) {
    const g = 60 * sx;
    L.push([[g, -22], [g - 18 * sx, -22], [g - 18 * sx, 22], [g, 22]]);
    L.push([[g, -10], [g - 6 * sx, -10], [g - 6 * sx, 10], [g, 10]]);
    const spot = 48 * sx, half = 53.13;
    L.push(sx > 0 ? arcW([spot, 0], 10, 180 - half, 180 + half, 20) : arcW([spot, 0], 10, -half, half, 20));
  }
  for (const [cx, cy, a0] of [[-60, -40, 0], [60, -40, 90], [60, 40, 180], [-60, 40, 270]]) L.push(arcW([cx, cy], 1.2, a0, a0 + 90, 6));
  return L;
})();

const Pitch = memo(function Pitch({ C, M }) {
  const spots = [[0, 0], [-48, 0], [48, 0]].map((q) => M.p(q));
  return (
    <g>
      <Grass M={M} rect={RECT} C={C} band={10} along="x" rx={8} />
      <PLines M={M} C={C} lines={PITCH_LINES} w={2.4} />
      {spots.map((q, i) => <circle key={i} cx={q[0]} cy={q[1]} r={3.2} fill="#fff" opacity={0.7} />)}
      {[-1, 1].map((sx) => {
        const a = M.p([60 * sx, 4]), b = M.p([60 * sx + 2.2 * sx, -4]);
        return <rect key={sx} x={Math.min(a[0], b[0])} y={a[1]} width={Math.abs(b[0] - a[0])} height={b[1] - a[1]}
          fill="none" stroke="#fff" strokeOpacity={0.75} strokeWidth={2.6} />;
      })}
    </g>
  );
});

const light0 = (C) => (C.name === "light" ? "#2c3a22" : "#fff");
/** 좌표축 · 눈금 — 중등: 가운데 원점 · 초등: 왼쪽 아래 원점 */
function Axes({ C, mode, o, V }) {
  if (o <= 0.001) return null;
  if (V.mini) return <ZoomAxes C={C} mode={mode} o={o} V={V} />;
  const isM = mode === "m";
  const ox = isM ? 0 : -60, oy = isM ? 0 : -40;
  const xs = [], ys = [];
  for (let v = -60; v <= 60; v += 10) xs.push(v);
  for (let v = -40; v <= 40; v += 10) ys.push(v);
  const grid = [];
  xs.forEach((v) => { const a = M.p([v, -40]), b = M.p([v, 40]); grid.push(<line key={"gx" + v} x1={a[0]} x2={b[0]} y1={a[1]} y2={b[1]} stroke={light0(C)} strokeOpacity={0.09} strokeWidth={1.2} />); });
  ys.forEach((v) => { const a = M.p([-60, v]), b = M.p([60, v]); grid.push(<line key={"gy" + v} x1={a[0]} x2={b[0]} y1={a[1]} y2={b[1]} stroke={light0(C)} strokeOpacity={0.09} strokeWidth={1.2} />); });
  const X0 = M.p([-60, oy]), X1 = M.p([60, oy]), Y0 = M.p([ox, -40]), Y1 = M.p([ox, 40]);
  const light = C.name === "light";
  const ink = light ? "#2c3a22" : "#fff", hal = light ? "#e4efd8" : "#173126", lab = [];
  xs.forEach((v) => {
    if (v === ox || (v - ox) % 20 || Math.abs(v) === 60) return;
    const q = M.p([v, oy]);
    lab.push(<line key={"tx" + v} x1={q[0]} x2={q[0]} y1={q[1] - 5} y2={q[1] + 5} stroke={ink} strokeWidth={2} opacity={0.8} />);
    lab.push(<MText key={"nx" + v} x={q[0]} y={q[1] + (isM ? 22 : -10)} s={num(isM ? v : v + 60)} size={15} weight={700} anchor="middle" fill={ink} halo={hal} opacity={0.85} C={C} />);
  });
  ys.forEach((v) => {
    if (v === oy || (v - oy) % 20 || Math.abs(v) === 40) return;
    const q = M.p([ox, v]);
    lab.push(<line key={"ty" + v} x1={q[0] - 5} x2={q[0] + 5} y1={q[1]} y2={q[1]} stroke={ink} strokeWidth={2} opacity={0.8} />);
    lab.push(<MText key={"ny" + v} x={q[0] + (isM ? -9 : 10)} y={q[1] + 5} s={num(isM ? v : v + 40)} size={15} weight={700} anchor={isM ? "end" : "start"} fill={ink} halo={hal} opacity={0.85} C={C} />);
  });
  const O = M.p([ox, oy]);
  return (
    <g opacity={o}>
      {grid}
      <line x1={X0[0]} x2={X1[0] + 14} y1={X0[1]} y2={X1[1]} stroke={ink} strokeWidth={2.6} opacity={0.85} />
      <line x1={Y0[0]} x2={Y1[0]} y1={Y0[1]} y2={Y1[1] - 14} stroke={ink} strokeWidth={2.6} opacity={0.85} />
      <path d={`M${X1[0] + 22} ${X1[1]}l-12 -6v12z`} fill={ink} opacity={0.9} />
      <path d={`M${Y1[0]} ${Y1[1] - 22}l-6 12h12z`} fill={ink} opacity={0.9} />
      <MText x={X1[0] + 30} y={X1[1] + 8} s="x" size={24} fill={ink} halo={hal} C={C} />
      <MText x={Y1[0] + 10} y={Y1[1] - 26} s="y" size={24} fill={ink} halo={hal} C={C} />
      <MText x={O[0] - 8} y={O[1] + 22} s="O" size={18} weight={700} anchor="end" fill={ink} halo={hal} C={C} />
      {lab}
    </g>
  );
}

/** 최소화(확대) 눈금: 보이는 칸에 격자, 판 아래 · 왼쪽 가장자리에 자(눈금 숫자) — 축이 화면 밖이어도 좌표를 읽을 수 있게 */
function ZoomAxes({ C, mode, o, V }) {
  const isM = mode === "m", { M: Mz, box } = V;
  const [bx0, by0, bx1, by1] = box;
  const light = C.name === "light";
  const ink = light ? "#2c3a22" : "#fff", hal = light ? "#e4efd8" : "#173126";
  const ox = isM ? 0 : -60, oy = isM ? 0 : -40;
  const wx0 = (bx0 - Mz.ox) / Mz.s, wx1 = (bx1 - Mz.ox) / Mz.s, wy1 = (Mz.oy - by0) / Mz.s, wy0 = (Mz.oy - by1) / Mz.s;
  const st = Mz.s >= 15 ? 5 : 10;
  const grid = [], lab = [];
  for (let v = Math.ceil(wx0 / st) * st; v <= wx1; v += st) {
    const q = Mz.p([v, 0]);
    grid.push(<line key={"gx" + v} x1={q[0]} x2={q[0]} y1={by0} y2={by1} stroke={ink} strokeOpacity={v === ox ? 0.85 : 0.1} strokeWidth={v === ox ? 2.6 : 1.2} />);
    if (q[0] > bx0 + 40 && q[0] < bx1 - 20) lab.push(<MText key={"nx" + v} x={q[0]} y={by1 - 12} s={num(v - ox)} size={18} weight={750} anchor="middle" fill={ink} halo={hal} C={C} />);
  }
  for (let v = Math.ceil(wy0 / st) * st; v <= wy1; v += st) {
    const q = Mz.p([0, v]);
    grid.push(<line key={"gy" + v} x1={bx0} x2={bx1} y1={q[1]} y2={q[1]} stroke={ink} strokeOpacity={v === oy ? 0.85 : 0.1} strokeWidth={v === oy ? 2.6 : 1.2} />);
    if (q[1] > by0 + 116 && q[1] < by1 - 34) lab.push(<MText key={"ny" + v} x={bx0 + 12} y={q[1] + 6} s={num(v - oy)} size={18} weight={750} anchor="start" fill={ink} halo={hal} C={C} />);
  }
  const O = Mz.p([ox, oy]);
  const inBox = (q) => q[0] > bx0 + 20 && q[0] < bx1 - 20 && q[1] > by0 + 20 && q[1] < by1 - 20;
  return (
    <g opacity={o}>
      {grid}
      <rect x={bx0} y={by1 - 34} width={bx1 - bx0} height={34} fill={light ? "#f3f7ee" : "#0d1d16"} opacity={0.55} />
      <rect x={bx0} y={by0} width={50} height={by1 - by0 - 34} fill={light ? "#f3f7ee" : "#0d1d16"} opacity={0.55} />
      {lab}
      {inBox(O) && <MText x={O[0] - 8} y={O[1] + 24} s="O" size={20} weight={750} anchor="end" fill={ink} halo={hal} C={C} />}
      <MText x={bx1 - 14} y={by1 - 40} s="x" size={22} anchor="end" fill={ink} halo={hal} C={C} />
      <MText x={bx0 + 60} y={by0 + 128} s="y" size={22} fill={ink} halo={hal} C={C} />
    </g>
  );
}

/** 무한 직선을 경기장 안 선분으로 */
function pitchSeg(L, a) {
  if (L.kind === "pt") return null;
  const d = L.kind === "v" ? [0, 1] : [L.m[1], L.m[0]];
  return clipLine(a, d, RECT);
}

/* ══════════ 장면 ══════════ */
const lum = (hex) => { const n = parseInt(hex.slice(1), 16); return (0.299 * ((n >> 16) & 255) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255; };
const ink = (hex) => (lum(hex) < 0.4 ? "#e9edf6" : "#14171f");
function Players({ sc, teams, o, k, M, r0 = 8.5 }) {
  if (o <= 0.001 || !sc.ff) return null;
  const mine = teams[sc.t].c, theirs = teams[1 - sc.t].c;
  return (
    <g opacity={o}>
      {sc.ff.map(([x, y, tm, gk, act], i) => {
        if (act) return null;
        const q = M.p([clamp(x, -61.5, 61.5), clamp(y, -41.5, 41.5)]), col = tm ? mine : theirs;   // 360 자료의 줄 밖 자리(5,229명 중 29명)는 줄 바로 밖으로
        const kk = clamp(k * 1.6 - (i % 7) * 0.08);
        return (
          <g key={i} opacity={kk}>
            <ellipse cx={q[0] + 2} cy={q[1] + r0} rx={r0} ry={r0 * 0.36} fill="#000" opacity={0.25} />
            <circle cx={q[0]} cy={q[1]} r={gk ? r0 * 1.12 : r0} fill={col} stroke={ink(col)} strokeWidth={2} />
            {gk ? <circle cx={q[0]} cy={q[1]} r={r0 * 1.53} fill="none" stroke={col} strokeWidth={2} opacity={0.8} /> : null}
          </g>
        );
      })}
    </g>
  );
}

export function SoccerArt({ C, mode, P, data, at, ex = "full" }) {
  if (!data) return <MText x={600} y={480} s="경기 자료를 불러오는 중…" size={34} anchor="middle" fill={C.soft} C={C} />;
  const list = scenesOf(data, P);
  if (!list.length) return null;
  const { i, t } = at;
  const { mi, sc } = list[i];
  const match = data.matches[mi], teams = match.teams;
  const isM = mode === "m", mini = ex === "mini";
  // 최소화: 지난 장면 카메라에서 이번 장면 카메라로 0.9초에 걸쳐 옮겨 간다
  let V = VFULL;
  if (mini) {
    const z1 = zoomOf(sc), prev = list.length > 1 && (i > 0 || at.k > 0) ? list[(i - 1 + list.length) % list.length].sc : null;
    const z0 = prev ? zoomOf(prev) : z1, kz = seg(t, 0, 900, E.io);
    V = viewOf({ s: Math.exp(lerp(Math.log(z0.s), Math.log(z1.s), kz)), cx: lerp(z0.cx, z1.cx, kz), cy: lerp(z0.cy, z1.cy, kz) });
  }
  const Mv = V.M, fit = (x, w) => fitV(V, x, w);
  const cs = mini ? 28 : 24, ts = mini ? 26 : 23;   // 이름표 글자 크기(좌표 · 기울기 삼각형) — 그림에서 눈에 띄게
  const oOut = 1 - seg(t, SC.out[0], SC.out[1]);
  const a = Mv.p(sc.a), b = Mv.p(sc.b);
  const { L, lines } = soccerSteps(sc, mode);
  const mine = teams[sc.t].c;
  // 공: 출발 → 도착(크로스 · 롱패스는 높이 뜬다)
  const kb = seg(t, SC.ball[0], SC.ball[1], E.io);
  const lofty = /크로스|롱패스|코너킥|프리킥|로빙|방향 전환/.test(sc.ty) ? 0.9 : sc.k === "s" ? 0.25 : 0.12;
  const bp = [lerp(a[0], b[0], kb), lerp(a[1], b[1], kb)];
  const scored = sc.g && t >= SC.ball[1];
  // 지난 장면의 직선(옅게)
  const ghosts = [];
  for (let g = 1; g <= 5; g++) {
    const j = i - g;
    if (j < 0 && at.k < g) break;
    const it = list[((j % list.length) + list.length) % list.length];
    const Lg = lineOf(it.sc.a, it.sc.b), sg = pitchSeg(Lg, it.sc.a);
    if (!sg) continue;
    const col = data.matches[it.mi].teams[it.sc.t].c;
    ghosts.push(<Path key={g} pts={[Mv.p(sg[0]), Mv.p(sg[1])]} stroke={col} sw={2.4} o={(0.34 - g * 0.055) * (g === 1 ? 1 - 0.6 * seg(t, 0, 2000) : 1)} />);
  }
  // 이번 직선(그래프)
  const full = pitchSeg(L, sc.a);
  const kl = seg(t, SC.line[0], SC.line[1], E.out);
  let lineEl = null;
  if (full && kl > 0) {
    const A = Mv.p(full[0]), B = Mv.p(full[1]);
    const mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    const ext = (q) => [lerp(mid[0], q[0], kl), lerp(mid[1], q[1], kl)];
    lineEl = <Path pts={[ext(A), ext(B)]} stroke={C.name === "light" ? "#0f766e" : "#7fe3d3"} sw={mini ? 3.8 : 3.2} dash="12 9" o={0.95 * oOut} />;
  }
  // 기울기 삼각형: 출발 → (도착 x, 출발 y) → 도착
  const kt = seg(t, SC.tri[0], SC.tri[1]);
  const corner3 = [b[0], a[1]];
  const dxs = sc.b[0] - sc.a[0], dys = sc.b[1] - sc.a[1];
  const sx = isM ? `x ${dxs > 0 ? "+" : "−"}${Math.abs(dxs)}` : `가로 ${Math.abs(dxs)}칸`;
  const sy = isM ? `y ${dys > 0 ? "+" : "−"}${Math.abs(dys)}` : `세로 ${Math.abs(dys)}칸`;
  const triEl = kt > 0 && dxs && dys ? (
    <g opacity={kt * oOut}>
      <Path pts={[a, corner3, b]} stroke="#fff" sw={2.4} dash="7 6" o={0.9} />
      <Chip x={fit((a[0] + b[0]) / 2, chipW(sx, ts))} y={clamp(a[1] + (dys > 0 ? 1 : -1) * ts * 1.35, V.YT, V.YB)} s={sx} size={ts} C={C} />
      <Chip x={fit(b[0] + (dxs > 0 ? 1 : -1) * (chipW(sy, ts) / 2 + 12), chipW(sy, ts))} y={clamp((a[1] + b[1]) / 2, V.YT, V.YB)} s={sy} size={ts} C={C} />
    </g>
  ) : null;
  // 점 · 좌표 이름표
  const A0 = isM ? sc.a : corner(sc.a), B0 = isM ? sc.b : corner(sc.b);
  const ka = seg(t, SC.a[0], SC.a[1]), kbb = seg(t, SC.b[0], SC.b[1]);
  const la = ptSpot(V, a, b, pt(A0), true, cs), lb = ptSpot(V, b, a, pt(B0), false, cs);
  // 식 이름표(중등): 직선 위, 도착점에서 조금 떨어진 곳
  const eq = eqText(L);
  const eqSpot = (avoid) => {
    if (!(isM && full && eq && !mini)) return null;
    const A = Mv.p(full[0]), B = Mv.p(full[1]), es = 26, w = chipW(eq, es);
    const cands = [0.12, 0.88, 0.2, 0.8, 0.3, 0.7].flatMap((u) => [besideLine(A, B, w, es * 1.5, u, -1), besideLine(A, B, w, es * 1.5, u, 1)]);
    return pickSpot(cands, w, es * 1.5, avoid, [V.XL, V.YT, V.XR, V.YB]);
  };
  // 선수 이름
  const kin = seg(t, SC.in[0], SC.in[1]);
  const ns = mini ? 24 : 20;
  const actorLbl = <UText x={fit(a[0], uWidth(sc.pl, ns, 800))} y={clamp(a[1] + (la.y < a[1] ? ns * 1.7 : -ns * 1.1), V.YT + 6, V.YB + 10)} s={sc.pl} size={ns} weight={800} anchor="middle" fill="#fff" halo="#0c1a14" opacity={kin * oOut} C={C} />;
  const rec = sc.k === "p" && /→ (.+)$/.exec(sc.rs);
  const recLbl = rec ? <UText x={fit(b[0], uWidth(rec[1], ns - 2, 700))} y={clamp(b[1] + (lb.y < b[1] ? ns * 1.7 : -ns), V.YT + 6, V.YB + 10)} s={rec[1]} size={ns - 2} weight={700} anchor="middle" fill="#fff" halo="#0c1a14" opacity={kbb * oOut} C={C} /> : null;
  // 골 반짝
  const flash = scored ? seg(t, SC.ball[1], SC.ball[1] + 500) * (1 - seg(t, SC.ball[1] + 2600, SC.ball[1] + 3400)) : 0;
  const gp = mini ? [clamp(b[0] + (sc.b[0] > 0 ? -90 : 90), V.XL + 90, V.XR - 90), clamp(b[1] - 90, V.YT + 60, V.YB - 60)] : Mv.p([sc.b[0] > 0 ? 50 : -50, 30]);
  const rr = mini ? clamp(Mv.s * 0.95, 9, 15) : 8.5;
  // ── 기울기 · y절편 강조(금테 큰 칩): 피할 것 = 두 점 · 좌표 칩 · 선수 이름 · 기울기 삼각형 칩 ──
  const box = [V.XL, V.YT, V.XR, V.YB];
  const avoid = [{ x: a[0], y: a[1], w: rr * 4, h: rr * 4 }, { x: b[0], y: b[1], w: 16, h: 16 },
    chipRect(la.x, la.y, pt(A0), cs, la.anchor), chipRect(lb.x, lb.y, pt(B0), cs, lb.anchor),
    { x: a[0], y: clamp(a[1] + (la.y < a[1] ? ns * 1.7 : -ns * 1.1), V.YT + 6, V.YB + 10) - ns * 0.35, w: uWidth(sc.pl, ns, 800), h: ns * 1.2 }];
  if (dxs && dys) {
    avoid.push(chipRect(fit((a[0] + b[0]) / 2, chipW(sx, ts)), clamp(a[1] + (dys > 0 ? 1 : -1) * ts * 1.35, V.YT, V.YB), sx, ts));
    avoid.push(chipRect(fit(b[0] + (dxs > 0 ? 1 : -1) * (chipW(sy, ts) / 2 + 12), chipW(sy, ts)), clamp((a[1] + b[1]) / 2, V.YT, V.YB), sy, ts));
  }
  const tc = C.name === "light" ? "#0f766e" : "#7fe3d3";
  // 기울기(가장 먼저 자리를 잡는다): 직선 옆(삼각형 바깥) 여러 자리 가운데
  const bs = mini ? 40 : 34;
  const slopeTxt = isM ? (L.kind === "f" ? `기울기 ${fs(L.m[0], L.m[1])}` : L.kind === "h" ? "기울기 0" : "") : dxs && dys ? `세로 ÷ 가로 = ${fs(Math.abs(dys), Math.abs(dxs))}` : "";
  const sw0 = slopeTxt ? bigW(slopeTxt, bs) : 0;
  const slopeAt = slopeTxt ? pickSpot([0.5, 0.36, 0.64, 0.24, 0.76].map((f) => besideLine(a, b, sw0, bs * 1.5, f, 1)).concat([0.5, 0.3, 0.7].map((f) => besideLine(a, b, sw0, bs * 1.5, f, -1))), sw0, bs * 1.5, avoid, box) : null;
  if (slopeAt) avoid.push({ x: slopeAt[0], y: slopeAt[1], w: sw0, h: bs * 1.5 });
  // y절편(중등): 직선이 y축(하프라인)과 만나는 점 — 자리가 좁으면 작게
  let icpt = null;
  const yb = isM && (L.kind === "f" || L.kind === "h") ? L.b[0] / L.b[1] : null;
  if (yb != null && Math.abs(yb) <= 40) {
    const q = Mv.p([0, yb]);
    if (q[0] > V.XL + 20 && q[0] < V.XR - 20 && q[1] > V.YT - 10 && q[1] < V.YB + 10) {
      const txt = `y절편 ${fs(L.b[0], L.b[1])}`;
      let is = mini ? 30 : 26, w = bigW(txt, is), h = is * 1.5;
      const cands = (w2, h2) => [-1, 1].flatMap((sx) => [1, -1, 2, -2].map((k) => [q[0] + sx * (w2 / 2 + 16), q[1] + k * h2 * 0.75]));
      const room = (spot, w2, h2) => Math.min(...avoid.map((r) => Math.hypot(Math.max(0, Math.abs(r.x - spot[0]) - (r.w + w2) / 2), Math.max(0, Math.abs(r.y - spot[1]) - (r.h + h2) / 2))));
      let at2 = pickSpot(cands(w, h), w, h, avoid, box);
      if (room(at2, w, h) < 4) { is = mini ? 22 : 19; w = bigW(txt, is); h = is * 1.5; at2 = pickSpot(cands(w, h), w, h, avoid, box); }
      icpt = { q, txt, is, at: at2, w, h };
      avoid.push({ x: at2[0], y: at2[1], w, h }, { x: q[0], y: q[1], w: 14, h: 14 });
    }
  }
  const icptEl = icpt ? (
    <g opacity={seg(t, SC.line[1] - 200, SC.line[1] + 400) * oOut}>
      <circle cx={icpt.q[0]} cy={icpt.q[1]} r={mini ? 9 : 7.5} fill={tc} stroke="#fff" strokeWidth={2.4} />
      <BigChip x={icpt.at[0]} y={icpt.at[1]} s={icpt.txt} size={icpt.is} C={C} color={tc} edge={tc} />
    </g>
  ) : null;
  const body = (
    <g>
      {mini && <rect x={MBOX[0]} y={MBOX[1]} width={MBOX[2] - MBOX[0]} height={MBOX[3] - MBOX[1]} fill={C.name === "light" ? "#bcd3a3" : "#14291f"} />}
      <Pitch C={C} M={Mv} />
      {sc.va && <path d={"M" + sc.va.map((q) => Mv.p(q).map((v) => v.toFixed(1)).join(" ")).join("L") + "Z"} fill="#fff" opacity={0.05 * kin * oOut} />}
      <Axes C={C} mode={mode} o={1} V={V} />
      {ghosts}
      {lineEl}
      <Players sc={sc} teams={teams} o={oOut} k={kin} M={Mv} r0={rr} />
      {/* 공을 가진 선수 */}
      <g opacity={kin * oOut}>
        <circle cx={a[0]} cy={a[1]} r={rr * 2} fill="none" stroke={C.gold} strokeWidth={3} opacity={0.9} />
        <circle cx={a[0]} cy={a[1]} r={rr * 1.3} fill={mine} stroke={ink(mine)} strokeWidth={2.4} />
      </g>
      {actorLbl}
      {/* 지나간 길 */}
      {kb > 0 && <Path pts={[a, bp]} stroke={C.gold} sw={mini ? 5 : 4} o={0.95 * oOut} />}
      {triEl}
      <g opacity={ka * oOut}><circle cx={a[0]} cy={a[1]} r={mini ? 6.5 : 5} fill={C.gold} /><Chip x={la.x} y={la.y} s={pt(A0)} size={cs} C={C} anchor={la.anchor} /></g>
      <g opacity={kbb * oOut}><circle cx={b[0]} cy={b[1]} r={mini ? 7.5 : 6} fill={C.gold} stroke="#fff" strokeWidth={2} /><Chip x={lb.x} y={lb.y} s={pt(B0)} size={cs} C={C} anchor={lb.anchor} /></g>
      {recLbl}
      {(() => { const q = eqSpot(avoid); return q ? <Chip x={q[0]} y={q[1]} s={eq} size={26} C={C} o={seg(t, SC.line[1] - 300, SC.line[1] + 300) * oOut} /> : null; })()}
      {icptEl}
      {slopeAt && <BigChip x={slopeAt[0]} y={slopeAt[1]} s={slopeTxt} size={bs} C={C} o={kt * oOut} />}
      {kb > 0 && oOut > 0.01 && <Ball x={bp[0]} y={bp[1]} r={mini ? rr * 0.85 : 7} h={lofty * 4 * kb * (1 - kb)} C={C} o={oOut} />}
      {flash > 0 && <GoalFlash x={gp[0]} y={gp[1]} k={flash} C={C} />}
    </g>
  );
  if (!mini) {
    return (
      <g>
        {body}
        <SoccerPanel C={C} mode={mode} sc={sc} match={match} lines={lines} t={t} scored={scored} idx={i} n={list.length} oOut={oOut} />
      </g>
    );
  }
  const [bx0, by0, bx1, by1] = MBOX;
  return (
    <g>
      <defs><clipPath id="soccer-mini-clip"><rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} /></clipPath></defs>
      <g clipPath="url(#soccer-mini-clip)">{body}</g>
      <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} fill="none" stroke={C.cardEdge} strokeWidth={1.4} />
      <SoccerMini C={C} mode={mode} sc={sc} match={match} lines={lines} t={t} scored={scored} oOut={oOut} />
    </g>
  );
}

/** 최소화 — 위 왼쪽: 경기 · 시계 · 점수, 위 오른쪽: 누가 무엇을 → 결과, 아래: 식(중등) 또는 가파른 정도(초등) 한 줄 */
function SoccerMini({ C, mode, sc, match, lines, t, scored, oOut }) {
  const [bx0, by0, bx1, by1] = MBOX;
  const teams = match.teams, score = scored && sc.sa ? sc.sa : sc.sc;
  const per = sc.p === 5 ? "승부차기" : `${PERIOD[sc.p]} ${clock(sc.m, sc.s)}`;
  const a = `${match.title} · ${per} · ${teams[0].n} ${score[0]} : ${score[1]} ${teams[1].n}`;
  const done = t >= SC.ball[1];
  const bTxt = `${sc.pl} — ${sc.ty}${done ? ` → ${sc.rs}` : ""}`;
  const hi = [...lines].reverse().find((L) => L.hi);
  const kin = seg(t, 0, 500) * oOut;
  return (
    <g>
      <Chip x={bx0 + 16} y={by0 + 32} s={a} size={21} C={C} anchor="start" o={kin} />
      <Chip x={bx1 - 16} y={by0 + 32} s={bTxt} size={21} C={C} anchor="end" color={sc.g && done ? C.gold : undefined} o={kin} />
      {hi && <Chip x={bx0 + 16} y={by0 + 80} s={hi.s} size={26} C={C} color={C.gold} anchor="start" o={seg(t, SC.line[1], SC.line[1] + 500) * oOut} />}
    </g>
  );
}

/** 오른쪽 설명 판 */
function SoccerPanel({ C, mode, sc, match, lines, t, scored, idx, n, oOut }) {
  const { x, y, w, h } = PANEL;
  const teams = match.teams;
  const score = scored && sc.sa ? sc.sa : sc.sc;
  const x0 = x + 22, mw = w - 44;
  const kin = seg(t, 0, 500);
  const per = PERIOD[sc.p];
  // 승부차기 점수: 공이 닿기 전에는 이번 차기 앞의 점수
  let pens = "";
  if (sc.p === 5 && sc.pe) {
    const pe = sc.pe.slice();
    if (sc.g && t < SC.ball[1]) pe[sc.t] -= 1;
    pens = `${pe[0]} : ${pe[1]}`;
  }
  const shown = lines.map((L, j) => ({ ...L, at: STEP_AT[Math.min(j, STEP_AT.length - 1)] + (j >= STEP_AT.length ? (j - STEP_AT.length + 1) * 700 : 0) }));
  const rsCol = sc.g ? C.gold : /실패|밖|막힘|빗나감/.test(sc.rs) ? C.soft : C.teal;
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <Small x={x0} y={y + 36} s={`2022 FIFA 월드컵 · ${match.title} · ${match.date}`} size={16} C={C} />
      {/* 점수 */}
      <g>
        <circle cx={x0 + 8} cy={y + 76} r={8} fill={teams[0].c} stroke={ink(teams[0].c)} strokeWidth={1.6} />
        <UText x={x0 + 24} y={y + 85} s={`${teams[0].n}  ${score[0]} : ${score[1]}  ${teams[1].n}`} size={26} weight={800} C={C} />
        <circle cx={x0 + 44 + uWidth(`${teams[0].n}  ${score[0]} : ${score[1]}  ${teams[1].n}`, 26, 800)} cy={y + 76} r={8} fill={teams[1].c} stroke={ink(teams[1].c)} strokeWidth={1.6} />
      </g>
      <UText x={x0} y={y + 122} s={sc.p === 5 ? `승부차기 ${pens}` : `${per} ${clock(sc.m, sc.s)}`} size={22} weight={700} fill={mode === "m" ? C.teal : C.coral} C={C} />
      {/* 누가 · 무엇을 */}
      <g opacity={kin * oOut}>
        <circle cx={x0 + 9} cy={y + 162} r={9} fill={teams[sc.t].c} stroke={ink(teams[sc.t].c)} strokeWidth={1.6} />
        <FitText x={x0 + 26} y={y + 171} s={`${sc.pl}`} size={26} maxW={mw - 26} weight={800} fill={C.ink} C={C} />
        <UText x={x0} y={y + 204} s={sc.ty} size={20} weight={650} fill={C.soft} C={C} />
        <g opacity={seg(t, SC.ball[1], SC.ball[1] + 400)}>
          <FitText x={x0} y={y + 238} s={sc.rs} size={22} maxW={mw} weight={800} fill={rsCol} C={C} />
          {sc.xg != null && <Small x={x0} y={y + 266} s={mode === "m" ? `xG ${sc.xg.toFixed(2)} — 이런 기회 100번이면 약 ${Math.round(sc.xg * 100)}골` : `이런 기회 100번이면 약 ${Math.round(sc.xg * 100)}번 골`} size={16} C={C} />}
        </g>
      </g>
      <line x1={x0} x2={x + w - 22} y1={y + 290} y2={y + 290} stroke={C.cardEdge} strokeWidth={1.2} />
      <Lines x={x0} y={y + 332} lines={shown} t={t} C={C} size={24} lh={50} maxW={mw} o={oOut} hiSize={32} />
      <Small x={x0} y={y + h - 20} s={`장면 ${idx + 1} / ${n}`} size={15} C={C} />
      <Small x={x + w - 22} y={y + h - 20} s="데이터: StatsBomb 오픈 데이터" size={14} C={C} anchor="end" />
    </g>
  );
}

/* ══════════ 액자 ══════════ */
let CACHE = null;
function useSoccerData() {
  const [d, setD] = useState(CACHE);
  useEffect(() => {
    if (CACHE) return;
    let live = true;
    import("../curio/data-soccer.js").then((m) => { CACHE = m.default; if (live) setD(m.default); }).catch(() => {});
    return () => { live = false; };
  }, []);
  return d;
}

export function SoccerFnFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, DEF, fixPrm);
  const P = lab.prm;
  const data = useSoccerData();
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const list = data ? scenesOf(data, P) : [];
  const e = lab.elapsed() * P.sp;
  const at = cycleAt(e, SC.D, list.length || 1);
  const jumpScene = (d) => { const k = Math.max(0, at.k + d); lab.jump((k * SC.D) / P.sp); poke(); };
  const stepIn = (key, opts, d) => { const i = opts.indexOf(P[key]); const j = clamp(i + d, 0, opts.length - 1); if (j !== i) lab.setPrm({ [key]: opts[j] }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: lab.restart, toggleFs, onMode, poke }),
    ArrowRight: () => jumpScene(1), ArrowLeft: () => jumpScene(-1),
    ArrowUp: () => stepIn("match", MATCHES, 1), ArrowDown: () => stepIn("match", MATCHES, -1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="경기"><Stepper ui={ui} label="경기" value={P.match} options={MATCHES} fmt={(v) => (v < 0 ? "전체" : MATCH_SHORT[v])} onChange={(v) => lab.setPrm({ match: v })} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="장면" sep><Seg label="장면" value={P.kind} options={[["all", "모두"], ["s", "슈팅"], ["p", "패스"]]} onChange={(v) => lab.setPrm({ kind: v })} poke={poke} /></Setting>
      <Setting label="풀이" sep><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
      <span className="dsp-sep" />
      <ui.Btn title="이전 장면 (←)" onClick={() => jumpScene(-1)}><ui.Ic d="M15 5 8 12l7 7" /></ui.Btn>
      <ui.Btn title="다음 장면 (→)" onClick={() => jumpScene(1)}><ui.Ic d="m9 5 7 7-7 7" /></ui.Btn>
    </>
  );
  const title = { e: "축구로 보는 좌표와 직선", m: "축구로 보는 일차함수" };
  const sub = data && list.length ? (() => { const m = data.matches[list[at.i].mi]; return `${m.teams[0].n} ${m.final[0]} : ${m.final[1]} ${m.teams[1].n}${m.pens ? ` (승부차기 ${m.pens[0]} : ${m.pens[1]})` : ""} · 슈팅 · 패스가 지나간 두 점`; })() : "2022 FIFA 월드컵";
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="축구 경기 장면으로 보는 일차함수">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <SoccerArt C={C} mode={Ly.mode} P={P} data={data} at={at} ex={P.ex} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={lab.restart}
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings}
        prog={list.length ? (at.i + at.t / SC.D) / list.length : 0} />
    </>
  );
}

/* 목록 그림 — 2022 월드컵 대한민국–포르투갈, 후반 90분 황희찬 결승골 */
const THUMB = {
  matches: [{ title: "조별리그 H조 3차전", date: "2022. 12. 2.", final: [2, 1], pens: null, teams: [{ n: "대한민국", c: "#e53935" }, { n: "포르투갈", c: "#f4f4f4" }],
    scenes: [{ k: "s", p: 2, m: 90, s: 28, t: 0, pl: "황희찬", a: [48, -5], b: [60, 1], sc: [1, 1], sa: [2, 1], g: 1, ty: "오른발 슈팅", rs: "골!", xg: 0.42,
      ff: [[31.9, -18.3, 1, 0, 0], [37.3, -9.4, 1, 0, 0], [37.4, 0.3, 0, 0, 0], [37.4, -11.9, 1, 0, 0], [38.5, -8, 0, 0, 0], [38.6, -10.1, 0, 0, 0], [40.4, -9.8, 0, 0, 0],
        [42.2, -11.3, 0, 0, 0], [42.2, -4.8, 0, 0, 0], [42.2, -7.1, 0, 0, 0], [47.3, -2.7, 0, 0, 0], [48.3, -4.6, 1, 0, 1], [53.9, -1, 0, 1, 0]] }] }],
};
export const SoccerFnThumb = memo(function SoccerFnThumb({ C, mode = "m" }) {
  return <SoccerArt C={C} mode={mode} P={{ match: -1, kind: "all", sp: 1 }} data={THUMB} at={{ i: 0, k: 0, t: 5200 }} />;
});
