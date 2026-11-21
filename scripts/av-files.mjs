// 기본기 해설(초등 · 중등 · 고등 단원 100가지) PDF 만들기 — 문제지 · 해설지 · 빠른 정답 · OMR (앱의 📄 문서와 같은 문서를 Chromium 으로 찍는다)
//
//   node scripts/av-files.mjs [--out .cf] [--manifest] [--only e-add,m-root | --level e] [--docs problems,solutions,answers,omr]
//
//   · 문서 HTML 은 앱과 같은 함수(src/features/display/frames/avprint.js)로 Chromium 안에서 만든다 — 그림(그림 DSL → 흑백 SVG,
//     frames/avfig.jsx)의 글자 폭을 그 브라우저의 캔버스로 재야 하므로. 이 스크립트는 그 코드를 esbuild 로 한 덩어리로 묶어 넣는다.
//   · 문제지 PDF 에는 등록 정보 ashrain-print.json(avManifest — 코드 · 번호 · 정답 · 쪽)을 붙인다(pdf-lib). 강사도구에 PDF 만 올리면 잡힌다.
//   · 문제지 쪽 수가 계산(단계마다 새 쪽 · 쪽마다 pp 문항)과 다르면 넘친 것 — 멈춘다(올리지 않는다). OMR 도 카드 쪽 수와 맞춘다.
// 만드는 것
//   <out>/av/<단원>/{problems,solutions,answers,omr}.pdf   Storage(concept-sets 버킷)에 올라갈 경로 그대로
//   <out>/build-av.json                                            sha256 · 크기 · 쪽 수 — scripts/push-concept-files.mjs 가 올리고 검사
//   --manifest 면 public/av-sets/files.json(쪽 수 · 크기)도 고친다 — 앱의 📄 문서 칸에 보이는 값(일부만 찍었으면 찍은 것만 바꿔 넣는다)
// 글꼴: 로컬 @fontsource 가 있으면(FONTSOURCE, 콜론 구분) 거기서, 없으면(워크플로) jsDelivr 에서 받는다.
// 워크플로 push-av-files 가 main 머지 때 이 스크립트로 PDF 를 만들고 Storage 에 올린다 — PDF 는 저장소에 넣지 않는다.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const need = (name) => {
  try { return require(name); } catch { return require(`/home/claude/.npm-global/lib/node_modules/${name}`); }
};
const { chromium } = need("playwright");
const { PDFDocument } = need("pdf-lib");

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const OUT = path.resolve(arg("--out", path.join(ROOT, ".cf")));
const ONLY = (arg("--only", "") || "").split(",").filter(Boolean);
const LEVEL = arg("--level", "");
const ALL_DOCS = ["problems", "solutions", "answers", "omr"];
const DOCS = (arg("--docs", "") || ALL_DOCS.join(",")).split(",").filter(Boolean);
if (DOCS.some((d) => !ALL_DOCS.includes(d))) throw new Error(`--docs 는 ${ALL_DOCS.join(" · ")} 중에서: ${DOCS}`);
const FONT_DIRS = (process.env.FONTSOURCE ?? "/tmp/fonts/node_modules/@fontsource").split(":").filter((d) => d && fs.existsSync(d));

const sha256 = (buf) => crypto.createHash("sha256").update(buf).digest("hex");
const pdfPages = (buf) => (Buffer.from(buf).toString("latin1").match(/\/Type\s*\/Page(?![s\w])/g) || []).length;
function localFont(url) {
  const m = url.match(/^https:\/\/cdn\.jsdelivr\.net\/npm\/@fontsource\/([^@/]+)@[^/]+\/(.+)$/);
  if (!m) return null;
  for (const d of FONT_DIRS) { const p = path.join(d, m[1], m[2]); if (fs.existsSync(p)) return p; }
  return null;
}

