// 우물 추천 — 콘텐츠를 꾹 누르면 화면 가운데에 우물이 떠오르고, 둘레에 이어지는 콘텐츠 6가지가 뜬다.
// 누른 채로 손가락을 옮겨 한 콘텐츠 위에서 떼면 그 콘텐츠가 열리고, 우물이나 빈 곳에서 떼면 원래 화면 그대로.
// 프린트가 있는 콘텐츠(단원 100제 · 유형 · 주차별 회차)면 위쪽에 「📄 프린트」가 함께 뜬다 — 그 위에서 떼면 그 콘텐츠의
//   문제지 · 해설지 · 빠른 정답 · OMR 받기 판(components/AvPrintSheet.jsx)이 열린다.
//   쓰는 곳: pages/Study.jsx(시청각 학습 › 문제 풀이 해설). 추천은 lib/recommend.js — 학습 기록이 넉넉하면 숙달도 맞춤,
//   없거나 모자라면 교육과정 단원 지도(lib/units.js)로 고르는 기본 추천. 카드의 rel 이 추천 이유(약한 앞 단원 · 이어서 · 다음 단원 도전 …).
//   우물 그림은 탭바 우물과 같은 1장(components/Well.jsx — 관리자가 바꾼 그림이 있으면 그것).
// 손 다루기: 누르고 0.42초 동안 거의 움직이지 않으면 뜬다(그 전에 움직이면 보통 스크롤). 뜬 동안은 화면이 밀리지 않게 touchmove 를 막고,
//   손을 뗀 뒤 따라오는 click 은 삼킨다(그냥 누른 것으로 열리지 않게). 마우스로 길게 눌러도 같다.
import { useCallback, useEffect, useRef, useState } from "react";
import { WELL_BUNDLED, useWellImg } from "./Well.jsx";
import { unitLabel } from "../lib/units";

const HOLD = 420;       // ms — 꾹 누르기
const SLOP = 10;        // px — 이만큼 움직이면 꾹 누르기가 아니다(스크롤)
const HEX = [-90, -30, 30, 90, 150, 210];
const ANGS = { 1: [-90], 2: [-90, 90], 3: [-90, 30, 150], 4: [-30, 30, 150, 210], 5: [-90, -30, 30, 150, 210], 6: HEX };

/** 우물 · 카드 자리 — 세로 휴대폰에서도 카드가 우물과 겹치지 않게 육각 자리(위 · 아래로 길게)
 *   위 TOP(누른 콘텐츠 · 📄 프린트) · 아래 BOT(안내 글) 띠는 비워 둔다 — 키가 낮은 화면(가로 휴대폰)이면 위 · 아래 카드를 우물 쪽으로 당긴다 */
const TOP = 76, BOT = 46;
export function wellLayout(n, vw, vh) {
  const cx = vw / 2;
  const cw = Math.min(182, vw * 0.44), ch = 60;
  const D = Math.min(170, vw * 0.36, vh * 0.24);
  const rx = Math.min(Math.max(vw / 2 - cw / 2 - 10, 96), 300);
  const ry0 = Math.min(Math.max(vh * 0.3, 150), 270), need = ry0 + ch / 2 + 4;
  let cy = vh / 2;
  if (cy - TOP < need || vh - BOT - cy < need) cy = (TOP + vh - BOT) / 2;      // 키 낮은 화면 — 위 · 아래 띠 사이 가운데로
  const fit = Math.min(cy - TOP, vh - BOT - cy) - ch / 2 - 4;
  const ry = Math.max(Math.min(ry0, fit), D / 2 + ch / 2 + 4);
  const angs = ANGS[Math.min(n, 6)] || [];
  return { cx, cy, D, cw, ch, pos: angs.map((a) => ({ x: cx + rx * Math.cos((a * Math.PI) / 180), y: cy + ry * Math.sin((a * Math.PI) / 180) })) };
}

/**
 * useWellPick({ related, onGo, onPrint?, canPrint? }) → { bind(item, onTap), overlay, pressing }
 *   related(item) → 추천 콘텐츠 배열(.key · .icon · .short|.title · .rel · .grade · .unit) — 최대 6
 *   onGo(item) → 고른 콘텐츠 열기 · bind 는 목록 단추에 펼쳐 넣는다(onClick 까지 대신 단다)
 *   onPrint(item) → 「📄 프린트」 위에서 뗐을 때(누른 콘텐츠) · canPrint(item) → 그 콘텐츠에 프린트가 있나(없으면 「📄 프린트」를 띄우지 않는다)
 */
