// 한글 검색 — 공백 무시 부분일치 + 초성 검색 (개념·기능 찾기 공용)
//   koMatch("정수", "정수와 유리수")      → true
//   koMatch("ㅈㅅ", "정수와 유리수")      → true  (질의가 전부 초성이면 초성열로 비교)
//   koMatch("유리 수", "정수와 유리수")   → true  (공백 무시)
const CHO = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"];

const norm = (s) => String(s || "").toLowerCase().replace(/\s+/g, "");

/** 문자열의 초성열 — 한글 음절은 초성으로, 나머지 글자는 소문자 그대로 */
export function choOf(s) {
  let out = "";
  for (const ch of String(s || "")) {
    const c = ch.codePointAt(0);
    if (c >= 0xac00 && c <= 0xd7a3) out += CHO[Math.floor((c - 0xac00) / 588)];
    else if (!/\s/.test(ch)) out += ch.toLowerCase();
  }
  return out;
}

const isChoQuery = (q) => q.length > 0 && [...q].every((ch) => CHO.includes(ch));

/** 질의가 주어진 텍스트들 중 어디든 걸리면 true. 빈 질의는 항상 true. */
export function koMatch(query, ...texts) {
  const q = norm(query);
  if (!q) return true;
  const hay = texts.map(norm).join("\u0000");
  if (hay.includes(q)) return true;
  if (isChoQuery(q)) return texts.map(choOf).join("\u0000").includes(q);
  return false;
}

/** 목록 필터 — pick(row) 가 돌려준 텍스트들로 koMatch, 최대 limit 개 */
export function koFilter(rows, query, pick, limit = 30) {
  const out = [];
  for (const r of rows || []) {
    if (koMatch(query, ...[].concat(pick(r) || []))) { out.push(r); if (out.length >= limit) break; }
  }
  return out;
}
