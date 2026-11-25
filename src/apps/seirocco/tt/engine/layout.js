// 강사도구 엔진 — 시험지 짜기 (PC mf2exam: 쪽·단 배치 · 문정중/초등 양식 · 머리 · 바닥글) + 정답과 해설 (mfsolution.build_answer_pdf)
import { MM, A4W, A4H, twoPass, baseOf, isXmas } from "./base";
import { TEMPLATES } from "../logic";
export { baseOf, isXmas };
export const TEMPLATE_KEYS = TEMPLATES.map(([k]) => k);

export const DEFAULTS = {
  제목: "", 부제: "", 윗줄: "", 바닥글_왼쪽: "수학", 바닥글_오른쪽: "", 소요시간: "",
  목표_여백_mm: 45, 최소_여백_mm: 22, 단당_최대_문항: 4, 그림_선택지_변형: true, 정답해설_분리: true, 끝_표시: true,
  양식: "문정중", 주관식_이름: "서답형", 대상: "", 코드: "", 정답해설_원본모양: false,
};
export const GEO = {
  frame: [11 * MM, 11 * MM, A4W - 11 * MM, A4H - 17 * MM],
  head_h: 30 * MM, pad_t: 4 * MM, pad_side: 4.2 * MM, pad_bL: 3 * MM, pad_bR: 7.5 * MM, gutter: 6.6 * MM, end_h: 6 * MM,
};
export const fmtCode = (c) => { c = String(c || "").toUpperCase(); return c.length === 6 ? `${c.slice(0, 3)}-${c.slice(3)}` : c; };

// 「초등 크리스마스」: 테두리 안 아래 눈밭 띠(트리·산타·순록) 자리만큼 단 아래 끝을 올린다.
// 장식 그림은 public/tt-deco/xmas.pdf (쪽 0 전구 줄 · 1 화환 · 2 눈밭 띠) — 그린 코드는 프로젝트 문서 SRC-초등크리스마스양식-v1.py
export const XMAS = { strip_h: 26 * MM, pad_b: 27.5 * MM };
const XMAS_LIGHTS = [0, 0, A4W, 34];
const xmasStripBox = () => [0, GEO.frame[3] - XMAS.strip_h - 2, A4W, GEO.frame[3] + 1];
let xmasBytes = null;
async function xmasDeco(doc) {
  if (!xmasBytes) {
    xmasBytes = fetch("/tt-deco/xmas.pdf").then((r) => { if (!r.ok) throw new Error("크리스마스 장식 파일을 불러오지 못했어요"); return r.arrayBuffer(); })
      .then((b) => new Uint8Array(b)).catch((e) => { xmasBytes = null; throw e; });
  }
  const [lights, wreath, strip] = await doc.embedPdf(await xmasBytes, [0, 1, 2]);
  return { lights, wreath, strip };
}
function drawDeco(pen, emb, [bx0, by0, bx1, by1]) {
  pen.p.drawPage(emb, { x: bx0, y: A4H - by1, width: bx1 - bx0, height: by1 - by0 });
}

