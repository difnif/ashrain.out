// ashrain.out — 예제·유제(#/p/<개념>) 순수 도우미 (React·Supabase·DOM 없음, node 테스트: tests/practice.test.mjs)
// · 흐름 규칙: 예제는 해설 먼저(답 입력 없음), 유제는 답 먼저 → 맞든 틀리든 해설.
// · 입력 칸 힌트는 "표기 방식"만 알려 준다 — 세트 JSON 의 placeholder 예시(예: 100°)가 답을 그대로 보여 주는 경우가 많아서 쓰지 않는다.

export const CIRC = ["①", "②", "③", "④", "⑤", "⑥"];

/** 문항 종류 — "예제"(해설 먼저, 답 입력 없음) | "유제"(답 먼저, 그다음 해설). 표기가 없으면 유제 */
export const practiceKind = (p) => (p?.kind === "예제" ? "예제" : "유제");

// ── 답 판정 ──────────────────────────────────────────────────────────────────
export function normAns(s) {
  let t = String(s ?? "").replace(/\s+/g, "")
    .replace(/−/g, "-").replace(/×/g, "x").replace(/÷/g, "/")
    .replace(/[，]/g, ",").toLowerCase();
  CIRC.forEach((c, i) => { t = t.replace(new RegExp(c, "g"), String(i + 1)); });
  return t;
}

export function numVal(s) {
  const t = normAns(s);
  if (/^-?\d+(\.\d+)?$/.test(t)) return parseFloat(t);
  const m = t.match(/^(-?\d+)\/(\d+)$/);
  if (m && +m[2] !== 0) return +m[1] / +m[2];
  return null;
}

/** accept 목록 중 하나와 같으면 정답 (exact 가 아니면 1/2 = 0.5 같은 수치 동치도 허용) */
export function isCorrect(input, accept, { exact = false } = {}) {
  const inN = normAns(input);
  if (!inN) return false;
  for (const a of accept || []) {
    if (inN === normAns(a)) return true;
    if (!exact) {
      const va = numVal(a), vi = numVal(input);
      if (va !== null && vi !== null && Math.abs(va - vi) < 1e-9) return true;
    }
  }
  return false;
}

/** 값은 맞는데 단위만 빠졌나 — "12" 를 "12cm" 로 받는 문항 */
export function unitMissing(input, answer = {}) {
  const unit = answer.unit;
  if (!unit || !normAns(input)) return false;
  if (normAns(input).includes(normAns(unit))) return false;
  return isCorrect(String(input) + unit, answer.accept, { exact: answer.format === "fraction" });
}

// ── 입력 힌트 (표기 방식만) ──────────────────────────────────────────────────
/** placeholder 에서 "(예: …)" / "예: …" 예시를 뗀다 → 남는 안내문 ("번호만 입력", "두 근을 쉼표로") 또는 "" */
export function stripExample(ph) {
  return String(ph ?? "")
    .replace(/\(?\s*(?:예|예시|ex|e\.g\.)\s*[:：)]\s*[^)]*\)?\s*$/i, "")
    .replace(/\(\s*\)/g, "")
    .trim();
}

/**
 * 답의 표기 모양 — 값은 감추고 꼴만: "(-1,1)" → "(□,□)", "x=-1" → "x=□", "2x-1" → "□x-□", "10√2" → "□√□", "100°" → "□°".
 * 숫자가 하나도 없으면(㉠, 없다, a …) 모양이 곧 답이라 null.
 */
export function answerShape(ans) {
  const s = String(ans ?? "").replace(/\s+/g, "");
  if (!s) return null;
  const shape = s
    .replace(/(^|[(=,:;<>≤≥±/])[-−](?=\d)/g, "$1")      // 맨 앞·괄호·등호 뒤의 음수 부호는 값의 일부 → 감춘다
    .replace(/\d+(?:\.\d+)?/g, "□");
  return shape === s ? null : shape;
}

/**
 * 입력 칸 힌트.
 *   객관식 → "번호로 입력 (1~5)"
 *   분수 칸 → "분자 / 분모"
 *   그 외 → placeholder 의 안내문(예시 뗀 것) + 답 모양. 둘 다 없으면 단위 안내 또는 "답 입력"
 */
export function inputHint(answer = {}, { hasChoices = false, nChoices = 0 } = {}) {
  if (hasChoices) return nChoices > 1 ? `번호로 입력 (1~${nChoices})` : "번호로 입력";
  if (answer.format === "fraction") return "분자 / 분모";
  const rest = stripExample(answer.placeholder);
  const shape = answerShape(answer.accept?.[0]);
  if (rest) return shape && shape !== "□" && !/꼴|형태|모양/.test(rest) ? `${rest} (${shape} 꼴)` : rest;
  if (shape) return shape === "□" ? "숫자로 입력" : `${shape} 꼴로 입력`;
  return answer.unit ? `단위까지 (${answer.unit})` : "답 입력";
}

/** 해설 끝에 보여 줄 답 문자열 — 객관식은 ①②…, 분수 칸은 {{a/b}} (rich 토큰) */
export function displayAnswer(answer = {}, { hasChoices = false } = {}) {
  const a = String(answer.accept?.[0] ?? "").trim();
  if (!a) return "";
  if (hasChoices) {
    const n = Number(normAns(a));
    if (Number.isInteger(n) && n >= 1 && n <= CIRC.length) return CIRC[n - 1];
    return a;
  }
  if (answer.format === "fraction") {
    const m = a.match(/^(-?\d+)\/(\d+)$/);
    if (m) return `{{${m[1]}/${m[2]}}}`;
  }
  return a;
}

// ── 흐름 ─────────────────────────────────────────────────────────────────────
/**
 * 문항 하나의 화면 단계.
 *   예제: 항상 "explain" (해설 → 답 표시).
 *   유제: 시도(attempt)나 기록(solved)이 없으면 "answer", 있으면 "explain".
 */
export function practicePhase(p, { attempt = null, solved = false } = {}) {
  if (practiceKind(p) === "예제") return "explain";
  return attempt || solved ? "explain" : "answer";
}
