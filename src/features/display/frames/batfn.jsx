// ashrain.out — 수학 호기심 액자: 야구로 보는 정비례 (frames/batfn.jsx)
// 실제 MLB 경기(Statcast 타구 기록, 2020. 9. 3. — 양키스–메츠 연장 끝내기 · 추신수 홈런 경기 · 커쇼 등판 · 블루제이스–레드삭스)의
// 인플레이 타구를 차례로: 타자 · 투수 · 주자 → 공이 날아가 떨어진 곳 → 홈플레이트와 그 점을 지나는 직선 → 설명.
//   좌표: 홈플레이트 = 원점, 1루 파울선 = x축, 3루 파울선 = y축 → 페어 지역이 그대로 제1사분면.
//         1루 (90, 0) · 2루 (90, 90) · 3루 (0, 90), 1칸 = 1피트.
//   중등: 타구 직선 y = ax(정비례) — 기울기가 1이면 한가운데, 1보다 크면 3루 쪽, 작으면 1루 쪽. 땅볼 아웃은 1루로 던진 송구 직선 y = ax + b 까지.
//   초등: 1루 쪽으로 몇 피트, 3루 쪽으로 몇 피트 — 3루 쪽 ÷ 1루 쪽으로 방향을 읽는다.
// 구장 윤곽은 그 경기 구장(시티 필드 · 미닛메이드 파크 · 다저 스타디움 · 펜웨이 파크). 자료: ../curio/data-mlb.js(늦게 들여온다)
import { memo, useEffect, useState } from "react";
import { W, H, MText, SceneTitle, Path } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, Chip, chipW, uWidth } from "../kit-story.jsx";
import { lineOf, lineSteps, fs, pt, num, eqText, cycleAt, SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx } from "../curio/kit.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { FitText, Lines, Panel, Small, clipLine, BigChip, bigW, besideLine, pickSpot } from "./curio-kit.jsx";

const LSK = "ash.display.curio.batfn";
const GAMES = [-1, 0, 1, 2, 3];
const GAME_SHORT = ["양키스–메츠", "레인저스–애스트로스", "D백스–다저스", "블루제이스–레드삭스"];
const DEF = { game: -1, sp: 1, ex: "full" };
const fixPrm = (p = {}) => ({ game: GAMES.includes(p.game) ? p.game : -1, sp: SPEEDS.includes(p.sp) ? p.sp : 1, ex: fixEx(p.ex) });

/* ── 무대: 구장(가운데 왼쪽, 홈이 아래) · 설명 판(오른쪽) ── */
const S = 1.66, HX = 540, HY = 866;
const R2 = Math.SQRT1_2;
/** 세계 (u = 1루 쪽, v = 3루 쪽, 피트) → 무대 */
export const bp = (q) => [HX + (q[0] - q[1]) * R2 * S, HY - (q[0] + q[1]) * R2 * S];
/** 홈에서 (U, V) 쪽으로 425피트 — 직선을 구장 끝까지만 */
const farOf = (U, V) => { const r = Math.hypot(U, V) || 1; return [(U * 425) / r, (V * 425) / r]; };
const PANEL = { x: 1060, y: 150, w: 502, h: 720 };
/** 그림 영역(설명 판 왼쪽) — 직선 · 이름표가 판 밑이나 무대 밖으로 나가지 않게(위쪽은 가운데 담장 너머까지 비어 있다) */
const AREA_FULL = [8, 30, PANEL.x - 14, 896];
/*
 * 최소화: 설명 판 없이 그 타구 쪽으로 다가간 카메라(홈 · 떨어진 곳 · 송구 끝을 넉넉히). 지도 B = { p, s }.
 * 공 길 · 직선은 그대로, 좌표는 판 아래 · 왼쪽 가장자리 자 대신 파울선(축) 눈금으로 읽는다.
 */
const MBOX = [36, 150, 1564, 872];
const VFULL = { p: bp, s: S, area: AREA_FULL, mini: false };
const ZB = new WeakMap();
function zoomOf(b) {
  if (ZB.has(b)) return ZB.get(b);
  const pts = [[0, 0], [b.u, b.v], [b.U, b.V], ...(b.th ? [b.th] : [])];
  const X = pts.map((q) => (q[0] - q[1]) * R2), Y = pts.map((q) => (q[0] + q[1]) * R2);
  const mg = 40;
  let x0 = Math.min(...X) - mg, x1 = Math.max(...X) + mg, y0 = Math.min(...Y) - mg, y1 = Math.max(...Y) + mg;
  const w = Math.max(230, x1 - x0), h = Math.max(170, y1 - y0);
  const aw = MBOX[2] - MBOX[0], ah = MBOX[3] - MBOX[1] - 70;
  const s = clamp(Math.min(aw / w, ah / h), 1.62, 4.2);
  const z = { s, cx: (x0 + x1) / 2, cy: clamp((y0 + y1) / 2, -20 + ah / s / 2 - 30, 440) };
  ZB.set(b, z);
  return z;
}
function viewOf(z) {
  const mx = (MBOX[0] + MBOX[2]) / 2, my = (MBOX[1] + 70 + MBOX[3]) / 2;
  const p = (q) => [mx + ((q[0] - q[1]) * R2 - z.cx) * z.s, my - ((q[0] + q[1]) * R2 - z.cy) * z.s];
  return { p, s: z.s, area: [MBOX[0] + 4, MBOX[1] + 4, MBOX[2] - 4, MBOX[3] - 4], mini: true };
}
/** 홈(영역 안)에서 p 쪽으로 그은 선분을 영역 안까지만 */
function inArea(a, p, AREA = AREA_FULL) {
  let k = 1;
  const dx = p[0] - a[0], dy = p[1] - a[1];
  if (dx > 0) k = Math.min(k, (AREA[2] - a[0]) / dx); else if (dx < 0) k = Math.min(k, (AREA[0] - a[0]) / dx);
  if (dy > 0) k = Math.min(k, (AREA[3] - a[1]) / dy); else if (dy < 0) k = Math.min(k, (AREA[1] - a[1]) / dy);
  k = Math.max(0, k);
  return [a[0] + dx * k, a[1] + dy * k];
}

