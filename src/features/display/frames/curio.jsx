// ashrain.out — 수학 호기심 액자 묶음 등록 (frames/curio.jsx)
// 교실 모니터 액자 목록(frames/index.js)에 그림 액자로 더한 일곱 — 학생앱 공부하기 › 시청각 학습 › 수학 호기심에 저절로 들어간다(lib/av.js).
//   soccerfn 축구로 보는 일차함수 · hoopfn 농구로 보는 정비례 · batfn 야구로 보는 정비례
//   pouch 주머니 공 꺼내기 · lexi 알파벳 카드 사전식 배열 · lineup 일렬로 세우기 · crowd 북적북적 학년별 뽑기
// AdminDisplay.jsx 의 FrameStage(LABS)와 액자 목록 그림이 여기서 key 로 고른다. 큰 자료(경기 · 사전)는 액자를 열 때 늦게 들여온다.
import { SoccerFnFrame, SoccerFnThumb } from "./soccerfn.jsx";
import { HoopFnFrame, HoopFnThumb } from "./hoopfn.jsx";
import { BatFnFrame, BatFnThumb } from "./batfn.jsx";
import { PouchFrame, PouchThumb } from "./pouch.jsx";
import { LexiFrame, LexiThumb } from "./lexi.jsx";
import { LineupFrame, LineupThumb } from "./lineup.jsx";
import { CrowdFrame, CrowdThumb } from "./crowd.jsx";

export const CURIO_LABS = {
  soccerfn: SoccerFnFrame, hoopfn: HoopFnFrame, batfn: BatFnFrame,
  pouch: PouchFrame, lexi: LexiFrame, lineup: LineupFrame, crowd: CrowdFrame,
};
const THUMBS = {
  soccerfn: SoccerFnThumb, hoopfn: HoopFnThumb, batfn: BatFnThumb,
  pouch: PouchThumb, lexi: LexiThumb, lineup: LineupThumb, crowd: CrowdThumb,
};
/** 액자 목록의 작은 그림(없는 key 면 아무것도 그리지 않는다) */
export function CurioThumb({ fkey, C, mode }) {
  const T = THUMBS[fkey];
  return T ? <T C={C} mode={mode === "e" ? "e" : "m"} /> : null;
}
export const isCurio = (key) => key in CURIO_LABS;
