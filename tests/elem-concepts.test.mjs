// node tests/elem-concepts.test.mjs — 기본 제공 초등 개념 카드(public/concepts/elem/*.json · elemgen/) 검산. 실패 시 exit 1.
// 관리자 「개념 등록」의 「기본 제공 초등 개념 등록」 단추가 이 파일들을 DB(concepts)에 넣는다 — 이미 있는 id 는 건너뛴다.
// 자료: 학기 12개 · 대단원(src/lib/chapters.js)마다 개념이 있다 · id = <학기>-<단원><차례> · sort_order = 단원 × 10 + 차례.
// 카드: 왜 필요할까? → 낱말 풀이 → 핵심 정의 → 이렇게 해요(움직이는 예시) → 왜 그럴까?(src why · 주의 바로 앞) → 꼭 조심할 것 → 바로 확인.
// 글자: ** · == 짝 · ASCII 빼기 · √ 없음 · 빈 값 없음 · 「바로 확인」 물음 ①②③ 과 답 칩이 맞는다.
// 움직이는 예시: 글줄 「[[av:<개념 id>-1,…]]」의 예시가 그 학기 파일(public/concept-av/<학기>.json)에 있고, 학기 파일의 예시는 꼭 한 번 쓰인다.
// 그리기: 개념 화면의 단락 미리보기(BlockPreview)로 모든 단락을 두 테마로 — 오류 · NaN 없음.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { CHAPTERS, chapterIndexOf } from "../src/lib/chapters.js";
import { avMarker, avUnitOf } from "../src/lib/conceptAv.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const DIR = path.join(ROOT, "public/concepts/elem");
const E_UNITS = ["e1-1", "e1-2", "e2-1", "e2-2", "e3-1", "e3-2", "e4-1", "e4-2", "e5-1", "e5-2", "e6-1", "e6-2"];
const BLOCK_TYPES = ["text", "definition", "warning", "check", "image"];   // components/AdminConcepts.jsx 검증과 같다
const IDX = JSON.parse(fs.readFileSync(path.join(DIR, "index.json"), "utf8"));
const PACK = Object.fromEntries(E_UNITS.map((u) => [u, JSON.parse(fs.readFileSync(path.join(DIR, `${u}.json`), "utf8"))]));
const AV = Object.fromEntries(E_UNITS.map((u) => [u, JSON.parse(fs.readFileSync(path.join(ROOT, "public/concept-av", `${u}.json`), "utf8"))]));
const ALL = E_UNITS.flatMap((u) => PACK[u].map((c) => ({ u, c })));
const strings = (x) => (typeof x === "string" ? [x] : Array.isArray(x) ? x.flatMap(strings) : x && typeof x === "object" ? Object.values(x).flatMap(strings) : []);
const labels = (c) => c.blocks.map((b) => b.label);

/* ══════════ 자료 ══════════ */
test("목록(index.json): 학기 12개 · 개념 수가 파일과 같다 · 파일은 학기 12개 + 목록뿐", () => {
  assert.equal(IDX.v, 1);
  assert.deepEqual(IDX.units, E_UNITS);
  assert.equal(IDX.count, ALL.length);
  assert.deepEqual(fs.readdirSync(DIR).sort(), [...E_UNITS.map((u) => `${u}.json`), "index.json"].sort());
});

test("개념 id = <학기>-<단원><차례> · unitId · sort_order = 단원 × 10 + 차례 · 대단원 범위 안 · id 겹침 없음", () => {
  const seen = new Set();
  for (const { u, c } of ALL) {
    assert.match(c.id, new RegExp(`^${u}-\\d\\d$`), c.id);
    assert.ok(!seen.has(c.id), `${c.id} 겹침`);
    seen.add(c.id);
    assert.equal(c.unitId, u, c.id);
    assert.equal(c.order, Number(c.id.slice(-2)), c.id);
    const ch = chapterIndexOf({ unit_id: u, sort_order: c.order });
    assert.ok(ch >= 0, `${c.id} 대단원 밖`);
    assert.ok(c.title && c.subtitle, `${c.id} 제목`);
  }
});

