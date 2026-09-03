# -*- coding: utf-8 -*-
# esc_sonnet_h2-1_4of4 — 이미지 기준 전사 (19 항목 / 19쪽, 로그의 뜻과 성질) — 2차 작업자가 19장 전부 이미지 재대조 완료
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# p5 — 로그의 정의
add(id="ff1f5641", qtype="choice",
    question=("[[4 < a < b < 200]]인 두 자연수 [[a]], [[b]]에 대하여\n"
              "집합 [[A]] = { [[k]] | [[k = log(a, b)]], [[k]]는 유리수 }라 하자.\n"
              "[[card(A)]]의 값은?"),
    choices=["[[11]]", "[[13]]", "[[15]]", "[[17]]", "[[19]]"],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2019년 11월 고2 문과 21번/4점]. a=m^q, b=m^p 꼴 전수 확인(파이썬) → 유리수 k 11개 → ①. 집합 조건은 텍스트 혼합.")

# p13 — 로그의 밑과 진수의 조건
add(id="e97ec19d", qtype="short",
    question="[[log(abs(a), -pow(a,2) + 16)]]이 정의되도록 하는 정수 [[a]]의 개수를 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2024년 10월 고2 25번 변형]. |a|>0, |a|≠1, a²<16 → a=±2, ±3 → 4개 = 빠른정답 ✓.")

