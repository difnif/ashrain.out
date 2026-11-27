// 강사도구 — 재원 · 원비: 달 계산 · 원비 칸 읽기 · 노랑/빨강 · 달마다 매출 (node --test tests/ttmonths.test.mjs)
import { test } from "node:test";
import assert from "node:assert/strict";
import { monthStart, addMonths, monthLabel, parseFee, fmtMan, fmtWon, monthFlag, monthTotals } from "../src/apps/seirocco/tt/logic.js";

test("달 — 그달 1일 · 앞뒤 달 · 해 넘김", () => {
  assert.equal(monthStart("2026-11-27"), "2026-11-01");
  assert.equal(addMonths("2026-11-01", 1), "2026-12-01");
  assert.equal(addMonths("2026-12-01", 1), "2027-01-01");
  assert.equal(addMonths("2026-01-01", -1), "2025-12-01");
  assert.equal(addMonths("2026-03-01", -12), "2025-03-01");
  assert.equal(monthLabel("2026-03-01"), "3월");
});

test("원비 칸 — 숫자 · 쉼표 · 만 · 천, 비면 null, 못 읽으면 NaN", () => {
  assert.equal(parseFee("300000"), 300000);
  assert.equal(parseFee("300,000원"), 300000);
  assert.equal(parseFee("30만"), 300000);
  assert.equal(parseFee("35.5만"), 355000);
  assert.equal(parseFee("30만 5천"), 305000);
  assert.equal(parseFee("5천"), 5000);
  assert.equal(parseFee(""), null);
  assert.equal(parseFee("  "), null);
  assert.ok(Number.isNaN(parseFee("삼십만")));
  assert.ok(Number.isNaN(parseFee("30만원쯤")));
  assert.equal(fmtMan(300000), "30만");
  assert.equal(fmtMan(305000), "30만 5천");
  assert.equal(fmtMan(12345), "12,345원");
  assert.equal(fmtWon(1500000), "1,500,000원");
});

test("재원 표시 — 적었으면 그 상태, 안 적었으면 노랑(지난달 있음 · 처음) · 빨강(지난달도 비었음), 그만둔 학생 · 기록 없는 쉬는 학생은 안 물음", () => {
  const cur = "2026-11-01";
  const rows = [
    { student_id: 1, month: "2026-11-01", status: "attend", fee: 300000, note: "" },
    { student_id: 2, month: "2026-10-01", status: "attend", fee: 300000, note: "" },
    { student_id: 3, month: "2026-08-01", status: "pause", fee: null, note: "" },
    { student_id: 4, month: "2026-09-01", status: "quit", fee: null, note: "" },
    { student_id: 6, month: "2026-12-01", status: "attend", fee: 1, note: "" },          // 앞 달 기록은 안 봄
  ];
  assert.equal(monthFlag({ id: 1, active: true }, rows, cur).status, "attend");
  assert.equal(monthFlag({ id: 2, active: true }, rows, cur).flag, "y");
  assert.equal(monthFlag({ id: 3, active: false }, rows, cur).flag, "r");
  const q = monthFlag({ id: 4, active: false }, rows, cur);
  assert.equal(q.flag, ""); assert.equal(q.quit, true);
  assert.equal(monthFlag({ id: 5, active: true }, rows, cur).flag, "y");               // 기록이 하나도 없는 다니는 학생
  assert.equal(monthFlag({ id: 5, active: false }, rows, cur).flag, "");               // 기록 없이 쉬는 중인 옛 학생
  assert.equal(monthFlag({ id: 6, active: true }, rows, cur).flag, "y");
});

test("달마다 모아 보기 — 매출은 다님 원비 합, 원비 안 적은 다님 수", () => {
  const rows = [
    { student_id: 1, month: "2026-11-01", status: "attend", fee: 300000 },
    { student_id: 2, month: "2026-11-01", status: "attend", fee: null },
    { student_id: 3, month: "2026-11-01", status: "pause", fee: 300000 },
    { student_id: 4, month: "2026-11-01", status: "quit", fee: null },
    { student_id: 1, month: "2026-10-01", status: "attend", fee: 280000 },
  ];
  assert.deepEqual(monthTotals(rows, "2026-11-01"), { month: "2026-11-01", attend: 2, pause: 1, quit: 1, revenue: 300000, no_fee: 1, entered: 4 });
  assert.equal(monthTotals(rows, "2026-10-01").revenue, 280000);
  assert.equal(monthTotals(rows, "2026-09-01").entered, 0);
});

