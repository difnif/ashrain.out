// 컨셉 문제 「종이처럼 풀기」 — 손글씨 꼴(ink.js) · 답안 · 채점(paperlogic.js) 노드 테스트
//   node tests/conceptsets-paper.test.mjs
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { hasInk, inkBox, hasDenominator, inkSvg, strokePath, normalizeRead, inkSheets, PAD_H } from "../src/pages/sets/ink.js";
import { isAnswered, togglePick, rawFor, gradePaper, levelSummary, answerLabel } from "../src/pages/sets/paperlogic.js";
import { rawOf } from "../src/lib/conceptsets.js";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const SET = JSON.parse(fs.readFileSync(path.join(ROOT, "public/concept-sets/prob/01.json"), "utf8"));
let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log("  ok  " + name); }
  catch (e) { failed++; console.log("FAIL  " + name + "\n      " + (e && e.stack || e).toString().split("\n").slice(0, 5).join("\n      ")); }
}

// 손글씨 꼴: 판 좌표 정수, 획마다 [x0,y0,x1,y1,…]
const INT = { k: "ink", lay: "int", w: 320, h: PAD_H.int, s: [[40, 100, 60, 40, 80, 100], [100, 60, 140, 60]], wd: [3.4, 3.4] };
const FRAC_UP = { k: "ink", lay: "frac", w: 320, h: PAD_H.frac, s: [[150, 40, 150, 90]], wd: [3] };            // 분자만
const FRAC = { ...FRAC_UP, s: [[150, 40, 150, 90], [130, 150, 170, 150, 170, 200]], wd: [3, 3] };                // 분자 + 분모

console.log("손글씨");
test("hasInk · inkBox: 빈 판 · 점 하나 · 여러 획", () => {
  assert.equal(hasInk(null), false);
  assert.equal(hasInk({ k: "ink", s: [] }), false);
  assert.equal(hasInk({ k: "ink", s: [[5]] }), false);
  assert.equal(hasInk({ k: "ink", s: [[5, 6]] }), true);
  assert.equal(inkBox({ k: "ink", s: [] }), null);
  assert.deepEqual(inkBox(INT), { x0: 40, y0: 40, x1: 140, y1: 100 });
});
test("hasDenominator: 분수 판에서 가로선 아래에 쓴 글씨만", () => {
  assert.equal(hasDenominator(FRAC_UP), false);
  assert.equal(hasDenominator(FRAC), true);
  assert.equal(hasDenominator({ ...FRAC, lay: "int" }), false);
});
test("inkSvg: 글씨만 잘라 비율 유지 · 분수는 분모가 있을 때만 가로선 · NaN 없음", () => {
  const a = inkSvg(INT), b = inkSvg(FRAC_UP), c = inkSvg(FRAC);
  for (const s of [a, b, c]) { assert.ok(s.startsWith("<svg") && s.endsWith("</svg>")); assert.ok(!/NaN|undefined/.test(s), s); }
  assert.equal((a.match(/<path /g) || []).length, 2);
  assert.ok(!/<line /.test(b) && /<line /.test(c), "분모를 쓴 분수만 가로선");
  const [w, h] = a.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).slice(1).map(Number);
  assert.equal(w, 100 + 12); assert.equal(h, 60 + 12);
  assert.equal(inkSvg({ k: "ink", s: [] }), "");
});
test("strokePath: 점 하나는 아주 짧은 선 · 여러 점은 2차 곡선", () => {
  assert.equal(strokePath([10, 20]), "M10 20l0.01 0");
  const d = strokePath([0, 0, 10, 0, 20, 10, 30, 10]);
  assert.ok(d.startsWith("M0 0Q10 0 15 5Q20 10 25 10L30 10"), d);
});
test("normalizeRead: 빈칸 · 전각 · 빼기 기호 · 「답:」 · 괄호 · 두 수 구분", () => {
  assert.equal(normalizeRead(" 5 / 12 "), "5/12");
  assert.equal(normalizeRead("１２"), "12");
  assert.equal(normalizeRead("−3"), "-3");
  assert.equal(normalizeRead("답: 7"), "7");
  assert.equal(normalizeRead("(3,4)"), "3, 4");
  assert.equal(normalizeRead("3|4"), "3, 4");
  assert.equal(normalizeRead(null), "");
});
test("inkSheets: 캔버스가 없으면(노드) 빈 묶음", () => {
  assert.deepEqual(inkSheets([{ no: 1, ink: INT }], { doc: null }), []);
});

