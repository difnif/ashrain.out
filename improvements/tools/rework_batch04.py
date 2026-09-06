# -*- coding: utf-8 -*-
# batch04 (63문항: esc_sonnet_h2-2_2of3 41, esc_sonnet_h2-2_3of3 6, esc_opus_h3-1_1of1 2, esc_sonnet_h3-1_1of2 14) — v1.5 문법 재작업
# 핵심 교체: f′(x)→app(prime(f), x) / 조각적 정의→cases(식, 조건, …)('또는' 구간은 같은 식 두 쌍) / (f∘f)(x)→app(comp(f,f), x)
#            첨자 함수 v₁(t)·Fₙ(x)→app(sub(v,1), t)·app(sub(F,n), x) / 빈칸→box(n)(식 안) / p̂→hat(p) / σ→sigma, σ₁→sub(sigma,1), σ_A²→pow(sub(sigma,A),2)
# 도형(그래프·정규분포곡선)은 unsupported(raw) 유지 — 도형만 남은 항목은 통과
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= esc_sonnet_h2-2_2of3 =================
# ---------------- 평균값 정리 ----------------
# 0. 19250d01 — p73: f′(c) → app(prime(f), c)
add(id="19250d01", qtype="choice",
    question="[[frac(f(1) - f(-1), 2) = app(prime(f), c)]]인 [[c]]가 열린구간 [[itv(-1, 1, oo)]]에\n존재하는 함수인 것만을 보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(x) = -pow(x,2) abs(x)]]\nㄴ. [[f(x) = sqrt(pow(x + 4, 2))]]\nㄷ. [[f(x) = pow(x,2) - 2 abs(x)]]",
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="f′(c)를 app(prime(f), c)로 교체. 답 ④ 유지")

# 1. 3e73cc1a — p74: f′(c) → app(prime(f), c)
add(id="3e73cc1a", qtype="choice",
    question="[[frac(f(1) - f(-1), 2) = app(prime(f), c)]]인 [[c]]가 열린구간 [[itv(-1, 1, oo)]]에\n존재하는 함수인 것만을 보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(x) = -x abs(x)]]\nㄴ. [[f(x) = -sqrt(x + 2)]]\nㄷ. [[f(x) = x + sqrt(pow(x,2))]]",
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="f′(c)를 app(prime(f), c)로 교체. 답 ④ 유지")

# 2. 11ff3746 — p75: 경우 나눔 → cases
add(id="11ff3746", qtype="short",
    question="[[f(x) = cases(pow(x,2) - 8x + 16, x >= 0, -pow(x,2) - 8x + 16, x < 0)]]에 대하여\n닫힌구간 [[itv(-5, 6, cc)]]에서 평균값의 정리를 만족시키는\n상수 [[c]]의 개수를 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로 교체. 답 2 유지(빠른정답 3과 불일치는 초안대로)")

# 3. 78ea83e8 — p92: f′(c) → app. 그래프 unsupported → 통과
add(id="78ea83e8", qtype="choice",
    question="함수 [[y = f(x)]]의 그래프가 다음 그림과 같을 때,\n[[frac(f(b) - f(a), b - a) = app(prime(f), c)]]\n를 만족시키는 상수 [[c]]의 개수는? (단, [[a < c < b]])",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 곡선 y=f(x): x=a(원점 왼쪽)에서 점 찍고 올라가 극대, 내려가 극소(원점 오른쪽), 다시 올라가 극대(b 직전) 후 x=b에서 점 찍고 급감; 두 점 (a,f(a)), (b,f(b))를 잇는 직선, a·b에서 x축까지 점선"}}],
    confidence=0.8,
    note="f′(c)를 app(prime(f), c)로 교체, 그래프는 unsupported(raw). 답 ③ 유지(그래프 판독 기반, 빠른정답 5와 불일치는 초안대로)")

# ---------------- 함수의 연속 ----------------
# 4. df171387 — p7: 선지 ③④⑤ 경우 나눔 → cases
add(id="df171387", qtype="choice",
    question="다음 중 [[x = 1]]에서 연속인 함수는?\n(단, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)",
    choices=["[[f(x) = 4 pow(floor(x), 2)]]", "[[f(x) = frac(1, x - 1)]]",
             "[[f(x) = cases(pow(x - 1, 2), x != 1, 1, x = 1)]]",
             "[[f(x) = cases(frac(pow(x,2) - 1, x - 1), x != 1, 2, x = 1)]]",
             "[[f(x) = cases(frac(4 abs(x - 1), x - 1), x != 1, 4, x = 1)]]"],
    figure=None, confidence=0.85,
    note="선지의 경우 나눔을 cases로 교체. 답 ④ 유지(빠른정답 2와 불일치는 초안대로)")

# 5·6. 0c3d90f2, 159ea7cc — p8(같은 이미지 id 2개): 선지 ③④⑤ 경우 나눔 → cases
dup(["0c3d90f2", "159ea7cc"], qtype="choice",
    question="다음 중 [[x = 2]]에서 불연속인 함수를 모두 고르면?\n(단, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)\n(정답 3개)",
    choices=["[[f(x) = x abs(x - 2)]]", "[[f(x) = x - floor(x)]]",
             "[[f(x) = cases(frac(pow(x,2) + 2x - 8, pow(x,2) - 2x), x != 2, 3, x = 2)]]",
             "[[f(x) = cases(pow(x - 2, 2) + 3, x != 2, 2, x = 2)]]",
             "[[f(x) = cases(frac(abs(x - 2), x - 2), x != 2, 1, x = 2)]]"],
    derived_answer="②, ④, ⑤",
    figure=None, confidence=0.85,
    note="선지의 경우 나눔을 cases로 교체. 답 ②, ④, ⑤ 유지(정답 3개 문항; 빠른정답 5는 그중 하나)")

# 7. 2bfb83cb — p10: 선지 ④⑤ 경우 나눔 → cases
add(id="2bfb83cb", qtype="choice",
    question="다음 중 [[x = 0]]에서 연속인 함수는?",
    choices=["[[f(x) = -frac(3, pow(x,2))]]", "[[f(x) = sqrt(x + 1)]]", "[[f(x) = frac(10, x) - 9]]",
             "[[f(x) = cases(frac(abs(x), x), x != 0, 1, x = 0)]]",
             "[[f(x) = cases(pow(x,2) - 1, x >= 0, -pow(x,2) + 2, x < 0)]]"],
    figure=None, confidence=0.85,
    note="선지의 경우 나눔을 cases로 교체. 답 ② 유지")

# 8. 3e19ea11 — p11: 보기 ㄷ 경우 나눔 → cases
add(id="3e19ea11", qtype="choice",
    question="모든 실수 [[x]]에서 연속인 함수인 것만을 보기에서 있는 대로\n고른 것은?\n<보기>\nㄱ. [[f(x) = pow(x,2) abs(x)]]\nㄴ. [[f(x) = frac(2 pow(x,2) + 5x - 3, x + 3)]]\nㄷ. [[f(x) = cases(frac(pow(x,2) + 5x + 6, x + 2), x != -2, 1, x = -2)]]",
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ"],
    figure=None, confidence=0.85,
    note="보기 ㄷ의 경우 나눔을 cases로 교체. 답 ⑤ 유지")

