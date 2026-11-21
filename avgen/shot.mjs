// 학년별 해설 한 장면 그려 보기: node shot.mjs <학년> <세트> <번호> <theme> <frac|end> [out]
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
const ROOT = process.env.ASHRAIN_REPO || path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
const [g, sk, no, th = "dark", when = "end", out = `/tmp/cv/${g}${sk}${no}${th}${when}.png`] = process.argv.slice(2);
const entry = "/tmp/cv/shot-entry.jsx";
fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE, SceneTitle } from "${ROOT}/src/features/display/draw.jsx";
import { L10Art } from "${ROOT}/src/features/display/frames/lin10.jsx";
import { l10Plan } from "${ROOT}/src/features/display/lin10.js";
import { SETS } from "${ROOT}/src/features/display/grades/${g}.js";
import { gradeOf } from "${ROOT}/src/features/display/grades/index.js";
export const shot = (sk, no, th, when) => { const it = SETS[sk].items[no - 1]; const C = PALETTE[th]; const P = l10Plan(it);
  const meta = gradeOf("${g}").sets.find((s) => s.key === sk);
  const t = when === "end" ? P.ans + 900 : when === "q" ? 1200 : P.lines[Math.min(P.lines.length - 1, Math.floor(Number(when) * P.lines.length))].a + 900;
  return '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><rect width="1600" height="900" fill="'+C.bg[1]+'"/>' +
    renderToStaticMarkup(<g><SceneTitle title={meta.title} sub={it.st + "단계 " + meta.stages[it.st] + " · " + it.no + "번"} C={C} mode="m" /><L10Art it={it} t={t} C={C} /></g>) + '</svg>'; };
`);
await build({ entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: "/tmp/cv/shot.mjs",
  nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
  banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" } });
const m = await import(pathToFileURL("/tmp/cv/shot.mjs").href + "?" + Date.now());
const items = String(no).split(",");
const files = [];
for (const n of items) {
  const svg = m.shot(sk, Number(n), th, when);
  const f = `/tmp/cv/${g}${sk}${n}${th}${when}.html`;
  fs.writeFileSync(f, `<html><head><link rel="stylesheet" href="file:///tmp/cv/pretendard.css"><style>body{margin:0}</style></head><body>${svg}</body></html>`.replace("<svg", "<svg style='font-family:Pretendard Variable,Pretendard,Noto Sans KR,sans-serif'"));
  files.push(f);
}
console.log(files.join("\n"));
