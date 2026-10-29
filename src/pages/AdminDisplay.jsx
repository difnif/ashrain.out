// 관리자 — 교실 모니터 (#/admin/display)
// 가로 화면에 도형 애니메이션을 자동으로 돌린다(공간 감각 기르기). 오른쪽 위 「초등 | 중등」 토글을 누르면
// 지금 장면이 짝이 되는 장면으로 같은 시각에 겹쳐 넘어간다 — 두 판은 같은 박자표를 쓰도록 저작되어 있다.
// 장면 목록: src/features/display/pairs.js · 엔진: core.js(계산) + draw.jsx(그리기)
// 화면은 탭·마우스 움직임에 조작 막대가 잠깐 뜨고 스스로 숨는다. 전체 화면·화면 꺼짐 방지 포함.
// 액자: 토글 왼쪽의 액자 단추 → 액자 목록 → 고르면 수업 장면 대신 그 액자가 계속 돈다. 액자는 벽시계로 흘러서 새로고침해도
//       이어진다. 목록: src/features/display/frames/index.js
//       · 하노이의 탑(frames/hanoi.jsx · hanoi.js)
//       · 실험 액자 — 몬티홀 · 갈림길과 구슬 · 구슬 낙하 실험(frames/monty.jsx · branchlab.jsx · galtonlab.jsx, 공용 frames/xkit.jsx).
//         교육과정에 딱 맞기보다 융합·탐구에 가까워 수업 장면 순환에서 빼고, 직접 해 보는 것을 먼저 보여 준다.
//         「풀이 보기」를 고르면 예전 설명 장면(몬티홀·찍기 · 갈림길·구슬 · 정규분포)을 그대로 돌린다.
//       · 장면 묶음 — 숫자로 읽는 축구 · 서술형 이야기(stories.js · frames/story.jsx): 여러 단원을 섞는 융합 장면.
// 장면 설정: 장면이 controls(구슬 수·단계·문 개수 …)를 가지면 조작 막대 아래에 설정 칩이 뜬다. 바꾸면 그 장면을
//       처음부터 다시 튼다. 장면마다 기기에 기억한다. 장면은 render(mode, t, C, P) 의 P 로 설정을 받는다.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { PAIRS, GROUPS } from "../features/display/pairs";
import { PALETTE, W, H, SceneTitle, clearMeasureCache } from "../features/display/draw";
import { E, clamp } from "../features/display/core";
import { FRAMES } from "../features/display/frames/index.js";
import { paramsOf, durOf, optVal } from "../features/display/params.js";
import { HanoiArt, HanoiThumb } from "../features/display/frames/hanoi.jsx";
import { StoryFrame, StoryThumb } from "../features/display/frames/story.jsx";
import { MontyFrame, MontyThumb } from "../features/display/frames/monty.jsx";
import { BranchFrame, BranchThumb } from "../features/display/frames/branchlab.jsx";
import { GaltonFrame, GaltonThumb } from "../features/display/frames/galtonlab.jsx";
import { HANOI, hanoiTimeline, hanoiAt, remapElapsed, fmtDur, comma } from "../features/display/hanoi";

const LS = { mode: "ash.display.mode", theme: "ash.display.theme", idx: "ash.display.idx", rep: "ash.display.repeat", grp: "ash.display.group",
  view: "ash.display.view", hanoi: "ash.display.hanoi", prm: "ash.display.params" };
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 사생활 모드 등 */ } };

const MODE_FADE = 1000;   // 초등↔중등 겹침
const PAIR_FADE = 1300;   // 다음 장면으로
const FRAME_MS = 1000 / 40;
const IDLE_MS = 3600;
const PRETENDARD = "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css";

/* ── 장면 설정: 기기에 기억(장면 key 마다) ── */
function loadPrm() {
  try { const o = JSON.parse(localStorage.getItem(LS.prm) || "{}"); return o && typeof o === "object" ? o : {}; } catch { return {}; }
}

/* ── 묶음: 전체 / 도형 / 경우의 수·확률 … — 고른 묶음 안에서만 돈다 ── */
const orderOf = (g) => PAIRS.map((_, i) => i).filter((i) => g === "all" || PAIRS[i].group === g);
function stepIdx(cur, dir, g) {
  const ord = orderOf(g);
  if (!ord.length) return cur;
  const pos = ord.indexOf(cur);
  if (pos < 0) return dir >= 0 ? ord[0] : ord[ord.length - 1];
  return ord[(pos + dir + ord.length) % ord.length];
}

export default function AdminDisplay() {
  const [me, setMe] = useState(undefined);   // undefined 확인 중 | false | true
  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) { setMe(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
      setMe(p?.role === "admin");
    }).catch(() => setMe(false));
  }, []);
  if (me === undefined) return <div style={{ position: "fixed", inset: 0, background: PALETTE.dark.bg[2] }} />;
  if (!me) {
    return (
      <div style={{ position: "fixed", inset: 0, background: "#121a33", color: "#F2E8D0", fontSize: 15,
        display: "grid", placeItems: "center", fontFamily: "'Pretendard Variable', Pretendard, system-ui, sans-serif" }}>
        <p>관리자 전용 화면이에요. <a href="#/" style={{ color: "#B8B0A0" }}>돌아가기</a></p>
      </div>
    );
  }
  return <Stage />;
}

