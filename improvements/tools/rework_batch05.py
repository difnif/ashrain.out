# -*- coding: utf-8 -*-
# batch05 (80문항: esc_sonnet_h3-1_2of2 22, esc_opus_h3-2_1of1 23, esc_sonnet_h3-2_1of4 25, esc_sonnet_h3-2_2of4 10) — v1.5 문법 재작업
# 핵심 교체: 확률질량함수 경우 나눔→cases(식, in(x, set(…)), …) / 조각적 정의→cases(식, 조건, …)('x<0, x>2'는 같은 식 두 쌍)
#            X̄→xbar(X), X̄_A→xbar(sub(X,A)) / σ→sigma, σ²→pow(sigma,2), N(m,σ²)→normald(m, pow(sigma,2))
#            f′(x)→app(prime(f), x), f″(x)→app(prime(f, 2), x), (f∘g)(x)→app(comp(f, g), x), (f∘g)′(2)→app(prime(comp(f, g)), 2)
#            f⁻¹(x)→app(inv(f), x), S₁(t)→app(sub(S,1), t), α(t)→alpha(t), fⁿ(x)→iter(f, n, x), 줄임표→cdots
#            첨자 점 라벨 ∠D₁OA₁→angle(D1OA1), ∠P₁OP₂→angle(P1OP2); 가변 첨자 라벨(Pₙ, Aₙ, C_k …)은 sub 텍스트 혼합으로 파싱 → 통과
# 도형(그래프·입체·원뿔 등)은 unsupported(raw) 유지 — 도형만 남은 항목은 통과
# 여전히 보류: 한 이미지에 별개 문항 2개(id 1개) 2건(c8fb9377, 27c8d446)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= esc_sonnet_h3-1_2of2 =================
# ---------------- 확률변수와 확률분포 ----------------
# 0. 1812aeb5 — p21: 확률질량함수 경우 나눔 → cases + in(x, set(…))
add(id="1812aeb5", qtype="choice",
    question="확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = cases(frac(x, 8) + k, in(x, set(1, 2)), k, in(x, set(3, 4)))]]\n일 때, 상수 [[k]]의 값은?",
    choices=["[[frac(1,32)]]", "[[frac(1,16)]]", "[[frac(3,32)]]", "[[frac(1,8)]]", "[[frac(5,32)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로(조건 'x=1, 2'는 in(x, set(1, 2))). 답 ⑤ 유지(3/8+4k=1)")

# 1. 1ce47ee7 — p22
add(id="1ce47ee7", qtype="choice",
    question="확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = cases(-frac(x, 7) + k, in(x, set(-1, 0)), frac(x, 7) + k, in(x, set(1, 2)))]]\n일 때, 상수 [[k]]의 값은?",
    choices=["[[frac(1,28)]]", "[[frac(1,14)]]", "[[frac(3,28)]]", "[[frac(1,7)]]", "[[frac(5,28)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로(조건은 in(x, set(…))). 답 ③ 유지(4/7+4k=1)")

# 2. 4029b6cc — p23
add(id="4029b6cc", qtype="choice",
    question="이산확률변수 [[X]]가 취할 수 있는 값이 -3, -1, 0, 1, 3이고 [[X]]의 확률질량함수가\n[[prob(X = x) = cases(k - frac(x, 10), in(x, set(-3, -1, 0)), k + frac(x, 10), in(x, set(1, 3)))]]\n일 때, 상수 [[k]]의 값은?",
    choices=["[[frac(1,25)]]", "[[frac(2,25)]]", "[[frac(3,25)]]", "[[frac(4,25)]]", "[[frac(1,5)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로(조건은 in(x, set(…))). 답 ① 유지(5k+8/10=1)")

# 3. 9794ed2c — p26
add(id="9794ed2c", qtype="choice",
    question="이산확률변수 [[X]]가 취할 수 있는 값이 -2, -1, 0, 1, 2이고 [[X]]의 확률질량함수가\n[[prob(X = x) = cases(k - frac(x, 9), in(x, set(-2, -1, 0)), k + frac(x, 9), in(x, set(1, 2)))]]\n일 때, 상수 [[k]]의 값은?",
    choices=["[[frac(1,15)]]", "[[frac(2,15)]]", "[[frac(1,5)]]", "[[frac(4,15)]]", "[[frac(1,3)]]"],
    figure=None, confidence=0.85,
    note="[2008년 9월 고3 이과 확률과 통계 27번]. 경우 나눔을 cases로(조건은 in(x, set(…))). 답 ① 유지(5k+6/9=1)")

# 4. 466846f8 — p27
add(id="466846f8", qtype="choice",
    question="확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = cases(frac(x, 3) + 2k, in(x, set(-2, -1)), k, in(x, set(0, 1)))]]\n일 때, 상수 [[k]]의 값은?",
    choices=["[[frac(1,2)]]", "[[frac(1,3)]]", "[[frac(1,4)]]", "[[frac(1,5)]]", "[[frac(1,6)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로(조건은 in(x, set(…))). 답 ② 유지(−1+6k=1)")

# 5. d6ad04c6 — p28: cases + 'P(X=3 또는 X=4)'는 한글이 든 확률이라 텍스트 혼합 유지(뜻 불변)
add(id="d6ad04c6", qtype="choice",
    question="확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = cases(frac(x, 11) + k, in(x, set(0, 1, 2)), frac(x, 11) - k, in(x, set(3, 4)))]]\n일 때, P([[X = 3]] 또는 [[X = 4]])는? (단, [[k]]는 상수이다.)",
    choices=["[[frac(3,11)]]", "[[frac(4,11)]]", "[[frac(5,11)]]", "[[frac(6,11)]]", "[[frac(7,11)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 'P(X=3 또는 X=4)'는 한글 '또는'이 들어 P(…)를 텍스트로 두고 조건만 마커(원문 표기 그대로). 답 ③ 유지(k=1/11 → 5/11)")

# 6. 61295479 — p30
add(id="61295479", qtype="choice",
    question="이산확률변수 [[X]]의 확률분포가\n[[prob(X = x) = cases(frac(x, 8) + k, in(x, set(1, 2, 3)), k, in(x, set(4, 5, 6)))]]\n일 때, 확률 [[prob(abs(X - 4) <= 1)]]은? (단, [[k]]는 상수)",
    choices=["[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로(조건은 in(x, set(…))). 답 ⑤ 유지(k=1/24 → P(3≤X≤5)=1/2)")

# 7. 8843c3bd — p96: 확률밀도함수 경우 나눔 → cases('x<0, x>2'는 0을 두 쌍으로). 그래프 unsupported → 통과
add(id="8843c3bd", qtype="choice",
    question="연속확률변수 [[X]]의 확률밀도함수 [[f(x)]]가\n[[f(x) = cases(abs(x - 1), 0 <= x <= 2, 0, x < 0, 0, x > 2)]]\n이고, 그 그래프는 그림과 같다.\n이 때, 확률 [[prob(frac(1,2) <= X <= frac(3,2))]]의 값은?",
    choices=["[[frac(1,16)]]", "[[frac(1,8)]]", "[[frac(1,6)]]", "[[frac(1,4)]]", "[[frac(1,2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: (0,1)에서 (1,0)으로 내려가고 (2,1)로 올라가는 V자 꺾은선(x<0, x>2에서는 0), 점선으로 y=1과 x=2 표시, 원점 O·1·2 눈금"}}],
    confidence=0.8,
    note="[2005년 10월 고3 이과 5번]. 경우 나눔을 cases로(조건 'x<0, x>2'는 0을 두 쌍으로 분리). 그래프는 unsupported(raw). 답 ④ 유지")

# ---------------- 모평균의 추정 ----------------
# 8. 3d28869b — p4: X̄ → xbar(X) (본문·표)
add(id="3d28869b", qtype="short",
    question="모집단 [[set(1, 3, 7, 9)]]에서 크기가 2인 표본을 임의로 복원추출할 때, 표본평균 [[xbar(X)]]의 확률분포를 표로 나타내면 다음과 같다. 0이 아닌 세 상수 [[a]], [[b]], [[c]]에 대하여 [[a b c]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "table", "args": {"head": ["[[xbar(X)]]", "[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]", "합계"],
                                      "rows": [["[[prob(xbar(X) = xbar(x))]]", "[[frac(1,16)]]", "[[frac(1,8)]]", "[[frac(1,16)]]", "[[frac(1,a)]]", "[[frac(1,b)]]", "[[frac(1,8)]]", "[[frac(1,16)]]", "[[frac(1,c)]]", "[[frac(1,16)]]", "[[1]]"]]}}],
    confidence=0.85,
    note="표본평균 X̄를 conj(X)에서 xbar(X)로 교체(표 머리·행 포함). 답 256 유지(a=8, b=4, c=8)")

# 9. 6901a158 — p6
add(id="6901a158", qtype="short",
    question="모집단 [[set(2, 4, 6)]]에서 크기가 2인 표본을 복원추출할 때, 표본평균 [[xbar(X)]]의 확률분포가 다음 표와 같다. 이때 상수 [[a]], [[b]], [[c]]에 대하여 [[9(a + 2b + c)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "table", "args": {"head": ["[[xbar(X)]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]", "합계"],
                                      "rows": [["[[prob(xbar(X) = xbar(x))]]", "[[a]]", "[[b]]", "[[c]]", "[[frac(2,9)]]", "[[frac(1,9)]]", "[[1]]"]]}}],
    confidence=0.85,
    note="표본평균 X̄를 xbar(X)로 교체(표 포함). 답 8 유지(a=1/9, b=2/9, c=3/9)")

