// ashrain.out — 교실 모니터 「액자」 · 학생앱 시청각 학습 › 문제 풀이 해설: 학년별 기본기 해설 (frames/grade.jsx)
// 초1 ~ 고3 학년마다 한 액자 — 기본기 · 원리 세트 둘(100문항씩, 1 ~ 5단계)을 문항마다 한 장면으로 끝없이 돌린다.
//   ① 문제 → ② 방침 → ③ 판서(한 줄씩, 빨간 메모) → ④ 답 · 오른쪽 그림은 판서 줄에 맞춰 자란다(그림 DSL — frames/figdsl.jsx).
// 그리기 · 박자는 일차함수 10단계 액자와 같다(frames/lin10.jsx 의 L10Art · ../lin10.js 의 l10Plan).
// 조작: 「세트 A | 세트 B」(B) · 「1× | 1.5×」(S) · 번호 · 단계 목록(L — 단계 칩을 고르면 그 단계만) · 오른쪽 위 📄 문서 ·
//   두 막대(frames/scrub.jsx — 아래 긴 막대 = 문항 이동, 옆 짧은 막대 = 풀이 이동: 문제 · 방침 · 판서 줄 · 답)
//   (문제지 · 해설지 · 빠른 정답 · OMR 을 골라 확인 → 개별 다운 | 압축 다운 — frames/docsmenu.jsx).
// 문항 자료는 학년마다 따로 늦게 들여온다(../grades/<학년>.js) — 머리 정보는 ../grades/index.js, 목록 그림용 한 문항은 ../grades/thumbs.js.
import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { W, H } from "../draw.jsx";
import { l10Plan } from "../lin10.js";
import { L10Art } from "./lin10.jsx";
import { StoryPlayer } from "./player.jsx";
import { Seg, useKeys, lsRead, lsWrite } from "./xkit.jsx";
import { GRADES, gradeOf, loadGrade, gradeCached } from "../grades/index.js";
import { THUMBS } from "../grades/thumbs.js";
import { DocsMenu } from "./docsmenu.jsx";
import { stepMarks } from "./scrub.jsx";

