// ashrain.out — 촬영 답안 보관 게이트 · 순수 함수 (DOM 없음 · LLM 없음 · 결정적)
//
// 배경: 답안이 원 문항을 "복원할 수 있느냐"가 아니라 원 문항의 창작적 "표현이 옮겨졌느냐"가 잣대다
// (LEGAL-판례조사-답안보관-v1). 그래서 게이트는 두 축으로 정한다.
//   1축  문항 표현 등급 S/M/C (촬영 시 서버가 LLM 으로 판정 — 발문표준성 검토 v2 기준)
//   2축  문항–답안 겹침 (여기서 결정적으로 계산): 조건 문장 재진술 · 긴 문자열 공유 · 소재어 재현 · 수치 재현
// 둘을 정책(app_settings.photo_retention)에 넣어 답안 원문의 보관 위치를 정한다.
//   labels : 서버에는 라벨만, 원문은 기기(IndexedDB)에만        ← 법률 검토 전 기본값
//   gated  : S → 중앙 · M → 겹침 낮음이면 중앙 · C → 기기        ← Q1·Q2 회신 뒤
//   all    : 전부 중앙 (연구용 · 쓰지 않음)
// 서버(api/photo.js)와 클라이언트가 같은 함수를 쓴다 — 결과가 어긋나지 않게 이 파일만 고친다.

export const POLICIES = ["labels", "gated", "all"];
export const DEFAULT_POLICY = "labels";
export const GRADES = ["S", "M", "C"];

// 겹침 점수 임계값 (0~100). 복원력 v2 자료로 보정한 초기값 — 정기 표본 감사에서 조정한다.
export const OVERLAP_LOW = 30;    // 미만이면 낮음
export const OVERLAP_HIGH = 60;   // 이상이면 높음
// 조건 문장 재진술로 보는 최소 길이(공백 제외 글자) · 공유 문자열 최소 길이
export const SENT_MIN = 10;
export const RUN_MIN = 8;

// ── 정규화 ─────────────────────────────────────────────────────────────────
const PARTICLE_TAIL = /(?:에서는|으로는|에서도|보다도|까지의|부터의|에서의|에게|에서|으로|보다|부터|까지|처럼|마다|이며|이면서|이면|이고|인지|이라|이나|만큼|가|이|은|는|을|를|의|와|과|도|로|에|만|나|인)$/;
// 흔한 발문·기능어 — 소재어로 세지 않는다
const STOP = new Set([
  "구하시오", "구하여라", "구하라", "고르시오", "구하면", "구하는", "구하기", "값을", "값은", "것은", "것을", "다음", "때", "일", "이때",
  "모두", "각각", "만족", "만족하는", "만족시키는", "대하여", "대한", "경우", "개수", "합", "차", "곱", "몫", "나머지", "최댓값", "최솟값",
  "그림", "같이", "위", "아래", "앞", "뒤", "이상", "이하", "초과", "미만", "단", "단위", "정수", "자연수", "실수", "유리수", "무리수",
  "함수", "방정식", "부등식", "삼각형", "사각형", "직선", "원", "점", "선분", "각", "길이", "넓이", "부피", "둘레", "높이", "반지름",
  "두", "세", "네", "한", "수", "식", "답", "문제", "보기", "중", "옳은", "옳지", "않은", "모두", "고르면", "얼마", "몇", "이다", "있다", "없다",
]);
const DIGIT_RE = /[0-9]/;
// 용언 꼴(동사·형용사 활용) — 소재어가 아니다
const VERBISH = /(?:으면|면|는지|는가|있다|없다|이다|하다|되다|된다|한다|하여|하고|되어|되면|아서|어서|여서|니까|므로|라고|다고|이면|라면|하자|하면|한|된|되는|하는|있는|없는)$/;

/** 마커([[frac(1,2)]] 등)를 평문으로 — mathir 가 없어도 동작하도록 얕게 푼다 */
export function plainMath(s) {
  return String(s ?? "")
    .replace(/\[\[\s*frac\(([^,()]+),([^()]+)\)\s*\]\]/g, "$1/$2")
    .replace(/\[\[\s*pow\(([^,()]+),([^()]+)\)\s*\]\]/g, "$1^$2")
    .replace(/\[\[\s*sqrt\(([^()]+)\)\s*\]\]/g, "√$1")
    .replace(/\[\[\s*deg\(([^()]+)\)\s*\]\]/g, "$1°")
    .replace(/\[\[\s*seg\(([^()]+)\)\s*\]\]/g, "$1")
    .replace(/\[\[\s*angle\(([^()]+)\)\s*\]\]/g, "∠$1")
    .replace(/\[\[\s*point\(([^()]+)\)\s*\]\]/g, "($1)")
    .replace(/\[\[|\]\]/g, "");
}

