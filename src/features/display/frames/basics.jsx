// ashrain.out — 교실 모니터 「액자」 · 학생앱 시청각 학습 › 문제 풀이 해설: 기본기 해설 (frames/basics.jsx)
// 초등 · 중등 · 고등 학교급마다 한 액자 — 단원(100문항, 1 ~ 5단계)이나 주차별 회차(20문항)를 골라 문항마다 한 장면으로 끝없이 돌린다.
// 단원은 학년에 묶지 않고 학년을 넘나든다(span — 초3~초5 처럼). 학생앱에서는 단원 · 유형 · 회차마다 한 항목(#/av/<단원 id> · #/av/e-ten.3 ·
// #/av/w-e3-07a)이라 그것으로 바로 열리고(pick), 액자 안 「단원」 · 「유형」 · 「회차」(U) 목록으로 옮길 수 있다 —
// 목록 머리에서 「단원 100제 | 유형 | 주차별 학년」을 바꾼다.
//   유형 = 단원의 한 단계 20문항(lib/avtypes.js) — 번호 1 ~ 20 · 유형마다 따로 프린트(유형 코드). 단원 100제를 보면 그 문항의 유형에도 본 기록.
//   주차별 기초 다지기: 학년마다 주 2회 × 52주 = 104회차(../weeks — public/av-weeks/<학년>/), 목록은 학기 · 방학으로 나누고 이번 주를 표시.
//   ① 문제 → ② 방침 → ③ 판서(한 줄씩, 빨간 메모) → ④ 답 · 오른쪽 그림은 판서 줄에 맞춰 자란다(그림 DSL — frames/figdsl.jsx).
// 그리기 · 박자는 일차함수 10단계 액자와 같다(frames/lin10.jsx 의 L10Art · ../lin10.js 의 l10Plan).
// 조작은 해설 액자 공통 틀(frames/lesson.jsx) — 「보기 단일 | 듀얼」(D) · 「단원」 · 「회차」 목록(U · B 다음) · 빠르기 0.75× ~ 2×(S) ·
//   번호 · 단계 목록(L — 단계 칩을 고르면 그 단계만) · 두 막대(아래 긴 막대 = 문항 이동, 옆 짧은 막대 = 풀이 이동) · 듀얼 가운데 ⇄(X).
//   듀얼 판마다 문제 풀이 해설 전부(단원 100제 · 유형 · 주차별 회차 · 해설 액자 — frames/allspec.jsx)에서 따로 고른다(같은 것 둘도 됨).
//   오른쪽 위 📄 문서(문제지 · 해설지 · 빠른 정답 · OMR — frames/docsmenu.jsx) — 듀얼에서 두 판이 다르면 하나씩. 문항은 고를 때 들여온다(spec.load).
// 학생앱에서 열면(pick) 본 기록을 기기에 남긴다(lib/avHistory.js — 우물 추천 · 목록의 ✓ · 진행 막대).
// 문항 자료는 단원마다 따로 늦게 들여온다(../basics/<단원>.js) — 머리 정보는 ../basics/index.js, 목록 그림용 한 문항은 ../basics/thumbs.js.
import { memo, useCallback, useEffect, useRef, useState } from "react";
import { l10Plan } from "../lin10.js";
import { PANE_REGION } from "../board.js";
import { L10Art } from "./lin10.jsx";
import { LessonFrame, LESSON_SPEEDS, Loading } from "./lesson.jsx";
import { LEVELS, levelOf, basicsOf, basicOf, loadBasic, basicCached } from "../basics/index.js";
import { THUMBS } from "../basics/thumbs.js";
import { parseWeekId, weekId, gradeOf, gradesOfLevel, loadWeekIndex, weekIndexCached, weekMetaCached, loadWeek, weekCached,
  PERIODS, KIND_ICON, weekOfDate, weekLabel } from "../weeks/index.js";
import { DocsMenu } from "./docsmenu.jsx";
import { stepMarks } from "./scrub.jsx";
import { lsRead, lsWrite } from "./xkit.jsx";
import { unitLabel } from "../../../lib/units.js";
import { noteOpen, noteSeen } from "../../../lib/avHistory.js";
import { parseTypeKey, typeKey, typeMeta, typeCached, loadType, typesOf } from "../../../lib/avtypes.js";

export const B_SPEEDS = LESSON_SPEEDS;

