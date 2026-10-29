// ashrain.out — 컨셉 문제 「종이처럼 풀기」: 손글씨(획) 데이터 · SVG · 판독용 묶음 이미지
//
// 손글씨 답 = { k:"ink", lay:"int"|"frac"|"pair", w, h, s:[[x0,y0,x1,y1,…],…], wd:[굵기,…] }
//   좌표는 입력판(InkPad) 논리 px, 정수. 분수 판은 가운데 가로선(y = h/2) 위가 분자 · 아래가 분모, 두 수 판은 가운데 세로선 왼쪽 · 오른쪽.
// 화면(문제지 괄호)에는 SVG 로, 판독(/api/ai task "omr")에는 번호를 붙인 칸들을 한 장(JPEG)에 모아 보낸다.

export const INK_COLOR = "#2c3138";          // 연필 흑연색
export const PAD_H = { int: 150, frac: 230, pair: 150 };

const r1 = (v) => Math.round(v * 10) / 10;

/** 획이 하나라도 있는지 */
export function hasInk(ink) {
  return !!(ink && Array.isArray(ink.s) && ink.s.some((st) => Array.isArray(st) && st.length >= 2));
}

/** 획들의 경계 상자 { x0, y0, x1, y1 } (없으면 null) */
export function inkBox(ink) {
  if (!hasInk(ink)) return null;
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const st of ink.s) for (let i = 0; i + 1 < st.length; i += 2) {
    const x = st[i], y = st[i + 1];
    if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
  }
  return { x0, y0, x1, y1 };
}

/** 분수 판에서 가로선 아래에도 글씨가 있나(= 분모를 썼나) */
export function hasDenominator(ink) {
  if (!hasInk(ink) || ink.lay !== "frac") return false;
  const mid = ink.h / 2;
  return ink.s.some((st) => { for (let i = 1; i < st.length; i += 2) if (st[i] > mid + 4) return true; return false; });
}

/** 한 획 → 부드러운 SVG 경로 (중점을 잇는 2차 곡선) */
export function strokePath(st, sx = 1, sy = 1, ox = 0, oy = 0) {
  const n = Math.floor(st.length / 2);
  if (!n) return "";
  const X = (i) => r1((st[2 * i] - ox) * sx), Y = (i) => r1((st[2 * i + 1] - oy) * sy);
  if (n === 1) return `M${X(0)} ${Y(0)}l0.01 0`;                 // 점
  let d = `M${X(0)} ${Y(0)}`;
  for (let i = 1; i < n - 1; i++) d += `Q${X(i)} ${Y(i)} ${r1((X(i) + X(i + 1)) / 2)} ${r1((Y(i) + Y(i + 1)) / 2)}`;
  return d + `L${X(n - 1)} ${Y(n - 1)}`;
}

/**
 * 손글씨 → SVG 문자열. 글씨가 있는 부분만 잘라(여백 pad) 비율을 지킨다.
 * opts: { color, width(굵기 배율), cls, frac(분수 가로선 그리기, 기본 자동) }
 */
export function inkSvg(ink, opts = {}) {
  const b = inkBox(ink);
  if (!b) return "";
  const color = opts.color || INK_COLOR;
  const pad = 6;
  let { x0, y0, x1, y1 } = b;
  const bar = (opts.frac ?? true) && ink.lay === "frac" && hasDenominator(ink);
  if (bar) { y0 = Math.min(y0, ink.h / 2 - 2); y1 = Math.max(y1, ink.h / 2 + 2); }
  x0 -= pad; y0 -= pad; x1 += pad; y1 += pad;
  const w = Math.max(1, x1 - x0), h = Math.max(1, y1 - y0);
  const k = opts.width || 1;
  const paths = ink.s.map((st, i) => `<path d="${strokePath(st, 1, 1, x0, y0)}" stroke-width="${r1((ink.wd?.[i] || 3) * k)}"/>`).join("");
  const line = bar ? `<line x1="${r1(b.x0 - x0 - 2)}" y1="${r1(ink.h / 2 - y0)}" x2="${r1(b.x1 - x0 + 2)}" y2="${r1(ink.h / 2 - y0)}" stroke-width="${r1(2.4 * k)}"/>` : "";
  return `<svg class="${opts.cls || "cs-ink"}" viewBox="0 0 ${r1(w)} ${r1(h)}" data-w="${r1(w)}" data-h="${r1(h)}" xmlns="http://www.w3.org/2000/svg" `
    + `fill="none" stroke="${color}" stroke-linecap="round" stroke-linejoin="round">${line}${paths}</svg>`;
}

