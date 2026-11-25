// 강사도구 「옮겨 오기」 — PC 자료 맞추기 순수 함수 (node --test tests/ttpc.test.mjs)
import { test } from "node:test";
import assert from "node:assert/strict";
import { KST, tsKey, jparse, safeQuery, knownFromPc, cleanPrintMeta, cleanEventDetail, markKey, eventKey, scanKey, onlyNew, sessionPlan, gradingNewer, insidePcTool, applyWal } from "../src/apps/seirocco/tt/pccore.js";

// 가짜 mf.db: SQL 문장 첫머리로 표를 고른다
const fakeQ = (tables) => (sql) => {
  const m = /FROM\s+(\w+)/i.exec(sql);
  const t = m && m[1];
  if (!(t in tables)) throw new Error(`no such table: ${t}`);
  return tables[t];
};

test("PC 시각(한국, 시간대 없음)과 웹 시각(UTC)이 같은 열쇠", () => {
  assert.equal(KST("2026-11-12 16:21:05"), "2026-11-12T16:21:05+09:00");
  assert.equal(KST("2026-11-12T07:21:05+00:00"), "2026-11-12T07:21:05+00:00");
  assert.equal(tsKey("2026-11-12 16:21:05"), tsKey("2026-11-12T07:21:05+00:00"));
  assert.equal(tsKey("2026-11-12 16:21:05"), tsKey("2026-11-12T07:21:05.000Z"));
  assert.notEqual(tsKey("2026-11-12 16:21:05"), tsKey("2026-11-12 16:21:06"));
  assert.equal(tsKey(null), "");
  assert.deepEqual(jparse('{"a":1}', {}), { a: 1 });
  assert.deepEqual(jparse("깨짐{", []), []);
  assert.deepEqual(jparse({ b: 2 }, {}), { b: 2 });
});

test("옛 판에 없는 표는 빈 것으로, 다른 오류는 그대로", () => {
  const q = safeQuery(fakeQ({ prints: [{ id: 1 }] }));
  assert.deepEqual(q("SELECT * FROM prints"), [{ id: 1 }]);
  assert.deepEqual(q("SELECT * FROM scans WHERE grading_id=1"), []);
  assert.deepEqual(q("SELECT * FROM transcripts"), []);
  const bad = safeQuery(() => { throw new Error("database disk image is malformed"); });
  assert.throws(() => bad("SELECT 1"), /malformed/);
});

test("학생 이름 모으기: 명단 + 출제 대상 + 매쓰플랫 파일 이름", () => {
  const q = fakeQ({
    students: [{ name: "가나다" }, { name: " 라마바 " }],
    prints: [
      { options: JSON.stringify({ targets: ["사아자"] }), sources: JSON.stringify(["261112_11&12 3-2 5,6단원_차카타_문제지.pdf"]) },
      { options: null, sources: "[\"261113_11&13 소인수분해_문제지.pdf\"]" },
    ],
  });
  const n = knownFromPc(q, ["파하"]);
  assert.deepEqual([...n].sort(), ["가나다", "라마바", "사아자", "차카타", "파하"].sort());
  assert.ok(!n.has("소인수분해"));
});

test("프린트 글자 정보에서 이름 빼기 · 출제 대상은 옵션에서 뺌", () => {
  const names = new Set(["차카타"]);
  const m = cleanPrintMeta({
    code: "9HN2P3", title: "복습 11/12 3-2 5,6단원 차카타", sub: "",
    sources: JSON.stringify(["261112_11&12 3-2 5,6단원_차카타_문제지.pdf"]),
    options: JSON.stringify({ template: "초등", label: "단답형", targets: ["차카타"], title: "복습 11/12 3-2 5,6단원 차카타" }),
  }, names);
  assert.equal(m.title, "복습 11/12 3-2 5,6단원");
  assert.equal(m.sources[0].includes("차카타"), false);
  assert.ok(m.sources[0].endsWith("문제지.pdf"));
  assert.equal(m.options.targets, undefined);
  assert.equal(m.options.template, "초등");
  assert.equal(m.options.title.includes("차카타"), false);
  // 제목이 이름뿐이면 코드
  assert.equal(cleanPrintMeta({ code: "ABCDEF", title: "차카타", options: null, sources: null }, names).title, "ABCDEF");
});

test("활동 로그 내용: 변환 기록의 파일 이름·대상 이름은 빼고, 학생 추가는 그대로", () => {
  const names = new Set(["차카타"]);
  const d = cleanEventDetail("convert", JSON.stringify({ code: "9HN2P3", title: "복습", files: ["261112_단원_차카타_문제지.pdf"], targets: ["차카타"] }), names);
  assert.equal(d.files[0].includes("차카타"), false);
  assert.equal(d.targets, undefined);
  assert.equal(d.n_targets, 1);
  assert.equal(d.code, "9HN2P3");
  assert.deepEqual(cleanEventDetail("student_add", '{"name":"차카타"}', names), { name: "차카타" });
});

