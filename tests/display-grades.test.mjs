// node tests/display-grades.test.mjs — 학년별 기본기 해설(초1 ~ 고3, frames/grade.jsx · grades/*.js) 검산. 실패 시 exit 1.
// 자료: 학년마다 세트 둘 · 세트마다 100문항(1 ~ 5단계 20문항씩, 번호 차례) · 프린트 코드(6글자, 겹치지 않음) · 단계 이름 · 요령 · 도움말.
// 판서: 수만 있는 「=」 줄(분수 {a/b} · 거듭제곱 ^{n} · 괄호 · + − × ÷ · 나머지 … )을 이 파일의 분수 계산기로 다시 계산한다
//       (생성기의 sympy 검산과 다른 두 번째 계산 — 문자가 든 줄은 생성기 검산만).
// 그리기: 2400문항을 다 푼 순간(어둠) · 문제 순간 · 중간(밝음)으로 그려 오류 · NaN 이 없는지, 글자 판이 무대 안인지, 그림 좌표가 그림 칸 안인지.
// 문서: 문제지 · 해설지 · 빠른 정답 HTML(frames/avprint.js)과 OMR 카드(4쪽 이하) · 등록 정보(ashrain-print.json)의 문항 · 쪽.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { GRADES, GRADE_KEYS } from "../src/features/display/grades/index.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}
const DATA = {};
for (const k of GRADE_KEYS) DATA[k] = (await import(`../src/features/display/grades/${k}.js`)).SETS;
const ALL = GRADES.flatMap((g) => g.sets.map((meta) => ({ g, meta, set: DATA[g.key][meta.key] })));