export function useWellPick({ related, onGo, onPrint = null, canPrint = null }) {
  const [st, setSt] = useState(null);           // { item, cards, cx, cy, D, hover }
  const [pressing, setPressing] = useState(null);
  const R = useRef({ timer: 0, id: null, x0: 0, y0: 0, item: null, active: false, swallow: false, st: null });
  const prRef = useRef(null);
  const img = useWellImg();

  const reset = useCallback(() => {
    clearTimeout(R.current.timer);
    R.current.active = false;
    R.current.st = null;
    setSt(null);
    setPressing(null);
  }, []);

  useEffect(() => {
    const stop = (e) => { if (R.current.active) e.preventDefault(); };     // 우물이 떠 있는 동안 화면이 밀리지 않게
    const esc = (e) => { if (e.key === "Escape" && R.current.active) reset(); };
    window.addEventListener("touchmove", stop, { passive: false });
    window.addEventListener("keydown", esc);
    window.addEventListener("blur", reset);
    return () => { window.removeEventListener("touchmove", stop); window.removeEventListener("keydown", esc); window.removeEventListener("blur", reset); clearTimeout(R.current.timer); };
  }, [reset]);

  const hoverAt = (s, x, y) => {
    const pr = s.print && prRef.current?.getBoundingClientRect();
    if (pr && x >= pr.left - 8 && x <= pr.right + 8 && y >= pr.top - 8 && y <= pr.bottom + 8) return "print";
    const i = s.cards.findIndex((c) => Math.abs(x - c.x) <= s.cw / 2 + 8 && Math.abs(y - c.y) <= s.ch / 2 + 8);
    if (i >= 0) return i;
    return Math.hypot(x - s.cx, y - s.cy) <= s.D / 2 + 6 ? "well" : null;
  };

  const open = (item, x, y) => {
    const rel = (related(item) || []).slice(0, 6);
    const L = wellLayout(rel.length, window.innerWidth, window.innerHeight);
    const s = { item, cx: L.cx, cy: L.cy, D: L.D, cw: L.cw, ch: L.ch, cards: rel.map((it, i) => ({ it, ...L.pos[i] })), hover: null,
      print: !!onPrint && (!canPrint || canPrint(item)) };
    s.hover = hoverAt(s, x, y);
    R.current.active = true;
    R.current.st = s;
    try { navigator.vibrate?.(12); } catch { /* 무시 */ }
    setPressing(null);
    setSt(s);
  };

  const bind = (item, onTap) => ({
    onPointerDown: (e) => {
      if (e.button && e.button !== 0) return;
      clearTimeout(R.current.timer);
      R.current = { ...R.current, id: e.pointerId, x0: e.clientX, y0: e.clientY, x: e.clientX, y: e.clientY, item, active: false, swallow: false };
      try { e.currentTarget.setPointerCapture?.(e.pointerId); } catch { /* 무시 */ }
      setPressing(item.key);
      R.current.timer = setTimeout(() => open(item, R.current.x, R.current.y), HOLD);
    },
    onPointerMove: (e) => {
      const r = R.current;
      if (e.pointerId !== r.id) return;
      r.x = e.clientX; r.y = e.clientY;
      if (!r.active) {
        if (Math.hypot(e.clientX - r.x0, e.clientY - r.y0) > SLOP) { clearTimeout(r.timer); setPressing(null); }
        return;
      }
      const h = hoverAt(r.st, e.clientX, e.clientY);
      if (h !== r.st.hover) { r.st = { ...r.st, hover: h }; setSt(r.st); }
    },
    onPointerUp: (e) => {
      const r = R.current;
      if (e.pointerId !== r.id) return;
      clearTimeout(r.timer);
      if (!r.active) { setPressing(null); return; }
      r.swallow = true;                                   // 뒤따르는 click 은 삼킨다
      const h = hoverAt(r.st, e.clientX, e.clientY);
      const pick = typeof h === "number" ? r.st.cards[h].it : null;
      const item0 = r.st.item;
      reset();
      if (h === "print") onPrint?.(item0);
      else if (pick) onGo(pick);
    },
    onPointerCancel: () => { clearTimeout(R.current.timer); if (R.current.active) R.current.swallow = true; reset(); },
    onContextMenu: (e) => e.preventDefault(),            // 길게 누를 때 뜨는 메뉴 막기
    onClick: (e) => {
      if (R.current.swallow) { R.current.swallow = false; e.preventDefault(); return; }
      onTap?.(e);
    },
  });

  const overlay = st && <WellOverlay st={st} img={img?.url || WELL_BUNDLED} prRef={prRef} />;
  return { bind, overlay, pressing };
}