export const BC = { D: 9000, in: [0, 500], pitch: [500, 1100], hit: [1200, 2600], land: [2600, 3000], line: [3000, 3900], thr: [3900, 4800], thl: [4800, 5400], out: [8300, 9000] };
const STEP_AT = [800, 2700, 3200, 3800, 4400, 5000, 5600, 6200, 6800];

const LIST = new WeakMap();
export function ballsOf(data, P) {
  const key = `${P.game}`;
  if (!LIST.has(data)) LIST.set(data, new Map());
  const memo = LIST.get(data);
  if (memo.has(key)) return memo.get(key);
  const out = [];
  data.games.forEach((g, gi) => { if (P.game >= 0 && P.game !== gi) return; g.balls.forEach((b, n) => out.push({ gi, b, n })); });
  memo.set(key, out);
  return out;
}

const dirWord = (U, V) => {
  if (U < 0 || V < 0) return "파울 지역 — 제1사분면 밖";
  const r = V / U;
  if (Math.abs(r - 1) < 0.05) return "기울기 1 — 2루 쪽 한가운데";
  return r > 1 ? "기울기 > 1 — 3루(왼쪽) 쪽 타구" : "기울기 < 1 — 1루(오른쪽) 쪽 타구";
};
export function batSteps(b, mode) {
  const Q = [b.U, b.V];
  const out = [];
  if (mode === "m") {
    out.push({ s: `떨어진 곳 ${pt(Q)}` });
    if (Q[0] === 0 && Q[1] === 0) return [...out, { s: "홈과 같은 점 — 직선이 하나로 안 정해져요", small: true }];
    const { lines } = lineSteps([0, 0], Q, { origin: true });
    out.push(...lines.filter((l) => !l.small));
    out.push({ s: dirWord(b.U, b.V), small: true });
    if (b.th) {
      const L2 = lineOf(Q, b.th);
      out.push({ s: `송구 ${pt(Q)} → 1루 ${pt(b.th)}`, gap: 6 });
      if (L2.kind === "f") {
        out.push({ s: `기울기 = {${num(b.th[1])} − ${Q[1] < 0 ? `(${num(Q[1])})` : Q[1]}/${num(b.th[0])} − ${Q[0] < 0 ? `(${num(Q[0])})` : Q[0]}} = ${fs(L2.m[0], L2.m[1])}` });
        out.push({ s: eqText(L2), hi: true, col: "lilac" });
      } else out.push({ s: eqText(L2), hi: true, col: "lilac" });
    }
    return out;
  }
  out.push({ s: `떨어진 곳 ${pt(Q)}` });
  if (Q[0] <= 0 || Q[1] <= 0) { out.push({ s: "파울 지역(1루선 · 3루선 바깥)", small: true }); return out; }
  out.push({ s: `1루 쪽으로 ${Q[0]}피트, 3루 쪽으로 ${Q[1]}피트` });
  out.push({ s: "방향 = 3루 쪽 ÷ 1루 쪽", small: true });
  out.push({ s: `${Q[1]} ÷ ${Q[0]} = ${fs(Q[1], Q[0])}`, hi: true });
  out.push({ s: Q[1] === Q[0] ? "1이면 한가운데(2루 쪽)" : Q[1] > Q[0] ? "1보다 커요 → 왼쪽(3루) 쪽으로 간 공" : "1보다 작아요 → 오른쪽(1루) 쪽으로 간 공", small: true });
  return out;
}

