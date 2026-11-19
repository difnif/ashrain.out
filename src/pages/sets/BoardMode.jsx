// ashrain.out — 컨셉 문제 「판서 모드」(#/sets/<범주>/<NN>/board) — 관리자 전용
// 문제지 한 쪽을 화면 가득 펼쳐 놓고, 선생님(갤럭시탭 S펜)과 학생(유선 미러링한 터치 모니터 — 손가락 · 디스크팁)이
// 그 위에 동시에 풀이를 쓴다. 미러링이라 두 기기의 입력이 이 화면 하나로 함께 들어온다 — 펜과 터치를 따로 받아 따로 그린다.
//   · 선생님 = 펜(pointerType pen · 노트북이면 마우스): 빨강 · 검정 · 초록. S펜 옆 단추를 누른 채 쓰면 지우개.
//   · 학생 = 터치: 파랑 · 검정 · 보라. 손바닥 거르기(palm.js) — 손 받침 안내 → 단 잠금 → 쪽 밖으로 손이 걸치면 해제 → 아래 · 손 쪽 무시,
//     접촉 크기 · 한 번에 하나 · 가장자리 여백 · 지연 확정. 펜 근처의 새 터치는 선생님 손바닥으로 보고 버린다.
//   · 판서는 쪽마다 이 기기에 저장된다(나갔다 와도 그대로). 되돌리기는 사람마다 따로.
//   · 쪽 밖(도구 막대 · 쪽 옆 빈 곳)은 그리지 않는다. 손 쪽 빈 곳은 손 받침 자리. 도구 막대는 손 반대쪽(오른손잡이면 왼쪽).
//   · 나가기 · 이 쪽 지우기는 길게 눌러야 한다(손바닥이 잘못 눌러도 안 나가게).
//   · ⚙ 설정: 학생 손잡이 · 손바닥 크기 기준(모니터가 접촉 크기를 안 알려 주면 0 = 끔) · 진단(닿은 접촉의 종류 · 크기 · 버린 까닭).
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { printUrl, pad2 } from "../../lib/conceptsets";
import { splitDoc } from "./printdoc";
import { Paper, PAGE_W_PX, ensureLinks } from "./paper";
import { ensureSerif, useIsAdmin } from "./common";
import { PalmGuard, PALM_DEFAULT, toPage, toStage, hitStrokes } from "./palm";

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
function loadCfg() {
  try {
    const o = JSON.parse(lsGet(CK, "null")) || {};
    return { hand: o.hand === "L" ? "L" : "R", palmSize: Number.isFinite(o.palmSize) ? o.palmSize : PALM_DEFAULT.palmSize, diag: !!o.diag };
  } catch { return { hand: "R", palmSize: PALM_DEFAULT.palmSize, diag: false }; }
}

