// node tests/display-lin10.test.mjs — 교실 모니터 「일차함수 10단계 계산 해설」 액자 검산. 실패 시 exit 1.
// 판서: 줄마다 식을 분수로 직접 계산해 「=」로 이은 모든 쪽이 같은지 본다(문자는 그 문항의 판서가 구한 값으로).
//       마지막에 구한 값이 답과 같은지, 10단계(방정식 ↔ 함수 식)는 모든 줄이 답의 직선과 같은 식인지(x = −2 ~ 3 에서).
// 박자표: 문제 → 방침 → 줄 차례 → 답, 메모는 그 줄 안. 목록: 세트마다 1~200번 · 단계마다 20문항.
// 그리기: 400문항을 여러 순간 × 두 테마로 그려 오류 · NaN 이 없는지, 글자 판 · 9단계 그림이 무대 안인지 훑는다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { L10_SETS, L10, l10Plan, lineAt, lapOf } from "../src/features/display/lin10.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}
const ALL = [...L10_SETS[1].items.map((it) => [1, it]), ...L10_SETS[2].items.map((it) => [2, it])];

/* ══════════ 분수 ══════════ */
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
const Q = (n, d = 1) => { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d); return { n: n / g, d: d / g }; };
const add = (a, b) => Q(a.n * b.d + b.n * a.d, a.d * b.d);
const neg = (a) => Q(-a.n, a.d);
const mul = (a, b) => Q(a.n * b.n, a.d * b.d);
const div = (a, b) => { assert.ok(b.n !== 0, "0으로 나눔"); return Q(a.n * b.d, a.d * b.n); };
const eq = (a, b) => a.n === b.n && a.d === b.d;
const str = (a) => (a.d === 1 ? `${a.n}` : `${a.n}/${a.d}`);

/* ══════════ 판서 식 읽기: 수 · {a/b} · 괄호 · + − × ÷ · 곱 생략(2k · {3/4}x) · 문자 ══════════ */
function tokens(s) {
  const t = s.replace(/\(기울기\)|기울기/g, "g").replace(/−/g, "-");
  const out = [];
  for (let i = 0; i < t.length;) {
    const c = t[i];
    if (c === " ") { i++; continue; }
    if (c === "{") {
      const j = t.indexOf("}", i), [a, b] = t.slice(i + 1, j).split("/");
      out.push({ k: "num", v: Q(parseInt(a, 10), parseInt(b, 10)) }); i = j + 1; continue;
    }
    if (/\d/.test(c)) { let j = i; while (j < t.length && /\d/.test(t[j])) j++; out.push({ k: "num", v: Q(parseInt(t.slice(i, j), 10)) }); i = j; continue; }
    if (/[a-z]/.test(c)) { out.push({ k: "var", v: c }); i++; continue; }
    if ("+-×÷()".includes(c)) { out.push({ k: c }); i++; continue; }
    throw new Error(`읽을 수 없는 글자 「${c}」 in ${s}`);
  }
  return out;
}
function evalExpr(s, env) {
  const T = tokens(s);
  let p = 0;
  const peek = () => T[p];
  const startsFactor = (tk) => tk && (tk.k === "num" || tk.k === "var" || tk.k === "(");
  function factor() {
    const tk = T[p++];
    if (!tk) throw new Error("식이 끊김: " + s);
    if (tk.k === "-") return neg(factor());
    if (tk.k === "num") return tk.v;
    if (tk.k === "var") { if (!(tk.v in env)) throw new Error(`모르는 문자 ${tk.v}: ${s}`); return env[tk.v]; }
    if (tk.k === "(") { const v = expr(); assert.equal(T[p++]?.k, ")", "괄호: " + s); return v; }
    throw new Error("뜻밖의 기호 " + tk.k + ": " + s);
  }
  function term() {
    let v = factor();
    for (;;) {
      const tk = peek();
      if (tk && tk.k === "×") { p++; v = mul(v, factor()); }
      else if (tk && tk.k === "÷") { p++; v = div(v, factor()); }
      else if (startsFactor(tk)) v = mul(v, factor());          // 곱 생략
      else return v;
    }
  }
  function expr() {
    let v = term();
    for (;;) {
      const tk = peek();
      if (tk && tk.k === "+") { p++; v = add(v, term()); }
      else if (tk && tk.k === "-") { p++; v = add(v, neg(term())); }
      else return v;
    }
  }
  const v = expr();
  assert.equal(p, T.length, "남은 글자: " + s);
  return v;
}
/** 식 줄인가(설명 글 줄은 건너뛴다) — 「기울기」 말고 한글이 없어야 식 */
const isEq = (ln) => ln.s.includes(" = ") && !/[가-힣]/.test(ln.s.replace(/\(기울기\)|기울기/g, ""));
const ansValue = (it) => {
  const m = it.ans.match(/= (.+)$/);
  return evalExpr(m[1], {});
};
/** 판서가 구한 값: 「문자 = … = 수」 꼴의 줄에서 */
function solved(it) {
  const env = {};
  for (const ln of it.lines.filter(isEq)) {
    const sides = ln.s.split(" = ");
    const head = sides[0].replace(/\(기울기\)|기울기/, "g").trim();
    if (sides.length >= 2 && /^[a-z]$/.test(head)) {
      try { env[head] = evalExpr(sides[sides.length - 1], {}); } catch { /* 끝이 수가 아니면 건너뜀 */ }
    }
  }
  return env;
}

