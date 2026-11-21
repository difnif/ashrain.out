// ashrain.out — 교실 모니터 「액자」 · 학생앱 시청각 학습 › 문제 풀이 해설: 기본기 해설 (frames/basics.jsx)
// 초등 · 중등 · 고등 학교급마다 한 액자 — 단원(100문항, 1 ~ 5단계)을 골라 문항마다 한 장면으로 끝없이 돌린다.
// 단원은 학년에 묶지 않고 학년을 넘나든다(span — 초3~초5 처럼). 학생앱에서는 단원마다 한 항목(#/av/<단원 id>)이라
// 그 단원으로 바로 열리고(pick), 액자 안 「단원」(U)으로 같은 학교급의 다른 단원으로 옮길 수 있다.
//   ① 문제 → ② 방침 → ③ 판서(한 줄씩, 빨간 메모) → ④ 답 · 오른쪽 그림은 판서 줄에 맞춰 자란다(그림 DSL — frames/figdsl.jsx).
// 그리기 · 박자는 일차함수 10단계 액자와 같다(frames/lin10.jsx 의 L10Art · ../lin10.js 의 l10Plan).
// 조작: 「단원」 목록(U · B 다음 단원) · 「1× | 1.5×」(S) · 번호 · 단계 목록(L — 단계 칩을 고르면 그 단계만) · 오른쪽 위 📄 문서 ·
//   두 막대(frames/scrub.jsx — 아래 긴 막대 = 문항 이동, 옆 짧은 막대 = 풀이 이동: 문제 · 방침 · 판서 줄 · 답)
//   (문제지 · 해설지 · 빠른 정답 · OMR 을 골라 확인 → 개별 다운 | 압축 다운 — frames/docsmenu.jsx).
// 문항 자료는 단원마다 따로 늦게 들여온다(../basics/<단원>.js) — 머리 정보는 ../basics/index.js, 목록 그림용 한 문항은 ../basics/thumbs.js.
import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { W, H } from "../draw.jsx";
import { l10Plan } from "../lin10.js";
import { L10Art } from "./lin10.jsx";
import { StoryPlayer } from "./player.jsx";
import { Seg, useKeys, lsRead, lsWrite } from "./xkit.jsx";
import { LEVELS, levelOf, basicsOf, basicOf, loadBasic, basicCached } from "../basics/index.js";
import { THUMBS } from "../basics/thumbs.js";
import { DocsMenu } from "./docsmenu.jsx";
import { stepMarks } from "./scrub.jsx";
import { unitLabel } from "../../../lib/units.js";
import { parseWeekId, gradeOf, gradesOfLevel, loadWeekIndex, weekIndexCached, loadWeekMeta, weekMetaCached, loadWeek, weekCached,
  PERIODS, KIND_ICON, weekOfDate, weekLabel } from "../weeks/index.js";
import { noteOpen, noteSeen } from "../../../lib/avHistory.js";

