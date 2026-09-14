// ashrain.out — 사진 OMR: 순수 이미지 분석 (DOM 없음 — node 테스트 가능)
//
// 입력은 { width, height, data: Uint8ClampedArray(RGBA) } (canvas getImageData 결과) 또는 { width, height, gray: Uint8Array }.
// 흐름: 회색조 → 국소 평균 이진화 → 네 모서리 영역에서 정사각 blob(마커) 탐색 → 방향(0/90/180/270°) 판별
//      → 호모그래피(8자유도, 가우스 소거)로 캔버스 좌표계(sheet.js 의 1000×1414)로 역매핑(이중선형)
//      → 버블 안 어둡기 − 주변 종이 밝기 로 채움 비율 → 행마다 결정(선택 / blank / double).
// 원칙: 추측하지 않는다 — 애매하면 "" 로 두고 낮은 conf 로 표시해 학생이 확인 화면에서 고친다.

import { markerCenters } from "./sheet.js";

// ── 조정용 상수 ─────────────────────────────────────────────────────────────
export const FILL_MIN = 0.28;          // 이 이상 채워졌으면 "표시했다" (빈 버블은 라벨·테두리 번짐까지 ≈0.02~0.08)
export const MARGIN = 0.15;            // 1위·2위 차이가 이보다 작으면 double
export const CONF_OK = 0.5;            // 행 결정 신뢰 기준
export const CONFIDENCE_OK = 0.6;      // 카드 전체 — 이 미만이면 AI 보조 권장
export const MARKER_MIN_SIDE = 9;      // 마커 blob 최소 한 변(px)
export const MARKER_MAX_FRAC = 0.22;   // 마커 한 변 ≤ min(w,h)×이 값
export const CORNER_FRACS = [0.35, 0.5]; // 모서리 탐색 영역(이미지 폭·높이 비율) — 작으면 다음 값으로 재시도
export const ORIENT_MIN_CONTRAST = 45; // 방향 막대 판별 최소 대비(0~255)
export const INNER_R = 0.7;            // 버블 안쪽 표본 반지름 비율
export const RING_R = [1.3, 1.65];     // 종이 밝기 표본 고리(반지름 비율)

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

// ── 회색조 · 이진화 ────────────────────────────────────────────────────────
export function toGray(img) {
  if (img.gray) return img.gray;
  const { width: w, height: h, data } = img;
  const g = new Uint8Array(w * h);
  for (let i = 0, p = 0; i < g.length; i++, p += 4) g[i] = (data[p] * 77 + data[p + 1] * 150 + data[p + 2] * 29) >> 8;
  return g;
}

/** Otsu 전역 임계값 (참고용 — 카드의 잉크/종이 구분값) */
export function otsu(gray) {
  const hist = new Float64Array(256);
  for (let i = 0; i < gray.length; i++) hist[gray[i]]++;
  const total = gray.length;
  let sum = 0;
  for (let t = 0; t < 256; t++) sum += t * hist[t];
  let sumB = 0, wB = 0, best = 0, thr = 127;
  for (let t = 0; t < 256; t++) {
    wB += hist[t]; if (!wB) continue;
    const wF = total - wB; if (!wF) break;
    sumB += t * hist[t];
    const mB = sumB / wB, mF = (sum - sumB) / wF;
    const v = wB * wF * (mB - mF) * (mB - mF);
    if (v > best) { best = v; thr = t; }
  }
  return thr;
}

/**
 * 국소 평균 이진화 — 1 = 어두움(잉크). 창은 마커보다 커야 속이 비지 않는다 (기본 min(w,h)/8).
 * 종이의 그림자 기울기에 강하다 (전역 Otsu 는 그림자 쪽 종이를 통째로 어둡다고 본다).
 */
