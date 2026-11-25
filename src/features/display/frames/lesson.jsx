// ashrain.out — 해설 액자 공통 틀 (frames/lesson.jsx) — 문제 풀이 해설 액자가 모두 이 틀로 돈다
//   일차함수 그래프 그리기(graphdraw) · 10단계 계산(lin10) · 그래프와 넓이(area) · 경우의 수와 확률 100제(cnt100) · 기본기 해설 초등 · 중등 · 고등(basics — 세트 = 단원, 목록으로 고름)
// 어느 액자든 조작이 같다 — 단일 모드든 듀얼 모드든:
//   「보기 단일 | 듀얼」(D) · 「세트」(B — 세트가 둘 이상일 때) · 「빠르기 0.75× · 1× · 1.5× · 2×」(S) · 번호 · 단계 목록(L — 단계 칩을 고르면 그 단계만)
//   · 이전 · 멈춤 · 다음(←/→ · 스페이스) · 이 문항 반복(R) · 밝기 · 전체 화면(F) · 액자 목록 · 나가기
//   · 두 막대(frames/scrub.jsx — 아래 긴 막대 = 문항 이동, 옆 짧은 막대 = 풀이 이동) · 오른쪽 위 더할 것(기본기 해설의 📄 문서).
//   듀얼 모드는 화면을 좌우 둘로 나눠 두 판을 따로 돌린다 — 판마다 세트(같은 세트 둘도 됨) · 단계 · 번호 · 빠르기 · 멈춤 · 반복 · 두 막대.
//   판마다 고를 수 있는 것은 이 액자의 세트가 아니라 문제 풀이 해설 전부 — 단원 100제 · 유형 · 주차별 회차 · 해설 액자 세트
//   (frames/allspec.jsx 가 setDualAll 로 넣어 둔 「전부」 spec — 액자마다 따로 기억, 처음엔 단일 모드에서 보던 것).
//   가운데 ⇄(X)는 두 판의 자리를 맞바꾼다. 판마다 자리 · 고른 것은 기기에 기억한다(벽시계라 새로고침해도 이어 돈다).
// 액자마다 다른 것은 spec 하나로 넘긴다:
//   { lsk 기억 이름, title 액자 이름, sets [{ key, name, short, icon?, note?, sub? }], stages(set) → [{ v, lab, chip? }], scenes(set, sp, st) → 장면 목록,
//     posKey(lsk, set, st) 단일 모드 자리 기억 이름, cols 목록 칸 수, topExtra({ set, open, onOpen, poke }) 오른쪽 위,
//     setMenu { word, title, hint } — 세트가 많으면(기본기 해설의 단원) 「세트」 칸 대신 단추 → 목록(U),
//     ready(set) · load(set) → Promise — 세트 문항을 고를 때 들여오면(기본기 해설) 들여오는 동안 「불러오는 중」,
//     세트가 아주 많거나 늦게 알게 되면(「전부」 spec) sets 대신 hasSet(key) · setOf(key) · defSet · single0() · Menu(목록 화면) ·
//     titleOf(set) · colsOf(set) — 세트마다 액자 이름 · 목록 칸 수가 다를 때 }
//   pick — 처음 열 때 이 세트로(학생앱에서 고른 단원 — 단일 모드로 연다). pickNo — pick 과 함께, 그 세트의 이 번호부터(단계는 전체로).
//   ownDual — 듀얼 판도 이 액자의 세트에서만 고른다(「전부」 spec 을 쓰지 않는다 — 컨셉 문제 해설 영상).
//   menuExtra({ close }) — 세트 목록 머리에 더 놓을 것(기본기 해설: 「단원 100제 | 유형 | 주차별 학년」 바꾸기) · 세트에 grp 가 있으면 목록을 그 이름으로 나눈다.
//   onSeen(set, no) — 단일 모드에서 장면이 바뀔 때마다(학생앱이 본 기록을 남긴다).
//   장면 = StoryPlayer 형식(key · no · st · dur · grp · marks · title · sub · render) + pane(t, C, uid) 반쪽 판 그리기 · card 목록 칸 글자 · head 판 머리 글자
//     · cardTag { s, bg }(목록 칸 둘째 줄 앞 색 딱지) · cardMeta(둘째 줄 글자 — 초 앞).
//   단계 { v, lab, chip?, short? } — chip 단일 목록 칩 글자 · short 듀얼 판 목록 칩 글자(없으면 「n단계」).
import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { W, H, SANS, mathWidth } from "../draw.jsx";
import { PANE_W, PANE_H } from "../board.js";
import { StoryPlayer } from "./player.jsx";
import { Scrub } from "./scrub.jsx";
import { Seg, Setting, useKeys, lsRead, lsWrite } from "./xkit.jsx";

export const LESSON_SPEEDS = [0.75, 1, 1.5, 2];
export const DUAL_SPEEDS = LESSON_SPEEDS;
const SIDES = ["L", "R"];
const fixSp = (v) => (LESSON_SPEEDS.includes(v) ? v : 1);
const nextSp = (v) => LESSON_SPEEDS[(LESSON_SPEEDS.indexOf(fixSp(v)) + 1) % LESSON_SPEEDS.length];
const spLab = (v) => `${v}×`;
const LIST_IC = "M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01";

