// ashrain.out — 판서 모드 손바닥 거르기(팜 리젝션) — 순수 함수 · 클래스(DOM 없음, node 로 시험)
//
// 쓰는 자리: 갤럭시탭(S펜 = 선생님)과 유선 미러링한 터치 모니터(손가락 · 디스크팁 = 학생)가 같은 화면 하나를 본다.
// 미러링이라 두 기기의 입력이 한 브라우저에 함께 들어온다 — 펜(pointerType "pen")과 터치("touch")를 따로 받아 동시에 그린다.
//   · 펜(과 마우스)은 늘 받는다. 펜이 닿거나 화면 위에 떠 있는(호버) 동안, 그 근처에서 새로 닿는 터치는 선생님 손바닥으로 보고 버린다.
//   · 터치(학생)는 교실 모니터 배선 방에서 정한 규칙을 차례로 적용한다.
//     1) 손 받침 안내(hint) — 쪽을 열면 손이 놓일 단(오른손잡이면 오른쪽 단)에 형광펜 안내. 거기에 손바닥을 0.3초 대고 있으면
//        그 단을 잠근다(locked). 손잡이도 이때 정해진다(손바닥이 왼쪽 단이면 왼손잡이).
//     2) 잠금은 고정 — 손바닥이 잠깐 들렸다 다시 닿아도 풀리지 않는다. 잠긴 단에서 「시작한」 터치만 버린다(넘어 들어오는 획은 산다).
//     3) 풀기 — 잠긴 단 쪽 쪽 바깥(오른손이면 쪽 오른쪽 바깥)에 0.3초 넘게 닿아 있으면(손바닥이 쪽 밖으로 걸침) 잠금 해제(free).
//     4) 해제 뒤(free) — 마지막 필기 지점의 아래 · 손 쪽에서 새로 닿는 터치는 버린다.
//     늘: 접촉 크기(손바닥은 넓다, palmSize px 이상이면 버림 · 0 이면 끔) · 터치 필기는 한 번에 하나 · 쪽 손 쪽 · 아래 가장자리 여백 ·
//         쪽 밖에 놓인 손 근처에서 새로 닿는 터치 버림 · 지연 확정(처음 pendMs 동안 붙잡아 두었다가, 그 사이 가까이 다른 접촉이
//         또 오면 둘 다 손바닥으로 보고 버림).
//
// 좌표는 무대 px(화면). page = { l, t, r, b } 지금 보이는 쪽 상자. 시간 t 는 ms.
// 입력: down/move/up/cancel(p) — p = { id, type: "pen"|"touch"|"mouse", x, y, w, h, t, buttons? }, tick(t), setPage(page), rehint().
// 출력: 동작 목록 — { k: "start", id, src, pts } · { k: "add", id, pts } · { k: "end", id } · { k: "drop", id } (그리던 획 취소)
//        · { k: "phase", phase, col } · { k: "reject", id, why } (진단용)
// src: "pen"(펜 · 마우스 = 선생님) | "touch"(학생)

export const PALM_DEFAULT = Object.freeze({
  hand: "R",        // 학생 손잡이 R | L — 손바닥을 대면 저절로 바뀐다
  palmSize: 40,     // px — 접촉 너비 · 높이 중 큰 값이 이 이상이면 손바닥(0 = 크기 규칙 끔: 모니터가 크기를 안 알려 줄 때)
  edge: 16,         // px — 쪽의 손 쪽 · 아래 가장자리 안쪽 여백
  pendMs: 70,       // 터치 지연 확정
  pendNear: 140,    // px — 지연 확정 중 이 거리 안에 다른 접촉이 오면 손바닥
  holdMs: 300,      // 손 받침 안내 단에 이만큼 가만히 대면 잠금
  holdMove: 10,     // px — 이만큼 넘게 움직이면 「가만히」가 아니다(그냥 필기)
  unlockMs: 300,    // 쪽 밖 손 쪽에 이만큼 닿아 있으면 잠금 해제
  penNear: 220,     // px — 펜이 닿거나 떠 있는 곳에서 이 거리 안의 새 터치는 선생님 손바닥
  penMs: 700,       // 펜을 마지막으로 본 뒤 이 시간까지 펜 근처 규칙 유지
  restNear: 150,    // px — 쪽 밖에 놓인 손(접촉) 근처의 새 터치는 버림
  belowGap: 40,     // px — free 단계: 마지막 필기 지점보다 이만큼 아래 · 손 쪽이면 버림
  belowBox: 260,    // px — 그 아래 영역의 크기
  belowMs: 1500,    // 마지막 필기 뒤 이 시간까지
});

