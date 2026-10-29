// 컨셉 문제(주제별 50제) — 데이터 · 답 판정 · OMR(grid.js) 노드 테스트
//   node tests/conceptsets.test.mjs
// 실제 세트 JSON 38개를 읽어 형식을 확인하고, 카드를 그려 원근 · 조명 · 잡음을 얹은 "사진"에서 답을 되읽는지 본다.
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  layoutCard, cardHtml, pageSvg, bandBits, parseBand, bandCells, readCardPhoto, kindOf,
  GW, GH, BUB_R, BAND, AREA, BLOCK_H,
} from "../src/lib/omr/grid.js";
import { homography, applyH, invertH } from "../src/lib/omr/detect.js";
import { judge, rawOf, toInt, parseFrac, answerText, pdfUrl, printUrl, progressSummary, downloadName, fmtBytes } from "../src/lib/conceptsets.js";
import { questionHtml, solutionHtml, missingCueKeys, scaleSvg, safeHtml, boardHtml } from "../src/pages/sets/render.js";
import { scopeCss, splitDoc, composePrint } from "../src/pages/sets/printdoc.js";
import { zipStore, crc32 } from "../src/lib/zipstore.js";
import { execFileSync } from "node:child_process";
import os from "node:os";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIR = path.join(ROOT, "public/concept-sets/prob");
let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log("  ok  " + name); }
  catch (e) { failed++; console.log("FAIL  " + name + "\n      " + (e && e.stack || e).toString().split("\n").slice(0, 5).join("\n      ")); }
}

const INDEX = JSON.parse(fs.readFileSync(path.join(DIR, "index.json"), "utf8"));
const CAT = INDEX.categories[0];
const SETS = CAT.sets.map((s) => JSON.parse(fs.readFileSync(path.join(DIR, `${String(s.no).padStart(2, "0")}.json`), "utf8")));

console.log("데이터");
test("index: 범주 prob · 세트 38 · 묶음이 세트를 한 번씩", () => {
  assert.equal(CAT.id, "prob");
  assert.equal(CAT.sets.length, 38);
  const inGroups = CAT.groups.flatMap((g) => g.sets).sort((a, b) => a - b);
  assert.deepEqual(inGroups, CAT.sets.map((s) => s.no).sort((a, b) => a - b));
  for (const s of CAT.sets) { assert.ok(s.icon && s.short && s.key && s.title); assert.equal(s.n, 50); assert.ok(s.pages.problems >= 8 && s.pages.solutions >= 15); }
});
test("세트 JSON: 문항 50 · 하 15 중 25 상 10 · 필수 필드 · 인쇄 HTML 짝", () => {
  for (const s of SETS) {
    assert.equal(s.items.length, 50, s.key);
    const lv = s.items.reduce((m, it) => ((m[it.lv] = (m[it.lv] || 0) + 1), m), {});
    assert.deepEqual(lv, { 하: 15, 중: 25, 상: 10 }, s.key);
    for (const it of s.items) {
      assert.ok(it.id && it.q && it.a && it.omr && it.s, `${s.key} ${it.id}`);
      assert.ok(["int", "frac", "pick", "pair"].includes(it.a.k), `${s.key} ${it.id} kind`);
      assert.ok(Array.isArray(it.s.board) && it.s.board.length === it.s.steps.length, `${s.key} ${it.id} board`);
      assert.equal(it.s.anim.length, it.s.board.length, `${s.key} ${it.id} anim`);
      // 큐가 가리키는 도식 키는 도식 안에 있어야 한다 (판서 line/hint 는 앱이 그린다)
      for (const step of it.s.anim) for (const c of step) {
        if (/^(line|hint):/.test(c.k)) continue;
        assert.ok(it.s.dg && (it.s.dg.includes(`data-k="${c.k}"`) || it.s.dg.includes(`data-ka="${c.k}"`)), `${s.key} ${it.id} cue ${c.k}`);
      }
      assert.ok(!/<script/i.test(JSON.stringify(it)), "no script");
    }
    const nn = String(s.no).padStart(2, "0");
    for (const d of ["problems", "solutions"]) assert.ok(fs.existsSync(path.join(DIR, "print", `${nn}-${d}.html`)), `${nn}-${d}.html`);
  }
});
test("인쇄 HTML: 글꼴은 jsDelivr · file:// 없음 · @page", () => {
  for (const f of fs.readdirSync(path.join(DIR, "print"))) {
    const h = fs.readFileSync(path.join(DIR, "print", f), "utf8");
    assert.ok(!h.includes("file://"), f);
    assert.ok(h.includes("https://cdn.jsdelivr.net/npm/@fontsource/"), f);
    assert.ok(h.includes("@page{size:A4"), f);
  }
});

