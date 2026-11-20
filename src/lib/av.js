// ashrain.out — 공부하기 › 시청각 학습 목록 (교실 모니터 콘텐츠를 학생앱에)
// 교실 모니터(#/admin/display)의 수업 장면 · 액자를 학생이 직접 연다 — 같은 무대(AdminDisplay 의 Stage)를 av 모드로.
//   · 수학 호기심 — 수업 장면(도형 · 경우의 수 애니메이션), 하노이의 탑, 실험 액자(몬티홀 · 갈림길 · 갈톤 보드), 장면 묶음(축구 · 서술형 이야기),
//                  그림 액자 일곱(축구 · 농구 · 야구 직선, 주머니 공 꺼내기, 알파벳 카드, 일렬로 세우기, 학년별 뽑기 — frames/curio.jsx)
//   · 문제 풀이 해설 — 해설 액자(일차함수 그래프 그리기 · 10단계 계산 · 그래프와 넓이 · 경우의 수와 확률 100제 — 선발 · 공 꺼내기 · 사전식 · 줄 세우기)
// 여는 주소: #/av/<key> — key 는 액자 key(frames/index.js) 또는 scenes-<묶음>(pairs.js 의 GROUPS).
// 교실 모니터에 액자가 새로 들어오면: frames/index.js 의 lesson 표시를 따라 저절로 갈린다(lesson → 문제 풀이 해설, 나머지 → 수학 호기심).
import { FRAMES } from "../features/display/frames/index.js";

export const AV_CATS = [
  { id: "fun", title: "수학 호기심", icon: "🔭", sub: "도형이 움직이고, 구슬이 떨어지고, 문이 열려요 — 보고 직접 해 보는 수학" },
  { id: "sol", title: "문제 풀이 해설", icon: "🎬", sub: "학원 프린트 문항을 한 문항씩 — 문제 → 방침 → 한 줄씩 → 답" },
];

// 수업 장면(초등 ↔ 중등 짝 애니메이션) — 묶음별로 하나씩
const SCENES = [
  { key: "scenes-geo", grp: "geo", icon: "🔷", title: "도형 애니메이션", desc: "도형이 접히고 펼쳐지고 돌아가요. 오른쪽 위 「초등 | 중등」을 누르면 같은 장면이 짝 장면으로 겹쳐 넘어가요." },
  { key: "scenes-data", grp: "data", icon: "🎲", title: "경우의 수 · 확률 애니메이션", desc: "줄 세우기 · 뽑기 · 확률을 움직이는 그림으로. 「초등 | 중등」으로 같은 장면을 두 학년 눈높이로 봐요." },
];
const ICON = { hanoi: "🗼", monty: "🚪", branch: "🔀", galton: "⚪", soccer: "⚽", essay: "📖", graph: "📈", lin10: "🔢", area: "📐", cnt100: "🎯",
  soccerfn: "🥅", hoopfn: "🏀", batfn: "⚾", pouch: "👝", lexi: "🔤", lineup: "🧍", crowd: "🔍" };

export const AV_ITEMS = [
  ...SCENES.map((s) => ({ ...s, cat: "fun", kind: "scene", frame: null })),
  ...FRAMES.map((f) => ({
    key: f.key, frame: f.key, grp: null, cat: f.lesson ? "sol" : "fun", icon: ICON[f.key] || "🖼",
    kind: f.lesson ? "해설" : f.lab ? "실험" : f.story ? "이야기" : "그림", title: f.title, desc: f.desc,
  })),
];
for (const s of AV_ITEMS) if (s.kind === "scene") s.kind = "애니메이션";

export const avItem = (key) => AV_ITEMS.find((x) => x.key === key) || null;
export const avOfCat = (cat) => AV_ITEMS.filter((x) => x.cat === cat);
