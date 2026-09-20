// ashrain.out — 촬영 모듈 공용: 사진 파일 → 캔버스(축소) → 영역 자르기 → JPEG base64
// 사진은 서버에 올리지 않는다(Storage 업로드 없음). 서버로는 인식에 필요한 JPEG base64 만 보내고, 응답 뒤 버린다.

export const MAX_SIDE = 1600;   // 긴 변 기준 축소 (문항 글씨 인식에 충분, 4G 에서 1~2초)

/** File → HTMLImageElement */
export function loadImage(file) {
  return new Promise((resolve, reject) => {
    const im = new Image();
    im.onload = () => resolve(im);
    im.onerror = () => reject(new Error("사진을 열 수 없어요"));
    im.src = URL.createObjectURL(file);
  });
}

/** 이미지 → 축소 캔버스 */
export function toCanvas(im, maxSide = MAX_SIDE) {
  const sc = Math.min(1, maxSide / Math.max(im.width, im.height));
  const cv = document.createElement("canvas");
  cv.width = Math.max(1, Math.round(im.width * sc));
  cv.height = Math.max(1, Math.round(im.height * sc));
  cv.getContext("2d").drawImage(im, 0, 0, cv.width, cv.height);
  try { URL.revokeObjectURL(im.src); } catch { /* data: URL 이면 무시 */ }
  return cv;
}

/** 파일을 골라 바로 캔버스로 */
export async function fileToCanvas(file, maxSide = MAX_SIDE) {
  return toCanvas(await loadImage(file), maxSide);
}

/** 비율 좌표 상자 {x,y,w,h} (0~1) 를 0~1 안으로 정리 */
export function clampBox(b) {
  if (!b) return null;
  const x = Math.min(Math.max(+b.x || 0, 0), 1), y = Math.min(Math.max(+b.y || 0, 0), 1);
  const w = Math.min(Math.max(+b.w || 0, 0), 1 - x), h = Math.min(Math.max(+b.h || 0, 0), 1 - y);
  if (w < 0.02 || h < 0.02) return null;
  return { x, y, w, h };
}

/** 캔버스에서 비율 상자만큼 잘라 새 캔버스로 (여백 pad: 비율) */
export function cropCanvas(cv, box, pad = 0.01) {
  const b = clampBox(box);
  if (!b) return cv;
  const x0 = Math.max(0, Math.floor((b.x - pad) * cv.width)), y0 = Math.max(0, Math.floor((b.y - pad) * cv.height));
  const x1 = Math.min(cv.width, Math.ceil((b.x + b.w + pad) * cv.width)), y1 = Math.min(cv.height, Math.ceil((b.y + b.h + pad) * cv.height));
  const out = document.createElement("canvas");
  out.width = Math.max(1, x1 - x0); out.height = Math.max(1, y1 - y0);
  out.getContext("2d").drawImage(cv, x0, y0, out.width, out.height, 0, 0, out.width, out.height);
  return out;
}

/** 캔버스 → JPEG base64 (data: 접두 없이) */
export function canvasToBase64(cv, quality = 0.85) {
  return cv.toDataURL("image/jpeg", quality).split(",")[1];
}
export const canvasToDataUrl = (cv, quality = 0.85) => cv.toDataURL("image/jpeg", quality);

/** 손가락 드래그로 잡은 화면 좌표 두 점 → 비율 상자 */
export function boxFromPoints(p0, p1, w, h) {
  if (!w || !h) return null;
  const x = Math.min(p0.x, p1.x) / w, y = Math.min(p0.y, p1.y) / h;
  return clampBox({ x, y, w: Math.abs(p1.x - p0.x) / w, h: Math.abs(p1.y - p0.y) / h });
}