console.log("답 판정");
const I = (a) => ({ a });
test("정수: 단위 · 쉼표 · 공백", () => {
  assert.equal(toInt("1,200가지"), 1200); assert.equal(toInt(" 12 가지 "), 12); assert.equal(toInt("12a"), null);
  assert.deepEqual(judge(I({ k: "int", v: 12 }), "12가지"), { ok: true, note: "" });
  assert.equal(judge(I({ k: "int", v: 12 }), "13").ok, false);
  assert.equal(judge(I({ k: "int", v: 117600 }), "117,600").ok, true);
  assert.equal(judge(I({ k: "int", v: 12 }), "").ok, null);
  assert.equal(judge(I({ k: "int", v: 12 }), "1?").ok, null);
});
test("분수: 값이 같으면 정답 · 약분 안내 · '분의' · 0과 1", () => {
  const f = I({ k: "frac", n: 5, d: 12 });
  assert.equal(judge(f, "5/12").ok, true); assert.equal(judge(f, "5 / 12").ok, true); assert.equal(judge(f, "12분의 5").ok, true);
  const r = judge(I({ k: "frac", n: 2, d: 3 }), "6/9"); assert.equal(r.ok, true); assert.ok(r.note.includes("2/3"));
  assert.equal(judge(f, "5/13").ok, false); assert.equal(judge(f, "abc").ok, false);
  assert.equal(judge(I({ k: "frac", n: 0, d: 1 }), "0").ok, true); assert.equal(judge(I({ k: "frac", n: 1, d: 1 }), "1").ok, true);
  assert.deepEqual(parseFrac("3/0"), { n: 3, d: 0 }); assert.equal(judge(f, "3/0").ok, false);
});
test("보기 · 두 수", () => {
  const p = I({ k: "pick", v: ["ㄱ", "ㄷ"], o: ["ㄱ", "ㄴ", "ㄷ", "ㄹ"] });
  assert.equal(judge(p, "ㄱ, ㄷ").ok, true); assert.equal(judge(p, "ㄷㄱ").ok, true); assert.equal(judge(p, "ㄱ").ok, false); assert.equal(judge(p, "ㄱ,ㄴ,ㄷ").ok, false);
  const q = I({ k: "pair", v: [14, 21] });
  assert.equal(judge(q, "14, 21").ok, true); assert.equal(judge(q, "최솟값 14경기, 최댓값 21경기").ok, true); assert.equal(judge(q, "21, 14").ok, false);
});
test("모든 세트: 정답의 쓰는 꼴(rawOf)은 스스로 정답 · 정답 글자 있음", () => {
  for (const s of SETS) for (const it of s.items) {
    assert.equal(judge(it, rawOf(it)).ok, true, `${s.key} ${it.id} ${rawOf(it)}`);
    assert.ok(answerText(it).length > 0);
  }
});
test("파일 주소 · 진도 요약", () => {
  const s = SETS[0];
  const u = pdfUrl("prob", s, "omr");
  assert.ok(u.startsWith("https://") && u.includes("/concept-sets/prob/01/omr.pdf?download=") && u.includes(encodeURIComponent("01-야구-OMR.pdf")));
  assert.equal(printUrl("prob", 7, "solutions"), "/concept-sets/prob/print/07-solutions.html");
  const sum = progressSummary(s, { items: { [s.items[0].id]: { ok: true }, [s.items[1].id]: { ok: false } } });
  assert.deepEqual(sum, { done: 2, ok: 1, n: 50 });
});