const BD_CSS = `
.bd-root { position: fixed; inset: 0; z-index: 60; background: #d9dde3; overflow: hidden; touch-action: none; user-select: none;
  -webkit-user-select: none; -webkit-touch-callout: none; font-family: 'Pretendard Variable', Pretendard, 'Noto Sans KR', system-ui, sans-serif; }
.bd-stage { position: absolute; inset: 0; touch-action: none; }
.bd-host { position: absolute; left: 0; top: 0; pointer-events: none; }
.bd-cv { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.bd-zone { position: absolute; pointer-events: none; transition: opacity .25s; }
.bd-zone.hint { background: rgba(255, 221, 77, .30); box-shadow: inset 0 0 0 2px rgba(230, 170, 0, .55); border-radius: 6px; }
.bd-zone.hint b { position: absolute; left: 50%; top: 58%; transform: translate(-50%, -50%); width: 86%; text-align: center; font-size: 15px;
  font-weight: 800; color: #7a5200; line-height: 1.5; word-break: keep-all; }
.bd-zone.lock { background: rgba(80, 90, 110, .07); }
.bd-bar { position: absolute; top: 8px; bottom: 8px; width: 74px; display: flex; flex-direction: column; gap: 6px; align-items: stretch;
  overflow-y: auto; scrollbar-width: none; z-index: 2; touch-action: manipulation; }
.bd-bar::-webkit-scrollbar { display: none; }
.bd-bar.L { left: 8px; } .bd-bar.R { right: 8px; }
.bd-grp { background: rgba(255,255,255,.92); border: 1px solid #c8ced6; border-radius: 14px; padding: 6px 5px; display: flex; flex-direction: column;
  gap: 5px; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
.bd-grp .lb { font-size: 10.5px; font-weight: 800; color: #5b6573; text-align: center; line-height: 1.25; }
.bd-b { width: 56px; min-height: 40px; border-radius: 11px; border: 1px solid #c8ced6; background: #fff; color: #1f2937; font: inherit;
  font-size: 12px; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 3px; padding: 2px; cursor: pointer;
  -webkit-tap-highlight-color: transparent; position: relative; overflow: hidden; }
.bd-b:active { transform: scale(.96); }
.bd-b.on { border-color: #0d9488; box-shadow: inset 0 0 0 2px #0d9488; color: #0b6e65; }
.bd-b:disabled { opacity: .35; }
.bd-b .hold { position: absolute; left: 0; bottom: 0; height: 3px; background: #d42a3c; width: 0; }
.bd-b.holding .hold { width: 100%; transition: width .6s linear; }
.bd-dots { display: flex; gap: 5px; justify-content: center; flex-wrap: wrap; }
.bd-dot { width: 22px; height: 22px; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 0 0 1px #c8ced6; cursor: pointer; padding: 0; }
.bd-dot.on { box-shadow: 0 0 0 2.5px #0d9488; }
.bd-pg { font-size: 12px; font-weight: 800; color: #1f2937; text-align: center; font-variant-numeric: tabular-nums; }
.bd-set { position: absolute; top: 8px; z-index: 3; width: 260px; background: #fff; border: 1px solid #c8ced6; border-radius: 14px; padding: 12px 13px;
  box-shadow: 0 10px 30px rgba(0,0,0,.18); font-size: 13px; color: #1f2937; touch-action: manipulation; }
.bd-set.L { left: 90px; } .bd-set.R { right: 90px; }
.bd-set h4 { margin: 0 0 8px; font-size: 14px; }
.bd-set .row { margin: 10px 0 4px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.bd-set .seg { display: flex; gap: 6px; }
.bd-set .seg button { flex: 1; padding: 8px 6px; border-radius: 9px; border: 1px solid #c8ced6; background: #fff; font: inherit; font-weight: 700; }
.bd-set .seg button.on { border-color: #0d9488; color: #0b6e65; box-shadow: inset 0 0 0 1.5px #0d9488; }
.bd-set input[type=range] { width: 100%; }
.bd-set p { margin: 6px 0 0; font-size: 11.5px; color: #6b7480; line-height: 1.55; }
.bd-diag { position: absolute; bottom: 8px; z-index: 2; font: 600 11.5px/1.5 ui-monospace, Menlo, monospace; color: #1f2937; background: rgba(255,255,255,.9);
  border: 1px solid #c8ced6; border-radius: 10px; padding: 6px 9px; pointer-events: none; max-width: 46%; white-space: pre-wrap; }
.bd-diag.L { left: 90px; } .bd-diag.R { right: 90px; }
.bd-msg { position: absolute; inset: 0; display: grid; place-items: center; font-size: 15px; color: #4b5563; text-align: center; padding: 20px; }
.bd-toast { position: absolute; left: 50%; top: 12px; transform: translateX(-50%); z-index: 4; background: rgba(31,41,55,.9); color: #fff; font-size: 13px;
  font-weight: 700; border-radius: 999px; padding: 7px 14px; pointer-events: none; }
`;
const SHADOW_CSS = `
.csx-p { min-width: 0 !important; }
.pg { display: none !important; }
.pg.bd-cur { display: flex !important; margin: 0 !important; background: #fff; box-shadow: 0 2px 14px rgba(0,0,0,.16); }
.q { cursor: default !important; }
.q:active, .q:hover { background-color: transparent !important; }
`;