function WellOverlay({ st, img, prRef }) {
  const { item, cards, cx, cy, D, cw, ch, hover } = st;
  const on = typeof hover === "number" ? cards[hover].it : null;
  return (
    <div className="wpk" aria-live="polite">
      <style>{WPK_CSS}</style>
      <div className="wpk-head">
        <div className="wpk-top">
          <span className="i" aria-hidden="true">{item.icon}</span>
          <b>{item.short || item.title}</b>
          <small>{unitLabel(item.unit)}</small>
        </div>
        {st.print && <div ref={prRef} className={"wpk-pr" + (hover === "print" ? " on" : "")}><span aria-hidden="true">📄</span>프린트</div>}
      </div>
      <svg className="wpk-lines" width="100%" height="100%" aria-hidden="true">
        {cards.map((c, i) => {
          const mx = (cx + c.x) / 2 + (c.y - cy) * 0.18, my = (cy + c.y) / 2 - (c.x - cx) * 0.18;
          return <path key={c.it.key} d={`M${cx} ${cy} Q${mx} ${my} ${c.x} ${c.y}`} className={hover === i ? "on" : ""} />;
        })}
      </svg>
      <div className={"wpk-well" + (hover === "well" ? " on" : "")} style={{ left: cx, top: cy, width: D, height: D }}>
        <span className="wpk-rip" /><span className="wpk-rip r2" />
        <img src={img} alt="" draggable="false" />
      </div>
      {cards.map((c, i) => (
        <div key={c.it.key} className="wpk-c" data-key={c.it.key} style={{ left: c.x, top: c.y, width: cw, height: ch, "--dx": `${cx - c.x}px`, "--dy": `${cy - c.y}px`, "--i": i }}>
          <div className={"wpk-card" + (hover === i ? " on" : "")}>
            <span className="i" aria-hidden="true">{c.it.icon}</span>
            <span className="t"><b>{c.it.short || c.it.title}</b><small><em>{c.it.rel}</em> · {c.it.grade}</small></span>
          </div>
        </div>
      ))}
      {!cards.length && <div className="wpk-none" style={{ top: cy + D / 2 + 28 }}>이어지는 콘텐츠가 아직 없어요</div>}
      <div className="wpk-hint">
        {on ? <>놓으면 <b>{on.short || on.title}</b> 열기</> : hover === "print" ? <>놓으면 <b>프린트 받기</b> — 문제지 · 해설지 · 빠른 정답 · OMR</>
          : hover === "well" ? "우물에서 놓으면 그대로예요" : st.print ? "콘텐츠 위에서 놓으면 열기 · 위 「📄 프린트」에서 놓으면 프린트 받기" : "손가락을 옮겨 콘텐츠 위에서 놓으세요 · 빈 곳에서 놓으면 그대로"}
      </div>
    </div>
  );
}

