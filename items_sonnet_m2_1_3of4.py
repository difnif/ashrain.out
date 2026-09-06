# -*- coding: utf-8 -*-
# esc_sonnet_m2-1_3of4 — 이미지 기준 전사 (81 항목 / 80쪽)
# 관례: 순환소수는 recdec(정수부·비순환부, 순환마디). 단항식으로 나누는 나눗셈(÷ 3y 등)은 파서가 좌결합이므로
#       나누는 단항식을 괄호로 묶음. 빈칸 상자는 □(텍스트). 도형·그래프 선지는 unsupported + raw 설명.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ---------------- 다항식의 덧셈과 뺄셈
add(id="daa26317", qtype="short",
    question=("[[3 pow(x,2) - 2x + 2]]에서 어떤 식을 빼야 할 것을 잘못하여 더했더니 [[-2 pow(x,2) + 2x + 3]]이 되었다. "
              "이때 바르게 계산한 식이 [[a pow(x,2) + b x + c]]일 때, [[a + b + c]]의 값을 구하시오.\n(단, [[a]], [[b]], [[c]]는 상수)"),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="어떤 식 = −5x²+4x+1, 바른 계산 8x²−6x+1 → 3. 빠른정답 2와 불일치.")

add(id="73cac7dc", qtype="short",
    question=("[[-5y + 4x - 2]]에서 어떤 식을 빼어야 할 것을 잘못하여 더했더니 [[x - 2y + 3]]이 되었다.\n"
              "어떤 식이 [[a x + b y + c]]이고 바르게 계산한 답이 [[d x + e y + f]]일 때, [[a f - b d - c e]]의 값을 구하시오.\n"
              "(단, [[a]], [[b]], [[c]], [[d]], [[e]], [[f]]는 상수)"),
    choices=None, derived_answer="40", figure=None, difficulty_est=2, confidence=0.9,
    note="어떤 식 −3x+3y+5, 바른 답 7x−8y−7 → 21−21+40 = 40. 빠른정답 4와 불일치.")

# ---------------- 연립방정식의 활용(2)
add(id="513af674", qtype="short",
    question=("둘레의 길이가 1200 m인 호수가 있다. 민호와 정아가 호수의 둘레를 동시에 같은 방향으로 돌면 10분 후에 만나고, "
              "반대 방향으로 돌면 3분 후에 만난다고 한다. 민호의 속력이 정아의 속력보다 빠르다고 할 때, 민호의 속력을 구하시오."),
    choices=None, derived_answer="분속 260 m", figure=None, difficulty_est=2, confidence=0.9,
    note="x−y=120, x+y=400 → 민호 분속 260 m. 빠른정답 5와 불일치.")

