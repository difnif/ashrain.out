// ashrain.out — 「문제지 그대로」 강사 모드의 화면 다루기 — 순수 함수 · 클래스(DOM 없음, node 로 시험)
//
// 강사 모드는 학생 모드와 같은 화면(폭 맞춤 × 확대, 쪽을 위아래로 이어 붙여 스크롤)을 그대로 쓴다.
//   · 펜(S펜 · 마우스) = 선생님 필기, 한 손가락 터치 = 학생 필기(palm.js 손바닥 거르기), 두 손가락 = 확대 · 이동.
//   · 손가락을 「넘기기」로 두면 한 손가락은 이동, 두 손가락은 확대 · 이동(학생 모니터 없이 선생님 혼자 쓸 때).
// Gestures — 터치 하나하나를 「필기(guard)」와 「화면 다루기(gest)」로 나눈다.
//   · 두 손가락: 첫 터치가 막 닿은 참(pairMs 안 · pairMove 안 움직임)에 둘째가 pairMin 넘게 떨어져 닿으면 둘 다 화면 다루기.
//     첫 터치는 필기로 이미 넘어갔을 수 있으므로 cancel 로 돌려받는다(지연 확정 중이면 그린 것 없음).
//   · 손바닥 막기: 펜이 닿거나 떠 있던 직후(penMs)에는 화면 다루기를 시작하지 않는다(선생님 손바닥).
//     두 손가락 후보가 아직 움직이지 않았는데(활성 전) 셋째가 닿으면 그 둘은 손바닥으로 보고 버리고 셋째를 필기로 넘긴다.
//     활성은 거리 변화나 가운데 이동이 activate px 를 넘을 때 — 가만히 놓인 손바닥은 화면을 움직이지 않는다.
//   · 출력 — view: { k: "view", s, tx, ty, ox, oy }(두 손가락: 시작 가운데 (ox, oy) 기준 배율 s · 이동 tx, ty)
//            pan:  { k: "pan", dx, dy }(한 손가락 이동 — 그때그때 스크롤)
//            end:  두 손가락 제스처가 끝나면 마지막 view(확정할 값) 또는 null
// 좌표는 화면(뷰포트) px, 시간 t 는 ms.

export const GESTURE_DEFAULT = Object.freeze({
  pairMs: 220,      // 둘째 손가락이 이 안에 닿아야 두 손가락
  pairMove: 14,     // 첫 손가락이 이만큼 넘게 움직였으면 이미 필기 — 두 손가락으로 보지 않음
  pairMin: 30,      // 두 손가락 사이가 이보다 가까우면(손바닥 한 덩이) 두 손가락으로 보지 않음
  activate: 12,     // 거리 변화 · 가운데 이동이 이만큼 넘어야 화면이 움직이기 시작
  panStart: 4,      // 한 손가락 이동의 떨림 막기
  penMs: 700,       // 펜을 본 뒤 이 시간 안에는 화면 다루기를 시작하지 않음
});

const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
const mid = (a, b) => ({ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 });

export class Gestures {
  constructor(cfg = {}) {
    this.cfg = { ...GESTURE_DEFAULT, ...cfg };
    this.t = new Map();      // id → { x0, y0, x, y, t0, route: "guard" | "gest" }
    this.g = null;           // 두 손가락 { ids: [a, b], c0, d0, active, last } | 한 손가락 { ids: [a], last: {x,y}, moved }
    this.palm = new Set();   // 버린 접촉(끝날 때까지 무시)
    this.penT = -Infinity;
  }
  setCfg(cfg) { this.cfg = { ...this.cfg, ...cfg }; }
  /** 펜이 닿거나 떠 있음 */
  pen(t) { this.penT = t; }
  busy() { return !!this.g; }
  owns(id) { return this.palm.has(id) || this.t.get(id)?.route === "gest"; }
  /** 그 접촉이 어디로 가는지 — "guard" | "gest" | "ignore" | null(모르는 접촉) */
  routeOf(id) { return this.palm.has(id) ? "ignore" : this.t.get(id)?.route ?? null; }
  reset() { this.t.clear(); this.g = null; this.palm.clear(); }

  /** ctx: { fingers: "draw" | "pan" } → { route: "guard" | "gest" | "ignore", cancel: [id] } */
  down(p, ctx = {}) {
    const c = this.cfg, fingers = ctx.fingers === "pan" ? "pan" : "draw";
    const rec = { x0: p.x, y0: p.y, x: p.x, y: p.y, t0: p.t, route: "guard" };
    const out = { route: "guard", cancel: [] };
    const g = this.g;
    if (g) {
      if (g.ids.length === 1) {
        // 한 손가락 이동 중에 둘째 → 두 손가락(확대 · 이동)으로
        const a = this.t.get(g.ids[0]);
        rec.route = "gest"; this.t.set(p.id, rec);
        this.g = { ids: [g.ids[0], p.id], c0: mid(a, p), d0: Math.max(1, dist(a, p)), active: false, last: null };
        return { route: "gest", cancel: [] };
      }
      if (!g.active && fingers === "draw") {
        // 움직이지 않던 두 접촉 + 셋째 = 손바닥(두 점) + 쓰는 손가락
        for (const id of g.ids) { this.palm.add(id); this.t.delete(id); }
        this.g = null;
        this.t.set(p.id, rec);
        return out;
      }
      this.palm.add(p.id);
      return { route: "ignore", cancel: [] };
    }
    if (fingers === "pan") {
      rec.route = "gest"; this.t.set(p.id, rec);
      this.g = { ids: [p.id], last: { x: p.x, y: p.y }, moved: false };
      return { route: "gest", cancel: [] };
    }
    if (p.t - this.penT > c.penMs) {
      // 막 닿은 필기 터치가 하나 있으면 → 두 손가락
      const young = [...this.t.entries()].filter(([id, r]) => r.route === "guard" && !this.palm.has(id));
      if (young.length === 1) {
        const [oid, o] = young[0];
        if (p.t - o.t0 <= c.pairMs && dist({ x: o.x0, y: o.y0 }, o) <= c.pairMove && dist(o, p) >= c.pairMin) {
          o.route = "gest"; rec.route = "gest"; this.t.set(p.id, rec);
          this.g = { ids: [oid, p.id], c0: mid(o, p), d0: Math.max(1, dist(o, p)), active: false, last: null };
          return { route: "gest", cancel: [oid] };
        }
      }
    }
    this.t.set(p.id, rec);
    return out;
  }

