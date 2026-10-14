// ashrain.out — 서술형 평가 시험지 좌표계 · 쪽 번호 띠 · 사진 품질 (순수 함수, DOM 없음 — node 테스트 가능)
//
// 시험지 한 쪽 = 찰칵 채점(OMR) 카드와 같은 좌표계: 가로 1000 × 세로 1414 단위(1단위 = 0.19mm → 190 × 268.66mm, A4 여백 10mm).
//   · 네 귀퉁이 검은 정사각형 마커 60(안쪽 여백 50) + 왼쪽 위 마커 오른쪽 방향 막대(x 122~146, y 50~110)
//     → src/lib/omr/detect.js 의 threshold · findMarkers · orientCorners · warpToSpec 를 그대로 쓴다.
//   · 아래 가운데 「쪽 번호 띠」 14칸(검은 칸 = 1): 쪽 번호 4비트 + 평가 확인 5비트 → 해밍(13,9) + 전체 패리티(SECDED, 거리 4).
//     칸 3개까지 잘못 읽어도 다른 값으로 통과하지 않는다(고치지는 않고 다시 찍게 한다).
//     찍은 사진이 몇 쪽인지, 이 평가의 시험지가 맞는지 브라우저에서 바로 안다(서버·AI 없이).
// 생성기(build_assess.py)가 같은 값으로 그린다 — 값을 바꾸면 양쪽을 함께 바꿀 것.

export const SHEET_W = 1000;
export const SHEET_H = 1414;
export const MM_PER_UNIT = 0.19;
export const MARKER_SIZE = 60;
export const MARKER_INSET = 50;
export const ORIENT = { x: 122, y: 50, w: 24, h: 60 };
export const PAGECODE = { n: 14, x0: 308, y0: 1324, size: 20, pitch: 28 };
export const CODE_MARGIN_MIN = 0.12;   // 가장 애매한 칸이 기준선에서 이만큼은 떨어져야 믿는다
export const MAX_PAGES = 15;          // 쪽 번호 4비트 (1~15)

/** 마커 4개 (TL, TR, BR, BL) — detect.js 가 받는 모양 */
export function markerRects(size = MARKER_SIZE, inset = MARKER_INSET, W = SHEET_W, H = SHEET_H) {
  return [
    { x: inset, y: inset, size },
    { x: W - inset - size, y: inset, size },
    { x: W - inset - size, y: H - inset - size, size },
    { x: inset, y: H - inset - size, size },
  ];
}

/** detect.js 용 spec — 평가 JSON 의 sheet 값이 있으면 그것으로 */
export function sheetSpec(sheet = null) {
  const W = +sheet?.w || SHEET_W, H = +sheet?.h || SHEET_H;
  const size = +sheet?.markers?.size || MARKER_SIZE, inset = +sheet?.markers?.inset || MARKER_INSET;
  const o = sheet?.orient || ORIENT;
  return { W, H, markers: markerRects(size, inset, W, H), orient: { x: +o.x, y: +o.y, w: +o.w, h: +o.h } };
}

