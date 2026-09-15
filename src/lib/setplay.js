// ashrain.out — 세트 풀기(ItemPlay) 순수 도우미
// React·Supabase·DOM 에 의존하지 않는다 (node 테스트: tests/itemplay.test.mjs).
// 세트 구성 · 채점 요약 · 오개념 묶기 · 답 표시 문자열 · 설정/최근 결과 저장 키.

import { CIRCLED, correctChoiceIndex, displayAnswer, kindOf } from "./answers.js";
import { distractorTag, mcLabel } from "./misconceptions.js";
import { renderText } from "./mathir.js";

// ── 설정 선택지 ───────────────────────────────────────────────────────────────
export const N_OPTIONS = [5, 10, 20];
export const QTYPE_OPTIONS = [
  { key: "all", label: "전체", qtypes: ["choice", "short"] },
  { key: "choice", label: "객관식", qtypes: ["choice"] },
  { key: "short", label: "단답", qtypes: ["short"] },
];
export const BAND_OPTIONS = [
  { key: "all", label: "전체", sub: null, levels: null },
  { key: "easy", label: "쉬움", sub: "1-2", levels: [1, 2] },
  { key: "mid", label: "보통", sub: "3", levels: [3] },
  { key: "hard", label: "어려움", sub: "4-5", levels: [4, 5] },
];
export const DEFAULT_CONFIG = { n: 10, qtype: "all", band: "all" };

export const bandLevels = (key) => BAND_OPTIONS.find((b) => b.key === key)?.levels ?? null;
export const qtypesOf = (key) => QTYPE_OPTIONS.find((q) => q.key === key)?.qtypes ?? QTYPE_OPTIONS[0].qtypes;

/** 난이도 구간에 드는 문항인가 (구간이 "전체"면 항상 true) */
export function inBand(item, key) {
  const lv = bandLevels(key);
  if (!lv) return true;
  return lv.includes(Number(item?.difficulty));
}

/** 저장된/외부 설정을 안전한 값으로 (모르는 값은 기본값) */
export function normalizeConfig(raw) {
  const c = raw && typeof raw === "object" ? raw : {};
  return {
    n: N_OPTIONS.includes(Number(c.n)) ? Number(c.n) : DEFAULT_CONFIG.n,
    qtype: QTYPE_OPTIONS.some((q) => q.key === c.qtype) ? c.qtype : DEFAULT_CONFIG.qtype,
    band: BAND_OPTIONS.some((b) => b.key === c.band) ? c.band : DEFAULT_CONFIG.band,
  };
}

// ── 세트 구성 ─────────────────────────────────────────────────────────────────
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

/**
 * 세트 구성.
 *  primary  조건(난이도 등)에 맞는 후보들 — 여기서 n개를 고른다
 *  fallback 조건을 푼 후보들 — primary 가 모자랄 때만 채운다 (relaxed=true)
 *  diversify(list, k) 템플릿 분산 함수 (items.js 의 diversify 를 넘긴다; 없으면 앞에서 k개)
 * 반환 { items, relaxed, short }  short = 요청 n 보다 모자란 수
 */
export function assembleSet({ primary = [], fallback = [], n = 10, diversify = null, rng = Math.random } = {}) {
  const want = Math.max(1, Number(n) || 1);
  const pick = typeof diversify === "function" ? diversify : (list, k) => list.slice(0, k);
  let items = pick(shuffleWith(dedupeById(primary), rng), want).slice(0, want);
  let relaxed = false;
  if (items.length < want && fallback?.length) {
    const have = new Set(items.map((x) => x.id));
    const extra = shuffleWith(dedupeById(fallback).filter((x) => !have.has(x.id)), rng);
    const fill = pick(extra, want - items.length).slice(0, want - items.length);
    if (fill.length) { items = items.concat(fill); relaxed = true; }
  }
  return { items, relaxed, short: Math.max(0, want - items.length) };
}

export const newSetId = (conceptId, now = Date.now()) => `set:${conceptId || "misc"}:${Number(now).toString(36)}`;

// ── 결과 요약 ─────────────────────────────────────────────────────────────────
// result 항목: { item, correct, rawAnswer, chosenIndex, chosenChoice, elapsedSec, tag, skipped }

export function summarizeResults(results = [], n = results.length) {
  const list = results.filter(Boolean);
  const ok = list.filter((r) => r.correct === true).length;
  const totalSec = list.reduce((s, r) => s + (Number(r.elapsedSec) || 0), 0);
  const wrongIdx = [];
  for (let i = 0; i < n; i++) if (!results[i] || results[i].correct !== true) wrongIdx.push(i);
  return { n, answered: list.length, ok, pct: n ? Math.round((ok / n) * 100) : 0, totalSec: Math.round(totalSec), wrongIdx };
}