/** spec 다듬기 — 고를 수 있는 값으로만 */
function fixers(spec) {
  const keys = spec.sets ? spec.sets.map((s) => s.key) : [];
  const has = spec.hasSet || ((v) => keys.includes(v));
  const fixSet = (v) => (v != null && has(v) ? v : spec.defSet ?? keys[0]);
  const fixSt = (set, v) => { const st = spec.stages(set); return Number.isInteger(v) && (v === 0 || st.some((x) => x.v === v)) ? v : 0; };
  return { keys, fixSet, fixSt };
}
/** 세트 하나의 이름표 { key, name, short, icon?, note?, sub? } */
export const setOfSpec = (spec, k) => (spec.setOf ? spec.setOf(k) : spec.sets.find((x) => x.key === k)) || null;
const posKeyOf = (spec, set, st) => (spec.posKey ? spec.posKey(spec.lsk, set, st) : `${spec.lsk}.${set}.${st}`);
/** 단일 모드에서 보던 세트 */
const single0Of = (spec, F) => (spec.single0 ? F.fixSet(spec.single0()) : F.fixSet((lsRead(spec.lsk) || {}).set ?? (lsRead(spec.lsk) || {}).id));

/** 듀얼 모드 판마다 고를 「전부」 spec — frames/allspec.jsx 가 넣는다(이 파일이 액자 모듈을 들이면 서로 물리므로 거꾸로) */
let DUAL_ALL = null;
export function setDualAll(fn) { DUAL_ALL = fn; }
const dualSpecOf = (spec) => (DUAL_ALL && !spec.all && !spec.ownDual ? DUAL_ALL(spec) || spec : spec);

/** 목록을 열 때 지금 것(sel)이 가운데 오게 — 목록 상자 안에서만 굴린다(무대 · 바깥 화면은 그대로). 머리(.lsn-head)는 위에 붙어 있으므로 그 아래 가운데 */
function centerIn(box, sel) {
  const on = box?.querySelector?.(sel);
  if (!on || !box.getBoundingClientRect) return;
  const b = box.getBoundingClientRect(), r = on.getBoundingClientRect();
  const hd = box.querySelector(".lsn-head")?.getBoundingClientRect?.().height || 0;
  box.scrollTop += r.top - b.top - hd - (b.height - hd - r.height) / 2;
}

/** 해설 액자 — 단일 | 듀얼. pick(세트 key)을 주면 그 세트로 단일 모드부터(pickNo — 그 번호부터) */
export function LessonFrame({ spec, pick = null, pickNo = null, menuExtra = null, onSeen = null, ...props }) {
  const pk = useRef(pick != null && spec.sets.some((s) => s.key === pick) ? pick : null);
  const pn = useRef(pk.current != null && Number.isInteger(pickNo) ? pickNo : null);
  const [dual, setDual] = useState(() => !pk.current && (lsRead(spec.lsk + ".mode") || "") === "dual");
  useEffect(() => { lsWrite(spec.lsk + ".mode", dual ? "dual" : "single"); }, [dual, spec.lsk]);
  const pick0 = pk.current, pickNo0 = pn.current;
  useEffect(() => { pk.current = null; pn.current = null; }, []);   // 처음 한 번만 — 듀얼로 갔다 오면 기억한 자리로
  const dspec = useMemo(() => dualSpecOf(spec), [spec]);
  return dual
    ? <DualStage spec={dspec} menuExtra={dspec === spec ? menuExtra : null} {...props} onSingle={() => setDual(false)} />
    : <SingleStage spec={spec} pick={pick0} pickNo={pickNo0} menuExtra={menuExtra} onSeen={onSeen} {...props} onDual={() => setDual(true)} />;
}