test("대단원마다 개념이 있다(초등 69단원) · 첫 개념의 제목 = 단원 이름", () => {
  let chs = 0;
  for (const u of E_UNITS) {
    CHAPTERS[u].forEach(([title, from, to], i) => {
      chs++;
      const cs = PACK[u].filter((c) => c.order >= from && c.order <= to).sort((a, b) => a.order - b.order);
      assert.ok(cs.length >= 1, `${u} ${i + 1}단원 「${title}」에 개념이 없음`);
      assert.equal(cs[0].title, title, `${u} ${i + 1}단원`);
    });
  }
  assert.equal(chs, 69);
  assert.ok(ALL.length >= 69, `개념 ${ALL.length}`);
});

test("카드 차례: 왜 필요할까? → 낱말 풀이 → 핵심 정의(1개 이상) → 이렇게 해요 → 왜 그럴까?(src why) → 꼭 조심할 것 → 바로 확인 · 단락 id b1 … · 종류는 관리자 검증과 같다", () => {
  for (const { c } of ALL) {
    const L = labels(c), bs = c.blocks;
    assert.deepEqual(bs.map((b) => b.id), bs.map((_, i) => `b${i + 1}`), c.id);
    for (const b of bs) assert.ok(BLOCK_TYPES.includes(b.type), `${c.id} ${b.id} ${b.type}`);
    assert.equal(L[0], "왜 필요할까?", c.id);
    assert.equal(L[1], "낱말 풀이", c.id);
    const nd = bs.filter((b) => b.type === "definition").length;
    assert.ok(nd >= 1 && nd <= 3, `${c.id} 핵심 정의 ${nd}`);
    assert.ok(bs.slice(2, 2 + nd).every((b) => b.type === "definition"), `${c.id} 핵심 정의 자리`);
    const w = bs.findIndex((b) => b.src === "why");
    assert.equal(bs[w].label, "왜 그럴까?", c.id);
    assert.equal(bs[w + 1].type, "warning", `${c.id}: 왜 그럴까? 는 주의 바로 앞`);
    assert.equal(bs.filter((b) => b.src === "why").length, 1, c.id);
    assert.equal(w, 2 + nd + 1, `${c.id}: 이렇게 해요 다음이 왜 그럴까?`);
    assert.equal(bs[bs.length - 1].type, "check", c.id);
    assert.equal(bs.length, nd + 6, c.id);
    for (const b of bs) assert.ok(b.icon?.kind === "emoji" && b.icon.value && b.style?.tone && b.style?.size, `${c.id} ${b.id} 모양`);
  }
});

test("낱말 풀이: 2개 이상 · 「**낱말** — 뜻」 꼴 · 왜 그럴까? 첫 줄은 「**왜 …?**」 · 정의 · 주의 · 확인이 비지 않음", () => {
  for (const { c } of ALL) {
    const words = c.blocks[1].lines;
    assert.ok(words.length >= 2, `${c.id} 낱말 ${words.length}`);
    for (const l of words) assert.match(l, /^\*\*[^*]+\*\* — \S/, `${c.id}: ${l.slice(0, 30)}`);
    const why = c.blocks.find((b) => b.src === "why");
    assert.ok(why.lines.length >= 1 && /^\*\*왜 [^*]+\?\*\*/.test(why.lines[0]), `${c.id} 왜 그럴까?`);
    for (const d of c.blocks.filter((b) => b.type === "definition")) assert.ok(d.term && d.text && Array.isArray(d.chips), `${c.id} 정의`);
    const warn = c.blocks.find((b) => b.type === "warning");
    assert.ok(warn.items.length >= 1, `${c.id} 주의`);
  }
});

