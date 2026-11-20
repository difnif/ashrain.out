// ashrain.out — 교실 모니터 「액자」: 일차함수 그래프와 넓이 해설 (frames/area.jsx)
// 학원 프린트 「일차함수 그래프와 넓이 · 직선 1개 100제 · 직선 2개 이상 240제」를 문항마다 한 장면으로 끝없이 돌린다.
//   ① 문제 → ② 방침(한 줄) → ③ 풀이를 한 줄씩(지금 줄에 금빛 막대) — 오른쪽 그림에 그 줄의 것이 같이 나타난다:
//      절편 · 교점 · 꼭짓점 좌표, 밑변(금빛) · 높이(빨강), 나눈 조각 · 둘러싼 직사각형, 이등분하는 직선 → ④ 답
// 재생기는 장면 묶음과 같은 StoryPlayer. 이 액자만의 것: 「100제 | 240제」 · 「1× | 1.5×」 · 번호 목록(L) — 240제는 목록 위
//   단계 칩(전체 · 1~10)으로 고르면 그 단계 24문항만 돈다.
// 계산 · 박자표: ../area.js · 문항: ../area-items.js
import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { MText, Arrow, Path, mathWidth, SANS, SERIF } from "../draw.jsx";
import { seg, E, clamp } from "../core.js";
import { AREA_SETS, AREA_SPEEDS, AREA_LEVEL, arPlan, lineAt, figPoints } from "../area.js";
import { StoryPlayer } from "./player.jsx";
import { stepMarks } from "./scrub.jsx";
import { Seg, useKeys, lsRead, lsWrite } from "./xkit.jsx";

/* ══════════ 배치 (1600×900) ══════════ */
const LEFT = 60, TOP = 168, BOTTOM = 866, RIGHT = 836;
const FIG = { x0: 884, y0: 166, x1: 1544, y1: 858 };
export const AREA_BOX = { LEFT, TOP, BOTTOM, RIGHT, FIG };

const HANGUL = /[\uac00-\ud7a3]/;
const openParen = (a) => (a.match(/\(/g) || []).length > (a.match(/\)/g) || []).length;
/** 줄을 크게 나눌 자리 — 「→」 앞 · 괄호 밖 쉼표 뒤 */
const strongBreak = (a, b) => b.startsWith("→") || (a.endsWith(",") && !openParen(a));
/** 띄어쓰기 자리 중 줄을 바꿔도 되는 곳 — 식 가운데(= + − × 옆) · 좌표 가운데는 안 되고, 큰 자리 · 한글 낱말 사이만 */
function canBreak(a, b) {
  if (strongBreak(a, b)) return true;
  if (a.endsWith(":") && HANGUL.test(a)) return true;
  return HANGUL.test(a) && HANGUL.test(b) && !/[=+−×]$/.test(a) && !/^[=+−×]/.test(b) && !openParen(a);
}
function chunksOf(words, test) {
  const out = [];
  let cur = [];
  words.forEach((w, i) => { cur.push(w); if (i === words.length - 1 || test(w, words[i + 1])) { out.push(cur.join(" ")); cur = []; } });
  return out;
}
/** 수식 글자 줄 바꾸기. strong — 풀이 줄: 「→」 앞 · 쉼표 뒤에서 먼저 나눠 본다 */
export function wrapMath(s, size, maxW, weight = 560, strong = false) {
  const fits = (x) => mathWidth(x, size, weight) <= maxW;
  const lines = [];
  const add = (ch) => {
    const n = lines.length;
    if (n && fits(lines[n - 1] + " " + ch)) { lines[n - 1] += " " + ch; return; }
    if (fits(ch)) { lines.push(ch); return; }
    for (const w of ch.split(" ")) {
      const m = lines.length;
      if (m && fits(lines[m - 1] + " " + w)) lines[m - 1] += " " + w; else lines.push(w);
    }
  };
  const words = String(s).split(" ");
  for (const B of strong ? chunksOf(words, strongBreak) : [String(s)]) {
    const n = lines.length;
    if (strong && n && fits(lines[n - 1] + " " + B)) { lines[n - 1] += " " + B; continue; }
    if (strong && fits(B)) { lines.push(B); continue; }
    for (const ch of chunksOf(B.split(" "), canBreak)) add(ch);
  }
  return lines.length ? lines : [""];
}

