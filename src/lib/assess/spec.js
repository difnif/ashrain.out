// ashrain.out — 서술형 평가 JSON(채팅방 생성기 산출물) 검사 · 공개용 분리 · 점수 합산 (순수 함수 — 서버·관리자 화면·테스트 공용)
//
// 흐름: 채팅방에서 PDF(확인·인쇄용) + JSON(앱 등록용)을 만든다 → 관리자 화면에서 JSON 을 올리면 validateSpec 통과 후 등록.
// 학생에게는 publicView(문제·배점·쪽 좌표)만 간다. 정답·모범 풀이·채점 기준은 서버에만 남고, 공개 시점(reveal)이 되면 결과 화면에 붙는다.
import { checkOf, SHEET_W, SHEET_H, MAX_PAGES, PAGECODE } from "./sheet.js";

export const SPEC_KIND = "ashrain.assess";
export const SPEC_VERSION = 1;
export const CODE_RE = /^[A-Z0-9]{4,12}$/;
export const REVEALS = ["after_submit", "after_close", "never"];
export const LEVELS = ["elem", "mid", "high"];
export const MAX_ITEMS = 13;               // 1쪽 안내 + 2쪽 응시 정보 + 문제 쪽(쪽 번호 4비트 → 15쪽)
export const MAX_SPEC_BYTES = 2_000_000;
export const MAX_SVG_BYTES = 200_000;
const UNSAFE_SVG = /<script|<foreignObject|<iframe|<object|<embed|<image|<use|\bon[a-z]+\s*=|javascript|&#|href\s*=/i;   // 그림은 <img> 로만 그리지만, 실행·외부 참조 흔적은 아예 받지 않는다

const isStr = (v) => typeof v === "string";
const nonEmpty = (v) => isStr(v) && v.trim().length > 0;
const isBox = (b) => Array.isArray(b) && b.length === 4 && b.every((v) => Number.isFinite(+v))
  && +b[0] >= 0 && +b[1] >= 0 && +b[2] <= SHEET_W && +b[3] <= SHEET_H && +b[2] > +b[0] && +b[3] > +b[1];

/** 기본 정책 — 채점 프롬프트로 간다. JSON 의 policy 가 있으면 덮어쓴다 */
export const DEFAULT_POLICY = { carry: "half", alt_method: "accept", answer_only_max: 3 };
export function policyOf(spec) {
  const p = { ...DEFAULT_POLICY, ...(spec?.policy || {}) };
  if (!["full", "half", "none"].includes(p.carry)) p.carry = DEFAULT_POLICY.carry;
  if (!["accept", "deduct"].includes(p.alt_method)) p.alt_method = DEFAULT_POLICY.alt_method;
  p.answer_only_max = Number.isFinite(+p.answer_only_max) ? Math.max(0, Math.round(+p.answer_only_max)) : DEFAULT_POLICY.answer_only_max;
  return p;
}

/**
 * JSON 검사. → { ok, errors[], warnings[], summary }
 * errors 가 하나라도 있으면 등록하지 않는다. warnings 는 보여 주기만.
 */
