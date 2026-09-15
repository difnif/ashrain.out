// node tests/review.test.mjs — 개념 복습 모드 순수 로직(src/lib/review.js) 검사. 실패 시 exit 1.
import assert from "node:assert/strict";
import {
  CAPS, RECENT_KEY, RECENT_MAX, QUIZ_N, REWARD, DAILY_CAP, MIN_STEP_MS,
  capForRank, rankOf, normRecent,
  getRecentConcepts, pushRecentConcept, recentIds,
  unitFor, defaultConceptFor,
  checkBlockItems, pickQuiz, stripAnswers, judgeQuiz, kstDayStart,
} from "../src/lib/review.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}
const fakeStore = (init = {}) => {
  const m = { ...init };
  return { getItem: (k) => (k in m ? m[k] : null), setItem: (k, v) => { m[k] = String(v); }, dump: () => m };
};

// ── 상수 ────────────────────────────────────────────────────────────────────
test("상수 — 상한 5·3·3·2·2, 보상 10, 하루 5회, 퀴즈 3, 단락 4초", () => {
  assert.deepEqual(CAPS, [5, 3, 3, 2, 2]);
  assert.equal(REWARD, 10); assert.equal(DAILY_CAP, 5); assert.equal(QUIZ_N, 3); assert.equal(MIN_STEP_MS, 4000);
  assert.equal(RECENT_KEY, "ash.recentConcepts"); assert.equal(RECENT_MAX, 5);
});

// ── capForRank ──────────────────────────────────────────────────────────────
test("capForRank — 순위별 상한, 범위 밖은 2", () => {
  assert.deepEqual([1, 2, 3, 4, 5].map(capForRank), [5, 3, 3, 2, 2]);
  assert.equal(capForRank(6), 2); assert.equal(capForRank(99), 2);
  assert.equal(capForRank(0), 2); assert.equal(capForRank(-1), 2);
  assert.equal(capForRank("3"), 3); assert.equal(capForRank(null), 2); assert.equal(capForRank("x"), 2); assert.equal(capForRank(2.5), 2);
});

test("rankOf / normRecent — 최근 목록 순위, 없으면 5, 중복·객체·잘못된 id 정리", () => {
  assert.equal(rankOf(["a", "b", "c"], "a"), 1);
  assert.equal(rankOf(["a", "b", "c"], "c"), 3);
  assert.equal(rankOf(["a", "b", "c"], "zzz"), 5);
  assert.equal(rankOf([], "a"), 5);
  assert.equal(rankOf(null, "a"), 5);
  assert.deepEqual(normRecent(["m1-1-01", { id: "m1-1-02" }, "m1-1-01", "", null, 7, "bad id!", "m1-1-03"]), ["m1-1-01", "m1-1-02", "m1-1-03"]);
  assert.deepEqual(normRecent(["a", "b", "c", "d", "e", "f", "g"]), ["a", "b", "c", "d", "e"]);
  assert.deepEqual(normRecent("a"), []);
});

// ── 최근 읽은 개념 (가짜 localStorage) ────────────────────────────────────────
test("pushRecentConcept — 맨 앞에 넣고 중복 제거, 최대 5, 저장 형식", () => {
  const st = fakeStore();
  pushRecentConcept("m1-1-01", "소수와 합성수", st, 1000);
  pushRecentConcept("m1-1-02", "소인수분해", st, 2000);
  pushRecentConcept("m1-1-01", "소수와 합성수", st, 3000);   // 다시 읽음 → 맨 앞으로
  let l = getRecentConcepts(st);
  assert.deepEqual(l.map((x) => x.id), ["m1-1-01", "m1-1-02"]);
  assert.equal(l[0].at, 3000); assert.equal(l[0].title, "소수와 합성수");
  for (const id of ["a", "b", "c", "d"]) pushRecentConcept(id, id, st, 4000);
  l = getRecentConcepts(st);
  assert.equal(l.length, 5);
  assert.deepEqual(recentIds(l), ["d", "c", "b", "a", "m1-1-01"]);
  assert.deepEqual(recentIds(["x", { id: "y" }, null]), ["x", "y"]);
  assert.deepEqual(JSON.parse(st.dump()[RECENT_KEY]).map((x) => x.id), ["d", "c", "b", "a", "m1-1-01"]);
});

