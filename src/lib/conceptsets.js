// ashrain.out — 공부하기 › 컨셉 문제: 세트 목록 · 세트 데이터 · 답 판정 · 진도 · 파일(다운로드 · 인쇄)
//
// 데이터는 정적 JSON(public/concept-sets/<범주>/index.json · NN.json) — 생성기(guard-daily tk_export.py)가 만든다.
//   문항: { id, no, lv, cat, ty, sp, q(HTML), rows?, box?, fig?(SVG), a(답), omr(카드 칸), s(3단 해설 · 판서 · 도식 · 애니메이션 큐) }
//   답 a: { k:"int", v, u } · { k:"frac", n, d } · { k:"pick", v:["ㄱ","ㄷ"], o:[…] } · { k:"pair", v:[a,b], l:[…], u }
// PDF(문제지 · 해설지 · OMR 카드)는 Supabase Storage 공개 버킷 concept-sets 에 있다(워크플로 push-concept-files).
// 인쇄는 PDF 가 아니라 같은 모양의 HTML(public/concept-sets/<범주>/print/NN-*.html)을 새 창에서 연다 — 휴대폰에서도 바로 인쇄된다.

export const CS_BASE = "/concept-sets";
export const FILES_BASE = "https://ueohwmjtfmvqunjgfrhx.supabase.co/storage/v1/object/public/concept-sets";
export const pad2 = (n) => String(n).padStart(2, "0");

export const DOCS = [
  { id: "problems", label: "문제지", suf: "문제", ic: "📄" },
  { id: "solutions", label: "해설지", suf: "해설", ic: "📘" },
  { id: "omr", label: "OMR 카드", suf: "OMR", ic: "🔘" },
];

// ── 불러오기 (세션 캐시) ──────────────────────────────────────────────────────
let indexCache = null;
const setCache = new Map();

async function getJson(url) {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw new Error(`불러오지 못했어요 (${r.status})`);
  return r.json();
}

/** 범주 목록 — 「경우의 수와 확률」(prob · 중2-2) · 「일차함수와 그래프」(lin · 중2-1 · 과학 단원별) */
export const CATEGORIES = [
  { id: "prob", title: "경우의 수와 확률", sub: "중2-2 · 주제별 50제", icon: "🎲" },
  { id: "lin", title: "일차함수와 그래프", sub: "중2-1 · 과학 단원별 50제", icon: "📈" },
];

export async function loadIndex(cat = "prob") {
  if (indexCache?.[cat]) return indexCache[cat];
  const j = await getJson(`${CS_BASE}/${cat}/index.json`);
  const c = (j.categories || []).find((x) => x.id === cat) || null;
  indexCache = { ...(indexCache || {}), [cat]: c };
  return c;
}

export async function loadSet(cat, no) {
  const k = `${cat}/${pad2(no)}`;
  if (setCache.has(k)) return setCache.get(k);
  const j = await getJson(`${CS_BASE}/${cat}/${pad2(no)}.json`);
  setCache.set(k, j);
  return j;
}

// ── 답 ────────────────────────────────────────────────────────────────────────
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };

/** "1,200가지" · "12 가지" · "12" → 12 (숫자가 아니면 null) */
export function toInt(s) {
  const t = String(s ?? "").replace(/[\s,]/g, "").replace(/[가-힣]+$/u, "");
  return /^\d+$/.test(t) ? Number(t) : null;
}

/** "5/12" · "5 / 12" · "12분의 5" · "0" → { n, d } */
export function parseFrac(s) {
  const t = String(s ?? "").replace(/\s+/g, "");
  let m = t.match(/^(\d+)분의(\d+)$/u);
  if (m) return { n: +m[2], d: +m[1] };
  m = t.match(/^(\d+)\/(\d+)$/);
  if (m) return { n: +m[1], d: +m[2] };
  m = t.match(/^(\d+)$/);
  if (m) return { n: +m[1], d: 1 };
  return null;
}