export function colBox(pageNo, side, cfg = null) {
  const [x0, y0, x1, y1] = GEO.frame;
  const cw = (x1 - x0) / 2;
  const top = y0 + (pageNo === 0 ? GEO.head_h : 0);
  const cx0 = x0 + side * cw;
  const padB = cfg && isXmas(cfg.양식) ? XMAS.pad_b : side === 0 ? GEO.pad_bL : GEO.pad_bR;
  return [cx0 + GEO.pad_side, top + GEO.pad_t, cx0 + cw - GEO.pad_side, y1 - padB];
}
function colCaps(P, cfg) {
  const caps = [];
  for (let pg = 0; pg < P; pg++) for (const side of [0, 1]) { const [, y0, , y1] = colBox(pg, side, cfg); caps.push(y1 - y0); }
  if (cfg.끝_표시) caps[caps.length - 1] -= GEO.end_h;
  return caps;
}
function solveLayout(heights, weights, pens, P, cfg) {
  const caps = colCaps(P, cfg);
  const n = heights.length, C = caps.length;
  if (n < C) return null;
  const MIN = cfg.최소_여백_mm * MM, MAXN = cfg.단당_최대_문항;
  const base = heights.map((h) => Math.min(...h));
  const sumW = weights.reduce((a, b) => a + b, 0);
  const T = (caps.reduce((a, b) => a + b, 0) - heights.reduce((a, h) => a + h[0], 0)) / Math.max(sumW, 1e-9);
  if (T <= MIN) return null;
  const INF = Infinity;
  const D = Array.from({ length: C + 1 }, () => new Array(n + 1).fill(INF));
  const Pk = Array.from({ length: C + 1 }, () => new Array(n + 1).fill(null));
  D[0][0] = 0;
  const cache = new Map();
  const seg = (k, i, cap) => {
    const key = k + ":" + i + ":" + cap;
    if (cache.has(key)) return cache.get(key);
    let ww = 0;
    for (let t = k; t < i; t++) ww += weights[t];
    let best = [INF, null];
    const pick = [];
    const rec = (t, hs, pen) => {
      if (t === i) {
        const u = (cap - hs) / ww;
        if (u < MIN) return;
        const r = u / T;
        const c = ww * Math.log(r) ** 2 + 0.05 * pen;
        if (c < best[0]) best = [c, pick.slice()];
        return;
      }
      let rest = 0;
      for (let q = t; q < i; q++) rest += base[q];
      if (hs + rest > cap - MIN * ww) return;
      heights[t].forEach((h, vi) => { pick.push(vi); rec(t + 1, hs + h, pen + pens[t][vi]); pick.pop(); });
    };
    rec(k, 0, 0);
    cache.set(key, best);
    return best;
  };
  for (let j = 1; j <= C; j++) {
    for (let i = 1; i <= n; i++) {
      for (let k = Math.max(j - 1, i - MAXN); k < i; k++) {
        if (D[j - 1][k] === INF) continue;
        const [c, pick] = seg(k, i, caps[j - 1]);
        if (!pick) continue;
        if (D[j - 1][k] + c < D[j][i]) { D[j][i] = D[j - 1][k] + c; Pk[j][i] = [k, pick]; }
      }
    }
  }
  if (D[C][n] === INF) return null;
  const cols = [];
  let i = n;
  for (let j = C; j > 0; j--) { const [k, pick] = Pk[j][i]; cols.unshift([k, i, pick]); i = k; }
  return { P, cost: D[C][n], T, cols, caps };
}
export function plan(items, cfg) {
  const n = items.length;
  const target = cfg.목표_여백_mm * MM;
  let best = null;
  for (let P = 1; P < Math.floor(n / 2) + 2; P++) {
    const r = solveLayout(items.map((it) => it.heights), items.map((it) => it.w), items.map((it) => it.pens), P, cfg);
    if (!r) continue;
    r.score = r.cost + 1.5 * n * Math.log(r.T / target) ** 2;
    if (!best || r.score < best.score) best = r;
    if (r.T > target * 1.6) break;
  }
  if (!best && n >= 1) {
    // 문항이 아주 적으면(1개 등) 첫 단에만 — PC판에는 없던 예비 배치
    const caps = colCaps(1, cfg);
    const h = items.reduce((a, it) => a + it.heights[0], 0);
    if (n === 1 || h < caps[0]) best = { P: 1, cost: 0, T: Math.max(1, (caps[0] - h) / Math.max(1e-9, items.reduce((a, it) => a + it.w, 0))), cols: [[0, n, items.map(() => 0)], [n, n, []]], caps };
  }
  return best;
}

