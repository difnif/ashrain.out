// 촬영 → 미리보기(+ 드래그로 영역 잡기) → 인식(/api/photo scan). 사진은 서버에 올리지 않는다(인식용 base64 만 보내고 버림).
//   mode     'problem' | 'answer' | 'page'
//   region   true 면 드래그로 인식할 부분을 잘라 보낼 수 있다(선택 사항)
//   onScan(result, { canvas, full, box, thumb })  — 인식 성공 시. result 는 서버 응답 그대로.
//   onPicked(canvas, url)                          — 사진을 고른 직후(페이지 검사처럼 화면이 직접 다루고 싶을 때). 이때는 인식 버튼을 그리지 않는다.
import { useRef, useState } from "react";
import { fileToCanvas, cropCanvas, canvasToBase64, canvasToDataUrl, boxFromPoints, clampBox } from "../../lib/camera";
import { scanCall } from "../../lib/photoApi";
import { thumbOf, Busy, ErrorNote } from "./shared";

const MODE_TEXT = {
  problem: { label: "문제 찍기", hint: "문항 하나가 화면에 꽉 차게, 그림자 없이 찍어 주세요.", busy: "문제를 읽는 중… (10초쯤 걸려요)", bad: "문항을 읽지 못했어요 — 더 가까이, 밝게 다시 찍어 주세요." },
  answer: { label: "답안 찍기", hint: "내가 쓴 풀이만 보이게 찍어 주세요. 문제 문장이 함께 찍혔으면 아래에서 풀이 부분만 잡아 주세요.", busy: "풀이를 읽는 중…", bad: "풀이를 읽지 못했어요 — 손글씨가 보이게 다시 찍어 주세요." },
  page: { label: "페이지 찍기", hint: "문제집 한 페이지가 다 들어오게, 정면에서 찍어 주세요.", busy: "페이지에서 문항과 풀이 자리를 찾는 중…", bad: "페이지를 읽지 못했어요 — 다시 찍어 주세요." },
};

