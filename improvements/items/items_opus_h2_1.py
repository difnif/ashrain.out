# -*- coding: utf-8 -*-
# esc_opus_h2-1_1of1 — 이미지 기준 전사 (58 항목 / 49쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))
SEQ = "[[set(sub(a,n))]]"
CH_GD = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_GN = ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_GL = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# 여러 가지 수열의 합 p3
add(id="e83dfab7", qtype="choice",
    question=("집합 [[A]] = { [[a]] | [[2 <= a <= 8]], [[a]]는 자연수 }의 원소 [[a]]와 집합 [[B]] = { [[b]] | [[2 <= b <= 5]], [[b]]는 자연수 }는 "
              "자연수의 원소 [[b]]에 대하여 다음 조건을 만족시키는 [[m]], [[n]]의 모든 순서쌍 [[point(m, n)]]의 개수는?\n"
              "(가) [[m]], [[n]]은 모두 자연수이다.\n(나) [[a]]는 [[m n]]의 [[b]]제곱근이다."),
    choices=["[[214]]", "[[224]]", "[[234]]", "[[244]]", "[[254]]"], derived_answer="②", quick_answer="2", figure=None, difficulty_est=4,
    note="원문 문장('…}는 자연수의 원소 b에 대하여') 그대로. mn=a^b인 (m,n) 서로 다른 순서쌍: Σd(a^b)=236에서 중복(16,64) 12 제외 → 224 → ② = 빠른정답 ✓.")
# p83 (id 2개) 등비수열 곱
dup(["e5667b0d", "cb73aadc"], qtype="choice",
    question=("첫째항이 2이고 공비가 2인 등비수열 " + SEQ + "에서 임의의 연속된 [[2m + 1]]개의 항\n"
              "[[sub(a,k)]], [[sub(a,k+1)]], [[sub(a,k+2)]], ⋯, [[sub(a,k+2m)]]에 대하여\n"
              "[[sub(a,k) sub(a,k+1)]] ⋯ [[sub(a,k+m)]] = [[sub(a,k+m+1) sub(a,k+m+2)]] ⋯ [[sub(a,k+2m)]]\n"
              "일 때, [[sub(a,k+m)]]을 [[sub(b,m)]]이라 하자. 이 때, <보기>에서 옳은 것만을 있는 대로 고른 것은? (단, [[k]], [[m]]은 자연수이다.)\n<보기>\n"
              "ㄱ. [[sub(b,1) = 4]]\nㄴ. 수열 [[sub(b,1)]], [[sub(b,2)]], [[sub(b,3)]], ⋯은 등비수열이다.\n"
              "ㄷ. [[sum(m, 1, 10, log(2, sub(b,m))) = 440]]"),
    choices=CH_GN, derived_answer="③", quick_answer="9", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2009년 9월 고2 이과 14번]. k=m², b_m=2^(m²+m): ㄱ✓ ㄴ✗ ㄷ✓(385+55) → ③. 빠른정답 9는 선지 범위 밖. 곱의 '⋯'는 텍스트로 분절 전사.")
# 삼각함수 p29
add(id="5e4a5dc5", qtype="short",
    question=("두 실수 [[a]], [[b]] ([[a != 0]], [[b > 1]])에 대하여 함수 [[f(x)]]를 [[f(x) = a cos(frac(pi,3)(x - 2)) + b]]라 하고, "
              "[[g(x) = abs(f(x))]] 라 하자. 양수 [[t]]에 대하여 [[0 <= x <= t]]에서 함수 [[g(x)]]의 그래프가 직선 [[y = 2]]와 만나는 점의 개수를 "
              "[[h(t)]]라 하자. 함수 [[f(x)]]의 그래프는 원점을 지나고, [[h(9) = 4]]일 때, [[h(n) = a + b]]를 만족시키는 모든 자연수 [[n]]의 값의 합을 구하시오."),
    choices=None, derived_answer="23", quick_answer="3", figure=None, difficulty_est=5, confidence=0.8,
    note="출처 [2020년 11월 고2 30번 변형]. a=2b, h(9)=4 ⇒ b=2, a=4; |f|=2인 x: 0.5,3.5,5,6.5,9.5,11,12.5,… → h(n)=6 ⇔ n=11,12 → 23. 빠른정답 3과 불일치.")
# 삼각함수 p38
add(id="f539123c", qtype="choice",
    question=("자연수 [[k]]에 대하여 집합 [[sub(A,k)]]를\n[[sub(A,k)]] = { [[sin(frac(m - 1, k) pi)]] | [[m]]은 자연수 }라 할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(A,2) = set(-1, 0, 1)]]\nㄴ. 1이 집합 [[sub(A,k)]]의 원소가 되도록 하는 두 자리 자연수 [[k]]의 개수는 45이다.\n"
              "ㄷ. [[card(sub(A,k)) = 15]]를 만족시키는 모든 [[k]]의 값의 합은 29이다."),
    choices=CH_GL, derived_answer="⑤", quick_answer="5", figure=None, difficulty_est=4,
    note="출처 [2020년 4월 고3 이과 21번 변형]. ㄱ✓, ㄴ k 짝수 45개 ✓, ㄷ n(A_k)=k+1(짝수)/k(홀수) → k=14,15 합 29 ✓ → ⑤ = 빠른정답 ✓.")
# 삼각함수 p45
add(id="02dfe7bc", qtype="short",
    question=("두 실수 [[a]], [[b]]와\n두 함수 [[f(x) = sin(x)]], [[g(x) = a cos(x) + b]]에 대하여\n[[0 <= x <= 2 pi]]에서 정의된\n"
              "함수 [[h(x) = frac(abs(f(x) - g(x)) + f(x) + g(x), 2)]]가\n다음 조건을 만족시킨다.\n"
              "(가) 함수 [[h(x)]]의 최솟값은 [[-frac(sqrt(3), 2)]] 이다.\n(나) [[0 < c < frac(pi,2)]] 인 어떤 실수 [[c]]에 대하여\n[[h(c) = h(c + pi) = frac(1,2)]] 이다.\n"
              "상수 [[k]] ([[k > frac(1,2)]])에 대하여 방정식 [[h(x) = k]]가 서로 다른 세 실근을 가질 때, [[a + 20 pow(frac(k, b), 2)]]의 값을 구하시오."),
    choices=None, derived_answer="59", quick_answer="59", figure=None, difficulty_est=5,
    note="출처 [2022년 6월 고2 30번/4점]. h=max(sin x, g): c=π/6, a=−1, b=(1−√3)/2, k=(3−√3)/2 → (k/b)²=3 → 59 = 빠른정답 ✓.")
# 삼각함수 p83 — 그리스 문자 함수 α(t) 표기 불가 → review
add(id="b7b42bcd", qtype="choice",
    question=("[[-1 <= t <= 1]]인 실수 [[t]]에 대하여\n[[x]]에 대한 방정식 [[(sin(frac(pi x, 2)) - t)(cos(frac(pi x, 2)) - t) = 0]]의\n"
              "실근 중에서 집합 { [[x]] | [[0 <= x < 4]] }에 속하는 가장 작은 값을 [[alpha]]([[t]]), 가장 큰 값을 [[beta]]([[t]])라 하자. "
              "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[-1 <= t < 0]]인 모든 실수 [[t]]에 대하여 [[alpha]]([[t]]) + [[beta]]([[t]]) = 5이다.\n"
              "ㄴ. { [[t]] | [[beta]]([[t]]) − [[alpha]]([[t]]) = [[beta]](0) − [[alpha]](0) } = { [[t]] | [[0 <= t <= frac(sqrt(2), 2)]] }\n"
              "ㄷ. [[alpha]]([[sub(t,1)]]) = [[alpha]]([[sub(t,2)]])인 두 실수 [[sub(t,1)]], [[sub(t,2)]]에 대하여 [[sub(t,2) - sub(t,1) = frac(1,2)]] 이면 [[sub(t,1) sub(t,2) = frac(1,3)]] 이다."),
    choices=CH_GL, derived_answer="②", quick_answer="3", figure=None, difficulty_est=5, confidence=0.75,
    needs_review="문법 범위 밖: 그리스 문자 함수 α(t), β(t)의 적용 표기(alpha(t)는 '미지의 함수' 오류) → 텍스트 혼합 전사",
    note="출처 [2021년 6월 고3 15번/4점]. ㄱ✓(θ합 5π/2), ㄴ✓, ㄷ✗(t₁=(√7−1)/4, t₂=(√7+1)/4 → t₁t₂=3/8) → ②. 빠른정답 3과 불일치.")
