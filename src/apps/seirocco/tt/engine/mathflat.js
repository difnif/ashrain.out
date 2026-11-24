// 매쓰플랫 학습지 PDF 해체 (PC mf2exam.parse · mfanswer · mfsolution.parse_solutions)
import { openPdf, pageSpans, pageGraphics, imageData, renderClip, inkColor, isBlue, spanWords, pageLines, gray, crop, newImg, paste, fillRect,
  bboxWhere, cropGray, resizeGray, toPng } from "./base";

const ANS_MARK = ["빠른정답", "정답과 해설"];
const GENERIC = new Set(["일일 TEST", "유형별 학습", "MATH SQUARE", "실시일자", "이름"]);
const nos = (s) => s.replace(/\s+/g, "");

// 쪽 하나 읽기 — 글자 덩이 + 그림 + (필요하면) 색을 보려고 그린 그림
async function readPage(doc, i, { dpi = 0 } = {}) {
  const page = await doc.getPage(i + 1);
  const gfx = await pageGraphics(page);
  const sp = await pageSpans(page, gfx.ops);
  const vp = page.getViewport({ scale: 1 });
  const r = { page, sp, gfx, W: vp.width, H: vp.height, text: nos(pageLines(sp).map((l) => l.text).join("")) };
  if (dpi) { r.im = await renderClip(page, null, dpi); r.s = dpi / 72; }
  return r;
}
async function colorize(pg, spans) {
  if (!pg.im) { pg.im = await renderClip(pg.page, null, 144); pg.s = 2; }
  for (const s of spans) if (s.color === undefined) { const c = inkColor(pg.im, pg.s, [s.x, s.y + (s.y1 - s.y) * 0.15, s.x1, s.y1 - (s.y1 - s.y) * 0.1]); s.color = c; s.blue = isBlue(c); }
}

const isNumCand = (s) => /^\d{2,3}$/.test(s.t) && s.size > 15 && (!s.font || /Bold/i.test(s.font));

function guessTitles(sp) {
  const cand = sp.filter((s) => !s.isNum && !GENERIC.has(s.t) && s.y < 200);
  const big = cand.filter((s) => s.size >= 13 && !/\d+문제|선생님|쪽/.test(s.t));
  if (!big.length) return ["", ""];
  const top = Math.max(...big.map((s) => s.size));
  const tl = big.filter((s) => Math.abs(s.size - top) < 0.5).sort((a, b) => Math.round(a.y) - Math.round(b.y) || a.x - b.x);
  const title = tl.map((s) => s.t).join(" ").replace(/^(유형별 학습|일일 TEST|MATH SQUARE)\s+/, "").trim();
  const below = cand.filter((s) => s.y > tl[tl.length - 1].y + 5 && s.size >= 9.5 && s.size < top && !/\d+문제|선생님/.test(s.t)).sort((a, b) => a.y - b.y);
  return [title, below.length ? below[0].t : ""];
}

// → {doc, items:[{no, img, tag, rate}], ansFrom, title, sub, pages:[...읽은 쪽]}
export async function parse(bytes) {
  const doc = await openPdf(bytes);
  const items = [];
  let ansFrom = null, first = null;
  for (let pi = 0; pi < doc.numPages; pi++) {
    const pg = await readPage(doc, pi);
    if (pi === 0) first = pg;
    const sp = pg.sp;
    const heads = sp.filter((s) => ANS_MARK.some((m) => nos(s.t).includes(nos(m)))).map((s) => s.y);
    const limit = heads.length ? Math.min(...heads) - 4 : pg.H + 1;
    const cand = sp.filter((s) => isNumCand(s) && s.y < limit);
    if (cand.length) await colorize(pg, cand);
    const nums = cand.filter((s) => s.blue);
    nums.forEach((s) => (s.isNum = true));
    const mid = pg.W / 2;
    const imgs = pg.gfx.imgs.filter((im) => {
      const w = im.bbox[2] - im.bbox[0];
      const dpi = (im.w / Math.max(w, 1)) * 72;
      return w >= 120 && w <= pg.W * 0.9 && dpi < 600;
    });
    for (const n of nums) {
      const col = n.x > mid;
      const same = nums.filter((m) => (m.x > mid) === col).sort((a, b) => a.y - b.y);
      const nx = same.find((m) => m.y > n.y + 1);
      const nxt = nx ? nx.y : limit;
      const body = imgs.filter((im) => (im.bbox[0] > mid) === col && n.x < im.bbox[0] && im.bbox[0] < n.x + 80 && n.y - 12 <= im.bbox[1] && im.bbox[1] < nxt - 4)
        .sort((a, b) => a.bbox[1] - b.bbox[1]);
      if (!body.length) continue;
      const pieces = [];
      for (const im of body) { const d = await imageData(pg.page, im); if (d) pieces.push([im, d]); }
      if (!pieces.length) continue;
      let img;
      if (pieces.length === 1) img = pieces[0][1];
      else {
        const k0 = pieces[0][1].w / (pieces[0][0].bbox[2] - pieces[0][0].bbox[0]);
        const top = pieces[0][0].bbox[1];
        const H = Math.trunc(Math.max(...pieces.map(([im]) => (im.bbox[3] - top) * k0))) + 2;
        const W = Math.max(...pieces.map(([, p]) => p.w));
        img = newImg(W, H);
        for (const [im, p] of pieces) paste(img, p, 0, Math.trunc((im.bbox[1] - top) * k0));
      }
      const tagS = sp.find((s) => s.t.startsWith("|") && Math.abs(s.y - (n.y - 11)) < 6 && Math.abs(s.x - n.x) < 20);
      const rateS = sp.find((s) => s.t.startsWith("정답률") && Math.abs(s.y - (n.y - 11)) < 6 && s.x - n.x > 0 && s.x - n.x < 140);
      items.push({ no: Number(n.t), img, tag: tagS ? tagS.t.replace(/^[|\s]+|[|\s]+$/g, "") : null, rate: rateS ? rateS.t : null });
    }
    if (heads.length) { ansFrom = pi; break; }
  }
  items.sort((a, b) => a.no - b.no);
  const [title, sub] = first ? guessTitles(first.sp) : ["", ""];
  return { doc, items, ansFrom, title, sub };
}

