// node tests/mockexams.test.mjs — 학교별 모의고사 순수 도우미(src/lib/mockexams.js) 검사
//   학교 찾기(초성) · 판 · 회차 묶음 · 보기 고르기 · 채점(선택형 · 서답형 스스로 채점) · 채점 요소 · 보기 누르는 자리 · 글자 꾸밈 · 돌아올 주소 · 시간
import assert from "node:assert/strict";
import {
  searchSchools, editionsOf, examGroups, EDITIONS, edInfo, toggleChoice, judgeMc, isAnswered, gradeMock, rubricScore, rubricPart,
  choiceRects, richHtml, safeFrom, avHref, avLinksOf, timerLeft, fmtClock, choiceText, downloadName, mcItems, saItems, itemByI,
} from "../src/lib/mockexams.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.stack || e).split("\n").slice(0, 4).join("\n      ")); }
}

const SCHOOLS = [
  { id: "munjeong", name: "문정중학교", short: "문정중", region: "서울 송파구", level: "중등", alias: ["문정"], n: 2 },
  { id: "garak", name: "가락중학교", short: "가락중", region: "서울 송파구", level: "중등", alias: [], n: 0 },
  { id: "daechi", name: "대치중학교", short: "대치중", region: "서울 강남구", level: "중등", alias: [], n: 5 },
  { id: "munhyeon", name: "문현고등학교", short: "문현고", region: "부산 남구", level: "고등", alias: [], n: 1 },
];
const EXAMS = [
  { id: "munjeong-2026-2m-01", school: "munjeong", ed: "기출 분석", grade: "중2", year: 2026, term: "2학기 중간고사 대비", no: 1 },
  { id: "munjeong-2026-2m-02", school: "munjeong", ed: "기본", grade: "중2", year: 2026, term: "2학기 중간고사 대비", no: 2 },
  { id: "munjeong-2026-2f-b02", school: "munjeong", ed: "기본", grade: "중2", year: 2026, term: "2학기 기말고사 대비", no: 2 },
  { id: "munjeong-2026-2f-b01", school: "munjeong", ed: "기본", grade: "중2", year: 2026, term: "2학기 기말고사 대비", no: 1 },
  { id: "munjeong-2026-2f-f01", school: "munjeong", ed: "융합", grade: "중2", year: 2026, term: "2학기 기말고사 대비", no: 1 },
  { id: "daechi-2026-1f-x01", school: "daechi", ed: "심화", grade: "중3", year: 2026, term: "1학기 기말고사 대비", no: 1 },
];
const INDEX = { schools: SCHOOLS, exams: EXAMS };

console.log("학교 찾기");
test("빈 검색 = 전부 · 이름 · 줄임 · 지역 · 다른 이름", () => {
  assert.equal(searchSchools(SCHOOLS, "").length, 4);
  assert.deepEqual(searchSchools(SCHOOLS, "문정").map((s) => s.id), ["munjeong"]);
  assert.deepEqual(searchSchools(SCHOOLS, "문정중").map((s) => s.id), ["munjeong"]);
  assert.deepEqual(searchSchools(SCHOOLS, "문정 중학교").map((s) => s.id), ["munjeong"], "띄어 써도");
  assert.deepEqual(searchSchools(SCHOOLS, "송파").map((s) => s.id).sort(), ["garak", "munjeong"]);
  assert.deepEqual(searchSchools(SCHOOLS, "강남").map((s) => s.id), ["daechi"]);
  assert.equal(searchSchools(SCHOOLS, "없는학교").length, 0);
});
test("초성 — ㅁㅈ · ㄷㅊㅈ, 이름이 앞에서 맞는 학교부터", () => {
  assert.deepEqual(searchSchools(SCHOOLS, "ㅁㅈ").map((s) => s.id), ["munjeong"]);
  assert.deepEqual(searchSchools(SCHOOLS, "ㄷㅊㅈ").map((s) => s.id), ["daechi"]);
  const r = searchSchools(SCHOOLS, "ㅁ");
  assert.ok(r.length >= 2 && r.every((s) => /^문/.test(s.name) || s.region.includes("ㅁ") || true));
  assert.equal(r[0].id, "munjeong", "앞에서 맞고 시험이 많은 학교가 먼저");
});