/** 세트 문항이 아직 없으면 들여온다 — [다 왔나, 오류] */
function useSetsReady(spec, keys) {
  const need = spec.ready ? keys.filter((k) => !spec.ready(k)) : [];
  const [, bump] = useState(0);
  const [err, setErr] = useState(null);
  const sig = need.join("|");
  useEffect(() => {
    if (!sig) return undefined;
    let live = true;
    Promise.all(sig.split("|").map((k) => spec.load(k))).then(() => { if (live) bump((x) => x + 1); })
      .catch((e) => { if (live) setErr(e?.message || "불러오지 못했어요"); });
    return () => { live = false; };
  }, [sig, spec]);
  return [!need.length, err];
}
/** 들여오는 동안의 무대 */
export function Loading({ C, ui, onExit, title, err }) {
  const { Btn, Ic } = ui;
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label={title}>
        <text x={W / 2} y={H / 2} textAnchor="middle" fontSize="40" fontWeight="700" fill={C.soft}>{err ? `해설을 불러오지 못했어요 — ${err}` : `「${title}」 불러오는 중…`}</text>
      </svg>
      <div className="dsp-ctl show"><Btn title="나가기" onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn></div>
    </>
  );
}
/** 세트 고르는 단추 — 세트가 많으면(setMenu) 목록을 여는 칩, 아니면 칸 고르기 */
function SetPick({ spec, value, onChange, onMenu, menuOn, poke, label = "세트" }) {
  if (spec.setMenu) {
    const S = setOfSpec(spec, value) || setOfSpec(spec, spec.defSet) || { name: String(value) };
    return (
      <button type="button" className={"dsp-chip lsn-unit" + (menuOn ? " on" : "")} title={`${spec.setMenu.word} 목록 (U)`} aria-pressed={!!menuOn}
        onClick={() => { onMenu(); poke(); }}>
        {S.icon && <span aria-hidden="true">{S.icon}</span>} {S.short || S.name}{S.note && <small>{S.note}</small>}
      </button>
    );
  }
  if (spec.sets.length < 2) return null;
  return <Seg label={label} value={value} options={spec.sets.map((s) => [s.key, s.short || s.name])} onChange={onChange} poke={poke} />;
}
/** 세트(단원) 목록 — 고르면 그 세트 1번부터 */
export function SetMenu({ spec, cur, onPick, onClose, side = "", extra = null }) {
  const M = spec.setMenu;
  const box = useRef(null);
  useLayoutEffect(() => { centerIn(box.current, ".lsn-set.on"); }, []);
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" ref={box} onClick={(e) => e.stopPropagation()} role="dialog" aria-label={`${M.word} 목록`}>
        <div className="lsn-head">
          <div className="dsp-list-h">
            <b>{side ? `${side} 판 · ` : ""}{M.title}</b>
            <button type="button" onClick={onClose} aria-label="닫기">✕</button>
          </div>
          {extra && extra({ close: onClose })}
          {M.hint && <p className="dsp-gal-sub">{M.hint}</p>}
        </div>
        <div className="lsn-sets">
          {spec.sets.map((b, i) => [
            b.grp && b.grp !== spec.sets[i - 1]?.grp ? <div key={"g" + b.key} className="lsn-grp">{b.grp}</div> : null,
            <button key={b.key} type="button" className={"lsn-set" + (b.key === cur ? " on" : "") + (b.hot ? " hot" : "")} onClick={() => onPick(b.key)}>
              <span className="i" aria-hidden="true">{b.icon || "•"}</span>
              <span className="t">{b.short || b.name}{b.note && <small>{b.note}</small>}</span>
              <span className="u">{b.sub || b.name}</span>
            </button>,
          ])}
        </div>
      </div>
    </div>
  );
}

const ModeSeg = ({ dual, onChange, poke }) => (
  <Seg label="보기" value={dual ? "dual" : "single"} options={[["single", "단일"], ["dual", "듀얼"]]} onChange={onChange} poke={poke} />
);
const SpeedSeg = ({ value, onChange, poke, label = "빠르기" }) => (
  <Seg label={label} value={value} options={LESSON_SPEEDS.map((v) => [v, spLab(v)])} onChange={onChange} poke={poke} />
);

