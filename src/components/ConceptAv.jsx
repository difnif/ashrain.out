// ashrain.out — 개념 설명의 「움직이는 예시」 재생 카드 (components/ConceptAv.jsx)
// 개념 설명이 예를 드는 단락 안에서, 그 예를 해설 액자(교실 모니터 시청각 콘텐츠)와 같은 판서 재생기로 돌린다 —
//   문제 → 방침 → 판서(포지티브 · 네거티브 → 식 한 줄씩) → 답, 그림(자리 돌리기 · 짚어 세기 · 뽑기 · 나뭇가지 …)은 판서 줄에 맞춰 움직인다.
// 예시 · 붙이는 자리: features/display/concept-av.js(CONCEPT_AV) — ConceptViewer 가 단락 끝에 이 카드를 놓는다(React.lazy — 그림 엔진은 이 카드를 열 때만 받는다).
//   그 밖의 개념은 학기 파일 예시(public/concept-av/<학기>.json · cvgen/) — DB 단락 글줄의 「[[av:m1-1-26-1]]」 자리에서, 그 학기 파일을 처음 쓸 때 한 번 받는다.
// 판: 카드가 넓으면 넓은 판(1600 폭 — 글자 왼쪽 · 그림 오른쪽), 좁으면(휴대폰) 좁은 판(800 폭 — 그림은 글자 아래). 판은 글자 · 그림 아래에서 잘라 빈 곳을 남기지 않는다.
// 재생: 화면에 반쯤 들어오면 한 번 저절로 돈다(문제는 바로 보이고 방침부터 써진다) · 화면 밖으로 나가면 멈췄다가 돌아오면 잇는다 ·
//   판을 누르면 멈춤/이어 보기 · 막대(단계 눈금)를 누르거나 끌면 그때로 · ↺ 처음부터 · 빠르기 1× / 1.5× · 움직임 줄이기 설정이면 다 푼 모습만.
// 색: 다크 = 남색 종이 · 라이트 = 한지(해설 액자 팔레트 그대로).
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { PALETTE, clearMeasureCache } from "../features/display/draw.jsx";
import { l10Plan } from "../features/display/lin10.js";
import { L10Art, layoutOf } from "../features/display/frames/lin10.jsx";
import { stepMarks } from "../features/display/frames/scrub.jsx";
import { AV_BY_ID } from "../features/display/concept-av.js";
import { avUnitOf } from "../lib/conceptAv.js";

export const AV_WIDE = { key: "cavw", left: 60, right: 1540, top: 64, bottom: 790, figTop: true };
export const AV_NARROW = { key: "cavn", left: 40, right: 760, top: 56, bottom: 1900, figTop: true };
const NARROW_PX = 540;            // 카드 폭이 이보다 좁으면 좁은 판
const SPEEDS = [1, 1.5];
const PRETENDARD = "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css";

/** 판을 글자 · 그림 아래에서 자른 모습 — viewBox · 높이 · 그림이 들어갔나 */
export function avView(it, R) {
  const Lo = layoutOf(it, R);
  const fb = Lo.fig ? Lo.fig.y + Lo.fig.h : 0;
  const bottom = Math.max(Lo.bottom, fb) + 52;
  const y0 = R.top - 44, w = R.right > 1000 ? 1600 : 800;
  return { vb: `0 ${y0} ${w} ${Math.round(bottom - y0)}`, w, h: bottom - y0, fig: !!Lo.fig, Lo };
}
/** 도는 구간(1배속 ms) — 문제는 처음부터 보이고 방침부터 써진다 · 답 칸이 그려지고 조금 뒤 멈춘다 */
export function avSpan(it) {
  const P = l10Plan(it);
  return { P, t0: Math.max(700, P.plan[0] - 700), t1: P.ans + 1700 };
}
const cloneIt = (it) => JSON.parse(JSON.stringify(it));

