// ashrain.out — 생성 풀 도형 가독성 검사 (itemfactory/tools/legible.mjs, v1.0)
//
// out/gen/*_pool.json 의 question figure(scene)를 figsvg로 실제로 그려 보고, SVG 안의
//   · 글자 상자끼리 겹침 (라벨·점 이름·각도 표시가 서로 포개짐)
//   · 글자 상자가 선분을 가로지름 (라벨이 변 위에 얹힘)
// 을 찾아 틀별로 센다. 제약을 풀 때 "그림이 찌그러져 읽기 어려운 것"을 각도 상한 대신 이걸로 거른다.
// 파이프라인(genkit)과 무관한 검수 도구 — DB를 읽지 않는다.
//
// 실행:  node itemfactory/tools/legible.mjs                      # out/gen 전량
//        node itemfactory/tools/legible.mjs --dir out/s11          # 다른 산출 폴더
//        node itemfactory/tools/legible.mjs --tpl m2-2-tri-similar-t1 --list 20   # 틀 하나, 문제 항목 20건 나열
//        node itemfactory/tools/legible.mjs --json out/legible.json # 결과 JSON 저장
//
// 판정 기준(픽셀, 렌더 viewBox 기준): 글자 상자 교차 면적이 두 상자 중 작은 것의 25% 이상이면 '겹침',
// 선분이 글자 몸통(상자를 가로 70%·세로 40%로 줄인 것)을 지나가면 '선 위'. 절대 기준이 아니라 제약을 바꾸기 전후의 비교용이다. 글자 폭은 글꼴 크기 × (ASCII 0.58 / 그 밖 0.95)로 어림한다.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { figureToHtml1 } from "../../src/lib/figsvg.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i < 0 ? d : argv[i + 1]; };
const DIR = path.resolve(ROOT, arg("--dir", "out/gen"));
const TPL = arg("--tpl", null);
const LIST = Number(arg("--list", 0)) || 0;
const JSON_OUT = arg("--json", null);

// ---------------------------------------------------------------- SVG 파싱(정규식 — figsvg가 내는 단순 SVG 전용)
const attr = (tag, name) => { const m = tag.match(new RegExp(`\\s${name}="([^"]*)"`)); return m ? m[1] : null; };
const unesc = (s) => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&");

function textBoxes(svg) {
  const fs0 = Number((svg.match(/<svg[^>]*font-size="([\d.]+)"/) || [])[1]) || 13;
  const out = [];
  const re = /<text([^>]*)>([^<]*)<\/text>/g;
  let m;
  while ((m = re.exec(svg))) {
    const tag = m[1], text = unesc(m[2]).trim();
    if (!text) continue;
    const x = Number(attr(tag, "x")), y = Number(attr(tag, "y"));
    const size = Number(attr(tag, "font-size")) || fs0;
    const anchor = attr(tag, "text-anchor") || "middle";
    let w = 0;
    for (const ch of text) w += size * (/[\x20-\x7e]/.test(ch) ? 0.58 : 0.95);
    const sym = text.length === 1 && /[•∘×○●]/.test(text);            // 각 표시 기호는 작다 (폭·높이 모두 반)
    if (sym) w = size * 0.5;
    const x0 = anchor === "start" ? x : anchor === "end" ? x - w : x - w / 2;
    out.push({ text, k: attr(tag, "data-k"), x0, x1: x0 + w, y0: y - size * (sym ? 0.55 : 0.78), y1: y + size * (sym ? 0.05 : 0.22) });
  }
  return out;
}

function dots(svg) {
  const out = [];
  const re = /<circle([^>]*)\/>/g;
  let m;
  while ((m = re.exec(svg))) {
    const t = m[1];
    const r = Number(attr(t, "r"));
    if (r <= 3.5) out.push({ x: +attr(t, "cx"), y: +attr(t, "cy") });
  }
  return out;
}
const distToSeg = (px, py, l) => {
  const dx = l.x2 - l.x1, dy = l.y2 - l.y1, L2 = dx * dx + dy * dy || 1;
  const t = Math.max(0, Math.min(1, ((px - l.x1) * dx + (py - l.y1) * dy) / L2));
  return Math.hypot(px - (l.x1 + t * dx), py - (l.y1 + t * dy));
};

function lines(svg) {
  const out = [];
  const re = /<line([^>]*)\/>/g;
  let m;
  while ((m = re.exec(svg))) {
    const t = m[1];
    out.push({ x1: +attr(t, "x1"), y1: +attr(t, "y1"), x2: +attr(t, "x2"), y2: +attr(t, "y2"), k: attr(t, "data-k") });
  }
  return out;
}

const overlapArea = (a, b) => Math.max(0, Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0)) * Math.max(0, Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0));
const area = (a) => (a.x1 - a.x0) * (a.y1 - a.y0);

