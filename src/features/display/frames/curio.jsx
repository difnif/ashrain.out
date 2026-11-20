// ashrain.out — 수학 호기심 액자 묶음 등록 (frames/curio.jsx)
// 교실 모니터 액자 목록(frames/index.js)에 그림 액자로 더한 열여섯 — 학생앱 공부하기 › 시청각 학습 › 수학 호기심에 저절로 들어간다(lib/av.js).
//   soccerfn 축구로 보는 일차함수 · hoopfn 농구로 보는 정비례 · batfn 야구로 보는 정비례
//   badminton · tennis · tabletennis · volleyball · jokgu · sepak — 네트 운동(친 곳 → 떨어진 곳, 네트를 지난 자리 = y절편, frames/netfn.jsx)
//   golf 골프로 보는 이차함수(포물선) · cue 당구로 보는 대칭(빈쿠션) · bowl 볼링으로 보는 일차함수와 점수 계산
//   pouch 주머니 공 꺼내기 · lexi 알파벳 카드 사전식 배열 · lineup 일렬로 세우기 · crowd 북적북적 학년별 뽑기
// 모두 「풀이: 상세 | 최소화」를 고를 수 있다(D 키) — 최소화는 설명 판을 접고 그림을 크게, 핵심 칩 하나만.
// AdminDisplay.jsx 의 FrameStage(LABS)와 액자 목록 그림이 여기서 key 로 고른다. 큰 자료(경기 · 사전)는 액자를 열 때 늦게 들여온다.
import { SoccerFnFrame, SoccerFnThumb } from "./soccerfn.jsx";
import { HoopFnFrame, HoopFnThumb } from "./hoopfn.jsx";
import { BatFnFrame, BatFnThumb } from "./batfn.jsx";
import { PouchFrame, PouchThumb } from "./pouch.jsx";
import { LexiFrame, LexiThumb } from "./lexi.jsx";
import { LineupFrame, LineupThumb } from "./lineup.jsx";
import { CrowdFrame, CrowdThumb } from "./crowd.jsx";
import { NetFnFrame, NetFnThumb } from "./netfn.jsx";
import { GolfFrame, GolfThumb } from "./golffn.jsx";
import { CueFrame, CueThumb } from "./cuefn.jsx";
import { BowlFrame, BowlThumb } from "./bowlfn.jsx";

/** 네트 운동 여섯은 같은 액자에 종목만 다르게 */
const NET_SPORTS = ["badminton", "tennis", "tabletennis", "volleyball", "jokgu", "sepak"];
const netFrame = (sport) => { const F = (props) => <NetFnFrame sport={sport} {...props} />; F.displayName = `NetFn_${sport}`; return F; };
const netThumb = (sport) => { const F = (props) => <NetFnThumb sport={sport} {...props} />; F.displayName = `NetFnThumb_${sport}`; return F; };

export const CURIO_LABS = {
  soccerfn: SoccerFnFrame, hoopfn: HoopFnFrame, batfn: BatFnFrame,
  ...Object.fromEntries(NET_SPORTS.map((s) => [s, netFrame(s)])),
  golf: GolfFrame, cue: CueFrame, bowl: BowlFrame,
  pouch: PouchFrame, lexi: LexiFrame, lineup: LineupFrame, crowd: CrowdFrame,
};
const THUMBS = {
  soccerfn: SoccerFnThumb, hoopfn: HoopFnThumb, batfn: BatFnThumb,
  ...Object.fromEntries(NET_SPORTS.map((s) => [s, netThumb(s)])),
  golf: GolfThumb, cue: CueThumb, bowl: BowlThumb,
  pouch: PouchThumb, lexi: LexiThumb, lineup: LineupThumb, crowd: CrowdThumb,
};
/** 액자 목록의 작은 그림(없는 key 면 아무것도 그리지 않는다) */
export function CurioThumb({ fkey, C, mode }) {
  const T = THUMBS[fkey];
  return T ? <T C={C} mode={mode === "e" ? "e" : "m"} /> : null;
}
export const isCurio = (key) => key in CURIO_LABS;
