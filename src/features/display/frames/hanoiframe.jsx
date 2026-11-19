// ashrain.out — 교실 모니터 「액자」: 하노이의 탑 — 액자 (frames/hanoiframe.jsx)
// 끝없이 옮긴다(첫 기둥 → 마지막 기둥, 쉬고, 거꾸로 …). 시계는 벽시계(Date.now)라 새로고침 · 잠깐 나갔다 와도 그 자리에서 이어진다.
//   원판 3 ~ 30개 · 기둥 3 ~ 5개(4개부터는 프레임–스튜어트) · 세트 1 ~ 5개 · 빠르기 자연스럽게 | 1 ~ 4배속
//   세트 2개부터 대각선 위에서 내려다보고, 5개면 로봇 다섯 대가 나른다. 4배속이면 파티(조명 · 콘페티).
// 보기: 「입체」(three.js 3D, 처음 볼 때 내려받는다 — 그동안은 평면 그림) | 「평면」(SVG). 3D 를 못 쓰면 저절로 평면.
// 원판 · 기둥 수를 바꾸면 처음부터, 빠르기를 바꾸면 옮기던 그 이동의 같은 진행에서, 세트 수는 그대로 이어진다.
import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { HANOI, normSpeed, hanoiTimeline, hanoiAt, remapElapsed, fmtDur, comma, movesOf } from "../hanoi";
import { HanoiInfo, HanoiSets2D } from "./hanoi.jsx";

const Stage3D = lazy(() => import("../hanoi3d/Stage.jsx"));
const LSK = "ash.display.hanoi";
const W = 1600, H = 900;
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 사생활 모드 등 */ } };
const SP_SHORT = { natural: "자연스럽게", x1: "1배", x2: "2배", x3: "3배", x4: "4배" };
const SP_TITLE = { natural: "자연스럽게 — 옮기는 길이에 맞춰", x1: "1배속 — 1초에 1개", x2: "2배속 — 1초에 2개", x3: "3배속 — 1초에 3개", x4: "4배속 — 1초에 4개 · 파티" };

/** 저장된 상태: 원판 · 기둥 · 세트 · 빠르기 · 보기 · 시작 시각(벽시계 ms) · 멈춘 경과. 예전 값("fast")도 읽는다 */
export function loadHanoi() {
  try {
    const o = JSON.parse(localStorage.getItem(LSK) || "null");
    if (o && Number.isInteger(o.n) && o.n >= HANOI.MIN && o.n <= HANOI.MAX && Number.isFinite(o.t0) && o.t0 <= Date.now()) {
      return {
        n: o.n, pegs: HANOI.PEGS.includes(o.pegs) ? o.pegs : 3, sets: HANOI.SETS.includes(o.sets) ? o.sets : 1,
        sp: normSpeed(o.sp), view: o.view === "2d" ? "2d" : "3d",
        t0: o.t0, held: Number.isFinite(o.held) && o.held >= 0 ? o.held : null,
      };
    }
  } catch { /* 처음이거나 망가진 값 */ }
  return { n: HANOI.DEF, pegs: 3, sets: 1, sp: "x1", view: "3d", t0: Date.now(), held: null };
}