# 9. 8ba42773 — p12: 경우 나눔 → cases
add(id="8ba42773", qtype="choice",
    question="[[a > 2]]인 상수 [[a]]에 대하여 함수 [[f(x)]]를\n[[f(x) = cases(pow(x,2) - 4x + 3, x <= 2, -pow(x,2) + a x, x > 2)]]라 하자.\n최고차항의 계수가 1인 삼차함수 [[g(x)]]에 대하여\n실수 전체의 집합에서 연속인 함수 [[h(x)]]가\n다음 조건을 만족시킬 때, [[h(1) + h(3)]]의 값은?\n(가) [[x != 1]], [[x != a]]일 때, [[h(x) = frac(g(x), f(x))]]이다.\n(나) [[h(1) = h(a)]]",
    choices=["[[-frac(15,6)]]", "[[-frac(7,3)]]", "[[-frac(13,6)]]", "[[-2]]", "[[-frac(11,6)]]"],
    figure=None, confidence=0.85,
    note="[2022년 3월 고3 12번/4점]. 경우 나눔을 cases로 교체. 답 ③ 유지")

# 10·11. c18d0ca1, 710ca9ce — p13(같은 이미지 id 2개): 경우 나눔 → cases
dup(["c18d0ca1", "710ca9ce"], qtype="choice",
    question="[[a > 3]]인 상수 [[a]]에 대하여 함수 [[f(x)]]를\n[[f(x) = cases(pow(x,2) - 6x + 5, x <= 3, -pow(x,2) + a x, x > 3)]]이라 하자.\n최고차항의 계수가 1인 삼차함수 [[g(x)]]에 대하여\n실수 전체의 집합에서 연속인 함수 [[h(x)]]가\n다음 조건을 만족시킬 때, [[h(1) + h(5)]]의 값은?\n(가) [[x != 1]], [[x != a]]일 때, [[h(x) = frac(g(x), f(x))]]이다.\n(나) [[h(1) = h(a)]]",
    choices=["[[-frac(21,5)]]", "[[-frac(41,10)]]", "[[-4]]", "[[-frac(39,10)]]", "[[-frac(19,5)]]"],
    figure=None, confidence=0.85,
    note="[2022년 3월 고3 12번 변형]. 경우 나눔을 cases로 교체. 답 ② 유지")

# 12. 184c1695 — p16: 선지 ④⑤ 경우 나눔 → cases
add(id="184c1695", qtype="choice",
    question="다음 중 [[x = -1]]에서 연속인 함수는?\n(단, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)",
    choices=["[[f(x) = sqrt(x)]]", "[[f(x) = pow(floor(x), 2)]]", "[[f(x) = frac(2, x + 1)]]",
             "[[f(x) = cases(frac(3 abs(x + 1), x + 1), x != -1, 0, x = -1)]]",
             "[[f(x) = cases(frac(pow(x,2) - 1, x + 1), x != -1, -2, x = -1)]]"],
    figure=None, confidence=0.85,
    note="선지의 경우 나눔을 cases로 교체. 답 ⑤ 유지(빠른정답 2와 불일치는 초안대로)")

# 13. e22e754a — p39: 경우 나눔 → cases, (f∘f)(x) → app. 보기 ㄱㄴㄷ가 그래프라 여전히 보류
add(id="e22e754a", qtype="choice",
    question="닫힌구간 [[itv(0, 4, cc)]]에서 정의된 함수 [[y = f(x)]]에 대하여\n함수 [[g(x)]]를 [[g(x) = cases(pow(f(x), 2), 0 <= x <= 2, app(comp(f, f), x), 2 < x <= 4)]]\n라 하자. 다음 보기 중 함수 [[g(x)]]가 닫힌구간 [[itv(0, 4, cc)]]에서\n불연속이 되도록 하는 함수 [[y = f(x)]]의 그래프로 옳은\n것만을 있는 대로 고른 것은?\n<보기>\nㄱ. (그래프 ㄱ)\nㄴ. (그래프 ㄴ)\nㄷ. (그래프 ㄷ)",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=[{"fn": "unsupported", "args": {"raw": "보기 그래프 3개(모두 [0,4] 위의 y=f(x), 격자 점선). ㄱ: (0,3)에서 감소해 (1,1), (2,0)에서 최소, (3,2) 극대, (4,1)까지 연속. ㄴ: (0,0)에서 (1,1) 극대, (2,0) 최소, 증가해 (3,2)(채운 점), x=3에서 (3,3) 빈 점부터 (4,4)까지 증가. ㄷ: (0,3)에서 감소해 (1,1), 1.5에서 0 최소, (2,1), (3,2)(채운 점), x=3에서 (3,3) 빈 점부터 (4,4)까지 증가"}}],
    confidence=0.7,
    needs_review="보기 ㄱ·ㄴ·ㄷ가 함수 y=f(x)의 그래프 3개 — 문법·텍스트로 표현 불가(설명문으로 대체)",
    note="경우 나눔을 cases로, (f∘f)(x)를 app(comp(f, f), x)로 교체. 답 ⑤ 유지(그래프 판독 기반)")

# 14. 940a9d3b — p40: 경우 나눔 2개(3구간·2구간) → cases
add(id="940a9d3b", qtype="choice",
    question="실수 전체의 집합에서 정의된 두 함수\n[[f(x) = cases(2, x > -1, 1, x = -1, 0, x < -1)]], [[g(x) = cases(frac(abs(x + 1), x + 1), x != -1, 0, x = -1)]]\n에 대하여 옳은 것만을 보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(f(x))]]는 실수 전체의 집합에서 연속이다.\nㄴ. [[lim(x, -1, f(g(x)))]]의 값이 존재한다.\nㄷ. [[g(f(x))]]는 [[x = -1]]에서 연속이다.",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="두 경우 나눔을 cases로 교체. 답 ④ 유지(빠른정답 5와 불일치는 초안대로)")

# 15. 12ccfc71 — p52: 경우 나눔 → cases
add(id="12ccfc71", qtype="choice",
    question="함수\n[[f(x) = cases(a x - 9, x <= 2, 3x - a, x > 2)]]\n가 실수 전체의 집합에서 연속일 때, 상수 [[a]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    figure=None, confidence=0.85,
    note="[2016년 4월 고3 문과 6번 변형]. 경우 나눔을 cases로 교체. 답 ⑤ 유지")

# 16. 8f41c800 — p57: 경우 나눔 → cases
add(id="8f41c800", qtype="short",
    question="함수 [[f(x) = cases(-2x + 4, x < 1, pow(x,2) + a x - 3, x >= 1)]]이 실수 전체의\n집합에서 연속일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2017년 7월 고3 문과 24번 변형]. 경우 나눔을 cases로 교체. 답 4 유지")

