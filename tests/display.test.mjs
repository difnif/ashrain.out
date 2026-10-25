// node tests/display.test.mjs — 교실 모니터(#/admin/display) 장면 검산. 실패 시 exit 1.
//   1) 화면에 나오는 수를 facts.js 와 따로 다시 계산해 맞춰 본다(입체의 위치 관계는 좌표로 판정).
//   2) 모든 장면 × 초등/중등 × 다크/라이트를 처음부터 끝까지 그려 보고 오류·NaN 이 없는지 본다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  BLOCKS, CIRCLE, LEAF, NETS, CYL, SPHERE, TRI3, POLY, DIAG, ISO, PARA, TRAP, interiorAngles, sameEdge, fmt,
} from "../src/features/display/facts.js";
import { SOLIDS, foldAt, netEdgesOf, isHinge, lineRelation, linePlane } from "../src/features/display/solids.js";

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
export { PAIRS };
export const frame = (p, mode, t, th) => renderToStaticMarkup(<g><SceneTitle title={p.title[mode]} sub={p.sub[mode]} C={PALETTE[th]} mode={mode} />{p.render(mode, t, PALETTE[th])}</g>);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  test("장면 12쌍 · 키 중복 없음 · 제목/부제 두 판 모두 있음", () => {
    assert.equal(m.PAIRS.length, 12);
    assert.equal(new Set(m.PAIRS.map((p) => p.key)).size, 12);
    for (const p of m.PAIRS) { assert.ok(p.title.e && p.title.m && p.sub.e && p.sub.m, p.key); assert.ok(p.dur > 15000 && p.dur < 60000, `${p.key} ${p.dur}`); }
  });
  for (const p of m.PAIRS) {
    test(`그리기 훑기: ${p.key} (${(p.dur / 1000).toFixed(1)}초) — 두 판·두 테마, 오류·NaN 없음`, () => {
      for (const mode of ["e", "m"]) for (const th of ["dark", "light"]) {
        for (let t = 0; t <= p.dur; t += th === "dark" ? 125 : 500) {
          const s = m.frame(p, mode, t, th);
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
