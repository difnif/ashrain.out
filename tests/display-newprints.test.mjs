// node tests/display-newprints.test.mjs — 시그니처 프린트 해설 11장(2026-11-26) 검산. 실패 시 exit 1.
// ① 두 점을 지나는 일차함수의 식 1 ~ 5세트(lin2) · 교점 활용 · 만날 조건 쉬운 판 · 중~상 판 · 삼각형 조건(meet):
//    세트마다 100문항 · 번호 1 ~ 100 · 단계(lin2 10단계 × 10 · meet 5단계 × 20) · 문항 칸 · 그림 DSL(나타나는 때가 판서 줄 안 · 그림 칸 근처).
// ② 두 점 → 식: 발문의 두 점이 답의 직선 위 · 판서의 기울기 = 두 점의 증가량의 비.
// ③ 넓이 이등분(area C) · 넓이로 미지수(area D): 5단계 × 20 · 이등분 조각은 정확히 반씩 · 발문의 넓이 = 그림의 넓이 · 점선 직선이 나타난다.
// ④ 액자: 세트 문항은 고를 때 들여온다(들여오기 전 「불러오는 중」) · 장면 수 · 단계 고르기 · 목록 그림 · 모든 문항을 여러 순간 × 두 테마로 그려 오류 · NaN 없음.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