/* ══════════ 단일 모드 ══════════ */
function SingleStage({ menuExtra, onSeen, pickNo = null, ...props }) {
  const { spec, ui, poke, inert, onDual, pick, C, onExit } = props;
  const sa = useRef(pickNo);                                       // 처음 열 때 이 번호부터(한 번)
  const { Btn, Ic } = ui;
  const F = useMemo(() => fixers(spec), [spec]);
  const [cfg, setCfg] = useState(() => {
    const o = lsRead(spec.lsk) || {};
    const saved = o.set ?? o.id;
    const set = F.fixSet(pick ?? saved);
    return { set, sp: fixSp(o.sp), st: (pick != null && pick !== saved) || sa.current != null ? 0 : F.fixSt(set, o.st ?? o.lv) };
  });
  useEffect(() => { lsWrite(spec.lsk, cfg); }, [cfg, spec.lsk]);
  const [list, setList] = useState(false);
  const [menu, setMenu] = useState(false);
  const [docs, setDocs] = useState(false);
  const [cur, setCur] = useState(0);
  const api = useRef(null);
  const [ready, err] = useSetsReady(spec, [cfg.set]);
  const scenes = useMemo(() => (ready ? spec.scenes(cfg.set, cfg.sp, cfg.st) : null), [spec, cfg, ready]);
  const seenNo = scenes?.[cur]?.no;
  const j0 = scenes && sa.current != null ? scenes.findIndex((x) => x.no === sa.current) : -1;
  const startAt = j0 >= 0 ? j0 : null;
  useEffect(() => { if (scenes) sa.current = null; }, [scenes]);   // 재생기가 그 번호로 뜬 뒤에는 기억한 자리로
  useEffect(() => { if (onSeen && seenNo != null) onSeen(cfg.set, seenNo); }, [onSeen, cfg.set, seenNo]);
  const pickSet = useCallback((v) => setCfg((c) => { const set = F.fixSet(v); return set === c.set ? c : { ...c, set, st: F.fixSt(set, c.st) }; }), [F]);
  const pickSt = useCallback((v) => setCfg((c) => ({ ...c, st: F.fixSt(c.set, v) })), [F]);
  /** 빠르기 — 그림 속 같은 순간에서 이어지게 기억한 자리를 옮겨 둔다(재생기는 새 빠르기로 다시 뜬다) */
  const pickSp = useCallback((v) => setCfg((c) => {
    const sp = fixSp(v);
    if (sp === c.sp) return c;
    const k = posKeyOf(spec, c.set, c.st), o = lsRead(k), now = Date.now();
    if (o && Number.isInteger(o.i)) {
      const e = (Number.isFinite(o.held) && o.held >= 0 ? o.held : Math.max(0, now - o.t0)) * c.sp / sp;
      lsWrite(k, { ...o, t0: now - e, held: Number.isFinite(o.held) && o.held >= 0 ? e : null });
    }
    return { ...c, sp };
  }), [spec]);
  useKeys({
    l: () => { setMenu(false); setList((v) => !v); poke(); },
    u: () => { if (spec.setMenu) { setList(false); setMenu((v) => !v); poke(); } },
    b: () => { if (F.keys.length > 1) { pickSet(F.keys[(F.keys.indexOf(cfg.set) + 1) % F.keys.length]); poke(); } },
    s: () => { pickSp(nextSp(cfg.sp)); poke(); },
    d: () => { onDual(); poke(); },
    Escape: () => { setList(false); setMenu(false); setDocs(false); },
  }, inert || docs);
  const meta = setOfSpec(spec, cfg.set);
  if (!scenes) return <Loading C={C} ui={ui} onExit={onExit} title={meta.name} err={err} />;
  const extra = (
    <>
      <Btn title="번호 · 단계 목록 (L)" on={list} onClick={() => { setMenu(false); setList((v) => !v); poke(); }}><Ic d={LIST_IC} /></Btn>
      <span className="dsp-sep" />
    </>
  );
  // 둘째 줄 — 보기 · 세트 · 빠르기(듀얼 모드 판 조작과 같은 이름 · 같은 값)
  const row = (
    <>
      <Setting label="보기"><ModeSeg dual={false} onChange={(v) => { if (v === "dual") onDual(); }} poke={poke} /></Setting>
      {(spec.setMenu || spec.sets.length > 1) && <Setting label={spec.setMenu ? spec.setMenu.word : "세트"} sep>
        <SetPick spec={spec} value={cfg.set} onChange={pickSet} menuOn={menu} onMenu={() => { setList(false); setMenu((v) => !v); }} poke={poke} />
      </Setting>}
      <Setting label="빠르기" sep><SpeedSeg value={cfg.sp} onChange={pickSp} poke={poke} /></Setting>
    </>
  );
  const goTo = (i) => { api.current?.goTo(i); setList(false); poke(); };
  const stLab = cfg.st ? spec.stages(cfg.set).find((x) => x.v === cfg.st)?.lab : null;
  const label = `${spec.title} · ${meta.name}${stLab ? ` · ${stLab}` : ""}`;
  const top = spec.topExtra ? spec.topExtra({ set: cfg.set, open: docs, onOpen: (v) => { setDocs(v); poke(); }, poke }) : null;
  return (
    <>
      <style>{SET_CSS}</style>
      <StoryPlayer key={`${cfg.set}|${cfg.sp}|${cfg.st}`} list={scenes} lsKey={posKeyOf(spec, cfg.set, cfg.st)} label={label}
        {...props} inert={inert || list || docs || menu} noMode extra={extra} extraRow={row} topExtra={top} apiRef={api} onIdx={setCur} scrub startAt={startAt} />
      {list && <NumList spec={spec} set={cfg.set} st={cfg.st} scenes={scenes} cur={cur} onPick={goTo}
        onStage={(v) => { pickSt(v); poke(); }} onClose={() => setList(false)} />}
      {menu && <SetMenu spec={spec} cur={cfg.set} extra={menuExtra} onPick={(v) => { pickSet(v); setMenu(false); poke(); }} onClose={() => setMenu(false)} />}
    </>
  );
}

/* ══════════ 듀얼 모드 — 좌우 두 판을 따로 ══════════ */
/** 판 하나의 처음 상태 — 저장한 것이 있으면 그것(비운 동안 돈 만큼 앞으로), 없으면 기본(왼쪽 앞에서 빠르게 · 오른쪽 가운데부터 느리게) */
export function paneLoad(spec, o, side, setDefault, now = Date.now()) {
  const F = fixers(spec);
  const set = F.fixSet(o?.set || setDefault), st = F.fixSt(set, o?.st), sp = fixSp(o?.sp ?? (side === "L" ? 1.5 : 0.75));
  const list = spec.scenes(set, sp, st);
  const n = list.length;
  let i = Number.isInteger(o?.i) && o.i >= 0 && o.i < n ? o.i : side === "L" ? 0 : Math.floor(n / 2);
  const rep = o?.rep === true;
  if (o && Number.isFinite(o.held) && o.held >= 0) return { set, st, sp, i, t0: now - o.held, held: Math.min(o.held, list[i].dur), rep };
  if (!o || !Number.isFinite(o.t0) || o.t0 > now) return { set, st, sp, i, t0: now, held: null, rep };
  let e = now - o.t0;
  if (rep) e %= list[i].dur;
  else {
    e %= list.reduce((a, x) => a + x.dur, 0);
    while (e >= list[i].dur) { e -= list[i].dur; i = (i + 1) % n; }
  }
  return { set, st, sp, i, t0: now - e, held: null, rep };
}
const elapsed = (p, now) => (p.held != null ? p.held : now - p.t0);