// ── 유리수 · 일차식 (일차함수 범주: 음수 · 분수 · 소수 · y = ax + b · 점) ──────────────────
/** [n, d] 기약 · 분모 양수 */
export function rat(n, d = 1) {
  if (d < 0) { n = -n; d = -d; }
  const g = gcd(n, d) || 1;
  return [n / g + 0, d / g];      // + 0: −0 → 0
}
const rAdd = (a, b) => rat(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const rSub = (a, b) => rat(a[0] * b[1] - b[0] * a[1], a[1] * b[1]);
const rDiv = (a, b) => rat(a[0] * b[1], a[1] * b[0]);
const rNeg = (a) => [0 - a[0], a[1]];
const rEq = (a, b) => !!a && !!b && a[0] * b[1] === b[0] * a[1];
const MINUS = "−";
const unify = (s) => String(s ?? "").normalize("NFKC").replace(/[−–—‐]/g, "-").replace(/[{}]/g, "");

function decRat(str) {
  const [i, f = ""] = String(str).split(".");
  return rat(Number(i + f), 10 ** f.length);
}

/** "−3" · "3/4" · "-0.5" · "12.5" · "4분의 3" · "−4분의 3" → [n, d] (수가 아니면 null) */
export function parseRat(s) {
  const t = unify(s).replace(/\s+/g, "");
  let m = t.match(/^([+-]?)(\d+)분의(\d+)$/u);
  if (m) return +m[2] === 0 ? null : rat((m[1] === "-" ? -1 : 1) * +m[3], +m[2]);
  m = t.match(/^([+-]?)(\d+(?:\.\d+)?)(?:\/(\d+(?:\.\d+)?))?$/);
  if (!m) return null;
  const num = decRat(m[2]), den = m[3] ? decRat(m[3]) : [1, 1];
  if (den[0] === 0) return null;
  return rat((m[1] === "-" ? -1 : 1) * num[0] * den[1], num[1] * den[0]);
}

/** 수 → 쓰는 꼴: "−3" · "3/4" · (dec) "12.5" */
export function ratText(r, dec = false) {
  const [n, d] = r;
  const sg = n < 0 ? MINUS : "";
  const an = Math.abs(n);
  if (d === 1) return sg + an;
  if (dec) {
    let dd = d, k = 0;
    while (dd % 2 === 0) { dd /= 2; k++; }
    let k5 = 0;
    while (dd % 5 === 0) { dd /= 5; k5++; }
    if (dd === 1) {
      const p = Math.max(k, k5), scale = 10 ** p, v = (an * scale) / d;
      const s = String(v).padStart(p + 1, "0");
      return sg + s.slice(0, s.length - p) + "." + s.slice(s.length - p);
    }
  }
  return `${sg}${an}/${d}`;
}

/** 일차식 한 쪽 → { x, y, c } 계수 (꼴이 아니면 null). "2x+3" · "-x" · "1/2x" · "x/2" · "0.5x" · "(1/2)x" */
function linSide(e) {
  const out = { x: [0, 1], y: [0, 1], c: [0, 1] };
  e = e.replace(/\(([\d./]+)\)/g, "$1");
  if (!e) return null;
  const re = /([+-]?)(\d+(?:\.\d+)?(?:\/\d+(?:\.\d+)?)?)?([xy])?(?:\/(\d+(?:\.\d+)?))?/y;
  let pos = 0;
  while (pos < e.length) {
    re.lastIndex = pos;
    const m = re.exec(e);
    if (!m || !m[0] || (!m[2] && !m[3])) return null;
    const [, sg, num, v, den] = m;
    let r = num ? parseRat(num) : [1, 1];
    if (!r) return null;
    if (den) { const dr = parseRat(den); if (!dr || dr[0] === 0) return null; r = rDiv(r, dr); }
    if (sg === "-") r = rNeg(r);
    out[v || "c"] = rAdd(out[v || "c"], r);
    pos = re.lastIndex;
    if (pos < e.length && !/[+-]/.test(e[pos])) return null;
  }
  return out;
}

/** "y = 2x + 3" · "y=-x" · "2x − 3"(y = 생략) · "2x − y + 3 = 0" → { a, b } (y = ax + b, 꼴이 아니면 null) */
export function parseLine(s) {
  const t = unify(s).toLowerCase().replace(/\s+/g, "").replace(/[×·*]/g, "");
  if (!t) return null;
  const sides = t.split("=");
  if (sides.length > 2 || sides.some((x) => !x)) return null;
  const L = linSide(sides.length === 2 ? sides[0] : "y"), R = linSide(sides.length === 2 ? sides[1] : sides[0]);
  if (!L || !R) return null;
  const cx = rSub(L.x, R.x), cy = rSub(L.y, R.y), c = rSub(L.c, R.c);
  if (cy[0] === 0) return null;
  return { a: rNeg(rDiv(cx, cy)), b: rNeg(rDiv(c, cy)) };
}

/** "(2, −3)" · "2, -3" · "(1/2, 4)" → { x, y } */
export function parsePt(s) {
  const t = unify(s).replace(/[()（）\s]/g, "");
  const parts = t.split(/[,，]/);
  if (parts.length !== 2) return null;
  const x = parseRat(parts[0]), y = parseRat(parts[1]);
  return x && y ? { x, y } : null;
}

/** y = ax + b → 쓰는 꼴 "y = −1/2x + 3" (dec 이면 "y = 0.5x + 12") */
export function lineText(a, b, dec = false) {
  const head = a[0] === 0 ? "" : (a[0] === a[1] ? "x" : a[0] === -a[1] ? `${MINUS}x` : `${ratText(a, dec)}x`);
  if (!head) return `y = ${ratText(b, dec)}`;
  if (b[0] === 0) return `y = ${head}`;
  return `y = ${head} ${b[0] < 0 ? MINUS : "+"} ${ratText([Math.abs(b[0]), b[1]], dec)}`;
}

/** 단위 떼기 — 정답 단위(u)가 끝에 있으면 떼고, 남은 끝 글자(가지 · cm · ℃ …)도 뗀다 */
function stripUnit(s, u) {
  let t = unify(s).trim();
  const uu = unify(u || "").trim();
  if (uu && t.endsWith(uu)) t = t.slice(0, -uu.length).trim();
  return t.replace(/[^\d)]+$/u, "").trim();
}

