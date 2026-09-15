// ashrain.out — 문장 표시(문제 읽기) 규칙 엔진 · 순수 함수 (DOM 없음 · LLM 없음 · 결정적)
//
// 1층(규칙 · 채점 대상)
//   NUM   동그라미 = 숫자 정보 (단위까지 한 덩어리: "54cm", "14 cm", "2 : 3", "(-1, -9)", "[[deg(90)]]")
//   SCALE 밑줄     = 숫자 앞에 붙은 척도 (둘레·시속·넓이…, 조사 제외: "둘레가" → "둘레")
//   BOUND 빗금     = 단서 경계 / 흐름 전환점 (쉼표 · 문장 끝 · "…이고/…일 때" 같은 연결 어미 — 연결 어미는 보너스)
// 2층(재량 · 채점 안 함) — 문항 labels(L21_traps)에서 유도할 수 있을 때만 시범에 보여 준다
//   EMPH  강조 승격 (놓치면 틀리는 것)   DIST  항목 구분 (v1 에서는 만들지 않음)
//
// 표시 위치는 토큰 인덱스 기준. tokens.map(t => t.text).join("") === text 가 항상 성립한다.
// 수식([[마커]] · x²−3x+2=0 · y = ax + b)은 한 토큰(math)으로 묶고 그 안의 숫자는 동그라미 치지 않는다.
// 단, 마커 자체가 값 하나인 경우([[deg(90)]] · [[frac(1,2)]] · [[5 * pi]])는 그 값이 곧 숫자 정보이므로 num 으로 본다.
// "[[seg(BC)]] = 14 cm" 처럼 (이름 = 값) 꼴은 합치지 않아 값 "14 cm" 가 동그라미 대상이 된다.

export const TIER1 = ["NUM", "SCALE", "BOUND"];
export const FUNC_LABEL = { NUM: "동그라미", SCALE: "밑줄", BOUND: "빗금", EMPH: "강조(두 줄)", DIST: "구분(물결)" };
export const FUNC_MEANING = { NUM: "숫자 정보", SCALE: "척도(무엇의 값인지)", BOUND: "단서 경계", EMPH: "놓치면 틀리는 것", DIST: "항목 구분" };

// ── 사전 ─────────────────────────────────────────────────────────────────────

// 척도 낱말 (조사 없이). 숫자 바로 앞(조사 1~2개 허용)에 오면 SCALE.
const SCALE_WORDS = [
  "둘레", "넓이", "부피", "겉넓이", "밑넓이", "옆넓이", "면적", "길이", "높이", "깊이", "두께", "폭", "너비",
  "밑변", "윗변", "아랫변", "가로", "세로", "반지름", "지름", "중심각", "각", "각도", "호", "현", "모선",
  "속력", "속도", "시속", "분속", "초속", "거리", "시간", "농도", "가격", "정가", "원가", "판매가", "할인가", "이익", "할인율",
  "예산", "비용", "배송비", "요금", "금액", "값", "개수", "합", "합계", "차", "차이", "곱", "몫", "나머지", "나이", "무게", "질량", "온도", "용량",
  "비", "비율", "닮음비", "축척", "확률", "평균", "평균값", "중앙값", "최빈값", "도수", "상대도수", "계급값", "계급", "총합",
  "인원", "인원수", "수", "점수", "득점", "최대공약수", "최소공배수", "공약수", "공배수", "배수", "약수",
  "기울기", "절편", "크기", "성공률", "정답률", "타율",
];
const SCALE_SET = new Set(SCALE_WORDS);
const DICT_SORTED = [...SCALE_WORDS].sort((a, b) => b.length - a.length);
// 두루 쓰이는 척도 낱말 — 바로 앞의 "X의" 까지 묶어 "반지름의 길이" 로 밑줄 친다
const GENERIC_SCALE = new Set(["길이", "크기", "값", "수", "개수"]);

// 한글 낱말 뒤에 붙는 조사(사전 낱말을 조사와 분리할 때만 쓴다)
const PARTICLE_RE = /^(?:에서는|으로는|에서도|보다도|까지의|부터의|에서의|에게|에서|으로|보다|부터|까지|처럼|마다|이며|이면서|이면|이고|인지|이라|이나|만큼|가|이|은|는|을|를|의|와|과|도|로|에|만|나|인)+$/;
// 척도 ↔ 숫자 사이에 끼어도 되는 조사 (보다·만큼·으로·에 는 "차이·수단" 이라 척도로 보지 않는다)
const OK_PARTICLE = /^(?:가|이|은|는|의|을|를|와|과|도|이가)$/;

// 라틴 단위 — 띄어 쓴 꼴("14 cm") 은 모두 허용, 붙여 쓴 꼴("54cm") 은 한 글자 m 만 제외(변수 3m 과 충돌)
const LATIN_UNITS = ["km/h", "m/s", "kWh", "cm³", "cm²", "cm3", "cm2", "km²", "km2", "mm²", "mm2", "m³", "m²", "m3", "m2",
  "mm", "cm", "km", "kg", "mg", "mL", "ml", "°C", "L", "g", "m", "%", "°"].sort((a, b) => b.length - a.length);
const LATIN_UNITS_TIGHT = LATIN_UNITS.filter((u) => u !== "m");
// 한글 단위 — 숫자에 바로 붙은 것만 ("10개", "56세", "3장")
const HANGUL_UNITS = ["킬로미터", "킬로그램", "센티미터", "밀리리터", "리터", "그램", "미터", "퍼센트", "시간", "학년", "학기", "개월",
  "번째", "종류", "자루", "마리", "켤레", "상자", "봉지", "가지", "호선", "걸음", "문제", "문항", "인분", "그루", "송이", "포기", "등분",
  "자리", "세트", "세대", "조각", "명", "원", "개", "세", "점", "쪽", "장", "회", "주", "배", "반", "병", "시", "분", "초", "번", "층",
  "살", "년", "월", "일", "도", "권", "대", "벌", "줄", "칸", "통", "잔", "판", "봉", "팀", "조", "등", "위", "곡", "편", "척", "채", "컵"]
  .sort((a, b) => b.length - a.length);

