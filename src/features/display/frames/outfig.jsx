// ashrain.out — 「경우 카드」 그림 (frames/outfig.jsx) — 움직임 차례는 ../outwalk.js
// 주사위의 눈 · 동전 · 갈림길처럼 경우 하나하나를 카드로 놓고, 판서 줄에 맞춰 센다 — 개념 설명의 「움직이는 예시」(../concept-av.js)가 쓴다.
// 해설 액자의 그림들(frames/c100fig.jsx)과 같은 말씨로 움직인다:
//   짚는 손(금빛 고리)이 하나씩 짚으며 1, 2, 3 … 세고 → 금빛 도장 · 센 카드가 아래 묶음 칸으로 휘어 날아가 「+」로 합쳐지고 ·
//   나뭇가지(수형도)가 첫 갈림 → 「각각」에서 다시 갈라지고 · 뿌리에서 잎까지 한 갈래씩 금빛으로 따라가며 세고 ·
//   반대인 경우를 × 로 지우고 · 앞에서 찍은 도장 둘이 모여 분수 도장이 된다.
// 무대 좌표: 그림 칸 660 × 680(x 880 ~ 1540 · y 170 ~ 850). outsBox(f) = 실제로 차지하는 네모(../board.js 가 빈자리에 맞춰 줄여 넣는다).
import { seg, E, clamp } from "../core.js";
import { SANS, MText, mathWidth } from "../draw.jsx";
import { l10Plan } from "../lin10.js";
import { outsTimes, outsGroups, outsCount, OUT_T } from "../outwalk.js";

const BOX = { x0: 880, y0: 170, x1: 1540, y1: 850 };
const CX = (BOX.x0 + BOX.x1) / 2;
const LANE = 66;          // 도장 줄 간격
const STAMP_Z = 36;
const LEAF_Z = 36;        // 잎(경우) 글자
const NODE_R = 33;        // 동전 · 가지 마디

/* ══════════ 배치 ══════════ */
const GEO = new WeakMap();
const countActs = (f) => (f.acts || []).filter((a) => a.type === "count" || a.type === "all" || a.type === "cross" || a.type === "scan");
const hasFrac = (f) => (f.acts || []).some((a) => a.type === "frac");
const FRAC_Z = 52;
const fracW = (f) => Math.max(0, ...(f.acts || []).filter((a) => a.type === "frac").map((a) => mathWidth(a.s, FRAC_Z, 800) + 52));
export const stampW = (val) => mathWidth(String(val), STAMP_Z, 800) + 40;

function rowGeom(f) {
  const n = f.items.length, gap = 18;
  const S = Math.min(96, Math.floor((BOX.x1 - BOX.x0 - 40 - (n - 1) * gap) / n));
  const top = BOX.y0 + (f.cap ? 86 : 40);
  const y = top + S / 2 + 8;
  const W = n * S + (n - 1) * gap, xa = CX - W / 2 + S / 2;
  const pos = f.items.map((_, i) => ({ x: xa + i * (S + gap), y, s: S }));
  const groups = outsGroups(f);
  let gbox = [], bottom;
  if (groups.length) {
    let gs = S * 0.86;
    const widths = () => groups.map((g) => g.ids.length * gs + (g.ids.length - 1) * 12 + 36);
    while (widths().reduce((a, b) => a + b, 0) + (groups.length - 1) * 86 > BOX.x1 - BOX.x0 - 20 && gs > S * 0.5) gs *= 0.92;
    const ws = widths(), tot = ws.reduce((a, b) => a + b, 0) + (groups.length - 1) * 86;
    const gy = y + S / 2 + 150, h = gs + 36;
    let x = CX - tot / 2;
    gbox = groups.map((g, gi) => {
      const b = { ...g, x0: x, x1: x + ws[gi], y0: gy - h / 2, y1: gy + h / 2, cy: gy, gs };
      b.slots = g.ids.map((_, q) => ({ x: x + 18 + gs / 2 + q * (gs + 12), y: gy, s: gs }));
      x += ws[gi] + 86;
      return b;
    });
    bottom = gy + h / 2 + 52 + (f.acts.some((a) => a.type === "join") ? 78 : 0) + 24;
  } else {
    const lanes = countActs(f).length;
    bottom = y + S / 2 + 30 + lanes * LANE + (hasFrac(f) ? 96 : 0);
  }
  return { lay: "row", S, pos, groups: gbox, top: f.cap ? BOX.y0 + 12 : top - 34, bottom, laneY: (k) => y + S / 2 + 44 + k * LANE, fracY: y + S / 2 + 44 + countActs(f).length * LANE + 26 };
}

