# SPEC-경시대비-v1 — 경시 대비(KUT 등) 문항 패키지·내보내기 규격

앱은 AI를 부르지 않는다. AI가 필요한 일(정답·해설·문항 특성 판단, 학생 분석)은 전부 채팅방에서 한다.

## 0. 흐름 (관리자 #/admin/contest)

1. **① 학생** — 이름·학년·전화번호 뒷자리로 등록 (이름+뒷자리가 같으면 같은 학생)
2. **② 채점** — 학생 → 프린트(연도·상/하반기로 찾기) → 답안 입력(칸 또는 한 줄 `3 5 12 - 4`) → [채점]
3. **③ 오답 프린트** — 채점한 프린트 체크 → 오답·무응답 모아 보기(원본 기준 중복 제거) → 생성 → [인쇄]
4. 오답 프린트도 ②에서 📝 표시로 골라 같은 방식으로 채점
5. **④ 분석·브리핑** — 분석할 프린트 체크 → [분석 진행] → 분석 파일(md) 받기 → 채팅방에 의뢰
6. 채팅방 분석을 다듬어 ④ 브리핑에 저장
- **프린트 관리** — 문항 패키지 JSON 가져오기, 문제지·정답지·해설지 파일 올리기·받기

DB: `supabase/2026-11_contest.sql` — contest_sets(original|wrong) · contest_items · contest_takers · contest_responses · contest_attempts · contest_briefings, 비공개 버킷 `contest-files`. 전부 관리자 전용.
코드: `src/lib/contest.js`, `src/pages/AdminContest.jsx`.

## 1. 프린트 코드

원본 `KUT-{연도}-H{1|2}-{학년}` 예: `KUT-2025-H1-M2`. 오답 프린트는 앱이 `W-S0003-20261103-1`처럼 붙인다. 같은 코드로 다시 가져오면 문항을 교체하고 이미 채점한 학생을 새 정답으로 다시 채점한다.

## 2. 문항 패키지 JSON (`contest-set/v1`)

```json
{
  "format": "contest-set/v1",
  "set": { "code": "KUT-2025-H1-M2", "title": "2025 상반기 KUT 중2", "contest": "KUT",
           "year": 2025, "half": "상반기", "grade_label": "중2", "test_date": "2025-06-01" },
  "items": [
    {
      "no": 1, "points": 4,
      "answer_type": "choice",          // choice | int | text
      "n_choices": 5,
      "answer": "3",                    // 또는 ["3"] — 여럿이면 모두 정답
      "choices": ["2", "3", "4", "5", "6"],  // 객관식 보기 문구 (오답 프린트 인쇄용)
      "text": "발문 원문 (유니코드 수식: x², ≤, ×)",  // 앱이 글자 수·문장 수·수식 수·조건 항목을 세고, 오답 프린트에 인쇄
      "figure": "data:image/png;base64,…",  // 그림 크롭 (있으면 오답 프린트에 인쇄)
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

## 4. 분석 파일 (`contest-student-export/v1`, 학생 1명 · 고른 프린트들)

1. 프린트 요약(점수·응시일) · 2. 프린트별 문항표(결과 ○/×쓴답/·, 특성, 집단 정답률, 문장·도형 지표, 함정·오답 예측) · 3. 재응시 추적(원본 문항별 시도 순서 ×→○) · 4. 영역별(기출만) · 5. 원자료 JSON.
- 학생은 익명 코드 `S0001`과 학년만 나간다. 집단 정답률 = 같은 원본 문항을 푼 모든 학생 기준.
