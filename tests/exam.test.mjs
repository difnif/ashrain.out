// node tests/exam.test.mjs — 시험 응시 순수 도우미(src/lib/exam.js) 검사
import assert from "node:assert/strict";
import {
  TEST_TYPES, presetOf, describeTimer, presetRules, SELECT_BY_TEST_TYPE, DEFAULT_QTYPES, fetchPlan,
  dedupeById, shuffleWith, diversify, prefers, buildSelection,
  emptyAnswer, isAnswered, answeredCount, judgeAll, itemPoints, scoreRun, scoreText, examMessage,
  fmtTimer, remainingSec, isTimerWarn,
  newRunId, runToRow, RUNS_KEY, RUNS_KEEP, loadRunsLocal, saveRunLocal, mergeRuns, describeRun,
} from "../src/lib/exam.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}

const seq = (vals) => { let i = 0; return () => vals[i++ % vals.length]; };   // 결정적 rng
const mk = (id, extra = {}) => ({ id, unit_id: "m1-1", concept_ids: ["m1-1-01"], qtype: "short", difficulty: 3, points: 4, question: `문제 ${id}`, answer: "1", ...extra });
const choice = (id, extra = {}) => mk(id, { qtype: "choice", choices: ["27", "31", "39", "41", "45"], answer: "31", labels: { L42_distractor_map: { "27": "MC-CALC-01" } }, ...extra });

// ── 프리셋 ──
test("TEST_TYPES: 8종, 코드 고유, 필수 필드", () => {
  assert.equal(TEST_TYPES.length, 8);
  assert.deepEqual(TEST_TYPES.map((t) => t.code), ["concept_set", "unit", "calc", "sangwa", "mock", "ash", "rain", "out"]);
  assert.equal(new Set(TEST_TYPES.map((t) => t.code)).size, 8);
  for (const t of TEST_TYPES) {
    assert.ok(t.name && t.desc, t.code);
    assert.ok(["none", "total", "item"].includes(t.timer.kind), t.code);
    assert.ok(["concept", "unit"].includes(t.scope), t.code);
    assert.ok(["count", "points", "scaled100"].includes(t.pointsMode), t.code);
    assert.equal(typeof t.n, "number");
  }
  assert.equal(presetOf("calc").timer.kind, "item");
  assert.equal(presetOf("calc").timer.sec, 20);
  assert.equal(presetOf("calc").difficultyMax, 2);
  assert.equal(presetOf("unit").timer.sec, 1800);
  assert.equal(presetOf("unit").timer.soft, true);
  assert.equal(presetOf("mock").pointsMode, "scaled100");
  assert.equal(presetOf("mock").timer.sec, 2400);
  assert.equal(presetOf("rain").n, 100);
  assert.equal(presetOf("rain").timer.sec, 1500);
  assert.equal(presetOf("ash").badge.text, "ASH");
  assert.equal(presetOf("ash").n, 15);
  assert.equal(presetOf("out").n, 30);
  assert.equal(presetOf("out").timer.sec, 2700);
  assert.equal(presetOf("concept_set").scope, "concept");
  assert.equal(presetOf("concept_set").timer.kind, "none");
  assert.equal(presetOf("sangwa").route, "#/solve/essay");
  assert.equal(presetOf("nope"), null);
  assert.equal(presetOf(null), null);
});

test("describeTimer / presetRules", () => {
  assert.equal(describeTimer(presetOf("concept_set")), "제한 시간 없음");
  assert.equal(describeTimer(presetOf("unit")), "총 30분");
  assert.equal(describeTimer(presetOf("calc")), "문항당 20초");
  assert.equal(describeTimer({ timer: { kind: "total", sec: 90 } }), "총 1분 30초");
  assert.equal(describeTimer(null), "제한 시간 없음");
  assert.ok(presetRules(presetOf("mock")).some((r) => r.includes("100점")));
  assert.ok(presetRules(presetOf("calc")).some((r) => r.includes("자동") || r.includes("바로 다음")));
  assert.ok(presetRules(presetOf("unit")).some((r) => r.includes("고칠")));
  assert.deepEqual(presetRules(null), []);
});

