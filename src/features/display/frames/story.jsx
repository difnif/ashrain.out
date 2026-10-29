// ashrain.out — 교실 모니터 「액자」: 장면 묶음 (frames/story.jsx)
// 축구·서술형처럼 여러 단원을 섞는 융합 장면을 하노이의 탑처럼 액자로 켜 둔다(목록: ../stories.js).
// 수업 장면과 같은 초등↔중등 짝 장면을 차례로 끝없이 돌리고, 오른쪽 위 학년 토글을 누르면 같은 순간의 짝 장면으로 겹쳐 넘어간다.
// 시계는 벽시계(Date.now)라 새로고침하거나 잠깐 나갔다 와도 그 자리에서 이어진다(그동안 돈 만큼 앞으로).
// 조작: 이전 · 멈춤 · 다음 · 이 장면 반복 · 밝기 · 전체 화면 · 수업 장면으로. 키보드 ←/→ · 스페이스 · T(E 초등 · M 중등) · R 반복 · F.
// 장면이 controls(문 개수 · 단계 …)를 가지면 조작 막대 아래에 설정 칩이 뜬다(수업 장면과 같다, ../params.js).
// StoryPlayer 는 실험 액자의 「풀이 보기」도 그린다(extra 로 막대에 「해 보기」 단추를 더한다).
// 단추 모양(Btn · Ic · FrameIc)은 교실 모니터 무대가 ui 로 넘겨준다 — 하노이 액자와 같은 모양을 쓴다.
import { memo, useCallback, useEffect, useRef, useState } from "react";
import { W, H, SceneTitle } from "../draw.jsx";
import { E, clamp } from "../core.js";
import { paramsOf, durOf, optVal } from "../params.js";
import { STORIES } from "../stories.js";

const MODE_FADE = 1000;   // 초등↔중등 겹침
const PAIR_FADE = 1300;   // 다음 장면으로
const FRAME_MS = 1000 / 40;
const elapsedOf = (c) => (c.held != null ? c.held : Date.now() - c.t0);
const read = (k) => { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch { return null; } };
const write = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* 사생활 모드 등 */ } };