# 지수함수의 활용 p43
add(id="8430976d", qtype="short",
    question=("지수함수 [[f(x) = pow(a, x)]], [[g(x) = pow(b, x)]] 에 대하여\n다음 조건을 만족시키는 [[a]], [[b]]의 모든 순서쌍 [[point(a, b)]]의\n개수를 구하시오. (단, [[a]], [[b]]는 1보다 큰 자연수이다.)\n"
              "(가) [[f(2) × g(11) = pow(2, 2015)]]\n(나) [[f(2) < g(4)]]"),
    choices=None, derived_answer="25", quick_answer="25", figure=None, difficulty_est=4,
    note="출처 [2014년 6월 고2 문과 30번/4점]. a=2^p,b=2^q, 2p+11q=2015, p<2q → q 홀수 135~183 → 25 = 빠른정답 ✓.")
# 수학적 귀납법 p28 (빈칸)
_S = lambda hi, body: f"sum(k, 1, {hi}, {body})"
add(id="fc7848eb", qtype="choice",
    question=("수열 " + SEQ + "의 일반항은 [[sub(a,n) = n + 1]]이다.\n다음은 모든 자연수 [[n]]에 대하여\n"
              "[[pow(sum(k, 1, n, sub(a,k)), 2) = sum(k, 1, n, pow(sub(a,k), 3)) - 2 sum(k, 1, n, sub(a,k))]] …… (*)\n"
              "가 성립함을 수학적 귀납법을 이용하여 증명한 것이다.\n\n"
              "(ⅰ) [[n = 1]]일 때,\n(좌변) = [[pow(sum(k, 1, 1, sub(a,k)), 2) = 4]],\n"
              "(우변) = [[sum(k, 1, 1, pow(sub(a,k), 3)) - 2 sum(k, 1, 1, sub(a,k)) = 4]]이므로 (*)이 성립한다.\n"
              "(ⅱ) [[n = m]] ([[m >= 1]])일 때, (*)이 성립한다고 가정하면\n"
              "[[pow(sum(k, 1, m, sub(a,k)), 2) = sum(k, 1, m, pow(sub(a,k), 3)) - 2 sum(k, 1, m, sub(a,k))]]이므로\n"
              "[[pow(sum(k, 1, m + 1, sub(a,k)), 2)]]\n= [[pow(sum(k, 1, m, sub(a,k)) + sub(a,m+1), 2)]]\n"
              "= [[pow(sum(k, 1, m, sub(a,k)), 2) + 2(sum(k, 1, m, sub(a,k))) sub(a,m+1) + pow(sub(a,m+1), 2)]]\n"
              "= [[sum(k, 1, m, pow(sub(a,k), 3)) - 2 sum(k, 1, m, sub(a,k)) + 2(sum(k, 1, m, sub(a,k))) sub(a,m+1) + pow(sub(a,m+1), 2)]]\n"
              "= [[sum(k, 1, m, pow(sub(a,k), 3))]] + 2([[m]] + (가))[[sum(k, 1, m, sub(a,k))]] + [[pow(sub(a,m+1), 2)]]\n"
              "= [[sum(k, 1, m, pow(sub(a,k), 3)) + pow(sub(a,m+1), 3)]] − (나)\n"
              "= [[sum(k, 1, m + 1, pow(sub(a,k), 3)) - 2 sum(k, 1, m + 1, sub(a,k))]]\n"
              "즉, [[n = m + 1]]일 때에도 (*)이 성립한다.\n따라서 (ⅰ), (ⅱ)에서 모든 자연수 [[n]]에 대하여 (*)이 성립한다.\n\n"
              "위의 (가)에 알맞은 수를 [[p]], (나)에 알맞은 식을 [[f(m)]]이라 할 때, [[f(p)]]의 값은?"),
    choices=["[[10]]", "[[11]]", "[[12]]", "[[13]]", "[[14]]"], derived_answer="①", quick_answer="4", figure=None, difficulty_est=4, confidence=0.8,
    note="(가)=1, (나)=(m+1)(m+4) → f(1)=10 → ①. 빠른정답 4와 불일치. 빈칸 상자는 텍스트.")
# 수학적 귀납법 p40 (빈칸, 표 선지)
add(id="c356caa5", qtype="choice",
    question=("다음은 수열 " + SEQ + "의 일반항 [[sub(a,n)]]이 [[sub(a,n) = p n + q]]일 때,\n모든 자연수 [[n]]에 대하여\n"
              "[[n sub(a,1) + (n - 1) sub(a,2) + (n - 2) sub(a,3)]] + ⋯ + [[sub(a,n)]]\n= [[frac(1,6) n(n + 1)(p n + 2p + 3q)]]\n"
              "임을 수학적 귀납법으로 증명한 것이다.\n\n[증명]\n(ⅰ) [[n = 1]]일 때, (좌변)=(우변)= (가) 이므로 성립한다.\n"
              "(ⅱ) [[n = k]]일 때 성립한다고 가정하면\n[[k sub(a,1) + (k - 1) sub(a,2) + (k - 2) sub(a,3)]] + ⋯ + [[sub(a,k)]]\n"
              "= [[frac(1,6) k(k + 1)(p k + 2p + 3q)]]\n이 식의 양변에 (나) 를 더하면\n"
              "[[k sub(a,1) + (k - 1) sub(a,2) + (k - 2) sub(a,3)]] + ⋯ + [[sub(a,k)]] + (나)\n"
              "= [[frac(1,6) k(k + 1)(p k + 2p + 3q)]] + (나)\n= [[frac(1,6)(k + 1)]]{[[p pow(k,2) + (5p + 3q) k]] + (다)}\n"
              "= [[frac(1,6)(k + 1)(k + 2)(p(k + 1) + 2p + 3q)]]\n그러므로 [[n = k + 1]]일 때도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 주어진 등식은 모든 자연수 [[n]]에 대하여 성립한다.\n\n이 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[p q]], (나) [[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,k)]], (다) [[3(p + q)]]",
             "(가) [[p q]], (나) [[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,k)]], (다) [[4(p + q)]]",
             "(가) [[p + q]], (나) [[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,k)]], (다) [[6(p + q)]]",
             "(가) [[p + q]], (나) [[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,k+1)]], (다) [[4(p + q)]]",
             "(가) [[p + q]], (나) [[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,k+1)]], (다) [[6(p + q)]]"],
    derived_answer="⑤", quick_answer="1", figure=None, difficulty_est=3, confidence=0.8,
    note="출처 [2007년 11월 고2 이과 16번]. (가)=p+q, (나)=a₁+…+a_{k+1}, (다)=6(p+q) → ⑤. 빠른정답 1과 불일치. 표 형태 선지는 '(가) …, (나) …, (다) …' 문자열로.")
