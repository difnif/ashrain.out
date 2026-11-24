// 강사도구 엔진 — 바탕: pdf.js(읽기·그리기) · pdf-lib(쓰기) · 글꼴 · 그림 처리 (브라우저 안에서만 돈다)
// PC판(PyMuPDF·PIL) 계산을 그대로 옮긴 것: 회색 변환(L24) · 쌍선형 줄이기(PIL Resample 고정소수점) · 문항 지문(img_hash)

export const MM = 72 / 25.4;
export const A4W = 595.28, A4H = 841.89;

// ── pdf.js (시록고의 다른 화면과 같은 판 — cdnjs 3.11.174)
const PDFJS = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174";
let libP = null;
export function pdfjs() {
  if (typeof window !== "undefined" && window.pdfjsLib) {
    const L = window.pdfjsLib;
    if (L.GlobalWorkerOptions && !L.GlobalWorkerOptions.workerSrc) L.GlobalWorkerOptions.workerSrc = `${PDFJS}/pdf.worker.min.js`;
    return Promise.resolve(L);
  }
  if (!libP) {
    libP = new Promise((res, rej) => {
      const s = document.createElement("script");
      s.src = `${PDFJS}/pdf.min.js`;
      s.onload = () => { window.pdfjsLib.GlobalWorkerOptions.workerSrc = `${PDFJS}/pdf.worker.min.js`; res(window.pdfjsLib); };
      s.onerror = () => { libP = null; rej(new Error("PDF 도구(pdf.js)를 불러오지 못했어요. 인터넷 연결을 확인해 주세요.")); };
      document.head.appendChild(s);
    });
  }
  return libP;
}
export async function openPdf(bytes) {
  const L = await pdfjs();
  const data = bytes instanceof Uint8Array ? bytes.slice() : new Uint8Array(bytes);
  return L.getDocument({ data, isOffscreenCanvasSupported: false, isEvalSupported: false, useSystemFonts: false }).promise;
}

// ── pdf-lib
let plP = null;
export function pdflib() {
  if (!plP) plP = Promise.all([import("pdf-lib"), import("@pdf-lib/fontkit")]).then(([P, fk]) => ({ ...P, fontkit: fk.default || fk }));
  return plP;
}

// ── 글꼴 (public/tt-fonts) — 양식별
const FONT_FILES = {
  serifR: "/tt-fonts/NotoSerifKR-Regular.ttf", serifB: "/tt-fonts/NotoSerifKR-Bold.ttf",
  sansR: "/tt-fonts/Pretendard-Medium.ttf", sansB: "/tt-fonts/Pretendard-ExtraBold.ttf",
};
const fontBytes = new Map();
export async function fontFile(key) {
  if (!fontBytes.has(key)) {
    fontBytes.set(key, (async () => {
      const r = await fetch(FONT_FILES[key]);
      if (!r.ok) throw new Error("글꼴을 불러오지 못했어요 (" + key + ")");
      return new Uint8Array(await r.arrayBuffer());
    })());
  }
  try { return await fontBytes.get(key); } catch (e) { fontBytes.delete(key); throw e; }
}
// 양식: 「초등 크리스마스」는 초등 양식에 장식만 더한 판 — 글꼴·배치의 바탕은 초등
export const baseOf = (template) => (String(template || "").startsWith("초등") ? "초등" : template);
export const isXmas = (template) => template === "초등 크리스마스";
export const fontsFor = (template) => (baseOf(template) === "초등" ? ["sansR", "sansB"] : ["serifR", "serifB"]);

