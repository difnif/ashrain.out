// ashrain.out — 사진 OMR: 답안 카드 레이아웃 + 인쇄용 HTML (순수 함수, DOM 없음 — node 테스트 가능)
//
// 캔버스 단위: 가로 1000 × 세로 1414 (A4 비율). 인쇄 시 카드 폭 190mm(A4 210 − 여백 10×2)에 맞춰 같은 비율로 축소되므로
// 실물 카드의 모든 점은 이 좌표계와 비례한다 → detect.js 는 네 모서리 마커 중심을 이 좌표계로 사영(호모그래피)해 읽는다.
//
// 카드 구성
//   · 네 모서리 검은 정사각형 마커(60, 안쪽 여백 50) — 검출 기준점
//   · TL 마커 오른쪽의 세로 막대(ORIENT) — 카드가 어느 방향으로 찍혔는지(0/90/180/270°) 판별용
//   · 상단: 세트 코드(크게) · 제목 · 안내문 · 이름/날짜 줄
//   · 행: 번호 + ①~⑤ 버블(객관식) 또는 빈 답칸(단답). 15문항까지 1열, 16~30문항은 2열(1~15 왼쪽, 16~30 오른쪽)

import { renderHtml, MATH_CSS } from "../mathir.js";
import { figureToHtml1 } from "../figsvg.js";

export const SHEET_W = 1000;
export const SHEET_H = 1414;
export const MARKER_SIZE = 60;
export const MARKER_INSET = 50;
export const BUBBLE_R = 17;
export const ROW_Y0 = 350;          // 첫 행 중심 y
export const ROW_PITCH = 60;        // 행 간격
export const ROWS_PER_COL = 15;
export const MAX_ITEMS = 30;
export const LABELS = ["①", "②", "③", "④", "⑤"];
export const CARD_MM_W = 190;       // 인쇄 카드 폭(mm)
export const MM_PER_PX = CARD_MM_W / SHEET_W;
/** 방향 표시 막대 — TL 마커 오른쪽 (x 122~146, y 50~110). 180° 대칭 위치(BR 마커 왼쪽)는 비워 둔다. */
export const ORIENT = { x: 122, y: 50, w: 24, h: 60 };

// 열 배치 — 1열(≤15) / 2열(>15)
const COL1 = { numX: 300, x0: 380, dx: 80 };
const COL2 = [{ numX: 85, x0: 150, dx: 68 }, { numX: 505, x0: 570, dx: 68 }];
const BOX_H = 44;

/** 마커 4개 (TL, TR, BR, BL) — 왼쪽 위 좌표 + 크기 */
export function markerRects() {
  const i = MARKER_INSET, s = MARKER_SIZE, W = SHEET_W, H = SHEET_H;
  return [
    { x: i, y: i, size: s },
    { x: W - i - s, y: i, size: s },
    { x: W - i - s, y: H - i - s, size: s },
    { x: i, y: H - i - s, size: s },
  ];
}

/** 마커 중심 좌표 [[x,y]×4] (TL, TR, BR, BL) — 호모그래피 대응점 */
export function markerCenters(spec) {
  return (spec?.markers || markerRects()).map((m) => [m.x + m.size / 2, m.y + m.size / 2]);
}

/**
 * 레이아웃 계산.
 * items: [{ no, kind: "choice"|"short" }] (no 는 1부터, 없으면 순서대로 부여) — 최대 30개
 * → { W, H, markers, orient, rows, cols, header, meta:{code, n} }
 */
export function layoutSheet({ code = "", items = [] } = {}) {
  const list = (items || []).slice(0, MAX_ITEMS);
  const n = list.length;
  const cols = n > ROWS_PER_COL ? 2 : 1;
  const rows = list.map((it, i) => {
    const no = Number.isFinite(+it?.no) ? +it.no : i + 1;
    const kind = it?.kind === "short" ? "short" : "choice";
    const col = cols === 2 ? Math.floor(i / ROWS_PER_COL) : 0;
    const ri = cols === 2 ? i % ROWS_PER_COL : i;
    const g = cols === 2 ? COL2[col] : COL1;
    const y = ROW_Y0 + ri * ROW_PITCH;
    const xs = LABELS.map((_, k) => g.x0 + k * g.dx);
    const row = { no, kind, col, y, numX: g.numX, bubbles: null, blankBox: null };
    if (kind === "choice") row.bubbles = xs.map((x, k) => ({ x, y, r: BUBBLE_R, label: LABELS[k] }));
    else row.blankBox = { x: xs[0] - BUBBLE_R - 4, y: y - BOX_H / 2, w: xs[4] - xs[0] + 2 * BUBBLE_R + 8, h: BOX_H };
    return row;
  });
  return {
    W: SHEET_W, H: SHEET_H,
    markers: markerRects(),
    orient: { ...ORIENT },
    rows, cols,
    header: { codeY: 150, titleY: 208, subY: 238, instrY: 270, nameY: 304, dividerX: cols === 2 ? 497 : null },
    meta: { code: String(code || ""), n },
  };
}

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const mm = (v) => (v * MM_PER_PX).toFixed(3) + "mm";