function DualStage(props) {
  const { spec } = props;
  const need = useMemo(() => {
    const F = fixers(spec), o = lsRead(spec.lsk + ".dual") || {}, s0 = single0Of(spec, F);
    return [...new Set([F.fixSet(o.L?.set || s0), F.fixSet(o.R?.set || s0)])];
  }, [spec]);
  const [ready, err] = useSetsReady(spec, need);
  if (!ready) return <Loading C={props.C} ui={props.ui} onExit={props.onExit} title={spec.title} err={err} />;
  return <DualInner {...props} />;
}

function DualInner(props) {
  const { spec, ui, C, ctl, poke, inert, isFs, toggleFs, onTheme, onGallery, onExit, onSingle, menuExtra } = props;
  const { Btn, Ic, FrameIc } = ui;
  const F = useMemo(() => fixers(spec), [spec]);
  const DLSK = spec.lsk + ".dual";
  const panes = useRef(null);
  if (!panes.current) {
    const o = lsRead(DLSK) || {};
    const single0 = single0Of(spec, F);
    panes.current = { L: paneLoad(spec, o.L, "L", single0), R: paneLoad(spec, o.R, "R", single0) };
  }
  const [, setFrame] = useState(0);
  const [list, setList] = useState(null);           // "L" | "R" | null
  const [menu, setMenu] = useState(null);           // 세트(단원) 목록을 연 판 "L" | "R" | null
  const [docs, setDocs] = useState(null);           // 문서를 펼친 세트 | null
  const sc = (p) => spec.scenes(p.set, p.sp, p.st);
  const save = useCallback(() => lsWrite(DLSK, panes.current), [DLSK]);
  const redraw = useCallback(() => setFrame((f) => (f + 1) % 1e9), []);
  const upd = useCallback((side, fn) => { panes.current[side] = fn(panes.current[side]); save(); redraw(); }, [save, redraw]);

  /** 판 하나 조작 */
  const goTo = useCallback((side, i) => upd(side, (p) => {
    const n = spec.scenes(p.set, p.sp, p.st).length;
    return { ...p, i: ((i % n) + n) % n, t0: Date.now(), held: p.held != null ? 0 : null };
  }), [upd, spec]);
  const togglePause = useCallback((side) => upd(side, (p) => {
    const now = Date.now();
    return p.held != null ? { ...p, t0: now - p.held, held: null } : { ...p, held: now - p.t0 };
  }), [upd]);
  const setSet = useCallback((side, v) => {
    const set = F.fixSet(v);
    const apply = () => upd(side, (p) => (p.set === set ? p : { ...p, set, st: F.fixSt(set, p.st), i: 0, t0: Date.now(), held: p.held != null ? 0 : null }));
    if (spec.ready && !spec.ready(set)) spec.load(set).then(apply).catch(() => {});        // 단원 문항을 들여온 뒤에
    else apply();
  }, [upd, F, spec]);
  const setStage = useCallback((side, st) => upd(side, (p) => ({ ...p, st: F.fixSt(p.set, st), i: 0, t0: Date.now(), held: p.held != null ? 0 : null })), [upd, F]);
  /** 가운데 단추 — 두 판의 자리를 맞바꾼다(세트 · 번호 · 빠르기 · 시계 모두 그대로 옮겨 간다) */
  const swap = useCallback(() => {
    const { L, R } = panes.current;
    panes.current = { L: R, R: L };
    save(); redraw();
  }, [save, redraw]);
  const seek = useCallback((side, tt) => upd(side, (p) => {           // 풀이 이동 — 멈춰 있으면 멈춘 채
    const now = Date.now();
    return { ...p, t0: now - tt, held: p.held != null ? tt : null };
  }), [upd]);
  const setSpeed = useCallback((side, v) => upd(side, (p) => {
    const sp = fixSp(v);
    if (p.sp === sp) return p;
    const now = Date.now(), e = elapsed(p, now) * p.sp / sp;     // 그림 속 같은 순간에서 이어서
    return { ...p, sp, t0: now - e, held: p.held != null ? e : null };
  }), [upd]);

  /* 그리기 루프 — 두 판의 시계를 함께 */
  useEffect(() => {
    let raf = 0, last = 0;
    const loop = (now) => {
      raf = requestAnimationFrame(loop);
      if (now - last < 1000 / 30) return;
      last = now;
      const wall = Date.now();
      let moved = false;
      for (const side of SIDES) {
        const p = panes.current[side];
        const L = spec.scenes(p.set, p.sp, p.st);
        if (p.held == null && wall - p.t0 >= L[p.i].dur) {
          panes.current[side] = { ...p, i: p.rep ? p.i : (p.i + 1) % L.length, t0: p.t0 + L[p.i].dur };
          moved = true;
        }
      }
      if (moved) save();
      if (panes.current.L.held == null || panes.current.R.held == null || moved) setFrame((f) => (f + 1) % 1e9);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [save, spec]);

  useKeys({
    d: () => { onSingle(); poke(); },
    " ": () => { const both = panes.current.L.held == null || panes.current.R.held == null;
      for (const s of SIDES) if ((panes.current[s].held == null) === both) togglePause(s); poke(); },
    f: () => toggleFs(),
    x: () => { swap(); poke(); },
    Escape: () => { setList(null); setMenu(null); setDocs(null); },
  }, inert || !!list || !!docs || !!menu);

  const now = Date.now();
  const stop = (e) => e.stopPropagation();
  const view = SIDES.map((side, k) => {
    const p = panes.current[side], S = setOfSpec(spec, p.set) || { key: p.set, name: String(p.set) }, L = sc(p), s = L[p.i];
    const e = Math.min(elapsed(p, now), s.dur);
    return { side, k, p, S, L, s, e };
  });
  const sets = [...new Set(view.map((v) => v.p.set))];
  return (
    <>
      <style>{DUAL_CSS + SET_CSS}</style>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img"
        aria-label={`${spec.title} — 듀얼: 왼쪽 ${view[0].S.name} ${view[0].s.no}번, 오른쪽 ${view[1].S.name} ${view[1].s.no}번`}>
        <line x1={W / 2} y1={36} x2={W / 2} y2={H - 36} stroke={C.soft} strokeWidth={2} opacity={0.35} />
        {view.map(({ side, k, p, S, s, e }) => (
          <svg key={side} x={k * (W / 2)} y={0} width={W / 2} height={H} viewBox={`0 0 ${PANE_W} ${PANE_H}`}>
            <text x={46} y={116} fontFamily={SANS} fontSize={30} fontWeight={800} fill={C.soft}>{paneHead(spec, S, s)}</text>
            <text x={PANE_W - 40} y={116} fontFamily={SANS} fontSize={28} fontWeight={800} fill={p.held != null ? C.gold : C.soft} textAnchor="end">
              {`${spLab(p.sp)}${p.rep ? " · 반복" : ""}${p.held != null ? " · 멈춤" : ""}`}
            </text>
            <g key={s.key}>{s.pane(e, C, `d${side}`)}</g>
          </svg>
        ))}
      </svg>

      {spec.topExtra && (
        <div className="dsp-tr">
          {sets.map((set) => <span key={set}>{spec.topExtra({ set, open: docs === set, onOpen: (v) => { setDocs(v ? set : null); poke(); }, poke })}</span>)}
        </div>
      )}

      <div className={"dsp-ctl" + (ctl ? " show" : "")} onPointerDown={stop}>
        <ModeSeg dual onChange={(v) => { if (v === "single") onSingle(); }} poke={poke} />
        <span className="dsp-sep" />
        <Btn title="밝기 바꾸기" onClick={onTheme}><Ic d="M12 3a9 9 0 1 0 0 18V3z" fill /></Btn>
        <Btn title={isFs ? "전체 화면 끝내기 (F)" : "전체 화면 (F)"} onClick={() => { toggleFs(); poke(); }}>
          {isFs ? <Ic d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /> : <Ic d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />}
        </Btn>
        {onGallery && <Btn title="액자 목록" onClick={() => { onGallery(); poke(); }}><FrameIc /></Btn>}
        <Btn title="나가기" onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn>
      </div>

      {view.map(({ side, k, p }) => (
        <div key={side} className={"lsn-pane-ctl " + side + (ctl ? " show" : "")} onPointerDown={stop}>
          <div className="row">
            <SetPick spec={spec} label={`${k ? "오른쪽" : "왼쪽"} 세트`} value={p.set} onChange={(v) => setSet(side, v)} poke={poke}
              menuOn={menu === side} onMenu={() => { setList(null); setMenu(menu === side ? null : side); }} />
            <Btn title="번호 · 단계 목록" on={list === side} onClick={() => { setMenu(null); setList(list === side ? null : side); poke(); }}><Ic d={LIST_IC} /></Btn>
          </div>
          <div className="row">
            <Btn title="이전 문항" onClick={() => { goTo(side, p.i - 1); poke(); }}><Ic d="M15 5 8 12l7 7M6 5v14" /></Btn>
            <Btn title={p.held != null ? "재생" : "멈춤"} onClick={() => { togglePause(side); poke(); }}>
              {p.held != null ? <Ic d="M8 5v14l11-7z" fill /> : <Ic d="M8 5v14M16 5v14" />}
            </Btn>
            <Btn title="다음 문항" onClick={() => { goTo(side, p.i + 1); poke(); }}><Ic d="m9 5 7 7-7 7M18 5v14" /></Btn>
            <Btn title="이 문항 반복" on={p.rep} onClick={() => { upd(side, (q) => ({ ...q, rep: !q.rep })); poke(); }}>
              <Ic d="M17 2l3 3-3 3M4 11V9a4 4 0 0 1 4-4h12M7 22l-3-3 3-3M20 13v2a4 4 0 0 1-4 4H4" />
            </Btn>
            <span className="dsp-sep" />
            <SpeedSeg label={`${k ? "오른쪽" : "왼쪽"} 빠르기`} value={p.sp} onChange={(v) => setSpeed(side, v)} poke={poke} />
          </div>
        </div>
      ))}
      {view.map(({ side, e, s }) => (
        <div key={"pg" + side} className={"lsn-pane-prog " + side} aria-hidden="true"><i style={{ transform: `scaleX(${e / s.dur})` }} /></div>
      ))}
      <button type="button" className={"lsn-swap" + (ctl && !list && !menu ? " show" : "")} title="왼쪽 · 오른쪽 판 자리 바꾸기 (X)" aria-label="왼쪽 · 오른쪽 판 자리 바꾸기"
        onPointerDown={stop} onClick={() => { swap(); poke(); }}>
        <svg viewBox="0 0 24 24" width="55%" height="55%" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M7 4 3 8l4 4M3 8h14M17 12l4 4-4 4M21 16H7" />
        </svg>
      </button>
      {view.map(({ side, p, L, e, s }) => (
        <Scrub key={"sc" + side} variant={side} show={ctl && !list && !menu} scenes={L} idx={p.i} onPick={(i) => { goTo(side, i); poke(); }}
          t={e} dur={s.dur} marks={s.marks} onSeek={(tt) => { seek(side, tt); poke(); }} poke={poke} />
      ))}
      {menu && (() => {
        const M = spec.Menu || SetMenu;
        return (
          <div className={"lsn-pane-list " + menu}>
            <M spec={spec} cur={panes.current[menu].set} side={menu === "L" ? "왼쪽" : "오른쪽"} extra={menuExtra}
              onPick={(v) => { setSet(menu, v); setMenu(null); poke(); }} onClose={() => setMenu(null)} />
          </div>
        );
      })()}
      {list && (() => {
        const p = panes.current[list];
        return (
          <div className={"lsn-pane-list " + list}>
            <NumList spec={spec} set={p.set} st={p.st} scenes={sc(p)} cur={p.i} side={list === "L" ? "왼쪽" : "오른쪽"}
              onPick={(i) => { goTo(list, i); setList(null); poke(); }} onStage={(v) => { setStage(list, v); poke(); }} onClose={() => setList(null)} />
          </div>
        );
      })()}
    </>
  );
}

/** 판 머리 — 세트 짧은 이름 · 단계 · 번호(판 폭에 맞게 줄인다) */
export function paneHead(spec, S, s) {
  const nm = S.short || S.name, own = spec.paneHead ? spec.paneHead(S, s) : null;
  const cands = [...(own ? [own] : []), `${nm} · ${s.sub?.m || `${s.no}번`}`,
    `${nm} · ${s.grp ? `${s.grp} · ` : ""}${s.no}번`, `${s.grp ? `${s.grp} · ` : ""}${s.no}번`];
  return cands.find((c) => mathWidth(c, 30, 800) <= 540) || cands[cands.length - 1];
}

const SET_CSS = `
.dsp-chip.lsn-unit { display: inline-flex; align-items: center; gap: .45cqw; max-width: 26cqw; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;
  font-size: 1.15cqw; font-weight: 800; padding: .45cqw .9cqw; }
.dsp-chip.lsn-unit small { opacity: .65; font-weight: 600; font-size: .9cqw; margin-left: .2cqw; }
.lsn-pane-ctl .dsp-chip.lsn-unit { max-width: 22cqw; font-size: 1.05cqw; }
.lsn-sets { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 15.5em), 1fr)); gap: .6cqw; }
.lsn-set { display: grid; grid-template-columns: 2.1em 1fr; grid-template-rows: auto auto; column-gap: .6cqw; align-items: center; text-align: left;
  padding: .6cqw .8cqw; border-radius: .9cqw; border: 1px solid var(--chipbd); background: var(--chip); color: inherit; font: inherit; cursor: pointer; }
.lsn-set .i { grid-row: 1 / span 2; font-size: 1.45em; text-align: center; }
.lsn-set .t { font-weight: 800; font-size: .95em; display: flex; gap: .4cqw; align-items: baseline; flex-wrap: wrap; }
.lsn-set .t small { font-weight: 700; font-size: .78em; opacity: .6; }
.lsn-set .u { font-size: .76em; opacity: .66; }
.lsn-set.on { border-color: var(--gold); box-shadow: inset 0 0 0 1px var(--gold); }
.lsn-pane-list .lsn-sets { grid-template-columns: repeat(2, 1fr); }
.lsn-grp { grid-column: 1 / -1; font-weight: 800; font-size: .86em; opacity: .75; margin: .5cqw 0 -.1cqw; padding-left: .3cqw; }
.lsn-set.hot { border-color: var(--teal, #2a9d8f); }
/* 목록 머리(이름 · 단계 칩 · 안내)는 위에 붙어 있다 — 긴 목록을 굴려도(지금 것을 가운데로 열어도) 보인다. 상자 위 여백까지 덮는다 */
.dsp-list-in { --lsn-pad: 1.6cqw; }
.lsn-pane-list .dsp-list-in { --lsn-pad: 1.2cqw; }
.lsn-head { position: sticky; top: calc(-1 * var(--lsn-pad)); z-index: 2; background: var(--card); margin-top: calc(-1 * var(--lsn-pad));
  padding: var(--lsn-pad) 0 .2cqw; }
.lsn-tag { font-style: normal; color: #fff; font-weight: 800; border-radius: .4em; padding: 0 .45em; margin-right: .45em; line-height: 1.55; }
.lsn-set.hot .t::after { content: "이번 주"; font-size: .7em; font-weight: 800; color: var(--teal, #2a9d8f); margin-left: .3cqw; }
`;

export const DUAL_CSS = `
.lsn-pane-ctl { position: absolute; bottom: 4.4cqw; width: 48%; display: flex; flex-direction: column; align-items: center; gap: .5cqw;
  opacity: 0; pointer-events: none; transition: opacity .3s; z-index: 6; }
.lsn-pane-ctl.L { left: 1%; } .lsn-pane-ctl.R { right: 1%; }
.lsn-pane-ctl.show { opacity: 1; pointer-events: auto; }
.lsn-pane-ctl .row { display: flex; align-items: center; gap: .4cqw; padding: .35cqw .6cqw; border-radius: 999px;
  background: var(--chip); border: 1px solid var(--chipbd); max-width: 100%; flex-wrap: wrap; justify-content: center; }
.lsn-pane-ctl .dsp-btn { width: 3cqw; height: 3cqw; font-size: 1.45cqw; }
.lsn-pane-ctl .dsp-seg button { font-size: 1.05cqw; padding: .45cqw .85cqw; }
.lsn-swap { position: absolute; left: 50%; top: 50%; width: 4.4cqw; height: 4.4cqw; margin: -2.2cqw 0 0 -2.2cqw; z-index: 7;
  border-radius: 999px; border: 1px solid var(--chipbd); background: var(--chip); color: var(--ink); display: grid; place-items: center;
  cursor: pointer; opacity: 0; pointer-events: none; transition: opacity .3s, color .25s, border-color .25s; -webkit-tap-highlight-color: transparent; }
.lsn-swap.show { opacity: 1; pointer-events: auto; }
.lsn-swap:hover { color: var(--gold); border-color: var(--gold); }
.lsn-pane-prog { position: absolute; bottom: 0; height: .22cqw; width: 50%; opacity: .45; }
.lsn-pane-prog.L { left: 0; } .lsn-pane-prog.R { right: 0; }
.lsn-pane-prog i { display: block; height: 100%; background: var(--gold); transform-origin: 0 50%; }
.lsn-pane-list { position: absolute; top: 0; bottom: 0; width: 50%; z-index: 8; }
.lsn-pane-list.L { left: 0; } .lsn-pane-list.R { right: 0; }
.lsn-pane-list .dsp-list-in { width: 46.5cqw; max-height: 92%; padding: 1.2cqw 1.3cqw; }
.lsn-pane-list .dsp-list-h { font-size: 1.4cqw; }
.lsn-pane-list .lsn-grid { grid-template-columns: repeat(3, 1fr) !important; gap: .6cqw; }
.lsn-pane-list .dsp-card { padding: .7cqw .8cqw; column-gap: .6cqw; }
.lsn-pane-list .dsp-card .e, .lsn-pane-list .dsp-card .m { font-size: 1.02cqw; }
.lsn-pane-list .dsp-chip { font-size: 1.05cqw; padding: .4cqw .85cqw; }
.lsn-pane-list .dsp-gal-sub { font-size: .98cqw; }
`;

/** 번호 · 단계 목록 — 단계 칩을 고르면 그 단계만 돌고, 번호를 고르면 그 문항부터 */
export function NumList({ spec, set, st, scenes, cur, onPick, onStage, onClose, side = "" }) {
  const S = setOfSpec(spec, set) || { name: String(set) };
  const box = useRef(null);
  useLayoutEffect(() => { centerIn(box.current, ".dsp-card.on"); }, []);
  const stages = spec.stages(set);
  const title = spec.titleOf ? spec.titleOf(set) : spec.title, cols = (spec.colsOf ? spec.colsOf(set) : spec.cols) || 5;
  const lap = scenes.reduce((a, x) => a + x.dur, 0);
  const all = spec.scenes(set, 1, 0).length;
  const now = stages.find((x) => x.v === st);
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" ref={box} onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호 · 단계 목록">
        <style>{`.lsn-grid { grid-template-columns: repeat(${cols}, 1fr); }`}</style>
        <div className="lsn-head">
          <div className="dsp-list-h">
            <b>{side ? `${side} 판 · ` : ""}{title} · {S.name}</b>
            <button type="button" onClick={onClose} aria-label="닫기">✕</button>
          </div>
          {stages.length > 0 && (
            <div className="dsp-chips">
              {[{ v: 0 }, ...stages].map((x) => (
                <button key={x.v} type="button" className={"dsp-chip" + (st === x.v ? " on" : "")} aria-pressed={st === x.v} onClick={() => onStage(x.v)}>
                  {x.v === 0 ? `전체 ${all}` : side ? x.short || `${x.v}단계` : x.chip || x.lab}
                </button>
              ))}
            </div>
          )}
          <p className="dsp-gal-sub">
            {now ? `${now.lab} ${scenes.length}문항만 돌아요` : stages.length ? "첫 단계부터 차례로 돌아요" : "처음부터 차례로 돌아요"}
            {" "}· 한 바퀴 약 {Math.max(1, Math.round(lap / 60000))}분 · 지금 {scenes[cur]?.no}번 · 번호를 고르면 그 문항부터
          </p>
        </div>
        <div className="dsp-grid lsn-grid">
          {scenes.map((s, i) => (
            <button key={s.key} type="button" className={"dsp-card" + (i === cur ? " on" : "")} onClick={() => onPick(i)}>
              <span className="n">{s.no}</span>
              <span className="e">{s.card || s.grp || ""}</span>
              <span className="m">
                {s.cardTag && <i className="lsn-tag" style={{ background: s.cardTag.bg }}>{s.cardTag.s}</i>}
                {s.cardMeta ? `${s.cardMeta} · ` : ""}{Math.round(s.dur / 1000)}초
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