/** 비교용 정규화: 마커 풀기 · 유니코드 마이너스·공백 통일 · 소문자 */
export function normalize(s) {
  return plainMath(s)
    .replace(/[−–—]/g, "-")
    .replace(/[×·]/g, "*")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}
const squash = (s) => normalize(s).replace(/\s+/g, "");

/** 문장 나누기(공백 제외 SENT_MIN 자 이상만) */
export function sentencesOf(s) {
  return normalize(s)
    .split(/(?<=[.。!?])\s+|\n+/)
    .map((x) => x.trim())
    .filter((x) => x.replace(/\s+/g, "").length >= SENT_MIN);
}

/** 숫자 토큰 집합 — 정수·소수·분수(a/b)·비(a:b). 문항 번호처럼 보이는 "1." 은 뺀다 */
export function numbersOf(s) {
  const out = new Set();
  const t = normalize(s).replace(/^\s*\(?\d{1,2}[.)]\s/, "");
  const re = /-?\d+(?:\.\d+)?(?:\s*[/:]\s*\d+(?:\.\d+)?)?/g;
  let m;
  const add = (v) => { if (/^-?\d$/.test(v) && (v === "1" || v === "2" || v === "0")) return; out.add(v); };   // 0·1·2 는 어디에나 있어 신호가 없다
  while ((m = re.exec(t))) {
    const v = m[0].replace(/\s+/g, "");
    add(v);
    if (/[/:]/.test(v)) v.split(/[/:]/).forEach(add);   // 45/500 → 45 · 500 도 같이 (분수 안의 수치가 문항의 수치다)
  }
  return out;
}

/** 소재어(내용 낱말) 집합 — 한글 2자 이상, 조사 떼기, 발문·기능어·숫자 제외 */
export function contentWords(s) {
  const out = new Set();
  const words = normalize(s).split(/[^가-힣a-z]+/).filter(Boolean);
  for (let w of words) {
    if (!/^[가-힣]+$/.test(w)) continue;   // 한글로만 된 낱말만(단위 g·cm 가 붙은 조각 제외)
    for (let k = 0; k < 2; k++) { const w2 = w.replace(PARTICLE_TAIL, ""); if (w2 === w || w2.length < 2) break; w = w2; }
    if (w.length < 2 || STOP.has(w) || DIGIT_RE.test(w)) continue;
    if (w.length >= 3 && VERBISH.test(w)) continue;
    out.add(w);
  }
  return out;
}

/** 가장 긴 공통 부분 문자열(공백 제거 기준) — 길이와 문자열 */
export function longestCommonRun(a, b) {
  const x = squash(a), y = squash(b);
  if (!x || !y) return { len: 0, text: "" };
  let prev = new Array(y.length + 1).fill(0), best = 0, end = 0;
  for (let i = 1; i <= x.length; i++) {
    const cur = new Array(y.length + 1).fill(0);
    for (let j = 1; j <= y.length; j++) {
      if (x[i - 1] === y[j - 1]) {
        cur[j] = prev[j - 1] + 1;
        if (cur[j] > best) { best = cur[j]; end = i; }
      }
    }
    prev = cur;
  }
  return { len: best, text: x.slice(end - best, end) };
}

/** 문항의 문장 가운데 답안에 그대로(공백 무시) 들어간 것 */
export function restatedSentences(question, answer) {
  const a = squash(answer);
  if (!a) return [];
  return sentencesOf(question).filter((s) => a.includes(s.replace(/\s+/g, "")));
}

/**
 * 문항–답안 겹침. 값이 클수록 답안이 문항의 표현을 많이 옮겼다.
 * → { score(0~100), level('low'|'mid'|'high'), sentences(재진술 문장 수), sentTotal, run(최장 공유 문자열 길이),
 *     words(공유 소재어 수), wordTotal, wordRatio, nums(공유 수치 수), numTotal, numRatio }
 * 가중치: 재진술 45 · 소재어 30 · 수치 25 — 수치는 풀이에 필연적으로 들어가므로 가장 가볍다(Addison-Wesley 논리로 0 은 아니다).
 */
