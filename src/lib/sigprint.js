// ashrain.out — 시그니처 프린트 원본(문제지 · 정답) 받기 — 주소 · 이름 (lib/sigprint.js) — 순수 도우미
// 시그니처 프린트 = 해설 액자의 세트 하나(frames/index.js 의 prints — code 프린트 코드). 원본 PDF 는 강사도구 보관함
//   (teacher-tool/<선생님>/tt/<코드>/…, 비공개)에 있고, 워크플로 push-sig-files(scripts/sig-files.mjs)가 그 원본을
//   공개 버킷 concept-sets 의 av/sig/<코드>/{problems,answers}.pdf 로 올린다 — main 머지 때와 매일 한 번(새로 등록한 프린트도).
//   문제지 = 보관함의 문제지 그대로 · 정답 = 보관함의 정답 문서(빠른정답 > 정답해설 > 해설 > 정답 PDF 차례로 첫 것).
//   아직 보관함에 없는 프린트는 받을 때 「아직 올라가지 않았어요」(frames/sigdocs.jsx).
//   쓰는 곳: 해설 액자 오른쪽 위 📄(frames/sigdocs.jsx — 단일 · 듀얼 「전부」) · 학생앱 목록 꾹 눌러 「📄 프린트」(components/AvPrintSheet.jsx).
import { avItem } from "./av.js";
import { FILES_BASE } from "./conceptsets.js";

export const SIG_DOCS = [
  { id: "problems", label: "문제지", suf: "문제지" },
  { id: "answers", label: "정답 · 해설", suf: "정답" },
];
/** 「WF7-QYN」 → 「WF7QYN」(저장소 폴더 이름) */
export const codeKey = (code) => String(code || "").replace(/-/g, "").toUpperCase();
export const sigPdfUrl = (code, doc) => `${FILES_BASE}/av/sig/${codeKey(code)}/${doc}.pdf`;
/** 콘텐츠 key(「meet:tri」)가 원본을 받을 수 있는 시그니처 프린트면 그 항목(lib/av.js — code 있음), 아니면 null */
export function sigOf(key) {
  const it = avItem(key);
  return it && it.sig && it.code ? it : null;
}
export const sigFileBase = (it) => `${it.level}-${String(it.short).replace(/[\s·/\\:*?"<>|()—~]+/g, "")}`;
export const sigDownloadName = (it, doc) => `${sigFileBase(it)}-${(SIG_DOCS.find((d) => d.id === doc) || SIG_DOCS[0]).suf}.pdf`;
