// 공부하기 데이터 캐시 — 개념 목록·문항 수를 캐시 우선(SWR)으로 즉시 그린다 (2026-09-21).
// 느렸던 원인: 화면마다 단원 12개 × 개념 N개의 count 질의를 따로 날렸다(30+ 왕복).
// 지금은: 문항 수는 서버 함수 live_counts(supabase/2026-09_live_counts.sql) 한 번으로 학기별·개념별을 받고,
// 결과는 메모리+sessionStorage 에 10분 캐시 → 재방문은 왕복 0회, 첫 방문도 셸이 미리 데워 둔다.
// supabase 는 호출 시점에만 불러온다 — tallyCounts 같은 순수 부분을 node 테스트에서 그대로 쓰기 위해
const sb = async () => (await import("../supabaseClient.js")).supabase;

const TTL = 10 * 60 * 1000;          // 캐시 수명
const FRESH = 2 * 60 * 1000;         // 이보다 신선하면 재검증도 생략
const mem = {};                      // key → { t, v }

const ssKey = (k) => "ash.cache." + k;
const readSS = (k) => {
  try { const r = JSON.parse(sessionStorage.getItem(ssKey(k)) || "null"); return r && typeof r.t === "number" && Date.now() - r.t < TTL ? r : null; }
  catch { return null; }
};
const writeSS = (k, rec) => { try { sessionStorage.setItem(ssKey(k), JSON.stringify(rec)); } catch { /* 용량 초과 등 — 캐시는 최선노력 */ } };

/** 캐시 우선 + 백그라운드 재검증. onData(v, fresh) 는 1~2번 불린다(캐시 → 신선). */
function swr(key, fetcher, onData) {
  const hit = mem[key] || readSS(key);
  if (hit) {
    mem[key] = hit;
    onData(hit.v, false);
    if (Date.now() - hit.t < FRESH) return;
  }
  fetcher()
    .then((v) => { const rec = { t: Date.now(), v }; mem[key] = rec; writeSS(key, rec); onData(v, true); })
    .catch(() => { if (!hit) onData(null, true); });
}

/** 개념 목록 (id·unit·제목·부제) — 캐시 우선 */
export const swrConcepts = (onData) =>
  swr("concepts", async () => (await import("./concepts.js")).listConcepts(), onData);

/** 문항 수 스냅샷 집계 — (unit_id, concept_ids) 행들에서 단원·개념별 수를 센다 */
export function tallyCounts(rows) {
  const unit = {}, concept = {};
  for (const r of rows || []) {
    if (r.unit_id) unit[r.unit_id] = (unit[r.unit_id] || 0) + 1;
    for (const c of r.concept_ids || []) concept[c] = (concept[c] || 0) + 1;
  }
  return { unit, concept };
}

/** live_counts(supabase/2026-09_live_counts.sql) 인자 — studyCache 필터와 1:1 */
export const rpcArgs = (filter = {}) => ({
  p_qtypes: Array.isArray(filter.qtypes) && filter.qtypes.length ? filter.qtypes : null,
  p_with_rubric: !!filter.withRubric,
  p_with_figure: !!filter.withFigure,
  p_difficulty: filter.difficulty || null,
});

/** 함수 응답 → { unit, concept } (모양이 아니면 null) */
export function fromRpc(data) {
  if (!data || typeof data !== "object" || Array.isArray(data)) return null;
  const unit = data.unit && typeof data.unit === "object" ? data.unit : null;
  const concept = data.concept && typeof data.concept === "object" ? data.concept : null;
  if (!unit && !concept) return null;
  return { unit: unit || {}, concept: concept || {} };
}

// live 문항이 10만 건이 넘어 행을 내려받아 세는 방식(limit 20000)은 뒤쪽 학기·개념을 0으로 세어 「준비 중」으로 잘못 보였다(2026-09-21).
// 그래서 서버 함수 live_counts 로 한 번에 센다. 함수가 아직 없으면(마이그레이션 전) 학기 수는 count 질의로 정확히 세고, 개념 수만 행 표본으로 근사한다.
async function fetchCounts(filter = {}) {
  const s = await sb();
  try {
    const { data, error } = await s.rpc("live_counts", rpcArgs(filter));
    if (!error) { const v = fromRpc(data); if (v) return v; }
  } catch { /* 함수 없음 등 → 아래 폴백 */ }
  const units = Object.keys((await import("./items.js")).UNIT_NAMES);
  const countUnit = async (u) => {
    let q = s.from("test_items").select("id", { count: "exact", head: true }).eq("status", "live").eq("unit_id", u);
    if (Array.isArray(filter.qtypes) && filter.qtypes.length) q = q.in("qtype", filter.qtypes);
    if (filter.withRubric) q = q.not("solution->rubric", "is", null);
    if (filter.withFigure) q = q.not("figure", "is", null);
    if (filter.difficulty) q = q.eq("difficulty", filter.difficulty);
    const { count, error } = await q;
    return error ? 0 : count || 0;
  };
  let q = s.from("test_items").select("unit_id, concept_ids").eq("status", "live");
  if (Array.isArray(filter.qtypes) && filter.qtypes.length) q = q.in("qtype", filter.qtypes);
  if (filter.withRubric) q = q.not("solution->rubric", "is", null);
  if (filter.withFigure) q = q.not("figure", "is", null);
  if (filter.difficulty) q = q.eq("difficulty", filter.difficulty);
  const [unitPairs, rows] = await Promise.all([
    Promise.all(units.map(async (u) => [u, await countUnit(u)])),
    q.limit(20000).then(({ data, error }) => { if (error) throw error; return data || []; }),
  ]);
  return { unit: Object.fromEntries(unitPairs), concept: tallyCounts(rows).concept, approx: true };
}

const filterKey = (f = {}) =>
  "counts:" + JSON.stringify({ q: f.qtypes || null, r: !!f.withRubric, g: !!f.withFigure, d: f.difficulty || null });

/** 필터별 단원×개념 문항 수 — 한 번의 질의, 캐시 우선. onData({unit:{},concept:{}}) */
export const swrCounts = (filter, onData) => swr(filterKey(filter), () => fetchCounts(filter), onData);

/** 관리자 문항 등록 직후 등 — 다음 조회가 새로 세도록 캐시를 비운다 */
export function bustStudyCache() {
  for (const k of Object.keys(mem)) delete mem[k];
  try { for (let i = sessionStorage.length - 1; i >= 0; i--) { const k = sessionStorage.key(i); if (k && k.startsWith("ash.cache.")) sessionStorage.removeItem(k); } } catch { /* 무시 */ }
}

/** 셸이 한가할 때 미리 데워 두기 — 화면 코드와 데이터 모두 (세션 1회) */
let warmed = false;
export function warmStudy() {
  if (warmed) return;
  warmed = true;
  try { import("../pages/Study.jsx"); import("../pages/solve/ItemPicker.jsx"); } catch { /* 무시 */ }
  swrConcepts(() => {});
  swrCounts({}, () => {});
}
