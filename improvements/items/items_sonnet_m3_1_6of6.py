# -*- coding: utf-8 -*-
# esc_sonnet_m3-1_6of6 — 이미지 기준 전사 (45 항목 / 45쪽)
# 다항식과 다항식의 곱셈 · 이차함수 y=ax²의 그래프 · 제곱근을 이용한 이차방정식의 풀이 · 무리수와 실수 · 인수분해
# 규약: 빈칸 상자(□, ⓐⓑ, ㉠㉡)는 마커 밖 텍스트. 과정 상자는 텍스트(figure=None). 이차함수 그래프·분류 수형도는 unsupported + "도형 표현 불가" 한 구절.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))
def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
def M(*xs): return ["[[%s]]" % x for x in xs]
FIG = "도형 표현 불가: "
TREE = "실수 { 유리수 { 정수 { 양의 정수(자연수), 0, 음의 정수 }, 정수가 아닌 유리수 }, □ }"
TREE_RAW = "실수의 분류 수형도(상자): 실수 → 유리수·□(빈칸), 유리수 → 정수·정수가 아닌 유리수, 정수 → 양의 정수(자연수)·0·음의 정수. 빈칸 □은 유리수 아래 가지"
TREE2 = "실수 { 유리수, □ }"
TREE2_RAW = "실수의 분류(상자): 실수 → 유리수·□(빈칸). 빈칸 □은 유리수 아래 가지"

# ======================================================================
# 다항식과 다항식의 곱셈
# ======================================================================
# ---------------- p81
add(id="1c482cea", qtype="choice",
    question="[[(3x + a y - 2)(2x - y + 4)]]를 전개하면 상수항을\n제외한 각 항의 계수의 총합이 8이다. 이때, [[a]]의 값은?",
    choices=M("-3", "-1", "0", "1", "3"), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="상수항 제외 계수합 13+5a=8 → a=−1 → ② = 빠른정답 ✓.")

