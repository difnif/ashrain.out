// 컨셉 문제 · 일차함수와 그래프(lin, 중2-1 × 과학 단원) — 답 판정(수 · 식 · 점) · OMR 손글씨 한 줄 카드 · 세트 데이터
//   node tests/conceptsets-lin.test.mjs
// 확률(prob) 범주는 tests/conceptsets.test.mjs 가 본다. 여기서는 일차함수 범주에만 있는 것:
//   답 꼴 num { n, d, dec, u } · lin { a:[n,d], b:[n,d], dec } · pt { x, y, dec } · pick
//   OMR: 보기만 동그라미, 나머지는 손으로 쓰는 한 줄 칸(AI 판독) — 2쪽 · 띠의 범주 코드 3 · 예전(v1) 판 없음
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  layoutCard, cardHtml, pageSvg, bandBits, parseBand, bandCells, readCardPhoto, kindOf, handCrops,
  GW, BAND, BAND2, LINE, CAT_CODES, INSTRUCTION_LIN,
} from "../src/lib/omr/grid.js";
import { judge, rawOf, parseRat, ratText, parseLine, parsePt, lineText, answerText, CATEGORIES } from "../src/lib/conceptsets.js";
import { solutionHtml, questionHtml, missingCueKeys } from "../src/pages/sets/render.js";
import { omrKindName, kindLabel } from "../src/pages/sets/labels.js";
import { raster, fillRect, fillCircle, ring, strokeRect, handText, photograph } from "./fixtures/omrsynth.mjs";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIR = process.env.CS_LIN_DIR || path.join(ROOT, "public/concept-sets/lin");     // CS_LIN_DIR: 만드는 중인 데이터로 미리 보기
let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log("  ok  " + name); }
  catch (e) { failed++; console.log("FAIL  " + name + "\n      " + (e && e.stack || e).toString().split("\n").slice(0, 5).join("\n      ")); }
}
const I = (a) => ({ a });
const M = "−";

console.log("수 · 식 · 점 읽기");
test("parseRat: 음수 · 분수 · 소수 · '분의' · 0 나누기는 아님", () => {
  assert.deepEqual(parseRat("−3"), [-3, 1]); assert.deepEqual(parseRat("3/4"), [3, 4]); assert.deepEqual(parseRat("-0.5"), [-1, 2]);
  assert.deepEqual(parseRat("12.5"), [25, 2]); assert.deepEqual(parseRat("1.50"), [3, 2]); assert.deepEqual(parseRat("+6/8"), [3, 4]);
  assert.deepEqual(parseRat("4분의 3"), [3, 4]); assert.deepEqual(parseRat("−4분의 3"), [-3, 4]); assert.deepEqual(parseRat("０.２５"), [1, 4]);
  assert.equal(parseRat("3/0"), null); assert.equal(parseRat("abc"), null); assert.equal(parseRat("3/-4"), null); assert.equal(parseRat(""), null);
});
test("ratText: 기약분수 · 유니코드 마이너스 · 소수로 쓰는 문항은 끝나는 소수만 소수로", () => {
  assert.equal(ratText([-3, 1]), `${M}3`); assert.equal(ratText([-1, 2]), `${M}1/2`); assert.equal(ratText([25, 2], true), "12.5");
  assert.equal(ratText([-1, 2], true), `${M}0.5`); assert.equal(ratText([1, 8], true), "0.125"); assert.equal(ratText([1, 3], true), "1/3");
  assert.equal(ratText([3, 100], true), "0.03"); assert.equal(ratText([0, 1]), "0");
});
test("parseLine: y = 생략 · 일반형 · 좌우 바꿈 · 분수 계수 세 꼴 · 곱셈 기호", () => {
  const L = (s) => { const r = parseLine(s); return r && [r.a, r.b]; };
  assert.deepEqual(L("y = −2x + 3"), [[-2, 1], [3, 1]]); assert.deepEqual(L("-2x+3"), [[-2, 1], [3, 1]]);
  assert.deepEqual(L("2x + y − 3 = 0"), [[-2, 1], [3, 1]]); assert.deepEqual(L("-2x+3=y"), [[-2, 1], [3, 1]]); assert.deepEqual(L("y=3-2x"), [[-2, 1], [3, 1]]);
  for (const s of ["y=-1/2x+5", "y=-x/2+5", "y=-0.5x+5", "y = −(1/2)x + 5", "2y = -x + 10", "x + 2y - 10 = 0"]) assert.deepEqual(L(s), [[-1, 2], [5, 1]], s);
  assert.deepEqual(L("y = 3 × x"), [[3, 1], [0, 1]]); assert.deepEqual(L("y=x"), [[1, 1], [0, 1]]); assert.deepEqual(L("y=5"), [[0, 1], [5, 1]]);
  for (const s of ["x=3", "y=x^2", "y==2x", "", "y=2x+", "y=2xy"]) assert.equal(parseLine(s), null, s);
});
test("parsePt: 괄호 · 공백 · 전각 쉼표 · 분수 좌표", () => {
  assert.deepEqual(parsePt("(2, −1)"), { x: [2, 1], y: [-1, 1] }); assert.deepEqual(parsePt("2,-1"), { x: [2, 1], y: [-1, 1] });
  assert.deepEqual(parsePt("（1/2，4）"), { x: [1, 2], y: [4, 1] }); assert.deepEqual(parsePt("(0.5, 4)"), { x: [1, 2], y: [4, 1] });
  assert.equal(parsePt("(2)"), null); assert.equal(parsePt("(1, 2, 3)"), null); assert.equal(parsePt("(a, 2)"), null);
});
test("lineText: 계수 1 · −1 · 0 · 상수항 0 · 소수 꼴", () => {
  assert.equal(lineText([-2, 1], [3, 1]), `y = ${M}2x + 3`); assert.equal(lineText([1, 1], [-1, 1]), `y = x ${M} 1`);
  assert.equal(lineText([-1, 1], [0, 1]), `y = ${M}x`); assert.equal(lineText([0, 1], [5, 1]), "y = 5"); assert.equal(lineText([-1, 2], [5, 1]), `y = ${M}1/2x + 5`);
  assert.equal(lineText([1, 2], [12, 1], true), "y = 0.5x + 12"); assert.equal(lineText([3, 2], [-5, 2], true), `y = 1.5x ${M} 2.5`);
});

