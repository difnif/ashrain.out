// 앱의 pipeline.analyzePhoto 를 사진 흉내 래스터에 돌린다 (capture.js 와 같은 순서: 1600 축소본에서 마커 → 원본으로 펴기)
import fs from "node:fs";
import { pathToFileURL } from "node:url";
const [repo, dir, jpath] = process.argv.slice(2);
const { analyzePhoto } = await import(pathToFileURL(repo + "/src/lib/assess/pipeline.js").href);
const { readRegion } = await import(pathToFileURL(repo + "/src/lib/assess/sheet.js").href);
const J = JSON.parse(fs.readFileSync(jpath, "utf8"));
const set = { sheet: J.sheet, pages: J.pages };
function shrink(gray, w, h, side) {          // 넓이 평균 축소(브라우저 drawImage 근사)
  const sc = Math.min(1, side / Math.max(w, h));
  const W = Math.round(w * sc), H = Math.round(h * sc);
  const out = new Uint8Array(W * H);
  const fx = w / W, fy = h / H;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    let s = 0, n = 0;
    for (let yy = Math.floor(y * fy); yy < Math.min(h, Math.floor((y + 1) * fy)); yy++)
      for (let xx = Math.floor(x * fx); xx < Math.min(w, Math.floor((x + 1) * fx)); xx++) { s += gray[yy * w + xx]; n++; }
    out[y * W + x] = n ? s / n : 255;
  }
  return { gray: out, width: W, height: H, sc: W / w };
}
const meta = JSON.parse(fs.readFileSync(dir + "/meta.json", "utf8"));
const res = {}; let pass = 0, fail = 0;
for (const [k, m] of Object.entries(meta)) {
  const gray = new Uint8Array(fs.readFileSync(`${dir}/${k}.gray`));
  const full = { gray, width: m.width, height: m.height };
  const t0 = Date.now();
  const small = shrink(gray, m.width, m.height, 1600);
  const r = analyzePhoto(full, small, set);
  const ms = Date.now() - t0;
  let good;
  if (m.expect === "ok") good = r.ok && r.page === m.page;
  else if (m.expect === "fail") good = !r.ok;
  else good = !r.ok && r.reason === m.expect;
  if (r.ok) { const reg = readRegion(set.pages.find((p) => p.no === r.page)); r.region = reg; delete r.warped; }
  res[k] = { good, expect: m.expect, ok: r.ok, page: r.page, reason: r.reason, quality: r.quality, shift: r.shift, ms };
  good ? pass++ : fail++;
}
console.log(JSON.stringify(res, null, 1));
console.log(`${pass} pass / ${fail} fail`);
process.exit(fail ? 1 : 0);
