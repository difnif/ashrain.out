# -*- coding: utf-8 -*-
# esc_sonnet_h1-2_7of7 — 이미지 기준 전사 (26 항목 / 26쪽: 함수의 개념과 그래프 6 + 평행이동 20)
# 표기 관행: 평행이동 (x, y)→(x+a, y+b)는 [[point(x, y)]]→[[point(x + a, y + b)]] (화살표는 텍스트).
#            프라임 라벨 C′은 prime(C)로 표기(도함수 기호와 동형) → needs_review. 조각적 정의·fⁿ(x) 표기는 텍스트 혼합 → needs_review.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_NUM = lambda *v: ["[[%s]]" % x for x in v]
MOVE = "[[point(x, y)]]→[[point({x}, {y})]]"

# ===================== 함수의 개념과 그래프 =====================
# p63
add(id="50c56465", qtype="choice",
    question=("집합 [[X = set(-1, 0, 1)]]에 대하여 함수 [[f]]가 "
              "[[X]]에서 [[X]]로의 함수일 때, 다음 중 항등함수인 것은?"),
    choices=["[[f(x) = abs(x)]]", "[[f(x) = pow(x,2)]]", "[[f(x) = -x]]", "[[f(x) = pow(x,3)]]",
             "[[f(x)]] = { [[sqrt(x)]] ([[x >= 0]]) ; [[sqrt(-x)]] ([[x < 0]]) }"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 선지 ⑤의 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사",
    note="x³=x (x=−1,0,1) → ④ (빠른정답 없음). ⑤는 f(−1)=1≠−1.")

# p69
add(id="510a1936", qtype="short",
    question=("두 집합 [[X = set(1, 3, 5, 7)]], [[Y = set(2, 4, 6, 8)]]에 대하여 "
              "함수 [[f]]: [[X]]→[[Y]]가 상수함수일 때,\n"
              "[[f(1) + f(3) + f(5) + f(7)]]의 최댓값과 최솟값의 합을 구하시오."),
    choices=None, derived_answer="40", figure=None, difficulty_est=1, confidence=0.85,
    note="최댓값 4×8=32, 최솟값 4×2=8 → 합 40. 빠른정답 18과 불일치.")

# p70
add(id="55875147", qtype="short",
    question=("두 집합\n[[X = set(a, b, c, d)]], [[Y = set(1, 2, 3, 4, 5)]]에 "
              "대하여 다음 조건을 만족하는 함수 [[f]]: [[X]]→[[Y]]의 개수를 구하시오.\n"
              "집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 "
              "[[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다."),
    choices=None, derived_answer="120", figure=None, difficulty_est=2, confidence=0.85,
    note="일대일함수의 개수 ₅P₄=120. 빠른정답 37과 불일치. 조건 상자는 줄바꿈 텍스트.")

# p77
add(id="89ad02e6", qtype="short",
    question=("두 집합 [[X = set(1, 2, 3, 4, 5)]],\n[[Y = set(2, 4, 6, 8, 10, 12, 14, 16)]]에 대하여 함수 "
              "[[f]]: [[X]]→[[Y]]가 다음 조건을 만족할 때, 함수 [[f]]의 개수를 구하시오.\n"
              "(가) [[f(4) = 8]]\n"
              "(나) [[in(sub(x,1), X)]], [[in(sub(x,2), X)]]일 때,\n"
              "[[sub(x,1) < sub(x,2)]]이면 [[f(sub(x,1)) > f(sub(x,2))]]이다."),
    choices=None, derived_answer="12", figure=None, difficulty_est=3, confidence=0.85,
    note="감소함수: f(5)∈{2,4,6} 3가지 × f(1)>f(2)>f(3)>8은 {10,12,14,16}에서 3개 택 ₄C₃=4 → 12. 빠른정답 36과 불일치.")

# p78
add(id="ad423f71", qtype="short",
    question=("집합 [[X = set(1, 3, 5, 7, 9)]]에 대하여 다음 조건을 "
              "만족시키는 함수 [[f]]: [[X]]→[[X]]의 개수를 구하시오.\n"
              "(가) [[f(5) > f(7) > f(9)]]\n"
              "(나) [[f(1) < f(3)]]"),
    choices=None, derived_answer="100", figure=None, difficulty_est=3, confidence=0.85,
    note="(가) ₅C₃=10, (나) ₅C₂=10 → 100. 빠른정답 240과 불일치.")

# p97
add(id="0465605c", qtype="short",
    question=("함수 [[f(x) = -abs(x + 1) + 1]]에 대하여\n"
              "[[pow(f,1)]]([[x]]) = [[f(x)]], [[pow(f, n + 1)]]([[x]]) = ([[comp(f, pow(f,n))]])([[x]])\n"
              "([[n]] = 1, 2, 3, ⋯)\n"
              "으로 정의할 때, [[y]] = [[pow(f,n)]]([[x]])의 그래프와 [[x]]축으로 둘러싸인 "
              "도형의 넓이는 [[a n + b]]이다. 이때 상수 [[a]], [[b]]에 대하여 "
              "[[pow(a,2) + pow(b,2)]]의 값을 구하시오."),
    choices=None, derived_answer="5", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="문법 범위 밖: 합성함수 거듭제곱 fⁿ(x)·(f∘fⁿ)(x) 적용 표기 → 텍스트 혼합 전사",
    note="fⁿ의 그래프와 x축 사이 넓이 = 2n−1 (수치 확인: n=1..5 → 1,3,5,7,9) → a=2, b=−1 → 5 = 빠른정답 ✓.")

# ===================== 평행이동 =====================
# p2
add(id="1f49e6fa", qtype="choice",
    question=("평행이동 " + MOVE.format(x="x + 1", y="y - 2") + "에 의하여\n점 [[point(1, 2)]]가 옮겨진 점의 좌표는?"),
    choices=CH_NUM("point(2, 1)", "point(2, 0)", "point(-2, 1)", "point(0, 4)", "point(1, -2)"),
    derived_answer="②", figure=None, difficulty_est=1,
    note="(1+1, 2−2)=(2, 0) → ② = 빠른정답 ✓.")

# p9
add(id="244548d0", qtype="choice",
    question=("평행이동 " + MOVE.format(x="x + 3", y="y + 5") + "에 의하여\n점 [[point(-7, -9)]]가 점 [[point(a, b)]]로 옮겨질 때, "
              "[[a + b]]의 값을 구하면?"),
    choices=CH_NUM("-10", "-9", "-8", "-7", "-6"),
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.85,
    note="(−4, −4) → a+b=−8 → ③. 빠른정답 1과 불일치.")

# p11
add(id="13cbef2e", qtype="choice",
    question=("평행이동 " + MOVE.format(x="x - 3", y="y + 2") + "에 의하여\n점 [[point(2, 3)]]이 점 [[point(a, b)]]로 옮겨질 때, "
              "[[a + b]]의 값을 구하면?"),
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="④", figure=None, difficulty_est=1,
    note="(−1, 5) → a+b=4 → ④ = 빠른정답 ✓.")

# p13
add(id="5a565d68", qtype="choice",
    question=("평행이동 " + MOVE.format(x="x - 5", y="y + 3") + "에 의하여\n점 [[point(4, a)]]가 직선 [[y = 4x + 9]] 위의 점으로 옮겨질 때,\n"
              "[[a]]의 값은?"),
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.85,
    note="(−1, a+3)이 y=4x+9 위: a+3=5 → a=2 → ②. 빠른정답 3과 불일치.")

# p20
add(id="54659a11", qtype="choice",
    question=("평행이동 [[f]]: " + MOVE.format(x="x + a", y="y + b") + "에 의하여\n점 [[point(3, 5)]]가 점 [[point(-1, 7)]]로 옮겨질 때, "
              "평행이동 [[f]]에\n의하여 원점으로 옮겨지는 점의 좌표는?"),
    choices=CH_NUM("point(4, -2)", "point(2, 2)", "point(2, 0)", "point(-2, 2)", "point(4, 2)"),
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.85,
    note="a=−4, b=2 → 원점의 원상 (4, −2) → ①. 빠른정답 10과 불일치(선지 범위 밖).")

# p23
add(id="7965a694", qtype="choice",
    question=("평행이동 [[f]]: " + MOVE.format(x="x + a", y="y + b") + "에 의해\n점 [[point(-1, 2)]]가 점 [[point(6, 3)]]으로 옮겨질 때, "
              "평행이동 [[f]]에\n의해 원점으로 옮겨지는 점의 좌표는?"),
    choices=CH_NUM("point(7, -1)", "point(7, 1)", "point(-7, -1)", "point(-7, 1)", "point(7, 2)"),
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.85,
    note="a=7, b=1 → 원점의 원상 (−7, −1) → ③. 빠른정답 1과 불일치.")

# p26
add(id="7b4d843a", qtype="short",
    question=("평행이동 " + MOVE.format(x="x + p", y="y + q") + "에 의하여\n점 [[point(1, -5)]]가 점 [[point(3, 2)]]로 옮겨진다. 이 평행이동에\n"
              "의하여 원점으로 옮겨지는 점 P의 좌표를 [[point(a, b)]]라 할 때,\n[[a b]]의 값을 구하시오."),
    choices=None, derived_answer="14", figure=None, difficulty_est=1, confidence=0.85,
    note="p=2, q=7 → P(−2, −7) → ab=14. 빠른정답 3과 불일치.")

# p32
add(id="1bd353eb", qtype="short",
    question=("점 [[point(3, 1)]]을 점 [[point(5, 4)]]로 옮기는\n평행이동 " + MOVE.format(x="x + a", y="y + b") + "에 의하여\n"
              "직선 [[2x - 5y + 3 = 0]]이 점 [[point(3, c)]]를 지나는 직선으로\n옮겨진다고 한다. 이때 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="9", figure=None, difficulty_est=2, confidence=0.85,
    note="a=2, b=3; 옮긴 직선 2x−5y+14=0에 (3, c) 대입 → c=4 → 9. 빠른정답 21과 불일치.")

# p33
add(id="de233119", qtype="short",
    question=("점 [[point(-1, 4)]]를 점 [[point(3, 2)]]로 옮기는\n평행이동 " + MOVE.format(x="x + a", y="y + b") + "에 의하여\n"
              "직선 [[x + 3y - 10 = 0]]이 점 [[point(c, 2)]]를 지나는 직선으로\n옮겨진다고 한다. 이때 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.85,
    note="a=4, b=−2; 옮긴 직선 x+3y−8=0에 (c, 2) 대입 → c=2 → 4. 빠른정답 1과 불일치.")

# p34
add(id="f178e7b7", qtype="choice",
    question=("평행이동 " + MOVE.format(x="x - 1", y="y + 1") + "에 의하여\n직선 [[y = m x + n]]을 옮기면 직선 [[x - 2y + 1 = 0]]과\n"
              "[[y]]축 위에서 수직으로 만날 때, 상수 [[m]], [[n]]의 곱 [[m n]]의\n값은?"),
    choices=CH_NUM("3", "1", "-1", "-3", "-5"),
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="옮긴 직선 y=mx+m+n+1; 수직 → m=−2, y축 교점 (0, 1/2) 통과 → n=3/2 → mn=−3 → ④. 빠른정답 '-3'은 값 기준(선지 ④와 같은 값).")

# p35
add(id="e0514e73", qtype="choice",
    question=("평행이동 " + MOVE.format(x="x - 4", y="y") + "에 의하여\n직선 [[y = m x + n]]을 옮기면 직선 [[3x - y + 5 = 0]]과\n"
              "[[x]]축 위에서 수직으로 만날 때, 상수 [[m]], [[n]]에 대하여\n[[81(pow(m,2) + pow(n,2))]]의 값은?"),
    choices=CH_NUM("54", "58", "62", "66", "70"),
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="옮긴 직선 y=mx+4m+n; 수직 → m=−1/3, x축 교점 (−5/3, 0) 통과 → n=7/9 → 81(1/9+49/81)=58 → ②. 빠른정답 9와 불일치.")

# p46
_CPRIME = ("두 {AB} [[a]], [[b]]에 대하여 원 [[C]]: [[pow(x - {h}, 2) + pow(y, 2) = pow(r, 2)]]을\n"
           "[[x]]축의 방향으로 [[a]]만큼, [[y]]축의 방향으로 [[b]]만큼 평행이동한\n"
           "원을 [[prime(C)]]이라 할 때, 두 원 [[C]], [[prime(C)]]이 다음 조건을 만족시킨다.\n"
           "(가) 원 [[prime(C)]]은 원 [[C]]의 중심을 지난다.\n"
           "(나) 직선 [[{line} = 0]]은 두 원 [[C]], [[prime(C)]]에 모두\n접한다.\n")
_CPRIME_RV = "문법 범위 밖: 프라임 라벨 C′을 prime(C)(도함수 기호)로 표기 → 검토 필요"
add(id="13cc5969", qtype="short",
    question=_CPRIME.format(AB="양수", h="1", line="4x - 3y + 21") + "[[a + b + r]]의 값을 구하시오. (단, [[r]]는 양수이다.)",
    choices=None, derived_answer="12", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=_CPRIME_RV,
    note="출처 [2022년 3월 고2 27번/4점]. r=5(중심 (1,0)과 직선 거리), a²+b²=25, 4a−3b=0 → a=3, b=4 → 12. 빠른정답 4와 불일치.")

# p47
add(id="d17a802f", qtype="short",
    question=("원 [[pow(x - 1, 2) + pow(y - 2, 2) = 4]]를 원 [[pow(x + 3, 2) + pow(y, 2) = 4]]로\n"
              "옮기는 평행이동에 의하여 직선 [[2x - y + 3 = 0]]이\n"
              "직선 [[a x + b y + c = 0]]으로 옮겨질 때, 상수 [[a]], [[b]], [[c]]에\n대하여 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=2,
    note="평행이동 (−4, −2): 2(x+4)−(y+2)+3=0 → 2x−y+9=0 → a+b+c=10 = 빠른정답 ✓.")

# p48
add(id="b50bb5b9", qtype="short",
    question=("원 [[pow(x + 2, 2) + pow(y - 5, 2) = 4]]가\n평행이동 " + MOVE.format(x="x - a", y="y - b") + "에 의하여\n"
              "원 [[pow(x,2) + pow(y,2) - 2x - 14y + 46 = 0]]으로 옮겨질 때, [[a b]]의\n값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.85,
    note="옮긴 원 (x−1)²+(y−7)²=4: 중심 (−2,5)→(1,7) → −2−a=1, 5−b=7 → a=−3, b=−2 → ab=6. 빠른정답 4와 불일치.")

# p51
add(id="91164e9f", qtype="short",
    question=("원 [[pow(x - 1, 2) + pow(y + 2, 2) = 16]]이\n평행이동 " + MOVE.format(x="x - a", y="y - b") + "에 의하여\n"
              "원 [[pow(x,2) + pow(y,2) - 6x - 7 = 0]]으로 옮겨질 때,\n[[a b]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=2,
    note="옮긴 원 (x−3)²+y²=16: 중심 (1,−2)→(3,0) → a=−2, b=−2 → ab=4 = 빠른정답 ✓.")

# p52
add(id="e4daaa9c", qtype="short",
    question=("원 [[pow(x,2) + pow(y,2) + 6x - 6y + 9 = 0]]과 이 원이\n평행이동 " + MOVE.format(x="x + 3", y="y + a") + "에 의하여 옮겨지는\n"
              "원이 만나는 두 점을 A, B라 하면 [[seg(AB) = 2]]이다.\n이때 모든 [[a]]의 값의 곱을 구하시오."),
    choices=None, derived_answer="-23", figure=None, difficulty_est=3,
    note="반지름 3, 중심 거리 d=√(9+a²); 공통현 2 → 중심에서 현까지 2√2=d/2 → a²=23 → 곱 −23 = 빠른정답 ✓.")

# p53
add(id="ee519531", qtype="short",
    question=_CPRIME.format(AB="실수", h="2", line="3x + 4y + 14") +
             "[[2a + b + r]]의 값을 구하시오. (단, [[a]], [[r]]는 양수이다.)",
    choices=None, derived_answer="8", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=_CPRIME_RV,
    note="출처 [2022년 3월 고2 27번 변형]. r=4, a²+b²=16, 3a+4b=0(a>0) → a=16/5, b=−12/5 → 2a+b+r=8. 빠른정답 5와 불일치. 원문 '(단, a ,r는 양수이다.)' 띄어쓰기 오타는 보정.")

# p59 (도형)
add(id="721eca1a", qtype="short",
    question=("다음 그림과 같이 좌표평면에서 원 [[sub(C,1)]]: [[pow(x,2) + pow(y,2) = 25]]를\n"
              "[[x]]축의 방향으로 3만큼, [[y]]축의 방향으로 [[-1]]만큼\n"
              "평행이동한 원을 [[sub(C,2)]]라 하자. 원 [[sub(C,1)]]과 직선\n"
              "[[3x - y - 10 = 0]]이 만나는 두 점 A, B를 [[x]]축의 방향으로\n"
              "3만큼, [[y]]축의 방향으로 [[-1]]만큼 평행이동한 점을 각각 C,\nD라 하자.\n"
              "선분 AC, 선분 BD, 호 AB 및 호 CD로 둘러싸인 색칠된\n"
              "부분의 넓이를 [[S]]라 할 때, [[pow(S,2)]]의 값을 구하시오."),
    choices=None, derived_answer="600",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O 중심 원 C₁, 오른쪽 아래로 평행이동한 원 C₂, 직선 3x−y−10=0이 C₁과 만나는 점 A(위)·B(아래), 그 평행이동 점 C·D(C₂ 위); 선분 AC·BD와 호 AB·호 CD로 둘러싸인 부분 색칠"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 좌표평면 두 원+직선+색칠 영역 복합 도형",
    note="출처 [2017년 3월 고2 문과 28번 변형]. 색칠 부분 = 현 AB(=2√15)를 (3,−1)로 평행이동한 자취 → 평행사변형 넓이 2√15·√10=10√6 → S²=600. 빠른정답 40과 불일치.")

# p72
add(id="a65731eb", qtype="short",
    question=("포물선 [[y = -pow(x,2) + 6x]]를 [[x]]축의 방향으로 [[-2]]만큼,\n[[y]]축의 방향으로 [[-3]]만큼 평행이동하면 직선 [[y = a x]]와\n"
              "두 점 P, Q에서 만난다. 선분 PQ의 중점이 원점일 때,\n상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2,
    note="옮긴 포물선 y=−x²+2x+5; x²+(a−2)x−5=0의 두 근의 합 0 → a=2 = 빠른정답 ✓.")

# p88
add(id="349e8fcf", qtype="choice",
    question=("원 [[sub(C,1)]]: [[pow(x,2) + pow(y,2) = 12]]를 [[x]]축의 방향으로 [[k]]만큼,\n"
              "[[y]]축의 방향으로 [[k]]만큼 평행이동한 원을 [[sub(C,2)]]라 하자.\n"
              "점 [[A(-2, -2)]]에서 원 [[sub(C,2)]]에 그은 두 접선이 서로\n수직일 때, 상수 [[k]]의 값은? (단, [[k > 1]])"),
    choices=CH_NUM("-1 + sqrt(3)", "-1 + 2 sqrt(3)", "-1 + 3 sqrt(3)", "-2 + sqrt(3)", "-2 + 2 sqrt(3)"),
    derived_answer="⑤", figure=None, difficulty_est=3,
    note="출처 [2019년 9월 고1 15번 변형]. 접선 수직 ⇔ 중심 (k,k)까지 거리 = √2·r=2√6 → √2|k+2|=2√6 → k=−2+2√3 → ⑤ = 빠른정답 ✓.")
