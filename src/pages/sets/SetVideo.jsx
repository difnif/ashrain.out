// ashrain.out — 컨셉 문제 「해설 영상」(#/sets/<범주>/<NN>/video[?no=N])
// 세트 50문항의 해설을 교실 모니터처럼 끝없이 돌린다 — 시청각 해설(교실 모니터 해설 액자)과 같은 틀(features/display/frames/lesson.jsx):
//   · 문항 하나 = 장면 하나(videoScenes.jsx): 문제 → 방침 → 전개(도식이 함께 빛난다) → 확인 · 답. 끝나면 다음 문항, 마지막 다음은 처음.
//   · 조작 막대(화면을 건드리면 뜨고 3.6초 뒤 숨는다): 이전 · 멈춤 · 다음 · 이 문항 반복 · 밝기 · 전체 화면 · 번호 · 단계 목록 · 나가기
//     둘째 줄: 「보기 단일 | 듀얼」 · 「세트」(컨셉 문제 세트 전부 — 목록) · 「빠르기 0.75× · 1× · 1.5× · 2×」
//     아래 긴 막대 = 문항 이동(하 · 중 · 상 눈금) · 옆 짧은 막대 = 풀이 이동(문제 · 방침 · 전개 줄 · 확인 · 답).
//     키보드 ←/→ · 스페이스 · R(반복) · F(전체 화면) · L(목록) · U(세트 목록) · B(다음 세트) · S(빠르기) · D(단일 | 듀얼) · X(듀얼 판 자리 바꾸기) · Esc.
//   · 듀얼 모드: 화면을 좌우 둘로 나눠 두 판을 따로 — 판마다 세트 · 단계 · 번호 · 빠르기 · 멈춤 · 반복 · 두 막대(videoSpec.js).
//   · 벽시계로 흐른다 — 새로고침하거나 나갔다 와도 그 자리에서(그동안 돈 만큼 앞으로). ?no=N 으로 들어오면 그 문항부터(단일 모드).
//     같은 세트로 다시 들어오면 마지막 보기(단일 · 듀얼) 그대로, 다른 세트로 들어오면 그 세트를 단일 모드로.
//   · 단일 모드에서 세트를 바꾸면 주소 · 제목 · 나가기(세트 화면)도 그 세트로 — 새로고침해도 그 세트.
//   · 화면 꺼짐 방지(wake lock) · 전체 화면이면 가로로 고정 · 휴대폰에서도 누를 수 있게 단추 · 막대 · 목록에 바닥 크기.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { PALETTE, clearMeasureCache } from "../../features/display/draw.jsx";
import { LessonFrame } from "../../features/display/frames/lesson.jsx";
import { DSP_CSS, Btn, Ic, FrameIc } from "../../features/display/stage-ui.jsx";
import { CATEGORIES, loadIndex, loadSet, pad2 } from "../../lib/conceptsets";
import { ensureSerif } from "./common";
import { bumpFontEpoch } from "./videoScenes";
import { videoSpec, videoKey, parseVideoKey, VIDEO_LSK } from "./videoSpec";

const IDLE_MS = 3600;
const UI = { Btn, Ic, FrameIc };
const TK = "ash.cs.video.theme";
const PRETENDARD = "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css";
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 사생활 모드 등 */ } };
const lsJson = (k) => { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch { return null; } };

/** 들여온 세트(key → 세트 JSON) — 화면을 나갔다 와도 남는다(lib/conceptsets 도 같은 것을 기억한다) */
const SETS = new Map();
const SRC = {
  get: (k) => SETS.get(k),
  load: (k) => {
    const p = parseVideoKey(k);
    if (!p) return Promise.reject(new Error(`없는 세트: ${k}`));
    return loadSet(p.cat, p.no).then((j) => { SETS.set(k, j); return j; });
  },
};