  /** → null | { k: "view", … } | { k: "pan", dx, dy } */
  move(p) {
    const r = this.t.get(p.id);
    if (!r) return null;
    r.x = p.x; r.y = p.y;
    const g = this.g;
    if (!g || !g.ids.includes(p.id)) return null;
    if (g.ids.length === 1) {
      const dx = p.x - g.last.x, dy = p.y - g.last.y;
      if (!g.moved && Math.hypot(p.x - r.x0, p.y - r.y0) < this.cfg.panStart) return null;
      g.moved = true; g.last = { x: p.x, y: p.y };
      return dx || dy ? { k: "pan", dx, dy } : null;
    }
    const a = this.t.get(g.ids[0]), b = this.t.get(g.ids[1]);
    if (!a || !b) return null;
    const cc = mid(a, b), d = dist(a, b);
    if (!g.active && (Math.abs(d - g.d0) >= this.cfg.activate || dist(cc, g.c0) >= this.cfg.activate)) g.active = true;
    if (!g.active) return null;
    g.last = { k: "view", s: d / g.d0, tx: cc.x - g.c0.x, ty: cc.y - g.c0.y, ox: g.c0.x, oy: g.c0.y };
    return g.last;
  }

  /** → { route, end } — end: 두 손가락이 끝났으면 확정할 마지막 view(움직이지 않았으면 null) */
  up(p) {
    if (this.palm.delete(p.id)) { this.t.delete(p.id); return { route: "ignore", end: null }; }
    const r = this.t.get(p.id);
    this.t.delete(p.id);
    if (!r) return { route: "ignore", end: null };
    if (r.route !== "gest") return { route: "guard", end: null };
    const g = this.g;
    let end = null;
    if (g && g.ids.includes(p.id)) {
      if (g.ids.length === 2) {
        end = g.active ? g.last : null;
        const other = g.ids.find((id) => id !== p.id);
        if (this.t.has(other)) { this.palm.add(other); this.t.delete(other); }   // 남은 손가락은 뗄 때까지 무시(필기로 새지 않게)
      }
      this.g = null;
    }
    return { route: "gest", end };
  }
  cancel(p) { return this.up(p); }
}

/** 확대 배율(폭 맞춤의 몇 배) — ± 단추의 단계 */
export const ZOOM_STEPS = [1, 1.25, 1.5, 2, 2.5, 3];
export const ZOOM_MIN = 1, ZOOM_MAX = 3;
export const clampZoom = (zm) => Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, Number.isFinite(zm) ? zm : 1));
export function stepZoom(zm, dir) {
  const e = 1e-3;
  if (dir > 0) return ZOOM_STEPS.find((s) => s > zm + e) ?? ZOOM_MAX;
  return [...ZOOM_STEPS].reverse().find((s) => s < zm - e) ?? ZOOM_MIN;
}
export const zoomLabel = (zm) => (Math.abs(zm - 1) < 0.01 ? "맞춤" : `${Math.round(zm * 100)}%`);

/**
 * 확대를 바꾼 뒤 스크롤 보정 — 화면의 한 점 (ax, ay) 아래 있던 내용이 (ax + tx, ay + ty) 로 오게.
 * r0 · r1: 바꾸기 전 · 뒤 문서 상자(host)의 화면 위치 { left, top }, z0 · z1: 배율. → { dx, dy } 만큼 스크롤을 더한다
 */
export function anchorScroll(r0, z0, r1, z1, ax, ay, tx = 0, ty = 0) {
  const ux = (ax - r0.left) / z0, uy = (ay - r0.top) / z0;      // 배율 1 기준 문서 좌표
  const wantL = ax + tx - ux * z1, wantT = ay + ty - uy * z1;
  return { dx: r1.left - wantL, dy: r1.top - wantT };
}

/** 쪽 상자들(화면 좌표) 가운데 y 가 든 쪽 — 쪽 사이 틈이면 가까운 쪽 */
export function pageAt(rects, y) {
  let best = -1, bd = Infinity;
  rects.forEach((r, i) => {
    if (!r) return;
    const d = y < r.t ? r.t - y : y > r.b ? y - r.b : 0;
    if (d < bd) { bd = d; best = i; }
  });
  return best;
}

/** 되돌리기 — 사람(src)마다 따로, 쪽에 상관없이 그 사람의 마지막 일부터 */
export function undoLast(hist, src) {
  for (let j = hist.length - 1; j >= 0; j--) if (hist[j].src === src) return hist.splice(j, 1)[0];
  return null;
}