console.log("답 판정");
test("수: 값이 같으면 정답 · 약분 안내 · 단위(cm · ℃ · N) 떼기 · 빈 답 · 못 읽은 자리", () => {
  const h = I({ k: "num", n: -1, d: 2, dec: 0, u: "" });
  for (const s of ["-1/2", "−1/2", "-0.5", "−2분의 1"]) assert.equal(judge(h, s).ok, true, s);
  const r = judge(h, "-2/4"); assert.equal(r.ok, true); assert.ok(r.note.includes(`${M}1/2`), r.note);
  assert.equal(judge(h, "1/2").ok, false); assert.equal(judge(h, "abc").ok, false); assert.ok(judge(h, "abc").note);
  assert.equal(judge(h, "").ok, null); assert.equal(judge(h, "1?").ok, null);
  const cm = I({ k: "num", n: 25, d: 2, dec: 1, u: "cm" });
  for (const s of ["12.5 cm", "12.5cm", "25/2", "12.5", "12.50"]) assert.equal(judge(cm, s).ok, true, s);
  assert.equal(judge(cm, "12").ok, false);
  const deg = I({ k: "num", n: -3, d: 1, dec: 0, u: "℃" });
  for (const s of ["-3℃", "−3 ℃", "-3°C", "-3"]) assert.equal(judge(deg, s).ok, true, s);
  assert.equal(judge(I({ k: "num", n: 49, d: 5, dec: 1, u: "N" }), "9.8 N").ok, true);
});
test("식: y = 생략 · 일반형 · 분수 계수 · 다른 기울기 · 식이 아니면 안내", () => {
  const f = I({ k: "lin", a: [-2, 1], b: [3, 1], dec: 0 });
  for (const s of ["y = −2x + 3", "y=-2x+3", "-2x+3", "2x+y-3=0", "y=3-2x"]) assert.equal(judge(f, s).ok, true, s);
  for (const s of ["y=-2x", "y=2x+3", "y=-2x-3"]) assert.equal(judge(f, s).ok, false, s);
  const bad = judge(f, "x = 3"); assert.equal(bad.ok, false); assert.ok(bad.note.includes("y = ax + b"));
  const g = I({ k: "lin", a: [1, 2], b: [12, 1], dec: 1 });
  for (const s of ["y = 0.5x + 12", "y=1/2x+12", "y=x/2+12"]) assert.equal(judge(g, s).ok, true, s);
});
test("점: 괄호 없이도 · 순서가 바뀌면 오답 · 꼴이 아니면 안내", () => {
  const p = I({ k: "pt", x: [2, 1], y: [-1, 1], dec: 0 });
  for (const s of ["(2, −1)", "(2,-1)", "2, -1"]) assert.equal(judge(p, s).ok, true, s);
  assert.equal(judge(p, "(-1, 2)").ok, false);
  const r = judge(p, "(2)"); assert.equal(r.ok, false); assert.ok(r.note.includes("(x좌표, y좌표)"));
});
test("정답의 쓰는 꼴(rawOf)은 스스로 정답 — 꼴마다 · 소수 문항", () => {
  const items = [
    { a: { k: "num", n: -3, d: 1, dec: 0, u: "℃" } }, { a: { k: "num", n: 3, d: 4, dec: 0 } }, { a: { k: "num", n: 25, d: 2, dec: 1, u: "cm" } },
    { a: { k: "lin", a: [-1, 2], b: [5, 1], dec: 0 } }, { a: { k: "lin", a: [1, 2], b: [12, 1], dec: 1 } }, { a: { k: "lin", a: [0, 1], b: [-4, 1], dec: 0 } },
    { a: { k: "lin", a: [-1, 1], b: [0, 1], dec: 0 } }, { a: { k: "pt", x: [1, 2], y: [-4, 1], dec: 0 } }, { a: { k: "pt", x: [3, 2], y: [0, 1], dec: 1 } },
  ];
  for (const it of items) assert.equal(judge(it, rawOf(it)).ok, true, rawOf(it));
  assert.equal(rawOf(items[2]), "12.5"); assert.equal(rawOf(items[4]), "y = 0.5x + 12"); assert.equal(rawOf(items[8]), "(1.5, 0)");
});
test("이름표: 입력 안내 · OMR 칸 이름(수 · 식 · 점 · 보기)", () => {
  assert.ok(kindLabel(I({ k: "num", u: "cm" })).includes("cm")); assert.ok(kindLabel(I({ k: "lin" })).includes("y = ax + b")); assert.ok(kindLabel(I({ k: "pt" })).includes("(x좌표, y좌표)"));
  assert.equal(omrKindName("line", "num"), "수"); assert.equal(omrKindName("line", "lin"), "식"); assert.equal(omrKindName("line", "pt"), "점"); assert.equal(omrKindName("pick"), "보기");
});

