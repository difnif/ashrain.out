# -*- coding: utf-8 -*-
# esc_sonnet_m1-1_3of3 — 이미지 기준 전사 (35 항목 / 35쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= 덧셈, 뺄셈, 곱셈, 나눗셈의 혼합 계산 =================
# p32
add(id="92a8cfe1", qtype="short",
    question=("[[(frac(1,2) - 1) × (frac(1,3) - 1) × (frac(1,4) - 1)]] × ⋯ × [[(frac(1,10) - 1)]]을 계산하시오."),
    choices=None, derived_answer="-frac(1,10)", figure=None, difficulty_est=2, confidence=0.9,
    note="(−1/2)(−2/3)⋯(−9/10): 음수 9개 곱 → −1/10 = 빠른정답 ✓. 줄임표는 텍스트.")

# p38
add(id="2eb83082", qtype="short",
    question=("다음 □ 안에 알맞은 수를 구하시오.\n"
              "[[pow((-frac(1,4)), 3) × pow(16, 2)]] − □ × {[[(-frac(1,3)) ÷ frac(1,9) - pow((-5), 2) × pow((frac(3,5)), 2)]]} = 8"),
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.9,
    note="(−1/64)·256=−4, 중괄호 안 −3−9=−12 → −4+12□=8 → □=1 = 빠른정답 ✓. 빈칸 □와 중괄호는 텍스트.")

# p55
add(id="a847d43b", qtype="short",
    question=("다음 □ 안에 알맞은 수를 구하시오.\n"
              "[[pow((-frac(1,2)), 3) × pow(2, 4)]] − □ × {[[(-frac(1,4)) ÷ frac(1,8) - pow((-3), 2) × pow((frac(4,3)), 2)]]} = 34"),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="(−1/8)·16=−2, 중괄호 안 −2−16=−18 → −2+18□=34 → □=2. 빠른정답 1과 불일치. 빈칸 □와 중괄호는 텍스트.")