// ── 글꼴 줄이기 (HarfBuzz hb-subset) — pdf-lib 자체 줄이기는 한글 글자가 빠지는 문제가 있어 쓰지 않는다.
//    쓴 글자만 남기고 GSUB·GPOS 표를 빼서(대체 글자·커닝 없음) 글자 폭·글자 뽑기가 PyMuPDF 때처럼 단순해진다.
let hbP = null;
function harfbuzz() {
  if (!hbP) hbP = import("harfbuzzjs/hb-subset.wasm?url").then(async ({ default: url }) => {
    const r = await fetch(url);
    const { instance } = await WebAssembly.instantiate(await r.arrayBuffer(), {});
    return instance.exports;
  }).catch((e) => { hbP = null; throw e; });
  return hbP;
}
const tag4 = (t) => ((t.charCodeAt(0) << 24) | (t.charCodeAt(1) << 16) | (t.charCodeAt(2) << 8) | t.charCodeAt(3)) >>> 0;
const subsetCache = new Map();
export async function subsetFont(key, text) {
  const chars = [...new Set(String(text))].sort().join("");
  const ck = key + "\u0000" + chars;
  if (subsetCache.has(ck)) return subsetCache.get(ck);
  const [X, font] = await Promise.all([harfbuzz(), fontFile(key)]);
  const fb = X.malloc(font.byteLength);
  new Uint8Array(X.memory.buffer).set(font, fb);
  const blob = X.hb_blob_create(fb, font.byteLength, 2, 0, 0);
  const face = X.hb_face_create(blob, 0);
  X.hb_blob_destroy(blob);
  const input = X.hb_subset_input_create_or_fail();
  const us = X.hb_subset_input_unicode_set(input);
  for (const ch of chars) X.hb_set_add(us, ch.codePointAt(0));
  const drop = X.hb_subset_input_set(input, 3);            // HB_SUBSET_SETS_DROP_TABLE_TAG
  for (const t of ["GSUB", "GPOS", "GDEF", "morx", "kern"]) X.hb_set_add(drop, tag4(t));
  const sub = X.hb_subset_or_fail(face, input);
  X.hb_subset_input_destroy(input);
  if (!sub) { X.hb_face_destroy(face); X.free(fb); throw new Error("글꼴을 줄이지 못했어요"); }
  const rb = X.hb_face_reference_blob(sub);
  const off = X.hb_blob_get_data(rb, 0), len = X.hb_blob_get_length(rb);
  const out = new Uint8Array(X.memory.buffer).slice(off, off + len);
  X.hb_blob_destroy(rb); X.hb_face_destroy(sub); X.hb_face_destroy(face); X.free(fb);
  if (!len) throw new Error("글꼴을 줄이지 못했어요");
  if (subsetCache.size > 40) subsetCache.clear();
  subsetCache.set(ck, out);
  return out;
}
// 글자 폭 재기용 (fontkit — 글자표만 보고 대체 글자 없이: 줄인 글꼴과 같은 폭)
const measCache = new Map();
async function measurer(key) {
  if (!measCache.has(key)) measCache.set(key, (async () => {
    const P = await pdflib();
    const f = P.fontkit.create(await fontFile(key));
    const k = 1 / f.unitsPerEm;
    return { widthOfTextAtSize: (s, size) => { let w = 0; for (const g of f.glyphsForString(String(s))) w += g.advanceWidth; return w * k * size; } };
  })());
  return measCache.get(key);
}
// 늘 넣어 두는 글자 (1차와 2차의 줄임표·숫자 차이 대비)
const BASE_CHARS = (() => { let t = ""; for (let c = 32; c < 127; c++) t += String.fromCharCode(c); return t + "…·−–—①②③④⑤○×÷±%"; })();
const pngSize = (b) => (b && b.length > 24 && b[0] === 0x89 ? { width: (b[16] << 24 | b[17] << 16 | b[18] << 8 | b[19]) >>> 0, height: (b[20] << 24 | b[21] << 16 | b[22] << 8 | b[23]) >>> 0 } : { width: 100, height: 100 });
// 두 번 그리기: 1차는 쓰는 글자만 모으고(그리지 않음), 2차는 그 글자만 담은 글꼴로 실제로 그린다.
// draw(ctx) 는 같은 입력이면 같은 것을 그려야 한다. ctx = {P, doc, R, B, dry}
export async function twoPass(template, draw) {
  const P = await pdflib();
  const [rk, bk] = fontsFor(template);
  const used = new Set(BASE_CHARS);
  const note = (s) => { for (const ch of String(s ?? "")) used.add(ch); };
  const [mr, mb] = await Promise.all([measurer(rk), measurer(bk)]);
  const fakeFont = (m) => ({ widthOfTextAtSize: (s, size) => { note(s); return m.widthOfTextAtSize(s, size); } });
  let nPages = 0;
  const fakePage = (size) => ({ drawText: (s) => note(s), drawLine() {}, drawRectangle() {}, drawSvgPath() {}, drawCircle() {}, drawImage() {}, drawPage() {},
    getSize: () => ({ width: (size || [A4W, A4H])[0], height: (size || [A4W, A4H])[1] }) });
  const fakeDoc = { addPage: (size) => { nPages++; return fakePage(size); }, embedPng: async (b) => pngSize(b), embedJpg: async () => ({ width: 100, height: 100 }),
    embedPdf: async (b, idx = [0]) => idx.map(() => ({ width: 1, height: 1 })),
    getPageCount: () => nPages, save: async () => new Uint8Array(0), registerFontkit() {} };
  await draw({ P, doc: fakeDoc, R: fakeFont(mr), B: fakeFont(mb), dry: true });
  const doc = await P.PDFDocument.create();
  doc.registerFontkit(P.fontkit);
  const text = [...used].join("");
  const [sr, sb] = await Promise.all([subsetFont(rk, text), subsetFont(bk, text)]);
  const R = await doc.embedFont(sr, { subset: false });
  const Bf = rk === bk ? R : await doc.embedFont(sb, { subset: false });
  return draw({ P, doc, R, B: Bf, dry: false });
}
// 글자를 미리 아는 경우: 그 글자만 담은 글꼴 하나
export async function embedText(doc, key, text) {
  const P = await pdflib();
  doc.registerFontkit(P.fontkit);
  return doc.embedFont(await subsetFont(key, BASE_CHARS + String(text)), { subset: false });
}

