// ashrain.out — 컨셉 문제 OMR: 숫자 · 보기 칸 + 분수 손글씨 칸 답안 카드(여러 쪽) — 배치 · 인쇄 SVG · 사진 판독 (순수 함수, DOM 없음 — node 테스트 가능)
//
// 주제별 50제는 답이 단답(정수 · 분수 · 보기 고르기 · 두 수)이라 ①~⑤ 카드(sheet.js)로는 받을 수 없다.
// 그래서 수능 주관식 칸처럼 자리마다 0~9 동그라미를 세로로 둔 「숫자 칸」을 문항마다 놓는다.
//   · 정수: 자리 수 = max(3, 답의 자리 수)        · 두 수(최솟값 · 최댓값 등): 정수 칸 두 개
//   · 보기 고르기: ㄱ ㄴ ㄷ ㄹ (여러 개 칠해도 됨)
//   · 분수: 카드 v2 부터는 「손글씨 칸」 — 위 칸에 분자, 아래 칸에 분모를 손으로 쓴다(0 · 1 은 위 칸에만).
//     판독은 칸에 글씨가 있는지만 기기 안에서 보고, 글씨는 그 칸만 잘라 AI(/api/ai task "omr")가 읽는다(OmrGrade).
//   자리 수는 세트 데이터의 omr.c 로 온다(답 자체는 카드에 없다).
//
// 카드 판(版) — 이미 인쇄한 카드도 읽도록 둘 다 안다.
//   v1 (2026-10): 작은 동그라미(지름 ≈ 2.8 mm) · 분수도 동그라미 · 2쪽. 쪽 코드 띠가 위쪽 마커 사이에 있다.
//   v2 (지금 인쇄): 동그라미 지름 ≈ 3.7 mm · 간격 넉넉히 · 글씨 진하게 · 분수는 손글씨 칸 · 3쪽 안팎.
//       쪽 코드 띠가 아래쪽 마커 사이로 옮겨 간다 — 띠가 어느 자리에서 읽히느냐로 판을 가린다(한 칸 오독으로 판이 바뀌지 않는다).
//       v2 카드의 위쪽 띠 자리는 비워 둔다(예전 띠로 잘못 읽히지 않게).
//
// 캔버스 단위: 가로 1000 × 세로 1478 = 인쇄 184 × 272 mm (A4 − 여백 13·12·13·13 mm). 한 쪽은 SVG 하나.
// 판독은 sheet.js 카드와 같은 길을 쓴다 — detect.js 의 국소 이진화 → 네 모서리 마커 → 방향 막대 → 호모그래피 → 역매핑.
// 띠의 14칸에 세트 번호 · 쪽 번호가 있어 사진을 어느 순서로 찍어도 된다.
// 원칙: 추측하지 않는다 — 애매한 칸은 "?"로 두고 낮은 conf 로 표시해 학생이 확인 화면에서 고친다.

import { toGray, threshold, findMarkers, orientCorners, warpToSpec, inkLevel } from "./detect.js";

export const GW = 1000;
export const GH = 1478;
export const CARD_MM_W = 184;
export const MM_PER_U = CARD_MM_W / GW;
export const MARKER_SIZE = 60;
export const MARKER_INSET = 50;
export const ORIENT = { x: 122, y: 50, w: 24, h: 60 };
export const OMR_VER = 2;            // 지금 인쇄하는 카드 판

// ── v1 치수 (예전 카드 — 읽기만) ────────────────────────────────────────────────
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
export const BAND = { x0: 230, y: 66, cell: 22, gap: 14, n: 14 };     // v1 띠: 위쪽 마커 사이

// ── v2 치수 (지금 인쇄) ────────────────────────────────────────────────────────
export const V2 = {
  BUB_R: 10,          // 지름 20 = 3.7 mm
  PX: 28,             // 열 간격 5.2 mm
  PY: 27,             // 행 간격 5.0 mm
  HEAD: 26,           // 번호 줄
  BOX_H: 30,          // 숫자 써 두는 칸
  BOX_GAP: 8,
  FOOT: 6,
  PAD: 4,             // 칸 좌우 안쪽 여백
  SEP_W: 20,          // 두 수 사이
  PICK_R: 13,         // 보기 동그라미
  PICK_DX: 36,
  FRAC_W: 124,        // 분수 손글씨 칸 22.8 mm
  FRAC_BOX_H: 124,    // 칸 하나 높이 22.8 mm
  FRAC_BAR: 30,       // 분자 칸과 분모 칸 사이(분수 막대)
  GAP_X: 16,          // 칸 사이 최소 · 최대(줄마다 고르게 벌린다)
  GAP_MAX: 52,
  ROW_MAX: 6,         // 한 줄에 칸 6개까지
  ROWS: 3,            // 한 쪽에 3줄
  AREA: { x0: 40, x1: 960, yFirst: 284, yOther: 208, yMax: 1352 },
  GAP_Y: { first: 12, other: 40 },
};
V2.BLOCK_H = V2.HEAD + V2.BOX_H + V2.BOX_GAP + 10 * V2.PY + V2.FOOT;    // 340
export const BAND2 = { x0: 230, y: GH - MARKER_INSET - MARKER_SIZE / 2 - 11, cell: 22, gap: 14, n: 14 };   // v2 띠: 아래쪽 마커 사이

// v2 일차함수(lin) 카드 — 답이 음수 · 분수 · 소수 · 식(y = ax + b) · 점이라 동그라미 대신 손글씨 한 줄 칸, 보기만 동그라미.
//   줄 높이가 낮아 2쪽(쪽마다 9줄)에 들어간다. 칸 폭은 답 꼴마다(수 < 점 < 식), 식 칸 앞에는 「y =」를 칸 밖에 인쇄한다.
export const LINE = {
  HEAD: 24, BOX_H: 76, FOOT: 6, PAD: 4, PRE: 36,
  W: { num: 196, pt: 236, lin: 300 },
  PICK_DX: 36, PICK_R: 13,
  GAP_X: 18, GAP_MAX: 64, GAP_Y: 14, ROW_MAX: 5,
  AREA: { x0: 40, x1: 960, yFirst: 284, yOther: 208, yMax: 1352 },
};
LINE.ROW_H = LINE.HEAD + LINE.BOX_H + LINE.FOOT;   // 106

