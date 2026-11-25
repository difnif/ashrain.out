// node tests/chapters.test.mjs — 대단원 도우미(src/lib/chapters.js) 검사
import assert from "node:assert/strict";
import { CHAPTERS, chaptersOf, chapterId, parseChapterId, conceptIdsInChapter, chapterIndexOf } from "../src/lib/chapters.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}

const UNITS = ["m1-1", "m1-2", "m2-1", "m2-2", "m3-1", "m3-2", "h1-1", "h1-2", "h2-1", "h2-2", "h3-1", "h3-2", "h3-3"];
const E_UNITS = ["e1-1", "e1-2", "e2-1", "e2-2", "e3-1", "e3-2", "e4-1", "e4-2", "e5-1", "e5-2", "e6-1", "e6-2"];

test("CHAPTERS: 초등 12 · 중등 · 고등 13개 학기 전부", () => {
  assert.deepEqual(Object.keys(CHAPTERS).sort(), [...E_UNITS, ...UNITS].sort());
});

test("초등 학기: 교과서 단원 하나가 대단원 하나 — 단원 k 는 sort_order 10k ~ 10k + 9", () => {
  let total = 0;
  for (const u of E_UNITS) {
    const chs = CHAPTERS[u];
    assert.ok(chs.length >= 4 && chs.length <= 6, `${u} 단원 ${chs.length}개`);
    chs.forEach(([title, from, to], i) => {
      assert.ok(typeof title === "string" && title.length, `${u} 제목`);
      assert.deepEqual([from, to], [(i + 1) * 10, (i + 1) * 10 + 9], `${u} ${title}`);
    });
    total += chs.length;
  }
  assert.equal(total, 69);
  assert.deepEqual(parseChapterId("e3-2~4"), { unitId: "e3-2", idx: 4, title: "들이와 무게", range: [50, 59] });
  assert.equal(parseChapterId("e1-2~4"), null);      // 초1-2 는 단원 4개
});

test("중등 · 고등 학기: 구간이 1부터 빈틈·겹침 없이 이어진다", () => {
  for (const u of UNITS) {
    const chs = CHAPTERS[u];
    assert.ok(chs.length >= 2, u);
    let next = 1;
    for (const [title, from, to] of chs) {
      assert.ok(typeof title === "string" && title.length, `${u} 제목`);
      assert.equal(from, next, `${u} ${title} 시작`);
      assert.ok(to >= from, `${u} ${title} 끝`);
      next = to + 1;
    }
  }
});

test("chaptersOf: 모르는 학기는 '전체' 하나", () => {
  assert.equal(chaptersOf("m1-1").length, 4);
  assert.deepEqual(chaptersOf("x9-9"), [["전체", 1, 999]]);
  assert.deepEqual(chaptersOf(undefined), [["전체", 1, 999]]);
});

test("chapterId / parseChapterId: 왕복, 형식 밖·없는 단원은 null", () => {
  assert.equal(chapterId("m1-1", 1), "m1-1~1");
  assert.deepEqual(parseChapterId("m1-1~1"), { unitId: "m1-1", idx: 1, title: "정수와 유리수", range: [9, 18] });
  assert.deepEqual(parseChapterId("h3-3~2"), { unitId: "h3-3", idx: 2, title: "벡터", range: [14, 21] });
  assert.equal(parseChapterId("m1-1~4"), null);      // 4번 단원 없음
  assert.equal(parseChapterId("m1-1"), null);        // 학기 id
  assert.equal(parseChapterId("m1-1-03"), null);     // 개념 id
  assert.equal(parseChapterId("x9-9~0"), null);      // 학기 id 형식(m/h) 밖
  assert.equal(parseChapterId(""), null);
  assert.equal(parseChapterId(null), null);
  assert.equal(parseChapterId("m1-1~"), null);
});

test("conceptIdsInChapter / chapterIndexOf: sort_order 구간으로, 정렬해서", () => {
  const concepts = [
    { id: "m1-1-10", unit_id: "m1-1", sort_order: 10 },
    { id: "m1-1-09", unit_id: "m1-1", sort_order: 9 },
    { id: "m1-1-18", unit_id: "m1-1", sort_order: 18 },
    { id: "m1-1-19", unit_id: "m1-1", sort_order: 19 },
    { id: "m1-1-08", unit_id: "m1-1", sort_order: 8 },
    { id: "m1-2-09", unit_id: "m1-2", sort_order: 9 },   // 다른 학기
    null,
  ];
  assert.deepEqual(conceptIdsInChapter(concepts, "m1-1", 1), ["m1-1-09", "m1-1-10", "m1-1-18"]);
  assert.deepEqual(conceptIdsInChapter(concepts, "m1-1", 0), ["m1-1-08"]);
  assert.deepEqual(conceptIdsInChapter(concepts, "m1-1", 3), []);
  assert.deepEqual(conceptIdsInChapter(concepts, "m1-1", 9), []);
  assert.deepEqual(conceptIdsInChapter(null, "m1-1", 1), []);
  assert.equal(chapterIndexOf({ unit_id: "m1-1", sort_order: 18 }), 1);
  assert.equal(chapterIndexOf({ unit_id: "m1-1", sort_order: 19 }), 2);
  assert.equal(chapterIndexOf({ unit_id: "m1-1", sort_order: 99 }), -1);
  assert.equal(chapterIndexOf(null), -1);
});

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