# 10. efe6b491 — p8
add(id="efe6b491", qtype="short",
    question="모평균이 14, 모표준편차가 3인 어떤 모집단에서 크기가 9인 표본을 임의추출할 때, 표본평균 [[xbar(X)]]에 대하여 [[sd(xbar(X))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="표본평균 X̄를 xbar(X)로 교체. 답 1 유지(3/√9; 빠른정답 3과 불일치는 초안대로)")

# 11. b7923ed2 — p9
add(id="b7923ed2", qtype="choice",
    question="표준편차가 12인 정규분포를 따르는 모집단에서 크기가 36인 표본을 임의추출하여 구한 표본평균을 [[xbar(X)]]라 할 때, [[sd(xbar(X))]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    figure=None, confidence=0.85,
    note="[2022년 10월 고3 확률과 통계 23번/2점]. X̄를 xbar(X)로 교체. 답 ② 유지(12/√36=2; 빠른정답 8과 불일치는 초안대로)")

# 12. cf61e054 — p15
add(id="cf61e054", qtype="choice",
    question="다음은 어느 모집단의 확률분포표이다.\n이 모집단에서 크기가 16인 표본을 임의추출할 때, 표본평균 [[xbar(X)]]의 표준편차는?(단, [[a]]는 상수이다.)",
    choices=["[[frac(sqrt(6), 8)]]", "[[frac(sqrt(6), 6)]]", "[[frac(sqrt(6), 4)]]", "[[frac(sqrt(6), 2)]]", "[[sqrt(6)]]"],
    figure=[{"fn": "table", "args": {"head": ["[[X]]", "[[-2]]", "[[0]]", "[[1]]", "계"],
                                      "rows": [["[[prob(X = x)]]", "[[frac(1,4)]]", "[[a]]", "[[frac(1,2)]]", "[[1]]"]]}}],
    confidence=0.85,
    note="[2010년 9월 고3 문과 29번]. X̄를 xbar(X)로 교체. 답 ① 유지(V(X)=3/2 → √6/8; 빠른정답 2와 불일치는 초안대로)")

# 13. be4386ce — p18
add(id="be4386ce", qtype="choice",
    question="다음은 어느 모집단의 확률분포를 표로 나타낸 것이다.\n이 모집단에서 크기가 12인 표본을 임의추출할 때, 표본평균 [[xbar(X)]]의 표준편차는?",
    choices=["[[frac(1,2)]]", "[[frac(sqrt(10), 6)]]", "[[frac(sqrt(11), 6)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(13), 6)]]"],
    figure=[{"fn": "table", "args": {"head": ["[[X]]", "[[2]]", "[[4]]", "[[6]]", "[[8]]", "합계"],
                                      "rows": [["[[prob(X = x)]]", "[[frac(1,6)]]", "[[a]]", "[[frac(1,3)]]", "[[frac(1,6)]]", "[[1]]"]]}}],
    confidence=0.85,
    note="X̄를 xbar(X)로 교체. 답 ③ 유지(V(X)=11/3 → √11/6; 빠른정답 1과 불일치는 초안대로)")

# 14. 92e8a462 — p20
add(id="92e8a462", qtype="choice",
    question="어느 모집단의 확률변수 [[X]]의 확률분포를 표로 나타내면 다음과 같다. [[ev(pow(X,2)) = 21]]일 때, 이 모집단에서 임의추출한 크기가 10인 표본의 표본평균 [[xbar(X)]]에 대하여 [[var(xbar(X))]]는?",
    choices=["[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    figure=[{"fn": "table", "args": {"head": ["[[X]]", "[[0]]", "[[3]]", "[[6]]", "합계"],
                                      "rows": [["[[prob(X = x)]]", "[[frac(1,6)]]", "[[a]]", "[[b]]", "[[1]]"]]}}],
    confidence=0.85,
    note="X̄를 xbar(X)로 교체. 답 ⑤ 유지(V(X)=5 → 1/2; 빠른정답 3과 불일치는 초안대로)")

# 15. b66acec2 — p41: X̄, Ȳ → xbar
add(id="b66acec2", qtype="choice",
    question="지역 A에 살고 있는 성인들의 1인 하루 물 사용량을 확률변수 [[X]], 지역 B에 살고 있는 성인들의 1인 하루 물 사용량을 확률변수 [[Y]]라 하자. 두 확률변수 [[X]], [[Y]]는 정규분포를 따르고 다음 조건을 만족시킨다.\n(가) 두 확률변수 [[X]], [[Y]]의 평균은 각각 220과 240이다.\n(나) 확률변수 [[Y]]의 표준편차는 확률변수 [[X]]의 표준편차의 1.5배이다.\n지역 A에 살고 있는 성인 중 임의추출한 [[n]]명의 1인 하루 물 사용량의 표본평균을 [[xbar(X)]], 지역 B에 살고 있는 성인 중 임의추출한 [[9n]]명의 1인 하루 물 사용량의 표본평균을 [[xbar(Y)]]라 하자. [[prob(xbar(X) <= 215) = 0.1587]]일 때, [[prob(xbar(Y) >= 235)]]의 값을 다음 표준정규분포표를 이용하여 구한 것은? (단, 물 사용량의 단위는 L이다.)",
    choices=["[[0.6915]]", "[[0.7745]]", "[[0.8185]]", "[[0.8413]]", "[[0.9772]]"],
    figure=[{"fn": "table", "args": {"head": ["[[z]]", "[[prob(0 <= Z <= z)]]"],
                                      "rows": [["[[0.5]]", "[[0.1915]]"], ["[[1.0]]", "[[0.3413]]"], ["[[1.5]]", "[[0.4332]]"], ["[[2.0]]", "[[0.4772]]"]]}}],
    confidence=0.85,
    note="[2021년 9월 고3 확률과 통계 27번/3점]. X̄·Ȳ를 xbar(X)·xbar(Y)로 교체. 답 ⑤ 유지(σ(Ȳ)=2.5 → P(Z≥−2)=0.9772)")

# 16. 73916e86 — p72: N(m₁, σ²)→normald(sub(m,1), pow(sigma,2)), (σ/2)²→pow(frac(sigma,2),2), X̄_A→xbar(sub(X,A))
add(id="73916e86", qtype="choice",
    question="모집단 [[A]]는 정규분포 [[normald(sub(m,1), pow(sigma,2))]]을 따르고, 모집단 [[B]]는 정규분포 [[normald(sub(m,2), pow(frac(sigma,2), 2))]]을 따른다. 모집단 [[A]]에서 크기 [[sub(n,1)]], 모집단 [[B]]에서 크기 [[sub(n,2)]]인 표본을 각각 임의추출할 때의 표본평균을 각각 [[xbar(sub(X,A))]], [[xbar(sub(X,B))]]라 하자. <보기>에서 옳은 것만을 있는 대로 고른 것은?\n(단, [[sub(n,1)]], [[sub(n,2)]]는 1보다 큰 자연수이다.)\n<보기>\nㄱ. [[sub(m,1) = sub(m,2)]]이면 [[ev(xbar(sub(X,A))) = ev(xbar(sub(X,B)))]]이다.\nㄴ. 표본평균 [[xbar(sub(X,B))]]는 정규분포 [[normald(sub(m,2), pow(frac(sigma,2), 2))]]을 따른다.\nㄷ. [[sub(n,1) = 4 sub(n,2)]]일 때, [[sub(m,1)]]에 대한 신뢰도 [[pct(95)]]의 신뢰구간이 [[itv(a, b, cc)]]이고, [[sub(m,2)]]에 대한 신뢰도 [[pct(95)]]의 신뢰구간이 [[itv(c, d, cc)]]이면, [[b - a = d - c]]이다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2008년 9월 고3 이과 확률과 통계 29번]. σ를 sigma로(N(m₁,σ²)=normald, (σ/2)²=pow(frac(sigma,2),2)), 윗줄이 X_A 전체에 걸린 표본평균은 xbar(sub(X,A)). 답 ③ 유지")

# 17·18. ae71c4e5, 19f5b1a4 — p73(같은 이미지 id 2개): X̄_A, X̄_B → xbar(sub(X,A)), xbar(sub(X,B))
dup(["ae71c4e5", "19f5b1a4"], qtype="choice",
    question="정규분포 [[normald(m, pow(2,2))]]을 따르는 모집단에서 임의추출한 크기가 4인 표본과 크기가 16인 표본의 표본평균을 각각 [[xbar(sub(X,A))]], [[xbar(sub(X,B))]]라 하고, [[xbar(sub(X,A))]]와 [[xbar(sub(X,B))]]의 분포를 이용하여 신뢰도 [[pct(90)]]로 추정한 모평균 [[m]]의 신뢰구간을 각각 [[a <= m <= b]], [[c <= m <= d]]라고 하자. 다음 보기 중 항상 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[xbar(sub(X,A))]]의 분산은 [[xbar(sub(X,B))]]의 분산보다 크다.\nㄴ. [[prob(xbar(sub(X,A)) <= m + 1) <= prob(xbar(sub(X,B)) <= m + 1)]]\nㄷ. [[d - c < b - a]]",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="같은 이미지에 id 2개(같은 내용). 윗줄이 X_A 전체에 걸린 표본평균을 xbar(sub(X,A))로 교체. 답 ⑤ 유지")

# 19. 1c7b092a — p75: N(m, σ²) → normald(m, pow(sigma,2))
add(id="1c7b092a", qtype="choice",
    question="어느 회사에서 생산하는 린스 1개의 용량은 정규분포 [[normald(m, pow(sigma,2))]]을 따른다고 한다. 이 회사에서 생산하는 린스 중에서 100개를 임의추출하여 얻은 표본평균을 이용하여 구한 [[m]]에 대한 신뢰도 [[pct(95)]]의 신뢰구간이 [[752.96 <= m <= 760.8]]이다. 이 회사에서 생산하는 린스 중에서 [[n]]개를 임의추출하여 얻은 표본평균을 이용하여 구하는 [[m]]에 대한 신뢰도 [[pct(99)]]의 신뢰구간이 [[a <= m <= b]]일 때, [[b - a]]의 값이 8 이하가 되기 위한 자연수 [[n]]의 최솟값은? (단, 용량의 단위는 mL이고, [[Z]]가 표준정규분포를 따르는 확률변수일 때, [[prob(abs(Z) <= 1.96) = 0.95]], [[prob(abs(Z) <= 2.58) = 0.99]]로 계산한다.)",
    choices=["[[167]]", "[[168]]", "[[169]]", "[[170]]", "[[171]]"],
    figure=None, confidence=0.85,
    note="[2022년 11월 고3 확률과통계 27번 변형]. N(m, σ²)를 normald(m, pow(sigma,2))로 교체. 답 ① 유지(σ=20 → n≥166.41; 빠른정답 3과 불일치는 초안대로)")

# 20. 8dcfd9b2 — p87: '분산이 σ²인' → pow(sigma,2)
add(id="8dcfd9b2", qtype="choice",
    question="분산이 [[pow(sigma,2)]]인 정규분포를 따르는 모집단에서 크기 [[n]]인 표본을 임의추출하여 모평균 [[m]]을 추정한 후 신뢰구간의 길이를 구하고자 한다. 아래 표준정규분포표를 이용하여 구한 모평균 [[m]]에 대한 신뢰도 [[pct(79.6)]]의 신뢰구간의 길이가 [[l]]이고, 모평균 [[m]]에 대한 신뢰도 [[pct(alpha)]]의 신뢰구간의 길이는 [[2l]]이다. 이 때, [[alpha]]의 값은?",
    choices=["[[87.3]]", "[[90.9]]", "[[95.0]]", "[[98.9]]", "[[99.9]]"],
    figure=[{"fn": "table", "args": {"head": ["[[z]]", "[[prob(0 <= Z <= z)]]"],
                                      "rows": [["[[1.27]]", "[[0.3980]]"], ["[[1.69]]", "[[0.4545]]"], ["[[1.96]]", "[[0.4750]]"], ["[[2.54]]", "[[0.4945]]"], ["[[3.29]]", "[[0.4995]]"]]}}],
    confidence=0.85,
    note="[2010년 4월 고3 이과 13번]. σ²를 pow(sigma,2)로 교체. 답 ④ 유지(z=2.54 ↔ 98.9%)")

# 21. 6988bd90 — p97: 'σ' 및 선지 'σ = 4' → sigma
add(id="6988bd90", qtype="choice",
    question="표준편차가 [[sigma]]인 정규분포를 따르는 모집단에서 크기가 [[n]]인 표본을 임의추출하여 모평균을 추정하려고 한다. 일정한 신뢰도로 모평균을 추정할 때, 다음 중 신뢰구간의 길이가 가장 긴 것은?",
    choices=["[[n = 16]], [[sigma = 4]]", "[[n = 16]], [[sigma = 8]]", "[[n = 36]], [[sigma = 4]]", "[[n = 36]], [[sigma = 8]]", "[[n = 64]], [[sigma = 12]]"],
    figure=None, confidence=0.85,
    note="σ를 sigma로 교체(본문·선지). 답 ② 유지(σ/√n 최대 = 8/4)")

