// ashrain.out — 교실 모니터 「액자」: 경우의 수와 확률 100제 해설 (frames/cnt100.jsx)
// 학원 프린트 「학년별 선발」 · 「주머니 공 꺼내기」 · 「사전식 나열(영어 단어)」 · 「한 줄로 세우기(이웃 · 양 끝)」 100제(중2-2)를
//   문항마다 한 장면으로 끝없이 돌린다 — ① 문제 → ② 전략 → ③ 판서(포지티브 · 네거티브 → 식 한 줄씩) → ④ 답.
// 그리기 · 박자는 일차함수 10단계 액자(frames/lin10.jsx 의 L10Art · ../lin10.js 의 l10Plan)를 그대로 쓴다.
//   사전식은 「숫자 분석」 → 묶음 개수로 시작 글자 → 최종 묶음, 오른쪽에 세로 나무(frames/lextree.jsx — 칠판 판서 그대로).
//   단일 모드에서는 오른쪽에 그림이 판서 줄과 맞물려 움직인다(frames/c100fig.jsx — 줄 세우기 자리 칸 · 학년별 학생 · 주머니 공,
//   사전식 세로 나무). 글자가 그림 옆에 다 들어가지 않는 문항은 그림 없이 넓게.
// 이 액자만의 것: 「선발 | 공 꺼내기 | 사전식 | 줄 세우기」(B로 차례로) · 「1× | 1.5×」 · 번호 목록(L) — 목록 위 단계 칩(전체 · 1~5단계)으로 고르면 그 단계만 돈다.
//   「단일 | 듀얼」(D): 듀얼 모드는 화면을 좌우 둘로 나눠 두 판을 따로 돌린다 — 판마다 세트(같은 세트 둘도 됨) · 단계 · 번호 ·
//   빠르기(0.75× ~ 2×) · 멈춤 · 반복을 따로. 예: 왼쪽은 앞쪽 문항을 빠르게, 오른쪽은 뒤쪽 문항을 느리게 — 교실 앞에 두고 여러 학생을 함께 본다.
//   듀얼 판에는 그림 없이 판서만(반쪽이라 글자를 크게). 판마다 자리 · 고른 것은 기기에 기억한다(벽시계라 새로고침해도 이어 돈다).
//   가운데 단추(⇄ · 키보드 X): 두 판의 자리를 맞바꾼다 — 세트 · 번호 · 빠르기 · 시계가 그대로 옮겨 간다.
//   두 막대(frames/scrub.jsx): 아래 긴 막대 = 문항 이동(동그라미를 끌거나 누름), 옆 짧은 막대 = 풀이 이동(문제 · 방침 · 판서 줄 · 답).
//   단일 모드는 StoryPlayer 의 scrub, 듀얼 모드는 판마다(왼쪽 판은 왼쪽 가장자리, 오른쪽 판은 오른쪽 가장자리에 짧은 막대).
// 문항: ../cnt100-items.js
import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { l10Plan } from "../lin10.js";
import { W, H, SANS } from "../draw.jsx";
import { C100_SETS, C100_KEYS, C100_SPEEDS } from "../cnt100.js";
import { L10Art } from "./lin10.jsx";
import { StoryPlayer } from "./player.jsx";
import { Scrub, stepMarks } from "./scrub.jsx";
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
      key: `c100-${setKey}-${it.no}`, no: it.no, st: it.st, it, dur: Math.round(l10Plan(it).dur / sp),
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp, it.planTag || "방침"),
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
  const [dual, setDual] = useState(() => (lsRead(LSK + ".mode") || "") === "dual");
  useEffect(() => { lsWrite(LSK + ".mode", dual ? "dual" : "single"); }, [dual]);
  return dual ? <DualStage {...props} onSingle={() => setDual(false)} /> : <SingleStage {...props} onDual={() => setDual(true)} />;
}

const ModeSeg = ({ dual, onChange, poke }) => (
  <Seg label="보기" value={dual ? "dual" : "single"} options={[["single", "단일"], ["dual", "듀얼"]]} onChange={onChange} poke={poke} />
);

