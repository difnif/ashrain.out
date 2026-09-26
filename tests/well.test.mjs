// 우물 로직 테스트 — 태양 위치·그림자·연출 상태(3가지)·설정 죄기
// 실행: node tests/well.test.mjs
import { sunPos, shadowOf } from "../src/lib/sun.js";
import { clampWellCfg, wellMode, WELL_DEFAULT, WELL_FEATURES } from "../src/lib/well.js";
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

// ── 해시계 그림자 (2026-09-26 사용자 확정: 확실히 그림자로 보이게 매우 짙게, 길이 변화 반영) ──
t("낮 그림자는 짙다(α ≥ 0.6)", shN.alpha >= 0.6 && shM.alpha >= 0.6);
t("해가 지평선에 붙어도 그림자는 여전히 보인다(α ≥ 0.4)", shadowOf({ az: 270, el: 1 }, 0, 88).alpha >= 0.4);
t("가장자리는 살짝만 부드럽게(blur ≤ 2.2px)", [shN, shM, shE].every((x) => x.blur > 0 && x.blur <= 2.2));
t("길이 = 높이/tan(고도) — 고도 45°면 지름×0.55", Math.abs(shadowOf({ az: 180, el: 45 }, 0, 100).len - 55) < 0.2);
t("길이 상한 — 지름×2.4", shadowOf({ az: 90, el: 1 }, 0, 100).len === 240);
const lenAt = (m, d, h, mi) => shadowOf(sunPos(kst(m, d, h, mi)), 0, 100).len;
t("계절 반영 — 겨울 한낮 그림자가 여름 한낮보다 훨씬 길다", lenAt(12, 21, 12, 30) > lenAt(6, 21, 12, 30) * 4);
t("시각 반영 — 아침 8시가 한낮보다 길다", lenAt(9, 20, 8, 0) > lenAt(9, 20, 12, 40) * 2);
t("한낮 그림자는 화면 위(북)로 — dir ≈ 0", (() => { const x = shadowOf(noon, 0, 100).dir; return x < 20 || x > 340; })());
t("dir·len 과 dx·dy 가 서로 맞는다", Math.abs(Math.hypot(shM.dx, shM.dy) - shM.len) < 0.3);

// ── 연출 상태 3가지 (사용자 확정: 맑음 그림자 / 흐림·비 감광 / 밤 조명) ──
const W = (c) => pickWeather(c);
const CLEAR = W({ temperature_2m: 21, precipitation: 0, weather_code: 1, cloud_cover: 20, wind_speed_10m: 2 });
const RAIN = W({ temperature_2m: 18, precipitation: 8, weather_code: 65, cloud_cover: 95, wind_speed_10m: 3 });
const SNOW = W({ temperature_2m: -1, precipitation: 2, weather_code: 73, cloud_cover: 90, wind_speed_10m: 2 });
const OVERCAST = W({ temperature_2m: 20, precipitation: 0, weather_code: 3, cloud_cover: 92, wind_speed_10m: 2 });
t("맑은 낮 → sun", wellMode(CLEAR, 14) === "sun");
t("비 → dim", wellMode(RAIN, 14) === "dim");
t("눈 → dim", wellMode(SNOW, 14) === "dim");
t("잔뜩 흐림 → dim", wellMode(OVERCAST, 14) === "dim");
t("밤은 날씨와 무관하게 night", wellMode(CLEAR, 23) === "night" && wellMode(RAIN, 3) === "night" && wellMode(null, 21) === "night");
t("실황 없으면 시간만으로", wellMode(null, 10) === "sun" && wellMode(null, 5) === "night");
t("경계 — 6시는 낮, 20시는 밤", wellMode(CLEAR, 6) === "sun" && wellMode(CLEAR, 20) === "night");

// ── 설정 죄기 ──
t("빈 값은 기본값 그대로", JSON.stringify(clampWellCfg(null)) === JSON.stringify(WELL_DEFAULT));
const c2 = clampWellCfg('{"btn":{"d":500,"dy":-9},"img":{"scale":"abc","on":false},"fx":{"shadow":false}}');
t("범위 밖·엉뚱한 값은 죈다", c2.btn.d === 72 && c2.btn.dy === 0 && c2.img.scale === WELL_DEFAULT.img.scale
  && c2.img.on === false && c2.fx.shadow === false && c2.fx.compass === true && c2.bar.h === WELL_DEFAULT.bar.h);
t("깨진 JSON은 기본값", JSON.stringify(clampWellCfg("{oops")) === JSON.stringify(WELL_DEFAULT));
t("객체로 줘도 된다", clampWellCfg({ bar: { h: 60 } }).bar.h === 60);

// ── 런처 목록 ──
t("사진 도구 5종(찰칵 채점은 개발중 제외)", WELL_FEATURES.length === 5 && WELL_FEATURES.every(([, , , to]) => to.startsWith("#/"))
  && !WELL_FEATURES.some(([, , , to]) => to.includes("omr")));

console.log(`${ok}/${n} passed`);
if (ok !== n) process.exit(1);