export async function titleOf(doc) {
  try {
    const pg = await readPage(doc, 0);
    const lines = pageLines(pg.sp).map((l) => l.text.trim()).filter(Boolean);
    for (const l of lines) if ((l.includes("유형별") || l.includes("TEST") || l.includes("학습")) && l.length > 6) return nos(l);
    return lines.length ? nos(lines[0]) : "";
  } catch { return ""; }
}
export async function isAnswerOnly(doc) {
  try { return doc.numPages > 0 && (await readPage(doc, 0)).text.includes("빠른정답"); } catch { return false; }
}

// ── 빠른정답 (mfanswer)
const TEMPLATES = [
  ["2", "03e007f80c38181c101c001c00180038007000e001c0038007000e061ffc1ffc"], ["4", "006000e001e003e007e007e00ce01ce038e070e070e0fffc00e000e000e000e0"],
  ["2", "03e00ff01c381018301c001800380030007000e001c0038007000e041ffc3ff8"], ["1", "01c007c00fc001c001c001c001c001c001c001c001c001c001c003c007f00ff0"],
  ["3", "07e00e70183810380038007000e003e003f00038001c001c001c001818381ff0"], ["2", "07e00ff01838301c201c001c00380038007000e001c0038007000e061fbc3ffc"],
  ["1", "03c007c00bc001c001c001c001c001c001c001c001c001c001c001c007e00ff0"], ["5", "000003f807000e000c001f800fe000780038001c001c001c001800383c703fe0"],
  ["1", "01c007c00fc001c001c001c001c001c001c001c001c001c001c001c007f00ff0"], ["2", "03c00ff01838301c201c001c00180030007000e001c0038007000e043ffc3ff8"],
  ["4", "00e000e001e003e007e00fe00ce01ce038e070e071e0fffc01e000e000e000e0"], ["4", "006000e001e003e007e007e00ce018e038e070e070e0fffc01e000e000e000e0"],
];
const TPL = TEMPLATES.map(([lab, h]) => [lab, [...BigInt("0x" + h).toString(2).padStart(256, "0")].map(Number)]);

