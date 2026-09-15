// node tests/essay.test.mjs — 서술형 자가채점 순수 로직
import assert from "node:assert/strict";
import {
  partialPoints, fullPoints, computeScore, checkEffects, allMarked, verdict, reviewList,
  saveResult, loadResults, LS_RESULTS, RESULTS_KEEP,
} from "../src/lib/essay.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok  -", name); }
  catch (e) { failed++; console.log("FAIL-", name); console.log("      " + (e?.message || e).split("\n").join("\n      ")); }
}

// 실제 DB 의 루브릭 모양을 그대로 흉내 낸 표본
const RUBRIC = {
  total: 7,
  items: [
    { no: 1, element: "겉넓이 식 세우기", points: 3, criterion: "높이를 h로 놓고 겉넓이를 128π + 16πh 로 나타냈다.", partial: "밑넓이·옆넓이 중 하나만 옳으면 1점.", zero: "무응답 또는 그 외 오답" },
    { no: 2, element: "방정식 풀기", points: 2, criterion: "16πh = 144π 에서 h = 9 를 얻었다.", partial: "식은 옳으나 계산 실수면 1점.", zero: "무응답 또는 그 외 오답" },
    { no: 3, element: "답 쓰기", points: 2, criterion: "h = 9 cm 라고 답했다.", partial: "단위를 빠뜨렸으면 1점.", zero: "무응답 또는 그 외 오답" },
  ],
  checks: [
    { text: "겉넓이 식에서 밑면을 하나만 넣음 (64π + 16πh)", effect: "부분", element_no: 1 },
    { text: "겉넓이 대신 부피를 구함", effect: "불인정", element_no: 1 },
    { text: "단위 누락", effect: "부분", element_no: 3 },
  ],
  principles: ["예시 답안과 풀이 방법이 다르더라도 수학적으로 타당하면 정답으로 인정한다."],
};

// ── partialPoints ────────────────────────────────────────────────────────────
test("partialPoints: '…1점' 문구를 읽는다", () => {
  assert.equal(partialPoints({ points: 3, partial: "밑넓이·옆넓이 중 하나만 옳으면 1점." }), 1);
  assert.equal(partialPoints({ points: 4, partial: "기울기만 옳으면 2점, 대입 실수로 b가 틀렸으면 2점." }), 2);
  assert.equal(partialPoints({ points: 5, partial: "식만 세웠으면 2 점." }), 2);
});
test("partialPoints: 문구에 점수가 없으면 max(1, floor(points/2))", () => {
  assert.equal(partialPoints({ points: 3, partial: "지수를 더해 [[pow(a, 6)]]으로 썼으면 인정하지 않는다." }), 1);
  assert.equal(partialPoints({ points: 4, partial: "인정하지 않는다." }), 2);
  assert.equal(partialPoints({ points: 5 }), 2);
  assert.equal(partialPoints({ points: 1, partial: "" }), 1);
  assert.equal(partialPoints({ points: 2, partial: null }), 1);
});
test("partialPoints: 배점을 넘지 않고, 이상한 입력에도 죽지 않는다", () => {
  assert.equal(partialPoints({ points: 2, partial: "잘했으면 9점" }), 2);
  assert.equal(partialPoints({ points: 0, partial: "1점" }), 0);
  assert.equal(partialPoints({}), 0);
  assert.equal(partialPoints(null), 0);
  assert.equal(partialPoints({ points: "3", partial: "하나만 옳으면 1점" }), 1);
  assert.equal(fullPoints({ points: "abc" }), 0);
});

