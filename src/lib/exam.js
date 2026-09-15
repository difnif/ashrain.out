// ashrain.out — 시험 응시(#/solve/test) 순수 도우미
// React·Supabase·DOM 에 의존하지 않는다 (node 테스트: tests/exam.test.mjs).
// 시험 유형 프리셋 · 출제 계획/문항 선발 · 채점 · 타이머 표시 · 응시 기록(test_runs 행 · 로컬 보관).
//
// [확정] 시험에는 Ⓟ/Ⓓ 보상이 붙지 않는다 — 여기에는 재화 관련 코드가 없다.
// [예고] 지금은 모든 live 문항이 test_type='concept_set' 이라 유형은 "형식"만 정한다.
//        출제 풀을 test_type 로 가르게 되면 fetchPlan() 하나만 바꾸면 된다 (SELECT_BY_TEST_TYPE 참고).

import { isChoiceCorrect, isCorrect, kindOf } from "./answers.js";
import { distractorTag } from "./misconceptions.js";

// ── 시험 유형 프리셋 ──────────────────────────────────────────────────────────
// timer.kind: total(총 제한) | item(문항당 제한) | none.  timer.soft: 시간이 끝나도 제출 전까지 계속 풀 수 있음(경고만)
// scope: concept(개념 하나) | unit(단원 하나)
// pointsMode: count(정답 수) | points(배점 합) | scaled100(배점 합을 100점 만점으로 환산)
// difficultyMax: 이 난이도 이하를 우선 출제.  mixed: 난이도 1~5 를 고루 출제.  order: "difficulty" 면 쉬운 문항부터
// route: 자체 러너 없이 다른 화면으로 보낸다 (산과 시험 → 서술형 자가채점)
export const TEST_TYPES = [
  { code: "concept_set", name: "개념 묶음", icon: "🧩", desc: "개념 하나를 고르고 문항 5개로 가볍게 확인해요. 시간 제한이 없어요.",
    n: 5, timer: { kind: "none", sec: 0 }, scope: "concept", pointsMode: "count" },
  { code: "unit", name: "단원 테스트", icon: "📘", desc: "단원 전체에서 20문항 · 30분. 시간이 끝나도 제출 전까지 답을 고칠 수 있어요.",
    n: 20, timer: { kind: "total", sec: 1800, soft: true }, scope: "unit", pointsMode: "count", order: "difficulty" },
  { code: "calc", name: "연산 테스트", icon: "⚡", desc: "쉬운 문항 10개를 문항마다 20초 안에 풀어요. 시간이 지나면 자동으로 넘어가요.",
    n: 10, timer: { kind: "item", sec: 20 }, scope: "unit", pointsMode: "count", difficultyMax: 2, qtypes: ["short", "choice"] },
  { code: "sangwa", name: "산과 시험", icon: "📝", desc: "서술·증명 문항을 직접 쓰고 채점 기준표로 스스로 채점해요.",
    n: 0, timer: { kind: "none", sec: 0 }, scope: "unit", pointsMode: "count", route: "#/solve/essay" },
  { code: "mock", name: "실전 모의고사", icon: "🎯", desc: "배점이 있는 20문항 · 40분. 100점 만점으로 환산해요.",
    n: 20, timer: { kind: "total", sec: 2400 }, scope: "unit", pointsMode: "scaled100", order: "difficulty" },
  { code: "ash", name: "Ash TEST", icon: "🔥", desc: "난이도를 골고루 섞은 15문항 · 20분. 애쉬레인의 대표 시험이에요.",
    n: 15, timer: { kind: "total", sec: 1200 }, scope: "unit", pointsMode: "count", mixed: true, badge: { text: "ASH", color: "#7C3AED" } },
  { code: "rain", name: "Rain TEST", icon: "🌧️", desc: "100문항을 25분 안에. 속도와 집중력이 실력이에요.",
    n: 100, timer: { kind: "total", sec: 1500 }, scope: "unit", pointsMode: "count", badge: { text: "RAIN", color: "#0EA5E9" }, grid: "dense" },
  { code: "out", name: "Out TEST", icon: "🏁", desc: "일제고사 30문항 · 45분. 결과는 단원 이해도 분석 자료로 저장돼요.",
    n: 30, timer: { kind: "total", sec: 2700 }, scope: "unit", pointsMode: "count", order: "difficulty", badge: { text: "OUT", color: "#F59E0B" },
    note: "일제고사 결과는 개인 성적표가 아니라 단원별 이해도 분석 자료로 쌓여요. 편하게 실력대로 풀면 돼요." },
];

