// node tests/marking.test.mjs — 문장 표시 규칙 엔진(src/lib/marking.js) 검사. 실패 시 exit 1.
import assert from "node:assert/strict";
import { tokenize, autoMark, explain, scoreMarks, practiceEligible, markText, trapText } from "../src/lib/marking.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e.message || e).split("\n").join("\n      ")); }
}
const texts = (tokens, m) => markText(m, tokens);
const byFunc = (marks, f) => marks.filter((m) => m.func === f);

// ── 토큰 왕복 ────────────────────────────────────────────────────────────────
test("tokenize 는 원문을 그대로 복원한다 (\\n · [[마커]] · 공백 포함)", () => {
  const samples = [
    "둘레가 54cm이고, 가로가 세로보다 3cm 더 긴 직사각형의 넓이를 구하시오.",
    "다음 수가 소수인지 합성수인지 쓰시오.\n118",
    "분수 [[frac(1,2)]]과 0.5의 크기를 비교하시오.\n(단, 계산 과정을 쓰시오.)",
    "다음 그림과 같이 [[seg(AB)]] = [[seg(AC)]]인 이등변삼각형 ABC에서  [[seg(BC)]] = 14 cm,\t[[seg(AD)]] = 6 cm일 때, △ABC의 넓이를 구하시오.",
    "두 점 (-1, -9), (1, -1)을 지나는 일차함수의 식을 y = ax + b라 할 때, ab의 값을 구하시오.",
    "(-3ab²)³ = Aaᵐbⁿ일 때, 상수 A, m, n에 대하여 A + m + n의 값을 구하시오.",
    "x에 대한 일차부등식 ax − 6 > 14의 해가 x < -5일 때, 상수 a의 값을 구하시오.",
    "  앞뒤 공백  \n\n두 줄 바꿈  ",
    "",
  ];
  for (const s of samples) {
    const toks = tokenize(s);
    assert.equal(toks.map((t) => t.text).join(""), s, "round-trip: " + JSON.stringify(s));
    toks.forEach((t, i) => assert.equal(t.i, i, "index"));
    for (const t of toks) assert.ok(["word", "num", "math", "punct", "space", "newline"].includes(t.kind), "kind " + t.kind);
  }
});

test("tokenize: 숫자+단위 · 조사 분리 · 마커 · 수식", () => {
  const t1 = tokenize("54cm이고,").map((t) => [t.kind, t.text]);
  assert.deepEqual(t1, [["num", "54cm"], ["word", "이고"], ["punct", ","]]);
  const t2 = tokenize("둘레가 14 cm일 때").filter((t) => t.kind !== "space").map((t) => [t.kind, t.text]);
  assert.deepEqual(t2, [["word", "둘레"], ["word", "가"], ["num", "14 cm"], ["word", "일"], ["word", "때"]]);
  assert.equal(tokenize("[[frac(1,2)]]").length, 1);
  assert.equal(tokenize("[[frac(1,2)]]")[0].kind, "num");                 // 값 마커 = 숫자 정보
  assert.equal(tokenize("[[seg(AB)]]")[0].kind, "math");
  assert.equal(tokenize("[[deg(x)]]")[0].kind, "math");
  const t3 = tokenize("x²-3x+2=0");
  assert.equal(t3.length, 1); assert.equal(t3[0].kind, "math");
  for (const s of ["2x+1", "3/4", "√2", "AB", "∠ABC", "3x", "1/aᵏ"]) assert.equal(tokenize(s)[0].kind, "math", s);
  assert.deepEqual(tokenize("2 : 3이다").filter((t) => t.kind === "num").map((t) => t.text), ["2 : 3"]);
  assert.deepEqual(tokenize("(-1, -9)와 (2, m)").filter((t) => t.kind !== "space").map((t) => t.kind), ["num", "word", "math"]);
  // 띄어 쓴 수식은 한 토큰, (이름 = 값) 은 분리
  assert.equal(tokenize("2x − 6 ≥ 4x + 4를 푸시오")[0].text, "2x − 6 ≥ 4x + 4");
  assert.deepEqual(tokenize("[[seg(BC)]] = 14 cm").filter((t) => t.kind !== "space").map((t) => t.kind), ["math", "punct", "num"]);
  assert.equal(tokenize("270일 때")[0].text, "270");                         // '일' 은 서술어
  assert.equal(tokenize("3일 동안")[0].text, "3일");
  assert.equal(tokenize("12만큼")[0].text, "12");
  assert.equal(tokenize("3배가")[0].text, "3배");
});

