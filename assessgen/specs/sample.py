# 서술형 평가 샘플(체험용, 3문제) — 앱 흐름 시험용. 실제 회차는 채팅에서 범위를 받아 같은 모양으로 만든다.
from fractions import Fraction as F

FIG_TANK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 170" width="220" height="170" font-family="Noto Sans KR, sans-serif" font-size="11">
  <line x1="36" y1="140" x2="206" y2="140" stroke="#111" stroke-width="1.4"/>
  <line x1="36" y1="140" x2="36" y2="12" stroke="#111" stroke-width="1.4"/>
  <path d="M202 136 L208 140 L202 144" fill="none" stroke="#111" stroke-width="1.4"/>
  <path d="M32 16 L36 10 L40 16" fill="none" stroke="#111" stroke-width="1.4"/>
  <line x1="36" y1="30" x2="186" y2="140" stroke="#111" stroke-width="2"/>
  <line x1="31" y1="30" x2="41" y2="30" stroke="#111" stroke-width="1.2"/>
  <line x1="186" y1="135" x2="186" y2="145" stroke="#111" stroke-width="1.2"/>
  <text x="28" y="34" text-anchor="end">200</text>
  <text x="186" y="157" text-anchor="middle">25</text>
  <text x="28" y="152" text-anchor="end">O</text>
  <text x="214" y="132" text-anchor="end" font-style="italic">x(분)</text>
  <text x="44" y="14" font-style="italic">y(L)</text>
</svg>"""

SPEC = {
    "code": "SAMPLE01",
    "title": "서술형 평가 샘플(체험용)",
    "level": "mid",
    "grade_label": "중2",
    "date": "2026-10-14",
    "reveal": "after_submit",
    "policy": {"carry": "half", "alt_method": "accept", "answer_only_max": 3},
    "items": [
        {
            "topic": "연립방정식의 활용",
            "story": "과학관 입장료는 어른 한 명에 3000원, 학생 한 명에 2000원입니다. 어른과 학생을 합하여 12명이 과학관에 들어가면서 입장료로 모두 29000원을 냈습니다.",
            "conditions": [],
            "ask": "학생은 몇 명인지 구하시오.",
            "answer": "7명",
            "solution": [
                "어른을 [[x]]명, 학생을 [[y]]명이라 하면",
                "[[x + y = 12]], [[3000x + 2000y = 29000]] (곧 [[3x + 2y = 29]])",
                "[[3x + 2y = 29]] 에서 [[2x + 2y = 24]] 를 빼면 [[x = 5]], [[y = 7]]",
                "따라서 학생은 7명",
            ],
            "rubric": [
                {"no": 1, "element": "식 세우기", "points": 4, "criterion": "어른·학생 수를 미지수로 놓고 x + y = 12, 3000x + 2000y = 29000(또는 3x + 2y = 29)을 세웠다.", "partial": "식 하나만 바르게 세웠으면 2점."},
                {"no": 2, "element": "식 풀기", "points": 3, "criterion": "연립방정식을 풀어 x = 5, y = 7을 구했다.", "partial": "풀이 방법은 맞으나 계산 실수로 값이 틀리면 1점."},
                {"no": 3, "element": "구하는 것", "points": 3, "criterion": "학생 수 7명을 답했다.", "partial": "어른 수(5명)를 답하면 0점."},
            ],
        },
        {
            "topic": "일차함수의 활용",
            "story": "물 200 L가 들어 있는 물탱크에서 1분에 8 L씩 물을 빼냅니다. 물을 빼기 시작한 지 [[x]]분 후 물탱크에 남은 물의 양을 [[y]] L라 할 때, [[x]]와 [[y]] 사이의 관계를 나타낸 그래프는 오른쪽 그림과 같습니다.",
            "figure_svg": FIG_TANK,
            "conditions": [],
            "ask": "남은 물의 양이 72 L가 되는 것은 물을 빼기 시작한 지 몇 분 후인지 구하시오.",
            "answer": "16분 후",
            "solution": [
                "1분에 8 L씩 줄어드므로 [[y = 200 - 8x]]",
                "[[y = 72]] 를 대입하면 [[72 = 200 - 8x]], [[8x = 128]], [[x = 16]]",
                "따라서 16분 후",
            ],
            "rubric": [
                {"no": 1, "element": "식 세우기", "points": 4, "criterion": "y = 200 − 8x (또는 y = −8x + 200)를 세웠다.", "partial": "기울기와 y절편 중 하나만 맞으면 2점."},
                {"no": 2, "element": "식 풀기", "points": 3, "criterion": "y = 72를 대입해 x = 16을 구했다.", "partial": "대입은 맞으나 계산 실수로 값이 틀리면 1점."},
                {"no": 3, "element": "구하는 것", "points": 3, "criterion": "16분 후라고 답했다.", "partial": "단위(분)가 빠지면 2점."},
            ],
        },
        {
            "topic": "확률의 계산",
            "story": "주머니 속에 빨간 공 3개와 파란 공 2개가 들어 있습니다. 이 주머니에서 공을 한 개 꺼내 색을 확인하고, 꺼낸 공을 다시 넣지 않고 한 개를 더 꺼냅니다.",
            "conditions": [],
            "ask": "두 번 모두 빨간 공이 나올 확률을 구하시오.",
            "answer": "[[frac(3,10)]]",
            "solution": [
                "첫 번째에 빨간 공이 나올 확률은 [[frac(3,5)]]",
                "다시 넣지 않으므로 두 번째에 빨간 공이 나올 확률은 [[frac(2,4)]]",
                "[[frac(3,5) * frac(2,4) = frac(6,20) = frac(3,10)]]",
            ],
            "rubric": [
                {"no": 1, "element": "식 세우기", "points": 4, "criterion": "첫 번째 3/5, 두 번째(다시 넣지 않음) 2/4를 곱하는 식을 세웠다.", "partial": "두 번째 확률을 3/5로 썼으면(다시 넣는 경우) 1점."},
                {"no": 2, "element": "식 풀기", "points": 3, "criterion": "3/5 × 2/4 = 6/20을 계산했다.", "partial": "곱셈 실수가 있으면 1점."},
                {"no": 3, "element": "구하는 것", "points": 3, "criterion": "3/10으로 답했다.", "partial": "약분하지 않은 6/20이면 2점."},
            ],
        },
    ],
}


def verify():
    # 1번: 어른 x, 학생 y
    sols = [(x, 12 - x) for x in range(13) if 3000 * x + 2000 * (12 - x) == 29000]
    assert sols == [(5, 7)], sols
    # 2번: y = 200 - 8x, y = 72
    assert [x for x in range(30) if 200 - 8 * x == 72] == [16]
    assert 200 / 8 == 25                      # 그림의 x절편
    # 3번: 빨강 3, 파랑 2, 다시 넣지 않고 두 번
    balls = ["R"] * 3 + ["B"] * 2
    pairs = [(i, j) for i in range(5) for j in range(5) if i != j]
    rr = [(i, j) for i, j in pairs if balls[i] == "R" and balls[j] == "R"]
    assert F(len(rr), len(pairs)) == F(3, 10) == F(3, 5) * F(2, 4)
    return {"1": "학생 7명 (어른 5)", "2": "16분 후", "3": "3/10 (6/20 약분)"}
