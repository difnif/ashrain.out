// ashrain.out — 교실 모니터 「액자」: 경우의 수와 확률 100제 해설 (frames/cnt100.jsx)
// 학원 프린트 「학년별 선발」 · 「주머니 공 꺼내기」 · 「사전식 나열(영어 단어)」 · 「한 줄로 세우기(이웃 · 양 끝)」 100제(중2-2)를
//   문항마다 한 장면으로 끝없이 돌린다 — ① 문제 → ② 전략 → ③ 판서(포지티브 · 네거티브 → 식 한 줄씩) → ④ 답.
// 그리기 · 박자는 일차함수 10단계 액자(frames/lin10.jsx 의 L10Art · ../lin10.js 의 l10Plan)를 그대로 쓴다.
//   사전식은 「숫자 분석」 → 묶음 개수로 시작 글자 → 최종 묶음, 오른쪽에 세로 나무(frames/lextree.jsx — 칠판 판서 그대로).
// 이 액자만의 것: 「선발 | 공 꺼내기 | 사전식 | 줄 세우기」(B로 차례로) · 「1× | 1.5×」 · 번호 목록(L) — 목록 위 단계 칩(전체 · 1~5단계)으로 고르면 그 단계만 돈다.
// 문항: ../cnt100-items.js
import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { l10Plan } from "../lin10.js";
import { C100_SETS, C100_KEYS, C100_SPEEDS } from "../cnt100.js";
import { L10Art } from "./lin10.jsx";
import { StoryPlayer } from "./player.jsx";
import { Seg, useKeys, lsRead, lsWrite } from "./xkit.jsx";

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
      key: `c100-${setKey}-${it.no}`, no: it.no, st: it.st, dur: Math.round(l10Plan(it).dur / sp),
      title: { e: title, m: title }, sub: { e: sub, m: sub },
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} uid={`c${setKey}`} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 ══════════ */
const LSK = "ash.display.cnt100";
const fixSet = (v) => (C100_SETS[v] ? v : "sel");
const fixSp = (v) => (C100_SPEEDS.includes(v) ? v : 1);
const fixSt = (v) => (Number.isInteger(v) && v >= 0 && v <= 5 ? v : 0);

export function Cnt100Frame(props) {
  const { ui, poke, inert } = props;
  const { Btn, Ic } = ui;
  const [cfg, setCfg] = useState(() => { const o = lsRead(LSK) || {}; return { set: fixSet(o.set), sp: fixSp(o.sp), st: fixSt(o.st) }; });
  useEffect(() => { lsWrite(LSK, cfg); }, [cfg]);
  const [list, setList] = useState(false);
  const [cur, setCur] = useState(0);
  const api = useRef(null);
  const scenes = useMemo(() => c100Scenes(cfg.set, cfg.sp, cfg.st), [cfg]);
  const pickSet = useCallback((v) => setCfg((c) => ({ ...c, set: fixSet(v) })), []);
  const pickSp = useCallback((v) => setCfg((c) => ({ ...c, sp: fixSp(v) })), []);
  const pickSt = useCallback((v) => setCfg((c) => ({ ...c, st: fixSt(v) })), []);
  useKeys({
    l: () => { setList((v) => !v); poke(); },
    b: () => { pickSet(C100_KEYS[(C100_KEYS.indexOf(cfg.set) + 1) % C100_KEYS.length]); poke(); },
    s: () => { pickSp(cfg.sp === 1 ? 1.5 : 1); poke(); },
    Escape: () => setList(false),
  }, inert);
  const extra = (
    <>
      <span className="dsp-sep" />
      <Seg label="세트" value={cfg.set} options={C100_KEYS.map((k) => [k, C100_SETS[k].short || C100_SETS[k].name])} onChange={pickSet} poke={poke} />
      <Seg label="빠르기" value={cfg.sp} options={[[1, "1×"], [1.5, "1.5×"]]} onChange={pickSp} poke={poke} />
      <Btn title="번호 · 단계 목록 (L)" on={list} onClick={() => { setList((v) => !v); poke(); }}>
        <Ic d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" />
      </Btn>
      <span className="dsp-sep" />
    </>
  );
  const pick = (i) => { api.current?.goTo(i); setList(false); poke(); };
  const label = `경우의 수와 확률 100제 해설 · ${C100_SETS[cfg.set].name}${cfg.st ? ` · ${cfg.st}단계` : ""}`;
  return (
    <>
      <StoryPlayer key={`${cfg.set}|${cfg.sp}|${cfg.st}`} list={scenes} lsKey={`${LSK}.${cfg.set}.${cfg.st}`} label={label}
        {...props} inert={inert || list} noMode extra={extra} apiRef={api} onIdx={setCur} />
      {list && <NumList scenes={scenes} cfg={cfg} cur={cur} onPick={pick} onStage={(v) => { pickSt(v); poke(); }} onClose={() => setList(false)} />}
    </>
  );
}

/** 번호 · 단계 목록 — 단계 칩을 고르면 그 단계만 돌고, 번호를 고르면 그 문항부터 */
function NumList({ scenes, cfg, cur, onPick, onStage, onClose }) {
  const S = C100_SETS[cfg.set];
  const lap = scenes.reduce((s, x) => s + x.dur, 0);
  const cnt = (v) => S.items.filter((it) => it.st === v).length;
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호 · 단계 목록">
        <style>{".c100-grid { grid-template-columns: repeat(5, 1fr); }"}</style>
        <div className="dsp-list-h">
          <b>경우의 수와 확률 100제 · {S.name}</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="dsp-chips">
          {[0, 1, 2, 3, 4, 5].map((v) => (
            <button key={v} type="button" className={"dsp-chip" + (cfg.st === v ? " on" : "")} aria-pressed={cfg.st === v} onClick={() => onStage(v)}>
              {v ? `${v}단계` : `전체 ${S.items.length}`}
            </button>
          ))}
        </div>
        <p className="dsp-gal-sub">
          {cfg.st ? `${cfg.st}단계 ${S.stage[cfg.st]} ${cnt(cfg.st)}문항만 돌아요` : "1단계부터 5단계까지 차례로 돌아요"} · 한 바퀴 약 {Math.round(lap / 60000)}분 · 지금 {scenes[cur]?.no}번 · 번호를 고르면 그 문항부터
        </p>
        <div className="dsp-grid c100-grid">
          {scenes.map((s, i) => (
            <button key={s.key} type="button" className={"dsp-card" + (i === cur ? " on" : "")} onClick={() => onPick(i)}>
              <span className="n">{s.no}</span>
              <span className="e">{s.st}단계 · {S.stage[s.st]}</span>
              <span className="m">{Math.round(s.dur / 1000)}초</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

/** 액자 목록의 작은 그림 — 주머니 공 87번(세 수의 합이 홀수일 확률) 다 푼 순간 */
export const Cnt100Thumb = memo(function Cnt100Thumb({ C }) {
  const it = C100_SETS.ball.items[86];
  return <L10Art it={it} t={l10Plan(it).ans + 900} C={C} uid="c100th" />;
});