function Stage() {
  const [mode, setMode] = useState(() => (lsGet(LS.mode, "e") === "m" ? "m" : "e"));
  const [idx, setIdx] = useState(() => {
    const n = Number(lsGet(LS.idx, 0));
    return Number.isInteger(n) && n >= 0 && n < PAIRS.length ? n : 0;
  });
  const [thm, setThm] = useState(() => (lsGet(LS.theme, "dark") === "light" ? "light" : "dark"));
  const [grp, setGrp] = useState(() => { const g = lsGet(LS.grp, "all"); return GROUPS.some((x) => x.key === g) ? g : "all"; });
  const [paused, setPaused] = useState(false);
  const [repeat, setRepeat] = useState(() => lsGet(LS.rep, "0") === "1");
  const [ctl, setCtl] = useState(true);
  const [list, setList] = useState(false);
  const [gal, setGal] = useState(false);       // 액자 목록
  const [view, setView] = useState(() => (FRAMES.some((f) => f.key === lsGet(LS.view, "")) ? lsGet(LS.view, "") : null));   // null = 수업 장면
  const [isFs, setIsFs] = useState(false);
  const [prm, setPrm] = useState(loadPrm);     // { 장면 key: { 설정 key: 값 } }
  const [, setFrame] = useState(0);

  const rootRef = useRef(null);
  // held = 멈춘 동안의 경과(ms). 액자로 시작하면 수업 장면 시계는 0에서 멈춰 둔다.
  const clk = useRef(view ? { start: performance.now(), held: 0 } : { start: performance.now(), held: null });
  const sceneHold = useRef(view ? { wasPaused: false } : null);   // 액자로 가며 멈춘 수업 장면 — 돌아오면 다시 흐른다
  const mfade = useRef(null);   // { from, t0 }
  const pfade = useRef(null);   // { idx, mode, t, t0 }
  const S = useRef({});         // 루프가 읽는 최신 상태
  S.current = { idx, mode, repeat, paused, list, grp, view, gal, prm, P: paramsOf(PAIRS[idx], prm) };

  const elapsed = (now = performance.now()) => (clk.current.held != null ? clk.current.held : now - clk.current.start);

  useEffect(() => { lsSet(LS.mode, mode); }, [mode]);
  useEffect(() => { lsSet(LS.idx, idx); }, [idx]);
  useEffect(() => { lsSet(LS.theme, thm); }, [thm]);
  useEffect(() => { lsSet(LS.rep, repeat ? 1 : 0); }, [repeat]);
  useEffect(() => { lsSet(LS.grp, grp); }, [grp]);
  useEffect(() => { lsSet(LS.view, view || ""); }, [view]);
  useEffect(() => { lsSet(LS.prm, JSON.stringify(prm)); }, [prm]);

  /* ── 액자 열기·닫기 — 수업 장면 시계는 액자 동안 멈춰 둔다 ── */
  const openFrame = useCallback((key) => {
    setGal(false); setList(false);
    if (!S.current.view) {
      sceneHold.current = { wasPaused: clk.current.held != null };
      if (clk.current.held == null) clk.current = { start: clk.current.start, held: performance.now() - clk.current.start };
    }
    pfade.current = null; mfade.current = null;
    setView(key);
  }, []);
  const closeFrame = useCallback(() => {
    setGal(false);
    if (S.current.view && sceneHold.current && !sceneHold.current.wasPaused && clk.current.held != null) {
      clk.current = { start: performance.now() - clk.current.held, held: null };
    }
    sceneHold.current = null;
    setView(null);
  }, []);

  /* ── 장면 이동 (다음 쌍은 겹치며 넘어간다) ── */
  const goTo = useCallback((i, fade = true) => {
    const now = performance.now();
    const cur = S.current;
    const from = PAIRS[cur.idx];
    if (fade) pfade.current = { idx: cur.idx, mode: cur.mode, t: Math.min(elapsed(now), durOf(from, cur.P)), t0: now, P: cur.P };
    clk.current = { start: now, held: cur.paused ? 0 : null };
    mfade.current = null;
    setIdx(((i % PAIRS.length) + PAIRS.length) % PAIRS.length);
  }, []);
  const flipMode = useCallback((to) => {
    const cur = S.current.mode;
    const next = to || (cur === "e" ? "m" : "e");
    if (next === cur) return;
    mfade.current = { from: cur, t0: performance.now() };
    setMode(next);
  }, []);
  const togglePause = useCallback(() => {
    const now = performance.now();
    if (clk.current.held != null) { clk.current = { start: now - clk.current.held, held: null }; setPaused(false); }
    else { clk.current = { start: clk.current.start, held: now - clk.current.start }; setPaused(true); }
  }, []);
  /** 지금 장면의 설정 하나를 바꾸고 처음부터 다시 튼다 */
  const setParam = useCallback((k, v) => {
    const cur = S.current, pair = PAIRS[cur.idx];
    if (cur.P[k] === v) return;
    goTo(cur.idx, true);
    setPrm((o) => ({ ...o, [pair.key]: { ...(o[pair.key] || {}), [k]: v } }));
  }, [goTo]);
  /** 단계형 설정을 한 칸 앞뒤로 */
  const stepParam = useCallback((c, dir) => {
    const ops = c.options.map(optVal), i = ops.indexOf(S.current.P[c.key]);
    const j = clamp(i + dir, 0, ops.length - 1);
    if (j !== i) setParam(c.key, ops[j]);
  }, [setParam]);

  /* ── 그리기 루프 (최대 40fps) ── */
  useEffect(() => {
    let raf = 0, last = 0;
    const loop = (now) => {
      raf = requestAnimationFrame(loop);
      if (now - last < FRAME_MS) return;
      last = now;
      const cur = S.current;
      if (cur.view) return;   // 액자는 FrameStage 가 따로 그린다
      if (clk.current.held == null && now - clk.current.start >= durOf(PAIRS[cur.idx], cur.P)) {
        goTo(cur.repeat ? cur.idx : stepIdx(cur.idx, 1, cur.grp), true);
      }
      if (mfade.current && now - mfade.current.t0 > MODE_FADE) mfade.current = null;
      if (pfade.current && now - pfade.current.t0 > PAIR_FADE) pfade.current = null;
      setFrame((f) => (f + 1) % 1e9);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [goTo]);

  /* ── 글꼴: Pretendard(본문) — 늦게 오면 글자 폭을 다시 잰다 ── */
  useEffect(() => {
    if (!document.getElementById("pretendard-css")) {
      const l = document.createElement("link");
      l.id = "pretendard-css"; l.rel = "stylesheet"; l.href = PRETENDARD;
      document.head.appendChild(l);
    }
    const fonts = document.fonts;
    const onDone = () => clearMeasureCache();
    fonts?.ready?.then(onDone).catch(() => {});
    fonts?.addEventListener?.("loadingdone", onDone);
    return () => fonts?.removeEventListener?.("loadingdone", onDone);
  }, []);

  /* ── 화면 꺼짐 방지 ── */
  useEffect(() => {
    let lock = null;
    const req = async () => {
      try { if (document.visibilityState === "visible" && navigator.wakeLock) lock = await navigator.wakeLock.request("screen"); }
      catch { /* 지원 안 함·거부 */ }
    };
    req();
    const onVis = () => { if (document.visibilityState === "visible") req(); };
    document.addEventListener("visibilitychange", onVis);
    return () => { document.removeEventListener("visibilitychange", onVis); try { lock?.release?.(); } catch { /* 무시 */ } };
  }, []);

  /* ── 문서 제목 · 전체 화면 상태 ── */
  useEffect(() => {
    const prev = document.title;
    document.title = "교실 모니터";
    const onFs = () => setIsFs(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", onFs);
    return () => { document.title = prev; document.removeEventListener("fullscreenchange", onFs); };
  }, []);
  const toggleFs = useCallback(async () => {
    try {
      if (!document.fullscreenElement) {
        await rootRef.current?.requestFullscreen?.({ navigationUI: "hide" });
        try { await screen.orientation?.lock?.("landscape"); } catch { /* 고정 불가 기기 */ }
      } else await document.exitFullscreen();
    } catch { /* 전체 화면 불가 */ }
  }, []);

  /* ── 조작 막대: 움직이면 잠깐 보이고 스스로 숨는다 ── */
  const idleT = useRef(0);
  const poke = useCallback(() => {
    setCtl(true);
    clearTimeout(idleT.current);
    idleT.current = setTimeout(() => { if (!S.current.list && !S.current.gal) setCtl(false); }, IDLE_MS);
  }, []);
  useEffect(() => { poke(); return () => clearTimeout(idleT.current); }, [poke]);
  useEffect(() => { if (!list && !gal) poke(); }, [list, gal, poke]);

  /* ── 키보드 (노트북에 띄울 때) — 액자 동안은 FrameStage 가 받는다 ── */
  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const k = e.key;
      if (k === "Escape") { setList(false); setGal(false); return; }
      if (S.current.view || S.current.gal) return;
      if (k === "ArrowRight") { goTo(stepIdx(S.current.idx, 1, S.current.grp)); poke(); }
      else if (k === "ArrowLeft") { goTo(stepIdx(S.current.idx, -1, S.current.grp)); poke(); }
      else if (k === " ") { e.preventDefault(); togglePause(); poke(); }
      else if (k === "e" || k === "E") flipMode("e");
      else if (k === "m" || k === "M") flipMode("m");
      else if (k === "t" || k === "T" || k === "Tab") { e.preventDefault(); flipMode(); }
      else if (k === "f" || k === "F") toggleFs();
      else if (k === "l" || k === "L") setList((v) => !v);
      else if (k === "ArrowUp" || k === "ArrowDown") {
        const c = (PAIRS[S.current.idx].controls || []).find((x) => x.kind === "step");
        if (c) { e.preventDefault(); stepParam(c, k === "ArrowUp" ? 1 : -1); poke(); }
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [goTo, flipMode, togglePause, toggleFs, poke, stepParam]);

  /* ── 묶음 고르기: 지금 장면이 그 묶음에 없으면 묶음의 첫 장면으로 ── */
  const pickGroup = (g) => {
    setGrp(g);
    const ord = orderOf(g);
    if (!ord.includes(S.current.idx)) goTo(ord[0]);
  };
  const card = (i) => {
    const p = PAIRS[i];
    return (
      <button key={p.key} type="button" className={"dsp-card" + (i === idx ? " on" : "")}
        onClick={() => { if (grp !== "all" && p.group !== grp) setGrp(p.group); goTo(i); setList(false); }}>
        <span className="n">{String(i + 1).padStart(2, "0")}</span>
        <span className="e">{p.title.e}</span>
        <span className="m">{p.title.m}</span>
      </button>
    );
  };

  /* ── 그릴 층 계산 ── */
  const now = performance.now();
  const C = PALETTE[thm];
  const pair = PAIRS[idx];
  const P = paramsOf(pair, prm);
  const dur = durOf(pair, P);
  const t = clamp(elapsed(now), 0, dur);
  const layers = [];
  const pf = pfade.current, mf = mfade.current;
  const kin = pf ? E.sine(clamp((now - pf.t0) / PAIR_FADE)) : 1;
  if (pf && kin < 1) layers.push({ key: "out", pair: PAIRS[pf.idx], mode: pf.mode, t: pf.t, o: 1 - kin, P: pf.P });
  if (mf) {
    const k = E.sine(clamp((now - mf.t0) / MODE_FADE));
    if (k < 1) layers.push({ key: "from-" + mf.from, pair, mode: mf.from, t, o: kin * (1 - k * k), P });
    layers.push({ key: "to-" + mode, pair, mode, t, o: kin * k, P });
  } else layers.push({ key: "cur-" + mode, pair, mode, t, o: kin, P });

  const toggleThm = () => { setThm((v) => (v === "dark" ? "light" : "dark")); poke(); };

  return (
    <div ref={rootRef} className={"dsp-root dsp-" + thm + (ctl ? "" : " dsp-idle")}
      onPointerMove={poke} onPointerDown={poke}>
      <style>{DSP_CSS}</style>
      <div className="dsp-frame">
        <div className="dsp-paper" />
        {view ? (
          <FrameStage key={view} fkey={view} C={C} ctl={ctl} poke={poke} isFs={isFs} toggleFs={toggleFs}
            onTheme={toggleThm} onGallery={() => setGal(true)} onExit={closeFrame} inert={gal} mode={mode} onMode={flipMode} />
        ) : (<>
        <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet"
          role="img" aria-label={`${pair.title[mode]} — 수학 애니메이션`}>
          {layers.map((L) => (
            <g key={L.key + "@" + L.pair.key} opacity={L.o}>
              <SceneTitle title={L.pair.title[L.mode]} sub={L.pair.sub[L.mode]} C={C} mode={L.mode} />
              {L.pair.render(L.mode, L.t, C, L.P || paramsOf(L.pair, prm))}
            </g>
          ))}
        </svg>

        {/* 오른쪽 위 — 액자 단추 · 학년 토글, 늘 보인다 */}
        <div className="dsp-tr">
          <button type="button" className="dsp-fbtn" title="액자" aria-label="액자" onClick={() => { setGal(true); poke(); }}>
            <FrameIc />
          </button>
          <div className={"dsp-mode on-" + mode} role="radiogroup" aria-label="학년">
            <span className="dsp-knob" aria-hidden="true" />
            <button type="button" role="radio" aria-checked={mode === "e"} onClick={() => { flipMode("e"); poke(); }}>초등</button>
            <button type="button" role="radio" aria-checked={mode === "m"} onClick={() => { flipMode("m"); poke(); }}>중등</button>
          </div>
        </div>

        {/* 조작 막대 */}
        <div className={"dsp-ctl" + (ctl ? " show" : "")} onPointerDown={(e) => e.stopPropagation()}>
          <Btn title="이전 장면 (←)" onClick={() => { goTo(stepIdx(idx, -1, grp)); poke(); }}><Ic d="M15 5 8 12l7 7M6 5v14" /></Btn>
          <Btn title={paused ? "재생 (스페이스)" : "멈춤 (스페이스)"} onClick={() => { togglePause(); poke(); }}>
            {paused ? <Ic d="M8 5v14l11-7z" fill /> : <Ic d="M8 5v14M16 5v14" />}
          </Btn>
          <Btn title="다음 장면 (→)" onClick={() => { goTo(stepIdx(idx, 1, grp)); poke(); }}><Ic d="m9 5 7 7-7 7M18 5v14" /></Btn>
          <span className="dsp-sep" />
          <Btn title="이 장면 반복" on={repeat} onClick={() => { setRepeat((v) => !v); poke(); }}>
            <Ic d="M17 2l3 3-3 3M4 11V9a4 4 0 0 1 4-4h12M7 22l-3-3 3-3M20 13v2a4 4 0 0 1-4 4H4" />
          </Btn>
          <Btn title="장면 목록 (L)" on={list} onClick={() => setList((v) => !v)}><Ic d="M4 6h16M4 12h16M4 18h16" /></Btn>
          <Btn title="밝기 바꾸기" onClick={toggleThm}>
            <Ic d="M12 3a9 9 0 1 0 0 18V3z" fill />
          </Btn>
          <Btn title={isFs ? "전체 화면 끝내기 (F)" : "전체 화면 (F)"} onClick={() => { toggleFs(); poke(); }}>
            {isFs ? <Ic d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /> : <Ic d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />}
          </Btn>
          <Btn title="나가기" onClick={() => { if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); location.hash = ""; }}>
            <Ic d="M6 6l12 12M18 6 6 18" />
          </Btn>
        </div>

        {/* 장면 설정 — 이 장면이 고를 것을 가지고 있을 때만 */}
        {pair.controls && (
          <div className={"dsp-pctl" + (ctl ? " show" : "")} onPointerDown={(e) => e.stopPropagation()}>
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

        {/* 진행 — 장면 점 + 지금 장면의 흐름 */}
        <div className="dsp-dots" aria-hidden="true">
          {orderOf(grp).map((i) => <i key={PAIRS[i].key} className={i === idx ? "on" : ""} />)}
        </div>
        <div className="dsp-prog" aria-hidden="true"><i style={{ transform: `scaleX(${t / dur})` }} /></div>
        {paused && <div className="dsp-paused">멈춤</div>}

        {list && (
          <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()}>
            <div className="dsp-list-in">
              <div className="dsp-list-h">
                <b>장면 목록</b>
                <button type="button" onClick={() => setList(false)} aria-label="닫기">✕</button>
              </div>
              <div className="dsp-chips" role="radiogroup" aria-label="돌릴 묶음">
                <span className="lb">돌릴 묶음</span>
                {GROUPS.map((g) => (
                  <button key={g.key} type="button" role="radio" aria-checked={grp === g.key}
                    className={"dsp-chip" + (grp === g.key ? " on" : "")} onClick={() => pickGroup(g.key)}>
                    {g.label}<small>{orderOf(g.key).length}</small>
                  </button>
                ))}
              </div>
              {GROUPS.filter((g) => g.key !== "all").map((g) => (
                <div key={g.key} className={"dsp-sec" + (grp !== "all" && grp !== g.key ? " off" : "")}>
                  <div className="dsp-sec-h">{g.label}</div>
                  <div className="dsp-grid">{orderOf(g.key).map(card)}</div>
                </div>
              ))}
            </div>
          </div>
        )}
        </>)}

        {gal && <FrameGallery C={C} mode={mode} view={view} onPick={openFrame} onClose={() => setGal(false)} onScenes={closeFrame} />}
      </div>
    </div>
  );
}

/* ══════════ 액자 목록 ══════════ */
const THUMB_TL = { hanoi: null };
function FrameGallery({ C, mode, view, onPick, onClose, onScenes }) {
  if (!THUMB_TL.hanoi) THUMB_TL.hanoi = hanoiTimeline(5, "fast");
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()}>
      <div className="dsp-list-in dsp-gal-in">
        <div className="dsp-list-h">
          <b>액자</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <p className="dsp-gal-sub">수업 장면과 따로, 오래 켜 두는 그림 · 실험 · 이야기예요. 고르면 바로 돌기 시작해요.</p>
        <div className="dsp-gal">
          {FRAMES.map((f) => (
            <button key={f.key} type="button" className={"dsp-fcard" + (view === f.key ? " on" : "")} onClick={() => onPick(f.key)}>
              <svg viewBox={`0 150 ${W} 700`} aria-hidden="true">
                {f.key === "hanoi" && <HanoiThumb C={C} TL={THUMB_TL.hanoi} />}
                {f.story && <StoryThumb fkey={f.key} C={C} mode={mode} />}
                {f.key === "monty" && <MontyThumb C={C} mode={mode} />}
                {f.key === "branch" && <BranchThumb C={C} mode={mode} />}
                {f.key === "galton" && <GaltonThumb C={C} mode={mode} />}
              </svg>
              <span className="k">{f.lab ? "실험" : f.story ? "장면 묶음" : "그림"}</span>
              <span className="t">{f.title}{view === f.key && <small>지금 켜 둔 액자</small>}</span>
              <span className="d">{f.desc}</span>
            </button>
          ))}
        </div>
        {view && (
          <div className="dsp-gal-foot">
            <button type="button" className="dsp-chip" onClick={onScenes}>← 수업 장면으로 돌아가기</button>
          </div>
        )}
      </div>
    </div>
  );
}

/* ══════════ 액자 무대 ══════════ */
const UI = { Btn, Ic, FrameIc };
const LABS = { monty: MontyFrame, branch: BranchFrame, galton: GaltonFrame };
function FrameStage({ fkey, ...rest }) {
  if (fkey === "hanoi") return <HanoiFrame {...rest} />;
  if (LABS[fkey]) { const Lab = LABS[fkey]; return <Lab ui={UI} {...rest} />; }
  if (FRAMES.some((f) => f.key === fkey && f.story)) return <StoryFrame fkey={fkey} ui={UI} {...rest} />;
  return null;
}

/** 저장된 하노이 상태: 원판 수 · 빠르기 · 시작 시각(벽시계 ms) · 멈춘 경과 */
function loadHanoi() {
  try {
    const o = JSON.parse(localStorage.getItem(LS.hanoi) || "null");
    if (o && Number.isInteger(o.n) && o.n >= HANOI.MIN && o.n <= HANOI.MAX && (o.sp === "fast" || o.sp === "natural")
      && Number.isFinite(o.t0) && o.t0 <= Date.now()) {
      return { n: o.n, sp: o.sp, t0: o.t0, held: Number.isFinite(o.held) && o.held >= 0 ? o.held : null };
    }
  } catch { /* 처음이거나 망가진 값 */ }
  return { n: HANOI.DEF, sp: "fast", t0: Date.now(), held: null };
}

/**
 * 하노이의 탑 액자 — 끝없이 옮긴다(A → C, 쉬고, C → A …).
 * 시계는 벽시계(Date.now)라 새로고침·잠깐 나갔다 와도 그 자리에서 이어진다. 원판 수를 바꾸면 처음부터,
 * 빠르기를 바꾸면 지금 옮기던 그 이동의 같은 진행 비율에서 이어진다.
 */
function HanoiFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert }) {
  const init = useRef(null);
  if (!init.current) init.current = loadHanoi();
  const [n, setN] = useState(init.current.n);
  const [sp, setSp] = useState(init.current.sp);
  const [paused, setPaused] = useState(init.current.held != null);
  const clk = useRef({ t0: init.current.t0, held: init.current.held });
  const [, setFrame] = useState(0);
  const TLs = useMemo(() => ({ fast: hanoiTimeline(n, "fast"), natural: hanoiTimeline(n, "natural") }), [n]);
  const TL = TLs[sp];
  const R = useRef({});
  R.current = { n, sp, TLs, inert };

  const save = (nn, ss) => lsSet(LS.hanoi, JSON.stringify({ n: nn, sp: ss, t0: clk.current.t0, held: clk.current.held }));
  useEffect(() => { save(n, sp); }, []);   // eslint-disable-line react-hooks/exhaustive-deps
  const elapsedNow = () => (clk.current.held != null ? clk.current.held : Date.now() - clk.current.t0);

  const togglePause = useCallback(() => {
    const now = Date.now(), c = clk.current;
    if (c.held != null) { clk.current = { t0: now - c.held, held: null }; setPaused(false); }
    else { clk.current = { t0: c.t0, held: now - c.t0 }; setPaused(true); }
    save(R.current.n, R.current.sp);
  }, []);   // eslint-disable-line react-hooks/exhaustive-deps
  const restart = useCallback(() => {
    clk.current = { t0: Date.now(), held: clk.current.held != null ? 0 : null };
    save(R.current.n, R.current.sp); setFrame((f) => f + 1);
  }, []);   // eslint-disable-line react-hooks/exhaustive-deps
  const setDisks = useCallback((k) => {
    const nn = clamp(k, HANOI.MIN, HANOI.MAX);
    if (nn === R.current.n) return;
    clk.current = { t0: Date.now(), held: clk.current.held != null ? 0 : null };
    setN(nn); save(nn, R.current.sp);
  }, []);   // eslint-disable-line react-hooks/exhaustive-deps
  const setSpeed = useCallback((s2) => {
    const { sp: s1, TLs: T, n: nn } = R.current;
    if (s2 === s1) return;
    const now = Date.now(), c = clk.current;
    const e2 = remapElapsed(T[s1], T[s2], c.held != null ? c.held : now - c.t0);
    clk.current = c.held != null ? { t0: c.t0, held: e2 } : { t0: now - e2, held: null };
    setSp(s2); save(nn, s2);
  }, []);   // eslint-disable-line react-hooks/exhaustive-deps

  /* ── 그리기 루프 (최대 40fps, 멈추면 쉰다) ── */
  useEffect(() => {
    let raf = 0, last = 0;
    const loop = (now) => {
      raf = requestAnimationFrame(loop);
      if (now - last < FRAME_MS || clk.current.held != null) return;
      last = now;
      setFrame((f) => (f + 1) % 1e9);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, []);

  /* ── 키보드 ── */
  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey || R.current.inert) return;
      const k = e.key;
      if (k === " ") { e.preventDefault(); togglePause(); poke(); }
      else if (k === "ArrowUp" || k === "+" || k === "=") { e.preventDefault(); setDisks(R.current.n + 1); poke(); }
      else if (k === "ArrowDown" || k === "-" || k === "_") { e.preventDefault(); setDisks(R.current.n - 1); poke(); }
      else if (k === "s" || k === "S") { setSpeed(R.current.sp === "fast" ? "natural" : "fast"); poke(); }
      else if (k === "r" || k === "R") { restart(); poke(); }
      else if (k === "f" || k === "F") toggleFs();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [togglePause, setDisks, setSpeed, restart, toggleFs, poke]);

  const st = hanoiAt(TL, elapsedNow());
  const prog = st.hold != null ? 1 : st.tau / TL.total;
  const total = { fast: TLs.fast.total, natural: TLs.natural.total };
  const stop = (e) => e.stopPropagation();

  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet"
        role="img" aria-label={`하노이의 탑 — 원판 ${n}개`}>
        <HanoiArt L={TL.L} st={st} C={C} uid="hnf" info={{ total: TL.total, speed: sp }} />
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
        <div className="dsp-seg" role="radiogroup" aria-label="빠르기">
          <button type="button" role="radio" aria-checked={sp === "natural"} onClick={() => { setSpeed("natural"); poke(); }}>자연스럽게</button>
          <button type="button" role="radio" aria-checked={sp === "fast"} onClick={() => { setSpeed("fast"); poke(); }}>빠르게</button>
        </div>
        <span className="dsp-sep" />
        <Btn title="밝기 바꾸기" onClick={onTheme}><Ic d="M12 3a9 9 0 1 0 0 18V3z" fill /></Btn>
        <Btn title={isFs ? "전체 화면 끝내기 (F)" : "전체 화면 (F)"} onClick={() => { toggleFs(); poke(); }}>
          {isFs ? <Ic d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /> : <Ic d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />}
        </Btn>
        <Btn title="액자 목록" onClick={() => { onGallery(); poke(); }}><FrameIc /></Btn>
        <Btn title="수업 장면으로" onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn>
      </div>
      <div className={"dsp-hint" + (ctl ? " show" : "")} aria-hidden={!ctl}>
        원판 {n}개 → {comma(TL.moves)}번 · 빠르게 <b className={sp === "fast" ? "on" : ""}>{fmtDur(total.fast)}</b>
        {" · "}자연스럽게 <b className={sp === "natural" ? "on" : ""}>{fmtDur(total.natural)}</b>
      </div>

      <div className="dsp-prog" aria-hidden="true"><i style={{ transform: `scaleX(${prog})` }} /></div>
      {paused && <div className="dsp-paused fr">멈춤</div>}
    </>
  );
}