# 지수함수 p36
add(id="8fd761ca", qtype="short",
    question=("두 함수 [[y = pow(4, x)]], [[y = frac(1, pow(2, a)) × pow(4, x) - a]]의 그래프와\n두 직선 [[y = -2x - log(b)]], [[y = -2x + log(c)]]로 둘러싸인\n"
              "도형의 넓이가 3이 되도록 하는 자연수 [[a]], [[b]], [[c]]의\n순서쌍 ([[a]], [[b]], [[c]])의 개수를 구하시오."),
    choices=None, derived_answer="78", quick_answer="3", figure=None, difficulty_est=5, confidence=0.8,
    note="출처 [2023년 경찰대 25번/5점]. 평행이동 벡터(a/2,−a)가 직선과 평행 → 넓이 a·log(bc)/2=3 → bc=10^(6/a), a∈{1,2,3,6} → 49+16+9+4=78. 빠른정답 3과 불일치(옆 문항 p39의 빠른정답이 78).")
# 지수함수 p39 (id 3개)
dup(["2c195c12", "dbc78320", "cf4cd555"], qtype="short",
    question=("자연수 [[a]], [[b]]에 대하여 곡선 [[y = pow(a, x + 1)]]과 곡선 [[y = 5 pow(b, x)]]이\n직선 [[x = t]] ([[t >= 1]])과 만나는 점을 각각 P, Q라 하자.\n"
              "다음 조건을 만족시키는 [[a]], [[b]]의 모든 순서쌍 [[point(a, b)]]의\n개수를 구하시오.\n(예를 들어, [[a = 6]], [[b = 7]]은 다음 조건을 만족시킨다.)\n"
              "(가) [[6 <= a <= 12]], [[6 <= b <= 12]]\n(나) [[t >= 1]]인 어떤 실수 [[t]]에 대하여 [[seg(PQ) <= 18]]이다."),
    choices=None, derived_answer="21", quick_answer="78", figure=None, difficulty_est=5, confidence=0.8,
    note="a=b: (6,6),(7,7); a>b: 없음; a<b: a²−5b≥−18 → 19 → 21. 빠른정답 78과 불일치(p36 답으로 추정).")
# 지수함수 p40 (id 3개)
dup(["8b2d8e81", "2cf5ac71", "d7ba5dc8"], qtype="short",
    question=("자연수 [[a]], [[b]]에 대하여 곡선 [[y = pow(a, x + 1)]]과 곡선 [[y = 3 pow(b, x)]]이\n직선 [[x = t]] ([[t >= 1]])과 만나는 점을 각각 P, Q라 하자.\n"
              "다음 조건을 만족시키는 [[a]], [[b]]의 모든 순서쌍 [[point(a, b)]]의\n개수를 구하시오.\n(예를 들어, [[a = 4]], [[b = 5]]는 다음 조건을 만족시킨다.)\n"
              "(가) [[4 <= a <= 10]], [[4 <= b <= 10]]\n(나) [[t >= 1]]인 어떤 실수 [[t]]에 대하여 [[seg(PQ) <= 10]]이다."),
    choices=None, derived_answer="21", quick_answer="170", figure=None, difficulty_est=5, confidence=0.8,
    note="a=b: (4,4),(5,5); a>b: 없음; a<b: a²−3b≥−10 → 19 → 21. 빠른정답 170과 불일치.")
# 지수함수 p89 (조각적 정의)
add(id="18ac8550", qtype="short",
    question=("양의 실수 [[a]]에 대하여 함수 [[f(x)]]를\n[[f(x)]] = { [[pow(3, x) + pow(3, -a) - 2]] ([[x < a]]) ; [[pow(3, -x) + pow(3, a) - 2]] ([[x >= a]]) }\n"
              "라 할 때, 함수 [[f(x)]]가 다음 조건을 만족시키도록 하는 [[a]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 하자.\n"
              "함수 [[y = abs(f(x))]]의 그래프와 직선 [[y = k]]가 서로 다른 두 점에서 만나도록 하는 양수 [[k]]는 오직 하나뿐이다.\n"
              "[[pow(9, M + m) = p + 4 sqrt(q)]] 일 때, [[p q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 자연수이다.)"),
    choices=None, derived_answer="12", quick_answer="4", figure=None, difficulty_est=5, confidence=0.75,
    needs_review="문법 범위 밖: 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사",
    note="출처 [2022년 11월 고2 30번 변형]. 3^a∈[(2+√2)/2, 2] → 9^(M+m)=(2+√2)²=6+4√2 → pq=12. 빠른정답 4와 불일치.")
# 로그함수 p29
add(id="ec75df22", qtype="short",
    question=("함수 [[f(x) = log(2, x)]]에 대하여 곡선 [[y = f(x)]]를\n[[x]]축의 방향으로 3만큼, [[y]]축의 방향으로 [[-4]]만큼\n평행이동한 곡선을 [[y = g(x)]]라 하자.\n"
              "곡선 [[y = f(x)]] 위의 점 P를 지나고 기울기가 [[-frac(4,3)]] 인\n직선이 곡선 [[y = g(x)]]와 만나는 점을 Q,\n기울기가 [[frac(3,4)]] 인 직선이 곡선 [[y = g(x)]]와 만나는 점을\n"
              "R라 하자. [[seg(PQ) = seg(PR)]]가 성립하도록 하는 점 P의 [[x]]좌표를\n[[a]]라 할 때, [[254 a]]의 값을 구하시오."),
    choices=None, derived_answer="2", quick_answer="2", figure=None, difficulty_est=4,
    note="평행이동 벡터(3,−4)가 기울기 −4/3 → PQ=5, R=P+(4,3) → a=1/127 → 254a=2 = 빠른정답 ✓.")
# 로그함수 p40 (조각적 정의)
add(id="7a3c7cd6", qtype="choice",
    question=("함수 [[f(x)]] = { [[pow(3, x + 1)]] ([[x <= 1]]) ; [[9 - 3 log(3, x)]] ([[x > 1]]) }에 대하여\n"
              "다음 조건을 만족시키는 모든 양수 [[k]]의 값의 집합이\n{ [[k]] | [[0 < k <= alpha]] 또는 [[beta < k < gamma]] }일 때, [[alpha + beta + gamma]]의\n값은? (단, [[alpha]], [[beta]], [[gamma]]는 상수이다.)\n"
              "함수 [[y = abs(f(x) - k)]]의 그래프가\n두 직선 [[y = p]], [[y = 2p]]와 만나는 점의 개수가 각각\n3, 2가 되도록 하는 양수 [[p]]가 존재한다."),
    choices=["[[17]]", "[[18]]", "[[19]]", "[[20]]", "[[21]]"], derived_answer=None, quick_answer=None, figure=None, difficulty_est=5, confidence=0.75,
    needs_review="문법 범위 밖: 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사 (답 미도출)",
    note="출처 [2026년 6월 고2 21번 변형]. 빠른정답 없음.")
# 로그함수 p53
add(id="47bd11c1", qtype="short",
    question=("두 자연수 [[m]], [[n]]에 대하여 곡선 [[y = pow(3, x - m) + n]] 위의\n점 [[A(a, b)]] ([[a < b]])가 제1사분면에 있다. 점 A를\n직선 [[y = x]]에 대하여 대칭이동한 점을 B라 하자. 점 B를\n"
              "중심으로 하고 반지름의 길이가 [[5 sqrt(2)]] 인 원이\n곡선 [[y = log(3, x - n + 1) + m - 7]]과 만나는 두 점 중\n[[x]]좌표가 작은 점을 C라 할 때, 세 점 A, B, C가 다음\n조건을 만족시킨다.\n"
              "(가) 직선 AC와 직선 [[y = frac(1,3) x]]는 서로 수직이다.\n(나) 삼각형 AOB와 삼각형 ACB의 넓이의 비는\n[[ratio(31, 8)]]이다.\n"
              "[[m + n]]의 최댓값을 구하시오. (단, O는 원점이다.)"),
    choices=None, derived_answer=None, quick_answer=None, figure=None, difficulty_est=5, confidence=0.85,
    note="출처 [2026년 7월 고3 22번 변형]. 빠른정답 없음, 답 미도출(null).")