// ── 출제 계획 ──
test("fetchPlan: 기본은 fetch 1회, calc 는 난이도 1·2 + 채움, ash 는 난이도 5단 + 채움", () => {
  assert.equal(SELECT_BY_TEST_TYPE, false);
  const u = fetchPlan(presetOf("unit"), { kind: "unit", id: "m1-1" });
  assert.equal(u.length, 1);
  assert.deepEqual(u[0], { unitId: "m1-1", qtypes: DEFAULT_QTYPES, n: 20, pool: 60, stage: "primary" });
  const c = fetchPlan(presetOf("concept_set"), { kind: "concept", id: "m1-1-03" });
  assert.equal(c[0].conceptId, "m1-1-03");
  assert.equal(c[0].unitId, undefined);
  const calc = fetchPlan(presetOf("calc"), { kind: "unit", id: "m2-1" });
  assert.deepEqual(calc.map((p) => [p.difficulty, p.stage]), [[1, "primary"], [2, "primary"], [undefined, "fill"]]);
  assert.deepEqual(calc[0].qtypes, ["short", "choice"]);
  assert.equal(calc[0].n, 10);
  const ash = fetchPlan(presetOf("ash"), { kind: "unit", id: "m2-1" });
  assert.equal(ash.length, 6);
  assert.equal(ash[0].n, 3);
  assert.equal(ash[5].stage, "fill");
  assert.equal(ash[5].n, 15);
  assert.ok(!("testType" in u[0]));
  assert.deepEqual(fetchPlan(presetOf("sangwa"), { kind: "unit", id: "m1-1" }), []);
  assert.deepEqual(fetchPlan(null), []);
});

// ── 문항 선발 ──
test("dedupeById / shuffleWith / diversify", () => {
  const a = mk("a"), b = mk("b");
  assert.deepEqual(dedupeById([a, b, a, null, { id: null }]).map((x) => x.id), ["a", "b"]);
  const sh = shuffleWith([1, 2, 3, 4], seq([0]));
  assert.deepEqual([...sh].sort(), [1, 2, 3, 4]);
  assert.deepEqual(shuffleWith(null), []);
  const tpl = [mk("a", { template_id: "T" }), mk("b", { template_id: "T" }), mk("c", { template_id: "T" }), mk("d", { template_id: "U" })];
  assert.deepEqual(diversify(tpl, 3).map((x) => x.id), ["a", "b", "d"]);
  assert.deepEqual(diversify(tpl, 4).map((x) => x.id), ["a", "b", "d", "c"]);   // 모자라면 나머지로 채움
  assert.deepEqual(diversify([], 3), []);
});

test("prefers: 난이도 상한 · 유형", () => {
  const calc = presetOf("calc");
  assert.equal(prefers(calc, mk("a", { difficulty: 2 })), true);
  assert.equal(prefers(calc, mk("a", { difficulty: 3 })), false);
  assert.equal(prefers(calc, mk("a", { difficulty: 1, qtype: "essay" })), false);
  assert.equal(prefers(presetOf("unit"), mk("a", { difficulty: 5 })), true);
  assert.equal(prefers(calc, null), false);
});

test("buildSelection: n 개, 중복 없음, 선호 문항 우선, 모자라면 short", () => {
  const pool = Array.from({ length: 30 }, (_, i) => mk("p" + i, { difficulty: (i % 5) + 1 }));
  const r = buildSelection(presetOf("unit"), pool.concat(pool), seq([0.3, 0.7, 0.1]));
  assert.equal(r.items.length, 20);
  assert.equal(new Set(r.items.map((x) => x.id)).size, 20);
  assert.equal(r.short, 0);
  assert.equal(r.relaxed, false);
  // order:"difficulty" → 쉬운 문항부터
  for (let i = 1; i < r.items.length; i++) assert.ok(r.items[i - 1].difficulty <= r.items[i].difficulty);

  const calc = buildSelection(presetOf("calc"), pool, seq([0.5]));
  assert.equal(calc.items.length, 10);
  assert.ok(calc.items.every((x) => x.difficulty <= 2));   // 쉬운 문항이 12개 있으니 전부 선호 문항
  assert.equal(calc.relaxed, false);

  const few = buildSelection(presetOf("calc"), [mk("e1", { difficulty: 1 }), mk("h1", { difficulty: 4 }), mk("h2", { difficulty: 5 })], seq([0]));
  assert.equal(few.items.length, 3);
  assert.equal(few.items[0].id, "e1");                    // 선호 문항이 앞
  assert.equal(few.relaxed, true);
  assert.equal(few.short, 7);

  assert.deepEqual(buildSelection(presetOf("rain"), []), { items: [], short: 100, relaxed: false });
  assert.deepEqual(buildSelection(presetOf("rain"), null).items, []);
});

