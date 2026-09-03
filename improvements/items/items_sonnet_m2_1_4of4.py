# -*- coding: utf-8 -*-
# esc_sonnet_m2-1_4of4 — 이미지 기준 전사 (8 항목 / 8쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ---------------- 단항식의 계산에서 빈 칸에 알맞은 식 구하기 p60
add(id="d99410a5", qtype="choice",
    question=("두 식 [[a]], [[b]]에 대하여 ◇, ◎를\n"
              "[[a]] ◇ [[b]] = [[3a pow(b,2)]], [[a]] ◎ [[b]] = [[a b]]\n"
              "라 하자. 이때 다음을 만족시키는 두 식 [[A]], [[B]]에 대하여 [[2A / (3 pow(B,2))]]을 계산한 것은?\n"
              "[[A]] ◇ [[3x]] = [[54 pow(x,5) pow(y,3)]], [[3 pow(y,2)]] ◎ [[B]] = [[12 pow(x,3) pow(y,4)]]"),
    choices=["[[frac(3,4) pow(x,2) y]]", "[[frac(1, 12 pow(x,3) y)]]", "[[frac(8,9) x pow(y,3)]]",
             "[[frac(1, 24 pow(x,3) pow(y,2))]]", "[[frac(5 pow(x,2), 4 pow(y,3))]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="A◇3x=3A(3x)²=27x²A=54x⁵y³ → A=2x³y³; 3y²B=12x³y⁴ → B=4x³y²; 2A÷3B²=4x³y³÷48x⁶y⁴=1/(12x³y) → ②. 빠른정답 5와 불일치. 연산 기호 ◇, ◎는 텍스트.")

# ---------------- 도형에서의 단항식의 계산(1) - 평면도형 p65
add(id="d895de47", qtype="choice",
    question="밑변의 길이가 [[9a pow(b,2)]], 높이가 [[2 pow(a,2) pow(b,2)]]인 삼각형의 넓이는?",
    choices=["[[9 pow(a,2) pow(b,4)]]", "[[9 pow(a,3) pow(b,2)]]", "[[9 pow(a,3) pow(b,4)]]",
             "[[18 pow(a,2) pow(b,4)]]", "[[18 pow(a,3) pow(b,4)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="½·9ab²·2a²b²=9a³b⁴ → ③. 빠른정답 2와 불일치.")

# ---------------- p67
add(id="c809f497", qtype="choice",
    question="밑변의 길이가 [[2a pow(b,2)]], 높이가 [[pow(a,2) b]]인 삼각형의 넓이는?",
    choices=["[[pow(a,2) b]]", "[[pow(a,3) pow(b,3)]]", "[[2 pow(a,3) pow(b,3)]]",
             "[[4 pow(a,3) pow(b,3)]]", "[[pow(a,6) pow(b,6)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="½·2ab²·a²b=a³b³ → ② = 빠른정답 ✓.")

# ---------------- p73 (직사각형·삼각형 그림)
add(id="640d358f", qtype="choice",
    question="다음 그림의 직사각형과 삼각형의 넓이가 서로 같을 때 삼각형의 높이는?",
    choices=["[[7a b]]", "[[7 pow(a,2) b]]", "[[7 pow(a,3) pow(b,2)]]",
             "[[14 pow(a,2) pow(b,2)]]", "[[14 pow(a,3) pow(b,2)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽: 분홍 음영 직사각형, 가로 2a³b³(아래 점선 호 치수), 세로 7a²b⁴(오른쪽 점선 호 치수). 오른쪽: 하늘색 음영 삼각형(꼭짓점 위), 밑변 4a²b⁵(아래 점선 호 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형·삼각형 치수 도형(치수가 그림에만 있음)",
    note="직사각형 넓이 14a⁵b⁷ = ½·4a²b⁵·h → h=7a³b² → ③. 빠른정답 4와 불일치.")

# ---------------- p74
add(id="480b78f5", qtype="choice",
    question=("가로의 길이가 [[3a pow(b,2)]], 세로의 길이가 [[4 pow(a,2) b]]인 직사각형의 넓이는 밑변이 [[6 pow(a,3) pow(b,2)]], "
              "높이가 □인 평행사변형의 넓이와 같을 때, □ 안에 들어갈 식을 구하면?"),
    choices=["[[a b]]", "[[2a b]]", "[[2a]]", "[[2b]]", "[[pow(a,2) b]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="12a³b³ = 6a³b²·h → h=2b → ④. 빠른정답 3과 불일치. 빈칸 상자는 □ 텍스트.")

# ---------------- 도형에서의 단항식의 계산(2) - 입체도형 p80 (원기둥·쇠공 그림)
add(id="c315269f", qtype="short",
    question=("밑면의 반지름의 길이가 [[4x]]인 원기둥 모양의 그릇과 반지름의 길이가 [[3x]]인 구 모양의 쇠공이 있다. "
              "다음 그림과 같이 그릇 안에 쇠공이 잠길 만큼 충분히 많은 양의 물을 넣은 후 쇠공을 넣을 때, 높아진 물의 높이는 [[k x]]이다. "
              "이때 [[abs(4k - 11)]]의 값을 구하시오. (단, [[k]]는 상수이다.)"),
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": "물(하늘색)이 담긴 원기둥 그릇 안에 분홍색 구(쇠공)가 잠겨 있는 삽화. 윗면 반지름 4x, 구의 반지름 3x 표시"}}],
    difficulty_est=2, confidence=0.85,
    note="구 부피 36πx³ ÷ 밑넓이 16πx² = (9/4)x → k=9/4, |9−11|=2. 빠른정답 '54개'와 불일치(정렬 어긋남). 그림은 본문 치수를 그대로 보여주는 삽화.")

# ---------------- p88
add(id="e7f99769", qtype="choice",
    question="직육면체의 가로의 길이가 [[4 pow(a,2) b]], 세로의 길이가 [[3b]]이고, 부피가 [[24 pow(a,3) pow(b,4)]]이다. 이때 직육면체의 높이는?",
    choices=["[[2 pow(a,2) b]]", "[[2a pow(b,2)]]", "[[6 pow(a,2) b]]", "[[6a pow(b,2)]]", "[[2a b]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="24a³b⁴÷(4a²b·3b)=2ab² → ② = 빠른정답 ✓.")

# ---------------- 단항식의 곱셈과 나눗셈의 활용 p95 (전력 관계식)
add(id="bcf62e1d", qtype="choice",
    question=("저항 양단에 걸리는 전압에 의해 전류가 흐를 때 소모되는 전력을 전기 에너지라고 한다. "
              "저항에서 소모되는 전력을 [[P]](W), 저항값을 [[R]](Ω), 저항에 걸리는 전압을 [[V]](V)라 할 때, "
              "저항에서 소모되는 전력은 다음과 같은 관계식이 성립한다.\n"
              "[[P = frac(pow(V,2), R)]]\n"
              "두 저항기 [[A]]와 [[B]]에 대하여 저항기 [[A]]의 저항값은 저항기 [[B]]의 저항값의 2배이고, "
              "저항기 [[A]]에 걸리는 전압은 저항기 [[B]]에 걸리는 전압의 3배이다. "
              "두 저항기 [[A]]와 [[B]]에서 소모되는 전력을 각각 [[sub(P, A)]]와 [[sub(P, B)]]라 할 때, "
              "[[frac(sub(P, A), sub(P, B))]]의 값은?"),
    choices=["[[frac(5,2)]]", "[[3]]", "[[frac(7,2)]]", "[[4]]", "[[frac(9,2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2025년 6월 고1 7번 변형]. P_A=(3V)²/(2R)=9V²/(2R), P_B=V²/R → 9/2 → ⑤ = 빠른정답 ✓.")
