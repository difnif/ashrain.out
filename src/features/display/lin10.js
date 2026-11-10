// ashrain.out — 교실 모니터 「일차함수 10단계 계산 해설」 계산 (lin10.js) — JSX 없음
// 프린트 세트 1 · 2(lin10-items.js)의 문항마다 박자표: ① 문제 → ② 방침 → ③ 판서 줄이 하나씩(빨간 메모는 줄 뒤에 써지듯) → ④ 답.
// 읽는 시간은 글자 수로 어림한다(분수 덩어리는 두 글자쯤). 그리기는 frames/lin10.jsx.
import { LIN10_SET1, LIN10_SET2 } from "./lin10-items.js";

export const L10_SETS = {
  1: { key: 1, name: "세트 1", items: LIN10_SET1 },
  2: { key: 2, name: "세트 2", items: LIN10_SET2 },
};
export const L10_SPEEDS = [1, 1.5];
export const L10_STAGE = {
  1: "두 점 → 기울기", 2: "기울기 · 한 점 → 상수항", 3: "x절편", 4: "식 위의 빈 좌표", 5: "평행 · y절편 → 좌표",
  6: "평행 · 한 점 → y절편", 7: "수직인 직선의 기울기", 8: "수직 · 교점 → 절편", 9: "색칠한 부분의 넓이", 10: "방정식 ↔ 함수 식",
};
export const L10_HIGH = new Set([7, 8]);          // 고1 내용(수직)

/* ══════════ 박자 (1배속 ms) ══════════ */
export const L10 = {
  Q0: 2000, QC: 55,      // 문제: 기본 + 글자당
  PLAN: 2600,            // 방침
  L0: 1500, LC: 80,      // 판서 한 줄: 기본 + 글자당
  MEMO: 1100,            // 빨간 메모가 써지는 시간
  GAP: 350,
  ANS: 1400,
  HOLD: 3800,
};
/** 읽는 글자 수 — 분수 {a/b} 는 두 글자쯤, 띄어쓰기 · 괄호는 덜 */
export const readLen = (s) => String(s ?? "").replace(/\{[^}]*\}/g, "00").replace(/[\s(),]/g, "").length;

/**
 * 문항 하나의 박자표
 *   q:[a,b] 문제 · plan:[a,b] 방침 · lines[i] = { a(나타남), m:[a,b](메모 · 없으면 null), b(끝) } · ans 답이 뜨는 시각 · dur
 */
const PLAN = new WeakMap();
export function l10Plan(it) {
  if (PLAN.has(it)) return PLAN.get(it);
  let t = 0;
  const q = [t, t + L10.Q0 + L10.QC * Math.min(readLen(it.q), 90)];
  t = q[1];
  const plan = [t, t + L10.PLAN];
  t = plan[1] + L10.GAP;
  const lines = it.lines.map((ln) => {
    const a = t;
    const body = L10.L0 + L10.LC * Math.min(readLen((ln.pre || "") + ln.s), 40);
    const m = ln.memo ? [a + body * 0.55, a + body * 0.55 + L10.MEMO] : null;
    const b = Math.max(a + body, m ? m[1] + 300 : 0);
    t = b + L10.GAP;
    return { a, m, b };
  });
  const ans = t;
  const out = { q, plan, lines, ans, dur: ans + L10.ANS + L10.HOLD };
  PLAN.set(it, out);
  return out;
}
/** 지금 판서 몇 번째 줄인가(아직이면 −1, 다 끝났으면 lines.length) */
export function lineAt(P, t) {
  if (t < P.plan[1]) return -1;
  for (let i = 0; i < P.lines.length; i++) if (t < P.lines[i].b + L10.GAP) return i;
  return P.lines.length;
}
export const lapOf = (items, sp = 1) => items.reduce((s, it) => s + l10Plan(it).dur, 0) / sp;
