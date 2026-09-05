// ashrain.out — StageFigure v3.0: 3:2 종이 무대 + 컷아웃 레이어 + 타임라인
// - 씬(anim:"stage")은 슬롯 번호로 이미지를 참조: figures 버킷 slots/{n}/{k}.webp
// - 채택본·필터는 figure_slots.meta (테마별) / 라벨·점·선·화살표·호는 앱이 그림(mark)
// - 관리자: ⚙ 편집(레이어 드래그·크기, 재생 노브, JSON) → set_figure RPC 저장
// 좌표계: 무대 폭 = 1 (x,y,w 모두 폭 기준. 무대 높이 = 2/3)
import { useEffect, useRef, useState, useCallback, useMemo } from "react";
import { supabase } from "../supabaseClient";

export const STAGE_H = 2 / 3; // 3:2
const SLOT_ROOT = "slots";

/* ══════════ 슬롯 메타/URL ══════════ */
const metaCache = new Map();
export async function loadSlotMeta(slots) {
  const need = [...new Set(slots)].filter((n) => Number.isFinite(n) && !metaCache.has(n));
  if (need.length) {
    const { data } = await supabase.from("figure_slots").select("slot, meta").in("slot", need);
    for (const r of data || []) metaCache.set(r.slot, r.meta || {});
    for (const n of need) if (!metaCache.has(n)) metaCache.set(n, null); // 미등록
  }
  const out = {};
  for (const n of new Set(slots)) out[n] = metaCache.get(n) ?? null;
  return out;
}
export function bustSlotMeta(n) { metaCache.delete(n); }
export function slotUrl(n, k, v) {
  const { data } = supabase.storage.from("figures").getPublicUrl(`${SLOT_ROOT}/${n}/${k}.webp`);
  return data.publicUrl + (v ? `?v=${encodeURIComponent(v)}` : "");
}
export function adoptedCand(meta, theme) {
  const a = meta?.adopted || {};
  return a[theme] ?? a.dark ?? a.light ?? 1;
}
const FILTER_PRESET = {
  dark: { b: 1, c: 1, s: 1, e: 0 },
  light: { b: 0.94, c: 1.08, s: 1.06, e: 0.12 },
};
export function filterCss(meta, theme) {
  const f = { ...FILTER_PRESET[theme], ...((meta?.filters || {})[theme] || {}) };
  const sh = theme === "light"
    ? "drop-shadow(0 2px 3px rgba(84,54,20,.30))"
    : "drop-shadow(0 0 7px rgba(240,205,130,.16))";
  return `brightness(${f.b}) contrast(${f.c}) saturate(${f.s}) sepia(${f.e}) ${sh}`;
}

/* ══════════ 타임라인 ══════════ */
const EASE = {
  linear: (t) => t,
  in: (t) => t * t * t,
  out: (t) => 1 - Math.pow(1 - t, 3),
  inout: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
};
const ABS_PROPS = ["x", "y", "scale", "fade", "skew", "state", "wipe", "w"];
// rotate만 누적(delta). 나머지는 절대 목표값.
function buildTracks(scene) {
  const base = {};
  for (const L of scene.layers || []) {
    base[L.id] = {
      x: L.x ?? 0.5, y: L.y ?? STAGE_H / 2, w: L.w ?? 0.2, scale: 1,
      fade: L.opacity ?? 1, rotate: L.rotate ?? 0, skew: 0, state: 0, wipe: 1,
    };
  }
  const tracks = {}; // id -> prop -> [{t,d,from,to,ease,loop}]
  const cur = JSON.parse(JSON.stringify(base));
  const tl = [...(scene.tl || [])].sort((a, b) => (a.t || 0) - (b.t || 0));
  for (const tw of tl) {
    const id = tw.target; if (!base[id]) continue;
    tracks[id] = tracks[id] || {};
    const put = (prop, to, delta) => {
      const from = cur[id][prop];
      const seg = { t: tw.t || 0, d: Math.max(1, tw.d || 1), ease: EASE[tw.ease] || EASE.inout, loop: !!tw.loop };
      if (delta) { seg.from = from; seg.to = from + to; seg.delta = to; }
      else { seg.from = from; seg.to = to; }
      (tracks[id][prop] = tracks[id][prop] || []).push(seg);
      cur[id][prop] = seg.to;
    };
    if (tw.rotate != null) put("rotate", tw.rotate, true);
    for (const p of ABS_PROPS) if (tw[p] != null) put(p, tw[p], false);
  }
  let dur = 1200;
  for (const tw of tl) if (!tw.loop) dur = Math.max(dur, (tw.t || 0) + (tw.d || 0));
  return { base, tracks, dur };
}
function sampleTracks({ base, tracks }, time) {
  const st = {};
  for (const id of Object.keys(base)) {
    st[id] = { ...base[id] };
    const tr = tracks[id]; if (!tr) continue;
    for (const prop of Object.keys(tr)) {
      for (const s of tr[prop]) {
        if (s.loop) {
          if (time < s.t) continue;
          if (prop === "rotate") { st[id][prop] = s.from + s.delta * ((time - s.t) / s.d); continue; }
          const p = ((time - s.t) % s.d) / s.d;
          st[id][prop] = s.from + (s.to - s.from) * s.ease(p);
        } else if (time >= s.t + s.d) st[id][prop] = s.to;
        else if (time > s.t) st[id][prop] = s.from + (s.to - s.from) * s.ease((time - s.t) / s.d);
      }
    }
  }
  return st;
}

