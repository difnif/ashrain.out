// node tests/display-graph.test.mjs — 교실 모니터 「일차함수 그래프 그리기 해설」 액자 검산. 실패 시 exit 1.
// 문항: 발문의 조건(식 · 기울기 · 절편 · 두 점 · 평행 · 증가량 · 일차방정식)을 따로 읽어 정답 직선 y = mx + b 와 맞추고,
//       찍는 두 점이 그 직선 위 · 모눈(−5~5) 안인지, 풀이 순서 글자의 좌표 · 칸 수 · 방향이 두 점과 맞는지 본다.
// 박자표: 줄마다 형광펜 → 칸 채우기 → 그림 순서, 두 점을 한 번씩 찍고 마지막 줄이 직선, 정답 식은 다 그린 뒤.
// 네모 칸: 풀이 줄의 수 · 방향이 빠짐없이 칸에 들어가고, 조각을 이으면 원래 글자가 된다.
// 그리기: 160문항을 여러 순간 × 두 테마로 그려 오류 · NaN 이 없는지, 글자 판이 무대 안에 들어가는지 훑는다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { GD_SETS, GD, gdPlan, stepAt, stepAtoms, q, qv, qeq, qadd, qmul, qneg, qstr, ptStr, linStr, clipLine, lapOf } from "../src/features/display/graphdraw.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}
const ALL = [...GD_SETS.basic.items.map((it) => ["기본", it]), ...GD_SETS.hard.items.map((it) => ["심화", it])];

/* ══════════ 일차식 읽기 (발문을 따로 읽는다) ══════════ */
/** "3x − 4y − 12" · "−(3/4)x + 4" · "3 − 2x" → { x, y, c } (분수) */
function linExpr(s) {
  const t = s.replace(/−/g, "-").replace(/\s+/g, "");
  const out = { x: q(0), y: q(0), c: q(0) };
  const re = /([+-]?)(\(\d+\/\d+\)|\d+(?:\/\d+)?)?([xy])?/g;
  let m;
  while ((m = re.exec(t)) && m[0] !== "") {
    let k = m[2] ? q(m[2].replace(/[()]/g, "")) : q(1);
    if (m[1] === "-") k = qneg(k);
    const v = m[3] || "c";
    if (!m[2] && !m[3]) continue;
    out[v] = qadd(out[v], k);
  }
  return out;
}
/** "y = …" 꼴 → { m, b } */
function fromY(s) { const e = linExpr(s.split("=")[1]); assert.ok(qeq(e.y, q(0))); return { m: e.x, b: e.c }; }
/** 일차방정식 "Ax + By + C = 0" · "Ax + By = D" → { m, b } */
function fromEq(s) {
  const [l, r] = s.split("=");
  const L = linExpr(l), Rr = linExpr(r);
  const A = qadd(L.x, qneg(Rr.x)), B = qadd(L.y, qneg(Rr.y)), C = qadd(L.c, qneg(Rr.c));
  assert.ok(qv(B) !== 0, "y 계수 0");
  const inv = q(`${-B.d}/${B.n}`);
  return { m: qmul(A, inv), b: qmul(C, inv) };
}
const num = (s) => q(s);
const onLine = (m, b, P) => qeq(qadd(qmul(m, P[0]), b), P[1]);

