// ashrain.out — 손글씨 입력판 (손가락 · 펜 · 마우스) — 컨셉 문제 「종이처럼 풀기」의 답 시트
// 펜이 한 번이라도 닿으면 그다음부터 손가락(손바닥) 터치는 무시한다(S펜 · 애플 펜슬로 쓸 때 손을 대도 괜찮게).
// 펜 압력은 굵기로. 판 모양: int(한 칸 + 단위) · frac(가운데 가로선 — 위 분자, 아래 분모) · pair(가운데 세로선 — 두 수).
// 획 좌표는 판의 논리 px(정수)로 저장하고, 판 크기가 바뀌면(화면 회전 등) 처음 쓴 판 크기에 맞춰 늘이거나 줄여 그린다.
import { useCallback, useEffect, useRef, useState } from "react";
import { drawInk, PAD_H, INK_COLOR } from "./ink";

const MAX_W = 560;

export default function InkPad({ lay = "int", value, onChange, unit = "", labels = [] }) {
  const wrapRef = useRef(null), cvRef = useRef(null);
  const [size, setSize] = useState({ w: 320, h: PAD_H[lay] || 150 });
  const S = useRef({ cur: null, penSeen: false, ink: value || null });
  S.current.ink = value || null;

  // 판 크기 — 감싼 상자 너비에 맞춘다
  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return undefined;
    const fit = () => setSize({ w: Math.max(220, Math.min(MAX_W, Math.floor(el.clientWidth))), h: PAD_H[lay] || 150 });
    fit();
    const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(fit) : null;
    ro?.observe(el);
    return () => ro?.disconnect();
  }, [lay]);

  /** 화면 좌표 → 잉크 좌표(처음 쓴 판 크기 기준) */
  const toInk = (px, py) => {
    const ink = S.current.ink;
    const k = ink && ink.w ? ink.w / size.w : 1;
    return [Math.round(px * k), Math.round(py * k)];
  };

  const redraw = useCallback(() => {
    const cv = cvRef.current;
    if (!cv) return;
    const dpr = Math.min(3, window.devicePixelRatio || 1);
    const W = size.w, H = size.h;
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
    const ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    // 안내선
    ctx.save();
    ctx.strokeStyle = "rgba(60,70,90,.28)"; ctx.fillStyle = "rgba(60,70,90,.38)"; ctx.lineWidth = 1.4; ctx.setLineDash([6, 6]);
    ctx.font = "600 13px Pretendard, 'Noto Sans KR', sans-serif"; ctx.textBaseline = "top";
    if (lay === "frac") {
      ctx.beginPath(); ctx.moveTo(18, H / 2); ctx.lineTo(W - 18, H / 2); ctx.stroke();
      ctx.fillText("분자", 12, 10); ctx.fillText("분모", 12, H / 2 + 10);
    } else if (lay === "pair") {
      ctx.beginPath(); ctx.moveTo(W / 2, 14); ctx.lineTo(W / 2, H - 14); ctx.stroke();
      ctx.fillText(labels[0] || "", 12, 10); ctx.fillText(labels[1] || "", W / 2 + 12, 10);
      ctx.setLineDash([]); ctx.beginPath(); ctx.moveTo(18, H * 0.78); ctx.lineTo(W / 2 - 14, H * 0.78); ctx.moveTo(W / 2 + 14, H * 0.78); ctx.lineTo(W - 18, H * 0.78); ctx.stroke();
    } else {
      ctx.setLineDash([]); ctx.beginPath(); ctx.moveTo(18, H * 0.78); ctx.lineTo(W - (unit ? 70 : 18), H * 0.78); ctx.stroke();
      if (unit) { ctx.font = "700 20px Pretendard, 'Noto Sans KR', sans-serif"; ctx.textBaseline = "alphabetic"; ctx.fillText(unit, W - 60, H * 0.78 - 4); }
    }
    ctx.restore();
    const ink = S.current.ink;
    if (ink) { const k = size.w / (ink.w || size.w); drawInk(ctx, ink, { sx: k, color: INK_COLOR, k, bar: false }); }
  }, [size, lay, unit, labels]);

  useEffect(() => { redraw(); }, [redraw, value]);

  const pos = (e) => { const r = cvRef.current.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  const widthOf = (e) => (e.pointerType === "pen" ? 1.8 + 3.4 * (e.pressure || 0.5) : 3.4);

  const down = (e) => {
    if (e.pointerType === "pen") S.current.penSeen = true;
    else if (e.pointerType === "touch" && S.current.penSeen) return;     // 손바닥
    if (S.current.cur) return;
    e.preventDefault();
    try { cvRef.current.setPointerCapture(e.pointerId); } catch { /* 무시 */ }
    const [x, y] = pos(e);
    const [ix, iy] = toInk(x, y);
    S.current.cur = { id: e.pointerId, pts: [ix, iy], scr: [[x, y]], w: widthOf(e) };
    const ctx = cvRef.current.getContext("2d");
    ctx.save(); ctx.fillStyle = INK_COLOR; ctx.beginPath(); ctx.arc(x, y, S.current.cur.w / 2, 0, Math.PI * 2); ctx.fill(); ctx.restore();
  };
  const move = (e) => {
    const cur = S.current.cur;
    if (!cur || cur.id !== e.pointerId) return;
    e.preventDefault();
    const evs = typeof e.getCoalescedEvents === "function" ? e.getCoalescedEvents() : [e];
    const ctx = cvRef.current.getContext("2d");
    ctx.save(); ctx.strokeStyle = INK_COLOR; ctx.lineCap = "round"; ctx.lineJoin = "round";
    for (const ev of evs.length ? evs : [e]) {
      const [x, y] = pos(ev);
      const last = cur.scr[cur.scr.length - 1];
      if (Math.hypot(x - last[0], y - last[1]) < 1.6) continue;
      const k = size.w / ((S.current.ink && S.current.ink.w) || size.w);
      ctx.lineWidth = cur.w * k;
      ctx.beginPath(); ctx.moveTo(last[0], last[1]); ctx.lineTo(x, y); ctx.stroke();
      cur.scr.push([x, y]);
      const [ix, iy] = toInk(x, y);
      cur.pts.push(ix, iy);
    }
    ctx.restore();
  };
  const up = (e) => {
    const cur = S.current.cur;
    if (!cur || cur.id !== e.pointerId) return;
    S.current.cur = null;
    const base = S.current.ink || { k: "ink", lay, w: size.w, h: size.h, s: [], wd: [] };
    const next = { ...base, k: "ink", lay, s: [...base.s, cur.pts], wd: [...(base.wd || []), Math.round(cur.w * 10) / 10] };
    onChange(next);
  };

  return (
    <div ref={wrapRef} className="cs-padwrap">
      <canvas ref={cvRef} className="cs-pad" style={{ width: size.w, height: size.h }}
        onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerCancel={up} onLostPointerCapture={up}
        aria-label="손글씨로 답 쓰기" role="img" />
    </div>
  );
}
