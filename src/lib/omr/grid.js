// ashrain.out — 컨셉 문제 OMR: 숫자·분수·보기 칸 답안 카드(여러 쪽) — 배치 · 인쇄 SVG · 사진 판독 (순수 함수, DOM 없음 — node 테스트 가능)
//
// 주제별 50제는 답이 단답(정수 · 분수 · 보기 고르기 · 두 수)이라 ①~⑤ 카드(sheet.js)로는 받을 수 없다.
// 그래서 수능 주관식 칸처럼 자리마다 0~9 동그라미를 세로로 둔 「숫자 칸」을 문항마다 놓는다.
//   · 정수: 자리 수 = max(3, 답의 자리 수)        · 분수: 분자 칸 | 분모 칸 (각 max(2, 자리 수))
//   · 보기 고르기: ㄱ ㄴ ㄷ ㄹ (여러 개 칠해도 됨)  · 두 수(최솟값·최댓값 등): 정수 칸 두 개
//   자리 수는 세트 데이터의 omr.c 로 온다(답 자체는 카드에 없다).
//
// 캔버스 단위: 가로 1000 × 세로 1478 = 인쇄 184 × 272 mm (A4 − 여백 13·12·13·13 mm). 한 쪽은 SVG 하나.
// 판독은 sheet.js 카드와 같은 길을 쓴다 — detect.js 의 국소 이진화 → 네 모서리 마커 → 방향 막대 → 호모그래피 → 역매핑.
// 쪽마다 위쪽 마커 사이에 14칸 「쪽 코드 띠」가 있어 세트 번호 · 쪽 번호를 읽는다(사진을 어느 순서로 찍어도 된다).
// 원칙: 추측하지 않는다 — 애매한 칸은 "?"로 두고 낮은 conf 로 표시해 학생이 확인 화면에서 고친다.

import { toGray, threshold, findMarkers, orientCorners, warpToSpec, inkLevel } from "./detect.js";

export const GW = 1000;
export const GH = 1478;
export const CARD_MM_W = 184;
export const MM_PER_U = CARD_MM_W / GW;
export const MARKER_SIZE = 60;
export const MARKER_INSET = 50;
export const ORIENT = { x: 122, y: 50, w: 24, h: 60 };
export const BUB_R = 7.5;            // 동그라미 반지름 (≈ 지름 2.8 mm)
export const PX = 21;                // 자리(열) 간격 ≈ 3.9 mm
export const PY = 20.5;              // 숫자(행) 간격 ≈ 3.8 mm
export const BOX_H = 22;             // 손글씨 칸
export const LABEL_W = 27;           // 번호 칸
export const SEP_W = 15;             // 분자|분모 · 두 수 사이
export const PICK_DX = 30;           // 보기 동그라미 간격
export const BLOCK_H = BOX_H + 6 + 10 * PY + 16;   // 237 + 캡션 16
export const GAP_X = 10;
export const GAP_Y = 14;
export const AREA = { x0: 40, x1: 960, yFirst: 268, yOther: 168, yMax: 1352 };
export const BAND = { x0: 230, y: 66, cell: 22, gap: 14, n: 14 };
export const FILL_MIN = 0.3;         // 이 이상 채워졌으면 칠한 것 (빈 동그라미는 속 숫자 · 테두리 번짐까지 ≈ 0.05~0.15)
export const MARGIN = 0.18;          // 한 자리에서 1위·2위 차이가 이보다 작으면 "?"(두 개 칠함)
export const CONF_OK = 0.5;

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const mm = (v) => (v * MM_PER_U).toFixed(3) + "mm";

export function markerRects() {
  const i = MARKER_INSET, s = MARKER_SIZE;
  return [
    { x: i, y: i, size: s }, { x: GW - i - s, y: i, size: s },
    { x: GW - i - s, y: GH - i - s, size: s }, { x: i, y: GH - i - s, size: s },
  ];
}