test("getRecentConcepts — 저장소 없음·깨진 JSON·이상한 항목은 안전하게", () => {
  assert.deepEqual(getRecentConcepts(fakeStore()), []);
  assert.deepEqual(getRecentConcepts(fakeStore({ [RECENT_KEY]: "{not json" })), []);
  assert.deepEqual(getRecentConcepts(fakeStore({ [RECENT_KEY]: JSON.stringify([{ id: "ok" }, { title: "no id" }, null, "str"]) })).map((x) => x.id), ["ok"]);
  assert.deepEqual(getRecentConcepts(fakeStore({ [RECENT_KEY]: JSON.stringify({ id: "obj" }) })), []);
  const bad = { getItem: () => { throw new Error("blocked"); }, setItem: () => { throw new Error("blocked"); } };
  assert.deepEqual(getRecentConcepts(bad), []);
  assert.doesNotThrow(() => pushRecentConcept("a", "A", bad));
  assert.deepEqual(pushRecentConcept("", "빈 id", fakeStore()), []);
});

// ── 첫 사용자 기본 개념 ─────────────────────────────────────────────────────
test("unitFor — 학년·학기 → 단원 id (3~8월 1학기, 9~2월 2학기), 학년 없음/초등/기타 → m1-1", () => {
  const mar = new Date(2026, 2, 5), sep = new Date(2026, 8, 15), feb = new Date(2027, 1, 20), aug = new Date(2026, 7, 31);
  assert.equal(unitFor({ grade: "중1" }, mar), "m1-1");
  assert.equal(unitFor({ grade: "중1" }, sep), "m1-2");
  assert.equal(unitFor({ grade: "중2" }, aug), "m2-1");
  assert.equal(unitFor({ grade: "중3" }, feb), "m3-2");
  assert.equal(unitFor({ grade: "고1" }, mar), "h1-1");
  assert.equal(unitFor({ grade: "고3" }, sep), "h3-2");
  assert.equal(unitFor({ grade: "초5" }, sep), "m1-1");
  assert.equal(unitFor({ grade: "기타" }, sep), "m1-1");
  assert.equal(unitFor({}, sep), "m1-1");
  assert.equal(unitFor(null, sep), "m1-1");
});

test("defaultConceptFor — 단원의 sort_order 최소 개념, 없으면 같은 학년 1학기 → m1-1 → 전체 첫 개념", () => {
  const concepts = [
    { id: "m1-1-03", unit_id: "m1-1", title: "셋", sort_order: 3 },
    { id: "m1-1-01", unit_id: "m1-1", title: "소수와 합성수", sort_order: 1 },
    { id: "m1-2-05", unit_id: "m1-2", title: "정수", sort_order: 5 },
    { id: "m1-2-02", unit_id: "m1-2", title: "유리수", sort_order: 2 },
    { id: "h1-1-01", unit_id: "h1-1", title: "다항식", sort_order: 1 },
  ];
  const sep = new Date(2026, 8, 15), mar = new Date(2026, 2, 1);
  assert.equal(defaultConceptFor({ grade: "중1" }, concepts, mar).id, "m1-1-01");
  assert.equal(defaultConceptFor({ grade: "중1" }, concepts, sep).id, "m1-2-02");
  assert.equal(defaultConceptFor({ grade: "고1" }, concepts, sep).id, "h1-1-01");   // h1-2 없음 → h1-1
  assert.equal(defaultConceptFor({ grade: "중3" }, concepts, sep).id, "m1-1-01");   // m3 없음 → m1-1
  assert.equal(defaultConceptFor(null, concepts, sep).id, "m1-1-01");
  assert.equal(defaultConceptFor({ grade: "고2" }, [{ id: "h3-1-07", unit_id: "h3-1", sort_order: 7 }, { id: "m2-2-01", unit_id: "m2-2", sort_order: 1 }], sep).id, "m2-2-01"); // 전체 첫 개념(단원 순)
  assert.equal(defaultConceptFor({ grade: "중1" }, [], sep), null);
  assert.equal(defaultConceptFor({ grade: "중1" }, null, sep), null);
});

