// node tests/gyeokeon.test.mjs — 시록고 격언 도우미: 고르기(= pick_gy.py) · 보고서 문장 · PRZ-1 코드 읽기 · 데이터 검사
import { readFileSync } from "node:fs";
import { pickMonths, fillReport, nameWithTopic, dominantType, monthContext, teacherCard } from "../src/apps/seirocco/gyeokeon/gyPick.js";
import { parseCodeLine, monthsFromCodes } from "../src/apps/seirocco/gyeokeon/codeline.js";

const read = (p) => JSON.parse(readFileSync(new URL(p, import.meta.url), "utf8"));
const data = read("../public/gyeokeon/gyeokeon.v2.json");
const fx = read("./fixtures/gyeokeon-pick.fixture.json");

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; } else { fail++; console.log("FAIL -", name); } };

// 1) 고르기 — pick_gy.py가 낸 답(합성 학생, 실제 학생 아님)과 한 달도 다르지 않아야 한다
let months = 0, same = 0;
for (const st of fx.students) {
  const got = pickMonths(st.name, st.months, data.entries).map((p) => p.id);
  months += got.length;
  got.forEach((id, j) => { if (id === st.expect[j]) same++; });
}
ok(months > 900 && same === months, `고르기 ${same}/${months}달이 pick_gy.py와 같음`);

// 2) 보고서 문장 · 조사
for (const r of fx.reports) ok(fillReport(data.entries.find((e) => e.id === r.id), r.short, r.cum) === r.expect, "보고서 문장 " + r.id);
for (const [a, b] of [["소현", "소현이는"], ["러비", "러비는"], ["가원", "가원이는"], ["지후", "지후는"], ["Amy", "Amy는"]]) ok(nameWithTopic(a) === b, "조사 " + a);

// 3) 주 유형 — S의 가장 큰 몫, 동점 · 미분화 · 0이면 없음
const S0 = { rush: 0, shadow: 0, cross: 0, steady: 0, stubborn: 0, cue: 0, evap: 0, shrink: 0, auto: 0 };
ok(dominantType({ ...S0, steady: 0.5, cue: 0.2 }) === "steady", "주 유형 하나");
ok(dominantType({ ...S0, steady: 0.4, cue: 0.4 }) === null, "동점이면 없음");
ok(dominantType(Object.fromEntries(Object.keys(S0).map((k) => [k, 2 / 15]))) === null, "미분화(222222222)면 없음");
ok(dominantType(S0) === null, "모두 0이면 없음");
// 달 기록의 dom 칸(주 렌즈)은 읽지 않는다
const base = { label: "2026.1", who: "P", S: { ...S0, steady: 0.6, cue: 0.2 }, dacc: 0, cum: 500, n: 500, med_n: 500, band: { vol: 1 } };
ok(monthContext({ ...base, dom: null }, 1, 0).s.none === 0 && monthContext({ ...base, dom: "cause" }, 1, 0).s.none === 0, "dom 칸과 무관");
ok(monthContext({ ...base, n: 300 }, 1, 0).R === 2 && monthContext({ ...base, R: 5 }, 1, 0).R === 5, "R 밴드: n/med_n 또는 코드 값");

// 4) PRZ-1 코드 읽기
const L1 = "PRZ1 하늘·중2 2610#02 │ 3312↑40 │ P1 │ 62C0·120000 │ 302150040 │ 000000000 │ 000000000 │ Σ013";
const m1 = parseCodeLine(L1);
ok(!m1.error && m1.short === "하늘" && m1.grade === "중2" && m1.label === "2026.10" && m1.nth === 2, "머리");
ok(m1.who === "P" && m1.seen && m1.vb === 2 && m1.R === 4 && m1.dacc === 1 && m1.cum === 1300, "입사광 · 관측 · 누적");
ok(m1.type === "stubborn" && Math.abs(m1.S.stubborn - 5 / 15) < 1e-12, "스펙트럼 16진 → 몫 · 주 유형");
ok(parseCodeLine(L1.replace("P1", "A0")).who === "AI" && parseCodeLine(L1.replace("P1", "E0")).who === "E", "관측자 A → AI, E");
ok(!!parseCodeLine("PRZ1 하늘 │ 1").error && !!parseCodeLine(L1.replace("Σ013", "S013")).error
  && !!parseCodeLine(L1.replace("302150040", "30215004")).error, "못 읽는 줄은 error");