/* ══════════ 구장 ══════════ */
function fieldColors(C) {
  return C.name === "light"
    ? { stands: "#d9cdb3", foul: "#bfd6a2", grass: "#a9cc85", grass2: "#a1c47d", dirt: "#d9b384", track: "#cfa877", line: "#ffffff", ink: "#2f3a22", halo: "#e6f0da" }
    : { stands: "#1a2238", foul: "#1f3a2c", grass: "#25503a", grass2: "#224a36", dirt: "#6a4a33", track: "#5a3f2c", line: "#efe7d6", ink: "#f1ead8", halo: "#183022" };
}
const polyD = (pts, P = bp) => "M" + pts.map((q) => P(q).map((v) => v.toFixed(1)).join(" ")).join("L") + "Z";
const arcOf = (fence) => fence.filter((p) => p[0] > 4 && p[1] > 4).sort((a, b) => Math.atan2(a[1], a[0]) - Math.atan2(b[1], b[0]));
const Field = memo(function Field({ C, park, pk, B = VFULL }) {
  const bp = B.p, S = B.s;
  const K = fieldColors(C);
  const bases = [[90, 0], [90, 90], [0, 90]].map(bp);
  const home = bp([0, 0]), mound = bp([42.8, 42.8]);
  const arc = arcOf(park.fence);
  const a0 = arc[0], a1 = arc[arc.length - 1];
  const bowl = [[-48, -48], [a0[0] * 1.07 + 18, -48], ...arc.map((p) => [p[0] * 1.07, p[1] * 1.07]), [-48, a1[1] * 1.07 + 18]];
  // 잔디 띠: 홈에서 퍼지는 부채꼴 줄무늬
  const stripes = [];
  for (let a = 0; a < 90; a += 7.5) {
    if ((a / 7.5) % 2) continue;
    const r = 470, rad = (d) => (d * Math.PI) / 180;
    stripes.push(<path key={a} d={polyD([[0, 0], [r * Math.cos(rad(a)), r * Math.sin(rad(a))], [r * Math.cos(rad(a + 7.5)), r * Math.sin(rad(a + 7.5))]], bp)} fill={K.grass2} />);
  }
  const fid = `curio-fence-${pk}-${C.name}`;
  const arcD = "M" + arc.map((q) => bp(q).map((v) => v.toFixed(1)).join(" ")).join("L");
  return (
    <g>
      <path d={polyD(bowl, bp)} fill={K.foul} />
      <defs><clipPath id={fid}><path d={polyD(park.fence, bp)} /></clipPath></defs>
      <path d={polyD(park.fence, bp)} fill={K.grass} />
      <g clipPath={`url(#${fid})`}>
        {stripes}
        <path d={arcD} fill="none" stroke={K.track} strokeWidth={15 * S * 2} strokeLinejoin="round" />
      </g>
      <path d={arcD} fill="none" stroke={K.ink} strokeOpacity={0.6} strokeWidth={3} strokeLinejoin="round" />
      <path d={polyD(park.dirt, bp)} fill={K.dirt} />
      <path d={polyD(park.grass, bp)} fill={K.grass} />
      <circle cx={mound[0]} cy={mound[1]} r={9 * S} fill={K.dirt} />
      <circle cx={home[0]} cy={home[1] - 2} r={13 * S} fill={K.dirt} />
      {[0, 1].map((i) => {
        const end = i ? bp([0, a1[1] * 1.0]) : bp([a0[0] * 1.0, 0]);
        return <line key={i} x1={home[0]} y1={home[1]} x2={end[0]} y2={end[1]} stroke={K.line} strokeWidth={2.4} opacity={0.9} />;
      })}
      {bases.map((q, i) => <rect key={i} x={q[0] - 6} y={q[1] - 6} width={12} height={12} transform={`rotate(45 ${q[0]} ${q[1]})`} fill="#fff" stroke="#555" strokeWidth={1} />)}
      <path d={`M${home[0] - 7} ${home[1] - 6}h14v6l-7 6l-7 -6z`} fill="#fff" stroke="#555" strokeWidth={1} />
      <rect x={mound[0] - 6} y={mound[1] - 1.5} width={12} height={3} fill="#fff" />
    </g>
  );
});