// ── 캔버스·그림
export function canvas(w, h) {
  const c = document.createElement("canvas");
  c.width = Math.max(1, Math.round(w));
  c.height = Math.max(1, Math.round(h));
  return c;
}
export function toBlob(c, type = "image/png", q) {
  return new Promise((res, rej) => c.toBlob((b) => (b ? res(b) : rej(new Error("그림을 만들지 못했어요"))), type, q));
}
export async function toPng(img) {
  const c = img instanceof HTMLCanvasElement ? img : imgToCanvas(img);
  return new Uint8Array(await (await toBlob(c, "image/png")).arrayBuffer());
}
// Img = {w, h, d: Uint8ClampedArray RGBA}
export function newImg(w, h, fill = 255) {
  const d = new Uint8ClampedArray(w * h * 4);
  d.fill(fill);
  return { w, h, d };
}
export function canvasToImg(c) {
  const ctx = c.getContext("2d", { willReadFrequently: true });
  return { w: c.width, h: c.height, d: ctx.getImageData(0, 0, c.width, c.height).data };
}
export function imgToCanvas(im) {
  const c = canvas(im.w, im.h);
  c.getContext("2d").putImageData(new ImageData(im.d, im.w, im.h), 0, 0);
  return c;
}
export async function pngToImg(bytes) {
  const bmp = await createImageBitmap(new Blob([bytes], { type: "image/png" }));
  const c = canvas(bmp.width, bmp.height);
  const ctx = c.getContext("2d", { willReadFrequently: true });
  ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height);
  ctx.drawImage(bmp, 0, 0);
  return canvasToImg(c);
}
export function crop(im, x0, y0, x1, y1) {
  x0 = Math.max(0, Math.round(x0)); y0 = Math.max(0, Math.round(y0));
  x1 = Math.min(im.w, Math.round(x1)); y1 = Math.min(im.h, Math.round(y1));
  const w = Math.max(1, x1 - x0), h = Math.max(1, y1 - y0);
  const out = newImg(w, h);
  for (let y = 0; y < h && y0 + y < im.h; y++) {
    const s = ((y0 + y) * im.w + x0) * 4;
    out.d.set(im.d.subarray(s, s + Math.min(w, im.w - x0) * 4), y * w * 4);
  }
  return out;
}
export function paste(dst, src, x, y) {
  for (let yy = 0; yy < src.h; yy++) {
    const ty = y + yy;
    if (ty < 0 || ty >= dst.h) continue;
    const sx0 = Math.max(0, -x), sx1 = Math.min(src.w, dst.w - x);
    if (sx1 <= sx0) continue;
    const s = (yy * src.w + sx0) * 4;
    dst.d.set(src.d.subarray(s, s + (sx1 - sx0) * 4), (ty * dst.w + x + sx0) * 4);
  }
}
export function fillRect(im, x0, y0, x1, y1, v = 255) {
  x0 = Math.max(0, x0 | 0); y0 = Math.max(0, y0 | 0); x1 = Math.min(im.w, x1 | 0); y1 = Math.min(im.h, y1 | 0);
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) { const i = (y * im.w + x) * 4; im.d[i] = im.d[i + 1] = im.d[i + 2] = v; im.d[i + 3] = 255; }
}
// PIL convert("L") — L = (R*19595 + G*38470 + B*7471 + 0x8000) >> 16
export function gray(im) {
  const n = im.w * im.h, g = new Uint8Array(n);
  for (let i = 0, j = 0; i < n; i++, j += 4) g[i] = (im.d[j] * 19595 + im.d[j + 1] * 38470 + im.d[j + 2] * 7471 + 0x8000) >>> 16;
  return { w: im.w, h: im.h, g };
}
// 흰 바탕 위에 합성된 RGBA (알파를 흰색과 섞음 — PIL paste(mask) 와 같은 반올림)
export function flattenWhite(im) {
  const d = im.d;
  for (let j = 0; j < d.length; j += 4) {
    const a = d[j + 3];
    if (a === 255) continue;
    for (let k = 0; k < 3; k++) {
      // PIL: out = (src*a + dst*(255-a)) / 255, 반올림 (ImagingPaste 의 BLEND: tmp = in*a + out*(255-a) + 128; (tmp + (tmp>>8)) >> 8)
      const tmp = d[j + k] * a + 255 * (255 - a) + 128;
      d[j + k] = (tmp + (tmp >> 8)) >> 8;
    }
    d[j + 3] = 255;
  }
  return im;
}

