// 우물 — 하단 탭바 중앙의 원형 버튼. 애쉬레인의 메인 테마.
// 시간·실황 날씨(대시보드 히어로와 같은 신호)에 따라 우물 그림이 바뀌고,
// 태양 각도에 맞춘 그림자(나침반 되는 기기는 실제 방위 연동), 탭하면 카메라 기능 런처가 열린다.
// 그림이 없으면 자리그림(SVG)으로 그린다 — 관리자 업로드는 #/admin/well.
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { getWx } from "../lib/wx";
import { sunPos, shadowOf } from "../lib/sun";
import {
  WELL_FEATURES, WELL_DEFAULT, clampWellCfg, wellVariant, timeBand, bandFilter, resolveWellImg,
} from "../lib/well";

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

/* ── 변주 이미지 (figures/well/<key>.*) — 10분 캐시 ── */
let imgCache = null, imgAt = 0;
export function useWellImgs(bust = 0) {
  const [map, setMap] = useState(() => imgCache || {});
  useEffect(() => {
    let alive = true;
    (async () => {
      if (imgCache && Date.now() - imgAt < 10 * 60e3 && !bust) { setMap(imgCache); return; }
      try {
        const { data } = await supabase.storage.from("figures").list("well", { limit: 60 });
        const m = {};
        for (const f of data || []) {
          const key = f.name.replace(/\.[^.]+$/, "");
          const { data: pu } = supabase.storage.from("figures").getPublicUrl(`well/${f.name}`);
          m[key] = { name: f.name, url: pu.publicUrl + "?v=" + encodeURIComponent(f.updated_at || "") };
        }
        if (alive) { imgCache = m; imgAt = Date.now(); setMap(m); }
      } catch { /* 자리그림 폴백 */ }
    })();
    return () => { alive = false; };
  }, [bust]);
  return map;
}
export function bustWellImgs() { imgCache = null; imgAt = 0; }

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

/* ── 자리그림 — 위에서 내려다본 돌우물 (원작 SVG, 변주별) ── */
const STONES = Array.from({ length: 11 }, (_, i) => i * (360 / 11));
const STONE_FILL = ["#8B8E96", "#7C7F88", "#95989F", "#84878F", "#8F929A"];
export function PlaceholderWell({ variant = "water", size = 92 }) {
  const wet = variant === "rain" || variant === "drizzle";
  const rim = STONES.map((a, i) => (
    <g key={a} transform={`rotate(${a} 50 50)`}>
      <rect x={41.5} y={3.5} width={17} height={14.5} rx={6.2}
        fill={STONE_FILL[i % STONE_FILL.length]} stroke={wet ? "#4A5560" : "#6A6D75"} strokeWidth=".7" />
      {wet && <rect x={43} y={5} width={14} height={5} rx={3} fill="#B9C9D6" opacity=".28" />}
      {(variant === "snow") && <rect x={42.5} y={2.6} width={15} height={6.5} rx={3.4} fill="#F5F9FF" stroke="#D8E4F2" strokeWidth=".5" />}
      {(variant === "frost") && <rect x={42.5} y={3} width={15} height={4.6} rx={2.4} fill="#DDF1FA" opacity=".85" />}
    </g>
  ));
  const ripples = (n, tone, w = 1.1) => Array.from({ length: n }, (_, i) => (
    <circle key={i} cx={50} cy={50} r={8 + i * (18 / n)} fill="none" stroke={tone} strokeWidth={w} opacity={0.5 - i * 0.09} />
  ));
  let inner = null;
  if (variant === "dark") inner = (<>
    <circle cx={50} cy={50} r={30.5} fill="url(#wl-g-dark)" />
    <path d="M 27 41 A 26 26 0 0 1 45 26" fill="none" stroke="#3D4654" strokeWidth="2.4" opacity=".55" strokeLinecap="round" />
  </>);
  else if (variant === "water") inner = (<>
    <circle cx={50} cy={50} r={30.5} fill="url(#wl-g-water)" />
    <ellipse cx={42} cy={41} rx={12} ry={6.5} fill="#DFF6FF" opacity=".2" transform="rotate(-24 42 41)" />
    {ripples(2, "#8FDCE8", 0.9)}
  </>);
  else if (variant === "drizzle") inner = (<>
    <circle cx={50} cy={50} r={30.5} fill="url(#wl-g-water)" />
    <ellipse cx={42} cy={41} rx={11} ry={6} fill="#DFF6FF" opacity=".16" transform="rotate(-24 42 41)" />
    {ripples(3, "#9FE3EE")}
  </>);
  else if (variant === "rain") inner = (<>
    <circle cx={50} cy={50} r={32} fill="url(#wl-g-rain)" />
    {ripples(5, "#C4EFF7", 1.2)}
    {[[36, 38], [62, 33], [57, 60], [40, 62]].map(([x, y], i) => (
      <circle key={i} cx={x} cy={y} r={1.4} fill="#EAFBFF" opacity=".85" />
    ))}
  </>);
  else if (variant === "snow") inner = (<>
    <circle cx={50} cy={50} r={30.5} fill="url(#wl-g-dark)" />
    {[[38, 40, 1.3], [58, 35, 1.1], [52, 58, 1.4], [42, 55, 1], [63, 50, 1.2]].map(([x, y, r], i) => (
      <circle key={i} cx={x} cy={y} r={r} fill="#F2F7FF" opacity=".9" />
    ))}
  </>);
  else inner = (<>{/* frost */}
    <circle cx={50} cy={50} r={30.5} fill="url(#wl-g-frost)" />
    <path d="M35 45 L50 50 L44 63 M50 50 L66 42 M50 50 L58 61" stroke="#F4FBFF" strokeWidth="1" opacity=".7" fill="none" />
  </>);
  return (
    <svg viewBox="0 0 100 100" width={size} height={size} aria-hidden="true">
      <defs>
        <radialGradient id="wl-g-dark" cx="50%" cy="46%"><stop offset="0%" stopColor="#0B0E13" /><stop offset="78%" stopColor="#161B23" /><stop offset="100%" stopColor="#232A35" /></radialGradient>
        <radialGradient id="wl-g-water" cx="46%" cy="42%"><stop offset="0%" stopColor="#1D7A8C" /><stop offset="70%" stopColor="#0F4A5C" /><stop offset="100%" stopColor="#0B3644" /></radialGradient>
        <radialGradient id="wl-g-rain" cx="48%" cy="45%"><stop offset="0%" stopColor="#2E96A8" /><stop offset="72%" stopColor="#15606F" /><stop offset="100%" stopColor="#0E4552" /></radialGradient>
        <radialGradient id="wl-g-frost" cx="46%" cy="42%"><stop offset="0%" stopColor="#CFEAF4" /><stop offset="75%" stopColor="#8FBCCD" /><stop offset="100%" stopColor="#6E9FB3" /></radialGradient>
      </defs>
      <circle cx={50} cy={50} r={46.5} fill={wet ? "#565E68" : "#63666E"} />
      {inner}
      <circle cx={50} cy={50} r={30.5} fill="none" stroke="#2E333C" strokeWidth="1.6" opacity=".7" />
      {rim}
    </svg>
  );
}

