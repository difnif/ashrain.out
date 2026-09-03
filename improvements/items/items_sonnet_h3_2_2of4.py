# -*- coding: utf-8 -*-
# esc_sonnet_h3-2_2of4 — 이미지 기준 전사 (83 항목 / 80쪽)
# 표기 관행: 도함수 적용 f′(x)는 prime(f)(x)(파서는 곱으로 해석) → needs_review PR.
#            조각적 정의 { … (조건) ; … (조건) }는 텍스트 혼합 → needs_review PW.
#            첨자 점 라벨(Oₙ, Pₙ, C′ 등)은 텍스트 혼합 → needs_review PS.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

PR = "문법 범위 밖: 도함수 적용 표기 f′(x)를 prime(f)(x)로 전사(파서는 곱으로 해석)"
PW = "문법 범위 밖: 조각적(경우 나눔) 정의는 텍스트 혼합 { … (조건) ; … (조건) }"
PS = "문법 범위 밖: 첨자·프라임 점 라벨은 텍스트 혼합"
CH_G = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ───────────── 매개변수로 나타낸 함수의 미분법 ─────────────
# p48
add(id="c9bb61fa", qtype="choice",
    question="매개변수 [[t]]로 나타내어진 곡선\n[[x = pow(e,t) + cos(t)]], [[y = sin(t)]]에서 [[t = 0]]일 때, [[dydx(y,x)]]의 값은?",
    choices=["[[frac(1,2)]]", "[[1]]", "[[frac(3,2)]]", "[[2]]", "[[frac(5,2)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2021년 6월 고3 미적분 24번/3점]. dx/dt=e^t−sin t=1, dy/dt=cos t=1 → 1 → ②.")

# p49
add(id="0e67313f", qtype="choice",
    question="매개변수 [[t]]로 나타내어진\n곡선 [[x = pow(e,t) - 4pow(e,-t)]], [[y = t + 1]]에서 [[t = ln(2)]]일 때,\n[[dydx(y,x)]]의 값은?",
    choices=["[[1]]", "[[frac(1,2)]]", "[[frac(1,3)]]", "[[frac(1,4)]]", "[[frac(1,5)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2021년 9월 고3 미적분 25번/3점]. dx/dt=e^t+4e^{-t}=4, dy/dt=1 → 1/4 → ④.")

# p51
add(id="9dd19ec9", qtype="short",
    question=("[[0 < t < frac(pi,2)]]인 실수 [[t]]에 대하여 점 [[point(t, 0)]]을 P라 하고, "
              "곡선 [[y = tan(x)]] 위의 점 Q를 점 Q에서의 접선의 기울기가 직선 PQ의 기울기와 같도록 잡는다. "
              "원점 O에 대하여 삼각형 OPQ의 외접원이 [[y]]축과 만나는 점 중 원점이 아닌 점을 R이라 하자. "
              "점 Q의 [[x]]좌표를 [[f(t)]], 점 R의 [[y]]좌표를 [[g(t)]]라 하자. [[tan(f(a)) = 3]]을 만족시키는 상수 [[a]]에 대하여 "
              "[[f(a) + 3 prime(g)(a) = frac(q,p)]]일 때, [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="107",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=tan x, x축 위의 점 P, 곡선 위의 점 Q, 원점 O·P·Q를 지나는 외접원, 외접원과 y축의 교점 R"}}],
    difficulty_est=5, confidence=0.8,
    needs_review=PR + " / 도형 표현 불가: 곡선 y=tan x와 삼각형 OPQ의 외접원 좌표평면 도형",
    note="f=s: t=s−sin s cos s, g=s cos²s+tan s; tan s=3 → f′=5/9, g′=101/18−s/3 → f+3g′=101/6 → p+q=107 = 빠른정답 ✓.")

# p52
add(id="e34bc085", qtype="choice",
    question=("양의 실수 [[t]]와 함수 [[f(x)]] = { [[pow(x,2)]] ([[x < 0]]) ; [[log(2, x + 1)]] ([[x >= 0]]) }에 "
              "대하여 직선 [[y = -x + t]]가 함수 [[y = f(x)]]의 그래프와 만나는 두 점의 [[x]]좌표를 각각 "
              "[[alpha]]([[t]]), [[beta]]([[t]]) ([[alpha]]([[t]]) > 0, [[beta]]([[t]]) < 0)이라 하자.\n"
              "매개변수 [[t]] ([[t > 0]])으로 나타낸 곡선 [[x]] = [[alpha]]([[t]]), [[y]] = [[beta]]([[t]])에 대하여 [[x = 1]]에 대응하는 점에서의 접선의 기울기는?"),
    choices=["[[-frac(2 ln(2) + 1, 6 ln(2))]]", "[[-frac(3 ln(2) + 1, 6 ln(2))]]", "[[-frac(4 ln(2) + 1, 6 ln(2))]]",
             "[[-frac(6 ln(2) + 1, 12 ln(2))]]", "[[-frac(8 ln(2) + 1, 12 ln(2))]]"],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PW + " / 문법 범위 밖: 그리스 문자 함수 α(t), β(t) 적용 표기",
    note="α=1 → t=2, α′=2ln2/(1+2ln2); β=−2, β′=−1/3 → dy/dx=−(2ln2+1)/(6ln2) → ①.")

# p56
add(id="d491e948", qtype="short",
    question=("다음 그림과 같이 좌표평면 위의 두 점 [[A(2, 0)]], [[B(3, 0)]]을 잇는 선분을 한 변으로 하는 정사각형 ABCD가 있다. "
              "이 정사각형을 꼭짓점 B를 중심으로 시곗바늘이 도는 방향으로 [[theta]] ([[0 < theta < frac(pi,2)]])만큼 회전시켰을 때, "
              "점 C가 이동한 점을 C′[[point(x, y)]]라 하자.\n"
              "점 C′의 자취의 방정식을 매개변수 [[theta]]로 나타낼 때, [[sin(theta) = frac(sqrt(5), 5)]]일 때의 [[dydx(y,x)]]의 값을 [[p]]라 하자.\n"
              "이때 [[frac(1, pow(p,2))]]의 값을 구하시오."),
    choices=None, derived_answer="4",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: x축 위 A, B와 정사각형 ABCD, 점 B를 중심으로 θ만큼 시계 방향 회전한 정사각형과 점 C′"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=PS + " / 도형 표현 불가: 좌표평면 위 정사각형과 회전한 정사각형",
    note="x=3+sinθ, y=cosθ → dy/dx=−tanθ=−1/2 → 1/p²=4 = 빠른정답 ✓.")

# p58
add(id="b3db4bb5", qtype="choice",
    question=("매개변수 [[t]]로 나타낸 곡선\n[[x = pow(e,t) + pow(e,2t) + pow(e,3t)]] + ⋯ + [[pow(e, n t)]],\n"
              "[[y = pow(e,t) + pow(e,4t) + pow(e,7t)]] + ⋯ + [[pow(e, (3n - 2)t)]]\n"
              "에 대하여 [[t = 0]]에 대응하는 점에서의 접선의 기울기를 [[g(n)]]이라 할 때, [[g(n) = frac(5,2)]]를 만족시키는 자연수 [[n]]의 값은?"),
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="g(n)=(3n−1)/(n+1)=5/2 → n=7 → ③.")

