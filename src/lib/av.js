// ashrain.out — 공부하기 › 시청각 학습 목록 (교실 모니터 콘텐츠를 학생앱에)
// 교실 모니터(#/admin/display)의 수업 장면 · 액자를 학생이 직접 연다 — 같은 무대(AdminDisplay 의 Stage)를 av 모드로.
//   · 수학 호기심 — 수업 장면(도형 · 경우의 수 애니메이션), 하노이의 탑, 실험 액자(몬티홀 · 갈림길 · 갈톤 보드), 장면 묶음(축구 · 서술형 이야기),
//                  그림 액자 열여섯(축구 · 농구 · 야구 직선, 배드민턴 · 테니스 · 탁구 · 배구 · 족구 · 세팍타크로 · 골프 · 당구 · 볼링,
//                  주머니 공 꺼내기, 알파벳 카드, 일렬로 세우기, 학년별 뽑기 — frames/curio.jsx)
//   · 문제 풀이 해설 — 기본기 해설 단원(초등 · 중등 · 고등, frames/basics.jsx — 단원마다 한 항목, 학년을 넘나듦)
//                  + 해설 액자(일차함수 그래프 그리기 · 10단계 계산 · 그래프와 넓이 · 경우의 수와 확률 100제 — 중등, after 단원 뒤에).
//                  학교급(level)으로 나눠 보인다(AV_LEVELS — 학생앱 상단 버튼). 학년 꼬리표 대신 학년 범위(grade = span).
//   · unit — 콘텐츠의 주요 단원(lib/units.js). 꾹 누르면 우물이 떠서 앞 · 같은 · 다음 단원 콘텐츠를 추천한다(components/WellPick.jsx).
// 여는 주소: #/av/<key> — key 는 액자 key(frames/index.js) · 기본기 단원 id(basics/index.js) · 유형 「<단원>.<단계>」(lib/avtypes.js)
//   · 회차 「w-<학년>-<주><A|B>」(weeks/index.js) · scenes-<묶음>(pairs.js 의 GROUPS).
// 교실 모니터에 액자가 새로 들어오면: frames/index.js 의 lesson 표시를 따라 저절로 갈린다(lesson → 문제 풀이 해설, 나머지 → 수학 호기심).
import { FRAMES } from "../features/display/frames/index.js";
import { BASICS, LEVELS } from "../features/display/basics/index.js";
import { relatedOf } from "./units.js";
import { parseWeekId, gradeOf, frameOfGrade, weekMetaCached, KIND_ICON, WGRADES } from "../features/display/weeks/index.js";
import { parseTypeKey, typeMeta, typesOf } from "./avtypes.js";

export const AV_CATS = [
  { id: "fun", title: "수학 호기심", icon: "🔭", sub: "도형이 움직이고, 구슬이 떨어지고, 문이 열려요 — 보고 직접 해 보는 수학" },
  { id: "sol", title: "문제 풀이 해설", icon: "🎬", sub: "단원마다 100문항을 한 문항씩 — 문제 → 방침 → 한 줄씩 → 답" },
];
export const AV_LEVELS = ["초등", "중등", "고등"];

// 수업 장면(초등 ↔ 중등 짝 애니메이션) — 묶음별로 하나씩
const SCENES = [
  { key: "scenes-geo", grp: "geo", icon: "🔷", title: "도형 애니메이션", desc: "도형이 접히고 펼쳐지고 돌아가요. 오른쪽 위 「초등 | 중등」을 누르면 같은 장면이 짝 장면으로 겹쳐 넘어가요." },
  { key: "scenes-data", grp: "data", icon: "🎲", title: "경우의 수 · 확률 애니메이션", desc: "줄 세우기 · 뽑기 · 확률을 움직이는 그림으로. 「초등 | 중등」으로 같은 장면을 두 학년 눈높이로 봐요." },
];
const ICON = { hanoi: "🗼", monty: "🚪", branch: "🔀", galton: "⚪", soccer: "⚽", essay: "📖", graph: "📈", lin10: "🔢", area: "📐", cnt100: "🎯",
  soccerfn: "🥅", hoopfn: "🏀", batfn: "⚾", badminton: "🏸", tennis: "🎾", tabletennis: "🏓", volleyball: "🏐", jokgu: "🦶", sepak: "🦵",
  golf: "⛳", cue: "🎱", bowl: "🎳", pouch: "👝", lexi: "🔤", lineup: "🧍", crowd: "🔍" };
const LEVEL_FRAME = Object.fromEntries(LEVELS.map((L) => [L.level, L.frame]));

/** 기본기 단원 하나 = 학생앱 한 항목 (같은 학교급 액자를 그 단원으로 연다) */
const basicItem = (b) => ({
  key: b.id, frame: LEVEL_FRAME[b.level], set: b.id, grp: null, cat: "sol", icon: b.icon, kind: "해설",
  title: b.title, short: b.short, desc: b.desc, grade: b.span, level: b.level, unit: b.unit,
});
const frameItem = (f) => ({
  key: f.key, frame: f.key, grp: null, cat: f.lesson ? "sol" : "fun", icon: ICON[f.key] || "🖼",
  kind: f.lesson ? "해설" : f.lab ? "실험" : f.story ? "이야기" : "그림", title: f.title, desc: f.desc,
  grade: f.grade || null, level: f.level || null, unit: f.unit || null,
});