// ── PIL Image.resize(BILINEAR) — 8비트 한 채널(회색) 고정소수점 그대로
const PREC = 22;
function coeffs(inSize, outSize) {
  const scale = inSize / outSize;
  const fscale = Math.max(1, scale);
  const support = 1.0 * fscale;
  const ksize = Math.ceil(support) * 2 + 1;
  const bounds = new Int32Array(outSize * 2);
  const kk = new Float64Array(outSize * ksize);
  for (let xx = 0; xx < outSize; xx++) {
    const center = (xx + 0.5) * scale;
    let ww = 0;
    const ss = 1 / fscale;
    let xmin = Math.trunc(center - support + 0.5);
    if (xmin < 0) xmin = 0;
    let xmax = Math.trunc(center + support + 0.5);
    if (xmax > inSize) xmax = inSize;
    xmax -= xmin;
    for (let x = 0; x < xmax; x++) {
      let t = Math.abs((x + xmin - center + 0.5) * ss);
      const w = t < 1 ? 1 - t : 0;
      kk[xx * ksize + x] = w;
      ww += w;
    }
    for (let x = 0; x < xmax; x++) if (ww !== 0) kk[xx * ksize + x] /= ww;
    bounds[xx * 2] = xmin;
    bounds[xx * 2 + 1] = xmax;
  }
  const ik = new Float64Array(kk.length);
  for (let i = 0; i < kk.length; i++) ik[i] = kk[i] < 0 ? Math.trunc(-0.5 + kk[i] * (1 << PREC)) : Math.trunc(0.5 + kk[i] * (1 << PREC));
  return { ksize, bounds, k: ik };
}
const clip8 = (v) => (v >= 2 ** (PREC + 8) ? 255 : v <= 0 ? 0 : Math.floor(v / 2 ** PREC));
export function resizeGray(src, W, H) {
  const { w, h, g } = src;
  let cur = { w, h, g };
  if (W !== w) {
    const C = coeffs(w, W);
    const out = new Uint8Array(W * h);
    for (let y = 0; y < h; y++) {
      const row = y * w;
      for (let xx = 0; xx < W; xx++) {
        const xmin = C.bounds[xx * 2], xmax = C.bounds[xx * 2 + 1], o = xx * C.ksize;
        let ss = 2 ** (PREC - 1);
        for (let x = 0; x < xmax; x++) ss += g[row + x + xmin] * C.k[o + x];
        out[y * W + xx] = clip8(ss);
      }
    }
    cur = { w: W, h, g: out };
  }
  if (H !== h) {
    const C = coeffs(h, H);
    const out = new Uint8Array(cur.w * H);
    for (let yy = 0; yy < H; yy++) {
      const ymin = C.bounds[yy * 2], ymax = C.bounds[yy * 2 + 1], o = yy * C.ksize;
      for (let xx = 0; xx < cur.w; xx++) {
        let ss = 2 ** (PREC - 1);
        for (let y = 0; y < ymax; y++) ss += cur.g[(y + ymin) * cur.w + xx] * C.k[o + y];
        out[yy * cur.w + xx] = clip8(ss);
      }
    }
    cur = { w: cur.w, h: H, g: out };
  }
  return cur;
}
// 회색 그림의 「잉크 상자」 (PIL getbbox — 0이 아닌 칸) : pred(v) 가 참인 칸
export function bboxWhere(gr, pred) {
  let x0 = gr.w, y0 = gr.h, x1 = -1, y1 = -1;
  for (let y = 0; y < gr.h; y++) {
    const r = y * gr.w;
    for (let x = 0; x < gr.w; x++) if (pred(gr.g[r + x])) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; y1 = y; }
  }
  return x1 < 0 ? null : [x0, y0, x1 + 1, y1 + 1];
}
export function cropGray(gr, x0, y0, x1, y1) {
  const w = x1 - x0, h = y1 - y0, g = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) g.set(gr.g.subarray((y0 + y) * gr.w + x0, (y0 + y) * gr.w + x0 + w), y * w);
  return { w, h, g };
}