# ================= esc_opus_h3-2_1of1 =================
# ---------------- 부분적분법 ----------------
# 22. 85f5cbaa — p62: 경우 나눔 → cases
add(id="85f5cbaa", qtype="short",
    question="함수\n[[f(x) = cases(pow(e, x), 0 <= x < 1, pow(e, 2 - x), 1 <= x <= 2)]]\n에 대하여 열린 구간 [[itv(0, 2, oo)]]에서 정의된 함수\n[[g(x) = dinteg(0, x, abs(f(x) - f(t)), t)]]\n의 극댓값과 극솟값의 차는 [[a e + b root(3, pow(e,2))]] 이다. [[pow(a b, 2)]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수이다.)",
    choices=None, figure=None, confidence=0.8,
    note="[2018년 3월 고3 이과 30번/4점]. 경우 나눔을 cases로 교체. 답 36 유지(a=−2, b=3; 빠른정답 2와 불일치는 초안대로)")

# 23. e2975b44 — p64: f′(x) → app(prime(f), x)
add(id="e2975b44", qtype="short",
    question="실수 전체의 집합에서 미분가능한 함수 [[f(x)]]의 도함수 [[app(prime(f), x)]]가 [[app(prime(f), x) = abs(sin(x)) cos(x)]]이다. 양수 [[a]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[point(a, f(a))]]에서의 접선의 방정식을 [[y = g(x)]]라 하자. 함수 [[h(x) = dinteg(0, x, (f(t) - g(t)), t)]]가 [[x = a]]에서 극대 또는 극소가 되도록 하는 모든 양수 [[a]]를 작은 수부터 크기순으로 나열할 때, [[n]]번째 수를 [[sub(a,n)]]이라 하자. [[frac(100, pi)(sub(a,6) - sub(a,2))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2023년 11월 고3 미적분 30번/4점]. f′(x)를 app(prime(f), x)로 교체(원문 중괄호 {f(t)−g(t)}는 소괄호). 답 125 유지")

# 24. 4c87a401 — p67
add(id="4c87a401", qtype="short",
    question="실수 전체의 집합에서 미분가능한 함수 [[f(x)]]의 도함수 [[app(prime(f), x)]]가 [[app(prime(f), x) = abs(cos(x)) sin(x)]]이다. 양수 [[a]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[point(a, f(a))]]에서의 접선의 방정식을 [[y = g(x)]]라 하자. 함수 [[h(x) = dinteg(0, x, (f(t) - g(t)), t)]]가 [[x = a]]에서 극대 또는 극소가 되도록 하는 모든 양수 [[a]]를 작은 수부터 크기순으로 나열할 때, [[n]]번째 수를 [[sub(a,n)]]이라 하자. [[frac(60, pi)(sub(a,5) - sub(a,3))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2023년 11월 고3 미적분 30번 변형]. f′(x)를 app(prime(f), x)로 교체(원문 중괄호는 소괄호). 답 45 유지")

# ---------------- 넓이 ----------------
# 25. 1bd42de5 — p43: S₁(t) → app(sub(S,1), t)
add(id="1bd42de5", qtype="choice",
    question="[[0 < t < 1]]인 실수 [[t]]에 대하여 직선 [[y = 2t x]]가 곡선 [[y = 2x pow(e, -x)]]과 만나는 점 중 원점이 아닌 점을 P라 하자. 직선 [[y = 2t x]]와 곡선 [[y = 2x pow(e, -x)]]으로 둘러싸인 부분의 넓이를 [[app(sub(S,1), t)]]라 하고, 점 P를 지나고 [[x]]축에 수직인 직선과 직선 [[y = 2t x]] 및 [[x]]축으로 둘러싸인 부분의 넓이를 [[app(sub(S,2), t)]]라 하자. 집합 [[setb(t, 0 < t < 1)]]에서 정의된 함수 [[f(t) = app(sub(S,1), t) - app(sub(S,2), t)]]가 [[t = alpha]]에서 극솟값을 가질 때, [[frac(f(alpha), alpha)]]의 값은?",
    choices=["[[2e]]", "[[2e - 2]]", "[[2e - 4]]", "[[2e - 6]]", "[[2e - 8]]"],
    figure=None, confidence=0.85,
    note="첨자 함수 S₁(t)·S₂(t)를 app(sub(S,1), t)·app(sub(S,2), t)로 교체. 답 ④ 유지(2e−6; 빠른정답 2와 불일치는 초안대로)")

# 26. c9d2b1ee — p91: f′(xₙ) → app(prime(f), sub(x,n))
add(id="c9d2b1ee", qtype="short",
    question="상수 [[a]], [[b]]에 대하여 함수 [[f(x) = a pow(sin(x), 3) + b sin(x)]]가 [[f(frac(pi,4)) = sqrt(2)]], [[f(frac(pi,3)) = 2 sqrt(3)]] 을 만족시킨다. 실수 [[t]] ([[1 < t < 6]])에 대하여 함수 [[y = f(x)]]의 그래프와 직선 [[y = t]]가 만나는 점의 [[x]]좌표 중 양수인 것을 작은 수부터 크기순으로 모두 나열할 때, [[n]]번째 수를 [[sub(x,n)]]이라 하고 [[sub(c,n) = dinteg(sqrt(2), 2 sqrt(3), frac(t, app(prime(f), sub(x,n))), t)]]라 하자. [[sum(n, 1, 51, sub(c,n)) = p sqrt(2) + q]]일 때, [[p - q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 유리수이다.)",
    choices=None, figure=None, confidence=0.85,
    note="[2019년 6월 고3 이과 30번 변형]. f′(xₙ)을 app(prime(f), sub(x,n))으로 교체. 답 5 유지")

# ---------------- 함수의 그래프 ----------------
# 27. c8fb9377 — p99: 문법 문제 없음. 한 이미지에 별개 문항 2개(id 1개) → 보류 유지
add(id="c8fb9377", qtype="short",
    question="다음 그림과 같이 [[y = -frac(1,2) x]] 위의 제2사분면에 있는 점 P에서 곡선 [[y = frac(1, x)]]에 그은 두 접선의 접점을 각각 A, B라 할 때, [[pow(seg(PA), 2) + pow(seg(PB), 2)]]의 최솟값은 [[p + q sqrt(2)]] 이다. [[p + q]]의 값을 구하시오. (단, [[p]], [[q]]는 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=1/x(두 가지), 직선 y=−x/2, 제2사분면 위의 점 P에서 곡선에 그은 두 접선과 접점 A(제1사분면), B(제3사분면)"}}],
    confidence=0.75,
    needs_review="같은 이미지에 별개 문항 2개(위: [2017년 3월 고3 이과 30번 변형] — 전사함 / 아래: [2017년 10월 고3 이과 21번 변형] 반원 색종이를 AP로 접어 호 AP·호 PB·선분 AB로 둘러싸인 넓이 S(θ), S′(α)=2일 때 cos2α는? 선지 ①1/8 ②1/4 ③3/8 ④1/2 ⑤5/8, 답 ④)인데 id 1개 — 위 문항만 전사; 빠른정답 4는 아래 문항의 답과 일치",
    note="위 문항은 v1.5 문법 문제 없음(도형 unsupported). 답 25 유지(PA²+PB² 최솟값 15+10√2)")

# ---------------- 음함수와 역함수의 미분법 ----------------
# 28. ee440096 — p90: f′(x)·f⁻¹(x)·(g∘f)(x)·g′(1)·h′(1) → app
add(id="ee440096", qtype="short",
    question="[[a < b]]인 서로 다른 두 양수 [[a]], [[b]]에 대하여 함수 [[f(x)]]를 [[f(x) = -frac(a pow(x,3) + 3b x, pow(x,2) + 2)]]라 하자. 모든 실수 [[x]]에 대하여 [[app(prime(f), x) != 0]]이고, 두 함수 [[g(x) = f(x) - app(inv(f), x)]], [[h(x) = app(comp(g, f), x)]]가 다음 조건을 모두 만족시킨다.\n(가) [[g(1) = h(0)]]\n(나) [[app(prime(g), 1) = -2 app(prime(h), 1)]]\n[[18(b - a)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2021년 10월 고3 미적분 30번 변형]. f′(x)→app(prime(f), x), f⁻¹(x)→app(inv(f), x), (g∘f)(x)→app(comp(g, f), x), g′(1)·h′(1)→app. 답 12 유지(a=1/4, b=11/12; 빠른정답 11과 불일치는 초안대로)")

# ---------------- 속도와 거리 ----------------
# 29. 55a988b5 — p27: f′(t), f′(ln4) → app
add(id="55a988b5", qtype="choice",
    question="시각 [[t = 0]]일 때 원점을 출발하여 좌표평면 위를 움직이는 점 P의 시각 [[t]] ([[t > 0]])에서의 위치 [[point(x, y)]]가 [[x = t]], [[y = f(t)]]이다. 점 P가 다음 조건을 만족시킬 때, 시각 [[t = ln(4)]]에서 점 P의 [[y]]좌표는?\n(가) [[t > 0]]인 모든 실수 [[t]]에 대하여 함수 [[app(prime(f), t)]]는 연속이고, [[app(prime(f), ln(4)) > 0]]이다.\n(나) 모든 양의 실수 [[a]]에 대하여 점 P가 시각 [[t = 0]]에서 [[t = a]]까지 움직인 거리가 [[s]]일 때, [[a = ln(s + sqrt(pow(s,2) + 1))]]이다.",
    choices=["[[1]]", "[[frac(17,16)]]", "[[frac(9,8)]]", "[[frac(19,16)]]", "[[frac(5,4)]]"],
    figure=None, confidence=0.85,
    note="f′(t)·f′(ln4)를 app(prime(f), …)로 교체. 답 ③ 유지(f=cosh t−1 → 9/8)")

# ---------------- 부피 ----------------
# 30. 0288baf1 — p44: f′(1), f′(a)≥f′(b), f″(x) → app(prime(f), …), app(prime(f, 2), x)
add(id="0288baf1", qtype="choice",
    question="[[x > 0]]에서 미분가능한 함수 [[f(x)]]가 다음 조건을 만족한다.\n(가) [[f(1) = 0]], [[app(prime(f), 1) = 2]]\n(나) [[1 < a < b < pow(e,3)]]이면 [[app(prime(f), a) >= app(prime(f), b)]]\n(다) 구간 [[itv(1, pow(e,2), oo)]]에서 [[app(prime(f, 2), x) = -frac(2, pow(x,2))]]\n(라) 구간 [[itv(pow(e,2), pow(e,3), cc)]]에서 [[f(x) >= 0]]\n함수 [[y = f(x)]]의 그래프 위의 한 점 P에서 [[x]]축에 내린 수선의 발을 Q라 하고 선분 PQ를 지름으로 하는 반원을 좌표평면에 수직으로 세운다. 점 P가 함수 [[y = f(x)]] ([[1 <= x <= pow(e,3)]])의 그래프 위를 움직일 때, 이 반원에 의하여 생기는 입체도형의 부피의 최댓값은?",
    choices=["[[frac(pi,6)(pow(e,5) + 3 pow(e,4) + 3 pow(e,3) - pow(e,2) - 6)]]", "[[frac(pi,6)(pow(e,5) + 3 pow(e,4) + 3 pow(e,3) - pow(e,2) - 5)]]", "[[frac(pi,6)(pow(e,5) + 3 pow(e,4) + 3 pow(e,3) - pow(e,2) - 4)]]", "[[frac(pi,6)(pow(e,5) + 3 pow(e,4) + 3 pow(e,3) - pow(e,2) - 3)]]", "[[frac(pi,6)(pow(e,5) + 3 pow(e,4) + 3 pow(e,3) - pow(e,2) - 2)]]"],
    figure=None, confidence=0.85,
    note="f′(1)·f′(a)·f′(b)→app(prime(f), …), f″(x)→app(prime(f, 2), x). 답 ① 유지(빠른정답 128은 선지 범위 밖, 초안대로)")

