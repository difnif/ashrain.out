// ashrain.out — 교실 모니터 장면 목록 (pairs.js)
// 한 항목 = 초등·중등 짝 장면. 두 판은 같은 박자표(dur·구간)를 써서, 토글하면 같은 시각의 짝 장면으로 겹친다.
//   { key, group, dur, title: {e, m}, sub: {e, m}, render(mode, t, C, P), controls? }
//   dur 은 수(ms) 또는 설정을 받는 함수. controls 가 있으면 화면에 설정 칩이 뜬다(params.js).
// 묶음(group): geo = 도형·측정 · data = 자료와 가능성 ↔ 경우의 수와 확률 · soccer = 축구 · essay = 서술형 ·
//   guess = 몬티홀·찍기 · branch = 갈림길·구슬 · galton = 정규분포(구슬 낙하). 목록에서 묶음만 골라 돌릴 수 있다.
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
import socCorner from "./scenes/soc-corner.jsx";
import socSetpiece from "./scenes/soc-setpiece.jsx";
import socThrough from "./scenes/soc-through.jsx";
import socTriangle from "./scenes/soc-triangle.jsx";
import socCounter from "./scenes/soc-counter.jsx";
import socXg from "./scenes/soc-xg.jsx";
import essRails from "./scenes/ess-rails.jsx";
import essWrongway from "./scenes/ess-wrongway.jsx";
import essClub from "./scenes/ess-club.jsx";
import essRps from "./scenes/ess-rps.jsx";
import essSign from "./scenes/ess-sign.jsx";
import essShirt from "./scenes/ess-shirt.jsx";
import monty from "./scenes/monty.jsx";
import pick5 from "./scenes/pick5.jsx";
import linked from "./scenes/linked.jsx";
import fork from "./scenes/fork.jsx";
import forkn from "./scenes/forkn.jsx";
import bump from "./scenes/bump.jsx";
import galton from "./scenes/galton.jsx";

const GEO = [blocks, tri3, nets, circle, poly, cylinder, diag, leaf, iso, sphere, para, trap];
const DATA = [sort, table, numcards, freq, chance];
const SOCCER = [socCorner, socSetpiece, socThrough, socTriangle, socCounter, socXg];
const ESSAY = [essRails, essWrongway, essClub, essRps, essSign, essShirt];
const GUESS = [monty, pick5, linked];
const BRANCH = [fork, forkn, bump];
const GALTON = [galton];

export const GROUPS = [
  { key: "all", label: "전체" },
  { key: "geo", label: "도형" },
  { key: "data", label: "경우의 수·확률" },
  { key: "soccer", label: "축구" },
  { key: "essay", label: "서술형" },
  { key: "guess", label: "몬티홀·찍기" },
  { key: "branch", label: "갈림길·구슬" },
  { key: "galton", label: "정규분포" },
];
const tagged = (list, group) => list.map((p) => ({ ...p, group }));
export const PAIRS = [
  ...tagged(GEO, "geo"), ...tagged(DATA, "data"), ...tagged(SOCCER, "soccer"), ...tagged(ESSAY, "essay"),
  ...tagged(GUESS, "guess"), ...tagged(BRANCH, "branch"), ...tagged(GALTON, "galton"),
];
