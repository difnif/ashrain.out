// ashrain.out — 사진 OMR: 인쇄한 세트(시험지+답안 카드) 기록 — localStorage (기기 안에서만)
// 저장하는 것은 채점에 필요한 최소치: 문항 id·번호·종류·정답(·대안)·보기 + 표시용 문제 앞부분.
// 채점 때는 id 로 문항을 다시 불러(해설 포함) 판정하므로 여기 정답은 표시·비상용이다.

export const LS_KEY = "ash.omr.sets";
export const MAX_SETS = 20;
export const CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";   // 0/O · 1/I/L 제외 (헷갈리는 글자 없음)
export const CODE_LEN = 6;

function rand(n) {
  try {
    if (typeof crypto !== "undefined" && crypto.getRandomValues) {
      const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n;
    }
  } catch { /* fall through */ }
  return Math.floor(Math.random() * n);
}

/** "K7Q2-4M" 꼴 (6글자 + 표시용 하이픈) */
export function newCode() {
  let s = "";
  for (let i = 0; i < CODE_LEN; i++) s += CODE_ALPHABET[rand(CODE_ALPHABET.length)];
  return fmtCode(s);
}

export function fmtCode(raw) {
  const s = String(raw || "").toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, CODE_LEN);
  return s.length > 4 ? s.slice(0, 4) + "-" + s.slice(4) : s;
}

/** 입력 정규화 — 소문자·공백·하이픈 차이, 0→O 1→I 등 흔한 오타 흡수 */
export function normCode(input) {
  let s = String(input || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
  s = s.replace(/0/g, "O").replace(/[1L]/g, "I");   // 알파벳에 없는 글자 → 비슷한 것으로 (어차피 매칭용)
  return s;
}
const key = (code) => normCode(code);

function readAll() {
  try {
    const raw = typeof localStorage !== "undefined" ? localStorage.getItem(LS_KEY) : null;
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch { return []; }
}
function writeAll(list) {
  try { localStorage.setItem(LS_KEY, JSON.stringify(list)); return true; } catch { return false; }
}

const snippet = (q) => String(q ?? "").replace(/\[\[|\]\]/g, "").replace(/\s+/g, " ").trim().slice(0, 80);

/**
 * 세트 저장. set: { code, conceptId, conceptTitle, unitId, title, items:[{ id, no, kind, answer, answer_alt, choices, question }], createdAt }
 * 같은 코드는 덮어쓴다. 최신이 앞. 최대 MAX_SETS.
 */
export function saveSet(set) {
  if (!set?.code || !Array.isArray(set.items)) return null;
  const row = {
    code: fmtCode(set.code),
    conceptId: set.conceptId || null,
    conceptTitle: set.conceptTitle || "",
    unitId: set.unitId || null,
    title: set.title || "",
    createdAt: set.createdAt || new Date().toISOString(),
    items: set.items.map((it, i) => ({
      id: it.id,
      no: Number.isFinite(+it.no) ? +it.no : i + 1,
      kind: it.kind === "short" ? "short" : "choice",
      answer: it.answer ?? null,
      answer_alt: Array.isArray(it.answer_alt) ? it.answer_alt : null,
      choices: Array.isArray(it.choices) ? it.choices : null,
      q: it.q ?? snippet(it.question),
    })),
  };
  const rest = readAll().filter((s) => key(s.code) !== key(row.code));
  writeAll([row, ...rest].slice(0, MAX_SETS));
  return row;
}

/** 최신순 목록 */
export function listSets() {
  return readAll().sort((a, b) => String(b.createdAt || "").localeCompare(String(a.createdAt || "")));
}

export function getSet(code) {
  const k = key(code);
  if (!k) return null;
  return readAll().find((s) => key(s.code) === k) || null;
}

export function removeSet(code) {
  const k = key(code);
  const list = readAll();
  const next = list.filter((s) => key(s.code) !== k);
  if (next.length !== list.length) writeAll(next);
  return list.length - next.length;
}
