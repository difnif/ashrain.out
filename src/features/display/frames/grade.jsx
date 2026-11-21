// ashrain.out — 교실 모니터 「액자」 · 학생앱 시청각 학습 › 문제 풀이 해설: 학년별 기본기 해설 (frames/grade.jsx)
// 초1 ~ 고3 학년마다 한 액자 — 기본기 · 원리 세트 둘(100문항씩, 1 ~ 5단계)을 문항마다 한 장면으로 끝없이 돌린다.
//   ① 문제 → ② 방침 → ③ 판서(한 줄씩, 빨간 메모) → ④ 답 · 오른쪽 그림은 판서 줄에 맞춰 자란다(그림 DSL — frames/figdsl.jsx).
// 그리기 · 박자는 일차함수 10단계 액자와 같다(frames/lin10.jsx 의 L10Art · ../lin10.js 의 l10Plan).
// 조작은 해설 액자 공통 틀(frames/lesson.jsx) — 「단일 | 듀얼」(D) · 세트(B) · 빠르기 0.75× ~ 2×(S) · 번호 · 단계 목록(L) · 두 막대 ·
//   듀얼 가운데 ⇄(X). 오른쪽 위 📄 문서(문제지 · 해설지 · 빠른 정답 · OMR 을 골라 확인 → 개별 다운 | 압축 다운 — frames/docsmenu.jsx) —
//   듀얼 모드에서 두 판의 세트가 다르면 세트마다 하나씩.
// 문항 자료는 학년마다 따로 늦게 들여온다(../grades/<학년>.js) — 머리 정보는 ../grades/index.js, 목록 그림용 한 문항은 ../grades/thumbs.js.
import { memo, useEffect, useState } from "react";
import { W, H } from "../draw.jsx";
import { l10Plan } from "../lin10.js";
import { L10Art } from "./lin10.jsx";
import { PANE_REGION } from "../board.js";
import { LessonFrame } from "./lesson.jsx";
import { GRADES, gradeOf, loadGrade, gradeCached } from "../grades/index.js";
import { THUMBS } from "../grades/thumbs.js";
import { DocsMenu } from "./docsmenu.jsx";
import { stepMarks } from "./scrub.jsx";

export { LESSON_SPEEDS as G_SPEEDS } from "./lesson.jsx";

/* ══════════ 장면 목록 (StoryPlayer 형식) ══════════ */
const SCENES = new Map();
export function gradeScenes(g, sets, setKey, sp = 1, stage = 0) {
  const k = `${g.key}|${setKey}|${sp}|${stage}`;
  if (SCENES.has(k)) return SCENES.get(k);
  const meta = g.sets.find((s) => s.key === setKey) || g.sets[0];
  const S = sets[meta.key];
  const list = S.items.filter((it) => !stage || it.st === stage).map((it) => {
    const title = `${g.grade} · ${meta.title}`;
    const sub = `${it.st}단계 ${meta.stages[it.st]} · ${it.no}번`;
    return {
      key: `g-${g.key}-${meta.key}-${it.no}`, no: it.no, st: it.st, dur: Math.round(l10Plan(it).dur / sp),
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp, it.planTag || "방침"), card: `${it.st}단계 · ${meta.stages[it.st]}`,
      title: { e: title, m: title }, sub: { e: sub, m: sub }, tsz: "lesson",
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} uid={`g${g.key}${meta.key}`} />,
      pane: (t, C, uid) => <L10Art it={it} t={t * sp} C={C} uid={`g${g.key}${meta.key}${uid}`} region={PANE_REGION} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 — 조작은 해설 액자 공통 틀(frames/lesson.jsx), 오른쪽 위에 📄 문서 ══════════ */
const SPECS = new Map();
/** 학년 하나의 틀 설정 — 문항을 들여온 뒤 한 번 만든다 */
export function gradeSpec(g, sets) {
  if (SPECS.has(g.key)) return SPECS.get(g.key);
  const metaOf = (k) => g.sets.find((x) => x.key === k) || g.sets[0];
  const spec = {
    lsk: `ash.display.g.${g.key}`, title: g.title, defSet: g.sets[0].key, cols: 5,
    sets: g.sets.map((x) => ({ key: x.key, name: x.title, short: x.short })),
    stages: (set) => [1, 2, 3, 4, 5].map((v) => ({ v, lab: `${v}단계 ${metaOf(set).stages[v]}` })),
    scenes: (set, sp, st) => gradeScenes(g, sets, set, sp, st),
    topExtra: ({ set, open, onOpen, poke }) => <DocsMenu g={g} meta={metaOf(set)} set={sets[metaOf(set).key]} open={open} onOpen={onOpen} poke={poke} />,
  };
  SPECS.set(g.key, spec);
  return spec;
}

export function GradeFrame(props) {
  const { gkey, C, onExit, ui } = props;
  const g = gradeOf(gkey);
  const [sets, setSets] = useState(() => gradeCached(gkey));
  const [err, setErr] = useState(null);
  useEffect(() => {
    if (sets) return undefined;
    let live = true;
    loadGrade(gkey).then((x) => { if (live) setSets(x); }).catch((e) => { if (live) setErr(e?.message || "불러오지 못했어요"); });
    return () => { live = false; };
  }, [gkey, sets]);
  if (err || !sets) {
    const { Btn, Ic } = ui;
    return (
      <>
        <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label={g.title}>
          <text x={W / 2} y={H / 2} textAnchor="middle" fontSize="40" fontWeight="700" fill={C.soft}>{err ? `해설을 불러오지 못했어요 — ${err}` : "해설을 불러오는 중…"}</text>
        </svg>
        <div className="dsp-ctl show"><Btn title="나가기" onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn></div>
      </>
    );
  }
  return <LessonFrame spec={gradeSpec(g, sets)} {...props} />;
}

/** 액자 목록의 작은 그림 — 학년마다 고른 한 문항을 다 푼 순간 */
export const GradeThumb = memo(function GradeThumb({ gkey, C }) {
  const it = THUMBS[gkey];
  if (!it) return null;
  return <L10Art it={it} t={l10Plan(it).ans + 900} C={C} uid={`th${gkey}`} />;
});

/** 액자 무대(AdminDisplay 의 LABS)에 넣을 학년별 액자 — key 마다 컴포넌트 하나(모듈이 읽힐 때 한 번 만든다) */
export const GRADE_LABS = Object.fromEntries(GRADES.map((g) => {
  const F = (props) => <GradeFrame gkey={g.key} {...props} />;
  F.displayName = `GradeFrame_${g.key}`;
  return [g.key, F];
}));