export function threshold(gray, w, h, { win, rel = 0.8, minGap = 10 } = {}) {
  const half = Math.max(8, Math.floor((win || Math.max(31, Math.round(Math.min(w, h) / 8))) / 2));
  const W1 = w + 1;
  const S = new Float64Array(W1 * (h + 1));
  for (let y = 1; y <= h; y++) {
    let rs = 0; const ro = y * W1, go = (y - 1) * w;
    for (let x = 1; x <= w; x++) { rs += gray[go + x - 1]; S[ro + x] = S[ro - W1 + x] + rs; }
  }
  const bin = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) {
    const y0 = Math.max(0, y - half), y1 = Math.min(h, y + half + 1);
    const r0 = y0 * W1, r1 = y1 * W1, go = y * w;
    for (let x = 0; x < w; x++) {
      const x0 = Math.max(0, x - half), x1 = Math.min(w, x + half + 1);
      const mean = (S[r1 + x1] - S[r0 + x1] - S[r1 + x0] + S[r0 + x0]) / ((y1 - y0) * (x1 - x0));
      const t = Math.min(mean * rel, mean - minGap);
      if (gray[go + x] < t) bin[go + x] = 1;
    }
  }
  return bin;
}

// ── 연결 요소 ───────────────────────────────────────────────────────────────
/**
 * rect 안의 어두운 연결 요소(4-연결). seen 은 호출자가 이미지 크기로 한 번 만들어 넘긴다.
 * 반환 [{ area, minX, minY, maxX, maxY, sumX, sumY, touches }] — touches: rect 경계에 닿음(잘린 blob)
 */
export function componentsInRect(bin, w, h, rect, seen, { minArea = 20, maxArea = Infinity } = {}) {
  const { x0, y0, x1, y1 } = rect;
  const out = [];
  const stack = [];
  for (let y = y0; y < y1; y++) {
    for (let x = x0; x < x1; x++) {
      const i = y * w + x;
      if (!bin[i] || seen[i]) continue;
      seen[i] = 1; stack.push(i);
      let area = 0, minX = x, maxX = x, minY = y, maxY = y, sumX = 0, sumY = 0, touches = false;
      while (stack.length) {
        const p = stack.pop();
        const px = p % w, py = (p - px) / w;
        area++; sumX += px; sumY += py;
        if (px < minX) minX = px; if (px > maxX) maxX = px; if (py < minY) minY = py; if (py > maxY) maxY = py;
        if (px === x0 || px === x1 - 1 || py === y0 || py === y1 - 1) touches = true;
        // 4-연결 이웃 (rect 안에서만)
        if (px > x0) { const q = p - 1; if (bin[q] && !seen[q]) { seen[q] = 1; stack.push(q); } }
        if (px < x1 - 1) { const q = p + 1; if (bin[q] && !seen[q]) { seen[q] = 1; stack.push(q); } }
        if (py > y0) { const q = p - w; if (bin[q] && !seen[q]) { seen[q] = 1; stack.push(q); } }
        if (py < y1 - 1) { const q = p + w; if (bin[q] && !seen[q]) { seen[q] = 1; stack.push(q); } }
      }
      if (area >= minArea && area <= maxArea) out.push({ area, minX, minY, maxX, maxY, sumX, sumY, touches });
    }
  }
  return out;
}

function isConvexQuad(p) {
  let sign = 0;
  for (let i = 0; i < 4; i++) {
    const a = p[i], b = p[(i + 1) % 4], c = p[(i + 2) % 4];
    const cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]);
    if (Math.abs(cr) < 1e-6) return false;
    const s = cr > 0 ? 1 : -1;
    if (sign && s !== sign) return false;
    sign = s;
  }
  return true;
}

/**
 * 네 모서리 마커 중심 — 이미지 사분면 순서 [TL, TR, BR, BL] (카드가 돌아가 찍혔으면 orientCorners 가 바로잡는다).
 * 각 모서리 영역에서 정사각·속찬 blob 후보를 뽑고, 크기가 서로 비슷하며 볼록 사각형을 이루는 조합을 고른다.
 * 못 찾으면 null.
 */
export function findMarkers(bin, w, h, opts = {}) {
  const fracs = opts.fracs || CORNER_FRACS;
  for (const f of fracs) {
    const r = findMarkersAt(bin, w, h, f, opts);
    if (r) return r;
  }
  return null;
}

