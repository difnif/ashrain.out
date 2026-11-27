// node tests/majors.test.mjs — 시록고 서고 › 전공 수학 서가 v2(public/majors/*.json · majorgen/ · pages/MajorMath.jsx · pages/majors/anims/) 검산. 실패 시 exit 1.
// 자료: 목록(index.json v2)이 책 파일과 맞는다 · 분야 · 책 차례 · 먼저 볼 책 · 장 번호 1 … · v2 책은 장마다 목표 3 · 용어 4 · 요약 3 · 왜 · 그림 · 예제 2 · 연습 3(풀이) · 흔한 실수.
// 그림: kinds.json = anims/index.js 의 KINDS · 책이 쓰는 그림 종류가 모두 있다 · 그림마다 여러 시각(t)에 책이 주는 값으로 그려 오류 · NaN 이 없다.
// 글자: MathIR 표식이 모두 읽힌다(남은 [[…]] 없음) · ** 짝 · 평문 ASCII 빼기 · ^ · _ 없음 · 평문 분수 뒤에 위 · 아래 첨자가 붙지 않는다(1/x² 은 (1/x)² 로 보인다).
// 그리기: 서가(분야 · 처음 길 · 읽은 막대) · 찾기 · 차례(배지) · 모든 장(목표 · 용어 · 요약 · 단추 수 · 그림 자리 · 다음 장) · 서고 탭.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseText } from "../src/lib/mathir.js";
import { KINDS } from "../src/apps/seirocco/pages/majors/anims/index.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const DIR = path.join(ROOT, "public/majors");
const ANIM_DIR = path.join(ROOT, "src/apps/seirocco/pages/majors/anims");
const IDX = JSON.parse(fs.readFileSync(path.join(DIR, "index.json"), "utf8"));
const IDS = IDX.books.map((b) => b.id);
const BOOKS = Object.fromEntries(IDS.map((id) => [id, JSON.parse(fs.readFileSync(path.join(DIR, `${id}.json`), "utf8"))]));
const V2 = IDS.filter((id) => BOOKS[id].v >= 2);
const KIND_FILE = JSON.parse(fs.readFileSync(path.join(ANIM_DIR, "kinds.json"), "utf8")).kinds;
// 글자 모으기 — 그림의 값(p) · 코드 · 이름표(k · id · kind …)는 글이 아니다
const SKIP = new Set(["k", "tone", "id", "kind", "lang", "code", "field", "pre", "v"]);
const strs = (x) => (typeof x === "string" ? [x] : Array.isArray(x) ? x.flatMap(strs)
  : x && typeof x === "object" ? Object.entries(x).filter(([k, v]) => !SKIP.has(k) && !(k === "p" && !Array.isArray(v))).flatMap(([, v]) => strs(v)) : []);
const blocks = (b) => b.chapters.flatMap((c) => c.blocks);
const anims = (b) => blocks(b).filter((x) => x.k === "anim");

/* ══════════ 자료 ══════════ */
test("목록 v2 · 분야 · 파일은 책 + 목록뿐 · 목록이 책과 맞는다(제목 · 분야 · 장 제목 · 예제 · 연습 · 그림 수)", () => {
  assert.equal(IDX.v, 2);
  assert.ok(Array.isArray(IDX.fields) && IDX.fields.length >= 1, "분야");
  const fieldIds = IDX.fields.map((f) => f.id);
  assert.deepEqual(fs.readdirSync(DIR).sort(), [...IDS.map((id) => `${id}.json`), "index.json"].sort());
  for (const e of IDX.books) {
    const b = BOOKS[e.id];
    assert.equal(e.title, b.title, e.id);
    assert.equal(e.field, b.field, `${e.id} 분야`);
    assert.ok(fieldIds.includes(e.field), `${e.id} 분야 ${e.field}`);
    assert.deepEqual(e.chapters, b.chapters.map((c) => c.title), e.id);
    const cnt = (k) => blocks(b).filter((x) => x.k === k).length;
    assert.equal(e.ex, cnt("ex"), `${e.id} 예제 수`);
    assert.equal(e.pr, cnt("pr"), `${e.id} 연습 수`);
    assert.equal(e.anim, cnt("anim"), `${e.id} 그림 수`);
    for (const p of e.pre) assert.ok(IDS.includes(p), `${e.id} 먼저 볼 책 ${p}`);
  }
  // 분야 차례대로 책이 놓인다(서가가 분야별 칸으로 그린다)
  const order = IDX.books.map((b) => fieldIds.indexOf(b.field));
  assert.ok(IDX.books.length >= 9, `책 ${IDX.books.length}`);
  console.log(`   책 ${IDS.length}(v2 ${V2.length}) · 분야 ${fieldIds.join(" · ")} · 칸 차례 ${order.join("")}`);
});

