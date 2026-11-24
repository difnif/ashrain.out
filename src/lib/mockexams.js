// ashrain.out — 공부하기 › 시험 보기 › 학교별 모의고사: 목록 · 시험 데이터 · 채점 · 진도 · 글자 꾸밈 · 시청각 해설 연결
//
// 데이터는 공개 버킷 mock-exams — 비공개 저장소(difnif/ashrainout_prints)의 tools/mock_build.py 가 보관함 PDF 로 만들어 올린다
// (프린트는 공개 저장소에 넣지 않는다 — 앱은 버킷에서 읽기만 한다. 시험이 늘어도 앱을 다시 배포할 일이 없다).
//   index.json      { v, updated, eds[], schools[{ id, name, short, region, level, alias[], n }],
//                     exams[{ id, school, ed, grade, year, term, no, title, sub, range, minutes, code, total, n:{mc,sa}, pts:{mc,sa}, pages, units[] }] }
//   <id>/exam.json  { …같은 머리…, docs[{ id, label, pdf, bytes, pages[{ img, w, h }] }], items[], notes[] }
//     선택형 { i, kind:"mc", no, label, pts, ans[1~5], multi, unit, av[], box:{ p, x, y, w, h }(쪽 비율), ch[{ x, y, r }](보기 ①~⑤ 자리) }
//     서답형 { i, kind:"sa", no, label:"서답형 N", pts, title, answer, rubric[[문장, 점수]], parts[], unit, av[], box }
//   docs 의 pdf · 쪽 그림(img)은 <id>/<파일> — 이름에 내용 지문이 있어 오래 캐시된다.
// 글자 꾸밈(unit · answer · rubric 문장): {AD} 선분(윗줄) · x^2 위첨자 · [[32/5]] 분수 · <<식1 | 식2>> 연립(왼쪽 묶음)
// 진도는 이 기기 · 계정별 localStorage(컨셉 문제와 같은 방식 — 서버 표 없음).

const DEFAULT_BASE = "https://ueohwmjtfmvqunjgfrhx.supabase.co/storage/v1/object/public/mock-exams";
const ENV_BASE = (() => { try { return import.meta.env && import.meta.env.VITE_MOCK_BASE; } catch { return ""; } })();
export const MOCK_BASE = String(ENV_BASE || DEFAULT_BASE).replace(/\/+$/, "");
export const mockUrl = (rel) => `${MOCK_BASE}/${rel}`;
export const fileUrl = (exam, name) => mockUrl(`${exam.id}/${name}`);

/** 판(edition) — 앱이 따로 꾸미는 셋. 다른 판도 목록에는 나온다(아이콘 📄). 융합 · 기본은 시험이 없어도 늘 보인다. */
export const EDITIONS = [
  { id: "융합", icon: "🧪", title: "융합", desc: "과학 · 사회 · 역사 · 국어 · 영어 내용과 엮은 실전 모의고사", always: true },
  { id: "기본", icon: "📘", title: "기본", desc: "같은 범위를 교과서 수준 문장으로 — 개념을 다지는 모의고사", always: true },
  { id: "기출 분석", icon: "🔍", title: "기출 분석", desc: "그 학교 기출 문제의 경향을 분석해 만든 실전 모의고사" },
];
export const edInfo = (ed) => EDITIONS.find((e) => e.id === ed) || { id: ed, icon: "📄", title: ed, desc: "" };

// ── 불러오기 ──────────────────────────────────────────────────────────────────
let indexWait = null;
const examWait = new Map();
async function getJson(url) {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw Object.assign(new Error(r.status === 400 || r.status === 404 ? "NOINDEX" : `불러오지 못했어요 (${r.status})`), { status: r.status });
  return r.json();
}
/** 목록 — 아직 올라간 시험이 없으면(버킷 · 파일 없음) { schools: [], exams: [], empty: true } */
export function loadMockIndex(force = false) {
  if (force || !indexWait) {
    indexWait = getJson(mockUrl("index.json"))
      .then((j) => ({ v: j.v || 1, updated: j.updated || "", schools: j.schools || [], exams: j.exams || [], empty: false }))
      .catch((e) => { indexWait = null; if (e.message === "NOINDEX") return { schools: [], exams: [], empty: true }; throw e; });
  }
  return indexWait;
}
export function loadMockExam(id) {
  if (!/^[a-z0-9][a-z0-9-]{2,60}$/.test(String(id || ""))) return Promise.reject(new Error("없는 시험이에요"));
  if (!examWait.has(id)) {
    examWait.set(id, getJson(mockUrl(`${id}/exam.json`)).catch((e) => {
      examWait.delete(id);
      throw e.message === "NOINDEX" ? new Error("없는 시험이에요 — 목록에서 다시 골라 주세요") : e;
    }));
  }
  return examWait.get(id);
}