/* ── 우물 버튼 (탭바 중앙) ── */
export function WellButton({ theme = "light", cfg = WELL_DEFAULT, onOpen,
  reveal = false, variantOverride = null, hourOverride = null, headingOverride = null }) {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => { const t = setInterval(() => setNow(new Date()), 60000); return () => clearInterval(t); }, []);
  const [wx, setWx] = useState(null);
  useEffect(() => {
    let a = true;
    getWx().then((w) => { if (a) setWx(w); });
    const t = setInterval(() => getWx().then((w) => { if (a) setWx(w); }), 10 * 60e3);
    return () => { a = false; clearInterval(t); };
  }, []);
  const imgs = useWellImgs();
  const [heading, hdLive] = useHeading(!!cfg.fx.compass && headingOverride == null);
  const askedRef = useRef(false);

  const hour = hourOverride ?? now.getHours();
  const date = useMemo(() => {
    if (hourOverride == null) return now;
    const d = new Date(now); d.setHours(hourOverride, 30, 0, 0); return d;
  }, [now, hourOverride]);
  const variant = variantOverride || wellVariant(wx, hour);
  const band = timeBand(hour);
  const sun = useMemo(() => sunPos(date), [date]);
  const hd = headingOverride ?? (hdLive ? heading : 0);
  const sunny = !wx || (!wx.rainy && !wx.snowy && wx.cloudLv <= 4);
  const sh = cfg.fx.shadow && sunny ? shadowOf(sun, hd, cfg.btn.d) : null;

  const found = resolveWellImg(imgs, variant);
  const showImg = cfg.img.on || reveal;
  const d = cfg.btn.d;
  const imgD = Math.round(d * cfg.img.scale / 100);
  const btnBottom = `calc(var(--wt-h, 52px) - ${d - cfg.btn.dy}px)`;
  const sunDir = sh ? (((sun.az - hd) % 360) + 360) % 360 : null;

  const filters = [];
  const bf = bandFilter(band, variant);
  if (bf !== "none") filters.push(bf);
  if (sh) filters.push(`drop-shadow(${sh.dx}px ${sh.dy}px ${sh.blur}px rgba(15,20,30,${sh.alpha}))`);
  else if (band === "night") filters.push("drop-shadow(0 3px 9px rgba(130,160,255,.25))");
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
            {found ? <img src={imgs[found].url} alt="" draggable="false" />
              : <PlaceholderWell variant={variant} size={imgD} />}
            {sunDir != null && (
              <div className="wl-shade" style={{
                background: `linear-gradient(${Math.round((sunDir + 180) % 360)}deg, rgba(6,10,18,${(0.16 + 0.2 * (1 - Math.min(sun.el, 75) / 75)).toFixed(2)}) 0%, rgba(6,10,18,0) 58%)`,
              }} />
            )}
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
          <button type="button" onClick={() => go("#/solve/photo/mine")}>🗂 내 기록</button>
          <button type="button" onClick={() => go("#/solve/photo")}>📸 찍어서 배우기 홈</button>
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
.wl-btn .wl-dot { font-size: calc(var(--wl-d, 46px) * .44); line-height: 1; }
.wl-btn.ghost { background: none; border-color: transparent; color: transparent; }
.wl-btn:active { transform: translateX(-50%) scale(.96); }
.wl-img { position: absolute; left: 50%; z-index: 2; pointer-events: none; }
.wl-core { position: relative; width: 100%; height: 100%; animation: wl-breathe 7s ease-in-out infinite; }
.wl-core img, .wl-core svg { width: 100%; height: 100%; display: block; user-select: none; }
.wl-core img { object-fit: contain; }
.wl-shade { position: absolute; inset: 9%; border-radius: 50%; mix-blend-mode: multiply; }
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