/** 길게 눌러야 하는 단추 */
function HoldBtn({ onHold, children, title, ms = 600 }) {
  const [h, setH] = useState(false);
  const tm = useRef(0);
  const start = () => { setH(true); clearTimeout(tm.current); tm.current = setTimeout(() => { setH(false); onHold(); }, ms); };
  const stop = () => { setH(false); clearTimeout(tm.current); };
  useEffect(() => () => clearTimeout(tm.current), []);
  return (
    <button type="button" className={"bd-b" + (h ? " holding" : "")} title={title} aria-label={title}
      onPointerDown={start} onPointerUp={stop} onPointerLeave={stop} onPointerCancel={stop} onContextMenu={(e) => e.preventDefault()}>
      {children}<i className="hold" />
    </button>
  );
}

export default function BoardMode({ catId, set }) {
  const admin = useIsAdmin();
  if (admin === null) return <div className="bd-root"><style>{BD_CSS}</style><div className="bd-msg">확인 중…</div></div>;
  if (!admin) {
    return (
      <div className="bd-root"><style>{BD_CSS}</style>
        <div className="bd-msg"><p>판서 모드는 관리자만 쓸 수 있어요.<br /><a href={`#/sets/${catId}/${pad2(set.no)}`}>세트로 돌아가기</a></p></div>
      </div>
    );
  }
  return <Board catId={catId} set={set} />;
}