/** 정답의 '쓰는 꼴' — OMR 판독 결과와 같은 꼴 ("12" · "5/12" · "ㄱ, ㄷ" · "14, 21" · "−3" · "y = 2x + 3" · "(2, −1)") */
export function rawOf(item) {
  const a = item?.a || {};
  if (a.k === "frac") return a.d === 1 ? String(a.n) : `${a.n}/${a.d}`;
  if (a.k === "pick") return (a.v || []).join(", ");
  if (a.k === "pair") return `${a.v[0]}, ${a.v[1]}`;
  if (a.k === "num") return ratText([a.n, a.d], !!a.dec);
  if (a.k === "lin") return lineText(a.a, a.b, !!a.dec);
  if (a.k === "pt") return `(${ratText(a.x, !!a.dec)}, ${ratText(a.y, !!a.dec)})`;
  return String(a.v);
}

/** 정답 표시용 평문 ("12가지" · "5/12" …) */
export function answerText(item) {
  return String(item?.a?.t || "").replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    || rawOf(item);
}

/**
 * 학생 답 판정 → { ok: true | false | null(빈 답 · 읽지 못함), note }
 * 분수는 값이 같으면 정답, 약분하지 않았으면 note 로 알려 준다(교과서 표기 = 기약분수).
 */