const WPK_CSS = `
.wpk { position: fixed; inset: 0; z-index: 3000; pointer-events: none; background: rgba(6, 10, 16, 0.56);
  -webkit-backdrop-filter: blur(3px); backdrop-filter: blur(3px); animation: wpk-in .18s ease-out; touch-action: none; }
@keyframes wpk-in { from { opacity: 0; } to { opacity: 1; } }
.wpk-head { position: absolute; left: 50%; top: max(14px, env(safe-area-inset-top)); transform: translateX(-50%); max-width: 94vw;
  display: flex; align-items: stretch; gap: 8px; }
.wpk-top { display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 999px; white-space: nowrap; min-width: 0;
  background: rgba(255,255,255,.12); color: #fff; font-size: 13px; border: 1px solid rgba(255,255,255,.22); }
.wpk-top b { font-size: 14px; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
.wpk-pr { flex: none; display: flex; align-items: center; gap: 6px; min-height: 46px; padding: 0 18px; border-radius: 999px; white-space: nowrap;
  background: var(--surface, #fff); color: var(--ink, #15171a); font-size: 14.5px; font-weight: 800; border: 1px solid rgba(255,255,255,.4);
  box-shadow: 0 8px 22px rgba(0,0,0,.32); transition: transform .12s ease, box-shadow .12s ease, background .12s ease;
  animation: wpk-pr .3s cubic-bezier(.2, 1.4, .4, 1) both; }
.wpk-pr span { font-size: 18px; }
.wpk-pr.on { background: #f4c65a; color: #15171a; transform: scale(1.1); box-shadow: 0 0 0 3px rgba(244,198,90,.5), 0 12px 28px rgba(0,0,0,.4); }
@keyframes wpk-pr { from { transform: translateY(-10px); opacity: 0; } to { transform: none; opacity: 1; } }
.wpk-top small { opacity: .75; font-weight: 600; }
.wpk-top .i { font-size: 18px; }
.wpk-lines { position: absolute; inset: 0; overflow: visible; }
.wpk-lines path { fill: none; stroke: rgba(150, 205, 255, .38); stroke-width: 2; stroke-dasharray: 5 7; animation: wpk-flow 1.2s linear infinite; }
.wpk-lines path.on { stroke: #f4c65a; stroke-width: 3.5; stroke-dasharray: none; }
@keyframes wpk-flow { to { stroke-dashoffset: -24; } }
.wpk-well { position: absolute; transform: translate(-50%, -50%); border-radius: 50%; animation: wpk-well .34s cubic-bezier(.2, 1.5, .4, 1) both; }
.wpk-well img { position: relative; width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 12px 26px rgba(0,0,0,.5)); -webkit-user-drag: none; }
.wpk-well.on img { filter: drop-shadow(0 0 18px rgba(150, 205, 255, .85)); }
@keyframes wpk-well { from { transform: translate(-50%, -50%) scale(.45); opacity: 0; } to { transform: translate(-50%, -50%) scale(1); opacity: 1; } }
.wpk-rip { position: absolute; inset: -4%; border-radius: 50%; border: 2px solid rgba(150, 205, 255, .6); animation: wpk-rip 1.8s ease-out infinite; }
.wpk-rip.r2 { animation-delay: .9s; }
@keyframes wpk-rip { from { transform: scale(.9); opacity: .9; } to { transform: scale(1.45); opacity: 0; } }
.wpk-c { position: absolute; transform: translate(-50%, -50%); animation: wpk-out .36s cubic-bezier(.2, 1.25, .4, 1) both; animation-delay: calc(var(--i) * 35ms); }
@keyframes wpk-out { from { transform: translate(calc(-50% + var(--dx)), calc(-50% + var(--dy))) scale(.3); opacity: 0; }
  to { transform: translate(-50%, -50%) scale(1); opacity: 1; } }
.wpk-card { width: 100%; height: 100%; display: grid; grid-template-columns: 30px 1fr; align-items: center; column-gap: 8px; padding: 0 10px 0 8px;
  border-radius: 15px; background: var(--surface, #fff); color: var(--ink, #15171a); border: 1px solid rgba(255,255,255,.35);
  box-shadow: 0 10px 26px rgba(0,0,0,.34); transition: transform .12s ease, box-shadow .12s ease; text-align: left; }
.wpk-card .i { font-size: 22px; text-align: center; }
.wpk-card .t { min-width: 0; }
.wpk-card b { display: block; font-size: 13.5px; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wpk-card small { display: block; font-size: 11px; color: var(--muted, #667); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wpk-card small em { font-style: normal; font-weight: 800; color: var(--accent, #b07a00); }
.wpk-card.on { transform: scale(1.1); box-shadow: 0 0 0 3px #f4c65a, 0 14px 30px rgba(0,0,0,.4); }
.wpk-none { position: absolute; left: 50%; transform: translateX(-50%); color: #fff; font-size: 13px; font-weight: 700; opacity: .85; white-space: nowrap; }
.wpk-hint { position: absolute; left: 50%; bottom: max(22px, calc(env(safe-area-inset-bottom) + 14px)); transform: translateX(-50%); max-width: 92vw;
  color: #fff; font-size: 12.5px; font-weight: 600; text-align: center; opacity: .92; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wpk-hint b { color: #f4c65a; }
.wpk-able { -webkit-touch-callout: none; -webkit-user-select: none; user-select: none; touch-action: pan-y; position: relative; overflow: hidden; }
.wpk-able.wpk-press { transform: scale(.985); transition: transform .3s ease; }
.wpk-able.wpk-press::after { content: ""; position: absolute; left: 0; bottom: 0; height: 3px; width: 100%; background: var(--accent, #f4c65a);
  transform-origin: left; animation: wpk-hold .42s linear both; }
@keyframes wpk-hold { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@media (prefers-reduced-motion: reduce) { .wpk, .wpk-well, .wpk-c, .wpk-rip, .wpk-lines path, .wpk-pr { animation: none !important; } }
`;