// ── 합성 세트: 데이터가 없어도 카드 · 판독을 본다 ──────────────────────────────────────
const OPTS = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ"];
function fakeItem(no) {
  const t = no % 7;
  const a = t === 0 || t === 4 ? { k: "lin", a: [-(no % 5) - 1, 2], b: [no, 1], dec: 0 }
    : t === 2 ? { k: "pt", x: [no % 9 - 4, 1], y: [-(no % 4), 1], dec: 0 }
    : t === 5 ? { k: "pick", v: no % 2 ? ["ㄱ", "ㄷ"] : ["ㄴ"], o: OPTS.slice(0, 3 + (no % 3)) }
    : { k: "num", n: no % 3 ? -no : no, d: no % 4 ? 1 : 4, dec: 0, u: no % 6 ? "" : "cm" };
  if (a.k === "num" && a.d === 4 && a.n % 2 === 0) a.n += 1;
  return { id: `x${no}`, no, a, omr: a.k === "pick" ? { o: a.o.length } : { w: a.k } };
}
const FAKE = { cat: "lin", no: 3, title: "힘과 무게 (합성)", short: "힘과 무게", items: Array.from({ length: 50 }, (_, i) => fakeItem(i + 1)) };
const CARD = layoutCard(FAKE);

console.log("OMR 카드(손글씨 한 줄)");
test("띠: 범주 코드 3 · 세트 1~63 · 쪽 0~3 왕복 · 한 칸 뒤집히면 다른 것으로 안 읽힘 · 64번부터는 없음", () => {
  assert.equal(CAT_CODES.lin, 3);
  for (let set = 1; set <= 63; set++) for (let page = 0; page < 4; page++) {
    const b = bandBits("lin", set, page);
    assert.equal(b.length, BAND.n);
    assert.deepEqual(parseBand(b), { cat: "lin", set, page });
    for (let i = 1; i < BAND.n - 1; i++) { const c = b.slice(); c[i] ^= 1; const r = parseBand(c); assert.ok(!r || r.set !== set || r.page !== page || r.cat !== "lin", `flip ${i}`); }
  }
  assert.throws(() => bandBits("lin", 64, 0));
  // 확률 세트와 띠가 겹치지 않는다
  assert.notDeepEqual(bandBits("lin", 3, 0), bandBits("prob", 3, 0));
});
test("칸 종류: 보기만 동그라미, 수 · 식 · 점은 손글씨 한 줄", () => {
  assert.deepEqual(kindOf({ a: { k: "num", n: 1, d: 1 }, omr: { w: "num" } }), { kind: "line", ak: "num" });
  assert.deepEqual(kindOf({ a: { k: "lin", a: [1, 1], b: [0, 1] }, omr: { w: "lin" } }), { kind: "line", ak: "lin" });
  assert.deepEqual(kindOf({ a: { k: "pt", x: [1, 1], y: [0, 1] }, omr: { w: "pt" } }), { kind: "line", ak: "pt" });
  assert.equal(kindOf({ a: { k: "pick", v: ["ㄱ"], o: ["ㄱ", "ㄴ", "ㄷ"] }, omr: { o: 3 } }).kind, "pick");
});
function checkLayout(card, label) {
  assert.equal(card.ver, 2, label);
  assert.ok(card.pages.length >= 1 && card.pages.length <= 3, `${label} ${card.pages.length}쪽`);
  assert.equal(card.pages.reduce((a, p) => a + p.blocks.length, 0), 50, label);
  const A = LINE.AREA;
  for (const p of card.pages) {
    assert.deepEqual(p.bandPos, BAND2);
    assert.deepEqual(parseBand(p.band), { cat: "lin", set: card.set, page: p.index });
    const rects = p.blocks.map((b) => ({ x0: b.x, y0: b.y, x1: b.x + b.w, y1: b.y + b.h }));
    for (const r of rects) assert.ok(r.x0 >= A.x0 - 0.5 && r.x1 <= A.x1 + 0.5 && r.y0 >= (p.index ? A.yOther : A.yFirst) - 0.5 && r.y1 <= A.yMax + 0.5, `${label} p${p.index} inside`);
    for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
      const a = rects[i], b = rects[j];
      assert.ok(a.x1 + LINE.GAP_X - 0.5 <= b.x0 || b.x1 + LINE.GAP_X - 0.5 <= a.x0 || a.y1 <= b.y0 || b.y1 <= a.y0, `${label} overlap`);
    }
    const keep = [...p.markers.map((m) => ({ x0: m.x - 15, y0: m.y - 15, x1: m.x + m.size + 15, y1: m.y + m.size + 15 })),
      ...[BAND, BAND2].map((B) => ({ x0: B.x0 - 10, y0: B.y - 10, x1: B.x0 + B.n * (B.cell + B.gap), y1: B.y + B.cell + 10 }))];
    for (const r of rects) for (const k of keep) assert.ok(r.x1 <= k.x0 || k.x1 <= r.x0 || r.y1 <= k.y0 || k.y1 <= r.y0, `${label} near marker/band`);
    for (const b of p.blocks) {
      if (b.kind === "pick") { assert.equal(b.hand, null); assert.ok(b.picks.length >= 2 && b.picks.every((q) => q.r === LINE.PICK_R)); continue; }
      assert.equal(b.kind, "line", `${label} ${b.no}`);
      assert.equal(b.hand.den, null); assert.equal(b.hand.bar, null);
      assert.equal(!!b.hand.pre, b.ak === "lin", `${label} ${b.no} y = 머리`);
      const r = b.hand.num;
      assert.ok(r.x >= b.x && r.x + r.w <= b.x + b.w + 0.01 && r.y + r.h <= b.y + b.h, `${label} ${b.no} 칸`);
      assert.ok(r.h >= 70 && r.w >= 180, `${label} ${b.no} 칸 크기 ${r.w}×${r.h}`);
    }
    // 번호가 차례대로(쪽 안에서 왼쪽 → 오른쪽, 위 → 아래)
    const nos = p.blocks.map((b) => b.no);
    assert.deepEqual(nos, [...nos].sort((x, y) => x - y));
  }
}
test("배치: 50칸 · 영역 안 · 겹치지 않음 · 마커 · 띠와 떨어짐 · 식 칸만 「y =」 · 칸 높이", () => {
  checkLayout(CARD, "합성");
  assert.equal(CARD.pages.length, 2);
  assert.ok(CARD.pages.every((p) => new Set(p.blocks.map((b) => b.y)).size <= 9), "쪽마다 9줄까지");
});
test("예전(v1) 판은 없다 — 일차함수 카드를 v1 으로 그리라면 거부", () => {
  assert.throws(() => layoutCard(FAKE, { ver: 1 }), /v1/);
});
test("cardHtml: 쪽마다 SVG · 중2-1 · 손글씨 안내 · 식 칸의 「y =」 · 분수 칸 없음 · 위쪽 띠 자리는 비움", () => {
  const h = cardHtml(CARD);
  assert.equal((h.match(/<svg /g) || []).length, CARD.pages.length);
  const p0 = pageSvg(CARD, CARD.pages[0]);
  assert.ok(p0.includes(FAKE.title) && p0.includes("1/2쪽") && p0.includes("중2-1"));
  assert.ok(p0.includes(INSTRUCTION_LIN[0].slice(0, 12)));
  assert.ok(!h.includes("분수 · 손으로") && !h.includes("분자"));
  const nLin = FAKE.items.filter((it) => it.a.k === "lin").length;
  assert.equal((h.match(/font-style="italic">y<\/tspan> =/g) || []).length, nLin);
  for (const m of p0.matchAll(/<(rect|text|line|circle) ([^>]*)>/g)) {
    const a = Object.fromEntries([...m[2].matchAll(/([\w-]+)="([^"]*)"/g)].map((x) => [x[1], x[2]]));
    const y = Number(a.y ?? a.cy ?? a.y1), x = Number(a.x ?? a.cx ?? a.x1);
    if (Number.isFinite(y) && Number.isFinite(x) && x > 220 && x < 730) assert.ok(y > 112 || y < 50, `위쪽 띠 자리에 그림: ${m[0].slice(0, 60)}`);
  }
  assert.ok(pageSvg(CARD, CARD.pages[1]).includes("답은 칸 안에 한 줄로"));
});

// ── 합성 사진 ─────────────────────────────────────────────────────────────────
/** 한 쪽 그리기(인쇄 + 학생의 연필). fills: { [no]: 쓰는 꼴 } — 손글씨 칸은 그 글자를, 보기는 고른 것을 칠한다 */
function drawPage(card, p, fills, { maskBand = false } = {}) {
  const r = raster(GW, 1478, 236);
  for (const m of p.markers) fillRect(r, m.x, m.y, m.size, m.size, 24);
  fillRect(r, p.orient.x, p.orient.y, p.orient.w, p.orient.h, 24);
  if (!maskBand) bandCells(p.bandPos).forEach((c, i) => { if (p.band[i]) fillRect(r, c.x, c.y, c.size, c.size, 24); else strokeRect(r, c.x, c.y, c.size, c.size, 1, 215); });
  if (p.index === 0) {
    fillRect(r, 300, 126, 400, 28, 40); fillRect(r, 340, 166, 320, 18, 90);
    fillRect(r, 196, 225, 264, 2, 30); fillRect(r, 586, 225, 264, 2, 30);
    fillRect(r, 140, 240, 720, 14, 120); fillRect(r, 170, 261, 660, 14, 120);
  } else { fillRect(r, 290, 128, 420, 22, 40); fillRect(r, 260, 164, 480, 14, 120); }
  for (const b of p.blocks) {
    fillRect(r, b.x + 4, b.y + 4, 13, 17, 20);                         // 번호
    fillRect(r, b.x + 30, b.y + 8, 22, 12, 110);                       // 수 · 식 · 점
    if (b.kind === "pick") {
      for (const q of b.picks) { ring(r, q.x, q.y, q.r, 1.6, 40); strokeRect(r, q.x - 4.5, q.y - 5.5, 9, 11, 1.4, 120); }
    } else {
      const bx = b.hand.num;
      strokeRect(r, bx.x, bx.y, bx.w, bx.h, 1.8, 30);
      if (b.hand.pre) fillRect(r, b.hand.pre.x + 2, b.hand.pre.y - 7, 26, 15, 40);   // 「y =」
    }
    const f = fills[b.no];
    if (!f) continue;
    if (b.kind === "pick") {
      const on = String(f).match(/[ㄱ-ㅎ]/gu) || [];
      for (const q of b.picks) if (on.includes(q.label)) fillCircle(r, q.x, q.y, q.r - 0.6, 52);
      continue;
    }
    const txt = String(f).replace(/^y = /, "").replace(/\s+/g, "");
    handText(r, b.hand.num, txt, b.no % 2 ? 58 : 96);                  // 짝수 번은 연하게
  }
  return r;
}
const FILLS = Object.fromEntries(FAKE.items.map((it) => [it.no, rawOf(it)]));
const BLANK = [5, 21, 33];                                              // 빈 칸(손글씨 · 보기)
for (const n of BLANK) FILLS[n] = "";
assert.equal(FAKE.items[32].a.k, "pick");
const PAGES = CARD.pages.map((p) => drawPage(CARD, p, FILLS));

function checkRead(res, p, label) {
  assert.equal(res.ok, true, `${label} ok (${res.reason})`);
  assert.equal(res.page, p.index); assert.equal(res.ver, 2);
  for (const b of p.blocks) {
    const a = res.answers.find((x) => x.no === b.no);
    assert.ok(a, `${label} no ${b.no}`);
    if (b.kind === "pick") { assert.equal(a.raw, FILLS[b.no], `${label} 보기 ${b.no}`); continue; }
    if (!FILLS[b.no]) { assert.equal(a.flag, null, `${label} ${b.no} 빈 칸`); assert.equal(a.raw, ""); continue; }
    assert.equal(a.flag, "hand", `${label} ${b.no} 손글씨 ${JSON.stringify(a.hand)}`);
    assert.deepEqual(a.hand, { num: true, den: false });
  }
}

console.log("OMR 판독 (합성 사진)");
test("1쪽: 기울여 찍은 사진 — 손글씨 한 줄 칸(글씨 유무) · 보기 동그라미 · 빈 칸", () => {
  const img = photograph(PAGES[0], 1300, 1820, [[95, 70], [1215, 110], [1250, 1745], [60, 1700]], 3);
  checkRead(readCardPhoto(img, { 2: CARD }), CARD.pages[0], "p1");
});
test("2쪽을 거꾸로(180°) · 원근 심하게", () => {
  const img = photograph(PAGES[1], 1400, 1900, [[1300, 1840], [70, 1760], [180, 120], [1180, 60]], 7);
  checkRead(readCardPhoto(img, CARD), CARD.pages[1], "p2");
});
test("그림자 경계가 칸을 가로질러도 빈 칸은 빈 칸 · 쓴 칸은 쓴 칸", () => {
  for (const k of [0, 1]) {
    const img = photograph(PAGES[k], 1300, 1820, [[90, 80], [1210, 70], [1240, 1740], [70, 1750]], 13 + k, 100, 900);
    checkRead(readCardPhoto(img, { 2: CARD }), CARD.pages[k], `그림자 p${k + 1}`);
  }
});
test("손글씨 조각(handCrops): 쓴 칸만 · 분모 없음 · 식 칸이 수 칸보다 넓다 · 밝기 펴기", () => {
  const res = readCardPhoto(photograph(PAGES[0], 1300, 1820, [[95, 70], [1215, 110], [1250, 1745], [60, 1700]], 17), { 2: CARD });
  assert.equal(res.ok, true);
  const crops = handCrops(res);
  const want = CARD.pages[0].blocks.filter((b) => b.kind === "line" && FILLS[b.no]).map((b) => b.no);
  assert.deepEqual(crops.map((c) => c.no), want);
  assert.ok(!crops.some((c) => BLANK.includes(c.no)));
  for (const c of crops) {
    assert.equal(c.den, null);
    const g = c.num.gray, s = [...g].sort((a, b) => a - b);
    // 한 줄 칸은 넓어 사진의 조명 기울기가 조각 안에 남는다(바탕 230 안팎) — 바탕과 글씨의 차이만 크면 된다
    const bg = s[Math.floor(s.length * 0.5)], inkv = s[Math.floor(s.length * 0.005)];
    assert.ok(bg >= 225 && inkv <= 40 && bg - inkv >= 190, `${c.no} 밝기 ${bg} · ${inkv} · ${c.num.width}×${c.num.height}`);
  }
  const ak = Object.fromEntries(FAKE.items.map((it) => [it.no, it.a.k]));
  const w = (k) => Math.max(...crops.filter((c) => ak[c.no] === k).map((c) => c.num.width));
  assert.ok(w("lin") > w("pt") && w("pt") > w("num"), `폭 ${w("lin")} · ${w("pt")} · ${w("num")}`);
});
test("다른 범주 · 다른 세트의 카드면 거부(other-set)", () => {
  const other = layoutCard({ ...FAKE, no: 4 });
  const r = readCardPhoto(photograph(drawPage(other, other.pages[0], {}), 1200, 1700, [[60, 60], [1140, 60], [1140, 1640], [60, 1640]], 5), { 2: CARD });
  assert.equal(r.ok, false); assert.equal(r.reason, "other-set"); assert.equal(r.band.set, 4);
});
test("띠를 못 읽으면 band → 쪽을 고르면 그 쪽 배치로 읽는다", () => {
  const img = photograph(drawPage(CARD, CARD.pages[1], FILLS, { maskBand: true }), 1300, 1820, [[90, 70], [1220, 100], [1240, 1750], [60, 1710]], 41);
  assert.equal(readCardPhoto(img, { 2: CARD }).reason, "band");
  const res = readCardPhoto(img, { 2: CARD }, { page: 1 });
  checkRead(res, CARD.pages[1], "쪽 고름");
  assert.equal(res.bandOk, false);
});
test("판독 → 판정: AI 가 읽은 ASCII 글자(y= 없이 · 마이너스 - · 점 괄호)도 그대로 채점", () => {
  const byK = (k) => FAKE.items.find((it) => it.a.k === k);
  const L = byK("lin"), P = byK("pt"), N = byK("num");
  const ascii = (s) => s.replace(/−/g, "-").replace(/^y = /, "").replace(/\s+/g, "");
  for (const it of [L, P, N]) assert.equal(judge(it, ascii(rawOf(it))).ok, true, ascii(rawOf(it)));
});

// ── 세트 데이터(public/concept-sets/lin) ─────────────────────────────────────────
console.log("데이터");
const HAS = fs.existsSync(path.join(DIR, "index.json"));
test("범주 목록에 lin 이 있으면 데이터도 있다", () => {
  assert.ok(CATEGORIES.some((c) => c.id === "lin"));
  assert.ok(HAS, "public/concept-sets/lin/index.json 이 없다");
});
if (HAS) {
  const INDEX = JSON.parse(fs.readFileSync(path.join(DIR, "index.json"), "utf8"));
  const CAT = INDEX.categories[0];
  const SETS = CAT.sets.map((s) => JSON.parse(fs.readFileSync(path.join(DIR, `${String(s.no).padStart(2, "0")}.json`), "utf8")));
  test("index: 범주 lin · 묶음(과학 1-1 ~ 2-2)이 세트를 한 번씩 · 세트마다 50문항 · 쪽 수", () => {
    assert.equal(CAT.id, "lin"); assert.equal(CAT.title, "일차함수와 그래프");
    assert.ok(CAT.sets.length >= 1);
    const inGroups = CAT.groups.flatMap((g) => g.sets).sort((a, b) => a - b);
    assert.deepEqual(inGroups, CAT.sets.map((s) => s.no).sort((a, b) => a - b));
    assert.ok(CAT.groups.every((g) => /^과학 [12]-[12]$/.test(g.title)));
    for (const s of CAT.sets) { assert.ok(s.icon && s.short && s.key && s.title); assert.equal(s.n, 50); assert.ok(s.pages.problems >= 8 && s.pages.solutions >= 15); }
  });
  test("세트 JSON: 문항 50 · 하 15 중 25 상 10 · 답 꼴 · OMR 칸 · 방침 이름표 · 큐 키 · 인쇄 HTML 짝", () => {
    for (const s of SETS) {
      assert.equal(s.cat, "lin"); assert.deepEqual(s.labels, ["주어진 것", "구할 것"]);
      assert.equal(s.items.length, 50, s.key);
      const lv = s.items.reduce((m, it) => ((m[it.lv] = (m[it.lv] || 0) + 1), m), {});
      assert.deepEqual(lv, { 하: 15, 중: 25, 상: 10 }, s.key);
      const kinds = {};
      for (const it of s.items) {
        assert.ok(it.id && it.q && it.a && it.omr && it.s, `${s.key} ${it.id}`);
        assert.ok(["num", "lin", "pt", "pick"].includes(it.a.k), `${s.key} ${it.id} kind ${it.a.k}`);
        kinds[it.a.k] = (kinds[it.a.k] || 0) + 1;
        if (it.a.k === "pick") assert.deepEqual(it.omr, { o: it.a.o.length }, `${s.key} ${it.id} omr`);
        else assert.deepEqual(it.omr, { w: it.a.k }, `${s.key} ${it.id} omr`);
        if (it.a.k === "num") assert.equal(it.a.n === 0 ? 1 : Math.abs(gcd(it.a.n, it.a.d)), 1, `${s.key} ${it.id} 기약`);
        assert.deepEqual(it.s.labs, ["주어진 것", "구할 것"], `${s.key} ${it.id} labs`);
        assert.ok(Array.isArray(it.s.board) && it.s.board.length === it.s.steps.length, `${s.key} ${it.id} board`);
        assert.equal(it.s.anim.length, it.s.board.length, `${s.key} ${it.id} anim`);
        for (const step of it.s.anim) for (const c of step) {
          if (/^(line|hint):/.test(c.k)) continue;
          assert.ok(it.s.dg && (it.s.dg.includes(`data-k="${c.k}"`) || it.s.dg.includes(`data-ka="${c.k}"`)), `${s.key} ${it.id} cue ${c.k}`);
        }
        assert.ok(!/<script|√|%/i.test(JSON.stringify({ q: it.q, a: it.a.t })), `${s.key} ${it.id} 금지 기호`);
      }
      assert.ok((kinds.lin || 0) >= 8, `${s.key} 식 답 ${kinds.lin}`);
      assert.ok((kinds.pick || 0) <= 8, `${s.key} 보기 답 ${kinds.pick}`);
      const nn = String(s.no).padStart(2, "0");
      for (const d of ["problems", "solutions"]) assert.ok(fs.existsSync(path.join(DIR, "print", `${nn}-${d}.html`)), `${nn}-${d}.html`);
    }
  });
  test("인쇄 HTML: 글꼴은 jsDelivr · file:// 없음 · @page", () => {
    for (const f of fs.readdirSync(path.join(DIR, "print"))) {
      const h = fs.readFileSync(path.join(DIR, "print", f), "utf8");
      assert.ok(!h.includes("file://"), f);
      assert.ok(h.includes("https://cdn.jsdelivr.net/npm/@fontsource/"), f);
      assert.ok(h.includes("@page{size:A4"), f);
    }
  });
  test("모든 문항: 정답의 쓰는 꼴(rawOf)과 그 ASCII 꼴(AI 판독)은 스스로 정답 · 정답 글자 있음", () => {
    for (const s of SETS) for (const it of s.items) {
      assert.equal(judge(it, rawOf(it)).ok, true, `${s.key} ${it.id} ${rawOf(it)}`);
      const ascii = rawOf(it).replace(/−/g, "-").replace(/^y = /, "").replace(/\s+/g, "");
      assert.equal(judge(it, ascii).ok, true, `${s.key} ${it.id} ${ascii}`);
      assert.ok(answerText(it).length > 0);
    }
  });
  test("3단 해설: 방침은 「주어진 것 · 구할 것」 · 전개 · 확인 · 모범 답안 · 채점 기준 · 큐 키", () => {
    for (const s of SETS) for (const it of s.items) {
      const h = solutionHtml(it);
      for (const w of ["방침", "주어진 것", "구할 것", "전개", "확인", "모범 답안", "채점 기준"]) assert.ok(h.includes(w), `${s.key} ${it.id} ${w}`);
      assert.ok(!h.includes("포지티브") && !h.includes("네거티브"), `${s.key} ${it.id} 확률 이름표`);
      assert.deepEqual(missingCueKeys(it, h), [], `${s.key} ${it.id} cue keys`);
      assert.ok(!/<script|\son[a-z]+=/i.test(h), "safe");
      const q = questionHtml(it);
      assert.ok(q.length > 20 && !/<script|\son[a-z]+=/i.test(q));
    }
  });
  test("OMR: 세트마다 손글씨 한 줄 카드 — 50칸 · 영역 안 · 겹치지 않음 · 띠", () => {
    for (const s of SETS) checkLayout(layoutCard({ cat: "lin", no: s.no, title: s.title, short: s.short, items: s.items }), s.key);
  });
}
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; }

console.log(`\n${passed} passed, ${failed} failed`);
if (failed) process.exit(1);