function SingleStage(props) {
  const { ui, poke, inert, onDual } = props;
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
    d: () => { onDual(); poke(); },
    Escape: () => setList(false),
  }, inert);
  const extra = (
    <>
      <span className="dsp-sep" />
      <ModeSeg dual={false} onChange={(v) => { if (v === "dual") onDual(); }} poke={poke} />
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
        {...props} inert={inert || list} noMode extra={extra} apiRef={api} onIdx={setCur} scrub />
      {list && <NumList scenes={scenes} cfg={cfg} cur={cur} onPick={pick} onStage={(v) => { pickSt(v); poke(); }} onClose={() => setList(false)} />}
    </>
  );
}

/* ══════════ 듀얼 모드 — 좌우 두 판을 따로 ══════════ */
export const DUAL_SPEEDS = [0.75, 1, 1.5, 2];
export const PANE = { W: 1000, H: 1125 };          // 반쪽(800 × 900) 자리에 그리는 판의 좌표 — 글자가 0.8 배로 보인다
export const PANE_BOX = { key: "pane", right: PANE.W - 50, top: 225, bottom: PANE.H - 40 };   // 위쪽은 판 이름 · 가운데 조작 막대 자리
const DLSK = LSK + ".dual";
const fixDsp = (v) => (DUAL_SPEEDS.includes(v) ? v : 1);
const SIDES = ["L", "R"];