export const INSTRUCTION = "보기 번호를 진하게 칠하세요 · 카드 네 모서리의 검은 네모가 모두 사진에 나오게 찍어요";

/**
 * 답안 카드 인쇄용 HTML 조각 (전체 문서는 페이지가 감싼다).
 * 카드 본체는 viewBox 0 0 1000 1414 의 SVG 하나 — 마커·버블이 배경색이 아닌 "내용"이므로 브라우저 인쇄 옵션과 무관하게 찍힌다.
 */
export function sheetHtml(spec, { title = "", subtitle = "" } = {}) {
  const s = spec || layoutSheet({});
  const parts = [];
  // 마커
  for (const m of s.markers) parts.push(`<rect class="mk" x="${m.x}" y="${m.y}" width="${m.size}" height="${m.size}" fill="#000"/>`);
  const o = s.orient;
  parts.push(`<rect class="or" x="${o.x}" y="${o.y}" width="${o.w}" height="${o.h}" fill="#000"/>`);
  // 머리
  const h = s.header;
  parts.push(`<text x="500" y="${h.codeY}" text-anchor="middle" font-size="64" font-weight="800" letter-spacing="6" fill="#000">${esc(s.meta.code)}</text>`);
  if (title) parts.push(`<text x="500" y="${h.titleY}" text-anchor="middle" font-size="26" font-weight="700" fill="#111">${esc(title)}</text>`);
  if (subtitle) parts.push(`<text x="500" y="${h.subY}" text-anchor="middle" font-size="18" fill="#555">${esc(subtitle)}</text>`);
  parts.push(`<text x="500" y="${h.instrY}" text-anchor="middle" font-size="17" fill="#333">${esc(INSTRUCTION)}</text>`);
  const ny = h.nameY;
  parts.push(`<text x="170" y="${ny}" font-size="18" fill="#111">이름</text><line x1="215" y1="${ny + 4}" x2="470" y2="${ny + 4}" stroke="#333" stroke-width="1.5"/>`);
  parts.push(`<text x="540" y="${ny}" font-size="18" fill="#111">날짜</text><line x1="585" y1="${ny + 4}" x2="830" y2="${ny + 4}" stroke="#333" stroke-width="1.5"/>`);
  if (h.dividerX) {
    const y1 = ROW_Y0 - ROW_PITCH / 2, y2 = ROW_Y0 + (ROWS_PER_COL - 0.5) * ROW_PITCH;
    parts.push(`<line x1="${h.dividerX}" y1="${y1}" x2="${h.dividerX}" y2="${y2}" stroke="#bbb" stroke-width="1.5"/>`);
  }
  // 행
  for (const r of s.rows) {
    parts.push(`<text x="${r.numX}" y="${r.y + 8}" text-anchor="end" font-size="22" font-weight="700" fill="#111">${r.no}</text>`);
    if (r.bubbles) {
      for (const b of r.bubbles) {
        parts.push(`<circle cx="${b.x}" cy="${b.y}" r="${b.r}" fill="none" stroke="#333" stroke-width="1.6"/>`);
        parts.push(`<text x="${b.x}" y="${b.y + 6}" text-anchor="middle" font-size="17" fill="#c4c4c4">${b.label}</text>`);
      }
    } else if (r.blankBox) {
      const b = r.blankBox;
      parts.push(`<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="5" fill="none" stroke="#333" stroke-width="1.6"/>`);
      parts.push(`<text x="${b.x + 8}" y="${b.y + b.h - 8}" font-size="12" fill="#bbb">답</text>`);
    }
  }
  const svg = `<svg class="om-card-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${s.W} ${s.H}" width="${mm(s.W)}" height="${mm(s.H)}" font-family="'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',sans-serif">${parts.join("")}</svg>`;
  return `<style>
@page { size: A4; margin: 10mm; }
.om-card { width: ${mm(s.W)}; height: ${mm(s.H)}; margin: 0; padding: 0; background: #fff; color: #111; overflow: hidden; page-break-inside: avoid; break-inside: avoid; }
.om-card svg { display: block; }
</style>
<div class="om-card" data-code="${esc(s.meta.code)}">${svg}</div>`;
}

const snippetHtml = (q) => renderHtml(String(q ?? ""));