/** 평가 코드 → 5비트 확인값 (FNV-1a 32 접기). 생성기(Python)와 같은 계산 */
export function checkOf(code) {
  let h = 2166136261 >>> 0;
  for (const ch of String(code || "")) {
    h ^= ch.codePointAt(0);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return ((h >>> 27) ^ (h >>> 22) ^ (h >>> 17) ^ (h >>> 12) ^ (h >>> 7) ^ (h >>> 2) ^ h) & 31;
}

// 해밍(13,9): 위치 1~13 중 1·2·4·8 은 패리티, 나머지 9자리에 데이터(쪽 4비트 → 확인 5비트, 각각 낮은 자리부터). 14번째 = 전체 패리티.
const DATA_POS = [3, 5, 6, 7, 9, 10, 11, 12, 13];
const PAR_POS = [1, 2, 4, 8];

/** 쪽 번호 + 확인값 → 14비트 (칸 0 = 위치 1) */
export function encodePage(page, check) {
  if (!(page >= 1 && page <= MAX_PAGES)) throw new Error("쪽 번호는 1~15");
  const d = [];
  for (let i = 0; i < 4; i++) d.push((page >> i) & 1);
  for (let i = 0; i < 5; i++) d.push((check >> i) & 1);
  const c = new Array(15).fill(0);
  DATA_POS.forEach((pos, i) => { c[pos] = d[i]; });
  for (const p of PAR_POS) { let x = 0; for (let j = 1; j <= 13; j++) if (j !== p && (j & p)) x ^= c[j]; c[p] = x; }
  let all = 0; for (let j = 1; j <= 13; j++) all ^= c[j];
  c[14] = all;
  return c.slice(1);
}

/** 14비트 → { page, check, ok } — 증후군·전체 패리티가 하나라도 어긋나거나 쪽 0 이면 ok=false (고치지 않는다) */
export function decodeBits(bits) {
  if (!Array.isArray(bits) || bits.length !== PAGECODE.n) return { page: 0, check: -1, ok: false };
  const c = [0, ...bits.map((b) => (b ? 1 : 0))];
  let syn = 0;
  for (const p of PAR_POS) { let x = 0; for (let j = 1; j <= 13; j++) if (j & p) x ^= c[j]; if (x) syn |= p; }
  let all = 0; for (let j = 1; j <= 14; j++) all ^= c[j];
  let page = 0, check = 0;
  DATA_POS.forEach((pos, i) => { if (i < 4) page |= c[pos] << i; else check |= c[pos] << (i - 4); });
  return { page, check, ok: syn === 0 && all === 0 && page >= 1 };
}

/** 띠 칸 좌표 (단위) */
export function codeCells(pc = PAGECODE) {
  const out = [];
  for (let i = 0; i < pc.n; i++) out.push({ x: pc.x0 + pc.pitch * i, y: pc.y0, w: pc.size, h: pc.size });
  return out;
}

// ── 워프된 래스터 { width, height, gray, scale } 위 표본 ─────────────────────
function meanRect(g, W, H, x0, y0, x1, y1) {
  const a = Math.max(0, Math.floor(x0)), b = Math.max(0, Math.floor(y0));
  const c = Math.min(W, Math.ceil(x1)), d = Math.min(H, Math.ceil(y1));
  let s = 0, n = 0;
  for (let y = b; y < d; y++) for (let x = a; x < c; x++) { s += g[y * W + x]; n++; }
  return n ? s / n : 255;
}
function pctRect(g, W, H, x0, y0, x1, y1, p, step = 1) {
  const a = Math.max(0, Math.floor(x0)), b = Math.max(0, Math.floor(y0));
  const c = Math.min(W, Math.ceil(x1)), d = Math.min(H, Math.ceil(y1));
  const hist = new Uint32Array(256);
  let n = 0;
  for (let y = b; y < d; y += step) for (let x = a; x < c; x += step) { hist[g[y * W + x]]++; n++; }
  if (!n) return 255;
  const target = n * p;
  let acc = 0;
  for (let v = 0; v < 256; v++) { acc += hist[v]; if (acc >= target) return v; }
  return 255;
}

/**
 * 쪽 번호 띠 읽기. warped: warpToSpec 결과(scale 배 래스터), sheet: 평가 JSON 의 sheet(없으면 기본값).
 * → { bits, page, check, ok, contrast, margin }  margin = 가장 애매한 칸이 기준선에서 떨어진 정도(0~0.5)
 */
export function readPageCode(warped, sheet = null) {
  const { gray: g, width: W, height: H } = warped;
  const s = warped.scale || (W / (+sheet?.w || SHEET_W));
  const pc = sheet?.pagecode || PAGECODE;
  const cells = codeCells(pc);
  const last = cells[cells.length - 1];
  // 종이 밝기: 띠를 둘러싼 띠 영역의 85% 분위수 (칸 사이·위아래 여백이 대부분이라 종이 쪽으로 붙는다)
  const paper = pctRect(g, W, H, (pc.x0 - 24) * s, (pc.y0 - 14) * s, (last.x + last.w + 24) * s, (pc.y0 + pc.size + 14) * s, 0.85);
  // 잉크 밝기: 왼쪽 아래 마커 속 (항상 검다)
  const sz = +sheet?.markers?.size || MARKER_SIZE, ins = +sheet?.markers?.inset || MARKER_INSET;
  const Hs = +sheet?.h || SHEET_H;
  const mk = { x: ins, y: Hs - ins - sz };
  const ink = meanRect(g, W, H, (mk.x + sz * 0.25) * s, (mk.y + sz * 0.25) * s, (mk.x + sz * 0.75) * s, (mk.y + sz * 0.75) * s);
  const contrast = paper - ink;
  const t = (paper + ink) / 2;
  let margin = 0.5;
  const bits = cells.map((c) => {
    const m = meanRect(g, W, H, (c.x + c.w * 0.25) * s, (c.y + c.h * 0.25) * s, (c.x + c.w * 0.75) * s, (c.y + c.h * 0.75) * s);
    if (contrast > 0) margin = Math.min(margin, Math.abs(m - t) / contrast);
    return m < t ? 1 : 0;
  });
  const dec = decodeBits(bits);
  return { bits, ...dec, ok: dec.ok && contrast >= 40 && margin >= CODE_MARGIN_MIN, contrast: Math.round(contrast), margin: Math.round(margin * 100) / 100 };
}

/**
 * 사진 품질 — 워프된 쪽에서 종이 밝기(90% 분위수)와 선명도(라플라시안 분산, 가운데 영역).
 * 선명도는 scale 에 따라 달라서 1단위=1px 기준으로 맞춘 값을 돌려준다.
 */
export function pageQuality(warped) {
  const { gray: g, width: W, height: H } = warped;
  const s = warped.scale || 1;
  const paper = pctRect(g, W, H, W * 0.06, H * 0.06, W * 0.94, H * 0.94, 0.9, 3);
  const dark = pctRect(g, W, H, W * 0.06, H * 0.06, W * 0.94, H * 0.94, 0.02, 3);
  // 라플라시안 분산 — 1/2 로 줄여(이웃 평균) 잡음 영향을 덜고, scale 차이를 줄인다
  const step = Math.max(1, Math.round(s));
  let sum = 0, sum2 = 0, n = 0;
  const x0 = Math.floor(W * 0.08), x1 = Math.floor(W * 0.92), y0 = Math.floor(H * 0.1), y1 = Math.floor(H * 0.9);
  for (let y = y0; y < y1; y += step) {
    for (let x = x0; x < x1; x += step) {
      const c = g[y * W + x];
      const l = g[y * W + x - step], r = g[y * W + x + step], u = g[(y - step) * W + x], d = g[(y + step) * W + x];
      const v = 4 * c - l - r - u - d;
      sum += v; sum2 += v * v; n++;
    }
  }
  const mean = n ? sum / n : 0;
  const lapVar = n ? sum2 / n - mean * mean : 0;
  return { paper, dark, sharp: Math.round(lapVar), contrast: paper - dark };
}

/** 품질 판정 기준 — 아주 나쁜 것만 다시 찍게 한다(멀쩡한 사진을 돌려보내지 않는 쪽으로) */
export const QUALITY_MIN = { paper: 95, contrast: 70, sharp: 60 };

/** 품질 → { ok, reason } (reason: dark | flat | blur) */
export function judgeQuality(q) {
  if (!q) return { ok: false, reason: "flat" };
  if (q.paper < QUALITY_MIN.paper) return { ok: false, reason: "dark" };
  if (q.contrast < QUALITY_MIN.contrast) return { ok: false, reason: "flat" };
  if (q.sharp < QUALITY_MIN.sharp) return { ok: false, reason: "blur" };
  return { ok: true, reason: null };
}

/** 영역들 [x0,y0,x1,y1] 의 합집합 (+여백 pad 단위), 시트 안으로 */
export function unionBox(boxes, pad = 0, W = SHEET_W, H = SHEET_H) {
  const list = (boxes || []).filter((b) => Array.isArray(b) && b.length === 4);
  if (!list.length) return null;
  const x0 = Math.max(0, Math.min(...list.map((b) => b[0])) - pad);
  const y0 = Math.max(0, Math.min(...list.map((b) => b[1])) - pad);
  const x1 = Math.min(W, Math.max(...list.map((b) => b[2])) + pad);
  const y1 = Math.min(H, Math.max(...list.map((b) => b[3])) + pad);
  return x1 > x0 && y1 > y0 ? [x0, y0, x1, y1] : null;
}

/** 쪽의 판독 영역: 문제 쪽 = 답안 칸 셋, 2쪽 = 학년·이름·닉네임·필적 줄 */
export function readRegion(page) {
  const r = page?.regions || {};
  if (page?.kind === "item") return unionBox([r.s1, r.s2, r.s3], 6);
  if (page?.kind === "info") return unionBox(Object.entries(r).filter(([k]) => /^(grade|name|nickname|phrase_\d+)$/.test(k)).map(([, v]) => v), 6);
  return null;
}

/** 판독 영역 안에서 각 칸의 상대 위치(0~1) — 모델에게 "어느 칸이 어디" 를 알려 줄 때 */
export function relBoxes(page) {
  const reg = readRegion(page);
  if (!reg) return {};
  const [X0, Y0, X1, Y1] = reg;
  const w = X1 - X0, h = Y1 - Y0;
  const out = {};
  for (const [k, b] of Object.entries(page.regions || {})) {
    if (!Array.isArray(b) || k === "q") continue;
    out[k] = { x: +((b[0] - X0) / w).toFixed(3), y: +((b[1] - Y0) / h).toFixed(3), w: +((b[2] - b[0]) / w).toFixed(3), h: +((b[3] - b[1]) / h).toFixed(3) };
  }
  return out;
}
