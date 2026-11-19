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
import { lineOf, lineSteps, runRiseSteps, pt, num, eqText, cycleAt, SPEEDS, spFmt, keepSpeed } from "../curio/kit.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { FitText, Lines, Panel, Small, clipLine } from "./curio-kit.jsx";

const LSK = "ash.display.curio.soccerfn";
const MATCH_SHORT = ["우루과이전", "가나전", "포르투갈전", "브라질전", "네덜·아르", "결승"];
const MATCHES = [-1, 0, 1, 2, 3, 4, 5];
const DEF = { match: -1, kind: "all", sp: 1 };
const fixPrm = (p = {}) => ({
  match: MATCHES.includes(p.match) ? p.match : -1,
  kind: ["all", "s", "p"].includes(p.kind) ? p.kind : "all",
  sp: SPEEDS.includes(p.sp) ? p.sp : 1,
});

/* ── 무대 자리: 경기장(왼쪽) · 설명 판(오른쪽) ── */
const S = 9, PX0 = 52, PY0 = 150;                  // 1야드 = 9px, 경기장 1080 × 720
const M = mapper({ ox: PX0 + 60 * S, oy: PY0 + 40 * S, s: S, flipY: true });
/** 이름표가 경기장 밖(오른쪽 판 · 아래 눈금)으로 나가지 않게 */
const XL = PX0 + 6, XR = PX0 + 120 * S - 6, YT = PY0 + 16, YB = PY0 + 80 * S - 16;
const fitC = (x, w) => clamp(x, XL + w / 2, XR - w / 2);
/** 좌표 이름표 자리: 상대 점의 반대쪽 옆 · 위아래, 경기장 밖으로 나가면 뒤집는다 */
function ptSpot(q, other, s, first) {
  const w = chipW(s, 19);
  let side = q[0] < other[0] ? -1 : q[0] > other[0] ? 1 : first ? -1 : 1;
  if (side > 0 && q[0] + 12 + w > XR) side = -1;
  else if (side < 0 && q[0] - 12 - w < XL) side = 1;
  let y = q[1] + (q[1] <= other[1] ? -26 : 30);
  if (y < YT) y = q[1] + 30;
  else if (y > YB) y = q[1] - 26;
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

const Pitch = memo(function Pitch({ C }) {
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
function Axes({ C, mode, o }) {
  if (o <= 0.001) return null;
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

/** 무한 직선을 경기장 안 선분으로 */
function pitchSeg(L, a) {
  if (L.kind === "pt") return null;
  const d = L.kind === "v" ? [0, 1] : [L.m[1], L.m[0]];
  return clipLine(a, d, RECT);
}

/* ══════════ 장면 ══════════ */
const lum = (hex) => { const n = parseInt(hex.slice(1), 16); return (0.299 * ((n >> 16) & 255) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255; };
const ink = (hex) => (lum(hex) < 0.4 ? "#e9edf6" : "#14171f");
function Players({ sc, teams, o, k }) {
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
            <ellipse cx={q[0] + 2} cy={q[1] + 8} rx={8} ry={3} fill="#000" opacity={0.25} />
            <circle cx={q[0]} cy={q[1]} r={gk ? 9.5 : 8.5} fill={col} stroke={ink(col)} strokeWidth={2} />
            {gk ? <circle cx={q[0]} cy={q[1]} r={13} fill="none" stroke={col} strokeWidth={2} opacity={0.8} /> : null}
          </g>
        );
      })}
    </g>
  );
}

