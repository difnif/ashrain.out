// ashrain.out — 교실 모니터: 구슬 물리 (physics.js) — JSX 없음
// 움직이는 것은 구슬(원)뿐. 못(정지한 원)·벽(두께 있는 선분)은 움직이지 않는다.
// 고정 시간 간격(기본 1/240초)으로 돌아서 같은 설정이면 언제나 같은 결과가 나온다(결정적).
//
// 장면은 "시간 t → 그림" 의 순수 함수라서, simAt(key, make, t) 가 t 까지 돌린 세계를 캐시해 두고
// 앞으로만 이어 돌린다(t 가 뒤로 가면 처음부터 다시). 초등·중등 두 판이 같은 t 를 그리면 같은 세계를 본다.
//
// 충돌: 위치 밀어내기 + 법선 방향 반발(반발 계수) + 접선 마찰. 구슬끼리는 질량이 같다고 본다.
// 바닥에 쌓여 거의 멈춘 구슬은 얼린다(frozen) — 그 뒤로는 움직이지 않는 장애물이 된다(쌓인 더미가 흔들리지 않게).
import { rng } from "./core.js";

const ST_WAIT = 0, ST_LIVE = 1, ST_FROZEN = 2, ST_GONE = 3;
export const MARBLE = { WAIT: ST_WAIT, LIVE: ST_LIVE, FROZEN: ST_FROZEN, GONE: ST_GONE };

/**
 * 세계 만들기.
 *   g 중력(px/s²) · dt 한 걸음(s) · eWall 못·벽 반발 · eBall 구슬끼리 반발 · fric 접선 마찰(0~1) · drag 공기 저항(1/s)
 *   freezeY 이 높이보다 아래에서 느려진 구슬은 얼린다 · seed 난수 씨앗(멈춘 구슬 살짝 밀기 등)
 */
export function makeWorld({ g = 1800, dt = 1 / 240, eWall = 0.35, eBall = 0.25, fric = 0.06, cell = 16, drag = 0,
  freezeY = Infinity, freezeV = 26, freezeT = 0.12, seed = 7, maxV = 2400, nudge = 90, kick = 0, crowd = 0 } = {}) {
  const W = {
    g, dt, eWall, eBall, fric, cell, freezeY, freezeV, freezeT, maxV, nudge, kick, crowd, dragK: Math.exp(-drag * dt),
    time: 0, steps: 0, rnd: rng(seed),
    // 구슬
    n: 0, x: [], y: [], vx: [], vy: [], r: [], st: [], tag: [], slow: [], born: [], spawnAt: [], sx: [], sy: [], svx: [], svy: [],
    order: [],                 // 나올 차례(spawnAt 오름차순 인덱스)
    nextSpawn: 0,
    live: [],                  // 지금 움직이는 구슬 인덱스
    frozenList: [],            // 얼린 순서
    // 정지 장애물
    pegs: [],                  // {x, y, r}
    segs: [],                  // {ax, ay, bx, by, hw(반두께), dx, dy, len2}
    splits: [],                // 갈림목 {x, y, hw, v} — 꼭대기 바로 위를 지나는 구슬을 왼쪽·오른쪽 중 한쪽으로 살짝 민다(동전 던지기)
                               // crowd > 0 이면: 그때 바로 아래·옆에 다른 구슬이 (crowd px 안으로) 붙어 있으면 동전 대신 부딪힘에 맡긴다
    lastSplit: [],
    sgrid: new Map(),          // 칸 → { p: [peg], s: [seg], f: [frozen marble] }
    onFreeze: null,            // (i) => void
    onLand: null,
  };
  return W;
}

const key = (cx, cy) => cx * 73856093 ^ cy * 19349663;
function cellOf(W, cx, cy) {
  const k = key(cx, cy);
  let c = W.sgrid.get(k);
  if (!c) { c = { p: [], s: [], f: [] }; W.sgrid.set(k, c); }
  return c;
}