function segCrossesBox(l, b) {
  // 상자 가장자리를 스치는 것은 무시하고 글자 몸통(가로 70%·세로 40%)을 지나가는 선만 센다
  const px = 0.15 * (b.x1 - b.x0), py = 0.3 * (b.y1 - b.y0);
  const x0 = b.x0 + px, x1 = b.x1 - px, y0 = b.y0 + py, y1 = b.y1 - py;
  if (x1 <= x0 || y1 <= y0) return false;
  // Liang–Barsky
  let t0 = 0, t1 = 1;
  const dx = l.x2 - l.x1, dy = l.y2 - l.y1;
  for (const [p, q] of [[-dx, l.x1 - x0], [dx, x1 - l.x1], [-dy, l.y1 - y0], [dy, y1 - l.y1]]) {
    if (p === 0) { if (q < 0) return false; continue; }
    const r = q / p;
    if (p < 0) { if (r > t1) return false; if (r > t0) t0 = r; }
    else { if (r < t0) return false; if (r < t1) t1 = r; }
  }
  return t0 < t1;
}

function inspect(svg) {
  const boxes = textBoxes(svg), ls = lines(svg), ds = dots(svg);
  const issues = [];
  for (let i = 0; i < boxes.length; i++) {
    for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], b = boxes[j];
      const ov = overlapArea(a, b);
      if (ov > 0 && ov >= 0.25 * Math.min(area(a), area(b))) issues.push({ kind: "겹침", a: a.text, b: b.text, ka: a.k, kb: b.k });
    }
  }
  for (const b of boxes) {
    const cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2;
    // 글자가 붙어 있는 점(20px 안의 가장 가까운 점): 그 점을 지나는 선은 정상(점 이름은 원래 선 곁에 놓인다)
    let own = null, best = 20;
    for (const d of ds) { const dd = Math.hypot(d.x - cx, d.y - cy); if (dd < best) { best = dd; own = d; } }
    for (const l of ls) {
      if (Math.hypot(l.x1 - cx, l.y1 - cy) < 18 || Math.hypot(l.x2 - cx, l.y2 - cy) < 18) continue;
      if (own && distToSeg(own.x, own.y, l) < 2.5) continue;
      if (segCrossesBox(l, b)) { issues.push({ kind: "선위", a: b.text, ka: b.k, line: l.k }); break; }
    }
  }
  return issues;
}

// ---------------------------------------------------------------- 풀 순회
const files = fs.readdirSync(DIR).filter((f) => f.endsWith("_pool.json")).sort();
const stat = {};   // tpl → {n, scene, bad, byKind, samples[]}
const flagged = [];
for (const f of files) {
  const items = JSON.parse(fs.readFileSync(path.join(DIR, f), "utf8"));
  for (const it of items) {
    const tpl = it.template_id;
    if (TPL && tpl !== TPL) continue;
    const st = stat[tpl] || (stat[tpl] = { n: 0, scene: 0, bad: 0, byKind: {}, samples: [] });
    st.n++;
    const figs = Array.isArray(it.figure) ? it.figure : it.figure ? [it.figure] : [];
    const scenes = figs.filter((g) => g && g.fn === "scene");
    if (!scenes.length) continue;
    st.scene++;
    let issues = [];
    for (const g of scenes) {
      const r = figureToHtml1(g, {});
      if (r.kind !== "svg") { issues.push({ kind: "미렌더", a: (r.warnings || []).join(";") }); continue; }
      issues = issues.concat(inspect(r.html));
    }
    if (issues.length) {
      st.bad++;
      for (const is of issues) st.byKind[is.kind] = (st.byKind[is.kind] || 0) + 1;
      if (st.samples.length < 5) st.samples.push({ key: it.item_key, issues });
      flagged.push({ tpl, key: it.item_key, idx: it.param_index, issues });
    }
  }
}

const rows = Object.entries(stat).filter(([, s]) => s.scene).sort((a, b) => b[1].bad / b[1].scene - a[1].bad / a[1].scene);
let totScene = 0, totBad = 0;
for (const [tpl, s] of rows) {
  totScene += s.scene; totBad += s.bad;
  const kinds = Object.entries(s.byKind).map(([k, v]) => `${k} ${v}`).join(", ");
  console.log(`${tpl.padEnd(32)} 도형 ${String(s.scene).padStart(4)} · 문제 ${String(s.bad).padStart(4)} (${(100 * s.bad / s.scene).toFixed(0).padStart(3)}%)  ${kinds}`);
}
console.log(`\n합계: scene 도형 ${totScene}건 중 문제 ${totBad}건 (${totScene ? (100 * totBad / totScene).toFixed(1) : 0}%)`);
if (LIST) {
  for (const fl of flagged.slice(0, LIST)) {
    console.log(`  ${fl.key}  ` + fl.issues.map((i) => i.kind === "겹침" ? `${i.kind}[${i.a}|${i.b}]` : `${i.kind}[${i.a}${i.line ? " × " + i.line : ""}]`).join("  "));
  }
}
if (JSON_OUT) fs.writeFileSync(path.resolve(ROOT, JSON_OUT), JSON.stringify({ dir: DIR, stat, flagged }, null, 1));
