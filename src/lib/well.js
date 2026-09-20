// 우물(하단 탭바 중앙 버튼) 순수 로직 — 연출 상태 결정·설정 정리.
// 렌더는 components/Well.jsx, 태양 위치는 lib/sun.js, 실황 분류는 lib/wx.js.
// 연출은 딱 3가지(사용자 확정): 맑음 = 해 그림자 · 흐림/비 = 그림자 없이 감광 · 밤 = 중앙 조명.
// 우물 그림은 기본 1장 — 번들(/brand/well/base.webp)이 기본, 관리자가 figures/well/base.* 업로드로 교체.

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

/**
 * 연출 상태 — 실황(wx: lib/wx.js pickWeather 결과 | null)과 시각으로 셋 중 하나.
 *  · "night" 밤(20시~6시): 중앙 조명
 *  · "dim"   흐리거나 비·눈: 그림자 없이 명도만 낮춤
 *  · "sun"   맑은 낮: 태양 각도 그림자
 */
export function wellMode(wx, hour) {
  if (hour >= 20 || hour < 6) return "night";
  if (wx && (wx.rainy || wx.snowy || wx.cloudLv >= 5)) return "dim";
  return "sun";
}
