// node tests/majors.test.mjs — 시록고 서고 › 전공 수학 서가(public/majors/*.json · majorgen/ · apps/seirocco/pages/MajorMath.jsx) 검산. 실패 시 exit 1.
// 자료: 책 9권(차례가 정해져 있다) · 목록(index.json)이 책 파일과 맞는다 · 장 번호 1 … · 장마다 이론 단락과 예제 · 예제는 풀이 2줄 이상과 답.
// 글자: MathIR 표식이 모두 읽힌다(lib/mathir.js parseText — 오류가 있으면 화면에 [[…]] 가 그대로 남는다) · ** 짝 · 평문 ASCII 빼기 없음.
// 그리기: 서가 · 차례 · 모든 장(예제 · 연습은 닫힌 모양)을 그려 오류 · NaN · 남은 표식이 없다. 서고 탭 넷과 장서고의 바로 가기도 본다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseText } from "../src/lib/mathir.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const DIR = path.join(ROOT, "public/majors");
const ORDER = ["calc", "econ", "trade", "mech", "astro", "elec", "data", "phys", "stat"];
const IDX = JSON.parse(fs.readFileSync(path.join(DIR, "index.json"), "utf8"));
const BOOKS = Object.fromEntries(ORDER.map((id) => [id, JSON.parse(fs.readFileSync(path.join(DIR, `${id}.json`), "utf8"))]));
const strs = (x) => (typeof x === "string" ? [x] : Array.isArray(x) ? x.flatMap(strs)
  : x && typeof x === "object" ? Object.entries(x).filter(([k]) => !["k", "tone", "id"].includes(k)).flatMap(([, v]) => strs(v)) : []);

/* ══════════ 자료 ══════════ */
test("책 9권 · 파일은 책 + 목록뿐 · 목록이 책과 맞는다(제목 · 장 제목 · 예제 · 연습 수)", () => {
  assert.equal(IDX.v, 1);
  assert.deepEqual(IDX.books.map((b) => b.id), ORDER);
  assert.deepEqual(fs.readdirSync(DIR).sort(), [...ORDER.map((id) => `${id}.json`), "index.json"].sort());
  for (const e of IDX.books) {
    const b = BOOKS[e.id];
    assert.equal(e.title, b.title, e.id);
    assert.deepEqual(e.chapters, b.chapters.map((c) => c.title), e.id);
    const cnt = (k) => b.chapters.reduce((s, c) => s + c.blocks.filter((x) => x.k === k).length, 0);
    assert.equal(e.ex, cnt("ex"), `${e.id} 예제 수`);
    assert.equal(e.pr, cnt("pr"), `${e.id} 연습 수`);
  }
});

test("책마다 제목 · 부제 · 소개 · 대상 · 색 · 장 5 ~ 9개(번호 1 …) · 장마다 이론 단락과 예제", () => {
  let chs = 0, exs = 0;
  for (const id of ORDER) {
    const b = BOOKS[id];
    assert.equal(b.id, id);
    assert.ok(b.title && b.sub && b.intro && b.who && b.tone, id);
    assert.ok(b.chapters.length >= 5 && b.chapters.length <= 9, `${id} 장 ${b.chapters.length}`);
    b.chapters.forEach((c, i) => {
      chs++;
      assert.equal(c.n, i + 1, `${id} 장 번호`);
      assert.ok(c.title && c.sum, `${id} ${c.n}장 제목`);
      const ks = c.blocks.map((x) => x.k);
      assert.ok(ks.includes("s") && ks.includes("ex"), `${id} ${c.n}장: 이론 · 예제`);
      for (const x of c.blocks) {
        assert.ok(["s", "ex", "pr"].includes(x.k), `${id} ${c.n}장 블록 ${x.k}`);
        if (x.k === "s") assert.ok(x.h && x.p.length >= 1 && Array.isArray(x.eq), `${id} ${c.n}장 「${x.h}」`);
        if (x.k === "ex") { exs++; assert.ok(x.q && x.steps.length >= 2 && x.ans, `${id} ${c.n}장 예제`); }
        if (x.k === "pr") assert.ok(x.q && x.ans, `${id} ${c.n}장 연습`);
      }
    });
  }
  assert.ok(chs >= 50, `장 ${chs}`);
  assert.ok(exs >= 100, `예제 ${exs}`);
  console.log(`   장 ${chs} · 예제 ${exs}`);
});

