// ashrain.out — 컨셉 문제 OMR 카드(v2)의 분수 손글씨 칸 → AI 판독용 묶음 이미지
// grid.handCrops 가 사진에서 잘라 밝기를 편 조각(분자 칸 · 분모 칸)을 번호 붙은 칸에 모은다.
//   분자 위 · 굵은 분수 막대 · 분모 아래로 다시 그려 AI 가 「5/12」처럼 읽게 하고, 분모 칸이 비었으면(0 · 1) 분자만 둔다.
//   사진 전체는 보내지 않는다 — 이 조각들만 /api/ai(task "omr")로 간다(recognize.readSheets).

const LAB = 34, PAD = 12, BAR = 26, GAP = 10, MAX_EDGE = 1568;

function grayCanvas(doc, crop) {
  const cv = doc.createElement("canvas");
  cv.width = crop.width; cv.height = crop.height;
  const ctx = cv.getContext("2d");
  const im = ctx.createImageData(crop.width, crop.height);
  for (let i = 0; i < crop.gray.length; i++) {
    const v = crop.gray[i];
    im.data[i * 4] = v; im.data[i * 4 + 1] = v; im.data[i * 4 + 2] = v; im.data[i * 4 + 3] = 255;
  }
  ctx.putImageData(im, 0, 0);
  return cv;
}

/**
 * crops: [{ no, num:{width,height,gray}, den|null }] → [{ canvas, nos }]
 * 한 장에 최대 per 칸(cols 열). 긴 변이 1568px 를 넘으면 줄인다.
 */
export function handSheets(crops, { per = 12, cols: colsMax = 6, scale = 1.6, doc = typeof document !== "undefined" ? document : null } = {}) {
  if (!doc || !crops.length) return [];
  const out = [];
  const cw = Math.max(...crops.map((c) => c.num.width)), chh = Math.max(...crops.map((c) => c.num.height));
  const boxW = Math.round(cw * scale), boxH = Math.round(chh * scale);
  const CW = boxW + 2 * PAD, CH = LAB + boxH + BAR + boxH + PAD;
  for (let s = 0; s < crops.length; s += per) {
    const chunk = crops.slice(s, s + per);
    const cols = Math.max(1, Math.min(colsMax, chunk.length));
    const rows = Math.ceil(chunk.length / cols);
    const W = GAP + cols * (CW + GAP), H = GAP + rows * (CH + GAP);
    const k = Math.min(1, MAX_EDGE / Math.max(W, H));
    const cv = doc.createElement("canvas");
    cv.width = Math.round(W * k); cv.height = Math.round(H * k);
    const ctx = cv.getContext("2d");
    ctx.scale(k, k);
    ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H);
    ctx.imageSmoothingEnabled = true;
    chunk.forEach((c, i) => {
      const x = GAP + (i % cols) * (CW + GAP), y = GAP + Math.floor(i / cols) * (CH + GAP);
      ctx.strokeStyle = "#c8c8c8"; ctx.lineWidth = 1.5; ctx.strokeRect(x + 0.5, y + 0.5, CW - 1, CH - 1);
      ctx.fillStyle = "#111"; ctx.font = "bold 22px sans-serif"; ctx.textBaseline = "top";
      ctx.fillText(`${c.no}번`, x + 10, y + 7);
      const ny = y + LAB;
      ctx.drawImage(grayCanvas(doc, c.num), x + PAD, ny, boxW, boxH);
      if (c.den) {
        const by = ny + boxH + BAR / 2;
        ctx.strokeStyle = "#000"; ctx.lineWidth = 5; ctx.lineCap = "round";
        ctx.beginPath(); ctx.moveTo(x + PAD + 10, by); ctx.lineTo(x + PAD + boxW - 10, by); ctx.stroke();
        ctx.drawImage(grayCanvas(doc, c.den), x + PAD, ny + boxH + BAR, boxW, boxH);
      }
    });
    out.push({ canvas: cv, nos: chunk.map((c) => c.no) });
  }
  return out;
}
