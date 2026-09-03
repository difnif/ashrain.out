# -*- coding: utf-8 -*-
# esc_sonnet_h3-1_2of2 — 이미지 기준 전사 (57 항목 / 56쪽; 모평균의 추정 p73에 id 2개)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_G1 = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_G2 = ["ㄱ", "ㄷ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_G3 = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
XBAR_REVIEW = "문법 한계: 표본평균 X̄(윗줄) 기호가 mathir에 없어 conj(X)로 표기"

# ───────────────────────── 이항정리 ─────────────────────────
# p52
add(id="3de87a3f", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여 부등식 [[pow(2,n) <= comb(2n,n) < pow(4,n)]]이 성립함을 증명하는 과정이다.\n"
              "[[comb(2n,n) < comb(2n,0) + comb(2n,1) + comb(2n,2)]] + ⋯ + [[comb(2n,2n)]]이므로\n"
              "(가) < [[pow(4,n)]] ⋯ ㉠\n"
              "또, [[1 <= k <= n]]을 만족시키는 자연수 [[k]]에 대하여\n"
              "[[frac(n + k, k) >= frac(k + k, k) = 2]]이므로\n"
              "[[comb(2n,n) = 2 × frac(n + (n - 1), n - 1)]] × ⋯ × [[frac(n + 1, 1)]]\n"
              "≥ (나) ⋯ ㉡\n"
              "따라서 ㉠, ㉡에 의하여 모든 자연수 [[n]]에 대하여 주어진 부등식이 성립한다.\n"
              "위의 증명에서 (가)에 알맞은 식을 [[f(n)]], (나)에 알맞은 식을 [[g(n)]]이라 할 때, [[f(2) + g(2)]]의 값은?"),
    choices=["[[4]]", "[[6]]", "[[8]]", "[[10]]", "[[12]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="(가)=₂ₙCₙ → f(2)=₄C₂=6, (나)=2ⁿ → g(2)=4, 합 10 → ④ = 빠른정답 ✓.")

# p54
add(id="65c06f71", qtype="choice",
    question=("다음은 등식 [[comb(n,r) + comb(n,r + 1) = comb(n + 1,r + 1)]]을 이용하여 "
              "[[pow(1,2) + pow(2,2) + pow(3,2)]] + ⋯ + [[pow(n,2) = frac(n(n + 1)(2n + 1), 6)]] ([[n]] = 1, 2, 3, ⋯)을 증명한 것이다.\n"
              "2 이상인 자연수 [[k]]에 대하여\n"
              "[[pow(k,2)]] = (가) + [[2 × comb(k,2)]]로 나타낼 수 있으므로\n"
              "[[pow(1,2) + pow(2,2) + pow(3,2)]] + ⋯ + [[pow(n,2)]]\n"
              "= [[comb(1,1) + (comb(2,1) + 2 × comb(2,2)) + (comb(3,1) + 2 × comb(3,2))]] + ⋯ + ((나) + [[2 × comb(n,2)]])\n"
              "= ([[comb(1,1) + comb(2,1) + comb(3,1)]] + ⋯ + (나)) + 2([[comb(2,2) + comb(3,2)]] + ⋯ + [[comb(n,2)]])\n"
              "= (다) + [[2 × comb(n + 1,3)]]\n"
              "= [[frac(n(n + 1)(2n + 1), 6)]]\n"
              "위의 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[comb(k,1)]], (나) [[comb(n,1)]], (다) [[comb(n,2)]]",
             "(가) [[comb(k,1)]], (나) [[comb(n,1)]], (다) [[comb(n + 1,2)]]",
             "(가) [[comb(k,1)]], (나) [[comb(n + 1,1)]], (다) [[comb(n,2)]]",
             "(가) [[comb(k + 1,1)]], (나) [[comb(n,1)]], (다) [[comb(n,2)]]",
             "(가) [[comb(k + 1,1)]], (나) [[comb(n + 1,1)]], (다) [[comb(n + 1,2)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="k²=ₖC₁+2ₖC₂ → (가)=ₖC₁, (나)=ₙC₁, (다)=ₙ₊₁C₂ → ②. 빠른정답 169는 값 아님(정렬 오류 의심).")

# p55
add(id="dcd5c73b", qtype="choice",
    question=("다음은 등식 [[comb(n,r) + comb(n,r + 1) = comb(n + 1,r + 1)]]을 이용하여 "
              "[[pow(1,2) + pow(2,2) + pow(3,2)]] + ⋯ + [[pow(n,2) = frac(n(n + 1)(2n + 1), 6)]]을 증명한 것이다. (단, [[n]]은 자연수)\n"
              "2 이상인 자연수 [[k]]에 대하여\n"
              "[[pow(k,2) = comb(k,1)]] + 2 · (가)로 나타낼 수 있으므로\n"
              "[[pow(1,2) + pow(2,2) + pow(3,2)]] + ⋯ + [[pow(n,2)]]\n"
              "= [[comb(1,1) + (comb(2,1) + 2 × comb(2,2)) + (comb(3,1) + 2 × comb(3,2))]] + ⋯ + ([[comb(n,1)]] + 2 · (나))\n"
              "= ([[comb(1,1) + comb(2,1) + comb(3,1)]] + ⋯ + [[comb(n,1)]]) + 2([[comb(2,2) + comb(3,2) + comb(4,2)]] + ⋯ + (나))\n"
              "= (다) + [[2 × comb(n + 1,3) = frac(n(n + 1)(2n + 1), 6)]]\n"
              "위의 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[comb(k,2)]], (나) [[comb(n,2)]], (다) [[comb(n,2)]]",
             "(가) [[comb(k,2)]], (나) [[comb(n,2)]], (다) [[comb(n + 1,2)]]",
             "(가) [[comb(k,2)]], (나) [[comb(n + 1,2)]], (다) [[comb(n,2)]]",
             "(가) [[comb(k + 1,2)]], (나) [[comb(n,2)]], (다) [[comb(n,2)]]",
             "(가) [[comb(k + 1,2)]], (나) [[comb(n + 1,2)]], (다) [[comb(n + 1,2)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="(가)=ₖC₂, (나)=ₙC₂, (다)=ₙ₊₁C₂(하키스틱) → ②. 빠른정답 4와 불일치.")

# p60 — [2007년 10월 고3 문과 13번]
add(id="416b4743", qtype="choice",
    question=("다음은 등식 [[comb(n,r) + comb(n,r + 1) = comb(n + 1,r + 1)]]을 이용하여 "
              "[[pow(1,2) + pow(2,2) + pow(3,2)]] + ⋯ + [[pow(n,2) = frac(n(n + 1)(2n + 1), 6)]] ([[n]] = 1, 2, 3, ⋯)\n"
              "을 증명한 것이다.\n"
              "<증명>\n"
              "2이상인 자연수 [[k]]에 대하여\n"
              "[[pow(k,2)]] = (가) + 2 · [[comb(k,2)]] 로 나타낼 수 있으므로\n"
              "[[pow(1,2) + pow(2,2) + pow(3,2)]] + ⋯ + [[pow(n,2)]]\n"
              "= [[comb(1,1) + (comb(2,1) + 2 × comb(2,2)) + (comb(3,1) + 2 × comb(3,2))]] + ⋯ + ([[comb(n,1)]] + 2 · (나))\n"
              "= ([[comb(1,1) + comb(2,1) + comb(3,1)]] + ⋯ + [[comb(n,1)]]) + 2([[comb(2,2) + comb(3,2)]] + ⋯ + (나))\n"
              "= [[comb(n + 1,2)]] + 2 · (다)\n"
              "= [[frac(n(n + 1)(2n + 1), 6)]]\n"
              "위 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[comb(k,1)]], (나) [[comb(n,2)]], (다) [[comb(n,3)]]",
             "(가) [[comb(k,1)]], (나) [[comb(n,2)]], (다) [[comb(n + 1,3)]]",
             "(가) [[comb(k,1)]], (나) [[comb(n + 1,2)]], (다) [[comb(n,3)]]",
             "(가) [[comb(k + 1,1)]], (나) [[comb(n,2)]], (다) [[comb(n,3)]]",
             "(가) [[comb(k + 1,1)]], (나) [[comb(n + 1,2)]], (다) [[comb(n + 1,3)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2007년 10월 고3 문과 13번]. (가)=ₖC₁, (나)=ₙC₂, (다)=ₙ₊₁C₃ → ②. 빠른정답 4와 불일치.")

# p61 — [2019년 4월 고3 이과 14번 변형]
add(id="dafd0e7e", qtype="choice",
    question=("집합 [[A]] = { [[x]] | [[x]]는 20 이하의 자연수 }의 부분집합 중 세 원소 1, 2, 3을 모두 포함하고 "
              "원소의 개수가 짝수인 부분집합의 개수는?"),
    choices=["[[pow(2,15)]]", "[[pow(2,16)]]", "[[pow(2,17)]]", "[[pow(2,18)]]", "[[pow(2,19)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 4월 고3 이과 14번 변형]. 나머지 17개 원소 중 홀수 개 선택 → 2¹⁶ → ② = 빠른정답 ✓.")

# p64
add(id="9d5b2996", qtype="choice",
    question=("집합 [[A]] = { [[x]] | [[x]]는 20 이하의 자연수 }의 부분집합 중 원소 1을 포함하고 원소의 개수가 홀수인 "
              "부분집합의 개수는?"),
    choices=["[[pow(2,16)]]", "[[pow(2,17)]]", "[[pow(2,18)]]", "[[pow(2,19)]]", "[[pow(2,20)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="나머지 19개 원소 중 짝수 개 선택 → 2¹⁸ → ③. 빠른정답 2와 불일치.")

# p90
add(id="a405e0fa", qtype="choice",
    question="파스칼의 삼각형을 이용하여 [[comb(3,3) + comb(4,3) + comb(5,3)]] + ⋯ + [[comb(11,3)]]을 간단히 하면?",
    choices=["[[comb(11,3)]]", "[[comb(11,4)]]", "[[comb(11,5)]]", "[[comb(12,4)]]", "[[comb(12,5)]]"],
    derived_answer="④",
    figure=[{"fn": "table", "args": {"rows": [["[[comb(1,0)]]", "[[comb(1,1)]]"],
                                              ["[[comb(2,0)]]", "[[comb(2,1)]]", "[[comb(2,2)]]"],
                                              ["[[comb(3,0)]]", "[[comb(3,1)]]", "[[comb(3,2)]]", "[[comb(3,3)]]"],
                                              ["[[comb(4,0)]]", "[[comb(4,1)]]", "[[comb(4,2)]]", "[[comb(4,3)]]", "[[comb(4,4)]]"],
                                              ["⋮"]]}}],
    difficulty_est=2, confidence=0.85,
    note="파스칼의 삼각형(조합 기호 배열)을 표로 표현. 하키스틱 Σ₍ₖ₌₃₎¹¹ ₖC₃ = ₁₂C₄ → ④. 빠른정답 5와 불일치.")

# ───────────────────────── 조건부확률 ─────────────────────────
# p9 — [2024년 9월 고3 확률과 통계 28번/4점]
add(id="ec5e4d3e", qtype="choice",
    question=("집합 [[X = set(1, 2, 3, 4)]]에 대하여 [[f]]: [[X]]→[[X]]인 모든 함수 [[f]] 중에서 임의로 하나를 선택하는 시행을 한다. "
              "이 시행에서 선택한 함수 [[f]]가 다음 조건을 만족시킬 때, [[f(4)]]가 짝수일 확률은?\n"
              "[[in(a, X)]], [[in(b, X)]]에 대하여 [[a]]가 [[b]]의 약수이면 [[f(a)]]는 [[f(b)]]의 약수이다."),
    choices=["[[frac(9,19)]]", "[[frac(8,15)]]", "[[frac(3,5)]]", "[[frac(27,40)]]", "[[frac(19,25)]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2024년 9월 고3 확률과 통계 28번/4점]. 전수 계산: 조건 만족 함수 40개 중 f(4) 짝수 27개 → 27/40 → ④. 빠른정답 1과 불일치.")

# p18
add(id="edffcc6f", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여 [[subset(A, B)]]이고, [[prob(A) = frac(1,5)]], [[prob(B) = frac(1,4)]]일 때, "
              "[[cprob(A, B)]]는?"),
    choices=["[[frac(1,5)]]", "[[frac(2,5)]]", "[[frac(3,5)]]", "[[frac(4,5)]]", "[[1]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="A⊂B → P(A∩B)=1/5, (1/5)/(1/4)=4/5 → ④ = 빠른정답 ✓.")

# p19 — [2019년 9월 고3 문과 8번/3점]
add(id="36ff599f", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여\n[[prob(A) = frac(7,10)]], [[prob(union(A, B)) = frac(9,10)]]\n"
              "일 때, [[cprob(comp(B), comp(A))]]의 값은?\n(단, [[comp(A)]]은 [[A]]의 여사건이다.)"),
    choices=["[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 9월 고3 문과 8번/3점]. (1/10)/(3/10)=1/3 → ④ = 빠른정답 ✓.")

# p21
add(id="da6eb90c", qtype="short",
    question=("두 사건 [[A]], [[B]]에 대하여 [[prob(A) = frac(2,5)]], [[prob(B) = frac(1,2)]], [[cprob(B, A) = frac(3,10)]]일 때, "
              "[[prob(inter(A, B))]]를 구하시오."),
    choices=None, derived_answer="frac(3,25)", figure=None, difficulty_est=1, confidence=0.9,
    note="2/5 × 3/10 = 3/25 = 빠른정답 ✓.")

# p22
add(id="2c1005cf", qtype="short",
    question=("두 사건 [[A]], [[B]]에 대하여 [[prob(A) = frac(1,5)]], [[prob(B) = frac(2,3)]], [[cprob(B, A) = frac(7,10)]]일 때, "
              "[[prob(inter(A, B))]]를 구하시오."),
    choices=None, derived_answer="frac(7,50)", figure=None, difficulty_est=1, confidence=0.9,
    note="1/5 × 7/10 = 7/50 = 빠른정답 ✓.")

# p24 — [2015년 7월 고3 문과 4번 변형]
add(id="fac40991", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여\n[[prob(A) = frac(2,5)]], [[prob(inter(A, B)) = frac(4,15)]]\n"
              "일 때, [[cprob(B, A)]]의 값은?"),
    choices=["[[frac(1,6)]]", "[[frac(1,3)]]", "[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(5,6)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2015년 7월 고3 문과 4번 변형]. (4/15)/(2/5)=2/3 → ④ = 빠른정답 ✓.")

# p25
add(id="fd88dcb1", qtype="short",
    question=("두 사건 [[A]], [[B]]에 대하여 [[prob(A) = frac(1,4)]], [[prob(union(A, B)) = frac(6,7)]]일 때, "
              "[[cprob(comp(B), comp(A))]]을 구하시오."),
    choices=None, derived_answer="frac(4,21)", figure=None, difficulty_est=2, confidence=0.9,
    note="P(Aᶜ∩Bᶜ)=1/7, P(Aᶜ)=3/4 → (1/7)/(3/4)=4/21. 빠른정답 1/21과 불일치.")

# p26
add(id="9d2fba67", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여\n[[prob(A) = frac(3,5)]], [[prob(B) = frac(3,7)]], [[prob(inter(A, B)) = frac(1,7)]]일 때,\n"
              "[[cprob(comp(B), comp(A))]]은? (단, [[comp(A)]]는 [[A]]의 여사건이다.)"),
    choices=["[[frac(1,7)]]", "[[frac(2,7)]]", "[[frac(3,7)]]", "[[frac(4,7)]]", "[[frac(5,7)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="P(A∪B)=31/35, P(Aᶜ∩Bᶜ)=4/35, P(Aᶜ)=14/35 → 2/7 → ② = 빠른정답 ✓.")

# p27
add(id="5cf5a350", qtype="short",
    question=("두 사건 [[A]], [[B]]에 대하여 [[prob(A) = frac(1,6)]], [[prob(union(A, B)) = frac(2,3)]]일 때, "
              "[[cprob(comp(B), comp(A))]]을 구하시오."),
    choices=None, derived_answer="frac(2,5)", figure=None, difficulty_est=2, confidence=0.9,
    note="(1/3)/(5/6)=2/5 = 빠른정답 ✓.")

# p28
add(id="731bc849", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여\n[[prob(A) = 4 prob(B) = frac(1,2)]], [[cprob(A, B) = cprob(B, A) + frac(1,2)]]\n"
              "일 때, [[prob(inter(A, B))]]의 값은?"),
    choices=["[[frac(1,24)]]", "[[frac(1,18)]]", "[[frac(1,12)]]", "[[frac(1,9)]]", "[[frac(1,6)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="P(B)=1/8, x=P(A∩B): 8x=2x+1/2 → x=1/12 → ③ = 빠른정답 ✓.")

# p29
add(id="068e9e05", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여 [[prob(A) = frac(2,3)]], [[prob(comp(B)) = frac(3,4)]],\n"
              "[[cprob(B, A) = frac(1,3)]]일 때, [[cprob(A, comp(B))]]는?"),
    choices=["[[frac(4,9)]]", "[[frac(13,27)]]", "[[frac(14,27)]]", "[[frac(5,9)]]", "[[frac(16,27)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="P(A∩B)=2/9, P(A∩Bᶜ)=4/9 → (4/9)/(3/4)=16/27 → ⑤ = 빠른정답 ✓.")

# p30
add(id="d3d19808", qtype="short",
    question=("두 사건 [[A]], [[B]]에 대하여 [[prob(A) = frac(2,7)]], [[prob(B) = frac(4,7)]],\n"
              "[[prob(union(A, B)) = frac(11,14)]]일 때, [[cprob(A, B)]]를 구하시오."),
    choices=None, derived_answer="frac(1,8)", figure=None, difficulty_est=2, confidence=0.9,
    note="P(A∩B)=1/14 → (1/14)/(4/7)=1/8 = 빠른정답 ✓.")

# p31 — [2020년 11월 고3 이과 4번/3점]
add(id="b2d15951", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여 [[cprob(B, A) = frac(1,4)]], [[cprob(A, B) = frac(1,3)]],\n"
              "[[prob(A) + prob(B) = frac(7,10)]]일 때, [[prob(inter(A, B))]]의 값은?"),
    choices=["[[frac(1,7)]]", "[[frac(1,8)]]", "[[frac(1,9)]]", "[[frac(1,10)]]", "[[frac(1,11)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2020년 11월 고3 이과 4번/3점]. P(A)=4x, P(B)=3x, 7x=7/10 → x=1/10 → ④ = 빠른정답 ✓.")

# p33 — [2009년 9월 고3 문과 4번]
add(id="b98fde0d", qtype="choice",
    question="두 사건 [[A]], [[B]]에 대하여 [[prob(A) = cprob(B, A) = frac(2,3)]]일 때,\n[[prob(inter(A, B))]]의 값은?",
    choices=["[[frac(5,18)]]", "[[frac(1,3)]]", "[[frac(7,18)]]", "[[frac(4,9)]]", "[[frac(1,2)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2009년 9월 고3 문과 4번]. 2/3 × 2/3 = 4/9 → ④ = 빠른정답 ✓.")

# p34 — [2016년 4월 고3 이과 5번 변형]
add(id="2be4989d", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여\n[[prob(comp(A)) = frac(1,3)]], [[cprob(B, A) = frac(1,4)]]\n"
              "일 때, [[prob(inter(A, B))]]의 값은? (단, [[comp(A)]]은 [[A]]의 여사건이다.)"),
    choices=["[[frac(1,8)]]", "[[frac(1,7)]]", "[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2016년 4월 고3 이과 5번 변형]. P(A)=2/3, 2/3 × 1/4 = 1/6 → ③. 빠른정답 4와 불일치.")

# p77 — [2010년 10월 고3 문과 9번]
add(id="322848f4", qtype="choice",
    question=("어떤 시행에서 나올 수 있는 모든 결과의 집합을 [[S]]라 하자. [[S]]의 부분집합인 세 사건 [[A]], [[B]], [[C]]가 "
              "다음 조건을 만족시킨다.\n"
              "(가) [[union(union(A, B), C) = S]]\n"
              "(나) [[A]], [[B]], [[C]] 중 어느 두 사건도 동시에 일어나지 않는다.\n"
              "(다) [[prob(A) = 2 prob(B) = 4 prob(C)]]\n"
              "[[S]]의 부분집합인 사건 [[D]]에 대하여\n"
              "[[cprob(D, A) = frac(1,10)]], [[cprob(D, B) = frac(1,5)]], [[cprob(D, C) = frac(3,10)]]\n"
              "일 때, [[prob(D)]]의 값은?"),
    choices=["[[frac(9,70)]]", "[[frac(11,70)]]", "[[frac(13,70)]]", "[[frac(3,14)]]", "[[frac(17,70)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2010년 10월 고3 문과 9번]. P(A,B,C)=4/7,2/7,1/7 → P(D)=4/70+4/70+3/70=11/70 → ② = 빠른정답 ✓.")

# p98 — [2026년 7월 고3 확률과 통계 30번 변형]
add(id="453ae6ee", qtype="short",
    question=("수직선의 원점에 점 P가 있다. 한 개의 주사위를 사용하여 다음 시행을 한다.\n"
              "주사위를 한 번 던져 나온 눈의 수를 [[k]]라 하자.\n"
              "[[k]]가 5의 약수이면 점 P를 양의 방향으로 1만큼 이동시키고,\n"
              "[[k]]가 6이면 점 P를 음의 방향으로 1만큼 이동시키고,\n"
              "그 외의 경우는 점 P를 이동시키지 않는다.\n"
              "이 시행을 5번 반복할 때, [[n]] ([[1 <= n <= 5]])번째 시행 후 점 P의 좌표를 [[sub(a,n)]]이라 하자. "
              "[[sub(a,1) = 0]]이고 [[sub(a,5) = 1]]일 때, 집합 { [[sub(a,m)]] | [[m]]은 5 이하의 자연수 }의 원소 중 가장 큰 값이 "
              "2일 확률은 [[frac(q,p)]]이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="17", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2026년 7월 고3 확률과 통계 30번 변형]. 전수 계산(+1: 1/3, −1: 1/6, 0: 1/2): 조건부확률 2/15 → p+q=17. 빠른정답 238과 불일치.")

# ───────────────────────── 확률변수와 확률분포 ─────────────────────────
# p14
add(id="28b3ff59", qtype="choice",
    question=("확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = frac(x, 10)]] ([[x]] = 1, 2, 3, 4)일 때,\n"
              "[[prob(pow(X,2) - 3X + 2 = 0)]]은?"),
    choices=["[[frac(1,10)]]", "[[frac(1,5)]]", "[[frac(3,10)]]", "[[frac(2,5)]]", "[[frac(1,2)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="X=1 또는 2 → 1/10+2/10=3/10 → ③. 빠른정답 20과 불일치.")

# p15
add(id="12de0151", qtype="short",
    question=("확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = frac(x, 10)]] ([[x]] = 1, 2, 3, 4)일 때,\n"
              "[[prob(pow(X,2) - 4X + 3 = 0) = frac(q,p)]]이다. 이때 [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="X=1 또는 3 → 4/10=2/5 → p+q=7. 빠른정답 '이산'은 값 아님.")

# p17
add(id="9cd36589", qtype="short",
    question=("확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = frac(x, 10)]] ([[x]] = 1, 2, 3, 4)일 때,\n"
              "[[prob(pow(X,2) - 6X + 8 = 0) = frac(q,p)]]이다. 이때 [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="X=2 또는 4 → 6/10=3/5 → p+q=8 = 빠른정답 ✓.")

# p18
add(id="04b22b46", qtype="choice",
    question=("이산확률변수 [[X]]가 갖는 값이 1, 2, 3, ⋯, [[n]]이고 [[X]]의 확률질량함수가\n"
              "[[prob(X = x) = frac(a x, 36)]] ([[x]] = 1, 2, 3, ⋯, [[n]])이다.\n"
              "[[prob(X = 4) = frac(1,9)]]일 때, [[prob(X = 2) - prob(X = 1)]]의 값은?\n"
              "(단, [[n]]은 자연수이고 [[a]]는 상수이다.)"),
    choices=["[[frac(1,30)]]", "[[frac(1,32)]]", "[[frac(1,34)]]", "[[frac(1,36)]]", "[[frac(1,38)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="4a/36=1/9 → a=1 → 2/36−1/36=1/36 → ④ (n=8). 빠른정답 없음.")

# p20
add(id="21ea20aa", qtype="choice",
    question=("확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = frac(x, k + 1)]] ([[x]] = 2, 3, 4)일 때,\n"
              "[[prob(3 <= X <= 4)]]는? (단, [[k]]는 상수이다.)"),
    choices=["[[frac(5,8)]]", "[[frac(7,9)]]", "[[frac(7,8)]]", "[[frac(8,9)]]", "[[frac(9,10)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="9/(k+1)=1 → k+1=9 → 7/9 → ②. 빠른정답 없음.")

# p21 — 조각적 정의
add(id="1812aeb5", qtype="choice",
    question=("확률변수 [[X]]의 확률질량함수가\n"
              "[[prob(X = x)]] = [[frac(x, 8) + k]] ([[x]] = 1, 2), [[k]] ([[x]] = 3, 4)\n"
              "일 때, 상수 [[k]]의 값은?"),
    choices=["[[frac(1,32)]]", "[[frac(1,16)]]", "[[frac(3,32)]]", "[[frac(1,8)]]", "[[frac(5,32)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 P(X=x)={x/8+k (x=1,2); k (x=3,4)}",
    note="3/8+4k=1 → k=5/32 → ⑤. 빠른정답 없음.")

# p22 — 조각적 정의
add(id="1ce47ee7", qtype="choice",
    question=("확률변수 [[X]]의 확률질량함수가\n"
              "[[prob(X = x)]] = [[-frac(x, 7) + k]] ([[x]] = -1, 0), [[frac(x, 7) + k]] ([[x]] = 1, 2)\n"
              "일 때, 상수 [[k]]의 값은?"),
    choices=["[[frac(1,28)]]", "[[frac(1,14)]]", "[[frac(3,28)]]", "[[frac(1,7)]]", "[[frac(5,28)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 P(X=x)={−x/7+k (x=−1,0); x/7+k (x=1,2)}",
    note="4/7+4k=1 → k=3/28 → ③. 빠른정답 없음.")

# p23 — 조각적 정의
add(id="4029b6cc", qtype="choice",
    question=("이산확률변수 [[X]]가 취할 수 있는 값이 -3, -1, 0, 1, 3이고 [[X]]의 확률질량함수가\n"
              "[[prob(X = x)]] = [[k - frac(x, 10)]] ([[x]] = -3, -1, 0), [[k + frac(x, 10)]] ([[x]] = 1, 3)\n"
              "일 때, 상수 [[k]]의 값은?"),
    choices=["[[frac(1,25)]]", "[[frac(2,25)]]", "[[frac(3,25)]]", "[[frac(4,25)]]", "[[frac(1,5)]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 P(X=x)={k−x/10 (x=−3,−1,0); k+x/10 (x=1,3)}",
    note="5k+8/10=1 → k=1/25 → ①. 빠른정답 없음.")

# p25
add(id="f2e959c6", qtype="short",
    question=("확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = frac(k, (x - 2)(x - 1))]] ([[x]] = 3, 4, ⋯, 9)\n"
              "일 때, [[prob(X = 9)]]를 구하시오. (단, [[k]]는 상수)"),
    choices=None, derived_answer="frac(1,49)", figure=None, difficulty_est=2, confidence=0.9,
    note="Σ k(1/(x−2)−1/(x−1)) = 7k/8 = 1 → k=8/7 → P(X=9)=(8/7)/56=1/49. 빠른정답 1/19와 불일치.")

# p26 — [2008년 9월 고3 이과 확률과 통계 27번] 조각적 정의
add(id="9794ed2c", qtype="choice",
    question=("이산확률변수 [[X]]가 취할 수 있는 값이 -2, -1, 0, 1, 2이고 [[X]]의 확률질량함수가\n"
              "[[prob(X = x)]] = [[k - frac(x, 9)]] ([[x]] = -2, -1, 0), [[k + frac(x, 9)]] ([[x]] = 1, 2)\n"
              "일 때, 상수 [[k]]의 값은?"),
    choices=["[[frac(1,15)]]", "[[frac(2,15)]]", "[[frac(1,5)]]", "[[frac(4,15)]]", "[[frac(1,3)]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 P(X=x)={k−x/9 (x=−2,−1,0); k+x/9 (x=1,2)}",
    note="출처 [2008년 9월 고3 이과 확률과 통계 27번]. 5k+6/9=1 → k=1/15 → ①. 빠른정답 없음.")

# p27 — 조각적 정의
add(id="466846f8", qtype="choice",
    question=("확률변수 [[X]]의 확률질량함수가\n"
              "[[prob(X = x)]] = [[frac(x, 3) + 2k]] ([[x]] = -2, -1), [[k]] ([[x]] = 0, 1)\n"
              "일 때, 상수 [[k]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[frac(1,3)]]", "[[frac(1,4)]]", "[[frac(1,5)]]", "[[frac(1,6)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 P(X=x)={x/3+2k (x=−2,−1); k (x=0,1)}",
    note="−1+6k=1 → k=1/3 → ②. 빠른정답 없음.")

# p28 — 조각적 정의
add(id="d6ad04c6", qtype="choice",
    question=("확률변수 [[X]]의 확률질량함수가\n"
              "[[prob(X = x)]] = [[frac(x, 11) + k]] ([[x]] = 0, 1, 2), [[frac(x, 11) - k]] ([[x]] = 3, 4)\n"
              "일 때, P([[X = 3]] 또는 [[X = 4]])는? (단, [[k]]는 상수이다.)"),
    choices=["[[frac(3,11)]]", "[[frac(4,11)]]", "[[frac(5,11)]]", "[[frac(6,11)]]", "[[frac(7,11)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 P(X=x)={x/11+k (x=0,1,2); x/11−k (x=3,4)}; 'P(X=3 또는 X=4)'는 텍스트 혼합",
    note="10/11+k=1 → k=1/11 → P=(3+4)/11−2/11=5/11 → ③. 빠른정답 없음.")

# p29
add(id="7160218f", qtype="choice",
    question=("이산확률변수 [[X]]가 갖는 값이 -1, 0, 1, 2이고\n[[prob(X = k + 1) = 2 prob(X = k)]] ([[k]] = 0, 1)\n"
              "이다. [[ev(X) = frac(7,10)]]일 때, [[prob(X = -1) - prob(X = 0)]]의 값은?"),
    choices=["[[-frac(1,5)]]", "[[-frac(1,10)]]", "[[0]]", "[[frac(1,10)]]", "[[frac(1,5)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="P(0)=a, P(1)=2a, P(2)=4a, P(−1)=b: b+7a=1, 10a−b=7/10 → a=1/10, b=3/10 → 1/5 → ⑤. 빠른정답 없음.")

# p30 — 조각적 정의
add(id="61295479", qtype="choice",
    question=("이산확률변수 [[X]]의 확률분포가\n"
              "[[prob(X = x)]] = [[frac(x, 8) + k]] ([[x]] = 1, 2, 3), [[k]] ([[x]] = 4, 5, 6)\n"
              "일 때, 확률 [[prob(abs(X - 4) <= 1)]]은? (단, [[k]]는 상수)"),
    choices=["[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 P(X=x)={x/8+k (x=1,2,3); k (x=4,5,6)}",
    note="6/8+6k=1 → k=1/24 → P(3≤X≤5)=3/8+2/24+1/24=1/2 → ⑤. 빠른정답 없음.")

# p31
add(id="8353588b", qtype="choice",
    question=("확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = a(x - 2)]] ([[x]] = 3, 4, 5)일 때,\n"
              "[[prob(X >= 4)]]은? (단, [[a]]는 상수이다.)"),
    choices=["[[frac(1,6)]]", "[[frac(1,3)]]", "[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(5,6)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="6a=1 → a=1/6 → P(X≥4)=5/6 → ⑤. 빠른정답 없음.")

# p36 — [2006년 9월 고3 이과 13번]
add(id="6ccf8af3", qtype="choice",
    question=("이산확률변수 [[X]]의 확률분포표는 다음과 같다.\n"
              "(단, [[sub(p,i) > 0]]이고 [[i]] = 0, 1, 2, ⋯, 10이다.)\n"
              "집합 [[setb(x, 0 <= x <= 10)]]에서 정의된 두 함수 [[F(x)]], [[G(x)]]가\n"
              "[[F(x) = prob(0 <= X <= x)]], [[G(x) = prob(X > x)]]\n"
              "일 때, <보기>에서 옳은 것을 모두 고른 것은?\n<보기>\n"
              "ㄱ. [[G(3) = 1 - F(3)]]\n"
              "ㄴ. [[prob(3 <= X <= 8) = F(8) - F(3)]]\n"
              "ㄷ. [[prob(3 <= X <= 8) = G(2) - G(8)]]"),
    choices=CH_G2, derived_answer="④",
    figure=[{"fn": "table", "args": {"head": ["[[X]]", "[[0]]", "[[1]]", "[[2]]", "⋯", "[[10]]", "계"],
                                     "rows": [["[[prob(X = x)]]", "[[sub(p,0)]]", "[[sub(p,1)]]", "[[sub(p,2)]]", "⋯", "[[sub(p,10)]]", "[[1]]"]]}}],
    difficulty_est=3, confidence=0.9,
    note="출처 [2006년 9월 고3 이과 13번]. ㄱ ✓, ㄴ F(8)−F(3)=P(4≤X≤8) ✗, ㄷ G(2)−G(8)=P(3≤X≤8) ✓ → ④ ㄱ, ㄷ. 빠른정답 없음.")

# p38
add(id="b064dd2c", qtype="choice",
    question=("다음은 확률변수 [[X]]의 확률분포를 표로 나타낸 것이다.\n"
              "(단, [[sub(p,i) > 0]], [[i]] = 0, 1, 2, ⋯, 10)\n"
              "집합 { [[0]], [[1]], [[2]], ⋯, [[10]] }에서 정의된 두 함수 [[F(x)]], [[G(x)]]가 [[F(x) = prob(0 <= X <= x)]], "
              "[[G(x) = prob(X > x)]]일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[prob(5 <= X <= 9) = F(9) - F(4)]]\n"
              "ㄴ. [[prob(5 <= X <= 9) = G(5) - G(9)]]\n"
              "ㄷ. [[F(6) = 1 - G(6)]]"),
    choices=CH_G3, derived_answer="③",
    figure=[{"fn": "table", "args": {"head": ["[[X]]", "[[0]]", "[[1]]", "[[2]]", "⋯", "[[10]]", "합계"],
                                     "rows": [["[[prob(X = x)]]", "[[sub(p,0)]]", "[[sub(p,1)]]", "[[sub(p,2)]]", "⋯", "[[sub(p,10)]]", "[[1]]"]]}}],
    difficulty_est=3, confidence=0.9,
    note="ㄱ ✓, ㄴ G(5)−G(9)=P(6≤X≤9) ✗, ㄷ F(6)=1−G(6) ✓ → ③ ㄱ, ㄷ. 빠른정답 없음.")

# p96 — [2005년 10월 고3 이과 5번] 조각적 정의 + 그래프
add(id="8843c3bd", qtype="choice",
    question=("연속확률변수 [[X]]의 확률밀도함수 [[f(x)]]가\n"
              "[[f(x)]] = [[abs(x - 1)]] ([[0 <= x <= 2]]), [[0]] ([[x < 0]], [[x > 2]])\n"
              "이고, 그 그래프는 그림과 같다.\n"
              "이 때, 확률 [[prob(frac(1,2) <= X <= frac(3,2))]]의 값은?"),
    choices=["[[frac(1,16)]]", "[[frac(1,8)]]", "[[frac(1,6)]]", "[[frac(1,4)]]", "[[frac(1,2)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: (0,1)에서 (1,0)으로 내려가고 (2,1)로 올라가는 V자 꺾은선(x<0, x>2에서는 0), 점선으로 y=1과 x=2 표시, 원점 O·1·2 눈금"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 f(x)={|x−1| (0≤x≤2); 0 (x<0, x>2)} / 도형 표현 불가: 함수 그래프",
    note="출처 [2005년 10월 고3 이과 5번]. 두 직각삼각형 넓이 2×(1/2·1/2·1/2)=1/4 → ④. 빠른정답 없음.")

# ───────────────────────── 모평균의 추정 ─────────────────────────
# p4
add(id="3d28869b", qtype="short",
    question=("모집단 [[set(1, 3, 7, 9)]]에서 크기가 2인 표본을 임의로 복원추출할 때, 표본평균 [[conj(X)]]의 확률분포를 표로 나타내면 "
              "다음과 같다. 0이 아닌 세 상수 [[a]], [[b]], [[c]]에 대하여 [[a b c]]의 값을 구하시오."),
    choices=None, derived_answer="256",
    figure=[{"fn": "table", "args": {"head": ["[[conj(X)]]", "[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]", "합계"],
                                     "rows": [["[[prob(conj(X) = conj(x))]]", "[[frac(1,16)]]", "[[frac(1,8)]]", "[[frac(1,16)]]", "[[frac(1,a)]]", "[[frac(1,b)]]",
                                               "[[frac(1,8)]]", "[[frac(1,16)]]", "[[frac(1,c)]]", "[[frac(1,16)]]", "[[1]]"]]}}],
    difficulty_est=2, confidence=0.8, needs_review=XBAR_REVIEW,
    note="16가지 중 X̄=4: 2/16 → a=8, X̄=5: 4/16 → b=4, X̄=8: 2/16 → c=8 → abc=256 = 빠른정답 ✓.")

# p6
add(id="6901a158", qtype="short",
    question=("모집단 [[set(2, 4, 6)]]에서 크기가 2인 표본을 복원추출할 때, 표본평균 [[conj(X)]]의 확률분포가 다음 표와 같다. "
              "이때 상수 [[a]], [[b]], [[c]]에 대하여 [[9(a + 2b + c)]]의 값을 구하시오."),
    choices=None, derived_answer="8",
    figure=[{"fn": "table", "args": {"head": ["[[conj(X)]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]", "합계"],
                                     "rows": [["[[prob(conj(X) = conj(x))]]", "[[a]]", "[[b]]", "[[c]]", "[[frac(2,9)]]", "[[frac(1,9)]]", "[[1]]"]]}}],
    difficulty_est=2, confidence=0.8, needs_review=XBAR_REVIEW,
    note="a=1/9, b=2/9, c=3/9 → 9(1/9+4/9+3/9)=8 = 빠른정답 ✓.")

# p8
add(id="efe6b491", qtype="short",
    question=("모평균이 14, 모표준편차가 3인 어떤 모집단에서 크기가 9인 표본을 임의추출할 때, 표본평균 [[conj(X)]]에 대하여 "
              "[[sd(conj(X))]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=1, confidence=0.8, needs_review=XBAR_REVIEW,
    note="σ(X̄)=3/√9=1. 빠른정답 3과 불일치.")

# p9 — [2022년 10월 고3 확률과 통계 23번/2점]
add(id="b7923ed2", qtype="choice",
    question=("표준편차가 12인 정규분포를 따르는 모집단에서 크기가 36인 표본을 임의추출하여 구한 표본평균을 [[conj(X)]]라 할 때, "
              "[[sd(conj(X))]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.8, needs_review=XBAR_REVIEW,
    note="출처 [2022년 10월 고3 확률과 통계 23번/2점]. 12/√36=2 → ②. 빠른정답 8과 불일치.")

# p15 — [2010년 9월 고3 문과 29번]
add(id="cf61e054", qtype="choice",
    question=("다음은 어느 모집단의 확률분포표이다.\n"
              "이 모집단에서 크기가 16인 표본을 임의추출할 때, 표본평균 [[conj(X)]]의 표준편차는?(단, [[a]]는 상수이다.)"),
    choices=["[[frac(sqrt(6), 8)]]", "[[frac(sqrt(6), 6)]]", "[[frac(sqrt(6), 4)]]", "[[frac(sqrt(6), 2)]]", "[[sqrt(6)]]"],
    derived_answer="①",
    figure=[{"fn": "table", "args": {"head": ["[[X]]", "[[-2]]", "[[0]]", "[[1]]", "계"],
                                     "rows": [["[[prob(X = x)]]", "[[frac(1,4)]]", "[[a]]", "[[frac(1,2)]]", "[[1]]"]]}}],
    difficulty_est=2, confidence=0.8, needs_review=XBAR_REVIEW,
    note="출처 [2010년 9월 고3 문과 29번]. a=1/4, E(X)=0, V(X)=3/2 → σ(X̄)=(√6/2)/4=√6/8 → ①. 빠른정답 2와 불일치.")

# p18
add(id="be4386ce", qtype="choice",
    question=("다음은 어느 모집단의 확률분포를 표로 나타낸 것이다.\n"
              "이 모집단에서 크기가 12인 표본을 임의추출할 때, 표본평균 [[conj(X)]]의 표준편차는?"),
    choices=["[[frac(1,2)]]", "[[frac(sqrt(10), 6)]]", "[[frac(sqrt(11), 6)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(13), 6)]]"],
    derived_answer="③",
    figure=[{"fn": "table", "args": {"head": ["[[X]]", "[[2]]", "[[4]]", "[[6]]", "[[8]]", "합계"],
                                     "rows": [["[[prob(X = x)]]", "[[frac(1,6)]]", "[[a]]", "[[frac(1,3)]]", "[[frac(1,6)]]", "[[1]]"]]}}],
    difficulty_est=2, confidence=0.8, needs_review=XBAR_REVIEW,
    note="a=1/3, E(X)=5, V(X)=11/3 → σ(X̄)=√(11/36)=√11/6 → ③. 빠른정답 1과 불일치.")

# p20
add(id="92e8a462", qtype="choice",
    question=("어느 모집단의 확률변수 [[X]]의 확률분포를 표로 나타내면 다음과 같다. [[ev(pow(X,2)) = 21]]일 때, 이 모집단에서 "
              "임의추출한 크기가 10인 표본의 표본평균 [[conj(X)]]에 대하여 [[var(conj(X))]]는?"),
    choices=["[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    derived_answer="⑤",
    figure=[{"fn": "table", "args": {"head": ["[[X]]", "[[0]]", "[[3]]", "[[6]]", "합계"],
                                     "rows": [["[[prob(X = x)]]", "[[frac(1,6)]]", "[[a]]", "[[b]]", "[[1]]"]]}}],
    difficulty_est=2, confidence=0.8, needs_review=XBAR_REVIEW,
    note="a=1/3, b=1/2, E(X)=4, V(X)=21−16=5 → V(X̄)=5/10=1/2 → ⑤. 빠른정답 3과 불일치.")

# p41 — [2021년 9월 고3 확률과 통계 27번/3점]
add(id="b66acec2", qtype="choice",
    question=("지역 A에 살고 있는 성인들의 1인 하루 물 사용량을 확률변수 [[X]], 지역 B에 살고 있는 성인들의 1인 하루 물 사용량을 "
              "확률변수 [[Y]]라 하자. 두 확률변수 [[X]], [[Y]]는 정규분포를 따르고 다음 조건을 만족시킨다.\n"
              "(가) 두 확률변수 [[X]], [[Y]]의 평균은 각각 220과 240이다.\n"
              "(나) 확률변수 [[Y]]의 표준편차는 확률변수 [[X]]의 표준편차의 1.5배이다.\n"
              "지역 A에 살고 있는 성인 중 임의추출한 [[n]]명의 1인 하루 물 사용량의 표본평균을 [[conj(X)]], 지역 B에 살고 있는 성인 중 "
              "임의추출한 [[9n]]명의 1인 하루 물 사용량의 표본평균을 [[conj(Y)]]라 하자. [[prob(conj(X) <= 215) = 0.1587]]일 때, "
              "[[prob(conj(Y) >= 235)]]의 값을 다음 표준정규분포표를 이용하여 구한 것은? (단, 물 사용량의 단위는 L이다.)"),
    choices=["[[0.6915]]", "[[0.7745]]", "[[0.8185]]", "[[0.8413]]", "[[0.9772]]"],
    derived_answer="⑤",
    figure=[{"fn": "table", "args": {"head": ["[[z]]", "[[prob(0 <= Z <= z)]]"],
                                     "rows": [["[[0.5]]", "[[0.1915]]"], ["[[1.0]]", "[[0.3413]]"], ["[[1.5]]", "[[0.4332]]"], ["[[2.0]]", "[[0.4772]]"]]}}],
    difficulty_est=3, confidence=0.8, needs_review=XBAR_REVIEW,
    note="출처 [2021년 9월 고3 확률과 통계 27번/3점]. σ/√n=5, σ(Ȳ)=2.5 → P(Z≥−2)=0.9772 → ⑤ = 빠른정답 ✓.")

# p71 — [2019년 9월 고3 문과 25번 변형]
add(id="7af5b0e7", qtype="short",
    question=("어느 영화관을 방문한 고객의 머무른 시간은 평균이 [[m]]분, 표준편차가 σ분인 정규분포를 따른다고 한다. 이 영화관을 "
              "방문한 고객 중 100명을 임의추출하여 얻은 표본평균을 이용하여, 이 영화관을 방문한 고객의 머무른 시간의 평균 [[m]]에 대한 "
              "신뢰도 [[pct(99)]]의 신뢰구간을 구하면 [[a <= m <= b]]이다. [[b - a = 7.74]]일 때, σ의 값을 구하시오. "
              "(단, [[Z]]가 표준정규분포를 따르는 확률변수일 때, [[prob(abs(Z) <= 2.58) = 0.99]]로 계산한다.)"),
    choices=None, derived_answer="15", figure=None, difficulty_est=2, confidence=0.85,
    note="출처 [2019년 9월 고3 문과 25번 변형]. σ(그리스 문자, 문법 미지원)는 본문 텍스트로. 2·2.58·σ/10=7.74 → σ=15 = 빠른정답 ✓.")

# p72 — [2008년 9월 고3 이과 확률과 통계 29번]
add(id="73916e86", qtype="choice",
    question=("모집단 [[A]]는 정규분포 N([[sub(m,1)]], σ²)을 따르고, 모집단 [[B]]는 정규분포 N([[sub(m,2)]], (σ/2)²)을 따른다. "
              "모집단 [[A]]에서 크기 [[sub(n,1)]], 모집단 [[B]]에서 크기 [[sub(n,2)]]인 표본을 각각 임의추출할 때의 표본평균을 각각 "
              "[[conj(sub(X,A))]], [[conj(sub(X,B))]]라 하자. <보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
              "(단, [[sub(n,1)]], [[sub(n,2)]]는 1보다 큰 자연수이다.)\n<보기>\n"
              "ㄱ. [[sub(m,1) = sub(m,2)]]이면 [[ev(conj(sub(X,A))) = ev(conj(sub(X,B)))]]이다.\n"
              "ㄴ. 표본평균 [[conj(sub(X,B))]]는 정규분포 N([[sub(m,2)]], (σ/2)²)을 따른다.\n"
              "ㄷ. [[sub(n,1) = 4 sub(n,2)]]일 때, [[sub(m,1)]]에 대한 신뢰도 [[pct(95)]]의 신뢰구간이 [[itv(a, b, cc)]]이고, "
              "[[sub(m,2)]]에 대한 신뢰도 [[pct(95)]]의 신뢰구간이 [[itv(c, d, cc)]]이면, [[b - a = d - c]]이다."),
    choices=CH_G2, derived_answer="③", figure=None, difficulty_est=3, confidence=0.75,
    needs_review="문법 한계: σ(그리스 문자) 미지원으로 N(m₁, σ²)·(σ/2)²를 텍스트 혼합 / 첨자 달린 표본평균 X̄_A, X̄_B를 conj(sub(X,A))로 표기",
    note="출처 [2008년 9월 고3 이과 확률과 통계 29번]. ㄱ ✓, ㄴ V(X̄_B)=σ²/(4n₂) ✗, ㄷ 길이 모두 1.96σ/√n₂ ✓ → ③ = 빠른정답 ✓.")

# p73 (id 2개)
dup(["ae71c4e5", "19f5b1a4"], qtype="choice",
    question=("정규분포 [[normald(m, pow(2,2))]]을 따르는 모집단에서 임의추출한 크기가 4인 표본과 크기가 16인 표본의 표본평균을 "
              "각각 [[conj(sub(X,A))]], [[conj(sub(X,B))]]라 하고, [[conj(sub(X,A))]]와 [[conj(sub(X,B))]]의 분포를 이용하여 "
              "신뢰도 [[pct(90)]]로 추정한 모평균 [[m]]의 신뢰구간을 각각 [[a <= m <= b]], [[c <= m <= d]]라고 하자. "
              "다음 보기 중 항상 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[conj(sub(X,A))]]의 분산은 [[conj(sub(X,B))]]의 분산보다 크다.\n"
              "ㄴ. [[prob(conj(sub(X,A)) <= m + 1) <= prob(conj(sub(X,B)) <= m + 1)]]\n"
              "ㄷ. [[d - c < b - a]]"),
    choices=CH_G1, derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.75,
    needs_review="문법 한계: 첨자 달린 표본평균 X̄_A, X̄_B를 conj(sub(X,A))로 표기",
    note="같은 쪽에 id 2개. ㄱ V=1 vs 1/4 ✓, ㄴ P(Z≤1)≤P(Z≤2) ✓, ㄷ 1.645 < 3.29 ✓ → ⑤ = 빠른정답 ✓.")

# p75 — [2022년 11월 고3 확률과통계 27번 변형]
add(id="1c7b092a", qtype="choice",
    question=("어느 회사에서 생산하는 린스 1개의 용량은 정규분포 N([[m]], σ²)을 따른다고 한다. 이 회사에서 생산하는 린스 중에서 "
              "100개를 임의추출하여 얻은 표본평균을 이용하여 구한 [[m]]에 대한 신뢰도 [[pct(95)]]의 신뢰구간이 "
              "[[752.96 <= m <= 760.8]]이다. 이 회사에서 생산하는 린스 중에서 [[n]]개를 임의추출하여 얻은 표본평균을 이용하여 구하는 "
              "[[m]]에 대한 신뢰도 [[pct(99)]]의 신뢰구간이 [[a <= m <= b]]일 때, [[b - a]]의 값이 8 이하가 되기 위한 자연수 [[n]]의 "
              "최솟값은? (단, 용량의 단위는 mL이고, [[Z]]가 표준정규분포를 따르는 확률변수일 때, [[prob(abs(Z) <= 1.96) = 0.95]], "
              "[[prob(abs(Z) <= 2.58) = 0.99]]로 계산한다.)"),
    choices=["[[167]]", "[[168]]", "[[169]]", "[[170]]", "[[171]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: σ(그리스 문자) 미지원으로 N(m, σ²)를 텍스트 혼합",
    note="출처 [2022년 11월 고3 확률과통계 27번 변형]. 7.84=2·1.96·σ/10 → σ=20; 103.2/√n≤8 → n≥166.41 → 167 → ①. 빠른정답 3과 불일치.")

# p87 — [2010년 4월 고3 이과 13번]
add(id="8dcfd9b2", qtype="choice",
    question=("분산이 σ²인 정규분포를 따르는 모집단에서 크기 [[n]]인 표본을 임의추출하여 모평균 [[m]]을 추정한 후 신뢰구간의 "
              "길이를 구하고자 한다. 아래 표준정규분포표를 이용하여 구한 모평균 [[m]]에 대한 신뢰도 [[pct(79.6)]]의 신뢰구간의 길이가 "
              "[[l]]이고, 모평균 [[m]]에 대한 신뢰도 [[pct(alpha)]]의 신뢰구간의 길이는 [[2l]]이다. 이 때, [[alpha]]의 값은?"),
    choices=["[[87.3]]", "[[90.9]]", "[[95.0]]", "[[98.9]]", "[[99.9]]"],
    derived_answer="④",
    figure=[{"fn": "table", "args": {"head": ["[[z]]", "[[prob(0 <= Z <= z)]]"],
                                     "rows": [["[[1.27]]", "[[0.3980]]"], ["[[1.69]]", "[[0.4545]]"], ["[[1.96]]", "[[0.4750]]"],
                                              ["[[2.54]]", "[[0.4945]]"], ["[[3.29]]", "[[0.4995]]"]]}}],
    difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: σ(그리스 문자) 미지원으로 '분산이 σ²인'을 텍스트 혼합",
    note="출처 [2010년 4월 고3 이과 13번]. 79.6% ↔ z=1.27, 2배 길이 ↔ z=2.54 ↔ 2·0.4945=98.9% → ④ = 빠른정답 ✓.")

# p97
add(id="6988bd90", qtype="choice",
    question=("표준편차가 σ인 정규분포를 따르는 모집단에서 크기가 [[n]]인 표본을 임의추출하여 모평균을 추정하려고 한다. "
              "일정한 신뢰도로 모평균을 추정할 때, 다음 중 신뢰구간의 길이가 가장 긴 것은?"),
    choices=["[[n = 16]], σ = 4", "[[n = 16]], σ = 8", "[[n = 36]], σ = 4", "[[n = 36]], σ = 8", "[[n = 64]], σ = 12"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: σ(그리스 문자) 미지원으로 선지의 'σ = 4' 등을 텍스트로 표기",
    note="길이 ∝ σ/√n: 1, 2, 2/3, 4/3, 3/2 → ② = 빠른정답 ✓.")