let n = 0, failed = 0;
async function test(name, fn) {
  n++;
  try { await fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.stack?.split("\n").slice(0, 3).join("\n   ") || e.message}`); }
}
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-newprints-"));
const store = {};
globalThis.localStorage = { getItem: (k) => store[k] ?? null, setItem: (k, v) => { store[k] = String(v); }, removeItem: (k) => { delete store[k]; } };

/** 무대 수식 문법의 수 → 수(「−{5/2}」 · 「3」 · 「1.5」) */
const numOf = (s) => {
  const t = String(s).replace(/−/g, "-").replace(/\s/g, "");
  const m = t.match(/^(-?)\{(\d+)\/(\d+)\}$/);
  if (m) return (m[1] ? -1 : 1) * (+m[2] / +m[3]);
  return Number(t);
};
/** 「y = −{5/2}x − 11」 → [기울기, 절편] */
function lineOf(ans) {
  const t = ans.replace(/^y = /, "").replace(/\*/g, "");
  const m = t.match(/^(−?)(\{\d+\/\d+\}|\d+(?:\.\d+)?)?x(?: ([+−]) (\{\d+\/\d+\}|\d+(?:\.\d+)?))?$/);
  assert.ok(m, `식 꼴: ${ans}`);
  const a = (m[1] ? -1 : 1) * (m[2] ? numOf(m[2]) : 1);
  const b = m[3] ? (m[3] === "−" ? -1 : 1) * numOf(m[4]) : 0;
  return [a, b];
}
const near = (a, b, e = 1e-9) => Math.abs(a - b) < e;
const polyArea = (pts) => { let s = 0; for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; s += p[0] * q[1] - q[0] * p[1]; } return Math.abs(s) / 2; };

try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { Btn, Ic, FrameIc } from ${F("stage-ui.jsx")};
import { FRAMES } from ${F("frames/index.js")};
import { L10Art } from ${F("frames/lin10.jsx")};
import { AreaArt } from ${F("frames/area.jsx")};
import { LessonFrame } from ${F("frames/lesson.jsx")};
import { LIN2_SPEC, MEET_SPEC, Lin2Thumb, MeetThumb } from ${F("frames/prints.jsx")};
import { dslBox, atTime, FIG_BOX } from ${F("frames/figdsl.jsx")};
export { PRINT_FRAMES, printCached, loadPrintSet, loadPrintFrame } from ${F("prints/index.js")};
export { THUMBS } from ${F("prints/thumbs.js")};
export { l10Plan } from ${F("lin10.js")};
export { AREA_SETS, arPlan, onLine } from ${F("area.js")};
export { AREA_SPEC } from ${F("frames/area.jsx")};
export { FRAMES, LIN2_SPEC, MEET_SPEC, dslBox, atTime, FIG_BOX };
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const art = (it, t, th) => svg(<L10Art it={it} t={t} C={PALETTE[th]} uid="t" />);
export const area = (it, t, th) => svg(<AreaArt it={it} t={t} C={PALETTE[th]} />);
export const thumbs = (th) => [svg(<Lin2Thumb C={PALETTE[th]} />), svg(<MeetThumb C={PALETTE[th]} />)];
const props = (th) => ({ C: PALETTE[th], ui: { Btn, Ic, FrameIc }, ctl: true, poke: () => {}, inert: false, isFs: false, toggleFs: () => {},
  onTheme: () => {}, onGallery: () => {}, onExit: () => {}, mode: "m", onMode: () => {} });
export const frame = (spec, th, pick = null) => renderToStaticMarkup(<LessonFrame spec={spec} pick={pick} {...props(th)} />);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", loader: { ".js": "jsx" },
    define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{50}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];

  await test("들여오기 전: 세트 문항이 없고 액자는 「불러오는 중」 · 들여오면 세트 문항(한 번만)", async () => {
    for (const fk of ["lin2", "meet"]) {
      const S = fk === "lin2" ? m.LIN2_SPEC : m.MEET_SPEC;
      for (const k of m.PRINT_FRAMES[fk].keys) assert.equal(S.ready(k), false, `${fk}:${k}`);
      const h = m.frame(S, "dark");
      assert.ok(h.includes("불러오는 중") && !BAD.test(h), `${fk} 「불러오는 중」`);
    }
    const a = m.loadPrintSet("meet", "tri"), b = m.loadPrintSet("meet", "tri");
    const [x, y] = await Promise.all([a, b]);
    assert.equal(x, y, "같은 세트는 한 번만");
    await m.loadPrintFrame("lin2"); await m.loadPrintFrame("meet");
    await assert.rejects(m.loadPrintSet("meet", "nope"));
  });

  const SETS = ["lin2", "meet"].flatMap((fk) => m.PRINT_FRAMES[fk].keys.map((k) => ({ fk, k, items: m.printCached(fk, k), S: m.PRINT_FRAMES[fk].sets[k] })));

  await test("문항: 세트마다 100 · 번호 1 ~ 100 · 단계(lin2 10단계 × 10 · meet 5단계 × 20) · 발문 · 방침 · 판서 · 답 · 그림", () => {
    assert.equal(SETS.length, 10);
    for (const { fk, k, items, S } of SETS) {
      assert.equal(items.length, 100, `${fk}:${k}`);
      const nst = Object.keys(S.stage).length, per = 100 / nst;
      items.forEach((it, i) => {
        const tag = `${fk}:${k} ${it.no}`;
        assert.equal(it.no, i + 1, tag);
        assert.equal(it.st, Math.floor(i / per) + 1, `${tag} 단계`);
        assert.equal(it.sub, S.stage[it.st], `${tag} 단계 이름`);
        assert.ok(it.q && it.plan && it.ans && it.lines.length >= 2 && it.lines.every((l) => l.s), `${tag} 칸`);
        assert.ok(!/√|순열|조합|여사건|배반|\d!|undefined|NaN/.test(JSON.stringify([it.q, it.plan, it.ans, it.lines])), `${tag} 글자`);
        assert.ok(it.fig && it.fig.kind === "dsl" && it.fig.els.length >= 6, `${tag} 그림`);
      });
      // 같은 발문이라도 그래프 · 표가 다르면 다른 문항(교점 활용 2단계) — 발문 + 판서로 본다.
      // 해설은 프린트 그대로 — 만날 조건 쉬운 판(N59-X84)은 1단계 5 · 14번, 7 · 11번이 같은 문제다(프린트에서 고칠 일).
      const dup = 100 - new Set(items.map((it) => it.q + it.lines.map((l) => l.s).join("|"))).size;
      assert.equal(dup, fk === "meet" && k === "mE" ? 2 : 0, `${fk}:${k} 문항 겹침`);
    }
  });

  await test("그림 DSL: 나타나는 때 · 사라지는 때 · 옮기는 때가 판서 줄 안 · 그림이 그림 칸 근처 · 꼭 보일 그림은 「다음 그래프 · 표」 문항만", () => {
    const okAt = (at, it) => at == null || at === "q" || at === "p" || at === "a" || (Number.isInteger(at) && at >= 0 && at < it.lines.length);
    let must = 0;
    for (const { fk, k, items } of SETS) for (const it of items) {
      const tag = `${fk}:${k} ${it.no}`;
      for (const el of it.fig.els) {
        assert.ok(okAt(el.at, it), `${tag} at ${el.at}`);
        if (el.un != null) assert.ok(okAt(el.un, it), `${tag} un`);
        if (el.mv) assert.ok(okAt(el.mv.at, it), `${tag} mv`);
      }
      const b = m.dslBox(it.fig), X = m.FIG_BOX;
      // 점 이름 · 좌표 글자가 칸 가장자리 밖으로 조금 나갈 수 있다(판은 그림이 실제로 차지하는 네모로 줄여 넣는다)
      assert.ok(b && b.x0 >= X.x0 - 130 && b.x1 <= X.x1 + 130 && b.y0 >= X.y0 - 90 && b.y1 <= X.y1 + 90, `${tag} 그림 칸 밖 ${b && [b.x0, b.y0, b.x1, b.y1].map(Math.round)}`);
      if (it.fig.must) { must++; assert.ok(/다음 (그래프|표)/.test(it.q), `${tag} must`); }
    }
    assert.equal(must, 40, "읽어야 하는 그래프 · 표 문항 수(교점 활용 2단계 20 · 3단계 표 10 · 4단계 같아질 때의 값 5 · 5단계 그래프 일부 5)");
  });

  await test("두 점 → 식: 발문의 두 점이 답의 직선 위 · ① 기울기 = 두 점의 증가량의 비 · 1 ~ 6쪽 정수 기울기, 7 ~ 10쪽 분수", () => {
    let cnt = 0;
    for (const { fk, k, items } of SETS.filter((x) => x.fk === "lin2")) for (const it of items) {
      const pts = [...it.q.matchAll(/\((−?\d+), (−?\d+)\)/g)].map((x) => [numOf(x[1]), numOf(x[2])]);
      assert.equal(pts.length, 2, `${k} ${it.no} 두 점`);
      const [a, b] = lineOf(it.ans);
      for (const [x, y] of pts) assert.ok(near(a * x + b, y), `${k} ${it.no} ${x}, ${y} 가 ${it.ans} 위가 아님`);
      assert.ok(near(a, (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])), `${k} ${it.no} 기울기`);
      assert.ok(it.lines[0].s.startsWith("① 기울기") && it.lines.at(-1).s === `③ ${it.ans}`, `${k} ${it.no} 판서 차례`);
      assert.equal(Number.isInteger(a), it.st <= 6, `${k} ${it.no} 정수 · 분수 기울기`);
      cnt++;
    }
    assert.equal(cnt, 500);
  });

  await test("넓이 이등분 · 넓이로 미지수(area C · D): 5단계 × 20 · 이등분 조각은 반씩(두 직사각형은 둘 다) · 발문의 넓이 = 그림의 넓이 · 점선 직선이 나타남", () => {
    const Cs = m.AREA_SETS.C.items, Ds = m.AREA_SETS.D.items;
    for (const [nm, its] of [["C", Cs], ["D", Ds]]) {
      assert.equal(its.length, 100, nm);
      its.forEach((it, i) => { assert.equal(it.no, i + 1); assert.equal(it.lv, Math.floor(i / 20) + 1, `${nm}${it.no} 단계`); assert.equal(it.sub && m.AREA_SETS[nm].stage[it.lv] ? 1 : 0, 1); });
    }
    for (const it of Cs) {
      const ops = it.lines.flatMap((l) => l.ops), pieces = ops.filter((o) => o.t === "poly");
      const shapes = [it.fig.poly, ...(it.fig.poly2 ? [it.fig.poly2] : [])];
      assert.equal(pieces.length, 2 * shapes.length, `C${it.no} 조각 수`);
      shapes.forEach((sh, j) => {
        const A = polyArea(sh);
        for (const p of pieces.slice(2 * j, 2 * j + 2)) assert.ok(near(polyArea(p.pts), A / 2, 1e-6), `C${it.no} 반쪽 ${polyArea(p.pts)} / ${A}`);
      });
      assert.ok(ops.some((o) => o.t === "reveal") && it.fig.lines.filter((l) => l.dash).length === 1, `C${it.no} 점선 직선`);
      const d = it.fig.lines.find((l) => l.dash);
      for (const p of pieces) assert.ok(p.pts.filter((q) => m.onLine(d, q, 1e-6)).length >= 2, `C${it.no} 자른 선이 점선 직선`);
    }
    for (const it of Ds) {
      if (it.kind === "D넓이비") { assert.ok(it.lines.flatMap((l) => l.ops).some((o) => o.t === "reveal"), `D${it.no} y = ax 가 나타남`); continue; }
      const mm = it.q.match(/넓이가 (\d+(?:\{\d+\/\d+\})?|\{\d+\/\d+\})(?:일 때|이다)/);
      assert.ok(mm, `D${it.no} 발문의 넓이`);
      assert.ok(near(polyArea(it.fig.poly), numOf(mm[1]), 1e-6), `D${it.no} ${polyArea(it.fig.poly)} ≠ ${mm[1]}`);
    }
  });

  await test("삼각형이 만들어지지 않을 조건(meet ntri): 모든 문항이 「만들어지지 않을」 조건 · 단계마다 답 꼴 · 1단계는 돌아서 나란해지는 직선 · 교점으로 도는 직선", () => {
    const its = m.printCached("meet", "ntri");
    assert.equal(its.length, 100);
    const vals = (a) => a.replace(/^.*?a = /, "").split(", ");
    for (const it of its) {
      const tag = `ntri ${it.no}`;
      assert.ok(it.q.includes("만들어지지 않"), `${tag} 만들어지지 않을 조건만`);
      assert.ok(!it.q.includes("만들어지도록"), `${tag} 만들어지는 조건은 묻지 않음`);
      const rot = it.fig.els.filter((e) => e.k === "L" && e.mv && e.mv.r);
      const dash = it.fig.els.filter((e) => e.k === "L" && e.d && e.c === "coral");
      if (it.st === 1) {
        assert.ok(/^a = [^,]+, [^,]+$/.test(it.ans), `${tag} 평행 값 둘 ${it.ans}`);
        assert.ok(rot.length === 2 && rot.every((e) => e.un != null), `${tag} 돌아서 나란해지는 직선 둘(다음 줄에 넘겨줌)`);
        assert.equal(dash.length, 2, `${tag} 나란해진 자리에 산호 점선 둘`);
        assert.ok(it.lines.filter((l) => /[과와] 평행: /.test(l.s)).length === 2, `${tag} 평행 줄 둘`);
      } else if (it.st === 2) {
        assert.ok(/^a = [^,]+$/.test(it.ans), `${tag} 한 점 값 하나 ${it.ans}`);
        assert.ok(it.lines.some((l) => l.s.includes("교점 (")), `${tag} 교점`);
      } else if (it.st <= 4) {
        assert.ok(/^평행 (a = .+|없음) · 한 점 (a = .+|없음)$/.test(it.ans), `${tag} 두 칸 ${it.ans}`);
        const [p, c] = it.ans.split(" · 한 점 ");
        if (!p.includes("없음") && !c.includes("없음")) {
          const pv = vals(p), cv = vals(c);
          assert.ok(cv.every((v) => !pv.includes(v)), `${tag} 평행 값과 한 점 값이 겹치지 않음`);
        }
      } else {
        assert.ok(it.no <= 90 ? /^(−?[\d{}/]+|\d+개)$/.test(it.ans) : /^a = /.test(it.ans), `${tag} 답 꼴 ${it.ans}`);
      }
      if (it.st >= 2 && !/없음/.test(it.ans.split(" · 한 점 ")[1] || "") && /y = \*?a|\*a|y = \(a|ay =|ax/.test(it.q)) {
        // 늘 지나는 점이 있는 미지수 직선은 그 점을 축으로 돌아 교점을 지난다(기울기가 정해진 직선 · x = a · y = a 는 미끄러짐)
        assert.ok(rot.length >= 1 || it.fig.els.some((e) => e.mv && (e.mv.dx || e.mv.dy)), `${tag} 움직이는 직선`);
      }
    }
    assert.ok(its.slice(70, 80).filter((it) => it.ans.includes("없음")).length >= 4, "축에 평행한 직선 쪽에 「없음」");
    assert.deepEqual([...new Set(its.slice(80, 90).map((it) => it.q.match(/(합|개수|곱)을 구하시오/)[1]))].sort(), ["개수", "곱", "합"]);
  });

  await test("액자: 세트 · 단계 · 장면 수 · 고른 세트로 열기(숫자 세트도) · 목록 그림 두 테마", () => {
    assert.deepEqual(m.LIN2_SPEC.sets.map((s) => s.key), [1, 2, 3, 4, 5]);
    assert.deepEqual(m.MEET_SPEC.sets.map((s) => s.key), ["ix", "mE", "mH", "tri", "ntri"]);
    assert.equal(m.LIN2_SPEC.stages(1).length, 10); assert.equal(m.MEET_SPEC.stages("tri").length, 5);
    assert.deepEqual(m.AREA_SPEC.sets.map((s) => s.key), ["A", "B", "C", "D"]);
    assert.equal(m.AREA_SPEC.stages("C").length, 5); assert.equal(m.AREA_SPEC.stages("A").length, 0);
    for (const [S, k, st, want] of [[m.LIN2_SPEC, 3, 7, 10], [m.MEET_SPEC, "mH", 4, 20], [m.AREA_SPEC, "D", 5, 20]]) {
      assert.equal(S.scenes(k, 1, 0).length, 100, `${S.lsk} ${k}`);
      const sc = S.scenes(k, 1, st);
      assert.ok(sc.length === want && sc.every((x) => x.st === st), `${S.lsk} ${k} ${st}단계`);
      assert.ok(Math.abs(S.scenes(k, 1.5, 0)[0].dur * 1.5 - S.scenes(k, 1, 0)[0].dur) <= 2, "1.5× 길이");
    }
    for (const th of ["dark", "light"]) {
      for (const s of m.thumbs(th)) assert.ok(s.length > 3000 && !BAD.test(s), `목록 그림 ${th}: ${bad(s)}`);
      const h2 = m.frame(m.LIN2_SPEC, th, 4), hm = m.frame(m.MEET_SPEC, th, "tri"), ha = m.frame(m.AREA_SPEC, th, "C");
      assert.ok(/aria-checked="true">4세트</.test(h2), "4세트로");
      assert.ok(/aria-checked="true">삼각형 조건</.test(hm), "삼각형 조건으로");
      assert.ok(/aria-checked="true">이등분</.test(ha), "넓이 이등분으로");
      for (const h of [h2, hm, ha]) assert.ok(!BAD.test(h) && !h.includes("불러오는 중"), bad(h));
    }
  });

  await test("그리기 훑기: 새 문항 1,200개 × (문제 · 방침 · 줄마다 · 답 · 끝) × 두 테마 — 오류 · NaN 없음", () => {
    let cnt = 0;
    for (const { fk, k, items } of SETS) for (const it of items) {
      const P = m.l10Plan(it), ts = [0, 900, P.plan[0] + 300, P.ans + 300, P.dur - 1];
      for (const L of P.lines) ts.push(L.a + 200, (L.a + L.b) / 2);
      for (const t of ts) { const s = m.art(it, t, cnt++ % 2 ? "dark" : "light"); assert.ok(!BAD.test(s), `${fk}:${k} ${it.no} t=${Math.round(t)}: ${bad(s)}`); }
    }
    for (const k of ["C", "D"]) for (const it of m.AREA_SETS[k].items) {
      const P = m.arPlan(it), ts = [0, 300, P.plan[0] + 300, P.ans + 300, P.dur - 1];
      for (const L of P.lines) ts.push(L.a + 100, L.a + 400, (L.a + L.b) / 2);
      for (const t of ts) { const s = m.area(it, t, cnt++ % 2 ? "dark" : "light"); assert.ok(!BAD.test(s), `area ${k}${it.no} t=${Math.round(t)}: ${bad(s)}`); }
    }
    console.log(`   그림 ${cnt}장`);
  });
} catch (e) {
  failed++;
  console.log("✗ 준비 실패\n  ", e.stack?.split("\n").slice(0, 4).join("\n   "));
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
