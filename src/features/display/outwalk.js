// ashrain.out — 「경우 카드」 그림의 움직임 차례 (outwalk.js) — 그리기는 frames/outfig.jsx 의 OutsFig · JSX 없음
// 주사위의 눈 · 동전 · 갈림길처럼 「경우 하나하나」를 카드로 늘어놓고, 판서 줄에 맞춰 세는 움직임을 보인다.
// 개념 설명의 「움직이는 예시」(../concept-av.js)가 쓴다 — 해설 액자와 같은 판서 재생기(../lin10.js 의 l10Plan) 위에서 돈다.
//   lay row  — 한 줄로 늘어놓은 카드(주사위 한 개의 눈 1 ~ 6)            items[{ die }]
//   lay tree — 두 번 갈라지는 나뭇가지(수형도 — 동전 두 개 · 집 → 도서관 → 학교)  root · lv[{ lab, opts[], coin? }] · leaf "pair" | "cat"
//   lay grid — 두 주사위의 눈을 가로 · 세로로 놓은 6 × 6 칸(순서쌍)           rows · cols { lab, n }
// acts — 판서 줄(at)마다 적힌 차례로 돈다(줄 시간이 모자라면 outsPrep 이 hold 를 더한다):
//   count { sel, val, fly? }   짚어 세기 — 금빛 고리가 하나씩 짚으며 1, 2, 3 … 세고 「val」 도장(fly: 묶음 칸 번호 — 센 카드가 아래 묶음 칸으로 날아간다)
//   all   { val }              모든 경우 — 전체가 물결치듯 한 번 빛나고 도장
//   grow  { lv, val }          가지 뻗기 — lv 0: 첫 갈림 · lv 1: 그 「각각」에서 다시 갈림(가지마다 차례로)
//   trace { val }              길 따라 세기 — 뿌리에서 잎까지 한 갈래씩 금빛으로 짚으며 1, 2, 3 …
//   cross { sel, val }         반대인 경우 — 하나씩 × 로 지우고 도장
//   scan  { val }              찾아도 없다 — 고리가 하나하나 짚어 보지만 셀 것이 없어 0 그대로(절대 일어나지 않는 사건)
//   join  { val }              묶음 합치기 — 묶음 칸 사이에 「+」, 다 함께 빛나며 도장
//   frac  { s }                분수 도장 — 앞에서 찍은 도장 둘이 모여 분수(무대 수식 문법 「{3/6} = {1/2}」)가 된다
// sel: 카드 번호 목록(0부터) · "all" · 칸(grid)은 "r5"(가로줄) · "c5"(세로줄) · "r5c5"(한 칸) · 잎(tree)은 잎 번호(첫 갈림 i, 둘째 j → i × n1 + j).
import { lineLen } from "./lin10.js";

export const OUT_T = {
  START: 260, POOL: 300, TOUCH_MIN: 150, TOUCH_MAX: 300, TOUCH_ALL: 1200, STAMP: 320,
  FLY: 640, FLY_GAP: 110, ALL: 1100, GROW: 300, TRACE: 640, CROSS: 420, JOIN: 820, FRAC: 1100, TAIL: 360,
};
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
/** 짚는 박자(ms) — 많을수록 빠르게 */
export const outTick = (n) => clamp(OUT_T.TOUCH_ALL / Math.max(1, n), OUT_T.TOUCH_MIN, OUT_T.TOUCH_MAX);

/** 카드 수 */
export function outsCount(f) {
  if (f.lay === "row") return f.items.length;
  if (f.lay === "tree") return f.lv[0].opts.length * f.lv[1].opts.length;
  if (f.lay === "grid") return f.rows.n * f.cols.n;
  return 0;
}
/** 고른 카드 번호 목록 */
export function selIds(f, sel) {
  const N = outsCount(f);
  if (sel === "all" || sel == null) return Array.from({ length: N }, (_, i) => i);
  if (Array.isArray(sel)) return sel.filter((i) => Number.isInteger(i) && i >= 0 && i < N);
  if (f.lay === "grid" && typeof sel === "string") {
    const m = sel.match(/^(?:r(\d+))?(?:c(\d+))?$/);
    if (!m) return [];
    const r = m[1] != null ? +m[1] : null, c = m[2] != null ? +m[2] : null, nc = f.cols.n;
    return Array.from({ length: N }, (_, i) => i).filter((i) => (r == null || Math.floor(i / nc) === r) && (c == null || i % nc === c));
  }
  return [];
}

