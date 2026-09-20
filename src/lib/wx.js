// 실황 날씨 공용 모듈 — 대시보드 히어로와 우물(하단 탭바)이 같은 신호를 쓴다.
// Open-Meteo 현재값 → pickWeather 로 단계 분류. 10분 캐시로 화면당 중복 요청을 막는다.
const WX_URL = "https://api.open-meteo.com/v1/forecast?latitude=37.66&longitude=126.83&current=temperature_2m,precipitation,weather_code,cloud_cover,wind_speed_10m";
const TTL = 10 * 60 * 1000;

/** Open-Meteo current → 장면 단계 (HomeDash 히어로와 동일 규칙) */
export function pickWeather(c) {
  const t = c.temperature_2m, p = c.precipitation || 0, code = c.weather_code,
        cc = c.cloud_cover ?? 0, ws = c.wind_speed_10m || 0;
  const snowy = [71, 73, 75, 77, 85, 86].includes(code);
  const rainy = !snowy && ([51,53,55,56,57,61,63,65,66,67,80,81,82,95,96,99].includes(code) || p > 0);
  let base;
  if (snowy)      base = "s" + (p >= 7 ? 6 : p >= 5 ? 5 : p >= 3 ? 4 : p >= 1.5 ? 3 : p >= 0.5 ? 2 : 1);
  else if (rainy) base = "r" + (p >= 20 ? 6 : p >= 10 ? 5 : p >= 5 ? 4 : p >= 2 ? 3 : p >= 0.5 ? 2 : 1);
  else            base = "c" + Math.min(6, Math.max(1, Math.round(cc / 20) + 1));
  const over = [];
  if (t <= 5)       over.push("f" + (t <= -15 ? 6 : t <= -12 ? 5 : t <= -8 ? 4 : t <= -3 ? 3 : t <= 0 ? 2 : 1));
  else if (t >= 26) over.push("h" + (t >= 35 ? 6 : t >= 33 ? 5 : t >= 31 ? 4 : t >= 29 ? 3 : t >= 27.5 ? 2 : 1));
  if (ws >= 4)      over.push("w" + (ws >= 21 ? 6 : ws >= 14 ? 5 : ws >= 11 ? 4 : ws >= 8 ? 3 : ws >= 6 ? 2 : 1));
  return { base, over, t, p, snowy, rainy, cloudLv: +(base[0] === "c" ? base[1] : 6) };
}

let cache = null; // { at, wx }
let inflight = null;

/** 분류된 실황(wx)을 캐시와 함께 — 실패하면 null (호출부는 시간 기반으로 폴백) */
export function getWx() {
  const now = Date.now();
  if (cache && now - cache.at < TTL) return Promise.resolve(cache.wx);
  if (inflight) return inflight;
  inflight = fetch(WX_URL)
    .then((r) => r.json())
    .then((j) => {
      const wx = j?.current ? pickWeather(j.current) : null;
      if (wx) cache = { at: Date.now(), wx };
      return wx;
    })
    .catch(() => null)
    .finally(() => { inflight = null; });
  return inflight;
}

/** 테스트·미리보기용 캐시 주입 */
export function _setWxCache(wx) { cache = wx ? { at: Date.now(), wx } : null; }
