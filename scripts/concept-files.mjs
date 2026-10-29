// 컨셉 문제 PDF 만들기 — 문제지 · 해설지 · OMR 카드 (앱의 「바로 인쇄」와 같은 문서를 Chromium 으로 찍는다)
//
//   node scripts/concept-files.mjs [--cat prob] [--out .concept-files] [--manifest] [--only 01,02]
//
//   · 문제지 · 해설지: public/concept-sets/<범주>/print/NN-{problems,solutions}.html — 생성기(guard-daily)가 PDF 를 찍은
//     바로 그 HTML(글꼴만 jsDelivr 고정 버전)이라 쪽 나눔 · 모양이 처음 배포한 PDF 와 같다. 쪽 수가 index.json 과 다르면 멈춘다.
//   · OMR 카드: grid.js → printdoc.composePrint (앱에서 인쇄하는 것과 같은 문서).
// 만드는 것
//   <out>/<범주>/NN/{problems,solutions,omr}.pdf     Storage 에 올라갈 경로 그대로
//   <out>/build-<범주>.json                           sha256 · 크기 · 쪽 수 — scripts/push-concept-files.mjs 가 올리고 검사할 때 쓴다
//   --manifest 면 public/concept-sets/<범주>/files.json(쪽 수 · 크기)도 고친다 — 앱의 자료 칸에 보이는 값
// 글꼴: 로컬 @fontsource 가 있으면(FONTSOURCE, 콜론 구분) 거기서, 없으면(워크플로) jsDelivr 에서 받는다.
// 워크플로 push-concept-files 가 main 머지 때 이 스크립트로 PDF 를 만들고 Storage 에 올린다 — PDF 는 저장소에 넣지 않는다.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";
import { layoutCard, cardHtml } from "../src/lib/omr/grid.js";
import { composePrint } from "../src/pages/sets/printdoc.js";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); } catch { ({ chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright")); }

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const CAT = arg("--cat", "prob");
const OUT = path.resolve(arg("--out", path.join(ROOT, ".concept-files")));
const ONLY = (arg("--only", "") || "").split(",").filter(Boolean);
const PUB = path.join(ROOT, "public/concept-sets", CAT);
const FONT_DIRS = (process.env.FONTSOURCE ?? "/home/claude/ashrain.out/assessgen/node_modules/@fontsource:/home/claude/work/guard-daily/fonts/node_modules/@fontsource")
  .split(":").filter((d) => d && fs.existsSync(d));

const sha256 = (buf) => crypto.createHash("sha256").update(buf).digest("hex");
const pad2 = (n) => String(n).padStart(2, "0");
/** Chromium(Skia) PDF 의 쪽 수 — 쪽 객체 사전은 압축되지 않는다 */
const pdfPages = (buf) => (Buffer.from(buf).toString("latin1").match(/\/Type\s*\/Page(?![s\w])/g) || []).length;

function localFont(url) {
  const m = url.match(/^https:\/\/cdn\.jsdelivr\.net\/npm\/@fontsource\/([^@/]+)@[^/]+\/(.+)$/);
  if (!m) return null;
  for (const d of FONT_DIRS) { const p = path.join(d, m[1], m[2]); if (fs.existsSync(p)) return p; }
  return null;
}

const index = JSON.parse(fs.readFileSync(path.join(PUB, "index.json"), "utf8")).categories.find((c) => c.id === CAT);
if (!index) throw new Error(`index.json 에 범주 ${CAT} 가 없다`);
fs.mkdirSync(path.join(OUT, CAT), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage();
let routed = 0, net = 0;
await page.route("https://cdn.jsdelivr.net/**", (route) => {
  const p = FONT_DIRS.length ? localFont(route.request().url()) : null;
  if (!p) { net++; return route.continue(); }
  routed++;
  return route.fulfill({ status: 200, body: fs.readFileSync(p), headers: { "content-type": p.endsWith(".css") ? "text/css" : "font/woff2", "access-control-allow-origin": "*" } });
});

async function toPdf() {
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  return page.pdf({ preferCSSPageSize: true, printBackground: true });
}

const build = { v: 1, cat: CAT, bucket: "concept-sets", made: new Date().toISOString(), sets: {} };
let bad = 0;
for (const s of index.sets) {
  const nn = pad2(s.no);
  if (ONLY.length && !ONLY.includes(nn)) continue;
  const set = JSON.parse(fs.readFileSync(path.join(PUB, `${nn}.json`), "utf8"));
  const dir = path.join(OUT, CAT, nn);
  fs.mkdirSync(dir, { recursive: true });
  const entry = {};
  for (const doc of ["problems", "solutions"]) {
    const src = path.join(PUB, "print", `${nn}-${doc}.html`);
    await page.goto(pathToFileURL(src).href, { waitUntil: "networkidle" });
    const buf = await toPdf();
    fs.writeFileSync(path.join(dir, `${doc}.pdf`), buf);
    entry[doc] = { path: `${CAT}/${nn}/${doc}.pdf`, bytes: buf.length, pages: pdfPages(buf), sha256: sha256(buf) };
    if (entry[doc].pages !== s.pages[doc]) { bad++; console.error(`✗ ${set.key} ${doc}: 쪽 수 ${entry[doc].pages} ≠ index ${s.pages[doc]}`); }
  }
  const card = layoutCard({ cat: CAT, no: set.no, title: set.title, short: set.short, items: set.items });
  await page.setContent(composePrint([{ kind: "omr", html: cardHtml(card) }], `${set.key} OMR`).replace(/<script>[\s\S]*?<\/script>/g, ""), { waitUntil: "networkidle" });
  const buf = await toPdf();
  fs.writeFileSync(path.join(dir, "omr.pdf"), buf);
  entry.omr = { path: `${CAT}/${nn}/omr.pdf`, bytes: buf.length, pages: pdfPages(buf), sha256: sha256(buf) };
  if (entry.omr.pages !== card.pages.length) { bad++; console.error(`✗ ${set.key} OMR: 쪽 수 ${entry.omr.pages} ≠ ${card.pages.length}`); }
  build.sets[nn] = entry;
  console.log(`  ${set.key.padEnd(10)} 문제 ${entry.problems.pages}쪽 · 해설 ${entry.solutions.pages}쪽 · OMR ${entry.omr.pages}쪽`);
}
await browser.close();

const n = Object.keys(build.sets).length;
const total = Object.values(build.sets).reduce((t, e) => t + e.problems.bytes + e.solutions.bytes + e.omr.bytes, 0);
fs.writeFileSync(path.join(OUT, `build-${CAT}.json`), JSON.stringify(build, null, 1) + "\n");
console.log(`\n${n}세트 · PDF ${n * 3}개 · ${(total / 1e6).toFixed(1)} MB · 글꼴 로컬 ${routed} / 네트워크 ${net}`);
if (process.argv.includes("--manifest") && !ONLY.length) {
  const files = { v: 1, cat: CAT, bucket: build.bucket, made: build.made.slice(0, 10), sets: {} };
  for (const [nn, e] of Object.entries(build.sets)) {
    files.sets[nn] = Object.fromEntries(Object.entries(e).map(([d, x]) => [d, { path: x.path, pages: x.pages, bytes: x.bytes }]));
  }
  fs.writeFileSync(path.join(PUB, "files.json"), JSON.stringify(files) + "\n");
  console.log(`목록 → ${path.relative(ROOT, path.join(PUB, "files.json"))}`);
}
if (bad) { console.error(`쪽 수가 맞지 않는 문서 ${bad}개 — 올리지 않는다`); process.exit(1); }