console.log("화면 HTML");
test("3단 해설: 모든 문항 — 방침 · 전개 · 확인 · 모범 답안 · 채점 기준, 큐 키가 모두 렌더에 있음", () => {
  for (const s of SETS) for (const it of s.items) {
    const h = solutionHtml(it);
    for (const w of ["방침", "전개", "확인", "포지티브", "네거티브", "모범 답안", "채점 기준"]) assert.ok(h.includes(w), `${s.key} ${it.id} ${w}`);
    assert.ok(h.includes('class="lv cs-st anim-level"') && h.includes("data-anim="), `${s.key} ${it.id} anim`);
    assert.deepEqual(missingCueKeys(it, h), [], `${s.key} ${it.id} cue keys`);
    assert.equal((h.match(/class="fig-line"/g) || []).length, it.s.board.length);
    assert.ok(!/<script|\son[a-z]+=/i.test(h), "safe");
  }
});
test("문항 HTML: 발문 · 보기 · 표 · 그림 · 움직임 끄기", () => {
  const it = SETS[0].items.find((x) => x.box);
  const h = questionHtml(it);
  assert.ok(h.includes("cs-box") && h.includes("보기"));
  const r = SETS[0].items.find((x) => x.rows);
  assert.ok(questionHtml(r).includes("<table class=\"cs-rows\">") && questionHtml(r).includes("<th>"));
  const f = SETS[0].items.find((x) => x.fig);
  assert.ok(questionHtml(f).includes("cs-qfig") && /style="width:[\d.]+px;max-width:100%;height:auto"/.test(questionHtml(f)));
  assert.ok(!solutionHtml(it, { anim: false }).includes("data-anim"));
});
test("SVG 크기 · id 겹침 방지 · 위험 요소 제거", () => {
  const svg = '<svg viewBox="0 0 10 5" width="10mm" height="5mm"><defs><marker id="ah"/></defs><path marker-end="url(#ah)"/></svg>';
  const a = scaleSvg(svg, 1), b = scaleSvg(svg, 1);
  const ida = a.match(/id="([^"]+)"/)[1], idb = b.match(/id="([^"]+)"/)[1];
  assert.notEqual(ida, idb); assert.ok(a.includes(`url(#${ida})`)); assert.ok(a.includes("width:37.8px"));
  assert.equal(safeHtml('<b onclick="x()">a</b><script>alert(1)</script><a href="javascript:x">y</a>'), '<b>a</b><a href="#">y</a>');
  assert.ok(boardHtml([{ h: "볼", t: "4가지" }, { h: "", t: "4 × 3" }]).includes('data-k="hint:0"'));
  assert.ok(!boardHtml([{ h: "", t: "4 × 3" }]).includes("hint:0"));
});
test("인쇄 CSS 감싸기: html/body → 감싼 상자 · @page 버림 · @media 안쪽", () => {
  const css = "@page{size:A4;margin:1mm}html,body{margin:0}body{font-size:10pt}* {box-sizing:border-box}.q .lv,p+p{color:red}@media screen{html{background:#eee}.cs-p .pg{margin:0}}.cs-p{font-size:9pt}";
  const o = scopeCss(css, ".cs-p");
  assert.ok(!o.includes("@page"));
  assert.ok(o.includes(".cs-p{margin:0}") && o.includes(".cs-p{font-size:10pt}") && o.includes(".cs-p *{box-sizing:border-box}"));
  assert.ok(o.includes(".cs-p .q .lv,.cs-p p+p{color:red}"));
  assert.ok(o.includes("@media screen{.cs-p{background:#eee}.cs-p .pg{margin:0}}"));
  assert.ok(o.endsWith(".cs-p{font-size:9pt}"));
});
test("인쇄 합치기: 하나면 원본 그대로 + 인쇄 스크립트 · 여럿이면 문서마다 감싸고 쪽 나눔", () => {
  const P = fs.readFileSync(path.join(DIR, "print/01-problems.html"), "utf8");
  const S = fs.readFileSync(path.join(DIR, "print/01-solutions.html"), "utf8");
  const one = composePrint([{ kind: "doc", cls: "cs-p", html: P }], "t");
  assert.ok(one.includes("window.print") && one.includes("@page{size:A4;margin:12mm 13mm 13mm 13mm"));
  const card = layoutCard({ cat: "prob", no: 1, title: SETS[0].title, items: SETS[0].items });
  const all = composePrint([{ kind: "doc", cls: "cs-p", html: P }, { kind: "doc", cls: "cs-s", html: S }, { kind: "omr", html: cardHtml(card) }], "t");
  assert.ok(all.includes('<div class="cs-doc csx-p"><div class="cs-p">') && all.includes('<div class="cs-doc csx-s cs-brk"><div class="cs-s">') && all.includes('<div class="cs-omr cs-brk">'));
  assert.equal((all.match(/class="omr-pg"/g) || []).length, 2);
  assert.equal((all.match(/<style>/g) || []).length >= 3, true);
  assert.ok(!/<body[^>]*>[\s\S]*<style>[\s\S]*<\/body>/.test(all.replace(/<div class="cs-omr[\s\S]*$/, "")), "본문 안 style 은 head 로 옮김");
  const d = splitDoc(P); assert.ok(d.links.length >= 5 && d.css.length >= 2 && !d.body.includes("<style"));
});
test("ZIP(store): 파이썬 zipfile 로 열림 · UTF-8 이름 · CRC", () => {
  assert.equal(crc32(new TextEncoder().encode("123456789")), 0xcbf43926);
  const files = [{ name: "01-야구-문제.pdf", data: new Uint8Array([37, 80, 68, 70, 1, 2, 3]) }, { name: "01-야구-OMR.pdf", data: new Uint8Array(5000).map((_, i) => i % 251) }];
  const z = zipStore(files);
  const f = path.join(os.tmpdir(), `cs-zip-${process.pid}.zip`);
  fs.writeFileSync(f, z);
  const out = execFileSync("python3", ["-c", "import zipfile,sys;z=zipfile.ZipFile(sys.argv[1]);assert z.testzip() is None;print('|'.join(f'{i.filename}:{i.file_size}:{i.flag_bits & 0x800}' for i in z.infolist()))", f]).toString().trim();
  fs.unlinkSync(f);
  assert.equal(out, "01-야구-문제.pdf:7:2048|01-야구-OMR.pdf:5000:2048");
  assert.equal(downloadName(SETS[0], "solutions"), "01-야구-해설.pdf");
  assert.equal(fmtBytes(1058096), "1.1MB"); assert.equal(fmtBytes(43000), "43KB"); assert.equal(fmtBytes(0), "");
});

console.log("OMR 카드");
test("쪽 코드 띠: 세트 1~38 · 쪽 0~3 왕복 · 한 칸 뒤집히면 거부", () => {
  for (let set = 1; set <= 38; set++) for (let page = 0; page < 4; page++) {
    const b = bandBits("prob", set, page);
    assert.equal(b.length, BAND.n);
    assert.deepEqual(parseBand(b), { cat: "prob", set, page });
    for (let i = 1; i < BAND.n - 1; i++) { const c = b.slice(); c[i] ^= 1; const r = parseBand(c); assert.ok(!r || r.set !== set || r.page !== page || r.cat !== "prob", `flip ${i}`); }
  }
});
test("배치: 38세트 모두 2쪽 · 칸은 영역 안 · 서로 겹치지 않음 · 마커/띠와 떨어짐", () => {
  for (const s of SETS) {
    const card = layoutCard({ cat: "prob", no: s.no, title: s.title, items: s.items });
    assert.equal(card.pages.length, 2, s.key);
    assert.equal(card.pages.reduce((n, p) => n + p.blocks.length, 0), 50);
    for (const p of card.pages) {
      const rects = p.blocks.map((b) => ({ x0: b.x, y0: b.y, x1: b.x + b.w, y1: b.y + b.h }));
      for (const r of rects) assert.ok(r.x0 >= AREA.x0 - 0.5 && r.x1 <= AREA.x1 + 0.5 && r.y1 <= AREA.yMax + 0.5, `${s.key} p${p.index} inside`);
      for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
        const a = rects[i], b = rects[j];
        assert.ok(a.x1 <= b.x0 || b.x1 <= a.x0 || a.y1 <= b.y0 || b.y1 <= a.y0, `${s.key} overlap`);
      }
      const keep = [...p.markers.map((m) => ({ x0: m.x - 15, y0: m.y - 15, x1: m.x + m.size + 15, y1: m.y + m.size + 15 })),
        { x0: BAND.x0 - 10, y0: BAND.y - 10, x1: BAND.x0 + BAND.n * (BAND.cell + BAND.gap), y1: BAND.y + BAND.cell + 10 }];
      for (const r of rects) for (const k of keep) assert.ok(r.x1 <= k.x0 || k.x1 <= r.x0 || r.y1 <= k.y0 || k.y1 <= r.y0, `${s.key} near marker/band`);
    }
  }
});
test("칸 종류 · 자리 수", () => {
  assert.deepEqual(kindOf({ a: { k: "int", v: 5 }, omr: { c: [3] } }), { kind: "int", cols: [3] });
  assert.deepEqual(kindOf({ a: { k: "frac", n: 1, d: 125 }, omr: { c: [2, 3] } }), { kind: "frac", cols: [2, 3] });
  assert.equal(kindOf({ a: { k: "pick", v: ["ㄱ"], o: ["ㄱ", "ㄴ", "ㄷ"] }, omr: { o: 3 } }).opts.length, 3);
  for (const s of SETS) for (const it of s.items) {
    const k = kindOf(it);
    if (k.kind === "int") assert.ok(String(it.a.v).length <= k.cols[0], `${s.key} ${it.id} int cols`);
    if (k.kind === "frac") assert.ok(String(it.a.n).length <= k.cols[0] && String(it.a.d).length <= k.cols[1], `${s.key} ${it.id} frac cols`);
    if (k.kind === "pair") assert.ok(String(it.a.v[0]).length <= k.cols[0] && String(it.a.v[1]).length <= k.cols[1]);
  }
});
test("cardHtml: 쪽마다 SVG 한 장 · viewBox · 띠 칸", () => {
  const s = SETS[0];
  const card = layoutCard({ cat: "prob", no: s.no, title: s.title, items: s.items });
  const h = cardHtml(card);
  assert.equal((h.match(/<svg /g) || []).length, 2);
  assert.ok(h.includes(`viewBox="0 0 ${GW} ${GH}"`));
  assert.ok(pageSvg(card, card.pages[0]).includes(s.title));
});

// ── 합성 사진 ─────────────────────────────────────────────────────────────────
function raster(w, h, v) { return { w, h, px: new Float32Array(w * h).fill(v) }; }
function fillRect(r, x, y, w, h, v) {
  for (let j = Math.max(0, Math.floor(y)); j < Math.min(r.h, Math.ceil(y + h)); j++)
    for (let i = Math.max(0, Math.floor(x)); i < Math.min(r.w, Math.ceil(x + w)); i++) r.px[j * r.w + i] = v;
}
function fillCircle(r, cx, cy, rad, v) {
  for (let j = Math.max(0, Math.floor(cy - rad)); j <= Math.min(r.h - 1, Math.ceil(cy + rad)); j++)
    for (let i = Math.max(0, Math.floor(cx - rad)); i <= Math.min(r.w - 1, Math.ceil(cx + rad)); i++) {
      const dx = i + 0.5 - cx, dy = j + 0.5 - cy;
      if (dx * dx + dy * dy <= rad * rad) r.px[j * r.w + i] = Math.min(r.px[j * r.w + i], v);
    }
}
function ring(r, cx, cy, rad, width, v) {
  const a = (rad - width / 2) ** 2, b = (rad + width / 2) ** 2;
  for (let j = Math.max(0, Math.floor(cy - rad - width)); j <= Math.min(r.h - 1, Math.ceil(cy + rad + width)); j++)
    for (let i = Math.max(0, Math.floor(cx - rad - width)); i <= Math.min(r.w - 1, Math.ceil(cx + rad + width)); i++) {
      const dx = i + 0.5 - cx, dy = j + 0.5 - cy, d = dx * dx + dy * dy;
      if (d >= a && d <= b) r.px[j * r.w + i] = Math.min(r.px[j * r.w + i], v);
    }
}
function strokeRect(r, x, y, w, h, lw, v) { fillRect(r, x, y, w, lw, v); fillRect(r, x, y + h - lw, w, lw, v); fillRect(r, x, y, lw, h, v); fillRect(r, x + w - lw, y, lw, h, v); }
function sampleBilinear(r, x, y) {
  x = Math.max(0, Math.min(r.w - 1.001, x)); y = Math.max(0, Math.min(r.h - 1.001, y));
  const x0 = x | 0, y0 = y | 0, fx = x - x0, fy = y - y0, i = y0 * r.w + x0;
  const top = r.px[i] * (1 - fx) + r.px[i + 1] * fx, bot = r.px[i + r.w] * (1 - fx) + r.px[i + r.w + 1] * fx;
  return top * (1 - fy) + bot * fy;
}
function prng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

/** 자리마다 칠할 숫자 — 오른쪽 맞춤. "" = 빈자리 */
function digitsRight(str, cols) { const d = String(str).split(""); return Array.from({ length: cols }, (_, i) => d[i - (cols - d.length)] ?? ""); }

/**
 * 한 쪽 그리기. fills: { [no]: 그 문항의 "쓰는 꼴" 또는 { cols: [[자리 숫자…]…] } (이상한 칠 시험용) }
 */
function drawPage(card, p, fills) {
  const r = raster(GW, GH, 236);
  for (const m of p.markers) fillRect(r, m.x, m.y, m.size, m.size, 24);
  fillRect(r, p.orient.x, p.orient.y, p.orient.w, p.orient.h, 24);
  bandCells().forEach((c, i) => { if (p.band[i]) fillRect(r, c.x, c.y, c.size, c.size, 24); else strokeRect(r, c.x, c.y, c.size, c.size, 1, 215); });
  if (p.index === 0) {                                              // 제목 · 이름 · 날짜 줄 흉내 (pageSvg 와 같은 자리)
    fillRect(r, 330, 136, 340, 24, 70);
    fillRect(r, 203, 229, 257, 2, 80); fillRect(r, 583, 229, 257, 2, 80);
    fillRect(r, 200, 244, 600, 12, 150);
  } else fillRect(r, 300, 134, 400, 18, 70);
  for (const b of p.blocks) {
    fillRect(r, b.x + 3, b.y + 4, 12, 15, 40);                     // 번호
    if (b.kind === "pick") {
      for (const q of b.picks) { ring(r, q.x, q.y, BUB_R + 3, 1.6, 70); fillRect(r, q.x - 3, q.y - 4, 6, 8, 185); }
    } else {
      for (const g of b.grids) {
        for (const bx of g.boxes) strokeRect(r, bx.x, bx.y, bx.w, bx.h, 1.2, 85);
        for (const col of g.bubbles) for (const bb of col) { ring(r, bb.x, bb.y, BUB_R, 1.4, 75); fillRect(r, bb.x - 2.5, bb.y - 3.5, 5, 7, 190); }
      }
    }
    const f = fills[b.no];
    if (f == null) continue;
    const pen = (x, y, rad, k) => (k % 3 === 0 ? fillCircle(r, x + 0.8, y - 0.6, rad + 1.6, 120) : fillCircle(r, x, y, rad - 0.6, 52));
    if (b.kind === "pick") {
      const on = String(f).match(/[ㄱ-ㅎ]/gu) || [];
      for (const q of b.picks) if (on.includes(q.label)) pen(q.x, q.y, BUB_R + 3, b.no);
      continue;
    }
    let cols;
    if (typeof f === "object") cols = f.cols;
    else {
      const parts = b.kind === "frac" ? (String(f).includes("/") ? String(f).split("/") : [String(f), ""]) : b.kind === "pair" ? String(f).split(/,\s*/) : [String(f)];
      cols = b.grids.map((g, gi) => digitsRight(parts[gi] ?? "", g.cols));
    }
    b.grids.forEach((g, gi) => g.bubbles.forEach((col, ci) => {
      const want = cols[gi]?.[ci];
      for (const dgt of Array.isArray(want) ? want : [want]) {
        if (dgt === "" || dgt == null) continue;
        const bb = col[+dgt];
        pen(bb.x, bb.y, BUB_R, b.no + ci);
      }
    }));
  }
  return r;
}

function photograph(card, W, H, quad, seed = 1, table = 100) {
  const Hc2i = homography([[0, 0], [card.w, 0], [card.w, card.h], [0, card.h]], quad);
  const Hi2c = invertH(Hc2i);
  const rnd = prng(seed);
  const g = new Float32Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const [cx, cy] = applyH(Hi2c, x + 0.5, y + 0.5);
    let v = table;
    if (cx >= 0 && cy >= 0 && cx < card.w && cy < card.h) v = sampleBilinear(card, cx, cy);
    v *= 0.74 + 0.3 * (x / W) - 0.08 * (y / H);
    g[y * W + x] = v + (rnd() - 0.5) * 14;
  }
  const b = new Float32Array(W * H);
  for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
    let s = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) s += g[(y + dy) * W + x + dx];
    b[y * W + x] = s / 9;
  }
  const data = new Uint8ClampedArray(W * H * 4);
  for (let i = 0; i < W * H; i++) { const v = Math.max(0, Math.min(255, Math.round(b[i]))); data[i * 4] = v; data[i * 4 + 1] = v; data[i * 4 + 2] = v; data[i * 4 + 3] = 255; }
  return { width: W, height: H, data };
}