/** 못(정지한 원) */
export function addPeg(W, x, y, r) {
  const i = W.pegs.length;
  W.pegs.push({ x, y, r });
  const m = r + 12, cs = W.cell;
  for (let cx = Math.floor((x - m) / cs); cx <= Math.floor((x + m) / cs); cx++)
    for (let cy = Math.floor((y - m) / cs); cy <= Math.floor((y + m) / cs); cy++) cellOf(W, cx, cy).p.push(i);
  return i;
}
/** 벽(두께 2·hw 인 선분) */
export function addWall(W, ax, ay, bx, by, hw = 2) {
  const i = W.segs.length;
  const dx = bx - ax, dy = by - ay;
  W.segs.push({ ax, ay, bx, by, hw, dx, dy, len2: dx * dx + dy * dy || 1 });
  const m = hw + 12, cs = W.cell;
  const x0 = Math.min(ax, bx) - m, x1 = Math.max(ax, bx) + m, y0 = Math.min(ay, by) - m, y1 = Math.max(ay, by) + m;
  for (let cx = Math.floor(x0 / cs); cx <= Math.floor(x1 / cs); cx++)
    for (let cy = Math.floor(y0 / cs); cy <= Math.floor(y1 / cs); cy++) {
      // 선분과 칸 사이 거리로 거른다(긴 사선 벽이 큰 상자 전체에 들어가지 않게)
      const px = (cx + 0.5) * cs, py = (cy + 0.5) * cs;
      const t = Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy || 1)));
      const qx = ax + dx * t - px, qy = ay + dy * t - py;
      if (qx * qx + qy * qy <= (cs * 0.75 + m) * (cs * 0.75 + m)) cellOf(W, cx, cy).s.push(i);
    }
  return i;
}
/** 갈림목 — 꼭대기 (x, y) 바로 위(높이 h, 폭 2·hw)를 지나는 구슬을 반반으로 왼쪽·오른쪽 v 만큼 민다(한 구슬에 한 번).
 *  혼자 지나는 구슬의 "작은 흔들림"을 동전 던지기로 대신한 것. 다른 구슬과 함께 오면(crowd) 부딪힘이 길을 정한다 */
export function addSplitter(W, x, y, hw, v, h = 24) {
  W.splits.push({ x, y, hw, v, h });
  W.splits.sort((a, b) => a.y - b.y);
}
/** 구슬 하나 — at(초)에 (x, y)에서 속도 (vx, vy)로 나온다 */
export function addMarble(W, { x, y, r, at = 0, vx = 0, vy = 0, tag = 0 }) {
  const i = W.n++;
  W.x.push(x); W.y.push(y); W.vx.push(vx); W.vy.push(vy); W.r.push(r);
  W.sx.push(x); W.sy.push(y); W.svx.push(vx); W.svy.push(vy);
  W.st.push(ST_WAIT); W.tag.push(tag); W.slow.push(0); W.born.push(-1); W.spawnAt.push(at); W.lastSplit.push(-Infinity);
  W.order.push(i);
  return i;
}
/** 나올 차례를 시각순으로 (구슬을 다 넣은 뒤 한 번) */
export function seal(W) {
  W.order.sort((a, b) => W.spawnAt[a] - W.spawnAt[b] || a - b);
  W.nextSpawn = 0;
  return W;
}

function freeze(W, i) {
  W.st[i] = ST_FROZEN; W.vx[i] = 0; W.vy[i] = 0;
  W.frozenList.push(i); W.lastFreeze = W.time;
  const r = W.r[i], m = r + 12, cs = W.cell, x = W.x[i], y = W.y[i];
  for (let cx = Math.floor((x - m) / cs); cx <= Math.floor((x + m) / cs); cx++)
    for (let cy = Math.floor((y - m) / cs); cy <= Math.floor((y + m) / cs); cy++) cellOf(W, cx, cy).f.push(i);
  if (W.onFreeze) W.onFreeze(i);
}

/** 정지한 원(못·얼린 구슬)과 부딪힘. kick: 부딪힐 때 옆으로 작게 흔들기(못·구슬의 작은 흠) */
function hitCircle(W, i, ox, oy, or, e, kick = 0) {
  const dx = W.x[i] - ox, dy = W.y[i] - oy, R = W.r[i] + or;
  const d2 = dx * dx + dy * dy;
  if (d2 >= R * R || d2 < 1e-9) return false;
  const d = Math.sqrt(d2), nx = dx / d, ny = dy / d;
  W.x[i] = ox + nx * R; W.y[i] = oy + ny * R;
  const vn = W.vx[i] * nx + W.vy[i] * ny;
  if (vn < 0) {
    const tx = W.vx[i] - vn * nx, ty = W.vy[i] - vn * ny;
    const k = 1 - W.fric;
    W.vx[i] = tx * k - e * vn * nx; W.vy[i] = ty * k - e * vn * ny;
    if (kick && vn < -kick * 0.25) W.vx[i] += (W.rnd() - 0.5) * kick;
  }
  return true;
}
/** 벽(두께 있는 선분)과 부딪힘 */
function hitSeg(W, i, s, e) {
  const px = W.x[i], py = W.y[i];
  let t = ((px - s.ax) * s.dx + (py - s.ay) * s.dy) / s.len2;
  t = t < 0 ? 0 : t > 1 ? 1 : t;
  const qx = s.ax + s.dx * t, qy = s.ay + s.dy * t;
  let dx = px - qx, dy = py - qy;
  const R = W.r[i] + s.hw;
  const d2 = dx * dx + dy * dy;
  if (d2 >= R * R) return false;
  let d = Math.sqrt(d2);
  if (d < 1e-6) { dx = -s.dy; dy = s.dx; d = Math.sqrt(dx * dx + dy * dy) || 1; }
  const nx = dx / d, ny = dy / d;
  W.x[i] = qx + nx * R; W.y[i] = qy + ny * R;
  const vn = W.vx[i] * nx + W.vy[i] * ny;
  if (vn < 0) {
    const tx = W.vx[i] - vn * nx, ty = W.vy[i] - vn * ny;
    const k = 1 - W.fric;
    W.vx[i] = tx * k - e * vn * nx; W.vy[i] = ty * k - e * vn * ny;
  }
  return true;
}