// 학기 파일 예시(public/concept-av/<학기>.json — cvgen 생성기) — 그 학기 카드가 처음 쓸 때 한 번 받아 둔다
const UNIT_DONE = new Map(), UNIT_WAIT = new Map();
function loadUnit(unit) {
  if (UNIT_DONE.has(unit)) return Promise.resolve(UNIT_DONE.get(unit));
  if (!UNIT_WAIT.has(unit)) {
    UNIT_WAIT.set(unit, fetch(`/concept-av/${unit}.json`, { cache: "no-cache" })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => { const items = d?.items || {}; UNIT_DONE.set(unit, items); UNIT_WAIT.delete(unit); return items; })
      .catch(() => { UNIT_WAIT.delete(unit); return {}; }));
  }
  return UNIT_WAIT.get(unit);
}
/** 시험 · 미리 보기 — 학기 파일을 받아 둔 것으로 넣는다({ items } 또는 items) */
export function primeAvUnit(unit, data) { UNIT_DONE.set(unit, data?.items || data || {}); }
/** 예시 id → 예시(코드 안 예시가 먼저, 다음은 받아 둔 학기 파일) */
export const avItem = (id) => AV_BY_ID.get(id) || UNIT_DONE.get(avUnitOf(id))?.[id] || null;
const unitsToLoad = (key) => [...new Set(key.split(",").filter((id) => id && !AV_BY_ID.has(id)).map(avUnitOf).filter((u) => u && !UNIT_DONE.has(u)))];

const CSS = `
.cav { margin: 14px 0 2px; border-radius: 14px; overflow: hidden; border: 1px solid var(--cav-bd); background: var(--cav-bg); }
.cav-wait { min-height: 120px; }
.cav-head { display: flex; align-items: baseline; gap: 8px; padding: 9px 12px 6px; }
.cav-tag { font-size: 11.5px; font-weight: 800; letter-spacing: .4px; color: var(--cav-ac); white-space: nowrap; }
.cav-title { font-size: 12.5px; font-weight: 700; color: var(--cav-ink); min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cav-tabs { display: flex; gap: 6px; flex-wrap: wrap; padding: 0 12px 8px; }
.cav-tab { border: 1px solid var(--cav-bd); background: transparent; color: var(--cav-mut); border-radius: 999px; font-size: 12px; font-weight: 800;
  padding: 6px 11px; cursor: pointer; font-family: inherit; }
.cav-tab.on { color: var(--cav-ac); border-color: var(--cav-ac); background: var(--cav-acbg); }
.cav-stage { position: relative; cursor: pointer; touch-action: manipulation; -webkit-user-select: none; user-select: none; }
.cav-stage svg { display: block; width: 100%; height: auto; }
.cav-hint { position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%); padding: 6px 13px; border-radius: 999px; font-size: 12px; font-weight: 800;
  background: var(--cav-hintbg); color: var(--cav-hint); pointer-events: none; white-space: nowrap; animation: cavhint 2.6s ease forwards; }
@keyframes cavhint { 0% { opacity: 0; } 12% { opacity: 1; } 75% { opacity: 1; } 100% { opacity: 0; } }   /* 잠깐 알려 주고 사라진다(판을 가리지 않게) */
.cav-ctl { display: flex; align-items: center; gap: 8px; padding: 7px 10px 9px; }
.cav-btn { flex-shrink: 0; width: 32px; height: 32px; border-radius: 999px; border: 1px solid var(--cav-bd); background: transparent; color: var(--cav-ink);
  display: flex; align-items: center; justify-content: center; cursor: pointer; padding: 0; }
.cav-btn svg { width: 15px; height: 15px; }
.cav-bar { flex: 1; position: relative; height: 26px; cursor: pointer; touch-action: none; min-width: 60px; }
.cav-bar .tr { position: absolute; left: 0; right: 0; top: 11px; height: 4px; border-radius: 999px; background: var(--cav-track); }
.cav-bar .fill { position: absolute; left: 0; top: 11px; height: 4px; border-radius: 999px; background: var(--cav-ac); }
.cav-bar .tick { position: absolute; top: 8px; width: 2px; height: 10px; margin-left: -1px; border-radius: 1px; background: var(--cav-mut); opacity: .55; }
.cav-bar .knob { position: absolute; top: 6px; width: 14px; height: 14px; margin-left: -7px; border-radius: 50%; background: var(--cav-ac); box-shadow: 0 0 0 3px var(--cav-acbg); }
.cav-sp { flex-shrink: 0; border: 1px solid var(--cav-bd); background: transparent; color: var(--cav-mut); border-radius: 999px; font-size: 11.5px; font-weight: 800;
  padding: 6px 9px; cursor: pointer; font-family: inherit; min-width: 42px; }
.cav-sp.on { color: var(--cav-ac); border-color: var(--cav-ac); }
`;
const VARS = {
  light: { "--cav-bg": "#fbf6ea", "--cav-bd": "#e3d6b8", "--cav-ink": "#3B3021", "--cav-mut": "#7B6C55", "--cav-ac": "#9a6a0c", "--cav-acbg": "rgba(179,122,14,.13)",
    "--cav-track": "rgba(59,48,33,.14)", "--cav-hintbg": "rgba(59,48,33,.78)", "--cav-hint": "#fff8e8" },
  dark: { "--cav-bg": "#151c33", "--cav-bd": "#2c3a66", "--cav-ink": "#F2E8D0", "--cav-mut": "#B8B0A0", "--cav-ac": "#F4C65A", "--cav-acbg": "rgba(244,198,90,.14)",
    "--cav-track": "rgba(242,232,208,.16)", "--cav-hintbg": "rgba(8,12,27,.72)", "--cav-hint": "#F5ECD5" },
};
const ICON = {
  play: <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.8v10.4L13 8z" fill="currentColor" /></svg>,
  pause: <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.8h2.8v10.4H4zM9.2 2.8H12v10.4H9.2z" fill="currentColor" /></svg>,
  again: <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.5a5.5 5.5 0 1 1-5.2 3.7" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" /><path d="M2.2 2.4v4h4" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" /></svg>,
};