test("채점 표시·활동 로그·스캔본: 이미 웹에 있는 것은 빼고 새것만 (시각 꼴이 달라도)", () => {
  const pc = [
    { session_no: 2, seq: 1, result: "O", at: "2026-11-12T16:22:54+09:00" },
    { session_no: 2, seq: 2, result: "X", at: "2026-11-12T16:23:02+09:00" },
    { session_no: 2, seq: 2, result: "X", at: "2026-11-12T16:23:02+09:00" },   // 같은 것이 두 번이면 한 번만
  ];
  const web = [{ session_no: 2, seq: 1, result: "O", at: "2026-11-12T07:22:54+00:00" }];
  const nw = onlyNew(pc, web, markKey);
  assert.equal(nw.length, 1);
  assert.equal(nw[0].seq, 2);
  const ev = onlyNew([{ at: "2026-11-12 14:48:15", kind: "convert", student_id: null, print_id: 7 }], [{ at: "2026-11-12T05:48:15+00:00", kind: "convert", student_id: null, print_id: 7 }], eventKey);
  assert.equal(ev.length, 0);
  assert.equal(onlyNew([{ name: "a.jpg", size: 10 }, { name: "b.jpg", size: 3 }], [{ name: "a.jpg", size: 10 }], scanKey).length, 1);
});

test("회차: 없는 것은 넣고, 웹에서 안 끝난 회차가 PC에서 끝났으면 끝냄", () => {
  const p = sessionPlan(
    [{ no: 1, ended_at: "2026-11-12 16:21:00" }, { no: 2, ended_at: "2026-11-12 16:28:40" }, { no: 3, ended_at: null }],
    [{ no: 1, ended_at: "2026-11-12T07:21:00+00:00" }, { no: 2, ended_at: null }],
  );
  assert.deepEqual(p.add.map((s) => s.no), [3]);
  assert.deepEqual(p.close.map((s) => s.no), [2]);
});

test("채점 상태: PC가 더 나중이고 상태가 다를 때만 바꿈", () => {
  assert.equal(gradingNewer({ status: "done", updated_at: "2026-11-13 10:00:00" }, { status: "open", updated_at: "2026-11-12T07:00:00+00:00" }), true);
  assert.equal(gradingNewer({ status: "done", updated_at: "2026-11-12 10:00:00" }, { status: "open", updated_at: "2026-11-13T07:00:00+00:00" }), false);
  assert.equal(gradingNewer({ status: "open", updated_at: "2026-11-13 10:00:00" }, { status: "open", updated_at: "2026-11-12T07:00:00+00:00" }), false);
});

test("PC 강사도구의 「결과」 폴더(변환 PDF 사본)는 Claude 프린트로 보지 않음", () => {
  assert.equal(insidePcTool("애쉬레인 강사도구/data/prints/A/print_시험지.pdf", "애쉬레인 강사도구/data/"), true);
  assert.equal(insidePcTool("애쉬레인 강사도구/결과/2026-11-12/a_시험지.pdf", "애쉬레인 강사도구/data/"), true);
  assert.equal(insidePcTool("받은 프린트/모의고사 1회 문제지.pdf", "애쉬레인 강사도구/data/"), false);
  assert.equal(insidePcTool("data/prints/A/x.pdf", "data/"), true);
  assert.equal(insidePcTool("x.pdf", null), false);
});

test("WAL: 없거나 이상하면 원래 그대로", () => {
  const db = new Uint8Array([1, 2, 3]);
  assert.equal(applyWal(db, null), db);
  assert.equal(applyWal(db, new Uint8Array(40)), db);
});

import { pngSize, readSolutions, quickText, pickAnswer } from "../src/apps/seirocco/tt/pccore.js";

test("PNG 크기 읽기", () => {
  const b = Uint8Array.from(Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAMAAAACCAYAAACddGYaAAAAEUlEQVR42mP8z8DAwMjAwMAAAA4ABQGh7QUAAAAASUVORK5CYII=", "base64"));
  assert.deepEqual(pngSize(b), [3, 2]);
  assert.equal(pngSize(new Uint8Array([1, 2, 3])), null);
});

test("해설 묶음 읽기: 형식이 맞는 것만, 파일 이름은 영문·숫자만", () => {
  assert.equal(readSolutions({ kind: "x" }), null);
  const s = readSolutions({ kind: "ashrain.tt.solutions", made: "2026-11-25", items: {
    abc: { answer: " 2 ", sol: "abc.png", w: 220, h: 80 },
    bad: { answer: "3", sol: "../x.png", w: 10, h: 10 },
    nos: { answer: "5" },
  } });
  assert.equal(s.items.size, 3);
  assert.deepEqual(s.items.get("abc"), { answer: "2", sol: "abc.png", w: 220, h: 80 });
  assert.equal(s.items.get("bad").sol, null);
  assert.equal(s.items.get("nos").sol, null);
  assert.equal(s.stamp, "2026-11-25|3");
});

test("정답 고르기: PC에 적은 것 > 해설 묶음 > 빠른정답", () => {
  assert.equal(quickText({ choice: "2", text: "" }), "2");
  assert.equal(quickText({ choice: null, text: "3100 mL" }), "3100 mL");
  assert.equal(pickAnswer("4", "2", "3"), "4");
  assert.equal(pickAnswer("", "2", "3"), "2");
  assert.equal(pickAnswer(null, "", "3"), "3");
  assert.equal(pickAnswer("", "", ""), "");
});