export const presetOf = (code) => TEST_TYPES.find((t) => t.code === String(code || "")) || null;

/** 타이머 한 줄 설명 — "제한 시간 없음" · "총 30분" · "문항당 20초" */
export function describeTimer(preset) {
  const t = preset?.timer;
  if (!t || t.kind === "none" || !t.sec) return "제한 시간 없음";
  if (t.kind === "item") return `문항당 ${t.sec}초`;
  const m = Math.floor(t.sec / 60), s = t.sec % 60;
  return `총 ${m ? `${m}분` : ""}${s ? ` ${s}초` : ""}`.replace(/\s+/g, " ").trim();
}

/** 시험 규칙 목록 (시작 전 확인 카드) */
export function presetRules(preset) {
  if (!preset) return [];
  const out = [];
  if (preset.n > 0) out.push(`${preset.n}문항 · ${describeTimer(preset)}`);
  const t = preset.timer || {};
  if (t.kind === "total") out.push(t.soft ? "시간이 끝나면 알려 드려요. 제출 전까지 답을 고칠 수 있어요." : "시간이 끝나면 그때까지 쓴 답으로 제출해요.");
  if (t.kind === "item") out.push("답을 내면 바로 다음 문제로 넘어가요. 시간이 지나면 그 문항은 오답으로 처리돼요.");
  if (t.kind === "none") out.push("언제든 이전 문제로 돌아가 답을 고칠 수 있어요.");
  if (preset.pointsMode === "scaled100") out.push("문항마다 배점이 있고, 100점 만점으로 환산해요.");
  else if (preset.pointsMode === "points") out.push("문항마다 배점이 있어요. 배점 합이 점수예요.");
  else out.push("맞힌 문항 수가 점수예요.");
  if (preset.difficultyMax) out.push(`난이도 ${preset.difficultyMax} 이하의 문항을 우선 출제해요.`);
  if (preset.mixed) out.push("난이도 1~5 를 고루 섞어 출제해요.");
  if (preset.scope === "unit") out.push("단원 전체의 개념에서 골고루 나와요.");
  return out;
}

// ── 출제 계획 ─────────────────────────────────────────────────────────────────
/** [예고] true 로 바꾸면 각 fetch 옵션에 testType 이 붙는다 (items.js applyFilters 가 testType 을 지원해야 함) */
export const SELECT_BY_TEST_TYPE = false;
export const DEFAULT_QTYPES = ["choice", "short"];

/**
 * 시험 하나를 위한 fetchLiveItems 옵션 목록 (우선순위 순).
 *   scope: { kind: "unit"|"concept", id }
 *   stage "primary" 는 항상, "fill" 은 primary 를 합쳐도 n 에 모자랄 때만 부른다.
 * 출제 풀 규칙은 이 함수 한 곳에서만 정한다.
 */
export function fetchPlan(preset, scope = {}) {
  if (!preset || !(preset.n > 0)) return [];
  const n = preset.n;
  const base = scope?.kind === "concept" ? { conceptId: scope.id } : { unitId: scope?.id };
  const qtypes = Array.isArray(preset.qtypes) && preset.qtypes.length ? preset.qtypes.slice() : DEFAULT_QTYPES.slice();
  const plans = [];
  if (preset.difficultyMax) {
    for (let d = 1; d <= preset.difficultyMax; d++) plans.push({ ...base, qtypes, difficulty: d, n, pool: n * 3, stage: "primary" });
    plans.push({ ...base, qtypes, n, pool: n * 3, stage: "fill" });
  } else if (preset.mixed) {
    const per = Math.max(1, Math.ceil(n / 5));
    for (let d = 1; d <= 5; d++) plans.push({ ...base, qtypes, difficulty: d, n: per, pool: per * 3, stage: "primary" });
    plans.push({ ...base, qtypes, n, pool: n * 3, stage: "fill" });
  } else {
    plans.push({ ...base, qtypes, n, pool: n * 3, stage: "primary" });
  }
  if (SELECT_BY_TEST_TYPE) for (const p of plans) p.testType = preset.code;
  return plans;
}

