// ashrain.out — 개념 복습 모드(Ⓓ Drop 적립) 공용 로직
// · 순수 부분(최근 개념 목록 · 상한 · 첫 개념 규칙 · 퀴즈 추출 · 채점)은 node 에서 그대로 import 된다
//   (DOM·Supabase 를 import 시점에 건드리지 않는다 — tests/review.test.mjs, api/review.js 가 같이 쓴다).
// · 서버 호출(reviewStatus / startReview / completeReview)만 authx.api 를 지연 import 한다.
//
// 규칙(확정): 출석만으로는 Ⓓ 없음. 복습 모드 완주(순서대로 읽기 → 퀴즈 만점)만 Ⓓ 를 준다.
//   대상 = 최근 읽은 개념 5개, 상한 = 최근 순위별 5·3·3·2·2 회, 하루 보상 5회, 1회 10 Ⓓ.

import { CIRCLED, isChoiceCorrect, isCorrect, kindOf } from "./answers.js";

export const RECENT_KEY = "ash.recentConcepts";
export const RECENT_MAX = 5;
export const MIN_STEP_MS = 4000;        // 단락 하나에 최소 머무는 시간 (클라 "다음" 잠금)
export const MIN_TOTAL_MS = 45000;      // 시작→완료 최소 경과 (서버 판정)
export const RETRY_WINDOW_MS = 2 * 3600000; // 같은 개념 재도전 시 최초 시작 시각을 인정하는 창
export const REWARD = 10;               // 완주 1회 Ⓓ
export const DAILY_CAP = 5;             // 하루 보상 완주 횟수
export const QUIZ_N = 3;
export const CAPS = [5, 3, 3, 2, 2];    // 순위 1(가장 최근) → 5 순 상한 (과거→최근 "2·2·3·3·5")

const UNIT_ORDER = ["m1-1", "m1-2", "m2-1", "m2-2", "m3-1", "m3-2", "h1-1", "h1-2", "h2-1", "h2-2", "h3-1", "h3-2", "h3-3"];

// ── 상한·순위 ────────────────────────────────────────────────────────────────

/** 최근 순위(1=가장 최근)별 보상 완주 상한. 범위 밖(0·6 이상·비숫자)은 가장 낮은 2 */
export function capForRank(rank) {
  const r = Number(rank);
  if (!Number.isInteger(r) || r < 1) return CAPS[CAPS.length - 1];
  return CAPS[Math.min(r, CAPS.length) - 1];
}

/** recent(가장 최근이 앞) 안의 순위. 없으면 5 */
export function rankOf(recent, conceptId) {
  const ids = normRecent(recent);
  const i = ids.indexOf(String(conceptId));
  return i < 0 ? RECENT_MAX : i + 1;
}

/** 클라가 보낸 recent 를 id 문자열 배열로 정리 — 문자열/객체({id}) 혼용 허용, 중복 제거, 최대 5 */
export function normRecent(recent) {
  const out = [];
  for (const x of Array.isArray(recent) ? recent : []) {
    const id = typeof x === "string" ? x : x && typeof x === "object" ? x.id : null;
    if (!id || typeof id !== "string" || !/^[\w-]{1,40}$/.test(id) || out.includes(id)) continue;
    out.push(id);
    if (out.length >= RECENT_MAX) break;
  }
  return out;
}

// ── 최근 읽은 개념 (localStorage, 가장 최근이 앞) ─────────────────────────────

function storeOf(store) {
  if (store) return store;
  try { return typeof localStorage !== "undefined" ? localStorage : null; } catch { return null; }
}

/** [{ id, title, at }] — 가장 최근이 앞. 저장소가 없거나 깨졌으면 [] */
export function getRecentConcepts(store) {
  const s = storeOf(store);
  if (!s) return [];
  try {
    const v = JSON.parse(s.getItem(RECENT_KEY) || "[]");
    return Array.isArray(v) ? v.filter((x) => x && typeof x.id === "string").slice(0, RECENT_MAX) : [];
  } catch { return []; }
}