export default function Capture({ mode = "problem", region = false, onScan, onPicked, setToast = () => {}, label, hint, extra }) {
  const T = MODE_TEXT[mode] || MODE_TEXT.problem;
  const camRef = useRef(null), fileRef = useRef(null);
  const [cv, setCv] = useState(null);
  const [url, setUrl] = useState(null);
  const [box, setBox] = useState(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);
  const [drag, setDrag] = useState(false);
  const [cut, setCut] = useState(false);

  const pick = async (file) => {
    if (!file) return;
    if (file.type && !/^image\//.test(file.type)) { setToast("사진 파일만 올릴 수 있어요"); return; }   // 종류를 안 알려 주는 파일 선택기도 있다 → 열어 보고 판단
    setErr(null); setBox(null); setCut(false);
    try {
      const c = await fileToCanvas(file);
      const u = canvasToDataUrl(c, 0.8);
      if (onPicked) { onPicked(c, u); return; }        // 화면이 직접 다룬다 — 여기서는 버튼만 다시 보여 준다
      setCv(c); setUrl(u);
    } catch { setErr("사진을 열 수 없어요 — 다른 사진으로 해 보세요."); }
  };

  const reset = () => { setCv(null); setUrl(null); setBox(null); setErr(null); setCut(false); };

  const scan = async () => {
    if (!cv || busy) return;
    setBusy(true); setErr(null);
    try {
      const src = box ? cropCanvas(cv, box, 0.01) : cv;
      const image = canvasToBase64(src, 0.85);
      const r = await scanCall({ image, mode });   // 1차 실패 시 강한 모델로 한 번 더(수율 폴백)
      if (r?.unreadable) { setErr(T.bad); return; }
      onScan?.(r, { canvas: src, full: cv, box, thumb: thumbOf(src) });
    } catch (e) {
      setErr(e?.message || "인식에 실패했어요 — 잠시 뒤 다시 시도해 주세요.");
    } finally { setBusy(false); }
  };

  return (
    <div className="ph-cap">
      <input ref={camRef} type="file" accept="image/*" capture="environment" hidden onChange={(e) => { pick(e.target.files?.[0]); e.target.value = ""; }} />
      <input ref={fileRef} type="file" accept="image/*" hidden onChange={(e) => { pick(e.target.files?.[0]); e.target.value = ""; }} />
      {!cv && (
        <>
          <button type="button" className={"ph-big" + (drag ? " dragon" : "")} onClick={() => camRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)}
            onDrop={(e) => { e.preventDefault(); setDrag(false); pick(e.dataTransfer?.files?.[0]); }}>
            <span className="ic">📷</span>
            <span>{label || T.label}</span>
            <small>{hint || T.hint}</small>
          </button>
          <div className="ph-alt">
            <button className="sv-btn sm" onClick={() => fileRef.current?.click()}>앨범에서 고르기</button>
            {extra}
          </div>
          {err && <div style={{ marginTop: 10, textAlign: "left" }}><ErrorNote text={err} onShoot={() => { setErr(null); camRef.current?.click(); }} /></div>}
        </>
      )}
      {cv && !onPicked && (
        <>
          {region && !busy && (
            <div className="ph-mode" style={{ justifyContent: "flex-start" }}>
              <button className={"sv-chip" + (cut ? " on" : "")} onClick={() => setCut((v) => !v)}>✂ {cut ? "영역 잡는 중 — 사진 위를 드래그" : "일부만 읽기 (영역 잡기)"}</button>
              {box && <button className="sv-chip" onClick={() => { setBox(null); setCut(false); }}>영역 지우기</button>}
            </div>
          )}
          {region
            ? <RegionPicker url={url} drawing={cut && !busy} editable={!busy} selected={box ? "r" : null}
                boxes={box ? [{ id: "r", kind: mode === "answer" ? "a" : "q", box, label: "인식할 부분" }] : []}
                onDraw={(b) => { setBox(b); setCut(false); }} onMoveBox={(b, nb) => setBox(nb)}
                onMiss={() => setToast("영역이 너무 작아요 — 조금 더 크게 잡아 주세요")} />
            : <div className="ph-stage-wrap"><div className="ph-shot"><div className="ph-stage"><img src={url} alt="" /></div></div></div>}
          {region && !busy && (
            <div className="sv-small" style={{ margin: "8px 0 2px", textAlign: "left", lineHeight: 1.6 }}>
              {box ? "잡은 부분만 읽어요. 모서리를 끌면 크기를, 상자를 끌면 자리를 고칠 수 있어요." : (mode === "answer" ? "문제 문장이 같이 찍혔으면 '일부만 읽기'로 풀이 부분만 잡아 주세요. 안 잡으면 사진 전체를 읽어요." : "사진에 문제가 여럿이면 '일부만 읽기'로 하나만 잡아 주세요. 안 잡으면 사진 전체를 읽어요.")}
            </div>
          )}
          {busy && <div style={{ marginTop: 8 }}><Busy text={T.busy} /></div>}
          {err && !busy && <div style={{ marginTop: 10, textAlign: "left" }}><ErrorNote text={err} onShoot={reset} onRetry={scan} retryLabel="다시 인식하기" /></div>}
          {!busy && !err && (
            <div className="ph-actions" style={{ marginTop: 10 }}>
              <button className="sv-btn pri" onClick={scan}>인식하기</button>
              <button className="sv-btn" onClick={reset}>다시 찍기</button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
const MIN = 0.04;                                  // 상자 최소 크기(비율)
const CORNERS = ["nw", "ne", "sw", "se"];

/**
 * 사진 위에 상자를 그리거나 보여 주는 화면. 상자는 언제나 비율 좌표 {x,y,w,h}(0~1) 로 주고받는다.
 *   url        미리보기 data URL
 *   boxes      [{ id, kind:'q'|'a', box, label }]
 *   drawing    true 면 드래그로 새 상자 → onDraw(box)
 *   editable   true 면 고른 상자를 끌어 옮기고 모서리로 크기를 바꾼다 → onMoveBox(box, 새상자)
 *   onTapBox(b) · selected(id) · renderMenu(b) — 고른 상자 번호 배지를 탭하면 그 옆에 뜨는 팝오버
 */
export function RegionPicker({ url, boxes = [], drawing = false, onDraw, onMiss, onTapBox, onMoveBox, selected = null, editable = false, renderMenu }) {
  const ref = useRef(null);
  const [live, setLive] = useState(null);      // 그리는 중인 상자
  const [tall, setTall] = useState(false);     // 사진 크게 보기(긴 문제가 잘리지 않게)
  const start = useRef(null);
  const grab = useRef(null);                   // { b, mode:'move'|'resize', corner, px, py, base, moved }

  const pos = (e) => { const r = ref.current.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top, w: r.width, h: r.height }; };
  const selBox = boxes.find((b) => b.id === selected) || null;

  // ── 새 상자 그리기 ──
  const down = (e) => {
    if (!drawing || !ref.current) return;
    if (e.pointerType === "mouse" && e.button !== 0) return;
    e.preventDefault();
    try { ref.current.setPointerCapture(e.pointerId); } catch { /* 지원 안 하면 무시 */ }
    const p = pos(e); start.current = p; setLive({ x: p.x / p.w, y: p.y / p.h, w: 0, h: 0 });
  };
  const move = (e) => {
    if (grab.current) { dragMove(e); return; }
    if (!drawing || !start.current) return;
    const p = pos(e); const s = start.current;
    const b = boxFromPoints(s, p, p.w, p.h);
    setLive(b || { x: Math.min(s.x, p.x) / p.w, y: Math.min(s.y, p.y) / p.h, w: Math.abs(p.x - s.x) / p.w, h: Math.abs(p.y - s.y) / p.h });
  };
  const up = (e) => {
    if (grab.current) { dragEnd(e); return; }
    if (!drawing || !start.current) return;
    const p = pos(e); const b = boxFromPoints(start.current, p, p.w, p.h);
    start.current = null; setLive(null);
    if (b) onDraw?.(b); else onMiss?.();
  };

  // ── 상자 옮기기 · 모서리 끌기 ──
  const dragStart = (e, b, corner) => {
    if (!editable || drawing) return;
    if (e.pointerType === "mouse" && e.button !== 0) return;
    e.preventDefault(); e.stopPropagation();
    try { ref.current?.setPointerCapture(e.pointerId); } catch { /* 지원 안 하면 무시 */ }
    const p = pos(e);
    grab.current = { b, mode: corner ? "resize" : "move", corner, px: p.x, py: p.y, base: { ...b.box }, moved: false, pid: e.pointerId };
  };
  const dragMove = (e) => {
    const g = grab.current; if (!g) return;
    const p = pos(e);
    const dx = (p.x - g.px) / p.w, dy = (p.y - g.py) / p.h;
    if (Math.abs(p.x - g.px) > 3 || Math.abs(p.y - g.py) > 3) g.moved = true;
    const o = g.base;
    let nb;
    if (g.mode === "move") nb = { x: clamp(o.x + dx, 0, 1 - o.w), y: clamp(o.y + dy, 0, 1 - o.h), w: o.w, h: o.h };
    else {
      let { x, y, w, h } = o;
      if (g.corner.includes("w")) { x = clamp(o.x + dx, 0, o.x + o.w - MIN); w = o.x + o.w - x; }
      if (g.corner.includes("e")) { w = clamp(o.w + dx, MIN, 1 - o.x); }
      if (g.corner.includes("n")) { y = clamp(o.y + dy, 0, o.y + o.h - MIN); h = o.y + o.h - y; }
      if (g.corner.includes("s")) { h = clamp(o.h + dy, MIN, 1 - o.y); }
      nb = { x, y, w, h };
    }
    onMoveBox?.(g.b, clampBox(nb) || g.base);
  };
  const dragEnd = () => {
    const g = grab.current; grab.current = null;
    if (!g) return;
    try { ref.current?.releasePointerCapture?.(g.pid); } catch { /* */ }
    if (!g.moved && g.mode === "move") onTapBox?.(g.b);      // 끌지 않았으면 그냥 탭
  };

  // ── 키보드 — 고른 상자를 화살표로 옮기고 Shift+화살표로 크기 조절 ──
  const onKey = (e) => {
    if (!editable || !selBox || drawing) return;
    const D = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[e.key];
    if (!D) return;
    e.preventDefault();
    const st = e.altKey ? 0.004 : 0.02;
    const o = selBox.box;
    const nb = e.shiftKey
      ? { x: o.x, y: o.y, w: clamp(o.w + D[0] * st, MIN, 1 - o.x), h: clamp(o.h + D[1] * st, MIN, 1 - o.y) }
      : { x: clamp(o.x + D[0] * st, 0, 1 - o.w), y: clamp(o.y + D[1] * st, 0, 1 - o.h), w: o.w, h: o.h };
    onMoveBox?.(selBox, clampBox(nb) || o);
  };

  const pct = (b) => ({ left: `${b.x * 100}%`, top: `${b.y * 100}%`, width: `${b.w * 100}%`, height: `${b.h * 100}%` });
  const menuUp = selBox ? selBox.box.y + selBox.box.h > 0.62 : false;

  return (
    <div className="ph-stage-wrap">
      <div className={"ph-shot" + (tall ? " tall" : "")}>
        <div ref={ref} className={"ph-stage" + (drawing ? " draw" : "")} tabIndex={editable ? 0 : undefined}
          aria-label={editable ? "영역 상자 — 화살표로 옮기고 Shift+화살표로 크기를 바꿔요" : undefined}
          onKeyDown={editable ? onKey : undefined}
          onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerCancel={() => { start.current = null; grab.current = null; setLive(null); }}>
          <img src={url} alt="" draggable={false} />
          {!drawing && <button type="button" className="ph-zoom" onClick={(e) => { e.stopPropagation(); setTall((v) => !v); }}>{tall ? "⤡ 사진 줄이기" : "⤢ 사진 크게"}</button>}
          {boxes.map((b) => {
            const on = selected === b.id;
            return (
              <div key={b.id} data-box={b.id} className={"ph-box " + (b.kind || "q") + (on ? " sel" : "") + (editable && on && !drawing ? " movable" : "")}
                style={{ ...pct(b.box), pointerEvents: drawing ? "none" : "auto", cursor: editable && on ? "move" : onTapBox ? "pointer" : "default" }}
                onPointerDown={editable && on ? (e) => dragStart(e, b, null) : undefined}
                onClick={(e) => { e.stopPropagation(); if (!editable || !on) onTapBox?.(b); }}>
                {b.label && (
                  renderMenu
                    ? <button type="button" className={"tag btn" + (b.box.y < 0.06 ? " in" : "")} aria-label={`${b.label} 고치기`}
                        onPointerDown={(e) => e.stopPropagation()} onClick={(e) => { e.stopPropagation(); onTapBox?.(b); }}>{b.label}</button>
                    : <span className={"tag" + (b.box.y < 0.06 ? " in" : "")}>{b.label}</span>
                )}
                {editable && on && !drawing && CORNERS.map((c) => (
                  <span key={c} className={"hdl " + c} data-hdl={c} role="button" aria-label={`모서리 ${c}`}
                    onPointerDown={(e) => dragStart(e, b, c)} onClick={(e) => e.stopPropagation()} />
                ))}
              </div>
            );
          })}
          {live && live.w > 0 && live.h > 0 && <div className="ph-box live" style={pct(live)} />}
        </div>
        {renderMenu && selBox && !drawing && (
          <div className={"ph-pop" + (menuUp ? " up" : "")} style={{ left: `${clamp(selBox.box.x + selBox.box.w / 2, 0.22, 0.78) * 100}%`, top: `${(menuUp ? selBox.box.y : selBox.box.y + selBox.box.h) * 100}%` }}>
            {renderMenu(selBox)}
          </div>
        )}
      </div>
      {editable && selBox && !drawing && <div className="ph-hint-kb">상자를 끌면 자리가, 모서리를 끌면 크기가 바뀌어요. 키보드로는 화살표(이동) · Shift+화살표(크기).</div>}
    </div>
  );
}