/* ══════════ 문항 ══════════ */
test("문항 수 · 번호 · 단계: 세트마다 200문항, 1~200번, 단계마다 20문항씩 차례로", () => {
  for (const k of [1, 2]) {
    const L = L10_SETS[k].items;
    assert.equal(L.length, 200);
    L.forEach((it, i) => { assert.equal(it.no, i + 1); assert.equal(it.st, Math.floor(i / 20) + 1); });
  }
});

test("판서 1~9단계: 줄마다 「=」로 이은 모든 쪽이 같다 · 마지막에 구한 값 = 답", () => {
  let lines = 0;
  for (const [S, it] of ALL) {
    if (it.st === 10) continue;
    const env = solved(it), tag = `세트${S} ${it.no}`;
    for (const ln of it.lines) {
      if (!isEq(ln)) { assert.ok(/[가-힣]/.test(ln.s), `${tag} 식도 글도 아닌 줄 「${ln.s}」`); continue; }
      const sides = ln.s.split(" = ");
      const vals = sides.map((x) => evalExpr(x, env));
      for (const v of vals) assert.ok(eq(v, vals[0]), `${tag} 「${ln.s}」 ${vals.map(str).join(" | ")}`);
      lines++;
    }
    const last = [...it.lines].reverse().find(isEq);
    const lv = last.s.split(" = ");
    assert.ok(eq(evalExpr(lv[lv.length - 1], env), ansValue(it)), `${tag} 마지막 값 ≠ 답 ${it.ans}`);
  }
  console.log(`   등식 ${lines}줄`);
});

test("판서 10단계: 모든 줄이 답의 직선과 같은 식 (x = −2 ~ 3)", () => {
  for (const [S, it] of ALL) {
    if (it.st !== 10) continue;
    const tag = `세트${S} ${it.no}`;
    // 답의 직선: y = … 꼴이면 그대로, … = 0 꼴이면 y 에 대해 푼 값
    const yAt = (x) => {
      if (it.ans.startsWith("y = ")) return evalExpr(it.ans.slice(4), { x });
      const lhs = it.ans.split(" = ")[0];
      const c0 = evalExpr(lhs, { x, y: Q(0) }), c1 = add(evalExpr(lhs, { x, y: Q(1) }), neg(c0));
      return div(neg(c0), c1);
    };
    for (const ln of it.lines) {
      const sides = ln.s.split(" = ");
      assert.equal(sides.length, 2, tag);
      for (let x = -2; x <= 3; x++) {
        const env = { x: Q(x), y: yAt(Q(x)) };
        assert.ok(eq(evalExpr(sides[0], env), evalExpr(sides[1], env)), `${tag} 「${ln.s}」 x=${x}`);
      }
    }
    assert.ok(it.lines.length >= 1 && (it.lines[it.lines.length - 1].s === it.ans || it.ans.startsWith(it.lines[it.lines.length - 1].s.split(" = ")[0])), `${tag} 마지막 줄 ${it.lines[it.lines.length - 1].s} / ${it.ans}`);
  }
});

test("박자표: 문제 → 방침 → 줄 차례 → 답, 메모는 그 줄 안 · 한 문항 9~45초", () => {
  for (const [S, it] of ALL) {
    const P = l10Plan(it), tag = `세트${S} ${it.no}`;
    assert.ok(P.q[0] === 0 && P.plan[0] >= P.q[1] && P.lines[0].a > P.plan[1], tag);
    let prev = P.plan[1];
    P.lines.forEach((L, i) => {
      assert.ok(L.a >= prev && L.b > L.a, tag);
      if (L.m) assert.ok(L.m[0] > L.a && L.m[1] <= L.b, `${tag} 메모`);
      assert.equal(!!L.m, !!it.lines[i].memo, tag);
      prev = L.b;
    });
    assert.ok(P.ans > prev && P.dur === P.ans + L10.ANS + L10.HOLD, tag);
    assert.equal(lineAt(P, 0), -1); assert.equal(lineAt(P, P.ans), it.lines.length);
    assert.ok(P.dur >= 9000 && P.dur <= 45000, `${tag} ${P.dur}`);
  }
  console.log(`   한 바퀴(1×): 세트 1 ${(lapOf(L10_SETS[1].items) / 60000).toFixed(0)}분 · 세트 2 ${(lapOf(L10_SETS[2].items) / 60000).toFixed(0)}분`);
});

