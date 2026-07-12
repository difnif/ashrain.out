// 파이프라인 1·2단계 — MediaPipe tasks-vision (전 과정 온디바이스)
// 모델 파일은 public/models/ 에 배치 (README 참고). 사진은 기기 밖으로 나가지 않음.
// ⚠ 이 모듈은 실제 브라우저+모델 파일 환경에서 최종 검증 필요 (샌드박스에서 미검증)

import { FilesetResolver, FaceDetector, ImageSegmenter } from "@mediapipe/tasks-vision";

let detector = null, segmenter = null, initPromise = null;

export function initVision(base = "/models") {
  if (initPromise) return initPromise;
  initPromise = (async () => {
    const fileset = await FilesetResolver.forVisionTasks(`${base}/wasm`);
    detector = await FaceDetector.createFromOptions(fileset, {
      baseOptions: { modelAssetPath: `${base}/blaze_face_short_range.tflite` },
      runningMode: "IMAGE",
    });
    segmenter = await ImageSegmenter.createFromOptions(fileset, {
      baseOptions: { modelAssetPath: `${base}/selfie_segmenter.tflite` },
      runningMode: "IMAGE",
      outputConfidenceMasks: true,
    });
  })();
  return initPromise;
}

// 1단계: 얼굴 점검 — { ok, reason?, face? }
export async function checkFace(imgEl, { minFaceRatio = 0.15, minBrightness = 55 } = {}) {
  await initVision();
  const res = detector.detect(imgEl);
  const faces = res.detections || [];
  if (faces.length === 0) return { ok: false, reason: "얼굴을 찾지 못했어요. 얼굴이 잘 보이는 사진으로 올려줘!" };
  if (faces.length > 1) return { ok: false, reason: "한 명만 나온 사진으로 부탁해요. 주인공은 너 하나야 🌟" };

  const bb = faces[0].boundingBox; // { originX, originY, width, height }
  const ratio = Math.max(bb.width / imgEl.naturalWidth, bb.height / imgEl.naturalHeight);
  if (ratio < minFaceRatio) return { ok: false, reason: "얼굴이 너무 작아요. 조금 더 가까이에서 찍은 사진으로 올려줘!" };

  // 밝기 검사 (평균 휘도)
  const c = document.createElement("canvas");
  const s = 64; c.width = s; c.height = s;
  const ctx = c.getContext("2d");
  ctx.drawImage(imgEl, 0, 0, s, s);
  const d = ctx.getImageData(0, 0, s, s).data;
  let lum = 0;
  for (let i = 0; i < d.length; i += 4) lum += 0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2];
  lum /= (d.length / 4);
  if (lum < minBrightness) return { ok: false, reason: "사진이 너무 어두워요. 밝은 곳에서 찍은 사진으로 올려줘!" };

  return { ok: true, face: bb };
}

// 얼굴 기준 3:4 크롭 (얼굴 중심을 상단 1/3에 배치)
export function cropPortrait(imgEl, face, { maxWidth = 810 } = {}) {
  const AR = 3 / 4;
  const iw = imgEl.naturalWidth, ih = imgEl.naturalHeight;
  const fcx = face.originX + face.width / 2;
  const fcy = face.originY + face.height / 2;
  // 크롭 높이: 얼굴 높이의 ~3.6배 (포스터 여백 확보), 프레임 안으로 클램프
  let ch = Math.min(ih, face.height * 3.6);
  let cw = ch * AR;
  if (cw > iw) { cw = iw; ch = cw / AR; }
  let cx = Math.min(Math.max(0, fcx - cw / 2), iw - cw);
  let cy = Math.min(Math.max(0, fcy - ch / 3), ih - ch);
  const scale = Math.min(1, maxWidth / cw);
  const W = Math.round(cw * scale), H = Math.round(ch * scale);
  const out = document.createElement("canvas");
  out.width = W; out.height = H;
  out.getContext("2d").drawImage(imgEl, cx, cy, cw, ch, 0, 0, W, H);
  return out;
}

// 2단계: 배경 제거 + 그라디언트 배경 합성 (마스크 페더 처리)
export async function segmentCompose(srcCanvas, bgColors = ["#E5E9F0", "#B9C1CC"], feather = 6) {
  await initVision();
  const W = srcCanvas.width, H = srcCanvas.height;
  const result = segmenter.segment(srcCanvas);
  const mask = result.confidenceMasks[0]; // 인물 확률 0..1

  // 마스크 → 캔버스 (알파)
  const maskCv = document.createElement("canvas");
  maskCv.width = W; maskCv.height = H;
  const mctx = maskCv.getContext("2d");
  const mimg = mctx.createImageData(W, H);
  const mdata = mask.getAsFloat32Array();
  for (let i = 0; i < W * H; i++) {
    const a = Math.round(mdata[i] * 255);
    mimg.data[i*4] = 255; mimg.data[i*4+1] = 255; mimg.data[i*4+2] = 255; mimg.data[i*4+3] = a;
  }
  mctx.putImageData(mimg, 0, 0);
  result.close();

  // 페더: 마스크 자체를 블러
  const soft = document.createElement("canvas");
  soft.width = W; soft.height = H;
  const sctx = soft.getContext("2d");
  sctx.filter = `blur(${feather}px)`;
  sctx.drawImage(maskCv, 0, 0);
  sctx.filter = "none";

  // 인물만 추출
  const person = document.createElement("canvas");
  person.width = W; person.height = H;
  const pctx = person.getContext("2d");
  pctx.drawImage(srcCanvas, 0, 0);
  pctx.globalCompositeOperation = "destination-in";
  pctx.drawImage(soft, 0, 0);
  pctx.globalCompositeOperation = "source-over";

  // 그라디언트 배경 위 합성
  const out = document.createElement("canvas");
  out.width = W; out.height = H;
  const octx = out.getContext("2d");
  const g = octx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, bgColors[0]); g.addColorStop(1, bgColors[1]);
  octx.fillStyle = g; octx.fillRect(0, 0, W, H);
  octx.drawImage(person, 0, 0);
  return out;
}
