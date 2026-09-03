# -*- coding: utf-8 -*-
# esc_sonnet_h3-1_1of2 — 이미지 기준 전사 (83 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_5 = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ───────── 여러 가지 순열 ─────────
# p41
add(id="1151f2da", qtype="choice",
    question=("집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여 다음 조건을 모두 만족시키는 함수 [[f]]: [[X]]→[[X]]의 개수는?\n"
              "(가) [[f(4)]]의 값은 짝수이다.\n"
              "(나) [[x < 4]]이면 [[f(x) <= f(4)]]이다.\n"
              "(다) [[x > 4]]이면 [[f(x) >= f(4)]]이다."),
    choices=["140", "160", "180", "200", "220"], derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="f(4)=2: 2³·4=32, f(4)=4: 4³·2=128 → 160 → ② (전수 확인).")

# p44
add(id="70659100", qtype="short",
    question=("집합 [[X = set(2, 3, 5, 7, 11)]]과 함수 [[f]]: [[X]]→[[X]]에 대하여 함수 [[f]]의 치역을 [[A]], "
              "합성함수 [[comp(f, f)]]의 치역을 [[B]]라 할 때, 다음 조건을 만족시키는 함수 [[f]]의 개수를 구하시오.\n"
              "(가) [[card(B) = 2]]\n"
              "(나) 집합 [[A]]의 모든 원소의 곱은 집합 [[B]]의 모든 원소의 곱의 2배이다."),
    choices=None, derived_answer="180", figure=None, difficulty_est=5, confidence=0.85,
    note="출처 [2025년 10월 고3 확률과 통계 29번/4점]. 전수 확인 180. 빠른정답 2와 불일치(정렬 어긋남 추정).")

# p50
add(id="663b3b30", qtype="choice",
    question=("집합 [[X = set(2, 3, 4, 5, 6)]]에 대하여 다음 조건을 만족시키는 함수 [[f]]: [[X]]→[[X]]의 개수는?\n"
              "(가) [[f(2) f(4) f(6)]]은 홀수이다.\n"
              "(나) [[f(3) < f(5)]]\n"
              "(다) 함수 [[f]]의 치역의 원소의 개수는 3이다."),
    choices=["40", "42", "44", "46", "48"], derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2023년 6월 고3 확률과통계 28번 변형]. 전수 확인 48 → ⑤. 빠른정답 1과 불일치.")

# p51
add(id="735e269f", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 6, 12)]]과 함수 [[f]]: [[X]]→[[X]]에 대하여 함수 [[f]]의 치역을 [[A]], "
              "합성함수 [[comp(f, f)]]의 치역을 [[B]]라 할 때, 다음 조건을 만족시키는 함수 [[f]]의 개수를 구하시오.\n"
              "(가) [[card(B) = 3]]\n"
              "(나) 집합 [[A]]의 모든 원소의 곱은 집합 [[B]]의 모든 원소의 곱의 3배이다."),
    choices=None, derived_answer="2520", figure=None, difficulty_est=5, confidence=0.9,
    note="출처 [2025년 10월 고3 확률과 통계 29번 변형]. 전수 확인 2520 = 빠른정답 ✓.")

# p53
add(id="7c6f6d6b", qtype="short",
    question=("한 개의 주사위를 네 번 던져서 나오는 눈의 수를 차례로 [[a]], [[b]], [[c]], [[d]]라 하자. "
              "[[a b c d]]가 16의 배수가 되는 모든 순서쌍 ([[a]], [[b]], [[c]], [[d]])의 개수를 구하시오."),
    choices=None, derived_answer="363", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2025년 3월 고3 확률과 통계 29번/4점]. 전수 확인 363. 빠른정답 5와 불일치(정렬 어긋남 추정).")

# p59
add(id="cd1967ba", qtype="short",
    question="다음 문자를 일렬로 나열하는 경우의 수를 구하시오.\n[[a]], [[b]], [[b]], [[c]], [[c]], [[c]], [[c]]",
    choices=None, derived_answer="105", figure=None, difficulty_est=1, confidence=0.9,
    note="7!/(2!4!) = 105 = 빠른정답 ✓.")