const mixed = [
  "PRZ1 하늘·중2 2611#03 │ 4321↑30 │ P1 │ 55C0·110100 │ 100752000 │ 000000000 │ 000000000 │ Σ021", L1,
  "PRZ1 바다·초5 2605#05 │ 2213↓20 │ O1 │ 40N0·300000 │ 000900600 │ 000000000 │ 000000000 │ Σ034", "아무 글", "깨진 │ 줄",
].join("\n");
const g = monthsFromCodes(mixed);
ok(g.students.length === 2 && g.errors.length === 1 && g.errors[0].line === 5, "학생별로 나누고 깨진 줄만 알림");
const ha = g.students.find((s) => s.short === "하늘"), ba = g.students.find((s) => s.short === "바다");
ok(ha.months.map((m) => m.nth).join() === "2,3" && ha.months[1].prevCum === 1300, "순번 차례 · 앞달 누적");
ok(!ha.fromFirst && ha.months[0].prevCum === ha.months[0].cum, "첫 달이 아니면 첫 줄에서 누적 사건이 안 터짐");
// 5번째 달(누적 3,400)부터 넣어도 1,000 · 3,000 사건이 그 줄에 붙지 않는다
const evIds = new Set(data.entries.filter((e) => e.event && e.event.sigCross).map((e) => e.id));
ok(!evIds.has(pickMonths(ba.short, ba.months, data.entries)[0].id), "중간부터 넣은 첫 줄에 누적 사건 없음");
// 첫 달부터 넣으면 1,000을 넘는 달에 一勺之多(누적 1,000)가 후보로 크게 앞선다
const fromFirst = monthsFromCodes([
  "PRZ1 바다·초5 2601#01 │ 2213○30 │ P1 │ 40N0·300000 │ 222222222 │ 000000000 │ 000000000 │ Σ006",
  "PRZ1 바다·초5 2602#02 │ 2213↑30 │ P1 │ 40N0·300000 │ 222222222 │ 000000000 │ 000000000 │ Σ012",
].join("\n")).students[0];
const pk = pickMonths(fromFirst.short, fromFirst.months, data.entries);
ok(pk[0].entry.label === "志于學" && pk[1].entry.label === "一勺之多", "첫 달 志于學 · 1,000문항 넘는 달 一勺之多");
ok(pickMonths("바다", fromFirst.months, data.entries).map((p) => p.id).join() === pk.map((p) => p.id).join(), "같은 코드면 같은 격언");

// 5) 데이터
const ids = new Set(data.entries.map((e) => e.id));
ok(data.entries.length === 1009 && ids.size === data.entries.length && data.count === data.entries.length, "1,009개 · 번호 겹침 없음");
ok(data.entries.every((e) => (e.report.match(/\{N\}/g) || []).length === 1), "보고서 문장마다 {N} 하나");
ok(data.entries.every((e) => !e.report.includes("{C}") || (e.event && e.event.sigCross)), "{C}는 누적 사건 항목에만");
const keys = new Set(data.types.map((t) => t.key)), groups = new Set(data.books.map((b) => b.group));
ok(data.entries.every((e) => keys.has(e.primary) && groups.has(e.book_group) && e.kid && e.story && e.src), "유형 · 갈래 · 아이에게 · 고사 · 출전");
ok(data.entries.every((e) => ["원문 텍스트", "웹 인용 대조"].includes(e.check.how)), "모두 원문 대조됨");
ok(!JSON.stringify(data.entries).includes("정답률"), "항목 글 어디에도 정답률 없음");
const tc = teacherCard(data.entries.find((e) => Object.keys(e.check.edition_chars).length));
ok(tc.edition.startsWith("대조 판본 표기:") && tc.checked.startsWith("원문 대조:"), "선생님 카드 판본 · 대조 줄");

console.log(fail ? `실패 ${fail} · 통과 ${pass}` : `통과 ${pass} — 고르기 ${months}달 · 항목 ${data.entries.length}개`);
process.exit(fail ? 1 : 0);
