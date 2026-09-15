// ashrain.out — 문항 정답 판정 (test_items 용)
// 정답 문자열은 mathir 마커([[frac(1,2)]] · [[deg(60)]] · [[105 * pi]])이거나 평문("2", "소수", "x=3")이다.
// 학생 입력은 평문("1/2", "60°", "105π", "x = 3", "3 또는 -2")이다.
// 판정 순서: ① 값 동치(mathir 파싱 → 유리수/실수 집합 비교) ② 표기 정규화 문자열 비교. 둘 다 실패면 오답.
// 원칙 P3 "오류보다 침묵": 파싱이 안 되는 쪽은 그냥 그 경로를 포기하고 다음 경로로 넘어간다.

import { parseAnswer, ev, disp, Frac } from "./mathir.js";

export const CIRCLED = ["①", "②", "③", "④", "⑤"];

// 뒤에 붙는 단위 — 정답이 단위 없이 저장돼 있어도 "12 cm²" 를 맞다고 볼 수 있게 벗긴다
const UNIT_TAIL = /\s*(cm³|cm²|m³|m²|km²|mm²|mm|cm|km|kg|mL|ml|g|L|m|명|개|원|마리|권|자루|살|세|년|시간|분|초|도|점|장|벌|대|병|줄|칸|번|가지|경우|퍼센트|%)\s*$/u;

/** 표기 정규화 — 공백·유니코드 기호·접두어 정리 */
export function normText(s) {
  let t = String(s ?? "").trim();
  t = t.replace(/[−–]/g, "-").replace(/×/g, "*").replace(/÷/g, "/").replace(/·/g, "*");
  t = t.replace(/^(답\s*[:：]?\s*)/, "");
  // "x = 3" → "3", "x=3 또는 x=-2" → "3 또는 -2" (단, "a=5, b=1" 같은 서로 다른 변수는 그대로)
  t = t.replace(/(^|또는\s*|\|\s*)([a-zA-Z])\s*=\s*(?=[-+]?\d|\[|√|sqrt)/g, "$1");
  t = t.replace(/°/g, "");
  t = t.replace(/(\d)\s*π/g, "$1*pi").replace(/π/g, "pi");
  t = t.replace(/√\s*\(([^)]+)\)/g, "sqrt($1)").replace(/√\s*(\d+(?:\.\d+)?)/g, "sqrt($1)");
  t = t.replace(/\s*,\s*/g, ", ").replace(/\s+/g, " ").trim();
  return t;
}

/** 단위 꼬리 제거 ("12 cm²" → "12"). 숫자로 끝나지 않을 때만 시도 */
export function stripUnit(s) {
  const t = String(s ?? "").trim();
  if (/[\d)\]]$/.test(t)) return t;
  const u = t.replace(UNIT_TAIL, "");
  return u === t ? t : u.trim();
}

/** 값 키: Frac → "n/d", 실수 → 소수 9자리, 그 외 → 표시 문자열 */
function valueKey(v) {
  if (v instanceof Frac) return `${v.n}/${v.d}`;
  if (typeof v === "number" && Number.isFinite(v)) {
    const r = Math.round(v * 1e9) / 1e9;
    return Number.isInteger(r) ? `${BigInt(r)}/1` : `~${r}`;
  }
  if (typeof v === "bigint") return `${v}/1`;
  return null;
}

/** 문자열 → 값 키 목록(집합). 파싱 실패면 null */
export function valueKeys(s) {
  const t = stripUnit(normText(s));
  if (!t) return null;
  try {
    const pa = parseAnswer(t);
    const items = pa?.kind === "set" ? pa.items : pa ? [pa] : [];
    const keys = [];
    for (const it of items) {
      if (it?.kind !== "ir" || !it.node) return null;
      const v = ev(it.node);
      const k = valueKey(v);
      if (k == null) return null;
      keys.push(k);
    }
    return keys.length ? keys.sort() : null;
  } catch {
    return null;
  }
}

/** 마커를 표시 문자열로 ("[[frac(1,2)]]" → "1/2", "[[deg(60)]]" → "60°") — 비교용 */
export function displayAnswer(s) {
  const t = String(s ?? "");
  try {
    const pa = parseAnswer(normText(t));
    if (pa?.kind === "set") return pa.items.map((it) => (it.kind === "ir" ? disp(it.node) : String(it.text ?? ""))).join(" 또는 ");
    if (pa?.kind === "ir") return disp(pa.node);
  } catch { /* 평문 */ }
  return t.replace(/\[\[|\]\]/g, "");
}

const flat = (s) => stripUnit(normText(displayAnswer(s))).replace(/\s+/g, "").replace(/\*/g, "").toLowerCase();

function sameKeys(a, b) {
  if (!a || !b || a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) {
    const x = a[i], y = b[i];
    if (x === y) continue;
    if (x.startsWith("~") || y.startsWith("~")) {
      const nx = x.startsWith("~") ? parseFloat(x.slice(1)) : fracToNum(x);
      const ny = y.startsWith("~") ? parseFloat(y.slice(1)) : fracToNum(y);
      if (Math.abs(nx - ny) <= 1e-7 * Math.max(1, Math.abs(nx))) continue;
    }
    return false;
  }
  return true;
}
function fracToNum(k) { const [n, d] = k.split("/"); return Number(n) / Number(d); }

/** 정답 후보 목록 (answer + answer_alt) */
export function answerCandidates(item) {
  const alts = Array.isArray(item?.answer_alt) ? item.answer_alt : [];
  return [item?.answer, ...alts].filter((x) => x != null && String(x).trim() !== "");
}

/** 단답 판정 — 값 동치 → 표기 동치 순 */
export function isCorrect(item, input) {
  const u = String(input ?? "").trim();
  if (!u) return false;
  const cands = answerCandidates(item);
  const uk = valueKeys(u);
  for (const c of cands) {
    if (uk) { const ck = valueKeys(c); if (ck && sameKeys(uk, ck)) return true; }
  }
  const uf = flat(u);
  if (!uf) return false;
  for (const c of cands) if (flat(c) === uf) return true;
  return false;
}

/** 객관식 판정 — 보기 텍스트가 정답과 같거나 값이 같으면 정답 */
export function isChoiceCorrect(item, idx) {
  const ch = item?.choices?.[idx];
  if (ch == null) return false;
  if (String(ch) === String(item.answer)) return true;
  const a = String(item.answer ?? "").trim();
  const ci = CIRCLED.indexOf(a);
  if (ci >= 0) return ci === idx;                       // 정답이 "③" 꼴로 저장된 경우
  if (/^[1-5]$/.test(a) && !item.choices.includes(a)) return Number(a) - 1 === idx;   // 정답이 번호로 저장된 경우
  return isCorrect(item, ch);
}

/** 정답 보기 번호 (없으면 -1) */
export function correctChoiceIndex(item) {
  const n = item?.choices?.length || 0;
  for (let i = 0; i < n; i++) if (isChoiceCorrect(item, i)) return i;
  return -1;
}

/** 문항 종류 — choice(객관식) / short(단답) / ox / essay(서술) */
export function kindOf(item) {
  const q = String(item?.qtype || "").toLowerCase();
  if (q === "choice" || (Array.isArray(item?.choices) && item.choices.length >= 2)) return "choice";
  if (q === "ox") return "ox";
  if (q === "essay" || q === "proof") return "essay";
  return "short";
}
