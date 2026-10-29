// ashrain.out — 서술형 평가 촬영 처리 (브라우저 입출력): 사진 파일 → 회색조 → pipeline.analyzePhoto → 판독 영역 JPEG
// 서버·AI 없이 "몇 쪽인지, 이 평가 시험지인지, 다시 찍어야 하는지"를 바로 안다. 서버로는 판독 영역(crop)만(+저장이 켜졌으면 펴진 쪽 전체) 보낸다.
import { fileToCanvas } from "../camera";
import { toGray } from "../omr/detect.js";
import { readRegion } from "./sheet.js";
import { analyzePhoto, WARP_SCALE } from "./pipeline.js";

export { WARP_SCALE };
export const CAPTURE_SIDE = 2400;     // 사진 긴 변 (손글씨 판독에 쓸 해상도 — 쪽 기준 ≈ 7~8 px/mm)
export const DETECT_SIDE = 1600;      // 마커 찾기는 줄인 사진으로(빠르게) — 찾은 모서리는 원본 좌표로 키운다

/** 안내 문구 — reason → 다시 찍기 안내 */
export const REASON_TEXT = {
  markers: "네 귀퉁이의 검은 네모(■) 네 개가 모두 화면에 들어오게 찍어 주세요.",
  orient: "네 귀퉁이 ■가 모두 보이게, 종이를 평평하게 놓고 바로 위에서 찍어 주세요.",
  code: "아래 가운데의 작은 네모 줄을 읽지 못했어요 — 가리지 말고, 흔들리지 않게 찍어 주세요.",
  other: "이 평가의 시험지가 아니에요 — 오늘 받은 시험지인지 확인해 주세요.",
  dark: "너무 어두워요 — 밝은 곳에서 그림자 없이 찍어 주세요.",
  flat: "글씨가 흐리게 찍혔어요 — 조금 더 가까이, 밝게 찍어 주세요.",
  blur: "흔들렸어요 — 휴대폰을 잠깐 멈추고 다시 찍어 주세요.",
  open: "사진을 열 수 없어요 — 다시 찍거나 다른 사진을 골라 주세요.",
};

function grayOf(cv) {
  const ctx = cv.getContext("2d", { willReadFrequently: true });
  return toGray(ctx.getImageData(0, 0, cv.width, cv.height));
}
function shrink(cv, maxSide) {
  const sc = Math.min(1, maxSide / Math.max(cv.width, cv.height));
  if (sc >= 1) return { cv, sc: 1 };
  const t = document.createElement("canvas");
  t.width = Math.round(cv.width * sc); t.height = Math.round(cv.height * sc);
  t.getContext("2d").drawImage(cv, 0, 0, t.width, t.height);
  return { cv: t, sc: t.width / cv.width };
}

/** 회색 래스터의 [x0,y0,x1,y1](단위) 부분 → JPEG dataURL. outScale: 1단위당 px (없으면 래스터 배율 그대로) */
function grayJpeg(warped, box, quality, outScale = null) {
  const s = warped.scale;
  const [x0, y0, x1, y1] = box ? box.map((v) => Math.round(v * s)) : [0, 0, warped.width, warped.height];
  const w = Math.max(1, Math.min(warped.width, x1) - x0), h = Math.max(1, Math.min(warped.height, y1) - y0);
  const cv = document.createElement("canvas");
  cv.width = w; cv.height = h;
  const ctx = cv.getContext("2d");
  const im = ctx.createImageData(w, h);
  const g = warped.gray, W = warped.width;
  for (let y = 0; y < h; y++) {
    const row = (y0 + y) * W + x0;
    for (let x = 0; x < w; x++) {
      const v = g[row + x];
      const p = (y * w + x) * 4;
      im.data[p] = v; im.data[p + 1] = v; im.data[p + 2] = v; im.data[p + 3] = 255;
    }
  }
  ctx.putImageData(im, 0, 0);
  let out = cv;
  if (outScale && Math.abs(outScale - s) > 0.01) {
    const r = outScale / s;
    out = document.createElement("canvas");
    out.width = Math.max(1, Math.round(w * r)); out.height = Math.max(1, Math.round(h * r));
    const c2 = out.getContext("2d");
    c2.imageSmoothingQuality = "high";
    c2.drawImage(cv, 0, 0, out.width, out.height);
  }
  return out.toDataURL("image/jpeg", quality);
}

/**
 * 사진 파일 하나 처리. set: 공개 평가(sheet·pages). wantImage: 서버가 사진 저장을 켰을 때만 펴진 쪽 전체를 만든다.
 * → { ok:true, page, kind, check, quality, crop(base64), image(base64|null), thumb(dataURL) } | { ok:false, reason, page? }
 */
export async function processPhoto(file, set, { wantImage = false, skipQuality = false } = {}) {
  let cv;
  try { cv = await fileToCanvas(file, CAPTURE_SIDE); } catch { return { ok: false, reason: "open" }; }
  const sm = shrink(cv, DETECT_SIDE);
  const small = { gray: grayOf(sm.cv), width: sm.cv.width, height: sm.cv.height, sc: sm.sc };
  const full = sm.sc === 1 ? small : { gray: grayOf(cv), width: cv.width, height: cv.height };
  const r = analyzePhoto(full, small, set, { skipQuality });
  if (!r.ok) return r;
  const page = (set.pages || []).find((p) => +p.no === r.page);
  const region = readRegion(page);
  const crop = region ? grayJpeg(r.warped, region, 0.82).split(",")[1] : null;
  const image = wantImage && page.kind !== "guide" ? grayJpeg(r.warped, null, 0.72, 1).split(",")[1] : null;
  const thumb = grayJpeg(r.warped, null, 0.6, 0.32);
  return { ok: true, page: r.page, kind: r.kind, check: r.check, quality: r.quality, crop, image, thumb };
}