const CSV_CSS = `
.csv .dsp-dots { display: none; }
/* 휴대폰에서도 누를 수 있게 — 조작 막대 · 둘째 줄 · 목록 · 듀얼 판 조작 · 두 막대에 바닥 크기(교실 모니터에선 cqw 쪽이 커서 그대로) */
.csv .dsp-ctl { gap: max(.5cqw, 2px); padding: max(.45cqw, 4px) max(.7cqw, 7px); top: max(2.4cqw, 10px); }
.csv .dsp-btn { width: max(3.5cqw, 38px); height: max(3.5cqw, 38px); font-size: max(1.65cqw, 18px); }
.csv .dsp-sep { height: max(2.2cqw, 20px); }
.csv .dsp-pctl { top: max(7.5cqw, 58px); gap: max(.4cqw, 4px); padding: max(.35cqw, 3px) max(.8cqw, 8px); }
.csv .dsp-pc .lb { font-size: max(1.1cqw, 11.5px); }
.csv .dsp-seg { padding: max(.25cqw, 2px); }
.csv .dsp-seg button { font-size: max(1.2cqw, 12.5px); padding: max(.55cqw, 6px) max(1.1cqw, 10px); }
.csv .dsp-chip { font-size: max(1.25cqw, 13px); padding: max(.45cqw, 5px) max(1.1cqw, 11px); }
.csv .dsp-chip.lsn-unit { font-size: max(1.15cqw, 12.5px); max-width: max(26cqw, 190px); }
.csv .dsp-paused { font-size: max(1.25cqw, 13px); padding: max(.3cqw, 3px) max(1.1cqw, 12px); }
.csv .dsp-prog { height: max(.22cqw, 3px); }
.csv .dsp-list-in { width: min(94%, max(78cqw, 340px)); padding: max(1.6cqw, 14px) max(1.8cqw, 14px); border-radius: max(1.6cqw, 14px); overscroll-behavior: contain;
  --lsn-pad: max(1.6cqw, 14px); }
.csv .dsp-list-h { font-size: max(1.6cqw, 16px); margin-bottom: max(.5cqw, 6px); gap: 12px; }
.csv .dsp-list-h button { font-size: max(1.7cqw, 18px); padding: 4px 8px; }
.csv .dsp-gal-sub { margin: 0 0 max(1.1cqw, 10px); font-size: max(1.05cqw, 12.5px); color: var(--soft); line-height: 1.5; }
.csv .dsp-grid { grid-template-columns: repeat(auto-fill, minmax(max(22cqw, 210px), 1fr)); gap: max(.8cqw, 8px); }
.csv .dsp-card { padding: max(.8cqw, 9px) max(1cqw, 10px); border-radius: max(1cqw, 10px); column-gap: max(.9cqw, 10px); row-gap: max(.25cqw, 3px); }
.csv .dsp-card .n { font-size: max(1.4cqw, 16px); min-width: 1.5em; text-align: center; font-variant-numeric: tabular-nums; }
.csv .dsp-card .e { color: var(--ink); font-size: max(1.12cqw, 13.5px); line-height: 1.35; word-break: keep-all; overflow-wrap: anywhere; }
.csv .dsp-card .m { color: var(--soft); font-weight: 600; font-size: max(.92cqw, 11.5px); display: flex; align-items: center; flex-wrap: wrap; }
.csv .lsn-sets { gap: max(.6cqw, 6px); }
.csv .lsn-set { padding: max(.6cqw, 7px) max(.8cqw, 9px); border-radius: max(.9cqw, 9px); font-size: max(1.1cqw, 13px); }
.csv .lsn-grp { font-size: max(.95cqw, 12px); }
/* 듀얼 판 */
.csv .lsn-pane-ctl .dsp-btn { width: max(3cqw, 34px); height: max(3cqw, 34px); font-size: max(1.45cqw, 16px); }
.csv .lsn-pane-ctl .dsp-seg button { font-size: max(1.05cqw, 11.5px); padding: max(.45cqw, 5px) max(.85cqw, 8px); }
.csv .lsn-pane-ctl .dsp-chip.lsn-unit { font-size: max(1.05cqw, 12px); max-width: max(22cqw, 150px); }
.csv .lsn-pane-list .dsp-chip { font-size: max(1.05cqw, 12px); }
.csv .lsn-pane-list .dsp-list-in { width: max(46.5cqw, 300px); max-width: 96%; }
.csv .lsn-swap { width: max(4.4cqw, 40px); height: max(4.4cqw, 40px); margin: calc(max(4.4cqw, 40px) / -2) 0 0 calc(max(4.4cqw, 40px) / -2); }
/* 두 막대 */
.csv .scb-long { height: max(3.6cqw, 30px); }
.csv .scb-long .tr { height: max(.5cqw, 5px); }
.csv .scb-long .tl { font-size: max(.82cqw, 10px); top: max(1.05cqw, 9px); }
.csv .scb-short { width: max(3.6cqw, 30px); }
.csv .scb-short .tr { width: max(.5cqw, 5px); }
.csv .scb-knob { width: max(2.5cqw, 22px); height: max(2.5cqw, 22px); margin: calc(max(2.5cqw, 22px) / -2) 0 0 calc(max(2.5cqw, 22px) / -2); font-size: max(1.05cqw, 11px); }
.csv .scb-short .scb-knob { width: max(1.9cqw, 18px); height: max(1.9cqw, 18px); margin: calc(max(1.9cqw, 18px) / -2) 0 0 calc(max(1.9cqw, 18px) / -2); }
.csv .scb-tip { font-size: max(1.1cqw, 12px); }
@media (max-width: 640px) {
  .csv .dsp-pctl { flex-wrap: wrap; justify-content: center; white-space: normal; width: max-content; max-width: 94%; border-radius: 18px; row-gap: 4px; }
}
.csv-wait { position: absolute; inset: 0; display: grid; place-items: center; color: var(--soft); font-size: max(1.6cqw, 15px); font-weight: 700; }
.csv-rot { position: absolute; left: 50%; bottom: max(18px, env(safe-area-inset-bottom)); transform: translateX(-50%); z-index: 4; display: none;
  white-space: nowrap; font-size: 13px; font-weight: 700; color: var(--soft); background: var(--chip); border: 1px solid var(--chipbd);
  border-radius: 999px; padding: 6px 14px; pointer-events: none; }
@media (orientation: portrait) and (max-width: 900px) { .csv-rot { display: block; } }
`;