/** 점수(%)에 따른 한 줄 격려 */
export function resultMessage(pct, n = 1) {
  if (!n) return "푼 문항이 없어요.";
  const p = Number(pct) || 0;
  if (p >= 100) return "완벽해요! 이 개념은 자신 있게 넘어가도 좋아요.";
  if (p >= 80) return "잘했어요! 틀린 문제만 한 번 더 보면 충분해요.";
  if (p >= 50) return "절반 넘게 맞혔어요. 해설을 보고 틀린 문제를 다시 풀어 보세요.";
  return "아직 낯선 개념이에요. 개념을 다시 읽고 쉬운 난이도부터 도전해 봐요.";
}

/** 틀린 문항을 오개념 코드별로 묶는다 → [{ tag, label, count, idx }] (많은 순) */
export function groupMisconceptions(results = []) {
  const map = new Map();
  results.forEach((r, i) => {
    if (!r || r.correct === true) return;
    const tag = r.tag || distractorTag(r.item, r.chosenChoice);
    if (!tag) return;
    const g = map.get(tag) || { tag, label: mcLabel(tag), count: 0, idx: [] };
    g.count += 1; g.idx.push(i);
    map.set(tag, g);
  });
  return [...map.values()].sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag));
}

/** 오답노트 저장용 항목 — 틀린(또는 건너뛴) 문항만 */
export function wrongEntries(results = []) {
  return results
    .filter((r) => r && r.item && r.correct !== true)
    .map((r) => ({ item: r.item, myAnswer: r.chosenChoice ?? r.rawAnswer ?? null, tag: r.tag || distractorTag(r.item, r.chosenChoice) || null }));
}

// ── 표시 문자열 ───────────────────────────────────────────────────────────────
/** 정답 표시 — 객관식은 "② 31", 단답은 마커를 읽기 좋게 */
export function correctAnswerText(item) {
  if (kindOf(item) === "choice") {
    const ci = correctChoiceIndex(item);
    if (ci >= 0) return `${CIRCLED[ci] || ci + 1} ${item.choices[ci]}`;
  }
  return displayAnswer(item?.answer);
}

/** 학생 답 표시 — 고른 보기는 "③ 39", 단답은 입력 그대로, 없으면 (무응답)/(건너뜀) */
export function myAnswerText(item, r) {
  if (!r) return "(무응답)";
  if (r.skipped) return "(건너뜀)";
  const ci = r.chosenIndex;
  if (ci != null && item?.choices?.[ci] != null) return `${CIRCLED[ci] || ci + 1} ${item.choices[ci]}`;
  const raw = String(r.rawAnswer ?? "").trim();
  return raw || "(무응답)";
}

/** 문제 첫머리 미리보기 — 마커를 읽는 글로, 공백 정리, max 글자 */
export function questionPreview(text, max = 70) {
  let t = String(text ?? "");
  try { t = renderText(t); } catch { t = t.replace(/\[\[|\]\]/g, ""); }
  t = t.replace(/\s+/g, " ").trim();
  return t.length > max ? t.slice(0, Math.max(1, max - 1)) + "…" : t;
}

export function fmtClock(sec) {
  const s = Math.max(0, Math.floor(Number(sec) || 0));
  const m = Math.floor(s / 60);
  return `${String(m).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
}

// ── localStorage (호출 시점에만 접근, 실패는 조용히) ─────────────────────────
export const LAST_KEY = "ash.solve.last";      // { conceptId, title, n, ok, at }
export const CFG_KEY = "ash.solve.setcfg";     // { n, qtype, band }

function lsGet(key) {
  try { const raw = globalThis.localStorage?.getItem(key); return raw ? JSON.parse(raw) : null; } catch { return null; }
}
function lsSet(key, val) {
  try { globalThis.localStorage?.setItem(key, JSON.stringify(val)); } catch { /* 무시 */ }
}

export const readSetConfig = () => normalizeConfig(lsGet(CFG_KEY));
export const saveSetConfig = (cfg) => lsSet(CFG_KEY, normalizeConfig(cfg));
export const readLastResult = () => lsGet(LAST_KEY);
export function saveLastResult({ conceptId, title, n, ok, at = Date.now() }) {
  const rec = { conceptId: conceptId || null, title: title || null, n: Number(n) || 0, ok: Number(ok) || 0, at };
  lsSet(LAST_KEY, rec);
  return rec;
}