test("대학수학 바탕 여섯 권(미적분학 · 다변수 · 선형대수 · 미분방정식 · 확률론 · 통계학)이 v2 로 있다", () => {
  for (const id of ["calc", "mvc", "linalg", "ode", "prob", "stat"]) {
    assert.ok(BOOKS[id], id);
    assert.equal(BOOKS[id].v, 2, `${id} v2`);
    assert.equal(BOOKS[id].field, "base", `${id} 분야`);
  }
});

test("책마다 제목 · 부제 · 소개 · 대상 · 색 · 장 5 ~ 10개(번호 1 …) · 장마다 이론 단락(또는 정의)과 예제", () => {
  let chs = 0;
  for (const id of IDS) {
    const b = BOOKS[id];
    assert.equal(b.id, id);
    assert.ok(b.title && b.sub && b.intro && b.who && b.tone, id);
    assert.ok(b.chapters.length >= 5 && b.chapters.length <= 10, `${id} 장 ${b.chapters.length}`);
    b.chapters.forEach((c, i) => {
      chs++;
      assert.equal(c.n, i + 1, `${id} 장 번호`);
      assert.ok(c.title && c.sum, `${id} ${c.n}장 제목`);
      const ks = c.blocks.map((x) => x.k);
      assert.ok((ks.includes("s") || ks.includes("def")) && ks.includes("ex"), `${id} ${c.n}장: 이론 · 예제`);
    });
  }
  assert.ok(chs >= 80, `장 ${chs}`);
});

const KNOWN = new Set(["s", "why", "def", "thm", "anim", "ex", "pr", "warn", "use", "tbl", "code"]);
test("v2 책: 장마다 목표 3 · 용어 4(우리말 · 영어 · 뜻) · 요약 3 · 왜 · 그림 · 흔한 실수 · 예제 2(풀이 2줄) · 연습 3(답 · 풀이) · 블록 꼴", () => {
  let ex = 0, pr = 0, an = 0, th = 0;
  for (const id of V2) for (const c of BOOKS[id].chapters) {
    const t = `${id} ${c.n}장`, ks = c.blocks.map((x) => x.k);
    assert.ok((c.goals || []).length >= 3, `${t} 목표`);
    assert.ok((c.terms || []).length >= 4 && c.terms.every((r) => r.length === 3 && r.every(Boolean)), `${t} 용어`);
    assert.ok((c.recap || []).length >= 3, `${t} 요약`);
    for (const k of ["why", "anim", "warn"]) assert.ok(ks.includes(k), `${t} ${k}`);
    assert.ok(ks.filter((k) => k === "ex").length >= 2, `${t} 예제 2`);
    assert.ok(ks.filter((k) => k === "pr").length >= 3, `${t} 연습 3`);
    for (const x of c.blocks) {
      assert.ok(KNOWN.has(x.k), `${t} 블록 ${x.k}`);
      if (x.k === "ex") { ex++; assert.ok(x.q && x.steps.length >= 2 && x.ans, `${t} 예제`); }
      if (x.k === "pr") { pr++; assert.ok(x.q && x.ans && (x.sol || []).length >= 1, `${t} 연습 풀이 — ${x.q.slice(0, 30)}`); }
      if (x.k === "anim") { an++; assert.ok(x.h && x.cap && x.p && typeof x.p === "object" && !Array.isArray(x.p), `${t} 그림 꼴`); }
      if (x.k === "thm") { th++; assert.ok(x.name && x.stmt && Array.isArray(x.proof), `${t} 정리`); }
      if (x.k === "def") assert.ok(x.term && x.en && x.p.length, `${t} 정의`);
      if (x.k === "warn") assert.ok(x.items.length >= 2, `${t} 흔한 실수 2개 이상`);
      if (x.k === "tbl") assert.ok(x.rows.length && x.rows.every((r) => r.length === x.head.length), `${t} 표 칸 수`);
    }
  }
  assert.ok(ex >= 90 && pr >= 130 && an >= 60, `예제 ${ex} · 연습 ${pr} · 그림 ${an}`);
  console.log(`   v2 — 예제 ${ex} · 연습 ${pr} · 그림 ${an} · 정리 ${th}`);
});

