// 컨셉 문제 OMR 테스트용 합성 사진 — 카드 좌표(1000×1478)의 흑백 래스터에 인쇄 · 연필을 그리고,
// 원근 · 조명 · 잡음 · 흐림 · 그림자를 얹어 휴대폰 사진처럼 만든다. (conceptsets · conceptsets-lin 테스트가 함께 쓴다)
import { homography, applyH, invertH } from "../../src/lib/omr/detect.js";

export function raster(w, h, v) { return { w, h, px: new Float32Array(w * h).fill(v) }; }
export function fillRect(r, x, y, w, h, v) {
  for (let j = Math.max(0, Math.floor(y)); j < Math.min(r.h, Math.ceil(y + h)); j++)
    for (let i = Math.max(0, Math.floor(x)); i < Math.min(r.w, Math.ceil(x + w)); i++) r.px[j * r.w + i] = v;
}
export function fillCircle(r, cx, cy, rad, v) {
  for (let j = Math.max(0, Math.floor(cy - rad)); j <= Math.min(r.h - 1, Math.ceil(cy + rad)); j++)
    for (let i = Math.max(0, Math.floor(cx - rad)); i <= Math.min(r.w - 1, Math.ceil(cx + rad)); i++) {
      const dx = i + 0.5 - cx, dy = j + 0.5 - cy;
      if (dx * dx + dy * dy <= rad * rad) r.px[j * r.w + i] = Math.min(r.px[j * r.w + i], v);
    }
}
export function ring(r, cx, cy, rad, width, v) {
  const a = (rad - width / 2) ** 2, b = (rad + width / 2) ** 2;
  for (let j = Math.max(0, Math.floor(cy - rad - width)); j <= Math.min(r.h - 1, Math.ceil(cy + rad + width)); j++)
    for (let i = Math.max(0, Math.floor(cx - rad - width)); i <= Math.min(r.w - 1, Math.ceil(cx + rad + width)); i++) {
      const dx = i + 0.5 - cx, dy = j + 0.5 - cy, d = dx * dx + dy * dy;
      if (d >= a && d <= b) r.px[j * r.w + i] = Math.min(r.px[j * r.w + i], v);
    }
}
export function strokeRect(r, x, y, w, h, lw, v) { fillRect(r, x, y, w, lw, v); fillRect(r, x, y + h - lw, w, lw, v); fillRect(r, x, y, lw, h, v); fillRect(r, x + w - lw, y, lw, h, v); }
/** 굵기 lw 의 선분 (연필 획) */
export function seg(r, x0, y0, x1, y1, lw, v) {
  const n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / 0.7));
  for (let k = 0; k <= n; k++) fillCircle(r, x0 + ((x1 - x0) * k) / n, y0 + ((y1 - y0) * k) / n, lw / 2, v);
}
// 손글씨 숫자 흉내 — 7획 표시기 꼴을 살짝 기울여
export const SEG7 = { 0: "abcdef", 1: "bc", 2: "abged", 3: "abgcd", 4: "fgbc", 5: "afgcd", 6: "afgedc", 7: "abc", 8: "abcdefg", 9: "abcdfg" };
export function handText(r, rect, text, v = 58) {
  const ch = String(text).split(""), H = rect.h * 0.52, W = Math.min(rect.w * 0.8 / ch.length, H * 0.62) * 0.8;
  const x0 = rect.x + (rect.w - ch.length * W * 1.25) / 2, y0 = rect.y + (rect.h - H) / 2, sl = 0.12;
  ch.forEach((c, i) => {
    const L = x0 + i * W * 1.25, P = { tl: [L, y0], tr: [L + W, y0], ml: [L, y0 + H / 2], mr: [L + W, y0 + H / 2], bl: [L, y0 + H], br: [L + W, y0 + H] };
    const sk = ([x, y]) => [x + (y0 + H - y) * sl, y];
    const S = { a: ["tl", "tr"], b: ["tr", "mr"], c: ["mr", "br"], d: ["bl", "br"], e: ["ml", "bl"], f: ["tl", "ml"], g: ["ml", "mr"] };
    for (const s of SEG7[c] || "") { const [p, q] = S[s].map((k) => sk(P[k])); seg(r, p[0], p[1], q[0], q[1], 3, v); }
    for (const [u0, v0, u1, v1] of MARKS[c] || []) {          // 기호(− + / . x y ( ) , =) — 칸 안 상대 좌표(0~1)
      const p = sk([L + u0 * W, y0 + v0 * H]), q = sk([L + u1 * W, y0 + v1 * H]);
      seg(r, p[0], p[1], q[0], q[1], 3, v);
    }
  });
}
// 일차함수 답(−3 · 3/4 · 0.5 · −2x+3 · (2,−1))의 기호 획 — 판독은 글씨 유무만 보므로 모양은 대강
const MARKS = {
  "-": [[0.1, 0.5, 0.9, 0.5]], "−": [[0.1, 0.5, 0.9, 0.5]], "+": [[0.1, 0.5, 0.9, 0.5], [0.5, 0.2, 0.5, 0.8]],
  "/": [[0.9, 0.05, 0.1, 0.95]], ".": [[0.45, 0.92, 0.55, 0.95]], ",": [[0.55, 0.85, 0.4, 1.05]], "=": [[0.1, 0.38, 0.9, 0.38], [0.1, 0.66, 0.9, 0.66]],
  x: [[0.1, 0.35, 0.9, 1], [0.9, 0.35, 0.1, 1]], y: [[0.1, 0.35, 0.5, 0.7], [0.9, 0.35, 0.3, 1.1]],
  "(": [[0.7, 0, 0.35, 0.5], [0.35, 0.5, 0.7, 1]], ")": [[0.3, 0, 0.65, 0.5], [0.65, 0.5, 0.3, 1]],
};
export function sampleBilinear(r, x, y) {
  x = Math.max(0, Math.min(r.w - 1.001, x)); y = Math.max(0, Math.min(r.h - 1.001, y));
  const x0 = x | 0, y0 = y | 0, fx = x - x0, fy = y - y0, i = y0 * r.w + x0;
  const top = r.px[i] * (1 - fx) + r.px[i + 1] * fx, bot = r.px[i + r.w] * (1 - fx) + r.px[i + r.w + 1] * fx;
  return top * (1 - fy) + bot * fy;
}
export function prng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

