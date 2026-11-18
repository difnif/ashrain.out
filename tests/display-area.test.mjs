// node tests/display-area.test.mjs — 교실 모니터 「일차함수 그래프와 넓이 해설」 액자 검산. 실패 시 exit 1.
// 문항: 100제 · 240제 번호 · 단계. 그림: 색칠한 부분의 넓이 = 답(꼭짓점 신발끈), 꼭짓점은 두 경계 직선의 교점, 모든 변이 경계 직선 위.
//       9단계(넓이가 주어질 때)는 발문의 넓이 = 그림의 넓이, 10단계(이등분)는 두 조각이 정확히 반씩.
//       풀이 줄의 점은 직선(축 포함) 위 · 둘러싼 직사각형 − 바깥 삼각형 = 넓이.
// 박자표: 문제 → 방침 → 줄 차례 → 답. 그리기: 340문항을 여러 순간 × 두 테마로 그려 오류 · NaN 이 없는지,
//       글자 판이 무대 안 · 그림 글자가 그림 칸 안인지 훑는다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { AREA_SETS, AR, arPlan, lineAt, lapOf, onLine, polyArea } from "../src/features/display/area.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}
const A = AREA_SETS.A.items, B = AREA_SETS.B.items;
const ALL = [...A.map((it) => ["A", it]), ...B.map((it) => ["B", it])];
const near = (a, b, e = 1e-6) => Math.abs(a - b) < e;
/** 「넓이 = {25/2}」 · 「−{3/2}」 → 수 */
const val = (s) => {
  const t = String(s).replace(/^넓이 = /, "").replace(/−/g, "-").trim();
  const m = t.match(/^(-?)\{(\d+)\/(\d+)\}$/);
  return m ? (m[1] ? -1 : 1) * (+m[2] / +m[3]) : Number(t);
};
const AXES = [{ t: "hy", k: 0 }, { t: "vx", k: 0 }];
const bounds = (it) => [...AXES, ...it.fig.lines.filter((L) => !L.dash)];

/* ══════════ 문항 ══════════ */
test("문항 수 · 번호 · 단계: 100제 1~100번 · 240제 1~240번(단계마다 24문항씩 차례로)", () => {
  assert.equal(A.length, 100); assert.equal(B.length, 240);
  A.forEach((it, i) => assert.equal(it.no, i + 1));
  B.forEach((it, i) => { assert.equal(it.no, i + 1); assert.equal(it.lv, Math.floor(i / 24) + 1); });
  for (const [, it] of ALL) assert.ok(it.q && it.plan && it.ans && it.lines.length >= 2, it.no);
});

test("넓이: 색칠한 부분(꼭짓점 신발끈) = 답 · 9단계는 발문의 넓이", () => {
  for (const [S, it] of ALL) {
    const a = polyArea(it.fig.poly), tag = `${S}${it.no}`;
    if (it.ans.startsWith("넓이 = ")) assert.ok(near(a, val(it.ans)), `${tag} ${a} ≠ ${it.ans}`);
    else if (it.lv === 9) {
      const m = it.q.match(/넓이가 (\d+(?:\{[^}]*\})?)일 때/);
      assert.ok(m && near(a, val(m[1])), `${tag} ${a} / ${m && m[1]}`);
    }
  }
});

test("경계: 모든 변이 경계 직선(축 포함) 위 · 꼭짓점은 두 직선의 교점", () => {
  for (const [S, it] of ALL) {
    const P = it.fig.poly, L = bounds(it), tag = `${S}${it.no}`;
    P.forEach((p, i) => {
      const q = P[(i + 1) % P.length];
      assert.ok(L.some((l) => onLine(l, p) && onLine(l, q)), `${tag} 변 ${p}–${q}`);
      assert.ok(L.filter((l) => onLine(l, p)).length >= 2, `${tag} 꼭짓점 ${p}`);
    });
  }
});

