// ashrain.out — 교실 모니터 「액자」: 일차함수 그래프와 넓이 해설 (frames/area.jsx)
// 학원 프린트 「일차함수 그래프와 넓이 · 직선 1개 100제 · 직선 2개 이상 240제」 · 「넓이를 이등분하는 직선의 식 100제」 ·
//   「넓이가 주어질 때 미지수 구하기 100제」(세트 C · D — 1 ~ 5단계)를 문항마다 한 장면으로 끝없이 돌린다.
//   fig.poly2(둘째 직사각형) · fig.edge(도형 테두리 — 꼭짓점으로 준 삼각형 · 두 직사각형)도 그린다.
//   ① 문제 → ② 방침(한 줄) → ③ 풀이를 한 줄씩(지금 줄에 금빛 막대) — 오른쪽 그림이 그 줄대로 움직인다:
//      절편 · 교점은 직선을 따라 미끄러져 와 축(다른 직선)에 닿고, 밑변(금빛) · 높이(빨강)는 한 끝에서 자라고, 치수선은 펴지고,
//      나눈 조각은 칠이 번지며 들어오고, 둘러싼 직사각형 · 이등분하는 직선은 그어진다 → ④ 답. 처음에는 축 → 직선 → 색칠할 곳 차례로 그린다.
// 글자 판은 ../board.js · frames/board.jsx(해설 액자 공통 — 글자 크기 두 벌, 문제는 판 너비를 다 쓴다), 좌표평면은 글자를 다 놓고
//   남은 빈자리에 맞춰 스스로 그린다(AREA_FIG — 글자 크기는 그대로, 화면의 25%까지). 남은 자리가 모자라면 판서만.
// 조작은 해설 액자 공통 틀(frames/lesson.jsx) — 「100제 | 240제」 · 빠르기 0.75× ~ 2× · 번호 · 단계 목록(240제는 1~10단계) · 단일 | 듀얼.
// 계산 · 박자표: ../area.js · 문항: ../area-items.js
import { memo } from "react";
import { MText, Arrow, Path, Draw, mathWidth, SANS, SERIF } from "../draw.jsx";
import { seg, E, clamp } from "../core.js";
import { AREA_SETS, AREA_KEYS, arPlan, lineAt, figPoints, onLine } from "../area.js";
import { stepMarks } from "./scrub.jsx";
import { LessonFrame } from "./lesson.jsx";
import { boardLayout, wrapMath as wrapMath0, STAGE_REGION, PANE_REGION } from "../board.js";
import { Board, FigSlot } from "./board.jsx";

/* ══════════ 배치 (1600×900) — 글자 판은 ../board.js 가 놓는다(문제는 판 너비를 다 쓰고, 좌표평면은 남은 빈자리에) ══════════ */
const FIG = { x0: 884, y0: 166, x1: 1544, y1: 858 };          // 그림의 제 칸(예전 오른쪽 칸) — 시험이 글자 자리를 이 칸으로 본다
export const AREA_BOX = { FIG };
/** 좌표평면은 받은 칸에 맞춰 스스로 그린다(글자 크기는 그대로) — 가장 작게 · 가장 크게 */
export const AREA_FIG = { flex: true, minW: 430, minH: 400, maxW: 700, maxH: 700 };

const fracH = (s) => String(s).includes("{");
/** 수식 글자 줄 바꾸기(../board.js 의 것 — 예전 이름 그대로 내보낸다) */
export const wrapMath = wrapMath0;
/** 글자 판 배치 — region 무대(기본) · 듀얼 반쪽 판. Lo.fig 가 그림(좌표평면) 칸 */
export function layoutOf(it, region = STAGE_REGION) {
  return boardLayout(it, region, AREA_FIG);
}

