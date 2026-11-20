// ashrain.out — 수학 호기심 액자: 네트를 사이에 둔 구기 (frames/netfn.jsx)
// 배드민턴(실제 경기 — ShuttleSet) · 테니스 · 탁구 · 배구 · 족구 · 세팍타크로(가상 경기)를 위에서 내려다본다.
//   랠리가 흘러가며 친 공마다 두 점(친 곳 → 떨어진 곳)을 잇는 선이 쌓이고, 점수가 끝나면 결정구를 다시 본다:
//   두 점 → 기울기 삼각형 → 직선 → 네트(x = 0, 곧 y축)를 지난 자리 = y절편.
//   중등: 네트 가운데가 원점 · 초등: 판의 왼쪽 아래가 원점(가로 · 세로 칸, 네트까지 비례).
// 풀이 상세: 오른쪽 설명 판(점수판 · 랠리 흐름 · 판서) · 최소화: 설명 판 없이 코트를 크게(점수 막대 · 식 칩만).
// 계산: ../curio/net.js · 배드민턴 자료: ../curio/data-badminton.js(늦게 들여온다)
import { memo, useEffect, useState } from "react";
import { W, H, MText, SceneTitle, Path, SANS, textW } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, Chip, chipW, uWidth } from "../kit-story.jsx";
import { lineOf, eqText, pt, fs, SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx } from "../curio/kit.js";
import { NETS, NT, RP, genMatch, badmintonMatches, scheduleOf, rallyAt, netSteps, shotLog, scoreRows, crosses, netY, ruleText } from "../curio/net.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { FitText, Lines, Panel, Small, clipLine, BigChip, bigW, besideLine, pickSpot, chipRect } from "./curio-kit.jsx";

/* ══════════ 무대 자리 ══════════ */
const AREA = { full: [40, 150, 1140, 870], mini: [36, 150, 1564, 872] };
const PANEL = { x: 1162, y: 150, w: 400, h: 720 };
const CAMS = new Map();
/** 종목 · 풀이 보기별 카메라: 세계(칸) → 무대 px */
export function netCam(sport, ex) {
  const key = sport + ex;
  if (CAMS.has(key)) return CAMS.get(key);
  const S = NETS[sport], v = ex === "mini" ? S.miniView : S.view, A = AREA[ex];
  const s = Math.min((A[2] - A[0]) / (2 * v[0]), (A[3] - A[1]) / (2 * v[1]));
  const cx = (A[0] + A[2]) / 2, cy = (A[1] + A[3]) / 2;
  const cam = { s, v, cx, cy, p: (q) => [cx + q[0] * s, cy - q[1] * s], box: [cx - v[0] * s, cy - v[1] * s, cx + v[0] * s, cy + v[1] * s] };
  CAMS.set(key, cam);
  return cam;
}

/* ══════════ 코트 ══════════ */
const PAL = {
  badminton: { dark: ["#1b2a3f", "#1f5e4d", "#e8f1ea"], light: ["#cdb388", "#3b8f73", "#ffffff"] },
  tennis: { dark: ["#22503c", "#244b72", "#e8eef6"], light: ["#5f9c76", "#3b6ea3", "#ffffff"] },
  tabletennis: { dark: ["#38202f", "#1b4278", "#f2f4f8"], light: ["#b9735e", "#2a5ea8", "#ffffff"] },
  volleyball: { dark: ["#1f3f66", "#a8612a", "#f4f1ea"], light: ["#3a71b0", "#df8f48", "#ffffff"] },
  jokgu: { dark: ["#23332a", "#2e5e39", "#eef3ea"], light: ["#9fb48a", "#4f8f58", "#ffffff"] },
  sepak: { dark: ["#21453a", "#274f86", "#eef2f8"], light: ["#5f9c7c", "#3d6fb8", "#ffffff"] },
};
const rectL = (x0, y0, x1, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]];
/** 종목별 코트 바닥(안쪽 사각형) · 선(세계 꺾은선) · 원 · 네트 반 길이 */
const GEO = {
  badminton: (() => {
    const L = 13.4, Wd = 6.1, Ws = 5.18, sv = 3.96, lv = 11.88;
    return { inner: [-L, -Wd, L, Wd], net: 6.7, circles: [],
      lines: [rectL(-L, -Wd, L, Wd), [[-L, Ws], [L, Ws]], [[-L, -Ws], [L, -Ws]], [[-sv, -Wd], [-sv, Wd]], [[sv, -Wd], [sv, Wd]],
        [[-lv, -Wd], [-lv, Wd]], [[lv, -Wd], [lv, Wd]], [[-L, 0], [-sv, 0]], [[sv, 0], [L, 0]]] };
  })(),
  tennis: (() => {
    const L = 11.885, Wd = 5.485, Ws = 4.115, sv = 6.4;
    return { inner: [-L, -Wd, L, Wd], net: 6.4, circles: [],
      lines: [rectL(-L, -Wd, L, Wd), [[-L, Ws], [L, Ws]], [[-L, -Ws], [L, -Ws]], [[-sv, -Ws], [-sv, Ws]], [[sv, -Ws], [sv, Ws]],
        [[-sv, 0], [sv, 0]], [[-L, 0], [-L + 0.3, 0]], [[L - 0.3, 0], [L, 0]]] };
  })(),
  tabletennis: (() => {
    const L = 13.7, Wd = 7.625;
    return { inner: [-L, -Wd, L, Wd], net: 9.15, circles: [], table: true,
      lines: [rectL(-L, -Wd, L, Wd), [[-L, 0], [L, 0]]] };
  })(),
  volleyball: (() => {
    const L = 9, Wd = 4.5;
    return { inner: [-L, -Wd, L, Wd], net: 5, circles: [], antenna: 4.5,
      lines: [rectL(-L, -Wd, L, Wd), [[-3, -Wd], [-3, Wd]], [[3, -Wd], [3, Wd]]] };
  })(),
  jokgu: (() => {
    const L = 15, Wd = 6.5;
    return { inner: [-L, -Wd, L, Wd], net: 7.2, circles: [], antenna: 6.9,
      lines: [rectL(-L, -Wd, L, Wd), [[-L - 6, -Wd], [-L, -Wd]], [[-L - 6, Wd], [-L, Wd]], [[L, -Wd], [L + 6, -Wd]], [[L, Wd], [L + 6, Wd]]] };
  })(),
  sepak: (() => {
    const L = 13.4, Wd = 6.1;
    return { inner: [-L, -Wd, L, Wd], net: 6.7, circles: [[-8.5, 0, 0.6], [8.5, 0, 0.6]], quarter: 1.8,
      lines: [rectL(-L, -Wd, L, Wd)] };
  })(),
};

