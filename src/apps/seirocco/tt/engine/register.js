// 강사도구 엔진 — 프린트 등록 (PC printreg · anon) · 정답 PDF 붙이기 · 보관함 초안
import { openPdf, pdflib, embedText, pageSpans, pageLines, pageGraphics, renderClip, gray, crop, newImg, paste, fillRect, bboxWhere, toPng,
  imgHash, A4W, A4H } from "./base";
import { fmtCode, buildAnswerPdf, TEMPLATE_KEYS } from "./layout";
import { nn } from "../sb";
import { settings, reserveCode, storePrint } from "./print";
import { parseQuick, renderQuick, solutionPages, parseSolutions, pageImageNoNames } from "./mathflat";

const CODE_ALPHA = "23456789ABCDEFGHJKMNPQRSTUVWXYZ";
const CIRC = "①②③④⑤⑥⑦⑧⑨⑩";
const validCode = (c) => { c = [...String(c || "").toUpperCase()].filter((ch) => CODE_ALPHA.includes(ch)).join(""); return c.length === 6 ? c : null; };

// ── 초안(화면에서 확인하는 동안만 이 브라우저에 둠): 「_draft/<id>/…」 주소로 그림을 보여 준다
const DRAFTS = new Map();
let dseq = 0;
const urlCache = new Map();
export function draftUrl(rel) {
  if (urlCache.has(rel)) return urlCache.get(rel);
  const m = /^_draft\/([^/]+)\/(.+)$/.exec(rel);
  const d = m && DRAFTS.get(m[1]);
  const b = d && d.files.get(m[2]);
  if (!b) return null;
  const u = URL.createObjectURL(new Blob([b], { type: /\.png$/i.test(rel) ? "image/png" : "application/octet-stream" }));
  urlCache.set(rel, u);
  return u;
}

// ── 등록 정보 (PDF 첨부 ashrain-print.json)
async function readManifest(doc) {
  try {
    const at = await doc.getAttachments();
    for (const k of Object.keys(at || {})) {
      const a = at[k];
      if (!/\.json$/i.test(a.filename || k)) continue;
      try {
        const m = JSON.parse(new TextDecoder("utf-8").decode(a.content).replace(/^﻿/, ""));
        if (m && typeof m === "object" && m.kind === "ashrain.print") return m;
      } catch { /* 다음 */ }
    }
  } catch { /* 없음 */ }
  return null;
}
function checkManifest(m) {
  if (!m || typeof m !== "object" || m.kind !== "ashrain.print") throw new Error("등록 정보 형식이 아니에요 (kind가 ashrain.print 여야 해요)");
  if (!Array.isArray(m.items) || !m.items.length) throw new Error("등록 정보에 문항(items)이 없어요");
  return m;
}

// ── 쪽 정보 모으기
async function readDoc(bytes) {
  const doc = await openPdf(bytes);
  const pages = [];
  for (let i = 0; i < doc.numPages; i++) {
    const page = await doc.getPage(i + 1);
    const g = await pageGraphics(page);
    const sp = await pageSpans(page, g.ops);
    const vp = page.getViewport({ scale: 1 });
    pages.push({ page, sp, lines: pageLines(sp), edges: g.edges, W: vp.width, H: vp.height });
  }
  return { doc, pages };
}