console.log("판 · 회차");
test("판: 융합 · 기본은 늘, 기출 분석은 있을 때만, 모르는 판도 목록에", () => {
  const e1 = editionsOf(INDEX, "munjeong");
  assert.deepEqual(e1.map((e) => [e.id, e.n]), [["융합", 1], ["기본", 3], ["기출 분석", 1]]);
  const e2 = editionsOf(INDEX, "garak");
  assert.deepEqual(e2.map((e) => [e.id, e.n]), [["융합", 0], ["기본", 0]]);
  const e3 = editionsOf(INDEX, "daechi");
  assert.deepEqual(e3.map((e) => e.id), ["융합", "기본", "심화"]);
  assert.equal(edInfo("심화").icon, "📄");
  assert.equal(EDITIONS.find((e) => e.id === "융합").always, true);
});
test("회차 묶음: 같은 시기끼리, 기말 → 중간(최근 먼저), 묶음 안은 회차 차례", () => {
  const g = examGroups(INDEX, "munjeong", "기본");
  assert.deepEqual(g.map((x) => x.term), ["2학기 기말고사 대비", "2학기 중간고사 대비"]);
  assert.deepEqual(g[0].exams.map((e) => e.no), [1, 2]);
  assert.equal(g[0].title, "2026학년도 중2 2학기 기말고사 대비");
  assert.equal(examGroups(INDEX, "munjeong", "융합")[0].exams.length, 1);
  assert.equal(examGroups(INDEX, "garak", "기본").length, 0);
});

// 작은 시험 하나 — 선택형 3(하나는 정답 2개) + 서답형 2
const EXAM = {
  id: "t-exam", year: 2026, grade: "중2", term: "2학기 중간고사 대비", title: "실전 모의고사 1회", sub: "문정중 기출 분석형", ed: "기출 분석", minutes: 45,
  items: [
    { i: 1, kind: "mc", no: 1, label: "1", pts: 3, ans: [4], multi: false, av: ["m-sys"], box: { p: 0, x: 0.05, y: 0.2, w: 0.44, h: 0.3 },
      ch: [{ x: 0.08, y: 0.45, r: 0.0085 }, { x: 0.22, y: 0.45, r: 0.0085 }, { x: 0.36, y: 0.45, r: 0.0085 }, { x: 0.08, y: 0.475, r: 0.0085 }, { x: 0.22, y: 0.475, r: 0.0085 }] },
    { i: 2, kind: "mc", no: 2, label: "2", pts: 4, ans: [2, 4], multi: true, av: ["m-sim.1", "m-sys"], box: { p: 0, x: 0.5, y: 0.2, w: 0.44, h: 0.3 },
      ch: [{ x: 0.53, y: 0.3, r: 0.0085 }, { x: 0.53, y: 0.33, r: 0.0085 }, { x: 0.53, y: 0.36, r: 0.0085 }, { x: 0.53, y: 0.39, r: 0.0085 }, { x: 0.53, y: 0.42, r: 0.0085 }] },
    { i: 3, kind: "mc", no: 3, label: "3", pts: 3, ans: [1], multi: false, av: [] },
    { i: 4, kind: "sa", no: 1, label: "서답형 1", pts: 4, parts: [0], av: ["m-sys.2"], rubric: [["식을 세운다", 1], ["x = 4", 1], ["a = 2", 1], ["b = 10", 1]] },
    { i: 5, kind: "sa", no: 2, label: "서답형 2", pts: 6, parts: [1, 2], av: [], rubric: [["(1) 첫째 식", 2], ["(1) 둘째 식", 2], ["(2) 답", 2]] },
  ],
};