const Court = memo(function Court({ sport, ex, C }) {
  const cam = netCam(sport, ex), G = GEO[sport];
  const [floor, inner, line] = PAL[sport][C.name === "light" ? "light" : "dark"];
  const [bx0, by0, bx1, by1] = cam.box;
  const a = cam.p([G.inner[0], G.inner[3]]), b = cam.p([G.inner[2], G.inner[1]]);
  const lw = Math.max(2, cam.s * (sport === "tabletennis" ? 0.2 : sport === "tennis" ? 0.06 : 0.1));
  const id = `net-clip-${sport}-${ex}`;
  const nt = cam.p([0, G.net]), nb = cam.p([0, -G.net]);
  return (
    <g>
      <defs><clipPath id={id}><rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} /></clipPath></defs>
      <g clipPath={`url(#${id})`}>
        <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} fill={floor} />
        {G.table && <rect x={a[0] + 6} y={a[1] + 10} width={b[0] - a[0]} height={b[1] - a[1]} fill="#000" opacity={0.28} rx={4} />}
        <rect x={a[0]} y={a[1]} width={b[0] - a[0]} height={b[1] - a[1]} fill={inner} rx={G.table ? 4 : 0} />
        {G.lines.map((pts, i) => <path key={i} d={"M" + pts.map((q) => cam.p(q).map((v) => v.toFixed(1)).join(" ")).join("L")} fill="none" stroke={line} strokeWidth={lw} strokeLinejoin="round" opacity={0.92} />)}
        {G.circles.map(([x, y, r], i) => { const q = cam.p([x, y]); return <circle key={i} cx={q[0]} cy={q[1]} r={r * cam.s} fill="none" stroke={line} strokeWidth={lw} opacity={0.9} />; })}
        {G.quarter && [[1, 1], [1, -1], [-1, 1], [-1, -1]].map(([sx, sy], i) => {
          const c = cam.p([0, sy * 6.1]), r = G.quarter * cam.s;
          return <path key={i} d={`M${c[0] + sx * r} ${c[1]}A${r} ${r} 0 0 ${sx * sy > 0 ? 0 : 1} ${c[0]} ${c[1] + sy * r}`} fill="none" stroke={line} strokeWidth={lw} opacity={0.9} />;
        })}
        {/* 네트(= y축 자리) */}
        <line x1={nt[0] + 3} x2={nb[0] + 3} y1={nt[1]} y2={nb[1]} stroke="#000" strokeWidth={5} opacity={0.25} />
        <line x1={nt[0]} x2={nb[0]} y1={nt[1]} y2={nb[1]} stroke={C.name === "light" ? "#2b2b2b" : "#dfe6ee"} strokeWidth={4.5} opacity={0.95} strokeDasharray="2 3" />
        <line x1={nt[0]} x2={nb[0]} y1={nt[1]} y2={nb[1]} stroke="#fff" strokeWidth={1.6} opacity={0.9} />
        {[nt, nb].map((q, i) => <circle key={i} cx={q[0]} cy={q[1]} r={5} fill={C.name === "light" ? "#444" : "#cfd6de"} />)}
        {G.antenna && [1, -1].map((sy) => { const q = cam.p([0, sy * G.antenna]); return <circle key={sy} cx={q[0]} cy={q[1]} r={4.5} fill="#e53935" stroke="#fff" strokeWidth={1.5} />; })}
      </g>
      <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} fill="none" stroke={C.cardEdge} strokeWidth={1.4} />
    </g>
  );
});

/* ══════════ 좌표 ══════════ */
const tickStep = (sport) => (sport === "tabletennis" ? 5 : sport === "volleyball" || sport === "tennis" ? 2 : 2);
/** 눈금: 중등은 네트 가운데 원점(x축 · y축 = 네트), 초등은 판 왼쪽 아래 원점 — 숫자는 판 가장자리에도 */
function Axes({ sport, ex, mode, C }) {
  const cam = netCam(sport, ex), S = NETS[sport], isM = mode === "m";
  const v = cam.v, off = S.view;
  const st = tickStep(sport) * (sport === "tabletennis" && ex === "full" ? 1 : 1);
  const ink = C.name === "light" ? "#1f2a24" : "#ffffff", hal = C.name === "light" ? "#eef3ea" : "#14202b";
  const out = [];
  const [bx0, by0, bx1, by1] = cam.box;
  // 눈금은 보이는 좌표(중등: 네트 가운데가 원점 · 초등: 왼쪽 아래가 원점)의 st 배수에
  const ox = isM ? 0 : off[0], oy = isM ? 0 : off[1];
  for (let x = Math.ceil((-v[0] + ox) / st) * st - ox; x <= v[0]; x += st) {
    const q = cam.p([x, 0]);
    out.push(<line key={"gx" + x} x1={q[0]} x2={q[0]} y1={by0} y2={by1} stroke={ink} strokeOpacity={x === 0 && isM ? 0 : 0.07} strokeWidth={1} />);
    const val = x + ox;
    if ((val % (st * 2) === 0 || ex === "mini") && q[0] > bx0 + 30 && q[0] < bx1 - 14) out.push(<MText key={"lx" + x} x={q[0]} y={by1 - 8} s={String(val).replace("-", "−")} size={13} weight={700} anchor="middle" fill={ink} halo={hal} opacity={0.7} C={C} />);
  }
  for (let y = Math.ceil((-v[1] + oy) / st) * st - oy; y <= v[1]; y += st) {
    const q = cam.p([0, y]);
    out.push(<line key={"gy" + y} x1={bx0} x2={bx1} y1={q[1]} y2={q[1]} stroke={ink} strokeOpacity={y === 0 && isM ? 0 : 0.07} strokeWidth={1} />);
    const val = y + oy;
    if (q[1] < by1 - 22 && q[1] > by0 + 12) out.push(<MText key={"ly" + y} x={bx0 + 8} y={q[1] + 5} s={String(val).replace("-", "−")} size={13} weight={700} anchor="start" fill={ink} halo={hal} opacity={0.7} C={C} />);
  }
  if (isM) {
    const X0 = cam.p([-v[0], 0]), X1 = cam.p([v[0], 0]), Y0 = cam.p([0, -v[1]]), Y1 = cam.p([0, v[1]]);
    out.push(<line key="ax" x1={X0[0]} x2={X1[0] - 4} y1={X0[1]} y2={X1[1]} stroke={ink} strokeWidth={1.8} opacity={0.55} />);
    out.push(<path key="axh" d={`M${X1[0] - 2} ${X1[1]}l-11 -5.5v11z`} fill={ink} opacity={0.7} />);
    out.push(<MText key="axl" x={X1[0] - 16} y={X1[1] - 9} s="x" size={20} fill={ink} halo={hal} C={C} />);
    out.push(<MText key="ayl" x={Y1[0] + 10} y={Y1[1] + 20} s="y" size={20} fill={ink} halo={hal} C={C} />);
    out.push(<MText key="ao" x={Y0[0] + 7} y={cam.cy + 18} s="O" size={15} weight={700} fill={ink} halo={hal} opacity={0.85} C={C} />);
  } else {
    const O = cam.p([-off[0], -off[1]]);
    if (O[0] >= bx0 - 1 && O[1] <= by1 + 1) out.push(<MText key="ao" x={O[0] + 6} y={O[1] - 6} s="O" size={15} weight={700} fill={ink} halo={hal} opacity={0.85} C={C} />);
  }
  return <g>{out}</g>;
}

