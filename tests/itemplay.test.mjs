// node tests/itemplay.test.mjs — 세트 풀기 순수 도우미(src/lib/setplay.js) 검사
import assert from "node:assert/strict";
import {
  N_OPTIONS, QTYPE_OPTIONS, BAND_OPTIONS, DEFAULT_CONFIG, bandLevels, qtypesOf, inBand, normalizeConfig,
  dedupeById, shuffleWith, assembleSet, newSetId,
  summarizeResults, groupMisconceptions, wrongEntries, resultMessage,
  correctAnswerText, myAnswerText, questionPreview, fmtClock,
  LAST_KEY, CFG_KEY, saveLastResult, readLastResult, saveSetConfig, readSetConfig,
} from "../src/lib/setplay.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      ", e.message); }
}

const seq = (vals) => { let i = 0; return () => vals[i++ % vals.length]; };   // 결정적 rng
const mk = (id, extra = {}) => ({ id, unit_id: "m1-1", concept_ids: ["m1-1-01"], qtype: "short", difficulty: 3, question: `문제 ${id}`, answer: "1", ...extra });

// ── 설정 ──
test("normalizeConfig: 기본값과 유효값", () => {
  assert.deepEqual(normalizeConfig(null), DEFAULT_CONFIG);
  assert.deepEqual(normalizeConfig({ n: "20", qtype: "choice", band: "hard" }), { n: 20, qtype: "choice", band: "hard" });
  assert.deepEqual(normalizeConfig({ n: 7, qtype: "essay", band: "x" }), DEFAULT_CONFIG);
  assert.deepEqual(N_OPTIONS, [5, 10, 20]);
  assert.equal(QTYPE_OPTIONS.length, 3);
  assert.equal(BAND_OPTIONS.length, 4);
});

test("bandLevels / qtypesOf / inBand", () => {
  assert.equal(bandLevels("all"), null);
  assert.deepEqual(bandLevels("easy"), [1, 2]);
  assert.deepEqual(bandLevels("mid"), [3]);
  assert.deepEqual(bandLevels("hard"), [4, 5]);
  assert.deepEqual(qtypesOf("short"), ["short"]);
  assert.deepEqual(qtypesOf("nope"), ["choice", "short"]);
  assert.equal(inBand(mk("a", { difficulty: 2 }), "easy"), true);
  assert.equal(inBand(mk("a", { difficulty: 3 }), "easy"), false);
  assert.equal(inBand(mk("a", { difficulty: 5 }), "all"), true);
  assert.equal(inBand(null, "hard"), false);
});

// ── 세트 구성 ──
test("dedupeById / shuffleWith", () => {
  const a = mk("a"), b = mk("b");
  assert.deepEqual(dedupeById([a, b, a, null, { id: null }]).map((x) => x.id), ["a", "b"]);
  const sh = shuffleWith([1, 2, 3, 4], seq([0]));
  assert.deepEqual([...sh].sort(), [1, 2, 3, 4]);
  assert.equal(sh.length, 4);
  assert.deepEqual(shuffleWith([], Math.random), []);
});

test("assembleSet: 후보가 넉넉하면 n개, relaxed 아님", () => {
  const primary = Array.from({ length: 12 }, (_, i) => mk("p" + i));
  const r = assembleSet({ primary, n: 5, rng: seq([0.1, 0.5, 0.9]) });
  assert.equal(r.items.length, 5);
  assert.equal(r.relaxed, false);
  assert.equal(r.short, 0);
  assert.equal(new Set(r.items.map((x) => x.id)).size, 5);
});

test("assembleSet: 모자라면 fallback 으로 채우고 relaxed", () => {
  const primary = [mk("p1"), mk("p2"), mk("p2")];
  const fallback = [mk("p1"), mk("f1"), mk("f2"), mk("f3")];
  const r = assembleSet({ primary, fallback, n: 4, rng: seq([0.3]) });
  assert.equal(r.items.length, 4);
  assert.equal(r.relaxed, true);
  assert.equal(r.short, 0);
  const ids = r.items.map((x) => x.id);
  assert.ok(ids.includes("p1") && ids.includes("p2"));
  assert.equal(new Set(ids).size, 4);
});