# ---------------- 등비수열의 극한 ----------------
# 31. 5fe92d90 — p70: fⁿ(x) → iter(f, n, x); 단서 f¹=f, f^{n+1}=f∘fⁿ는 x를 붙여 iter로. 그래프 unsupported → 통과
add(id="5fe92d90", qtype="choice",
    question="그림은 함수 [[f(x) = 2 abs(x - frac(1,2))]] ([[0 <= x <= 1]])의 그래프이다.\n자연수 [[n]]에 대하여 집합 [[sub(A,n)]]을\n[[sub(A,n)]] = { [[x]] | [[iter(f, n, x) = 1]], [[0 <= x <= 1]] }\n이라 할 때, 집합 [[sub(A,n)]]의 원소의 개수를 [[sub(a,n)]]이라 하자. 예를 들어 [[sub(A,1) = set(0, 1)]], [[sub(A,2) = set(0, frac(1,2), 1)]]이므로 [[sub(a,1) = 2]], [[sub(a,2) = 3]]이다. [[lim(n, inf, frac(sub(a,n), sub(a, n + 1)))]]의 값은?\n(단, [[iter(f, 1, x) = f(x)]], [[iter(f, n + 1, x) = f(iter(f, n, x))]] ([[n]] = 1, 2, 3, ⋯) 이다.)",
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(3,4)]]", "[[1]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "y=f(x)=2|x−1/2| (0≤x≤1)의 그래프: (0,1), (1/2,0), (1,1)을 잇는 V자 꺾은선, y=1과 x=1 점선 보조선"}}],
    confidence=0.8,
    note="[2009년 3월 고3 문과 29번]. fⁿ(x)를 iter(f, n, x)로; 단서의 함수 등식 'f¹=f, f^{n+1}=f∘fⁿ'은 인자 없는 표기가 없어 x를 붙인 iter(f,1,x)=f(x), iter(f,n+1,x)=f(iter(f,n,x))로 표기(뜻 동일). 집합 조건 2개는 텍스트 혼합. 답 ② 유지(빠른정답 432는 선지 범위 밖)")

# ---------------- 접선의 방정식 ----------------
# 32. 3e109ea1 — p65: 경우 나눔 → cases
add(id="3e109ea1", qtype="choice",
    question="두 함수 [[f(x) = 2 ln(x) + 5]], [[g(x) = a pow(x,2) + b]]의 그래프가 [[x = 1]]인 점에서 공통의 접선을 갖고 함수 [[h(x)]]를\n[[h(x) = cases(f(x), x >= 1, g(x), x < 1)]]\n이라 하자. 점 [[point(0, k)]]에서 곡선 [[y = h(x)]]에 그을 수 있는 접선의 개수를 [[i(k)]]라 할 때, 함수 [[i(x)(pow(x,2) + c x + d)]]가 실수 전체의 집합에서 연속이다. [[frac(c d, a b)]]의 값은? (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)",
    choices=["[[-21]]", "[[-18]]", "[[-15]]", "[[-12]]", "[[-9]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로 교체. 답 ① 유지(a=1, b=4, c=−7, d=12; 빠른정답 4와 불일치는 초안대로)")

# 33. bad87dbc — p66
add(id="bad87dbc", qtype="choice",
    question="두 함수 [[f(x) = 2 ln(x) + 3]], [[g(x) = a pow(x,2) + b]]의 그래프가 [[x = 1]]인 점에서 공통의 접선을 갖고 함수 [[h(x)]]를\n[[h(x) = cases(f(x), x >= 1, g(x), x < 1)]]\n이라 하자. 점 [[point(0, k)]]에서 곡선 [[y = h(x)]]에 그을 수 있는 접선의 개수를 [[i(k)]]라 할 때, 함수 [[i(x)(pow(x,2) + c x + d)]]가 실수 전체의 집합에서 연속이다. [[a b + c d]]의 값은? (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)",
    choices=["[[-8]]", "[[-6]]", "[[-4]]", "[[-2]]", "[[0]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로 교체. 답 ③ 유지(a=1, b=2, c=−3, d=2)")

# ---------------- 지수함수와 로그함수의 극한과 미분 ----------------
# 34. 06e3fb8e — p84: (가) 경우 나눔 → cases
add(id="06e3fb8e", qtype="short",
    question="[[x >= 0]]에서 정의된 함수 [[f(x)]]가 다음 조건을 만족시킨다.\n(가) [[f(x) = cases(pow(2, x) - 1, 0 <= x <= 1, 4 × pow(frac(1,2), x) - 1, 1 < x <= 2)]]\n(나) 모든 양의 실수 [[x]]에 대하여 [[f(x + 2) = frac(1,2) f(x)]]이다.\n[[x > 0]]에서 정의된 함수 [[g(x)]]를 [[g(x) = lim(h, 0, frac(f(x + 6h) - f(x - 6h), h), +)]] 라 할 때, [[lim(t, 0, g(n - t) - g(n + t), +) - 8 g(n) = frac(3 ln(2), pow(2, 12))]] 를 만족시키는 모든 자연수 [[n]]의 값의 합을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    note="[2023년 4월 고3 미적분 30번 변형]. 경우 나눔을 cases로 교체(원문 중괄호 {g(n−t)−g(n+t)}는 lim 본체). 답 61 유지(n=33, 28; 빠른정답 4와 불일치는 초안대로)")

# ---------------- 등비급수 ----------------
# 35. 4d69fc35 — p17: bₙ 경우 나눔 → cases
add(id="4d69fc35", qtype="short",
    question="수열 [[set(sub(a,n))]]은 공비가 0이 아닌 등비수열이고, 수열 [[set(sub(b,n))]]을 모든 자연수 [[n]]에 대하여\n[[sub(b,n) = cases(2 sub(a,n), abs(sub(a,n)) < alpha, -frac(2, sub(a,n)), abs(sub(a,n)) >= alpha)]] ([[alpha]]는 양의 상수)\n라 할 때, 두 수열 [[set(sub(a,n))]], [[set(sub(b,n))]]과 자연수 [[p]]가 다음 조건을 만족시킨다.\n(가) [[sum(n, 1, inf, sub(a,n)) = -6]]\n(나) [[sum(n, 1, m, frac(sub(a,n), sub(b,n)))]] 의 값이 최소가 되도록 하는 자연수 [[m]]은 [[p]]이고, [[sum(n, 1, p, sub(b,n)) = 42]], [[sum(n, p + 1, inf, sub(b,n)) = -frac(3,16)]] 이다.\n[[16 × (sub(a,4) + p)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2024년 5월 고3 미적분 30번 변형]. 경우 나눔을 cases로 교체. 답 90 유지(r=1/2, p=6, a₄=−3/8)")

# 36. 73129095 — p67: ∠D₁OA₁ → angle(D1OA1); 낱말 '정사각형/삼각형/변'이 붙은 첨자 점 라벨은 sub 텍스트 혼합. 도형 unsupported → 통과
add(id="73129095", qtype="choice",
    question="그림과 같이 한 변의 길이가 [[a]]인 정사각형 O[[sub(B,1)]][[sub(C,1)]][[sub(A,0)]]이 있다. 삼각형 O[[sub(A,1)]][[sub(D,1)]]이 [[angle(D1OA1) = deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,1)]][[sub(C,1)]], [[sub(A,0)]][[sub(C,1)]] 위에 각각 점 [[sub(A,1)]], [[sub(D,1)]]을 잡고 변 O[[sub(A,1)]]의 길이를 [[sub(l,1)]]이라 하자.\n선분 O[[sub(A,1)]]을 한 변으로 하는 정사각형 O[[sub(B,2)]][[sub(C,2)]][[sub(A,1)]]에서 삼각형 O[[sub(A,2)]][[sub(D,2)]]가 [[angle(D2OA2) = deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,2)]][[sub(C,2)]], [[sub(A,1)]][[sub(C,2)]] 위에 각각 점 [[sub(A,2)]], [[sub(D,2)]]를 잡고 변 O[[sub(A,2)]]의 길이를 [[sub(l,2)]]라 하자.\n선분 O[[sub(A,2)]]를 한 변으로 하는 정사각형 O[[sub(B,3)]][[sub(C,3)]][[sub(A,2)]]에서 삼각형 O[[sub(A,3)]][[sub(D,3)]]이 [[angle(D3OA3) = deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,3)]][[sub(C,3)]], [[sub(A,2)]][[sub(C,3)]] 위에 각각 점 [[sub(A,3)]], [[sub(D,3)]]을 잡고 변 O[[sub(A,3)]]의 길이를 [[sub(l,3)]]이라 하자.\n이와 같은 과정을 계속하여 얻은 이등변삼각형 O[[sub(A,n)]][[sub(D,n)]]에서 변 O[[sub(A,n)]]의 길이를 [[sub(l,n)]] 이라 하자. [[sum(n, 1, inf, frac(1, sub(l,n))) = sqrt(3)]] 일 때, [[a]]의 값은?",
    choices=["[[sqrt(3)]]", "[[1 + sqrt(3)]]", "[[2 + sqrt(3)]]", "[[3 + sqrt(3)]]", "[[6 + sqrt(3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 OB₁C₁A₀ 안의 이등변삼각형 OA₁D₁(음영, ∠O=30°), OA₁을 한 변으로 하는 정사각형 OB₂C₂A₁과 삼각형 OA₂D₂(음영), 정사각형 OB₃C₃A₂와 삼각형 OA₃D₃(음영)이 O를 중심으로 회전하며 이어짐, 길이 a·l₁·l₂·l₃ 점선 호 표시, … 계속"}}],
    confidence=0.8,
    note="[2006년 6월 고3 이과 16번]. ∠D₁OA₁=30° 등 각 기호는 angle(D1OA1) = deg(30)으로; 원문이 낱말(정사각형·삼각형·변)로 쓴 첨자 점 라벨(OAₙDₙ 등 가변 첨자 포함)은 sub 텍스트 혼합 유지. 도형 unsupported(raw). 답 ③ 유지")

# 37. 26213efc — p72: Σ(P₁P_{i+1})² → sum 안에 sub 병치(가변 첨자라 seg 불가, 윗줄 생략). 원 도형 unsupported → 통과
add(id="26213efc", qtype="short",
    question="다음 그림과 같이 자연수 [[n]] 에 대하여 지름의 길이가 2인 원의 둘레를 [[4n]]등분하는 점을 시계 반대 방향으로 차례대로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, 4n)]] 이라 하자. [[sub(S,n) = sum(i, 1, 4n - 1, pow(sub(P,1) sub(P, i + 1), 2))]]이라 하면\n[[sum(m, 1, inf, pow(sum(n, 1, inf, frac(20, sub(S,n) sub(S, n + 1))), m - 1)) = frac(q, p)]] 일 때, [[p + q]] 의 값을 구하시오. (단, [[p]], [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "원 위에 4n등분점 P₁(위), P₂, P₃(왼쪽 위), …, P_{2n}, P_{2n+1}(아래), P_{2n+2}, …, P_{4n−1}, P_{4n}(오른쪽 위) 표시"}}],
    confidence=0.8,
    note="Sₙ 정의를 sum(i, 1, 4n−1, pow(sub(P,1) sub(P, i+1), 2))로 한 마커에 넣음 — 선분 P₁P_{i+1}은 가변 첨자라 seg로 못 써 sub 병치(윗줄 생략, 길이의 제곱 뜻 동일). 도형 unsupported(raw). 답 27 유지(Sₙ=8n → 16/11)")

# ---------------- 삼각함수의 덧셈정리 ----------------
# 38. 96818024 — p72: ∠P₁OP₂ → angle(P1OP2). 도형 unsupported → 통과
add(id="96818024", qtype="choice",
    question="두 직선 [[y = x + a]], [[y = frac(1,3) x + b]]가 원 [[pow(x,2) + pow(y,2) = pow(r,2)]]에 접하는 점을 각각 [[sub(P,1)]], [[sub(P,2)]]라 하고 [[angle(P1OP2) = alpha]]일 때, [[tan(alpha)]]의 값은? (단, [[a < 0]], [[b < 0]])",
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원 x²+y²=r²(중심 O), 제4사분면 쪽에서 접하는 두 직선 y=x+a, y=x/3+b, 접점 P₁·P₂, 각 α 표시"}}],
    confidence=0.85,
    note="[2008년 7월 고3 이과 미분과 적분 29번]. ∠P₁OP₂=α를 angle(P1OP2) = alpha로 교체. 도형 unsupported(raw). 답 ② 유지")

# ---------------- 여러 가지 함수의 적분 ----------------
# 39. 582840a2 — p33: 보기 ㄷ g′(β), g′(α) → app
add(id="582840a2", qtype="choice",
    question="실수 [[t]]에 대하여 곡선 [[y = pow(e, x)]] 위의 점 [[point(t, pow(e, t))]]에서의 접선의 방정식을 [[y = f(x)]]라 할 때, 함수 [[y = abs(f(x) + k - 2 sqrt(x))]] 가 양의 실수 전체의 집합에서 미분가능하도록 하는 실수 [[k]]의 최솟값을 [[g(t)]]라 하자. 두 실수 [[a]], [[b]] ([[a < b]])에 대하여 [[dinteg(a, b, g(t), t) = m]]이라 할 때, 보기에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[m < 0]]이 되도록 하는 두 실수 [[a]], [[b]] ([[a < b]])가 존재한다.\nㄴ. 실수 [[c]]에 대하여 [[g(c) = 0]]이면 [[g(-c) = 0]]이다.\nㄷ. [[a = alpha]], [[b = beta]] ([[alpha < beta]])일 때, [[m]]의 값이 최소이면 [[frac(app(prime(g), beta) + pow(e, -beta), app(prime(g), alpha)) > -e]]이다.",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="보기 ㄷ의 g′(β)·g′(α)를 app(prime(g), …)로 교체. 답 ③ 유지")

# 40. f5287f32 — p35
add(id="f5287f32", qtype="choice",
    question="실수 [[t]]에 대하여 곡선 [[y = pow(e, x)]] 위의 점 [[point(t, pow(e, t))]]에서의 접선의 방정식을 [[y = f(x)]]라 할 때, 함수 [[y = abs(f(x) + k - ln(x))]]가 양의 실수 전체의 집합에서 미분가능하도록 하는 실수 [[k]]의 최솟값을 [[g(t)]]라 하자. 두 실수 [[a]], [[b]] ([[a < b]])에 대하여 [[dinteg(a, b, g(t), t) = m]]이라 할 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[m < 0]]이 되도록 하는 두 실수 [[a]], [[b]] ([[a < b]])가 존재한다.\nㄴ. 실수 [[c]]에 대하여 [[g(c) = 0]]이면 [[g(-c) = 0]]이다.\nㄷ. [[a = alpha]], [[b = beta]] ([[alpha < beta]])일 때 [[m]]의 값이 최소이면 [[frac(1 + app(prime(g), beta), 1 + app(prime(g), alpha)) < -pow(e,2)]]이다.",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2019년 11월 고3 이과 21번/4점]. 보기 ㄷ의 g′(β)·g′(α)를 app(prime(g), …)로 교체. 답 ⑤ 유지(빠른정답 1과 불일치는 초안대로)")

# 41. fdda64cc — p64: 3조각 경우 나눔 → cases. 그래프 unsupported → 통과
add(id="fdda64cc", qtype="short",
    question="함수 [[f(x) = cases(-x - 2, x <= -2, sin(frac(pi,2) x), -2 < x <= 2, x - 2, x > 2)]]가 있다. 실수 [[t]]에 대하여 부등식 [[f(x) <= f(t)]]를 만족시키는 실수 [[x]]의 최솟값을 [[g(t)]]라 하자. 함수 [[g(t)]]가 [[t = a]]에서 미분가능하지 않은 모든 실수 [[a]]의 값을 작은 수부터 크기순으로 나열한 것을 [[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,n)]] ([[n]]은 자연수)라 할 때, [[n dinteg(sub(a,1), sub(a,n), g(t), t) = frac(p, pi) + q]]이다. [[20 abs(p + q)]] 의 값을 구하시오. (단, [[p]], [[q]]는 유리수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "y=f(x)의 그래프: x≤−2에서 직선(x=−2에서 0), −2<x≤2에서 사인 곡선(x=−1에서 최소, x=1에서 최대, x=0·2에서 0), x>2에서 직선"}}],
    confidence=0.8,
    note="[2018년 10월 고3 이과 30번 변형]. 3조각 경우 나눔을 cases로 교체. 그래프 unsupported(raw). 답 570 유지(빠른정답 3과 불일치는 초안대로)")

# 42. 90be9a31 — p78: 경우 나눔 → cases
add(id="90be9a31", qtype="short",
    question="실수 [[t]]에 대하여 함수 [[f(x)]]를 [[f(x) = cases(1 - abs(x - t), abs(x - t) <= 1, 0, abs(x - t) > 1)]] 이라 할 때, 어떤 짝수 [[k]]에 대하여 함수 [[g(t) = dinteg(k + frac(1,2), k + frac(17,2), f(x) sin(pi x), x)]]가 다음 조건을 만족시킨다.\n함수 [[g(t)]]가 [[t = alpha]]에서 극대이고 [[g(alpha) > 0]]인 모든 [[alpha]]를 작은 수부터 크기순으로 나열한 것을 [[sub(alpha,1)]], [[sub(alpha,2)]], ⋯, [[sub(alpha,m)]] ([[m]]은 자연수)라 할 때, [[sum(i, 1, m, sub(alpha, i)) = frac(65,2)]] 이다.\n[[k + pow(pi, 2) sum(i, 1, m, g(sub(alpha, i)))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    note="[2017년 11월 고3 이과 30번 변형]. 경우 나눔을 cases로 교체. 답 18 유지(k=2; 빠른정답 1과 불일치는 초안대로)")

# ---------------- 정적분과 급수의 합 사이의 관계 ----------------
# 43. facbee4c — p61: 문법 문제 없음(C_k는 sub(C,k)로 파싱). 원뿔 도형 unsupported → 통과
add(id="facbee4c", qtype="short",
    question="다음 그림과 같은 원뿔에서 밑면의 지름의 양 끝 점을 A, B라 하자. 원뿔의 모선 OB를 [[n]]등분하는 [[n - 1]]개의 점을 잡고 점 O로부터 [[k]]번째의 점을 [[sub(C,k)]]라 하자. 점 A에서 원뿔의 옆면을 따라 점 [[sub(C,k)]]까지 이르는 최단거리를 [[sub(l,k)]]라 할 때, [[lim(n, inf, sum(k, 1, n - 1, frac(pow(sub(l,k), 2), n)))]]의 값을 구하시오. (단, [[seg(AB) = 4]], [[seg(OA) = 6]])",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "원뿔(꼭짓점 O, 밑면 지름 AB), 모선 OB 위의 점 C_k, A에서 옆면을 따라 C_k에 이르는 곡선, 옆면 일부 음영"}}],
    confidence=0.85,
    note="가변 첨자 점 C_k는 sub(C,k)로 파싱되어 문법 문제 없음, 원뿔 도형은 unsupported(raw)만 남음 → 통과. 답 30 유지")