# 귀납적 정의 p44
add(id="8be4ae0a", qtype="short",
    question=("수열 " + SEQ + "이\n[[sub(a,1) = 2]], [[sub(a,n+1) = 2 sub(a,n) + 3 × pow(5, n - 1)]] ([[n]] = 1, 2, 3, ⋯)으로\n"
              "정의될 때, [[sub(a,15)]]는 [[m]]자리의 자연수이다.\n[[m]]의 값을 구하시오. (단, [[log(2) = 0.30]], [[log(3) = 0.48]],\n[[log(7) = 0.85]]로 계산한다.)"),
    choices=None, derived_answer="10", quick_answer="10", figure=None, difficulty_est=4,
    note="a_n=2^(n−1)+5^(n−1), a₁₅≈6.1×10⁹ → 10자리 = 빠른정답 ✓.")
# 귀납적 정의 p89
add(id="7d2c2b1a", qtype="short",
    question=("자연수 [[n]]에 대하여 순서쌍 [[point(sub(x,n), sub(y,n))]]을 다음 규칙에 따라\n정한다.\n"
              "(가) [[point(sub(x,1), sub(y,1)) = point(1, 1)]]\n(나) [[n]]이 홀수이면\n[[point(sub(x,n+1), sub(y,n+1)) = point(sub(x,n), pow(sub(y,n) - 3, 2))]]이고,\n"
              "[[n]]이 짝수이면\n[[point(sub(x,n+1), sub(y,n+1)) = point(pow(sub(x,n) - 3, 2), sub(y,n))]]이다.\n"
              "순서쌍 [[point(sub(x,2015), sub(y,2015))]]에서 [[sub(x,2015) + sub(y,2015)]]의 값을 구하시오."),
    choices=None, derived_answer="8", quick_answer="125", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2014년 6월 고3 문과 28번/4점]. 주기 4: (1,1),(1,4),(4,4),(4,1) → 2015≡3 → (4,4) → 8. 빠른정답 125와 불일치(p92의 빠른정답이 8).")
# 귀납적 정의 p91
add(id="17ff0460", qtype="short",
    question=("자연수 [[n]]에 대하여 두 집합 [[sub(A,n)]], [[sub(B,n)]]이\n"
              "[[sub(A,n)]] = { [[point(x, y)]] | [[pow(x + n, 2) + pow(y, 2) <= pow(n + 1, 2)]], [[x]], [[y]]는 정수 },\n"
              "[[sub(B,n)]] = { [[point(x, y)]] | [[pow(x - n, 2) + pow(y, 2) <= pow(n + 1, 2)]], [[x]], [[y]]는 정수 }\n"
              "일 때, 집합 [[inter(sub(A,n), sub(B,n))]]의 모든 원소의 개수를 [[sub(a,n)]]이라\n하자. [[sum(n, 1, 18, sub(a,n))]]의 값을 구하시오."),
    choices=None, derived_answer="192", quick_answer="192", figure=None, difficulty_est=4,
    note="출처 [2017년 9월 고2 이과 29번/4점]. a_n=3+2⌊√(2n+1)⌋, 합 192 = 빠른정답 ✓ (전수 확인).")
# 귀납적 정의 p92
add(id="fc15f891", qtype="short",
    question=("자연수 [[n]]에 대하여 두 집합 [[sub(A,n)]], [[sub(B,n)]]이\n"
              "[[sub(A,n)]] = { [[point(x, y)]] | [[pow(x, 2) + pow(y - n + 1, 2) < pow(n, 2)]], [[x]], [[y]]는 정수 },\n"
              "[[sub(B,n)]] = { [[point(x, y)]] | [[pow(x, 2) + pow(y + n - 1, 2) < pow(n, 2)]], [[x]], [[y]]는 정수 }\n"
              "일 때, 집합 [[inter(sub(A,n), sub(B,n))]]의 모든 원소의 개수를 [[sub(a,n)]]이라 하자.\n[[sum(n, 1, 14, sub(a,n))]]의 값을 구하시오."),
    choices=None, derived_answer="96", quick_answer="8", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2017년 9월 고2 이과 29번 변형]. a_n=1+2⌊√(2n−2)⌋, 합 96(전수 확인). 빠른정답 8과 불일치.")
# 등차수열 p13
add(id="61585bb7", qtype="short",
    question=("일반항이 [[sub(a,n) = 2n + 1]]인 등차수열 " + SEQ + "에 대하여\n집합 [[sub(A,k)]] ([[k]] = 1, 2, 3, ⋯)는\n"
              "[[sub(A,1) = set(3, 5, 7, 9, 11)]]이고 다음 조건을 만족시킨다.\n"
              "(가) 집합 [[sub(A,k)]]는 수열 " + SEQ + "의 항들 중 [[(2k + 3)]]개의\n연속한 항들을 원소로 하는 집합이다\n"
              "(나) 집합 [[sub(A,k+1)]]의 가장 작은 원소는 집합 [[sub(A,k)]]의\n가장 작은 원소보다 크다.\n(다) [[card(sub(A,k) - sub(A,k+1)) = 3]]\n"
              "예를 들어 [[sub(A,2)]] = {9, 11, 13, ⋯, 21}이다.\n[[inter(sub(A,15), sub(A,p)) = empty]]을 만족하는 15보다 큰 자연수 [[p]]의\n최솟값을 구하시오."),
    choices=None, derived_answer="26", quick_answer="9", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2017년 6월 고2 이과 29번/4점]. A_k 첨자 [3k−2, 5k]; A₁₅=[43,75] → 3p−2>75 → p=26. 빠른정답 9와 불일치(p16의 빠른정답이 26).")
# 등차수열 p16
add(id="8e242d5b", qtype="short",
    question=("일반항이 [[sub(a,n) = 3n + 2]]인 등차수열 " + SEQ + "에 대하여\n집합 [[sub(A,k)]] ([[k]] = 1, 2, 3, ⋯)는\n"
              "[[sub(A,1) = set(5, 8, 11, 14, 17)]]이고 다음 조건을 만족시킨다.\n"
              "(가) 집합 [[sub(A,k)]]는 수열 " + SEQ + "의 항들 중 [[(3k + 2)]]개의\n연속한 항들을 원소로 하는 집합이다.\n"
              "(나) 집합 [[sub(A,k+1)]]의 가장 작은 원소는 집합 [[sub(A,k)]]의 가장\n작은 원소보다 크다.\n(다) [[card(sub(A,k) - sub(A,k+1)) = 2]]\n"
              "예를 들어 [[sub(A,2)]] = {11, 14, 17, ⋯, 32}이다.\n[[inter(sub(A,14), sub(A,p)) != empty]]을 만족하는 자연수 [[p]]의 최솟값과\n최댓값의 합을 구하시오."),
    choices=None, derived_answer="41", quick_answer="26", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2017년 6월 고2 이과 29번 변형]. A_k 첨자 [2k−1, 5k]; A₁₄=[27,70] → 6≤p≤35 → 41. 빠른정답 26과 불일치.")
# 등차수열 p42 (좌표 도형)
add(id="80cb6eba", qtype="choice",
    question=("그림과 같이 좌표축 위의 다섯 개의 점 A, B, C, D, E\n에 대하여 [[perp(seg(AB), seg(BC))]], [[perp(seg(BC), seg(CD))]], [[perp(seg(CD), seg(DE))]]가 성립한다.\n"
              "세 선분 AO, OC, EA의 길이가\n이 순서대로 등차수열을 이룰 때, 직선 AB의 기울기는?\n(단, O는 원점이고 [[seg(OA) < seg(OB)]]이다.)"),
    choices=["[[sqrt(2)]]", "[[sqrt(3)]]", "[[2]]", "[[sqrt(5)]]", "[[sqrt(6)]]"], derived_answer="①", quick_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: E, A는 x축 음의 부분(E가 더 멀리), C는 x축 양의 부분, B는 y축 양의 부분, D는 y축 음의 부분; 꺾은선 A–B–C–D–E, B·C·D에서 직각 표시"}}],
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 좌표축 위 꺾은선 도형",
    note="출처 [2006년 3월 고3 이과 14번]. b²=ac, c²=bd, d²=ce, e=2c → a=c/2, b=c/√2 → 기울기 √2 → ①. 빠른정답 3과 불일치.")
