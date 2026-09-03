# -*- coding: utf-8 -*-
# esc_sonnet_h1-2_2of7 — 이미지 기준 전사 (88 항목 / 80쪽)
# 문서: 260828_집합의 개념과 표현 (63 id) + 무리함수의 그래프 (8) + 두 직선의 평행 조건과 수직 조건 (9) + 대칭이동 (7)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_3A = ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_3B = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ================= 집합의 개념과 표현 =================
# p16
add(id="7150516c", qtype="choice",
    question=("자연수 [[n]]에 대하여 집합\n[[sub(T,n)]] = { [[A]] | [[pow(A, 2n) = E]], [[A]]는 이차정사각행렬 }\n"
              "일 때, 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, [[E]]는 단위행렬이다.)\n<보기>\n"
              "ㄱ. [[in(A, sub(T,1))]]이면 [[in(A, sub(T,3))]]이다.\n"
              "ㄴ. [[in(A, sub(T,2))]]이면 [[in(A, sub(T,1))]]이다.\n"
              "ㄷ. [[in(A, union(sub(T,2), sub(T,3)))]]이면 [[in(A, sub(T,6))]]이다."),
    choices=CH_3A, derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2012년 9월 고2 문과 7번/3점]. ㄱ A²=E⇒A⁶=E ✓, ㄴ A⁴=E인데 A²=-E인 행렬 존재 ✗, ㄷ A⁴=E 또는 A⁶=E⇒A¹²=E ✓ → ③. 빠른정답 2와 불일치.")

