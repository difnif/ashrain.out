// 강사도구 — 교재 기록: 쪽 읽기 · 진도 칸 · 채점 기록이 없는 쪽 어림 · 채점한 날 (node --test tests/ttbooks.test.mjs)
import { test } from "node:test";
import assert from "node:assert/strict";
import { parsePages, fmtPages, mergeRanges, subtractRanges, parseProgress, uncheckedPages, gradedDays, daysBetween, roundsInfo, gradingStats } from "../src/apps/seirocco/tt/logic.js";

test("쪽 읽기 — 범위 · 쉼표 · 띄어쓰기 · 쪽/p/~ 표기, 겹치면 합침", () => {
  assert.deepEqual(parsePages("12-20, 25"), [[12, 20], [25, 25]]);
  assert.deepEqual(parsePages("12 ~ 20쪽 25쪽"), [[12, 20], [25, 25]]);
  assert.deepEqual(parsePages("p.30-32, 31-35, 36"), [[30, 36]]);
  assert.deepEqual(parsePages("20-12"), [[12, 20]]);
  assert.deepEqual(parsePages(""), []);
  assert.equal(parsePages("12-20, abc"), null);
  assert.equal(parsePages("1-2-3"), null);
  assert.equal(fmtPages([[12, 20], [25, 25]]), "12-20, 25");
  assert.deepEqual(mergeRanges([[5, 6], [1, 3], [4, 4]]), [[1, 6]]);
});

test("범위 빼기", () => {
  assert.deepEqual(subtractRanges([[1, 20]], [[5, 8], [15, 30]]), [[1, 4], [9, 14]]);
  assert.deepEqual(subtractRanges([[1, 5]], [[1, 5]]), []);
  assert.deepEqual(subtractRanges([[10, 12]], []), [[10, 12]]);
});

test("진도 칸 — 「45」 = 45쪽까지, 「30-45」 = 범위, 비면 empty, 못 읽으면 null", () => {
  assert.deepEqual(parseProgress("45"), { to: 45, pages: "" });
  assert.deepEqual(parseProgress("45쪽까지"), { to: 45, pages: "" });
  assert.deepEqual(parseProgress("30~45"), { to: 45, pages: "30-45" });
  assert.deepEqual(parseProgress("45-30"), { to: 45, pages: "30-45" });
  assert.deepEqual(parseProgress("  "), { empty: true });
  assert.equal(parseProgress("12, 14"), null);
  assert.equal(parseProgress("사십오"), null);
});

test("채점 기록이 없는 쪽 어림 — 앞 진도 다음 쪽부터, 첫 진도는 채점 기록의 첫 쪽부터", () => {
  const solved = [{ page_to: 20, pages: "" }, { page_to: 32, pages: "" }, { page_to: 40, pages: "" }];
  // 12-20 · 21-28 채점 → 29-40 이 남음
  assert.deepEqual(uncheckedPages(solved, [{ pages: "12-20" }, { pages: "21-28" }]), { known: true, ranges: [[29, 40]], text: "29-40" });
  // 중간 구멍도 보임
  assert.equal(uncheckedPages(solved, [{ pages: "12-20, 25-40" }]).text, "21-24");
  // 다 채점
  assert.equal(uncheckedPages(solved, [{ pages: "12-40" }]).text, "");
  // 채점 쪽 기록이 없으면 어림하지 않음
  assert.deepEqual(uncheckedPages(solved, [{ pages: "" }]), { known: false, ranges: [], text: "" });
  // 범위로 적은 진도는 그 범위
  assert.equal(uncheckedPages([{ page_to: 50, pages: "45-50" }], [{ pages: "45-47" }]).text, "48-50");
  // 뒤로 간 진도(다시 풀기)는 새 범위를 만들지 않음
  assert.equal(uncheckedPages([{ page_to: 30, pages: "" }, { page_to: 25, pages: "" }], [{ pages: "10-30" }]).text, "");
});

test("두 날 사이 일수", () => {
  assert.equal(daysBetween("2026-11-20", "2026-11-27"), 7);
  assert.equal(daysBetween("2026-11-27", "2026-11-27"), 0);
  assert.equal(daysBetween("2026-10-31", "2026-11-01"), 1);
});

test("채점한 날 — 차마다 매긴 날(처음 · 마지막), 셈에서 빠진 기록은 빼고", () => {
  const sessions = [{ no: 1, round: 1, kind: "solve", targets: null }, { no: 2, round: 2, kind: "retry", targets: [2] }];
  const at = (d) => new Date(d + "T12:00:00").toISOString();       // 이 기기 시간대의 그날 낮
  const marks = [
    { id: 1, seq: 1, result: "O", session_no: 1, at: at("2026-11-20") },
    { id: 2, seq: 2, result: "X", session_no: 1, at: at("2026-11-21") },
    { id: 3, seq: 2, result: "O", session_no: 2, at: at("2026-11-25") },
    { id: 4, seq: 1, result: "O", session_no: 2, at: at("2026-11-26") },   // 2차 대상이 아님 → 셈에서 빠짐
  ];
  assert.deepEqual(gradedDays(marks, sessions), [
    { round: 1, first: "2026-11-20", last: "2026-11-21", n_days: 2 },
    { round: 2, first: "2026-11-25", last: "2026-11-25", n_days: 1 },
  ]);
  const ri = roundsInfo(sessions, marks, [1, 2]);
  assert.equal(ri[0].graded_first, "2026-11-20");
  assert.equal(ri[1].graded_last, "2026-11-25");
  assert.equal(gradingStats(marks, sessions, 2).graded_days.length, 2);
});