export function overlapScore(question, answer) {
  const q = String(question ?? ""), a = String(answer ?? "");
  const sents = sentencesOf(q);
  const restated = restatedSentences(q, a);
  const run = longestCommonRun(q, a);
  const qw = contentWords(q), aw = contentWords(a);
  let words = 0; qw.forEach((w) => { if (aw.has(w)) words++; });
  const qn = numbersOf(q), an = numbersOf(a);
  let nums = 0; qn.forEach((v) => { if (an.has(v)) nums++; });
  const sentRatio = sents.length ? restated.length / sents.length : 0;
  const wordRatio = qw.size ? words / qw.size : 0;
  const numRatio = qn.size ? nums / qn.size : 0;
  // 긴 공유 문자열은 문장 단위로 안 잡혀도 재진술의 증거 — 재진술 비율의 하한으로 쓴다
  const runBoost = run.len >= RUN_MIN ? Math.min(1, (run.len - RUN_MIN + 4) / 24) : 0;
  const s = 45 * Math.max(sentRatio, runBoost * 0.6) + 30 * wordRatio + 25 * numRatio;
  const score = Math.round(Math.min(100, s));
  return {
    score, level: score >= OVERLAP_HIGH ? "high" : score >= OVERLAP_LOW ? "mid" : "low",
    sentences: restated.length, sentTotal: sents.length, run: run.len,
    words, wordTotal: qw.size, wordRatio: +wordRatio.toFixed(3),
    nums, numTotal: qn.size, numRatio: +numRatio.toFixed(3),
  };
}

/** 정책 문자열 정리 — 모르는 값은 기본값 */
export const normalizePolicy = (p) => (POLICIES.includes(String(p || "").trim()) ? String(p).trim() : DEFAULT_POLICY);

/**
 * 보관 방식 결정 → { where:'central'|'device', reason }
 *   grade: 'S'|'M'|'C'|null(판정 실패)   overlap: overlapScore() 결과   policy: 'labels'|'gated'|'all'
 */
export function decideRetention({ grade, overlap, policy } = {}) {
  const pol = normalizePolicy(policy);
  const g = GRADES.includes(grade) ? grade : null;
  const lvl = overlap?.level || "high";
  if (pol === "labels") return { where: "device", reason: "정책: 라벨만 서버 보관(법률 검토 전 기본값)" };
  if (pol === "all") return { where: "central", reason: "정책: 전부 중앙 보관" };
  if (!g) return { where: "device", reason: "문항 등급을 판정하지 못해 기기에만 보관" };
  if (g === "S") return { where: "central", reason: "표준(S) 문항 — 관용 표현이라 중앙 보관" };
  if (g === "M") {
    return lvl === "low"
      ? { where: "central", reason: "소폭 선택(M) 문항이지만 답안이 문항 표현을 거의 옮기지 않아 중앙 보관" }
      : { where: "device", reason: "소폭 선택(M) 문항이고 답안이 문항 표현을 옮겨 기기에만 보관" };
  }
  return { where: "device", reason: "창작적(C) 문항 — 기기에만 보관" };
}

/**
 * 서버에 남기는 라벨 — 문항·답안 텍스트가 들어갈 자리가 없다.
 * std: {item_grade, sub_type, elements}  overlap: overlapScore()  result: 기능별 결과(essay: total/max, process: criteria …)
 */
export function buildLabels({ feature, std, overlap, result, unit } = {}) {
  const lights = result?.criteria
    ? Object.fromEntries(Object.entries(result.criteria).map(([k, v]) => [k, v?.light || null]))
    : null;
  return {
    feature: String(feature || ""),
    unit_guess: unit || null,
    std_grade: GRADES.includes(std?.item_grade) ? std.item_grade : null,
    sub_type: std?.sub_type || null,
    el_grades: std?.elements || null,
    overlap_score: overlap?.score ?? null,
    overlap_level: overlap?.level ?? null,
    overlap_parts: overlap ? { sentences: overlap.sentences, run: overlap.run, words: overlap.words, nums: overlap.nums } : null,
    score: Number.isFinite(+result?.total) ? +result.total : null,
    max_score: Number.isFinite(+result?.max) ? +result.max : null,
    verdict: result?.verdict || null,
    lights,
    pitfalls: Array.isArray(result?.pitfall_tags) ? result.pitfall_tags.slice(0, 12) : null,
    error_kind: result?.error?.kind || null,
    mental_load: result?.mental_load || null,
  };
}