console.log("보기 고르기 · 판정");
test("한 개 답: 바꿔 고르고, 같은 것을 다시 누르면 지움", () => {
  let a = toggleChoice(null, 3, false);
  assert.deepEqual(a, { k: "mc", sel: [3] });
  a = toggleChoice(a, 4, false);
  assert.deepEqual(a.sel, [4]);
  assert.equal(toggleChoice(a, 4, false), null);
});
test("정답 2개: 켜고 끄고, 차례대로", () => {
  let a = toggleChoice(null, 4, true);
  a = toggleChoice(a, 2, true);
  assert.deepEqual(a.sel, [2, 4]);
  a = toggleChoice(a, 4, true);
  assert.deepEqual(a.sel, [2]);
  assert.equal(toggleChoice(a, 2, true), null);
});
test("judgeMc — 정답 2개는 둘 다 골라야 맞음", () => {
  const [m1, m2] = EXAM.items;
  assert.equal(judgeMc(m1, { k: "mc", sel: [4] }), "ok");
  assert.equal(judgeMc(m1, { k: "mc", sel: [3] }), "wrong");
  assert.equal(judgeMc(m1, null), "blank");
  assert.equal(judgeMc(m2, { k: "mc", sel: [4, 2] }), "ok");
  assert.equal(judgeMc(m2, { k: "mc", sel: [2] }), "wrong");
  assert.equal(judgeMc(m2, { k: "mc", sel: [2, 3, 4] }), "wrong");
});
test("isAnswered — 서답형은 손글씨 획이나 글자가 하나라도", () => {
  const sa = EXAM.items[3];
  assert.equal(isAnswered(sa, null), false);
  assert.equal(isAnswered(sa, { k: "sa", parts: { 0: { k: "text", raw: "  " } } }), false);
  assert.equal(isAnswered(sa, { k: "sa", parts: { 0: { k: "text", raw: "x = 4" } } }), true);
  assert.equal(isAnswered(sa, { k: "sa", parts: { 0: { k: "ink", s: [[1, 2, 3, 4]] } } }), true);
  assert.equal(isAnswered(EXAM.items[0], { k: "mc", sel: [] }), false);
});

console.log("채점");
test("선택형 바로 · 서답형은 스스로 채점 전 pending", () => {
  const answers = { 1: { k: "mc", sel: [4] }, 2: { k: "mc", sel: [2] }, 4: { k: "sa", parts: { 0: { k: "text", raw: "a = 2" } } } };
  const g = gradeMock(EXAM, answers, {});
  assert.equal(g.mc.got, 3); assert.equal(g.mc.max, 10); assert.equal(g.mc.ok, 1);
  assert.equal(g.sa.max, 10); assert.equal(g.sa.got, 0);
  assert.equal(g.max, 20); assert.equal(g.score, 3);
  const st = Object.fromEntries(g.rows.map((r) => [r.i, r.status]));
  assert.deepEqual(st, { 1: "ok", 2: "wrong", 3: "blank", 4: "pending", 5: "blank" });
  assert.equal(g.counts.pending, 1);
});
test("서답형 점수 — 만점 ok · 부분 part · 0점 wrong · 배점을 넘지 않음", () => {
  const answers = { 4: { k: "sa", parts: { 0: { k: "text", raw: "…" } } }, 5: { k: "sa", parts: { 1: { k: "text", raw: "…" } } } };
  let g = gradeMock(EXAM, answers, { 4: { got: 4 }, 5: { got: 3 } });
  assert.equal(g.sa.got, 7); assert.equal(g.sa.done, 2);
  assert.deepEqual(g.rows.filter((r) => r.kind === "sa").map((r) => r.status), ["ok", "part"]);
  g = gradeMock(EXAM, answers, { 4: { got: 0 }, 5: { got: 99 } });
  assert.deepEqual(g.rows.filter((r) => r.kind === "sa").map((r) => [r.status, r.got]), [["wrong", 0], ["ok", 6]]);
});
test("채점 요소 체크 → 점수 · (1)/(2) 가르기", () => {
  const sa = EXAM.items[4];
  assert.equal(rubricScore(sa, [true, false, true]), 4);
  assert.equal(rubricScore(sa, []), 0);
  assert.equal(rubricPart("(2) 답"), 2);
  assert.equal(rubricPart("식을 세운다"), 0);
});

console.log("시험지 위 보기 자리");
test("choiceRects — 같은 줄 다음 보기 앞까지, 줄 끝 보기는 칸 끝까지, 위아래가 겹치지 않음", () => {
  const r = choiceRects(EXAM.items[0]);
  assert.equal(r.length, 5);
  assert.ok(r[0].x < 0.08 && r[0].x + r[0].w < 0.22, "① 은 ② 앞에서 끝남");
  assert.ok(Math.abs(r[2].x + r[2].w - (0.05 + 0.44 - 0.006)) < 1e-9, "③ 은 칸 끝까지");
  assert.ok(r[0].y + r[0].h <= r[3].y + 1e-9, "윗줄 · 아랫줄이 겹치지 않음");
  const v = choiceRects(EXAM.items[1]);          // 세로로 늘어선 보기 — 한 줄에 하나
  assert.ok(v.every((x) => Math.abs(x.x + x.w - (0.5 + 0.44 - 0.006)) < 1e-9));
  assert.deepEqual(choiceRects({ box: { x: 0, w: 1 }, ch: [] }), []);
});