test("9단계 그림: 색칠한 부분의 넓이 = 판서의 답 (꼭짓점으로 다시 계산)", () => {
  for (const [S, it] of ALL) {
    if (it.st !== 9) continue;
    const pts = it.fig.poly;
    let a2 = 0;
    for (let i = 0; i < pts.length; i++) { const [x1, y1] = pts[i], [x2, y2] = pts[(i + 1) % pts.length]; a2 += x1 * y2 - x2 * y1; }
    assert.ok(eq(Q(Math.abs(a2), 2), ansValue(it)), `세트${S} ${it.no}`);
    // P 는 두 직선의 교점: ℓ = A–P, m = B–P 가 서로 다른 직선
    const [A, B, P] = [it.fig.A, it.fig.B, it.fig.P];
    assert.ok((A[0] - P[0]) * (B[1] - P[1]) - (A[1] - P[1]) * (B[0] - P[0]) !== 0, `세트${S} ${it.no} 평행`);
  }
});

/* ══════════ 그리기 훑기(번들) ══════════ */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-lin10-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { FRAMES } from ${F("frames/index.js")};
import { L10Art, Lin10Thumb, l10Scenes, layoutOf, L10_BOX } from ${F("frames/lin10.jsx")};
export { FRAMES, l10Scenes, layoutOf, L10_BOX };
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const art = (it, t, th) => svg(<L10Art it={it} t={t} C={PALETTE[th]} />);
export const scene = (sc, t, th) => svg(sc.render("m", t, PALETTE[th]));
export const thumb = (th) => svg(<Lin10Thumb C={PALETTE[th]} />);
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

  test("액자 목록: 「일차함수 10단계 계산 해설」이 해설 액자로 · 그림 두 테마 오류 없음", () => {
    const f = m.FRAMES.find((x) => x.key === "lin10");
    assert.ok(f && f.lesson && f.title && f.desc);
    for (const th of ["dark", "light"]) { const s = m.thumb(th); assert.ok(s.length > 4000 && !BAD.test(s), `${th}: ${bad(s)}`); }
  });

  test("그리기 훑기: 400문항 × (문제 · 방침 · 줄마다 · 메모 · 답 · 끝) × 두 테마 — 오류 · NaN 없음", () => {
    let cnt = 0;
    for (const [S, it] of ALL) {
      const P = l10Plan(it);
      const ts = [0, 300, P.plan[0] + 300, P.ans + 300, P.dur - 1];
      for (const L of P.lines) { ts.push(L.a + 100, (L.a + L.b) / 2); if (L.m) ts.push((L.m[0] + L.m[1]) / 2); }
      for (const t of ts) {
        const s = m.art(it, t, cnt++ % 2 ? "dark" : "light");
        assert.ok(!BAD.test(s), `세트${S} ${it.no} t=${Math.round(t)}: ${bad(s)}`);
      }
    }
    console.log(`   그림 ${cnt}장`);
  });

  test("글자 판: 발문 · 판서 · 메모 · 답이 무대 안(9단계는 그림 왼쪽) · 그림은 칸 안", () => {
    const B = m.L10_BOX;
    for (const [S, it] of ALL) {
      const L = m.layoutOf(it), tag = `세트${S} ${it.no}`;
      assert.ok(L.ansY + L.bs * 0.75 <= B.BOTTOM, `${tag} 아래로 넘침 (${Math.round(L.ansY)})`);
      for (const r of L.rows) {
        assert.ok(r.sx + r.sW <= L.right + 2, `${tag} 줄이 오른쪽으로 넘침`);
        if (r.mx != null) assert.ok(r.my < B.BOTTOM, tag);
      }
      if (it.fig) for (const v of [...it.fig.poly, it.fig.P]) assert.ok(Number.isFinite(v[0]) && Number.isFinite(v[1]));
    }
  });

  test("장면 목록: 세트 × 빠르기 × 단계 — 단계를 고르면 20문항 · 1.5× 는 길이 2/3 · 같은 순간", () => {
    for (const k of [1, 2]) {
      const all = m.l10Scenes(k, 1, 0), fast = m.l10Scenes(k, 1.5, 0);
      assert.equal(all.length, 200);
      assert.equal(new Set(all.map((s) => s.key)).size, 200);
      for (let st = 1; st <= 10; st++) {
        const one = m.l10Scenes(k, 1, st);
        assert.equal(one.length, 20); assert.ok(one.every((s) => s.st === st));
        assert.ok(one[0].sub.m.startsWith(`${st}단계`));
      }
      all.forEach((s, i) => assert.ok(Math.abs(fast[i].dur - s.dur / 1.5) <= 1));
      assert.equal(m.scene(all[30], 9000, "dark"), m.scene(fast[30], 6000, "dark"));
    }
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
