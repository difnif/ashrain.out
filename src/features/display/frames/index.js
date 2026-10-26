// ashrain.out — 교실 모니터 「액자」 목록 (frames/index.js)
// 액자 = 수업 장면(초등↔중등 짝)과 따로, 오래 켜 두는 그림. 모니터 오른쪽 위 액자 단추 → 목록 → 고르면 그 액자가 돈다.
// 하나 더 넣으려면: 여기에 { key, title, desc } 를 더하고 AdminDisplay.jsx 의 FrameStage 에서 key 로 그릴 것을 고른다.
export const FRAMES = [
  { key: "hanoi", title: "하노이의 탑", desc: "원판을 하나씩 옮겨 탑을 통째로 옮겨요. 다 옮기면 거꾸로 — 쉬지 않고 돌아요." },
];
export const frameOf = (key) => FRAMES.find((f) => f.key === key) || null;
