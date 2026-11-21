// ashrain.out — 교실 모니터 「경우의 수와 확률 100제 해설」 계산 (cnt100.js) — JSX 없음
// 프린트 네 세트(cnt100-items.js)를 일차함수 10단계 액자와 같은 판서 재생기로 돌린다:
//   ① 문제 → ② 전략(방침 칸) → ③ 판서: 포지티브 · 네거티브 → 식을 한 줄씩 → ④ 답. 박자표는 lin10.js 의 l10Plan 을 그대로 쓴다.
//   사전식은 강사 판서 방식: ② 칸이 「숫자 분석」(번호를 덩어리 합으로 쪼갬) → ③ 묶음 개수로 시작 글자 → 최종 묶음.
//   그림은 카드로 순번 찾기(frames/lexcards.jsx · ./lexwalk.js) — 묶음이 휘리릭 지나가고, 글자를 고정하고, 최종 묶음에서 점멸하며 센다.
//   그 움직임이 판서 줄 안에 다 돌도록 줄마다 hold 를 더해 둔다(lexPrep — 박자표를 처음 만들기 전에 한 번).
//   한 줄로 세우기도 자리마다 후보가 돌며 가짓수를 세는 움직임(./seatwalk.js)이 있어 같은 식으로 hold(seatsPrep).
//   학년별 선발 · 주머니 공은 판서 식의 수를 그림에 맞춰 짚어 세고 자리로 뽑는 움직임(./pickwalk.js — pickPrep).
import { CNT100_SEL, CNT100_BALL, CNT100_LEX, CNT100_LINE } from "./cnt100-items.js";
import { lexPrep } from "./lexwalk.js";
import { seatsPrep } from "./seatwalk.js";
import { pickPrep } from "./pickwalk.js";

for (const it of CNT100_LEX) lexPrep(it);
for (const it of CNT100_LINE) seatsPrep(it);
for (const it of [...CNT100_SEL, ...CNT100_BALL]) pickPrep(it);

export const C100_SETS = {
  sel: {
    key: "sel", name: "학년별 선발", short: "선발", items: CNT100_SEL,
    stage: { 1: "합 · 곱의 법칙", 2: "자격이 다른 · 같은 대표", 3: "조건이 붙은 선발", 4: "선발의 확률", 5: "도전" },
  },
  ball: {
    key: "ball", name: "주머니 공 꺼내기", short: "공 꺼내기", items: CNT100_BALL,
    stage: { 1: "한 개 꺼내기 · 두 주머니", 2: "수 만들기 · 동시에 꺼내기", 3: "색 조건 · 기본 확률", 4: "두 개 꺼내는 확률", 5: "도전" },
  },
  lex: {
    key: "lex", name: "사전식 나열(영어 단어)", short: "사전식", items: CNT100_LEX,
    stage: { 1: "A, B, C · A ~ D 중 2장", 2: "A ~ D 모두 · 3장", 3: "A ~ E · A ~ F", 4: "단어 카드 — ○번째 찾기", 5: "단어 카드 — 몇 번째인가" },
  },
  line: {
    key: "line", name: "한 줄로 세우기(이웃 · 양 끝)", short: "줄 세우기", items: CNT100_LINE,
    stage: { 1: "줄 세우기 · 자리 고정", 2: "양 끝", 3: "이웃 · 이웃하지 않기", 4: "이웃 + 양 끝 · 번갈아 · 확률", 5: "빈자리에 넣기 · 도전" },
  },
};
export const C100_KEYS = ["sel", "ball", "lex", "line"];
export const C100_SPEEDS = [1, 1.5];
