// 관리자 — 교실 모니터 (#/admin/display)
// 가로 화면에 도형 애니메이션을 자동으로 돌린다(공간 감각 기르기). 오른쪽 위 「초등 | 중등」 토글을 누르면
// 지금 장면이 짝이 되는 장면으로 같은 시각에 겹쳐 넘어간다 — 두 판은 같은 박자표를 쓰도록 저작되어 있다.
// 장면 목록: src/features/display/pairs.js · 엔진: core.js(계산) + draw.jsx(그리기)
// 화면은 탭·마우스 움직임에 조작 막대가 잠깐 뜨고 스스로 숨는다. 전체 화면·화면 꺼짐 방지 포함.
// 액자: 토글 왼쪽의 액자 단추 → 액자 목록 → 고르면 수업 장면 대신 그 액자가 계속 돈다. 액자는 벽시계로 흘러서 새로고침해도
//       이어진다. 목록: src/features/display/frames/index.js
//       · 하노이의 탑(frames/hanoiframe.jsx · hanoi.jsx(2D) · hanoi3d/(3D, three.js 는 입체로 볼 때만) · hanoi.js) — 원판 3~30 · 기둥 3~5 ·
//         세트 1~5(5세트는 로봇 다섯 대) · 자연스럽게 | 1~4배속(4배속은 파티)
//       · 해설 액자 — 일차함수 그래프 그리기 해설(frames/graphdraw.jsx · graphdraw.js): 학원 프린트 기본 96제 · 심화 64제를
//         한 문항씩 풀이 순서(네모 칸)대로 점 찍기 → 칸 세며 옮기기 → 직선으로 그린다. 기본 | 심화 · 1× | 1.5× · 번호 목록(L).
//         · 일차함수 10단계 계산 해설(frames/lin10.jsx · lin10.js): 프린트 세트 1 · 2(200문항씩)의 계산 과정을 한 줄씩 판서로.
//         세트 1 | 세트 2 · 1× | 1.5× · 번호 · 단계 목록(L — 단계를 고르면 그 단계만).
//         · 일차함수 그래프와 넓이 해설(frames/area.jsx · area.js): 프린트 100제 · 240제를 풀이 줄마다 그림(밑변 · 높이 · 조각)과 함께.
//         · 경우의 수와 확률 100제 해설(frames/cnt100.jsx · cnt100.js): 프린트 학년별 선발 · 주머니 공 100제를 같은 판서 재생기로.
//         학년별 선발 | 주머니 공 · 1× | 1.5× · 번호 · 단계 목록(L).
//       · 실험 액자 — 몬티홀 · 갈림길과 구슬 · 구슬 낙하 실험(frames/monty.jsx · branchlab.jsx · galtonlab.jsx, 공용 frames/xkit.jsx).
//         교육과정에 딱 맞기보다 융합·탐구에 가까워 수업 장면 순환에서 빼고, 직접 해 보는 것을 먼저 보여 준다.
//         「풀이 보기」를 고르면 예전 설명 장면(몬티홀·찍기 · 갈림길·구슬 · 정규분포)을 그대로 돌린다.
//       · 장면 묶음 — 숫자로 읽는 축구 · 서술형 이야기(stories.js · frames/story.jsx): 여러 단원을 섞는 융합 장면.
//       · 수학 호기심 일곱(frames/curio.jsx) — 축구 · 농구 · 야구 실제 기록으로 그리는 직선, 주머니 공 꺼내기, 알파벳 카드 사전식 배열,
//         일렬로 세우기, 북적북적 학년별 뽑기. 실험 액자와 같은 조작 막대(xkit)를 쓰고, 큰 자료는 열 때 늦게 들여온다.
//         축구 여섯 장면은 「2D | 3D」 토글로 경기장 속 눈높이의 3D 시뮬레이션으로도 본다(frames/player.jsx · sim3d/ — three.js 는 3D 를 켤 때만).
// 학생앱 「시청각 학습」(#/av/<key> — pages/AvPlayer.jsx · lib/av.js): 같은 Stage 를 av 모드로 연다 — 관리자 확인 없이,
//       처음부터 그 액자(또는 그 묶음의 수업 장면)로. 액자 목록은 그 범주(수학 호기심 · 문제 풀이 해설)의 항목만, 나가기는 공부하기 목록으로.
// 장면 설정: 장면이 controls(구슬 수·단계·문 개수 …)를 가지면 조작 막대 아래에 설정 칩이 뜬다. 바꾸면 그 장면을
//       처음부터 다시 튼다. 장면마다 기기에 기억한다. 장면은 render(mode, t, C, P) 의 P 로 설정을 받는다.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { PAIRS, GROUPS } from "../features/display/pairs";
import { PALETTE, W, H, SceneTitle, clearMeasureCache } from "../features/display/draw";
import { E, clamp } from "../features/display/core";
import { FRAMES } from "../features/display/frames/index.js";
import { paramsOf, durOf, optVal } from "../features/display/params.js";
import { HanoiThumb } from "../features/display/frames/hanoi.jsx";
import { HanoiFrame } from "../features/display/frames/hanoiframe.jsx";
import { StoryFrame, StoryThumb } from "../features/display/frames/story.jsx";
import { MontyFrame, MontyThumb } from "../features/display/frames/monty.jsx";
import { BranchFrame, BranchThumb } from "../features/display/frames/branchlab.jsx";
import { GaltonFrame, GaltonThumb } from "../features/display/frames/galtonlab.jsx";
import { GraphFrame, GraphThumb } from "../features/display/frames/graphdraw.jsx";
import { Lin10Frame, Lin10Thumb } from "../features/display/frames/lin10.jsx";
import { AreaFrame, AreaThumb } from "../features/display/frames/area.jsx";
import { Cnt100Frame, Cnt100Thumb } from "../features/display/frames/cnt100.jsx";
import { Lin2Frame, Lin2Thumb, MeetFrame, MeetThumb } from "../features/display/frames/prints.jsx";
import { hanoiTimeline } from "../features/display/hanoi";
import { CURIO_LABS, CurioThumb } from "../features/display/frames/curio.jsx";
import { BASIC_LABS, BasicsThumb } from "../features/display/frames/basics.jsx";
import "../features/display/frames/allspec.jsx";        // 듀얼 모드 판마다 「문제 풀이 해설 전부」에서 고르기(frames/lesson.jsx 에 넣어 둔다)
import { DSP_CSS, Btn, Ic, FrameIc } from "../features/display/stage-ui.jsx";
import { avOfCat, printSeen } from "../lib/av.js";

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