export function judge(item, raw) {
  const a = item?.a || {};
  const s = String(raw ?? "").trim();
  if (!s) return { ok: null, note: "" };
  if (s.includes("?")) return { ok: null, note: "읽지 못한 자리가 있어요" };
  if (a.k === "int") {
    const v = toInt(s);
    return v == null ? { ok: false, note: "숫자로 써 주세요" } : { ok: v === a.v, note: "" };
  }
  if (a.k === "frac") {
    const f = parseFrac(s);
    if (!f || f.d === 0) return { ok: false, note: "분수는 3/4 처럼 써 주세요" };
    const eq = f.n * a.d === a.n * f.d;
    const reduced = f.d === 1 || gcd(f.n, f.d) === 1;
    return { ok: eq, note: eq && !reduced ? `기약분수로 쓰면 ${a.d === 1 ? a.n : `${a.n}/${a.d}`}이에요` : "" };
  }
  if (a.k === "pick") {
    const got = [...new Set(s.match(/[ㄱ-ㅎ]/gu) || [])].sort();
    const exp = [...(a.v || [])].sort();
    return { ok: got.length === exp.length && got.every((x, i) => x === exp[i]), note: "" };
  }
  if (a.k === "pair") {
    const nums = (s.match(/\d[\d,]*/g) || []).map((x) => Number(x.replace(/,/g, "")));
    if (nums.length !== 2) return { ok: false, note: "두 수를 차례로 써 주세요 (예: 14, 21)" };
    return { ok: nums[0] === a.v[0] && nums[1] === a.v[1], note: "" };
  }
  if (a.k === "num") {
    const t = stripUnit(s, a.u);
    const r = parseRat(t);
    if (!r) return { ok: false, note: "수로 써 주세요 (예: −3 · 3/4 · 0.5)" };
    const ok = rEq(r, [a.n, a.d]);
    const m = unify(t).replace(/\s+/g, "").match(/^[+-]?(\d+)\/(\d+)$/);
    const unreduced = ok && m && gcd(+m[1], +m[2]) > 1;
    return { ok, note: unreduced ? `기약분수로 쓰면 ${ratText([a.n, a.d])}이에요` : "" };
  }
  if (a.k === "lin") {
    const L = parseLine(s);
    if (!L) return { ok: false, note: "y = ax + b 꼴로 써 주세요 (예: y = −2x + 3)" };
    return { ok: rEq(L.a, a.a) && rEq(L.b, a.b), note: "" };
  }
  if (a.k === "pt") {
    const P = parsePt(s);
    if (!P) return { ok: false, note: "점은 (x좌표, y좌표)로 써 주세요 (예: (2, −1))" };
    return { ok: rEq(P.x, a.x) && rEq(P.y, a.y), note: "" };
  }
  return { ok: null, note: "" };
}

// ── 진도 (이 기기 · localStorage, 계정별) ─────────────────────────────────────
// 한 기기를 여럿이 쓸 수 있어(학원 태블릿) 로그인한 계정 id 로 나눠 둔다 — 화면이 setProgressUser 로 알려 준다.
let USER = "";
export function setProgressUser(uid) { USER = uid ? String(uid) : ""; }
const LS = (cat, no) => `ash.cs.${USER ? USER.slice(0, 8) + "." : ""}${cat}.${pad2(no)}`;

export function readProgress(cat, no) {
  try {
    const v = JSON.parse(localStorage.getItem(LS(cat, no)) || "null");
    if (v && typeof v === "object") return { items: v.items || {}, omr: Array.isArray(v.omr) ? v.omr : [] };
  } catch { /* 무시 */ }
  return { items: {}, omr: [] };
}
function writeProgress(cat, no, p) {
  try { localStorage.setItem(LS(cat, no), JSON.stringify(p)); return true; } catch { return false; }
}