function figHtml(figure, width) {
  if (!Array.isArray(figure) || !figure.length) return "";
  let html = "";
  for (const fg of figure) {
    try { html += figureToHtml1(fg, { width }).html || ""; } catch { /* 그릴 수 없는 도형은 침묵 */ }
  }
  return html ? `<div class="fig-stage">${html}</div>` : "";
}

/**
 * 시험지 인쇄용 HTML 조각 — 번호 · 문제 · 도형 · 보기(①~⑤ 인라인). A4 2단, 문항 안에서는 쪽 나눔 금지.
 * items: test_items 행 (question, figure, choices, qtype) — 순서 = 카드 번호
 */
export function testHtml({ title = "", subtitle = "", items = [], spec = null } = {}) {
  const code = spec?.meta?.code || "";
  const body = (items || []).map((it, i) => {
    const no = spec?.rows?.[i]?.no ?? i + 1;
    const isChoice = (spec?.rows?.[i]?.kind || (Array.isArray(it?.choices) && it.choices.length >= 2 ? "choice" : "short")) === "choice";
    const ch = isChoice && Array.isArray(it?.choices)
      ? `<div class="ch">${it.choices.slice(0, 5).map((c, k) => `<span><b>${LABELS[k]}</b> ${renderHtml(String(c ?? ""))}</span>`).join("")}</div>`
      : `<div class="ans">답: <span class="ln"></span></div>`;
    return `<div class="om-it"><div class="hd"><span class="no">${no}</span>${it?.points ? `<span class="pt">[${esc(it.points)}점]</span>` : ""}</div>` +
      `<div class="q">${snippetHtml(it?.question)}</div>${figHtml(it?.figure, 230)}${ch}</div>`;
  }).join("");
  return `<style>
@page { size: A4; margin: 10mm; }
${MATH_CSS}
.om-test { font-family: 'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',sans-serif; color: #111; font-size: 10.5pt; line-height: 1.55; }
.om-test .th { display: flex; align-items: baseline; justify-content: space-between; gap: 6mm; border-bottom: 0.5mm solid #111; padding-bottom: 2mm; margin-bottom: 4mm; }
.om-test .th h1 { font-size: 15pt; margin: 0; }
.om-test .th .sb { font-size: 9.5pt; color: #444; }
.om-test .th .cd { font-size: 12pt; font-weight: 800; letter-spacing: 1px; }
.om-test .nm { font-size: 9.5pt; color: #333; margin: 0 0 4mm; }
.om-test .cols { column-count: 2; column-gap: 8mm; column-rule: 0.2mm solid #ccc; }
.om-it { break-inside: avoid; page-break-inside: avoid; margin: 0 0 5mm; padding: 0 0 2.5mm; border-bottom: 0.2mm dashed #ddd; }
.om-it .hd { display: flex; align-items: center; gap: 2mm; margin-bottom: 1mm; }
.om-it .no { display: inline-flex; align-items: center; justify-content: center; min-width: 6mm; height: 6mm; padding: 0 1.5mm; border-radius: 3mm; background: #111; color: #fff; font-weight: 800; font-size: 9.5pt; }
.om-it .pt { font-size: 9pt; color: #555; }
.om-it .q { white-space: pre-wrap; word-break: keep-all; }
.om-it .ch { display: flex; flex-wrap: wrap; gap: 1.5mm 6mm; margin-top: 1.5mm; }
.om-it .ch span { white-space: nowrap; }
.om-it .ans { margin-top: 2mm; color: #333; }
.om-it .ans .ln { display: inline-block; width: 40mm; border-bottom: 0.3mm solid #333; vertical-align: baseline; }
.om-it .fig-stage { margin: 2mm 0; padding: 1.5mm; border: 0.2mm solid #e0ddd4; border-radius: 2mm; background: #fcfcfb; }
.om-it .fig-stage svg { max-width: 100%; height: auto; display: block; margin: 0 auto; }
</style>
<div class="om-test">
  <div class="th"><h1>${esc(title || "시험지")}</h1><span class="sb">${esc(subtitle)}</span>${code ? `<span class="cd">${esc(code)}</span>` : ""}</div>
  <p class="nm">이름: ____________ &nbsp;&nbsp; 날짜: ____________ &nbsp;&nbsp; 답은 <b>답안 카드</b>에 표시해요 (객관식은 보기 번호를 진하게, 단답은 답칸에 또박또박).</p>
  <div class="cols">${body}</div>
</div>`;
}

/** 시험지 + 답안 카드(마지막 쪽) 한 문서 */
export function packetHtml({ title, subtitle, items, spec }) {
  return testHtml({ title, subtitle, items, spec }) +
    `<div style="page-break-before:always;break-before:page"></div>` +
    sheetHtml(spec, { title, subtitle });
}
