// 강사도구 엔진 — backend.js 가 부르는 입구 (PDF 일은 모두 이 브라우저 안에서)
import { openPdf, renderClip, canvas, toBlob, imgToCanvas } from "./base";
export { convert, wrongMake } from "./print";
export { registerAnalyze, registerCommit, libraryDraft, libraryAuto, draftUrl, partsInSheet } from "./register";
export { exportPrints, exportTranscribe, exportAnalysis, importTranscripts, exportBookPack } from "./exports";
export { gradingPdf, studentPdf, stampNames, mergeScans } from "./reports";
import { attachAnswer as attach } from "./register";

export async function pageCount(bytes) {
  const doc = await openPdf(bytes);
  const n = doc.numPages;
  doc.destroy();
  return n;
}
export async function renderPagePng(bytes, no, scale = 2) {
  const doc = await openPdf(bytes);
  try {
    const page = await doc.getPage(Math.max(1, Math.min(doc.numPages, no)));
    const im = await renderClip(page, null, 72 * scale * 0.76);
    return toBlob(imgToCanvas(im), "image/png");
  } finally { doc.destroy(); }
}
export const attachAnswer = (pr, up, ctx) => attach(pr, up, ctx);
void canvas;