export async function answerPages(doc, start = 0) {
  const out = [];
  for (let i = start; i < doc.numPages; i++) if ((await readPage(doc, i)).text.includes("빠른정답")) out.push(i);
  return out;
}
async function feature(page, rect) {
  const g = await renderClip(page, rect, 300, true);
  const bb = bboxWhere(g, (v) => v < 128);
  if (!bb) return null;
  const c = cropGray(g, ...bb);
  const { w, h } = c;
  if (w < 8 || h < 8) return null;
  const inner = cropGray(c, Math.trunc(w * 0.22), Math.trunc(h * 0.18), Math.trunc(w * 0.78), Math.trunc(h * 0.82));
  const r = resizeGray(inner, 16, 16);
  return [...r.g].map((v) => (v < 160 ? 1 : 0));
}
async function classifyChoice(page, rect) {
  const f = await feature(page, rect);
  if (!f) return null;
  const best = {};
  for (const [lab, t] of TPL) {
    let d = 0;
    for (let i = 0; i < 256; i++) if (f[i] !== t[i]) d++;
    best[lab] = Math.min(best[lab] ?? 999, d);
  }
  const ranked = Object.entries(best).sort((a, b) => a[1] - b[1]);
  const [[lab, d1], [, d2]] = ranked;
  return d1 <= 35 && d2 - d1 >= 15 ? lab : null;
}
// {번호: {page, rect:[x0,y0,x1,y1], choice, text}}
export async function parseQuick(doc, pages = null) {
  const res = {};
  for (const pno of pages ?? (await answerPages(doc))) {
    const pg = await readPage(doc, pno);
    const H = pg.H;
    let top = 0;
    for (const s of pg.sp) if (nos(s.t) === "빠른정답") top = Math.max(top, s.y1);
    const cand = pg.sp.filter((s) => /^\d{1,3}$/.test(s.t) && s.y > top && s.y1 < H * 0.95);
    await colorize(pg, cand);
    const nums = cand.filter((s) => s.blue || s.bold).map((s) => [Number(s.t), [s.x, s.y, s.x1, s.y1]]);
    if (nums.length < 2) continue;
    const imgs = pg.gfx.imgs.map((im) => im.bbox);
    const words = spanWords(pg.sp);
    const rightEdge = imgs.length ? Math.max(...imgs.map((r) => r[2])) : pg.W * 0.5;
    for (const [n, nb] of nums) {
      const b0 = nb[1] - 3, b1 = nb[3] + 3;
      const nxt = nums.filter(([, r]) => r[0] > nb[2] + 2 && Math.abs(r[1] - nb[1]) < 4).map(([, r]) => r[0]);
      const limit = nxt.length ? Math.min(...nxt) - 2 : rightEdge + 2;
      const parts = imgs.filter((r) => r[0] >= nb[2] - 1 && r[0] < limit && r[3] > b0 - 8 && r[1] < b1 + 8 && Math.min(r[3], b1) - Math.max(r[1], b0) > 0);
      const texts = words.filter((w) => w.x >= nb[2] - 1 && w.x < limit && Math.abs((w.y + w.y1) / 2 - (nb[1] + nb[3]) / 2) < 6 && !/^\d{2}$/.test(w.t));
      if (!parts.length && !texts.length) continue;
      let u = parts.length ? parts[0].slice() : [texts[0].x, texts[0].y, texts[0].x1, texts[0].y1];
      const uni = (r) => { u = [Math.min(u[0], r[0]), Math.min(u[1], r[1]), Math.max(u[2], r[2]), Math.max(u[3], r[3])]; };
      parts.forEach(uni);
      texts.forEach((w) => uni([w.x, w.y, w.x1, w.y1]));
      let choice = null;
      if (parts.length && !texts.length && parts.every((r) => { const w = r[2] - r[0], h = r[3] - r[1]; return w / Math.max(h, 0.1) > 0.8 && w / Math.max(h, 0.1) < 1.25 && h < 16; })) {
        const labs = [];
        for (const r of [...parts].sort((a, b) => a[0] - b[0])) labs.push(await classifyChoice(pg.page, r));
        if (labs.every(Boolean)) choice = labs.join(",");
      }
      res[n] = { page: pno, rect: u, choice, text: texts.length && !parts.length ? texts.map((w) => w.t).join(" ") : "" };
    }
  }
  return res;
}
export async function renderQuick(doc, info, dpi = 220) {
  const page = await doc.getPage(info.page + 1);
  const r = info.rect;
  const im = await renderClip(page, [r[0] - 2, r[1] - 2, r[2] + 2, r[3] + 2], dpi);
  return { png: await toPng(im), wh: [r[2] - r[0] + 4, r[3] - r[1] + 4] };
}