function treeGeom(f) {
  const n0 = f.lv[0].opts.length, n1 = f.lv[1].opts.length, L = n0 * n1;
  const dy = Math.min(88, (BOX.y1 - BOX.y0 - 190) / L);
  const top = BOX.y0 + 78;
  const leaf = Array.from({ length: L }, (_, m) => ({ x: BOX.x0 + 392, y: top + dy * (m + 0.5) }));
  const n1Y = Array.from({ length: n0 }, (_, i) => (leaf[i * n1].y + leaf[i * n1 + n1 - 1].y) / 2);
  const root = { x: BOX.x0 + (f.root ? 40 : 16), y: (leaf[0].y + leaf[L - 1].y) / 2 };
  const X1 = BOX.x0 + 164, X2 = BOX.x0 + 330;
  const node1 = n1Y.map((y) => ({ x: X1, y }));
  const node2 = leaf.map((l) => ({ x: X2, y: l.y }));
  const badgeY = leaf[L - 1].y + dy * 0.5 + 44;
  const rightX = BOX.x0 + 584;
  return {
    lay: "tree", n0, n1, L, dy, root, node1, node2, leaf, headY: BOX.y0 + 34, X1, X2, rightX, badgeY,
    fracY: badgeY + 86, bottom: badgeY + 34 + (hasFrac(f) ? 98 : 0),
  };
}

function gridGeom(f) {
  const nr = f.rows.n, nc = f.cols.n, c = 62;
  const gx = BOX.x0 + 104, gy = BOX.y0 + 108;
  const cell = Array.from({ length: nr * nc }, (_, i) => ({ x: gx + (i % nc) * c + c / 2, y: gy + Math.floor(i / nc) * c + c / 2, s: c }));
  const gBottom = gy + nr * c;
  return {
    lay: "grid", nr, nc, c, gx, gy, cell, rightX: gx + nc * c + 76, allY: gBottom + 50,
    fracY: gBottom + 128, bottom: gBottom + 80 + (hasFrac(f) ? 96 : 0),
  };
}

export function outsGeom(f) {
  if (GEO.has(f)) return GEO.get(f);
  const G = f.lay === "tree" ? treeGeom(f) : f.lay === "grid" ? gridGeom(f) : rowGeom(f);
  GEO.set(f, G);
  return G;
}

/** 실제로 차지하는 네모(무대 좌표) */
export function outsBox(f) {
  const G = outsGeom(f);
  const fw = fracW(f);
  if (G.lay === "row") {
    const xs = G.pos.map((p) => p.x);
    let x0 = Math.min(...xs) - G.S / 2 - 8, x1 = Math.max(...xs) + G.S / 2 + 8;
    for (const g of G.groups) { x0 = Math.min(x0, g.x0 - 6); x1 = Math.max(x1, g.x1 + 6); }
    x0 = Math.min(x0, CX - fw / 2 - 10); x1 = Math.max(x1, CX + fw / 2 + 10);
    return { x0, y0: G.top, x1, y1: G.bottom };
  }
  if (G.lay === "tree") return { x0: BOX.x0 + 4, y0: BOX.y0, x1: BOX.x1 - 2, y1: G.bottom };
  const x1 = Math.max(G.rightX + 70, CX + fw / 2 + 10);
  return { x0: BOX.x0 + 40, y0: BOX.y0 + 4, x1: Math.min(BOX.x1, x1), y1: G.bottom };
}

/* ══════════ 지금 순간 — 움직임을 처음부터 되짚어 만든다(시각만으로 정해짐) ══════════ */
function badgeSpot(f, G, a, ids, lane) {
  if (G.lay === "row") {
    if (a.fly != null) { const g = G.groups.find((b) => b.g === a.fly); return { x: (g.x0 + g.x1) / 2, y: g.y1 + 40 }; }
    if (a.type === "all" || ids.length === G.pos.length) return { x: CX, y: G.laneY(lane) };
    const xs = ids.map((j) => G.pos[j].x);
    const w = stampW(a.val);
    return { x: clamp(xs.reduce((s, x) => s + x, 0) / xs.length, BOX.x0 + w / 2, BOX.x1 - w / 2), y: G.laneY(lane) };
  }
  if (G.lay === "tree") {
    const ys = ids.map((m) => G.leaf[m].y);
    return { x: G.rightX, y: ys.length ? ys.reduce((s, y) => s + y, 0) / ys.length : G.badgeY };
  }
  if (a.type === "all") return { x: G.gx + (G.nc * G.c) / 2, y: G.allY };
  const ys = ids.map((i) => G.cell[i].y);
  return { x: G.rightX, y: ys.reduce((s, y) => s + y, 0) / ys.length };
}