function Btn({ title, on, onClick, disabled, children }) {
  return (
    <button type="button" className={"dsp-btn" + (on ? " on" : "")} title={title} aria-label={title} disabled={disabled}
      aria-pressed={on === undefined ? undefined : !!on} onClick={onClick}>{children}</button>
  );
}
/** 액자 모양(못에 걸린 그림틀 · 산과 해) */
function FrameIc() {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth={1.9}
      strokeLinecap="round" strokeLinejoin="round">
      <path d="M8.6 7.2 12 3.6l3.4 3.6" />
      <circle cx="12" cy="3.4" r="0.9" fill="currentColor" stroke="none" />
      <rect x="3.2" y="7.2" width="17.6" height="13.4" rx="1.6" />
      <path d="M6.2 17.6l3.6-4.4 2.6 2.7 1.9-1.9 3.5 3.6" />
      <circle cx="15.6" cy="11" r="1.35" />
    </svg>
  );
}
function Ic({ d, fill }) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" aria-hidden="true">
      <path d={d} fill={fill ? "currentColor" : "none"} stroke="currentColor" strokeWidth={fill ? 0 : 2.2}
        strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

const NOISE = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E\")";
const DSP_CSS = `
@font-face { font-family: "EBS Hunminjeongeum Saeron"; font-weight: 400; font-display: swap;
  src: url("/fonts/EBSHunminjeongeumSaeronR.woff2") format("woff2"), url("/fonts/EBSHunminjeongeumSaeronR.ttf") format("truetype"); }
.dsp-root { position: fixed; inset: 0; z-index: 200; display: flex; align-items: center; justify-content: center;
  overflow: hidden; -webkit-user-select: none; user-select: none; touch-action: manipulation;
  font-family: 'Pretendard Variable', Pretendard, system-ui, sans-serif; }
.dsp-dark { background: #121a33; --ink: #F2E8D0; --soft: #B8B0A0; --chip: rgba(10,15,32,.62); --chipbd: rgba(242,232,208,.22);
  --e: #F2877B; --m: #6BD3C3; --gold: #F4C65A; --card: #1c2647; }
.dsp-light { background: #e9dec3; --ink: #3B3021; --soft: #7B6C55; --chip: rgba(255,251,241,.78); --chipbd: rgba(59,48,33,.22);
  --e: #C34E3E; --m: #13877A; --gold: #B37A0E; --card: #f6efdf; }
.dsp-idle { cursor: none; }
.dsp-frame { position: relative; width: min(100vw, calc(100vh * 16 / 9)); aspect-ratio: 16 / 9; container-type: inline-size; }
.dsp-paper { position: absolute; inset: -40vmax; pointer-events: none; }
.dsp-dark .dsp-paper { background: radial-gradient(70% 70% at 50% 40%, #2a3762 0%, #1c2647 55%, #121a33 100%); }
.dsp-light .dsp-paper { background: radial-gradient(70% 70% at 50% 35%, #fcf8ee 0%, #f3ead6 55%, #e6d9bb 100%); }
.dsp-paper::after { content: ""; position: absolute; inset: 0; opacity: .06; mix-blend-mode: overlay; background-image: ${NOISE}; }
.dsp-svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; overflow: visible; }
.dsp-svg text { font-kerning: normal; }

/* 오른쪽 위: 액자 단추 + 학년 토글 */
.dsp-tr { position: absolute; right: 2.6cqw; top: 2.4cqw; display: flex; align-items: center; gap: .9cqw; z-index: 5; }
.dsp-fbtn { width: 4.3cqw; height: 4.3cqw; padding: 0; border-radius: 999px; border: 1px solid var(--chipbd); background: var(--chip);
  color: var(--ink); display: grid; place-items: center; font-size: 2.15cqw; cursor: pointer; -webkit-tap-highlight-color: transparent;
  transition: color .25s, border-color .25s; }
.dsp-fbtn:hover { color: var(--gold); border-color: var(--gold); }

/* 학년 토글 */
.dsp-mode { position: relative; display: flex; background: var(--chip);
  border: 1px solid var(--chipbd); border-radius: 999px; padding: .35cqw; }
.dsp-mode button { position: relative; z-index: 1; border: 0; background: none; color: var(--soft); cursor: pointer;
  font: inherit; font-size: 1.62cqw; font-weight: 800; letter-spacing: .04em; padding: .62cqw 1.75cqw; border-radius: 999px;
  -webkit-tap-highlight-color: transparent; transition: color .35s; min-width: 7.2cqw; }
.dsp-mode button[aria-checked="true"] { color: #fff; }
.dsp-light .dsp-mode button[aria-checked="true"] { color: #fffdf6; }
.dsp-knob { position: absolute; top: .35cqw; bottom: .35cqw; left: .35cqw; width: calc(50% - .35cqw); border-radius: 999px;
  background: var(--e); transition: transform .45s cubic-bezier(.65,0,.35,1), background .45s; }
.dsp-mode.on-m .dsp-knob { transform: translateX(100%); background: var(--m); }

/* 조작 막대 */
.dsp-ctl { position: absolute; left: 50%; top: 2.4cqw; transform: translate(-50%, -.6cqw); display: flex; align-items: center;
  gap: .5cqw; padding: .45cqw .7cqw; border-radius: 999px; background: var(--chip); border: 1px solid var(--chipbd);
  opacity: 0; pointer-events: none; transition: opacity .3s, transform .3s; z-index: 6; }
.dsp-ctl.show { opacity: 1; pointer-events: auto; transform: translate(-50%, 0); }
.dsp-btn { width: 3.5cqw; height: 3.5cqw; border-radius: 999px; border: 0; background: none; color: var(--ink);
  font-size: 1.65cqw; display: grid; place-items: center; cursor: pointer; -webkit-tap-highlight-color: transparent; }
.dsp-btn:hover { background: rgba(127,127,127,.16); }
.dsp-btn.on { color: var(--gold); background: rgba(127,127,127,.14); }
.dsp-btn:disabled { opacity: .28; cursor: default; background: none; }
.dsp-sep { width: 1px; height: 2.2cqw; background: var(--chipbd); margin: 0 .3cqw; }

/* 액자 조작: 원판 수 · 빠르기 · 걸리는 시간 */
.dsp-num { display: inline-flex; flex-direction: column; align-items: center; min-width: 3.3cqw; line-height: 1; color: var(--ink); }
.dsp-num b { font-size: 1.9cqw; font-weight: 800; font-variant-numeric: tabular-nums; }
.dsp-num small { font-size: .8cqw; color: var(--soft); font-weight: 700; margin-top: .28cqw; }
.dsp-seg { display: flex; border: 1px solid var(--chipbd); border-radius: 999px; padding: .25cqw; gap: .2cqw; }
.dsp-seg button { border: 0; background: none; color: var(--soft); font: inherit; font-size: 1.2cqw; font-weight: 800; cursor: pointer; white-space: nowrap;
  padding: .55cqw 1.1cqw; border-radius: 999px; -webkit-tap-highlight-color: transparent; transition: background .25s, color .25s; }
.dsp-seg button[aria-checked="true"] { background: var(--gold); color: #1c2647; }
.dsp-light .dsp-seg button[aria-checked="true"] { color: #fffdf6; }
.dsp-hint { position: absolute; left: 50%; top: 7.5cqw; transform: translate(-50%, -.5cqw); z-index: 6; white-space: nowrap;
  font-size: 1.08cqw; font-weight: 600; color: var(--soft); background: var(--chip); border: 1px solid var(--chipbd);
  border-radius: 999px; padding: .42cqw 1.25cqw; opacity: 0; pointer-events: none; transition: opacity .3s, transform .3s; }
.dsp-hint.show { opacity: 1; transform: translate(-50%, 0); }
.dsp-hint b { color: var(--ink); font-weight: 800; }
.dsp-hint b.on { color: var(--gold); }

/* 장면 설정 칩 — 조작 막대 아래 */
.dsp-pctl { position: absolute; left: 50%; top: 7.5cqw; transform: translate(-50%, -.5cqw); display: flex; align-items: center;
  gap: .4cqw; padding: .35cqw .8cqw; border-radius: 999px; background: var(--chip); border: 1px solid var(--chipbd);
  opacity: 0; pointer-events: none; transition: opacity .3s, transform .3s; z-index: 6; white-space: nowrap; }
.dsp-pctl.show { opacity: 1; pointer-events: auto; transform: translate(-50%, 0); }
.dsp-pc { display: flex; align-items: center; gap: .35cqw; }
.dsp-pc .lb { font-size: 1.1cqw; font-weight: 800; color: var(--soft); margin: 0 .3cqw 0 .2cqw; }
.dsp-pctl .dsp-num { min-width: 4.6cqw; }

/* 진행 */
.dsp-dots { position: absolute; right: 2.8cqw; bottom: 1.6cqw; display: flex; gap: .55cqw; opacity: .55; }
.dsp-dots i { width: .5cqw; height: .5cqw; border-radius: 999px; background: var(--soft); }
.dsp-dots i.on { background: var(--gold); width: 1.4cqw; }
.dsp-prog { position: absolute; left: 0; right: 0; bottom: 0; height: .22cqw; opacity: .45; }
.dsp-prog i { display: block; height: 100%; background: var(--gold); transform-origin: 0 50%; }
.dsp-paused { position: absolute; left: 50%; bottom: 7.4cqw; transform: translateX(-50%); font-size: 1.25cqw; font-weight: 800;
  color: var(--ink); background: var(--chip); border: 1px solid var(--chipbd); border-radius: 999px; padding: .3cqw 1.1cqw; }
.dsp-paused.fr { left: 3.4cqw; top: 3cqw; bottom: auto; transform: none; }   /* 액자: 받침 글자를 가리지 않게 왼쪽 위 */
.dsp-paused.lab { left: auto; right: 2.8cqw; bottom: 2.6cqw; transform: none; }   /* 실험 액자: 기록·자막을 가리지 않게 오른쪽 아래 */

/* 장면 목록 */
.dsp-list { position: absolute; inset: 0; z-index: 8; display: grid; place-items: center; background: rgba(0,0,0,.35);
  backdrop-filter: blur(3px); -webkit-backdrop-filter: blur(3px); }
.dsp-list-in { width: 78cqw; max-height: 86%; overflow: auto; background: var(--card); color: var(--ink); border-radius: 1.6cqw;
  border: 1px solid var(--chipbd); padding: 1.6cqw 1.8cqw; box-shadow: 0 2cqw 5cqw rgba(0,0,0,.35); }
.dsp-list-h { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2cqw; font-size: 1.7cqw; }
.dsp-list-h button { border: 0; background: none; color: var(--soft); font-size: 1.7cqw; cursor: pointer; }
.dsp-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: .9cqw; }
.dsp-chips { display: flex; align-items: center; gap: .6cqw; margin-bottom: 1.1cqw; flex-wrap: wrap; }
.dsp-chips .lb { font-size: 1.2cqw; color: var(--soft); font-weight: 700; margin-right: .4cqw; }
.dsp-chip { border: 1px solid var(--chipbd); background: transparent; color: var(--ink); border-radius: 999px; cursor: pointer;
  font: inherit; font-size: 1.25cqw; font-weight: 700; padding: .45cqw 1.1cqw; -webkit-tap-highlight-color: transparent; }
.dsp-chip small { font-size: .95cqw; color: var(--soft); margin-left: .45cqw; font-weight: 600; }
.dsp-chip.on { border-color: var(--gold); color: var(--gold); box-shadow: inset 0 0 0 1px var(--gold); }
.dsp-chip.on small { color: var(--gold); }
.dsp-sec { margin-top: 1.1cqw; transition: opacity .25s; }
.dsp-sec.off { opacity: .42; }
.dsp-sec-h { font-size: 1.15cqw; font-weight: 800; color: var(--soft); margin: 0 0 .6cqw .2cqw; letter-spacing: .02em; }
.dsp-card { text-align: left; border: 1px solid var(--chipbd); border-radius: 1cqw; background: transparent; color: var(--ink);
  padding: .9cqw 1.1cqw; cursor: pointer; display: grid; grid-template-columns: auto 1fr; column-gap: .9cqw; row-gap: .15cqw;
  font: inherit; -webkit-tap-highlight-color: transparent; }
.dsp-card.on { border-color: var(--gold); box-shadow: inset 0 0 0 1px var(--gold); }
.dsp-card .n { grid-row: span 2; font-size: 1.5cqw; font-weight: 800; color: var(--gold); align-self: center; }
.dsp-card .e { font-size: 1.25cqw; font-weight: 700; color: var(--e); }
.dsp-card .m { font-size: 1.25cqw; font-weight: 700; color: var(--m); }

/* 액자 목록 */
.dsp-gal-in { width: 84cqw; max-height: 94%; padding-bottom: 1.2cqw; }
.dsp-gal-sub { margin: -.4cqw 0 1.2cqw .1cqw; font-size: 1.15cqw; color: var(--soft); }
.dsp-gal { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.1cqw; }
.dsp-fcard { text-align: left; border: 1px solid var(--chipbd); border-radius: 1.2cqw; background: transparent; color: var(--ink);
  padding: 0 0 1.1cqw; cursor: pointer; overflow: hidden; display: flex; flex-direction: column; gap: .4cqw; font: inherit;
  -webkit-tap-highlight-color: transparent; transition: border-color .25s, box-shadow .25s; }
.dsp-fcard svg { width: 100%; aspect-ratio: 1600 / 700; display: block; background: rgba(127,127,127,.09); border-bottom: 1px solid var(--chipbd); }
.dsp-fcard .t { padding: .6cqw 1.1cqw 0; font-size: 1.4cqw; font-weight: 800; display: flex; align-items: baseline; flex-wrap: wrap; column-gap: .7cqw; }
.dsp-fcard .t small { font-size: .9cqw; color: var(--gold); font-weight: 700; }
.dsp-fcard .d { padding: 0 1.1cqw; font-size: 1.02cqw; color: var(--soft); line-height: 1.45;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.dsp-fcard .k { margin: 0 1.1cqw; align-self: flex-start; font-size: .82cqw; font-weight: 800; letter-spacing: .04em; color: var(--soft);
  border: 1px solid var(--chipbd); border-radius: 999px; padding: .12cqw .6cqw; }
.dsp-fcard:hover, .dsp-fcard.on { border-color: var(--gold); box-shadow: inset 0 0 0 1px var(--gold); }
.dsp-gal-foot { margin-top: 1.2cqw; display: flex; justify-content: flex-end; }
`;
