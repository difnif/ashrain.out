// ashrain.out — 교실 모니터 「액자」: 장면 묶음 (frames/story.jsx)
// 축구·서술형처럼 여러 단원을 섞는 융합 장면을 하노이의 탑처럼 액자로 켜 둔다(목록: ../stories.js).
// 수업 장면과 같은 초등↔중등 짝 장면을 차례로 끝없이 돌리고, 오른쪽 위 학년 토글을 누르면 같은 순간의 짝 장면으로 겹쳐 넘어간다.
// 재생기(StoryPlayer · loadStory)는 frames/player.jsx — 실험 액자의 「풀이 보기」 · 컨셉 문제 해설 영상도 같은 재생기를 쓴다.
import { memo } from "react";
import { paramsOf } from "../params.js";
import { STORIES } from "../stories.js";
import { StoryPlayer, loadStory } from "./player.jsx";

export { StoryPlayer, loadStory };

/** 장면 묶음 액자(축구 · 서술형) */
export function StoryFrame({ fkey, ...rest }) {
  const story = STORIES[fkey];
  return <StoryPlayer list={story.scenes} lsKey={`ash.display.story.${fkey}`} label={story.label} {...rest} />;
}

/** 액자 목록의 작은 그림 — 묶음의 대표 장면 한 순간 */
export const StoryThumb = memo(function StoryThumb({ fkey, C, mode = "e" }) {
  const s = STORIES[fkey];
  if (!s) return null;
  const p = s.scenes[s.thumb.i];
  return <g>{p.render(mode, s.thumb.t, C, paramsOf(p, null))}</g>;
});