function findMarkersAt(bin, w, h, frac, opts) {
  const rw = Math.round(w * frac), rh = Math.round(h * frac);
  const rects = [
    { x0: 0, y0: 0, x1: rw, y1: rh },
    { x0: w - rw, y0: 0, x1: w, y1: rh },
    { x0: w - rw, y0: h - rh, x1: w, y1: h },
    { x0: 0, y0: h - rh, x1: rw, y1: h },
  ];
  const corners = [[0, 0], [w, 0], [w, h], [0, h]];
  const minSide = opts.minSide || MARKER_MIN_SIDE;
  const maxSide = Math.min(w, h) * (opts.maxFrac || MARKER_MAX_FRAC);
  const diag = Math.hypot(w, h);
  const seen = new Uint8Array(w * h);
  const cands = rects.map((rect, ci) => {
    const blobs = componentsInRect(bin, w, h, rect, seen, { minArea: Math.floor(minSide * minSide * 0.5), maxArea: maxSide * maxSide * 1.5 });
    const out = [];
    for (const b of blobs) {
      if (b.touches) continue;
      const bw = b.maxX - b.minX + 1, bh = b.maxY - b.minY + 1;
      if (bw < minSide || bh < minSide || bw > maxSide || bh > maxSide) continue;
      const sq = Math.min(bw, bh) / Math.max(bw, bh);
      const fill = b.area / (bw * bh);
      if (sq < 0.5 || fill < 0.55) continue;
      const cx = b.sumX / b.area, cy = b.sumY / b.area;
      const d = Math.hypot(cx - corners[ci][0], cy - corners[ci][1]) / diag;
      out.push({ cx, cy, area: b.area, bw, bh, sq, fill, d, score: sq * fill + 0.35 * (1 - d) });
    }
    out.sort((a, b) => b.score - a.score);
    return out.slice(0, 5);
  });
  if (cands.some((c) => !c.length)) return null;
  let best = null;
  for (const a of cands[0]) for (const b of cands[1]) for (const c of cands[2]) for (const d of cands[3]) {
    const areas = [a.area, b.area, c.area, d.area];
    const ratio = Math.max(...areas) / Math.min(...areas);
    if (ratio > 6) continue;
    const pts = [[a.cx, a.cy], [b.cx, b.cy], [c.cx, c.cy], [d.cx, d.cy]];
    if (!isConvexQuad(pts)) continue;
    const s = a.score + b.score + c.score + d.score - 0.6 * Math.log(ratio);
    if (!best || s > best.s) best = { s, pts };
  }
  return best ? best.pts : null;
}

// ── 호모그래피 ──────────────────────────────────────────────────────────────
/** 8×8 가우스 소거 (부분 피벗) */
function solve8(A, b) {
  const n = 8;
  for (let c = 0; c < n; c++) {
    let piv = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[piv][c])) piv = r;
    if (Math.abs(A[piv][c]) < 1e-12) return null;
    if (piv !== c) { [A[c], A[piv]] = [A[piv], A[c]]; [b[c], b[piv]] = [b[piv], b[c]]; }
    for (let r = c + 1; r < n; r++) {
      const f = A[r][c] / A[c][c];
      if (!f) continue;
      for (let k = c; k < n; k++) A[r][k] -= f * A[c][k];
      b[r] -= f * b[c];
    }
  }
  const x = new Array(n).fill(0);
  for (let r = n - 1; r >= 0; r--) {
    let s = b[r];
    for (let k = r + 1; k < n; k++) s -= A[r][k] * x[k];
    x[r] = s / A[r][r];
  }
  return x;
}

/**
 * src 4점 → dst 4점 호모그래피 (3×3, 행 우선 Float64Array(9), h33 = 1). 퇴화하면 null.
 * 점은 [x, y]. 순서만 대응하면 된다.
 */
export function homography(src, dst) {
  const A = [], b = [];
  for (let i = 0; i < 4; i++) {
    const [x, y] = src[i], [u, v] = dst[i];
    A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u);
    A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v);
  }
  const s = solve8(A, b);
  if (!s) return null;
  return Float64Array.from([...s, 1]);
}

export function applyH(H, x, y) {
  const w = H[6] * x + H[7] * y + H[8];
  return [(H[0] * x + H[1] * y + H[2]) / w, (H[3] * x + H[4] * y + H[5]) / w];
}