/* ══════════ 사람 · 공 ══════════ */
const lum = (hex) => { const n = parseInt(hex.slice(1), 16); return (0.299 * ((n >> 16) & 255) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255; };
const inkOn = (hex) => (lum(hex) < 0.55 ? "#ffffff" : "#15181f");
function Players({ sport, ex, r, teams, at, C, hitter, o }) {
  const cam = netCam(sport, ex), S = NETS[sport], n = S.team;
  const R = (n === 1 ? 15 : 13) * (ex === "mini" ? 1.15 : 1);
  return (
    <g opacity={o}>
      {at.map((q, id) => {
        const t = Math.floor(id / n), w = id % n, p = cam.p(q), col = teams[t].c;
        const hit = hitter === id;
        return (
          <g key={id}>
            <ellipse cx={p[0] + 2} cy={p[1] + R * 0.8} rx={R * 0.9} ry={R * 0.32} fill="#000" opacity={0.25} />
            {hit && <circle cx={p[0]} cy={p[1]} r={R + 6} fill="none" stroke={C.gold} strokeWidth={3} opacity={0.95} />}
            <circle cx={p[0]} cy={p[1]} r={R} fill={col} stroke={inkOn(col) === "#ffffff" ? "#ffffff" : "#1b1f27"} strokeWidth={2.2} strokeOpacity={0.85} />
            {n > 1 && <text x={p[0]} y={p[1] + 5} textAnchor="middle" fontSize={R * 0.95} fontWeight={800} fill={inkOn(col)} fontFamily="system-ui, sans-serif">{teams[t].ps[w]}</text>}
          </g>
        );
      })}
    </g>
  );
}
/** 공(셔틀콕은 깃털 꼴) — h: 높이(0~1) */
function NBall({ sport, p, h, C, o = 1, dir }) {
  if (o <= 0.001) return null;
  const lift = h * 30, k = 1 + 0.5 * h;
  const y = p[1] - lift;
  let body;
  if (sport === "badminton") {
    const a = Math.atan2(dir ? dir[1] : 0, dir ? dir[0] : 1);
    const ca = Math.cos(a), sa = Math.sin(a), s = 7 * k;
    const tip = [p[0] + ca * s, y + sa * s], l = [p[0] - ca * s * 1.4 - sa * s, y - sa * s * 1.4 + ca * s], rr = [p[0] - ca * s * 1.4 + sa * s, y - sa * s * 1.4 - ca * s];
    body = (
      <g>
        <path d={`M${tip[0]} ${tip[1]}L${l[0]} ${l[1]}L${rr[0]} ${rr[1]}Z`} fill="#fbfbf6" stroke="#333" strokeWidth={1.2} />
        <circle cx={tip[0]} cy={tip[1]} r={3.2 * k} fill="#f2f2ea" stroke="#333" strokeWidth={1} />
      </g>
    );
  } else {
    const col = { tennis: "#d7ee3c", tabletennis: "#ffffff", volleyball: "#f7f3e2", jokgu: "#fafafa", sepak: "#f2c14e" }[sport] || "#fff";
    const r = ({ tabletennis: 5.5, tennis: 7, volleyball: 9.5, jokgu: 9, sepak: 8.5 }[sport] || 8) * k;
    body = (
      <g>
        <circle cx={p[0]} cy={y} r={r} fill={col} stroke="#2b2b2b" strokeWidth={1.4} />
        {sport === "volleyball" && <path d={`M${p[0] - r} ${y}Q${p[0]} ${y - r * 0.6} ${p[0] + r} ${y}`} fill="none" stroke="#2f62a3" strokeWidth={2} />}
        {sport === "tennis" && <path d={`M${p[0] - r * 0.7} ${y - r * 0.7}Q${p[0]} ${y} ${p[0] - r * 0.7} ${y + r * 0.7}`} fill="none" stroke="#fff" strokeWidth={1.4} />}
        {sport === "sepak" && <path d={`M${p[0] - r} ${y}L${p[0] + r} ${y}M${p[0]} ${y - r}L${p[0]} ${y + r}`} stroke="#8a5a14" strokeWidth={1.4} />}
      </g>
    );
  }
  return (
    <g opacity={o}>
      <ellipse cx={p[0]} cy={p[1] + 3} rx={7 * (1 - 0.3 * h)} ry={2.6 * (1 - 0.3 * h)} fill="#000" opacity={0.3 - 0.12 * h} />
      {body}
    </g>
  );
}

/* ══════════ 한 랠리 ══════════ */
const WHO = (teams, s) => (teams[s.t].ps.length > 1 ? `${teams[s.t].n} ${teams[s.t].ps[s.w]}번` : teams[s.t].n);
const ease = (u) => 1 - (1 - u) * (1 - u);
/** 그 순간의 상태: 몇 번째 샷인지 · 선수 자리 · 공 자리 */
function stateAt(r, T, t) {
  const n = r.shots.length;
  let k = -1;
  for (let j = 0; j < n; j++) if (t >= T.shotsAt[j]) k = j;
  if (k < 0) return { k, u: 0, at: r.pos[0], ball: r.shots[0].a, h: 0, inFlight: false };
  const s = r.shots[k];
  const u = clamp((t - T.shotsAt[k]) / s.d);
  const e = ease(u);
  const at = r.pos[k].map((q, i) => [lerp(q[0], r.pos[k + 1][i][0], e), lerp(q[1], r.pos[k + 1][i][1], e)]);
  const ball = [lerp(s.a[0], s.b[0], u), lerp(s.a[1], s.b[1], u)];
  return { k, u, at, ball, h: s.h * 4 * u * (1 - u), inFlight: u < 1 };
}

export function NetArt({ C, mode, sport, ex, matches, at, fullPanel = true, credit }) {
  const mini = ex === "mini";
  if (!matches) return <MText x={mini ? 800 : 590} y={500} s="경기 자료를 불러오는 중…" size={34} anchor="middle" fill={C.soft} C={C} />;
  const S = NETS[sport], cam = netCam(sport, ex), isM = mode === "m";
  const { item, t } = at, T = item.T;
  const match = matches[item.m], r = match.rallies[item.i], teams = match.teams;
  const oOut = 1 - seg(t, T.outAt, T.outAt + NT.out);
  const kin = seg(t, 0, 500);
  const st = stateAt(r, T, t);
  const done = t >= T.endAt;
  const rep = T.replay && t >= T.replayAt ? seg(t, T.replayAt, T.replayAt + 600) * oOut : 0;
  const rt = t - T.replayAt;
  const ks = r.shots[r.key];
  const hitter = st.k >= 0 && st.inFlight ? r.shots[st.k].t * S.team + r.shots[st.k].w : -1;
  // 지나간 샷의 선
  const trails = [];
  r.shots.forEach((s, j) => {
    if (j > st.k) return;
    const A = cam.p(s.a), B = cam.p(j === st.k && st.inFlight ? st.ball : s.b);
    const col = teams[s.t].c, cr = crosses(s) || s.r === "net";
    const dim = rep > 0 && j !== r.key ? 1 - 0.75 * rep : 1;
    trails.push(<Path key={"t" + j} pts={[A, B]} stroke={col} sw={cr ? 3 : 2} dash={cr ? undefined : "4 6"} o={(cr ? 0.75 : 0.45) * dim * oOut} />);
    if (j < st.k || !st.inFlight) trails.push(<circle key={"d" + j} cx={B[0]} cy={B[1]} r={cr ? 4.5 : 3} fill={col} stroke="#fff" strokeWidth={1.2} opacity={0.9 * dim * oOut} />);
  });
  // 끝 표시
  const last = r.shots[r.shots.length - 1];
  const endK = seg(t, T.endAt, T.endAt + 400) * (1 - seg(t, T.replayAt - 200, T.replayAt + 300)) * oOut;
  const endP = cam.p(last.b);
  const endTxt = last.r === "net" ? "네트!" : last.r === "out" ? "아웃!" : "득점!";
  // 다시 보기(결정구)
  let replayEl = null;
  if (rep > 0) replayEl = <Replay sport={sport} ex={ex} mode={mode} s={ks} rt={rt} k={rep} C={C} teams={teams} />;
  const ballO = (done ? 1 - seg(t, T.endAt + 200, T.endAt + 900) : 1) * oOut * (st.k >= 0 ? 1 : 0);
  const sb = st.k >= 0 ? r.shots[st.k] : null;
  return (
    <g>
      <Court sport={sport} ex={ex} C={C} />
      <Axes sport={sport} ex={ex} mode={mode} C={C} />
      {trails}
      <Players sport={sport} ex={ex} r={r} teams={teams} at={st.at} C={C} hitter={hitter} o={kin * oOut} />
      {sb && <NBall sport={sport} p={cam.p(st.ball)} h={st.h} C={C} o={ballO} dir={[sb.b[0] - sb.a[0], -(sb.b[1] - sb.a[1])]} />}
      {endK > 0.01 && <UText x={clamp(endP[0], cam.box[0] + 70, cam.box[2] - 70)} y={clamp(endP[1] - 26, cam.box[1] + 40, cam.box[3] - 20)} s={endTxt} size={mini ? 40 : 34} weight={900} anchor="middle" fill={last.r === "in" ? C.gold : C.coral} halo={C.halo} opacity={endK} C={C} />}
      {replayEl}
      {!mini && fullPanel && <NetPanel C={C} mode={mode} sport={sport} match={match} r={r} T={T} t={t} st={st} idx={at.idx} n={at.n} credit={credit} />}
      {mini && <MiniBar C={C} mode={mode} sport={sport} match={match} r={r} T={T} t={t} st={st} />}
    </g>
  );
}

/** 결정구 다시 보기: 두 점 → 기울기 삼각형 → 직선 → 네트를 지난 자리 */
function Replay({ sport, ex, mode, s, rt, k, C, teams }) {
  const cam = netCam(sport, ex), S = NETS[sport], isM = mode === "m", mini = ex === "mini";
  const A = cam.p(s.a), B = cam.p(s.b);
  const off = S.view;
  const sh = (q) => (isM ? q : [q[0] + off[0], q[1] + off[1]]);
  const [bx0, by0, bx1, by1] = cam.box;
  const kp = seg(rt, RP.pts[0], RP.pts[1]), kt = seg(rt, RP.tri[0], RP.tri[1]), kl = seg(rt, RP.line[0], RP.line[1], E.out), kn = seg(rt, RP.net[0], RP.net[1]);
  const L = lineOf(s.a, s.b);
  const box = [-cam.v[0], -cam.v[1], cam.v[0], cam.v[1]];
  const full = L.kind === "pt" ? null : clipLine(s.a, [s.b[0] - s.a[0], s.b[1] - s.a[1]], box);
  const col = C.name === "light" ? "#0f766e" : "#7fe3d3";
  let lineEl = null;
  if (full && kl > 0) {
    const P0 = cam.p(full[0]), P1 = cam.p(full[1]), mid = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2];
    const ext = (q) => [lerp(mid[0], q[0], kl), lerp(mid[1], q[1], kl)];
    lineEl = <Path pts={[ext(P0), ext(P1)]} stroke={col} sw={3.4} dash="12 9" o={0.95 * k} />;
  }
  const dx = s.b[0] - s.a[0], dy = s.b[1] - s.a[1];
  const cn = [B[0], A[1]];
  const sx = isM ? `x ${dx > 0 ? "+" : "−"}${Math.abs(dx)}` : `가로 ${Math.abs(dx)}칸`;
  const sy = isM ? `y ${dy > 0 ? "+" : "−"}${Math.abs(dy)}` : `세로 ${Math.abs(dy)}칸`;
  const fitX = (x, w) => clamp(x, bx0 + w / 2 + 6, bx1 - w / 2 - 6);
  const fitY = (y) => clamp(y, by0 + 22, by1 - 30);
  const y0 = netY(s.a, s.b);
  const N = y0 == null ? null : cam.p([0, y0]);
  // 네트 이름표
  const { lines } = netSteps(s, mode, off);
  const netLine = lines[lines.length - 1];
  const onNet = Math.abs(s.b[0]) < 1e-9;   // 네트에 걸린 공: 떨어진 곳 = 네트 위 점
  const nLbl = isM ? (y0 == null ? "" : `y절편 ${(netLine.s.match(/\(0, [^)]*\)/) || [""])[0]}`) : onNet ? "네트에 걸린 곳" : "네트를 지난 곳";
  const eq = eqText(L);
  const eqEl = isM && full && eq ? (() => {
    const ke = seg(rt, RP.line[1] - 200, RP.line[1] + 400);
    const P0 = cam.p(full[0]), P1 = cam.p(full[1]);
    const u = Math.abs(P0[0] - A[0]) > Math.abs(P1[0] - A[0]) ? 0.18 : 0.82;
    const q = [lerp(P0[0], P1[0], u), lerp(P0[1], P1[1], u)];
    const w = chipW(eq, mini ? 28 : 24);
    return <Chip x={fitX(q[0], w)} y={fitY(q[1] + 36)} s={eq} size={mini ? 28 : 24} C={C} o={ke * k} />;
  })() : null;
  const fs2 = mini ? 27 : 23, ns2 = mini ? 30 : 25;   // 좌표 · 기울기 삼각형 칩, 네트(y절편) 칩 — 그림에서 눈에 띄게
  const la = { x: A[0] + (A[0] < B[0] ? -12 : 12), anchor: A[0] < B[0] ? "end" : "start", y: fitY(A[1] + (A[1] <= B[1] ? -(fs2 + 6) : fs2 + 12)) };
  const lb = { x: B[0] + (B[0] < A[0] ? -12 : 12), anchor: B[0] < A[0] ? "end" : "start", y: fitY(B[1] + (B[1] < A[1] ? -(fs2 + 6) : fs2 + 12)) };
  const clampLbl = (l, s2) => { const w = chipW(s2, fs2); return { ...l, x: l.anchor === "end" ? Math.max(l.x, bx0 + w + 6) : Math.min(l.x, bx1 - w - 6) }; };
  const la2 = clampLbl(la, pt(sh(s.a))), lb2 = clampLbl(lb, pt(sh(s.b)));
  // ── 기울기 · y절편 강조 칩 자리: 두 점 칩 · 삼각형 칩을 피해서 ──
  const pbox = [bx0, by0, bx1, by1];
  const avoid = [{ x: A[0], y: A[1], w: 18, h: 18 }, { x: B[0], y: B[1], w: 18, h: 18 },
    chipRect(la2.x, la2.y, pt(sh(s.a)), fs2, la2.anchor), chipRect(lb2.x, lb2.y, pt(sh(s.b)), fs2, lb2.anchor)];
  if (dx && dy) {
    avoid.push(chipRect(fitX((A[0] + B[0]) / 2, chipW(sx, fs2)), fitY(A[1] + (N ? (N[1] > A[1] ? -28 : 30) : dy > 0 ? 26 : -26)), sx, fs2));
    avoid.push(chipRect(fitX(B[0] + (dx > 0 ? 50 : -50), chipW(sy, fs2)), fitY((A[1] + B[1]) / 2), sy, fs2));
  }
  const tcol = C.name === "light" ? "#0f766e" : "#7fe3d3";
  const bs = mini ? 38 : 32;
  const slopeTxt = L.kind === "f" || L.kind === "h" ? (isM ? `기울기 ${fs(L.m[0], L.m[1])}` : dx && dy ? `세로 ÷ 가로 = ${fs(Math.abs(dy), Math.abs(dx))}` : "") : "";
  const sbw = slopeTxt ? bigW(slopeTxt, bs) : 0;
  const slopeAt = slopeTxt ? pickSpot([0.5, 0.35, 0.65, 0.25, 0.75].map((f) => besideLine(A, B, sbw, bs * 1.5, f, 1)).concat([0.5, 0.3, 0.7].map((f) => besideLine(A, B, sbw, bs * 1.5, f, -1))), sbw, bs * 1.5, avoid, pbox) : null;
  if (slopeAt) avoid.push({ x: slopeAt[0], y: slopeAt[1], w: sbw, h: bs * 1.5 });
  const nPos = N && nLbl ? (() => {
    const w = bigW(nLbl, ns2), h = ns2 * 1.5;
    const c = [-1, 1].flatMap((sd) => [1, -1, 2].map((kk) => [N[0] + sd * (w / 2 + 18), N[1] + kk * h * 0.8]));
    return pickSpot(c, w, h, avoid, pbox);
  })() : null;
  return (
    <g>
      <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} fill={C.name === "light" ? "#fffaf0" : "#0b1020"} opacity={0.28 * k} />
      {lineEl}
      {kt > 0 && dx && dy ? (
        <g opacity={kt * k}>
          <Path pts={[A, cn, B]} stroke="#fff" sw={2.4} dash="7 6" o={0.9} />
          <Chip x={fitX((A[0] + B[0]) / 2, chipW(sx, fs2))} y={fitY(A[1] + (N ? (N[1] > A[1] ? -28 : 30) : dy > 0 ? 26 : -26))} s={sx} size={fs2} C={C} />
          <Chip x={fitX(B[0] + (dx > 0 ? 50 : -50), chipW(sy, fs2))} y={fitY((A[1] + B[1]) / 2)} s={sy} size={fs2} C={C} />
        </g>
      ) : null}
      <Path pts={[A, B]} stroke={C.gold} sw={4.5} o={k} />
      <g opacity={kp * k}>
        <circle cx={A[0]} cy={A[1]} r={6.5} fill={C.gold} stroke="#fff" strokeWidth={2} />
        <circle cx={B[0]} cy={B[1]} r={6.5} fill={C.gold} stroke="#fff" strokeWidth={2} />
        <Chip x={la2.x} y={la2.y} s={pt(sh(s.a))} size={fs2} C={C} anchor={la2.anchor} />
        {!(onNet && isM && N) && <Chip x={lb2.x} y={lb2.y} s={pt(sh(s.b))} size={fs2} C={C} anchor={lb2.anchor} />}
      </g>
      {N && kn > 0 && (
        <g opacity={kn * k}>
          <circle cx={N[0]} cy={N[1]} r={16 * (1.6 - 0.6 * kn)} fill={C.gold} opacity={0.25} />
          <circle cx={N[0]} cy={N[1]} r={8} fill={C.gold} stroke="#fff" strokeWidth={2.4} />
          {nLbl && <BigChip x={nPos[0]} y={nPos[1]} s={nLbl} size={ns2} C={C} color={tcol} edge={tcol} />}
        </g>
      )}
      {eqEl}
      {slopeAt && <BigChip x={slopeAt[0]} y={slopeAt[1]} s={slopeTxt} size={bs} C={C} o={kt * k} />}
    </g>
  );
}

