# -*- coding: utf-8 -*-
# esc_sonnet_h2-1_1of4 — 이미지 기준 전사 (84 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_G = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_15 = ["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"]

# ───────── 지수의 확장과 지수법칙 ─────────
# p25 (id 2개)
dup(["8f2a41fa", "1d7e0747"], qtype="choice",
    question=("두 집합 [[A = set(2, 3, 4)]], [[B = set(-16, -4, 4, 16)]]에 대하여 집합 [[X]]를\n"
              "[[X]] = { [[x]] | [[pow(x, a) = b]], [[in(a, A)]], [[in(b, B)]], [[x]]는 실수 }\n"
              "라 할 때, 다음 보기 중에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[in(root(3, -16), X)]]\n"
              "ㄴ. 집합 [[X]]의 원소의 개수는 12이다.\n"
              "ㄷ. 집합 [[X]]의 원소 중 양수인 모든 원소의 곱은 [[32 sqrt(2)]]이다."),
    choices=CH_G, derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2017년 6월 고2 이과 17번 변형]. X={±2,±4,±√2,±∛4,±2∛2} 10개(ㄴ✗), ㄱ✓, 양수 곱 2·4·√2·∛4·2∛2=32√2(ㄷ✓) → ③.")

# p46
add(id="d22d4550", qtype="short",
    question=("집합 [[A]] = { [[x]] | [[x = pow(frac(1, 64), frac(1, k))]], [[k]]는 0이 아닌 정수 }의 "
              "원소 중 자연수인 것들의 합을 구하시오."),
    choices=None, derived_answer="78", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2008년 9월 고2 문과 24번]. k=-1,-2,-3,-6 → 64+8+4+2=78. 빠른정답 381과 불일치.")

