// ashrain.out — 대단원(학기 안의 단원) 구성 · 순수 도우미 (DOM·Supabase 없음)
// 단원은 DB 에 표가 없고, 개념(concepts)의 sort_order 구간으로 정한다 — 표준 교육과정 기준.
// Home.jsx(개념 트리)와 시험 보기(단원 테스트의 범위 고르기)가 같이 쓴다. 범위 id 는 "<학기>~<단원 번호>" (예: m1-1~2).

// [제목, 시작 번호, 끝 번호]
export const CHAPTERS = {
  "m1-1": [["소인수분해", 1, 8], ["정수와 유리수", 9, 18], ["문자와 식", 19, 28], ["좌표평면과 그래프", 29, 34]],
  "m1-2": [["기본 도형과 작도", 1, 6], ["평면도형", 7, 11], ["입체도형", 12, 16], ["자료의 정리와 해석", 17, 21]],
  "m2-1": [["수와 식의 계산", 1, 6], ["부등식과 연립방정식", 7, 15], ["일차함수", 16, 23]],
  "m2-2": [["도형의 성질", 1, 4], ["도형의 닮음과 피타고라스 정리", 5, 11], ["확률", 12, 14]],
  "m3-1": [["제곱근과 실수", 1, 6], ["다항식의 곱셈과 인수분해", 7, 13], ["이차방정식", 14, 21], ["이차함수", 22, 30]],
  "m3-2": [["삼각비", 1, 5], ["원의 성질", 6, 11], ["통계", 12, 14]],
  "h1-1": [["다항식", 1, 3], ["방정식과 부등식", 4, 13], ["경우의 수", 14, 16], ["행렬", 17, 18]],
  "h1-2": [["도형의 방정식", 1, 7], ["집합과 명제", 8, 15], ["함수", 16, 20]],
  "h2-1": [["지수함수와 로그함수", 1, 7], ["삼각함수", 8, 11], ["수열", 12, 17]],
  "h2-2": [["함수의 극한과 연속", 1, 4], ["미분", 5, 12], ["적분", 13, 15]],
  "h3-1": [["수열의 극한", 1, 4], ["미분법", 5, 12], ["적분법", 13, 18]],
  "h3-2": [["경우의 수", 1, 3], ["확률", 4, 7], ["통계", 8, 14]],
  "h3-3": [["이차곡선", 1, 7], ["공간도형과 공간좌표", 8, 13], ["벡터", 14, 21]],
};

/** 학기의 단원 목록 (없으면 "전체" 하나) */
export const chaptersOf = (unit) => CHAPTERS[unit] || [["전체", 1, 999]];

/** 단원 범위 id — "m1-1~2" (두 번째 단원, 0부터) */
export const chapterId = (unit, idx) => `${unit}~${idx}`;

/** "m1-1~2" → { unitId:"m1-1", idx:2, title, range:[from,to] } · 형식이 아니거나 없는 단원이면 null */
export function parseChapterId(id) {
  const m = /^([mh]\d-\d)~(\d+)$/.exec(String(id || ""));
  if (!m) return null;
  const unitId = m[1], idx = Number(m[2]);
  const ch = chaptersOf(unitId)[idx];
  if (!ch) return null;
  return { unitId, idx, title: ch[0], range: [ch[1], ch[2]] };
}

/** 개념 목록(listConcepts 결과)에서 단원에 드는 개념 id 들 — sort_order 구간으로 */
export function conceptIdsInChapter(concepts, unitId, idx) {
  const ch = chaptersOf(unitId)[idx];
  if (!ch) return [];
  return (concepts || [])
    .filter((c) => c && c.unit_id === unitId && Number(c.sort_order) >= ch[1] && Number(c.sort_order) <= ch[2])
    .sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0))
    .map((c) => c.id);
}

/** 개념이 속한 단원 번호 (없으면 -1) */
export function chapterIndexOf(concept) {
  if (!concept) return -1;
  return chaptersOf(concept.unit_id).findIndex((ch) => Number(concept.sort_order) >= ch[1] && Number(concept.sort_order) <= ch[2]);
}