/* ══════════ 설명 판(상세) ══════════ */
function ScoreBoard({ x, y, w, C, sport, teams, sc, big = true }) {
  const rows = scoreRows(sport, teams, sc);
  const nsets = sc.sets.length;
  return (
    <g>
      {rows.map((R, i) => {
        const yy = y + i * (big ? 40 : 30);
        const nameW = w - 46 - nsets * 30 - (sport === "tennis" ? 104 : 54);
        return (
          <g key={i}>
            <circle cx={x + 9} cy={yy - 8} r={9} fill={R.col} stroke={inkOn(R.col) === "#ffffff" ? "#fff" : "#222"} strokeWidth={1.6} />
            <FitText x={x + 26} y={yy} s={R.name} size={big ? 22 : 18} maxW={nameW} weight={800} fill={C.ink} C={C} />
            {R.srv && <circle cx={x + 30 + Math.min(nameW, uWidth(R.name, big ? 22 : 18, 800)) + 12} cy={yy - 8} r={5} fill={C.gold} />}
            {R.sets.map((v, j) => <MText key={j} x={x + w - (sport === "tennis" ? 104 : 54) - (nsets - j) * 30 + 14} y={yy} s={String(v)} size={big ? 18 : 15} weight={700} anchor="middle" fill={C.soft} C={C} />)}
            <MText x={x + w - (sport === "tennis" ? 64 : 14)} y={yy} s={R.cur} size={big ? 26 : 20} weight={800} anchor="end" fill={C.gold} C={C} />
            {sport === "tennis" && <MText x={x + w - 6} y={yy} s={R.pts} size={big ? 20 : 16} weight={800} anchor="end" fill={C.teal} C={C} />}
          </g>
        );
      })}
    </g>
  );
}