export function validateSpec(spec, { bytes = null } = {}) {
  const errors = [], warnings = [];
  const err = (m) => errors.push(m), warn = (m) => warnings.push(m);
  if (!spec || typeof spec !== "object" || Array.isArray(spec)) return { ok: false, errors: ["JSON 객체가 아니에요"], warnings, summary: null };
  if (bytes != null && bytes > MAX_SPEC_BYTES) err(`파일이 너무 커요 (${Math.round(bytes / 1024)}KB > ${MAX_SPEC_BYTES / 1000}KB)`);
  if (spec.kind !== SPEC_KIND) err(`kind 가 "${SPEC_KIND}" 가 아니에요 — 서술형 평가 생성기로 만든 JSON 인가요?`);
  if (+spec.version !== SPEC_VERSION) err(`version ${spec.version} 은 지원하지 않아요 (지원: ${SPEC_VERSION})`);
  if (!CODE_RE.test(String(spec.code || ""))) err("code 는 영문 대문자·숫자 4~12자여야 해요");
  if (!nonEmpty(spec.title)) err("title 이 비어 있어요");
  if (spec.level != null && !LEVELS.includes(spec.level)) err("level 은 elem·mid·high 중 하나");
  if (spec.date != null && !/^\d{4}-\d{2}-\d{2}$/.test(String(spec.date))) err("date 는 YYYY-MM-DD");
  if (spec.reveal != null && !REVEALS.includes(spec.reveal)) err("reveal 은 after_submit·after_close·never 중 하나");
  for (const k of ["opens_at", "closes_at"]) if (spec[k] != null && Number.isNaN(Date.parse(spec[k]))) err(`${k} 날짜 형식이 이상해요`);

  // 시트 · 쪽 번호 띠
  const sh = spec.sheet || {};
  if (+sh.w !== SHEET_W || +sh.h !== SHEET_H) err("sheet 좌표계가 1000×1414 가 아니에요");
  const pc = sh.pagecode || {};
  const num = (v) => Number.isFinite(+v) && v !== null && v !== "";
  if (!(+pc.n === PAGECODE.n && num(pc.x0) && num(pc.y0) && +pc.size > 0 && +pc.pitch > 0)) err("sheet.pagecode 값이 없거나 이 앱의 쪽 번호 띠(14칸)와 달라요 — 생성기로 다시 만들어 주세요");
  else if (+pc.x0 < 0 || +pc.x0 + +pc.pitch * (+pc.n - 1) + +pc.size > SHEET_W || +pc.y0 < 0 || +pc.y0 + +pc.size > SHEET_H) err("sheet.pagecode 좌표가 시트 밖이에요");
  if (!(+sh.markers?.size > 0 && num(sh.markers?.inset))) err("sheet.markers 값이 없어요");
  if (!["x", "y", "w", "h"].every((k) => num(sh.orient?.[k]))) err("sheet.orient 값이 없어요");
  if (CODE_RE.test(String(spec.code || "")) && +pc.check !== checkOf(spec.code)) err("쪽 번호 띠 확인값이 code 와 맞지 않아요 — code 를 손으로 바꿨다면 생성기로 다시 만들어 주세요");

  // 쪽
  const pages = Array.isArray(spec.pages) ? spec.pages : [];
  if (!pages.length) err("pages 가 없어요");
  if (pages.length > MAX_PAGES) err(`쪽이 너무 많아요 (최대 ${MAX_PAGES})`);
  pages.forEach((p, i) => {
    if (+p?.no !== i + 1) err(`pages[${i}].no 는 ${i + 1} 이어야 해요`);
    if (!["guide", "info", "item"].includes(p?.kind)) err(`${i + 1}쪽 kind 가 이상해요`);
    for (const [k, b] of Object.entries(p?.regions || {})) if (!isBox(b)) err(`${i + 1}쪽 영역 ${k} 좌표가 이상해요`);
    if (p?.kind === "item") for (const k of ["s1", "s2", "s3"]) if (!p.regions?.[k]) err(`${i + 1}쪽에 답안 칸 ${k} 좌표가 없어요`);
    if (p?.kind === "info" && !(p.regions?.name && p.regions?.grade)) err(`${i + 1}쪽에 이름·학년 칸 좌표가 없어요`);
  });
  if (pages[0] && pages[0].kind !== "guide") warn("1쪽이 안내(guide) 쪽이 아니에요");
  if (!pages.some((p) => p?.kind === "info")) err("응시 정보(info) 쪽이 없어요 — 비로그인 응시자를 알아볼 수 없어요");

  // 문항
  const items = Array.isArray(spec.items) ? spec.items : [];
  if (!items.length) err("items 가 없어요");
  if (items.length > MAX_ITEMS) err(`문항이 너무 많아요 (최대 ${MAX_ITEMS})`);
  const itemPages = pages.filter((p) => p?.kind === "item");
  if (items.length !== itemPages.length) err(`문항 수(${items.length})와 문제 쪽 수(${itemPages.length})가 달라요`);
  items.forEach((it, i) => {
    const tag = `${i + 1}번`;
    if (+it?.no !== i + 1) err(`${tag}: no 는 ${i + 1}`);
    const pg = pages.find((p) => +p?.no === +it?.page);
    if (!pg || pg.kind !== "item" || +pg.item !== i + 1) err(`${tag}: page 가 문제 쪽과 맞지 않아요`);
    if (!nonEmpty(it?.story) && !nonEmpty(it?.ask)) err(`${tag}: 문제 문장이 없어요`);
    if (!nonEmpty(it?.answer)) err(`${tag}: answer(정답)가 없어요 — 채점에 필요해요`);
    const rb = Array.isArray(it?.rubric) ? it.rubric : [];
    if (!rb.length || rb.length > 5) err(`${tag}: rubric 은 요소 1~5개`);
    let sum = 0;
    rb.forEach((r, k) => {
      if (!nonEmpty(r?.element)) err(`${tag}: rubric[${k}].element 없음`);
      if (!(Number.isInteger(+r?.points) && +r.points > 0 && +r.points <= 20)) err(`${tag}: rubric[${k}].points 는 1~20 정수`);
      if (!nonEmpty(r?.criterion)) warn(`${tag}: rubric[${k}].criterion 이 비어 있어 채점이 흔들릴 수 있어요`);
      sum += +r?.points || 0;
    });
    if (it?.points != null && +it.points !== sum) err(`${tag}: points(${it.points})가 rubric 합(${sum})과 달라요`);
    if (!Array.isArray(it?.solution) || !it.solution.length) warn(`${tag}: solution(모범 풀이)이 없어요`);
    if (it?.figure_svg != null) {
      if (!isStr(it.figure_svg) || !/^\s*<svg[\s>]/i.test(it.figure_svg)) err(`${tag}: figure_svg 는 <svg> 문자열`);
      else if (it.figure_svg.length > MAX_SVG_BYTES) err(`${tag}: 그림이 너무 커요`);
      else if (UNSAFE_SVG.test(it.figure_svg)) err(`${tag}: 그림에 실행 코드·외부 링크가 있어요`);
    }
    for (const k of ["conditions", "solution", "accept"]) if (it?.[k] != null && !(Array.isArray(it[k]) && it[k].every(isStr))) err(`${tag}: ${k} 는 문자열 배열`);
  });
  if (spec.phrase != null && !(Array.isArray(spec.phrase) && spec.phrase.every(isStr))) err("phrase 는 문자열 배열");

  const summary = errors.length ? null : {
    code: spec.code, title: spec.title, level: spec.level || null, grade_label: spec.grade_label || null, date: spec.date || null,
    n_items: items.length, n_pages: pages.length, max: items.reduce((s, it) => s + (it.rubric || []).reduce((a, r) => a + (+r.points || 0), 0), 0),
    reveal: spec.reveal || "after_close",
  };
  return { ok: errors.length === 0, errors, warnings, summary };
}