// ── 펜 (pdf-lib, 좌표는 PyMuPDF 처럼 왼쪽 위 원점 · y 는 글자 바닥선)
export class Pen {
  constructor(ctx, page) { this.c = ctx; this.p = page; }
  width(s, size, bold = false) { return (bold ? this.c.B : this.c.R).widthOfTextAtSize(String(s), size); }
  fit(s, size, maxw, bold = false, smallest = 8) { const w = this.width(s, size, bold); return w <= maxw ? size : Math.max(smallest, (size * maxw) / w); }
  text(x, y, s, { size = 10, bold = false, align = "left", color = [0, 0, 0] } = {}) {
    s = String(s);
    if (!s) return 0;
    const w = this.width(s, size, bold);
    if (align === "center") x -= w / 2; else if (align === "right") x -= w;
    this.p.drawText(s, { x, y: A4H - y, size, font: bold ? this.c.B : this.c.R, color: this.c.P.rgb(...color) });
    return w;
  }
  line(x0, y0, x1, y1, { width = 1, color = [0, 0, 0], dashes = null } = {}) {
    this.p.drawLine({ start: { x: x0, y: A4H - y0 }, end: { x: x1, y: A4H - y1 }, thickness: width, color: this.c.P.rgb(...color), dashArray: dashes || undefined });
  }
  rect(x0, y0, x1, y1, { width = 1, color = [0, 0, 0], fill = null, radius = 0 } = {}) {
    const P = this.c.P;
    const opt = {};
    if (color) { opt.borderColor = P.rgb(...color); opt.borderWidth = width; } else opt.borderWidth = 0;
    if (fill) opt.color = P.rgb(...fill);
    if (radius) {
      const d = Math.min(x1 - x0, y1 - y0) * radius;
      const k = 0.5523 * d;
      const path = `M ${x0 + d} ${y0} L ${x1 - d} ${y0} C ${x1 - d + k} ${y0} ${x1} ${y0 + d - k} ${x1} ${y0 + d} L ${x1} ${y1 - d} C ${x1} ${y1 - d + k} ${x1 - d + k} ${y1} ${x1 - d} ${y1} L ${x0 + d} ${y1} C ${x0 + d - k} ${y1} ${x0} ${y1 - d + k} ${x0} ${y1 - d} L ${x0} ${y0 + d} C ${x0} ${y0 + d - k} ${x0 + d - k} ${y0} ${x0 + d} ${y0} Z`;
      this.p.drawSvgPath(path, { x: 0, y: A4H, ...opt });
    } else {
      this.p.drawRectangle({ x: x0, y: A4H - y1, width: x1 - x0, height: y1 - y0, ...opt });
    }
  }
  circle(cx, cy, r, { width = 1, color = [0, 0, 0], fill = null, dashes = null } = {}) {
    const P = this.c.P;
    const opt = { x: cx, y: A4H - cy, size: r };
    if (color) { opt.borderColor = P.rgb(...color); opt.borderWidth = width; if (dashes) opt.borderDashArray = dashes; } else opt.borderWidth = 0;
    if (fill) opt.color = P.rgb(...fill);
    this.p.drawCircle(opt);
  }
  image(img, x0, y0, x1, y1) { this.p.drawImage(img, { x: x0, y: A4H - y1, width: x1 - x0, height: y1 - y0 }); }
}

function drawHeader(pen, cfg, title, sub, n, npages, nch) {
  const [x0, y0, x1] = GEO.frame;
  const hb = y0 + GEO.head_h;
  const tw = 62 * MM;
  pen.line(x0, hb, x1, hb, { width: 1.2 });
  pen.line(x1 - tw, y0, x1 - tw, hb, { width: 0.9 });
  const cx = (x0 + x1 - tw) / 2;
  const room = x1 - tw - x0 - 8 * MM;
  const lines = [];
  if (cfg.윗줄) lines.push([cfg.윗줄, pen.fit(cfg.윗줄, 9, room), false]);
  lines.push([title, pen.fit(title, 15.5, room, true, 9), true]);
  if (sub) lines.push([sub, pen.fit(sub, 10.5, room), false]);
  lines.push([`${n}문항 · 총 ${npages}면` + (cfg.코드 ? ` · 코드 ${fmtCode(cfg.코드)}` : ""), 8.8, false]);
  const hs = lines.map(([, s]) => s * 1.45);
  let y = y0 + (GEO.head_h - hs.reduce((a, b) => a + b, 0)) / 2;
  lines.forEach(([s, size, bold], i) => { y += hs[i]; pen.text(cx, y - hs[i] * 0.28, s, { size, bold, align: "center" }); });
  const rows = [["선택형", `${nch}문항`], [cfg.주관식_이름 || "서답형", `${n - nch}문항`], ["이름", cfg.대상 || ""]];
  if (cfg.소요시간) rows.push(["소요시간", String(cfg.소요시간)]);
  const rh = GEO.head_h / rows.length, lw = 18 * MM;
  rows.forEach(([k, v], r) => {
    const ry = y0 + r * rh;
    if (r) pen.line(x1 - tw, ry, x1, ry, { width: 0.8 });
    pen.text(x1 - tw + lw / 2, ry + rh / 2 + 3.5, k, { size: pen.fit(k, 10, lw - 2 * MM, true), bold: true, align: "center" });
    if (k === "이름") cfg._name_box = { page: 0, rect: [x1 - tw + lw, ry, x1, ry + rh].map((v2) => Math.round(v2 * 100) / 100), size: 10, align: "center" };
    if (v) pen.text(x1 - tw + lw + (tw - lw) / 2, ry + rh / 2 + 3.5, v, { size: 10, align: "center" });
  });
  pen.line(x1 - tw + lw, y0, x1 - tw + lw, hb, { width: 0.8 });
}

