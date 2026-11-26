// ashrain.out — 교실 모니터 「액자」 · 학생앱 시청각 학습 › 문제 풀이 해설: 시그니처 프린트 해설 액자 둘 (frames/prints.jsx)
//   「두 점을 지나는 일차함수의 식 해설」(lin2) — 프린트 1 ~ 5세트(10단계 × 10문항): ① 기울기 → ② 한 점 대입 → ③ 식.
//      그림: 두 점에서 x · y의 증가량 화살이 자라고, 두 점을 지나는 직선이 그어지며 y절편(상수항 b)이 찍힌다.
//   「직선의 교점 · 만날 조건 해설」(meet) — 교점 활용 100제(두 상황의 그래프가 만나는 점) · 직선이 도형과 만날 조건 쉬운 판 · 중~상 판
//      (정점을 지나는 직선이 꼭짓점 사이를 돌며 쓸고 지나감 · 기울기가 정해진 직선은 미끄러짐) · 세 직선으로 삼각형이 만들어질 조건
//      (기울기가 같은 경우의 점선 → 두 직선의 교점 → 미지수 직선이 교점을 지나도록).
// 그리기 · 박자는 기본기 해설과 같다(frames/lin10.jsx 의 L10Art — 그림 DSL · ../lin10.js 의 l10Plan). 조작은 해설 액자 공통 틀(frames/lesson.jsx).
// 문항은 세트마다 고를 때 들여온다(../prints/index.js — spec.ready · load). 학생앱 목록 · 듀얼 「전부」에는 frames/index.js 의 prints 로 한 줄씩.
import { memo } from "react";
import { l10Plan } from "../lin10.js";
import { PANE_REGION } from "../board.js";
import { L10Art } from "./lin10.jsx";
import { stepMarks } from "./scrub.jsx";
import { LessonFrame } from "./lesson.jsx";
import { PRINT_FRAMES, printCached, loadPrintSet } from "../prints/index.js";
import { THUMBS } from "../prints/thumbs.js";

/* ══════════ 장면 목록 (StoryPlayer 형식) ══════════ */
const SCENES = new Map();
export function printScenes(fk, setKey, sp = 1, stage = 0) {
  const k = `${fk}|${setKey}|${sp}|${stage}`;
  if (SCENES.has(k)) return SCENES.get(k);
  const F = PRINT_FRAMES[fk], S = F.sets[setKey], items = printCached(fk, setKey);
  if (!items) return [];
  const uid = `p${fk}${setKey}`;
  const list = items.filter((it) => !stage || it.st === stage).map((it) => {
    const title = `${F.title.replace(/ 해설$/, "")} · ${S.name}`;
    const sub = `${it.st}단계 ${S.stage[it.st]} · ${it.no}번`;
    return {
      key: `${fk}-${setKey}-${it.no}`, no: it.no, st: it.st, it, dur: Math.round(l10Plan(it).dur / sp),
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp, "방침"), card: `${it.st}단계 · ${S.stage[it.st]}`,
      title: { e: title, m: title }, sub: { e: sub, m: sub }, tsz: "lesson",
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} uid={uid} />,
      pane: (t, C, u) => <L10Art it={it} t={t * sp} C={C} uid={`${uid}${u}`} region={PANE_REGION} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 틀 설정 ══════════ */
function makeSpec(fk) {
  const F = PRINT_FRAMES[fk];
  return {
    lsk: `ash.display.${fk}`, title: F.title, defSet: F.keys[0], cols: 5,
    sets: F.keys.map((k) => ({ key: k, name: F.sets[k].name, short: F.sets[k].short })),
    stages: (set) => {
      const st = F.sets[set]?.stage || {};
      return Object.keys(st).map(Number).map((v) => ({ v, lab: `${v}단계 ${st[v]}`, chip: `${v}단계` }));
    },
    scenes: (set, sp, st) => printScenes(fk, set, sp, st),
    ready: (set) => !!printCached(fk, set),
    load: (set) => loadPrintSet(fk, set),
  };
}
export const LIN2_SPEC = makeSpec("lin2");
export const MEET_SPEC = makeSpec("meet");

export function Lin2Frame(props) {
  return <LessonFrame spec={LIN2_SPEC} {...props} />;
}
export function MeetFrame(props) {
  return <LessonFrame spec={MEET_SPEC} {...props} />;
}

/** 액자 목록의 작은 그림 — 다 푼 순간(../prints/thumbs.js 의 한 문항) */
export const Lin2Thumb = memo(function Lin2Thumb({ C }) {
  const it = THUMBS.lin2;
  return <L10Art it={it} t={l10Plan(it).ans + 900} C={C} uid="l2th" />;
});
export const MeetThumb = memo(function MeetThumb({ C }) {
  const it = THUMBS.meet;
  return <L10Art it={it} t={l10Plan(it).ans + 900} C={C} uid="mtth" />;
});