// ── 스펙 예제 ────────────────────────────────────────────────────────────────
test("스펙 예제: 54cm·3cm 동그라미, 둘레 밑줄, 쉼표 뒤 빗금 — 가로·세로는 요구하지 않음", () => {
  const s = "둘레가 54cm이고, 가로가 세로보다 3cm 더 긴 직사각형의 넓이를 구하시오.";
  const toks = tokenize(s);
  const marks = autoMark(s);
  const num = byFunc(marks, "NUM").map((m) => texts(toks, m));
  assert.deepEqual(num, ["54cm", "3cm"]);
  const scale = byFunc(marks, "SCALE").map((m) => texts(toks, m));
  assert.deepEqual(scale, ["둘레"]);                                        // 조사 없이 · 세로(보다) 는 아님
  const bound = byFunc(marks, "BOUND");
  assert.equal(bound.length, 1);
  assert.equal(toks[bound[0].t0].text, ",");
  assert.equal(bound[0].required, true);
  assert.ok(marks.every((m) => m.note && m.note.length > 3), "모든 표시에 설명이 있다");
  assert.ok(marks.every((m) => m.tier === 1));
  const ex = explain(s, null);
  assert.equal(ex.asking, "직사각형의 넓이");
  assert.deepEqual(ex.givens, ["둘레가 54cm이고", "가로가 세로보다 3cm 더 긴"]);
  assert.deepEqual(ex.traps, []); assert.deepEqual(ex.prereq, []); assert.equal(ex.discriminates, null);
});

test("수식 문장: 수식 안의 숫자는 동그라미 치지 않는다", () => {
  const s = "이차방정식 x²−3x+2=0의 두 근의 합을 구하시오.";
  const marks = autoMark(s);
  assert.equal(byFunc(marks, "NUM").length, 0);
  const s2 = "일차부등식 2x − 6 ≥ 4x + 4를 푸시오.";
  assert.equal(byFunc(autoMark(s2), "NUM").length, 0);
  // 그러나 (이름 = 값) 의 값과 값 마커는 숫자 정보다
  const s3 = "[[seg(BC)]] = 14 cm, [[angle(A)]] = [[deg(90)]]일 때";
  const toks3 = tokenize(s3);
  assert.deepEqual(byFunc(autoMark(s3), "NUM").map((m) => texts(toks3, m)), ["14 cm", "[[deg(90)]]"]);
});

test("두 문장 문제: 구하는 것 추출 · 조건 분리 · 문장 끝 빗금", () => {
  const s = "편의점에서 한 개에 1200원인 삼각김밥과 한 개에 3500원인 음료수를 합하여 10개 사고 30000원을 냈더니 거스름돈으로 4200원을 받았다. 음료수는 몇 개 샀는지 구하시오.";
  const toks = tokenize(s);
  const ex = explain(s, { labels: { L21_traps: ["조건누락", "구하는대상혼동"], L15_prereq: ["일차방정식의 풀이"], L43_discriminates: "거스름돈을 빼는가" } });
  assert.equal(ex.asking, "음료수는 몇 개 샀는지");
  assert.ok(ex.givens.length >= 2, "조건이 둘 이상");
  assert.ok(ex.givens.every((g) => !g.includes("구하시오")), "구하는 절은 조건에서 빠진다");
  assert.equal(ex.givens.join(" ").includes("4200원"), true);
  const sent = byFunc(ex.marks, "BOUND").filter((m) => m.why === "sentence");
  assert.equal(sent.length, 1); assert.equal(toks[sent[0].t0].text, "."); assert.equal(sent[0].required, true);
  assert.deepEqual(byFunc(ex.marks, "NUM").map((m) => texts(toks, m)), ["1200원", "3500원", "10개", "30000원", "4200원"]);
  assert.deepEqual(ex.traps, ["조건 하나를 빠뜨리기 쉬워요", "무엇을 구하는지 헷갈리기 쉬워요"]);
  assert.deepEqual(ex.prereq, ["일차방정식의 풀이"]);
  assert.equal(ex.discriminates, "거스름돈을 빼는가");
  // 2층: 구하는대상혼동 → 구하는 것에 EMPH (채점 대상 아님)
  const emph = byFunc(ex.marks, "EMPH");
  assert.equal(emph.length, 1); assert.equal(texts(toks, emph[0]), "음료수는 몇 개 샀는지"); assert.equal(emph[0].required, false);
  assert.ok(autoMark(s).every((m) => m.func !== "EMPH"), "autoMark 는 1층만");
});

