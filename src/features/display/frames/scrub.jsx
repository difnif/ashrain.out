// ashrain.out — 해설 액자의 두 막대 (frames/scrub.jsx)
//   긴 막대(아래) — 문항 이동: 동그라미를 끌거나 막대를 누르면 그 문항으로. 단계가 바뀌는 자리에 눈금 · 이름.
//   짧은 막대(옆, 세로) — 풀이 이동: 지금 문항의 풀이 단계(문제 · 방침 · 판서 줄 · 답)마다 눈금, 끌거나 누르면 가까운 단계로.
// 해설 액자(일차함수 그래프 그리기 · 10단계 계산 · 그래프와 넓이 · 경우의 수와 확률 100제)가 StoryPlayer 의 scrub 로,
//   경우의 수와 확률 100제의 듀얼 모드가 판마다 쓴다. 조작 막대처럼 화면을 건드리면 나타났다가 숨는다(끄는 중에는 계속).
// 장면(scene)이 가질 것: no(번호) · grp?(단계 이름 — 눈금) · marks [{ t(장면 시각 ms), lab(이름) }].
import { useRef, useState } from "react";

/** 풀이 단계 눈금 — 문제 · 방침 · 판서 줄 · 답(시각은 1배속 판, sp 로 나눠 장면 시각으로) */
export function stepMarks(P, lines, sp = 1, planTag = "방침") {
  const snip = (s) => {
    const t = String(s || "").replace(/\{(-?\d+)\/(\d+)\}/g, "$1/$2").replace(/\$/g, "");
    return t.length > 22 ? t.slice(0, 21) + "…" : t;
  };
  const out = [{ t: 0, lab: "문제" }];
  if (P.plan) out.push({ t: P.plan[0] / sp, lab: planTag });
  P.lines.forEach((L, i) => {
    const ln = lines[i] || {};
    out.push({ t: L.a / sp, lab: ln.pre ? `${ln.pre}` : `${i + 1}줄 · ${snip(ln.s ?? ln.text)}` });
  });
  out.push({ t: P.ans / sp, lab: "답" });
  return out;
}

const SCRUB_CSS = `
.scb-long { position: absolute; z-index: 7; height: 3.6cqw; display: flex; align-items: center; cursor: pointer; touch-action: none;
  opacity: 0; pointer-events: none; transition: opacity .3s; }
.scb-long.show, .scb-short.show { opacity: 1; pointer-events: auto; }
.scb-long.full { left: 16cqw; right: 16cqw; bottom: .9cqw; }
.scb-long.L { left: 4cqw; width: 42cqw; bottom: .7cqw; }
.scb-long.R { left: 54cqw; width: 42cqw; bottom: .7cqw; }
.scb-long .tr { position: relative; width: 100%; height: .5cqw; border-radius: 999px; background: var(--chipbd); }
.scb-long .fill { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 999px; background: var(--gold); opacity: .45; }
.scb-long .tick { position: absolute; top: -.45cqw; width: 2px; height: 1.4cqw; background: var(--soft); opacity: .55; }
.scb-long .tl { position: absolute; top: 1.05cqw; transform: translateX(-2px); font-size: .82cqw; font-weight: 700; color: var(--soft); white-space: nowrap; }
.scb-knob { position: absolute; top: 50%; width: 2.5cqw; height: 2.5cqw; margin: -1.25cqw 0 0 -1.25cqw; border-radius: 999px; background: var(--gold);
  color: #1c2647; display: grid; place-items: center; font-size: 1.05cqw; font-weight: 900; box-shadow: 0 .2cqw .8cqw rgba(0,0,0,.35);
  font-variant-numeric: tabular-nums; }
.dsp-light .scb-knob { color: #fffdf6; }
.scb-tip { position: absolute; bottom: 2.2cqw; transform: translateX(-50%); white-space: nowrap; font-size: 1.1cqw; font-weight: 800;
  color: var(--ink); background: var(--chip); border: 1px solid var(--chipbd); border-radius: 999px; padding: .3cqw 1cqw; pointer-events: none; }
.scb-short { position: absolute; z-index: 7; width: 3.6cqw; top: 26%; height: 46%; display: flex; justify-content: center; cursor: pointer;
  touch-action: none; opacity: 0; pointer-events: none; transition: opacity .3s; }
.scb-short.full, .scb-short.R { right: .4cqw; }
.scb-short.L { left: .4cqw; }
.scb-short .tr { position: relative; width: .5cqw; height: 100%; border-radius: 999px; background: var(--chipbd); }
.scb-short .fill { position: absolute; left: 0; right: 0; top: 0; border-radius: 999px; background: var(--gold); opacity: .45; }
.scb-short .tick { position: absolute; left: -.5cqw; width: 1.5cqw; height: 2px; background: var(--soft); opacity: .6; }
.scb-short .tick.on { background: var(--gold); opacity: 1; }
.scb-short .scb-knob { left: 50%; width: 1.9cqw; height: 1.9cqw; margin: -.95cqw 0 0 -.95cqw; }
.scb-short .scb-tip { bottom: auto; transform: translateY(-50%); }
.scb-short.full .scb-tip, .scb-short.R .scb-tip { right: 3.2cqw; }
.scb-short.L .scb-tip { left: 3.2cqw; }
`;