function Board({ catId, set }) {
  const rootRef = useRef(null), stageRef = useRef(null), hostRef = useRef(null), cvRef = useRef(null);
  const paperRef = useRef(null), pagesRef = useRef([]);
  const [ready, setReady] = useState(false);
  const [err, setErr] = useState(null);
  const [pi, setPi] = useState(0);
  const [nP, setNP] = useState(0);
  const [cfg, setCfg] = useState(loadCfg);
  const [phase, setPhase] = useState({ phase: "hint", col: cfg.hand });
  const [color, setColor] = useState({ pen: COLORS.pen[0][0], touch: COLORS.touch[0][0] });
  const [tool, setTool] = useState({ pen: "draw", touch: "draw" });
  const [showSet, setShowSet] = useState(false);
  const [rect, setRect] = useState(null);        // 쪽 상자(무대 px)
  const [diag, setDiag] = useState("");
  const [toast, setToast] = useState("");
  const [, bump] = useState(0);                  // 되돌리기 단추 상태 갱신용
  const guard = useMemo(() => new PalmGuard({ hand: cfg.hand, palmSize: cfg.palmSize }), []);   // eslint-disable-line react-hooks/exhaustive-deps
  const ink = useRef(null);
  if (!ink.current) ink.current = { pages: loadInk(catId, set.no), hist: {}, live: new Map(), btn: new Map() };
  const R = useRef({});
  R.current = { pi, rect, color, tool, cfg };

  const toastT = useRef(0);
  const say = useCallback((m) => { setToast(m); clearTimeout(toastT.current); toastT.current = setTimeout(() => setToast(""), 1600); }, []);

  useEffect(() => { lsSet(CK, JSON.stringify(cfg)); guard.setCfg({ palmSize: cfg.palmSize, hand: cfg.hand }); }, [cfg, guard]);

  // 저장(쪽마다)
  const saveT = useRef(0);
  const save = useCallback(() => {
    clearTimeout(saveT.current);
    saveT.current = setTimeout(() => {
      const pages = Object.fromEntries(Object.entries(ink.current.pages).filter(([, v]) => v && v.length));
      lsSet(dataKey(catId, set.no), JSON.stringify({ v: 1, pages }));
    }, 400);
  }, [catId, set.no]);
  useEffect(() => () => {
    clearTimeout(saveT.current);
    const pages = Object.fromEntries(Object.entries(ink.current.pages).filter(([, v]) => v && v.length));
    lsSet(dataKey(catId, set.no), JSON.stringify({ v: 1, pages }));
  }, [catId, set.no]);

  // 문제지 불러와 shadow 에 펼치기
  useEffect(() => {
    let alive = true;
    ensureSerif();
    fetch(printUrl(catId, set.no, "problems"), { cache: "no-cache" })
      .then((r) => { if (!r.ok) throw new Error(`문제지를 불러오지 못했어요 (${r.status})`); return r.text(); })
      .then((html) => {
        if (!alive || !hostRef.current) return;
        const doc = splitDoc(html);
        ensureLinks(doc.links);
        const p = new Paper(hostRef.current, doc, set, {});
        const st = document.createElement("style");
        st.textContent = SHADOW_CSS;
        p.root.appendChild(st);
        paperRef.current = p;
        pagesRef.current = [...p.root.querySelectorAll(".pg")];
        setNP(pagesRef.current.length);
        setReady(true);
      })
      .catch((e) => { if (alive) setErr(e?.message || String(e)); });
    return () => { alive = false; paperRef.current?.destroy(); paperRef.current = null; };
  }, [catId, set]);

  /* ── 그리기 ── */
  const strokesOf = (i) => (ink.current.pages[i] = ink.current.pages[i] || []);
  const ctxOf = () => {
    const cv = cvRef.current, st = stageRef.current;
    if (!cv || !st) return null;
    const dpr = Math.min(3, window.devicePixelRatio || 1), W = st.clientWidth, H = st.clientHeight;
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
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
    let [x0, y0] = pt(0);
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
    const ctx = ctxOf(), pg = R.current.rect, st = stageRef.current;
    if (!ctx || !st) return;
    ctx.clearRect(0, 0, st.clientWidth, st.clientHeight);
    if (!pg) return;
    for (const s of strokesOf(R.current.pi)) pathStroke(ctx, s, pg);
    for (const L of ink.current.live.values()) if (L.tool === "draw") pathStroke(ctx, L, pg);
  }, []);
  const drawSeg = (L) => {
    const ctx = ctxOf(), pg = R.current.rect;
    if (!ctx || !pg) return;
    const P = L.p, n = P.length;
    const k = (pg.r - pg.l) / PAGE_W_PX;
    ctx.strokeStyle = L.c; ctx.lineWidth = Math.max(1, L.w * k);
    ctx.beginPath();
    const a = toStage(pg, PAGE_W_PX, P[Math.max(0, n - 4)], P[Math.max(1, n - 3)]), b = toStage(pg, PAGE_W_PX, P[n - 2], P[n - 1]);
    ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
  };

  /* ── 쪽 배치: 화면에 한 쪽을 통째로(높이 · 너비 중 맞는 쪽으로), 도구 막대 자리는 비운다 ── */
  const layout = useCallback(() => {
    const st = stageRef.current, p = paperRef.current, pg = pagesRef.current[R.current.pi];
    if (!st || !p || !pg) return;
    pagesRef.current.forEach((el, i) => el.classList.toggle("bd-cur", i === R.current.pi));
    p.setZoom(1);
    const h1 = pg.getBoundingClientRect().height || 1120;
    const W = st.clientWidth, H = st.clientHeight, bar = 90;
    const z = Math.max(0.2, Math.min((W - bar * 2) / PAGE_W_PX, (H - 16) / h1));
    p.setZoom(z.toFixed(4));
    const host = hostRef.current;
    host.style.left = `${Math.round((W - PAGE_W_PX * z) / 2)}px`;
    host.style.top = `${Math.round(Math.max(8, (H - h1 * z) / 2))}px`;
    const sr = st.getBoundingClientRect(), r = pg.getBoundingClientRect();
    const box = { l: r.left - sr.left, t: r.top - sr.top, r: r.right - sr.left, b: r.bottom - sr.top };
    R.current.rect = box;
    guard.setPage(box);
    setRect(box);
    redraw();
  }, [guard, redraw]);
  useEffect(() => { if (ready) layout(); }, [ready, pi, layout]);
  useEffect(() => {
    const st = stageRef.current;
    if (!st || typeof ResizeObserver === "undefined") return undefined;
    const ro = new ResizeObserver(() => layout());
    ro.observe(st);
    // 글꼴이 늦게 와 쪽 높이가 바뀌면 다시
    document.fonts?.ready?.then(() => layout()).catch(() => {});
    return () => ro.disconnect();
  }, [layout]);

  /* ── 동작(palm.js) → 획 ── */
  const hist = (i) => (ink.current.hist[i] = ink.current.hist[i] || []);
  const eraseAt = (L, u, v) => {
    const list = strokesOf(R.current.pi);
    const hit = hitStrokes(list, u, v, ERASE_R);
    if (!hit.length) return;
    for (let j = hit.length - 1; j >= 0; j--) L.removed.push(list.splice(hit[j], 1)[0]);
    redraw();
  };
  const apply = useCallback((acts) => {
    if (!acts.length) return;
    const pg = R.current.rect;
    let dirty = false, phaseChanged = null;
    for (const a of acts) {
      if (a.k === "start") {
        const btn = ink.current.btn.get(a.id) || 0;
        const erase = R.current.tool[a.src] === "erase" || (a.src === "pen" && (btn & 32 || btn & 2));
        const L = { src: a.src, tool: erase ? "erase" : "draw", c: R.current.color[a.src], w: WIDTH[a.src], p: [], removed: [] };
        ink.current.live.set(a.id, L);
        for (const [x, y] of a.pts) {
          const [u, v] = toPage(pg, PAGE_W_PX, x, y);
          if (L.tool === "erase") eraseAt(L, u, v); else L.p.push(u, v);
        }
        if (L.tool === "draw") { if (L.p.length > 2) dirty = true; else drawSeg(L); }
      } else if (a.k === "add") {
        const L = ink.current.live.get(a.id);
        if (!L || !pg) continue;
        for (const [x, y] of a.pts) {
          const [u, v] = toPage(pg, PAGE_W_PX, x, y);
          if (L.tool === "erase") eraseAt(L, u, v);
          else {
            const n = L.p.length;
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
          strokesOf(R.current.pi).push(s);
          hist(R.current.pi).push({ src: L.src, add: s });
        } else if (L.tool === "erase" && L.removed.length) hist(R.current.pi).push({ src: L.src, del: L.removed });
        dirty = true; save(); bump((n) => n + 1);
      } else if (a.k === "drop") {
        const L = ink.current.live.get(a.id);
        ink.current.live.delete(a.id); ink.current.btn.delete(a.id);
        if (L?.removed?.length) strokesOf(R.current.pi).push(...L.removed);
        dirty = true;
      } else if (a.k === "phase") phaseChanged = { phase: a.phase, col: a.col };
      else if (a.k === "reject" && R.current.cfg.diag) setDiag((d) => `버림 #${a.id} · ${({ size: "접촉이 넓음(손바닥)", "pen-near": "펜 근처(선생님 손)", "pen-after": "펜이 바로 옆에 닿음", "rest-near": "쪽 밖 손 근처", edge: "가장자리 여백", "one-writer": "이미 쓰는 중", "two-touch": "두 점이 함께 닿음", locked: "잠긴 단", below: "필기 아래 · 손 쪽", "palm-near": "손바닥 옆" })[a.why] || a.why}\n${d.split("\n")[0] || ""}`);
    }
    if (dirty) redraw();
    if (phaseChanged) {
      setPhase(phaseChanged);
      if (phaseChanged.phase === "locked" && phaseChanged.col !== R.current.cfg.hand) setCfg((c) => ({ ...c, hand: phaseChanged.col }));
      if (phaseChanged.phase === "locked") say(`손 받침 확인 — ${phaseChanged.col === "R" ? "오른쪽" : "왼쪽"} 단은 잠시 쉬어요`);
      if (phaseChanged.phase === "free") say("이제 쪽 어디든 써요");
    }
  }, [redraw, save, say]);

  /* ── 포인터 ── */
  useEffect(() => {
    const st = stageRef.current;
    if (!st || !ready) return undefined;
    const P = (e) => {
      const sr = st.getBoundingClientRect();
      return { id: e.pointerId, type: e.pointerType || "mouse", x: e.clientX - sr.left, y: e.clientY - sr.top,
        w: e.width || 0, h: e.height || 0, t: e.timeStamp || performance.now(), buttons: e.buttons };
    };
    const showDiag = (e, what) => {
      if (!R.current.cfg.diag) return;
      setDiag((d) => `${what} ${e.pointerType} #${e.pointerId} · 크기 ${Math.round(e.width || 0)}×${Math.round(e.height || 0)} · 압력 ${(e.pressure || 0).toFixed(2)}\n${d.split("\n").slice(-1)[0] || ""}`);
    };
    const down = (e) => {
      e.preventDefault();
      try { st.setPointerCapture(e.pointerId); } catch { /* 무시 */ }
      ink.current.btn.set(e.pointerId, e.buttons);
      showDiag(e, "닿음");
      apply(guard.down(P(e)));
    };
    const move = (e) => {
      const list = e.getCoalescedEvents ? e.getCoalescedEvents() : null;
      const evs = list && list.length ? list : [e];
      const acts = [];
      for (const ce of evs) {
        const p = P(ce); p.id = e.pointerId; p.type = e.pointerType || "mouse";
        acts.push(...guard.move(p));
      }
      apply(acts);
    };
    const up = (e) => { apply(guard.up(P(e))); };
    const cancel = (e) => { apply(guard.cancel(P(e))); };
    const noMenu = (e) => e.preventDefault();
    st.addEventListener("pointerdown", down, { passive: false });
    st.addEventListener("pointermove", move);
    st.addEventListener("pointerup", up);
    st.addEventListener("pointercancel", cancel);
    st.addEventListener("contextmenu", noMenu);
    // 손을 가만히 대고 있을 때(움직임 없음)도 시간 규칙이 돌게
    let raf = 0;
    const loop = () => { raf = requestAnimationFrame(loop); if (guard.busy()) apply(guard.tick(performance.now())); };
    raf = requestAnimationFrame(loop);
    return () => {
      st.removeEventListener("pointerdown", down); st.removeEventListener("pointermove", move);
      st.removeEventListener("pointerup", up); st.removeEventListener("pointercancel", cancel); st.removeEventListener("contextmenu", noMenu);
      cancelAnimationFrame(raf);
    };
  }, [ready, guard, apply]);

  /* ── 화면 꺼짐 방지 · 제목 ── */
  useEffect(() => {
    let lock = null;
    const req = async () => { try { if (document.visibilityState === "visible" && navigator.wakeLock) lock = await navigator.wakeLock.request("screen"); } catch { /* 지원 안 함 */ } };
    req();
    const onVis = () => { if (document.visibilityState === "visible") req(); };
    document.addEventListener("visibilitychange", onVis);
    const prev = document.title; document.title = `판서 — ${set.short || set.title}`;
    return () => { document.removeEventListener("visibilitychange", onVis); try { lock?.release?.(); } catch { /* 무시 */ } document.title = prev; };
  }, [set]);

  /* ── 도구 ── */
  const goPage = (d) => {
    const n = Math.max(0, Math.min(nP - 1, pi + d));
    if (n === pi) return;
    ink.current.live.clear();
    apply(guard.rehint());
    setPi(n);
  };
  const undo = (src) => {
    const H = hist(pi);
    for (let j = H.length - 1; j >= 0; j--) {
      if (H[j].src !== src) continue;
      const e = H.splice(j, 1)[0], list = strokesOf(pi);
      if (e.add) { const k = list.lastIndexOf(e.add); if (k >= 0) list.splice(k, 1); }
      if (e.del) list.push(...e.del);
      redraw(); save(); bump((x) => x + 1);
      return;
    }
  };
  const canUndo = (src) => hist(pi).some((e) => e.src === src);
  const clearPage = () => {
    const list = strokesOf(pi);
    if (!list.length) return;
    hist(pi).length = 0;
    ink.current.pages[pi] = [];
    redraw(); save(); bump((x) => x + 1);
    say("이 쪽 판서를 지웠어요");
  };
  const exit = () => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    location.hash = `#/sets/${catId}/${pad2(set.no)}`;
  };
  const toggleFs = async () => {
    try {
      if (!document.fullscreenElement) {
        await rootRef.current?.requestFullscreen?.({ navigationUI: "hide" });
        try { await screen.orientation?.lock?.("landscape"); } catch { /* 고정 불가 */ }
      } else await document.exitFullscreen();
    } catch { /* 불가 */ }
  };

  const side = cfg.hand === "R" ? "L" : "R";   // 도구 막대 = 학생 손 반대쪽
  const half = rect ? (rect.r - rect.l) / 2 : 0;
  const zoneStyle = (col) => rect && ({ left: col === "R" ? rect.l + half : rect.l, top: rect.t, width: half, height: rect.b - rect.t });
  const group = (src) => (
    <div className="bd-grp">
      <span className="lb">{WHO[src]}<br /><small>{src === "pen" ? "S펜" : "손 · 터치펜"}</small></span>
      <div className="bd-dots">
        {COLORS[src].map(([c, nm]) => (
          <button key={c} type="button" className={"bd-dot" + (color[src] === c && tool[src] === "draw" ? " on" : "")} style={{ background: c }}
            title={`${WHO[src]} ${nm}`} aria-label={`${WHO[src]} ${nm}`}
            onClick={() => { setColor((o) => ({ ...o, [src]: c })); setTool((o) => ({ ...o, [src]: "draw" })); }} />
        ))}
      </div>
      <button type="button" className={"bd-b" + (tool[src] === "erase" ? " on" : "")} title={`${WHO[src]} 지우개`}
        onClick={() => setTool((o) => ({ ...o, [src]: o[src] === "erase" ? "draw" : "erase" }))}>지우개</button>
      <button type="button" className="bd-b" disabled={!canUndo(src)} title={`${WHO[src]} 되돌리기`} onClick={() => undo(src)}>↶ 되돌리기</button>
    </div>
  );

  return (
    <div ref={rootRef} className="bd-root">
      <style>{BD_CSS}</style>
      <div ref={stageRef} className="bd-stage">
        <div ref={hostRef} className="bd-host" />
        {rect && phase.phase === "hint" && (
          <div className="bd-zone hint" style={zoneStyle(cfg.hand)}><b>✋ 학생 손바닥을<br />여기에 먼저 올려 두세요</b></div>
        )}
        {rect && phase.phase === "locked" && <div className="bd-zone lock" style={zoneStyle(phase.col)} />}
        <canvas ref={cvRef} className="bd-cv" />
        {!ready && <div className="bd-msg">{err || "문제지를 펼치는 중…"}</div>}
      </div>

      <div className={"bd-bar " + side} onPointerDown={(e) => e.stopPropagation()}>
        <div className="bd-grp">
          <HoldBtn title="길게 눌러 나가기" onHold={exit}>✕ 나가기</HoldBtn>
          <button type="button" className="bd-b" disabled={pi <= 0} onClick={() => goPage(-1)} title="앞 쪽">‹ 앞</button>
          <span className="bd-pg">{nP ? `${pi + 1} / ${nP}` : "…"}</span>
          <button type="button" className="bd-b" disabled={pi >= nP - 1} onClick={() => goPage(1)} title="다음 쪽">다음 ›</button>
        </div>
        {group("pen")}
        {group("touch")}
        <div className="bd-grp">
          {phase.phase === "hint"
            ? <button type="button" className="bd-b" onClick={() => apply(guard.skipHint())} title="손 받침 안내 건너뛰기">안내 건너뛰기</button>
            : <button type="button" className="bd-b" onClick={() => apply(guard.rehint())} title="손 받침 다시">손 받침 다시</button>}
          <HoldBtn title="길게 눌러 이 쪽 판서 지우기" onHold={clearPage} ms={800}>쪽 지우기</HoldBtn>
          <button type="button" className="bd-b" onClick={toggleFs} title="전체 화면">⛶ 전체</button>
          <button type="button" className={"bd-b" + (showSet ? " on" : "")} onClick={() => setShowSet((v) => !v)} title="설정">⚙ 설정</button>
        </div>
      </div>

      {showSet && (
        <div className={"bd-set " + side} onPointerDown={(e) => e.stopPropagation()}>
          <h4>판서 설정</h4>
          <div className="row">학생 손잡이</div>
          <div className="seg">
            {[["R", "오른손"], ["L", "왼손"]].map(([k, l]) => (
              <button key={k} type="button" className={cfg.hand === k ? "on" : ""}
                onClick={() => { setCfg((c) => ({ ...c, hand: k })); guard.setCfg({ hand: k }); apply(guard.rehint()); }}>{l}</button>
            ))}
          </div>
          <p>손바닥을 안내 칸에 대면 저절로 맞춰져요. 도구 막대는 손 반대쪽으로 옮겨 가요.</p>
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
      {cfg.diag && <div className={"bd-diag " + side}>{diag || "화면에 닿아 보세요 — 펜 · 손가락 · 손바닥의 종류와 크기가 여기 떠요."}</div>}
      {toast && <div className="bd-toast" role="status">{toast}</div>}
    </div>
  );
}
