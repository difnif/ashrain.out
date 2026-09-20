// node tests/retention.test.mjs — 촬영 답안 보관 게이트(src/lib/retention.js) 검사. 실패 시 exit 1.
import assert from "node:assert/strict";
import {
  plainMath, normalize, sentencesOf, numbersOf, contentWords, longestCommonRun, restatedSentences,
  overlapScore, decideRetention, buildLabels, normalizePolicy, OVERLAP_LOW, OVERLAP_HIGH,
} from "../src/lib/retention.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e.message || e).split("\n").join("\n      ")); }
}

const Q1 = "소금물 300 g에 소금 45 g이 녹아 있다. 여기에 물 200 g을 더 넣으면 소금물의 농도는 몇 %가 되는지 구하시오.";
const A1_ROUGH = "45/(300+200) × 100 = 45/500 × 100 = 9 ∴ 9%";
const A1_NEAT = "소금물 300 g에 소금 45 g이 녹아 있다. 물 200 g을 더 넣으면 소금물은 500 g이 되므로 농도는 45/500 × 100 = 9(%)이다.";
const A1_OTHER = "x + y = 10, 2x − y = 5 → x = 5, y = 5";

test("plainMath: 마커를 평문으로", () => {
  assert.equal(plainMath("[[frac(1,2)]] + [[pow(x,2)]] = [[deg(90)]]"), "1/2 + x^2 = 90°");
  assert.equal(plainMath("[[seg(AB)]] 와 [[angle(ABC)]]"), "AB 와 ∠ABC");
});
test("normalize: 마이너스·공백 통일", () => {
  assert.equal(normalize("x −  3  = −5"), "x - 3 = -5");
});
test("sentencesOf: 10자 이상 문장만", () => {
  const s = sentencesOf(Q1);
  assert.equal(s.length, 2);
});
test("numbersOf: 0·1·2 는 제외, 분수·비 포함", () => {
  const s = numbersOf("2개의 주사위, 확률 1/6, 비 3:4, 값 12.5, 답 1");
  assert.ok(s.has("1/6") && s.has("3:4") && s.has("12.5"));
  assert.ok(!s.has("1") && !s.has("2"));
});
test("contentWords: 조사 떼고 기능어 제외", () => {
  const w = contentWords(Q1);
  assert.ok(w.has("소금물") && w.has("소금") && w.has("농도"));
  assert.ok(!w.has("구하시오") && !w.has("몇"));
});
test("longestCommonRun: 공백 무시 최장 공유 문자열", () => {
  const r = longestCommonRun("소금물 300 g에 소금", "물 200 g을 넣으면 소금물300g에소금이");
  assert.ok(r.len >= 9, "len " + r.len);
});
test("restatedSentences: 정연 답안은 첫 문장을 재진술", () => {
  assert.equal(restatedSentences(Q1, A1_NEAT).length, 1);
  assert.equal(restatedSentences(Q1, A1_ROUGH).length, 0);
});
test("overlapScore: 거친 < 정연, 무관 답안은 낮음", () => {
  const r = overlapScore(Q1, A1_ROUGH), nn = overlapScore(Q1, A1_NEAT), o = overlapScore(Q1, A1_OTHER);
  assert.ok(r.score < nn.score, `${r.score} < ${nn.score}`);
  assert.equal(o.level, "low");
  assert.equal(nn.level, "high", "neat " + nn.score);
  assert.ok(r.score >= 0 && r.score <= 100);
  assert.equal(r.sentences, 0); assert.equal(nn.sentences, 1);
  assert.ok(r.nums >= 2, "shared nums " + r.nums);
});
test("overlapScore: 빈 입력은 0", () => {
  const z = overlapScore("", "");
  assert.equal(z.score, 0); assert.equal(z.level, "low");
});
test("decideRetention: labels 정책은 항상 기기", () => {
  for (const g of ["S", "M", "C", null])
    assert.equal(decideRetention({ grade: g, overlap: { level: "low" }, policy: "labels" }).where, "device");
});
test("decideRetention: gated 매트릭스", () => {
  const lo = { level: "low" }, hi = { level: "high" }, mid = { level: "mid" };
  assert.equal(decideRetention({ grade: "S", overlap: hi, policy: "gated" }).where, "central");
  assert.equal(decideRetention({ grade: "M", overlap: lo, policy: "gated" }).where, "central");
  assert.equal(decideRetention({ grade: "M", overlap: mid, policy: "gated" }).where, "device");
  assert.equal(decideRetention({ grade: "M", overlap: hi, policy: "gated" }).where, "device");
  assert.equal(decideRetention({ grade: "C", overlap: lo, policy: "gated" }).where, "device");
  assert.equal(decideRetention({ grade: null, overlap: lo, policy: "gated" }).where, "device");
});
test("decideRetention: all 은 중앙, 모르는 정책은 기본값(labels)", () => {
  assert.equal(decideRetention({ grade: "C", overlap: { level: "high" }, policy: "all" }).where, "central");
  assert.equal(normalizePolicy("whatever"), "labels");
  assert.equal(decideRetention({ grade: "S", overlap: { level: "low" }, policy: "whatever" }).where, "device");
});
test("buildLabels: 텍스트 없이 라벨만", () => {
  const ov = overlapScore(Q1, A1_ROUGH);
  const lab = buildLabels({ feature: "essay", std: { item_grade: "M", sub_type: "단순 소재 대입형", elements: { 발문: "S" }, unit: "m1-1" }, overlap: ov,
    result: { total: 6, max: 8, verdict: "ok", pitfall_tags: ["단위"], criteria: { 충실성: { light: "green" } } } });
  assert.equal(lab.std_grade, "M"); assert.equal(lab.score, 6); assert.equal(lab.lights.충실성, "green");
  assert.equal(lab.overlap_score, ov.score);
  const json = JSON.stringify(lab);
  assert.ok(!json.includes("소금물") && !json.includes("45/"), "라벨에 본문이 섞임");
});
test("임계값 상수는 순서가 맞다", () => { assert.ok(OVERLAP_LOW < OVERLAP_HIGH); });

console.log(`\n${n - failed}/${n} passed`);
if (failed) process.exit(1);
