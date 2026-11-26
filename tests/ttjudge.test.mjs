// 강사도구 — OMR 카드 자동 채점: 단위만 다른 답은 「?」(선생님께 묻기) (node --test tests/ttjudge.test.mjs)
import { test } from "node:test";
import assert from "node:assert/strict";
import { judge, splitUnit } from "../src/apps/seirocco/tt/logic.js";

const r = (k, g) => judge(k, g).result;

test("같은 답은 O, 다른 답은 X", () => {
  assert.equal(r("12", "12"), "O");
  assert.equal(r("③", "3"), "O");
  assert.equal(r("1/2", "0.5"), "O");
  assert.equal(r("12 cm", "12cm"), "O");
  assert.equal(r("12cm", "12㎝"), "O");
  assert.equal(r("6cm²", "6 cm2"), "O");
  assert.equal(r("6㎠", "6cm²"), "O");
  assert.equal(r("30°", "30도"), "O");
  assert.equal(r("2L", "2 ℓ"), "O");
  assert.equal(r("y = 2x + 3", "y=2x+3"), "O");
  assert.equal(r("13", "12"), "X");
  assert.equal(r("12cm", "13cm"), "X");
  assert.equal(r("12cm", "13"), "X");
  assert.equal(r("2", "3"), "X");
});

test("단위만 다르면 ? — 맞다 · 틀리다 정하지 않음", () => {
  assert.deepEqual(judge("12cm", "12"), { result: "?", why: "단위가 빠졌어요 (정답 cm)" });
  assert.equal(r("3개", "3"), "?");
  assert.equal(r("25%", "25"), "?");
  assert.equal(r("12", "12cm"), "?");
  assert.equal(r("12cm", "12m"), "?");
  assert.match(judge("12cm", "120mm").why, /바꿔 적었어요/);
  assert.equal(r("2시간", "120분"), "?");
  assert.equal(r("1.5L", "1500mL"), "?");
  assert.equal(r("12cm", "1200mm"), "X");          // 값이 다름
});

test("여러 개 답 · 빈 칸", () => {
  assert.equal(r("3, 5", "5,3"), "O");
  assert.equal(r("3cm, 5cm", "5cm,3"), "?");
  assert.equal(r("3, 5", "3,4"), "X");
  assert.equal(r("", "3"), "");
  assert.equal(r("3", " "), "");
});

test("단위 떼기", () => {
  assert.deepEqual(splitUnit("12cm²"), { v: "12", u: "cm²" });
  assert.deepEqual(splitUnit("3/4m"), { v: "3/4", u: "m" });
  assert.deepEqual(splitUnit("5개씩"), { v: "5", u: "개씩" });
  assert.deepEqual(splitUnit("cm"), { v: "cm", u: "" });
  assert.deepEqual(splitUnit("가나다"), { v: "가나다", u: "" });
});