// ── 퀴즈 구성 ─────────────────────────────────────────────────────────────────
const seedConcept = {
  id: "m1-1-01",
  blocks: [
    { id: "b1", type: "text", lines: ["소수는 …"] },
    { id: "b5", type: "check", question: "다음 수를 **분류**해 보세요:  1, 2, 9, 11, 15, 21",
      answer: [{ group: "소수", nums: "2, 11", tone: "teal" }, { group: "합성수", nums: "9, 15, 21", tone: "amber" }, { group: "둘 다 아님", nums: "1", tone: "coral" }] },
    { id: "b6", type: "check", question: "빈 답", answer: [{ group: "x", nums: "" }] },
    { id: "b7", type: "check", question: "답 없음" },
  ],
};

test("checkBlockItems — check 단락 → 그룹별 단답 의사 문항 (정답 포함, 마크업 제거)", () => {
  const its = checkBlockItems(seedConcept);
  assert.equal(its.length, 3);
  assert.deepEqual(its.map((x) => x.id), ["check:b5:0", "check:b5:1", "check:b5:2"]);
  assert.equal(its[0].qtype, "short"); assert.equal(its[0].source, "check");
  assert.equal(its[0].answer, "2, 11"); assert.equal(its[1].answer, "9, 15, 21");
  assert.ok(its[0].question.includes("「소수」"));
  assert.ok(!its[0].question.includes("**"), "굵게 마크업 제거");
  assert.deepEqual(checkBlockItems({ id: "x", blocks: [] }), []);
  assert.deepEqual(checkBlockItems(null), []);
});

test("pickQuiz — 객관식 우선, 같은 템플릿 회피, 부족하면 채움, 최대 n", () => {
  const items = [
    { id: "s1", qtype: "short", template_id: "T1" },
    { id: "c1", qtype: "choice", choices: ["1", "2", "3", "4", "5"], template_id: "T1" },
    { id: "c2", qtype: "choice", choices: ["1", "2", "3", "4", "5"], template_id: "T1" },
    { id: "c3", qtype: "choice", choices: ["1", "2", "3", "4", "5"], template_id: "T2" },
    { id: "s2", qtype: "short", template_id: "T3" },
  ];
  const seq = [0.1, 0.9, 0.3, 0.7, 0.5, 0.2, 0.8, 0.4, 0.6];
  let k = 0; const rnd = () => seq[k++ % seq.length];
  const q = pickQuiz(items, 3, rnd);
  assert.equal(q.length, 3);
  const ids = q.map((x) => x.id);
  assert.ok(ids.filter((id) => id.startsWith("c")).length >= 2, "객관식 2개(템플릿 T1·T2) 먼저: " + ids);
  assert.ok(!(ids.includes("c1") && ids.includes("c2")), "같은 템플릿 T1 객관식이 둘 다 뽑히면 안 됨: " + ids);
  assert.equal(pickQuiz(items.slice(0, 2), 3, rnd).length, 2);
  assert.equal(pickQuiz([], 3, rnd).length, 0);
  assert.equal(pickQuiz([{ id: "a", qtype: "short", template_id: "T" }, { id: "b", qtype: "short", template_id: "T" }], 3, rnd).length, 2, "부족하면 같은 템플릿이라도 채운다");
});