/** 글꼴(Pretendard)이 늦게 오면 글자 폭을 다시 재서 판을 다시 놓는다 */
function useFontEpoch() {
  const [ep, setEp] = useState(0);
  useEffect(() => {
    if (typeof document === "undefined") return undefined;
    if (!document.getElementById("pretendard-css")) {
      const l = document.createElement("link");
      l.id = "pretendard-css"; l.rel = "stylesheet"; l.href = PRETENDARD;
      document.head.appendChild(l);
    }
    const fonts = document.fonts;
    let live = true;
    const onDone = () => { if (!live) return; clearMeasureCache(); setEp((v) => v + 1); };
    fonts?.ready?.then(onDone).catch(() => {});
    fonts?.addEventListener?.("loadingdone", onDone);
    return () => { live = false; fonts?.removeEventListener?.("loadingdone", onDone); };
  }, []);
  return ep;
}
const reducedMotion = () => typeof matchMedia !== "undefined" && matchMedia("(prefers-reduced-motion: reduce)").matches;

/** 재생 카드 — ids: 예시 id 목록(둘 이상이면 칩으로 고른다) */
export default function ConceptAv({ ids, theme = "light" }) {
  const key = (ids || []).join(",");
  const [ver, setVer] = useState(0);            // 학기 파일을 받으면 다시 고른다
  const pending = unitsToLoad(key).length > 0;
  useEffect(() => {
    const units = unitsToLoad(key);
    if (!units.length) return undefined;
    let live = true;
    Promise.all(units.map(loadUnit)).then(() => { if (live) setVer((v) => v + 1); });
    return () => { live = false; };
  }, [key]);
  const list = useMemo(() => key.split(",").map(avItem).filter(Boolean), [key, ver]); // eslint-disable-line react-hooks/exhaustive-deps
  const [sel, setSel] = useState(0);
  const ep = useFontEpoch();
  const base = list[Math.min(sel, list.length - 1)];
  // 글꼴이 바뀌면 문항을 새로 떠서(배치 기억이 문항마다 붙어 있다) 다시 잰다
  const it = useMemo(() => (base && ep ? cloneIt(base) : base), [base, ep]);
  const wrap = useRef(null);
  const [narrow, setNarrow] = useState(false);
  useEffect(() => {
    const el = wrap.current;
    if (!el) return undefined;
    const fit = () => setNarrow(el.clientWidth > 0 && el.clientWidth < NARROW_PX);
    fit();
    if (typeof ResizeObserver === "undefined") return undefined;
    const ro = new ResizeObserver(fit);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  const R = narrow ? AV_NARROW : AV_WIDE;
  const view = useMemo(() => (it ? avView(it, R) : null), [it, R]);
  const span = useMemo(() => (it ? avSpan(it) : null), [it]);
  const marks = useMemo(() => (span ? stepMarks(span.P, it.lines, 1, it.planTag || "방침").filter((m) => m.t >= span.t0 - 1 && m.t <= span.t1) : []), [span, it]);

  const reduce = useMemo(reducedMotion, []);
  const [t, setT] = useState(() => (span ? (reduce ? span.t1 : span.t0) : 0));
  const tRef = useRef(t);
  const [want, setWant] = useState(false);      // 돌리려는 뜻(저절로 · 누름)
  const [vis, setVis] = useState(false);        // 화면에 반쯤 들어와 있나
  const [sp, setSp] = useState(1);
  const auto = useRef(false);
  const seek = useCallback((v) => { tRef.current = v; setT(v); }, []);
  // 예시가 늦게 도착하면(학기 파일) 처음 모습으로 — 문제는 보이고 방침부터
  useEffect(() => {
    if (span && tRef.current < span.t0) seek(reduce ? span.t1 : span.t0);
  }, [span, reduce, seek]);
  // 예시를 바꾸면 처음부터
  const first = useRef(true);
  useEffect(() => {
    if (!span) return;
    if (first.current) { first.current = false; return; }
    seek(reduce ? span.t1 : span.t0);
    if (!reduce) setWant(true);
  }, [sel]); // eslint-disable-line react-hooks/exhaustive-deps
  // 화면에 들어오면 한 번 저절로
  useEffect(() => {
    const el = wrap.current;
    if (!el || typeof IntersectionObserver === "undefined") { setVis(true); if (!reduce) setWant(true); return undefined; }
    const ob = new IntersectionObserver(([e]) => {
      // 반쯤 들어왔거나(카드가 화면보다 길면) 화면의 절반 가까이를 채우면 보이는 것
      const v = e.isIntersecting && (e.intersectionRatio >= 0.5 || e.intersectionRect.height >= (window.innerHeight || 800) * 0.45);
      setVis(v);
      if (v && !auto.current && !reduce) { auto.current = true; setWant(true); }
    }, { threshold: [0, 0.5, 1] });
    ob.observe(el);
    return () => ob.disconnect();
  }, [reduce]);
  // 돌리기
  useEffect(() => {
    if (!span || !want || !vis) return undefined;
    let raf = 0, last = performance.now();
    if (tRef.current >= span.t1 - 1) seek(span.t0);
    const tick = (now) => {
      const dt = Math.min(64, now - last);
      last = now;
      const nt = tRef.current + dt * sp;
      if (nt >= span.t1) { seek(span.t1); setWant(false); return; }
      seek(nt);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [want, vis, sp, span, seek]);

  // 막대 — 누르거나 끌면 그때로
  const bar = useRef(null);
  const drag = useRef(false);
  const posT = (clientX) => {
    const r = bar.current.getBoundingClientRect();
    const k = Math.max(0, Math.min(1, (clientX - r.left) / Math.max(1, r.width)));
    return span.t0 + (span.t1 - span.t0) * k;
  };
  const onBarDown = (e) => {
    if (!span) return;
    e.preventDefault();
    drag.current = true;
    setWant(false);
    seek(posT(e.clientX));
    try { e.currentTarget.setPointerCapture?.(e.pointerId); } catch { /* 무시 */ }
  };
  const onBarMove = (e) => { if (drag.current) seek(posT(e.clientX)); };
  const onBarUp = () => { drag.current = false; };

  if (!it || !view || !span) {
    // 학기 파일을 받는 동안은 자리만(뷰포트 · 폭 재기는 이 상자에 붙어 그대로 이어진다)
    return pending ? <div className="cav cav-wait" ref={wrap} style={VARS[theme === "dark" ? "dark" : "light"]}><style>{CSS}</style></div> : null;
  }
  const C = PALETTE[theme === "dark" ? "dark" : "light"];
  const ended = t >= span.t1 - 1;
  const playing = want && !ended;
  const frac = (span.t1 - span.t0) > 0 ? (t - span.t0) / (span.t1 - span.t0) : 1;
  const pct = (v) => `${(Math.max(0, Math.min(1, v)) * 100).toFixed(2)}%`;
  const toggle = () => {
    if (ended) { seek(span.t0); setWant(true); return; }
    setWant((v) => !v);
  };
  const again = () => { seek(span.t0); setWant(true); };
  const bg = `radial-gradient(130% 110% at 50% 8%, ${C.bg[0]} 0%, ${C.bg[1]} 58%, ${C.bg[2]} 100%)`;
  const hint = ended ? "↺ 누르면 다시 봐요" : !playing && t > span.t0 + 50 ? "▶ 누르면 이어서 봐요" : null;

  return (
    <div className="cav" ref={wrap} style={VARS[theme === "dark" ? "dark" : "light"]}>
      <style>{CSS}</style>
      <div className="cav-head">
        <span className="cav-tag">▶ 움직이는 예시</span>
        <span className="cav-title">{it.title}</span>
      </div>
      {list.length > 1 && (
        <div className="cav-tabs" role="tablist" aria-label="예시 고르기">
          {list.map((x, i) => (
            <button key={x.id} type="button" role="tab" aria-selected={i === sel} className={"cav-tab" + (i === sel ? " on" : "")}
              onClick={() => { if (i !== sel) setSel(i); }}>{x.tab}</button>
          ))}
        </div>
      )}
      <div className="cav-stage" style={{ background: bg }} onClick={toggle} role="img" aria-label={`움직이는 예시: ${it.q}`}>
        <svg viewBox={view.vb} preserveAspectRatio="xMidYMin meet">
          <L10Art it={it} t={t} C={C} uid={`cav${it.id}`} region={R} />
        </svg>
        {hint && <span key={hint} className="cav-hint">{hint}</span>}
      </div>
      <div className="cav-ctl">
        <button type="button" className="cav-btn" onClick={toggle} aria-label={playing ? "멈춤" : "재생"} title={playing ? "멈춤" : "재생"}>{playing ? ICON.pause : ICON.play}</button>
        <div className="cav-bar" ref={bar} onPointerDown={onBarDown} onPointerMove={onBarMove} onPointerUp={onBarUp} onPointerCancel={onBarUp}
          role="slider" aria-label="풀이 단계" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(frac * 100)}>
          <div className="tr" />
          <div className="fill" style={{ width: pct(frac) }} />
          {marks.map((m, i) => <div key={i} className="tick" title={m.lab} style={{ left: pct((m.t - span.t0) / (span.t1 - span.t0)) }} />)}
          <div className="knob" style={{ left: pct(frac) }} />
        </div>
        <button type="button" className="cav-btn" onClick={again} aria-label="처음부터" title="처음부터">{ICON.again}</button>
        {SPEEDS.map((v) => (
          <button key={v} type="button" className={"cav-sp" + (sp === v ? " on" : "")} onClick={() => setSp(v)} aria-pressed={sp === v}>{v}×</button>
        ))}
      </div>
    </div>
  );
}