/** 3×3 역행렬 (호모그래피 뒤집기) */
export function invertH(H) {
  const [a, b, c, d, e, f, g, h, i] = H;
  const A = e * i - f * h, B = -(d * i - f * g), C = d * h - e * g;
  const det = a * A + b * B + c * C;
  if (Math.abs(det) < 1e-12) return null;
  const inv = [A, -(b * i - c * h), b * f - c * e, B, a * i - c * g, -(a * f - c * d), C, -(a * h - b * g), a * e - b * d].map((v) => v / det);
  const k = inv[8] || 1;
  return Float64Array.from(inv.map((v) => v / k));
}

function sampleBilinear(gray, w, h, x, y) {
  if (x < 0) x = 0; else if (x > w - 1.001) x = w - 1.001;
  if (y < 0) y = 0; else if (y > h - 1.001) y = h - 1.001;
  const x0 = x | 0, y0 = y | 0, fx = x - x0, fy = y - y0;
  const i00 = y0 * w + x0, i10 = i00 + 1, i01 = i00 + w, i11 = i01 + 1;
  const top = gray[i00] * (1 - fx) + gray[i10] * fx;
  const bot = gray[i01] * (1 - fx) + gray[i11] * fx;
  return top * (1 - fy) + bot * fy;
}

/** 캔버스 좌표 직사각형(안쪽 20% 여유) 을 H 로 사영해 표본 평균 밝기 */
function meanRegion(gray, w, h, H, rx, ry, rw, rh) {
  const nx = Math.max(3, Math.round(rw / 4)), ny = Math.max(3, Math.round(rh / 4));
  let s = 0, n = 0;
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const cx = rx + rw * (0.2 + 0.6 * (i + 0.5) / nx), cy = ry + rh * (0.2 + 0.6 * (j + 0.5) / ny);
    const [x, y] = applyH(H, cx, cy);
    if (x < 0 || y < 0 || x > w - 1 || y > h - 1) continue;
    s += gray[(y | 0) * w + (x | 0)]; n++;
  }
  return n ? s / n : 255;
}

/**
 * 사분면 순서의 4점을 카드 기준 [TL, TR, BR, BL] 로 돌린다 — 방향 막대(TL 마커 오른쪽)가 어두운 회전을 고른다.
 * 반환 { corners, shift, contrast, H } 또는 null(막대가 어느 방향에서도 안 보임 → 마커 오검출 가능성).
 */
export function orientCorners(gray, w, h, quad, spec) {
  const centers = markerCenters(spec);
  const o = spec.orient;
  const rx = spec.W - o.x - o.w;    // 대칭 참조 위치(TR 마커 왼쪽) — 항상 빈 종이
  const tried = [];
  for (let s = 0; s < 4; s++) {
    const corners = [0, 1, 2, 3].map((i) => quad[(i + s) % 4]);
    const H = homography(centers, corners);
    if (!H) continue;
    const dark = meanRegion(gray, w, h, H, o.x, o.y, o.w, o.h);
    const ref = meanRegion(gray, w, h, H, rx, o.y, o.w, o.h);
    tried.push({ corners, shift: s, contrast: ref - dark, H });
  }
  if (!tried.length) return null;
  tried.sort((a, b) => b.contrast - a.contrast);
  const best = tried[0], second = tried[1]?.contrast ?? -Infinity;
  if (best.contrast < ORIENT_MIN_CONTRAST || best.contrast < 2 * Math.max(second, 1)) return null;
  return best;
}

/**
 * 카드 캔버스 좌표계로 역매핑한 회색조 래스터 (scale 배: 기본 500×707).
 * corners: 이미지 좌표 [TL, TR, BR, BL] 마커 중심. 반환 { width, height, gray, scale, H(캔버스→이미지) }
 */
export function warpToSpec(gray, w, h, corners, spec, scale = 0.5) {
  const W = Math.round(spec.W * scale), Hh = Math.round(spec.H * scale);
  const H = homography(markerCenters(spec), corners);
  if (!H) return null;
  const out = new Uint8Array(W * Hh);
  for (let j = 0; j < Hh; j++) {
    const cy = (j + 0.5) / scale;
    for (let i = 0; i < W; i++) {
      const cx = (i + 0.5) / scale;
      const [x, y] = applyH(H, cx, cy);
      out[j * W + i] = sampleBilinear(gray, w, h, x, y) + 0.5;
    }
  }
  return { width: W, height: Hh, gray: out, scale, H };
}

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
 * 고리(r0~r1) 픽셀의 p-분위수 — 버블 주변 "종이" 밝기. 평균 대신 상위 분위수를 쓰는 이유:
 * 삐져나온 연필 자국은 고리 일부만 어둡게 하므로(무시돼야 함) 70% 분위수엔 거의 안 잡히고,
 * 그림자는 고리 전체를 어둡게 하므로(반영돼야 함) 그대로 따라간다.
 */