console.log("글자 꾸밈 · 주소 · 시간");
test("richHtml — 이스케이프 먼저, 선분 · 위첨자 · 분수 · 연립", () => {
  assert.equal(richHtml("<b>x</b>"), "&lt;b&gt;x&lt;/b&gt;");
  assert.equal(richHtml("{AD} = 7"), '<span class="mx-ov">AD</span> = 7');
  assert.equal(richHtml("a^2 + 15^2"), "a<sup>2</sup> + 15<sup>2</sup>");
  assert.equal(richHtml("[[32/5]] cm"), '<span class="mx-fr"><span class="n">32</span><span class="d">5</span></span> cm');
  const sys = richHtml("(1) <<x + y = 5 | [[x/3]] + [[y/6]] = [[3/2]]>> (2) 답");
  assert.ok(sys.startsWith('(1) <span class="mx-sys"><span>x + y = 5</span><span><span class="mx-fr">'), sys);
  assert.ok(sys.endsWith("</span></span> (2) 답"));
  assert.ok(!/<script/i.test(richHtml("<<<script>alert(1)</script>|x>>")));
});
test("safeFrom — 시험 화면 안쪽 주소만 돌아올 곳으로", () => {
  assert.equal(safeFrom("#/mock/munjeong-2026-2m-01"), "#/mock/munjeong-2026-2m-01");
  assert.equal(safeFrom("#/mock/munjeong-2026-2m-01/q/19"), "#/mock/munjeong-2026-2m-01/q/19");
  assert.equal(safeFrom("#/study/exam/school/munjeong/%EA%B8%B0%EB%B3%B8"), "#/study/exam/school/munjeong/%EA%B8%B0%EB%B3%B8");
  assert.equal(safeFrom("https://evil.example/"), "");
  assert.equal(safeFrom("javascript:alert(1)"), "");
  assert.equal(safeFrom("#/admin/users"), "");
  assert.equal(safeFrom(""), "");
});
test("avHref · avLinksOf — key 마다 걸린 문항(처음 나온 차례), 모르는 key 는 뺌", () => {
  assert.equal(avHref("m-sys.2", "#/mock/x-1"), "#/av/m-sys.2?from=%23%2Fmock%2Fx-1");
  const L = avLinksOf(EXAM, (k) => k !== "m-sim.1");
  assert.deepEqual(L.map((x) => [x.key, x.items.map((y) => y.label)]), [["m-sys", ["1", "2"]], ["m-sys.2", ["서답형 1"]]]);
});
test("timerLeft · fmtClock — 멈춘 시간은 빼고, 넘기면 +", () => {
  const t0 = 1_000_000;
  assert.equal(timerLeft(null, 45, t0), 45 * 60000);
  assert.equal(timerLeft({ start: t0, paused: null, used: 0 }, 45, t0 + 60000), 44 * 60000);
  assert.equal(timerLeft({ start: t0, paused: t0 + 30000, used: 60000 }, 45, t0 + 999999), 45 * 60000 - 90000);
  assert.equal(fmtClock(44 * 60000 + 5000), "44:05");
  assert.equal(fmtClock(-65000), "+1:05");
});
test("choiceText · 받을 때 이름 · 문항 고르기", () => {
  assert.equal(choiceText([2, 4]), "②, ④");
  assert.equal(downloadName(EXAM, { label: "문제지" }, "문정중"), "문정중 2026 중2 2학기 중간고사 대비 실전 모의고사 1회 (기출 분석) 문제지.pdf");
  assert.equal(downloadName({ ...EXAM, ed: "기본", sub: "기본 다지기" }, { label: "빠른 정답지" }, "문정중"), "문정중 2026 중2 2학기 중간고사 대비 실전 모의고사 1회 (기본) 빠른 정답지.pdf");
  assert.equal(downloadName({ ...EXAM, title: "a/b:c" }, { label: "문제지" }, ""), "2026 중2 2학기 중간고사 대비 a b c (기출 분석) 문제지.pdf", "파일 이름에 못 쓰는 글자는 빈칸");
  assert.equal(mcItems(EXAM).length, 3); assert.equal(saItems(EXAM).length, 2);
  assert.equal(itemByI(EXAM, "4").label, "서답형 1");
});

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