# p53
add(id="0e846abd", qtype="choice",
    question=("음이 아닌 정수 [[n]]에 대하여 [[sub(F, n) = pow(2, pow(2, n)) + 1]]을 [[n]]번째 '페르마 수'라 하고, "
              "[[sub(F, n)]]이 소수일 때 이것을 '페르마 소수'라고 한다. 예를 들면\n"
              "[[sub(F, 0) = pow(2, pow(2, 0)) + 1 = 2 + 1 = 3]],\n"
              "[[sub(F, 1) = pow(2, pow(2, 1)) + 1 = pow(2, 2) + 1 = 5]],\n"
              "[[sub(F, 2)]], [[sub(F, 3)]], [[sub(F, 4)]]는 페르마 소수이다.\n"
              "[[N = pow(2, 32) - 1]]을 소인수 분해할 때, <보기> 중 [[N]]의 약수인 것을 모두 고르면?\n<보기>\n"
              "ㄱ. [[sub(F, 0) × sub(F, 1)]]\n"
              "ㄴ. [[sub(F, 0) × sub(F, 2) × sub(F, 4)]]\n"
              "ㄷ. [[sub(F, 2) × sub(F, 3) × sub(F, 4)]]"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2004년 6월 고2 문과 18번]. 2³²−1=(2−1)(2+1)(2²+1)(2⁴+1)(2⁸+1)(2¹⁶+1)=F₀F₁F₂F₃F₄ → ㄱㄴㄷ 모두 약수 → ⑤. 빠른정답 1과 불일치.")

# p98
add(id="818a7ef6", qtype="choice",
    question=("다음 표는 국악에서 사용하는 한 옥타브의 12음계에 해당하는 율명에 차례로 번호를 붙인 것이다.\n"
              "번호가 [[n]] ([[n]] = 1, 2, 3, ⋯, 12)인 율명의 진동수를 [[f(n)]]이라 하면, 등식 "
              "[[f(n) = C × pow(2, frac(n - 1, 12))]] 이 성립한다. 다음 보기 중 항상 옳은 것만을 있는 대로 고른 것은? "
              "(단, [[C]]는 상수이고, 진동수의 단위는 Hz이다.)\n<보기>\n"
              "ㄱ. [[frac(f(10), f(6)) = pow(2, frac(1, 3))]]\n"
              "ㄴ. '협종'의 진동수가 [[a]]일 때, '응종'의 진동수는 [[root(3, 2) a]]이다.\n"
              "ㄷ. '태주'의 진동수가 [[b]]일 때, '고선'과 '이칙'의 진동수의 곱은 [[root(3, 4) pow(b, 2)]]이다."),
    choices=CH_G, derived_answer="③",
    figure=[{"fn": "table", "args": {"head": ["번호", "1", "2", "3", "4", "5", "6"],
                                     "rows": [["율명", "황종", "대려", "태주", "협종", "고선", "중려"]]}},
            {"fn": "table", "args": {"head": ["번호", "7", "8", "9", "10", "11", "12"],
                                     "rows": [["율명", "유빈", "임종", "이칙", "남려", "무역", "응종"]]}}],
    difficulty_est=3, confidence=0.9,
    note="ㄱ 2^(4/12)=2^(1/3)✓, ㄴ f(12)/f(4)=2^(8/12)=∛4 (✗), ㄷ b²·2^(2/12+6/12)=∛4b²✓ → ③ = 빠른정답 ✓.")

# ───────── 여러 가지 수열의 합 ─────────
# p6
add(id="e5d87df2", qtype="choice",
    question=("첫째항이 1인 등차수열 [[set(sub(a, n))]]에 대하여 수열 [[set(sub(b, n))]]을\n"
              "[[sub(b, n) = sub(a, 1) + 2 sub(a, 2) + 3 sub(a, 3)]] + ⋯ + [[n sub(a, n)]] ([[n >= 1]])이라 하자.\n"
              "[[sub(b, 10) = 715]]일 때, [[sum(n, 1, 10, frac(sub(b, n), n(n + 1)))]] 의 값은?"),
    choices=["[[30]]", "[[35]]", "[[40]]", "[[45]]", "[[50]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2017년 3월 고2 문과 21번/4점]. b_n=n(n+1)/2+d·(n−1)n(n+1)/3, b₁₀=55+330d=715 → d=2; Σ(1/2+2(n−1)/3)=5+30=35 → ② = 빠른정답 ✓.")

# p22
add(id="e1fefc49", qtype="short",
    question="다음 식의 값을 구하시오.\n[[-1 - 2 - 3]] − ⋯ − [[8]]",
    choices=None, derived_answer="-36", figure=None, difficulty_est=1, confidence=0.9,
    note="−(1+⋯+8)=−36. 빠른정답 15와 불일치.")

# p44
add(id="8536ef2c", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[2 × n + 4 × (n - 1) + 6 × (n - 2)]] + ⋯ + [[2n × 1]]\n"
              "= [[frac(n(n + 1)(n + 2), 3)]]\n"
              "가 성립함을 보이는 과정이다.\n\n"
              "[[2 × n + 4 × (n - 1) + 6 × (n - 2)]] + ⋯ + [[2n × 1]]\n"
              "= Σ[k=1..n] ((가)){[[n - (k - 1)]]}\n"
              "= Σ[k=1..n] ((가)){[[(n + 1) - k]]}\n"
              "= [[(n + 1)]] Σ[k=1..n] ((가)) − [[2 sum(k, 1, n, pow(k, 2))]]\n"
              "= [[(n + 1) × n(n + 1)]] − 2 × [[n(n + 1)(2n + 1)]]/((나))\n"
              "= [[n pow(n + 1, 2)]] − [[frac(1, 3) n(n + 1)]]((다))\n"
              "= [[frac(n(n + 1)(n + 2), 3)]]\n\n"
              "위의 (가), (다)에 알맞은 식을 각각 [[f(k)]], [[g(n)]]이라 하고, (나)에 알맞은 수를 [[a]]라 할 때, "
              "[[frac(f(a) × g(a), a)]]의 값은?"),
    choices=["[[25]]", "[[26]]", "[[27]]", "[[28]]", "[[29]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2018년 9월 고2 문과 18번 변형]. (가)=2k, (나)=6, (다)=2n+1 → 12·13/6=26 → ②. 빠른정답 1과 불일치. Σ 안의 빈칸은 텍스트 조각.")

# p48
add(id="d96361a6", qtype="short",
    question=("수열 [[set(sub(a, n))]]에 대하여\n"
              "[[n sub(a, 1) + (n - 1) sub(a, 2) + (n - 2) sub(a, 3)]] + ⋯ + [[2 sub(a, n - 1) + sub(a, n)]]\n"
              "= [[pow(n, 3) - 2 pow(n, 2) + 3n]]\n"
              "이 성립할 때, [[sum(k, 1, 30, sub(a, k))]]의 값을 구하시오."),
    choices=None, derived_answer="2496", figure=None, difficulty_est=3, confidence=0.9,
    note="S_n−S_(n−1)=Σa_k=3n²−7n+6 → n=30: 2496. 빠른정답 2와 불일치.")

# p49
add(id="b70d9401", qtype="choice",
    question=("자연수 [[n]]과 세 정수 [[a]], [[b]], [[c]]에 대하여\n"
              "[[(2n - 1) + 2 × (2n - 3) + 3 × (2n - 5)]] + ⋯ + [[n × 1]]\n"
              "= [[frac(n(n + a)(b n + c), 6)]]\n"
              "일 때, [[a + b + c]]의 값은?"),
    choices=CH_15, derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="Σk(2n+1−2k)=n(n+1)(2n+1)/6 → a=1,b=2,c=1 → 4 → ④. 빠른정답 885와 불일치.")

# p50
add(id="ac580200", qtype="short",
    question=("수열 [[set(sub(a, n))]]에 대하여\n"
              "[[n sub(a, 1) + (n - 1) sub(a, 2) + (n - 2) sub(a, 3)]] + ⋯ + [[2 sub(a, n - 1) + sub(a, n)]]\n"
              "= [[pow(n, 3) - pow(n, 2) + 2n]]\n"
              "이 성립할 때, [[sum(k, 1, 14, sub(a, k))]]의 값을 구하시오."),
    choices=None, derived_answer="522", figure=None, difficulty_est=3, confidence=0.9,
    note="S_n−S_(n−1)=Σa_k=3n²−5n+4 → n=14: 522. 빠른정답 84와 불일치.")

# p54
add(id="2f1b52b4", qtype="short",
    question=("자연수 [[n]]에 대하여 등식\n"
              "[[1 × n + 2 × (n - 1) + 3 × (n - 2)]] + ⋯ + [[(n - 1) × 2 + n × 1]]\n"
              "= [[frac(n(n + a)(n + b), 6)]] ([[a < b]])\n"
              "가 성립할 때, 자연수 [[a]], [[b]]에 대하여 [[b - a]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.9,
    note="Σk(n+1−k)=n(n+1)(n+2)/6 → a=1, b=2 → 1. 빠른정답 2와 불일치.")

# p55
add(id="9b368ba9", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[1 × 2n + 3 × (2n - 2) + 5 × (2n - 4)]] + ⋯ + [[(2n - 1) × 2 = frac(n(n + 1)(2n + 1), 3)]]\n"
              "이 성립함을 보이는 과정이다.\n\n"
              "[[1 × 2n + 3 × (2n - 2) + 5 × (2n - 4)]] + ⋯ + [[(2n - 1) × 2]]\n"
              "= Σ[k=1..n] ((가)){[[2n - (2k - 2)]]}\n"
              "= Σ[k=1..n] ((가)){[[2(n + 1) - 2k]]}\n"
              "= [[2(n + 1)]] Σ[k=1..n] ((가)) − [[2 sum(k, 1, n, 2 pow(k, 2) - k)]]\n"
              "= [[2(n + 1)(n(n + 1) - n)]]\n"
              "− 2{[[n(n + 1)(2n + 1)]]/((나)) − [[frac(n(n + 1), 2)]]}\n"
              "= [[2(n + 1) pow(n, 2)]] − [[frac(1, 3) n(n + 1)]]((다))\n"
              "= [[frac(n(n + 1)(2n + 1), 3)]]\n"
              "이다.\n\n"
              "위의 (가), (다)에 알맞은 식을 각각 [[f(k)]], [[g(n)]]이라 하고, (나)에 알맞은 수를 [[a]]라 할 때, "
              "[[f(a) × g(a)]]의 값은?"),
    choices=["[[50]]", "[[55]]", "[[60]]", "[[65]]", "[[70]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2018년 9월 고2 문과 18번/4점]. (가)=2k−1, (나)=3, (다)=4n−1 → f(3)g(3)=5·11=55 → ②. 빠른정답 2145와 불일치. Σ 안의 빈칸은 텍스트 조각.")

# p78
add(id="b5691dd3", qtype="choice",
    question=("수열 [[set(sub(a, n))]]이 모든 자연수 [[n]]에 대하여\n"
              "[[sum(k, 1, n, sub(a, k)) = log(2, frac((n + 1)(n + 2), 3))]]를 만족시킨다.\n"
              "[[sum(k, 1, m, sub(a, 2k))]]의 값이 자연수가 되도록 하는 100 이하의 모든 자연수 [[m]]의 값의 합은?"),
    choices=["[[96]]", "[[102]]", "[[108]]", "[[114]]", "[[120]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 6월 고3 이과 21번 변형]. a_n=log₂((n+2)/n) (n≥2) → Σa_(2k)=log₂(m+1) → m=1,3,7,15,31,63 합 120 → ⑤. 빠른정답 26과 불일치.")

# p92
add(id="a09c741f", qtype="choice",
    question=("자연수 [[n]]에 대하여 함수 [[f(x)]]가 다음과 같다.\n"
              "[[f(x) = frac(x + 2 pow(n, 2) + n, x - n)]]\n"
              "[[n = k]] ([[k]] = 1, 2, 3, ⋯)일 때, 곡선 [[y = f(x)]]의 제1사분면 위의 점 중에서 [[x]]축, [[y]]축까지의 거리가 "
              "같게 되는 점을 [[sub(P, k)]]라 하고, 점 [[sub(P, k)]]에서 [[x]]축, [[y]]축에 내린 수선의 발을 각각 "
              "[[sub(Q, k)]], [[sub(R, k)]]라 하자. 사각형 O[[sub(Q, k)]][[sub(P, k)]][[sub(R, k)]]의 넓이를 [[sub(A, k)]]라 할 때, "
              "[[sum(k, 1, 10, sub(A, k))]]의 값은?"),
    choices=["[[1770]]", "[[1780]]", "[[1790]]", "[[1800]]", "[[1810]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 유리함수 y=f(x)의 그래프(점근선 x=n, y=1 점선), 제1사분면 점 P_k와 수선의 발 Q_k(x축)·R_k(y축), 정사각형 OQ_kP_kR_k 회색 음영 A_k"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 유리함수 그래프+정사각형 음영 좌표평면 도형; 첨자 점 라벨 사각형 OQₖPₖRₖ",
    note="출처 [2015년 9월 고2 이과 14번/4점]. x=y ⇒ x²−(n+1)x−(2n²+n)=0 → x=2n+1, A_k=(2k+1)², Σ=4·385+4·55+10=1770 → ①. 빠른정답 63과 불일치.")

# p93
add(id="e0e0694c", qtype="short",
    question=("함수 [[y = f(x)]]는 [[f(3) = f(15)]]를 만족하고, 그 그래프는 그림과 같다. 모든 자연수 [[n]]에 대하여 "
              "[[f(n) = sum(k, 1, n, sub(a, k))]]인 수열 [[set(sub(a, n))]]이 있다. [[m]]이 15보다 작은 자연수일 때,\n"
              "[[sub(a, m) + sub(a, m + 1)]] + ⋯ + [[sub(a, 15) < 0]]\n"
              "을 만족시키는 [[m]]의 최솟값을 구하시오."),
    choices=None, derived_answer="5",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 위로 볼록한 곡선 y=f(x), x=3과 x=15에서 같은 함숫값(점선), 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프(y=f(x), f(3)=f(15))",
    note="출처 [2009년 6월 고3 이과 22번]. a_m+⋯+a₁₅=f(15)−f(m−1)<0 ⇔ f(m−1)>f(3) ⇔ 3<m−1<15 → m 최솟값 5. 빠른정답 645와 불일치.")

# p95
add(id="53b70bab", qtype="choice",
    question=("수열 [[set(sub(a, n))]]은 등차수열이고, 수열 [[set(sub(b, n))]]은 모든 자연수 [[n]]에 "
              "대하여 [[sub(b, n) = sum(k, 1, n, pow(-1, k + 1) sub(a, k))]]를 만족시킨다.\n"
              "[[sub(b, 2) = -3]], [[sub(b, 3) + sub(b, 7) = 0]]일 때, 수열 [[set(sub(b, n))]]의 첫째항부터 "
              "제10항까지의 합은?"),
    choices=["[[-45]]", "[[-43]]", "[[-41]]", "[[-39]]", "[[-37]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2024년 9월 고3 12번 변형]. b_(2m)=−md, b_(2m+1)=a+md; d=3, a=−6 → 합 −45 → ① = 빠른정답 ✓.")

# ───────── 수열의 일반항 ─────────
add(id="384b3605", qtype="short",
    question="수열 [[1 × 4]], [[2 × 5]], [[3 × 6]], ⋯에 대하여 [[sub(a, k) = 130]]을 만족시키는 자연수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="10", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=n(n+3)=130 → n=10 = 빠른정답 ✓.")
add(id="abfe2d45", qtype="short",
    question="수열 [[1 × 5]], [[2 × 6]], [[3 × 7]], ⋯에 대하여 [[sub(a, k) = 252]]를 만족시키는 자연수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="14", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=n(n+4)=252 → n=14 = 빠른정답 ✓.")
add(id="af16d15b", qtype="short",
    question="수열 [[2 × 4]], [[4 × 6]], [[6 × 8]], ⋯에 대하여 [[sub(a, k) = 360]]을 만족시키는 자연수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="9", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=2n(2n+2)=360 → n(n+1)=90 → n=9 = 빠른정답 ✓.")

# p12
add(id="4767e033", qtype="choice",
    question=("자연수 [[n]]의 모든 양의 약수를 [[sub(a, 1)]], [[sub(a, 2)]], [[sub(a, 3)]], ⋯, [[sub(a, k)]]라 할 때,\n"
              "[[sub(x, n) = pow(-1, sub(a, 1)) + pow(-1, sub(a, 2))]] + ⋯ + [[pow(-1, sub(a, k))]]\n"
              "이라 하자. <보기>에서 옳은 것을 모두 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(x, 8) = 2]]\n"
              "ㄴ. [[n = pow(3, m)]]이면 [[sub(x, n) = -m + 1]]이다.\n"
              "ㄷ. [[n = pow(10, m)]]이면 [[sub(x, n) = pow(m, 2) - 1]]이다."),
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2008년 6월 고3 문과 28번]. x_n=(짝수 약수)−(홀수 약수): ㄱ 3−1=2✓, ㄴ −(m+1)✗, ㄷ m(m+1)−(m+1)=m²−1✓ → ④ = 빠른정답 ✓.")

# p24
add(id="b1bb6c17", qtype="short",
    question=("자연수의 집합에서 정의되는 두 함수 [[f]]와 [[g]]는\n"
              "[[f(n + 1) = f(n) + 3]], [[f(5) = 23]]\n"
              "[[g(n + 1) = 5 g(n)]], [[g(1) = 5]]\n"
              "를 만족한다. ([[comp(f, g)]])([[k]]) = 383일 때, [[20k]]의 값을 구하시오. "
              "(단, [[comp(f, g)]]는 [[f]]와 [[g]]의 합성함수이다.)"),
    choices=None, derived_answer="60", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="합성함수 적용 표기 (f∘g)(k) 텍스트 혼합",
    note="출처 [2005년 11월 고2 문과 23번]. f(n)=3n+8, g(n)=5ⁿ → 3·5^k+8=383 → k=3 → 60. 빠른정답 5와 불일치.")

# p41
add(id="816e9b51", qtype="choice",
    question=("자연수 [[n]]에 대하여 곡선 [[y = a pow(x, 2)]] ([[a > 0]]) 위의 점 [[sub(P, n)]]을 다음 규칙에 따라 정한다.\n"
              "(가) 점 [[sub(P, 1)]]의 좌표는 [[point(sub(x, 1), a pow(sub(x, 1), 2))]]이다.\n"
              "(나) 점 [[sub(P, n + 1)]]은 점 [[sub(P, n)]][[point(sub(x, n), a pow(sub(x, n), 2))]]을 지나는 직선 "
              "[[y = -a sub(x, n) x + 2a pow(sub(x, n), 2)]]과 곡선 [[y = a pow(x, 2)]]이 만나는 점 중에서 점 [[sub(P, n)]]이 아닌 점이다.\n"
              "점 [[sub(P, n)]]의 [[x]]좌표로 이루어진 수열 [[set(sub(x, n))]]에서 [[sub(x, 1) = frac(1, 2)]]일 때, "
              "[[sub(x, 10)]]의 값은?"),
    choices=["[[-1024]]", "[[-512]]", "[[-256]]", "[[512]]", "[[1024]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y=ax²과 점 P₁, P₂, P₃, P₄를 지나는 여러 직선, 원점 O 부근 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 여러 직선·점 P₁~P₄ 좌표평면 도형",
    note="출처 [2014년 10월 고3 문과 15번/4점]. x²+x_n x−2x_n²=0 → x_(n+1)=−2x_n, x₁₀=(1/2)(−2)⁹=−256 → ③ = 빠른정답 ✓.")

# p53
add(id="40ed7ac6", qtype="choice",
    question="수열 [[-1]], [[3]], [[-5]], [[7]], [[-9]], ⋯의 7번째 항은?",
    choices=["[[-13]]", "[[-11]]", "[[-10]]", "[[11]]", "[[13]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=(−1)ⁿ(2n−1) → a₇=−13 → ①. 빠른정답 5와 불일치.")

# p55
add(id="b26137dc", qtype="short",
    question="다음 수열의 제8항을 추측해 보시오.\n[[1]], [[frac(1, 3)]], [[frac(1, 5)]], [[frac(1, 7)]], [[frac(1, 9)]], ⋯",
    choices=None, derived_answer="frac(1,15)", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=1/(2n−1) → a₈=1/15 = 빠른정답 ✓.")

# p75
add(id="87108b78", qtype="short",
    question="다음 수열의 제8항을 추측해 보시오.\n[[-1]], [[3]], [[-5]], [[7]], [[-9]], ⋯",
    choices=None, derived_answer="15", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=(−1)ⁿ(2n−1) → a₈=15. 빠른정답 1과 불일치.")

# p79
add(id="6df63156", qtype="short",
    question="다음 수열의 제9항을 추측해 보시오.\n[[1]], [[frac(1, 4)]], [[frac(1, 9)]], [[frac(1, 16)]], [[frac(1, 25)]], ⋯",
    choices=None, derived_answer="frac(1,81)", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=1/n² → a₉=1/81 = 빠른정답 ✓.")

# p86
add(id="ac3567ac", qtype="short",
    question="다음 수열의 제6항을 추측해 보시오.\n[[-1]], [[2]], [[-4]], [[8]], [[-16]], ⋯",
    choices=None, derived_answer="32", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=(−1)ⁿ2^(n−1) → a₆=32. 빠른정답 10과 불일치.")

# ───────── 삼각함수의 그래프 ─────────
# p7
add(id="5ad515a9", qtype="short",
    question="함수 [[y = cos(8x)]]에 대하여 □ 안에 알맞은 것을 써넣으시오.\n그래프는 □에 대하여 대칭이다.",
    choices=None, derived_answer="y축", figure=None, difficulty_est=1, confidence=0.9,
    note="cos은 우함수 → y축 대칭. 빠른정답 frac(sqrt(3),3)과 불일치(정렬 어긋남).")

# p11
add(id="48f926c6", qtype="short",
    question="함수 [[y = tan(2x)]]에 대하여 □ 안에 알맞은 것을 써넣으시오.\n치역은 □ 전체의 집합이다.",
    choices=None, derived_answer="실수", figure=None, difficulty_est=1, confidence=0.9,
    note="tan의 치역은 실수 전체 = 빠른정답 ✓.")

# p17
add(id="e4ba9d37", qtype="choice",
    question=("두 상수 [[a]] ([[a != 0]]), [[b]]에 대하여 닫힌구간 [[itv(0, 2pi, cc)]]에서 정의된 함수 "
              "[[f(x)]] = { [[3 sin(x)]] ([[0 <= x < pi]]) ; [[a cos(x) + b]] ([[pi <= x <= 2pi]]) }가 있다. "
              "[[0 <= t <= 2pi]]인 실수 [[t]]에 대하여 [[x]]에 대한 방정식 [[f(x) = f(t)]]를 만족시키는 모든 [[x]]의 값의 합이 "
              "[[frac(7, 4) pi]]가 되도록 하는 서로 다른 모든 실수 [[t]]의 개수가 4일 때, [[pow(a, 2) + pow(b, 2)]]의 값은?"),
    choices=["[[frac(13, 2)]]", "[[frac(27, 4)]]", "[[7]]", "[[frac(29, 4)]]", "[[frac(15, 2)]]"],
    derived_answer=None, figure=None, difficulty_est=4, confidence=0.75,
    needs_review="조각적(경우 나눔) 함수 정의 f(x)={3sin x (0≤x<π); a cos x+b (π≤x≤2π)} 텍스트 혼합",
    note="출처 [2026년 3월 고3 14번/4점]. 답 미도출.")

# p53
add(id="5998fe0b", qtype="short",
    question=("다음 그림과 같이 점 [[P(4, 0)]]에서 출발하여 원 [[pow(x, 2) + pow(y, 2) = 16]] 위를 시계 반대 방향으로 움직이는 "
              "점 Q가 있다. 점 Q가 움직인 거리 [[t]]에 대하여 [[f(t) = -3 seg(PQ) + 6]]이라 하자. 함수 [[f(t)]]의 주기가 "
              "[[a pi]]이고 최댓값이 [[b]], 최솟값이 [[c]]일 때, [[a + b + c]]의 값을 구하시오. (단, [[a > 0]])"),
    choices=None, derived_answer="-4",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원 x²+y²=16 (x절편 ±4, y절편 ±4), 점 P(4,0)과 원 위의 점 Q, 선분 PQ, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 원과 두 점 P, Q·선분 PQ",
    note="PQ=8|sin(t/8)| → 주기 8π(a=8), 최대 6(b), 최소 −18(c) → −4 (빠른정답 'neg 4'와 값 일치).")

# p54
add(id="91b259cf", qtype="short",
    question=("그림과 같이 [[angle(A) = deg(90)]]인 직각이등변삼각형 ABC의 변 AB 위의 점 P, 변 BC 위의 점 Q, R, "
              "변 AC 위의 점 S를 꼭짓점으로 하는 정사각형 PQRS가 있다.\n"
              "[[angle(SBC) = theta]]라 할 때, "
              "[[frac(sin(pi + theta), cos(pi - theta)) - frac(cos(frac(pi, 2) + theta), sin(frac(pi, 2) - theta))]]의 "
              "값을 구하시오. (단, [[seg(BQ) < seg(BR)]])"),
    choices=None, derived_answer="1",
    figure=[{"fn": "unsupported", "args": {"raw": "직각이등변삼각형 ABC(∠A=90°, 밑변 BC)에 내접한 정사각형 PQRS(P∈AB, Q·R∈BC, S∈AC), 선분 BS와 ∠SBC=θ 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직각이등변삼각형 내부 정사각형 도형",
    note="식=tanθ+tanθ=2tanθ, tanθ=SR/BR=s/(2s)=1/2 → 1 = 빠른정답 ✓.")

# p56
add(id="d0cd17d1", qtype="short",
    question=("다음 그림과 같이 원에 내접하는 사각형 ABCD에 대하여 [[angle(BAD) = alpha]], [[angle(BCD) = beta]]라 할 때, "
              "[[cos(alpha) = frac(4, 5)]]이다.\n[[pow(tan(beta), 2)]]의 값을 구하시오."),
    choices=None, derived_answer="frac(9,16)",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 사각형 ABCD, 꼭짓점 A에 각 α, 꼭짓점 C에 각 β 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원에 내접하는 사각형 도형",
    note="α+β=π, tanα=3/4 → tan²β=9/16 = 빠른정답 ✓.")

# p99 — 이미지에 문항 2개 인쇄(id 1개): draft_a 대응인 상단 문항(방정식·k의 합)만 전사
add(id="14bca041", qtype="choice",
    question=("[[0 < theta < frac(pi, 2)]]일 때, [[x]]에 대한 방정식\n"
              "[[(2x + sin(theta))(x + 3 sin(theta)) = k x sin(theta) + pow(cos(theta), 2)]]의 서로 다른 두 근을 "
              "[[alpha]], [[beta]]라 하자. [[pow(alpha, 2) + pow(beta, 2) = 1]]이 되도록 하는 모든 실수 [[k]]의 값의 합은?"),
    choices=["[[8]]", "[[10]]", "[[12]]", "[[14]]", "[[16]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    needs_review="이미지에 별개 문항(이차방정식 x²−2x+2sin²θ−2cos²θ=0이 서로 다른 부호의 실근을 갖도록 하는 θ, 선지 0·π/6·7π/8·11π/8·2π) 1개가 더 인쇄됨(id 없음) — 상단 문항만 전사",
    note="2x²+(7−k)sinθ·x+3sin²θ−cos²θ=0, α²+β²=(k−7)²sin²θ/4−(3sin²θ−cos²θ)=1 → (k−7)²=16 → k=3,11 합 14 → ④. 빠른정답 3과 불일치.")

# ───────── 지수함수의 활용 ─────────
# p30
add(id="14a67174", qtype="short",
    question=("연립방정식 [[pow(2, x) + 2 × pow(3, y) = 70]], [[pow(2, x + 1) - pow(3, y) = 5]]의 근을 "
              "[[x = alpha]], [[y = beta]]라 할 때, [[alpha + beta]]의 값을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.9,
    note="2^x=16, 3^y=27 → α=4, β=3 → 7. 빠른정답 3과 불일치. 연립방정식 중괄호는 콤마 나열.")

# p31
add(id="97dbda74", qtype="short",
    question=("연립방정식 [[pow(2, x + 1) + pow(2, y + 1) = 24]], [[pow(2, x + y - 2) = 8]]의 해를\n"
              "[[x = alpha]], [[y = beta]]라 할 때, [[pow(alpha, 2) + pow(beta, 2)]]의 값을 구하시오."),
    choices=None, derived_answer="13", figure=None, difficulty_est=2, confidence=0.9,
    note="2^x+2^y=12, x+y=5 → {2^x,2^y}={4,8} → (2,3) → 13 = 빠른정답 ✓.")

# p44
add(id="62493ff9", qtype="choice",
    question=("다음 그림과 같이 가로줄 [[sub(l, 1)]], [[sub(l, 2)]], [[sub(l, 3)]]과 세로줄 [[sub(l, 4)]], [[sub(l, 5)]], [[sub(l, 6)]]이 "
              "만나는 곳에 있는 9개의 메모판에 모두 [[x]]에 대한 식이 하나씩 적혀 있고, 그 중 4개의 메모판은 접착 메모지로 "
              "가려져 있다. [[x = a]]일 때,\n"
              "각 줄 [[sub(l, k)]] ([[k]] = 1, 2, 3, 4, 5, 6)에 있는 3개의 메모판에 적혀 있는 모든 식의 값의 합을 [[sub(S, k)]]라 하자.\n"
              "[[sub(S, k)]] ([[k]] = 1, 2, 3, 4, 5, 6)의 값이 모두 같게 되는 모든 실수 [[a]]의 값의 합은?"),
    choices=["[[2 + log(3, 2)]]", "[[3 + log(3, 2)]]", "[[4 + log(3, 2)]]", "[[3 + 2 log(3, 2)]]", "[[4 + 2 log(3, 2)]]"],
    derived_answer="③",
    figure=[{"fn": "table", "args": {"head": ["", "l₄", "l₅", "l₆"],
                                     "rows": [["l₁", "9^x", "(가려짐)", "−3^(x+2)"],
                                              ["l₂", "(가려짐)", "3^(x+2) − 81", "(가려짐)"],
                                              ["l₃", "−3^(x+2)", "3^(x+2) − 81", "(가려짐)"]]}}],
    difficulty_est=3, confidence=0.85,
    note="출처 [2019년 11월 고2 문과 18번 변형]. 메모판 격자를 표로 표현. 9^x−3^(x+2)=2(3^(x+2)−81) → 3^x=9,18 → a=2, 2+log₃2 합 4+log₃2 → ③ = 빠른정답 ✓.")

# p48
add(id="27023612", qtype="choice",
    question=("다음은 어느 지역의 방음벽, 배수로, 도로를 나타낸 평면도이다. 평면도에서 방음벽을 [[x]]축, "
              "방음벽과 수직으로 건설된 배수로를 [[y]]축으로 할 때, 도로의 중앙선은 곡선 [[y = pow(a, x) + 2]] ([[a > 1]])의 일부로 "
              "나타내어진다. [[seg(AB) = seg(BC) = 2]]를 만족시키는 [[x]]축 위의 세 점 A, B, C를 지나고 [[x]]축에 수직인 세 직선을 그어 "
              "곡선 [[y = pow(a, x) + 2]]와 만나는 점을 각각 D, E, F라 하자.\n"
              "[[seg(AD) = frac(12, 5)]], [[seg(BE) = frac(9, 2)]], [[seg(CF) = h]]일 때, 상수 [[h]]의 값은?\n"
              "(단, 방음벽, 배수로, 도로의 중앙선의 폭은 무시한다.)"),
    choices=["[[frac(121, 8)]]", "[[frac(125, 8)]]", "[[frac(137, 8)]]", "[[frac(141, 8)]]", "[[frac(155, 8)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "평면도 삽화: 방음벽(x축)·배수로(y축)·도로 곡선·호수, x축 위 점 A, B, C(간격 2)와 곡선 위 점 D, E, F, 길이 12/5, 9/2, h 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평면도 삽화(지수함수 곡선·점 A~F)",
    note="출처 [2011년 4월 고3 이과 16번/4점]. a^t=2/5, a^(t+2)=5/2 → a²=25/4 → a^(t+4)=125/8 → h=141/8 → ④. 빠른정답 2와 불일치.")

# p54
add(id="5c23bc3d", qtype="choice",
    question=("두 집합 [[A = setb(x, pow(frac(1, 3), x + 2) < pow(frac(1, 3), pow(x, 2)))]],\n"
              "[[B = setb(x, pow(2, abs(x - 2)) <= pow(2, a))]] 에 대하여\n"
              "[[inter(A, B) = A]] 가 성립하도록 하는 실수 [[a]]의 최솟값은?"),
    choices=CH_15, derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2011년 9월 고2 문과 21번/4점]. A: −1<x<2, B: 2−a≤x≤2+a, A⊂B ⇔ a≥3 → ③. 빠른정답 2와 불일치.")

# p99 — 이미지에 문항 2개 인쇄(id 1개): 선지 ①~⑤가 딸린 하단 문항(지원비)으로 전사
add(id="d22d1b34", qtype="choice",
    question=("어느 연구소에서는 매년 두 부서 A, B에 대한 실험 지원비를 전년도에 비해 각각 [[pct(20)]], [[pct(28)]]씩 늘려간다고 "
              "한다. 현재 두 부서 A, B의 실험 지원비가 각각 2000만 원, 1000만 원일 때, 부서 B의 실험 지원비가 부서 A의 실험 "
              "지원비를 처음으로 초과하는 해는 지금으로부터 몇 년 후인가?\n"
              "(단, [[log(2) = 0.3]], [[log(3) = 0.48]]로 계산한다.)"),
    choices=["12년", "14년", "16년", "18년", "20년"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    needs_review="이미지 상단에 별개 문항(세균 A·B 배양, 합이 96 이상이 되는 최소 시간 — 단답형, 답 3시간) 함께 인쇄됨(id 없음) — 선지형 지원비 문항으로 전사",
    note="2·1.2ⁿ<1.28ⁿ → n(log1.28−log1.2)>log2 → n·0.02>0.3 → n=16 → ③ = 빠른정답 ✓.")

# ───────── 수학적 귀납법 ─────────
# p4
add(id="9e5acdce", qtype="choice",
    question=("3, 8, 13, 18⋯인 자연수 [[n]]에 대하여 명제 [[p(n)]]이 성립함을 수학적 귀납법을 이용하여 증명하려면 다음을 보여야 한다.\n"
              "(ⅰ) [[n]] = (가) 일 때, [[p(n)]]이 성립함을 보인다.\n"
              "(ⅱ) [[n = k]]일 때, [[p(n)]]이 성립한다고 가정하면 [[n]] = (나) 일 때도 [[p(n)]]이 성립함을 보인다.\n"
              "이때 (가), (나)에 알맞은 것을 차례대로 적은 것은?"),
    choices=["[[1]], [[k + 1]]", "[[1]], [[4k + 1]]", "[[3]], [[k + 5]]", "[[3]], [[5k - 2]]", "[[3]], [[5k + 3]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="첫항 3, 공차 5 → (가)=3, (나)=k+5 → ③. 빠른정답 7과 불일치.")

# p5
add(id="a6d6d2e2", qtype="choice",
    question=("2, 8, 14, 20, ⋯인 자연수 [[n]]에 대하여 명제 [[p(n)]]이 성립함을 수학적 귀납법을 이용하여 증명하려면 다음을 보여야 한다.\n"
              "(ⅰ) [[n]] = (가) 일 때, [[p(n)]]이 성립함을 보인다.\n"
              "(ⅱ) [[n = k]]일 때, [[p(n)]]이 성립한다고 가정하면 [[n]] = (나) 일 때도 [[p(n)]]이 성립함을 보인다.\n"
              "이때 (가), (나)에 알맞은 것을 차례대로 적은 것은?"),
    choices=["[[1]], [[k + 1]]", "[[1]], [[2k + 2]]", "[[2]], [[k + 6]]", "[[2]], [[6k - 4]]", "[[8]], [[6k - 4]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="첫항 2, 공차 6 → (가)=2, (나)=k+6 → ③. 빠른정답 10과 불일치.")

# p7
add(id="acffdef4", qtype="choice",
    question=("자연수 [[n]]에 대한 명제 [[p(n)]]이 모든 짝수에 대하여 성립함을 수학적 귀납법으로 증명하려면 다음을 보여야 한다.\n"
              "(ⅰ) [[n]] = (가) 일 때, [[p(n)]]이 성립함을 보인다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때, [[p(n)]]이 성립한다고 가정하면 [[n]] = (나) 일 때도 [[p(n)]]이 성립함을 보인다.\n"
              "이때 (가), (나)에 알맞은 것은?"),
    choices=["[[1]], [[k + 1]]", "[[1]], [[k + 2]]", "[[2]], [[k + 1]]", "[[2]], [[k + 2]]", "[[2]], [[2k]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="짝수 전체: (가)=2, (나)=k+2 → ④ = 빠른정답 ✓.")

# p31
add(id="71a8f1ee", qtype="choice",
    question=("다음은 수열 [[set(sub(a, n))]]의 일반항 [[sub(a, n)]]이 [[sub(a, n) = p n + q]]일 때,\n"
              "모든 자연수 [[n]]에 대하여\n"
              "[[n sub(a, 1) + (n - 1) sub(a, 2) + (n - 2) sub(a, 3)]] + ⋯ + [[sub(a, n)]]\n"
              "= [[frac(1, 6) n(n + 1)(p n + 2p + 3q)]]\n"
              "임을 수학적 귀납법으로 증명한 것이다.\n\n[증명]\n"
              "(ⅰ) [[n = 1]]일 때, (좌변)=(우변)=[[p + q]]이므로 성립한다.\n"
              "(ⅱ) [[n = k]]일 때 성립한다고 가정하면\n"
              "[[k sub(a, 1) + (k - 1) sub(a, 2) + (k - 2) sub(a, 3)]] + ⋯ + [[sub(a, k)]]\n"
              "= [[frac(1, 6) k(k + 1)(p k + 2p + 3q)]]\n"
              "이 식의 양변에 (가) 를 더하면\n"
              "[[k sub(a, 1) + (k - 1) sub(a, 2) + (k - 2) sub(a, 3)]] + ⋯ + [[sub(a, k)]] + (가)\n"
              "= [[frac(1, 6) k(k + 1)(p k + 2p + 3q)]] + (가)\n"
              "= [[frac(1, 6) (k + 1)]]{[[p pow(k, 2)]] + (나) [[k]] + [[6(p + q)]]}\n"
              "= [[frac(1, 6) (k + 1)(k + 2)(p(k + 1) + 2p + 3q)]]\n"
              "그러므로 [[n]] = (다) 일 때도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 주어진 등식은 모든 자연수 [[n]]에 대하여 성립한다.\n\n"
              "이 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[sub(a, 1) + sub(a, 2)]] + ⋯ + [[sub(a, k + 1)]], (나) [[5p + 3q]], (다) [[k]]",
             "(가) [[sub(a, 1) + sub(a, 2)]] + ⋯ + [[sub(a, k + 1)]], (나) [[5p + 3q]], (다) [[k + 1]]",
             "(가) [[sub(a, 1) + sub(a, 2)]] + ⋯ + [[sub(a, k + 1)]], (나) [[3p + 5q]], (다) [[k + 1]]",
             "(가) [[sub(a, 1) + sub(a, 2)]] + ⋯ + [[sub(a, k)]], (나) [[5p + 3q]], (다) [[k + 1]]",
             "(가) [[sub(a, 1) + sub(a, 2)]] + ⋯ + [[sub(a, k)]], (나) [[3p + 5q]], (다) [[k]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="(가)=a₁+⋯+a_(k+1), (나)=5p+3q (k(pk+2p+3q)+3p(k+2)+6q 전개), (다)=k+1 → ② = 빠른정답 ✓. 빈칸·줄임표는 텍스트.")

# p32 (id 3개)
dup(["6c29883a", "f03a9f14", "d80e13fc"], qtype="choice",
    question=("수열 [[set(sub(a, n))]]의 일반항은 [[sub(a, n) = 2n + 1]]이다.\n"
              "다음은 모든 자연수 [[n]]에 대하여\n"
              "[[2 pow(sum(k, 1, n, sub(a, k)), 2) = sum(k, 1, n, pow((sub(a, k)), 3)) - 3 sum(k, 1, n, sub(a, k))]] ⋯ (∗)\n"
              "이 성립함을 수학적 귀납법을 이용하여 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때,\n"
              "(좌변)=[[2 pow(sum(k, 1, 1, sub(a, k)), 2)]] = (가),\n"
              "(우변)=[[sum(k, 1, 1, pow((sub(a, k)), 3)) - 3 sum(k, 1, 1, sub(a, k))]] = (가)\n"
              "이므로 (∗)이 성립한다.\n"
              "(ⅱ) [[n = m]] ([[m >= 1]])일 때, (∗)이 성립한다고 하면\n"
              "[[2 pow(sum(k, 1, m, sub(a, k)), 2) = sum(k, 1, m, pow((sub(a, k)), 3)) - 3 sum(k, 1, m, sub(a, k))]]이므로\n"
              "[[2 pow(sum(k, 1, m + 1, sub(a, k)), 2)]]\n"
              "= [[2 pow(sum(k, 1, m, sub(a, k)) + sub(a, m + 1), 2)]]\n"
              "= [[2 pow(sum(k, 1, m, sub(a, k)), 2) + 4 (sum(k, 1, m, sub(a, k))) sub(a, m + 1) + 2 pow((sub(a, m + 1)), 2)]]\n"
              "= [[sum(k, 1, m, pow((sub(a, k)), 3)) - 3 sum(k, 1, m, sub(a, k)) + 4 (sum(k, 1, m, sub(a, k))) sub(a, m + 1) + 2 pow((sub(a, m + 1)), 2)]]\n"
              "= [[sum(k, 1, m, pow((sub(a, k)), 3))]] + (나) [[sum(k, 1, m, sub(a, k)) + 2 pow((sub(a, m + 1)), 2)]]\n"
              "= [[sum(k, 1, m, pow((sub(a, k)), 3)) + pow((sub(a, m + 1)), 3) - (3 pow(m, 2) + 12m + 9)]]\n"
              "= [[sum(k, 1, m + 1, pow((sub(a, k)), 3)) - 3 sum(k, 1, m + 1, sub(a, k))]]\n"
              "즉, [[n = m + 1]]일 때에도 (∗)이 성립한다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여 (∗)이 성립한다.\n\n"
              "위의 (가)에 알맞은 수를 [[p]], (나)에 알맞은 식을 [[f(m)]]이라 할 때, [[f(p)]]의 값은?"),
    choices=["[[135]]", "[[144]]", "[[153]]", "[[162]]", "[[171]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="(가)=2·3²=18, (나)=4a_(m+1)−3=8m+9 → f(18)=153 → ③. 빠른정답 5와 불일치(검산: (8m+9)(m²+2m)+2(2m+3)²=(2m+3)³−(3m²+12m+9) 성립).")

# p34
add(id="d740c738", qtype="choice",
    question=("다음은 자연수 [[n]]에 대하여\n"
              "[[1 = pow(1, 3)]]\n[[3 + 5 = pow(2, 3)]]\n[[7 + 9 + 11 = pow(3, 3)]]\n[[13 + 15 + 17 + 19 = pow(4, 3)]]\n⋮\n"
              "[[sum(i, 1, n, 2i + pow(n, 2) - n - 1) = pow(n, 3)]]\n"
              "이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n[증명]\n"
              "(ⅰ) [[n = 1]]일 때, [[2 × 1 + pow(1, 2) - 1 - 1 = pow(1, 3)]]이므로 성립한다.\n"
              "(ⅱ) [[n = k]]일 때 성립한다고 가정하면\n"
              "[[sum(i, 1, k, 2i + pow(k, 2) - k - 1) = pow(k, 3)]]이다.\n"
              "[[n = k + 1]]일 때 성립함을 보이자.\n"
              "Σ[i=1..k+1] (가)\n"
              "= [[sum(i, 1, k, 2i + pow(k, 2) - k - 1) + sum(i, 1, k, 2k)]] + (나)\n"
              "= [[pow(k, 3) + 3 pow(k, 2) + 3k + 1]]\n"
              "= [[pow(k + 1, 3)]]\n"
              "그러므로 [[n = k + 1]]일 때도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의해서 모든 자연수 [[n]]에 대하여 성립한다.\n\n"
              "이 증명에서 (가), (나)에 알맞은 것은?"),
    choices=["(가) [[2i + pow(k, 2) + k - 1]], (나) [[pow(k, 2) + 3k + 1]]",
             "(가) [[2i + pow(k, 2) + k - 1]], (나) [[pow(k, 2) - 3k + 1]]",
             "(가) [[2i + pow(k, 2) + k + 1]], (나) [[pow(k, 2) + 3k + 1]]",
             "(가) [[2i + pow(k, 2) - k + 1]], (나) [[pow(k, 2) - 3k + 1]]",
             "(가) [[2i + pow(k, 2) - k + 1]], (나) [[pow(k, 2) + 3k + 1]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2006년 4월 고3 이과 15번]. (가)=2i+(k+1)²−(k+1)−1=2i+k²+k−1, (나)=i=k+1항=2(k+1)+k²+k−1=k²+3k+1 → ①. 빠른정답 2와 불일치. 합 기호의 첨자 i는 파서상 상수 i로 처리됨.")

# p35
add(id="a07758e5", qtype="choice",
    question=("수열 [[set(sub(a, n))]]의 일반항은 [[sub(a, n) = n + 2]]이다.\n"
              "다음은 모든 자연수 [[n]]에 대하여\n"
              "[[pow(sum(k, 1, n, sub(a, k)), 2) = sum(k, 1, n, pow((sub(a, k)), 3)) - 6 sum(k, 1, n, sub(a, k))]] ⋯⋯(∗)\n"
              "가 성립함을 수학적 귀납법을 이용하여 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때,\n"
              "(좌변)=[[pow(sum(k, 1, 1, sub(a, k)), 2)]] = (가),\n"
              "(우변)=[[sum(k, 1, 1, pow((sub(a, k)), 3)) - 6 sum(k, 1, 1, sub(a, k))]] = (가)\n"
              "이므로 (∗)이 성립한다.\n"
              "(ⅱ) [[n = m]] ([[m >= 1]])일 때, (∗)이 성립한다고 가정하면\n"
              "[[pow(sum(k, 1, m, sub(a, k)), 2) = sum(k, 1, m, pow((sub(a, k)), 3)) - 6 sum(k, 1, m, sub(a, k))]]이므로\n"
              "[[pow(sum(k, 1, m + 1, sub(a, k)), 2)]]\n"
              "= [[pow(sum(k, 1, m, sub(a, k)) + sub(a, m + 1), 2)]]\n"
              "= [[pow(sum(k, 1, m, sub(a, k)), 2) + 2 (sum(k, 1, m, sub(a, k))) sub(a, m + 1) + pow((sub(a, m + 1)), 2)]]\n"
              "= [[sum(k, 1, m, pow((sub(a, k)), 3)) - 6 sum(k, 1, m, sub(a, k)) + 2 (sum(k, 1, m, sub(a, k))) sub(a, m + 1) + pow((sub(a, m + 1)), 2)]]\n"
              "= [[sum(k, 1, m, pow((sub(a, k)), 3))]] + (나) [[sum(k, 1, m, sub(a, k)) + pow((sub(a, m + 1)), 2)]]\n"
              "= [[sum(k, 1, m, pow((sub(a, k)), 3)) + pow((sub(a, m + 1)), 3) - (3 pow(m, 2) + 21m + 18)]]\n"
              "= [[sum(k, 1, m + 1, pow((sub(a, k)), 3)) - 6 sum(k, 1, m + 1, sub(a, k))]]\n"
              "즉, [[n = m + 1]]일 때에도 (∗)이 성립한다.\n"
              "따라서 (ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여 (∗)이 성립한다.\n\n"
              "위의 (가)에 알맞은 수를 [[p]], (나)에 알맞은 식을 [[f(m)]]이라 할 때, [[f(p)]]의 값은?"),
    choices=["[[15]]", "[[16]]", "[[17]]", "[[18]]", "[[19]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="(가)=3²=9, (나)=2a_(m+1)−6=2m → f(9)=18 → ④. 빠른정답 3과 불일치.")

# p37
add(id="ea8dafbd", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "Σ[k=1..n] [[k]]{[[k + (k + 1) + (k + 2)]] + ⋯ + [[n]]}\n"
              "= [[frac(n(n + 1)(n + 2)(3n + 1), 24)]] ⋯ (∗)\n"
              "이 성립함을 수학적 귀납법으로 증명하는 과정이다.\n\n"
              "(ⅰ) [[n = 1]]일 때,\n(좌변)=(우변)= (가) 이므로 (∗)이 성립한다.\n"
              "(ⅱ) [[n = m]]일 때, (∗)이 성립한다고 가정하면\n"
              "Σ[k=1..m] [[k]]{[[k + (k + 1) + (k + 2)]] + ⋯ + [[m]]}\n"
              "= [[frac(m(m + 1)(m + 2)(3m + 1), 24)]]이다.\n"
              "[[n = m + 1]]일 때, (∗)이 성립함을 보이자.\n"
              "Σ[k=1..m+1] [[k]]{[[k + (k + 1) + (k + 2)]] + ⋯ + [[(m + 1)]]}\n"
              "= Σ[k=1..m] [[k]]{[[k + (k + 1) + (k + 2)]] + ⋯ + [[(m + 1)]]} + (나)\n"
              "= (다) + [[frac(m pow(m + 1, 2), 2)]] + (나)\n"
              "= [[frac((m + 1)(m + 2)(m + 3)(3m + 4), 24)]]\n"
              "따라서 [[n = m + 1]]일 때도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여 (∗)이 성립한다.\n\n"
              "위의 (가)에 알맞은 수를 [[a]],\n(나), (다)에 알맞은 식을 각각 [[f(m)]], [[g(m)]]이라 할 때,\n"
              "[[a + f(2) + g(3)]]의 값은?"),
    choices=["[[35]]", "[[36]]", "[[37]]", "[[38]]", "[[39]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2018년 3월 고2 이과 17번/4점]. a=1, (나)=(m+1)², (다)=m(m+1)(m+2)(3m+1)/24 → 1+9+25=35 → ① = 빠른정답 ✓. Σ 안의 줄임표는 텍스트.")

# p38
add(id="e08d5fe3", qtype="choice",
    question=("수열 [[set(sub(a, n))]]의 일반항은\n"
              "[[sub(a, n) = (pow(2, 2n) - 1) × pow(2, n(n - 1)) + (n - 1) × pow(2, -n)]]\n"
              "이다. 다음은 모든 자연수 [[n]]에 대하여\n"
              "[[sum(k, 1, n, sub(a, k)) = pow(2, n(n + 1)) - (n + 1) × pow(2, -n)]] ⋯ (∗)\n"
              "임을 수학적 귀납법을 이용하여 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때, (좌변)=[[3]], (우변)=[[3]]이므로 (∗)이 성립한다.\n"
              "(ⅱ) [[n = m]]일 때, (∗)이 성립한다고 가정하면\n"
              "[[sum(k, 1, m, sub(a, k)) = pow(2, m(m + 1)) - (m + 1) × pow(2, -m)]]\n"
              "이다. [[n = m + 1]]일 때,\n"
              "[[sum(k, 1, m + 1, sub(a, k))]]\n"
              "= [[pow(2, m(m + 1)) - (m + 1) × pow(2, -m)]] + [[(pow(2, 2m + 2) - 1)]] × (가) + [[m × pow(2, -m - 1)]]\n"
              "= (가) × (나) − [[frac(m + 2, 2) × pow(2, -m)]]\n"
              "= [[pow(2, (m + 1)(m + 2)) - (m + 2) × pow(2, -(m + 1))]]\n"
              "이다.\n따라서 [[n = m + 1]]일 때도 (∗)이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여\n"
              "[[sum(k, 1, n, sub(a, k)) = pow(2, n(n + 1)) - (n + 1) × pow(2, -n)]]이다.\n\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(m)]], [[g(m)]]이라 할 때, [[frac(g(6), f(2))]]의 값은?"),
    choices=["[[32]]", "[[64]]", "[[128]]", "[[256]]", "[[512]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="(가)=2^(m(m+1)), (나)=2^(2m+2) → g(6)/f(2)=2¹⁴/2⁶=256 → ④ = 빠른정답 ✓.")

# p41
add(id="35dde57f", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[(pow(1, 2) + 1) × fact(1) + (pow(2, 2) + 1) × fact(2)]] + ⋯ + [[(pow(n, 2) + 1) × fact(n) = n × fact(n + 1)]]\n"
              "이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n<증명>\n"
              "(1) [[n = 1]]일 때, (좌변)=[[2]], (우변)=[[2]]이므로 주어진 등식은 성립한다.\n"
              "(2) [[n = k]]일 때 성립한다고 가정하면\n"
              "[[(pow(1, 2) + 1) × fact(1) + (pow(2, 2) + 1) × fact(2)]] + ⋯ + [[(pow(k, 2) + 1) × fact(k) = k × fact(k + 1)]]\n"
              "이다. [[n = k + 1]]일 때 성립함을 보이자.\n"
              "[[(pow(1, 2) + 1) × fact(1) + (pow(2, 2) + 1) × fact(2)]] + ⋯ + [[(pow(k, 2) + 1) × fact(k) + (pow(k + 1, 2) + 1) × fact(k + 1)]]\n"
              "= (가) + [[(pow(k + 1, 2) + 1) × fact(k + 1)]]\n"
              "= ((나)) × [[fact(k + 1)]]\n"
              "= [[(k + 1)]] × (다)\n"
              "그러므로 [[n = k + 1]]일 때도 성립한다.\n"
              "따라서 모든 자연수 [[n]]에 대하여 주어진 등식은 성립한다.\n\n"
              "위 증명에서 (가), (나), (다)에 들어갈 식으로 알맞은 것은?"),
    choices=["(가) [[k × fact(k + 1)]], (나) [[pow(k, 2) + 2k + 1]], (다) [[fact(k + 1)]]",
             "(가) [[k × fact(k + 1)]], (나) [[pow(k, 2) + 3k + 2]], (다) [[fact(k + 2)]]",
             "(가) [[k × fact(k + 1)]], (나) [[pow(k, 2) + 3k + 2]], (다) [[fact(k + 1)]]",
             "(가) [[(k + 1) × fact(k + 1)]], (나) [[pow(k, 2) + 3k + 2]], (다) [[fact(k + 2)]]",
             "(가) [[(k + 1) × fact(k + 1)]], (나) [[pow(k, 2) + 2k + 1]], (다) [[fact(k + 1)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2007년 11월 고3 이과 11번]. (가)=k·(k+1)!, (나)=k+(k+1)²+1=k²+3k+2, (다)=(k+2)! → ② = 빠른정답 ✓.")

# p43
add(id="9d193e1f", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[frac(16, 5) + frac(32, pow(5, 2)) + frac(48, pow(5, 3))]] + ⋯ + [[frac(16n, pow(5, n)) = 5 - frac(4n + 5, pow(5, n))]] ⋯ (∗)\n"
              "가 성립함을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때,\n"
              "(좌변)=[[frac(16, 5)]], (우변)=[[5 - frac(9, 5) = frac(16, 5)]]\n"
              "이므로 (∗)이 성립한다.\n"
              "(ⅱ) [[n = k]]일 때, (∗)이 성립한다고 가정하면\n"
              "[[frac(16, 5) + frac(32, pow(5, 2)) + frac(48, pow(5, 3))]] + ⋯ + [[frac(16k, pow(5, k)) = 5 - frac(4k + 5, pow(5, k))]]\n"
              "이다.\n"
              "위 등식의 양변에 [[frac(16(k + 1), pow(5, k + 1))]]을 더하여 정리하면\n"
              "[[frac(16, 5) + frac(32, pow(5, 2)) + frac(48, pow(5, 3))]] + ⋯ + [[frac(16k, pow(5, k)) + frac(16(k + 1), pow(5, k + 1))]]\n"
              "= [[5]] − [[frac(1, pow(5, k))]]{[[(4k + 5)]] − ((가))}\n"
              "= [[5]] − ((나))/[[pow(5, k + 1)]]\n"
              "따라서 [[n = k + 1]]일 때도 (∗)이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여\n모든 자연수 [[n]]에 대하여 (∗)이 성립한다.\n\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(k)]], [[g(k)]]라 할 때,\n[[f(1) × g(4)]]의 값은?"),
    choices=["[[150]]", "[[160]]", "[[170]]", "[[180]]", "[[190]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2016년 4월 고3 문과 18번 변형]. (가)=16(k+1)/5, (나)=4k+9 → f(1)g(4)=(32/5)·25=160 → ②. 빠른정답 5와 불일치.")

# p44
add(id="159b77c4", qtype="short",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[1 + 5 + pow(5, 2)]] + ⋯ + [[pow(5, n - 1) = frac(pow(5, n) - 1, 4)]] ⋯ ㉠\n"
              "이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때\n(좌변)=[[1]], (우변)=[[frac(pow(5, 1) - 1, 4) = 1]]\n따라서 ㉠이 성립한다.\n"
              "(ⅱ) [[n = k]]일 때, ㉠이 성립한다고 가정하면\n"
              "[[1 + 5 + pow(5, 2)]] + ⋯ + [[pow(5, k - 1) = frac(pow(5, k) - 1, 4)]]\n"
              "위의 식의 양변에 (가) 을 더하면\n"
              "[[1 + 5 + pow(5, 2)]] + ⋯ + [[pow(5, k - 1)]] + (가)\n"
              "= [[frac(pow(5, k) - 1, 4)]] + (가)\n"
              "= (나)\n"
              "따라서 [[n = k + 1]]일 때도 ㉠이 성립한다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여 ㉠이 성립한다.\n\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 각각 [[f(k)]], [[g(k)]]라 할 때, [[f(3) + g(2)]]의 값을 구하시오."),
    choices=None, derived_answer="156", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=5^k, (나)=(5^(k+1)−1)/4 → f(3)+g(2)=125+31=156. 빠른정답 2와 불일치.")

# p47
add(id="6cc793c8", qtype="short",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[1 × 6 + 2 × 7 + 3 × 8]] + ⋯ + [[n(n + 5) = frac(n(n + 1)(n + 8), 3)]]\n"
              "가 성립함을 수학적 귀납법으로 증명한 것이다.\n\n<증명>\n"
              "(ⅰ) [[n = 1]]일 때,\n(좌변)=[[1 × 6 = 6]], (우변)=[[frac(1 × 2 × 9, 3) = 6]]\n따라서 주어진 등식이 성립한다.\n"
              "(ⅱ) [[n = k]]일 때 주어진 등식이 성립한다고 가정하면\n"
              "[[1 × 6 + 2 × 7 + 3 × 8]] + ⋯ + [[k(k + 5) = frac(k(k + 1)(k + 8), 3)]]\n"
              "위의 식의 양변에 (가) 을 더하면\n"
              "[[1 × 6 + 2 × 7]] + ⋯ + [[k(k + 5)]] + ((가))\n"
              "= [[frac(k(k + 1)(k + 8), 3)]] + (가)\n"
              "= ((나))/[[3]]\n"
              "따라서 [[n = k + 1]]일 때도 주어진 등식이 성립한다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여 주어진 등식이 성립한다.\n\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 각각 [[f(k)]], [[g(k)]]라 할 때, [[f(3) + g(3)]]의 값을 구하시오."),
    choices=None, derived_answer="276", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=(k+1)(k+6), (나)=(k+1)(k+2)(k+9) → 36+240=276 = 빠른정답 ✓.")

# p48
add(id="3ab2a808", qtype="short",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[1 × 3 + 2 × 4 + 3 × 5]] + ⋯ + [[n(n + 2) = frac(n(n + 1)(2n + 7), 6)]]\n"
              "이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n<증명>\n"
              "(ⅰ) [[n = 1]]일 때,\n(좌변)=[[1 × 3 = 3]], (우변)=[[frac(1 × 2 × 9, 6) = 3]]\n따라서 주어진 등식이 성립한다.\n"
              "(ⅱ) [[n = k]]일 때 주어진 등식이 성립한다고 가정하면\n"
              "[[1 × 3 + 2 × 4 + 3 × 5]] + ⋯ + [[k(k + 2) = frac(k(k + 1)(2k + 7), 6)]]\n"
              "위의 식의 양변에 (가) 을 더하면\n"
              "[[1 × 3 + 2 × 4]] + ⋯ + [[k(k + 2)]] + ((가))\n"
              "= [[frac(k(k + 1)(2k + 7), 6)]] + (가)\n"
              "= ((나))/[[6]]\n"
              "따라서 [[n = k + 1]]일 때도 주어진 등식이 성립한다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여 주어진 등식이 성립한다.\n\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 각각 [[f(k)]], [[g(k)]]라 할 때, [[f(3) + g(3)]]의 값을 구하시오."),
    choices=None, derived_answer="324", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=(k+1)(k+3), (나)=(k+1)(k+2)(2k+9) → 24+300=324. 빠른정답 2와 불일치.")

# p49
add(id="a7808949", qtype="choice",
    question=("자연수 [[N]]을 음이 아닌 정수 [[m]]과 홀수 [[p]]에 대하여 [[N = pow(2, m) × p]]로 나타낼 때, [[f(N) = m]]이라 하자. "
              "예를 들어, [[28 = pow(2, 2) × 7]]이므로 [[f(28) = 2]]이다.\n"
              "다음은 모든 자연수 [[n]]에 대하여\n"
              "[[f(pow(5, 2n - 1) + 1) = 1]]임을 수학적 귀납법을 이용하여 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때,\n[[pow(5, 1) + 1 = pow(2, 1) × 3]]이므로\n[[f(pow(5, 1) + 1) = 1]]이다.\n"
              "따라서 [[n = 1]]일 때 [[f(pow(5, 2n - 1) + 1) = 1]]이 성립한다.\n"
              "(ⅱ) [[n = k]]일 때 [[f(pow(5, 2n - 1) + 1) = 1]]이 성립한다고 가정하면\n"
              "[[f(pow(5, 2k - 1) + 1) = 1]]\n"
              "음이 아닌 정수 [[m]]과 홀수 [[p]]에 대하여\n"
              "[[pow(5, 2k - 1) + 1 = pow(2, m) × p]]\n"
              "로 나타낼 수 있으므로\n"
              "[[pow(5, 2k - 1) + 1]] = (가) × [[p]]\n"
              "이다.\n"
              "[[pow(5, 2(k + 1) - 1) + 1 = 25 × pow(5, 2k - 1) + 1]]\n"
              "= [[2]] × ((나))\n"
              "이고, [[p]]는 홀수이므로 (나) 도 홀수이다.\n"
              "따라서 [[f(pow(5, 2(k + 1) - 1) + 1) = 1]]이다.\n"
              "그러므로 [[n = k + 1]]일 때도\n[[f(pow(5, 2n - 1) + 1) = 1]]이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여\n[[f(pow(5, 2n - 1) + 1) = 1]]이다.\n\n"
              "위의 (가)에 알맞은 수를 [[a]], (나)에 알맞은 식을 [[g(p)]]라 할 때, [[a + g(2)]]의 값은?"),
    choices=["[[35]]", "[[40]]", "[[45]]", "[[50]]", "[[55]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2017년 3월 고2 이과 16번 변형]. (가)=2, 25(2p−1)+1=2(25p−12) → (나)=25p−12, g(2)=38 → 40 → ② = 빠른정답 ✓.")

# p54 — 배수의 증명
add(id="1b7d7377", qtype="short",
    question=("다음은 모든 자연수 [[n]]에 대하여 [[pow(2, n + 1) + pow(3, 2n - 1)]]이 7의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "[[f(n) = pow(2, n + 1) + pow(3, 2n - 1)]]로 놓으면\n"
              "(ⅰ) [[n = 1]]일 때,\n"
              "[[f(1) = pow(2, 2) + pow(3, 1) = 7]]이므로 [[f(1)]]은 7의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때, [[f(k)]]가 7의 배수라고 가정하면\n"
              "[[f(k + 1) = pow(2, k + 2) + pow(3, 2k + 1)]]\n"
              "= (가) × [[f(k)]] − (가) × [[pow(3, 2k - 1)]] + [[pow(3, 2k + 1)]]\n"
              "= (가) × [[f(k)]] + [[7]] × (나)\n"
              "이므로 [[f(k + 1)]]도 7의 배수이다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여\n"
              "[[pow(2, n + 1) + pow(3, 2n - 1)]]은 7의 배수이다.\n\n"
              "위의 (가)에 알맞은 수를 [[a]], (나)에 알맞은 식을 [[g(k)]]라 할 때, [[g(a)]]의 값을 구하시오."),
    choices=None, derived_answer="27", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=2, (나)=3^(2k−1) → g(2)=3³=27. 빠른정답 3과 불일치.")

# p56
add(id="400d9d2e", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여 [[n(pow(n, 2) + 5)]]가 6의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때,\n[[1 × (pow(1, 2) + 5) = 6]]이므로 6의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때, [[n(pow(n, 2) + 5)]]가 6의 배수라 가정하면\n"
              "[[k(pow(k, 2) + 5) = 6N]] ([[N]]은 자연수)으로 놓을 수 있다.\n"
              "이때, [[n = k + 1]]이면\n"
              "[[(k + 1)(pow(k + 1, 2) + 5) = pow(k, 3) + 3 pow(k, 2)]] + (가)\n"
              "= (나) + [[6 + 3k(k + 1)]]\n"
              "= (다) [[(N + 1) + 3k(k + 1)]]\n"
              "이고, [[3k(k + 1)]]이 (다) 의 배수이므로\n"
              "[[n = k + 1]]일 때도 [[n(pow(n, 2) + 5)]]가 6의 배수이다.\n"
              "(ⅰ), (ⅱ)에 의해 모든 자연수 [[n]]에 대하여 [[n(pow(n, 2) + 5)]]는 6의 배수이다.\n\n"
              "위의 증명 과정에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[8k + 2]], (나) [[pow(k, 3) + 5k]], (다) [[2]]",
             "(가) [[8k + 2]], (나) [[pow(k, 3) + 6k]], (다) [[6]]",
             "(가) [[8k + 6]], (나) [[pow(k, 3) + 5k]], (다) [[2]]",
             "(가) [[8k + 6]], (나) [[pow(k, 3) + 5k]], (다) [[6]]",
             "(가) [[8k + 6]], (나) [[pow(k, 3) + 6k]], (다) [[2]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(k+1)(k²+2k+6)=k³+3k²+8k+6 → (가)=8k+6, (나)=k³+5k, (다)=6 → ④. 빠른정답 125와 불일치.")

# p58
add(id="6c3066a2", qtype="choice",
    question=("수열 [[set(sub(a, n))]]이\n"
              "[[sub(a, 1) = 2]], [[sub(a, 1) + sub(a, 2) + sub(a, 3)]] + ⋯ + [[sub(a, n) = frac(n + 1, 2) sub(a, n)]] ([[n >= 1]])\n"
              "으로 정의될 때, 다음은 수열 [[set(sub(a, n))]]의 일반항이 [[sub(a, n) = 2n]] ([[n >= 1]])임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때 [[sub(a, 1) = 2 = 2 × 1]]\n"
              "(ⅱ) [[n = k]]일 때, [[sub(a, k) = 2k]]라 가정하자.\n"
              "[[sub(a, 1) + sub(a, 2) + sub(a, 3)]] + ⋯ + [[sub(a, k) = frac(k + 1, 2) sub(a, k)]] ⋯ ㉠\n"
              "[[sub(a, 1) + sub(a, 2) + sub(a, 3)]] + ⋯ + [[sub(a, k) + sub(a, k + 1)]] = (가) × [[sub(a, k + 1)]] ⋯ ㉡\n"
              "이므로 ㉠, ㉡에서\n"
              "[[sub(a, k + 1)]] = (나) × [[sub(a, k) = 2(k + 1)]]\n"
              "그러므로 (ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여 [[sub(a, n) = 2n]]이다.\n\n"
              "위의 과정에서 (가)와 (나)에 알맞은 식을 각각 [[f(k)]]와 [[g(k)]]라 할 때, [[f(4) × g(6)]]의 값은?"),
    choices=["[[3]]", "[[frac(7, 2)]]", "[[4]]", "[[frac(9, 2)]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=(k+2)/2, ㉡−㉠: a_(k+1)=((k+1)/k)a_k → (나)=(k+1)/k → 3·7/6=7/2 → ② = 빠른정답 ✓.")

# p59 (id 2개)
dup(["3a5efe65", "2c4a2c9f"], qtype="choice",
    question=("다음은 2 이상인 모든 자연수 [[n]]에 대하여\n"
              "[[pow(n, 3) - 3 pow(n, 2) + 8n - 6]]이 3의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n]] = (가) 일 때,\n"
              "[[pow(2, 3) - 3 × pow(2, 2) + 8 × 2 - 6 = 6]]이므로 3의 배수이다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때, [[pow(n, 3) - 3 pow(n, 2) + 8n - 6]]이 3의 배수라 가정하면\n"
              "[[pow(k, 3) - 3 pow(k, 2) + 8k - 6 = 3N]] ([[N]]은 자연수)\n"
              "[[n = k + 1]]일 때\n"
              "[[pow(k + 1, 3) - 3 pow(k + 1, 2) + 8(k + 1) - 6]]\n"
              "= [[(pow(k, 3) - 3 pow(k, 2) + 8k - 6) + 3]] × ((나))\n"
              "= [[3N + 3]] × ((나))\n"
              "= [[3]]([[N]] + (나))\n"
              "따라서 [[n = k + 1]]일 때도 [[pow(n, 3) - 3 pow(n, 2) + 8n - 6]]이 3의 배수이다.\n"
              "(ⅰ), (ⅱ)에서 2 이상인 모든 자연수 [[n]]에 대하여 [[pow(n, 3) - 3 pow(n, 2) + 8n - 6]]은 3의 배수이다.\n\n"
              "위의 (가)에 알맞은 수를 [[a]], (나)에 알맞은 식을 [[f(k)]]라 할 때, [[a + f(6)]]의 값은?"),
    choices=["[[33]]", "[[34]]", "[[35]]", "[[36]]", "[[37]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=2, 차=3k²−3k+6=3(k²−k+2) → (나)=k²−k+2, f(6)=32 → 34 → ②. 빠른정답 4와 불일치.")

# p60
add(id="4f94f65d", qtype="short",
    question=("다음은 모든 자연수 [[n]]에 대하여 [[frac(pow(n, 3), 6) + frac(pow(n, 2), 2) + frac(n, 3)]]이 자연수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때, [[frac(1, 6) + frac(1, 2) + frac(1, 3) = 1]]이므로 자연수이다.\n"
              "(ⅱ) [[n = k]]일 때, [[frac(pow(n, 3), 6) + frac(pow(n, 2), 2) + frac(n, 3)]]이 자연수라 가정하면\n"
              "[[frac(pow(k, 3), 6) + frac(pow(k, 2), 2) + frac(k, 3)]]가 자연수이므로 [[n = k + 1]]일 때\n"
              "[[frac(pow(k + 1, 3), 6) + frac(pow(k + 1, 2), 2) + frac(k + 1, 3)]]\n"
              "= [[frac(pow(k, 3), 6) + frac(pow(k, 2), 2) + frac(k, 3)]] + ((가))/[[6]] + [[frac(2k + 1, 2) + frac(1, 3)]]\n"
              "= [[frac(pow(k, 3), 6) + frac(pow(k, 2), 2) + frac(k, 3)]] + [[(k + 1)]] × ((나))/[[2]]\n"
              "따라서 [[n = k + 1]]일 때도\n[[frac(pow(n, 3), 6) + frac(pow(n, 2), 2) + frac(n, 3)]]이 자연수이다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여\n[[frac(pow(n, 3), 6) + frac(pow(n, 2), 2) + frac(n, 3)]]이 자연수이다.\n\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(k)]], [[g(k)]]라 할 때,\n[[f(4) - g(9)]]의 값을 구하시오."),
    choices=None, derived_answer="50", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=3k²+3k+1, (나)=k+2 → f(4)−g(9)=61−11=50. 빠른정답 17과 불일치.")

# p62
add(id="ddcacb13", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여 [[pow(6, n) - 5n + 24]]가 25의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때, [[6 - 5 + 24 = 25]]이므로 25의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때, [[pow(6, n) - 5n + 24]]가 25의 배수라 가정하면\n"
              "[[pow(6, k) - 5k + 24]] = (가) ([[N]]은 자연수)\n"
              "[[n = k + 1]]일 때\n"
              "[[pow(6, k + 1) - 5(k + 1) + 24 = pow(6, k + 1) - 5k + 19]]\n"
              "= [[6]] × (가) + [[25]]((나))\n"
              "= [[25]]([[6N]] + (나))\n"
              "따라서 [[n = k + 1]]일 때도 [[pow(6, n) - 5n + 24]]가 25의 배수이다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여\n[[pow(6, n) - 5n + 24]]가 25의 배수이다.\n\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(N)]], [[g(k)]]라 할 때, [[f(2) + g(7)]]의 값은?"),
    choices=["[[48]]", "[[50]]", "[[52]]", "[[54]]", "[[56]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=25N, 6·25N+25k−125 → (나)=k−5 → 50+2=52 → ③. 빠른정답 2와 불일치.")

# p64
add(id="daa9331f", qtype="short",
    question=("다음은 모든 자연수 [[n]]에 대하여 [[pow(4, 2n) - 1]]이 15의 배수임을 수학적 귀납법으로 증명하는 과정이다. "
              "(가), (나)에 알맞은 것을 각각 [[a]], [[f(m)]]이라 할 때, [[f(a)]]의 값을 구하시오.\n\n"
              "(ⅰ) [[n = 1]]일 때, [[pow(4, 2) - 1 = 15]]이므로 15의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때, [[pow(4, 2k) - 1 = 15m]] ([[m]]은 자연수)라고 가정하면\n"
              "[[pow(4, 2(k + 1)) - 1]] = (가) × [[pow(4, 2k)]] − 1\n"
              "= [[15]] × ((나))\n"
              "따라서 [[n = k + 1]]일 때도 15의 배수이다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여 [[pow(4, 2n) - 1]]은 15의 배수이다."),
    choices=None, derived_answer="257", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=16, 16(15m+1)−1=15(16m+1) → (나)=16m+1 → f(16)=257. 빠른정답 5와 불일치.")

# p66
add(id="4ad4bd3f", qtype="short",
    question=("다음은 모든 자연수 [[n]]에 대하여 [[pow(5, 2n) - 1]]이 24의 배수임을 수학적 귀납법으로 증명하는 과정이다. "
              "(가), (나)에 알맞은 것을 각각 [[a]], [[f(m)]]이라고 할 때, [[f(a)]]의 값을 구하시오.\n\n"
              "(ⅰ) [[n = 1]]일 때, [[pow(5, 2) - 1 = 24]]이므로 24의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때, [[pow(5, 2k) - 1 = 24m]] ([[m]]은 자연수)라고 가정하면\n"
              "[[pow(5, 2(k + 1)) - 1]] = (가) × [[pow(5, 2k)]] − 1\n"
              "= [[24]] × ((나))\n"
              "따라서 [[n = k + 1]]일 때도 24의 배수이다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여\n[[pow(5, 2n) - 1]]은 24의 배수이다."),
    choices=None, derived_answer="626", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=25, 25(24m+1)−1=24(25m+1) → (나)=25m+1 → f(25)=626. 빠른정답 3과 불일치.")

# p68
add(id="3185db4b", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여 [[pow(n, 3) + 3 pow(n, 2) + 2n]]이 3의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n<증명>\n"
              "(ⅰ) [[n = 1]]일 때,\n[[pow(1, 3) + 3 × pow(1, 2) + 2 × 1 = 6]]\n이므로 3의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때 [[pow(n, 3) + 3 pow(n, 2) + 2n]]이 3의 배수라 가정하면\n"
              "[[pow(k, 3) + 3 pow(k, 2) + 2k = 3N]] ([[N]]은 자연수)으로 놓을 수 있다.\n"
              "이때 [[n = k + 1]]이면\n"
              "[[pow(k + 1, 3) + 3 pow(k + 1, 2) + 2(k + 1)]]\n"
              "= [[pow(k, 3) + 6 pow(k, 2)]] + (가)\n"
              "= (나) + [[6 + 3k(k + 3)]]\n"
              "= [[3(N + 2) + 3k(k + 3)]]\n"
              "이고, [[3k(k + 3)]]이 (다) 의 배수이므로\n"
              "[[n = k + 1]]일 때도 [[pow(n, 3) + 3 pow(n, 2) + 2n]]이 3의 배수이다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여\n[[pow(n, 3) + 3 pow(n, 2) + 2n]]은 3의 배수이다.\n\n"
              "위의 과정에서 (가), (나)에 알맞은 식을 각각 [[f(k)]], [[g(k)]]라 하고, (다)에 알맞은 수를 [[a]]라 할 때, "
              "[[frac(g(a), f(a)) = frac(q, p)]]이다.\n이때 서로소인 두 자연수 [[p]], [[q]]에 대하여 [[p + q]]의 값은?"),
    choices=["[[25]]", "[[27]]", "[[29]]", "[[31]]", "[[33]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=11k+6, (나)=k³+3k²+2k, (다)=3 → g(3)/f(3)=60/39=20/13 → 33 → ⑤ = 빠른정답 ✓.")

# p70
add(id="f46bf2cd", qtype="short",
    question=("다음은 모든 자연수 [[n]]에 대하여 [[n(pow(n, 2) + 2)]]가 3의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때,\n[[1 × (pow(1, 2) + 2) = 3]]이므로 3의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때,\n[[n(pow(n, 2) + 2)]]가 3의 배수라 가정하면\n"
              "[[k(pow(k, 2) + 2) = 3N]] ([[N]]은 자연수)로 놓을 수 있다.\n"
              "이때 [[n = k + 1]]이면\n"
              "[[(k + 1)(pow(k + 1, 2) + 2)]]\n"
              "= (가) + [[5k + 3]]\n"
              "= [[k(pow(k, 2) + 2) + 3]] + (나)\n"
              "= (다) [[(N + 1) + 3k(k + 1)]]\n"
              "이므로 [[n = k + 1]]일 때도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여\n[[n(pow(n, 2) + 2)]]는 3의 배수이다.\n\n"
              "위의 증명 과정에서 (가), (나)에 알맞은 식을 각각 [[f(k)]], [[g(k)]]라 하고, (다)에 알맞은 수를 [[a]]라 할 때, "
              "[[frac(g(a), f(1))]]의 값을 구하시오."),
    choices=None, derived_answer="9", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=k³+3k², (나)=3k²+3k, (다)=3 → g(3)/f(1)=36/4=9. 빠른정답 4와 불일치.")

# p72
add(id="ea8d6892", qtype="choice",
    question=("수열 [[set(sub(a, n))]]이 [[sub(a, 1) = 1]], [[sub(a, 2) = 1]],\n"
              "[[sub(a, n + 2) = sub(a, n + 1) + sub(a, n)]] ([[n]] = 1, 2, 3, ⋯)으로 정의될 때,\n"
              "다음은 모든 자연수 [[n]]에 대하여 [[sub(a, 4n)]]은 3의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때, [[sub(a, 4)]] = (가) 이므로 3의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때, [[sub(a, 4k)]]가 3의 배수라고 가정하면\n"
              "[[sub(a, 4(k + 1))]] = (나) [[sub(a, 4k + 1)]] + (다) [[sub(a, 4k)]]\n"
              "즉, [[n = k + 1]]일 때에도 [[sub(a, 4n)]]은 3의 배수이다.\n"
              "(ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여 [[sub(a, 4n)]]은 3의 배수이다.\n\n"
              "위 증명에서 (가), (나), (다)에 알맞은 수들의 곱은?"),
    choices=["[[16]]", "[[18]]", "[[20]]", "[[22]]", "[[24]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="a₄=3, a_(4k+4)=3a_(4k+1)+2a_(4k) → 3·3·2=18 → ② = 빠른정답 ✓.")

# p74
add(id="a2d6a9d2", qtype="choice",
    question=("다음은 [[n >= 2]]인 모든 자연수 [[n]]에 대하여 [[pow(4, n) - 3n - 1]]이 9의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 2]]일 때,\n[[pow(4, 2) - 3 × 2 - 1 = 9]]이므로 9의 배수이다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때,\n[[pow(4, n) - 3n - 1]]이 9의 배수라 가정하면\n"
              "자연수 [[N]]에 대하여 [[pow(4, k) - 3k - 1 = 9N]]으로 놓을 수 있다.\n"
              "이때 [[n = k + 1]]이면\n"
              "[[pow(4, k + 1) - 3(k + 1) - 1]]\n"
              "= (가) [[-3k - 4]]\n"
              "= [[4(pow(4, k) - 3k - 1)]] + (나)\n"
              "= [[4 × 9N]] + (나)\n"
              "= [[9]]((다))\n"
              "따라서 [[n = k + 1]]일 때에도 [[pow(4, n) - 3n - 1]]은 9의 배수이다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여\n[[pow(4, n) - 3n - 1]]은 9의 배수이다.\n\n"
              "위의 증명 과정에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[pow(4, k)]], (나) [[3k]], (다) [[4N]]",
             "(가) [[pow(4, k)]], (나) [[9k]], (다) [[4N + k]]",
             "(가) [[4 × pow(4, k)]], (나) [[3k]], (다) [[4N + k]]",
             "(가) [[4 × pow(4, k)]], (나) [[9k]], (다) [[4N]]",
             "(가) [[4 × pow(4, k)]], (나) [[9k]], (다) [[4N + k]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=4·4^k, 4(4^k−3k−1)+9k → (나)=9k, (다)=4N+k → ⑤. 빠른정답 2와 불일치.")

# p75
add(id="7f7f5d6c", qtype="choice",
    question=("수열 [[set(sub(a, n))]]이\n"
              "[[sub(a, 1) = 1]], [[sub(a, 2) = 2]], [[sub(a, n + 2) = 2 sub(a, n + 1) + sub(a, n)]] ([[n]] = 1, 2, 3, ⋯)\n"
              "으로 정의될 때, 다음은 모든 자연수 [[n]]에 대하여 [[sub(a, 4n)]]은 12의 배수임을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때, [[sub(a, 4)]] = (가) 이므로 12의 배수이다.\n"
              "(ⅱ) [[n = k]]일 때, [[sub(a, 4k)]]가 12의 배수라고 가정하면\n"
              "[[sub(a, 4(k + 1))]] = (나) [[sub(a, 4k + 1)]] + (다) [[sub(a, 4k)]]\n"
              "즉, [[n = k + 1]]일 때에도 [[sub(a, 4n)]]은 12의 배수이다.\n"
              "따라서 (ⅰ), (ⅱ)에 의해 모든 자연수 [[n]]에 대하여 [[sub(a, 4n)]]은 12의 배수이다.\n\n"
              "위 증명에서 (가), (나), (다)에 알맞은 수들의 합은?"),
    choices=["[[26]]", "[[27]]", "[[28]]", "[[29]]", "[[30]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a₃=5, a₄=12; a_(4k+4)=12a_(4k+1)+5a_(4k) → 12+12+5=29 → ④. 빠른정답 2와 불일치.")

# p76 — 부등식의 증명
add(id="6903d27e", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여 부등식\n"
              "[[pow(fact(n), 2) × pow(4, n) > fact(2n)]] ⋯ ㉠\n"
              "이 성립함을 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때, (좌변)=[[4]], (우변)= (가)\n이므로 ㉠이 성립한다.\n"
              "(ⅱ) [[n = k]]일 때, ㉠이 성립한다고 가정하면\n"
              "[[pow(fact(k), 2) × pow(4, k) > fact(2k)]] ⋯ ㉡\n"
              "[[n = k + 1]]일 때 ㉠이 성립함을 보이자.\n"
              "㉡의 양변에 (나) 를 곱하면\n"
              "[[pow(fact(k + 1), 2) × pow(4, k + 1)]] > ((나)) × [[fact(2k)]]\n"
              "> [[(2k + 2)]]((다)) × [[fact(2k)]]\n"
              "= [[fact(2k + 2)]]\n"
              "따라서 [[n = k + 1]]일 때에도 ㉠은 성립한다.\n"
              "그러므로 (ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여 ㉠이 성립한다.\n\n"
              "위의 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[1]], (나) [[4 pow(k + 1, 2)]], (다) [[2k]]",
             "(가) [[1]], (나) [[2 pow(k + 1, 2)]], (다) [[2k]]",
             "(가) [[2]], (나) [[4 pow(k + 1, 2)]], (다) [[2k + 1]]",
             "(가) [[2]], (나) [[2 pow(k + 1, 2)]], (다) [[2k + 1]]",
             "(가) [[2]], (나) [[4 pow(k + 1, 2)]], (다) [[2k]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2010년 10월 고3 이과 13번]. (가)=2!=2, (나)=4(k+1)², 4(k+1)²=(2k+2)·2(k+1)>(2k+2)(2k+1) → (다)=2k+1 → ③. 빠른정답 4와 불일치.")

# p77
add(id="b3382571", qtype="short",
    question=("다음은 [[n >= 2]]인 모든 자연수 [[n]]에 대하여 부등식\n"
              "[[1 + frac(1, 2) + frac(1, 3)]] + ⋯ + [[frac(1, n) > frac(2n, n + 1)]]이 성립함을 수학적 귀납법으로 증명하는 과정이다.\n\n"
              "(ⅰ) [[n = 2]]일 때\n(좌변)=[[1 + frac(1, 2) = frac(3, 2)]]\n(우변)=[[frac(2 × 2, 2 + 1) = frac(4, 3)]]\n"
              "따라서 주어진 부등식이 성립한다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때\n주어진 부등식이 성립한다고 가정하면\n"
              "[[1 + frac(1, 2) + frac(1, 3)]] + ⋯ + [[frac(1, k) > frac(2k, k + 1)]] ⋯ ㉠\n"
              "㉠이 성립한다.\n"
              "이때 부등식 ㉠의 양변에 [[frac(1, k + 1)]]을 더하면\n"
              "[[1 + frac(1, 2) + frac(1, 3)]] + ⋯ + [[frac(1, k) + frac(1, k + 1)]] > (가) ⋯ ㉡\n"
              "이때 [[k >= 2]]이므로\n"
              "(가) − [[frac(2(k + 1), k + 2)]] = (나) > 0\n"
              "∴ (가) > [[frac(2(k + 1), k + 2)]] ⋯ ㉢\n"
              "㉡, ㉢에서\n"
              "[[1 + frac(1, 2) + frac(1, 3)]] + ⋯ + [[frac(1, k) + frac(1, k + 1) > frac(2(k + 1), k + 2)]]\n"
              "따라서 [[n = k + 1]]일 때도 주어진 부등식은 성립한다.\n"
              "(ⅰ), (ⅱ)에 의해 주어진 부등식은 [[n >= 2]]인 모든 자연수 [[n]]에 대하여 성립한다.\n\n"
              "위 증명에서 (가), (나)에 알맞은 식을 각각 [[f(k)]], [[g(k)]]라 할 때, [[f(5) + g(1)]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=(2k+1)/(k+1), (나)=k/((k+1)(k+2)) → 11/6+1/6=2. 빠른정답 5와 불일치.")

# p79
add(id="5b8bddbc", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[1 + frac(1, sqrt(2)) + frac(1, sqrt(3))]] + ⋯ + [[frac(1, sqrt(n)) >= 2 - frac(1, sqrt(n))]] ⋯ ㉠\n"
              "이 성립함을 수학적 귀납법으로 증명한 것의 일부이다.\n\n"
              "(ⅰ) [[n = 1]]일 때, (좌변)=[[1]], (우변)=[[2 - 1 = 1]]\n따라서 부등식 ㉠이 성립한다.\n"
              "(ⅱ) [[n = k]]일 때, ㉠이 성립한다고 가정하면\n"
              "[[1 + frac(1, sqrt(2)) + frac(1, sqrt(3))]] + ⋯ + [[frac(1, sqrt(k)) >= 2 - frac(1, sqrt(k))]] ⋯ ㉡\n"
              "㉡의 양변에 [[frac(1, sqrt(k + 1))]]을 더하면\n"
              "[[1 + frac(1, sqrt(2)) + frac(1, sqrt(3))]] + ⋯ + [[frac(1, sqrt(k)) + frac(1, sqrt(k + 1))]]\n"
              "≥ [[2 - frac(1, sqrt(k)) + frac(1, sqrt(k + 1))]]\n"
              "그런데 모든 자연수 [[k]]에 대하여\n"
              "[[4k]] (가) [[k + 1]]이므로\n"
              "[[2 sqrt(k) - sqrt(k + 1)]] (가) [[0]]이다.\n"
              "∴ [[(2 - frac(1, sqrt(k)) + frac(1, sqrt(k + 1)))]] − ((나))\n"
              "= [[frac(2, sqrt(k + 1)) - frac(1, sqrt(k))]]\n"
              "= [[frac(2 sqrt(k) - sqrt(k + 1), sqrt(pow(k, 2) + k)) >= 0]]\n"
              "즉, [[2 - frac(1, sqrt(k)) + frac(1, sqrt(k + 1))]] ≥ (나) 이 성립하므로\n"
              "[[1 + frac(1, sqrt(2)) + frac(1, sqrt(3))]] + ⋯ + [[frac(1, sqrt(k + 1))]] ≥ (나)\n"
              "따라서 [[n = k + 1]]일 때도 ㉠이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의해 ㉠은 모든 자연수 [[n]]에 대하여 성립한다.\n\n"
              "위의 증명에서 (가), (나)에 알맞은 것을 차례대로 적은 것은?"),
    choices=["≥, [[1 - frac(1, sqrt(k + 1))]]", "≤, [[1 - frac(1, sqrt(k + 1))]]", "≥, [[2 - frac(1, sqrt(k + 1))]]",
             "≤, [[2 - frac(1, sqrt(k + 1))]]", "≥, [[2 + frac(1, sqrt(k + 1))]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="4k≥k+1 → (가)=≥, (나)=2−1/√(k+1) → ③ = 빠른정답 ✓. 부등호 빈칸·선지의 부등호는 텍스트.")

# p81 — 이미지 하단 잘림(선지 ④⑤ 안 보임)
add(id="655842bf", qtype="choice",
    question=("다음은 2 이상의 모든 자연수 [[n]]에 대하여\n"
              "[[1 + frac(1, pow(2, 2)) + frac(1, pow(3, 2))]] + ⋯ + [[frac(1, pow(n, 2)) < 2 - frac(1, n)]]임을\n"
              "수학적 귀납법으로 증명한 것이다.\n\n<증명>\n"
              "(ⅰ) [[n]] = (가) 일 때,\n"
              "(좌변)=[[1 + frac(1, pow(2, 2)) = frac(5, 4) < 2 - frac(1, 2) = frac(3, 2)]]=(우변)\n"
              "따라서, [[n]] = (가) 일 때, 주어진 식은 성립한다.\n"
              "(ⅱ) [[n = k]] ([[n >= 2]])일 때, 주어진 식이 성립한다고 가정하면\n"
              "[[1 + frac(1, pow(2, 2)) + frac(1, pow(3, 2))]] + ⋯ + [[frac(1, pow(k, 2)) < 2 - frac(1, k)]]이다.\n"
              "위 식의 양변에 [[frac(1, pow(k + 1, 2))]]을 더하면\n"
              "[[1 + frac(1, pow(2, 2)) + frac(1, pow(3, 2))]] + ⋯ + [[frac(1, pow(k, 2)) + frac(1, pow(k + 1, 2))]]\n"
              "< [[2 - frac(1, k) + frac(1, pow(k + 1, 2))]]\n"
              "그런데\n"
              "{[[-frac(1, k) + frac(1, pow(k + 1, 2))]]} − (나)\n"
              "= [[-frac(1, k pow(k + 1, 2)) < 0]] 이므로\n"
              "[[2 - frac(1, k) + frac(1, pow(k + 1, 2)) < 2 - frac(1, k + 1)]]이다.\n"
              "따라서, [[n = k + 1]]일 때에도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 [[n >= 2]]인 모든 자연수 [[n]]에 대하여\n"
              "[[1 + frac(1, pow(2, 2)) + frac(1, pow(3, 2))]] + ⋯ + [[frac(1, pow(n, 2)) < 2 - frac(1, n)]]이 성립한다.\n\n"
              "이 증명 과정에서 (가), (나)에 알맞은 내용을 바르게 짝지은 것은?"),
    choices=["(가) [[1]], (나) [[frac(1, k + 1)]]", "(가) [[1]], (나) [[-frac(1, k + 1)]]", "(가) [[2]], (나) [[-frac(1, k + 1)]]",
             "(이미지 하단 잘림)", "(이미지 하단 잘림)"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.75,
    needs_review="이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움)",
    note="출처 [2004년 11월 고2 이과 13번]. (가)=2, (나)=−1/(k+1) → ③ = 빠른정답 ✓ (보이는 선지 기준).")

# p82
add(id="bc426cdb", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[sub(a, n) = sqrt(1 × 2) + sqrt(2 × 3)]] + ⋯ + [[sqrt(n(n + 1))]]\n"
              "일 때, 부등식 [[frac(n(n + 1), 2) < sub(a, n) < frac(pow(n + 1, 2), 2)]]이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n[증명]\n"
              "(ⅰ) [[n = 1]]일 때,\n[[1 < sub(a, 1) = sqrt(2) < 2]]이므로 성립한다.\n"
              "(ⅱ) [[n = k]]일 때,\n[[frac(k(k + 1), 2) < sub(a, k) < frac(pow(k + 1, 2), 2)]]이 성립한다고 가정하면\n"
              "[[frac(k(k + 1), 2) + sqrt((k + 1)(k + 2)) < sub(a, k + 1) < frac(pow(k + 1, 2), 2) + sqrt((k + 1)(k + 2))]]\n"
              "이다.\n"
              "한편, [[sqrt((k + 1)(k + 2))]] > (가) 이므로\n"
              "[[frac(k(k + 1), 2) + sqrt((k + 1)(k + 2))]] > (나)\n"
              "이다.\n"
              "[[k + 1 > 0]], [[k + 2 > 0]]이므로\n"
              "[[sqrt((k + 1)(k + 2))]] < (다) 이고,\n"
              "[[frac(pow(k + 1, 2), 2) + sqrt((k + 1)(k + 2)) < frac(pow(k + 2, 2), 2)]]\n"
              "이다.\n"
              "그러므로 [[n = k + 1]]일 때에도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여 주어진 부등식은 성립한다.\n\n"
              "(가) ~ (다)에 알맞은 것을 바르게 짝지은 것은?"),
    choices=["(가) [[k + 1]], (나) [[frac((k + 1)(k + 2), 2)]], (다) [[frac(2k + 1, 2)]]",
             "(가) [[k + 1]], (나) [[frac((k + 1)(k + 2), 2)]], (다) [[frac(2k + 3, 2)]]",
             "(가) [[k + 1]], (나) [[frac((k + 2)(k + 3), 2)]], (다) [[frac(2k + 1, 2)]]",
             "(가) [[k + 2]], (나) [[frac((k + 1)(k + 2), 2)]], (다) [[frac(2k + 1, 2)]]",
             "(가) [[k + 2]], (나) [[frac((k + 2)(k + 3), 2)]], (다) [[frac(2k + 3, 2)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2008년 11월 고2 이과 18번]. (가)=k+1, (나)=(k+1)(k+2)/2, (다)=(2k+3)/2 (산술·기하평균) → ②. 빠른정답 3과 불일치.")

# p83
add(id="38e7eb10", qtype="choice",
    question=("다음은 [[h > 0]]일 때, [[n >= 2]]인 자연수 [[n]]에 대하여 부등식 [[pow(2 + h, n) > 2 + 2n h]]가 성립함을 증명한 것이다.\n\n"
              "(ⅰ) [[n = 2]]일 때,\n(좌변)=[[pow(2 + h, 2) = 4 + 4h + pow(h, 2)]]\n(우변)= (가)\n"
              "이때 [[h > 0]]이므로 [[4 + 4h + pow(h, 2)]] > (가)\n따라서 주어진 부등식이 성립한다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때 주어진 부등식이 성립한다고 가정하면\n"
              "[[pow(2 + h, k)]] > (나)\n"
              "위 식의 양변에 [[2 + h]]를 곱하면\n"
              "[[pow(2 + h, k + 1)]]\n"
              "> ((나))[[(2 + h)]]\n"
              "= [[2 + 2(k + 1) h + (2 + 2k h + 2k pow(h, 2))]]\n"
              "> [[2 + 2(k + 1) h]]\n"
              "따라서 [[n = k + 1]]일 때에도 주어진 부등식이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 [[n >= 2]]인 자연수 [[n]]에 대하여 주어진 부등식이 성립한다.\n\n"
              "위의 증명에서 (가), (나)에 알맞은 것을 차례로 적은 것은?"),
    choices=["(가) [[2 + 2h]], (나) [[2 + k h]]", "(가) [[2 + 2h]], (나) [[2 + 2k h]]", "(가) [[2 + 4h]], (나) [[2 + k h]]",
             "(가) [[2 + 4h]], (나) [[2 + 2k h]]", "(가) [[h + 2 pow(h, 2)]], (나) [[2k h + pow(h, 2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=2+4h, (나)=2+2kh → ④. 빠른정답 5와 불일치.")

# p84
add(id="d3e1c8b5", qtype="choice",
    question=("다음은 [[n >= 2]]인 모든 자연수 [[n]]에 대하여\n"
              "[[(1 + frac(1, pow(1, 3)))(1 + frac(1, pow(2, 3)))(1 + frac(1, pow(3, 3)))]] ⋯ [[(1 + frac(1, pow(n, 3))) < 3 - frac(1, n)]] ⋯ ㉠\n"
              "이 성립함을 수학적귀납법으로 증명하는 과정이다.\n\n<증명>\n"
              "(ⅰ) [[n = 2]]일 때\n"
              "(좌변)=[[(1 + frac(1, pow(1, 3)))(1 + frac(1, pow(2, 3))) = frac(9, 4)]],\n"
              "(우변)=[[3 - frac(1, 2) = frac(5, 2)]]이므로 ㉠이 성립한다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때 ㉠이 성립한다고 가정하면\n"
              "[[(1 + frac(1, pow(1, 3)))(1 + frac(1, pow(2, 3)))(1 + frac(1, pow(3, 3)))]] ⋯ [[(1 + frac(1, pow(k, 3)))]]\n"
              "< [[3 - frac(1, k)]] ⋯ ㉡\n"
              "㉡의 양변에 (가) 를 곱하면\n"
              "[[(1 + frac(1, pow(1, 3)))(1 + frac(1, pow(2, 3)))(1 + frac(1, pow(3, 3)))]] ⋯ [[(1 + frac(1, pow(k, 3)))]]((가))\n"
              "< [[(3 - frac(1, k))]]((가)) ⋯ ㉢\n"
              "㉢의 우변을 정리하면\n"
              "(우변)= [[3]] − ((나))/[[k pow(k + 1, 3)]]\n"
              "이 때, ((나))/[[k pow(k + 1, 3)]] − [[frac(1, k + 1)]] (다) [[0]]\n"
              "따라서 [[n = k + 1]]일 때도 ㉠이 성립한다.\n"
              "그러므로 (ⅰ), (ⅱ)에 의하여 [[n >= 2]]인 모든 자연수 [[n]]에 대하여 주어진 부등식은 성립한다.\n\n"
              "위의 증명 과정에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[1 + frac(1, pow(k + 1, 3))]], (나) [[pow(k, 3) + 3 pow(k, 2) + 2]], (다) <",
             "(가) [[1 + frac(1, pow(k + 1, 3))]], (나) [[pow(k, 3) + 3 pow(k, 2) + 2]], (다) >",
             "(가) [[1 + frac(1, pow(k + 1, 3))]], (나) [[pow(k, 3) - 3 pow(k, 2) + 2]], (다) <",
             "(가) [[frac(1, pow(k + 1, 3))]], (나) [[pow(k, 3) - 3 pow(k, 2) + 2]], (다) >",
             "(가) [[frac(1, pow(k + 1, 3))]], (나) [[pow(k, 3) - 3 pow(k, 2) + 2]], (다) <"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2008년 7월 고3 이과 14번]. (가)=1+1/(k+1)³, (3−1/k)(가)=3−(k³+3k²+2)/(k(k+1)³), 차=(k²−k+2)/(k(k+1)³)>0 → ②. 빠른정답 3과 불일치. 부등호 빈칸은 텍스트.")

# p85
add(id="ee0929a6", qtype="choice",
    question=("다음은 [[n >= 2]]인 모든 자연수 [[n]]에 대하여 부등식\n"
              "[[pow(2, n + 1) > n(n + 1) + 1]]이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n<증명>\n"
              "(ⅰ) [[n = 2]]일 때,\n(좌변)=[[pow(2, 3) = 8]], (우변)=[[2 × 3 + 1 = 7]]\n따라서 주어진 부등식이 성립한다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때 주어진 부등식이 성립한다고 가정하면\n"
              "[[pow(2, k + 1)]] > (가) + 1\n"
              "위의 식의 양변에 2를 곱하면\n"
              "[[pow(2, k + 2) > 2(pow(k, 2) + k + 1)]]\n"
              "그런데 [[k >= 2]]이면\n"
              "[[pow(k, 2) - k - 1 = 2(pow(k, 2) + k + 1)]] − {(나)} > 0\n"
              "이므로 [[2(pow(k, 2) + k + 1)]] > (나)\n"
              "∴ [[pow(2, k + 2)]] > (나)\n"
              "따라서 [[n = k + 1]]일 때도 주어진 부등식이 성립한다.\n"
              "(ⅰ), (ⅱ)에서 [[n >= 2]]인 모든 자연수 [[n]]에 대하여 주어진 부등식이 성립한다.\n\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 차례대로 나열한 것은?"),
    choices=["[[k(k + 1)]], [[(k + 1)(k + 2) - 1]]", "[[k(k + 1)]], [[(k + 1)(k + 2) + 1]]", "[[k(k + 2)]], [[(k + 1)(k + 2) - 1]]",
             "[[k(k + 2)]], [[(k + 1)(k + 2) + 1]]", "[[k(k + 2)]], [[(k + 2)(k + 3) - 1]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=k(k+1), 2(k²+k+1)−{(k+1)(k+2)+1}=k²−k−1 → (나)=(k+1)(k+2)+1 → ② = 빠른정답 ✓.")

# p88
add(id="2f8fe85a", qtype="choice",
    question=("2 이상의 자연수 [[n]]에 대하여\n부등식 [[pow(1 + frac(1, n), n) > 2]]가 성립함이 알려져 있다.\n"
              "다음은 이 사실을 이용하여 [[n]]이 6 이상의 자연수일 때,\n"
              "부등식 [[pow(frac(n, 2), n) > fact(n)]]이 성립함을 수학적귀납법으로 증명한 것이다. (단, [[n != 1 × 2 × 3]] × ⋯ × [[n]])\n\n"
              "(ⅰ) [[n = 6]]일 때, [[pow(3, 6) = 729]], [[fact(6) = 720]]이므로 성립한다.\n"
              "(ⅱ) [[n = k]] ([[k >= 6]])일 때 성립한다고 가정하면\n"
              "[[pow(frac(k + 1, 2), k + 1) = frac(k + 1, pow(2, k + 1)) × frac(pow(k + 1, k), pow(k, k))]] × □\n"
              "= [[frac(k + 1, 2) × pow(1 + frac(1, k), k)]] × (가)\n"
              "> [[frac(k + 1, 2)]] × (나)\n"
              "= □\n"
              "이므로 [[n = k + 1]]일 때도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 주어진 부등식은 6 이상의 모든 자연수에 대하여 성립한다.\n\n"
              "위의 증명에서 (가), (나)에 알맞은 것은?"),
    choices=["(가) [[pow(k, k)]], (나) [[fact(k + 1)]]", "(가) [[pow(k, k)]], (나) [[2 fact(k)]]", "(가) [[pow(k, k)]], (나) [[fact(k)]]",
             "(가) [[pow(frac(k, 2), k)]], (나) [[fact(k + 1)]]", "(가) [[pow(frac(k, 2), k)]], (나) [[2 fact(k)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2005년 7월 고3 이과 12번]. (가)=(k/2)^k, (1+1/k)^k>2·(k/2)^k>k! → (나)=2k! → ⑤. 빠른정답 2와 불일치. 원문 조건 'n≠1×2×3×⋯×n'은 n! 오식으로 보이나 그대로 전사, 빈 상자 □는 텍스트.")

# p90
add(id="aae6afeb", qtype="choice",
    question=("다음은 [[n >= 2]]인 모든 자연수 [[n]]에 대하여\n"
              "[[1 + frac(1, 2) + frac(1, 3)]] + ⋯ + [[frac(1, n) > frac(2n, n + 1)]] ⋯ ㉠\n"
              "이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 2]]일 때\n(좌변)=[[1 + frac(1, 2) = frac(3, 2)]],\n(우변)=[[frac(4, 3)]]\n이므로 ㉠이 성립한다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때 ㉠이 성립한다고 가정하면\n"
              "[[1 + frac(1, 2) + frac(1, 3)]] + ⋯ + [[frac(1, k) > frac(2k, k + 1)]] ⋯ ㉡\n"
              "㉡의 양변에 (가) 를 더하면\n"
              "[[1 + frac(1, 2) + frac(1, 3)]] + ⋯ + [[frac(1, k)]] + (가)\n"
              "> [[frac(2k, k + 1)]] + (가) ⋯ ㉢\n"
              "㉢의 우변을 정리하면\n"
              "(우변)= ((나))/[[k + 1]]\n"
              "이때 ((나))/[[k + 1]] − [[frac(2(k + 1), k + 2)]] (다) [[0]]\n"
              "따라서 [[n = k + 1]]일 때도 ㉠이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 [[n >= 2]]인 모든 자연수 [[n]]에 대하여 주어진 부등식은 성립한다.\n\n"
              "위의 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[frac(1, k)]], (나) [[2k + 1]], (다) <", "(가) [[frac(1, k)]], (나) [[2k - 1]], (다) >",
             "(가) [[frac(1, k + 1)]], (나) [[2k + 1]], (다) >", "(가) [[frac(1, k + 1)]], (나) [[2k + 1]], (다) <",
             "(가) [[frac(1, k + 1)]], (나) [[2k - 1]], (다) >"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="(가)=1/(k+1), (나)=2k+1, (2k+1)/(k+1)−2(k+1)/(k+2)=k/((k+1)(k+2))>0 → (다)=> → ③. 빠른정답 2와 불일치. 부등호 빈칸은 텍스트.")

# p91
add(id="00ab4140", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "부등식 [[frac(1, n + 1) + frac(1, n + 2)]] + ⋯ + [[frac(1, 3n + 1) > 1]]이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n"
              "[[sub(a, n) = frac(1, n + 1) + frac(1, n + 2)]] + ⋯ + [[frac(1, 3n + 1)]]이라 할 때,\n"
              "모든 자연수 [[n]]에 대하여 [[sub(a, n) > 1]]임을 보이면 된다.\n"
              "(ⅰ) [[n = 1]]일 때,\n"
              "[[sub(a, 1) = frac(1, 2)]] + (가) + [[frac(1, 4) > 1]]\n"
              "따라서 주어진 부등식이 성립한다.\n"
              "(ⅱ) [[n = k]]일 때, 주어진 부등식이 성립한다고 가정하면\n"
              "[[sub(a, k) = frac(1, k + 1) + frac(1, k + 2)]] + ⋯ + [[frac(1, 3k + 1) > 1]]\n"
              "[[n = k + 1]]일 때,\n"
              "[[sub(a, k + 1)]]\n"
              "= [[frac(1, k + 2) + frac(1, k + 3)]] + ⋯ + [[frac(1, 3k + 4)]]\n"
              "= [[sub(a, k)]] + (나) − [[frac(1, k + 1)]]\n"
              "한편, [[(3k + 2)(3k + 4) < pow(3k + 3, 2)]]이므로\n"
              "[[frac(1, 3k + 2) + frac(1, 3k + 4) > frac(2, 3k + 3)]]에서\n"
              "[[sub(a, k + 1) > sub(a, k)]] + ([[frac(1, 3k + 3)]] + (다)) − [[frac(1, k + 1)]]\n"
              "> 1\n"
              "따라서 [[n = k + 1]]일 때도 주어진 부등식이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여 주어진 부등식은 성립한다.\n\n"
              "위의 증명에서 (가)에 알맞은 수를 [[a]]라 하고, (나), (다)에 알맞은 식을 각각 [[f(k)]], [[g(k)]]라 할 때, "
              "[[frac(g(a), f(a))]]의 값은?"),
    choices=["[[frac(28, 47)]]", "[[frac(30, 47)]]", "[[frac(32, 47)]]", "[[frac(34, 47)]]", "[[frac(36, 47)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="(가)=1/3, (나)=1/(3k+2)+1/(3k+3)+1/(3k+4), (다)=2/(3k+3) → f(1/3)=47/60, g(1/3)=1/2 → 30/47 → ② = 빠른정답 ✓.")

# p92
add(id="89987741", qtype="short",
    question=("다음은 [[n >= 3]]인 모든 자연수 [[n]]에 대하여 부등식\n"
              "[[1 × 2 × 3]] × ⋯ × [[n > pow(2, n - 1)]]\n"
              "이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 3]]일 때\n(좌변)=[[1 × 2 × 3 = 6]],\n(우변)=[[pow(2, 3 - 1) = 4]]\n따라서 주어진 부등식이 성립한다.\n"
              "(ⅱ) [[n = k]] ([[k >= 3]])일 때, 주어진 부등식이 성립한다고 가정하면\n"
              "[[1 × 2 × 3]] × ⋯ × [[k > pow(2, k - 1)]]\n"
              "위의 부등식의 양변에 (가) 을(를) 곱하면\n"
              "[[1 × 2 × 3]] × ⋯ × [[k]] × ((가))\n"
              "> [[pow(2, k - 1)]] × ((가))\n"
              "이때 [[k >= 3]]이므로 위의 식의 우변에서\n"
              "[[pow(2, k - 1)]] × ((가)) > (나)\n"
              "∴ [[1 × 2 × 3]] × ⋯ × [[k]] × ((가)) > (나)\n"
              "따라서 [[n = k + 1]]일 때에도 주어진 부등식이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 [[n >= 3]]인 자연수 [[n]]에 대하여 주어진 부등식이 성립한다.\n\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(k)]], [[g(k)]]라 할 때,\n[[frac(g(8), f(31))]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)=k+1, (나)=2^k → g(8)/f(31)=256/32=8. 빠른정답 5와 불일치.")