// ── 문항 선발 ─────────────────────────────────────────────────────────────────
export function dedupeById(list) {
  const seen = new Set(), out = [];
  for (const it of list || []) {
    if (!it || it.id == null || seen.has(it.id)) continue;
    seen.add(it.id); out.push(it);
  }
  return out;
}

export function shuffleWith(list, rng = Math.random) {
  const a = (list || []).slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** 같은 템플릿이 몰리지 않게 — 템플릿당 최대 perTpl 개 (items.js diversify 와 같은 규칙) */
export function diversify(items, n, perTpl = 2) {
  const out = [], cnt = {};
  for (const it of items || []) {
    const k = it.template_id || it.math_key || it.id;
    if ((cnt[k] || 0) >= perTpl) continue;
    cnt[k] = (cnt[k] || 0) + 1;
    out.push(it);
    if (out.length >= n) break;
  }
  if (out.length < n) {
    const have = new Set(out);
    for (const it of items || []) { if (out.length >= n) break; if (!have.has(it)) { out.push(it); have.add(it); } }
  }
  return out;
}

/** 프리셋이 선호하는 문항인가 (난이도 상한 · 유형) */
export function prefers(preset, item) {
  if (!item) return false;
  if (preset?.difficultyMax && !(Number(item.difficulty) <= preset.difficultyMax)) return false;
  const qt = Array.isArray(preset?.qtypes) && preset.qtypes.length ? preset.qtypes : null;
  if (qt && !qt.includes(String(item.qtype || "").toLowerCase())) return false;
  return true;
}

/**
 * 후보 문항들에서 시험 문항을 고른다.
 *   선호 문항(prefers) 먼저, 모자라면 나머지로 채운다. 템플릿 분산(diversify). n 을 넘지 않는다.
 *   order:"difficulty" 프리셋은 쉬운 문항부터 배열한다.
 * 반환 { items, short, relaxed }  short = 요청 n 보다 모자란 수, relaxed = 선호 조건 밖 문항이 섞임
 */
export function buildSelection(preset, items, rng = Math.random) {
  const n = Math.max(1, Number(preset?.n) || 1);
  const list = dedupeById(items);
  const pref = list.filter((it) => prefers(preset, it));
  const rest = list.filter((it) => !prefers(preset, it));
  let picked = diversify(shuffleWith(pref, rng), n);
  let relaxed = false;
  if (picked.length < n && rest.length) {
    const fill = diversify(shuffleWith(rest, rng), n - picked.length);
    if (fill.length) { picked = picked.concat(fill); relaxed = true; }
  }
  picked = picked.slice(0, n);
  if (preset?.order === "difficulty") {
    picked = picked.map((it, i) => [it, i]).sort((a, b) => (Number(a[0].difficulty) || 0) - (Number(b[0].difficulty) || 0) || a[1] - b[1]).map((x) => x[0]);
  }
  return { items: picked, short: Math.max(0, n - picked.length), relaxed };
}

// ── 답 상태 · 채점 ───────────────────────────────────────────────────────────
// answer 항목: { sel: 보기 번호(0부터)|null, text: 단답 입력 }
export const emptyAnswer = () => ({ sel: null, text: "" });

export function isAnswered(item, a) {
  if (!a) return false;
  if (kindOf(item) === "choice") return Number.isInteger(a.sel) && a.sel >= 0;
  return String(a.text ?? "").trim() !== "";
}

export const answeredCount = (items = [], answers = []) => items.reduce((s, it, i) => s + (isAnswered(it, answers[i]) ? 1 : 0), 0);

/**
 * 제출 채점 — 문항 순서대로 빽빽한 결과 배열을 만든다 (무응답도 항목이 있다).
 * 결과 항목: { item, correct, skipped, rawAnswer, chosenIndex, chosenChoice, elapsedSec, tag }
 */
export function judgeAll(items = [], answers = [], elapsed = []) {
  return (items || []).map((item, i) => {
    const a = answers?.[i];
    const el = Math.max(0, Math.round(Number(elapsed?.[i]) || 0));
    const blank = { item, correct: false, skipped: true, rawAnswer: null, chosenIndex: null, chosenChoice: null, elapsedSec: el, tag: null };
    if (!item) return blank;
    if (kindOf(item) === "choice") {
      const ci = Number.isInteger(a?.sel) ? a.sel : null;
      const ch = ci != null ? item.choices?.[ci] : undefined;
      if (ch == null) return blank;
      const correct = isChoiceCorrect(item, ci);
      return { item, correct, skipped: false, rawAnswer: String(ch), chosenIndex: ci, chosenChoice: ch, elapsedSec: el, tag: correct ? null : distractorTag(item, ch) };
    }
    const t = String(a?.text ?? "").trim();
    if (!t) return blank;
    return { item, correct: isCorrect(item, t), skipped: false, rawAnswer: t, chosenIndex: null, chosenChoice: null, elapsedSec: el, tag: null };
  });
}

/** 문항 배점 — points 가 없으면 1 */
export function itemPoints(item) {
  const p = Number(item?.points);
  return Number.isFinite(p) && p > 0 ? p : 1;
}

/**
 * 점수 — pointsMode 에 따라
 *   count      score = 정답 수, max = 문항 수
 *   points     score = 맞힌 문항 배점 합, max = 전체 배점 합
 *   scaled100  score = 배점 합을 100점 만점으로 환산(반올림), max = 100 (raw/rawMax 에 배점 합)
 * 반환 { correct_n, n, score, max, pct, raw, rawMax }   (null 항목은 문항이 아니므로 뺀다)
 */
export function scoreRun(preset, results = []) {
  const list = Array.isArray(results) ? results.filter(Boolean) : [];
  const n = list.length;
  const correct_n = list.filter((r) => r.correct === true).length;
  const mode = preset?.pointsMode || "count";
  const pct = n ? Math.round((correct_n / n) * 100) : 0;
  if (mode !== "points" && mode !== "scaled100") return { correct_n, n, score: correct_n, max: n, pct, raw: correct_n, rawMax: n };
  const rawMax = list.reduce((s, r) => s + itemPoints(r.item), 0);
  const raw = list.reduce((s, r) => s + (r.correct === true ? itemPoints(r.item) : 0), 0);
  if (mode === "points") return { correct_n, n, score: raw, max: rawMax, pct, raw, rawMax };
  return { correct_n, n, score: rawMax ? Math.round((raw / rawMax) * 100) : 0, max: 100, pct, raw, rawMax };
}

/** 결과 한 줄 격려 — 범위(개념/단원) 표현 · 무응답이 있으면 시간 안배 힌트 */
export function examMessage(preset, s, unanswered = 0) {
  const n = Number(s?.n) || 0;
  if (!n) return "푼 문항이 없어요.";
  const p = Number(s?.pct) || 0;
  const where = preset?.scope === "concept" ? "이 개념" : "이 단원";
  let msg = p >= 90 ? `훌륭해요! ${where}은 자신 있게 넘어가도 좋아요.`
    : p >= 70 ? "잘했어요. 틀린 문제만 한 번 더 보면 충분해요."
    : p >= 50 ? "절반 넘게 맞혔어요. 해설을 보고 틀린 문제를 다시 풀어 보세요."
    : `아직 낯선 범위예요. ${where}의 개념을 다시 읽고 쉬운 문항부터 도전해 봐요.`;
  const u = Number(unanswered) || 0;
  if (u > 0 && preset?.timer?.kind && preset.timer.kind !== "none") msg += ` 무응답 ${u}문항은 오답으로 채점됐어요. 시간 안배를 연습해 봐요.`;
  else if (u > 0) msg += ` 무응답 ${u}문항은 오답으로 채점됐어요.`;
  return msg;
}

/** 점수 표시 문자열 — "12 / 20" · "38 / 45점" · "85점" */
export function scoreText(preset, s) {
  if (!s) return "";
  const mode = preset?.pointsMode || "count";
  if (mode === "points") return `${s.score} / ${s.max}점`;
  if (mode === "scaled100") return `${s.score}점`;
  return `${s.correct_n} / ${s.n}`;
}

// ── 타이머 ───────────────────────────────────────────────────────────────────
const pad2 = (v) => String(v).padStart(2, "0");

/** 초 → "mm:ss" (한 시간 이상이면 "h:mm:ss", 음수면 앞에 "-") */
export function fmtTimer(sec) {
  const v = Number(sec);
  const s = Number.isFinite(v) ? Math.trunc(v) : 0;
  const a = Math.abs(s);
  const h = Math.floor(a / 3600), m = Math.floor((a % 3600) / 60), r = a % 60;
  return (s < 0 ? "-" : "") + (h ? `${h}:${pad2(m)}:${pad2(r)}` : `${pad2(m)}:${pad2(r)}`);
}

/**
 * 남은 시간(초, 올림) — total 은 시험 시작 기준, item 은 문항 진입 기준. none 이면 null.
 * 음수면 그만큼 초과한 것.
 */
export function remainingSec(preset, { startedAt, enteredAt, now = Date.now() } = {}) {
  const t = preset?.timer;
  if (!t || t.kind === "none" || !(t.sec > 0)) return null;
  const from = t.kind === "item" ? enteredAt : startedAt;
  if (!Number.isFinite(Number(from))) return null;
  return Math.ceil((Number(from) + t.sec * 1000 - now) / 1000);
}

/** 남은 시간이 얼마 안 남았는가 (60초 이하 또는 전체의 10% 이하) */
export function isTimerWarn(preset, remaining) {
  const t = preset?.timer;
  if (remaining == null || !t || !(t.sec > 0)) return false;
  if (t.kind === "item") return remaining <= Math.max(3, Math.ceil(t.sec * 0.25));
  return remaining <= Math.max(60, Math.ceil(t.sec * 0.1));
}

// ── 응시 기록 ─────────────────────────────────────────────────────────────────
export const newRunId = (code, now = Date.now()) => `test:${code || "misc"}:${Number(now).toString(36)}`;

const toIso = (ms) => {
  const v = Number(ms);
  if (!Number.isFinite(v) || v <= 0) return null;
  try { return new Date(v).toISOString(); } catch { return null; }
};
const uniq = (list) => [...new Set((list || []).filter((x) => x != null && x !== ""))];

/**
 * test_runs 행 만들기.
 *   ctx: { unitId, conceptId, scopeTitle, startedAt(ms), finishedAt(ms), elapsedSec?, timedOut?, overtimeSec?, short?, runId? }
 *   results: judgeAll() 결과 (빽빽한 배열)
 */
export function runToRow(uid, preset, ctx = {}, results = []) {
  const list = (results || []).filter(Boolean);
  const s = scoreRun(preset, list);
  const startedAt = Number(ctx.startedAt) || null;
  const finishedAt = Number(ctx.finishedAt) || Date.now();
  const elapsedSec = Number.isFinite(Number(ctx.elapsedSec)) ? Math.max(0, Math.round(Number(ctx.elapsedSec)))
    : startedAt ? Math.max(0, Math.round((finishedAt - startedAt) / 1000))
    : list.reduce((a, r) => a + (Number(r.elapsedSec) || 0), 0);
  const unitId = ctx.unitId || list.find((r) => r.item?.unit_id)?.item?.unit_id || null;
  const conceptIds = uniq([ctx.conceptId, ...list.flatMap((r) => (Array.isArray(r.item?.concept_ids) ? r.item.concept_ids : []))]);
  const timer = { ...(preset?.timer || { kind: "none", sec: 0 }) };
  if (ctx.timedOut) timer.timed_out = true;
  if (ctx.overtimeSec > 0) timer.overtime_sec = Math.round(ctx.overtimeSec);
  return {
    user_id: uid || null,
    test_type: preset?.code || "concept_set",
    unit_id: unitId,
    concept_ids: conceptIds,
    item_ids: list.map((r) => r.item?.id).filter((x) => x != null),
    answers: list.map((r) => {
      const a = { item_id: r.item?.id ?? null, answer: r.rawAnswer == null ? null : String(r.rawAnswer).slice(0, 500), correct: r.correct === true, elapsed_sec: Math.max(0, Math.round(Number(r.elapsedSec) || 0)) };
      if (Number.isInteger(r.chosenIndex)) a.chosen_index = r.chosenIndex + 1;
      return a;
    }),
    n: s.n, correct_n: s.correct_n, score: s.score, max: s.max,
    started_at: toIso(startedAt), finished_at: toIso(finishedAt), elapsed_sec: elapsedSec,
    meta: {
      timer,
      preset: { code: preset?.code, name: preset?.name, n: preset?.n, scope: preset?.scope, pointsMode: preset?.pointsMode || "count" },
      scope: { kind: ctx.conceptId ? "concept" : "unit", id: ctx.conceptId || unitId || null, title: ctx.scopeTitle || null },
      short: Math.max(0, Number(ctx.short) || 0),
      run_id: ctx.runId || null,
      ...(preset?.pointsMode === "scaled100" ? { raw: s.raw, raw_max: s.rawMax } : {}),
    },
  };
}

// ── 로컬 보관 (test_runs 에 못 넣었을 때) ────────────────────────────────────
export const RUNS_KEY = "ash.test.runs";
export const RUNS_KEEP = 30;

function store() {
  try { return typeof globalThis !== "undefined" && globalThis.localStorage ? globalThis.localStorage : null; } catch { return null; }
}

export function loadRunsLocal() {
  const st = store();
  if (!st) return [];
  try {
    const raw = st.getItem(RUNS_KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list.filter((r) => r && typeof r === "object") : [];
  } catch { return []; }
}

/** 최근 RUNS_KEEP 건만, 최신이 앞 */
export function saveRunLocal(row, now = Date.now()) {
  if (!row || typeof row !== "object") return null;
  const rec = { ...row, id: row.id || `local:${Number(now).toString(36)}${Math.random().toString(36).slice(2, 6)}`, local: true };
  const list = [rec, ...loadRunsLocal().filter((r) => r.id !== rec.id)].slice(0, RUNS_KEEP);
  const st = store();
  if (st) { try { st.setItem(RUNS_KEY, JSON.stringify(list)); } catch { /* 저장 공간 부족 등 — 침묵 */ } }
  return rec;
}

/** DB 행 + 로컬 행을 합쳐 최신순 (같은 id 는 한 번) */
export function mergeRuns(dbRows = [], localRows = [], limit = 10) {
  const seen = new Set(), out = [];
  for (const r of [...(dbRows || []), ...(localRows || [])]) {
    if (!r || r.id == null || seen.has(String(r.id))) continue;
    seen.add(String(r.id)); out.push(r);
  }
  out.sort((a, b) => (Date.parse(b.finished_at || "") || 0) - (Date.parse(a.finished_at || "") || 0));
  return out.slice(0, Math.max(0, limit));
}

/** 최근 응시 한 줄 — { name, scope, score, when } */
export function describeRun(row, unitNames = {}) {
  const preset = presetOf(row?.test_type) || { name: row?.test_type || "시험", pointsMode: "count" };
  const meta = row?.meta && typeof row.meta === "object" ? row.meta : {};
  const scopeTitle = meta.scope?.title || unitNames[row?.unit_id] || row?.unit_id || "";
  const s = { correct_n: Number(row?.correct_n) || 0, n: Number(row?.n) || 0, score: Number(row?.score) || 0, max: Number(row?.max) || 0 };
  const mode = meta.preset?.pointsMode || preset.pointsMode;
  return {
    name: preset.name, scope: scopeTitle, mode,
    score: scoreText({ pointsMode: mode }, s),
    when: row?.finished_at || null,
    local: !!row?.local,
    link: `#/solve/test/${preset.code || row?.test_type}${meta.scope?.id ? `/${encodeURIComponent(meta.scope.id)}` : row?.unit_id ? `/${encodeURIComponent(row.unit_id)}` : ""}`,
  };
}