export const EL_ACC = [0.13, 0.58, 0.53], EL_DARK = [0.09, 0.27, 0.27], EL_SOFT = [0.9, 0.97, 0.95], EL_GRAY = [0.55, 0.6, 0.64];
export const EL_DOTS = [[0.13, 0.58, 0.53], [0.96, 0.47, 0.55], [0.98, 0.66, 0.2], [0.36, 0.52, 0.89]];
function pill(pen, x, y, w, h, label, value) {
  pen.rect(x, y, x + w, y + h, { color: EL_ACC, fill: [1, 1, 1], width: 1.1, radius: 0.5 });
  pen.text(x + 4 * MM, y + h / 2 + 3.4, label, { size: 9.5, bold: true, color: EL_ACC });
  if (value) {
    const lw = pen.width(label, 9.5, true) + 7 * MM;
    pen.text(x + lw, y + h / 2 + 3.6, value, { size: pen.fit(value, 11, w - lw - 3 * MM, true), bold: true, color: EL_DARK });
  }
}
function drawHeaderElem(pen, cfg, title, sub, n, npages, nch, deco = null) {
  const [x0, y0, x1] = GEO.frame;
  const band = [x0 + 2.5 * MM, y0 + 2.5 * MM, x1 - 2.5 * MM, y0 + GEO.head_h - 1.5 * MM];
  pen.rect(...band, { color: null, fill: EL_SOFT, radius: 0.18 });
  const stR = 10.5 * MM;
  const scx = band[2] - stR - 3.5 * MM, scy = (band[1] + band[3]) / 2;
  if (deco) drawDeco(pen, deco.wreath, [scx - 42, scy - 42, scx + 42, scy + 42]);   // 도장 둘레 화환 (원 안쪽은 아래 흰 원이 덮음)
  pen.circle(scx, scy, stR, { color: EL_DOTS[1], width: 1.1, dashes: [2.5, 2], fill: [1, 1, 1] });
  pen.text(scx, scy - 1.0, "참 잘했어요", { size: 7.5, bold: true, align: "center", color: EL_DOTS[1] });
  pen.text(scx, scy + 9, "도장", { size: 7, align: "center", color: EL_GRAY });
  const pw = 54 * MM, ph = 8.6 * MM;
  const px = scx - stR - 4 * MM - pw;
  pill(pen, px, band[1] + 4 * MM, pw, ph, "이름", cfg.대상 || "");
  const lw = pen.width("이름", 9.5, true) + 7 * MM;
  cfg._name_box = { page: 0, rect: [px + lw - 2, band[1] + 4 * MM, px + pw - 2 * MM, band[1] + 4 * MM + ph].map((v) => Math.round(v * 100) / 100), size: 11, align: "left", bold: true };
  pill(pen, px, band[1] + 4 * MM + ph + 2.6 * MM, pw, ph, "날짜", "       월       일");
  const room = px - band[0] - 9 * MM;
  const tx = band[0] + 5 * MM;
  pen.text(tx, band[1] + 11 * MM, title, { size: pen.fit(title, 17, room, true, 10), bold: true, color: EL_DARK });
  if (sub) pen.text(tx, band[1] + 17 * MM, sub, { size: pen.fit(sub, 10.5, room), color: EL_GRAY });
  const lab = cfg.주관식_이름 || "서답형";
  let meta = `모두 ${n}문제 (선택형 ${nch} · ${lab} ${n - nch}) · ${npages}쪽`;
  if (cfg.코드) meta += ` · 코드 ${fmtCode(cfg.코드)}`;
  pen.text(tx, band[1] + 22.6 * MM, meta, { size: pen.fit(meta, 8.6, room), color: EL_ACC });
}

