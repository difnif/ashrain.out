# -*- coding: utf-8 -*-
# esc_sonnet_m3-1_5of6 — 이미지 기준 전사 (80 항목 / 80쪽) — 중3-1 제곱근·다항식의 곱셈·이차함수의 활용
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

REV_FIG = "도형 표현 불가: "

# ====================================================================
# 제곱근의 뜻과 성질
# ====================================================================

# p2
add(id="2c953734", qtype="choice",
    question="[[pow(a,2) = 17]]일 때, [[a]]의 값을 모두 구한 것은?",
    choices=["[[sqrt(17)]]", "[[-sqrt(17)]]", "[[pm(sqrt(17))]]", "[[-17]]", "+[[17]]"],
    derived_answer="③", figure=None, difficulty_est=1,
    note="17의 제곱근 ±√17 → ③ = 빠른정답 ✓. 선지 ⑤의 +17은 단항 + 를 텍스트로 둠.")

# p7
add(id="4633b61b", qtype="choice",
    question="[[x > 0]]이고 [[x]]의 음의 제곱근이 [[a]]일 때, 다음 중 옳은 것은?",
    choices=["[[pow(a,2) = x]]", "[[x = sqrt(a)]]", "[[pow(x,2) = a]]", "[[x = -sqrt(a)]]", "[[a = sqrt(x)]]"],
    derived_answer="①", figure=None, difficulty_est=1,
    note="a=−√x ⇒ a²=x → ① = 빠른정답 ✓.")