import { gradeKey, feeFor, planStart } from "../src/apps/seirocco/tt/logic.js";
test("원비표 — 학년 글자 읽기 · 그달 원비표에서 학년 · 주당 횟수로 원비", () => {
  assert.equal(gradeKey("초4"), "초4"); assert.equal(gradeKey("초등 4학년"), "초4"); assert.equal(gradeKey("중2"), "중2");
  assert.equal(gradeKey("고등학교 1학년"), "고1"); assert.equal(gradeKey("4학년"), null); assert.equal(gradeKey("중4"), null); assert.equal(gradeKey(""), null);
  const plans = [   // 시험용 값(실제 원비표 아님)
    { start_month: "2024-01-01", level: "A", grades: ["초4"], per_week: 3, fee: 100 },
    { start_month: "2024-01-01", level: "B", grades: ["중1", "중2", "중3"], per_week: 2, fee: 300 },
    { start_month: "2026-01-01", level: "A2", grades: ["초1", "초2", "초3", "초4"], per_week: 3, fee: 90 },
    { start_month: "2026-01-01", level: "B", grades: ["중1", "중2", "중3"], per_week: 2, fee: 300 },
  ];
  assert.equal(planStart(plans, "2025-12-01"), "2024-01-01");
  assert.equal(feeFor(plans, "2025-06-01", "초4", 3).fee, 100);
  assert.equal(feeFor(plans, "2026-01-01", "초4", 3).fee, 90);
  assert.equal(feeFor(plans, "2025-06-01", "초2", 3), null);          // 그때는 받지 않은 학년
  assert.equal(feeFor(plans, "2026-03-01", "초2", 3).level, "A2");
  assert.equal(feeFor(plans, "2026-03-01", "중2", 3), null);          // 그 주당 횟수는 원비표에 없음
  assert.equal(feeFor(plans, "2023-12-01", "중2", 2), null);          // 원비표가 시작되기 전
});

import { parseGrades, fmtGrades, perWeekOpts, suggestFee } from "../src/apps/seirocco/tt/logic.js";
test("원비표 학년 칸 · 주당 횟수 · 원비 채우기(원비표가 바뀐 달 · 할인 · 3월에 학년이 오름)", () => {
  assert.deepEqual(parseGrades("초1-4"), ["초1", "초2", "초3", "초4"]);
  assert.deepEqual(parseGrades("초등 5~6학년"), ["초5", "초6"]);
  assert.deepEqual(parseGrades("중등"), ["중1", "중2", "중3"]);
  assert.deepEqual(parseGrades("초5,6 중1"), ["초5", "초6", "중1"]);
  assert.equal(parseGrades("중4"), null); assert.equal(parseGrades("4학년"), null); assert.equal(parseGrades(""), null);
  assert.equal(fmtGrades(["중3", "중1", "중2"]), "중1-3"); assert.equal(fmtGrades(["초1", "초3", "고2"]), "초1,3 고2");
  const plans = [   // 시험용 값(실제 원비표 아님)
    { start_month: "2025-01-01", level: "E", grades: ["초5", "초6"], per_week: 2, fee: 100 }, { start_month: "2025-01-01", level: "E", grades: ["초5", "초6"], per_week: 3, fee: 120 },
    { start_month: "2025-01-01", level: "M", grades: ["중1", "중2", "중3"], per_week: 2, fee: 200 },
    { start_month: "2026-01-01", level: "E", grades: ["초5", "초6"], per_week: 2, fee: 110 }, { start_month: "2026-01-01", level: "E", grades: ["초5", "초6"], per_week: 3, fee: 130 },
    { start_month: "2026-01-01", level: "M", grades: ["중1", "중2", "중3"], per_week: 2, fee: 210 },
  ];
  assert.deepEqual(perWeekOpts(plans, "2026-05-01"), [2, 3]);
  assert.deepEqual(perWeekOpts([], "2026-05-01", [1]), [1, 2, 3]);
  const att = (fee, pw) => ({ status: "attend", fee, per_week: pw });
  // 원비표대로 내던 학생 → 원비표가 바뀐 달에 새 원비
  assert.deepEqual([suggestFee(plans, "2026-01-01", "초5", 2, att(100, 2)).fee, suggestFee(plans, "2026-01-01", "초5", 2, att(100, 2)).src], [110, "plan"]);
  // 할인(원비표와 달랐음) → 지난달 원비 그대로(special)
  const sp = suggestFee(plans, "2026-01-01", "초5", 2, att(90, 2));
  assert.equal(sp.fee, 90); assert.equal(sp.special, true);
  // 주당 횟수가 바뀌면 원비표 값
  assert.equal(suggestFee(plans, "2026-02-01", "초5", 3, att(110, 2)).fee, 130);
  // 주당 횟수를 안 고르면 지난달 원비, 지난달도 없으면 null
  assert.equal(suggestFee(plans, "2026-02-01", "초5", null, att(110, null)).fee, 110);
  assert.equal(suggestFee(plans, "2026-02-01", "초5", null, null), null);
  // 원비표에 없는 학년 → 지난달 원비
  assert.equal(suggestFee(plans, "2026-02-01", "고1", 2, att(300, 2)).fee, 300);
  // 3월: 초6 → 중1로 오른 학생이 2월에 초등 원비표대로 냈으면 중등 원비
  assert.equal(suggestFee(plans, "2026-03-01", "중1", 2, att(110, 2)).fee, 210);
  // 3월에도 할인이던 학생은 그대로
  assert.equal(suggestFee(plans, "2026-03-01", "중2", 2, att(150, 2)).fee, 150);
});