// ── 학교 · 판 · 회차 ──────────────────────────────────────────────────────────
const CHO = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"];
const squash = (s) => String(s || "").toLowerCase().replace(/[\s·.,\-()]/g, "");
const choOf = (s) => [...String(s || "")].map((ch) => { const c = ch.codePointAt(0); return c >= 0xac00 && c <= 0xd7a3 ? CHO[Math.floor((c - 0xac00) / 588)] : /\s/.test(ch) ? "" : ch.toLowerCase(); }).join("");
const isCho = (q) => q.length > 0 && [...q].every((ch) => CHO.includes(ch));
/** 학교 검색 — 이름 · 줄임 · 지역 · 다른 이름(공백 무시 부분 일치, 초성만 쓰면 초성으로). 「중학교」 · 「중」을 떼고 써도 찾는다. 이름이 앞에서 맞는 학교부터. */
export function searchSchools(schools, query) {
  const q = squash(query);
  const list = schools || [];
  if (!q) return list.slice();
  const texts = (s) => [s.name, s.short, s.region, ...(s.alias || [])];
  const hit = list.filter((s) => {
    const t = texts(s);
    if (t.some((x) => squash(x).includes(q))) return true;
    return isCho(q) && t.some((x) => choOf(x).includes(q));
  });
  const head = (s) => (squash(s.name).startsWith(q) || squash(s.short).startsWith(q) || (isCho(q) && choOf(s.name).startsWith(q)) ? 0 : 1);
  return hit.sort((a, b) => head(a) - head(b) || (b.n || 0) - (a.n || 0) || String(a.name).localeCompare(String(b.name), "ko"));
}
/** 그 학교의 판들 — [{ ...edInfo, n }] (융합 · 기본은 늘, 나머지는 시험이 있을 때만) */
export function editionsOf(index, schoolId) {
  const ex = (index?.exams || []).filter((e) => e.school === schoolId);
  const known = EDITIONS.map((e) => ({ ...e, n: ex.filter((x) => x.ed === e.id).length })).filter((e) => e.always || e.n > 0);
  const extra = [...new Set(ex.map((x) => x.ed))].filter((ed) => !EDITIONS.some((e) => e.id === ed)).map((ed) => ({ ...edInfo(ed), n: ex.filter((x) => x.ed === ed).length }));
  return [...known, ...extra];
}
/** 그 학교 · 판의 회차 — 시기(학년도 · 학년 · 시기)로 묶어 최근 시기부터, 묶음 안은 회차 차례 */
export function examGroups(index, schoolId, ed) {
  const ex = (index?.exams || []).filter((e) => e.school === schoolId && (!ed || e.ed === ed));
  const groups = new Map();
  for (const e of ex) {
    const k = `${e.year}|${e.grade}|${e.term}`;
    if (!groups.has(k)) groups.set(k, { key: k, year: e.year, grade: e.grade, term: e.term, title: `${e.year}학년도 ${e.grade} ${e.term}`, exams: [] });
    groups.get(k).exams.push(e);
  }
  const out = [...groups.values()];
  for (const g of out) g.exams.sort((a, b) => a.no - b.no);
  const termRank = (t) => (/기말/.test(t) ? 1 : 0) + (/2학기/.test(t) ? 2 : 0);
  return out.sort((a, b) => b.year - a.year || String(b.grade).localeCompare(String(a.grade)) || termRank(b.term) - termRank(a.term));
}