# 17. 697cb4d0 — p59: 경우 나눔 → cases
add(id="697cb4d0", qtype="choice",
    question="함수 [[f(x) = cases(2 pow(x,2) - 3x + 4, x < 3, x + a, x >= 3)]]이 실수 전체의\n집합에서 연속일 때, 상수 [[a]]의 값은?",
    choices=["[[4]]", "[[6]]", "[[8]]", "[[10]]", "[[12]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로 교체. 답 ④ 유지(빠른정답 −3과 불일치는 초안대로)")

# 18. 41d7b923 — p61: 경우 나눔 → cases
add(id="41d7b923", qtype="choice",
    question="함수 [[f(x) = cases(a x - 4, x < 1, 2x - a, x >= 1)]]이 실수 전체의 집합에서\n연속일 때, 상수 [[a]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    figure=None, confidence=0.85,
    note="[2016년 4월 고3 문과 6번/3점]. 경우 나눔을 cases로 교체. 답 ③ 유지")

# 19. 765905e6 — p66: 경우 나눔('x<−3 또는 x≥0'은 f(x) 두 쌍으로 분리) → cases 3쌍
add(id="765905e6", qtype="choice",
    question="최고차항의 계수가 1이고 [[f(-3) = f(0)]]인\n삼차함수 [[f(x)]]에 대하여 함수 [[g(x)]]를\n[[g(x) = cases(f(x), x < -3, f(x), x >= 0, -f(x), -3 <= x < 0)]]\n이라 하자. 함수 [[g(x) g(x - 3)]]이 [[x = k]]에서 불연속인\n실수 [[k]]의 값이 한 개일 때, <보기>에서 옳은 것만을 있는\n대로 고른 것은?\n<보기>\nㄱ. 함수 [[g(x) g(x - 3)]]은 [[x = 0]]에서 연속이다.\nㄴ. [[f(-6) × f(3) = 0]]\nㄷ. 함수 [[g(x) g(x - 3)]]이 [[x = k]]에서 불연속인\n실수 [[k]]가 음수일 때\n집합 { [[x]] | [[f(x) = 0]], [[x]]는 실수 }의 모든 원소의\n합이 [[-1]]이면 [[g(-1) = -48]]이다.",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2023년 7월 고3 14번/4점]. 경우 나눔을 cases로(원문 'f(x) (x<−3 또는 x≥0)'는 x<−3과 x≥0 두 쌍으로 분리). 답 ⑤ 유지(빠른정답 11은 값 아님)")

# 20. df4992ae — p67: 경우 나눔 → cases
add(id="df4992ae", qtype="short",
    question="함수\n[[f(x) = cases(x(x - 2), x <= 1, x(x - 2) + 16, x > 1)]]\n에 대하여 함수 [[f(x)(f(x) - a)]]가 실수 전체의 집합에서\n연속이 되도록 하는 상수 [[a]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2018년 6월 고2 이과 27번/4점]. 경우 나눔을 cases로 교체. 답 14 유지")

# 21. e94ee10e — p69: 경우 나눔 → cases
add(id="e94ee10e", qtype="choice",
    question="함수 [[f(x) = cases(-2x + 6, x < a, 2x - a, x >= a)]]에 대하여\n함수 [[pow(f(x), 2)]]이 실수 전체의 집합에서 연속이 되도록\n하는 모든 상수 [[a]]의 값의 합은?",
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    figure=None, confidence=0.85,
    note="[2021년 6월 고3 8번/3점]. 경우 나눔을 cases로 교체. 답 ④ 유지(빠른정답 5와 불일치는 초안대로)")

# 22. a823a7ba — p70: 경우 나눔 → cases
add(id="a823a7ba", qtype="short",
    question="두 함수\n[[f(x) = cases(x + 2, x <= a, pow(x,2) + 2x, x > a)]], [[g(x) = x - (3a + 1)]]에\n대하여 함수 [[f(x) g(x)]]가 실수 전체의 집합에서 연속이\n되도록 하는 모든 실수 [[a]]의 값의 합을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로 교체. 답 −3/2 유지")

# 23. 8ae0e6db — p82: 경우 나눔(조건 f(x)≠0 / f(x)=0) → cases
add(id="8ae0e6db", qtype="choice",
    question="최고차항의 계수가 1인 삼차함수 [[f(x)]]에 대하여\n함수 [[g(x)]]를\n[[g(x) = cases(frac(f(x + 3)(f(x) + 1), f(x)), f(x) != 0, 3, f(x) = 0)]]이라 하자.\n[[lim(x, 3, g(x)) = g(3) - 1]]일 때, [[g(5)]]의 값은?",
    choices=["[[14]]", "[[16]]", "[[18]]", "[[20]]", "[[22]]"],
    figure=None, confidence=0.85,
    note="[2023년 9월 고3 15번/4점]. 경우 나눔을 cases로 교체. 답 ④ 유지(빠른정답 80과 불일치는 초안대로)")

# ---------------- 연속함수의 성질 ----------------
# 24. c1a1eb14 — p49: 경우 나눔 → cases
add(id="c1a1eb14", qtype="choice",
    question="3이 아닌 양수 [[a]]에 대하여 함수\n[[f(x) = cases(pow(x - a, 2), x <= a, (x - 3)(x - a), x > a)]]\n가 다음 조건을 만족시킬 때, [[f(3a)]]의 값은?\n(가) [[f(c) = 0]]인 [[c]]가 0과 [[frac(3 + a, 2)]] 사이에\n적어도 하나 존재한다.\n(나) 세 점 [[point(3, f(3))]], [[point(a, f(a))]],\n[[point(frac(3 + a, 2), f(frac(3 + a, 2)))]]를 꼭짓점으로 하는\n삼각형의 넓이는 [[frac(1,8)]] 이다.",
    choices=["[[3]]", "[[6]]", "[[12]]", "[[24]]", "[[48]]"],
    figure=None, confidence=0.85,
    note="[2017년 9월 고2 문과 20번 변형]. 경우 나눔을 cases로 교체. 답 ③ 유지(빠른정답 4와 불일치는 초안대로)")

# 25. aef686b6 — p54: 경우 나눔 → cases
add(id="aef686b6", qtype="short",
    question="함수 [[f(x) = pow(x,2) - 8x + a]]에 대하여 함수 [[g(x)]]를\n[[g(x) = cases(2x + 5a, x >= a, f(x + 4), x < a)]]라 할 때, 다음 조건을\n만족시키는 모든 실수 [[a]]의 값의 곱을 구하시오.\n(가) 방정식 [[f(x) = 0]]은 열린 구간 [[itv(0, 2, oo)]]에서 적어도\n하나의 실근을 갖는다.\n(나) 함수 [[f(x) g(x)]]는 [[x = a]]에서 연속이다.",
    choices=None, figure=None, confidence=0.85,
    note="[2016년 4월 고3 문과 30번/4점]. 경우 나눔을 cases로 교체. 답 56 유지(빠른정답 3과 불일치는 초안대로)")

# ---------------- 부정적분 ----------------
# 26. c8d5dc9d — p9: f′(1) → app(prime(f), 1)
add(id="c8d5dc9d", qtype="short",
    question="함수 [[f(x)]]에 대하여 [[f(x) = dydx(integ(3 pow(x,3) + 4x + 5, x), x)]]일\n때, [[app(prime(f), 1)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(1)을 app(prime(f), 1)로 교체(d/dx∫…dx는 dydx(integ(…,x),x)). 답 13 유지(빠른정답 4와 불일치는 초안대로)")

# 27. 9c42633f — p10: f′(1) → app
add(id="9c42633f", qtype="short",
    question="함수 [[f(x)]]에 대하여 [[f(x) = dydx(integ(5 pow(x,3) + 2x + 1, x), x)]]일\n때, [[app(prime(f), 1)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(1)을 app(prime(f), 1)로 교체. 답 17 유지")

# 28. 1bdf9683 — p13: f′(2) → app
add(id="1bdf9683", qtype="short",
    question="함수 [[f(x)]]에 대하여 [[f(x) = dydx(integ(pow(x,3) - 2x + 3, x), x)]]일\n때, [[app(prime(f), 2)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(2)를 app(prime(f), 2)로 교체. 답 10 유지(빠른정답 17과 불일치는 초안대로)")

# 29. 1ad2af91 — p29: 피적분함수 속 f(x)f′(x) → f(x) app(prime(f), x)
add(id="1ad2af91", qtype="short",
    question="최고차항의 계수가 양수인 다항함수 [[f(x)]]가 다음 조건을\n모두 만족할 때, [[f(a)]]의 값을 구하시오.\n(단, [[a]]는 상수이고, [[C]]는 적분상수이다.)\n(가) 함수 [[y = f(x)]]의 그래프는 원점에 대하여\n대칭이다.\n(나) [[integ(2f(x) + f(x) app(prime(f), x), x) = frac(1,2) pow(x,6) - frac(7,2) pow(x,4) + a pow(x,2) + C]]",
    choices=None, figure=None, confidence=0.85,
    note="f(x)f′(x)를 f(x) app(prime(f), x)로 교체. 답 48 유지(빠른정답 3과 불일치는 초안대로)")

# 30. 34170754 — p36: Fₙ(x)·Fₙ(0)·Fₙ(1) → app(sub(F,n), ·)
add(id="34170754", qtype="choice",
    question="함수 [[app(sub(F,n), x) = sum(k, 1, n + 1, (k integ(pow(x, k - 1), x)))]]에 대하여\n[[app(sub(F,n), 0) = 0]]일 때, [[app(sub(F,n), 1)]]의 값은? (단, [[n]] = 1, 2, 3, ⋯)",
    choices=["[[frac(n,2)]]", "[[frac(n + 1, 2)]]", "[[n - 1]]", "[[n]]", "[[n + 1]]"],
    figure=None, confidence=0.85,
    note="첨자 함수 적용 Fₙ(x)를 app(sub(F,n), x)로 교체. 답 ⑤ 유지(빠른정답 2와 불일치는 초안대로)")

# 31. e6324ec4 — p53: Fₙ(x)·F_{n+1}(x)·Gₙ(x) → app(sub(F,n), x) 등, G₉₈′(1) → app(prime(sub(G,98)), 1)
add(id="e6324ec4", qtype="short",
    question="함수 [[f(x) = -x + 1]]에 대하여 함수 [[app(sub(F,n), x)]]는 다음 조건을\n모두 만족시킨다.\n(가) [[app(sub(F,1), x) = integ(f(x), x)]], [[app(sub(F,1), 0) = -1]]\n(나) [[app(sub(F, n + 1), x) = integ(app(sub(F,n), x), x)]],\n[[app(sub(F, n + 1), 0) = pow(-1, n + 1)]]\n[[app(sub(G,n), x) = app(sub(F,n), x) + app(sub(F, n + 1), x)]]일 때, [[frac(app(prime(sub(G,98)), 1), app(sub(G,98), 1))]]의\n값을 구하시오. (단, [[n]] = 1, 2, 3, ⋯)",
    choices=None, figure=None, confidence=0.85,
    note="첨자 함수 적용을 app(sub(F,n), x)로, G₉₈′(1)을 app(prime(sub(G,98)), 1)로 교체. 답 100 유지(빠른정답 4와 불일치는 초안대로)")

# 32. ced862e3 — p56: 도함수 f′(x)의 경우 나눔 → app(prime(f), x) = cases(…)
add(id="ced862e3", qtype="short",
    question="모든 실수 [[x]]에 대하여 연속인 함수 [[f(x)]]의\n도함수 [[app(prime(f), x)]]가 [[app(prime(f), x) = cases(-2x + 1, x > 1, 3 pow(x,2) - 4, x < 1)]]이고\n[[f(0) = 2]]일 때, [[f(-2)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(x)를 app(prime(f), x)로, 경우 나눔을 cases로 교체. 답 2 유지(빠른정답 100과 불일치는 초안대로)")

# 33. b2925b8a — p83: 보기 ㄱㄴ의 f′(0) → app(prime(f), 0)
add(id="b2925b8a", qtype="choice",
    question="다항함수 [[f(x)]]가 모든 실수 [[x]], [[y]]에 대하여\n[[f(x + y) = f(x) + f(y) + 6x y(x + y) + 1]]일 때, 옳은\n것만을 보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. [[app(prime(f), 0) = f(1)]]\nㄴ. [[app(prime(f), 0) = 0]]이면 함수 [[f(x)]]는 극값을 갖지\n않는다.\nㄷ. 함수 [[f(x)]]가 극값을 가질 때, 극댓값과\n극솟값의 합은 [[-2]]이다.",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="f′(0)을 app(prime(f), 0)으로 교체. 답 ④ 유지")

# ---------------- 속도와 거리 ----------------
# 34. 7a66e82f — p4: v₁(t)·v₂(t) → app(sub(v,1), t)
add(id="7a66e82f", qtype="choice",
    question="수직선 위를 움직이는 두 점 P, Q의 시각 [[t]] ([[t > 0]])에서의\n속도를 각각 [[app(sub(v,1), t)]], [[app(sub(v,2), t)]]라 할 때, [[app(sub(v,1), t) = 3 pow(t,2) - 7t + 2]],\n[[app(sub(v,2), t) = 2t + 2]]이다. 시각 [[t = 0]]에서의 점 P의 위치는\n4이고 점 Q의 위치는 [[k]]일 때, 두 점 P, Q가 동시에\n출발한 후 2번 만나도록 하는 정수 [[k]]의 개수는?",
    choices=["[[11]]", "[[12]]", "[[13]]", "[[14]]", "[[15]]"],
    figure=None, confidence=0.85,
    note="첨자 함수 적용 v₁(t)·v₂(t)를 app(sub(v,1), t)·app(sub(v,2), t)로 교체. 답 ③ 유지(빠른정답 8과 불일치는 초안대로)")

# 35. 6edf187f — p34: v₁(t)·x₁(t) → app(sub(·,1), t), 식 안 빈칸 (가)(나) → box(1)(2) ((다)는 문장 속이라 텍스트)
add(id="6edf187f", qtype="choice",
    question="원점을 동시에 출발하여 수직선 위를 움직이는\n두 점 P, Q의 시각 [[t]]에서의 속도가 각각\n[[app(sub(v,1), t) = frac(1,2) pow(t,2) - 3t]], [[app(sub(v,2), t) = -frac(1,2) pow(t,2) + t]]\n이다. 다음은 두 점 P, Q가 출발 후 처음으로 만날 때까지\n두 점 P, Q 사이의 거리의 최댓값을 구하는 과정이다.\n두 점 P, Q의 시각 [[t]]에서의 위치를 각각\n[[app(sub(x,1), t)]], [[app(sub(x,2), t)]]라 하면\n[[app(sub(x,1), t) = frac(1,6) pow(t,3) - frac(3,2) pow(t,2)]]\n[[app(sub(x,2), t) = box(1)]]\n출발 후 처음으로 두 점 P, Q가 만나는 시각은\n[[t = 6]]이다.\n[[0 < t <= 6]]에서 두 점 P, Q 사이의 거리를 [[l(t)]]라\n하면\n[[l(t)]]는 [[t = box(2)]] 일 때 극대이면서 최대이므로\n[[l(t)]]의 최댓값은 (다) 이다.\n위의 (가)에 알맞은 식을 [[f(t)]]라 하고, (나), (다)에 알맞은\n수를 각각 [[a]], [[b]]라 할 때, [[frac(a × b, f(2))]]의 값은?",
    choices=["[[60]]", "[[62]]", "[[64]]", "[[66]]", "[[68]]"],
    figure=None, confidence=0.85,
    note="[2017년 11월 고2 이과 18번/4점]. 첨자 함수 적용을 app(sub(v,1), t)·app(sub(x,1), t)로, 식 안 빈칸 (가)(나)를 box(1)(2)로 교체. 답 ③ 유지(빠른정답 '180m'은 값 아님)")

# 36. 18ab835c — p99: 속도 v(t) 3구간 경우 나눔 → cases
add(id="18ab835c", qtype="choice",
    question="수직선 위에서 원점을 출발하여 움직이는 점 P의\n시각 [[t]]([[0 <= t <= 5]])일 때의 속도 [[v(t)]]가 다음과 같다.\n[[v(t) = cases(4t, 0 <= t < 1, -2t + 6, 1 <= t < 3, t - 3, 3 <= t <= 5)]]\n실수 [[x]] ([[0 < x < 3]])에 대하여 점 P가\n시각 [[t = 0]]에서 [[t = x]]까지 움직인 거리,\n시각 [[t = x]]에서 [[t = x + 2]]까지 움직인 거리,\n시각 [[t = x + 2]]에서 [[t = 5]]까지 움직인 거리\n중에서 최소인 값을 [[f(x)]]라고 하자. [[f(0) = 0]]일 때,\n[[2 dinteg(0, 2, f(x), x)]]의 값은?",
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    figure=None, confidence=0.85,
    note="3구간 경우 나눔을 cases로 교체. 답 ③ 유지")

# ---------------- 함수의 증가와 감소, 극대와 극소 ----------------
# 37. 17844967 — p8: f′(x) → app(prime(f), x)
add(id="17844967", qtype="choice",
    question="사차함수 [[f(x)]] 의 도함수 [[app(prime(f), x)]] 가\n[[app(prime(f), x) = (x + 1)(pow(x,2) + a x + b)]]\n이다. 함수 [[y = f(x)]] 가 구간 [[itv(-inf, 0, oo)]] 에서 감소하고\n구간 [[itv(2, inf, oo)]] 에서 증가하도록 하는 실수 [[a]], [[b]] 의\n순서쌍 [[point(a, b)]] 에 대하여, [[pow(a,2) + pow(b,2)]] 의 최댓값을 [[M]],\n최솟값을 [[m]] 이라 하자. [[M + m]] 의 값은?",
    choices=["[[frac(21,4)]]", "[[frac(43,8)]]", "[[frac(11,2)]]", "[[frac(45,8)]]", "[[frac(23,4)]]"],
    figure=None, confidence=0.85,
    note="[2013년 9월 고3 문과 21번/4점]. f′(x)를 app(prime(f), x)로 교체. 답 ③ 유지(빠른정답 1과 불일치는 초안대로)")

# 38. 08f7ee20 — p30: 경우 나눔 → cases
add(id="08f7ee20", qtype="choice",
    question="두 실수 [[a]], [[b]]에 대하여\n함수 [[f(x) = cases(-frac(1,3) pow(x,3) - a pow(x,2) - b x, x < 0, frac(1,3) pow(x,3) + a pow(x,2) - b x, x >= 0)]]이\n구간 [[itv(-inf, -1, oc)]]에서 감소하고 구간 [[itv(-1, inf, co)]]에서\n증가할 때, [[a + b]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 하자.\n[[M - m]]의 값은?",
    choices=["[[frac(3,2) + 3 sqrt(2)]]", "[[3 + 3 sqrt(2)]]", "[[frac(9,2) + 3 sqrt(2)]]", "[[6 + 3 sqrt(2)]]", "[[frac(15,2) + 3 sqrt(2)]]"],
    figure=None, confidence=0.85,
    note="[2023년 9월 고3 13번/4점]. 경우 나눔을 cases로 교체. 답 ③ 유지(빠른정답 4와 불일치는 초안대로)")

# 39. ba35e6d9 — p40: y=f′(x) → y = app(prime(f), x). 도함수 그래프 unsupported → 통과
add(id="ba35e6d9", qtype="choice",
    question="다항함수 [[y = f(x)]]의 도함수 [[y = app(prime(f), x)]]의 그래프가\n아래 그림과 같을 때, 다음 중 옳은 것은?",
    choices=["[[f(x)]]는 구간 [[itv(-inf, -2, oo)]]에서 증가한다.", "[[f(x)]]는 구간 [[itv(0, 1, oo)]]에서 감소한다.", "[[f(x)]]는 구간 [[itv(2, 3, oo)]]에서 증가한다.", "[[f(x)]]는 구간 [[itv(3, 6, oo)]]에서 증가하다가 감소한다.", "[[f(x)]]는 구간 [[itv(6, inf, oo)]]에서 감소한다."],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f′(x)의 그래프: x=−2, 1, 3, 6에서 x축과 만남; (−∞,−2)와 (1,3)(x=2에서 극소, 점선), (6,∞)에서 음수; (−2,1), (3,6)에서 양수"}}],
    confidence=0.8,
    note="f′(x)를 app(prime(f), x)로 교체, 도함수 그래프는 unsupported(raw). 답 ⑤ 유지(빠른정답 3과 불일치는 초안대로)")

# ---------------- 함수의 그래프 ----------------
# 40. af8cd741 — p61: 경우 나눔 → cases, g′(0) → app(prime(g), 0)
add(id="af8cd741", qtype="choice",
    question="삼차함수 [[f(x)]]의 최고차항의 계수가 1이고 함수 [[g(x)]]는\n[[g(x) = cases(2, x < 0, f(x), x >= 0)]]이다.\n[[g(x)]]가 실수 전체의 집합에서 미분가능하고 [[g(x)]]의\n최솟값이 2보다 작을 때, 다음 보기 중에서 옳은 것을\n있는 대로 고른 것은?\n<보기>\nㄱ. [[g(0) + app(prime(g), 0) = 2]]\nㄴ. [[g(1) < 3]]\nㄷ. [[g(x)]]의 최솟값이 [[frac(3,2)]] 일 때, [[g(2) = 2]]이다.",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로, g′(0)을 app(prime(g), 0)으로 교체. 답 ② 유지")

# ================= esc_sonnet_h2-2_3of3 =================
# 41. 204c586d — 넓이 p93: 문법 문제 없음(도형만) → 그대로 통과
add(id="204c586d", qtype="choice",
    question="다음 그림은 함수 [[y = f(x)]]와 그 역함수 [[y = g(x)]]의\n그래프이다. 두 그래프가 점 [[point(1, 1)]], [[point(5, 5)]]에서 만나고\n[[dinteg(1, 5, f(x), x) = 9]]일 때, 두 곡선 [[y = f(x)]]와\n[[y = g(x)]]로 둘러싸인 도형의 넓이는?",
    choices=["[[3]]", "[[4]]", "[[6]]", "[[8]]", "[[12]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 가파르게 증가하는 곡선 y=f(x)와 완만하게 증가하는 곡선 y=g(x)(서로 역함수)가 점 (1,1), (5,5)에서 만남; 두 교점에서 축으로 점선, 축 눈금 1, 5"}}],
    confidence=0.8,
    note="문법 수정 없음(함수·역함수 그래프는 unsupported(raw)). 답 ③ 유지")