export function SoccerArt({ C, mode, P, data, at }) {
  if (!data) return <MText x={600} y={480} s="경기 자료를 불러오는 중…" size={34} anchor="middle" fill={C.soft} C={C} />;
  const list = scenesOf(data, P);
  if (!list.length) return null;
  const { i, t } = at;
  const { mi, sc } = list[i];
  const match = data.matches[mi], teams = match.teams;
  const isM = mode === "m";
  const oOut = 1 - seg(t, SC.out[0], SC.out[1]);
  const a = M.p(sc.a), b = M.p(sc.b);
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
    ghosts.push(<Path key={g} pts={[M.p(sg[0]), M.p(sg[1])]} stroke={col} sw={2.4} o={(0.34 - g * 0.055) * (g === 1 ? 1 - 0.6 * seg(t, 0, 2000) : 1)} />);
  }
  // 이번 직선(그래프)
  const full = pitchSeg(L, sc.a);
  const kl = seg(t, SC.line[0], SC.line[1], E.out);
  let lineEl = null;
  if (full && kl > 0) {
    const A = M.p(full[0]), B = M.p(full[1]);
    const mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    const ext = (q) => [lerp(mid[0], q[0], kl), lerp(mid[1], q[1], kl)];
    lineEl = <Path pts={[ext(A), ext(B)]} stroke={C.name === "light" ? "#0f766e" : "#7fe3d3"} sw={3.2} dash="12 9" o={0.95 * oOut} />;
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
      <Chip x={fitC((a[0] + b[0]) / 2, chipW(sx, 18))} y={clamp(a[1] + (dys > 0 ? 24 : -24), YT, YB)} s={sx} size={18} C={C} />
      <Chip x={fitC(b[0] + (dxs > 0 ? 44 : -44), chipW(sy, 18))} y={clamp((a[1] + b[1]) / 2, YT, YB)} s={sy} size={18} C={C} />
    </g>
  ) : null;
  // 점 · 좌표 이름표
  const A0 = isM ? sc.a : corner(sc.a), B0 = isM ? sc.b : corner(sc.b);
  const ka = seg(t, SC.a[0], SC.a[1]), kbb = seg(t, SC.b[0], SC.b[1]);
  const la = ptSpot(a, b, pt(A0), true), lb = ptSpot(b, a, pt(B0), false);
  // 식 이름표(중등): 직선 위, 도착점에서 조금 떨어진 곳
  const eq = eqText(L);
  let eqEl = null;
  if (isM && full && eq) {
    const ke = seg(t, SC.line[1] - 300, SC.line[1] + 300);
    const A = M.p(full[0]), B = M.p(full[1]);
    const u = 0.22, q = [lerp(A[0], B[0], u), lerp(A[1], B[1], u)];
    const qq = [fitC(q[0], chipW(eq, 22)), clamp(q[1] + 30, PY0 + 30, PY0 + 700)];
    eqEl = <Chip x={qq[0]} y={qq[1]} s={eq} size={22} C={C} o={ke * oOut} />;
  }
  // 선수 이름
  const kin = seg(t, SC.in[0], SC.in[1]);
  const actorLbl = <UText x={fitC(a[0], uWidth(sc.pl, 20, 800))} y={clamp(a[1] + (la.y < a[1] ? 34 : -22), YT + 6, YB + 10)} s={sc.pl} size={20} weight={800} anchor="middle" fill="#fff" halo="#0c1a14" opacity={kin * oOut} C={C} />;
  const rec = sc.k === "p" && /→ (.+)$/.exec(sc.rs);
  const recLbl = rec ? <UText x={fitC(b[0], uWidth(rec[1], 18, 700))} y={clamp(b[1] + (lb.y < b[1] ? 34 : -20), YT + 6, YB + 10)} s={rec[1]} size={18} weight={700} anchor="middle" fill="#fff" halo="#0c1a14" opacity={kbb * oOut} C={C} /> : null;
  // 골 반짝
  const flash = scored ? seg(t, SC.ball[1], SC.ball[1] + 500) * (1 - seg(t, SC.ball[1] + 2600, SC.ball[1] + 3400)) : 0;
  const gp = M.p([sc.b[0] > 0 ? 50 : -50, 30]);
  return (
    <g>
      <Pitch C={C} />
      {sc.va && <path d={"M" + sc.va.map((q) => M.p(q).map((v) => v.toFixed(1)).join(" ")).join("L") + "Z"} fill="#fff" opacity={0.05 * kin * oOut} />}
      <Axes C={C} mode={mode} o={1} />
      {ghosts}
      {lineEl}
      <Players sc={sc} teams={teams} o={oOut} k={kin} />
      {/* 공을 가진 선수 */}
      <g opacity={kin * oOut}>
        <circle cx={a[0]} cy={a[1]} r={17} fill="none" stroke={C.gold} strokeWidth={3} opacity={0.9} />
        <circle cx={a[0]} cy={a[1]} r={11} fill={mine} stroke={ink(mine)} strokeWidth={2.4} />
      </g>
      {actorLbl}
      {/* 지나간 길 */}
      {kb > 0 && <Path pts={[a, bp]} stroke={C.gold} sw={4} o={0.95 * oOut} />}
      {triEl}
      <g opacity={ka * oOut}><circle cx={a[0]} cy={a[1]} r={5} fill={C.gold} /><Chip x={la.x} y={la.y} s={pt(A0)} size={19} C={C} anchor={la.anchor} /></g>
      <g opacity={kbb * oOut}><circle cx={b[0]} cy={b[1]} r={6} fill={C.gold} stroke="#fff" strokeWidth={2} /><Chip x={lb.x} y={lb.y} s={pt(B0)} size={19} C={C} anchor={lb.anchor} /></g>
      {recLbl}
      {eqEl}
      {kb > 0 && oOut > 0.01 && <Ball x={bp[0]} y={bp[1]} r={7} h={lofty * 4 * kb * (1 - kb)} C={C} o={oOut} />}
      {flash > 0 && <GoalFlash x={gp[0]} y={gp[1]} k={flash} C={C} />}
      <SoccerPanel C={C} mode={mode} sc={sc} match={match} lines={lines} t={t} scored={scored} idx={i} n={list.length} oOut={oOut} />
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
  }, inert);
  const settings = (
    <>
      <Setting label="경기"><Stepper ui={ui} label="경기" value={P.match} options={MATCHES} fmt={(v) => (v < 0 ? "전체" : MATCH_SHORT[v])} onChange={(v) => lab.setPrm({ match: v })} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="장면" sep><Seg label="장면" value={P.kind} options={[["all", "모두"], ["s", "슈팅"], ["p", "패스"]]} onChange={(v) => lab.setPrm({ kind: v })} poke={poke} /></Setting>
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
            <SoccerArt C={C} mode={Ly.mode} P={P} data={data} at={at} />
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