// ── 쪽 코드 띠: [1][범주 2비트][세트 6비트][쪽 2비트][검사 2비트][1] ──────────────────────────
// 세트 칸은 6비트(1~63)다. 64번부터는 범주의 확장 코드(prob → 2)에 (세트 − 63)을 담는다 —
// 이미 인쇄한 1~63번 카드의 띠는 그대로이고, 한 범주에 126세트까지 담는다.
export const CAT_CODES = { prob: 1 };
export const CAT_EXT = { prob: 2 };
export const SET_MAX = 126;
export function bandBits(cat, set, page) {
  let c = CAT_CODES[cat] ?? 0, s = set;
  if (set > 63 && CAT_EXT[cat] != null) { c = CAT_EXT[cat]; s = set - 63; }
  if (!(s >= 1 && s <= 63) || !(page >= 0 && page <= 3)) throw new Error("쪽 코드 범위 밖");
  const data = [...[1, 0].map((b) => (c >> b) & 1), ...[5, 4, 3, 2, 1, 0].map((b) => (s >> b) & 1), ...[1, 0].map((b) => (page >> b) & 1)];
  const ones = data.reduce((a, b) => a + b, 0) % 4;
  return [1, ...data, (ones >> 1) & 1, ones & 1, 1];
}
export function parseBand(bits) {
  if (!Array.isArray(bits) || bits.length !== BAND.n || bits[0] !== 1 || bits[BAND.n - 1] !== 1) return null;
  const data = bits.slice(1, 11), chk = bits[11] * 2 + bits[12];
  if (data.reduce((a, b) => a + b, 0) % 4 !== chk) return null;
  const v = (arr) => arr.reduce((a, b) => a * 2 + b, 0);
  const catN = v(data.slice(0, 2)), s = v(data.slice(2, 8));
  let cat = Object.keys(CAT_CODES).find((k) => CAT_CODES[k] === catN) || null, set = s;
  if (!cat) {
    const ext = Object.keys(CAT_EXT).find((k) => CAT_EXT[k] === catN);
    if (ext) { cat = ext; set = s >= 1 ? s + 63 : 0; }
  }
  return { cat, set, page: v(data.slice(8, 10)) };
}
export function bandCells() {
  return Array.from({ length: BAND.n }, (_, i) => ({ x: BAND.x0 + i * (BAND.cell + BAND.gap), y: BAND.y, size: BAND.cell }));
}

// ── 문항 칸 ─────────────────────────────────────────────────────────────────────
/** 세트 문항(a · omr) → 칸 종류 */
export function kindOf(it) {
  const k = it?.a?.k;
  if (k === "pick") return { kind: "pick", opts: it.a.o || ["ㄱ", "ㄴ", "ㄷ", "ㄹ"] };
  if (k === "frac") return { kind: "frac", cols: (it.omr?.c || [2, 2]).slice(0, 2) };
  if (k === "pair") return { kind: "pair", cols: (it.omr?.c || [3, 3]).slice(0, 2), labels: it.omr?.l || it.a.l || ["", ""] };
  return { kind: "int", cols: [(it.omr?.c || [3])[0]] };
}

function blockWidth(b) {
  if (b.kind === "pick") return LABEL_W + b.opts.length * PICK_DX + 8;
  if (b.kind === "int") return LABEL_W + b.cols[0] * PX + 8;
  return LABEL_W + (b.cols[0] + b.cols[1]) * PX + SEP_W + 8;
}

/** 칸 하나의 동그라미 좌표 (캔버스 단위). grids: [{ x0, cols, label, bubbles: [[{x,y,d}]×10]×cols }] */
function placeBlock(b, x, y) {
  const gx = x + LABEL_W;
  const by0 = y + BOX_H + 6 + PY / 2;
  const grid = (x0, cols, label) => ({
    x0, cols, label,
    boxes: Array.from({ length: cols }, (_, c) => ({ x: x0 + c * PX, y, w: PX, h: BOX_H })),
    bubbles: Array.from({ length: cols }, (_, c) => Array.from({ length: 10 }, (_, d) => ({ x: x0 + c * PX + PX / 2, y: by0 + d * PY, d }))),
  });
  const out = { ...b, x, y, w: blockWidth(b), h: BLOCK_H, grids: [], picks: null };
  if (b.kind === "pick") {
    out.picks = b.opts.map((label, i) => ({ x: gx + i * PICK_DX + PICK_DX / 2, y: by0 + 2 * PY, label }));
  } else if (b.kind === "int") {
    out.grids.push(grid(gx, b.cols[0], ""));
  } else {
    out.grids.push(grid(gx, b.cols[0], b.kind === "frac" ? "분자" : b.labels[0]));
    out.grids.push(grid(gx + b.cols[0] * PX + SEP_W, b.cols[1], b.kind === "frac" ? "분모" : b.labels[1]));
  }
  return out;
}