/** 문항 하나 기록 { raw, ok, at, n(시도 횟수) } — 처음 맞힌 기록은 지우지 않는다 */
export function saveAttempt(cat, no, itemId, raw, ok) {
  const p = readProgress(cat, no);
  const prev = p.items[itemId];
  p.items[itemId] = { raw, ok, at: new Date().toISOString(), n: (prev?.n || 0) + 1, everOk: !!(prev?.everOk || ok) };
  writeProgress(cat, no, p);
  return p;
}
export function resetProgress(cat, no) { writeProgress(cat, no, { items: {}, omr: readProgress(cat, no).omr }); }

/** OMR 채점 기록 — 최근 10개 */
export function saveOmrResult(cat, no, res) {
  const p = readProgress(cat, no);
  p.omr = [{ ...res, at: new Date().toISOString() }, ...p.omr].slice(0, 10);
  writeProgress(cat, no, p);
  return p;
}

/** 종이처럼 풀기 — 문제지 위 답안(초안 · 채점 결과). { answers:{no: 답}, reads:{no: 손글씨 판독}, graded:{score,n,at,rows}|null } */
const PK = (cat, no) => `${LS(cat, no)}.paper`;
export function readPaper(cat, no) {
  try {
    const v = JSON.parse(localStorage.getItem(PK(cat, no)) || "null");
    if (v && typeof v === "object") return { answers: v.answers || {}, reads: v.reads || {}, graded: v.graded || null };
  } catch { /* 무시 */ }
  return { answers: {}, reads: {}, graded: null };
}
export function savePaper(cat, no, paper) {
  try { localStorage.setItem(PK(cat, no), JSON.stringify({ answers: paper.answers || {}, reads: paper.reads || {}, graded: paper.graded || null })); return true; }
  catch { return false; }
}
export function clearPaper(cat, no) { try { localStorage.removeItem(PK(cat, no)); } catch { /* 무시 */ } }

/** 세트 진도 요약 { done, ok, n } */
export function progressSummary(set, p) {
  const ids = (set?.items || []).map((it) => it.id);
  let done = 0, ok = 0;
  for (const id of ids) { const r = p.items[id]; if (r) { done++; if (r.ok) ok++; } }
  return { done, ok, n: ids.length };
}

// ── 파일 ──────────────────────────────────────────────────────────────────────
/** 받을 때의 한글 파일 이름 — "01-야구-문제.pdf" */
export function downloadName(set, doc) {
  const d = DOCS.find((x) => x.id === doc) || DOCS[0];
  return `${set.key}-${d.suf}.pdf`;
}
/** PDF 받기 주소 — ?download= 로 한글 파일 이름을 붙인다 */
export function pdfUrl(cat, set, doc) {
  const d = DOCS.find((x) => x.id === doc) || DOCS[0];
  return `${FILES_BASE}/${cat}/${pad2(set.no)}/${d.id}.pdf?download=${encodeURIComponent(downloadName(set, doc))}`;
}
/** 내려받기 없이 PDF 만 (ZIP 묶을 때 fetch) */
export function pdfRawUrl(cat, no, doc) { return `${FILES_BASE}/${cat}/${pad2(no)}/${doc}.pdf`; }

/** 파일 목록(files.json — 쪽 수 · 크기 · sha256). 없으면 null */
const filesCache = new Map();
export async function loadFiles(cat = "prob") {
  if (filesCache.has(cat)) return filesCache.get(cat);
  let j = null;
  try { j = await getJson(`${CS_BASE}/${cat}/files.json`); } catch { j = null; }
  filesCache.set(cat, j);
  return j;
}
export function fileInfo(files, no, doc) { return files?.sets?.[pad2(no)]?.[doc] || null; }
export function fmtBytes(n) {
  if (!(n > 0)) return "";
  return n >= 1e6 ? `${(n / 1e6).toFixed(1)}MB` : `${Math.max(1, Math.round(n / 1e3))}KB`;
}
/** 인쇄용 HTML (문제지 · 해설지 — 같은 사이트) */
export const printUrl = (cat, no, doc) => `${CS_BASE}/${cat}/print/${pad2(no)}-${doc}.html`;
