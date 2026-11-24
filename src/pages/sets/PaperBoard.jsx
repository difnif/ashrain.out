// ashrain.out — 「문제지 그대로」 강사 모드 레이어(관리자) — PaperSolve 위에 얹는다
// 학생 모드와 같은 화면(폭 맞춤 × 확대, 쪽을 이어 붙여 스크롤)에 그대로 쓴다. 학생 | 강사 토글로 오간다.
//   · 강사 모드: 필기 도구 창이 옆(학생 손 반대쪽)에서 들어오고, 풀기 막대는 아래로 빠진다. 학생 모드로 바꾸면 거꾸로.
//   · 펜(S펜 · 마우스) = 선생님(빨강 · 검정 · 초록, S펜 옆 단추 = 지우개), 한 손가락 터치 = 학생(파랑 · 검정 · 보라,
//     손바닥 거르기 palm.js), 두 손가락 = 확대 · 이동(boardview.js Gestures). 손가락 「넘기기」면 한 손가락도 이동.
//   · 학생 손 쪽 끝의 좁은 띠 = 손 받침(쪽 밖) — 손바닥을 걸치면 잠긴 단이 풀린다(palm.js 규칙 그대로).
//   · 필기는 쪽마다 이 기기에 저장(ash.cs.board.<범주>.<NN> — 예전 판서 모드와 같은 꼴)되고, 학생 모드에서도 보인다.
//   · 되돌리기는 사람마다(쪽 상관없이 그 사람의 마지막 일), 쪽 지우기는 화면 가운데 쪽을 길게 눌러서.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { pad2 } from "../../lib/conceptsets";
import { PAGE_W_PX } from "./paper";
import { PalmGuard, PALM_DEFAULT, toPage, toStage, hitStrokes } from "./palm";
import { Gestures, pageAt, undoLast, stepZoom, zoomLabel, clampZoom } from "./boardview";

export const PANEL_W = 84;     // 도구 창
export const STRIP_W = 44;     // 손 받침 띠
/** 강사 모드에서 문제지 양옆 비울 자리 — 도구 창은 학생 손 반대쪽, 손 받침 띠는 손 쪽 */
export const boardPads = (hand) => (hand === "L" ? { l: STRIP_W, r: PANEL_W } : { l: PANEL_W, r: STRIP_W });

const COLORS = {
  pen: [["#d42a3c", "빨강"], ["#1f2937", "검정"], ["#0f8a4c", "초록"]],
  touch: [["#1d5fd6", "파랑"], ["#1f2937", "검정"], ["#7c3aed", "보라"]],
};
const WIDTH = { pen: 2.2, touch: 3.0 };       // 쪽 단위(210 mm = 793.7)
const ERASE_R = 11;
const WHO = { pen: "선생님", touch: "학생" };
const CK = "ash.cs.board.cfg";
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch { /* 가득 참 · 사생활 모드 */ } };
const dataKey = (cat, no) => `ash.cs.board.${cat}.${pad2(no)}`;
function loadInk(cat, no) {
  try { const o = JSON.parse(lsGet(dataKey(cat, no), "null")); if (o && o.pages && typeof o.pages === "object") return o.pages; } catch { /* 망가진 값 */ }
  return {};
}
export function loadBoardCfg() {
  try {
    const o = JSON.parse(lsGet(CK, "null")) || {};
    return { hand: o.hand === "L" ? "L" : "R", palmSize: Number.isFinite(o.palmSize) ? o.palmSize : PALM_DEFAULT.palmSize, diag: !!o.diag,
      fingers: o.fingers === "pan" ? "pan" : "draw" };
  } catch { return { hand: "R", palmSize: PALM_DEFAULT.palmSize, diag: false, fingers: "draw" }; }
}
const headerBottom = () => {
  const fb = document.querySelector(".fb");
  return fb ? Math.max(0, Math.round(fb.getBoundingClientRect().bottom)) : 0;
};