const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
const inPage = (pg, x, y) => !!pg && x >= pg.l && x <= pg.r && y >= pg.t && y <= pg.b;
const midX = (pg) => (pg.l + pg.r) / 2;
const colOf = (pg, x) => (x >= midX(pg) ? "R" : "L");
const isPenLike = (type) => type === "pen" || type === "mouse";

export class PalmGuard {
  constructor(cfg = {}) {
    this.cfg = { ...PALM_DEFAULT, ...cfg };
    this.page = null;
    this.phase = "hint";            // hint | locked | free
    this.col = this.cfg.hand;       // 잠글(잠근) 단 = 손이 놓이는 단
    this.w = new Map();             // id → 필기 { src, pend, t0, pts, x0, y0, moved }
    this.hint = new Map();          // id → 손 받침 후보(안내 단에서 닿은 터치) { t0, x0, y0, x, y, moved, pts }
    this.rest = new Map();          // id → 쪽 밖 접촉 { t0, x, y, side }
    this.palm = new Set();          // 버린 포인터(손바닥) — 끝날 때까지 무시
    this.pen = null;                // { x, y, t } 펜을 마지막으로 본 곳
    this.lastTouch = null;          // { x, y, t } 학생 마지막 필기 지점
  }

  setCfg(cfg) { this.cfg = { ...this.cfg, ...cfg }; if (this.phase === "hint") this.col = this.cfg.hand; }
  setPage(page) { this.page = page; }
  /** 새 쪽 · 「손 받침 다시」 — 다시 안내부터 */
  rehint() {
    const out = [];
    for (const [id, h] of this.hint) { if (h.moved) out.push({ k: "end", id }); }
    this.hint.clear();
    this.phase = "hint"; this.col = this.cfg.hand; this.lastTouch = null;
    out.push({ k: "phase", phase: this.phase, col: this.col });
    return out;
  }
  skipHint() {
    if (this.phase !== "hint") return [];
    this.phase = "free";
    return [{ k: "phase", phase: "free", col: this.col }];
  }

  _touchWriters() { return [...this.w.entries()].filter(([, s]) => s.src === "touch"); }
  _confirm(id, s, out) {
    s.pend = false;
    out.push({ k: "start", id, src: s.src, pts: s.pts.slice() });
  }
  _drop(id, out, why) {
    const s = this.w.get(id);
    if (s) {
      this.w.delete(id);
      if (!s.pend) out.push({ k: "drop", id });
    }
    this.palm.add(id);
    out.push({ k: "reject", id, why });
  }
  _lock(col, out) {
    this.phase = "locked"; this.col = col; this.cfg.hand = col;
    out.push({ k: "phase", phase: "locked", col });
  }

