// ashrain.out — 교실 모니터 「일차함수 그래프와 넓이 해설」 계산 (area.js) — JSX 없음
// 프린트 직선 1개 100제 · 직선 2개 이상 240제(area-items.js)의 문항마다 박자표:
//   ① 문제 → ② 방침 → ③ 풀이 줄이 하나씩(그 줄의 그림 — 점 · 밑변 · 높이 · 나눈 조각 — 이 같이 나타남) → ④ 답.
// 읽는 시간은 글자 수로 어림한다(분수 덩어리는 두 글자쯤). 그리기는 frames/area.jsx.
import { AREA_SET_A, AREA_SET_B, AREA_LEVEL } from "./area-items.js";

export const AREA_SETS = {
  A: { key: "A", name: "직선 1개 100제", short: "100제", code: "W7X-PY3", items: AREA_SET_A },
  B: { key: "B", name: "직선 2개 이상 240제", short: "240제", code: "6MF-CQ5", items: AREA_SET_B },
};
export const AREA_SPEEDS = [1, 1.5];
export { AREA_LEVEL };

/* ══════════ 박자 (1배속 ms) ══════════ */
export const AR = {
  Q0: 2000, QC: 55,      // 문제: 기본 + 글자당
  PLAN: 2600,            // 방침
  L0: 1500, LC: 75,      // 풀이 한 줄: 기본 + 글자당
  FIG: 700,              // 그림이 따라 나오는 줄은 조금 더
  GAP: 350,
  ANS: 1400,
  HOLD: 4200,
};
/** 읽는 글자 수 — 분수 {a/b} 는 두 글자쯤, 띄어쓰기 · 괄호는 덜 */
export const readLen = (s) => String(s ?? "").replace(/\{[^}]*\}/g, "00").replace(/[\s(),]/g, "").length;

/**
 * 문항 하나의 박자표
 *   q:[a,b] 문제 · plan:[a,b] 방침 · lines[i] = { a(나타남), b(끝) } · ans 답이 뜨는 시각 · dur
 */
const PLAN = new WeakMap();
export function arPlan(it) {
  if (PLAN.has(it)) return PLAN.get(it);
  let t = 0;
  const q = [t, t + AR.Q0 + AR.QC * Math.min(readLen(it.q), 90)];
  t = q[1];
  const plan = [t, t + AR.PLAN];
  t = plan[1] + AR.GAP;
  const lines = it.lines.map((ln) => {
    const a = t;
    const b = a + AR.L0 + AR.LC * Math.min(readLen(ln.s), 44) + (ln.ops.length ? AR.FIG : 0);
    t = b + AR.GAP;
    return { a, b };
  });
  const ans = t;
  const out = { q, plan, lines, ans, dur: ans + AR.ANS + AR.HOLD };
  PLAN.set(it, out);
  return out;
}
/** 지금 풀이 몇 번째 줄인가(아직이면 −1, 다 끝났으면 lines.length) */
export function lineAt(P, t) {
  if (t < P.plan[1]) return -1;
  for (let i = 0; i < P.lines.length; i++) if (t < P.lines[i].b + AR.GAP) return i;
  return P.lines.length;
}
export const lapOf = (items, sp = 1) => items.reduce((s, it) => s + arPlan(it).dur, 0) / sp;

/* ══════════ 그림 수 계산 (그리기와 검산이 같이 쓴다) ══════════ */
/** 직선 { t: lin | vx | hy } 위 점인가 */
export function onLine(L, p, eps = 1e-6) {
  if (L.t === "lin") return Math.abs(L.m * p[0] + L.b - p[1]) < eps;
  if (L.t === "vx") return Math.abs(p[0] - L.k) < eps;
  return Math.abs(p[1] - L.k) < eps;
}
/** 신발끈 넓이 */
export function polyArea(pts) {
  let s = 0;
  for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; s += p[0] * q[1] - q[0] * p[1]; }
  return Math.abs(s) / 2;
}
/** 문항의 그림에 나오는 모든 점(범위 잡기용) */
export function figPoints(it) {
  const out = [[0, 0], ...it.fig.poly, ...it.fig.pts.map((p) => p.p)];
  for (const ln of it.lines) for (const o of ln.ops) {
    if (o.p) out.push(o.p);
    if (o.a && Array.isArray(o.a)) out.push(o.a, o.b);
    if (o.pts) out.push(...o.pts);
  }
  if (it.fig.ghost) out.push([0, it.fig.ghost.b]);
  return out;
}