/* ── 앱 코드 묶기(브라우저용 한 덩어리) ── */
const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
const { BASICS } = await import(pathToFileURL(path.join(ROOT, "src/features/display/basics/index.js")).href);
const VAR = (id) => "S_" + id.replace(/-/g, "_");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "av-files-"));
const S = (p) => JSON.stringify(path.join(ROOT, p));
fs.writeFileSync(path.join(tmp, "entry.jsx"), `
import { BASICS } from ${S("src/features/display/basics/index.js")};
${BASICS.map((m) => `import { SET as ${VAR(m.id)} } from ${S(`src/features/display/basics/${m.id}.js`)};`).join("\n")}
import { avDocHtml, avManifest, avCard, problemPages } from ${S("src/features/display/frames/avprint.js")};
import { figSvg } from ${S("src/features/display/frames/avfig.jsx")};
import { cardHtml } from ${S("src/lib/omr/grid.js")};
import { composePrint } from ${S("src/pages/sets/printdoc.js")};
const DATA = { ${BASICS.map((m) => `${JSON.stringify(m.id)}: ${VAR(m.id)}`).join(", ")} };
const pick = (id) => ({ meta: BASICS.find((b) => b.id === id), set: DATA[id] });
/** 그림 글자에 쓰는 글자들 — 캔버스로 재기 전에 글꼴(유니코드 조각)을 미리 받아 둔다 */
const figChars = (id) => { const { set } = pick(id); let s = ""; for (const it of set.items) for (const el of it.fig?.els || []) if (el.k === "T") s += el.s; return [...new Set(s)].join(""); };
window.AVB = {
  doc(id, doc) {
    const { meta, set } = pick(id);
    if (doc === "omr") return composePrint([{ kind: "omr", html: cardHtml(avCard(meta, set.items)) }], meta.short + " OMR");
    return avDocHtml(meta, set, doc, figSvg);
  },
  manifest(id) { const { meta, set } = pick(id); return avManifest(meta, set); },
  omrPages(id) { const { meta, set } = pick(id); return avCard(meta, set.items).pages.length; },
  problemPages(id) { return problemPages(pick(id).set).length; },
  figChars,
};
`);
const bundle = path.join(tmp, "avb.js");
await build({ entryPoints: [path.join(tmp, "entry.jsx")], bundle: true, platform: "browser", format: "iife", jsx: "automatic", outfile: bundle,
  nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' }, minify: true });

/* ── Chromium ── */
const FONT_LINKS = [
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-kr@5.3.1/400.css",
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-kr@5.3.1/500.css",
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-kr@5.3.1/700.css",
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-serif@5.3.0/400-italic.css",
];
const browser = await chromium.launch();
let routed = 0, net = 0;
const route = async (pg) => pg.route("https://cdn.jsdelivr.net/**", (r) => {
  const p = FONT_DIRS.length ? localFont(r.request().url()) : null;
  if (!p) { net++; return r.continue(); }
  routed++;
  return r.fulfill({ status: 200, body: fs.readFileSync(p), headers: { "content-type": p.endsWith(".css") ? "text/css" : "font/woff2", "access-control-allow-origin": "*" } });
});
const maker = await browser.newPage();          // 문서 HTML 을 만드는 쪽(캔버스로 글자 폭을 잰다)
await route(maker);
await maker.setContent(`<!doctype html><html lang="ko"><head><meta charset="utf-8">${FONT_LINKS.map((u) => `<link rel="stylesheet" href="${u}">`).join("")}</head><body></body></html>`, { waitUntil: "networkidle" });
await maker.addScriptTag({ path: bundle });
const page = await browser.newPage();           // PDF 를 찍는 쪽
await route(page);

async function preloadFonts(id) {
  await maker.evaluate(async (i) => {
    const chars = window.AVB.figChars(i) + "가나다0123456789xyπ()";
    const faces = ["400 30px 'Noto Sans KR'", "500 30px 'Noto Sans KR'", "700 30px 'Noto Sans KR'", "italic 400 30px 'Noto Serif'"];
    await Promise.all(faces.map((f) => document.fonts.load(f, chars).catch(() => null)));
    await document.fonts.ready;
  }, id);
}
async function toPdf(html) {
  await page.setContent(html.replace(/<script\b[\s\S]*?<\/script>/gi, ""), { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
  return page.pdf({ preferCSSPageSize: true, printBackground: true });
}

const build_ = { v: 1, cat: "av", bucket: "concept-sets", made: new Date().toISOString(), sets: {} };
let bad = 0;
for (const meta of BASICS) {
  if (ONLY.length && !ONLY.includes(meta.id)) continue;
  if (LEVEL && meta.id[0] !== LEVEL) continue;
  const id = meta.id;
  const dir = path.join(OUT, "av", id);
  fs.mkdirSync(dir, { recursive: true });
  await preloadFonts(id);
  const entry = {};
  for (const doc of DOCS) {
    const html = await maker.evaluate(([a, c]) => window.AVB.doc(a, c), [id, doc]);
    if (/undefined|NaN|\[object Object\]/.test(html.replace(/<style[\s\S]*?<\/style>/g, ""))) { bad++; console.error(`✗ ${id} ${doc}: 글자에 undefined · NaN`); }
    let buf = Buffer.from(await toPdf(html));
    let pages = pdfPages(buf);
    if (doc === "problems") {
      const man = await maker.evaluate((a) => window.AVB.manifest(a), id);
      const pdf = await PDFDocument.load(buf);
      await pdf.attach(Buffer.from(JSON.stringify(man, null, 1), "utf8"), "ashrain-print.json",
        { mimeType: "application/json", description: "ashrain.print 등록 정보", creationDate: new Date(), modificationDate: new Date() });
      buf = Buffer.from(await pdf.save({ useObjectStreams: false }));
      pages = pdf.getPageCount();
      const want = await maker.evaluate((a) => window.AVB.problemPages(a), id);
      if (pages !== want) { bad++; console.error(`✗ ${id} 문제지: 쪽 수 ${pages} ≠ ${want} (칸이 넘쳤다)`); }
    }
    if (doc === "omr") {
      const want = await maker.evaluate((a) => window.AVB.omrPages(a), id);
      if (pages !== want) { bad++; console.error(`✗ ${id} OMR: 쪽 수 ${pages} ≠ ${want}`); }
    }
    fs.writeFileSync(path.join(dir, `${doc}.pdf`), buf);
    entry[doc] = { path: `av/${id}/${doc}.pdf`, bytes: buf.length, pages, sha256: sha256(buf) };
  }
  build_.sets[id] = entry;
  console.log(`  ${id.padEnd(10)} ${meta.span.padEnd(8)} ${meta.short.padEnd(12)} ` + [["problems", "문제"], ["solutions", "해설"], ["answers", "정답"], ["omr", "OMR"]]
    .filter(([d]) => entry[d]).map(([d, l]) => `${l} ${entry[d].pages}쪽`).join(" · "));
}
await browser.close();

const n = Object.keys(build_.sets).length;
const total = Object.values(build_.sets).reduce((t, e) => t + Object.values(e).reduce((a, x) => a + x.bytes, 0), 0);
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "build-av.json"), JSON.stringify(build_, null, 1) + "\n");
console.log(`\n${n}세트 · PDF ${n * DOCS.length}개 · ${(total / 1e6).toFixed(1)} MB · 글꼴 로컬 ${routed} / 네트워크 ${net}`);
if (process.argv.includes("--manifest")) {
  const fp = path.join(ROOT, "public/av-sets/files.json");
  const partial = ONLY.length || LEVEL || DOCS.length < ALL_DOCS.length;
  const files = partial && fs.existsSync(fp) ? JSON.parse(fs.readFileSync(fp, "utf8")) : { v: 1, bucket: build_.bucket, made: "", sets: {} };
  files.made = build_.made.slice(0, 10);
  for (const [id, e] of Object.entries(build_.sets)) {
    files.sets[id] = { ...(partial ? files.sets[id] : {}), ...Object.fromEntries(Object.entries(e).map(([d, x]) => [d, { path: x.path, pages: x.pages, bytes: x.bytes }])) };
  }
  fs.mkdirSync(path.dirname(fp), { recursive: true });
  fs.writeFileSync(fp, JSON.stringify(files) + "\n");
  console.log(`목록 → ${path.relative(ROOT, fp)}`);
}
fs.rmSync(tmp, { recursive: true, force: true });
if (bad) { console.error(`맞지 않는 문서 ${bad}개 — 올리지 않는다`); process.exit(1); }