function statics(W, i) {
  const cs = W.cell, r = W.r[i];
  const cx0 = Math.floor((W.x[i] - r) / cs), cx1 = Math.floor((W.x[i] + r) / cs);
  const cy0 = Math.floor((W.y[i] - r) / cs), cy1 = Math.floor((W.y[i] + r) / cs);
  let touch = false;
  for (let cx = cx0; cx <= cx1; cx++) for (let cy = cy0; cy <= cy1; cy++) {
    const c = W.sgrid.get(key(cx, cy));
    if (!c) continue;
    for (const p of c.p) { const P = W.pegs[p]; if (hitCircle(W, i, P.x, P.y, P.r, W.eWall, W.kick)) touch = true; }
    for (const s of c.s) if (hitSeg(W, i, W.segs[s], W.eWall)) touch = true;
    for (const f of c.f) if (f !== i && hitCircle(W, i, W.x[f], W.y[f], W.r[f], W.eBall)) touch = true;
  }
  return touch;
}

/** 움직이는 구슬끼리 */
function pairs(W) {
  const L = W.live;
  if (L.length < 2) return;
  const cs = W.cell * 2, grid = new Map();
  for (const i of L) {
    const k = key(Math.floor(W.x[i] / cs), Math.floor(W.y[i] / cs));
    const a = grid.get(k);
    if (a) a.push(i); else grid.set(k, [i]);
  }
  for (const i of L) {
    const gx = Math.floor(W.x[i] / cs), gy = Math.floor(W.y[i] / cs);
    for (let ax = gx - 1; ax <= gx + 1; ax++) for (let ay = gy - 1; ay <= gy + 1; ay++) {
      const a = grid.get(key(ax, ay));
      if (!a) continue;
      for (const j of a) {
        if (j <= i) continue;
        const dx = W.x[j] - W.x[i], dy = W.y[j] - W.y[i], R = W.r[i] + W.r[j];
        const d2 = dx * dx + dy * dy;
        if (d2 >= R * R) continue;
        let d = Math.sqrt(d2), nx, ny;
        if (d < 1e-6) { nx = 1; ny = 0; d = 0; } else { nx = dx / d; ny = dy / d; }
        const push = (R - d) / 2;
        W.x[i] -= nx * push; W.y[i] -= ny * push; W.x[j] += nx * push; W.y[j] += ny * push;
        const rv = (W.vx[j] - W.vx[i]) * nx + (W.vy[j] - W.vy[i]) * ny;
        if (rv < 0) {
          const jm = -(1 + W.eBall) * rv / 2;
          W.vx[i] -= jm * nx; W.vy[i] -= jm * ny; W.vx[j] += jm * nx; W.vy[j] += jm * ny;
        }
      }
    }
  }
}

/** 구슬 i 곁에 다른 움직이는 구슬이 붙어 있나(W.crowd px 안) — 나란히(옆) 있거나, 떨어질 길(바로 아래)에 있거나 */
function crowded(W, i) {
  const r = W.r[i];
  for (const j of W.live) {
    if (j === i) continue;
    const dx = W.x[j] - W.x[i], dy = W.y[j] - W.y[i], R = r + W.r[j] + W.crowd;
    if (dx * dx + dy * dy >= R * R) continue;
    if (Math.abs(dy) <= r * 0.5) return true;                              // 나란히
    if (dy > 0 && Math.abs(dx) < (r + W.r[j]) * 0.85) return true;         // 바로 아래
  }
  return false;
}

