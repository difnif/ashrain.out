// ashrain.out — 개념 설명의 「움직이는 예시」를 붙이는 자리 (lib/conceptAv.js) — 그림 엔진 없이 가볍게(개념 화면이 읽는다)
// 예시 내용(문제 · 판서 · 그림)은 features/display/concept-av.js, 재생 카드는 components/ConceptAv.jsx(React.lazy — 카드가 있을 때만 엔진을 받는다).
//   CONCEPT_AV[개념 id][단락 id] = [예시 id …] — 그 단락 끝(접기 칸 위)에 재생 카드 하나(예시가 둘 이상이면 카드 안에서 칩으로 고른다).
//   단락 글줄(또는 접기 칸 글줄)에 「[[av:예시 id]]」(여럿이면 「[[av:id1,id2]]」) 한 줄을 두면 그 자리에 놓는다 — 그 단락의 기본 자리에는 다시 놓지 않는다.
// 코드 안 예시(CONCEPT_AV)는 경우의 수와 확률(중2-2 개념 12 · 13 · 14) — 나머지 개념은 아래 학기 파일 예시.
export const CONCEPT_AV = {
  "m2-2-12": { b2: ["c12-sum"], b3: ["c12-road"], b4: ["c12-line"] },
  "m2-2-13": { b2: ["c13-prime", "c13-hh"], b3: ["c13-sure"], b4: ["c13-least"] },
  "m2-2-14": { b2: ["c14-add"], b3: ["c14-66"], b4: ["c14-back", "c14-noback"] },
};
export const AV_IDS = new Set(Object.values(CONCEPT_AV).flatMap((m) => Object.values(m).flat()));

// 그 밖의 개념(초 · 중 · 고 전체): 예시가 단원마다 public/concept-av/<학기>.json 에 있다(cvgen/ 생성기가 만든다).
//   id = <개념 id>-<번호>(예: m1-1-26-1) — DB 개념 단락 글줄의 「[[av:m1-1-26-1]]」가 그 자리에 카드를 놓는다.
//   재생 카드가 그 학기 파일을 처음 쓸 때 한 번 받는다(ConceptAv.jsx).
const UNIT_AV_RE = /^([emh][1-6]-[1-3])-\d{2}-\d+$/;
/** 학기 파일 예시 id 면 그 학기("m1-1"), 아니면 null */
export const avUnitOf = (id) => (UNIT_AV_RE.exec(String(id ?? "")) || [])[1] || null;
const knownAv = (id) => AV_IDS.has(id) || avUnitOf(id) != null;

const AV_RE = /^\[\[av:([\w-]+(?:\s*,\s*[\w-]+)*)\]\]$/;
/** 글줄 하나가 「[[av:id]]」 · 「[[av:id1,id2]]」면 아는 id 목록(없으면 빈 목록), 아니면 null */
export function avMarker(line) {
  const m = typeof line === "string" ? line.trim().match(AV_RE) : null;
  return m ? m[1].split(",").map((s) => s.trim()).filter(knownAv) : null;
}
const markersOf = (block) => [...(block?.lines || []), ...((block?.panels || []).flatMap((p) => p.lines || []))]
  .flatMap((l) => avMarker(l) || []);
/** 단락의 기본 자리(끝 · 접기 칸 위)에 놓을 예시 id — 글줄의 「[[av:…]]」로 이미 놓은 것은 뺀다 */
export function avForBlock(conceptId, block) {
  const ids = CONCEPT_AV[conceptId]?.[block?.id] || [];
  const placed = new Set(markersOf(block));
  return ids.filter((id) => !placed.has(id));
}