/** 개념을 맨 앞에 두고(중복 제거) 최대 5개 유지. 새 목록을 돌려준다 */
export function pushRecentConcept(id, title, store, now = Date.now()) {
  if (!id) return getRecentConcepts(store);
  const list = [{ id: String(id), title: title || "", at: now }, ...getRecentConcepts(store).filter((x) => x.id !== String(id))].slice(0, RECENT_MAX);
  const s = storeOf(store);
  if (s) { try { s.setItem(RECENT_KEY, JSON.stringify(list)); } catch { /* 저장 실패는 무시 */ } }
  return list;
}

export const recentIds = (list) => (list || []).map((x) => (typeof x === "string" ? x : x?.id)).filter(Boolean);

// ── 첫 사용자 기본 개념 ───────────────────────────────────────────────────────

/** profiles.grade("중1"·"고2"…) + 오늘 날짜 → 단원 id. 3~8월 = 1학기, 9~2월 = 2학기. 학년 없음/초등/기타 → "m1-1" */
export function unitFor(profile, now = new Date()) {
  const g = String(profile?.grade || "").trim();
  const m = g.match(/^(중|고)\s*([1-3])/);
  const month = now.getMonth() + 1;
  const sem = month >= 3 && month <= 8 ? 1 : 2;
  if (!m) return "m1-1";
  return `${m[1] === "고" ? "h" : "m"}${m[2]}-${sem}`;
}

/** 읽은 기록이 없는 학생에게 권하는 개념 — 학년·학기 단원의 첫 개념(sort_order 최소). 없으면 같은 학년 1학기 → m1-1 → 전체 첫 개념 */
export function defaultConceptFor(profile, concepts, now = new Date()) {
  const list = Array.isArray(concepts) ? concepts.filter((c) => c && c.id) : [];
  if (!list.length) return null;
  const bySort = (a, b) => (Number(a.sort_order) || 0) - (Number(b.sort_order) || 0);
  const first = (u) => list.filter((c) => c.unit_id === u).sort(bySort)[0] || null;
  const unit = unitFor(profile, now);
  const unitIdx = (u) => { const i = UNIT_ORDER.indexOf(u); return i < 0 ? 99 : i; };
  return first(unit) || first(unit.replace(/-\d$/, "-1")) || first("m1-1")
    || list.slice().sort((a, b) => unitIdx(a.unit_id) - unitIdx(b.unit_id) || bySort(a, b))[0];
}

// ── 퀴즈 구성 ────────────────────────────────────────────────────────────────

const stripRich = (s) => String(s ?? "").replace(/\*\*|==/g, "").replace(/\[\[\w+:([^\]]+)\]\]/g, "$1").trim();

/** 개념의 check 단락 → 단답 의사 문항 (live 문항이 3개 미만일 때 채움). 답은 서버가 다시 만든다 */
export function checkBlockItems(concept) {
  const out = [];
  for (const b of Array.isArray(concept?.blocks) ? concept.blocks : []) {
    if (!b || b.type !== "check" || !b.question || !Array.isArray(b.answer)) continue;
    b.answer.forEach((a, i) => {
      if (!a || a.nums == null || String(a.nums).trim() === "") return;
      out.push({
        id: `check:${b.id}:${i}`, source: "check", qtype: "short", concept_ids: [concept.id],
        question: `${stripRich(b.question)}\n이 중 「${stripRich(a.group)}」에 해당하는 것을 모두 쓰세요. (여러 개면 쉼표로 구분)`,
        choices: null, figure: null, difficulty: null,
        answer: String(a.nums).trim(), answer_alt: [],
      });
    });
  }
  return out;
}

/** 후보에서 n개 — 객관식 우선, 같은 템플릿 중복 회피. rnd 는 테스트용 주입 */
export function pickQuiz(items, n = QUIZ_N, rnd = Math.random) {
  const shuffle = (arr) => {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  };
  const list = (items || []).filter((x) => x && x.id);
  const choice = shuffle(list.filter((x) => kindOf(x) === "choice"));
  const rest = shuffle(list.filter((x) => kindOf(x) !== "choice"));
  const out = [], seen = new Set();
  const take = (src) => {
    for (const it of src) {
      if (out.length >= n) return;
      const k = it.template_id || it.math_key || it.id;
      if (seen.has(k)) continue;
      seen.add(k); out.push(it);
    }
  };
  take(choice); take(rest);
  if (out.length < n) for (const it of [...choice, ...rest]) { if (out.length >= n) break; if (!out.includes(it)) out.push(it); }
  return out;
}

