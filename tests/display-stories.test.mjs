// node tests/display-stories.test.mjs — 교실 모니터 「축구」·「서술형」 묶음 검산. 실패 시 exit 1.
//   1) 화면에 나오는 수를 facts-soccer.js · facts-essay.js 와 따로 다시 계산해 맞춰 본다
//      (피타고라스 · 교점 · 계급(이상·미만) · 확률은 분수로 정확히, 경우의 수는 모두 늘어놓아 센다).
//   2) 판서 · 자막에 쓰는 글자에 맞는 수가 들어 있는지 본다.
//   3) 열두 장면 × 초등/중등 × 다크/라이트를 처음부터 끝까지 그려 보고 오류 · NaN 이 없는지 본다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { CORNER, SETPIECE, THROUGH, TRIANGLE, COUNTER, XG } from "../src/features/display/facts-soccer.js";
import { RAILS, WRONGWAY, CLUB, RPS, SIGN, SHIRT } from "../src/features/display/facts-essay.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}
const near = (a, b, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${a} ≠ ${b}`);
const has = (s, frag) => assert.ok(String(s).includes(frag), `"${s}" 에 "${frag}" 없음`);

/* ── 분수(정수 두 개로 정확히) ── */
const g = (a, b) => (b ? g(b, a % b) : Math.abs(a));
const Q = (p, q = 1) => { if (q < 0) { p = -p; q = -q; } const d = g(p, q) || 1; return [p / d, q / d]; };
const add = (a, b) => Q(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const sub = (a, b) => Q(a[0] * b[1] - b[0] * a[1], a[1] * b[1]);
const mul = (a, b) => Q(a[0] * b[0], a[1] * b[1]);
const div = (a, b) => Q(a[0] * b[1], a[1] * b[0]);
const eqQ = (a, b) => assert.deepEqual(Q(...a), Q(...b), `${a.join("/")} ≠ ${b.join("/")}`);
const tx = ([p, q]) => (q === 1 ? String(p) : `{${p}/${q}}`);
/** 정수의 제곱근(제곱수가 아니면 실패) */
const isqrt = (v) => { const r = Math.round(Math.sqrt(v)); assert.equal(r * r, v, `${v} 는 제곱수가 아님`); return r; };
/** 두 직선 y = m1 x + b1, y = m2 x + b2 의 교점(분수) */
const meetQ = (m1, b1, m2, b2) => { const x = div(sub(b2, b1), sub(m1, m2)); return [x, add(mul(m1, x), b1)]; };
/** [이상, 미만, …] 표에서 d 가 드는 행 — 경계값은 '이상' 쪽 */
const rowOf = (tab, d) => { const out = []; tab.forEach((r, i) => { if (r[0] <= d && d < r[1]) out.push(i); }); assert.equal(out.length, 1, `${d} 의 계급이 하나가 아님`); return out[0]; };

/* ══════════ 축구 ══════════ */
test("축구 1 코너킥: KF 24 (10·24·26), FT 7.5, HT 12.5 (7.5·10·12.5), 날아간 길 38.5 m", () => {
  const KF = isqrt(26 * 26 - 10 * 10);
  assert.equal(KF, 24); assert.equal(CORNER.KF, KF);
  eqQ([63, 2], [CORNER.KT * 2, 2]);                                  // 31.5 = 63/2
  const FT = sub(Q(63, 2), Q(KF)); eqQ(FT, [15, 2]); near(CORNER.FT, 7.5);
  const HT2 = add(mul(FT, FT), Q(100)); eqQ(HT2, [625, 4]); near(CORNER.HT, 12.5);   // 12.5² = 625/4
  near(CORNER.flight, 38.5);
  // 그림 좌표: K(0,0) → H 까지 26, H 는 골라인에서 10, T 는 골문(34 ± 3.66) 안
  near(Math.hypot(...CORNER.P.H), 26); near(CORNER.P.H[1], 10); near(CORNER.P.T[0], 31.5);
  assert.ok(Math.abs(CORNER.P.T[0] - CORNER.GOAL.c) < CORNER.GOAL.w / 2);
  has(CORNER.E.ft, "31.5 − 24 = ‹7.5 m›"); has(CORNER.E.sum, "26 + 12.5 = ‹38.5 m›");
  has(CORNER.M.kf2, "676 − 100 = 576 = 24²"); has(CORNER.M.eq2, "7.5² + 10² = 156.25"); has(CORNER.M.ht, "12.5²  →  HT = ‹12.5 m›");
  has(CORNER.M.ratio, "5 : 12 : 13 (× 2)"); has(CORNER.M.ratio, "3 : 4 : 5 (× 2.5)");
});

test("축구 2 세트피스: FH 25 · HG 10(경계값 → 10 이상 15 미만), {2/5} × {1/10} = {1/25}, 100번 → 40번 → 4번", () => {
  const FH = isqrt((26 - 6) ** 2 + (23 - 8) ** 2), HG = isqrt(6 ** 2 + 8 ** 2);
  assert.equal(FH, 25); assert.equal(HG, 10); near(SETPIECE.FH, FH); near(SETPIECE.HG, HG);
  const ci = rowOf(SETPIECE.CROSS, FH), hi = rowOf(SETPIECE.HEAD, HG);
  assert.deepEqual([SETPIECE.CROSS[ci][0], SETPIECE.CROSS[ci][1]], [20, 30]);
  assert.deepEqual([SETPIECE.HEAD[hi][0], SETPIECE.HEAD[hi][1]], [10, 15]);   // 10 은 '10 이상' 쪽
  assert.equal(SETPIECE.ci, ci); assert.equal(SETPIECE.hi, hi);
  const pC = Q(SETPIECE.CROSS[ci][3], SETPIECE.CROSS[ci][2]), pH = Q(SETPIECE.HEAD[hi][3], SETPIECE.HEAD[hi][2]);
  eqQ(pC, [2, 5]); eqQ(pH, [1, 10]); eqQ(mul(pC, pH), [1, 25]); eqQ(SETPIECE.p, [1, 25]);
  // 함정: 10 m 를 '5 이상 10 미만' 으로 읽으면 {3/20}
  eqQ(Q(SETPIECE.HEAD[rowOf(SETPIECE.HEAD, 9.99)][3], SETPIECE.HEAD[rowOf(SETPIECE.HEAD, 9.99)][2]), [3, 20]);
  // 자연 빈도
  assert.equal(100 * pC[0] / pC[1], 40); assert.equal(40 * pH[0] / pH[1], 4);
  assert.equal(SETPIECE.nHead, 40); assert.equal(SETPIECE.nGoal, 4);
  assert.deepEqual(SETPIECE.tot.cross, [250, 97]); assert.deepEqual(SETPIECE.tot.head, [200, 28]);
  has(SETPIECE.M.fh, "20² + 15² = 625 = 25²"); has(SETPIECE.M.hg, "6² + 8² = 100 = 10²");
  has(SETPIECE.M.prod, "{2/5} × {1/10} = ‹{1/25}›"); has(SETPIECE.E.edge, "‘10 이상 15 미만’");
  has(SETPIECE.E.n1, "‹40›"); has(SETPIECE.E.n2, "‹4›"); has(SETPIECE.E.n3, "100번 중 ‹4›번 — 25번에 1번꼴");
  assert.deepEqual(SETPIECE.M.grid, ["100", "× {2/5} = 40", "× {1/10} = 4"]);
});

test("축구 3 쓰루패스: y = {7/24}x 와 y = −{3/4}x + 25 의 교점 M(24, 7), OM 25 · SM 20, 2초 · 2.5초 → 0.5초 먼저", () => {
  const [x, y] = meetQ(Q(7, 24), Q(0), Q(-3, 4), Q(25));
  eqQ(x, [24, 1]); eqQ(y, [7, 1]);
  assert.deepEqual(THROUGH.pts.M, [24, 7]);
  assert.equal(-3 / 4 * 8 + 25, 19); assert.deepEqual(THROUGH.pts.S, [8, 19]);   // S 는 달리는 직선 위
  assert.equal(isqrt(24 ** 2 + 7 ** 2), 25); assert.equal(isqrt(16 ** 2 + 12 ** 2), 20);
  near(THROUGH.OM, 25); near(THROUGH.SM, 20);
  eqQ(div(Q(25), Q(25, 2)), [2, 1]); eqQ(div(Q(20), Q(8)), [5, 2]); eqQ(sub(Q(5, 2), Q(2)), [1, 2]);
  near(THROUGH.tBall, 2); near(THROUGH.tRun, 2.5); near(THROUGH.lead, 0.5);
  // 수비수는 패스 길(O→M) · 달리는 길(S→M) 에서 떨어져 있다
  const segDist = (p, a, b) => { const [ax, ay] = a, [bx, by] = b, dx = bx - ax, dy = by - ay; const k = Math.max(0, Math.min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy))); return Math.hypot(p[0] - ax - k * dx, p[1] - ay - k * dy); };
  for (const d of THROUGH.defenders) {
    assert.ok(segDist(d, [0, 0], [24, 7]) > 1.5, `수비수 ${d} 가 패스 길 위`);
    assert.ok(segDist(d, [8, 19], [24, 7]) > 1.5, `수비수 ${d} 가 달리는 길 위`);
  }
  has(THROUGH.M.sol, "M(24, 7)"); has(THROUGH.M.om, "24² + 7² = 625 = 25²"); has(THROUGH.M.sm, "16² + 12² = 400 = 20²");
  has(THROUGH.E.tb, "25 ÷ 12.5 = ‹2›초"); has(THROUGH.E.tr, "20 ÷ 8 = ‹2.5›초"); has(THROUGH.E.lead, "‹0.5초› 먼저 출발");
});

test("축구 4 삼각패스: A(3, 2) · B(12, 14) · C(28, 2), 밑변 25 · 높이 12 → 150 m² (직사각형 300 − 54 − 96)", () => {
  const b = sub(Q(2), mul(Q(-3, 4), Q(28)));              // B→C : 2 = −3/4 × 28 + b
  eqQ(b, [23, 1]); assert.equal(TRIANGLE.bcB, 23);
  const A = div(add(Q(2), Q(2)), Q(4, 3));                // 4/3 x − 2 = 2
  eqQ(A, [3, 1]); assert.deepEqual(TRIANGLE.A, [3, 2]);
  const [bx, by] = meetQ(Q(4, 3), Q(-2), Q(-3, 4), Q(23));
  eqQ(bx, [12, 1]); eqQ(by, [14, 1]); assert.deepEqual(TRIANGLE.B, [12, 14]);
  const shoelace = (P) => Math.abs(P.reduce((s, p, i) => s + p[0] * P[(i + 1) % P.length][1] - P[(i + 1) % P.length][0] * p[1], 0)) / 2;
  assert.equal(shoelace([[3, 2], [12, 14], [28, 2]]), 150);
  assert.equal(TRIANGLE.base, 25); assert.equal(TRIANGLE.height, 12); assert.equal(TRIANGLE.area, 150);
  assert.equal(TRIANGLE.rect - TRIANGLE.left - TRIANGLE.right, 150);
  assert.equal(TRIANGLE.left, (9 * 12) / 2); assert.equal(TRIANGLE.right, (16 * 12) / 2);
  has(TRIANGLE.E.area, "300 − 54 − 96 = ‹150 m²›"); has(TRIANGLE.M.area, "{1/2} × 25 × 12 = ‹150 m²›");
  has(TRIANGLE.M.trap, "높이를 14로 쓰면 175"); has(TRIANGLE.M.bb, "B(12, 14)"); has(TRIANGLE.M.a, "A(3, 2)");
});

test("축구 5 역습: R(48, 36) · C(63, 16), OR 60 · RC 25 · OC 65 → 20 m 더, 오각형 2268 − 150 = 2118 m²", () => {
  const [rx, ry] = meetQ(Q(3, 4), Q(0), Q(-4, 3), Q(100));
  const [cx, cy] = meetQ(Q(16, 63), Q(0), Q(-4, 3), Q(100));
  eqQ(rx, [48, 1]); eqQ(ry, [36, 1]); eqQ(cx, [63, 1]); eqQ(cy, [16, 1]);
  assert.deepEqual(COUNTER.R, [48, 36]); assert.deepEqual(COUNTER.C, [63, 16]);
  assert.equal(isqrt(48 ** 2 + 36 ** 2), 60); assert.equal(isqrt(15 ** 2 + 20 ** 2), 25); assert.equal(isqrt(63 ** 2 + 16 ** 2), 65);
  near(COUNTER.OR, 60); near(COUNTER.RC, 25); near(COUNTER.OC, 65); near(COUNTER.more, 20);
  // 오각형 O-H-C-R-K 의 넓이를 신발끈 공식으로 따로
  const P = [[0, 0], [63, 0], [63, 16], [48, 36], [0, 36]];
  const area = Math.abs(P.reduce((s, p, i) => s + p[0] * P[(i + 1) % 5][1] - P[(i + 1) % 5][0] * p[1], 0)) / 2;
  assert.equal(area, 2118); assert.equal(COUNTER.penta, 2118); assert.equal(COUNTER.rect, 2268); assert.equal(COUNTER.tri, 150);
  has(COUNTER.E.more, "85 − 65 = ‹20 m› 더"); has(COUNTER.E.penta, "2268 − 150 = ‹2118 m²›");
  has(COUNTER.M.r, "R(48, 36)"); has(COUNTER.M.c, "C(63, 16)"); has(COUNTER.M.more, "60 + 25 − 65 = ‹20 m›");
});

test("축구 6 xG: 5 · 10 · 20 m (10 · 20 은 경계값), {1/4} · {1/8} · {1/25}, 적어도 한 골 {37/100} — 800경기 → 296경기", () => {
  const D = [[3, 4], [8, 6], [16, 12]].map(([a, b]) => isqrt(a * a + b * b));
  assert.deepEqual(D, [5, 10, 20]); assert.deepEqual(XG.D, D);
  const rows = D.map((d) => rowOf(XG.TAB, d));
  assert.deepEqual(rows, [0, 1, 2]); assert.deepEqual(XG.cls, rows);
  const P = rows.map((i) => Q(XG.TAB[i][3], XG.TAB[i][2]));
  assert.deepEqual(P, [[1, 4], [1, 8], [1, 25]]); assert.deepEqual(XG.P, P);
  // 2³ 가지(골 / 골 아님)를 모두 늘어놓아 '골이 하나도 없는' 경우만 빼기
  let none = Q(0), some = Q(0);
  for (let m = 0; m < 8; m++) {
    let pr = Q(1);
    for (let k = 0; k < 3; k++) pr = mul(pr, (m >> k) & 1 ? P[k] : sub(Q(1), P[k]));
    if (m === 0) none = add(none, pr); else some = add(some, pr);
  }
  eqQ(none, [63, 100]); eqQ(some, [37, 100]); eqQ(XG.none, none); eqQ(XG.atLeast, some);
  // 더하면 틀린다
  assert.notDeepEqual(add(add(P[0], P[1]), P[2]), some);
  // 800경기의 사슬
  assert.equal(XG.N, 4 * 8 * 25);
  assert.deepEqual(XG.miss, [800, 600, 525, 504]); assert.deepEqual(XG.goals, [200, 75, 21]);
  assert.equal(XG.hit, 296); assert.equal(200 + 75 + 21, 296); assert.equal(XG.per100, 37);
  has(XG.M.none, "{3/4} × {7/8} × {24/25} = {63/100}"); has(XG.M.ans, "1 − {63/100} = ‹{37/100}›");
  assert.deepEqual(XG.M.chain, ["1", "{3/4}", "{21/32}", "{63/100}"]);
  has(XG.E.hit, "800 − 504 = 296경기"); has(XG.E.per, "‹37›경기"); assert.deepEqual(XG.E.ops, ["4번 중 3번", "8번 중 7번", "25번 중 24번"]);
  has(XG.M.edge, "10 m, 20 m는 경계값");
});

/* ══════════ 서술형 ══════════ */
test("서술형 1 두 갈래 선로: 갈림목 네 곳을 모두 늘어놓으면(16가지) 빈 선로 {3/8}, {2/5} 는 틀림 · 전차 8대 → 2 · 2 · 2 · 1 · 1", () => {
  let empty = 0;
  const cnt = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
  for (let m = 0; m < 16; m++) {
    const [a, b, c, d] = [m & 1, (m >> 1) & 1, (m >> 2) & 1, (m >> 3) & 1];     // 0 = 왼쪽(위), 1 = 오른쪽(아래)
    const end = a === 0 ? (b === 0 ? "1" : "2") : c === 0 ? "3" : d === 0 ? "4" : "5";
    cnt[end]++;
    if (RAILS.PEOPLE[end] === 0) empty++;
  }
  eqQ([empty, 16], [3, 8]); eqQ(RAILS.pEmpty, [3, 8]);
  for (const e of RAILS.ENDS) eqQ(RAILS.P[e], [cnt[e], 16]);
  assert.notDeepEqual(Q(...RAILS.wrong), Q(3, 8)); eqQ(RAILS.wrong, [2, 5]);
  assert.deepEqual(RAILS.EMPTY, ["2", "4"]);
  // 장면의 전차 8대: 선로마다 들어간 수가 8 × 확률과 같다
  const got = {}; for (const e of RAILS.TRAM_ENDS) got[e] = (got[e] || 0) + 1;
  for (const e of RAILS.ENDS) assert.equal(got[e] || 0, (8 * cnt[e]) / 16, `선로 ${e}`);
  assert.deepEqual(RAILS.COUNT, { 1: 2, 2: 2, 3: 2, 4: 1, 5: 1 }); assert.equal(RAILS.nEmpty, 3);
  has(RAILS.E.empty, "= ‹3대›"); has(RAILS.E.ans, "8대 중 3대 → ‹{3/8}›"); has(RAILS.E.trap, "{2/5}?");
  has(RAILS.M.p[0], "{1/2} × {1/2} = {1/4}"); has(RAILS.M.p[1], "{1/2} × {1/2} × {1/2} = {1/8}");
  has(RAILS.M.sum, "{1/4} + {1/8} = ‹{3/8}›"); has(RAILS.M.each, "①②③ {1/4},  ④⑤ {1/8}");
});

test("서술형 2 역주행: 멈춤 0 · 왼쪽 0.648 · 오른쪽 0.392 → 왼쪽, 점프 0.72 > 0.648 → 점프 (1000번이면 648 · 392 · 720번)", () => {
  // 10분의 몇으로 정확히: 9 · 9 · 8 / 1000 …
  const left = 9 * 9 * 8, right = 7 * 7 * 8, jump = 9 * 8 * 10;   // 1000 분의 몇
  assert.equal(left, 648); assert.equal(right, 392); assert.equal(jump, 720);
  near(WRONGWAY.p.left, 0.648); near(WRONGWAY.p.right, 0.392); near(WRONGWAY.p.jump, 0.72); assert.equal(WRONGWAY.p.stop, 0);
  assert.deepEqual(WRONGWAY.LEFT, [1000, 900, 810, 648]); assert.deepEqual(WRONGWAY.RIGHT, [1000, 700, 490, 392]); assert.deepEqual(WRONGWAY.JMP, [1000, 900, 720]);
  assert.equal(WRONGWAY.best2, "left"); assert.equal(WRONGWAY.best3, "jump");
  assert.ok(jump > left && left > right && right > 0);
  has(WRONGWAY.E.left, "1000 → 900 → 810 → ‹648›번"); has(WRONGWAY.E.right, "1000 → 700 → 490 → ‹392›번"); has(WRONGWAY.E.jump, "1000 → 900 → ‹720›번");
  has(WRONGWAY.E.change, "720 > 648");
  has(WRONGWAY.M.left, "0.9 × 0.9 × 0.8 = ‹0.648›"); has(WRONGWAY.M.right, "0.7 × 0.7 × 0.8 = ‹0.392›"); has(WRONGWAY.M.jump, "0.9 × 0.8 = ‹0.72› > 0.648");
  assert.deepEqual(WRONGWAY.M.vals.left, ["1", "0.9", "0.81", "0.648"]); assert.deepEqual(WRONGWAY.M.vals.right, ["1", "0.7", "0.49", "0.392"]); assert.deepEqual(WRONGWAY.M.vals.jump, ["1", "0.9", "0.72"]);
});

test("서술형 3 동아리: 64가지를 모두 늘어놓으면 셋 다 붙는 경우 24 → {3/8}, 서아의 선택마다 6칸 · 상의하면 1", () => {
  let all = 0, ok = 0;
  const per = [0, 0, 0, 0];
  for (let s = 0; s < 4; s++) for (let d = 0; d < 4; d++) for (let j = 0; j < 4; j++) {
    all++;
    const pick = [s, d, j];
    const admitted = pick.map((c, i) => pick.filter((x) => x === c).length === 1);   // 한 동아리에 둘 이상이면 아무도 못 붙음
    assert.deepEqual(CLUB.admitted(pick), admitted);
    if (admitted.every(Boolean)) { ok++; per[s]++; }
  }
  assert.equal(all, 64); assert.equal(ok, 24); assert.deepEqual(per, [6, 6, 6, 6]);
  assert.equal(CLUB.total, 64); assert.equal(CLUB.ok, 24); assert.equal(CLUB.perBlock, 6); eqQ(CLUB.p, [3, 8]);
  assert.equal(4 * 3 * 2, 24);
  assert.ok(!CLUB.admitted(CLUB.TRIES[0]).every(Boolean)); assert.ok(CLUB.admitted(CLUB.TRIES[1]).every(Boolean));
  assert.equal(CLUB.CELLS.length, 64); assert.equal(CLUB.CELLS.filter((c) => c.ok).length, 24);
  has(CLUB.E.sum, "6 + 6 + 6 + 6 = ‹24›"); has(CLUB.E.ans, "64번 중 24번 → ‹{3/8}›");
  has(CLUB.M.all, "4 × 4 × 4 = 64"); has(CLUB.M.ok, "4 × 3 × 2 = 24"); has(CLUB.M.ans, "{24/64} = ‹{3/8}›"); has(CLUB.M.trap, "4 + 4 + 4 = 12");
});

test("서술형 4 가위바위보: 27가지 중 모두 같음 3 · 모두 다름 6 → 비김 9 · 승부 18 → {2/3}, 1 − {3/27} = {8/9} 는 틀림", () => {
  let same = 0, diff = 0, dec = 0;
  for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) for (let c = 0; c < 3; c++) {
    const k = new Set([a, b, c]).size;
    if (k === 1) same++; else if (k === 3) diff++; else dec++;
  }
  assert.deepEqual([same, diff, dec], [3, 6, 18]);
  assert.equal(3 * (2 ** 3 - 2), 18);                      // 승부가 나는 18을 바로 세기: 나온 손 두 가지 고르기 × 셋이 그 둘만 쓰되 한쪽으로 몰리지 않기
  assert.equal(RPS.total, 27); assert.equal(RPS.same, 3); assert.equal(RPS.diff, 6); assert.equal(RPS.draw, 9); assert.equal(RPS.dec, 18);
  eqQ(RPS.p, [2, 3]); eqQ(RPS.wrong, [8, 9]); assert.notDeepEqual(Q(...RPS.wrong), Q(...RPS.p));
  const kinds = RPS.SHOW.map((h) => new Set(h).size);
  assert.deepEqual(kinds, [1, 3, 2]);                      // 예: 모두 같음(비김) · 모두 다름(비김) · 승부
  has(RPS.E.draw, "3 + 6 = 9 → 승부 27 − 9 = ‹18›"); has(RPS.E.ans, "27번 중 18번 = 3번 중 2번 → ‹{2/3}›"); has(RPS.E.trap, "24번?");
  has(RPS.M.all, "3 × 3 × 3 = 27"); has(RPS.M.draw, "3 + 3 × 2 × 1 = 9"); has(RPS.M.ans, "1 − {9/27} = ‹{2/3}›"); has(RPS.M.trap, "1 − {3/27} = {8/9}");
});

test("서술형 5 간판: y = 120x + 3000, 4800 이 되는 x = 15 → CP 60 · PB 40 cm (직사각형 6000 − 1200 으로도)", () => {
  for (const x of [0, 1, 5, 12.5, 15, 24]) near(SIGN.area(x), ((4 * x + 100) * 60) / 2);
  for (const x of [0, 7, 15]) near(SIGN.area(x), 120 * x + 3000);
  near(SIGN.area(0), (100 * 60) / 2);                     // 처음 삼각형 ACD
  const x = (4800 - 3000) / 120;
  assert.equal(x, 15); assert.equal(SIGN.x, 15); assert.ok(0 < x && x < 25 && SIGN.full === 25);
  assert.equal(SIGN.CP, 4 * 15); assert.equal(SIGN.PB, 100 - 60);
  assert.equal(6000 - (SIGN.PB * 60) / 2, 4800); assert.equal(SIGN.tri, 1200);  // 불 꺼진 삼각형 ABP
  assert.equal((1200 * 2) / 60, 40); assert.equal(60 / 4, 15);
  assert.deepEqual(SIGN.TABLE, [[0, 3000], [5, 3600], [10, 4200], [15, 4800]]);
  has(SIGN.E.dark, "6000 − 4800 = ‹1200 cm²›"); has(SIGN.E.pb1, "PB × 60 ÷ 2 = 1200"); has(SIGN.E.pb, "1200 × 2 ÷ 60 = ‹40 cm›");
  has(SIGN.E.time, "CP = 100 − 40 = 60 cm,  60 ÷ 4 = ‹15초›"); has(SIGN.E.rate, "4 × 60 ÷ 2 = 120 cm²");
  has(SIGN.M.y, "y = {1/2} × (4x + 100) × 60"); has(SIGN.M.y2, "‹120x + 3000›"); has(SIGN.M.solve, "x = 15");
  has(SIGN.M.cp2, "4 × 15 = 60"); has(SIGN.M.pb, "100 − 60 = ‹40 cm›"); has(SIGN.M.trap, "CP = 60 cm");
});

test("서술형 6 반티: A = 6000x + 24000, B = 8000x 의 교점 P(12, 96000) → A 가 싼 가장 적은 벌 수 13 (12 는 같은 값)", () => {
  const [px, py] = meetQ(Q(6000), Q(24000), Q(8000), Q(0));
  eqQ(px, [12, 1]); eqQ(py, [96000, 1]); assert.equal(SHIRT.x, 12); assert.equal(SHIRT.y, 96000);
  let k = 1; while (!(24000 + 6000 * k < 8000 * k)) k++;
  assert.equal(k, 13); assert.equal(SHIRT.ans, 13);
  assert.equal(SHIRT.A(12), SHIRT.B(12));                 // 함정: 12벌은 같은 값
  for (const [m, a, b] of SHIRT.ROWS) { assert.equal(a, 24000 + 6000 * m); assert.equal(b, 8000 * m); }
  assert.equal(24000 / (8000 - 6000), 12);
  for (const m of [0, 5, 12, 13, 14]) assert.equal(SHIRT.E.gap(m), SHIRT.A(m) - SHIRT.B(m));
  has(SHIRT.E.meet1, "24000 ÷ 2000 = 12"); has(SHIRT.E.meet, "12벌에서 둘 다 96000원"); has(SHIRT.E.ans, "‹13벌›"); has(SHIRT.E.trap, "12벌은 두 업체가 같아요");
  has(SHIRT.M.a, "y = 6000x + 24000"); has(SHIRT.M.b, "y = 8000x"); has(SHIRT.M.solve, "x = 12"); has(SHIRT.M.p, "P(12, 96000)"); has(SHIRT.M.ans, "‹13벌›");
});

test("분수 글자: 기약분수 · 정수", () => {
  assert.equal(tx(Q(6, 16)), "{3/8}"); assert.equal(tx(Q(18, 27)), "{2/3}"); assert.equal(tx(Q(8, 8)), "1");
});

/* ── 그리기 훑기 ── */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-stories-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PAIRS, GROUPS } from ${JSON.stringify(path.join(ROOT, "src/features/display/pairs.js"))};
import { PALETTE, SceneTitle } from ${JSON.stringify(path.join(ROOT, "src/features/display/draw.jsx"))};
export { PAIRS, GROUPS };
export const frame = (p, mode, t, th, opt) => renderToStaticMarkup(<g><SceneTitle title={p.title[mode]} sub={p.sub[mode]} C={PALETTE[th]} mode={mode} />{p.render(mode, t, PALETTE[th], opt)}</g>);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const mine = m.PAIRS.filter((p) => p.group === "soccer" || p.group === "essay");
  test("묶음: 축구 6 · 서술형 6, 키 soc-* · ess-*, 키 중복 없음, 제목 · 부제 두 판 모두 있음", () => {
    assert.ok(m.GROUPS.some((x) => x.key === "soccer" && x.label === "축구"));
    assert.ok(m.GROUPS.some((x) => x.key === "essay" && x.label === "서술형"));
    const soc = m.PAIRS.filter((p) => p.group === "soccer"), ess = m.PAIRS.filter((p) => p.group === "essay");
    assert.equal(soc.length, 6); assert.equal(ess.length, 6);
    assert.ok(soc.every((p) => p.key.startsWith("soc-"))); assert.ok(ess.every((p) => p.key.startsWith("ess-")));
    assert.equal(new Set(m.PAIRS.map((p) => p.key)).size, m.PAIRS.length);
    for (const p of mine) {
      assert.ok(p.title.e && p.title.m && p.sub.e && p.sub.m, p.key);
      assert.ok(p.dur > 15000 && p.dur < 60000, `${p.key} ${p.dur}`);
      assert.equal(typeof p.render, "function");
    }
  });
  for (const p of mine) {
    test(`그리기 훑기: ${p.key} (${(p.dur / 1000).toFixed(1)}초) — 두 판 · 두 테마, 오류 · NaN 없음`, () => {
      for (const mode of ["e", "m"]) for (const th of ["dark", "light"]) {
        for (let t = 0; t <= p.dur + 1000; t += th === "dark" ? 100 : 400) {
          const s = m.frame(p, mode, t, th, t % 800 === 0 ? { any: 1 } : undefined);   // 넷째 인자(장면 설정)가 와도 그대로
          assert.ok(!/NaN|undefined|Infinity|\[object Object\]/.test(s), `${mode}/${th} t=${t}: ${(s.match(/.{50}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0]}`);
        }
      }
    });
  }
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