// items: [{seq, choice, w, heights[], sizes[[w,h]], renders[png bytes]}] · layout: plan() 결과 → PDF bytes
export async function renderSheet(items, layout, cfg, title, sub) {
  return twoPass(cfg.양식, async (ctx) => {
  const elem = baseOf(cfg.양식) === "초등";
  const deco = isXmas(cfg.양식) ? await xmasDeco(ctx.doc) : null;
  const P = layout.P;
  const [x0, y0, x1, y1] = GEO.frame;
  const nch = items.filter((it) => it.choice).length;
  const embedded = new Map();
  const emb = async (it, v) => {
    const key = it.seq + ":" + v;
    if (!embedded.has(key)) embedded.set(key, await ctx.doc.embedPng(it.renders[v]));
    return embedded.get(key);
  };
  for (let pg = 0; pg < P; pg++) {
    const page = ctx.doc.addPage([A4W, A4H]);
    const pen = new Pen(ctx, page);
    const top = y0 + (pg === 0 ? GEO.head_h : 0);
    const fy = A4H - 9 * MM;
    const right = cfg.바닥글_오른쪽 || (cfg.코드 ? `코드 ${fmtCode(cfg.코드)}` : "");
    if (elem) {
      pen.rect(x0, y0, x1, y1, { color: EL_ACC, width: 1.6, radius: 0.025 });
      pen.line((x0 + x1) / 2, top + 3 * MM, (x0 + x1) / 2, deco ? y1 - XMAS.strip_h - 1.5 * MM : y1 - 3 * MM, { color: [0.8, 0.86, 0.88], width: 0.9, dashes: [3, 3] });
      if (pg === 0) drawHeaderElem(pen, cfg, title, sub, items.length, P, nch, deco);
      if (deco) { drawDeco(pen, deco.lights, XMAS_LIGHTS); drawDeco(pen, deco.strip, xmasStripBox()); }
      if (cfg.바닥글_왼쪽) pen.text(x0 + 2 * MM, fy, cfg.바닥글_왼쪽, { size: 9, color: EL_GRAY });
      pen.text(A4W / 2, fy, `${pg + 1} / ${P}`, { size: 9.5, bold: true, align: "center", color: EL_ACC });
      if (right) pen.text(x1 - 2 * MM, fy, right, { size: 9, align: "right", color: EL_GRAY });
      if (pg < P - 1) pen.text(x1 - 5 * MM, y1 - 2.4 * MM, "다음 쪽에 계속", { size: 9, bold: true, align: "right", color: EL_ACC });
    } else {
      pen.rect(x0, y0, x1, y1, { width: 1.3 });
      pen.line((x0 + x1) / 2, top, (x0 + x1) / 2, y1, { width: 0.9 });
      if (pg === 0) drawHeader(pen, cfg, title, sub, items.length, P, nch);
      pen.text(x0, fy, cfg.바닥글_왼쪽, { size: 9.5 });
      pen.text(A4W / 2, fy, `${P}면 중 − ${pg + 1}`, { size: 9.5, align: "center" });
      if (right) pen.text(x1, fy, right, { size: 9.5, align: "right" });
      if (pg < P - 1) pen.text(x1 - 4 * MM, y1 - 2.2 * MM, pg % 2 === 0 ? "[뒷면에 계속]" : "[다음 장에 계속]", { size: 9.5, bold: true, align: "right" });
    }
    for (const side of [0, 1]) {
      const ci = pg * 2 + side;
      const [k, i, pick] = layout.cols[ci];
      const [cx0, cy0, cx1, cy1] = colBox(pg, side, cfg);
      const cap = layout.caps[ci];
      const idx = [];
      for (let t = k; t < i; t++) idx.push(t);
      const hs = idx.map((t, q) => items[t].heights[pick[q]]);
      const ww = idx.reduce((a, t) => a + items[t].w, 0);
      const u = ww ? (cap - hs.reduce((a, b) => a + b, 0)) / ww : 0;
      let y = cy0;
      for (let q = 0; q < idx.length; q++) {
        const it = items[idx[q]], v = pick[q], h = hs[q];
        if (elem) {
          const r = 3.1 * MM;
          const c = EL_DOTS[(it.seq - 1) % EL_DOTS.length];
          pen.circle(cx0 + r, y + r + 0.6, r, { color: null, fill: c });
          const num = String(it.seq);
          pen.text(cx0 + r, y + r + 3.6, num, { size: num.length < 3 ? 9.6 : 8, bold: true, align: "center", color: [1, 1, 1] });
        } else {
          pen.text(cx0, y + 10.2, `${it.seq}.`, { size: pen.fit(`${it.seq}.`, 11, GEO.gutter - 1, true, 7), bold: true });   // 100. 이상도 번호 칸 안에
        }
        const w = it.sizes[v][0];
        pen.image(await emb(it, v), cx0 + GEO.gutter, y, cx0 + GEO.gutter + w, y + h);
        y += h + u * it.w;
      }
      if (ci === 2 * P - 1 && cfg.끝_표시) {
        if (elem) pen.text((cx0 + cx1) / 2, cy1 - 1.6 * MM, "끝! 수고했어요", { size: 10.5, bold: true, align: "center", color: EL_ACC });
        else pen.text((cx0 + cx1) / 2, cy1 - 1.6 * MM, "<끝>", { size: 10.5, bold: true, align: "center" });
      }
    }
  }
  return ctx.doc.save();
  });
}