/** 캔버스에 손글씨 그리기 (판 좌표 → 캔버스 변환 sx · ox …) */
export function drawInk(ctx, ink, { sx = 1, sy = sx, ox = 0, oy = 0, dx = 0, dy = 0, color = "#000", k = 1, bar = true } = {}) {
  if (!hasInk(ink)) return;
  ctx.save();
  ctx.strokeStyle = color; ctx.lineCap = "round"; ctx.lineJoin = "round";
  const P = (x, y) => [dx + (x - ox) * sx, dy + (y - oy) * sy];
  ink.s.forEach((st, i) => {
    const n = Math.floor(st.length / 2);
    if (!n) return;
    ctx.lineWidth = Math.max(1.2, (ink.wd?.[i] || 3) * k);
    ctx.beginPath();
    const [ax, ay] = P(st[0], st[1]);
    ctx.moveTo(ax, ay);
    if (n === 1) ctx.lineTo(ax + 0.01, ay);
    for (let j = 1; j < n - 1; j++) {
      const [cx, cy] = P(st[2 * j], st[2 * j + 1]);
      const [nx, ny] = P(st[2 * j + 2], st[2 * j + 3]);
      ctx.quadraticCurveTo(cx, cy, (cx + nx) / 2, (cy + ny) / 2);
    }
    if (n > 1) { const [ex, ey] = P(st[2 * (n - 1)], st[2 * (n - 1) + 1]); ctx.lineTo(ex, ey); }
    ctx.stroke();
  });
  if (bar && ink.lay === "frac" && hasDenominator(ink)) {
    const b = inkBox(ink);
    const [lx, ly] = P(b.x0 - 4, ink.h / 2), [rx] = P(b.x1 + 4, ink.h / 2);
    ctx.lineWidth = Math.max(1.6, 2.6 * k);
    ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(rx, ly); ctx.stroke();
  }
  ctx.restore();
}

/**
 * 판독용 묶음 이미지 — 손글씨 답 여럿을 번호 붙은 칸에 모은다(칸마다 글씨를 잘라 크게).
 * entries: [{ no, ink }] → [{ canvas, nos }] (한 장에 최대 per 칸, 이미지 긴 변이 1568px 를 넘지 않게)
 * doc: 캔버스를 만들 document (테스트 · 다른 창)
 */
export function inkSheets(entries, { per = 24, cols: colsMax = 4, doc = typeof document !== "undefined" ? document : null } = {}) {
  if (!doc) return [];
  const CW = 340, CH = { int: 130, pair: 130, frac: 190 }, LAB = 34, GAP = 10;
  const out = [];
  for (let s = 0; s < entries.length; s += per) {
    let cols = colsMax;
    const chunk = entries.slice(s, s + per);
    cols = Math.max(1, Math.min(cols, chunk.length));           // 몇 개 안 되면 열을 줄여 이미지를 작게
    const rows = [];
    for (let i = 0; i < chunk.length; i += cols) rows.push(chunk.slice(i, i + cols));
    const rowH = rows.map((r) => Math.max(...r.map((e) => CH[e.ink.lay] || 130)) + LAB);
    const W = GAP + cols * (CW + GAP), H = GAP + rowH.reduce((a, h) => a + h + GAP, 0);
    const cv = doc.createElement("canvas");
    cv.width = W; cv.height = H;
    const ctx = cv.getContext("2d");
    ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H);
    let y = GAP;
    rows.forEach((r, ri) => {
      r.forEach((e, ci) => {
        const x = GAP + ci * (CW + GAP);
        ctx.strokeStyle = "#c8c8c8"; ctx.lineWidth = 1.5; ctx.strokeRect(x + 0.5, y + 0.5, CW - 1, rowH[ri] - 1);
        ctx.fillStyle = "#111"; ctx.font = "bold 22px sans-serif"; ctx.textBaseline = "top";
        ctx.fillText(`${e.no}번`, x + 10, y + 7);
        const b = inkBox(e.ink);
        if (!b) return;
        const bar = e.ink.lay === "frac" && hasDenominator(e.ink);
        let { x0, y0, x1, y1 } = b;
        if (bar) { y0 = Math.min(y0, e.ink.h / 2 - 2); y1 = Math.max(y1, e.ink.h / 2 + 2); }
        const bw = Math.max(20, x1 - x0), bh = Math.max(20, y1 - y0);
        const boxW = CW - 40, boxH = rowH[ri] - LAB - 18;
        const sc = Math.min(boxW / bw, boxH / bh, 2.2);
        const dx = x + 20 + (boxW - bw * sc) / 2, dy = y + LAB + 6 + (boxH - bh * sc) / 2;
        drawInk(ctx, e.ink, { sx: sc, ox: x0, oy: y0, dx, dy, color: "#000", k: Math.max(1, Math.min(1.6, sc)) });
        if (e.ink.lay === "pair") {                               // 두 수 사이 구분
          const mx = dx + (e.ink.w / 2 - x0) * sc;
          ctx.fillStyle = "#000"; ctx.font = "bold 30px sans-serif"; ctx.fillText(",", mx - 4, dy + bh * sc * 0.45);
        }
      });
      y += rowH[ri] + GAP;
    });
    out.push({ canvas: cv, nos: chunk.map((e) => e.no) });
  }
  return out;
}

/** 판독 글자 정리 — "5 / 12" → "5/12", 유니코드 빼기 · 전각 숫자 등 */
export function normalizeRead(text) {
  let t = String(text ?? "").normalize("NFKC").trim();
  t = t.replace(/[−–—]/g, "-").replace(/\s*\/\s*/g, "/").replace(/\s*,\s*/g, ", ").replace(/\s*\|\s*/g, ", ");
  t = t.replace(/^답\s*[:：]?\s*/, "").replace(/[()（）]/g, "").trim();
  return t;
}
