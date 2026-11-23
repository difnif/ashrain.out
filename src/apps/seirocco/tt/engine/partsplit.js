// 매쓰플랫 문항 그림을 부품(발문 줄 · 그림 · <보기> 상자 · 선택지)으로 나누고 배열을 바꾼 변형을 만든다 (PC partsplit.py 그대로)
import { gray, crop, newImg, paste, canvas, imgToCanvas, canvasToImg } from "./base";

const REF_W = 930, INK = 200, GAP_STD = 40, CH_GAP = 28;

function runs(v, gap = 0) {
  const out = [];
  let x = 0;
  const n = v.length;
  while (x < n) {
    if (v[x]) {
      const x0 = x;
      while (x < n && v[x]) x++;
      if (out.length && x0 - out[out.length - 1][1] <= gap) out[out.length - 1] = [out[out.length - 1][0], x];
      else out.push([x0, x]);
    } else x++;
  }
  return out;
}
// 회색 배열 도우미 (g: {w,h,g})
const at = (G, x, y) => G.g[y * G.w + x];
function colsAny(G, y0, y1, x0 = 0, x1 = G.w) {
  const v = new Uint8Array(Math.max(0, x1 - x0));
  for (let y = Math.max(0, y0); y < Math.min(G.h, y1); y++) for (let x = Math.max(0, x0); x < Math.min(G.w, x1); x++) if (at(G, x, y) < INK) v[x - x0] = 1;
  return v;
}
function rowsAny(G, y0, y1, x0 = 0, x1 = G.w) {
  const v = new Uint8Array(Math.max(0, y1 - y0));
  for (let y = Math.max(0, y0); y < Math.min(G.h, y1); y++) for (let x = Math.max(0, x0); x < Math.min(G.w, x1); x++) if (at(G, x, y) < INK) { v[y - y0] = 1; break; }
  return v;
}
function isCircled(G, bx0, by0, w, h) {
  const blk = (yy, xx) => at(G, bx0 + xx, by0 + yy) < INK;
  const cy = (h - 1) / 2, cx = (w - 1) / 2;
  const r = (h + w) / 4 - 1.0;
  let hit = 0;
  const n = 72;
  for (let k = 0; k < n; k++) {
    const t = (2 * Math.PI * k) / n;
    let ok = false;
    for (const dr of [-3, -2, -1, 0, 1]) {
      const yy = Math.round(cy + (r + dr) * Math.sin(t)), xx = Math.round(cx + (r + dr) * Math.cos(t));
      if (yy >= 0 && yy < h && xx >= 0 && xx < w && blk(yy, xx)) { ok = true; break; }
    }
    hit += ok ? 1 : 0;
  }
  let out = 0, tot = 0;
  for (let yy = 0; yy < h; yy++) for (let xx = 0; xx < w; xx++) {
    if ((yy - cy) ** 2 + (xx - cx) ** 2 > (r + 2.5) ** 2) { tot++; if (blk(yy, xx)) out++; }
  }
  const corner = tot ? out / tot : 0;
  return hit / n >= 0.85 && corner <= 0.03;
}
function circleDigit(G, x, y0, y1) {
  const sx0 = Math.max(0, x - 2), sx1 = Math.min(G.w, x + 46);
  const cols = colsAny(G, y0, y1, sx0, sx1);
  const rs = runs(cols).filter((r) => r[0] <= 6);
  if (!rs.length) return null;
  const [cx0, cx1] = rs[0];
  if (!(cx1 - cx0 >= 28 && cx1 - cx0 <= 44)) return null;
  const rows = rowsAny(G, y0, y1, sx0 + cx0, sx0 + cx1);
  const rr = runs(rows).filter((r) => r[1] - r[0] >= 28 && r[1] - r[0] <= 44);
  if (!rr.length) return null;
  const [ry0, ry1] = rr[0];
  if (Math.abs(ry1 - ry0 - (cx1 - cx0)) > 5) return null;
  return isCircled(G, sx0 + cx0, y0 + ry0, cx1 - cx0, ry1 - ry0) ? 1 : null;
}
function cellStarts(G, y0, y1) {
  const cols = colsAny(G, y0, y1);
  const out = [];
  for (const [r0, r1] of runs(cols, 10)) if (r1 - r0 >= 28 && r1 - r0 <= 44 && circleDigit(G, r0, y0, y1)) out.push([r0, 0]);
  return out;
}
export function analyse(img) {
  const G = gray(img);
  const { w: W, h: H } = G;
  const rowInk = rowsAny(G, 0, H);
  const parts = [];
  for (const [y0, y1] of runs(rowInk)) {
    const c = colsAny(G, y0, y1);
    let x0 = -1, x1 = -1;
    for (let x = 0; x < W; x++) if (c[x]) { if (x0 < 0) x0 = x; x1 = x + 1; }
    parts.push({ y0, y1, x0, x1, kind: null });
  }
  for (const p of parts) if (p.x0 <= 6 && p.y1 - p.y0 >= 33 && circleDigit(G, p.x0, p.y0, p.y1)) p.kind = "ch";
  const merged = [];
  for (const p of parts) {
    const m = merged[merged.length - 1];
    if (m && m.kind === "ch" && p.kind === null && p.x0 >= 40 && p.y0 - m.y1 < 26) { m.y1 = p.y1; m.x1 = Math.max(m.x1, p.x1); continue; }
    merged.push(p);
  }
  for (const p of merged) {
    if (p.kind) continue;
    const h = p.y1 - p.y0;
    const full = p.x0 <= 12 && p.x1 >= W - 25;
    let topLine = false;
    if (h > 60) {
      let mx = 0;
      for (let y = p.y0; y < p.y0 + 4; y++) { let s = 0; for (let x = 0; x < W; x++) if (at(G, x, y) < INK) s++; mx = Math.max(mx, s); }
      topLine = mx > 0.85 * (p.x1 - p.x0);
    }
    if (full && topLine && h > 80) p.kind = "box";
    else if (p.x0 <= 12 && h <= 100) p.kind = "line";
    else p.kind = "fig";
  }
  const out = [];
  for (const p of merged) {
    const o = out[out.length - 1];
    if (o && p.kind === "fig" && o.kind === "fig" && p.y0 - o.y1 < 45) { o.y1 = p.y1; o.x0 = Math.min(o.x0, p.x0); o.x1 = Math.max(o.x1, p.x1); continue; }
    if (o && o.kind === "fig" && p.kind === "line" && p.y0 - o.y1 < 30 && p.x0 > 12) { o.y1 = p.y1; o.x0 = Math.min(o.x0, p.x0); o.x1 = Math.max(o.x1, p.x1); continue; }
    out.push(p);
  }
  for (const p of out) if (p.kind === "ch") p.cells = cellStarts(G, p.y0, p.y1);
  return { parts: out, W, H, G };
}
function choiceCells(img, parts, G) {
  const out = [];
  const W = img.w;
  for (const p of parts) {
    if (p.kind !== "ch") continue;
    const cells = p.cells || [];
    if (!cells.length) return null;
    const xs = cells.map((c) => c[0]);
    for (let idx = 0; idx < cells.length; idx++) {
      const x = cells[idx][0];
      const xEnd = idx + 1 < xs.length ? xs[idx + 1] - 8 : W;
      const c = colsAny(G, p.y0, p.y1, x, xEnd);
      let last = -1;
      for (let k = 0; k < c.length; k++) if (c[k]) last = k;
      if (last < 0) return null;
      out.push(crop(img, x, p.y0, Math.min(xEnd, x + last + 2), p.y1));
    }
  }
  if (!(out.length >= 4 && out.length <= 5)) return null;
  return out;
}
function compose(blocks, W) {
  const H = blocks.reduce((a, [b, , gap]) => a + b.h + gap, 0);
  const cv = newImg(W, Math.max(H, 1));
  let y = 0;
  for (const [b, align, gap] of blocks) {
    y += gap;
    const x = align === "center" ? Math.floor((W - b.w) / 2) : align === "left" ? 0 : Math.trunc(align);
    paste(cv, b, Math.max(0, x), y);
    y += b.h;
  }
  return cv;
}
function choiceBlock(cells, per, W) {
  const slot = Math.floor(W / per);
  const imgs = [];
  for (let i = 0; i < cells.length; i += per) {
    const r = cells.slice(i, i + per);
    const h = Math.max(...r.map((c) => c.h));
    const row = newImg(W, h);
    r.forEach((c, j) => paste(row, c, j * slot, Math.floor((h - c.h) / 2)));
    imgs.push(row);
  }
  return compose(imgs.map((im, i) => [im, "left", i ? CH_GAP : 0]), W);
}
function scaleImg(im, k) {
  const c = canvas(Math.max(1, Math.trunc(im.w * k)), Math.max(1, Math.trunc(im.h * k)));
  const ctx = c.getContext("2d", { willReadFrequently: true });
  ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
  ctx.drawImage(imgToCanvas(im), 0, 0, c.width, c.height);
  return canvasToImg(c);
}
// (변형 그림, 벌점) 목록 — 원본은 넣지 않음
export function variants(img, A = null) {
  if (img.w !== REF_W) return [];
  const { parts, W, H, G } = A || analyse(img);
  const kinds = parts.map((p) => p.kind);
  const out = [];
  const cropP = (p) => crop(img, 0, Math.max(0, p.y0), W, Math.min(H, p.y1));
  const build = (compact, figK, chMode) => {
    const blocks = [];
    let prev = null;
    const chParts = parts.filter((p) => p.kind === "ch");
    const cells = chMode ? choiceCells(img, parts, G) : null;
    if (chMode && !cells) return null;
    for (const p of parts) {
      if (p.kind === "ch" && chMode) continue;
      let gap = prev === null ? 0 : p.y0 - prev.y1;
      if (compact && gap > 70) gap = GAP_STD;
      if (p.kind === "fig" && figK !== 1.0) {
        const f = scaleImg(crop(img, p.x0, p.y0, p.x1, p.y1), figK);
        const cx = (p.x0 + p.x1) / 2;
        blocks.push([f, p.x0 > 12 ? Math.trunc(cx - f.w / 2) : 0, gap]);
      } else blocks.push([cropP(p), "left", gap]);
      prev = p;
    }
    if (chMode) {
      const per = { "5row": 5, "2col": 2, "1col": 1 }[chMode];
      const mw = Math.max(...cells.map((c) => c.w));
      if (per === 5 && mw > Math.floor(W / 5) - 6) return null;
      if (per === 2 && !(W * 0.22 <= mw && mw <= Math.floor(W / 2) - 6)) return null;
      let gap = prev === null ? 0 : chParts[0].y0 - prev.y1;
      if (compact && gap > 70) gap = GAP_STD;
      blocks.push([choiceBlock(cells, per, W), "left", gap]);
    }
    return compose(blocks, W);
  };
  const hasFig = kinds.includes("fig"), hasCh = kinds.includes("ch");
  const bigGap = parts.some((p, i) => i + 1 < parts.length && parts[i + 1].y0 - p.y1 > 70);
  const plans = [];
  if (bigGap) plans.push([true, 1.0, null, 0.05]);
  if (hasFig) plans.push([true, 0.8, null, 0.3]);
  if (hasCh) {
    plans.push([true, 1.0, "5row", 0.15]);
    plans.push([false, 1.0, "2col", 0.35]);
    if (hasFig) plans.push([true, 0.8, "5row", 0.4]);
  }
  const seen = new Set([H]);
  for (const [compact, fk, ch, pen] of plans) {
    let v = null;
    try { v = build(compact, fk, ch); } catch { v = null; }
    if (!v || seen.has(v.h)) continue;
    seen.add(v.h);
    out.push([v, pen]);
  }
  return out;
}
export function info(img, A = null) {
  if (img.w !== REF_W) return { choice: false, fig: false, A: null };
  const a = A || analyse(img);
  const ks = new Set(a.parts.map((p) => p.kind));
  return { choice: ks.has("ch") && choiceCells(img, a.parts, a.G) !== null, fig: ks.has("fig"), A: a };
}