/** 한 걸음 */
export function step(W) {
  const dt = W.dt;
  W.time += dt; W.steps++;
  // 나올 구슬
  while (W.nextSpawn < W.order.length && W.spawnAt[W.order[W.nextSpawn]] <= W.time + 1e-9) {
    const i = W.order[W.nextSpawn++];
    W.st[i] = ST_LIVE; W.born[i] = W.time; W.live.push(i);
  }
  const L = W.live;
  const vmax = W.maxV;
  const dk = W.dragK;
  for (const i of L) {
    W.vy[i] += W.g * dt;
    if (dk !== 1) { W.vx[i] *= dk; W.vy[i] *= dk; }
    const sp = Math.sqrt(W.vx[i] * W.vx[i] + W.vy[i] * W.vy[i]);
    if (sp > vmax) { W.vx[i] *= vmax / sp; W.vy[i] *= vmax / sp; }
    W.x[i] += W.vx[i] * dt; W.y[i] += W.vy[i] * dt;
  }
  for (const i of L) statics(W, i);
  pairs(W);
  for (const i of L) statics(W, i);
  if (W.splits.length) for (const i of L) {
    for (const sp of W.splits) {
      if (sp.y <= W.lastSplit[i]) continue;
      const dy = sp.y - W.y[i];
      if (dy < 0 || dy > sp.h || Math.abs(W.x[i] - sp.x) >= sp.hw) continue;
      W.lastSplit[i] = sp.y;
      const coin = W.rnd() < 0.5 ? -1 : 1;                   // 난수는 늘 같은 차례로 뽑는다(붙어 있어도)
      if (W.crowd > 0 && crowded(W, i)) {                     // 부딪힘에 맡긴 자리·시각(그림에서 표시)
        W.crowded = (W.crowded || 0) + 1;
        (W.crowds || (W.crowds = [])).push({ t: W.time, x: sp.x, y: sp.y, i });
        break;
      }
      W.vx[i] = coin * sp.v;
      break;
    }
  }
  // 얼리기 · 멈춘 구슬 살짝 밀기
  let w = 0;
  for (const i of L) {
    const sp = Math.sqrt(W.vx[i] * W.vx[i] + W.vy[i] * W.vy[i]);
    if (sp < W.freezeV) W.slow[i] += dt; else W.slow[i] = 0;
    if (W.y[i] > W.freezeY && W.slow[i] >= W.freezeT) { freeze(W, i); continue; }
    if (W.y[i] <= W.freezeY && W.slow[i] > 0.25) {            // 못 꼭대기에 얹혀 멈춤 → 살짝 밀어 떨어뜨린다
      W.vx[i] += (W.rnd() < 0.5 ? -1 : 1) * W.nudge; W.vy[i] -= W.nudge * 0.3; W.slow[i] = 0;
    }
    if (W.y[i] > 5000 || W.x[i] < -500 || W.x[i] > 5000) { W.st[i] = ST_GONE; continue; }
    L[w++] = i;
  }
  L.length = w;
}

/** 시각 tSec 까지 돌린다(앞으로만) */
export function runTo(W, tSec) {
  let guard = 0;
  while (W.time + W.dt <= tSec + 1e-9 && guard++ < 1e7) step(W);
  return W;
}

/** 씨앗 섞기 — 작은 씨앗(1, 2, 3…)도 첫 난수부터 고르게 퍼지도록(core.rng 는 작은 씨앗의 첫 값이 0 에 가깝다) */
export function seedMix(h) {
  h = Math.imul((h >>> 0) ^ (h >>> 16), 0x85ebca6b);
  h = Math.imul(h ^ (h >>> 13), 0xc2b2ae35);
  return ((h ^ (h >>> 16)) >>> 0) || 1;
}

/* ══════════ 시간에 따른 캐시 ══════════ */
const SIMS = new Map();
/**
 * key 마다 하나의 세계를 기억해 두고 tMs 까지 이어 돌린다. tMs 가 지난번보다 작으면 make() 로 새로 만든다.
 * 서로 다른 장면·설정이 번갈아 그려져도(겹쳐 넘어갈 때) 몇 개까지는 함께 기억한다.
 */
export function simAt(key, make, tMs) {
  let s = SIMS.get(key);
  if (!s || tMs < s.tMs - 0.5) {
    s = { W: make(), tMs: 0 };
    SIMS.delete(key);
    SIMS.set(key, s);
    while (SIMS.size > 6) SIMS.delete(SIMS.keys().next().value);
  } else { SIMS.delete(key); SIMS.set(key, s); }         // 최근에 쓴 것을 뒤로
  runTo(s.W, tMs / 1000);
  s.tMs = tMs;
  return s.W;
}
export function clearSims() { SIMS.clear(); }

/* ══════════ 그리기 도우미 ══════════ */
const f1 = (v) => Math.round(v * 10) / 10;
/** 원 여러 개를 하나의 path d 로 */
export function circlesD(xs, ys, rs, idx) {
  let d = "";
  for (const i of idx) {
    const x = xs[i], y = ys[i], r = rs[i];
    d += `M${f1(x - r)} ${f1(y)}a${f1(r)} ${f1(r)} 0 1 0 ${f1(2 * r)} 0a${f1(r)} ${f1(r)} 0 1 0 ${f1(-2 * r)} 0`;
  }
  return d;
}