/** 판 하나의 처음 상태 — 저장한 것이 있으면 그것(비운 동안 돈 만큼 앞으로), 없으면 기본(왼쪽 앞에서 빠르게 · 오른쪽 뒤에서 느리게) */
export function paneLoad(o, side, setDefault, now = Date.now()) {
  const set = fixSet(o?.set || setDefault), st = fixSt(o?.st), sp = fixDsp(o?.sp ?? (side === "L" ? 1.5 : 0.75));
  const list = c100Scenes(set, sp, st);
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
  const { ui, C, ctl, poke, inert, isFs, toggleFs, onTheme, onGallery, onExit, onSingle } = props;
  const { Btn, Ic, FrameIc } = ui;
  const single0 = fixSet((lsRead(LSK) || {}).set);
  const panes = useRef(null);
  if (!panes.current) {
    const o = lsRead(DLSK) || {};
    panes.current = { L: paneLoad(o.L, "L", single0), R: paneLoad(o.R, "R", single0) };
  }
  const [, setFrame] = useState(0);
  const [list, setList] = useState(null);           // "L" | "R" | null
  const save = useCallback(() => lsWrite(DLSK, panes.current), []);
  const redraw = useCallback(() => setFrame((f) => (f + 1) % 1e9), []);
  const upd = useCallback((side, fn) => { panes.current[side] = fn(panes.current[side]); save(); redraw(); }, [save, redraw]);

  /** 판 하나 조작 */
  const goTo = useCallback((side, i) => upd(side, (p) => {
    const n = c100Scenes(p.set, p.sp, p.st).length;
    return { ...p, i: ((i % n) + n) % n, t0: Date.now(), held: p.held != null ? 0 : null };
  }), [upd]);
  const togglePause = useCallback((side) => upd(side, (p) => {
    const now = Date.now();
    return p.held != null ? { ...p, t0: now - p.held, held: null } : { ...p, held: now - p.t0 };
  }), [upd]);
  const setSet = useCallback((side, set) => upd(side, (p) => (p.set === set ? p : { ...p, set, st: 0, i: 0, t0: Date.now(), held: p.held != null ? 0 : null })), [upd]);
  const setStage = useCallback((side, st) => upd(side, (p) => ({ ...p, st, i: 0, t0: Date.now(), held: p.held != null ? 0 : null })), [upd]);
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
  const setSpeed = useCallback((side, sp) => upd(side, (p) => {
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
        const L = c100Scenes(p.set, p.sp, p.st);
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
  }, [save]);

  useKeys({
    d: () => { onSingle(); poke(); },
    " ": () => { const both = panes.current.L.held == null || panes.current.R.held == null;
      for (const s of SIDES) if ((panes.current[s].held == null) === both) togglePause(s); poke(); },
    f: () => toggleFs(),
    x: () => { swap(); poke(); },
    Escape: () => setList(null),
  }, inert || !!list);

  const now = Date.now();
  const stop = (e) => e.stopPropagation();
  const view = SIDES.map((side, k) => {
    const p = panes.current[side], S = C100_SETS[p.set], L = c100Scenes(p.set, p.sp, p.st), sc = L[p.i];
    const e = Math.min(elapsed(p, now), sc.dur);
    return { side, k, p, S, L, sc, e };
  });
  return (
    <>
      <style>{DUAL_CSS}</style>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img"
        aria-label={`경우의 수와 확률 100제 해설 — 듀얼: 왼쪽 ${view[0].S.name} ${view[0].sc.no}번, 오른쪽 ${view[1].S.name} ${view[1].sc.no}번`}>
        <line x1={W / 2} y1={36} x2={W / 2} y2={H - 36} stroke={C.soft} strokeWidth={2} opacity={0.35} />
        {view.map(({ side, k, p, S, sc, e }) => (
          <svg key={side} x={k * (W / 2)} y={0} width={W / 2} height={H} viewBox={`0 0 ${PANE.W} ${PANE.H}`}>
            <text x={60} y={172} fontFamily={SANS} fontSize={30} fontWeight={800} fill={C.soft}>
              {`${S.short} · ${sc.st}단계 ${S.stage[sc.st]} · ${sc.no}번`}
            </text>
            <text x={PANE.W - 50} y={172} fontFamily={SANS} fontSize={28} fontWeight={800} fill={p.held != null ? C.gold : C.soft} textAnchor="end">
              {`${p.sp}×${p.rep ? " · 반복" : ""}${p.held != null ? " · 멈춤" : ""}`}
            </text>
            <g key={sc.key}>
              <L10ArtPane it={sc.it} t={e * p.sp} C={C} uid={`d${side}`} />
            </g>
          </svg>
        ))}
      </svg>

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

      {view.map(({ side, k, p, L, e, sc }) => (
        <div key={side} className={"c100-pane-ctl " + side + (ctl ? " show" : "")} onPointerDown={stop}>
          <div className="row">
            <Seg label={`${k ? "오른쪽" : "왼쪽"} 세트`} value={p.set} options={C100_KEYS.map((x) => [x, C100_SETS[x].short])} onChange={(v) => setSet(side, v)} poke={poke} />
            <Btn title="번호 · 단계 목록" on={list === side} onClick={() => { setList(list === side ? null : side); poke(); }}>
              <Ic d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" />
            </Btn>
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
            <Seg label={`${k ? "오른쪽" : "왼쪽"} 빠르기`} value={p.sp} options={DUAL_SPEEDS.map((v) => [v, `${v}×`])} onChange={(v) => setSpeed(side, v)} poke={poke} />
          </div>
        </div>
      ))}
      {view.map(({ side, e, sc }) => (
        <div key={"pg" + side} className={"c100-pane-prog " + side} aria-hidden="true"><i style={{ transform: `scaleX(${e / sc.dur})` }} /></div>
      ))}
      <button type="button" className={"c100-swap" + (ctl && !list ? " show" : "")} title="왼쪽 · 오른쪽 판 자리 바꾸기 (X)" aria-label="왼쪽 · 오른쪽 판 자리 바꾸기"
        onPointerDown={stop} onClick={() => { swap(); poke(); }}>
        <svg viewBox="0 0 24 24" width="55%" height="55%" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M7 4 3 8l4 4M3 8h14M17 12l4 4-4 4M21 16H7" />
        </svg>
      </button>
      {view.map(({ side, p, L, e, sc }) => (
        <Scrub key={"sc" + side} variant={side} show={ctl && !list} scenes={L} idx={p.i} onPick={(i) => { goTo(side, i); poke(); }}
          t={e} dur={sc.dur} marks={sc.marks} onSeek={(tt) => { seek(side, tt); poke(); }} poke={poke} />
      ))}
      {list && (() => {
        const p = panes.current[list];
        const scenes = c100Scenes(p.set, p.sp, p.st);
        return (
          <div className={"c100-pane-list " + list}>
            <NumList scenes={scenes} cfg={{ set: p.set, st: p.st }} cur={p.i} side={list === "L" ? "왼쪽" : "오른쪽"}
              onPick={(i) => { goTo(list, i); setList(null); poke(); }} onStage={(v) => { setStage(list, v); poke(); }} onClose={() => setList(null)} />
          </div>
        );
      })()}
    </>
  );
}

const L10ArtPane = ({ it, t, C, uid }) => <L10Art it={it} t={t} C={C} uid={uid} box={PANE_BOX} />;

export const DUAL_CSS = `
.c100-pane-ctl { position: absolute; bottom: 4.4cqw; width: 48%; display: flex; flex-direction: column; align-items: center; gap: .5cqw;
  opacity: 0; pointer-events: none; transition: opacity .3s; z-index: 6; }
.c100-pane-ctl.L { left: 1%; } .c100-pane-ctl.R { right: 1%; }
.c100-pane-ctl.show { opacity: 1; pointer-events: auto; }
.c100-pane-ctl .row { display: flex; align-items: center; gap: .4cqw; padding: .35cqw .6cqw; border-radius: 999px;
  background: var(--chip); border: 1px solid var(--chipbd); }
.c100-pane-ctl .dsp-btn { width: 3cqw; height: 3cqw; font-size: 1.45cqw; }
.c100-pane-ctl .dsp-seg button { font-size: 1.05cqw; padding: .45cqw .85cqw; }
.c100-swap { position: absolute; left: 50%; top: 50%; width: 4.4cqw; height: 4.4cqw; margin: -2.2cqw 0 0 -2.2cqw; z-index: 7;
  border-radius: 999px; border: 1px solid var(--chipbd); background: var(--chip); color: var(--ink); display: grid; place-items: center;
  cursor: pointer; opacity: 0; pointer-events: none; transition: opacity .3s, color .25s, border-color .25s; -webkit-tap-highlight-color: transparent; }
.c100-swap.show { opacity: 1; pointer-events: auto; }
.c100-swap:hover { color: var(--gold); border-color: var(--gold); }
.c100-pane-prog { position: absolute; bottom: 0; height: .22cqw; width: 50%; opacity: .45; }
.c100-pane-prog.L { left: 0; } .c100-pane-prog.R { right: 0; }
.c100-pane-prog i { display: block; height: 100%; background: var(--gold); transform-origin: 0 50%; }
.c100-pane-list { position: absolute; top: 0; bottom: 0; width: 50%; z-index: 8; }
.c100-pane-list.L { left: 0; } .c100-pane-list.R { right: 0; }
.c100-pane-list .dsp-list-in { width: 46.5cqw; max-height: 92%; padding: 1.2cqw 1.3cqw; }
.c100-pane-list .dsp-list-h { font-size: 1.4cqw; }
.c100-pane-list .c100-grid { grid-template-columns: repeat(3, 1fr) !important; gap: .6cqw; }
.c100-pane-list .dsp-card { padding: .7cqw .8cqw; column-gap: .6cqw; }
.c100-pane-list .dsp-card .e, .c100-pane-list .dsp-card .m { font-size: 1.02cqw; }
.c100-pane-list .dsp-chip { font-size: 1.05cqw; padding: .4cqw .85cqw; }
.c100-pane-list .dsp-gal-sub { font-size: .98cqw; }
`;

/** 번호 · 단계 목록 — 단계 칩을 고르면 그 단계만 돌고, 번호를 고르면 그 문항부터 */
export function NumList({ scenes, cfg, cur, onPick, onStage, onClose, side = "" }) {
  const S = C100_SETS[cfg.set];
  const lap = scenes.reduce((s, x) => s + x.dur, 0);
  const cnt = (v) => S.items.filter((it) => it.st === v).length;
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호 · 단계 목록">
        <style>{".c100-grid { grid-template-columns: repeat(5, 1fr); }"}</style>
        <div className="dsp-list-h">
          <b>{side ? `${side} 판 · ` : ""}경우의 수와 확률 100제 · {S.name}</b>
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
