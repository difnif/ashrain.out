// 래스터(회색조 raw) → 앱 검출기(detect.js)로 마커 찾기 → 펴기 → 쪽 번호 띠·품질 읽기
// 사용: node read_pages.mjs <repo> <raster_dir(meta.json + pN.gray)> <assess.json> [--warp]
import fs from "node:fs";
import { pathToFileURL } from "node:url";
const [repo, dir, jpath] = process.argv.slice(2);
const SAVE = process.argv.includes("--warp");
const det = await import(pathToFileURL(repo + "/src/lib/omr/detect.js").href);
const sh = await import(pathToFileURL(repo + "/src/lib/assess/sheet.js").href);
const J = JSON.parse(fs.readFileSync(jpath, "utf8"));
const spec = sh.sheetSpec(J.sheet);
const meta = JSON.parse(fs.readFileSync(dir + "/meta.json", "utf8"));
const out = {};
for (const [key, { width: w, height: h }] of Object.entries(meta)) {
  const gray = new Uint8Array(fs.readFileSync(`${dir}/${key}.gray`));
  const bin = det.threshold(gray, w, h);
  const quad = det.findMarkers(bin, w, h);
  if (!quad) { out[key] = { ok: false, reason: "markers" }; continue; }
  const o = det.orientCorners(gray, w, h, quad, spec);
  if (!o) { out[key] = { ok: false, reason: "orient" }; continue; }
  const scale = 1.4;
  const warped = det.warpToSpec(gray, w, h, o.corners, spec, scale);
  warped.scale = scale;
  const code = sh.readPageCode(warped, J.sheet);
  const q = sh.pageQuality(warped);
  if (SAVE) fs.writeFileSync(`${dir}/${key}.warped.gray`, Buffer.from(warped.gray));
  out[key] = { ok: code.ok, page: code.page, check: code.check, bits: code.bits.join(""), contrast: code.contrast, margin: code.margin,
    shift: o.shift, quality: q, judge: sh.judgeQuality(q), size: [warped.width, warped.height] };
}
process.stdout.write(JSON.stringify(out));