console.log("답안 · 채점");
test("isAnswered: 타자 · 보기 · 손글씨 · 빈 답", () => {
  assert.equal(isAnswered(null), false);
  assert.equal(isAnswered({ k: "text", raw: "  " }), false);
  assert.equal(isAnswered({ k: "text", raw: "12" }), true);
  assert.equal(isAnswered({ k: "pick", sel: [] }), false);
  assert.equal(isAnswered({ k: "pick", sel: ["ㄱ"] }), true);
  assert.equal(isAnswered({ ...INT, s: [] }), false);
  assert.equal(isAnswered(INT), true);
});
test("togglePick: 여러 개 체크(중복 허용) · 다시 누르면 해제 · 보기 차례로 · 다 지우면 빈 답", () => {
  let a = togglePick(null, "ㄷ");
  assert.deepEqual(a, { k: "pick", sel: ["ㄷ"] });
  a = togglePick(a, "ㄱ");
  assert.deepEqual(a.sel, ["ㄱ", "ㄷ"]);
  a = togglePick(a, "ㄹ");
  assert.deepEqual(a.sel, ["ㄱ", "ㄷ", "ㄹ"]);
  a = togglePick(a, "ㄷ");
  assert.deepEqual(a.sel, ["ㄱ", "ㄹ"]);
  a = togglePick(togglePick(a, "ㄱ"), "ㄹ");
  assert.equal(a, null);
  assert.deepEqual(togglePick({ k: "text", raw: "3" }, "ㄴ"), { k: "pick", sel: ["ㄴ"] }, "다른 꼴의 답은 버리고 새로");
});
test("rawFor · answerLabel: 손글씨는 판독 글자(못 읽으면 null)", () => {
  assert.equal(rawFor({ k: "text", raw: " 5/12 " }), "5/12");
  assert.equal(rawFor({ k: "pick", sel: ["ㄱ", "ㄷ"] }), "ㄱ, ㄷ");
  assert.equal(rawFor(INT, undefined), null);
  assert.equal(rawFor(INT, " 1 2 "), "1 2");
  assert.equal(answerLabel(INT, null), "손글씨");
  assert.equal(answerLabel(INT, "5 / 12"), "5/12");
  assert.equal(answerLabel(null), "");
});
test("gradePaper: 맞음 · 틀림 · 빈칸(그냥 넘어감) · 손글씨 못 읽음(점수에서 뺌) · 보기 더 고르면 틀림", () => {
  const it = (k) => SET.items.find((x) => x.a.k === k);
  const ints = SET.items.filter((x) => x.a.k === "int");
  const fr = it("frac"), pk = it("pick");
  const answers = {
    [ints[0].no]: { k: "text", raw: rawOf(ints[0]) },                         // 맞음(타자)
    [ints[1].no]: { k: "text", raw: String(ints[1].a.v + 1) },               // 틀림
    [ints[2].no]: INT,                                                       // 손글씨 — 정답으로 읽힘
    [ints[3].no]: INT,                                                       // 손글씨 — 못 읽음
    [fr.no]: { k: "text", raw: `${fr.a.n * 2}/${fr.a.d * 2}` },              // 약분 안 한 같은 값 → 맞음(안내)
    [pk.no]: { k: "pick", sel: [...pk.a.v, ...["ㄱ", "ㄴ", "ㄷ", "ㄹ"].filter((x) => !pk.a.v.includes(x)).slice(0, 1)] },   // 하나 더 → 틀림
  };
  const reads = { [ints[2].no]: rawOf(ints[2]), [ints[3].no]: "" };
  const g = gradePaper(SET, answers, reads);
  const st = Object.fromEntries(g.rows.map((r) => [r.no, r.status]));
  assert.equal(st[ints[0].no], "ok");
  assert.equal(st[ints[1].no], "wrong");
  assert.equal(st[ints[2].no], "ok");
  assert.equal(st[ints[3].no], "unread");
  assert.equal(st[fr.no], "ok");
  assert.ok(/기약분수/.test(g.rows.find((r) => r.no === fr.no).note));
  assert.equal(st[pk.no], "wrong");
  assert.equal(g.n, 50);
  assert.deepEqual(g.counts, { ok: 3, wrong: 2, blank: 44, unread: 1 });
  assert.equal(g.score, 3);
  const lv = levelSummary(SET, g);
  assert.equal(lv.reduce((a, [, ok]) => a + ok, 0), 3);
  assert.equal(lv.reduce((a, [, , n]) => a + n, 0), 50);
  // 정답대로 보기를 고르면 맞음
  assert.equal(gradePaper(SET, { [pk.no]: { k: "pick", sel: [...pk.a.v] } }).rows.find((r) => r.no === pk.no).status, "ok");
  // 아무것도 안 쓰고 제출해도 된다
  assert.deepEqual(gradePaper(SET, {}).counts, { ok: 0, wrong: 0, blank: 50, unread: 0 });
});

console.log(`\n${passed}/${passed + failed} 통과`);
if (failed) process.exit(1);
