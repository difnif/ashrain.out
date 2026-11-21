// 그림이 있는 문항 중 글자가 넘쳐 그림이 빠지는(noFig) 문항 찾기: node figfit.mjs <json>...
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
const ROOT = process.env.ASHRAIN_REPO || path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
const entry = "/tmp/cv/figfit-entry.jsx";
fs.writeFileSync(entry, `export { layoutOf } from "${ROOT}/src/features/display/frames/lin10.jsx";`);
await build({ entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: "/tmp/cv/figfit.mjs",
  nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
  banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" } });
const m = await import(pathToFileURL("/tmp/cv/figfit.mjs").href + "?" + Date.now());
for (const js of process.argv.slice(2)) {
  const S = JSON.parse(fs.readFileSync(js, "utf8"));
  const bad = [], small = [];
  for (const it of S.items) {
    const Lo = m.layoutOf(it);
    if (it.fig && Lo.noFig) bad.push(it.no);
    if (Lo.bs <= 28 && !Lo.noFig) small.push(it.no);
  }
  console.log(path.basename(js), "그림 빠짐", bad.length, bad.join(","), "| 글자 28", small.length);
}