const PB_CSS = `
.pb-cv { position: fixed; left: 0; top: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 50; }
.pb-touch { position: fixed; bottom: 0; z-index: 55; touch-action: none; user-select: none; -webkit-user-select: none; -webkit-touch-callout: none; }
.pb-strip { position: absolute; top: 0; bottom: 0; pointer-events: none; background: repeating-linear-gradient(135deg, rgba(100,116,139,.10) 0 6px, rgba(100,116,139,.04) 6px 12px);
  display: flex; align-items: center; justify-content: center; }
.pb-strip span { writing-mode: vertical-rl; font: 800 11.5px/1 'Pretendard Variable', Pretendard, system-ui, sans-serif; color: #64748b; letter-spacing: .12em; }
.pb-zone { position: absolute; pointer-events: none; transition: opacity .25s; }
.pb-zone.hint { background: rgba(255, 221, 77, .26); box-shadow: inset 0 0 0 2px rgba(230, 170, 0, .5); border-radius: 6px; }
.pb-zone.hint b { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 80%; text-align: center; font: 800 15px/1.5 'Pretendard Variable', Pretendard, system-ui, sans-serif;
  color: #7a5200; word-break: keep-all; background: rgba(255,255,255,.75); border-radius: 10px; padding: 8px 6px; }
.pb-zone.lock { background: rgba(80, 90, 110, .07); }
.pb-panel { position: fixed; bottom: 0; z-index: 66; width: ${PANEL_W}px; box-sizing: border-box; padding: 8px 5px calc(8px + env(safe-area-inset-bottom, 0px));
  background: rgba(241, 243, 246, .97); display: flex; flex-direction: column; gap: 6px; align-items: stretch; overflow-y: auto; scrollbar-width: none;
  touch-action: pan-y; transition: transform .3s cubic-bezier(.2,.8,.2,1), visibility .3s; font-family: 'Pretendard Variable', Pretendard, 'Noto Sans KR', system-ui, sans-serif; }
.pb-panel::-webkit-scrollbar { display: none; }
.pb-panel > * { flex-shrink: 0; }
.pb-panel.L { left: 0; border-right: 1px solid #cfd5dd; box-shadow: 4px 0 18px rgba(0,0,0,.10); transform: translateX(-105%); }
.pb-panel.R { right: 0; border-left: 1px solid #cfd5dd; box-shadow: -4px 0 18px rgba(0,0,0,.10); transform: translateX(105%); }
.pb-panel:not(.in) { visibility: hidden; }
.pb-panel.in { transform: none; visibility: visible; }
.pb-grp { background: #fff; border: 1px solid #d3d9e0; border-radius: 13px; padding: 6px 4px; display: flex; flex-direction: column; gap: 5px; align-items: center; }
.pb-grp .lb { font-size: 10.5px; font-weight: 800; color: #5b6573; text-align: center; line-height: 1.25; }
.pb-b { width: 64px; min-height: 34px; border-radius: 10px; border: 1px solid #c8ced6; background: #fff; color: #1f2937; font: inherit;
  font-size: 12px; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 3px; padding: 2px; cursor: pointer;
  -webkit-tap-highlight-color: transparent; position: relative; overflow: hidden; word-break: keep-all; line-height: 1.2; }
.pb-b:active { transform: scale(.96); }
.pb-b.on { border-color: #0d9488; box-shadow: inset 0 0 0 2px #0d9488; color: #0b6e65; }
.pb-b:disabled { opacity: .35; }
.pb-b .hold { position: absolute; left: 0; bottom: 0; height: 3px; background: #d42a3c; width: 0; }
.pb-b.holding .hold { width: 100%; transition: width .6s linear; }
.pb-dots { display: flex; gap: 4px; justify-content: center; flex-wrap: wrap; }
.pb-dot { width: 20px; height: 20px; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 0 0 1px #c8ced6; cursor: pointer; padding: 0; }
.pb-dot.on { box-shadow: 0 0 0 2.5px #0d9488; }
.pb-pg { font-size: 12px; font-weight: 800; color: #1f2937; text-align: center; font-variant-numeric: tabular-nums; }
.pb-row { display: flex; gap: 3px; }
.pb-row .pb-b { width: 31px; min-height: 34px; font-size: 15px; }
.pb-row .pb-b.ic { font-size: 16px; }
.pb-set { position: fixed; z-index: 67; width: 270px; background: #fff; border: 1px solid #c8ced6; border-radius: 14px; padding: 12px 13px;
  box-shadow: 0 10px 30px rgba(0,0,0,.18); font: 13px/1.4 'Pretendard Variable', Pretendard, system-ui, sans-serif; color: #1f2937; touch-action: manipulation; }
.pb-set h4 { margin: 0 0 8px; font-size: 14px; }
.pb-set .row { margin: 10px 0 4px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.pb-set .seg { display: flex; gap: 6px; }
.pb-set .seg button { flex: 1; padding: 8px 6px; border-radius: 9px; border: 1px solid #c8ced6; background: #fff; font: inherit; font-weight: 700; }
.pb-set .seg button.on { border-color: #0d9488; color: #0b6e65; box-shadow: inset 0 0 0 1.5px #0d9488; }
.pb-set input[type=range] { width: 100%; }
.pb-set p { margin: 6px 0 0; font-size: 11.5px; color: #6b7480; line-height: 1.55; }
.pb-diag { position: fixed; bottom: 8px; z-index: 56; font: 600 11.5px/1.5 ui-monospace, Menlo, monospace; color: #1f2937; background: rgba(255,255,255,.92);
  border: 1px solid #c8ced6; border-radius: 10px; padding: 6px 9px; pointer-events: none; max-width: 46%; white-space: pre-wrap; }
.pb-toast { position: fixed; left: 50%; top: 70px; transform: translateX(-50%); z-index: 68; background: rgba(31,41,55,.9); color: #fff; font: 700 13px/1.3 'Pretendard Variable', Pretendard, system-ui, sans-serif;
  border-radius: 999px; padding: 7px 14px; pointer-events: none; }
.pb-mode { display: flex; border: 1px solid #c8ced6; border-radius: 12px; overflow: hidden; background: #fff; }
.pb-mode button { flex: 1; border: 0; background: transparent; font: inherit; font-size: 12.5px; font-weight: 800; color: #5b6573; padding: 8px 9px; cursor: pointer;
  white-space: nowrap; -webkit-tap-highlight-color: transparent; }
.pb-mode button.on { background: #0d9488; color: #fff; }
.pb-mode.v { flex-direction: column; border-radius: 12px; }
.pb-mode.v button { padding: 7px 2px; }
`;