export const B_SPEEDS = [1, 1.5];

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
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp, it.planTag || "방침"),
      title: { e: title, m: title }, sub: { e: sub, m: sub },
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} uid={`b${meta.id}`} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 ══════════ */
export function BasicsFrame(props) {
  const { lv, pick, ui, poke, inert, C, onExit } = props;
  const L = levelOf(lv);
  const units = basicsOf(lv);
  const grades = gradesOfLevel(L.level);
  const LSK = `ash.display.basic.${L.key}`;
  const okId = (v) => units.some((b) => b.id === v) || (!!parseWeekId(v) && gradeOf(parseWeekId(v).gk)?.level === L.level);
  const fixId = (v) => (okId(v) ? v : units[0].id);
  const fixSp = (v) => (B_SPEEDS.includes(v) ? v : 1);
  const fixSt = (v) => (Number.isInteger(v) && v >= 0 && v <= 5 ? v : 0);
  const [cfg, setCfg] = useState(() => {
    const o = lsRead(LSK) || {};
    const p = pick && okId(pick) ? pick : null;     // 학생앱에서 고른 단원 · 회차면 그것부터(단계는 처음부터)
    return { id: fixId(p || o.id), sp: fixSp(o.sp), st: p && p !== o.id ? 0 : fixSt(o.st) };
  });
  useEffect(() => { lsWrite(LSK, cfg); }, [cfg, LSK]);
  const wk = parseWeekId(cfg.id);
  const [wmeta, setWmeta] = useState(() => (wk ? weekMetaCached(cfg.id) : null));
  const [set, setSet] = useState(() => (wk ? weekCached(cfg.id) : basicCached(cfg.id)));
  const [err, setErr] = useState(null);
  useEffect(() => {
    let live = true;
    setErr(null);
    if (wk) {
      const m = weekMetaCached(cfg.id);
      if (m) setWmeta(m);
      else loadWeekMeta(cfg.id).then((v) => { if (live) setWmeta(v); }).catch((e) => { if (live) setErr(e?.message || "불러오지 못했어요"); });
    }
    const c = wk ? weekCached(cfg.id) : basicCached(cfg.id);
    if (c) { setSet(c); return () => { live = false; }; }
    setSet(null);
    (wk ? loadWeek : loadBasic)(cfg.id).then((v) => { if (live) setSet(v); }).catch((e) => { if (live) setErr(e?.message || "불러오지 못했어요"); });
    return () => { live = false; };
  }, [cfg.id]);   // eslint-disable-line react-hooks/exhaustive-deps
  const meta = wk ? (wmeta && wmeta.id === cfg.id ? { ...wmeta, icon: KIND_ICON[wmeta.kind] || "🗓" } : null) : basicOf(cfg.id);
  const [list, setList] = useState(false);
  const [unitsOpen, setUnitsOpen] = useState(false);
  const [docs, setDocs] = useState(false);
  const [cur, setCur] = useState(0);
  const api = useRef(null);
  const ready = !!meta && set && set.id === cfg.id;
  const scenes = useMemo(() => (ready ? basicScenes(meta, set, cfg.sp, cfg.st) : null), [ready, meta, set, cfg.sp, cfg.st]);
  // 학생앱에서 연 것만 본 기록을 남긴다(교실 모니터는 남기지 않는다)
  useEffect(() => { if (pick && ready) noteOpen(cfg.id, set.items.length); }, [pick, ready, cfg.id]);   // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (pick && scenes && scenes[cur]) noteSeen(cfg.id, scenes[cur].no, set.items.length); }, [pick, scenes, cur]);   // eslint-disable-line react-hooks/exhaustive-deps
  const pickId = useCallback((v) => setCfg((c) => (c.id === v ? c : { ...c, id: fixId(v), st: 0 })), []);   // eslint-disable-line react-hooks/exhaustive-deps
  const pickSp = useCallback((v) => setCfg((c) => ({ ...c, sp: fixSp(v) })), []);      // eslint-disable-line react-hooks/exhaustive-deps
  const pickSt = useCallback((v) => setCfg((c) => ({ ...c, st: fixSt(v) })), []);      // eslint-disable-line react-hooks/exhaustive-deps
  const nextId = () => {
    if (wk) {
      const h = weekIndexCached(wk.gk);
      if (h) { const i = h.sessions.findIndex((x) => x.id === cfg.id); return h.sessions[(i + 1) % h.sessions.length].id; }
      return cfg.id;
    }
    const i = units.findIndex((b) => b.id === cfg.id);
    return units[(i + 1) % units.length].id;
  };
  useKeys({
    l: () => { setUnitsOpen(false); setList((v) => !v); poke(); },
    u: () => { setList(false); setUnitsOpen((v) => !v); poke(); },
    b: () => { pickId(nextId()); poke(); },
    s: () => { pickSp(cfg.sp === 1 ? 1.5 : 1); poke(); },
    Escape: () => { setList(false); setUnitsOpen(false); setDocs(false); },
  }, inert || docs);
  const { Btn, Ic } = ui;
  const btnLabel = meta ? (wk ? `${meta.week}주${meta.slot} ${meta.title}` : meta.short) : "";
  const unitBtn = meta && (
    <button type="button" className={"dsp-chip bs-unit" + (unitsOpen ? " on" : "")} title="단원 · 회차 고르기 (U)" aria-pressed={unitsOpen}
      onClick={() => { setList(false); setUnitsOpen((v) => !v); poke(); }}>
      <span aria-hidden="true">{meta.icon}</span> {btnLabel} <small>{meta.span}</small>
    </button>
  );
  const unitPanel = unitsOpen && <PickPanel L={L} units={units} grades={grades} cur={cfg.id} onPick={(v) => { pickId(v); setUnitsOpen(false); poke(); }} onClose={() => setUnitsOpen(false)} />;
  if (err || !scenes) {
    const t = meta ? meta.title : wk ? `${gradeOf(wk.gk).grade} ${wk.week}주 ${wk.slot}` : "";
    return (
      <>
        <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label={t}>
          <text x={W / 2} y={H / 2} textAnchor="middle" fontSize="40" fontWeight="700" fill={C.soft}>{err ? `해설을 불러오지 못했어요 — ${err}` : `「${t}」 불러오는 중…`}</text>
        </svg>
        <div className="dsp-ctl show"><Btn title="나가기" onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn></div>
      </>
    );
  }
  const extra = (
    <>
      <span className="dsp-sep" />
      {unitBtn}
      <Seg label="빠르기" value={cfg.sp} options={[[1, "1×"], [1.5, "1.5×"]]} onChange={pickSp} poke={poke} />
      <Btn title="번호 · 단계 목록 (L)" on={list} onClick={() => { setUnitsOpen(false); setList((v) => !v); poke(); }}>
        <Ic d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" />
      </Btn>
      <span className="dsp-sep" />
    </>
  );
  const goTo = (i) => { api.current?.goTo(i); setList(false); poke(); };
  const label = wk ? `${meta.grade} ${meta.week}주 ${meta.slot} · ${meta.title}${cfg.st ? ` · ${cfg.st}단계` : ""}` : `${L.title} · ${meta.title}${cfg.st ? ` · ${cfg.st}단계` : ""}`;
  const top = <DocsMenu meta={meta} set={set} open={docs} onOpen={(v) => { setDocs(v); poke(); }} poke={poke} />;
  return (
    <>
      <style>{BS_CSS}</style>
      <StoryPlayer key={`${cfg.id}|${cfg.sp}|${cfg.st}`} list={scenes} lsKey={`${LSK}.${cfg.id}.${cfg.st}`} label={label}
        {...props} inert={inert || list || docs || unitsOpen} noMode extra={extra} topExtra={top} apiRef={api} onIdx={setCur} scrub />
      {list && <NumList meta={meta} scenes={scenes} cfg={cfg} cur={cur} onPick={goTo} onStage={(v) => { pickSt(v); poke(); }} onClose={() => setList(false)} />}
      {unitPanel}
    </>
  );
}