// ── 문항 · 채점 ───────────────────────────────────────────────────────────────
export const CIRCLED = ["", "①", "②", "③", "④", "⑤"];
export const choiceText = (arr) => (arr || []).map((c) => CIRCLED[c] || c).join(", ");
export const mcItems = (exam) => (exam?.items || []).filter((it) => it.kind === "mc");
export const saItems = (exam) => (exam?.items || []).filter((it) => it.kind === "sa");
export const itemByI = (exam, i) => (exam?.items || []).find((it) => it.i === Number(i)) || null;

/** 선택형 답 고르기 — 한 개 답은 바꿔 고르고(다시 누르면 지움), 여러 개 답(정답 2개)은 켜고 끈다 */
export function toggleChoice(prev, c, multi) {
  const sel = prev?.k === "mc" ? prev.sel || [] : [];
  let next;
  if (multi) next = sel.includes(c) ? sel.filter((x) => x !== c) : [...sel, c].sort((a, b) => a - b);
  else next = sel.length === 1 && sel[0] === c ? [] : [c];
  return next.length ? { k: "mc", sel: next } : null;
}
const sameSet = (a, b) => a.length === b.length && [...a].sort().every((x, i) => x === [...b].sort()[i]);
export function isAnswered(it, ans) {
  if (!ans) return false;
  if (it.kind === "mc") return ans.k === "mc" && (ans.sel || []).length > 0;
  return ans.k === "sa" && Object.values(ans.parts || {}).some((p) => (p?.k === "text" && String(p.raw || "").trim()) || (p?.k === "ink" && Array.isArray(p.s) && p.s.length));
}
/** 선택형 하나 판정 → "ok" | "wrong" | "blank" */
export function judgeMc(it, ans) {
  const sel = ans?.k === "mc" ? ans.sel || [] : [];
  if (!sel.length) return "blank";
  return sameSet(sel, it.ans || []) ? "ok" : "wrong";
}
/**
 * 채점 — 선택형은 바로, 서답형은 스스로 채점한 점수(sa: { i: { got, checks[] } }).
 * → { rows[{ i, kind, label, pts, got, status }], mc:{ got, max, ok, n }, sa:{ got, max, done, n }, score, max, counts:{ ok, wrong, blank, pending } }
 *   서답형 status: "ok"(만점) · "part"(부분) · "wrong"(0점) · "blank"(답 안 씀) · "pending"(아직 스스로 채점 안 함)
 */
export function gradeMock(exam, answers = {}, sa = {}) {
  const rows = [];
  const mc = { got: 0, max: 0, ok: 0, n: 0 }, s = { got: 0, max: 0, done: 0, n: 0 };
  const counts = { ok: 0, wrong: 0, blank: 0, pending: 0, part: 0 };
  for (const it of exam?.items || []) {
    if (it.kind === "mc") {
      const st = judgeMc(it, answers[it.i]);
      const got = st === "ok" ? it.pts : 0;
      mc.max += it.pts; mc.n++; mc.got += got; if (st === "ok") mc.ok++;
      counts[st]++;
      rows.push({ i: it.i, kind: "mc", label: it.label, pts: it.pts, got, status: st });
    } else {
      s.max += it.pts; s.n++;
      const g = sa[it.i];
      const answered = isAnswered(it, answers[it.i]);
      let st, got = 0;
      if (g && Number.isFinite(g.got)) {
        got = Math.max(0, Math.min(it.pts, g.got)); s.done++;
        st = got >= it.pts ? "ok" : got > 0 ? "part" : answered ? "wrong" : "blank";
      } else st = answered ? "pending" : "blank";
      s.got += got;
      counts[st] = (counts[st] || 0) + 1;
      rows.push({ i: it.i, kind: "sa", label: it.label, pts: it.pts, got, status: st });
    }
  }
  return { rows, mc, sa: s, score: mc.got + s.got, max: mc.max + s.max, counts };
}
/** 서답형 채점 요소 체크 → 점수(체크한 요소의 점수 합) */
export const rubricScore = (it, checks = []) => (it.rubric || []).reduce((n, r, k) => n + (checks[k] ? r[1] : 0), 0);
/** 채점 요소가 어느 하위 문항((1) · (2))의 것인지 — 없으면 0 */
export const rubricPart = (text) => Number((String(text || "").match(/^\((\d)\)/) || [])[1] || 0);