// ── 정답과 해설 (강사도구 양식) — entries: [{seq, choice, answer, answer_png, answer_wh:[w,h] pt, sol:{png,w,h}|null}]
const CIRC = { 1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤" };
function theme(cfg) {
  const elem = baseOf(cfg.양식) === "초등";
  return { elem, acc: elem ? EL_ACC : [0, 0, 0], dark: elem ? EL_DARK : [0, 0, 0], soft: elem ? EL_SOFT : [0.94, 0.94, 0.94],
    gray: elem ? EL_GRAY : [0.35, 0.35, 0.35], line: elem ? [0.8, 0.86, 0.88] : [0.55, 0.55, 0.55] };
}
function frame(pen, th, cfg, title, pno, npages, first, deco = null) {
  const [x0, y0, x1, y1] = GEO.frame;
  if (deco) drawDeco(pen, deco.lights, XMAS_LIGHTS);     // 정답지는 전구 줄만 (해설 자리를 줄이지 않게)
  if (th.elem) pen.rect(x0, y0, x1, y1, { color: th.acc, width: 1.6, radius: 0.025 });
  else pen.rect(x0, y0, x1, y1, { width: 1.3 });
  const fy = A4H - 9 * MM;
  pen.text(x0 + (th.elem ? 2 * MM : 0), fy, "정답과 해설", { size: 9.5, color: th.elem ? th.gray : [0, 0, 0] });
  pen.text(A4W / 2, fy, `${pno + 1} / ${npages}`, { size: 9.5, bold: th.elem, align: "center", color: th.elem ? th.acc : [0, 0, 0] });
  if (cfg.코드) pen.text(x1 - (th.elem ? 2 * MM : 0), fy, `코드 ${fmtCode(cfg.코드)}`, { size: 9, align: "right", color: th.gray });
  if (first) {
    const hh = 21 * MM;
    if (th.elem) {
      const band = [x0 + 2.5 * MM, y0 + 2.5 * MM, x1 - 2.5 * MM, y0 + hh - 1.5 * MM];
      pen.rect(...band, { color: null, fill: th.soft, radius: 0.18 });
      pen.text(band[0] + 5 * MM, band[1] + 8.6 * MM, title, { size: pen.fit(title, 15, band[2] - band[0] - 70 * MM, true, 9), bold: true, color: th.dark });
      pen.text(band[0] + 5 * MM, band[1] + 14.2 * MM, "정답과 해설", { size: 10.5, color: th.acc, bold: true });
      if (cfg.코드) pen.text(band[2] - 5 * MM, band[1] + 8.6 * MM, `코드 ${fmtCode(cfg.코드)}`, { size: 10, bold: true, align: "right", color: th.acc });
    } else {
      pen.line(x0, y0 + hh, x1, y0 + hh, { width: 1.2 });
      pen.text((x0 + x1) / 2, y0 + 9.2 * MM, title, { size: pen.fit(title, 15, x1 - x0 - 30 * MM, true, 9), bold: true, align: "center" });
      pen.text((x0 + x1) / 2, y0 + 15.4 * MM, "정답과 해설" + (cfg.코드 ? `  ·  코드 ${fmtCode(cfg.코드)}` : ""), { size: 10, align: "center" });
    }
  }
}
export async function buildAnswerPdf(entries, cfg, title, appendPages = []) {
  return twoPass(cfg.양식, async (ctx) => {
  const th = theme(cfg);
  const deco = isXmas(cfg.양식) ? await xmasDeco(ctx.doc) : null;
  const [x0, y0, x1, y1] = GEO.frame;
  const pages = [];
  const newPage = () => { const p = ctx.doc.addPage([A4W, A4H]); const pen = new Pen(ctx, p); pages.push(pen); return pen; };
  let pen = newPage();
  const top = y0 + 21 * MM + 5 * MM;
  pen.text(x0 + 6 * MM, top + 4.2 * MM, "빠른 정답", { size: 12, bold: true, color: th.elem ? th.acc : [0, 0, 0] });
  let y = top + 8 * MM;
  const isCirc = (e) => e.choice && CIRC[e.answer];
  const wide = entries.some((e) => e.answer_png && !isCirc(e) && (e.answer_wh || [0, 0])[0] > 70);
  let per = wide ? 4 : 5;
  const inner0 = x0 + 6 * MM, inner1 = x1 - 6 * MM;
  const nw = 9 * MM, rowMin = 7.6 * MM;
  // 글자 정답이 긴 프린트(낱말 · 여러 칸 답)는 한 줄 칸 수를 줄이고(5 → 2), 그래도 긴 답은 칸 안에서 줄을 바꾼다
  const tw = (t, size) => pen.width(t, size, false);
  const isTxt = (e) => !isCirc(e) && !e.answer_png && String(e.answer || "") !== "";
  const txts = entries.filter(isTxt).map((e) => String(e.answer));
  while (txts.length && per > 2 && txts.filter((t) => tw(t, 8) > (inner1 - inner0) / per - nw - 3 * MM).length > txts.length * 0.1) per--;
  // 그림 정답(글꼴에 없는 글자 등)이 넓으면 칸 수를 줄여 작아지지 않게 (85% 크기까지는 그대로)
  const aws = entries.filter((e) => e.answer_png && !isCirc(e)).map((e) => (e.answer_wh || [40, 12])[0]);
  while (aws.length && per > 2 && aws.filter((w) => w * 0.85 > (inner1 - inner0) / per - nw - 3 * MM).length > aws.length * 0.1) per--;
  const cw = (inner1 - inner0) / per;
  const aw = cw - nw - 3 * MM;
  const wrap = (t, size) => {
    const lines = [];
    let cur = "";
    for (const w of t.split(/(\s+)/)) {
      const nx = cur + w;
      if (!cur.trim() || tw(nx.trim(), size) <= aw) cur = nx;
      else { lines.push(cur.trim()); cur = w.trimStart(); }
    }
    if (cur.trim()) lines.push(cur.trim());
    const out = [];
    for (const l of lines) {
      if (tw(l, size) <= aw) { out.push(l); continue; }
      let c = "";
      for (const ch of l) { if (c && tw(c + ch, size) > aw) { out.push(c); c = ch; } else c += ch; }
      if (c) out.push(c);
    }
    return out;
  };
  const ansText = (t) => { const sz = pen.fit(t, 10.5, aw, false, 8); return tw(t, sz) <= aw + 0.5 ? { size: sz, lines: [t] } : { size: 8, lines: wrap(t, 8) }; };
  const embs = new Map();
  const emb = async (bytes) => { if (!embs.has(bytes)) embs.set(bytes, await ctx.doc.embedPng(bytes)); return embs.get(bytes); };
  for (let r0 = 0; r0 < entries.length; r0 += per) {
    const row = entries.slice(r0, r0 + per);
    const hs = row.filter((e) => e.answer_png && !isCirc(e)).map((e) => {
      const [w, h] = e.answer_wh || [40, 12];
      const s = Math.min(1.25, (cw - nw - 3 * MM) / Math.max(w, 1));
      return h * s + 3 * MM;
    });
    const ths = row.filter(isTxt).map((e) => { const a = ansText(String(e.answer)); return a.lines.length * a.size * 1.3 + 2.6 * MM; });
    const rh = Math.max(rowMin, ...hs, ...ths);
    if (y + rh > y1 - 6 * MM) { pen = newPage(); y = y0 + 8 * MM; }
    for (let i = 0; i < row.length; i++) {
      const e = row[i];
      const cx = inner0 + i * cw;
      pen.rect(cx, y, cx + cw, y + rh, { color: th.line, width: 0.6 });
      pen.rect(cx, y, cx + nw, y + rh, { color: th.line, fill: th.soft, width: 0.6 });
      const lab = String(e.label ?? e.seq);     // 문항 번호(시험지에 적힌 대로 — 1(1) · 1(2) 처럼 나뉜 문항)
      pen.text(cx + nw / 2, y + rh / 2 + 3.4, lab, { size: pen.fit(lab, 10, nw - 1.5, true, 6), bold: true, align: "center", color: th.dark });
      const ans = String(e.answer || "");
      const ax0 = cx + nw + 2 * MM;
      if (isCirc(e)) {
        const rr = 5.4, ccx = ax0 + 5.6, ccy = y + rh / 2;
        pen.circle(ccx, ccy, rr, { color: [0, 0, 0], width: 0.9 });
        pen.text(ccx, ccy + 3.2, ans, { size: 9, bold: true, align: "center" });
      } else if (e.answer_png) {
        const [w, h] = e.answer_wh || [40, 12];
        const s = Math.min(1.25, (cw - nw - 3 * MM) / Math.max(w, 1), (rh - 2 * MM) / Math.max(h, 1));
        pen.image(await emb(e.answer_png), ax0, y + (rh - h * s) / 2, ax0 + w * s, y + (rh + h * s) / 2);
      } else if (ans) {
        const a = ansText(ans), lh = a.size * 1.3;
        let ty = y + (rh - a.lines.length * lh) / 2 + a.size * 0.98;
        for (const l of a.lines) { pen.text(ax0, ty, l, { size: a.size }); ty += lh; }
      } else {
        pen.text(ax0, y + rh / 2 + 3.4, "-", { size: 10, color: th.gray });
      }
    }
    y += rh;
  }
  const sols = entries.filter((e) => e.sol);
  if (sols.length) {
    y += 7 * MM;
    if (y > y1 - 40 * MM) { pen = newPage(); y = y0 + 6 * MM; }
    pen.line(x0 + 6 * MM, y - 2 * MM, x1 - 6 * MM, y - 2 * MM, { color: th.line, width: 0.8 });
    pen.text(x0 + 6 * MM, y + 3.2 * MM, "해설", { size: 12, bold: true, color: th.elem ? th.acc : [0, 0, 0] });
    let colTop = y + 7 * MM;
    // 해설 단: 기본 2단. cfg.해설_단 = 1 이면 한 단(넓은 해설 그림 — 원래 한 줄 가득 쓴 해설을 줄이지 않고 싣기)
    const one = Number(cfg.해설_단) === 1;
    const colw = one ? x1 - x0 : (x1 - x0) / 2, pad = 4.5 * MM, gut = GEO.gutter;
    let side = 0, cy = colTop;
    const midLine = (p, topY) => {
      if (one) return;
      if (th.elem) p.line((x0 + x1) / 2, topY, (x0 + x1) / 2, y1 - 3 * MM, { color: th.line, width: 0.9, dashes: [3, 3] });
      else p.line((x0 + x1) / 2, topY, (x0 + x1) / 2, y1, { width: 0.9 });
    };
    midLine(pen, colTop - 2 * MM);
    const availW = colw - 2 * pad - gut;
    for (const e of sols) {
      const sol = e.sol;
      let s = Math.min(1, availW / Math.max(sol.w, 1));
      let h = sol.h * s;
      const maxH = y1 - (y0 + 6 * MM) - 6 * MM;
      if (h > maxH) { s *= maxH / h; h = maxH; }
      const need = h + 2 * MM;
      if (cy + need > y1 - 4 * MM) {
        if (side === 0 && !one) { side = 1; cy = colTop; }
        else { pen = newPage(); side = 0; colTop = y0 + 6 * MM; cy = colTop; midLine(pen, y0); }
      }
      const cx = x0 + side * colw + pad;
      const lab = String(e.label ?? e.seq);
      if (th.elem) {
        const rr = 3.1 * MM;
        const c = EL_DOTS[(e.seq - 1) % EL_DOTS.length];
        pen.circle(cx + rr, cy + rr + 0.6, rr, { color: null, fill: c });
        pen.text(cx + rr, cy + rr + 3.6, lab, { size: lab.length < 3 ? 9.6 : lab.length < 4 ? 8 : pen.fit(lab, 7, 2 * rr - 1, true, 5), bold: true, align: "center", color: [1, 1, 1] });
      } else pen.text(cx, cy + 10.2, `${lab}.`, { size: pen.fit(`${lab}.`, 11, gut - 1, true, 7), bold: true });   // 100. 이상 · 10-1 같은 번호도 번호 칸 안에
      pen.image(await emb(sol.png), cx + gut, cy, cx + gut + sol.w * s, cy + h);
      cy += need + 5 * MM;
    }
  }
  const n = pages.length;
  pages.forEach((p, i) => frame(p, th, cfg, title, i, n, i === 0, deco));
  // 번호를 못 찾은 쪽(그림으로 바꿔 이름을 지운 것)은 뒤에 그대로
  for (const pg of appendPages) {
    const page = ctx.doc.addPage([pg.w || A4W, pg.h || A4H]);
    const img = await ctx.doc.embedPng(pg.png);
    page.drawImage(img, { x: 0, y: 0, width: pg.w || A4W, height: pg.h || A4H });
  }
  return { pdf: await ctx.doc.save(), pages: ctx.doc.getPageCount(), n_sol: sols.length };
  });
}

// 여러 파일을 합친 원본 모양 정답해설 사이에 끼우는 안내 쪽
export async function dividerPage(ctx, lines) {
  const page = ctx.doc.addPage([A4W, A4H]);
  const pen = new Pen(ctx, page);
  let y = A4H * 0.4;
  for (const [t, size, bold] of lines) {
    pen.text(A4W / 2, y, t, { size: pen.fit(t, size, A4W - 40 * MM, bold), bold, align: "center" });
    y += size * 1.9;
  }
}