function NetPanel({ C, mode, sport, match, r, T, t, st, idx, n, credit }) {
  const { x, y, w, h } = PANEL;
  const S = NETS[sport], teams = match.teams;
  const x0 = x + 22, mw = w - 44;
  const sc = t < T.endAt + 600 ? r.sc.pre : r.sc.post;
  const inRep = T.replay && t >= T.replayAt - 100;
  const kRep = T.replay ? seg(t, T.replayAt - 100, T.replayAt + 400) : 0;
  const head = match.title ? `${S.name} · ${match.title} · ${match.date}` : `${S.name} · 가상 경기 — ${ruleText[sport]}`;
  // 랠리 흐름(지나간 샷 · 최근 6개)
  const flow = [];
  const k = Math.max(st.k, -1);
  for (let j = Math.max(0, k - 5); j <= k; j++) {
    const s = r.shots[j];
    const lg = shotLog(s, mode, S.view);
    flow.push({ j, s, lg });
  }
  const ks = r.shots[r.key];
  const { lines } = netSteps(ks, mode, S.view);
  const shown = lines.map((L, j) => ({ ...L, col: L.col ? C[L.col] : undefined, at: T.replayAt + RP.step0 + j * RP.stepGap }));
  const scoreNote = t >= T.endAt + 600 && r.note ? r.note : "";
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <FitText x={x0} y={y + 34} s={head} size={15} maxW={scoreNote ? mw - 70 : mw} minSize={10} weight={650} fill={C.soft} C={C} />
      <ScoreBoard x={x0} y={y + 78} w={mw} C={C} sport={sport} teams={teams} sc={sc} />
      {scoreNote && <UText x={x + w - 22} y={y + 34} s={scoreNote} size={16} weight={800} anchor="end" fill={C.coral} C={C} />}
      <line x1={x0} x2={x + w - 22} y1={y + 134} y2={y + 134} stroke={C.cardEdge} strokeWidth={1.2} />
      {/* 랠리 흐름 */}
      <g opacity={1 - kRep}>
        <UText x={x0} y={y + 168} s={`랠리 ${idx + 1} · ${r.shots.length}번 오감`} size={18} weight={750} fill={C.soft} C={C} />
        {flow.map(({ j, s, lg }, i) => {
          const yy = y + 210 + i * 62;
          const cur = j === k;
          return (
            <g key={j} opacity={cur ? 1 : 0.62}>
              <circle cx={x0 + 8} cy={yy - 7} r={7} fill={teams[s.t].c} />
              <FitText x={x0 + 22} y={yy} s={`${j + 1}. ${s.ty} — ${WHO(teams, s)}`} size={19} maxW={mw - 22} weight={cur ? 800 : 650} fill={C.ink} C={C} />
              {lg && <FitText x={x0 + 22} y={yy + 27} s={lg} size={18} maxW={mw - 22} weight={700} fill={C.teal} C={C} />}
            </g>
          );
        })}
        {t >= T.endAt && <FitText x={x0} y={y + 210 + 6 * 62 + 4} s={`→ ${r.end} · ${teams[r.win].n} 득점`} size={21} maxW={mw} weight={800} fill={C.gold} C={C} opacity={seg(t, T.endAt, T.endAt + 400)} />}
      </g>
      {/* 결정구 다시 보기 */}
      {inRep && (
        <g opacity={kRep}>
          <FitText x={x0} y={y + 170} s={`결정구 다시 보기 — ${ks.ty} (${WHO(teams, ks)})`} size={19} maxW={mw} weight={800} fill={C.coral} C={C} />
          <Lines x={x0} y={y + 214} lines={shown} t={t} C={C} size={21} lh={43} maxW={mw} hiSize={27} />
        </g>
      )}
      <Small x={x0} y={y + h - 18} s={`${S.unit} · 랠리 ${idx + 1} / ${n}`} size={14} C={C} />
      <Small x={x + w - 22} y={y + h - 18} s={credit} size={13} C={C} anchor="end" />
    </g>
  );
}

