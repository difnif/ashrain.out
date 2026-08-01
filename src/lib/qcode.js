// ashrain.out — 질문코드 + 익명 필명 생성기
// 질문코드: {학기문자}{개념번호}-{단락번호}  예) m1-1-03 의 b2 → A03-2
export const UNIT_LETTER = {
  "m1-1": "A", "m1-2": "B", "m2-1": "C", "m2-2": "D", "m3-1": "E", "m3-2": "F",
  "h1-1": "G", "h1-2": "H", "h2-1": "J", "h2-2": "K", "h3-1": "L", "h3-2": "M", "h3-3": "N",
}; // I·O는 숫자와 혼동되어 건너뜀
export const LETTER_UNIT = Object.fromEntries(Object.entries(UNIT_LETTER).map(([u, l]) => [l, u]));
export const UNIT_NAME = {
  "m1-1": "중1-1", "m1-2": "중1-2", "m2-1": "중2-1", "m2-2": "중2-2", "m3-1": "중3-1", "m3-2": "중3-2",
  "h1-1": "공통수학1", "h1-2": "공통수학2", "h2-1": "대수", "h2-2": "미적분1",
  "h3-1": "미적분2", "h3-2": "확률과 통계", "h3-3": "기하",
};

export function qcode(conceptId, blockId) {
  const m = String(conceptId || "").match(/^([mh]\d-\d)-(\d+)$/);
  if (!m) return "";
  const letter = UNIT_LETTER[m[1]] || "?";
  const num = m[2].padStart(2, "0");
  const bd = String(blockId || "").match(/\d+/);
  return bd ? `${letter}${num}-${bd[0]}` : `${letter}${num}`;
}

// ── 익명 필명: 수학자 × 문학작품 (결정적 — 같은 seed면 항상 같은 이름) ──
const MATH = [
  "유클리드","피타고라스","아르키메데스","디오판토스","히파티아","알콰리즈미","피보나치","네이피어",
  "데카르트","페르마","파스칼","뉴턴","라이프니츠","베르누이","오일러","라그랑주","라플라스","푸리에",
  "가우스","코시","아벨","갈루아","리만","칸토어","힐베르트","푸앵카레","소피 제르맹","코발레프스카야",
  "라마누잔","뇌터","괴델","튜링","폰 노이만","에르되시","하이젠베르크","콜모고로프",
];
const WORKS = [
  "톰 소여의 모험","님의 침묵","호밀밭의 파수꾼","중용 24장","어린 왕자","데미안","노인과 바다","변신",
  "이방인","죄와 벌","전쟁과 평화","위대한 개츠비","오만과 편견","폭풍의 언덕","제인 에어","레 미제라블",
  "몬테크리스토 백작","돈키호테","파우스트","햄릿","리어왕","맥베스","신곡","오디세이아",
  "소나기","메밀꽃 필 무렵","동백꽃","봄봄","운수 좋은 날","무정","상록수","홍길동전",
  "구운몽","춘향전","진달래꽃","청포도","별 헤는 밤","서시","목민심서","난쟁이가 쏘아올린 작은 공",
];
const hashStr = (s) => { let h = 5381; for (const ch of String(s)) h = ((h * 33) ^ ch.codePointAt(0)) >>> 0; return h; };
const josa = (name) => { // 와/과: 받침 있으면 '과'
  const c = name.charCodeAt(name.length - 1);
  return c >= 0xac00 && c <= 0xd7a3 && (c - 0xac00) % 28 > 0 ? "과" : "와";
};
export function penName(seed) {
  const h = hashStr(seed);
  const m = MATH[h % MATH.length];
  const w = WORKS[Math.floor(h / 97) % WORKS.length];
  return h % 2 === 0 ? `${m}의 ${w}` : `${m}${josa(m)} ${w}`;
}