# p21 (제곱근 나선 도형)
add(id="18240e69", qtype="short",
    question="다음 그림에서 [[seg(OA) = 1]], [[seg(AB) = 1]]일 때, [[seg(OF)]]의 길이를 구하시오.",
    choices=None, derived_answer="sqrt(6)",
    figure=[{"fn": "unsupported", "args": {"raw": "점 O를 공통 꼭짓점으로 직각삼각형을 잇달아 붙인 도형: OA=1, AB=1(∠A 직각), 이어서 B, C, D, E에서 직각 표시(변 BC, CD, DE, EF), 점선 호 위에 OB=√2, OC=√3, OD=√4, OE=√5 표시, OF=x"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형을 잇달아 붙인 제곱근 나선 도형",
    note="OB=√2, OC=√3, OD=√4, OE=√5(그림 표기) → OF=√6. 빠른정답 3과 불일치.")

# p25
add(id="56998b0d", qtype="short",
    question=("다음 그림과 같이 [[seg(AC) = 3]] cm, [[seg(BC) = 4]] cm, [[angle(C) = deg(90)]]인 직각삼각형 ABC에서 빗변 AB의 중점을 M, "
              "점 C에서 [[seg(AB)]]에 내린 수선의 발을 D라 할 때, [[tri(CDM)]]의 넓이를 구하시오."),
    choices=None, derived_answer="frac(21,25) cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(∠C=90°, A 위, B 왼쪽 아래, C 오른쪽 아래, AC=3 cm, BC=4 cm), 빗변 AB 위의 중점 M과 C에서 내린 수선의 발 D(직각 표시), △CDM 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·중점·수선의 발 도형",
    note="AB=5, CD=12/5, AD=9/5, AM=5/2 → DM=7/10 → △CDM=½·(7/10)·(12/5)=21/25 cm². 빠른정답 없음.")

# p28
add(id="12b2a911", qtype="choice",
    question="[[0.36]]의 제곱근을 근호를 사용하지 않고 나타낸 것은?",
    choices=["[[-0.36]]", "[[pm(sqrt(0.6))]]", "[[-0.6]]", "[[pm(0.36)]]", "[[pm(0.6)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="0.36의 제곱근 ±0.6 → ⑤. 빠른정답 2와 불일치.")

# p37 (보기 5개, 개수 세기)
add(id="f7883027", qtype="short",
    question=("다음 보기 중 옳은 것은 모두 몇 개인지 구하시오.\n<보기>\n"
              "ㄱ. [[-pow(sqrt(3), 2)]]의 제곱근은 2개이다.\n"
              "ㄴ. 음수가 아닌 수의 제곱근은 2개이다.\n"
              "ㄷ. [[recdec(2,7)]]의 제곱근은 [[pm(recdec(1,6))]]이다.\n"
              "ㄹ. 제곱근 [[sqrt(49)]]는 7이다.\n"
              "ㅁ. [[sqrt(pow(-1, 2))]]의 양의 제곱근과 음의 제곱근의 합은 2이다."),
    choices=None, derived_answer="1개", figure=None, difficulty_est=2, confidence=0.85,
    note="ㄱ −3<0 ✗, ㄴ 0의 제곱근은 1개 ✗, ㄷ 2.7̇=25/9 → ±5/3=±1.6̇ ✓, ㄹ 제곱근 √49=√7 ✗, ㅁ 합 0 ✗ → 1개 = 빠른정답 ✓. 순환소수 2.7̇, 1.6̇은 recdec(2,7), recdec(1,6).")

# p50
add(id="549ee92c", qtype="short",
    question="[[a - b > 0]], [[a b < 0]]일 때, [[sqrt(pow(a,2)) - sqrt(pow(-a, 2))]]을 간단히 하시오.",
    choices=None, derived_answer="0", figure=None, difficulty_est=2,
    note="a>0, b<0 → a − a = 0. 빠른정답 4와 불일치.")

# p52
add(id="4b4de657", qtype="short",
    question="[[a - b < 0]], [[a b < 0]]일 때, [[sqrt(pow(-a, 2)) - sqrt(pow(a,2))]]을 간단히 하시오.",
    choices=None, derived_answer="0", figure=None, difficulty_est=2,
    note="a<0, b>0 → (−a) − (−a) = 0 = 빠른정답 ✓.")

# p77 (빈칸 과정)
add(id="cd3c7e6f", qtype="choice",
    question=("다음은 [[n]]이 자연수일 때 [[sqrt(78 - 3n)]]이 자연수가 되게 하는 [[n]]의 값을 구하는 과정이다.\n"
              "자연수 [[k]]에 대하여 [[sqrt(78 - 3n) = k]]라 하면\n"
              "[[78 - 3n = pow(k,2)]]이므로 [[n = frac(78 - pow(k,2), 3)]]이다.\n"
              "이때 [[n]]은 자연수이므로 [[78 - pow(k,2)]]은 3의 배수이다.\n"
              "따라서 [[k]]는 (가) 의 배수이다.\n"
              "또, [[78 - pow(k,2) > 0]]이므로\n"
              "[[k]] = (나) 또는 [[k = 6]]이다.\n"
              "그러므로 [[n]] = (다) 또는 [[n = 14]]이다.\n"
              "위의 과정에서 (가), (나), (다)에 들어갈 수의 합은?"),
    choices=["[[27]]", "[[29]]", "[[31]]", "[[33]]", "[[35]]"],
    derived_answer="②", figure=None, difficulty_est=2,
    note="출처 [2007년 3월 고1 14번]. (가)=3, (나)=3, (다)=23 → 29 → ②. 빠른정답 12와 불일치.")

# p92
add(id="8a8066f0", qtype="short",
    question=("[[sqrt(a + b + c) = k]]를 만족시키는 자연수 [[k]]가 존재하고 [[a + b + c < 300]]일 때, "
              "연속하는 세 자연수 [[a]], [[b]], [[c]]의 순서쌍 ([[a]], [[b]], [[c]])의 개수를 구하시오. (단, [[a < b < c]])"),
    choices=None, derived_answer="5", figure=None, difficulty_est=3, confidence=0.85,
    note="a+b+c=3b가 제곱수 → b=3m², 9m²<300 → m=1~5 → 5개. 빠른정답 1과 불일치.")

# ====================================================================
# 이차함수의 활용
# ====================================================================

# p6
add(id="f16f85f2", qtype="choice",
    question=("합이 15인 두 수가 있다. 한 수를 [[x]], 두 수의 곱을 [[y]]라 할 때, [[y]]를 [[x]]에 대한 식으로 나타내면 "
              "[[y = a pow(x,2) + b x + c]]이다. 이때 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값을 구하면?"),
    choices=["[[8]]", "[[10]]", "[[12]]", "[[14]]", "[[16]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="y=x(15−x)=−x²+15x → −1+15+0=14 → ④. 빠른정답 36과 불일치.")

# p7
add(id="c07dfd08", qtype="short",
    question=("차가 12인 두 수가 있다. 두 수 중 작은 수를 [[x]], 두 수의 곱을 [[y]]라 할 때, [[y]]를 [[x]]에 대한 식으로 나타내면 "
              "[[y = a pow(x,2) + b x + c]]이다. 이때 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="13", figure=None, difficulty_est=2,
    note="y=x(x+12)=x²+12x → 1+12+0=13. 빠른정답 1/2과 불일치.")

# p9
add(id="b6ed9d78", qtype="short",
    question=("합이 50인 두 수가 있다. 한 수를 [[x]], 두 수의 곱을 [[y]]라 할 때, [[y]]를 [[x]]에 대한 식으로 나타내면 "
              "[[y = a pow(x,2) + b x + c]]이다. 이때 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="49", figure=None, difficulty_est=2,
    note="y=x(50−x)=−x²+50x → −1+50+0=49. 빠른정답 없음.")

# p33
add(id="6f2c55a0", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 [[12]] cm인 정사각형 ABCD에서 [[seg(AP) = seg(AQ)]], [[seg(BQ) = seg(BR)]]일 때, "
              "[[tri(PQR)]]의 넓이의 최댓값을 구하시오."),
    choices=None, derived_answer="36 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, 변 CD 옆에 12 cm 표시), P는 변 AD 위, Q는 변 AB 위(AP=AQ 같은 표시), R는 변 BC 위(BQ=BR 같은 표시), △PQR 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "정사각형 안의 삼각형 PQR 도형",
    note="AP=x: △PQR=x(12−x) → x=6일 때 최대 36 cm². 빠른정답 없음.")

# p39
add(id="1b0dcf4b", qtype="choice",
    question=("다음 그림과 같이 길이가 [[9]] cm인 [[seg(AB)]] 위에 점 C를 잡아 [[seg(AC)]], [[seg(BC)]]를 각각 한 변으로 하는 두 정사각형을 만들었다. "
              "[[seg(AC)]]의 길이를 [[x]] cm, 두 정사각형의 넓이의 합을 [[y]] cm²라 할 때, [[y = a pow(x,2) + b x + c]]의 관계가 성립한다고 한다. "
              "상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값은?"),
    choices=["[[60]]", "[[65]]", "[[70]]", "[[75]]", "[[80]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "선분 AB(9 cm) 위의 점 C, AC(x cm)를 한 변으로 하는 작은 정사각형(왼쪽, 파란색)과 BC를 한 변으로 하는 큰 정사각형(오른쪽, 초록색)이 AB 위에 나란히 놓인 그림"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=REV_FIG + "선분 위 두 정사각형 그림",
    note="y=x²+(9−x)²=2x²−18x+81 → 2−18+81=65 → ②. 빠른정답 없음.")

# p45
add(id="3987d30b", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 20]], [[seg(BC) = 10]]인 직각삼각형 ABC의 빗변 AC 위의 한 점 D에서 [[seg(AB)]]와 [[seg(BC)]]에 내린 수선의 발을 각각 E, F라 하자. "
              "[[quad(DEBF)]]의 넓이가 최대일 때, [[quad(DEBF)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="30",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(∠B=90°, A 위, B 왼쪽 아래, C 오른쪽 아래, AB=20, BC=10), 빗변 AC 위의 점 D에서 AB·BC에 내린 수선의 발 E, F, 직사각형 DEBF 음영(직각 표시)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형에 내접하는 직사각형 도형",
    note="BF=x, DF=20−2x → 넓이 x(20−2x) 최대는 x=5 → 5×10 직사각형, 둘레 30. 빠른정답 14m와 불일치.")

# p53
add(id="bcd0e523", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]이고 [[seg(BC) = 16]] cm인 직각이등변삼각형 ABC에 내접하는 직사각형을 그렸을 때, "
              "이 직사각형의 최대 넓이는?"),
    choices=["[[28]] cm²", "[[30]] cm²", "[[32]] cm²", "[[34]] cm²", "[[36]] cm²"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직각이등변삼각형 ABC(A 위 꼭짓점 직각 표시, B 왼쪽 아래, C 오른쪽 아래, BC=16 cm), 밑변 BC 위에 놓이고 두 꼭짓점이 AB, AC 위에 있는 직사각형 음영"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=REV_FIG + "직각이등변삼각형에 내접하는 직사각형 도형",
    note="높이 8, 가로 w·세로 8−w/2 → w=8일 때 최대 32 cm² → ③. 빠른정답 없음.")

# p55
add(id="3a7d3f29", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]이고 [[seg(BC) = 20]] cm인 직각이등변삼각형 ABC에 내접하는 직사각형을 그렸을 때, "
              "이 직사각형의 최대 넓이는?"),
    choices=["[[50]] cm²", "[[52]] cm²", "[[54]] cm²", "[[56]] cm²", "[[58]] cm²"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "직각이등변삼각형 ABC(A 위 꼭짓점 직각 표시, B 왼쪽 아래, C 오른쪽 아래, BC=20 cm), 밑변 BC 위에 놓이고 두 꼭짓점이 AB, AC 위에 있는 직사각형 음영"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=REV_FIG + "직각이등변삼각형에 내접하는 직사각형 도형",
    note="높이 10, 가로 w·세로 10−w/2 → w=10일 때 최대 50 cm² → ①. 빠른정답 없음.")

# p61
add(id="7de457dd", qtype="short",
    question=("초속 [[30]] m로 쏘아 올린 물 로켓의 [[x]]초 후의 높이를 [[y]] m라 하면 [[y = -4 pow(x,2) + a x + b]]인 관계가 성립한다고 한다. "
              "이 물 로켓의 5초 후의 높이가 [[70]] m일 때, 상수 [[a]], [[b]]에 대하여 [[5a + b]]의 값을 구하시오."),
    choices=None, derived_answer="170", figure=None, difficulty_est=2,
    note="x=5 대입: −100+5a+b=70 → 5a+b=170 = 빠른정답 ✓.")

# p66
add(id="2a2d472c", qtype="choice",
    question=("지면으로부터 똑바로 위로 쏘아 올린 물 로켓의 [[x]]초 후의 높이를 [[y]] m라 하면 [[x]], [[y]] 사이에는 [[y = 30x - 6 pow(x,2)]]인 관계가 성립한다고 한다. "
              "물 로켓을 쏘아 올린 지 2초 후의 물 로켓의 지면으로부터의 높이를 구하면?"),
    choices=["[[30]] m", "[[32]] m", "[[34]] m", "[[36]] m", "[[38]] m"],
    derived_answer="④", figure=None, difficulty_est=1,
    note="60−24=36 → ④. 빠른정답 없음.")

# p74
add(id="0ef5608a", qtype="short",
    question=("지면으로부터 초속 [[55]] m로 똑바로 위로 쏘아 올린 물체의 [[x]]초 후의 높이를 [[y]] m라 하면 [[x]], [[y]] 사이에는 [[y = 55x - 5 pow(x,2)]]의 관계가 성립한다. "
              "이 물체가 지면에 떨어지는 것은 쏘아 올린 지 몇 초 후인지 구하시오."),
    choices=None, derived_answer="11초 후", figure=None, difficulty_est=1,
    note="55x−5x²=0 → x=11 → 11초 후 = 빠른정답 ✓.")

# p94 (벌집 그림)
add(id="a0beae2b", qtype="short",
    question=("벌집의 내부 구조를 살펴보면 다음 그림과 같이 한 정육각형 모양의 벌집을 6개의 정육각형 모양의 벌집이 둘러싸고 있음을 관찰할 수 있다. "
              "[[x]]단계에서 정육각형 모양의 벌집의 개수를 [[y]]라 하면 [[y = a pow(x,2) + b x + 1]]인 관계가 성립한다고 할 때, "
              "5단계에서 정육각형 모양의 벌집의 개수를 구하시오. (단, [[a]], [[b]]는 상수)"),
    choices=None, derived_answer="61",
    figure=[{"fn": "unsupported", "args": {"raw": "벌집 그림: [1단계] 정육각형 1개, [2단계] 가운데 정육각형을 6개의 정육각형이 둘러싼 7개, 이어서 … 표시"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=REV_FIG + "벌집 단계 그림(1단계 1개, 2단계 7개)",
    note="x=1: a+b=0, x=2: 4a+2b=6 → a=3, b=−3 → y=3x²−3x+1, x=5: 61. 빠른정답 150m와 불일치.")

# ====================================================================
# 근호를 포함한 복잡한 식의 계산
# ====================================================================

# p11 ([a]·⟨a⟩ 약속 기호)
add(id="69390e7c", qtype="choice",
    question=("실수 [[a]]에 대하여 [[floor(a)]]는 [[a]]보다 크지 않은 가장 큰 정수를 나타내고 ⟨[[a]]⟩ = [[a - floor(a)]]로 나타내기로 하였다.\n"
              "즉, [[floor(sqrt(2)) = 1]], ⟨[[sqrt(2)]]⟩ = [[sqrt(2) - 1]]일 때,\n"
              "[[floor(5 - sqrt(5))]] + ⟨[[5 + sqrt(5)]]⟩의 값은?"),
    choices=["[[-2 sqrt(5)]]", "[[-sqrt(5)]]", "[[0]]", "[[sqrt(5)]]", "[[2 sqrt(5)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="[5−√5]=2, ⟨5+√5⟩=√5−2 → 합 √5 → ④ = 빠른정답 ✓. [a]는 floor, 약속 기호 ⟨a⟩는 텍스트.")

# p12
add(id="2f1bae71", qtype="choice",
    question=("실수 [[a]]에 대하여 [[floor(a)]]는 [[a]]보다 크지 않은 가장 큰 정수를 나타내고 ⟨[[a]]⟩ = [[a - floor(a)]]로 나타내기로 하였다. 즉, "
              "[[floor(sqrt(2)) = 1]], ⟨[[sqrt(2)]]⟩ = [[sqrt(2) - 1]]일 때,\n"
              "[[floor(4 - sqrt(15))]] + ⟨[[4 + sqrt(15)]]⟩의 값은?"),
    choices=["[[-sqrt(15)]]", "[[0]]", "[[sqrt(15) - 3]]", "[[sqrt(15)]]", "[[sqrt(15) + 3]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="[4−√15]=0, ⟨4+√15⟩=√15−3 → ③ = 빠른정답 ✓. 약속 기호 ⟨a⟩는 텍스트.")

# p13 (기호 (a, b) = 작지 않은 수)
add(id="72ee0a7c", qtype="short",
    question=("기호 ([[a]], [[b]])는 두 수 [[a]], [[b]] 중 작지 않은 수를 나타낼 때, 다음을 간단히 하시오.\n"
              "([[frac(5, sqrt(2))]], [[3 sqrt(2)]]) × ([[6 sqrt(2)]], [[8.3]]) − ([[-2 sqrt(5)]], [[-4.2]])"),
    choices=None, derived_answer="40.2", figure=None, difficulty_est=3, confidence=0.85,
    note="(5/√2≈3.54, 3√2≈4.24)→3√2, (6√2≈8.49, 8.3)→6√2, (−2√5≈−4.47, −4.2)→−4.2 → 36+4.2=40.2. 약속 기호 (a, b)는 텍스트. 빠른정답 8과 불일치.")

# p14
add(id="f7a1e9b2", qtype="short",
    question=("기호 ([[a]], [[b]])는 두 수 [[a]], [[b]] 중 작지 않은 수를 나타낼 때, 다음을 간단히 하시오.\n"
              "([[frac(4, sqrt(3))]], [[sqrt(5)]]) × ([[6 sqrt(3)]], [[10.1]]) − ([[-2 sqrt(2)]], [[-2.5]])"),
    choices=None, derived_answer="26.5", figure=None, difficulty_est=3, confidence=0.85,
    note="(4/√3≈2.31, √5≈2.24)→4/√3, (6√3≈10.39, 10.1)→6√3, (−2√2≈−2.83, −2.5)→−2.5 → 24+2.5=26.5. 약속 기호 (a, b)는 텍스트. 빠른정답 4와 불일치.")

# p15 (<x, y> 약속)
add(id="d544dbf7", qtype="short",
    question=("두 유리수 [[x]], [[y]]에 대하여\n<[[x]], [[y]]> = [[sqrt(3) x + sqrt(pow(x - y, 2))]]이라 하자.\n"
              "[[a > 0]], [[b < 0]]일 때,\n<[[-a]], [[-2b]]> = <[[5b]], [[3a]]> − 13을 만족시키는 두 유리수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.85,
    note="좌변 −√3a+(a−2b), 우변 5√3b+(3a−5b)−13 → a=−5b, −2a+3b+13=0 → b=−1, a=5 → 4. 약속 기호 <x, y>는 텍스트. 빠른정답 3과 불일치.")

# p16
add(id="d90882b6", qtype="short",
    question=("두 유리수 [[x]], [[y]]에 대하여\n<[[x]], [[y]]> = [[sqrt(2) x + sqrt(pow(x + y, 2))]]이라 하자.\n"
              "[[a > 0]], [[b < 0]]일 때,\n<[[a]], [[-2b]]> = <[[-2b]], [[5a]]> − 8을 만족시키는\n두 유리수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.85,
    note="좌변 √2a+(a−2b), 우변 −2√2b+(5a−2b)−8 → a=−2b, 4a=8 → a=2, b=−1 → 1. 약속 기호 <x, y>는 텍스트. 빠른정답 40.2와 불일치.")

# p18 (★ 연산)
add(id="4e5af321", qtype="choice",
    question=("임의의 실수 [[a]], [[b]]에 대하여 ★을\n[[a]]★[[b]] = [[a b - a - b - 3]]이라 할 때, [[sqrt(5)]]★[[frac(3 sqrt(5), 5)]]의 값은?"),
    choices=["[[0]]", "[[-frac(3 sqrt(5), 5)]]", "[[-frac(8 sqrt(5), 5)]]", "[[3 - frac(3 sqrt(5), 5)]]", "[[3 - frac(8 sqrt(5), 5)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="3−√5−3√5/5−3=−8√5/5 → ③. 연산 기호 ★는 텍스트. 빠른정답 4와 불일치.")

# p28 ({x, y} 약속)
add(id="bd115db3", qtype="short",
    question=("두 유리수 [[x]], [[y]]에 대하여 {[[x]], [[y]]} = [[sqrt(pow(-x, 2)) + sqrt(5) y]]라 하자. [[m < 0]], [[n > 0]]일 때, "
              "{[[m]], [[-4n]]} − 1 = {[[n]], [[3m]]}을 만족시키는 두 유리수 [[m]], [[n]]에 대하여 [[m n]]의 값을 구하시오."),
    choices=None, derived_answer="-12", figure=None, difficulty_est=3, confidence=0.85,
    note="−m−4√5n−1 = n+3√5m → m=−4n/3, −m−1=n → n=3, m=−4 → mn=−12. 약속 기호 {x, y}는 텍스트. 빠른정답 3과 불일치.")

# p46
add(id="1a4b05a8", qtype="choice",
    question="[[a = sqrt(2)]], [[b = sqrt(3)]]일 때, [[sqrt(216) + frac(sqrt(24), sqrt(2))]]를 [[a]], [[b]]로 나타내면?",
    choices=["[[6a + 2b]]", "[[6a + 2 a b]]", "[[6 a b + 2b]]", "[[2 a b + 6b]]", "[[2a + 6 a b]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="√216=6√6=6ab, √24/√2=√12=2√3=2b → ③. 빠른정답 1과 불일치.")

# p50
add(id="c4dd043e", qtype="choice",
    question=("[[sqrt(2) = a]], [[sqrt(5) = b]]라 할 때,\n[[sqrt(5)(sqrt(10) + sqrt(8)) - (5 - sqrt(5)) sqrt(2)]]를 [[a]], [[b]]를 이용하여 나타낸 것은?"),
    choices=["[[-5 a b]]", "[[-3 a b]]", "[[-a b]]", "[[a b]]", "[[3 a b]]"],
    derived_answer="⑤", figure=None, difficulty_est=2,
    note="5√2+2√10−5√2+√10=3√10=3ab → ⑤. 빠른정답 4와 불일치.")

# p52
add(id="5d6e1bb1", qtype="choice",
    question="[[a > 0]], [[b > 0]]이고 [[a b = 9]]일 때, [[a sqrt(frac(25b, a)) - b sqrt(frac(4a, b))]]의 값은?",
    choices=["[[3]]", "[[3 sqrt(3)]]", "[[6]]", "[[9]]", "[[9 sqrt(3)]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="√(25ab)−√(4ab)=15−6=9 → ④ = 빠른정답 ✓.")

# p58
add(id="ea17fbcd", qtype="choice",
    question="[[a > 0]], [[b > 0]]이고 [[2a + b = 12]], [[a b = 4]]일 때,\n[[sqrt(frac(2a, b)) + sqrt(frac(b, 2a))]]의 값은?",
    choices=["[[2 sqrt(3)]]", "[[3 sqrt(2)]]", "[[2 sqrt(5)]]", "[[4 sqrt(2)]]", "[[4 sqrt(3)]]"],
    derived_answer="②", figure=None, difficulty_est=3,
    note="(2a+b)/√(2ab)=12/√8=3√2 → ②. 빠른정답 −12와 불일치.")

# p66 (정사각뿔, G′)
add(id="9e7bb6c5", qtype="short",
    question=("다음 그림과 같이 밑면이 정사각형이고 옆면이 정삼각형인 사각뿔 A−BCDE가 있다. [[tri(ACD)]]의 무게중심을 G, [[tri(ADE)]]의 무게중심을 G′이라 하자. "
              "모서리 CD 위의 점 P와 모서리 DE 위의 점 Q에 대하여 [[seg(GP) + seg(PQ)]] + [[seg(QG)]]′의 길이의 최솟값이 [[6 sqrt(2) + 2 sqrt(6)]]일 때, "
              "사각뿔 A−BCDE의 한 모서리의 길이를 구하시오."),
    choices=None, derived_answer="12",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각뿔 A−BCDE(꼭짓점 A 위, 밑면 정사각형 BCDE: B 뒤 왼쪽, C 앞 왼쪽, D 앞, E 오른쪽), 면 ACD 위의 무게중심 G, 면 ADE 위의 무게중심 G′, 모서리 CD 위의 점 P, 모서리 DE 위의 점 Q, 선분 GP·PQ·QG′"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="프라임 점 라벨 G′: seg(QG′)를 [[seg(QG)]]′로 텍스트 혼합 / " + REV_FIG + "정사각뿔 입체 도형(무게중심 G, G′와 점 P, Q)",
    note="전개도에서 GG′=s(3√2+√6)/6=6√2+2√6 → s=12. 빠른정답 3과 불일치.")

# p67
add(id="2daff16c", qtype="short",
    question=("다음 그림과 같이 밑면이 정사각형이고 옆면이 정삼각형인 사각뿔 A−BCDE가 있다. [[tri(ACD)]]의 무게중심을 G, [[tri(ADE)]]의 무게중심을 G′이라 하자. "
              "모서리 CD 위의 점 P와 모서리 DE 위의 점 Q에 대하여 [[seg(GP) + seg(PQ)]] + [[seg(QG)]]′의 길이의 최솟값이 [[3(3 sqrt(2) + sqrt(6))]]일 때, "
              "사각뿔 A−BCDE의 한 모서리의 길이를 구하시오."),
    choices=None, derived_answer="18",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각뿔 A−BCDE(꼭짓점 A 위, 밑면 정사각형 BCDE: B 뒤 왼쪽, C 앞 왼쪽, D 앞, E 오른쪽), 면 ACD 위의 무게중심 G, 면 ADE 위의 무게중심 G′, 모서리 CD 위의 점 P, 모서리 DE 위의 점 Q, 선분 GP·PQ·QG′"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="프라임 점 라벨 G′: seg(QG′)를 [[seg(QG)]]′로 텍스트 혼합 / " + REV_FIG + "정사각뿔 입체 도형(무게중심 G, G′와 점 P, Q)",
    note="전개도에서 GG′=s(3√2+√6)/6=3(3√2+√6) → s=18 = 빠른정답 ✓.")

# p74 (모눈종이 수직선)
add(id="fe5662f5", qtype="choice",
    question=("다음 그림은 한 눈금의 길이가 1인 모눈종이 위에 수직선과 두 직각삼각형 ABC, CDE를 그린 것이다.\n"
              "[[seg(AC) = seg(PC)]], [[seg(EC) = seg(QC)]]인 수직선 위의 두 점 P, Q에 대응하는 수를 각각 [[p]], [[q]]라 할 때, [[q - p]]의 값은?"),
    choices=["[[3 sqrt(2)]]", "[[5 sqrt(2)]]", "[[8]]", "[[4 + 3 sqrt(2)]]", "[[4 + 5 sqrt(2)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "모눈종이(한 눈금 1) 위의 수직선(−4~4 눈금): 직각삼각형 ABC(B=−2 위치, A는 B에서 위로 3칸, C=1, ∠B 직각)와 직각삼각형 CDE(D=3, E는 D에서 위로 2칸, ∠D 직각), C를 중심으로 A를 왼쪽 수직선 위로 돌린 점 P(−3과 −4 사이), E를 오른쪽 수직선 위로 돌린 점 Q(3과 4 사이), 점선 호"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=REV_FIG + "모눈종이 위 수직선·직각삼각형 도형",
    note="AC=3√2 → p=1−3√2, EC=2√2 → q=1+2√2 → q−p=5√2 → ② = 빠른정답 ✓.")

# p77 (수직선 A, M, N, B)
add(id="f1381559", qtype="choice",
    question=("다음 그림과 같은 수직선에서 점 A와 점 B에 대응하는 수는 각각 [[2 - sqrt(5)]], [[4 + sqrt(5)]]이고 점 M은 [[seg(AB)]]의 중점이다. "
              "점 N이 [[ratio(seg(MN), seg(NB)) = ratio(3, 1)]]을 만족시킬 때, 점 N에 대응하는 수는?"),
    choices=["[[frac(15 + 3 sqrt(5), 4)]]", "[[frac(17 + 3 sqrt(5), 4)]]", "[[frac(19 + 3 sqrt(5), 4)]]", "[[frac(17 + 5 sqrt(5), 4)]]", "[[frac(17 + 7 sqrt(5), 4)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "수직선 위에 왼쪽부터 점 A, M, N, B 순서로 표시(N은 B 바로 왼쪽)"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=REV_FIG + "수직선 위 네 점 A, M, N, B 그림",
    note="M=3, MB=1+√5, N=3+¾(1+√5)=(15+3√5)/4 → ①. 빠른정답 2와 불일치.")

# p78
add(id="5aba65b1", qtype="choice",
    question=("다음 그림과 같은 수직선에서 점 A와 점 B에 대응하는 수는 각각 [[2 - sqrt(2)]], [[6 + sqrt(2)]]이고 점 M은 [[seg(AB)]]의 중점이다. "
              "점 N이 [[ratio(seg(MN), seg(NB)) = ratio(2, 1)]]을 만족시킬 때, 점 N에 대응하는 수는?"),
    choices=["[[frac(16 + sqrt(2), 3)]]", "[[frac(16 + 2 sqrt(2), 3)]]", "[[frac(20 + sqrt(2), 3)]]", "[[frac(20 + 2 sqrt(2), 3)]]", "[[frac(20 + 4 sqrt(2), 3)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "수직선 위에 왼쪽부터 점 A, M, N, B 순서로 표시(N은 B 바로 왼쪽)"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=REV_FIG + "수직선 위 네 점 A, M, N, B 그림",
    note="M=4, MB=2+√2, N=4+⅔(2+√2)=(16+2√2)/3 → ②. 빠른정답 5와 불일치.")

# p81 (대소 비교 빈칸)
add(id="24dca600", qtype="choice",
    question=("다음은 [[a = 4 sqrt(2)]], [[b = 3 sqrt(6)]]의 대소를 비교하는 과정이다. □ 안에 알맞은 것을 순서대로 넣은 것은?\n"
              "[[a]] □ [[b]] = [[4 sqrt(2)]] − □\n"
              "= [[sqrt(32) - sqrt(54)]] □ 0\n"
              "∴ [[a]] □ [[b]]"),
    choices=["+, [[3 sqrt(6)]], <, >", "+, [[4 sqrt(2)]], >, >", "−, [[3 sqrt(6)]], >, >", "−, [[4 sqrt(2)]], <, <", "−, [[3 sqrt(6)]], <, <"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="a−b=√32−√54<0 ∴ a<b → ⑤ = 빠른정답 ✓. 빈칸 □와 부등호 선지는 텍스트.")

# ====================================================================
# 다항식과 다항식의 곱셈
# ====================================================================

# p1
add(id="ce541ed5", qtype="short",
    question="[[(3x - 2)(y + 2x) = 6 pow(x,2) + a x y + b x + c y]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a b - c]]의 값을 구하시오.",
    choices=None, derived_answer="-10", figure=None, difficulty_est=1,
    note="6x²+3xy−4x−2y → a=3, b=−4, c=−2 → −12+2=−10 = 빠른정답 ✓.")

# p2
add(id="f1c9034f", qtype="short",
    question="[[(5x - 3)(y + 3x) = 15 pow(x,2) + a x y + b x + c y]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a b - c]]의 값을 구하시오.",
    choices=None, derived_answer="-42", figure=None, difficulty_est=1,
    note="15x²+5xy−9x−3y → a=5, b=−9, c=−3 → −45+3=−42 = 빠른정답 ✓.")

# p3
add(id="e0344587", qtype="short",
    question="[[(4x - 1)(y + 3x) = 12 pow(x,2) + a x y + b x + c y]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a b - c]]의 값을 구하시오.",
    choices=None, derived_answer="-11", figure=None, difficulty_est=1,
    note="12x²+4xy−3x−y → a=4, b=−3, c=−1 → −12+1=−11 = 빠른정답 ✓.")

# p5
add(id="1ab3f7d3", qtype="choice",
    question="[[(3x + a)(4x - 5) = 12 pow(x,2) + b x - 10]]에서 [[a]], [[b]]가 상수일 때, [[a + b]]의 값은?",
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    derived_answer="①", figure=None, difficulty_est=1,
    note="−5a=−10 → a=2, b=−15+8=−7 → −5 → ①. 빠른정답 −42와 불일치.")

# p8
add(id="1c1c4dde", qtype="choice",
    question="[[(3x + y)(x - y + 2)]]를 전개하면?",
    choices=["[[-3 pow(x,2) - 4 x y + 6x - pow(y,2) + 2y]]",
             "[[-3 pow(x,2) - 2 x y + 6x - pow(y,2) + 2y]]",
             "[[3 pow(x,2) - 4 x y + 6x - pow(y,2) + 2y]]",
             "[[3 pow(x,2) - 2 x y + 6x - pow(y,2) + 2y]]",
             "[[3 pow(x,2) - x y + 6x - 2 pow(y,2) + 2y]]"],
    derived_answer="④", figure=None, difficulty_est=1,
    note="3x²−3xy+6x+xy−y²+2y=3x²−2xy+6x−y²+2y → ④. 빠른정답 1과 불일치.")

# p10
add(id="b0510286", qtype="short",
    question="[[(2x + y)(4x - y) = a pow(x,2) + b x y - pow(y,2)]]일 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="10", figure=None, difficulty_est=1,
    note="8x²+2xy−y² → 8+2=10 = 빠른정답 ✓.")

# p11
add(id="36d72bcc", qtype="short",
    question="[[(5x + y)(3x - y) = a pow(x,2) + b x y - pow(y,2)]]일 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="13", figure=None, difficulty_est=1,
    note="15x²−2xy−y² → 15−2=13 = 빠른정답 ✓.")

# p13
add(id="31e2c04b", qtype="choice",
    question="[[(2x - 1)(3 + 4y) = a x y + b x + c y - 3]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값은?",
    choices=["[[7]]", "[[8]]", "[[9]]", "[[10]]", "[[11]]"],
    derived_answer="④", figure=None, difficulty_est=1,
    note="8xy+6x−4y−3 → 8+6−4=10 → ④ (빠른정답 10과 값 일치).")

# p14
add(id="e217f4b5", qtype="choice",
    question="[[(4x - 1)(5 + 3y) = a x y + b x + c y - 5]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값은?",
    choices=["[[25]]", "[[27]]", "[[29]]", "[[31]]", "[[33]]"],
    derived_answer="③", figure=None, difficulty_est=1,
    note="12xy+20x−3y−5 → 12+20−3=29 → ③. 빠른정답 13과 불일치.")

# p15
add(id="0675ebdf", qtype="choice",
    question="[[(5x - 2)(1 + 4y) = a x y + b x + c y - 2]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값은?",
    choices=["[[15]]", "[[17]]", "[[19]]", "[[21]]", "[[23]]"],
    derived_answer="②", figure=None, difficulty_est=1,
    note="20xy+5x−8y−2 → 20+5−8=17 → ②. 빠른정답 25와 불일치.")

# p16
add(id="89db8ac1", qtype="choice",
    question="[[(2x + 1)(x + 3y)]]를 전개하면?",
    choices=["[[2 pow(x,2) + 5 x y + 3y]]",
             "[[2 pow(x,2) + 6 x y + 3y]]",
             "[[2 pow(x,2) + 5 x y + x + 3y]]",
             "[[2 pow(x,2) + 6 x y + x + 3y]]",
             "[[2 pow(x,2) + 6 x y + 3x + y]]"],
    derived_answer="④", figure=None, difficulty_est=1,
    note="2x²+6xy+x+3y → ④ = 빠른정답 ✓.")

# p18
add(id="975acde8", qtype="choice",
    question="[[(4x + 1)(x + 2y)]]를 전개하면?",
    choices=["[[4 pow(x,2) + 6 x y + 8y]]",
             "[[4 pow(x,2) + 8 x y + 8y]]",
             "[[4 pow(x,2) + 6 x y + x + 2y]]",
             "[[4 pow(x,2) + 8 x y + x + 2y]]",
             "[[4 pow(x,2) + 8 x y + 2x + y]]"],
    derived_answer="④", figure=None, difficulty_est=1,
    note="4x²+8xy+x+2y → ④. 빠른정답 2와 불일치.")

# p20
add(id="b31d1cb2", qtype="short",
    question="[[(4x + 3)(x + a) = 4 pow(x,2) + b x + 27]]에서 [[a]], [[b]]가 상수일 때, [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="48", figure=None, difficulty_est=1,
    note="3a=27 → a=9, b=4·9+3=39 → 48. 빠른정답 5와 불일치.")

# p22
add(id="d830e221", qtype="choice",
    question="[[(4x + 5)(A x + B) = 12 pow(x,2) - C x - 15]]일 때,\n상수 [[A]], [[B]], [[C]]에 대하여 [[A + B - C]]의 값은?",
    choices=["[[-3]]", "[[-1]]", "[[1]]", "[[3]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="A=3, B=−3, 4B+5A=3=−C → C=−3 → 3−3+3=3 → ④. 빠른정답 2와 불일치.")

# p24
add(id="fad93df9", qtype="choice",
    question="[[(x - 2)(A x + B) = 3 pow(x,2) - C x + 4]]일 때, 상수 [[A]], [[B]], [[C]]에 대하여 [[A + B + C]]의 값은?",
    choices=["[[-9]]", "[[-3]]", "[[9]]", "[[18]]", "[[21]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="A=3, B=−2, B−2A=−8=−C → C=8 → 9 → ③ = 빠른정답 ✓.")

# p25
add(id="4b52cecd", qtype="choice",
    question="[[(2x - 5)(A x + B) = 8 pow(x,2) - C x + 25]]일 때, 상수 [[A]], [[B]], [[C]]에 대하여 [[A + B + C]]의 값은?",
    choices=["[[-40]]", "[[-16]]", "[[8]]", "[[29]]", "[[39]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="A=4, B=−5, 2B−5A=−30=−C → C=30 → 29 → ④ = 빠른정답 ✓.")

# p26
add(id="c4d73e64", qtype="choice",
    question="[[(x + 3)(A x + B) = 3 pow(x,2) - C x + 18]]일 때, 상수 [[A]], [[B]], [[C]]에 대하여 [[A + B + C]]의 값은?",
    choices=["[[-15]]", "[[-6]]", "[[10]]", "[[15]]", "[[24]]"],
    derived_answer="②", figure=None, difficulty_est=2,
    note="A=3, B=6, B+3A=15=−C → C=−15 → −6 → ②. 빠른정답 4와 불일치.")

# p27 (△ 연산)
add(id="bd193e70", qtype="short",
    question=("두 정수 [[x]], [[y]]에 대하여\n[[x]]△[[y]] = [[(1 - x)(1 - y) - x y]]로 정의한다.\n"
              "([[x]]△[[y]])△[[z]] + ([[y]]△[[z]])△[[x]] + ([[z]]△[[x]])△[[y]] = [[-2]]일 때,\n[[x + y + z]]의 값을 구하시오."),
    choices=None, derived_answer="-2", figure=None, difficulty_est=3, confidence=0.85,
    note="x△y=1−x−y → (x△y)△z=x+y−z, 세 항의 합=x+y+z=−2 = 빠른정답 ✓. 연산 기호 △는 텍스트.")

# p28
add(id="83669a27", qtype="choice",
    question="[[(2x + y - 2)(3x + 2y + 4)]]를 전개하면?",
    choices=["[[3 pow(x,2) + 3 x y + 2 pow(y,2)]]",
             "[[3 pow(x,2) + 6 x y + 2 pow(y,2) - 8]]",
             "[[6 pow(x,2) + 7 x y + 2 pow(y,2) - 8]]",
             "[[6 pow(x,2) + 2x + 7 x y + 2 pow(y,2) - 8]]",
             "[[12 pow(x,2) + 2x + 7 x y - 8 pow(y,2)]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="6x²+7xy+2y²+2x−8 → ④ = 빠른정답 ✓.")

# p29
add(id="cd0c1b0c", qtype="choice",
    question="[[(x + 3y - 1)(2x + y - 2)]]를 전개하면?",
    choices=["[[2 pow(x,2) + 3x + 5 x y + 2 pow(y,2) - 2]]",
             "[[2 pow(x,2) + x + 7 x y + 3 pow(y,2) - 5]]",
             "[[2 pow(x,2) - 4x + 7 x y + 3 pow(y,2) - 7y + 2]]",
             "[[2 pow(x,2) + 4x + 3 x y + 3 pow(y,2) - 3y - 2]]",
             "[[2 pow(x,2) - 4x + 7 x y + 3 pow(y,2) - 5y - 2]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="2x²+7xy+3y²−4x−7y+2 → ③. 빠른정답 2와 불일치.")

# p31
add(id="90a9509c", qtype="choice",
    question="[[(2x - y)(3x + 5y)]]를 전개한 식은?",
    choices=["[[5 pow(x,2) - 3 x y - 5 pow(y,2)]]",
             "[[5 pow(x,2) + 10 x y - 5 pow(y,2)]]",
             "[[6 pow(x,2) - 3 x y - 5 pow(y,2)]]",
             "[[6 pow(x,2) + 7 x y - 5 pow(y,2)]]",
             "[[6 pow(x,2) + 10 x y - 5 pow(y,2)]]"],
    derived_answer="④", figure=None, difficulty_est=1,
    note="6x²+7xy−5y² → ④ = 빠른정답 ✓.")

# p34
add(id="ba5250e9", qtype="choice",
    question="[[(3x - 5)(2x + 3) = A pow(x,2) + B x + C]]에서 상수 [[A]], [[B]], [[C]]의 합 [[A + B + C]]의 값은?",
    choices=["[[-12]]", "[[-11]]", "[[-10]]", "[[-9]]", "[[-8]]"],
    derived_answer="③", figure=None, difficulty_est=1,
    note="6x²−x−15 → 6−1−15=−10 → ③. 빠른정답 4와 불일치.")

# p35
add(id="a976f9c7", qtype="choice",
    question="[[(x + 2y)(2x + y)]]를 전개하면?",
    choices=["[[pow(x,2) + 5 x y + pow(y,2)]]",
             "[[pow(x,2) + 5 x y + 2 pow(y,2)]]",
             "[[2 pow(x,2) + x y + pow(y,2)]]",
             "[[2 pow(x,2) + 2 x y + pow(y,2)]]",
             "[[2 pow(x,2) + 5 x y + 2 pow(y,2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="2x²+5xy+2y² → ⑤ = 빠른정답 ✓.")

# p40
add(id="cec07d93", qtype="choice",
    question="[[(5x - 2)(3 - y) = a x y + b x + c y - 6]]일 때,\n상수 [[a]], [[b]], [[c]]에 대하여 [[a + b - c]]의 값은?",
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="③", figure=None, difficulty_est=1,
    note="−5xy+15x+2y−6 → −5+15−2=8 → ③. 빠른정답 1과 불일치.")

# p42
add(id="43fd355d", qtype="choice",
    question="[[(2x - 9)(3 - y) = a x y + b x + c y - 27]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값은?",
    choices=["[[1]]", "[[4]]", "[[7]]", "[[10]]", "[[13]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="−2xy+6x+9y−27 → −2+6+9=13 → ⑤. 빠른정답 3과 불일치.")

# p44
add(id="0f2be950", qtype="choice",
    question="[[(4x - 7)(3 - y) = a x y + b x + c y - 21]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값은?",
    choices=["[[3]]", "[[6]]", "[[9]]", "[[12]]", "[[15]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="−4xy+12x+7y−21 → −4+12+7=15 → ⑤. 빠른정답 2와 불일치.")

# p51
add(id="e0de9c0a", qtype="short",
    question="[[(4x - 5y + 3)(x + 3y)]]의 전개식에서 [[x y]]의 계수를 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=1,
    note="4·3+(−5)·1=7 = 빠른정답 ✓.")

# p53
add(id="2300875b", qtype="short",
    question="[[(2x + 3y)(x - 5y + 3)]]의 전개식에서 [[x y]]의 계수를 구하시오.",
    choices=None, derived_answer="-7", figure=None, difficulty_est=1,
    note="2·(−5)+3·1=−7. 빠른정답 3과 불일치.")

# p59
add(id="a19f53e6", qtype="short",
    question="[[(x + 4y)(2x - 5y + 3)]]의 전개식에서 [[x y]]의 계수를 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1,
    note="1·(−5)+4·2=3. 빠른정답 10과 불일치.")

# p63
add(id="af5ef5b4", qtype="short",
    question="[[(x + a y + 1)(x + 2y + 3)]]의 전개식에서 [[x y]]의 계수가 [[-3]]일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="-5", figure=None, difficulty_est=1,
    note="2+a=−3 → a=−5. 빠른정답 16과 불일치.")

# p64
add(id="8f72c725", qtype="choice",
    question="[[(x - y + 2)(3x - y + 4)]]의 전개식에서 [[x y]]의 계수를 [[A]], [[x]]의 계수를 [[B]]라 할 때, [[A + B]]의 값은?",
    choices=["[[-10]]", "[[-6]]", "[[6]]", "[[8]]", "[[14]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="A=−1−3=−4, B=4+6=10 → 6 → ③. 빠른정답 −8과 불일치.")

# p65
add(id="f7a11f04", qtype="choice",
    question="[[(2x + y - 3)(3x - 2y + 1)]]의 전개식에서 [[x y]]의 계수는?",
    choices=["[[-4]]", "[[-1]]", "[[1]]", "[[3]]", "[[7]]"],
    derived_answer="②", figure=None, difficulty_est=1,
    note="−4+3=−1 → ②. 빠른정답 1과 불일치.")

# p67
add(id="eccba168", qtype="short",
    question="[[(2x + 3y - 5)(3x + a y + 4)]]의 전개식에서 [[x y]]의 계수가 5일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="-2", figure=None, difficulty_est=1,
    note="2a+9=5 → a=−2 = 빠른정답 ✓.")

# p68
add(id="08adec08", qtype="short",
    question=("[[(x + a y - 2)(2x - 3y + b)]]를 전개한 식에서 상수항이 2, [[x y]]의 계수가 [[-1]]일 때, 상수 [[a]], [[b]]에 대하여 "
              "[[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=2,
    note="−2b=2 → b=−1, 2a−3=−1 → a=1 → 0. 빠른정답 2와 불일치.")

# p71
add(id="eecffa72", qtype="choice",
    question="[[(-5x + 3y)(a x - 2y + 1)]]의 전개식에서 [[pow(x,2)]]의 계수와 [[x y]]의 계수가 같을 때, 상수 [[a]]의 값은?",
    choices=["[[-frac(9,4)]]", "[[-frac(7,4)]]", "[[-frac(5,4)]]", "[[-frac(3,4)]]", "[[-frac(1,4)]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="−5a=10+3a → a=−5/4 → ③ = 빠른정답 ✓.")

# p73
add(id="5864baae", qtype="choice",
    question="[[(-2x + 3y)(a x + 5y - 2)]]의 전개식에서 [[pow(x,2)]]의 계수와 [[x y]]의 계수가 같을 때, 상수 [[a]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=2,
    note="−2a=−10+3a → a=2 → ② = 빠른정답 ✓.")

# p74
add(id="18131cf3", qtype="short",
    question=("[[(x - 2y + 1)(x + a y + b)]]의 전개식에서 [[x y]]의 계수와 [[y]]의 계수가 모두 [[-4]]일 때, [[a b]]의 값을 구하시오.\n"
              "(단, [[a]], [[b]]는 상수)"),
    choices=None, derived_answer="-2", figure=None, difficulty_est=2,
    note="a−2=−4 → a=−2, −2b+a=−4 → b=1 → ab=−2. 빠른정답 3과 불일치.")

# p75
add(id="d3f8dd13", qtype="short",
    question=("[[(3x + A y - 1)(2x + y + B)]]의 전개식에서 [[x y]]의 계수가 9이고 [[x]]의 계수가 4일 때, [[y]]의 계수를 구하시오.\n"
              "(단, [[A]], [[B]]는 상수이다.)"),
    choices=None, derived_answer="5", figure=None, difficulty_est=2,
    note="3+2A=9 → A=3, 3B−2=4 → B=2, y의 계수 AB−1=5. 빠른정답 −1과 불일치.")

# p76
add(id="341cb821", qtype="short",
    question=("[[(x + a y + 5)(4x - 2y + b)]]를 전개한 식에서 상수항이 15, [[x y]]의 계수가 18일 때, 상수 [[a]], [[b]]에 대하여 "
              "[[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2,
    note="5b=15 → b=3, −2+4a=18 → a=5 → 8 = 빠른정답 ✓.")

# p78
add(id="db2ecc5c", qtype="short",
    question="[[(a x + 2y)(5x - 3y + 3)]]의 전개식에서 [[x y]]의 계수가 4일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=1,
    note="−3a+10=4 → a=2 = 빠른정답 ✓.")
