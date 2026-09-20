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
 * 그림자 렌더 값 — 해 반대 방향으로, 해가 낮을수록 길고 흐리고 옅게.
 * heading: 화면 위쪽이 향한 방위(나침반, 도). 기본 0 = "화면 위 = 북쪽" 고정.
 * unit: 우물 지름(px) — 길이를 이에 비례시킨다.
 * 반환: null(해가 진 뒤) 또는 { dx, dy, blur, alpha }
 */
export function shadowOf(sun, heading = 0, unit = 46) {
  if (!sun || sun.el <= 0.5) return null;             // 지평선 아래·직전 — 해 그림자 없음
  const rad = Math.PI / 180;
  const el = Math.min(sun.el, 88);
  // 그림자 방위 = 해 방위 + 180, 화면 기준으로 heading 만큼 되돌린다
  const dir = (sun.az + 180 - heading) * rad;         // 북=0 시계방향
  const len = Math.min(unit * 1.15, (unit * 0.34) / Math.tan(Math.max(el, 8) * rad));
  const dx = Math.sin(dir) * len;
  const dy = -Math.cos(dir) * len;                    // 화면 y 는 아래로 +
  const soft = 1 - Math.min(el / 60, 1);              // 낮은 해일수록 부드럽게
  return {
    dx: Math.round(dx * 10) / 10,
    dy: Math.round(dy * 10) / 10,
    blur: Math.round((3 + soft * 9) * 10) / 10,
    alpha: Math.round((0.38 - soft * 0.16) * 100) / 100,
  };
}