// ── 답 상태 · 채점 ──
test("emptyAnswer / isAnswered / answeredCount", () => {
  assert.deepEqual(emptyAnswer(), { sel: null, text: "" });
  assert.equal(isAnswered(choice("c"), { sel: 0, text: "" }), true);
  assert.equal(isAnswered(choice("c"), { sel: null, text: "3" }), false);
  assert.equal(isAnswered(mk("s"), { sel: null, text: "  " }), false);
  assert.equal(isAnswered(mk("s"), { sel: null, text: " 1/2 " }), true);
  assert.equal(isAnswered(mk("s"), null), false);
  assert.equal(answeredCount([choice("c"), mk("s"), mk("t")], [{ sel: 2 }, { text: "x" }, undefined]), 2);
  assert.equal(answeredCount([], []), 0);
});

test("judgeAll: 객관식·단답·무응답, 경과 시간, 오개념 태그", () => {
  const items = [choice("c1"), choice("c2"), mk("s1", { answer: "[[frac(1,2)]]" }), mk("s2"), mk("s3")];
  const answers = [{ sel: 1 }, { sel: 0 }, { text: "1/2" }, { text: "" }, null];
  const rs = judgeAll(items, answers, [3.4, 10, 7, 0, undefined]);
  assert.equal(rs.length, 5);
  assert.deepEqual(rs.map((r) => r.correct), [true, false, true, false, false]);
  assert.deepEqual(rs.map((r) => r.skipped), [false, false, false, true, true]);
  assert.equal(rs[0].chosenIndex, 1);
  assert.equal(rs[0].chosenChoice, "31");
  assert.equal(rs[0].rawAnswer, "31");
  assert.equal(rs[0].tag, null);
  assert.equal(rs[1].tag, "MC-CALC-01");
  assert.equal(rs[2].rawAnswer, "1/2");
  assert.equal(rs[2].chosenIndex, null);
  assert.deepEqual(rs.map((r) => r.elapsedSec), [3, 10, 7, 0, 0]);
  assert.equal(rs[4].rawAnswer, null);
  // 보기 범위 밖 번호는 무응답
  assert.equal(judgeAll([choice("c")], [{ sel: 9 }])[0].skipped, true);
  assert.deepEqual(judgeAll([], []), []);
  assert.equal(judgeAll([null], [{ text: "1" }])[0].skipped, true);
});

test("itemPoints / scoreRun (count · points · scaled100)", () => {
  assert.equal(itemPoints(mk("a", { points: 3 })), 3);
  assert.equal(itemPoints(mk("a", { points: null })), 1);
  assert.equal(itemPoints(mk("a", { points: "5" })), 5);
  assert.equal(itemPoints(mk("a", { points: -2 })), 1);
  assert.equal(itemPoints(null), 1);
  const rs = [
    { item: mk("a", { points: 3 }), correct: true },
    { item: mk("b", { points: 4 }), correct: false },
    { item: mk("c", { points: 5 }), correct: true },
    null,
  ];
  // null 항목은 문항이 아니므로 n 에서도 뺀다
  assert.deepEqual(scoreRun(presetOf("unit"), rs), { correct_n: 2, n: 3, score: 2, max: 3, pct: 67, raw: 2, rawMax: 3 });
  assert.deepEqual(scoreRun({ pointsMode: "points" }, rs), { correct_n: 2, n: 3, score: 8, max: 12, pct: 67, raw: 8, rawMax: 12 });
  assert.deepEqual(scoreRun(presetOf("mock"), rs), { correct_n: 2, n: 3, score: 67, max: 100, pct: 67, raw: 8, rawMax: 12 });
  assert.deepEqual(scoreRun(presetOf("mock"), []), { correct_n: 0, n: 0, score: 0, max: 100, pct: 0, raw: 0, rawMax: 0 });
  assert.deepEqual(scoreRun(null, null), { correct_n: 0, n: 0, score: 0, max: 0, pct: 0, raw: 0, rawMax: 0 });
  // 배점이 없으면 문항당 1점
  const all = [{ item: mk("x", { points: null }), correct: true }, { item: mk("y", { points: null }), correct: true }];
  assert.equal(scoreRun(presetOf("mock"), all).score, 100);
});