/**
 * 카드 배치. set: { cat:"prob", no, title, short, items:[{ no, a, omr }] }
 * → { cat, set, title, pages:[{ index, n, W, H, markers, orient, band, blocks:[…] }] }
 */
export function layoutCard(set) {
  const blocks = (set.items || []).map((it, i) => ({ no: it.no ?? i + 1, ...kindOf(it) }));
  const pages = [];
  let page = null, x = 0, y = 0;
  const newPage = () => {
    page = { index: pages.length, blocks: [] };
    pages.push(page);
    x = AREA.x0; y = page.index === 0 ? AREA.yFirst : AREA.yOther;
  };
  newPage();
  for (const b of blocks) {
    const w = blockWidth(b);
    if (x + w > AREA.x1) { x = AREA.x0; y += BLOCK_H + GAP_Y; }
    if (y + BLOCK_H > AREA.yMax) newPage();
    page.blocks.push(placeBlock(b, x, y));
    x += w + GAP_X;
  }
  const n = pages.length;
  for (const p of pages) {
    Object.assign(p, { n, W: GW, H: GH, markers: markerRects(), orient: { ...ORIENT }, band: bandBits(set.cat || "prob", set.no, p.index) });
    // 같은 줄의 칸들을 가운데로 — 오른쪽 여백을 줄 양끝에 나눠 준다(보기 좋게, 좌표는 그대로 판독에 쓴다)
    const rows = {};
    for (const b of p.blocks) (rows[b.y] = rows[b.y] || []).push(b);
    for (const list of Object.values(rows)) {
      const right = Math.max(...list.map((b) => b.x + b.w));
      const shift = Math.max(0, (AREA.x1 - right) / 2);
      if (shift > 0.5) for (const b of list) shiftBlock(b, shift);
    }
  }
  return { cat: set.cat || "prob", set: set.no, title: set.title || "", short: set.short || "", pages };
}

function shiftBlock(b, dx) {
  b.x += dx;
  for (const g of b.grids) {
    g.x0 += dx;
    for (const bx of g.boxes) bx.x += dx;
    for (const col of g.bubbles) for (const bb of col) bb.x += dx;
  }
  if (b.picks) for (const p of b.picks) p.x += dx;
}

// ── 인쇄 SVG ───────────────────────────────────────────────────────────────────
export const INSTRUCTION = "숫자는 한 자리에 하나씩 동그라미를 진하게 칠해요 · 분수는 분자 칸과 분모 칸에 · 남는 자리는 비워 둬요";
export const PHOTO_TIP = "사진은 네 모서리의 검은 네모가 모두 나오게 위에서 찍어요";