export const FILL_MIN = 0.3;         // 이 이상 채워졌으면 칠한 것 (빈 동그라미의 속 숫자 · 테두리 번짐은 열마다 바탕으로 빼고 잰다)
export const MARGIN = 0.18;          // 한 자리에서 1위·2위 차이가 이보다 작으면 "?"(두 개 칠함)
export const FAINT_MIN = 0.16;       // FILL_MIN 아래라도 이만큼 칠했고 다른 동그라미보다 FAINT_GAP 넘게 어두우면 「흐리게 칠함」으로 읽는다
export const FAINT_GAP = 0.12;
export const CONF_OK = 0.5;
export const HAND_INSET = 7;         // 손글씨 칸 테두리에서 이만큼 안쪽만 본다(사진 어긋남 · 테두리 번짐)

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const mm = (v) => (v * MM_PER_U).toFixed(3) + "mm";
const median = (arr) => { const a = arr.slice().sort((x, y) => x - y); const m = a.length >> 1; return a.length ? (a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2) : 0; };

export function markerRects() {
  const i = MARKER_INSET, s = MARKER_SIZE;
  return [
    { x: i, y: i, size: s }, { x: GW - i - s, y: i, size: s },
    { x: GW - i - s, y: GH - i - s, size: s }, { x: i, y: GH - i - s, size: s },
  ];
}

// ── 쪽 코드 띠: [1][범주 2비트][세트 6비트][쪽 2비트][검사 2비트][1] ──────────────────────────
// 세트 칸은 6비트(1~63)다. 64번부터는 범주의 확장 코드(prob → 2)에 (세트 − 63)을 담는다 —
// 이미 인쇄한 1~63번 카드의 띠는 그대로이고, 한 범주에 126세트까지 담는다. 판(v1 · v2)은 띠의 자리로 가린다(위 · 아래).
export const CAT_CODES = { prob: 1, lin: 3 };
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
/** 띠 칸 자리 — pos: BAND(v1, 위) · BAND2(v2, 아래) */
export function bandCells(pos = BAND) {
  return Array.from({ length: pos.n }, (_, i) => ({ x: pos.x0 + i * (pos.cell + pos.gap), y: pos.y, size: pos.cell }));
}
export const bandPosOf = (ver) => (ver === 1 ? BAND : BAND2);

// ── 문항 칸 ─────────────────────────────────────────────────────────────────────
/** 세트 문항(a · omr) → 칸 종류 */
export function kindOf(it) {
  const k = it?.a?.k;
  if (k === "pick") return { kind: "pick", opts: it.a.o || ["ㄱ", "ㄴ", "ㄷ", "ㄹ"] };
  if (k === "frac") return { kind: "frac", cols: (it.omr?.c || [2, 2]).slice(0, 2) };
  if (k === "pair") return { kind: "pair", cols: (it.omr?.c || [3, 3]).slice(0, 2), labels: it.omr?.l || it.a.l || ["", ""] };
  if (k === "num" || k === "lin" || k === "pt") return { kind: "line", ak: k };     // 일차함수: 손글씨 한 줄 칸(수 · 식 · 점)
  return { kind: "int", cols: [(it.omr?.c || [3])[0]] };
}

// v1 — 예전 카드의 좌표를 그대로 다시 만든다(인쇄한 카드를 읽으려면 한 점도 달라지면 안 된다)
function blockWidthV1(b) {
  if (b.kind === "pick") return LABEL_W + b.opts.length * PICK_DX + 8;
  if (b.kind === "int") return LABEL_W + b.cols[0] * PX + 8;
  return LABEL_W + (b.cols[0] + b.cols[1]) * PX + SEP_W + 8;
}

/** 칸 하나의 동그라미 좌표 (캔버스 단위). grids: [{ x0, cols, label, r, bubbles: [[{x,y,d}]×10]×cols }] */
function placeBlockV1(b, x, y) {
  const gx = x + LABEL_W;
  const by0 = y + BOX_H + 6 + PY / 2;
  const grid = (x0, cols, label) => ({
    x0, cols, label, r: BUB_R,
    boxes: Array.from({ length: cols }, (_, c) => ({ x: x0 + c * PX, y, w: PX, h: BOX_H })),
    bubbles: Array.from({ length: cols }, (_, c) => Array.from({ length: 10 }, (_, d) => ({ x: x0 + c * PX + PX / 2, y: by0 + d * PY, d }))),
  });
  const out = { ...b, x, y, w: blockWidthV1(b), h: BLOCK_H, grids: [], picks: null, hand: null };
  if (b.kind === "pick") {
    out.picks = b.opts.map((label, i) => ({ x: gx + i * PICK_DX + PICK_DX / 2, y: by0 + 2 * PY, label, r: BUB_R + 3 }));
  } else if (b.kind === "int") {
    out.grids.push(grid(gx, b.cols[0], ""));
  } else {
    out.grids.push(grid(gx, b.cols[0], b.kind === "frac" ? "분자" : b.labels[0]));
    out.grids.push(grid(gx + b.cols[0] * PX + SEP_W, b.cols[1], b.kind === "frac" ? "분모" : b.labels[1]));
  }
  return out;
}