test("assembleSet: fallback 까지 모자라면 short 를 알린다", () => {
  const r = assembleSet({ primary: [mk("a")], fallback: [mk("b")], n: 5 });
  assert.equal(r.items.length, 2);
  assert.equal(r.short, 3);
  assert.equal(r.relaxed, true);
  const e = assembleSet({ primary: [], fallback: [], n: 5 });
  assert.deepEqual(e, { items: [], relaxed: false, short: 5 });
});

test("assembleSet: diversify 함수를 통해 고른다", () => {
  const primary = [mk("a", { template_id: "T" }), mk("b", { template_id: "T" }), mk("c", { template_id: "T" }), mk("d", { template_id: "U" })];
  const onePerTpl = (list, k) => { const seen = new Set(), out = []; for (const it of list) { if (seen.has(it.template_id)) continue; seen.add(it.template_id); out.push(it); if (out.length >= k) break; } return out; };
  const r = assembleSet({ primary, n: 3, diversify: onePerTpl, rng: seq([0]) });
  assert.equal(r.items.length, 2);                     // 템플릿 2종 → 2개만
  assert.equal(r.short, 1);
});

test("newSetId 형식", () => {
  assert.equal(newSetId("m1-1-01", 1000), "set:m1-1-01:rs");
  assert.match(newSetId("m1-1-01"), /^set:m1-1-01:[0-9a-z]+$/);
  assert.match(newSetId(null, 1), /^set:misc:1$/);
});

// ── 결과 요약 ──
const results = [
  { item: mk("a"), correct: true, elapsedSec: 10 },
  { item: mk("b"), correct: false, elapsedSec: 20.4, chosenChoice: "27", tag: "MC-CALC-01" },
  null,
  { item: mk("d"), correct: false, skipped: true, elapsedSec: 0 },
];

test("summarizeResults", () => {
  const s = summarizeResults(results, 4);
  assert.equal(s.n, 4);
  assert.equal(s.answered, 3);
  assert.equal(s.ok, 1);
  assert.equal(s.pct, 25);
  assert.equal(s.totalSec, 30);
  assert.deepEqual(s.wrongIdx, [1, 2, 3]);
  assert.deepEqual(summarizeResults([], 0), { n: 0, answered: 0, ok: 0, pct: 0, totalSec: 0, wrongIdx: [] });
});

test("groupMisconceptions: 명시 tag + L42 매핑, 많은 순", () => {
  const labeled = mk("x", {
    qtype: "choice", choices: ["27", "31", "39"], answer: "31",
    labels: { L42_distractor_map: { "27": "MC-CALC-01", "39": "MC-READ-01" } },
  });
  const rs = [
    { item: labeled, correct: false, chosenChoice: "39" },          // READ via map
    { item: mk("b"), correct: false, tag: "MC-CALC-01" },            // explicit
    { item: labeled, correct: false, chosenChoice: "27" },          // CALC via map
    { item: mk("c"), correct: true, tag: "MC-CALC-01" },             // 정답은 제외
    { item: mk("d"), correct: false, chosenChoice: "zzz" },          // 태그 없음 → 제외
  ];
  const g = groupMisconceptions(rs);
  assert.equal(g.length, 2);
  assert.equal(g[0].tag, "MC-CALC-01");
  assert.equal(g[0].count, 2);
  assert.deepEqual(g[0].idx, [1, 2]);
  assert.equal(g[0].label, "단순 계산 실수");
  assert.equal(g[1].tag, "MC-READ-01");
  assert.deepEqual(groupMisconceptions([]), []);
  assert.deepEqual(groupMisconceptions([null, undefined]), []);
});

test("wrongEntries: 틀린 것만, 내 답은 보기 우선", () => {
  const w = wrongEntries(results);
  assert.equal(w.length, 2);
  assert.equal(w[0].item.id, "b");
  assert.equal(w[0].myAnswer, "27");
  assert.equal(w[0].tag, "MC-CALC-01");
  assert.equal(w[1].item.id, "d");
  assert.equal(w[1].myAnswer, null);
  assert.equal(w[1].tag, null);
});

