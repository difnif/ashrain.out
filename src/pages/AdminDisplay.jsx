// 관리자 — 교실 모니터 (#/admin/display)
// 가로 화면에 도형 애니메이션을 자동으로 돌린다(공간 감각 기르기). 오른쪽 위 「초등 | 중등」 토글을 누르면
// 지금 장면이 짝이 되는 장면으로 같은 시각에 겹쳐 넘어간다 — 두 판은 같은 박자표를 쓰도록 저작되어 있다.
// 장면 목록: src/features/display/pairs.js · 엔진: core.js(계산) + draw.jsx(그리기)
// 화면은 탭·마우스 움직임에 조작 막대가 잠깐 뜨고 스스로 숨는다. 전체 화면·화면 꺼짐 방지 포함.
import { useCallback, useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { PAIRS } from "../features/display/pairs";
import { PALETTE, W, H, SceneTitle, clearMeasureCache } from "../features/display/draw";
import { E, clamp } from "../features/display/core";

const LS = { mode: "ash.display.mode", theme: "ash.display.theme", idx: "ash.display.idx", rep: "ash.display.repeat" };
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 사생활 모드 등 */ } };

const MODE_FADE = 1000;   // 초등↔중등 겹침
const PAIR_FADE = 1300;   // 다음 장면으로
const FRAME_MS = 1000 / 40;
const IDLE_MS = 3600;
const PRETENDARD = "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css";

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
  const [paused, setPaused] = useState(false);
  const [repeat, setRepeat] = useState(() => lsGet(LS.rep, "0") === "1");
  const [ctl, setCtl] = useState(true);
  const [list, setList] = useState(false);
  const [isFs, setIsFs] = useState(false);
  const [, setFrame] = useState(0);

  const rootRef = useRef(null);
  const clk = useRef({ start: performance.now(), held: null });   // held = 멈춘 동안의 경과(ms)
  const mfade = useRef(null);   // { from, t0 }
  const pfade = useRef(null);   // { idx, mode, t, t0 }
  const S = useRef({});         // 루프가 읽는 최신 상태
  S.current = { idx, mode, repeat, paused, list };

  const elapsed = (now = performance.now()) => (clk.current.held != null ? clk.current.held : now - clk.current.start);

  useEffect(() => { lsSet(LS.mode, mode); }, [mode]);
  useEffect(() => { lsSet(LS.idx, idx); }, [idx]);
  useEffect(() => { lsSet(LS.theme, thm); }, [thm]);
  useEffect(() => { lsSet(LS.rep, repeat ? 1 : 0); }, [repeat]);

  /* ── 장면 이동 (다음 쌍은 겹치며 넘어간다) ── */
  const goTo = useCallback((i, fade = true) => {
    const now = performance.now();
    const cur = S.current;
    const from = PAIRS[cur.idx];
    if (fade) pfade.current = { idx: cur.idx, mode: cur.mode, t: Math.min(elapsed(now), from.dur), t0: now };
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

  /* ── 그리기 루프 (최대 40fps) ── */
  useEffect(() => {
    let raf = 0, last = 0;
    const loop = (now) => {
      raf = requestAnimationFrame(loop);
      if (now - last < FRAME_MS) return;
      last = now;
      const cur = S.current;
      if (clk.current.held == null && now - clk.current.start >= PAIRS[cur.idx].dur) {
        goTo(cur.repeat ? cur.idx : cur.idx + 1, true);
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
    idleT.current = setTimeout(() => { if (!S.current.list) setCtl(false); }, IDLE_MS);
  }, []);
  useEffect(() => { poke(); return () => clearTimeout(idleT.current); }, [poke]);
  useEffect(() => { if (!list) poke(); }, [list, poke]);

  /* ── 키보드 (노트북에 띄울 때) ── */
  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const k = e.key;
      if (k === "ArrowRight") { goTo(S.current.idx + 1); poke(); }
      else if (k === "ArrowLeft") { goTo(S.current.idx - 1); poke(); }
      else if (k === " ") { e.preventDefault(); togglePause(); poke(); }
      else if (k === "e" || k === "E") flipMode("e");
      else if (k === "m" || k === "M") flipMode("m");
      else if (k === "t" || k === "T" || k === "Tab") { e.preventDefault(); flipMode(); }
      else if (k === "f" || k === "F") toggleFs();
      else if (k === "l" || k === "L") setList((v) => !v);
      else if (k === "Escape") setList(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [goTo, flipMode, togglePause, toggleFs, poke]);

  /* ── 그릴 층 계산 ── */
  const now = performance.now();
  const C = PALETTE[thm];
  const pair = PAIRS[idx];
  const t = clamp(elapsed(now), 0, pair.dur);
  const layers = [];
  const pf = pfade.current, mf = mfade.current;
  const kin = pf ? E.sine(clamp((now - pf.t0) / PAIR_FADE)) : 1;
  if (pf && kin < 1) layers.push({ key: "out", pair: PAIRS[pf.idx], mode: pf.mode, t: pf.t, o: 1 - kin });
  if (mf) {
    const k = E.sine(clamp((now - mf.t0) / MODE_FADE));
    if (k < 1) layers.push({ key: "from-" + mf.from, pair, mode: mf.from, t, o: kin * (1 - k * k) });
    layers.push({ key: "to-" + mode, pair, mode, t, o: kin * k });
  } else layers.push({ key: "cur-" + mode, pair, mode, t, o: kin });

  return (
    <div ref={rootRef} className={"dsp-root dsp-" + thm + (ctl ? "" : " dsp-idle")}
      onPointerMove={poke} onPointerDown={poke}>
      <style>{DSP_CSS}</style>
      <div className="dsp-frame">
        <div className="dsp-paper" />
        <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet"
          role="img" aria-label={`${pair.title[mode]} — 도형 애니메이션`}>
          {layers.map((L) => (
            <g key={L.key + "@" + L.pair.key} opacity={L.o}>
              <SceneTitle title={L.pair.title[L.mode]} sub={L.pair.sub[L.mode]} C={C} mode={L.mode} />
              {L.pair.render(L.mode, L.t, C)}
            </g>
          ))}
        </svg>

        {/* 학년 토글 — 늘 보인다 */}
        <div className={"dsp-mode on-" + mode} role="radiogroup" aria-label="학년">
          <span className="dsp-knob" aria-hidden="true" />
          <button type="button" role="radio" aria-checked={mode === "e"} onClick={() => { flipMode("e"); poke(); }}>초등</button>
          <button type="button" role="radio" aria-checked={mode === "m"} onClick={() => { flipMode("m"); poke(); }}>중등</button>
        </div>

        {/* 조작 막대 */}
        <div className={"dsp-ctl" + (ctl ? " show" : "")} onPointerDown={(e) => e.stopPropagation()}>
          <Btn title="이전 장면 (←)" onClick={() => { goTo(idx - 1); poke(); }}><Ic d="M15 5 8 12l7 7M6 5v14" /></Btn>
          <Btn title={paused ? "재생 (스페이스)" : "멈춤 (스페이스)"} onClick={() => { togglePause(); poke(); }}>
            {paused ? <Ic d="M8 5v14l11-7z" fill /> : <Ic d="M8 5v14M16 5v14" />}
          </Btn>
          <Btn title="다음 장면 (→)" onClick={() => { goTo(idx + 1); poke(); }}><Ic d="m9 5 7 7-7 7M18 5v14" /></Btn>
          <span className="dsp-sep" />
          <Btn title="이 장면 반복" on={repeat} onClick={() => { setRepeat((v) => !v); poke(); }}>
            <Ic d="M17 2l3 3-3 3M4 11V9a4 4 0 0 1 4-4h12M7 22l-3-3 3-3M20 13v2a4 4 0 0 1-4 4H4" />
          </Btn>
          <Btn title="장면 목록 (L)" on={list} onClick={() => setList((v) => !v)}><Ic d="M4 6h16M4 12h16M4 18h16" /></Btn>
          <Btn title="밝기 바꾸기" onClick={() => { setThm((v) => (v === "dark" ? "light" : "dark")); poke(); }}>
            <Ic d="M12 3a9 9 0 1 0 0 18V3z" fill />
          </Btn>
          <Btn title={isFs ? "전체 화면 끝내기 (F)" : "전체 화면 (F)"} onClick={() => { toggleFs(); poke(); }}>
            {isFs ? <Ic d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /> : <Ic d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />}
          </Btn>
          <Btn title="나가기" onClick={() => { if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); location.hash = ""; }}>
            <Ic d="M6 6l12 12M18 6 6 18" />
          </Btn>
        </div>

        {/* 진행 — 장면 점 + 지금 장면의 흐름 */}
        <div className="dsp-dots" aria-hidden="true">
          {PAIRS.map((p, i) => <i key={p.key} className={i === idx ? "on" : ""} />)}
        </div>
        <div className="dsp-prog" aria-hidden="true"><i style={{ transform: `scaleX(${t / pair.dur})` }} /></div>
        {paused && <div className="dsp-paused">멈춤</div>}

        {list && (
          <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()}>
            <div className="dsp-list-in">
              <div className="dsp-list-h">
                <b>장면 목록</b>
                <button type="button" onClick={() => setList(false)} aria-label="닫기">✕</button>
              </div>
              <div className="dsp-grid">
                {PAIRS.map((p, i) => (
                  <button key={p.key} type="button" className={"dsp-card" + (i === idx ? " on" : "")}
                    onClick={() => { goTo(i); setList(false); }}>
                    <span className="n">{String(i + 1).padStart(2, "0")}</span>
                    <span className="e">{p.title.e}</span>
                    <span className="m">{p.title.m}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function Btn({ title, on, onClick, children }) {
  return (
    <button type="button" className={"dsp-btn" + (on ? " on" : "")} title={title} aria-label={title}
      aria-pressed={on === undefined ? undefined : !!on} onClick={onClick}>{children}</button>
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

/* 학년 토글 */
.dsp-mode { position: absolute; right: 2.6cqw; top: 2.4cqw; display: flex; background: var(--chip);
  border: 1px solid var(--chipbd); border-radius: 999px; padding: .35cqw; z-index: 5; }
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
.dsp-sep { width: 1px; height: 2.2cqw; background: var(--chipbd); margin: 0 .3cqw; }

/* 진행 */
.dsp-dots { position: absolute; right: 2.8cqw; bottom: 1.6cqw; display: flex; gap: .55cqw; opacity: .55; }
.dsp-dots i { width: .5cqw; height: .5cqw; border-radius: 999px; background: var(--soft); }
.dsp-dots i.on { background: var(--gold); width: 1.4cqw; }
.dsp-prog { position: absolute; left: 0; right: 0; bottom: 0; height: .22cqw; opacity: .45; }
.dsp-prog i { display: block; height: 100%; background: var(--gold); transform-origin: 0 50%; }
.dsp-paused { position: absolute; left: 50%; bottom: 7.4cqw; transform: translateX(-50%); font-size: 1.25cqw; font-weight: 800;
  color: var(--ink); background: var(--chip); border: 1px solid var(--chipbd); border-radius: 999px; padding: .3cqw 1.1cqw; }

/* 장면 목록 */
.dsp-list { position: absolute; inset: 0; z-index: 8; display: grid; place-items: center; background: rgba(0,0,0,.35);
  backdrop-filter: blur(3px); -webkit-backdrop-filter: blur(3px); }
.dsp-list-in { width: 78cqw; max-height: 86%; overflow: auto; background: var(--card); color: var(--ink); border-radius: 1.6cqw;
  border: 1px solid var(--chipbd); padding: 1.6cqw 1.8cqw; box-shadow: 0 2cqw 5cqw rgba(0,0,0,.35); }
.dsp-list-h { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2cqw; font-size: 1.7cqw; }
.dsp-list-h button { border: 0; background: none; color: var(--soft); font-size: 1.7cqw; cursor: pointer; }
.dsp-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: .9cqw; }
.dsp-card { text-align: left; border: 1px solid var(--chipbd); border-radius: 1cqw; background: transparent; color: var(--ink);
  padding: .9cqw 1.1cqw; cursor: pointer; display: grid; grid-template-columns: auto 1fr; column-gap: .9cqw; row-gap: .15cqw;
  font: inherit; -webkit-tap-highlight-color: transparent; }
.dsp-card.on { border-color: var(--gold); box-shadow: inset 0 0 0 1px var(--gold); }
.dsp-card .n { grid-row: span 2; font-size: 1.5cqw; font-weight: 800; color: var(--gold); align-self: center; }
.dsp-card .e { font-size: 1.25cqw; font-weight: 700; color: var(--e); }
.dsp-card .m { font-size: 1.25cqw; font-weight: 700; color: var(--m); }
`;
