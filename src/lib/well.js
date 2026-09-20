// 우물(하단 탭바 중앙 버튼) 순수 로직 — 상태 결정·설정 정리·이미지 폴백.
// 렌더는 components/Well.jsx, 태양 위치는 lib/sun.js, 실황 분류는 lib/wx.js.

/** 관리자 업로드 이미지 키(figures/well/<key>.*)와 표시 이름 */
export const WELL_VARIANTS = [
  ["water",   "맑은 물"],
  ["dark",    "깊은 어둠"],
  ["drizzle", "가랑비"],
  ["rain",    "폭우"],
  ["snow",    "눈"],
  ["frost",   "결빙"],
];

/** 해당 변주 이미지가 없을 때 대신 쓸 순서 */
export const WELL_FALLBACK = {
  water:   ["dark"],
  dark:    ["water"],
  drizzle: ["rain", "water", "dark"],
  rain:    ["drizzle", "water", "dark"],
  snow:    ["frost", "dark", "water"],
  frost:   ["snow", "dark", "water"],
};

/** 우물이 여는 카메라 기능들 (탭하면 바로 실행) */
export const WELL_FEATURES = [
  ["📖", "문장 이해하기", "문제를 찍으면 단서에 형광펜", "#/solve/photo/read"],
  ["✍️", "표시 연습", "어디에 표시할지 차례대로 보여줘요", "#/solve/photo/mark"],
  ["📝", "서술형 채점", "답안까지 찍으면 채점·첨삭", "#/solve/photo/essay"],
  ["🔍", "풀이과정 검사", "페이지를 찍어 풀이 습관 진단", "#/solve/photo/check"],
  ["🖨️", "사진 채점", "답안 카드를 찍어 자동 채점", "#/solve/omr"],
  ["🗝️", "사진 힌트", "막힌 문제, 답 대신 첫걸음만", "#/learn/hint"],
];

/** 기본 설정 — app_settings.well_ui 로 관리자가 덮어쓴다 */
export const WELL_DEFAULT = {
  bar: { h: 52, tab: 100 },              // 탭바 안쪽 높이(px) · 탭 크기(%)
  btn: { d: 46, dy: 10 },                // 우물 자리 지름(px) · 위로 튀어나옴(px)
  img: { scale: 200, dy: 0, on: true },  // 이미지 지름 = d×scale% · 세로 미세조정(px) · 이미지 표시
  fx:  { shadow: true, compass: true },  // 해 그림자 · 나침반 연동
};

const num = (v, def, min, max) => {
  const n = Number(v);
  return Number.isFinite(n) ? Math.min(max, Math.max(min, n)) : def;
};
const bool = (v, def) => (typeof v === "boolean" ? v : def);

/** 저장된 JSON(문자열/객체)을 기본값 위에 얹고 범위를 죈다 — 깨진 값은 조용히 기본값 */
export function clampWellCfg(raw) {
  let o = raw;
  if (typeof raw === "string") { try { o = JSON.parse(raw); } catch { o = null; } }
  if (!o || typeof o !== "object") o = {};
  const d = WELL_DEFAULT;
  return {
    bar: { h: num(o.bar?.h, d.bar.h, 40, 80), tab: num(o.bar?.tab, d.bar.tab, 70, 130) },
    btn: { d: num(o.btn?.d, d.btn.d, 32, 72), dy: num(o.btn?.dy, d.btn.dy, 0, 28) },
    img: {
      scale: num(o.img?.scale, d.img.scale, 100, 340),
      dy: num(o.img?.dy, d.img.dy, -40, 40),
      on: bool(o.img?.on, d.img.on),
    },
    fx: { shadow: bool(o.fx?.shadow, d.fx.shadow), compass: bool(o.fx?.compass, d.fx.compass) },
  };
}

/** 시간대 이름 — 색 필터에 쓴다 */
export function timeBand(h) {
  return h < 6 ? "dawn" : h < 11 ? "morn" : h < 17 ? "day" : h < 20 ? "dusk" : "night";
}

/**
 * 실황(wx: lib/wx.js pickWeather 결과 | null)과 시각으로 우물 상태를 고른다.
 * 눈 > 비 > 결빙 > (밤이면 어둠 / 낮이면 물).
 */
export function wellVariant(wx, hour) {
  if (wx?.snowy) return "snow";
  if (wx?.rainy) return (wx.p || 0) >= 5 || +wx.base[1] >= 4 ? "rain" : "drizzle";
  if (wx && wx.t != null && wx.t <= 0) return "frost";
  const night = hour >= 20 || hour < 6;
  return night ? "dark" : "water";
}

/** 이미지 맵(map[key] = url)에서 변주에 맞는 키를 폴백 순서로 찾는다 — 없으면 null(자리그림) */
export function resolveWellImg(map, variant) {
  if (!map) return null;
  if (map[variant]) return variant;
  for (const k of WELL_FALLBACK[variant] || []) if (map[k]) return k;
  return null;
}

/** 시간대별 색 보정(CSS filter 문자열) — 이미지·자리그림 공통 */
export function bandFilter(band, variant) {
  const dim = variant === "dark" ? "" : " brightness(.72) saturate(.8)";
  switch (band) {
    case "dawn":  return "brightness(.8) saturate(.75) hue-rotate(-8deg)";
    case "morn":  return "brightness(1.04) saturate(1.02)";
    case "day":   return "none";
    case "dusk":  return "brightness(.94) saturate(1.1) sepia(.18) hue-rotate(-14deg)";
    case "night": return ("brightness(1)" + dim).trim();
    default:      return "none";
  }
}
