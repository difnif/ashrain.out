// ashrain.out — 교실 모니터 「실험 액자」 공용 부품 (frames/xkit.jsx)
// 몬티홀 · 갈림길과 구슬 · 구슬 낙하 실험 액자가 함께 쓴다. 하노이의 탑 액자처럼 화면 전체가 실험이고,
//   조작 막대: 처음부터 · 재생/멈춤 · 밝기 · 전체 화면 · [해 보기 | 풀이 보기] · 수업 장면으로
//   그 아래 설정 줄: 액자마다 고르는 수(문 개수 · 단계 · 구슬 수 …)
// 오른쪽 위에는 수업 장면처럼 액자 단추와 학년 토글(초등 · 중등)을 둔다.
// 「풀이 보기」는 교실 모니터의 설명 장면을 그대로 돌린다(StoryPlayer) — 실험이 먼저, 풀이는 고를 때만.
// 시계는 벽시계(Date.now)라 새로고침하거나 잠깐 나갔다 와도 그 자리에서 이어진다. 고른 수와 시계는 기기에 기억한다.
// 단추 모양(Btn · Ic · FrameIc)은 교실 모니터 무대가 ui 로 넘겨준다.
import { useCallback, useEffect, useRef, useState } from "react";
import { E, clamp } from "../core.js";
import { StoryPlayer } from "./story.jsx";

export const FRAME_MS = 1000 / 40;
export const MODE_FADE = 1000;
export const lsRead = (k) => { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch { return null; } };
export const lsWrite = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* 사생활 모드 등 */ } };

/**
 * 벽시계 + 고른 수. fix(prm) 은 고를 수 있는 값으로 고친 prm 을 돌려준다.
 * setPrm(patch, keep) — keep(old, new, elapsed) 가 있으면 그 값으로 시계를 옮기고(빠르기 바꾸기 등), 없으면 처음부터.
 * jump(e) — 경과를 e 로(멈춰 있으면 멈춘 채). epoch — 처음부터 다시 틀 때마다 1씩 는다.
 */
export function useLabClock(key, defaults, fix) {
  const init = useRef(null);
  if (!init.current) {
    const o = lsRead(key), now = Date.now();
    const ok = o && typeof o === "object" && Number.isFinite(o.t0) && o.t0 <= now;
    init.current = ok
      ? { prm: fix({ ...defaults, ...(o.prm && typeof o.prm === "object" ? o.prm : {}) }), t0: o.t0, held: Number.isFinite(o.held) && o.held >= 0 ? o.held : null }
      : { prm: fix({ ...defaults }), t0: now, held: null };
  }
  const [prm, setPrmState] = useState(init.current.prm);
  const [paused, setPaused] = useState(init.current.held != null);
  const [epoch, setEpoch] = useState(0);
  const clk = useRef({ t0: init.current.t0, held: init.current.held });
  const P = useRef(prm);
  P.current = prm;
  const save = useCallback((p) => lsWrite(key, { prm: p, t0: clk.current.t0, held: clk.current.held }), [key]);
  useEffect(() => { save(P.current); }, [save]);

  const elapsed = useCallback(() => (clk.current.held != null ? clk.current.held : Date.now() - clk.current.t0), []);
  const togglePause = useCallback(() => {
    const now = Date.now(), c = clk.current;
    clk.current = c.held != null ? { t0: now - c.held, held: null } : { t0: c.t0, held: now - c.t0 };
    setPaused(clk.current.held != null);
    save(P.current);
  }, [save]);
  const jump = useCallback((e) => {
    const c = clk.current, e2 = Math.max(0, e);
    clk.current = c.held != null ? { t0: c.t0, held: e2 } : { t0: Date.now() - e2, held: null };
    save(P.current);
  }, [save]);
  const restart = useCallback(() => {
    clk.current = { t0: Date.now(), held: clk.current.held != null ? 0 : null };
    setEpoch((e) => e + 1);
    save(P.current);
  }, [save]);
  const setPrm = useCallback((patch, keep) => {
    const old = P.current, next = fix({ ...old, ...patch });
    if (Object.keys(next).every((k) => next[k] === old[k])) return;
    const now = Date.now(), c = clk.current;
    if (keep) {
      const e2 = Math.max(0, keep(old, next, c.held != null ? c.held : now - c.t0));
      clk.current = c.held != null ? { t0: c.t0, held: e2 } : { t0: now - e2, held: null };
    } else {
      clk.current = { t0: now, held: c.held != null ? 0 : null };
      setEpoch((e) => e + 1);
    }
    P.current = next;
    setPrmState(next);
    save(next);
  }, [fix, save]);
  return { prm, setPrm, paused, togglePause, restart, jump, elapsed, clk, epoch };
}