const HANGUL = /[가-힣ㄱ-ㅎㅏ-ㅣ]/;
const DIGIT = /[0-9]/;
const SIGN = /[-−+]/;
// 위·아래 첨자: ²³¹ ⁰-ⁿ ₀-ₜ ᵃ-ᵛ ʰ-ʸ ˠ-ˤ ᶻ
const SUP = "\u00b2\u00b3\u00b9\u2070-\u209c\u1d43-\u1d5b\u02b0-\u02b8\u02e0-\u02e4\u1dbb";
const SUPER = new RegExp(`[${SUP}]`);
const SUPER_RUN = new RegExp(`^[${SUP}]+$`);
// 수식 런(붙여 쓴 것)에 들어갈 수 있는 글자 — 마침표·쉼표·한글은 제외
const RUN_CHAR = new RegExp(`[A-Za-z0-9α-ωΑ-Ωπ√∠△□∆°′″'+\\-−×÷*/=<>≤≥≠^_|()${SUP}]`);
const RUN_START = /[A-Za-zα-ωΑ-Ωπ√∠△□∆]/;
const OP_CHARS = new Set(["=", "+", "−", "-", "×", "÷", "·", "*", "/", "<", ">", "≤", "≥", "≠", ":", "∥", "⊥", "∽", "≡", "≅", "→"]);
const TRAIL_OP = /[+\-−×÷*/=<>≤≥≠^_]$/;

// (순서쌍) "(2, 3)" · "(a, b)" · "(-1, m)"
const TUPLE_RE = /^\(\s*([^\s(),\[\]]{1,12})\s*,\s*([^\s(),\[\]]{1,12})\s*\)/;
const TUPLE_PART = new RegExp(`^[-−+]?(?:\\d+(?:\\.\\d+)?|\\d*[A-Za-z][A-Za-z0-9′${SUP}]*)$`);
const NUMERIC = /^[-−+]?\d+(?:\.\d+)?$/;
// 비 "2 : 3" · "1 : 2 : 3"
const RATIO_RE = /^\d+(?:\.\d+)?\s?:\s?\d+(?:\.\d+)?(?:\s?:\s?\d+(?:\.\d+)?)?(?![\d:])/;
const NUMBER_RE = /^[-−+]?\d+(?:\.\d+)?(?:(?:천|만|억)(?!큼))?/;

const cnt = (s, ch) => s.split(ch).length - 1;

function matchUnit(s, j, list) {
  for (const u of list) {
    if (s.startsWith(u, j)) {
      const after = s[j + u.length] || "";
      if (/[A-Za-z0-9]/.test(after)) continue;           // "3 mm" 를 "3 m"+"m" 로 읽지 않기
      return u;
    }
  }
  return null;
}
function matchHangulUnit(s, j) {
  for (const u of HANGUL_UNITS) {
    if (!s.startsWith(u, j)) continue;
    if (u === "일" && /^\s*때/.test(s.slice(j + 1))) return null;   // "270일 때" 의 '일' 은 서술어
    return u;
  }
  return null;
}
/** 숫자(또는 값 마커) 뒤에 붙은 단위를 읽는다 → [단위문자열(공백 포함), 단위] */
function readUnitAfter(s, j) {
  const ch = s[j] || "";
  if (ch === "%" || ch === "°") return [ch, ch];
  if (/[A-Za-z]/.test(ch)) { const u = matchUnit(s, j, LATIN_UNITS_TIGHT); return u ? [u, u] : null; }
  if (ch === " ") {
    const u = matchUnit(s, j + 1, LATIN_UNITS);
    if (u) return [" " + u, u];
    return null;
  }
  if (HANGUL.test(ch)) { const u = matchHangulUnit(s, j); return u ? [u, u] : null; }
  return null;
}

/** 마커 [[…]] 가 '값 하나' 인가 — deg(90) · frac(1,2) · mixed(1,1,2) · 5 * pi · 12 */
function markerIsValue(inner) {
  const rest = inner.replace(/\b(?:deg|frac|mixed|pow|sqrt|pi)\b/g, "");
  return !/[A-Za-zα-ωΑ-Ω]/.test(rest) && /\d/.test(inner);
}

/** 사전 낱말 + 조사 → [낱말, 조사] (아니면 null) */
function splitParticle(word) {
  for (const w of DICT_SORTED) {
    if (word.length > w.length && word.startsWith(w) && PARTICLE_RE.test(word.slice(w.length))) return [w, word.slice(w.length)];
  }
  return null;
}

const isOperand = (a) => a && (a.kind === "math" || a.kind === "num");
// 단순 이름: 마커(값 아닌 것) · △ABC · ∠AOB · x · AB · a₁
const isSimpleName = (a) => a && a.kind === "math" && (a.sub === "marker" || /^[∠△□∆]?[A-Za-z]{1,4}[′″]?[₀-₉]?$/.test(a.text));

/**
 * 문장 → 토큰. kind: word | num | math | punct | space | newline
 * 부가 필드: unit(숫자 단위) · p(조사) · sub(num: unit|ratio|point|marker|plain / math: expr|marker|run|point) · op(연산자 문장부호)
 */