/* ══════════ CSS ══════════ */
const CSS = `
.sf3 { margin: 14px auto; max-width: 430px; }
.sf3-stage { position: relative; width: 100%; aspect-ratio: 3 / 2; border-radius: 14px; overflow: hidden;
  cursor: pointer; -webkit-user-select: none; user-select: none; touch-action: manipulation; }
.sf3-stage.dark { background: radial-gradient(130% 100% at 50% 12%, #26325a 0%, #1b2544 52%, #121a33 100%);
  border: 1px solid #2c3a66; }
.sf3-stage.light { background:
  radial-gradient(120% 130% at 50% 0%, #faf4e6 0%, #f3ead6 60%, #eadfc4 100%); border: 1px solid #ddd0b4; }
.sf3-noise { position: absolute; inset: 0; pointer-events: none; opacity: .07; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E"); }
.sf3-layer { position: absolute; will-change: transform, opacity; }
.sf3-layer img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain;
  transition: opacity .45s ease; pointer-events: none; -webkit-user-drag: none; }
.sf3-marks { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.sf3-cap { font-size: 12px; color: var(--mut, #64748B); text-align: center; margin: 7px 4px 0; line-height: 1.5; }
.sf3-badge { position: absolute; right: 7px; bottom: 5px; font-size: 8px; letter-spacing: .4px;
  color: rgba(150,150,150,.65); pointer-events: none; font-weight: 700; }
.sf3-gear { position: absolute; top: 7px; right: 7px; z-index: 6; background: var(--card,#fff);
  border: 1px solid var(--bd,#E2E8F0); border-radius: 8px; font-size: 12.5px; padding: 4px 7px; cursor: pointer; }
.sf3-empty { position: absolute; inset: 0; display: flex; flex-direction: column; gap: 6px;
  align-items: center; justify-content: center; text-align: center; padding: 12px; box-sizing: border-box; }
.sf3-empty b { font-size: 13px; color: var(--ink,#475569); }
.sf3-empty span { font-size: 11.5px; color: var(--mut,#64748B); line-height: 1.55; }
/* 편집 패널 */
.sf3-ed { border: 1px solid var(--bd,#DFE3E8); border-radius: 12px; background: var(--card,#fff);
  padding: 10px; margin-top: 8px; font-size: 12.5px; color: var(--ink,#1F2937); }
.sf3-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin: 6px 0; }
.sf3-ed label { font-weight: 700; color: var(--mut,#8A929C); font-size: 12px; }
.sf3-ed select, .sf3-ed input[type=number] { background: var(--in,#F4F6F8); border: 1px solid var(--inbd,#D3D9DF);
  border-radius: 8px; padding: 5px 7px; font-size: 12.5px; color: var(--ink,#1F2937); }
.sf3-ed textarea { width: 100%; min-height: 120px; box-sizing: border-box; font-family: ui-monospace, monospace;
  font-size: 11.5px; background: var(--in,#F4F6F8); border: 1px solid var(--inbd,#D3D9DF); border-radius: 8px; padding: 8px; }
.sf3-btn { border: none; border-radius: 9px; font-size: 12.5px; font-weight: 800; padding: 8px 12px; cursor: pointer;
  background: var(--in,#F4F6F8); color: var(--ink,#1F2937); border: 1px solid var(--inbd,#D3D9DF); }
.sf3-btn.pri { background: var(--ac,#0DA95F); color: #fff; border-color: transparent; }
.sf3-btn.on { border-color: var(--ac,#0DA95F); color: var(--ac,#0DA95F); }
.sf3-warn { color: #DC2626; font-size: 12px; margin-top: 4px; }
.sf3-sel { outline: 2px dashed rgba(230,170,60,.9); outline-offset: 2px; }
.sf3-grip { position: absolute; right: -7px; bottom: -7px; width: 16px; height: 16px; border-radius: 999px;
  background: #E6AA3C; border: 2px solid #fff; cursor: nwse-resize; z-index: 5; }
`;