test("글자: MathIR 표식이 모두 읽힌다 · ** 짝 · 평문 ASCII 빼기 · x^2 꼴 없음 · 빈 값 없음", () => {
  let marks = 0;
  for (const id of ORDER) for (const s of strs(BOOKS[id])) {
    const r = parseText(s);
    marks += r.segs.filter((x) => x.kind === "ir").length;
    assert.equal(r.errs.length, 0, `${id}: 표식 오류 ${JSON.stringify(r.errs[0])}`);
    const plain = s.replace(/\[\[[\s\S]*?\]\]/g, "");
    assert.ok(plain.split("**").length % 2 === 1, `${id} ** 짝: ${s.slice(0, 40)}`);
    assert.ok(!/(^|[\s(=,[])-\d/.test(plain) && !plain.includes(" - "), `${id} ASCII 빼기: ${s.slice(0, 50)}`);
    assert.ok(!/\^(?!\()/.test(plain), `${id} 평문 ^: ${s.slice(0, 50)}`);
    assert.ok(!/undefined|NaN|\[object/.test(s), `${id} 빈 값`);
  }
  assert.ok(marks > 150, `표식 ${marks}`);
  console.log(`   표식 ${marks}개`);
});

/* ══════════ 그리기(번들) ══════════ */
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "majors-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { richHtml, Shelf, Toc, Chapter } from ${JSON.stringify(path.join(ROOT, "src/apps/seirocco/pages/MajorMath.jsx"))};
import Seogo from ${JSON.stringify(path.join(ROOT, "src/apps/seirocco/pages/Seogo.jsx"))};
export { richHtml };
export const seogo = (p) => renderToStaticMarkup(<Seogo param={p} />);
export const shelf = (idx, read) => renderToStaticMarkup(<Shelf idx={idx} read={read} />);
export const toc = (book, read) => renderToStaticMarkup(<Toc book={book} read={read} />);
export const chapter = (book, n) => renderToStaticMarkup(<Chapter book={book} n={n} onRead={() => {}} />);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent",
    define: { "process.env.NODE_ENV": '"production"', "import.meta.env": "{}" },
    loader: { ".png": "dataurl", ".jpg": "dataurl", ".svg": "dataurl", ".webp": "dataurl", ".css": "empty" },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]|\[\[/;
  const bad = (s) => (s.match(/.{40}(NaN|undefined|Infinity|\[object Object\]|\[\[).{30}/) || [""])[0];
  // 브라우저 흉내: 주소(location.hash) — 서고 화면이 읽는다
  globalThis.location = { hash: "" };
  const at = (h) => { globalThis.location.hash = h; };

  test("richHtml: **굵게** · 분수 표식은 상하로 · 평문 1/2 도 상하로 · 꺾쇠는 이스케이프", () => {
    const s = m.richHtml("**정의** — [[frac(a,b)]] 와 1/2 그리고 <b>");
    assert.ok(s.startsWith("<b>정의</b>"), s);
    assert.equal((s.match(/class="mf"/g) || []).length, 2, s);
    assert.ok(s.includes("&lt;b&gt;"), "이스케이프");
  });

  test("서고: 탭 넷(장서고 · 문서고 · 기록고 · 전공 수학) · 전공 수학 탭이 서가를 연다(받기 전엔 불러오는 중)", () => {
    at("#/seogo/jeon");
    const s = m.seogo("jeon");
    for (const t of ["장서고", "문서고", "기록고", "전공 수학"]) assert.ok(s.includes(t), t);
    assert.ok(s.includes("서가를 불러오는 중"), "받기 전");
    assert.ok(m.seogo("jang").includes("전공 수학 서가"), "장서고의 바로 가기");
  });

  test("서가 · 차례 · 모든 장 그리기 — 오류 · NaN · 남은 표식 없음 · 예제 · 연습 단추 · 이전/다음 장", () => {
    const sh = m.shelf(IDX, { calc: [1, 2] });
    assert.ok(!BAD.test(sh), bad(sh));
    for (const b of IDX.books) assert.ok(sh.includes(b.title), b.title);
    assert.ok(sh.includes("width:28.5"), "읽은 장 막대(대학수학 2/7)");
    let cnt = 1;
    for (const id of ORDER) {
      const B = BOOKS[id];
      const st = m.toc(B, { [id]: [1] });
      assert.ok(!BAD.test(st), `${id} 차례: ${bad(st)}`);
      assert.equal((st.match(/class="mm-ch"/g) || []).length, B.chapters.length, `${id} 차례 줄`);
      cnt++;
      for (const c of B.chapters) {
        const s = m.chapter(B, c.n);
        cnt++;
        assert.ok(!BAD.test(s), `${id} ${c.n}장: ${bad(s)}`);
        const ne = c.blocks.filter((x) => x.k === "ex").length, np = c.blocks.filter((x) => x.k === "pr").length;
        assert.equal((s.match(/풀이 한 줄씩 보기/g) || []).length, ne, `${id} ${c.n}장 예제 단추`);
        assert.equal((s.match(/답 보기/g) || []).length, np, `${id} ${c.n}장 연습 단추`);
        assert.ok(c.n === B.chapters.length ? s.includes("서가로") : s.includes(`${c.n + 1}장 →`), `${id} ${c.n}장 다음`);
      }
    }
    assert.ok(cnt > 60, `그린 화면 ${cnt}`);
    console.log(`   화면 ${cnt}개`);
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
