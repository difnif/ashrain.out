// 생성기 자료(json) 한 장면 그려 보기: node shot2.mjs <json> <번호,번호> <theme> <q|end|0.5> → png
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";
const ROOT = process.env.ASHRAIN_REPO || path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
const [js, nos, th = "dark", when = "end"] = process.argv.slice(2);
const entry = "/tmp/cv/shot2-entry.jsx";
fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE, SceneTitle } from "${ROOT}/src/features/display/draw.jsx";
import { L10Art } from "${ROOT}/src/features/display/frames/lin10.jsx";
import { l10Plan } from "${ROOT}/src/features/display/lin10.js";
export const shot = (S, no, th, when) => { const it = S.items[no - 1]; const C = PALETTE[th]; const P = l10Plan(it);
  const t = when === "end" ? P.ans + 900 : when === "q" ? 1200 : P.lines[Math.min(P.lines.length - 1, Math.floor(Number(when) * P.lines.length))].a + 900;
  return '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><rect width="1600" height="900" fill="'+C.bg[1]+'"/>' +
    renderToStaticMarkup(<g><SceneTitle title={S.title} sub={it.st + "단계 " + S.stages[it.st] + " · " + it.no + "번"} C={C} mode="m" /><L10Art it={it} t={t} C={C} /></g>) + '</svg>'; };
`);
await build({ entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: "/tmp/cv/shot2.mjs",
  nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
  banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" } });
const m = await import(pathToFileURL("/tmp/cv/shot2.mjs").href + "?" + Date.now());
const S = JSON.parse(fs.readFileSync(js, "utf8"));
const require = createRequire(import.meta.url);
const { chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright");
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
const outs = [];
for (const n of String(nos).split(",")) {
  const svg = m.shot(S, Number(n), th, when);
  const f = js.replace(/\.json$/, `-${n}-${when}.html`);
  fs.writeFileSync(f, `<html><head><link rel="stylesheet" href="file:///tmp/cv/pretendard.css"><style>body{margin:0}</style></head><body>${svg}</body></html>`.replace("<svg", "<svg style='font-family:Pretendard Variable,Pretendard,Noto Sans KR,sans-serif'"));
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(120);
  const png = f.replace(/\.html$/, ".png");
  await p.screenshot({ path: png });
  outs.push(png);
}
await b.close();
console.log(outs.join(" "));