test("resultMessage", () => {
  assert.match(resultMessage(100, 5), /완벽/);
  assert.match(resultMessage(80, 5), /잘했어요/);
  assert.match(resultMessage(50, 5), /절반/);
  assert.match(resultMessage(10, 5), /낯선/);
  assert.match(resultMessage(0, 0), /없어요/);
});

// ── 표시 문자열 ──
test("correctAnswerText: 객관식은 번호+보기, 단답은 마커 풀기", () => {
  assert.equal(correctAnswerText(mk("a", { qtype: "choice", choices: ["27", "31", "39"], answer: "31" })), "② 31");
  assert.equal(correctAnswerText(mk("a", { qtype: "choice", choices: ["27", "31", "39"], answer: "③" })), "③ 39");
  assert.equal(correctAnswerText(mk("a", { answer: "[[frac(1,2)]]" })), "1/2");
  assert.equal(correctAnswerText(mk("a", { answer: "[[deg(60)]]" })), "60°");
  assert.equal(correctAnswerText(mk("a", { answer: "합성수" })), "합성수");
  assert.equal(correctAnswerText(null), "");
});

test("myAnswerText", () => {
  const ch = mk("a", { qtype: "choice", choices: ["27", "31", "39"], answer: "31" });
  assert.equal(myAnswerText(ch, null), "(무응답)");
  assert.equal(myAnswerText(ch, { skipped: true }), "(건너뜀)");
  assert.equal(myAnswerText(ch, { chosenIndex: 2, rawAnswer: "39" }), "③ 39");
  assert.equal(myAnswerText(mk("s"), { rawAnswer: " 1/2 " }), "1/2");
  assert.equal(myAnswerText(mk("s"), { rawAnswer: "" }), "(무응답)");
});

test("questionPreview: 마커를 읽는 글로, 공백 정리, 자르기", () => {
  assert.equal(questionPreview("다음 수가 소수인지\n합성수인지 쓰시오.\n63"), "다음 수가 소수인지 합성수인지 쓰시오. 63");
  assert.equal(questionPreview("[[frac(1,2)]] 을 계산하시오"), "1/2 을 계산하시오");
  const long = questionPreview("가".repeat(100), 20);
  assert.equal(long.length, 20);
  assert.ok(long.endsWith("…"));
  assert.equal(questionPreview(null), "");
});

test("fmtClock", () => {
  assert.equal(fmtClock(0), "00:00");
  assert.equal(fmtClock(65), "01:05");
  assert.equal(fmtClock(59.9), "00:59");
  assert.equal(fmtClock(-3), "00:00");
  assert.equal(fmtClock(3600), "60:00");
  assert.equal(fmtClock("abc"), "00:00");
});

// ── localStorage (가짜 저장소) ──
test("saveLastResult / readLastResult / config 저장", () => {
  const store = new Map();
  globalThis.localStorage = { getItem: (k) => (store.has(k) ? store.get(k) : null), setItem: (k, v) => store.set(k, String(v)) };
  assert.equal(readLastResult(), null);
  const rec = saveLastResult({ conceptId: "m1-1-01", title: "소수", n: 10, ok: 7, at: 123 });
  assert.deepEqual(rec, { conceptId: "m1-1-01", title: "소수", n: 10, ok: 7, at: 123 });
  assert.deepEqual(readLastResult(), rec);
  assert.deepEqual(JSON.parse(store.get(LAST_KEY)), rec);
  saveSetConfig({ n: 5, qtype: "short", band: "bogus" });
  assert.deepEqual(readSetConfig(), { n: 5, qtype: "short", band: "all" });
  assert.ok(store.has(CFG_KEY));
  // 저장소가 죽어도 조용히
  globalThis.localStorage = { getItem: () => { throw new Error("nope"); }, setItem: () => { throw new Error("nope"); } };
  assert.equal(readLastResult(), null);
  assert.deepEqual(readSetConfig(), DEFAULT_CONFIG);
  assert.doesNotThrow(() => saveLastResult({ conceptId: "x", n: 1, ok: 1 }));
  delete globalThis.localStorage;
});

console.log(`\n${n - failed}/${n} passed`);
if (failed) process.exit(1);