test("척도: 반지름의 길이 · 학생의 수 · 시속 · 보다/으로 는 척도 아님 · 배수 아님", () => {
  const s = "밑면의 반지름의 길이가 12 cm, 높이가 5 cm인 원기둥과 전체 학생의 수는 900명, 시속 4 km의 속력으로 2시간, 나이의 3배보다 4세 많다";
  const toks = tokenize(s);
  const sc = byFunc(autoMark(s), "SCALE").map((m) => texts(toks, m));
  assert.deepEqual(sc, ["반지름의 길이", "높이", "학생의 수", "시속"]);
});

test("빗금: 연결 어미는 보너스 · 나열 쉼표는 없음 · 마지막 문장부호는 없음", () => {
  const s = "두 자연수 A, B의 곱이 2430이고 최소공배수가 270일 때, 두 수의 최대공약수를 구하시오.";
  const toks = tokenize(s);
  const b = byFunc(autoMark(s), "BOUND").map((m) => [toks[m.t0].text, m.required]);
  assert.deepEqual(b, [["이고", false], [",", true]]);
  const s2 = "수직선 위의 두 점 A, B가 나타내는 수가 각각 -8, -6이다.";
  assert.equal(byFunc(autoMark(s2), "BOUND").length, 0);
  const s3 = "다음 중 소수인 것은?";
  assert.equal(byFunc(autoMark(s3), "BOUND").length, 0);
  assert.equal(explain(s3).asking, "다음 중 소수인 것");
});

test("의문사가 있는 절은 통째로 구하는 것", () => {
  assert.equal(explain("시속 4 km의 속력으로 2시간 동안 걸은 거리는 몇 km인지 구하시오.").asking, "시속 4 km의 속력으로 2시간 동안 걸은 거리는 몇 km인지");
  assert.equal(explain("마스크 팩을 몇 장 이상 살 때 온라인 뷰티몰에서 사는 것이 유리한지 구하시오.").asking, "마스크 팩을 몇 장 이상 살 때 온라인 뷰티몰에서 사는 것이 유리한지");
  const ex = explain("중심각의 크기가 [[deg(90)]]이고 호의 길이가 [[5 * pi]] cm인 부채꼴의 반지름의 길이를 구하시오.");
  assert.equal(ex.asking, "부채꼴의 반지름의 길이");
  assert.deepEqual(ex.givens, ["중심각의 크기가 [[deg(90)]]이고", "호의 길이가 [[5 * pi]] cm인"]);
  const ex2 = explain("분수 [[frac(1,2)]]과 0.5의 크기를 비교하시오.\n(단, 계산 과정을 쓰시오.)");
  assert.equal(ex2.asking, "분수 [[frac(1,2)]]과 0.5의 크기");
  assert.deepEqual(ex2.givens, ["단, 계산 과정을 쓰시오"]);
  const ex3 = explain("ㄱ. 2는 소수이다.\nㄴ. 9는 소수이다.\n다음 중 옳은 것을 모두 고르시오.");
  assert.equal(ex3.asking, "다음 중 옳은 것");
  assert.deepEqual(ex3.givens, ["ㄱ. 2는 소수이다", "ㄴ. 9는 소수이다"]);
  // 자료 목록 · 줄머리 번호는 숫자 정보가 아니다
  const ex4 = explain("다음은 어느 학생의 점수이다. 이 자료의 중앙값이 26.5일 때, x의 값을 구하시오.  [ 31, 22, x, 34 ]  (단위: 점)");
  assert.equal(ex4.asking, "x의 값");
  assert.deepEqual(byFunc(ex4.marks, "NUM").map((m) => texts(ex4.tokens, m)), ["26.5"]);
  assert.deepEqual(byFunc(autoMark("1. 첫째 조건\n2. 둘째 조건 5개"), "NUM").length, 1);
});