/** 최소화: 위쪽 점수 막대 + 아래 한 줄 */
function MiniBar({ C, mode, sport, match, r, T, t, st }) {
  const S = NETS[sport], teams = match.teams, cam = netCam(sport, "mini");
  const sc = t < T.endAt + 600 ? r.sc.pre : r.sc.post;
  const rows = scoreRows(sport, teams, sc);
  const parts = rows.map((R) => `${R.name}${R.sets.length ? ` (${R.setsWon})` : ""} ${R.cur}${sport === "tennis" && R.pts ? ` · ${R.pts}` : ""}`);
  const s = `${parts[0]}  :  ${parts[1]}`;
  const w = textW(s, 22, 800) + 84;
  const k = st.k;
  const cur = k >= 0 ? r.shots[k] : null;
  const ks = r.shots[r.key];
  const inRep = T.replay && t >= T.replayAt;
  const cap = inRep ? `결정구 — ${ks.ty} (${WHO(teams, ks)}) · ${S.unit}` : cur ? `${k + 1}. ${cur.ty} — ${WHO(teams, cur)}` : `서브 — ${WHO(teams, r.shots[0])}`;
  const capW = textW(cap, 20, 750) + 32;
  const bx = cam.box[2] - w - 14, by = cam.box[1] + 14;
  return (
    <g>
      <rect x={bx} y={by} width={w} height={40} rx={20} fill={C.capBg} />
      <circle cx={bx + 24} cy={by + 20} r={8} fill={teams[0].c} stroke="#fff" strokeWidth={1.4} />
      <circle cx={bx + w - 24} cy={by + 20} r={8} fill={teams[1].c} stroke="#fff" strokeWidth={1.4} />
      <text x={bx + w / 2} y={by + 28} textAnchor="middle" fontFamily={SANS} fontSize={22} fontWeight={800} fill={C.capInk}>{s}</text>
      <rect x={cam.box[0] + 52} y={cam.box[3] - 64} width={capW} height={36} rx={18} fill={C.capBg} />
      <text x={cam.box[0] + 68} y={cam.box[3] - 39} fontFamily={SANS} fontSize={20} fontWeight={750} fill={inRep ? C.gold : C.capInk}>{cap}</text>
    </g>
  );
}

