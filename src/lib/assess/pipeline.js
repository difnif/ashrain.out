// ashrain.out — 서술형 평가 사진 분석의 순수 부분 (DOM 없음 — node 테스트 가능). 브라우저 쪽 입출력은 capture.js.
// 회색조 사진 → (줄인 사진에서) 마커 찾기·방향 → 원본 해상도로 펴기 → 쪽 번호 띠 → 품질 판정
import { threshold, findMarkers, orientCorners, warpToSpec } from "../omr/detect.js";
import { sheetSpec, readPageCode, pageQuality, judgeQuality } from "./sheet.js";

export const WARP_SCALE = 1.4;        // 펴진 쪽 1단위 = 1.4px (1400×1980)

/**
 * full: { gray, width, height } 원본(긴 변 ~2400) · small: { gray, width, height, sc } 마커 찾기용 축소본(sc = small/full 배율)
 * set: 공개 평가(sheet·pages) · opts.skipQuality: 품질 판정을 건너뛴다(학생이 '이대로 보내기'를 고른 경우)
 * → { ok:true, page, kind, check, warped, quality, margin } | { ok:false, reason, page? , quality? }
 */
export function analyzePhoto(full, small, set, opts = {}) {
  const s = small || { ...full, sc: 1 };
  const bin = threshold(s.gray, s.width, s.height);
  const quad = findMarkers(bin, s.width, s.height);
  if (!quad) return { ok: false, reason: "markers" };
  const spec = sheetSpec(set.sheet);
  const o = orientCorners(s.gray, s.width, s.height, quad, spec);
  if (!o) return { ok: false, reason: "orient" };
  const corners = o.corners.map(([x, y]) => [x / s.sc, y / s.sc]);
  const warped = warpToSpec(full.gray, full.width, full.height, corners, spec, WARP_SCALE);
  if (!warped) return { ok: false, reason: "orient" };
  warped.scale = WARP_SCALE;
  const code = readPageCode(warped, set.sheet);
  if (!code.ok) return { ok: false, reason: "code" };
  if (code.check !== +set.sheet?.pagecode?.check) return { ok: false, reason: "other", page: code.page };
  const page = (set.pages || []).find((p) => +p.no === code.page);
  if (!page) return { ok: false, reason: "other", page: code.page };
  const q = pageQuality(warped);
  const judge = judgeQuality(q);
  if (!judge.ok && !opts.skipQuality) return { ok: false, reason: judge.reason, page: code.page, quality: q };
  return { ok: true, page: code.page, kind: page.kind, check: code.check, warped, quality: { ...q, margin: code.margin }, shift: o.shift };
}
