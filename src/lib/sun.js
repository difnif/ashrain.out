// 태양 위치 근사(NOAA/Spencer 간이식) — 우물 그림자용. 오차 ±1° 수준이면 충분하다.
// az: 방위각(도, 북=0 시계방향) · el: 고도(도, 지평선=0)
export function sunPos(date = new Date(), lat = 37.66, lon = 126.83) {
  const rad = Math.PI / 180;
  const start = Date.UTC(date.getUTCFullYear(), 0, 1);
  const doy = Math.floor((date.getTime() - start) / 86400000) + 1; // 1~366
  const minutesUTC = date.getUTCHours() * 60 + date.getUTCMinutes() + date.getUTCSeconds() / 60;
  const g = (2 * Math.PI / 365) * (doy - 1 + (minutesUTC / 60 - 12) / 24);
  // 균시차(분)
  const eot = 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g)
            - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g));
  // 태양 적위(라디안)
  const decl = 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g)
             - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g)
             - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g);
  const tst = minutesUTC + eot + 4 * lon;          // 진태양시(분, UTC 기준 경도 보정)
  const ha = (tst / 4 - 180) * rad;                // 시간각(정오=0)
  const phi = lat * rad;
  const sinEl = Math.sin(phi) * Math.sin(decl) + Math.cos(phi) * Math.cos(decl) * Math.cos(ha);
  const el = Math.asin(Math.max(-1, Math.min(1, sinEl)));
  // 방위각: 남=0·서=+ 관례의 atan2 → 북=0 시계방향으로 변환
  const az = Math.atan2(Math.sin(ha), Math.cos(ha) * Math.sin(phi) - Math.tan(decl) * Math.cos(phi));
  const azDeg = (((az / rad + 180) % 360) + 360) % 360;
  return { az: azDeg, el: el / rad };
}

/**
 * 그림자 렌더 값 — 해시계처럼: 해 반대 방향으로, 해가 낮을수록 길게. 그림자는 늘 짙다(사용자 확정 2026-09-26).
 * 우물을 "지름 unit, 높이 unit×WELL_H 인 원통"으로 보고, 땅에 떨어지는 그림자(원을 그림자 방향으로 끌어 늘인 캡슐)의
 * 늘어난 길이 len = 높이 / tan(고도). 날짜(계절)와 시각이 모두 고도에 들어가므로 여름 한낮은 짧고 겨울·아침저녁은 길다.
 * heading: 화면 위쪽이 향한 방위(나침반, 도). 기본 0 = "화면 위 = 북쪽" 고정.
 * unit: 그림자를 드리우는 우물(돌 테두리)의 화면 지름(px).
 * 반환: null(해가 진 뒤) 또는 { dir, len, dx, dy, blur, alpha }
 *   dir 화면 기준 그림자 방향(도, 위=0 시계방향) · len 늘어난 길이(px) · dx/dy 그림자 끝 쪽 벡터(px)
 *   blur 가장자리 반그림자(px, 길수록 조금 더 부드럽게) · alpha 짙기(0.62, 해가 지평선에 붙을 때만 살짝 옅게)
 */
export const WELL_H = 0.55;       // 우물 돌담 높이 / 지름 — 실제 우물(지름 1.2m·높이 0.65m 안팎) 비율
export const SHADOW_MAX = 2.4;    // 그림자 최대 길이 = 지름 × 이 값 (해 뜰 녘·질 녘에 화면을 뒤덮지 않게)

export function shadowOf(sun, heading = 0, unit = 46) {
  if (!sun || sun.el <= 0.5) return null;             // 지평선 아래·직전 — 해 그림자 없음
  const rad = Math.PI / 180;
  const el = Math.min(sun.el, 89);
  const dirDeg = (((sun.az + 180 - heading) % 360) + 360) % 360;   // 그림자 방위(화면 기준, 위=0 시계방향)
  const len = Math.min(unit * SHADOW_MAX, (unit * WELL_H) / Math.tan(Math.max(el, 2) * rad));
  const dir = dirDeg * rad;
  const r1 = (v) => Math.round(v * 10) / 10;
  const low = Math.max(0, (12 - el) / 11);            // 0(고도 12° 이상) ~ 1(지평선)
  return {
    dir: r1(dirDeg),
    len: r1(len),
    dx: r1(Math.sin(dir) * len),
    dy: r1(-Math.cos(dir) * len),                      // 화면 y 는 아래로 +
    blur: r1(0.6 + Math.min(len / unit, SHADOW_MAX) * 0.6),
    alpha: Math.round((0.62 - 0.2 * low) * 100) / 100,
  };
}