/** 문항 하나의 공개용 모양 — 정답·풀이·채점 기준 문장은 뺀다 */
export function publicItem(it) {
  return {
    no: +it.no, page: +it.page, topic: it.topic || "", story: it.story || "", figure_svg: it.figure_svg || null,
    conditions: Array.isArray(it.conditions) ? it.conditions : [], ask: it.ask || "",
    points: (it.rubric || []).reduce((a, r) => a + (+r.points || 0), 0),
    elements: (it.rubric || []).map((r, k) => ({ no: +r.no || k + 1, element: r.element, points: +r.points })),
  };
}

/** 학생에게 보내는 평가 — 문제·배점·쪽 좌표·필적 문장 */
export function publicView(spec) {
  return {
    code: spec.code, title: spec.title, level: spec.level || null, grade_label: spec.grade_label || null, date: spec.date || null,
    open_book: spec.open_book !== false,
    sheet: spec.sheet, pages: (spec.pages || []).map((p) => ({ no: p.no, kind: p.kind, item: p.item ?? null, regions: p.regions || {} })),
    phrase: Array.isArray(spec.phrase) ? spec.phrase : [],
    items: (spec.items || []).map(publicItem),
  };
}

/** 공개 시점이 지난 뒤 결과 화면에 붙이는 정답·모범 풀이 */
export function answerKey(spec) {
  return (spec.items || []).map((it) => ({
    no: +it.no, answer: it.answer || "", solution: Array.isArray(it.solution) ? it.solution : [],
    rubric: (it.rubric || []).map((r, k) => ({ no: +r.no || k + 1, element: r.element, points: +r.points, criterion: r.criterion || "" })),
  }));
}