export const G_SPEEDS = [1, 1.5];

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
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp, it.planTag || "방침"),
      title: { e: title, m: title }, sub: { e: sub, m: sub },
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} uid={`g${g.key}${meta.key}`} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 ══════════ */
export function GradeFrame(props) {
  const { gkey, ui, poke, inert, C, onExit } = props;
  const g = gradeOf(gkey);
  const LSK = `ash.display.g.${gkey}`;
  const fixSet = (v) => (g.sets.some((s) => s.key === v) ? v : g.sets[0].key);
  const fixSp = (v) => (G_SPEEDS.includes(v) ? v : 1);
  const fixSt = (v) => (Number.isInteger(v) && v >= 0 && v <= 5 ? v : 0);
  const [cfg, setCfg] = useState(() => { const o = lsRead(LSK) || {}; return { set: fixSet(o.set), sp: fixSp(o.sp), st: fixSt(o.st) }; });
  useEffect(() => { lsWrite(LSK, cfg); }, [cfg, LSK]);
  const [sets, setSets] = useState(() => gradeCached(gkey));
  const [err, setErr] = useState(null);
  useEffect(() => {
    if (sets) return undefined;
    let live = true;
    loadGrade(gkey).then((s) => { if (live) setSets(s); }).catch((e) => { if (live) setErr(e?.message || "불러오지 못했어요"); });
    return () => { live = false; };
  }, [gkey, sets]);
  const [list, setList] = useState(false);
  const [docs, setDocs] = useState(false);
  const [cur, setCur] = useState(0);
  const api = useRef(null);
  const meta = g.sets.find((s) => s.key === cfg.set) || g.sets[0];
  const scenes = useMemo(() => (sets ? gradeScenes(g, sets, cfg.set, cfg.sp, cfg.st) : null), [g, sets, cfg]);
  const pickSet = useCallback((v) => setCfg((c) => ({ ...c, set: fixSet(v) })), []);   // eslint-disable-line react-hooks/exhaustive-deps
  const pickSp = useCallback((v) => setCfg((c) => ({ ...c, sp: fixSp(v) })), []);      // eslint-disable-line react-hooks/exhaustive-deps
  const pickSt = useCallback((v) => setCfg((c) => ({ ...c, st: fixSt(v) })), []);      // eslint-disable-line react-hooks/exhaustive-deps
  useKeys({
    l: () => { setList((v) => !v); poke(); },
    b: () => { const ks = g.sets.map((s) => s.key); pickSet(ks[(ks.indexOf(cfg.set) + 1) % ks.length]); poke(); },
    s: () => { pickSp(cfg.sp === 1 ? 1.5 : 1); poke(); },
    Escape: () => { setList(false); setDocs(false); },
  }, inert || docs);
  if (err || !scenes) {
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
  const { Btn, Ic } = ui;
  const extra = (
    <>
      <span className="dsp-sep" />
      {g.sets.length > 1 && <Seg label="세트" value={cfg.set} options={g.sets.map((s) => [s.key, s.short])} onChange={pickSet} poke={poke} />}
      <Seg label="빠르기" value={cfg.sp} options={[[1, "1×"], [1.5, "1.5×"]]} onChange={pickSp} poke={poke} />
      <Btn title="번호 · 단계 목록 (L)" on={list} onClick={() => { setList((v) => !v); poke(); }}>
        <Ic d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" />
      </Btn>
      <span className="dsp-sep" />
    </>
  );
  const pick = (i) => { api.current?.goTo(i); setList(false); poke(); };
  const label = `${g.title} · ${meta.title}${cfg.st ? ` · ${cfg.st}단계` : ""}`;
  const top = <DocsMenu g={g} meta={meta} set={sets[meta.key]} open={docs} onOpen={(v) => { setDocs(v); poke(); }} poke={poke} />;
  return (
    <>
      <StoryPlayer key={`${cfg.set}|${cfg.sp}|${cfg.st}`} list={scenes} lsKey={`${LSK}.${cfg.set}.${cfg.st}`} label={label}
        {...props} inert={inert || list || docs} noMode extra={extra} topExtra={top} apiRef={api} onIdx={setCur} scrub />
      {list && <NumList g={g} meta={meta} scenes={scenes} cfg={cfg} cur={cur} onPick={pick} onStage={(v) => { pickSt(v); poke(); }} onClose={() => setList(false)} />}
    </>
  );
}

/** 번호 · 단계 목록 — 단계 칩을 고르면 그 단계만 돌고, 번호를 고르면 그 문항부터 */
function NumList({ g, meta, scenes, cfg, cur, onPick, onStage, onClose }) {
  const lap = scenes.reduce((s, x) => s + x.dur, 0);
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호 · 단계 목록">
        <style>{".gr-grid { grid-template-columns: repeat(5, 1fr); }"}</style>
        <div className="dsp-list-h">
          <b>{g.grade} · {meta.title}</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="dsp-chips">
          {[0, 1, 2, 3, 4, 5].map((v) => (
            <button key={v} type="button" className={"dsp-chip" + (cfg.st === v ? " on" : "")} aria-pressed={cfg.st === v} onClick={() => onStage(v)}>
              {v ? `${v}단계 ${meta.stages[v]}` : `전체 ${meta.n}`}
            </button>
          ))}
        </div>
        <p className="dsp-gal-sub">
          {cfg.st ? `${cfg.st}단계 ${meta.stages[cfg.st]}만 돌아요` : "1단계부터 5단계까지 차례로 돌아요"} · 한 바퀴 약 {Math.max(1, Math.round(lap / 60000))}분 · 지금 {scenes[cur]?.no}번 · 번호를 고르면 그 문항부터
        </p>
        <div className="dsp-grid gr-grid">
          {scenes.map((s, i) => (
            <button key={s.key} type="button" className={"dsp-card" + (i === cur ? " on" : "")} onClick={() => onPick(i)}>
              <span className="n">{s.no}</span>
              <span className="e">{s.st}단계 · {meta.stages[s.st]}</span>
              <span className="m">{Math.round(s.dur / 1000)}초</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
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