# 등차수열 p60
add(id="94e91ad7", qtype="short",
    question=("14와 2 사이에는 [[n]]개의 수 [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,n)]]을 넣고, 2\n이후에는 [[n]]개의 수 [[sub(b,1)]], [[sub(b,2)]], [[sub(b,3)]], ⋯, [[sub(b,n)]]을 넣어 14, [[sub(a,1)]], [[sub(a,2)]],\n"
              "[[sub(a,3)]], ⋯, [[sub(a,n)]], 2, [[sub(b,1)]], [[sub(b,2)]], [[sub(b,3)]], ⋯, [[sub(b,n)]]이 이 순서대로\n등차수열을 이루도록 하였다.\n"
              "([[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,n)]])\n+ ([[sub(b,1) + sub(b,2) + sub(b,3)]] + ⋯ + [[sub(b,n)]]) > 108\n을 만족시키는 자연수 [[n]]의 최솟값을 구하시오."),
    choices=None, derived_answer="28", quick_answer="3", figure=None, difficulty_est=3, confidence=0.85,
    note="Σa=8n, Σb=−4n → 4n>108 → n=28. 빠른정답 3과 불일치.")
# 등차수열 p89 (id 2개) / p91 (id 2개) — 동일 문항(3P(−1), x+3)
_POLY_Q = ("모든 항이 0이 아닌 등차수열 " + SEQ + "과 1보다 큰\n자연수 [[m]]에 대하여 다항식\n"
           "[[P(x) = sub(a,m+1) pow(x, m) + sub(a,m) pow(x, m - 1) + sub(a,m-1) pow(x, m - 2)]] + ⋯\n+ [[sub(a,2) x + sub(a,1)]]\n"
           "이 있다. [[P(1) = 3 P(-1)]]을 만족시키는\n다항식 [[P(x)]]에서 자연수 [[m]]의 값을 [[k]]라 하자.\n"
           "다항식 [[sub(a,k+1) pow(x, k) + sub(a,k) pow(x, k - 1)]] + ⋯ + [[sub(a,2) x + sub(a,1)]]이 [[x + 3]]으로\n"
           "나누어떨어질 때, [[frac(sub(a,1), sub(a,k+1))]]의 값을 구하시오.")
dup(["ba1b855a", "5b187067"], qtype="short", question=_POLY_Q, choices=None, derived_answer="15", quick_answer="9", figure=None, difficulty_est=4, confidence=0.85,
    note="k=2(m=2이면 항등적으로 성립), 9a₃−3a₂+a₁=0 → 7a₁+15d=0 → a₁/a₃=15. 빠른정답 9와 불일치(p91의 빠른정답이 15).")
dup(["340c8699", "6836c00f"], qtype="short", question=_POLY_Q, choices=None, derived_answer="15", quick_answer="15", figure=None, difficulty_est=4,
    note="출처 [2018년 3월 고2 문과 30번 변형]. k=2, 7a₁+15d=0 → 15 = 빠른정답 ✓.")
dup(["52ac268d", "4a405cd6"], qtype="short",
    question=("모든 항이 0이 아닌 등차수열 " + SEQ + "과 1보다 큰\n자연수 [[m]]에 대하여 다항식\n"
              "[[P(x) = sub(a,m+1) pow(x, m) + sub(a,m) pow(x, m - 1) + sub(a,m-1) pow(x, m - 2)]] + ⋯\n+ [[sub(a,2) x + sub(a,1)]]\n이 있다.\n"
              "[[P(1) = 5 P(-1)]]\n을 만족시키는 다항식 [[P(x)]]에서 자연수 [[m]]의 값을 [[k]]라\n하자.\n"
              "다항식 [[sub(a,k+1) pow(x, k) + sub(a,k) pow(x, k - 1)]] + ⋯ + [[sub(a,2) x + sub(a,1)]]이 [[x + 2]]로\n"
              "나누어떨어질 때, [[frac(sub(a,1), sub(a,k+1))]]의 값을 구하시오."),
    choices=None, derived_answer="23", quick_answer="10", figure=None, difficulty_est=4, confidence=0.8,
    note="출처 [2018년 3월 고2 문과 30번/4점]. k=4(m=4이면 항등), 16a₅−8a₄+4a₃−2a₂+a₁=0 → 11a₁+46d=0 → a₁/a₅=23. 빠른정답 10과 불일치.")
# ∑ p18
add(id="c5dc3140", qtype="short",
    question=("자연수 [[k]]에 대하여 집합 [[sub(A,k)]]가\n[[sub(A,k)]] = { [[frac(b, a)]] | [[log(a, b) = frac(k, 2)]], [[a]]와 [[b]]는 2 이상의 자연수 }일 때,\n"
              "집합 [[sub(A,k)]]의 원소 중 최솟값을 [[sub(a,k)]]라 하자. [[sum(k, 3, 10, sub(a,k))]]의 값을\n구하시오."),
    choices=None, derived_answer="200", quick_answer="420", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2018년 6월 고2 이과 29번 변형]. a_k: 2,2,8,4,32,8,128,16 → 200(전수 확인). 빠른정답 420과 불일치.")
# ∑ p19
add(id="4eeaede4", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6)]]에서 정의된\n두 함수 [[f]]: [[X]]→[[X]], [[g]]: [[X]]→[[X]]의 치역을 각각\n[[A]], [[B]]라 할 때, 두 집합 [[A]], [[B]]가 다음 조건을 만족시킨다.\n"
              "(가) [[inter(A, B) = empty]] 이고 [[card(A) = card(B) = 3]]이다.\n(나) 두 집합 [[A]], [[B]]의 모든 원소의 합을 각각\n[[a]], [[b]]라 하면 [[a < b]]이다.\n"
              "두 집합 [[A]], [[B]]의 원소 중 가장 큰 원소를 각각\n[[m]], [[n]]이라 하자. [[m = n + 1]]일 때,\n[[sum(k, 1, 6, f(k)) + sum(k, 1, 6, g(k))]]의 최솟값을 구하시오."),
    choices=None, derived_answer="30", quick_answer="35", figure=None, difficulty_est=4, confidence=0.85,
    note="A={1,3,6}, B={2,4,5} → 13+17=30(전수 확인). 빠른정답 35와 불일치.")
# ∑ p20 (조각적 정의)
add(id="84f3ab83", qtype="short",
    question=("자연수 [[k]]에 대하여\n함수 [[f(x)]] = { [[-pow(x,2) + 16]] ([[x <= 4]]) ; [[k sqrt(x - 4)]] ([[x > 4]]) }일 때, 다음 조건을\n"
              "만족시키는 정사각형의 내부 또는 변 위에 있는\n곡선 [[y = f(x)]] 위의 점 [[point(x, y)]] 중 [[x]], [[y]]의 값이 모두\n정수인 점의 개수를 [[sub(a,n)]] ([[n]] = 1, 2, 3, ⋯)이라 하자.\n"
              "(가) 정사각형의 두 대각선의 교점의 좌표는\n[[point(n, f(n))]]이다.\n(나) 정사각형의 각 변은 [[x]]축 또는 [[y]]축에 평행하고\n한 변의 길이는 4이다.\n"
              "[[g(k) = sum(n, 1, 8, sub(a,n))]]이라 할 때, [[g(k) = 11]]을 만족시키는\n모든 [[k]]의 값의 합을 구하시오."),
    choices=None, derived_answer=None, quick_answer="3", figure=None, difficulty_est=5, confidence=0.75,
    needs_review="문법 범위 밖: 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사 (답 미도출)",
    note="빠른정답 3 미검증.")