// ── computeScore ─────────────────────────────────────────────────────────────
test("computeScore: 전부 정확 → 만점", () => {
  const s = computeScore(RUBRIC, { 1: "full", 2: "full", 3: "full" }, new Set());
  assert.equal(s.max, 7);
  assert.equal(s.total, 7);
  assert.deepEqual(s.perElement.map((e) => e.got), [3, 2, 2]);
  assert.deepEqual(s.perElement.map((e) => e.no), [1, 2, 3]);
});
test("computeScore: 부분/0점 반영", () => {
  const s = computeScore(RUBRIC, { 1: "partial", 2: "zero", 3: "full" }, []);
  assert.equal(s.total, 1 + 0 + 2);
  assert.equal(s.perElement[0].reason, "부분");
  assert.equal(s.perElement[1].reason, "0점");
  assert.equal(s.perElement[2].mark, "full");
});
test("computeScore: 표시하지 않은 요소는 0점", () => {
  const s = computeScore(RUBRIC, { 1: "full" }, new Set());
  assert.equal(s.total, 3);
  assert.equal(s.perElement[1].got, 0);
  assert.equal(s.perElement[1].mark, "zero");
  assert.equal(computeScore(RUBRIC, {}, new Set()).total, 0);
  assert.equal(computeScore(RUBRIC, undefined, undefined).total, 0);
  assert.equal(computeScore(RUBRIC, { 1: "banana" }).perElement[0].got, 0);
});
test("computeScore: 문자열 키 marks 도 받는다", () => {
  const s = computeScore(RUBRIC, { "1": "full", "2": "partial", "3": "zero" });
  assert.equal(s.total, 4);
});
test("computeScore: 불인정 체크 → 해당 요소 0점", () => {
  const s = computeScore(RUBRIC, { 1: "full", 2: "full", 3: "full" }, new Set([1]));
  assert.equal(s.perElement[0].got, 0);
  assert.equal(s.perElement[0].reason, "실수거리 → 불인정");
  assert.equal(s.total, 4);
  // 다른 요소는 그대로
  assert.equal(s.perElement[1].got, 2);
  assert.equal(s.perElement[2].got, 2);
});
test("computeScore: 부분 체크 → 부분 점수 상한", () => {
  const s = computeScore(RUBRIC, { 1: "full", 2: "full", 3: "full" }, [0]);
  assert.equal(s.perElement[0].got, 1);
  assert.equal(s.perElement[0].reason, "실수거리 → 부분 인정");
  assert.equal(s.total, 5);
  // 이미 부분/0점이면 더 깎지 않는다
  const s2 = computeScore(RUBRIC, { 1: "partial", 2: "full", 3: "zero" }, [0, 2]);
  assert.equal(s2.perElement[0].got, 1);
  assert.equal(s2.perElement[0].reason, "부분");
  assert.equal(s2.perElement[2].got, 0);
  assert.equal(s2.perElement[2].reason, "0점");
});
test("computeScore: 같은 요소에 부분+불인정이면 불인정이 이긴다", () => {
  const s = computeScore(RUBRIC, { 1: "full", 2: "full", 3: "full" }, [0, 1]);
  assert.equal(s.perElement[0].got, 0);
  assert.equal(s.total, 4);
  assert.deepEqual(checkEffects(RUBRIC, [0, 1, 2]), { 1: "zero", 3: "partial" });
});
test("computeScore: 합계는 만점을 넘지 않는다", () => {
  const weird = { total: 3, items: [{ no: 1, points: 2, partial: "5점" }, { no: 2, points: 1, partial: "9점" }] };
  const s = computeScore(weird, { 1: "partial", 2: "partial" });
  assert.equal(s.max, 3);
  assert.equal(s.total, 3);
  assert.ok(s.total <= s.max);
  for (const e of s.perElement) assert.ok(e.got <= e.points && e.got >= 0);
});
test("computeScore: 필드가 빠진 루브릭에도 죽지 않는다", () => {
  const r = { items: [{ no: 1, element: "식", points: 2 }, { no: 2, points: 3, partial: null, zero: undefined }] };
  const s = computeScore(r, { 1: "partial", 2: "full" }, new Set([0, 5]));
  assert.equal(s.max, 5);
  assert.equal(s.total, 1 + 3);
  assert.deepEqual(computeScore(null), { total: 0, max: 0, perElement: [] });
  assert.deepEqual(computeScore({}), { total: 0, max: 0, perElement: [] });
  assert.equal(computeScore({ total: 6 }).max, 6);
  // checks 의 element_no 가 없거나 이상해도 무시
  const r2 = { ...RUBRIC, checks: [{ text: "x", effect: "불인정" }, { text: "y", effect: "부분", element_no: 99 }, null, { text: "z", effect: "이상함", element_no: 1 }] };
  const s2 = computeScore(r2, { 1: "full", 2: "full", 3: "full" }, [0, 1, 2, 3]);
  assert.equal(s2.total, 7);
  // no 가 없는 요소는 순번으로
  const r3 = { items: [{ points: 2 }, { points: 3 }] };
  assert.equal(computeScore(r3, { 1: "full", 2: "full" }).total, 5);
});

