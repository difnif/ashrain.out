// ashrain.out — 교실 모니터 「장면 묶음」 재생기 (frames/player.jsx)
// 짝 장면을 차례로 끝없이 돌린다 — 장면 묶음 액자(story.jsx: 축구 · 서술형), 실험 액자의 「풀이 보기」,
// 컨셉 문제 해설 영상(pages/sets/SetVideo)이 함께 쓴다. 장면 목록을 모르는 순수 재생기라 어느 화면이든 가볍게 들여온다.
// 시계는 벽시계(Date.now)라 새로고침하거나 잠깐 나갔다 와도 그 자리에서 이어진다(그동안 돈 만큼 앞으로).
// 조작: 이전 · 멈춤 · 다음 · 이 장면 반복 · 밝기 · 전체 화면 · 나가기. 키보드 ←/→ · 스페이스 · T(E 초등 · M 중등) · R 반복 · F.
// 장면이 controls(문 개수 · 단계 …)를 가지면 조작 막대 아래에 설정 칩이 뜬다(수업 장면과 같다, ../params.js).
// 단추 모양(Btn · Ic · FrameIc)은 쓰는 화면이 ui 로 넘겨준다(../stage-ui.jsx).
// 3D: 장면이 sim3d(../sim3d/index.js — 지금은 축구 여섯 장면)를 가지면 오른쪽 위에 「2D | 3D」 토글이 뜬다(키보드 3).
//   3D 를 켜면 경기장 속 눈높이의 시뮬레이션이 화면 전체에 돌고(WebGL — three.js 는 이때 처음 불러온다), 설명할 때만 장면이
//   멈추며 화면이 어두워지고 큰 글씨가 나온다. 3D 판은 박자표가 따로라 켜고 끌 때 그 장면을 처음부터 튼다. 기기에 기억한다.
//   WebGL 을 못 쓰는 기기면 2D 로 돌아오고 잠깐 알린다.
import { lazy, Suspense, useCallback, useEffect, useRef, useState } from "react";
import { W, H, SceneTitle } from "../draw.jsx";
import { E, clamp } from "../core.js";
import { paramsOf, durOf, optVal } from "../params.js";
import { Title3D } from "../sim3d/overlay.jsx";

const Stage3D = lazy(() => import("../sim3d/Stage3D.jsx"));
/** 3D 를 켰고 그 장면에 3D 판이 있으면 3D 박자표 */
export const durFor = (pair, P, v3) => (v3 && pair.sim3d ? pair.sim3d.dur : durOf(pair, P));
const FRAME_3D = 1000 / 60;

const MODE_FADE = 1000;   // 초등↔중등 겹침
const PAIR_FADE = 1300;   // 다음 장면으로
const FRAME_MS = 1000 / 40;
const elapsedOf = (c) => (c.held != null ? c.held : Date.now() - c.t0);
const read = (k) => { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch { return null; } };
const write = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* 사생활 모드 등 */ } };

/** 저장된 자리(장면 번호 · 시작 벽시계 · 멈춘 경과 · 반복). 흐르던 중이면 비운 동안 돈 만큼 앞으로 간다 */
export function loadStory(list, now = Date.now(), o = null, prm = null, v3 = false) {
  const n = list.length;
  const d = (i) => durFor(list[i], paramsOf(list[i], prm), v3);
  if (!o || !Number.isInteger(o.i) || o.i < 0 || o.i >= n || !Number.isFinite(o.t0) || o.t0 > now) return { i: 0, t0: now, held: null, rep: false };
  const rep = o.rep === true;
  if (Number.isFinite(o.held) && o.held >= 0) return { i: o.i, t0: o.t0, held: Math.min(o.held, d(o.i)), rep };
  let i = o.i, e = now - o.t0;
  if (rep) e %= d(i);
  else {
    let total = 0;
    for (let j = 0; j < n; j++) total += d(j);
    e %= total;                                   // 한 바퀴를 돌면 같은 장면의 같은 자리
    while (e >= d(i)) { e -= d(i); i = (i + 1) % n; }
  }
  return { i, t0: now - e, held: null, rep };
}