function layoutV1(blocks) {
  const pages = [];
  let page = null, x = 0, y = 0;
  const newPage = () => {
    page = { index: pages.length, blocks: [] };
    pages.push(page);
    x = AREA.x0; y = page.index === 0 ? AREA.yFirst : AREA.yOther;
  };
  newPage();
  for (const b of blocks) {
    const w = blockWidthV1(b);
    if (x + w > AREA.x1) { x = AREA.x0; y += BLOCK_H + GAP_Y; }
    if (y + BLOCK_H > AREA.yMax) newPage();
    page.blocks.push(placeBlockV1(b, x, y));
    x += w + GAP_X;
  }
  for (const p of pages) {
    // 같은 줄의 칸들을 가운데로 — 오른쪽 여백을 줄 양끝에 나눠 준다(보기 좋게, 좌표는 그대로 판독에 쓴다)
    const rows = {};
    for (const b of p.blocks) (rows[b.y] = rows[b.y] || []).push(b);
    for (const list of Object.values(rows)) {
      const right = Math.max(...list.map((b) => b.x + b.w));
      const shift = Math.max(0, (AREA.x1 - right) / 2);
      if (shift > 0.5) for (const b of list) shiftBlock(b, shift);
    }
  }
  return pages;
}

// v2 — 번호는 칸 위 줄에, 숫자 칸은 크게, 분수는 손글씨 칸
function blockWidthV2(b) {
  const G = V2;
  if (b.kind === "pick") return b.opts.length * G.PICK_DX + 2 * G.PAD;
  if (b.kind === "frac") return G.FRAC_W + 2 * G.PAD;
  if (b.kind === "int") return b.cols[0] * G.PX + 2 * G.PAD;
  return (b.cols[0] + b.cols[1]) * G.PX + G.SEP_W + 2 * G.PAD;
}

function placeBlockV2(b, x, y) {
  const G = V2;
  const gx = x + G.PAD;
  const boxY = y + G.HEAD;
  const by0 = boxY + G.BOX_H + G.BOX_GAP + G.PY / 2;
  const grid = (x0, cols, label) => ({
    x0, cols, label, r: G.BUB_R,
    boxes: Array.from({ length: cols }, (_, c) => ({ x: x0 + c * G.PX, y: boxY, w: G.PX, h: G.BOX_H })),
    bubbles: Array.from({ length: cols }, (_, c) => Array.from({ length: 10 }, (_, d) => ({ x: x0 + c * G.PX + G.PX / 2, y: by0 + d * G.PY, d }))),
  });
  const out = { ...b, x, y, w: blockWidthV2(b), h: G.BLOCK_H, grids: [], picks: null, hand: null };
  if (b.kind === "pick") {
    out.picks = b.opts.map((label, i) => ({ x: gx + i * G.PICK_DX + G.PICK_DX / 2, y: boxY + 54, label, r: G.PICK_R }));
  } else if (b.kind === "frac") {
    const ny = boxY + 4;
    const num = { x: gx, y: ny, w: G.FRAC_W, h: G.FRAC_BOX_H };
    const den = { x: gx, y: ny + G.FRAC_BOX_H + G.FRAC_BAR, w: G.FRAC_W, h: G.FRAC_BOX_H };
    out.hand = { num, den, bar: { x1: gx + 8, x2: gx + G.FRAC_W - 8, y: ny + G.FRAC_BOX_H + G.FRAC_BAR / 2 } };
  } else if (b.kind === "int") {
    out.grids.push(grid(gx, b.cols[0], ""));
  } else {
    out.grids.push(grid(gx, b.cols[0], b.labels[0]));
    out.grids.push(grid(gx + b.cols[0] * G.PX + G.SEP_W, b.cols[1], b.labels[1]));
  }
  return out;
}

function layoutV2(blocks) {
  const G = V2, A = G.AREA, AW = A.x1 - A.x0;
  // 줄 나누기: 순서대로, 폭(최소 간격 포함)과 한 줄 칸 수 안에서
  const fits = (list) => list.reduce((a, b) => a + blockWidthV2(b), 0) + G.GAP_X * (list.length - 1) <= AW;
  let rows = [];
  let row = [];
  for (const b of blocks) {
    if (row.length && (row.length >= G.ROW_MAX || !fits([...row, b]))) { rows.push(row); row = []; }
    row.push(b);
  }
  if (row.length) rows.push(row);
  // 줄 수는 그대로 두고 칸 수를 고르게(6 · 6 · … · 2 → 6 · 6 · 5 · 5 …) — 폭이 넘치면 처음 나눈 대로
  const R = rows.length, base = Math.floor(blocks.length / R), extra = blocks.length % R;
  const even = [];
  for (let i = 0, at = 0; i < R; i++) { const n = base + (i < extra ? 1 : 0); even.push(blocks.slice(at, at + n)); at += n; }
  if (even.every((l) => l.length && l.length <= G.ROW_MAX && fits(l))) rows = even;
  const pages = [];
  rows.forEach((list, ri) => {
    const pi = Math.floor(ri / G.ROWS), k = ri % G.ROWS;
    if (!pages[pi]) pages[pi] = { index: pi, blocks: [] };
    const y = pi === 0 ? A.yFirst + k * (G.BLOCK_H + G.GAP_Y.first) : A.yOther + k * (G.BLOCK_H + G.GAP_Y.other);
    // 칸 사이를 고르게 벌리고(최대 GAP_MAX) 남는 폭은 양끝에 나눈다
    const ws = list.map(blockWidthV2), sum = ws.reduce((a, c) => a + c, 0);
    const gap = list.length > 1 ? Math.min(G.GAP_MAX, (AW - sum) / (list.length - 1)) : 0;
    let x = A.x0 + (AW - sum - gap * (list.length - 1)) / 2;
    list.forEach((b, i) => { pages[pi].blocks.push(placeBlockV2(b, x, y)); x += ws[i] + gap; });
  });
  return pages;
}

// 일차함수(lin) — 손글씨 한 줄 칸 · 보기
function blockWidthLine(b) {
  const G = LINE;
  if (b.kind === "pick") return b.opts.length * G.PICK_DX + 2 * G.PAD;
  return G.W[b.ak] || G.W.num;
}