test("examMessage: 범위 표현 · 무응답 힌트", () => {
  assert.match(examMessage(presetOf("unit"), { n: 20, pct: 95 }), /이 단원은 자신 있게/);
  assert.match(examMessage(presetOf("concept_set"), { n: 5, pct: 100 }), /이 개념은/);
  assert.match(examMessage(presetOf("unit"), { n: 20, pct: 75 }), /잘했어요/);
  assert.match(examMessage(presetOf("unit"), { n: 20, pct: 55 }), /절반/);
  assert.match(examMessage(presetOf("rain"), { n: 100, pct: 20 }), /낯선 범위/);
  assert.match(examMessage(presetOf("rain"), { n: 100, pct: 20 }, 40), /무응답 40문항.*시간 안배/);
  assert.doesNotMatch(examMessage(presetOf("concept_set"), { n: 5, pct: 60 }, 2), /시간 안배/);
  assert.match(examMessage(presetOf("concept_set"), { n: 5, pct: 60 }, 2), /무응답 2문항/);
  assert.equal(examMessage(presetOf("unit"), { n: 0, pct: 0 }), "푼 문항이 없어요.");
  assert.equal(examMessage(null, null), "푼 문항이 없어요.");
});

test("scoreText", () => {
  assert.equal(scoreText(presetOf("unit"), { correct_n: 12, n: 20, score: 12, max: 20 }), "12 / 20");
  assert.equal(scoreText({ pointsMode: "points" }, { score: 38, max: 45 }), "38 / 45점");
  assert.equal(scoreText(presetOf("mock"), { score: 85, max: 100 }), "85점");
  assert.equal(scoreText(presetOf("mock"), null), "");
});

// ── 타이머 ──
test("fmtTimer", () => {
  assert.equal(fmtTimer(0), "00:00");
  assert.equal(fmtTimer(65), "01:05");
  assert.equal(fmtTimer(1800), "30:00");
  assert.equal(fmtTimer(3661), "1:01:01");
  assert.equal(fmtTimer(-12), "-00:12");
  assert.equal(fmtTimer(59.9), "00:59");
  assert.equal(fmtTimer("x"), "00:00");
  assert.equal(fmtTimer(null), "00:00");
});

test("remainingSec / isTimerWarn", () => {
  const unit = presetOf("unit"), calc = presetOf("calc");
  assert.equal(remainingSec(unit, { startedAt: 1000, now: 1000 }), 1800);
  assert.equal(remainingSec(unit, { startedAt: 1000, now: 1000 + 1800 * 1000 }), 0);
  assert.equal(remainingSec(unit, { startedAt: 1000, now: 1000 + 1801 * 1000 }), -1);
  assert.equal(remainingSec(unit, { startedAt: 1000, now: 1500 }), 1800);          // 올림 (0.5초 지남 → 1800)
  assert.equal(remainingSec(unit, { startedAt: 1000, now: 2001 }), 1799);
  assert.equal(remainingSec(calc, { startedAt: 0, enteredAt: 5000, now: 12000 }), 13);
  assert.equal(remainingSec(presetOf("concept_set"), { startedAt: 1, now: 2 }), null);
  assert.equal(remainingSec(unit, { now: 2 }), null);
  assert.equal(remainingSec(null, {}), null);
  assert.equal(isTimerWarn(unit, 60), true);
  assert.equal(isTimerWarn(unit, 180), true);        // 1800 의 10% = 180
  assert.equal(isTimerWarn(unit, 181), false);
  assert.equal(isTimerWarn(calc, 5), true);
  assert.equal(isTimerWarn(calc, 6), false);
  assert.equal(isTimerWarn(unit, null), false);
  assert.equal(isTimerWarn(presetOf("concept_set"), 1), false);
});