# ---------------- 방정식과 부등식에의 활용 ----------------
# 44. 14a43a06 — p56: f′(k) → app(prime(f), k)
add(id="14a43a06", qtype="short",
    question="[[a > 0]], [[b > 0]]인 두 상수 [[a]], [[b]]에 대하여 실수 전체의 집합에서 미분가능한 함수 [[f(x)]]가 다음 조건을 만족시킨다.\n(가) 모든 실수 [[x]]에 대하여 [[pow(f(x), 3) + f(x) = frac(a, pow(x,2) + 3) - b x - frac(8,3) b]] 이다.\n(나) 함수 [[f(x)]]의 역함수가 존재하고, [[app(prime(f), k) = 0]]인 실수 [[k]]가 존재한다.\n곡선 [[y = f(x)]]와 직선 [[y = -b x]]가 만나는 서로 다른 모든 점의 [[x]]좌표의 합이 [[k + 2]]일 때, [[a b = frac(q, p)]] 이다. [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None, figure=None, confidence=0.8,
    note="[2026년 7월 고3 미적분 30번 변형]. f′(k)를 app(prime(f), k)로 교체(원문 {f(x)}³는 pow(f(x),3)). 답 19 유지(ab=16/3; 빠른정답 86과 불일치는 초안대로)")

# ================= esc_sonnet_h3-2_1of4 =================
# ---------------- 치환적분법 ----------------
# 45. fdb87206 — p24: f′(x) → app(prime(f), x)
add(id="fdb87206", qtype="short",
    question="[[0 < x < 2 pi]]에서 정의된 미분가능한 함수 [[f(x)]]가 [[f(0) = ln(3)]]이고 [[app(prime(f), x) pow(e, f(x)) = -sin(x)]]를 만족시킨다.\n함수 [[f(x)]]가 [[x = a]]에서 극솟값 [[b]]를 가질 때, [[frac(a × pow(e,b), pi)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(x)e^{f(x)}를 app(prime(f), x) pow(e, f(x))로 교체. 답 1 유지(a=π, b=0)")

# ---------------- 부분적분법 ----------------
# 46. 13594afe — p2: f′(x) 경우 나눔 → app(prime(f), x) = cases(…)
add(id="13594afe", qtype="choice",
    question="실수 전체의 집합에서 연속인 함수 [[f(x)]]의 도함수 [[app(prime(f), x)]]가 [[app(prime(f), x) = cases(2x + 5, x < 1, 2 ln(x), x > 1)]]이다.\n[[f(e) = 3]]일 때, [[f(-8)]]의 값은?",
    choices=["[[15]]", "[[17]]", "[[19]]", "[[21]]", "[[23]]"],
    figure=None, confidence=0.85,
    note="f′(x)를 app(prime(f), x)로, 경우 나눔을 cases로 교체. 답 ③ 유지(f(−8)=19)")

# 47. 971ca355 — p3
add(id="971ca355", qtype="choice",
    question="실수 전체의 집합에서 연속인 함수 [[f(x)]]의 도함수 [[app(prime(f), x)]]가 [[app(prime(f), x) = cases(2x + 4, x < 1, 4 ln(x), x > 1)]]이다.\n[[f(e) = 5]]일 때, [[f(-5)]]의 값은?",
    choices=["[[1]]", "[[3]]", "[[5]]", "[[7]]", "[[9]]"],
    figure=None, confidence=0.85,
    note="f′(x)를 app(prime(f), x)로, 경우 나눔을 cases로 교체. 답 ① 유지(f(−5)=1)")

