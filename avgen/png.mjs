// html(svg) 파일들 → png (Playwright Chromium)
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright");
const files = process.argv.slice(2);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
for (const f of files) {
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(150);
  await p.screenshot({ path: f.replace(/\.html$/, ".png") });
}
await b.close();
console.log("png", files.length);
