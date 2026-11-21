// ashrain.out — 주차별 기초 다지기 (기본기 해설 회차) 머리 정보 · 불러오기 · 학사 달력 (순수 도우미 + fetch)
// 학년마다 52주 × 주 2회(A · B) = 104회차, 회차마다 20문항(5단계 × 4문항). 초등 624 · 중등 312 · 고등 312.
// 자료는 public/av-weeks/<학년>/index.json(회차 머리 정보 104개)과 <회차 id>.json(문항) — 생성기 avgen/weeks.py 가 만든다(손으로 고치지 말 것).
// 회차 id: w-<학년>-<주 두 자리><a|b> (예: w-e3-07a = 초3 7주 A). 학생앱 #/av/<회차 id> · 교실 모니터 기본기 액자(frames/basics.jsx)가 같이 쓴다.
// 학사 달력: 1주 = 3월 2일이 든 주(월요일 시작). 1 ~ 20주 1학기 · 21 ~ 25주 여름방학 · 26 ~ 45주 2학기 · 46 ~ 52주 겨울방학.

export const WGRADES = [
  { gk: "e1", grade: "초1", level: "초등" }, { gk: "e2", grade: "초2", level: "초등" }, { gk: "e3", grade: "초3", level: "초등" },
  { gk: "e4", grade: "초4", level: "초등" }, { gk: "e5", grade: "초5", level: "초등" }, { gk: "e6", grade: "초6", level: "초등" },
  { gk: "m1", grade: "중1", level: "중등" }, { gk: "m2", grade: "중2", level: "중등" }, { gk: "m3", grade: "중3", level: "중등" },
  { gk: "h1", grade: "고1", level: "고등" }, { gk: "h2", grade: "고2", level: "고등" }, { gk: "h3", grade: "고3", level: "고등" },
];
export const WEEKS = 52, PER_WEEK = 2, PER_GRADE = WEEKS * PER_WEEK;
export const PERIODS = [
  { key: "1학기", from: 1, to: 20 },
  { key: "여름방학", from: 21, to: 25 },
  { key: "2학기", from: 26, to: 45 },
  { key: "겨울방학", from: 46, to: 52 },
];
export const KIND_ICON = { 개념: "📘", 연습: "✏️", 응용: "🧩", 마무리: "🏁", 복습: "🔁", 예습: "🔭" };

const ID_RE = /^w-(e[1-6]|m[1-3]|h[1-3])-(\d\d)([ab])$/;
/** 회차 id 인가 — 맞으면 { gk, week, slot } */
export function parseWeekId(id) {
  const m = ID_RE.exec(String(id || ""));
  if (!m) return null;
  const week = Number(m[2]);
  if (week < 1 || week > WEEKS) return null;
  return { gk: m[1], week, slot: m[3].toUpperCase() };
}
export const weekId = (gk, week, slot) => `w-${gk}-${String(week).padStart(2, "0")}${String(slot).toLowerCase()}`;
export const gradeOf = (gk) => WGRADES.find((g) => g.gk === gk || g.grade === gk) || null;
export const gradesOfLevel = (lv) => WGRADES.filter((g) => g.level === lv);
export const frameOfGrade = (gk) => `basic-${String(gk)[0]}`;
export const periodOf = (week) => PERIODS.find((p) => week >= p.from && week <= p.to)?.key || "1학기";

/* ══════════ 학사 달력 ══════════ */
const DAY = 86400000;
/** 그 해 1주의 월요일(3월 2일이 든 주) — 현지 시각 자정 */
export function yearStart(y) {
  const d = new Date(y, 2, 2);
  const dow = (d.getDay() + 6) % 7;            // 월 0 … 일 6
  return new Date(y, 2, 2 - dow);
}
/** 날짜 → { year: 학년도, week: 1 ~ 52 } */
export function weekOfDate(date = new Date()) {
  const d = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  let y = d.getFullYear();
  if (d < yearStart(y)) y -= 1;
  const w = Math.floor((d - yearStart(y)) / DAY / 7) + 1;
  return { year: y, week: Math.max(1, Math.min(WEEKS, w)) };
}
/** 학년도 · 주 → 그 주 월요일 */
export const mondayOf = (year, week) => new Date(yearStart(year).getTime() + (week - 1) * 7 * DAY);
/** "5월 3주" — 그 주 수요일이 든 달의 몇째 주 */
export function weekLabel(year, week) {
  const wed = new Date(mondayOf(year, week).getTime() + 2 * DAY);
  return `${wed.getMonth() + 1}월 ${Math.ceil(wed.getDate() / 7)}주`;
}

/* ══════════ 불러오기 ══════════ */
const idxDone = new Map(), idxWait = new Map(), setDone = new Map(), setWait = new Map();
const getJson = (url) => fetch(url, { cache: "no-cache" }).then((r) => { if (!r.ok) throw new Error(`${r.status}`); return r.json(); });
/** 학년 머리 정보 { gk, grade, level, n, gaps, sessions:[…104] } */
export function loadWeekIndex(gk) {
  if (!gradeOf(gk)) return Promise.reject(new Error(`없는 학년: ${gk}`));
  if (!idxWait.has(gk)) {
    idxWait.set(gk, getJson(`/av-weeks/${gk}/index.json`).then((h) => { idxDone.set(gk, h); return h; })
      .catch((e) => { idxWait.delete(gk); throw e; }));
  }
  return idxWait.get(gk);
}
export const weekIndexCached = (gk) => idxDone.get(gk) || null;
/** 회차 머리 정보(학년 머리 정보가 이미 읽혔을 때) */
export function weekMetaCached(id) {
  const p = parseWeekId(id);
  const h = p && idxDone.get(p.gk);
  return (h && h.sessions.find((s) => s.id === id)) || null;
}
export async function loadWeekMeta(id) {
  const p = parseWeekId(id);
  if (!p) throw new Error(`없는 회차: ${id}`);
  const h = await loadWeekIndex(p.gk);
  const m = h.sessions.find((s) => s.id === id);
  if (!m) throw new Error(`없는 회차: ${id}`);
  return m;
}
/** 회차 문항 { id, pp, note, tips, items:[…20] } */
export function loadWeek(id) {
  const p = parseWeekId(id);
  if (!p) return Promise.reject(new Error(`없는 회차: ${id}`));
  if (!setWait.has(id)) {
    setWait.set(id, getJson(`/av-weeks/${p.gk}/${id}.json`).then((s) => { setDone.set(id, s); return s; })
      .catch((e) => { setWait.delete(id); throw e; }));
  }
  return setWait.get(id);
}
export const weekCached = (id) => setDone.get(id) || null;
