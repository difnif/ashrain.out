# -*- coding: utf-8 -*-
# esc_sonnet_h3-2_4of4 — 이미지 기준 전사 (53 항목 / 53쪽, 미적분). 모든 이미지가 id 1개씩.
# 표기 관행: 도함수 적용 f′(x)는 prime(f)(x)(파서는 곱으로 해석) → needs_review PR.
#            조각적 정의 { … (조건) ; … (조건) }는 텍스트 혼합 → needs_review PW.
#            첨자 점 라벨(P_k, A_k …)은 sub()로 텍스트 혼합, 선분 기호(윗줄)는 표기 불가 → needs_review PS.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

PR = "문법 범위 밖: 도함수 적용 표기 f′(x)를 prime(f)(x)로 전사(파서는 곱으로 해석)"
PW = "문법 범위 밖: 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사"
PS = "문법 범위 밖: 첨자 점 라벨(P_k 등)은 sub()로 텍스트 혼합 전사, 선분 기호(윗줄)는 표기 불가"
CH_G = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]

# ───────────────────────── 삼각함수의 덧셈정리 ─────────────────────────
# p90 — [2013년 11월 고2 이과 17번/4점]
add(id="a8562a8d", qtype="choice",
    question=("그림과 같이 원 [[pow(x,2) + pow(y,2) = 1]] 위의 점 A[[point(-1, 0)]]을 지나는 직선이 제1사분면에서 원과 만나는 점을 P, "
              "점 P에서의 접선이 [[x]]축과 만나는 점을 Q라 하자. 삼각형 POQ의 넓이가 [[frac(3,8)]]일 때, [[angle(PAO) = theta]]이다. "
              "[[tan(theta)]]의 값은? (단, 점 O는 원점이다.)"),
    choices=["[[frac(2,9)]]", "[[frac(sqrt(3),6)]]", "[[frac(1,3)]]", "[[frac(sqrt(6),6)]]", "[[frac(4,9)]]"],
    derived_answer="③",
    figure=U("좌표평면: 단위원 x²+y²=1, 점 A(−1,0)·원점 O·제1사분면의 점 P·x축 위의 점 Q, 직선 AP, P에서의 접선, 삼각형 POQ 음영, ∠PAO=θ 표시"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 좌표평면 위 원+직선+접선+삼각형 복합 도형",
    note="출처 [2013년 11월 고2 이과 17번/4점]. ∠POQ=2θ, 넓이 (1/2)tan2θ=3/8 → tan2θ=3/4 → tanθ=1/3 → ③ = 빠른정답 ✓.")

# p91 — [2015년 7월 고3 이과 20번/4점]
add(id="64b86a4d", qtype="choice",
    question=("그림과 같이 반지름의 길이가 6이고 중심각의 크기가 [[frac(pi,2)]]인 부채꼴 OAB가 있다. [[angle(COA) = theta]] ([[0 < theta < frac(pi,4)]])가 "
              "되도록 호 AB 위의 점 C를 잡고, 점 C에서의 접선이 변 OA의 연장선, 변 OB의 연장선과 만나는 점을 각각 P, Q라 하자. "
              "[[seg(PQ) = 15]]일 때, [[tan(2 theta)]]의 값은?"),
    choices=["[[frac(4,3)]]", "[[frac(3,2)]]", "[[frac(5,3)]]", "[[frac(11,6)]]", "[[2]]"],
    derived_answer="①",
    figure=U("부채꼴 OAB(반지름 6, 중심각 π/2, OA 가로·OB 세로), 호 위의 점 C, C에서의 접선이 OA·OB의 연장선과 만나는 점 P·Q, ∠COA=θ 표시, 직각삼각형 OPQ"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 부채꼴+접선+삼각형 복합 도형",
    note="출처 [2015년 7월 고3 이과 20번/4점]. PQ=6(tanθ+cotθ)=12/sin2θ=15 → sin2θ=4/5, cos2θ=3/5 → tan2θ=4/3 → ① = 빠른정답 ✓.")

# p95 — [2010년 6월 고3 이과 미분과 적분 28번]
add(id="43d4f2f1", qtype="choice",
    question=("좌표평면에서 원점 O를 중심으로 하고 반지름의 길이가 각각 1, [[sqrt(2)]]인 두 원 [[sub(C,1)]], [[sub(C,2)]]가 있다. "
              "직선 [[y = frac(1,2)]]이 원 [[sub(C,1)]], [[sub(C,2)]]와 제 1사분면에서 만나는 점을 각각 P, Q라고 하자. "
              "점 A[[point(sqrt(2), 0)]]에 대하여 [[angle(QOP) = alpha]], [[angle(AOQ) = beta]]라고 할 때, [[sin(alpha - beta)]]의 값은?"),
    choices=["[[frac(3 - sqrt(14), 8)]]", "[[frac(sqrt(7) - sqrt(14), 8)]]", "[[frac(sqrt(6) - sqrt(14), 8)]]",
             "[[frac(3 - sqrt(21), 8)]]", "[[frac(sqrt(7) - sqrt(21), 8)]]"],
    derived_answer="④",
    figure=U("좌표평면 제1사분면: 원점 중심의 두 사분원 C₁(반지름 1), C₂(반지름 √2), 직선 y=1/2와의 교점 P(C₁)·Q(C₂), x축 위의 점 A, ∠QOP=α, ∠AOQ=β 표시"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 좌표평면 위 두 원+직선+각 표시 도형",
    note="출처 [2010년 6월 고3 이과 미분과 적분 28번]. α+β=π/6, sinβ=√2/4, cosβ=√14/4 → sin(α−β)=sin(π/6−2β)=(3−√21)/8 → ④. 빠른정답 5와 불일치.")

# p97 — [2017년 9월 고3 이과 15번 변형]
add(id="1c5a0f91", qtype="choice",
    question=("곡선 [[y = 2 - pow(x,2)]] ([[0 < x < sqrt(2)]]) 위의 점 P에서 [[y]]축에 내린 수선의 발을 H라 하고, 원점 O와 점 A[[point(0, 2)]]에 대하여 "
              "[[angle(APH) = sub(theta,1)]], [[angle(HPO) = sub(theta,2)]]라 하자. [[tan(sub(theta,1)) = frac(4,3)]]일 때, "
              "[[tan(sub(theta,1) + sub(theta,2))]]의 값은?"),
    choices=["[[frac(25,14)]]", "[[frac(27,14)]]", "[[2]]", "[[frac(15,7)]]", "[[frac(17,7)]]"],
    derived_answer="②",
    figure=U("좌표평면: 곡선 y=2−x², y축 위의 점 A(0,2)·H, 곡선 위의 점 P, 선분 AP·OP·PH(점선), ∠APH=θ₁, ∠HPO=θ₂ 표시"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 좌표평면 위 곡선+삼각형+각 표시 도형",
    note="출처 [2017년 9월 고3 이과 15번 변형]. P(t, 2−t²): tanθ₁=t=4/3, tanθ₂=(2−t²)/t=1/6 → tan(θ₁+θ₂)=27/14 → ② = 빠른정답 ✓.")

# ───────────────────────── 여러 가지 함수의 적분 ─────────────────────────
# p2 — [2019년 10월 고3 이과 17번/4점]
add(id="a6825c71", qtype="choice",
    question=("실수 전체의 집합에서 미분가능한 함수 [[f(x)]]가 다음 조건을 만족시킨다.\n"
              "(가) [[x > 0]]일 때 [[f(x) = a x pow(e, 2x) + b pow(x,2)]]\n"
              "(나) [[sub(x,1) < sub(x,2) < 0]]인 임의의 두 실수 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[f(sub(x,2)) - f(sub(x,1)) = 3 sub(x,2) - 3 sub(x,1)]]\n"
              "[[f(frac(1,2)) = 2e]]일 때, [[prime(f)(frac(1,2))]]의 값은? (단, [[a]], [[b]]는 상수이다.)"),
    choices=["[[2e]]", "[[4e]]", "[[6e]]", "[[8e]]", "[[10e]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85, needs_review=PR,
    note="출처 [2019년 10월 고3 이과 17번/4점]. x<0에서 f′=3, x=0 미분가능 → a=3; f(1/2)=2e → b=2e; f′(1/2)=6e+2e=8e → ④ = 빠른정답 ✓.")

# p15 — [2016년 3월 고3 이과 7번/3점]
add(id="4c956d62", qtype="choice",
    question=("함수 [[f(x)]]가 모든 실수에서 연속일 때, 도함수 [[prime(f)(x)]]가 [[prime(f)(x)]] = { [[pow(e, x - 1)]] ([[x <= 1]]) ; [[frac(1,x)]] ([[x > 1]]) }이다.\n"
              "[[f(-1) = e + frac(1, pow(e,2))]]일 때, [[f(e)]]의 값은?"),
    choices=["[[e - 2]]", "[[e - 1]]", "[[e]]", "[[e + 1]]", "[[e + 2]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.8, needs_review=PR + " / " + PW,
    note="출처 [2016년 3월 고3 이과 7번/3점]. x≤1: f=e^{x−1}+e, f(1)=1+e; x>1: f=ln x+1+e → f(e)=e+2 → ⑤. 빠른정답 4와 불일치.")

# p34 — 출처 머리말 없음
add(id="63c335ae", qtype="choice",
    question=("삼차함수 [[y = f(x)]]의 그래프가 아래 그림과 같고, [[f(x)]]는 [[dinteg(a, b, f(x), x) = 2]], [[dinteg(a, c, f(x), x) = 0]]을 만족한다.\n"
              "함수 [[f(x)]]의 한 부정적분을 [[F(x)]]라 할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[F(b) = F(a) + 2]]\n"
              "ㄴ. 점 [[point(c, F(c))]]는 곡선 [[y = F(x)]]의 변곡점이다.\n"
              "ㄷ. [[-2 < F(a) < 0]]이면 방정식 [[F(x) = 0]]은 서로 다른 네 실근을 갖는다."),
    choices=CH_G, derived_answer="③",
    figure=U("삼차함수 y=f(x)의 그래프: 원점 O 오른쪽의 a<b<c에서 x축과 만나고, a~b 구간은 x축 위, b~c 구간은 x축 아래, c 이후 위로 증가(x<a에서는 아래)"),
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 삼차함수 그래프",
    note="ㄱ ✓, ㄴ F″(c)=f′(c)≠0이므로 변곡점 아님 ✗, ㄷ F(a)<0, F(b)=F(a)+2>0, F(c)=F(a)<0 → 네 실근 ✓ → ③. 빠른정답 2와 불일치.")

# p37 — [2010년 11월 고3 이과 미분과 적분 29번]
add(id="cdcef23a", qtype="choice",
    question=("실수 전체의 집합에서 미분가능하고, 다음 조건을 만족시키는 모든 함수 [[f(x)]]에 대하여 [[dinteg(0, 2, f(x), x)]]의 최솟값은?\n"
              "(가) [[f(0) = 1]], [[prime(f)(0) = 1]]\n"
              "(나) [[0 < a < b < 2]]이면 [[prime(f)(a) <= prime(f)(b)]]이다.\n"
              "(다) 구간 [[itv(0, 1, oo)]]에서 [[prime(f, 2)(x) = pow(e, x)]]이다."),
    choices=["[[frac(1,2) e - 1]]", "[[frac(3,2) e - 1]]", "[[frac(5,2) e - 1]]", "[[frac(7,2) e - 2]]", "[[frac(9,2) e - 2]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85, needs_review=PR,
    note="출처 [2010년 11월 고3 이과 미분과 적분 29번]. (0,1)에서 f=eˣ, [1,2]에서 f′≥e로 최소일 때 f=ex → (e−1)+3e/2 = 5e/2−1 → ③ = 빠른정답 ✓.")

# p72 — [2017년 4월 고3 이과 20번/4점]
add(id="f1e392d8", qtype="choice",
    question=("그림과 같이 세 점 A[[point(1, 1)]], B[[point(4, 1)]], C[[point(4, 5)]]를 꼭짓점으로 하는 삼각형 ABC가 있다. "
              "점 P는 점 A를 출발하여 삼각형 ABC의 변을 따라 점 B를 지나 점 C까지 매초 1의 일정한 속력으로 움직이고 "
              "이차함수 [[f(x) = k pow(x,2)]]의 그래프가 점 P를 지난다. [[t]]초 후 곡선 [[y = f(x)]] 위의 점 P에서의 접선의 기울기를 [[g(t)]]라 하자. "
              "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n(단, 점 P는 한 번 지나간 점은 다시 지나가지 않는다.)\n<보기>\n"
              "ㄱ. [[0 <= t < 3]]일 때 점 P의 좌표는 [[point(t + 1, 1)]]\n"
              "ㄴ. [[g(t) = frac(2, t + 1)]] ([[0 <= t < 3]])\n"
              "ㄷ. [[dinteg(0, 7, g(t), t) = 6 + 4 ln(2)]]"),
    choices=CH_G, derived_answer="⑤",
    figure=U("좌표평면: 포물선 f(x)=kx², 삼각형 ABC(A(1,1), B(4,1), C(4,5)), 변 AB 위의 점 P와 오른쪽 이동 화살표"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 좌표평면 위 포물선+삼각형 도형",
    note="출처 [2017년 4월 고3 이과 20번/4점]. ㄱ ✓, ㄴ k=1/(t+1)² → g=2/(t+1) ✓, ㄷ ∫₀³ 2/(t+1)dt + ∫₃⁷ (t−2)/2 dt = 4ln2+6 ✓ → ⑤ = 빠른정답 ✓.")

# ───────────────────────── 정적분과 급수의 합 사이의 관계 ─────────────────────────
# p5 — 구분구적법(정사각뿔), 출처 머리말 없음
add(id="433bbcd9", qtype="choice",
    question=("다음은 밑면의 한 변의 길이가 [[a]], 높이가 [[h]]인 정사각뿔의 부피 [[V]]를 구분구적법을 이용하여 구하는 과정이다.\n"
              "아래 그림과 같이 정사각뿔의 높이를 [[n]]등분하여 각 분점을 지나고 밑면에 평행한 평면으로 정사각뿔을 자른 단면의 한 변의 길이는 위에서부터 차례대로 "
              "[[frac(a,n)]], [[frac(2a,n)]], [[frac(3a,n)]], ⋯, [[frac((n - 1) a, n)]] 이다.\n"
              "이때 [[(n - 1)]]개의 정사각기둥의 부피의 합을 [[sub(V,n)]]이라 하면 각 사각기둥의 높이는 (가) 이므로\n"
              "[[sub(V,n) = frac(pow(a,2) h, pow(n,3))]] × ((나))\n"
              "따라서 구하는 부피 [[V]]는\n[[V = lim(n, inf, sub(V,n)) = frac(1,3) pow(a,2) h]]\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 차례대로 나열한 것은?"),
    choices=["[[frac(a,n)]], [[sum(k, 1, n - 1, pow(k,2))]]", "[[frac(h,n)]], [[sum(k, 1, n - 1, pow(k,2))]]",
             "[[frac(a,n)]], [[sum(k, 1, n, pow(k,2))]]", "[[frac(h,n)]], [[sum(k, 1, n, pow(k,2))]]",
             "[[frac(a,n)]], [[sum(k, 1, n - 1, pow(k,3))]]"],
    derived_answer="②",
    figure=U("정사각뿔(밑면 한 변 a, 높이 h)을 높이 n등분한 평면으로 잘라 그 단면을 밑면으로 쌓아 올린 (n−1)개의 정사각기둥 입체 그림, h·a 치수 표시"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 정사각뿔을 등분해 쌓은 사각기둥 입체 그림",
    note="(가) h/n, (나) Σ_{k=1}^{n−1}k² → ②. 빠른정답 9(선지 번호 아님)와 불일치. 원문 'a²h/n³ · (나)'의 '·'는 ×로.")

# p6 — 구분구적법(y=x², [0,2]), 출처 머리말 없음
add(id="fb80dd71", qtype="choice",
    question=("다음은 곡선 [[y = pow(x,2)]]과 [[x]]축 및 직선 [[x = 2]]로 둘러싸인 부분의 넓이를 구분구적법을 이용하여 구하는 과정이다. □ 안에 알맞은 식은?\n"
              "닫힌 구간 [[itv(0, 2, cc)]]를 [[n]]등분하면 양 끝점을 포함한 각 분점의 [[x]]좌표는 각각 "
              "0, [[frac(2,n)]], [[frac(4,n)]], ⋯, [[frac(2(n - 1), n)]], [[frac(2n, n)]] (= 2)이고 "
              "다음 그림의 색칠한 직사각형의 넓이의 합을 [[sub(S,n)]]이라 하면 구하는 넓이 [[S]]는\n"
              "[[S = lim(n, inf, sub(S,n))]] = lim_{[[n]]→∞} □ = [[frac(8,3)]]"),
    choices=["[[sum(k, 0, n - 1, frac(4k, n))]]", "[[sum(k, 0, n - 1, frac(4 pow(k,2), pow(n,2)))]]",
             "[[sum(k, 0, n - 1, frac(8 pow(k,2), pow(n,2)))]]", "[[sum(k, 0, n - 1, frac(8 pow(k,2), pow(n,3)))]]",
             "[[sum(k, 0, n - 1, frac(8 pow(k,3), pow(n,3)))]]"],
    derived_answer="④",
    figure=U("곡선 y=x²와 [0,2]를 n등분한 분점 2/n, 4/n, 6/n, 8/n, 10/n, …, 2(n−1)/n, 2n/n(=2) 위에 세운 색칠한 직사각형들(높이는 왼쪽 끝점의 함숫값), y=4 점선 표시"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+구분구적 직사각형 도형 / 문법 범위 밖: 빈칸 □가 든 극한식은 텍스트 혼합",
    note="Σ_{k=0}^{n−1}(2k/n)²·(2/n)=Σ8k²/n³ → 8/3 → ④(극한이 8/3이 되는 유일한 선지). 빠른정답 1과 불일치.")

# p7 — 구분구적법(y=2x³, [0,1]), 출처 머리말 없음
add(id="ec8e0b06", qtype="choice",
    question=("다음은 곡선 [[y = 2 pow(x,3)]]과 [[x]]축 및 직선 [[x = 1]]로 둘러싸인 도형의 넓이 [[S]]를 구분구적법을 이용하여 구하는 과정이다.\n"
              "다음 그림과 같이 닫힌 구간 [[itv(0, 1, cc)]]을 [[n]]등분하면 양 끝 점과 각 분점의 [[x]]좌표는 "
              "0, [[frac(1,n)]], [[frac(2,n)]], ⋯, [[frac(n - 1, n)]], 1이므로 직사각형의 넓이의 합을 [[sub(S,n)]]이라 하면\n"
              "[[sub(S,n)]] = (가)\n따라서 구하는 넓이 [[S]]는\n"
              "[[S = lim(n, inf, sub(S,n))]] = lim_{[[n]]→∞} (가) = (나)\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 차례대로 나열한 것은?"),
    choices=["[[sum(k, 1, n, frac(2 pow(k,3), pow(n,4)))]], [[frac(1,4)]]", "[[sum(k, 1, n, frac(2 pow(k,3), pow(n,4)))]], [[frac(1,2)]]",
             "[[sum(k, 1, n, frac(2 pow(k,3), pow(n,4)))]], [[1]]", "[[sum(k, 1, n, frac(2 pow(k,3), pow(n,3)))]], [[frac(1,4)]]",
             "[[sum(k, 1, n, frac(2 pow(k,3), pow(n,3)))]], [[frac(1,2)]]"],
    derived_answer="②",
    figure=U("곡선 y=2x³와 [0,1]을 n등분한 분점 1/n, 2/n, 3/n, …, (n−1)/n, n/n(=1) 위의 색칠한 직사각형들(높이는 오른쪽 끝점의 함숫값), y=2 점선 표시"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+구분구적 직사각형 도형",
    note="S_n=Σ2(k/n)³(1/n)=Σ2k³/n⁴ → 1/2 → ② = 빠른정답 ✓.")

# p39 — 출처 머리말 없음
add(id="66e9c693", qtype="choice",
    question=("함수 [[f(x) = frac(1,x)]]이 있다. 2 이상의 자연수 [[n]]에 대하여 닫힌구간 [[itv(1, 5, cc)]]을 [[n]]등분한 각 분점(양 끝점도 포함)을 차례대로 "
              "[[1 = sub(x,0)]], [[sub(x,1)]], [[sub(x,2)]], ⋯, [[sub(x, n - 1)]], [[sub(x,n) = 5]]라고 하자. "
              "세 점 [[point(1, 0)]], [[point(sub(x,k), 0)]], [[point(sub(x,k), f(sub(x,k)))]]를 꼭짓점으로 하는 삼각형의 넓이를 [[S(k)]] "
              "([[k]] = 1, 2, 3, ⋯, [[n]])라고 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n, S(k)))]]의 값은?"),
    choices=["[[frac(4 + ln(5), 4)]]", "[[frac(4 + ln(5), 8)]]", "[[frac(ln(5) - 4, 8)]]", "[[frac(4 - ln(5), 4)]]", "[[frac(4 - ln(5), 8)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="S(k)=(1/2)(x_k−1)/x_k, Δx=4/n → (1/4)∫₁⁵ (1/2)(1−1/x)dx = (4−ln5)/8 → ⑤. 빠른정답 4와 불일치.")

# p40 — [2006년 9월 고3 이과 12번]
add(id="6ea1669c", qtype="choice",
    question=("함수 [[f(x) = pow(x,2)]]에 대하여 그림과 같이 구간 [[itv(0, 1, cc)]]을 [[2n]]등분한 후, 구간 [[itv(frac(k - 1, 2n), frac(k, 2n), cc)]]를 밑변으로 하고 "
              "높이가 [[f(frac(k, 2n))]]인 직사각형의 넓이를 [[sub(S,k)]]라 하자.\n(단, [[n]]은 자연수이고 [[k]] = 1, 2, 3, ⋯, [[2n]]이다.)\n"
              "<보기>에서 옳은 것을 모두 고른 것은?\n<보기>\n"
              "ㄱ. [[lim(n, inf, sum(k, 1, n, sub(S,k))) = dinteg(0, frac(1,2), pow(x,2), x)]]\n"
              "ㄴ. [[lim(n, inf, sum(k, 1, n, (sub(S, 2k) - sub(S, 2k - 1)))) = 0]]\n"
              "ㄷ. [[lim(n, inf, sum(k, 1, n, sub(S, 2k))) = frac(1,2) dinteg(0, 1, pow(x,2), x)]]"),
    choices=CH_G, derived_answer="⑤",
    figure=U("곡선 f(x)=x² 위 [0,1]을 2n등분한 직사각형 S₁, S₂, …, S₆, …, S_{2n−1}, S_{2n}(홀수 번째 흰색·짝수 번째 음영), 분점 1/2n, 2/2n, …, (2n−2)/2n, (2n−1)/2n, 1 표시"),
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 함수 그래프+구분구적 직사각형 도형",
    note="출처 [2006년 9월 고3 이과 12번]. ㄱ ✓, ㄴ Σ차 = (1/2n)Σ(4k−1)/(4n²) → 0 ✓, ㄷ S_{2k}=(1/2)(1/n)f(k/n) ✓ → ⑤. 빠른정답 2와 불일치.")

# p42 — [2014년 4월 고3 이과 28번/4점]
add(id="8bc42ce6", qtype="short",
    question=("그림과 같이 곡선 [[y = -pow(x,2) + 1]] 위에 세 점 A[[point(-1, 0)]], B[[point(1, 0)]], C[[point(0, 1)]]이 있다. "
              "2 이상의 자연수 [[n]]에 대하여 선분 OC를 [[n]]등분할 때, 양 끝점을 포함한 각 분점을 차례로 "
              "O = [[sub(D,0)]], [[sub(D,1)]], [[sub(D,2)]], ⋯, [[sub(D, n - 1)]], [[sub(D,n)]] = C라 하자. "
              "직선 A[[sub(D,k)]]가 곡선과 만나는 점 중 A가 아닌 점을 [[sub(P,k)]]라 하고, 점 [[sub(P,k)]]에서 [[x]]축에 내린 수선의 발을 [[sub(Q,k)]]라 하자. "
              "([[k]] = 1, 2, ⋯, [[n]])\n삼각형 A[[sub(P,k)]][[sub(Q,k)]]의 넓이를 [[sub(S,k)]]라 할 때,\n"
              "[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(S,k))) = alpha]]\n이다. [[24 alpha]]의 값을 구하시오."),
    choices=None, derived_answer="11",
    figure=U("좌표평면: 포물선 y=−x²+1, A(−1,0)·B(1,0)·C(0,1)(=D_n), y축 위의 분점 D₁, D₂, …, D_k, …, D_{n−1}, 직선 AD_k와 곡선의 교점 P_k, 수선의 발 Q_k(직각 표시)"),
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 포물선+직선+수선 도형 / " + PS,
    note="출처 [2014년 4월 고3 이과 28번/4점]. P_k=(1−t, t(2−t)), S_k=(1/2)t(2−t)² (t=k/n) → α=∫₀¹(1/2)t(2−t)²dt=11/24 → 24α=11. 빠른정답 5와 불일치.")

# p43 — [2013년 6월 고3 이과 18번/4점]
add(id="43724bfa", qtype="choice",
    question=("함수 [[f(x) = pow(e, x)]]이 있다. 2 이상인 자연수 [[n]]에 대하여 닫힌 구간 [[itv(1, 2, cc)]]를 [[n]]등분한 각 분점(양 끝점도 포함)을 차례로 "
              "[[1 = sub(x,0)]], [[sub(x,1)]], [[sub(x,2)]], ⋯, [[sub(x, n - 1)]], [[sub(x,n) = 2]]라 하자. "
              "세 점 [[point(0, 0)]], [[point(sub(x,k), 0)]], [[point(sub(x,k), f(sub(x,k)))]]를 꼭짓점으로 하는 삼각형의 넓이를 [[sub(A,k)]] "
              "([[k]] = 1, 2, ⋯, [[n]])이라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n, sub(A,k)))]]의 값은?"),
    choices=["[[frac(1,2) pow(e,2) - e]]", "[[frac(1,2)(pow(e,2) - e)]]", "[[frac(1,2) pow(e,2)]]", "[[pow(e,2) - e]]", "[[pow(e,2) - frac(1,2) e]]"],
    derived_answer="③",
    figure=U("곡선 y=eˣ, 원점 O·(x_k,0)·(x_k, f(x_k))를 꼭짓점으로 하는 삼각형 A_k 음영, x₀=1·x_n=2 점선 표시, y절편 1"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+삼각형 도형",
    note="출처 [2013년 6월 고3 이과 18번/4점]. ∫₁² (1/2)x eˣ dx = (1/2)[(x−1)eˣ]₁² = e²/2 → ③. 빠른정답 5와 불일치.")

# p46 — 출처 머리말 없음
add(id="6ec71ce8", qtype="short",
    question=("그림과 같이 2 이상의 자연수 [[n]]에 대하여 곡선 [[y = sin(frac(x,2))]] 위의 점 [[sub(P,k)]][[point(frac(2k pi, n), sin(frac(k pi, n)))]] "
              "([[k]] = 1, 2, 3, ⋯, [[n]])에서의 접선이 [[y]]축과 만나는 점을 [[sub(Q,k)]]라 하고, "
              "점 [[sub(P,k)]] ([[k]] = 1, 2, 3, ⋯, [[n - 1]])에서 [[x]]축에 내린 수선의 발을 [[sub(R,k)]]라 하자. "
              "두 삼각형 O[[sub(P,k)]][[sub(Q,k)]], O[[sub(P,k)]][[sub(R,k)]]의 넓이를 각각 [[sub(S,k)]], [[sub(T,k)]]라 할 때, "
              "[[lim(n, inf, frac(1,n) sum(k, 1, n, (sub(S,k) - sub(T,k))))]]의 값을 구하시오. (단, [[sub(T,n) = 0]]이다.)"),
    choices=None, derived_answer="2",
    figure=U("곡선 y=sin(x/2)(0~2π 부근), 곡선 위의 점 P_k에서의 접선과 y축의 교점 Q_k, P_k에서 x축에 내린 수선의 발 R_k(직각 표시), 원점 O, 선분 OP_k, x축의 2π 표시"),
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 함수 그래프+접선+삼각형 도형 / " + PS,
    note="S_k−T_k=−(1/4)t²cos(t/2) (t=2kπ/n) → (1/2π)∫₀^{2π} −(1/4)t²cos(t/2)dt = 2. 빠른정답 3과 불일치.")

# p47 — 출처 머리말 없음
add(id="bbbc1fba", qtype="choice",
    question=("함수 [[f(x) = a pow(x,2) + b]] ([[a > 0]], [[b > 0]])이 있다. 자연수 [[n]]에 대하여 두 점 [[point(0, 0)]], [[point(4, 0)]]을 잇는 선분을 "
              "[[n]]등분한 각 분점 (양 끝점도 포함)을 차례대로 [[sub(P,0)]][[point(0, 0)]], [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P,n)]][[point(4, 0)]]이라 하자. "
              "점 [[sub(P,k)]] ([[k]] = 0, 1, 2, ⋯, [[n]])을 지나면서 [[x]]축에 수직인 직선과 곡선 [[y = f(x)]]의 교점을 [[sub(Q,k)]]라 하자.\n"
              "[[sub(l,k)]] = [[sub(P,k)]][[sub(Q,k)]]라 하면 [[sub(l,1) + sub(l,n) = frac(18 pow(n,2) + 16, pow(n,2))]]일 때,\n"
              "[[lim(n, inf, frac(4,n) sum(k, 1, n, sqrt(sub(l,k) - 1) pow(e, sub(l,k))))]]의 값은?"),
    choices=["[[frac(pow(e,16) - 1, 2)]]", "[[frac(pow(e,17) - e, 2)]]", "[[frac(pow(e,17) - 1, 2)]]", "[[frac(pow(e,16), 2)]]", "[[pow(e,17) + 1]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.8, needs_review=PS + " (l_k = P_kQ_k 위에 선분 기호)",
    note="l₁+l_n=16a/n²+16a+2b → a=1, b=1, f=x²+1 → ∫₀⁴ x e^{x²+1}dx = (e¹⁷−e)/2 → ② = 빠른정답 ✓.")

# p48 — 출처 머리말 없음
add(id="9cd31371", qtype="choice",
    question=("[[n]] 이하의 자연수 [[k]]에 대하여 [[sub(x,k) = frac(k,n)]]라 하자.\n함수 [[f(x) = pow(e, 3x) - pow(e, x) + 2e x]]에 대하여 "
              "곡선 [[y = f(x)]] 위의 점 [[sub(A,k)]][[point(sub(x,k), f(sub(x,k)))]]에서의 접선이 [[x]]축과 만나는 점을 [[sub(B,k)]]라 하고 "
              "점 [[sub(A,k)]]에서 [[x]]축에 내린 수선의 발을 [[sub(C,k)]]라 하자. "
              "[[lim(n, inf, frac(1,n) sum(k, 1, n, frac(pow(f(sub(x,k)), 3), sub(B,k) sub(C,k))))]]의 값은?\n(단, [[n]]은 자연수이다.)"),
    choices=["[[frac(pow(pow(e,4) - e, 4), 4)]]", "[[frac(pow(pow(e,3) - e, 3), 3)]]", "[[pow(e,3)]]",
             "[[frac(pow(pow(e,3) + e, 3), 3)]]", "[[frac(pow(pow(e,4) + e, 4), 4)]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PS + " (분모 B_kC_k는 선분 길이(윗줄)이나 sub(B,k) sub(C,k) 곱으로 전사, 분자 {f(x_k)}³의 중괄호는 pow로)",
    note="B_kC_k=f/f′ → 피적분 f²f′ → [f³/3]₀¹ = (e³+e)³/3 (f(0)=0, f(1)=e³+e) → ④. 빠른정답 3과 불일치.")

# p49 — 출처 머리말 없음
add(id="5d964b32", qtype="short",
    question=("그림과 같이 2 이상인 자연수 [[n]]에 대하여 닫힌 구간 [[itv(1, 2, cc)]]를 [[n]]등분한 각 분점(양 끝점도 포함)을 차례로\n"
              "[[1 = sub(x,0)]], [[sub(x,1)]], [[sub(x,2)]], ⋯, [[sub(x, n - 1)]], [[sub(x,n) = 2]]\n"
              "라 하자. 점 [[point(sub(x,k), 0)]] ([[k]] = 1, 2, 3, ⋯, [[n]])을 지나고 기울기가 [[-2]]인 직선이 곡선 [[y = pow(x,2) + 1]]과 "
              "제1사분면에서 만나는 점을 [[sub(A,k)]], [[y]]축과 만나는 점을 [[sub(B,k)]]라 하자. 삼각형 O[[sub(A,k)]][[sub(B,k)]]의 넓이를 [[sub(S,k)]]라 할 때,\n"
              "[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(S,k))) = p + q sqrt(2)]]\n이다. [[10(p + q)]]의 값을 구하시오.\n"
              "(단, [[O]]는 원점이고, [[p]], [[q]]는 유리수이다.)"),
    choices=None, derived_answer="13",
    figure=U("좌표평면: 곡선 y=x²+1, (x_k,0)을 지나는 기울기 −2인 직선, 곡선과의 교점 A_k, y축과의 교점 B_k, 삼각형 OA_kB_k 음영, x축의 1·x_k·2 점선 표시"),
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 곡선+직선+삼각형 도형 / " + PS,
    note="A_k의 x좌표 √(2t)−1, S=t(√(2t)−1) (t=x_k) → ∫₁² = 17/10−(2/5)√2 → p=17/10, q=−2/5 → 10(p+q)=13. 빠른정답 2와 불일치.")

# p50 — 출처 머리말 없음
add(id="60c3747c", qtype="choice",
    question=("다음 그림과 같이 곡선 [[y = x cos(x)]] ([[x >= 0]])와 직선 [[y = x]]가 접하는 점을 원점 O에 가까운 순서대로 "
              "[[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,n)]]이라 하자. 곡선 [[y = x cos(x)]] ([[x >= 0]])와 선분 [[sub(P, n - 1)]][[sub(P,n)]] "
              "([[n]]은 자연수)으로 둘러싸인 도형의 넓이를 [[sub(A,n)]]이라 할 때, [[lim(n, inf, frac(1, pow(n,2)) sum(k, 1, n, sub(A,k)))]]의 값은?\n"
              "(단, 원점 O는 [[sub(P,0)]]이라 하자.)"),
    choices=["[[pow(pi,2)]]", "[[2 pow(pi,2)]]", "[[3 pow(pi,2)]]", "[[4 pow(pi,2)]]", "[[5 pow(pi,2)]]"],
    derived_answer="②",
    figure=U("좌표평면: 곡선 y=x cos x와 직선 y=x, 접점 P₀(=O), P₁, P₂, 곡선과 선분 P₀P₁·P₁P₂로 둘러싸인 영역 A₁·A₂ 음영"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+직선+음영 영역 도형 / " + PS,
    note="접점 x=2kπ, A_n=∫(x−x cos x)dx = 2π²(2n−1), ΣA_k=2π²n² → 2π² → ② = 빠른정답 ✓.")

# p53 — 출처 머리말 없음
add(id="a5b5ddc0", qtype="choice",
    question=("함수 [[f(x) = pow(e, x)]]이 있다. 2 이상인 자연수 [[n]]에 대하여 닫힌 구간 [[itv(2, 4, cc)]]를 [[n]]등분한 각 분점(양 끝 점도 포함)을 차례로\n"
              "[[2 = sub(x,0)]], [[sub(x,1)]], [[sub(x,2)]], ⋯, [[sub(x, n - 1)]], [[sub(x,n) = 4]]\n"
              "라 하자. 세 점 [[point(0, 0)]], [[point(sub(x,k), 0)]], [[point(sub(x,k), f(sub(x,k)))]]를 꼭짓점으로 하는 삼각형의 넓이를 [[sub(A,k)]] "
              "([[k]] = 1, 2, ⋯, [[n]])이라 할 때,\n[[lim(n, inf, frac(2,n) sum(k, 1, n, sub(A,k)))]]의 값은?"),
    choices=["[[frac(1,2)(pow(e,4) - pow(e,2))]]", "[[frac(1,2) pow(e,4)]]", "[[frac(1,2)(3 pow(e,4) - pow(e,2))]]",
             "[[frac(3,2) pow(e,4)]]", "[[frac(1,2)(3 pow(e,4) + pow(e,2))]]"],
    derived_answer="③",
    figure=U("곡선 y=eˣ, 원점·(x_k,0)·(x_k, f(x_k))를 꼭짓점으로 하는 삼각형 A_k 음영, x₀=2·x_n=4 점선 표시, y절편 1"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+삼각형 도형",
    note="Δx=2/n → ∫₂⁴ (1/2)x eˣ dx = (1/2)[(x−1)eˣ]₂⁴ = (3e⁴−e²)/2 → ③. 빠른정답 2와 불일치.")

# p54 — 출처 머리말 없음
add(id="97a8448c", qtype="short",
    question=("다음 그림과 같이 길이가 8인 선분 AB를 지름으로 하는 반원의 호 AB를 [[n]]등분한 각 분점을 점 A에 가까운 것부터 차례대로 "
              "[[sub(P,k)]] ([[k]] = 1, 2, 3, ⋯, [[n - 1]])이라 한다.\n삼각형 AB[[sub(P,k)]]의 넓이를 [[sub(S,k)]]라 할 때, "
              "[[lim(n, inf, frac(pi,n) sum(k, 1, n - 1, sub(S,k)))]]의 값을 구하시오."),
    choices=None, derived_answer="32",
    figure=U("지름 AB=8(중심 O, AO=4 표시)인 반원, 호 위의 분점 P₁, P₂, …, P_k, …, P_{n−1}, 삼각형 ABP_k 음영"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 반원+분점+삼각형 도형 / " + PS,
    note="S_k=(1/2)·8·4sin(kπ/n)=16sin(kπ/n) → 16∫₀^π sin x dx = 32. 빠른정답 4와 불일치.")

# p55 — 출처 머리말 없음
add(id="67cad6ab", qtype="choice",
    question=("함수 [[f(x) = pow(e, 2x)]]이 있다. 2 이상인 자연수 [[n]]에 대하여 닫힌 구간 [[itv(1, 2, cc)]]을 [[n]]등분한 각 분점(양 끝 점도 포함)을 차례로\n"
              "[[1 = sub(x,0)]], [[sub(x,1)]], [[sub(x,2)]], ⋯, [[sub(x, n - 1)]], [[sub(x,n) = 2]]\n"
              "라 하자. 세 점 [[point(0, 0)]], [[point(sub(x,k), 0)]], [[point(sub(x,k), f(sub(x,k)))]]를 꼭짓점으로 하는 삼각형의 넓이를 [[sub(A,k)]] "
              "([[k]] = 1, 2, ⋯, [[n]])이라 할 때,\n[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(A,k)))]]의 값은?"),
    choices=["[[frac(1,8) pow(e,4) - pow(e,2)]]", "[[frac(1,8) pow(e,4)]]", "[[frac(3,8)(pow(e,4) - pow(e,2))]]",
             "[[frac(3,8) pow(e,4) - frac(1,8) pow(e,2)]]", "[[frac(3,8) pow(e,4)]]"],
    derived_answer="④",
    figure=U("곡선 y=e^{2x}, 원점·(x_k,0)·(x_k, f(x_k))를 꼭짓점으로 하는 삼각형 A_k 음영, x₀=1·x_n=2 점선 표시, y절편 1"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+삼각형 도형",
    note="∫₁² (1/2)x e^{2x}dx = (1/2)[(x/2−1/4)e^{2x}]₁² = 3e⁴/8−e²/8 → ④ = 빠른정답 ✓.")

# p56 — 출처 머리말 없음
add(id="003cfc46", qtype="choice",
    question=("함수 [[f(x) = pow(e, frac(x,2))]]이 있다. 2 이상인 자연수 [[n]]에 대하여 닫힌 구간 [[itv(2, 4, cc)]]를 [[n]]등분한 각 분점(양 끝 점도 포함)을 차례로 "
              "[[2 = sub(x,0)]], [[sub(x,1)]], [[sub(x,2)]], ⋯, [[sub(x, n - 1)]], [[sub(x,n) = 4]]라 하자.\n"
              "세 점 [[point(0, 0)]], [[point(sub(x,k), 0)]], [[point(sub(x,k), f(sub(x,k)))]]를 꼭짓점으로 하는 삼각형의 넓이를 [[sub(A,k)]] "
              "([[k]] = 1, 2, ⋯, [[n]])이라 할 때,\n[[lim(n, inf, frac(2,n) sum(k, 1, n, sub(A,k)))]]의 값은?"),
    choices=["[[pow(e,2) - 4e]]", "[[pow(e,2)]]", "[[2 pow(e,2) - e]]", "[[2 pow(e,2)]]", "[[2(pow(e,2) + e)]]"],
    derived_answer="④",
    figure=U("곡선 y=e^{x/2}, 원점·(x_k,0)·(x_k, f(x_k))를 꼭짓점으로 하는 삼각형 A_k 음영, x₀=2·x_n=4 점선 표시, y절편 1"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+삼각형 도형",
    note="∫₂⁴ (1/2)x e^{x/2}dx = (1/2)[(2x−4)e^{x/2}]₂⁴ = 2e² → ④ = 빠른정답 ✓.")

# p57 — 출처 머리말 없음
add(id="2cc5ae4b", qtype="short",
    question=("다음 그림과 같이 [[x]]축 위의 닫힌 구간 [[itv(0, 2, cc)]]를 [[n]]등분한 점을 앞에서부터 차례대로 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A, n - 1)]]이라 하고, "
              "점 [[sub(A,k)]] ([[1 <= k <= n - 1]])을 지나고 [[y]]축에 평행한 직선이 곡선 [[y = pow(x,2)]]과 만나는 점을 [[sub(B,k)]]라 할 때, "
              "[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(A,k) sub(B,k)))]]의 값을 구하시오. (단, [[sub(A,n)]][[point(2, 0)]]이다.)"),
    choices=None, derived_answer="frac(4,3)",
    figure=U("좌표평면: 곡선 y=x², x축 위의 분점 A₁, A₂, A₃, …, A_{n−1}, A_n(x=2)과 곡선 위의 점 B₁, B₂, B₃, …, B_{n−1}, B_n(y=4 점선), 세로 선분 A_kB_k"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+세로 선분 도형 / " + PS + " (Σ 안의 A_kB_k는 선분 길이)",
    note="(1/n)Σ(2k/n)² → (1/2)∫₀² x²dx = 4/3 = 빠른정답 ✓.")

# p58 — 출처 머리말 없음
add(id="80a825e4", qtype="choice",
    question=("다음 그림과 같이 [[x]]축 위의 구간 [[itv(0, 3, cc)]]을 [[n]]등분한 점을 앞에서부터 차례대로 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A, n - 1)]]이라 하고, "
              "점 [[sub(A,k)]]를 지나고 [[y]]축에 평행한 직선이 곡선 [[y = pow(x,2)]]과 만나는 점을 [[sub(B,k)]]라 할 때, "
              "[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(A,k) sub(B,k)))]]의 값은?\n(단, 점 [[sub(A,n)]]의 좌표는 [[point(3, 0)]]이다.)"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="③",
    figure=U("좌표평면: 곡선 y=x², x축 위의 분점 A₁, A₂, A₃, …, A_{n−1}, A_n(x=3)과 곡선 위의 점 B₁, B₂, B₃, …, B_{n−1}, B_n(y=9 점선), 세로 선분 A_kB_k"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+세로 선분 도형 / " + PS + " (Σ 안의 A_kB_k는 선분 길이)",
    note="(1/n)Σ(3k/n)² → (1/3)∫₀³ x²dx = 3 → ③ = 빠른정답 ✓.")

# p59 — 출처 머리말 없음
add(id="d79354f7", qtype="choice",
    question=("다음 그림과 같이 [[x]]축 위의 구간 [[itv(2, 4, cc)]]를 [[n]]등분한 점을 앞에서부터 차례대로 [[sub(A,1)]], [[sub(A,2)]] [[sub(A,3)]], ⋯, [[sub(A, n - 1)]]이라 하고, "
              "점 [[sub(A,k)]]를 지나고 [[y]]축에 평행한 직선이 곡선 [[y = frac(1,4) pow(x,3) - 2]]와 만나는 점을 [[sub(B,k)]]라 할 때, "
              "[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(A,k) sub(B,k)))]]의 값은?\n(단, 점 [[sub(A,n)]]의 좌표는 [[point(4, 0)]]이다.)"),
    choices=["[[frac(9,2)]]", "[[5]]", "[[frac(11,2)]]", "[[6]]", "[[frac(13,2)]]"],
    derived_answer="③",
    figure=U("좌표평면: 곡선 y=(1/4)x³−2(y절편 −2), x축 위의 분점 A₁, A₂, A₃, …, A_{n−1}, A_n(x=4)과 곡선 위의 점 B₁, B₂, B₃, …(y=14 점선), 세로 선분, x=2 표시"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 함수 그래프+세로 선분 도형 / " + PS + " (Σ 안의 A_kB_k는 선분 길이)",
    note="(1/2)∫₂⁴ (x³/4−2)dx = (1/2)(8+3) = 11/2 → ③ = 빠른정답 ✓. 원문 'A₁, A₂ A₃'(콤마 누락) 그대로 전사.")

# p60 — 출처 머리말 없음
add(id="303db9f3", qtype="choice",
    question=("다음 그림과 같이 좌표평면에서 두 점 A[[point(-1, 0)]], B[[point(1, 0)]]을 지름의 양 끝으로 하는 원 [[pow(x,2) + pow(y,2) = 1]]의 호 AB를 "
              "[[n]]등분하는 점을 [[sub(P,k)]] ([[k]] = 1, 2, 3, ⋯, [[n - 1]])이라 한다. 삼각형 A[[sub(P,k)]]B의 넓이를 [[sub(S,k)]]라 할 때,\n"
              "[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(S,k)))]]의 값은?"),
    choices=["[[frac(1,pi)]]", "[[frac(2,pi)]]", "[[frac(3,pi)]]", "[[frac(4,pi)]]", "[[frac(5,pi)]]"],
    derived_answer="②",
    figure=U("좌표평면: 위쪽 반원 x²+y²=1, A(−1,0)·B(1,0)·원점 O, 호 위의 점 P_k, 삼각형 AP_kB 음영"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 좌표평면 위 반원+삼각형 도형 / " + PS,
    note="S_k=sin(kπ/n) → (1/π)∫₀^π sin x dx = 2/π → ② = 빠른정답 ✓.")

# p62 — 출처 머리말 없음
add(id="4d46fd70", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 6인 정사각형 ABCD가 있다. 선분 CD를 [[ratio(5, 1)]]로 내분하는 점을 E라 하고 2 이상의 자연수 [[n]]과 "
              "[[1 <= k <= n - 1]]인 자연수 [[k]]에 대하여 선분 BE를 [[ratio(k, (n - k))]]로 내분하는 점을 [[sub(P,k)]], [[sub(P,n)]] = E라 하자. "
              "삼각형 BC[[sub(P,k)]]의 넓이를 [[sub(S,k)]]라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n, pow(e, sub(S,k)))) = p pow(e,15) + q]]이다.\n"
              "두 유리수 [[p]], [[q]]에 대하여 [[60(p - q)]]의 값을 구하시오.\n(단, [[pow(e,15)]]은 무리수이다.)"),
    choices=None, derived_answer="8",
    figure=U("정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), 변 CD 위의 점 E, 선분 BE 위의 점 P_k, 삼각형 BCP_k 음영"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 정사각형+내분점+삼각형 도형 / " + PS,
    note="CE=5, S_k=(1/2)·6·(5k/n)=15k/n → ∫₀¹ e^{15x}dx = (e¹⁵−1)/15 → p=1/15, q=−1/15 → 60(p−q)=8. 빠른정답 3과 불일치.")

# p63 — 출처 머리말 없음
add(id="7b9aac7d", qtype="short",
    question=("다음 그림과 같이 중심각의 크기가 [[frac(pi,2)]]이고, 반지름의 길이가 6인 부채꼴 OAB가 있다. 2 이상의 자연수 [[n]]에 대하여 호 AB를 [[n]]등분한 각 분점을 "
              "점 A에서 가까운 것부터 순서대로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, n - 1)]]이라 하자.\n"
              "[[1 <= k <= n - 1]]인 자연수 [[k]]에 대하여 점 B에서 선분 O[[sub(P,k)]]에 내린 수선의 발을 [[sub(Q,k)]]라 하고, "
              "삼각형 O[[sub(Q,k)]]B의 넓이를 [[sub(S,k)]]라 하자.\n"
              "[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(S,k))) = frac(alpha, pi)]]일 때, 상수 [[alpha]]의 값을 구하시오."),
    choices=None, derived_answer="18",
    figure=U("부채꼴 OAB(반지름 6, OA 가로·OB 세로, 중심각 π/2), 호 위의 분점 P₁, P₂, P₃, …, P_k, …, P_{n−1}, B에서 OP_k에 내린 수선의 발 Q_k(직각 표시), 삼각형 OQ_kB 음영"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 부채꼴+수선+삼각형 도형 / " + PS,
    note="∠BOP_k=π/2−kπ/2n → S_k=(1/2)·36·sinθcosθ=9sin(kπ/n) → 9·(1/π)·2 = 18/π → α=18. 빠른정답 2와 불일치.")

# p65 — 출처 머리말 없음
add(id="91774f21", qtype="short",
    question=("한 변의 길이가 1인 정삼각형 ABC에서 변 BC를 [[n]]등분하여 차례로 점 [[sub(P,0)]](= B), [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, n - 1)]], [[sub(P,n)]](= C)를 정할 때,\n"
              "[[lim(n, inf, frac(1,n) sum(k, 1, n, pow(A sub(P,k), 2)))]]의 값을 구하시오."),
    choices=None, derived_answer="frac(5,6)",
    figure=U("정삼각형 ABC(한 변 1, 점선 표시), 변 BC 위의 분점 P₁, P₂, …, P_{n−1}, B(=P₀), C(=P_n)"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 정삼각형+분점 도형 / " + PS + " (Σ 안의 AP_k²은 선분 길이의 제곱)",
    note="AP²=x²−x+1 (BP=x) → ∫₀¹(x²−x+1)dx = 5/6 = 빠른정답 ✓.")

# p66 — 출처 머리말 없음
add(id="576909b3", qtype="choice",
    question=("다음 그림과 같이 반지름의 길이가 1인 사분원의 호 AB를 5등분하는 점을 각각 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], [[sub(P,4)]]라 하자. "
              "이와 같은 방법으로 사분원의 둘레를 [[n]]등분하여 각 분점을 [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, n - 1)]]라 하고 "
              "점 [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, n - 1)]]에서 반지름 OA에 내린 수선의 발을 각각 [[sub(Q,1)]], [[sub(Q,2)]], ⋯, [[sub(Q, n - 1)]]라 하자. "
              "[[f(n) = sum(k, 1, n - 1, pow(O sub(Q,k), 2))]]이라 할 때, [[lim(n, inf, frac(f(n), n))]]의 값은?"),
    choices=["[[-2]]", "[[-frac(1,2)]]", "[[0]]", "[[frac(1,2)]]", "[[2]]"],
    derived_answer="④",
    figure=U("사분원 OAB(반지름 1, OB 세로·OA 가로), 호 위의 점 P₁, P₂, P₃, P₄와 OA에 내린 수선의 발 Q₁, Q₂, Q₃, Q₄(직각 표시)"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 사분원+수선 도형 / " + PS + " (Σ 안의 OQ_k²은 선분 길이의 제곱)",
    note="OQ_k=sin(kπ/2n) → (2/π)∫₀^{π/2} sin²x dx = 1/2 → ④ = 빠른정답 ✓.")

# p67 — 출처 머리말 없음
add(id="8df80d3c", qtype="choice",
    question=("그림과 같이 한 변의 길이가 1인 정삼각형 OAB가 있다. 2 이상의 자연수 [[n]]과 [[1 <= k < n]]인 자연수 [[k]]에 대하여 선분 AB를 [[ratio(k, (n - k))]]로 내분하는 점을 [[sub(P,k)]]라 하자.\n"
              "[[sub(l,k) = pow(O sub(P,k), 2) - pow(A sub(P,k), 2)]]이라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n - 1, pow(2, sub(l,k))))]]의 값은?"),
    choices=["[[frac(1, ln(2))]]", "[[frac(2, ln(2))]]", "[[frac(3, ln(2))]]", "[[frac(4, ln(2))]]", "[[frac(5, ln(2))]]"],
    derived_answer="①",
    figure=U("정삼각형 OAB(O 왼쪽 아래, A 오른쪽 아래, B 위), 변 AB 위의 점 P₁, P₂, P₃, …, P_k, …, P_{n−1}, 선분 OP_k"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 정삼각형+내분점 도형 / " + PS + " (OP_k², AP_k²은 선분 길이의 제곱)",
    note="AP=x=k/n, OP²=1−x+x² → l=1−x → ∫₀¹ 2^{1−x}dx = 1/ln2 → ① = 빠른정답 ✓.")

# p74 — 출처 머리말 없음
add(id="01d47f62", qtype="choice",
    question=("[[seg(AB) = 2]], [[seg(BC) = 1]], [[angle(B) = deg(90)]]인 직각삼각형 ABC의 변 AB를 [[n]]등분한 점을 다음 그림과 같이 점 A에서 가까운 순서대로 "
              "[[sub(B,1)]], [[sub(B,2)]], ⋯, [[sub(B, n - 1)]]이라 하고, 각 점에서 변 BC와 평행한 선분을 그었을 때 변 AC와 만나는 점을 각각 "
              "[[sub(C,1)]], [[sub(C,2)]], ⋯, [[sub(C, n - 1)]]이라 할 때, [[lim(n, inf, frac(2 pi, n) sum(k, 1, n - 1, pow(sub(B,k) sub(C,k), 2)))]]의 값은?"),
    choices=["[[frac(pi,6)]]", "[[frac(pi,3)]]", "[[frac(pi,2)]]", "[[frac(2,3) pi]]", "[[pi]]"],
    derived_answer="④",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래 직각, C 오른쪽 아래), AB 위의 분점 B₁, B₂, B₃, …, B_{n−2}, B_{n−1}과 AC 위의 점 C₁, C₂, C₃, …, C_{n−2}, C_{n−1}, BC에 평행한 선분 B_kC_k"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 직각삼각형+평행선 도형 / " + PS + " (Σ 안의 B_kC_k²은 선분 길이의 제곱)",
    note="B_kC_k=k/n → 2π∫₀¹ x²dx = 2π/3 → ④. 빠른정답 3과 불일치.")

# p75 — [2013년 4월 고3 이과 29번/4점]
add(id="92b98315", qtype="short",
    question=("그림과 같이 한 변의 길이가 1인 정사각형 ABCD가 있다. 2 이상의 자연수 [[n]]에 대하여 변 BC를 [[n]]등분한 각 분점을 점 B에서 가까운 것부터 차례로 "
              "[[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, n - 1)]]이라 하고, 변 CD를 [[n]]등분한 각 분점을 점 C에서 가까운 것부터 차례로 "
              "[[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], ⋯, [[sub(Q, n - 1)]]이라 하자.\n"
              "[[1 <= k <= n - 1]]인 자연수 [[k]]에 대하여 사각형 A[[sub(P,k)]][[sub(Q,k)]]D의 넓이를 [[sub(S,k)]]라 하자.\n"
              "[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(S,k))) = alpha]]일 때, [[150 alpha]]의 값을 구하시오."),
    choices=None, derived_answer="100",
    figure=U("정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위, 한 변 1), BC 위의 점 P₁, P₂, P₃, …, P_k, …, P_{n−1}, CD 위의 점 Q₁, Q₂, Q₃, …, Q_k, …, Q_{n−1}, 사각형 AP_kQ_kD 음영"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 정사각형+분점+사각형 음영 도형 / " + PS,
    note="출처 [2013년 4월 고3 이과 29번/4점]. S=1−x/2−(1−x)x/2 = 1−x+x²/2 → α=∫₀¹ = 2/3 → 150α=100. 빠른정답 3과 불일치.")

# p76 — [2015년 4월 고3 이과 28번/4점]
add(id="d0f6dae1", qtype="short",
    question=("그림과 같이 중심각의 크기가 [[frac(pi,2)]]이고, 반지름의 길이가 8인 부채꼴 OAB가 있다. 2 이상의 자연수 [[n]]에 대하여 호 AB를 [[n]]등분한 각 분점을 "
              "점 A에서 가까운 것부터 차례로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, n - 1)]]이라 하자. "
              "[[1 <= k <= n - 1]]인 자연수 [[k]]에 대하여 점 B에서 선분 O[[sub(P,k)]]에 내린 수선의 발을 [[sub(Q,k)]]라 하고, "
              "삼각형 O[[sub(Q,k)]]B의 넓이를 [[sub(S,k)]]라 하자.\n"
              "[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(S,k))) = frac(alpha, pi)]]일 때, [[alpha]]의 값을 구하시오."),
    choices=None, derived_answer="32",
    figure=U("부채꼴 OAB(반지름 8, OA 가로·OB 세로, 중심각 π/2), 호 위의 분점 P₁, P₂, P₃, …, P_k, …, P_{n−1}, B에서 OP_k에 내린 수선의 발 Q_k(직각 표시), 삼각형 OQ_kB 음영"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 부채꼴+수선+삼각형 도형 / " + PS,
    note="출처 [2015년 4월 고3 이과 28번/4점]. S_k=(1/2)·64·sinθcosθ=16sin(kπ/n) → 16·(2/π)=32/π → α=32. 빠른정답 16과 불일치.")

# p77 — [2015년 4월 고3 이과 28번 변형]
add(id="37c54bce", qtype="short",
    question=("다음 그림과 같이 중심각의 크기가 [[frac(pi,2)]]이고, 반지름의 길이가 10인 부채꼴 OAB가 있다. 2 이상의 자연수 [[n]]에 대하여 호 AB를 [[2n]]등분한 각 분점을 "
              "점 A에서 가까운 것부터 차례로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, 2n - 1)]] 이라 하자.\n"
              "[[1 <= k <= 2n - 1]]인 자연수 [[k]]에 대하여 점 B에서 선분 O[[sub(P,k)]]에 내린 수선의 발을 [[sub(Q,k)]]라 하고, "
              "삼각형 O[[sub(Q,k)]]B의 넓이를 [[sub(S,k)]]라 하자. [[lim(n, inf, frac(1,n) sum(k, 1, 2n - 1, sub(S,k))) = frac(alpha, pi)]]일 때,\n"
              "[[alpha]]의 값을 구하시오."),
    choices=None, derived_answer="100",
    figure=U("부채꼴 OAB(반지름 10, OA 가로·OB 세로, 중심각 π/2), 호 위의 분점 P₁, P₂, P₃, …, P_k, …, P_{2n−1}, B에서 OP_k에 내린 수선의 발 Q_k(직각 표시), 삼각형 OQ_kB 음영"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 부채꼴+수선+삼각형 도형 / " + PS,
    note="출처 [2015년 4월 고3 이과 28번 변형]. S_k=25sin(kπ/2n), (1/n)=(2/π)Δ → (2/π)·25·∫₀^π sin x dx = 100/π → α=100. 빠른정답 4와 불일치.")

# p78 — [2007년 7월 고3 이과 23번]
add(id="c316b524", qtype="short",
    question=("[[seg(AD) = 1]], [[seg(AB) = sqrt(2)]], [[seg(BC) = 3]]인 등변사다리꼴 ABCD에서 변 AB를 [[n]]등분한 점을 각각 "
              "[[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, n - 1)]]이라 하고 각 점에서 변 BC에 평행한 직선을 그어 변 CD와 만나는 점을 각각 "
              "[[sub(Q,1)]], [[sub(Q,2)]], ⋯, [[sub(Q, n - 1)]]이라 할 때,\n"
              "lim_{[[n]]→∞} [[frac(1,n)]] ([[pow(sub(P,1) sub(Q,1), 3) + pow(sub(P,2) sub(Q,2), 3) + pow(sub(P,3) sub(Q,3), 3)]] + ⋯ + [[pow(sub(P,n) sub(Q,n), 3)]])\n"
              "의 값을 구하시오."),
    choices=None, derived_answer="10",
    figure=U("등변사다리꼴 ABCD(AD 위쪽 짧은 변, BC 아래쪽 긴 변), AB 위의 점 P₁, P₂, …, P_{n−1}, B(=P_n), CD 위의 점 Q₁, Q₂, …, Q_{n−1}, C(=Q_n), BC에 평행한 선분 P_kQ_k"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 등변사다리꼴+평행선 도형 / " + PS + " (P_kQ_k³은 선분 길이의 세제곱) / 줄임표 ⋯가 든 극한식은 텍스트 혼합",
    note="출처 [2007년 7월 고3 이과 23번]. P_kQ_k=1+2k/n → ∫₀¹(1+2x)³dx = [(1+2x)⁴/8]₀¹ = 10. 빠른정답 100과 불일치.")

# p79 — [2014년 9월 고3 이과 13번/3점]
add(id="31a8a84e", qtype="choice",
    question=("그림과 같이 중심이 O, 반지름의 길이가 1이고 중심각의 크기가 [[frac(pi,2)]]인 부채꼴 OAB가 있다.\n"
              "자연수 [[n]]에 대하여 호 AB를 [[2n]]등분한 각 분점(양 끝점도 포함)을 차례로 [[sub(P,0)]](= A), [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, 2n - 1)]], [[sub(P, 2n)]](= B)라 하자. "
              "다음 물음에 답하시오.\n주어진 자연수 [[n]]에 대하여 [[sub(S,k)]] ([[1 <= k <= n]])을 삼각형 O[[sub(P, n - k)]][[sub(P, n + k)]]의 넓이라 할 때,\n"
              "[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(S,k)))]]의 값은?"),
    choices=["[[frac(1,pi)]]", "[[frac(13, 12 pi)]]", "[[frac(7, 6 pi)]]", "[[frac(5, 4 pi)]]", "[[frac(4, 3 pi)]]"],
    derived_answer="①",
    figure=U("부채꼴 OAB(반지름 1, 중심각 π/2, OA 가로), 호 위의 분점 P₀(=A), P₁, …, P_{n−2}, P_{n−1}, P_n, P_{n+1}, P_{n+2}, …, P_{2n−1}, P_{2n}(=B)과 O에서 각 분점으로 그은 선분"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 부채꼴+분점 도형 / " + PS,
    note="출처 [2014년 9월 고3 이과 13번/3점]. ∠P_{n−k}OP_{n+k}=kπ/2n → S_k=(1/2)sin(kπ/2n) → (1/2)(2/π)∫₀^{π/2} sin x dx = 1/π → ①. 빠른정답 32와 불일치.")

# ───────────────────────── 삼각함수의 극한과 미분 ─────────────────────────
# p67 — [2015년 3월 고3 이과 21번/4점]
add(id="1d979d08", qtype="choice",
    question=("실수 전체의 집합에서 정의된 두 함수\n[[f(x) = pow(sin(x), 2) + a cos(x)]]\n"
              "[[g(x)]] = { 0 ([[x < -frac(pi,2)]]) ; [[x]] ([[-frac(pi,2) <= x < pi]]) ; [[b x]] ([[x >= pi]]) }\n"
              "에 대하여 <보기>에서 옳은 것만을 있는 대로 고른 것은?\n(단, [[a]], [[b]]는 실수이다.)\n<보기>\n"
              "ㄱ. [[lim(x, -frac(pi,2), g(x), -) = 0]]\n"
              "ㄴ. [[a = 2]]이면 합성함수 ([[comp(f, g)]])([[x]])는 [[x = -frac(pi,2)]]에서 연속이다.\n"
              "ㄷ. [[a]]의 값에 관계없이 합성 함수 ([[comp(f, g)]])([[x]])가 [[x = pi]]에서 연속이면 [[b = 2n - 1]] ([[n]]은 정수)이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PW + " / 문법 범위 밖: 합성함수 적용 표기 (f∘g)(x)는 ([[comp(f, g)]])([[x]])로 텍스트 혼합",
    note="출처 [2015년 3월 고3 이과 21번/4점]. ㄱ ✓, ㄴ x→−π/2− 에서 f(0)=2, (f∘g)(−π/2)=f(−π/2)=1 ✗, ㄷ cos(bπ)=−1·sin(bπ)=0 → b=2n−1 ✓ → ③ = 빠른정답 ✓.")

# p69 — [2015년 10월 고3 이과 12번/3점]
add(id="2596567d", qtype="choice",
    question=("그림과 같이 길이가 2인 선분 AB를 지름으로 하는 반원 위의 점 P에 대하여 [[angle(PAB) = theta]]라 하자. "
              "선분 OB 위의 점 C가 [[angle(APO) = angle(OPC)]]를 만족시킬 때, [[lim(theta, 0, seg(OC), +)]]의 값은?\n"
              "(단, [[0 < theta < frac(pi,4)]]이고, 점 O는 선분 AB의 중점이다.)"),
    choices=["[[frac(1,12)]]", "[[frac(1,6)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(5,12)]]"],
    derived_answer="④",
    figure=U("지름 AB=2인 반원, 중점 O, 반원 위의 점 P, 선분 OB 위의 점 C, 선분 AP·PO·PC, ∠PAB=θ 표시, ∠APO=∠OPC 같은 각 표시"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 반원+각의 이등분 도형",
    note="출처 [2015년 10월 고3 이과 12번/3점]. △OPC에서 ∠POC=2θ, ∠OPC=θ → OC=sinθ/sin3θ → 1/3 → ④ = 빠른정답 ✓.")

# p70 — [2015년 10월 고3 이과 12번 변형]
add(id="10454b95", qtype="choice",
    question=("다음 그림과 같이 길이가 4인 선분 AB를 지름으로 하는 반원 위의 점 P에 대하여 [[angle(APO) = theta]]라 하자. "
              "선분 OB 위의 점 C가 [[2 angle(APO) = angle(OPC)]]를 만족시킬 때, [[lim(theta, 0, seg(OC), +)]]의 값은?\n"
              "(단, [[0 < theta < frac(pi,6)]]이고, 점 O는 선분 AB의 중점이다.)"),
    choices=["[[frac(1,6)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]", "[[1]]"],
    derived_answer="⑤",
    figure=U("지름 AB=4인 반원, 중점 O, 반원 위의 점 P, 선분 OB 위의 점 C, 선분 AP·PO·PC, ∠APO=θ, ∠OPC=2θ 표시"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 반원+각 표시 도형",
    note="출처 [2015년 10월 고3 이과 12번 변형]. OP=2, ∠POC=2θ, ∠OPC=2θ → OC=2sin2θ/sin4θ=1/cos2θ → 1 → ⑤. 빠른정답 '1'은 값 1과 일치하나 선지 번호로는 불일치.")

# p74 — 출처 머리말 없음
add(id="a3b4c0ed", qtype="choice",
    question=("다음 그림과 같이 반지름의 길이가 1이고 중심각의 크기가 [[frac(pi,3)]]인 부채꼴 OAB가 있다. 호 AB 위의 점 P에서 선분 OA에 내린 수선의 발을 H, "
              "선분 PH와 선분 AB의 교점을 Q라 하자. [[angle(POH) = theta]]일 때, 삼각형 AQH의 넓이를 [[S(theta)]]라 하자. "
              "[[lim(theta, 0, frac(S(theta), pow(theta,4)), +)]]의 값은?\n(단, [[0 < theta < frac(pi,3)]])"),
    choices=["[[frac(1,8)]]", "[[frac(sqrt(3),8)]]", "[[frac(1,4)]]", "[[frac(sqrt(5),8)]]", "[[frac(sqrt(6),8)]]"],
    derived_answer="②",
    figure=U("부채꼴 OAB(반지름 1, 중심각 π/3, OA 가로), 호 위의 점 P, OA 위의 수선의 발 H(직각 표시), PH와 AB의 교점 Q, 삼각형 AQH 음영, ∠POH=θ 표시"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 부채꼴+수선+삼각형 음영 도형",
    note="△OAB 정삼각형 → QH=√3(1−cosθ), S=(√3/2)(1−cosθ)² ~ (√3/8)θ⁴ → ②. 빠른정답 1과 불일치.")

# p76 — [2020년 11월 고3 이과 24번/3점]
add(id="eb745fc7", qtype="short",
    question=("그림과 같이 [[seg(AB) = 2]], [[angle(B) = frac(pi,2)]]인 직각삼각형 ABC에서 중심이 A, 반지름의 길이가 1인 원이 두 선분 AB, AC와 만나는 점을 각각 D, E라 하자. "
              "호 DE의 삼등분점 중 점 D에 가까운 점을 F라 하고, 직선 AF가 선분 BC와 만나는 점을 G라 하자. [[angle(BAG) = theta]]라 할 때, "
              "삼각형 ABG의 내부와 부채꼴 ADF의 외부의 공통부분의 넓이를 [[f(theta)]], 부채꼴 AFE의 넓이를 [[g(theta)]]라 하자.\n"
              "[[40 × lim(theta, 0, frac(f(theta), g(theta)), +)]]의 값을 구하시오. (단, [[0 < theta < frac(pi,6)]])"),
    choices=None, derived_answer="60",
    figure=U("직각삼각형 ABC(A 왼쪽, B 오른쪽 아래 직각, C 오른쪽 위), A 중심 반지름 1인 원과 AB·AC의 교점 D·E, 호 DE의 삼등분점 F, AF의 연장선과 BC의 교점 G, 영역 f(θ)(삼각형 ABG 내부·부채꼴 ADF 외부)와 g(θ)(부채꼴 AFE) 음영, ∠BAG=θ 표시"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 직각삼각형+원+부채꼴 음영 복합 도형",
    note="출처 [2020년 11월 고3 이과 24번/3점]. f=2tanθ−θ/2, g=(1/2)·1·2θ=θ → f/g→3/2 → 40·3/2=60. 빠른정답 1과 불일치. 원문 '40 ·'는 ×로.")

# p77 — 출처 머리말 없음
add(id="32653483", qtype="choice",
    question=("다음 그림과 같이 한 변의 길이가 3인 마름모 ABCD가 있다. 점 B에서 선분 CD의 연장선에 내린 수선의 발을 E, 점 E에서 선분 BD에 내린 수선의 발을 F, "
              "직선 EF와 선분 AB의 교점을 G라 하자. [[angle(ABD) = theta]]일 때, 삼각형 BFG의 넓이를 [[S(theta)]]라 하자. "
              "[[lim(theta, 0, frac(S(theta), pow(theta,5)), +)]]의 값은? (단, [[0 < theta < frac(pi,4)]])"),
    choices=["[[12]]", "[[14]]", "[[16]]", "[[18]]", "[[20]]"],
    derived_answer="④",
    figure=U("마름모 ABCD(B 왼쪽, D 오른쪽, A 위, C 아래, CD=3 표시), CD의 연장선 위의 수선의 발 E(직각 표시), BD 위의 수선의 발 F(직각 표시), EF와 AB의 교점 G, 대각선 BD"),
    difficulty_est=4, confidence=0.85, needs_review="도형 표현 불가: 마름모+수선 복합 도형",
    note="BF=6cosθsin²θ, GF=6sin³θ → S=18cosθsin⁵θ → 18 → ④. 빠른정답 2와 불일치.")

# p94 — 출처 머리말 없음
add(id="77b20513", qtype="short",
    question=("함수 [[f(x)]] = { [[a sin(x) + (b + 1) cos(x) - 1]] ([[x >= 0]]) ; [[pow(e, 4x + 1)]] ([[x < 0]]) }이 모든 실수 [[x]]에서 미분가능할 때, "
              "상수 [[a]], [[b]]에 대하여 [[frac(a,b)]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.85, needs_review=PW,
    note="연속: b=e, 미분가능: a=4e → a/b=4 = 빠른정답 ✓.")

# p95 — 출처 머리말 없음
add(id="e3ee7eb2", qtype="short",
    question=("함수 [[f(x)]] = { [[a cos(x) + b sin(x)]] ([[x >= 0]]) ; [[pow(e, x)]] ([[x < 0]]) }이 [[x = 0]]에서 미분가능하도록 하는 상수 [[a]], [[b]]의 합 "
              "[[a + b]]의 값을 구하여라."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.85, needs_review=PW,
    note="연속: a=1, 미분가능: b=1 → a+b=2 = 빠른정답 ✓.")

# p97 — 출처 머리말 없음
add(id="6a637d39", qtype="choice",
    question=("함수 [[f(x)]] = { [[2 pow(x,2) + a x + b]] ([[x < 0]]) ; [[sin(x)]] ([[x >= 0]]) }이 [[x = 0]]에서 미분가능하도록 하는 상수 [[a]], [[b]]에 대하여 "
              "[[a + b]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85, needs_review=PW,
    note="연속: b=0, 미분가능: a=1 → a+b=1 → ① = 빠른정답 ✓.")

# ───────────────────────── 방정식과 부등식에의 활용 ─────────────────────────
# p81 — [2016년 4월 고3 이과 14번/4점]
add(id="ee4c0863", qtype="choice",
    question=("다음은 모든 실수 [[x]]에 대하여 [[2x - 1 >= k pow(e, pow(x,2))]]을 성립시키는 실수 [[k]]의 최댓값을 구하는 과정이다.\n"
              "[[f(x) = (2x - 1) pow(e, -pow(x,2))]]이라 하자.\n"
              "[[prime(f)(x)]] = ( (가) ) × [[pow(e, -pow(x,2))]]\n"
              "[[prime(f)(x) = 0]]에서 [[x = -frac(1,2)]] 또는 [[x = 1]]\n"
              "함수 [[f(x)]]의 증가와 감소를 조사하면 함수 [[f(x)]]의 극솟값은 (나) 이다.\n"
              "또한 [[lim(x, inf, f(x)) = 0]], [[lim(x, -inf, f(x)) = 0]]이므로 함수 [[y = f(x)]]의 그래프의 개형을 그리면 함수 [[f(x)]]의 최솟값은 (나) 이다.\n"
              "따라서 [[2x - 1 >= k pow(e, pow(x,2))]]을 성립시키는 실수 [[k]]의 최댓값은 (나) 이다.\n"
              "위의 (가)에 알맞은 식을 [[g(x)]], (나)에 알맞은 수를 [[p]]라 할 때, [[g(2) × p]]의 값은?"),
    choices=["[[frac(10, e)]]", "[[frac(15, e)]]", "[[frac(20, root(4, e))]]", "[[frac(25, root(4, e))]]", "[[frac(30, root(4, e))]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85, needs_review=PR,
    note="출처 [2016년 4월 고3 이과 14번/4점]. g(x)=−4x²+2x+2, g(2)=−10, p=f(−1/2)=−2/⁴√e → g(2)p=20/⁴√e → ③ = 빠른정답 ✓.")

# p84 — [2016년 4월 고3 이과 14번 변형]
add(id="fcb5aed9", qtype="choice",
    question=("다음은 모든 실수 [[x]]에 대하여 [[3x + frac(3,2) >= k pow(e, pow(x,2))]]을 성립시키는 실수 [[k]]의 최댓값을 구하는 과정이다.\n"
              "[[f(x) = (3x + frac(3,2)) pow(e, -pow(x,2))]]이라 하자.\n"
              "[[prime(f)(x)]] = ( (가) ) × [[pow(e, -pow(x,2))]]\n"
              "[[prime(f)(x) = 0]]에서 [[x = -1]] 또는 [[x = frac(1,2)]]\n"
              "함수 [[f(x)]]의 증가와 감소를 조사하면 함수 [[f(x)]]의 극솟값은 (나) 이다.\n"
              "또한, [[lim(x, inf, f(x)) = 0]], [[lim(x, -inf, f(x)) = 0]]이므로 함수 [[y = f(x)]]의 그래프의 개형을 그리면 함수 [[f(x)]]의 최솟값은 (나) 이다.\n"
              "따라서 [[3x + frac(3,2) >= k pow(e, pow(x,2))]]을 성립시키는 실수 [[k]]의 최댓값은 (나) 이다.\n"
              "위의 (가)에 알맞은 식을 [[g(x)]], (나)에 알맞은 수를 [[p]]라 할 때, [[g(3) × p]]의 값은?"),
    choices=["[[frac(30, e)]]", "[[frac(90, e)]]", "[[frac(30, root(4, e))]]", "[[frac(60, root(4, e))]]", "[[frac(90, root(4, e))]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85, needs_review=PR,
    note="출처 [2016년 4월 고3 이과 14번 변형]. g(x)=−6x²−3x+3, g(3)=−60, p=f(−1)=−3/(2e) → g(3)p=90/e → ②. 빠른정답 3과 불일치. 원문 '·'는 ×로.")

# p91 — 출처 머리말 없음
add(id="8fad3145", qtype="choice",
    question=("다음은 [[n]]이 자연수이고 [[x > 1]]일 때, 부등식 [[pow(x, n + 1) + n > (n + 1) x]]가 성립하는 과정을 나타낸 것이다.\n"
              "[[f(x) = pow(x, n + 1) + n - (n + 1) x]]라 하면\n"
              "[[prime(f)(x) = (n + 1) pow(x, n) - (n + 1) = (n + 1)(pow(x, n) - 1)]]\n"
              "[[n]]은 자연수이고 [[x > 1]]일 때, [[prime(f)(x) > 0]]이므로 [[x > 1]]에서 함수 [[y = f(x)]]는 (가) 한다.\n"
              "이때 (나) = 0이므로 [[x > 1]]에서 (다) 이다.\n"
              "따라서 [[x > 1]]일 때,\n부등식 [[pow(x, n + 1) + n > (n + 1) x]]가 성립한다.\n"
              "위의 증명 과정 중 (가), (나), (다)에 알맞은 것을 차례로 적은 것으로 옳은 것은?"),
    choices=["감소, [[f(1)]], [[f(x) < 0]]", "감소, [[f(0)]], [[f(x) < 0]]", "증가, [[f(1)]], [[f(x) > 0]]", "증가, [[f(0)]], [[f(x) > 0]]", "증가, [[f(1)]], [[f(x) < 0]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85, needs_review=PR,
    note="(가) 증가, (나) f(1), (다) f(x)>0 → ③ = 빠른정답 ✓.")

# p92 — 출처 머리말 없음
add(id="f2d2fc0a", qtype="choice",
    question=("다음은 [[a > 0]], [[b > 0]]이고, [[n]]이 2 이상의 자연수일 때 [[pow(a + b, n) <= pow(2, n - 1)(pow(a, n) + pow(b, n))]]임을 증명한 것이다.\n"
              "[[f(x) = pow(2, n - 1)(pow(x, n) + 1) - pow(x + 1, n)]]이라 하면\n"
              "[[prime(f)(x)]] = [[n]]{ ((가))^([[n - 1]]) − [[pow(x + 1, n - 1)]] }\n"
              "이때 [[prime(f)(x) = 0]]에서 [[x]] = (나) 이고,\n"
              "[[f(x)]]는 [[x]] = (나) 에서 (다) 이며 최소이다.\n"
              "따라서 함수 [[f(x)]]의 최솟값은\n[[f]]((나)) = [[pow(2, n - 1) × 2 - pow(2, n) = 0]]\n"
              "∴ [[f(x) >= 0]] (단, 등호는 [[x = 1]]일 때 성립)\n"
              "즉, [[pow(x + 1, n) <= pow(2, n - 1)(pow(x, n) + 1)]]\n"
              "위의 부등식에 [[x]] = (라) 를 대입하면 주어진 부등식을 얻는다.\n"
              "위의 과정에서 (가), (나), (다), (라)에 알맞은 것을 차례로 적은 것은?"),
    choices=["[[x]], [[1]], 극소, [[a b]]", "[[x]], [[2]], 극대, [[a + b]]", "[[2x]], [[1]], 극소, [[frac(a,b)]]",
             "[[2x]], [[1]], 극대, [[frac(b,a)]]", "[[2x]], [[2]], 극소, [[frac(a,b)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PR + " / 문법 범위 밖: 빈칸 (가)의 거듭제곱 ((가))^(n−1)은 텍스트 혼합, 선지는 (가)(나)(다)(라) 열 제목의 표 형태",
    note="f′=n{(2x)^{n−1}−(x+1)^{n−1}} → (가) 2x, (나) 1, (다) 극소, (라) a/b → ③. 빠른정답 'neg(4)'와 불일치. 원문 '2^{n−1}·2'의 '·'는 ×로.")
