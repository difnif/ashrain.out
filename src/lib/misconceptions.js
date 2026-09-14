// ashrain.out — 오개념 코드 사전 (itemfactory/genkit/labels.py MISCONCEPTIONS 와 동일 내용의 JS 사본)
// 생성 문항의 labels.L42_distractor_map(보기 → 코드), tags(MC-*) 를 학생 화면에서 한글로 풀 때 쓴다.
// 코드를 추가할 때는 labels.py 에 먼저 등록하고 여기에 복사한다.

export const MISCONCEPTIONS = {
  // 수와 연산
  "MC-SIGN-01": "음수 부호를 빠뜨림",
  "MC-SIGN-02": "뺄셈에서 부호를 바꾸지 않음 (a-(-b))",
  "MC-ORDER-01": "연산 순서 무시 (곱셈·나눗셈 우선 안 함)",
  "MC-FRAC-01": "분모끼리·분자끼리 더함",
  "MC-FRAC-02": "통분하지 않고 계산",
  "MC-FRAC-03": "역수를 취하지 않고 분수 나눗셈",
  "MC-DEC-01": "소수점 자리 어긋남",
  "MC-ABS-01": "절댓값을 부호 제거로만 이해",
  "MC-MID-01": "중점 대신 두 수의 합/차를 씀",
  "MC-DIST-01": "거리에서 절댓값을 취하지 않음",
  // 문자와 식
  "MC-ALG-01": "동류항이 아닌 항을 합침",
  "MC-ALG-02": "괄호 앞 음수를 분배하지 않음",
  "MC-ALG-03": "계수와 차수를 혼동",
  "MC-EQ-01": "이항할 때 부호를 바꾸지 않음",
  "MC-EQ-02": "양변에 같은 연산을 하지 않음",
  // 함수·그래프
  "MC-FUN-01": "기울기와 y절편을 바꿔 읽음",
  "MC-FUN-02": "x의 증가량과 y의 증가량을 뒤집음",
  "MC-FUN-03": "정비례와 반비례를 혼동",
  // 기하
  "MC-GEO-01": "넓이 공식에 밑변·높이가 아닌 변을 넣음",
  "MC-GEO-02": "반지름과 지름을 혼동",
  "MC-GEO-03": "닮음비와 넓이비를 같게 봄 (제곱 누락)",
  "MC-GEO-04": "겉넓이와 부피를 혼동 (차원 혼동)",
  "MC-GEO-05": "각의 합 성질을 잘못 적용 (삼각형 180°)",
  "MC-GEO-06": "π를 빠뜨리거나 3으로 대체",
  "MC-SECT-01": "중심각 비율을 곱하지 않고 원 전체로 계산",
  "MC-SECT-02": "부채꼴의 호의 길이와 넓이를 바꿔 씀",
  "MC-POLY-01": "다각형 내각의 합에서 (n-2)를 n으로 씀",
  "MC-POLY-02": "내각의 합과 한 내각을 혼동 (n으로 나누지 않음)",
  "MC-TRI-01": "삼각형 세 내각의 합을 360°로 봄",
  "MC-TRI-02": "외각을 이웃한 내각과 같다고 봄",
  "MC-CYL-01": "원기둥 부피에서 반지름을 제곱하지 않음",
  "MC-CYL-02": "지름을 반지름으로 그대로 씀",
  "MC-CYL-03": "원기둥 겉넓이에서 밑면을 하나만 셈",
  "MC-CYL-04": "옆면 직사각형의 가로를 원주 2πr가 아니라 지름·반지름으로 씀",
  "MC-CONE-01": "뿔의 부피에 1/3을 곱하지 않음 (기둥의 부피로 계산)",
  "MC-CONE-02": "원뿔 옆넓이에서 모선 대신 높이를 씀",
  "MC-SPH-01": "구의 부피 4/3 또는 겉넓이 4를 빠뜨림",
  "MC-DIAG-01": "대각선 개수에서 2로 나누지 않음 (두 번 셈)",
  "MC-DIAG-02": "한 꼭짓점에서 그을 수 있는 대각선을 n − 2 로 봄 (n − 3 이 맞음)",
  "MC-ANG-01": "평각을 360°로 봄 (180°가 맞음)",
  "MC-ANG-02": "맞꼭지각이 아닌 이웃한 각을 같다고 봄",
  "MC-MEAN-01": "평균에서 합을 개수로 나누지 않거나 개수를 잘못 셈",
  "MC-MEAN-02": "두 집단의 평균을 인원수와 무관하게 단순 평균 냄",
  "MC-INEQ-01": "음수로 나눌 때 부등호의 방향을 바꾸지 않음",
  "MC-INEQ-02": "이항할 때 부호를 바꾸지 않음 (부등식)",
  "MC-INEQ-03": "부등호 방향이 반대인 해를 고름",
  "MC-EXP-01": "지수법칙에서 지수끼리 곱함 (aᵐ × aⁿ = aᵐⁿ 으로)",
  "MC-EXP-02": "거듭제곱의 거듭제곱에서 지수를 더함 ((aᵐ)ⁿ = aᵐ⁺ⁿ 으로)",
  "MC-EXP-03": "나눗셈에서 지수를 나눔 (aᵐ ÷ aⁿ = aᵐ÷ⁿ 으로)",
  "MC-EXP-04": "곱의 거듭제곱에서 계수에 지수를 적용하지 않음",
  "MC-DIGIT-01": "두 자리 수를 10a + b 가 아니라 ab(곱)나 a + b 로 씀",
  "MC-PCT-01": "증감률을 각 집단이 아니라 전체에 적용함",
  // 공간 — 위치관계
  "MC-POS-01": "만나지 않으면 모두 평행이라고 봄 (꼬인 위치를 평행으로)",
  "MC-POS-02": "한 점에서 만나는 모서리를 꼬인 위치(또는 평행)로 봄",
  "MC-POS-03": "면에 포함된 모서리를 면과 평행하다고 봄",
  "MC-POS-04": "면과 수직인 모서리와 면에 평행한 모서리를 혼동",
  // 통계·확률
  "MC-STAT-01": "도수와 상대도수를 혼동",
  "MC-STAT-02": "평균 대신 중앙값(또는 반대)",
  "MC-PROB-01": "전체 경우의 수를 잘못 셈",
  // 활용 유형
  "MC-TRAIN-01": "통과 거리에 기차 길이를 더하지 않음",
  "MC-CONC-01": "농도를 두 농도의 단순 평균으로 계산",
  // 절차·부주의
  "MC-CALC-01": "단순 계산 실수",
  "MC-UNIT-01": "단위 환산 누락 (분↔시간, cm↔m)",
  "MC-READ-01": "구하는 대상을 잘못 읽음 (중간값을 답으로)",
};