/* ══════════ 액자 ══════════ */
const MATCHES = new Map();
/** 가상 경기 두 판(씨앗 s, s + 1000)을 이어 돌린다 — 같은 배열을 다시 쓰도록 기억 */
function genPair(sport, seed) {
  const key = sport + "|" + seed;
  if (!MATCHES.has(key)) MATCHES.set(key, [genMatch(sport, seed), genMatch(sport, seed + 1000)]);
  return MATCHES.get(key);
}
let BCACHE = null;
function useBadminton(on) {
  const [d, setD] = useState(BCACHE);
  useEffect(() => {
    if (!on || BCACHE) return;
    let live = true;
    import("../curio/data-badminton.js").then((m) => { BCACHE = badmintonMatches(m.default); if (live) setD(BCACHE); }).catch(() => {});
    return () => { live = false; };
  }, [on]);
  return d;
}
const RPS = [["all", "매 랠리"], ["some", "가끔"], ["off", "끄기"]];
const BMATCH = ["전체", "코리아오픈 22", "말레이시아 22", "전영오픈 22", "세계선수권 22", "코리아오픈 19", "투어 파이널 20"];
const TITLE = {
  badminton: ["배드민턴으로 보는 좌표와 직선", "배드민턴으로 보는 일차함수"],
  tennis: ["테니스로 보는 좌표와 직선", "테니스로 보는 일차함수"],
  tabletennis: ["탁구로 보는 좌표와 직선", "탁구로 보는 일차함수"],
  volleyball: ["배구로 보는 좌표와 직선", "배구로 보는 일차함수"],
  jokgu: ["족구로 보는 좌표와 직선", "족구로 보는 일차함수"],
  sepak: ["세팍타크로로 보는 좌표와 직선", "세팍타크로로 보는 일차함수"],
};