/**
 * 공개 여부 — reveal 정책 × 제출 여부 × 마감 여부 × 다 채점됐는지(complete).
 * after_submit 도 모든 문제 쪽이 채점된 제출에만 바로 공개한다(빈 제출로 정답부터 보는 것을 막는다). 마감되면 제출한 사람 모두에게.
 */
export function canReveal({ reveal = "after_close", submitted = false, status = "live", closes_at = null, now = Date.now(), complete = true } = {}) {
  if (reveal === "never" || !submitted) return false;
  const closed = status === "closed" || (closes_at && Date.parse(closes_at) <= now);
  if (closed) return true;
  return reveal === "after_submit" && !!complete;
}

/** 채점 결과(문항별 marks) → 문항 점수 · 합계. 칸이 빠진 문항은 0점 */
export function aggregate(spec, gradesByItem = {}) {
  const items = (spec.items || []).map((it) => {
    const rb = it.rubric || [];
    const max = rb.reduce((a, r) => a + (+r.points || 0), 0);
    const g = gradesByItem[it.no];
    if (!g || !Array.isArray(g.marks)) return { no: +it.no, got: 0, max, graded: false };
    const got = rb.reduce((a, r, k) => {
      const m = g.marks.find((x) => +x.no === (+r.no || k + 1));
      return a + Math.min(+r.points || 0, Math.max(0, Math.round(+m?.got || 0)));
    }, 0);
    return { no: +it.no, got, max, graded: true };
  });
  return { items, total: items.reduce((a, x) => a + x.got, 0), max: items.reduce((a, x) => a + x.max, 0), graded: items.filter((x) => x.graded).length };
}

/** 2쪽 학년 손글씨 → 표준 표기 ("2", "중학교 2" → m2 / 초등 판이면 e2) */
export function normGrade(raw, level = "mid") {
  const d = String(raw ?? "").match(/\d+/)?.[0];
  if (!d) return null;
  const n = +d;
  const lv = level === "elem" ? "e" : level === "high" ? "h" : "m";
  const max = lv === "e" ? 6 : 3;
  return n >= 1 && n <= max ? `${lv}${n}` : null;
}
/** 이름 정리: 공백·기호 제거 (한글·영문·숫자만). 못 읽은 글자(⍰·?)가 섞이면 null — 글자를 빼고 붙이면 다른 이름이 된다 */
export function normName(raw) {
  if (/[⍰?？]/.test(String(raw ?? ""))) return null;
  const s = String(raw ?? "").normalize("NFC").replace(/[^0-9A-Za-z가-힣]/g, "");
  return s.length >= 1 && s.length <= 20 ? s : null;
}
/** 비로그인 응시자 명부 키 — 이름|학년 (같은 이름·학년이 둘이면 관리자 화면에서 나눈다) */
export function personKey({ name, grade }) {
  const n = normName(name), g = String(grade || "").trim();
  return n && g ? `n:${n}|${g}` : null;
}
export const gradeLabel = (g) => {
  const m = String(g || "").match(/^([emh])(\d)$/);
  if (!m) return g || "";
  return `${{ e: "초", m: "중", h: "고" }[m[1]]}${m[2]}`;
};