const SET = SETS[0];
const CARD = layoutCard({ cat: "prob", no: SET.no, title: SET.title, items: SET.items });
const byNo = Object.fromEntries(SET.items.map((it) => [it.no, it]));
// 정답대로 칠하되 몇 문항은 일부러 비틀기
const FILLS = {};
for (const it of SET.items) FILLS[it.no] = rawOf(it);
const intItem = SET.items.find((it) => it.a.k === "int" && kindOf(it).cols[0] === 3 && it.no > 3);
const fracItem = SET.items.find((it) => it.a.k === "frac" && it.no > 3);
FILLS[2] = null;                                                         // 무응답
FILLS[intItem.no] = { cols: [[[1, 4], "2", "7"]] };                      // 첫 자리 두 개 칠함 → "?"
const gapNo = SET.items.find((it) => it.a.k === "int" && kindOf(it).cols[0] === 3 && it.no !== intItem.no && it.no > 3).no;
FILLS[gapNo] = { cols: [["1", "", "2"]] };                               // 가운데 빈자리 → "1?2"
const wrongNo = fracItem.no; FILLS[wrongNo] = "6/9";                     // 약분 안 한 답(값이 다르면 오답)
const expectRaw = (no) => {
  if (no === 2) return "";
  if (no === intItem.no) return "?27";
  if (no === gapNo) return "1?2";
  if (no === wrongNo) return "6/9";
  return rawOf(byNo[no]);
};