/** 도장끼리 겹치지 않게 — 앞 도장과 겹치면 한 줄 아래로 */
function place(badges, b) {
  const w = stampW(b.val) * (b.big ? 1.25 : 1);
  let y = b.y;
  for (let tries = 0; tries < 6; tries++) {
    const hit = badges.find((o) => Math.abs(o.y - y) < 50 && Math.abs(o.x - b.x) < (w + stampW(o.val)) / 2 + 6);
    if (!hit) break;
    y = hit.y + 58;
  }
  badges.push({ ...b, y });
}

function outsState(it, P, t) {
  const f = it.fig, G = outsGeom(f), T = outsTimes(it, P), N = outsCount(f);
  const S = {
    lit: new Map(), dim: null, spot: null, badges: [], ghost: new Set(), fly: new Map(), inGroup: new Map(),
    crossed: new Map(), grow: [null, null], path: null, join: 0, frac: null, wave: new Map(),
  };
  const growActs = (f.acts || []).filter((a) => a.type === "grow");
  if (f.lay === "tree") {
    S.grow[0] = growActs.some((a) => a.lv === 0) ? 0 : G.n0;
    S.grow[1] = growActs.some((a) => a.lv === 1) ? 0 : G.L;
  }
  let lane = 0;
  for (const a of T.acts) {
    if (t < a.t0) break;
    const tt = Math.min(t, a.t1), on = t < a.t1;
    if (a.type === "count") {
      if (a.keep) for (const [j, v] of S.lit) S.lit.set(j, Math.min(v, 0.42));
      else S.lit.clear();
      const n = tt < a.u0 ? 0 : Math.min(a.ids.length, Math.floor((tt - a.u0) / a.tick) + 1);
      for (let q = 0; q < n; q++) S.lit.set(a.ids[q], 1);
      if (on && n > 0 && tt < a.done) S.spot = { j: a.ids[n - 1], n, k: ((tt - a.u0) % a.tick) / a.tick };
      S.dim = new Set([...S.lit.keys()]);
      if (a.fly != null && t >= a.flyAt) {
        const g = G.groups.find((b) => b.g === a.fly);
        a.ids.forEach((j, q) => {
          const t0 = a.flyAt + q * OUT_T.FLY_GAP, k = seg(t, t0, t0 + OUT_T.FLY, E.io);
          if (k <= 0) return;
          S.ghost.add(j);
          if (k < 1) S.fly.set(j, { from: G.pos[j], to: g.slots[q], k });
          else S.inGroup.set(j, { ...g.slots[q], g: a.fly });
        });
      }
      const ln = a.fly != null ? 0 : lane++;
      if (t >= a.stamp) place(S.badges, { key: a.k, val: a.val, k: seg(t, a.stamp, a.stamp + OUT_T.STAMP, E.lin), ...badgeSpot(f, G, a, a.ids, ln) });
    } else if (a.type === "all") {
      const u = (tt - a.t0) / OUT_T.ALL;
      if (on) for (let j = 0; j < N; j++) { const d = u * 1.4 - (j / N) * 0.9; if (d > 0 && d < 0.5) S.wave.set(j, Math.sin((d / 0.5) * Math.PI)); }
      S.lit.clear(); S.dim = null;
      const ts = a.t0 + OUT_T.ALL * 0.62;
      if (t >= ts) place(S.badges, { key: a.k, val: a.val, k: seg(t, ts, ts + OUT_T.STAMP, E.lin), ...badgeSpot(f, G, a, [], lane) });
      lane++;
    } else if (a.type === "scan") {
      S.lit.clear(); S.dim = null;
      const n = tt < a.u0 ? 0 : Math.min(N, Math.floor((tt - a.u0) / a.tick) + 1);
      if (on && n > 0 && tt < a.done) S.spot = { j: n - 1, n: 0, k: ((tt - a.u0) % a.tick) / a.tick, miss: true };
      if (t >= a.done) place(S.badges, { key: a.k, val: a.val, k: seg(t, a.done, a.done + OUT_T.STAMP, E.lin), red: true, ...badgeSpot(f, G, { type: "all" }, [], lane) });
      lane++;
    } else if (a.type === "grow") {
      const step = OUT_T.GROW * (a.lv === 0 ? 1 : 0.8), cnt = a.lv === 0 ? G.n0 : G.L;
      const u = (tt - a.t0) / step;
      S.grow[a.lv] = clamp(u, 0, cnt);
      if (on && u < cnt) {
        const m = Math.floor(u);
        S.spot = { tree: a.lv, j: m, n: a.lv === 0 ? m + 1 : (m % G.n1) + 1, k: u - m };
      }
      const ts = a.t0 + cnt * step;
      if (t >= ts) {
        const x = a.lv === 0 ? G.X1 : G.X2;
        place(S.badges, { key: a.k, val: a.val, k: seg(t, ts, ts + OUT_T.STAMP, E.lin), x, y: G.badgeY });
      }
    } else if (a.type === "trace") {
      S.lit.clear(); S.dim = null;
      const u = (tt - a.t0) / OUT_T.TRACE;
      const m = Math.floor(u);
      for (let q = 0; q < Math.min(G.L, m + 1); q++) S.lit.set(q, q < m || !on ? 1 : seg(u - m, 0, 0.6, E.io) > 0.98 ? 1 : 0.5);
      if (on && m < G.L) { S.path = { m, k: seg(u - m, 0, 0.62, E.io) }; S.spot = { j: m, n: m + 1, k: u - m }; }
      const ts = a.t0 + G.L * OUT_T.TRACE;
      if (t >= ts) place(S.badges, { key: a.k, val: a.val, k: seg(t, ts, ts + OUT_T.STAMP, E.lin), x: G.leaf[0].x + 118, y: G.badgeY });
    } else if (a.type === "cross") {
      a.ids.forEach((j, q) => { const t0 = a.t0 + q * OUT_T.CROSS; if (t >= t0) S.crossed.set(j, seg(t, t0, t0 + OUT_T.CROSS * 0.8, E.io)); });
      S.lit.clear(); S.dim = null;
      const ts = a.t0 + a.ids.length * OUT_T.CROSS;
      if (t >= ts) place(S.badges, { key: a.k, val: a.val, k: seg(t, ts, ts + OUT_T.STAMP, E.lin), red: true, ...badgeSpot(f, G, a, a.ids, lane) });
      lane++;
    } else if (a.type === "join") {
      S.join = seg(t, a.t0, a.t0 + 520, E.out);
      if (t >= a.t0 + 360) {
        const gb = G.groups;
        place(S.badges, { key: a.k, val: a.val, k: seg(t, a.t0 + 360, a.t0 + 360 + OUT_T.STAMP, E.lin), big: true, x: CX, y: gb[0].y1 + 40 + 74 });
      }
    } else if (a.type === "frac") {
      S.frac = { s: a.s, k: seg(t, a.t0 + 380, a.t0 + 900, E.lin), from: a.from || [], m: seg(t, a.t0, a.t0 + 520, E.io) };
    }
  }
  return S;
}