// ── 채점 ─────────────────────────────────────────────────────────────────────
test("scoreMarks: hit / missed / extra / score", () => {
  const s = "둘레가 54cm이고, 가로가 세로보다 3cm 더 긴 직사각형의 넓이를 구하시오.";
  const toks = tokenize(s);
  const key = autoMark(s);                      // NUM 54cm, NUM 3cm, SCALE 둘레, BOUND ,
  const idx = (txt) => toks.find((t) => t.text === txt).i;
  const user = [
    { kind: "span", t0: idx("54cm"), t1: idx("54cm"), func: "NUM" },
    { kind: "span", t0: idx("둘레"), t1: idx("둘레"), func: "SCALE" },
    { kind: "point", t0: idx("이고"), func: "BOUND" },                     // 쉼표 바로 앞 낱말 뒤 → 위치 차 1 → 맞음
    { kind: "span", t0: idx("가로"), t1: idx("가로"), func: "SCALE" },    // 키에 없음 → extra
    { kind: "span", t0: idx("넓이"), t1: idx("넓이"), func: "EMPH" },     // 2층 → 무시
  ];
  const r = scoreMarks(user, key, toks);
  assert.equal(r.required, 4);
  assert.equal(r.hit, 3);
  assert.equal(r.missed.length, 1); assert.equal(texts(toks, r.missed[0]), "3cm");
  assert.equal(r.extra.length, 1); assert.equal(texts(toks, r.extra[0]), "가로");
  assert.equal(r.score, 75);
  assert.equal(r.detail.length, 4);
  assert.equal(r.detail.filter((d) => d.matched).length, 3);
  // 빈 키 → 100, 아무 표시 없음 → 0
  assert.equal(scoreMarks([], [], toks).score, 100);
  assert.equal(scoreMarks([], key, toks).score, 0);
  // 겹침 50% 규칙: "반지름의 길이" 키에 "길이" 만 밑줄 → 맞음, 두 칸 떨어진 빗금 → 틀림
  const s2 = "반지름의 길이가 12 cm, 높이가 5 cm인 원기둥의 부피를 구하시오.";
  const toks2 = tokenize(s2), key2 = autoMark(s2);
  const i2 = (txt) => toks2.find((t) => t.text === txt).i;
  const r2 = scoreMarks([{ kind: "span", t0: i2("길이"), t1: i2("길이"), func: "SCALE" }, { kind: "point", t0: i2("부피"), func: "BOUND" }], key2, toks2);
  assert.equal(r2.detail.find((d) => d.key.func === "SCALE" && texts(toks2, d.key) === "반지름의 길이").matched != null, true);
  assert.equal(r2.extra.length, 1);                                          // '부피' 뒤 빗금은 어느 키와도 두 칸 이상 떨어짐
  const r2b = scoreMarks([{ kind: "point", t0: i2("원기둥의"), func: "BOUND" }], key2, toks2);
  assert.equal(r2b.extra.length, 0); assert.equal(r2b.bonusHit, 1);          // '인' 뒤 보너스 키와 한 칸 차이 → 맞음
  // 보너스 키(연결 어미)는 required 에 안 들어가고 맞혀도 점수에 영향 없음
  const s3 = "곱이 2430이고 최소공배수가 270일 때, 최대공약수를 구하시오.";
  const toks3 = tokenize(s3), key3 = autoMark(s3);
  const r3 = scoreMarks([{ kind: "point", t0: toks3.find((t) => t.text === "이고").i, func: "BOUND" }], key3, toks3);
  assert.equal(r3.bonusHit, 1); assert.equal(r3.extra.length, 0);
  assert.equal(r3.required, key3.filter((m) => m.required).length);
});

test("practiceEligible: 30자 미만이거나 필수 표시가 2개 미만이면 제외", () => {
  assert.equal(practiceEligible("다음 중 소수인 것은?"), false);
  assert.equal(practiceEligible("1부터 19까지의 자연수 중에서 소수는 모두 몇 개인지 구하시오."), false);   // 29자
  assert.equal(practiceEligible("둘레가 54cm이고, 가로가 세로보다 3cm 더 긴 직사각형의 넓이를 구하시오."), true);
  assert.equal(practiceEligible("이차방정식 x²−3x+2=0의 두 근의 합과 두 근의 곱을 각각 구하여 더한 값을 구하시오."), false);  // 표시할 숫자 없음
  assert.equal(practiceEligible(""), false);
  assert.equal(practiceEligible(null), false);
});

test("함정 사전 · 널 안전", () => {
  assert.equal(trapText("부호"), "부호(+, −)를 놓치기 쉬워요");
  assert.equal(trapText("단위"), "단위를 맞추는 걸 잊기 쉬워요");
  assert.equal(trapText("낯선태그"), "낯선태그");
  const ex = explain("둘레가 54cm이고, 가로가 세로보다 3cm 더 긴 직사각형의 넓이를 구하시오.", { labels: null });
  assert.deepEqual(ex.traps, []);
  const ex2 = explain("", null);
  assert.deepEqual(ex2.tokens, []); assert.deepEqual(ex2.marks, []); assert.equal(ex2.asking, null); assert.deepEqual(ex2.givens, []);
  assert.deepEqual(autoMark("   \n  "), []);
});

console.log(`\n${n - failed}/${n} passed`);
if (failed) process.exit(1);