test("글자: ** · == 짝 · ASCII 빼기 · √ · * 곱하기 · 빈 값 없음", () => {
  for (const { c } of ALL) {
    for (const s of strings(c)) {
      assert.ok(s.split("**").length % 2 === 1, `${c.id} ** 짝: ${s.slice(0, 40)}`);
      assert.ok(s.split("==").length % 2 === 1, `${c.id} == 짝: ${s.slice(0, 40)}`);
      assert.ok(!/(^|[\s(=,])-\d/.test(s) && !s.includes(" - "), `${c.id} ASCII 빼기: ${s.slice(0, 40)}`);
      assert.ok(!s.includes("√"), `${c.id} 초등에 √`);
      assert.ok(!/\d\s*\*\s*\d/.test(s.replace(/\*\*/g, "")), `${c.id} * 곱하기: ${s.slice(0, 40)}`);
      assert.ok(!/undefined|NaN|\[object/.test(s), `${c.id} 빈 값: ${s.slice(0, 40)}`);
    }
  }
});

test("바로 확인: 물음의 ①②③ 과 답 칩(group)이 하나씩 맞는다 · 답이 비지 않음", () => {
  for (const { c } of ALL) {
    const ck = c.blocks[c.blocks.length - 1];
    const marks = ck.question.match(/[①②③④⑤]/g) || [];
    assert.ok(marks.length >= 2, `${c.id} 물음 ${marks.length}`);
    assert.deepEqual(ck.answer.map((a) => a.group), marks, c.id);
    for (const a of ck.answer) assert.ok(typeof a.nums === "string" && a.nums.trim() && a.tone, `${c.id} ${a.group}`);
  }
});

test("움직이는 예시: 「이렇게 해요」 글줄 하나에 [[av:<개념 id>-1, …]] · 학기 파일에 있다 · 학기 파일 예시는 꼭 한 번 · 개념 id 가 같다 · 학기 = avUnitOf", () => {
  const used = new Set();
  for (const { u, c } of ALL) {
    const mk = c.blocks.flatMap((b) => (b.lines || []).map((l) => ({ b, l, ids: avMarker(l) }))).filter((x) => x.ids);
    if (!mk.length) continue;
    assert.equal(mk.length, 1, `${c.id} 표식 ${mk.length}줄`);
    const { b, ids } = mk[0];
    assert.equal(b.label, "이렇게 해요", `${c.id} 표식 자리`);
    assert.deepEqual(ids, ids.map((_, i) => `${c.id}-${i + 1}`), c.id);
    for (const id of ids) {
      assert.equal(avUnitOf(id), u, id);
      const it = AV[u].items[id];
      assert.ok(it, `${id} 가 학기 파일에 없음`);
      assert.equal(it.cid, c.id, id);
      assert.equal(it.tab, `예제 ${id.split("-").pop()}`, id);
      assert.ok(!used.has(id), `${id} 두 번`);
      used.add(id);
    }
  }
  for (const u of E_UNITS) for (const id of Object.keys(AV[u].items)) assert.ok(used.has(id), `${id} 는 어느 개념에도 없음`);
  assert.ok(used.size >= 120, `예시 ${used.size}`);
  const withAv = ALL.filter(({ c }) => c.blocks.some((b) => (b.lines || []).some((l) => avMarker(l)))).length;
  assert.equal(withAv, ALL.length, `움직이는 예시가 있는 개념 ${withAv}/${ALL.length}`);
});

/* ══════════ 그리기(번들) ══════════ */
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "elem-concepts-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { BlockPreview } from ${JSON.stringify(path.join(ROOT, "src/components/ConceptViewer.jsx"))};
export const block = (b, cid, th) => renderToStaticMarkup(<BlockPreview b={b} conceptId={cid} theme={th} />);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent",
    define: { "process.env.NODE_ENV": '"production"', "import.meta.env": "{}" },
    loader: { ".png": "dataurl", ".jpg": "dataurl", ".svg": "dataurl", ".webp": "dataurl", ".css": "empty" },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const warn = console.warn;
  console.warn = () => {};
  const m = await import(pathToFileURL(out).href);
  console.warn = warn;
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;

  test("개념 화면 단락 미리보기(BlockPreview): 모든 단락 × 두 테마 — 오류 · NaN 없음 · 낱말이 굵게 · 정의 칩 · 움직이는 예시 자리", () => {
    let cnt = 0;
    for (const { c } of ALL) for (const b of c.blocks) for (const th of ["light", "dark"]) {
      const s = m.block(b, c.id, th);
      cnt++;
      assert.ok(s.length > 80 && !BAD.test(s), `${c.id} ${b.id} ${th}: ${(s.match(/.{40}(NaN|undefined|Infinity|\[object Object\]).{20}/) || [""])[0]}`);
      assert.ok(!s.includes("**") && !s.includes("=="), `${c.id} ${b.id}: 꾸밈 표시가 그대로 보임`);
      if (b.label === "낱말 풀이") assert.ok((s.match(/<b /g) || []).length >= b.lines.length, `${c.id} 낱말 굵게`);
      if (b.type === "definition") assert.ok(s.includes("cv-chip"), `${c.id} ${b.id} 칩`);
      if (b.label === "이렇게 해요") assert.ok(s.includes("cv-avwait") && !s.includes("[[av:"), `${c.id}: 움직이는 예시 자리`);
    }
    assert.ok(cnt > 1000, `그린 단락 ${cnt}`);
    console.log(`   단락 ${cnt}개`);
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