// ── 시청각 해설 연결 ──────────────────────────────────────────────────────────
/** 시청각 해설 key → 주소(돌아올 곳을 붙여서) */
export const avHref = (key, from) => `#/av/${encodeURIComponent(key)}${from ? `?from=${encodeURIComponent(from)}` : ""}`;
/** 시험 전체의 시청각 해설 — key 마다 걸린 문항들(처음 나온 차례) [{ key, items[{ i, label }] }] */
export function avLinksOf(exam, known = () => true) {
  const m = new Map();
  for (const it of exam?.items || []) {
    for (const k of it.av || []) {
      if (!known(k)) continue;
      if (!m.has(k)) m.set(k, { key: k, items: [] });
      m.get(k).items.push({ i: it.i, label: it.label });
    }
  }
  return [...m.values()];
}
/** 돌아올 곳으로 받아도 되는 주소인가(시험 화면 안쪽만) */
export const safeFrom = (h) => (/^#\/(mock\/[a-z0-9-]+(\/[a-z0-9/?=&.-]*)?|study\/exam(\/[^\s]*)?)$/i.test(String(h || "")) ? String(h) : "");

// ── 글자 꾸밈 → HTML (먼저 이스케이프) ─────────────────────────────────────────
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function inline(t) {
  return t
    .replace(/\[\[([^\]/]+)\/([^\]]+)\]\]/g, '<span class="mx-fr"><span class="n">$1</span><span class="d">$2</span></span>')
    .replace(/\{([A-Z]{1,3}[′']?)\}/g, '<span class="mx-ov">$1</span>')
    .replace(/\^\{([^}]{1,6})\}/g, "<sup>$1</sup>")
    .replace(/\^([0-9a-z])/g, "<sup>$1</sup>");
}
/** 등록 정보의 글자(단원 · 답 · 채점 요소) → HTML */
export function richHtml(s) {
  let t = esc(s);
  t = t.replace(/&lt;&lt;(.+?)&gt;&gt;/g, (_, body) => `<span class="mx-sys">${body.split(/\s*\|\s*/).map((x) => `<span>${inline(x)}</span>`).join("")}</span>`);
  return inline(t);
}

// ── 진도 (이 기기 · 계정별) ───────────────────────────────────────────────────
let USER = "";
export function setMockUser(uid) { USER = uid ? String(uid) : ""; }
const PK = (id) => `ash.mock.${USER ? USER.slice(0, 8) + "." : ""}${id}`;
const lsGet = (k) => { try { return localStorage.getItem(k); } catch { return null; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); return true; } catch { return false; } };
const lsDel = (k) => { try { localStorage.removeItem(k); } catch { /* 무시 */ } };

/**
 * 시험지 풀이 — { answers:{ i: {k:"mc", sel[]} | {k:"sa", parts:{ n: ink|text }} }, sa:{ i: { got, checks[] } },
 *   submitted: null | { at, score, max }, timer: null | { start(ms), paused(ms|null), used(ms) } }
 */
export function readMockPaper(id) {
  try {
    const v = JSON.parse(lsGet(PK(id)) || "null");
    if (v && typeof v === "object") return { answers: v.answers || {}, sa: v.sa || {}, submitted: v.submitted || null, timer: v.timer || null };
  } catch { /* 무시 */ }
  return { answers: {}, sa: {}, submitted: null, timer: null };
}
export function saveMockPaper(id, st) {
  return lsSet(PK(id), JSON.stringify({ answers: st.answers || {}, sa: st.sa || {}, submitted: st.submitted || null, timer: st.timer || null }));
}
export function clearMockPaper(id) { lsDel(PK(id)); }

/** 한 문제씩 기록 { items:{ i:{ sel?, ok, at, n } }, results:[{ at, score, max, kind }] } */
const RK = (id) => `${PK(id)}.rec`;
export function readMockRecord(id) {
  try {
    const v = JSON.parse(lsGet(RK(id)) || "null");
    if (v && typeof v === "object") return { items: v.items || {}, results: Array.isArray(v.results) ? v.results : [] };
  } catch { /* 무시 */ }
  return { items: {}, results: [] };
}
export function saveMockAttempt(id, i, rec, { count = true } = {}) {
  const r = readMockRecord(id);
  const prev = r.items[i];
  r.items[i] = { ...rec, at: new Date().toISOString(), n: (prev?.n || 0) + (count || !prev ? 1 : 0), everOk: !!(prev?.everOk || rec.ok) };
  lsSet(RK(id), JSON.stringify(r));
  return r;
}
/** 채점 결과 — 최근 10개. 같은 sid(제출 시각)는 고쳐 쓴다(서답형을 나중에 스스로 채점하면 점수가 바뀜) */
export function saveMockResult(id, res) {
  const r = readMockRecord(id);
  const row = { ...res, at: res.at || new Date().toISOString() };
  const k = res.sid ? r.results.findIndex((x) => x.sid === res.sid) : -1;
  if (k >= 0) r.results[k] = row; else r.results = [row, ...r.results].slice(0, 10);
  lsSet(RK(id), JSON.stringify(r));
  return r;
}

/** 시험지 위 보기 누르는 자리 — 보기 번호 가운데에서 같은 줄 다음 보기 앞까지(없으면 칸 끝까지). 쪽 비율 { x, y, w, h }[] */
export function choiceRects(it) {
  const ch = it?.ch || [];
  const b = it?.box || { x: 0, w: 1 };
  return ch.map((c) => {
    const row = ch.filter((d) => d !== c && Math.abs(d.y - c.y) < c.r * 0.9 && d.x > c.x);
    const next = row.length ? Math.min(...row.map((d) => d.x)) : null;
    const gaps = ch.map((d) => Math.abs(d.y - c.y)).filter((dy) => dy >= c.r * 0.9);      // 다른 줄까지 — 위아래 자리가 겹치지 않게
    const half = Math.min(Math.max(c.r * 1.5, 0.0105), gaps.length ? Math.min(...gaps) / 2 - 0.0004 : 1);
    const x0 = Math.max(b.x, c.x - c.r * 1.8);
    const x1 = next != null ? next - d1(c.r) : b.x + b.w - 0.006;
    return { x: x0, y: c.y - half, w: Math.max(c.r * 3.2, x1 - x0), h: half * 2 };
  });
}
const d1 = (r) => r * 1.9;

/** 타이머 — 남은 ms(음수면 넘김). timer: { start, paused, used } */
export function timerLeft(timer, minutes, now = Date.now()) {
  if (!timer) return minutes * 60000;
  const run = timer.paused != null ? timer.paused - timer.start : now - timer.start;
  return minutes * 60000 - (timer.used || 0) - run;
}
export const fmtClock = (ms) => {
  const neg = ms < 0, t = Math.round(Math.abs(ms) / 1000);
  return `${neg ? "+" : ""}${Math.floor(t / 60)}:${String(t % 60).padStart(2, "0")}`;
};

/** 최근 본 학교(이 기기) */
const RS = "ash.mock.recentSchools";
export function readRecentSchools() { try { const v = JSON.parse(lsGet(RS) || "[]"); return Array.isArray(v) ? v.filter((x) => typeof x === "string") : []; } catch { return []; } }
export function pushRecentSchool(id) { const v = [id, ...readRecentSchools().filter((x) => x !== id)].slice(0, 6); lsSet(RS, JSON.stringify(v)); return v; }

export const fmtBytes = (n) => (!(n > 0) ? "" : n >= 1e6 ? `${(n / 1e6).toFixed(1)}MB` : `${Math.max(1, Math.round(n / 1e3))}KB`);
/** 받을 때 파일 이름 — 「문정중 2026 중2 2학기 중간고사 대비 실전 모의고사 1회 (기출 분석) 문제지.pdf」 */
export function downloadName(exam, doc, schoolShort = "") {
  const base = [schoolShort, `${exam.year}`, exam.grade, exam.term, exam.title, exam.ed ? `(${exam.ed})` : "", doc.label]
    .filter(Boolean).join(" ").replace(/[\\/:*?"<>|]+/g, " ").replace(/\s+/g, " ").trim();
  return `${base}.pdf`;
}