test("stripAnswers — 정답·해설·라벨 제거", () => {
  const s = stripAnswers({ id: "i1", qtype: "choice", question: "q", choices: ["a", "b"], figure: null, difficulty: 2, answer: "b", answer_alt: ["x"], solution: { levels: [] }, labels: { L21_traps: [] } });
  assert.deepEqual(Object.keys(s).sort(), ["choices", "difficulty", "figure", "id", "qtype", "question", "source"]);
  assert.equal(s.source, "item");
  assert.equal(stripAnswers(null), null);
});

// ── 채점 ─────────────────────────────────────────────────────────────────────
const quiz = [
  { id: "c1", qtype: "choice", choices: ["1", "2", "3", "4", "5"], answer: "3" },
  { id: "c2", qtype: "choice", choices: ["[[frac(1,2)]]", "[[frac(1,3)]]", "2", "3", "4"], answer: "[[frac(1,2)]]" },
  { id: "s1", qtype: "short", answer: "[[deg(60)]]", answer_alt: ["60"] },
  ...checkBlockItems(seedConcept).slice(0, 1),   // check:b5:0 → "2, 11"
];

test("judgeQuiz — 객관식 index, 단답 값 동치, 분류 집합 순서 무관 → 만점", () => {
  const r = judgeQuiz(quiz, [
    { item_id: "c1", index: 2 },
    { item_id: "c2", index: 0 },
    { item_id: "s1", answer: "60°" },
    { item_id: "check:b5:0", answer: "11,2" },
  ]);
  assert.equal(r.max, 4); assert.equal(r.score, 4); assert.deepEqual(r.wrong, []);
  assert.deepEqual(r.results.map((x) => x.correct), [true, true, true, true]);
});

test("judgeQuiz — 객관식 answer 텍스트('③'·보기 문자열·값)도 인정, index 문자열도 허용", () => {
  assert.equal(judgeQuiz(quiz.slice(0, 1), [{ item_id: "c1", answer: "③" }]).score, 1);
  assert.equal(judgeQuiz(quiz.slice(0, 1), [{ item_id: "c1", answer: "3" }]).score, 1);
  assert.equal(judgeQuiz(quiz.slice(0, 1), [{ item_id: "c1", index: "2" }]).score, 1);
  assert.equal(judgeQuiz(quiz.slice(1, 2), [{ item_id: "c2", answer: "1/2" }]).score, 1);
});

test("judgeQuiz — 오답·빈 답·없는 문항·index 범위 밖은 wrong 에 모인다", () => {
  const r = judgeQuiz(quiz, [
    { item_id: "c1", index: 1 },
    { item_id: "c2", index: 7 },
    { item_id: "s1", answer: "   " },
    { item_id: "nope", answer: "2, 11" },
  ]);
  assert.equal(r.max, 4); assert.equal(r.score, 0);
  assert.deepEqual(r.wrong, ["c1", "c2", "s1", "check:b5:0"]);
  assert.deepEqual(judgeQuiz([], []), { score: 0, max: 0, wrong: [], results: [] });
  assert.deepEqual(judgeQuiz(null, null).max, 0);
  assert.equal(judgeQuiz(quiz.slice(3), [{ item_id: "check:b5:0", answer: "2, 11, 9" }]).score, 0, "집합이 다르면 오답");
});

// ── 날짜 ─────────────────────────────────────────────────────────────────────
test("kstDayStart — 한국 시간 0시 (UTC 15:00)", () => {
  assert.equal(kstDayStart(Date.parse("2026-09-15T10:00:00Z")), "2026-09-14T15:00:00.000Z");   // KST 9/15 19:00
  assert.equal(kstDayStart(Date.parse("2026-09-15T16:00:00Z")), "2026-09-15T15:00:00.000Z");   // KST 9/16 01:00
  assert.equal(kstDayStart("2026-09-15T14:59:59Z"), "2026-09-14T15:00:00.000Z");
  assert.equal(kstDayStart("2026-09-15T15:00:00Z"), "2026-09-15T15:00:00.000Z");
});

console.log(`\n${n - failed}/${n} passed`);
if (failed) process.exit(1);