function ringStats(g, W, H, cx, cy, r0, r1) {
  const vals = [];
  const a = r0 * r0, b = r1 * r1;
  for (let y = Math.max(0, Math.floor(cy - r1)); y <= Math.min(H - 1, Math.ceil(cy + r1)); y++)
    for (let x = Math.max(0, Math.floor(cx - r1)); x <= Math.min(W - 1, Math.ceil(cx + r1)); x++) {
      const dx = x + 0.5 - cx, dy = y + 0.5 - cy, d = dx * dx + dy * dy;
      if (d >= a && d <= b) vals.push(g[y * W + x]);
    }
  if (!vals.length) return { bg: 255, spread: 0 };
  vals.sort((x, y) => x - y);
  const q = (p) => vals[Math.min(vals.length - 1, Math.floor(vals.length * p))];
  const p70 = q(0.7);
  return { bg: p70, spread: p70 - q(0.3) };   // spread 가 크면 고리가 고르지 않다 (그림자 경계·큰 번짐)
}
const median = (arr) => { const a = arr.slice().sort((x, y) => x - y); const m = a.length >> 1; return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2; };

/** 잉크 밝기 — 워프된 래스터에서 마커 속 평균 (중앙값) */
export function inkLevel(warped, spec) {
  const { gray: g, width: W, height: H, scale } = warped;
  const vals = spec.markers.map((m) => meanDisk(g, W, H, (m.x + m.size / 2) * scale, (m.y + m.size / 2) * scale, m.size * scale * 0.3));
  return median(vals);
}

/**
 * 행마다 버블 채움 비율과 결정.
 * 반환 [{ no, kind, answer, conf, flag, fills, bg }] — flag: null | "blank" | "double" | "weak"(2위도 표시 기준 넘음) | "manual"(단답)
 */
export function readBubbles(warped, spec, scale = warped.scale || 0.5) {
  const { gray: g, width: W, height: H } = warped;
  const ink = inkLevel(warped, spec);
  const rows = [];
  for (const r of spec.rows) {
    if (!r.bubbles) { rows.push({ no: r.no, kind: "short", answer: "", conf: 0, flag: "manual", fills: null, bg: null }); continue; }
    const inside = r.bubbles.map((b) => meanDisk(g, W, H, b.x * scale, b.y * scale, b.r * scale * INNER_R));
    // 버블마다 제 주변 종이 밝기를 기준으로 — 행의 일부만 그림자에 들어가도 그쪽 버블이 "칠한 것"으로 보이지 않게
    const ring = r.bubbles.map((b) => ringStats(g, W, H, b.x * scale, b.y * scale, b.r * scale * RING_R[0], b.r * scale * RING_R[1]));
    const bg = median(ring.map((s) => s.bg));
    const fills = inside.map((v, k) => clamp01((ring[k].bg - v) / Math.max(ring[k].bg - ink, 40)));
    const order = fills.map((f, i) => i).sort((a, b) => fills[b] - fills[a]);
    const max = fills[order[0]], second = fills[order[1]] ?? 0;
    let answer = "", flag = null, conf = 0;
    if (max >= FILL_MIN) {
      if (second >= FILL_MIN && max - second < MARGIN) { flag = "double"; }
      else {
        answer = r.bubbles[order[0]].label;
        conf = clamp01(Math.min((max - FILL_MIN) / 0.15, (max - second) / (2 * MARGIN)));
        if (second >= FILL_MIN) flag = "weak";
        // 고른 버블 주변이 고르지 않으면(그림자 경계가 버블을 가로지름 등) 반만 믿는다
        const k = order[0];
        if (ring[k].spread > 0.25 * Math.max(ring[k].bg - ink, 40)) { conf = Math.min(conf * 0.4, CONF_OK - 0.05); flag = flag || "uneven"; }
      }
    } else {
      flag = "blank";
      conf = clamp01((FILL_MIN - max) / FILL_MIN);
    }
    rows.push({ no: r.no, kind: "choice", answer, conf: Math.round(conf * 100) / 100, flag, fills: fills.map((f) => Math.round(f * 100) / 100), bg: Math.round(bg) });
  }
  return rows;
}

