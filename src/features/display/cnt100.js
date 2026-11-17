// ashrain.out — 교실 모니터 「경우의 수와 확률 100제 해설」 계산 (cnt100.js) — JSX 없음
// 프린트 두 세트(cnt100-items.js)를 일차함수 10단계 액자와 같은 판서 재생기로 돌린다:
//   ① 문제 → ② 전략(방침 칸) → ③ 판서: 포지티브 · 네거티브 → 식을 한 줄씩 → ④ 답. 박자표는 lin10.js 의 l10Plan 을 그대로 쓴다.
import { CNT100_SEL, CNT100_BALL } from "./cnt100-items.js";

export const C100_SETS = {
  sel: {
    key: "sel", name: "학년별 선발", items: CNT100_SEL,
    stage: { 1: "합 · 곱의 법칙", 2: "자격이 다른 · 같은 대표", 3: "조건이 붙은 선발", 4: "선발의 확률", 5: "도전" },
  },
  ball: {
    key: "ball", name: "주머니 공 꺼내기", items: CNT100_BALL,
    stage: { 1: "한 개 꺼내기 · 두 주머니", 2: "수 만들기 · 동시에 꺼내기", 3: "색 조건 · 기본 확률", 4: "두 개 꺼내는 확률", 5: "도전" },
  },
};
export const C100_KEYS = ["sel", "ball"];
export const C100_SPEEDS = [1, 1.5];