export function HanoiFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, ui }) {
  const { Btn, Ic, FrameIc } = ui;
  const init = useRef(null);
  if (!init.current) init.current = loadHanoi();
  const [n, setN] = useState(init.current.n);
  const [pegs, setPegs] = useState(init.current.pegs);
  const [sets, setSets] = useState(init.current.sets);
  const [sp, setSp] = useState(init.current.sp);
  const [view, setView] = useState(init.current.view);
  const [fail3d, setFail3d] = useState(false);
  const [ready3d, setReady3d] = useState(false);
  const [paused, setPaused] = useState(init.current.held != null);
  const clk = useRef({ t0: init.current.t0, held: init.current.held });
  const [, setTick] = useState(0);
  const [ver, setVer] = useState(0);
  const TL = useMemo(() => hanoiTimeline(n, sp, pegs), [n, sp, pegs]);
  const natTotal = useMemo(() => hanoiTimeline(n, "natural", pegs).total, [n, pegs]);
  const R = useRef({});
  R.current = { n, pegs, sets, sp, view, inert };

  const save = () => {
    const c = R.current;
    lsSet(LSK, JSON.stringify({ n: c.n, pegs: c.pegs, sets: c.sets, sp: c.sp, view: c.view, t0: clk.current.t0, held: clk.current.held }));
  };
  useEffect(() => { save(); }, [n, pegs, sets, sp, view, paused, ver]);   // eslint-disable-line react-hooks/exhaustive-deps
  const elapsedNow = useCallback(() => (clk.current.held != null ? clk.current.held : Date.now() - clk.current.t0), []);

  const togglePause = useCallback(() => {
    const now = Date.now(), c = clk.current;
    if (c.held != null) { clk.current = { t0: now - c.held, held: null }; setPaused(false); }
    else { clk.current = { t0: c.t0, held: now - c.t0 }; setPaused(true); }
  }, []);
  const restartClock = () => { clk.current = { t0: Date.now(), held: clk.current.held != null ? 0 : null }; };
  const restart = useCallback(() => { restartClock(); setVer((v) => v + 1); }, []);
  const setDisks = useCallback((k) => {
    const nn = clamp(k, HANOI.MIN, HANOI.MAX);
    if (nn === R.current.n) return;
    restartClock(); setN(nn); setVer((v) => v + 1);
  }, []);
  const setPegCount = useCallback((k) => {
    if (!HANOI.PEGS.includes(k) || k === R.current.pegs) return;
    restartClock(); setPegs(k); setVer((v) => v + 1);
  }, []);
  const setSetCount = useCallback((k) => { if (HANOI.SETS.includes(k)) setSets(k); }, []);
  const setSpeed = useCallback((s2) => {
    const { sp: s1, n: nn, pegs: pp } = R.current;
    s2 = normSpeed(s2);
    if (s2 === s1) return;
    const now = Date.now(), c = clk.current;
    const e2 = remapElapsed(hanoiTimeline(nn, s1, pp), hanoiTimeline(nn, s2, pp), c.held != null ? c.held : now - c.t0);
    clk.current = c.held != null ? { t0: c.t0, held: e2 } : { t0: now - e2, held: null };
    setSp(s2); setVer((v) => v + 1);
  }, []);
  const stepSpeed = useCallback((dir) => {
    const L = HANOI.SPEEDS, i = L.indexOf(R.current.sp);
    setSpeed(L[clamp(i + dir, 0, L.length - 1)]);
  }, [setSpeed]);
  const show3d = view === "3d" && !fail3d;

  /* ── 다시 그리기: 평면은 40fps, 입체는 글자만(8fps — 그림은 엔진이 스스로) · 멈추면 쉰다 ── */
  const drawing3d = show3d && ready3d;
  useEffect(() => {
    let raf = 0, last = 0;
    const gap = drawing3d ? 125 : 25;
    const loop = (now) => {
      raf = requestAnimationFrame(loop);
      if (now - last < gap || clk.current.held != null) return;
      last = now;
      setTick((f) => (f + 1) % 1e9);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [drawing3d]);

  /* ── 키보드 ── */
  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey || R.current.inert) return;
      const k = e.key;
      if (k === " ") { e.preventDefault(); togglePause(); poke(); }
      else if (k === "ArrowUp" || k === "+" || k === "=") { e.preventDefault(); setDisks(R.current.n + 1); poke(); }
      else if (k === "ArrowDown" || k === "-" || k === "_") { e.preventDefault(); setDisks(R.current.n - 1); poke(); }
      else if (k === "ArrowRight") { e.preventDefault(); stepSpeed(1); poke(); }
      else if (k === "ArrowLeft") { e.preventDefault(); stepSpeed(-1); poke(); }
      else if (k === "s" || k === "S") { const L = HANOI.SPEEDS; setSpeed(L[(L.indexOf(R.current.sp) + 1) % L.length]); poke(); }
      else if (k === "p" || k === "P") { const L = HANOI.PEGS; setPegCount(L[(L.indexOf(R.current.pegs) + 1) % L.length]); poke(); }
      else if (/^[1-5]$/.test(k)) { setSetCount(Number(k)); poke(); }
      else if (k === "v" || k === "V") { setReady3d(false); setView((v) => (v === "3d" ? "2d" : "3d")); poke(); }
      else if (k === "r" || k === "R") { restart(); poke(); }
      else if (k === "f" || k === "F") toggleFs();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [togglePause, setDisks, stepSpeed, setSpeed, setPegCount, setSetCount, restart, toggleFs, poke]);

  const e = elapsedNow();
  const st = hanoiAt(TL, e);
  const prog = st.hold != null ? 1 : st.tau / TL.total;
  const moves = movesOf(n, pegs);
  const info = { total: TL.total, speed: sp, moves, pegs, sets };
  const cfg = useMemo(() => ({ TL, sets, speed: sp }), [TL, sets, sp]);
  const stop = (ev) => ev.stopPropagation();
  const x1 = moves * 1000;
  const cur = sp === "x2" || sp === "x3" ? sp : "x4";
  const flat = (
    <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label={`하노이의 탑 — 원판 ${n}개, 기둥 ${pegs}개`}>
      <HanoiSets2D TL={TL} elapsed={e} sets={sets} C={C} speed={sp} />
    </svg>
  );

  return (
    <>
      {(!show3d || !ready3d) && flat}
      {show3d && (
        <Suspense fallback={null}>
          <Stage3D cfg={cfg} theme={C.name} clock={elapsedNow} paused={paused} onFail={() => setFail3d(true)} onReady={() => setTimeout(() => setReady3d(true), 760)} />
        </Suspense>
      )}
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" aria-hidden="true" style={{ pointerEvents: "none" }}>
        <HanoiInfo L={TL.L} st={st} C={C} info={info} bannerY={show3d || sets > 1 ? 128 : undefined} />
      </svg>

      <div className={"dsp-ctl" + (ctl ? " show" : "")} onPointerDown={stop}>
        <Btn title="처음부터 (R)" onClick={() => { restart(); poke(); }}><Ic d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3M4.5 4.5v4.6h4.6" /></Btn>
        <Btn title={paused ? "재생 (스페이스)" : "멈춤 (스페이스)"} onClick={() => { togglePause(); poke(); }}>
          {paused ? <Ic d="M8 5v14l11-7z" fill /> : <Ic d="M8 5v14M16 5v14" />}
        </Btn>
        <span className="dsp-sep" />
        <Btn title="원판 하나 빼기 (↓)" disabled={n <= HANOI.MIN} onClick={() => { setDisks(n - 1); poke(); }}><Ic d="M6 12h12" /></Btn>
        <span className="dsp-num" aria-live="polite"><b>{n}</b><small>원판</small></span>
        <Btn title="원판 하나 더 (↑)" disabled={n >= HANOI.MAX} onClick={() => { setDisks(n + 1); poke(); }}><Ic d="M12 6v12M6 12h12" /></Btn>
        <span className="dsp-sep" />
        <div className="dsp-seg" role="radiogroup" aria-label="빠르기 (← →)">
          {HANOI.SPEEDS.map((s) => (
            <button key={s} type="button" role="radio" aria-checked={sp === s} title={SP_TITLE[s]} onClick={() => { setSpeed(s); poke(); }}>{SP_SHORT[s]}</button>
          ))}
        </div>
        <span className="dsp-sep" />
        <Btn title="밝기 바꾸기" onClick={onTheme}><Ic d="M12 3a9 9 0 1 0 0 18V3z" fill /></Btn>
        <Btn title={isFs ? "전체 화면 끝내기 (F)" : "전체 화면 (F)"} onClick={() => { toggleFs(); poke(); }}>
          {isFs ? <Ic d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /> : <Ic d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />}
        </Btn>
        <Btn title="액자 목록" onClick={() => { onGallery(); poke(); }}><FrameIc /></Btn>
        <Btn title="수업 장면으로" onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn>
      </div>
      <div className={"dsp-pctl" + (ctl ? " show" : "")} onPointerDown={stop}>
        <div className="dsp-pc">
          <span className="lb">기둥</span>
          <div className="dsp-seg" role="radiogroup" aria-label="기둥 수 (P)">
            {HANOI.PEGS.map((k) => (
              <button key={k} type="button" role="radio" aria-checked={pegs === k} onClick={() => { setPegCount(k); poke(); }}>{k}</button>
            ))}
          </div>
        </div>
        <span className="dsp-sep" />
        <div className="dsp-pc">
          <span className="lb">세트</span>
          <div className="dsp-seg" role="radiogroup" aria-label="세트 수 (1 ~ 5)">
            {HANOI.SETS.map((k) => (
              <button key={k} type="button" role="radio" aria-checked={sets === k} title={k === 5 ? "5세트 — 로봇이 옮겨요" : `${k}세트`}
                onClick={() => { setSetCount(k); poke(); }}>{k}</button>
            ))}
          </div>
        </div>
        <span className="dsp-sep" />
        <div className="dsp-pc">
          <span className="lb">보기</span>
          <div className="dsp-seg" role="radiogroup" aria-label="보기 (V)">
            <button type="button" role="radio" aria-checked={view === "3d"} disabled={fail3d} title={fail3d ? "이 화면에서는 입체를 쓸 수 없어요" : "입체(3D)"}
              onClick={() => { if (view !== "3d") setReady3d(false); setView("3d"); poke(); }}>입체</button>
            <button type="button" role="radio" aria-checked={view !== "3d"} onClick={() => { setView("2d"); poke(); }}>평면</button>
          </div>
        </div>
      </div>
      <div className={"dsp-hint low" + (ctl ? " show" : "")} aria-hidden={!ctl}>
        원판 {n}개 · 기둥 {pegs}개 → {comma(moves)}번 · 자연스럽게 <b className={sp === "natural" ? "on" : ""}>{fmtDur(natTotal)}</b>
        {" · "}1배속 <b className={sp === "x1" ? "on" : ""}>{fmtDur(x1)}</b>
        {" · "}{SP_SHORT[cur]}속 <b className={sp === cur ? "on" : ""}>{fmtDur(x1 / Number(cur.slice(1)))}</b>
      </div>

      <div className="dsp-prog" aria-hidden="true"><i style={{ transform: `scaleX(${prog})` }} /></div>
      <div className="dsp-tags">
        {paused && <span className="dsp-tag">멈춤</span>}
        {sets >= 5 && show3d && <span className="dsp-tag robot">로봇 다섯 대</span>}
        {sp === "x4" && show3d && <span className="dsp-tag party">파티 모드</span>}
      </div>
    </>
  );
}