// ── 해설 쪽 (mfsolution)
export async function solutionPages(doc, start = 0) {
  const res = [];
  for (let i = start; i < doc.numPages; i++) {
    const t = (await readPage(doc, i)).text;
    if (t.includes("빠른정답") && !["정답과해설", "정답및해설"].some((m) => t.includes(m))) continue;
    res.push(i);
  }
  return res;
}
function trim(im, pad = 6) {
  const g = gray(im);
  let x0 = im.w, y0 = im.h, x1 = -1, y1 = -1;
  for (let y = 0; y < im.h; y++) for (let x = 0; x < im.w; x++) {
    const i = (y * im.w + x) * 4;
    // ImageChops.difference(흰 바탕).convert("L") > 18
    const dl = ((255 - im.d[i]) * 19595 + (255 - im.d[i + 1]) * 38470 + (255 - im.d[i + 2]) * 7471 + 0x8000) >>> 16;
    if (dl > 18) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; y1 = y; }
  }
  void g;
  if (x1 < 0) return null;
  return crop(im, Math.max(0, x0 - pad), Math.max(0, y0 - pad), Math.min(im.w, x1 + 1 + pad), Math.min(im.h, y1 + 1 + pad));
}
// → [{원래 번호: {img, w(pt), h(pt)}}, 번호를 찾은 쪽들]
export async function parseSolutions(doc, pages, dpi = 200) {
  const res = {}, used = [];
  const k = dpi / 72;
  for (const pno of pages) {
    const pg = await readPage(doc, pno, { dpi });
    const H = pg.H, W = pg.W;
    const cand = pg.sp.filter((s) => /^\d{1,3}$/.test(s.t) && s.y > H * 0.05 && s.y < H * 0.95 && s.size >= 8.5);
    await colorize(pg, cand);
    const ok = cand.filter((s) => s.blue || s.bold || /Bold/.test(s.font));
    const groups = new Map();
    for (const s of ok) {
      const key = `${Math.round(s.size)}|${s.blue ? 1 : 0}|${/Bold/.test(s.font) || s.bold ? 1 : 0}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(s);
    }
    if (!groups.size) continue;
    const nums = [...groups.values()].sort((a, b) => (b.filter((s) => s.blue).length - a.filter((s) => s.blue).length) || b.length - a.length || b[0].size - a[0].size)[0];
    if (!nums.length) continue;
    used.push(pno);
    const mid = W / 2;
    const foot = pg.sp.filter((s) => s.y > H * 0.92).map((s) => s.y);
    const bottom = foot.length ? Math.min(...foot) - 3 : H - 24;
    const left = Math.min(...nums.map((s) => s.x)) - 6;
    const two = nums.some((s) => s.x > mid) && nums.some((s) => s.x < mid);
    for (const n of nums) {
      const rc = two && n.x > mid;
      const cx0 = rc ? mid + 2 : Math.max(0, left);
      const cx1 = rc || !two ? W - Math.max(0, left) : mid - 2;
      const same = nums.filter((m) => (two && m.x > mid) === rc).sort((a, b) => a.y - b.y);
      const nx = same.find((m) => m.y > n.y + 2);
      const nxt = nx ? nx.y : bottom;
      const clip = [cx0, n.y - 2, cx1, Math.max(n.y + 10, nxt - 3)];
      let im = crop(pg.im, clip[0] * k, clip[1] * k, clip[2] * k, clip[3] * k);
      fillRect(im, Math.trunc((n.x - clip[0] - 1) * k), 0, Math.trunc((n.x1 - clip[0] + 2) * k), Math.trunc((n.y1 - clip[1] + 2) * k));
      im = trim(im);
      if (!im) continue;
      const no = Number(n.t);
      if (res[no]) {
        const prev = res[no].img;
        const cat = newImg(Math.max(prev.w, im.w), prev.h + im.h + 8);
        paste(cat, prev, 0, 0);
        paste(cat, im, 0, prev.h + 8);
        im = cat;
      }
      res[no] = { img: im, w: im.w / k, h: im.h / k };
    }
  }
  return [res, used];
}

// 이름 지운 쪽 그림 (번호를 못 찾은 해설 쪽 · 원본 모양 정답해설) — 그림으로 바꾸며 이름 자리를 희게
export async function pageImageNoNames(doc, pno, names, dpi = 200) {
  const pg = await readPage(doc, pno, { dpi });
  const k = dpi / 72;
  const set = new Set(names.filter((n) => n && n.length >= 2));
  const lines = pageLines(pg.sp);
  for (const l of lines) {
    // 「이름」 칸 오른쪽 값
    const li = l.spans.findIndex((s) => /^(이름|성명|Name|NAME)\s*[:：]?$/.test(s.t));
    if (li >= 0) for (const s of l.spans.slice(li + 1, li + 3)) if (s.t.length <= 14) fillRect(pg.im, (s.x - 1) * k, (s.y - 1) * k, (s.x1 + 1) * k, (s.y1 + 1) * k);
  }
  for (const s of pg.sp) {
    for (const n of set) if (s.t.includes(n) && (s.y1 < pg.H * 0.16 || s.y > pg.H * 0.93 || s.t === n)) fillRect(pg.im, (s.x - 1) * k, (s.y - 1) * k, (s.x1 + 1) * k, (s.y1 + 1) * k);
  }
  return { png: await toPng(pg.im), w: pg.W, h: pg.H };
}
