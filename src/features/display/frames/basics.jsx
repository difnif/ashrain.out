// ashrain.out — 교실 모니터 「액자」 · 학생앱 시청각 학습 › 문제 풀이 해설: 기본기 해설 (frames/basics.jsx)
// 초등 · 중등 · 고등 학교급마다 한 액자 — 단원(100문항, 1 ~ 5단계)을 골라 문항마다 한 장면으로 끝없이 돌린다.
// 단원은 학년에 묶지 않고 학년을 넘나든다(span — 초3~초5 처럼). 학생앱에서는 단원마다 한 항목(#/av/<단원 id>)이라
// 그 단원으로 바로 열리고(pick), 액자 안 「단원」(U)으로 같은 학교급의 다른 단원으로 옮길 수 있다.
//   ① 문제 → ② 방침 → ③ 판서(한 줄씩, 빨간 메모) → ④ 답 · 오른쪽 그림은 판서 줄에 맞춰 자란다(그림 DSL — frames/figdsl.jsx).
// 그리기 · 박자는 일차함수 10단계 액자와 같다(frames/lin10.jsx 의 L10Art · ../lin10.js 의 l10Plan).
// 조작은 해설 액자 공통 틀(frames/lesson.jsx) — 「보기 단일 | 듀얼」(D) · 「단원」 목록(U · B 다음 단원) · 빠르기 0.75× ~ 2×(S) ·
//   번호 · 단계 목록(L — 단계 칩을 고르면 그 단계만) · 두 막대(아래 긴 막대 = 문항 이동, 옆 짧은 막대 = 풀이 이동) · 듀얼 가운데 ⇄(X).
//   듀얼 판마다 단원을 따로 고른다(같은 단원 둘도 됨). 오른쪽 위 📄 문서(문제지 · 해설지 · 빠른 정답 · OMR — frames/docsmenu.jsx) —
//   듀얼에서 두 판의 단원이 다르면 단원마다 하나씩. 단원 문항은 고를 때 들여온다(spec.load).
// 문항 자료는 단원마다 따로 늦게 들여온다(../basics/<단원>.js) — 머리 정보는 ../basics/index.js, 목록 그림용 한 문항은 ../basics/thumbs.js.
import { memo } from "react";
import { l10Plan } from "../lin10.js";
import { PANE_REGION } from "../board.js";
import { L10Art } from "./lin10.jsx";
import { LessonFrame, LESSON_SPEEDS } from "./lesson.jsx";
import { LEVELS, levelOf, basicsOf, basicOf, loadBasic, basicCached } from "../basics/index.js";
import { THUMBS } from "../basics/thumbs.js";
import { DocsMenu } from "./docsmenu.jsx";
import { stepMarks } from "./scrub.jsx";
import { unitLabel } from "../../../lib/units.js";

export const B_SPEEDS = LESSON_SPEEDS;

/* ══════════ 장면 목록 (StoryPlayer 형식) ══════════ */
const SCENES = new Map();
export function basicScenes(meta, set, sp = 1, stage = 0) {
  const k = `${meta.id}|${sp}|${stage}`;
  if (SCENES.has(k)) return SCENES.get(k);
  const list = set.items.filter((it) => !stage || it.st === stage).map((it) => {
    const title = meta.title;
    const sub = `${meta.span} · ${it.st}단계 ${meta.stages[it.st]} · ${it.no}번`;
    return {
      key: `b-${meta.id}-${it.no}`, no: it.no, st: it.st, dur: Math.round(l10Plan(it).dur / sp),
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp, it.planTag || "방침"), card: `${it.st}단계 · ${meta.stages[it.st]}`,
      title: { e: title, m: title }, sub: { e: sub, m: sub }, tsz: "lesson",
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} uid={`b${meta.id}`} />,
      pane: (t, C, uid) => <L10Art it={it} t={t * sp} C={C} uid={`b${meta.id}${uid}`} region={PANE_REGION} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 — 조작은 해설 액자 공통 틀(frames/lesson.jsx) ══════════ */
const SPECS = new Map();
/** 학교급 하나의 틀 설정 — 세트 = 단원(목록으로 고름) · 단원 문항은 고를 때 들여온다 */
export function basicsSpec(lv) {
  const L = levelOf(lv);
  if (SPECS.has(L.key)) return SPECS.get(L.key);
  const units = basicsOf(L.key);
  const spec = {
    lsk: `ash.display.basic.${L.key}`, title: L.title, defSet: units[0].id, cols: 5,
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

/** 학교급 액자 — pick: 학생앱에서 고른 단원(그 단원부터 단일 모드로) */
export function BasicsFrame({ lv, ...props }) {
  return <LessonFrame spec={basicsSpec(lv)} {...props} />;
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
