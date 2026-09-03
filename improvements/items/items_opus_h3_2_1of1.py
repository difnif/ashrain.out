# -*- coding: utf-8 -*-
# esc_opus_h3-2_1of1 — 이미지 기준 전사 (44 항목 / 43쪽, 미적분). 등비수열의 극한 p88은 id 2개.
# 표기 관행: 도함수 적용 f′(x)는 prime(f)(x)(파서는 곱으로 해석) → needs_review PR.
#            조각적 정의 { … (조건) ; … (조건) }는 텍스트 혼합 → needs_review PW.
#            첨자 함수 적용 S₁(t)는 sub(S,1)(t)(파서는 곱으로 해석) → needs_review PS.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

PR = "문법 범위 밖: 도함수 적용 표기 f′(x)를 prime(f)(x)로 전사(파서는 곱으로 해석)"
PW = "문법 범위 밖: 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사"
PS = "문법 범위 밖: 첨자 함수 적용 표기 S₁(t)를 sub(S,1)(t)로 전사(파서는 곱으로 해석)"

# ───────────────────────── 치환적분법 ─────────────────────────
# p73 — [2020년 10월 고3 이과 30번 변형]
add(id="2a5830d9", qtype="short",
    question=("최고차항의 계수가 [[p]] ([[p > 0]])인 이차함수 [[f(x)]]에 대하여 [[f(0) = f(-4)]]이다. "
              "이때 함수 [[g(x) = (a x + b) pow(e, f(x))]] ([[a < 0]])이 다음 조건을 모두 만족시킨다.\n"
              "(가) 모든 실수 [[x]]에 대하여 [[(x + 2)(g(x) - m x - 2m) <= 0]]을 만족시키는 실수 [[m]]의 최솟값은 [[-1]]이다.\n"
              "(나) [[dinteg(0, 1, g(x), x) = dinteg(-f(-4), 1, g(x), x) = frac(pow(e,4) - pow(e,9), 2p)]]\n"
              "[[f(a + b)]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="1", figure=None, difficulty_est=5, confidence=0.85,
    note="출처 [2020년 10월 고3 이과 30번 변형]. b=2a, m최솟값 ae^{f(-2)}=-1, 적분조건 → p=1, f(x)=(x+2)², a=-1, b=-2 → f(-3)=1 = 빠른정답 ✓ (f(-4)=0인 퇴화 해도 존재하나 의도 답 1). 원문 중괄호 {g(x)−mx−2m}는 소괄호로.")

# p83
add(id="59a20542", qtype="short",
    question=("1보다 큰 실수 전체의 집합에서 정의된 함수 [[f(x) = frac(sin(ln(x)), x)]]가 극값을 갖도록 하는 [[x]]의 값을 작은 수부터 차례로 "
              "[[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯이라 하고, 함수 [[y = f(x)]]의 그래프가 [[x]]축과 만나는 점의 [[x]]좌표를 작은 수부터 차례로 "
              "[[sub(b,1)]], [[sub(b,2)]], [[sub(b,3)]], ⋯이라 하자. [[sub(S,n) = dinteg(sub(a,n), sub(b,n), f(x), x)]]라 할 때, "
              "[[sum(n, 1, n, sub(S,n)) = 0]]을 만족시키는 20 이하의 자연수 [[N]]의 개수를 [[p]], [[m < l <= 20]]이고 "
              "[[dinteg(sub(a,m), sub(a,l), f(x), x) = 0]]을 만족시키는 두 자연수 [[m]], [[l]]의 순서쌍 [[point(m, l)]]의 개수를 [[q]]라 할 때, "
              "[[p + q]]의 값을 구하시오."),
    choices=None, derived_answer="100", figure=None, difficulty_est=4, confidence=0.8,
    note="원문 Σ의 위끝이 'n'으로 인쇄됨(N의 오타로 보이나 그대로 전사). S_n=(−1)^{n−1}(1+√2/2) → N 짝수 10개(p=10), ∫=0 ⇔ m,l 같은 홀짝 → q=2·C(10,2)=90 → 100. 빠른정답 4와 불일치.")

# p88 — [2020년 7월 고3 이과 30번 변형]
add(id="0362e7e0", qtype="short",
    question=("함수 [[f(x) = a cos(pi x)]] ([[a > 0]])에 대하여 함수 [[g(x)]]를 [[g(x) = pow(e, f(x)) - f(x)]] ([[0 < x <= 10]])이라 하자. "
              "함수 [[g(x)]]가 [[x = alpha]]에서 극대 또는 극소인 모든 [[alpha]]를 작은 수부터 크기순으로 나열한 것을 "
              "[[sub(alpha,1)]], [[sub(alpha,2)]], [[sub(alpha,3)]], ⋯, [[sub(alpha,m)]] ([[m]]은 자연수)라 하자. "
              "함수 [[g(x)]]가 서로 다른 두 개의 극댓값을 갖고 그 합이 [[pow(e,2) + pow(e,-2)]]일 때, "
              "[[pi dinteg(sub(alpha,1), sub(alpha,m), g(x) sin(pi x), x) = p + q pow(e,2)]]이다. [[p - q]]의 값을 구하시오. "
              "(단, [[a]]는 상수, [[p]]와 [[q]]는 유리수이다.)"),
    choices=None, derived_answer="2", figure=None, difficulty_est=5, confidence=0.85,
    note="출처 [2020년 7월 고3 이과 30번 변형]. 극댓값 e^a−a, e^{−a}+a 합 → a=2; α₁=1/2, α_m=10, u=f(x) 치환 → −(1/2)[e^u−u²/2]₀² = 3/2 − e²/2 → p−q=2. 빠른정답 5와 불일치.")

# ───────────────────────── 부분적분법 ─────────────────────────
# p62 — [2018년 3월 고3 이과 30번/4점]
add(id="85f5cbaa", qtype="short",
    question=("함수\n[[f(x)]] = { [[pow(e, x)]] ([[0 <= x < 1]]) ; [[pow(e, 2 - x)]] ([[1 <= x <= 2]]) }\n"
              "에 대하여 열린 구간 [[itv(0, 2, oo)]]에서 정의된 함수\n[[g(x) = dinteg(0, x, abs(f(x) - f(t)), t)]]\n"
              "의 극댓값과 극솟값의 차는 [[a e + b root(3, pow(e,2))]] 이다. [[pow(a b, 2)]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수이다.)"),
    choices=None, derived_answer="36", figure=None, difficulty_est=5, confidence=0.8, needs_review=PW,
    note="출처 [2018년 3월 고3 이과 30번/4점]. g(1)=1 극대, g(4/3)=1+2e−3e^{2/3} 극소 → 차 −2e+3∛e² → a=−2, b=3 → 36. 빠른정답 2와 불일치.")

# p64 — [2023년 11월 고3 미적분 30번/4점]
add(id="e2975b44", qtype="short",
    question=("실수 전체의 집합에서 미분가능한 함수 [[f(x)]]의 도함수 [[prime(f)(x)]]가 [[prime(f)(x) = abs(sin(x)) cos(x)]]이다. "
              "양수 [[a]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[point(a, f(a))]]에서의 접선의 방정식을 [[y = g(x)]]라 하자. "
              "함수 [[h(x) = dinteg(0, x, (f(t) - g(t)), t)]]가 [[x = a]]에서 극대 또는 극소가 되도록 하는 모든 양수 [[a]]를 작은 수부터 크기순으로 나열할 때, "
              "[[n]]번째 수를 [[sub(a,n)]]이라 하자. [[frac(100, pi)(sub(a,6) - sub(a,2))]]의 값을 구하시오."),
    choices=None, derived_answer="125", figure=None, difficulty_est=5, confidence=0.85, needs_review=PR,
    note="출처 [2023년 11월 고3 미적분 30번/4점]. f−g 부호 변화점: π/4+kπ/2 및 x=kπ(꺾임점) → a₂=3π/4, a₆=2π → 125 = 빠른정답 ✓. 원문 중괄호 {f(t)−g(t)}는 소괄호로.")

# p67 — 변형
add(id="4c87a401", qtype="short",
    question=("실수 전체의 집합에서 미분가능한 함수 [[f(x)]]의 도함수 [[prime(f)(x)]]가 [[prime(f)(x) = abs(cos(x)) sin(x)]]이다. "
              "양수 [[a]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[point(a, f(a))]]에서의 접선의 방정식을 [[y = g(x)]]라 하자. "
              "함수 [[h(x) = dinteg(0, x, (f(t) - g(t)), t)]]가 [[x = a]]에서 극대 또는 극소가 되도록 하는 모든 양수 [[a]]를 작은 수부터 크기순으로 나열할 때, "
              "[[n]]번째 수를 [[sub(a,n)]]이라 하자. [[frac(60, pi)(sub(a,5) - sub(a,3))]]의 값을 구하시오."),
    choices=None, derived_answer="45", figure=None, difficulty_est=5, confidence=0.85, needs_review=PR,
    note="출처 [2023년 11월 고3 미적분 30번 변형]. 부호 변화점: π/4+kπ/2 및 x=π/2+kπ → a₃=3π/4, a₅=3π/2 → 60·3/4=45 = 빠른정답 ✓. 원문 중괄호는 소괄호로.")

# ───────────────────────── 넓이 ─────────────────────────
_SEMI_FIG = [{"fn": "unsupported", "args": {"raw": "선분 AB를 지름으로 하는 반원, AB 위의 점 P에서 세운 수선이 반원과 만나는 점 Q, 두 선분 AP·PQ와 호 AQ로 둘러싸인 영역 S(x) 음영, AP=x 점선 표시, P에서 직각 표시"}}]
_SEMI_RV = "도형 표현 불가: 반원+수선+음영 영역 도형"
# p1
add(id="4649dc25", qtype="short",
    question=("그림과 같이 길이가 2인 선분 AB 위의 점 P를 지나고 선분 AB에 수직인 직선이 선분 AB를 지름으로 하는 반원과 만나는 점을 Q라 하자. "
              "[[seg(AP) = x]]라 할 때, [[S(x)]]를 다음과 같이 정의한다. [[0 < x < 2]]일 때 [[S(x)]]는 두 선분 AP, PQ와 호 AQ로 둘러싸인 도형의 넓이이고, "
              "[[x = 2]]일 때 [[S(x)]]는 선분 AB를 지름으로 하는 반원의 넓이이다.\n"
              "[[dinteg(frac(pi,4), pi, S(1 + sin(theta)) - S(1 + cos(theta)), theta) = p + q pow(pi,2)]]일 때 [[frac(30p, q)]]의 값을 구하시오. "
              "(단, [[p]]와 [[q]]는 유리수이다.)"),
    choices=None, derived_answer="96", figure=_SEMI_FIG, difficulty_est=5, confidence=0.85, needs_review=_SEMI_RV,
    note="피적분함수: [π/4,π/2]에서 θ−π/4, [π/2,π]에서 (π/2−sin2θ)/2 → 1/2+5π²/32 → 30p/q=96 = 빠른정답 ✓. 원문 중괄호는 dinteg 안에서 생략.")

# p2
add(id="0442561d", qtype="short",
    question=("다음 그림과 같이 길이가 4인 선분 AB 위의 점 P를 지나고 선분 AB에 수직인 직선이 선분 AB를 지름으로 하는 반원과 만나는 점을 Q라 하자. "
              "[[seg(AP) = x]]라 할 때, [[S(x)]]를 다음과 같이 정의한다. [[0 < x < 4]]일 때 [[S(x)]]는 두 선분 AP, PQ와 호 AQ로 둘러싸인 도형의 넓이이고, "
              "[[x = 4]]일 때 [[S(x)]]는 선분 AB를 지름으로 하는 반원의 넓이이다.\n"
              "[[dinteg(0, pi, S(2 + 2 sin(theta)) - S(2 + 2 cos(theta)), theta) = p + q pow(pi,2)]]일 때, [[8 p q]]의 값을 구하시오. "
              "(단, [[p]]와 [[q]]는 유리수이다.)"),
    choices=None, derived_answer="8", figure=_SEMI_FIG, difficulty_est=5, confidence=0.85, needs_review=_SEMI_RV,
    note="반지름 2 → 4배: [0,π/2] 적분 0, [π/2,π] 적분 π²/8+1/2 → 2+π²/2 → 8pq=8 = 빠른정답 ✓.")

# p10 — [2017년 10월 고3 이과 30번 변형]
add(id="f8ad1ab7", qtype="short",
    question=("다음 그림과 같이 길이가 2인 선분 AB 위의 점 P를 지나고 선분 AB에 수직인 직선이 선분 AB를 지름으로 하는 반원과 만나는 점을 Q라 하자. "
              "[[seg(AP) = x]]라 할 때, [[S(x)]]를 다음과 같이 정의한다. [[0 < x < 2]]일 때 [[S(x)]]는 두 선분 AP, PQ와 호 AQ로 둘러싸인 도형의 넓이이고, "
              "[[x = 2]]일 때 [[S(x)]]는 선분 AB를 지름으로 하는 반원의 넓이이다.\n"
              "[[dinteg(frac(pi,3), frac(2,3) pi, S(1 + sin(theta)) - S(1 + cos(theta)), theta) = p + q pow(pi,2)]]\n"
              "일 때, [[frac(40p, q)]]의 값을 구하시오. (단, [[p]]와 [[q]]는 유리수이다.)"),
    choices=None, derived_answer="72", figure=_SEMI_FIG, difficulty_est=5, confidence=0.85, needs_review=_SEMI_RV,
    note="출처 [2017년 10월 고3 이과 30번 변형]. π²/36 + (π²/24+1/8) = 1/8+5π²/72 → 40p/q=72 = 빠른정답 ✓.")

# p43
add(id="1bd42de5", qtype="choice",
    question=("[[0 < t < 1]]인 실수 [[t]]에 대하여 직선 [[y = 2t x]]가 곡선 [[y = 2x pow(e, -x)]]과 만나는 점 중 원점이 아닌 점을 P라 하자. "
              "직선 [[y = 2t x]]와 곡선 [[y = 2x pow(e, -x)]]으로 둘러싸인 부분의 넓이를 [[sub(S,1)(t)]]라 하고, "
              "점 P를 지나고 [[x]]축에 수직인 직선과 직선 [[y = 2t x]] 및 [[x]]축으로 둘러싸인 부분의 넓이를 [[sub(S,2)(t)]]라 하자. "
              "집합 [[setb(t, 0 < t < 1)]]에서 정의된 함수 [[f(t) = sub(S,1)(t) - sub(S,2)(t)]]가 [[t = alpha]]에서 극솟값을 가질 때, "
              "[[frac(f(alpha), alpha)]]의 값은?"),
    choices=["[[2e]]", "[[2e - 2]]", "[[2e - 4]]", "[[2e - 6]]", "[[2e - 8]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85, needs_review=PS,
    note="k=−ln t, f=2−e^{−k}(2k²+2k+2), df/dk=2ke^{−k}(k−1) → 극소 t=1/e, f(α)=2−6/e → f(α)/α=2e−6 → ④. 빠른정답 2와 불일치.")

# p62 — [2024년 사관학교 미적분 28번 변형]
add(id="6c76a99a", qtype="choice",
    question=("실수 전체의 집합에서 연속인 함수 [[f(x)]]가 모든 실수 [[x]]에 대하여 [[dinteg(0, x, (x - t) f(t), t) = 2 pow(e, 2x) - 4x + a]]를 만족시킨다. "
              "곡선 [[y = f(x)]] 위의 점 [[point(a, f(a))]]에서의 접선을 [[l]]이라 할 때, 곡선 [[y = f(x)]]와 직선 [[l]] 및 [[y]]축으로 둘러싸인 부분의 넓이는? "
              "(단, [[a]]는 상수이다.)"),
    choices=["[[2 - frac(48, pow(e,4))]]", "[[2 - frac(52, pow(e,4))]]", "[[2 - frac(56, pow(e,4))]]", "[[4 - frac(52, pow(e,4))]]", "[[4 - frac(56, pow(e,4))]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2024년 사관학교 미적분 28번 변형]. a=−2, f(x)=8e^{2x}, 접선 y=16e^{−4}x+40e^{−4}, ∫_{−2}^0 = 4−52e^{−4} → ④ = 빠른정답 ✓.")

# p65
add(id="009c373d", qtype="short",
    question=("원 [[pow(x,2) + pow(y,2) = 2]] 위의 점 [[point(a, b)]]에서 곡선 [[y = 2 pow(x,2)]]에 그은 두 접선과 곡선 [[y = 2 pow(x,2)]]으로 둘러싸인 영역의 넓이를 [[S]]라 할 때, "
              "[[S]]의 최댓값은 [[frac(q, p) sqrt(33)]] 이다. 서로소인 두 자연수 [[p]], [[q]]에 대하여 [[p + q]]의 값을 구하시오. (단, [[b < 0]])"),
    choices=None, derived_answer="27", figure=None, difficulty_est=4, confidence=0.85,
    note="접점 s₁,s₂: 2s²−4as+b=0, S=(s₂−s₁)³/6, (s₂−s₁)²=8−4b²−2b 최대 33/4 (b=−1/4) → S=11√33/16 → p+q=27. 빠른정답 4와 불일치.")

# p91 — [2019년 6월 고3 이과 30번 변형]
add(id="c9d2b1ee", qtype="short",
    question=("상수 [[a]], [[b]]에 대하여 함수 [[f(x) = a pow(sin(x), 3) + b sin(x)]]가 [[f(frac(pi,4)) = sqrt(2)]], [[f(frac(pi,3)) = 2 sqrt(3)]] 을 만족시킨다. "
              "실수 [[t]] ([[1 < t < 6]])에 대하여 함수 [[y = f(x)]]의 그래프와 직선 [[y = t]]가 만나는 점의 [[x]]좌표 중 양수인 것을 작은 수부터 크기순으로 모두 나열할 때, "
              "[[n]]번째 수를 [[sub(x,n)]]이라 하고 [[sub(c,n) = dinteg(sqrt(2), 2 sqrt(3), frac(t, prime(f)(sub(x,n))), t)]]라 하자. "
              "[[sum(n, 1, 51, sub(c,n)) = p sqrt(2) + q]]일 때, [[p - q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 유리수이다.)"),
    choices=None, derived_answer="5", figure=None, difficulty_est=5, confidence=0.85, needs_review=PR,
    note="출처 [2019년 6월 고3 이과 30번 변형]. a=8, b=−2; c_n=(−1)^{n−1}∫_{π/4}^{π/3}f dx, 합=I=−8/3+7√2/3 → p−q=5 = 빠른정답 ✓.")

# ───────────────────────── 함수의 그래프 ─────────────────────────
# p99 — 같은 이미지에 문항 2개. 위 문항([2017년 3월 고3 이과 30번 변형], src_tag '최대·최소의 활용'과 부합)을 전사.
add(id="c8fb9377", qtype="short",
    question=("다음 그림과 같이 [[y = -frac(1,2) x]] 위의 제2사분면에 있는 점 P에서 곡선 [[y = frac(1, x)]]에 그은 두 접선의 접점을 각각 A, B라 할 때, "
              "[[pow(seg(PA), 2) + pow(seg(PB), 2)]]의 최솟값은 [[p + q sqrt(2)]] 이다. [[p + q]]의 값을 구하시오. (단, [[p]], [[q]]는 자연수이다.)"),
    choices=None, derived_answer="25",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=1/x(두 가지), 직선 y=−x/2, 제2사분면 위의 점 P에서 곡선에 그은 두 접선과 접점 A(제1사분면), B(제3사분면)"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="같은 이미지에 문항 2개(위: 2017년 3월 고3 이과 30번 변형 — 전사함 / 아래: 2017년 10월 고3 이과 21번 변형 — 반원 색종이를 AP로 접어 호 AP·호 PB·선분 AB로 둘러싸인 넓이 S(θ), S′(α)=2일 때 cos2α는? 선지 ①1/8 ②1/4 ③3/8 ④1/2 ⑤5/8, 그림 2개) — 빠른정답 4는 아래 문항의 답 ④(cos2α=1/2)와 일치 / 도형 표현 불가: 좌표평면 곡선·접선 도형",
    note="위 문항: P(−2k,k), 접점 s₁+s₂=2/k, s₁s₂=−2 → PA²+PB²=5/k²+10k²+15 ≥ 15+10√2 → p+q=25. 아래 문항: S(θ)=sin2θ−sin4θ/2, S′=2 ⇔ cos2α=1/2 → ④.")

# ───────────────────────── 음함수와 역함수의 미분법 ─────────────────────────
# p90 — [2021년 10월 고3 미적분 30번 변형]
add(id="ee440096", qtype="short",
    question=("[[a < b]]인 서로 다른 두 양수 [[a]], [[b]]에 대하여 함수 [[f(x)]]를 [[f(x) = -frac(a pow(x,3) + 3b x, pow(x,2) + 2)]]라 하자. "
              "모든 실수 [[x]]에 대하여 [[prime(f)(x) != 0]]이고, 두 함수 [[g(x) = f(x) - inv(f)(x)]], [[h(x) = (comp(g, f))(x)]]가 다음 조건을 모두 만족시킨다.\n"
              "(가) [[g(1) = h(0)]]\n(나) [[prime(g)(1) = -2 prime(h)(1)]]\n"
              "[[18(b - a)]]의 값을 구하시오."),
    choices=None, derived_answer="12", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PR + " / 역함수 적용 f⁻¹(x)는 inv(f)(x), 합성함수 적용 (g∘f)(x)는 (comp(g,f))(x)로 전사(파서는 곱으로 해석)",
    note="출처 [2021년 10월 고3 미적분 30번 변형]. f 감소·홀함수, g(1)=0 ⇒ f(1)=−1 ⇒ a+3b=3; u=f′(1): (2u+1)(u²−1)=0, a<b ⇒ u=−1/2 ⇒ 7a+3b=9/2 ⇒ a=1/4, b=11/12 → 18(b−a)=12. 빠른정답 11과 불일치.")

# ───────────────────────── 합성함수의 미분법 ─────────────────────────
# p69 — [2020년 6월 고3 이과 30번 변형]
add(id="51e88abc", qtype="short",
    question=("실수 전체의 집합에서 정의된 함수 [[f(x)]]는 [[0 <= x <= 4]]일 때 [[f(x) = abs(x - 1) + abs(x - 3)]]이고, 모든 실수 [[x]]에 대하여 [[f(x) = f(x + 4)]]를 만족시킨다. "
              "함수 [[g(x)]]를 [[g(x) = lim(h, 0, abs(frac(f(pow(3, x + h)) - f(pow(3, x)), h)), +)]]이라 하자. "
              "함수 [[g(x)]]가 [[x = a]]에서 불연속인 [[a]]의 값 중에서 열린 구간 [[itv(-5, 5, oo)]]에 속하는 모든 값을 작은 수부터 크기순으로 나열한 것을 "
              "[[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,n)]] ([[n]]은 자연수)라 할 때, [[n + sum(k, 1, n, frac(g(sub(a,k)), 30 × ln(3)))]]의 값을 구하시오."),
    choices=None, derived_answer="605",
    figure=[{"fn": "unsupported", "args": {"raw": "y=f(x)의 그래프: 주기 4의 꺾은선, x=−1,1,3,5에서 2(평평한 구간 [1,3]), x=0,4에서 최댓값 4, 점선 보조선"}}],
    difficulty_est=5, confidence=0.8, needs_review="도형 표현 불가: 함수 그래프",
    note="출처 [2020년 6월 고3 이과 30번 변형]. 불연속점 3^x=홀수(1~241) → n=121, g(a_k)=2·u·ln3 (u≡3 mod 4) → Σ/(30ln3)=484 → 605(수치 검증). 빠른정답 3과 불일치.")

# p73 — [2020년 6월 고3 이과 30번/4점]
add(id="63effb35", qtype="short",
    question=("실수 전체의 집합에서 정의된 함수 [[f(x)]]는 [[0 <= x < 3]]일 때 [[f(x) = abs(x - 1) + abs(x - 2)]]이고, 모든 실수 [[x]]에 대하여 [[f(x + 3) = f(x)]]를 만족시킨다. "
              "함수 [[g(x)]]를 [[g(x) = lim(h, 0, abs(frac(f(pow(2, x + h)) - f(pow(2, x)), h)), +)]]이라 하자. "
              "함수 [[g(x)]]가 [[x = a]]에서 불연속인 [[a]]의 값 중에서 열린 구간 [[itv(-5, 5, oo)]]에 속하는 모든 값을 작은 수부터 크기순으로 나열한 것을 "
              "[[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,n)]] ([[n]]은 자연수)라 할 때, [[n + sum(k, 1, n, frac(g(sub(a,k)), ln(2)))]]의 값을 구하시오."),
    choices=None, derived_answer="331",
    figure=[{"fn": "unsupported", "args": {"raw": "y=f(x)의 그래프: 주기 3의 꺾은선, x=0,3,6에서 최댓값 3, 구간 [1,2],[4,5]에서 1, x축 눈금 −1~7, 점선 보조선"}}],
    difficulty_est=5, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프",
    note="출처 [2020년 6월 고3 이과 30번/4점]. 불연속점 2^x∈{1..31, 3의 배수 제외} → n=21, Σg/ln2=2(2+5+…+29)=310 → 331 = 빠른정답 ✓.")

# ───────────────────────── 속도와 거리 ─────────────────────────
# p26
add(id="cb9224c7", qtype="short",
    question=("양의 실수 전체의 집합에서 이계도함수를 갖는 함수 [[f(t)]]에 대하여 좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t >= 2]])에서의 위치 [[point(x, y)]]가 "
              "[[x = 4 ln(t)]], [[y = f(t)]]이다. 점 P가 점 [[point(4 ln(2), f(2))]]로부터 움직인 거리가 [[s]]가 될 때 시각 [[t]]는 [[t = frac(s + sqrt(pow(s,2) + 16), 2)]] 이고, "
              "[[t = 4]]일 때 점 P의 속도는 [[point(1, frac(3,4))]]이다. 시각 [[t = 4]]일 때 점 P의 가속도를 [[point(-frac(1,4), a)]]라 할 때, [[160a]]의 값을 구하시오."),
    choices=None, derived_answer="20", figure=None, difficulty_est=4, confidence=0.85,
    note="s=t−4/t, 속력 1+4/t², f′(t)²=(1−4/t²)² → f′=1−4/t², f″(4)=1/8 → 160a=20. 빠른정답 4와 불일치. 원문 연립 중괄호 {x=4ln t, y=f(t)}는 콤마 나열로.")

# p27
add(id="55a988b5", qtype="choice",
    question=("시각 [[t = 0]]일 때 원점을 출발하여 좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t > 0]])에서의 위치 [[point(x, y)]]가 [[x = t]], [[y = f(t)]]이다. "
              "점 P가 다음 조건을 만족시킬 때, 시각 [[t = ln(4)]]에서 점 P의 [[y]]좌표는?\n"
              "(가) [[t > 0]]인 모든 실수 [[t]]에 대하여 함수 [[prime(f)(t)]]는 연속이고, [[prime(f)(ln(4)) > 0]]이다.\n"
              "(나) 모든 양의 실수 [[a]]에 대하여 점 P가 시각 [[t = 0]]에서 [[t = a]]까지 움직인 거리가 [[s]]일 때, [[a = ln(s + sqrt(pow(s,2) + 1))]]이다."),
    choices=["[[1]]", "[[frac(17,16)]]", "[[frac(9,8)]]", "[[frac(19,16)]]", "[[frac(5,4)]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85, needs_review=PR,
    note="s=sinh a, 속력 cosh t → f′=sinh t, f=cosh t−1 → f(ln4)=17/8−1=9/8 → ③ = 빠른정답 ✓.")

_CURVE_Q = ("미분가능한 함수 [[f(theta)]], [[g(theta)]]에 대하여 [[0 < theta < frac(pi,2)]] 에서 정의된 곡선 [[x = f(theta)]], [[y = g(theta)]] 위의 임의의 점 "
            "[[point(f(theta), g(theta))]]에서의 접선의 기울기는 [[{slope}]]이고 [[y]]절편은 [[{icpt}]]이다. [[{lo} <= theta <= {hi}]] 에서 주어진 곡선의 길이는?")
# p91
add(id="905c0eca", qtype="choice",
    question=_CURVE_Q.format(slope="cot(theta)", icpt="-cos(theta)", lo="frac(pi,4)", hi="frac(pi,3)"),
    choices=["[[frac(1,4)]]", "[[frac(3,8)]]", "[[frac(1,2)]]", "[[frac(5,8)]]", "[[frac(3,4)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.9,
    note="접선 y=cotθ·x−cosθ 위에 (f,g), g′=cotθ f′ → f=sin³θ, g=−cos³θ, 길이 ∫(3/2)sin2θ = 3/8 → ② = 빠른정답 ✓.")

# p97
add(id="e149946b", qtype="choice",
    question=_CURVE_Q.format(slope="-cot(theta)", icpt="cos(theta)", lo="frac(pi,4)", hi="frac(pi,3)"),
    choices=["[[frac(1,8)]]", "[[frac(1,4)]]", "[[frac(3,8)]]", "[[frac(1,2)]]", "[[frac(5,8)]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.9,
    note="f=sin³θ, g=cos³θ, 길이 ∫_{π/4}^{π/3}(3/2)sin2θ = 3/8 → ③ = 빠른정답 ✓.")

# p98
add(id="5823f5bf", qtype="choice",
    question=_CURVE_Q.format(slope="cot(theta)", icpt="-cos(theta)", lo="frac(pi,6)", hi="frac(pi,4)"),
    choices=["[[frac(1,8)]]", "[[frac(3,16)]]", "[[frac(1,4)]]", "[[frac(5,16)]]", "[[frac(3,8)]]"],
    derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.9,
    note="f=sin³θ, g=−cos³θ, 길이 ∫_{π/6}^{π/4}(3/2)sin2θ = 3/8 → ⑤ = 빠른정답 ✓.")

# ───────────────────────── 부피 ─────────────────────────
# p44
_VOL = "[[frac(pi,6)(pow(e,5) + 3 pow(e,4) + 3 pow(e,3) - pow(e,2) - {c})]]"
add(id="0288baf1", qtype="choice",
    question=("[[x > 0]]에서 미분가능한 함수 [[f(x)]]가 다음 조건을 만족한다.\n"
              "(가) [[f(1) = 0]], [[prime(f)(1) = 2]]\n"
              "(나) [[1 < a < b < pow(e,3)]]이면 [[prime(f)(a) >= prime(f)(b)]]\n"
              "(다) 구간 [[itv(1, pow(e,2), oo)]]에서 [[prime(f, 2)(x) = -frac(2, pow(x,2))]]\n"
              "(라) 구간 [[itv(pow(e,2), pow(e,3), cc)]]에서 [[f(x) >= 0]]\n"
              "함수 [[y = f(x)]]의 그래프 위의 한 점 P에서 [[x]]축에 내린 수선의 발을 Q라 하고 선분 PQ를 지름으로 하는 반원을 좌표평면에 수직으로 세운다. "
              "점 P가 함수 [[y = f(x)]] ([[1 <= x <= pow(e,3)]])의 그래프 위를 움직일 때, 이 반원에 의하여 생기는 입체도형의 부피의 최댓값은?"),
    choices=[_VOL.format(c=6), _VOL.format(c=5), _VOL.format(c=4), _VOL.format(c=3), _VOL.format(c=2)],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.85, needs_review=PR,
    note="(1,e²)에서 f=2ln x, [e²,e³]에서 f≤2x/e²+2(등호일 때 최대) → V=(π/8)[(8e²−8)+(4/3)(e⁵+3e⁴+3e³−7e²)] = (π/6)(e⁵+3e⁴+3e³−e²−6) → ①. 빠른정답 128은 선지 범위 밖.")

# ───────────────────────── 등비수열의 극한 ─────────────────────────
# p70 — [2009년 3월 고3 문과 29번]
add(id="5fe92d90", qtype="choice",
    question=("그림은 함수 [[f(x) = 2 abs(x - frac(1,2))]] ([[0 <= x <= 1]])의 그래프이다.\n"
              "자연수 [[n]]에 대하여 집합 [[sub(A,n)]]을\n[[sub(A,n)]] = { [[x]] | [[pow(f, n)(x) = 1]], [[0 <= x <= 1]] }\n"
              "이라 할 때, 집합 [[sub(A,n)]]의 원소의 개수를 [[sub(a,n)]]이라 하자. "
              "예를 들어 [[sub(A,1) = set(0, 1)]], [[sub(A,2) = set(0, frac(1,2), 1)]]이므로 [[sub(a,1) = 2]], [[sub(a,2) = 3]]이다. "
              "[[lim(n, inf, frac(sub(a,n), sub(a, n + 1)))]]의 값은?\n"
              "(단, [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]] = 1, 2, 3, ⋯) 이다.)"),
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(3,4)]]", "[[1]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "y=f(x)=2|x−1/2| (0≤x≤1)의 그래프: (0,1), (1/2,0), (1,1)을 잇는 V자 꺾은선, y=1과 x=1 점선 보조선"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프 / 문법 범위 밖: 합성함수의 거듭제곱 표기 fⁿ(x)를 pow(f,n)(x)로 전사(파서는 곱으로 해석)",
    note="출처 [2009년 3월 고3 문과 29번]. a_n=2^{n−1}+1 → 극한 1/2 → ②. 빠른정답 432는 선지 범위 밖.")

# p86 — [2015년 6월 고2 이과 30번/4점]
add(id="59261dab", qtype="short",
    question=("두 집합 [[A]] = { [[2l]] | [[l]]은 자연수 }, [[B]] = { [[pow(2, m)]] | [[m]]은 자연수 } 가 있다. 집합 [[A]] 의 원소 [[a]]에 대하여 "
              "집합 [[B]]의 원소 중 [[a]]의 약수의 최댓값을 [[M(a)]]라 하자. 예를 들어, [[M(2) = 2]], [[M(12) = 4]]이다.\n"
              "수열 [[set(sub(a,n))]]을 [[sub(a,n) = sum(k, 1, pow(2, n - 1), M(2k))]] ([[n]] = 1, 2, 3, ⋯)\n"
              "라 할 때, [[lim(n, inf, frac(150 sub(a,n), (3n + 1) × pow(2, n)))]] 의 값을 구하시오."),
    choices=None, derived_answer="25", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2015년 6월 고2 이과 30번/4점]. a_n=2^{n−1}(n+1) (a₁=2, a₂=6 확인) → 150·(1/2)·(1/3)=25. 빠른정답 7과 불일치.")

# p88 — [2004년 6월 고3 이과 16번] (id 2개)
dup(["25707271", "5dc849b1"], qtype="choice",
    question=("한 변의 길이가 1인 정삼각형 ABC가 있다. 양수 [[r]] 에 대하여 점 [[sub(P,n)]]을 다음 규칙에 따라 정한다.\n"
              "(가) 점 [[sub(P,1)]]은 꼭짓점 A이다.\n"
              "(나) 점 [[sub(P, n + 1)]]은 점 [[sub(P,n)]]에서 정삼각형 ABC의 변을 따라 시계 반대 방향으로 [[pow(r, n)]] 만큼 이동한 점이다.\n"
              "집합 [[S]]를 [[S]] = { [[sub(P,n)]] | [[n]]은 자연수 }라 할 때, <보기>에서 옳은 것을 모두 고른 것은?\n<보기>\n"
              "ㄱ. [[r = 2]]이면, 점 [[sub(P,3)]]은 꼭짓점 C이다.\n"
              "ㄴ. [[r = frac(4,5)]]이면, 변 CA위에 [[S]]의 원소가 무수히 많다.\n"
              "ㄷ. [[0 < r < frac(1,2)]]이면, 변 AB위에 [[S]]의 원소가 무수히 많다."),
    choices=["ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 위)"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 정삼각형 ABC 그림(꼭짓점 배치)",
    note="출처 [2004년 6월 고3 이과 16번]. ㄱ: P₂=C, P₃=C+4≡A ✗; ㄴ: 위치 합→4≡1(B) 접근, CA(2~3) 위 유한개 ✗; ㄷ: 합<1이므로 AB 위 무수히 많음 ✓ → ②. 빠른정답 35는 선지 범위 밖. 원문 첨자 점 라벨 P_n은 sub(P,n).")

# p95
add(id="930e83c4", qtype="choice",
    question=("두 집합\n[[A]] = { [[3l]] | [[l]]은 자연수 }, [[B]] = { [[pow(3, m)]] | [[m]]은 자연수 }가 있다. 집합 [[A]]의 원소 [[a]]에 대하여 집합 [[B]]의 원소 중 [[a]]의 약수의 "
              "최댓값을 [[M(a)]]라 하자. 예를 들어 [[M(3) = 3]], [[M(18) = 9]]이다. 수열 [[set(sub(a,n))]]을\n"
              "[[sub(a,n) = sum(k, 1, pow(3, n - 1), M(3k))]] ([[n]] = 1, 2, 3, ⋯)이라 할 때,\n"
              "[[lim(n, inf, frac(180 sub(a,n), (4n - 1) × pow(3, n)))]] 의 값은?"),
    choices=["[[20]]", "[[30]]", "[[40]]", "[[50]]", "[[60]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.85,
    note="a_n=3^{n−1}(2n+1) (a₁=3, a₂=15 확인) → 180·(1/3)·(1/2)=30 → ②. 빠른정답 15는 선지 범위 밖.")

# ───────────────────────── 접선의 방정식 ─────────────────────────
_TAN_Q = ("두 함수 [[f(x) = 2 ln(x) + {c}]], [[g(x) = a pow(x,2) + b]]의 그래프가 [[x = 1]]인 점에서 공통의 접선을 갖고 함수 [[h(x)]]를\n"
          "[[h(x)]] = {{ [[f(x)]] ([[x >= 1]]) ; [[g(x)]] ([[x < 1]]) }}\n"
          "이라 하자. 점 [[point(0, k)]]에서 곡선 [[y = h(x)]]에 그을 수 있는 접선의 개수를 [[i(k)]]라 할 때, 함수 [[i(x)(pow(x,2) + c x + d)]]가 실수 전체의 집합에서 "
          "연속이다. [[{ask}]]의 값은? (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)")
# p65
add(id="3e109ea1", qtype="choice",
    question=_TAN_Q.format(c=5, ask="frac(c d, a b)"),
    choices=["[[-21]]", "[[-18]]", "[[-15]]", "[[-12]]", "[[-9]]"],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.8, needs_review=PW,
    note="a=1, b=4; i(k)는 k=3, 4에서만 불연속(1→2→3→2→1) → x²+cx+d=(x−3)(x−4), c=−7, d=12 → cd/ab=−21 → ①. 빠른정답 4와 불일치.")

# p66
add(id="bad87dbc", qtype="choice",
    question=_TAN_Q.format(c=3, ask="a b + c d"),
    choices=["[[-8]]", "[[-6]]", "[[-4]]", "[[-2]]", "[[0]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85, needs_review=PW,
    note="a=1, b=2; 불연속점 k=1, 2 → c=−3, d=2 → ab+cd=2−6=−4 → ③ = 빠른정답 ✓.")

# ───────────────────────── 지수함수와 로그함수의 극한과 미분 ─────────────────────────
# p84 — [2023년 4월 고3 미적분 30번 변형]
add(id="06e3fb8e", qtype="short",
    question=("[[x >= 0]]에서 정의된 함수 [[f(x)]]가 다음 조건을 만족시킨다.\n"
              "(가) [[f(x)]] = { [[pow(2, x) - 1]] ([[0 <= x <= 1]]) ; [[4 × pow(frac(1,2), x) - 1]] ([[1 < x <= 2]]) }\n"
              "(나) 모든 양의 실수 [[x]]에 대하여 [[f(x + 2) = frac(1,2) f(x)]]이다.\n"
              "[[x > 0]]에서 정의된 함수 [[g(x)]]를 [[g(x) = lim(h, 0, frac(f(x + 6h) - f(x - 6h), h), +)]] 라 할 때, "
              "[[lim(t, 0, g(n - t) - g(n + t), +) - 8 g(n) = frac(3 ln(2), pow(2, 12))]] 를 만족시키는 모든 자연수 [[n]]의 값의 합을 구하시오."),
    choices=None, derived_answer="61", figure=None, difficulty_est=5, confidence=0.8, needs_review=PW,
    note="출처 [2023년 4월 고3 미적분 30번 변형]. g=6(f′₊+f′₋); n=2k+1: 48ln2/2^k, n=2k: 12ln2/2^k → n=33, 28 → 61(정확식 검증). 빠른정답 4와 불일치. 원문 중괄호 {g(n−t)−g(n+t)}는 lim 본체로.")

# ───────────────────────── 등비급수 ─────────────────────────
# p17 — [2024년 5월 고3 미적분 30번 변형]
add(id="4d69fc35", qtype="short",
    question=("수열 [[set(sub(a,n))]]은 공비가 0이 아닌 등비수열이고, 수열 [[set(sub(b,n))]]을 모든 자연수 [[n]]에 대하여\n"
              "[[sub(b,n)]] = { [[2 sub(a,n)]] ([[abs(sub(a,n)) < alpha]]) ; [[-frac(2, sub(a,n))]] ([[abs(sub(a,n)) >= alpha]]) } ([[alpha]]는 양의 상수)\n"
              "라 할 때, 두 수열 [[set(sub(a,n))]], [[set(sub(b,n))]]과 자연수 [[p]]가 다음 조건을 만족시킨다.\n"
              "(가) [[sum(n, 1, inf, sub(a,n)) = -6]]\n"
              "(나) [[sum(n, 1, m, frac(sub(a,n), sub(b,n)))]] 의 값이 최소가 되도록 하는 자연수 [[m]]은 [[p]]이고, "
              "[[sum(n, 1, p, sub(b,n)) = 42]], [[sum(n, p + 1, inf, sub(b,n)) = -frac(3,16)]] 이다.\n"
              "[[16 × (sub(a,4) + p)]]의 값을 구하시오."),
    choices=None, derived_answer="90", figure=None, difficulty_est=5, confidence=0.85, needs_review=PW,
    note="출처 [2024년 5월 고3 미적분 30번 변형]. r^p=1/64, Σ1/a_n=−21 → r/(1−r)²=2 → r=1/2, p=6, a=−3, a₄=−3/8 → 16(−3/8+6)=90 = 빠른정답 ✓.")

# p67 — [2006년 6월 고3 이과 16번]
add(id="73129095", qtype="choice",
    question=("그림과 같이 한 변의 길이가 [[a]]인 정사각형 O[[sub(B,1)]][[sub(C,1)]][[sub(A,0)]]이 있다. 삼각형 O[[sub(A,1)]][[sub(D,1)]]이 "
              "∠[[sub(D,1)]]O[[sub(A,1)]] = [[deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,1)]][[sub(C,1)]], [[sub(A,0)]][[sub(C,1)]] 위에 각각 점 [[sub(A,1)]], [[sub(D,1)]]을 잡고 "
              "변 O[[sub(A,1)]]의 길이를 [[sub(l,1)]]이라 하자.\n"
              "선분 O[[sub(A,1)]]을 한 변으로 하는 정사각형 O[[sub(B,2)]][[sub(C,2)]][[sub(A,1)]]에서 삼각형 O[[sub(A,2)]][[sub(D,2)]]가 "
              "∠[[sub(D,2)]]O[[sub(A,2)]] = [[deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,2)]][[sub(C,2)]], [[sub(A,1)]][[sub(C,2)]] 위에 각각 점 [[sub(A,2)]], [[sub(D,2)]]를 잡고 "
              "변 O[[sub(A,2)]]의 길이를 [[sub(l,2)]]라 하자.\n"
              "선분 O[[sub(A,2)]]를 한 변으로 하는 정사각형 O[[sub(B,3)]][[sub(C,3)]][[sub(A,2)]]에서 삼각형 O[[sub(A,3)]][[sub(D,3)]]이 "
              "∠[[sub(D,3)]]O[[sub(A,3)]] = [[deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,3)]][[sub(C,3)]], [[sub(A,2)]][[sub(C,3)]] 위에 각각 점 [[sub(A,3)]], [[sub(D,3)]]을 잡고 "
              "변 O[[sub(A,3)]]의 길이를 [[sub(l,3)]]이라 하자.\n"
              "이와 같은 과정을 계속하여 얻은 이등변삼각형 O[[sub(A,n)]][[sub(D,n)]]에서 변 O[[sub(A,n)]]의 길이를 [[sub(l,n)]] 이라 하자. "
              "[[sum(n, 1, inf, frac(1, sub(l,n))) = sqrt(3)]] 일 때, [[a]]의 값은?"),
    choices=["[[sqrt(3)]]", "[[1 + sqrt(3)]]", "[[2 + sqrt(3)]]", "[[3 + sqrt(3)]]", "[[6 + sqrt(3)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 OB₁C₁A₀ 안의 이등변삼각형 OA₁D₁(음영, ∠O=30°), OA₁을 한 변으로 하는 정사각형 OB₂C₂A₁과 삼각형 OA₂D₂(음영), 정사각형 OB₃C₃A₂와 삼각형 OA₃D₃(음영)이 O를 중심으로 회전하며 이어짐, 길이 a·l₁·l₂·l₃ 점선 호 표시, … 계속"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형·이등변삼각형 반복 도형 / 문법 범위 밖: 첨자 점 라벨(OB₁C₁A₀, ∠D₁OA₁ 등)은 텍스트 혼합",
    note="출처 [2006년 6월 고3 이과 16번]. l₁=a/cos30°=2a/√3, l_n=a(2/√3)^n → Σ1/l_n=(2√3+3)/a=√3 → a=2+√3 → ③ = 빠른정답 ✓.")

# p72
add(id="26213efc", qtype="short",
    question=("다음 그림과 같이 자연수 [[n]] 에 대하여 지름의 길이가 2인 원의 둘레를 [[4n]]등분하는 점을 시계 반대 방향으로 차례대로 "
              "[[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, 4n)]] 이라 하자. "
              "[[sub(S,n)]] = Σ_{[[i]] = 1}^{[[4n - 1]]} [[sub(P,1)]][[sub(P, i + 1)]]²이라 하면\n"
              "[[sum(m, 1, inf, pow(sum(n, 1, inf, frac(20, sub(S,n) sub(S, n + 1))), m - 1)) = frac(q, p)]] 일 때, [[p + q]] 의 값을 구하시오. "
              "(단, [[p]], [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="27",
    figure=[{"fn": "unsupported", "args": {"raw": "원 위에 4n등분점 P₁(위), P₂, P₃(왼쪽 위), …, P_{2n}, P_{2n+1}(아래), P_{2n+2}, …, P_{4n−1}, P_{4n}(오른쪽 위) 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원과 등분점 도형 / 문법 범위 밖: 첨자 점 라벨 선분 P₁P_{i+1}(윗줄)의 제곱은 텍스트 혼합(Σ 포함)",
    note="S_n=Σ|P₁P_j|²=2·4n=8n → Σ20/(8n·8(n+1))=5/16 → Σ(5/16)^{m−1}=16/11 → p+q=27 = 빠른정답 ✓. 원문 P₁P_{i+1} 위에 선분 기호(윗줄) 있음.")

# ───────────────────────── 삼각함수의 덧셈정리 ─────────────────────────
# p32
add(id="8a3f8157", qtype="short",
    question=("원점을 지나고 서로 수직인 두 직선 [[l]], [[m]]이 있다. 직선 [[l]]이 곡선 [[y = -frac(1,20) pow(x,2) + 5]]와 만나는 두 점을 A, B, "
              "직선 [[m]]이 곡선 [[y = -frac(1,20) pow(x,2) + 5]]와 만나는 두 점을 C, D라 하면 [[frac(seg(AB), seg(CD)) = frac(4,25)]] 이다. "
              "직선 [[l]]이 [[x]]축의 양의 방향과 이루는 각의 크기를 [[theta]]라 할 때, "
              "[[frac(1, sec(theta))(frac(1, csc(theta) + cot(theta)) + frac(1, csc(theta) - cot(theta)))]]의 값을 구하시오. (단, [[0 < theta < frac(pi,2)]])"),
    choices=None, derived_answer="5", figure=None, difficulty_est=3, confidence=0.9,
    note="기울기 k: AB=20(1+k²), CD=20(1+k²)/k² → k²=4/25, k=2/5; 식=cosθ·2cscθ=2cotθ=5 = 빠른정답 ✓.")

# p72 — [2008년 7월 고3 이과 미분과 적분 29번]
add(id="96818024", qtype="choice",
    question=("두 직선 [[y = x + a]], [[y = frac(1,3) x + b]]가 원 [[pow(x,2) + pow(y,2) = pow(r,2)]]에 접하는 점을 각각 [[sub(P,1)]], [[sub(P,2)]]라 하고 "
              "∠[[sub(P,1)]]O[[sub(P,2)]] = [[alpha]]일 때, [[tan(alpha)]]의 값은? (단, [[a < 0]], [[b < 0]])"),
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원 x²+y²=r²(중심 O), 제4사분면 쪽에서 접하는 두 직선 y=x+a, y=x/3+b, 접점 P₁·P₂, 각 α 표시"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 원과 두 접선 좌표평면 도형 / 문법 범위 밖: 첨자 점 라벨 ∠P₁OP₂는 텍스트 혼합",
    note="출처 [2008년 7월 고3 이과 미분과 적분 29번]. OP₁ 기울기 −1, OP₂ 기울기 −3 → tanα=|(−1+3)/(1+3)|=1/2 → ② = 빠른정답 ✓.")

# ───────────────────────── 여러 가지 함수의 적분 ─────────────────────────
# p33 — 변형 (2√x)
add(id="582840a2", qtype="choice",
    question=("실수 [[t]]에 대하여 곡선 [[y = pow(e, x)]] 위의 점 [[point(t, pow(e, t))]]에서의 접선의 방정식을 [[y = f(x)]]라 할 때, "
              "함수 [[y = abs(f(x) + k - 2 sqrt(x))]] 가 양의 실수 전체의 집합에서 미분가능하도록 하는 실수 [[k]]의 최솟값을 [[g(t)]]라 하자. "
              "두 실수 [[a]], [[b]] ([[a < b]])에 대하여 [[dinteg(a, b, g(t), t) = m]]이라 할 때, 보기에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[m < 0]]이 되도록 하는 두 실수 [[a]], [[b]] ([[a < b]])가 존재한다.\n"
              "ㄴ. 실수 [[c]]에 대하여 [[g(c) = 0]]이면 [[g(-c) = 0]]이다.\n"
              "ㄷ. [[a = alpha]], [[b = beta]] ([[alpha < beta]])일 때, [[m]]의 값이 최소이면 [[frac(prime(g)(beta) + pow(e, -beta), prime(g)(alpha)) > -e]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=5, confidence=0.8, needs_review=PR,
    note="g(t)=e^{−t}+e^t(t−1): ㄱ✓(0<t<c₁에서 음수), ㄴ✗(영점 0, c₁∈(0,1)만), ㄷ: α=0, β=c₁ → −βe^β>−e ✓ → ③ = 빠른정답 ✓.")

# p35 — [2019년 11월 고3 이과 21번/4점]
add(id="f5287f32", qtype="choice",
    question=("실수 [[t]]에 대하여 곡선 [[y = pow(e, x)]] 위의 점 [[point(t, pow(e, t))]]에서의 접선의 방정식을 [[y = f(x)]]라 할 때, "
              "함수 [[y = abs(f(x) + k - ln(x))]]가 양의 실수 전체의 집합에서 미분가능하도록 하는 실수 [[k]]의 최솟값을 [[g(t)]]라 하자. "
              "두 실수 [[a]], [[b]] ([[a < b]])에 대하여 [[dinteg(a, b, g(t), t) = m]]이라 할 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[m < 0]]이 되도록 하는 두 실수 [[a]], [[b]] ([[a < b]])가 존재한다.\n"
              "ㄴ. 실수 [[c]]에 대하여 [[g(c) = 0]]이면 [[g(-c) = 0]]이다.\n"
              "ㄷ. [[a = alpha]], [[b = beta]] ([[alpha < beta]])일 때 [[m]]의 값이 최소이면 [[frac(1 + prime(g)(beta), 1 + prime(g)(alpha)) < -pow(e,2)]]이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=5, confidence=0.85, needs_review=PR,
    note="출처 [2019년 11월 고3 이과 21번/4점]. g(t)=e^t(t−1)−t−1: ㄱ✓(g(0)=−2), ㄴ✓(g(−t)=e^{−t}g(t)), ㄷ✓(α=−β, 비=−e^{2β}<−e², β>1) → ⑤. 빠른정답 1과 불일치.")

# p56 — [2018년 4월 고3 이과 30번/4점]
add(id="fbe3cb02", qtype="short",
    question=("함수 [[f(x) = pow(e, x)(a pow(x,3) + b pow(x,2))]]과 양의 실수 [[t]]에 대하여 닫힌 구간 [[itv(-t, t, cc)]]에서 함수 [[f(x)]]의 최댓값을 [[M(t)]], "
              "최솟값을 [[m(t)]]라 할 때, 두 함수 [[M(t)]], [[m(t)]]는 다음 조건을 만족시킨다.\n"
              "(가) 모든 양의 실수 [[t]]에 대하여 [[M(t) = f(t)]]이다.\n"
              "(나) 양수 [[k]]에 대하여 닫힌 구간 [[itv(k, k + 2, cc)]]에 있는 임의의 실수 [[t]]에 대해서만 [[m(t) = f(-t)]]가 성립한다.\n"
              "(다) [[dinteg(1, 5, pow(e, t) × m(t), t) = frac(7,3) - 8e]]\n"
              "[[f(k + 1) = frac(q, p) pow(e, k + 1)]]일 때, [[p + q]]의 값을 구하시오. "
              "(단, [[a]]와 [[b]]는 0이 아닌 상수, [[p]]와 [[q]]는 서로소인 자연수이고, [[lim(x, inf, frac(pow(x,3), pow(e,x))) = 0]]이다.)"),
    choices=None, derived_answer="49", figure=None, difficulty_est=5, confidence=0.8,
    note="출처 [2018년 4월 고3 이과 30번/4점]. a,b>0, m(t)=f(−t) ⇔ b/a≤t≤|x₁| → k=b/a, x₁=−(k+2) → k=2, b=2a; (다) → a=1/4 → f(3)=(45/4)e³ → 49. 빠른정답 2와 불일치. 원문 중괄호 {e^t×m(t)}는 dinteg 안에서 생략.")

# p64 — [2018년 10월 고3 이과 30번 변형]
add(id="fdda64cc", qtype="short",
    question=("함수 [[f(x)]] = { [[-x - 2]] ([[x <= -2]]) ; [[sin(frac(pi,2) x)]] ([[-2 < x <= 2]]) ; [[x - 2]] ([[x > 2]]) }가 있다. "
              "실수 [[t]]에 대하여 부등식 [[f(x) <= f(t)]]를 만족시키는 실수 [[x]]의 최솟값을 [[g(t)]]라 하자. "
              "함수 [[g(t)]]가 [[t = a]]에서 미분가능하지 않은 모든 실수 [[a]]의 값을 작은 수부터 크기순으로 나열한 것을 "
              "[[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,n)]] ([[n]]은 자연수)라 할 때, [[n dinteg(sub(a,1), sub(a,n), g(t), t) = frac(p, pi) + q]]이다. "
              "[[20 abs(p + q)]] 의 값을 구하시오. (단, [[p]], [[q]]는 유리수이다.)"),
    choices=None, derived_answer="570",
    figure=[{"fn": "unsupported", "args": {"raw": "y=f(x)의 그래프: x≤−2에서 직선(x=−2에서 0), −2<x≤2에서 사인 곡선(x=−1에서 최소, x=1에서 최대, x=0·2에서 0), x>2에서 직선"}}],
    difficulty_est=5, confidence=0.8, needs_review=PW + " / 도형 표현 불가: 함수 그래프",
    note="출처 [2018년 10월 고3 이과 30번 변형]. g(t)=t(t≤−1), −2−t(−1≤t≤0), −2−sin(πt/2)(0≤t≤2), −t(t≥2) → 꺾임점 −1,0,2(n=3), 3∫_{−1}^{2}g=−33/2−12/π → 20|p+q|=570(수치 검증). 빠른정답 3과 불일치.")

# p78 — [2017년 11월 고3 이과 30번 변형]
add(id="90be9a31", qtype="short",
    question=("실수 [[t]]에 대하여 함수 [[f(x)]]를 [[f(x)]] = { [[1 - abs(x - t)]] ([[abs(x - t) <= 1]]) ; [[0]] ([[abs(x - t) > 1]]) } 이라 할 때, "
              "어떤 짝수 [[k]]에 대하여 함수 [[g(t) = dinteg(k + frac(1,2), k + frac(17,2), f(x) sin(pi x), x)]]가 다음 조건을 만족시킨다.\n"
              "함수 [[g(t)]]가 [[t = alpha]]에서 극대이고 [[g(alpha) > 0]]인 모든 [[alpha]]를 작은 수부터 크기순으로 나열한 것을 "
              "[[sub(alpha,1)]], [[sub(alpha,2)]], ⋯, [[sub(alpha,m)]] ([[m]]은 자연수)라 할 때, [[sum(i, 1, m, sub(alpha, i)) = frac(65,2)]] 이다.\n"
              "[[k + pow(pi, 2) sum(i, 1, m, g(sub(alpha, i)))]]의 값을 구하시오."),
    choices=None, derived_answer="18", figure=None, difficulty_est=5, confidence=0.8, needs_review=PW,
    note="출처 [2017년 11월 고3 이과 30번 변형]. k=0 기준 극대점 1/2, 5/2, 9/2, 13/2, 17/2 (m=5, g=2/π²,4/π²,4/π²,4/π²,2/π²; 수치 검증) → 5k+45/2=65/2 → k=2 → 2+16=18. 빠른정답 1과 불일치.")

# ───────────────────────── 정적분과 급수의 합 사이의 관계 ─────────────────────────
# p61
add(id="facbee4c", qtype="short",
    question=("다음 그림과 같은 원뿔에서 밑면의 지름의 양 끝 점을 A, B라 하자. 원뿔의 모선 OB를 [[n]]등분하는 [[n - 1]]개의 점을 잡고 점 O로부터 [[k]]번째의 점을 [[sub(C,k)]]라 하자. "
              "점 A에서 원뿔의 옆면을 따라 점 [[sub(C,k)]]까지 이르는 최단거리를 [[sub(l,k)]]라 할 때, [[lim(n, inf, sum(k, 1, n - 1, frac(pow(sub(l,k), 2), n)))]]의 값을 구하시오. "
              "(단, [[seg(AB) = 4]], [[seg(OA) = 6]])"),
    choices=None, derived_answer="30",
    figure=[{"fn": "unsupported", "args": {"raw": "원뿔(꼭짓점 O, 밑면 지름 AB), 모선 OB 위의 점 C_k, A에서 옆면을 따라 C_k에 이르는 곡선, 옆면 일부 음영"}}],
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 원뿔 입체 도형 / 첨자 점 라벨 C_k는 sub(C,k)",
    note="전개도 중심각 2π/3, ∠AOB=π/3 → l_k²=36+36(k/n)²−36(k/n) → ∫₀¹(36+36x²−36x)dx=30 = 빠른정답 ✓.")

# ───────────────────────── 삼각함수의 극한과 미분 ─────────────────────────
# p75 — [2020년 10월 고3 이과 21번/4점]
add(id="6ec05223", qtype="choice",
    question=("그림과 같이 길이가 2인 선분 AB를 지름으로 하는 반원이 있다. 호 AB 위의 점 P와 선분 AB 위의 점 C에 대하여 [[angle(PAC) = theta]]일 때, [[angle(APC) = 2 theta]]이다. "
              "[[angle(ADC) = angle(PCD) = frac(pi,2)]] 인 점 D에 대하여 두 선분 AP와 CD가 만나는 점을 E라 하자. "
              "삼각형 DEP의 넓이를 [[S(theta)]]라 할 때, [[lim(theta, 0, frac(S(theta), theta), +)]] 의 값은? (단, [[0 < theta < frac(pi,6)]])"),
    choices=["[[frac(5,9)]]", "[[frac(2,3)]]", "[[frac(7,9)]]", "[[frac(8,9)]]", "[[1]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "선분 AB를 지름으로 하는 반원, 호 위의 점 P, AB 위의 점 C(∠PCD 직각), D(∠ADC 직각), AP와 CD의 교점 E, 각 θ(A)·2θ(P) 표시, 삼각형 DEP 음영"}}],
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 반원·삼각형 복합 도형",
    note="출처 [2020년 10월 고3 이과 21번/4점]. 좌표 계산(수치 검증) S(θ)/θ → 8/9 → ④. 빠른정답 2와 불일치.")

# ───────────────────────── 방정식과 부등식에의 활용 ─────────────────────────
# p56 — [2026년 7월 고3 미적분 30번 변형]
add(id="14a43a06", qtype="short",
    question=("[[a > 0]], [[b > 0]]인 두 상수 [[a]], [[b]]에 대하여 실수 전체의 집합에서 미분가능한 함수 [[f(x)]]가 다음 조건을 만족시킨다.\n"
              "(가) 모든 실수 [[x]]에 대하여 [[pow(f(x), 3) + f(x) = frac(a, pow(x,2) + 3) - b x - frac(8,3) b]] 이다.\n"
              "(나) 함수 [[f(x)]]의 역함수가 존재하고, [[prime(f)(k) = 0]]인 실수 [[k]]가 존재한다.\n"
              "곡선 [[y = f(x)]]와 직선 [[y = -b x]]가 만나는 서로 다른 모든 점의 [[x]]좌표의 합이 [[k + 2]]일 때, [[a b = frac(q, p)]] 이다. "
              "[[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="19", figure=None, difficulty_est=5, confidence=0.8, needs_review=PR,
    note="출처 [2026년 7월 고3 미적분 30번 변형]. r(x)=a/(x²+3)−bx−8b/3 감소·r′(k)=0 → b=a/8, k=−1; 교점 x=0과 b²x(x²+3)=8/3의 실근 하나=1 → b²=2/3, ab=8b²=16/3 → 19. 빠른정답 86과 불일치. 원문 중괄호 {f(x)}³는 pow(f(x),3).")
