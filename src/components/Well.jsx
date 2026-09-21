// 우물 — 하단 탭바 중앙의 원형 버튼. 애쉬레인의 메인 테마.
// 그림은 기본 1장: 번들 /brand/well/base.webp (관리자가 figures/well/base.* 업로드로 교체 가능).
// 연출은 3가지(사용자 확정): 맑은 낮 = 태양 각도 그림자(나침반 되는 기기는 실제 방위 연동) ·
// 흐림/비 = 그림자 없이 감광 · 밤 = 중앙에 조명이 비치는 연출. 탭하면 카메라 기능 런처.
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { getWx } from "../lib/wx";
import { sunPos, shadowOf } from "../lib/sun";
import { WELL_FEATURES, WELL_DEFAULT, clampWellCfg, wellMode } from "../lib/well";

/** 번들 기본 이미지 — 템페라 화풍 돌우물 (배경 오려낸 원형 메달) */
export const WELL_BUNDLED = "/brand/well/base.webp";

/* ── 설정 (app_settings.well_ui) — localStorage 즉시 + 서버 값 갱신 ── */
export function useWellCfg() {
  const [cfg, setCfg] = useState(() => {
    try { return clampWellCfg(localStorage.getItem("ash.wellui")); } catch { return clampWellCfg(null); }
  });
  useEffect(() => {
    let alive = true;
    supabase.from("app_settings").select("value").eq("key", "well_ui").maybeSingle()
      .then(({ data }) => {
        if (!alive || !data?.value) return;
        const c = clampWellCfg(data.value);
        setCfg(c);
        try { localStorage.setItem("ash.wellui", JSON.stringify(c)); } catch { /* 무시 */ }
      })
      .catch(() => {});
    const on = () => { try { setCfg(clampWellCfg(localStorage.getItem("ash.wellui"))); } catch { /* 무시 */ } };
    window.addEventListener("ash:wellui", on);
    return () => { alive = false; window.removeEventListener("ash:wellui", on); };
  }, []);
  return cfg;
}

/* ── 우물 이미지 — 스토리지 figures/well/base.* 가 있으면 그걸, 없으면 번들 (10분 캐시) ── */
let imgCache;            // undefined 미조회 | null 없음 | { name, url }
let imgAt = 0;
export function useWellImg(bust = 0) {
  const [img, setImg] = useState(() => (imgCache === undefined ? null : imgCache));
  useEffect(() => {
    let alive = true;
    (async () => {
      if (imgCache !== undefined && Date.now() - imgAt < 10 * 60e3 && !bust) { setImg(imgCache); return; }
      try {
        const { data } = await supabase.storage.from("figures").list("well", { limit: 20 });
        const f = (data || []).find((x) => x.name.replace(/\.[^.]+$/, "") === "base");
        let v = null;
        if (f) {
          const { data: pu } = supabase.storage.from("figures").getPublicUrl(`well/${f.name}`);
          v = { name: f.name, url: pu.publicUrl + "?v=" + encodeURIComponent(f.updated_at || "") };
        }
        if (alive) { imgCache = v; imgAt = Date.now(); setImg(v); }
      } catch { /* 번들 폴백 */ }
    })();
    return () => { alive = false; };
  }, [bust]);
  return img; // null 이면 번들 이미지를 쓴다
}
export function bustWellImg() { imgCache = undefined; imgAt = 0; }

/* ── 나침반 — 화면 위쪽이 향한 방위(도). 안 되면 [0, false] ── */
export function useHeading(on) {
  const [hd, setHd] = useState(0);
  const [live, setLive] = useState(false);
  useEffect(() => {
    if (!on) { setLive(false); setHd(0); return; }
    let cur = null, target = null, raf = 0, lastSet = 0;
    const norm = (a) => ((a % 360) + 360) % 360;
    const step = () => {
      raf = 0;
      if (target == null) return;
      if (cur == null) cur = target;
      const d = norm(target - cur + 180) - 180; // 최단 호
      cur = norm(cur + d * 0.25);
      const now = Date.now();
      if (now - lastSet > 90) { lastSet = now; setHd(Math.round(cur)); }
      if (Math.abs(d) > 0.6) raf = requestAnimationFrame(step);
      else setHd(Math.round(cur));
    };
    const onEv = (e) => {
      const h = e.webkitCompassHeading != null ? e.webkitCompassHeading
        : (e.absolute && e.alpha != null ? 360 - e.alpha : null);
      if (h == null || Number.isNaN(h)) return;
      target = norm(h);
      setLive(true);
      if (!raf) raf = requestAnimationFrame(step);
    };
    const ev = "ondeviceorientationabsolute" in window ? "deviceorientationabsolute" : "deviceorientation";
    window.addEventListener(ev, onEv, true);
    return () => { window.removeEventListener(ev, onEv, true); if (raf) cancelAnimationFrame(raf); };
  }, [on]);
  return [hd, live];
}

