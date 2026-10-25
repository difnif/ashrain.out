// ashrain.out — 교실 모니터 장면 목록 (pairs.js)
// 한 항목 = 초등·중등 짝 장면. 두 판은 같은 박자표(dur·구간)를 써서, 토글하면 같은 시각의 짝 장면으로 겹친다.
//   { key, dur, title: {e, m}, sub: {e, m}, render(mode, t, C) }
// 순서: 입체(3D)와 평면을 번갈아 — 쉬지 않고 돌아도 눈이 덜 지친다.
import blocks from "./scenes/blocks.jsx";
import circle from "./scenes/circle.jsx";
import leaf from "./scenes/leaf.jsx";
import nets from "./scenes/nets.jsx";
import cylinder from "./scenes/cylinder.jsx";
import sphere from "./scenes/sphere.jsx";
import tri3 from "./scenes/tri3.jsx";
import poly from "./scenes/poly.jsx";
import diag from "./scenes/diag.jsx";
import iso from "./scenes/iso.jsx";
import para from "./scenes/para.jsx";
import trap from "./scenes/trap.jsx";

export const PAIRS = [blocks, tri3, nets, circle, poly, cylinder, diag, leaf, iso, sphere, para, trap];