/**
 * 확인 화면 행 만들기 — CV 결과와 AI 결과를 합친다.
 *   items: 세트 문항 [{ no, kind, q? }]  ·  cv: readSheet 결과(또는 null)  ·  ai: [{ no, answer }](또는 null)  ·  prev: 이전 행(학생이 고친 행은 그대로 둔다)
 * 규칙: 객관식은 CV 가 확신(conf ≥ CONF_OK)하면 CV, 아니면 AI(①~⑤ 꼴일 때만), 그것도 없으면 CV 의 낮은 답.
 *       단답은 기계로 읽지 않는다 — AI 답이 있으면 채워 주고(확인 필요), 없으면 빈칸.
 * 행: { no, kind, q, answer, conf, flag, src:"cv"|"ai"|"none"|"me", edited }
 */
export function mergeAnswers(items, cv, ai, prev) {
  const LABELS = ["①", "②", "③", "④", "⑤"];
  return (items || []).map((it) => {
    const p = prev?.find((x) => x.no === it.no);
    if (p?.edited) return p;
    const c = cv?.ok ? cv.answers.find((a) => a.no === it.no) : null;
    const a = ai?.find((x) => x.no === it.no);
    let answer = "", src = "none", conf = 0, flag = c?.flag || null;
    if (it.kind === "choice") {
      if (c && c.conf >= CONF_OK) { answer = c.answer; conf = c.conf; src = "cv"; }
      else if (a && LABELS.includes(String(a.answer).trim())) { answer = String(a.answer).trim(); conf = 0.6; src = "ai"; }
      else if (c) { answer = c.answer; conf = c.conf; src = "cv"; }
    } else {
      flag = "manual";
      if (a && String(a.answer ?? "").trim()) { answer = String(a.answer).trim(); conf = 0.6; src = "ai"; }
    }
    return { no: it.no, kind: it.kind === "short" ? "short" : "choice", q: it.q || "", answer, conf, flag, src, edited: false };
  });
}

export function blankAnswers(spec) {
  return spec.rows.map((r) => ({ no: r.no, kind: r.kind, answer: "", conf: 0, flag: r.kind === "choice" ? "unread" : "manual", fills: null, bg: null }));
}

/**
 * 사진 한 장 → 답.  { ok, reason?, corners, orientation, answers, confidence, nMarked, warped, path:"cv" }
 * ok=false 면 answers 는 모두 "" (호출자는 AI 보조로 넘어간다).
 */
export function readSheet(img, spec, opts = {}) {
  const w = img.width, h = img.height;
  const gray = toGray(img);
  const bin = threshold(gray, w, h, opts.threshold);
  const quad = findMarkers(bin, w, h, opts);
  const fail = (reason, corners) => ({ ok: false, reason, corners: corners || null, orientation: null, answers: blankAnswers(spec), confidence: 0, nMarked: 0, warped: null, path: "cv" });
  if (!quad) return fail("markers");
  const o = orientCorners(gray, w, h, quad, spec);
  if (!o) return fail("orient", quad);
  const scale = opts.scale || 0.5;
  const warped = warpToSpec(gray, w, h, o.corners, spec, scale);
  if (!warped) return fail("warp", o.corners);
  const answers = readBubbles(warped, spec, scale);
  const choice = answers.filter((a) => a.kind === "choice");
  const confident = choice.filter((a) => a.conf >= CONF_OK).length;
  const confidence = choice.length ? Math.round((confident / choice.length) * 100) / 100 : 1;
  const nMarked = choice.filter((a) => a.answer).length;
  return { ok: true, reason: null, corners: o.corners, orientation: o.shift, answers, confidence, nMarked, warped, path: "cv" };
}