// ── 응시 기록 ──
test("newRunId 형식", () => {
  assert.equal(newRunId("unit", 1000), "test:unit:rs");
  assert.match(newRunId("rain"), /^test:rain:[0-9a-z]+$/);
  assert.equal(newRunId(null, 1), "test:misc:1");
});

test("runToRow: test_runs 행 모양", () => {
  const items = [choice("c1", { concept_ids: ["m1-1-02"] }), mk("s1", { concept_ids: ["m1-1-03"] }), mk("s2")];
  const rs = judgeAll(items, [{ sel: 1 }, { text: "2" }, null], [10, 20, 0]);
  const row = runToRow("u1", presetOf("mock"), { unitId: "m1-1", scopeTitle: "중1-1", startedAt: 1_700_000_000_000, finishedAt: 1_700_000_030_000, short: 17, runId: "test:mock:abc" }, rs);
  assert.equal(row.user_id, "u1");
  assert.equal(row.test_type, "mock");
  assert.equal(row.unit_id, "m1-1");
  assert.deepEqual(row.concept_ids, ["m1-1-02", "m1-1-03", "m1-1-01"]);
  assert.deepEqual(row.item_ids, ["c1", "s1", "s2"]);
  assert.equal(row.answers.length, 3);
  assert.deepEqual(row.answers[0], { item_id: "c1", answer: "31", correct: true, elapsed_sec: 10, chosen_index: 2 });
  assert.deepEqual(row.answers[1], { item_id: "s1", answer: "2", correct: false, elapsed_sec: 20 });
  assert.deepEqual(row.answers[2], { item_id: "s2", answer: null, correct: false, elapsed_sec: 0 });
  assert.equal(row.n, 3);
  assert.equal(row.correct_n, 1);
  assert.equal(row.score, 33);                 // 4 / 12 → 33점
  assert.equal(row.max, 100);
  assert.equal(row.started_at, "2023-11-14T22:13:20.000Z");
  assert.equal(row.finished_at, "2023-11-14T22:13:50.000Z");
  assert.equal(row.elapsed_sec, 30);
  assert.deepEqual(row.meta.timer, { kind: "total", sec: 2400 });
  assert.deepEqual(row.meta.preset, { code: "mock", name: "실전 모의고사", n: 20, scope: "unit", pointsMode: "scaled100" });
  assert.deepEqual(row.meta.scope, { kind: "unit", id: "m1-1", title: "중1-1" });
  assert.equal(row.meta.short, 17);
  assert.equal(row.meta.run_id, "test:mock:abc");
  assert.equal(row.meta.raw, 4);
  assert.equal(row.meta.raw_max, 12);
  // 개념 범위 · 시간 초과 · 로그인 없음
  const r2 = runToRow(null, presetOf("concept_set"), { conceptId: "m1-1-01", timedOut: true, overtimeSec: 12.4 }, rs);
  assert.equal(r2.user_id, null);
  assert.equal(r2.unit_id, "m1-1");            // 문항에서 유추
  assert.equal(r2.concept_ids[0], "m1-1-01");
  assert.deepEqual(r2.meta.scope, { kind: "concept", id: "m1-1-01", title: null });
  assert.equal(r2.meta.timer.timed_out, true);
  assert.equal(r2.meta.timer.overtime_sec, 12);
  assert.equal(r2.started_at, null);
  assert.equal(r2.elapsed_sec, 30);            // 시작 시각이 없으면 문항 경과 합
  assert.equal(r2.score, 1);
  assert.equal(r2.max, 3);
  assert.ok(!("raw" in r2.meta));
  // 빈 결과도 안전
  const r3 = runToRow("u", presetOf("rain"), {}, []);
  assert.equal(r3.n, 0);
  assert.deepEqual(r3.item_ids, []);
  assert.equal(r3.unit_id, null);
});

