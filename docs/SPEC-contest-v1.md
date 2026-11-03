# SPEC-경시대비-v1 — 경시 대비(KUT 등) 문항 패키지·내보내기 규격

앱은 AI를 부르지 않는다. AI가 필요한 일(정답·해설·문항 특성 판단, 학생 분석)은 전부 채팅방에서 한다.

```
PDF(프린트) ──채팅방──▶ 문항 패키지 JSON ──▶ 관리자 #/admin/contest 가져오기
                                              │  응시자·응답 입력 (정오 판정 = 앱)
                                              ▼
                       채팅방 ◀── 분석용 md (익명 코드, 특성표 + 응답 행렬 + 집계 + 원자료 JSON)
```

- DB: `supabase/2026-11_contest.sql` — contest_sets · contest_items · contest_takers · contest_responses, 비공개 버킷 `contest-files`(프린트 PDF). 전부 관리자 전용.
- 코드: `src/lib/contest.js`(검증·판정·지표·내보내기), `src/pages/AdminContest.jsx`.

## 1. 세트 코드

`KUT-{연도}-{회차}-{학년}` 예: `KUT-2025-1-M2`. 같은 코드로 다시 가져오면 문항을 교체하고 기존 응답을 새 정답으로 재채점한다. 프린트 파일만 먼저 올리려면 「+ 새 프린트」로 같은 코드의 빈 세트를 만든다.

## 2. 문항 패키지 JSON (`contest-set/v1`)

```json
{
  "format": "contest-set/v1",
  "set": { "code": "KUT-2025-1-M2", "title": "2025 상반기 KUT 중2", "contest": "KUT",
           "year": 2025, "round": "상반기", "grade_label": "중2", "test_date": "2025-06-01" },
  "items": [
    {
      "no": 1, "points": 4,
      "answer_type": "choice",          // choice | int | text
      "n_choices": 5,
      "answer": "3",                    // 또는 ["3"] — 여럿이면 모두 정답
      "text": "발문 원문 (수식은 $...$)",  // 앱이 글자 수·문장 수·수식 수·조건 항목을 센다
      "features": {
        "grade": "중2", "unit": "연립방정식",
        "concept_main": "m2-1-3", "concept_sub": ["m1-2-1"],
        "domain": "대수",                // 대수·정수론·조합(경우의 수)·확률·기하·함수·통계·논리
        "type_code": "ALG-SYS-02", "type_name": "연립방정식 활용(비율)",
        "strategies": ["미지수 설정", "비례식"],
        "figure": { "has": false, "kind": null, "aux_line": false },   // kind: 평면|입체|좌표|그래프|표
        "steps": 3, "concepts_needed": 2,
        "calc_load": "중",               // 상|중|하
        "insight": "정형",               // 정형|발상
        "trap": "단위 환산을 빠뜨리기 쉬움",
        "difficulty": 3,                 // 1~5 예상 난이도 (근거: steps·concepts_needed·calc_load·insight·trap)
        "distractors": { "2": "부호 실수", "5": "합과 차 혼동" }
      },
      "solution": { "steps": ["…", "…"] }
    }
  ]
}
```

필수: `set.code`, `set.title`, 각 문항 `no`(정수·중복 없음), `answer`. 나머지는 비면 내보내기에 "—"로 나간다.

## 3. 답 판정 (앱)

정규화 후 일치: 공백 제거 · ①~⑩ → 1~10 · 전각 숫자 → 반각 · 끝의 "번" 제거 · 숫자는 `007 → 7`. 빈칸 = 무응답(정오 null).

## 4. 응답 입력

- 프린트 찾기(연도·학년·회차 검색) → 학생 선택·추가(이름+학년이 같으면 같은 학생) → 번호 칸에 답 입력 → 저장.
- 여러 명: `이름⇥학년⇥1번⇥2번⇥…` 줄 단위 붙여넣기(엑셀 복사 그대로, 쉼표도 됨).

## 5. 분석용 md (`contest-export/v1`)

1. 시험 정보 · 2. 문항 특성표(1-1 판단+실측 지표, 1-2 문장·도형 지표, 1-3 함정·오답 예측) · 3. 응답 행렬(○ / ×쓴답 / ·) · 4. 집계(학생별 점수·순위·영역별 정답, 객관식 선택 분포) · 5. 원자료 JSON.
- 학생은 익명 코드 `S0001`만 나간다. 변별도 = 상위·하위 27% 정답률 차(응시 4명 이상일 때).
