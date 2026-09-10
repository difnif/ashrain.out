# AI허브 공공데이터 4종 — 구조·용도 판정 (2026-09-08)

원본 위치: `C:\Users\opens\Documents\public data\` (다운로드 완료). 라벨 JSON은 UTF-8 **BOM** 있음 → `encoding="utf-8-sig"`.
**이용 조건**: AI허브 데이터는 출처 표기 의무(제품·문서에 "본 결과물은 AI허브 「데이터셋명」을 활용하였습니다" 류). 학습·평가 실험용으로만 쓰고 문항 텍스트를 서비스에 그대로 노출하지 않는다.

## 요약 판정

| 데이터셋 | 내용 | 우리 용도 | 우선순위 |
|---|---|---|---|
| **110. 수학 과목 자동 풀이 데이터** | 문항(서술형 100 %) + 모범답안(필수 요소 bbox·개수) + **학생 손글씨 풀이 전사 + 오류 라벨**. 중1 검증셋만 486문항 × 6풀이 = 2,853건 | **채점 실험의 정답 데이터.** 우리 채점기준(요소·checks)으로 학생 풀이를 채점 → 라벨(정답 여부·필수요소 누락 수·계산 오류)과 대조 | ★★★ |
| 111. 수학 과목 문제생성 데이터 | 문항 + 모범답안(선택형 포함). 중1 검증셋 1,152문항. 학생 풀이 없음 | 토픽 코드(`question_topic` 7자리)·난이도·정답률 메타가 붙은 문항 코퍼스. 유형 참고 | ★★ |
| 30. 수학 교과 문제 풀이과정 데이터 | 2015 교과서(교학사 등) 주관식 문항 + 정답 + 짧은 해설, 성취기준 코드(2009/2015/2022) 매핑 | 성취기준 코드 ↔ 우리 concept 매핑 참고. 채점 정보 없음 | ★ |
| 25. 서술형 글쓰기 평가 데이터(수학) | **개념 설명 글쓰기**(중1 수학 지시문 3개 × ~320답안). 채점자 2명, 총체 1~5점 + 분석 8항목(충실성·명료성·구체성·적절성·조직·표현) + 피드백 문장 | 계산 서술형과는 다름. "개념 설명형" 문항의 수행 수준 문구·채점자 일치도(총체 점수 정확 일치 76 %, ±1 이내 99 %) 참고 | ★ |

## 110 자동 풀이 데이터 — 스키마 (중1 Validation 기준)

파일 3종이 같은 `id` 로 연결된다. 파일명 `M1_1_01_21720_51479[_A|_{n}_O].json` = 학년_학기_단원_id.

```
question_info[0]: question_grade "M1", question_term 1, question_unit "01", question_topic "7101003",
                  question_topic_name "수를 거듭제곱으로 나타내기", question_type1 "서술", question_sector1 "추론"(이해/추론/문제해결…),
                  question_sector2 "수와 연산", question_step "기본", question_difficulty 1~5, question_rtime(초), question_success_rate(%)
OCR_info[0].question_text        : 문항 텍스트 (LaTeX $…$)
answer_info[0] (모범답안, _A)     : answer_text · answer_bbox(type: line/paragraph/answer)
                                   answer_required_num · answer_required_bbox  ← 모범답안 안의 '필수 요소' 개수·위치 (1~6, 최빈 2~3)
                                   answer_clac_num · answer_clac_bbox          ← 계산 단계 개수·위치
explanation_info[0] (학생 풀이, _n_O): explanation_text(손글씨 전사, LaTeX array 포함)
                                   explanation_error_required  ← 필수 요소 누락 개수 (0~6)
                                   explanation_error_clac_num / _acc ← 계산 단계 수 / 계산 정확 여부
                                   explanation_correct 0|1 · explanation_difficulty
```

중1 검증셋 분포: 정답 855 / 오답 1,998 (정답률 30 %). 필수요소 누락 0개 522 · 1개 770 · 2개 835 · 3개 577 · 4개 이상 149. 모범답안 필수요소 수 1개 446 · 2개 1,218 · 3개 957 · 4개 이상 232. 토픽 181개(다각형 내·외각, 종이접기, y=a/x 식, 바르게 계산한 답, 삼각형 외각, 해가 같은 연립·방정식 미지수, 회전체 단면, 식의 값 활용 순).

**라벨의 채점 철학**: "최종 값이 맞아도 필수 요소를 빠뜨리면 오답(correct=0)" 으로 매긴 사례가 있다(예: 사각형 합동 문항 — 115를 맞게 썼지만 근거 진술 3개 누락 → 0). 즉 이 데이터의 `answer_required` 는 **우리 v3의 '요소'(items) 와 같은 층**이고, 교육청 원칙("과정 없이 결과만 쓰면 요소 불인정")과 일치한다. 계산 오류는 별도 라벨(`clac_acc`)로 분리 → 교육청 원칙 "개념 오류와 계산 실수 구분"과 같은 구조.

### 채점 실험 설계 메모 (추후 논의용)
1. 우리 시드 틀과 토픽이 겹치는 110 문항을 고른다(일차방정식 활용·다각형 내외각·평행선·기둥 부피·정비례/반비례 등 — 토픽명으로 필터).
2. 모범답안의 `answer_required_num` 과 우리 rubric 요소 수를 비교 → 요소 끊기 감각 보정.
3. 학생 풀이 6개씩에 우리 채점기준(items + checks)을 LLM 채점기로 적용 → `explanation_correct`, `explanation_error_required` 와 일치도 측정. 이게 하이러닝식 LLM 초벌 채점의 우리 버전 성능 기준선이 된다.
4. Training 셋(중1 손글씨 풀이 2.1 GB 이미지 + 라벨 31 MB)은 라벨 JSON만 쓰면 충분 — 이미지는 필요 없다.
