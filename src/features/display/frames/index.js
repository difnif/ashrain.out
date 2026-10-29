// ashrain.out — 교실 모니터 「액자」 목록 (frames/index.js)
// 액자 = 수업 장면(초등↔중등 짝)과 따로, 오래 켜 두는 그림. 모니터 오른쪽 위 액자 단추 → 목록 → 고르면 그 액자가 돈다.
// 하나 더 넣으려면: 여기에 { key, title, desc } 를 더하고 AdminDisplay.jsx 의 FrameStage 에서 key 로 그릴 것을 고른다.
//   story: true — 장면 묶음(../stories.js 의 같은 key). 수업 장면처럼 짝 장면을 차례로 돌린다(frames/story.jsx).
//   lab: true   — 실험 액자. 하노이의 탑처럼 고르는 수(문 개수 · 단계 · 구슬 수 …)를 바꿔 가며 직접 해 보고,
//                 「풀이 보기」를 고르면 설명 장면(../stories.js 의 EXPLAIN)을 돌린다(frames/xkit.jsx).
// 순서: 하노이의 탑 · 실험 액자 셋 · 장면 묶음 둘
export const FRAMES = [
  { key: "hanoi", title: "하노이의 탑", desc: "원판을 하나씩 옮겨 탑을 통째로 옮겨요. 다 옮기면 거꾸로 — 쉬지 않고 돌아요." },
  { key: "monty", lab: true, title: "몬티홀 — 바꿀까, 그대로 둘까?",
    desc: "문을 눌러 고르고, 사회자가 문을 연 뒤 바꿀지 정해요. 문 수를 바꿔 가며 기록을 모아요." },
  { key: "branch", lab: true, title: "갈림길과 구슬 — 하나씩, 한꺼번에",
    desc: "구슬을 하나씩, 또 주머니째 한꺼번에 떨어뜨려요. 서로 부딪히면 확률이 달라질까요?" },
  { key: "galton", lab: true, title: "구슬 낙하 실험 — 갈톤 보드",
    desc: "구슬 수백 개가 못에 부딪히며 칸에 쌓여요. 못 줄과 구슬 수를 바꿔 보세요." },
  { key: "soccer", story: true, title: "숫자로 읽는 축구",
    desc: "실제 경기 여섯 장면을 줄자·시간·넓이와 피타고라스·교점·확률로 읽어요." },
  { key: "essay", story: true, title: "서술형 이야기",
    desc: "선로·역주행·동아리·가위바위보·간판·반티 — 여섯 이야기를 가능성과 확률, 일차함수로 풀어요." },
];
export const frameOf = (key) => FRAMES.find((f) => f.key === key) || null;