/** 발문만 읽어 정답 직선을 정한다 — 생성기와 따로 */
function solve(it) {
  const s = it.q;
  let g;
  if ((g = s.match(/^일차방정식 (.+?)의 그래프와 평행하고 점 \((\S+), (\S+)\)[을를] 지나는/))) {
    const { m } = fromEq(g[1]); const P = [num(g[2]), num(g[3])];
    return { m, b: qadd(P[1], qneg(qmul(m, P[0]))), par: fromEq(g[1]).b };
  }
  if ((g = s.match(/^일차방정식 (.+?)의 그래프를/))) return fromEq(g[1]);
  if ((g = s.match(/^일차함수 (y = .+?)의 그래프와 평행하고 y절편이 (\S+)인/))) { const L = fromY(g[1]); return { m: L.m, b: num(g[2]), par: L.b }; }
  if ((g = s.match(/^일차함수 (y = .+?)의 그래프와 평행하고 점 \((\S+), (\S+)\)[을를] 지나는/))) {
    const L = fromY(g[1]); const P = [num(g[2]), num(g[3])];
    return { m: L.m, b: qadd(P[1], qneg(qmul(L.m, P[0]))), par: L.b };
  }
  if ((g = s.match(/^일차함수 (y = .+?)의 그래프를/))) return fromY(g[1]);
  if ((g = s.match(/^기울기가 일차함수 (y = .+?)의 그래프와 같고 y절편이 (\S+)인/))) return { m: fromY(g[1]).m, b: num(g[2]) };
  if ((g = s.match(/^기울기가 (\S+)이고 y절편이 (\S+)인/))) return { m: num(g[1]), b: num(g[2]) };
  if ((g = s.match(/^기울기가 (\S+)이고 점 \((\S+), (\S+)\)[을를] 지나는/))) {
    const m = num(g[1]), P = [num(g[2]), num(g[3])]; return { m, b: qadd(P[1], qneg(qmul(m, P[0]))) };
  }
  if ((g = s.match(/^x절편이 (\S+), y절편이 (\S+)인/))) {
    const x0 = num(g[1]), b = num(g[2]); return { m: qmul(qneg(b), q(`${x0.d}/${x0.n}`)), b };
  }
  if ((g = s.match(/^두 점 \((\S+), (\S+)\), \((\S+), (\S+)\)[을를] 지나는/))) {
    const A = [num(g[1]), num(g[2])], B = [num(g[3]), num(g[4])];
    const m = qmul(qadd(B[1], qneg(A[1])), q(`${qadd(B[0], qneg(A[0])).d}/${qadd(B[0], qneg(A[0])).n}`));
    return { m, b: qadd(A[1], qneg(qmul(m, A[0]))), pts: [A, B] };
  }
  if ((g = s.match(/^x의 값이 (\d+)만큼 증가할 때 y의 값은 (\d+)만큼 (증가|감소)하고, (?:y절편이 (\S+)인|점 \((\S+), (\S+)\)[을를] 지나는)/))) {
    const m = q(`${(g[3] === "증가" ? 1 : -1) * +g[2]}/${g[1]}`);
    if (g[4] != null) return { m, b: num(g[4]) };
    const P = [num(g[5]), num(g[6])]; return { m, b: qadd(P[1], qneg(qmul(m, P[0]))) };
  }
  throw new Error("못 읽은 발문: " + s);
}

/* ══════════ 문항 ══════════ */
test("문항 수 · 번호: 기본 96 · 심화 64, 1번부터 빠짐없이", () => {
  for (const [k, cnt] of [["basic", 96], ["hard", 64]]) {
    const L = GD_SETS[k].items;
    assert.equal(L.length, cnt);
    L.forEach((it, i) => assert.equal(it.no, i + 1, `${k} ${i}`));
  }
});

test("발문을 따로 읽은 직선 = 정답 직선 (160문항, 평행은 다른 직선 · 두 점은 주어진 두 점)", () => {
  for (const [S, it] of ALL) {
    const r = solve(it), m = q(it.m), b = q(it.b), tag = `${S} ${it.no}`;
    assert.ok(qeq(r.m, m), `${tag} 기울기 ${qstr(r.m)} ≠ ${qstr(m)}`);
    assert.ok(qeq(r.b, b), `${tag} y절편 ${qstr(r.b)} ≠ ${qstr(b)}`);
    if (r.par) assert.ok(!qeq(r.par, b), `${tag} 평행인데 같은 직선`);
    if (r.pts) for (const P of r.pts) assert.ok(r.pts.some(() => [it.P1, it.P2].some((Pp) => qeq(q(Pp[0]), P[0]) && qeq(q(Pp[1]), P[1]))), `${tag} 두 점`);
  }
});

test("찍는 두 점: 정답 직선 위 · 모눈 −5~5 안 · 서로 다름 · 기울기 0 아님", () => {
  for (const [S, it] of ALL) {
    const m = q(it.m), b = q(it.b), P1 = it.P1.map(q), P2 = it.P2.map(q), tag = `${S} ${it.no}`;
    assert.ok(m.n !== 0, tag);
    for (const P of [P1, P2]) {
      assert.ok(onLine(m, b, P), `${tag} ${ptStr(P)} 직선 밖`);
      assert.ok(Math.abs(qv(P[0])) <= 5 && Math.abs(qv(P[1])) <= 5, `${tag} ${ptStr(P)} 모눈 밖`);
      assert.ok(P[0].d === 1 && P[1].d === 1, `${tag} 격자점 아님`);
    }
    assert.ok(!(qeq(P1[0], P2[0]) && qeq(P1[1], P2[1])), tag);
  }
});