/** 고르기 — 「주차별 기초 다지기」(학년 → 학기 · 방학 → 주) | 「단원 100제」 */
function PickPanel({ L, units, grades, cur, onPick, onClose }) {
  const cw = parseWeekId(cur);
  const [tab, setTab] = useState(cw ? "week" : "unit");
  const [gk, setGk] = useState(() => cw?.gk || grades[0].gk);
  const [h, setH] = useState(() => weekIndexCached(gk));
  const [err, setErr] = useState(null);
  useEffect(() => {
    let live = true;
    setH(weekIndexCached(gk));
    setErr(null);
    loadWeekIndex(gk).then((v) => { if (live) setH(v); }).catch(() => { if (live) setErr("회차 목록을 불러오지 못했어요"); });
    return () => { live = false; };
  }, [gk]);
  const now = weekOfDate();
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="단원 · 회차 고르기">
        <div className="dsp-list-h">
          <b>{L.title}</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="dsp-chips">
          <button type="button" className={"dsp-chip" + (tab === "week" ? " on" : "")} onClick={() => setTab("week")}>🗓 주차별 기초 다지기</button>
          <button type="button" className={"dsp-chip" + (tab === "unit" ? " on" : "")} onClick={() => setTab("unit")}>📚 단원 100제 {units.length}</button>
        </div>
        {tab === "unit" ? (
          <>
            <p className="dsp-gal-sub">학년에 묶지 않고 이어지는 단원끼리 100문항씩 — 고르면 그 단원 1번부터 돌아요 · B 다음 단원</p>
            <div className="bs-grid">
              {units.map((b) => (
                <button key={b.id} type="button" className={"bs-card" + (b.id === cur ? " on" : "")} onClick={() => onPick(b.id)}>
                  <span className="i" aria-hidden="true">{b.icon}</span>
                  <span className="t">{b.short}<small>{b.span}</small></span>
                  <span className="u">{unitLabel(b.unit)}</span>
                </button>
              ))}
            </div>
          </>
        ) : (
          <>
            <div className="dsp-chips">
              {grades.map((g) => (
                <button key={g.gk} type="button" className={"dsp-chip" + (g.gk === gk ? " on" : "")} onClick={() => setGk(g.gk)}>{g.grade}</button>
              ))}
            </div>
            <p className="dsp-gal-sub">주 2회 × 52주 = 104회차 · 회차마다 20문항 · 지금은 {now.week}주({weekLabel(now.year, now.week)}) · B 다음 회차</p>
            {err && <p className="dsp-gal-sub">{err}</p>}
            {h && PERIODS.map((p) => (
              <div key={p.key} className="bs-per">
                <b className="bs-per-h">{p.key} <small>{p.from} ~ {p.to}주</small></b>
                <div className="bs-weeks">
                  {h.sessions.filter((m) => m.week >= p.from && m.week <= p.to).map((m) => (
                    <button key={m.id} type="button" className={"bs-wk" + (m.id === cur ? " on" : "") + (m.week === now.week ? " now" : "")} onClick={() => onPick(m.id)}>
                      <span className="w">{m.week}{m.slot}</span>
                      <span className="k" aria-hidden="true">{KIND_ICON[m.kind]}</span>
                      <span className="t">{m.title}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}

/** 번호 · 단계 목록 — 단계 칩을 고르면 그 단계만 돌고, 번호를 고르면 그 문항부터 */
function NumList({ meta, scenes, cfg, cur, onPick, onStage, onClose }) {
  const lap = scenes.reduce((s, x) => s + x.dur, 0);
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호 · 단계 목록">
        <div className="dsp-list-h">
          <b>{meta.title} <small style={{ opacity: 0.7 }}>{meta.span}</small></b>
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
        <div className="dsp-grid bs-nums">
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

const BS_CSS = `.bs-nums { grid-template-columns: repeat(5, 1fr); }
.dsp-chip.bs-unit { display: inline-flex; align-items: center; gap: 6px; max-width: 26cqw; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.dsp-chip.bs-unit small { opacity: .65; font-weight: 600; }
.bs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 15.5em), 1fr)); gap: 8px; }
.bs-card { display: grid; grid-template-columns: 2.1em 1fr; grid-template-rows: auto auto; column-gap: 8px; align-items: center; text-align: left;
  padding: 9px 11px; border-radius: 12px; border: 1px solid var(--chipbd); background: var(--chip); color: inherit; font: inherit; cursor: pointer; }
.bs-card .i { grid-row: 1 / span 2; font-size: 1.45em; text-align: center; }
.bs-card .t { font-weight: 800; font-size: .95em; display: flex; gap: 6px; align-items: baseline; flex-wrap: wrap; }
.bs-card .t small { font-weight: 700; font-size: .78em; opacity: .6; }
.bs-card .u { font-size: .76em; opacity: .66; }
.bs-card.on { outline: 2.5px solid var(--accent, #f4c65a); }
.bs-per { margin-top: 10px; }
.bs-per-h { display: block; margin: 4px 2px 6px; font-size: .92em; }
.bs-per-h small { font-weight: 600; opacity: .6; margin-left: 6px; }
.bs-weeks { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 13.5em), 1fr)); gap: 6px; }
.bs-wk { display: grid; grid-template-columns: 2.6em 1.4em 1fr; align-items: center; gap: 4px; text-align: left; padding: 7px 9px; border-radius: 10px;
  border: 1px solid var(--chipbd); background: var(--chip); color: inherit; font: inherit; font-size: .86em; cursor: pointer; min-width: 0; }
.bs-wk .w { font-weight: 800; opacity: .75; }
.bs-wk .t { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.bs-wk.now { box-shadow: inset 0 0 0 2px var(--accent, #f4c65a); }
.bs-wk.on { outline: 2.5px solid var(--accent, #f4c65a); }
`;

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