const INK = { dark: "#EFE4C8", light: "#4A3B25" };
const ACCENT = { dark: "#D9B662", light: "#8A6A2F" };

/* ══════════ 마크(앱이 그리는 도형) ══════════ */
function MarkSvg({ marks, st, theme }) {
  const S = 300, H = S * STAGE_H;
  return (
    <svg className="sf3-marks" viewBox={`0 0 ${S} ${H}`} preserveAspectRatio="none">
      {marks.map((m) => {
        const o = st[m.id] ? st[m.id].fade : (m.opacity ?? 1);
        if (o <= 0.01) return null;
        const col = m.color === "accent" ? ACCENT[theme] : m.color || INK[theme];
        const k = { key: m.id, opacity: o };
        if (m.mark === "dot")
          return <circle {...k} cx={m.x * S} cy={m.y * S} r={(m.w || 0.02) * S / 2} fill={col} />;
        if (m.mark === "label")
          return <text {...k} x={m.x * S} y={m.y * S} textAnchor="middle" dominantBaseline="middle"
            fontSize={(m.size || 0.045) * S} fontWeight={m.weight || 800} fill={col}
            style={{ fontFamily: "'Pretendard Variable', Pretendard, serif" }}>{m.text}</text>;
        if (m.mark === "line" || m.mark === "arrow") {
          const el = [<line {...k} x1={m.x1 * S} y1={m.y1 * S} x2={m.x2 * S} y2={m.y2 * S}
            stroke={col} strokeWidth={(m.w || 0.006) * S} strokeDasharray={m.dash ? "4 4" : undefined}
            strokeLinecap="round" />];
          if (m.mark === "arrow") {
            const a = Math.atan2(m.y2 - m.y1, m.x2 - m.x1), L = 0.024 * S;
            const px = m.x2 * S, py = m.y2 * S;
            el.push(<path key={m.id + "h"} opacity={o} fill={col}
              d={`M ${px} ${py} L ${px - L * Math.cos(a - 0.42)} ${py - L * Math.sin(a - 0.42)} L ${px - L * Math.cos(a + 0.42)} ${py - L * Math.sin(a + 0.42)} Z`} />);
          }
          return el;
        }
        if (m.mark === "arc") {
          const r = m.r * S, a1 = (m.a1 || 0) * Math.PI / 180, a2 = (m.a2 || 90) * Math.PI / 180;
          const x1 = m.cx * S + r * Math.cos(a1), y1 = m.cy * S + r * Math.sin(a1);
          const x2 = m.cx * S + r * Math.cos(a2), y2 = m.cy * S + r * Math.sin(a2);
          const lg = Math.abs(a2 - a1) > Math.PI ? 1 : 0;
          return <path {...k} d={`M ${x1} ${y1} A ${r} ${r} 0 ${lg} 1 ${x2} ${y2}`} fill="none"
            stroke={col} strokeWidth={(m.w || 0.006) * S} strokeDasharray={m.dash ? "4 4" : undefined} strokeLinecap="round" />;
        }
        return null;
      })}
    </svg>
  );
}