/** av: null(교실 모니터) | { key, cat, frame, grp, title } — 학생앱 시청각 학습(AvPlayer) */
export function Stage({ av = null }) {
  const [mode, setMode] = useState(() => (lsGet(LS.mode, "e") === "m" ? "m" : "e"));
  const [idx, setIdx] = useState(() => {
    const n = Number(lsGet(LS.idx, 0));
    const ok = Number.isInteger(n) && n >= 0 && n < PAIRS.length ? n : 0;
    if (av?.grp && av.grp !== "all" && PAIRS[ok]?.group !== av.grp) return Math.max(0, PAIRS.findIndex((p) => p.group === av.grp));
    return ok;
  });
  const [thm, setThm] = useState(() => (lsGet(LS.theme, "dark") === "light" ? "light" : "dark"));
  const [grp, setGrp] = useState(() => {
    if (av) return av.grp && GROUPS.some((x) => x.key === av.grp) ? av.grp : "all";
    const g = lsGet(LS.grp, "all"); return GROUPS.some((x) => x.key === g) ? g : "all";
  });
  const [paused, setPaused] = useState(false);
  const [repeat, setRepeat] = useState(() => lsGet(LS.rep, "0") === "1");
  const [ctl, setCtl] = useState(true);
  const [list, setList] = useState(false);
  const [gal, setGal] = useState(false);       // 액자 목록
  const [view, setView] = useState(() => (av ? (av.frame && FRAMES.some((f) => f.key === av.frame) ? av.frame : null)
    : FRAMES.some((f) => f.key === lsGet(LS.view, "")) ? lsGet(LS.view, "") : null));   // null = 수업 장면
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
  useEffect(() => { if (!av) lsSet(LS.grp, grp); }, [grp, av]);
  useEffect(() => { if (!av) lsSet(LS.view, view || ""); }, [view, av]);
  const avExit = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    location.hash = av?.back || `#/study/av/${av?.cat || ""}`;      // 학교별 모의고사 등에서 왔으면 그곳으로(AvPlayer 의 ?from=)
  }, [av]);
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
    if (av) { avExit(); return; }
    if (S.current.view && sceneHold.current && !sceneHold.current.wasPaused && clk.current.held != null) {
      clk.current = { start: performance.now() - clk.current.held, held: null };
    }
    sceneHold.current = null;
    setView(null);
  }, [av, avExit]);

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
    document.title = av ? `${av.title} — 시청각 학습` : "교실 모니터";
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
  // 학생앱에서 연 시그니처 프린트(av.sig) — 본 기록을 프린트 key(「액자:세트」)로(lib/av.js 의 printSeen).
  // 기본기 단원 · 회차는 기본기 액자가 따로 남긴다(그 액자에는 onSeen 을 넘기지 않는다 — 넘기면 액자 것을 덮는다).
  const sigFk = av?.sig ? av.frame : null;
  const sigSeen = useMemo(() => (sigFk ? printSeen(sigFk) : null), [sigFk]);

  return (
    <div ref={rootRef} className={"dsp-root dsp-" + thm + (ctl ? "" : " dsp-idle")}
      onPointerMove={poke} onPointerDown={poke}>
      <style>{DSP_CSS}</style>
      {av && <style>{AV_ROT_CSS}</style>}
      {av && <div className="av-rot" aria-hidden="true">가로로 돌리면 크게 보여요</div>}
      <div className="dsp-frame">
        <div className="dsp-paper" />
        {view ? (
          <FrameStage key={view} fkey={view} pick={av?.frame === view ? av.set : null} C={C} ctl={ctl} poke={poke} isFs={isFs} toggleFs={toggleFs}
            onTheme={toggleThm} onGallery={() => setGal(true)} onExit={closeFrame} inert={gal} mode={mode} onMode={flipMode}
            {...(sigSeen && sigFk === view ? { onSeen: sigSeen } : {})} />
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
          <Btn title="나가기" onClick={() => { if (av) { avExit(); return; } if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); location.hash = ""; }}>
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

        {gal && !av && <FrameGallery C={C} mode={mode} view={view} onPick={openFrame} onClose={() => setGal(false)} onScenes={closeFrame} />}
        {gal && av && <AvGallery C={C} mode={mode} av={av} onClose={() => setGal(false)} onExit={avExit} />}
      </div>
    </div>
  );
}