const NUM_RE = /^(\d{1,2})(\s*[.)]|번)?(?=\s|$)/;
const ESSAY_RE = /^\[?\s*(서답형|서술형|주관식|단답형)\s*(\d{1,2})\s*(\]|[.)]|번)/;
function cands(D) {
  const out = [];
  D.pages.forEach((pg, pno) => {
    for (const ln of pg.lines) {
      let m = ESSAY_RE.exec(ln.text);
      if (m) { out.push({ ...ln, page: pno, n: Number(m[2]), kind: "essay", style: m[1], W: pg.W }); continue; }
      if (/^\[\s*(서답형|서술형|주관식)\s*$/.test(ln.text)) { out.push({ ...ln, page: pno, n: null, kind: "essay", style: ln.text.replace(/^[[\s]+|[[\s]+$/g, ""), W: pg.W }); continue; }
      m = NUM_RE.exec(ln.first) || NUM_RE.exec(ln.text);
      if (m) {
        const n = Number(m[1]);
        if (n >= 1 && n <= 99) out.push({ ...ln, page: pno, n, kind: "num", style: (m[2] || "").trim() || "-", W: pg.W });
      }
    }
  });
  return out;
}
function chain(group) {
  if (!group.length) return [];
  const W = group[0].W;
  const xs = [...new Set(group.map((c) => Math.round(c.x)))];
  const two = xs.some((x) => x > W * 0.45) && xs.some((x) => x < W * 0.3);
  const key = (c) => [c.page, two && c.x > W * 0.45 ? 1 : 0, c.y];
  const seq = [...group].sort((a, b) => { const ka = key(a), kb = key(b); return ka[0] - kb[0] || ka[1] - kb[1] || ka[2] - kb[2]; });
  let best = [];
  seq.forEach((c, i) => {
    if (c.n !== 1) return;
    const run = [];
    let want = 1;
    for (const d of seq.slice(i)) if (d.n === want) { run.push(d); want++; }
    if (run.length > best.length) best = run;
  });
  return best;
}
function score(run) {
  if (!run.length) return -1;
  const pages = new Set(run.map((c) => c.page)).size;
  const gaps = [];
  for (let i = 1; i < run.length; i++) if (run[i].page === run[i - 1].page) gaps.push(run[i].y - run[i - 1].y);
  const avg = gaps.length ? gaps.reduce((a, b) => a + b, 0) / gaps.length : 300;
  return run.length * 10 + pages * 4 + Math.min(avg / 40, 6) - (avg < 28 ? 60 : 0);
}
function detectItems(D) {
  const cs = cands(D);
  const groups = new Map();
  for (const c of cs) {
    if (c.kind !== "num") continue;
    const k = [c.style, c.size, c.font, c.bold].join("|");
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(c);
  }
  let best = [];
  for (const g of groups.values()) { const r = chain(g); if (score(r) > score(best)) best = r; }
  if (score(best) < 15) best = [];
  const items = best.map((c) => ({ label: String(c.n), page: c.page, x: c.x, y: c.y, kind: "num", size: c.size }));
  const order = (c) => [c.page, c.x > c.W * 0.45 ? 1 : 0, c.y];
  const cmp = (a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2];
  const last = best.length ? order(best[best.length - 1]) : [-1, -1, -1];
  let want = 1;
  for (const c of cs.filter((c) => c.kind === "essay" && cmp(order(c), last) > 0).sort((a, b) => cmp(order(a), order(b)))) {
    const n = c.n != null ? c.n : want;
    if (n === want) { items.push({ label: `${c.style} ${n}`, page: c.page, x: c.x, y: c.y, kind: "essay", size: c.size }); want++; }
  }
  return items;
}
function contentBottom(pg) {
  const ys = pg.lines.filter((l) => l.y > pg.H * 0.9).map((l) => l.y);
  return ys.length ? Math.min(...ys) - 4 : pg.H - 24;
}
const columnOf = (it, W, two) => (!two ? [18, W - 18] : it.x < W * 0.45 ? [14, W / 2 - 9] : [W / 2 + 9, W - 14]);
function bandTop(lines, it, x0, x1) {
  let top = it.y;
  for (const ln of lines) {
    if (!(x0 - 2 <= ln.x && ln.x <= x1) || ln.y >= it.y) continue;
    if (ln.y1 > it.y + 2) top = Math.min(top, ln.y);
    else if (ln.x > it.x + 15 && ln.y >= it.y - 18 && ln.y1 > it.y - 4) top = Math.min(top, ln.y);
  }
  return top;
}
function regions(D, items) {
  if (!items.length) return [];
  const W = D.pages[0].W;
  const two = items.some((it) => it.x > W * 0.45) && items.some((it) => it.x < W * 0.3);
  return items.map((it, i) => {
    const pg = D.pages[it.page];
    const [x0, x1] = columnOf(it, W, two);
    const top = Math.max(0, bandTop(pg.lines, it, x0, x1) - 5);
    let bottom = contentBottom(pg);
    for (const nx of items.slice(i + 1)) {
      const c = columnOf(nx, W, two);
      if (nx.page === it.page && c[0] === x0 && c[1] === x1 && nx.y > it.y) { bottom = bandTop(D.pages[nx.page].lines, nx, x0, x1) - 6; break; }
    }
    for (const ln of pg.lines) {
      if (x0 - 2 <= ln.x && ln.x <= x1 && top + 20 < ln.y && ln.y < bottom && /^(■|※ 다음|\[서답형 문항|◆)/.test(ln.text)) { bottom = ln.y - 6; break; }
    }
    return [it.page, [x0, top, x1, Math.max(top + 20, bottom)]];
  });
}

// ── 자르기 (150dpi) — 가장자리 긴 줄 지우기 · 여백 줄이기
function eraseEdgeRules(im) {
  const g = gray(im);
  const { w, h } = g;
  const bandX = Math.max(4, Math.trunc(w * 0.12));
  const xs = [...Array(bandX).keys()].concat([...Array(bandX).keys()].map((i) => w - bandX + i));
  for (const x of xs) {
    let dark = 0;
    for (let y = 0; y < h; y += 2) if (g.g[y * w + x] < 140) dark++;
    if (dark > 0.55 * (h / 2)) fillRect(im, x, 0, x + 1, h);
  }
  const bandY = Math.max(4, Math.trunc(h * 0.06));
  const ys = [...Array(bandY).keys()].concat([...Array(bandY).keys()].map((i) => h - bandY + i));
  for (const y of ys) {
    let dark = 0;
    for (let x = 0; x < w; x += 2) if (g.g[y * w + x] < 140) dark++;
    if (dark > 0.8 * (w / 2)) fillRect(im, 0, y, w, y + 1);
  }
  return im;
}
function squeezeBlank(im, keep = 28, minRun = 70) {
  const g = gray(im);
  const { w, h } = g;
  const blank = [];
  for (let y = 0; y < h; y++) { let mn = 255; for (let x = 0; x < w; x++) { const v = g.g[y * w + x]; if (v < mn) mn = v; } blank.push(mn > 225); }
  let rows = [], run = [];
  for (let y = 0; y < h; y++) {
    if (blank[y]) { run.push(y); continue; }
    if (run.length) { rows = rows.concat(run.length < minRun ? run : run.slice(0, keep / 2).concat(run.slice(-keep / 2))); run = []; }
    rows.push(y);
  }
  rows = rows.concat(run.slice(0, keep));
  if (rows.length >= h * 0.97) return im;
  const out = newImg(w, rows.length);
  rows.forEach((y, i) => out.d.set(im.d.subarray(y * w * 4, (y + 1) * w * 4), i * w * 4));
  return out;
}
async function cropItem(page, rect, dpi = 150) {
  let im = await renderClip(page, rect, dpi);
  im = eraseEdgeRules(im);
  const box = bboxWhere(gray(im), (v) => 255 - v > 30);
  if (box) { const pad = 8; im = crop(im, Math.max(0, box[0] - pad), Math.max(0, box[1] - pad), Math.min(im.w, box[2] + pad), Math.min(im.h, box[3] + pad)); }
  return squeezeBlank(im);
}
const looksChoice = (pg, r) => {
  const t = pg.sp.filter((s) => s.x >= r[0] - 1 && s.x1 <= r[2] + 1 && s.y >= r[1] - 1 && s.y1 <= r[3] + 1).map((s) => s.t).join("");
  return [..."①②③④⑤"].filter((ch) => t.includes(ch)).length >= 4;
};

// ── 정답지 읽기
function normAnswer(s) {
  s = String(s).trim().replace(/^,+|,+$/g, "").trim().replace(/^답\s*[:：]\s*/, "");
  if (s && [...s].every((ch) => (CIRC + " ,·").includes(ch))) return [...s].filter((ch) => CIRC.includes(ch)).map((ch) => String(CIRC.indexOf(ch) + 1)).join(",");
  return s;
}
function readAnswerLines(A, labels) {
  const found = {};
  const wantNum = new Set(labels.filter((l) => /^\d+$/.test(l)));
  for (const pg of A.pages) {
    const lines = pg.lines;
    const cells = lines.filter((ln) => wantNum.has(ln.text.trim()) && ln.x1 - ln.x < 30);
    const cols = new Map();
    for (const ln of cells) { const k = Math.round(ln.x / 10); if (!cols.has(k)) cols.set(k, []); cols.get(k).push(ln); }
    for (const col of cols.values()) {
      if (!(col.length >= 2 && new Set(col.map((l) => l.text.trim())).size / col.length >= 0.8)) continue;
      for (const ln of col) {
        const t = ln.text.trim();
        if (t in found) continue;
        const mid = (ln.y + ln.y1) / 2;
        const right = lines.filter((o) => Math.abs((o.y + o.y1) / 2 - mid) < 6 && o.x - ln.x1 > 2 && o.x - ln.x1 < 90);
        if (right.length) {
          const a = right.sort((p, q) => p.x - q.x)[0].text;
          if (a && !a.startsWith("[") && a.length <= 40) found[t] = normAnswer(a);
        }
      }
    }
    for (const ln of lines) {
      const t = ln.text.trim();
      const re = /(?:^|\s)(\d{1,2})\s*[).]\s*([①②③④⑤]|[^\s\d][^\s]{0,12}|\d[\d./,]*)/g;
      let m;
      while ((m = re.exec(t))) { const k = m[1]; if (wantNum.has(k) && !(k in found) && /[).]/.test(t)) found[k] = normAnswer(m[2]); }
    }
    for (const ln of lines) {
      const m = ESSAY_RE.exec(ln.text);
      if (!m) continue;
      const lab = `${m[1]} ${Number(m[2])}`;
      if (!labels.includes(lab) || lab in found) continue;
      const below = lines.filter((o) => o.y > ln.y && o.y - ln.y < 60 && o.text.startsWith("답")).sort((a, b) => a.y - b.y);
      if (below.length) found[lab] = normAnswer(below[0].text);
    }
  }
  return found;
}

// ── 이름 칸 찾기 · 지우기 (anon)
const LABELS = ["이름", "성명", "학생", "Name", "NAME", "name"];
const STOP = /^(날짜|일시|학년|반|번호?|점수|확인|월|일|실시일자|교과|과목|담당|선생님|학교|코드|소요시간|시간|\d+(문항|문제|쪽|면)?)[:：]?$/;
function labelOf(t) {
  const t2 = t.replace(/\s/g, "");
  for (const lab of LABELS) {
    if (t2 === lab || t2 === lab + ":" || t2 === lab + "：") return [true, ""];
    const m = new RegExp(`^${lab}\\s*[:：]\\s*(\\S.*)$`).exec(t);
    if (m) return [true, m[1].trim()];
  }
  return [false, ""];
}
function nameFields(pg) {
  const out = [];
  const { sp, edges, W } = pg;
  for (const s of sp) {
    const [ok, inline] = labelOf(s.t);
    if (!ok || s.x1 - s.x > 80) continue;
    const yc = (s.y + s.y1) / 2, h = s.y1 - s.y;
    const hit = edges.filter(([x, a, b]) => a - 1 <= yc && yc <= b + 1 && x > s.x1 + 0.5);
    const xs = [...new Set(hit.map(([x]) => Math.round(x * 10) / 10))].sort((a, b) => a - b);
    let bx0, bx1, align = "left";
    if (xs.length >= 2 && xs[0] - s.x1 < 40 && xs[1] - xs[0] <= 170) { bx0 = xs[0]; bx1 = xs[1]; align = "center"; }
    else if (xs.length && xs[0] - s.x1 >= 25) { bx0 = s.x1 + 3; bx1 = Math.min(xs[0], s.x1 + 150); }
    else { bx0 = s.x1 + 3; bx1 = Math.min(W - 14, s.x1 + 120); }
    let by0 = s.y - 2, by1 = s.y1 + 2;
    if (hit.length) {
      const [, a, b] = hit.sort((p, q) => (p[2] - p[1]) - (q[2] - q[1]))[0];
      if (b - a < h * 3.2) { by0 = a; by1 = b; }
    }
    const box = [bx0, by0, bx1, by1];
    const values = [];
    if (inline) {
      // 「이름: 홍길동」 한 덩이 — 값 자리는 덩이 안 글자 비율로
      const cw = (s.x1 - s.x) / Math.max(1, s.t.length);
      const at = s.t.lastIndexOf(inline);
      values.push([inline, [s.x + at * cw, s.y, s.x1, s.y1]]);
    }
    const right = sp.filter((t) => t !== s && t.x >= s.x1 - 1 && t.x <= Math.max(box[2], s.x1 + 60) && Math.min(t.y1, s.y1) - Math.max(t.y, s.y) > 0.45 * Math.min(h, t.y1 - t.y)).sort((a, b) => a.x - b.x);
    for (const t of right) {
      if (STOP.test(t.t.replace(/\s/g, "")) || labelOf(t.t)[0]) break;
      if (t.t.length > 14 || /^[_\-–—.·:：\s]+$/.test(t.t)) continue;
      values.push([t.t, [t.x, t.y, t.x1, t.y1]]);
    }
    out.push({ label: [s.x, s.y, s.x1, s.y1], values, box, size: s.size, align });
  }
  // 긴 덩이 속 「이름: 홍길동」 (제목과 한 줄에 붙은 경우)
  for (const s of sp) {
    if (labelOf(s.t)[0]) continue;
    const m = /(이름|성명)\s*[:：]\s*([가-힣]{2,4})(?![가-힣])/.exec(s.t);
    if (!m) continue;
    const cw = (s.x1 - s.x) / Math.max(1, s.t.length);
    const at = m.index + m[0].length - m[2].length;
    const r = [s.x + at * cw, s.y, s.x + (at + m[2].length) * cw, s.y1];
    const lx = s.x + m.index * cw;
    out.push({ label: [lx, s.y, r[0], s.y1], values: [[m[2], r]], box: [r[0] - 2, s.y - 2, Math.min(W - 14, r[0] + 110), s.y1 + 2], size: s.size, align: "left" });
  }
  return out;
}
const inter = (a, b) => a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
// D(readDoc 결과) → {removed:[{page,text}], boxes:[{page,rect,size,align}], targets: Map(page → [rect])}
function findNames(D, known) {
  const kn = new Set([...known].map((n) => String(n).replace(/\s+/g, " ").trim()).filter((n) => n.length >= 2));
  const removed = [], boxes = [], targets = new Map();
  const found = new Set();
  D.pages.forEach((pg, pno) => {
    const t = [];
    for (const f of nameFields(pg)) {
      for (const [txt, r] of f.values) { t.push(r); found.add(txt); removed.push({ page: pno + 1, text: txt }); }
      boxes.push({ page: pno, rect: f.box.map((v) => Math.round(v * 100) / 100), size: Math.round(Math.min(Math.max(f.size, 9), 12) * 10) / 10, align: f.align });
    }
    targets.set(pno, t);
  });
  const names = new Set([...kn, ...found]);
  D.pages.forEach((pg, pno) => {
    const t = targets.get(pno);
    for (const s of pg.sp) {
      const r = [s.x, s.y, s.x1, s.y1];
      if (names.has(s.t) && !t.some((x) => x.join() === r.join())) { t.push(r); removed.push({ page: pno + 1, text: s.t }); continue; }
      for (const n of names) {
        if (s.t.includes(n) && (s.y1 < pg.H * 0.16 || s.y > pg.H * 0.93) && !t.some((x) => inter(x, r))) {
          const cw = (s.x1 - s.x) / Math.max(1, s.t.length), at = s.t.indexOf(n);
          t.push([s.x + at * cw, s.y, s.x + (at + n.length) * cw, s.y1]);
          removed.push({ page: pno + 1, text: n });
        }
      }
    }
  });
  const uniq = [];
  for (const b of boxes) if (!uniq.some((u) => u.page === b.page && inter(u.rect, b.rect))) uniq.push(b);
  const seen = new Set(), rem = [];
  for (const r of removed) { const k = r.page + ":" + r.text; if (!seen.has(k)) { seen.add(k); rem.push(r); } }
  return { removed: rem, boxes: uniq, targets };
}
// 이름이 있는 쪽만 그림(300dpi)으로 바꾸며 이름 자리를 희게 — 글자 자료까지 남지 않게. 다른 쪽은 그대로.
async function redactPages(bytes, D, targets) {
  const pagesTo = [...targets.entries()].filter(([, t]) => t.length);
  if (!pagesTo.length) return bytes;
  const P = await pdflib();
  const out = await P.PDFDocument.load(bytes, { ignoreEncryption: true, updateMetadata: false });
  for (const [pno, rects] of pagesTo) {
    const pg = D.pages[pno];
    const dpi = 300, k = dpi / 72;
    const im = await renderClip(pg.page, null, dpi);
    for (const r of rects) fillRect(im, Math.floor((r[0] - 0.6) * k), Math.floor((r[1] - 0.6) * k), Math.ceil((r[2] + 0.6) * k), Math.ceil((r[3] + 0.6) * k));
    const png = await toPng(im);
    const old = out.getPage(pno);
    const { width, height } = old.getSize();
    const np = out.insertPage(pno, [pg.W, pg.H]);
    out.removePage(pno + 1);
    np.drawImage(await out.embedPng(png), { x: 0, y: 0, width: pg.W, height: pg.H });
    void width; void height;
  }
  return out.save();
}

// ── 코드 찍기
async function stampCode(bytes, code) {
  const P = await pdflib();
  const doc = await P.PDFDocument.load(bytes, { ignoreEncryption: true, updateMetadata: false });
  const label = "코드 " + fmtCode(code);
  const font = await embedText(doc, "sansR", label);
  for (const page of doc.getPages()) {
    const cb = page.getCropBox();
    const w = font.widthOfTextAtSize(label, 8);
    page.drawText(label, { x: cb.x + cb.width - w - 16, y: cb.y + cb.height - 13, size: 8, font, color: P.rgb(0.35, 0.35, 0.35) });
  }
  return doc.save();
}
const codePrinted = (D, code) => { const t = D.pages[0] ? D.pages[0].sp.map((s) => s.t).join("").replace(/\s/g, "") : ""; return t.includes(fmtCode(code)) || t.includes(code); };

// ── 분석 → 초안
// D · A: 이름을 지운 문서(쪽 그림 · 문항 그림 · 정답 그림을 여기서 오림)
// T · TA: 지우기 전 문서(글자 읽기 — 이름 있는 쪽은 그림으로 바뀌어 글자가 없으므로 문항 번호 · 제목 · 정답은 여기서)
async function analyze(D, A, manifest, draft, trust = false, T = D, TA = A) {
  if (!D.pages.length) throw new Error("빈 PDF예요");
  let m = manifest || (await readManifest(T.doc));
  const method = m ? "manifest" : "auto";
  let title = (m && m.title) || "";
  if (!title) { try { title = ((await T.doc.getMetadata()).info || {}).Title || ""; } catch { /* */ } }
  if (!title) {
    const big = T.pages[0].lines.filter((l) => l.y < T.pages[0].H * 0.3 && l.text.length >= 3).sort((a, b) => b.size - a.size);
    title = big.length ? big[0].text.slice(0, 60) : "";
  }
  const pages = [];
  for (let i = 0; i < D.pages.length; i++) {
    const rel = `pages/p${String(i + 1).padStart(2, "0")}.png`;
    draft.files.set(rel, await toPng(await renderClip(D.pages[i].page, null, 60)));
    pages.push(rel);
  }
  const items = [];
  if (m) {
    checkManifest(m);
    m.items.forEach((mi, i) => {
      const it = { label: String(mi.no || i + 1), answer: String(mi.answer ?? ""), choice: !!mi.choice, points: mi.points ?? null, topic: mi.topic || "", key: mi.key || "",
        sol: typeof mi.sol === "string" && /^sols\/[\w.-]+\.png$/.test(mi.sol) ? mi.sol : "",
        ans: typeof mi.ans === "string" && /^anss\/[\w.-]+\.png$/.test(mi.ans) ? mi.ans : "" };
      if (mi.page && mi.bbox) { it.page = Number(mi.page) - 1; it.rect = mi.bbox.map(Number); }
      items.push(it);
    });
    if (items.some((it) => !it.rect)) {
      const det = detectItems(T);
      const rg = new Map(det.map((d, i) => [d.label, regions(T, det)[i]]));
      for (const it of items) if (!it.rect && rg.has(it.label)) [it.page, it.rect] = rg.get(it.label);
    }
  } else {
    const det = detectItems(T);
    regions(T, det).forEach(([pno, rect], i) => items.push({ label: det[i].label, answer: "", choice: false, points: null, topic: "", key: "", page: pno, rect }));
  }
  const meth = m ? method : items.length ? "auto" : "pages";
  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    it.seq = i + 1;
    if (it.rect && D.pages[it.page]) {
      const im = await cropItem(D.pages[it.page].page, it.rect);
      const rel = `items/${String(i + 1).padStart(3, "0")}.png`;
      draft.files.set(rel, await toPng(im));
      it.png = rel;
      it.hash = it.key ? "key:" + it.key : imgHash(im);
      if (!m) it.choice = looksChoice(T.pages[it.page], it.rect);
      it.bbox = it.rect.map((v) => Math.round(v * 10) / 10);
      delete it.rect;
    } else {
      it.png = null;
      it.hash = it.key ? "key:" + it.key : null;
      delete it.rect;
    }
  }
  if (A && items.length) {
    // 정답지 글자로 정답 짐작하기 — 그림으로 답하는 문항(등록 정보의 정답 그림)과
    // 보관함 프린트(등록 정보의 정답이 기준 · 정답 칸이 없는 과제도 있음)는 짐작하지 않는다
    const guess = (it) => !it.answer && !it.ans && !(trust && m);
    try {
      const quick = await parseQuick(TA.doc);
      for (const it of items) {
        const q = /^\d+$/.test(it.label) ? quick[Number(it.label)] : null;
        if (!q) continue;
        const rq = await renderQuick(A.doc, q);           // 그림은 이름 지운 쪽에서
        const rel = `answers/${String(it.seq).padStart(3, "0")}.png`;
        draft.files.set(rel, rq.png);
        it.answer_png = rel;
        if (guess(it) && (q.choice || q.text)) { it.answer = q.choice || q.text; it.answer_guess = true; }
      }
    } catch { /* 매쓰플랫 빠른정답이 아님 */ }
    const got = readAnswerLines(TA, items.map((it) => it.label));
    for (const it of items) if (guess(it) && it.label in got) { it.answer = got[it.label]; it.answer_guess = true; }
  }
  return { method: meth, title, sub: (m && m.sub) || "", label: (m && m.label) || "", code: validCode(m && m.code), items, pages, manifest: m || null };
}

export async function registerAnalyze(b, ctx) {
  const sheetU = b.sheet && b.sheet.id ? await ctx.takeUpload(b.sheet.id) : null;
  if (!sheetU) throw new Error("시험지 PDF가 없어요");
  const ansU = b.answer && b.answer.id ? await ctx.takeUpload(b.answer.id) : null;
  let manifest = null;
  if (b.manifest && b.manifest.id) manifest = checkManifest(JSON.parse(new TextDecoder().decode((await ctx.takeUpload(b.manifest.id)).bytes).replace(/^﻿/, "")));
  const known = (await ctx.knownNames()).concat((b.extra_names || []).map(String).filter((x) => x.trim()));
  return makeDraft(ctx, { sheet: sheetU.bytes, sheetName: b.sheet.name || sheetU.name, answer: ansU && ansU.bytes, answerName: ansU && (b.answer.name || ansU.name), manifest, known });
}
async function makeDraft(ctx, { sheet, sheetName, answer, answerName, manifest, known, library = null, extras = [] }) {
  const id = "d" + ++dseq + Date.now().toString(36);
  const draft = { id, files: new Map() };
  let D = await readDoc(sheet);
  const fn = findNames(D, known);
  let A = answer ? await readDoc(answer) : null;
  const fa = A ? findNames(A, known) : { removed: [], targets: new Map() };
  const sheetClean = await redactPages(sheet, D, fn.targets);
  const ansClean = A ? await redactPages(answer, A, fa.targets) : null;
  const D0 = D, A0 = A;                       // 지우기 전 글자(문항 번호 · 정답 읽기용)
  if (sheetClean !== sheet) D = await readDoc(sheetClean);
  if (A && ansClean !== answer) A = await readDoc(ansClean);
  const r = await analyze(D, A, manifest, draft, !!library, D0, A0);
  const removed = fn.removed.concat(fa.removed);
  const names = new Set([...known, ...removed.map((x) => x.text)]);
  r.sheet_name = ctx.stripNames(ctx.cleanName(sheetName || "시험지.pdf"), names) || "시험지.pdf";
  r.answer_name = answer ? ctx.stripNames(ctx.cleanName(answerName || "정답지.pdf"), names) || "정답지.pdf" : null;
  if (!r.title) r.title = r.sheet_name.replace(/\.pdf$/i, "");
  r.title = ctx.stripNames(r.title, names) || "프린트";
  r.sub = ctx.stripNames(r.sub || "", names);
  r.anon = removed;
  r.name_boxes = fn.boxes;
  r.draft = id;
  r.base = `_draft/${id}`;
  if (library) { r.library = library.info; r.code = library.code; r.extras = extras; }
  // 첫 쪽 글자(지우기 전) — 이름 때문에 첫 쪽이 그림으로 바뀌어도 이미 찍힌 코드를 알아보게(코드 두 번 찍기 막기)
  const p1 = D0.pages[0] ? D0.pages[0].sp.map((s) => s.t).join("").replace(/\s/g, "") : "";
  draft.data = { ...r, sheet: sheetClean, answer: ansClean, libraryPid: library ? library.pid : null, extrasFiles: extras, p1 };
  DRAFTS.set(id, draft);
  return r;
}

export async function registerCommit(b, ctx) {
  const draft = DRAFTS.get(String(b.draft || ""));
  if (!draft) throw new Error("등록 초안이 없어요. 다시 분석해 주세요.");
  const dr = draft.data;
  const known = await ctx.knownNames();
  const title = ctx.stripNames(String(b.title || dr.title || "프린트").trim(), new Set([...known, ...(dr.anon || []).map((x) => x.text)])) || "프린트";
  const label = b.label || dr.label || "서답형";
  const bySeq = new Map(dr.items.map((it) => [it.seq, it]));
  const items = [];
  if (b.mode === "pages" || !dr.items.length) {
    const n = Math.max(1, Math.min(200, Number(b.count) || dr.items.length || 1));
    const edits = new Map((b.items || []).map((e) => [Number(e.seq), e]));
    for (let k = 1; k <= n; k++) {
      const e = edits.get(k) || {};
      items.push({ label: String(e.label || k), answer: String(e.answer || ""), choice: !!e.choice, png: null, hash: null, points: null, topic: "" });
    }
  } else {
    for (const e of b.items || []) {
      if (e.keep === false) continue;
      const src = bySeq.get(Number(e.seq));
      if (!src) continue;
      items.push({ label: String(e.label || src.label), answer: String(e.answer || "").trim(), choice: !!e.choice, png: src.png, hash: src.hash,
        points: src.points, topic: src.topic || "", answer_png: src.answer_png, bbox: src.bbox, page: src.page, sol: src.sol || "", ans: src.ans || "" });
    }
  }
  if (!items.length) throw new Error("문항이 하나도 없어요");
  const sids = await ctx.ensureStudents(b.targets || []);
  const libPid = dr.libraryPid;
  const code = libPid ? dr.code : await reserveCode(ctx, dr.code);
  const D = await readDoc(dr.sheet);
  const p1 = dr.p1 || "";
  const sheet = p1.includes(fmtCode(code)) || p1.includes(code) || codePrinted(D, code) ? dr.sheet : await stampCode(dr.sheet, code);
  const files = [{ rel: `${code}/sheet.pdf`, data: sheet, type: "application/pdf" }];
  if (dr.answer) files.push({ rel: `${code}/answer.pdf`, data: dr.answer, type: "application/pdf" });
  const rows = items.map((it, i) => {
    const n3 = String(i + 1).padStart(3, "0");
    const row = { seq: i + 1, src: dr.sheet_name, src_no: it.label, choice: it.choice, hash: it.hash, png: null, answer: it.answer, label: it.label,
      points: it.points ?? null, topic: it.topic || "", answer_png: null, page: it.page != null ? it.page + 1 : null, bbox: it.bbox || null, scale: it.png ? 72 / 150 : null };
    if (it.png) { files.push({ rel: `${code}/items/${n3}.png`, data: draft.files.get(it.png), type: "image/png" }); row.png = `items/${n3}.png`; }
    if (it.answer_png) { files.push({ rel: `${code}/answers/${n3}.png`, data: draft.files.get(it.answer_png), type: "image/png" }); row.answer_png = `answers/${n3}.png`; }
    if (libPid && it.sol) row.sol_png = it.sol;     // 보관함(저장소)이 미리 올려 둔 문항별 해설 그림 — <코드>/sols/NNN.png
    if (libPid && it.ans && !row.answer_png) row.answer_png = it.ans;     // 〃 정답 그림(분수 · 그림으로 답하는 문항) — <코드>/anss/NNN.png
    return row;
  });
  const sub = String(b.sub || dr.sub || "").trim();
  const rowP = { title, sub, kind: "registered", template: "등록", label, level: b.level || ctx.guessLevel(title, sub, ""), n_items: items.length,
    n_choice: items.filter((it) => it.choice).length, pages: D.pages.length, sources: [dr.sheet_name, dr.answer_name].filter(Boolean),
    files: { sheet: `${code}/sheet.pdf`, answer: dr.answer ? `${code}/answer.pdf` : null, src: [], extras: [] },
    name_boxes: dr.name_boxes || [], options: { method: dr.method, mode: b.mode || "items" }, shelf: "active" };
  if (libPid) {
    // 보관함 프린트를 꺼내 등록: 같은 줄을 고쳐 쓴다
    const { T, must, put, log } = ctx;
    const old = must(await T("tt_prints").select("files,options").eq("id", libPid).single());
    for (const f of files) await put(f.rel, f.data, f.type);
    rowP.files.extras = (old.files && old.files.extras) || [];
    rowP.options = { ...(old.options || {}), ...rowP.options };
    must(await T("tt_print_items").delete().eq("print_id", libPid));
    must(await T("tt_prints").update(nn("tt_prints", { ...rowP, updated_at: new Date().toISOString() })).eq("id", libPid));
    must(await T("tt_print_items").insert(nn("tt_print_items", rows.map((r) => ({ print_id: libPid, ...r })))));
    if (sids.length) must(await T("tt_targets").upsert(sids.map((s) => ({ print_id: libPid, student_id: s })), { onConflict: "print_id,student_id", ignoreDuplicates: true }));
    log("library_register", null, libPid, { code, title });
    log("register", null, libPid, { code, title, items: items.length, method: dr.method, mode: b.mode || "items", answers: items.filter((it) => it.answer).length });
    DRAFTS.delete(draft.id);
    return ctx.printBrief(libPid);
  }
  const brief = await storePrint(ctx, { code, row: rowP, items: rows, files, targets: sids, logKind: "register",
    logDetail: { title, items: items.length, method: dr.method, mode: b.mode || "items", answers: items.filter((it) => it.answer).length } });
  DRAFTS.delete(draft.id);
  return brief;
}

// 보관함 프린트(문항을 아직 안 나눈 것) → 등록 확인 화면
export async function libraryDraft(pr, ctx) {
  const f = pr.files || {};
  if (!f.sheet) throw new Error("보관함 프린트에 문제지 파일이 없어요");
  const sheet = await ctx.bytes(f.sheet);
  const answer = f.answer ? await ctx.bytes(f.answer) : null;
  const lib = (pr.options && pr.options.library) || {};
  const r = await makeDraft(ctx, { sheet, sheetName: f.sheet_name || pr.title + ".pdf", answer, answerName: f.answer_name || null,
    // 프린트를 만들어 준 학생 이름(for)은 지금 학생 목록에 없어도 지운다(보관 프린트는 이름 없는 판으로)
    manifest: lib.manifest || null, known: (await ctx.knownNames()).concat((lib.for || []).map(String).filter((x) => x.trim())),
    library: { pid: pr.id, code: pr.code, info: { files: (lib.roles || []).map((role) => ({ role })), made: lib.made || "", level: pr.level || lib.level || "", for: lib.for || [] } },
    extras: f.extras || [] });
  if (lib.title || pr.title) r.title = pr.title || lib.title;
  if (pr.sub) r.sub = pr.sub;
  return r;
}

// 보관함 프린트를 코드만으로 바로 등록 — 등록 정보(ashrain-print.json · 저장소 print.json)로 문항 자리를 모두 찾았으면
// 확인 화면 없이 문항 나누기 · 이름 지우기 · 정답 · 해설 그림까지 넣는다. 못 찾은 문항이 있으면 확인 화면(초안)으로.
const CIRC_NUM = { "①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5" };
export async function libraryAuto(pr, ctx) {
  const d = await libraryDraft(pr, ctx);
  const ready = d.method === "manifest" && d.items.length > 0 && d.items.every((it) => it.png);
  if (!ready) return { done: false, draft: d };
  const lib = (pr.options && pr.options.library) || {};
  const active = new Set((await ctx.all(() => ctx.T("tt_students").select("name,active"))).filter((s) => s.active).map((s) => s.name));
  const targets = (lib.for || []).filter((n) => active.has(n));     // 있는 학생만 (새로 만들지 않음)
  const print = await registerCommit({
    draft: d.draft, title: d.title, sub: d.sub, label: d.label || "서답형", level: pr.level || lib.level || "", targets, mode: "items",
    items: d.items.map((it) => ({ seq: it.seq, keep: true, label: it.label, choice: it.choice,
      answer: it.choice ? CIRC_NUM[String(it.answer).trim()] || String(it.answer || "").trim() : String(it.answer || "").trim() })),
  }, ctx);
  return { done: true, auto: true, print, n_items: d.items.length, n_answers: d.items.filter((it) => String(it.answer || "").trim()).length,
    n_sols: d.items.filter((it) => it.sol).length, n_ans_imgs: d.items.filter((it) => it.ans).length, targets };
}

// 정답 PDF 붙이기 (프린트 화면) — 이름 지우기 · 빠른정답 채우기 · (매쓰플랫이면) 강사도구 양식 정답해설
export async function attachAnswer(pr, up, ctx) {
  const { T, must, put, log, all } = ctx;
  const known = await ctx.knownNames();
  let A = await readDoc(up.bytes);
  const fa = findNames(A, known);
  const clean = await redactPages(up.bytes, A, fa.targets);
  const A0 = A;                               // 지우기 전 글자(빠른정답 읽기용) — 그림은 지운 쪽에서
  if (clean !== up.bytes) A = await readDoc(clean);
  let rel = `${pr.code}/answer_att.pdf`;
  await put(rel, clean, "application/pdf");
  const items = await all(() => T("tt_print_items").select("seq,src,src_no,label,answer,answer_png,choice").eq("print_id", pr.id).order("seq"));
  let n = 0;
  let quick = {};
  try { quick = await parseQuick(A0.doc); } catch { quick = {}; }
  const single = new Set(items.map((it) => it.src)).size <= 1;
  if (Object.keys(quick).length && single) {
    for (const it of items) {
      const key = pr.kind !== "registered" ? it.src_no : it.label;
      const q = /^\d+$/.test(String(key || "")) ? quick[Number(key)] : null;
      if (!q) continue;
      const rq = await renderQuick(A.doc, q);
      const arel = `answers/${String(it.seq).padStart(3, "0")}.png`;
      await put(`${pr.code}/${arel}`, rq.png, "image/png");
      const ans = it.answer || q.choice || q.text || "";
      must(await T("tt_print_items").update({ answer: ans, answer_png: arel }).eq("print_id", pr.id).eq("seq", it.seq));
      it.answer = ans; it.answer_png = arel; it._wh = rq.wh; it._png = rq.png;
      n++;
    }
  }
  let designed = false;
  if (pr.kind !== "registered" && single && items.length) {
    try {
      const sp = await solutionPages(A.doc, 0);
      const [sols, used] = sp.length ? await parseSolutions(A.doc, sp) : [{}, []];
      if (Object.keys(quick).length || Object.keys(sols).length) {
        const entries = [];
        for (const it of items) {
          const sol = sols[Number(it.src_no)];
          let solE = null;
          if (sol) {
            const png = await toPng(sol.img);
            const srel = `sols/${String(it.seq).padStart(3, "0")}.png`;
            await put(`${pr.code}/${srel}`, png, "image/png");
            must(await T("tt_print_items").update({ sol_png: srel }).eq("print_id", pr.id).eq("seq", it.seq));
            solE = { png, w: sol.w, h: sol.h };
          }
          entries.push({ seq: it.seq, choice: !!it.choice, answer: it.answer || "", answer_png: it._png || null, answer_wh: it._wh || null, sol: solE });
        }
        const cfg = settings({ template: TEMPLATE_KEYS.includes(pr.template) ? pr.template : "문정중" });
        cfg.코드 = pr.code;
        const left = [];
        for (const i of sp.filter((x) => !used.includes(x))) left.push(await pageImageNoNames(A.doc, i, known));
        const out = await buildAnswerPdf(entries, cfg, pr.title, left);
        rel = `${pr.code}/answer.pdf`;
        await put(rel, out.pdf, "application/pdf");
        designed = true;
      }
    } catch (e) { console.warn("정답해설 양식 바꾸기 실패", e); }
  }
  const files = { ...(pr.files || {}), answer: rel };
  must(await T("tt_prints").update({ files, updated_at: new Date().toISOString() }).eq("id", pr.id));
  log("answer_attach", null, pr.id, { quick: n, designed });
  return n;
}
// 옮겨 오기(PDF 묶음)에서 쓰는 도구
export { readDoc, readManifest, findNames, redactPages, stampCode, codePrinted, validCode };