const LAYOUT = new WeakMap();
const fracH = (s) => String(s).includes("{");
export function layoutOf(it) {
  if (LAYOUT.has(it)) return LAYOUT.get(it);
  const W0 = RIGHT - LEFT;
  let best = null;
  for (const [qs, bs] of [[36, 40], [34, 38], [32, 35], [30, 32], [28, 30], [26, 28]]) {
    const qLines = wrapMath(`${it.no}. ${it.q}`, qs, W0, 560);
    let y = TOP + qs;
    const qY = [];
    qLines.forEach((s, i) => { if (i) y += qs * (fracH(s) || fracH(qLines[i - 1]) ? 1.66 : 1.42); qY.push(y); });
    y += qs * 1.55;
    const ps = Math.round(bs * 0.66);
    const planY = y;
    let ok = ps * 3.4 + mathWidth(it.plan, Math.round(ps * 1.12), 600) <= W0;
    y += bs * 1.45;
    const rows = [];
    it.lines.forEach((ln) => {
      const parts = wrapMath(ln.s, bs, W0 - 10, 560, true);
      if (parts.some((p) => mathWidth(p, bs, 560) > W0 - 4)) ok = false;
      const ys = [];
      parts.forEach((p, i) => {
        y += i === 0 ? (fracH(p) ? bs * 0.34 : 0) : bs * (fracH(p) || fracH(parts[i - 1]) ? 1.6 : 1.32);
        ys.push(y + bs * 0.35);
      });
      const top = ys[0] - bs * (fracH(parts[0]) ? 1.12 : 0.92);
      const bot = ys[ys.length - 1] + bs * (fracH(parts[parts.length - 1]) ? 0.56 : 0.3);
      rows.push({ parts, ys, top, bot });
      y = bot + bs * 0.62;
    });
    const ansY = y + bs * 0.62;
    best = { qs, bs, ps, qLines, qY, planY, rows, ansY };
    if (ok && ansY + bs * 0.8 <= BOTTOM) break;
  }
  LAYOUT.set(it, best);
  return best;
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

const LS = { pt: 28, tag: 27, name: 34, ax: 28 };   // 글자 크기
function metrics(s, size, weight) {
  const fr = fracH(s);
  return { w: mathWidth(s, size, weight), up: size * (fr ? 1.02 : 0.8), dn: size * (fr ? 0.52 : 0.24) };
}

const GEO = new WeakMap();
export function figGeom(it) {
  if (GEO.has(it)) return GEO.get(it);
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
  const polyS = f.poly.map(S);
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
  Object.assign(G, { s, X, Y, S, xr, yr, lines, ghost, axX, axY, polyS, cen });
  GEO.set(it, G);
  return G;
}

/* ══════════ 그림 ══════════ */
const COL = { gold: "gold", red: "red", coral: "coral", teal: "teal" };
function Figure({ it, t, cur, C }) {
  const G = figGeom(it), P = arPlan(it);
  const o0 = seg(t, 300, 1100, E.sine);
  const vis = (i) => (t < P.lines[i].a + 150 ? 0 : seg(t, P.lines[i].a + 150, P.lines[i].a + 700, E.sine));
  const isCur = (i) => cur === i;
  const done = t >= P.ans;
  const emph = (i) => (isCur(i) ? 1 : 0.72);
  const revealAt = G.ops.find((g) => g.o.t === "reveal");
  const rv = revealAt ? vis(revealAt.o.i) : 0;
  const fullG = G.ops.find((g) => g.o.t === "full");
  const fv = fullG ? vis(fullG.o.i) : 0;
  const pulse = (i) => (isCur(i) ? ((t - P.lines[i].a) % 1100) / 1100 : -1);
  const lbl = (x, y, s, size, fill, weight = 650, op = 1) => <MText x={x} y={y} s={s} size={size} weight={weight} fill={fill} halo={C.halo} opacity={op} C={C} />;
  const els = [];
  // 나눈 조각 · 둘러싼 직사각형(밑에)
  for (const g of G.ops) {
    const v = vis(g.o.i);
    if (!v) continue;
    if (g.o.t === "poly") els.push(<Path key={`p${g.o.i}-${g.o.j}`} pts={g.pts} closed fill={C[COL[g.o.c]]} fo={0.42 * emph(g.o.i)} stroke={C[COL[g.o.c]]} sw={2.5} o={v} />);
    if (g.o.t === "box") els.push(<Path key={`b${g.o.i}`} pts={g.pts} closed stroke={C.teal} sw={3.5} dash="12 9" o={v} />);
  }
  const over = [];
  for (const g of G.ops) {
    const v = vis(g.o.i), k = `o${g.o.i}-${g.o.j}`;
    if (!v) continue;
    const o = g.o;
    if (o.t === "seg") {
      const c = C[COL[o.c]];
      if (o.c === "gold") {
        if (isCur(o.i)) over.push(<Path key={k + "g"} pts={[g.a, g.b]} stroke={c} sw={18} o={0.25 * v} />);
        over.push(<Path key={k} pts={[g.a, g.b]} stroke={c} sw={9} o={0.86 * v} dash={o.dash ? "14 10" : undefined} />);
      } else over.push(<Path key={k} pts={[g.a, g.b]} stroke={c} sw={isCur(o.i) ? 5.5 : 4.5} dash={o.dash ? "12 9" : undefined} o={v} />);
    }
    if (o.t === "ext") over.push(<Path key={k} pts={[g.a, g.b]} stroke={C.soft} sw={2.5} dash="6 8" o={v} />);
    if (o.t === "arrow") over.push(<Arrow key={k} p={g.a} q={g.b} stroke={C.red} sw={4} h={16} o={v} />);
    if (o.t === "dim") {
      const tk = o.side === "below" ? [[0, -9], [0, 9]] : [[-9, 0], [9, 0]];
      over.push(<g key={k} opacity={v}>
        {g.ext.map((e, q) => e && <line key={q} x1={e[0]} y1={e[1]} x2={e[2]} y2={e[3]} stroke={C.soft} strokeWidth={2} strokeDasharray="5 7" />)}
        <Path pts={[g.a, g.b]} stroke={C.red} sw={3.5} />
        {[g.a, g.b].map((p, q) => <line key={"t" + q} x1={p[0] + tk[0][0]} y1={p[1] + tk[0][1]} x2={p[0] + tk[1][0]} y2={p[1] + tk[1][1]} stroke={C.red} strokeWidth={3.5} strokeLinecap="round" />)}
      </g>);
    }
  }
  const dots = [];
  const labels = [];
  for (const b of G.base) {
    const rg = b.rep != null ? vis(b.rep) : 0;
    dots.push(<circle key={`bd${b.s}${b.p[0]}`} cx={b.p[0]} cy={b.p[1]} r={7} fill={C.ink} opacity={o0} />);
    if (b.x != null) labels.push(<g key={`bl${b.s}${b.p[0]}`}>{lbl(b.x, b.y, b.s, LS.pt, C.ink, 650, o0 * (1 - rg))}</g>);
  }
  for (const g of G.ops) {
    const v = vis(g.o.i), o = g.o, k = `l${o.i}-${o.j}`;
    if (!v) continue;
    if (o.t === "pt") {
      dots.push(<circle key={k} cx={g.p[0]} cy={g.p[1]} r={7} fill={C.ink} opacity={v} />);
      labels.push(<g key={k}>{lbl(g.x, g.y, o.s, o.pos === "free" ? LS.pt : LS.ax, isCur(o.i) ? C.gold : C.ink, 680, v)}</g>);
    }
    if (o.t === "seg" && o.s) labels.push(<g key={k}>{lbl(g.x, g.y, o.s, LS.tag, C[COL[o.c]], 750, v)}</g>);
    if (o.t === "dim" && o.s) labels.push(<g key={k}>{lbl(g.tag.x, g.tag.y, o.s, LS.tag, C.red, 750, v)}</g>);
  }
  const rings = [];
  for (const g of G.ops) {
    const o = g.o;
    if (o.t !== "pulse" && o.t !== "pt") continue;
    const ph = pulse(o.i);
    if (ph < 0 || (o.t === "pt" && t > P.lines[o.i].a + 1300)) continue;
    rings.push(<circle key={`r${o.i}-${o.j}`} cx={g.p[0]} cy={g.p[1]} r={10 + 22 * ph} fill="none" stroke={C.gold} strokeWidth={4} opacity={(1 - ph) * 0.9} />);
    if (o.t === "pulse") rings.push(<circle key={`rc${o.i}-${o.j}`} cx={g.p[0]} cy={g.p[1]} r={9} fill={C.gold} opacity={vis(o.i)} />);
  }
  const fullOn = fv > 0;
  const fg = fullG && (isCur(fullG.o.i) || done) ? (isCur(fullG.o.i) ? 0.5 + 0.5 * Math.sin(((t - P.lines[fullG.o.i].a) / 900) * Math.PI) ** 2 : 0.4) : 0;
  const tip = G.axTxt;
  return (
    <g opacity={o0}>
      <Path pts={G.polyS} closed fill={C.gold} fo={fullOn ? 0.22 + 0.16 * fv : 0.22} stroke="none" />
      {els}
      <Arrow p={G.axX[0]} q={G.axX[1]} stroke={C.ink} sw={3} h={18} />
      <Arrow p={G.axY[0]} q={G.axY[1]} stroke={C.ink} sw={3} h={18} />
      <text x={tip.x[0]} y={tip.x[1]} fontFamily={SERIF} fontStyle="italic" fontSize={34} fill={C.ink}>x</text>
      <text x={tip.y[0]} y={tip.y[1]} fontFamily={SERIF} fontStyle="italic" fontSize={34} fill={C.ink}>y</text>
      <text x={tip.O[0]} y={tip.O[1]} fontFamily={SERIF} fontStyle="italic" fontSize={28} fill={C.soft} textAnchor="end">O</text>
      {G.ghost && (() => {
        const g = G.ops.find((x) => x.o.t === "ghost");
        const v = g ? vis(g.o.i) : 0;
        return v > 0 && <Path pts={G.ghost} stroke={C.soft} sw={3.5} dash="10 10" o={0.85 * v} />;
      })()}
      {G.lines.map((l, k) => l.ends && (!l.L.dash || rv > 0) && (
        <Path key={k} pts={l.ends} stroke={l.L.dash ? C.lilac : C.sky} sw={l.L.dash ? 5 : 4.5} dash={l.L.dash ? "16 11" : undefined} o={l.L.dash ? rv : 1} />
      ))}
      {fullOn && <Path pts={G.polyS} closed stroke={C.gold} sw={5} o={fv} />}
      {fg > 0 && <Path pts={G.polyS} closed stroke={C.gold} sw={16} o={0.28 * fg} />}
      {over}
      {dots}
      {G.lines.map((l, k) => G.names[k] && (!l.L.dash || rv > 0) && (
        <g key={"n" + k}>{lbl(G.names[k].x, G.names[k].y, l.L.name, LS.name, l.L.dash ? C.lilac : C.sky, 600, l.L.dash ? rv : 1)}</g>
      ))}
      {labels}
      {rings}
    </g>
  );
}

/* ══════════ 한 문항 한 순간 ══════════ */
export function AreaArt({ it, t, C }) {
  const P = arPlan(it), Lo = layoutOf(it);
  const cur = lineAt(P, t);
  const qo = seg(t, 0, 600, E.sine);
  const po = seg(t, P.plan[0], P.plan[0] + 600, E.sine);
  const ans = seg(t, P.ans, P.ans + 700, E.sine);
  return (
    <g>
      <g opacity={qo}>
        {Lo.qLines.map((s, i) => <MText key={i} x={LEFT} y={Lo.qY[i]} s={s} size={Lo.qs} weight={i === 0 ? 620 : 560} fill={C.ink} C={C} />)}
      </g>
      {po > 0 && (
        <g opacity={po}>
          <rect x={LEFT - 4} y={Lo.planY - Lo.ps * 1.05} width={Lo.ps * 2.9} height={Lo.ps * 1.45} rx={Lo.ps * 0.72} fill={C.teal} opacity={0.2} />
          <text x={LEFT + Lo.ps * 1.41} y={Lo.planY - Lo.ps * 0.02} fontFamily={SANS} fontSize={Lo.ps} fontWeight={800} fill={C.teal} textAnchor="middle">방침</text>
          <MText x={LEFT + Lo.ps * 3.4} y={Lo.planY} s={it.plan} size={Math.round(Lo.ps * 1.12)} weight={600} fill={C.teal} C={C} />
        </g>
      )}
      {it.lines.map((ln, i) => {
        const T = P.lines[i], R = Lo.rows[i];
        if (t < T.a) return null;
        const a = seg(t, T.a, T.a + 420, E.out);
        const dim = i < cur ? 0.78 : 1;
        const dy = (1 - a) * 12;
        return (
          <g key={i} opacity={a * dim}>
            {i === cur && <rect x={LEFT - 24} y={R.top + dy} width={6} height={R.bot - R.top} rx={3} fill={C.bar} />}
            {R.parts.map((p, k) => <MText key={k} x={LEFT + (k ? Lo.bs * 0.6 : 0)} y={R.ys[k] + dy} s={p} size={Lo.bs} weight={560} fill={C.ink} C={C} />)}
          </g>
        );
      })}
      {ans > 0 && (() => {
        const w = mathWidth(it.ans, Lo.bs, 700) + Lo.bs * 2.6;
        const fr = fracH(it.ans);
        return (
          <g opacity={ans}>
            <rect x={LEFT - 8} y={Lo.ansY - Lo.bs * (fr ? 1.25 : 1.05)} width={w} height={Lo.bs * (fr ? 1.95 : 1.5)} rx={Lo.bs * 0.3} fill="none" stroke={C.gold} strokeWidth={3.5} />
            <text x={LEFT + Lo.bs * 0.3} y={Lo.ansY - Lo.bs * 0.02} fontFamily={SANS} fontSize={Lo.bs * 0.7} fontWeight={800} fill={C.gold}>답</text>
            <MText x={LEFT + Lo.bs * 1.7} y={Lo.ansY} s={it.ans} size={Lo.bs} weight={700} fill={C.ink} C={C} />
          </g>
        );
      })()}
      <Figure it={it} t={t} cur={cur} C={C} />
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
    const sub = it.lv ? `${it.lv}단계 ${AREA_LEVEL[it.lv]} · ${it.no}번` : `${it.no}번 · ${it.sub}`;
    return {
      key: `area-${setKey}-${it.no}`, no: it.no, lv: it.lv || 0, sub0: it.sub, dur: Math.round(arPlan(it).dur / sp),
      grp: it.lv ? `${it.lv}단계` : null, marks: stepMarks(arPlan(it), it.lines, sp),
      title: { e: title, m: title }, sub: { e: sub, m: sub },
      render: (mode, t, C) => <AreaArt it={it} t={t * sp} C={C} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 ══════════ */
const LSK = "ash.display.area";
const fixSet = (v) => (AREA_SETS[v] ? v : "A");
const fixSp = (v) => (AREA_SPEEDS.includes(v) ? v : 1);
const fixLv = (v) => (Number.isInteger(v) && v >= 0 && v <= 10 ? v : 0);

export function AreaFrame(props) {
  const { ui, poke, inert } = props;
  const { Btn, Ic } = ui;
  const [cfg, setCfg] = useState(() => { const o = lsRead(LSK) || {}; return { set: fixSet(o.set), sp: fixSp(o.sp), lv: fixLv(o.lv) }; });
  useEffect(() => { lsWrite(LSK, cfg); }, [cfg]);
  const [list, setList] = useState(false);
  const [cur, setCur] = useState(0);
  const api = useRef(null);
  const lv = cfg.set === "B" ? cfg.lv : 0;
  const scenes = useMemo(() => areaScenes(cfg.set, cfg.sp, lv), [cfg.set, cfg.sp, lv]);
  const pickSet = useCallback((v) => setCfg((c) => ({ ...c, set: fixSet(v) })), []);
  const pickSp = useCallback((v) => setCfg((c) => ({ ...c, sp: fixSp(v) })), []);
  const pickLv = useCallback((v) => setCfg((c) => ({ ...c, lv: fixLv(v) })), []);
  useKeys({
    l: () => { setList((v) => !v); poke(); },
    b: () => { pickSet(cfg.set === "A" ? "B" : "A"); poke(); },
    s: () => { pickSp(cfg.sp === 1 ? 1.5 : 1); poke(); },
    Escape: () => setList(false),
  }, inert);
  const extra = (
    <>
      <span className="dsp-sep" />
      <Seg label="세트" value={cfg.set} options={[["A", "100제"], ["B", "240제"]]} onChange={pickSet} poke={poke} />
      <Seg label="빠르기" value={cfg.sp} options={[[1, "1×"], [1.5, "1.5×"]]} onChange={pickSp} poke={poke} />
      <Btn title="번호 · 단계 목록 (L)" on={list} onClick={() => { setList((v) => !v); poke(); }}>
        <Ic d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" />
      </Btn>
      <span className="dsp-sep" />
    </>
  );
  const pick = (i) => { api.current?.goTo(i); setList(false); poke(); };
  const label = `일차함수 그래프와 넓이 해설 · ${AREA_SETS[cfg.set].name}${lv ? ` · ${lv}단계` : ""}`;
  return (
    <>
      <StoryPlayer key={`${cfg.set}|${cfg.sp}|${lv}`} list={scenes} lsKey={`${LSK}.${cfg.set}.${lv}`} label={label}
        {...props} inert={inert || list} noMode extra={extra} apiRef={api} onIdx={setCur} scrub />
      {list && <NumList scenes={scenes} setKey={cfg.set} lv={lv} cur={cur} onPick={pick} onLevel={(v) => { pickLv(v); poke(); }} onClose={() => setList(false)} />}
    </>
  );
}

/** 번호 · 단계 목록 — 240제는 단계 칩을 고르면 그 단계만 돌고, 번호를 고르면 그 문항부터 */
function NumList({ scenes, setKey, lv, cur, onPick, onLevel, onClose }) {
  const lap = scenes.reduce((s, x) => s + x.dur, 0);
  const S = AREA_SETS[setKey];
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호 · 단계 목록">
        <style>{".ar-grid { grid-template-columns: repeat(5, 1fr); }"}</style>
        <div className="dsp-list-h">
          <b>일차함수 그래프와 넓이 · {S.name}</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        {setKey === "B" && (
          <div className="dsp-chips">
            {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((v) => (
              <button key={v} type="button" className={"dsp-chip" + (lv === v ? " on" : "")} aria-pressed={lv === v} onClick={() => onLevel(v)}>
                {v ? `${v}단계` : "전체 240"}
              </button>
            ))}
          </div>
        )}
        <p className="dsp-gal-sub">
          {setKey === "B" ? (lv ? `${lv}단계 ${AREA_LEVEL[lv]} 24문항만 돌아요` : "1단계부터 10단계까지 차례로 돌아요") : "쉬운 문항부터 100번까지 차례로 돌아요"}
          {" "}· 한 바퀴 약 {Math.round(lap / 60000)}분 · 지금 {scenes[cur]?.no}번 · 번호를 고르면 그 문항부터
        </p>
        <div className="dsp-grid ar-grid">
          {scenes.map((s, i) => (
            <button key={s.key} type="button" className={"dsp-card" + (i === cur ? " on" : "")} onClick={() => onPick(i)}>
              <span className="n">{s.no}</span>
              <span className="e">{s.lv ? `${s.lv}단계 · ` : ""}{s.sub0}</span>
              <span className="m">{Math.round(s.dur / 1000)}초</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

/** 액자 목록의 작은 그림 — 240제 7단계(사각형 OAPB) 첫 문항을 다 푼 순간 */
export const AreaThumb = memo(function AreaThumb({ C }) {
  const it = AREA_SETS.B.items.find((x) => x.kind === "OAPB");
  return <AreaArt it={it} t={arPlan(it).ans + 900} C={C} />;
});