export function NetFnFrame({ sport, C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const real = sport === "badminton";
  const DEF = { match: -1, rp: "all", ex: "full", sp: 1, seed: 1 };
  const fix = (p = {}) => ({
    match: real && [-1, 0, 1, 2, 3, 4, 5].includes(p.match) ? p.match : -1,
    rp: ["all", "some", "off"].includes(p.rp) ? p.rp : "all",
    ex: fixEx(p.ex), sp: SPEEDS.includes(p.sp) ? p.sp : 1,
    seed: Number.isInteger(p.seed) && p.seed > 0 && p.seed < 1e6 ? p.seed : 1,
  });
  const lab = useLabClock(`ash.display.curio.${sport}`, DEF, fix);
  const P = lab.prm;
  const bd = useBadminton(real);
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  // 경기 목록(같은 배열을 다시 써야 시간표 기억이 맞는다)
  let list = null;
  if (!real) list = genPair(sport, P.seed);
  else if (bd) {
    if (P.match < 0) list = bd;
    else { const m = bd[P.match]; if (!SINGLE.has(m)) SINGLE.set(m, [m]); list = SINGLE.get(m); }
  }
  const sched = list ? scheduleOf(list, P.rp) : null;
  const e = lab.elapsed() * P.sp;
  const at0 = sched ? rallyAt(sched, e) : null;
  const at = at0 ? { ...at0, n: sched.items.length } : null;
  const jump = (d) => {
    if (!sched || !at0) return;
    const j = clamp(at0.idx + d, 0, sched.items.length - 1);
    lab.jump((at0.k * sched.total + sched.items[j].at) / P.sp); poke();
  };
  const newMatch = () => { if (real) lab.restart(); else lab.setPrm({ seed: P.seed + 1 }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: newMatch, toggleFs, onMode, poke }),
    ArrowRight: () => jump(1), ArrowLeft: () => jump(-1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      {real && <Setting label="경기"><Stepper ui={ui} label="경기" value={P.match} options={[-1, 0, 1, 2, 3, 4, 5]} fmt={(v) => BMATCH[v + 1]} onChange={(v) => lab.setPrm({ match: v })} poke={poke} /></Setting>}
      <Setting label="풀이" sep={real}><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="결정구" sep><Seg label="결정구 다시 보기" value={P.rp} options={RPS} onChange={(v) => lab.setPrm({ rp: v })} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
      <span className="dsp-sep" />
      <ui.Btn title="이전 랠리 (←)" onClick={() => jump(-1)}><ui.Ic d="M15 5 8 12l7 7" /></ui.Btn>
      <ui.Btn title="다음 랠리 (→)" onClick={() => jump(1)}><ui.Ic d="m9 5 7 7-7 7" /></ui.Btn>
    </>
  );
  const S = NETS[sport];
  const m0 = list && at ? list[at.item.m] : null;
  const sub = m0 ? (real ? `${m0.title} · ${m0.teams[0].n} ${m0.final.filter((s) => s[0] > s[1]).length} : ${m0.final.filter((s) => s[0] < s[1]).length} ${m0.teams[1].n} · 친 곳과 떨어진 곳을 잇는 직선, 네트를 지난 자리`
    : `가상 경기 · ${m0.teams[0].n} vs ${m0.teams[1].n} · 네트(y축)를 지난 자리 = y절편`) : S.name;
  const credit = real ? "데이터: ShuttleSet (MIT)" : `가상 경기 · 씨앗 ${P.seed}`;
  const prog = sched && at0 ? (at0.item.at + at0.t) / sched.total : 0;
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label={`${S.name} 랠리로 보는 일차함수`}>
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={TITLE[sport][Ly.mode === "m" ? 1 : 0]} sub={sub} C={C} mode={Ly.mode} />
            <NetArt C={C} mode={Ly.mode} sport={sport} ex={P.ex} matches={list} at={at} credit={credit} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={newMatch}
        restartTitle={real ? "처음부터" : "새 경기"} isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings} prog={prog} />
    </>
  );
}
const SINGLE = new WeakMap();

/* ══════════ 목록 그림 ══════════ */
const THUMB_T = new Map();
/** 목록 그림: 그 종목 첫 경기에서 결정구 다시 보기가 있는 랠리의 한가운데 */
export const NetFnThumb = memo(function NetFnThumb({ sport, C, mode = "m" }) {
  let list = THUMB_T.get(sport);
  if (!list) {
    const m = sport === "badminton" ? THUMB_BWF : genMatch(sport, 7);
    const pickI = m.rallies.findIndex((r) => r.shots.length >= 4 && crosses(r.shots[r.key]) && r.shots[r.key].r === "in");
    const r = m.rallies[Math.max(0, pickI)];
    list = [{ ...m, rallies: [r] }];
    THUMB_T.set(sport, list);
  }
  const sched = scheduleOf(list, "all");
  const it = sched.items[0];
  return <NetArt C={C} mode={mode} sport={sport} ex="full" matches={list} at={{ item: it, idx: 0, n: 1, t: it.T.replayAt + 5600, k: 0 }} credit="" />;
});
// 목록 그림용 배드민턴 랠리 하나(2022 코리아오픈 결승, 안세영 — 자료 파일과 같은 꼴, 늦게 들여오지 않으려고 따로 둔다)
const THUMB_BWF = badmintonMatches({
  types: ["짧은 서브", "헤어핀", "로빙", "클리어", "스매시"],
  matches: [{ title: "2022 코리아오픈 결승", date: "2022. 4. 10.", names: ["안세영", "폰파위 초추웡"], cols: ["#e53935", "#1e88e5"], sets: [[21, 17], [21, 18]],
    rallies: [{ s: 1, pre: [12, 9], post: [13, 9], w: 0, e: "상대 코트에 떨어짐",
      sh: [[0, 0, -6, 1, 5, -2, -6.4, 1.1, 8.9, -1.6], [1, 1, 5, -2, -3, 3, 6.1, -1.8, -5.8, 0.7], [0, 2, -3, 3, 12, -4, -3.9, 2.4, 4.6, -1.5],
        [1, 3, 12, -4, -11, 2, 12.1, -3.6, -4.2, 2.3], [0, 4, -11, 2, 9, 5, -11.4, 1.8, 10.2, -2.9]] }] }],
})[0];