// 문제 풀이 해설 — 기본기 단원 차례대로, 해설 액자는 after 단원 바로 뒤에(학교급 액자 셋 자체는 항목이 아니다)
const SOL = BASICS.map(basicItem);
for (const f of FRAMES.filter((x) => x.lesson && !x.basics)) {
  const it = frameItem(f);
  let i = SOL.findIndex((x) => x.key === f.after);
  if (i < 0) { SOL.push(it); continue; }
  while (SOL[i + 1] && SOL[i + 1].frame === SOL[i + 1].key && SOL[i + 1].level === it.level) i++;    // 같은 단원 뒤에 이미 붙은 액자 다음
  SOL.splice(i + 1, 0, it);
}

export const AV_ITEMS = [
  ...SCENES.map((s) => ({ ...s, cat: "fun", kind: "애니메이션", frame: null })),
  ...FRAMES.filter((f) => !f.lesson).map(frameItem),
  ...SOL,
];
// 예전 주소(학년별 해설 #/av/e1 … h3 — PR #62) → 그 학년 첫 단원
const OLD = { e1: "e-ten", e2: "e-col", e3: "e-area3", e4: "e-frac4", e5: "e-red", e6: "e-fdiv", m1: "m-int", m2: "m-exp", m3: "m-fact", h1: "h-rem", h2: "h-explog", h3: "h-count" };

/** 주차별 기초 다지기 회차(#/av/w-e3-07a) — 머리 정보가 아직 없으면 id 로 만든다(제목은 액자가 읽은 뒤 채운다) */
export function weekItem(id) {
  const p = parseWeekId(id);
  if (!p) return null;
  const g = gradeOf(p.gk), m = weekMetaCached(id);
  return {
    key: id, frame: frameOfGrade(p.gk), set: id, grp: null, cat: "sol", icon: m ? KIND_ICON[m.kind] || "🗓" : "🗓", kind: "해설",
    title: m ? m.title : `${g.grade} ${p.week}주 ${p.slot}`, short: m ? m.title : `${p.week}주 ${p.slot}`, desc: m ? m.desc : "",
    grade: g.grade, level: g.level, unit: m ? m.unit : null, week: p.week, slot: p.slot,
  };
}
/** 단원 100제의 유형 하나(#/av/e-ten.3) — 그 단원 액자를 그 단계만(20문항) */
export function typeItem(key) {
  const p = parseTypeKey(key);
  if (!p) return null;
  const m = typeMeta(key);
  return {
    key, frame: LEVEL_FRAME[m.level], set: key, grp: null, cat: "sol", icon: m.icon, kind: "유형",
    title: m.title, short: m.short, desc: `${m.short} — ${m.name} 20문항`, grade: m.span, level: m.level, unit: m.unit, base: p.id, st: p.st,
  };
}
export const avItem = (key) => weekItem(key) || typeItem(key) || AV_ITEMS.find((x) => x.key === key) || AV_ITEMS.find((x) => x.key === OLD[key]) || null;

/* ══════════ 우물 추천용 카드(lib/recommend.js 의 pool) ══════════ */
const GIDX = Object.fromEntries(WGRADES.map((g, i) => [g.grade, i]));
/** 회차 머리 정보 → 카드 */
export const weekCard = (m) => ({
  key: m.id, unit: m.unit, gidx: GIDX[m.grade], week: m.week, kind: m.kind, seq: m.seq || 0, level: m.level,
  title: m.title, short: m.title, icon: KIND_ICON[m.kind] || "🗓", grade: `${m.grade} ${m.week}주${m.slot}`,
});
/** 단원 100제 · 해설 액자 → 카드(학년 범위의 첫 학년 · 주는 없음) */
export const unitCard = (it) => ({ ...it, gidx: GIDX[String(it.grade || "").split("~")[0]] ?? null, week: 60, kind: "단원" });
/** 유형 → 카드(교과서 단원의 학년 · 단원 100제 뒤) — base 는 유형이 든 단원(우물 추천이 서로 품은 것끼리는 고르지 않게) */
export const typeCard = (m) => ({
  key: m.id, base: m.base, unit: m.unit, gidx: GIDX[m.span] ?? null, week: 60 + m.st, kind: "유형", seq: m.st, level: m.level,
  title: m.title, short: m.short, icon: m.icon, grade: `${m.span} · ${m.st}단계`,
});
/** 단원 100제의 유형 전부(학교급) — 목록 · 우물 추천 */
export const typesOfLevel = (lv) => SOL.filter((x) => x.level === lv && x.frame === LEVEL_FRAME[lv]).flatMap((x) => typesOf(x.key));
export const avOfCat = (cat) => AV_ITEMS.filter((x) => x.cat === cat);
export const avOfLevel = (lv) => SOL.filter((x) => x.level === lv);
/** 꾹 눌렀을 때 우물에 띄울 추천 — 앞 단원 · 같은 단원 · 다음 단원 콘텐츠(학교급을 넘어서도) */
export const avRelated = (item, max = 6) => relatedOf(item, SOL, max);
