// node tests/koSearch.test.mjs — 한글 검색(부분일치·초성) + 문항 수 집계
import { koMatch, koFilter, choOf } from "../src/lib/koSearch.js";
import { tallyCounts } from "../src/lib/studyCache.js";

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; } else { fail++; console.log("FAIL -", name); } };

// 부분일치
ok(koMatch("정수", "정수와 유리수"), "부분일치");
ok(koMatch("유리 수", "정수와 유리수"), "질의의 공백 무시");
ok(koMatch("정수와유리수", "정수와 유리수"), "본문의 공백 무시");
ok(!koMatch("절대", "정수와 유리수"), "안 맞으면 false");
ok(koMatch("", "아무거나"), "빈 질의는 항상 true");
ok(koMatch("ABC", "abc 도형"), "영문 대소문자 무시");
ok(koMatch("도형", "정수와 유리수", "기본 도형"), "여러 텍스트 중 하나만 걸려도 됨");

// 초성
ok(choOf("정수와 유리수") === "ㅈㅅㅇㅇㄹㅅ", "초성열 변환");
ok(koMatch("ㅈㅅ", "정수와 유리수"), "초성 검색");
ok(koMatch("ㅇㄹㅅ", "정수와 유리수"), "초성 검색(중간)");
ok(koMatch("ㅉ", "짝수와 홀수"), "된소리 초성");
ok(!koMatch("ㄷㅎ", "정수와 유리수"), "초성 불일치");
ok(!koMatch("정ㅅ", "정수와 유리수"), "음절+초성 혼합 질의는 초성 검색으로 확장하지 않음");

// koFilter — pick 이 준 텍스트들에서, limit 지킴
const rows = [
  { id: 1, title: "정수와 유리수", subtitle: "수직선", unit: "중1-1" },
  { id: 2, title: "절댓값", subtitle: "", unit: "중1-1" },
  { id: 3, title: "기본 도형", subtitle: "", unit: "중1-2" },
];
const pick = (r) => [r.title, r.subtitle, r.unit];
ok(koFilter(rows, "ㅈㄷ", pick).map((r) => r.id).join(",") === "2", "초성으로 절댓값");
ok(koFilter(rows, "수직선", pick)[0]?.id === 1, "부제로도 찾음");
ok(koFilter(rows, "중1-2", pick)[0]?.id === 3, "학기명으로도 찾음");
ok(koFilter(rows, "", pick).length === 3, "빈 질의는 전부");
ok(koFilter(rows, "ㅈ", pick, 1).length === 1, "limit 준수");

// tallyCounts — (unit_id, concept_ids) 행 → 단원·개념별 수
const t = tallyCounts([
  { unit_id: "m1-1", concept_ids: ["m1-1-11"] },
  { unit_id: "m1-1", concept_ids: ["m1-1-11", "m1-1-12"] },
  { unit_id: "m1-2", concept_ids: ["m1-2-01"] },
  { unit_id: "m1-2", concept_ids: [] },
  { unit_id: null, concept_ids: null },
]);
ok(t.unit["m1-1"] === 2 && t.unit["m1-2"] === 2, "단원별 수");
ok(t.concept["m1-1-11"] === 2 && t.concept["m1-1-12"] === 1 && t.concept["m1-2-01"] === 1, "개념별 수(복수 개념 문항 포함)");
ok(Object.keys(t.unit).length === 2, "null 단원은 빠짐");

console.log(`${pass}/${pass + fail} passed`);
if (fail) process.exit(1);