/** 저장된 자리(장면 번호 · 시작 벽시계 · 멈춘 경과 · 반복). 흐르던 중이면 비운 동안 돈 만큼 앞으로 간다 */
export function loadStory(list, now = Date.now(), o = null, prm = null) {
  const n = list.length;
  const d = (i) => durOf(list[i], paramsOf(list[i], prm));
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
export function StoryPlayer({ list, lsKey, label, C, mode, onMode, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, ui, extra, fresh }) {
  const { Btn, Ic, FrameIc } = ui;
  const n = list.length;
  const init = useRef(null);
  if (!init.current) {
    const prm0 = read(lsKey + ".prm") || {};
    const o = read(lsKey);
    const st = loadStory(list, Date.now(), o, prm0);
    if (fresh) {
      const i = o && Number.isInteger(o.i) && o.i >= 0 && o.i < n ? o.i : 0;
      Object.assign(st, { i, t0: Date.now(), held: null });
    }
    init.current = { ...st, prm: prm0 };
  }
  const [idx, setIdx] = useState(init.current.i);
  const [paused, setPaused] = useState(init.current.held != null);
  const [repeat, setRepeat] = useState(init.current.rep);
  const [prm, setPrm] = useState(init.current.prm);       // { 장면 key: { 설정 key: 값 } }
  const clk = useRef({ t0: init.current.t0, held: init.current.held });
  const pf = useRef(null);          // { idx, mode, t, t0, P } — 앞 장면이 사라지는 중
  const mf = useRef(null);          // { from, t0 } — 학년이 바뀌는 중
  const lastMode = useRef(mode);
  if (lastMode.current !== mode) { mf.current = { from: lastMode.current, t0: performance.now() }; lastMode.current = mode; }
  const [, setFrame] = useState(0);
  const R = useRef({});
  const P = paramsOf(list[idx], prm);
  R.current = { idx, repeat, mode, inert, P };

  const save = useCallback((i, rep) => write(lsKey, { i, t0: clk.current.t0, held: clk.current.held, rep }), [lsKey]);
  useEffect(() => { save(init.current.i, init.current.rep); }, [save]);
  useEffect(() => { write(lsKey + ".prm", prm); }, [lsKey, prm]);

  /** 장면 i 로 — 앞 장면은 겹치며 사라진다. 멈춰 있었으면 새 장면도 처음에서 멈춘 채 */
  const goTo = useCallback((i, fade = true) => {
    const cur = R.current;
    if (fade) pf.current = { idx: cur.idx, mode: cur.mode, t: Math.min(elapsedOf(clk.current), durOf(list[cur.idx], cur.P)), t0: performance.now(), P: cur.P };
    clk.current = { t0: Date.now(), held: clk.current.held != null ? 0 : null };
    mf.current = null;
    const j = ((i % n) + n) % n;
    setIdx(j); save(j, cur.repeat);
  }, [list, n, save]);
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
  const stepParam = useCallback((c, dir) => {
    const ops = c.options.map(optVal), i = ops.indexOf(R.current.P[c.key]);
    const j = clamp(i + dir, 0, ops.length - 1);
    if (j !== i) setParam(c.key, ops[j]);
  }, [setParam]);

  /* ── 그리기 루프 (최대 40fps, 멈추고 겹침도 끝나면 쉰다) ── */
  useEffect(() => {
    let raf = 0, last = 0;
    const loop = (now) => {
      raf = requestAnimationFrame(loop);
      if (now - last < FRAME_MS) return;
      last = now;
      const cur = R.current;
      if (clk.current.held == null && Date.now() - clk.current.t0 >= durOf(list[cur.idx], cur.P)) goTo(cur.repeat ? cur.idx : cur.idx + 1, true);
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
      else if (k === "e" || k === "E") onMode("e");
      else if (k === "m" || k === "M") onMode("m");
      else if (k === "t" || k === "T" || k === "Tab") { e.preventDefault(); onMode(); }
      else if (k === "r" || k === "R") { toggleRepeat(); poke(); }
      else if (k === "f" || k === "F") toggleFs();
      else if (k === "ArrowUp" || k === "ArrowDown") {
        const c = (list[R.current.idx].controls || []).find((x) => x.kind === "step");
        if (c) { e.preventDefault(); stepParam(c, k === "ArrowUp" ? 1 : -1); poke(); }
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [goTo, togglePause, toggleRepeat, stepParam, onMode, toggleFs, poke, list]);

  /* ── 그릴 층: 사라지는 앞 장면 · 학년 겹침 ── */
  const now = performance.now();
  const pair = list[idx];
  const dur = durOf(pair, P);
  const t = clamp(elapsedOf(clk.current), 0, dur);
  const layers = [];
  const p = pf.current, m = mf.current;
  const kin = p ? E.sine(clamp((now - p.t0) / PAIR_FADE)) : 1;
  if (p && kin < 1) layers.push({ key: "out", pair: list[p.idx], mode: p.mode, t: p.t, o: 1 - kin, P: p.P });
  if (m) {
    const k = E.sine(clamp((now - m.t0) / MODE_FADE));
    if (k < 1) layers.push({ key: "from-" + m.from, pair, mode: m.from, t, o: kin * (1 - k * k), P });
    layers.push({ key: "to-" + mode, pair, mode, t, o: kin * k, P });
  } else layers.push({ key: "cur-" + mode, pair, mode, t, o: kin, P });
  const stop = (e) => e.stopPropagation();

  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet"
        role="img" aria-label={`${label} — ${pair.title[mode]}`}>
        {layers.map((L) => (
          <g key={L.key + "@" + L.pair.key} opacity={L.o}>
            <SceneTitle title={L.pair.title[L.mode]} sub={L.pair.sub[L.mode]} C={C} mode={L.mode} />
            {L.pair.render(L.mode, L.t, C, L.P)}
          </g>
        ))}
      </svg>

      {/* 오른쪽 위 — 액자 단추 · 학년 토글 (수업 장면과 같은 자리) */}
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
        <Btn title="수업 장면으로" onClick={onExit}><Ic d="M6 6l12 12M18 6 6 18" /></Btn>
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
    </>
  );
}

/** 장면 묶음 액자(축구 · 서술형) */
export function StoryFrame({ fkey, ...rest }) {
  const story = STORIES[fkey];
  return <StoryPlayer list={story.scenes} lsKey={`ash.display.story.${fkey}`} label={story.label} {...rest} />;
}

/** 액자 목록의 작은 그림 — 묶음의 대표 장면 한 순간 */
export const StoryThumb = memo(function StoryThumb({ fkey, C, mode = "e" }) {
  const s = STORIES[fkey];
  if (!s) return null;
  const p = s.scenes[s.thumb.i];
  return <g>{p.render(mode, s.thumb.t, C, paramsOf(p, null))}</g>;
});