/** 학생에게 보내는 형태 — 정답·해설·라벨 제거 */
export function stripAnswers(item) {
  if (!item) return null;
  return {
    id: item.id, qtype: item.qtype || (kindOf(item) === "choice" ? "choice" : "short"),
    question: item.question, choices: Array.isArray(item.choices) ? item.choices : null,
    figure: item.figure ?? null, difficulty: item.difficulty ?? null, source: item.source || "item",
  };
}

// ── 채점 ─────────────────────────────────────────────────────────────────────

/**
 * items(정답 포함) × answers[{ item_id, answer?(text) | index?(0~4) }] → { score, max, wrong:[item_id], results }
 * 객관식은 index 우선, 없으면 answer 를 보기 번호("③")·보기 텍스트·값으로 해석. 단답은 isCorrect.
 */
export function judgeQuiz(items, answers) {
  const by = new Map();
  for (const a of Array.isArray(answers) ? answers : []) if (a && a.item_id != null) by.set(String(a.item_id), a);
  const results = [];
  for (const it of Array.isArray(items) ? items : []) {
    if (!it) continue;
    const a = by.get(String(it.id));
    let correct = false, given = null;
    if (a) {
      if (kindOf(it) === "choice") {
        const n = it.choices?.length || 0;
        let idx = Number.isInteger(a.index) ? a.index : (typeof a.index === "string" && /^\d+$/.test(a.index) ? Number(a.index) : null);
        if (idx == null && a.answer != null && String(a.answer).trim()) {
          const s = String(a.answer).trim();
          const ci = CIRCLED.indexOf(s);
          if (ci >= 0) idx = ci;
          else { const j = (it.choices || []).findIndex((c) => String(c) === s); if (j >= 0) idx = j; }
        }
        if (idx != null && idx >= 0 && idx < n) { correct = isChoiceCorrect(it, idx); given = idx; }
        else if (a.answer != null && String(a.answer).trim()) { correct = isCorrect(it, a.answer); given = String(a.answer); }
      } else if (a.answer != null && String(a.answer).trim()) {
        correct = isCorrect(it, a.answer); given = String(a.answer);
      }
    }
    results.push({ item_id: it.id, correct, given });
  }
  const max = results.length, score = results.filter((r) => r.correct).length;
  return { score, max, wrong: results.filter((r) => !r.correct).map((r) => r.item_id), results };
}

// ── 날짜 (하루 상한은 한국 시간 기준) ────────────────────────────────────────

const KST = 9 * 3600000;
/** 한국 시간으로 "오늘" 0시 → ISO 문자열 */
export function kstDayStart(now = Date.now()) {
  const t = typeof now === "number" ? now : new Date(now).getTime();
  const day = Math.floor((t + KST) / 86400000);
  return new Date(day * 86400000 - KST).toISOString();
}

// ── 서버 호출 (api/review.js) ─────────────────────────────────────────────────
// authx 는 .jsx + Supabase 클라이언트라 정적 import 하면 node 에서 이 모듈을 못 연다 → 호출 시점에만 불러온다.

async function call(body) {
  const { api } = await import("./authx.jsx");
  return api("review", body, { auth: true });
}

/** { ready, concepts:[{concept_id, rank, cap, done, remaining}], today_done, today_cap } */
export const reviewStatus = (recent) => call({ action: "status", recent: normRecent(recent) });

/** { review_id|null, items(정답 없음), rank, cap, done, remaining, today_done, today_cap, rewardable, reward, ready } */
export const startReview = (conceptId, recent) => call({ action: "start", concept_id: conceptId, recent: normRecent(recent) });

/**
 * answers: [{ item_id, answer?, index? }] · read_ms: 단락 읽기에 쓴 시간(보고용)
 * → 만점: { ok:true, score, max, reward, drop_balance, remaining, today_done, today_cap }
 *   오답: { ok:false, reason:"wrong", score, max, wrong:[item_id] } · 너무 빠름: { ok:false, reason:"too_fast", wait }
 * review_id 가 없으면(테이블 미적용) concept_id 로 채점만 한다 (보상 없음).
 */
export const completeReview = (review_id, answers, read_ms, extra = {}) =>
  call({ action: "complete", review_id, answers, read_ms, ...extra });