/** 비스듬한 좌표축(파울선) · 50피트 눈금 · 옅은 모눈 */
function BatAxes({ C, o, B = VFULL }) {
  if (o <= 0.001) return null;
  const bp = B.p;
  const K = fieldColors(C);
  const grid = [], lab = [];
  for (let c = 50; c <= 400; c += 50) {
    const vmax = Math.sqrt(Math.max(0, 430 * 430 - c * c));
    const a1 = bp([c, 0]), a2 = bp([c, vmax]), b1 = bp([0, c]), b2 = bp([vmax, c]);
    grid.push(<line key={"u" + c} x1={a1[0]} y1={a1[1]} x2={a2[0]} y2={a2[1]} stroke={K.ink} strokeOpacity={0.09} strokeWidth={1.2} />);
    grid.push(<line key={"v" + c} x1={b1[0]} y1={b1[1]} x2={b2[0]} y2={b2[1]} stroke={K.ink} strokeOpacity={0.09} strokeWidth={1.2} />);
    if (c >= 200 && c % 100 === 0) {
      const pu = bp([c, 0]), pv = bp([0, c]);
      lab.push(<MText key={"lu" + c} x={pu[0] + 12} y={pu[1] + 18} s={String(c)} size={14} weight={700} fill={K.ink} halo={K.halo} opacity={0.85} C={C} />);
      lab.push(<MText key={"lv" + c} x={pv[0] - 12} y={pv[1] + 18} s={String(c)} size={14} weight={700} anchor="end" fill={K.ink} halo={K.halo} opacity={0.85} C={C} />);
    }
  }
  const ex = bp([420, 0]), ey = bp([0, 420]), O = bp([0, 0]);
  return (
    <g opacity={o}>
      {grid}
      <line x1={O[0]} y1={O[1]} x2={ex[0]} y2={ex[1]} stroke={K.ink} strokeWidth={2} opacity={0.6} />
      <line x1={O[0]} y1={O[1]} x2={ey[0]} y2={ey[1]} stroke={K.ink} strokeWidth={2} opacity={0.6} />
      <MText x={ex[0] + 8} y={ex[1] + 4} s="x" size={22} fill={K.ink} halo={K.halo} C={C} />
      <MText x={ey[0] - 8} y={ey[1] + 4} s="y" size={22} anchor="end" fill={K.ink} halo={K.halo} C={C} />
      <MText x={O[0] + 14} y={O[1] + 24} s="O" size={16} weight={700} fill={K.ink} halo={K.halo} C={C} />
      <MText x={bp([90, 0])[0] + 14} y={bp([90, 0])[1] + 6} s="1루 (90, 0)" size={13} weight={700} fill={K.ink} halo={K.halo} opacity={0.85} C={C} />
      <MText x={bp([0, 90])[0] - 14} y={bp([0, 90])[1] + 6} s="3루 (0, 90)" size={13} weight={700} anchor="end" fill={K.ink} halo={K.halo} opacity={0.85} C={C} />
      <MText x={bp([90, 90])[0]} y={bp([90, 90])[1] - 14} s="2루 (90, 90)" size={13} weight={700} anchor="middle" fill={K.ink} halo={K.halo} opacity={0.85} C={C} />
      {lab}
    </g>
  );
}