# p21
add(id="177b6c1d", qtype="choice",
    question=("집합 [[A]]는 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j) = -sub(a,j,i)]] ([[i]] = 1, 2, [[j]] = 1, 2)를 만족시키는 행렬의 집합이다. "
              "다음 중 집합 [[A]]의 원소인 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[mat(2,2, 0,-3, 3,0)]]\nㄴ. [[mat(2,2, 2,0, 0,-2)]]\nㄷ. [[mat(2,2, 0,0, 0,0)]]\nㄹ. [[mat(2,2, 0,1, 1,0)]]"),
    choices=["ㄱ, ㄷ", "ㄱ, ㄹ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="a₁₁=a₂₂=0, a₁₂=-a₂₁ → ㄱ, ㄷ → ①.")

# p22 (id 4개, 같은 문항)
dup(["e065e9c4", "c45652c6", "3ac1a047", "a54c1c9b"], qtype="choice",
    question=("집합 [[A]] = { [[mat(2,2, pow(3,x), 0, 0, 2y)]] | [[x]], [[y]]는 자연수 }에 대하여 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[in(P, A)]], [[in(Q, A)]]이면 [[in(P + Q, A)]]\n"
              "ㄴ. [[in(P, A)]], [[in(Q, A)]]이면 [[in(P Q, A)]]\n"
              "ㄷ. [[in(P, A)]]일 때, [[in(n pow(P, n), A)]]가 되도록 하는 100 이하의 자연수 [[n]]은 4개이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"], derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="ㄱ 3+3=6 ✗, ㄴ 3^(x+x')·4yy' ✓, ㄷ n·3^(nx)가 3의 거듭제곱 ⇔ n=1,3,9,27,81(5개) ✗ → ②.")

# p25
add(id="5a834468", qtype="choice",
    question="10의 약수의 집합을 [[A]], 12의 약수의 집합을 [[B]]라고 할 때, 다음 중 옳은 것을 모두 고르면? (정답 2개)",
    choices=["[[in(10, A)]]", "[[in(12, A)]]", "[[notin(14, A)]]", "[[in(8, B)]]", "[[notin(6, B)]]"],
    derived_answer="①, ③", figure=None, difficulty_est=1, confidence=0.9,
    note="A={1,2,5,10}, B={1,2,3,4,6,12} → ①, ③.")

# p28
add(id="d497bae3", qtype="choice",
    question="방정식 [[pow(x,3) - 2 pow(x,2) - x + 2 = 0]]의 해의 집합을 [[A]]라 할 때, 다음 중 옳지 않은 것은?",
    choices=["[[notin(-2, A)]]", "[[in(-1, A)]]", "[[notin(0, A)]]", "[[in(1, A)]]", "[[notin(2, A)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="(x²-1)(x-2)=0 → A={-1,1,2} → ⑤ 거짓.")

# p29
add(id="703f8cda", qtype="choice",
    question="정수 전체의 집합을 [[Z]], 유리수 전체의 집합을 [[Q]], 실수 전체의 집합을 [[R]]라 할 때, 다음 중 옳은 것은? (단, [[i = sqrt(-1)]])",
    choices=["[[notin(frac(4,2), Z)]]", "[[notin(sqrt(9), Q)]]", "[[in(frac(pi,3), Q)]]", "[[in(sqrt(2), R)]]", "[[notin(pow(i,1000), R)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="4/2=2∈Z, √9=3∈Q, π/3∉Q, √2∈R ✓, i¹⁰⁰⁰=1∈R → ④.")

# p30
add(id="642091ed", qtype="choice",
    question="6의 양의 약수의 집합을 [[A]], 21의 양의 약수의 집합을 [[B]]라고 할 때, 다음 중 옳은 것은?",
    choices=["[[notin(2, A)]]", "[[in(5, A)]]", "[[in(6, A)]]", "[[notin(7, B)]]", "[[notin(21, B)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="A={1,2,3,6}, B={1,3,7,21} → ③.")

# p35
add(id="62b65337", qtype="choice",
    question="집합 [[A]] = { [[3x + 5y]] | [[x]], [[y]]는 음이 아닌 정수 }에 대하여 다음 중 옳지 않은 것은?",
    choices=["[[notin(4, A)]]", "[[in(11, A)]]", "[[nsubset(set(17), A)]]", "{ [[5m]] | [[m]]은 음이 아닌 정수 } ⊂ [[A]]", "[[subset(setb(8n, in(n, A)), A)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="17=3·4+5·1∈A이므로 {17}⊂A → ③ 거짓. 4∉A ✓, 11=6+5 ✓, ④⑤ ✓.")

# p36
add(id="b18831d6", qtype="choice",
    question="3보다 크고 11보다 작은 홀수의 집합을 [[A]]라고 할 때, 다음 중 옳은 것을 모두 고르면?",
    choices=["[[in(3, A)]]", "[[notin(4, A)]]", "[[in(6, A)]]", "[[notin(9, A)]]", "[[notin(11, A)]]"],
    derived_answer="②, ⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="A={5,7,9} → ②, ⑤.")

# p38
add(id="11807b94", qtype="choice",
    question="7보다 작은 홀수의 집합을 [[A]]라 할 때, 다음 중 옳은 것은?",
    choices=["[[in(0, A)]]", "[[in(3, A)]]", "[[in(4, A)]]", "[[notin(5, A)]]", "[[in(7, A)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="A={1,3,5} → ②.")

# p39
add(id="79846a70", qtype="short",
    question=("다음 조건을 만족시키는 행렬 [[A = mat(2,2, a,b, c,a)]]의 개수를 구하시오.\n"
              "(가) 세 수 [[a]], [[b]], [[c]]는 집합 [[set(-3, -2, -1, 0, 1, 2, 3, 4)]]의 서로 다른 원소이다.\n"
              "(나) 행렬 [[pow(A,2)]]의 모든 성분은 양수이다."),
    choices=None, derived_answer="30", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2014년 6월 고2 문과 28번/4점]. A²=(a²+bc, 2ab; 2ac, a²+bc) → a,b,c 같은 부호·서로 다름: 양수 4·3·2=24, 음수 3·2·1=6 → 30 (파이썬 전수 확인).")

# p40
add(id="05ba9ae5", qtype="choice",
    question="다음 중 집합 [[A]] = {2, 5, 8, 11, 14, ⋯}을 조건제시법으로 나타낸 것은?",
    choices=["[[A]] = { [[x]] | [[x]]는 3으로 나눈 나머지가 1인 자연수 }",
             "[[A]] = { [[x]] | [[x]]는 3으로 나눈 나머지가 2인 자연수 }",
             "[[A]] = { [[x]] | [[x]]는 4로 나눈 나머지가 1인 자연수 }",
             "[[A]] = { [[x]] | [[x]]는 4로 나눈 나머지가 2인 자연수 }",
             "[[A]] = { [[x]] | [[x]]는 4로 나눈 나머지가 3인 자연수 }"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="3k+2 꼴 → ②.")

# p41 (id 4개, 같은 문항)
dup(["50e113ca", "0e0cc900", "be0e75ee", "bd557e09"], qtype="short",
    question=("다음은 원소나열법으로 표현된 집합을 조건제시법으로 나타낸 것이다. 보기 중에서 옳은 것을 있는 대로 고르시오.\n<보기>\n"
              "㉠ {전자레인지, 전화기, 화분, 침대, 이불} = { [[x]] | [[x]]는 전자제품 }\n"
              "㉡ [[set(1, 2, 3, 4)]] = { [[x]] | [[x]]는 자연수를 4로 나누었을 때, 나머지 }\n"
              "㉢ [[set(1, 3, 5, 7, 9)]] = { [[x]] | [[x]]는 10 이하의 홀수 }\n"
              "㉣ [[set(frac(1,2), frac(1,3))]] = {0과 1 사이의 분수}"),
    choices=None, derived_answer=None, figure=None, difficulty_est=1, confidence=0.8,
    needs_review="답 기호 ㉢이 답 문법(ㄱㄴㄷ·①~⑤) 범위 밖이라 answer 미기재",
    note="옳은 것은 ㉢뿐(㉠ 화분·침대·이불은 전자제품 아님, ㉡ 나머지는 0~3, ㉣ 0과 1 사이의 분수는 무수히 많음).")

# p45
add(id="dabfe6bb", qtype="choice",
    question="다음 중 원소나열법은 조건제시법으로, 조건제시법은 원소나열법으로 나타낸 것으로 옳지 않은 것은?",
    choices=["{ [[x]] | [[x]]는 계절 } → {봄, 여름, 가을, 겨울}",
             "[[set(3, 6, 9)]] → { [[x]] | [[x]]는 3의 배수인 한 자리 자연수 }",
             "{ [[x]] | [[x]]는 100 미만의 2의 양의 배수 } → {2, 4, 6, ⋯, 98}",
             "{1, 2, ⋯, 50} → { [[x]] | [[x]]는 50 미만의 자연수 }",
             "{ [[x]] | [[x]]는 9의 양의 약수 } → [[set(1, 3, 9)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="50은 50 미만이 아님 → ④.")

# p46
add(id="96c3466b", qtype="choice",
    question=("자연수 [[n]]에 대하여 집합 [[sub(A,n)]]을\n[[sub(A,n)]] = { [[z]] | [[pow(z,n) = 1]], [[z]]는 복소수 }\n"
              "라 정의하자. [[sub(A,n)]]이 다음 두 조건을 만족할 때, [[n]]의 최솟값은? (단, [[i = sqrt(-1)]])\n"
              "(가) [[in(frac(-1 + sqrt(3) i, 2), sub(A,n))]]\n(나) [[in(z, sub(A,n))]]이면 [[in(-z, sub(A,n))]]이다."),
    choices=["3", "4", "5", "6", "7"], derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2011년 9월 고1 15번/4점]. (가) 3|n, (나) n 짝수 → n=6 → ④.")

# p47
add(id="8f7d17ec", qtype="short",
    question=("[[A]] = { [[x]] | [[x = 4 pow(n,2) + 3]], [[n]]은 [[n < 4]]인 자연수 },\n"
              "[[B]] = { [[y]] | [[y]]는 [[x]]를 6으로 나누었을 때의 나머지, [[in(x, A)]] }에 대하여 집합 [[B]]의 모든 원소의 합을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="A={7,19,39} → 나머지 {1,3} → 합 4 = 빠른정답 ✓.")

# p48
add(id="b8531ae5", qtype="short",
    question=("[[A]] = { [[x]] | [[x = 3 pow(n,2) + 10]], [[n]]은 [[n < 5]]인 자연수 },\n"
              "[[B]] = { [[y]] | [[y]]는 [[x]]를 7로 나누었을 때의 나머지, [[in(x, A)]] }에 대하여 집합 [[B]]의 모든 원소의 합을 구하시오."),
    choices=None, derived_answer="9", figure=None, difficulty_est=1, confidence=0.9,
    note="A={13,22,37,58} → 나머지 {6,1,2} → 합 9.")

# p49
add(id="eec5923f", qtype="short",
    question=("서로 다른 세 자연수를 원소로 갖는 집합 [[A = set(a, b, c)]]에 대하여 집합 [[B]]를 [[B]] = { [[x + y]] | [[in(x, A)]], [[in(y, A)]], [[x != y]] }라 하자. "
              "집합 [[B = set(9, 14, 17)]]일 때, 집합 [[A]]의 원소 중 가장 큰 수를 구하시오."),
    choices=None, derived_answer="11", figure=None, difficulty_est=2, confidence=0.9,
    note="a+b+c=20 → A={3,6,11} → 11.")

# p50
add(id="5e0e0215", qtype="short",
    question=("두 집합\n[[A]] = { [[x]] | [[x = 2 pow(n,2) + 1]], [[n]]은 [[n <= 5]]인 자연수 },\n"
              "[[B]] = { [[y]] | [[y]]는 [[x]]를 5로 나누었을 때의 나머지, [[in(x, A)]] }에 대하여 집합 [[B]]의 모든 원소의 합을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="A={3,9,19,33,51} → 나머지 {3,4,1} → 합 8. 빠른정답 4와 불일치.")

# p52
add(id="3c13ad90", qtype="choice",
    question="집합 [[A]] = { [[x]] | [[x = 4 pow(m,2) - pow(n,2)]], [[m]], [[n]]은 정수 }의 원소만을 보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. 15\nㄴ. 18\nㄷ. 20",
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(2m-n)(2m+n): 15=1·15 ✓, 18은 같은 홀짝 인수분해 불가 ✗, 20=2·10 ✓ → ④.")

# p53
add(id="b9af4ed2", qtype="choice",
    question="집합 [[A]] = { [[x]] | [[x = 4 pow(m,2) - pow(n,2)]], [[m]], [[n]]은 정수 }의 원소만을 보기에서 있는 대로 고른것은?\n<보기>\nㄱ. 12\nㄴ. 20\nㄷ. 26",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="12=2·6 ✓, 20=2·10 ✓, 26=2·13(홀짝 다름) ✗ → ③. 빠른정답 8과 불일치.")

# p56
add(id="86e851a9", qtype="choice",
    question="다음 중 유한집합이 아닌 것은?",
    choices=["{ [[x]] | [[x]]는 10의 약수 }", "{ [[x]] | [[x]]는 10보다 작은 홀수 }", "{ [[x]] | [[x]]는 5보다 큰 자연수 }",
             "{ [[x]] | [[x]]는 30보다 작은 5의 배수 }", "{1, 2, 3, ⋯, 49, 50}"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9, note="③ 무한집합.")

# p57
add(id="d003cd5e", qtype="short",
    question="다음 집합이 유한집합이면 ‘유’, 무한집합이면 ‘무’를 ( ) 안에 써넣고, 공집합인 경우에는 ‘공’을 함께 써넣으시오.\n{ [[x]] | [[x]]는 7로 나누어 떨어지는 자연수 } ( )",
    choices=None, derived_answer="무", figure=None, difficulty_est=1, confidence=0.9, note="7의 배수 무한 → 무 = 빠른정답 ✓.")

# p58
add(id="8af287af", qtype="choice",
    question="다음 중 유한집합인 것은?",
    choices=["{1, 3, 5, 7, 9, ⋯}", "{ [[x]] | [[x = 2n]], [[n]]은 자연수 }", "{ [[x]] | [[x]]는 100보다 큰 자연수 }",
             "{ [[x]] | [[x]]는 [[pow(x,2) < 0]]인 유리수 }", "{ [[a + 2b]] | [[0 < a < 1]], [[0 < b < 1]] }"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9, note="④는 공집합(유한) → ④. 빠른정답 '무'와 불일치.")

# p59
add(id="5add5326", qtype="short",
    question="다음 집합이 유한집합이면 ‘유’, 무한집합이면 ‘무’를 ( ) 안에 써넣고, 공집합인 경우에는 ‘공’을 함께 써넣으시오.\n{1, 3, 5, 7, ⋯} ( )",
    choices=None, derived_answer="무", figure=None, difficulty_est=1, confidence=0.9, note="홀수 전체 → 무.")

# p61
add(id="632d16fa", qtype="short",
    question="다음 집합이 유한집합이면 ‘유’, 무한집합이면 ‘무’를 ( ) 안에 써넣으시오.\n{ [[x]] | [[x]]는 8로 나누어떨어지는 자연수 } ( )",
    choices=None, derived_answer="무", figure=None, difficulty_est=1, confidence=0.9, note="8의 배수 무한 → 무 = 빠른정답 ✓.")

# p63
add(id="a278eac4", qtype="short",
    question="다음 집합이 유한집합이면 ‘유’, 무한집합이면 ‘무’를 ( ) 안에 써넣으시오.\n{ [[x]] | [[x]]는 13의 양의 배수 } ( )",
    choices=None, derived_answer="무", figure=None, difficulty_est=1, confidence=0.9, note="13의 양의 배수 무한 → 무. 빠른정답 '유'와 불일치.")

# p64
add(id="981ca761", qtype="short",
    question="다음 집합이 유한집합이면 ‘유’, 무한집합이면 ‘무’를 ( ) 안에 써넣으시오.\n{ [[x]] | [[x]]는 50 이하의 7의 배수 } ( )",
    choices=None, derived_answer="유", figure=None, difficulty_est=1, confidence=0.85, note="7,14,…,49 → 유. 빠른정답 '무'와 불일치(이 문서의 빠른정답 정렬이 한 칸 밀린 듯).")

# p65
add(id="625ee22f", qtype="choice",
    question="다음 중 무한집합이 아닌 것을 모두 고르면?",
    choices=["{ [[x]] | [[x]]는 짝수인 소수 }", "{ [[x]] | [[x]]는 1과 2 사이의 분수 }", "{ [[x]] | [[x]]는 [[x × 0 = 0]]인 자연수 }",
             "{ [[2x + 1]] | [[x]]는 11보다 큰 소수 }", "{ [[x]] | [[1.5 <= x <= 3.5]], [[x]]는 자연수 }"],
    derived_answer="①, ⑤", figure=None, difficulty_est=1, confidence=0.9, note="①={2}, ⑤={2,3} 유한 → ①, ⑤. 빠른정답 '유'와 불일치.")

# p66
add(id="16a84e2f", qtype="choice",
    question="집합 [[X]] = { [[x]] | [[pow(x,2) - 2k x + 7 <= 0]], [[x]]는 실수 }가 유한집합이 되도록 하는 실수 [[k]]의 최댓값은?",
    choices=["[[sqrt(6)]]", "[[sqrt(7)]]", "[[2 sqrt(2)]]", "3", "[[sqrt(10)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9, note="D/4=k²-7≤0 → k≤√7 → ②. 빠른정답 '무'와 불일치.")

# p67
add(id="c65a5046", qtype="short",
    question="집합 [[A]] = { [[x]] | [[x]]는 [[k < x < 14]]인 10의 양의 약수 }가 공집합이 되도록 하는 모든 자연수 [[k]]의 값의 합을 구하시오. (단, [[k < 14]])",
    choices=None, derived_answer="46", figure=None, difficulty_est=2, confidence=0.9, note="k≥10 → 10+11+12+13=46 = 빠른정답 ✓.")

# p68
add(id="34e01023", qtype="choice",
    question="집합 [[X]] = { [[x]] | [[pow(x,2) - k x + 5 <= 0]], [[x]]는 실수 }가 유한집합이 되도록 하는 실수 [[k]]의 최댓값은?",
    choices=["4", "[[sqrt(17)]]", "[[3 sqrt(2)]]", "[[sqrt(19)]]", "[[2 sqrt(5)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9, note="D=k²-20≤0 → k≤2√5 → ⑤.")

# p71
add(id="69380baf", qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["[[A = set(1, 3)]]일 때, [[card(A) = 2]]", "[[card(empty) = 0]]", "[[card(set(2, 4, 5)) = 3]]",
             "[[A]] = { [[x]] | [[x]]는 6의 약수 }이면 [[card(A) = 3]]", "[[card(set(2, 5, 7)) - card(set(2, 5)) = 1]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9, note="6의 약수 4개 → ④ 거짓.")

# p73 (id 2개)
dup(["1ab47725", "9c1e0398"], qtype="choice",
    question="다음 중 옳은 것을 모두 고르면? (정답 2개)",
    choices=["[[A]] = { [[x]] | [[x]]는 짝수 }이면 [[A]]는 유한집합이다.",
             "[[B = set(0, 1, 2)]]이면 [[in(2, B)]]이다.",
             "[[C]] = { [[x]] | [[x]]는 [[2 < x < 4]]인 짝수 }이면 [[card(C) = 1]]이다.",
             "[[D]] = { [[x]] | [[x]]는 6보다 작은 2의 배수 }이면 [[D = empty]]이다.",
             "[[card(set(0, 1, 4)) - card(set(1, 2)) = 1]]이다."],
    derived_answer="②, ⑤", figure=None, difficulty_est=1, confidence=0.9, note="① 무한, ③ C=∅, ④ D={2,4}≠∅ → ②, ⑤.")

# p75
add(id="97d0b069", qtype="short",
    question=("두 집합 [[A]], [[B]]에 대하여\n[[A]] = { [[x]] | [[x]]는 [[pow(x,2) <= 20]]인 자연수 },\n"
              "[[B]] = { [[x]] | [[x]]는 100보다 작은 15의 양의 배수 }일 때, [[card(B) - card(A)]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.9, note="n(A)=4, n(B)=6 → 2.")

# p76
add(id="639d8b3e", qtype="short",
    question=("실수의 집합 [[A]], [[B]]에 대하여 [[A]]⊗[[B]]를\n[[A]]⊗[[B]] = { [[x]] | [[x = a b]], [[in(a, A)]], [[in(b, B)]] }로 정의한다.\n"
              "[[A = set(-1, 0, 1)]], [[B = set(1, 2)]]일 때,\n집합 [[A]]⊗([[B]]⊗[[A]])의 모든 원소의 합을 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=2, confidence=0.85,
    note="연산 기호 ⊗는 텍스트로 표기. B⊗A={-2,-1,0,1,2}, A⊗(B⊗A)={-2,-1,0,1,2} → 합 0.")

# p77
add(id="a54b0794", qtype="choice",
    question="두 집합 [[A = set(1, 2, 3, 4)]], [[B]] = { [[x]] | [[x]]는 6의 약수 }에 대하여 [[A + B]] = { [[a + b]] | [[in(a, A)]], [[in(b, B)]] }일 때, [[card(A + B)]]는?",
    choices=["7", "8", "9", "10", "11"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9, note="A+B={2,…,10} 9개 → ③.")

# p78
add(id="60d5e47b", qtype="short",
    question="두 집합 [[A = set(-3, 4)]], [[B = set(-1, 0)]]에 대하여 집합 [[X]] = { [[a b]] | [[in(a, A)]], [[in(b, B)]] }의 모든 원소의 합을 구하시오.",
    choices=None, derived_answer="-1", figure=None, difficulty_est=1, confidence=0.9, note="X={3,0,-4} → 합 -1. 빠른정답 6과 불일치.")

# p79
add(id="04d31564", qtype="choice",
    question="집합 [[A]] = { [[x]] | [[x]]는 3과 서로소인 한 자리 자연수 }에 대하여 집합 [[B]] = { [[x]] | [[pow(x,2) - 11x + 18 < 0]], [[in(x, A)]] }일 때, [[card(B)]]는?",
    choices=["2", "3", "4", "5", "6"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="A={1,2,4,5,7,8}, 2<x<9 → B={4,5,7,8} → ③. 빠른정답 0과 불일치.")

# p80
add(id="94026880", qtype="choice",
    question=("두 집합 [[A]] = { [[x]] | [[pow(x,2) + 3x + 3 = 0]], [[x]]는 실수 },\n"
              "[[B]] = { [[x]] | [[pow(x,2) - 2k x + 5k = 0]], [[x]]는 실수 }에 대하여 [[card(A) = card(B)]]가 되도록 하는 정수 [[k]]의 개수는?"),
    choices=["4", "5", "6", "7", "8"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="n(A)=0 → k²-5k<0 → k=1,2,3,4 → ①.")

# p81
add(id="777d265a", qtype="short",
    question=("두 집합 [[A]] = { [[x]] | [[x pow(x - 5, 2) = 0]] },\n[[B]] = { [[x]] | [[x = frac(10, n)]], [[x]], [[n]]은 자연수 }에 대하여 [[card(A) + card(B)]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9, note="A={0,5}, B={1,2,5,10} → 6 = 빠른정답 ✓.")

# p82
add(id="a3866d60", qtype="short",
    question=("서로 다른 세 자연수 [[a]], [[b]], [[c]] ([[a < b < c]])를 원소로 하는 집합 [[A = set(a, b, c)]]에 대하여 "
              "[[B]] = { [[x + y]] | [[in(x, A)]], [[in(y, A)]] }라 하면 집합 [[B]]의 원소 중 최솟값은 8이고 최댓값은 24이다. [[card(B) = 5]]일 때, [[b]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9, note="a=4, c=12, n(B)=5 ⇔ a+c=2b → b=8.")

# p83
add(id="dea7a50f", qtype="short",
    question=("집합 [[A]] = { [[z]] | [[z = pow(i, n + 2) - pow(i, n)]], [[n]]은 자연수 }에 대하여 "
              "집합 [[B]] = { [[pow(sub(z,1), 2) - pow(sub(z,2), 2)]] | [[in(sub(z,1), A)]], [[in(sub(z,2), A)]] }일 때, 집합 [[B]]의 원소의 개수를 구하시오. (단, [[i = sqrt(-1)]])"),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9, note="A={-2iⁿ}={±2, ±2i}, 제곱은 ±4 → B={-8,0,8} → 3.")

# p84
add(id="55eaaa6e", qtype="choice",
    question=("두 집합 [[A = set(-1, 3, a)]],\n[[B]] = { [[x]] | [[x]]는 6의 양의 약수 }에 대하여 집합 [[C]]를\n[[C]] = { [[x y]] | [[in(x, A)]], [[in(y, B)]] }라 할 때,\n"
              "[[C = set(-6, -3, -2, -1, 1, 2, 3, 6, 9, 18)]]이다.\n이때 상수 [[a]]의 값은?"),
    choices=["[[-2]]", "[[-1]]", "0", "1", "2"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="1, 2가 필요 → a=1 → ④. 빠른정답 6과 불일치.")

# p85
add(id="d9d429db", qtype="short",
    question="집합 [[A = set(0, 1, 2, 3, 4)]]에 대하여 집합 [[X]] = { [[comb(a, b)]] | [[in(a, A)]], [[in(b, A)]], [[a != 0]], [[a >= b]] }일 때, [[card(X)]]를 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9, note="X={1,2,3,4,6} → 5. 빠른정답 8과 불일치.")

# p87
add(id="32eafa50", qtype="short",
    question="자연수 전체의 집합의 부분집합 [[A]]에 대하여 ‘[[in(a, A)]]이면 [[in(frac(81, a), A)]]이다.’를 만족하는 집합 [[A]]의 개수를 구하시오. (단, [[A != empty]])",
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.9, note="{1,81},{3,27},{9} 묶음의 합집합 → 2³-1=7 = 빠른정답 ✓.")

# p89
add(id="8b1e5134", qtype="choice",
    question="집합 [[S]]의 원소가 자연수이고 ‘[[in(a, S)]], [[in(b, S)]]이면 [[in(a b, S)]]’가 성립한다. [[in(3, S)]], [[in(4, S)]]일 때, 다음 중 반드시 집합 [[S]]의 원소라고 할 수 없는 것은?",
    choices=["[[in(12, S)]]", "[[in(16, S)]]", "[[in(24, S)]]", "[[in(27, S)]]", "[[in(36, S)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9, note="24=2·3·4에 2가 필요 → ③. 빠른정답 15와 불일치.")

# p90 (id 2개)
dup(["b9936bec", "8179328b"], qtype="short",
    question=("원소의 개수가 3인 집합 [[S]]가 다음 조건을 모두 만족할 때, [[frac(1,3)]]과 1을 제외한 집합 [[S]]의 나머지 원소를 구하시오.\n"
              "(가) [[in(frac(1,3), S)]], [[in(1, S)]], [[notin(0, S)]]\n(나) [[in(p, S)]], [[in(q, S)]]이면 [[in(p q, S)]] (단, [[p != q]])"),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9, note="x/3∈S → x=3 → S={1/3,1,3}. 빠른정답 7과 불일치.")

# p91
add(id="0c3c7e68", qtype="short",
    question="두 집합 [[A = set(2, 3, a)]], [[B = set(3, 4, 5)]]에 대하여 집합 [[X]] = { [[x + y]] | [[in(x, A)]], [[in(y, B)]] }라 할 때, [[card(X) = 6]]이 되도록 하는 자연수 [[a]]의 최댓값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9, note="기본 {5,6,7,8}에 새 원소 2개 → a=5 = 빠른정답 ✓.")

# p92
add(id="fe35f814", qtype="short",
    question="두 집합 [[A = set(1, 3, 5, a)]], [[B = set(2, 4, 6)]]에 대하여 집합 [[X]] = { [[x + y]] | [[in(x, A)]], [[in(y, B)]] }라 할 때, [[card(X) = 7]]이 되도록 하는 자연수 [[a]]의 최댓값을 구하시오.",
    choices=None, derived_answer="9", figure=None, difficulty_est=2, confidence=0.9, note="기본 {3,5,7,9,11}에 새 원소 2개 → a=9.")

# p93
add(id="04c18af3", qtype="short",
    question=("원소의 개수가 3인 집합 [[S]]가 다음 조건을 모두 만족할 때, [[frac(1,2)]]과 1을 제외한 집합 [[S]]의 나머지 원소를 구하시오.\n"
              "(가) [[in(frac(1,2), S)]], [[in(1, S)]], [[notin(0, S)]]\n(나) [[in(p, S)]], [[in(q, S)]]이면 [[in(p q, S)]] (단, [[p != q]])"),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9, note="x/2∈S → x=2. 빠른정답 3과 불일치.")

# p95
add(id="37699ec1", qtype="choice",
    question=("집합 [[U]] = { [[x]] | [[x]]는 200 이하의 자연수 }의 부분집합 [[A]]가 다음 조건을 모두 만족시킬 때, 집합 [[A]]의 원소의 개수의 최솟값은?\n"
              "(가) [[subset(set(3, 4), A)]]\n(나) [[in(x, A)]], [[in(3x, U)]]이면 [[in(3x, A)]]이다."),
    choices=["8", "9", "10", "11", "12"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="3,9,27,81 / 4,12,36,108 → 8 → ①. 빠른정답 9와 불일치.")

# p96
add(id="dcedb5d3", qtype="short",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 9 이하의 자연수 }의 부분집합 [[A]]는 다음 조건을 만족시킨다.\n"
              "[[m]]이 집합 [[A]]의 원소이면 [[pow(m,4)]]의 일의 자릿수와 [[pow(n,4)]]의 일의 자릿수가 같아지는 [[m]]이 아닌 모든 자연수 [[n]]이 집합 [[A]]에 존재한다.\n"
              "예를 들면, 2가 집합 [[A]]의 원소이면 [[pow(2,4)]]의 일의 자릿수와 [[pow(8,4)]]의 일의 자릿수가 같으므로 8도 집합 [[A]]의 원소이다.\n"
              "공집합이 아닌 집합 [[A]]의 개수를 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2019년 10월 고3 문과 25번 변형]. 묶음 {1,3,7,9},{2,4,6,8},{5} → 2³-1=7. 빠른정답 2와 불일치.")

# p98
add(id="fee012bb", qtype="short",
    question=("집합 [[A]] = { [[x]] | [[x]]는 자연수 }에 대하여 다음 조건을 모두 만족시키면서 [[k]]개의 원소를 갖는 집합 [[B]]의 개수를 [[sub(a,k)]]라 하자. 이때 [[sub(a,3) + sub(a,4)]]의 값을 구하시오.\n"
              "(가) [[subset(B, A)]], [[card(B) != 0]]\n(나) [[in(x, B)]]이면 [[in(10 - x, B)]]이다."),
    choices=None, derived_answer="10", figure=None, difficulty_est=3, confidence=0.85,
    note="묶음 {1,9},{2,8},{3,7},{4,6},{5}: a₃=4, a₄=C(4,2)=6 → 10.")

# p99
add(id="e9a20529", qtype="short",
    question="두 집합 [[A = set(0, 1, 2, 3)]], [[B = set(1, 2, 5)]]에 대하여 집합 [[C]]가 [[C]] = { [[x y]] | [[in(x, A)]], [[in(y, B)]] }일 때, [[card(A) + card(B) - card(C)]]의 값을 구하시오.",
    choices=None, derived_answer="-2", figure=None, difficulty_est=1, confidence=0.9, note="C={0,1,2,3,4,5,6,10,15} 9개 → 4+3-9=-2. 빠른정답 7과 불일치.")

# ================= 무리함수의 그래프 =================
# p20
add(id="997ccf3f", qtype="choice",
    question="등식 [[a (1 + 3 sqrt(2)) + b (2 - sqrt(2)) = -4 + 9 sqrt(2)]]를 만족하는 유리수 [[a]], [[b]]의 값은?",
    choices=["[[a = 1]], [[b = -3]]", "[[a = 1]], [[b = -2]]", "[[a = 2]], [[b = -3]]", "[[a = -2]], [[b = -1]]", "[[a = -2]], [[b = 3]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="a+2b=-4, 3a-b=9 → a=2, b=-3 → ③. 빠른정답 9와 불일치. (내용은 무리수 상등 조건)")

# p29
add(id="87001f24", qtype="choice",
    question=("별에서 단위시간동안 방출되는 복사에너지의 양을 별의 광도라 한다. 별의 표면 온도를 [[T]], 별의 반지름의 길이를 [[R]], 별의 광도를 [[L]]이라 하면 다음과 같은 관계식이 성립한다고 한다.\n"
              "[[pow(T,2) = frac(1, R)]] × √( [[L]] / (4πσ) )\n(단, σ는 슈테판-볼츠만 상수이다.)\n"
              "두 별 A, B에 대하여 별 A의 표면 온도는 별 B의 표면 온도의 [[frac(1,2)]]배이고, 별 A의 반지름의 길이는 별 B의 반지름의 길이의 36배 일 때, "
              "별 A의 광도는 별 B의 광도의 [[k]]배이다. [[k]]의 값은?"),
    choices=["49", "64", "81", "100", "121"], derived_answer="③", figure=None, difficulty_est=3, confidence=0.75,
    needs_review="문법 범위 밖: 그리스 문자 σ(시그마) 미지원 → 관계식 T²=(1/R)√(L/(4πσ))를 텍스트 혼합으로 표기",
    note="출처 [2015년 11월 고1 16번/4점]. L=4πσ(T²R)² ∝ T⁴R² → (1/2)⁴·36²=81 → ③. 빠른정답 1과 불일치.")

# p38
add(id="4bace5cc", qtype="short",
    question="[[x > y > 0]]인 [[x]], [[y]]에 대하여 [[x + y = 5]], [[x y = 4]]일 때, [[frac(sqrt(x) - sqrt(y), sqrt(x) + sqrt(y)) = k]]라 하자. 상수 [[k]] 에 대하여 [[3k + 1]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9, note="x=4, y=1 → k=1/3 → 3k+1=2. 빠른정답 19와 불일치.")

# p52
add(id="7102f165", qtype="short",
    question=("실수 전체의 집합에서 정의된 함수 [[f]]가\n[[f(x) = frac(x + 5, x - 2)]] ([[x > 3]]), [[f(x) = sqrt(3 - x) + k]] ([[x <= 3]])\n일 때, 함수 [[f]]는 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[f]]의 치역은 { [[y]] | [[y > 1]] }이다.\n"
              "(나) 임의의 두 실수 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n"
              "[[f(p) f(-1) = 15]]일 때, 상수 [[p]]의 값을 구하시오.\n(단, [[k]]는 상수)"),
    choices=None, derived_answer="16", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="조각적(경우 나눔) 정의 함수 f(x) — 두 식을 콤마로 나열",
    note="x>3에서 치역 (1,8), 일대일·치역 조건으로 k=8, f(-1)=10 → f(p)=3/2 → p=16 = 빠른정답 ✓.")

# p57
add(id="273bbd0f", qtype="choice",
    question=("함수 [[f(x) = -pow(x - a, 2) + b]] ([[x <= a]]), [[f(x) = -sqrt(x - a) + b]] ([[x > a]])와 서로 다른 세 실수 [[alpha]], [[beta]], [[gamma]]가 다음 조건을 만족시킨다.\n"
              "(가) 방정식 [[(f(x) - alpha)(f(x) - beta) = 0]]을 만족시키는 실수 [[x]]의 값은 [[alpha]], [[beta]], [[gamma]]뿐이다.\n"
              "(나) [[f(alpha) = alpha]], [[f(beta) = beta]]\n"
              "[[alpha + beta + gamma = 15]]일 때, [[f(alpha + beta)]]의 값은? (단, [[a]], [[b]]는 상수이다.)"),
    choices=["1", "2", "3", "4", "5"], derived_answer="③", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="조각적(경우 나눔) 정의 함수 f(x) — 두 식을 콤마로 나열(원문의 중괄호 {f(x)-α}{f(x)-β}는 소괄호로)",
    note="출처 [2023년 3월 고2 20번/4점]. 최댓값 b=a가 고정점 α=a, β=a-1, γ=a+1 → 3a=15, a=5 → f(9)=-2+5=3 → ③ = 빠른정답 ✓.")

# p82
add(id="78965e1f", qtype="choice",
    question="함수 [[f(x) = -sqrt(x) + 1]] ([[x >= 1]]), [[f(x) = sqrt(2 - x)]] ([[x < 1]])에 대하여 ([[comp(inv(f), inv(f))]])([[a]]) = 9를 만족하는 상수 [[a]]의 값은?",
    choices=["[[-1]]", "0", "1", "2", "3"], derived_answer="④", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="조각적 정의 함수 + 합성함수 적용 표기 (f⁻¹∘f⁻¹)(a)",
    note="f⁻¹(a)=f(9)=-2 → a=f(-2)=2 → ④ = 빠른정답 ✓.")

# p83
add(id="9935fe9a", qtype="short",
    question="함수 [[f]]를 [[f(x) = 1 - sqrt(x)]] ([[x >= 0]]), [[f(x) = sqrt(1 - x)]] ([[x < 0]])으로 정의할 때, ([[comp(inv(f), inv(f))]])([[a]]) = 16을 만족시키는 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="조각적 정의 함수 + 합성함수 적용 표기 (f⁻¹∘f⁻¹)(a)",
    note="f⁻¹(a)=f(16)=-3 → a=f(-3)=2 = 빠른정답 ✓.")

# p84
add(id="e62608af", qtype="choice",
    question=("유리함수 [[y = frac(x - 5, 2n x - 240 n)]]의 그래프의 두 점근선 [[x = k]], [[y = f(n)]]과 이차함수 [[y = frac(1,2) pow(x,2) - frac(1,2)]] ([[x >= 0]])의 역함수 [[y = g(x)]]에 대하여 "
              "[[h(x)]] = ([[comp(g, f)]])([[x]])라 할 때, [[h(1) × h(2) × h(3)]] × ⋯ × [[h(k)]]의 값은?\n(단, [[n]]은 자연수이다.)"),
    choices=["10", "11", "12", "13", "14"], derived_answer="②", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="합성함수 적용 표기 (g∘f)(x)",
    note="k=120, f(n)=1/(2n), g(x)=√(2x+1) → h(x)=√((x+1)/x) → 곱 √121=11 → ②. 빠른정답 6과 불일치.")

# ================= 두 직선의 평행 조건과 수직 조건 =================
# p8
add(id="604d957f", qtype="short",
    question="직선 [[y = (m - 5) x - n - 7]]가 점 [[point(1, -4)]]를 지나고 [[x]]축의 양의 방향과 이루는 각의 크기가 [[deg(45)]]일 때, 상수 [[m]], [[n]]에 대하여 [[m + n]]의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9, note="기울기 1 → m=6, -4=1-n-7 → n=-2 → 4.")

# p14
add(id="f17248d7", qtype="choice",
    question="두 점 [[A point(-1, 10)]], [[B point(2, 4)]]와 [[x]]축 위의 점 P에 대하여 [[abs(seg(AP) - seg(BP))]]의 값이 최대일 때, 선분 BP의 길이는?",
    choices=["4", "[[sqrt(17)]]", "[[3 sqrt(2)]]", "[[sqrt(19)]]", "[[2 sqrt(5)]]"], derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="직선 AB(y=-2x+8)와 x축 교점 P(4,0) → BP=√20=2√5 → ⑤. 빠른정답 3과 불일치.")

# p32
add(id="ab4e249c", qtype="short",
    question="다음 그림에서 직선 [[y = a x + b]]가 두 직사각형의 넓이를 동시에 이등분할 때, 상수 [[a]], [[b]]의 합 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="frac(7,8)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 제1사분면에 x∈[1,3], y∈[1,3]인 정사각형(음영), 제3사분면에 x∈[-3,-1], y∈[-3,-2]인 직사각형(음영); 축 눈금 -3,-1,1,3 / -3,-2,1,3"}}],
    difficulty_est=2, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 두 직사각형(문항 정보가 그림에 있음)",
    note="두 중심 (2,2), (-2,-5/2)를 지남 → a=9/8, b=-1/4 → 7/8 = 빠른정답 ✓.")

# p38
add(id="0b7e360a", qtype="choice",
    question="[[a b < 0]], [[b c > 0]]일 때, 직선 [[a x + b y + c = 0]]이 지나지 않는 사분면은?",
    choices=["제1사분면", "제2사분면", "제3사분면", "제4사분면", "제1, 2사분면"], derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 -a/b>0, y절편 -c/b<0 → 제2사분면 안 지남 → ②.")

# p49
add(id="8778e84b", qtype="choice",
    question=("좌표평면 위에 네 점 [[A point(-1, 4)]], [[B point(-3, 0)]], [[C point(0, -2)]], [[D point(1, 3)]]이 있다. 다음은 네 점 A, B, C, D가 각각 네 변 PQ, QR, RS, SP 위에 있도록 하는 정사각형 PQRS의 한 변의 길이를 구하는 과정이다.\n"
              "점 A를 지나고 두 점 B와 D를 지나는 직선에 수직인 직선 [[sub(l,1)]]의 방정식은 [[y]] = (가) 이다.\n"
              "점 A를 중심으로 하고 반지름의 길이가 [[seg(BD)]]인 원을 [[C]]라 하자. 원 [[C]]와 직선 [[sub(l,1)]]이 만나는 두 점 중 점 C와의 거리가 더 작은 점을 E라 하고, 두 점 C와 E를 지나는 직선을 [[sub(l,2)]]라 하면 직선 [[sub(l,2)]]의 방정식은 [[y]] = (나) 이다.\n"
              "두 점 B와 D에서 직선 [[sub(l,2)]]에 내린 수선의 발을 각각 R, S라 하자. 점 A를 지나고 직선 [[sub(l,2)]]와 평행한 직선을 [[sub(l,3)]]이라 하고, 두 점 B와 D에서 직선 [[sub(l,3)]]에 내린 수선의 발을 각각 Q, P라 하자.\n"
              "사각형 PQRS는 네 점 A, B, C, D가 각각 네 변 PQ, QR, RS, SP 위에 있고 한 변의 길이가 [[seg(PQ) = seg(QR)]] = (다) 인 정사각형이다.\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(x)]], [[g(x)]]라 하고, (다)에 알맞은 수를 [[alpha]]라 할 때, [[frac(3,4) f(alpha) - g(alpha)]]의 값은?"),
    choices=["[[4 - 3 sqrt(2)]]", "[[4 - 4 sqrt(2)]]", "[[4 - 5 sqrt(2)]]", "[[4 - 6 sqrt(2)]]", "[[4 - 7 sqrt(2)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 그림 2개: (위) 점 A,B,C,D,E와 직선 l₁(A를 지나 BD에 수직), A 중심 원호, 직선 l₂(C,E 지남, E는 x축 위); (아래) 직선 l₁,l₂,l₃와 수선의 발 P,Q,R,S로 만든 정사각형 PQRS(직각 표시)"}}],
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 직선·원·정사각형 복합 좌표평면 도형 2개 + 빈칸 (가)(나)(다)",
    note="출처 [2022년 9월 고1 19번/4점]. (가) -4/3x+8/3, E(2,0), (나) x-2, (다) 7√2/2 → 4-2α=4-7√2 → ⑤.")

# p66
add(id="569c08af", qtype="choice",
    question=("그림과 같이 좌표평면에서 두 점 [[A point(0, 6)]], [[B point(18, 0)]]과 제1사분면 위의 점 [[C point(a, b)]]가 [[seg(AC) = seg(BC)]]를 만족시킨다. "
              "두 선분 AC, BC를 1 : 3으로 내분하는 점을 각각 P, Q라 할 때, 삼각형 CPQ의 무게중심을 G라 하자. 선분 CG의 길이가 [[sqrt(10)]]일 때, [[a + b]]의 값은?"),
    choices=["17", "18", "19", "20", "21"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y축 위 A, x축 위 B, 위쪽 점 C, 선분 AC 위 P·BC 위 Q, 삼각형 CPQ 내부의 점 G와 선분 CG"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 삼각형·내분점·무게중심 그림",
    note="출처 [2017년 3월 고2 이과 19번/4점]. G=((a+9)/2,(b+3)/2), 3a-b=24, (a-9)²+(b-3)²=40 → a=11, b=9 → 20 → ④.")

# p69
add(id="1be584e8", qtype="short",
    question=("다음 그림과 같이 원점 O와 세 점 [[A point(5, 2)]], [[B point(a, b)]], [[C point(c, d)]]에 대하여 삼각형 OAB는 [[angle(AOB) = deg(90)]]인 직각이등변삼각형이고, "
              "삼각형 OAC는 [[angle(OAC) = deg(90)]]인 직각이등변삼각형이다. 점 B가 제2사분면 위에 있고, 점 C가 제1사분면 위에 있을 때, [[a b + c d]]의 값을 구하시오."),
    choices=None, derived_answer="11",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O, 제1사분면 점 A, 제2사분면 점 B, 위쪽 점 C; OA=OB(직각 표시 O), OA=AC(직각 표시 A), 같은 길이 표시"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 두 직각이등변삼각형 그림",
    note="B=(-2,5), C=(3,7) → -10+21=11.")

# p78
add(id="b7cb29e6", qtype="choice",
    question=("그림과 같이 제1사분면에 있는 곡선 [[y = frac(2, x)]] 위의 서로 다른 두 점 [[A point(a, frac(2, a))]], [[B point(b, frac(2, b))]]에 대하여 직선 AB가 [[x]]축과 만나는 점을 C, 선분 AB의 중점을 D라 하자.\n"
              "<보기>에서 옳은 것만을 있는 대로 고른 것은? (단, [[a < b]]이고, O는 원점이다.)\n<보기>\n"
              "ㄱ. 점 C의 [[x]]좌표는 [[a + b]]이다.\n"
              "ㄴ. 두 직선 AB와 OD의 기울기의 합은 0이다.\n"
              "ㄷ. [[seg(AB) = 2 seg(OA)]]일 때, [[angle(AOC) = frac(3,2) angle(AOD)]]이다."),
    choices=CH_3B, derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 제1사분면 곡선 y=2/x 위의 점 A, B, 직선 AB와 x축의 교점 C, AB의 중점 D, 선분 OA·OD·OC"}}],
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 곡선 y=2/x와 직선·점이 있는 좌표평면 그림",
    note="출처 [2014년 3월 고2 이과 18번/4점]. ㄱ x=a+b ✓, ㄴ 기울기 ∓2/(ab) ✓, ㄷ 수치 검산 ∠AOC/∠AOD=1.5 ✓ → ⑤.")

# p79
add(id="ed24078c", qtype="choice",
    question=("좌표평면 위의 두 직선 [[y = m x]], [[y = n x]] ([[m > 0]], [[n > 0]])가 다음 두 조건을 만족한다.\n"
              "(가) 직선 [[y = m x]]가 [[x]]축의 양의 방향과 이루는 각의 크기는 직선 [[y = n x]]가 [[x]]축의 양의 방향과 이루는 각의 크기의 2배이다.\n"
              "(나) 직선 [[y = m x]]의 기울기는 직선 [[y = n x]]의 기울기의 4배이다.\n"
              "두 상수 [[m]], [[n]]의 곱 [[m n]]의 값은?"),
    choices=["1", "2", "[[2 sqrt(2)]]", "4", "[[4 sqrt(2)]]"], derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2006년 3월 고2 18번]. tan2θ=4tanθ → tan²θ=1/2 → n=1/√2, m=2√2 → mn=2 → ②.")

# p92
add(id="129c5d91", qtype="choice",
    question=("그림과 같이 한 변의 길이가 12인 정사각형 OABC 모양의 종이를 점 O가 원점에, 두 점 A, C가 각각 [[x]]축, [[y]]축 위에 있도록 좌표평면 위에 놓았다. "
              "두 점 D, E는 각각 두 선분 OC, AB를 2 : 1로 내분하는 점이고, 선분 OA 위의 점 F에 대하여 [[seg(OF) = 5]]이다.\n"
              "선분 OC 위의 점 P와 선분 AB 위의 점 Q에 대하여 선분 PQ를 접는 선으로 하여 종이를 접었더니 점 O는 선분 BC 위의 점 O′으로, 점 F는 선분 DE 위의 점 F′으로 옮겨졌다. "
              "이때 좌표평면에서 직선 PQ의 방정식은 [[y = m x + n]]이다. [[m + n]]의 값은?\n(단, [[m]], [[n]]은 상수이고, 종이의 두께는 고려하지 않는다.)"),
    choices=["6", "[[frac(25,4)]]", "[[frac(13,2)]]", "[[frac(27,4)]]", "7"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 정사각형 OABC(O 원점, A x축, C y축), D(OC 위)·E(AB 위)와 점선 DE, F(OA 위, OF=5), 접는 선 PQ(P는 OC 위, Q는 AB 위), 접힌 뒤 O′(BC 위)·F′(DE 위), 접는 방향 화살표"}}],
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 종이접기 좌표평면 그림 / 프라임 점 라벨 O′, F′",
    note="출처 [2016년 3월 고2 문과 21번/4점]. O′(6,12), F′(9,8) → 접는 선 x+2y=15 → m=-1/2, n=15/2 → 7 → ⑤.")

# ================= 대칭이동 =================
# p5
add(id="cf06cf26", qtype="choice",
    question=("직선 [[y = frac(1,2) x]] 위의 점 [[P point(a, b)]]를 [[x]]축, [[y]]축에 대하여 각각 대칭이동한 점을 [[sub(P,1)]], [[sub(P,2)]]라 하자. "
              "△P[[sub(P,1)]][[sub(P,2)]]의 넓이가 4일 때, 두 양수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?"),
    choices=["1", "2", "3", "4", "5"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="첨자 점 라벨 삼각형 △PP₁P₂ (tri()에 첨자 점 불가) → 텍스트 혼합",
    note="넓이 2ab=4, b=a/2 → a=2, b=1 → 3 → ③. 빠른정답 140과 불일치.")

# p33
add(id="b499c4b1", qtype="short",
    question=("좌표평면 위의 한 점 [[sub(P,1)]][[point(-3, 5)]]를 원점에 대하여 대칭이동한 점을 [[sub(P,2)]]라 하고, 점 [[sub(P,2)]]를 직선 [[y = x]]에 대하여 대칭이동한 점을 [[sub(P,3)]]라 하자. "
              "다시 점 [[sub(P,3)]]를 원점에 대하여 대칭이동한 점을 [[sub(P,4)]]라 하고, 점 [[sub(P,4)]]를 직선 [[y = x]]에 대하여 대칭이동한 점을 [[sub(P,5)]]라 하자. "
              "이와 같은 방법으로 원점과 직선 [[y = x]]에 대하여 대칭이동한 점을 차례대로 [[sub(P,6)]], [[sub(P,7)]], ⋯이라 할 때, 점 [[sub(P,3003)]]의 좌표를 [[point(a, b)]]라 하자. 이때 [[b - a]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="주기 4: P₁(-3,5), P₂(3,-5), P₃(-5,3), P₄(5,-3); 3003≡3 → P₃(-5,3) → b-a=8. 빠른정답 -1과 불일치.")

# p79
add(id="80e6c9b3", qtype="choice",
    question="두 점 [[A point(1, 1)]], [[B point(4, 3)]]에 대하여 점 P가 [[x]]축 위의 점일때, [[seg(AP) + seg(BP)]]의 최솟값은?",
    choices=["5", "[[2 sqrt(2)]]", "[[4 sqrt(2)]]", "[[8 sqrt(2)]]", "8"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="A′(1,-1)과 B 거리 5 → ①. 빠른정답 4와 불일치.")

# p80
add(id="59760879", qtype="choice",
    question="정점 [[A point(3, 1)]]과 직선 [[y = x]] 위를 움직이는 점 P, [[x]]축 위를 움직이는 점 Q에 대하여 [[seg(AP) + seg(PQ) + seg(QA)]]의 최솟값을 구하면?",
    choices=["[[2 sqrt(3)]]", "4", "[[2 sqrt(5)]]", "[[3 sqrt(5)]]", "[[4 sqrt(3)]]"], derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="A를 y=x, x축에 대칭한 (1,3), (3,-1) 거리 √20=2√5 → ③. 빠른정답 5와 불일치.")

# p81
add(id="b15fab5e", qtype="choice",
    question=("반지름의 길이가 20 m인 원형의 수영장이 있다. 점 O는 수영장의 중심이고, 두 점 P, Q는 원 위의 점이며 [[angle(POQ) = deg(60)]]이다. "
              "갑과 을이 각각 P, Q에서 동시에 출발하여 중심 O를 향해 가고 있다. 호 PQ 위에 한 점 C를 고정하고 선분 OP와 선분 OQ 위의 임의의 두 지점 A, B에 갑과 을이 각각 도달하였을 때, "
              "세 지점 A, B, C를 서로 연결한 거리의 합 [[seg(AB) + seg(BC) + seg(CA)]]의 최솟값은?"),
    choices=["[[15 sqrt(2)]] m", "[[15 sqrt(3)]] m", "[[20 sqrt(2)]] m", "[[20 sqrt(3)]] m", "[[25 sqrt(2)]] m"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O) 위의 점 P, Q, 호 PQ 위의 점 C; OP 위의 A, OQ 위의 B(점선 화살표로 O를 향함), 삼각형 ABC, ∠POQ=60° 표시"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 원·삼각형·화살표 복합 도형",
    note="출처 [2005년 11월 고1 15번]. C를 OP, OQ에 대칭한 두 점 사이 거리 = 2·20·sin60° = 20√3 → ④ = 빠른정답 ✓.")

# p82
add(id="47ff2962", qtype="choice",
    question=("그림과 같이 좌표평면 위에 두 원\n[[sub(C,1)]]: [[pow(x - 8, 2) + pow(y - 2, 2) = 4]],\n[[sub(C,2)]]: [[pow(x - 3, 2) + pow(y + 4, 2) = 4]]와 직선 [[y = x]]가 있다.\n"
              "점 A는 원 [[sub(C,1)]] 위에 있고, 점 B는 원 [[sub(C,2)]] 위에 있다.\n점 P는 [[x]]축 위에 있고, 점 Q는 직선 [[y = x]] 위에 있을 때,\n"
              "[[seg(AP) + seg(PQ) + seg(QB)]]의 최솟값은?\n(단, 세 점 A, P, Q는 서로 다른 점이다.)"),
    choices=["7", "8", "9", "10", "11"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원 C₁(제1사분면, x축에 접함) 위의 점 A, 원 C₂(제4사분면) 위의 점 B, x축 위의 점 P, 직선 y=x 위(제3사분면 쪽)의 점 Q, 꺾은선 A-P-Q-B"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 두 원·직선·꺾은선 복합 좌표평면 도형",
    note="출처 [2023년 9월 고1 16번/4점]. C₁ 중심을 x축 대칭 (8,-2), C₂ 중심을 y=x 대칭 (-4,3) → 거리 13-2-2=9 → ③. 빠른정답 1과 불일치.")

# p83
add(id="e65611ea", qtype="short",
    question=("반지름의 길이가 20 m인 원형의 수영장이 있다. 점 O는 수영장의 중심이고, 두 점 P, Q는 원 위의 점이며 [[angle(POQ) = deg(60)]]이다. "
              "갑과 을이 각각 P, Q에서 동시에 출발하여 중심 O를 향해가고 있다.\n호 PQ 위의 한 점 C에 대하여 선분 OP와 선분 OQ 위의 임의의 두 지점 A, B에 갑과 을이 각각 도달하였을 때, "
              "[[seg(AB) + seg(BC) + seg(CA)]]의 최솟값은 [[a sqrt(3)]] m이다.\n[[a]]의 값을 구하시오. (단, [[a]]는 자연수이다.)"),
    choices=None, derived_answer="20",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O) 위의 점 P, Q, 호 PQ 위의 점 C; OP 위의 A, OQ 위의 B, 삼각형 ABC, ∠POQ=60° 표시"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 원·삼각형 복합 도형",
    note="최솟값 20√3 → a=20. 빠른정답 3과 불일치.")