/* ══════════ 자료 ══════════ */
test("학년 열둘(초1 ~ 고3) · 학년마다 세트 둘 · 학교급 · 아이콘 · 제목 · 설명", () => {
  assert.deepEqual(GRADE_KEYS, ["e1", "e2", "e3", "e4", "e5", "e6", "m1", "m2", "m3", "h1", "h2", "h3"]);
  assert.deepEqual(GRADES.map((g) => g.grade), ["초1", "초2", "초3", "초4", "초5", "초6", "중1", "중2", "중3", "고1", "고2", "고3"]);
  for (const g of GRADES) {
    assert.equal(g.level, g.grade[0] === "초" ? "초등" : g.grade[0] === "중" ? "중등" : "고등", g.key);
    assert.ok(g.icon && g.title.startsWith(g.grade) && g.desc.length > 20, g.key);
    assert.deepEqual(g.sets.map((s) => s.key), ["a", "b"], g.key);
  }
});
test("세트마다 100문항 · 번호 1 ~ 100 · 단계 1 ~ 5 가 20문항씩 차례로 · 문항 칸이 다 있다", () => {
  for (const { g, meta, set } of ALL) {
    const tag = `${g.key}/${meta.key}`;
    assert.equal(set.items.length, 100, tag);
    assert.equal(meta.n, 100, tag);
    set.items.forEach((it, i) => {
      assert.equal(it.no, i + 1, tag);
      assert.equal(it.st, Math.floor(i / 20) + 1, `${tag} ${it.no} 단계`);
      assert.ok(it.q && it.ans && it.plan && it.lines.length >= 1 && it.ap, `${tag} ${it.no} 빈 칸`);
      assert.ok(["num", "ex", "pt"].includes(it.omr), `${tag} ${it.no} omr ${it.omr}`);
      for (const ln of it.lines) assert.ok(typeof ln.s === "string" && ln.s.length, `${tag} ${it.no} 판서 줄`);
      assert.ok(!/undefined|NaN|None|\[object/.test(JSON.stringify(it)), `${tag} ${it.no} 글자에 undefined · NaN · None`);
    });
    assert.equal(new Set(set.items.map((it) => it.q)).size, 100, `${tag} 같은 발문`);
  }
});
test("단계 이름 · 요령(1 ~ 5단계) · 지도 도움말 · 한 쪽 문항 수 · 프린트 코드(6글자 · 헷갈리는 글자 없음 · 겹치지 않음)", () => {
  const codes = new Set();
  for (const { g, meta, set } of ALL) {
    const tag = `${g.key}/${meta.key}`;
    for (let st = 1; st <= 5; st++) {
      assert.ok(meta.stages[st], `${tag} ${st}단계 이름`);
      assert.ok(set.tips[st], `${tag} ${st}단계 요령`);
    }
    assert.ok(set.note.length > 30, `${tag} 도움말`);
    assert.ok([6, 8, 10, 20].includes(set.pp), `${tag} pp ${set.pp}`);
    assert.match(meta.code, /^[23456789ABCDEFGHJKMNPQRSTUVWXYZ]{6}$/, tag);
    assert.ok(!codes.has(meta.code), `${tag} 코드 겹침`);
    codes.add(meta.code);
  }
});

/* ══════════ 판서 다시 계산 (수만 있는 줄) ══════════ */
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
const Q = (p, q = 1) => { if (q < 0) { p = -p; q = -q; } const d = gcd(p, q); return { p: p / d, q: q / d }; };
const add = (a, b) => Q(a.p * b.q + b.p * a.q, a.q * b.q);
const mul = (a, b) => Q(a.p * b.p, a.q * b.q);
const div = (a, b) => { if (b.p === 0) throw new Error("0으로 나눔"); return Q(a.p * b.q, a.q * b.p); };
function pow(a, k) {
  if (k.q !== 1) throw new Error("분수 지수");
  let r = Q(1), e = Math.abs(k.p);
  if (e > 40) throw new Error("큰 지수");
  for (let i = 0; i < e; i++) r = mul(r, a);
  return k.p < 0 ? div(Q(1), r) : r;
}
/** 수만 있는 식 → 분수 (못 읽으면 null) — 분수 {a/b} · 거듭제곱 ^{n} · 괄호 · + − × ÷ · 소수 · 곱 생략 2(3) */
function numVal(src) {
  const s = String(src).replace(/(?<=\d),(?=\d{3}(?!\d))/g, "").replace(/−/g, "-").replace(/\s+/g, "");
  if (!s || !/^[\d+\-×÷().{}/^]+$/.test(s) || !/\d/.test(s)) return null;
  let i = 0;
  const peek = () => s[i];
  const sub = (str) => { const v = numVal(str); if (!v) throw new Error("식"); return v; };
  function grab(open, close) {
    let d = 0, j = i;
    for (; j < s.length; j++) { if (s[j] === open) d++; else if (s[j] === close && --d === 0) break; }
    if (j >= s.length) throw new Error("괄호");
    const inner = s.slice(i + 1, j);
    i = j + 1;
    return inner;
  }
  function atom() {
    const c = peek();
    let v;
    if (c === "(") v = sub(grab("(", ")"));
    else if (c === "{") {
      const inner = grab("{", "}");
      let d = 0, k = -1;
      for (let j = 0; j < inner.length; j++) { if (inner[j] === "{") d++; else if (inner[j] === "}") d--; else if (inner[j] === "/" && d === 0) { k = j; break; } }
      if (k < 0) throw new Error("분수");
      v = div(sub(inner.slice(0, k)), sub(inner.slice(k + 1)));
    } else if (c && /\d/.test(c)) {
      let j = i;
      while (j < s.length && /[\d.]/.test(s[j])) j++;
      const t = s.slice(i, j);
      i = j;
      if (t.includes(".")) { const [x, y] = t.split("."); v = Q(Number(x + y), 10 ** y.length); } else v = Q(Number(t));
      if (peek() === "{" && !t.includes(".")) v = add(v, atom());     // 대분수 1{1/12} = 1 + {1/12} (곱이 아니다)
    } else throw new Error(`읽을 수 없음 ${c}`);
    while (peek() === "^") { i++; if (peek() !== "{") throw new Error("지수"); v = pow(v, sub(grab("{", "}"))); }
    return v;
  }
  function unary() { if (peek() === "-") { i++; return mul(Q(-1), unary()); } if (peek() === "+") { i++; return unary(); } return atom(); }
  function term() {
    let v = unary();
    for (;;) {
      const c = peek();
      if (c === "×") { i++; v = mul(v, unary()); } else if (c === "÷") { i++; v = div(v, unary()); }
      else if (c === "(" || c === "{") v = mul(v, atom());
      else return v;
    }
  }
  function expr() {
    let v = term();
    for (;;) { const c = peek(); if (c === "+") { i++; v = add(v, term()); } else if (c === "-") { i++; v = add(v, mul(Q(-1), term())); } else return v; }
  }
  try { const v = expr(); return i === s.length ? v : null; } catch { return null; }
}
const eq = (a, b) => a.p === b.p && a.q === b.q;

let checks = 0;
test("판서의 수 계산(분수 · 거듭제곱 · 괄호 · 나머지) — 「=」로 이은 쪽이 모두 같다", () => {
  const bad = [];
  for (const { g, meta, set } of ALL) {
    for (const it of set.items) {
      for (const ln of [...it.lines.map((l) => l.s), it.plan]) {
        for (const m of ln.matchAll(/(\d+) ÷ (\d+) = (\d+) … (\d+)/g)) {
          const [a, b, q, r] = m.slice(1).map(Number);
          checks++;
          if (!(a === b * q + r && r >= 0 && r < b)) bad.push(`${g.key}/${meta.key} ${it.no}: ${m[0]}`);
        }
        for (const part of ln.split(/→|⇒|, (?=[^)]*(?:\(|$))/)) {
          if (part.includes("…") || part.includes("≠")) continue;
          const sides = part.split("=").map((x) => x.split(/<|>|≤|≥/)[0]);
          if (sides.length < 2) continue;
          const vals = sides.map((x) => { const t = x.match(/[가-힣][^가-힣]*$/) ? x.slice(x.search(/[^가-힣]*$/)) : x; return numVal(t.trim()); });
          for (let k = 0; k + 1 < vals.length; k++) {
            if (!vals[k] || !vals[k + 1]) continue;
            checks++;
            if (!eq(vals[k], vals[k + 1])) bad.push(`${g.key}/${meta.key} ${it.no}: ${part.trim()}`);
          }
        }
      }
    }
  }
  assert.equal(bad.length, 0, bad.slice(0, 8).join("\n   "));
  assert.ok(checks > 2000, `다시 계산한 등식이 너무 적다 (${checks})`);
});

/* ══════════ 그리기 훑기(번들) ══════════ */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-grades-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { l10Plan } from ${F("lin10.js")};
import { L10Art, layoutOf } from ${F("frames/lin10.jsx")};
import { STAGE_REGION as L10_BOX } from ${F("board.js")};
import { FigDsl } from ${F("frames/figdsl.jsx")};
import { gradeScenes, GradeThumb, GRADE_LABS } from ${F("frames/grade.jsx")};
import { DocsMenu, AV_DOCS, avDownloadName, avFileBase } from ${F("frames/docsmenu.jsx")};
import { avDocHtml, avManifest, avCard, problemPages, mathHtml } from ${F("frames/avprint.js")};
import { PRINT_C } from ${F("frames/avfig.jsx")};
import { FRAMES } from ${F("frames/index.js")};
import { AV_ITEMS, avOfCat } from ${JSON.stringify(path.join(ROOT, "src/lib/av.js"))};
export { l10Plan, layoutOf, L10_BOX, gradeScenes, GRADE_LABS, AV_DOCS, avDownloadName, avFileBase, avDocHtml, avManifest, avCard, problemPages, mathHtml, FRAMES, AV_ITEMS, avOfCat };
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const art = (it, t, th) => svg(<L10Art it={it} t={t} C={PALETTE[th]} />);
export const thumb = (k, th) => svg(<GradeThumb gkey={k} C={PALETTE[th]} />);
export const scene = (sc, t, th) => svg(sc.render("m", t, PALETTE[th]));
export const figPrint = (it, when) => { const P = l10Plan(it); const t = when === "q" ? P.plan[0] - 1 : P.ans + 5000;
  return renderToStaticMarkup(<svg viewBox="880 170 660 680"><FigDsl it={it} t={t} C={PRINT_C} /></svg>); };
export const docsMenu = (g, meta, set) => renderToStaticMarkup(<DocsMenu g={g} meta={meta} set={set} open onOpen={() => {}} poke={() => {}} />);
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

  test("목록: 액자 열둘이 해설(lesson)로 · 학생앱 문제 풀이 해설은 초1 → 고3 차례(같은 학년은 원래 차례) · 액자 무대에 열둘", () => {
    for (const k of GRADE_KEYS) {
      const f = m.FRAMES.find((x) => x.key === k);
      assert.ok(f && f.lesson && f.grade && f.level, k);
      assert.ok(m.GRADE_LABS[k], `${k} 액자 무대`);
    }
    const sol = m.avOfCat("sol");
    const ORDER = ["초1", "초2", "초3", "초4", "초5", "초6", "중1", "중2", "중3", "고1", "고2", "고3"];
    const ranks = sol.map((x) => ORDER.indexOf(x.grade));
    assert.ok(ranks.every((r) => r >= 0), "학년 없는 해설");
    assert.deepEqual([...ranks].sort((a, b) => a - b), ranks, "학년 차례");
    assert.deepEqual(sol.filter((x) => x.grade === "중2").map((x) => x.key), ["graph", "lin10", "area", "cnt100", "m2"]);
    assert.equal(sol.length, 16);
  });

  test("판 짜기: 2400문항 모두 글자 판이 무대 안(아래로 · 오른쪽으로 넘치지 않음)", () => {
    const B = m.L10_BOX;
    for (const { g, meta, set } of ALL) for (const it of set.items) {
      const L = m.layoutOf(it), tag = `${g.key}/${meta.key} ${it.no}`;
      if (it.fig) assert.equal(L.noFig, false, `${tag} 글자를 다 놓고 남은 자리에 그림이 들어가지 않는다`);
      assert.ok(!L.scroll && L.bottom <= B.bottom + 1, `${tag} 아래로 넘침 (${Math.round(L.bottom)})`);
      for (const r of L.rows) for (const q of r.parts) assert.ok(q.x + q.w <= B.right + 2, `${tag} 줄이 오른쪽으로 넘침`);
    }
  });

  test("그림 좌표: 요소마다 수 · 그림 칸(660 × 680) 안(여유 40) · 나타나는 때가 문항의 줄 안", () => {
    const NUM = ["x", "y", "x2", "y2", "w", "h", "r"];
    for (const { g, meta, set } of ALL) for (const it of set.items) {
      if (!it.fig) continue;
      const tag = `${g.key}/${meta.key} ${it.no}`;
      assert.equal(it.fig.kind, "dsl", tag);
      for (const el of it.fig.els) {
        for (const k of NUM) if (el[k] != null) assert.ok(Number.isFinite(el[k]), `${tag} ${el.k}.${k}`);
        if (el.k !== "A" && el.x != null) assert.ok(el.x >= -40 && el.x <= 700, `${tag} ${el.k} x ${el.x}`);
        if (el.k !== "A" && el.y != null) assert.ok(el.y >= -40 && el.y <= 720, `${tag} ${el.k} y ${el.y}`);
        if (el.pts) for (const [px, py] of el.pts) assert.ok(px >= -40 && px <= 700 && py >= -40 && py <= 720, `${tag} P (${px}, ${py})`);
        for (const at of [el.at, el.un, el.mv?.at]) if (Number.isInteger(at)) assert.ok(at < it.lines.length, `${tag} at ${at} ≥ 줄 수`);
      }
    }
  });

  test("그리기 훑기: 2400문항 다 푼 순간(어둠) · 600문항 문제 · 중간 순간(밝음) — 오류 · NaN 없음", () => {
    let k = 0;
    for (const { g, meta, set } of ALL) for (const it of set.items) {
      const P = m.l10Plan(it), tag = `${g.key}/${meta.key} ${it.no}`;
      const s = m.art(it, P.ans + 900, "dark");
      assert.ok(s.length > 800 && !BAD.test(s), `${tag}: ${bad(s)}`);
      if (k++ % 4 === 0) for (const t of [1500, P.lines[Math.floor(P.lines.length / 2)].a + 300]) {
        const s2 = m.art(it, t, "light");
        assert.ok(s2.length > 300 && !BAD.test(s2), `${tag} @${t}: ${bad(s2)}`);
      }
    }
  });

  test("장면 목록 · 목록 그림: 세트마다 100장면(단계를 고르면 20) · 1.5× 는 길이 2/3 · 학년마다 목록 그림", () => {
    for (const g of GRADES) {
      for (const meta of g.sets) {
        const all = m.gradeScenes(g, DATA[g.key], meta.key, 1, 0), fast = m.gradeScenes(g, DATA[g.key], meta.key, 1.5, 0);
        assert.equal(all.length, 100);
        for (const sc of all) {           // 두 막대: 단계 눈금(grp) · 풀이 눈금(문제 · 방침 · 판서 줄 · 답 — 차례대로, 장면 안)
          assert.equal(sc.grp, `${sc.st}단계`);
          assert.ok(sc.marks.length >= 4 && sc.marks[0].lab === "문제" && sc.marks.at(-1).lab === "답", `${g.key}/${meta.key} ${sc.no} 눈금`);
          for (let i = 1; i < sc.marks.length; i++) assert.ok(sc.marks[i].t > sc.marks[i - 1].t && sc.marks[i].t < sc.dur, `${g.key}/${meta.key} ${sc.no} 눈금 차례`);
        }
        assert.equal(m.gradeScenes(g, DATA[g.key], meta.key, 1, 3).length, 20);
        assert.ok(Math.abs(fast[7].dur - all[7].dur / 1.5) <= 1);
        const s = m.scene(all[41], all[41].dur - 10, "dark");
        assert.ok(!BAD.test(s), `${g.key}/${meta.key}: ${bad(s)}`);
      }
      for (const th of ["dark", "light"]) {
        const s = m.thumb(g.key, th);
        assert.ok(s.length > 1500 && !BAD.test(s), `${g.key} 목록 그림 ${th}`);
      }
    }
  });

  test("문서: 문제지(단계마다 새 쪽 · 쪽마다 pp) · 해설지 · 빠른 정답 HTML — 100문항 · 코드 · @ashrain.out · 흑백 그림", () => {
    for (const { g, meta, set } of ALL) {
      const tag = `${g.key}/${meta.key}`, code = `${meta.code.slice(0, 3)}-${meta.code.slice(3)}`;
      const P = m.avDocHtml(g, meta, set, "problems", m.figPrint), S = m.avDocHtml(g, meta, set, "solutions", m.figPrint), A = m.avDocHtml(g, meta, set, "answers");
      for (const [nm, h] of [["문제지", P], ["해설지", S], ["빠른 정답", A]]) {
        const body = h.replace(/<style[\s\S]*?<\/style>/g, "");
        assert.ok(!BAD.test(body), `${tag} ${nm}: ${bad(body)}`);
        assert.ok(h.includes(`코드 ${code}`) && h.includes("@ashrain.out"), `${tag} ${nm} 코드 · 문구`);
      }
      assert.equal((P.match(/<div class="q">/g) || []).length, 100, `${tag} 문제 칸`);
      assert.equal((P.match(/<section class="pg">/g) || []).length, m.problemPages(set).length, `${tag} 쪽`);
      assert.equal((S.match(/<div class="s[ "]/g) || []).length, 100, `${tag} 해설 칸`);
      assert.equal((A.match(/<span class="no">/g) || []).length, 100, `${tag} 정답 칸`);
      assert.equal((S.match(/<svg/g) || []).length, set.items.filter((it) => it.fig).length, `${tag} 해설 그림 수`);
      assert.equal((P.match(/<svg/g) || []).length, set.items.filter((it) => it.qf).length, `${tag} 문제 그림 수`);
      assert.ok(!/#F2877B|#6BD3C3|#F4C65A|#C34E3E|#13877A/i.test(S), `${tag} 해설 그림에 화면 색이 남음`);
    }
  });

  test("등록 정보(ashrain-print.json) · OMR 카드(4쪽 이하) · 받는 파일 이름", () => {
    for (const { g, meta, set } of ALL) {
      const tag = `${g.key}/${meta.key}`;
      const man = m.avManifest(g, meta, set);
      assert.equal(man.kind, "ashrain.print");
      assert.equal(man.code, meta.code);
      assert.equal(man.items.length, 100);
      const np = m.problemPages(set).length;
      man.items.forEach((x, i) => {
        assert.equal(x.no, String(i + 1));
        assert.ok(x.answer && !x.answer.includes("−") && x.page >= 1 && x.page <= np && x.key === `av/${g.key}/${meta.key}/${i + 1}`, `${tag} ${x.no}`);
      });
      const card = m.avCard(g, meta, set.items);
      assert.ok(card.pages.length >= 1 && card.pages.length <= 4, `${tag} OMR ${card.pages.length}쪽`);
      assert.equal(card.pages.reduce((a, p) => a + p.blocks.length, 0), 100, `${tag} OMR 칸`);
      assert.equal(m.avDownloadName(g, meta, "problems"), `${m.avFileBase(g, meta)}-문제지.pdf`);
      assert.ok(!/[\s·/\\:*?"<>|]/.test(m.avFileBase(g, meta)), m.avFileBase(g, meta));
    }
    assert.deepEqual(m.AV_DOCS.map((d) => d.id), ["problems", "solutions", "answers", "omr"]);
  });

  test("수식 글자 → HTML: 분수 · 위 · 아래 첨자 · 근호 · 이탤릭 · 강조", () => {
    assert.equal(m.mathHtml("{3/4}"), '<span class="fr"><span class="n">3</span><span class="d">4</span></span>');
    assert.equal(m.mathHtml("x^{2}"), '<i class="mi">x</i><sup>2</sup>');
    assert.equal(m.mathHtml("_{5}C_{2}"), "<sub>5</sub>C<sub>2</sub>");
    assert.equal(m.mathHtml("√{x + 1}"), '<span class="rt">√<span class="rb"><i class="mi">x</i> + 1</span></span>');
    assert.equal(m.mathHtml("‹답›"), "<b>답</b>");
    assert.equal(m.mathHtml("a < b & c"), '<i class="mi">a</i> &lt; <i class="mi">b</i> &amp; <i class="mi">c</i>');
  });

  test("📄 문서 단추: 펼치면 문제지 · 해설지 · 빠른 정답 · OMR 고르기와 확인", () => {
    const { g, meta, set } = ALL[0];
    const s = m.docsMenu(g, meta, set);
    for (const w of ["문제지", "해설지", "빠른 정답", "OMR", "확인"]) assert.ok(s.includes(w), w);
    assert.ok(!BAD.test(s));
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과 · 다시 계산한 등식 ${checks}개`);
if (failed) process.exit(1);
