// ashrain.out — 학생용 문항(test_items) 접근 + attempts 기록
// · 학생은 RLS(ti_read)로 status='live' 문항만 읽는다. 여기서는 그 전제로 status 필터를 항상 건다.
// · attempts 는 own insert/select 정책이 있다. 기록은 best-effort — 실패해도 화면 흐름을 막지 않는다.

import { supabase } from "../supabaseClient";
import { distractorTag } from "./misconceptions";

export const ITEM_COLS =
  "id, unit_id, concept_ids, qtype, difficulty, question, choices, answer, answer_alt, points, time_limit, tags, solution, figure, labels, template_id, math_key";

/** 단원 id → 표시명 (Home.jsx UNIT_NAMES 와 동일) */
export const UNIT_NAMES = {
  "m1-1": "중1-1", "m1-2": "중1-2", "m2-1": "중2-1", "m2-2": "중2-2", "m3-1": "중3-1", "m3-2": "중3-2",
  "h1-1": "고1-1", "h1-2": "고1-2", "h2-1": "고2-1", "h2-2": "고2-2", "h3-1": "고3-1", "h3-2": "고3-2", "h3-3": "고3-3",
};
export const UNIT_ORDER = Object.keys(UNIT_NAMES);

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

/** 같은 템플릿이 몰리지 않게 골라내기 — 템플릿당 최대 perTpl 개 */
export function diversify(items, n, perTpl = 2) {
  const out = [], cnt = {};
  for (const it of items) {
    const k = it.template_id || it.math_key || it.id;
    if ((cnt[k] || 0) >= perTpl) continue;
    cnt[k] = (cnt[k] || 0) + 1;
    out.push(it);
    if (out.length >= n) break;
  }
  if (out.length < n) for (const it of items) { if (out.length >= n) break; if (!out.includes(it)) out.push(it); }
  return out;
}

function applyFilters(q, { conceptId, unitId, qtypes, withRubric, difficulty, withFigure } = {}) {
  q = q.eq("status", "live");
  if (conceptId) q = q.contains("concept_ids", [conceptId]);
  if (unitId) q = q.eq("unit_id", unitId);
  if (Array.isArray(qtypes) && qtypes.length) q = q.in("qtype", qtypes);
  if (withRubric) q = q.not("solution->rubric", "is", null);
  if (withFigure) q = q.not("figure", "is", null);
  if (difficulty) q = q.eq("difficulty", difficulty);
  return q;
}

/**
 * 공개(live) 문항 n개 — 무작위 표본 + 템플릿 다양성.
 * opts: { conceptId, unitId, qtypes:["choice","short"], withRubric, withFigure, difficulty, n=10, pool=80 }
 */
export async function fetchLiveItems(opts = {}) {
  const n = opts.n ?? 10, pool = Math.max(opts.pool ?? 80, n * 4);
  let q = applyFilters(supabase.from("test_items").select(ITEM_COLS), opts);
  // 표본 편향을 줄이려고 정렬 축을 바꿔 가며 뽑는다 (RLS 아래 offset 랜덤은 비싸서 생략)
  const axis = ["created_at", "id", "difficulty", "param_index"][Math.floor(Math.random() * 4)];
  q = q.order(axis, { ascending: Math.random() < 0.5 }).limit(pool);
  const { data, error } = await q;
  if (error) throw error;
  return diversify(shuffle(data || []), n);
}

/** id 목록으로 (순서 유지). 못 읽는 id(비공개 등)는 빠진다 */
export async function fetchItemsByIds(ids) {
  const list = (ids || []).filter(Boolean);
  if (!list.length) return [];
  const out = [];
  for (let i = 0; i < list.length; i += 100) {
    const { data, error } = await supabase.from("test_items").select(ITEM_COLS).in("id", list.slice(i, i + 100));
    if (error) throw error;
    out.push(...(data || []));
  }
  const by = Object.fromEntries(out.map((x) => [x.id, x]));
  return list.map((id) => by[id]).filter(Boolean);
}

export async function fetchItem(id) {
  const { data, error } = await supabase.from("test_items").select(ITEM_COLS).eq("id", id).maybeSingle();
  if (error) throw error;
  return data;
}

/** 공개 문항 수 (head count) */
export async function countLive(opts = {}) {
  const { count, error } = await applyFilters(supabase.from("test_items").select("id", { count: "exact", head: true }), opts);
  if (error) return 0;
  return count || 0;
}

let _unitCounts = null;
/** 단원별 공개 문항 수 — 세션 동안 캐시 */
export async function liveCountsByUnit(force = false) {
  if (_unitCounts && !force) return _unitCounts;
  const pairs = await Promise.all(UNIT_ORDER.map(async (u) => [u, await countLive({ unitId: u })]));
  _unitCounts = Object.fromEntries(pairs);
  return _unitCounts;
}