# ---------------- 넓이 ----------------
# 48·49. fcd883a1, ced39667 — p46(같은 이미지 id 2개): Pₙ(n, f(n)) → app(sub(P,n), n, f(n)); 가변 첨자 라벨은 sub 텍스트 혼합. 그래프 unsupported → 통과
dup(["fcd883a1", "ced39667"], qtype="choice",
    question="함수 [[f(x) = pow(e, -x)]]과 자연수 [[n]]에 대하여 점 [[sub(P,n)]], [[sub(Q,n)]]을 각각 [[app(sub(P,n), n, f(n))]], [[app(sub(Q,n), n + 1, f(n))]]이라 하자.\n삼각형 [[sub(P,n)]][[sub(P,n+1)]][[sub(Q,n)]]의 넓이를 [[sub(A,n)]], 선분 [[sub(P,n)]][[sub(P,n+1)]]과 함수 [[y = f(x)]]의 그래프로 둘러싸인 도형의 넓이를 [[sub(B,n)]]이라 할 때, <보기>에서 옳은 것을 모두 고른 것은?\n<보기>\nㄱ. [[dinteg(n, n + 1, f(x), x) = f(n) - (sub(A,n) + sub(B,n))]]\nㄴ. [[sum(n, 1, inf, sub(A,n)) = frac(1, 2e)]]\nㄷ. [[sum(n, 1, inf, sub(B,n)) = frac(3 - e, 2e(e - 1))]]",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 f(x)=e^{-x}, 점 P_n(n,f(n))·Q_n(n+1,f(n))·P_{n+1}, 삼각형 P_nP_{n+1}Q_n 음영(A_n), 선분과 곡선 사이 빗금(B_n), x축 n, n+1 표시"}}],
    confidence=0.8,
    note="[2005년 11월 고3 이과 미분과 적분 28번]. 같은 이미지에 id 2개. 점 Pₙ(n, f(n))·Qₙ(n+1, f(n))을 app(sub(P,n), n, f(n))·app(sub(Q,n), n+1, f(n))으로; 삼각형·선분의 가변 첨자 라벨은 sub 텍스트 혼합 유지. 그래프 unsupported(raw). 답 ⑤ 유지(빠른정답 4와 불일치는 초안대로)")

# 50. 25f6155a — p68: f′(x), g′(1) → app
add(id="25f6155a", qtype="choice",
    question="실수 전체의 집합에서 미분가능한 함수 [[f(x)]]의 도함수 [[app(prime(f), x)]]가 [[app(prime(f), x) = -x + pow(e, 1 - pow(x,2))]]이다.\n양수 [[t]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[point(t, f(t))]]에서의 접선과 곡선 [[y = f(x)]] 및 [[y]]축으로 둘러싸인 부분의 넓이를 [[g(t)]]라 하자. [[g(1) + app(prime(g), 1)]]의 값은?",
    choices=["[[frac(1,2) e + frac(1,2)]]", "[[frac(1,2) e + frac(2,3)]]", "[[frac(1,2) e + frac(5,6)]]", "[[frac(2,3) e + frac(1,2)]]", "[[frac(2,3) e + frac(2,3)]]"],
    figure=None, confidence=0.85,
    note="[2024년 11월 고3 미적분 28번/4점]. f′(x)·g′(1)을 app(prime(…), …)로 교체. 답 ② 유지(빠른정답 1과 불일치는 초안대로)")

# 51. f361ea75 — p69
add(id="f361ea75", qtype="choice",
    question="실수 전체의 집합에서 미분가능한 함수 [[f(x)]]의 도함수 [[app(prime(f), x)]]가 [[app(prime(f), x) = -3x + 2 pow(e, 4 - pow(x,2))]]이다.\n양수 [[t]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[point(t, f(t))]]에서의 접선과 곡선 [[y = f(x)]] 및 [[y]]축으로 둘러싸인 부분의 넓이를 [[g(t)]]라 하자. [[g(2) + app(prime(g), 2)]]의 값은?",
    choices=["[[frac(1,2) pow(e,4) + 21]]", "[[frac(1,2) pow(e,4) + 23]]", "[[frac(1,2) pow(e,4) + 25]]", "[[pow(e,4) + 21]]", "[[pow(e,4) + 23]]"],
    figure=None, confidence=0.85,
    note="[2024년 11월 고3 미적분 28번 변형]. f′(x)·g′(2)를 app(prime(…), …)로 교체. 답 ④ 유지(빠른정답 2와 불일치는 초안대로)")

# ---------------- 함수의 그래프 ----------------
# 52. 0ed5a4c1 — p46: (f∘g)(x) → app(comp(f, g), x); h″(−2)·f″(4) → app(prime(·, 2), ·); f′(4)·h′(−2) → app
add(id="0ed5a4c1", qtype="choice",
    question="두 함수 [[f(x)]], [[g(x)]]가 실수 전체의 집합에서 이계도함수를 갖고 [[g(x)]]가 증가함수일 때, 함수 [[h(x)]]를 [[h(x) = app(comp(f, g), x)]]라 하자.\n점 [[point(-2, 4)]]가 곡선 [[y = g(x)]]의 변곡점이고 [[frac(app(prime(h, 2), -2), app(prime(f, 2), 4)) = 9]]이다. [[app(prime(f), 4) = 2]]일 때, [[app(prime(h), -2)]]의 값은?",
    choices=["[[8]]", "[[7]]", "[[6]]", "[[5]]", "[[4]]"],
    figure=None, confidence=0.85,
    note="[2020년 7월 고3 이과 15번 변형]. 합성 적용과 도함수·이계도함수 적용을 app으로 교체. 답 ③ 유지(g′(−2)=3 → h′(−2)=6; 빠른정답 1과 불일치는 초안대로)")

# 53·54. 3c650603, 1998723c — p57(같은 이미지 id 2개): f′(x) → app. 그래프 unsupported → 통과
dup(["3c650603", "1998723c"], qtype="choice",
    question="실수 전체의 집합에서 함수 [[f(x)]]가 미분가능하고 도함수 [[app(prime(f), x)]]가 연속이다. [[x]]축과의 교점이 [[x]]좌표가 [[b]], [[c]], [[d]]뿐인 함수 [[g(x) = frac(app(prime(f), x), x)]]의 그래프가 그림과 같을 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. 함수 [[f(x)]]는 열린 구간 [[itv(c, 0, oo)]]에서 감소한다.\nㄴ. 함수 [[f(x)]]는 [[x = c]]에서 극댓값을 갖는다.\nㄷ. 함수 [[f(x)]]는 닫힌 구간 [[itv(a, e, cc)]]에서 3개의 극값을 갖는다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=g(x) 그래프. x<0에서 a<b<c<0, g는 a에서 양, b·c에서 x축 교차, (b,c)에서 음, x→0⁻에서 +∞; x>0에서 -∞로부터 증가, d에서 교차 후 양, e 부근 완만"}}],
    confidence=0.8,
    note="같은 이미지에 id 2개. f′(x)를 app(prime(f), x)로 교체. 그래프 unsupported(raw). 답 ⑤ 유지")

# 55. b5e1f806 — p58
add(id="b5e1f806", qtype="choice",
    question="실수 전체의 집합에서 함수 [[f(x)]]가 미분가능하고 도함수 [[app(prime(f), x)]]가 연속이다. [[x]]축과의 교점이 [[x]]좌표가 [[b]], [[c]], [[d]]뿐인 함수 [[g(x) = frac(app(prime(f), x), x)]]의 그래프가 그림과 같을 때, 옳은 것만을 <보기>에서 있는 대로 고른 것은?\n<보기>\nㄱ. 함수 [[f(x)]]는 열린 구간 [[itv(b, 0, oo)]]에서 증가한다.\nㄴ. 함수 [[f(x)]]는 [[x = b]]에서 극솟값을 갖는다.\nㄷ. 함수 [[f(x)]]는 닫힌 구간 [[itv(a, e, cc)]]에서 4개의 극값을 갖는다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=g(x) 그래프. x<0에서 a<b<0, g는 x<b에서 양(a 부근 극대), b에서 교차 후 음, x→0⁻에서 -∞; x>0에서 +∞로부터 감소, c에서 교차 후 음(극소), d에서 교차 후 양으로 증가, e 표시"}}],
    confidence=0.8,
    note="[2013년 7월 고3 이과 18번/4점]. f′(x)를 app(prime(f), x)로 교체. 그래프 unsupported(raw). 답 ③ 유지(빠른정답 5와 불일치는 초안대로)")