# ∑ p79 (id 2개)
dup(["8bf84642", "7e9a554c"], qtype="choice",
    question=("곡선 [[y = pow(x,2)]] 위의 점을 [[sub(P,n)]]([[sub(x,n)]], [[pow(sub(x,n), 2)]])이라 하자.\n점 [[sub(P,1)]](0, 0)이고, 직선 [[sub(P,n) sub(P,n+1)]]의 기울기를 [[sub(a,n)]]이라 할 때,\n"
              "수열 " + SEQ + "이 다음 조건을 만족한다. (단, [[n]]은 자연수이다.)\n(가) [[sub(a,1) = 2]]\n(나) [[d > 1]]인 상수 [[d]]에 대하여\n[[sub(a,n+1) = sub(a,n) + 2d]] ([[n]] = 1, 2, 3, ⋯)이다.\n"
              "다음 보기 중 항상 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[sub(x,2) = 2]]\nㄴ. [[sub(x,26) - sub(x,25) = 2]]\n"
              "ㄷ. [[sum(k, 1, 15, sub(x,2k+1) - sub(x,2k)) <= 300]]을 만족시키는\n[[d]]의 최댓값은 10이다."),
    choices=CH_GL, derived_answer="②", quick_answer="3", figure=None, difficulty_est=4, confidence=0.85,
    note="x_{2k+1}=2kd, x_{2k}=2+2(k−1)d: ㄱ✓ ㄴ✓(x₂₆−x₂₅=2) ㄷ✗(30d−30≤300 → d≤11) → ②. 빠른정답 3과 불일치.")
# ∑ p80 (조각적 정의 + 그래프)
add(id="e865ebd9", qtype="short",
    question=("함수 [[f(x)]]는\n[[f(x)]] = { [[x]] ([[x < 0]] 또는 [[x > 4]]) ; [[-2x + 4]] ([[0 <= x < 2]]) ; [[x - 2]] ([[2 <= x <= 4]]) }\n"
              "이고, 함수 [[y = f(x)]]의 그래프는 다음 그림과 같다.\n[[x]]에 대한 방정식 ([[comp(f, f)]])([[x]]) + [[frac(1,2) f(x) = n]]의 서로\n"
              "다른 실근의 개수를 [[sub(a,n)]]이라 할 때, [[sum(n, 1, 10, sub(a,n))]]의 값을\n구하시오. (단, [[n]]은 자연수이다.)"),
    choices=None, derived_answer=None, quick_answer="98",
    figure=[{"fn": "unsupported", "args": {"raw": "y=f(x) 그래프: x<0에서 y=x(원점 열린 점), (0,4)에서 (2,0)까지 내려가는 선분, (2,0)에서 (4,2)까지 선분(닫힌 점), x>4에서 y=x(점 (4,4) 열린 점); 점선으로 y=4, y=2, x=4 표시"}}],
    difficulty_est=5, confidence=0.7,
    needs_review="문법 범위 밖: 조각적 정의(3구간) 및 (f∘f)(x) 적용 표기 / 도형(함수 그래프) 표현 불가",
    note="빠른정답 98 미검증.")
# ∑ p88
add(id="93a604a0", qtype="choice",
    question=("곡선 [[y = pow(x,2)]] 위의 점을 [[sub(P,n)]]([[sub(x,n)]], [[pow(sub(x,n), 2)]])이라 하자.\n점 [[sub(P,1)]](0, 0)이고, 직선 [[sub(P,n) sub(P,n+1)]]의 기울기를 [[sub(a,n)]]이라 할\n"
              "때, 수열 " + SEQ + "이 다음 조건을 만족시킨다.\n(단, [[n]]은 자연수이다.)\n(가) [[sub(a,1) = 3]]\n(나) [[d > 3]]인 상수 [[d]]에 대하여\n[[sub(a,n+1) = sub(a,n) + d]] ([[n]] = 1, 2, 3, ⋯)이다.\n"
              "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[sub(x,2) = 3]]\nㄴ. [[sub(x,20) = sub(x,19) + d]]\n"
              "ㄷ. [[sum(k, 1, 10, sub(x,2k+1) - sub(x,2k)) <= 100]]을 만족시키는\n[[d]]의 최댓값은 13이다."),
    choices=CH_GN, derived_answer="③", quick_answer="3", figure=None, difficulty_est=4,
    note="출처 [2017년 9월 고2 문과 21번/4점]. ㄱ✓ ㄴ✗(x₂₀=x₁₉+3) ㄷ✓(10(d−3)≤100) → ③ = 빠른정답 ✓.")
# ∑ p94
add(id="88ecfad6", qtype="short",
    question=("두 정수 [[l]], [[m]]에 대하여 두 등차수열 " + SEQ + ", [[set(sub(b,n))]]의\n일반항이\n[[sub(a,n) = 12 + (n - 1) l]],\n[[sub(b,n) = -10 + (n - 1) m]]\n일 때,\n"
              "[[sum(k, 1, 10, abs(sub(a,k) + sub(b,k))) = sum(k, 1, 10, abs(sub(a,k)) - abs(sub(b,k))) = 31]]\n을 만족시키는 모든 순서쌍 [[point(l, m)]]의 개수를 구하시오."),
    choices=None, derived_answer="7", quick_answer="3", figure=None, difficulty_est=5, confidence=0.85,
    note="출처 [2019년 11월 고2 이과 30번/4점]. 전수 탐색: (l,m)=(−11,10),…,(−5,4) 7개. 빠른정답 3과 불일치.")
# ∑ p95
add(id="6638b066", qtype="choice",
    question=("곡선 [[y = 15 pow(x,2)]] 위의 점을 [[sub(P,n)]]([[sub(x,n)]], [[15 pow(sub(x,n), 2)]])이라 하자.\n점 [[sub(P,1)]](0, 0)이고, 직선 [[sub(P,n) sub(P,n+1)]]의 기울기를 [[sub(a,n)]]이라 할 때,\n"
              "수열 " + SEQ + "이 아래 조건을 모두 만족시킨다.\n(단, [[n]]은 자연수이다.)\n(가) [[sub(a,1) = 3]]\n(나) [[d > 3]]인 정수 [[d]]에 대하여 [[sub(a,n+1) = sub(a,n) + d]]\n([[n]] = 1, 2, 3, ⋯)이다.\n"
              "다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[sub(x,2) = frac(1,5)]]\nㄴ. [[sub(x,40) = sub(x,30) + frac(d, 3)]]\n"
              "ㄷ. [[sum(k, 1, 10, sub(x,2k+1) + sub(x,2k)) <= 100]]을 만족시키는 [[d]]의\n최댓값은 14이다."),
    choices=CH_GN, derived_answer="⑤", quick_answer="4", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2017년 9월 고2 문과 21번 변형]. x_n+x_{n+1}=a_n/15: ㄱ✓ ㄴ✓(5d/15) ㄷ✓(20d/3+2≤100 → d≤14) → ⑤. 빠른정답 4와 불일치.")