export function pageSvg(card, p) {
  const s = [];
  for (const m of p.markers) s.push(`<rect x="${m.x}" y="${m.y}" width="${m.size}" height="${m.size}" fill="#000"/>`);
  const o = p.orient;
  s.push(`<rect x="${o.x}" y="${o.y}" width="${o.w}" height="${o.h}" fill="#000"/>`);
  bandCells().forEach((c, i) => {
    if (p.band[i]) s.push(`<rect x="${c.x}" y="${c.y}" width="${c.size}" height="${c.size}" fill="#000"/>`);
    else s.push(`<rect x="${c.x + 0.5}" y="${c.y + 0.5}" width="${c.size - 1}" height="${c.size - 1}" fill="none" stroke="#d6d6d6" stroke-width="1"/>`);
  });
  const pg = `${p.index + 1}/${p.n}쪽`;
  if (p.index === 0) {
    s.push(`<text x="500" y="158" text-anchor="middle" font-size="30" font-weight="800" fill="#111">${esc(card.title)}</text>`);
    s.push(`<text x="500" y="190" text-anchor="middle" font-size="17" fill="#444">OMR 답안 카드 · ${esc(pg)} · 중2-2 · 50제</text>`);
    s.push(`<text x="160" y="226" font-size="17" fill="#111">이름</text><line x1="203" y1="230" x2="460" y2="230" stroke="#333" stroke-width="1.4"/>`);
    s.push(`<text x="540" y="226" font-size="17" fill="#111">날짜</text><line x1="583" y1="230" x2="840" y2="230" stroke="#333" stroke-width="1.4"/>`);
    s.push(`<text x="500" y="254" text-anchor="middle" font-size="13.5" fill="#333">${esc(INSTRUCTION)}</text>`);
  } else {
    s.push(`<text x="500" y="150" text-anchor="middle" font-size="20" font-weight="800" fill="#111">${esc(card.title)} <tspan font-weight="500" font-size="16" fill="#444">· OMR ${esc(pg)}</tspan></text>`);
  }
  for (const b of p.blocks) {
    s.push(`<text x="${b.x + 2}" y="${b.y + 17}" font-size="17" font-weight="800" fill="#111">${b.no}</text>`);
    if (b.kind === "pick") {
      s.push(`<text x="${b.x + LABEL_W}" y="${b.y + 16}" font-size="12" fill="#666">맞는 것을 모두 칠해요</text>`);
      for (const q of b.picks) {
        s.push(`<circle cx="${q.x}" cy="${q.y}" r="${BUB_R + 3}" fill="none" stroke="#333" stroke-width="1.3"/>`);
        s.push(`<text x="${q.x}" y="${q.y + 5}" text-anchor="middle" font-size="13" fill="#aaa">${esc(q.label)}</text>`);
      }
      continue;
    }
    b.grids.forEach((g, gi) => {
      for (const bx of g.boxes) s.push(`<rect x="${bx.x}" y="${bx.y}" width="${bx.w}" height="${bx.h}" fill="none" stroke="#555" stroke-width="1.1"/>`);
      for (const col of g.bubbles) for (const bb of col) {
        s.push(`<circle cx="${bb.x}" cy="${bb.y}" r="${BUB_R}" fill="none" stroke="#444" stroke-width="1.1"/>`);
        s.push(`<text x="${bb.x}" y="${bb.y + 3.6}" text-anchor="middle" font-size="10" fill="#b4b4b4">${bb.d}</text>`);
      }
      const capY = b.y + BOX_H + 6 + 10 * PY + 12;
      if (g.label) s.push(`<text x="${g.x0 + (g.cols * PX) / 2}" y="${capY}" text-anchor="middle" font-size="11.5" fill="#555">${esc(g.label)}</text>`);
      if (gi === 1) {
        const sx = g.x0 - SEP_W / 2;
        s.push(`<text x="${sx}" y="${b.y + 17}" text-anchor="middle" font-size="17" fill="#333">${b.kind === "frac" ? "/" : ","}</text>`);
        s.push(`<line x1="${sx}" y1="${b.y + BOX_H + 8}" x2="${sx}" y2="${b.y + BOX_H + 4 + 10 * PY}" stroke="#bbb" stroke-width="1" stroke-dasharray="3 3"/>`);
      }
    });
  }
  s.push(`<text x="500" y="${GH - 70}" text-anchor="middle" font-size="12" fill="#888">${esc(PHOTO_TIP)}</text>`);
  return `<svg class="omr-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${GW} ${GH}" width="${mm(GW)}" height="${mm(GH)}" `
    + `font-family="'Pretendard Variable',Pretendard,'Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif">${s.join("")}</svg>`;
}

/** 인쇄용 HTML 조각 (전체 문서는 부르는 쪽이 감싼다). 쪽마다 한 장. */
export const CARD_CSS = `.omr-pg{width:${mm(GW)};height:${mm(GH)};margin:0;padding:0;background:#fff;overflow:hidden;break-after:page;page-break-after:always}
.omr-pg:last-child{break-after:auto;page-break-after:auto}.omr-pg svg{display:block}`;
export function cardHtml(card) {
  return `<style>${CARD_CSS}</style>` + card.pages.map((p) => `<div class="omr-pg" data-page="${p.index + 1}">${pageSvg(card, p)}</div>`).join("");
}