/* ══════════ 장면 ══════════ */
const isHit = (b) => /안타|루타|홈런/.test(b.res);
export function BatArt({ C, mode, P, data, at, ex = "full" }) {
  if (!data) return <MText x={560} y={520} s="경기 자료를 불러오는 중…" size={34} anchor="middle" fill={C.soft} C={C} />;
  const list = ballsOf(data, P);
  if (!list.length) return null;
  const { i, t } = at;
  const { gi, b, n } = list[i];
  const game = data.games[gi], park = data.parks[game.park], teams = game.teams;
  const K = fieldColors(C);
  const isM = mode === "m", mini = ex === "mini";
  // 최소화 카메라: 지난 타구 카메라에서 이번 타구 카메라로 0.9초
  let Bv = VFULL;
  if (mini) {
    const z1 = zoomOf(b), pb = list.length > 1 && (i > 0 || at.k > 0) ? list[(i - 1 + list.length) % list.length].b : null;
    const z0 = pb ? zoomOf(pb) : z1, kz = seg(t, 0, 900, E.io);
    Bv = viewOf({ s: Math.exp(lerp(Math.log(z0.s), Math.log(z1.s), kz)), cx: lerp(z0.cx, z1.cx, kz), cy: lerp(z0.cy, z1.cy, kz) });
  }
  const bp = Bv.p, AREA = Bv.area;
  const inA = (a2, p2) => inArea(a2, p2, AREA);
  const oOut = 1 - seg(t, BC.out[0], BC.out[1]);
  const home = bp([0, 0]), land = bp([b.u, b.v]), Q = bp([b.U, b.V]);
  const batTeam = teams[b.tb];
  // 지난 타구(이 경기)
  const prev = game.balls.slice(0, n);
  const dots = prev.map((q, j) => {
    const p = bp([q.u, q.v]);
    return isHit(q) ? <circle key={j} cx={p[0]} cy={p[1]} r={5} fill={teams[q.tb].c} stroke={teams[q.tb].k} strokeWidth={1} opacity={0.75} />
      : <circle key={j} cx={p[0]} cy={p[1]} r={4.2} fill="none" stroke={teams[q.tb].c} strokeWidth={2} opacity={0.6} />;
  });
  const ghost = prev.slice(-40).map((q, j, arr) => {
    if (q.U === 0 && q.V === 0) return null;
    return <Path key={j} pts={[home, inA(home, bp(farOf(q.U, q.V)))]} stroke={teams[q.tb].c} sw={1.4} o={0.05 + 0.1 * ((j + 1) / arr.length)} />;
  });
  // 투구 → 타구
  const kp = seg(t, BC.pitch[0], BC.pitch[1], E.lin);
  const mound = bp([42.8, 42.8]);
  const pitchEl = kp > 0 && kp < 1 ? <circle cx={lerp(mound[0], home[0], kp)} cy={lerp(mound[1], home[1], kp)} r={4} fill="#fff" stroke="#333" strokeWidth={1} /> : null;
  const kh = seg(t, BC.hit[0], BC.hit[1], b.bb === "땅볼" ? E.out : E.io);
  const fly = b.bb === "뜬공" || b.bb === "내야 뜬공" || b.ev === "home_run" ? 1 : b.bb === "직선타" ? 0.35 : 0;
  const bh = fly * 4 * kh * (1 - kh) * clamp((b.dist || 200) / 300, 0.3, 1.4);
  const bq = [lerp(home[0], land[0], kh), lerp(home[1], land[1], kh)];
  const bounce = b.bb === "땅볼" ? Math.abs(Math.sin(kh * Math.PI * 3)) * (1 - kh) * 0.25 : 0;
  // 송구
  const thr = b.th ? bp(b.th) : null;
  const kt = thr ? seg(t, BC.thr[0], BC.thr[1], E.io) : 0;
  let ballAt = null, ballH = 0;
  if (kh > 0 && kh < 1) { ballAt = bq; ballH = bh + bounce; }
  else if (kh >= 1 && thr && kt > 0 && kt < 1) { ballAt = [lerp(land[0], thr[0], kt), lerp(land[1], thr[1], kt)]; ballH = 0.25 * 4 * kt * (1 - kt); }
  else if (kh >= 1 && !(thr && kt >= 1)) { ballAt = land; }
  // 직선(타구) · 송구 직선
  const kl = seg(t, BC.line[0], BC.line[1], E.out);
  const L = lineOf([0, 0], [b.U, b.V]);
  let lineEl = null;
  if (L.kind !== "pt" && kl > 0) {
    const r = Math.hypot(b.U, b.V) || 1, fr = Math.max(425, r + 25);   // 담장 너머 홈런은 떨어진 곳보다 조금 더
    const far = inA(home, bp([(b.U * fr) / r, (b.V * fr) / r]));
    lineEl = <Path pts={[home, [lerp(Q[0], far[0], kl), lerp(Q[1], far[1], kl)]]} stroke={C.name === "light" ? "#0f766e" : "#7fe3d3"} sw={3} dash="12 9" o={0.95 * oOut} />;
  }
  const ktl = thr ? seg(t, BC.thl[0], BC.thl[1], E.out) : 0;
  let thrEl = null;
  if (thr && ktl > 0) {
    const L2 = lineOf([b.U, b.V], b.th);
    const d = L2.kind === "v" ? [0, 1] : [L2.dx, L2.dy];
    const sg = clipLine([b.U, b.V], d, [-60, -60, 300, 300]);
    if (sg) {
      const A = bp(sg[0]), B = bp(sg[1]), mid = [(Q[0] + thr[0]) / 2, (Q[1] + thr[1]) / 2];
      thrEl = <Path pts={[[lerp(mid[0], A[0], ktl), lerp(mid[1], A[1], ktl)], [lerp(mid[0], B[0], ktl), lerp(mid[1], B[1], ktl)]]} stroke={C.lilac} sw={2.8} dash="9 8" o={0.9 * oOut} />;
    }
  }
  const trail = kh > 0 ? <Path pts={[home, kh >= 1 ? land : bq]} stroke={C.gold} sw={3.2} o={0.9 * oOut} /> : null;
  const thrTrail = thr && kt > 0 ? <Path pts={[land, kt >= 1 ? thr : [lerp(land[0], thr[0], kt), lerp(land[1], thr[1], kt)]]} stroke={C.lilac} sw={2.8} o={0.85 * oOut} /> : null;
  const kland = seg(t, BC.land[0], BC.land[1]);
  const eq = isM && L.kind !== "pt" ? eqText(L) : "";
  const hr = b.ev === "home_run" && kh >= 1 ? seg(t, BC.hit[1], BC.hit[1] + 400) * (1 - seg(t, BC.hit[1] + 2600, BC.hit[1] + 3300)) : 0;
  // 떨어진 곳 이름표 자리(좌표 칩 — 그림에서 눈에 띄게)
  const CS = mini ? 26 : 23;
  const lt = (() => {
    const w = chipW(pt([b.U, b.V]), CS);
    let sd = b.U >= b.V ? 1 : -1;
    if (sd > 0 && land[0] + 16 + w > AREA[2]) sd = -1;
    else if (sd < 0 && land[0] - 16 - w < AREA[0]) sd = 1;
    const y = land[1] - 28 < AREA[1] + 14 ? land[1] + 32 : land[1] - 28;
    return { x: land[0] + sd * 16, y, anchor: sd > 0 ? "start" : "end", w };
  })();
  // 기울기 칩(금테 · 크게) — 홈에서 떨어진 곳까지의 직선 옆
  const bs = mini ? 38 : 32;
  const slopeTxt = L.kind === "pt" || L.kind === "v" ? "" : isM ? `기울기 ${fs(L.m[0], L.m[1])}` : b.U > 0 && b.V > 0 ? `3루 쪽 ÷ 1루 쪽 = ${fs(b.V, b.U)}` : "";
  const sbw = slopeTxt ? bigW(slopeTxt, bs) : 0;
  const slopeAt = slopeTxt ? pickSpot([0.55, 0.4, 0.7, 0.3, 0.8].flatMap((f) => [besideLine(home, Q, sbw, bs * 1.5, f, 1), besideLine(home, Q, sbw, bs * 1.5, f, -1)]), sbw, bs * 1.5,
    [{ x: home[0], y: home[1], w: 60, h: 60 }, { x: land[0], y: land[1], w: 20, h: 20 }, { x: lt.x + (lt.anchor === "start" ? lt.w / 2 : -lt.w / 2), y: lt.y, w: lt.w, h: CS * 1.5 },
      ...(thr ? [{ x: thr[0], y: thr[1], w: 30, h: 30 }] : []), ...(mini ? [{ x: MBOX[0] + 260, y: MBOX[1] + 56, w: 520, h: 90 }, { x: MBOX[2] - 200, y: MBOX[1] + 32, w: 400, h: 40 }] : [])],
    AREA) : null;
  // 주자
  const runners = [[90, 0], [90, 90], [0, 90]].map((q, j) => b.on[j] ? bp(q) : null).filter(Boolean);
  return (
    <g>
      {mini && <defs><clipPath id="bat-mini-clip"><rect x={MBOX[0]} y={MBOX[1]} width={MBOX[2] - MBOX[0]} height={MBOX[3] - MBOX[1]} rx={16} /></clipPath></defs>}
      <g clipPath={mini ? "url(#bat-mini-clip)" : undefined}>
      {mini && <rect x={MBOX[0]} y={MBOX[1]} width={MBOX[2] - MBOX[0]} height={MBOX[3] - MBOX[1]} fill={K.stands} />}
      <Field C={C} park={park} pk={game.park} B={Bv} />
      <BatAxes C={C} o={1} B={Bv} />
      {ghost}
      {dots}
      {lineEl}
      {thrEl}
      {trail}
      {thrTrail}
      <g opacity={seg(t, BC.in[0], BC.in[1]) * oOut}>
        {runners.map((q, j) => <circle key={j} cx={q[0]} cy={q[1] - 12} r={8} fill={batTeam.c} stroke={batTeam.k} strokeWidth={2} />)}
        <circle cx={home[0] + (b.st === "L" ? 14 : -14)} cy={home[1] - 6} r={8} fill={batTeam.c} stroke={batTeam.k} strokeWidth={2} />
        <circle cx={mound[0]} cy={mound[1] - 4} r={7} fill={teams[1 - b.tb].c} stroke={teams[1 - b.tb].k} strokeWidth={2} />
      </g>
      {pitchEl}
      <g opacity={kland * oOut}>
        <circle cx={land[0]} cy={land[1]} r={7} fill={C.gold} stroke="#fff" strokeWidth={2} />
        <Chip x={lt.x} y={lt.y} s={pt([b.U, b.V])} size={CS} C={C} anchor={lt.anchor} />
      </g>
      {ballAt && oOut > 0.01 && (
        <g>
          <ellipse cx={ballAt[0]} cy={ballAt[1] + 4} rx={5} ry={2} fill="#000" opacity={0.25} />
          <circle cx={ballAt[0]} cy={ballAt[1] - ballH * 70} r={5 + 4 * ballH} fill="#fbfbf5" stroke="#b33" strokeWidth={1.4} />
        </g>
      )}
      {eq && !mini && (() => { const w = chipW(eq, 24); const q = pickSpot([0.3, 0.8, 0.2, 0.9].flatMap((f) => [besideLine(home, Q, w, 36, f, -1), besideLine(home, Q, w, 36, f, 1)]), w, 36, [...(slopeAt ? [{ x: slopeAt[0], y: slopeAt[1], w: sbw, h: bs * 1.5 }] : []), { x: home[0], y: home[1], w: 60, h: 60 }, { x: land[0], y: land[1], w: 20, h: 20 }, { x: lt.x + (lt.anchor === "start" ? lt.w / 2 : -lt.w / 2), y: lt.y, w: lt.w, h: CS * 1.5 }], [140, 200, 990, 820]); return <Chip x={q[0]} y={q[1]} s={eq} size={24} C={C} o={seg(t, BC.line[1] - 300, BC.line[1] + 300) * oOut} />; })()}
      {slopeAt && <BigChip x={slopeAt[0]} y={slopeAt[1]} s={slopeTxt} size={bs} C={C} o={seg(t, BC.line[0] + 300, BC.line[1]) * oOut} />}
      {hr > 0 && <UText x={land[0]} y={land[1] - 40} s="홈런!" size={44 + 10 * hr} weight={900} anchor="middle" fill={C.gold} halo={C.halo} opacity={Math.min(1, hr * 1.5)} C={C} />}
      </g>
      {mini && <rect x={MBOX[0]} y={MBOX[1]} width={MBOX[2] - MBOX[0]} height={MBOX[3] - MBOX[1]} rx={16} fill="none" stroke={C.cardEdge} strokeWidth={1.4} />}
      {!mini && <BatPanel C={C} mode={mode} game={game} park={park} b={b} t={t} idx={i} total={list.length} oOut={oOut} />}
      {mini && <BatMini C={C} mode={mode} game={game} b={b} t={t} oOut={oOut} />}
    </g>
  );
}

