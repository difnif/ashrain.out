// ashrain.out — 컨셉 문제 「해설 영상」(#/sets/<범주>/<NN>/video[?no=N])
// 세트 50문항의 해설을 교실 모니터처럼 끝없이 돌린다 — 같은 무대(stage-ui) · 같은 재생기(frames/player.jsx 의 StoryPlayer).
//   · 문항 하나 = 장면 하나(videoScenes.jsx): 문제 → 방침 → 전개(도식이 함께 빛난다) → 확인 · 답. 끝나면 다음 문항, 50번 다음은 1번.
//   · 벽시계로 흐른다 — 새로고침하거나 나갔다 와도 그 자리에서(그동안 돈 만큼 앞으로). ?no=N 으로 들어오면 그 문항부터.
//   · 조작 막대(화면을 건드리면 뜨고 3.6초 뒤 숨는다): 이전 · 멈춤 · 다음 · 이 문항 반복 · 밝기 · 전체 화면 · 문항 목록 · 나가기.
//     키보드 ←/→ · 스페이스 · R(반복) · F(전체 화면) · L(목록) · Esc(목록 닫기).
//   · 화면 꺼짐 방지(wake lock) · 전체 화면이면 가로로 고정 · 휴대폰에서도 누를 수 있게 단추에 바닥 크기.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { PALETTE, clearMeasureCache } from "../../features/display/draw.jsx";
import { StoryPlayer } from "../../features/display/frames/player.jsx";
import { DSP_CSS, Btn, Ic, FrameIc } from "../../features/display/stage-ui.jsx";
import { pad2 } from "../../lib/conceptsets";
import { ensureSerif } from "./common";
import { LV_COLOR } from "./render";
import { solutionScenes, bumpFontEpoch, stageTitle } from "./videoScenes";

const IDLE_MS = 3600;
const UI = { Btn, Ic, FrameIc };
const TK = "ash.cs.video.theme";
const PRETENDARD = "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css";
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 사생활 모드 등 */ } };
const secs = (ms) => { const s = Math.round(ms / 1000); return s >= 60 ? `${Math.floor(s / 60)}분 ${s % 60}초` : `${s}초`; };

const CSV_CSS = `
.csv .dsp-dots { display: none; }
/* 휴대폰에서도 누를 수 있게 — 조작 막대 · 목록에 바닥 크기 */
.csv .dsp-ctl { gap: max(.5cqw, 2px); padding: max(.45cqw, 4px) max(.7cqw, 7px); top: max(2.4cqw, 10px); }
.csv .dsp-btn { width: max(3.5cqw, 38px); height: max(3.5cqw, 38px); font-size: max(1.65cqw, 18px); }
.csv .dsp-sep { height: max(2.2cqw, 20px); }
.csv .dsp-paused { font-size: max(1.25cqw, 13px); padding: max(.3cqw, 3px) max(1.1cqw, 12px); }
.csv .dsp-prog { height: max(.22cqw, 3px); }
.csv .dsp-list-in { width: min(94%, max(78cqw, 340px)); padding: max(1.6cqw, 14px) max(1.8cqw, 14px); border-radius: max(1.6cqw, 14px);
  display: flex; flex-direction: column; overflow: hidden; }
.csv-scroll { position: relative; flex: 1 1 auto; min-height: 0; overflow: auto; overscroll-behavior: contain; margin: 0 -6px; padding: 2px 6px 4px; }
.csv .dsp-list-h { font-size: max(1.6cqw, 16px); margin-bottom: max(.5cqw, 6px); gap: 12px; }
.csv .dsp-list-h button { font-size: max(1.7cqw, 18px); padding: 4px 8px; }
.csv-sub { margin: 0 0 max(1.1cqw, 10px); font-size: max(1.05cqw, 12.5px); color: var(--soft); line-height: 1.5; }
.csv .dsp-grid { grid-template-columns: repeat(auto-fill, minmax(max(22cqw, 210px), 1fr)); gap: max(.8cqw, 8px); }
.csv .dsp-card { padding: max(.8cqw, 9px) max(1cqw, 10px); border-radius: max(1cqw, 10px); column-gap: max(.9cqw, 10px); row-gap: max(.25cqw, 3px); }
.csv .dsp-card .n { font-size: max(1.4cqw, 16px); min-width: 1.5em; text-align: center; font-variant-numeric: tabular-nums; }
.csv .dsp-card .e { color: var(--ink); font-size: max(1.12cqw, 13.5px); line-height: 1.35; word-break: keep-all; overflow-wrap: anywhere; }
.csv .dsp-card .m { color: var(--soft); font-weight: 600; font-size: max(.92cqw, 11.5px); display: flex; align-items: center; gap: .45em; flex-wrap: wrap; }
.csv-lv { font-style: normal; color: #fff; font-weight: 800; border-radius: 6px; padding: 0 .45em; line-height: 1.55; }
.csv-rot { position: absolute; left: 50%; bottom: max(18px, env(safe-area-inset-bottom)); transform: translateX(-50%); z-index: 4; display: none;
  white-space: nowrap; font-size: 13px; font-weight: 700; color: var(--soft); background: var(--chip); border: 1px solid var(--chipbd);
  border-radius: 999px; padding: 6px 14px; pointer-events: none; }
@media (orientation: portrait) and (max-width: 900px) { .csv-rot { display: block; } }
`;