  down(p) {
    const out = [], c = this.cfg, pg = this.page, pt = [p.x, p.y, p.t];
    if (isPenLike(p.type)) {
      this.pen = { x: p.x, y: p.y, t: p.t };
      // 펜이 닿는 순간 — 펜 근처에서 막 시작한 터치(선생님 손바닥이 먼저 닿은 것)를 버린다
      for (const [id, s] of this._touchWriters()) {
        if (p.t - s.t0 <= 300 && dist({ x: s.x0, y: s.y0 }, p) < c.penNear) this._drop(id, out, "pen-after");
      }
      for (const [id, h] of this.hint) {
        if (dist({ x: h.x0, y: h.y0 }, p) < c.penNear) { this.hint.delete(id); this.palm.add(id); if (h.moved) out.push({ k: "drop", id }); }
      }
      if (p.type === "mouse" && p.buttons !== undefined && !(p.buttons & 1)) return out;
      if (!inPage(pg, p.x, p.y)) return out;
      this.w.set(p.id, { src: "pen", pend: false, t0: p.t, pts: [pt], x0: p.x, y0: p.y });
      out.push({ k: "start", id: p.id, src: "pen", pts: [pt] });
      return out;
    }

    // ── 터치(학생) ──
    if (!inPage(pg, p.x, p.y)) {
      const side = !pg ? null : p.x > pg.r ? "R" : p.x < pg.l ? "L" : null;
      this.rest.set(p.id, { t0: p.t, x: p.x, y: p.y, side });
      return out;
    }
    const size = Math.max(p.w || 0, p.h || 0);
    if (c.palmSize > 0 && size >= c.palmSize) {
      // 넓은 접촉 = 손바닥. 안내 중이면 그 단을 잠근다
      if (this.phase === "hint") this._lock(colOf(pg, p.x), out);
      for (const [id, s] of this._touchWriters()) {
        if (s.pend && dist({ x: s.x0, y: s.y0 }, p) < c.pendNear * 2) this._drop(id, out, "palm-near");
      }
      this.palm.add(p.id); out.push({ k: "reject", id: p.id, why: "size" });
      return out;
    }
    if (this.pen && p.t - this.pen.t <= c.penMs && dist(this.pen, p) < c.penNear) { this.palm.add(p.id); out.push({ k: "reject", id: p.id, why: "pen-near" }); return out; }
    for (const r of this.rest.values()) {
      if (dist(r, p) < c.restNear) { this.palm.add(p.id); out.push({ k: "reject", id: p.id, why: "rest-near" }); return out; }
    }
    // 손 쪽 · 아래 가장자리 여백(손바닥이 쪽 가장자리 바로 안쪽에서 닿는 빈틈)
    const hand = this.phase === "hint" ? this.cfg.hand : this.col;
    if (p.y > pg.b - c.edge || (hand === "R" ? p.x > pg.r - c.edge : p.x < pg.l + c.edge)) {
      this.palm.add(p.id); out.push({ k: "reject", id: p.id, why: "edge" }); return out;
    }
    // 이미 학생 필기가 있으면 — 지연 확정 중이고 가까우면 둘 다 손바닥, 아니면 이 터치만 버림(한 번에 하나)
    const tw = this._touchWriters();
    if (tw.length || this.hint.size) {
      for (const [id, s] of tw) {
        if (s.pend && dist({ x: s.x0, y: s.y0 }, p) < c.pendNear) this._drop(id, out, "two-touch");
      }
      for (const [id, h] of this.hint) {
        // 안내 단에 대고 있던 것 옆으로 또 닿음 = 손바닥(여러 점) → 잠금
        if (!h.moved && dist({ x: h.x0, y: h.y0 }, p) < c.pendNear) {
          this.hint.delete(id); this.palm.add(id);
          if (this.phase === "hint") this._lock(colOf(pg, h.x0), out);
        }
      }
      this.palm.add(p.id); out.push({ k: "reject", id: p.id, why: "one-writer" });
      return out;
    }
    const col = colOf(pg, p.x);
    if (this.phase === "locked" && col === this.col) { this.palm.add(p.id); out.push({ k: "reject", id: p.id, why: "locked" }); return out; }
    if (this.phase === "hint" && col === this.cfg.hand) {
      // 안내 단 — 가만히 대고 있으면 손바닥(잠금), 움직이면 그냥 필기
      this.hint.set(p.id, { t0: p.t, x0: p.x, y0: p.y, x: p.x, y: p.y, moved: false, pts: [pt] });
      return out;
    }
    if (this.phase === "free" && this.lastTouch && p.t - this.lastTouch.t <= c.belowMs) {
      const L = this.lastTouch, dy = p.y - L.y, dx = this.col === "R" ? p.x - L.x : L.x - p.x;
      if (dy > c.belowGap && dy < c.belowBox && dx > -30 && dx < c.belowBox) { this.palm.add(p.id); out.push({ k: "reject", id: p.id, why: "below" }); return out; }
    }
    this.w.set(p.id, { src: "touch", pend: true, t0: p.t, pts: [pt], x0: p.x, y0: p.y });
    return out;
  }

  move(p) {
    const out = [], c = this.cfg, pt = [p.x, p.y, p.t];
    if (isPenLike(p.type)) this.pen = { x: p.x, y: p.y, t: p.t };   // 호버도 펜 위치로
    if (this.palm.has(p.id)) return out;
    const r = this.rest.get(p.id);
    if (r) { r.x = p.x; r.y = p.y; this._restCheck(p.id, r, p.t, out); return out; }
    const h = this.hint.get(p.id);
    if (h) {
      h.x = p.x; h.y = p.y; h.pts.push(pt);
      if (!h.moved && dist({ x: h.x0, y: h.y0 }, p) > c.holdMove) {
        // 움직였다 = 손바닥이 아니라 필기 — 여기서부터 그린다(안내는 그대로)
        h.moved = true; this.hint.delete(p.id);
        this.w.set(p.id, { src: "touch", pend: false, t0: h.t0, pts: h.pts, x0: h.x0, y0: h.y0 });
        out.push({ k: "start", id: p.id, src: "touch", pts: h.pts.slice() });
      } else this._hintCheck(p.id, h, p.t, out);
      return out;
    }
    const s = this.w.get(p.id);
    if (!s) return out;
    s.pts.push(pt);
    if (s.pend) {
      if (p.t - s.t0 >= c.pendMs) this._confirm(p.id, s, out);
      return out;
    }
    out.push({ k: "add", id: p.id, pts: [pt] });
    if (s.src === "touch") this.lastTouch = { x: p.x, y: p.y, t: p.t };
    return out;
  }

