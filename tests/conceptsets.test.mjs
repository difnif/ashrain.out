// 컨셉 문제(주제별 50제) — 데이터 · 답 판정 · OMR(grid.js) 노드 테스트
//   node tests/conceptsets.test.mjs
// 실제 세트 JSON 116개를 읽어 형식을 확인하고, 카드(v2 · 예전 v1)를 그려 원근 · 조명 · 잡음 · 그림자를 얹은 "사진"에서 답을 되읽는지 본다.
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  layoutCard, cardHtml, pageSvg, bandBits, parseBand, bandCells, readCardPhoto, kindOf, handCrops,
  GW, GH, BAND, BAND2, V2, OMR_VER, MARKER_SIZE,
} from "../src/lib/omr/grid.js";
import { raster, fillRect, fillCircle, ring, strokeRect, handText, photograph } from "./fixtures/omrsynth.mjs";
import { judge, rawOf, toInt, parseFrac, answerText, pdfUrl, printUrl, progressSummary, downloadName, fmtBytes } from "../src/lib/conceptsets.js";
import { questionHtml, solutionHtml, missingCueKeys, scaleSvg, safeHtml, boardHtml } from "../src/pages/sets/render.js";
import { scopeCss, splitDoc, composePrint } from "../src/pages/sets/printdoc.js";
import { zipStore, crc32 } from "../src/lib/zipstore.js";
import { execFileSync } from "node:child_process";
import os from "node:os";
import crypto from "node:crypto";

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
test("index: 범주 prob · 세트 116 · 묶음이 세트를 한 번씩 · 역사는 한국사 · 유럽사 · 중국사 · 일본사", () => {
  assert.equal(CAT.id, "prob");
  assert.equal(CAT.sets.length, 116);
  const gt = CAT.groups.map((g) => g.title);
  for (const t of ["한국사", "유럽사", "중국사", "일본사", "과학"]) assert.ok(gt.includes(t), t);
  assert.deepEqual(CAT.groups.find((g) => g.title === "일본사").sets, [111, 112, 25, 26, 27, 28]);
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
  assert.equal((all.match(/class="omr-pg"/g) || []).length, card.pages.length);
  assert.equal(card.pages.length, 3);
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
const cardOf = (s, ver) => layoutCard({ cat: "prob", no: s.no, title: s.title, items: s.items }, ver ? { ver } : undefined);
test("쪽 코드 띠: 세트 1~126 · 쪽 0~3 왕복 · 한 칸 뒤집히면 거부 · 1~63번은 예전 띠 그대로", () => {
  // 예전(확장 전) 띠: 범주 코드 1 + 세트 6비트 — 이미 인쇄한 카드가 그대로 읽혀야 한다
  const old = (set, page) => { const d = [0, 1, ...[5, 4, 3, 2, 1, 0].map((x) => (set >> x) & 1), ...[1, 0].map((x) => (page >> x) & 1)]; const o = d.reduce((a, c) => a + c, 0) % 4; return [1, ...d, (o >> 1) & 1, o & 1, 1]; };
  for (let set = 1; set <= 63; set++) for (let page = 0; page < 4; page++) assert.deepEqual(bandBits("prob", set, page), old(set, page));
  assert.throws(() => bandBits("prob", 127, 0));
  for (let set = 1; set <= 126; set++) for (let page = 0; page < 4; page++) {
    const b = bandBits("prob", set, page);
    assert.equal(b.length, BAND.n);
    assert.deepEqual(parseBand(b), { cat: "prob", set, page });
    for (let i = 1; i < BAND.n - 1; i++) { const c = b.slice(); c[i] ^= 1; const r = parseBand(c); assert.ok(!r || r.set !== set || r.page !== page || r.cat !== "prob", `flip ${i}`); }
  }
});
test("판: 지금 카드는 v2 · 띠는 v1 위쪽 · v2 아래쪽(마커 사이) · 둘 다 방향 막대 기준 자리와 안 겹침", () => {
  assert.equal(OMR_VER, 2);
  const c2 = cardOf(SETS[0]), c1 = cardOf(SETS[0], 1);
  assert.equal(c2.ver, 2); assert.equal(c1.ver, 1);
  assert.deepEqual(c2.pages[0].bandPos, BAND2); assert.deepEqual(c1.pages[0].bandPos, BAND);
  const bot = c2.pages[0].markers[2];
  const cells = bandCells(BAND2);
  assert.ok(cells[0].x > c2.pages[0].markers[3].x + MARKER_SIZE + 20 && cells.at(-1).x + BAND2.cell < bot.x - 20);
  assert.ok(BAND2.y > bot.y && BAND2.y + BAND2.cell < bot.y + MARKER_SIZE);
  // 방향 막대의 대칭 참조 자리(오른쪽 위 마커 왼쪽)는 늘 빈 종이여야 한다
  const refX = GW - c2.pages[0].orient.x - c2.pages[0].orient.w;
  for (const pos of [BAND, BAND2]) assert.ok(pos.x0 + pos.n * (pos.cell + pos.gap) < refX);
});
// 이미 인쇄해 나간 카드(1~90번)의 배치 지문 — 판독은 이 배치로 사진을 읽으니 한 점이라도 바뀌면 예전 카드를 못 읽는다.
// 세트가 늘어도(91번~) 이 지문은 1~90번만 본다.
const PRINTED = SETS.filter((s) => s.no <= 90);
const r3 = (v) => Math.round(v * 1000) / 1000;
test("v1 배치(예전 카드 읽기용)는 한 점도 바뀌지 않았다 — 1~90번 지문", () => {
  const parts = [];
  for (const S of PRINTED) {
    const c = cardOf(S, 1);
    for (const p of c.pages) {
      parts.push(`${S.no}:${p.index}/${p.n}:${p.band.join("")}`);
      for (const b of p.blocks) {
        parts.push(`${b.no}${b.kind}@${r3(b.x)},${r3(b.y)},${r3(b.w)},${r3(b.h)}`);
        for (const g of b.grids) parts.push(g.bubbles.map((col) => col.map((q) => `${r3(q.x)},${r3(q.y)},${q.d}`).join(";")).join("|"));
        if (b.picks) parts.push(b.picks.map((q) => `${r3(q.x)},${r3(q.y)},${q.label}`).join(";"));
      }
    }
  }
  assert.equal(PRINTED.length, 90);
  const h = crypto.createHash("sha256").update(parts.join("\n")).digest("hex");
  assert.equal(h, "3bb60a8b2b7963c2fd1c4086fe10f99d309f25cee5e3f2bf7c8bc480e41dfeba");
});
test("v2 배치(지금 카드)도 1~90번은 한 점도 바뀌지 않았다 — 손글씨 칸까지 지문", () => {
  const parts = [];
  for (const S of PRINTED) {
    for (const p of cardOf(S).pages) {
      parts.push(`${S.no}:${p.index}/${p.n}:${p.band.join("")}`);
      for (const b of p.blocks) {
        parts.push(`${b.no}${b.kind}@${r3(b.x)},${r3(b.y)},${r3(b.w)},${r3(b.h)}`);
        for (const g of b.grids) parts.push(g.bubbles.map((col) => col.map((q) => `${r3(q.x)},${r3(q.y)},${q.d}`).join(";")).join("|"));
        if (b.picks) parts.push(b.picks.map((q) => `${r3(q.x)},${r3(q.y)},${q.label}`).join(";"));
        if (b.hand) parts.push(["num", "den"].map((k) => { const x = b.hand[k]; return `${k}:${r3(x.x)},${r3(x.y)},${r3(x.w)},${r3(x.h)}`; }).join(";") + `|bar:${r3(b.hand.bar.x1)},${r3(b.hand.bar.x2)},${r3(b.hand.bar.y)}`);
      }
    }
  }
  assert.equal(parts.length, 9271);
  const h = crypto.createHash("sha256").update(parts.join("\n")).digest("hex");
  assert.equal(h, "68d4b26c3d75b66bf5cfcdd5dbaf789315ef4e1b7f9ccb09caa4e8d02288ed85");
});
test("배치(v2): 모든 세트 3쪽 · 쪽마다 18/17/15칸 · 영역 안 · 겹치지 않음 · 마커 · 띠(위 자리도)와 떨어짐", () => {
  for (const s of SETS) {
    const card = cardOf(s);
    assert.equal(card.pages.length, 3, s.key);
    assert.deepEqual(card.pages.map((p) => p.blocks.length), [18, 17, 15], s.key);
    for (const p of card.pages) {
      const rects = p.blocks.map((b) => ({ x0: b.x, y0: b.y, x1: b.x + b.w, y1: b.y + b.h }));
      for (const r of rects) assert.ok(r.x0 >= V2.AREA.x0 - 0.5 && r.x1 <= V2.AREA.x1 + 0.5 && r.y1 <= V2.AREA.yMax + 0.5, `${s.key} p${p.index} inside`);
      for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
        const a = rects[i], b = rects[j];
        assert.ok(a.x1 + V2.GAP_X - 0.5 <= b.x0 || b.x1 + V2.GAP_X - 0.5 <= a.x0 || a.y1 <= b.y0 || b.y1 <= a.y0, `${s.key} overlap`);
      }
      const keep = [...p.markers.map((m) => ({ x0: m.x - 15, y0: m.y - 15, x1: m.x + m.size + 15, y1: m.y + m.size + 15 })),
        ...[BAND, BAND2].map((B) => ({ x0: B.x0 - 10, y0: B.y - 10, x1: B.x0 + B.n * (B.cell + B.gap), y1: B.y + B.cell + 10 }))];
      for (const r of rects) for (const k of keep) assert.ok(r.x1 <= k.x0 || k.x1 <= r.x0 || r.y1 <= k.y0 || k.y1 <= r.y0, `${s.key} near marker/band`);
      for (const b of p.blocks) {
        assert.equal(!!b.hand, b.kind === "frac", `${s.key} ${b.no} hand`);
        if (b.hand) assert.ok(b.hand.num.y + b.hand.num.h < b.hand.bar.y && b.hand.bar.y < b.hand.den.y && b.hand.den.y + b.hand.den.h <= b.y + b.h);
        for (const g of b.grids) assert.equal(g.r, V2.BUB_R);
      }
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
test("cardHtml: 쪽마다 SVG 한 장 · viewBox · 분수 손글씨 칸 · 위쪽 띠 자리는 비움", () => {
  const s = SETS[0];
  const card = cardOf(s);
  const h = cardHtml(card);
  assert.equal((h.match(/<svg /g) || []).length, 3);
  assert.ok(h.includes(`viewBox="0 0 ${GW} ${GH}"`));
  const p0 = pageSvg(card, card.pages[0]);
  assert.ok(p0.includes(s.title) && p0.includes("1/3쪽") && p0.includes("분수 · 손으로"));
  // v2 쪽에는 예전 띠 자리(y 56~98, x 220~730)에 아무것도 그리지 않는다 — 예전 띠로 잘못 읽히지 않게
  for (const m of p0.matchAll(/<(rect|text|line|circle) ([^>]*)>/g)) {
    const a = Object.fromEntries([...m[2].matchAll(/([\w-]+)="([^"]*)"/g)].map((x) => [x[1], x[2]]));
    const y = Number(a.y ?? a.cy ?? a.y1), x = Number(a.x ?? a.cx ?? a.x1);
    if (Number.isFinite(y) && Number.isFinite(x) && x > 220 && x < 730) assert.ok(y > 112 || y < 50, `위쪽 띠 자리에 그림: ${m[0].slice(0, 60)}`);
  }
  assert.ok(cardHtml(cardOf(s, 1)).includes("분자"), "v1 그림도 그대로 그린다(시험용)");
});

// ── 합성 사진(tests/fixtures/omrsynth.mjs) ──────────────────────────────────────
/** 자리마다 칠할 숫자 — 오른쪽 맞춤. "" = 빈자리 */
function digitsRight(str, cols) { const d = String(str).split(""); return Array.from({ length: cols }, (_, i) => d[i - (cols - d.length)] ?? ""); }

/**
 * 한 쪽 그리기(인쇄 + 학생의 연필). fills: { [no]: 그 문항의 "쓰는 꼴" 또는 { cols: [[자리 숫자…]…] } (이상한 칠 시험용) · { faint: "숫자" }(흐리게)
 * v2 의 동그라미 속 숫자는 획 네모로 흉내 낸다 — 빈 동그라미 바탕(채움 ≈0.20)이 실제 인쇄를 찍은 사진(≈0.14)보다 무겁게.
 */
function drawPage(card, p, fills, { maskBand = false } = {}) {
  const v2 = (p.ver || card.ver) === 2;
  const r = raster(GW, GH, 236);
  for (const m of p.markers) fillRect(r, m.x, m.y, m.size, m.size, 24);
  fillRect(r, p.orient.x, p.orient.y, p.orient.w, p.orient.h, 24);
  if (!maskBand) bandCells(p.bandPos).forEach((c, i) => { if (p.band[i]) fillRect(r, c.x, c.y, c.size, c.size, 24); else strokeRect(r, c.x, c.y, c.size, c.size, 1, 215); });
  if (v2) {
    if (p.index === 0) {                                            // 제목 · 이름 · 날짜 · 안내 두 줄 (pageSvgV2 와 같은 자리)
      fillRect(r, 300, 126, 400, 28, 40);
      fillRect(r, 340, 166, 320, 18, 90);
      fillRect(r, 196, 225, 264, 2, 30); fillRect(r, 586, 225, 264, 2, 30);
      fillRect(r, 140, 240, 720, 14, 120); fillRect(r, 170, 261, 660, 14, 120);
    } else { fillRect(r, 290, 128, 420, 22, 40); fillRect(r, 260, 164, 480, 14, 120); }
  } else if (p.index === 0) {                                       // v1: 제목 · 이름 · 날짜 줄 흉내 (pageSvgV1 과 같은 자리)
    fillRect(r, 330, 136, 340, 24, 70);
    fillRect(r, 203, 229, 257, 2, 80); fillRect(r, 583, 229, 257, 2, 80);
    fillRect(r, 200, 244, 600, 12, 150);
  } else fillRect(r, 300, 134, 400, 18, 70);
  for (const b of p.blocks) {
    if (v2) fillRect(r, b.x + 4, b.y + 4, 13, 17, 20); else fillRect(r, b.x + 3, b.y + 4, 12, 15, 40);   // 번호
    if (b.hand) {
      for (const bx of [b.hand.num, b.hand.den]) strokeRect(r, bx.x, bx.y, bx.w, bx.h, 1.8, 40);
      fillRect(r, b.hand.bar.x1, b.hand.bar.y - 1.6, b.hand.bar.x2 - b.hand.bar.x1, 3.2, 20);
      fillRect(r, b.x + 30, b.y + 8, 60, 12, 110);                  // 「분수 · 손으로」
    } else if (b.kind === "pick") {
      for (const q of b.picks) {
        ring(r, q.x, q.y, q.r, 1.6, v2 ? 40 : 70);
        if (v2) strokeRect(r, q.x - 4.5, q.y - 5.5, 9, 11, 1.4, 120); else fillRect(r, q.x - 3, q.y - 4, 6, 8, 185);
      }
    } else {
      for (const g of b.grids) {
        for (const bx of g.boxes) strokeRect(r, bx.x, bx.y, bx.w, bx.h, v2 ? 1.3 : 1.2, v2 ? 60 : 85);
        for (const col of g.bubbles) for (const bb of col) {
          ring(r, bb.x, bb.y, g.r, v2 ? 1.5 : 1.4, v2 ? 40 : 75);
          if (v2) strokeRect(r, bb.x - 3.5, bb.y - 4.7, 7, 9.4, 1, 140); else fillRect(r, bb.x - 2.5, bb.y - 3.5, 5, 7, 190);
        }
      }
    }
    const f = fills[b.no];
    if (f == null) continue;
    const pen = (x, y, rad, k) => (k % 3 === 0 ? fillCircle(r, x + 0.8, y - 0.6, rad + 1.6, 120) : fillCircle(r, x, y, rad - 0.6, 52));
    if (b.hand) {
      const [n, d] = String(f).split("/");
      if (n) handText(r, b.hand.num, n, b.no % 2 ? 58 : 96);       // 짝수 번은 연하게
      if (d) handText(r, b.hand.den, d, b.no % 2 ? 58 : 96);
      continue;
    }
    if (b.kind === "pick") {
      const on = String(f).match(/[ㄱ-ㅎ]/gu) || [];
      for (const q of b.picks) if (on.includes(q.label)) pen(q.x, q.y, q.r, b.no);
      continue;
    }
    if (typeof f === "object" && f.faint != null) {                  // 흐리게 · 덜 칠함
      b.grids[0].bubbles.forEach((col, ci) => { const dg = digitsRight(f.faint, b.grids[0].cols)[ci]; if (dg !== "") fillCircle(r, col[+dg].x, col[+dg].y, b.grids[0].r * 0.75, 165); });
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
        pen(bb.x, bb.y, g.r, b.no + ci);
      }
    }));
  }
  return r;
}

const SET = SETS[0];
const CARD = cardOf(SET), CARD1 = cardOf(SET, 1);
const CARDS = { 2: CARD, 1: CARD1 };
const byNo = Object.fromEntries(SET.items.map((it) => [it.no, it]));
// 정답대로 칠하되 몇 문항은 일부러 비틀기
const FILLS = {};
for (const it of SET.items) FILLS[it.no] = rawOf(it);
const intItem = SET.items.find((it) => it.a.k === "int" && kindOf(it).cols[0] === 3 && it.no > 3);
const fracs = SET.items.filter((it) => it.a.k === "frac" && it.no > 3);
FILLS[2] = null;                                                         // 무응답
FILLS[intItem.no] = { cols: [[[1, 4], "2", "7"]] };                      // 첫 자리 두 개 칠함 → "?"
const gapNo = SET.items.find((it) => it.a.k === "int" && kindOf(it).cols[0] === 3 && it.no !== intItem.no && it.no > 3).no;
FILLS[gapNo] = { cols: [["1", "", "2"]] };                               // 가운데 빈자리 → "1?2"
const faintNo = SET.items.find((it) => it.a.k === "int" && kindOf(it).cols[0] === 3 && ![intItem.no, gapNo].includes(it.no) && it.no > 3).no;
FILLS[faintNo] = { faint: "35" };                                        // 흐리게 · 덜 칠함 → "35" 확인
const wrongNo = fracs[0].no; FILLS[wrongNo] = "6/9";                     // 약분 안 한 답(값이 다르면 오답) — v1 은 동그라미, v2 는 손글씨
const blankFrac = fracs[1].no; FILLS[blankFrac] = null;                  // 빈 분수 칸
const numOnly = fracs[2].no; FILLS[numOnly] = "1";                       // 분자 칸에만(0 · 1)
const expectRaw = (no) => {
  if (no === 2 || no === blankFrac) return "";
  if (no === intItem.no) return "?27";
  if (no === gapNo) return "1?2";
  if (no === faintNo) return "35";
  if (no === wrongNo) return "6/9";
  if (no === numOnly) return "1";
  return rawOf(byNo[no]);
};

function checkPage(res, p, ver = 2, { faint = true, conf = true } = {}) {
  assert.equal(res.ok, true, "ok (" + res.reason + ")");
  assert.equal(res.page, p.index);
  assert.equal(res.ver, ver);
  for (const b of p.blocks) {
    const a = res.answers.find((x) => x.no === b.no);
    assert.ok(a, "no " + b.no);
    if (b.hand) {                                                         // v2 분수: 글씨 유무만
      const want = FILLS[b.no];
      if (!want) { assert.equal(a.flag, null, `no ${b.no} 빈 손글씨 칸`); assert.equal(a.raw, ""); continue; }
      assert.equal(a.flag, "hand", `no ${b.no} 손글씨 ${JSON.stringify(a.hand)}`);
      assert.deepEqual(a.hand, { num: true, den: String(want).includes("/") }, `no ${b.no} 칸`);
      continue;
    }
    assert.equal(a.raw, expectRaw(b.no), `no ${b.no} (${b.kind}) got ${a.raw}`);
    if (conf && ![intItem.no, gapNo, faintNo].includes(b.no) && b.kind !== "pick") assert.ok(a.conf >= 0.5, `no ${b.no} conf ${a.conf}`);
  }
  const d = res.answers.find((x) => x.no === intItem.no); if (d) assert.equal(d.flag, "double");
  const g = res.answers.find((x) => x.no === gapNo); if (g) assert.equal(g.flag, "gap");
  const f = res.answers.find((x) => x.no === faintNo); if (f && faint) { assert.equal(f.flag, "weak"); assert.ok(f.conf < 0.5); }
}

console.log("OMR 판독 (합성 사진)");
const PAGES = CARD.pages.map((p) => drawPage(CARD, p, FILLS));
const pageOf = (no) => CARD.pages.find((p) => p.blocks.some((b) => b.no === no)).index;
test("1쪽: 기울여 찍은 사진 — 숫자 동그라미 · 손글씨 칸(글씨 유무) · 흐리게 칠한 칸", () => {
  const img = photograph(PAGES[0], 1300, 1820, [[95, 70], [1215, 110], [1250, 1745], [60, 1700]], 3);
  checkPage(readCardPhoto(img, CARDS), CARD.pages[0]);
});
test("2쪽: 띠(아래)로 쪽을 알아낸다 · 원근 심하게", () => {
  const img = photograph(PAGES[1], 1400, 1900, [[180, 120], [1180, 60], [1300, 1840], [70, 1760]], 7);
  checkPage(readCardPhoto(img, CARDS), CARD.pages[1]);
});
test("3쪽을 거꾸로(180°) 찍어도 · 카드 하나만 줘도", () => {
  const img = photograph(PAGES[2], 1300, 1820, [[1220, 1730], [80, 1760], [100, 90], [1190, 60]], 11);
  checkPage(readCardPhoto(img, CARD), CARD.pages[2]);
});
test("그림자 경계가 손글씨 칸을 가로질러도 빈 칸은 빈 칸 · 쓴 칸은 쓴 칸", () => {
  // 흐린 칠은 그림자 밖에서만 따로 본다. 반그림자에 걸친 연한 칠은 맞게 읽되 확신이 낮을 수 있다(노란 칸) — 값만 본다
  const F = { ...FILLS, [faintNo]: "35" };
  for (const k of [0, 1]) {
    const img = photograph(drawPage(CARD, CARD.pages[k], F), 1300, 1820, [[90, 80], [1210, 70], [1240, 1740], [70, 1750]], 13 + k, 100, 900);
    checkPage(readCardPhoto(img, CARDS), CARD.pages[k], 2, { faint: false, conf: false });
  }
});
test("손글씨 조각(handCrops): 쓴 분수 칸만 · 분자 칸 늘 · 분모 칸은 글씨 있을 때만 · 밝기 펴기", () => {
  const k = pageOf(numOnly);
  const res = readCardPhoto(photograph(PAGES[k], 1300, 1820, [[95, 70], [1215, 110], [1250, 1745], [60, 1700]], 17), CARDS);
  assert.equal(res.ok, true);
  const crops = handCrops(res);
  const want = CARD.pages[k].blocks.filter((b) => b.hand && FILLS[b.no]).map((b) => b.no);
  assert.deepEqual(crops.map((c) => c.no), want);
  for (const c of crops) {
    assert.ok(c.num.width >= 100 && c.num.width <= 130 && c.num.height >= 100 && c.num.height <= 130, `${c.no} 크기 ${c.num.width}×${c.num.height}`);
    assert.equal(!!c.den, String(FILLS[c.no]).includes("/"), `${c.no} 분모`);
    const g = c.num.gray, s = [...g].sort((a, b) => a - b);
    assert.ok(s[Math.floor(s.length * 0.5)] >= 240 && s[Math.floor(s.length * 0.005)] <= 40, `${c.no} 밝기 ${s[Math.floor(s.length * 0.5)]} · ${s[Math.floor(s.length * 0.005)]}`);
  }
  assert.ok(!crops.some((c) => c.no === blankFrac));
  const one = crops.find((c) => c.no === numOnly);
  if (one) assert.equal(one.den, null);
});
test("다른 세트의 카드면 거부(other-set)", () => {
  const other = cardOf(SETS[1]);
  const img = photograph(drawPage(other, other.pages[0], {}), 1200, 1700, [[60, 60], [1140, 60], [1140, 1640], [60, 1640]], 5);
  const r = readCardPhoto(img, CARDS);
  assert.equal(r.ok, false); assert.equal(r.reason, "other-set"); assert.equal(r.band.set, SETS[1].no);
});
test("마커가 없으면 markers", () => {
  const r = raster(GW, GH, 236);
  const img = photograph(r, 900, 1200, [[40, 40], [860, 40], [860, 1160], [40, 1160]], 2);
  assert.equal(readCardPhoto(img, CARDS).reason, "markers");
});
test("예전 카드(v1) 사진: 띠(위)로 판을 알아보고 분수 동그라미까지 그대로 읽는다", () => {
  CARD1.pages.forEach((p, k) => {
    const img = photograph(drawPage(CARD1, p, FILLS), 1300, 1820, k ? [[1210, 1740], [70, 1770], [95, 80], [1180, 50]] : [[80, 60], [1230, 95], [1260, 1760], [50, 1720]], 30 + k);
    const res = readCardPhoto(img, CARDS);
    checkPage(res, p, 1);
    for (const b of p.blocks.filter((x) => x.kind === "frac")) assert.equal(res.answers.find((a) => a.no === b.no).raw, expectRaw(b.no), `v1 분수 ${b.no}`);
  });
  // v2 카드만 주면 예전 카드는 version 으로 거부(엉뚱한 자리를 읽지 않는다)
  const r = readCardPhoto(photograph(drawPage(CARD1, CARD1.pages[0], FILLS), 1300, 1820, [[80, 60], [1230, 95], [1260, 1760], [50, 1720]], 33), CARD);
  assert.equal(r.ok, false); assert.equal(r.reason, "version");
});
test("띠를 못 읽으면 band → 쪽을 고르면 쪽 그림(layoutFit)으로 v1 · v2 를 가려 읽는다", () => {
  for (const [C, ver] of [[CARD, 2], [CARD1, 1]]) {
    const img = photograph(drawPage(C, C.pages[1], FILLS, { maskBand: true }), 1300, 1820, [[90, 70], [1220, 100], [1240, 1750], [60, 1710]], 40 + ver);
    assert.equal(readCardPhoto(img, CARDS).reason, "band");
    const res = readCardPhoto(img, CARDS, { page: 1 });
    checkPage(res, C.pages[1], ver);
    assert.equal(res.bandOk, false);
  }
});
test("다른 세트(20 · 38)도 세 쪽 모두 정답 그대로(분수는 손글씨 칸)", () => {
  for (const S of [SETS[19], SETS[37]]) {
    const C = cardOf(S);
    const F = Object.fromEntries(S.items.map((it) => [it.no, rawOf(it)]));
    C.pages.forEach((p, k) => {
      const img = photograph(drawPage(C, p, F), 1300, 1820, k === 1 ? [[1210, 1740], [70, 1770], [95, 80], [1180, 50]] : [[80, 60], [1230, 95], [1260, 1760], [50, 1720]], 20 + k);
      const r = readCardPhoto(img, { 2: C, 1: cardOf(S, 1) });
      assert.equal(r.ok, true, `${S.key} p${k} ${r.reason}`);
      assert.equal(r.page, k);
      for (const a of r.answers) {
        const b = p.blocks.find((x) => x.no === a.no);
        if (b.hand) assert.equal(a.flag, "hand", `${S.key} ${a.no}`);
        else assert.equal(a.raw, F[a.no], `${S.key} ${a.no}`);
      }
      assert.equal(handCrops(r).length, p.blocks.filter((b) => b.hand).length);
    });
  }
});
test("판독 → 판정: 약분 안 한 값이 다르면 오답, 두 번 칠한 자리는 채점 보류", () => {
  assert.equal(judge(byNo[wrongNo], "6/9").ok, byNo[wrongNo].a.n * 9 === byNo[wrongNo].a.d * 6);
  assert.equal(judge(byNo[intItem.no], "?27").ok, null);
});

console.log(`\n${passed} passed, ${failed} failed`);
if (failed) process.exit(1);