export default function SetVideo({ catId, set, at }) {
  const [thm, setThm] = useState(() => (lsGet(TK, "dark") === "light" ? "light" : "dark"));
  const [ctl, setCtl] = useState(true);
  const [list, setList] = useState(false);
  const [isFs, setIsFs] = useState(false);
  const [cur, setCur] = useState(0);
  const rootRef = useRef(null);
  const api = useRef(null);
  const S = useRef({});
  S.current = { list };
  const scenes = useMemo(() => solutionScenes(set), [set]);
  const lap = useMemo(() => scenes.reduce((a, s) => a + s.dur, 0), [scenes]);
  const startAt = useMemo(() => {
    if (!at) return null;
    const i = set.items.findIndex((it) => it.no === at);
    return i >= 0 ? i : null;
  }, [set, at]);
  const home = `#/sets/${catId}/${pad2(set.no)}`;

  useEffect(() => { lsSet(TK, thm); }, [thm]);

  // ?no=N 은 들어올 때 한 번만 — 새로고침하면 벽시계 자리에서 이어지도록 주소에서 지운다
  useEffect(() => {
    if (!at) return;
    try {
      const h = location.hash.replace(/\?no=\d+$/, "");
      if (h !== location.hash) history.replaceState(history.state, "", `${location.pathname}${location.search}${h}`);
    } catch { /* 무시 */ }
  }, [at]);

  /* ── 글꼴: Pretendard(판서) · Noto Serif KR(도식) — 늦게 오면 글자 폭을 다시 잰다 ── */
  useEffect(() => {
    ensureSerif();
    if (!document.getElementById("pretendard-css")) {
      const l = document.createElement("link");
      l.id = "pretendard-css"; l.rel = "stylesheet"; l.href = PRETENDARD;
      document.head.appendChild(l);
    }
    const fonts = document.fonts;
    const onDone = () => { clearMeasureCache(); bumpFontEpoch(); };
    fonts?.ready?.then(onDone).catch(() => {});
    fonts?.addEventListener?.("loadingdone", onDone);
    return () => fonts?.removeEventListener?.("loadingdone", onDone);
  }, []);

  /* ── 화면 꺼짐 방지 ── */
  useEffect(() => {
    let lock = null;
    const req = async () => {
      try { if (document.visibilityState === "visible" && navigator.wakeLock) lock = await navigator.wakeLock.request("screen"); }
      catch { /* 지원 안 함 · 거부 */ }
    };
    req();
    const onVis = () => { if (document.visibilityState === "visible") req(); };
    document.addEventListener("visibilitychange", onVis);
    return () => { document.removeEventListener("visibilitychange", onVis); try { lock?.release?.(); } catch { /* 무시 */ } };
  }, []);

  /* ── 문서 제목 · 전체 화면 ── */
  useEffect(() => {
    const prev = document.title;
    document.title = `해설 영상 · ${pad2(set.no)} ${set.short}`;
    const onFs = () => setIsFs(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", onFs);
    return () => { document.title = prev; document.removeEventListener("fullscreenchange", onFs); };
  }, [set]);
  const toggleFs = useCallback(async () => {
    try {
      if (!document.fullscreenElement) {
        await rootRef.current?.requestFullscreen?.({ navigationUI: "hide" });
        try { await screen.orientation?.lock?.("landscape"); } catch { /* 고정 불가 기기 */ }
      } else await document.exitFullscreen();
    } catch { /* 전체 화면 불가 */ }
  }, []);

  /* ── 조작 막대: 움직이면 잠깐 보이고 스스로 숨는다(목록이 열려 있으면 숨지 않는다) ── */
  const idleT = useRef(0);
  const poke = useCallback(() => {
    setCtl(true);
    clearTimeout(idleT.current);
    idleT.current = setTimeout(() => { if (!S.current.list) setCtl(false); }, IDLE_MS);
  }, []);
  useEffect(() => { poke(); return () => clearTimeout(idleT.current); }, [poke]);
  useEffect(() => { if (!list) poke(); }, [list, poke]);

  /* ── 키보드: L 목록 · Esc 목록 닫기 (←/→ · 스페이스 · R · F 는 재생기가 받는다) ── */
  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key === "Escape") { if (S.current.list) { e.preventDefault(); setList(false); } return; }
      if (e.key === "l" || e.key === "L") { setList((v) => !v); poke(); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [poke]);

  const exit = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    location.hash = home;
  }, [home]);
  const toggleThm = useCallback(() => { setThm((v) => (v === "dark" ? "light" : "dark")); poke(); }, [poke]);
  const noop = useCallback(() => {}, []);
  const pick = (i) => { api.current?.goTo(i); setList(false); poke(); };

  return (
    <div ref={rootRef} className={`dsp-root dsp-${thm} csv` + (ctl ? "" : " dsp-idle")} onPointerMove={poke} onPointerDown={poke}>
      <style>{DSP_CSS + CSV_CSS}</style>
      <div className="dsp-frame">
        <div className="dsp-paper" />
        <StoryPlayer list={scenes} lsKey={`ash.cs.video.${catId}.${pad2(set.no)}`} label={`${pad2(set.no)} ${set.short} 해설 영상`}
          C={PALETTE[thm]} mode="m" onMode={noop} ctl={ctl} poke={poke} isFs={isFs} toggleFs={toggleFs} onTheme={toggleThm}
          onGallery={noop} onExit={exit} inert={list} ui={UI} noMode noGallery exitTitle="나가기 — 세트로" startAt={startAt}
          apiRef={api} onIdx={setCur}
          extra={<Btn title="문항 목록 (L)" on={list} onClick={() => { setList((v) => !v); poke(); }}><Ic d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" /></Btn>} />
      </div>
      {list && <VideoList set={set} scenes={scenes} cur={cur} lap={lap} onPick={pick} onClose={() => setList(false)} />}
      <div className="csv-rot" aria-hidden="true">가로로 돌리면 크게 보여요</div>
    </div>
  );
}

