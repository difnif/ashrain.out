// 강사도구 — 하위 문제 (1)(2)(3) 따로 채점 (node --test tests/ttparts.test.mjs)
import { test } from "node:test";
import assert from "node:assert/strict";
import { partsFromAnswer, partsFromLines, splitLabel, baseHash, groupProblems, expandParts, relayout } from "../src/apps/seirocco/tt/parts.js";

test("정답 글자에서 하위 문제 나누기", () => {
  assert.deepEqual(partsFromAnswer("(1) 12 (2) 5"), [{ label: "(1)", answer: "12" }, { label: "(2)", answer: "5" }]);
  assert.deepEqual(partsFromAnswer("(1) 36 (2) 7/10").map((x) => x.answer), ["36", "7/10"]);
  assert.deepEqual(partsFromAnswer("(1) 1 L 300 mL + 850 mL = 2 L 150 mL / (2) 2 L").map((x) => x.answer), ["1 L 300 mL + 850 mL = 2 L 150 mL", "2 L"]);
  assert.deepEqual(partsFromAnswer("(1)12,(2)5,(3)7").map((x) => x.answer), ["12", "5", "7"]);
  assert.deepEqual(partsFromAnswer("⑴ 3 ⑵ 6").map((x) => x.label), ["(1)", "(2)"]);
  assert.deepEqual(partsFromAnswer("(1) (2)"), [{ label: "(1)", answer: "" }, { label: "(2)", answer: "" }]);   // 그림 정답(표시만)
  assert.equal(partsFromAnswer("(1) 12"), null);            // 하나뿐
  assert.equal(partsFromAnswer("f(1)=3, f(2)=5"), null);   // 식 속 괄호
  assert.equal(partsFromAnswer("답: (1) 3 (2) 4"), null);   // 맨 앞이 아님
  assert.equal(partsFromAnswer("(2) 3 (1) 4"), null);       // 차례가 아님
  assert.equal(partsFromAnswer(""), null);
  assert.equal(partsFromAnswer("③"), null);
});

test("문항 자리 글줄의 줄머리 (1) (2)", () => {
  assert.equal(partsFromLines(["3. 다음 물음에 답하시오.", "(1) 사과는 몇 개?", "(2) 배는 몇 개?", "(3) 모두 몇 개?"]), 3);
  assert.equal(partsFromLines(["다음 조건을 만족하는", "① 3 ② 4 ③ 5"]), 0);      // 객관식 번호는 아님
  assert.equal(partsFromLines(["(1) 하나만"]), 0);
  assert.equal(partsFromLines(["(1) a", "(1) b"]), 0);
  assert.equal(partsFromLines(["⑴ a", "⑵ b"]), 2);
});

test("label 「3 (2)」 나누기 · 지문 #", () => {
  assert.deepEqual(splitLabel("3 (2)"), { base: "3", part: 2 });
  assert.deepEqual(splitLabel("서답형 1 (1)"), { base: "서답형 1", part: 1 });
  assert.deepEqual(splitLabel("3"), { base: "3", part: 0 });
  assert.deepEqual(splitLabel("1-2"), { base: "1-2", part: 0 });
  assert.equal(baseHash("abc#2"), "abc");
  assert.equal(baseHash("abc"), "abc");
  assert.equal(baseHash("7CSKHR:3"), "7CSKHR:3");
  assert.equal(baseHash(null), null);
});

const row = (seq, extra = {}) => ({ seq, label: "", answer: "", choice: false, hash: "h" + seq, png: `items/00${seq}.png`, points: null, ...extra });

test("변환 · 등록: 문제를 채점 단위 줄로 펼치기", () => {
  const rows = expandParts([
    { row: row(1, { answer: "3", choice: true }), no: "1", parts: null },
    { row: row(2, { answer: "(1) 12 (2) 5", points: 6 }), no: "2", parts: partsFromAnswer("(1) 12 (2) 5") },
    { row: row(3, { answer: "7" }), no: "3", parts: null },
  ]);
  assert.deepEqual(rows.map((r) => [r.seq, r.label, r.answer, r.hash, r.png, r.points]), [
    [1, "1", "3", "h1", "items/001.png", null],
    [2, "2 (1)", "12", "h2#1", "items/002.png", 6],
    [3, "2 (2)", "5", "h2#2", "items/002.png", null],
    [4, "3", "7", "h3", "items/003.png", null],
  ]);
  assert.ok(rows.every((r) => !("part" in r)));
  // 하위 문제가 없으면 label 그대로(비워 둠)
  assert.deepEqual(expandParts([{ row: row(1), no: "1", parts: null }]).map((r) => r.label), [""]);
});

test("이미 있는 프린트: 나누기 · 다시 나누기 · 다시 묶기 배치", () => {
  const rows = [row(1), row(2, { answer: "(1) 12 (2) 5" }), row(3)];
  // 2번을 둘로
  const lay = relayout(rows, new Map([[2, [{ answer: "12" }, { answer: "5" }]]]));
  assert.deepEqual(lay.map((r) => [r.seq, r.from, r.label, r.answer, r.hash]), [
    [1, 1, "1", "", "h1"], [2, 2, "2 (1)", "12", "h2#1"], [3, 2, "2 (2)", "5", "h2#2"], [4, 3, "3", "", "h3"]]);
  // 그 결과(나뉜 줄)를 셋으로 — 있던 하위 문제는 제 기록을, 새 하위 문제는 첫 줄 기록을
  const now = lay.map((r) => ({ ...row(r.seq), label: r.label, answer: r.answer, hash: r.hash, png: r.from === 2 ? "items/002.png" : `items/00${r.from}.png` }));
  const g = groupProblems(now);
  assert.deepEqual(g.map((x) => [x.base, x.rows.length, x.parts]), [["1", 1, false], ["2", 2, true], ["3", 1, false]]);
  const lay3 = relayout(now, new Map([[2, [{ answer: "12" }, { answer: "5" }, { answer: "9" }]]]));
  assert.deepEqual(lay3.map((r) => [r.seq, r.from, r.label]), [[1, 1, "1"], [2, 2, "2 (1)"], [3, 3, "2 (2)"], [4, 2, "2 (3)"], [5, 4, "3"]]);
  // 다시 하나로: 첫 줄 기록 · 정답은 「(1) … (2) …」로 모음
  const one = relayout(now, new Map([[2, null]]));
  assert.deepEqual(one.map((r) => [r.seq, r.from, r.label, r.answer, r.hash]), [[1, 1, "1", "", "h1"], [2, 2, "2", "(1) 12 (2) 5", "h2"], [3, 4, "3", "", "h3"]]);
  // 바꾸지 않은 문제는 그대로
  assert.deepEqual(relayout(now, new Map()).map((r) => [r.from, r.label]), [[1, "1"], [2, "2 (1)"], [3, "2 (2)"], [4, "3"]]);
});