/* ══════════ 장면 목록 (StoryPlayer 형식) — 단원 · 회차 같음 ══════════ */
const SCENES = new Map();
export function basicScenes(meta, set, sp = 1, stage = 0) {
  const k = `${meta.id}|${sp}|${stage}`;
  if (SCENES.has(k)) return SCENES.get(k);
  const wk = parseWeekId(meta.id), uid = `b${String(meta.id).replace(/[^\w-]/g, "_")}`;
  const list = set.items.filter((it) => !stage || it.st === stage).map((it) => {
    const title = wk ? `${meta.grade} ${meta.week}주 ${meta.slot} · ${meta.title}` : meta.title;
    const sub = `${meta.span} · ${it.st}단계 ${meta.stages[it.st]} · ${it.no}번`;
    return {
      key: `b-${meta.id}-${it.no}`, no: it.no, st: it.st, dur: Math.round(l10Plan(it).dur / sp),
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp, it.planTag || "방침"), card: `${it.st}단계 · ${meta.stages[it.st]}`,
      title: { e: title, m: title }, sub: { e: sub, m: sub }, tsz: "lesson",
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} uid={uid} />,
      pane: (t, C, u) => <L10Art it={it} t={t * sp} C={C} uid={`${uid}${u}`} region={PANE_REGION} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 틀 설정 — 단원 100제(학교급) · 주차별 회차(학년) ══════════ */
const SPECS = new Map();
/** 학교급 하나의 틀 설정 — 세트 = 단원(목록으로 고름) · 단원 문항은 고를 때 들여온다 */
export function basicsSpec(lv) {
  const L = levelOf(lv);
  if (SPECS.has(L.key)) return SPECS.get(L.key);
  const units = basicsOf(L.key);
  const spec = {
    lsk: `ash.display.basic.${L.key}`, dualLsk: `ash.display.basic.${L.key}`, title: L.title, defSet: units[0].id, cols: 5,
    setMenu: { word: "단원", title: `${L.title} · 단원 ${units.length}가지`, hint: "학년에 묶지 않고 이어지는 단원끼리 — 고르면 그 단원 1번부터 돌아요 · B 다음 단원" },
    sets: units.map((b) => ({ key: b.id, name: b.title, short: b.short, icon: b.icon, note: b.span, sub: unitLabel(b.unit) })),
    stages: (id) => [1, 2, 3, 4, 5].map((v) => ({ v, lab: `${v}단계 ${(basicOf(id) || units[0]).stages[v]}` })),
    ready: (id) => !!basicCached(id),
    load: (id) => loadBasic(id),
    scenes: (id, sp, st) => basicScenes(basicOf(id), basicCached(id), sp, st),
    topExtra: ({ set, open, onOpen, poke }) => <DocsMenu meta={basicOf(set)} set={basicCached(set)} open={open} onOpen={onOpen} poke={poke} />,
  };
  SPECS.set(L.key, spec);
  return spec;
}

/** 유형 번호 ①…⑤ — 목록 그림 대신 */
export const TYPE_NO = ["", "①", "②", "③", "④", "⑤"];
/** 학교급 하나의 유형 틀 설정 — 세트 = 유형(단원 × 1 ~ 5단계, 단원마다 묶어 목록) · 유형 문항 = 단원 문항의 그 단계 20문항(1 ~ 20번) */
export function typesSpec(lv) {
  const L = levelOf(lv);
  const k = `t:${L.key}`;
  if (SPECS.has(k)) return SPECS.get(k);
  const types = basicsOf(L.key).flatMap((b) => typesOf(b.id));
  const spec = {
    lsk: `ash.display.type.${L.key}`, dualLsk: `ash.display.basic.${L.key}`, title: `${L.title} · 유형`, defSet: types[0].id, cols: 5,
    setMenu: { word: "유형", title: `${L.title} · 유형 ${types.length}가지`,
      hint: "단원 100제를 단계마다 나눈 20문항 — 번호 1 ~ 20, 프린트도 유형마다 따로(유형 코드) · 고르면 그 유형 1번부터 · B 다음 유형" },
    sets: types.map((m) => {
      const b = basicOf(m.base);
      return { key: m.id, name: m.title, short: m.short, icon: TYPE_NO[m.st], note: m.span, sub: `${m.name} · ${unitLabel(m.unit)}`,
        grp: `${b.icon} ${b.title} · ${b.span}` };
    }),
    stages: () => [],
    ready: (id) => !!typeCached(id),
    load: (id) => loadType(id),
    scenes: (id, sp) => basicScenes(typeMeta(id), typeCached(id), sp, 0),
    topExtra: ({ set, open, onOpen, poke }) => <DocsMenu meta={typeMeta(set)} set={typeCached(set)} open={open} onOpen={onOpen} poke={poke} />,
  };
  SPECS.set(k, spec);
  return spec;
}

/** 이번 주(학사 달력 — 3월 2일이 든 주가 1주) */
const thisWeek = () => Math.min(52, Math.max(1, weekOfDate().week));

/** 학년 하나의 주차별 틀 설정 — 세트 = 회차 104개(학기 · 방학으로 나눠 목록) · 회차 머리 정보(index)가 들어온 뒤에 만든다 */
export function weeksSpec(gk) {
  const k = `w:${gk}`;
  if (SPECS.has(k)) return SPECS.get(k);
  const h = weekIndexCached(gk), g = gradeOf(gk);
  if (!h || !g) return null;
  const now = thisWeek();
  const per = (w) => PERIODS.find((p) => w >= p.from && w <= p.to);
  const spec = {
    lsk: `ash.display.week.${gk}`, dualLsk: `ash.display.basic.${levelOf(g.level).key}`, title: `${g.grade} 주차별 기초 다지기`, defSet: weekId(gk, now, "A"), cols: 5,
    setMenu: { word: "회차", title: `${g.grade} · 주차별 기초 다지기 104회차`,
      hint: `주 2회(A · B) × 52주 · 회차마다 20문항 · 지금은 ${now}주(${weekLabel(weekOfDate().year, now)}) · B 다음 회차` },
    sets: h.sessions.map((m) => {
      const p = per(m.week);
      return { key: m.id, name: m.title, short: `${m.week}주 ${m.slot}`, icon: KIND_ICON[m.kind] || "•", note: m.kind,
        sub: `${m.title} · ${unitLabel(m.unit)}`, grp: `${p.key} · ${p.from} ~ ${p.to}주`, hot: m.week === now };
    }),
    stages: (id) => [1, 2, 3, 4, 5].map((v) => ({ v, lab: `${v}단계 ${(weekMetaCached(id) || h.sessions[0]).stages[v]}` })),
    ready: (id) => !!weekCached(id),
    load: (id) => loadWeek(id),
    scenes: (id, sp, st) => basicScenes(weekMetaCached(id), weekCached(id), sp, st),
    topExtra: ({ set, open, onOpen, poke }) => <DocsMenu meta={weekMetaCached(set)} set={weekCached(set)} open={open} onOpen={onOpen} poke={poke} />,
  };
  SPECS.set(k, spec);
  return spec;
}

/* ══════════ 액자 ══════════ */
/** 목록 머리 — 「📚 단원 100제」 · 「🧩 유형」 · 「🗓 학년」 칩으로 보기를 바꾼다 */
function ViewChips({ L, view, onView, close }) {
  return (
    <div className="bs-views" role="group" aria-label="보기">
      <button type="button" className={"dsp-chip" + (!view ? " on" : "")} aria-pressed={!view} onClick={() => { onView(null); close(); }}>📚 단원 100제</button>
      <button type="button" className={"dsp-chip" + (view === "types" ? " on" : "")} aria-pressed={view === "types"}
        onClick={() => { onView("types"); close(); }}>🧩 유형</button>
      <span className="bs-views-w">🗓 주차별</span>
      {gradesOfLevel(L.level).map((g) => (
        <button key={g.gk} type="button" className={"dsp-chip" + (view === g.gk ? " on" : "")} aria-pressed={view === g.gk}
          onClick={() => { onView(g.gk); close(); }}>{g.grade}</button>
      ))}
    </div>
  );
}
const VIEW_CSS = `
.bs-views { display: flex; flex-wrap: wrap; align-items: center; gap: .5cqw; margin: .2cqw 0 .6cqw; }
.bs-views .dsp-chip { font-size: 1.05cqw; padding: .4cqw .9cqw; }
.bs-views-w { font-weight: 800; font-size: 1cqw; opacity: .7; margin-left: .8cqw; }
`;

/** 주차별 — 학년 회차 머리 정보를 들여온 뒤 공통 틀로 */
function WeekStage({ gk, pick, menuExtra, onSeen, ...props }) {
  const [h, setH] = useState(() => weekIndexCached(gk));
  const [err, setErr] = useState(null);
  useEffect(() => {
    if (h) return undefined;
    let live = true;
    loadWeekIndex(gk).then((v) => { if (live) setH(v); }).catch((e) => { if (live) setErr(e?.message || "불러오지 못했어요"); });
    return () => { live = false; };
  }, [gk, h]);
  const spec = h ? weeksSpec(gk) : null;
  if (!spec) return <Loading C={props.C} ui={props.ui} onExit={props.onExit} title={`${gradeOf(gk)?.grade || ""} 주차별 기초 다지기`} err={err} />;
  return <LessonFrame spec={spec} pick={pick} menuExtra={menuExtra} onSeen={onSeen} {...props} />;
}

/** 본 기록 하나 — 단원 · 유형 · 회차 key 와 번호(1부터) · first 면 연 횟수도.
 *  단원 100제를 보면 그 문항이 든 유형에도(유형 안 번호로) — 학생앱 목록의 유형 ✓ · 진행 막대 */
export function noteBasicSeen(set, no, first = false) {
  const S = parseWeekId(set) ? weekCached(set) : parseTypeKey(set) ? typeCached(set) : basicCached(set);
  const n = S?.items?.length || 0;
  if (!n || !no) return;
  if (first) noteOpen(set, n);
  noteSeen(set, no, n);
  if (basicOf(set)) {
    const it = S.items.find((x) => x.no === no), tk = it && typeKey(set, it.st), T = tk && typeCached(tk);
    const r = T ? T.items.findIndex((x) => x.src === no) : -1;
    if (r >= 0) noteSeen(tk, r + 1, T.items.length);
  }
}

/** 학교급 액자 — pick: 학생앱에서 고른 단원 · 유형 · 회차(그것부터 단일 모드로) */
export function BasicsFrame({ lv, pick = null, ...props }) {
  const L = levelOf(lv);
  const pw = pick ? parseWeekId(pick) : null;
  const pt = pick ? parseTypeKey(pick) : null;
  const vk = `ash.display.basic.${L.key}.view`;
  const [view, setView] = useState(() => {                    // null = 단원 100제 · "types" = 유형 · 학년 key = 그 학년 주차별
    if (pw) return gradeOf(pw.gk)?.level === L.level ? pw.gk : null;
    if (pt) return basicOf(pt.id)?.level === L.level ? "types" : null;
    if (pick) return null;
    const v = lsRead(vk);
    return v === "types" || (typeof v === "string" && gradeOf(v)?.level === L.level) ? v : null;
  });
  useEffect(() => { lsWrite(vk, view); }, [vk, view]);
  const menuExtra = useCallback(({ close }) => <><style>{VIEW_CSS}</style><ViewChips L={L} view={view} onView={setView} close={close} /></>, [L, view]);
  // 학생앱에서 열었을 때만 본 기록 — 처음 연 단원 · 유형 · 회차는 연 횟수, 장면마다 가장 멀리 본 번호
  const opened = useRef(null);
  const onSeen = useCallback((set, no) => {
    const first = opened.current !== set;
    opened.current = set;
    noteBasicSeen(set, no, first);
  }, []);
  const seen = pick ? onSeen : null;
  if (view === "types") return <LessonFrame key="types" spec={typesSpec(lv)} pick={pt ? pick : null} menuExtra={menuExtra} onSeen={seen} {...props} />;
  if (view) {
    const wp = pw && pw.gk === view ? pick : null;
    return <WeekStage key={view} gk={view} pick={wp} menuExtra={menuExtra} onSeen={seen} {...props} />;
  }
  return <LessonFrame key="units" spec={basicsSpec(lv)} pick={pw || pt ? null : pick} menuExtra={menuExtra} onSeen={seen} {...props} />;
}

/** 액자 목록의 작은 그림 — 학교급마다 고른 한 문항을 다 푼 순간 */
export const BasicsThumb = memo(function BasicsThumb({ fkey, C }) {
  const it = THUMBS[fkey];
  if (!it) return null;
  return <L10Art it={it} t={l10Plan(it).ans + 900} C={C} uid={`th${fkey}`} />;
});

/** 액자 무대(AdminDisplay 의 LABS)에 넣을 학교급 액자 — 셋(모듈이 읽힐 때 한 번 만든다) */
export const BASIC_LABS = Object.fromEntries(LEVELS.map((L) => {
  const F = (props) => <BasicsFrame lv={L.frame} {...props} />;
  F.displayName = `BasicsFrame_${L.key}`;
  return [L.frame, F];
}));