// ── md5 (문항 지문용)
export function md5hex(bytes) {
  const K = new Uint32Array(64), S = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21];
  for (let i = 0; i < 64; i++) K[i] = Math.floor(Math.abs(Math.sin(i + 1)) * 2 ** 32) >>> 0;
  const n = bytes.length, total = ((n + 8) >>> 6) * 64 + 64;
  const m = new Uint8Array(total);
  m.set(bytes); m[n] = 0x80;
  const bits = n * 8;
  const dv = new DataView(m.buffer);
  dv.setUint32(total - 8, bits >>> 0, true); dv.setUint32(total - 4, Math.floor(bits / 2 ** 32), true);
  let a0 = 0x67452301, b0 = 0xefcdab89, c0 = 0x98badcfe, d0 = 0x10325476;
  const M = new Uint32Array(16);
  for (let off = 0; off < total; off += 64) {
    for (let i = 0; i < 16; i++) M[i] = dv.getUint32(off + i * 4, true);
    let A = a0, B = b0, C = c0, D = d0;
    for (let i = 0; i < 64; i++) {
      let F, g;
      if (i < 16) { F = (B & C) | (~B & D); g = i; }
      else if (i < 32) { F = (D & B) | (~D & C); g = (5 * i + 1) % 16; }
      else if (i < 48) { F = B ^ C ^ D; g = (3 * i + 5) % 16; }
      else { F = C ^ (B | ~D); g = (7 * i) % 16; }
      F = (F + A + K[i] + M[g]) >>> 0;
      A = D; D = C; C = B;
      const s = S[(i >> 4) * 4 + (i % 4)];
      B = (B + ((F << s) | (F >>> (32 - s)))) >>> 0;
    }
    a0 = (a0 + A) >>> 0; b0 = (b0 + B) >>> 0; c0 = (c0 + C) >>> 0; d0 = (d0 + D) >>> 0;
  }
  return [a0, b0, c0, d0].map((x) => [0, 8, 16, 24].map((s) => ((x >>> s) & 255).toString(16).padStart(2, "0")).join("")).join("");
}
// mf2exam.img_hash 와 같은 값
export function imgHash(im) {
  let g = gray(im);
  const inv = bboxWhere(g, (v) => 255 - v > 40);
  if (inv) g = cropGray(g, ...inv);
  const W = 160;
  const H = Math.max(1, Math.min(480, Math.round((g.h * W) / Math.max(g.w, 1))));
  const r = resizeGray(g, W, H);
  const q = new Uint8Array(r.g.length);
  for (let i = 0; i < q.length; i++) q[i] = r.g[i] >> 6;
  return md5hex(q).slice(0, 24) + "-" + H;
}