/** iOS 는 사용자 탭 안에서 방향 센서 권한을 물어야 한다 — 우물 첫 탭에서 한 번 */
export function requestCompass() {
  try {
    const D = window.DeviceOrientationEvent;
    if (D && typeof D.requestPermission === "function") return D.requestPermission().then((r) => r === "granted").catch(() => false);
    return Promise.resolve(true);
  } catch { return Promise.resolve(false); }
}

/* ── 자리그림 — 번들 이미지마저 못 불러올 때의 최후 폴백 (원작 SVG) ── */
const STONES = Array.from({ length: 11 }, (_, i) => i * (360 / 11));
const STONE_FILL = ["#8B8E96", "#7C7F88", "#95989F", "#84878F", "#8F929A"];
export function PlaceholderWell({ size = 92 }) {
  return (
    <svg viewBox="0 0 100 100" width={size} height={size} aria-hidden="true">
      <defs>
        <radialGradient id="wl-g-water" cx="46%" cy="42%">
          <stop offset="0%" stopColor="#1D7A8C" /><stop offset="70%" stopColor="#0F4A5C" /><stop offset="100%" stopColor="#0B3644" />
        </radialGradient>
      </defs>
      <circle cx={50} cy={50} r={46.5} fill="#63666E" />
      <circle cx={50} cy={50} r={30.5} fill="url(#wl-g-water)" />
      <ellipse cx={42} cy={41} rx={12} ry={6.5} fill="#DFF6FF" opacity=".2" transform="rotate(-24 42 41)" />
      <circle cx={50} cy={50} r={30.5} fill="none" stroke="#2E333C" strokeWidth="1.6" opacity=".7" />
      {STONES.map((a, i) => (
        <g key={a} transform={`rotate(${a} 50 50)`}>
          <rect x={41.5} y={3.5} width={17} height={14.5} rx={6.2}
            fill={STONE_FILL[i % STONE_FILL.length]} stroke="#6A6D75" strokeWidth=".7" />
        </g>
      ))}
    </svg>
  );
}