test("10단계 이등분: 점선 직선으로 나눈 두 조각이 정확히 반씩 · 조각을 합치면 전체", () => {
  for (const it of B.filter((x) => x.lv === 10)) {
    const ops = it.lines.flatMap((l) => l.ops);
    const halves = ops.filter((o) => o.t === "poly");
    assert.equal(halves.length, 2, `${it.no}`);
    const all = polyArea(it.fig.poly);
    for (const h of halves) assert.ok(near(polyArea(h.pts), all / 2), `${it.no} ${polyArea(h.pts)} / ${all}`);
    assert.ok(ops.some((o) => o.t === "reveal") && it.fig.lines.some((l) => l.dash), `${it.no}`);
    const d = it.fig.lines.find((l) => l.dash);
    // 나눈 선은 답의 직선
    if (it.ans.startsWith("y = ")) assert.ok(it.ans.includes("x"), it.no);
    assert.ok(halves.every((h) => h.pts.filter((p) => onLine(d, p)).length >= 2), `${it.no} 자른 선`);
  }
});

test("풀이 줄의 그림: 점은 직선(축 포함) 위 · 밑변 · 높이는 길이가 있다 · 바깥 삼각형 합 = 직사각형 − 넓이", () => {
  let pts = 0;
  for (const [S, it] of ALL) {
    const L = [...AXES, ...it.fig.lines], tag = `${S}${it.no}`;
    const ops = it.lines.flatMap((l) => l.ops);
    for (const o of ops) {
      if (o.t === "pt") {
        const free = /^M\(|^\(/.test(o.s) && it.kind.startsWith("이등분");     // 중점 · 중심
        if (!free) assert.ok(L.some((l) => onLine(l, o.p)), `${tag} 점 ${o.s}`);
        pts++;
      }
      if (o.t === "seg") assert.ok(Math.hypot(o.a[0] - o.b[0], o.a[1] - o.b[1]) > 1e-9, `${tag} 선분`);
    }
    const box = ops.find((o) => o.t === "box");
    if (box) {
      const tri = ops.filter((o) => o.t === "poly").reduce((s, o) => s + polyArea(o.pts), 0);
      assert.ok(near(tri, polyArea(box.pts) - polyArea(it.fig.poly)), `${tag} 바깥 삼각형`);
    }
  }
  console.log(`   풀이 줄의 점 ${pts}개`);
});

test("박자표: 문제 → 방침 → 줄 차례 → 답 · 한 문항 12~60초", () => {
  for (const [S, it] of ALL) {
    const P = arPlan(it), tag = `${S}${it.no}`;
    assert.ok(P.q[0] === 0 && P.plan[0] >= P.q[1] && P.lines[0].a > P.plan[1], tag);
    let prev = P.plan[1];
    for (const L of P.lines) { assert.ok(L.a >= prev && L.b > L.a, tag); prev = L.b; }
    assert.ok(P.ans > prev && P.dur === P.ans + AR.ANS + AR.HOLD, tag);
    assert.equal(lineAt(P, 0), -1); assert.equal(lineAt(P, P.ans), it.lines.length);
    assert.ok(P.dur >= 12000 && P.dur <= 60000, `${tag} ${P.dur}`);
  }
  console.log(`   한 바퀴(1×): 100제 ${(lapOf(A) / 60000).toFixed(0)}분 · 240제 ${(lapOf(B) / 60000).toFixed(0)}분`);
});

/* ══════════ 그리기 훑기(번들) ══════════ */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-area-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { FRAMES } from ${F("frames/index.js")};
import { AreaArt, AreaThumb, areaScenes, layoutOf, figGeom, wrapMath, AREA_BOX } from ${F("frames/area.jsx")};
export { FRAMES, areaScenes, layoutOf, figGeom, wrapMath, AREA_BOX };
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const art = (it, t, th) => svg(<AreaArt it={it} t={t} C={PALETTE[th]} />);
export const scene = (sc, t, th) => svg(sc.render("m", t, PALETTE[th]));
export const thumb = (th) => svg(<AreaThumb C={PALETTE[th]} />);
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

  test("액자 목록: 「일차함수 그래프와 넓이 해설」이 해설 액자로 · 그림 두 테마 오류 없음", () => {
    const f = m.FRAMES.find((x) => x.key === "area");
    assert.ok(f && f.lesson && f.title && f.desc);
    for (const th of ["dark", "light"]) { const s = m.thumb(th); assert.ok(s.length > 4000 && !BAD.test(s), `${th}: ${bad(s)}`); }
  });

  test("줄 바꾸기: 식 가운데 · 좌표 가운데에서 끊지 않는다", () => {
    const rows = m.wrapMath("두 점 (0, −8), (1, 0)을 지나는 직선: y = 8x − 8", 40, 640, 560, true);
    assert.ok(rows.every((r) => !/[=+−×]$/.test(r) && !/^[=+−×]/.test(r)), rows.join(" | "));
    assert.ok(rows.every((r) => (r.match(/\(/g) || []).length === (r.match(/\)/g) || []).length), rows.join(" | "));
    const q = m.wrapMath("두 직선 ℓ: y = 2x − 8, m: y = *ax* + b가 점 P(1, −6)에서 만난다.", 36, 500);
    assert.ok(q.every((r) => !/\($|\(\S*,$/.test(r)), q.join(" | "));
  });

  test("그리기 훑기: 340문항 × (문제 · 방침 · 줄마다 · 답 · 끝) × 두 테마 — 오류 · NaN 없음", () => {
    let cnt = 0;
    for (const [S, it] of ALL) {
      const P = arPlan(it);
      const ts = [0, 300, P.plan[0] + 300, P.ans + 300, P.dur - 1];
      for (const L of P.lines) ts.push(L.a + 100, L.a + 400, (L.a + L.b) / 2);
      for (const t of ts) {
        const s = m.art(it, t, cnt++ % 2 ? "dark" : "light");
        assert.ok(!BAD.test(s), `${S}${it.no} t=${Math.round(t)}: ${bad(s)}`);
      }
    }
    console.log(`   그림 ${cnt}장`);
  });

  test("글자 판: 발문 · 방침 · 풀이 · 답이 무대 안(그림 왼쪽) · 그림 글자는 그림 칸 안", () => {
    const X = m.AREA_BOX;
    let tight = 0, labels = 0;
    for (const [S, it] of ALL) {
      const L = m.layoutOf(it), tag = `${S}${it.no}`;
      assert.ok(L.ansY + L.bs * 0.8 <= X.BOTTOM, `${tag} 아래로 넘침 (${Math.round(L.ansY)})`);
      const G = m.figGeom(it);
      const boxes = [...G.base.filter((b) => b.box).map((b) => b.box), ...G.ops.filter((g) => g.box).map((g) => g.box), ...G.names.filter(Boolean).map((g) => g.box)];
      for (const b of boxes) {
        assert.ok(b[0] >= X.FIG.x0 && b[2] <= X.FIG.x1 && b[1] >= X.FIG.y0 && b[3] <= X.FIG.y1, `${tag} 그림 글자가 칸 밖 ${b.map(Math.round)}`);
        labels++;
      }
      tight += [...G.base, ...G.ops, ...G.names.filter(Boolean)].filter((g) => g.sc != null && g.sc < -8).length;
    }
    console.log(`   그림 글자 ${labels}개 · 다른 것과 붙은 글자 ${tight}개`);
    assert.ok(tight <= labels * 0.04, `붙은 글자가 많다 ${tight}/${labels}`);
  });

  test("장면 목록: 세트 × 빠르기 × 단계 — 240제 단계를 고르면 24문항 · 1.5× 는 길이 2/3 · 같은 순간", () => {
    const a = m.areaScenes("A", 1, 0), b = m.areaScenes("B", 1, 0), bf = m.areaScenes("B", 1.5, 0);
    assert.equal(a.length, 100); assert.equal(b.length, 240);
    assert.equal(new Set([...a, ...b].map((s) => s.key)).size, 340);
    for (let lv = 1; lv <= 10; lv++) {
      const one = m.areaScenes("B", 1, lv);
      assert.equal(one.length, 24); assert.ok(one.every((s) => s.lv === lv));
      assert.ok(one[0].sub.m.startsWith(`${lv}단계`));
    }
    b.forEach((s, i) => assert.ok(Math.abs(bf[i].dur - s.dur / 1.5) <= 1));
    assert.equal(m.scene(b[150], 9000, "dark"), m.scene(bf[150], 6000, "dark"));
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