/** 움직임 하나의 길이(ms) */
export function outActMs(f, a) {
  switch (a.type) {
    case "count": {
      const n = selIds(f, a.sel).length;
      return OUT_T.POOL + n * outTick(n) + OUT_T.STAMP + (a.fly != null ? OUT_T.FLY + (n - 1) * OUT_T.FLY_GAP : 0);
    }
    case "all": return OUT_T.ALL + OUT_T.STAMP;
    case "grow": {
      const n0 = f.lv[0].opts.length, n1 = f.lv[1].opts.length;
      return (a.lv === 0 ? n0 : n0 * n1) * OUT_T.GROW * (a.lv === 0 ? 1 : 0.8) + OUT_T.STAMP;
    }
    case "trace": return outsCount(f) * OUT_T.TRACE + OUT_T.STAMP;
    case "cross": return selIds(f, a.sel).length * OUT_T.CROSS + OUT_T.STAMP;
    case "scan": { const n = outsCount(f); return OUT_T.POOL + n * outTick(n) + OUT_T.STAMP; }
    case "join": return OUT_T.JOIN;
    case "frac": return OUT_T.FRAC;
    default: return 0;
  }
}

const actsOf = (it) => (it.fig?.kind === "outs" ? it.fig.acts || [] : []);
/** 판서 줄에 hold(ms)를 더해 움직임이 줄 안에 다 돌게 한다 — l10Plan 보다 먼저 한 번 */
export function outsPrep(it) {
  if (!it.fig || it.fig.kind !== "outs") return;
  const by = new Map();
  for (const a of actsOf(it)) { if (!by.has(a.at)) by.set(a.at, []); by.get(a.at).push(a); }
  for (const [i, acts] of by) {
    const ln = it.lines[i];
    if (!ln) continue;
    const need = OUT_T.START + acts.reduce((s, a) => s + outActMs(it.fig, a), 0) + OUT_T.TAIL;
    const len0 = lineLen({ ...ln, hold: 0 }), body = lineLen({ ...ln, hold: 0, memo: null });
    ln.hold = len0 >= need ? 0 : Math.max(0, Math.round(need - body));
  }
}

const TIMES = new WeakMap();
/** 시각표 — 움직임마다 t0 · t1(P = l10Plan(it)) · 짚는 박자 tick · 짚기 시작 u0 · 다 짚음 done · 날기 시작 flyAt · 도장 stamp */
export function outsTimes(it, P) {
  if (TIMES.has(it)) return TIMES.get(it);
  const f = it.fig;
  const cur = new Map();
  const acts = actsOf(it).map((a, k) => {
    const L = P.lines[a.at];
    const c = cur.has(a.at) ? cur.get(a.at) : (L ? L.a : P.ans) + OUT_T.START;
    const d = outActMs(f, a), ids = a.sel != null ? selIds(f, a.sel) : [];
    cur.set(a.at, c + d);
    const A = { ...a, k, ids, t0: c, t1: c + d };
    if (a.type === "scan") { A.tick = outTick(outsCount(f)); A.u0 = c + OUT_T.POOL; A.done = A.u0 + outsCount(f) * A.tick; }
    if (a.type === "count") {
      A.tick = outTick(ids.length);
      A.u0 = c + OUT_T.POOL;
      A.done = A.u0 + ids.length * A.tick;
      A.flyAt = a.fly != null ? A.done : null;
      A.stamp = a.fly != null ? A.done + OUT_T.FLY + (ids.length - 1) * OUT_T.FLY_GAP : A.done;
    }
    return A;
  });
  acts.sort((x, y) => x.t0 - y.t0 || x.k - y.k);
  const out = { acts };
  TIMES.set(it, out);
  return out;
}

/** 묶음 칸(count 의 fly) — [{ g, ids, lab }] 차례대로 */
export function outsGroups(f) {
  const gs = [];
  for (const a of f.acts || []) {
    if (a.type !== "count" || a.fly == null) continue;
    gs[a.fly] = { g: a.fly, ids: selIds(f, a.sel), lab: a.lab || "" };
  }
  return gs.filter(Boolean);
}