# 42. d8e6aed4 — 미분계수 p41: f′(3)·f′(9) → app(prime(f), ·)
add(id="d8e6aed4", qtype="short",
    question="다항함수 [[f(x)]]에 대하여 [[y = f(x)]]의 그래프가 [[y]]축에\n대하여 대칭이고 [[app(prime(f), 3) = 3]], [[app(prime(f), 9) = -1]]일 때,\n[[lim(x, -3, frac(f(pow(x,2)) - f(9), f(x) - f(3)))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(3)·f′(9)를 app(prime(f), 3)·app(prime(f), 9)로 교체. 답 −2 유지")

# 43. 9fcb51b4 — 미분계수 p92: 경우 나눔 → cases
add(id="9fcb51b4", qtype="choice",
    question="함수 [[f(x) = cases(pow(x,3) - a x + 2b, x < 1, -3x + b, x >= 1)]]이 실수 전체의\n집합에서 미분가능할 때, [[a b]]의 값은?\n(단, [[a]]와 [[b]]는 상수이다.)",
    choices=["[[3]]", "[[6]]", "[[9]]", "[[12]]", "[[15]]"],
    figure=None, confidence=0.85,
    note="[2021년 11월 고2 12번/3점]. 경우 나눔을 cases로 교체. 답 ④ 유지")