/** 문항 목록 — 고르면 그 문항부터 이어서 돈다 */
function VideoList({ set, scenes, cur, lap, onPick, onClose }) {
  const ref = useRef(null);
  useEffect(() => {                                   // 지금 문항이 가운데 오게(목록 안에서만 굴린다)
    const box = ref.current, on = box?.querySelector(".dsp-card.on");
    if (on) box.scrollTop = Math.max(0, on.offsetTop - box.clientHeight / 2 + on.offsetHeight / 2);
  }, []);
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="문항 목록">
        <div className="dsp-list-h">
          <b>{pad2(set.no)} {set.short} · 해설 영상</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <p className="csv-sub">고르면 그 문항부터 이어서 돌아요 · {set.items.length}문항 한 바퀴 약 {Math.round(lap / 60000)}분 · 지금 {set.items[cur]?.no}번</p>
        <div ref={ref} className="csv-scroll"><div className="dsp-grid">
          {set.items.map((it, i) => (
            <button key={it.id} type="button" className={"dsp-card" + (i === cur ? " on" : "")} onClick={() => onPick(i)}>
              <span className="n">{it.no}</span>
              <span className="e">{stageTitle(it.ty)}</span>
              <span className="m"><i className="csv-lv" style={{ background: LV_COLOR[it.lv] }}>{it.lv}</i>{stageTitle(it.sp)} · {secs(scenes[i].dur)}</span>
            </button>
          ))}
        </div></div>
      </div>
    </div>
  );
}