// ── 판독 ───────────────────────────────────────────────────────────────────────
function meanDisk(g, W, H, cx, cy, r) {
  let s = 0, n = 0;
  const r2 = r * r;
  for (let y = Math.max(0, Math.floor(cy - r)); y <= Math.min(H - 1, Math.ceil(cy + r)); y++)
    for (let x = Math.max(0, Math.floor(cx - r)); x <= Math.min(W - 1, Math.ceil(cx + r)); x++) {
      const dx = x + 0.5 - cx, dy = y + 0.5 - cy;
      if (dx * dx + dy * dy <= r2) { s += g[y * W + x]; n++; }
    }
  return n ? s / n : 255;
}
function ringBg(g, W, H, cx, cy, r0, r1) {
  const vals = [];
  const a = r0 * r0, b = r1 * r1;
  for (let y = Math.max(0, Math.floor(cy - r1)); y <= Math.min(H - 1, Math.ceil(cy + r1)); y++)
    for (let x = Math.max(0, Math.floor(cx - r1)); x <= Math.min(W - 1, Math.ceil(cx + r1)); x++) {
      const dx = x + 0.5 - cx, dy = y + 0.5 - cy, d = dx * dx + dy * dy;
      if (d >= a && d <= b) vals.push(g[y * W + x]);
    }
  if (!vals.length) return 255;
  vals.sort((p, q) => p - q);
  return vals[Math.min(vals.length - 1, Math.floor(vals.length * 0.8))];   // 이웃 동그라미 테두리 · 번진 연필은 버리고 종이 밝기
}
function meanRect(g, W, H, x, y, w, h) {
  let s = 0, n = 0;
  for (let j = Math.max(0, Math.floor(y)); j < Math.min(H, Math.ceil(y + h)); j++)
    for (let i = Math.max(0, Math.floor(x)); i < Math.min(W, Math.ceil(x + w)); i++) { s += g[j * W + i]; n++; }
  return n ? s / n : 255;
}

/** 동그라미 하나의 채움 비율 (0~1) — 안쪽 어둡기를 그 둘레 종이 밝기와 잉크 밝기 사이에서 잰다 */
function fillAt(wp, x, y, r, ink) {
  const { gray: g, width: W, height: H, scale: sc } = wp;
  const inside = meanDisk(g, W, H, x * sc, y * sc, r * sc * 0.62);
  const bg = ringBg(g, W, H, x * sc, y * sc, r * sc * 1.25, r * sc * 1.9);
  return clamp01((bg - inside) / Math.max(bg - ink, 40));
}

/** 띠 14칸 읽기 — 양 끝 칸(늘 검정)과 칸 사이 종이로 기준을 잡는다 */
export function readBand(wp) {
  const { gray: g, width: W, height: H, scale: sc } = wp;
  const cells = bandCells().map((c) => meanRect(g, W, H, (c.x + 4) * sc, (c.y + 4) * sc, (c.size - 8) * sc, (c.size - 8) * sc));
  const paper = meanRect(g, W, H, (BAND.x0 + BAND.cell + 2) * sc, (BAND.y + 4) * sc, (BAND.gap - 4) * sc, (BAND.cell - 8) * sc);
  const black = (cells[0] + cells[BAND.n - 1]) / 2;
  if (paper - black < 40) return { bits: null, contrast: paper - black };
  const mid = (paper + black) / 2;
  const bits = cells.map((v) => (v < mid ? 1 : 0));
  return { bits, contrast: paper - black, info: parseBand(bits) };
}