/* ── 우물 버튼 (탭바 중앙) ── */
export function WellButton({ theme = "light", cfg = WELL_DEFAULT, onOpen,
  reveal = false, modeOverride = null, hourOverride = null, headingOverride = null }) {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => { const t = setInterval(() => setNow(new Date()), 60000); return () => clearInterval(t); }, []);
  const [wx, setWx] = useState(null);
  useEffect(() => {
    let a = true;
    getWx().then((w) => { if (a) setWx(w); });
    const t = setInterval(() => getWx().then((w) => { if (a) setWx(w); }), 10 * 60e3);
    return () => { a = false; clearInterval(t); };
  }, []);
  const stImg = useWellImg();
  const [broken, setBroken] = useState(false);
  const [heading, hdLive] = useHeading(!!cfg.fx.compass && headingOverride == null);
  const askedRef = useRef(false);

  const hour = hourOverride ?? now.getHours();
  const date = useMemo(() => {
    if (hourOverride == null) return now;
    const d = new Date(now); d.setHours(hourOverride, 30, 0, 0); return d;
  }, [now, hourOverride]);
  const mode = modeOverride || wellMode(wx, hour);
  const sun = useMemo(() => sunPos(date), [date]);
  const hd = headingOverride ?? (hdLive ? heading : 0);
  const sh = mode === "sun" && cfg.fx.shadow ? shadowOf(sun, hd, cfg.btn.d) : null;

  const showImg = cfg.img.on || reveal;
  const d = cfg.btn.d;
  const imgD = Math.round(d * cfg.img.scale / 100);
  const btnBottom = `calc(var(--wt-h, 52px) - ${d - cfg.btn.dy}px)`;
  const sunDir = sh ? (((sun.az - hd) % 360) + 360) % 360 : null;

  // 3연출: 맑음 = 해 그림자 / 흐림·비 = 감광 / 밤 = 감광 + 중앙 조명
  const filters = [];
  if (mode === "dim") filters.push("brightness(.74) saturate(.85)");
  if (mode === "night") filters.push("brightness(.8) saturate(.9)");
  if (sh) filters.push(`drop-shadow(${sh.dx}px ${sh.dy}px ${sh.blur}px rgba(15,20,30,${sh.alpha}))`);
  else if (mode === "night") filters.push("drop-shadow(0 3px 9px rgba(130,160,255,.25))");
  else filters.push("drop-shadow(0 2px 5px rgba(15,20,30,.28))");

  const open = () => {
    if (cfg.fx.compass && !askedRef.current && !sessionStorage.getItem("ash.compass.asked")) {
      askedRef.current = true;
      try { sessionStorage.setItem("ash.compass.asked", "1"); } catch { /* 무시 */ }
      requestCompass(); // iOS: 탭 제스처 안에서 1회 — 결과와 무관하게 폴백이 있다
    }
    onOpen?.();
  };

  return (
    <div className="wl-slot" style={{ "--wl-d": d + "px" }}>
      {showImg && (
        <div className="wl-img" aria-hidden="true"
          style={{ width: imgD, height: imgD, bottom: btnBottom,
            transform: `translateX(-50%) translateY(${(imgD - d) / 2 - cfg.img.dy}px)`, filter: filters.join(" ") }}>
          <div className="wl-core">
            {broken && !stImg ? <PlaceholderWell size={imgD} />
              : <img src={stImg ? stImg.url : WELL_BUNDLED} alt="" draggable="false"
                  onError={() => setBroken(true)} />}
            {sunDir != null && (
              <div className="wl-shade" style={{
                background: `linear-gradient(${Math.round((sunDir + 180) % 360)}deg, rgba(6,10,18,${(0.14 + 0.18 * (1 - Math.min(sun.el, 75) / 75)).toFixed(2)}) 0%, rgba(6,10,18,0) 58%)`,
              }} />
            )}
            {mode === "night" && <div className="wl-lamp" />}
          </div>
        </div>
      )}
      <button type="button" className={"wl-btn" + (showImg ? " ghost" : "")} style={{ bottom: btnBottom }}
        aria-label="우물 — 사진으로 배우는 기능 열기" title="우물" onClick={open}>
        {!showImg && <span className="wl-dot">⛲</span>}
      </button>
    </div>
  );
}

/* ── 런처 시트 — 카메라 기능 바로 실행 ── */
export function WellSheet({ open, onClose, theme = "light" }) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === "Escape") onClose?.(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);
  if (!open) return null;
  const go = (to) => { onClose?.(); location.hash = to; };
  return (
    <div className={`wl-sheet wl-${theme}`} role="dialog" aria-modal="true" aria-label="우물 — 사진 기능">
      <div className="wl-dim" onClick={onClose} />
      <div className="wl-panel">
        <div className="wl-grip" aria-hidden="true" />
        <p className="wl-title">⛲ 우물 <span>문제를 찍으면, 여기서 길어 올려요</span></p>
        <div className="wl-grid">
          {WELL_FEATURES.map(([ic, nm, ds, to]) => (
            <button key={to} type="button" className="wl-item" onClick={() => go(to)}>
              <span className="ic">{ic}</span>
              <span className="nm">{nm}</span>
              <span className="ds">{ds}</span>
            </button>
          ))}
        </div>
        <div className="wl-links">
          <button type="button" onClick={() => go("#/records")}>🗂 내 기록</button>
          <span className="sp" />
          <button type="button" className="wl-close" onClick={onClose}>닫기</button>
        </div>
      </div>
    </div>
  );
}