/* ══════════ 무대 씬 ══════════ */
export function StageScene({ scene, figure, conceptId, blockId, isAdmin = false, theme = "light" }) {
  const [sc, setSc] = useState(scene);              // 편집 반영본
  useEffect(() => setSc(scene), [scene]);
  const [meta, setMeta] = useState(null);           // slot -> meta|null
  const [dims, setDims] = useState({});             // slot -> naturalW/H 비율
  const [time, setTime] = useState(0);
  const [edit, setEdit] = useState(false);
  const [selId, setSelId] = useState(null);
  const stageRef = useRef(null);
  const raf = useRef(0);
  const playedOnce = useRef(false);

  const imgLayers = useMemo(() => (sc.layers || []).filter((l) => !l.mark), [sc]);
  const markLayers = useMemo(() => (sc.layers || []).filter((l) => l.mark && !l.parent), [sc]);
  const childMarks = useMemo(() => (sc.layers || []).filter((l) => l.mark && l.parent), [sc]);
  const slots = useMemo(() => imgLayers.flatMap((l) => l.slots || [l.slot]).filter(Number.isFinite), [imgLayers]);
  const tlData = useMemo(() => buildTracks(sc), [sc]);
  const play = sc.play || {};
  const hasLoop = (sc.tl || []).some((t) => t.loop) || play.loop;

  useEffect(() => { let on = true; loadSlotMeta(slots).then((m) => on && setMeta(m)); return () => { on = false; }; }, [JSON.stringify(slots)]);

  const start = useCallback(() => {
    cancelAnimationFrame(raf.current);
    if (typeof matchMedia !== "undefined" && matchMedia("(prefers-reduced-motion: reduce)").matches) { setTime(tlData.dur); return; }
    const t0 = performance.now();
    const spd = play.speed || 1;
    const tick = (now) => {
      let t = (now - t0) * spd;
      const total = hasLoop ? Infinity : tlData.dur;
      if (play.reverse) t = Math.max(0, tlData.dur - t);
      if (!hasLoop && ((play.reverse && t <= 0) || (!play.reverse && t >= total))) {
        setTime(play.reverse ? 0 : tlData.dur);
        if (play.loop) raf.current = requestAnimationFrame(() => setTimeout(start, 900));
        return;
      }
      setTime(t);
      raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
  }, [tlData, play.speed, play.reverse, play.loop, hasLoop]);

  useEffect(() => {
    const el = stageRef.current;
    if (!el || typeof IntersectionObserver === "undefined") { start(); return; }
    const ob = new IntersectionObserver(([e]) => {
      if (e.intersectionRatio >= 0.6 && !playedOnce.current) { playedOnce.current = true; start(); }
    }, { threshold: [0.6] });
    ob.observe(el);
    return () => { ob.disconnect(); cancelAnimationFrame(raf.current); };
  }, [start]);

  const st = sampleTracks(tlData, time);
  const registered = meta && slots.length > 0 && slots.every((n) => meta[n]);
  const missing = meta ? slots.filter((n) => !meta[n]) : [];

  /* 편집: 드래그 */
  const drag = useRef(null);
  const onPointerDown = (e, L) => {
    if (!edit) return;
    e.preventDefault(); e.stopPropagation(); setSelId(L.id);
    const r = stageRef.current.getBoundingClientRect();
    drag.current = { id: L.id, mode: e.target.dataset.grip ? "size" : "move",
      sx: e.clientX, sy: e.clientY, w: r.width, x0: L.x ?? 0.5, y0: L.y ?? STAGE_H / 2, w0: L.w ?? 0.2 };
    const mv = (ev) => {
      const d = drag.current; if (!d) return;
      const dx = (ev.clientX - d.sx) / d.w, dy = (ev.clientY - d.sy) / d.w;
      setSc((s) => ({ ...s, layers: s.layers.map((x) => x.id !== d.id ? x :
        d.mode === "move" ? { ...x, x: +(d.x0 + dx).toFixed(3), y: +(d.y0 + dy).toFixed(3) }
                          : { ...x, w: +Math.max(0.03, d.w0 + dx * 2).toFixed(3) }) }));
    };
    const up = () => { drag.current = null; window.removeEventListener("pointermove", mv); window.removeEventListener("pointerup", up); };
    window.addEventListener("pointermove", mv); window.addEventListener("pointerup", up);
  };

  const badge = `${conceptId}·${blockId}·${sc.id}`;
  return (
    <div className="sf3">
      <style>{CSS}</style>
      <div style={{ position: "relative" }}>
        {isAdmin && <button className="sf3-gear" onClick={() => setEdit((v) => !v)} title="무대 편집">{edit ? "✕" : "⚙️"}</button>}
        <div ref={stageRef} className={`sf3-stage ${theme}`}
          onClick={() => { if (!edit) { playedOnce.current = true; start(); } else setSelId(null); }}>
          <div className="sf3-noise" />
          {imgLayers.map((L) => {
            const s = st[L.id] || {};
            const slotList = L.slots || [L.slot];
            const stateIdx = Math.round(s.state || 0);
            const m0 = meta?.[slotList[0]];
            const ar = dims[slotList[Math.min(stateIdx, slotList.length - 1)]] || dims[slotList[0]] || 1;
            const w = s.w ?? L.w ?? 0.2, h = w / ar;
            const rot = (s.rotate || 0), sk = s.skew || 0, scl = (s.scale ?? 1) * (L.flip ? -1 : 1);
            const pv = L.pivot || [0.5, 0.5];
            return (
              <div key={L.id} className={"sf3-layer" + (edit && selId === L.id ? " sf3-sel" : "")}
                onPointerDown={(e) => onPointerDown(e, L)}
                style={{
                  left: `${(s.x - w / 2) * 100}%`, top: `${((s.y - h / 2) / STAGE_H) * 100}%`,
                  width: `${w * 100}%`, height: `${(h / STAGE_H) * 100}%`,
                  transformOrigin: `${pv[0] * 100}% ${pv[1] * 100}%`,
                  transform: `rotate(${rot}deg) skewX(${sk}deg) scaleX(${scl}) scaleY(${s.scale ?? 1})`,
                  opacity: s.fade, zIndex: L.z ?? 1, pointerEvents: edit ? "auto" : "none",
                  clipPath: (s.wipe ?? 1) >= 1 ? undefined : `inset(0 ${(1 - (s.wipe ?? 1)) * 100}% 0 0)`,
                  cursor: edit ? "grab" : undefined,
                }}>
                {slotList.map((n, i) => {
                  const mm = meta?.[n];
                  if (!mm) return null;
                  const k = adoptedCand(mm, theme);
                  return <img key={n} src={slotUrl(n, k, mm?.updated || "")} alt=""
                    onLoad={(e) => { const im = e.target; if (!dims[n]) setDims((d) => ({ ...d, [n]: im.naturalWidth / im.naturalHeight })); }}
                    style={{ opacity: i === Math.min(stateIdx, slotList.length - 1) ? 1 : 0, filter: filterCss(mm, theme) }} />;
                })}
                {childMarks.filter((c) => c.parent === L.id).map((c) => {
                  const co = st[c.id] ? st[c.id].fade : (c.opacity ?? 1);
                  const col = c.color === "accent" ? ACCENT[theme] : c.color || INK[theme];
                  return c.mark === "dot"
                    ? <span key={c.id} style={{ position: "absolute", left: `${(c.x - (c.w || .05) / 2) * 100}%`, top: `${(c.y - (c.w || .05) / 2) * 100}%`, width: `${(c.w || .05) * 100}%`, aspectRatio: "1", borderRadius: "999px", background: col, opacity: co }} />
                    : <span key={c.id} style={{ position: "absolute", left: `${c.x * 100}%`, top: `${c.y * 100}%`, transform: "translate(-50%,-50%)", color: col, opacity: co, fontWeight: 800, fontSize: `${(c.size || .12) * 100}cqw` }}>{c.text}</span>;
                })}
                {edit && selId === L.id && <span className="sf3-grip" data-grip onPointerDown={(e) => onPointerDown(e, L)} />}
              </div>
            );
          })}
          <MarkSvg marks={markLayers} st={st} theme={theme} />
          {meta && missing.length > 0 && (
            <div className="sf3-empty">
              <b>{sc.label}</b>
              <span>{sc.caption || sc.desc || ""}</span>
              <span>🖼 슬롯 {missing.join(", ")}번 이미지 대기{isAdmin ? " — 이미지 관리에서 등록" : ""}</span>
            </div>
          )}
          {isAdmin && <span className="sf3-badge">{badge}</span>}
        </div>
      </div>
      {sc.caption ? <p className="sf3-cap">{sc.caption}</p> : null}
      {edit && <StageEditor sc={sc} setSc={setSc} selId={selId} figure={figure}
        conceptId={conceptId} blockId={blockId} onReplay={start} />}
    </div>
  );
}

/* ══════════ 무대 편집 패널 ══════════ */
function StageEditor({ sc, setSc, selId, figure, conceptId, blockId, onReplay }) {
  const [jsonMode, setJsonMode] = useState(false);
  const [txt, setTxt] = useState("");
  const [warn, setWarn] = useState("");
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const sel = (sc.layers || []).find((l) => l.id === selId);
  const play = sc.play || {};
  const setPlay = (p) => setSc((s) => ({ ...s, play: { ...s.play, ...p } }));
  const setLayer = (patch) => setSc((s) => ({ ...s, layers: s.layers.map((l) => l.id === selId ? { ...l, ...patch } : l) }));

  const validate = (s) => {
    if (!s || s.anim !== "stage" || !Array.isArray(s.layers)) return "anim:'stage' + layers[] 필요";
    const ids = s.layers.map((l) => l.id);
    if (new Set(ids).size !== ids.length) return "레이어 id 중복";
    for (const t of s.tl || []) if (!ids.includes(t.target)) return `tl target 없음: ${t.target}`;
    return "";
  };
  const save = async () => {
    const w = validate(sc); if (w) { setWarn(w); return; }
    setBusy(true); setWarn("");
    const scenes = (figure.scenes || []).map((s) => (s.id === sc.id ? sc : s));
    const { error } = await supabase.rpc("set_figure", {
      p_concept: conceptId, p_block: blockId, p_figure: { ...figure, kind: figure.kind || "animset", scenes },
    });
    setBusy(false);
    if (error) setWarn("저장 실패: " + error.message + " (figure_slots SQL 실행 여부 확인)");
    else { setSaved(true); setTimeout(() => setSaved(false), 2000); }
  };

  return (
    <div className="sf3-ed">
      <div className="sf3-row">
        <label>재생</label>
        <select value={play.speed || 1} onChange={(e) => setPlay({ speed: +e.target.value })}>
          {[0.25, 0.5, 0.75, 1, 1.5, 2, 3].map((v) => <option key={v} value={v}>{v}×</option>)}
        </select>
        <button className={"sf3-btn" + (play.reverse ? " on" : "")} onClick={() => setPlay({ reverse: !play.reverse })}>역재생</button>
        <button className={"sf3-btn" + (play.loop ? " on" : "")} onClick={() => setPlay({ loop: !play.loop })}>반복</button>
        <button className="sf3-btn" onClick={onReplay}>▶ 다시</button>
        <span style={{ flex: 1 }} />
        <button className={"sf3-btn" + (jsonMode ? " on" : "")} onClick={() => { setJsonMode(!jsonMode); setTxt(JSON.stringify(sc, null, 1)); }}>JSON</button>
        <button className="sf3-btn pri" disabled={busy} onClick={save}>{busy ? "…" : saved ? "저장됨 ✓" : "저장"}</button>
      </div>
      {sel && !sel.mark && (
        <div className="sf3-row">
          <label>#{sel.slots ? sel.slots.join("/") : sel.slot} {sel.id}</label>
          x <input type="number" step="0.01" value={sel.x ?? 0.5} onChange={(e) => setLayer({ x: +e.target.value })} style={{ width: 62 }} />
          y <input type="number" step="0.01" value={sel.y ?? 0.33} onChange={(e) => setLayer({ y: +e.target.value })} style={{ width: 62 }} />
          w <input type="number" step="0.01" value={sel.w ?? 0.2} onChange={(e) => setLayer({ w: +e.target.value })} style={{ width: 62 }} />
          회전 <input type="number" step="1" value={sel.rotate ?? 0} onChange={(e) => setLayer({ rotate: +e.target.value })} style={{ width: 56 }} />
          <button className={"sf3-btn" + (sel.flip ? " on" : "")} onClick={() => setLayer({ flip: !sel.flip })}>좌우반전</button>
          <button className="sf3-btn" onClick={() => setLayer({ z: (sel.z ?? 1) + 1 })}>앞으로</button>
          <button className="sf3-btn" onClick={() => setLayer({ z: Math.max(0, (sel.z ?? 1) - 1) })}>뒤로</button>
        </div>
      )}
      {!sel && <div className="sf3-row" style={{ color: "var(--mut)" }}>무대 위 레이어를 탭하면 선택 · 드래그로 이동 · 우하단 점으로 크기</div>}
      {jsonMode && (
        <>
          <textarea value={txt} onChange={(e) => setTxt(e.target.value)} spellCheck={false} />
          <div className="sf3-row">
            <button className="sf3-btn" onClick={() => {
              try { const s = JSON.parse(txt); const w = validate(s); if (w) { setWarn(w); return; } setWarn(""); setSc(s); }
              catch (e) { setWarn("JSON 파싱 실패: " + e.message); }
            }}>적용</button>
            <span style={{ fontSize: 11.5, color: "var(--mut)" }}>붙여넣기 → 적용 → 저장 (저장해야 DB 반영)</span>
          </div>
        </>
      )}
      {warn && <div className="sf3-warn">{warn}</div>}
    </div>
  );
}

export default StageScene;