# ───────── 사건의 독립과 종속 ─────────
# p1 (id 2개) — 9장 카드
dup(["5e84286b", "346f6bfa"], qtype="choice",
    question=("1부터 9까지의 자연수가 하나씩 적혀 있는 9장의 카드가 있다. 이 카드를 모두 한 번씩 사용하여 그림과 같은 9개의 자리에 "
              "각각 한 장씩 임의로 놓을 때, 9 이하의 자연수 [[k]]에 대하여 [[k]]번째 자리에 놓인 카드에 적힌 수가 [[k]] 이하인 사건을 "
              "[[sub(A,k)]]라 하자.\n"
              "다음은 두 자연수 [[m]], [[n]] ([[1 <= m < n <= 9]])에 대하여 두 사건 [[sub(A,m)]]과 [[sub(A,n)]]이 서로 독립이 되도록 하는 "
              "[[m]], [[n]]의 모든 순서쌍 ([[m]], [[n]])의 개수를 구하는 과정이다.\n"
              "[[sub(A,k)]]는 [[k]]번째 자리에 [[k]] 이하의 자연수 중 하나가 적힌 카드가 놓여 있고, [[k]]번째 자리를 제외한 8개의 자리에 "
              "나머지 8장의 카드가 놓여 있는 사건이므로 [[prob(sub(A,k))]] = (가) 이다.\n"
              "[[inter(sub(A,m), sub(A,n))]] ([[m < n]])은 [[m]]번째 자리에 [[m]] 이하의 자연수 중 하나가 적힌 카드가 놓여 있고, "
              "[[n]]번째 자리에 [[n]] 이하의 자연수 중 [[m]]번째 자리에 놓인 카드에 적힌 수가 아닌 자연수가 적힌 카드가 놓여 있고, "
              "[[m]]번째와 [[n]]번째 자리를 제외한 7개의 자리에 나머지 7장의 카드가 놓여 있는 사건이므로 "
              "[[prob(inter(sub(A,m), sub(A,n)))]] = (나) 이다.\n"
              "한편, 두 사건 [[sub(A,m)]]과 [[sub(A,n)]]이 서로 독립이기 위해서는 "
              "[[prob(inter(sub(A,m), sub(A,n))) = prob(sub(A,m)) prob(sub(A,n))]]을 만족시켜야 한다.\n"
              "따라서 두 사건 [[sub(A,m)]]과 [[sub(A,n)]]이 서로 독립이 되도록 하는 [[m]], [[n]]의 모든 순서쌍 ([[m]], [[n]])의 개수는 (다) 이다.\n"
              "위의 (가)에 알맞은 식에 [[k = 3]]을 대입한 값을 [[p]], (나)에 알맞은 식에 [[m = 6]], [[n = 7]]을 대입한 값을 [[q]], "
              "(다)에 알맞은 수를 [[r]]라 할 때, [[p q r]]의 값은?"),
    choices=["[[frac(1,3)]]", "[[frac(2,3)]]", "[[1]]", "[[frac(4,3)]]", "[[frac(5,3)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "빈 카드 자리 9개(직사각형)가 가로로 나열되고 각 자리 아래 화살표와 '1번째 자리'~'9번째 자리' 라벨"}}],
    difficulty_est=4, confidence=0.85,
    note="출처 [2019년 6월 고3 이과 17번 변형]. (가) k/9 → p=1/3, (나) m(n−1)/72 → q=1/2, (다) n=9, m=1~8 → r=8, pqr=4/3 → ④ = 빠른정답 ✓. 그림은 장식(자리 배치).")

# p3
add(id="5da8682f", qtype="short",
    question=("표본공간 [[S]] = {1, 2, 3, ⋯, 12}에서 모든 근원사건의 확률은 같고 [[A = set(1, 2, 3, 6)]]이다. "
              "사건 [[A]]와 독립이고 [[card(inter(A, X)) = 3]]인 사건 [[X]]의 개수를 구하시오.\n"
              "(단, [[A]]와 [[X]]는 [[S]]의 부분집합이고, [[card(A)]]는 집합 [[A]]의 원소의 개수이다.)"),
    choices=None, derived_answer="112", figure=None, difficulty_est=3, confidence=0.9,
    note="독립 조건 3/12 = (4/12)(n(X)/12) → n(X)=9, C(4,3)·C(8,6)=112 = 빠른정답 ✓.")

# p14
add(id="12b0e984", qtype="choice",
    question=("1부터 10까지의 자연수가 각각 하나씩 적힌 10장의 카드 중에서 임의로 한 장의 카드를 뽑을 때, [[n]]의 배수가 적힌 카드를 뽑는 사건을 "
              "[[sub(A,n)]]이라 하자. 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(A,3)]]과 [[sub(A,5)]]는 배반사건이다.\n"
              "ㄴ. [[cprob(sub(A,6), sub(A,3)) = frac(1,2)]]\n"
              "ㄷ. [[sub(A,2)]]와 [[sub(A,6)]]은 서로 독립이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="A₃={3,6,9}, A₅={5,10} 배반 ㄱ✓; P(A₆|A₃)=1/3 ㄴ✗; P(A₂∩A₆)=1/10 ≠ (1/2)(1/10) ㄷ✗ → ①. 빠른정답 5와 불일치.")

# p15 (id 2개) — 7장 카드
dup(["51b62c33", "b6a14ab0"], qtype="choice",
    question=("1부터 7까지의 자연수가 하나씩 적혀 있는 7장의 카드가 있다. 이 카드를 모두 한 번씩 사용하여 다음 그림과 같은 7개의 자리에 "
              "각각 한 장씩 임의로 놓을 때, 7 이하의 자연수 [[k]]에 대하여 [[k]]번째 자리에 놓인 카드에 적힌 수가 [[k]] 이하인 사건을 "
              "[[sub(A,k)]]라 하자.\n"
              "다음은 두 자연수 [[m]], [[n]] ([[1 <= m < n <= 7]])에 대하여 두 사건 [[sub(A,m)]]과 [[sub(A,n)]]이 서로 독립이 되도록 하는 "
              "[[m]], [[n]]의 모든 순서쌍 ([[m]], [[n]])의 개수를 구하는 과정이다.\n"
              "[[sub(A,k)]]는 [[k]]번째 자리에 [[k]] 이하의 자연수 중 하나가 적힌 카드가 놓여 있고, [[k]]번째 자리를 제외한 6개의 자리에 "
              "나머지 6장의 카드가 놓여 있는 사건이므로 [[prob(sub(A,k))]] = (가) 이다.\n"
              "[[inter(sub(A,m), sub(A,n))]] ([[m < n]])은 [[m]]번째 자리에 [[m]] 이하의 자연수 중 하나가 적힌 카드가 놓여 있고, "
              "[[n]]번째 자리에 [[n]] 이하의 자연수 중 [[m]]번째 자리에 놓인 카드에 적힌 수가 아닌 자연수가 적힌 카드가 놓여 있고, "
              "[[m]]번째와 [[n]]번째 자리를 제외한 5개의 자리에 나머지 5장의 카드가 놓여 있는 사건이므로 "
              "[[prob(inter(sub(A,m), sub(A,n)))]] = (나) 이다.\n"
              "한편, 두 사건 [[sub(A,m)]]과 [[sub(A,n)]]이 서로 독립이기 위해서는 "
              "[[prob(inter(sub(A,m), sub(A,n))) = prob(sub(A,m)) prob(sub(A,n))]]을 만족시켜야 한다.\n"
              "따라서 두 사건 [[sub(A,m)]]과 [[sub(A,n)]]이 서로 독립이 되도록 하는 [[m]], [[n]]의 모든 순서쌍 ([[m]], [[n]])의 개수는 (다) 이다.\n"
              "위의 (가)에서 알맞은 식에 [[k = 3]]을 대입한 값을 [[p]], (나)에 알맞은 식에 [[m = 3]], [[n = 7]]을 대입한 값을 [[q]], "
              "(다)에 알맞은 수를 [[r]]라 할 때, [[frac(p r, q)]]의 값은?"),
    choices=["[[frac(1,6)]]", "[[frac(1,3)]]", "[[1]]", "[[3]]", "[[6]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "빈 카드 자리 7개(직사각형)가 가로로 나열되고 각 자리 아래 화살표와 '1번째 자리'~'7번째 자리' 라벨"}}],
    difficulty_est=4, confidence=0.85,
    note="출처 [2019년 6월 고3 문과 19번 변형]. (가) k/7 → p=3/7, (나) m(n−1)/42 → q=3/7, (다) n=7, m=1~6 → r=6, pr/q=6 → ⑤. 빠른정답 36과 불일치(정렬 어긋남 추정).")

# p17
add(id="0c6f4c7e", qtype="short",
    question=("표본공간 [[S]]는 [[S]] = {1, 2, 3, ⋯, 12}이고 모든 근원사건의 확률은 같다. 사건 [[A]]가 [[A = set(4, 8, 12)]]일 때, "
              "사건 [[A]]와 독립이고 [[card(inter(A, X)) = 2]]인 사건 [[X]]의 개수를 구하시오.\n"
              "(단, [[card(B)]]는 집합 [[B]]의 원소의 개수를 나타낸다.)"),
    choices=None, derived_answer="252", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2004년 6월 고3 이과 확률과 통계 30번]. 2/12=(1/4)(n(X)/12) → n(X)=8, C(3,2)·C(9,6)=252 = 빠른정답 ✓.")

# p19
add(id="a55dd38c", qtype="choice",
    question=("표본공간 [[S]]의 임의의 두 사건 [[A]], [[B]]에 대하여 [[prob(A) != 0]], [[prob(B) != 0]]일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[prob(union(A, B)) = 1]]이면 [[prob(A) + prob(B) = 1]]이다.\n"
              "ㄴ. [[A]], [[B]]가 서로 독립이면 [[A]], [[B]]는 서로 배반이다.\n"
              "ㄷ. [[A]], [[B]]가 서로 배반이면 [[prob(A) + prob(B) <= 1]]이다.\n"
              "ㄹ. [[A]], [[B]]가 서로 독립이면 [[cprob(A, B) = cprob(B, A)]]이다."),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㄷ, ㄹ"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="ㄱ✗ ㄴ✗ ㄷ✓(배반이면 P(A)+P(B)=P(A∪B)≤1) ㄹ✗(P(A|B)=P(A), P(B|A)=P(B)로 일반적으로 다름) → ③. 빠른정답 4와 불일치.")

# p20
add(id="e96ad91f", qtype="short",
    question=("확률이 0이 아닌 두 사건 [[A]], [[B]]에 대하여 다음 보기 중 옳은 것만을 있는 대로 고르시오.\n<보기>\n"
              "ㄱ. [[subset(A, B)]]이면 [[cprob(B, A) < 1]]이다.\n"
              "ㄴ. [[A]], [[B]]가 서로 배반사건이면 [[cprob(B, A) = 0]]이다.\n"
              "ㄷ. [[A]], [[B]]가 서로 독립이면 [[cprob(comp(A), B) = cprob(A, comp(B))]]이다."),
    choices=None, derived_answer="ㄴ", figure=None, difficulty_est=2, confidence=0.85,
    note="ㄱ✗(A⊂B이면 P(B|A)=1) ㄴ✓ ㄷ✗(1−P(A) vs P(A)) → ㄴ. 빠른정답 252와 불일치(옆 문항 답 정렬 어긋남).")

# p23
add(id="c0414381", qtype="choice",
    question="[[prob(A) > 0]], [[prob(B) > 0]]인 두 사건 [[A]], [[B]]에 대하여 옳지 않은 것은?",
    choices=["[[A]]와 [[comp(A)]]은 서로 배반이다.",
             "[[A]]와 [[B]]가 서로 배반이면 [[cprob(comp(A), B) = 1]]이다.",
             "[[A]]와 [[B]]가 서로 독립이면 [[prob(inter(comp(A), B)) = prob(comp(A)) prob(B)]]이다.",
             "[[A]]와 [[B]]가 서로 독립이면 [[cprob(comp(A), comp(B)) = 1 - cprob(A, comp(B))]]이다.",
             "[[prob(A) cprob(B, A) = prob(B) cprob(A, B)]]이면 [[A]], [[B]]는 서로 독립이다."],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="⑤의 등식은 항상 성립(둘 다 P(A∩B))하므로 독립을 뜻하지 않음 → ⑤. 빠른정답 없음.")

# p26
add(id="c6c7167e", qtype="choice",
    question=("두 사건 [[A]], [[B]]가 서로 독립일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은? (단, [[comp(A)]]은 [[A]]의 여사건이다.)\n<보기>\n"
              "ㄱ. [[(1 - prob(A))(1 - prob(B)) = 1 - prob(union(A, B))]]\n"
              "ㄴ. [[cprob(comp(A), B) = 1 - prob(A)]]\n"
              "ㄷ. [[cprob(comp(A), comp(B)) = 1 - cprob(comp(A), B)]]"),
    choices=CH_5, derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    note="원문 ㄱ의 중괄호 {1−P(A)}{1−P(B)}는 소괄호로 표기. ㄱ✓ ㄴ✓ ㄷ✗(P(Aᶜ) vs P(A)) → ②. 빠른정답 5와 불일치.")

# p27
add(id="4637a12d", qtype="choice",
    question="두 사건 [[A]], [[B]]에 대하여 [[prob(A) = cprob(A, B)]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[prob(A) = cprob(A, comp(B))]]",
             "[[cprob(B, A) = cprob(B, comp(A))]]",
             "[[prob(union(A, B)) = prob(A) + prob(comp(A)) prob(comp(B))]]",
             "[[prob(inter(A, B)) = prob(A) cprob(B, A)]]",
             "[[prob(B) = prob(A) prob(B) + prob(comp(A)) prob(B)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="독립. P(A∪B)=P(A)+P(Aᶜ)P(B)이므로 ③이 틀림 = 빠른정답 ✓.")

# p31
add(id="2c202453", qtype="choice",
    question=("정보이론에서는 사건 [[E]]가 발생했을 때, 사건 [[E]]의 정보량 [[I(E)]]가 다음과 같이 정의된다고 한다.\n"
              "[[I(E) = -log(2, prob(E))]]\n"
              "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
              "(단, 사건 [[E]]가 일어날 확률 [[prob(E)]]는 양수이고, 정보량의 단위는 비트이다.)\n<보기>\n"
              "ㄱ. 한 개의 주사위를 던져 홀수의 눈이 나오는 사건을 [[E]]라 하면 [[I(E) = 1]]이다.\n"
              "ㄴ. 두 사건 [[A]], [[B]]가 서로 독립이고 [[prob(inter(A, B)) > 0]]이면 [[I(inter(A, B)) = I(A) + I(B)]]이다.\n"
              "ㄷ. [[prob(A) > 0]], [[prob(B) > 0]]인 두 사건 [[A]], [[B]]에 대하여 [[2 I(union(A, B)) <= I(A) + I(B)]]이다."),
    choices=CH_5, derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2008년 11월 고3 이과 17번]. ㄱ✓ ㄴ✓ ㄷ✓(P(A∪B)²≥P(A)P(B)) → ⑤ = 빠른정답 ✓.")

# p34
add(id="43e8247e", qtype="choice",
    question=("두 사건 [[A]], [[B]]가 서로 독립이고\n[[prob(A) = frac(1,3)]], [[prob(B) = frac(1,3)]]일 때, [[prob(inter(A, comp(B)))]]의 값은?\n"
              "(단, [[comp(B)]]은 [[B]]의 여사건이다.)"),
    choices=["[[frac(5,27)]]", "[[frac(2,9)]]", "[[frac(7,27)]]", "[[frac(8,27)]]", "[[frac(1,3)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2013년 11월 고3 문과 7번/3점]. (1/3)(2/3)=2/9 → ② = 빠른정답 ✓.")

# p35
add(id="2e8c4f53", qtype="choice",
    question=("서로 독립인 두 사건 [[A]], [[B]]에 대하여\n[[cprob(A, B) = cprob(B, A) = frac(3,4)]]\n이 성립할 때, [[prob(union(A, B))]]의 값은?"),
    choices=["[[frac(15,16)]]", "[[frac(13,16)]]", "[[frac(11,16)]]", "[[frac(9,16)]]", "[[frac(7,16)]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2008년 3월 고3 이과 4번]. P(A)=P(B)=3/4 → 3/4+3/4−9/16=15/16 → ① = 빠른정답 ✓.")

# p40
add(id="971c638e", qtype="choice",
    question=("세 사건 [[A]], [[B]], [[C]]가 다음 조건을 만족시킨다.\n"
              "(가) [[prob(A) = frac(1,2)]], [[prob(B) = frac(1,3)]], [[prob(C) = frac(1,12)]]\n"
              "(나) 두 사건 [[A]], [[B]]는 서로 독립이다.\n"
              "(다) 사건 [[union(A, B)]]와 사건 [[C]]는 서로 배반이다.\n"
              "이때, 확률 [[prob(union(union(A, B), C))]]의 값은?"),
    choices=["[[frac(7,12)]]", "[[frac(2,3)]]", "[[frac(3,4)]]", "[[frac(5,6)]]", "[[frac(11,12)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2009년 10월 고3 문과 7번]. P(A∪B)=2/3, +1/12=3/4 → ③ = 빠른정답 ✓.")

# p43
add(id="36711ac0", qtype="choice",
    question=("두 사건 [[A]]와 [[B]]가 서로 독립이고\n[[cprob(A, B) = prob(B)]], [[prob(inter(A, B)) = frac(1,4)]]일 때, [[prob(union(A, B))]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[frac(5,8)]]", "[[frac(3,4)]]", "[[frac(7,8)]]", "[[1]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="P(A)=P(B)=1/2 → 1/2+1/2−1/4=3/4 → ③ = 빠른정답 ✓.")

# p46
add(id="955fef60", qtype="choice",
    question=("두 사건 [[A]]와 [[B]]가 서로 독립이고 [[cprob(A, B) = frac(1,4)]],\n[[prob(inter(comp(A), B)) = frac(1,6)]]일 때, [[prob(comp(B))]]의 값은?\n"
              "(단, [[comp(B)]]은 [[B]]의 여사건이다.)"),
    choices=["[[frac(8,9)]]", "[[frac(7,9)]]", "[[frac(2,3)]]", "[[frac(5,9)]]", "[[frac(4,9)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 10월 고3 이과 4번 변형]. P(A)=1/4, (3/4)P(B)=1/6 → P(B)=2/9, P(Bᶜ)=7/9 → ② = 빠른정답 ✓.")

# ───────── 확률의 덧셈정리 ─────────
# p1
add(id="4ccda204", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여\n[[prob(comp(A)) = frac(2,3)]], [[prob(inter(comp(A), B)) = frac(1,4)]]\n"
              "일 때, [[prob(union(A, B))]]의 값은? (단, [[comp(A)]]은 [[A]]의 여사건이다.)"),
    choices=["[[frac(1,2)]]", "[[frac(7,12)]]", "[[frac(2,3)]]", "[[frac(3,4)]]", "[[frac(5,6)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2019년 11월 고3 문과 5번/3점]. P(A)+P(Aᶜ∩B)=1/3+1/4=7/12 → ② = 빠른정답 ✓.")

# p6
add(id="218d28a4", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여\n[[prob(inter(A, comp(B))) = prob(inter(comp(A), B)) = frac(1,6)]], [[prob(union(A, B)) = frac(2,3)]]\n"
              "일 때, [[prob(inter(A, B))]]의 값은? (단, [[comp(A)]]은 [[A]]의 여사건이다.)"),
    choices=["[[frac(1,12)]]", "[[frac(1,6)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(5,12)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2015년 9월 고3 문과 15번/4점]. 2/3−1/6−1/6=1/3 → ④ = 빠른정답 ✓.")

# p17
add(id="67674df7", qtype="choice",
    question=("두 사건 [[A]], [[B]]에 대하여\n[[prob(A) = frac(2,3)]], [[prob(inter(A, B)) = frac(1,4)]]일 때, [[prob(inter(A, comp(B)))]]의 값은? "
              "(단, [[comp(B)]]은 [[B]]의 여사건이다.)"),
    choices=["[[frac(1,3)]]", "[[frac(5,12)]]", "[[frac(1,2)]]", "[[frac(7,12)]]", "[[frac(2,3)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2018년 6월 고3 문과 12번/3점]. 2/3−1/4=5/12 → ② = 빠른정답 ✓.")

# p44
add(id="ebc3703a", qtype="choice",
    question=("표본공간 [[S]]는 [[S = set(1, 2, 3, 4, 5, 6, 7)]]이고 모든 근원사건의 확률은 같다. 표본공간 [[S]]의 두 사건 [[A]], [[B]]가 "
              "서로 배반사건이고 [[0 < prob(B) < prob(A)]]가 되도록 두 사건 [[A]], [[B]]를 선택하는 경우의 수는?"),
    choices=["680", "710", "740", "770", "800"], derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="서로소 순서쌍(둘 다 공집합 아님) 1932개 중 크기 같은 392개 제외 후 절반 → 770 → ④ (전수 확인). 빠른정답 5와 불일치.")

# p48
add(id="61be617a", qtype="choice",
    question=("1부터 8까지의 자연수가 하나씩 적혀 있는 8개의 공이 들어 있는 주머니에서 임의로 한 개의 공을 꺼내어 꺼낸 공에 적혀 있는 수를 확인하고 "
              "다시 넣는 시행을 3번 실시한다. 꺼낸 공에 적혀 있는 수를 차례로 [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]]이라 할 때, 두 집합\n"
              "[[A = setb(x, pow(x,2) - (sub(a,1) × sub(a,2) × sub(a,3)) x + 20 = 0)]],\n"
              "[[B]] = { [[x]] | [[x]]는 10의 양의 약수 }\n"
              "에 대하여 [[inter(A, B) != empty]]일 확률은?"),
    choices=["[[frac(21,512)]]", "[[frac(3,64)]]", "[[frac(27,512)]]", "[[frac(15,256)]]", "[[frac(33,512)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.9,
    note="a₁a₂a₃ ∈ {21, 12, 9} → 6+15+3=24가지, 24/512=3/64 → ② = 빠른정답 ✓.")

# p51
add(id="758e0304", qtype="short",
    question="서로 배반사건인 두 사건 [[A]], [[B]]에 대하여 [[prob(B) = frac(1,3)]],\n[[prob(union(A, B)) = frac(3,4)]]일 때, [[prob(A)]]를 구하시오.",
    choices=None, derived_answer="frac(5,12)", figure=None, difficulty_est=1, confidence=0.9,
    note="3/4−1/3=5/12 = 빠른정답 ✓.")

# p56
add(id="153dc1d5", qtype="choice",
    question="두 사건 [[A]], [[B]]는 서로 배반사건이고\n[[prob(union(A, B)) = frac(7,8)]], [[prob(A) = frac(1,5)]]일 때, [[prob(B)]]의 값은?",
    choices=["[[frac(51,80)]]", "[[frac(13,20)]]", "[[frac(53,80)]]", "[[frac(27,40)]]", "[[frac(11,16)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2025년 7월 고3 확률과 통계 24번 변형]. 7/8−1/5=27/40 → ④ = 빠른정답 ✓.")

# p85
add(id="3166fe0b", qtype="choice",
    question=("1부터 8까지의 자연수가 하나씩 적혀 있는 8장의 카드가 들어 있는 주머니가 있다. 이 주머니에서 임의로 두 장의 카드를 동시에 꺼내어 "
              "적혀 있는 수를 확인한 후 다시 넣는 시행을 두 번 반복한다. 첫 번째 시행에서 확인한 두 수 중 작은 수를 [[sub(a,1)]], 큰 수를 [[sub(a,2)]]라 하고, "
              "두 번째 시행에서 확인한 두 수 중 작은 수를 [[sub(b,1)]], 큰 수를 [[sub(b,2)]]라 하자. 두 집합 [[A]], [[B]]를\n"
              "[[A = setb(x, sub(a,1) <= x <= 2 sub(a,2))]], [[B = setb(x, sub(b,1) <= x <= 2 sub(b,2))]]라 할 때, [[inter(A, B) != empty]]일 확률은?"),
    choices=["[[frac(48,49)]]", "[[frac(46,49)]]", "[[frac(44,49)]]", "[[frac(6,7)]]", "[[frac(40,49)]]"],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2020년 9월 고3 문과 19번 변형]. 서로소인 경우 2·8/784=1/49 → 48/49 → ① = 빠른정답 ✓.")

# p91
add(id="072b6b0d", qtype="choice",
    question=("1부터 6까지의 자연수가 하나씩 적혀 있는 6장의 카드가 들어 있는 주머니가 있다. 이 주머니에서 임의로 두 장의 카드를 동시에 꺼내어 "
              "적혀 있는 수를 확인한 후 다시 넣는 시행을 두 번 반복한다. 첫 번째 시행에서 확인한 두 수 중 작은 수를 [[sub(a,1)]], 큰 수를 [[sub(a,2)]]라 하고, "
              "두 번째 시행에서 확인한 두 수 중 작은 수를 [[sub(b,1)]], 큰 수를 [[sub(b,2)]]라 하자. 두 집합 [[A]], [[B]]를\n"
              "[[A = setb(x, sub(a,1) <= x <= sub(a,2))]], [[B = setb(x, sub(b,1) <= x <= sub(b,2))]]라 할 때, [[inter(A, B) != empty]]일 확률은?"),
    choices=["[[frac(3,5)]]", "[[frac(2,3)]]", "[[frac(11,15)]]", "[[frac(4,5)]]", "[[frac(13,15)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "주머니 안에 1~6이 적힌 카드 6장이 들어 있는 삽화(장식)"}}],
    difficulty_est=3, confidence=0.85,
    note="출처 [2020년 9월 고3 문과 19번/4점]. 서로소인 경우 2·C(6,4)/225=2/15 → 13/15 → ⑤ = 빠른정답 ✓. 그림은 장식.")

# ───────── 모비율의 추정 ─────────
# p49
add(id="dfb31e08", qtype="short",
    question=("어느 모집단에서 표본을 임의추출하여 구한 모비율 [[p]]의 신뢰도 99%의 신뢰구간이 [[0.5484 <= p <= 0.6516]]일 때, "
              "이 표본의 표본비율 p̂의 값을 구하시오.\n(단, [[prob(abs(Z) <= 2.58) = 0.99]])"),
    choices=None, derived_answer="0.6", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 표본비율 p̂(hat) 표기 → 텍스트 혼합",
    note="신뢰구간의 중점 (0.5484+0.6516)/2=0.6. 빠른정답 1과 불일치(정렬 어긋남 추정).")

# p68
add(id="4864355c", qtype="short",
    question=("우리나라 성인을 대상으로 특정 질병에 대한 항체 보유 비율을 조사하려고 한다. 모집단의 항체 보유 비율을 [[p]], "
              "모집단에서 임의로 추출한 [[n]]명을 대상으로 조사한 표본의 항체 보유 비율을 p̂이라고 할 때,\n"
              "| p̂ − [[p]] | ≤ 0.16 √( p̂(1 − p̂) ) 일 확률이 0.9544 이상이 되도록 하는 [[n]]의 최솟값을 구하시오.\n"
              "(단, [[Z]]가 표준정규분포가 따르는 확률변수일 때, [[prob(0 <= Z <= 2) = 0.4772]]이다.)"),
    choices=None, derived_answer="157", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 표본비율 p̂(hat) 표기 → 부등식 |p̂−p| ≤ 0.16√(p̂(1−p̂))을 텍스트 혼합으로 표기",
    note="출처 [2010년 11월 고3 이과 확률과 통계 30번]. 2√(p̂(1−p̂)/n) ≤ 0.16√(p̂(1−p̂)) → √n ≥ 12.5 → n ≥ 156.25 → 157. 빠른정답 1과 불일치. 원문 '표준정규분포가 따르는' 그대로.")

# ───────── 중복조합 ─────────
# p8
add(id="b10ef05f", qtype="short",
    question=("다음 조건을 만족시키는 음이 아닌 정수 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]]의 모든 순서쌍 "
              "([[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]])의 개수를 구하시오.\n"
              "(가) [[n]] = 1, 2, 3일 때, [[sub(x, n+1) - sub(x, n) >= 3]]\n"
              "(나) [[sub(x,4) <= 16]]"),
    choices=None, derived_answer="330", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2019년 6월 고3 문과 29번 변형]. x₄=x₁+9+y₂+y₃+y₄ ≤ 16 → y₁+…+y₄ ≤ 7 → ₅H₇=330 (전수 확인). 빠른정답 없음.")

# p14
add(id="64c11e44", qtype="choice",
    question=("세 정수 [[a]], [[b]], [[c]]에 대하여 [[2 <= abs(a) <= abs(b) <= abs(c) <= 7]]을 만족시키는 모든 순서쌍 ([[a]], [[b]], [[c]])의 개수는?"),
    choices=["448", "440", "432", "424", "416"], derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2015년 11월 고3 이과 14번 변형]. ₆H₃=56, 부호 2³ → 448 → ①. 빠른정답 3과 불일치.")

# p54
add(id="7e798cde", qtype="short",
    question=("방정식 [[x + y + z + 3w = 10]]을 만족시키는 자연수 [[x]], [[y]], [[z]], [[w]]의 순서쌍 ([[x]], [[y]], [[z]], [[w]])의 개수를 구하시오."),
    choices=None, derived_answer="18", figure=None, difficulty_est=2, confidence=0.85,
    note="w=1: C(6,2)=15, w=2: C(3,2)=3 → 18. 빠른정답 330과 불일치(옆 문항 p8 답, 정렬 어긋남).")

# p68 (id 2개)
dup(["24b547bd", "fd9fb36e"], qtype="short",
    question=("집합 [[X = set(-2, -1, 0, 1, 2, 3)]]에 대하여 다음 조건을 만족시키는 함수 [[f]]: [[X]]→[[X]]의 개수를 구하시오.\n"
              "(가) [[X]]의 모든 원소 [[x]]에 대하여 [[in(x + f(x), X)]]\n"
              "(나) [[x]] = −1, 0, 1일 때 [[f(x) <= f(x + 1)]]"),
    choices=None, derived_answer="180", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2024년 6월 고3 확률과 통계 30번 변형]. 전수 확인 180. 빠른정답 4와 불일치(정렬 어긋남 추정).")

# p70
add(id="5683b023", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4)]]에서 집합 [[Y = set(4, 5, 6, 7)]]로의 함수 [[f]]: [[X]]→[[Y]] 중에서 [[f(2) <= f(4)]]를 만족시키는 "
              "[[f]]의 개수를 구하시오."),
    choices=None, derived_answer="160", figure=None, difficulty_est=2, confidence=0.85,
    note="₄H₂=10, f(1), f(3) 각 4가지 → 160. 빠른정답 5와 불일치.")

# p73
add(id="531aac0c", qtype="choice",
    question=("집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여 다음 조건을 만족시키는 함수 [[f]]: [[X]]→[[X]]의 개수는?\n"
              "(가) [[x]] = 1, 2, 3, 4일 때 [[f(x) <= f(x + 1)]]이다.\n"
              "(나) [[x]]가 소수가 아니면 ([[comp(f, f)]])([[x]]) = [[x]]이다."),
    choices=["12", "14", "16", "18", "20"], derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="합성함수 적용 표기 (f∘f)(x) = x를 텍스트 혼합으로 표기",
    note="출처 [2025년 3월 고3 확률과 통계 27번 변형]. f(1)=1, f(4)=4 강제 → f(2)≤f(3)∈[1,4] 10가지 × f(5)∈{4,5} 2가지 = 20 → ⑤ = 빠른정답 ✓.")

# p76
add(id="f1bce155", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6)]]에 대하여 함수 [[f]]: [[X]]→[[X]] 중에서 다음 조건을 만족시키는 함수 [[f]]의 개수를 구하시오.\n"
              "(가) [[f(3) × f(6)]]은 3의 배수이다.\n"
              "(나) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) < sub(x,2)]]이면 [[f(sub(x,1)) <= f(sub(x,2))]]이다."),
    choices=None, derived_answer="327", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2020년 7월 고3 이과 28번/4점]. 원문 f(3)·f(6)의 가운뎃점은 ×로 표기. 전수 확인 327(비감소 462 − 3의 배수 아닌 135). 빠른정답 5와 불일치.")

# p77
add(id="644df093", qtype="choice",
    question=("집합 [[X = set(1, 2, 3, 4)]]에 대하여 다음 조건을 만족시키는 함수 [[f]]: [[X]]→[[X]]의 개수는?\n"
              "[[f(2) <= f(3) <= f(4)]]"),
    choices=["64", "68", "72", "76", "80"], derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    note="출처 [2020년 11월 고3 문과 13번/3점]. ₄H₃=20, f(1) 4가지 → 80 → ⑤. 빠른정답 150과 불일치.")

# p80
add(id="09c45015", qtype="short",
    question=("집합 [[X = set(2, 3, 5, 7, 11)]]에 대하여 다음 조건을 만족시키는 함수 [[f]]: [[X]]→[[X]]의 개수를 구하시오.\n"
              "(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) < sub(x,2)]]이면 [[f(sub(x,1)) <= f(sub(x,2))]]이다.\n"
              "(나) [[f(5) != 5]]이고, [[f(3) × f(7) < 49]]이다."),
    choices=None, derived_answer="63", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2023년 3월 고3 확률과 통계 30번 변형]. 원문 f(3)·f(7)의 가운뎃점은 ×로 표기. 전수 확인 63. 빠른정답 5와 불일치.")

# p81
add(id="11feedee", qtype="short",
    question=("두 집합\n[[X = set(1, 3, 5, 7)]], [[Y]] = { [[y]] | [[y]]는 8 이하의 자연수 }\n"
              "에 대하여 다음 조건을 모두 만족시키는 함수 [[f]]: [[X]]→[[Y]]의 개수를 구하시오.\n"
              "(가) [[in(sub(x,1), X)]], [[in(sub(x,2), X)]]일 때, [[sub(x,1) < sub(x,2)]]이면 [[f(sub(x,1)) <= f(sub(x,2))]]\n"
              "(나) [[f(5) = 5]]"),
    choices=None, derived_answer="60", figure=None, difficulty_est=3, confidence=0.9,
    note="f(1)≤f(3)≤5: ₅H₂=15, f(7)∈{5,…,8}: 4 → 60 = 빠른정답 ✓.")

# p82
add(id="0e460de1", qtype="short",
    question=("두 집합 [[X = set(1, 2, 3, 4, 5)]], [[Y = set(-1, 0, 1, 2, 3)]]에 대하여 다음 조건을 만족시키는 함수 [[f]]: [[X]]→[[Y]]의 개수를 구하시오.\n"
              "(가) [[f(1) <= f(2) <= f(3) <= f(4) <= f(5)]]\n"
              "(나) [[f(a) + f(b) = 0]]을 만족시키는 집합 [[X]]의 서로 다른 두 원소 [[a]], [[b]]가 존재한다."),
    choices=None, derived_answer="65", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2022년 3월 고3 확률과통계 29번/4점]. 전수 확인 65. 빠른정답 523과 불일치(정렬 어긋남 추정).")

# p86
add(id="3bb3fa41", qtype="short",
    question=("집합 [[A = set(1, 2, 3, 4, 5, 6, 7)]]에 대하여 다음 세 조건을 모두 만족하는 함수 [[f]]: [[A]]→[[A]]의 개수를 구하시오.\n"
              "(가) 함수 [[f]]는 일대일 대응\n"
              "(나) [[f(1) = 7]]\n"
              "(다) [[k >= 2]]이면 [[f(k) <= k]]"),
    choices=None, derived_answer="32", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2004년 9월 고3 이과 25번]. f(2)~f(6) 각 2가지, f(7) 1가지 → 2⁵=32. 빠른정답 3589와 불일치(정렬 어긋남).")

# p95
add(id="ec3661fd", qtype="short",
    question=("두 집합 [[X = set(0, 2, 4)]], [[Y = set(1, 3, 5, 7, 9)]]에 대하여 [[in(a, X)]], [[in(b, X)]]일 때, 다음을 만족시키는 함수 "
              "[[f]]: [[X]]→[[Y]]의 개수를 구하시오.\n[[a < b]]이면 [[f(a) < f(b)]]"),
    choices=None, derived_answer="10", figure=None, difficulty_est=2, confidence=0.85,
    note="증가함수 → ₅C₃=10. 빠른정답 120과 불일치.")

# p99
add(id="7ba26fa0", qtype="choice",
    question=("다음은 집합 [[X = set(1, 2, 3, 4, 5)]]와 함수 [[f]]: [[X]]→[[X]]에 대하여 합성함수 [[comp(f, f)]]의 치역의 원소의 개수가 4인 "
              "함수 [[f]]의 개수를 구하는 과정이다.\n"
              "함수 [[f]]와 함수 [[comp(f, f)]]의 치역을 각각 [[A]]와 [[B]]라 하자. [[card(A) = 5]]이면 함수 [[f]]는 일대일대응이고, "
              "함수 [[comp(f, f)]]도 일대일대응이므로 [[card(B) = 5]]이다.\n"
              "또, [[card(A) <= 3]]이면 [[subset(B, A)]]이므로 [[card(B) <= 3]]이다.\n"
              "따라서 [[card(A) = 4]], 즉 [[B = A]]인 경우만 생각하면 된다.\n"
              "(i) [[card(A) = 4]]인 [[X]]의 부분집합 [[A]]를 선택하는 경우의 수는 (가) 이다.\n"
              "(ii) (i)에서 선택한 집합 [[A]]에 대하여 [[X]]의 원소 중 [[A]]에 속하지 않는 원소를 [[k]]라 하자. "
              "[[card(A) = 4]]이므로 집합 [[A]]에서 [[f(k)]]를 선택하는 경우의 수는 (나) 이다.\n"
              "(iii) (i)에서 선택한 [[A = set(sub(a,1), sub(a,2), sub(a,3), sub(a,4))]]와 (ii)에서 선택한 [[f(k)]]에 대하여 "
              "[[in(f(k), A)]]이며 [[A = B]]이므로\n"
              "[[A = set(f(sub(a,1)), f(sub(a,2)), f(sub(a,3)), f(sub(a,4)))]] ⋯ ㉠\n"
              "㉠을 만족시키는 경우의 수는 집합 [[A]]에서 집합 [[A]]로의 일대일대응의 개수와 같으므로 (다) 이다.\n"
              "따라서 (i), (ii), (iii)에 의하여 구하는 함수 [[f]]의 개수는 (가) × (나) × (다) 이다.\n"
              "위의 (가), (나), (다)에 알맞은 수를 각각 [[p]], [[q]], [[r]]라 할 때, [[p + q + r]]의 값은?"),
    choices=["32", "33", "34", "35", "36"], derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2018년 11월 고3 문과 19번 변형]. (가) ₅C₄=5, (나) 4, (다) 4!=24 → 33 → ②. 빠른정답 128과 불일치.")

# ───────── 이항분포 ─────────
# p1
add(id="4346f700", qtype="short",
    question=("확률변수 [[X]]의 확률질량함수가\n"
              "[[prob(X = r) = comb(80, r) pow(frac(1,4), r) pow(frac(3,4), 80 - r)]] ([[r]] = 0, 1, 2, ⋯, 80)\n"
              "일 때, [[X]]는 이항분포 [[binomd(n, p)]]를 따른다고 한다. [[n p]]의 값을 구하시오."),
    choices=None, derived_answer="20", figure=None, difficulty_est=1, confidence=0.9,
    note="B(80, 1/4) → np=20. 빠른정답 없음.")

# p2
add(id="e9f92cf8", qtype="short",
    question=("확률변수 [[X]]의 확률질량함수가\n"
              "[[prob(X = x) = comb(n, x) pow(p, x) pow(1 - p, n - x)]] ([[x]] = 0, 1, 2, ⋯, [[n]])\n"
              "일 때, [[X]]는 이항분포 [[binomd(49, frac(2,5))]]를 따른다고 한다.\n[[n + 5p]]의 값을 구하시오."),
    choices=None, derived_answer="51", figure=None, difficulty_est=1, confidence=0.9,
    note="n=49, p=2/5 → 49+2=51. 빠른정답 없음.")

# p5
add(id="cb9118b3", qtype="choice",
    question=("한 개의 주사위를 5번 던지는 시행에서 3 이상의 눈이 나오는 횟수를 확률변수 [[X]]라 할 때, [[X]]의 확률질량함수는\n"
              "[[prob(X = r) = comb(5, r) pow(a, r) pow(b, 5 - r)]] ([[r]] = 0, 1, 2, 3, 4, 5)이다.\n"
              "두 상수 [[a]], [[b]]의 값을 순서대로 적은 것은?"),
    choices=["[[frac(1,6)]], [[frac(5,6)]]", "[[frac(1,3)]], [[frac(2,3)]]", "[[frac(1,2)]], [[frac(1,2)]]",
             "[[frac(2,3)]], [[frac(1,3)]]", "[[frac(5,6)]], [[frac(1,6)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="P(3 이상)=2/3 → a=2/3, b=1/3 → ④. 빠른정답 없음.")

# p11
add(id="109a0f08", qtype="choice",
    question=("확률변수 [[X]]의 확률질량함수가\n"
              "[[prob(X = x) = comb(60, x) frac(pow(1, x) × pow(5, 60 - x), pow(6, 60))]] ([[x]] = 0, 1, 2, ⋯, 60)\n"
              "일 때, [[X]]는 이항분포 [[binomd(n, p)]]를 따른다고 한다.\n[[n + 18p]]의 값은?"),
    choices=["60", "61", "62", "63", "64"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="원문 1ˣ·5⁶⁰⁻ˣ의 가운뎃점은 ×로 표기. B(60, 1/6) → 60+3=63 → ④ = 빠른정답 ✓.")

# p23
add(id="81a205dc", qtype="choice",
    question=("확률변수 [[X]]는 이항분포 [[binomd(3, p)]]를 따르고,\n확률변수 [[Y]]는 이항분포 [[binomd(4, 2p)]]를 따른다고 할 때,\n"
              "[[15 prob(X = 3) = prob(Y >= 3)]]을 만족시키는 양수 [[p]]의 값은 [[frac(n, m)]]이다. [[m + n]]의 값은?\n"
              "(단, [[m]], [[n]]은 서로소인 자연수이다.)"),
    choices=["55", "60", "65", "70", "75"], derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="15p³ = 32p³−48p⁴ → p=17/48 → 65 → ③ = 빠른정답 ✓.")

# p48
add(id="ff432543", qtype="short",
    question=("이항분포 [[binomd(n, p)]]를 따르는 확률변수 [[X]]의 분산은 2이고,\n[[prob(X = n - 1) = 18 prob(X = n)]]이 성립한다.\n"
              "확률변수 [[X]]의 평균을 [[m]], 표준편차를 σ라 할 때,\n"
              "P( | [[X - m]] | < [[frac(sqrt(2), 2)]] σ ) = [[frac(k, pow(3, 8))]]이다. [[k]]의 값을 구하시오."),
    choices=None, derived_answer="1792", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="문법 범위 밖: 그리스 문자 σ(표준편차) → P(|X−m| < (√2/2)σ)를 텍스트 혼합으로 표기",
    note="n(1−p)=18p, np(1−p)=2 → p=1/3, n=9, m=3, σ=√2 → P(X=3)=₉C₃(1/3)³(2/3)⁶=1792/3⁸ → k=1792. 빠른정답 6과 불일치.")

# ───────── 이산확률변수의 기댓값과 표준편차 ─────────
# p21
add(id="fcebebfa", qtype="choice",
    question=("이산확률변수 [[X]]가 가지는 값이 1부터 5까지의 정수이고\n[[prob(X = k) = prob(X = k + 2)]] ([[k]] = 1, 2, 3)\n"
              "이다. [[ev(pow(X, 2)) = frac(21, 2)]]일 때, [[prob(X = 1)]]의 값은?"),
    choices=["[[frac(1,20)]]", "[[frac(1,10)]]", "[[frac(3,20)]]", "[[frac(1,5)]]", "[[frac(1,4)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="P(1)=P(3)=P(5)=a, P(2)=P(4)=b, 3a+2b=1, 35a+20b=21/2 → a=1/10 → ②. 빠른정답 5와 불일치.")

# p24
add(id="416ba62c", qtype="choice",
    question=("그림과 같이 중심이 O, 반지름의 길이가 1이고 중심각의 크기가 [[frac(pi, 2)]]인 부채꼴 OAB가 있다.\n"
              "자연수 [[n]]에 대하여 호 AB를 [[2n]]등분한 각 분점(양 끝점도 포함)을 차례로\n"
              "[[sub(P,0)]](= A), [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, 2n - 1)]], [[sub(P, 2n)]](= B)라 하자.\n"
              "다음 물음에 답하시오.\n"
              "[[n = 3]]일 때, 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], [[sub(P,4)]], [[sub(P,5)]] 중에서 임의로 선택한 한 개의 점을 P라 하자. "
              "부채꼴 OPA의 넓이와 부채꼴 OPB의 넓이의 차를 확률변수 [[X]]라 할 때, [[ev(X)]]의 값은?"),
    choices=["[[frac(pi, 11)]]", "[[frac(pi, 10)]]", "[[frac(pi, 9)]]", "[[frac(pi, 8)]]", "[[frac(pi, 7)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "사분원 부채꼴 OAB(반지름 1): 호 AB를 2n등분한 분점 P₀(=A), P₁, …, Pₙ₋₂, Pₙ₋₁, Pₙ, Pₙ₊₁, Pₙ₊₂, …, P₂ₙ₋₁, P₂ₙ(=B)과 O를 잇는 반지름들이 그려짐"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 부채꼴의 호를 2n등분한 분점과 반지름을 그린 도형",
    note="출처 [2014년 9월 고3 이과 14번/4점]. 넓이 차 |k−3|π/12 (k=1~5) 평균 (6/5)(π/12)=π/10 → ② = 빠른정답 ✓.")

# p26
add(id="ed9bf9ec", qtype="choice",
    question=("다음 그림과 같이 중심이 O, 반지름의 길이가 2, 중심각의 크기가 [[deg(180)]]인 부채꼴 OAB가 있다. 자연수 [[n]]에 대하여 호 AB를 "
              "[[2n]] 등분한 각 분점(양 끝 점도 포함)을 차례로 [[sub(P,0)]](= A), [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, 2n - 1)]], [[sub(P, 2n)]](= B)라 하자.\n"
              "[[n = 4]]일 때, 점 [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P,7)]] 중에서 임의로 선택한 한 개의 점을 P라 하자. "
              "부채꼴 OPA의 넓이와 부채꼴 OPB의 넓이의 곱을 확률변수 [[X]]라 할 때, [[ev(X)]]의 값은?"),
    choices=["[[frac(pow(pi, 2), 4)]]", "[[frac(pow(pi, 2), 2)]]", "[[frac(3 pow(pi, 2), 4)]]", "[[pow(pi, 2)]]", "[[frac(5 pow(pi, 2), 4)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "반원 부채꼴 OAB(반지름 2): 호 AB를 2n등분한 분점 P₀(=A), P₁, …, Pₙ₋₂, Pₙ₋₁, Pₙ, Pₙ₊₁, Pₙ₊₂, …, P₂ₙ₋₁, P₂ₙ(=B)과 O를 잇는 반지름들이 그려짐"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 반원의 호를 2n등분한 분점과 반지름을 그린 도형",
    note="넓이 곱 k(8−k)π²/16 (k=1~7) 평균 (84/7)(π²/16)=3π²/4 → ③. 빠른정답 1과 불일치.")

# p70
add(id="d7b25562", qtype="choice",
    question=("2005학년도 대학수학능력시험 수리영역의 원점수 [[X]]의 평균을 [[m]], 표준편차를 σ라 할 때 표준점수 [[T]]는\n"
              "[[T]] = [[a]] × ( ([[X - m]]) / σ ) + [[b]] (단, [[a > 0]])\n"
              "꼴로 나타내어진다. 수리영역의 표준점수 [[T]]가 평균이 100, 표준편차가 20인 분포를 이룬다고 할 때, 두 상수 [[a]], [[b]]의 합 [[a + b]]의 값은?"),
    choices=["80", "90", "100", "110", "120"], derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 그리스 문자 σ → T = a((X−m)/σ) + b를 텍스트 혼합으로 표기",
    note="출처 [2004년 3월 고3 이과 14번]. E(T)=b=100, σ(T)=a=20 → 120 → ⑤. 빠른정답 11과 불일치(정렬 어긋남).")

# p75
add(id="241addef", qtype="choice",
    question=("이산확률변수 [[X]]의 확률질량함수가\n[[prob(X = x) = frac(abs(x - 3), 6)]] ([[x]] = 1, 2, 3, 4, 5)\n일 때, [[ev(8X + 1)]]의 값은?"),
    choices=["24", "25", "26", "27", "28"], derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    note="E(X)=(2+2+0+4+10)/6=3 → 25 → ②. 빠른정답 105와 불일치.")

# p80
add(id="b05684dc", qtype="choice",
    question=("어느 과목의 시험점수 [[X]]의 평균이 [[m]]점이고 표준편차가 σ점일 때, 새로운 확률변수 [[T]]를\n"
              "[[T]] = [[a]] · ([[X - m]]) / σ + [[b]]로 정하였다. [[T]]의 평균이 80점, 표준편차가 10점이 되도록 하는 두 상수 [[a]], [[b]]에 대하여 "
              "[[a + b]]의 값은? (단, [[a > 0]])"),
    choices=["80", "90", "100", "110", "120"], derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 그리스 문자 σ → T = a·(X−m)/σ + b를 텍스트 혼합으로 표기",
    note="a=10, b=80 → 90 → ②. 빠른정답 16과 불일치(정렬 어긋남).")

# ───────── 정규분포 ─────────
# p1
add(id="86645a45", qtype="choice",
    question=("2학년 재학생 수가 동일한 두 고등학교 A, B의 2학년 학생의 수학 성적 분포가 각각 정규분포를 이루고 그 정규분포곡선이 다음 그림과 같다. "
              "두 고등학교 A, B의 수학 성적의 평균을 각각 [[sub(m,1)]], [[sub(m,2)]], 표준편차를 각각 σ₁, σ₂라 할 때, 다음 중 옳은 것은?"),
    choices=["[[sub(m,1) < sub(m,2)]], σ₁ < σ₂", "[[sub(m,1) < sub(m,2)]], σ₁ > σ₂", "[[sub(m,1) < sub(m,2)]], σ₁ = σ₂",
             "[[sub(m,1) > sub(m,2)]], σ₁ < σ₂", "[[sub(m,1) > sub(m,2)]], σ₁ > σ₂"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 두 정규분포곡선: A(초록)는 오른쪽에 있고 높고 좁음, B(주황)는 왼쪽에 있고 낮고 넓음"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 정규분포곡선 그래프 / 문법 범위 밖: 그리스 문자 σ₁, σ₂ 텍스트 혼합",
    note="A가 오른쪽·뾰족 → m₁>m₂, σ₁<σ₂ → ④ = 빠른정답 ✓.")

# p3
add(id="4c30c7df", qtype="choice",
    question=("정규분포 N(14, σ²)을 따르는 확률변수 [[X]]에 대하여 함수 [[f(k)]]를 [[f(k) = prob(k <= X <= k + 6)]]이라 할 때, "
              "다음 보기 중 옳은 것을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(5) = f(17)]]\n"
              "ㄴ. 함수 [[f(k)]]는 [[k = 14]]일 때, 최댓값을 갖는다.\n"
              "ㄷ. 임의의 실수 [[a]]에 대하여 [[f(a) = f(22 - a)]]이다."),
    choices=CH_5, derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 그리스 문자 σ → 정규분포 N(14, σ²)을 텍스트로 표기",
    note="평균 14 대칭: ㄱ✓(5↔23, 11↔17), ㄴ✗(k=11에서 최대), ㄷ✓ → ③ = 빠른정답 ✓.")

# p4
add(id="2845703b", qtype="choice",
    question=("다음 세 곡선 A, B, C는 각각 정규분포를 따르는 확률분포의 정규분포곡선이다. 세 확률분포의 평균을 각각 [[sub(m,A)]], [[sub(m,B)]], [[sub(m,C)]], "
              "분산을 각각 σ_A², σ_B², σ_C²이라 할 때, 다음 중 옳은 것은? (단, 곡선 A는 함수 [[y = f(x)]]의 그래프이고, 곡선 B는 함수 [[y = f(x - k)]]의 그래프이다.)"),
    choices=["[[sub(m,A) = sub(m,B) > sub(m,C)]], σ_B² > σ_A² = σ_C²",
             "[[sub(m,B) = sub(m,C) > sub(m,A)]], σ_C² > σ_A² = σ_B²",
             "[[sub(m,B) > sub(m,A) = sub(m,C)]], σ_A² = σ_B² > σ_C²",
             "[[sub(m,C) > sub(m,A) = sub(m,B)]], σ_A² = σ_C² > σ_B²",
             "[[sub(m,C) > sub(m,A) = sub(m,B)]], σ_B² > σ_A² = σ_C²"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 세 정규분포곡선: A(빨강, 왼쪽, 높고 좁음, 꼭대기 아래 점선), B(청록, 오른쪽, A와 같은 모양, 꼭대기 아래 점선), C(노랑, B와 같은 중심, 낮고 넓음)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정규분포곡선 3개 그래프 / 문법 범위 밖: σ_A², σ_B², σ_C² 텍스트 혼합",
    note="B=f(x−k) 평행이동 → σ_A=σ_B, C는 B와 중심 같고 넓음 → m_B=m_C>m_A, σ_C²>σ_A²=σ_B² → ②. 빠른정답 4와 불일치.")

# p5
add(id="992d8e58", qtype="choice",
    question=("다음 그림은 A반과 B반의 수학 성적을 나타내는 정규분포의 확률밀도함수의 그래프이다. A반과 B반의 성적의 평균을 각각 [[sub(m,1)]], [[sub(m,2)]], "
              "표준편차를 각각 σ₁, σ₂라 할 때, 다음 중 옳은 것은?"),
    choices=["[[sub(m,1) > sub(m,2)]], σ₁ > σ₂", "[[sub(m,1) > sub(m,2)]], σ₁ < σ₂", "[[sub(m,1) < sub(m,2)]], σ₁ > σ₂",
             "[[sub(m,1) < sub(m,2)]], σ₁ < σ₂", "[[sub(m,1) = sub(m,2)]], σ₁ = σ₂"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "x축 위 두 정규분포곡선: A는 왼쪽에 있고 낮고 넓음, B는 오른쪽에 있고 높고 좁음(각 꼭대기 아래 점선)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 정규분포곡선 그래프 / 문법 범위 밖: 그리스 문자 σ₁, σ₂ 텍스트 혼합",
    note="A 왼쪽·넓음 → m₁<m₂, σ₁>σ₂ → ③. 빠른정답 4와 불일치.")

# p13
add(id="5082298d", qtype="short",
    question=("확률변수 [[X]]는 정규분포 N([[m]], σ²)을 따른다.\n[[frac(1,3) X]]의 분산이 1이고, [[prob(X <= 25) = prob(X >= 35)]]일 때,\n"
              "[[m]] + σ²의 값을 구하시오."),
    choices=None, derived_answer="39", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 그리스 문자 σ → N(m, σ²), m+σ²을 텍스트 혼합으로 표기",
    note="σ²/9=1 → σ²=9, m=30 → 39. 빠른정답 673과 불일치(정렬 어긋남).")

# p35
add(id="98dd587a", qtype="short",
    question=("두 양수 [[m]], σ에 대하여 확률변수 [[X]]는 정규분포 [[normald(m, pow(1, 2))]], 확률변수 [[Y]]는 정규분포 N([[pow(m, 2) + 4m + 36]], σ²)을 "
              "따르고, 두 확률변수 [[X]], [[Y]]는 [[prob(X <= 0) = prob(Y <= 0)]]을 만족시킨다. σ의 값이 최소가 되도록 하는 [[m]]의 값을 [[sub(m,1)]]이라 하자. "
              "[[m = sub(m,1)]]일 때, 두 확률변수 [[X]], [[Y]]에 대하여 [[prob(X >= 1) = prob(Y <= k)]]를 만족시키는 상수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="176", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="문법 범위 밖: 그리스 문자 σ → N(m²+4m+36, σ²)을 텍스트 혼합으로 표기",
    note="출처 [2024년 7월 고3 확률과 통계 29번 변형]. σ=(m²+4m+36)/m=m+36/m+4 ≥ 16 (m=6) → X~N(6,1), Y~N(96,16²); P(X≥1)=P(Z≤5) → (k−96)/16=5 → k=176. 빠른정답 126과 불일치.")

# p55
add(id="e924b723", qtype="choice",
    question=("어느 학교 3학년 학생의 A 과목 시험 점수는 평균이 [[m]], 표준편차가 σ인 정규분포를 따르고, B 과목 시험 점수는 평균이 [[m + 3]], "
              "표준편차가 σ인 정규분포를 따른다고 한다. 이 학교 3학년 학생 중에서 A 과목 시험 점수가 80점 이상인 학생의 비율이 9%이고, "
              "B 과목 시험 점수가 80점 이상인 학생의 비율이 15%일 때, [[m]] + σ의 값은?\n"
              "(단, [[Z]]가 표준정규분포를 따르는 확률변수일 때, [[prob(0 <= Z <= 1.04) = 0.35]], [[prob(0 <= Z <= 1.34) = 0.41]]로 계산한다.)"),
    choices=["68.6", "70.6", "72.6", "74.6", "76.6"], derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 그리스 문자 σ(표준편차) 텍스트 혼합",
    note="출처 [2014년 9월 고3 이과 19번/4점]. (80−m)/σ=1.34, (77−m)/σ=1.04 → σ=10, m=66.6 → 76.6 → ⑤. 빠른정답 400과 불일치(정렬 어긋남).")

# p57
add(id="a5771908", qtype="choice",
    question=("어느 학교 3학년 학생의 A 과목 시험 점수는 평균이 [[m]], 표준편차가 σ인 정규분포를 따르고, B 과목 시험 점수는 평균이 [[m - 3]], "
              "표준편차가 σ인 정규분포를 따른다고 한다. 이 학교 3학년 학생 중에서 A 과목 시험 점수가 25점 이하인 학생의 비율이 9%이고, "
              "B 과목 시험 점수가 25점 이하인 학생의 비율이 15%일 때, [[m]] + σ의 값은?\n"
              "(단, [[Z]]가 표준정규분포를 따르는 확률변수일 때, [[prob(0 <= Z <= 1.04) = 0.35]], [[prob(0 <= Z <= 1.34) = 0.41]]로 계산한다.)"),
    choices=["45.4", "48.4", "51.4", "54.4", "57.4"], derived_answer="②", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 그리스 문자 σ(표준편차) 텍스트 혼합",
    note="(m−25)/σ=1.34, (m−28)/σ=1.04 → σ=10, m=38.4 → 48.4 → ② = 빠른정답 ✓.")

# p78
add(id="f9533ab1", qtype="short",
    question=("다음 (가), (나)에 알맞은 수의 합을 구하시오.\n"
              "확률변수 [[X]]가 이항분포 [[binomd(108, frac(1,6))]]을 따를 때,\n"
              "[[n p = 108 × frac(1,6) = 18 >= 5]],\n"
              "[[n q = 108 × frac(5,6) = 90 >= 5]]이므로\n"
              "확률변수 [[X]]는 근사적으로 정규분포 N((가), (나))를 따른다."),
    choices=None, derived_answer="33", figure=None, difficulty_est=1, confidence=0.85,
    note="원문 108·1/6의 가운뎃점은 ×로 표기. (가) 18, (나) npq=15 → 33. 빠른정답 256과 불일치(정렬 어긋남).")

# ───────── 확률의 뜻 ─────────
# p1
add(id="3c11270f", qtype="short",
    question=("표본공간 [[S]] = { [[x]] | [[x]]는 12 이하의 자연수 }에 대하여 두 사건 [[A]], [[B]]가 [[A]] = { [[x]] | [[x]]는 12의 약수 }, "
              "[[B]] = { [[x]] | [[x]]는 12 이하의 홀수 }일 때, 두 사건 [[A]], [[B]]와 모두 배반인 사건 [[C]]의 개수를 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="A∪B의 여집합 {8, 10}의 부분집합 개수 2²=4 = 빠른정답 ✓.")

# p14
add(id="ae4837ee", qtype="choice",
    question=("전체집합 [[U = set(1, 2, 3, 4, 5, 6)]]에 대하여 집합 [[U]]의 부분집합 [[A]]가 [[A]] = { [[x]] | [[x]]는 홀수 }이다. "
              "집합 [[U]]의 공집합이 아닌 부분집합 중 임의로 한 부분집합 [[X]]를 택할 때, 집합 [[union(A, X)]]의 모든 원소의 곱이 짝수일 확률은?"),
    choices=["[[frac(52,63)]]", "[[frac(6,7)]]", "[[frac(8,9)]]", "[[frac(58,63)]]", "[[frac(20,21)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="짝수 원소를 포함하는 부분집합 63−7=56 → 56/63=8/9 → ③ = 빠른정답 ✓.")

# p15
add(id="aec50742", qtype="choice",
    question=("집합 [[X = set(1, 2, 3, 4)]]의 공집합이 아닌 모든 부분집합 15개 중에서 임의로 서로 다른 세 부분집합을 뽑아 임의로 일렬로 나열하고, "
              "나열된 순서대로 [[A]], [[B]], [[C]]라 할 때, [[A]] ⊂ [[B]] ⊂ [[C]]일 확률은?"),
    choices=["[[frac(1,91)]]", "[[frac(2,91)]]", "[[frac(3,91)]]", "[[frac(4,91)]]", "[[frac(5,91)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 9월 고3 이과 19번/4점]. 포함 연쇄 A⊂B⊂C는 텍스트 기호로 표기. 사슬 60개/(15·14·13) = 2/91 → ② = 빠른정답 ✓.")

# p21
add(id="5856d71a", qtype="short",
    question=("집합 {1, 2, 3, ⋯, 16}에서 선택한 임의의 두 수 [[m]], [[n]]에 대하여 [[pow(3, m) + pow(8, n)]]의 일의 자리의 숫자가 3일 확률이 "
              "[[frac(b, a)]]일 때, [[a + b]]의 값을 구하시오.\n(단, [[a]], [[b]]는 서로소인 자연수)"),
    choices=None, derived_answer=None, figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2008년 7월 고3 문과 30번]. 답 미도출: 두 수 선택 해석에 따라 3/16(중복 허용 → 19) 또는 11/60(서로 다른 두 수 → 71). 빠른정답 4는 정렬 어긋남으로 보임.")

# p58
add(id="8eab8f4b", qtype="choice",
    question=("집합 { [[x]] | [[x]]는 12 이하의 자연수 }의 원소의 개수가 4인 부분집합 중 임의로 하나의 집합을 택하여 [[X]]라 할 때, "
              "집합 [[X]]가 다음 조건을 만족시킬 확률은?\n"
              "집합 [[X]]의 서로 다른 세 원소의 합은 항상 3의 배수가 아니다."),
    choices=["[[frac(2,11)]]", "[[frac(1,5)]]", "[[frac(12,55)]]", "[[frac(13,55)]]", "[[frac(14,55)]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.9,
    note="나머지 두 종류를 2개씩: 3·C(4,2)²=108, 108/495=12/55 → ③ = 빠른정답 ✓.")

# p89
add(id="630dfb37", qtype="short",
    question=("1부터 50까지의 자연수가 각각 하나씩 적힌 50개의 공이 들어 있는 상자가 있다. 이 상자에서 임의로 한 개의 공을 꺼낼 때, "
              "짝수가 적힌 공을 뽑는 사건을 [[A]], 홀수가 적힌 공을 뽑는 사건을 [[B]]라 하자. [[prob(union(A, B))]]를 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=1, confidence=0.85,
    note="A∪B=S → 1. 빠른정답 47과 불일치(정렬 어긋남).")

# ───────── 이항정리 ─────────
# p4
add(id="c0178a84", qtype="choice",
    question=("[[pow(x + 5, 40) = sub(a,0) + sub(a,1) x + sub(a,2) pow(x, 2)]] + ⋯ + [[sub(a,40) pow(x, 40)]]이라 할 때,\n"
              "[[frac(sub(a, k+1), sub(a, k)) > frac(1,5)]]을 만족시키는 음이 아닌 정수 [[k]]의 최댓값은?"),
    choices=["9", "12", "14", "16", "19"], derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="a_{k+1}/a_k = (40−k)/(5(k+1)) > 1/5 → k < 19.5 → 19 → ⑤. 빠른정답 2와 불일치.")

# p5
add(id="d4de724e", qtype="choice",
    question=("[[pow(x + 4, 40) = sub(a,0) + sub(a,1) x + sub(a,2) pow(x, 2)]] + ⋯ + [[sub(a,40) pow(x, 40)]]이라 할 때,\n"
              "[[frac(sub(a, k+1), sub(a, k)) > frac(1,4)]]을 만족시키는 음이 아닌 정수 [[k]]의 최댓값은?"),
    choices=["9", "12", "14", "16", "19"], derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="a_{k+1}/a_k = (40−k)/(4(k+1)) > 1/4 → k < 19.5 → 19 → ⑤. 빠른정답 3과 불일치.")

# p6
add(id="362ed40d", qtype="choice",
    question=("[[pow(x + 4, 50) = sub(a,0) + sub(a,1) x + sub(a,2) pow(x, 2)]] + ⋯ + [[sub(a,50) pow(x, 50)]]이라 할 때,\n"
              "[[frac(sub(a, k+1), sub(a, k)) > frac(1,4)]]을 만족시키는 음이 아닌 정수 [[k]]의 최댓값은?"),
    choices=["16", "20", "24", "26", "29"], derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="a_{k+1}/a_k = (50−k)/(4(k+1)) > 1/4 → k < 24.5 → 24 → ③. 빠른정답 2와 불일치.")

# p28
add(id="aedaa880", qtype="choice",
    question=("다음은 [[x]]에 대한 다항식 [[pow(x + pow(a, 2), n)]]과 [[(pow(x, 2) - 2a) pow(x + a, n)]]의 전개식에서 [[pow(x, n - 1)]]의 계수가 같게 되는 "
              "두 자연수 [[a]]와 [[n]] ([[n >= 4]])의 값을 구하는 과정의 일부이다.\n"
              "[[pow(x + pow(a, 2), n)]]의 전개식에서 [[pow(x, n - 1)]]의 계수는 [[pow(a, 2) n]]이다.\n"
              "[[(pow(x, 2) - 2a) pow(x + a, n) = pow(x, 2) pow(x + a, n) - 2a pow(x + a, n)]]에서\n"
              "[[pow(x, 2) pow(x + a, n)]]을 전개하면\n"
              "[[pow(x, n - 1)]]의 계수는 (가) × [[pow(a, 3)]]이고,\n"
              "[[2a pow(x + a, n)]]을 전개하면 [[pow(x, n - 1)]]의 계수는 [[2 pow(a, 2) n]]이다.\n"
              "따라서 [[(pow(x, 2) - 2a) pow(x + a, n)]]의 전개식에서 [[pow(x, n - 1)]]의 계수는\n"
              "(가) × [[pow(a, 3)]] − [[2 pow(a, 2) n]]\n"
              "이다. 그러므로\n"
              "[[pow(a, 2) n]] = (가) × [[pow(a, 3)]] − [[2 pow(a, 2) n]]\n"
              "이고, 이 식을 정리하여 [[a]]를 [[n]]에 관한 식으로 나타내면\n"
              "[[a]] = 18 / (나)\n"
              "이다. 여기서 [[a]]는 자연수이고 [[n]]은 4이상의 자연수이므로\n"
              "[[n]] = (다)\n"
              "이다.\n"
              "위 (가), (나)에 알맞은 식을 각각 [[f(n)]], [[g(n)]]이라 하고, (다)에 알맞은 수를 [[k]]라 할 때, [[f(k) + g(k)]]의 값은?"),
    choices=["10", "16", "22", "28", "34"], derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2017년 6월 고3 이과 19번/4점]. (가) ₙC₃, (나) (n−1)(n−2), (다) 4 → f(4)+g(4)=4+6=10 → ①. 빠른정답 20과 불일치(선지에 없음).")

# p31
add(id="b9345ce6", qtype="short",
    question=("다항식 [[2 pow(x + a, n)]]의 전개식에서 [[pow(x, n - 1)]]의 계수와 다항식 [[(x - 1) pow(x + a, n)]]의 전개식에서 [[pow(x, n - 1)]]의 계수가 "
              "같게 되는 모든 순서쌍 ([[a]], [[n]])에 대하여 [[a n]]의 최댓값을 구하시오.\n"
              "(단, [[a]]는 자연수이고, [[n]]은 [[n >= 2]]인 자연수이다.)"),
    choices=None, derived_answer="12", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2005년 11월 고3 문과 30번]. 2na = ₙC₂a² − na → (n−1)a=6 → (a,n)=(1,7),(2,4),(3,3),(6,2) → an 최대 12 = 빠른정답 ✓.")

# p33
add(id="69f79977", qtype="choice",
    question=("다음은 [[x]]에 대한 다항식 [[pow(x + pow(a, 3), n)]]과 [[(pow(x, 2) - 4a) pow(x + a, n)]]의 전개식에서 [[pow(x, n - 1)]]의 계수가 같게 되는 "
              "두 자연수 [[a]]와 [[n]] ([[n > 5]])의 값을 구하는 과정의 일부이다.\n"
              "[[pow(x + pow(a, 3), n)]]의 전개식에서 [[pow(x, n - 1)]]의 계수는 [[pow(a, 3) n]]이다.\n"
              "[[(pow(x, 2) - 4a) pow(x + a, n) = pow(x, 2) pow(x + a, n) - 4a pow(x + a, n)]]에서 [[pow(x, 2) pow(x + a, n)]]을 전개하면 "
              "[[pow(x, n - 1)]]의 계수는 (가) · [[pow(a, 3)]]이고, [[4a pow(x + a, n)]]을 전개하면 [[pow(x, n - 1)]]의 계수는 [[4 pow(a, 2) n]]이다.\n"
              "따라서 [[(pow(x, 2) - 4a) pow(x + a, n)]]의 전개식에서 [[pow(x, n - 1)]]의 계수는 (가) · [[pow(a, 3)]] − [[4 pow(a, 2) n]]이다.\n"
              "그러므로 [[pow(a, 3) n]] = (가) · [[pow(a, 3)]] − [[4 pow(a, 2) n]]이고, 이 식을 정리하여 [[a]]를 [[n]]에 관한 식으로 나타내면 "
              "[[a]] = 24 / (나) 이다.\n"
              "여기서 [[a]]는 자연수이고 [[n]]은 5보다 큰 자연수이므로 [[n]] = (다) 이다.\n"
              "위 (가), (나)에 알맞은 식을 각각 [[f(n)]], [[g(n)]]이라 하고, (다)에 알맞은 수를 [[k]]라 할 때, [[f(k) + g(k)]]의 값은?"),
    choices=["35", "43", "51", "59", "67"], derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2017년 6월 고3 문과 19번 변형]. (가) ₙC₃, a=24/(n²−3n−4)=24/((n−4)(n+1)), n>5 → n=7(a=1) → f(7)+g(7)=35+24=59 → ④. 빠른정답 9와 불일치.")