function checkPage(res, p) {
  assert.equal(res.ok, true, "ok (" + res.reason + ")");
  assert.equal(res.page, p.index);
  for (const b of p.blocks) {
    const a = res.answers.find((x) => x.no === b.no);
    assert.ok(a, "no " + b.no);
    assert.equal(a.raw, expectRaw(b.no), `no ${b.no} (${b.kind}) got ${a.raw}`);
    if (![intItem.no, gapNo].includes(b.no) && b.kind !== "pick") assert.ok(a.conf >= 0.5, `no ${b.no} conf ${a.conf}`);
  }
  const d = res.answers.find((x) => x.no === intItem.no); if (d) assert.equal(d.flag, "double");
  const g = res.answers.find((x) => x.no === gapNo); if (g) assert.equal(g.flag, "gap");
}

console.log("OMR 판독 (합성 사진)");
const PAGES = CARD.pages.map((p) => drawPage(CARD, p, FILLS));
test("1쪽: 기울여 찍은 사진", () => {
  const img = photograph(PAGES[0], 1300, 1820, [[95, 70], [1215, 110], [1250, 1745], [60, 1700]], 3);
  checkPage(readCardPhoto(img, CARD), CARD.pages[0]);
});
test("2쪽: 띠로 쪽을 알아낸다 · 원근 심하게", () => {
  const img = photograph(PAGES[1], 1400, 1900, [[180, 120], [1180, 60], [1300, 1840], [70, 1760]], 7);
  checkPage(readCardPhoto(img, CARD), CARD.pages[1]);
});
test("1쪽을 거꾸로(180°) 찍어도", () => {
  const img = photograph(PAGES[0], 1300, 1820, [[1220, 1730], [80, 1760], [100, 90], [1190, 60]], 11);
  checkPage(readCardPhoto(img, CARD), CARD.pages[0]);
});
test("다른 세트의 카드면 거부(other-set)", () => {
  const other = layoutCard({ cat: "prob", no: SETS[1].no, title: SETS[1].title, items: SETS[1].items });
  const img = photograph(drawPage(other, other.pages[0], {}), 1200, 1700, [[60, 60], [1140, 60], [1140, 1640], [60, 1640]], 5);
  const r = readCardPhoto(img, CARD);
  assert.equal(r.ok, false); assert.equal(r.reason, "other-set"); assert.equal(r.band.set, SETS[1].no);
});
test("마커가 없으면 markers", () => {
  const r = raster(GW, GH, 236);
  const img = photograph(r, 900, 1200, [[40, 40], [860, 40], [860, 1160], [40, 1160]], 2);
  assert.equal(readCardPhoto(img, CARD).reason, "markers");
});
test("다른 세트(20 · 38)도 두 쪽 모두 정답 그대로 읽힘", () => {
  for (const S of [SETS[19], SETS[37]]) {
    const C = layoutCard({ cat: "prob", no: S.no, title: S.title, items: S.items });
    const F = Object.fromEntries(S.items.map((it) => [it.no, rawOf(it)]));
    C.pages.forEach((p, k) => {
      const img = photograph(drawPage(C, p, F), 1300, 1820, k ? [[1210, 1740], [70, 1770], [95, 80], [1180, 50]] : [[80, 60], [1230, 95], [1260, 1760], [50, 1720]], 20 + k);
      const r = readCardPhoto(img, C);
      assert.equal(r.ok, true, `${S.key} p${k} ${r.reason}`);
      assert.equal(r.page, k);
      for (const a of r.answers) assert.equal(a.raw, F[a.no], `${S.key} ${a.no}`);
    });
  }
});
test("판독 → 판정: 약분 안 한 값이 다르면 오답, 두 번 칠한 자리는 채점 보류", () => {
  assert.equal(judge(byNo[wrongNo], "6/9").ok, byNo[wrongNo].a.n * 9 === byNo[wrongNo].a.d * 6);
  assert.equal(judge(byNo[intItem.no], "?27").ok, null);
});

console.log(`\n${passed} passed, ${failed} failed`);
if (failed) process.exit(1);