/**
 * 짝 장면을 차례로 돌리는 재생기. list = 장면들, lsKey = 기기에 기억할 이름(자리 · 장면 설정).
 * extra = 조작 막대 끝(수업 장면으로 앞)에 더할 단추들.
 * fresh = 지난번 그 장면을 처음부터(실험 액자에서 「풀이 보기」로 넘어올 때) — 아니면 비운 동안 돈 만큼 앞으로.
 */
// 다른 화면이 같은 재생기를 쓸 때(컨셉 문제 해설 영상): noMode — 학년 토글 숨김 · noGallery — 액자 단추 숨김 ·
//   exitTitle — 나가기 단추 이름 · startAt — 이 장면부터 새로 · apiRef — { goTo, idx } 를 밖으로(목록에서 고르기) ·
//   onIdx — 장면이 바뀔 때 알림. 모두 생략하면 교실 모니터 액자와 똑같다.
export function StoryPlayer({ list, lsKey, label, C, mode, onMode, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, ui, extra, fresh,
  noMode = false, noGallery = false, exitTitle = "수업 장면으로", startAt = null, apiRef = null, onIdx = null }) {
  const { Btn, Ic, FrameIc } = ui;
  const n = list.length;
  const init = useRef(null);
  if (!init.current) {
    const prm0 = read(lsKey + ".prm") || {};
    const o = read(lsKey);
    const v30 = read(lsKey + ".v3") === true && list.some((p) => p.sim3d);
    const st = loadStory(list, Date.now(), o, prm0, v30);
    st.v3 = v30;
    if (fresh) {
      const i = o && Number.isInteger(o.i) && o.i >= 0 && o.i < n ? o.i : 0;
      Object.assign(st, { i, t0: Date.now(), held: null });
    }
    if (Number.isInteger(startAt) && startAt >= 0 && startAt < n) Object.assign(st, { i: startAt, t0: Date.now(), held: null });
    init.current = { ...st, prm: prm0 };
  }
  const [idx, setIdx] = useState(init.current.i);
  const [paused, setPaused] = useState(init.current.held != null);
  const [repeat, setRepeat] = useState(init.current.rep);
  const [prm, setPrm] = useState(init.current.prm);       // { 장면 key: { 설정 key: 값 } }
  const [v3, setV3] = useState(init.current.v3);          // 3D 로 보기(sim3d 가 있는 장면만)
  const [hint3, setHint3] = useState(null);               // 3D 를 못 열었을 때 잠깐 알림
  const clk = useRef({ t0: init.current.t0, held: init.current.held });
  const pf = useRef(null);          // { idx, mode, t, t0, P, v3 } — 앞 장면이 사라지는 중
  const mf = useRef(null);          // { from, t0 } — 학년이 바뀌는 중
  const lastMode = useRef(mode);
  if (lastMode.current !== mode) { mf.current = { from: lastMode.current, t0: performance.now() }; lastMode.current = mode; }
  const [, setFrame] = useState(0);
  const R = useRef({});
  const P = paramsOf(list[idx], prm);
  const use3d = v3 && !!list[idx].sim3d;
  R.current = { idx, repeat, mode, inert, P, use3d, v3 };

  const save = useCallback((i, rep) => write(lsKey, { i, t0: clk.current.t0, held: clk.current.held, rep }), [lsKey]);
  useEffect(() => { if (onIdx) onIdx(idx); }, [idx, onIdx]);
  useEffect(() => { save(init.current.i, init.current.rep); }, [save]);
  useEffect(() => { write(lsKey + ".prm", prm); }, [lsKey, prm]);
  useEffect(() => { if (list.some((p) => p.sim3d)) write(lsKey + ".v3", v3); }, [lsKey, v3, list]);
  useEffect(() => { if (!hint3) return undefined; const h = setTimeout(() => setHint3(null), 4200); return () => clearTimeout(h); }, [hint3]);

  /** 장면 i 로 — 앞 장면은 겹치며 사라진다. 멈춰 있었으면 새 장면도 처음에서 멈춘 채 */
  const goTo = useCallback((i, fade = true) => {
    const cur = R.current;
    if (fade) pf.current = { idx: cur.idx, mode: cur.mode, t: Math.min(elapsedOf(clk.current), durFor(list[cur.idx], cur.P, cur.use3d)), t0: performance.now(), P: cur.P, v3: cur.use3d };
    clk.current = { t0: Date.now(), held: clk.current.held != null ? 0 : null };
    mf.current = null;
    const j = ((i % n) + n) % n;
    setIdx(j); save(j, cur.repeat);
  }, [list, n, save]);
  if (apiRef) apiRef.current = { goTo, idx };
  const togglePause = useCallback(() => {
    const now = Date.now(), c = clk.current;
    clk.current = c.held != null ? { t0: now - c.held, held: null } : { t0: c.t0, held: now - c.t0 };
    setPaused(clk.current.held != null);
    save(R.current.idx, R.current.repeat);
  }, [save]);
  const toggleRepeat = useCallback(() => {
    const rep = !R.current.repeat;
    setRepeat(rep); save(R.current.idx, rep);
  }, [save]);
  /** 지금 장면의 설정 하나를 바꾸고 처음부터 다시 튼다 */
  const setParam = useCallback((k, v) => {
    const cur = R.current, pair = list[cur.idx];
    if (cur.P[k] === v) return;
    goTo(cur.idx, true);
    setPrm((o) => ({ ...o, [pair.key]: { ...(o[pair.key] || {}), [k]: v } }));
  }, [goTo, list]);
  /** 2D ↔ 3D — 박자표가 달라서 그 장면을 처음부터 다시 튼다(앞 그림은 겹치며 사라진다) */
  const set3d = useCallback((on) => {
    const cur = R.current;
    if (!!on === !!cur.v3) return;
    goTo(cur.idx, true);
    setV3(!!on);
  }, [goTo]);
  const on3dFail = useCallback(() => {
    if (pf.current) pf.current.v3 = false;
    setV3(false);
    setHint3("이 화면에서는 3D 를 열 수 없어서 2D 로 보여 줘요");
  }, []);
  const stepParam = useCallback((c, dir) => {
    const ops = c.options.map(optVal), i = ops.indexOf(R.current.P[c.key]);
    const j = clamp(i + dir, 0, ops.length - 1);
    if (j !== i) setParam(c.key, ops[j]);
  }, [setParam]);

  /* ── 그리기 루프 (최대 40fps · 3D 는 60fps, 멈추고 겹침도 끝나면 쉰다) ── */
  useEffect(() => {
    let raf = 0, last = 0;
    const loop = (now) => {
      raf = requestAnimationFrame(loop);
      const cur = R.current;
      if (now - last < (cur.use3d ? FRAME_3D - 1 : FRAME_MS)) return;
      last = now;
      if (clk.current.held == null && Date.now() - clk.current.t0 >= durFor(list[cur.idx], cur.P, cur.use3d)) goTo(cur.repeat ? cur.idx : cur.idx + 1, true);
      const busy = !!(mf.current || pf.current);
      if (mf.current && now - mf.current.t0 > MODE_FADE) mf.current = null;
      if (pf.current && now - pf.current.t0 > PAIR_FADE) pf.current = null;
      if (clk.current.held != null && !busy) return;
      setFrame((f) => (f + 1) % 1e9);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [goTo, list]);

  /* ── 키보드 ── */
  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey || R.current.inert) return;
      const k = e.key;
      if (k === "ArrowRight") { goTo(R.current.idx + 1); poke(); }
      else if (k === "ArrowLeft") { goTo(R.current.idx - 1); poke(); }
      else if (k === " ") { e.preventDefault(); togglePause(); poke(); }
      else if (!noMode && (k === "e" || k === "E")) onMode("e");
      else if (!noMode && (k === "m" || k === "M")) onMode("m");
      else if (!noMode && (k === "t" || k === "T" || k === "Tab")) { e.preventDefault(); onMode(); }
      else if (k === "r" || k === "R") { toggleRepeat(); poke(); }
      else if (k === "3" && list[R.current.idx].sim3d) { set3d(!R.current.v3); poke(); }
      else if (k === "f" || k === "F") toggleFs();
      else if (k === "ArrowUp" || k === "ArrowDown") {
        const c = (list[R.current.idx].controls || []).find((x) => x.kind === "step");
        if (c) { e.preventDefault(); stepParam(c, k === "ArrowUp" ? 1 : -1); poke(); }
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [goTo, togglePause, toggleRepeat, stepParam, onMode, toggleFs, poke, list, noMode, set3d]);

  /* ── 그릴 층: 사라지는 앞 장면 · 학년 겹침 ── */
  const now = performance.now();
  const pair = list[idx];
  const dur = durFor(pair, P, use3d);
  const t = clamp(elapsedOf(clk.current), 0, dur);
  const layers = [];
  const p = pf.current, m = mf.current;
  const kin = p ? E.sine(clamp((now - p.t0) / PAIR_FADE)) : 1;
  if (p && kin < 1) layers.push({ key: "out", pair: list[p.idx], mode: p.mode, t: p.t, o: 1 - kin, P: p.P, v3: !!p.v3 });
  if (m) {
    const k = E.sine(clamp((now - m.t0) / MODE_FADE));
    if (k < 1) layers.push({ key: "from-" + m.from, pair, mode: m.from, t, o: kin * (1 - k * k), P, v3: use3d });
    layers.push({ key: "to-" + mode, pair, mode, t, o: kin * k, P, v3: use3d });
  } else layers.push({ key: "cur-" + mode, pair, mode, t, o: kin, P, v3: use3d });
  // 3D 세계: 지금 장면(3D 면) — 아니면 3D 로 돌던 앞 장면이 사라지는 동안 그 장면
  const outgoing3d = p && kin < 1 && p.v3 ? list[p.idx] : null;
  const world3d = use3d ? pair.sim3d.world(t) : outgoing3d ? outgoing3d.sim3d.world(p.t) : null;
  for (const L of layers) if (L.v3) L.W = L.key === "out" ? (outgoing3d ? outgoing3d.sim3d.world(p.t) : null) : use3d ? world3d : null;
  const canvasO = use3d ? (p && !p.v3 && kin < 1 ? kin : 1) : outgoing3d ? 1 - kin : 0;
  const has3d = !!pair.sim3d;
  const stop = (e) => e.stopPropagation();

  return (
    <>
      {world3d && (
        <Suspense fallback={<div className="dsp-3d dsp-3d-wait"><span>3D 경기장을 불러오는 중…</span></div>}>
          <Stage3D world={world3d} theme={C.name === "light" ? "light" : "dark"} o={canvasO} onFail={on3dFail} />
        </Suspense>
      )}
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet"
        role="img" aria-label={`${label} — ${pair.title[mode]}${use3d ? " (3D)" : ""}`}>
        {layers.map((L) => (
          <g key={L.key + "@" + L.pair.key + (L.v3 ? "@3d" : "")} opacity={L.o}>
            {L.v3 && L.W ? (
              <g opacity={1 - (L.W.edge || 0)}>
                {L.pair.sim3d.overlay(L.mode, L.t, C, L.P, L.W)}
                <Title3D title={L.pair.title[L.mode]} sub={L.pair.sub[L.mode]} mode={L.mode} o={1 - clamp(L.W.dim / 0.55)} />
              </g>
            ) : (<>
              <SceneTitle title={L.pair.title[L.mode]} sub={L.pair.sub[L.mode]} C={C} mode={L.mode} />
              {L.pair.render(L.mode, L.t, C, L.P)}
            </>)}
          </g>
        ))}
      </svg>

      {/* 오른쪽 위 — 액자 단추 · 학년 토글 (수업 장면과 같은 자리) */}
      {!(noMode && noGallery && !has3d) && <div className="dsp-tr">
        {!noGallery && <button type="button" className="dsp-fbtn" title="액자 목록" aria-label="액자 목록" onClick={() => { onGallery(); poke(); }}>
          <FrameIc />
        </button>}
        {has3d && <div className={"dsp-vw on-" + (v3 ? "3d" : "2d")} role="radiogroup" aria-label="보기 (키보드 3)">
          <span className="dsp-knob" aria-hidden="true" />
          <button type="button" role="radio" aria-checked={!v3} title="위에서 내려다본 그림" onClick={() => { set3d(false); poke(); }}>2D</button>
          <button type="button" role="radio" aria-checked={v3} title="경기장 속 눈높이 시뮬레이션 (키보드 3)" onClick={() => { set3d(true); poke(); }}>3D</button>
        </div>}
        {!noMode && <div className={"dsp-mode on-" + mode} role="radiogroup" aria-label="학년">
          <span className="dsp-knob" aria-hidden="true" />
          <button type="button" role="radio" aria-checked={mode === "e"} onClick={() => { onMode("e"); poke(); }}>초등</button>
          <button type="button" role="radio" aria-checked={mode === "m"} onClick={() => { onMode("m"); poke(); }}>중등</button>
        </div>}
      </div>}

      <div className={"dsp-ctl" + (ctl ? " show" : "")} onPointerDown={stop}>
        {n > 1 && <Btn title="이전 장면 (←)" onClick={() => { goTo(idx - 1); poke(); }}><Ic d="M15 5 8 12l7 7M6 5v14" /></Btn>}
        <Btn title={paused ? "재생 (스페이스)" : "멈춤 (스페이스)"} onClick={() => { togglePause(); poke(); }}>
          {paused ? <Ic d="M8 5v14l11-7z" fill /> : <Ic d="M8 5v14M16 5v14" />}
        </Btn>
        {n > 1 && <Btn title="다음 장면 (→)" onClick={() => { goTo(idx + 1); poke(); }}><Ic d="m9 5 7 7-7 7M18 5v14" /></Btn>}
        <span className="dsp-sep" />
        {n > 1 && <Btn title="이 장면 반복 (R)" on={repeat} onClick={() => { toggleRepeat(); poke(); }}>
          <Ic d="M17 2l3 3-3 3M4 11V9a4 4 0 0 1 4-4h12M7 22l-3-3 3-3M20 13v2a4 4 0 0 1-4 4H4" />
        </Btn>}
        <Btn title="밝기 바꾸기" onClick={onTheme}><Ic d="M12 3a9 9 0 1 0 0 18V3z" fill /></Btn>
        <Btn title={isFs ? "전체 화면 끝내기 (F)" : "전체 화면 (F)"} onClick={() => { toggleFs(); poke(); }}>
          {isFs ? <Ic d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /> : <Ic d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />}
        </Btn>
        {extra}
        <Btn title={exitTitle} onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn>
      </div>

      {/* 장면 설정 — 이 장면이 고를 것을 가지고 있을 때만(수업 장면과 같은 모양) */}
      {pair.controls && (
        <div className={"dsp-pctl" + (ctl ? " show" : "")} onPointerDown={stop}>
          {pair.controls.map((c, ci) => (
            <div key={c.key} className="dsp-pc">
              {ci > 0 && <span className="dsp-sep" />}
              <span className="lb">{c.label}</span>
              {c.kind === "step" ? (<>
                <Btn title={`${c.label} 줄이기${ci === 0 ? " (↓)" : ""}`} disabled={P[c.key] === optVal(c.options[0])}
                  onClick={() => { stepParam(c, -1); poke(); }}><Ic d="M6 12h12" /></Btn>
                <span className="dsp-num" aria-live="polite"><b>{c.fmt ? c.fmt(P[c.key]) : P[c.key]}</b>{c.unit && <small>{c.unit}</small>}</span>
                <Btn title={`${c.label} 늘리기${ci === 0 ? " (↑)" : ""}`} disabled={P[c.key] === optVal(c.options.at(-1))}
                  onClick={() => { stepParam(c, 1); poke(); }}><Ic d="M12 6v12M6 12h12" /></Btn>
              </>) : (
                <div className="dsp-seg" role="radiogroup" aria-label={c.label}>
                  {c.options.map((o) => (
                    <button key={optVal(o)} type="button" role="radio" aria-checked={P[c.key] === optVal(o)}
                      onClick={() => { setParam(c.key, optVal(o)); poke(); }}>{Array.isArray(o) ? o[1] : o}</button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* 진행 — 묶음 안의 장면 점 + 지금 장면의 흐름 */}
      {n > 1 && <div className="dsp-dots" aria-hidden="true">
        {list.map((q, i) => <i key={q.key} className={i === idx ? "on" : ""} />)}
      </div>}
      <div className="dsp-prog" aria-hidden="true"><i style={{ transform: `scaleX(${t / dur})` }} /></div>
      {paused && <div className="dsp-paused">멈춤</div>}
      {hint3 && <div className="dsp-hint show dsp-hint3">{hint3}</div>}
    </>
  );
}
