// node tests/display.test.mjs — 교실 모니터(#/admin/display) 장면 검산. 실패 시 exit 1.
//   1) 화면에 나오는 수를 facts.js · branch.js · guess.js 와 따로 다시 계산해 맞춰 본다(입체의 위치 관계는 좌표로 판정,
//      확률은 모든 경우를 늘어놓아 세고, 물리 판·갈톤 보드는 실제로 굴려 이론과 견준다).
//   2) 모든 장면 × 설정(기본값 + 설정마다 처음·끝 값) × 초등/중등 × 다크/라이트를 처음부터 끝까지 그려 보고 오류·NaN 이 없는지 본다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  BLOCKS, CIRCLE, LEAF, NETS, CYL, SPHERE, TRI3, POLY, DIAG, ISO, PARA, TRAP, interiorAngles, sameEdge, fmt,
  SORT, SEASON, DICE2, NUMCARDS, FREQ, CHANCE, fracTxt,
} from "../src/features/display/facts.js";
import { SOLIDS, foldAt, netEdgesOf, isHinge, lineRelation, linePlane } from "../src/features/display/solids.js";
import { GALTON, galtonLayout, galtonWorld, binOf, binom, comb, spawnSpan } from "../src/features/display/galton.js";
import { runTo, MARBLE } from "../src/features/display/physics.js";
import { FORK, FORKN, BUMP, shapeProbs, shapeOf, bumpRuns, shapeFreq, chuteLayout, chuteWalls } from "../src/features/display/branch.js";
import { MONTY, PICK5, LINKED, red } from "../src/features/display/guess.js";
import { paramCases, durOf, paramsOf } from "../src/features/display/params.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}
const near = (a, b, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${a} ≠ ${b}`);
const has = (s, frag) => assert.ok(String(s).includes(frag), `"${s}" 에 "${frag}" 없음`);
const choose = (a, b) => { let r = 1; for (let i = 1; i <= b; i++) r = (r * (a - b + i)) / i; return r; };

/* ── 1. 쌓기나무 ↔ 최단 경로 ── */
test("쌓기나무: 층별 11·5·1, 줄별 8·6·3, 모두 17개", () => {
  const all = BLOCKS.HT.flat();
  assert.deepEqual(BLOCKS.LAYERS, [11, 5, 1]);
  assert.equal(all.reduce((a, b) => a + b, 0), 17);
  assert.equal(BLOCKS.TOTAL, 17);
  assert.deepEqual([...BLOCKS.ROW_SUM].reverse(), [8, 6, 3]);
  for (let k = 1; k <= 3; k++) assert.equal(all.filter((h) => h >= k).length, BLOCKS.LAYERS[k - 1]);
});
test("최단 경로: B 까지 35가지 = 7C3, 교차점 수는 왼쪽 + 아래쪽", () => {
  const { PASCAL, COLS, ROWS } = BLOCKS;
  assert.equal(PASCAL[ROWS][COLS], choose(COLS + ROWS, ROWS));
  assert.equal(PASCAL[ROWS][COLS], 35);
  for (let y = 0; y <= ROWS; y++) for (let x = 0; x <= COLS; x++) assert.equal(PASCAL[y][x], choose(x + y, y));
});
test("최단 경로 예시 4개: 모두 → 4번·↑ 3번, 서로 다름", () => {
  assert.equal(new Set(BLOCKS.PATHS).size, BLOCKS.PATHS.length);
  for (const p of BLOCKS.PATHS) { assert.equal([...p].filter((c) => c === "R").length, 4); assert.equal([...p].filter((c) => c === "U").length, 3); }
});

/* ── 2. 원 ↔ 부채꼴 ── */
test("원: 원주 31.4 cm, 넓이 78.5 cm² (3.14)", () => {
  near(CIRCLE.circE, 31.4, 1e-9); near(CIRCLE.areaE, 78.5, 1e-9);
  has(CIRCLE.E_TXT.circLine, "31.4"); has(CIRCLE.E_TXT.areaLine, "78.5");
  near(CIRCLE.circE / 2, 15.7, 1e-9);               // 가로 = 원주의 1/2
});
test("부채꼴(r=5, 72°): l = 2π, 둘레 2π + 10, S = 5π = ½rl, 원주 10π", () => {
  const r = 5, a = 72;
  near(CIRCLE.arcK * Math.PI, (2 * Math.PI * r * a) / 360);
  near(CIRCLE.secK * Math.PI, (Math.PI * r * r * a) / 360);
  near(CIRCLE.halfRL * Math.PI, 0.5 * r * CIRCLE.arcK * Math.PI);
  assert.equal(CIRCLE.M_TXT.circ, "10π");
  has(CIRCLE.M_TXT.arcLine2, "2π"); has(CIRCLE.M_TXT.areaLine1, "5π"); has(CIRCLE.M_TXT.areaLine2, "5π");
  near(CIRCLE.arcK * Math.PI + 2 * r, 2 * Math.PI + 10);                 // 둘레 = 호 + 반지름 2개
  has(CIRCLE.M_TXT.perLine, "2π + 10"); assert.equal(CIRCLE.M_TXT.per, "2π + 10");
});

/* ── 3. 은행잎 ── */
test("은행잎(한 변 10): 넓이 57 / 50π − 100, 둘레 31.4 / 10π", () => {
  near(LEAF.quarterE, 78.5, 1e-9); near(LEAF.tri, 50); near(LEAF.halfE, 28.5, 1e-9);
  near(LEAF.areaE, 57, 1e-9); near(LEAF.arcE, 15.7, 1e-9); near(LEAF.perE, 31.4, 1e-9);
  const exact = 2 * (Math.PI * 100 / 4 - 50);       // 정확한 넓이
  near(exact, LEAF.qK * 2 * Math.PI - 100);
  assert.ok(Math.abs(exact - LEAF.areaE) < 0.1, "3.14 근삿값과 π 값이 크게 다름");
  near(2 * (2 * Math.PI * 10 / 4), LEAF.arcK * 2 * Math.PI);
  has(LEAF.E.areaLine2, "57"); has(LEAF.E.perLine, "31.4");
  has(LEAF.M.areaLine2, "50π − 100"); has(LEAF.M.perLine, "10π");
  // 몬테카를로 대신 격자 적분으로 은행잎 넓이 확인
  let cnt = 0; const N = 800;
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
    const x = ((i + 0.5) / N) * 10, y = ((j + 0.5) / N) * 10;
    if (x * x + y * y <= 100 && (x - 10) ** 2 + (y - 10) ** 2 <= 100) cnt++;
  }
  near((cnt / (N * N)) * 100, exact, 0.05);
});

/* ── 4. 전개도 ↔ 공간에서의 위치 관계 ── */
for (const id of ["cuboid", "cube", "prism"]) {
  const S = SOLIDS[id];
  test(`${S.name}: 전개도를 접으면 꼭짓점이 모두 맞물린다`, () => {
    const pos = foldAt(S, 0);
    const key = (p) => p.map((v) => Math.round(v * 1e6) / 1e6).join(",");
    const vset = new Set(Object.values(S.V).map(key));
    for (const f of S.faces) for (const p of pos[f.id]) assert.ok(vset.has(key(p)), `${f.id} 의 꼭짓점 ${key(p)} 이 입체 꼭짓점이 아님`);
    // 모든 모서리가 정확히 두 면에 걸린다
    const ec = new Map();
    for (const f of S.faces) { const q = pos[f.id]; for (let i = 0; i < q.length; i++) { const k = [key(q[i]), key(q[(i + 1) % q.length])].sort().join("|"); ec.set(k, (ec.get(k) || 0) + 1); } }
    assert.equal(ec.size, S.edges.length);
    for (const v of ec.values()) assert.equal(v, 2);
    const c = NETS[id].count;
    assert.equal(Object.keys(S.V).length, c.V); assert.equal(S.edges.length, c.E); assert.equal(S.faces.length, c.F);
    assert.equal(c.V - c.E + c.F, 2);
  });
  test(`${S.name}: 펼친 전개도는 바닥 위 한 평면, 면끼리 겹치지 않음`, () => {
    const pos = foldAt(S, 1);
    for (const f of S.faces) for (const p of pos[f.id]) near(p[2], 0, 1e-9);
    const area = (q) => Math.abs(q.reduce((a, p, i) => a + p[0] * q[(i + 1) % q.length][1] - q[(i + 1) % q.length][0] * p[1], 0)) / 2;
    const xs = S.faces.flatMap((f) => pos[f.id].map((p) => p[0])), ys = S.faces.flatMap((f) => pos[f.id].map((p) => p[1]));
    let inside = 0; const N = 300, x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    const pip = (pt, q) => { let c = false; for (let i = 0, j = q.length - 1; i < q.length; j = i++) { if (((q[i][1] > pt[1]) !== (q[j][1] > pt[1])) && pt[0] < ((q[j][0] - q[i][0]) * (pt[1] - q[i][1])) / (q[j][1] - q[i][1]) + q[i][0]) c = !c; } return c; };
    let over = 0;
    for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
      const pt = [x0 + ((i + 0.5) / N) * (x1 - x0), y0 + ((j + 0.5) / N) * (y1 - y0)];
      const k = S.faces.filter((f) => pip(pt, pos[f.id])).length;
      if (k > 0) inside++; if (k > 1) over++;
    }
    assert.equal(over, 0, "전개도 면이 겹침");
    const sum = S.faces.reduce((a, f) => a + area(pos[f.id]), 0);
    near((inside / (N * N)) * (x1 - x0) * (y1 - y0), sum, sum * 0.02);
  });
  test(`${S.name}: 같은 색으로 보여 주는 모서리는 전개도의 두 곳(자른 모서리)`, () => {
    const names = [...NETS[id].pairsE, "AB"];
    for (const nm of names) {
      const hits = netEdgesOf(S, S.V[nm[0]], S.V[nm[1]]);
      assert.equal(hits.length, 2, `${nm}: ${hits.length}곳`);
      assert.equal(isHinge(S, S.V[nm[0]], S.V[nm[1]]), false, `${nm} 이 접는 선`);
    }
  });
}
for (const id of ["cuboid", "prism"]) {
  test(`${SOLIDS[id].name}: 모서리 AB 와의 위치 관계(만남·평행·꼬인 위치)`, () => {
    const S = SOLIDS[id], V = S.V, A = V.A, Bp = V.B;
    const want = { meet: [], parallel: [], skew: [] };
    for (const e of S.edges) {
      if (sameEdge(e, "AB")) continue;
      const r = lineRelation(A, Bp, V[e[0]], V[e[1]]);
      want[r].push(e);
    }
    for (const g of NETS[id].relM) {
      const got = [...g.list].map((x) => [...x].sort().join("")).sort();
      const exp = want[g.cat].map((x) => [...x].sort().join("")).sort();
      assert.deepEqual(got, exp, `${g.cat}`);
    }
    assert.equal(NETS[id].relM.reduce((a, g) => a + g.list.length, 0), S.edges.length - 1);
  });
}
test("정육면체: 직선 AB 와 면(포함 2 · 평행 2 · 수직 2)", () => {
  const S = SOLIDS.cube, V = S.V;
  const got = { contain: [], parallel: [], perp: [], meet: [] };
  for (const name of Object.values(NETS.cube.faceName)) got[linePlane(V.A, V.B, V[name[0]], V[name[1]], V[name[2]])].push(name);
  for (const g of NETS.cube.planesM) assert.deepEqual([...g.list].sort(), got[g.cat].sort(), g.cat);
  assert.equal(got.meet.length, 0);
});
test("직육면체·정육면체·삼각기둥 판서 글자와 개수", () => {
  has(NETS.cuboid.E.board[1].s, "6개"); has(NETS.cuboid.E.board[2].s, "12개"); has(NETS.cuboid.E.board[3].s, "8개");
  has(NETS.prism.E.board[2].s, "9개"); has(NETS.prism.E.board[3].s, "6개");
  assert.equal(NETS.cube.nets, 11);
});

/* ── 5. 원기둥 ── */
test("원기둥(r=3, h=8): 3.14 판", () => {
  near(CYL.sideE, 18.84, 1e-9); near(CYL.sideAreaE, 150.72, 1e-9); near(CYL.sidePerE, 53.68, 1e-9);
  near(CYL.baseE, 28.26, 1e-9); near(CYL.netE, 207.24, 1e-9);
  const b = CYL.E.board.map((L) => L.s).join(" | ");
  for (const v of ["18.84", "150.72", "53.68", "207.24"]) has(b, v);
});
test("원기둥(r=3, h=8): π 판 — 6π · 48π · 12π + 16 · 66π · 72π", () => {
  const r = 3, h = 8;
  near(CYL.sideK * Math.PI, 2 * Math.PI * r); near(CYL.sideAreaK * Math.PI, 2 * Math.PI * r * h);
  near(CYL.surfK * Math.PI, 2 * Math.PI * r * r + 2 * Math.PI * r * h); near(CYL.volK * Math.PI, Math.PI * r * r * h);
  const b = CYL.M.board.map((L) => L.s).join(" | ");
  for (const v of ["6π", "48π", "12π + 16", "66π", "72π"]) has(b, v);
  assert.equal(CYL.M.vol, "72π");
});

/* ── 6. 구 ── */
test("구(r=6): S = 144π, 원기둥 432π, V = 288π = 4/3πr³", () => {
  const r = 6;
  near(SPHERE.areaK * Math.PI, 4 * Math.PI * r * r);
  near(SPHERE.cylK * Math.PI, Math.PI * r * r * 2 * r);
  near(SPHERE.volK * Math.PI, (4 / 3) * Math.PI * r ** 3, 1e-6);
  near(SPHERE.volK, SPHERE.volK2, 1e-9);
  has(SPHERE.M.area, "144π"); has(SPHERE.M.cylV, "432π"); has(SPHERE.M.vol, "288π"); has(SPHERE.E.dia, "12");
});

/* ── 7. 삼각형의 세 각 ── */
test("삼각형: 50 + 70 + 60 = 180, x = 20, 외각 120", () => {
  assert.equal(TRI3.A + TRI3.B + TRI3.Cc, 180);
  const x = TRI3.x;
  assert.equal(2 * x + 10, TRI3.A); assert.equal(3 * x + 10, TRI3.B);
  assert.equal((2 * x + 10) + (3 * x + 10) + TRI3.Cc, 180);
  assert.equal(TRI3.ext, 180 - TRI3.Cc);
  has(TRI3.E.board[2].s, "60°"); has(TRI3.E.board[4].s, "120°"); has(TRI3.M.board[2].s, "x* = 20"); has(TRI3.M.board[4].s, "120°");
});

/* ── 8. 다각형의 각의 합 ── */
test("사각형·오각형: 그림의 내각이 표시한 각과 같다(볼록)", () => {
  const qa = interiorAngles(POLY.quad), pa = interiorAngles(POLY.pent);
  POLY.qa.forEach((v, i) => near(qa[i], v, 1e-6));
  POLY.pa.forEach((v, i) => near(pa[i], v, 1e-6));
  for (const poly of [POLY.quad, POLY.pent]) {
    const k = poly.length;
    for (let i = 0; i < k; i++) {
      const a = poly[i], b = poly[(i + 1) % k], c = poly[(i + 2) % k];
      assert.ok((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) > 0, "볼록이 아님");
    }
  }
});
test("다각형: 360 − 285 = 75, 540 − 420 = 120, x = 75 · x = 50", () => {
  assert.equal(POLY.qa.reduce((a, b) => a + b, 0), 360);
  assert.equal(POLY.pa.reduce((a, b) => a + b, 0), 540);
  assert.equal(360 - POLY.qKnown, POLY.qa[3]); assert.equal(540 - POLY.pKnown, POLY.pa[4]);
  assert.equal(POLY.px + 45, POLY.pa[3]); assert.equal(2 * POLY.px + 20, POLY.pa[4]);
  for (let k = 3; k <= 8; k++) assert.equal(180 * (k - 2), [180, 360, 540, 720, 900, 1080][k - 3]);
  has(POLY.E.board[2].s, "75°"); has(POLY.E.board[5].s, "120°"); has(POLY.M.board[6].s, "x* = 50");
});

/* ── 9. 대각선 ── */
test("대각선: 육각형 9, 팔각형 20, 20개인 다각형은 팔각형", () => {
  const brute = (k) => { let c = 0; for (let i = 0; i < k; i++) for (let j = i + 1; j < k; j++) if (j - i !== 1 && !(i === 0 && j === k - 1)) c++; return c; };
  assert.equal(DIAG.count(6), brute(6)); assert.equal(DIAG.count(8), brute(8));
  assert.equal(DIAG.count(6), 9); assert.equal(DIAG.count(8), 20);
  assert.equal(DIAG.seq(6).reduce((a, b) => a + b, 0), 9); assert.equal(DIAG.seq(8).reduce((a, b) => a + b, 0), 20);
  assert.equal(DIAG.nFor, 8);
  has(DIAG.E.board[3].s, "3 + 3 + 2 + 1"); has(DIAG.E.board[5].s, "5 + 5 + 4 + 3 + 2 + 1");
});

/* ── 10. 이등변삼각형 ── */
test("이등변삼각형: 꼭지각 40 → 밑각 70, x = 30", () => {
  assert.equal(ISO.apex + 2 * ISO.base, 180);
  assert.equal(ISO.x + 10, ISO.apex); assert.equal(2 * ISO.x + 10, ISO.base);
  has(ISO.E.board[5].s, "70°"); has(ISO.M.board[4].s, "x* = 30");
});

/* ── 11. 평행사변형 ── */
test("평행사변형: 65·115, x = 20, y = 4", () => {
  assert.equal(PARA.angA + PARA.angB, 180);
  assert.equal(3 * PARA.x + 5, PARA.angB); assert.equal(2 * PARA.x + 25, PARA.angB);
  assert.equal(2 * PARA.y + 1, PARA.BC);
  has(PARA.E.board[3].s, "115°"); has(PARA.M.board[1].s, "x* = 20"); has(PARA.M.board[3].s, "y* = 4");
});

/* ── 12. 사다리꼴·마름모 ── */
test("사다리꼴 42 · 마름모 24, x = 5 · x = 8", () => {
  assert.equal(TRAP.area, 42); assert.equal(TRAP.rArea, 24);
  assert.equal(TRAP.tx, TRAP.top); assert.equal(TRAP.tx + 4, TRAP.bot);
  assert.equal(0.5 * (TRAP.tx + TRAP.tx + 4) * TRAP.h, TRAP.area);
  assert.equal(TRAP.rx, TRAP.d1); assert.equal(0.5 * TRAP.rx * TRAP.d2, TRAP.rArea);
  // 반 바퀴 돌린 사다리꼴 두 개 = 밑변 (윗변 + 아랫변) 평행사변형
  assert.equal((TRAP.top + TRAP.bot) * TRAP.h / 2, TRAP.area);
  has(TRAP.M.board[2].s, "x* = 5"); has(TRAP.M.board[5].s, "x* = 8");
});

/* ══════════ 자료와 가능성 ↔ 경우의 수와 확률 ══════════ */
test("분류: 카드 12장 — 모양 5·4·3, 색 4·5·3, 빨간 동그라미 2", () => {
  const C = SORT.CARDS;
  assert.equal(C.length, 12);
  assert.equal(new Set(C.map((c) => c.shape + c.color)).size <= 9, true);
  assert.deepEqual(SORT.byShape, [5, 4, 3]); assert.deepEqual(SORT.byColor, [4, 5, 3]);
  assert.equal(SORT.byShape.reduce((a, b) => a + b, 0), 12); assert.equal(SORT.byColor.reduce((a, b) => a + b, 0), 12);
  assert.equal(SORT.circleRed, 2); assert.equal(SORT.mostColor, "b");
  has(SORT.E.shapeLine, "5장"); has(SORT.E.colorLine, "파랑 5"); has(SORT.E.most, "파란 카드");
});
test("합의 법칙: 동그라미 또는 세모 9, 파랑 또는 노랑 8, 동그라미 또는 빨강 7(겹침 빼기)", () => {
  const C = SORT.CARDS;
  assert.equal(C.filter((c) => c.shape === "circle" || c.shape === "tri").length, SORT.orCT);
  assert.equal(C.filter((c) => c.color === "b" || c.color === "y").length, SORT.orBY);
  assert.equal(C.filter((c) => c.shape === "circle" || c.color === "r").length, SORT.orCR);
  assert.deepEqual([SORT.orCT, SORT.orBY, SORT.orCR], [9, 8, 7]);
  // 앞의 두 경우는 정말로 동시에 일어나지 않는다(겹치는 카드 0장)
  assert.equal(C.filter((c) => c.shape === "circle" && c.shape === "tri").length, 0);
  assert.equal(C.filter((c) => c.color === "b" && c.color === "y").length, 0);
  has(SORT.M.ct, "5 + 4 = ‹9›"); has(SORT.M.by, "5 + 3 = ‹8›"); has(SORT.M.cr, "5 + 4 − 2 = ‹7›"); has(SORT.M.all, "12");
});
test("표: 계절 쪽지 16장 — 봄 5·여름 4·가을 3·겨울 4, 가장 많은 계절 봄", () => {
  assert.deepEqual(SEASON.COUNTS, [5, 4, 3, 4]); assert.equal(SEASON.TOTAL, 16);
  assert.equal(SEASON.COUNTS.reduce((a, b) => a + b, 0), SEASON.NOTES.length);
  assert.equal(SEASON.most, "봄");
  assert.equal(SEASON.COUNTS.filter((c) => c === Math.max(...SEASON.COUNTS)).length, 1);   // 가장 많은 것이 하나
  has(SEASON.sumLine, "5 + 4 + 3 + 4 = ‹16›");
});
test("두 주사위: 6 × 6 = 36, 합별 1~6~1, 합 7 확률 1/6", () => {
  assert.equal(DICE2.TOTAL, 36);
  assert.deepEqual(DICE2.BY_SUM, [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]);
  assert.equal(DICE2.BY_SUM.reduce((a, b) => a + b, 0), 36);
  assert.equal(DICE2.best, 7); assert.equal(DICE2.n7, 6);
  let n7 = 0; for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) if (a + b === 7) n7++;
  assert.equal(n7, 6); near(n7 / 36, 1 / 6);
  has(DICE2.p7Line, "{6/36}"); has(DICE2.p7Line, "{1/6}"); has(DICE2.mulLine, "36");
});
test("수 카드 0·1·2·3: 두 자리 9개(3 × 3), 세 자리 18개(3 × 3 × 2), 가장 큰 수 32·작은 수 10", () => {
  // 따로 세기: 서로 다른 두 장, 십의 자리 0 아님
  const two = new Set();
  for (const a of [0, 1, 2, 3]) for (const b of [0, 1, 2, 3]) if (a !== b && a !== 0) two.add(10 * a + b);
  assert.equal(two.size, 9); assert.deepEqual([...two].sort((x, y) => x - y), NUMCARDS.TWO);
  assert.equal(NUMCARDS.tens * NUMCARDS.ones, 9);
  const three = new Set();
  for (const a of [0, 1, 2, 3]) for (const b of [0, 1, 2, 3]) for (const c of [0, 1, 2, 3])
    if (a && a !== b && b !== c && a !== c) three.add(100 * a + 10 * b + c);
  assert.equal(three.size, 18); assert.equal(NUMCARDS.THREE.length, 18);
  assert.equal(NUMCARDS.tens * NUMCARDS.ones * (NUMCARDS.ones - 1), 18);
  assert.equal(NUMCARDS.max, 32); assert.equal(NUMCARDS.min, 10);
  assert.deepEqual(NUMCARDS.ROWS.map((r) => r.length), [3, 3, 3]);
  // 지우는 칸: 십의 자리 0(4칸) + 같은 카드(1·2·3 의 3칸) = 7칸, 남는 칸 9
  const g = NUMCARDS.GRID.flat();
  assert.equal(g.filter((c) => c.zero).length, 4); assert.equal(g.filter((c) => c.same && !c.zero).length, 3);
  assert.equal(g.filter((c) => c.ok).length, 9);
  has(NUMCARDS.M.two, "3 × 3 = ‹9›"); has(NUMCARDS.M.three, "3 × 3 × 2 = ‹18›"); has(NUMCARDS.E.count, "3 + 3 + 3 = ‹9›");
});
test("주사위 기록: 30번·60번 — 가장 많이/적게 나온 눈이 하나씩, 6000번 상대도수는 1/6 가까이", () => {
  assert.equal(FREQ.ROLLS.length, 6000);
  assert.ok(FREQ.ROLLS.every((v) => v >= 1 && v <= 6));
  const cnt = (n) => [1, 2, 3, 4, 5, 6].map((f) => FREQ.ROLLS.slice(0, n).filter((x) => x === f).length);
  assert.deepEqual(cnt(30), FREQ.c30); assert.deepEqual(cnt(60), FREQ.c60); assert.deepEqual(cnt(6000), FREQ.c6000);
  for (const c of [FREQ.c30, FREQ.c60]) {
    assert.equal(c.filter((v) => v === Math.max(...c)).length, 1, "가장 많이 나온 눈이 둘 이상");
    assert.equal(c.filter((v) => v === Math.min(...c)).length, 1, "가장 적게 나온 눈이 둘 이상");
  }
  assert.equal(FREQ.c30[FREQ.max30 - 1], Math.max(...FREQ.c30)); assert.equal(FREQ.c60[FREQ.max60 - 1], Math.max(...FREQ.c60));
  assert.equal(FREQ.c60[FREQ.min60 - 1], Math.min(...FREQ.c60));
  assert.ok(Math.max(...FREQ.c30) <= 10, "30번 그래프 눈금(10) 넘침"); assert.ok(Math.max(...FREQ.c60) <= 20, "60번 그래프 눈금(20) 넘침");
  for (const c of FREQ.c6000) assert.ok(Math.abs(c / 6000 - 1 / 6) < 0.01, `6000번 상대도수 ${c / 6000}`);
  assert.equal(FREQ.lo, 0.16); assert.equal(FREQ.hi, 0.17);
  has(FREQ.E.max30, `⟪d${FREQ.max30}⟫ ‹${Math.max(...FREQ.c30)}›번`); has(FREQ.M.ex30, `{${Math.max(...FREQ.c30)}/30}`);
  near(Number(FREQ.M.ex30.split("≈ ")[1]), Math.round((Math.max(...FREQ.c30) / 30) * 100) / 100);
});
test("가능성 ↔ 확률: 0 · 1/4 · 1/2 · 3/4 · 1, 일어나지 않을 확률 1 − 3/4 = 1/4", () => {
  assert.deepEqual(CHANCE.P, ["0", "{1/4}", "{1/2}", "{3/4}", "1"]);
  assert.deepEqual(CHANCE.WORDS, ["불가능하다", "~아닐 것 같다", "반반이다", "~일 것 같다", "확실하다"]);
  assert.equal(CHANCE.REDS.length, CHANCE.WORDS.length);
  CHANCE.REDS.forEach((r) => assert.ok(r / CHANCE.TOTAL >= 0 && r / CHANCE.TOTAL <= 1));
  near(1 - CHANCE.comp / CHANCE.TOTAL, 1 / 4);
  has(CHANCE.compLine, "1 − {3/4} = ‹{1/4}›");
  assert.equal(fracTxt(6, 36), "{1/6}"); assert.equal(fracTxt(4, 4), "1"); assert.equal(fracTxt(0, 4), "0"); assert.equal(fracTxt(2, 4), "{1/2}");
});

/* ── 18. 갈림길 — 두 갈래 길 2번 · 구슬 4개 ── */
test("두 갈래 길: 길 4가지(A·B·C 로 1·2·1), 확률 1/4·1/2·1/4", () => {
  assert.equal(FORK.PATHS.length, 4);
  assert.deepEqual(FORK.WAYS, [1, 2, 1]);
  assert.deepEqual(FORK.P, [[1, 4], [1, 2], [1, 4]]);
  // 구슬 4개는 B·A·C·B — 세 구멍에 모두
  assert.deepEqual(FORK.SEQ.map((k) => "ABC"[FORK.holeOf2(FORK.PATHS[k])]).join(""), "BACB");
});
test("구슬 4개가 A·B·C 에 모두: 모양 AABC·ABBC·ABCC (순서 12가지씩) = 3/32 + 3/16 + 3/32 = 3/8 — 4⁴ = 256가지를 모두 세어 96가지", () => {
  // 길 4가지가 같은 확률 → 구슬 4개의 길 조합 256가지를 모두 늘어놓는다
  let all = 0;
  const byWord = new Map();
  for (let c = 0; c < 256; c++) {
    const holes = [0, 1, 2, 3].map((q) => FORK.holeOf2(FORK.PATHS[(c >> (2 * q)) & 3]));
    const cnt = [0, 1, 2].map((h) => holes.filter((x) => x === h).length);
    if (cnt.every((v) => v > 0)) {
      all++;
      const w = "ABC".split("").map((h, k) => h.repeat(cnt[k])).join("");
      byWord.set(w, (byWord.get(w) || 0) + 1);
    }
  }
  assert.equal(all, 96); assert.equal(FORK.ALL, 96); assert.deepEqual(FORK.PALL, [3, 8]);
  for (const sh of FORK.SHAPES) {
    assert.equal(sh.ord, 12, sh.word);
    assert.equal(byWord.get(sh.word), sh.num, sh.word);
    assert.deepEqual(sh.p, red(sh.num, 256));
  }
  assert.deepEqual(FORK.SHAPES.map((o) => o.p), [[3, 32], [3, 16], [3, 32]]);
  // 확률의 곱으로도: 12 × (1/4)(1/4)(1/2)(1/4) = 3/32 …
  near(12 * (1 / 4) ** 3 * (1 / 2), 3 / 32); near(12 * (1 / 4) ** 2 * (1 / 2) ** 2, 3 / 16);
});
test("초등 40개 기록: 모두 40개, B 가 가장 많고 절반쯤(18~22), A·C 는 10개 안팎", () => {
  assert.equal(FORK.E40.length, 40);
  const [a, b, c] = FORK.E40C;
  assert.equal(a + b + c, 40); assert.ok(b > a && b > c);
  assert.ok(b >= 18 && b <= 22, `B ${b}`); assert.ok(a >= 7 && a <= 13 && c >= 7 && c <= 13, `A ${a} C ${c}`);
});
test("갈림길이 늘어나면(단계 2~6): 구멍 k 로 가는 길 C(n, k), 확률의 합 1, 256개 기록은 종 모양·기대 개수는 정수", () => {
  for (const n of FORKN.NS) {
    const F = FORKN.of(n);
    assert.deepEqual(F.ways, Array.from({ length: n + 1 }, (_, k) => choose(n, k)));
    // 파스칼: 위의 두 수의 합
    for (let k = 1; k < n; k++) assert.equal(F.ways[k], choose(n - 1, k - 1) + choose(n - 1, k));
    near(F.P.reduce((s, p) => s + p[0] / p[1], 0), 1);
    assert.equal(F.counts.reduce((a, b) => a + b, 0), FORKN.ROLLN);
    assert.ok(FORKN.bell(F.counts), `n=${n} ${F.counts}`);
    for (const e of F.expect) assert.ok(Number.isInteger(e), `기대 개수 ${e}`);
    F.rolls.forEach((w) => assert.equal(w.length, n));
  }
});
test("모양별 확률(shapeProbs): 단계 1~3 · 구슬 2~4 — 모든 길 조합을 세어 맞춰 보기, 합 1", () => {
  for (const n of BUMP.NS) for (const m of BUMP.MS) {
    const sp = shapeProbs(n, m);
    near(sp.reduce((a, o) => a + o.p, 0), 1);
    // 길 2ⁿ 가지를 구슬 m 개가 고른다: (2ⁿ)^m 가지
    const P = 2 ** n, cnt = new Map();
    for (let c = 0; c < P ** m; c++) {
      const holes = new Array(n + 1).fill(0);
      let x = c;
      for (let q = 0; q < m; q++) { const path = x % P; x = Math.floor(x / P); let h = 0; for (let b = 0; b < n; b++) h += (path >> b) & 1; holes[h]++; }
      const key = shapeOf(holes); cnt.set(key, (cnt.get(key) || 0) + 1);
    }
    for (const o of sp) assert.equal(cnt.get(o.key), o.num, `${n}/${m} ${o.key}`);
    assert.equal(sp.length, cnt.size);
  }
});
test("물리 판(하나씩·동시에): 잃어버린 구슬 없음 · 하나씩은 이론과 비슷 · 동시에 나란히 떨어지면 첫 갈림목에서 갈린다", () => {
  const T = BUMP.TRIALS;
  for (const [n, m] of [[1, 2], [2, 2], [3, 2], [2, 4]]) {
    for (const md of ["seq", "sim"]) {
      const R = bumpRuns(n, m, md, T);
      assert.equal(R.reduce((a, o) => a + o.lost, 0), 0, `${n}/${m}/${md} 잃어버린 구슬`);
      assert.ok(R.every((o) => o.counts.reduce((a, b) => a + b, 0) === m));
    }
    const th = shapeProbs(n, m), fs = shapeFreq(bumpRuns(n, m, "seq", T), T);
    for (const o of th) assert.ok(Math.abs(fs(o.key) - o.p) < 0.09, `하나씩 ${n}/${m} ${o.key}: ${fs(o.key)} vs ${o.p}`);
  }
  // 단계 1 · 구슬 2개를 동시에: 늘 다른 구멍(서로 밀어낸다)
  assert.equal(shapeFreq(bumpRuns(1, 2, "sim", T), T)("2-0"), 0);
  // 단계 2 · 구슬 2개: 같은 구멍이 이론(3/8)보다 확 줄어든다
  const same = shapeFreq(bumpRuns(2, 2, "sim", T), T)("2-0-0");
  assert.ok(same < 3 / 8 - 0.08, `동시에 같은 구멍 ${same}`);
});
test("물리 판 벽: 갈림목 지붕 · 칸막이 기둥 · 목 · 상자 — 좌우 대칭", () => {
  for (const n of BUMP.NS) {
    const L = chuteLayout({ n, m: 2, cx: 0, ...BUMP.GEO });
    const W = chuteWalls(L);
    assert.equal(W.filter((w) => w.kind === "roof").length, (n * (n - 1)) / 2);
    assert.equal(W.filter((w) => w.kind === "post").length, n);
    const key = (w) => w.pts.map(([x, y]) => `${Math.round(x * 10)},${Math.round(y * 10)}`).sort().join(" ");
    const mirror = (w) => ({ pts: w.pts.map(([x, y]) => [-x, y]) });
    const all = new Set(W.map(key));
    for (const w of W) assert.ok(all.has(key(mirror(w))), `대칭이 아닌 벽 ${key(w)}`);
  }
});

/* ── 19. 갈톤 보드(물리) ── */
test("갈톤 보드: 못 8줄 · 구슬 500개 — 칸별 개수가 B(8, 1/2) 에 가깝다(분포 거리 < 0.1, 표준편차 비 0.8~1.25), 쌓인 더미가 칸 안", () => {
  const L = galtonLayout({ R: 8, N: 500, cx: 560 });
  const W = galtonWorld(L, 11);
  runTo(W, 0.5 + spawnSpan(500) + 6);
  const cnt = new Array(9).fill(0);
  let landed = 0, top = Infinity;
  for (let i = 0; i < W.n; i++) {
    if (W.st[i] !== MARBLE.FROZEN) continue;
    const k = binOf(L, W.x[i], W.y[i]);
    if (k >= 0) { cnt[k]++; landed++; top = Math.min(top, W.y[i] - W.r[i]); }
  }
  assert.ok(landed >= 495, `칸에 든 구슬 ${landed}`);
  const p = cnt.map((c) => c / landed);
  const tvd = 0.5 * p.reduce((a, v, k) => a + Math.abs(v - binom(8, k)), 0);
  const mean = p.reduce((a, v, k) => a + v * k, 0), sd = Math.sqrt(p.reduce((a, v, k) => a + v * (k - mean) ** 2, 0));
  assert.ok(tvd < 0.1, `분포 거리 ${tvd}`);
  assert.ok(sd / Math.sqrt(2) > 0.8 && sd / Math.sqrt(2) < 1.25, `표준편차 비 ${sd / Math.sqrt(2)}`);
  assert.ok(top > L.yDiv - 4, `더미 꼭대기 ${top} < 칸막이 시작 ${L.yDiv}`);
  near(Array.from({ length: 9 }, (_, k) => binom(8, k)).reduce((a, b) => a + b, 0), 1);
  assert.equal(comb(10, 5), 252);
  assert.ok(GALTON.NS.includes(GALTON.NDEF) && GALTON.ROWS.includes(GALTON.RDEF));
});

/* ── 20. 몬티홀 · 찍기 ── */
test("몬티홀(문 3·4·5): 모든 경우를 확률로 따져 그대로 1/n · 하나 열고 바꾸기 (n−1)/(n(n−2)) · 하나만 남기고 바꾸기 (n−1)/n", () => {
  for (const n of MONTY.NS) {
    let stay = 0, sw1 = 0, swAll = 0;
    for (let car = 0; car < n; car++) {
      const pc = 1 / n;
      if (car === 0) stay += pc;
      const goats = []; for (let d = 1; d < n; d++) if (d !== car) goats.push(d);
      for (const open of goats) {
        const closed = []; for (let d = 1; d < n; d++) if (d !== open) closed.push(d);
        for (const sw of closed) if (sw === car) sw1 += pc / goats.length / closed.length;
      }
      if (car !== 0) swAll += pc;                    // 하나만 남기면 그 문이 자동차
    }
    const P = MONTY.probs(n);
    near(P.stay[0] / P.stay[1], stay); near(P.sw1[0] / P.sw1[1], sw1); near(P.swAll[0] / P.swAll[1], swAll);
    assert.ok(stay < sw1 && sw1 <= swAll);
    // 300판 기록: 이론에서 표준편차 3배 안, 그대로 < 바꾸기
    const G = MONTY.GAMES;
    for (const [key, p] of [["stay", stay], ["sw1", sw1], ["swAll", swAll]]) {
      const f = MONTY.wins(n, G, key) / G;
      assert.ok(Math.abs(f - p) < 3 * Math.sqrt((p * (1 - p)) / G), `${n} ${key} ${f} vs ${p}`);
    }
    assert.ok(MONTY.wins(n, G, "stay") < MONTY.wins(n, G, "sw1"));
    MONTY.games(n).forEach((g) => { assert.ok(g.open !== g.car && g.open !== 0); assert.ok(g.sw !== 0 && g.sw !== g.open); });
  }
  assert.deepEqual(MONTY.probs(4).sw1, [3, 8]); assert.deepEqual(MONTY.probs(5).sw1, [4, 15]); assert.deepEqual(MONTY.probs(5).swAll, [4, 5]);
});
test("5지선다: 남은 보기 5·4·3·2 → 1/5·1/4·1/3·1/2, 5문제 맞힌 수의 분포 합 1 · 평균 5/k, 200명 기록의 평균이 가깝고 차례대로 크다", () => {
  assert.deepEqual(PICK5.P, [[1, 5], [1, 4], [1, 3], [1, 2]]);
  for (const k of PICK5.STRATS) {
    const d = PICK5.dist(k);
    near(d.reduce((a, b) => a + b, 0), 1);
    near(d.reduce((a, v, j) => a + v * j, 0), PICK5.mean(k));
  }
  PICK5.sims.forEach((s) => {
    assert.equal(s.hist.reduce((a, b) => a + b, 0), PICK5.STUDENTS);
    assert.ok(Math.abs(s.avg - PICK5.mean(s.k)) < 0.25, `${s.k} 평균 ${s.avg}`);
  });
  assert.ok(PICK5.sims[0].avg < PICK5.sims[1].avg && PICK5.sims[1].avg < PICK5.sims[2].avg);
});
test("맞물린 답: 참인 짝(반반) × 내가 고른 짝 — 따로 1/4·1/2·1/4, 맞물려 1/2·0·1/2, 평균 둘 다 1 · 70% 확신이면 1.2 vs 1.4", () => {
  const truths = [[0, 0], [1, 1]];                   // 맞물린 짝만 참일 수 있다
  const dist = (guesses, pTruth) => {
    const d = [0, 0, 0];
    truths.forEach((tr, ti) => guesses.forEach(([g, pg]) => { d[(g[0] === tr[0]) + (g[1] === tr[1])] += pTruth[ti] * pg; }));
    return d;
  };
  const all4 = [[[0, 0], 1 / 4], [[0, 1], 1 / 4], [[1, 0], 1 / 4], [[1, 1], 1 / 4]];
  const link2 = [[[0, 0], 1 / 2], [[1, 1], 1 / 2]];
  const i0 = dist(all4, [0.5, 0.5]), l0 = dist(link2, [0.5, 0.5]);
  LINKED.indep.forEach((p, j) => near(p[0] / p[1], i0[j]));
  LINKED.linked.forEach((p, j) => near(p[0] / p[1], l0[j]));
  near(LINKED.mean(LINKED.indep), 1); near(LINKED.mean(LINKED.linked), 1);
  // 70% 확신: 따로 = 3번은 ②, 7번은 반반 · 맞물려 = (②, ①)
  const i7 = dist([[[0, 0], 0.5], [[0, 1], 0.5]], [0.7, 0.3]), l7 = dist([[[0, 0], 1]], [0.7, 0.3]);
  LINKED.pIndep.forEach((p, j) => near(p, i7[j])); LINKED.pLinked.forEach((p, j) => near(p, l7[j]));
  near(LINKED.meanP(LINKED.pIndep), 1.2); near(LINKED.meanP(LINKED.pLinked), 1.4);
  // 어긋난 짝은 늘 딱 한 문제
  for (const g of [[0, 1], [1, 0]]) for (const tr of truths) assert.equal((g[0] === tr[0]) + (g[1] === tr[1]), 1);
  assert.deepEqual(LINKED.three.indepBoth, [1, 9]); assert.deepEqual(LINKED.three.linkedBoth, [1, 3]);
});

test("fmt: 소수 둘째 자리·끝 0 지우기", () => {
  assert.equal(fmt(31.400000000000002), "31.4"); assert.equal(fmt(207.24), "207.24"); assert.equal(fmt(57), "57");
});

/* ── 그리기 훑기 ── */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-test-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PAIRS } from ${JSON.stringify(path.join(ROOT, "src/features/display/pairs.js"))};
import { PALETTE, SceneTitle } from ${JSON.stringify(path.join(ROOT, "src/features/display/draw.jsx"))};
import { paramCases, durOf } from ${JSON.stringify(path.join(ROOT, "src/features/display/params.js"))};
export { PAIRS, paramCases, durOf };
export const frame = (p, mode, t, th, P) => renderToStaticMarkup(<g><SceneTitle title={p.title[mode]} sub={p.sub[mode]} C={PALETTE[th]} mode={mode} />{p.render(mode, t, PALETTE[th], P)}</g>);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const GROUP_N = { geo: 12, data: 5, guess: 3, branch: 3, galton: 1 };
  test("장면 묶음(도형 12 · 경우의 수·확률 5 · 몬티홀·찍기 3 · 갈림길·구슬 3 · 정규분포 1) · 키 중복 없음 · 제목/부제 두 판 · 길이 15~70초", () => {
    for (const [g, n] of Object.entries(GROUP_N)) assert.equal(m.PAIRS.filter((p) => p.group === g).length, n, g);
    assert.equal(new Set(m.PAIRS.map((p) => p.key)).size, m.PAIRS.length);
    for (const p of m.PAIRS) {
      assert.ok(p.title.e && p.title.m && p.sub.e && p.sub.m, p.key);
      for (const P of m.paramCases(p)) { const d = m.durOf(p, P); assert.ok(d > 15000 && d < 70000, `${p.key} ${JSON.stringify(P)} ${d}`); }
    }
  });
  test("장면 설정(controls): 기본값이 고를 수 있는 값 · 단계/구슬/문 개수", () => {
    for (const p of m.PAIRS.filter((q) => q.controls)) for (const c of p.controls) {
      assert.ok(c.options.some((o) => (Array.isArray(o) ? o[0] : o) === c.def), `${p.key}.${c.key}`);
      assert.ok(["step", "seg"].includes(c.kind));
    }
    assert.deepEqual(m.PAIRS.filter((q) => q.controls).map((q) => q.key).sort(), ["bump", "forkn", "galton", "monty"]);
  });
  for (const p of m.PAIRS) for (const P of m.paramCases(p)) {
    const dur = m.durOf(p, P), tag = Object.keys(P).length ? ` ${JSON.stringify(P)}` : "";
    test(`그리기 훑기: ${p.key}${tag} (${(dur / 1000).toFixed(1)}초) — 두 판·두 테마, 오류·NaN 없음`, () => {
      for (const mode of ["e", "m"]) for (const th of ["dark", "light"]) {
        for (let t = 0; t <= dur; t += th === "dark" ? 125 : 500) {
          const s = m.frame(p, mode, t, th, P);
          assert.ok(!/NaN|undefined|Infinity/.test(s), `${mode}/${th} t=${t}: ${(s.match(/.{50}(NaN|undefined|Infinity).{30}/) || [""])[0]}`);
        }
      }
    });
  }
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