# p75 (연산 상자 그림)
add(id="fcc0b4a7", qtype="short",
    question=("아래 그림은 가로로 덧셈식과 곱셈식, 세로로 뺄셈식과 나눗셈식을 나타낸 것이다. 다음 식을 계산하시오.\n"
              "(㉢)² − (㉠ × ㉡ + ㉠ ÷ ㉣)"),
    choices=None, derived_answer="frac(39,5)",
    figure=[{"fn": "unsupported", "args": {"raw": "상자 계산 그림(화살표로 방향 표시): 가로 윗줄 2/5 + ㉠ = −2, 가로 아랫줄 −1.8 × ㉣ = 2/3, 세로 왼쪽 2/5 − ㉡ = −1.8, 세로 오른쪽 −2 ÷ ㉢ = 2/3. 그 아래 상자에 (㉢)² − (㉠ × ㉡ + ㉠ ÷ ㉣)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 연산 상자 그림(가로·세로 계산식) / 원문자 기호 ㉠~㉣는 텍스트",
    note="㉠=−12/5, ㉡=11/5, ㉢=−3, ㉣=−10/27 → 9−(−132/25+162/25)=9−6/5=39/5 = 빠른정답 ✓.")

# ================= 반비례 =================
# p52 (좌표평면 그래프)
add(id="7d1b27e8", qtype="choice",
    question=("상수 [[a]], [[b]]에 대하여 정비례 관계 [[y = a x]]의 그래프와 반비례 관계 [[y = frac(b, x)]]의 그래프가 아래의 그림과 같을 때, "
              "다음 중 옳지 않은 것을 모두 고르면? (정답 2개)"),
    choices=["[[y = a x]]의 그래프는 [[x]]의 값이 증가하면 [[y]]의 값도 증가한다.",
             "[[y = frac(b, x)]]의 그래프는 [[x]]의 값이 증가하면 [[y]]의 값은 감소한다.",
             "[[a < 0]], [[b > 0]]이다.",
             "[[y = frac(a, x)]]의 그래프와 [[y = -b x]]는 만난다.",
             "[[y = -frac(2b, x)]]의 그래프는 [[y = frac(b, x)]]의 그래프보다 원점으로부터 더 멀다."],
    derived_answer="③, ④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(원점 O): 원점을 지나는 오른쪽 위로 향하는 직선(y=ax, a>0)과 제1·3사분면에 놓인 쌍곡선(y=b/x, b>0). 제1사분면에서 두 그래프가 만남"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 정비례·반비례 그래프",
    note="그림에서 a>0, b>0 → ③ 거짓, ④ y=a/x(1·3사분면)와 y=−bx(2·4사분면)는 만나지 않음 → 거짓 → ③, ④. 빠른정답 '2, 5'와 불일치.")

# p79 (좌표평면 그래프)
add(id="3e9c2eb1", qtype="short",
    question=("다음 그림과 같이 반비례 관계 [[y = frac(72, x)]] ([[x > 0]])의 그래프 위의 점 [[P(a, b)]]에서 [[x]]축, [[y]]축에 수직인 직선을 그어 "
              "[[x]]축, [[y]]축과 만나는 점을 각각 Q, R라 하자.\n서로 다른 직사각형 PROQ의 개수를 구하시오.\n"
              "(단, O는 원점이고 [[a]], [[b]]는 자연수이고 꼭짓점의 좌표가 다른 경우 다른 사각형으로 본다.)"),
    choices=None, derived_answer="12",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(원점 O): 제1사분면의 반비례 그래프 y=72/x, 그래프 위의 점 P(a, b), P에서 x축·y축에 내린 수선의 발 Q(x축)·R(y축), 직각 표시, 직사각형 PROQ"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 반비례 그래프와 직사각형",
    note="ab=72인 자연수 순서쌍 = 72의 약수 개수 12. 빠른정답 '- 2'와 불일치(정렬 어긋남으로 보임).")

# ================= 곱셈과 나눗셈 기호의 생략 =================
# p19
add(id="2638137b", qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["[[a × b × (-1) = -a b]]",
             "[[a × 3 × b × b × 4 = 12 a pow(b, 2)]]",
             "[[(-3) × (-x) × (-y) = -3x y]]",
             "[[0.1 × x × x]] = 0.[[pow(x, 2)]]",
             "[[(a - b) × 2 × x = 2(a - b) x]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="④ 0.1×x×x=0.1x² (0.x² 아님) → ④. 빠른정답 1과 불일치. ④의 '0.x²'는 텍스트 혼합.")

# p21
add(id="17ada7a9", qtype="choice",
    question="다음 중에서 곱셈 기호를 생략하여 나타낸 것으로 옳은 것은?",
    choices=["[[a × a × b = 2 a b]]",
             "[[x × y × 1 = 1 x y]]",
             "[[a × b × 0.1 = 0.1 a b]]",
             "[[x × y × 3 = x y 3]]",
             "[[a × b × c × (-1) = -1 a b c]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="① a²b ② xy ④ 3xy ⑤ −abc → ③ = 빠른정답 ✓.")

# p23
add(id="65ed64e6", qtype="choice",
    question="[[a ÷ (b ÷ 2c)]]를 나눗셈 기호를 생략하여 나타내면?",
    choices=["[[frac(a b, 2c)]]", "[[frac(a c, 2b)]]", "[[frac(2 a c, b)]]", "[[frac(a, 2 b c)]]", "[[frac(2c, a b)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="a÷(b÷2c)=a×2c/b=2ac/b → ③ = 빠른정답 ✓. 원문 'b÷2c'는 그대로 전사(2c는 한 덩어리).")

# p33
add(id="042549fa", qtype="choice",
    question="다음 중 옳은 것을 모두 고르면? (정답 2개)",
    choices=["[[y ÷ 5 = frac(y, 5)]]",
             "[[x ÷ (-y) = -frac(y, x)]]",
             "[[a ÷ b ÷ c = frac(a b, c)]]",
             "[[a ÷ (a + b) = frac(a + b, a)]]",
             "[[(x - y) ÷ 5 = frac((x - y), 5)]]"],
    derived_answer="①, ⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="② −x/y ③ a/(bc) ④ a/(a+b) → 옳은 것 ①, ⑤. 빠른정답 4와 불일치.")

# p34
add(id="7917bf1e", qtype="choice",
    question="다음 중 옳은 것은?",
    choices=["[[8 ÷ a = frac(a, 8)]]",
             "[[b ÷ (-frac(1,3)) = -3b]]",
             "[[(-frac(1, x)) ÷ (-frac(1, y)) = frac(1, x y)]]",
             "[[(-a) ÷ b = -a b]]",
             "[[(x - y) ÷ 3 = frac(1, 3(x - y))]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="① 8/a ③ y/x ④ −a/b ⑤ (x−y)/3 → ②. 빠른정답 4와 불일치.")

# p41
add(id="4bce1cfa", qtype="choice",
    question="식 [[a ÷ c ÷ 2b]]와 같은 것을 고르면?",
    choices=["[[frac(a c, 2b)]]", "[[frac(2 a b, c)]]", "[[frac(2 b c, a)]]", "[[frac(c, 2 a b)]]", "[[frac(a, 2 b c)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="a÷c÷2b=a/(2bc) → ⑤ = 빠른정답 ✓. 원문 '÷2b'는 그대로 전사(2b는 한 덩어리).")

# p45
add(id="d1262e76", qtype="choice",
    question="[[y ÷ (x + y) + z × (-1) ÷ x]]를 기호 ×, ÷를 생략하여 간단히 나타낸 것은?",
    choices=["[[frac(x, x + y) - x z]]", "[[frac(x, x + y) - frac(z, x)]]", "[[frac(y, x + y) - y z]]",
             "[[frac(y, x + y) - frac(z, x)]]", "[[frac(x, y + z) - frac(z, x)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="y/(x+y) − z/x → ④. 빠른정답 1과 불일치.")

# p50
add(id="05c8994a", qtype="choice",
    question="다음 중 옳은 것은?",
    choices=["[[a ÷ b ÷ c = frac(a b, c)]]",
             "[[a ÷ b × c = a ÷ b c]]",
             "[[a × (b ÷ c) = a ÷ (b ÷ c)]]",
             "[[a ÷ b ÷ c = a ÷ (b × c)]]",
             "[[a ÷ b ÷ c = a c ÷ b]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="a÷b÷c=a/(bc)=a÷(b×c) → ④ = 빠른정답 ✓.")

# p51
add(id="1089f348", qtype="choice",
    question="다음 중 곱셈, 나눗셈의 기호를 생략하여 나타낸 것으로 옳은 것은?",
    choices=["[[3 × y ÷ frac(1,2) = frac(3y, 2)]]",
             "[[x ÷ (y + 3) × 4 = frac(4x, y + 3)]]",
             "[[(x + y) ÷ 2 × z = frac(x + y, 2z)]]",
             "[[1 - x × y ÷ z = frac((1 - x) y, z)]]",
             "[[(-1) ÷ x + y × z = -x + y z]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="① 6y ③ (x+y)z/2 ④ 1−xy/z ⑤ −1/x+yz → ②. 빠른정답 5와 불일치.")

# p52
add(id="0a162352", qtype="choice",
    question="다음 중 기호 ×, ÷를 생략하여 나타낸 식 중 옳은 것은?",
    choices=["[[x ÷ (y - z) = frac(x, y) - frac(x, z)]]",
             "[[4x - x = 4]]",
             "[[0.1 × x]] = 0.[[x]]",
             "[[(-1) × (x + y) = -x + y]]",
             "[[a ÷ b ÷ c = frac(a, b c)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="① x/(y−z) ② 3x ③ 0.1x ④ −x−y → ⑤. 빠른정답 2와 불일치. ③의 '0.x'는 텍스트 혼합.")

# p57
add(id="8b53b413", qtype="choice",
    question="다음 중 기호 ×, ÷를 생략하여 나타낸 식으로 옳은 것을 모두 고르면? (정답 3개)",
    choices=["[[2 ÷ a × b = frac(2, a b)]]",
             "[[x ÷ y ÷ 3 = frac(x, 3y)]]",
             "[[a × (-5) ÷ b = frac(5a, b)]]",
             "[[a × 2 ÷ b = frac(2a, b)]]",
             "[[(-7) ÷ x × y = -frac(7y, x)]]"],
    derived_answer="②, ④, ⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="① 2b/a ③ −5a/b → 옳은 것 ②, ④, ⑤. 빠른정답 3과 불일치.")

# p61
add(id="9056a24d", qtype="choice",
    question="다음 중 기호 ×, ÷를 생략하여 나타낸 것으로 옳은 것은?",
    choices=["[[3 ÷ a - b = frac(a, 3) - b]]",
             "[[4 ÷ (x + y) = frac(4, x + y)]]",
             "[[4x ÷ frac(y, 2) = frac(y, 8x)]]",
             "[[(a + b) × (-2) = a - 2b]]",
             "[[x × (-9) + y ÷ 8 = -x y]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="① 3/a−b ③ 8x/y ④ −2a−2b ⑤ −9x+y/8 → ②. 빠른정답 1과 불일치.")

# p67
add(id="e4e5291d", qtype="choice",
    question="다음 중 [[frac(x z, y)]]를 기호 ×, ÷를 사용하여 바르게 나타낸 것은?",
    choices=["[[x ÷ y ÷ z]]", "[[(x ÷ y) ÷ z]]", "[[x ÷ frac(1, y) × z]]", "[[x ÷ (y × z)]]", "[[x ÷ y × z]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="x÷y×z=xz/y → ⑤ = 빠른정답 ✓.")

# p75
add(id="607ed764", qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["[[x ÷ 3 - (-1) × y ÷ frac(1,2) = frac(x, 3) + 2y]]",
             "[[x ÷ (-1) - 3 × y = -x - 3y]]",
             "[[x × (-y) + pow((-2), 2) × z = -x y - 4z]]",
             "[[x × x × (-2) - y ÷ (-3) = -2 pow(x, 2) + frac(y, 3)]]",
             "[[a - b × c ÷ 3 = a - frac(b c, 3)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="③ (−2)²z=+4z → −xy+4z이므로 옳지 않음 → ③. 빠른정답 5와 불일치.")

# ================= 수직선 =================
# p31 (수직선 도형)
add(id="477729e7", qtype="choice",
    question="다음 수직선 위에 점 A, B에 대응하는 수를 부호 +, −를 사용하여 바르게 나타낸 것은?",
    choices=["A: [[-frac(3,5)]], B: +[[frac(7,4)]]",
             "A: [[-frac(3,5)]], B: +[[frac(11,4)]]",
             "A: [[-frac(8,5)]], B: +[[frac(7,4)]]",
             "A: [[-frac(8,5)]], B: +[[frac(11,4)]]",
             "A: [[-1.3]], B: +[[2.3]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "수직선(양쪽 화살표), 눈금 −2, −1, 0, +1, +2, +3. −2와 −1 사이를 5등분(등간격 표시)하여 −2에서 두 칸 오른쪽에 점 A. +2와 +3 사이를 4등분(등간격 표시)하여 +2에서 세 칸 오른쪽에 점 B"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 등분 눈금이 있는 수직선 도형 / 선지의 부호 +는 텍스트",
    note="A=−2+2/5=−8/5, B=+2+3/4=+11/4 → ④. 빠른정답 2와 불일치.")

# ================= 일차식의 덧셈과 뺄셈 =================
# p27
add(id="391bd717", qtype="short",
    question="[[x = -4]], [[y = 3]]일 때,\n[[10x - 3(3x + 7y - (2x - y - (5x - 6y)))]]의 값을 구하시오.",
    choices=None, derived_answer="14", figure=None, difficulty_est=2, confidence=0.85,
    note="식 정리 −8x−6y → 32−18=14 (빠른정답 없음). 원문 대괄호 [ ]·중괄호 { }는 소괄호로.")

# p30 (★ 연산)
add(id="c0d134e4", qtype="short",
    question=("[[x]]에 대한 일차식 [[A]]에서 [[x]]의 계수는 [[-2]]이다.\n"
              "[[A]] ★ [[a]] = ([[x = a]]일 때, [[A]]의 식의 값)이라 할 때,\n"
              "[[A]] ★ [[(-1)]] + [[A]] ★ [[2]] − [[A]] ★ [[(-2)]] − [[A]] ★ [[5]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 연산 ★ → 텍스트 혼합 전사",
    note="A=−2x+c: (2+c)+(−4+c)−(4+c)−(−10+c)=4. 빠른정답 14와 불일치.")

# p32 (★ 연산)
add(id="c7632096", qtype="short",
    question=("[[x]]에 대한 일차식 [[A]]에서 [[x]]의 계수는 [[-5]]이다.\n"
              "[[A]] ★ [[a]] = ([[x = a]]일 때, [[A]]의 식의 값)이라 할 때,\n"
              "[[A]] ★ [[(-1)]] + [[A]] ★ [[3]] − [[A]] ★ [[(-5)]] − [[A]] ★ [[7]]의 값을 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 연산 ★ → 텍스트 혼합 전사",
    note="A=−5x+c: (5+c)+(−15+c)−(25+c)−(−35+c)=0 (빠른정답 없음).")

# p49
add(id="722ceff7", qtype="choice",
    question="다항식 [[4 pow(x, 2) - 5x + 3 + a pow(x, 2) + x + 1]]을 간단히 나타내었을 때, 이 다항식은 [[x]]에 대한 일차식이었다. [[a]]의 값은?",
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-1]]", "[[0]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="4+a=0 → a=−4 → ② = 빠른정답 ✓.")

# p51
add(id="d9547ad2", qtype="short",
    question="다항식 [[3(2 pow(x, 2) - x) + a pow(x, 2) + 5x - 6]]을 간단히 하였더니 [[x]]에 대한 일차식이 되었다. 이때 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="-6", figure=None, difficulty_est=1, confidence=0.9,
    note="6+a=0 → a=−6 (빠른정답 없음).")

# p56
add(id="dc9aad60", qtype="choice",
    question=("[[A = -3x + 5]], [[B = 2x + 7]]일 때, [[2A + B]]를 계산하였더니 [[a x + b]]가 되었다. "
              "상수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?"),
    choices=["[[7]]", "[[13]]", "[[17]]", "[[21]]", "[[25]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="2A+B=−4x+17 → a+b=13 → ② (빠른정답 없음).")

# p59 (★, ◎ 연산)
add(id="c3f5bc90", qtype="choice",
    question=("두 단항식 [[A]], [[B]]에 대하여 [[A]]★[[B]] = [[-A + 2B]],\n[[A]]◎[[B]] = [[-2A + 3B]]라 할 때,\n"
              "2{([[3x]])★[[y]]} − {[[x]]◎([[-y]])}를 계산한 것은?"),
    choices=["[[-4x + 5y]]", "[[-4x + 7y]]", "[[-4x + 9y]]", "[[-2x + 5y]]", "[[-2x + 7y]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 연산 ★, ◎ → 텍스트 혼합 전사(중괄호는 텍스트)",
    note="(3x)★y=−3x+2y, x◎(−y)=−2x−3y → 2(−3x+2y)−(−2x−3y)=−4x+7y → ② (빠른정답 없음).")

# p60 (◉, ▼ 연산)
add(id="b4aaf009", qtype="short",
    question=("두 단항식 [[A]], [[B]]에 대하여 ([[A]]◉[[B]]) = [[4A - 3B]],\n([[A]]▼[[B]]) = [[B - 2A]]라 할 때, "
              "2([[2x]]◉[[y]]) − ([[x]]▼[[3y]])를 계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱을 구하시오."),
    choices=None, derived_answer="-162", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 연산 ◉, ▼ → 텍스트 혼합 전사",
    note="2x◉y=8x−3y, x▼3y=3y−2x → 18x−9y → 18×(−9)=−162 (빠른정답 없음).")

# p61 (★, ◎ 연산)
add(id="b3b71280", qtype="short",
    question=("두 단항식 [[A]], [[B]]에 대하여 ([[A]]★[[B]]) = [[3A - frac(1,2) B]],\n([[A]]◎[[B]]) = [[2B - A]]라 할 때,\n"
              "2{([[x + 2y]])★([[3y - x]])} + {([[x - y]])◎([[2x + 3y]])}를 계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱을 구하시오."),
    choices=None, derived_answer="160", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 연산 ★, ◎ → 텍스트 혼합 전사(중괄호는 텍스트)",
    note="(x+2y)★(3y−x)=7x/2+9y/2 → ×2=7x+9y; (x−y)◎(2x+3y)=3x+7y → 10x+16y → 160 (빠른정답 없음).")

# p62 (◎, ◆ 연산)
add(id="ec503ead", qtype="choice",
    question=("두 단항식 [[A]], [[B]]에 대하여 ([[A]]◎[[B]]) = [[3A - 2B]],\n([[A]]◆[[B]]) = [[B - A]]라 할 때, "
              "2([[x]]◎[[3y]]) − ([[2x]]◆[[y]])를 계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱은?"),
    choices=["[[-120]]", "[[-104]]", "[[-91]]", "[[91]]", "[[104]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 연산 ◎, ◆ → 텍스트 혼합 전사",
    note="x◎3y=3x−6y, 2x◆y=y−2x → 8x−13y → −104 → ② (빠른정답 없음).")

# ================= 소인수분해를 이용하여 약수 구하기 =================
# p37 (⟨a⟩, {a} 기호)
add(id="41ffd03a", qtype="short",
    question=("자연수 [[a]]의 약수의 개수를 ⟨[[a]]⟩, 자연수 [[a]]의 모든 약수의 합을 {[[a]]}라 하자. "
              "⟨[[72]]⟩ = [[x]], {[[x]]} = [[y]]일 때, [[x + y]]의 값을 구하시오."),
    choices=None, derived_answer="40", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 기호 ⟨a⟩, {a} → 텍스트 혼합 전사",
    note="72=2³·3² → x=12, 12의 약수 합 28 → 40. 빠른정답 3과 불일치.")

# p81
add(id="b0765e24", qtype="choice",
    question="[[12]] × □의 약수의 개수가 12일 때, 다음 중 □ 안에 들어갈 수 없는 수는?",
    choices=["[[6]]", "[[8]]", "[[9]]", "[[13]]", "[[15]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="72,96,108,156은 약수 12개, 180=2²·3²·5는 18개 → ⑤. 빠른정답 2와 불일치. 빈칸 □는 텍스트.")

# p84
add(id="862f5a9a", qtype="choice",
    question="[[A = pow(3, 5)]] × □의 약수가 18개일 때, □ 안에 들어갈 수 있는 가장 작은 자연수는?",
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="3⁵·2²: 6·3=18 → 4가 최소 → ②. 빠른정답 5와 불일치. 빈칸 □는 텍스트.")

# p96
add(id="914aa9e6", qtype="choice",
    question="[[pow(2, 3)]] × □의 약수의 개수가 8일 때, 다음 중 □ 안에 들어갈 수 없는 수를 모두 고르면? (정답 2개)",
    choices=["[[3]]", "[[4]]", "[[7]]", "[[9]]", "[[16]]"],
    derived_answer="②, ④", figure=None, difficulty_est=2, confidence=0.9,
    note="2³·3, 2³·7, 2⁷은 8개; 2⁵은 6개, 2³·3²은 12개 → ②, ④. 빠른정답 7과 불일치. 빈칸 □는 텍스트.")