// ── 쪽 읽기: 글자 덩이(spans) · 그림 자리 · 세로 선
// 글꼴 이름 (굵은 글꼴 가리기) — 글꼴이 화면에 붙은 뒤에야 commonObjs 에 들어오므로 기다린다
function fontName(page, id) {
  return new Promise((res) => {
    let done = false;
    const fin = (v) => { if (!done) { done = true; res(v); } };
    try { page.commonObjs.get(id, (f) => fin((f && (f.name || f.loadedName)) || "")); } catch { fin(""); }
    setTimeout(() => fin(""), 4000);
  });
}
// PyMuPDF spans 비슷한 것: [{t, x, y, x1, y1, size, font, bold, base}] (왼쪽 위 원점, pt)
export async function pageSpans(page, opList) {
  const L = await pdfjs();
  if (!opList) await page.getOperatorList();
  const vp = page.getViewport({ scale: 1 });
  const tc = await page.getTextContent({ disableCombineTextItems: false });
  const out = [], names = new Map();
  for (const it0 of tc.items) {
    // 글꼴에 유니코드 표가 없는 빈칸 글자(\u0001 등)는 빈칸으로
    const it = it0.str && /[\u0000-\u001f\u00a0]/.test(it0.str) ? { ...it0, str: it0.str.replace(/[\u0000-\u001f\u00a0]/g, " ") } : it0;
    if (!it.str || !it.str.trim()) continue;
    const st = tc.styles[it.fontName] || {};
    const tx = L.Util.transform(vp.transform, it.transform);
    const size = Math.hypot(tx[2], tx[3]) || Math.abs(it.height) || 10;
    const asc = st.ascent ? st.ascent : st.descent ? 1 + st.descent : 0.88;
    const desc = st.descent ? st.descent : asc - 1;
    if (!names.has(it.fontName)) names.set(it.fontName, await fontName(page, it.fontName));
    const fn = names.get(it.fontName);
    const lead = it.str.length - it.str.trimStart().length, trail = it.str.length - it.str.trimEnd().length;
    const cw = it.str.length ? it.width / it.str.length : 0;
    const x = tx[4] + lead * cw, x1 = tx[4] + it.width - trail * cw;
    out.push({ t: it.str.trim().replace(/\s+/g, " "), raw: it.str, x, x1, y: tx[5] - asc * size, y1: tx[5] - desc * size, base: tx[5], size: Math.round(size * 100) / 100,
      font: fn, bold: /bold|black|heavy|extrabold|semibold/i.test(fn), w: it.width });
  }
  // PyMuPDF 의 span 처럼: 같은 줄·같은 글꼴·같은 크기로 바로 이어진 덩이는 하나로
  const merged = [];
  for (const s of out) {
    const a = merged[merged.length - 1];
    const gap = a ? s.x - a.x1 : 0;
    if (a && !/^[|│]|^정답률/.test(s.t) && a.font === s.font && Math.abs(a.size - s.size) < 0.1 && Math.abs(a.base - s.base) < 0.5 && gap > -0.5 && gap < 1.2 * s.size) {
      a.t = a.t + (gap > 0.15 * s.size ? " " : "") + s.t;
      a.raw = a.raw + (gap > 0.15 * s.size ? " " : "") + s.raw;
      a.x1 = s.x1; a.y = Math.min(a.y, s.y); a.y1 = Math.max(a.y1, s.y1); a.w = a.x1 - a.x;
    } else merged.push({ ...s });
  }
  return merged;
}
// 낱말 (PyMuPDF get_text("words") 비슷하게 — 덩이 안 글자 폭을 고르게 나눔)
export function spanWords(spans) {
  const out = [];
  for (const s of spans) {
    const raw = s.raw || s.t;
    const cw = raw.length ? (s.w || s.x1 - s.x) / raw.length : 0;
    const x0 = s.x - (raw.length - raw.trimStart().length) * cw;
    let m;
    const re = /\S+/g;
    while ((m = re.exec(raw))) out.push({ t: m[0], x: x0 + m.index * cw, x1: x0 + (m.index + m[0].length) * cw, y: s.y, y1: s.y1 });
  }
  return out;
}
// 같은 줄 덩이 묶기 (printreg.page_lines)
export function pageLines(spans) {
  const sorted = [...spans].sort((a, b) => a.base - b.base || a.x - b.x);
  const lines = [];
  for (const s of sorted) {
    const ln = lines.find((l) => Math.abs(l.base - s.base) < Math.max(1.2, 0.3 * Math.min(l.size, s.size)) && s.x >= l.x1 - 2 && s.x - l.x1 < 2.2 * Math.max(l.size, s.size));
    if (ln) {
      ln.sp.push(s);
      ln.x1 = Math.max(ln.x1, s.x1); ln.y1 = Math.max(ln.y1, s.y1);
    } else lines.push({ base: s.base, x: s.x, x1: s.x1, y: s.y, y1: s.y1, size: s.size, sp: [s] });
  }
  return lines.map((l) => {
    l.sp.sort((a, b) => a.x - b.x);
    const s0 = l.sp[0];
    let text = "";
    l.sp.forEach((s, i) => { text += (i && s.x - l.sp[i - 1].x1 > 0.25 * s.size ? " " : "") + s.t; });
    return { text: text.trim(), x: s0.x, y: s0.y, y1: Math.max(...l.sp.map((s) => s.y1)), x1: Math.max(...l.sp.map((s) => s.x1)),
      size: Math.round(s0.size * 2) / 2, font: s0.font, bold: s0.bold, first: s0.t, spans: l.sp };
  }).sort((a, b) => a.y - b.y || a.x - b.x);
}
export const pageText = (spans) => pageLines(spans).map((l) => l.text).join("\n");