test("풀이 순서 글자: 좌표는 두 점 · 칸 수와 방향은 두 점의 차 · 적힌 기울기는 정답 기울기", () => {
  const DIR = { 오른쪽: 1, 왼쪽: -1, 위: 1, 아래: -1 };
  for (const [S, it] of ALL) {
    const tag = `${S} ${it.no}`, P1 = it.P1.map(q), P2 = it.P2.map(q), m = q(it.m);
    const pts = new Set([ptStr(P1), ptStr(P2)]);
    const all = it.steps.join(" / ");
    for (const c of all.matchAll(/\((−?\d+), (−?\d+)\)/g)) assert.ok(pts.has(c[0]), `${tag} 모르는 좌표 ${c[0]}`);
    assert.ok(all.includes(ptStr(P1)) && all.includes(ptStr(P2)), `${tag} 두 점이 다 적히지 않음`);
    const mv = all.match(/(오른쪽|왼쪽)으로 (\d+)칸, (위|아래)로 (\d+)칸/);
    if (mv) {
      assert.equal(DIR[mv[1]] * +mv[2], qv(P2[0]) - qv(P1[0]), `${tag} 가로`);
      assert.equal(DIR[mv[3]] * +mv[4], qv(P2[1]) - qv(P1[1]), `${tag} 세로`);
      assert.ok(qeq(q(`${DIR[mv[3]] * +mv[4]}/${DIR[mv[1]] * +mv[2]}`), m), `${tag} 칸 비율 ≠ 기울기`);
    }
    for (const s of it.steps) {
      const g = s.match(/기울기 (−?\d+(?:\/\d+)?)/) || s.match(/= (−?\d+(?:\/\d+)?)$/);
      if (g && s.includes("기울기")) assert.ok(qeq(q(g[1]), m), `${tag} 「${s}」`);
    }
    assert.ok(it.steps[it.steps.length - 1].startsWith("두 점을 지나는"), `${tag} 마지막 줄`);
  }
});

/* ══════════ 박자표 ══════════ */
test("박자표: 줄마다 형광펜 → 칸 채우기 → 그림, 두 점을 한 번씩 찍고 마지막 줄이 직선, 정답 식은 그 뒤", () => {
  for (const [S, it] of ALL) {
    const P = gdPlan(it), tag = `${S} ${it.no}`;
    let prev = 0;
    for (const st of P.steps) {
      assert.ok(st.a >= prev && st.f[0] > st.a && st.f[1] > st.f[0] && st.b > st.f[1], `${tag} 줄 순서`);
      for (const a of st.acts) assert.ok(a.a >= st.f[1] && a.b <= st.b && a.b > a.a, `${tag} 그림이 그 줄 안`);
      prev = st.b;
    }
    const acts = P.steps.flatMap((s) => s.acts);
    const dots = acts.filter((a) => a.type === "dot");
    assert.equal(dots.length, 2, `${tag} 점 ${dots.length}개`);
    assert.ok(dots.some((d) => d.P === P.P1) && dots.some((d) => d.P === P.P2), tag);
    assert.ok(dots.find((d) => d.P === P.P1).a < dots.find((d) => d.P === P.P2).a, `${tag} P1 먼저`);
    const lines = acts.filter((a) => a.type === "line");
    assert.equal(lines.length, 1); assert.ok(P.steps[P.steps.length - 1].acts.includes(lines[0]), tag);
    assert.ok(lines[0].a > dots[1].b, `${tag} 직선은 두 점 뒤`);
    const moves = acts.filter((a) => a.type === "move");
    assert.equal(moves.length, it.steps.filter((s) => s.includes("칸")).length, tag);
    for (const mv of moves) {
      assert.ok(mv.v[0] > mv.h[1], tag);
      assert.ok(Math.abs(mv.h[1] - mv.h[0] - GD.CELL * Math.abs(mv.run) - GD.MVPAD) < 1e-6, `${tag} 칸 수만큼`);
    }
    assert.ok(P.ans >= P.steps[P.steps.length - 1].b && P.dur === P.ans + GD.ANS + GD.HOLD, tag);
    assert.equal(stepAt(P, 0), 0); assert.equal(stepAt(P, P.ans), P.steps.length);
    assert.ok(P.dur > 12000 && P.dur < 60000, `${tag} 한 문항 ${P.dur} ms`);
  }
  const lapB = lapOf(GD_SETS.basic.items), lapH = lapOf(GD_SETS.hard.items);
  console.log(`   한 바퀴: 기본 ${(lapB / 60000).toFixed(1)}분 · 심화 ${(lapH / 60000).toFixed(1)}분 (1×)`);
});

test("직선 자르기: 두 끝이 칸 경계 위 · 직선 위", () => {
  for (const [, it] of ALL) {
    const mv = qv(q(it.m)), bv = qv(q(it.b)), L = 5.45;
    for (const p of clipLine(mv, bv, L)) {
      assert.ok(Math.abs(mv * p[0] + bv - p[1]) < 1e-9);
      assert.ok(Math.abs(Math.abs(p[0]) - L) < 1e-9 || Math.abs(Math.abs(p[1]) - L) < 1e-9);
    }
  }
});