function placeBlockLine(b, x, y) {
  const G = LINE;
  const out = { ...b, x, y, w: blockWidthLine(b), h: G.ROW_H, grids: [], picks: null, hand: null };
  if (b.kind === "pick") {
    out.picks = b.opts.map((label, i) => ({ x: x + G.PAD + i * G.PICK_DX + G.PICK_DX / 2, y: y + G.HEAD + G.BOX_H / 2, label, r: G.PICK_R }));
  } else {
    const pre = b.ak === "lin" ? G.PRE : 0;
    out.hand = { num: { x: x + G.PAD + pre, y: y + G.HEAD, w: out.w - 2 * G.PAD - pre, h: G.BOX_H }, den: null, bar: null,
      pre: pre ? { x: x + G.PAD, y: y + G.HEAD + G.BOX_H / 2 } : null };
  }
  return out;
}

function layoutLine(blocks) {
  const G = LINE, A = G.AREA, AW = A.x1 - A.x0;
  const fits = (list) => list.reduce((a, b) => a + blockWidthLine(b), 0) + G.GAP_X * (list.length - 1) <= AW;
  const rows = [];
  let row = [];
  for (const b of blocks) {
    if (row.length && (row.length >= G.ROW_MAX || !fits([...row, b]))) { rows.push(row); row = []; }
    row.push(b);
  }
  if (row.length) rows.push(row);
  const per = (pi) => Math.floor(((A.yMax - (pi === 0 ? A.yFirst : A.yOther)) + G.GAP_Y) / (G.ROW_H + G.GAP_Y));
  const pages = [];
  let pi = 0, k = 0;
  for (const list of rows) {
    if (k >= per(pi)) { pi++; k = 0; }
    if (!pages[pi]) pages[pi] = { index: pi, blocks: [] };
    const y = (pi === 0 ? A.yFirst : A.yOther) + k * (G.ROW_H + G.GAP_Y);
    const ws = list.map(blockWidthLine), sum = ws.reduce((a, c) => a + c, 0);
    const gap = list.length > 1 ? Math.min(G.GAP_MAX, (AW - sum) / (list.length - 1)) : 0;
    let x = A.x0 + (AW - sum - gap * (list.length - 1)) / 2;
    list.forEach((b, i) => { pages[pi].blocks.push(placeBlockLine(b, x, y)); x += ws[i] + gap; });
    k++;
  }
  return pages;
}

/**
 * 카드 배치. set: { cat:"prob", no, title, short, items:[{ no, a, omr }] } · opts.ver: 1(예전) | 2(지금, 기본)
 * 일차함수(cat "lin")는 v2 의 손글씨 한 줄 카드(layoutLine) — 예전 판이 없다.
 * → { cat, set, ver, title, pages:[{ index, n, ver, W, H, markers, orient, band, bandPos, blocks:[…] }] }
 */