# 44. 68d93f53 — 미분계수 p94: 경우 나눔 → cases
add(id="68d93f53", qtype="choice",
    question="함수 [[f(x) = cases(pow(x,2) - x + 1, x <= 1, a x + b, x > 1)]]가 [[x = 1]]에서\n미분가능할 때, [[a b]]의 값은?",
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로 교체. 답 ③ 유지")

# 45. a61f49df — 미분계수 p97: 4구간 경우 나눔 → cases. 그래프 unsupported → 통과
add(id="a61f49df", qtype="choice",
    question="정수 [[k]]와 함수 [[f(x) = cases(-x - 1, x < 0, -x + 1, 0 <= x < 1, 0, 1 <= x < 2, x - 3, x >= 2)]]에\n대하여 함수 [[g(x)]]를 [[g(x) = abs(f(x - k))]]라 할 때,\n다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[k = -2]]일 때, [[lim(x, 0, g(x), -) = g(0)]]이다.\nㄴ. 모든 정수 [[k]]에 대하여 함수 [[f(x) + g(x)]]는\n[[x = 0]]에서 불연속이다.\nㄷ. 함수 [[f(x) g(x)]]가 [[x = 0]]에서 미분가능하도록\n하는 모든 정수 [[k]]의 값의 합은 2이다.",
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: x<0에서 기울기 −1인 직선(x=−1에서 x축과 만남, x=0에서 −1로 접근하는 빈 점), 0≤x<1에서 (0,1)(채운 점)부터 (1,0)까지 감소, 1≤x<2에서 y=0(x=2에서 빈 점), x≥2에서 (2,−1)(채운 점)부터 기울기 1로 증가하여 (3,0) 지남; (2,−1)과 축을 잇는 점선"}}],
    confidence=0.8,
    note="[2022년 4월 고3 14번 변형]. 4구간 경우 나눔을 cases로 교체, 그래프는 unsupported(raw). 답 ② 유지")

# 46. 6b6bdce2 — 미분계수 p99: 경우 나눔 → cases
add(id="6b6bdce2", qtype="choice",
    question="함수 [[f(x) = cases(a pow(x,2) + b, x < 2, 2x + 4a, x >= 2)]]가 [[x = 2]]에서 미분가능할\n때, [[frac(b, a)]]의 값은? (단, [[a]], [[b]]는 상수이다.)",
    choices=["[[frac(1,2)]]", "[[1]]", "[[2]]", "[[4]]", "[[8]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로 교체. 답 ⑤ 유지(빠른정답 3과 불일치는 초안대로)")

# ================= esc_opus_h3-1_1of1 =================
# 47. c99f5383 — 중복조합 p62: 첨자 빈칸 ₄H₍가₎·₄H₍다₎ → hcomb(4, box(1))·hcomb(4, box(3)), (나) → box(2)(식 안)
add(id="c99f5383", qtype="choice",
    question="다음은 4 이상의 자연수 [[n]]에 대하여 등식\n[[a × b × c × d = pow(2,n) × pow(3,n)]]\n을 만족시키는 2 이상의 자연수 [[a]], [[b]], [[c]], [[d]]의 순서쌍 ([[a]], [[b]], [[c]], [[d]]) 중에서 [[a + b + c + d]]가 짝수가 되도록 하는 모든 순서쌍의 개수를 구하는 과정이다.\n[[a = pow(2, sub(x,1)) × pow(3, sub(y,1))]], [[b = pow(2, sub(x,2)) × pow(3, sub(y,2))]], [[c = pow(2, sub(x,3)) × pow(3, sub(y,3))]], [[d = pow(2, sub(x,4)) × pow(3, sub(y,4))]]이라 하면 [[sub(x,1) + sub(x,2) + sub(x,3) + sub(x,4) = n]], [[sub(y,1) + sub(y,2) + sub(y,3) + sub(y,4) = n]] (단, [[i]] = 1, 2, 3, 4에 대하여 [[sub(x,i)]], [[sub(y,i)]]는 음이 아닌 정수) 이다. 이때 [[a + b + c + d]]가 짝수이므로 [[a]], [[b]], [[c]], [[d]]가 모두 짝수이거나 [[a]], [[b]], [[c]], [[d]] 중에서 2개만 짝수이다.\n(i) [[a]], [[b]], [[c]], [[d]]가 모두 짝수인 경우 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]]가 모두 자연수이고 [[sub(y,1)]], [[sub(y,2)]], [[sub(y,3)]], [[sub(y,4)]]는 음이 아닌 정수이므로 순서쌍 ([[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]], [[sub(y,1)]], [[sub(y,2)]], [[sub(y,3)]], [[sub(y,4)]])의 개수는 [[hcomb(4, box(1)) × hcomb(4, n)]] ⋯ ㉠\n(ii) [[a]], [[b]], [[c]], [[d]] 중에서 2개만 짝수인 경우 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]] 중에서 자연수가 2개이고 0이 2개이므로 순서쌍 ([[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]])의 개수는 [[comb(4, 2) × box(2)]] 이다. 이때 [[a]], [[b]], [[c]], [[d]] 중 홀수인 두 수는 1이 될 수 없으므로 순서쌍 ([[sub(y,1)]], [[sub(y,2)]], [[sub(y,3)]], [[sub(y,4)]])의 개수는 [[hcomb(4, box(3))]] 이다. 따라서 순서쌍 ([[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]], [[sub(y,1)]], [[sub(y,2)]], [[sub(y,3)]], [[sub(y,4)]])의 개수는 [[comb(4, 2) × box(2) × hcomb(4, box(3))]] ⋯ ㉡\n(i), (ii)에 의하여 구하는 경우의 수는 ㉠+㉡이다.\n위의 (가), (나), (다)에 알맞은 식을 각각 [[f(n)]], [[g(n)]], [[h(n)]]이라 할 때, [[f(6) + g(7) + h(8)]]의 값은?",
    choices=["[[13]]", "[[14]]", "[[15]]", "[[16]]", "[[17]]"],
    figure=None, confidence=0.85,
    note="[2018년 10월 고3 이과 19번/4점]. 첨자 빈칸 ₄H₍가₎·₄H₍다₎를 hcomb(4, box(1))·hcomb(4, box(3))으로, 곱 속 (나)를 box(2)로 교체(이미지 재확인). 답 ② 유지(빠른정답 100과 불일치는 초안대로)")

# 48. 7673aae5 — 확률의 뜻 p68: 이미지 상단 잘림(재확인: 첫 줄이 '각 점 Pᵢ …'로 시작, 그림 1 설명 첫 문장 없음) → 보류 유지
add(id="7673aae5", qtype="short",
    question="각 점 [[sub(P,i)]] ([[i]] = 1, 2, 3, 4)에 대하여 점 [[sub(P,i)]]와 5개의 점 [[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], [[sub(Q,4)]], [[sub(Q,5)]] 중에서 임의로 선택한 한 점을 선분으로 연결한다. [그림 2]는 이러한 방법에 따라 4개의 선분을 그린 2가지 예이다. 직사각형 ABCD가 추가된 4개의 선분에 의하여 나누어진 영역의 개수가 6일 확률이 [[frac(q,p)]] 일 때, [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "[그림 1] 직사각형 ABCD, 변 AD 위 점 P₁~P₄, 변 BC 위 점 Q₁~Q₅; [그림 2] 각 Pᵢ에서 Q점으로 선분 4개를 그은 예 2가지"}}],
    confidence=0.7,
    needs_review="이미지 상단 잘림(문항 첫 문장 — [그림 1] 설정 설명 — 누락, 재확인) / 정보가 그림에만 있음(직사각형 위 점·선분)",
    note="문법 수정 없음(보이는 부분만 전사). 답 146 유지(p69·p70과 같은 설정 가정, 빠른정답 4와 불일치)")

# ================= esc_sonnet_h3-1_1of2 =================
# 49. dfb31e08 — 모비율 p49: p̂ → hat(p)
add(id="dfb31e08", qtype="short",
    question="어느 모집단에서 표본을 임의추출하여 구한 모비율 [[p]]의 신뢰도 99%의 신뢰구간이 [[0.5484 <= p <= 0.6516]]일 때, 이 표본의 표본비율 [[hat(p)]]의 값을 구하시오.\n(단, [[prob(abs(Z) <= 2.58) = 0.99]])",
    choices=None, figure=None, confidence=0.85,
    note="표본비율 p̂를 hat(p)로 교체. 답 0.6 유지(빠른정답 1과 불일치는 초안대로)")

# 50. 4864355c — 모비율 p68: |p̂−p| ≤ 0.16√(p̂(1−p̂)) → 한 식으로
add(id="4864355c", qtype="short",
    question="우리나라 성인을 대상으로 특정 질병에 대한 항체 보유 비율을 조사하려고 한다. 모집단의 항체 보유 비율을 [[p]], 모집단에서 임의로 추출한 [[n]]명을 대상으로 조사한 표본의 항체 보유 비율을 [[hat(p)]]이라고 할 때,\n[[abs(hat(p) - p) <= 0.16 sqrt(hat(p)(1 - hat(p)))]] 일 확률이 0.9544 이상이 되도록 하는 [[n]]의 최솟값을 구하시오.\n(단, [[Z]]가 표준정규분포가 따르는 확률변수일 때, [[prob(0 <= Z <= 2) = 0.4772]]이다.)",
    choices=None, figure=None, confidence=0.85,
    note="[2010년 11월 고3 이과 확률과 통계 30번]. p̂를 hat(p)로 써서 부등식을 한 식으로. 원문 '표준정규분포가 따르는' 그대로. 답 157 유지(빠른정답 1과 불일치는 초안대로)")

# 51. 531aac0c — 중복조합 p73: (f∘f)(x) = x → app(comp(f, f), x) = x
add(id="531aac0c", qtype="choice",
    question="집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여 다음 조건을 만족시키는 함수 [[f]]: [[X]]→[[X]]의 개수는?\n(가) [[x]] = 1, 2, 3, 4일 때 [[f(x) <= f(x + 1)]]이다.\n(나) [[x]]가 소수가 아니면 [[app(comp(f, f), x) = x]]이다.",
    choices=["12", "14", "16", "18", "20"],
    figure=None, confidence=0.85,
    note="[2025년 3월 고3 확률과 통계 27번 변형]. (f∘f)(x) = x를 app(comp(f, f), x) = x로 교체. 답 ⑤ 유지")

# 52. ff432543 — 이항분포 p48: σ → sigma, P(|X−m| < √2σ/2) 한 식으로
add(id="ff432543", qtype="short",
    question="이항분포 [[binomd(n, p)]]를 따르는 확률변수 [[X]]의 분산은 2이고,\n[[prob(X = n - 1) = 18 prob(X = n)]]이 성립한다.\n확률변수 [[X]]의 평균을 [[m]], 표준편차를 [[sigma]]라 할 때,\n[[prob(abs(X - m) < frac(sqrt(2) sigma, 2)) = frac(k, pow(3, 8))]]이다. [[k]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="σ를 sigma로 써서 확률식을 한 식으로(이미지 재확인: √2σ/2 꼴). 답 1792 유지(빠른정답 6과 불일치는 초안대로)")

# 53. d7b25562 — 기댓값 p70: T = a((X−m)/σ) + b → sigma로 한 식
add(id="d7b25562", qtype="choice",
    question="2005학년도 대학수학능력시험 수리영역의 원점수 [[X]]의 평균을 [[m]], 표준편차를 [[sigma]]라 할 때 표준점수 [[T]]는\n[[T = a × (frac(X - m, sigma)) + b]] (단, [[a > 0]])\n꼴로 나타내어진다. 수리영역의 표준점수 [[T]]가 평균이 100, 표준편차가 20인 분포를 이룬다고 할 때, 두 상수 [[a]], [[b]]의 합 [[a + b]]의 값은?",
    choices=["80", "90", "100", "110", "120"],
    figure=None, confidence=0.85,
    note="[2004년 3월 고3 이과 14번]. σ를 sigma로 써서 T의 정의식을 한 식으로(a(…)는 함수 적용으로 읽히므로 a × (…)). 답 ⑤ 유지(빠른정답 11과 불일치는 초안대로)")

# 54. b05684dc — 기댓값 p80: T = a·(X−m)/σ + b → sigma로 한 식
add(id="b05684dc", qtype="choice",
    question="어느 과목의 시험점수 [[X]]의 평균이 [[m]]점이고 표준편차가 [[sigma]]점일 때, 새로운 확률변수 [[T]]를\n[[T = a × frac(X - m, sigma) + b]]로 정하였다. [[T]]의 평균이 80점, 표준편차가 10점이 되도록 하는 두 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값은? (단, [[a > 0]])",
    choices=["80", "90", "100", "110", "120"],
    figure=None, confidence=0.85,
    note="σ를 sigma로 써서 T의 정의식을 한 식으로(원문 '·'는 ×). 답 ② 유지(빠른정답 16과 불일치는 초안대로)")

# 55. 86645a45 — 정규분포 p1: σ₁, σ₂ → sub(sigma,1), sub(sigma,2). 정규분포곡선 unsupported → 통과
add(id="86645a45", qtype="choice",
    question="2학년 재학생 수가 동일한 두 고등학교 A, B의 2학년 학생의 수학 성적 분포가 각각 정규분포를 이루고 그 정규분포곡선이 다음 그림과 같다. 두 고등학교 A, B의 수학 성적의 평균을 각각 [[sub(m,1)]], [[sub(m,2)]], 표준편차를 각각 [[sub(sigma,1)]], [[sub(sigma,2)]]라 할 때, 다음 중 옳은 것은?",
    choices=["[[sub(m,1) < sub(m,2)]], [[sub(sigma,1) < sub(sigma,2)]]", "[[sub(m,1) < sub(m,2)]], [[sub(sigma,1) > sub(sigma,2)]]", "[[sub(m,1) < sub(m,2)]], [[sub(sigma,1) = sub(sigma,2)]]", "[[sub(m,1) > sub(m,2)]], [[sub(sigma,1) < sub(sigma,2)]]", "[[sub(m,1) > sub(m,2)]], [[sub(sigma,1) > sub(sigma,2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 두 정규분포곡선: A(초록)는 오른쪽에 있고 높고 좁음, B(주황)는 왼쪽에 있고 낮고 넓음"}}],
    confidence=0.8,
    note="σ₁·σ₂를 sub(sigma,1)·sub(sigma,2)로 교체, 정규분포곡선은 unsupported(raw). 답 ④ 유지")

# 56. 4c30c7df — 정규분포 p3: N(14, σ²) → normald(14, pow(sigma, 2))
add(id="4c30c7df", qtype="choice",
    question="정규분포 [[normald(14, pow(sigma, 2))]]을 따르는 확률변수 [[X]]에 대하여 함수 [[f(k)]]를 [[f(k) = prob(k <= X <= k + 6)]]이라 할 때, 다음 보기 중 옳은 것을 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(5) = f(17)]]\nㄴ. 함수 [[f(k)]]는 [[k = 14]]일 때, 최댓값을 갖는다.\nㄷ. 임의의 실수 [[a]]에 대하여 [[f(a) = f(22 - a)]]이다.",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="N(14, σ²)을 normald(14, pow(sigma, 2))로 교체. 답 ③ 유지")

# 57. 2845703b — 정규분포 p4: σ_A²·σ_B²·σ_C² → pow(sub(sigma,A), 2) 등. 정규분포곡선 unsupported → 통과
add(id="2845703b", qtype="choice",
    question="다음 세 곡선 A, B, C는 각각 정규분포를 따르는 확률분포의 정규분포곡선이다. 세 확률분포의 평균을 각각 [[sub(m,A)]], [[sub(m,B)]], [[sub(m,C)]], 분산을 각각 [[pow(sub(sigma,A), 2)]], [[pow(sub(sigma,B), 2)]], [[pow(sub(sigma,C), 2)]]이라 할 때, 다음 중 옳은 것은? (단, 곡선 A는 함수 [[y = f(x)]]의 그래프이고, 곡선 B는 함수 [[y = f(x - k)]]의 그래프이다.)",
    choices=["[[sub(m,A) = sub(m,B) > sub(m,C)]], [[pow(sub(sigma,B), 2) > pow(sub(sigma,A), 2) = pow(sub(sigma,C), 2)]]",
             "[[sub(m,B) = sub(m,C) > sub(m,A)]], [[pow(sub(sigma,C), 2) > pow(sub(sigma,A), 2) = pow(sub(sigma,B), 2)]]",
             "[[sub(m,B) > sub(m,A) = sub(m,C)]], [[pow(sub(sigma,A), 2) = pow(sub(sigma,B), 2) > pow(sub(sigma,C), 2)]]",
             "[[sub(m,C) > sub(m,A) = sub(m,B)]], [[pow(sub(sigma,A), 2) = pow(sub(sigma,C), 2) > pow(sub(sigma,B), 2)]]",
             "[[sub(m,C) > sub(m,A) = sub(m,B)]], [[pow(sub(sigma,B), 2) > pow(sub(sigma,A), 2) = pow(sub(sigma,C), 2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 세 정규분포곡선: A(빨강, 왼쪽, 높고 좁음, 꼭대기 아래 점선), B(청록, 오른쪽, A와 같은 모양, 꼭대기 아래 점선), C(노랑, B와 같은 중심, 낮고 넓음)"}}],
    confidence=0.8,
    note="σ_A² 등을 pow(sub(sigma,A), 2)로 교체, 정규분포곡선은 unsupported(raw). 답 ② 유지(빠른정답 4와 불일치는 초안대로)")

