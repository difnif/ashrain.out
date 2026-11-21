// ashrain.out — 교실 모니터 「액자」: 경우의 수와 확률 100제 해설 (frames/cnt100.jsx)
// 학원 프린트 「학년별 선발」 · 「주머니 공 꺼내기」 · 「사전식 나열(영어 단어)」 · 「한 줄로 세우기(이웃 · 양 끝)」 100제(중2-2)를
//   문항마다 한 장면으로 끝없이 돌린다 — ① 문제 → ② 전략 → ③ 판서(포지티브 · 네거티브 → 식 한 줄씩) → ④ 답.
// 그리기 · 박자는 일차함수 10단계 액자(frames/lin10.jsx 의 L10Art · ../lin10.js 의 l10Plan)를 그대로 쓴다.
//   사전식은 「숫자 분석」 → 묶음 개수로 시작 글자 → 최종 묶음, 그림은 세로 나무(frames/lextree.jsx — 칠판 판서 그대로).
//   그림(줄 세우기 자리 칸 · 학년별 학생 · 주머니 공 · 사전식 세로 나무 — frames/c100fig.jsx)은 글자를 다 놓고 남은 빈자리에(../board.js).
// 조작은 해설 액자 공통 틀(frames/lesson.jsx) — 「단일 | 듀얼」 · 「선발 | 공 꺼내기 | 사전식 | 줄 세우기」 · 빠르기 0.75× ~ 2× · 번호 · 단계 목록 ·
//   두 막대 · 듀얼 가운데 ⇄. 듀얼 판(반쪽)에도 같은 규칙 — 글자를 먼저 놓고 남은 자리가 넉넉하면 그림도.
// 문항: ../cnt100-items.js
import { memo } from "react";
import { l10Plan } from "../lin10.js";
import { PANE_REGION } from "../board.js";
import { C100_SETS, C100_KEYS } from "../cnt100.js";
import { L10Art } from "./lin10.jsx";
import { stepMarks } from "./scrub.jsx";
import { LessonFrame, paneLoad as paneLoad0, DUAL_SPEEDS } from "./lesson.jsx";

export { DUAL_SPEEDS };

/* ══════════ 장면 목록 (StoryPlayer 형식) ══════════ */
const SCENES = new Map();
export function c100Scenes(setKey, sp = 1, stage = 0) {
  const k = `${setKey}|${sp}|${stage}`;
  if (SCENES.has(k)) return SCENES.get(k);
  const S = C100_SETS[setKey];
  const list = S.items.filter((it) => !stage || it.st === stage).map((it) => {
    const title = `경우의 수와 확률 100제 · ${S.name}`;
    const sub = `${it.st}단계 ${S.stage[it.st]} · ${it.no}번`;
    return {
      key: `c100-${setKey}-${it.no}`, no: it.no, st: it.st, it, dur: Math.round(l10Plan(it).dur / sp),
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp, it.planTag || "방침"), card: `${it.st}단계 · ${S.stage[it.st]}`,
      title: { e: title, m: title }, sub: { e: sub, m: sub }, tsz: "lesson",
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} uid={`c${setKey}`} />,
      pane: (t, C, uid) => <L10Art it={it} t={t * sp} C={C} uid={`c${setKey}${uid}`} region={PANE_REGION} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 ══════════ */
export const C100_SPEC = {
  lsk: "ash.display.cnt100", title: "경우의 수와 확률 100제 해설", defSet: "sel", cols: 5,
  sets: C100_KEYS.map((k) => ({ key: k, name: C100_SETS[k].name, short: C100_SETS[k].short || C100_SETS[k].name })),
  stages: (set) => [1, 2, 3, 4, 5].map((v) => ({ v, lab: `${v}단계 ${C100_SETS[set].stage[v]}`, chip: `${v}단계` })),
  scenes: c100Scenes,
};
export const paneLoad = (o, side, setDefault, now) => paneLoad0(C100_SPEC, o, side, setDefault, now);

export function Cnt100Frame(props) {
  return <LessonFrame spec={C100_SPEC} {...props} />;
}

/** 액자 목록의 작은 그림 — 주머니 공 87번(세 수의 합이 홀수일 확률) 다 푼 순간 */
export const Cnt100Thumb = memo(function Cnt100Thumb({ C }) {
  const it = C100_SETS.ball.items[86];
  return <L10Art it={it} t={l10Plan(it).ans + 900} C={C} uid="c100th" />;
});