export function layoutCard(set, opts = {}) {
  const ver = opts.ver === 1 ? 1 : OMR_VER;
  const cat = set.cat || "prob";
  if (ver === 1 && cat !== "prob") throw new Error("예전(v1) 카드는 경우의 수와 확률 범주에만 있다");
  const blocks = (set.items || []).map((it, i) => ({ no: it.no ?? i + 1, ...kindOf(it) }));
  const pages = ver === 1 ? layoutV1(blocks) : cat === "lin" ? layoutLine(blocks) : layoutV2(blocks);
  const n = pages.length;
  if (n > 4) throw new Error(`OMR 카드가 ${n}쪽 — 쪽 코드는 4쪽까지`);
  for (const p of pages) {
    Object.assign(p, { n, ver, W: GW, H: GH, markers: markerRects(), orient: { ...ORIENT }, band: bandBits(set.cat || "prob", set.no, p.index), bandPos: bandPosOf(ver) });
  }
  return { cat: set.cat || "prob", set: set.no, ver, title: set.title || "", short: set.short || "", pages };
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
export const INSTRUCTION2 = [
  "정수는 자리마다 숫자 하나를 진하게 칠해요(남는 앞자리는 비워요) · 보기는 맞는 것을 모두 칠해요",
  "분수는 칸에 손으로 크게 써요 — 위 칸에 분자, 아래 칸에 분모 (0 · 1은 위 칸에만)",
];
export const INSTRUCTION_LIN = [
  "답은 칸 안에 손으로 또박또박 한 줄로 써요 — 수(−3 · 3/4 · 0.5) · 식(y = −2x + 3) · 점((2, −1))",
  "보기는 맞는 것을 모두 칠해요 · 단위는 쓰지 않아도 돼요 · 사진은 네 모서리의 검은 네모가 모두 나오게",
];
const LINE_TAG = { num: "수", lin: "식", pt: "점 (x, y)" };
export const PHOTO_TIP = "사진은 네 모서리의 검은 네모가 모두 나오게 위에서 찍어요";
const FONT = `font-family="'Pretendard Variable',Pretendard,'Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif"`;

function svgOpen() {
  return `<svg class="omr-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${GW} ${GH}" width="${mm(GW)}" height="${mm(GH)}" ${FONT}>`;
}
function frameSvg(p, s, emptyStroke) {
  for (const m of p.markers) s.push(`<rect x="${m.x}" y="${m.y}" width="${m.size}" height="${m.size}" fill="#000"/>`);
  const o = p.orient;
  s.push(`<rect x="${o.x}" y="${o.y}" width="${o.w}" height="${o.h}" fill="#000"/>`);
  bandCells(p.bandPos || BAND).forEach((c, i) => {
    if (p.band[i]) s.push(`<rect x="${c.x}" y="${c.y}" width="${c.size}" height="${c.size}" fill="#000"/>`);
    else s.push(`<rect x="${c.x + 0.5}" y="${c.y + 0.5}" width="${c.size - 1}" height="${c.size - 1}" fill="none" stroke="${emptyStroke}" stroke-width="1"/>`);
  });
}

export function pageSvg(card, p) {
  return (p.ver || card.ver) === 1 ? pageSvgV1(card, p) : pageSvgV2(card, p);
}

function pageSvgV1(card, p) {
  const s = [];
  frameSvg(p, s, "#d6d6d6");
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
  return svgOpen() + s.join("") + "</svg>";
}

// v2 — 글씨는 검정에 가깝게 · 굵게, 동그라미 테두리도 진하게. 동그라미 속 숫자는 회색(칠한 것과 구별되게)이지만 굵고 크게.
const INK2 = { text: "#000", sub: "#222", line: "#1f1f1f", digit: "#6b6b6b", pickLabel: "#6b6b6b", hint: "#333" };

function pageSvgV2(card, p) {
  const G = V2, C = INK2;
  const lin = card.cat === "lin";
  const s = [];
  frameSvg(p, s, "#cfcfcf");
  const pg = `${p.index + 1}/${p.n}쪽`;
  if (p.index === 0) {
    s.push(`<text x="500" y="150" text-anchor="middle" font-size="30" font-weight="800" fill="${C.text}">${esc(card.title)}</text>`);
    s.push(`<text x="500" y="182" text-anchor="middle" font-size="17" font-weight="600" fill="${C.sub}">OMR 답안 카드 · ${esc(pg)} · ${lin ? "중2-1" : "중2-2"} · 50제</text>`);
    s.push(`<text x="150" y="222" font-size="18" font-weight="700" fill="${C.text}">이름</text><line x1="196" y1="226" x2="460" y2="226" stroke="${C.text}" stroke-width="1.6"/>`);
    s.push(`<text x="540" y="222" font-size="18" font-weight="700" fill="${C.text}">날짜</text><line x1="586" y1="226" x2="850" y2="226" stroke="${C.text}" stroke-width="1.6"/>`);
    (lin ? INSTRUCTION_LIN : INSTRUCTION2).forEach((t, i) => s.push(`<text x="500" y="${252 + i * 21}" text-anchor="middle" font-size="14.5" font-weight="600" fill="${C.sub}">${esc(t)}</text>`));
  } else {
    s.push(`<text x="500" y="148" text-anchor="middle" font-size="22" font-weight="800" fill="${C.text}">${esc(card.title)} <tspan font-weight="600" font-size="17" fill="${C.sub}">· OMR ${esc(pg)}</tspan></text>`);
    s.push(`<text x="500" y="176" text-anchor="middle" font-size="14" font-weight="600" fill="${C.hint}">${esc(PHOTO_TIP)} · ${lin ? "답은 칸 안에 한 줄로" : "분수는 위 칸 분자, 아래 칸 분모"}</text>`);
  }
  for (const b of p.blocks) {
    const nx = b.x + G.PAD, ny = b.y + 20;
    s.push(`<text x="${nx}" y="${ny}" font-size="21" font-weight="800" fill="${C.text}">${b.no}</text>`);
    const tagX = nx + String(b.no).length * 12.5 + 8;
    if (b.kind === "pick") {
      s.push(`<text x="${tagX}" y="${ny - 1}" font-size="12.5" font-weight="700" fill="${C.hint}">모두 칠해요</text>`);
      for (const q of b.picks) {
        s.push(`<circle cx="${q.x}" cy="${q.y}" r="${q.r}" fill="none" stroke="${C.line}" stroke-width="1.6"/>`);
        s.push(`<text x="${q.x}" y="${q.y + 5.5}" text-anchor="middle" font-size="15" font-weight="700" fill="${C.pickLabel}">${esc(q.label)}</text>`);
      }
      continue;
    }
    if (b.kind === "line") {                       // 일차함수: 손글씨 한 줄 칸 (식은 칸 앞에 「y =」)
      const r = b.hand.num;
      s.push(`<text x="${tagX}" y="${ny - 1}" font-size="13" font-weight="700" fill="${C.hint}">${LINE_TAG[b.ak] || "수"}</text>`);
      s.push(`<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" rx="4" fill="none" stroke="${C.line}" stroke-width="1.8"/>`);
      if (b.hand.pre) s.push(`<text x="${b.hand.pre.x}" y="${b.hand.pre.y + 7}" font-size="20" font-weight="700" fill="${C.text}"><tspan font-style="italic">y</tspan> =</text>`);
      continue;
    }
    if (b.kind === "frac") {
      const { num, den, bar } = b.hand;
      s.push(`<text x="${tagX}" y="${ny - 1}" font-size="13" font-weight="700" fill="${C.hint}">분수 · 손으로</text>`);
      for (const r of [num, den]) s.push(`<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" rx="4" fill="none" stroke="${C.line}" stroke-width="1.8"/>`);
      s.push(`<line x1="${bar.x1}" y1="${bar.y}" x2="${bar.x2}" y2="${bar.y}" stroke="#000" stroke-width="3.2" stroke-linecap="round"/>`);
      continue;
    }
    if (b.kind === "pair") s.push(`<text x="${tagX}" y="${ny - 1}" font-size="12.5" font-weight="700" fill="${C.hint}">${esc(b.grids.map((g) => g.label).filter(Boolean).join(" , "))}</text>`);
    b.grids.forEach((g, gi) => {
      for (const bx of g.boxes) s.push(`<rect x="${bx.x}" y="${bx.y}" width="${bx.w}" height="${bx.h}" fill="none" stroke="#333" stroke-width="1.3"/>`);
      for (const col of g.bubbles) for (const bb of col) {
        s.push(`<circle cx="${bb.x}" cy="${bb.y}" r="${g.r}" fill="none" stroke="${C.line}" stroke-width="1.5"/>`);
        s.push(`<text x="${bb.x}" y="${bb.y + 4.5}" text-anchor="middle" font-size="12.5" font-weight="700" fill="${C.digit}">${bb.d}</text>`);
      }
      if (gi === 1) {
        const sx = g.x0 - G.SEP_W / 2, top = g.boxes[0].y;
        s.push(`<text x="${sx}" y="${top + 22}" text-anchor="middle" font-size="22" font-weight="800" fill="${C.text}">,</text>`);
        s.push(`<line x1="${sx}" y1="${top + G.BOX_H + 10}" x2="${sx}" y2="${top + G.BOX_H + G.BOX_GAP + 10 * G.PY - 2}" stroke="#999" stroke-width="1.2" stroke-dasharray="4 4"/>`);
      }
    });
  }
  return svgOpen() + s.join("") + "</svg>";
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
/**
 * 동그라미 둘레(r0~r1) 종이 밝기 — 대각선 방향 네 부채꼴마다 80% 분위수(이웃 동그라미 테두리 · 번진 연필은 버림)를 내고 그중 가장 어두운 값.
 * 그림자 경계가 동그라미에 걸치면 어두운 쪽 종이를 기준으로 삼아, 경계 때문에 칠한 것처럼 보이지 않게 한다.
 */
function ringBg(g, W, H, cx, cy, r0, r1) {
  const sec = [[], [], [], []];
  const a = r0 * r0, b = r1 * r1;
  for (let y = Math.max(0, Math.floor(cy - r1)); y <= Math.min(H - 1, Math.ceil(cy + r1)); y++)
    for (let x = Math.max(0, Math.floor(cx - r1)); x <= Math.min(W - 1, Math.ceil(cx + r1)); x++) {
      const dx = x + 0.5 - cx, dy = y + 0.5 - cy, d = dx * dx + dy * dy;
      if (d >= a && d <= b) sec[(dx >= 0 ? 0 : 1) + (dy >= 0 ? 0 : 2)].push(g[y * W + x]);
    }
  let bg = 255;
  for (const vals of sec) {
    if (vals.length < 4) continue;
    vals.sort((p, q) => p - q);
    bg = Math.min(bg, vals[Math.min(vals.length - 1, Math.floor(vals.length * 0.8))]);
  }
  return bg;
}
function meanRect(g, W, H, x, y, w, h) {
  let s = 0, n = 0;
  for (let j = Math.max(0, Math.floor(y)); j < Math.min(H, Math.ceil(y + h)); j++)
    for (let i = Math.max(0, Math.floor(x)); i < Math.min(W, Math.ceil(x + w)); i++) { s += g[j * W + i]; n++; }
  return n ? s / n : 255;
}
function pix(g, W, H, x, y) {
  if (x < 0) x = 0; else if (x > W - 1.001) x = W - 1.001;
  if (y < 0) y = 0; else if (y > H - 1.001) y = H - 1.001;
  const x0 = x | 0, y0 = y | 0, fx = x - x0, fy = y - y0, i = y0 * W + x0;
  return (g[i] * (1 - fx) + g[i + 1] * fx) * (1 - fy) + (g[i + W] * (1 - fx) + g[i + W + 1] * fx) * fy;
}

/** 동그라미 하나의 채움 비율 (0~1) — 안쪽 어둡기를 그 둘레 종이 밝기와 잉크 밝기 사이에서 잰다 */
function fillAt(wp, x, y, r, ink) {
  const { gray: g, width: W, height: H, scale: sc } = wp;
  const inside = meanDisk(g, W, H, x * sc, y * sc, r * sc * 0.62);
  const bg = ringBg(g, W, H, x * sc, y * sc, r * sc * 1.25, r * sc * 1.9);
  return clamp01((bg - inside) / Math.max(bg - ink, 40));
}

/** 빈 동그라미의 바탕(속 숫자 · 테두리 번짐) — 한 열 10개 중 가운데 값들. 칠한 것은 많아야 둘이라 바탕만 남는다 */
function columnBase(fills) {
  const s = fills.slice().sort((a, b) => a - b);
  const mid = s.slice(2, 7);
  return mid.reduce((a, c) => a + c, 0) / mid.length;
}
const rel = (f, base) => clamp01((f - base) / Math.max(0.5, 1 - base));

/** 띠 14칸 읽기 — 양 끝 칸(늘 검정)과 칸 사이 종이로 기준을 잡는다. pos: BAND(v1, 위) · BAND2(v2, 아래) */
export function readBand(wp, pos = BAND) {
  const { gray: g, width: W, height: H, scale: sc } = wp;
  const cells = bandCells(pos).map((c) => meanRect(g, W, H, (c.x + 4) * sc, (c.y + 4) * sc, (c.size - 8) * sc, (c.size - 8) * sc));
  const paper = meanRect(g, W, H, (pos.x0 + pos.cell + 2) * sc, (pos.y + 4) * sc, (pos.gap - 4) * sc, (pos.cell - 8) * sc);
  const black = (cells[0] + cells[pos.n - 1]) / 2;
  if (paper - black < 40) return { bits: null, contrast: paper - black };
  const mid = (paper + black) / 2;
  const bits = cells.map((v) => (v < mid ? 1 : 0));
  return { bits, contrast: paper - black, info: parseBand(bits) };
}

function readGrid(wp, grid, ink) {
  const digits = [], confs = [], flags = [];
  const r = grid.r ?? BUB_R;
  for (const col of grid.bubbles) {
    const raw = col.map((b) => fillAt(wp, b.x, b.y, r, ink));
    const base = columnBase(raw);
    const fills = raw.map((f) => rel(f, base));
    const order = fills.map((f, i) => i).sort((p, q) => fills[q] - fills[p]);
    const max = fills[order[0]], second = fills[order[1]];
    if (max < FILL_MIN) {
      // 연하게 · 덜 칠한 것: 한 동그라미만 뚜렷이 어두우면 그 숫자로 읽되 노란 칸(확인)으로
      if (max >= FAINT_MIN && max - second >= FAINT_GAP) { digits.push(String(order[0])); confs.push(0.3); flags.push("weak"); continue; }
      digits.push(""); confs.push(clamp01((FILL_MIN - max) / FILL_MIN)); flags.push(null); continue;
    }
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

/**
 * 손글씨 칸에 글씨가 있나 — 칸 안쪽(테두리에서 HAND_INSET 만큼 안)에서 둘레 평균보다 확실히 어두운 점을 센다.
 * 그림자처럼 넓게 어두운 것은 둘레 평균도 같이 어두워져 세지 않는다.
 */
export function handInk(wp, rect, ink) {
  const { gray: g, width: W, height: H, scale: sc } = wp;
  const x0 = Math.max(0, Math.round((rect.x + HAND_INSET) * sc)), y0 = Math.max(0, Math.round((rect.y + HAND_INSET) * sc));
  const x1 = Math.min(W, Math.round((rect.x + rect.w - HAND_INSET) * sc)), y1 = Math.min(H, Math.round((rect.y + rect.h - HAND_INSET) * sc));
  const w = x1 - x0, h = y1 - y0;
  if (w < 4 || h < 4) return { ink: false, frac: 0, dark: 0 };
  // 적분 영상으로 둘레(창 2k+1) 평균
  const k = Math.max(3, Math.round(8 * sc));
  const I = new Float64Array((w + 1) * (h + 1));
  for (let j = 0; j < h; j++) {
    let row = 0;
    for (let i = 0; i < w; i++) { row += g[(y0 + j) * W + x0 + i]; I[(j + 1) * (w + 1) + i + 1] = I[j * (w + 1) + i + 1] + row; }
  }
  const vals = [];
  for (let j = 0; j < h; j += 2) for (let i = 0; i < w; i += 2) vals.push(g[(y0 + j) * W + x0 + i]);
  vals.sort((a, b) => a - b);
  const paper = vals[Math.floor(vals.length * 0.9)];
  const thr = Math.max(22, 0.22 * (paper - ink));
  let dark = 0;
  for (let j = 0; j < h; j++) {
    const ja = Math.max(0, j - k), jb = Math.min(h, j + k + 1);
    for (let i = 0; i < w; i++) {
      const ia = Math.max(0, i - k), ib = Math.min(w, i + k + 1);
      const sum = I[jb * (w + 1) + ib] - I[ja * (w + 1) + ib] - I[jb * (w + 1) + ia] + I[ja * (w + 1) + ia];
      const local = sum / ((jb - ja) * (ib - ia));
      if (g[(y0 + j) * W + x0 + i] < local - thr) dark++;
    }
  }
  const frac = dark / (w * h);
  return { ink: dark >= Math.max(10 * sc * sc, 0.003 * w * h), frac, dark };
}

/** 손글씨 칸 안쪽을 잘라 밝기를 펴 준다(종이 → 흰색, 연필 → 검정) — AI 에 보낼 조각. { width, height, gray } */
export function handCrop(wp, rect, ink, inset = 4) {
  const { gray: g, width: W, height: H, scale: sc } = wp;
  const x0 = Math.max(0, Math.round((rect.x + inset) * sc)), y0 = Math.max(0, Math.round((rect.y + inset) * sc));
  const x1 = Math.min(W, Math.round((rect.x + rect.w - inset) * sc)), y1 = Math.min(H, Math.round((rect.y + rect.h - inset) * sc));
  const w = Math.max(1, x1 - x0), h = Math.max(1, y1 - y0);
  const out = new Uint8ClampedArray(w * h);
  const vals = [];
  for (let j = 0; j < h; j += 2) for (let i = 0; i < w; i += 2) vals.push(g[(y0 + j) * W + x0 + i]);
  vals.sort((a, b) => a - b);
  const hi = vals[Math.floor(vals.length * 0.92)] || 255;
  const lo = Math.max(ink, Math.min(vals[Math.floor(vals.length * 0.01)] ?? 0, hi - 60));   // 가장 진한 획 → 검정(연한 연필도 또렷하게)
  for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
    const v = (g[(y0 + j) * W + x0 + i] - lo) / Math.max(1, hi - lo);
    out[j * w + i] = Math.round(255 * clamp01(v));
  }
  return { width: w, height: h, gray: out };
}

/** 칸 하나 → { no, kind, raw(학생이 쓴 꼴: "12" · "5/12" · "ㄱ, ㄷ" · "14, 21"), conf, flag[, hand] } */
export function readBlock(wp, b, ink, pageBase = 0.06) {
  if (b.hand) {
    // v2 분수 · 일차함수 한 줄 칸: 글씨가 있는지만 — 읽기는 AI(handCrops → OmrGrade)
    const num = handInk(wp, b.hand.num, ink), den = b.hand.den ? handInk(wp, b.hand.den, ink) : { ink: false };
    const any = num.ink || den.ink;
    return { no: b.no, kind: b.kind, raw: "", conf: any ? 0 : 0.95, flag: any ? "hand" : null, hand: { num: num.ink, den: den.ink } };
  }
  if (b.kind === "pick") {
    const fills = b.picks.map((q) => rel(fillAt(wp, q.x, q.y, q.r ?? BUB_R + 3, ink), pageBase));
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

/** 쪽의 빈 동그라미 바탕(열 바탕의 중앙값) — 보기 동그라미는 여러 개 칠할 수 있어 쪽 바탕을 빌려 쓴다 */
function pageBaseOf(wp, p, ink) {
  const bases = [];
  for (const b of p.blocks) for (const g of b.grids) for (const col of g.bubbles) {
    if (bases.length >= 16) break;
    bases.push(columnBase(col.map((q) => fillAt(wp, q.x, q.y, g.r ?? BUB_R, ink))));
  }
  return bases.length ? median(bases) : 0.06;
}

/**
 * 쪽 그림이 이 배치와 맞나 — 인쇄된 동그라미 테두리 · 손글씨 칸 테두리 자리가 그 바로 안팎보다 어두운 정도(0~255).
 * 띠를 못 읽어 학생이 쪽을 고른 사진에서 v1 · v2 중 어느 카드인지 가릴 때 쓴다.
 */
export function layoutFit(wp, p) {
  const { gray: g, width: W, height: H, scale: sc } = wp;
  const circles = [];
  for (const b of p.blocks) {
    for (const gr of b.grids) for (const col of gr.bubbles) for (const q of col) circles.push([q.x, q.y, gr.r ?? BUB_R]);
    if (b.picks) for (const q of b.picks) circles.push([q.x, q.y, q.r ?? BUB_R + 3]);
  }
  let sum = 0, n = 0;
  const step = Math.max(1, Math.floor(circles.length / 150));
  for (let i = 0; i < circles.length; i += step) {
    const [x, y, r] = circles[i];
    let ring = 0, off = 0;
    for (let k = 0; k < 16; k++) {
      const a = (k / 16) * 2 * Math.PI, c = Math.cos(a), s = Math.sin(a);
      ring += pix(g, W, H, (x + c * r) * sc, (y + s * r) * sc);
      off += (pix(g, W, H, (x + c * r * 0.8) * sc, (y + s * r * 0.8) * sc) + pix(g, W, H, (x + c * r * 1.3) * sc, (y + s * r * 1.3) * sc)) / 2;
    }
    sum += (off - ring) / 16; n++;
  }
  for (const b of p.blocks) if (b.hand) for (const r of [b.hand.num, b.hand.den].filter(Boolean)) {
    for (let k = 1; k < 8; k++) {
      const x = r.x + (r.w * k) / 8;
      for (const [ey, iy] of [[r.y, r.y + 6], [r.y + r.h, r.y + r.h - 6]]) {
        sum += pix(g, W, H, x * sc, iy * sc) - pix(g, W, H, x * sc, ey * sc); n++;
      }
    }
  }
  return n ? sum / n : 0;
}

/** 여러 판의 카드를 { [ver]: card } 로 */
function cardMap(cards) {
  const list = Array.isArray(cards) ? cards : cards && cards.pages ? [cards] : Object.values(cards || {});
  const m = {};
  for (const c of list) if (c && c.pages) m[c.ver || 1] = c;
  return m;
}

/**
 * 사진 한 장 → { ok, reason?, ver, page, set, cat, answers:[{no, kind, raw, conf, flag[, hand]}], corners, card, warped }
 * cards: layoutCard 결과 하나, 또는 판별 { 2: 지금 카드, 1: 예전 카드 } — 띠의 자리로 판을 가린다.
 * 띠를 못 읽으면 opts.page(0부터)로 읽고, 판은 쪽 그림이 더 잘 맞는 쪽(layoutFit)으로.
 */
export function readCardPhoto(img, cards, opts = {}) {
  const byVer = cardMap(cards);
  const vers = Object.keys(byVer).map(Number).sort((a, b) => b - a);
  const fail = (reason, extra = {}) => ({ ok: false, reason, page: null, answers: [], ...extra });
  if (!vers.length) return fail("card");
  const any = byVer[vers[0]];
  const w = img.width, h = img.height;
  const gray = toGray(img);
  const bin = threshold(gray, w, h, opts.threshold);
  const quad = findMarkers(bin, w, h, opts);
  if (!quad) return fail("markers");
  const spec0 = any.pages[0];
  const o = orientCorners(gray, w, h, quad, spec0);
  if (!o) return fail("orient", { corners: quad });
  const scale = opts.scale || 1;
  const wp = warpToSpec(gray, w, h, o.corners, spec0, scale);
  if (!wp) return fail("warp", { corners: o.corners });
  // 띠: 지금 카드(아래) → 예전 카드(위)
  let ver = null, band = null, bits = null;
  for (const v of [2, 1]) {
    const r = readBand(wp, bandPosOf(v));
    if (r.info) { ver = v; band = r; break; }
    if (r.bits && !bits) bits = r.bits;
  }
  let card, pageIdx;
  if (band) {
    if (band.info.set !== any.set || (band.info.cat && band.info.cat !== any.cat)) return fail("other-set", { band: band.info, corners: o.corners, ver });
    card = byVer[ver];
    if (!card) return fail("version", { ver, corners: o.corners });
    pageIdx = band.info.page;
  } else {
    pageIdx = opts.page ?? null;
    if (pageIdx == null) return fail("band", { corners: o.corners, band: bits });
    const cands = vers.map((v) => byVer[v]).filter((c) => c.pages[pageIdx] && (opts.ver == null || c.ver === opts.ver));
    if (!cands.length) return fail("band", { corners: o.corners, band: bits });
    card = cands.length === 1 ? cands[0] : cands.map((c) => [c, layoutFit(wp, c.pages[pageIdx])]).sort((a, b) => b[1] - a[1])[0][0];
    ver = card.ver || 1;
  }
  const p = card.pages[pageIdx];
  if (!p) return fail("band", { corners: o.corners, band: band?.bits || bits });
  const ink = inkLevel(wp, p);
  const base = p.blocks.some((b) => b.picks) ? pageBaseOf(wp, p, ink) : 0.06;
  const answers = p.blocks.map((b) => readBlock(wp, b, ink, base));
  return { ok: true, reason: null, ver, page: pageIdx, set: card.set, cat: card.cat, answers, corners: o.corners, bandOk: !!band, warped: wp, card, ink };
}

/**
 * 판독 결과에서 손글씨(분수) 칸 조각 — AI 에 보낼 것만: [{ no, num:{width,height,gray}, den|null }]
 * 분자 칸은 늘 넣고(0 · 1 은 분자만), 분모 칸은 글씨가 있을 때만.
 */
export function handCrops(res) {
  if (!res?.ok || !res.card) return [];
  const p = res.card.pages[res.page];
  const ink = res.ink ?? inkLevel(res.warped, p);
  const out = [];
  for (const a of res.answers) {
    if (a.flag !== "hand") continue;
    const b = p.blocks.find((x) => x.no === a.no);
    if (!b?.hand) continue;
    out.push({ no: a.no, num: handCrop(res.warped, b.hand.num, ink), den: a.hand?.den ? handCrop(res.warped, b.hand.den, ink) : null });
  }
  return out;
}