  up(p) {
    const out = [];
    if (this.palm.delete(p.id)) return out;
    if (this.rest.delete(p.id)) return out;
    const h = this.hint.get(p.id);
    if (h) {
      // 안내 단에서 짧게 톡 — 점 하나로 그린다
      this.hint.delete(p.id);
      out.push({ k: "start", id: p.id, src: "touch", pts: h.pts.slice() }, { k: "end", id: p.id });
      this.lastTouch = { x: h.x, y: h.y, t: p.t };
      return out;
    }
    const s = this.w.get(p.id);
    if (!s) return out;
    this.w.delete(p.id);
    if (s.pend) this._confirm(p.id, s, out);
    out.push({ k: "end", id: p.id });
    if (s.src === "touch") { const last = s.pts[s.pts.length - 1]; this.lastTouch = { x: last[0], y: last[1], t: p.t }; }
    return out;
  }

  cancel(p) {
    const out = [];
    this.palm.delete(p.id); this.rest.delete(p.id);
    const h = this.hint.get(p.id);
    if (h) { this.hint.delete(p.id); if (h.moved) out.push({ k: "drop", id: p.id }); return out; }
    const s = this.w.get(p.id);
    if (s) { this.w.delete(p.id); if (!s.pend) out.push({ k: "drop", id: p.id }); }
    return out;
  }

  /** 시간만 흐를 때(손을 가만히 대고 있어 move 가 안 올 때) — 화면이 그릴 때마다 부른다 */
  tick(t) {
    const out = [];
    for (const [id, r] of this.rest) this._restCheck(id, r, t, out);
    for (const [id, h] of this.hint) this._hintCheck(id, h, t, out);
    for (const [id, s] of this.w) if (s.pend && t - s.t0 >= this.cfg.pendMs) this._confirm(id, s, out);
    return out;
  }
  busy() { return this.rest.size > 0 || this.hint.size > 0 || [...this.w.values()].some((s) => s.pend); }

  _hintCheck(id, h, t, out) {
    if (h.moved || t - h.t0 < this.cfg.holdMs) return;
    this.hint.delete(id); this.palm.add(id);
    if (this.phase === "hint") this._lock(colOf(this.page, h.x0), out);
  }
  _restCheck(id, r, t, out) {
    if (this.phase !== "locked" || r.done || t - r.t0 < this.cfg.unlockMs) return;
    if (r.side !== this.col) return;
    r.done = true;
    this.phase = "free";
    out.push({ k: "phase", phase: "free", col: this.col });
  }
}

/** 무대 px ↔ 쪽 단위(인쇄 쪽 CSS px, 210 mm ≈ 793.7) — 화면 크기 · 확대가 바뀌어도 획이 쪽에 붙어 있게 */
export const toPage = (pg, unitW, x, y) => { const k = unitW / (pg.r - pg.l); return [+((x - pg.l) * k).toFixed(1), +((y - pg.t) * k).toFixed(1)]; };
export const toStage = (pg, unitW, u, v) => { const k = (pg.r - pg.l) / unitW; return [pg.l + u * k, pg.t + v * k]; };

/** 지우개: 점(쪽 단위)에서 r 안에 닿는 획의 번호들 */
export function hitStrokes(strokes, u, v, r) {
  const hit = [];
  strokes.forEach((s, i) => {
    const P = s.p;
    for (let j = 0; j < P.length; j += 2) {
      const a = [P[j], P[j + 1]], b = j + 3 < P.length ? [P[j + 2], P[j + 3]] : a;
      if (segDist(u, v, a, b) <= r + (s.w || 2) / 2) { hit.push(i); return; }
    }
  });
  return hit;
}
function segDist(x, y, a, b) {
  const dx = b[0] - a[0], dy = b[1] - a[1], L = dx * dx + dy * dy;
  const t = L ? Math.max(0, Math.min(1, ((x - a[0]) * dx + (y - a[1]) * dy) / L)) : 0;
  return Math.hypot(x - (a[0] + t * dx), y - (a[1] + t * dy));
}