# 56. 10cc3277 — p74: 경우 나눔 → cases
add(id="10cc3277", qtype="choice",
    question="함수 [[f(x) = cases(pow(x - 1, 2) pow(e, x) + k, x >= 0, -pow(x,2), x < 0)]]에 대하여 함수 [[g(x) = abs(f(x)) - f(x)]]가 다음 조건을 만족하도록 하는 [[k]]의 값의 범위는?\n(가) 함수 [[g(x)]]는 모든 실수에서 연속이다.\n(나) 함수 [[g(x)]]는 미분가능하지 않은 점이 2개이다.",
    choices=["[[k < -2]]", "[[k <= -1]]", "[[k < 0]]", "[[-1 <= k < 0]]", "[[0 < k < 1]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로 교체. 답 ④ 유지(−1≤k<0; 빠른정답 1과 불일치는 초안대로)")

# ---------------- 음함수와 역함수의 미분법 ----------------
# 57. 01426115 — p76: 경우 나눔 → cases; g′(f(a+1)) → app(prime(g), f(a + 1))
add(id="01426115", qtype="choice",
    question="함수 [[f(x)]]가 [[f(x) = cases(pow(x - a - 1, 2) pow(e, x), x >= a, pow(e, 2a)(x - a) + pow(e, a), x < a)]]일 때,\n실수 [[t]]에 대하여 [[f(x) = t]]를 만족시키는 [[x]]의 최솟값을 [[g(t)]]라 하자. 함수 [[g(t)]]가 [[t = 4]]에서만 불연속일 때,\n[[frac(app(prime(g), f(a + 1)), app(prime(g), f(a + 7)))]]의 값은? (단, [[a]]는 상수이다.)",
    choices=["[[12 pow(e,6)]]", "[[16 pow(e,6)]]", "[[20 pow(e,6)]]", "[[12 pow(e,7)]]", "[[16 pow(e,7)]]"],
    figure=None, confidence=0.8,
    note="[2024년 6월 고3 미적분 28번 변형]. 경우 나눔을 cases로, g′(f(a+1))·g′(f(a+7))을 app(prime(g), …)로 교체. 답 ④ 유지(빠른정답 3과 불일치는 초안대로)")

# 58. 47035b70 — p92: h′(6) → app(prime(h), 6)
add(id="47035b70", qtype="short",
    question="[[0 < t < 10]]인 실수 [[t]]에 대하여\n곡선 [[y = pow(x,3) - 2 pow(x,2) - 8x + 6]]과 직선 [[y = t]]가 만나는 세 점 중에서 [[x]]좌표가 가장 큰 점의 좌표를 [[point(f(t), t)]], [[x]]좌표가 가장 작은 점의 좌표를 [[point(g(t), t)]]라 하자.\n[[h(t) = t × (f(t) - g(t))]]라 할 때, [[app(prime(h), 6)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="h′(6)을 app(prime(h), 6)으로 교체(원문 t·{f(t)−g(t)}는 t × (…)). 답 23/4 유지")

# ---------------- 합성함수의 미분법 ----------------
# 59. 8d0ae140 — p4: (g∘f)(x) → app(comp(g, f), x); g′(−2) → app
add(id="8d0ae140", qtype="short",
    question="미분가능한 두 함수 [[f(x)]], [[g(x)]]에 대하여 함수 [[h(x)]]를 [[h(x) = app(comp(g, f), x)]]라 하면\n[[lim(x, 1, frac(f(x) + 2, x - 1)) = 4]], [[lim(x, 1, frac(h(x) - 4, x - 1)) = 12]]일 때,\n[[g(-2) + app(prime(g), -2)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app(comp(g, f), x)로, g′(−2)를 app(prime(g), −2)로 교체. 답 7 유지(빠른정답 2와 불일치는 초안대로)")

# 60. d5c11572 — p40: 경우 나눔 → cases; (g∘f)(x) → app
add(id="d5c11572", qtype="short",
    question="두 함수\n[[f(x) = cases(a x - a + 2, x >= 1, x, x < 1)]], [[g(x) = abs(pow(3, x - 1) + b)]]\n에 대하여 함수 [[h(x)]]를 [[h(x) = app(comp(g, f), x)]]라 하자.\n[[h(x)]]가 [[x = 1]]에서 미분가능할 때, 상수 [[a]], [[b]]에 대하여 [[6 a b]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    note="경우 나눔을 cases로, 합성 적용을 app(comp(g, f), x)로 교체. 답 4 유지(b=−2, a=−1/3; 빠른정답 3과 불일치는 초안대로)")

# 61. 11453899 — p41
add(id="11453899", qtype="short",
    question="두 함수\n[[f(x) = cases(a x - 2a + 3, x >= 2, x, x < 2)]], [[g(x) = abs(pow(3, x) + b)]]\n에 대하여 함수 [[h(x) = app(comp(g, f), x)]]라 하자. [[h(x)]]가 [[x = 2]]에서 미분가능할 때, 상수 [[a]], [[b]]에 대하여 [[3a - b]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    note="경우 나눔을 cases로, 합성 적용을 app(comp(g, f), x)로 교체. 답 17 유지(b=−18, a=−1/3)")

# 62. 8a2c9861 — p42: (f∘g)(2) → app(comp(f, g), 2); (f∘g)′(2) → app(prime(comp(f, g)), 2)
add(id="8a2c9861", qtype="short",
    question="이차 이상의 다항함수 [[f(x)]]와 함수 [[g(x) = pow(e, -2 pow(x,2) + 4x)]]이 [[app(comp(f, g), 2) = 1]], [[app(prime(comp(f, g)), 2) = -4]]를 만족한다.\n다항식 [[f(x)]]를 [[pow(x - 1, 2)]]으로 나누었을 때의 나머지를 [[R(x)]]라 할 때, [[R(3)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="(f∘g)(2)→app(comp(f, g), 2), (f∘g)′(2)→app(prime(comp(f, g)), 2). 답 3 유지(R(x)=x; 빠른정답 1과 불일치는 초안대로)")

# 63. c717ed73 — p43
add(id="c717ed73", qtype="short",
    question="이차 이상의 다항함수 [[f(x)]]와 함수 [[g(x) = pow(e, sin(x))]]이 [[app(comp(f, g), 0) = 1]], [[app(prime(comp(f, g)), 0) = 4]]를 만족한다.\n다항식 [[f(x)]]를 [[pow(x - 1, 2)]]으로 나눌 때의 나머지를 [[R(x)]]라 할 때, [[R(2)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="(f∘g)(0)→app(comp(f, g), 0), (f∘g)′(0)→app(prime(comp(f, g)), 0). 답 5 유지(R(x)=4x−3; 빠른정답 4와 불일치는 초안대로)")

# 64. 48c7503b — p44
add(id="48c7503b", qtype="choice",
    question="이차 이상의 다항함수 [[f(x)]]와 함수 [[g(x) = pow(e, sin(x))]]에 대하여 [[app(comp(f, g), 0) = 2]], [[app(prime(comp(f, g)), 0) = 1]]이 성립한다.\n다항식 [[f(x)]]를 [[pow(x - 1, 2)]]으로 나누었을 때의 나머지를 [[R(x)]]라 할 때, [[R(3)]]의 값은?",
    choices=["[[frac(1,4)]]", "[[frac(1,3)]]", "[[2]]", "[[3]]", "[[4]]"],
    figure=None, confidence=0.85,
    note="(f∘g)(0)→app(comp(f, g), 0), (f∘g)′(0)→app(prime(comp(f, g)), 0). 답 ⑤ 유지(R(x)=x+1 → 4; 빠른정답 17과 불일치는 초안대로)")

# 65. af1a0cdf — p47: (f∘g)(x) → app; h′(0) → app
add(id="af1a0cdf", qtype="short",
    question="두 함수 [[f(x) = k pow(x,3) - 3x]], [[g(x) = pow(e, -x) + 2]]가 있다.\n함수 [[h(x) = app(comp(f, g), x)]]에 대하여 [[app(prime(h), 0) = 30]]일 때,\n상수 [[-50k]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2017년 7월 고3 이과 25번 변형]. 합성 적용을 app(comp(f, g), x)로, h′(0)을 app(prime(h), 0)으로 교체. 답 50 유지(k=−1)")

# 66. f494e030 — p52: 100f′(e) → 100 app(prime(f), e)
add(id="f494e030", qtype="short",
    question="양의 실수 전체의 집합에서 미분가능한 함수 [[f(x)]]에 대하여 함수 [[g(x)]]를\n[[g(x) = f(x) ln(pow(x,4))]]\n이라 하자. 곡선 [[y = f(x)]] 위의 점 [[point(e, -e)]]에서의 접선과 곡선 [[y = g(x)]] 위의 점 [[point(e, -4e)]]에서의 접선이 서로 수직일 때, [[100 app(prime(f), e)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2014년 6월 고3 이과 26번/4점]. f′(e)를 app(prime(f), e)로 교체. 답 50 유지(f′(e)=1/2)")

# 67. 5f989a4c — p63: S′(θ) → app(prime(S), theta). 도형 unsupported → 통과
add(id="5f989a4c", qtype="short",
    question="다음 그림과 같이 기울기가 양수인 직선 [[y = (x - 2) tan(theta)]] 위의 두 점 A, B에 대하여 삼각형 OAB가 [[seg(OA) = seg(OB) = 4]]인 이등변삼각형일 때, 삼각형 OAB의 넓이를 [[S(theta)]]라 하자. [[lim(theta, 0, app(prime(S), theta), +)]]의 값을 구하시오. (단, O는 원점이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O, 직선 y=(x-2)tanθ 위의 두 점 A(제3사분면)·B(제1사분면), 삼각형 OAB 음영"}}],
    confidence=0.8,
    note="S′(θ)를 app(prime(S), theta)로 교체. 도형 unsupported(raw). 답 8 유지(빠른정답 4와 불일치는 초안대로 — 옆 문항 p65의 답)")

# 68. 8a792e27 — p65
add(id="8a792e27", qtype="short",
    question="다음 그림과 같이 기울기가 양수인 직선 [[y = (x - 1) tan(theta)]] 위의 두 점 A, B에 대하여 삼각형 OAB가 [[seg(OA) = seg(OB) = 4]]인 이등변삼각형일 때, 삼각형 OAB의 넓이를 [[S(theta)]]라 하자. [[lim(theta, 0, app(prime(S), theta), +)]]의 값을 구하시오. (단, O는 원점이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O, 직선 y=(x-1)tanθ 위의 두 점 A(제3사분면)·B(제1사분면), 삼각형 OAB 음영"}}],
    confidence=0.8,
    note="S′(θ)를 app(prime(S), theta)로 교체. 도형 unsupported(raw). 답 4 유지")

# 69. 520f5756 — p98: f′(3) → app(prime(f), 3)
add(id="520f5756", qtype="choice",
    question="함수 [[f(x) = 9 pow(x, sqrt(3))]] ([[x > 0]])에 대하여 [[app(prime(f), 3) = pow(3, k)]]일 때, [[k = a + b sqrt(3)]]이다. 유리수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?",
    choices=["[[frac(3,2)]]", "[[2]]", "[[frac(5,2)]]", "[[3]]", "[[frac(7,2)]]"],
    figure=None, confidence=0.85,
    note="f′(3)을 app(prime(f), 3)으로 교체. 답 ③ 유지(k=3/2+√3)")

# ================= esc_sonnet_h3-2_2of4 =================
# ---------------- 매개변수로 나타낸 함수의 미분법 ----------------
# 70. 9dd19ec9 — p51: g′(a) → app(prime(g), a). 도형 unsupported → 통과
add(id="9dd19ec9", qtype="short",
    question="[[0 < t < frac(pi,2)]]인 실수 [[t]]에 대하여 점 [[point(t, 0)]]을 P라 하고, 곡선 [[y = tan(x)]] 위의 점 Q를 점 Q에서의 접선의 기울기가 직선 PQ의 기울기와 같도록 잡는다. 원점 O에 대하여 삼각형 OPQ의 외접원이 [[y]]축과 만나는 점 중 원점이 아닌 점을 R이라 하자. 점 Q의 [[x]]좌표를 [[f(t)]], 점 R의 [[y]]좌표를 [[g(t)]]라 하자. [[tan(f(a)) = 3]]을 만족시키는 상수 [[a]]에 대하여 [[f(a) + 3 app(prime(g), a) = frac(q,p)]]일 때, [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=tan x, x축 위의 점 P, 곡선 위의 점 Q, 원점 O·P·Q를 지나는 외접원, 외접원과 y축의 교점 R"}}],
    confidence=0.8,
    note="g′(a)를 app(prime(g), a)로 교체. 도형 unsupported(raw). 답 107 유지")