/* ══════════ 그리기 부품 ══════════ */
const PIP = { 1: [[0, 0]], 2: [[-1, -1], [1, 1]], 3: [[-1, -1], [0, 0], [1, 1]], 4: [[-1, -1], [1, -1], [-1, 1], [1, 1]],
  5: [[-1, -1], [1, -1], [0, 0], [-1, 1], [1, 1]], 6: [[-1, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [1, 1]] };
/** 주사위 눈 하나 */
function Die({ x, y, s, n, C, lit = 0, o = 1 }) {
  const d = s * 0.27, r = Math.max(3, s * 0.085);
  return (
    <g opacity={o}>
      {lit > 0.05 && <rect x={x - s / 2 - 7} y={y - s / 2 - 7} width={s + 14} height={s + 14} rx={s * 0.24} fill={C.gold} fillOpacity={0.16 * lit} />}
      <rect x={x - s / 2} y={y - s / 2} width={s} height={s} rx={s * 0.18} fill={C.card} stroke={lit > 0.3 ? C.gold : C.cardEdge} strokeWidth={lit > 0.3 ? 4.5 : 2.4} />
      {(PIP[n] || []).map(([u, v], i) => <circle key={i} cx={x + u * d} cy={y + v * d} r={r} fill={n === 1 ? C.red : C.ink} />)}
    </g>
  );
}
/** 동전 한 면 */
function Coin({ x, y, r, face, C, lit = 0, o = 1 }) {
  const front = face === "앞";
  return (
    <g opacity={o}>
      <circle cx={x} cy={y} r={r} fill={front ? C.gold : C.sky} fillOpacity={0.22 + 0.2 * lit} stroke={lit > 0.3 ? C.gold : front ? C.gold : C.sky} strokeWidth={lit > 0.3 ? 4.5 : 2.6} />
      <circle cx={x} cy={y} r={r * 0.78} fill="none" stroke={front ? C.gold : C.sky} strokeOpacity={0.5} strokeWidth={1.6} />
      <text x={x} y={y + r * 0.36} fontFamily={SANS} fontSize={r * 0.95} fontWeight={800} fill={C.ink} textAnchor="middle">{face}</text>
    </g>
  );
}
/** 길 이름표 같은 알약 */
function Pill({ x, y, s, C, lit = 0, o = 1, z = 30 }) {
  const w = Math.max(z * 1.5, mathWidth(s, z, 800) + z * 0.9), h = z * 1.42;
  return (
    <g opacity={o}>
      <rect x={x - w / 2} y={y - h / 2} width={w} height={h} rx={h / 2} fill={lit > 0.3 ? C.gold : C.teal} fillOpacity={lit > 0.3 ? 0.2 : 0.12} stroke={lit > 0.3 ? C.gold : C.teal} strokeWidth={lit > 0.3 ? 3.5 : 2.4} />
      <MText x={x} y={y + z * 0.35} s={s} size={z} weight={800} anchor="middle" fill={C.ink} C={C} />
    </g>
  );
}
/** 금빛 도장 */
function Stamp({ x, y, val, k, C, red = false, big = false }) {
  if (k <= 0) return null;
  const z = big ? 40 : STAMP_Z, w = mathWidth(String(val), z, 800) + (big ? 52 : 40), h = z * 1.46;
  const sc = 0.7 + 0.3 * Math.max(0, E.back(k)), col = red ? C.red : C.gold;
  return (
    <g transform={`translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${sc.toFixed(3)})`} opacity={Math.min(1, k * 2)}>
      <rect x={-w / 2} y={-h * 0.68} width={w} height={h} rx={h / 2} fill={col} fillOpacity={0.18} stroke={col} strokeWidth={2.6} />
      <MText x={0} y={z * 0.06} s={String(val)} size={z} weight={800} anchor="middle" fill={col} C={C} />
    </g>
  );
}
/** 짚는 손 — 금빛 고리 + 세는 수 */
function Spot({ x, y, r, n, k, C }) {
  const rr = r * (1.12 + 0.1 * Math.sin(Math.PI * k));
  return (
    <g>
      <circle cx={x} cy={y} r={rr} fill="none" stroke={C.gold} strokeWidth={4.5} />
      <text x={x + r * 0.9} y={y - r * 0.92} fontFamily={SANS} fontSize={Math.max(34, r * 0.9)} fontWeight={800} fill={C.gold} textAnchor="middle"
        stroke={C.halo} strokeWidth={5} paintOrder="stroke">{n}</text>
    </g>
  );
}
function Cross({ x, y, r, k, C }) {
  if (k <= 0) return null;
  const a = Math.min(1, k * 2), b = Math.max(0, k * 2 - 1), s = r * 0.8;
  return (
    <g>
      <line x1={x - s} y1={y - s} x2={x - s + 2 * s * a} y2={y - s + 2 * s * a} stroke={C.red} strokeWidth={6} strokeLinecap="round" />
      {b > 0 && <line x1={x + s} y1={y - s} x2={x + s - 2 * s * b} y2={y - s + 2 * s * b} stroke={C.red} strokeWidth={6} strokeLinecap="round" />}
    </g>
  );
}

/* ══════════ 한 줄로 늘어놓은 카드(주사위 한 개의 눈) ══════════ */
function RowArt({ f, G, S, t, C }) {
  const els = [];
  if (f.cap) els.push(<text key="cap" x={CX} y={BOX.y0 + 40} fontFamily={SANS} fontSize={30} fontWeight={700} fill={C.soft} textAnchor="middle" opacity={seg(t, 0, 500, E.sine)}>{f.cap}</text>);
  // 묶음 칸
  G.groups.forEach((g, gi) => {
    const anyIn = [...S.inGroup.values()].some((v) => v.g === g.g) || [...S.fly.keys()].some((j) => g.ids.includes(j));
    if (!anyIn) return;
    const glow = S.join;
    els.push(
      <g key={`g${gi}`}>
        {glow > 0 && <rect x={g.x0 - 6} y={g.y0 - 6} width={g.x1 - g.x0 + 12} height={g.y1 - g.y0 + 12} rx={22} fill={C.gold} fillOpacity={0.12 * glow} />}
        <rect x={g.x0} y={g.y0} width={g.x1 - g.x0} height={g.y1 - g.y0} rx={18} fill="none" stroke={glow > 0.3 ? C.gold : C.teal} strokeWidth={3} strokeDasharray="10 8" />
        {g.lab && <text x={g.x0 + 10} y={g.y0 - 14} fontFamily={SANS} fontSize={28} fontWeight={800} fill={C.teal}>{g.lab}</text>}
      </g>,
    );
    if (gi > 0 && S.join > 0) {
      const xa = G.groups[gi - 1].x1, xb = g.x0;
      els.push(<text key={`p${gi}`} x={(xa + xb) / 2} y={g.cy + 20} fontFamily={SANS} fontSize={58 * (0.6 + 0.4 * Math.max(0, E.back(S.join)))} fontWeight={800} fill={C.gold} textAnchor="middle">+</text>);
    }
  });
  // 줄의 카드
  f.items.forEach((itm, j) => {
    const p = G.pos[j];
    const so = seg(t, j * 90, j * 90 + 420, E.out), dy = (1 - Math.max(0, E.back(so))) * -40;
    if (S.ghost.has(j)) {
      els.push(<rect key={`gh${j}`} x={p.x - p.s / 2} y={p.y - p.s / 2} width={p.s} height={p.s} rx={p.s * 0.18} fill="none" stroke={C.soft} strokeWidth={2} strokeDasharray="6 7" opacity={0.5} />);
      return;
    }
    const lit = Math.max(S.lit.get(j) || 0, S.wave.get(j) || 0);
    const o = S.dim && !S.dim.has(j) ? 0.4 : 1;
    els.push(<g key={`d${j}`} transform={dy ? `translate(0 ${dy.toFixed(1)})` : undefined} opacity={Math.min(1, so * 2)}><Die x={p.x} y={p.y} s={p.s} n={itm.die} C={C} lit={lit} o={o} /></g>);
  });
  // 날아가는 카드 · 묶음 칸에 들어간 카드
  for (const [j, v] of S.inGroup) els.push(<Die key={`in${j}`} x={v.x} y={v.y} s={v.s} n={f.items[j].die} C={C} lit={0.6 + 0.4 * S.join} />);
  for (const [j, v] of S.fly) {
    const x = v.from.x + (v.to.x - v.from.x) * v.k, y = v.from.y + (v.to.y - v.from.y) * v.k - Math.sin(Math.PI * v.k) * 70;
    const s = v.from.s + (v.to.s - v.from.s) * v.k;
    els.push(<Die key={`fl${j}`} x={x} y={y} s={s * (1 + 0.08 * Math.sin(Math.PI * v.k))} n={f.items[j].die} C={C} lit={1} />);
  }
  if (S.spot && S.spot.tree == null) { const p = G.pos[S.spot.j]; els.push(<Spot key="spot" x={p.x} y={p.y} r={p.s * 0.62} n={S.spot.n} k={S.spot.k} C={C} />); }
  return <g>{els}</g>;
}

/* ══════════ 나뭇가지(수형도) ══════════ */
const leafLab = (f, m, n1) => {
  const a = f.lv[0].opts[Math.floor(m / n1)], b = f.lv[1].opts[m % n1];
  return f.leaf === "cat" ? `${a}${b}` : `(${a}, ${b})`;
};
function TreeArt({ f, G, S, t, C }) {
  const els = [];
  const base = seg(t, 0, 600, E.sine);
  const heads = [[G.X1, f.lv[0].lab], [G.X2, f.lv[1].lab], [G.leaf[0].x + 60, f.leafLab || "경우"]];
  heads.forEach(([x, s], i) => els.push(<text key={`h${i}`} x={x} y={G.headY} fontFamily={SANS} fontSize={30} fontWeight={800} fill={C.soft} textAnchor="middle" opacity={base}>{s}</text>));
  const g0 = S.grow[0], g1 = S.grow[1];
  const pathOn = S.path;
  const onPath = (lv, i) => pathOn && (lv === 0 ? Math.floor(pathOn.m / G.n1) === i : pathOn.m === i);
  // 가지 — 첫 갈림
  for (let i = 0; i < G.n0; i++) {
    const k = clamp(g0 - i, 0, 1);
    if (k <= 0) continue;
    const a = G.root, b = G.node1[i];
    const sx0 = a.x + (f.root ? 36 : 12), ex = sx0 + (b.x - NODE_R - 4 - sx0) * E.out(k), ey = a.y + (b.y - a.y) * E.out(k);
    els.push(<line key={`b0${i}`} x1={sx0} y1={a.y} x2={ex} y2={ey} stroke={C.soft} strokeWidth={3.4} strokeLinecap="round" />);
    if (onPath(0, i)) {
      const pk = clamp(pathOn.k * 2, 0, 1);
      els.push(<line key={`p0${i}`} x1={sx0} y1={a.y} x2={sx0 + (b.x - NODE_R - 4 - sx0) * pk} y2={a.y + (b.y - a.y) * pk} stroke={C.gold} strokeWidth={9} strokeLinecap="round" strokeOpacity={0.85} />);
    }
  }
  // 가지 — 그 각각에서 다시
  for (let m = 0; m < G.L; m++) {
    const k = clamp(g1 - m, 0, 1);
    if (k <= 0) continue;
    const i = Math.floor(m / G.n1), a = G.node1[i], b = G.node2[m];
    const sx = a.x + NODE_R + 3, ex = sx + (b.x - NODE_R - 4 - sx) * E.out(k), ey = a.y + (b.y - a.y) * E.out(k);
    els.push(<line key={`b1${m}`} x1={sx} y1={a.y} x2={ex} y2={ey} stroke={C.soft} strokeWidth={3.4} strokeLinecap="round" />);
    if (onPath(1, m)) {
      const pk = clamp(pathOn.k * 2 - 1, 0, 1);
      if (pk > 0) els.push(<line key={`p1${m}`} x1={sx} y1={a.y} x2={sx + (b.x - NODE_R - 4 - sx) * pk} y2={a.y + (b.y - a.y) * pk} stroke={C.gold} strokeWidth={9} strokeLinecap="round" strokeOpacity={0.85} />);
    }
  }
  // 뿌리
  els.push(<g key="root" opacity={base}>{f.root ? <Pill x={G.root.x} y={G.root.y} s={f.root} C={C} z={32} /> : <circle cx={G.root.x} cy={G.root.y} r={10} fill={C.ink} />}</g>);
  const node = (lv, x, y, s, lit, key, o = 1) => (f.lv[lv].coin
    ? <Coin key={key} x={x} y={y} r={NODE_R} face={s} C={C} lit={lit} o={o} />
    : <Pill key={key} x={x} y={y} s={s} C={C} lit={lit} o={o} z={32} />);
  for (let i = 0; i < G.n0; i++) {
    const k = clamp(g0 - i, 0, 1);
    if (k < 0.55) continue;
    const pop = 0.7 + 0.3 * Math.max(0, E.back(clamp((k - 0.55) / 0.45, 0, 1)));
    const p = G.node1[i];
    els.push(<g key={`n0${i}`} transform={`translate(${p.x} ${p.y}) scale(${pop.toFixed(3)}) translate(${-p.x} ${-p.y})`}>{node(0, p.x, p.y, f.lv[0].opts[i], onPath(0, i) ? 1 : 0, "n")}</g>);
  }
  for (let m = 0; m < G.L; m++) {
    const k = clamp(g1 - m, 0, 1);
    if (k < 0.55) continue;
    const pop = 0.7 + 0.3 * Math.max(0, E.back(clamp((k - 0.55) / 0.45, 0, 1)));
    const p = G.node2[m], cr = S.crossed.get(m) || 0;
    const lit = Math.max(S.lit.get(m) || 0, onPath(1, m) ? 1 : 0);
    const o = cr > 0 ? 1 - 0.55 * cr : S.dim && !S.dim.has(m) ? 0.45 : 1;
    els.push(<g key={`n1${m}`} transform={`translate(${p.x} ${p.y}) scale(${pop.toFixed(3)}) translate(${-p.x} ${-p.y})`}>{node(1, p.x, p.y, f.lv[1].opts[m % G.n1], lit, "n", o)}</g>);
    // 잎(경우 하나) — 가지가 다 자라면 이름이 써진다
    const lo = seg(k, 0.7, 1, E.lin);
    const L = G.leaf[m];
    els.push(<g key={`lf${m}`} opacity={lo * o}>
      {lit > 0.3 && <rect x={L.x - 12} y={L.y - 30} width={mathWidth(leafLab(f, m, G.n1), LEAF_Z, 800) + 24} height={58} rx={16} fill={C.gold} fillOpacity={0.16} />}
      <MText x={L.x} y={L.y + 13} s={leafLab(f, m, G.n1)} size={LEAF_Z} weight={800} fill={lit > 0.3 ? C.gold : C.ink} C={C} />
    </g>);
    if (cr > 0) els.push(<Cross key={`x${m}`} x={L.x + mathWidth(leafLab(f, m, G.n1), LEAF_Z, 800) / 2} y={L.y} r={38} k={cr} C={C} />);
  }
  if (S.spot) {
    const lv = S.spot.tree;
    const p = lv === 0 ? G.node1[S.spot.j] : lv === 1 ? G.node2[S.spot.j] : { x: G.leaf[S.spot.j].x + mathWidth(leafLab(f, S.spot.j, G.n1), LEAF_Z, 800) / 2, y: G.leaf[S.spot.j].y };
    els.push(<Spot key="spot" x={p.x} y={p.y} r={lv == null ? Math.max(48, mathWidth(leafLab(f, S.spot.j, G.n1), LEAF_Z, 800) / 2 + 12) : NODE_R + 6} n={S.spot.n} k={S.spot.k} C={C} />);
  }
  return <g>{els}</g>;
}

/* ══════════ 두 주사위의 칸 ══════════ */
function GridArt({ f, G, S, t, C }) {
  const els = [];
  const base = seg(t, 0, 600, E.sine);
  const W = G.nc * G.c, H = G.nr * G.c;
  els.push(<text key="cap" x={G.gx + W / 2} y={BOX.y0 + 30} fontFamily={SANS} fontSize={28} fontWeight={700} fill={C.soft} textAnchor="middle" opacity={base}>{f.cap || ""}</text>);
  els.push(<text key="corner" x={G.gx - 40} y={G.gy - 24} fontFamily={SANS} fontSize={26} fontWeight={800} fill={C.soft} textAnchor="middle" opacity={base}>{`${f.rows.lab}＼${f.cols.lab}`}</text>);
  for (let r = 0; r < G.nr; r++) {
    const o = seg(t, 120 + r * 60, 480 + r * 60, E.out);
    const rowLit = [...S.lit.keys()].some((i) => Math.floor(i / G.nc) === r && S.lit.get(i) > 0.3);
    els.push(<g key={`rh${r}`} opacity={o}><Die x={G.gx - 38} y={G.gy + r * G.c + G.c / 2} s={46} n={r + 1} C={C} lit={rowLit ? 1 : 0} /></g>);
  }
  for (let c = 0; c < G.nc; c++) {
    const o = seg(t, 120 + c * 60, 480 + c * 60, E.out);
    const colLit = [...S.lit.keys()].some((i) => i % G.nc === c && S.lit.get(i) > 0.9);
    els.push(<g key={`ch${c}`} opacity={o}><Die x={G.gx + c * G.c + G.c / 2} y={G.gy - 38} s={46} n={c + 1} C={C} lit={colLit ? 1 : 0} /></g>);
  }
  els.push(<rect key="frame" x={G.gx} y={G.gy} width={W} height={H} fill="none" stroke={C.soft} strokeWidth={2.4} opacity={base} />);
  G.cell.forEach((p, i) => {
    const lit = Math.max(S.lit.get(i) || 0, S.wave.get(i) || 0);
    const o = S.dim && !S.dim.has(i) ? 0.5 : 1;
    const r = Math.floor(i / G.nc), c = i % G.nc;
    els.push(<rect key={`c${i}`} x={p.x - G.c / 2} y={p.y - G.c / 2} width={G.c} height={G.c} fill={lit > 0 ? C.gold : "none"} fillOpacity={lit > 0 ? 0.08 + 0.3 * lit : 0}
      stroke={C.faint} strokeWidth={1.6} opacity={base * o} />);
    if (lit > 0.3) els.push(<text key={`ct${i}`} x={p.x} y={p.y + 8} fontFamily={SANS} fontSize={23} fontWeight={800} fill={lit > 0.9 ? C.gold : C.soft} textAnchor="middle">{`${r + 1}, ${c + 1}`}</text>);
    else els.push(<circle key={`cd${i}`} cx={p.x} cy={p.y} r={3.2} fill={C.soft} opacity={0.45 * base * o} />);
  });
  if (S.spot) {
    const p = G.cell[S.spot.j];
    els.push(<Spot key="spot" x={p.x} y={p.y} r={G.c * 0.56} n={S.spot.n} k={S.spot.k} C={C} />);
  }
  return <g>{els}</g>;
}

/* ══════════ 그림 ══════════ */
export function OutsFig({ it, t, C }) {
  const f = it.fig, P = l10Plan(it), G = outsGeom(f);
  const S = outsState(it, P, t);
  const Art = G.lay === "tree" ? TreeArt : G.lay === "grid" ? GridArt : RowArt;
  const fracAt = (() => {
    if (!S.frac) return null;
    if (G.lay === "row") return { x: CX, y: G.groups.length ? G.bottom - 30 : G.fracY };
    if (G.lay === "tree") return { x: CX, y: G.fracY };
    return { x: G.gx + (G.nc * G.c) / 2, y: G.fracY };
  })();
  return (
    <g>
      <Art f={f} G={G} S={S} t={t} C={C} />
      {S.badges.map((b) => {
        // 분수 도장으로 모이는 도장은 그쪽으로 날아가며 흐려진다
        if (S.frac && S.frac.from.includes(b.key)) {
          const m = S.frac.m, x = b.x + (fracAt.x - b.x) * m, y = b.y + (fracAt.y - b.y) * m;
          if (m >= 1) return null;
          return <g key={`b${b.key}`} opacity={1 - m}><Stamp x={x} y={y} val={b.val} k={b.k} C={C} red={b.red} /></g>;
        }
        return <Stamp key={`b${b.key}`} x={b.x} y={b.y} val={b.val} k={b.k} C={C} red={b.red} big={b.big} />;
      })}
      {S.frac && S.frac.k > 0 && (
        <g transform={`translate(${fracAt.x} ${fracAt.y}) scale(${(0.75 + 0.25 * Math.max(0, E.back(S.frac.k))).toFixed(3)})`} opacity={Math.min(1, S.frac.k * 2)}>
          <rect x={-mathWidth(S.frac.s, FRAC_Z, 800) / 2 - 26} y={-56} width={mathWidth(S.frac.s, FRAC_Z, 800) + 52} height={96} rx={24} fill={C.gold} fillOpacity={0.14} stroke={C.gold} strokeWidth={2.8} />
          <MText x={0} y={14} s={S.frac.s} size={FRAC_Z} weight={800} anchor="middle" fill={C.gold} C={C} />
        </g>
      )}
    </g>
  );
}
