# -*- coding: utf-8 -*-
# esc_sonnet_h3-2_1of4 — 이미지 기준 전사 (84 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_G = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
PRIME_NOTE = "도함수 적용 표기 prime(f)(x) 우회"

# ───────── 치환적분법 ─────────
add(id="0bf8fd62", qtype="choice",
    question="등식 [[integ(pow(-x + 3, 4), x) = frac(1,a) pow(-x + 3, b) + C]]가 성립할 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값은? (단, [[C]]는 적분상수이다.)",
    choices=["[[-10]]", "[[-5]]", "[[0]]", "[[5]]", "[[10]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="-(1/5)(-x+3)^5 → a=-5, b=5 → 0 → ③.")

add(id="e78c7b35", qtype="choice",
    question="[[integ(pow(3x + 2, 6), x) = frac(1,a) pow(3x + 2, b) + C]]일 때, 상수 [[a]], [[b]]에 대하여 [[a - b]]의 값은? (단, [[C]]는 적분상수)",
    choices=["[[12]]", "[[14]]", "[[16]]", "[[17]]", "[[18]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(1/21)(3x+2)^7 → a=21, b=7 → 14 → ②.")

add(id="b9cec3a2", qtype="choice",
    question="[[0 < x < 1]]일 때,\n[[f(x) = 1 + (x - 1) + pow(x - 1, 2) + pow(x - 1, 3)]] + ⋯로 정의되는 함수 [[f(x)]]의 한 부정적분을 [[F(x)]]라 하자.\n[[F(frac(1,2)) = ln(2) - ln(3)]]일 때, [[F(2 - sqrt(e))]]의 값은?",
    choices=["[[-frac(1,2)]]", "[[-frac(1,4)]]", "[[0]]", "[[frac(1,2)]]", "[[frac(1,4)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="f(x)=1/(2-x), F(x)=-ln(2-x)+C, C=0 → F(2-√e)=-1/2 → ①.")

add(id="18e748a3", qtype="short",
    question="함수 [[f(x) = integ(pow(e, 2 cos(x)) sin(x), x)]]에 대하여\n[[f(0) = -frac(1,2) pow(e,2)]]일 때, [[f(frac(pi,2))]]의 값을 구하시오.",
    choices=None, derived_answer="-frac(1,2)", figure=None, difficulty_est=2, confidence=0.9,
    note="f(x)=-(1/2)e^{2cos x}+C, C=0 → f(π/2)=-1/2. 빠른정답 pm(frac(1,2))는 부호 표기 오류로 보임.")

add(id="fdb87206", qtype="short",
    question="[[0 < x < 2 pi]]에서 정의된 미분가능한 함수 [[f(x)]]가 [[f(0) = ln(3)]]이고 [[prime(f)(x) pow(e, f(x)) = -sin(x)]]를 만족시킨다.\n함수 [[f(x)]]가 [[x = a]]에서 극솟값 [[b]]를 가질 때, [[frac(a × pow(e,b), pi)]]의 값을 구하시오.",
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PRIME_NOTE,
    note="e^{f(x)}=cos x+2 → f=ln(cos x+2), 극소 x=π, b=0 → 1.")

add(id="532d99b2", qtype="choice",
    question="[[sub(a,n) = dinteg(0, frac(pi,4), pow(tan(x), n), x)]] ([[n]] = 1, 2, 3, ⋯)\n으로 정의할 때, 옳은 내용을 <보기>에서 모두 고른 것은?\n<보기>\nㄱ. [[sub(a,1) + sub(a,3) = frac(1,2)]]\nㄴ. [[sub(a,1) + sub(a,2) + sub(a,3) + sub(a,4) = frac(1,2) + frac(1,3)]]\nㄷ. [[sum(k, 1, 100, sub(a,k)) = frac(1,2) + frac(1,3) + frac(1,4)]] + ⋯ + [[frac(1,51)]]",
    choices=CH_G, derived_answer="③", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2006년 10월 고3 이과 미분과 적분 28번]. a_n+a_{n+2}=1/(n+1) → ㄱ✓ ㄴ✓, ㄷ은 1/2+1/3+1/6+1/7+… 꼴이라 ✗ → ③.")

dup(["f585f17a", "5ec82a6b", "6ccf6476"], qtype="choice",
    question="자연수 [[n]]에 대하여 [[sub(a,n) = dinteg(0, frac(pi,3), pow(tan(x), n), x)]]일 때, 보기에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[sub(a,1) + sub(a,3) = frac(3,2)]]\nㄴ. [[sub(a,1) + sub(a,2) + sub(a,3) + sub(a,4) = frac(3,2) + sqrt(3)]]\nㄷ. [[sum(k, 1, 20, frac(sub(a, 4k - 2) + sub(a, 4k), sub(a, 4k - 3) + sub(a, 4k - 1)))]] = [[sqrt(3)]]([[frac(2,3) + frac(6,7) + frac(10,11)]] + ⋯ + [[frac(78,79)]])",
    choices=CH_G, derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.9,
    note="a_n+a_{n+2}=(√3)^{n+1}/(n+1) → ㄱ 3/2 ✓, ㄴ 3/2+√3 ✓, ㄷ 각 항 √3(4k-2)/(4k-1) ✓ → ⑤.")

# ───────── 부분적분법 ─────────
add(id="13594afe", qtype="choice",
    question="실수 전체의 집합에서 연속인 함수 [[f(x)]]의 도함수 [[prime(f)(x)]]가 [[prime(f)(x)]] = { [[2x + 5]] ([[x < 1]]) ; [[2 ln(x)]] ([[x > 1]]) }이다.\n[[f(e) = 3]]일 때, [[f(-8)]]의 값은?",
    choices=["[[15]]", "[[17]]", "[[19]]", "[[21]]", "[[23]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="조각적(경우 나눔) 정의 f′(x) / " + PRIME_NOTE,
    note="x>1: f=2xlnx-2x+3, f(1)=1; x<1: f=x²+5x-5 → f(-8)=19 → ③.")

add(id="971ca355", qtype="choice",
    question="실수 전체의 집합에서 연속인 함수 [[f(x)]]의 도함수 [[prime(f)(x)]]가 [[prime(f)(x)]] = { [[2x + 4]] ([[x < 1]]) ; [[4 ln(x)]] ([[x > 1]]) }이다.\n[[f(e) = 5]]일 때, [[f(-5)]]의 값은?",
    choices=["[[1]]", "[[3]]", "[[5]]", "[[7]]", "[[9]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="조각적(경우 나눔) 정의 f′(x) / " + PRIME_NOTE,
    note="x>1: f=4xlnx-4x+5, f(1)=1; x<1: f=x²+4x-4 → f(-5)=1 → ①.")

add(id="0278ac18", qtype="choice",
    question="연속함수 [[f(x)]]가 [[f(x) = pow(e, 2 pow(x,2)) + dinteg(0, 1, t f(t), t)]]를\n만족시킬 때, [[dinteg(0, 1, x f(x), x)]]의 값은?",
    choices=["[[frac(pow(e,2) - 2, 3)]]", "[[frac(pow(e,2) - 1, 2)]]", "[[frac(pow(e,2), 2)]]", "[[frac(pow(e,2) + 1, 2)]]", "[[frac(pow(e,2) + 2, 3)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="k=∫₀¹xf(x)dx=(e²-1)/4+k/2 → k=(e²-1)/2 → ②. 빠른정답 3과 불일치.")

add(id="3de54f75", qtype="short",
    question="실수 전체의 집합에서 연속인 함수 [[f(x)]]가 모든 실수 [[x]]에 대하여\n[[dinteg(0, x, t f(t), t) - x dinteg(0, x, f(t), t) = a pow(e, 3x) - 9x + b]]\n를 만족시킬 때, [[f(a) f(b)]]의 값을 구하시오.\n(단, [[a]], [[b]]는 상수이다.)",
    choices=None, derived_answer="729", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2018년 3월 고3 이과 27번 변형]. x=0: a+b=0; 미분 후 x=0: a=3, b=-3; f(x)=-27e^{3x} → f(3)f(-3)=729.")

# ───────── 넓이 ─────────
dup(["fcd883a1", "ced39667"], qtype="choice",
    question="함수 [[f(x) = pow(e, -x)]]과 자연수 [[n]]에 대하여 점 [[sub(P,n)]], [[sub(Q,n)]]을 각각 [[sub(P,n)]][[point(n, f(n))]], [[sub(Q,n)]][[point(n + 1, f(n))]]이라 하자.\n삼각형 [[sub(P,n)]][[sub(P,n+1)]][[sub(Q,n)]]의 넓이를 [[sub(A,n)]], 선분 [[sub(P,n)]][[sub(P,n+1)]]과 함수 [[y = f(x)]]의 그래프로 둘러싸인 도형의 넓이를 [[sub(B,n)]]이라 할 때, <보기>에서 옳은 것을 모두 고른 것은?\n<보기>\nㄱ. [[dinteg(n, n + 1, f(x), x) = f(n) - (sub(A,n) + sub(B,n))]]\nㄴ. [[sum(n, 1, inf, sub(A,n)) = frac(1, 2e)]]\nㄷ. [[sum(n, 1, inf, sub(B,n)) = frac(3 - e, 2e(e - 1))]]",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 f(x)=e^{-x}, 점 P_n(n,f(n))·Q_n(n+1,f(n))·P_{n+1}, 삼각형 P_nP_{n+1}Q_n 음영(A_n), 선분과 곡선 사이 빗금(B_n), x축 n, n+1 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 지수함수 그래프+삼각형 좌표평면 도형 / 첨자 점 라벨(P_n, Q_n) 텍스트 혼합",
    note="출처 [2005년 11월 고3 이과 미분과 적분 28번]. ㄱ 직사각형-(A_n+B_n) ✓, ㄴ ΣA_n=1/(2e) ✓, ㄷ B_n=e^{-n}(3-e)/(2e) → 합 (3-e)/(2e(e-1)) ✓ → ⑤. 빠른정답 4와 불일치.")

add(id="25f6155a", qtype="choice",
    question="실수 전체의 집합에서 미분가능한 함수 [[f(x)]]의 도함수 [[prime(f)(x)]]가 [[prime(f)(x) = -x + pow(e, 1 - pow(x,2))]]이다.\n양수 [[t]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[point(t, f(t))]]에서의 접선과 곡선 [[y = f(x)]] 및 [[y]]축으로 둘러싸인 부분의 넓이를 [[g(t)]]라 하자. [[g(1) + prime(g)(1)]]의 값은?",
    choices=["[[frac(1,2) e + frac(1,2)]]", "[[frac(1,2) e + frac(2,3)]]", "[[frac(1,2) e + frac(5,6)]]", "[[frac(2,3) e + frac(1,2)]]", "[[frac(2,3) e + frac(2,3)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PRIME_NOTE,
    note="출처 [2024년 11월 고3 미적분 28번/4점]. g(1)=∫₀¹uf′(u)du=e/2-5/6, g′(1)=-(1/2)f″(1)=3/2 → e/2+2/3 → ②. 빠른정답 1과 불일치.")

add(id="f361ea75", qtype="choice",
    question="실수 전체의 집합에서 미분가능한 함수 [[f(x)]]의 도함수 [[prime(f)(x)]]가 [[prime(f)(x) = -3x + 2 pow(e, 4 - pow(x,2))]]이다.\n양수 [[t]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[point(t, f(t))]]에서의 접선과 곡선 [[y = f(x)]] 및 [[y]]축으로 둘러싸인 부분의 넓이를 [[g(t)]]라 하자. [[g(2) + prime(g)(2)]]의 값은?",
    choices=["[[frac(1,2) pow(e,4) + 21]]", "[[frac(1,2) pow(e,4) + 23]]", "[[frac(1,2) pow(e,4) + 25]]", "[[pow(e,4) + 21]]", "[[pow(e,4) + 23]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PRIME_NOTE,
    note="출처 [2024년 11월 고3 미적분 28번 변형]. g(2)=∫₀²uf′(u)du+8=e⁴-1, g′(2)=-2f″(2)=22 → e⁴+21 → ④. 빠른정답 2와 불일치.")

add(id="02f04a1b", qtype="choice",
    question="함수 [[y = pow(e, x - 1)]]의 그래프와 [[x]]축, [[y]]축 및 직선 [[x = 1]]로 둘러싸인 영역의 넓이가 직선 [[y = a x]] ([[0 < a < 1]])에 의하여 이등분될 때, 상수 [[a]]의 값은?",
    choices=["[[1 - frac(3, 2e)]]", "[[1 - frac(1, e)]]", "[[1 - frac(1, 2e)]]", "[[1 - frac(1, 3e)]]", "[[1 - frac(2, e)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="전체 넓이 1-1/e, 직선 아래 삼각형 a/2 → a=1-1/e → ②.")

# ───────── 함수의 그래프 ─────────
add(id="ce2f5ce5", qtype="choice",
    question="함수 [[f(x) = 4 pow(x,2) - k x + ln(x)]]가 극값을 갖도록 하는 정수 [[k]]의 최솟값은?",
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="8x²-kx+1=0이 양의 서로 다른 두 근: k>4√2≈5.66 → 6 → ②. 빠른정답 91과 불일치(정렬 오류로 보임).")

add(id="0ed5a4c1", qtype="choice",
    question="두 함수 [[f(x)]], [[g(x)]]가 실수 전체의 집합에서 이계도함수를 갖고 [[g(x)]]가 증가함수일 때, 함수 [[h(x)]]를 [[h(x)]] = ([[comp(f, g)]])([[x]])라 하자.\n점 [[point(-2, 4)]]가 곡선 [[y = g(x)]]의 변곡점이고 [[frac(prime(h,2)(-2), prime(f,2)(4)) = 9]]이다. [[prime(f)(4) = 2]]일 때, [[prime(h)(-2)]]의 값은?",
    choices=["[[8]]", "[[7]]", "[[6]]", "[[5]]", "[[4]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="합성함수 적용 표기 (f∘g)(x) / " + PRIME_NOTE,
    note="출처 [2020년 7월 고3 이과 15번 변형]. h″(-2)=f″(4)g′(-2)² → g′(-2)=3 → h′(-2)=f′(4)·3=6 → ③. 빠른정답 1과 불일치.")

dup(["3c650603", "1998723c"], qtype="choice",
    question="실수 전체의 집합에서 함수 [[f(x)]]가 미분가능하고 도함수 [[prime(f)(x)]]가 연속이다. [[x]]축과의 교점이 [[x]]좌표가 [[b]], [[c]], [[d]]뿐인 함수 [[g(x) = frac(prime(f)(x), x)]]의 그래프가 그림과 같을 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. 함수 [[f(x)]]는 열린 구간 [[itv(c, 0, oo)]]에서 감소한다.\nㄴ. 함수 [[f(x)]]는 [[x = c]]에서 극댓값을 갖는다.\nㄷ. 함수 [[f(x)]]는 닫힌 구간 [[itv(a, e, cc)]]에서 3개의 극값을 갖는다.",
    choices=CH_G, derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=g(x) 그래프. x<0에서 a<b<c<0, g는 a에서 양, b·c에서 x축 교차, (b,c)에서 음, x→0⁻에서 +∞; x>0에서 -∞로부터 증가, d에서 교차 후 양, e 부근 완만"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: y=g(x) 그래프 / " + PRIME_NOTE,
    note="f′=xg: (b,c)에서 +, (c,0)·(0,d)에서 −, (d,e)에서 + → ㄱ✓ ㄴ✓ ㄷ b,c,d 3개 ✓ → ⑤.")

add(id="b5e1f806", qtype="choice",
    question="실수 전체의 집합에서 함수 [[f(x)]]가 미분가능하고 도함수 [[prime(f)(x)]]가 연속이다. [[x]]축과의 교점이 [[x]]좌표가 [[b]], [[c]], [[d]]뿐인 함수 [[g(x) = frac(prime(f)(x), x)]]의 그래프가 그림과 같을 때, 옳은 것만을 <보기>에서 있는 대로 고른 것은?\n<보기>\nㄱ. 함수 [[f(x)]]는 열린 구간 [[itv(b, 0, oo)]]에서 증가한다.\nㄴ. 함수 [[f(x)]]는 [[x = b]]에서 극솟값을 갖는다.\nㄷ. 함수 [[f(x)]]는 닫힌 구간 [[itv(a, e, cc)]]에서 4개의 극값을 갖는다.",
    choices=CH_G, derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=g(x) 그래프. x<0에서 a<b<0, g는 x<b에서 양(a 부근 극대), b에서 교차 후 음, x→0⁻에서 -∞; x>0에서 +∞로부터 감소, c에서 교차 후 음(극소), d에서 교차 후 양으로 증가, e 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: y=g(x) 그래프 / " + PRIME_NOTE,
    note="출처 [2013년 7월 고3 이과 18번/4점]. f′=xg: (a,b) −, (b,c) +, (c,d) −, (d,e) + → ㄱ✓ ㄴ✓, 극값 b,c,d 3개 → ㄷ✗ → ③. 빠른정답 5와 불일치.")

add(id="10cc3277", qtype="choice",
    question="함수 [[f(x)]] = { [[pow(x - 1, 2) pow(e, x) + k]] ([[x >= 0]]) ; [[-pow(x,2)]] ([[x < 0]]) }에 대하여 함수 [[g(x) = abs(f(x)) - f(x)]]가 다음 조건을 만족하도록 하는 [[k]]의 값의 범위는?\n(가) 함수 [[g(x)]]는 모든 실수에서 연속이다.\n(나) 함수 [[g(x)]]는 미분가능하지 않은 점이 2개이다.",
    choices=["[[k < -2]]", "[[k <= -1]]", "[[k < 0]]", "[[-1 <= k < 0]]", "[[0 < k < 1]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="조각적(경우 나눔) 정의 f(x)",
    note="연속: k≥-1; 미분불가점 2개: f가 x≥0에서 0을 가로지르는 점 2개 → -1≤k<0 → ④. 빠른정답 1과 불일치.")

add(id="50c4db95", qtype="short",
    question="다음 그림과 같이 좌표평면에 점 A[[point(2, 0)]]을 중심으로 하고 반지름의 길이가 2인 원이 있다. 원 위의 점 Q에 대하여 [[angle(AOQ) = theta]] ([[0 < theta < frac(pi,3)]])라 할 때, 선분 OQ 위에 [[seg(PQ) = 1]]인 점 P를 정한다. 점 P의 [[y]]좌표가 최대가 될 때 [[cos(theta) = frac(a + sqrt(b), 16)]]이다. [[a + b]]의 값을 구하시오.\n(단, O는 원점이고, [[a]]와 [[b]]는 자연수이다.)",
    choices=None, derived_answer="130",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 중심 A(2,0) 반지름 2인 원(원점 통과), 원 위의 점 Q, 선분 OQ 위의 점 P(PQ=1), ∠AOQ=θ 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 원+선분 도형",
    note="출처 [2017년 6월 고3 이과 26번 변형]. OQ=4cosθ, y_P=(4cosθ-1)sinθ, 8cos²θ-cosθ-4=0 → cosθ=(1+√129)/16 → 130. 빠른정답 22와 불일치.")

# ───────── 음함수와 역함수의 미분법 ─────────
add(id="cf9f9f54", qtype="choice",
    question="음함수 [[3x + y - 2x y = 1]]에서 [[x = 2]]일 때의 [[dydx(y,x)]]의 값은?",
    choices=["[[-frac(1,3)]]", "[[-frac(1,9)]]", "[[0]]", "[[frac(1,9)]]", "[[frac(1,3)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="x=2 → y=5/3; y′=(2y-3)/(1-2x)=-1/9 → ②.")

add(id="f18c0e37", qtype="short",
    question="함수 [[2 sqrt(x) - sqrt(y) = 0]] ([[x > 0]], [[y > 0]])에 대하여\n[ [[dydx(y,x)]] ] ([[x = 2]], [[y = 8]])의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="원문은 [dy/dx]에 아래첨자 x=2, y=8 표기. y′=2√y/√x=4.")

add(id="50fae1ed", qtype="choice",
    question="곡선 [[pow(x,2) y - pow(y,2) ln(x) = 3]]에 대하여 [[x = 1]]일 때, [[dydx(y,x)]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 7월 고3 이과 8번 변형]. x=1 → y=3; 6+y′-9=0 → y′=3 → ③.")

add(id="713a6cf4", qtype="choice",
    question="음함수 [[sqrt(x) + sqrt(y) = 3 sqrt(3)]]에 대하여 [[x = 3]], [[y = 12]]일 때의 [[dydx(y,x)]]의 값은?",
    choices=["[[-12]]", "[[-6]]", "[[-4]]", "[[-3]]", "[[-2]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="y′=-√y/√x=-√12/√3=-2 → ⑤. 빠른정답 4와 불일치.")

add(id="38c4541f", qtype="choice",
    question="음함수 [[x y + 2(x + y) = 5]]에서 [[x = 1]]일 때의 [[dydx(y,x)]]의 값은?",
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="x=1 → y=1; y′=-(y+2)/(x+2)=-1 → ②.")

add(id="07f426c1", qtype="short",
    question="곡선 [[pow(x,2) y + frac(1,4)(x + y) = 8]]에서 [[x = -2]]일 때의\n[[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(31,17)", figure=None, difficulty_est=2, confidence=0.9,
    note="x=-2 → y=2; y′(x²+1/4)=-2xy-1/4 → 31/17.")

add(id="64890c5f", qtype="choice",
    question="곡선 [[pow(x,3) + a x - b pow(y,3) = 0]] 위의 점 [[point(1, -2)]]에서의 [[dydx(y,x)]]의 값이 [[-frac(5,6)]]일 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?",
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="1+a+8b=0, (3+a)/(12b)=-5/6 → a=7, b=-1 → 6 → ②.")

add(id="bc3e1494", qtype="choice",
    question="곡선 [[cos(x y) = -x]] 위의 점 [[point(frac(1,2), frac(4,3) pi)]]에서의\n[[dydx(y,x)]]의 값은?",
    choices=["[[frac(4 sqrt(3) - 8 pi, 3)]]", "[[frac(2 sqrt(3) - 4 pi, 3)]]", "[[frac(sqrt(3) - 2 pi, 3)]]", "[[frac(2 sqrt(3) - 2 pi, 3)]]", "[[frac(sqrt(3) - pi, 3)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="sin(xy)(y+xy′)=1, xy=2π/3 → y′=2(2/√3-4π/3)=(4√3-8π)/3 → ①.")

add(id="cfed9fc9", qtype="choice",
    question="곡선 [[2 pow(x,2) + 3 pow(y,2) + a x y + b = 0]] 위의 점 [[point(2, 1)]]에서의\n[[dydx(y,x)]]의 값이 [[-3]]일 때, 상수 [[a]], [[b]]에 대하여 [[a - b]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="2a+b=-11, 8-18+a-6a=0 → a=-2, b=-7 → a-b=5 → ⑤. 빠른정답 2와 불일치.")

add(id="c9b667aa", qtype="choice",
    question="곡선 [[x + a pow(x,2) pow(y,2) + b = 0]] 위의 점 [[point(1, 2)]]에서의 [[dydx(y,x)]]의\n값이 [[-frac(9,4)]]일 때, 두 실수 [[a]], [[b]]의 곱 [[a b]]의 값은?",
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="1+4a+b=0, 1+a(8-9)=0 → a=1, b=-5 → ab=-5 → ①. 빠른정답 23과 불일치(정렬 오류로 보임).")

add(id="072c3e85", qtype="short",
    question="음함수 [[sqrt(x) - sqrt(y) = 2 sqrt(7)]]에 대하여\n[[x = 63]], [[y = 7]]일 때의 [[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(1,3)", figure=None, difficulty_est=2, confidence=0.9,
    note="y′=√y/√x=√7/√63=1/3.")

add(id="9091f494", qtype="short",
    question="음함수 [[sqrt(x) + sqrt(y) = 2 sqrt(3)]]에 대하여\n[[x = 3]], [[y = 3]]일 때의 [[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.9,
    note="y′=-√y/√x=-1.")

add(id="b642c2de", qtype="short",
    question="세 실수 [[a]], [[b]], [[k]]에 대하여 두 점 A[[point(a, a + k)]], B[[point(b, b + k)]]가 곡선 [[C]]: [[pow(x,2) - 2x y + 2 pow(y,2) = 15]] 위에 있다. 곡선 [[C]] 위의 점 A에서의 접선과 곡선 [[C]] 위의 점 B에서의 접선이 서로 수직일 때, [[pow(k,2)]]의 값을 구하시오.\n(단, [[a + 2k != 0]], [[b + 2k != 0]])",
    choices=None, derived_answer="5", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2023년 6월 고3 미적분 29번/4점]. 기울기 k/(a+2k), k/(b+2k); a,b는 t²+2kt+2k²-15=0의 두 근 → (a+2k)(b+2k)=2k²-15=-k² → k²=5. 빠른정답 1과 불일치.")

add(id="7ed7c375", qtype="choice",
    question="세 정수 [[k]] ([[k < -1]]), [[a]], [[b]] ([[1 < a < b]])에 대하여\n두 점 A[[point(a, b)]], B[[point(b, a)]]가\n곡선 [[C]]: [[pow(x,2) - x y + pow(y,2) + k = 0]] 위에 있다. 곡선 [[C]] 위의 점 A에서의 접선과 곡선 [[C]] 위의 점 B에서의 접선이 이루는 예각의 크기를 [[theta]]라 하자.\n[[seg(AB) = 6 sqrt(2)]], [[tan(theta) = frac(12,5)]]일 때, [[k + a + b]]의 값은?",
    choices=["[[-60]]", "[[-57]]", "[[-54]]", "[[-51]]", "[[-48]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2025년 10월 고3 미적분 27번 변형]. 두 기울기 곱 1, |m-1/m|=24/5, b-a=6 → m=1/5, a=3, b=9, k=-63 → -51 → ④.")

add(id="5ef3b89b", qtype="short",
    question="다음 그림과 같이 길이가 20 m인 장대가 지면에 수직인 벽에 걸쳐 있고, 이 장대의 한 끝은 벽을 따라 미끄러진다. 이 장대의 한 끝은 벽으로부터 [[x]] m 떨어진 지점에 있고, 다른 한 끝은 지면으로부터 [[y]] m 떨어진 지점에 있다.\n[[x = 16]]일 때, [[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="-frac(4,3)",
    figure=[{"fn": "unsupported", "args": {"raw": "벽에 기댄 길이 20 m 장대 삽화: 벽에서 바닥 끝까지 x m, 지면에서 벽 쪽 끝까지 y m 표시"}}],
    difficulty_est=2, confidence=0.85,
    note="x²+y²=400, x=16 → y=12, y′=-x/y=-4/3. 빠른정답 -1/3과 불일치.")

add(id="01426115", qtype="choice",
    question="함수 [[f(x)]]가 [[f(x)]] = { [[pow(x - a - 1, 2) pow(e, x)]] ([[x >= a]]) ; [[pow(e, 2a)(x - a) + pow(e, a)]] ([[x < a]]) }일 때,\n실수 [[t]]에 대하여 [[f(x) = t]]를 만족시키는 [[x]]의 최솟값을 [[g(t)]]라 하자. 함수 [[g(t)]]가 [[t = 4]]에서만 불연속일 때,\n[[frac(prime(g)(f(a + 1)), prime(g)(f(a + 7)))]]의 값은? (단, [[a]]는 상수이다.)",
    choices=["[[12 pow(e,6)]]", "[[16 pow(e,6)]]", "[[20 pow(e,6)]]", "[[12 pow(e,7)]]", "[[16 pow(e,7)]]"],
    derived_answer="④", figure=None, difficulty_est=5, confidence=0.75,
    needs_review="조각적(경우 나눔) 정의 f(x) / " + PRIME_NOTE,
    note="출처 [2024년 6월 고3 미적분 28번 변형]. 불연속점 t=e^a=4; g′(0)=e^{-2a}, g′(f(a+7))=1/(48e^{a+7}) → 48e^{7-a}=12e⁷ → ④. 빠른정답 3과 불일치.")

add(id="47035b70", qtype="short",
    question="[[0 < t < 10]]인 실수 [[t]]에 대하여\n곡선 [[y = pow(x,3) - 2 pow(x,2) - 8x + 6]]과 직선 [[y = t]]가 만나는 세 점 중에서 [[x]]좌표가 가장 큰 점의 좌표를 [[point(f(t), t)]], [[x]]좌표가 가장 작은 점의 좌표를 [[point(g(t), t)]]라 하자.\n[[h(t) = t × (f(t) - g(t))]]라 할 때, [[prime(h)(6)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(23,4)", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PRIME_NOTE,
    note="t=6: 교점 x=-2,0,4; f′(6)=1/24, g′(6)=1/12 → h′(6)=6+6(1/24-1/12)=23/4.")

# ───────── 합성함수의 미분법 ─────────
add(id="8d0ae140", qtype="short",
    question="미분가능한 두 함수 [[f(x)]], [[g(x)]]에 대하여 함수 [[h(x)]]를 [[h(x)]] = ([[comp(g, f)]])([[x]])라 하면\n[[lim(x, 1, frac(f(x) + 2, x - 1)) = 4]], [[lim(x, 1, frac(h(x) - 4, x - 1)) = 12]]일 때,\n[[g(-2) + prime(g)(-2)]]의 값을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="합성함수 적용 표기 (g∘f)(x) / " + PRIME_NOTE,
    note="f(1)=-2, f′(1)=4, h(1)=4=g(-2), h′(1)=g′(-2)·4=12 → g′(-2)=3 → 7. 빠른정답 2와 불일치.")

add(id="d5c11572", qtype="short",
    question="두 함수\n[[f(x)]] = { [[a x - a + 2]] ([[x >= 1]]) ; [[x]] ([[x < 1]]) }, [[g(x) = abs(pow(3, x - 1) + b)]]\n에 대하여 함수 [[h(x)]]를 [[h(x)]] = ([[comp(g, f)]])([[x]])라 하자.\n[[h(x)]]가 [[x = 1]]에서 미분가능할 때, 상수 [[a]], [[b]]에 대하여 [[6 a b]]의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=4, confidence=0.75,
    needs_review="조각적(경우 나눔) 정의 f(x) / 합성함수 적용 표기 (g∘f)(x)",
    note="연속: |3+b|=|1+b| → b=-2; 미분: 3a ln3=-ln3 → a=-1/3 → 6ab=4. 빠른정답 3과 불일치.")

add(id="11453899", qtype="short",
    question="두 함수\n[[f(x)]] = { [[a x - 2a + 3]] ([[x >= 2]]) ; [[x]] ([[x < 2]]) }, [[g(x) = abs(pow(3, x) + b)]]\n에 대하여 함수 [[h(x)]]를 [[h(x)]] = ([[comp(g, f)]])([[x]])라 하자. [[h(x)]]가 [[x = 2]]에서 미분가능할 때, 상수 [[a]], [[b]]에 대하여 [[3a - b]]의 값을 구하시오.",
    choices=None, derived_answer="17", figure=None, difficulty_est=4, confidence=0.75,
    needs_review="조각적(경우 나눔) 정의 f(x) / 합성함수 적용 표기 (g∘f)(x)",
    note="연속: |27+b|=|9+b| → b=-18; 미분: 27a ln3=-9 ln3 → a=-1/3 → 3a-b=17.")

add(id="8a2c9861", qtype="short",
    question="이차 이상의 다항함수 [[f(x)]]와 함수 [[g(x) = pow(e, -2 pow(x,2) + 4x)]]이 ([[comp(f, g)]])([[2]]) = 1, [[prime(comp(f, g))(2) = -4]]를 만족한다.\n다항식 [[f(x)]]를 [[pow(x - 1, 2)]]으로 나누었을 때의 나머지를 [[R(x)]]라 할 때, [[R(3)]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="합성함수 적용 표기 (f∘g)(2), (f∘g)′(2) / " + PRIME_NOTE,
    note="g(2)=1, g′(2)=-4 → f(1)=1, f′(1)=1 → R(x)=x → R(3)=3. 빠른정답 1과 불일치.")

add(id="c717ed73", qtype="short",
    question="이차 이상의 다항함수 [[f(x)]]와 함수 [[g(x) = pow(e, sin(x))]]이 ([[comp(f, g)]])([[0]]) = 1, [[prime(comp(f, g))(0) = 4]]를 만족한다.\n다항식 [[f(x)]]를 [[pow(x - 1, 2)]]으로 나눌 때의 나머지를 [[R(x)]]라 할 때, [[R(2)]]의 값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="합성함수 적용 표기 (f∘g)(0), (f∘g)′(0) / " + PRIME_NOTE,
    note="g(0)=1, g′(0)=1 → f(1)=1, f′(1)=4 → R(x)=4x-3 → R(2)=5. 빠른정답 4와 불일치.")

add(id="48c7503b", qtype="choice",
    question="이차 이상의 다항함수 [[f(x)]]와 함수 [[g(x) = pow(e, sin(x))]]에 대하여 ([[comp(f, g)]])([[0]]) = 2, [[prime(comp(f, g))(0) = 1]]이 성립한다.\n다항식 [[f(x)]]를 [[pow(x - 1, 2)]]으로 나누었을 때의 나머지를 [[R(x)]]라 할 때, [[R(3)]]의 값은?",
    choices=["[[frac(1,4)]]", "[[frac(1,3)]]", "[[2]]", "[[3]]", "[[4]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="합성함수 적용 표기 (f∘g)(0), (f∘g)′(0) / " + PRIME_NOTE,
    note="f(1)=2, f′(1)=1 → R(x)=x+1 → R(3)=4 → ⑤. 빠른정답 17과 불일치.")

add(id="af1a0cdf", qtype="short",
    question="두 함수 [[f(x) = k pow(x,3) - 3x]], [[g(x) = pow(e, -x) + 2]]가 있다.\n함수 [[h(x)]] = ([[comp(f, g)]])([[x]])에 대하여 [[prime(h)(0) = 30]]일 때,\n상수 [[-50k]]의 값을 구하시오.",
    choices=None, derived_answer="50", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="합성함수 적용 표기 (f∘g)(x) / " + PRIME_NOTE,
    note="출처 [2017년 7월 고3 이과 25번 변형]. h′(0)=f′(3)g′(0)=-(27k-3)=30 → k=-1 → 50.")

add(id="f494e030", qtype="short",
    question="양의 실수 전체의 집합에서 미분가능한 함수 [[f(x)]]에 대하여 함수 [[g(x)]]를\n[[g(x) = f(x) ln(pow(x,4))]]\n이라 하자. 곡선 [[y = f(x)]] 위의 점 [[point(e, -e)]]에서의 접선과 곡선 [[y = g(x)]] 위의 점 [[point(e, -4e)]]에서의 접선이 서로 수직일 때, [[100 prime(f)(e)]]의 값을 구하시오.",
    choices=None, derived_answer="50", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PRIME_NOTE,
    note="출처 [2014년 6월 고3 이과 26번/4점]. g′(e)=4f′(e)-4, f′(e)(4f′(e)-4)=-1 → (2f′(e)-1)²=0 → f′(e)=1/2 → 50.")

add(id="5f989a4c", qtype="short",
    question="다음 그림과 같이 기울기가 양수인 직선 [[y = (x - 2) tan(theta)]] 위의 두 점 A, B에 대하여 삼각형 OAB가 [[seg(OA) = seg(OB) = 4]]인 이등변삼각형일 때, 삼각형 OAB의 넓이를 [[S(theta)]]라 하자. [[lim(theta, 0, prime(S)(theta), +)]]의 값을 구하시오. (단, O는 원점이다.)",
    choices=None, derived_answer="8",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O, 직선 y=(x-2)tanθ 위의 두 점 A(제3사분면)·B(제1사분면), 삼각형 OAB 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 직선+삼각형 도형 / " + PRIME_NOTE,
    note="O에서 직선까지 거리 2sinθ, S=4sinθ√(4-sin²θ) → S′(0⁺)=8. 빠른정답 4와 불일치(옆 문항 p65의 답).")

add(id="8a792e27", qtype="short",
    question="다음 그림과 같이 기울기가 양수인 직선 [[y = (x - 1) tan(theta)]] 위의 두 점 A, B에 대하여 삼각형 OAB가 [[seg(OA) = seg(OB) = 4]]인 이등변삼각형일 때, 삼각형 OAB의 넓이를 [[S(theta)]]라 하자. [[lim(theta, 0, prime(S)(theta), +)]]의 값을 구하시오. (단, O는 원점이다.)",
    choices=None, derived_answer="4",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O, 직선 y=(x-1)tanθ 위의 두 점 A(제3사분면)·B(제1사분면), 삼각형 OAB 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 직선+삼각형 도형 / " + PRIME_NOTE,
    note="O에서 직선까지 거리 sinθ, S=sinθ√(16-sin²θ) → S′(0⁺)=4.")

add(id="00bd2217", qtype="choice",
    question="[[dydx(frac(pow(x,x), sin(x)), x) = frac(pow(x,x), sin(x))(f(x) - cot(x))]]를 만족시키는 함수 [[f(x)]]는? (단, [[x > 0]])",
    choices=["[[ln(x)]]", "[[ln(x) + 1]]", "[[ln(x) + x]]", "[[2 ln(x)]]", "[[2 ln(x) + 1]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="원문 d/dx(x^x/sin x)를 dydx(식, x)로 표기. (x^x)′=x^x(ln x+1) → f(x)=ln x+1 → ②.")

add(id="520f5756", qtype="choice",
    question="함수 [[f(x) = 9 pow(x, sqrt(3))]] ([[x > 0]])에 대하여 [[prime(f)(3) = pow(3, k)]]일 때, [[k = a + b sqrt(3)]]이다. 유리수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?",
    choices=["[[frac(3,2)]]", "[[2]]", "[[frac(5,2)]]", "[[3]]", "[[frac(7,2)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PRIME_NOTE,
    note="f′(3)=9√3·3^{√3-1}=3^{3/2+√3} → a=3/2, b=1 → 5/2 → ③.")

# ───────── 매개변수로 나타낸 함수의 미분법 ─────────
add(id="5f42f13f", qtype="short",
    question="매개변수로 나타낸 함수 [[x = ln(4t - 3)]],\n[[y = ln(5 pow(t,2) + t)]]에 대하여 [[lim(t, inf, dydx(y,x))]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=(10t+1)(4t-3)/(4(5t²+t)) → 40/20=2.")

add(id="4231315c", qtype="choice",
    question="매개변수로 나타낸 함수 [[x = -2 pow(t,4)]],\n[[y = pow(t,4) + 3 pow(t,3) - pow(t,2)]]에 대하여 [[t = -1]]일 때, [[dydx(y,x)]]의 값은?",
    choices=["[[-frac(1,8)]]", "[[frac(1,8)]]", "[[frac(3,8)]]", "[[frac(5,8)]]", "[[frac(7,8)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="dx/dt=-8t³=8, dy/dt=4t³+9t²-2t=7 → 7/8 → ⑤.")

add(id="2cdeae70", qtype="short",
    question="매개변수 [[t]] ([[t > 0]])로 나타내어진\n함수 [[x = ln(2t)]], [[y = ln(2 pow(t,2) + 3)]]에 대하여\n[[lim(t, inf, dydx(y,x))]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2018년 10월 고3 이과 25번 변형]. dy/dx=4t²/(2t²+3) → 2.")

add(id="fcef851d", qtype="choice",
    question="매개변수 [[t]] ([[t > 0]])으로 나타내어진 함수\n[[x = pow(t,2) + ln(t)]], [[y = pow(t,3) + 6t]]\n에서 [[t = 1]]일 때, [[dydx(y,x)]]의 값은?",
    choices=["[[1]]", "[[frac(3,2)]]", "[[2]]", "[[frac(5,2)]]", "[[3]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 4월 고3 이과 7번/3점]. dx/dt=3, dy/dt=9 → 3 → ⑤.")

add(id="3d3b1bbc", qtype="choice",
    question="매개변수 [[t]] ([[t > 0]])으로 나타내어진\n함수 [[x = 4t - frac(1,t)]], [[y = 2t pow(e, t - 1)]]에서 [[t = 1]]일 때, [[dydx(y,x)]]의 값은?",
    choices=["[[frac(2,5)]]", "[[frac(3,5)]]", "[[frac(4,5)]]", "[[1]]", "[[frac(6,5)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2024년 7월 고3 미적분 24번 변형]. dx/dt=5, dy/dt=4 → 4/5 → ③.")

add(id="771c0746", qtype="choice",
    question="매개변수 [[t]]로 나타낸 함수 [[x = sqrt(t) + frac(1,t)]], [[y = pow(t,2) + frac(4,t)]]에\n대하여 [[lim(t, 0, dydx(y,x), +)]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="dy/dx=(2t³-4)/(t^{3/2}/2-1) → 4 → ④.")

add(id="9d3adb43", qtype="short",
    question="매개변수 [[t]] ([[t > 0]])으로 나타낸\n함수 [[x = pow(t,2) + 4]], [[y = frac(1,3) pow(t,3) + 6t - 5]]에 대하여\n[[t = 2]]일 때의 [[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(5,2)", figure=None, difficulty_est=2, confidence=0.9,
    note="dx/dt=4, dy/dt=10 → 5/2.")

add(id="ec4bfe8d", qtype="choice",
    question="매개변수 [[t]]로 나타낸 함수 [[x = frac(4t, 2 + pow(t,2))]], [[y = frac(2 - pow(t,2), 2 + pow(t,2))]]에\n대하여 [[t = 3]]일 때의 [[dydx(y,x)]]의 값이 [[frac(q,p)]]이다. 이때 [[p + q]]의 값은? (단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=["[[7]]", "[[10]]", "[[13]]", "[[16]]", "[[19]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="dy/dx=-8t/(8-4t²)=2t/(t²-2) → 6/7 → 13 → ③.")

add(id="0fc60b03", qtype="choice",
    question="매개변수로 나타낸 함수 [[x = t - sin(2t)]], [[y = cos(4t)]]에\n대하여 [[lim(t, frac(pi,8), dydx(y,x))]]의 값은?",
    choices=["[[4(sqrt(2) - 1)]]", "[[2]]", "[[4]]", "[[4 sqrt(2)]]", "[[4(sqrt(2) + 1)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="dx/dt=1-2cos2t=1-√2, dy/dt=-4sin4t=-4 → 4/(√2-1)=4(√2+1) → ⑤.")

add(id="1ac9e516", qtype="choice",
    question="매개변수로 나타낸 함수 [[x = frac(3t, 1 + t)]], [[y = frac(pow(t,2), 1 + t)]]에\n대하여 [[t = 1]]일 때, [[dydx(y,x)]]의 값은?",
    choices=["[[-frac(3,2)]]", "[[-frac(1,2)]]", "[[frac(1,2)]]", "[[1]]", "[[frac(3,2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="dx/dt=3/(1+t)²=3/4, dy/dt=(t²+2t)/(1+t)²=3/4 → 1 → ④.")

add(id="1c10d32b", qtype="choice",
    question="매개변수 [[t]] ([[t > 0]])으로 나타낸\n함수 [[x = frac(1,2) ln(t) + t]], [[y = -frac(4,3) pow(t,3) + t]]에 대하여\n[[dydx(y,x)]]가 [[t = a]]에서 최댓값을 가질 때, [[a]]의 값은?",
    choices=["[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 9월 고3 이과 7번 변형]. dy/dx=2t(1-2t)=2t-4t² → 최대 t=1/4 → ③.")

add(id="36d6006d", qtype="choice",
    question="매개변수 [[theta]]에 대하여 [[x = a pow(cos(theta), 4)]], [[y = a pow(sin(theta), 4)]]일 때,\n[[theta = frac(pi,3)]]에서의 [[dydx(y,x)]]의 값은? (단, [[a != 0]])",
    choices=["[[-3]]", "[[-frac(3,2)]]", "[[frac(3,2)]]", "[[1]]", "[[3]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=-tan²θ=-3 → ①.")

add(id="3b8c923c", qtype="choice",
    question="매개변수 [[theta]]에 대하여 [[x = a pow(cos(theta), 2)]], [[y = a pow(sin(theta), 4)]]일 때,\n[[theta = frac(pi,3)]]에서의 [[dydx(y,x)]]의 값은? (단, [[a != 0]])",
    choices=["[[-2]]", "[[-frac(3,2)]]", "[[frac(3,2)]]", "[[1]]", "[[2]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=-2sin²θ=-3/2 → ②.")

add(id="a4c3f8c9", qtype="choice",
    question="매개변수 [[t]] ([[t > 0]])으로 나타내어진\n곡선 [[x = 2 pow(t,2) - 2]], [[y = 2 sqrt(t)]]에서 [[t = frac(1,4)]]일 때,\n[[dydx(y,x)]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2020년 10월 고3 이과 6번 변형]. dx/dt=4t=1, dy/dt=1/√t=2 → 2 → ②.")

add(id="14ee6ca4", qtype="choice",
    question="함수 [[f(x) = pow(x,3) + x + 1]]의 역함수를 [[g(x)]]라 하자.\n매개변수 [[t]]로 나타내어진 곡선\n[[x = g(t) + t]], [[y = g(t) - t]]에서 [[t = 3]]일 때, [[dydx(y,x)]]의\n값은?",
    choices=["[[-frac(1,5)]]", "[[-frac(3,10)]]", "[[-frac(2,5)]]", "[[-frac(1,2)]]", "[[-frac(3,5)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2024년 5월 고3 미적분 27번/3점]. g(3)=1, g′(3)=1/4 → (1/4-1)/(1/4+1)=-3/5 → ⑤.")

add(id="8bd71488", qtype="short",
    question="매개변수 [[t]] ([[t > 0]])로 나타내어진\n함수 [[x = pow(t,2) + ln(t)]], [[y = pow(t,2) + 7t]]에서 [[t = 1]]일 때,\n[[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="dx/dt=3, dy/dt=9 → 3.")

add(id="236f7483", qtype="short",
    question="매개변수 [[t]]([[t > 0]])로 나타내어진 함수\n[[x = t + 2 sqrt(t)]], [[y = 4 pow(t,3)]]\n에 대하여 [[t = 1]]일 때, [[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2017년 4월 고3 이과 24번/3점]. dx/dt=2, dy/dt=12 → 6.")

add(id="bdc15359", qtype="short",
    question="매개변수 [[t]]로 나타내어진\n곡선 [[x = 4 pow(e,t) + 3 pow(e,-t)]], [[y = 6t + 3]]에서 [[t = ln(3)]]일 때,\n[[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(6,11)", figure=None, difficulty_est=2, confidence=0.9,
    note="dx/dt=4e^t-3e^{-t}=12-1=11, dy/dt=6 → 6/11.")

add(id="7a17494f", qtype="short",
    question="매개변수 [[t]] ([[t > 0]])으로 나타낸\n함수 [[x = 4 pow(t,2) + 4t + 1]], [[y = frac(1,2) pow(t,2) + 3t + 2]]에 대하여\n[[t = 1]]일 때의 [[dydx(y,x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(1,3)", figure=None, difficulty_est=2, confidence=0.9,
    note="dx/dt=12, dy/dt=4 → 1/3.")

add(id="7c777b22", qtype="choice",
    question="매개변수 [[t]] ([[t > 0]])으로 나타내어진\n함수 [[x = ln(t) + t]], [[y = -pow(t,3) + 3t]]에 대하여\n[[dydx(y,x)]]가 [[t = a]]에서 최댓값을 가질 때, [[a]]의 값은?",
    choices=["[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 9월 고3 이과 7번/3점]. dy/dx=3t(1-t) → 최대 t=1/2 → ⑤.")

add(id="48ff98e9", qtype="choice",
    question="매개변수 [[t]] ([[t > 0]])로 나타낸\n곡선 [[x = t + 4 ln(t)]], [[y = pow(t,3) - 48t]]에 대하여 [[dydx(y,x)]]의\n최솟값은?",
    choices=["[[-8]]", "[[-10]]", "[[-12]]", "[[-14]]", "[[-16]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="dy/dx=3t(t-4)=3t²-12t → 최소 t=2에서 -12 → ③.")

add(id="34354f14", qtype="choice",
    question="매개변수 [[t]] ([[t > 0]])으로 나타내어진 함수\n[[x = t + sqrt(t)]], [[y = pow(t,3) + frac(1,t)]]\n에서 [[t = 1]]일 때, [[dydx(y,x)]]의 값은?",
    choices=["[[frac(2,3)]]", "[[1]]", "[[frac(4,3)]]", "[[frac(5,3)]]", "[[2]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2017년 7월 고3 이과 9번/3점]. dx/dt=3/2, dy/dt=2 → 4/3 → ③.")

add(id="30232327", qtype="short",
    question="매개변수 [[t]] ([[t > 0]])으로 나타낸\n함수 [[x = 6 ln(t) + t]], [[y = -frac(1,3) pow(t,3) + 36t]]에 대하여 [[dydx(y,x)]]가\n[[t = a]]에서 최댓값을 가질 때, [[a]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="dy/dx=t(6-t)=6t-t² → 최대 t=3.")

add(id="4bc6ba46", qtype="short",
    question="매개변수 [[t]] ([[t > 0]])으로 나타낸\n함수 [[x = 4 ln(t) + t]], [[y = -frac(1,3) pow(t,3) + 16t]]에 대하여 [[dydx(y,x)]]가\n[[t = a]]에서 최댓값을 가질 때, [[a]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.9,
    note="dy/dx=t(4-t)=4t-t² → 최대 t=2.")

add(id="8837de51", qtype="choice",
    question="매개변수 [[t]] ([[t > 0]])으로 나타내어진\n곡선 [[x = ln(3 pow(t,2) + 1)]], [[y = sin(pi pow(t,2))]]에서 [[t = frac(1,2)]]일 때,\n[[dydx(y,x)]]의 값은?",
    choices=["[[frac(5 sqrt(2), 24) pi]]", "[[frac(sqrt(2), 4) pi]]", "[[frac(7 sqrt(2), 24) pi]]", "[[frac(sqrt(2), 3) pi]]", "[[frac(3 sqrt(2), 8) pi]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2023년 11월 고3 미적분 24번 변형]. dx/dt=12/7, dy/dt=π√2/2 → 7√2π/24 → ③.")

add(id="aea5554b", qtype="short",
    question="매개변수 [[t]]로 나타낸 함수\n[[x = frac(1,3)(pow(3, a t) + pow(3, 2a t))]], [[y = frac(1,3)(pow(3, a t) - pow(3, 2a t))]]\n에 대하여 [[dydx(y,x) = frac(b x + c y, 3x - y)]] ([[3x != y]])일 때, [[pow(b,2) + pow(c,2)]]의\n값을 구하시오. (단, [[a]], [[b]], [[c]]는 상수이다.)",
    choices=None, derived_answer="10", figure=None, difficulty_est=4, confidence=0.8,
    note="u=3^{at}: dy/dx=(1-2u)/(1+2u), 3x-y=2u(1+2u)/3 → bx+cy=(2u-4u²)/3 → b=-1, c=3 → 10. 빠른정답 2와 불일치.")

add(id="b9ab12cf", qtype="choice",
    question="[[x]], [[y]]가 매개변수 [[t]]에 대하여 [[x = t + pow(t,2) + pow(t,3)]] + ⋯ + [[pow(t,n)]],\n[[y = 3t + 2]]로 정의 될 때, [[sum(n, 1, inf, lim(t, 1, dydx(y,x)))]]의 값은?",
    choices=["[[frac(2,3)]]", "[[2]]", "[[3]]", "[[5]]", "[[6]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="lim dy/dx=3/(n(n+1)/2)=6/(n(n+1)) → 급수 합 6 → ⑤.")

add(id="abccb2aa", qtype="short",
    question="매개변수 [[t]]로 나타낸 함수\n[[x = pow(t,2) + pow(t,4) + pow(t,6)]] + ⋯ + [[pow(t, 2n)]],\n[[y = t + pow(t,3) + pow(t,5)]] + ⋯ + [[pow(t, 2n - 1)]]\n에 대하여 [[lim(n, inf, (lim(t, 1, dydx(y,x))))]]의 값을 구하시오.\n(단, [[n]]은 자연수)",
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.85,
    note="t=1: dy/dt=n², dx/dt=n(n+1) → n/(n+1) → 1. 빠른정답 10과 불일치.")

add(id="827ffe1b", qtype="choice",
    question="매개변수 [[t]]로 나타내어진\n곡선 [[x = t + sin(2t)]], [[y = pow(cos(t), 2)]]에서 [[t = frac(pi,4)]]일 때,\n[[dydx(y,x)]]의 값은?",
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2023년 9월 고3 미적분 24번 변형]. dx/dt=1+2cos2t=1, dy/dt=-sin2t=-1 → -1 → ②.")

add(id="89704b36", qtype="choice",
    question="매개변수 [[t]]로 나타내어진\n곡선 [[x = 2t + 2 sin(t)]], [[y = 6 cos(t) - 3 pow(sin(t), 2)]]에서\n[[t = frac(pi,6)]]일 때, [[dydx(y,x)]]의 값은?",
    choices=["[[-frac(1,2)]]", "[[-1]]", "[[-frac(3,2)]]", "[[-4]]", "[[-frac(5,2)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2025년 7월 고3 미적분 24번 변형]. dx/dt=2+√3, dy/dt=-3-3√3/2=-(3/2)(2+√3) → -3/2 → ③.")