function readGrid(wp, grid, ink) {
  const digits = [], confs = [], flags = [];
  for (const col of grid.bubbles) {
    const fills = col.map((b) => fillAt(wp, b.x, b.y, BUB_R, ink));
    const order = fills.map((f, i) => i).sort((p, q) => fills[q] - fills[p]);
    const max = fills[order[0]], second = fills[order[1]];
    if (max < FILL_MIN) { digits.push(""); confs.push(clamp01((FILL_MIN - max) / FILL_MIN)); flags.push(null); continue; }
    if (second >= FILL_MIN && max - second < MARGIN) { digits.push("?"); confs.push(0); flags.push("double"); continue; }
    digits.push(String(order[0]));
    confs.push(clamp01(Math.min((max - FILL_MIN) / 0.2, (max - second) / (2 * MARGIN))));
    flags.push(second >= FILL_MIN ? "weak" : null);
  }
  // 앞뒤 빈자리는 버리고, 숫자 사이에 빈자리가 끼면 "?" (어느 자리인지 모른다)
  let a = 0, b = digits.length;
  while (a < b && digits[a] === "") a++;
  while (b > a && digits[b - 1] === "") b--;
  const mid = digits.slice(a, b);
  const gap = mid.includes("");
  const text = gap ? mid.map((d) => d || "?").join("") : mid.join("");
  const conf = confs.length ? Math.min(...confs) : 0;
  return { text, conf: gap ? Math.min(conf, 0.2) : conf, flag: gap ? "gap" : flags.find(Boolean) || null };
}

/** 칸 하나 → { no, raw(학생이 쓴 꼴: "12" · "5/12" · "ㄱ, ㄷ" · "14, 21"), conf, flag } */
export function readBlock(wp, b, ink) {
  if (b.kind === "pick") {
    const fills = b.picks.map((q) => fillAt(wp, q.x, q.y, BUB_R + 3, ink));
    const on = b.picks.filter((q, i) => fills[i] >= FILL_MIN).map((q) => q.label);
    const unsure = fills.some((f) => f >= FILL_MIN * 0.6 && f < FILL_MIN * 1.3);
    return { no: b.no, kind: b.kind, raw: on.join(", "), conf: unsure ? 0.4 : 0.9, flag: unsure ? "weak" : null };
  }
  const parts = b.grids.map((g) => readGrid(wp, g, ink));
  const conf = Math.min(...parts.map((p) => p.conf));
  const flag = parts.map((p) => p.flag).find(Boolean) || null;
  let raw;
  if (b.kind === "int") raw = parts[0].text;
  else if (b.kind === "frac") raw = parts[1].text ? `${parts[0].text}/${parts[1].text}` : parts[0].text;
  else raw = parts.every((p) => p.text) ? `${parts[0].text}, ${parts[1].text}` : parts.map((p) => p.text).join(", ").replace(/^, |, $/g, "");
  return { no: b.no, kind: b.kind, raw, conf: Math.round(conf * 100) / 100, flag };
}

/**
 * 사진 한 장 → { ok, reason?, page, set, cat, answers:[{no, kind, raw, conf, flag}], corners }
 * card: layoutCard 결과. 띠를 못 읽으면 opts.page(0부터)로 읽는다.
 */
export function readCardPhoto(img, card, opts = {}) {
  const w = img.width, h = img.height;
  const gray = toGray(img);
  const bin = threshold(gray, w, h, opts.threshold);
  const fail = (reason, extra = {}) => ({ ok: false, reason, page: null, answers: [], ...extra });
  const quad = findMarkers(bin, w, h, opts);
  if (!quad) return fail("markers");
  const spec0 = card.pages[0];
  const o = orientCorners(gray, w, h, quad, spec0);
  if (!o) return fail("orient", { corners: quad });
  const scale = opts.scale || 1;
  const wp = warpToSpec(gray, w, h, o.corners, spec0, scale);
  if (!wp) return fail("warp", { corners: o.corners });
  const band = readBand(wp);
  let pageIdx = band.info ? band.info.page : opts.page ?? null;
  if (band.info && (band.info.set !== card.set || (band.info.cat && band.info.cat !== card.cat))) {
    return fail("other-set", { band: band.info, corners: o.corners });
  }
  if (pageIdx == null || !card.pages[pageIdx]) return fail("band", { corners: o.corners, band: band.bits });
  const p = card.pages[pageIdx];
  const ink = inkLevel(wp, p);
  const answers = p.blocks.map((b) => readBlock(wp, b, ink));
  return { ok: true, reason: null, page: pageIdx, set: card.set, cat: card.cat, answers, corners: o.corners, bandOk: !!band.info, warped: wp };
}