# 사인법칙 p9 (도형)
add(id="700f5147", qtype="short",
    question=("그림과 같이 1보다 큰 두 실수 [[a]], [[t]]에 대하여\n직선 [[y = -x + t]]가 두 곡선 [[y = pow(a, x)]], [[y = log(a, x)]]와\n만나는 점을 각각 A, B라 하자. 점 A에서 [[x]]축에 내린\n"
              "수선의 발을 H라 할 때, 세 점 A, B, H는 다음 조건을\n만족시킨다.\n(가) [[ratio(seg(OH), seg(AB)) = ratio(1, 2)]]\n(나) 삼각형 AOB의 외접원의 반지름의 길이는\n[[frac(sqrt(2), 2)]] 이다.\n"
              "[[200(t - a)]]의 값을 구하시오. (단, O는 원점이다.)"),
    choices=None, derived_answer=None, quick_answer="frac(4,3)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 직선 y=−x+t, 곡선 y=a^x와 y=log_a x(역함수 쌍), 교점 A(위)·B(아래), A에서 x축에 내린 수선의 발 H(직각 표시)"}}],
    difficulty_est=5, confidence=0.75, needs_review="도형 표현 불가: 좌표평면 곡선·직선·수선 복합 도형",
    note="출처 [2020년 9월 고2 29번/4점]. 빠른정답 'frac(4,3)'은 200(t−a) 형태와 맞지 않음(미검증).")
# 사인법칙 p36 / p37 (도형)
_CIRC = ("그림과 같이 넓이가 {S}이고, ∠[[sub(O,1)]][[sub(O,2)]][[sub(O,3)]] = [[deg(90)]]인\n직각삼각형 [[sub(O,1)]][[sub(O,2)]][[sub(O,3)]]가 있다. 중심이 [[sub(O,1)]]인 원 [[sub(C,1)]]과\n"
         "중심이 [[sub(O,2)]]인 원 [[sub(C,2)]]가 선분 [[sub(O,1)]][[sub(O,2)]] 위의 한 점에서 만나고,\n원 [[sub(C,2)]]와 중심이 [[sub(O,3)]]인 원 [[sub(C,3)]]이 선분 [[sub(O,2)]][[sub(O,3)]] 위의 한 점에서\n"
         "만난다. 두 원 [[sub(C,1)]], [[sub(C,3)]]이 선분 [[sub(O,1)]][[sub(O,3)]] 위의 한 점 A에서\n만나고, [[sub(O,1)]]A = {L}일 때 [[sub(O,1)]]A² = [[frac(q, p)]] 이다. [[p + q]]의 값을\n"
         "구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)")
_CIRC_FIG = [{"fn": "unsupported", "args": {"raw": "큰 원 C₁(중심 O₁)과 작은 두 원 C₂(중심 O₂)·C₃(중심 O₃)이 서로 외접, 직각삼각형 O₁O₂O₃(O₂에서 직각), 점 A는 O₁O₃ 위, 선분 O₁A 길이 표시"}}]
add(id="02a189a7", qtype="short", question=_CIRC.format(S="84", L="21").replace("[[sub(O,1)]]A² = ", "[[sub(O,2)]]A² = "), choices=None, derived_answer=None, quick_answer=None,
    figure=_CIRC_FIG, difficulty_est=5, confidence=0.7,
    needs_review="도형 표현 불가: 세 원·직각삼각형 복합 도형 / 문법 범위 밖: 첨자 점 라벨(∠O₁O₂O₃, 선분 O₁A)은 텍스트 혼합",
    note="빠른정답 없음. 원문: O₁A=21, O₂A²=q/p.")
add(id="ed49d2f5", qtype="short", question=_CIRC.format(S="60", L="12").replace("[[sub(O,1)]]A² = ", "[[sub(O,2)]]A² = "), choices=None, derived_answer=None, quick_answer="890",
    figure=_CIRC_FIG, difficulty_est=5, confidence=0.7,
    needs_review="도형 표현 불가: 세 원·직각삼각형 복합 도형 / 문법 범위 밖: 첨자 점 라벨은 텍스트 혼합",
    note="빠른정답 890 미검증. 원문: O₁A=12, O₂A²=q/p.")
# 사인법칙 p54 (도형)
add(id="6acad6e5", qtype="choice",
    question=("아래 그림과 같이 한 변의 길이가 1인 정삼각형 ABC가\n있다. 선분 AB 위의 점 P, 선분 BC 위의 점 Q,\n선분 CA 위의 점 R에 대하여 세 점 P, Q, R가\n"
              "[[seg(AP) = seg(CR)]], [[seg(PQ) = seg(PR)]]를 만족시킬 때, 다음 보기 중 옳은\n것만을 있는 대로 고른 것은? (단, [[0 < seg(AP) < seg(BQ)]])\n<보기>\n"
              "ㄱ. [[2 seg(AP) + seg(BQ) = 1]]\nㄴ. 삼각형 CRQ는 직각삼각형이다.\nㄷ. 삼각형 PBQ의 외접원의 넓이가 삼각형 CRQ의\n외접원의 넓이의 4배일 때,\n[[seg(AP) = frac(sqrt(5) - 1, 6)]] 이다."),
    choices=CH_GL, derived_answer=None, quick_answer=None,
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 위), P는 AB 위, Q는 BC 위, R은 CA 위; AP=CR 표시(‖), PQ=PR 표시(○)"}}],
    difficulty_est=5, confidence=0.75, needs_review="도형 표현 불가: 정삼각형 내부 점·선분 표시 도형",
    note="출처 [2020년 11월 고2 21번 변형]. 빠른정답 없음.")
# 사인법칙 p58 (도형)
add(id="94935827", qtype="short",
    question=("좌표평면 위의 두 점 [[O(0, 0)]], [[A(2, 0)]]과 [[y]]좌표가\n양수인 서로 다른 두 점 P, Q가 다음 조건을 만족시킨다.\n"
              "(가) [[seg(AP) = seg(AQ) = 2 sqrt(15)]] 이고 [[seg(OP) > seg(OQ)]]이다.\n(나) [[cos(angle(OPA)) = cos(angle(OQA)) = frac(sqrt(15), 4)]]\n"
              "사각형 OAPQ의 넓이가 [[frac(q, p) sqrt(15)]] 일 때, [[p q]]의 값을\n구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer=None, quick_answer="22",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: O(원점), A(x축 위), P(제1사분면, A 위쪽), Q(제2사분면); 선분 OP, OQ, AP, AQ 표시"}}],
    difficulty_est=5, confidence=0.75, needs_review="도형 표현 불가: 좌표평면 사각형 도형",
    note="출처 [2023년 4월 고3 21번/4점]. 빠른정답 22 미검증.")
# 등비수열 p18
add(id="5e636a42", qtype="short",
    question=("첫째항이 정수이고 모든 항이 서로 다른 등비수열 " + SEQ + "에\n대하여 두 집합 [[A]], [[B]]는 다음과 같다.\n"
              "[[A]] = { [[pow(sub(a,k), 2)]] | [[sub(a,k)]]는 수열 " + SEQ + "의 항,\n[[k]]는 [[1 <= k <= 20]]인 자연수 }\n"
              "[[B]] = { [[pow(-1, k) sub(a,k)]] | [[sub(a,k)]]는 수열 " + SEQ + "의 항,\n[[k]]는 [[1 <= k <= 20]]인 자연수 }\n"
              "집합 [[A]]의 원소를 큰 수부터 차례로\n[[sub(alpha,1)]], [[sub(alpha,2)]], [[sub(alpha,3)]], ⋯, [[sub(alpha,20)]]이라 하고, 집합 [[B]]의 원소를\n"
              "큰 수부터 차례로 [[sub(beta,1)]], [[sub(beta,2)]], [[sub(beta,3)]], ⋯, [[sub(beta,20)]]이라 하자.\n"
              "[[frac(sub(alpha,1), sub(alpha,2)) = pow(frac(sub(beta,1), sub(beta,2)), 2)]], [[sub(beta,3) = 2]], [[frac(sub(alpha,1) - sub(alpha,3), sub(beta,1) - sub(beta,3)) = 20]]일 때,\n"
              "[[sub(alpha,1) × sub(beta,5)]]의 값을 구하시오."),
    choices=None, derived_answer="72", quick_answer="12", figure=None, difficulty_est=5, confidence=0.75,
    note="r=−1/3, a₁=−18 → α₁=324, β₅=2/9 → 72(검토 필요). 빠른정답 12와 불일치.")
