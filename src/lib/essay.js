// ashrain.out — 서술형 자가채점 순수 로직 (DOM 을 import 시점에 건드리지 않는다 → node 테스트 가능)
// · 자동 채점·LLM 없음. 학생이 채점 기준의 요소마다 [정확/부분/0점] 을 스스로 고르고, 앱은 합계만 낸다.
// · 결과는 훈련용 "예상 점수" 다. 공식 성적이 아니다.
//
// rubric (test_items.solution.rubric):
//   { total, items:[{ no, element, points, criterion, partial, zero }],
//     checks:[{ text, element_no, effect:"부분"|"불인정" }], principles:[string] }
// marks:  { [no]: "full" | "partial" | "zero" }     — 빠진 요소는 0점으로 본다
// checks: 체크한 실수거리의 index 집합 (Set | array)
//   · 불인정 → 해당 요소 0점
//   · 부분   → 해당 요소를 부분 점수 이하로 깎는다 (이미 그 이하면 그대로)

export const MARKS = ["full", "partial", "zero"];
export const MARK_LABEL = { full: "정확", partial: "부분", zero: "0점" };

/** "거의 다 왔어요" 판정 비율 (이상) */
export const NEAR_RATIO = 0.7;

const num = (v, d = 0) => { const n = Number(v); return Number.isFinite(n) ? n : d; };

/** 요소 배점 — 숫자가 아니면 0 */
export function fullPoints(rubricItem) {
  return Math.max(0, num(rubricItem?.points, 0));
}

/**
 * 부분 점수 — partial 문구의 "…N점" 을 읽는다 (여러 번 나오면 마지막 것).
 * 없으면 max(1, floor(points/2)). 배점을 넘지 않고 0 이상.
 */
export function partialPoints(rubricItem) {
  const pts = fullPoints(rubricItem);
  const txt = String(rubricItem?.partial ?? "");
  const mentions = txt.match(/\d+\s*점/g);
  let p;
  if (mentions && mentions.length) p = Number(mentions[mentions.length - 1].match(/\d+/)[0]);
  else p = Math.max(1, Math.floor(pts / 2));
  return Math.min(pts, Math.max(0, p));
}

function toIndexSet(checks) {
  if (checks instanceof Set) return new Set([...checks].map(Number));
  if (Array.isArray(checks)) return new Set(checks.map(Number));
  if (checks && typeof checks === "object") return new Set(Object.keys(checks).filter((k) => checks[k]).map(Number));
  return new Set();
}

/** 체크한 실수거리가 각 요소에 미치는 효과 — { [no]: "zero" | "partial" } (불인정이 부분보다 세다) */
export function checkEffects(rubric, checks) {
  const list = Array.isArray(rubric?.checks) ? rubric.checks : [];
  const on = toIndexSet(checks);
  const eff = {};
  list.forEach((c, i) => {
    if (!on.has(i) || c == null) return;
    const no = c.element_no;
    if (no == null || no === "") return;
    const e = c.effect === "불인정" ? "zero" : c.effect === "부분" ? "partial" : null;
    if (!e) return;
    const k = String(no);
    if (eff[k] !== "zero") eff[k] = e;
  });
  return eff;
}

/**
 * 채점. 반환 { total, max, perElement:[{ no, element, points, got, mark, reason }] }
 * · max 는 요소 배점의 합 (요소가 없으면 rubric.total)
 * · total 은 언제나 0 ≤ total ≤ max
 */
export function computeScore(rubric, marks = {}, checks = new Set()) {
  const items = Array.isArray(rubric?.items) ? rubric.items.filter((it) => it != null) : [];
  const eff = checkEffects(rubric, checks);
  const mk = marks && typeof marks === "object" ? marks : {};
  const perElement = items.map((it, idx) => {
    const no = it.no ?? idx + 1;
    const points = fullPoints(it);
    const pp = partialPoints(it);
    let mark = mk[no] ?? mk[String(no)];
    if (!MARKS.includes(mark)) mark = "zero";
    let got = mark === "full" ? points : mark === "partial" ? pp : 0;
    let reason = MARK_LABEL[mark];
    const e = eff[String(no)];
    if (e === "zero") { got = 0; reason = "실수거리 → 불인정"; }
    else if (e === "partial" && got > pp) { got = pp; reason = "실수거리 → 부분 인정"; }
    got = Math.min(points, Math.max(0, got));
    return { no, element: it.element ?? "", points, got, mark, reason };
  });
  const max = items.length ? perElement.reduce((s, e) => s + e.points, 0) : Math.max(0, num(rubric?.total, 0));
  const total = Math.min(max, Math.max(0, perElement.reduce((s, e) => s + e.got, 0)));
  return { total, max, perElement };
}

/** 모든 요소에 표시가 있는지 (채점 완료 버튼 활성 조건) */
export function allMarked(rubric, marks = {}) {
  const items = Array.isArray(rubric?.items) ? rubric.items.filter((it) => it != null) : [];
  return items.every((it, idx) => { const no = it.no ?? idx + 1; return MARKS.includes(marks?.[no] ?? marks?.[String(no)]); });
}

/** 한 줄 평 */
export function verdict(total, max) {
  const t = num(total, 0), m = num(max, 0);
  if (m > 0 && t >= m) return "만점이에요";
  if (m > 0 && t / m >= NEAR_RATIO) return "거의 다 왔어요";
  return "핵심 요소를 다시 봐요";
}

/** 다시 볼 요소 — 만점을 못 받은 요소의 기준 문구 목록 [{ no, element, criterion, got, points, reason }] */
export function reviewList(rubric, score) {
  const items = Array.isArray(rubric?.items) ? rubric.items.filter((it) => it != null) : [];
  const per = Array.isArray(score?.perElement) ? score.perElement : [];
  const out = [];
  per.forEach((p) => {
    if (p.got >= p.points) return;
    const it = items.find((x, idx) => String(x.no ?? idx + 1) === String(p.no)) || {};
    out.push({ no: p.no, element: it.element ?? p.element ?? "", criterion: it.criterion ?? "", got: p.got, points: p.points, reason: p.reason });
  });
  return out;
}

// ── 결과 보관 (localStorage, 최근 50건) ───────────────────────────────────────

export const LS_RESULTS = "ash.essay.results";
export const RESULTS_KEEP = 50;

function storage() {
  try { return typeof globalThis !== "undefined" && globalThis.localStorage ? globalThis.localStorage : null; } catch { return null; }
}

/** 최근 결과 (최신 먼저). 읽을 수 없으면 [] */
export function loadResults() {
  const st = storage();
  if (!st) return [];
  try {
    const raw = st.getItem(LS_RESULTS);
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr.filter((r) => r && typeof r === "object") : [];
  } catch { return []; }
}

/**
 * 결과 1건 저장 — r: { itemId, snippet, total, max, correct, unitId, conceptId, synced, at? }
 * 최신을 앞에 두고 RESULTS_KEEP 개만 남긴다. 저장 후 목록을 돌려준다.
 */
export function saveResult(r) {
  if (!r || typeof r !== "object") return loadResults();
  const rec = { ...r, at: r.at || new Date().toISOString() };
  const list = [rec, ...loadResults()].slice(0, RESULTS_KEEP);
  const st = storage();
  if (st) { try { st.setItem(LS_RESULTS, JSON.stringify(list)); } catch { /* 저장 공간 부족 등 — 침묵 */ } }
  return list;
}
