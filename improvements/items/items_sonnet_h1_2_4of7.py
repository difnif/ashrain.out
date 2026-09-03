# -*- coding: utf-8 -*-
# esc_sonnet_h1-2_4of7 — 이미지 기준 전사 (86 항목 / 80쪽)
# 문서: 260828_집합의 연산과 벤 다이어그램 (13 id) + 260828_명제의 역과 대우 (17 id) + 260828_절대부등식 (15 id)
#       + 260828_명제와 조건 (34 id) + 260828_원의 방정식과 그래프 (7 id)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_A = ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]      # 흔한 합답형 배열 1
CH_B = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]   # 흔한 합답형 배열 2
CH_C = ["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_D = ["ㄱ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ================= 260828_집합의 연산과 벤 다이어그램 =================
# p71 (id 2개)
dup(["dee07042", "cf6f5149"], qtype="choice",
    question=("전체집합 [[U = set(1, 2, 3, 4, 5, 6, 7, 8)]]의 두 부분집합\n[[A]], [[B]]에 대하여 연산 ∗ 를\n"
              "[[A]] ∗ [[B]] = [[inter(comp(A - B), comp(B - A))]]라 할 때, 다음 보기 중\n옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[set(1, 2, 3)]] ∗ [[set(1, 3, 4, 5)]] = [[set(1, 3, 6, 7, 8)]]\n"
              "ㄴ. [[A]] ∗ [[B]] = [[comp(A)]] ∗ [[comp(B)]]\n"
              "ㄷ. [[A]] ∗ [[B]] = [[empty]]을 만족시키는 두 집합 [[A]], [[B]]의\n순서쌍 ([[A]], [[B]])의 개수는 256이다."),
    choices=CH_B, derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="연산 기호 ∗는 텍스트. A∗B=(A△B)ᶜ: ㄱ {1,3,6,7,8} ✓, ㄴ Aᶜ△Bᶜ=A△B ✓, ㄷ B=Aᶜ인 순서쌍 2⁸=256 ✓ → ⑤ = 빠른정답 ✓.")

# p73
add(id="9f17e176", qtype="short",
    question=("두 집합 [[A = setb(x, pow(x,2) + p x - q < 0)]],\n[[B = setb(x, pow(x,2) - 8x + 7 < 0)]]에 대하여\n"
              "[[inter(A, B) = setb(x, 1 < x < 5)]], [[union(A, B) = setb(x, -2 < x < 7)]]\n일 때, [[q - p]]의 값을 구하시오. (단, [[p]], [[q]]는 상수이다.)"),
    choices=None, derived_answer="13", figure=None, difficulty_est=2, confidence=0.9,
    note="B=(1,7) → A=(−2,5) → x²−3x−10 → p=−3, q=10 → 13 = 빠른정답 ✓.")

# p75
add(id="03de6b41", qtype="short",
    question=("자연수 [[n]]에 대하여 집합 [[sub(A,n)]]을\n[[sub(A,n)]] = { [[x]] | [[abs(frac(x,n) - 2) <= 1]], [[x]]는 자연수 }라 하고,\n"
              "[[sub(S,n)]]을 집합 [[sub(A,n)]]의 모든 원소들의 합이라 한다.\n이때 [[sub(S,1) + sub(S,2) + sub(S,3)]]의 값을 구하시오."),
    choices=None, derived_answer="68", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2004년 6월 고2 이과 26번]. n≤x≤3n: S₁=6, S₂=20, S₃=42 → 68. 빠른정답 1과 불일치.")

# p77
add(id="05d04e96", qtype="choice",
    question=("[[3 <= a < b]]인 두 상수 [[a]], [[b]]에 대하여 세 집합\n"
              "[[A]] = { [[point(x, y)]] | [[y = frac(15,8) x]], [[pow(x + 5, 2) + pow(y + 3, 2) = 9]] }\n"
              "[[B]] = { [[point(x, y)]] | [[y = frac(15,8) x]], [[pow(x - a - 2, 2) + pow(y - a, 2) = pow(a,2)]] }\n"
              "[[C]] = { [[point(x, y)]] | [[y = frac(15,8) x]], [[pow(x - b - 2, 2) + pow(y - b, 2) = pow(b,2)]] }\n"
              "이 있다. [[card(union(union(A, B), C)) = 3]]일 때, [[a + b]]의 값은?"),
    choices=["[[frac(158,17)]]", "[[frac(162,17)]]", "[[frac(166,17)]]", "10", "[[frac(174,17)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.85,
    note="A는 접점 1개(제3사분면), B는 a=3일 때만 접함(접점 (40/17,75/17)), C가 그 점을 지나야 함 → b=111/17 → a+b=162/17 → ②. 빠른정답 3과 불일치.")

# p78
add(id="f5ce1dba", qtype="short",
    question=("두 집합\n[[A = setb(x, pow(x,2) - 9 = 0)]], [[B = setb(x, pow(x,2) + a x - 3 = 0)]]\n"
              "에 대하여 [[A - B = set(-3)]]일 때, 집합 [[union(A, B)]]의 모든\n원소의 합을 구하시오. (단, [[a]]는 상수이다.)"),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.9,
    note="3∈B → a=−2, B={3,−1} → A∪B={−3,−1,3} 합 −1. 빠른정답 34와 불일치.")

# p79
add(id="6393c3f8", qtype="short",
    question=("[[card(U) = 50]]인 전체집합 [[U]]의 세 부분집합 [[A]], [[B]], [[C]]가\n다음과 같은 조건을 만족할 때,\n"
              "[[card(union(union((inter(A, B)), (inter(B, C))), (inter(C, A))))]]의 값을 구하시오.\n"
              "(가) [[card(A) = 38]], [[card(B) = 31]], [[card(C) = 27]]\n"
              "(나) [[card(inter(inter(A, B), C)) = 9]], [[card(comp((union(union(A, B), C)))) = 0]]"),
    choices=None, derived_answer="37", figure=None, difficulty_est=3, confidence=0.9,
    note="쌍교집합 합 = 96+9−50 = 55 → 55−3·9+9 = 37. 빠른정답 4와 불일치.")

# p80
add(id="c03f7ae3", qtype="choice",
    question=("집합 [[A]]의 부분집합의 개수를 [[f(A)]]라 할 때,\n두 집합 [[A]], [[B]]는 다음 조건을 만족한다.\n"
              "(가) [[card(A) = 10]], [[card(B) >= 10]]\n(나) [[f(A) + f(B) = f(union(A, B))]]\n"
              "[[f(inter(A, B)) = pow(2,a)]]일 때, 상수 [[a]]의 값은? (단, [[pow(2,0) = 1]])"),
    choices=["5", "6", "7", "8", "9"], derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="2¹⁰+2^n(B)가 2의 거듭제곱 → n(B)=10, n(A∪B)=11 → n(A∩B)=9 → ⑤. 빠른정답 2와 불일치.")

# p84
add(id="42f9840b", qtype="short",
    question="두 집합 [[A]], [[B]]에 대하여 [[card(A) = 8]], [[card(B) = 12]],\n[[card(inter(A, B)) = 4]]일 때, [[card(union(A, B))]]를 구하시오.",
    choices=None, derived_answer="16", figure=None, difficulty_est=1, confidence=0.9,
    note="8+12−4=16. 빠른정답 34와 불일치.")

# p88
add(id="0a0fa2ea", qtype="short",
    question=("1보다 큰 자연수 [[k]]에 대하여\n전체집합 [[U]] = { [[x]] | [[x]]는 [[k]] 이하의 자연수 }의\n"
              "두 부분집합 [[A]] = { [[x]] | [[x]]는 [[k]] 이하의 짝수 },\n[[B]] = { [[x]] | [[x]]는 [[k]]의 약수 }가\n"
              "[[card(A) × card(comp((union(A, B)))) = 15]]를 만족시킨다.\n집합 [[comp((union(A, B)))]]의 모든 원소의 곱을 구하시오."),
    choices=None, derived_answer="189", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2024년 3월 고2 28번/4점]. n(A)=[k/2]∈{1,3,5,15} 전수 확인 → k=10, (A∪B)ᶜ={3,7,9} → 189. 빠른정답 4와 불일치.")

# p90 (id 2개)
dup(["92cc777f", "12e49ec7"], qtype="short",
    question=("전체집합 [[U]]의 두 부분집합 [[A]], [[B]]가 다음 조건을 만족시킬\n때, [[card(B)]]의 최댓값을 구하시오.\n<조건>\n"
              "(가) [[card(U) = 30]]\n(나) [[inter(A, (union(B, comp(A)))) = empty]]\n(다) [[card(A - B) = 12]]"),
    choices=None, derived_answer="18", figure=None, difficulty_est=2, confidence=0.9,
    note="(나) ⇔ A∩B=∅ → n(A)=12 → n(B)≤18. 빠른정답 14와 불일치.")

# p93
add(id="ef1845f9", qtype="short",
    question=("전체집합이 [[U]] = { 1, 2, 3, ⋯, 100 }이고,\n[[A]] = { [[in(x, U)]] | [[x]]는 홀수 },\n"
              "[[B]] = { [[in(x, U)]] | [[x]]는 3의 배수 }일 때,\n집합 [[inter(comp(A), B)]]의 원소의 개수를 구하시오."),
    choices=None, derived_answer="16", figure=None, difficulty_est=1, confidence=0.9,
    note="짝수인 3의 배수 = 6의 배수 16개. 빠른정답 18과 불일치.")

# ================= 260828_명제의 역과 대우 =================
# p5
add(id="5034fe21", qtype="choice",
    question="다음 중 그 역과 대우가 모두 참인 명제는?\n(단, [[a]], [[b]], [[x]]는 모두 실수이다.)",
    choices=["[[a = b]]이면 [[a b = pow(b,2)]]이다.",
             "[[x > 3]]이면 [[x >= 3]]이다.",
             "[[pow(x,2) = 4]]이면 [[x + 2 = 0]]이다.",
             "두 집합 [[A]], [[B]]에 대하여 [[subset(B, A)]]이면 [[union(A, B) = A]]이다.",
             "[[quad(ABCD)]]의 네 변의 길이가 모두 같으면 [[quad(ABCD)]]는 정사각형이다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="④ B⊂A ⇔ A∪B=A (역·대우 모두 참). ①② 역 거짓, ③⑤ 명제 거짓 → ④. 빠른정답 'L'(값 아님).")

# p7
add(id="6e25be16", qtype="short",
    question=("두 조건 [[p]]: [[abs(x - 2) >= k]], [[q]]: [[abs(x - 1) < 2]]에 대하여\n"
              "명제 [[imp(p, neg(q))]]의 역이 참이 되도록 하는 실수 [[k]]의\n최댓값을 구하시오. (단, [[k > 0]])"),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.9,
    note="역 ~q→p: {x≤−1 또는 x≥3} ⊂ {x≤2−k 또는 x≥2+k} → k≤1 → 최댓값 1. 빠른정답 4와 불일치.")

# p18
add(id="767a6d94", qtype="choice",
    question="다음 중 그 역이 거짓인 명제는?",
    choices=["[[-2x < -2y]]이면 [[x > y]]이다.",
             "[[pow(x,2) = pow(y,2)]]이면 [[x = -y]]이다.",
             "3의 양의 약수이면 9의 양의 약수이다.",
             "[[x = 3]]이면 [[2x - 8 = -2]]이다.",
             "[[x y < 0]]이면 [[x < 0]]이고 [[y > 0]]이다."],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="③ 역 '9의 양의 약수이면 3의 양의 약수' 반례 9 → 거짓. 나머지 역은 참 → ③. 빠른정답 5와 불일치.")

# p26
add(id="3a7b0ada", qtype="short",
    question=("두 조건 [[p]]: [[a - 8 <= x <= a]], [[q]]: [[-a b <= x <= b - 1]]에\n"
              "대하여 명제 [[imp(p, q)]]의 역과 대우가 모두 참이다. 이때 양수\n[[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="P=Q: a=b−1, a−8=−ab → a²+2a−8=0 → a=2, b=3 → 5. 빠른정답 7과 불일치.")

# p38
add(id="06387297", qtype="choice",
    question=("두 실수 [[a]], [[b]]에 대하여\n명제 '[[a + b >= 5]]이면 [[a >= -1]] 또는 [[b >= k]]이다.'가 참일\n때, 실수 [[k]]의 최댓값은?"),
    choices=["0", "2", "4", "6", "8"], derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="대우: a<−1, b<k ⇒ a+b<5 → k−1≤5 → k≤6 → ④. 빠른정답 7과 불일치.")

# p40
add(id="27779b6f", qtype="short",
    question=("두 조건 [[p]]: [[abs(x - 2) >= 1]], [[q]]: [[abs(x - a) >= 3]]에 대하여\n"
              "명제 [[imp(q, p)]]가 참이 되도록 하는 실수 [[a]]의 값의 범위를\n[[m <= a <= n]]이라 할 때 [[m + n]]의 값을 구하시오.\n(단, [[m]], [[n]]은 실수이다.)"),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.9,
    note="대우 ~p→~q: (1,3)⊂(a−3,a+3) → 0≤a≤4 → m+n=4. 빠른정답 16과 불일치.")

# p42
add(id="7ec9577c", qtype="short",
    question=("실수 [[x]]에 대한 두 조건\n[[p]]: [[(pow(x,2) - m x + 2m)(pow(x,2) + x - 6) < 0]],\n[[q]]: [[pow(x,2) + x - 6 < 0]]\n"
              "에 대하여 명제 [[imp(p, q)]]가 참이 되도록 하는 실수 [[m]]의\n최댓값을 [[a]], 최솟값을 [[b]]라 할 때, [[-5a b]]의 값을 구하시오."),
    choices=None, derived_answer="72", figure=None, difficulty_est=4, confidence=0.85,
    note="x²−mx+2m≥0이 항상이거나(0≤m≤8) 두 근이 [−3,2] 안(−9/5≤m≤0) → −9/5≤m≤8 → −5·8·(−9/5)=72. 빠른정답 7과 불일치(다음 문항 빠른정답이 72).")

# p45
add(id="99e2bfa3", qtype="choice",
    question=("두 조건 [[p]], [[q]]가 '[[p]]: [[x < k]]', '[[q]]: [[-8 < x < 5]]'일 때,\n"
              "명제 [[imp(neg(p), neg(q))]]가 참이 되도록 하는 실수 [[k]]의 값의\n범위는?"),
    choices=["[[k <= -8]]", "[[k < -8]]", "[[k >= 5]]", "[[k > 5]]", "[[-8 <= k <= 5]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="~p→~q ⇔ q→p: (−8,5)⊂(−∞,k) → k≥5 → ③. 빠른정답 72와 불일치.")

# p54
add(id="8b081a68", qtype="choice",
    question="세 조건 [[p]], [[q]], [[r]]에 대하여 두 명제 [[imp(p, q)]], [[imp(q, neg(r))]]가\n참일 때, 항상 참인 명제는?",
    choices=["[[imp(q, p)]]", "[[imp(p, r)]]", "[[imp(r, neg(p))]]", "[[imp(neg(r), p)]]", "[[imp(neg(q), neg(r))]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="p⇒q⇒~r → 대우 r⇒~p → ③ = 빠른정답 ✓.")

# p55
add(id="a6b2e807", qtype="choice",
    question="세 조건 [[p]], [[q]], [[r]]에 대하여 두 명제 [[imp(neg(p), q)]],\n[[imp(q, r)]] 가 참일 때, 항상 참인 명제는?",
    choices=["[[imp(q, p)]]", "[[imp(p, r)]]", "[[imp(r, neg(p))]]", "[[imp(neg(r), p)]]", "[[imp(neg(q), neg(r))]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="~p⇒q⇒r → 대우 ~r⇒p → ④. 빠른정답 1과 불일치.")

# p57
add(id="9b0ab8ad", qtype="choice",
    question=("세 조건 [[p]], [[q]], [[r]]에 대하여\n두 명제 [[imp(neg(q), neg(p))]], [[imp(r, neg(q))]]가 모두 참일 때,\n<보기>에서 참인 명제를 모두 고른 것은?\n<보기>\n"
              "ㄱ. [[imp(p, q)]]\nㄴ. [[imp(q, r)]]\nㄷ. [[imp(r, neg(p))]]"),
    choices=CH_A, derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="p⇒q, q⇒~r: ㄱ ✓, ㄴ ✗, ㄷ r⇒~q⇒~p ✓ → ③ = 빠른정답 ✓.")

# p62
add(id="b5b02647", qtype="choice",
    question="명제 [[p]]⇒[[neg(q)]] 와 [[neg(p)]]⇒[[r]] 가 모두 참일 때, 다음\n중에서 반드시 참이라고 할 수 없는 것은?",
    choices=["[[q]]⇒[[neg(p)]]", "[[neg(r)]]⇒[[p]]", "[[q]]⇒[[r]]", "[[neg(r)]]⇒[[neg(q)]]", "[[q]]⇒[[neg(r)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="⇒ 기호는 텍스트. q⇒~p⇒r → ①③ ✓, ②④는 대우 ✓, ⑤ q⇒~r 보장 안 됨 → ⑤. 빠른정답 4와 불일치.")

# p64
add(id="758fc72d", qtype="choice",
    question="두 명제 [[p]] ⇒ [[q]]와 [[neg(r)]]⇒[[neg(q)]]가 모두 참일 때, 다음 중\n항상 참인 명제는?",
    choices=["[[p]]⇒[[r]]", "[[neg(q)]]⇒[[p]]", "[[p]]⇒[[neg(q)]]", "[[r]]⇒[[q]]", "[[r]]⇒[[neg(q)]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="⇒ 기호는 텍스트. ~r⇒~q ⇔ q⇒r → p⇒q⇒r → ①. 빠른정답 5와 불일치.")

# p66
add(id="2b737c73", qtype="choice",
    question="세 명제 [[imp(p, q)]], [[imp(s, neg(q))]], [[imp(neg(p), r)]]가 모두 참일 때,\n다음 명제 중 항상 참이라고 할 수 없는 것은?",
    choices=["[[imp(p, neg(s))]]", "[[imp(q, neg(s))]]", "[[imp(s, neg(p))]]", "[[imp(neg(r), q)]]", "[[imp(r, p)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="p⇒q⇒~s, ~r⇒p⇒q → ①~④ 참, ⑤ r⇒p 보장 안 됨 → ⑤. 빠른정답 4와 불일치.")

# p69
add(id="667fde25", qtype="choice",
    question=("네 조건 [[p]], [[q]], [[r]], [[s]]에 대하여 두 명제 [[imp(neg(p), neg(q))]], [[imp(r, s)]]가\n"
              "모두 참일 때, 다음 중 명제 [[imp(r, p)]]가 참임을 보이기 위하여\n필요한 참인 명제는?"),
    choices=["[[imp(q, neg(s))]]", "[[imp(neg(q), s)]]", "[[imp(s, q)]]", "[[imp(neg(s), q)]]", "[[imp(s, neg(q))]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="r⇒s, q⇒p(대우) → s⇒q가 있으면 r⇒s⇒q⇒p → ③. 빠른정답 5와 불일치.")

# p99 (한 이미지에 별개 문항 2개; draft_a 대응대로 분리) — 위쪽 문항
add(id="05a55aa9", qtype="choice",
    question=("두 명제 (가), (나)가 모두 참일 때, 다음 중\n명제 '오렌지를 좋아하면 딸기를 좋아한다.'가 참임을\n보이기 위해 필요한 명제는?\n"
              "(가) 배를 좋아하지 않으면 오렌지를 좋아하지 않는다.\n(나) 딸기를 좋아하지 않으면 사과를 좋아한다."),
    choices=["오렌지를 좋아하면 배를 좋아한다.", "딸기를 좋아하면 사과를 좋아하지 않는다.", "사과를 좋아하지 않으면 딸기를 좋아한다.",
             "배를 좋아하면 사과를 좋아하지 않는다.", "사과를 좋아하면 오렌지를 좋아한다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="p99 이미지 위쪽 문항. 오렌지⇒배(가의 대우), ~사과⇒딸기(나의 대우) → 배⇒~사과 필요 → ④. 빠른정답 1과 불일치.")

# p99 — 아래쪽 문항
add(id="9d722ea9", qtype="choice",
    question=("다음 두 명제가 모두 참일 때, 항상 참인 명제는?\n"
              "(가) 꽃을 좋아하는 사람은 나무를 좋아한다.\n(나) 꽃을 좋아하지 않는 사람은 산을 좋아하지 않는다."),
    choices=["꽃을 좋아하는 사람은 산을 좋아한다.", "나무를 좋아하는 사람은 산을 좋아한다.", "꽃을 좋아하지 않는 사람은 나무를 좋아하지 않는다.",
             "산을 좋아하는 사람은 나무를 좋아한다.", "산을 좋아하는 사람은 꽃은 좋아하지 않는다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="p99 이미지 아래쪽 문항. 산⇒꽃(나의 대우)⇒나무 → ④. 빠른정답 1과 불일치.")

# ================= 260828_절대부등식 =================
# p39
add(id="31ea86ad", qtype="short",
    question="[[a > 0]], [[b > 0]], [[c > 0]]일 때,\n[[(1 + frac(b,a))(1 + frac(3c,b))(1 + frac(a,3c))]]의 최솟값을 구하시오.",
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="각 인수 AM-GM: ≥ 2√(b/a)·2√(3c/b)·2√(a/3c) = 8 (a=b=3c). 빠른정답 12와 불일치(다음 문항 빠른정답이 8).")

# p42
add(id="3fe758cd", qtype="short",
    question=("집합 [[X]]의 모든 원소의 합을 [[S(X)]]라 하자.\n전체집합 [[U]] = { [[x]] | [[x]]는 10 이하의 자연수 }의\n"
              "두 부분집합 [[A]], [[B]]에 대하여 [[union(A, B) = U]],\n[[inter(A, B) = set(3, 6)]]일 때, [[S(A) S(B)]]의 최댓값을\n구하시오."),
    choices=None, derived_answer="1024", figure=None, difficulty_est=3, confidence=0.9,
    note="S(A)+S(B)=55+9=64, 32·32 가능(A={3,6,10,8,5}) → 1024. 빠른정답 8과 불일치(다음 문항 빠른정답이 1024).")

# p43
add(id="b78e3921", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 8 이하의 자연수 }의\n두 부분집합 [[A]], [[B]]에 대하여 집합 [[A]]의 원소들의 합을\n"
              "[[S(A)]], 집합 [[B]]의 원소들의 합을 [[S(B)]]라 하자.\n[[union(A, B) = U]], [[inter(A, B) = set(2, 6)]]일 때, [[S(A) S(B)]]의\n최댓값은?"),
    choices=["472", "476", "480", "484", "488"], derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="S(A)+S(B)=36+8=44, 22·22 가능(A={2,6,8,5,1}) → 484 → ④. 빠른정답 13과 불일치.")

# p45
add(id="65ae3d43", qtype="choice",
    question=("0이 아닌 [[n]]개의 실수 [[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,n)]]에 대하여\n"
              "[[f(n) = pow(sub(a,1),2) + pow(sub(a,2),2)]] + ⋯ + [[pow(sub(a,n),2)]],\n"
              "[[g(n) = frac(1, pow(sub(a,1),2)) + frac(1, pow(sub(a,2),2))]] + ⋯ + [[frac(1, pow(sub(a,n),2))]]\n"
              "이라 할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(2) g(2) >= 4]]\nㄴ. [[f(n) + g(n) >= 2n]]\nㄷ. [[f(n)]], [[g(n)]]은 모두 [[n]]보다 크거나 같다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="ㄱ 코시-슈바르츠 ✓, ㄴ aᵢ²+1/aᵢ²≥2 ✓, ㄷ aᵢ=1/2이면 f(n)=n/4<n ✗ → ③. 빠른정답 1024와 불일치.")

# p54
add(id="ad47bed2", qtype="short",
    question=("그림과 같이 [[seg(AB) = 3]], [[seg(AC) = 4]], [[A = deg(30)]]인\n삼각형 ABC의 변 BC 위의 점 P에서\n"
              "두 직선 AB, AC 위에 내린 수선의 발을 각각 M, N이라\n하자. [[frac(seg(AB), seg(PM)) + frac(seg(AC), seg(PN))]]의 최솟값이 [[frac(q,p)]]일 때, [[p + q]]의 값을\n"
              "구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="55",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 오른쪽 위), ∠A=30°, AB=3·AC=4를 점선 호로 표시, 변 BC 위의 점 P에서 직선 AB 위 M·AC 위 N에 내린 수선(직각 표시)"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 삼각형과 수선의 발 그림",
    note="넓이 3 = (3·PM+4·PN)/2 → 3PM+4PN=6, 코시: (3/PM+4/PN)·6 ≥ 49 → 최솟값 49/6 → 55. 빠른정답 2와 불일치.")

# p55
add(id="af097135", qtype="choice",
    question=("두 양수 [[a]], [[b]]에 대하여 좌표평면 위의 점 [[P(a, b)]]를 지나고\n직선 OP에 수직인 직선이 [[x]]축과 만나는 점을 Q라 하자.\n"
              "점 [[R(0, -frac(2,b))]]에 대하여 삼각형 OQR의 넓이의\n최솟값은? (단, O는 원점이다.)"),
    choices=["[[frac(1,2)]]", "1", "[[frac(3,2)]]", "2", "[[frac(5,2)]]"], derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 11월 고1 16번 변형]. Q=((a²+b²)/a, 0), 넓이=(a²+b²)/(ab)=a/b+b/a≥2 → ④. 빠른정답 36과 불일치.")

# p56
add(id="e2397f8d", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 6]], [[angle(A) = deg(30)]], [[angle(B) = deg(45)]]인\n삼각형 ABC의 변 AB 위의 점 P에서 두 직선 AC, BC\n"
              "위에 내린 수선의 발을 각각 M, N이라 하자.\n[[frac(1, seg(PM)) + frac(sqrt(2), seg(PN))]]의 최솟값이 [[frac(q,p)]]일 때, [[p + q]]의 값을\n"
              "구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="7",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 왼쪽 아래 30°, B 오른쪽 위 45°, C 아래), AB=6 점선 호, 변 AB 위의 점 P에서 AC 위 M·BC 위 N에 내린 수선(직각 표시)"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 삼각형과 수선의 발 그림",
    note="PM=AP/2, PN=BP/√2 → 식 = 2/AP+2/BP, AP+BP=6 → 최솟값 4/3 → 7. 빠른정답 3과 불일치(다음 문항 빠른정답이 7).")

# p57
add(id="22cb68f7", qtype="choice",
    question=("다음 그림과 같이 한 변의 길이가\n[[x + y]] ([[x > 0]], [[y > 0]])인 정사각형 ABCD가 있다.\n"
              "정사각형의 네 변 AB, BC, DC, AD를 [[ratio(x, y)]]로 내분하는\n점을 각각 E, F, G, H라 할 때, 사각형 EFGH의 넓이는\n25이다. 이때 선분 GH의 길이의 최솟값은?"),
    choices=["[[2 sqrt(6)]]", "5", "[[2 sqrt(7)]]", "[[4 sqrt(2)]]", "6"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), 변 AB 위 E(AE=x, EB=y 점선 표시), BC 위 F, DC 위 G, AD 위 H, 사각형 EFGH 음영"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 정사각형 안 내분점 사각형 그림",
    note="EG⊥FH, 길이 모두 x+y → 넓이 (x+y)²/2=25 → (x+y)²=50, GH²=x²+y²≥(x+y)²/2=25 → 5 → ② = 빠른정답 ✓.")

# p59
add(id="47608132", qtype="choice",
    question="[[angle(C) = deg(90)]]인 직각삼각형 ABC에 대하여\n삼각형 ABC의 넓이가 16일 때, [[pow(seg(AB), 2)]]의 최솟값은?",
    choices=["48", "56", "64", "72", "80"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2021년 11월 고1 14번/4점]. ab=32, a²+b²≥2ab=64 → ③. 빠른정답 7과 불일치.")

# p69
add(id="fe45536a", qtype="short",
    question="실수 [[x]], [[y]], [[z]]가 [[x + 2y + z = 3]], [[pow(x,2) + pow(y,2) + pow(z,2) = 9]]를\n만족시킬 때, [[x]]의 최댓값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="(2y+z)²≤5(y²+z²): (3−x)²≤5(9−x²) → −2≤x≤3 → 3 = 빠른정답 ✓.")

# p75
add(id="451df86e", qtype="short",
    question=("부등식 [[pow(x,2) + pow(y,2) <= 3]]을 만족시키는\n모든 실수 [[x]], [[y]]에 대하여 [[a = x + y]], [[b = x y]]라 할 때,\n"
              "[[a]]의 최댓값을 [[M]], [[b]]의 최솟값을 [[m]]이라 하자.\n[[pow(M,2) + pow(m,2) = frac(q,p)]]일 때, [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="37", figure=None, difficulty_est=3, confidence=0.9,
    note="M=√6, m=−3/2 → 6+9/4=33/4 → 37 = 빠른정답 ✓.")

# p77
add(id="88305001", qtype="choice",
    question="[[x > 0]], [[y > 0]], [[z > 0]]이고, [[x + y + z = 10]]일 때,\n[[sqrt(x) + 2 sqrt(y) + 3 sqrt(z)]] 의 최댓값은?",
    choices=["[[sqrt(35)]]", "[[2 sqrt(35)]]", "[[3 sqrt(35)]]", "[[4 sqrt(35)]]", "[[5 sqrt(35)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="코시: (1+4+9)(x+y+z)=140 ≥ (식)² → 2√35 → ②. 빠른정답 6과 불일치.")

# p87 (id 2개)
dup(["b517ea5b", "bcd970e7"], qtype="choice",
    question=("실수 [[a]], [[b]], [[c]], [[x]], [[y]], [[z]]에 대하여\n"
              "부등식 [[(pow(a,2) + pow(b,2) + pow(c,2))(pow(x,2) + pow(y,2) + pow(z,2)) >= pow(a x + b y + c z, 2)]]\n"
              "은 항상 성립하고 등호는 [[ratio(a, b, c) = ratio(x, y, z)]]일 때\n성립한다.\n"
              "다음은 이 부등식을 이용하여 삼각형의 세 변의 길이\n[[p]], [[q]], [[r]]에 대하여\n"
              "[[(p + q + r)(frac(1, -p + q + r) + frac(1, p - q + r) + frac(1, p + q - r))]]의\n최솟값을 구하는 과정이다.\n"
              "[[-p + q + r = l]], [[p - q + r = m]],\n[[p + q - r = n]]이라 하면 [[l]], [[m]], [[n]]은 모두 양수이다.\n"
              "[[(p + q + r)(frac(1, -p + q + r) + frac(1, p - q + r) + frac(1, p + q - r))]]\n"
              "= ((가))[[(frac(1,l) + frac(1,m) + frac(1,n))]]\n"
              "[[(pow(a,2) + pow(b,2) + pow(c,2))(pow(x,2) + pow(y,2) + pow(z,2)) >= pow(a x + b y + c z, 2)]]을\n이용하면\n"
              "((가))[[(frac(1,l) + frac(1,m) + frac(1,n))]] ≥ (나) 이고\n등호는 [[l = m = n]]일 때 성립한다.\n따라서\n"
              "[[(p + q + r)(frac(1, -p + q + r) + frac(1, p - q + r) + frac(1, p + q - r))]]\n의 최솟값은 (나) 이다.\n"
              "(가), (나)에 알맞은 것을 바르게 짝지은 것은?"),
    choices=["(가): [[l + m + n]], (나): 6", "(가): [[l + m + n]], (나): 9", "(가): [[2(l + m + n)]], (나): 8",
             "(가): [[2(l + m + n)]], (나): 16", "(가): [[3(l + m + n)]], (나): 18"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2008년 11월 고1 19번]. 빈칸 상자 (가)(나)는 텍스트, 선지는 (가)·(나) 표 형식. l+m+n=p+q+r, (l+m+n)(1/l+1/m+1/n)≥9 → ② = 빠른정답 ✓.")

# p98
add(id="8d148014", qtype="choice",
    question=("다음 그림과 같이 둘레의 길이가 20이고 [[angle(A) = deg(90)]] 인\n사각형 ABCD의 각 변을 한 변으로 하는 정사각형의\n"
              "넓이를 각각 [[sub(S,1)]], [[sub(S,2)]], [[sub(S,3)]], [[sub(S,4)]]라고 하자.\n"
              "[[sub(S,1) + sub(S,2) + sub(S,3) + sub(S,4)]]의 값이 최소가 될 때,\n사각형 ABCD의 넓이는?"),
    choices=["21", "23", "25", "27", "29"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 위쪽, ∠A 직각 표시, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽)의 네 변 바깥쪽에 각 변을 한 변으로 하는 정사각형 S₁(AB), S₂(BC), S₃(CD), S₄(DA) 음영"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 사각형 각 변 위의 정사각형 그림",
    note="네 변 합 20 → 제곱합 ≥ 100, 등호 네 변 모두 5 → ∠A=90°이면 정사각형 → 넓이 25 → ③. 빠른정답 288과 불일치.")

# ================= 260828_명제와 조건 =================
# p13
add(id="303dfc5f", qtype="choice",
    question=("다음 보기 중 부정이 참인 명제만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 125는 5의 배수이다.\nㄴ. [[pow(-4, 2) > pow(4, 2)]]\nㄷ. 6은 소수이다.\nㄹ. [[notin(2, setb(x, pow(x,2) - 4x + 4 <= 0))]]"),
    choices=["ㄱ, ㄴ", "ㄱ, ㄹ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄹ", "ㄴ, ㄷ, ㄹ"], derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="부정이 참 = 거짓인 명제: ㄴ(16>16 거짓), ㄷ, ㄹ(집합={2}) → ⑤. 빠른정답 '정리'(값 아님).")

# p21
add(id="d865033b", qtype="choice",
    question="조건 「[[x <= -1]] 또는 [[x > 2]]」의 부정을 옳게 나타낸\n것은?",
    choices=["[[x >= -1]] 또는 [[x < 2]]", "[[x >= -1]] 이고 [[x < 2]]", "[[x < -1]] 또는 [[x >= 2]]", "[[x > -1]] 이고 [[x <= 2]]", "[[x > -1]] 또는 [[x <= 2]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="부정: x>−1 이고 x≤2 → ④ (빠른정답 없음).")

# p23
add(id="dd4ad4ce", qtype="short",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 정수 }에 대하여 두 조건 [[p]], [[q]]가\n"
              "'[[p]]: [[pow(x,2) - 10x + 9 <= 0]]', '[[q]]: [[pow(x,2) - 8x + 7 = 0]]'\n일 때, 조건 '[[p]]이고 [[neg(q)]]' 의 진리집합의 모든 원소의 합을\n구하시오."),
    choices=None, derived_answer="37", figure=None, difficulty_est=2, confidence=0.9,
    note="P={1,…,9}, Q={1,7} → P−Q 합 45−8=37 (빠른정답 없음).")

# p28
add(id="bdad4294", qtype="choice",
    question=("두 자연수 [[a]], [[b]]에 대하여 실수 [[x]]에 대한 두 조건\n[[p]]: [[pow(x,2) + 4x + a + 1 <= 0]], [[q]]: [[0 < abs(x - b) <= 3]]의\n"
              "진리집합을 각각 [[P]], [[Q]]라 하자. [[P != empty]], [[subset(P, Q)]]가\n되도록 하는 [[a]], [[b]]의 모든 순서쌍 ([[a]], [[b]])의 개수는?"),
    choices=["1", "2", "3", "4", "5"], derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2024년 10월 고1 16번 변형]. (x+2)²≤3−a → a≤3; a=3: P={−2}, b=1만 가능; a=1,2는 b−3≤−3 필요 → 없음 → 1개 → ① (빠른정답 없음).")

# p29
add(id="229a7f73", qtype="choice",
    question=("전체집합 [[U]]에 대하여 두 조건 '[[p]]: [[x <= 5]]', '[[q]]: [[x < 2]]'의\n진리집합을 각각 [[P]], [[Q]]라 할 때, 다음 중\n"
              "조건 '[[2 <= x <= 5]]'의 진리집합을 나타낸 것은?"),
    choices=["[[union(P, Q)]]", "[[inter(P, Q)]]", "[[union(P, comp(Q))]]", "[[inter(P, comp(Q))]]", "[[inter(comp(P), Q)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="x≤5이고 x≥2 → P∩Qᶜ → ④ (빠른정답 없음).")

# p30
add(id="32d6804d", qtype="choice",
    question=("세 다항식 [[f(x)]], [[g(x)]], [[h(x)]]에 대하여 세 조건 [[p]], [[q]], [[r]]가\n[[p]]: [[f(x) != 0]], [[q]]: [[g(x) != 0]], [[r]]: [[h(x) != 0]]이다.\n"
              "전체집합 [[U]] = { [[x]] | [[x]]는 실수 }에 대하여 세 조건 [[p]], [[q]], [[r]]의\n진리집합을 각각 [[P]], [[Q]], [[R]]라 할 때, 다음 중\n"
              "조건 '[[f(x) g(x) h(x) = 0]]'의 진리집합을 나타내는 것은?"),
    choices=["[[union(inter(comp(P), Q), R)]]", "[[inter(union(P, comp(Q)), R)]]", "[[inter(inter(P, Q), comp(R))]]",
             "[[inter(inter(comp(P), comp(Q)), comp(R))]]", "[[union(union(comp(P), comp(Q)), comp(R))]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="fgh=0 ⇔ f=0 또는 g=0 또는 h=0 ⇔ Pᶜ∪Qᶜ∪Rᶜ → ⑤ (빠른정답 없음).")

# p36
add(id="69f78304", qtype="choice",
    question=("실수 전체의 집합에서 세 조건\n[[p]]: [[x > 2]], [[q]]: [[pow(x,2) - 1 > 0]], [[r]]: [[abs(x) <= 1]]에 대하여 다음 중\n"
              "참인 명제인 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[imp(p, q)]]\nㄴ. [[imp(r, neg(p))]]\nㄷ. [[imp(neg(r), q)]]"),
    choices=CH_C, derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄱ x>2⇒x²>1 ✓, ㄴ |x|≤1⇒x≤2 ✓, ㄷ |x|>1⇒x²−1>0 ✓ → ⑤ (빠른정답 없음).")

# p44
add(id="dc708fa1", qtype="choice",
    question="다음 중 조건 [[p]], [[q]] 에 대하여 명제 [[p]]⇒[[q]] 가 거짓인\n것은? (단, [[x]], [[y]] 는 실수이다.)",
    choices=["[[p]]: [[x = 1]], [[q]]: [[pow(x,2) - 3x + 2 = 0]]",
             "[[p]]: [[pow(x,2) = 1]], [[q]]: [[abs(x) = 1]]",
             "[[p]]: [[x]], [[y]]는 홀수이다. [[q]]: [[x + y]]는 짝수이다.",
             "세 집합 [[A]], [[B]], [[C]] 에 대하여 [[p]]: [[union(A, C) = union(B, C)]], [[q]]: [[A = B]]",
             "[[p]]: [[quad(ABCD)]] 는 마름모이다. [[q]]: [[quad(ABCD)]] 는 평행사변형이다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="⇒ 기호는 텍스트. ④ A∪C=B∪C여도 A≠B 가능(반례) → 거짓 → ④. 빠른정답 '거짓'(값 아님).")

# p47
add(id="8930c983", qtype="short",
    question=("두 조건 [[p]], [[q]]에 대하여 [[f(p, q)]]를 다음과 같이 정의하자.\n"
              "[[f(p, q)]] = 1 ([[imp(p, q)]]가 참), [[-1]] ([[imp(p, q)]]가 거짓)\n"
              "실수 전체의 집합에서 정의된 세 조건 [[p]], [[q]], [[r]]가 다음과\n같을 때, [[f(p, neg(q)) + 2 × f(q, r) + 3 × f(neg(r), p)]]의\n값을 구하시오.\n"
              "[[p]]: [[x]]는 4의 배수가 아니다.\n[[q]]: [[pow(x,2)]]은 4의 배수가 아니다.\n[[r]]: [[sqrt(x)]] 는 4의 배수가 아니다."),
    choices=None, derived_answer="-2", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: 경우 나눔(조각적) 정의 f(p, q)를 텍스트로 전사",
    note="p→~q 거짓(x=1), q→r 참(√x=4k⇒x²이 4의 배수), ~r→p 거짓(x=16k²) → −1+2−3=−2 = 빠른정답 ✓.")

# p48
add(id="d149ceed", qtype="short",
    question=("두 조건 [[p]], [[q]]에 대하여 [[f(p, q)]]를 다음과 같이 정의하자.\n"
              "[[f(p, q)]] = 1 ([[imp(p, q)]]가 참), [[-1]] ([[imp(p, q)]]가 거짓)\n"
              "실수 전체의 집합에서 정의된 세 조건 [[p]], [[q]], [[r]]가 다음과\n같을 때, [[f(p, neg(q)) + 2 × f(neg(q), neg(r)) + 3 × f(r, p)]]의\n값을 구하시오.\n"
              "[[p]]: [[x]]는 3의 배수이다.\n[[q]]: [[pow(x,3)]]은 3의 배수이다.\n[[r]]: [[sqrt(x)]] 는 3의 배수이다."),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: 경우 나눔(조각적) 정의 f(p, q)를 텍스트로 전사",
    note="p→~q 거짓(x=3), ~q→~r 참(대우 r⇒q), r→p 참(x=9k²) → −1+2+3=4 (빠른정답 없음).")

# p54
add(id="649136ac", qtype="choice",
    question=("두 조건 [[p]], [[q]]가\n'[[p]]: [[-3 <= x <= 1]]', '[[q]]: [[0 <= x <= 4]]'\n일 때, 명제 '[[p]]이면 [[q]]이다.'가 거짓임을 보이는 원소의\n집합은?"),
    choices=["[[setb(x, x < -3)]]", "[[setb(x, -4 <= x < -3)]]", "[[setb(x, -3 <= x < 0)]]", "[[setb(x, 1 <= x < 4)]]", "[[setb(x, x > 4)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="반례 집합 P−Q={x | −3≤x<0} → ③ (빠른정답 없음).")

# p55
add(id="652473e2", qtype="short",
    question=("두 조건 [[p]], [[q]]의 진리집합을 각각 [[P]], [[Q]]라 하자.\n두 집합 [[P]], [[Q]]에 대하여 [[union(P, Q)]] = { [[x]] | [[x]]는 18의 양의 약수 },\n"
              "[[inter(P, Q) = set(3, 6, 9, 18)]]일 때, 명제 [[imp(p, q)]]가 거짓임을\n보여주는 모든 원소의 합은 [[a]], 명제 [[imp(q, p)]]가 거짓임을\n"
              "보여주는 모든 원소의 합은 [[b]]이다. 이때 [[a + b]]의 값을\n구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="(P−Q)∪(Q−P)={1,2} → a+b=3. 빠른정답 27과 불일치.")

# p57
add(id="180df770", qtype="short",
    question=("두 조건 [[p]], [[q]]의 진리집합을 각각 [[P]], [[Q]]라 하면\n[[union(P, Q)]] = { [[x]] | [[x]]는 20의 양의 약수 },\n"
              "[[inter(P, Q) = set(1, 4, 5, 20)]]이다. 명제 [[imp(p, q)]]가 거짓임을\n보여주는 모든 원소의 합은 [[a]], 명제 [[imp(q, p)]]가 거짓임을\n"
              "보여주는 모든 원소의 합은 [[b]]라 할 때, [[a + b]]의 값을\n구하시오."),
    choices=None, derived_answer="12", figure=None, difficulty_est=2, confidence=0.9,
    note="(P−Q)∪(Q−P)={2,10} → 12 = 빠른정답 ✓.")

# p59
add(id="8d6d2db4", qtype="choice",
    question=("전체집합 [[U]]에서 두 조건 [[p]], [[q]]의 진리집합을\n각각 [[P]], [[Q]]라 할 때, 다음 중 명제 [[imp(p, neg(q))]]가\n거짓임을 보이는 원소가 속하는 집합은?"),
    choices=["[[inter(P, Q)]]", "[[inter(P, comp(Q))]]", "[[union(P, comp(Q))]]", "[[inter(comp(P), comp(Q))]]", "[[union(comp(P), comp(Q))]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="반례: P∩(Qᶜ)ᶜ = P∩Q → ① (빠른정답 없음).")

# p60
add(id="10e33503", qtype="short",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 자연수 }에서 정의된\n두 조건 [[p]], [[q]]가 다음과 같을 때, '[[q]]이면 [[neg(p)]]이다.'가\n거짓임을 보이는 원소의 개수를 구하시오.\n"
              "[[p]]: [[sqrt(2x + 1)]] 은 자연수이다.\n[[q]]: [[x <= 150]]"),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="Q∩P: 2x+1이 홀수 제곱수(9,25,…,289), x≤150 → 8개. 빠른정답 12와 불일치.")

# p61
add(id="09c7c7d7", qtype="choice",
    question=("두 조건\n[[p]]: [[-1 <= x <= k]], [[q]]: [[x <= 0]] 또는 [[x >= 7]]\n에 대하여 명제 [[imp(neg(p), q)]]가 거짓임을 보이는 양의 정수인\n"
              "반례가 [[x = 6]]뿐일 때, 실수 [[k]]의 값의 범위는?"),
    choices=["[[k < 5]]", "[[k >= 6]]", "[[4 <= k < 5]]", "[[5 <= k < 6]]", "[[6 <= k < 7]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="반례: k<x<7인 양의 정수 x가 6뿐 → 5≤k<6 → ④ (빠른정답 없음).")

# p62 (id 2개)
dup(["40a3a779", "65f72b94"], qtype="choice",
    question=("전체집합 [[U]]에 대하여 세 조건 [[p]], [[q]], [[r]]의 진리집합을\n각각 [[P]], [[Q]], [[R]]라 하면 [[union(P, Q) = P]], [[inter(P, comp(R)) = P]]인\n"
              "관계가 성립한다. 이때 다음 보기 중 참인 것만을 있는\n대로 고른 것은?\n<보기>\nㄱ. [[imp(r, neg(p))]]\nㄴ. [[imp(neg(p), q)]]\nㄷ. [[imp(r, neg(q))]]"),
    choices=CH_D, derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="Q⊂P, P∩R=∅ → ㄱ R⊂Pᶜ ✓, ㄴ Pᶜ⊂Q ✗, ㄷ Q∩R=∅ ✓ → ④ (빠른정답 없음).")

# p65
add(id="e81d414f", qtype="choice",
    question=("전체집합 [[U]]가 실수 전체의 집합일 때, 실수 [[x]]에 대한\n두 조건 [[p]], [[q]]가 [[p]]: [[a(x + 1)(x - 3) > 0]], [[q]]: [[x < b]]이다.\n"
              "두 조건 [[p]], [[q]]의 진리집합을 각각 [[P]], [[Q]]라고 할 때,\n보기에서 옳은 것만을 있는 대로 고른 것은?\n(단, [[a]], [[b]]는 실수이다.)\n<보기>\n"
              "ㄱ. [[a = 0]]일 때, [[P = empty]] 이다.\nㄴ. [[a < 0]], [[b = 3]]일 때, [[subset(P, Q)]]이다.\nㄷ. [[a > 0]], [[b = 3]]일 때,\n명제 '[[neg(p)]]이면 [[q]]이다.'는 참이다."),
    choices=CH_B, derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="ㄱ 0>0 거짓 → P=∅ ✓, ㄴ P=(−1,3)⊂(−∞,3) ✓, ㄷ ~p: −1≤x≤3, x=3은 q 불만족 ✗ → ② (빠른정답 없음).")

# p66
add(id="dde38fc1", qtype="choice",
    question=("전체집합 [[U]]의 세 부분집합 [[P]], [[Q]], [[R]]가 각각 세 조건\n[[p]], [[q]], [[r]]의 진리집합이고 두 명제 [[imp(p, neg(q))]]와 [[imp(neg(r), q)]]가\n"
              "모두 참일 때, 다음 중 옳은 것을 보기에서 모두 고른 것은?\n<보기>\nㄱ. [[subset(P, R)]]\nㄴ. [[subset((Q - R), comp(P))]]\nㄷ. [[subset(Q, (union(comp(P), R)))]]"),
    choices=CH_D, derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="P⊂Qᶜ⊂R: ㄱ ✓, ㄴ Q−R⊂Q⊂Pᶜ ✓, ㄷ Q⊂Pᶜ ✓ → ⑤ (빠른정답 없음).")

# p67
add(id="f80b25aa", qtype="short",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 13 이하의 자연수인 홀수 }에\n대하여 조건 '[[p]]: [[pow(x,2) - 3x <= 28]]'의 진리집합을 [[P]],\n"
              "두 조건 [[q]], [[r]]의 진리집합을 각각 [[Q]], [[R]]라 하자.\n두 명제 [[imp(p, q)]]와 [[imp(neg(p), r)]]가 모두 참일 때,\n"
              "두 집합 [[Q]], [[R]]의 순서쌍 ([[Q]], [[R]])의 개수를 구하시오."),
    choices=None, derived_answer="128", figure=None, difficulty_est=3, confidence=0.9,
    note="P={1,3,5,7}, Pᶜ={9,11,13}; P⊂Q 2³, Pᶜ⊂R 2⁴ → 128 = 빠른정답 ✓.")

# p70
add(id="871c6e23", qtype="choice",
    question=("실수 [[x]]에 대한 세 조건\n[[p]]: [[abs(x) <= 2]],\n[[q]]: [[pow(x,2) - 4 < 0]],\n[[r]]: [[x > 2]]\n"
              "에 대하여 보기에서 참인 명제만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[imp(p, q)]]\nㄴ. [[imp(p, neg(r))]]\nㄷ. [[imp(r, neg(q))]]"),
    choices=CH_A, derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2016년 6월 고3 문과 16번 변형]. ㄱ x=2 반례 ✗, ㄴ ✓, ㄷ ✓ → ④ (빠른정답 없음).")

# p71
add(id="ded92181", qtype="choice",
    question=("전체집합 [[U]]에서 두 조건 [[p]], [[q]]를 만족시키는 집합을 각각\n[[P]], [[Q]]라 하자. 명제 '[[p]]이면 [[neg(q)]]이다.'가 참일 때, 다음 중\n옳은 것은?"),
    choices=["[[subset(P, Q)]]", "[[subset(Q, P)]]", "[[P - Q = P]]", "[[subset(comp(Q), P)]]", "[[union(P, comp(Q)) = U]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="P⊂Qᶜ ⇔ P∩Q=∅ ⇔ P−Q=P → ③ (빠른정답 없음).")

# p72
add(id="4e937773", qtype="choice",
    question=("세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각 [[P]], [[Q]], [[R]]라 하고,\n벤다이어그램으로 나타내면 아래 그림과 같다. 다음 보기의\n"
              "명제 중 항상 참인 명제만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[imp(p, r)]]\nㄴ. [[p]]→([[r]] 또는 [[q]])\nㄷ. ([[neg(r)]] 이고 [[neg(q)]])→[[neg(p)]]"),
    choices=CH_C, derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "벤다이어그램: 전체집합 U 안에 두 원 R(왼쪽), Q(오른쪽)가 일부 겹치고, 가로로 긴 타원 P가 R∪Q 안에서 R와 Q에 걸쳐 놓임"}}],
    difficulty_est=2, confidence=0.8, needs_review="도형 표현 불가: 벤다이어그램(포함 관계가 그림에만 있음)",
    note="그림: P⊂R∪Q, P⊄R → ㄱ ✗, ㄴ ✓, ㄷ ㄴ의 대우 ✓ → ④ (빠른정답 없음).")

# p73
add(id="bba8c567", qtype="choice",
    question="전체집합 [[U]]에서 두 조건 [[p]], [[q]]의 진리집합을 각각 [[P]], [[Q]]라\n하자. 명제 [[imp(p, neg(q))]]가 참일 때, 다음 중 항상 옳은 것은?",
    choices=["[[union(P, Q) = Q]]", "[[inter(P, Q) = empty]]", "[[union(comp(P), Q) = U]]", "[[inter(comp(P), Q) = empty]]", "[[inter(comp(P), comp(Q)) = U]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="P⊂Qᶜ ⇔ P∩Q=∅ → ② (빠른정답 없음).")

# p78
add(id="cf9df772", qtype="short",
    question=("전체집합 [[U = set(1, 2, 3, 4, 5)]]의 공집합이 아닌\n두 부분집합 [[A]], [[B]]에 대하여 두 명제 '집합 [[A]]의 모든 원소\n"
              "[[x]]에 대하여 [[4 pow(x,2) - 12x + 5 < 0]]이다.'\n'집합 [[B]]의 어떤 원소 [[x]]에 대하여 [[in(x, A)]]이다.'가 있다.\n"
              "두 명제가 모두 참이 되도록 하는 두 집합 [[A]], [[B]]의 모든\n순서쌍 ([[A]], [[B]])의 개수를 구하시오."),
    choices=None, derived_answer="56", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2018년 3월 고3 문과 29번 변형]. 1/2<x<5/2 → A⊂{1,2}; A∩B≠∅인 B: 16+16+24=56(전수 확인). 빠른정답 '거짓'(값 아님).")

# p83
add(id="d0fef5f1", qtype="short",
    question=("전체집합 [[U = set(1, 2, 3, 4, 5)]]의 공집합이 아닌\n두 부분집합 [[A]], [[B]]에 대하여 두 명제\n"
              "'집합 [[A]]의 모든 원소 [[x]]에 대하여 [[pow(x,2) - 5x + 4 < 0]]이다.'\n'집합 [[B]]의 어떤 원소 [[x]]에 대하여 [[in(x, A)]]이다.'\n"
              "가 있다. 두 명제가 모두 참이 되도록 하는 두 집합 [[A]], [[B]]의\n모든 순서쌍 ([[A]], [[B]])의 개수를 구하시오."),
    choices=None, derived_answer="56", figure=None, difficulty_est=3, confidence=0.9,
    note="1<x<4 → A⊂{2,3}; A∩B≠∅인 B: 16+16+24=56(전수 확인). 빠른정답 '참'(값 아님).")

# p84
add(id="96f77167", qtype="short",
    question=("전체집합 [[U]]에 대하여 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각\n[[P]], [[Q]], [[R]]라 할 때, 다음은 세 집합 [[P]], [[Q]], [[R]]의 관계를\n나타낸 것이다.\n"
              "(가) 모든 [[in(x, P)]]에 대하여 [[in(x, comp(Q))]]이다.\n(나) 어떤 [[in(x, Q)]]에 대하여 [[in(x, comp(R))]]이다.\n"
              "다음 보기 중 항상 참인 명제인 것만을 있는 대로 고르시오.\n<보기>\nㄱ. [[imp(neg(p), r)]]\nㄴ. [[imp(q, neg(p))]]\nㄷ. [[imp(neg(r), q)]]"),
    choices=None, derived_answer="ㄴ", figure=None, difficulty_est=2, confidence=0.9,
    note="(가) P∩Q=∅, (나) Q⊄R → ㄴ Q⊂Pᶜ만 항상 참 → ㄴ. 빠른정답 '거짓'(값 아님).")

# p85
add(id="4597c729", qtype="short",
    question=("전체집합 [[U = set(1, 2, 3, 4, 5, 6, 7, 8)]]의 공집합이 아닌\n두 부분집합 [[A]], [[B]]에 대하여 두 명제\n"
              "'집합 [[A]]의 모든 원소 [[x]]에 대하여\n[[pow(x,2) - 13x + 40 < 0]]이다.'\n'집합 [[B]]의 어떤 원소 [[x]]에 대하여 [[in(x, A)]]이다.'\n"
              "가 있다. 두 명제가 모두 참이 되도록 하는 두 집합 [[A]], [[B]]의\n모든 순서쌍 ([[A]], [[B]])의 개수를 구하시오."),
    choices=None, derived_answer="448", figure=None, difficulty_est=3, confidence=0.9,
    note="5<x<8 → A⊂{6,7}; A∩B≠∅인 B: 128+128+192=448(전수 확인) (빠른정답 없음).")

# p87
add(id="3c74b364", qtype="short",
    question=("전체집합 [[U]]에 대하여 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각\n[[P]], [[Q]], [[R]]라 할 때, 다음은 세 집합 [[P]], [[Q]], [[R]]의 관계를\n나타낸 것이다.\n"
              "(가) 모든 [[in(x, P)]]에 대하여 [[notin(x, R)]]이다.\n(나) 어떤 [[in(x, Q)]]에 대하여 [[notin(x, R)]]이다.\n"
              "다음 보기 중 항상 참인 명제인 것만을 있는 대로 고르시오.\n<보기>\nㄱ. [[imp(p, neg(q))]]\nㄴ. [[imp(neg(q), r)]]\nㄷ. [[imp(r, neg(p))]]"),
    choices=None, derived_answer="ㄷ", figure=None, difficulty_est=2, confidence=0.9,
    note="(가) P∩R=∅, (나) Q⊄R → ㄷ R⊂Pᶜ만 항상 참 → ㄷ. 빠른정답 '도'(값 아님).")

# p95
add(id="dca1e1e3", qtype="short",
    question=("세 조건 [[p]]: [[x > a]], [[q]]: [[-1 < x <= 3]] 또는 [[x > 6]], [[r]]:\n[[x > b]]에 대하여 두 명제 [[imp(q, p)]], [[imp(r, q)]]가 참이 되도록 하는\n"
              "[[a]]의 최댓값과 [[b]]의 최솟값의 합을 구하시오."),
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="Q⊂P → a≤−1, R⊂Q → b≥6 → −1+6=5. 빠른정답 14와 불일치.")

# p97
add(id="363d131d", qtype="short",
    question=("실수 [[x]]에 대하여 세 조건 [[p]], [[q]], [[r]]가\n[[p]]: [[x < frac(a - 2, 3)]], [[q]]: [[5x - 1 = 29]], [[r]]: [[pow(x,2) - 7x + 10 = 0]]\n"
              "일 때, 명제 [[imp(q, p)]]는 거짓이고, 명제 [[imp(r, p)]]는 참이 되도록\n하는 정수 [[a]]의 개수를 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="Q={6}, R={2,5}: 6≥(a−2)/3 → a≤20, 5<(a−2)/3 → a>17 → 18,19,20 → 3 = 빠른정답 ✓.")

# p99 (한 이미지에 별개 문항 2개; draft_a 대응대로 분리) — 위쪽 문항(좌표평면)
add(id="62526bab", qtype="short",
    question=("좌표평면 위에 두 점 [[A(3, 3)]], [[B(-5, -1)]]과\n직선 [[l]]: [[y = 2x + k]]가 있다. 명제 '직선 [[l]] 위의 어떤\n"
              "점 P에 대하여 [[angle(APB) = deg(90)]]이다.'가 참이 되도록\n하는 정수 [[k]]의 개수를 구하시오.\n(단, 점 P는 두 점 A, B가 아니다.)"),
    choices=None, derived_answer="21", figure=None, difficulty_est=3, confidence=0.85,
    note="p99 이미지 위쪽 문항. AB를 지름으로 하는 원(중심 (−1,1), r=2√5)과 직선이 만나야 함: |k−3|/√5≤2√5 → −7≤k≤13 → 21개(접점은 A, B 아님). 빠른정답 3과 불일치.")

# p99 — 아래쪽 문항(세 조건)
add(id="0369e2a2", qtype="short",
    question=("세 조건 [[p]], [[q]], [[r]]가 [[p]]: [[-3 <= x <= 3]] 또는 [[x >= 4]],\n[[q]]: [[a <= x <= 2]], [[r]]: [[x >= b]]일 때, 두 명제 [[imp(q, p)]], [[imp(p, r)]]가\n"
              "모두 참이 되도록 하는 상수 [[a]]의 최솟값과 상수 [[b]]의\n최댓값의 곱을 구하시오."),
    choices=None, derived_answer="9", figure=None, difficulty_est=2, confidence=0.9,
    note="p99 이미지 아래쪽 문항. Q⊂P → a≥−3, P⊂R → b≤−3 → (−3)(−3)=9. 빠른정답 3과 불일치.")

# ================= 260828_원의 방정식과 그래프 =================
# p5
add(id="54352276", qtype="short",
    question=("평면 위에 반지름의 길이가 [[2 sqrt(10)]]인 원 O가 있다.\n그림은 원 O 위의 두 점 A, C와 원 내부의 점 B를\n"
              "잡아 [[seg(AB) = 8]], [[seg(BC) = 4]], [[angle(ABC) = deg(90)]]가 되도록\n원과 원의 내부의 일부를 잘라낸 도형이다.\n"
              "[[seg(OB) = l]]이라 할 때, [[3 pow(l,2)]]의 값을 구하시오."),
    choices=None, derived_answer="24",
    figure=[{"fn": "unsupported", "args": {"raw": "반지름 2√10인 원 O에서 원 위의 점 A(위쪽)·C, 내부의 점 B(A 바로 아래, ∠ABC=90°)로 AB=8, BC=4인 부분을 잘라낸 도형; 중심 O는 AB의 왼쪽, OA 점선(2√10), AB·BC 점선 표시"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 원의 일부를 잘라낸 도형 그림",
    note="출처 [2010년 11월 고1 30번]. B 원점, A(0,8), C(4,0): O=(2y−6, y), y²−8y+12=0 → O=(−2,2)(내부 조건) → l²=8 → 24. 빠른정답 108과 불일치.")

# p30
add(id="015b5ab3", qtype="short",
    question=("그림과 같이 원의 중심 [[C(a, b)]]가 제1사분면 위에 있고,\n반지름의 길이가 [[r]]이며 원점 O를 지나는 원이 있다.\n"
              "원과 [[x]]축, [[y]]축이 만나는 점 중 O가 아닌 점을\n각각 A, B라 하자. 네 점 O, A, B, C가 다음 조건을\n만족시킬 때, [[a + b + pow(r,2)]]의 값을 구하시오.\n"
              "(가) [[seg(OB) - seg(OA) = 4]]\n(나) 두 점 O, C를 지나는 직선의 방정식은\n[[y = 3x]]이다."),
    choices=None, derived_answer="14",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O를 지나는 원(중심 C, 제1사분면), x축과의 교점 A, y축과의 교점 B, O와 C를 지나는 직선 y=3x"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 원과 직선 그림",
    note="출처 [2021년 9월 고1 28번/4점]. A(2a,0), B(0,2b), b=3a, 2b−2a=4 → a=1, b=3, r²=10 → 14. 빠른정답 2와 불일치.")

# p42
add(id="f1088997", qtype="choice",
    question="원 [[pow(x,2) + pow(y,2) - 2x - 4a y + b = 0]] 이 점 [[point(-3, 4)]] 를\n지나고, [[x]] 축에 접하도록 [[a]], [[b]] 의 값을 정할 때,\n[[a + b]] 의 값은?",
    choices=["1", "2", "3", "4", "5"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="중심 (1,2a), r²=1+4a²−b=4a² → b=1; 대입 31−16a+1=0 → a=2 → 3 → ③. 빠른정답 5와 불일치.")

# p66
add(id="ee6c6ec3", qtype="short",
    question=("두 점 [[A(9, 0)]], [[B(0, 12)]]에 대하여\n[[ratio(seg(AP), seg(BP)) = ratio(1, 2)]]를 만족시키는 점 P가 있다.\n"
              "세 점 A, B, P를 꼭짓점으로 하는\n삼각형 ABP의 넓이의 최댓값을 구하시오."),
    choices=None, derived_answer="75", figure=None, difficulty_est=3, confidence=0.9,
    note="아폴로니우스 원 (x−12)²+(y+4)²=100, 중심이 직선 AB 위 → 높이 최대 10, AB=15 → 75. 빠른정답 15와 불일치(다음 문항 빠른정답이 75).")

# p69
add(id="5b18e889", qtype="choice",
    question=("다음 그림과 같이 두 점 [[A(-4, 0)]], [[B(1, 0)]]과\n제1사분면 위의 점 C를 꼭짓점으로 하는\n"
              "삼각형 ABC에서 [[angle(C)]]의 이등분선이 원점 O를 지날\n때, 점 C가 나타내는 도형의 길이는?"),
    choices=["[[pi]]", "[[frac(4,3) pi]]", "[[frac(5,3) pi]]", "[[2 pi]]", "[[frac(7,3) pi]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: x축 위의 점 A(−4,0), B(1,0), 제1사분면의 점 C, 삼각형 ABC와 C에서 원점 O로 그은 ∠C의 이등분선(같은 각 표시)"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 삼각형과 각의 이등분선 그림",
    note="CA:CB=AO:OB=4:1 → 아폴로니우스 원 (x−4/3)²+y²=16/9의 제1사분면 반원 → 길이 4π/3 → ②. 빠른정답 75와 불일치.")

# p72
add(id="a721d7c3", qtype="short",
    question=("두 점 [[A(-3, 0)]], [[B(3, 0)]]에 대하여 점 [[P(a, b)]]가\n[[pow(seg(PA), 2) + pow(seg(PB), 2) = 26]]을 만족시킬 때,\n"
              "[[pow(a - 3, 2) + pow(b + 4, 2)]]의 최댓값을 구하시오."),
    choices=None, derived_answer="49", figure=None, difficulty_est=2, confidence=0.9,
    note="a²+b²=4, (3,−4)까지 거리 최대 5+2=7 → 49 = 빠른정답 ✓.")

# p73
add(id="1c87c9cb", qtype="choice",
    question="두 점 [[A(-4, 0)]], [[B(4, 0)]]에 대하여\n[[pow(seg(PA), 2) + pow(seg(PB), 2) = 40]]을 만족시키는 점 P의 자취의\n방정식은?",
    choices=["[[x = 2]]", "[[x = 4]]", "[[pow(x,2) + pow(y,2) = 2]]", "[[pow(x,2) + pow(y,2) = 4]]", "[[pow(x,2) + pow(y,2) = 8]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="2x²+2y²+32=40 → x²+y²=4 → ④ = 빠른정답 ✓.")