// ── allMarked / verdict / reviewList ─────────────────────────────────────────
test("allMarked", () => {
  assert.equal(allMarked(RUBRIC, { 1: "full", 2: "zero", 3: "partial" }), true);
  assert.equal(allMarked(RUBRIC, { 1: "full", 2: "zero" }), false);
  assert.equal(allMarked(RUBRIC, {}), false);
  assert.equal(allMarked({ items: [] }, {}), true);
  assert.equal(allMarked(null, {}), true);
});
test("verdict", () => {
  assert.equal(verdict(7, 7), "만점이에요");
  assert.equal(verdict(5, 7), "거의 다 왔어요");
  assert.equal(verdict(4, 7), "핵심 요소를 다시 봐요");
  assert.equal(verdict(0, 7), "핵심 요소를 다시 봐요");
  assert.equal(verdict(0, 0), "핵심 요소를 다시 봐요");
  assert.equal(verdict(NaN, undefined), "핵심 요소를 다시 봐요");
});
test("reviewList: 만점이 아닌 요소만, 기준 문구와 함께", () => {
  const s = computeScore(RUBRIC, { 1: "partial", 2: "full", 3: "zero" });
  const rv = reviewList(RUBRIC, s);
  assert.deepEqual(rv.map((x) => x.no), [1, 3]);
  assert.equal(rv[0].criterion, RUBRIC.items[0].criterion);
  assert.equal(rv[0].element, "겉넓이 식 세우기");
  assert.equal(rv[1].got, 0);
  assert.deepEqual(reviewList(RUBRIC, computeScore(RUBRIC, { 1: "full", 2: "full", 3: "full" })), []);
  assert.deepEqual(reviewList(null, null), []);
});

// ── localStorage 보관 ────────────────────────────────────────────────────────
test("save/loadResults: 저장소가 없으면 조용히 넘어간다", () => {
  delete globalThis.localStorage;
  assert.deepEqual(loadResults(), []);
  const out = saveResult({ itemId: "a", total: 1, max: 2 });
  assert.equal(out.length, 1);                 // 돌려주는 목록에는 들어 있지만
  assert.equal(out[0].itemId, "a");
  assert.ok(typeof out[0].at === "string");
  assert.deepEqual(loadResults(), []);         // 저장은 되지 않는다
  assert.deepEqual(saveResult(null), []);
});
test("save/loadResults: 최신 먼저, 50건만 남긴다", () => {
  const mem = {};
  globalThis.localStorage = {
    getItem: (k) => (k in mem ? mem[k] : null),
    setItem: (k, v) => { mem[k] = String(v); },
    removeItem: (k) => { delete mem[k]; },
  };
  assert.deepEqual(loadResults(), []);
  saveResult({ itemId: "i1", snippet: "첫 문항", total: 5, max: 7, correct: true });
  saveResult({ itemId: "i2", snippet: "둘째 문항", total: 7, max: 7, correct: true, at: "2026-09-14T00:00:00.000Z" });
  const l = loadResults();
  assert.equal(l.length, 2);
  assert.equal(l[0].itemId, "i2");
  assert.equal(l[0].at, "2026-09-14T00:00:00.000Z");
  assert.ok(typeof l[1].at === "string" && !Number.isNaN(Date.parse(l[1].at)));
  for (let i = 0; i < 60; i++) saveResult({ itemId: "x" + i, total: i % 8, max: 7 });
  const all = loadResults();
  assert.equal(all.length, RESULTS_KEEP);
  assert.equal(all[0].itemId, "x59");
  assert.equal(JSON.parse(mem[LS_RESULTS]).length, RESULTS_KEEP);
  // 깨진 저장값은 빈 목록
  mem[LS_RESULTS] = "{not json";
  assert.deepEqual(loadResults(), []);
  mem[LS_RESULTS] = JSON.stringify([null, 1, { itemId: "ok" }]);
  assert.deepEqual(loadResults(), [{ itemId: "ok" }]);
  // setItem 이 던져도 죽지 않는다
  globalThis.localStorage.setItem = () => { throw new Error("quota"); };
  assert.ok(Array.isArray(saveResult({ itemId: "q" })));
  delete globalThis.localStorage;
});

console.log(`\n${n - failed}/${n} passed`);
if (failed) process.exit(1);