/** 최소화 — 위 왼쪽: 경기 · 회 · 점수, 위 오른쪽: 타자 → 결과, 둘째 줄: 식(중등) 또는 방향(초등) */
function BatMini({ C, mode, game, b, t, oOut }) {
  const teams = game.teams, done = t >= BC.land[0], sc = done ? b.post : b.pre;
  const a = `${teams[0].n} ${sc[0]} : ${sc[1]} ${teams[1].n} · ${b.i}회${b.tb ? "말" : "초"} · ${b.outs}아웃`;
  const r = `${b.bat}${done ? ` → ${b.res}` : ""}`;
  const L = batSteps(b, mode), hi = [...L].reverse().find((q) => q.hi) || L[L.length - 1];
  const kin = seg(t, 0, 500) * oOut;
  return (
    <g>
      <Chip x={MBOX[0] + 16} y={MBOX[1] + 32} s={a} size={21} C={C} anchor="start" o={kin} />
      <Chip x={MBOX[2] - 16} y={MBOX[1] + 32} s={r} size={21} C={C} anchor="end" color={done && /홈런|안타|루타/.test(b.res) ? C.gold : undefined} o={kin} />
      {hi && <Chip x={MBOX[0] + 16} y={MBOX[1] + 80} s={hi.s} size={25} C={C} anchor="start" color={C.gold} o={seg(t, BC.line[1], BC.line[1] + 500) * oOut} />}
    </g>
  );
}
const outsDots = (k, C, x, y) => [0, 1, 2].map((j) => <circle key={j} cx={x + j * 18} cy={y} r={6} fill={j < k ? C.coral : "none"} stroke={C.soft} strokeWidth={1.6} />);
function BatPanel({ C, mode, game, park, b, t, idx, total, oOut }) {
  const { x, y, w, h } = PANEL, x0 = x + 24, mw = w - 48;
  const teams = game.teams;
  const done = t >= BC.land[0];
  const sc = done ? b.post : b.pre;
  const lines = batSteps(b, mode).map((L, j) => ({ ...L, col: L.col ? C[L.col] : undefined, at: STEP_AT[Math.min(j, STEP_AT.length - 1)] }));
  const kmh = b.ls ? Math.round(b.ls * 1.609) : null, m = b.dist ? Math.round(b.dist * 0.3048) : null;
  const info = [kmh && `타구 속도 ${kmh}km/h`, b.la != null && `발사각 ${Math.round(b.la)}°`, m && `비거리 ${m}m`].filter(Boolean).join(" · ");
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <Small x={x0} y={y + 34} s={`${game.date} · MLB 정규 시즌 · ${park.name}`} size={16} C={C} />
      {teams.map((tm, j) => (
        <g key={j}>
          <circle cx={x0 + 9} cy={y + 64 + j * 32} r={8} fill={tm.c} stroke={tm.k} strokeWidth={1.6} />
          <UText x={x0 + 26} y={y + 71 + j * 32} s={tm.n} size={21} weight={j === b.tb ? 800 : 650} fill={j === b.tb ? C.ink : C.soft} C={C} />
          <UText x={x0 + 300} y={y + 71 + j * 32} s={String(sc[j])} size={24} weight={800} anchor="end" C={C} />
        </g>
      ))}
      <UText x={x0 + 330} y={y + 76} s={`${b.i}회${b.tb ? "말" : "초"}`} size={22} weight={800} fill={mode === "m" ? C.teal : C.coral} C={C} />
      <g transform={`translate(${x0 + 334}, ${y + 102})`}>{outsDots(b.outs, C, 0, 0)}</g>
      <g transform={`translate(${x0 + 420}, ${y + 84})`}>
        {[[0, -16], [-16, 0], [16, 0]].map(([dx, dy], j) => {
          const on = b.on[[1, 2, 0][j]];
          return <rect key={j} x={dx - 6} y={dy - 6} width={12} height={12} transform={`rotate(45 ${dx} ${dy})`} fill={on ? C.gold : "none"} stroke={C.soft} strokeWidth={1.6} />;
        })}
      </g>
      <line x1={x0} x2={x + w - 24} y1={y + 128} y2={y + 128} stroke={C.cardEdge} strokeWidth={1.2} />
      <g opacity={seg(t, 0, 400) * oOut}>
        <UText x={x0} y={y + 168} s={`🏏 ${b.bat}`.replace("🏏 ", "")} size={28} weight={800} C={C} />
        <UText x={x0 + uWidth(b.bat, 28, 800) + 14} y={y + 166} s={`투수 ${b.pit}`} size={18} weight={650} fill={C.soft} C={C} />
        <g opacity={seg(t, BC.land[0], BC.land[0] + 300)}>
          <UText x={x0} y={y + 206} s={`${b.res}${b.fd ? ` · ${b.fd}` : ""}`} size={24} weight={800} fill={/홈런|안타|루타/.test(b.res) ? C.gold : C.teal} C={C} />
          <Small x={x0} y={y + 234} s={info} size={16} C={C} />
        </g>
      </g>
      <line x1={x0} x2={x + w - 24} y1={y + 254} y2={y + 254} stroke={C.cardEdge} strokeWidth={1.2} />
      <Lines x={x0} y={y + 298} lines={lines} t={t} C={C} size={25} lh={50} maxW={mw} o={oOut} hiSize={33} />
      <Small x={x0} y={y + h - 18} s={`타구 ${idx + 1} / ${total}`} size={15} C={C} />
      <Small x={x + w - 24} y={y + h - 18} s="데이터: MLB Statcast(Baseball Savant)" size={14} C={C} anchor="end" />
    </g>
  );
}