export const isMcCode = (s) => typeof s === "string" && /^MC-[A-Z]+-\d{2}$/.test(s);

/** 코드 → 한글 설명 (미등록 코드는 코드 그대로) */
export const mcLabel = (code) => MISCONCEPTIONS[code] || code || "";

/** 문항의 오개념 코드 목록 (labels.L20_distractor_rule → tags 의 MC-* 순) */
export function mcCodesOf(item) {
  const a = item?.labels?.L20_distractor_rule;
  if (Array.isArray(a) && a.length) return a.filter(isMcCode);
  return (item?.tags || []).filter(isMcCode);
}

/** 학생이 고른 보기(텍스트)에 대응하는 오개념 코드 — labels.L42_distractor_map */
export function distractorTag(item, chosenChoice) {
  const map = item?.labels?.L42_distractor_map;
  if (!map || chosenChoice == null) return null;
  const k = String(chosenChoice);
  return map[k] || map[k.replace(/\s+/g, "")] || null;
}

/** 오개념 코드 → wrong_notes.reason (calc | concept | reading | time | guess | etc) */
export function reasonForMc(code) {
  if (!code) return "etc";
  if (/^MC-(CALC|SIGN|ORDER|DEC|UNIT)-/.test(code)) return "calc";
  if (/^MC-READ-/.test(code)) return "reading";
  return "concept";
}

export const REASON_LABEL = {
  calc: "계산 실수", concept: "개념 부족", reading: "문제 잘못 읽음", time: "시간 부족", guess: "찍음", etc: "기타",
};