/** 원근 · 조명 · 잡음 · 흐림을 얹은 "사진". shadow: 이미지 좌표 y ≈ shadow 아래를 38% 어둡게(조금 기운 그림자 경계, 반그림자 40px) */
export function photograph(card, W, H, quad, seed = 1, table = 100, shadow = null) {
  const Hc2i = homography([[0, 0], [card.w, 0], [card.w, card.h], [0, card.h]], quad);
  const Hi2c = invertH(Hc2i);
  const rnd = prng(seed);
  const g = new Float32Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const [cx, cy] = applyH(Hi2c, x + 0.5, y + 0.5);
    let v = table;
    if (cx >= 0 && cy >= 0 && cx < card.w && cy < card.h) v = sampleBilinear(card, cx, cy);
    v *= 0.74 + 0.3 * (x / W) - 0.08 * (y / H);
    if (shadow != null) { const t = (y - shadow - (x - W / 2) * 0.15) / 40; v *= 1 - 0.38 * Math.max(0, Math.min(1, t)); }   // 반그림자 40px
    g[y * W + x] = v + (rnd() - 0.5) * 14;
  }
  const b = new Float32Array(W * H);
  for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
    let s = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) s += g[(y + dy) * W + x + dx];
    b[y * W + x] = s / 9;
  }
  const data = new Uint8ClampedArray(W * H * 4);
  for (let i = 0; i < W * H; i++) { const v = Math.max(0, Math.min(255, Math.round(b[i]))); data[i * 4] = v; data[i * 4 + 1] = v; data[i * 4 + 2] = v; data[i * 4 + 3] = 255; }
  return { width: W, height: H, data };
}