/** 개념별 공개 문항 수 — 한 단원의 개념 id 목록에 대해 */
export async function liveCountsByConcept(conceptIds) {
  const pairs = await Promise.all((conceptIds || []).map(async (c) => [c, await countLive({ conceptId: c })]));
  return Object.fromEntries(pairs);
}

export const conceptOf = (item) => item?.concept_ids?.[0] || null;

/** 해설 단계 목록 — 신형(levels) 우선, 구형(outline/steps/check) 은 3단으로 변환 */
export function solutionLevels(item) {
  const s = item?.solution;
  if (!s) return [];
  if (Array.isArray(s.levels) && s.levels.length) return s.levels;
  const lv = [];
  if (s.outline) lv.push({ level: 1, title: "방침", text: s.outline, figure: null, anim: null });
  if (Array.isArray(s.steps) && s.steps.length) lv.push({ level: lv.length + 1, title: "전개", steps: s.steps, figure: null, anim: null });
  if (s.check) lv.push({ level: lv.length + 1, title: "확인", text: s.check, figure: null, anim: null });
  return lv;
}

export const hasRubric = (item) => !!(item?.solution?.rubric?.items?.length);

// ── attempts ─────────────────────────────────────────────────────────────────

export function deviceKind() {
  const ua = navigator.userAgent || "";
  if (/iPad|Tablet|Android(?!.*Mobile)/i.test(ua)) return "tablet";
  if (/Mobi|Android|iPhone/i.test(ua)) return "mobile";
  return "desktop";
}

export function sessionId() {
  try {
    let s = sessionStorage.getItem("ash.sid");
    if (!s) { s = Math.random().toString(36).slice(2, 10) + Date.now().toString(36); sessionStorage.setItem("ash.sid", s); }
    return s;
  } catch { return "nosession"; }
}

/**
 * 풀이 1건 기록. 실패해도 throw 하지 않고 { error } 를 돌려준다.
 * a: { uid, item, rawAnswer, correct, chosenIndex, chosenChoice, elapsedSec, hintLevel, solutionSeen, retryN, setId, seq, confidence, firstInputMs, editsN }
 */
export async function logAttempt(a) {
  try {
    const item = a.item;
    const row = {
      user_id: a.uid,
      item_id: item.id,
      set_id: a.setId ?? null,
      seq: a.seq ?? null,
      raw_answer: a.rawAnswer == null ? null : String(a.rawAnswer).slice(0, 500),
      correct: !!a.correct,
      chosen_index: a.chosenIndex == null ? null : a.chosenIndex + 1,
      chosen_choice: a.chosenChoice == null ? null : String(a.chosenChoice).slice(0, 200),
      distractor_tag: a.correct ? null : (distractorTag(item, a.chosenChoice) || null),
      elapsed_sec: a.elapsedSec == null ? null : Math.max(0, Math.round(a.elapsedSec)),
      first_input_ms: a.firstInputMs ?? null,
      edits_n: a.editsN ?? 0,
      hint_level: a.hintLevel ?? 0,
      solution_seen: !!a.solutionSeen,
      retry_n: a.retryN ?? 0,
      confidence: a.confidence ?? null,
      device: deviceKind(),
      session_id: sessionId(),
      b_at: item.difficulty == null ? null : (item.difficulty - 1) * 0.25,
      labels_snapshot: item.labels ? {
        template_id: item.template_id || item.labels.L02_template_id || null,
        difficulty: item.difficulty, math_key: item.math_key || item.labels.L46_math_key || null,
        traps: item.labels.L21_traps || null,
      } : null,
    };
    const { error } = await supabase.from("attempts").insert(row);
    return { error: error || null };
  } catch (e) {
    return { error: e };
  }
}

/** 최근 풀이 기록 (내 것) */
export async function recentAttempts(uid, { days = 7, limit = 200 } = {}) {
  const since = new Date(Date.now() - days * 86400000).toISOString();
  const { data, error } = await supabase.from("attempts")
    .select("id, item_id, set_id, correct, distractor_tag, elapsed_sec, ts, raw_answer")
    .eq("user_id", uid).gte("ts", since).order("ts", { ascending: false }).limit(limit);
  if (error) return [];
  return data || [];
}

/** 풀이 요약 — n, 정답 수, 오개념 코드 빈도 */
export function summarizeAttempts(rows) {
  const n = rows.length, ok = rows.filter((r) => r.correct).length;
  const tags = {};
  for (const r of rows) if (r.distractor_tag) tags[r.distractor_tag] = (tags[r.distractor_tag] || 0) + 1;
  const top = Object.entries(tags).sort((a, b) => b[1] - a[1]).slice(0, 5);
  return { n, ok, rate: n ? Math.round((ok / n) * 100) : null, topTags: top };
}