# ---------------- p90
add(id="1e331839", qtype="short",
    question="[[(3x + y)(k x + 2y)]]를 전개한 식에서 [[pow(x,2)]]의 계수와 [[x y]]의\n계수가 같을 때, 상수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="x² 계수 3k, xy 계수 6+k → 3k=6+k → k=3. 빠른정답 −19와 불일치.")

# ---------------- p91
add(id="bf7ac700", qtype="short",
    question="[[(4x + y)(k x + 6y)]]를 전개한 식에서 [[pow(x,2)]]의 계수와 [[x y]]의\n계수가 같을 때, 상수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="4k=24+k → k=8 = 빠른정답 ✓.")

# ---------------- p92
add(id="3e89f2e3", qtype="choice",
    question="[[(x + A y)(4x - y + 1)]]의 전개식에서 [[x y]]의 계수가 [[x]]의\n계수보다 6만큼 클 때, 상수 [[A]]의 값은?",
    choices=M("1", "2", "3", "4", "5"), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="xy 계수 4A−1, x 계수 1 → 4A−1=7 → A=2 → ②. 빠른정답 252와 불일치.")

# ---------------- p93
add(id="2b47b5db", qtype="choice",
    question="[[(x + A y)(3x - y + 5)]]의 전개식에서 [[x y]]의 계수가 [[x]]의\n계수보다 3만큼 클 때, 상수 [[A]]의 값은?",
    choices=M("1", "2", "3", "4", "5"), derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="xy 계수 3A−1, x 계수 5 → 3A−1=8 → A=3 → ③ = 빠른정답 ✓.")

# ---------------- p94
add(id="b827bf43", qtype="short",
    question="[[(x - 4y + 3)(x + a y - b)]]의 전개식에서 [[x y]]의 계수와\n[[y]]의 계수가 모두 [[-2]]일 때, [[a b]]의 값을 구하시오.\n(단, [[a]], [[b]]는 상수)",
    choices=None, derived_answer="-4", figure=None, difficulty_est=2, confidence=0.9,
    note="xy 계수 a−4=−2 → a=2, y 계수 4b+3a=−2 → b=−2 → ab=−4. 빠른정답 8과 불일치.")

# ---------------- p95
add(id="00785ed9", qtype="choice",
    question="[[(2x - 3)(pow(x,2) + a x + a) - (pow(x,2) - 2)(x + 1)]]의 전개식에서\n[[x]]의 계수가 4일 때, 상수항은? (단, [[a]]는 상수이다.)",
    choices=M("7", "8", "9", "10", "11"), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="x 계수 −a+2=4 → a=−2, 상수항 −3a+2=8 → ② = 빠른정답 ✓.")

# ---------------- p96
add(id="6c92bb41", qtype="choice",
    question="[[(2x - 5)(pow(x,2) + a x + a) - (pow(x,2) + 1)(x + 1)]]의 전개식에서\n[[x]]의 계수가 5일 때, 상수항은? (단, [[a]]는 상수이다.)",
    choices=M("7", "9", "11", "13", "15"), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="x 계수 −3a−1=5 → a=−2, 상수항 −5a−1=9 → ②. 빠른정답 3과 불일치.")

# ======================================================================
# 이차함수 y=ax²의 그래프
# ======================================================================
# ---------------- p72
add(id="2b457dce", qtype="short",
    question="다음 그림과 같이 이차함수 [[y = a pow(x,2)]]의 그래프 위에\n네 점 A, B, C, D가 있다. [[A(-2, 1)]], [[B(2, 1)]]이고\n[[seg(AB)]]에 평행한 [[seg(CD)]]의 길이가 20일 때, 사다리꼴 ABCD의\n넓이를 구하시오.",
    choices=None, derived_answer="288",
    figure=U("좌표평면: 아래로 볼록한 포물선(원점 O), 포물선 위의 네 점 A(왼쪽 아래)·B(오른쪽 아래)·C(오른쪽 위)·D(왼쪽 위), 사다리꼴 ABCD 색칠(보라), x축에 −2·2, y축에 1 표시, D–C 가로선"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "이차함수 그래프 위 사다리꼴 ABCD",
    note="a=1/4, C(10, 25), D(−10, 25) → (4+20)×24/2=288 = 빠른정답 ✓.")

# ---------------- p77
add(id="be1de7d6", qtype="short",
    question=("이차함수 [[y = frac(1,3) pow(x,2)]] ([[x >= 0]])의 그래프와 직선 [[x]] = 1, 2,\n3, ⋯, [[n]]에 대하여 다음 그림처럼 색칠하여 나타낸 [[n]]개의\n"
              "직사각형 전부를 도형 A라 한다. 두 직선 [[x = n]],\n[[y = frac(1,3) pow(n,2)]]과 [[x]]축, [[y]]축으로 둘러싸인 직사각형\n"
              "OQPR에서 도형 A를 제외한 부분의 넓이가 1050일 때,\n자연수 [[n]]의 값을 구하시오."),
    choices=None, derived_answer="15",
    figure=U("좌표평면: y=(1/3)x² (x≥0) 곡선, 직선 x=1,2,3,…,n 사이에 곡선을 가로지르는 직사각형 n개 색칠(분홍), 직사각형 OQPR(O 원점, Q(n, 0), P(n, (1/3)n²), R(0, (1/3)n²)) 점선, x축에 1·2·3·n−1·n, y축에 1/3·4/3·3·(1/3)n² 표시, 축 중간에 물결 생략 기호"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "이차함수 그래프와 계단형 직사각형 n개",
    note="k번째 직사각형 넓이 (2k−1)/3, 합 n²/3; n³/3−n²/3=1050 → n²(n−1)=3150 → n=15 = 빠른정답 ✓.")

# ---------------- p80
add(id="7391dbfa", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]]이 이차함수 [[y = frac(1,5) pow(x,2)]]의 그래프\n및 [[y]]축과 각각 두 점 A, B와 점 C에서 만난다. 점 C가\n"
              "직선 [[y = 1]] 위에 있고 [[ratio(seg(AC), seg(CB)) = ratio(1, 5)]]일 때, 직선 [[l]]의\n기울기는?"),
    choices=M("frac(3,5)", "frac(7,10)", "frac(4,5)", "frac(9,10)", "1"), derived_answer="③",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=(1/5)x²(원점 O), 오른쪽 위로 향하는 직선 l이 포물선과 A(y축 왼쪽, x축 부근)·B(오른쪽 위)에서 만나고 y축과 C(x축 바로 위)에서 만남"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "이차함수 그래프와 직선 l의 교점 A, B, C",
    note="C(0,1), A(−p, p²/5), B(5p, 5p²)에서 p²=1 → A(−1, 1/5), B(5, 5) → 기울기 4/5 → ③ = 빠른정답 ✓.")

# ======================================================================
# 제곱근을 이용한 이차방정식의 풀이
# ======================================================================
# ---------------- p3
add(id="322bbd59", qtype="short",
    question="[[alpha > 0]], [[beta > 0]]일 때, 이차방정식 [[9 pow(x - 5, 2) = pow(beta, 2)]]의 해가\n[[x = 3]] 또는 [[x = alpha]]이다. 이때 [[alpha + beta]]의 값을 구하시오.",
    choices=None, derived_answer="13", figure=None, difficulty_est=2, confidence=0.9,
    note="x=5±β/3, 5−β/3=3 → β=6, α=7 → 13 = 빠른정답 ✓.")

# ---------------- p8
add(id="d49358cd", qtype="short",
    question="이차방정식 [[pow(x - 2, 2) = 4A]]의 해가\n[[x = pm(2, sqrt(28))]]일 때, 유리수 [[A]]의 값을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="4A=28 → A=7. 빠른정답 1과 불일치.")

# ---------------- p15 (과정 상자)
add(id="6da9fb17", qtype="short",
    question="다음은 제곱근을 이용하여 이차방정식의 해를 구하는\n과정이다. □ 안에 알맞은 수를 쓰시오.\n[[pow(x,2) = 9]]  ∴ [[x]] = ±□",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="x=±3 → □=3. 빠른정답 4와 불일치. 빈칸 상자는 텍스트.")

# ---------------- p17
add(id="126ab5ab", qtype="choice",
    question="이차방정식 [[pow(x - 2, 2) - 5 = 0]]을 풀면?",
    choices=["[[x = 2]] 또는 [[x = -5]]", "[[x = pm(2, sqrt(5))]]", "[[x = pm(-2, sqrt(5))]]", "[[x = pm(2, frac(sqrt(3), 2))]]", "[[x = 2]] 또는 [[x = 5]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="(x−2)²=5 → x=2±√5 → ② = 빠른정답 ✓.")

# ---------------- p18
add(id="79f4540e", qtype="choice",
    question="이차방정식 [[2 pow(x + 3, 2) - 12 = 0]]의 근을\n[[x = pm(a, sqrt(b))]]라고 할 때, [[a]], [[b]]의 값을 구하면?",
    choices=["[[a = -3]], [[b = 3]]", "[[a = 3]], [[b = 3]]", "[[a = -3]], [[b = -3]]", "[[a = -3]], [[b = 6]]", "[[a = 3]], [[b = 6]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="(x+3)²=6 → x=−3±√6 → a=−3, b=6 → ④. 빠른정답 3과 불일치.")

# ---------------- p24
add(id="31d70113", qtype="choice",
    question="이차방정식 [[49 pow(x,2) - 6 = 0]]을 풀면?",
    choices=M("pm(sqrt(frac(6,7)))", "pm(frac(sqrt(2), 7))", "pm(frac(sqrt(3), 7))", "pm(frac(sqrt(6), 7))", "pm(frac(6,7))"),
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="x²=6/49 → x=±√6/7 → ④ = 빠른정답 ✓.")

# ---------------- p25
add(id="88278586", qtype="choice",
    question="다음 이차방정식 중 해가 [[x = pm(-5, sqrt(3))]]인 것은?",
    choices=M("pow(x + 1, 2) = 3", "pow(x + 2, 2) = 4", "pow(x - 3, 2) = 5", "pow(x + 5, 2) = 3", "pow(x - 5, 2) = 10"),
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="(x+5)²=3 → ④ = 빠른정답 ✓.")

# ---------------- p26
add(id="8a4f0cf1", qtype="choice",
    question="다음 중 이차방정식과 그 해를 나타낸 것으로 옳지 않은\n것은?",
    choices=["[[pow(x,2) - 16 = 0]], [[x = pm(4)]]",
             "[[pow(x + 2, 2) = 36]], [[x = -8]] 또는 [[x = 4]]",
             "[[25 - 9 pow(x,2) = 0]], [[x = pm(frac(5,3))]]",
             "[[4 pow(x - 1, 2) = 100]], [[x = -9]] 또는 [[x = 11]]",
             "[[3 pow(x + 4, 2) - 6 = 0]], [[x = pm(-4, sqrt(2))]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="④ (x−1)²=25 → x=−4 또는 6이어야 함 → ④ = 빠른정답 ✓.")

# ---------------- p27
add(id="5f14ec39", qtype="choice",
    question="이차방정식 [[4 pow(x,2) - 15 = 0]]을 풀면?",
    choices=M("x = pm(sqrt(3))", "x = pm(frac(sqrt(13), 2))", "x = pm(frac(sqrt(14), 2))", "x = pm(frac(sqrt(15), 2))", "x = pm(2)"),
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="x²=15/4 → x=±√15/2 → ④ = 빠른정답 ✓.")

# ---------------- p29
add(id="1f67c5b5", qtype="choice",
    question="이차방정식 [[16 pow(x,2) - 49 = 0]]을 풀면?",
    choices=M("x = pm(frac(3,2))", "x = pm(frac(7,4))", "x = pm(2)", "x = pm(frac(9,4))", "x = pm(frac(5,2))"),
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="x²=49/16 → x=±7/4 → ②. 빠른정답 4와 불일치.")

# ---------------- p30
add(id="5cc0cc68", qtype="choice",
    question="이차방정식 [[5 pow(x,2) - 11 = 0]]을 풀면?",
    choices=M("x = pm(frac(sqrt(11), 10))", "x = pm(frac(sqrt(11), 5))", "x = pm(frac(sqrt(55), 10))", "x = pm(frac(sqrt(55), 5))", "x = pm(sqrt(55))"),
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="x²=11/5 → x=±√55/5 → ④ = 빠른정답 ✓.")

# ---------------- p33
add(id="01c67e66", qtype="choice",
    question="이차방정식 [[3 pow(x + 2, 2) - 15 = 0]]의 해가\n[[x = pm(A, sqrt(B))]]일 때, [[A + B]]의 값은?\n(단, [[A]], [[B]]는 유리수)",
    choices=M("1", "3", "4", "5", "7"), derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="(x+2)²=5 → x=−2±√5 → A+B=3 → ②. 빠른정답 4와 불일치.")

# ---------------- p35 (과정 상자)
add(id="3e78eaaf", qtype="choice",
    question="다음 ⓐ, ⓑ에 알맞은 수를 차례대로 쓴 것은?\n[[2 pow(x,2) - 72 = 0]]에서 [[pow(x,2)]] = ⓐ\n∴ [[x]] = ⓑ",
    choices=["[[36]], [[-6]]", "[[36]], [[6]]", "[[36]], [[pm(6)]]", "[[72]], [[-6 sqrt(2)]]", "[[72]], [[6 sqrt(2)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="x²=36, x=±6 → ③. 빠른정답 5와 불일치. 빈칸 ⓐⓑ는 텍스트.")

# ---------------- p39
add(id="b29522b4", qtype="short",
    question="이차방정식 [[frac(pow(x - 2, 2), 5) = 1]]의 해가 [[x = pm(a, sqrt(b))]]일 때,\n유리수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="(x−2)²=5 → x=2±√5 → a+b=7 = 빠른정답 ✓.")

# ---------------- p45
add(id="15da149f", qtype="short",
    question="이차방정식 [[4 pow(x - b, 2) - 20 = 0]]의 근이 [[x = pm(2, sqrt(a))]]일\n때, [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="(x−b)²=5 → x=b±√5 → b=2, a=5 → 7. 빠른정답 −2와 불일치.")

# ---------------- p47
add(id="82b8d9eb", qtype="choice",
    question="이차방정식 [[pow(x + a, 2) = b]]의 해가 [[x = pm(-3, sqrt(2))]]일 때,\n상수 [[a]], [[b]]에 대하여 [[a - b]]의 값은? (단, [[b > 0]])",
    choices=M("1", "2", "3", "4", "5"), derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="x=−a±√b → a=3, b=2 → a−b=1 → ① = 빠른정답 ✓.")

# ======================================================================
# 무리수와 실수
# ======================================================================
# ---------------- p35
add(id="f1d6afd4", qtype="choice",
    question="다음 중 옳은 것은?",
    choices=["0을 제외한 모든 수의 제곱근은 2개이다.",
             "[[sqrt(pow(-4, 2))]]의 제곱근은 [[pm(2)]]이다.",
             "[[sqrt(9) + sqrt(16) = sqrt(9 + 16)]]이다.",
             "[[2 sqrt(3) = sqrt(6)]]이다.",
             "[[pi]]는 유리수이다."],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="①✗(음수), ② √16=4의 제곱근 ±2 ✓, ③ 7≠5 ✗, ④ √12≠√6 ✗, ⑤✗ → ②. 빠른정답 없음.")

# ---------------- p68 (분류 수형도)
add(id="643a680b", qtype="choice",
    question="다음 중 □ 안에 해당하는 수가 아닌 것은?\n" + TREE,
    choices=["[[sqrt(5) + 1]]", "[[-frac(pi, 2)]]", "[[sqrt(0.9)]]", "[[-sqrt(2.89)]]", "[[0.1234]]⋯"],
    derived_answer="④", figure=U(TREE_RAW), difficulty_est=1, confidence=0.85,
    needs_review=FIG + "실수의 분류 수형도(빈칸 □)",
    note="□=무리수. −√2.89=−1.7 유리수 → ④. 빠른정답 없음. 수형도는 텍스트로 병기.")

# ---------------- p69 (분류 수형도)
add(id="ac8904ff", qtype="choice",
    question="다음 중 □ 안의 수에 해당하는 것은?\n" + TREE,
    choices=M("sqrt(25)", "sqrt(frac(16,4))", "frac(3, sqrt(9))", "sqrt(1.6)", "5 - sqrt(4)"),
    derived_answer="④", figure=U(TREE_RAW), difficulty_est=1, confidence=0.85,
    needs_review=FIG + "실수의 분류 수형도(빈칸 □)",
    note="□=무리수. √1.6만 무리수 → ④. 빠른정답 없음. 수형도는 텍스트로 병기.")

# ---------------- p70 (분류 상자)
add(id="f0a1307b", qtype="choice",
    question="다음 중 아래 □ 안의 수에 해당하는 것만으로 짝 지어진\n것은?\n" + TREE2,
    choices=["[[0]], [[sqrt(3)]], [[sqrt(5)]]",
             "[[-sqrt(9)]], [[sqrt(7)]], [[pi]]",
             "[[sqrt(recdec(0,4))]], [[sqrt(2)]], [[sqrt(10)]]",
             "[[sqrt(0.4)]], [[sqrt(11)]], [[3 pi]]",
             "[[sqrt(frac(1,25))]], [[sqrt(15)]], [[5 pi]]"],
    derived_answer="④", figure=U(TREE2_RAW), difficulty_est=1, confidence=0.85,
    needs_review=FIG + "실수의 분류 상자(빈칸 □)",
    note="□=무리수. ① 0, ② −√9=−3, ③ √(4/9)=2/3, ⑤ 1/5 유리수 → ④. 빠른정답 2와 불일치. ③의 0.4̇는 recdec(0,4).")

# ---------------- p72 (분류 상자)
add(id="a4d2c4c6", qtype="choice",
    question="다음 중 아래 □ 안의 수에 해당하는 것만으로 짝 지어진\n것은?\n" + TREE2,
    choices=["[[-4.1]], [[sqrt(2)]], [[sqrt(3)]]",
             "[[-sqrt(4)]], [[sqrt(5)]], [[pi]]",
             "[[sqrt(recdec(0,1))]], [[sqrt(6)]], [[sqrt(31)]]",
             "[[sqrt(0.09)]], [[sqrt(13)]], [[2 pi]]",
             "[[sqrt(frac(1,47))]], [[sqrt(14)]], [[4 pi]]"],
    derived_answer="⑤", figure=U(TREE2_RAW), difficulty_est=1, confidence=0.85,
    needs_review=FIG + "실수의 분류 상자(빈칸 □)",
    note="□=무리수. ① −4.1, ② −2, ③ √(1/9)=1/3, ④ 0.3 유리수 → ⑤. 빠른정답 없음. ③의 0.1̇은 recdec(0,1).")

# ---------------- p73 (분류 수형도 + 보기)
add(id="debefb3f", qtype="short",
    question=("다음 보기 중 □ 안의 수에 해당하는 것의 개수를\n구하시오.\n" + TREE + "\n<보기>\n"
              "[[1 + sqrt(16)]], [[-sqrt(11) - 5]], [[frac(pi, 3)]], [[sqrt(pow(-121, 2))]], [[sqrt(0.25)]]"),
    choices=None, derived_answer="2", figure=U(TREE_RAW), difficulty_est=1, confidence=0.85,
    needs_review=FIG + "실수의 분류 수형도(빈칸 □)",
    note="□=무리수. −√11−5, π/3의 2개 = 빠른정답 ✓. 수형도는 텍스트로 병기.")

# ---------------- p75 (분류 수형도 + 보기)
add(id="fa5d22c5", qtype="short",
    question=("다음 보기 중 □ 안의 수에 해당하는 것의 개수를\n구하시오.\n" + TREE + "\n<보기>\n"
              "[[sqrt(recdec(1,4))]], [[-sqrt(6) + 1]], [[sqrt(pow(-1.1, 2))]], [[frac(pi, 5)]], [[2 + sqrt(81)]]"),
    choices=None, derived_answer="3", figure=U(TREE_RAW), difficulty_est=1, confidence=0.85,
    needs_review=FIG + "실수의 분류 수형도(빈칸 □)",
    note="□=무리수. √(13/9), −√6+1, π/5의 3개(√1.21=1.1, 2+9=11 유리수). 빠른정답 없음. 1.4̇는 recdec(1,4).")

# ======================================================================
# 인수분해
# ======================================================================
# ---------------- p29
add(id="33a91e83", qtype="short",
    question="[[(2x + 3)(3x + 1)]]은 [[a pow(x,2) + b x + c]]를 인수분해 한\n것이다. [[a + b + c]]의 값을 구하여라.",
    choices=None, derived_answer="20", figure=None, difficulty_est=1, confidence=0.9,
    note="6x²+11x+3 → 20. 빠른정답 3과 불일치.")

# ---------------- p31
add(id="9d5bb761", qtype="short",
    question="[[2(x + 3)(2x + 5)]]은 [[a pow(x,2) + b x + c]]를 인수분해 한\n것이다. [[a + b + c]]의 값을 구하여라.",
    choices=None, derived_answer="56", figure=None, difficulty_est=1, confidence=0.9,
    note="4x²+22x+30 → 56 = 빠른정답 ✓.")

# ---------------- p34
add(id="bdb280ac", qtype="choice",
    question="[[(x + 2)(x - 6)]]은 [[a pow(x,2) + b x + c]]를 인수분해한 것이다.\n[[a + b + c]]의 값을 구하면? (단, [[a]], [[b]], [[c]]는 상수)",
    choices=M("-15", "-10", "-5", "0", "5"), derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="x²−4x−12 → −15 → ①. 빠른정답 56과 불일치.")

# ---------------- p42 (화살표 상자)
add(id="690200e9", qtype="choice",
    question="다음 식에 대한 설명 중 옳지 않은 것은?\n[[3 pow(x,2) y - 9 x y]] ⇄ [[3 x y(x - 3)]] (오른쪽 방향 화살표: ㉠, 왼쪽 방향 화살표: ㉡)",
    choices=["㉠의 과정을 인수분해한다고 한다.",
             "㉡의 과정을 전개한다고 한다.",
             "[[3 pow(x,2) y]], [[-9 x y]]의 공통인수는 [[3 pow(x,2) y]]이다.",
             "㉡의 과정에서 분배법칙이 이용된다.",
             "[[3x]], [[x y]], [[3(x - 3)]]은 모두 [[3 x y(x - 3)]]의 인수이다."],
    derived_answer="③", figure=U("상자 안: 3x²y − 9xy ⇄ 3xy(x − 3), 오른쪽 방향 화살표(위)에 ㉠, 왼쪽 방향 화살표(아래)에 ㉡"),
    difficulty_est=1, confidence=0.85,
    note="공통인수는 3xy → ③. 빠른정답 5와 불일치. 화살표 ㉠㉡는 텍스트.")

# ---------------- p44
add(id="a8353383", qtype="choice",
    question="[[3x(x - 2y) - x + 2y]]를 인수분해한 것은?",
    choices=M("(3x - 1)(x - 2y)", "(3x + 1)(x + 2y)", "(3x - 2y)(x + y)", "(3x - 2y)(x - 1)", "(3x + 2y)(x - 1)"),
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="3x(x−2y)−(x−2y)=(3x−1)(x−2y) → ①. 빠른정답 2와 불일치.")

# ---------------- p50
add(id="54c78eac", qtype="choice",
    question="[[(3x - y)(y + 1) - x(y - 3x)]]가 [[x]]의 계수가 자연수인 두\n일차식의 곱으로 인수분해될 때, 두 일차식의 합은?",
    choices=M("2x + 1", "4x + 1", "2x + 2y - 1", "3x + y + 1", "4x - 2y + 1"),
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(3x−y)(x+y+1) → 합 4x+1 → ②. 빠른정답 4와 불일치.")

# ---------------- p52
add(id="2079097a", qtype="choice",
    question="[[a(x - 2) + b(2 - x)]]를 인수분해하면?",
    choices=M("(a - b)(x - 1)", "(a - b)(x + 1)", "(a - b)(x - 2)", "(b - a)(x - 2)", "(a - b)(x + 2)"),
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="(a−b)(x−2) → ③ = 빠른정답 ✓.")

# ---------------- p53
add(id="d62e9e8d", qtype="choice",
    question="[[-a(x - 1) - b(1 - x)]]를 인수분해하면?",
    choices=M("(a - b)(x - 1)", "(b - a)(x - 1)", "(a - b)(x + 1)", "(a - b)(x - 2)", "(b - a)(x + 2)"),
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="(b−a)(x−1) → ② = 빠른정답 ✓.")

# ---------------- p54
add(id="65b9b0ad", qtype="choice",
    question="[[a(3 - x) + b(x - 3)]]을 인수분해하면?",
    choices=M("(a - b)(x - 3)", "(b - a)(x - 3)", "(a - b)(x + 3)", "(b - a)(x - 6)", "(a - b)(x + 6)"),
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="(b−a)(x−3) → ②. 빠른정답 4와 불일치.")

# ---------------- p71
add(id="e67261e1", qtype="choice",
    question="다음 중 [[2 pow(a,3) b - 6 pow(a,2) pow(b,2) + 2 pow(b,3)]]에서 각 항의 공통인수는?",
    choices=M("2 a b", "2 pow(a,2) b", "2b", "2a", "2 pow(a,2) pow(b,2)"),
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="공통인수 2b → ③ = 빠른정답 ✓.")

# ---------------- p73 (빈칸 상자)
add(id="f1f56f28", qtype="short",
    question="다음 □ 안에 알맞은 것을 써넣으시오.\n[[30 pow(x,2) + 6x]] = □[[(5x + 1)]]",
    choices=None, derived_answer="6x", figure=None, difficulty_est=1, confidence=0.9,
    note="30x²+6x=6x(5x+1) → 6x = 빠른정답 ✓. 빈칸 상자는 텍스트.")