# 등비수열 p39 (3×3 격자 표)
add(id="bc0c307f", qtype="choice",
    question=("아래 그림과 같이 9개의 칸으로 나누어진 정사각형의\n각 칸에 서로 다른 9개의 양수 [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,9)]]가\n한 칸에 하나씩 쓰여 있다.\n"
              "위쪽부터 [[i]] ([[i]] = 1, 2, 3)번째 가로줄에 있는 세 수는\n왼쪽부터 차례대로 공비가 [[sub(r,i)]]인 등비수열을 이루고,\n"
              "왼쪽부터 [[j]] ([[j]] = 1, 2, 3)번째 세로줄에 있는 세 수는\n위쪽부터 차례대로 공비가 [[sub(s,j)]]인 등비수열을 이룰 때,\n보기에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(a,1) sub(a,9) = sub(a,3) sub(a,7)]]이면 [[sub(r,1) sub(s,1) = sub(r,3) sub(s,3)]]이다.\n"
              "ㄴ. 세 수 [[sub(r,1)]], [[sub(r,2)]], [[sub(r,3)]]은 이 순서대로 등비수열을\n이룬다.\n"
              "ㄷ. 세 수 [[sub(a,1)]], [[sub(a,5)]], [[sub(a,9)]]가 이 순서대로 등비수열을\n이루면 [[sub(r,1) = sub(r,2) = sub(r,3)]]이다."),
    choices=CH_GD, derived_answer="⑤", quick_answer="5",
    figure=[{"fn": "table", "args": {"rows": [["[[sub(a,1)]]", "[[sub(a,2)]]", "[[sub(a,3)]]", "→ 공비 [[sub(r,1)]]"],
                                              ["[[sub(a,4)]]", "[[sub(a,5)]]", "[[sub(a,6)]]", "→ 공비 [[sub(r,2)]]"],
                                              ["[[sub(a,7)]]", "[[sub(a,8)]]", "[[sub(a,9)]]", "→ 공비 [[sub(r,3)]]"],
                                              ["↓ 공비 [[sub(s,1)]]", "↓ 공비 [[sub(s,2)]]", "↓ 공비 [[sub(s,3)]]", ""]]}}],
    difficulty_est=4, confidence=0.85,
    note="ㄱ✓ ㄴ✓(r₂²=r₁r₃) ㄷ✓ → ⑤ = 빠른정답 ✓. 격자는 table로.")
# 등비수열 p47
add(id="706d0027", qtype="short",
    question=("첫째항이 16이고 공비가 [[pow(2, frac(1,10))]] 인 등비수열 " + SEQ + "에 대하여\n[[log(sub(a,n))]]의 소수 부분을 [[sub(b,n)]]이라 하자.\n"
              "[[sub(b,1)]], [[sub(b,2)]], [[sub(b,3)]], ⋯, [[sub(b,k-1)]], [[sub(b,k)]], [[sub(b,k+1) + 1]]이 주어진 순서로\n등차수열을 이룰 때, [[k]]의 값을 구하시오.\n(단, [[log(2) = 0.301]]로 계산한다.)"),
    choices=None, derived_answer="27", quick_answer="27", figure=None, difficulty_est=4,
    note="출처 [2010년 6월 고3 이과 25번]. log a_n=1.204+0.0301(n−1): n≤27까지 소수부분 증가 → k=27 = 빠른정답 ✓.")
# 등비수열 p69 / p70
_DIV = ("자연수 [[n]]에 대하여 [[pow({b}, n)]]의 모든 양의 약수를 [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]],\n⋯, [[sub(a,k)]]라 할 때, 두 수열 [[sub(S,n)]], [[sub(T,n)]]을 각각\n"
        "[[sub(S,n) = sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,k)]],\n"
        "[[sub(T,n) = frac(1, sub(a,1)) + frac(1, sub(a,2)) + frac(1, sub(a,3))]] + ⋯ + [[frac(1, sub(a,k))]] 이라 하자.\n"
        "[[log(sub(S,m)) - log(sub(T,m)) > {v}]]을 만족시키는 자연수 [[m]]의\n최솟값을 구하시오.\n(단, [[log(2) = 0.30]], [[log(3) = 0.48]]로 계산한다.)")
add(id="c28fa8a8", qtype="short", question=_DIV.format(b="18", v="15"), choices=None, derived_answer="12", quick_answer="3", figure=None, difficulty_est=4, confidence=0.85,
    note="T_n=S_n/18^n → 1.26m>15 → m=12. 빠른정답 3과 불일치.")
add(id="7695feb4", qtype="short", question=_DIV.format(b="12", v="5"), choices=None, derived_answer="5", quick_answer="7", figure=None, difficulty_est=4, confidence=0.85,
    note="T_n=S_n/12^n → 1.08m>5 → m=5. 빠른정답 7과 불일치.")
# 등비수열 p78 / p81
_RSET = ("[[r > 1]]인 실수 [[r]]에 대하여\n전체집합 [[U]] = {{ [[pow(r, k)]] | [[k]]는 {N} 이하의 자연수 }}의\n부분집합 [[A]]가 다음 조건을 {ALL}만족시킨다.\n"
         "(가) [[subset(set(r, pow(r, {e1}), pow(r, {e2})), A)]]\n(나) 집합 [[A]]의 원소들을 작은 수부터 차례대로\n배열한 수열은 등비수열이다.\n"
         "(다) 전체집합 [[U]]의 모든 원소들의 합은\n집합 [[A]]의 모든 원소들의 합의 {T}배이다.\n실수 [[r]]의 값을 구하시오.")
add(id="71e94c53", qtype="short", question=_RSET.format(N="102", ALL="", e1="31", e2="100", T="91"), choices=None, derived_answer="9", quick_answer="7", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2017년 11월 고1 29번/4점]. 지수 공차 3 → r²+r+1=91 → r=9. 빠른정답 7과 불일치(p81의 빠른정답이 7).")
add(id="54d5497a", qtype="short", question=_RSET.format(N="100", ALL="모두 ", e1="23", e2="99", T="8"), choices=None, derived_answer="7", quick_answer="7", figure=None, difficulty_est=4,
    note="출처 [2017년 11월 고1 29번 변형]. 지수 공차 2 → r+1=8 → r=7 = 빠른정답 ✓.")
# 로그의 뜻과 성질 p88 / p89
_LOGSET = ("{PRE}[[sub(A,m)]] = {{ [[a b]] | [[log(3, a) + log(9, b)]]는 100 이하의 자연수,\n[[a]] ([[1 <= a <= m]])은 자연수, [[b = pow(3, k)]] ([[k]]는 정수) }}\n"
           "라 하자. [[card(sub(A,m)) = 203]]이 되도록 하는 {M}의\n최댓값을 구하시오.")
add(id="b0df4f63", qtype="short", question=_LOGSET.format(PRE="", M="자연수 [[m]]"), choices=None, derived_answer="242", quick_answer=None, figure=None, difficulty_est=5, confidence=0.85,
    note="a=3^i(0≤i≤I), ab=3^(2j−i): n=200+I−1(I≥1) → I=4 → 81≤m<243 → 242 (빠른정답 없음).")
add(id="de791773", qtype="short", question=_LOGSET.format(PRE="자연수 [[m]]에 대하여 집합 [[sub(A,m)]]을\n", M="[[m]]"), choices=None, derived_answer="242", quick_answer="20", figure=None, difficulty_est=5, confidence=0.85,
    note="p88과 동일 문항 → 242. 빠른정답 20과 불일치.")
