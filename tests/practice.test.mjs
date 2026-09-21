// node tests/practice.test.mjs — 예제·유제 순수 도우미(src/lib/practice.js) 검사
import assert from "node:assert/strict";
import { CIRC, practiceKind, normAns, numVal, isCorrect, unitMissing, stripExample, answerShape, inputHint, displayAnswer, practicePhase } from "../src/lib/practice.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}

test("practiceKind: 예제만 예제, 나머지는 유제", () => {
  assert.equal(practiceKind({ kind: "예제" }), "예제");
  assert.equal(practiceKind({ kind: "유제" }), "유제");
  assert.equal(practiceKind({}), "유제");
  assert.equal(practiceKind(null), "유제");
});

test("normAns / numVal / isCorrect: 공백·기호 통일, ① → 1, 수치 동치", () => {
  assert.equal(normAns(" x = −3 "), "x=-3");
  assert.equal(normAns("②"), "2");
  assert.equal(numVal("1/2"), 0.5);
  assert.equal(numVal("abc"), null);
  assert.equal(isCorrect("0.5", ["1/2"]), true);
  assert.equal(isCorrect("0.5", ["1/2"], { exact: true }), false);
  assert.equal(isCorrect("②", ["2"]), true);
  assert.equal(isCorrect("", ["0"]), false);
  assert.equal(isCorrect("x=-3", ["x = −3", "-3"]), true);
  assert.equal(isCorrect("4", ["5"]), false);
});

test("unitMissing: 값은 맞는데 단위만 빠짐", () => {
  const a = { accept: ["12cm"], unit: "cm" };
  assert.equal(unitMissing("12", a), true);
  assert.equal(unitMissing("12cm", a), false);
  assert.equal(unitMissing("13", a), false);
  assert.equal(unitMissing("", a), false);
  assert.equal(unitMissing("12", { accept: ["12"] }), false);
});

test("stripExample: 예시를 떼고 안내문만", () => {
  assert.equal(stripExample("번호만 입력 (예: 1)"), "번호만 입력");
  assert.equal(stripExample("두 근을 쉼표로 (예: 1,-2)"), "두 근을 쉼표로");
  assert.equal(stripExample("예: 100°"), "");
  assert.equal(stripExample("예: (0,0)"), "");
  assert.equal(stripExample("숫자로 입력"), "숫자로 입력");
  assert.equal(stripExample(""), "");
  assert.equal(stripExample(null), "");
});

test("answerShape: 값은 감추고 꼴만", () => {
  assert.equal(answerShape("(-1,1)"), "(□,□)");
  assert.equal(answerShape("x=-1"), "x=□");
  assert.equal(answerShape("y=-2x+4"), "y=□x+□");
  assert.equal(answerShape("2x-1"), "□x-□");
  assert.equal(answerShape("10√2"), "□√□");
  assert.equal(answerShape("√18"), "√□");
  assert.equal(answerShape("100°"), "□°");
  assert.equal(answerShape("10cm"), "□cm");
  assert.equal(answerShape("-2±√3"), "□±√□");
  assert.equal(answerShape("±2"), "±□");
  assert.equal(answerShape("-1,0"), "□,□");
  assert.equal(answerShape("1,-2"), "□,□");
  assert.equal(answerShape("-2<k<2"), "□<k<□");
  assert.equal(answerShape("a^6"), "a^□");
  assert.equal(answerShape("0.05"), "□");
  assert.equal(answerShape("-1287"), "□");
  assert.equal(answerShape("3/4"), "□/□");
  assert.equal(answerShape("1:2"), "□:□");
  assert.equal(answerShape("㉠,㉢"), null);     // 숫자 없음 → 모양이 곧 답
  assert.equal(answerShape("없다"), null);
  assert.equal(answerShape("a"), null);
  assert.equal(answerShape(""), null);
  assert.equal(answerShape(null), null);
});

test("inputHint: 표기 방식만 — 예시 값은 절대 안 보인다", () => {
  assert.equal(inputHint({ placeholder: "번호만 입력 (예: 2)", accept: ["2"] }, { hasChoices: true, nChoices: 5 }), "번호로 입력 (1~5)");
  assert.equal(inputHint({ placeholder: "숫자로 입력", accept: ["-1287"] }), "숫자로 입력");
  assert.equal(inputHint({ placeholder: "예: 100°", accept: ["100°"] }), "□° 꼴로 입력");
  assert.equal(inputHint({ placeholder: "예: (0,0)", accept: ["(-1,1)"] }), "(□,□) 꼴로 입력");
  assert.equal(inputHint({ placeholder: "예: x=0", accept: ["x=-1"] }), "x=□ 꼴로 입력");
  assert.equal(inputHint({ placeholder: "두 근을 쉼표로 (예: 1,-2)", accept: ["-1,0"] }), "두 근을 쉼표로 (□,□ 꼴)");
  assert.equal(inputHint({ placeholder: "예: 0", accept: ["-1"] }), "숫자로 입력");
  assert.equal(inputHint({ placeholder: "예: 10개", accept: ["0개"], unit: "개" }), "□개 꼴로 입력");
  assert.equal(inputHint({ accept: ["1/2"], format: "fraction" }), "분자 / 분모");
  assert.equal(inputHint({ placeholder: "예: ㉠", accept: ["㉠,㉢"] }), "답 입력");
  assert.equal(inputHint({ accept: ["없다"], unit: "개" }), "단위까지 (개)");
  assert.equal(inputHint({}), "답 입력");
  // 어떤 경우에도 힌트에 답 값이 들어가지 않는다
  for (const [ans, ph] of [["100°", "예: 100°"], ["10√2", "예: 10√2"], ["2", "번호만 입력 (예: 2)"], ["y=-2x+4", "예: y=-2x+4"]]) {
    const h = inputHint({ placeholder: ph, accept: [ans] }, { hasChoices: ans === "2", nChoices: 5 });
    assert.ok(!h.includes(ans), `${ans} → ${h}`);
  }
});

test("displayAnswer: 객관식은 ①②…, 분수 칸은 {{a/b}}, 그 외 그대로", () => {
  assert.equal(displayAnswer({ accept: ["2"] }, { hasChoices: true }), "②");
  assert.equal(displayAnswer({ accept: ["7"] }, { hasChoices: true }), "7");
  assert.equal(displayAnswer({ accept: ["3/4"], format: "fraction" }), "{{3/4}}");
  assert.equal(displayAnswer({ accept: ["-3/4"], format: "fraction" }), "{{-3/4}}");
  assert.equal(displayAnswer({ accept: ["x=-1", "-1"] }), "x=-1");
  assert.equal(displayAnswer({}), "");
  assert.equal(CIRC.length, 6);
});

test("practicePhase: 예제는 항상 해설, 유제는 시도·기록이 있어야 해설", () => {
  assert.equal(practicePhase({ kind: "예제" }), "explain");
  assert.equal(practicePhase({ kind: "유제" }), "answer");
  assert.equal(practicePhase({ kind: "유제" }, { attempt: { result: "no" } }), "explain");
  assert.equal(practicePhase({ kind: "유제" }, { solved: true }), "explain");
  assert.equal(practicePhase({}), "answer");
});

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