/* ══════════ 그림 목록 ══════════ */
test("그림 종류: kinds.json = KINDS · 책이 쓰는 종류가 모두 있다 · 묶음 파일이 내보낸 이름이 있다", () => {
  assert.deepEqual([...KIND_FILE].sort(), Object.keys(KINDS).sort());
  const used = new Set(IDS.flatMap((id) => anims(BOOKS[id]).map((x) => x.kind)));
  for (const k of used) assert.ok(KINDS[k], `없는 그림 ${k}`);
  for (const [k, [mod, name]] of Object.entries(KINDS)) {
    const src = fs.readFileSync(path.join(ANIM_DIR, `${mod}.jsx`), "utf8");
    assert.ok(new RegExp(`export function ${name}\\b`).test(src), `${k} → ${mod}.${name}`);
  }
  console.log(`   그림 ${Object.keys(KINDS).length}종 · 책이 쓰는 것 ${used.size}종`);
});

/* ══════════ 글자 ══════════ */
const TOK = "(?:\\([^()\\n]{1,40}\\)|\\d+(?:\\.\\d+)?[A-Za-zπ]?|[A-Za-z]|\\d*π)";
const TAIL = new RegExp(`(^|[^\\wπ)\\]])(${TOK})/(${TOK})([²³⁴⁵⁶⁷⁸⁹ⁿˣʸᵏᵖ⁻¹⁰₀-₉ₙₖᵢⱼ!′])`, "g");
test("글자: 표식이 모두 읽힌다 · ** 짝 · ASCII 빼기 · ^ · _ · 빈 값 없음 · 평문 분수 뒤 첨자 없음", () => {
  let marks = 0;
  for (const id of IDS) for (const s of strs(BOOKS[id])) {
    const r = parseText(s);
    marks += r.segs.filter((x) => x.kind === "ir").length;
    assert.equal(r.errs.length, 0, `${id}: 표식 오류 ${JSON.stringify(r.errs[0])}`);
    const plain = s.replace(/\[\[[\s\S]*?\]\]/g, "  ");
    assert.ok(plain.split("**").length % 2 === 1, `${id} ** 짝: ${s.slice(0, 40)}`);
    assert.ok(!/(^|[\s(=,[])-\d/.test(plain) && !plain.includes(" - "), `${id} ASCII 빼기: ${s.slice(0, 50)}`);
    assert.ok(!/\^(?!\()/.test(plain), `${id} 평문 ^: ${s.slice(0, 50)}`);
    assert.ok(!/[A-Za-z0-9)]_[A-Za-z0-9{(]/.test(plain), `${id} 평문 _: ${s.slice(0, 50)}`);
    assert.ok(!/undefined|NaN|\[object/.test(s), `${id} 빈 값`);
    TAIL.lastIndex = 0;
    let m;
    while ((m = TAIL.exec(plain))) {
      if (/[가-힣]/.test(m[2] + m[3]) || (/^[A-Za-z]$/.test(m[2]) && /^[A-Za-z]$/.test(m[3]))) continue;
      assert.fail(`${id} 평문 분수 뒤 첨자 「${m[0].trim()}」 — ${s.slice(0, 50)}`);
    }
  }
  assert.ok(marks > 700, `표식 ${marks}`);
  console.log(`   표식 ${marks}개`);
});

/* ══════════ 그리기(번들) ══════════ */
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "majors-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const mods = [...new Set(Object.values(KINDS).map(([m]) => m))];
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { richHtml, Shelf, Toc, Chapter, searchBooks } from ${JSON.stringify(path.join(ROOT, "src/apps/seirocco/pages/MajorMath.jsx"))};
import Seogo from ${JSON.stringify(path.join(ROOT, "src/apps/seirocco/pages/Seogo.jsx"))};
${mods.map((m) => `import * as M_${m} from ${JSON.stringify(path.join(ANIM_DIR, `${m}.jsx`))};`).join("\n")}
const MODS = { ${mods.map((m) => `${m}: M_${m}`).join(", ")} };
export { richHtml, searchBooks };
export const seogo = (p) => renderToStaticMarkup(<Seogo param={p} />);
export const shelf = (idx, read) => renderToStaticMarkup(<Shelf idx={idx} read={read} />);
export const toc = (book, read, idx) => renderToStaticMarkup(<Toc book={book} read={read} idx={idx} />);
export const chapter = (book, n) => renderToStaticMarkup(<Chapter book={book} n={n} onRead={() => {}} />);
export const anim = (mod, name, p) => { const C = MODS[mod][name]; return renderToStaticMarkup(<C p={p} />); };
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
  globalThis.location = { hash: "" };
  const at = (h) => { globalThis.location.hash = h; };

  test("richHtml: **굵게** · 분수 표식은 상하로 · 평문 1/2 도 상하로 · 꺾쇠는 이스케이프", () => {
    const s = m.richHtml("**정의** — [[frac(a,b)]] 와 1/2 그리고 <b>");
    assert.ok(s.startsWith("<b>정의</b>"), s);
    assert.equal((s.match(/class="mf"/g) || []).length, 2, s);
    assert.ok(s.includes("&lt;b&gt;"), "이스케이프");
  });

  test("그림: 52종 모두 — 값 없이 · 책이 주는 값으로, 여러 시각(t)에서 그려 오류 · NaN · Infinity 없음", () => {
    const params = {};
    for (const id of IDS) for (const x of anims(BOOKS[id])) (params[x.kind] ||= []).push(x.p);
    let shots = 0;
    for (const [k, [mod, name]] of Object.entries(KINDS)) {
      const sets = [{}, ...(params[k] || [])];
      for (const p of sets) for (const t of [0, 0.7, 2.3, 4.1, 5.9, 7.7, 9.3, 11.6, 23]) {
        globalThis.__MA_T0 = t;
        let s;
        try { s = m.anim(mod, name, p); } catch (e) { assert.fail(`${k} ${JSON.stringify(p)} t=${t}: ${e.message}`); }
        shots++;
        assert.ok(s.includes("<svg"), `${k} svg`);
        assert.ok(!/NaN|undefined|Infinity|\[object/.test(s), `${k} ${JSON.stringify(p)} t=${t}: ${(s.match(/.{30}(NaN|undefined|Infinity|\[object).{20}/) || [""])[0]}`);
      }
    }
    globalThis.__MA_T0 = undefined;
    console.log(`   그림 그리기 ${shots}번`);
  });

  test("서고: 탭 넷(장서고 · 문서고 · 기록고 · 전공 수학) · 전공 수학 탭이 서가를 연다(받기 전엔 불러오는 중) · 장서고 바로 가기", () => {
    at("#/seogo/jeon");
    const s = m.seogo("jeon");
    for (const t of ["장서고", "문서고", "기록고", "전공 수학"]) assert.ok(s.includes(t), t);
    assert.ok(s.includes("서가를 불러오는 중"), "받기 전");
    assert.ok(m.seogo("jang").includes("전공 수학 서가"), "장서고의 바로 가기");
  });

  test("서가: 분야 칸 · 모든 책 · 처음 길(미적분학 → … → 통계학) · 찾기 칸 · 읽은 막대", () => {
    const sh = m.shelf(IDX, { calc: [1, 2] });
    assert.ok(!BAD.test(sh), bad(sh));
    for (const f of IDX.fields) assert.ok(sh.includes(f.title), `분야 ${f.title}`);
    for (const b of IDX.books) assert.ok(sh.includes(b.title), b.title);
    assert.ok(sh.includes("처음이라면"), "처음 길");
    assert.ok(sh.includes("mm-find"), "찾기 칸");
    const w = (100 * 2) / BOOKS.calc.chapters.length;
    assert.ok(sh.includes(`width:${w}%`), `읽은 장 막대(미적분학 2/${BOOKS.calc.chapters.length})`);
  });

  test("찾기: 책 제목 · 장 제목 · 용어(우리말 · 영어) · 없는 말", () => {
    const hit = (q) => m.searchBooks(IDX, q) || [];
    assert.ok(hit("선형대수").some((f) => f.b.id === "linalg" && f.n === 0), "책 제목");
    assert.ok(hit("라플라스").some((f) => f.b.id === "ode" && f.n > 0), "장 제목");
    assert.ok(hit("eigenvalue").some((f) => f.b.id === "linalg"), "영어 용어");
    assert.ok(hit("고윳값").some((f) => f.b.id === "linalg"), "우리말 용어");
    assert.equal(hit("ㅁㄴㅇㄹ없는말").length, 0, "없는 말");
    assert.equal(m.searchBooks(IDX, "   "), null, "빈 찾기 = 서가");
  });

  test("차례: 줄 수 · 읽은 장 · 배지(그림 · 예제 · 연습) · 먼저 볼 책 단추 · 오류 없음", () => {
    for (const id of IDS) {
      const B = BOOKS[id], st = m.toc(B, { [id]: [1] }, IDX);
      assert.ok(!BAD.test(st), `${id} 차례: ${bad(st)}`);
      assert.equal((st.match(/class="mm-ch"/g) || []).length, B.chapters.length, `${id} 차례 줄`);
      assert.equal((st.match(/class="mm-no on"/g) || []).length, 1, `${id} 읽은 장`);
      if (B.v >= 2) assert.ok(st.includes("🎬"), `${id} 그림 배지`);
      for (const p of B.pre || []) assert.ok(st.includes(BOOKS[p].title), `${id} 먼저 볼 책 ${p}`);
    }
  });

  test("모든 장 그리기 — 오류 · NaN · 남은 표식 없음 · 목표 · 용어 · 요약 · 예제 · 연습 · 증명 단추 · 그림 자리 · 이전/다음 장", () => {
    let cnt = 0;
    for (const id of IDS) {
      const B = BOOKS[id];
      for (const c of B.chapters) {
        const s = m.chapter(B, c.n);
        cnt++;
        assert.ok(!BAD.test(s), `${id} ${c.n}장: ${bad(s)}`);
        const k = (kk) => c.blocks.filter((x) => x.k === kk);
        assert.equal((s.match(/풀이 한 줄씩 보기/g) || []).length, k("ex").length, `${id} ${c.n}장 예제 단추`);
        assert.equal((s.match(/답 보기/g) || []).length, k("pr").length, `${id} ${c.n}장 연습 단추`);
        assert.equal((s.match(/풀이 보기/g) || []).length, k("pr").filter((x) => (x.sol || []).length).length, `${id} ${c.n}장 풀이 단추`);
        assert.equal((s.match(/증명 보기/g) || []).length, k("thm").filter((x) => x.proof.length).length, `${id} ${c.n}장 증명 단추`);
        assert.equal((s.match(/움직이는 그림을 불러오는 중/g) || []).length, k("anim").length, `${id} ${c.n}장 그림 자리`);
        if (B.v >= 2) for (const t of ["이 장의 목표", "용어", "한 장 요약", "흔한 실수", "왜 그럴까"]) assert.ok(s.includes(t), `${id} ${c.n}장 ${t}`);
        assert.ok(c.n === B.chapters.length ? s.includes("서가로") : s.includes(`${c.n + 1}장 →`), `${id} ${c.n}장 다음`);
        if (c.n > 1) assert.ok(s.includes(`← ${c.n - 1}장`), `${id} ${c.n}장 이전`);
      }
    }
    assert.ok(cnt >= 80, `그린 장 ${cnt}`);
    console.log(`   장 ${cnt}개`);
  });

  test("없는 장 · 없는 번호는 안내만", () => {
    const s = m.chapter(BOOKS.calc, 99);
    assert.ok(s.includes("없는 장"), s.slice(0, 80));
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