test("saveRunLocal / loadRunsLocal: 최근 30건, 최신이 앞, 저장소 없어도 조용히", () => {
  const storeMap = new Map();
  globalThis.localStorage = { getItem: (k) => (storeMap.has(k) ? storeMap.get(k) : null), setItem: (k, v) => storeMap.set(k, String(v)) };
  assert.deepEqual(loadRunsLocal(), []);
  const rec = saveRunLocal({ test_type: "unit", n: 20, correct_n: 15, finished_at: "2026-09-15T01:00:00.000Z" }, 1000);
  assert.equal(rec.local, true);
  assert.match(rec.id, /^local:rs/);
  assert.equal(loadRunsLocal().length, 1);
  assert.equal(loadRunsLocal()[0].test_type, "unit");
  for (let i = 0; i < 40; i++) saveRunLocal({ test_type: "rain", n: 100, correct_n: i, finished_at: new Date(2026, 0, 1, 0, i).toISOString() }, 2000 + i);
  const list = loadRunsLocal();
  assert.equal(list.length, RUNS_KEEP);
  assert.equal(list[0].correct_n, 39);           // 최신이 앞
  assert.ok(!list.some((r) => r.test_type === "unit"));   // 오래된 것은 밀려남
  assert.ok(storeMap.has(RUNS_KEY));
  assert.equal(saveRunLocal(null), null);
  // 깨진 저장 내용
  storeMap.set(RUNS_KEY, "{not json");
  assert.deepEqual(loadRunsLocal(), []);
  storeMap.set(RUNS_KEY, JSON.stringify({ a: 1 }));
  assert.deepEqual(loadRunsLocal(), []);
  // 저장소가 죽어도 조용히
  globalThis.localStorage = { getItem: () => { throw new Error("nope"); }, setItem: () => { throw new Error("nope"); } };
  assert.deepEqual(loadRunsLocal(), []);
  assert.doesNotThrow(() => saveRunLocal({ test_type: "unit" }));
  delete globalThis.localStorage;
  assert.deepEqual(loadRunsLocal(), []);
  assert.ok(saveRunLocal({ test_type: "unit" }));   // 저장소 없어도 rec 은 돌려준다
});

test("mergeRuns: id 중복 제거, 최신순, limit", () => {
  const db = [{ id: 1, finished_at: "2026-09-10T00:00:00Z" }, { id: 2, finished_at: "2026-09-12T00:00:00Z" }];
  const local = [{ id: "local:a", finished_at: "2026-09-11T00:00:00Z", local: true }, { id: 2, finished_at: "2026-09-12T00:00:00Z" }, null];
  const m = mergeRuns(db, local, 10);
  assert.deepEqual(m.map((r) => r.id), [2, "local:a", 1]);
  assert.deepEqual(mergeRuns(db, local, 1).map((r) => r.id), [2]);
  assert.deepEqual(mergeRuns(null, undefined), []);
  assert.deepEqual(mergeRuns([{ id: 3 }], [{ id: 4, finished_at: "bad" }]).map((r) => r.id), [3, 4]);
});

test("describeRun: 이름·범위·점수·링크", () => {
  const d = describeRun({ id: 1, test_type: "mock", unit_id: "m2-1", n: 20, correct_n: 15, score: 78, max: 100, finished_at: "2026-09-15T01:00:00Z",
    meta: { preset: { pointsMode: "scaled100" }, scope: { kind: "unit", id: "m2-1", title: "중2-1" } } }, { "m2-1": "중2-1" });
  assert.equal(d.name, "실전 모의고사");
  assert.equal(d.scope, "중2-1");
  assert.equal(d.score, "78점");
  assert.equal(d.link, "#/solve/test/mock/m2-1");
  assert.equal(d.local, false);
  const c = describeRun({ test_type: "concept_set", unit_id: "m1-1", n: 5, correct_n: 4, score: 4, max: 5, meta: { scope: { kind: "concept", id: "m1-1-03", title: "소인수분해" } }, local: true });
  assert.equal(c.score, "4 / 5");
  assert.equal(c.scope, "소인수분해");
  assert.equal(c.link, "#/solve/test/concept_set/m1-1-03");
  assert.equal(c.local, true);
  const u = describeRun({ test_type: "unit", unit_id: "h1-1", n: 20, correct_n: 9, score: 9, max: 20 }, { "h1-1": "고1-1" });
  assert.equal(u.scope, "고1-1");
  assert.equal(u.link, "#/solve/test/unit/h1-1");
  const x = describeRun({ test_type: "weird" });
  assert.equal(x.name, "weird");
  assert.equal(x.score, "0 / 0");
  assert.equal(x.link, "#/solve/test/weird");
  assert.equal(describeRun(null).name, "시험");
});

console.log(`\n${n - failed}/${n} passed`);
if (failed) process.exit(1);
