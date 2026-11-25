// 움직이는 예시(학기 파일) 그려 보기 — 머지된 재생 카드(components/ConceptAv.jsx · L10Art)와 같은 판으로 — node cvgen/shot.mjs <단원> <id,id…|all> <light|dark> <w|n> <q|p|0|1|…|a|end|ms숫자…(쉼표)> [out.png]
//   id 마다 순간들을 한 줄로 이어 붙인 그림 한 장(여러 id 면 세로로). 글꼴은 시스템 Noto Sans CJK 로 어림(화면은 Pretendard).
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const [unit, ids0, th = "light", lay = "w", whens = "end", out = "/tmp/cvshot/out.png"] = process.argv.slice(2);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "cvshot-"));
const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
const entry = path.join(tmp, "e.jsx");
fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${JSON.stringify(path.join(ROOT, "src/features/display/draw.jsx"))};
import { L10Art } from ${JSON.stringify(path.join(ROOT, "src/features/display/frames/lin10.jsx"))};
import { avView, avSpan, AV_WIDE, AV_NARROW } from ${JSON.stringify(path.join(ROOT, "src/components/ConceptAv.jsx"))};
export function when(it, w) {
  const S = avSpan(it), P = S.P;
  if (w === "q") return S.t0; if (w === "p") return P.plan[0] + 1800; if (w === "a") return P.ans + 300; if (w === "end") return S.t1;
  if (/^m\\d+$/.test(w)) return Number(w.slice(1));
  const i = Number(w); const L = P.lines[Math.min(P.lines.length - 1, i)]; return (L.a + L.b) / 2;
}
export function svg(it, t, th, wide) {
  const R = wide ? AV_WIDE : AV_NARROW, V = avView(it, R);
  const [x0, y0, w, h] = V.vb.split(" ").map(Number);
  return { w, h, s: renderToStaticMarkup(<svg xmlns="http://www.w3.org/2000/svg" viewBox={V.vb} width={w} height={h}><L10Art it={it} t={t} C={PALETTE[th]} uid={"s" + Math.round(t)} region={R} /></svg>) };
}
`);
const bundle = path.join(tmp, "b.mjs");
await build({ entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: bundle,
  nodePaths: [path.join(ROOT, "node_modules")], logLevel: "error", define: { "process.env.NODE_ENV": '"production"' },
  banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" } });
const m = await import(pathToFileURL(bundle).href);
const data = JSON.parse(fs.readFileSync(path.join(ROOT, "public/concept-av", `${unit}.json`), "utf8"));
const ids = ids0 === "all" ? Object.keys(data.items) : ids0.split(",");
const wide = lay === "w";
const rows = [];
for (const id of ids) {
  const it = data.items[id];
  if (!it) { console.error("없음", id); continue; }
  const cells = whens.split(",").map((w) => m.svg(it, m.when(it, w), th, wide));
  rows.push({ id, cells });
}
const scale = Number(process.env.SC || (wide ? 0.32 : 0.6));
const cols = Number(process.env.COLS || 1);
let html = `<html><head><meta charset="utf-8"><style>body{margin:0;background:#888;font-family:'Pretendard','Noto Sans CJK KR','Noto Sans KR',sans-serif}
.g{display:flex;flex-wrap:wrap;gap:6px;width:${cols > 1 ? "var(--gw)" : "auto"}}.b{display:block}
.r{display:flex;gap:6px;margin:0 0 6px 0;align-items:flex-start}.c{background:#fff}.id{font:12px monospace;color:#fff;padding:2px 4px}</style></head><body><div class="g">`;
let W = 0, H = 0, rowH = 0, colI = 0, lineW = 0;
for (const r of rows) {
  html += `<div class="b"><div class="id">${r.id}</div><div class="r">`;
  let rw = 0, rh = 0;
  for (const c of r.cells) {
    html += `<div class="c" style="width:${c.w * scale}px;height:${c.h * scale}px">${c.s.replace("<svg", `<svg style="width:${c.w * scale}px;height:${c.h * scale}px"`)}</div>`;
    rw += c.w * scale + 6; rh = Math.max(rh, c.h * scale);
  }
  html += `</div></div>`;
  lineW += rw + 6; rowH = Math.max(rowH, rh + 24);
  colI++;
  if (colI >= cols) { W = Math.max(W, lineW); H += rowH; colI = 0; lineW = 0; rowH = 0; }
}
if (colI) { W = Math.max(W, lineW); H += rowH; }
html = html.replace("var(--gw)", `${Math.ceil(W) + 4}px`);
html += `</div></body></html>`;
const hf = path.join(tmp, "p.html");
fs.writeFileSync(hf, html);
fs.mkdirSync(path.dirname(out), { recursive: true });
execFileSync("google-chrome", ["--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", `--window-size=${Math.ceil(W) + 10},${Math.ceil(H) + 10}`,
  `--screenshot=${out}`, `file://${hf}`], { stdio: "ignore" });
console.log(out, Math.ceil(W), Math.ceil(H));