/* ══════════ 그림: 자리 잡기(문항마다 한 번 — 나중에 나올 글자까지 미리 피해 자리를 잡아 두면 글자가 튀지 않는다) ══════════ */
const dRect = (q, r) => Math.hypot(Math.max(r[0] - q[0], 0, q[0] - r[2]), Math.max(r[1] - q[1], 0, q[1] - r[3]));
const rectDist = (a, b) => Math.hypot(Math.max(b[0] - a[2], 0, a[0] - b[2]), Math.max(b[1] - a[3], 0, a[1] - b[3]));
function dPtSeg(q, a, b) {
  const dx = b[0] - a[0], dy = b[1] - a[1], u = clamp(((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / (dx * dx + dy * dy || 1), 0, 1);
  return Math.hypot(q[0] - a[0] - u * dx, q[1] - a[1] - u * dy);
}
function segHitsRect(a, b, r) {
  let t0 = 0, t1 = 1;
  const dx = b[0] - a[0], dy = b[1] - a[1];
  for (const [p, q] of [[-dx, a[0] - r[0]], [dx, r[2] - a[0]], [-dy, a[1] - r[1]], [dy, r[3] - a[1]]]) {
    if (Math.abs(p) < 1e-12) { if (q < 0) return false; continue; }
    const t = q / p;
    if (p < 0) { if (t > t1) return false; if (t > t0) t0 = t; } else { if (t < t0) return false; if (t < t1) t1 = t; }
  }
  return true;
}
const segRectDist = (a, b, r) => (segHitsRect(a, b, r) ? 0
  : Math.min(dRect(a, r), dRect(b, r), dPtSeg([r[0], r[1]], a, b), dPtSeg([r[2], r[1]], a, b), dPtSeg([r[0], r[3]], a, b), dPtSeg([r[2], r[3]], a, b)));
function inPoly(q, v) {
  let c = false;
  for (let i = 0, j = v.length - 1; i < v.length; j = i++)
    if ((v[i][1] > q[1]) !== (v[j][1] > q[1]) && q[0] < ((v[j][0] - v[i][0]) * (q[1] - v[i][1])) / (v[j][1] - v[i][1]) + v[i][0]) c = !c;
  return c;
}
/** 두 점을 지나는 직선을 [xr]×[yr] 로 자른 두 끝 */
function clipThrough(p, q, xr, yr) {
  const dx = q[0] - p[0], dy = q[1] - p[1];
  let lo = -Infinity, hi = Infinity;
  for (const [d, a, r] of [[dx, p[0], xr], [dy, p[1], yr]]) {
    if (Math.abs(d) < 1e-12) { if (a < r[0] || a > r[1]) return null; continue; }
    const t1 = (r[0] - a) / d, t2 = (r[1] - a) / d;
    lo = Math.max(lo, Math.min(t1, t2)); hi = Math.min(hi, Math.max(t1, t2));
  }
  if (!(hi > lo)) return null;
  return [[p[0] + lo * dx, p[1] + lo * dy], [p[0] + hi * dx, p[1] + hi * dy]];
}
const lineEnds = (L, xr, yr) => (L.t === "lin" ? clipThrough([0, L.b], [1, L.m + L.b], xr, yr)
  : L.t === "vx" ? clipThrough([L.k, 0], [L.k, 1], xr, yr) : clipThrough([0, L.k], [1, L.k], xr, yr));
const same = (p, q) => Math.abs(p[0] - q[0]) < 1e-6 && Math.abs(p[1] - q[1]) < 1e-6;

const LS = { pt: 30, tag: 29, name: 36, ax: 30 };   // 글자 크기(약 1 m 에서 읽히게)
function metrics(s, size, weight) {
  const fr = fracH(s);
  return { w: mathWidth(s, size, weight), up: size * (fr ? 1.02 : 0.8), dn: size * (fr ? 0.52 : 0.24) };
}

const GEO = new WeakMap();
const boxKey = (B) => `${Math.round(B.x0)},${Math.round(B.y0)},${Math.round(B.x1)},${Math.round(B.y1)}`;
export function figGeom(it, box = FIG) {
  let cache = GEO.get(it);
  if (!cache) { cache = new Map(); GEO.set(it, cache); }
  const bk = boxKey(box);
  if (cache.has(bk)) return cache.get(bk);
  const FIG = box;           // 이 칸 안에 — 받은 칸에 맞춰 배율을 정한다
  const f = it.fig;
  const ops = it.lines.flatMap((ln, i) => ln.ops.map((o, j) => ({ ...o, i, j })));
  // 범위: 그림에 나오는 모든 점 + 여백(치수선 · 글자 자리)
  const P0 = figPoints(it);
  let [x0, x1, y0, y1] = [Math.min(...P0.map((p) => p[0])), Math.max(...P0.map((p) => p[0])), Math.min(...P0.map((p) => p[1])), Math.max(...P0.map((p) => p[1]))];
  const padU = 0.7;
  x0 -= padU; x1 += padU; y0 -= padU; y1 += padU;
  const exB = ops.some((o) => o.t === "dim" && o.side === "below") ? 58 : 0;
  const exL = ops.some((o) => o.t === "dim" && o.side === "left") ? 84 : 0;
  const IN = 50;
  const bw = FIG.x1 - FIG.x0 - 2 * IN - exL, bh = FIG.y1 - FIG.y0 - 2 * IN - exB;
  const s = Math.min(bw / (x1 - x0), bh / (y1 - y0), 120);
  const cxp = (FIG.x0 + IN + exL + FIG.x1 - IN) / 2, cyp = (FIG.y0 + IN + FIG.y1 - IN - exB) / 2;
  const mx = (x0 + x1) / 2, my = (y0 + y1) / 2;
  const X = (v) => cxp + s * (v - mx), Y = (v) => cyp - s * (v - my);
  const S = (p) => [X(p[0]), Y(p[1])];
  const ins = 14 / s;
  const xr = [(FIG.x0 - cxp) / s + mx + ins, (FIG.x1 - cxp) / s + mx - ins];
  const yr = [(cyp - FIG.y1) / s + my + ins, (cyp - FIG.y0) / s + my - ins];
  const polyS = f.poly.map(S), poly2S = f.poly2 ? f.poly2.map(S) : null;
  const cen = polyS.reduce((a, p) => [a[0] + p[0] / polyS.length, a[1] + p[1] / polyS.length], [0, 0]);

  // 선(장애물): 축 · 직선 · 본디 직선 · 그림 연산의 선분
  const lines = f.lines.map((L) => { const e = lineEnds(L, xr, yr); return { L, ends: e && e.map(S) }; });
  const axX = [S([xr[0], 0]), S([xr[1], 0])], axY = [S([0, yr[0]]), S([0, yr[1]])];
  const ghost = f.ghost ? lineEnds({ t: "lin", m: f.ghost.m, b: f.ghost.b }, xr, yr)?.map(S) : null;
  const segs = [axX, axY, ...lines.filter((l) => l.ends).map((l) => l.ends)];
  if (ghost) segs.push(ghost);
  // 치수선 자리
  const polyMaxY = Math.max(...polyS.map((p) => p[1])), polyMinX = Math.min(...polyS.map((p) => p[0]));
  const G = { ops: [], dots: [], base: [], names: [] };
  for (const o of ops) {
    const g = { o };
    if (o.t === "seg" || o.t === "ext") { g.a = S(o.a); g.b = S(o.b); segs.push([g.a, g.b]); }
    if (o.t === "arrow") {
      let a = S(o.a), b = S(o.b);
      if (Math.abs(o.a[0]) < 1e-9 && Math.abs(o.b[0]) < 1e-9) { const sh = cen[0] > X(0) ? -18 : 18; a = [a[0] + sh, a[1]]; b = [b[0] + sh, b[1]]; }
      g.a = a; g.b = b; segs.push([a, b]);
    }
    if (o.t === "dim") {
      if (o.side === "below") {
        const y = polyMaxY + 40;
        g.a = [X(o.a), y]; g.b = [X(o.b), y];
        g.ext = [o.a, o.b].map((v) => {
          const on = f.poly.filter((p) => Math.abs(p[0] - v) < 1e-9);
          return on.length ? [S(on.reduce((m, p) => (p[1] < m[1] ? p : m)))[0], S(on.reduce((m, p) => (p[1] < m[1] ? p : m)))[1], X(v), y] : null;
        });
      } else {
        const x = polyMinX - 40;
        g.a = [x, Y(o.a)]; g.b = [x, Y(o.b)];
        g.ext = [o.a, o.b].map((v) => {
          const on = f.poly.filter((p) => Math.abs(p[1] - v) < 1e-9);
          return on.length ? [S(on.reduce((m, p) => (p[0] < m[0] ? p : m)))[0], Y(v), x, Y(v)] : null;
        });
      }
      segs.push([g.a, g.b]);
    }
    if (o.t === "box") { g.pts = o.pts.map(S); for (let k = 0; k < 4; k++) segs.push([g.pts[k], g.pts[(k + 1) % 4]]); }
    if (o.t === "poly") g.pts = o.pts.map(S);
    if (o.t === "pt" || o.t === "pulse") g.p = S(o.p);
    G.ops.push(g);
  }
  // 점 찾아가기(직선을 따라 미끄러져 오는 길)
  G.cen = cen;
  G.lines = lines;
  G.trav = new Map();
  for (const g of G.ops) if (g.o.t === "pt") G.trav.set(g, travelers(it, G, { m: g.o.p, s: g.p }));
  // 점
  const dots = [];
  for (const p of f.pts) dots.push(S(p.p));
  for (const g of G.ops) if (g.o.t === "pt") dots.push(g.p);

  // 이미 차지한 자리: 축 글자 · O · 치수선 글자
  const placed = [];
  const tipX = S([xr[1], 0]), tipY = S([0, yr[1]]);
  G.axTxt = { x: [tipX[0] - 8, tipX[1] + 40], y: [tipY[0] + 16, tipY[1] + 24], O: [X(0) - 12, Y(0) + 32] };
  placed.push([tipX[0] - 14, tipX[1] + 14, tipX[0] + 14, tipX[1] + 46], [tipY[0] + 8, tipY[1] - 4, tipY[0] + 36, tipY[1] + 30], [X(0) - 36, Y(0) + 8, X(0) - 6, Y(0) + 38]);
  for (const g of G.ops) if (g.o.t === "dim" && g.o.s) {
    const m = metrics(g.o.s, LS.tag, 700);
    if (g.o.side === "below") { const cx = (g.a[0] + g.b[0]) / 2; g.tag = { x: cx - m.w / 2, y: g.a[1] + 12 + m.up }; }
    else { const cy = (g.a[1] + g.b[1]) / 2; g.tag = { x: g.a[0] - 12 - m.w, y: cy + (m.up - m.dn) / 2 }; }
    placed.push([g.tag.x - 2, g.tag.y - m.up, g.tag.x + m.w + 2, g.tag.y + m.dn]);
  }

  const score = (box, own, inPen) => {
    if (box[0] < FIG.x0 + 4 || box[2] > FIG.x1 - 4 || box[1] < FIG.y0 + 4 || box[3] > FIG.y1 - 4) return -1e9;
    let sc = 40;
    for (const r of placed) sc = Math.min(sc, rectDist(box, r) - 8);
    for (const d of dots) if (!own || d !== own) sc = Math.min(sc, dRect(d, box) - 12);
    for (const [a, b] of segs) sc = Math.min(sc, segRectDist(a, b, box) - 5);
    if (inPen && inPoly([(box[0] + box[2]) / 2, (box[1] + box[3]) / 2], polyS)) sc -= inPen;
    return sc;
  };
  const pick = (cands, own, inPen) => {
    let best = null;
    for (const c of cands) { const sc = score(c.box, own, inPen) + (c.pref || 0); if (!best || sc > best.sc + 0.01) best = { ...c, sc }; }
    placed.push(best.box);
    return best;
  };
  const at = (x, base, m) => ({ box: [x, base - m.up, x + m.w, base + m.dn], x, y: base });
  const ptCands = (p, m) => {
    const out = [];
    const ox = p[0] - cen[0], oy = p[1] - cen[1], ol = Math.hypot(ox, oy) || 1;
    for (const g of [11, 26, 46]) for (const [dx, dy] of [[1, -1], [-1, -1], [1, 1], [-1, 1], [0, -1], [0, 1], [1, 0], [-1, 0]]) {
      const x = dx > 0 ? p[0] + g : dx < 0 ? p[0] - g - m.w : p[0] - m.w / 2;
      const base = dy < 0 ? p[1] - g * 0.6 - m.dn : dy > 0 ? p[1] + g * 0.6 + m.up : p[1] + (m.up - m.dn) / 2;
      const dl = Math.hypot(dx, dy);
      out.push({ ...at(x, base, m), dir: [dx, dy], pref: (6 * (dx * ox + dy * oy)) / (dl * ol) - (g > 26 ? 9 : g > 11 ? 4 : 0) });
    }
    return out;
  };
  const axCands = (p, m, pos) => {
    const out = [];
    if (pos === "x") {
      for (const sh of [0, -1, 1]) {
        const x = p[0] - m.w / 2 + sh * (m.w / 2 + 10);
        out.push({ ...at(x, p[1] + 10 + m.up, m), pref: (cen[1] > p[1] ? -3 : 3) - Math.abs(sh) * 3 });
        out.push({ ...at(x, p[1] - 10 - m.dn, m), pref: (cen[1] > p[1] ? 3 : -3) - Math.abs(sh) * 3 });
      }
    } else {
      for (const sh of [0, -1, 1]) {
        const base = p[1] + (m.up - m.dn) / 2 + sh * ((m.up + m.dn) / 2 + 8);
        out.push({ ...at(p[0] - 12 - m.w, base, m), pref: (cen[0] > p[0] ? 3 : -3) - Math.abs(sh) * 3 });
        out.push({ ...at(p[0] + 12, base, m), pref: (cen[0] > p[0] ? -3 : 3) - Math.abs(sh) * 3 });
      }
    }
    return out;
  };

  // ① 처음부터 찍힌 점(나중에 좌표가 붙는 점은 그 좌표 글자 자리를 따른다)
  const ptOps = G.ops.filter((g) => g.o.t === "pt");
  f.pts.forEach((q, k) => {
    const p = S(q.p);
    const rep = ptOps.find((g) => same(g.o.p, q.p));
    G.base.push({ p, s: q.s, rep: rep ? rep.o.i : null, m: metrics(q.s, LS.pt, 650) });
  });
  for (const b of G.base) if (b.rep == null) Object.assign(b, pick(ptCands(b.p, b.m), b.p, 12));
  // ② 풀이 줄의 점
  for (const g of ptOps) {
    const m = metrics(g.o.s, g.o.pos === "free" ? LS.pt : LS.ax, 650);
    g.m = m;
    Object.assign(g, pick(g.o.pos === "free" ? ptCands(g.p, m) : axCands(g.p, m, g.o.pos), g.p, g.o.pos === "free" ? 12 : 4));
    const b = G.base.find((x) => x.rep != null && same(x.p, g.p));
    if (b) {   // 처음 이름(P · A …)은 좌표 글자의 머리 자리에
      const left = g.box[2] < g.p[0] + 1 && g.box[0] < g.p[0] - 1 && g.dir?.[0] < 0;
      b.x = left ? g.box[2] - b.m.w : g.x; b.y = g.y;
    }
  }
  // ③ 선분 이름표(밑변 · 높이 …)
  for (const g of G.ops) if (g.o.t === "seg" && g.o.s) {
    const m = metrics(g.o.s, LS.tag, 700);
    const dx = g.b[0] - g.a[0], dy = g.b[1] - g.a[1], len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len;
    const ext = Math.abs(nx) * m.w / 2 + Math.abs(ny) * (m.up + m.dn) / 2 + 9;
    const cands = [];
    for (const fr of [0.5, 0.36, 0.64, 0.22, 0.78]) for (const sg of [1, -1]) {
      const cx = g.a[0] + fr * dx + sg * nx * ext, cy = g.a[1] + fr * dy + sg * ny * ext;
      cands.push({ ...at(cx - m.w / 2, cy + (m.up - m.dn) / 2, m), pref: -Math.abs(fr - 0.5) * 6 });
    }
    g.m = m;
    Object.assign(g, pick(cands, null, 6));
  }
  // ④ 직선 이름(ℓ, m, x = k …): 선을 따라 몇 군데 · 양옆을 놓아 보고 가장 넉넉한 자리로
  lines.forEach((l, k) => {
    if (!l.ends || !l.L.name) return;
    const m = metrics(l.L.name, LS.name, 600);
    const [a, b] = l.ends;
    const dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len;
    const ext = Math.abs(nx) * m.w / 2 + Math.abs(ny) * (m.up + m.dn) / 2 + 10;
    const cands = [];
    for (let fr = 0.05; fr <= 0.951; fr += 0.05) for (const sg of [1, -1]) {
      const cx = a[0] + fr * dx + sg * nx * ext, cy = a[1] + fr * dy + sg * ny * ext;
      cands.push({ ...at(cx - m.w / 2, cy + (m.up - m.dn) / 2, m), pref: Math.min(Math.hypot(cx - cen[0], cy - cen[1]) / 40, 4) });
    }
    G.names[k] = { m, ...pick(cands, null, 20) };
  });
  Object.assign(G, { s, X, Y, S, xr, yr, lines, ghost, axX, axY, polyS, poly2S, cen, box });
  cache.set(bk, G);
  return G;
}

/* ══════════ 그림 ══════════ */
const COL = { gold: "gold", red: "red", coral: "coral", teal: "teal" };
/** 화면 위 선분 p → q 를 k 만큼(0 ~ 1) */
const part2 = (p, q, k) => [p, [p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k]];
/**
 * 점 찾아가기 — 그 점을 지나는 직선마다, 그림 안쪽에서 출발한 작은 점이 직선을 따라 미끄러져 와 그 자리에 닿는다
 * (절편이면 축에 닿는 순간, 교점이면 두 점이 만나는 순간). 직선 위 점이 아니면 그냥 톡.
 */
function travelers(it, G, p) {
  const f = it.fig, out = [];
  for (let k = 0; k < f.lines.length; k++) {
    const L = f.lines[k];
    const e = G.lines[k]?.ends;
    if (!e || !onLine(L, p.m, 1e-6)) continue;
    // 직선 방향(화면) — 그림 가운데 쪽에서 출발
    const d = [e[1][0] - e[0][0], e[1][1] - e[0][1]], dl = Math.hypot(d[0], d[1]) || 1, u = [d[0] / dl, d[1] / dl];
    const toC = [G.cen[0] - p.s[0], G.cen[1] - p.s[1]];
    const sg = toC[0] * u[0] + toC[1] * u[1] >= 0 ? 1 : -1;
    const run = Math.min(170, Math.max(70, Math.hypot(toC[0], toC[1]) * 0.8));
    out.push({ from: [p.s[0] + u[0] * run * sg, p.s[1] + u[1] * run * sg], to: p.s });
  }
  return out;
}
function Figure({ it, t, cur, C, box = FIG }) {
  const G = figGeom(it, box), P = arPlan(it);
  const o0 = seg(t, 120, 520, E.sine);
  // 그 줄이 시작된 뒤 그림이 따라 나오는 정도(그어지고 · 자라고 · 칠해지는 데 쓰는 0 ~ 1)
  const prog = (i, d = 620, lag = 150) => (t < P.lines[i].a + lag ? 0 : seg(t, P.lines[i].a + lag, P.lines[i].a + lag + d, E.io));
  const vis = (i) => prog(i, 420);
  const isCur = (i) => cur === i;
  const done = t >= P.ans;
  const emph = (i) => (isCur(i) ? 1 : 0.72);
  const revealAt = G.ops.find((g) => g.o.t === "reveal");
  const rv = revealAt ? prog(revealAt.o.i, 800) : 0;
  const fullG = G.ops.find((g) => g.o.t === "full");
  const fv = fullG ? prog(fullG.o.i, 900) : 0;
  const pulse = (i) => (isCur(i) ? ((t - P.lines[i].a) % 1100) / 1100 : -1);
  const lbl = (x, y, s, size, fill, weight = 650, op = 1) => <MText x={x} y={y} s={s} size={size} weight={weight} fill={fill} halo={C.halo} opacity={op} C={C} />;
  // 처음 그리기: 축 → 직선(그어짐) → 색칠할 곳
  const axK = seg(t, 120, 700, E.io), lnK = (k) => seg(t, 500 + k * 260, 1200 + k * 260, E.io);
  const regK = seg(t, 1100 + G.lines.length * 260, 1700 + G.lines.length * 260, E.sine);
  const els = [];
  // 나눈 조각 · 둘러싼 직사각형(밑에) — 조각은 칠이 번지듯 들어오며 살짝 커졌다 제자리, 직사각형은 한 바퀴 그어진다
  for (const g of G.ops) {
    const v = vis(g.o.i);
    if (!v) continue;
    if (g.o.t === "poly") {
      const k = prog(g.o.i, 700), cx = g.pts.reduce((a, q) => a + q[0], 0) / g.pts.length, cy = g.pts.reduce((a, q) => a + q[1], 0) / g.pts.length;
      const sc = 1 + 0.06 * Math.sin(Math.PI * k);
      els.push(<g key={`p${g.o.i}-${g.o.j}`} transform={`translate(${cx} ${cy}) scale(${sc.toFixed(3)}) translate(${-cx} ${-cy})`}>
        <Path pts={g.pts} closed fill={C[COL[g.o.c]]} fo={0.42 * emph(g.o.i) * k} stroke="none" />
        <Draw pts={g.pts} p={k} closed stroke={C[COL[g.o.c]]} sw={2.5} />
      </g>);
    }
    if (g.o.t === "box") els.push(<Draw key={`b${g.o.i}`} pts={g.pts} p={prog(g.o.i, 900)} closed stroke={C.teal} sw={3.5} dash="12 9" />);
  }
  const over = [];
  for (const g of G.ops) {
    const v = vis(g.o.i), k = `o${g.o.i}-${g.o.j}`;
    if (!v) continue;
    const o = g.o;
    if (o.t === "seg") {
      // 밑변 · 높이는 한 끝에서 다른 끝으로 자란다
      const c = C[COL[o.c]], gk = prog(o.i, 650);
      const pp = part2(g.a, g.b, gk);
      if (o.c === "gold") {
        if (isCur(o.i)) over.push(<Path key={k + "g"} pts={pp} stroke={c} sw={18} o={0.25} />);
        over.push(<Path key={k} pts={pp} stroke={c} sw={9} o={0.86} dash={o.dash ? "14 10" : undefined} />);
      } else over.push(<Path key={k} pts={pp} stroke={c} sw={isCur(o.i) ? 5.5 : 4.5} dash={o.dash ? "12 9" : undefined} />);
      if (gk > 0 && gk < 1) over.push(<circle key={k + "tip"} cx={pp[1][0]} cy={pp[1][1]} r={6} fill={c} />);
    }
    if (o.t === "ext") over.push(<Path key={k} pts={part2(g.a, g.b, prog(o.i, 500))} stroke={C.soft} sw={2.5} dash="6 8" />);
    if (o.t === "arrow") { const ak = prog(o.i, 600); if (ak > 0.05) over.push(<Arrow key={k} p={g.a} q={part2(g.a, g.b, ak)[1]} stroke={C.red} sw={4} h={16} />); }
    if (o.t === "dim") {
      // 치수선 — 가운데에서 양쪽으로 펴지고, 끝 눈금이 톡
      const dk = prog(o.i, 600), mid = [(g.a[0] + g.b[0]) / 2, (g.a[1] + g.b[1]) / 2];
      const a2 = [mid[0] + (g.a[0] - mid[0]) * dk, mid[1] + (g.a[1] - mid[1]) * dk], b2 = [mid[0] + (g.b[0] - mid[0]) * dk, mid[1] + (g.b[1] - mid[1]) * dk];
      const tk = o.side === "below" ? [[0, -9], [0, 9]] : [[-9, 0], [9, 0]];
      over.push(<g key={k}>
        {g.ext.map((e, q) => e && <line key={q} x1={e[0]} y1={e[1]} x2={e[0] + (e[2] - e[0]) * dk} y2={e[1] + (e[3] - e[1]) * dk} stroke={C.soft} strokeWidth={2} strokeDasharray="5 7" />)}
        <Path pts={[a2, b2]} stroke={C.red} sw={3.5} />
        {dk >= 1 && [g.a, g.b].map((p, q) => <line key={"t" + q} x1={p[0] + tk[0][0]} y1={p[1] + tk[0][1]} x2={p[0] + tk[1][0]} y2={p[1] + tk[1][1]} stroke={C.red} strokeWidth={3.5} strokeLinecap="round" />)}
      </g>);
    }
  }
  const dots = [];
  const labels = [];
  for (const b of G.base) {
    const rg = b.rep != null ? vis(b.rep) : 0;
    dots.push(<circle key={`bd${b.s}${b.p[0]}`} cx={b.p[0]} cy={b.p[1]} r={7 * (0.3 + 0.7 * Math.max(0, E.back(regK)))} fill={C.ink} opacity={o0} />);
    if (b.x != null) labels.push(<g key={`bl${b.s}${b.p[0]}`}>{lbl(b.x, b.y, b.s, LS.pt, C.ink, 650, regK * (1 - rg))}</g>);
  }
  const trails = [];
  for (const g of G.ops) {
    const v = vis(g.o.i), o = g.o, k = `l${o.i}-${o.j}`;
    if (!v) continue;
    if (o.t === "pt") {
      // 직선을 따라 미끄러져 와 닿는다 → 닿으면 점과 좌표가 톡
      const tr = G.trav.get(g) || [];
      const mk = prog(o.i, 760, 120), land = tr.length ? seg(mk, 0.85, 1, E.lin) : 1;
      tr.forEach((r, q) => {
        if (mk >= 1) return;
        const cur2 = [r.from[0] + (r.to[0] - r.from[0]) * mk, r.from[1] + (r.to[1] - r.from[1]) * mk];
        trails.push(<g key={`${k}t${q}`}>
          <Path pts={[r.from, cur2]} stroke={C.gold} sw={7} o={0.35} />
          <circle cx={cur2[0]} cy={cur2[1]} r={9} fill={C.gold} />
        </g>);
      });
      if (land > 0) {
        const r = 7 * (tr.length ? 0.4 + 0.6 * Math.max(0, E.back(land)) : 1);
        dots.push(<circle key={k} cx={g.p[0]} cy={g.p[1]} r={r} fill={C.ink} />);
        labels.push(<g key={k}>{lbl(g.x, g.y, o.s, o.pos === "free" ? LS.pt : LS.ax, isCur(o.i) ? C.gold : C.ink, 680, Math.min(1, land * 1.5))}</g>);
      }
    }
    if (o.t === "seg" && o.s) labels.push(<g key={k}>{lbl(g.x, g.y, o.s, LS.tag, C[COL[o.c]], 750, seg(prog(o.i, 650), 0.7, 1, E.lin))}</g>);
    if (o.t === "dim" && o.s) labels.push(<g key={k}>{lbl(g.tag.x, g.tag.y, o.s, LS.tag, C.red, 750, seg(prog(o.i, 600), 0.75, 1, E.lin))}</g>);
  }
  const rings = [];
  for (const g of G.ops) {
    const o = g.o;
    if (o.t !== "pulse" && o.t !== "pt") continue;
    const ph = pulse(o.i);
    const landAt = P.lines[o.i].a + 120 + (o.t === "pt" && (G.trav.get(g) || []).length ? 760 : 0);
    if (ph < 0 || t < landAt || (o.t === "pt" && t > landAt + 1300)) continue;
    rings.push(<circle key={`r${o.i}-${o.j}`} cx={g.p[0]} cy={g.p[1]} r={10 + 22 * ph} fill="none" stroke={C.gold} strokeWidth={4} opacity={(1 - ph) * 0.9} />);
    if (o.t === "pulse") rings.push(<circle key={`rc${o.i}-${o.j}`} cx={g.p[0]} cy={g.p[1]} r={9} fill={C.gold} opacity={vis(o.i)} />);
  }
  const fullOn = fv > 0;
  const fg = fullG && (isCur(fullG.o.i) || done) ? (isCur(fullG.o.i) ? 0.5 + 0.5 * Math.sin(((t - P.lines[fullG.o.i].a) / 900) * Math.PI) ** 2 : 0.4) : 0;
  const tip = G.axTxt;
  const ax = (A) => [A[0], [A[0][0] + (A[1][0] - A[0][0]) * axK, A[0][1] + (A[1][1] - A[0][1]) * axK]];
  return (
    <g opacity={o0}>
      <Path pts={G.polyS} closed fill={C.gold} fo={(fullOn ? 0.22 + 0.16 * fv : 0.22) * regK} stroke="none" />
      {G.poly2S && <Path pts={G.poly2S} closed fill={C.gold} fo={0.22 * regK} stroke="none" />}
      {it.fig.edge && <Path pts={G.polyS} closed stroke={C.ink} sw={3} o={0.75 * regK} />}
      {it.fig.edge && G.poly2S && <Path pts={G.poly2S} closed stroke={C.ink} sw={3} o={0.75 * regK} />}
      {els}
      {axK > 0.05 && <Arrow p={ax(G.axX)[0]} q={ax(G.axX)[1]} stroke={C.ink} sw={3} h={18} />}
      {axK > 0.05 && <Arrow p={ax(G.axY)[0]} q={ax(G.axY)[1]} stroke={C.ink} sw={3} h={18} />}
      <g opacity={axK}>
        <text x={tip.x[0]} y={tip.x[1]} fontFamily={SERIF} fontStyle="italic" fontSize={34} fill={C.ink}>x</text>
        <text x={tip.y[0]} y={tip.y[1]} fontFamily={SERIF} fontStyle="italic" fontSize={34} fill={C.ink}>y</text>
        <text x={tip.O[0]} y={tip.O[1]} fontFamily={SERIF} fontStyle="italic" fontSize={28} fill={C.soft} textAnchor="end">O</text>
      </g>
      {G.ghost && (() => {
        const g = G.ops.find((x) => x.o.t === "ghost");
        const v = g ? prog(g.o.i, 800) : 0;
        return v > 0 && <Draw pts={G.ghost} p={v} stroke={C.soft} sw={3.5} dash="10 10" o={0.85} />;
      })()}
      {G.lines.map((l, k) => l.ends && (!l.L.dash || rv > 0) && (
        <Draw key={k} pts={l.ends} p={l.L.dash ? rv : lnK(k)} stroke={l.L.dash ? C.lilac : C.sky} sw={l.L.dash ? 5 : 4.5} dash={l.L.dash ? "16 11" : undefined} />
      ))}
      {fullOn && <Draw pts={G.polyS} p={fv} closed stroke={C.gold} sw={5} />}
      {fg > 0 && <Path pts={G.polyS} closed stroke={C.gold} sw={16} o={0.28 * fg} />}
      {over}
      {trails}
      {dots}
      {G.lines.map((l, k) => G.names[k] && (!l.L.dash || rv > 0) && (
        <g key={"n" + k}>{lbl(G.names[k].x, G.names[k].y, l.L.name, LS.name, l.L.dash ? C.lilac : C.sky, 600, l.L.dash ? rv : seg(lnK(k), 0.8, 1, E.lin))}</g>
      ))}
      {labels}
      {rings}
    </g>
  );
}

/* ══════════ 한 문항 한 순간 ══════════ */
/** region — 무대 전체(기본) · 듀얼 반쪽 판. 글자 판은 Board(frames/board.jsx), 좌표평면은 글자를 다 놓고 남은 칸에 */
export function AreaArt({ it, t, C, region = STAGE_REGION, uid = "" }) {
  const P = arPlan(it), Lo = layoutOf(it, region);
  const cur = lineAt(P, t);
  return (
    <g>
      <Board it={it} Lo={Lo} P={P} t={t} cur={cur} C={C} uid={`ar${uid}`} />
      <FigSlot spot={Lo.fig} flex draw={(box) => <Figure it={it} t={t} cur={cur} C={C} box={box} />} />
    </g>
  );
}

/* ══════════ 장면 목록 (StoryPlayer 형식) ══════════ */
const SCENES = new Map();
export function areaScenes(setKey, sp = 1, lv = 0) {
  const k = `${setKey}|${sp}|${lv}`;
  if (SCENES.has(k)) return SCENES.get(k);
  const S = AREA_SETS[setKey];
  const list = S.items.filter((it) => !lv || it.lv === lv).map((it) => {
    const title = `일차함수 그래프와 넓이 · ${S.name}`;
    const sub = it.lv ? `${it.lv}단계 ${S.stage[it.lv]} · ${it.no}번` : `${it.no}번 · ${it.sub}`;
    return {
      key: `area-${setKey}-${it.no}`, no: it.no, lv: it.lv || 0, st: it.lv || 0, sub0: it.sub, dur: Math.round(arPlan(it).dur / sp),
      grp: it.lv ? `${it.lv}단계` : null, marks: stepMarks(arPlan(it), it.lines, sp), card: `${it.lv ? `${it.lv}단계 · ` : ""}${it.sub}`,
      title: { e: title, m: title }, sub: { e: sub, m: sub }, tsz: "lesson",
      render: (mode, t, C) => <AreaArt it={it} t={t * sp} C={C} />,
      pane: (t, C, uid) => <AreaArt it={it} t={t * sp} C={C} uid={uid} region={PANE_REGION} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 — 조작은 해설 액자 공통 틀(frames/lesson.jsx) ══════════ */
export const AREA_SPEC = {
  lsk: "ash.display.area", title: "일차함수 그래프와 넓이 해설", defSet: "A", cols: 5,
  sets: AREA_KEYS.map((k) => ({ key: k, name: AREA_SETS[k].name, short: AREA_SETS[k].short })),
  stages: (set) => { const st = AREA_SETS[set]?.stage; return st ? Object.keys(st).map(Number).map((v) => ({ v, lab: `${v}단계 ${st[v]}`, chip: `${v}단계` })) : []; },
  scenes: (set, sp, st) => areaScenes(set, sp, AREA_SETS[set]?.stage ? st : 0),
};
export function AreaFrame(props) {
  return <LessonFrame spec={AREA_SPEC} {...props} />;
}

/** 액자 목록의 작은 그림 — 240제 7단계(사각형 OAPB) 첫 문항을 다 푼 순간 */
export const AreaThumb = memo(function AreaThumb({ C }) {
  const it = AREA_SETS.B.items.find((x) => x.kind === "OAPB");
  return <AreaArt it={it} t={arPlan(it).ans + 900} C={C} />;
});