/** 학생 | 강사 토글 */
export function ModeSwitch({ mode, onChange, vertical = false }) {
  return (
    <div className={"pb-mode" + (vertical ? " v" : "")} role="radiogroup" aria-label="학생 · 강사 모드">
      <button type="button" role="radio" aria-checked={mode === "student"} className={mode === "student" ? "on" : ""} onClick={() => onChange("student")}>🎓 학생</button>
      <button type="button" role="radio" aria-checked={mode === "teacher"} className={mode === "teacher" ? "on" : ""} onClick={() => onChange("teacher")}>✍ 강사</button>
    </div>
  );
}

/** 길게 눌러야 하는 단추 */
function HoldBtn({ onHold, children, title, ms = 600 }) {
  const [h, setH] = useState(false);
  const tm = useRef(0);
  const start = () => { setH(true); clearTimeout(tm.current); tm.current = setTimeout(() => { setH(false); onHold(); }, ms); };
  const stop = () => { setH(false); clearTimeout(tm.current); };
  useEffect(() => () => clearTimeout(tm.current), []);
  return (
    <button type="button" className={"pb-b" + (h ? " holding" : "")} title={title} aria-label={title}
      onPointerDown={start} onPointerUp={stop} onPointerLeave={stop} onPointerCancel={stop} onContextMenu={(e) => e.preventDefault()}>
      {children}<i className="hold" />
    </button>
  );
}

/**
 * on: 강사 모드 · ready: 문제지가 펼쳐졌나 · paperRef / hostRef / boxRef: PaperSolve 의 문제지 · 문서 상자 · 가로 스크롤 상자
 * zm: 지금 확대 배율 · onZoom(zm, anchor?): 확대 확정(기준점 유지) · onMode(m): 모드 바꾸기 · onCfg(cfg): 손잡이가 바뀌면(양옆 자리)
 */