/* ══════════ 액자 ══════════ */
let CACHE = null;
function useBatData() {
  const [d, setD] = useState(CACHE);
  useEffect(() => {
    if (CACHE) return;
    let live = true;
    import("../curio/data-mlb.js").then((m) => { CACHE = m.default; if (live) setD(m.default); }).catch(() => {});
    return () => { live = false; };
  }, []);
  return d;
}

export function BatFnFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, DEF, fixPrm);
  const P = lab.prm;
  const data = useBatData();
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const list = data ? ballsOf(data, P) : [];
  const at = cycleAt(lab.elapsed() * P.sp, BC.D, list.length || 1);
  const jump = (d) => { const k = Math.max(0, at.k + d); lab.jump((k * BC.D) / P.sp); poke(); };
  const stepIn = (d) => { const i = GAMES.indexOf(P.game); const j = clamp(i + d, 0, GAMES.length - 1); if (j !== i) lab.setPrm({ game: GAMES[j] }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: lab.restart, toggleFs, onMode, poke }),
    ArrowRight: () => jump(1), ArrowLeft: () => jump(-1), ArrowUp: () => stepIn(1), ArrowDown: () => stepIn(-1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="경기"><Stepper ui={ui} label="경기" value={P.game} options={GAMES} fmt={(v) => (v < 0 ? "전체" : GAME_SHORT[v])} onChange={(v) => lab.setPrm({ game: v })} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="풀이" sep><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
      <span className="dsp-sep" />
      <ui.Btn title="이전 타구 (←)" onClick={() => jump(-1)}><ui.Ic d="M15 5 8 12l7 7" /></ui.Btn>
      <ui.Btn title="다음 타구 (→)" onClick={() => jump(1)}><ui.Ic d="m9 5 7 7-7 7" /></ui.Btn>
    </>
  );
  const title = { e: "야구로 보는 좌표와 방향", m: "야구로 보는 정비례" };
  const sub = mode === "m" ? "홈 = 원점, 1루선 = x축, 3루선 = y축 — 페어 지역은 제1사분면" : "홈에서 1루 쪽으로 몇 피트, 3루 쪽으로 몇 피트?";
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="야구 타구로 보는 정비례">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={Ly.mode === mode ? sub : ""} C={C} mode={Ly.mode} />
            <BatArt C={C} mode={Ly.mode} P={P} data={data} at={at} ex={P.ex} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={lab.restart}
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings}
        prog={list.length ? (at.i + at.t / BC.D) / list.length : 0} />
    </>
  );
}

