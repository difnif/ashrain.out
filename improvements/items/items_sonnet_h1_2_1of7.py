# -*- coding: utf-8 -*-
# esc_sonnet_h1-2_1of7 — 이미지 기준 전사 (84 항목 / 80쪽)
# 문서: 260828_두 집합 사이의 포함관계 (77 id) + 260828_점과 직선 사이의 거리 (7 id)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_ABC = ["[[A]] ⊂ [[B]] ⊂ [[C]]", "[[A]] ⊂ [[C]] ⊂ [[B]]", "[[B]] ⊂ [[A]] ⊂ [[C]]", "[[B]] ⊂ [[C]] ⊂ [[A]]", "[[C]] ⊂ [[B]] ⊂ [[A]]"]
CH_4 = ["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄹ", "ㄴ, ㄷ, ㄹ"]
CH_PAIR = ["ㄱ, ㄷ", "ㄱ, ㄹ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ"]
CH_3A = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_3B = ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_3C = ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ---------------- 기호 ∈, ⊂의 사용 ----------------
add(id="724adb57", qtype="choice",
    question="두 집합 [[A = set(1, 3, 5)]], [[B]] = { [[x]] | [[x]]는 10 미만의 소수 }에 대하여 다음 중 옳지 않은 것은?",
    choices=["[[in(1, A)]]", "[[in(2, B)]]", "[[subset(set(1, 3), B)]]", "[[subset(set(3, 5), A)]]", "[[subset(set(2, 3), B)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="B={2,3,5,7}, 1∉B → ③ = 빠른정답 ✓.")

add(id="6e917653", qtype="choice",
    question="두 집합 [[A = set(1, 3, 4)]], [[B]] = { [[x]] | [[x]]는 6의 약수 }에 대하여 다음 중 옳은 것을 모두 고르면? (정답 2개)",
    choices=["[[in(3, A)]]", "[[notin(1, B)]]", "[[in(empty, B)]]", "[[in(set(1), A)]]", "[[subset(set(1, 2, 3, 6), B)]]"],
    derived_answer="①, ⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="B={1,2,3,6}: ①✓ ⑤✓ → ①, ⑤ (빠른정답 '1, 5'와 같은 뜻).")

add(id="60208df1", qtype="choice",
    question="두 집합 [[A]], [[B]]를 벤다이어그램으로 나타내면 아래 그림과 같을 때, 다음 중 옳지 않은 것은?",
    choices=["[[subset(empty, A)]]", "[[in(3, B)]]", "[[notin(4, A)]]", "[[subset(set(4, 5), A)]]", "[[nsubset(set(2, 3, 5), B)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "벤다이어그램: 큰 원 A 안에 작은 원 B. B 안에 3, 5, 4; A에서 B 밖에 1, 2, 6 (A={1,2,3,4,5,6}, B={3,4,5})"}}],
    difficulty_est=1, confidence=0.8, needs_review="도형 표현 불가: 원소가 표시된 벤다이어그램(문항 정보 전부가 그림에 있음)",
    note="4∈A이므로 ③ 거짓 → ③ = 빠른정답 ✓.")

add(id="6ccb0b71", qtype="choice",
    question=("집합 [[A]] = { [[x]] | [[x]]는 14의 약수 }에 대하여 다음 보기 중 옳은 것의 개수는?\n보기\n"
              "㉠ [[in(2, A)]]\n㉡ [[in(set(14), A)]]\n㉢ [[in(set(4), A)]]\n㉣ [[subset(empty, A)]]\n㉤ [[card(A) = 4]]\n㉥ [[subset(set(1, 2, 7, 12, 14), A)]]"),
    choices=["0개", "1개", "2개", "3개", "4개"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.85,
    note="A={1,2,7,14}: ㉠㉣㉤ 참 → 3개 = ④. 빠른정답 '3'은 개수 3과는 맞으나 선지 번호는 ④.")

add(id="621beeaf", qtype="choice",
    question="5의 양의 배수의 집합을 [[A]], 9의 양의 약수의 집합을 [[B]]라 할 때, 다음 중 옳은 것은?",
    choices=["[[in(1, A)]]", "[[notin(3, B)]]", "[[notin(5, A)]]", "[[in(7, B)]]", "[[notin(9, A)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="B={1,3,9}; 9는 5의 배수가 아님 → ⑤. 빠른정답 3과 불일치.")

add(id="313959ea", qtype="choice",
    question="두 집합 [[A]], [[B]]를 벤다이어그램으로 나타내면 아래 그림과 같을 때, 다음 중 옳지 않은 것은?",
    choices=["[[subset(empty, B)]]", "[[subset(set(9), A)]]", "[[notin(7, A)]]", "[[notin(2, B)]]", "[[in(8, A)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "벤다이어그램: 큰 원 A 안에 작은 원 B. B 안에 7, 9; A에서 B 밖에 8, 2, 5 (A={2,5,7,8,9}, B={7,9})"}}],
    difficulty_est=1, confidence=0.8, needs_review="도형 표현 불가: 원소가 표시된 벤다이어그램(문항 정보 전부가 그림에 있음)",
    note="7∈B⊂A → ③ 거짓 = 빠른정답 ✓.")

add(id="623146c3", qtype="choice",
    question=("모든 원소가 자연수인 집합 [[A]]가 다음 조건을 만족시킨다.\n(가) [[in(2, A)]], [[in(5, A)]]\n"
              "(나) [[in(x, A)]]인 [[x]]에 대하여 [[4x <= 99]]이면 [[in(4x, A)]]이다.\n집합 [[A]]의 모든 원소의 합의 최솟값은?"),
    choices=["[[139]]", "[[141]]", "[[143]]", "[[145]]", "[[147]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="{2,8,32,5,20,80} 합 147 → ⑤ = 빠른정답 ✓.")

# ---------------- 집합 사이의 포함 관계 ----------------
add(id="e420f083", qtype="choice",
    question=("두 집합 [[A]], [[B]]에 대하여\n[[A]] = { [[x]] | [[x]]는 10보다 작은 자연수 },\n"
              "[[B]] = { [[x]] | [[x]]는 9 이하의 홀수 }일 때, 다음 중 옳은 것은?"),
    choices=["[[in(10, A)]]", "[[notin(9, A)]]", "[[subset(A, B)]]", "[[subset(set(3), B)]]", "[[A = B]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="B={1,3,5,7,9}⊂A; ④만 참 = 빠른정답 ✓.")

add(id="b7718152", qtype="choice",
    question="두 집합 [[A = set(3, 7)]], [[B = set(3, 5, 7)]]에 대하여 다음 중 옳은 것을 모두 고르면? (정답 2개)",
    choices=["[[subset(7, B)]]", "[[subset(set(3), A)]]", "[[in(set(3, 5), B)]]", "[[notin(5, A)]]", "[[in(B, A)]]"],
    derived_answer="②, ④", figure=None, difficulty_est=1, confidence=0.9,
    note="②✓ ④✓ → ②, ④ (빠른정답 '2, 4'와 같은 뜻).")

add(id="ef0e5fed", qtype="choice",
    question=("두 집합\n[[A]] = { [[x]] | [[x]]는 18의 양의 약수 }\n[[B]] = { [[x]] | [[x]]는 36의 양의 약수 }\n에 대하여 다음 중 옳은 것은?"),
    choices=["[[in(5, A)]]", "[[nsubset(set(2, 3, 4), B)]]", "[[subset(A, B)]]", "[[card(A) > card(B)]]", "[[card(B) - card(A) = 2]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="n(A)=6, n(B)=9, A⊂B → ③. 빠른정답 4와 불일치.")

add(id="fb9f8445", qtype="choice",
    question=("세 집합\n[[A = set(0, 1, 2)]],\n[[B]] = { [[x - y]] | [[in(x, A)]], [[in(y, A)]] },\n"
              "[[C]] = { [[-x + 2y]] | [[in(x, A)]], [[in(y, A)]] }\n사이의 포함 관계를 바르게 나타낸 것은?"),
    choices=CH_ABC, derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="B={-2,…,2}, C={-2,…,4} → A⊂B⊂C → ①. 빠른정답 '2, 4'와 불일치. 포함 연쇄 A⊂B⊂C는 ⊂를 텍스트로 둠.")

add(id="1138272b", qtype="choice",
    question=("세 집합\n[[A]] = {1, 2, 3, ⋯, 7},\n[[B]] = { [[x]] | [[x]]는 9보다 작은 홀수 },\n"
              "[[C]] = { [[x]] | [[x = 2n + 1]], [[n]] = 0, 1 }\n에 대하여 [[A]], [[B]], [[C]] 사이의 포함관계를 바르게 나타낸 것은?"),
    choices=["[[C]] ⊂ [[A]] ⊂ [[B]]", "[[A]] ⊂ [[B]] ⊂ [[C]]", "[[B]] ⊂ [[A]] ⊂ [[C]]", "[[C]] ⊂ [[B]] ⊂ [[A]]", "[[A]] ⊂ [[C]] ⊂ [[B]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="B={1,3,5,7}, C={1,3} → C⊂B⊂A → ④. 빠른정답 5와 불일치.")

add(id="94dda10d", qtype="choice",
    question=("세 집합\n[[A = set(0, 1, 2)]],\n[[B]] = { [[-x + 2y]] | [[in(x, A)]], [[in(y, A)]] },\n"
              "[[C]] = { [[x + y]] | [[in(x, A)]], [[in(y, A)]] }\n사이의 포함 관계를 바르게 나타낸 것은?"),
    choices=CH_ABC, derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="B={-2,…,4}, C={0,…,4} → A⊂C⊂B → ②. 빠른정답 3과 불일치.")

# ---------------- 포함 관계가 성립하도록 하는 상수 ----------------
add(id="0d04b4c1", qtype="short",
    question="두 집합 [[A = set(-2, pow(a,2) + 2)]], [[B = set(1, a - 1, 2 - a)]]에 대하여 [[subset(A, B)]]일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.9,
    note="a=-1(A={-2,3}⊂{1,-2,3}) ✓, a=4는 18∉B → -1 = 빠른정답 ✓.")

add(id="3d79acc0", qtype="short",
    question="두 집합 [[A = setb(x, 2 <= x < 5)]],\n[[B = setb(x, a < x < 2a + 7)]]에 대하여 [[subset(A, B)]]가 성립할 때, 정수 [[a]]의 개수를 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="a<2, 2a+7≥5 → -1≤a<2 → 정수 3개. 빠른정답 4와 불일치.")

add(id="26a6cb2d", qtype="short",
    question="두 집합 [[A = setb(x, -1 < x <= 9)]],\n[[B = setb(x, a + 1 <= x <= 2a + 3)]]에 대하여 [[subset(B, A)]]가 성립할 때, 상수 [[a]]의 최댓값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="a+1>-1, 2a+3≤9 → a≤3 → 최댓값 3. 빠른정답 2와 불일치.")

add(id="b0f96770", qtype="short",
    question="두 집합 [[A = setb(x, pow(x,2) + 2x - 8 = 0)]],\n[[B]] = { [[x]] | [[x]]는 [[a]]보다 큰 정수 }에 대하여 [[subset(A, B)]]를 만족시키는 정수 [[a]]의 최댓값을 구하시오.",
    choices=None, derived_answer="-5", figure=None, difficulty_est=2, confidence=0.9,
    note="A={-4,2}, a<-4 → 최댓값 -5. 빠른정답 '- 1'과 불일치(p23 자리의 빠른정답이 -5).")

add(id="ede646fa", qtype="short",
    question="두 집합 [[A = setb(x, -1 <= x < 2)]],\n[[B = setb(x, a - 2 < x < b + 1)]]에 대하여 [[subset(A, B)]]일 때, 정수 [[a]]의 최댓값과 정수 [[b]]의 최솟값의 합을 구하시오.",
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.9,
    note="a-2<-1 → a≤0, b+1≥2 → b≥1 → 0+1=1. 빠른정답 3과 불일치.")

add(id="dc927bb3", qtype="short",
    question="두 집합 [[A = setb(x, -3 < x <= 4)]],\n[[B = setb(x, a - 1 < x < b + 1)]]에 대하여 [[subset(A, B)]]일 때, 정수 [[a]]의 최댓값과 정수 [[b]]의 최솟값의 합을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="a-1≤-3 → a≤-2, b+1>4 → b≥4 → -2+4=2. 빠른정답 3과 불일치.")

add(id="5e935715", qtype="short",
    question=("자연수 [[n]]에 대하여 자연수 전체의 집합의 부분집합 [[sub(A,n)]]에 대하여 [[sub(A,n)]] = { [[x]] | [[x]]는 [[sqrt(n)]] 이하의 짝수 }라 할 때, "
              "[[subset(sub(A,n), sub(A,36))]]을 만족시키는 자연수 [[n]]의 최댓값을 구하시오."),
    choices=None, derived_answer="63", figure=None, difficulty_est=2, confidence=0.9,
    note="A₃₆={2,4,6}; √n<8 → n≤63. 빠른정답 '-5'와 불일치(옆 문항 p26의 빠른정답이 63).")

add(id="2deb3918", qtype="short",
    question="두 집합 [[A = setb(x, pow(x,2) + 5x - 24 = 0)]],\n[[B]] = { [[x]] | [[x]]는 [[k]]보다 작은 정수 }에 대하여 [[subset(A, B)]]를 만족시키는 정수 [[k]]의 최솟값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="A={-8,3}, k>3 → 최솟값 4. 빠른정답 1과 불일치.")

add(id="633ae180", qtype="short",
    question="집합 [[A]] = { [[3m + 10n]] | [[m]], [[n]]은 음이 아닌 정수 }에 대하여 {[[k]], [[k + 1]], [[k + 2]], ⋯} ⊂ [[A]]가 성립하기 위한 [[k]]의 최솟값을 구하시오.",
    choices=None, derived_answer="18", figure=None, difficulty_est=3, confidence=0.9,
    note="3·10-3-10=17은 표현 불가, 18 이상 전부 가능 → 18. 빠른정답 2와 불일치. 줄임표 집합은 텍스트.")

# ---------------- 집합을 원소로 가지는 집합 ----------------
add(id="87ec810a", qtype="choice",
    question=("집합 [[A = set(1, 2, 3, 4, 5)]]에 대하여 집합 [[P]]를\n[[P]] = { [[X]] | [[subset(X, A)]], [[card(X) = 2]] }라 하자. "
              "[[in(B, P)]], [[in(C, P)]]이고 [[card(union(B, C)) = 3]]인 두 집합 [[B]], [[C]]의 모든 순서쌍 ([[B]], [[C]])의 개수는?"),
    choices=["[[50]]", "[[60]]", "[[70]]", "[[80]]", "[[90]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="|B∩C|=1: 10×(2×3)=60 → ②. 빠른정답 63과 불일치.")

add(id="3e30b11c", qtype="choice",
    question="집합 [[A = set(1, 2, empty, set(1, 2))]]에 대하여 다음 중 옳지 않은 것은?",
    choices=["[[notin(set(1, 2), A)]]", "[[subset(empty, A)]]", "[[in(empty, A)]]", "[[subset(A, A)]]", "[[in(1, A)]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="{1,2}∈A → ① 거짓 = 빠른정답 ✓.")

add(id="f773d8b5", qtype="choice",
    question="집합 [[A = set(empty, 1, 2, set(1, 2))]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[in(empty, A)]]", "[[subset(empty, A)]]", "[[in(set(1), A)]]", "[[in(set(1, 2), A)]]", "[[subset(set(1, 2), A)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="{1}∉A → ③. 빠른정답 4와 불일치.")

add(id="55968057", qtype="choice",
    question="집합 [[A = set(empty, 1, set(3, 5), 5)]]에 대하여 다음 중 옳지 않은 것은?",
    choices=["[[subset(empty, A)]]", "[[in(1, A)]]", "[[in(set(3, 5), A)]]", "[[subset(set(1, 5), A)]]", "[[subset(set(3), A)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="3∉A → ⑤ 거짓. 빠른정답 2와 불일치.")

add(id="2dd231d4", qtype="choice",
    question="집합 [[A = set(a, set(b, c), c)]]에 대하여 다음 중 옳은 것은?",
    choices=["[[subset(set(a, b, c), A)]]", "[[subset(set(b, c), A)]]", "[[in(set(a, c), A)]]", "[[in(set(set(b, c), c), A)]]", "[[subset(empty, A)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="b∉A, {{b,c},c}는 부분집합이지 원소 아님 → ⑤만 참. 빠른정답 1과 불일치.")

add(id="0f905a60", qtype="choice",
    question=("집합 [[A = set(empty, 1, 2, set(1, 2))]]에 대하여 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[in(empty, A)]]\nㄴ. [[subset(empty, A)]]\nㄷ. [[in(set(1), A)]]\nㄹ. [[subset(set(1, 2), A)]]"),
    choices=CH_4, derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="ㄱㄴㄹ 참 → ④ = 빠른정답 ✓.")

add(id="1fb42413", qtype="choice",
    question=("집합 [[A = set(empty, 0, 1, set(0, 1))]]에 대하여 다음 보기 중 옳은 것의 개수는?\n<보기>\n"
              "ㄱ. [[in(empty, A)]]\nㄴ. [[subset(empty, A)]]\nㄷ. [[subset(set(empty), A)]]\nㄹ. [[in(set(0), A)]]\nㅁ. [[subset(set(0, 1), A)]]\nㅂ. [[subset(set(set(0, 1)), A)]]"),
    choices=["[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄹ만 거짓 → 5개 = ④. 빠른정답 '5'는 개수 5와는 맞으나 선지 번호는 ④.")

add(id="fcfb27b8", qtype="choice",
    question="집합 [[A = set(empty, 1, 2, set(2, 3), 3)]]에 대하여 다음 중 옳지 않은 것은?",
    choices=["[[subset(empty, A)]]", "[[in(empty, A)]]", "[[in(set(1, 2), A)]]", "[[in(set(2, 3), A)]]", "[[subset(set(2, 3), A)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="{1,2}∉A → ③. 빠른정답 5와 불일치.")

add(id="7b0848ae", qtype="choice",
    question="집합 [[A = set(empty, 1, 2, set(1, 3))]]에 대하여 다음 중 옳지 않은 것은?",
    choices=["[[in(empty, A)]]", "[[in(1, A)]]", "[[subset(set(2), A)]]", "[[subset(set(2, 3), A)]]", "[[in(set(1, 3), A)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="3∉A → ④ 거짓 = 빠른정답 ✓.")

add(id="2dac8257", qtype="choice",
    question=("집합 [[A = set(1, 2, set(2))]]에 대하여\n[[P(A) = setb(X, subset(X, A))]]로 정의할 때,\n다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[in(empty, P(A))]]\nㄴ. [[in(set(1, set(2)), P(A))]]\nㄷ. [[subset(set(set(2)), P(A))]]"),
    choices=CH_3A, derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄱ✓ ㄴ✓({1,{2}}⊂A) ㄷ✓({2}⊂A이므로 {2}∈P(A)) → ⑤. 빠른정답 4와 불일치.")

# ---------------- 부분집합 ----------------
add(id="17a92006", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 25 이하의 자연수 }의 부분집합 [[A]]가 다음 조건을 만족시킨다.\n"
              "(가) 집합 [[A]]의 모든 원소 [[a]]에 대하여 [[notin(3a, A)]]이다.\n(나) 집합 [[A]]의 모든 원소의 합은 짝수이다.\n"
              "집합 [[A]]의 원소의 개수가 최대일 때, 모든 원소의 합의 최댓값은?"),
    choices=["[[274]]", "[[280]]", "[[286]]", "[[292]]", "[[298]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2019년 3월 고3 문과 20번 변형]. 사슬 {1,3,9},{2,6,18},{4,12},{5,15},{7,21},{8,24}: 최대 19개, 합 최대 292(짝수) → ④(전수 확인). 빠른정답 3과 불일치.")

add(id="32da0ae6", qtype="choice",
    question=("집합 [[A = set(-1, 0, 3)]]의 서로 다른 8개의 부분집합을 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A,8)]]이라 하자. "
              "집합 [[sub(A,1)]]의 모든 원소의 합을 [[sub(a,1)]], 집합 [[sub(A,2)]]의 모든 원소의 합을 [[sub(a,2)]], ⋯, 집합 [[sub(A,8)]]의 모든 원소의 합을 [[sub(a,8)]]이라 할 때, "
              "[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,8)]]의 값은?"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="각 원소가 4번씩 → 4×2=8 → ③. 빠른정답 4와 불일치.")

dup(["0dc6852b", "460e3796"], qtype="choice",
    question=("두 자연수 [[a]], [[b]]의 최소공배수를 [[L(a, b)]]라 하자. 집합 [[U]] = { [[x]] | [[x]]는 100 이하의 자연수 }의 부분집합 [[sub(A,k)]]([[n]])을 "
              "[[sub(A,k)]]([[n]]) = { [[x]] | [[L(n, x) = k]] } ([[k]], [[n]]은 자연수)라 할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[12]] ∈ [[sub(A,24)]](8)\nㄴ. [[sub(A,20)]](2) = [[sub(A,20)]](4)\nㄷ. 집합 [[sub(A,36)]](12)의 모든 원소의 합은 63이다."),
    choices=CH_3B, derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: 첨자 함수 A_k(n) 적용 표기를 텍스트 혼합으로 전사",
    note="같은 쪽에 id 2개. ㄱ L(8,12)=24 ✓, ㄴ A₂₀(2)={20}≠A₂₀(4)={5,10,20} ✗, ㄷ {9,18,36} 합 63 ✓ → ③. 빠른정답 5와 불일치.")

add(id="a271a383", qtype="short",
    question=("집합 [[S = set(1, 2, 3, 4, 5)]]의 부분집합 중에서 원소가 2개 이상인 집합을 [[sub(A,k)]] ([[k]] = 1, 2, 3, ⋯, [[n]])이라 하고, "
              "집합 [[sub(A,k)]]의 원소 중에서 최대인 것을 [[sub(a,k)]]이라 하자.\n[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,n) - n]]의 값을 구하시오."),
    choices=None, derived_answer="88", figure=None, difficulty_est=3, confidence=0.9,
    note="n=26, 최댓값 합 Σm(2^(m-1)-1)=114 → 114-26=88 = 빠른정답 ✓.")

add(id="bd1645e8", qtype="short",
    question=("집합 [[S = set(1, 2, 4, 8, 16)]]의 부분집합 중에서 원소가 2개 이상인 집합을 [[sub(A,k)]] ([[k]] = 1, 2, 3, ⋯, [[n]])이라 하고, "
              "집합 [[sub(A,k)]]의 원소 중에서 최대인 것을 [[sub(a,k)]]이라 하자.\n[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,n) - n]]의 값을 구하시오."),
    choices=None, derived_answer="284", figure=None, difficulty_est=3, confidence=0.9,
    note="최댓값 합 2+12+56+240=310, n=26 → 284(전수 확인). 빠른정답 3과 불일치(p45의 빠른정답이 284).")

add(id="8f947094", qtype="choice",
    question="다음 중 옳은 것을 모두 고르면? (정답 2개)",
    choices=["[[A = empty]] 이면 [[card(A) = 0]] 이다.", "[[card(A) = card(B)]] 이면 [[A = B]] 이다.", "[[subset(A, B)]] 이면 [[card(A) <= card(B)]] 이다.",
             "[[A]] = { [[x]] | [[x]]는 10 이하의 짝수 } 이면 [[card(A) = 3]] 이다.", "[[card(set(1, 2, 4)) - card(set(2, 4, 6)) = 1]] 이다."],
    derived_answer="①, ③", figure=None, difficulty_est=1, confidence=0.9,
    note="①✓ ③✓, ④는 n(A)=5, ⑤는 0 → ①, ③. 빠른정답 '3'과 불일치(부분만 일치).")

add(id="f0fd7128", qtype="short",
    question=("전체집합\n[[U]] = { [[x]] | [[x]]는 3의 배수가 아닌 30 이하의 자연수 }\n의 부분집합 [[A]]에 대하여 [[card(A) = 4]]이고 집합 [[A]]의 모든 원소의 합은 100이다. "
              "집합 [[A]]의 모든 원소를 작은 수부터 크기순으로 나열한 것을 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]]라 할 때,\n"
              "[[sub(x,4) - sub(x,3) + sub(x,2) - sub(x,1)]]의 최댓값을 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2019년 3월 고3 문과 28번/4점]. 식=100-2(x₁+x₃), (17,26,28,29) → 10(전수 확인). 빠른정답 88과 불일치(p41의 답).")

dup(["a6e71c3a", "823d9999"], qtype="choice",
    question=("집합 [[A = set(0, 1, 2)]]에 대하여 집합 [[P(A)]]를\n[[P(A) = setb(X, subset(X, A))]]라 할 때, 다음 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[in(empty, P(A))]]\nㄴ. [[subset(set(0), P(A))]]\nㄷ. [[in(set(1, 2), P(A))]]\nㄹ. [[subset(set(0, 1, 2), P(A))]]"),
    choices=CH_PAIR, derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="같은 쪽에 id 2개. ㄱ✓ ㄷ✓, ㄴ·ㄹ은 0∉P(A) → ①. 빠른정답 284와 불일치(p42의 답).")

# ---------------- 서로 같은 집합 ----------------
add(id="a584ed65", qtype="choice",
    question="유한집합 [[A]], [[B]]에 대하여 다음 중 옳은 것은?",
    choices=["[[subset(A, B)]]이면 [[card(A) < card(B)]]이다.", "[[card(A) < card(B)]]이면 [[subset(A, B)]]이다.", "[[card(A) = 0]]이면 [[A = set(empty)]]이다.",
             "[[subset(A, B)]]이고 [[subset(B, A)]]이면 [[card(A) = card(B)]]이다.", "[[card(A) = card(B)]]이면 [[A = B]]이다."],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="A=B이면 n(A)=n(B) → ④ = 빠른정답 ✓.")

add(id="89a305b8", qtype="choice",
    question="다음 두 집합 [[A]], [[B]]에 대하여 [[A = B]]인 것은?",
    choices=["[[A = set(a, b, c)]], [[B = set(b, c, d)]]",
             "[[A]] = { [[x]] | [[x]]는 100보다 작은 홀수 }, [[B]] = { [[x]] | [[x]]는 10보다 큰 홀수 }",
             "[[A]] = {1, 2, 2·2, 2·2·2, 2·2·2·2}, [[B]] = { [[x]] | [[x]]는 16의 약수 }",
             "[[A = set(empty)]], [[B = set(0)]]",
             "[[A]] = {6, 12, 18, 24, ⋯}, [[B]] = { [[x]] | [[x]]는 20보다 작은 6의 배수 }"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="③ 둘 다 {1,2,4,8,16} → ③ = 빠른정답 ✓. ③·⑤의 나열 집합은 텍스트.")

add(id="22486f4c", qtype="choice",
    question=("[[A = set(3, 5)]]일 때, 다음 보기 중 집합 [[A]]와 서로 같은 집합인 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. { [[x]] | [[x]]는 7보다 작은 홀수인 자연수 }\nㄴ. [[setb(x, (x - 3)(x - 5) = 0)]]\nㄷ. { [[x]] | [[x]]는 7보다 작은 소수 }\nㄹ. { [[x]] | [[1 < x < 10]], [[x]]는 15의 약수 }"),
    choices=CH_PAIR, derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="ㄱ={1,3,5} ㄴ={3,5} ㄷ={2,3,5} ㄹ={3,5} → ㄴ, ㄹ = ④. 빠른정답 3과 불일치.")

add(id="40f3d246", qtype="choice",
    question=("[[A = set(3, 7)]]일 때, 다음 보기 중 집합 [[A]]와 서로 같은 집합인 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. { [[x]] | [[x]]는 10보다 작은 홀수인 자연수 }\nㄴ. [[setb(x, (x - 3)(x - 7) = 0)]]\nㄷ. { [[x]] | [[x]]는 10보다 작은 소수 }\nㄹ. { [[x]] | [[1 < x < 10]], [[x]]는 21의 약수 }"),
    choices=CH_PAIR, derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="ㄱ={1,3,5,7,9} ㄴ={3,7} ㄷ={2,3,5,7} ㄹ={3,7} → ㄴ, ㄹ = ④. 빠른정답 5와 불일치.")

add(id="5048263f", qtype="short",
    question="두 집합 [[A = set(6, a - 2, 3)]], [[B = set(a, 1, 6)]]에 대하여 [[subset(A, B)]]이고, [[subset(B, A)]]일 때, [[a]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="A=B: a-2=1 → a=3 (B={3,1,6}) = 빠른정답 ✓.")

add(id="3aedd48b", qtype="choice",
    question="두 집합 [[A = set(6, a - 2, 2)]], [[B = set(a, 4, 2)]]에 대하여 [[subset(A, B)]]이고, [[subset(B, A)]] 일 때, [[a]]의 값으로 옳은 것은?",
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="a-2=4 → a=6 (B={6,4,2}) → ④ = 빠른정답 ✓.")

# ---------------- 진부분집합 ----------------
add(id="0b64e773", qtype="choice",
    question=("다음 보기 중 집합 [[set(1, 2, 3)]]의 진부분집합인 것을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[empty]]\nㄴ. { [[x]] | [[x]]는 3의 양의 약수 }\nㄷ. { [[x]] | [[x]]는 4 미만의 자연수 }\nㄹ. { [[x]] | [[x]]는 [[0 < x < 3]]인 자연수 }"),
    choices=CH_4, derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="ㄷ={1,2,3}은 자기 자신 → ㄱ, ㄴ, ㄹ = ④ = 빠른정답 ✓.")

add(id="50eb5d87", qtype="choice",
    question=("다음 보기 중 집합 [[set(1, 2, 3, 4, 5)]]의 진부분집합인 것을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[empty]]\nㄴ. { [[x]] | [[x]]는 5의 양의 약수 }\nㄷ. { [[x]] | [[x]]는 6 미만의 자연수 }\nㄹ. { [[x]] | [[x]]는 [[0 < x < 4]]인 자연수 }"),
    choices=CH_4, derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="ㄷ={1,…,5}는 자기 자신 → ㄱ, ㄴ, ㄹ = ④ = 빠른정답 ✓.")

add(id="ff24697c", qtype="choice",
    question="전체집합 [[U]]의 두 부분집합 [[A]], [[B]]에 대하여 [[A]]가 [[B]]의 진부분집합일 때, 다음 중 항상 성립한다고 할 수 없는 것은? (단, [[U != empty]])",
    choices=["[[subset(A, B)]]", "[[subset(empty, A)]]", "[[A != B]]", "[[A != empty]]", "[[B != empty]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="A=∅일 수 있음 → ④ = 빠른정답 ✓.")

add(id="eccca165", qtype="choice",
    question=("집합 [[U = set(1, 2, 3, 4, 5)]]의 공집합이 아닌 진부분집합을 각각 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A,30)]]이라 하자.\n"
              "집합 [[sub(A,n)]] ([[n]] = 1, 2, 3, ⋯, 30)의 모든 원소의 평균을 [[sub(a,n)]]이라 할 때, [[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,30)]]의 값은?"),
    choices=["[[75]]", "[[80]]", "[[85]]", "[[90]]", "[[95]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="크기 k별 합 15·C(4,k-1)/k: 15+30+30+15=90 → ④ = 빠른정답 ✓.")

add(id="1f839554", qtype="choice",
    question=("집합 [[U = set(1, 2, 3, 4, 5, 6)]]의 공집합이 아닌 진부분집합을 각각 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A,62)]]라 하자.\n"
              "집합 [[sub(A,n)]] ([[n]] = 1, 2, 3, ⋯, 62)의 모든 원소의 평균을 [[sub(a,n)]]이라 할 때, [[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,62)]]의 값은?"),
    choices=["[[189]]", "[[196]]", "[[203]]", "[[210]]", "[[217]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="21·(1+5/2+10/3+10/4+1)=217 → ⑤(전수 확인). 빠른정답 59와 불일치(p71의 답).")

add(id="66bbf4ff", qtype="short",
    question="집합 [[A]] = { [[x]] | [[x]]는 20의 양의 약수 }의 진부분집합을 [[X]]라 하자. 집합 [[X]]의 모든 원소의 합을 [[S(X)]]라 할 때, [[S(X)]]의 최댓값을 구하시오.",
    choices=None, derived_answer="41", figure=None, difficulty_est=1, confidence=0.9,
    note="약수 합 42에서 1 제외 → 41. 빠른정답 4와 불일치.")

add(id="8e4d5a9c", qtype="short",
    question="집합 [[A]] = { [[x]] | [[x]]는 24의 양의 약수 }의 진부분집합을 [[X]]라 하자. 집합 [[X]]의 모든 원소의 합을 [[S(X)]]라 할 때, [[S(X)]]의 최댓값을 구하시오.",
    choices=None, derived_answer="59", figure=None, difficulty_est=1, confidence=0.9,
    note="약수 합 60에서 1 제외 → 59 = 빠른정답 ✓.")

# ---------------- 부분집합의 개수 ----------------
add(id="69769390", qtype="choice",
    question="집합 [[A]] = { [[x]] | [[x]]는 10보다 크고 15보다 작은 홀수 }의 부분집합의 개수는?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="A={11,13} → 2²=4 → ④ = 빠른정답 ✓.")

add(id="4e622116", qtype="short",
    question="집합 [[A]] = { [[x]] | [[x]]는 5보다 크고 15보다 작은 짝수 }의 부분집합의 개수를 구하시오.",
    choices=None, derived_answer="32", figure=None, difficulty_est=1, confidence=0.9,
    note="A={6,8,10,12,14} → 2⁵=32. 빠른정답 59와 불일치.")

add(id="c44e9f1c", qtype="short",
    question="집합 { [[x]] | [[x]]는 [[-3 < x < 1]]인 정수 }의 부분집합의 개수를 구하시오.",
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="{-2,-1,0} → 2³=8. 빠른정답 30과 불일치.")

dup(["3c099b2d", "47a54c74"], qtype="choice",
    question=("3 이상의 자연수 [[m]]에 대하여\n[[sub(A,m)]] = { [[x]] | [[x]]는 [[m + 1]] 이하의 소수 },\n[[sub(B,m)]] = { [[x]] | [[x]]는 [[m]]의 양의 약수 }\n"
              "일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[card(sub(A,6)) + card(sub(B,6)) = 8]]\nㄴ. [[subset(sub(A,m), sub(B,210))]]을 만족시키는 [[m]]의 최댓값은 10이다.\n"
              "ㄷ. [[m > 11]]일 때, 집합 [[sub(A,m)]]의 부분집합의 개수는 집합 [[sub(B,m)]]의 부분집합의 개수보다 작거나 같다."),
    choices=CH_3C, derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="같은 쪽에 id 2개. ㄱ 4+4=8 ✓, ㄴ 최댓값 9(m=10이면 11∈A₁₀, 11∤210) ✗, ㄷ m=13 반례 ✗ → ①. 빠른정답 32와 불일치(p74의 답).")

add(id="24dd2f2c", qtype="choice",
    question="전체집합 [[U = set(1, 2, 3, 4)]]의 공집합이 아닌 두 부분집합 [[A]], [[B]]에 대하여 [[subset(A, B)]]를 만족하는 두 집합 [[A]], [[B]]의 순서쌍 ([[A]], [[B]])의 개수는?",
    choices=["[[50]]", "[[55]]", "[[60]]", "[[65]]", "[[70]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="3⁴-2⁴=65 → ④. 빠른정답 3과 불일치.")

add(id="0e71a8d9", qtype="choice",
    question="전체집합 [[U = set(a, b, c, d, e)]]의 공집합이 아닌 두 부분집합 [[A]], [[B]]에 대하여 [[subset(A, B)]]를 만족시키는 두 집합 [[A]], [[B]]의 순서쌍 ([[A]], [[B]])의 개수는?",
    choices=["[[201]]", "[[211]]", "[[221]]", "[[231]]", "[[241]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="3⁵-2⁵=211 → ②. 빠른정답 1과 불일치.")

add(id="ea767024", qtype="choice",
    question="전체집합 [[U = set(a, b, c)]]의 공집합이 아닌 두 부분집합 [[A]], [[B]]에 대하여 [[subset(A, B)]]를 만족시키는 두 집합 [[A]], [[B]]의 순서쌍 ([[A]], [[B]])의 개수는?",
    choices=["[[17]]", "[[18]]", "[[19]]", "[[20]]", "[[21]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="3³-2³=19 → ③ = 빠른정답 ✓.")

# ---------------- 특정한 원소를 갖거나 갖지 않는 부분집합의 개수 ----------------
add(id="17b6d048", qtype="choice",
    question=("두 집합\n[[A]] = { [[x]] | [[x]]는 9 이하의 자연수 },\n[[B]] = { [[x]] | [[x]]는 7 이상 13 이하의 자연수 }\n"
              "가 있다. 다음은 [[subset(X, A)]], [[card(union(X, B)) = 10]]을 만족시키는 집합 [[X]]의 개수를 구하는 과정이다.\n"
              "[[subset(X, A)]]이므로 세 집합 [[A]], [[B]], [[X]]를 벤다이어그램으로 나타내면 다음과 같다.\n"
              "[[sub(X,1) = inter(X, (A - B))]], [[sub(X,2) = inter(X, (inter(A, B)))]]라 하면 [[X = union(sub(X,1), sub(X,2))]]이고 [[inter(sub(X,1), sub(X,2)) = empty]]이다.\n"
              "(ⅰ) [[card(union(X, B)) = 10]]이고 [[card(B) = 7]]이므로\n[[card(sub(X,1))]] = (가)\n따라서 가능한 집합 [[sub(X,1)]]의 개수는 (나) 이다.\n"
              "(ⅱ) 집합 [[sub(X,2)]]는 집합 [[inter(A, B)]]의 부분집합이므로 가능한 집합 [[sub(X,2)]]의 개수는 (다) 이다.\n"
              "(ⅰ), (ⅱ)에 의하여 집합 [[X]]의 개수는 (나) · (다) 이다.\n"
              "위의 (가), (나), (다)에 알맞은 수를 각각 [[p]], [[q]], [[r]]라 할 때, [[p + q + r]]의 값은?"),
    choices=["[[23]]", "[[25]]", "[[27]]", "[[29]]", "[[31]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "풀이 상자 안 벤다이어그램(원소 표시 없음): 두 원 A, B가 겹치고, A 안의 타원 X가 A∩B 부분에 걸쳐 있음"}}],
    difficulty_est=3, confidence=0.85,
    note="출처 [2019년 3월 고2 문과 19번 변형]. (가)=3, (나)=C(6,3)=20, (다)=2³=8 → 31 → ⑤. 빠른정답 15와 불일치. 벤다이어그램은 설명용(원소 없음)이라 unsupported로 처리.")

add(id="601526cd", qtype="choice",
    question="다음 중 부분집합의 개수가 32인 집합은?",
    choices=["[[set(a, b, c, d)]]", "{ [[x]] | [[x]]는 13 이하의 소수인 자연수 }", "{ [[x]] | [[x]]는 6보다 작은 홀수인 자연수 }",
             "{ [[x]] | [[x]]는 16의 양의 약수 }", "{ [[x]] | [[x]]는 10 이하의 자연수 }"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="원소 5개인 것: ④ {1,2,4,8,16}. 빠른정답 2와 불일치.")

add(id="0e3f256e", qtype="choice",
    question="집합 [[A]] = { [[x]] | [[x]]는 30 이하의 4의 양의 배수 }의 부분집합 중에서 8, 16을 반드시 원소로 갖고, 20을 원소로 갖지 않는 집합의 개수는?",
    choices=["[[4]]", "[[6]]", "[[8]]", "[[12]]", "[[16]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="n(A)=7 → 2^(7-3)=16 → ⑤. 빠른정답 3과 불일치.")

add(id="754c9736", qtype="short",
    question="[[M = set(1, 2, 3)]]일 때, [[pow(2, M) = setb(X, subset(X, M))]]으로 정의한다. 이때 [[pow(2, M)]]의 부분집합의 개수를 구하시오.",
    choices=None, derived_answer="256", figure=None, difficulty_est=2, confidence=0.9,
    note="n(2^M)=8 → 2⁸=256. 빠른정답 5와 불일치.")

add(id="18fcfc89", qtype="short",
    question="집합 [[A]] = { [[x]] | [[x]]는 1 이상 50 이하의 5의 배수 }의 진부분집합 중에서 홀수를 1개 이상 원소로 갖는 집합의 개수를 구하시오.",
    choices=None, derived_answer="991", figure=None, difficulty_est=2, confidence=0.9,
    note="진부분집합 1023개 - 홀수 없는 부분집합 2⁵=32 → 991(전수 확인). 빠른정답 4와 불일치(p89 자리의 빠른정답이 991).")

add(id="97b492b2", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 8 이하의 자연수 }의 부분집합 [[X]]에 대하여 집합 [[X]]의 모든 원소의 합을 [[S(X)]]라 하자. "
              "집합 [[U]]의 두 부분집합 [[A]], [[B]]에 대하여 [[card(A) >= 2]], [[card(B) >= 2]]일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은? (단, [[S(empty) = 0]])\n<보기>\n"
              "ㄱ. [[S(A) < S(B)]]이면 [[subset(A, B)]]이다.\nㄴ. [[A = set(1, 2)]]이면 [[S(union(A, B)) = S(A) + S(B)]]인 집합 [[B]]의 개수는 57이다.\n"
              "ㄷ. [[union(A, B) = U]], [[inter(A, B) = set(2, 4, 6)]]이면 [[S(A) × S(B)]]의 최댓값은 576이다."),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.85,
    note="ㄱ 반례 {1,5},{2,7} ✗; ㄴ A∩B=∅, B⊂{3,…,8}, n(B)≥2 → 64-1-6=57 ✓; ㄷ S(A)+S(B)=36+12=48, 24·24=576 달성 ✓ → ⑤. 빠른정답 991과 불일치(p86의 답).")

add(id="0d478b22", qtype="choice",
    question=("집합 [[U = set(2, 3, 5, 7, 11)]]의 부분집합 중 2개의 원소로 이루어진 부분집합 전체를 각각 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A,10)]]이라 하고, "
              "집합 [[sub(A,k)]]의 원소의 합을\n[[sub(a,k)]] ([[k]] = 1, 2, 3, ⋯, 10) 이라 할 때,\n[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,10)]]의 값은?"),
    choices=["[[104]]", "[[106]]", "[[108]]", "[[110]]", "[[112]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="각 원소가 4번씩 → 4×28=112 → ⑤. 빠른정답 4와 불일치.")

add(id="4b83bdde", qtype="short",
    question="집합 [[A]] = { [[x]] | [[x]]는 100의 양의 약수 }의 부분집합 중에서 홀수인 원소가 2개인 집합의 개수를 구하시오.",
    choices=None, derived_answer="192", figure=None, difficulty_est=2, confidence=0.9,
    note="홀수 약수 3개 중 2개 C(3,2)=3, 짝수 약수 6개 자유 2⁶ → 192 = 빠른정답 ✓.")

# ---------------- A⊂X⊂B를 만족하는 집합 X의 개수 ----------------
add(id="5b6a68df", qtype="short",
    question="두 집합 [[A]], [[B]]를 벤다이어그램으로 나타내면 다음 그림과 같다. [[B]] ⊂ [[X]] ⊂ [[A]]를 만족시키는 집합 [[X]] 중에서 12를 반드시 원소로 갖는 집합의 개수를 구하시오.",
    choices=None, derived_answer="8",
    figure=[{"fn": "unsupported", "args": {"raw": "벤다이어그램: 큰 원 A 안에 작은 원 B. B 안에 2, 4; A에서 B 밖에 6, 8, 10, 12 (A={2,4,6,8,10,12}, B={2,4})"}}],
    difficulty_est=2, confidence=0.8, needs_review="도형 표현 불가: 원소가 표시된 벤다이어그램(문항 정보 전부가 그림에 있음)",
    note="X={2,4,12}∪({6,8,10}의 부분집합) → 2³=8. 빠른정답 192와 불일치(p91의 답).")

add(id="efa6e4ae", qtype="short",
    question=("두 집합\n[[A = setb(x, pow(x,2) - 7x + 10 = 0)]],\n[[B]] = { [[x]] | [[x = frac(40, n)]], [[x]], [[n]]은 자연수 }\n"
              "에 대하여 [[A]] ⊂ [[X]] ⊂ [[B]]를 만족시키는 집합 [[X]]의 개수를 구하시오."),
    choices=None, derived_answer="64", figure=None, difficulty_est=2, confidence=0.9,
    note="A={2,5}, B=40의 약수 8개 → 2⁶=64. 빠른정답 4와 불일치.")

add(id="460b4216", qtype="short",
    question="두 집합 [[A = set(3, 5)]], [[B]] = { [[x]] | [[x]]는 20 미만의 소수 }에 대하여 [[A]] ⊂ [[X]] ⊂ [[B]], [[X != A]], [[X != B]]를 만족시키는 집합 [[X]]의 개수를 구하시오.",
    choices=None, derived_answer="62", figure=None, difficulty_est=2, confidence=0.9,
    note="n(B)=8 → 2⁶-2=62. 빠른정답 4와 불일치.")

add(id="1b0e632e", qtype="short",
    question="두 집합 [[A]] = {1, 2, 3, ⋯, [[n]]}, [[B = set(3, 6, 9)]]에 대하여 [[B]] ⊂ [[X]] ⊂ [[A]]를 만족시키는 집합 [[X]]의 개수가 256일 때, 자연수 [[n]]의 값을 구하시오.",
    choices=None, derived_answer="11", figure=None, difficulty_est=2, confidence=0.9,
    note="2^(n-3)=256 → n=11 = 빠른정답 ✓.")

# p99: 한 이미지에 문항 2개, id 2개 — draft_a 대응(da7f1296=첫째, 66cbfe02=둘째)
add(id="da7f1296", qtype="choice",
    question="다음 중 [[set(a, b)]] ⊂ [[A]] ⊂ [[set(a, b, c, d)]]를 만족시키는 집합 [[A]]가 될 수 없는 것은?",
    choices=["[[set(a, b)]]", "[[set(a, b, c)]]", "[[set(a, b, d)]]", "[[set(a, c, d)]]", "[[set(a, b, c, d)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.85,
    note="같은 이미지(p99)에 문항 2개 인쇄 — 이 id는 위쪽 문항(draft_a 대응). b∉{a,c,d} → ④. 빠른정답 62와 불일치.")

add(id="66cbfe02", qtype="choice",
    question="{ [[x]] | [[x]]는 6의 약수 } ⊂ [[X]] ⊂ { [[x]] | [[x]]는 12의 약수 }를 만족하는 집합 [[X]]의 개수는?",
    choices=["2개", "4개", "5개", "6개", "8개"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.85,
    note="같은 이미지(p99)에 문항 2개 인쇄 — 이 id는 아래쪽 문항(draft_a 대응). {1,2,3,6}⊂X⊂{1,2,3,4,6,12} → 2²=4개 → ②. 빠른정답 62와 불일치.")

# ================= 점과 직선 사이의 거리 =================
add(id="14fb603a", qtype="short",
    question=("아래 그림과 같이 [[seg(AB) = sqrt(85)]], [[seg(BC) = 8]], [[seg(CA) = sqrt(53)]]인 삼각형 ABC에 대하여 선분 BC를 [[ratio(3, 1)]]로 내분하는 점을 D라 하자. "
              "점 D에서 선분 AB에 내린 수선의 발을 E라 할 때, 선분 DE의 길이는 [[frac(p, q) sqrt(85)]]이다. [[q - p]]의 값을 구하시오. (단, [[p]], [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="43",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래). AB=√85, BC=8, CA=√53 표시. D는 BC 위(C쪽에 가까움), E는 AB 위, DE⊥AB 직각 표시"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 변의 길이·수선이 표시된 삼각형 도형",
    note="B(0,0), C(8,0), A(6,7), D(6,0); AB: 7x-6y=0 → DE=42/√85=(42/85)√85 → q-p=43 = 빠른정답 ✓.")

add(id="e7798212", qtype="choice",
    question=("한 변의 길이가 2인 정사각형 모양의 종이 ABCD가 있다. [[angle(ECD) = deg(30)]]인 변 AD 위의 점 E에 대하여 다음 그림과 같이 선분 CE를 기준으로 아래 부분의 종이를 접었을 때, "
              "점 D′과 선분 AC 사이의 거리는?"),
    choices=["[[frac(sqrt(6) + sqrt(2), 4)]]", "[[frac(sqrt(6) - sqrt(2), 2)]]", "[[frac(sqrt(3) + 1, 4)]]", "[[frac(sqrt(3) - 1, 2)]]", "[[frac(sqrt(2), 2)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(B 왼쪽 위, A 오른쪽 위, C 왼쪽 아래, D 오른쪽 아래). E는 AD 위, CE를 접는 선으로 D가 D′(정사각형 내부)로 접힘. ∠ECD=30° 표시, 대각선 AC 점선, CD·DE 점선"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 접힌 정사각형 도형 / 프라임 점 라벨 D′",
    note="C(0,0), D(2,0), E(2,2/√3), D′=(1,√3); AC: y=x → 거리 |1-√3|/√2=(√6-√2)/2 → ② = 빠른정답 ✓.")

add(id="8f73411e", qtype="choice",
    question=("좌표평면의 제1사분면에 있는 두 점 A, B와 원점 O에 대하여 삼각형 OAB의 무게중심 G의 좌표는 [[point(8, 4)]]이고, 점 B와 직선 OA 사이의 거리는 [[6 sqrt(2)]]이다.\n"
              "다음은 직선 OB의 기울기가 직선 OA의 기울기보다 클 때, 직선 OA의 기울기를 구하는 과정이다.\n"
              "선분 OA의 중점을 M이라 하자.\n"
              "점 G가 삼각형 OAB의 무게중심이므로\n[[ratio(seg(BG), seg(GM)) = ratio(2, 1)]]이고,\n"
              "점 B와 직선 OA 사이의 거리가 [[6 sqrt(2)]]이므로\n점 G와 직선 OA 사이의 거리는 (가) 이다.\n"
              "직선 OA의 기울기를 [[m]]이라 하면\n점 G와 직선 OA 사이의 거리는\n((나)) / [[sqrt(pow(m,2) + pow(-1,2))]] 이고 (가) 와 같다.\n"
              "즉, (나) = (가) · [[sqrt(pow(m,2) + 1)]] 이다.\n"
              "양변을 제곱하여 [[m]]의 값을 구하면\n[[m]] = □ 또는 [[m]] = □ 이다.\n"
              "이때 직선 OG의 기울기가 [[frac(1, 2)]] 이므로\n직선 OA의 기울기는 (다) 이다.\n"
              "위의 (가), (다)에 알맞은 수를 각각 [[p]], [[q]]라 하고,\n(나)에 알맞은 식을 [[f(m)]]이라 할 때, [[frac(f(q), pow(p,2))]]의 값은?"),
    choices=["[[frac(2, 7)]]", "[[frac(5, 14)]]", "[[frac(3, 7)]]", "[[frac(1, 2)]]", "[[frac(4, 7)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(풀이 상자 안): 원점 O, 제1사분면의 점 A(오른쪽 아래)·B(위쪽), 삼각형 OAB, 무게중심 G(8,4), 선분 OA의 중점 M, 선분 BM"}}],
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 삼각형 OAB·무게중심 G·중점 M 도형 / 빈칸 (나)가 분수 분자에 있어 조각 전사",
    note="출처 [2020년 3월 고2 18번/4점]. (가)=2√2, (나)=|8m-4|, 7m²-8m+1=0 → m=1/7 또는 1, OG 기울기 1/2보다 작은 (다)=1/7 → f(1/7)/p²=(20/7)/8=5/14 → ②. 빠른정답 30과 불일치.")

add(id="e2c4940e", qtype="choice",
    question="두 직선 [[3x - 4y + 3 = 0]], [[4x - 3y - 2 = 0]]이 이루는 각을 이등분하는 직선이 점 [[point(-1, a)]]를 지날 때, 모든 상수 [[a]]의 값의 곱은?",
    choices=["[[-frac(34, 7)]]", "[[-5]]", "[[-frac(36, 7)]]", "[[-frac(37, 7)]]", "[[-frac(38, 7)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="이등분선 x+y=5, 7x-7y+1=0 → a=6, a=-6/7 → 곱 -36/7 → ③. 빠른정답 4와 불일치.")

add(id="516375f3", qtype="short",
    question="점 P에서 두 직선 [[x + 2y - 1 = 0]], [[2x - y - 1 = 0]]에 내린 수선의 발을 각각 A, B라 할 때, [[2 seg(PA) = seg(PB)]]를 만족시키는 점 P가 지나지 않는 사분면을 구하시오.",
    choices=None, derived_answer="제3사분면", figure=None, difficulty_est=3, confidence=0.85,
    note="2|x+2y-1|=|2x-y-1| → y=1/5 또는 4x+3y-3=0; 두 직선 모두 제3사분면을 지나지 않음. 빠른정답 1과 불일치.")

add(id="b479f73b", qtype="choice",
    question=("두 직선 [[3x - 4y + 1 = 0]], [[4x + 3y + 2 = 0]]에 대하여 두 직선 위에 있지 않은 점 P에서 두 직선에 내린 수선의 발을 각각 R, S라 하자. "
              "[[ratio(seg(PR), seg(PS)) = ratio(1, 3)]]을 만족시키는 점 P의 자취는 두 개의 직선으로 나타난다. 이 두 직선의 기울기의 합은?"),
    choices=["[[frac(16, 9)]]", "[[2]]", "[[frac(20, 9)]]", "[[frac(22, 9)]]", "[[frac(8, 3)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="3|3x-4y+1|=|4x+3y+2| → 5x-15y+1=0(기울기 1/3), 13x-9y+5=0(기울기 13/9) → 합 16/9 → ①. 빠른정답 5와 불일치.")

add(id="488fe97f", qtype="choice",
    question=("직선 [[y = -x + 6]] 위의 점 A와 두 점 [[B(2, 0)]], [[C(5, 3)]]에 대하여 삼각형 ABC의 무게중심 G가 나타내는 도형의 방정식이 [[y = a x + b]]일 때, [[a + b]]의 값은?\n"
              "(단, [[a]], [[b]]는 상수이다.)"),
    choices=["[[frac(7, 3)]]", "[[frac(10, 3)]]", "[[frac(13, 3)]]", "[[frac(16, 3)]]", "[[frac(19, 3)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="A(t,6-t) → G=((t+7)/3,(9-t)/3) → y=-x+16/3 → a+b=13/3 → ③ = 빠른정답 ✓. 이미지 하단에 별개 문항(직선 y=3x+4, B(-2,1), C(4,7); 답 ③ 5)이 함께 인쇄돼 있으나 id가 하나뿐이라 위쪽 문항만 전사.")