/** 끌기: 막대 위 위치(0 ~ 1)를 알려 준다 — 누르는 순간부터 놓을 때까지 */
function useDrag(axis, onMove, onUp) {
  const ref = useRef(null);
  const frac = (e) => {
    const r = ref.current.getBoundingClientRect();
    const v = axis === "x" ? (e.clientX - r.left) / r.width : (e.clientY - r.top) / r.height;
    return Math.max(0, Math.min(1, v));
  };
  const handlers = {
    onPointerDown: (e) => { e.stopPropagation(); e.currentTarget.setPointerCapture?.(e.pointerId); onMove(frac(e)); },
    onPointerMove: (e) => { if (e.currentTarget.hasPointerCapture?.(e.pointerId)) onMove(frac(e)); },
    onPointerUp: (e) => { e.stopPropagation(); onUp(frac(e)); },
    onPointerCancel: () => onUp(null),
  };
  return [ref, handlers];
}

/**
 * variant: "full"(무대 전체 — 긴 막대 아래 가운데, 짧은 막대 오른쪽) | "L" | "R"(듀얼 모드의 왼쪽 · 오른쪽 판)
 * scenes · idx · onPick(i) — 문항 / t · dur · marks · onSeek(t) — 지금 문항의 풀이
 */
export function Scrub({ variant = "full", show, scenes, idx, onPick, t, dur, marks, onSeek, poke }) {
  const n = scenes.length;
  const [dragI, setDragI] = useState(null);          // 끄는 중인 문항 번호(목록 자리)
  const [dragM, setDragM] = useState(null);          // 끄는 중인 풀이 단계
  const iOf = (f) => Math.round(f * (n - 1));
  const [lRef, lH] = useDrag("x", (f) => { setDragI(iOf(f)); poke?.(); }, (f) => {
    if (f != null) { const i = iOf(f); if (i !== idx) onPick(i); }
    setDragI(null);
  });
  const ms = marks && marks.length ? marks : null;
  const near = (f) => {
    const tt = f * dur;
    let best = 0;
    ms.forEach((m, k) => { if (Math.abs(m.t - tt) < Math.abs(ms[best].t - tt)) best = k; });
    return best;
  };
  const [sRef, sH] = useDrag("y", (f) => { if (ms) { setDragM(near(f)); poke?.(); } }, (f) => {
    if (ms && f != null) onSeek(ms[near(f)].t + 1);
    setDragM(null);
  });
  const shown = show || dragI != null || dragM != null;
  const pos = (i) => (n > 1 ? (i / (n - 1)) * 100 : 0);
  const ki = dragI != null ? dragI : idx;
  // 단계가 바뀌는 자리
  const ticks = [];
  scenes.forEach((s, i) => { if (s.grp && (i === 0 || scenes[i - 1].grp !== s.grp)) ticks.push({ i, lab: s.grp }); });
  const showTl = ticks.length > 1 && ticks.length <= 12;
  // 지금 풀이 단계
  let cm = 0;
  if (ms) ms.forEach((m, k) => { if (t >= m.t) cm = k; });
  const km = dragM != null ? dragM : null;
  const ky = (km != null ? ms[km].t : t) / Math.max(1, dur) * 100;
  return (
    <>
      <style>{SCRUB_CSS}</style>
      <div className={`scb-long ${variant}${shown ? " show" : ""}`} ref={lRef} {...lH} role="slider" aria-label="문항 이동"
        aria-valuemin={1} aria-valuemax={n} aria-valuenow={(scenes[ki] || {}).no}>
        <div className="tr">
          <div className="fill" style={{ width: `${pos(ki)}%` }} />
          {ticks.length > 1 && ticks.map((k) => (
            <span key={k.i}>
              <i className="tick" style={{ left: `${pos(k.i)}%` }} />
              {showTl && <b className="tl" style={{ left: `${pos(k.i)}%` }}>{k.lab}</b>}
            </span>
          ))}
          <div className="scb-knob" style={{ left: `${pos(ki)}%` }}>{(scenes[ki] || {}).no}</div>
          {dragI != null && <div className="scb-tip" style={{ left: `${pos(ki)}%` }}>{`${scenes[ki].no}번${scenes[ki].grp ? ` · ${scenes[ki].grp}` : ""}`}</div>}
        </div>
      </div>
      {ms && (
        <div className={`scb-short ${variant}${shown ? " show" : ""}`} ref={sRef} {...sH} role="slider" aria-label="풀이 이동"
          aria-valuemin={1} aria-valuemax={ms.length} aria-valuenow={(km != null ? km : cm) + 1}>
          <div className="tr">
            <div className="fill" style={{ height: `${Math.min(100, ky)}%` }} />
            {ms.map((m, k) => <i key={k} className={"tick" + (k === (km != null ? km : cm) ? " on" : "")} style={{ top: `${(m.t / Math.max(1, dur)) * 100}%` }} />)}
            <div className="scb-knob" style={{ top: `${Math.min(100, ky)}%` }} />
            {km != null && <div className="scb-tip" style={{ top: `${(ms[km].t / Math.max(1, dur)) * 100}%` }}>{ms[km].lab}</div>}
          </div>
        </div>
      )}
    </>
  );
}