const mul = (m, n) => [m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1], m[0] * n[2] + m[2] * n[3], m[1] * n[2] + m[3] * n[3], m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5]];
const apply = (m, x, y) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];
// 쪽 안 그림 자리: [{id, kind:'x'|'inline', obj, w, h (원래 화소), bbox:[x0,y0,x1,y1] (왼쪽 위 원점 pt)}] + 세로선
export async function pageGraphics(page) {
  const L = await pdfjs();
  const O = L.OPS;
  const ops = await page.getOperatorList();
  const vp = page.getViewport({ scale: 1 });
  let ctm = vp.transform.slice();
  const stack = [];
  const imgs = [], edges = [];
  const toBox = (m) => {
    const ps = [apply(m, 0, 0), apply(m, 1, 0), apply(m, 0, 1), apply(m, 1, 1)];
    const xs = ps.map((p) => p[0]), ys = ps.map((p) => p[1]);
    return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
  };
  for (let i = 0; i < ops.fnArray.length; i++) {
    const fn = ops.fnArray[i], a = ops.argsArray[i];
    if (fn === O.save) stack.push(ctm.slice());
    else if (fn === O.restore) ctm = stack.pop() || ctm;
    else if (fn === O.transform) ctm = mul(ctm, a);
    else if (fn === O.paintFormXObjectBegin) { stack.push(ctm.slice()); if (a && a[0]) ctm = mul(ctm, a[0]); }
    else if (fn === O.paintFormXObjectEnd) ctm = stack.pop() || ctm;
    else if (fn === O.paintImageXObject || fn === O.paintImageXObjectRepeat) {
      imgs.push({ id: a[0], kind: "x", w: a[1], h: a[2], bbox: toBox(ctm) });
    } else if (fn === O.paintInlineImageXObject) {
      imgs.push({ id: null, kind: "inline", obj: a[0], w: a[0].width, h: a[0].height, bbox: toBox(ctm) });
    } else if (fn === O.constructPath) {
      // a = [ops[], coords[], minMax] — 선분(lineTo)·네모(rectangle)만 본다
      const pops = a[0], co = a[1];
      let k = 0, cx = 0, cy = 0;
      for (const op of pops) {
        if (op === O.rectangle) {
          const [x, y, w, h] = co.slice(k, k + 4); k += 4;
          const p0 = apply(ctm, x, y), p1 = apply(ctm, x + w, y + h);
          const r = [Math.min(p0[0], p1[0]), Math.min(p0[1], p1[1]), Math.max(p0[0], p1[0]), Math.max(p0[1], p1[1])];
          if (r[3] - r[1] > 4 && r[2] - r[0] > 1) { edges.push([r[0], r[1], r[3]]); edges.push([r[2], r[1], r[3]]); }
          else if (r[2] - r[0] <= 1.2 && r[3] - r[1] > 4) edges.push([(r[0] + r[2]) / 2, r[1], r[3]]);
        } else if (op === O.moveTo) { cx = co[k++]; cy = co[k++]; }
        else if (op === O.lineTo) {
          const nx = co[k++], ny = co[k++];
          const p = apply(ctm, cx, cy), q = apply(ctm, nx, ny);
          if (Math.abs(p[0] - q[0]) < 0.6 && Math.abs(p[1] - q[1]) > 4) edges.push([p[0], Math.min(p[1], q[1]), Math.max(p[1], q[1])]);
          cx = nx; cy = ny;
        } else if (op === O.curveTo) { k += 6; } else if (op === O.curveTo2 || op === O.curveTo3) { k += 4; }
      }
    }
  }
  return { imgs, edges, ops };
}
// 그림 화소 → 흰 바탕 RGBA Img
export async function imageData(page, im) {
  let o = im.obj;
  if (!o) {
    const store = String(im.id).startsWith("g_") ? page.commonObjs : page.objs;
    o = await new Promise((res) => store.get(im.id, res));
  }
  if (!o) return null;
  const { width: w, height: h } = o;
  const out = newImg(w, h);
  if (o.bitmap) {
    const c = canvas(w, h), ctx = c.getContext("2d", { willReadFrequently: true });
    ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, w, h); ctx.drawImage(o.bitmap, 0, 0);
    return canvasToImg(c);
  }
  const d = o.data;
  if (o.kind === 3) { out.d.set(d.subarray(0, w * h * 4)); return flattenWhite(out); }
  if (o.kind === 2) {
    for (let i = 0, j = 0; i < w * h; i++, j += 3) { out.d[i * 4] = d[j]; out.d[i * 4 + 1] = d[j + 1]; out.d[i * 4 + 2] = d[j + 2]; }
    return out;
  }
  if (o.kind === 1) {
    const rowBytes = (w + 7) >> 3;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const bit = (d[y * rowBytes + (x >> 3)] >> (7 - (x & 7))) & 1;
      const v = bit ? 255 : 0, i = (y * w + x) * 4;
      out.d[i] = out.d[i + 1] = out.d[i + 2] = v;
    }
    return out;
  }
  return null;
}