# 58. 992d8e58 — 정규분포 p5: σ₁, σ₂ → sub(sigma,1), sub(sigma,2). 정규분포곡선 unsupported → 통과
add(id="992d8e58", qtype="choice",
    question="다음 그림은 A반과 B반의 수학 성적을 나타내는 정규분포의 확률밀도함수의 그래프이다. A반과 B반의 성적의 평균을 각각 [[sub(m,1)]], [[sub(m,2)]], 표준편차를 각각 [[sub(sigma,1)]], [[sub(sigma,2)]]라 할 때, 다음 중 옳은 것은?",
    choices=["[[sub(m,1) > sub(m,2)]], [[sub(sigma,1) > sub(sigma,2)]]", "[[sub(m,1) > sub(m,2)]], [[sub(sigma,1) < sub(sigma,2)]]", "[[sub(m,1) < sub(m,2)]], [[sub(sigma,1) > sub(sigma,2)]]", "[[sub(m,1) < sub(m,2)]], [[sub(sigma,1) < sub(sigma,2)]]", "[[sub(m,1) = sub(m,2)]], [[sub(sigma,1) = sub(sigma,2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "x축 위 두 정규분포곡선: A는 왼쪽에 있고 낮고 넓음, B는 오른쪽에 있고 높고 좁음(각 꼭대기 아래 점선)"}}],
    confidence=0.8,
    note="σ₁·σ₂를 sub(sigma,1)·sub(sigma,2)로 교체, 정규분포곡선은 unsupported(raw). 답 ③ 유지(빠른정답 4와 불일치는 초안대로)")

# 59. 5082298d — 정규분포 p13: N(m, σ²), m+σ² → sigma
add(id="5082298d", qtype="short",
    question="확률변수 [[X]]는 정규분포 [[normald(m, pow(sigma, 2))]]을 따른다.\n[[frac(1,3) X]]의 분산이 1이고, [[prob(X <= 25) = prob(X >= 35)]]일 때,\n[[m + pow(sigma, 2)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="σ를 sigma로 써서 N(m, σ²)·m+σ²을 식으로. 답 39 유지(빠른정답 673과 불일치는 초안대로)")

# 60. 98dd587a — 정규분포 p35: N(m²+4m+36, σ²) → normald(…, pow(sigma, 2)), σ → sigma
add(id="98dd587a", qtype="short",
    question="두 양수 [[m]], [[sigma]]에 대하여 확률변수 [[X]]는 정규분포 [[normald(m, pow(1, 2))]], 확률변수 [[Y]]는 정규분포 [[normald(pow(m, 2) + 4m + 36, pow(sigma, 2))]]을 따르고, 두 확률변수 [[X]], [[Y]]는 [[prob(X <= 0) = prob(Y <= 0)]]을 만족시킨다. [[sigma]]의 값이 최소가 되도록 하는 [[m]]의 값을 [[sub(m,1)]]이라 하자. [[m = sub(m,1)]]일 때, 두 확률변수 [[X]], [[Y]]에 대하여 [[prob(X >= 1) = prob(Y <= k)]]를 만족시키는 상수 [[k]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2024년 7월 고3 확률과 통계 29번 변형]. σ를 sigma로 교체. 답 176 유지(빠른정답 126과 불일치는 초안대로)")

# 61. e924b723 — 정규분포 p55: σ → sigma, m+σ → 식
add(id="e924b723", qtype="choice",
    question="어느 학교 3학년 학생의 A 과목 시험 점수는 평균이 [[m]], 표준편차가 [[sigma]]인 정규분포를 따르고, B 과목 시험 점수는 평균이 [[m + 3]], 표준편차가 [[sigma]]인 정규분포를 따른다고 한다. 이 학교 3학년 학생 중에서 A 과목 시험 점수가 80점 이상인 학생의 비율이 9%이고, B 과목 시험 점수가 80점 이상인 학생의 비율이 15%일 때, [[m + sigma]]의 값은?\n(단, [[Z]]가 표준정규분포를 따르는 확률변수일 때, [[prob(0 <= Z <= 1.04) = 0.35]], [[prob(0 <= Z <= 1.34) = 0.41]]로 계산한다.)",
    choices=["68.6", "70.6", "72.6", "74.6", "76.6"],
    figure=None, confidence=0.85,
    note="[2014년 9월 고3 이과 19번/4점]. σ를 sigma로 교체. 답 ⑤ 유지(빠른정답 400과 불일치는 초안대로)")

# 62. a5771908 — 정규분포 p57: σ → sigma, m+σ → 식
add(id="a5771908", qtype="choice",
    question="어느 학교 3학년 학생의 A 과목 시험 점수는 평균이 [[m]], 표준편차가 [[sigma]]인 정규분포를 따르고, B 과목 시험 점수는 평균이 [[m - 3]], 표준편차가 [[sigma]]인 정규분포를 따른다고 한다. 이 학교 3학년 학생 중에서 A 과목 시험 점수가 25점 이하인 학생의 비율이 9%이고, B 과목 시험 점수가 25점 이하인 학생의 비율이 15%일 때, [[m + sigma]]의 값은?\n(단, [[Z]]가 표준정규분포를 따르는 확률변수일 때, [[prob(0 <= Z <= 1.04) = 0.35]], [[prob(0 <= Z <= 1.34) = 0.41]]로 계산한다.)",
    choices=["45.4", "48.4", "51.4", "54.4", "57.4"],
    figure=None, confidence=0.85,
    note="σ를 sigma로 교체. 답 ② 유지")
