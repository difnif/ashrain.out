// ashrain.out — 교실 모니터 장면 목록 (pairs.js)
// 한 항목 = 초등·중등 짝 장면. 두 판은 같은 박자표(dur·구간)를 써서, 토글하면 같은 시각의 짝 장면으로 겹친다.
//   { key, group, dur, title: {e, m}, sub: {e, m}, render(mode, t, C) }
// 묶음(group): geo = 도형·측정 · data = 자료와 가능성 ↔ 경우의 수와 확률. 목록에서 묶음만 골라 돌릴 수 있다.
// 순서: 도형 묶음은 입체(3D)와 평면을 번갈아 — 쉬지 않고 돌아도 눈이 덜 지친다.
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
import sort from "./scenes/sort.jsx";
import table from "./scenes/table.jsx";
import numcards from "./scenes/numcards.jsx";
import freq from "./scenes/freq.jsx";
import chance from "./scenes/chance.jsx";

const GEO = [blocks, tri3, nets, circle, poly, cylinder, diag, leaf, iso, sphere, para, trap];
const DATA = [sort, table, numcards, freq, chance];

export const GROUPS = [
  { key: "all", label: "전체" },
  { key: "geo", label: "도형" },
  { key: "data", label: "경우의 수·확률" },
];
export const PAIRS = [...GEO.map((p) => ({ ...p, group: "geo" })), ...DATA.map((p) => ({ ...p, group: "data" }))];