// ── 쪽 그리기: clip(pt, 왼쪽 위 원점)을 dpi 로
export async function renderClip(page, clip, dpi = 150, grayOnly = false) {
  const s = dpi / 72;
  const vp0 = page.getViewport({ scale: 1 });
  const [x0, y0, x1, y1] = clip || [0, 0, vp0.width, vp0.height];
  const W = Math.max(1, Math.ceil((x1 - x0) * s)), H = Math.max(1, Math.ceil((y1 - y0) * s));
  const c = canvas(W, H);
  const ctx = c.getContext("2d", { willReadFrequently: true });
  ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H);
  const vp = page.getViewport({ scale: s, offsetX: -x0 * s, offsetY: -y0 * s });
  await page.render({ canvasContext: ctx, viewport: vp, background: "rgb(255,255,255)" }).promise;
  const im = canvasToImg(c);
  return grayOnly ? gray(im) : im;
}
// 덩이 자리의 글자 색(잉크 화소 평균) — 매쓰플랫 파란 번호(0x00ABFF) 찾기
export function inkColor(im, s, box) {
  const [x0, y0, x1, y1] = box.map((v) => Math.round(v * s));
  let r = 0, g = 0, b = 0, n = 0;
  for (let y = Math.max(0, y0); y < Math.min(im.h, y1); y++) for (let x = Math.max(0, x0); x < Math.min(im.w, x1); x++) {
    const i = (y * im.w + x) * 4;
    const R = im.d[i], G = im.d[i + 1], B = im.d[i + 2];
    if (R + G + B > 690) continue;
    // 가장 진한 화소 위주 (글자 가장자리 섞임 줄이기)
    const k = 765 - (R + G + B);
    r += R * k; g += G * k; b += B * k; n += k;
  }
  return n ? [r / n, g / n, b / n] : null;
}
export const isBlue = (c) => !!c && c[0] < 90 && c[1] > 120 && c[1] < 215 && c[2] > 200;

// rgb 0~1
export const rgb01 = (P, c) => P.rgb(c[0], c[1], c[2]);