# ---------------- 일차함수와 일차방정식
add(id="fb4d290e", qtype="short",
    question=("일차방정식 [[16x - 4y + b = 0]]의 그래프와 일차함수 [[y = a x - 2]]의 그래프가 일치할 때, "
              "상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="-4", figure=None, difficulty_est=2, confidence=0.9,
    note="y = 4x + b/4 → a=4, b=−8 → −4. 빠른정답 1과 불일치.")

add(id="8b10a12d", qtype="short",
    question=("일차방정식 [[a x - y + 3 = 0]]의 그래프와 일차함수 [[y = 2x - b]]의 그래프가 일치할 때, "
              "상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.9,
    note="y = ax + 3 → a=2, b=−3 → −1 = 빠른정답 ✓.")

add(id="44143418", qtype="choice",
    question="[[x]], [[y]]의 값이 모두 정수일 때, 다음 중 일차방정식 [[x + y = 5]]의 그래프는?",
    choices=["좌표평면에서 두 점 [[point(0, 5)]], [[point(5, 0)]]을 지나는 직선",
             "좌표평면 위의 네 점 [[point(1, 4)]], [[point(2, 3)]], [[point(3, 2)]], [[point(4, 1)]]",
             "좌표평면 위의 점 [[point(-1, 6)]], [[point(0, 5)]], [[point(1, 4)]], [[point(2, 3)]], [[point(3, 2)]], [[point(4, 1)]], [[point(5, 0)]], [[point(6, -1)]]",
             "좌표평면에서 두 점 [[point(-5, 0)]], [[point(0, 5)]]를 지나는 직선",
             "좌표평면 위의 점 [[point(-6, -1)]], [[point(-5, 0)]], [[point(-4, 1)]], [[point(-3, 2)]], [[point(-2, 3)]], [[point(-1, 4)]], [[point(0, 5)]], [[point(1, 6)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "선지 ①~⑤가 좌표평면 그래프: ① (0,5),(5,0)을 지나는 직선 ② 점 (1,4),(2,3),(3,2),(4,1) ③ 점 (−1,6),(0,5),(1,4),(2,3),(3,2),(4,1),(5,0),(6,−1) ④ (−5,0),(0,5)를 지나는 직선 ⑤ 점 (−6,−1),(−5,0),…,(0,5),(1,6)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 선지 5개가 좌표평면 그래프(직선·점 나열)",
    note="x+y=5의 정수해 점 나열 → ③ = 빠른정답 ✓.")

add(id="5370d41c", qtype="choice",
    question="[[x]], [[y]]가 수 전체일 때, 일차방정식 [[3x + 2y = 12]]의 그래프는?",
    choices=["좌표평면에서 두 점 [[point(0, 6)]], [[point(4, 0)]]을 지나는 직선",
             "좌표평면에서 두 점 [[point(0, 6)]], [[point(2, 0)]]을 지나는 직선",
             "좌표평면에서 두 점 [[point(0, 4)]], [[point(6, 0)]]을 지나는 직선",
             "좌표평면 위의 세 점 [[point(0, 6)]], [[point(2, 3)]], [[point(4, 0)]]",
             "좌표평면 위의 세 점 [[point(0, 0)]], [[point(2, 2)]], [[point(4, 4)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "선지 ①~⑤가 좌표평면 그래프: ① y절편 6, x절편 4인 직선 ② y절편 6, x절편 2인 직선 ③ y절편 4, x절편 6인 직선 ④ 점 (0,6),(2,3),(4,0) ⑤ 점 (0,0),(2,2),(4,4)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 선지 5개가 좌표평면 그래프(직선·점)",
    note="x절편 4, y절편 6인 직선 → ①. 빠른정답 3과 불일치.")

add(id="a9653c2a", qtype="short",
    question=("[[x]], [[y]]가 정수일 때, 일차방정식 [[5x - 2y = -22]]의 해를 [[x = p]], [[y = q]]라 하자. "
              "이때 [[-3x y]]의 값 중 가장 큰 값을 구하시오."),
    choices=None, derived_answer="36", figure=None, difficulty_est=3, confidence=0.9,
    note="x=2k, y=5k+11 → −3xy = −30k²−66k, k=−1일 때 최대 36 = 빠른정답 ✓.")

add(id="2891b8cc", qtype="choice",
    question=("다음 그림은 [[x]], [[y]]가 모든 수일 때, 일차방정식 [[x + 3y = 12]]의 그래프이다. "
              "두 점 A[[point(a, 2)]], B[[point(b, a)]]가 그래프 위의 점일 때, [[a - b]]의 값은? (단, [[a]], [[b]]는 상수이다.)"),
    choices=["[[-frac(1,9)]]", "[[frac(1,9)]]", "[[6]]", "[[10]]", "[[12]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 일차방정식 x+3y=12의 그래프(x절편 12), 그래프 위의 두 점 (a, 2), (b, a)를 점선으로 축에 대응(b<0, a>0)"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 위 직선 그래프와 두 점",
    note="a=6, b=−6 → 12 → ⑤ = 빠른정답 ✓.")

# ---------------- 부등식
add(id="b8160cd3", qtype="short",
    question="[[x]]가 3 이하의 자연수일 때, 부등식 [[3x - 2 < 4]]를 푸시오.",
    choices=None, derived_answer="x = 1", figure=None, difficulty_est=1, confidence=0.9,
    note="3x<6 → x<2 → x=1. 빠른정답 없음.")

add(id="332865b3", qtype="choice",
    question="다음 중 옳지 않은 것을 모두 고르면? (정답 2개)",
    choices=["[[a - c < b - c]]이면 [[a < b]]이다.",
             "[[a - b > 0]]이면 [[a > b]]이다.",
             "[[a > b > 0]]이고 [[c < 0]]이면 [[a c < b c]]이다.",
             "[[a < b < 0]]이고 [[c < 0]]이면 [[a c < b c]]이다.",
             "[[a > b]]이고 [[c > d]]이면 [[a c > b d]]이다."],
    derived_answer="④, ⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="④ c<0이면 ac>bc / ⑤ 반례 존재 → ④, ⑤. 빠른정답 없음.")

add(id="8722752f", qtype="choice",
    question="다음 중 옳지 않은 것을 모두 고르면? (정답 2개)",
    choices=["[[a + c < b + c]]이면 [[a < b]]이다.",
             "[[c - a < c - b]]이면 [[a < b]]이다.",
             "[[a c < b c]]이면 [[a < b]]이다.",
             "[[a > b]], [[c > 0]]이면 [[a c > b c]]이다.",
             "[[a > b]], [[c > 0]]이면 [[frac(a, c) > frac(b, c)]]이다."],
    derived_answer="②, ③", figure=None, difficulty_est=2, confidence=0.9,
    note="② −a<−b → a>b / ③ c의 부호 불명 → ②, ③. 빠른정답 없음.")

add(id="be16e2de", qtype="short",
    question=("[[-1 < x <= 5]]일 때, [[-2x + 7]]의 최솟값을 [[p]], 최댓값을 [[q]]라 하자. 이때 [[p q]]의 값을 구하시오. "
              "(단, [[p]], [[q]]는 정수)"),
    choices=None, derived_answer=None, figure=None, difficulty_est=2, confidence=0.85,
    note="−3 ≤ −2x+7 < 9로 최댓값이 정해지지 않음(x 정수면 p=−3, q=7 → −21) → 답 미도출. 빠른정답 −24.")

# ---------------- 순환소수의 분수 표현
add(id="ddb6516f", qtype="choice",
    question="다음 중 순환소수 [[x = 7.31555]]⋯에 대한 설명으로 옳지 않은 것은?",
    choices=["무한소수이다.", "순환마디는 5이다.", "[[x]]는 [[recdec(7.31, 5)]]로 간단히 나타낸다.",
             "[[1000x - 100x]]의 값은 정수이다.", "[[x = frac(1207, 165)]]이다."],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="x = 6584/900 = 1646/225 ≠ 1207/165 → ⑤. 빠른정답 1과 불일치.")

add(id="2d5a06bf", qtype="short",
    question="다음은 순환소수를 분수로 나타내는 과정이다. □ 안에 알맞은 수를 써넣으시오.\n[[recdec(0, 83)]] = □/99",
    choices=None, derived_answer="83", figure=None, difficulty_est=1, confidence=0.9,
    note="0.8̇3̇ = 83/99 → 83. 빠른정답 3과 불일치.")

_ABCD = ("서로 다른 한 자리 자연수 [[a]], [[b]], [[c]], [[d]]에 대하여 abcd = [[1000a + 100b + 10c + d]]이고 ab = [[10a + b]]라 하자. "
         "[[frac({n}, 9900)]] = (abcd − ab)/9900 = 0.abċḋ일 때, [[abs({e})]]의 값을 구하시오.")
add(id="856bb476", qtype="short", question=_ABCD.format(n="4315", e="a - b + c - d"),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 자릿수 표기 abcd·문자 순환소수 0.abċḋ 텍스트 혼합",
    note="abcd−ab=4315 → a=4, b=3 → abcd=4358, c=5, d=8 → |4−3+5−8| = 2. 빠른정답 83과 불일치.")
add(id="7cd9846a", qtype="short", question=_ABCD.format(n="3651", e="a + b - c + d"),
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 자릿수 표기 abcd·문자 순환소수 0.abċḋ 텍스트 혼합",
    note="a=3, b=6 → abcd=3687, c=8, d=7 → |3+6−8+7| = 8. 빠른정답 237과 불일치.")
add(id="890f7408", qtype="short", question=_ABCD.format(n="5246", e="a - b + c + d"),
    choices=None, derived_answer="20", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 자릿수 표기 abcd·문자 순환소수 0.abċḋ 텍스트 혼합",
    note="a=5, b=2 → abcd=5298, c=9, d=8 → |5−2+9+8| = 20. 빠른정답 5와 불일치.")

add(id="38ec3323", qtype="short",
    question="다음은 순환소수를 분수로 나타내는 과정이다. □ 안에 알맞은 수를 써넣으시오.\n[[recdec(0, 56)]] = 56/□",
    choices=None, derived_answer="99", figure=None, difficulty_est=1, confidence=0.9,
    note="0.5̇6̇ = 56/99 → 99. 빠른정답 2와 불일치.")

add(id="db2ab4b6", qtype="short",
    question=("[[0.1 + 0.08 + 0.003 + 0.0003 + 0.00003]] + ⋯을 계산하여 기약분수로 나타내면 [[frac(m, n)]]이 된다. "
              "이때 [[m + n]]의 값을 구하시오."),
    choices=None, derived_answer="71", figure=None, difficulty_est=2, confidence=0.9,
    note="합 = 0.183̇ = 11/60 → 71 = 빠른정답 ✓.")

add(id="bb29191a", qtype="choice",
    question="[[a = recdec(2, 81)]], [[b = recdec(3, 4)]]일 때, [[frac(b, a)]]를 순환소수로 나타내면?",
    choices=["[[recdec(0, 2)]]", "[[recdec(0, 23)]]", "[[recdec(1, 2)]]", "[[recdec(1.3, 1)]]", "[[recdec(1, 32)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="a=31/11, b=31/9 → b/a = 11/9 = 1.2̇ → ③ = 빠른정답 ✓.")

add(id="2930680a", qtype="choice",
    question="한 자리 자연수 [[a]], [[b]]에 대하여 0.ȧḃ + 0.ḃȧ = [[recdec(0, 5)]]가 성립할 때, [[a + b]]의 값은?",
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 문자 순환소수 0.ȧḃ 텍스트 혼합",
    note="11(a+b)/99 = 5/9 → a+b = 5 → ② = 빠른정답 ✓.")

add(id="caef767c", qtype="short",
    question=("두 수 [[a]], [[b]]에 대하여 [[a]]◎[[b]] = [[-1]] ([[a > b]]), [[0]] ([[a = b]]), [[1]] ([[a < b]])로 정의할 때, "
              "([[0.5]]◎[[recdec(0, 5)]])◎([[1.3]]◎[[recdec(1.2, 9)]])의 값을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 조각적(경우 나눔) 정의 ◎ 연산 텍스트 혼합",
    note="0.5<0.5̇ → 1, 1.3 = 1.29̇ → 0, 1◎0 = −1 = 빠른정답 ✓.")

add(id="6d12b521", qtype="short",
    question=("[[a]]∘[[b]]를 ([[a = b]]이면 1, [[a != b]]이면 0)이라 하면 [[a = recdec(0.1, 9)]], [[b = 0.2]], "
              "[[c = recdec(0, 01)]], [[d = frac(1, 90)]]일 때, ([[a]]∘[[b]])∘([[c]]∘[[d]])의 값을 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 조각적(경우 나눔) 정의 ∘ 연산 텍스트 혼합",
    note="a=0.2=b → 1; c=1/99≠1/90 → 0; 1∘0 = 0. 빠른정답 3과 불일치.")

add(id="01c545d6", qtype="short",
    question=("[[A]] = 0.ȧ0bċ, [[B]] = 0.ȧcb0̇일 때, 다음 부등식을 만족시키는 [[c]]의 값을 구하시오.\n"
              "(단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.044 < B - A < 0.055]]"),
    choices=None, derived_answer="5", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 문자 순환소수 0.ȧ0bċ 텍스트 혼합",
    note="B−A = 99c/9999 = c/101 → 4.44<c<5.56 → c=5. 빠른정답 −2와 불일치.")

add(id="58010922", qtype="short",
    question=("[[A]] = 0.ȧc0ḃ, [[B]] = 0.ȧ0cḃ일 때, 다음 부등식을 만족하는 [[c]]의 값을 구하시오.\n"
              "(단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.02 < A - B < 0.03]]"),
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 문자 순환소수 0.ȧc0ḃ 텍스트 혼합",
    note="A−B = 90c/9999 → 2.22<c<3.33 → c=3 = 빠른정답 ✓.")

add(id="d1756fad", qtype="short",
    question=("[[A]] = 0.ḃa0ċ, [[B]] = 0.ḃ0aċ일 때, 다음 부등식을 만족하는 [[a]]의 값을 구하시오. "
              "(단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.07 < A - B < 0.08]]"),
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 문자 순환소수 0.ḃa0ċ 텍스트 혼합",
    note="A−B = 90a/9999 → 7.78<a<8.89 → a=8. 빠른정답 5와 불일치.")

add(id="bc283824", qtype="choice",
    question="다음 중 순환소수 [[x = 0.3525252]]⋯에 대한 옳지 않은 것은?",
    choices=["유리수이다.", "순환마디는 52이다.", "[[recdec(0.35, 2)]]보다 크다.",
             "분수로 나타내면 [[frac(349, 900)]]이다.", "[[recdec(0.3, 52)]]로 나타낼 수 있다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="x = 3490/9900 = 349/990 → ④ = 빠른정답 ✓.")

add(id="518f3cf4", qtype="choice",
    question="[[x = 1.24242424]]⋯에 대한 설명으로 옳지 않은 것은?",
    choices=["유리수이다.", "[[recdec(1, 24)]]로 나타낼 수 있다.", "순환마디는 24이다.",
             "[[100x - 10x]]를 이용하여 분수로 나타낼 수 있다.", "분수로 나타내면 [[frac(41, 33)]]이다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="100x−x를 이용해야 함 → ④ = 빠른정답 ✓.")

add(id="e06d76ce", qtype="choice",
    question="다음 중 순환소수 [[x = 1.201201201]]⋯에 대한 설명으로 옳지 않은 것은?",
    choices=["순환소수이다.", "순환마디는 201이다.", "[[recdec(1, 201)]]로 나타낼 수 있다.",
             "기약분수로 나타내면 [[frac(40, 33)]]이다.", "분수로 고칠 때, 가장 편리한 식은 [[1000x - x]]이다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="1200/999 = 400/333 → ④. 빠른정답 3과 불일치.")

add(id="fcba60ea", qtype="choice",
    question="[[x = 1.05252]]⋯에 대하여 다음 중 옳지 않은 것을 모두 고르면?",
    choices=["유리수이다.", "순환마디는 25이다.", "[[1000x - 100x]]는 정수이다.",
             "[[x = recdec(1.0, 52)]]이다.", "분수로 나타내면 [[frac(521, 495)]]이다."],
    derived_answer="②, ③", figure=None, difficulty_est=2, confidence=0.9,
    note="순환마디 52, 정수가 되는 것은 1000x−10x → ②, ③. 빠른정답 4와 불일치.")

add(id="151c5e63", qtype="choice",
    question="다음 중 유리수가 아닌 것은?",
    choices=["[[-3]]", "[[2.45]]", "[[4.010101]]⋯", "[[recdec(3.7, 62)]]", "[[0.10100100001]]⋯"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="⑤는 순환하지 않는 무한소수 → ⑤. 빠른정답 4와 불일치.")

# ---------------- 일차함수의 식 구하기
add(id="3fdfd4cc", qtype="short",
    question=("일차함수 [[f(x)]]가 상수 [[a]], [[b]]에 대하여 [[frac(f(b) - f(a), a - b) = 2]]를 만족시키고 "
              "[[y = f(x)]]의 그래프가 점 [[point(-1, 8)]]을 지날 때, [[f(2)]]의 값을 구하시오.\n(단, [[a != b]])"),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 −2, f(x) = −2x+6 → f(2) = 2. 빠른정답 없음.")

add(id="7279869a", qtype="choice",
    question=("두 점 [[point(6, -8)]], [[point(3, -2)]]를 지나는 직선과 평행하고 점 [[point(0, -4)]]를 지나는 직선을 그래프로 하는 "
              "일차함수의 식을 [[y = f(x)]]라 할 때, [[f(4) - f(-2)]]의 값은?"),
    choices=["[[-12]]", "[[-10]]", "[[-8]]", "[[-6]]", "[[-4]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="f(x) = −2x−4 → −12−0 = −12 → ①. 빠른정답 없음.")

add(id="571c8a07", qtype="short",
    question=("일차함수 [[y = a x + b]]의 그래프를 그리려는데 윤경이는 [[x]]의 계수를 잘못 보고 그려서 그래프가 두 점 "
              "[[point(-2, 1)]], [[point(3, 2)]]를 지나는 직선이 되었고 수정이는 상수항을 잘못 보고 그려서 그래프가 두 점 "
              "[[point(0, 2)]], [[point(-1, 4)]]를 지나는 직선이 되었을 때, 바르게 그려진 일차함수의 그래프의 [[x]]절편을 구하시오. "
              "(단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="frac(7,10)", figure=None, difficulty_est=3, confidence=0.9,
    note="b = 7/5, a = −2 → x절편 7/10 = 빠른정답 ✓.")

add(id="71cf7026", qtype="short",
    question=("일차함수 [[y = a x + b]]의 그래프가 다음 조건을 모두 만족할 때, 상수 [[a]], [[b]]에 대하여 [[3a - b]]의 값을 구하시오. "
              "(단, [[a > 0]])\n(가) 점 [[point(3, 0)]]을 지난다.\n(나) 이 그래프와 [[x]]축 및 [[y]]축으로 둘러싸인 도형의 넓이는 6이다."),
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.9,
    note="|b|=4, b=−3a<0 → b=−4, a=4/3 → 3a−b = 8. 빠른정답 9와 불일치.")

# ---------------- 일차함수의 활용
_TEMP = ("지면으로부터 높이가 {h} m 높아질 때마다 기온이 {t}℃씩 내려간다고 {s}, {p} □ 안에 알맞은 수를 써넣으시오.\n"
         "지면으로부터 높이가 {h} m 높아질 때마다 기온이 {t}℃씩 내려가므로 1 m 높아질 때마다 기온이 □℃씩 내려간다.")
dup(["9526de52", "a0dc7ff5"], qtype="short",
    question=_TEMP.format(h="100", t="0.5", s="할 때", p="다음의"),
    choices=None, derived_answer="0.005", figure=None, difficulty_est=1, confidence=0.9,
    note="0.5÷100 = 0.005. 같은 이미지에 id 2개 → 동일 전사. 빠른정답 없음.")
add(id="ebbf868e", qtype="short",
    question=_TEMP.format(h="200", t="0.8", s="한다. 지면의 기온이 23℃일 때", p="다음"),
    choices=None, derived_answer="0.004", figure=None, difficulty_est=1, confidence=0.9,
    note="0.8÷200 = 0.004. 빠른정답 없음.")
add(id="6dba5533", qtype="short",
    question=_TEMP.format(h="150", t="0.9", s="한다. 지면의 기온이 26℃일 때", p="다음"),
    choices=None, derived_answer="0.006", figure=None, difficulty_est=1, confidence=0.9,
    note="0.9÷150 = 0.006. 빠른정답 없음.")

add(id="b8fef912", qtype="short",
    question=("다음 그림에서 점 P는 점 B를 출발하여 점 C까지 매초 3 cm의 속력으로 [[seg(BC)]] 위를 움직인다. "
              "점 P가 점 B를 출발한 지 몇 초 후에 삼각형 ABP와 삼각형 DPC의 넓이의 합이 120 cm²가 되는지 구하시오."),
    choices=None, derived_answer="4초 후",
    figure=[{"fn": "unsupported", "args": {"raw": "선분 BC(24 cm) 위를 B에서 C로 움직이는 점 P(화살표), AB=12 cm(B에서 수직), DC=8 cm(C 위쪽), 삼각형 ABP와 삼각형 DPC 색칠"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 선분 위 동점 P와 두 삼각형(치수 표시) 도형",
    note="18t + (96−12t) = 120 → t = 4 → 4초 후 = 빠른정답 ✓.")

add(id="bb42e992", qtype="choice",
    question=("다음 그림과 같은 사다리꼴 ABCD에서 점 P는 꼭짓점 A를 출발하여 변 AD를 따라 꼭짓점 D까지 3초에 1 cm씩 움직이고 "
              "점 Q는 꼭짓점 B를 출발하여 변 BC를 따라 꼭짓점 C까지 4초에 1 cm씩 움직인다. 두 점 P, Q가 동시에 출발한 지 몇 초 후에 "
              "사각형 AQCP의 넓이가 133 cm²가 되는가?"),
    choices=["8초", "10초", "12초", "14초", "16초"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD: 윗변 AD=12 cm, 왼쪽 변 AB=14 cm(∠A=∠B=90°), 아랫변 BC=18 cm, AD 위의 점 P, BC 위의 점 Q, 사각형 AQCP 색칠"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 사다리꼴과 동점 P, Q 도형",
    note="AQCP = 126 + 7t/12 = 133 → t = 12 → ③. 빠른정답 없음.")

# ---------------- 일차함수의 그래프의 성질
add(id="faca51ae", qtype="short",
    question="[[a > 0]], [[b < 0]]일 때, 일차함수 [[y = -a x + b]]의 그래프가 지나지 않는 사분면을 구하시오.",
    choices=None, derived_answer="제1사분면", figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 음수, y절편 음수 → 제2, 3, 4사분면을 지남 → 제1사분면. 빠른정답 4와 불일치.")

_LINE_CH = {"pp": "기울기가 양수이고 [[y]]절편이 양수인 직선", "pn": "기울기가 양수이고 [[y]]절편이 음수인 직선",
            "np": "기울기가 음수이고 [[y]]절편이 양수인 직선", "nn": "기울기가 음수이고 [[y]]절편이 음수인 직선",
            "o": "원점을 지나고 기울기가 양수인 직선"}
add(id="48d4fb0f", qtype="choice",
    question="[[a b < 0]], [[a - b > 0]]일 때, 다음 중 일차함수 [[y = a x - b]]의 그래프로 알맞은 것은?",
    choices=[_LINE_CH["pp"], _LINE_CH["o"], _LINE_CH["nn"], _LINE_CH["np"], _LINE_CH["pn"]],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "선지 ①~⑤가 좌표평면 위 직선 그래프: ① 오른쪽 위로 향하고 y절편 양수 ② 원점을 지나며 오른쪽 위 ③ 오른쪽 아래로 향하고 y절편 음수 ④ 오른쪽 아래로 향하고 y절편 양수 ⑤ 오른쪽 위로 향하고 y절편 음수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 선지 5개가 좌표평면 위 직선 그래프",
    note="a>0, b<0 → 기울기 양수, y절편 −b>0 → ①. 빠른정답 4와 불일치.")

add(id="f2ffd0d1", qtype="choice",
    question="[[a b < 0]], [[a - b > 0]]일 때, 다음 중 일차함수 [[y = -a x + b]]의 그래프로 알맞은 것은?",
    choices=[_LINE_CH["pp"], _LINE_CH["np"], _LINE_CH["nn"], _LINE_CH["pn"], _LINE_CH["o"]],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "선지 ①~⑤가 좌표평면 위 직선 그래프: ① 오른쪽 위로 향하고 y절편 양수 ② 오른쪽 아래로 향하고 y절편 양수 ③ 오른쪽 아래로 향하고 y절편 음수 ④ 오른쪽 위로 향하고 y절편 음수 ⑤ 원점을 지나며 오른쪽 위"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 선지 5개가 좌표평면 위 직선 그래프",
    note="a>0, b<0 → 기울기 −a<0, y절편 b<0 → ③. 빠른정답 없음.")

add(id="e9993bc6", qtype="choice",
    question="[[a b > 0]], [[b c < 0]]일 때, 일차함수 [[y = -frac(a, b) x + frac(3c, a)]]의 그래프가 지나는 사분면은?",
    choices=["제1, 2사분면", "제1, 2, 3사분면", "제1, 2, 4사분면", "제1, 3, 4사분면", "제2, 3, 4사분면"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 −a/b<0, y절편 3c/a<0 → 제2, 3, 4사분면 → ⑤. 빠른정답 2와 불일치.")

add(id="c6a54a72", qtype="choice",
    question="[[a b < 0]], [[a c > 0]]일 때, 일차함수 [[y = -frac(b, a) x - frac(c, b)]]의 그래프가 지나지 않는 사분면은?",
    choices=["제1사분면", "제2사분면", "제3사분면", "제4사분면", "알 수 없다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 −b/a>0, y절편 −c/b>0 → 제1, 2, 3사분면 → 제4사분면 ④. 빠른정답 3과 불일치.")

add(id="5c7f2e01", qtype="choice",
    question="일차함수 [[y = a x + b]]의 그래프가 아래 그림과 같을 때, 다음 중 옳은 것은?",
    choices=["[[a < 0]], [[b < 0]]", "[[a < 0]], [[b > 0]]", "[[a > 0]], [[b > 0]]", "[[a > 0]], [[b < 0]]", "[[a b < 0]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 오른쪽 아래로 향하는 직선, x절편 음수, y절편 음수"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 위 직선 그래프",
    note="기울기 음수, y절편 음수 → ①. 빠른정답 4와 불일치.")

add(id="c25f170a", qtype="choice",
    question="일차함수 [[y = a x + b]]가 제3사분면을 지나지 않을 때, [[y = b x + a]]가 지나지 않는 사분면은?",
    choices=["제1사분면", "제2사분면", "제3사분면", "제4사분면", "제1, 2사분면"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="a<0, b>0 → y=bx+a는 제1, 3, 4사분면 → 제2사분면 ②. 빠른정답 3과 불일치.")

add(id="22b8c09c", qtype="short",
    question=("일차함수 [[y = -a x + a b]]의 그래프가 제1, 3, 4사분면을 지날 때, [[x]]에 대한 일차부등식 [[a x - 3a > b x - 3b]]를 "
              "만족시키는 가장 큰 정수 [[x]]의 값을 구하시오.\n(단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.9,
    note="a<0, b>0 → (a−b)x > 3(a−b), a−b<0 → x<3 → 2 = 빠른정답 ✓.")

add(id="6b85e37a", qtype="choice",
    question=("상수 [[a]], [[b]]에 대하여 좌표평면 위의 두 직선 [[y = a x - 3]], [[y = -2x + b]]의 교점이 [[point(1, 5)]]일 때, "
              "두 직선과 [[y]]축으로 둘러싸인 삼각형의 넓이는?"),
    choices=["[[frac(7,2)]]", "[[4]]", "[[frac(9,2)]]", "[[5]]", "[[frac(11,2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a=8, b=7; y절편 −3, 7 → 밑변 10, 높이 1 → 5 → ④ = 빠른정답 ✓.")

add(id="33a0cf3d", qtype="choice",
    question=("상수 [[a]], [[b]]에 대하여 좌표평면 위의 두 직선 [[y = a x + 4]], [[y = 5x + b]]의 교점의 좌표가 [[point(3, 6)]]일 때, "
              "두 직선과 [[x]]축으로 둘러싸인 삼각형의 넓이는?"),
    choices=["[[frac(111,5)]]", "[[frac(113,5)]]", "[[23]]", "[[frac(117,5)]]", "[[frac(119,5)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="a=2/3, b=−9; x절편 −6, 9/5 → 밑변 39/5, 높이 6 → 117/5 → ④ = 빠른정답 ✓.")

add(id="62eec11c", qtype="choice",
    question=("그림과 같이 두 직선 [[y = a x + b]]와 [[y = b x + a]]가 [[y]]축과 만나는 점을 각각 A, B라 하고, 이 두 직선이 만나는 점을 "
              "C라 하자. 점 C의 [[y]]좌표가 8이고, 삼각형 ABC의 넓이가 3일 때, [[2a + b]]의 값은? (단, [[0 < a < b]]이다.)"),
    choices=["[[9]]", "[[10]]", "[[11]]", "[[12]]", "[[13]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 두 직선 y=bx+a(가파름), y=ax+b가 제1사분면의 점 C(y좌표 8)에서 만남, y축과의 교점 A(위쪽), B(아래쪽), 삼각형 ABC 음영"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 두 직선과 삼각형 ABC 좌표평면 도형",
    note="출처 [2009년 3월 고1 19번]. C(1, 8): a+b=8, (b−a)/2=3 → a=1, b=7 → 9 → ①. 빠른정답 4와 불일치.")

add(id="e6f4c342", qtype="choice",
    question=("상수 [[a]], [[b]]에 대하여 좌표평면 위의 두 직선 [[y = a x - 8]], [[y = x + b]]의 교점의 좌표가 [[point(3, 4)]]일 때, "
              "두 직선과 [[x]]축으로 둘러싸인 삼각형의 넓이는?"),
    choices=["[[4]]", "[[6]]", "[[8]]", "[[10]]", "[[12]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2011년 3월 고1 13번/3점]. a=4, b=1; x절편 2, −1 → 밑변 3, 높이 4 → 6 → ②. 빠른정답 4와 불일치.")

add(id="68f5bb40", qtype="short",
    question=("평행한 두 일차함수 [[y = frac(1,4) x + 1]], [[y = a x + b]]의 그래프가 [[x]]축과 만나는 점을 각각 P, Q라 하자. "
              "[[seg(PQ) = 2]]일 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값 중 가장 큰 것을 구하시오."),
    choices=None, derived_answer="frac(7,4)", figure=None, difficulty_est=3, confidence=0.9,
    note="a=1/4, P(−4,0), Q(−4b,0), |4−4b|=2 → b=1/2 또는 3/2 → 최대 7/4 = 빠른정답 ✓.")

add(id="f751e388", qtype="choice",
    question="다음 중 [[y = -x]]에 대한 설명으로 옳은 것은?",
    choices=["점 [[point(-3, -3)]]을 지난다.", "[[x]]가 증가할 때 [[y]]가 증가하는 그래프이다.",
             "그래프는 제3사분면을 반드시 지난다.", "[[y = -2x]]보다 [[x]]축에 가깝다.", "[[f(frac(1,2)) = 2]]이다."],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="④만 옳음(①은 (−3,3), ② 감소, ③ 제2·4사분면, ⑤ −1/2). 빠른정답 3과 불일치.")

add(id="ef25dc26", qtype="choice",
    question="그래프는 일차함수 [[y = a x + b]]의 그래프이다. 이 그래프에 대한 다음 설명 중 옳지 않은 것은?",
    choices=["[[x = 1]]일 때, 함숫값이 [[-3]]이다.", "[[x]]절편은 [[-5]]이다.", "[[x]]의 값이 증가하면 [[y]]의 값은 감소한다.",
             "[[y = 5x + 2]]의 그래프와 [[y]]축에 대하여 대칭이다.", "[[y = -5x]]의 그래프를 [[y]]축의 방향으로 2만큼 평행이동한 그래프이다."],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 두 점 (−1, 7), (1, −3)을 지나는 오른쪽 아래로 향하는 직선(점선으로 좌표 표시)"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 좌표평면 위 직선 그래프 / 이미지 상단 잘림(첫 줄이 '그래프는'으로 시작, 앞 낱말 누락 가능)",
    note="y = −5x+2 → x절편 2/5 → ②. 빠른정답 1과 불일치.")

# ---------------- 단항식의 곱셈과 나눗셈
add(id="abb63233", qtype="choice",
    question="[[frac(2,3) a pow(b,3) × 3 pow(a,2) b]]를 계산하면?",
    choices=["[[2 pow(a,2) pow(b,4)]]", "[[3 pow(a,3) pow(b,4)]]", "[[2 pow(a,3) pow(b,4)]]", "[[3 pow(a,3) pow(b,3)]]", "[[2 pow(a,3) pow(b,5)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="2a³b⁴ → ③. 빠른정답 2와 불일치.")

add(id="2ed328ed", qtype="short",
    question=("다음 □ 안에 알맞은 것을 써넣으시오.\n[[(-3a) × 5b = (-3) × a × 5 × b]]\n= {[[(-3) × 5]]} × [[(a × b)]]\n= □[[a b]]"),
    choices=None, derived_answer="-15", figure=None, difficulty_est=1, confidence=0.9,
    note="(−3)×5 = −15. 빠른정답 5와 불일치.")

add(id="e8c9574d", qtype="short",
    question=("다음 □ 안에 알맞은 수를 써넣으시오.\n[[3a × (-7b) = 3 × a × (-7) × b]]\n= {[[3 × (-7)]]} × [[(a × b)]]\n= □[[a b]]"),
    choices=None, derived_answer="-21", figure=None, difficulty_est=1, confidence=0.9,
    note="3×(−7) = −21. 빠른정답 3과 불일치.")

add(id="b1201b92", qtype="short",
    question=("[[A pow(x,2) pow(y,3) × pow(-x y, B) = -5 pow(x, C) pow(y, 6)]]일 때, 자연수 [[A]], [[B]], [[C]]에 대하여 "
              "[[A + B - C]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="B=3, A=5, C=5 → 3. 빠른정답 4와 불일치.")

add(id="bcdcaa50", qtype="choice",
    question=("[[pow(-3x y, 3) × pow(2 pow(x,2) y, 2) × 5 pow(x,4) pow(y,3) = a pow(x, b + 1) pow(y, c)]]일 때, "
              "상수 [[a]], [[b]], [[c]]에 대하여 [[a + 15b + 30c]]의 값은?"),
    choices=["[[-180]]", "[[-150]]", "[[-110]]", "[[-90]]", "[[-50]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="−540x¹¹y⁸ → a=−540, b=10, c=8 → −150 → ②. 빠른정답 3과 불일치.")

add(id="54c86f93", qtype="choice",
    question="[[12 pow(x,5) pow(y,9) ÷ (-6 pow(x,3) pow(y,4)) ÷ (frac(1,3) pow(x,6) pow(y,3))]]을 간단히 하면?",
    choices=["[[-frac(6 pow(y,2), pow(x,4))]]", "[[-frac(2 pow(y,2), 3 pow(x,4))]]", "[[-frac(2, 3 pow(x,4) pow(y,2))]]",
             "[[frac(6, pow(x,4) pow(y,2))]]", "[[frac(24 pow(x,4), pow(y,2))]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="−6y²/x⁴ → ① = 빠른정답 ✓. 나누는 단항식은 괄호로 묶음.")

add(id="e6b18829", qtype="choice",
    question=("[[32 pow(x,5) pow(y,4) ÷ (-4x y) ÷ pow(-4x pow(y,3), 3) = frac(pow(x,c), a pow(y,b))]]일 때,\n"
              "상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값은?"),
    choices=["[[11]]", "[[13]]", "[[15]]", "[[17]]", "[[19]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="x/(8y⁶) → a=8, b=6, c=1 → 15 → ③. 빠른정답 1과 불일치.")

add(id="18f171fe", qtype="choice",
    question=("[[16 pow(x,10) pow(y,4) ÷ (4x y) ÷ pow(-2x pow(y,2), 3) = frac(pow(x,c), a pow(y,b))]]일 때,\n"
              "상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값은?"),
    choices=["[[1]]", "[[3]]", "[[5]]", "[[7]]", "[[9]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="x⁶/(−2y³) → a=−2, b=3, c=6 → 7 → ④. 빠른정답 1과 불일치. 나누는 단항식 4xy는 괄호로 묶음.")

add(id="2afee78f", qtype="short",
    question=("[[21 pow(x,5) pow(y,A) ÷ pow(B x y, 3) ÷ frac(pow(y,4), 8 pow(x,2)) = frac(21 pow(x,C), pow(y,6))]]일 때,\n"
              "자연수 [[A]], [[B]], [[C]]에 대하여 [[A + B + C]]의 값을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.9,
    note="168/B³=21 → B=2, C=4, A=1 → 7. 빠른정답 3과 불일치.")

add(id="f10d0b91", qtype="choice",
    question="다음 중 계산 결과가 옳은 것을 모두 고른 것은? (정답 2개)",
    choices=["[[6 pow(a,3) ÷ (2a b) = frac(3 pow(a,3), b)]]",
             "[[frac(1,3) pow(x,3) y ÷ (frac(1,9) pow(x,2) pow(y,2)) = frac(3x, y)]]",
             "[[pow(pow(x,2), 3) ÷ pow(-2 pow(x,2), 3) = -frac(1,6)]]",
             "[[pow(-pow(x,2) y, 2) ÷ (frac(1,3) x y) = 3 pow(x,3) y]]",
             "[[pow(-pow(x,2) y, 3) ÷ (2x pow(y,3)) = -frac(pow(x,5), 3)]]"],
    derived_answer="②, ④", figure=None, difficulty_est=2, confidence=0.9,
    note="② 3x/y ✓, ④ 3x³y ✓ (① 3a²/b, ③ −1/8, ⑤ −x⁵/2) → ②, ④. 빠른정답 4와 불일치. 나누는 단항식은 괄호로 묶음.")

add(id="5a95df56", qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["[[6x y ÷ (3y) = 2x]]", "[[(-4 pow(a,4)) ÷ (3 pow(a,2)) = -frac(4 pow(a,2), 3)]]",
             "[[12 pow(m,2) ÷ (-3 pow(m,3)) = -4m]]", "[[15 pow(a,2) b ÷ (3a pow(b,3)) = frac(5a, pow(b,2))]]",
             "[[3 pow(x,7) ÷ (12 pow(x,5)) = frac(pow(x,2), 4)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="③ 12m²÷(−3m³) = −4/m → ③. 빠른정답 '2, 4'와 불일치. 나누는 단항식은 괄호로 묶음.")

add(id="46c6384a", qtype="short",
    question=("두 문자 [[a]], [[b]]에 대하여 기호 ○, □를 [[a]]○[[b]] = [[a pow(b,2)]], [[a]]□[[b]] = [[4a b]]라 약속할 때, "
              "([[a]]○([[b]]□[[a]]))/([[b]]□([[b]]○[[a]]))를 구하시오."),
    choices=None, derived_answer="4a", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 ○·□ 연산 텍스트 혼합(분수 형태)",
    note="b□a=4ab, a○4ab=16a³b², b○a=a²b, b□a²b=4a²b² → 4a. 빠른정답 3과 불일치.")

add(id="e30f09a3", qtype="choice",
    question="[[2a pow(b,2) ÷ (3a b) × pow(a,2)]]을 간단히 하면?",
    choices=["[[frac(2,3) a b]]", "[[frac(2,3) pow(a,2) b]]", "[[frac(2,3) pow(a,2) pow(b,2)]]", "[[frac(2,3) a pow(b,2)]]", "[[frac(3,2) a pow(b,2)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="(2/3)a²b → ②. 빠른정답 '1, 3'과 불일치. 나누는 단항식은 괄호로 묶음.")

add(id="63a9438c", qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["[[32 pow(x,3) y ÷ (4 pow(x,2) y) × 2x = 16 pow(x,2)]]",
             "[[pow(-2x, 2) × (-3 pow(x,3)) ÷ pow(2 pow(x,2), 2) = -3x]]",
             "[[-4 pow(pow(x,2), 2) ÷ (2 pow(x,4)) × 3 pow(x,4) = -6 pow(x,4)]]",
             "[[pow(-2 pow(x,2) y, 3) × pow(-2x y, 2) ÷ pow(2x pow(y,2), 2) = 8 pow(x,6) y]]",
             "[[pow(-pow(x,2) pow(y,3), 2) ÷ pow(frac(1,3) x y, 2) × pow(2 pow(x,2) y, 3) = 72 pow(x,8) pow(y,7)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="④는 −8x⁶y → ④. 빠른정답 5와 불일치. 나누는 단항식은 괄호로 묶음.")

add(id="c431f70c", qtype="choice",
    question="다음 중 옳은 것을 모두 고르면? (정답 2개)",
    choices=["[[pow(a pow(b,2), 3) × pow(frac(a, pow(b,3)), 3) ÷ pow(frac(1, a b), 3) = pow(a,6)]]",
             "[[pow(pow(a,2), 3) × 2 pow(a,3) ÷ pow(2a, 3) = frac(pow(a,6), 4)]]",
             "[[12 pow(x,2) pow(y,3) ÷ (-4x pow(y,4)) × pow(-2x y, 3) = -24 pow(x,4) pow(y,2)]]",
             "[[pow(-2x, 3) ÷ (-4x) ÷ (frac(2,3) x) = 3 pow(x,3)]]",
             "[[5x y × (-4y) ÷ (2x y) = -10y]]"],
    derived_answer="②, ⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="② a⁶/4 ✓, ⑤ −10y ✓ (① a⁹, ③ 24x⁴y², ④ 3x) → ②, ⑤. 빠른정답 85와 불일치. 나누는 단항식은 괄호로 묶음.")

add(id="1a3250b5", qtype="choice",
    question="[[-21 pow(x,3) pow(y,2)]] ÷ □ = [[7x y]]에서 □ 안에 알맞은 것은?",
    choices=["[[-3 pow(x,2) y]]", "[[-3 pow(x,2) pow(y,2)]]", "[[-3x pow(y,2)]]", "[[3 pow(x,2) y]]", "[[3x pow(y,2)]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="−21x³y²÷7xy = −3x²y → ①. 빠른정답 '2, 5'와 불일치.")

add(id="37fbb6b1", qtype="choice",
    question="[[-4a b]] × □ = [[12 pow(a,3) pow(b,2)]]일 때, □ 안에 알맞은 식은?",
    choices=["[[-3 pow(a,2) b]]", "[[-3a pow(b,2)]]", "[[-pow(a,2) b]]", "[[pow(a,2) b]]", "[[3 pow(a,2) b]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="12a³b²÷(−4ab) = −3a²b → ①. 빠른정답 −56과 불일치.")

add(id="faf5287c", qtype="choice",
    question=("[[pow(frac(3, 2a b), 3)]] ÷ □ × [[pow(-frac(2,5) pow(a,3) pow(b,2), 2)]] = [[frac(3a, 5 pow(b,2))]]일 때, "
              "□ 안에 알맞은 식은?"),
    choices=["[[frac(10b, 3 pow(a,2))]]", "[[frac(3a b, 5)]]", "[[frac(9 pow(a,2) pow(b,3), 10)]]", "[[8a pow(b,2)]]", "[[frac(15a, 4 pow(b,2))]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="(27/50)a³b ÷ □ = 3a/(5b²) → □ = 9a²b³/10 → ③. 빠른정답 1과 불일치.")

add(id="ae305c0c", qtype="choice",
    question="[[12 pow(x,2) pow(y,2)]] ÷ □ × [[pow(-2y, 2)]] = [[frac(12 pow(y,2), x)]]일 때, □ 안에 알맞은 식은?",
    choices=["[[-2x pow(y,3)]]", "[[-4 pow(x,2) pow(y,3)]]", "[[2 pow(x,2) y]]", "[[4 pow(x,3) pow(y,2)]]", "[[6 pow(x,3) pow(y,3)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="48x²y⁴ × x/(12y²) = 4x³y² → ④. 빠른정답 1과 불일치.")

add(id="fb3b1bbd", qtype="choice",
    question="[[(-12x pow(y,2))]] ÷ □ × [[3 pow(x,2)]] = [[-6 pow(x,2) y]]일 때, □의 값은?",
    choices=["[[6x y]]", "[[-frac(4,3) x y]]", "[[-6 pow(x,2) y]]", "[[-12x pow(y,2)]]", "[[frac(4,3) pow(x,2) y]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="−36x³y²/□ = −6x²y → □ = 6xy → ①. 빠른정답 3과 불일치.")

add(id="168ff9e9", qtype="choice",
    question="□ ÷ [[(-8 pow(x,6) pow(y,3))]] × [[pow(-4 pow(x,3) y, 2)]] = [[-6 pow(x,5) pow(y,2)]]일 때,\n□ 안에 알맞은 식은?",
    choices=["[[-3 pow(x,5) pow(y,3)]]", "[[-3 pow(x,3) y]]", "[[3 pow(x,2) pow(y,3)]]", "[[3 pow(x,5) pow(y,3)]]", "[[3 pow(x,5) pow(y,6)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="□ × (−2/y) = −6x⁵y² → □ = 3x⁵y³ → ④. 빠른정답 3과 불일치.")

add(id="c573da07", qtype="choice",
    question=("[[pow(pow(a,4) pow(b,2), 2) × pow(frac(3 pow(b,3), 2a), 2)]] ÷ □ = [[frac(9,4) pow(a,3) pow(b,5)]]일 때, "
              "□ 안에 알맞은 식은?"),
    choices=["[[frac(1, pow(a,5) pow(b,5))]]", "[[pow(a,5) pow(b,5)]]", "[[pow(a,5) pow(b,3)]]", "[[pow(a,3) b]]", "[[pow(a,3) pow(b,5)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="(9/4)a⁶b¹⁰ ÷ □ = (9/4)a³b⁵ → □ = a³b⁵ → ⑤. 빠른정답 1과 불일치.")

add(id="8d7dfdbb", qtype="choice",
    question="[[pow(-2 pow(x,2) y, 3) ÷ (pow(x,2) pow(y,3))]] × □ = [[-16 pow(x,3) y]]일 때, □ 안에 알맞은 식은?",
    choices=["[[frac(2y, x)]]", "[[frac(8y, x)]]", "[[2x y]]", "[[2 pow(x,2) y]]", "[[8x y]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="−8x⁴ × □ = −16x³y → □ = 2y/x → ①. 빠른정답 2와 불일치. 나누는 단항식은 괄호로 묶음.")

add(id="ae6535ac", qtype="choice",
    question=("두 식 [[a]], [[b]]에 대하여 △, ◎를 [[a]]△[[b]] = [[a pow(b,2)]], [[a]]◎[[b]] = [[3 pow(a,2) b]]로 약속하자. "
              "이때 다음을 만족시키는 두 식 [[A]], [[B]]에 대하여 [[5 pow(A,2) ÷ (2B)]]를 계산하면?\n"
              "[[A]]△[[2x]] = [[8 pow(x,3) pow(y,2)]], [[y]]◎[[B]] = [[15 pow(x,2) pow(y,3)]]"),
    choices=["[[frac(2, x pow(y,3))]]", "[[frac(1, 2 pow(x,2) y)]]", "[[frac(1, 2 pow(y,3))]]", "[[frac(x pow(y,3), 2)]]", "[[2 pow(y,3)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 △·◎ 연산 텍스트 혼합",
    note="A=2xy², B=5x²y → 5A²÷2B = 2y³ → ⑤ = 빠른정답 ✓. 나누는 단항식 2B는 괄호로 묶음.")