/* ══════════ 네모 칸 ══════════ */
test("네모 칸: 수 · 방향이 빠짐없이 칸에, 조각을 이으면 원래 글자, 「y에 대해 풀면」은 식 한 칸", () => {
  for (const [S, it] of ALL) for (const s of it.steps) {
    const A = stepAtoms(s), tag = `${S} ${it.no} 「${s}」`;
    const back = A.map((a) => (a.t === "txt" ? a.s : a.v)).join("");
    assert.equal(back, s, tag);
    const txt = A.filter((a) => a.t === "txt").map((a) => a.s).join("|").replace("(y 증가량)/(x 증가량)", "");
    assert.ok(!/\d|오른쪽|왼쪽|위|아래/.test(txt), `${tag} 칸 밖에 남은 수 · 방향: ${txt}`);
    if (s.startsWith("y에 대해 풀면")) assert.equal(A.find((a) => a.t === "box").k, "eq", tag);
    assert.equal(A[0].glue, false, tag);
  }
});

test("정답 식 글자: y = (3/4)x − 3 꼴, 다시 읽으면 같은 직선", () => {
  for (const [S, it] of ALL) {
    const s = linStr(q(it.m), q(it.b)), r = fromY(s);
    assert.ok(qeq(r.m, q(it.m)) && qeq(r.b, q(it.b)), `${S} ${it.no} ${s}`);
  }
  assert.equal(linStr(q("-3/4"), q("-3")), "y = −(3/4)x − 3");
  assert.equal(linStr(q("1"), q("0")), "y = x");
});

/* ══════════ 그리기 훑기(번들) ══════════ */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-graph-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { FRAMES } from ${F("frames/index.js")};
import { GraphArt, GraphThumb, graphScenes, layoutOf, GD_BOX } from ${F("frames/graphdraw.jsx")};
export { FRAMES, graphScenes, layoutOf, GD_BOX };
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const art = (it, t, th) => svg(<GraphArt it={it} t={t} C={PALETTE[th]} />);
export const scene = (sc, t, th) => svg(sc.render("m", t, PALETTE[th]));
export const thumb = (th) => svg(<GraphThumb C={PALETTE[th]} />);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{50}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];

  test("액자 목록: 「일차함수 그래프 그리기 해설」이 해설 액자로 · 그림 두 테마 오류 없음", () => {
    const f = m.FRAMES.find((x) => x.key === "graph");
    assert.ok(f && f.lesson && f.title && f.desc);
    for (const th of ["dark", "light"]) { const s = m.thumb(th); assert.ok(s.length > 5000 && !BAD.test(s), `${th}: ${bad(s)}`); }
  });

  test("그리기 훑기: 160문항 × (시작 · 줄마다 형광펜 · 칸 채우기 · 그림 중간 · 정답 · 끝) × 두 테마 — 오류 · NaN 없음", () => {
    let cnt = 0;
    for (const [S, it] of ALL) {
      const P = gdPlan(it);
      const ts = [0, 500, P.ans, P.ans + 400, P.dur - 1];
      for (const st of P.steps) { ts.push(st.a + 200, (st.f[0] + st.f[1]) / 2); for (const a of st.acts) ts.push((a.a + a.b) / 2, a.b); }
      for (const t of ts) {
        const s = m.art(it, t, cnt++ % 2 ? "dark" : "light");
        assert.ok(!BAD.test(s), `${S} ${it.no} t=${Math.round(t)}: ${bad(s)}`);
      }
      const end = m.art(it, P.dur - 1, "dark");
      assert.ok(end.includes(ptStr(P.P1)) && end.includes(ptStr(P.P2)), `${S} ${it.no} 끝 그림에 두 점의 좌표`);
    }
    console.log(`   그림 ${cnt}장`);
  });

  test("글자 판: 발문 · 풀이 순서 · 정답 식이 무대 왼쪽 판(가로 · 세로) 안에", () => {
    const B = m.GD_BOX;
    for (const [S, it] of ALL) {
      const L = m.layoutOf(it), tag = `${S} ${it.no}`;
      assert.ok(L.ansY + L.ss * 0.6 <= B.BOTTOM, `${tag} 아래로 넘침 ${Math.round(L.ansY)}`);
      for (const st of L.steps) for (const line of st.lines) for (const p of line) assert.ok(p.x + p.w <= B.RIGHT + 4, `${tag} 오른쪽으로 넘침`);
    }
  });

  test("장면 목록(재생기 형식): 세트 × 빠르기 — 1.5× 는 길이가 2/3, 같은 순간을 그린다", () => {
    for (const k of ["basic", "hard"]) {
      const a = m.graphScenes(k, 1), b = m.graphScenes(k, 1.5);
      assert.equal(a.length, GD_SETS[k].items.length);
      assert.equal(new Set(a.map((s) => s.key)).size, a.length);
      a.forEach((s, i) => {
        assert.ok(Math.abs(b[i].dur - s.dur / 1.5) <= 1, s.key);
        assert.ok(s.title.m && s.sub.m.includes(`${s.no}번`));
      });
      assert.equal(m.scene(a[5], 9000, "dark"), m.scene(b[5], 6000, "dark"));
    }
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