/** 범주 index 들(범주 차례) — 지금 범주는 세트 화면이 이미 들여왔다. 못 받은 범주는 빼고, 지금 범주마저 없으면 이 세트 하나로 */
function useCats(catId, set) {
  const [cats, setCats] = useState(null);
  useEffect(() => {
    let live = true;
    Promise.allSettled(CATEGORIES.map((c) => loadIndex(c.id))).then((rs) => {
      if (!live) return;
      const ok = rs.map((r) => (r.status === "fulfilled" ? r.value : null)).filter((c) => c && Array.isArray(c.sets));
      const has = ok.some((c) => c.id === catId && c.sets.some((s) => s.no === set.no));
      const lv = {};
      for (const it of set.items || []) lv[it.lv] = (lv[it.lv] || 0) + 1;
      const own = { id: catId, title: CATEGORIES.find((c) => c.id === catId)?.title || catId, icon: set.icon,
        sets: [{ no: set.no, short: set.short, title: set.title, icon: set.icon, lv, n: set.items?.length || 0 }] };
      setCats(has ? ok : [...ok.filter((c) => c.id !== catId), own]);
    });
    return () => { live = false; };
  }, [catId, set]);
  return cats;
}

export default function SetVideo({ catId, set, at }) {
  const [thm, setThm] = useState(() => (lsGet(TK, "dark") === "light" ? "light" : "dark"));
  const [ctl, setCtl] = useState(true);
  const [isFs, setIsFs] = useState(false);
  const rootRef = useRef(null);
  const urlKey = videoKey(catId, set.no);
  SETS.set(urlKey, set);
  const cats = useCats(catId, set);
  const spec = useMemo(() => {
    if (!cats) return null;
    const sp = videoSpec(cats, SRC);
    return sp.sets.some((s) => s.key === urlKey) ? sp : null;
  }, [cats, urlKey]);
  // 처음 한 번: 다른 세트로 들어왔거나 ?no=N 이면 그 세트를 단일 모드로 — 같은 세트로 다시 들어오면 마지막 보기(단일 · 듀얼) 그대로
  const start = useRef(null);
  if (!start.current) {
    const o = lsJson(VIDEO_LSK) || {};
    start.current = { pick: at != null || o.set !== urlKey ? urlKey : null, no: at ?? null };
  }
  const cur = useRef({ cat: catId, no: set.no });          // 단일 모드에서 보던 세트 — 나가기 · 주소 · 제목

  useEffect(() => { lsSet(TK, thm); }, [thm]);

  // ?no=N 은 들어올 때 한 번만 — 새로고침하면 벽시계 자리에서 이어지도록 주소에서 지운다
  const setUrl = useCallback((cat, no) => {
    try {
      const h = `#/sets/${cat}/${pad2(no)}/video`;
      if (location.hash !== h) history.replaceState(history.state, "", `${location.pathname}${location.search}${h}`);
    } catch { /* 무시 */ }
  }, []);
  useEffect(() => { if (at) setUrl(catId, set.no); }, [at, catId, set.no, setUrl]);

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

  /* ── 조작 막대: 움직이면 잠깐 보이고 스스로 숨는다 ── */
  const idleT = useRef(0);
  const poke = useCallback(() => {
    setCtl(true);
    clearTimeout(idleT.current);
    idleT.current = setTimeout(() => setCtl(false), IDLE_MS);
  }, []);
  useEffect(() => { poke(); return () => clearTimeout(idleT.current); }, [poke]);

  /** 단일 모드에서 장면이 바뀔 때 — 보던 세트가 바뀌었으면 주소 · 제목도 그 세트로(새로고침 · 나가기가 그 세트로) */
  const onSeen = useCallback((k) => {
    const p = parseVideoKey(k);
    if (!p) return;
    cur.current = p;
    setUrl(p.cat, p.no);
    const S = SETS.get(k);
    if (S) document.title = `해설 영상 · ${pad2(p.no)} ${S.short}`;
  }, [setUrl]);
  const exit = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    location.hash = `#/sets/${cur.current.cat}/${pad2(cur.current.no)}`;
  }, []);
  const toggleThm = useCallback(() => { setThm((v) => (v === "dark" ? "light" : "dark")); poke(); }, [poke]);
  const noop = useCallback(() => {}, []);

  return (
    <div ref={rootRef} className={`dsp-root dsp-${thm} csv` + (ctl ? "" : " dsp-idle")} onPointerMove={poke} onPointerDown={poke}>
      <style>{DSP_CSS + CSV_CSS}</style>
      <div className="dsp-frame">
        <div className="dsp-paper" />
        {spec ? (
          <LessonFrame spec={spec} pick={start.current.pick} pickNo={start.current.no} onSeen={onSeen}
            C={PALETTE[thm]} mode="m" onMode={noop} ctl={ctl} poke={poke} isFs={isFs} toggleFs={toggleFs} onTheme={toggleThm}
            onGallery={null} noGallery onExit={exit} exitTitle="나가기 — 세트로" inert={false} ui={UI} />
        ) : <div className="csv-wait">해설 영상 불러오는 중…</div>}
      </div>
      <div className="csv-rot" aria-hidden="true">가로로 돌리면 크게 보여요</div>
    </div>
  );
}