export default function PaperBoard({ on, ready, admin, catId, set, paperRef, hostRef, boxRef, zm, onZoom, onMode, onCfg }) {
  const cvRef = useRef(null);
  const [cfg, setCfg] = useState(loadBoardCfg);
  const [phase, setPhase] = useState({ phase: "hint", col: cfg.hand });
  const [color, setColor] = useState({ pen: COLORS.pen[0][0], touch: COLORS.touch[0][0] });
  const [tool, setTool] = useState({ pen: "draw", touch: "draw" });
  const [showSet, setShowSet] = useState(false);
  const [reg, setReg] = useState(null);          // 쓰는 자리(화면 px) — 도구 창 · 손 받침 띠를 뺀 곳
  const [cur, setCur] = useState(0);             // 화면 가운데 쪽
  const [nP, setNP] = useState(0);
  const [diag, setDiag] = useState("");
  const [toast, setToast] = useState("");
  const [, bump] = useState(0);
  const guard = useMemo(() => new PalmGuard({ hand: cfg.hand, palmSize: cfg.palmSize }), []);   // eslint-disable-line react-hooks/exhaustive-deps
  const gest = useMemo(() => new Gestures(), []);
  const ink = useRef(null);
  if (!ink.current) ink.current = { pages: loadInk(catId, set.no), hist: [], live: new Map(), btn: new Map() };
  const R = useRef({});
  R.current = { on, reg, color, tool, cfg, zm, cur };
  const pv = useRef(null);                       // 두 손가락 미리 보기 { zm0, r0, s, tx, ty, ox, oy }

  const toastT = useRef(0);
  const say = useCallback((m) => { setToast(m); clearTimeout(toastT.current); toastT.current = setTimeout(() => setToast(""), 1600); }, []);
  useEffect(() => () => clearTimeout(toastT.current), []);

  useEffect(() => { lsSet(CK, JSON.stringify(cfg)); guard.setCfg({ palmSize: cfg.palmSize, hand: cfg.hand }); onCfg?.(cfg); }, [cfg, guard, onCfg]);

  // 저장(쪽마다)
  const saveT = useRef(0);
  const flush = useCallback(() => {
    const pages = Object.fromEntries(Object.entries(ink.current.pages).filter(([, v]) => v && v.length));
    lsSet(dataKey(catId, set.no), JSON.stringify({ v: 1, pages }));
  }, [catId, set.no]);
  const save = useCallback(() => { clearTimeout(saveT.current); saveT.current = setTimeout(flush, 400); }, [flush]);
  useEffect(() => () => { clearTimeout(saveT.current); flush(); }, [flush]);

  /* ── 쪽 ── */
  const pages = useCallback(() => {
    const root = paperRef.current?.root;
    return root ? [...root.querySelectorAll(".pg")] : [];
  }, [paperRef]);
  const rectOf = (el) => { const r = el.getBoundingClientRect(); return { l: r.left, t: r.top, r: r.right, b: r.bottom }; };
  useEffect(() => { if (ready) setNP(pages().length); }, [ready, pages]);

  /* ── 그리기(화면 전체 캔버스 — 학생 모드에서도 보인다) ── */
  const strokesOf = (i) => (ink.current.pages[i] = ink.current.pages[i] || []);
  const ctxOf = () => {
    const cv = cvRef.current;
    if (!cv) return null;
    const dpr = Math.min(3, window.devicePixelRatio || 1), W = window.innerWidth, H = window.innerHeight;
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) {
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); cv.style.width = `${W}px`; cv.style.height = `${H}px`;
    }
    const ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    return ctx;
  };
  const pathStroke = (ctx, s, pg) => {
    const P = s.p, k = (pg.r - pg.l) / PAGE_W_PX;
    if (!P.length) return;
    ctx.strokeStyle = s.c; ctx.fillStyle = s.c; ctx.lineWidth = Math.max(1, s.w * k);
    const pt = (j) => toStage(pg, PAGE_W_PX, P[j], P[j + 1]);
    if (P.length <= 2) { const [x, y] = pt(0); ctx.beginPath(); ctx.arc(x, y, ctx.lineWidth / 2, 0, Math.PI * 2); ctx.fill(); return; }
    ctx.beginPath();
    const [x0, y0] = pt(0);
    ctx.moveTo(x0, y0);
    for (let j = 2; j < P.length - 2; j += 2) {
      const [x1, y1] = pt(j), [x2, y2] = pt(j + 2);
      ctx.quadraticCurveTo(x1, y1, (x1 + x2) / 2, (y1 + y2) / 2);
    }
    const [xl, yl] = pt(P.length - 2);
    ctx.lineTo(xl, yl);
    ctx.stroke();
  };
  const redraw = useCallback(() => {
    const ctx = ctxOf();
    if (!ctx) return;
    const W = window.innerWidth, H = window.innerHeight;
    ctx.clearRect(0, 0, W, H);
    const els = pages();
    els.forEach((el, i) => {
      const list = ink.current.pages[i];
      const hasLive = [...ink.current.live.values()].some((L) => L.pi === i && L.tool === "draw");
      if (!(list && list.length) && !hasLive) return;
      const pg = rectOf(el);
      if (pg.b < 0 || pg.t > H) return;
      if (list) for (const s of list) pathStroke(ctx, s, pg);
      for (const L of ink.current.live.values()) if (L.pi === i && L.tool === "draw") pathStroke(ctx, L, pg);
    });
  }, [pages]);
  const raf = useRef(0);
  const req = useCallback(() => {
    if (raf.current) return;
    raf.current = requestAnimationFrame(() => {
      raf.current = 0;
      redraw();
      const r = R.current.reg, els = pages();
      if (els.length) {
        const cy = r ? (r.t + r.b) / 2 : window.innerHeight / 2;
        const i = pageAt(els.map(rectOf), cy);
        if (i >= 0 && i !== R.current.cur) setCur(i);
      }
    });
  }, [redraw, pages]);
  useEffect(() => () => cancelAnimationFrame(raf.current), []);
  const drawSeg = (L) => {
    const ctx = ctxOf(), el = pages()[L.pi];
    if (!ctx || !el) return;
    const pg = rectOf(el), P = L.p, n = P.length;
    const k = (pg.r - pg.l) / PAGE_W_PX;
    ctx.strokeStyle = L.c; ctx.lineWidth = Math.max(1, L.w * k);
    ctx.beginPath();
    const a = toStage(pg, PAGE_W_PX, P[Math.max(0, n - 4)], P[Math.max(1, n - 3)]), b = toStage(pg, PAGE_W_PX, P[n - 2], P[n - 1]);
    ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
  };

  // 스크롤 · 크기 · 확대가 바뀌면 다시 그리기
  useEffect(() => {
    if (!ready) return undefined;
    const box = boxRef.current, host = hostRef.current;
    window.addEventListener("scroll", req, { passive: true });
    window.addEventListener("resize", req);
    box?.addEventListener("scroll", req, { passive: true });
    let ro = null;
    if (host && typeof ResizeObserver !== "undefined") { ro = new ResizeObserver(() => req()); ro.observe(host); }
    document.fonts?.ready?.then(() => req()).catch(() => {});
    req();
    return () => {
      window.removeEventListener("scroll", req); window.removeEventListener("resize", req);
      box?.removeEventListener("scroll", req); ro?.disconnect();
    };
  }, [ready, req, boxRef, hostRef]);

  /* ── 쓰는 자리(손바닥 거르기의 「쪽」) ── */
  const layout = useCallback(() => {
    const pads = boardPads(R.current.cfg.hand);
    const box = { l: pads.l, t: headerBottom(), r: window.innerWidth - pads.r, b: window.innerHeight };
    guard.setPage(box);
    setReg(box);
    req();
  }, [guard, req]);
  useEffect(() => {
    if (!on) return undefined;
    layout();
    window.addEventListener("resize", layout);
    return () => window.removeEventListener("resize", layout);
  }, [on, layout, cfg.hand]);
  useEffect(() => {
    if (on) return;
    // 학생 모드로 — 쓰던 것 · 미리 보기 정리
    ink.current.live.clear(); ink.current.btn.clear(); gest.reset();
    if (pv.current && hostRef.current) { hostRef.current.style.transform = ""; hostRef.current.style.transformOrigin = ""; }
    pv.current = null; setShowSet(false);
    req();
  }, [on, gest, hostRef, req]);

  /* ── 동작(palm.js) → 획 ── */
  const toPg = (L, x, y) => {
    const el = pages()[L.pi];
    return el ? toPage(rectOf(el), PAGE_W_PX, x, y) : [0, 0];
  };
  const eraseAt = (L, x, y) => {
    const els = pages();
    const i = pageAt(els.map(rectOf), y);
    if (i < 0) return;
    const [u, v] = toPage(rectOf(els[i]), PAGE_W_PX, x, y);
    const list = strokesOf(i);
    const hit = hitStrokes(list, u, v, ERASE_R);
    if (!hit.length) return;
    for (let j = hit.length - 1; j >= 0; j--) L.removed.push({ pi: i, s: list.splice(hit[j], 1)[0] });
    req();
  };
  const apply = useCallback((acts) => {
    if (!acts.length) return;
    let dirty = false, phaseChanged = null;
    for (const a of acts) {
      if (a.k === "start") {
        const btn = ink.current.btn.get(a.id) || 0;
        const erase = R.current.tool[a.src] === "erase" || (a.src === "pen" && (btn & 32 || btn & 2));
        const [x0, y0] = a.pts[0] || [0, 0];
        const pi = Math.max(0, pageAt(pages().map(rectOf), y0));
        const L = { src: a.src, tool: erase ? "erase" : "draw", c: R.current.color[a.src], w: WIDTH[a.src], p: [], removed: [], pi };
        ink.current.live.set(a.id, L);
        for (const [x, y] of a.pts) {
          if (L.tool === "erase") eraseAt(L, x, y);
          else { const [u, v] = toPg(L, x, y); L.p.push(u, v); }
        }
        if (L.tool === "draw") { if (L.p.length > 2) dirty = true; else drawSeg(L); }
      } else if (a.k === "add") {
        const L = ink.current.live.get(a.id);
        if (!L) continue;
        for (const [x, y] of a.pts) {
          if (L.tool === "erase") eraseAt(L, x, y);
          else {
            const [u, v] = toPg(L, x, y), n = L.p.length;
            if (n >= 2 && Math.abs(L.p[n - 2] - u) < 0.4 && Math.abs(L.p[n - 1] - v) < 0.4) continue;
            L.p.push(u, v); drawSeg(L);
          }
        }
      } else if (a.k === "end") {
        const L = ink.current.live.get(a.id);
        ink.current.live.delete(a.id); ink.current.btn.delete(a.id);
        if (!L) continue;
        if (L.tool === "draw" && L.p.length) {
          const s = { s: L.src, c: L.c, w: L.w, p: L.p };
          strokesOf(L.pi).push(s);
          ink.current.hist.push({ src: L.src, pi: L.pi, add: s });
        } else if (L.tool === "erase" && L.removed.length) ink.current.hist.push({ src: L.src, del: L.removed });
        dirty = true; save(); bump((n) => n + 1);
      } else if (a.k === "drop") {
        const L = ink.current.live.get(a.id);
        ink.current.live.delete(a.id); ink.current.btn.delete(a.id);
        if (L?.removed?.length) for (const { pi, s } of L.removed) strokesOf(pi).push(s);
        dirty = true;
      } else if (a.k === "phase") phaseChanged = { phase: a.phase, col: a.col };
      else if (a.k === "reject" && R.current.cfg.diag) setDiag((d) => `버림 #${a.id} · ${({ size: "접촉이 넓음(손바닥)", "pen-near": "펜 근처(선생님 손)", "pen-after": "펜이 바로 옆에 닿음", "rest-near": "손 받침 근처", edge: "가장자리 여백", "one-writer": "이미 쓰는 중", "two-touch": "두 점이 함께 닿음", locked: "잠긴 단", below: "필기 아래 · 손 쪽", "palm-near": "손바닥 옆" })[a.why] || a.why}\n${d.split("\n")[0] || ""}`);
    }
    if (dirty) req();
    if (phaseChanged) {
      setPhase(phaseChanged);
      if (phaseChanged.phase === "locked" && phaseChanged.col !== R.current.cfg.hand) setCfg((c) => ({ ...c, hand: phaseChanged.col }));
      if (phaseChanged.phase === "locked") say(`손 받침 확인 — ${phaseChanged.col === "R" ? "오른쪽" : "왼쪽"} 단은 잠시 쉬어요`);
      if (phaseChanged.phase === "free") say("이제 어디든 써요");
    }
  }, [req, save, say, pages]);  // eslint-disable-line react-hooks/exhaustive-deps

  /* ── 두 손가락 · 넘기기 ── */
  const preview = useCallback((v) => {
    const host = hostRef.current;
    if (!host) return;
    if (!pv.current) {
      host.style.transform = "";
      const r = host.getBoundingClientRect();
      pv.current = { zm0: R.current.zm, r0: { left: r.left, top: r.top } };
      host.style.willChange = "transform";
    }
    const P = pv.current;
    const s = Math.min(3 / P.zm0, Math.max(1 / P.zm0, v.s));
    Object.assign(P, { s, tx: v.tx, ty: v.ty, ox: v.ox, oy: v.oy });
    host.style.transformOrigin = `${v.ox - P.r0.left}px ${v.oy - P.r0.top}px`;
    host.style.transform = `translate(${v.tx}px, ${v.ty}px) scale(${s})`;
    req();
  }, [hostRef, req]);
  const commit = useCallback(() => {
    const host = hostRef.current, P = pv.current;
    pv.current = null;
    if (!host || !P) return;
    host.style.transform = ""; host.style.transformOrigin = ""; host.style.willChange = "";
    if (P.s != null) onZoom(clampZoom(P.zm0 * P.s), { x: P.ox, y: P.oy, tx: P.tx, ty: P.ty });
    req();
  }, [hostRef, onZoom, req]);
  const panBy = useCallback((dx, dy) => {
    const box = boxRef.current;
    if (box && dx) box.scrollLeft -= dx;
    if (dy) window.scrollBy(0, -dy);
  }, [boxRef]);

  /* ── 포인터 ── */
  const touchRef = useRef(null);
  const hasReg = !!reg;
  useEffect(() => {
    const st = touchRef.current;
    if (!st || !on || !ready) return undefined;
    const P = (e) => ({ id: e.pointerId, type: e.pointerType || "mouse", x: e.clientX, y: e.clientY,
      w: e.width || 0, h: e.height || 0, t: e.timeStamp || performance.now(), buttons: e.buttons });
    const showDiag = (e, what) => {
      if (!R.current.cfg.diag) return;
      setDiag((d) => `${what} ${e.pointerType} #${e.pointerId} · 크기 ${Math.round(e.width || 0)}×${Math.round(e.height || 0)} · 압력 ${(e.pressure || 0).toFixed(2)}\n${d.split("\n").slice(-1)[0] || ""}`);
    };
    const gestOut = (r) => {
      if (!r) return;
      if (r.k === "pan") panBy(r.dx, r.dy);
      else if (r.k === "view") preview(r);
    };
    const down = (e) => {
      e.preventDefault();
      try { st.setPointerCapture(e.pointerId); } catch { /* 무시 */ }
      ink.current.btn.set(e.pointerId, e.buttons);
      showDiag(e, "닿음");
      const p = P(e);
      if (p.type === "touch") {
        const d = gest.down(p, { fingers: R.current.cfg.fingers });
        for (const id of d.cancel) apply(guard.cancel({ ...p, id }));
        if (d.route !== "guard") return;
      } else gest.pen(p.t);
      apply(guard.down(p));
    };
    const move = (e) => {
      const list = e.getCoalescedEvents ? e.getCoalescedEvents() : null;
      const evs = list && list.length ? list : [e];
      const touch = e.pointerType === "touch";
      if (touch && gest.routeOf(e.pointerId) && gest.routeOf(e.pointerId) !== "guard") {
        const p = P(evs[evs.length - 1]); p.id = e.pointerId;
        gestOut(gest.move(p));
        return;
      }
      const acts = [];
      for (const ce of evs) {
        const p = P(ce); p.id = e.pointerId; p.type = e.pointerType || "mouse";
        if (touch) gest.move(p); else gest.pen(p.t);
        acts.push(...guard.move(p));
      }
      apply(acts);
    };
    const up = (e, cancel = false) => {
      const p = P(e);
      if (p.type === "touch") {
        const r = gest.up(p);
        if (r.route === "gest") { if (r.end) commit(); else if (pv.current) commit(); return; }
        if (r.route === "ignore") return;
      }
      apply(cancel ? guard.cancel(p) : guard.up(p));
    };
    const onUp = (e) => up(e), onCancel = (e) => up(e, true);
    const noMenu = (e) => e.preventDefault();
    const wheel = (e) => {
      e.preventDefault();
      if (e.ctrlKey || e.metaKey) onZoom(clampZoom(R.current.zm * Math.exp(-e.deltaY * 0.0025)), { x: e.clientX, y: e.clientY });
      else panBy(-e.deltaX, -e.deltaY);
    };
    st.addEventListener("pointerdown", down, { passive: false });
    st.addEventListener("pointermove", move);
    st.addEventListener("pointerup", onUp);
    st.addEventListener("pointercancel", onCancel);
    st.addEventListener("contextmenu", noMenu);
    st.addEventListener("wheel", wheel, { passive: false });
    // 손을 가만히 대고 있을 때(움직임 없음)도 시간 규칙이 돌게
    let loop = 0;
    const tick = () => { loop = requestAnimationFrame(tick); if (guard.busy()) apply(guard.tick(performance.now())); };
    loop = requestAnimationFrame(tick);
    return () => {
      st.removeEventListener("pointerdown", down); st.removeEventListener("pointermove", move);
      st.removeEventListener("pointerup", onUp); st.removeEventListener("pointercancel", onCancel);
      st.removeEventListener("contextmenu", noMenu); st.removeEventListener("wheel", wheel);
      cancelAnimationFrame(loop);
    };
  }, [on, ready, hasReg, guard, gest, apply, preview, commit, panBy, onZoom]);

  /* ── 화면 꺼짐 방지 · 제목 (강사 모드) ── */
  useEffect(() => {
    if (!on) return undefined;
    let lock = null;
    const ask = async () => { try { if (document.visibilityState === "visible" && navigator.wakeLock) lock = await navigator.wakeLock.request("screen"); } catch { /* 지원 안 함 */ } };
    ask();
    const onVis = () => { if (document.visibilityState === "visible") ask(); };
    document.addEventListener("visibilitychange", onVis);
    const prev = document.title; document.title = `강사 모드 — ${set.short || set.title}`;
    return () => { document.removeEventListener("visibilitychange", onVis); try { lock?.release?.(); } catch { /* 무시 */ } document.title = prev; };
  }, [on, set]);

  /* ── 도구 ── */
  const goPage = (d) => {
    const els = pages(), i = Math.max(0, Math.min(els.length - 1, cur + d));
    const el = els[i], r = R.current.reg;
    if (!el) return;
    window.scrollBy({ top: el.getBoundingClientRect().top - (r ? r.t : 0) - 6, behavior: "smooth" });
  };
  const undo = (src) => {
    const e = undoLast(ink.current.hist, src);
    if (!e) return;
    if (e.add) { const list = strokesOf(e.pi), k = list.lastIndexOf(e.add); if (k >= 0) list.splice(k, 1); }
    if (e.del) for (const { pi, s } of e.del) strokesOf(pi).push(s);
    req(); save(); bump((x) => x + 1);
  };
  const canUndo = (src) => ink.current.hist.some((e) => e.src === src);
  const clearPage = () => {
    const list = strokesOf(cur);
    if (!list.length) { say(`${cur + 1}쪽엔 지울 필기가 없어요`); return; }
    ink.current.pages[cur] = [];
    ink.current.hist = ink.current.hist.filter((e) => e.pi !== cur).map((e) => (e.del ? { ...e, del: e.del.filter((d) => d.pi !== cur) } : e)).filter((e) => !e.del || e.del.length);
    req(); save(); bump((x) => x + 1);
    say(`${cur + 1}쪽 필기를 지웠어요`);
  };
  const toggleFs = async () => {
    try {
      if (!document.fullscreenElement) {
        await document.documentElement.requestFullscreen?.({ navigationUI: "hide" });
        try { await screen.orientation?.lock?.("landscape"); } catch { /* 고정 불가 */ }
      } else await document.exitFullscreen();
    } catch { /* 불가 */ }
    setTimeout(layout, 300);
  };

  const side = cfg.hand === "R" ? "L" : "R";     // 도구 창 = 학생 손 반대쪽
  const pads = boardPads(cfg.hand);
  const top = reg ? reg.t : 0;
  const half = reg ? (reg.r - reg.l) / 2 : 0;
  const zoneStyle = (col) => reg && ({ left: (col === "R" ? reg.l + half : reg.l) - (side === "L" ? PANEL_W : 0), top: 0, width: half, height: reg.b - reg.t });
  const drawFingers = cfg.fingers === "draw";
  const group = (src) => (
    <div className="pb-grp">
      <span className="lb">{WHO[src]} · {src === "pen" ? "S펜" : "터치"}</span>
      <div className="pb-dots">
        {COLORS[src].map(([c, nm]) => (
          <button key={c} type="button" className={"pb-dot" + (color[src] === c && tool[src] === "draw" ? " on" : "")} style={{ background: c }}
            title={`${WHO[src]} ${nm}`} aria-label={`${WHO[src]} ${nm}`}
            onClick={() => { setColor((o) => ({ ...o, [src]: c })); setTool((o) => ({ ...o, [src]: "draw" })); if (src === "touch" && !drawFingers) setCfg((o) => ({ ...o, fingers: "draw" })); }} />
        ))}
      </div>
      <button type="button" className={"pb-b" + (tool[src] === "erase" ? " on" : "")} title={`${WHO[src]} 지우개`}
        onClick={() => setTool((o) => ({ ...o, [src]: o[src] === "erase" ? "draw" : "erase" }))}>지우개</button>
      <button type="button" className="pb-b" disabled={!canUndo(src)} title={`${WHO[src]} 되돌리기`} onClick={() => undo(src)}>↶ 되돌리기</button>
      {src === "touch" && (
        <button type="button" className={"pb-b" + (!drawFingers ? " on" : "")} title="손가락으로 넘기기(쓰지 않고 이동만)"
          onClick={() => { setCfg((o) => ({ ...o, fingers: o.fingers === "pan" ? "draw" : "pan" })); gest.reset(); }}>
          {drawFingers ? "✋ 넘기기" : "✋ 넘기는 중"}
        </button>
      )}
    </div>
  );

  return (
    <>
      <style>{PB_CSS}</style>
      <canvas ref={cvRef} className="pb-cv" aria-hidden="true" />
      {on && reg && (
        <div ref={touchRef} className="pb-touch" data-testid="pb-touch"
          style={{ top, left: side === "L" ? PANEL_W : 0, right: side === "R" ? PANEL_W : 0 }}>
          <div className="pb-strip" style={cfg.hand === "R" ? { right: 0, width: STRIP_W } : { left: 0, width: STRIP_W }}><span>손 받침</span></div>
          {drawFingers && phase.phase === "hint" && (
            <div className="pb-zone hint" style={zoneStyle(cfg.hand)}><b>✋ 학생 손바닥을<br />여기에 먼저 올려 두세요</b></div>
          )}
          {drawFingers && phase.phase === "locked" && <div className="pb-zone lock" style={zoneStyle(phase.col)} />}
        </div>
      )}
      {admin && (
        <div className={"pb-panel " + side + (on ? " in" : "")} style={{ top: reg ? reg.t : headerBottom() }} aria-hidden={!on}
          onPointerDown={(e) => e.stopPropagation()}>
          <ModeSwitch mode={on ? "teacher" : "student"} onChange={onMode} vertical />
          <div className="pb-grp">
            <div className="pb-row">
              <button type="button" className="pb-b" disabled={cur <= 0} onClick={() => goPage(-1)} title="앞 쪽">‹</button>
              <button type="button" className="pb-b" disabled={cur >= nP - 1} onClick={() => goPage(1)} title="다음 쪽">›</button>
            </div>
            <span className="pb-pg">{nP ? `${cur + 1} / ${nP}쪽` : "…"}</span>
            <div className="pb-row">
              <button type="button" className="pb-b" disabled={zm <= 1.001} onClick={() => onZoom(stepZoom(zm, -1))} title="작게">−</button>
              <button type="button" className="pb-b" disabled={zm >= 2.999} onClick={() => onZoom(stepZoom(zm, 1))} title="크게">＋</button>
            </div>
            <button type="button" className="pb-b" onClick={() => onZoom(1)} title="폭 맞춤">{zoomLabel(zm)}</button>
          </div>
          {group("pen")}
          {group("touch")}
          <div className="pb-grp">
            {phase.phase === "hint"
              ? <button type="button" className="pb-b" onClick={() => apply(guard.skipHint())} title="손 받침 안내 건너뛰기">안내 건너뛰기</button>
              : <button type="button" className="pb-b" onClick={() => apply(guard.rehint())} title="손 받침 다시">손 받침 다시</button>}
            <HoldBtn title="길게 눌러 이 쪽 필기 지우기" onHold={clearPage} ms={800}>{nP ? `${cur + 1}쪽 지우기` : "쪽 지우기"}</HoldBtn>
            <div className="pb-row">
              <button type="button" className="pb-b ic" onClick={toggleFs} title="전체 화면" aria-label="전체 화면">⛶</button>
              <button type="button" className={"pb-b ic" + (showSet ? " on" : "")} onClick={() => setShowSet((v) => !v)} title="설정" aria-label="설정">⚙</button>
            </div>
          </div>
        </div>
      )}
      {on && showSet && (
        <div className="pb-set" style={{ top: top + 8, [side === "L" ? "left" : "right"]: pads[side === "L" ? "l" : "r"] + 8 }} onPointerDown={(e) => e.stopPropagation()}>
          <h4>강사 모드 설정</h4>
          <div className="row">학생 손잡이</div>
          <div className="seg">
            {[["R", "오른손"], ["L", "왼손"]].map(([k, l]) => (
              <button key={k} type="button" className={cfg.hand === k ? "on" : ""}
                onClick={() => { setCfg((c) => ({ ...c, hand: k })); guard.setCfg({ hand: k }); apply(guard.rehint()); }}>{l}</button>
            ))}
          </div>
          <p>손바닥을 안내 칸에 대면 저절로 맞춰져요. 도구 창은 손 반대쪽, 손 받침 띠는 손 쪽으로 옮겨 가요.</p>
          <div className="row">학생 손가락</div>
          <div className="seg">
            {[["draw", "✍ 쓰기"], ["pan", "✋ 넘기기"]].map(([k, l]) => (
              <button key={k} type="button" className={cfg.fingers === k ? "on" : ""} onClick={() => { setCfg((c) => ({ ...c, fingers: k })); gest.reset(); }}>{l}</button>
            ))}
          </div>
          <p>쓰기: 한 손가락은 필기, 두 손가락은 확대 · 이동. 넘기기: 손가락은 쓰지 않고 이동 · 확대만(선생님 혼자 S펜으로 쓸 때).</p>
          <div className="row">손바닥 크기 기준 <b>{cfg.palmSize ? `${cfg.palmSize}px` : "끔"}</b></div>
          <input type="range" min="0" max="120" step="5" value={cfg.palmSize}
            onChange={(e) => setCfg((c) => ({ ...c, palmSize: Number(e.target.value) }))} aria-label="손바닥 크기 기준" />
          <p>닿은 접촉이 이보다 넓으면 손바닥으로 보고 버려요. 진단을 켜고 손가락 · 디스크팁 · 손바닥을 대 보면 크기가 보여요 — 모니터가 크기를 늘 같은 값으로 보내면 0(끔)으로 두세요.</p>
          <div className="row">진단 표시
            <div className="seg" style={{ width: 120 }}>
              <button type="button" className={cfg.diag ? "on" : ""} onClick={() => setCfg((c) => ({ ...c, diag: true }))}>켬</button>
              <button type="button" className={!cfg.diag ? "on" : ""} onClick={() => { setCfg((c) => ({ ...c, diag: false })); setDiag(""); }}>끔</button>
            </div>
          </div>
        </div>
      )}
      {on && cfg.diag && <div className="pb-diag" style={{ [side === "L" ? "left" : "right"]: pads[side === "L" ? "l" : "r"] + 8 }}>{diag || "화면에 닿아 보세요 — 펜 · 손가락 · 손바닥의 종류와 크기가 여기 떠요."}</div>}
      {toast && <div className="pb-toast" role="status">{toast}</div>}
    </>
  );
}