# p59
add(id="cb7bd778", qtype="short",
    question=("매개변수 [[t]] ([[t > 1]])로 나타낸\n곡선 [[x = 3 ln(t - 1) + 2]], [[y = pow(t,3) - 3pow(t,2) + 3t + 3]] 위의 "
              "점 [[point(a, b)]]에서의 접선이 [[x]]축의 양의 방향과 이루는 각의 크기가 [[frac(pi,4)]]일 때, [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.9,
    note="dy/dx=(t−1)³=1 → t=2 → (2, 5) → 7 = 빠른정답 ✓.")

# p60
add(id="b53fc8ca", qtype="short",
    question=("매개변수 [[t]]로 나타낸\n곡선 [[x = 7t - 2 sin(2t)]], [[y = 3 - n cos(t)]]에 대하여 "
              "[[t = frac(pi,6)]]에 대응하는 점에서의 접선의 기울기를 [[f(n)]]이라 할 때, [[frac(1,3) < f(n) < 1]]을 만족시키는 모든 자연수 [[n]]의 값의 합을 구하시오."),
    choices=None, derived_answer="39", figure=None, difficulty_est=3, confidence=0.9,
    note="f(n)=(n/2)/5=n/10 → n=4~9 → 39 = 빠른정답 ✓.")

# p65
add(id="6be87e66", qtype="short",
    question=("어느 구호 단체에서 지진으로 고립된 마을에 보급품을 공수하려고 한다. 비행기에서 떨어진 지 [[t]]초 후의 보급품의 위치 [[point(x, y)]]를 좌표평면 위에 나타내면\n"
              "[[x = 40t]], [[y = -5pow(t,2) + 320]]\n이 된다고 한다. 보급품이 땅에 떨어지는 순간의 [[dydx(y,x)]]의 값을 구하시오."),
    choices=None, derived_answer="-2",
    figure=[{"fn": "unsupported", "args": {"raw": "삽화: 좌표평면 위 비행기(보급품을 떨어뜨리는 위치)와 보급품이 떨어지는 포물선 경로"}}],
    difficulty_est=2, confidence=0.85,
    note="y=0 → t=8, dy/dx=−10t/40=−2 = 빠른정답 ✓. 그림은 장식 삽화.")

# p66
add(id="bd07a790", qtype="short",
    question=("곡선 [[x = 3 cot(theta)]], [[y = 2 csc(theta)]] 위의 한 점 [[point(a, b)]]에서의 접선의 기울기가 [[frac(1,3)]]일 때, "
              "양수 [[a]], [[b]]에 대하여 [[a b]]의 값을 구하시오. (단, [[0 < theta < 2pi]])"),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.9,
    note="dy/dx=(2/3)cosθ=1/3 → θ=π/3 → a=√3, b=4/√3 → ab=4 = 빠른정답 ✓.")

# p67
add(id="c686f424", qtype="choice",
    question=("매개변수 [[t]]로 나타내어진 곡선 [[x = 2pow(e,t) - 4pow(e,-t)]], [[y = pow(e,t) + 3pow(e,-t)]]을 [[C]]라 하자. "
              "상수 [[k]]에 대하여 [[t]]에 대한 방정식 [[pow(e,t) + 3pow(e,-t) = k]]는 서로 다른 두 실근 [[sub(t,1)]], [[sub(t,2)]]를 갖는다. "
              "곡선 [[C]]에서 [[t = sub(t,1)]]일 때 [[dydx(y,x)]]의 값은 [[-frac(1,3)]]이고, [[t = sub(t,2)]]일 때 [[dydx(y,x)]]의 값은 [[m]]이다. [[k + m]]의 값은?"),
    choices=["[[frac(39,11)]]", "[[frac(43,11)]]", "[[frac(47,11)]]", "[[frac(51,11)]]", "[[frac(55,11)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2026년 5월 고3 미적분 27번 변형]. dy/dx=(u²−3)/(2u²+4)=−1/3 → u=1, k=4; u=3 → m=3/11 → 47/11 → ③.")

# p68
add(id="f8a8d17a", qtype="choice",
    question=("매개변수 [[t]]로 나타내어진 곡선 [[x = 2pow(e,t) - 3pow(e,-t)]], [[y = 2pow(e,t) + 6pow(e,-t)]]을 [[C]]라 하자. "
              "상수 [[k]]에 대하여 [[t]]에 대한 방정식 [[2pow(e,t) + 6pow(e,-t) = k]]는 서로 다른 두 실근 [[sub(t,1)]], [[sub(t,2)]]를 갖는다. "
              "곡선 [[C]]에서 [[t = sub(t,1)]]일 때 [[dydx(y,x)]]의 값은 [[-frac(1,5)]]이고, [[t = sub(t,2)]]일 때 [[dydx(y,x)]]의 값은 [[m]]이다. [[k + m]]의 값은?"),
    choices=["[[frac(75,11)]]", "[[frac(79,11)]]", "[[frac(83,11)]]", "[[frac(87,11)]]", "[[frac(91,11)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2026년 5월 고3 미적분 27번/3점]. dy/dx=(2u²−6)/(2u²+3)=−1/5 → u=3/2, k=7; u=2 → m=2/11 → 79/11 → ②.")

# p70
add(id="c84c28fb", qtype="choice",
    question=("자연수 [[n]]에 대하여 함수 [[y = f(x)]]를 매개변수 [[t]]로 나타내면\n[[x = pow(e,t)]], [[y = (2pow(t,2) + n t + n) pow(e,t)]]\n"
              "이고, [[x >= pow(e, -frac(n,2))]]일 때 함수 [[y = f(x)]]는 [[x = sub(a,n)]]에서 최솟값 [[sub(b,n)]]을 갖는다. "
              "[[frac(sub(b,3), sub(a,3)) + frac(sub(b,4), sub(a,4)) + frac(sub(b,5), sub(a,5)) + frac(sub(b,6), sub(a,6))]]의 값은?"),
    choices=["[[frac(23,2)]]", "[[12]]", "[[frac(25,2)]]", "[[13]]", "[[frac(27,2)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2013년 9월 고3 이과 21번/4점]. dy/dx=(2t+n)(t+2); n=3: 3, n≥4: 8−n → 3+4+3+2=12 → ②.")

# p74
add(id="e0ca9f7d", qtype="choice",
    question="매개변수 [[t]]로 나타낸 곡선 [[x = 2pow(t,2) - 4]], [[y = 6t - 5]] 위의 점 [[point(a, b)]]에서의 접선의 기울기가 [[frac(3,2)]]일 때, [[a + b]]의 값은?",
    choices=["[[-3]]", "[[-1]]", "[[1]]", "[[3]]", "[[6]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=3/(2t)=3/2 → t=1 → (−2, 1) → −1 → ②.")

# p75
add(id="6a06cddf", qtype="choice",
    question="매개변수 [[t]]로 나타낸 곡선 [[x = 4pow(t,2) - 2]], [[y = 24t - 7]] 위의\n점 [[point(a, b)]]에서의 접선의 기울기가 3일 때, [[a + b]]의 값은?",
    choices=["[[17]]", "[[18]]", "[[19]]", "[[20]]", "[[21]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=3/t=3 → t=1 → (2, 17) → 19 → ③.")

# p76
add(id="1d4da47d", qtype="choice",
    question="매개변수로 나타낸 곡선\n[[x = 6 sqrt(t) + 5a t]], [[y = 3a pow(t,2) - frac(1,t)]]\n에 대하여 [[t = 1]]에 대응하는 곡선 위의 점에서의 접선의 기울기가 1일 때, 상수 [[a]]의 값은?",
    choices=["[[-2]]", "[[-1]]", "[[1]]", "[[2]]", "[[4]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(6a+1)/(3+5a)=1 → a=2 → ④.")

# p77
add(id="df494a79", qtype="choice",
    question="매개변수 [[t]]로 나타낸 곡선 [[x = 3pow(t,2) - 4]], [[y = 12t - 5]] 위의 점 [[point(a, b)]]에서의 접선의 기울기가 1일 때, [[a + b]]의 값은?",
    choices=["[[23]]", "[[25]]", "[[27]]", "[[29]]", "[[31]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=2/t=1 → t=2 → (8, 19) → 27 → ③.")

# p78
add(id="e680d860", qtype="choice",
    question="매개변수로 나타낸 곡선\n[[x = 4 sqrt(t) + a t]], [[y = a pow(t,2) - frac(2,t)]]\n에 대하여 [[t = 1]]에 대응하는 곡선 위의 점에서의 접선의 기울기가 4일 때, 상수 [[a]]의 값은?",
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="(2a+2)/(2+a)=4 → a=−3 → ③.")

# p79
add(id="431c7f0e", qtype="short",
    question="매개변수 [[t]]로 나타낸 곡선 [[x = pow(t,3) + pow(a,2)]], [[y = pow(t,2) + 2a t]]에 대하여 [[t = 1]]에 대응하는 곡선 위의 점에서의 접선의 기울기가 4일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="(2+2a)/3=4 → a=5 = 빠른정답 ✓.")

# p82
add(id="9d117d82", qtype="choice",
    question=("매개변수 [[t]] ([[0 < t < frac(pi,2)]])로 나타내어진\n곡선 [[x = cos(t) + t sin(t)]], [[y = sin(t) - t cos(t)]]에 대하여 "
              "[[t = k]]일 때, 곡선 위의 점을 [[P(a, b)]]라 하자. 곡선 위의 점 P에서의 접선과 직선 [[y = frac(1,3) x]]가 이루는 예각의 크기를 "
              "[[theta]]라 하면 [[tan(theta) = frac(1,3)]]이다. [[4a + 3b + tan(k)]]의 값은?\n(단, [[k]]는 [[0 < k < frac(pi,2)]]인 상수이다.)"),
    choices=["[[frac(17,4)]]", "[[frac(19,4)]]", "[[frac(21,4)]]", "[[frac(23,4)]]", "[[frac(25,4)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2026년 7월 고3 미적분 27번 변형]. dy/dx=tan t; |(tan k−1/3)/(1+tan k/3)|=1/3 → tan k=3/4; 4a+3b=5 → 23/4 → ④.")

# p83
add(id="f068baed", qtype="choice",
    question="매개변수 [[t]]로 나타낸 곡선 [[x = 3pow(t,2) - 1]], [[y = 2pow(t,3) + a t]]에 대하여 [[t = 1]]에 대응하는 점에서의 접선의 기울기가 [[frac(3,2)]]일 때, 상수 [[a]]의 값은?",
    choices=["[[-3]]", "[[-1]]", "[[1]]", "[[3]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(6+a)/6=3/2 → a=3 → ④.")

# p85
add(id="d1ff103a", qtype="short",
    question="매개변수로 나타낸 곡선 [[x = 1 + 3 sin(theta)]], [[y = 2 - cos(theta)]]에 대하여 [[theta = alpha]]에 대응하는 곡선 위의 점에서의 접선이 직선 [[y = -6x + 1]]과 수직일 때, [[pow(sec(alpha), 2)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(5,4)", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=tanα/3=1/6 → tanα=1/2 → sec²α=5/4. 빠른정답 frac(5,1)과 불일치.")

# p86
add(id="5f948b07", qtype="short",
    question="매개변수로 나타낸 곡선 [[x = 3 - 2 sin(theta)]], [[y = 1 + cos(theta)]]에 대하여 [[theta = alpha]]에 대응하는 곡선 위의 점에서의 접선이 직선 [[y = 4x + 1]]과 수직일 때, [[pow(sec(alpha), 2)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(5,4)", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=tanα/2=−1/4 → tanα=−1/2 → sec²α=5/4. 빠른정답 5와 불일치.")

# p87
add(id="17a2d567", qtype="short",
    question="매개변수로 나타낸 곡선 [[x = 2 - sin(theta)]], [[y = 1 + 3 cos(theta)]]에 대하여 [[theta = alpha]]에 대응하는 곡선 위의 점에서의 접선이 직선 [[y = -frac(1,3) x + 2]]와 수직일 때, [[pow(sec(alpha), 2)]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="dy/dx=3tanα=3 → tanα=1 → sec²α=2. 빠른정답 frac(5,1)과 불일치.")

# p94
add(id="ddefe891", qtype="short",
    question=("곡선 [[x = 4 cot(theta)]], [[y = 3 csc(theta)]] 위의 한 점 [[point(a, b)]]에서의 접선의 기울기가 [[frac(3,8)]]일 때, "
              "양수 [[a]], [[b]]에 대하여 [[a b]]의 값을 구하시오. (단, [[0 < theta < 2pi]])"),
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.9,
    note="dy/dx=(3/4)cosθ=3/8 → θ=π/3 → a=4/√3, b=6/√3 → ab=8.")

# p95
add(id="e3633a32", qtype="choice",
    question=("두 곡선 [[x = a cos(alpha)]], [[y = b sin(alpha)]]와 [[x = sqrt(11) tan(beta)]], [[y = sqrt(11) sec(beta)]]는\n"
              "점 [[P(1, 2 sqrt(3))]]에서 만나고, 점 P에서의 두 곡선의 접선의 기울기의 곱은 [[-frac(1,3)]]이다. 이때 양수 [[a]], [[b]]에 대하여 "
              "[[pow(a,2) + pow(b,2)]]의 값은? (단, [[0 <= alpha < 2pi]], [[0 <= beta < 2pi]])"),
    choices=["[[5]]", "[[10]]", "[[15]]", "[[20]]", "[[25]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="쌍곡선 기울기 sinβ=1/(2√3) → 타원 기울기 −2√3/3 → b²=4a², 1/a²+12/b²=1 → a²=4, b²=16 → 20 → ④.")

# p96
add(id="91326864", qtype="choice",
    question="매개변수로 나타낸 곡선 [[x = 8 pow(sin(2theta), 3)]], [[y = 2 cos(theta)]]\n([[0 <= theta <= 2pi]])에 대하여 곡선 위의 점 [[point(3 sqrt(3), 1)]]에서의 접선의 기울기는?",
    choices=["[[frac(sqrt(3), 18)]]", "[[frac(sqrt(3), 15)]]", "[[frac(sqrt(3), 12)]]", "[[frac(sqrt(3), 9)]]", "[[frac(sqrt(3), 6)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="θ=π/3: dx/dθ=48sin²2θcos2θ=−18, dy/dθ=−√3 → √3/18 → ①.")

# p99 (같은 이미지에 별개 문항 2개, id 2개 — draft_a 대응대로 분리)
add(id="b8b2c3d0", qtype="short",
    question="매개변수 [[t]]로 나타낸 곡선\n[[x = 4pow(t,3) + 2a pow(t,2)]], [[y = 3pow(t,2) - 5]]\n에 대하여 [[t = 2]]에 대응하는 점에서의 접선의 기울기가\n[[frac(1,6)]]일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="같은 이미지 위쪽 문항. 12/(48+8a)=1/6 → a=3.")
add(id="013484e6", qtype="short",
    question="매개변수 [[t]]로 나타낸 곡선\n[[x = 3pow(t,3) + 3a pow(t,2)]], [[y = -pow(t,2) + 2]]\n에 대하여 [[t = -1]]에 대응하는 점에서의 접선의 기울기가\n[[frac(2,3)]]일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.9,
    note="같은 이미지 아래쪽 문항. 2/(9−6a)=2/3 → a=1.")

# ───────────── 속도와 거리 ─────────────
# p33
add(id="c684c4a0", qtype="choice",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]]에서의\n위치 [[point(x, y)]]가 [[x = pow(cos(t), 3)]], [[y = pow(sin(t), 3)]]일 때, [[t = 0]]에서\n[[t = frac(pi,3)]]까지 점 P가 움직인 거리는?",
    choices=["[[frac(3,2)]]", "[[frac(11,8)]]", "[[frac(5,4)]]", "[[frac(9,8)]]", "[[1]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="속력 (3/2)sin2t → ∫₀^{π/3} = (3/4)(1−cos(2π/3)) = 9/8 → ④. 빠른정답 10과 불일치.")

# p34
add(id="cbffd2a0", qtype="choice",
    question="좌표평면 위를 움직이는 점 [[P]]의 시각 [[t]]에서의 위치\n[[point(x, y)]]가 [[x = 2pow(t,2) + 3]], [[y = pow(t,3) - 1]]일 때, [[t = 0]]에서\n[[t = 1]]까지 점 [[P]]가 움직인 거리는?",
    choices=["[[frac(61,27)]]", "[[frac(7,3)]]", "[[frac(65,27)]]", "[[frac(67,27)]]", "[[frac(23,9)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="속력 t√(16+9t²) → (1/27)(125−64)=61/27 → ① = 빠른정답 ✓.")

# p53
add(id="ec0d1d6f", qtype="choice",
    question="곡선 [[x = 3 pow(sin(t), 2)]], [[y = 3 pow(cos(t), 2)]] ([[0 <= t <= frac(pi,2)]])의 길이는?",
    choices=["[[sqrt(2)]]", "[[2 sqrt(2)]]", "[[3 sqrt(2)]]", "[[4 sqrt(2)]]", "[[5 sqrt(2)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="속력 3√2 sin2t → ∫₀^{π/2} = 3√2 → ③ = 빠른정답 ✓.")

# p54
add(id="8f4de147", qtype="short",
    question="곡선 [[x = 2 pow(cos(3t), 3)]], [[y = 2 pow(sin(3t), 3)]] ([[0 <= t <= frac(pi,6)]])의\n길이를 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="속력 9 sin6t → ∫₀^{π/6} = 3 = 빠른정답 ✓.")

# p56
add(id="40de3c09", qtype="short",
    question="매개변수 [[t]]로 나타낸 곡선\n[[x = 3pow(t,2)]], [[y = -4pow(t,2) - 2]] ([[0 <= t <= 4]])\n의 길이를 구하시오.",
    choices=None, derived_answer="80", figure=None, difficulty_est=2, confidence=0.9,
    note="속력 10t → ∫₀⁴ = 80. 빠른정답 3과 불일치.")

# p61
add(id="3ae36ccd", qtype="choice",
    question="매개변수 [[t]]로 나타낸\n곡선 [[x = pow(e,t) sin(t)]], [[y = pow(e,t) cos(t)]] ([[0 <= t <= 2pi]])의 길이는?",
    choices=["[[(pow(e, 2pi) - 1)]]", "[[sqrt(2) (pow(e, 2pi) - 1)]]", "[[2 (pow(e, 2pi) - 1)]]", "[[2 (pow(e, 2pi) + 1)]]", "[[2 sqrt(2) (pow(e, 2pi) - 1)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="속력 √2 e^t → √2(e^{2π}−1) → ② = 빠른정답 ✓.")

# p63
add(id="af271628", qtype="short",
    question="곡선 [[x = 4 pow(cos(2t), 3)]], [[y = 4 pow(sin(2t), 3)]] ([[0 <= t <= frac(pi,4)]])의\n길이를 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.9,
    note="속력 12 sin4t → ∫₀^{π/4} = 6 = 빠른정답 ✓.")

# p71
add(id="4b4bedc1", qtype="choice",
    question="매개변수 [[t]]로 나타낸\n곡선 [[x = ln(pow(t,4))]], [[y = t + frac(4,t)]] ([[1 <= t <= a]])의 길이가\n3일 때, 상수 [[a]]의 값은?",
    choices=["[[frac(5,4)]]", "[[frac(3,2)]]", "[[frac(7,4)]]", "[[2]]", "[[frac(9,4)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="속력 1+4/t² → a+3−4/a=3 → a=2 → ④ = 빠른정답 ✓.")

# ───────────── 부피 ─────────────
_VOL_FIG = [{"fn": "unsupported", "args": {"raw": "입체도형 그림: x축 위 −ln a에서 e−1(또는 e³−e²)까지, 곡선 y=f(x) 위의 점 P와 수선의 발 H, 선분 PH를 한 변으로 하는 정사각형 단면들(x축에 수직)"}}]
_VOL_RV = PW + " / 도형 표현 불가: 정사각형 단면 입체도형 그림"
# p36
add(id="7e47303c", qtype="choice",
    question=("다음 그림과 같이 함수\n[[f(x)]] = { [[2pow(e,-x)]] ([[x < 0]]) ; [[sqrt(ln(x + 1) + 4)]] ([[x >= 0]]) }\n"
              "의 그래프 위의 점 [[P(x, f(x))]]에서 [[x]]축에 내린 수선의 발을 H라 하고, 선분 PH를 한 변으로 하는 정사각형을 [[x]]축에 수직인 평면 위에 그린다. "
              "점 P의 [[x]]좌표가 [[x = -ln(3)]]에서 [[x = e - 1]]까지 변할 때, 이 정사각형이 만드는 입체도형의 부피는?"),
    choices=["[[3e + 10]]", "[[3e + 13]]", "[[3e + 16]]", "[[4e + 10]]", "[[4e + 13]]"],
    derived_answer="⑤", figure=_VOL_FIG, difficulty_est=4, confidence=0.85, needs_review=_VOL_RV,
    note="출처 [2016년 3월 고3 이과 20번 변형]. ∫4e^{-2x}=16, ∫(ln(x+1)+4)=1+4(e−1) → 4e+13 → ⑤ = 빠른정답 ✓.")

# p59
add(id="1013c739", qtype="choice",
    question=("그림과 같이 함수\n[[f(x)]] = { [[pow(e,-x)]] ([[x < 0]]) ; [[sqrt(ln(x + 1) + 1)]] ([[x >= 0]]) }\n"
              "의 그래프 위의 점 [[P(x, f(x))]]에서 [[x]]축에 내린 수선의 발을 H라 하고, 선분 PH를 한 변으로 하는 정사각형을 [[x]]축에 수직인 평면 위에 그린다. "
              "점 P의 [[x]]좌표가 [[x = -ln(2)]]에서 [[x = e - 1]]까지 변할 때, 이 정사각형이 만드는 입체도형의 부피는?"),
    choices=["[[e - frac(3,2)]]", "[[e + frac(2,3)]]", "[[2e - frac(3,2)]]", "[[e + frac(3,2)]]", "[[2e - frac(2,3)]]"],
    derived_answer="④", figure=_VOL_FIG, difficulty_est=4, confidence=0.85, needs_review=_VOL_RV,
    note="출처 [2016년 3월 고3 이과 20번/4점]. ∫e^{-2x}=3/2, ∫(ln(x+1)+1)=e → e+3/2 → ④. 빠른정답 1과 불일치.")

# p63
add(id="81991cda", qtype="choice",
    question=("다음 그림과 같이\n함수 [[f(x)]] = { [[pow(e, -frac(x,2))]] ([[x < 0]]) ; [[sqrt(ln(x + pow(e,2)) - 1)]] ([[x >= 0]]) }의 그래프\n"
              "위의 점 [[P(x, f(x))]]에서 [[x]]축에 내린 수선의 발을 H라 하고, 선분 PH를 한 변으로 하는 정사각형을 [[x]]축에 수직인 평면 위에 그린다. "
              "점 P의 [[x]]좌표가 [[x = -ln(4)]]에서 [[x = pow(e,3) - pow(e,2)]]까지 변할 때, 이 정사각형이 만드는 입체도형의 부피는?"),
    choices=["[[pow(e,3) - 3]]", "[[pow(e,3) - 1]]", "[[pow(e,3) + 3]]", "[[2pow(e,3) + 1]]", "[[2pow(e,3) + 3]]"],
    derived_answer="③", figure=_VOL_FIG, difficulty_est=4, confidence=0.85, needs_review=_VOL_RV,
    note="∫e^{-x}(−ln4~0)=3, ∫(ln(x+e²)−1)(0~e³−e²)=e³ → e³+3 → ③ = 빠른정답 ✓.")

# ───────────── 속도와 가속도 ─────────────
# p22
add(id="d16ac071", qtype="choice",
    question="지면에 수직 방향으로 운동하는 물체의 시각 [[t]]에서의\n높이를 [[h]] m라 하면 [[h = 30 + 15pow(e,t) - pow(t,2) pow(e,t)]]이다. 이 물체가\n최고 높이에 도달할 때까지 움직인 거리는 몇 m인가?",
    choices=["[[2pow(e,3) - 5]]", "[[2(pow(e,3) - 5)]]", "[[3(pow(e,3) - 5)]]", "[[3(2pow(e,3) - 5)]]", "[[3(2pow(e,3) + 5)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="h′=−e^t(t+5)(t−3) → t=3 최고; h(3)−h(0)=6e³−15=3(2e³−5) → ④. 빠른정답 5와 불일치.")

# p39
add(id="0e4e13b6", qtype="choice",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]]에서의\n위치 [[point(x, y)]]가 [[x = 3t - cos(t)]], [[y = 2 + sin(t)]]이다.\n시각 [[t = frac(pi,6)]]에서의 점 P의 속력은?",
    choices=["[[3]]", "[[sqrt(10)]]", "[[sqrt(11)]]", "[[2 sqrt(3)]]", "[[sqrt(13)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 10월 고3 이과 7번 변형]. (7/2, √3/2) → √13 → ⑤ = 빠른정답 ✓.")

# p43
add(id="711e32fe", qtype="choice",
    question=("좌표평면 위를 움직이는 점 P의 시각\n[[t]] ([[0 <= t <= pi]])에서의 위치 [[point(x, y)]]가\n[[x = a t + sin(t)]], [[y = 1 + 2 cos(t)]]이다. "
              "점 P의 속력의\n최댓값이 8이 되게 하는 모든 상수 [[a]]의 값의 곱은?"),
    choices=["[[-49]]", "[[-42]]", "[[-35]]", "[[-28]]", "[[-21]]"],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.85,
    note="속력²=−3c²+2ac+a²+4 (c=cos t); |a|≤3이면 최대 (4/3)a²+4=64 불가, a>3: (a+1)²=64 → a=7, a<−3: a=−7 → −49 → ①. 빠른정답 4와 불일치.")

# p46
add(id="d1066f56", qtype="short",
    question=("좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t > 0]])에서의\n위치 [[P(x, y)]]가\n[[x = t + ln(t)]], [[y = frac(1,2) pow(t,2) + t]]\n"
              "이다. [[dydx(x,t) = dydx(y,t)]]일 때, 점 P의 속도를 [[vec(v)]]라 하자. [[pow(abs(vec(v)), 2)]]의\n값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 7월 고3 이과 25번/3점]. 1+1/t=t+1 → t=1, v=(2, 2) → 8. 빠른정답 1과 불일치.")

# p47
add(id="db2a38e5", qtype="short",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]]에서의\n좌표 [[point(x, y)]]가 [[x = sin(3t)]], [[y = cos(3t)]]로 나타내어질 때,\n점 P의 [[t = frac(pi,3)]]에서의 속도의 크기를 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="v=(3cos3t, −3sin3t) → 크기 3 = 빠른정답 ✓.")

# p48
add(id="40ca7c14", qtype="short",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t > 0]])에서의\n위치 [[point(x, y)]]가 [[x = 3t - frac(1,t)]], [[y = 5t + frac(2,t)]]일 때,\n[[t = 1]]에서의 점 P의 속력을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="v=(4, 3) → 5. 빠른정답 4와 불일치.")

# p50
add(id="89b15046", qtype="short",
    question=("좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t > 0]])에서의\n위치 [[point(x, y)]]가\n[[x = frac(1,2) pow(e, 2(t - 1)) - a t]], [[y = b pow(e, t - 1)]]\n"
              "이다. 시각 [[t = 1]]에서의 점 P의 속도가 [[point(-1, 2)]]일 때,\n[[a + b]]의 값을 구하시오. (단, [[a]]와 [[b]]는 상수이다.)"),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 9월 고3 이과 23번/3점]. 1−a=−1, b=2 → 4. 빠른정답 3과 불일치.")

# p53
add(id="770f3a50", qtype="short",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t > 0]])에서의\n위치 [[point(x, y)]]가 [[x = 9t + frac(8,pi) cos(frac(pi t, 2))]], [[y = 8 ln(t) - frac(4,pi) sin(pi t)]]\n이다. 이때 시각 [[t = 1]]에서 점 P의 속력을 구하시오.",
    choices=None, derived_answer="13", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 7월 고3 이과 25번 변형]. v=(9−4, 8+4)=(5, 12) → 13. 빠른정답 4와 불일치.")

# p54
add(id="3941f92b", qtype="choice",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]]에서의\n위치 [[point(x, y)]]가\n[[x = 2t + sin(t)]], [[y = 1 - cos(t)]]\n이다. 시각 [[t = frac(pi,3)]]에서의 점 P의 속력은?",
    choices=["[[sqrt(3)]]", "[[2]]", "[[sqrt(5)]]", "[[sqrt(6)]]", "[[sqrt(7)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 10월 고3 이과 7번/3점]. (5/2, √3/2) → √7 → ⑤. 빠른정답 4와 불일치.")

# p67
add(id="8ee803cf", qtype="choice",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t > 0]])\n에서의 위치 [[point(x, y)]]가\n[[x = t - frac(2,t)]], [[y = 2t + frac(1,t)]]\n이다. 시각 [[t = 1]]에서 점 P의 속력은?",
    choices=["[[2 sqrt(2)]]", "[[3]]", "[[sqrt(10)]]", "[[sqrt(11)]]", "[[2 sqrt(3)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2016년 11월 고3 이과 10번/3점]. v=(3, 1) → √10 → ③ = 빠른정답 ✓.")

# p68
add(id="39938824", qtype="choice",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t > 2]])에서의\n위치 [[point(x, y)]]가 [[x = t ln(t)]], [[y = frac(4t, ln(t))]]이다. 시각 [[t = pow(e,2)]]에서\n점 P의 속력은?",
    choices=["[[sqrt(7)]]", "[[2 sqrt(2)]]", "[[3]]", "[[sqrt(10)]]", "[[sqrt(11)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2021년 10월 고3 미적분 25번/3점]. v=(3, 1) → √10 → ④. 빠른정답 2와 불일치.")

# p74
add(id="994d9523", qtype="choice",
    question=("좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t >= 0]])에서의\n위치 [[point(x, y)]]가\n[[x = k - 2 cos(t)]], [[y = 3 sin(t)]] ([[k]]는 상수)이다. "
              "점 P가\n시각 [[t = 0]]일 때 원점을 출발한 다음, 다시 원점을\n지나는 모든 시각을 작은 수부터 크기순으로 나열한\n것을 [[sub(t,1)]], [[sub(t,2)]], [[sub(t,3)]], ⋯이라 하자. "
              "[[sub(t,1) < t < sub(t,2)]]에서 점 P의\n속력과 가속도의 크기가 서로 같은 시각 [[t]]의 개수는\n[[m]]이다. [[k + m]]의 값은?"),
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="k=2, 원점 재통과 t=2π, 4π; 속력=가속도 크기 ⇔ cos2t=0 → (2π, 4π)에 4개 → k+m=6 → ④. 빠른정답 2와 불일치.")

# p76
add(id="b6072124", qtype="short",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t >= 0]])에서의\n위치 [[point(x, y)]]가 [[x = 3 + cos(3t)]], [[y = frac(2,3) sin(3t)]]이다.\n점 P의 속력이 최대일 때, 점 P의 가속도의 크기를 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2018년 11월 고3 이과 24번 변형]. 속력²=4+5sin²3t 최대 ⇔ cos3t=0 → |a|=6. 빠른정답 1과 불일치.")

# p81
add(id="e6e6f29c", qtype="short",
    question="좌표평면 위를 움직이는 점 [[P(x, y)]]의 시각 [[t]]에서의\n위치가 [[x = a cos(t)]], [[y = a pow(t,2) - 2t + a sin(t)]]이다.\n[[t = pi]]에서의 점 P의 가속도의 크기가 [[5 sqrt(5)]]일 때,\n양수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=3, confidence=0.9,
    note="가속도 (a, 2a) → √5 a=5√5 → a=5 = 빠른정답 ✓.")

# p82
add(id="d694f883", qtype="choice",
    question="좌표평면 위를 움직이는 점 [[P(x, y)]]의 시각 [[t]]에서의\n위치가 [[x = frac(3,2) pow(t,2) + 2]], [[y = 6t - frac(3,2) pow(t,2)]]이다. [[t = 3]]에서\n점 P의 속도를 [[point(m, n)]], 가속도를 [[point(p, q)]]라 할 때,\n[[m + n + p + q]]의 값은?",
    choices=["[[-3]]", "[[0]]", "[[3]]", "[[6]]", "[[9]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="v=(9, −3), a=(3, −3) → 6 → ④. 빠른정답 3과 불일치.")

# p96
add(id="1fe15b48", qtype="choice",
    question="좌표평면 위를 움직이는 점 P에서의 시각 [[t]]에서의\n위치 [[point(x, y)]]가 [[x = pow(e,t) cos(t)]], [[y = pow(e,t) sin(t)]]이다. 점 P의\n속력이 [[sqrt(2) pow(e,2)]]일 때, 가속도의 크기는?",
    choices=["[[e]]", "[[2e]]", "[[4e]]", "[[2pow(e,2)]]", "[[4pow(e,2)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="속력 √2e^t → t=2; 가속도 (−2e^t sin t, 2e^t cos t) → 2e² → ④. 빠른정답 3과 불일치.")

# p99 (이미지에 문항 2개, id 1개 — 위 문항이 draft_a·빠른정답과 대응)
add(id="27c8d446", qtype="short",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]]에서의\n위치 [[point(x, y)]]가\n[[x = cos(t)]], [[y = 2 pow(sin(t), 2)]] ([[0 <= t <= frac(pi,2)]])이다. 점 P의\n위치가 [[point(0, 2)]]일 때, 가속도의 크기를 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.85,
    needs_review="같은 이미지에 문항 2개(위: 전사함 — 빠른정답 4와 일치 / 아래: id 미배정 — 위치 x=2t²−3t, y=kt³+t, t=1에서 가속도 크기 √52일 때 양수 k는? 선지 ①1 ②2 ③3 ④4 ⑤5, 답 ① k=1)",
    note="t=π/2: x″=−cos t=0, y=1−cos2t → y″=4cos2t=−4 → 4 = 빠른정답 ✓.")

# ───────────── 급수 ─────────────
# p12
add(id="e42526e5", qtype="short",
    question="다음 급수의 합을 구하시오.\n[[frac(1, 2 × 5) + frac(1, 5 × 8) + frac(1, 8 × 11)]] + ⋯ + [[frac(1, (3n - 1)(3n + 2))]] + ⋯",
    choices=None, derived_answer="frac(1,6)", figure=None, difficulty_est=2, confidence=0.9,
    note="(1/3)Σ(1/(3n−1)−1/(3n+2)) = (1/3)(1/2) = 1/6 = 빠른정답 ✓.")

# p13
add(id="dc511341", qtype="short",
    question="급수 [[frac(1, 2 × 5) + frac(1, 5 × 8) + frac(1, 8 × 11)]] + ⋯의 합을 구하시오.",
    choices=None, derived_answer="frac(1,6)", figure=None, difficulty_est=2, confidence=0.9,
    note="일반항 1/((3n−1)(3n+2)) → 1/6 = 빠른정답 ✓.")

# p14
add(id="73a00593", qtype="choice",
    question="급수 [[frac(1, 1 × 3) + frac(1, 3 × 5) + frac(1, 5 × 7) + frac(1, 7 × 9)]] + ⋯의 합은?",
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(3,2)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="Σ1/((2n−1)(2n+1)) = 1/2 → ②.")

# p20
add(id="6546a330", qtype="choice",
    question=("공차가 양수인 등차수열 [[set(sub(a,n))]]이 다음 조건을 만족시킨다.\n"
              "(가) 모든 자연수 [[n]]에 대하여\n([[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a, 2n - 1) + sub(a, 2n)]]) / ([[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a, n - 1) + sub(a,n)]])은 일정한 값을 가진다.\n"
              "(나) [[sum(n, 1, inf, frac(2, (2n + 1) sub(a,n))) = frac(1,10)]]\n"
              "[[sub(a,10)]]의 값은?"),
    choices=["[[190]]", "[[192]]", "[[194]]", "[[196]]", "[[198]]"],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.85,
    needs_review="문법 범위 밖: 줄임표가 든 분수(S₂ₙ/Sₙ 꼴)는 (…)/(…) 텍스트 혼합",
    note="출처 [2018년 9월 고2 문과 21번/4점]. S₂ₙ/Sₙ 일정 → a₁=d/2, aₙ=(2n−1)d/2; (나) 2/d=1/10 → d=20 → a₁₀=190 → ①. 빠른정답 12와 불일치.")

# p21
add(id="d1f111a8", qtype="choice",
    question=("수열 [[set(sub(a,n))]]에 대하여\n[[sub(a,n) = frac(1, sqrt(n + 1) + sqrt(n))]] ([[n]] = 1, 2, 3, ⋯)\n일 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[lim(n, inf, sub(a,n)) = 0]]\nㄴ. [[sum(n, 1, 99, sub(a,n)) = 9]]\nㄷ. [[sum(n, 1, inf, sub(a,n))]]은 수렴한다."),
    choices=CH_G, derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2008년 9월 고2 이과 15번]. aₙ=√(n+1)−√n: ㄱ✓, ㄴ √100−1=9 ✓, ㄷ 부분합 √(n+1)−1 발산 ✗ → ②.")

# p24
add(id="a9d90dd7", qtype="choice",
    question="수열 [[set(sub(a,n))]]이\n[[sub(a, n + 1) = sqrt(n + 1) sub(a,n)]] ([[n]] = 1, 2, 3, ⋯)으로 정의될 때,\n[[sum(n, 1, inf, frac((sqrt(n + 2) - sqrt(n + 1)) sub(a,n), sub(a, n + 2)))]]의 값은?",
    choices=["[[frac(sqrt(2), 2)]]", "[[1]]", "[[sqrt(2)]]", "[[2]]", "[[2 sqrt(2)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="a_{n+2}=√(n+2)√(n+1)aₙ → 항 = 1/√(n+1) − 1/√(n+2) → 합 1/√2 → ①.")

# p40
add(id="908e28ee", qtype="choice",
    question="수열 [[set(sub(a,n))]]에 대하여\n[[sub(a,1) sub(a,2) sub(a,3)]] ⋯ [[sub(a,n) = frac(3n, n + 2)]] ([[n]] = 1, 2, 3, ⋯)\n이 성립할 때, 급수 [[sum(n, 1, inf, log(3, sub(a,n)))]]의 합은?",
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="부분합 = log₃(a₁⋯aₙ) = log₃(3n/(n+2)) → 1 → ④.")

# p41 (id 2개)
dup(["2d1ed322", "d6930e8f"], qtype="choice",
    question=("다음 보기 중 수열 [[set(sub(a,n))]]에 대하여\n급수 [[sub(a,1) - sub(a,2) + sub(a,2) - sub(a,3) + sub(a,3) - sub(a,4)]] + ⋯가 수렴하도록\n하는 수열인 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(a,n) = frac(6, n + 1)]]\nㄴ. [[sub(a,n) = sqrt(n + 3) - sqrt(n)]]\nㄷ. [[sub(a,n) = log(2, frac(4n, n + 5))]]"),
    choices=CH_G, derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="괄호 없는 급수 → 부분합 S₂ₙ=a₁−a_{n+1}, S₂ₙ₋₁=a₁ → aₙ→0일 때만 수렴: ㄱ✓ ㄴ✓ ㄷ(→2)✗ → ②.")

# p43
add(id="16528744", qtype="choice",
    question=("다음 보기 중 급수 [[sub(a,1) - sub(a,2) + sub(a,2) - sub(a,3) + sub(a,3) - sub(a,4)]] + ⋯가\n수렴하는 수열 [[set(sub(a,n))]]을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(a,n) = frac(3, 4n)]]\nㄴ. [[sub(a,n) = sqrt(2n + 1) - sqrt(2n)]]\nㄷ. [[sub(a,n) = log(frac(6n, n + 1))]]"),
    choices=CH_G, derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="괄호 없는 급수 → aₙ→0일 때만 수렴: ㄱ✓ ㄴ✓ ㄷ(→log6)✗ → ②.")

# p46
add(id="57b01603", qtype="short",
    question=("다음 보기 중 수렴하는 급수인 것만을 있는 대로 고르시오\n<보기>\n"
              "ㄱ. [[(2 - frac(7,4)) + (frac(7,4) - frac(8,5)) + (frac(8,5) - frac(3,2))]] + ⋯\n"
              "ㄴ. [[5 - frac(9,2) + frac(9,2) - frac(13,3) + frac(13,3) - frac(17,4)]] + ⋯\n"
              "ㄷ. [[1 - frac(4,5) + frac(4,5) - frac(5,7) + frac(5,7) - frac(2,3)]] + ⋯"),
    choices=None, derived_answer="ㄱ", figure=None, difficulty_est=3, confidence=0.85,
    note="ㄱ 괄호 묶음 aₙ=(n+5)/(n+2) → 부분합 2−a_{n+1}→1 수렴 ✓; ㄴ aₙ=(4n+1)/n→4≠0 발산; ㄷ aₙ=(n+2)/(2n+1)→1/2≠0 발산 → ㄱ.")

# p49
add(id="2efa5755", qtype="choice",
    question=("다음 보기의 무한급수 중 수렴하는 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[1 - frac(1,3) + frac(1,3) - frac(1,5) + frac(1,5) - frac(1,7) + frac(1,7)]] − ⋯\n"
              "ㄴ. [[frac(1,2) - frac(2,3) + frac(2,3) - frac(3,4) + frac(3,4)]] − ⋯\n"
              "ㄷ. [[(frac(1,2) - frac(2,3)) + (frac(2,3) - frac(3,4)) + (frac(3,4) - frac(4,5))]] + ⋯"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="ㄱ 항 1/(2n+1)→0 → 1로 수렴 ✓; ㄴ 항 n/(n+1)→1≠0 발산; ㄷ 괄호 묶음 → 1/2−1=−1/2 수렴 ✓ → ③.")

# p52
add(id="2b6bbb15", qtype="short",
    question=("수열 [[set(sub(a,n))]]에 대하여 급수\n[[(3 sub(a,1) - 9) + (frac(3,2) sub(a,2) - 9) + (sub(a,3) - 9) + (frac(3 sub(a,4), 4) - 9)]] + ⋯\n"
              "이 수렴할 때, [[lim(n, inf, frac(8 sub(a,n) + 4n, 3 sub(a,n) - 5n))]]의 값을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.9,
    note="3aₙ/n−9→0 → aₙ/n→3 → (24+4)/(9−5)=7 = 빠른정답 ✓.")

# p78 (id 2개)
dup(["a3658335", "af4b8467"], qtype="choice",
    question=("두 수열 [[set(sub(a,n))]], [[set(sub(b,n))]]에 대하여\n[[sub(a,n) + sub(b,n) = 3 + frac(2,n)]] ([[n]] = 1, 2, 3, ⋯)일 때,\n다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[lim(n, inf, (sub(a,n) + sub(b,n))) = 3]]\nㄴ. 수열 [[set(sub(a,n))]]이 수렴하면 수열 [[set(sub(b,n))]]도 수렴한다.\n"
              "ㄷ. [[sum(n, 1, inf, sub(a,n))]]이 수렴하면 [[sum(n, 1, inf, sub(b,n))]]도 수렴한다."),
    choices=CH_G, derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="ㄱ✓, ㄴ bₙ=3+2/n−aₙ 수렴 ✓, ㄷ Σbₙ=Σ(3+2/n−aₙ) 발산 ✗ → ②. 빠른정답 19와 불일치.")

# p84
_FLOOR_Q = ("다음은 무한급수 [[sum(n, 1, inf, floor(frac(pow({b},{p}), pow(2,n)) + frac(1,2)))]]의 합을 구하는 과정을\n나타낸 것이다.\n(단, [[floor(x)]]는 [[x]]를 넘지 않는 최대의 정수이다.)\n"
            "[[floor(x) = n]] ([[n]]은 정수)로 놓으면 [[n <= x < n + 1]]\n"
            "(ⅰ) [[n <= x < n + frac(1,2)]]일 때, [[floor(x) = n]], [[floor(x + frac(1,2)) = n]], [[floor(2x) = 2n]]\n"
            "(ⅱ) [[n + frac(1,2) <= x < n + 1]]일 때, [[floor(x) = n]], [[floor(x + frac(1,2)) = n + 1]], [[floor(2x) = 2n + 1]]\n"
            "(ⅰ), (ⅱ)에 의하여 [[floor(x) + floor(x + frac(1,2)) = floor(2x)]]이다.\n"
            "한편, [[floor(frac(pow({b},{p}), pow(2,n))) + floor(frac(pow({b},{p}), pow(2,n)) + frac(1,2))]] = (A) 이므로\n"
            "[[sum(k, 1, n, floor(frac(pow({b},{p}), pow(2,k)) + frac(1,2))) = sum(k, 1, n, (floor(frac(pow({b},{p}), pow(2, k - 1))) - floor(frac(pow({b},{p}), pow(2,k)))))]] = (B)\n"
            "∴ [[sum(n, 1, inf, floor(frac(pow({b},{p}), pow(2,n)) + frac(1,2)))]] = (가)\n"
            "이 과정에서 (가)에 알맞은 것은?")
add(id="1f8cb03d", qtype="choice",
    question=_FLOOR_Q.format(b=3, p=4),
    choices=["[[55]]", "[[67]]", "[[73]]", "[[79]]", "[[81]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2004년 11월 고2 이과 14번]. [x]+[x+1/2]=[2x] → 항 = [81/2^{k−1}]−[81/2^k] → 부분합 81−[81/2ⁿ] → 81 → ⑤. 빠른정답 19와 불일치.")

# p85
add(id="b1192b55", qtype="choice",
    question=("수열 [[set(sub(a,n))]]에 대하여 집합\n[[A]] = { [[x]] | [[pow(x,2) - 1 < a < pow(x,2) + 2x]], [[x]]는 자연수 }\n"
              "가 공집합이 되도록 하는 자연수 [[a]]를 작은 수부터\n크기순으로 나열할 때, [[n]]번째 수를 [[sub(a,n)]]이라 하자.\n"
              "예를 들어, [[a = 3]]은 [[pow(x,2) - 1 < a < pow(x,2) + 2x]]를 만족시키는\n자연수 [[x]]가 존재하지 않는 첫 번째 수이므로 [[sub(a,1) = 3]]이다.\n"
              "[[sum(n, 1, inf, frac(1, sub(a,n)))]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]", "[[frac(3,2)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2016년 3월 고3 문과 21번/4점]. 구간 (x²−1, x²+2x) 사이 빈 수 aₙ=(n+1)²−1=n(n+2) → Σ1/(n(n+2))=3/4 → ②.")

# p86
add(id="8b8dfa68", qtype="choice",
    question=_FLOOR_Q.format(b=5, p=3),
    choices=["[[25]]", "[[50]]", "[[75]]", "[[125]]", "[[250]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="[x]+[x+1/2]=[2x] → 부분합 125−[125/2ⁿ] → 125 → ④ = 빠른정답 ✓.")

# p87
add(id="54232162", qtype="choice",
    question=("수열 [[set(sub(a,n))]]에 대하여\n집합 [[A]] = { [[x]] | [[pow(x,2) - 2x < a < pow(x,2) - 1]], [[x]]는 자연수 }가\n"
              "공집합이 되도록 하는 자연수 [[a]]를 작은 수부터 크기순으로\n나열할 때, [[n]]번째 수를 [[sub(a,n)]]이라 하자. 예를 들어, [[a = 3]]은\n"
              "[[pow(x,2) - 2x < a < pow(x,2) - 1]]을 만족시키는 자연수 [[x]]가\n존재하지 않는 첫 번째 수이므로 [[sub(a,1) = 3]]이다.\n"
              "[[sum(n, 1, inf, frac(1, sub(a,n)))]]의 값은?"),
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.9,
    note="구간 (x²−2x, x²−1) 사이 빈 수 aₙ=n(n+2) (3, 8, 15, …) → Σ1/(n(n+2))=3/4 → ③.")

# p88
add(id="191255af", qtype="short",
    question=("다음 그림과 같이 좌표평면 위의 점 [[sub(A,n)]][[point(n, 0)]]에서\n원 [[pow(x,2) + pow(y - n, 2) = 1]]에 두 접선을 그어 만나는 점을 각각\n"
              "[[sub(B,n)]], [[sub(C,n)]]이라 하자. [[sub(a,n) = sub(A,n) sub(B,n) + sub(A,n) sub(C,n)]]이라 할 때,\n"
              "[[sum(n, 3, inf, frac(16, pow(sub(a,n), 2) + 24n + 20))]]의 값을 구하시오.\n(단, [[n]]은 2보다 큰 자연수이다.)"),
    choices=None, derived_answer="frac(1,2)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원 x²+(y−n)²=1, x축 위의 점 Aₙ(n, 0)에서 원에 그은 두 접선과 접점 Bₙ, Cₙ"}}],
    difficulty_est=4, confidence=0.8,
    needs_review=PS + "(선분 AₙBₙ, AₙCₙ의 윗줄은 병치로 전사) / 도형 표현 불가: 원과 두 접선 좌표평면 도형",
    note="접선 길이 √(2n²−1) → aₙ²=8n²−4 → 항 = 2/((n+1)(n+2)) → Σ(n≥3) = 2·(1/4) = 1/2 = 빠른정답 ✓.")

# p92
add(id="7aaf5fe6", qtype="short",
    question=("수열 [[set(sub(a,n))]]의 각 항은 0 또는 1이고\n[[frac(3,8) = sub(a,1) + frac(sub(a,2), 3) + frac(sub(a,3), pow(3,2))]] + ⋯ + [[frac(sub(a,n), pow(3, n - 1))]] + ⋯을 만족할 때,\n"
              "[[sum(n, 1, 200, sub(a,n))]]의 값을 구하시오."),
    choices=None, derived_answer="100", figure=None, difficulty_est=3, confidence=0.9,
    note="3/8 = 1/3+1/27+… (3진 전개 0,1,0,1,…) → 짝수항만 1 → 100 = 빠른정답 ✓.")

# p96
add(id="1fe34bdf", qtype="short",
    question="[[x]]에 대한 이차방정식 [[pow(x,2) + (2n - 1) x + pow(n,2) = 0]]의\n두 근을 [[sub(alpha,n)]], [[sub(beta,n)]]이라 할 때, [[sum(n, 1, inf, frac(4, (sub(alpha,n) - 1)(sub(beta,n) - 1)))]]의\n값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="(α−1)(β−1)=αβ−(α+β)+1=n²+2n → Σ4/(n(n+2))=3 = 빠른정답 ✓.")

# p97
add(id="6f6e2571", qtype="short",
    question="[[x]]에 대한 이차방정식 [[pow(x,2) - 7x + pow(n,2) + n = 0]]의 두 근을\n[[sub(alpha,n)]], [[sub(beta,n)]]이라 할 때, [[sum(n, 1, inf, (frac(1, sub(alpha,n)) + frac(1, sub(beta,n))))]]의 값을 구하시오.\n(단, [[n]]은 자연수이다.)",
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.9,
    note="1/α+1/β = 7/(n(n+1)) → Σ = 7 = 빠른정답 ✓.")

# ───────────── 등비수열의 극한 ─────────────
# p15
add(id="9e952d4b", qtype="choice",
    question="첫째항이 2이고 공비가 [[r]] ([[r > 1]])인 등비수열 [[set(sub(a,n))]]에\n대하여 [[sub(S,n) = sum(k, 1, n, sub(a,k))]]일 때, [[lim(n, inf, frac(sub(a,n), sub(S,n))) = frac(9,10)]]이다.\n이때 [[r]]의 값은?",
    choices=["[[7]]", "[[8]]", "[[9]]", "[[10]]", "[[11]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="aₙ/Sₙ → (r−1)/r = 9/10 → r=10 → ④. 빠른정답 2와 불일치.")

# p38
add(id="5ffbe91e", qtype="choice",
    question="등비수열 [[set(pow((sqrt(2) cos(x)), n))]]이 수렴하도록 하는 [[x]]의 값의\n범위는? (단, [[0 <= x < pi]])",
    choices=["[[frac(pi,4) < x <= frac(3,4) pi]]", "[[frac(pi,6) <= x < frac(3,4) pi]]", "[[frac(pi,4) <= x < frac(3,4) pi]]",
             "[[frac(pi,6) < x <= frac(3,4) pi]]", "[[frac(pi,2) <= x < frac(3,4) pi]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="−1<√2cos x≤1 → −1/√2<cos x≤1/√2 → π/4≤x<3π/4 → ③. 빠른정답 5와 불일치.")

# p68
add(id="b1c78d01", qtype="short",
    question=("그림과 같이 한 변의 길이가 4인 정삼각형 ABC와\n점 A를 지나고 직선 BC와 평행한 직선 [[l]]이 있다.\n"
              "자연수 [[n]]에 대하여 중심 [[sub(O,n)]]이 변 AC 위에 있고\n반지름의 길이가 [[sqrt(3) pow(frac(1,2), n - 1)]]인 원이\n"
              "직선 AB와 직선 [[l]]에 모두 접한다. 이 원과 직선 AB가\n접하는 점을 [[sub(P,n)]], 직선 [[sub(O,n) sub(P,n)]]과 직선 [[l]]이 만나는 점을\n"
              "[[sub(Q,n)]]이라 하자. 삼각형 B[[sub(O,n)]][[sub(Q,n)]]의 넓이를 [[sub(S,n)]]이라 할 때,\n"
              "[[lim(n, inf, pow(2,n) sub(S,n)) = k]]이다. [[pow(k,2)]]의 값을 구하시오."),
    choices=None, derived_answer="192",
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 ABC(B 왼쪽 아래, C 오른쪽 아래, A 위), A를 지나 BC와 평행한 직선 l, 변 AC 위 중심 Oₙ의 원(AB·l에 접함), AB 위 접점 Pₙ, 직선 OₙPₙ과 l의 교점 Qₙ, 삼각형 BOₙQₙ"}}],
    difficulty_est=4, confidence=0.8,
    needs_review=PS + " / 도형 표현 불가: 정삼각형·접원·평행선 복합 도형",
    note="출처 [2016년 7월 고3 문과 29번/4점]. A 원점, l: y=0, r=√3/2^{n−1}: Oₙ=(r/√3, −r), Qₙ=(−2r/√3, 0) → Sₙ=4r−r²/√3 → 2ⁿSₙ→8√3 → k²=192. 빠른정답 4와 불일치.")