export function tokenize(text) {
  const s = String(text ?? "");
  const n = s.length;
  const atoms = [];
  let i = 0;
  const push = (kind, text, extra) => atoms.push(Object.assign({ kind, text }, extra || {}));

  while (i < n) {
    const ch = s[i];
    if (ch === "\n") { push("newline", "\n"); i++; continue; }
    if (/[ \t\r\u00a0\u3000]/.test(ch)) {
      let j = i + 1; while (j < n && /[ \t\r\u00a0\u3000]/.test(s[j])) j++;
      push("space", s.slice(i, j)); i = j; continue;
    }
    // [[마커]]
    if (s.startsWith("[[", i)) {
      const e = s.indexOf("]]", i + 2);
      if (e > 0) {
        const raw = s.slice(i, e + 2);
        let j = e + 2;
        if (markerIsValue(raw.slice(2, -2))) {
          let text = raw, unit;
          const u = readUnitAfter(s, j);
          if (u) { text += u[0]; unit = u[1]; j += u[0].length; }
          push("num", text, { sub: "marker", unit });
        } else push("math", raw, { sub: "marker" });
        i = j; continue;
      }
    }
    // 줄 첫머리 번호 매기기 "1. " · "(1) " · "1) " → 표시 대상이 아닌 문장부호
    if ((i === 0 || s[i - 1] === "\n") && /^(?:\(?\d{1,2}[.)])\s/.test(s.slice(i, i + 5))) {
      const m = /^(?:\(?\d{1,2}[.)])/.exec(s.slice(i));
      push("punct", m[0], { sub: "label" }); i += m[0].length; continue;
    }
    // 자료 목록 "[ 46, 49, x, 51 ]" → 한 덩어리(수식) — 자료값은 단서가 아니라 자료다
    if (ch === "[" && s[i + 1] !== "[") {
      const m = /^\[\s*(?:[-−]?\d+(?:\.\d+)?|[A-Za-z])(?:\s*,\s*(?:[-−]?\d+(?:\.\d+)?|[A-Za-z]))+\s*\]/.exec(s.slice(i));
      if (m) { push("math", m[0], { sub: "list" }); i += m[0].length; continue; }
    }
    // (순서쌍)
    if (ch === "(") {
      const m = TUPLE_RE.exec(s.slice(i));
      if (m && TUPLE_PART.test(m[1]) && TUPLE_PART.test(m[2])) {
        const numeric = NUMERIC.test(m[1]) && NUMERIC.test(m[2]);
        push(numeric ? "num" : "math", m[0], { sub: "point" }); i += m[0].length; continue;
      }
    }
    // 숫자 (부호 포함)
    if (DIGIT.test(ch) || (SIGN.test(ch) && DIGIT.test(s[i + 1] || ""))) {
      const rest = s.slice(i);
      const r = RATIO_RE.exec(rest);
      if (r) { push("num", r[0], { sub: "ratio" }); i += r[0].length; continue; }
      const m = NUMBER_RE.exec(rest);
      let j = i + m[0].length, text = m[0], unit, sub = "plain", asRun = false;
      const next = s[j] || "";
      if (/[A-Za-z]/.test(next)) {
        const u = matchUnit(s, j, LATIN_UNITS_TIGHT);
        if (u) { text += u; unit = u; j += u.length; } else asRun = true;        // 3x · 2a → 수식
      } else if (/[√(^/|]/.test(next) || SUPER.test(next)) asRun = true;         // 3/4 · 2(x+1) · 3² → 수식
      else {
        if (next === "π") { text += "π"; j++; }
        const u = readUnitAfter(s, j);
        if (u) { text += u[0]; unit = u[1]; j += u[0].length; }
      }
      if (!asRun) { push("num", text, { sub: unit ? "unit" : sub, unit }); i = j; continue; }
      // 수식 런으로 (아래 공통 처리)
      let k = i; while (k < n && RUN_CHAR.test(s[k])) k++;
      let run = s.slice(i, k);
      while (run.length > 1 && TRAIL_OP.test(run)) run = run.slice(0, -1);
      while (run.length > 1 && run.endsWith(")") && cnt(run, "(") < cnt(run, ")")) run = run.slice(0, -1);
      push("math", run, { sub: "run" }); i += run.length; continue;
    }
    // 수식 런 (문자·기호로 시작) · "(2x" 처럼 괄호로 시작하는 식
    if (RUN_START.test(ch) || (ch === "(" && /[A-Za-z0-9√\-−+]/.test(s[i + 1] || ""))) {
      let k = i; while (k < n && RUN_CHAR.test(s[k])) k++;
      let run = s.slice(i, k);
      while (run.length > 1 && TRAIL_OP.test(run)) run = run.slice(0, -1);
      while (run.length > 1 && run.endsWith(")") && cnt(run, "(") < cnt(run, ")")) run = run.slice(0, -1);
      if (run === "(") { push("punct", "("); i++; continue; }
      push("math", run, { sub: "run" }); i += run.length; continue;
    }
    // 한글 낱말 (사전 낱말이면 조사를 떼어 낸다)
    if (HANGUL.test(ch)) {
      let k = i; while (k < n && HANGUL.test(s[k])) k++;
      const word = s.slice(i, k);
      const sp = splitParticle(word);
      if (sp) { push("word", sp[0]); push("word", sp[1], { p: true }); }
      else push("word", word);
      i = k; continue;
    }
    // 연산자 하나 (띄어 쓴 "x = 3" 의 '=')
    if (OP_CHARS.has(ch)) { push("punct", ch, { op: true }); i++; continue; }
    push("punct", ch); i++;
  }

  // 띄어 쓴 수식 연쇄 병합: operand (공백? 연산자 공백? operand)+  → 한 math 토큰
  const out = [];
  let a = 0;
  while (a < atoms.length) {
    const first = atoms[a];
    if (!isOperand(first)) { out.push(first); a++; continue; }
    const chain = [first]; let j = a, ops = 0, lastOp = null;
    for (;;) {
      let k = j + 1; const buf = [];
      if (atoms[k]?.kind === "space" && !atoms[k].text.includes("\n") && atoms[k].text.length <= 2) buf.push(atoms[k++]);
      const op = atoms[k];
      if (!op || !(op.kind === "punct" && op.op)) break;
      buf.push(op); k++;
      if (atoms[k]?.kind === "space" && atoms[k].text.length <= 2) buf.push(atoms[k++]);
      const b = atoms[k];
      if (!isOperand(b)) break;
      buf.push(b); chain.push(...buf); ops++; lastOp = op.text; j = k;
    }
    if (ops === 0) { out.push(first); a++; continue; }
    const last = chain[chain.length - 1];
    // (이름 = 값) 은 합치지 않는다 — "[[seg(BC)]] = 14 cm", "x = 3", "[[angle(A)]] = [[deg(90)]]"
    if (ops === 1 && lastOp === "=" && isSimpleName(first) && last.kind === "num") { out.push(...chain); a = j + 1; continue; }
    let text = chain.map((x) => x.text).join("");
    let e = j + 1;
    while (atoms[e] && atoms[e].kind === "punct" && atoms[e].text === ")" && cnt(text, "(") > cnt(text, ")")) { text += ")"; e++; }
    while (atoms[e] && atoms[e].kind !== "space" && atoms[e].kind !== "newline" && (SUPER_RUN.test(atoms[e].text) || /^[°′″]$/.test(atoms[e].text))) { text += atoms[e].text; e++; }
    out.push({ kind: "math", text, sub: "expr" });
    a = e;
  }
  return out.map((t, idx) => Object.assign(t, { i: idx }));
}

// ── 문장 구조 도우미 ─────────────────────────────────────────────────────────

const isContent = (t) => t && t.kind !== "space" && t.kind !== "newline";
const jongOf = (ch) => { const c = ch.charCodeAt(0) - 0xac00; return c >= 0 && c < 11172 ? c % 28 : -1; };
function prevContent(tokens, i) { for (let k = i - 1; k >= 0; k--) if (isContent(tokens[k])) return tokens[k]; return null; }
function nextContent(tokens, i) { for (let k = i + 1; k < tokens.length; k++) if (isContent(tokens[k])) return tokens[k]; return null; }

// 쉼표 앞 낱말이 이렇게 끝나면 절(節) 경계 — "…이고," "…일 때," "…에서," "…하는데,"
const CLAUSE_FINAL = /(?:고|때|데|서|며|면|나|니|라|다|지|어|아|여|게|로|요|자|든|만|뒤|후|전|즉|또|또는|다음|이제|한편)$/;
const QUOTE_END = /(?:다고|라고|자고|냐고|으라고|려고|으려고)$/;   // 인용·의도("…려고") 는 경계가 아니다
const NOUN_MYEON = new Set(["평면", "밑면", "옆면", "단면", "겉면", "표면", "정면", "뒷면", "앞면", "화면", "지면", "수면", "측면", "곡면",
  "전면", "후면", "반면", "라면", "냉면", "가면", "도면", "장면", "국면", "방면", "다면", "삼면", "양면", "사면", "윗면", "아랫면", "면"]);
const NOUN_GO = new Set(["최고", "창고", "재고", "광고", "참고", "원고", "비고", "물고", "고"]);
const NOUN_DE = new Set(["가운데", "한가운데", "데"]);
const LABEL_DOT = /^(?:[ㄱ-ㅎ]|[A-Za-z]|[①-⑳㉠-㉻])$/;

/** 연결 어미 판정 → why 문자열 | null */
function connectiveWhy(tokens, i) {
  const t = tokens[i];
  if (t.kind !== "word") return null;
  const w = t.text;
  if (w === "때" || w === "때는" || w === "때에") {
    const p = prevContent(tokens, i);
    if (p && p.kind === "word" && (jongOf(p.text[p.text.length - 1]) === 8 || p.text === "일")) return "when";
    return null;
  }
  if (w === "인") {
    const p = tokens[i - 1];
    if (p && (p.kind === "num" || p.kind === "math")) return "copula";
    return null;
  }
  if (t.p) return null;                       // 사전 낱말에서 떼어 낸 조사(이고·이며 등)는 particleConnective 가 본다
  if (w.length < 2) return null;
  if (/고$/.test(w) && !QUOTE_END.test(w) && !NOUN_GO.has(w)) return "and";
  if (/(?:며|면서)$/.test(w)) return "and";
  if (/면$/.test(w) && !NOUN_MYEON.has(w)) return "if";
  if (/데$/.test(w) && !NOUN_DE.has(w)) return "but";
  return null;
}
// 조사로 떼어 낸 "이고/이며/이면" 도 연결 어미다
function particleConnective(t) {
  if (!t || !t.p) return null;
  if (/(?:이고|이며|이면서)$/.test(t.text)) return "and";
  if (/이면$/.test(t.text)) return "if";
  return null;
}

const BOUND_NOTE = {
  clause: "쉼표 — 조건 하나가 끝나고 다음 조건이 시작되는 자리예요",
  comma: "쉼표 — 흐름이 잠깐 끊기는 자리예요 (표시하면 좋아요)",
  sentence: "문장이 끝났어요 — 여기까지를 한 덩어리로 읽어요",
  and: "‘…고/…며’ — 조건이 이어지는 자리예요 (표시하면 조건이 몇 개인지 보여요)",
  if: "‘…면’ — 가정(조건)이 끝나는 자리예요",
  but: "‘…데’ — 상황 설명이 끝나고 다음 이야기가 시작돼요",
  when: "‘…일 때’ — 조건이 끝나고 구하는 것이 시작되는 자리예요",
  copula: "‘…인’ — 조건 설명이 끝나고 대상이 나오는 자리예요",
};

function numNote(t) {
  if (t.sub === "ratio") return "비(比)도 숫자 정보예요 — 두 수를 함께 묶어요";
  if (t.sub === "point") return "좌표도 숫자 정보예요 — 순서쌍을 한 덩어리로 묶어요";
  if (/^[-−]/.test(t.text)) return "음수예요 — 부호(−)까지 함께 동그라미 쳐요";
  if (t.unit) return `숫자 정보예요 — 단위(${t.unit.trim()})까지 한 덩어리로 동그라미 쳐요`;
  if (t.sub === "marker") return "각의 크기·분수도 숫자 정보예요 — 계산에 쓰는 값이에요";
  return "숫자 정보예요 — 계산에 쓰는 값이에요";
}

/** NUM 토큰 앞의 척도 낱말 찾기 → { t0, t1, word } | null */
function findScale(tokens, ni) {
  const num = tokens[ni];
  if (num.unit === "배" || num.unit === "번째") return null;       // "3배" 는 배수, 척도 아님
  let k = ni - 1, hops = 0, found = -1;
  while (k >= 0 && hops <= 2) {
    const t = tokens[k];
    if (!isContent(t)) { k--; continue; }
    if (t.kind !== "word") return null;
    if (SCALE_SET.has(t.text) && !t.p) { found = k; break; }
    if (OK_PARTICLE.test(t.text)) { k--; hops++; continue; }
    return null;
  }
  if (found < 0) return null;
  let t0 = found;
  const word = tokens[found].text;
  if (GENERIC_SCALE.has(word)) {
    // "반지름의 길이" · "학생의 수" — 바로 앞의 "X의" 까지 묶는다 (X 가 사전 낱말이면 "반지름"+"의" 로 나뉘어 있다)
    let a = found - 1; while (a >= 0 && !isContent(tokens[a])) a--;
    if (a >= 0 && tokens[a].kind === "word") {
      if (tokens[a].text === "의") {
        let b = a - 1; while (b >= 0 && !isContent(tokens[b])) b--;
        if (b >= 0 && tokens[b].kind === "word" && !tokens[b].p && !CLAUSE_FINAL.test(tokens[b].text)) t0 = b;
      } else if (/의$/.test(tokens[a].text) && tokens[a].text.length >= 2 && !tokens[a].p) t0 = a;
    }
  }
  return { t0, t1: found, word: tokens.slice(t0, found + 1).map((t) => t.text).join("").trim() };
}

/**
 * 1층 표시 정답(키). text 대신 tokenize() 결과를 넘겨도 된다.
 * span: { kind:"span", t0, t1, func:"NUM"|"SCALE", required, tier:1, note }
 * point: { kind:"point", t0, func:"BOUND", required, tier:1, why, note }  — t0 번째 토큰 '뒤' 에 빗금
 */
export function autoMark(text) {
  const tokens = Array.isArray(text) ? text : tokenize(text);
  const marks = [];
  // NUM
  for (const t of tokens) if (t.kind === "num") marks.push({ kind: "span", t0: t.i, t1: t.i, func: "NUM", required: true, tier: 1, note: numNote(t) });
  // SCALE
  const used = new Set();
  for (const m of marks.slice()) {
    const sc = findScale(tokens, m.t0);
    if (!sc || used.has(sc.t1)) continue;
    used.add(sc.t1);
    marks.push({ kind: "span", t0: sc.t0, t1: sc.t1, func: "SCALE", required: true, tier: 1, word: sc.word,
      note: `‘${sc.word}’ — 숫자 ${tokens[m.t0].text.trim()}가 무엇의 값인지 알려 주는 척도예요. 조사(가·는·의)는 빼고 밑줄을 쳐요` });
  }
  // BOUND
  const pts = [];
  const add = (i, required, why) => pts.push({ kind: "point", t0: i, func: "BOUND", required, tier: 1, why, note: BOUND_NOTE[why] });
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    if (t.kind === "punct") {
      if (t.text === ",") {
        const p = prevContent(tokens, i), q = nextContent(tokens, i);
        if (!p || !q) continue;
        if (p.text === "단" || p.kind === "punct") continue;     // "(단, …)" 관용구
        if (p.kind === "word" && CLAUSE_FINAL.test(p.text)) { add(i, true, "clause"); continue; }
        if (q.kind === "num" || q.kind === "math") continue;     // 나열 쉼표: "A, B" · "4명, A명" · "(2, 0), (6, -8)"
        add(i, false, "comma");
      } else if (t.text === "." || t.text === "?" || t.text === "!") {
        const p = prevContent(tokens, i);
        let q = nextContent(tokens, i);
        while (q && q.kind === "punct" && /^[(\[{「“‘]$/.test(q.text)) q = nextContent(tokens, q.i);   // "(단, …)" 앞의 여는 괄호는 건너뛴다
        if (!q || q.kind === "punct") continue;                  // 마지막 문장부호 · "…쓰시오.)"
        if (!p || p.kind === "punct") continue;
        if (LABEL_DOT.test(p.text)) continue;                    // "ㄱ." "A." 같은 항목 표시
        if (p.kind === "num" && /^\d+$/.test(p.text)) {          // 줄 첫머리 "1." 번호 매기기
          let k = p.i - 1; while (k >= 0 && tokens[k].kind === "space") k--;
          if (k < 0 || tokens[k].kind === "newline") continue;
        }
        add(i, true, "sentence");
      }
      continue;
    }
    if (t.kind !== "word") continue;
    const why = connectiveWhy(tokens, i) || particleConnective(t);
    if (!why) continue;
    const q = nextContent(tokens, i);
    if (!q) continue;                                            // 마지막 낱말
    if (q.kind === "punct" && /^[,.?!]$/.test(q.text)) continue; // 바로 뒤 문장부호가 경계를 만든다
    add(i, false, why);
  }
  marks.push(...pts);
  return marks.sort((x, y) => x.t0 - y.t0 || (x.kind === y.kind ? 0 : x.kind === "span" ? -1 : 1));
}

// ── 구하는 것 · 주어진 조건 ──────────────────────────────────────────────────

const ASK_VERB = /(?:(을|를|은|는|이|가)\s*)?(구하시오|구하여라|구하라|구하세요|구해라|구해\s*보시오|구하면|구하고|구하는\s*(?:과정|식|방법)(?:을|를)?\s*(?:쓰시오|서술하시오|설명하시오)|구하는|쓰시오|써라|써\s*보시오|써넣으시오|쓰면|고르시오|고르면|고르세요|나타내시오|나타내면|나타내어라|풀어라|푸시오|풀면|풀이하시오|답하시오|말하시오|계산하시오|계산하여라|계산하면|설명하시오|서술하시오|증명하시오|보이시오|찾으시오|찾아라|정하시오|알아보시오|비교하시오|판별하시오|구별하시오|구분하시오|확인하시오|완성하시오|채우시오|나열하시오|표시하시오|그리시오|택하시오|선택하시오|간단히\s*하시오|전개하시오|인수분해하시오|얼마인가|얼마인지|얼마입니까|무엇인가|무엇인지)\s*[.?!)]?\s*$/;
const INTERROG = /(?:몇|얼마|어느|무엇|어떤|누구|언제|어디)/;
// 관형어(수식어) — 뒤의 명사구가 '구하는 것' 이 되도록 앞을 잘라 낸다. 명사+는(거리는·넓이는) 과 헷갈리지 않게 보수적으로.
const MOD_EXACT = new Set(["긴", "큰", "작은", "같은", "다른", "짧은", "넓은", "높은", "낮은", "많은", "적은", "무거운", "가벼운", "빠른", "느린",
  "옳은", "알맞은", "남은", "늘어난", "줄어든", "필요한", "가능한", "평행한", "새로운", "얻은", "받은", "고른", "뽑은", "꺼낸", "던진", "굴린",
  "나온", "택한", "읽은", "걸린", "맞힌", "틀린", "더한", "뺀", "곱한", "나눈", "이은", "자른", "세운", "그린", "만든", "놓은", "놓인",
  "주어진", "그려진", "이루어진", "둘러싸인", "연결한", "지나는", "만나는", "이루는", "그리는", "나타내는", "지나가는", "이어지는", "겹치는",
  "접하는", "만드는", "늘어나는", "줄어드는", "나오는", "들어가는", "남는", "따르는", "이르는", "걸리는", "움직이는", "달리는", "걷는", "타는",
  "가는", "오는", "사는", "뽑는", "던지는", "굴리는", "꺼내는", "나누는", "속하는", "해당하는", "대응하는", "이동하는", "출발하는", "도착하는",
  "시작하는", "끝나는", "성립하는", "만족하는", "만족시키는", "포함하는", "포함된", "할인된", "증가한", "감소한", "늘린", "줄인", "구한",
  "나타낸", "되는", "된", "있는", "없는"]);
const MOD_SUFFIX = /(?:하는|되는|있는|없는|시키는|어지는|해진|어진|아진)$/;
const NOUN_IN = /(?:원인|할인|개인|확인|요인|무인|법인|주인|성인)$/;
const isModifier = (w) => MOD_EXACT.has(w) || MOD_SUFFIX.test(w) || (/인$/.test(w) && w.length >= 2 && !NOUN_IN.test(w));
const BAD_ASK_START = /^(?:것|수|때|지|데|이|가|은|는|을|를|의|에|도|만|중)/;

const rangeText = (tokens, a, b) => tokens.slice(a, b + 1).map((t) => t.text).join("");
const tidy = (s) => {
  let t = String(s).replace(/^[\s,.?!]+|[\s,.?!]+$/g, "");
  if (/^\(/.test(t) && /\)$/.test(t) && cnt(t, "(") === 1) t = t.slice(1, -1).replace(/^[\s,.?!]+|[\s,.?!]+$/g, "");
  return t;
};
const contentChars = (s) => s.replace(/\[\[\s*[a-z]+\(([^\]]*)\)\s*\]\]/g, "$1").replace(/\[\[|\]\]/g, "").replace(/\s/g, "");
const wordCount = (s) => tidy(s).split(/\s+/).filter(Boolean).length;

/** [a,b] 토큰 범위를 경계(토큰 뒤 위치) 목록으로 잘라 절 목록으로 */
function splitRange(tokens, a, b, cutsAfter) {
  const out = []; let s = a;
  for (const c of cutsAfter) { if (c < a || c >= b) continue; out.push([s, c]); s = c + 1; }
  out.push([s, b]);
  return out.map(([x, y]) => { while (x <= y && !isContent(tokens[x])) x++; while (y >= x && !isContent(tokens[y])) y--; return [x, y]; }).filter(([x, y]) => x <= y);
}

/** 구하는 것 · 주어진 조건 분석 */
function analyze(tokens, marks) {
  const last = tokens.length - 1;
  if (last < 0) return { asking: null, givens: [], askingRange: null };
  const sentenceCuts = [], clauseCuts = [], bonusCuts = [], givenCuts = [];
  for (const m of marks) {
    if (m.func !== "BOUND") continue;
    if (m.why === "sentence") sentenceCuts.push(m.t0);
    else if (m.required) { clauseCuts.push(m.t0); givenCuts.push(m.t0); }
    else { bonusCuts.push(m.t0); if (m.why !== "copula") givenCuts.push(m.t0); }   // "…인" 은 명사구 안이라 조건을 쪼개지 않는다
  }
  tokens.forEach((t) => { if (t.kind === "newline") sentenceCuts.push(t.i); });
  sentenceCuts.sort((x, y) => x - y);
  givenCuts.sort((x, y) => x - y);
  const sentences = splitRange(tokens, 0, last, sentenceCuts);
  const isNote = (k) => { const tx = rangeText(tokens, sentences[k][0], sentences[k][1]).trim(); return /^\(/.test(tx) && /\)$/.test(tx) && cnt(tx, "(") === 1; };   // "(단, …)" 같은 덧붙임

  // 묻는 문장: 뒤에서부터 구하시오/…? 가 있는 문장 (덧붙임 문장은 건너뛴다)
  let askIdx = -1;
  for (let k = sentences.length - 1; k >= 0; k--) {
    if (isNote(k)) continue;
    const tx = rangeText(tokens, sentences[k][0], sentences[k][1]);
    if (ASK_VERB.test(tx) || /\?\s*$/.test(tx)) { askIdx = k; break; }
  }
  if (askIdx < 0) for (let k = sentences.length - 1; k >= 0; k--) if (!isNote(k) && HANGUL.test(rangeText(tokens, ...sentences[k]))) { askIdx = k; break; }

  const givens = [];
  let asking = null, askingRange = null;
  sentences.forEach(([a, b], k) => {
    if (k !== askIdx) { for (const [x, y] of splitRange(tokens, a, b, givenCuts)) givens.push(tidy(rangeText(tokens, x, y))); return; }
    // 묻는 문장: 필수 경계 뒤가 후보, 보너스 경계는 그 사이에 의문사(몇·얼마)가 없을 때만 넘어간다
    const req = clauseCuts.filter((c) => c >= a && c < b);
    let start = req.length ? req[req.length - 1] + 1 : a;
    const pre = splitRange(tokens, a, start - 1, givenCuts);
    for (const [x, y] of pre) givens.push(tidy(rangeText(tokens, x, y)));
    for (const c of bonusCuts.filter((c) => c >= start && c < b).sort((x, y) => x - y)) {
      const seg = rangeText(tokens, start, c);
      if (INTERROG.test(seg)) break;
      givens.push(tidy(seg)); start = c + 1;
    }
    while (start <= b && !isContent(tokens[start])) start++;
    const clause = rangeText(tokens, start, b);
    let ask = tidy(clause);
    const vm = ASK_VERB.exec(ask);
    if (vm) ask = ask.slice(0, vm.index).trim();
    else { ask = ask.replace(/[?!.]\s*$/, "").trim(); ask = ask.replace(/(?:을|를|은|는)$/, "").trim(); }
    ask = ask.replace(/(?:구하는\s*(?:과정|식|방법)|과정)(?:을|를)?$/, "").trim();
    // "것을 모두 고르시오" — 부사를 떼고 남은 목적격 조사(을·를)도 뗀다 (은·는 은 '작은·옳은' 과 헷갈려 ? 꼴에서만)
    const adv = /\s+(?:모두|각각|다|전부)$/.test(ask);
    ask = ask.replace(/\s+(?:모두|각각|다|전부)$/, "").trim();
    if (adv && /[가-힣]+(?:을|를)$/.test(ask)) ask = ask.replace(/(?:을|를)$/, "").trim();
    // 관형절 분리: "가로가 세로보다 3cm 더 긴 | 직사각형의 넓이" (뒤쪽이 의문사로 시작하면 주어부라 자르지 않는다)
    const words = ask.split(" ");
    for (let w = words.length - 2; w >= 0; w--) {
      if (!isModifier(words[w])) continue;
      const head = words.slice(0, w + 1).join(" "), tail = words.slice(w + 1).join(" ");
      const nounish = tail.includes("의") || tail.split(" ").length >= 2;    // "직사각형의 넓이" · "점이 나타내는 수" — 맨 명사 하나("모서리")는 자르지 않는다
      if (nounish && contentChars(tail).length >= 3 && !BAD_ASK_START.test(tail) && !INTERROG.test(head) && !INTERROG.test(tail)) { givens.push(tidy(head)); ask = tail; }
      break;
    }
    asking = ask || null;
    if (asking) {
      const off = clause.lastIndexOf(asking);
      if (off >= 0) {
        let pos = 0, r0 = -1, r1 = -1;
        for (let t = start; t <= b; t++) {
          const len = tokens[t].text.length;
          if (r0 < 0 && pos + len > off) r0 = t;
          if (pos + len >= off + asking.length) { r1 = t; break; }
          pos += len;
        }
        if (r0 >= 0 && r1 >= r0) askingRange = [r0, r1];
      }
    }
  });
  // 너무 잘린 조각(낱말 하나)은 앞 조각에 붙인다
  const merged = [];
  for (const g of givens) {
    if (!g) continue;
    if (merged.length && wordCount(g) < 2 && !/\d/.test(g)) merged[merged.length - 1] += " " + g;
    else merged.push(g);
  }
  return { asking, givens: merged, askingRange };
}

// ── 2층(재량) · 함정 ─────────────────────────────────────────────────────────

export const TRAP_TEXT = {
  "구하는대상혼동": "무엇을 구하는지 헷갈리기 쉬워요",
  "부호": "부호(+, −)를 놓치기 쉬워요",
  "단위": "단위를 맞추는 걸 잊기 쉬워요",
  "단위환산": "단위 환산을 잊기 쉬워요",
  "조건누락": "조건 하나를 빠뜨리기 쉬워요",
  "역연산": "공식을 거꾸로(역으로) 풀어야 해요",
  "평균오용": "평균을 그냥 평균 내면 안 돼요",
  "제곱누락": "제곱(²)을 빠뜨리기 쉬워요",
  "계산실수": "계산 실수가 나기 쉬워요",
};
export const trapText = (tag) => TRAP_TEXT[tag] || String(tag || "");

function deriveTier2(tokens, marks, st, traps) {
  const out = [];
  const nums = tokens.filter((t) => t.kind === "num");
  const has = (x) => traps.includes(x);
  const seen = new Set();
  const emph = (t0, t1, note) => { const k = `${t0}:${t1}`; if (seen.has(k)) return; seen.add(k); out.push({ kind: "span", t0, t1, func: "EMPH", required: false, tier: 2, note }); };
  if (has("구하는대상혼동") && st.askingRange) emph(st.askingRange[0], st.askingRange[1], "구하는 것 — 중간에 나온 값을 답으로 쓰기 쉬워요. 마지막에 이걸 구했는지 확인해요");
  if (has("부호")) for (const t of nums) if (/^[-−]/.test(t.text) || /\(\s*[-−]|,\s*[-−]/.test(t.text)) emph(t.i, t.i, "부호(−)가 있어요 — 계산 끝까지 부호를 지켜요");
  if (has("단위") || has("단위환산")) {
    const units = new Set(nums.map((t) => t.unit).filter(Boolean));
    if (units.size >= 2) for (const t of nums) if (t.unit) emph(t.i, t.i, `단위(${t.unit.trim()})가 서로 달라요 — 하나로 맞춰야 해요`);
  }
  if (has("제곱누락")) for (const t of nums) if (/[²³]|cm2|m2|cm3|m3/.test(t.unit || "")) emph(t.i, t.i, "제곱(²)·세제곱(³) 단위 — 길이의 비를 그대로 쓰면 안 돼요");
  if (has("평균오용")) for (const m of marks) if (m.func === "SCALE" && m.word === "평균") {
    const nm = marks.find((x) => x.func === "NUM" && x.t0 > m.t1 && x.t0 - m.t1 <= 4);
    if (nm) emph(nm.t0, nm.t1, "평균 — 평균끼리 그냥 평균 내면 안 돼요. (평균 × 인원)으로 총합을 먼저 구해요");
  }
  return out;
}

/**
 * 문장 해설. item 은 test_items 행(없어도 됨).
 * → { tokens, marks(1층 + 2층), asking, givens, traps, prereq, discriminates, askingRange }
 */
export function explain(text, item) {
  const tokens = tokenize(text);
  const marks = autoMark(tokens);
  const st = analyze(tokens, marks);
  const labels = item?.labels || null;
  const rawTraps = Array.isArray(labels?.L21_traps) ? labels.L21_traps.filter((x) => typeof x === "string") : [];
  const tier2 = deriveTier2(tokens, marks, st, rawTraps);
  return {
    tokens,
    marks: [...marks, ...tier2],
    asking: st.asking,
    givens: st.givens,
    traps: rawTraps.map(trapText),
    prereq: Array.isArray(labels?.L15_prereq) ? labels.L15_prereq : [],
    discriminates: typeof labels?.L43_discriminates === "string" && labels.L43_discriminates ? labels.L43_discriminates : null,
    askingRange: st.askingRange,
  };
}

// ── 채점 ─────────────────────────────────────────────────────────────────────

/** 빗금 위치 비교용 — 공백 토큰을 뺀 위치 (tokens 가 없으면 인덱스 그대로) */
function contentPos(tokens, i) {
  if (!tokens) return i;
  let c = 0; for (let k = 0; k <= i && k < tokens.length; k++) if (isContent(tokens[k])) c++;
  return c;
}
function spanSet(tokens, m) {
  const s = new Set();
  for (let k = m.t0; k <= m.t1; k++) { const t = tokens?.[k]; if (!tokens || (isContent(t) && !t.p)) s.add(k); }
  return s;
}

/**
 * 학생 표시 vs 키. 1층(NUM·SCALE·BOUND)만 채점, 다른 func 은 무시.
 * span: 같은 func + 키 구간(조사·공백 제외)의 50% 이상 겹침 · point: 같은 func + 위치 차이 ≤ 1(공백 제외)
 * → { required, hit, missed:[key], extra:[user], score, detail:[{key, matched}], bonusHit }
 */
export function scoreMarks(userMarks, keyMarks, tokens) {
  const user = (userMarks || []).filter((m) => TIER1.includes(m.func));
  const keys = (keyMarks || []).filter((m) => TIER1.includes(m.func));
  const taken = new Set();
  const detail = [];
  // 겹침이 큰 순서로 짝 짓기
  const cands = [];
  keys.forEach((k, ki) => user.forEach((u, ui) => {
    if (u.func !== k.func || u.kind !== k.kind) return;
    let q = 0;
    if (k.kind === "span") {
      const ks = spanSet(tokens, k), us = spanSet(tokens, u);
      if (!ks.size) return;
      let ov = 0; ks.forEach((x) => { if (us.has(x)) ov++; });
      q = ov / ks.size;
      if (q < 0.5) return;
    } else {
      const d = Math.abs(contentPos(tokens, k.t0) - contentPos(tokens, u.t0));
      if (d > 1) return;
      q = 1 - d / 2;
    }
    cands.push({ ki, ui, q });
  }));
  cands.sort((x, y) => y.q - x.q);
  const kMatch = new Map();
  for (const c of cands) { if (kMatch.has(c.ki) || taken.has(c.ui)) continue; kMatch.set(c.ki, c.ui); taken.add(c.ui); }
  let required = 0, hit = 0, bonusHit = 0;
  const missed = [];
  keys.forEach((k, ki) => {
    const u = kMatch.has(ki) ? user[kMatch.get(ki)] : null;
    detail.push({ key: k, matched: u });
    if (k.required !== false) { required++; if (u) hit++; else missed.push(k); }
    else if (u) bonusHit++;
  });
  const extra = user.filter((_, ui) => !taken.has(ui));
  const score = required === 0 ? 100 : Math.round((hit / required) * 100);
  return { required, hit, missed, extra, score, detail, bonusHit };
}

/** 표시 연습에 쓸 만한 문장인가 — 공백 제외 30자 이상 + 필수 표시 2개 이상 */
export function practiceEligible(text) {
  const s = String(text ?? "");
  if (contentChars(s).length < 30) return false;
  return autoMark(s).filter((m) => m.required).length >= 2;
}

/** 표시가 가리키는 글자 (목록 표시용) — span: 토큰 텍스트, point: "‘,’ 뒤" */
export function markText(mark, tokens) {
  if (!mark || !tokens) return "";
  if (mark.kind === "span") return rangeText(tokens, mark.t0, mark.t1).trim();
  const t = tokens[mark.t0];
  return t ? `‘${t.text.trim()}’ 뒤` : "";
}

export const markKey = (m) => `${m.func}:${m.kind}:${m.t0}:${m.kind === "span" ? m.t1 : ""}`;
