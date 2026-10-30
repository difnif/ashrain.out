// ashrain.out — 교실 모니터 「3D 축구」 대본 목록 (sim3d/index.js)
// 「숫자로 읽는 축구」 여섯 장면의 3D 판. 장면 key → { dur, world(t), overlay(mode, t, C, P, W) }.
// stories.js 가 축구 장면에 sim3d 로 붙인다 — 재생기(frames/player.jsx)는 sim3d 가 있는 장면에만 「2D | 3D」 토글을 띄운다.
// 이 목록은 three.js 를 쓰지 않는다(그리기는 Stage3D.jsx · engine.js 가 3D 를 켤 때만 늦게 불러온다).
import corner from "./scenes/corner.jsx";
import setpiece from "./scenes/setpiece.jsx";
import through from "./scenes/through.jsx";
import triangle from "./scenes/triangle.jsx";
import counter from "./scenes/counter.jsx";
import xg from "./scenes/xg.jsx";

export const SIM3D = Object.fromEntries([corner, setpiece, through, triangle, counter, xg].map((s) => [s.key, s]));