export const WELL_CSS = `
.wl-slot { position: relative; flex: none; height: 100%; width: calc(var(--wl-d, 46px) + 26px); }
.wl-btn { position: absolute; left: 50%; transform: translateX(-50%); width: var(--wl-d, 46px); height: var(--wl-d, 46px);
  border-radius: 50%; cursor: pointer; z-index: 3; padding: 0; font-family: inherit;
  background: var(--card); border: 1.5px dashed var(--mut); color: var(--mut);
  display: flex; align-items: center; justify-content: center; }
/* 탭할 때 모바일 브라우저가 씌우는 사각형 하이라이트 제거 (우물은 원형이라 특히 티가 난다) */
.wl-btn, .wl-dim, .wl-item, .wl-links button { -webkit-tap-highlight-color: transparent; }
.wl-btn .wl-dot { font-size: calc(var(--wl-d, 46px) * .44); line-height: 1; }
.wl-btn.ghost { background: none; border-color: transparent; color: transparent; }
.wl-btn:active { transform: translateX(-50%) scale(.96); }
.wl-img { position: absolute; left: 50%; z-index: 2; pointer-events: none; }
.wl-core { position: relative; width: 100%; height: 100%; animation: wl-breathe 7s ease-in-out infinite; }
.wl-core img, .wl-core svg { width: 100%; height: 100%; display: block; user-select: none; }
.wl-core img { object-fit: contain; }
.wl-shade { position: absolute; inset: 9%; border-radius: 50%; mix-blend-mode: multiply; }
.wl-lamp { position: absolute; inset: 6%; border-radius: 50%; mix-blend-mode: screen;
  background: radial-gradient(circle at 50% 46%, rgba(255,241,198,.55) 0%, rgba(255,236,186,.22) 34%, rgba(0,0,0,0) 62%); }
@keyframes wl-breathe { 0%,100% { transform: scale(1); } 50% { transform: scale(1.022); } }
@media (prefers-reduced-motion: reduce) { .wl-core { animation: none; } }

.wl-sheet { position: fixed; inset: 0; z-index: 120;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.wl-sheet * { box-sizing: border-box; }
.wl-light { --wsb:#FFFFFF; --wsbd:#DFE3E8; --wsi:#1F2937; --wsm:#8A929C; --wsc:#F3F5F7; --wsa:#0D9488; }
.wl-dark { --wsb:#15171C; --wsbd:#23262D; --wsi:#E2E8F0; --wsm:#8A929C; --wsc:#1C1F26; --wsa:#5EEAD4; }
.wl-dim { position: absolute; inset: 0; background: rgba(8,10,14,.5); animation: wl-fade .18s ease; }
.wl-panel { position: absolute; left: 50%; transform: translateX(-50%); bottom: 0; width: 100%; max-width: 520px;
  background: var(--wsb); border: 1px solid var(--wsbd); border-bottom: none; border-radius: 20px 20px 0 0;
  padding: 8px 14px calc(14px + env(safe-area-inset-bottom, 0px)); color: var(--wsi);
  animation: wl-rise .22s cubic-bezier(.2,.9,.3,1); }
.wl-grip { width: 40px; height: 4px; border-radius: 99px; background: var(--wsbd); margin: 2px auto 8px; }
.wl-title { margin: 0 0 10px; font-size: 15px; font-weight: 800; }
.wl-title span { font-size: 11.5px; font-weight: 600; color: var(--wsm); margin-left: 7px; }
.wl-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.wl-item { display: flex; flex-direction: column; align-items: flex-start; gap: 3px; text-align: left;
  background: var(--wsc); border: 1px solid var(--wsbd); border-radius: 13px; padding: 11px 12px;
  cursor: pointer; color: var(--wsi); font-family: inherit; }
.wl-item:active { transform: scale(.98); }
.wl-item .ic { font-size: 19px; line-height: 1.1; }
.wl-item .nm { font-size: 13px; font-weight: 800; }
.wl-item .ds { font-size: 10.5px; color: var(--wsm); line-height: 1.45; }
.wl-links { display: flex; gap: 6px; align-items: center; margin-top: 10px; }
.wl-links .sp { flex: 1; }
.wl-links button { background: none; border: none; color: var(--wsm); font-size: 12px; font-weight: 700;
  cursor: pointer; font-family: inherit; padding: 6px 6px; }
.wl-links .wl-close { color: var(--wsi); background: var(--wsc); border: 1px solid var(--wsbd); border-radius: 999px; padding: 6px 14px; }
@keyframes wl-rise { from { transform: translateX(-50%) translateY(24px); opacity: 0; } to { transform: translateX(-50%) translateY(0); opacity: 1; } }
@keyframes wl-fade { from { opacity: 0; } to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .wl-panel, .wl-dim { animation: none; } }
`;
