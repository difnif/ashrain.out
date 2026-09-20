// 우물 로직 테스트 — 태양 위치·그림자·상태 결정·설정 죄기·이미지 폴백
// 실행: node tests/well.test.mjs
import { sunPos, shadowOf } from "../src/lib/sun.js";
import { clampWellCfg, wellVariant, timeBand, resolveWellImg, WELL_DEFAULT } from "../src/lib/well.js";
import { pickWeather } from "../src/lib/wx.js";

let n = 0, ok = 0;
const t = (name, cond) => { n++; if (cond) ok++; else console.log(" ✗ " + name); };
const kst = (m, d, h, min = 0) => new Date(Date.UTC(2026, m - 1, d, h - 9, min)); // KST → UTC

// ── 태양 위치 — 고양시(37.66N) 상식 점검 ──
const noon = sunPos(kst(9, 20, 12, 40));
t("추분 무렵 남중 고도 ~52°", noon.el > 46 && noon.el < 58);
t("남중 방위는 남쪽", noon.az > 160 && noon.az < 200);
const morn = sunPos(kst(9, 20, 8, 0));
t("아침 해는 동쪽 하늘 낮게", morn.az > 80 && morn.az < 140 && morn.el > 5 && morn.el < 40);
const eve = sunPos(kst(9, 20, 18, 0));
t("저녁 해는 서쪽 하늘", eve.az > 240 && eve.az < 290);
t("자정엔 해가 지평선 아래", sunPos(kst(9, 20, 0, 0)).el < 0);
t("여름 남중이 겨울보다 훨씬 높다", sunPos(kst(6, 21, 12, 40)).el > sunPos(kst(12, 21, 12, 40)).el + 30);

// ── 그림자 ──
t("해가 지면 해 그림자 없음", shadowOf({ az: 0, el: -10 }) === null && shadowOf(sunPos(kst(9, 20, 2, 0))) === null);
const shM = shadowOf(morn, 0, 46);
t("아침 그림자는 서쪽(화면 왼쪽)으로", !!shM && shM.dx < 0);
const away = (sh, sun) => sh.dx * Math.sin(sun.az * Math.PI / 180) + sh.dy * -Math.cos(sun.az * Math.PI / 180);
t("그림자는 항상 해 반대쪽", away(shM, morn) < 0 && away(shadowOf(eve, 0, 46), eve) < 0);
const shN = shadowOf(noon, 0, 46), shE = shadowOf(eve, 0, 46);
t("해가 낮을수록 그림자가 길고 흐리다", Math.hypot(shE.dx, shE.dy) > Math.hypot(shN.dx, shN.dy) && shE.blur > shN.blur);
const shH = shadowOf(noon, noon.az, 46);
t("나침반 보정 — 화면이 해를 향하면 그림자는 화면 아래로", shH.dy > 0 && Math.abs(shH.dx) < Math.abs(shH.dy));

// ── 상태 결정 (lib/wx.js 분류 결과를 그대로 먹는다) ──
const W = (c) => pickWeather(c);
t("눈 → snow", wellVariant(W({ temperature_2m: -1, precipitation: 2, weather_code: 73, cloud_cover: 90, wind_speed_10m: 2 }), 14) === "snow");
t("장대비 → rain", wellVariant(W({ temperature_2m: 18, precipitation: 8, weather_code: 65, cloud_cover: 95, wind_speed_10m: 3 }), 14) === "rain");
t("가랑비 → drizzle", wellVariant(W({ temperature_2m: 18, precipitation: 0.8, weather_code: 51, cloud_cover: 80, wind_speed_10m: 2 }), 14) === "drizzle");
t("영하 맑음 → frost", wellVariant(W({ temperature_2m: -4, precipitation: 0, weather_code: 0, cloud_cover: 10, wind_speed_10m: 1 }), 14) === "frost");
t("맑은 낮 → water", wellVariant(W({ temperature_2m: 21, precipitation: 0, weather_code: 1, cloud_cover: 20, wind_speed_10m: 2 }), 14) === "water");
t("맑은 밤 → dark", wellVariant(W({ temperature_2m: 15, precipitation: 0, weather_code: 0, cloud_cover: 5, wind_speed_10m: 1 }), 23) === "dark");
t("밤중 비 → rain(밤 보정은 필터가)", wellVariant(W({ temperature_2m: 15, precipitation: 6, weather_code: 63, cloud_cover: 95, wind_speed_10m: 3 }), 23) === "rain");
t("실황 없으면 시간만으로", wellVariant(null, 3) === "dark" && wellVariant(null, 10) === "water");

// ── 시간대 ──
t("시간대 구분", timeBand(4) === "dawn" && timeBand(9) === "morn" && timeBand(13) === "day" && timeBand(18) === "dusk" && timeBand(22) === "night");

// ── 설정 죄기 ──
t("빈 값은 기본값 그대로", JSON.stringify(clampWellCfg(null)) === JSON.stringify(WELL_DEFAULT));
const c2 = clampWellCfg('{"btn":{"d":500,"dy":-9},"img":{"scale":"abc","on":false},"fx":{"shadow":false}}');
t("범위 밖·엉뚱한 값은 죈다", c2.btn.d === 72 && c2.btn.dy === 0 && c2.img.scale === WELL_DEFAULT.img.scale
  && c2.img.on === false && c2.fx.shadow === false && c2.fx.compass === true && c2.bar.h === WELL_DEFAULT.bar.h);
t("깨진 JSON은 기본값", JSON.stringify(clampWellCfg("{oops")) === JSON.stringify(WELL_DEFAULT));
t("객체로 줘도 된다", clampWellCfg({ bar: { h: 60 } }).bar.h === 60);

// ── 이미지 폴백 ──
const m = { rain: 1, dark: 1 };
t("폴백 순서", resolveWellImg(m, "drizzle") === "rain" && resolveWellImg(m, "water") === "dark"
  && resolveWellImg({}, "water") === null && resolveWellImg(m, "rain") === "rain" && resolveWellImg(null, "rain") === null);

console.log(`${ok}/${n} passed`);
if (ok !== n) process.exit(1);