/* 목록 그림 — 일반 구장 모양 + 타구 하나 */
const GEN = (() => {
  const fence = [[0, 0]];
  for (let a = 0; a <= 90; a += 3) { const r = 330 + 75 * Math.sin((a * Math.PI) / 90) ** 2; fence.push([r * Math.cos((a * Math.PI) / 180), r * Math.sin((a * Math.PI) / 180)]); }
  const warn = [[0, 0]];
  for (let a = 0; a <= 90; a += 3) { const r = 315 + 75 * Math.sin((a * Math.PI) / 90) ** 2; warn.push([r * Math.cos((a * Math.PI) / 180), r * Math.sin((a * Math.PI) / 180)]); }
  const dirt = [[0, 0], [150, 0]];
  for (let a = 0; a <= 90; a += 6) dirt.push([60 + 95 * Math.cos((a * Math.PI) / 180), 60 + 95 * Math.sin((a * Math.PI) / 180)]);
  dirt.push([0, 150]);
  return { name: "구장", fence, warn, dirt, grass: [[8, 8], [84, 8], [84, 84], [8, 84]] };
})();
const THUMB = {
  parks: { gen: GEN },
  games: [{ date: "2020. 9. 3.", park: "gen", teams: [{ n: "텍사스 레인저스", c: "#2d5bb5", k: "#ffffff" }, { n: "휴스턴 애스트로스", c: "#eb6e1f", k: "#002d62" }],
    balls: [{ i: 8, tb: 0, bat: "추신수", pit: "사이 스니드", ev: "home_run", res: "홈런", bb: "뜬공", U: 230, V: 335, u: 230, v: 335, dist: 422, ls: 104, la: 27, outs: 1, on: [0, 0, 0], pre: [2, 6], post: [3, 6], fd: null, th: null, st: "L" }] }],
};
export const BatFnThumb = memo(function BatFnThumb({ C, mode = "m" }) {
  return <BatArt C={C} mode={mode} P={{ game: -1, sp: 1 }} data={THUMB} at={{ i: 0, k: 0, t: 5200 }} />;
});