# 71. e34bc085 — p52: 경우 나눔 → cases; α(t), β(t) → alpha(t), beta(t)
add(id="e34bc085", qtype="choice",
    question="양의 실수 [[t]]와 함수 [[f(x) = cases(pow(x,2), x < 0, log(2, x + 1), x >= 0)]]에 대하여 직선 [[y = -x + t]]가 함수 [[y = f(x)]]의 그래프와 만나는 두 점의 [[x]]좌표를 각각 [[alpha(t)]], [[beta(t)]] ([[alpha(t) > 0]], [[beta(t) < 0]])이라 하자.\n매개변수 [[t]] ([[t > 0]])으로 나타낸 곡선 [[x = alpha(t)]], [[y = beta(t)]]에 대하여 [[x = 1]]에 대응하는 점에서의 접선의 기울기는?",
    choices=["[[-frac(2 ln(2) + 1, 6 ln(2))]]", "[[-frac(3 ln(2) + 1, 6 ln(2))]]", "[[-frac(4 ln(2) + 1, 6 ln(2))]]", "[[-frac(6 ln(2) + 1, 12 ln(2))]]", "[[-frac(8 ln(2) + 1, 12 ln(2))]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 그리스 문자 함수 α(t)·β(t)를 alpha(t)·beta(t)로 교체. 답 ① 유지")

# 72. d491e948 — p56: 문법 문제 없음(단독 점 이름 C′는 텍스트, 좌표는 point). 도형 unsupported → 통과
add(id="d491e948", qtype="short",
    question="다음 그림과 같이 좌표평면 위의 두 점 [[A(2, 0)]], [[B(3, 0)]]을 잇는 선분을 한 변으로 하는 정사각형 ABCD가 있다. 이 정사각형을 꼭짓점 B를 중심으로 시곗바늘이 도는 방향으로 [[theta]] ([[0 < theta < frac(pi,2)]])만큼 회전시켰을 때, 점 C가 이동한 점을 C′[[point(x, y)]]라 하자.\n점 C′의 자취의 방정식을 매개변수 [[theta]]로 나타낼 때, [[sin(theta) = frac(sqrt(5), 5)]]일 때의 [[dydx(y,x)]]의 값을 [[p]]라 하자.\n이때 [[frac(1, pow(p,2))]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: x축 위 A, B와 정사각형 ABCD, 점 B를 중심으로 θ만큼 시계 방향 회전한 정사각형과 점 C′"}}],
    confidence=0.85,
    note="프라임 점 C′는 단독 점 이름이라 텍스트로 두고 좌표만 point(x, y)로 — 문법 문제 없음, 도형 unsupported(raw)만 남음 → 통과. 답 4 유지")

# ---------------- 부피 ----------------
# 73. 7e47303c — p36: 경우 나눔 → cases. 입체 도형 unsupported → 통과
add(id="7e47303c", qtype="choice",
    question="다음 그림과 같이 함수\n[[f(x) = cases(2 pow(e,-x), x < 0, sqrt(ln(x + 1) + 4), x >= 0)]]\n의 그래프 위의 점 [[P(x, f(x))]]에서 [[x]]축에 내린 수선의 발을 H라 하고, 선분 PH를 한 변으로 하는 정사각형을 [[x]]축에 수직인 평면 위에 그린다. 점 P의 [[x]]좌표가 [[x = -ln(3)]]에서 [[x = e - 1]]까지 변할 때, 이 정사각형이 만드는 입체도형의 부피는?",
    choices=["[[3e + 10]]", "[[3e + 13]]", "[[3e + 16]]", "[[4e + 10]]", "[[4e + 13]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "입체도형 그림: x축 위 −ln3에서 e−1까지, 곡선 y=2e^{−x}(x<0)·y=√(ln(x+1)+4)(x≥0) 위의 점 P와 수선의 발 H, 선분 PH를 한 변으로 하는 정사각형 단면들(x축에 수직), 원점 O와 높이 1 표시"}}],
    confidence=0.85,
    note="[2016년 3월 고3 이과 20번 변형]. 경우 나눔을 cases로 교체. 입체 도형 unsupported(raw, 이 문항 수치로 설명 정리). 답 ⑤ 유지(4e+13)")

# 74. 1013c739 — p59
add(id="1013c739", qtype="choice",
    question="그림과 같이 함수\n[[f(x) = cases(pow(e,-x), x < 0, sqrt(ln(x + 1) + 1), x >= 0)]]\n의 그래프 위의 점 [[P(x, f(x))]]에서 [[x]]축에 내린 수선의 발을 H라 하고, 선분 PH를 한 변으로 하는 정사각형을 [[x]]축에 수직인 평면 위에 그린다. 점 P의 [[x]]좌표가 [[x = -ln(2)]]에서 [[x = e - 1]]까지 변할 때, 이 정사각형이 만드는 입체도형의 부피는?",
    choices=["[[e - frac(3,2)]]", "[[e + frac(2,3)]]", "[[2e - frac(3,2)]]", "[[e + frac(3,2)]]", "[[2e - frac(2,3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "입체도형 그림: x축 위 −ln2에서 e−1까지, 곡선 y=e^{−x}(x<0)·y=√(ln(x+1)+1)(x≥0) 위의 점 P와 수선의 발 H, 선분 PH를 한 변으로 하는 정사각형 단면들(x축에 수직), 원점 O와 높이 1 표시"}}],
    confidence=0.85,
    note="[2016년 3월 고3 이과 20번/4점]. 경우 나눔을 cases로 교체. 입체 도형 unsupported(raw). 답 ④ 유지(e+3/2; 빠른정답 1과 불일치는 초안대로)")

# 75. 81991cda — p63
add(id="81991cda", qtype="choice",
    question="다음 그림과 같이\n함수 [[f(x) = cases(pow(e, -frac(x,2)), x < 0, sqrt(ln(x + pow(e,2)) - 1), x >= 0)]]의 그래프\n위의 점 [[P(x, f(x))]]에서 [[x]]축에 내린 수선의 발을 H라 하고, 선분 PH를 한 변으로 하는 정사각형을 [[x]]축에 수직인 평면 위에 그린다. 점 P의 [[x]]좌표가 [[x = -ln(4)]]에서 [[x = pow(e,3) - pow(e,2)]]까지 변할 때, 이 정사각형이 만드는 입체도형의 부피는?",
    choices=["[[pow(e,3) - 3]]", "[[pow(e,3) - 1]]", "[[pow(e,3) + 3]]", "[[2pow(e,3) + 1]]", "[[2pow(e,3) + 3]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "입체도형 그림: x축 위 −ln4에서 e³−e²까지, 곡선 y=e^{−x/2}(x<0)·y=√(ln(x+e²)−1)(x≥0) 위의 점 P와 수선의 발 H, 선분 PH를 한 변으로 하는 정사각형 단면들(x축에 수직), 원점 O와 높이 1 표시"}}],
    confidence=0.85,
    note="경우 나눔을 cases로 교체. 입체 도형 unsupported(raw). 답 ③ 유지(e³+3)")

# ---------------- 속도와 가속도 ----------------
# 76. 27c8d446 — p99: 문법 문제 없음. 한 이미지에 별개 문항 2개(id 1개) → 보류 유지
add(id="27c8d446", qtype="short",
    question="좌표평면 위를 움직이는 점 P의 시각 [[t]]에서의\n위치 [[point(x, y)]]가\n[[x = cos(t)]], [[y = 2 pow(sin(t), 2)]] ([[0 <= t <= frac(pi,2)]])이다. 점 P의\n위치가 [[point(0, 2)]]일 때, 가속도의 크기를 구하시오.",
    choices=None, figure=None, confidence=0.8,
    needs_review="같은 이미지에 별개 문항 2개(위: 전사함 — 빠른정답 4와 일치 / 아래: id 미배정 — 점 P(x, y)의 위치 x=2t²−3t, y=kt³+t, t=1에서 가속도의 크기가 √52일 때 양수 k는? 선지 ①1 ②2 ③3 ④4 ⑤5, 답 ① k=1)인데 id 1개 — 위 문항만 전사",
    note="위 문항은 v1.5 문법 문제 없음. 답 4 유지(t=π/2에서 |가속도|=4)")

# ---------------- 급수 ----------------
# 77. 6546a330 — p20: 줄임표 든 분수 → frac(… + cdots + …, … + cdots + …)
add(id="6546a330", qtype="choice",
    question="공차가 양수인 등차수열 [[set(sub(a,n))]]이 다음 조건을 만족시킨다.\n(가) 모든 자연수 [[n]]에 대하여\n[[frac(sub(a,1) + sub(a,2) + sub(a,3) + cdots + sub(a, 2n - 1) + sub(a, 2n), sub(a,1) + sub(a,2) + sub(a,3) + cdots + sub(a, n - 1) + sub(a,n))]]은 일정한 값을 가진다.\n(나) [[sum(n, 1, inf, frac(2, (2n + 1) sub(a,n))) = frac(1,10)]]\n[[sub(a,10)]]의 값은?",
    choices=["[[190]]", "[[192]]", "[[194]]", "[[196]]", "[[198]]"],
    figure=None, confidence=0.85,
    note="[2018년 9월 고2 문과 21번/4점]. 줄임표가 든 분수를 frac 안에 cdots로 한 마커로 교체. 답 ① 유지(d=20 → a₁₀=190; 빠른정답 12와 불일치는 초안대로)")

# 78. 191255af — p88: Aₙ(n, 0) → app(sub(A,n), n, 0); 선분 AₙBₙ·AₙCₙ(윗줄)은 가변 첨자라 sub 병치(윗줄 생략). 도형 unsupported → 통과
add(id="191255af", qtype="short",
    question="다음 그림과 같이 좌표평면 위의 점 [[app(sub(A,n), n, 0)]]에서\n원 [[pow(x,2) + pow(y - n, 2) = 1]]에 두 접선을 그어 만나는 점을 각각\n[[sub(B,n)]], [[sub(C,n)]]이라 하자. [[sub(a,n) = sub(A,n) sub(B,n) + sub(A,n) sub(C,n)]]이라 할 때,\n[[sum(n, 3, inf, frac(16, pow(sub(a,n), 2) + 24n + 20))]]의 값을 구하시오.\n(단, [[n]]은 2보다 큰 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원 x²+(y−n)²=1, x축 위의 점 Aₙ(n, 0)에서 원에 그은 두 접선과 접점 Bₙ, Cₙ"}}],
    confidence=0.8,
    note="점 Aₙ(n, 0)을 app(sub(A,n), n, 0)으로; 접선 길이 AₙBₙ·AₙCₙ의 윗줄은 가변 첨자라 seg로 못 써 sub 병치 유지(윗줄 생략, 길이 뜻 동일). 도형 unsupported(raw). 답 1/2 유지")

# ---------------- 등비수열의 극한 ----------------
# 79. b1c78d01 — p68: 문법 문제 없음(가변 첨자 라벨 Oₙ·Pₙ·Qₙ은 sub 텍스트 혼합으로 파싱). 도형 unsupported → 통과
add(id="b1c78d01", qtype="short",
    question="그림과 같이 한 변의 길이가 4인 정삼각형 ABC와\n점 A를 지나고 직선 BC와 평행한 직선 [[l]]이 있다.\n자연수 [[n]]에 대하여 중심 [[sub(O,n)]]이 변 AC 위에 있고\n반지름의 길이가 [[sqrt(3) pow(frac(1,2), n - 1)]]인 원이\n직선 AB와 직선 [[l]]에 모두 접한다. 이 원과 직선 AB가\n접하는 점을 [[sub(P,n)]], 직선 [[sub(O,n) sub(P,n)]]과 직선 [[l]]이 만나는 점을\n[[sub(Q,n)]]이라 하자. 삼각형 B[[sub(O,n)]][[sub(Q,n)]]의 넓이를 [[sub(S,n)]]이라 할 때,\n[[lim(n, inf, pow(2,n) sub(S,n)) = k]]이다. [[pow(k,2)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 ABC(B 왼쪽 아래, C 오른쪽 아래, A 위), A를 지나 BC와 평행한 직선 l, 변 AC 위 중심 Oₙ의 원(AB·l에 접함), AB 위 접점 Pₙ, 직선 OₙPₙ과 l의 교점 Qₙ, 삼각형 BOₙQₙ"}}],
    confidence=0.8,
    note="[2016년 7월 고3 문과 29번/4점]. 가변 첨자 점 라벨(직선 OₙPₙ, 삼각형 BOₙQₙ)은 sub 텍스트 혼합으로 파싱되어 문법 문제 없음, 도형 unsupported(raw)만 남음 → 통과. 답 192 유지(빠른정답 4와 불일치는 초안대로)")
