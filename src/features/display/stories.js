// ashrain.out — 교실 모니터 「장면 묶음 액자」 목록 (stories.js)
// 교육과정의 한 단원에 딱 맞기보다 여러 단원을 섞어 쓰는 융합 장면은 수업 장면 순환(pairs.js)에 넣지 않고,
// 하노이의 탑처럼 액자로 따로 켜 둔다. 장면 형식은 수업 장면과 같다 — { key, dur, title:{e,m}, sub:{e,m}, render(mode, t, C, P), controls? }.
//   soccer = 숫자로 읽는 축구(실제 경기 장면 · 피타고라스 · 교점 · 상대도수 · 여사건) — 3D 판이 붙는다(sim3d)
//   essay  = 서술형 이야기(경로 · 게임의 규칙 · 축제 서술형)
// thumb: 액자 목록에 작게 보여 줄 장면 번호와 시각(ms)
// EXPLAIN: 실험 액자(몬티홀 · 갈림길과 구슬 · 구슬 낙하 실험)의 「풀이 보기」에서 차례로 돌릴 설명 장면.
//   실험 액자는 직접 해 보는 것이 먼저고, 이 장면들은 풀이를 보고 싶을 때만 튼다(frames/xkit.jsx 의 LabShell).
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
import { SIM3D } from "./sim3d/index.js";

// 축구 여섯 장면에는 3D 판(sim3d/index.js)을 붙인다 — 재생기가 「2D | 3D」 토글을 띄운다
export const SOCCER = [socCorner, socSetpiece, socThrough, socTriangle, socCounter, socXg].map((p) => (SIM3D[p.key] ? { ...p, sim3d: SIM3D[p.key] } : p));
export const ESSAY = [essRails, essWrongway, essClub, essRps, essSign, essShirt];

export const STORIES = {
  soccer: { label: "축구", scenes: SOCCER, thumb: { i: 0, t: 28000 } },
  essay: { label: "서술형", scenes: ESSAY, thumb: { i: 0, t: 19500 } },
};

export const EXPLAIN = {
  monty: [monty, pick5, linked],
  branch: [fork, forkn, bump],
  galton: [galton],
};