# p24 — 로그의 밑의 변환
add(id="5dffb491", qtype="choice",
    question=("1보다 큰 세 실수 [[a]], [[b]], [[c]]가 [[log(a, b) = frac(log(b, c), 2) = frac(log(c, a), 4)]]를\n"
              "만족시킬 때, [[log(a, b) + log(b, c) + log(c, a)]]의 값은?"),
    choices=["[[frac(7,2)]]", "[[4]]", "[[frac(9,2)]]", "[[5]]", "[[frac(11,2)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 9월 고3 이과 11번/3점]. 공통값 t: 곱 8t³=1 → t=1/2, 합 7t=7/2 → ①.")

# p29 — 로그의 밑의 변환
add(id="53c86695", qtype="choice",
    question=("두 양수 [[a]], [[b]]에 대하여 좌표평면 위의\n"
              "두 점 [[point(5, log(5, a))]], [[point(9, log(5, b))]]를 지나는 직선이 원점을\n"
              "지날 때, [[log(a, b)]]의 값은? (단, [[a != 1]])"),
    choices=["[[frac(3,5)]]", "[[frac(6,5)]]", "[[frac(9,5)]]", "[[frac(5,3)]]", "[[frac(5,9)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="원점 지나므로 log₅b/9 = log₅a/5 → log_a b = 9/5 → ③. 빠른정답 5와 불일치.")

# p36 — 로그의 여러 가지 성질
add(id="66ddf408", qtype="choice",
    question=("수직선 위의 두 점 [[P(log(3, 2))]], [[Q(log(3, 36))]]에 대하여\n"
              "선분 [[seg(PQ)]]를 [[ratio(m, 1 - m)]]으로 내분하는 점의 좌표가 2일\n"
              "때, [[pow(18, m)]]의 값은? (단, [[0 < m < 1]])"),
    choices=["[[frac(7,2)]]", "[[4]]", "[[frac(9,2)]]", "[[5]]", "[[frac(11,2)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2023년 11월 고3 9번 변형]. (1-m)log₃2 + m log₃36 = 2 → 2·18^m = 9 → 18^m = 9/2 → ③. 빠른정답 9와 불일치.")

# p37 — 로그에 대한 증명
add(id="f6a80e33", qtype="choice",
    question=("다음은 [[a]], [[b]]가 1이 아닌 양의 실수일 때,\n"
              "[[log(a, b) = log(b, a)]]이면 [[frac(pow(a,2) + 1, pow(b,2) + 1) = frac(a, b)]]이다.' ⋯ (∗)가\n"
              "성립함을 증명한 것이다.\n\n"
              "<증명>\n"
              "[[log(b, a)]] = 1/(가) 이고 가정에서\n"
              "[[log(a, b) = log(b, a)]]이므로\n"
              "[[log(a, b) = 1]] 또는 [[log(a, b) = -1]]이다.\n"
              "(ⅰ) [[log(a, b) = 1]]일 때, [[frac(pow(a,2) + 1, pow(b,2) + 1)]] = (나) 이고\n"
              "[[frac(a, b)]] = (나) 이다.\n"
              "(ⅱ) [[log(a, b) = -1]]일 때, [[frac(pow(a,2) + 1, pow(b,2) + 1)]] = (다) 이고\n"
              "[[frac(a, b)]] = (다) 이다.\n"
              "따라서 (ⅰ), (ⅱ)에 의하여 [[frac(pow(a,2) + 1, pow(b,2) + 1) = frac(a, b)]]이므로\n"
              "(∗)가 성립한다.\n\n"
              "위 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[log(a, b)]], (나) [[-1]], (다) [[pow(b,2)]]",
             "(가) [[log(b, frac(1, a))]], (나) [[-1]], (다) [[a b]]",
             "(가) [[log(a, b)]], (나) [[1]], (다) [[pow(a,2)]]",
             "(가) [[log(b, frac(1, a))]], (나) [[-1]], (다) [[pow(a,2)]]",
             "(가) [[log(a, b)]], (나) [[1]], (다) [[pow(b,2)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="출처 [2010년 4월 고3 이과 7번]. (가)=log_a b, (나)=1, (다)=a² → ③. 빈칸 상자·분수 '1/(가)'는 텍스트, 표 형태 선지는 '(가) …, (나) …, (다) …' 문자열로.")

# p38 — 로그에 대한 증명 (log2 무리수)
add(id="43e0acdc", qtype="choice",
    question=("다음은 [[log(2)]]가 무리수임을 증명한 것이다.\n\n"
              "<증명>\n"
              "[[log(2)]]가 유리수라고 가정하자.\n"
              "[[log(2) = frac(n, m)]] ([[m]], [[n]]은 서로소인 자연수) ⋯ ㉠\n"
              "로 놓으면\n"
              "[[0 < log(2) < 1]]이므로 (가) 이다.\n"
              "㉠에서\n"
              "[[pow(10, frac(n, m)) = 2]]이므로\n"
              "2^(나) = [[pow(5, n)]]\n"
              "이때, (가) 이므로\n"
              "2^(나)은 (다) 이고 [[pow(5, n)]]은 □가 되어\n"
              "모순이다.\n"
              "따라서 [[log(2)]]는 무리수이다.\n\n"
              "위 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[m > n]], (나) [[m - n]], (다) 짝수",
             "(가) [[m > n]], (나) [[n - m]], (다) 홀수",
             "(가) [[m > n]], (나) [[m]], (다) 짝수",
             "(가) [[m < n]], (나) [[n - m]], (다) 홀수",
             "(가) [[m < n]], (나) [[m - n]], (다) 짝수"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="출처 [2008년 9월 고2 이과 9번]. 0<n/m<1 → m>n, 10^n=2^m → 2^(m-n)=5^n, 좌변 짝수·우변 홀수 → ①. 지수 빈칸 '2^(나)'와 마지막 빈 상자 '□'는 텍스트.")

# p39 — 로그에 대한 증명 (log_{a^m} b^n)
add(id="332df856", qtype="choice",
    question=("다음은 로그의 성질 [[log(p, pow(q, r)) = r log(p, q)]] 를 이용하여\n"
              "[[m]] 이 0 이 아닌 실수일 때,\n"
              "[[log(pow(a, m), pow(b, n)) = frac(n, m) log(a, b)]] (단, [[a]]는 1이 아닌 양수, [[b]]는 양수)\n"
              "가 성립함을 증명한 것이다.\n\n"
              "<증명>\n"
              "[[x = log(pow(a, m), pow(b, n))]] 로 놓으면\n"
              "[[pow(b, n)]] = (가) = ([[pow(a, x)]])^(나) 이므로\n"
              "[[pow(a, x)]] = (다)\n"
              "따라서 [[x]] = log_a (다) = [[frac(n, m) log(a, b)]]가\n"
              "성립한다.\n\n"
              "위의 증명에서 (가), (나), (다)에 알맞은 것을 차례로\n"
              "나열한 것은?"),
    choices=["(가) [[pow(a, x)]], (나) [[m]], (다) [[pow(b, n)]]",
             "(가) [[pow(a, x)]], (나) [[frac(m, n)]], (다) [[pow(b, frac(n, m))]]",
             "(가) [[pow(pow(a, m), x)]], (나) [[m]], (다) [[pow(b, frac(n, m))]]",
             "(가) [[pow(pow(a, m), x)]], (나) [[m]], (다) [[pow(b, n)]]",
             "(가) [[pow(pow(a, m), x)]], (나) [[frac(m, n)]], (다) [[pow(b, frac(n, m))]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="출처 [2004년 9월 고3 문과 15번]. b^n=(a^m)^x=(a^x)^m → a^x=b^(n/m) → ③. 지수 빈칸 '(a^x)^(나)'·'log_a (다)'는 텍스트.")

# p40 — 로그에 대한 증명 (log_a x^n = n log_a x)
add(id="0273cc5b", qtype="choice",
    question=("다음은 두 양수 [[a]], [[x]]에 대하여\n"
              "[[log(a, pow(x, n)) = n log(a, x)]] ([[a != 1]], [[n]]은 실수)가 성립함을 증명한\n"
              "것이다.\n\n"
              "[[log(a, x) = r]]로 놓으면\n"
              "[[x]] = (가) 이므로 [[pow(x, n) = pow(a, n r)]]\n"
              "따라서 (나) = [[n r]]이므로\n"
              "[[log(a, pow(x, n)) = n log(a, x)]]\n\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 차례대로 나열한\n"
              "것은?"),
    choices=["[[log(a, r)]], [[log(a, x)]]",
             "[[log(a, r)]], [[log(a, n)]]",
             "[[pow(a, r)]], [[log(a, x)]]",
             "[[pow(a, r)]], [[log(a, pow(x, n))]]",
             "[[a]], [[log(a, pow(x, n))]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="(가)=a^r, (나)=log_a x^n → ④. 출처 머리말 없음. 빈칸 상자는 텍스트.")

# p41 — 로그에 대한 증명 (밑 변환 공식)
add(id="18df84b2", qtype="choice",
    question=("다음은 세 양수 [[a]], [[b]], [[c]] ([[a != 1]], [[c != 1]])에 대하여\n"
              "[[log(a, b) = frac(log(c, b), log(c, a))]]\n"
              "가 성립함을 증명한 것이다.\n\n"
              "[[log(a, b) = x]], [[log(c, a) = y]]로 놓으면\n"
              "[[pow(a, x) = b]], [[pow(c, y) = a]]이므로\n"
              "[[b = pow(c, x y)]]\n"
              "따라서 [[log(c, b)]] = (가) 이므로\n"
              "[[log(c, b) = log(a, b) × log(c, a)]]\n"
              "이때 [[a != 1]]에서 [[log(c, a)]] ≠ (나) 이므로\n"
              "[[log(a, b) = frac(log(c, b), log(c, a))]]\n\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 차례대로 나열한\n"
              "것은?"),
    choices=["[[x y]], [[-1]]", "[[x y]], [[0]]", "[[x y]], [[1]]", "[[x + y]], [[0]]", "[[x + y]], [[1]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="(가)=xy, (나)=0 → ②. 출처 머리말 없음. 빈칸 상자는 텍스트.")

# p42 — 로그에 대한 증명 (log_4 n 유리수)
add(id="ab41fa7d", qtype="choice",
    question=("다음은 자연수 [[n]]에 대하여 [[log(4, n)]]이 유리수이면 [[n]]을\n"
              "[[n = pow(2, k)]] ([[k]]는 [[k >= 0]]인 정수)의 꼴로 나타낼 수 있음을\n"
              "증명한 것이다.\n\n"
              "자연수 [[n]]에 대하여 [[log(4, n)]]이 유리수라고 하자.\n"
              "[[n]]이 자연수이므로 [[n = pow(2, k) × m]]을 만족시키는\n"
              "[[k >= 0]]인 정수 [[k]]와 홀수인 자연수 [[m]]이 존재한다.\n"
              "그러면 [[log(4, n)]] = (가) + [[log(4, m)]]\n"
              "따라서 [[log(4, n)]]이 유리수이면 [[log(4, m)]]도\n"
              "유리수이어야 하므로 [[log(4, m) = frac(q, p)]]\n"
              "([[p]]는 자연수, [[q]]는 정수)로 놓을 수 있다.\n"
              "그러면 (나) 에서 [[m]]이 홀수이므로 [[pow(m, p)]]은\n"
              "홀수이다.\n"
              "따라서 (다) 이고 [[m = 1]]이다.\n"
              "그러므로 [[n]]을 [[n = pow(2, k)]] ([[k]]는 [[k >= 0]]인 정수)의 꼴로\n"
              "나타낼 수 있다.\n\n"
              "위의 증명 과정에서 (가), (나), (다)에 알맞은 것을\n"
              "차례대로 나열하면?"),
    choices=["(가) [[k]], (나) [[pow(m, q) = pow(2, p)]], (다) [[q = 1]]",
             "(가) [[k]], (나) [[pow(m, p) = pow(2, 2q)]], (다) [[q = 1]]",
             "(가) [[frac(k, 2)]], (나) [[pow(m, q) = pow(2, p)]], (다) [[q = 0]]",
             "(가) [[frac(k, 2)]], (나) [[pow(m, p) = pow(2, q)]], (다) [[q = 1]]",
             "(가) [[frac(k, 2)]], (나) [[pow(m, p) = pow(2, 2q)]], (다) [[q = 0]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="log₄(2^k·m)=k/2+log₄m, m^p=4^q=2^(2q), 홀수=2^(2q) → q=0 → ⑤. 출처 머리말 없음. 빈칸 상자는 텍스트.")

# p43 — 로그에 대한 증명 (p37 변형)
add(id="b588637f", qtype="choice",
    question=("다음은 [[a]], [[b]]가 1이 아닌 양의 실수일 때,\n"
              "'[[log(a, b) = log(b, a)]]이면 [[frac(pow(a,2) + 1, pow(b,2) + 1) = frac(a, b)]]이다.' ⋯ (∗)\n"
              "가 성립함을 증명한 것이다.\n\n"
              "<증명>\n"
              "[[log(b, a) = frac(1, log(a, b))]]이고 가정에서\n"
              "[[log(a, b) = log(b, a)]]이므로\n"
              "[[log(a, b)]] = (가) 또는 [[log(a, b)]] = (나) 이다.\n"
              "(ⅰ) [[log(a, b)]] = (가) 일 때, [[frac(pow(a,2) + 1, pow(b,2) + 1) = 1]]이고\n"
              "[[frac(a, b) = 1]]이다.\n"
              "(ⅱ) [[log(a, b)]] = (나) 일 때, [[frac(pow(a,2) + 1, pow(b,2) + 1)]] = (다) 이고\n"
              "[[frac(a, b)]] = (다) 이다.\n"
              "따라서 (ⅰ), (ⅱ)에 의하여 [[frac(pow(a,2) + 1, pow(b,2) + 1) = frac(a, b)]]이므로\n"
              "(∗)가 성립한다.\n\n"
              "위 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[1]], (나) [[-1]], (다) [[pow(a,2)]]",
             "(가) [[1]], (나) [[-1]], (다) [[pow(b,2)]]",
             "(가) [[1]], (나) [[1]], (다) [[a b]]",
             "(가) [[-1]], (나) [[-1]], (다) [[pow(a,2)]]",
             "(가) [[-1]], (나) [[1]], (다) [[pow(b,2)]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="(가)=1, (나)=-1, (다)=a² → ①. 출처 머리말 없음. 빈칸 상자는 텍스트, 표 형태 선지는 '(가) …' 문자열로.")

# p44 — 로그에 대한 증명 (p41 변형)
add(id="ea1b33e7", qtype="choice",
    question=("다음은 세 양수 [[a]], [[b]], [[c]] ([[a != 1]], [[c != 1]])에 대하여\n"
              "[[log(a, b) = frac(log(c, b), log(c, a))]]가 성립함을 증명한 것이다.\n\n"
              "[[log(a, b) = x]], [[log(c, a) = y]]로 놓으면\n"
              "[[pow(a, x) = b]], [[pow(c, y) = a]]이므로\n"
              "[[b = pow(c, x y)]]\n"
              "따라서 (가) = [[x y]]이므로\n"
              "(가) = [[log(a, b) × log(c, a)]]\n"
              "이때 [[a != 1]]에서 [[log(c, a)]] ≠ (나) 이므로\n"
              "[[log(a, b) = frac(log(c, b), log(c, a))]]\n\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 차례대로 나열한\n"
              "것은?"),
    choices=["[[log(b, c)]], [[-1]]", "[[log(b, c)]], [[0]]", "[[log(c, b)]], [[-1]]", "[[log(c, b)]], [[0]]", "[[log(c, b)]], [[1]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="(가)=log_c b, (나)=0 → ④. 출처 머리말 없음. 빈칸 상자는 텍스트.")

# p47 — 로그의 성질의 활용(1)
add(id="3be59d9e", qtype="choice",
    question="[[log(3, 2) = a]], [[log(3, 5) = b]]라 할 때, [[log(8, 125)]]를 [[a]], [[b]]로\n나타내면?",
    choices=["[[1 - 2b]]", "[[2b - a]]", "[[a - b]]", "[[frac(b, a)]]", "[[frac(a, b)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="log₈125 = 3log₃5/(3log₃2) = b/a → ④. 출처 머리말 없음.")

# p51 — 로그의 성질의 활용(1)
add(id="90034bfc", qtype="short",
    question=("1이 아닌 양수 [[a]], [[b]], [[c]], [[x]]에 대하여 [[log(a, x) = 1]],\n"
              "[[log(b, x) = 3]], [[log(c, x) = 4]]일 때, [[log(a b c, x)]]의 값을 구하시오."),
    choices=None, derived_answer="frac(12,19)", figure=None, difficulty_est=2, confidence=0.9,
    note="log_x a + log_x b + log_x c = 1 + 1/3 + 1/4 = 19/12 → 역수 12/19 = 빠른정답 ✓. 출처 머리말 없음.")

# p56 — 로그의 성질의 활용(2)
add(id="240b8715", qtype="short",
    question=("네 양수 [[a]], [[b]], [[c]], [[k]]가 다음 조건을 만족할 때, [[pow(k, 4)]]의 값을\n구하시오.\n"
              "(가) [[pow(6, a) = pow(3, b) = pow(k, c)]]\n"
              "(나) [[log(c) = log(4 a b) - log(4 a + b)]]"),
    choices=None, derived_answer="486", figure=None, difficulty_est=3, confidence=0.85,
    note="공통값 t: 1/a=log_t6, 1/b=log_t3, 1/c=(4a+b)/(4ab)=1/b+1/(4a) → k=3·6^(1/4) → k⁴=486. 출처 머리말 없음. 조건 상자는 텍스트.")

# p60 — 식의 값 구하기
add(id="d3d698e2", qtype="short",
    question=("두 양수 [[x]], [[y]]에 대하여 [[log(36, pow(x, 3)) + log(6, pow(y, 3)) = 3]]일 때,\n"
              "[[pow(3, log(sqrt(6), x)) × pow(3, log(sqrt(6), pow(y, 2)))]]의 값을 구하시오."),
    choices=None, derived_answer="81", figure=None, difficulty_est=3, confidence=0.85,
    note="log₆(xy²)=2 → xy²=36; 3^(log_√6 36)=3^4=81. 출처 머리말 없음.")

# p62 — 식의 값 구하기
add(id="e6b3f14e", qtype="choice",
    question=("두 실수 [[a]], [[b]]가 [[a b = log(2, 7)]], [[b - a = log(3, 7)]]을 만족시킬\n"
              "때, [[frac(1, a) - frac(1, b)]]의 값은?"),
    choices=["[[log(5, 2)]]", "[[log(3, 2)]]", "[[log(3, 5)]]", "[[log(2, 3)]]", "[[log(2, 5)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(b-a)/(ab) = log₃7/log₂7 = log₃2 → ②. 빠른정답 1과 불일치. 출처 머리말 없음.")

# p64 — 식의 값 구하기
add(id="8a5e0804", qtype="choice",
    question=("두 실수 [[a]], [[b]]가 [[2a + 3b = log(2, 81)]], [[a b = log(4, 3)]]을\n"
              "만족시킬 때, [[frac(1, 2a) + frac(1, 3b)]]의 값은?"),
    choices=["[[frac(7,6)]]", "[[frac(4,3)]]", "[[frac(3,2)]]", "[[frac(5,3)]]", "[[frac(11,6)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2023년 9월 고3 7번 변형]. (2a+3b)/(6ab) = 4log₂3/(3log₂3) = 4/3 → ②.")