/* ══════════ 액자 목록 ══════════ */
const THUMB_TL = { hanoi: null };
function FrameGallery({ C, mode, view, onPick, onClose, onScenes }) {
  if (!THUMB_TL.hanoi) THUMB_TL.hanoi = hanoiTimeline(5, "x1");
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
                {f.key === "graph" && <GraphThumb C={C} />}
                {f.key === "lin10" && <Lin10Thumb C={C} />}
                {f.key === "area" && <AreaThumb C={C} />}
                {f.key === "lin2" && <Lin2Thumb C={C} />}
                {f.key === "meet" && <MeetThumb C={C} />}
                {f.key === "cnt100" && <Cnt100Thumb C={C} />}
                {BASIC_LABS[f.key] && <BasicsThumb fkey={f.key} C={C} />}
                {CURIO_LABS[f.key] && <CurioThumb fkey={f.key} C={C} mode={mode} />}
              </svg>
              <span className="k">{f.lab ? "실험" : f.story ? "장면 묶음" : f.lesson ? "해설" : "그림"}</span>
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

/* ══════════ 시청각 학습(av) — 같은 범주의 항목만 ══════════ */
const AV_ROT_CSS = `.av-rot { position: absolute; left: 50%; bottom: max(18px, env(safe-area-inset-bottom)); transform: translateX(-50%); z-index: 4;
  display: none; white-space: nowrap; font-size: 13px; font-weight: 700; color: var(--soft); background: var(--chip); border: 1px solid var(--chipbd);
  border-radius: 999px; padding: 6px 14px; pointer-events: none; }
@media (orientation: portrait) and (max-width: 900px) { .av-rot { display: block; } }`;
function AvGallery({ C, mode, av, onClose, onExit }) {
  if (!THUMB_TL.hanoi) THUMB_TL.hanoi = hanoiTimeline(5, "fast");
  const items = av.level && av.cat === "sol" ? avOfCat(av.cat).filter((x) => x.level === av.level) : avOfCat(av.cat);
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()}>
      <div className="dsp-list-in dsp-gal-in">
        <div className="dsp-list-h">
          <b>{av.catTitle || "시청각 학습"}</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <p className="dsp-gal-sub">고르면 바로 돌기 시작해요.</p>
        <div className="dsp-gal">
          {items.map((it) => {
            const f = it.frame && !it.set ? FRAMES.find((x) => x.key === it.frame) : null;      // 유형별 문제 세트(기본기 단원 · 시그니처 프린트 — it.set)는 아이콘만
            return (
              <button key={it.key} type="button" className={"dsp-fcard" + (av.key === it.key ? " on" : "")}
                onClick={() => { if (it.key === av.key) onClose(); else location.hash = `#/av/${it.key}`; }}>
                <svg viewBox={`0 150 ${W} 700`} aria-hidden="true">
                  {it.key === "hanoi" && <HanoiThumb C={C} TL={THUMB_TL.hanoi} />}
                  {f?.story && <StoryThumb fkey={f.key} C={C} mode={mode} />}
                  {it.key === "monty" && <MontyThumb C={C} mode={mode} />}
                  {it.key === "branch" && <BranchThumb C={C} mode={mode} />}
                  {it.key === "galton" && <GaltonThumb C={C} mode={mode} />}
                  {it.key === "graph" && <GraphThumb C={C} />}
                  {it.key === "lin10" && <Lin10Thumb C={C} />}
                  {it.key === "area" && <AreaThumb C={C} />}
                  {it.key === "lin2" && <Lin2Thumb C={C} />}
                  {it.key === "meet" && <MeetThumb C={C} />}
                  {it.key === "cnt100" && <Cnt100Thumb C={C} />}
                  {CURIO_LABS[it.key] && <CurioThumb fkey={it.key} C={C} mode={mode} />}
                  {(!f || it.set) && <text x={W / 2} y={560} textAnchor="middle" fontSize="220">{it.icon}</text>}
                </svg>
                <span className="k">{it.kind}</span>
                <span className="t">{it.title}{av.key === it.key && <small>지금 보는 중</small>}</span>
                <span className="d">{it.desc}</span>
              </button>
            );
          })}
        </div>
        <div className="dsp-gal-foot">
          <button type="button" className="dsp-chip" onClick={onExit}>← 공부하기로 나가기</button>
        </div>
      </div>
    </div>
  );
}

/* ══════════ 액자 무대 ══════════ */
const UI = { Btn, Ic, FrameIc };
const LABS = { monty: MontyFrame, branch: BranchFrame, galton: GaltonFrame, graph: GraphFrame, lin10: Lin10Frame, area: AreaFrame,
  lin2: Lin2Frame, meet: MeetFrame, cnt100: Cnt100Frame, ...BASIC_LABS, ...CURIO_LABS };
function FrameStage({ fkey, ...rest }) {
  if (fkey === "hanoi") return <HanoiFrame ui={UI} {...rest} />;
  if (LABS[fkey]) { const Lab = LABS[fkey]; return <Lab ui={UI} {...rest} />; }
  if (FRAMES.some((f) => f.key === fkey && f.story)) return <StoryFrame fkey={fkey} ui={UI} {...rest} />;
  return null;
}