/** 40fps 로 다시 그린다. tick(now) 이 false 를 돌려주면 그 차례는 쉰다(멈춘 동안 등) */
export function useTicker(tick) {
  const [, setF] = useState(0);
  const T = useRef(tick);
  T.current = tick;
  useEffect(() => {
    let raf = 0, last = 0;
    const loop = (now) => {
      raf = requestAnimationFrame(loop);
      if (now - last < FRAME_MS) return;
      last = now;
      if (T.current(now) === false) return;
      setF((f) => (f + 1) % 1e9);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, []);
}

/** 키보드: keys = { 키: 할 일 } — 액자 목록이 열려 있으면(inert) 받지 않는다 */
export function useKeys(keys, inert) {
  const K = useRef(keys);
  K.current = keys;
  const I = useRef(inert);
  I.current = inert;
  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey || I.current) return;
      const f = K.current[e.key] || K.current[e.key.toLowerCase?.()];
      if (f) { if (e.key === " " || e.key.startsWith("Arrow") || e.key === "Tab") e.preventDefault(); f(); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);
}

/** 학년 토글이 바뀌면 MODE_FADE 동안 두 판을 겹쳐 그린다: [{ mode, o, top }] (top = 누를 수 있는 판) */
export function useModeLayers(mode) {
  const last = useRef(mode), mf = useRef(null);
  if (last.current !== mode) { mf.current = { from: last.current, t0: performance.now() }; last.current = mode; }
  const now = performance.now();
  if (mf.current && now - mf.current.t0 > MODE_FADE) mf.current = null;
  if (!mf.current) return [{ mode, o: 1, top: true }];
  const k = E.sine(clamp((now - mf.current.t0) / MODE_FADE));
  return [{ mode: mf.current.from, o: 1 - k * k, top: false }, { mode, o: k, top: true }];
}

/** − 값 + (옵션 배열 안에서 한 칸씩) */
export function Stepper({ ui, label, value, options, unit, onChange, poke, fmt, keyHint }) {
  const { Btn, Ic } = ui;
  const i = options.indexOf(value);
  const go = (d) => { const j = Math.max(0, Math.min(options.length - 1, i + d)); if (j !== i) onChange(options[j]); poke(); };
  return (
    <>
      <Btn title={`${label} 줄이기${keyHint ? ` (${keyHint[0]})` : ""}`} disabled={i <= 0} onClick={() => go(-1)}><Ic d="M6 12h12" /></Btn>
      <span className="dsp-num" aria-live="polite"><b>{fmt ? fmt(value) : value}</b>{unit && <small>{unit}</small>}</span>
      <Btn title={`${label} 늘리기${keyHint ? ` (${keyHint[1]})` : ""}`} disabled={i >= options.length - 1} onClick={() => go(1)}><Ic d="M12 6v12M6 12h12" /></Btn>
    </>
  );
}

/** 둘 이상 가운데 하나 고르기 */
export function Seg({ label, value, options, onChange, poke }) {
  return (
    <div className="dsp-seg" role="radiogroup" aria-label={label}>
      {options.map(([v, s]) => (
        <button key={String(v)} type="button" role="radio" aria-checked={value === v} onClick={() => { onChange(v); poke(); }}>{s}</button>
      ))}
    </div>
  );
}

/** 설정 줄의 한 칸: 이름 + 고르는 것 */
export function Setting({ label, sep, children }) {
  return (
    <div className="dsp-pc">
      {sep && <span className="dsp-sep" />}
      {label && <span className="lb">{label}</span>}
      {children}
    </div>
  );
}

/**
 * 실험 액자의 테두리: 오른쪽 위(액자 단추 · 학년 토글) · 조작 막대 · 설정 줄 · 진행 막대 · 멈춤 표시.
 * view — 「해 보기 | 풀이 보기」 고르기(막대 끝, 수업 장면으로 앞) · settings — 설정 줄에 넣을 것
 */
export function LabChrome({ ui, ctl, poke, mode, onMode, paused, onPause, onRestart, restartTitle, isFs, toggleFs, onTheme, onGallery, onExit,
  view, settings, prog }) {
  const { Btn, Ic, FrameIc } = ui;
  const stop = (e) => e.stopPropagation();
  return (
    <>
      <div className="dsp-tr">
        <button type="button" className="dsp-fbtn" title="액자 목록" aria-label="액자 목록" onClick={() => { onGallery(); poke(); }}>
          <FrameIc />
        </button>
        <div className={"dsp-mode on-" + mode} role="radiogroup" aria-label="학년">
          <span className="dsp-knob" aria-hidden="true" />
          <button type="button" role="radio" aria-checked={mode === "e"} onClick={() => { onMode("e"); poke(); }}>초등</button>
          <button type="button" role="radio" aria-checked={mode === "m"} onClick={() => { onMode("m"); poke(); }}>중등</button>
        </div>
      </div>
      <div className={"dsp-ctl" + (ctl ? " show" : "")} onPointerDown={stop}>
        <Btn title={`${restartTitle || "처음부터"} (R)`} onClick={() => { onRestart(); poke(); }}><Ic d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3M4.5 4.5v4.6h4.6" /></Btn>
        <Btn title={paused ? "재생 (스페이스)" : "멈춤 (스페이스)"} onClick={() => { onPause(); poke(); }}>
          {paused ? <Ic d="M8 5v14l11-7z" fill /> : <Ic d="M8 5v14M16 5v14" />}
        </Btn>
        <span className="dsp-sep" />
        <Btn title="밝기 바꾸기" onClick={onTheme}><Ic d="M12 3a9 9 0 1 0 0 18V3z" fill /></Btn>
        <Btn title={isFs ? "전체 화면 끝내기 (F)" : "전체 화면 (F)"} onClick={() => { toggleFs(); poke(); }}>
          {isFs ? <Ic d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /> : <Ic d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />}
        </Btn>
        {view}
        <Btn title="수업 장면으로" onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn>
      </div>
      {settings && <div className={"dsp-pctl" + (ctl ? " show" : "")} onPointerDown={stop}>{settings}</div>}
      {prog != null && <div className="dsp-prog" aria-hidden="true"><i style={{ transform: `scaleX(${Math.max(0, Math.min(1, prog))})` }} /></div>}
      {paused && <div className="dsp-paused lab">멈춤</div>}
    </>
  );
}

/** 공통 키: 스페이스 멈춤 · R 처음부터 · F 전체 화면 · T/Tab 학년 · E 초등 · M 중등 */
export const baseKeys = ({ togglePause, restart, toggleFs, onMode, poke }) => ({
  " ": () => { togglePause(); poke(); },
  r: () => { restart(); poke(); },
  f: () => toggleFs(),
  t: () => onMode(),
  Tab: () => onMode(),
  e: () => onMode("e"),
  m: () => onMode("m"),
});

/**
 * 실험 액자 껍데기: 「해 보기」(실험) ↔ 「풀이 보기」(설명 장면 묶음). 고른 보기는 기기에 기억한다. 키보드 V 로도 바꾼다.
 *   renderTry({ viewSeg }) — 실험 화면을 그린다(viewSeg 를 LabChrome 의 view 로 넘긴다)
 *   explain — 풀이 보기에서 돌릴 장면들(수업 장면과 같은 짝 장면 형식)
 */
export function LabShell({ fkey, label, explain, renderTry, ...rest }) {
  const vKey = `ash.display.lab.${fkey}.view`;
  const [view, setView] = useState(() => (lsRead(vKey) === "explain" ? "explain" : "try"));
  const [fresh, setFresh] = useState(false);       // 풀이 보기로 넘어온 직후 — 그 장면을 처음부터
  const V = useRef(view);
  V.current = view;
  const pick = useCallback((v) => {
    if (v === V.current) return;
    if (v === "explain") setFresh(true);
    setView(v);
  }, []);
  useEffect(() => { lsWrite(vKey, view); }, [vKey, view]);
  useKeys({ v: () => { pick(V.current === "try" ? "explain" : "try"); rest.poke(); } }, rest.inert);
  const viewSeg = (
    <>
      <span className="dsp-sep" />
      <Seg label="보기" value={view} options={[["try", "해 보기"], ["explain", "풀이 보기"]]} onChange={pick} poke={rest.poke} />
      <span className="dsp-sep" />
    </>
  );
  if (view === "try") return renderTry({ viewSeg });
  return <StoryPlayer list={explain} lsKey={`ash.display.lab.${fkey}.explain`} label={`${label} 풀이`} extra={viewSeg} fresh={fresh} {...rest} />;
}
