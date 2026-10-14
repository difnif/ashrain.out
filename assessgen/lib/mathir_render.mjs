// MathIR 문장 → HTML (앱과 같은 렌더러로 PDF 를 만들기 위해). 사용: node mathir_render.mjs <repo> < {"texts":[...]}
import fs from "node:fs";
import { pathToFileURL } from "node:url";
const repo = process.argv[2];
const m = await import(pathToFileURL(repo + "/src/lib/mathir.js").href);
const input = JSON.parse(fs.readFileSync(0, "utf8"));
const out = { html: [], errs: [], css: m.MATH_CSS };
for (const t of input.texts) {
  const v = m.parseText(String(t));
  out.errs.push(v.errs.map((e) => `${e.src} (${e.code})`));
  out.html.push(m.renderHtml(String(t)));
}
process.stdout.write(JSON.stringify(out));
