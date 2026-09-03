# -*- coding: utf-8 -*-
# esc_sonnet_h2-1_2of4 — 이미지 기준 전사 (82 항목 / 80쪽) — 이미지 80장 전부 직접 판독
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_A = ["ㄱ", "ㄴ", "ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ───────────────────────── 수학적 귀납법 ─────────────────────────
# p96 — 부등식의 증명 (빈칸)
add(id="59080860", qtype="choice",
    question=("다음은 [[n >= 2]]인 모든 자연수 [[n]]에 대하여\n"
              "[[1 + frac(1, sqrt(2)) + frac(1, sqrt(3))]] + ⋯ + [[frac(1, sqrt(n)) > 2(sqrt(n + 1) - 1)]] ⋯ ㉠\n"
              "이 성립함을 수학적 귀납법으로 증명한 것이다.\n\n"
              "(ⅰ) [[n = 2]]일 때\n"
              "(좌변) = [[1 + frac(1, sqrt(2)) = 1 + frac(sqrt(2), 2)]],\n"
              "(우변) = [[2 sqrt(3) - 2]]이므로 ㉠이 성립한다.\n"
              "(ⅱ) [[n = k]] ([[k >= 2]])일 때 ㉠이 성립한다고 가정하면\n"
              "[[1 + frac(1, sqrt(2)) + frac(1, sqrt(3))]] + ⋯ + [[frac(1, sqrt(k)) > 2(sqrt(k + 1) - 1)]] ⋯ ㉡\n"
              "㉡의 양변에 (가) 를 더하면\n"
              "[[1 + frac(1, sqrt(2)) + frac(1, sqrt(3))]] + ⋯ + [[frac(1, sqrt(k))]] + (가) > [[2(sqrt(k + 1) - 1)]] + (가) ⋯ ㉢\n"
              "㉢의 우변을 정리하면 (우변) = (나)/[[sqrt(k + 1)]] − 2\n"
              "이때 (나)/[[sqrt(k + 1)]] − 2 − [[(2 sqrt(k + 2) - 2)]] (다) 0\n"
              "따라서 [[n = k + 1]]일 때도 ㉠이 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 [[n >= 2]]인 모든 자연수 [[n]]에 대하여 주어진 부등식은 성립한다.\n\n"
              "위의 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[frac(1, sqrt(k) + 1)]], (나) [[2k + 1]], (다) <",
             "(가) [[frac(1, sqrt(k) + 1)]], (나) [[2k + 3]], (다) >",
             "(가) [[frac(1, sqrt(k + 1))]], (나) [[2k + 1]], (다) >",
             "(가) [[frac(1, sqrt(k + 1))]], (나) [[2k + 3]], (다) <",
             "(가) [[frac(1, sqrt(k + 1))]], (나) [[2k + 3]], (다) >"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="(가)=1/√(k+1), (나)=2k+3 (2(k+1)−2√(k+1)+1)/√(k+1), (다): (2k+3)²>4(k+1)(k+2) → '>' → ⑤. 빠른정답 3과 불일치. 표 형태 선지는 '(가) …, (나) …, (다) …' 문자열, 빈칸 상자·(나)/√(k+1)은 텍스트 조각.")

# p98 — 부등식의 증명 (빈칸)
add(id="7a3283ec", qtype="choice",
    question=("다음은 모든 자연수 [[n]]에 대하여\n"
              "[[sub(a,n) = sqrt(1 × 2) + sqrt(2 × 3)]] + ⋯ + [[sqrt(n(n + 1))]]\n"
              "일 때, 부등식 [[frac(n(n + 1), 2) < sub(a,n) < frac(pow(n + 1, 2), 2)]]이\n"
              "성립함을 수학적 귀납법으로 증명한 것이다.\n\n"
              "[증명]\n"
              "(ⅰ) [[n = 1]]일 때,\n"
              "[[1 < sub(a,1) = sqrt(2)]] < (가) 이므로 성립한다.\n"
              "(ⅱ) [[n = k]]일 때,\n"
              "[[frac(k(k + 1), 2) < sub(a,k) < frac(pow(k + 1, 2), 2)]]이 성립한다고\n"
              "가정하면\n"
              "[[frac(k(k + 1), 2)]] + (나) < [[sub(a, k+1)]]\n"
              "< [[frac(pow(k + 1, 2), 2)]] + (나) 이다.\n"
              "한편, (나) > [[k + 1]]이므로\n"
              "[[frac(k(k + 1), 2)]] + (나) > [[frac((k + 1)(k + 2), 2)]] 이다.\n"
              "[[k + 1 > 0]], [[k + 2 > 0]]이므로\n"
              "(나) < [[frac(2k + 3, 2)]] 이고,\n"
              "[[frac(pow(k + 1, 2), 2)]] + (나) < ((다))²/2 이다.\n"
              "그러므로 [[n = k + 1]]일 때에도 성립한다.\n"
              "(ⅰ), (ⅱ)에 의하여 모든 자연수 [[n]]에 대하여 주어진 부등식은 성립한다.\n\n"
              "(가) ~ (다)에 알맞은 것을 바르게 짝지은 것은?"),
    choices=["(가) [[2]], (나) [[sqrt(k(k + 1))]], (다) [[k + 2]]",
             "(가) [[2]], (나) [[sqrt((k + 1)(k + 2))]], (다) [[k + 2]]",
             "(가) [[2]], (나) [[sqrt((k + 1)(k + 2))]], (다) [[k + 3]]",
             "(가) [[4]], (나) [[sqrt(k(k + 1))]], (다) [[k + 2]]",
             "(가) [[4]], (나) [[sqrt((k + 1)(k + 2))]], (다) [[k + 3]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="(가)=(1+1)²/2=2, (나)=√((k+1)(k+2)), (다)=k+2 → ②. 빠른정답 5와 불일치. '1·2'는 1 × 2로, ((다))²/2는 텍스트 조각.")

# ───────────────────────── 지수함수의 뜻과 그래프 ─────────────────────────
# p9 — 지수함수의 함숫값
add(id="0805cad6", qtype="short",
    question=("함수 [[f(x) = pow(2, m x + n)]]에서 [[f(0) = frac(1, 128)]], [[f(3) = 4]]일 때,\n"
              "[[f(5)]]의 값을 구하시오. (단, [[m]], [[n]]은 상수이다.)"),
    choices=None, derived_answer="256", figure=None, difficulty_est=1, confidence=0.9,
    note="n=−7, 3m+n=2 → m=3, f(5)=2⁸=256. 빠른정답 5와 불일치.")

# p12 — 지수함수의 성질
add(id="3ba64156", qtype="choice",
    question=("함수 [[f(x) = pow(a, x)]] ([[a > 0]], [[a != 1]])에 대하여 다음 보기 중\n"
              "항상 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(-x) = -f(x)]]\n"
              "ㄴ. [[f(n x) = pow(f(x), n)]]\n"
              "ㄷ. [[f(x + y) = f(x) f(y)]]"),
    choices=["ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="ㄱ ✗(a^(−x)=1/a^x), ㄴ ✓, ㄷ ✓ → ⑤ = 빠른정답 ✓.")

# p22 — 지수함수의 그래프 (선지가 그래프)
add(id="7a62518d", qtype="choice",
    question=("함수 [[y = -pow(frac(1, a), x)]] ([[a > 0]], [[a != 1]])의 그래프가 다음 그림과\n"
              "같을 때, 함수 [[y = pow(-frac(1, 5) pow(a,2) + frac(2, 5) a + frac(2, 5), x - 1) - 3]]의\n"
              "그래프의 개형으로 알맞은 것은?"),
    choices=["[그래프] 점근선 [[y = -3]]인 증가 곡선, [[x = -frac(1,2)]] 위치 표시(수직 점선), [[x]]절편 양수",
             "[그래프] 점근선 [[y = -3]]인 증가 곡선, [[x = frac(1,2)]] 위치 표시(수직 점선), [[x]]절편 양수",
             "[그래프] 점근선 [[y = -3]]인 감소 곡선, [[x]]축 위 [[frac(1,2)]] 표시, 원점 부근을 지남",
             "[그래프] 점근선 [[y = -3]]인 감소 곡선, [[y]]축 위 [[-frac(1,2)]] 표시, [[y]]절편이 [[-frac(1,2)]]보다 위, [[x]]절편 음수",
             "[그래프] 점근선 [[y = -3]]인 감소 곡선, [[y]]축 위 [[-frac(1,2)]] 표시, [[y]]절편이 [[-frac(1,2)]]보다 아래, [[x]]절편 음수"],
    derived_answer=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=−(1/a)^x 그래프 — 왼쪽에서 x축(점근선) 아래로 붙어 있다가 오른쪽으로 급격히 감소, y절편 −1"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 문제 그림(지수함수 그래프) + 선지 5개가 모두 그래프(텍스트 설명으로 대체)",
    note="그림에서 0<a<1 → 밑 (−a²+2a+2)/5 ∈ (2/5, 3/5) 감소함수, 점근선 y=−3, y절편 1/밑−3 ∈ (−4/3, −1/2) → 판독상 ⑤로 보이나 그래프 선지 판독 불확실, 빠른정답 4. 답 미도출.")

# p30 — 지수함수의 그래프의 평행이동 (2010년 10월 고3 문과 20번)
add(id="fe1ef907", qtype="short",
    question=("그림과 같이 두 곡선 [[y = pow(2, x)]], [[y = pow(2, x - 2)]]과 직선 [[y = k]]의\n"
              "교점을 각각 [[sub(P,k)]], [[sub(Q,k)]]라 하고, 삼각형 O[[sub(P,k)]][[sub(Q,k)]]의 넓이를\n"
              "[[sub(A,k)]]라 하자.\n"
              "[[sub(A,1) + sub(A,4) + sub(A,7) + sub(A,10)]]의 값을 구하시오.\n"
              "(단, [[k]]는 자연수이고, O는 원점이다.)"),
    choices=None, derived_answer="22",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=2^x, y=2^(x−2)와 직선 y=k, 교점 P_k, Q_k, 삼각형 OP_kQ_k 음영, O 원점"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 두 지수곡선·직선·삼각형 좌표평면 그림 / 첨자 점 라벨(삼각형 OP_kQ_k) 텍스트 혼합",
    note="출처 [2010년 10월 고3 문과 20번]. P_kQ_k=2, 높이 k → A_k=k → 1+4+7+10=22. 빠른정답 2와 불일치.")

# p47 — 대소 비교 (2009년 6월 고3 문과 27번)
add(id="94bc9a34", qtype="choice",
    question=("지수함수 [[f(x) = pow(3, -x)]]에 대하여\n"
              "[[sub(a,1) = f(2)]], [[sub(a, n+1) = f(sub(a,n))]] ([[n]] = 1, 2, 3)일 때,\n"
              "[[sub(a,2)]], [[sub(a,3)]], [[sub(a,4)]]의 대소 관계를 옳게 나타낸 것은?"),
    choices=["[[sub(a,2) < sub(a,3) < sub(a,4)]]", "[[sub(a,4) < sub(a,3) < sub(a,2)]]",
             "[[sub(a,2) < sub(a,4) < sub(a,3)]]", "[[sub(a,3) < sub(a,2) < sub(a,4)]]",
             "[[sub(a,3) < sub(a,4) < sub(a,2)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 감소 곡선 y=3^(−x)와 직선 y=x, x=2에서의 함숫값 a₁을 점선으로 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프(y=3^(−x), y=x)",
    note="출처 [2009년 6월 고3 문과 27번]. a₁=1/9, a₂≈0.885, a₃≈0.378, a₄≈0.66 → a₃<a₄<a₂ → ⑤ = 빠른정답 ✓.")

# p54 — 대소 비교 보기
add(id="e4ba6c45", qtype="choice",
    question=("[[0 < a < b]]이고 [[a != 1]], [[b != 1]]일 때,\n"
              "다음 보기 중 두 함수 [[f(x) = pow(a, -x)]], [[g(x) = pow(b, -x)]]에 대하여\n"
              "옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[g(1) < 1 < f(1)]]이면 [[a < 1 < b]]이다.\n"
              "ㄴ. [[a < b < 1]]이면 [[f(a) > g(a)]]\n"
              "ㄷ. [[a b = 1]]이면 [[f(a) > g(-b)]]"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="ㄱ ✓, ㄴ ✓(a^(−a)>b^(−a)), ㄷ ✗(a^(−a)<a^(−1/a)) → ③ = 빠른정답 ✓.")

# p55 — 두 곡선의 교점 보기 (2020년 6월 고3 이과 18번 변형)
add(id="214f3d94", qtype="choice",
    question=("두 곡선 [[y = pow(3, x)]]과 [[y = -4 pow(x,2) + 4]]가 만나는 두 점을\n"
              "[[point(sub(x,1), sub(y,1))]], [[point(sub(x,2), sub(y,2))]]라 하자. [[sub(x,1) < sub(x,2)]]일 때, 다음 보기 중\n"
              "옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(x,2) < frac(1,2)]]\n"
              "ㄴ. [[sub(y,2) - sub(y,1) < 2(sub(x,2) - sub(x,1))]]\n"
              "ㄷ. [[frac(sqrt(3), 3) < sub(y,1) sub(y,2) < 1]]"),
    choices=["ㄴ", "ㄷ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 6월 고3 이과 18번 변형]. 수치 확인 x₁≈−0.955, x₂≈0.685: ㄱ ✗, ㄴ ✓(기울기≈1.08), ㄷ ✓(y₁y₂≈0.743) → ④ = 빠른정답 ✓.")

# p66 — 합성함수의 최소
add(id="9fd1c42b", qtype="short",
    question=("두 함수 [[f(x) = pow(4, x)]], [[g(x) = pow(x,2) - 6x + 7]]에 대하여\n"
              "함수 ([[comp(f, g)]])([[x]])는 [[x = a]]일 때 최솟값 [[m]]을 갖는다.\n"
              "이때 [[frac(a, m)]]의 값을 구하시오."),
    choices=None, derived_answer="48", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="합성함수 적용 표기 (f∘g)(x)를 텍스트 혼합으로 우회",
    note="g 최소 x=3, g(3)=−2 → m=4^(−2)=1/16, a/m=48 = 빠른정답 ✓.")

# ───────────────────────── 로그함수의 뜻과 그래프 ─────────────────────────
# p9 — 로그함수의 성질 (집합 보기)
add(id="ac0e9a15", qtype="choice",
    question=("두 집합\n"
              "[[A = setb(point(x, y), y = pow(2, x))]], [[B = setb(point(x, y), y = log(2, x))]]에\n"
              "대하여 [[in(point(a, b), A)]], [[in(point(c, d), B)]]일 때, 다음 보기 중 옳은\n"
              "것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[in(point(a + 1, 2b), A)]]    ㄴ. [[in(point(c + 1, 2d), B)]]\n"
              "ㄷ. [[in(point(b, a), B)]]    ㄹ. [[in(point(a + d, b c), A)]]"),
    choices=["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ", "ㄱ, ㄷ, ㄹ", "ㄱ, ㄴ, ㄹ"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄱ ✓(2^(a+1)=2b), ㄴ ✗, ㄷ ✓, ㄹ ✓(2^(a+d)=b·c) → ④. 빠른정답 '양의 실수'는 이 문항과 무관(정렬 어긋남).")

# p10 — 로그함수의 치역
add(id="aab974e3", qtype="short",
    question=("다음은 함수 [[f(x) = log(5, x)]]에 대한 설명이다. □ 안에\n알맞은 것을 쓰시오.\n"
              "치역은 □ 전체의 집합이다."),
    choices=None, derived_answer="실수", figure=None, difficulty_est=1, confidence=0.9,
    note="로그함수의 치역은 실수 전체 = 빠른정답 ✓. 빈칸 상자는 □ 텍스트.")

# p15 — 로그함수의 치역
add(id="5cb643f6", qtype="short",
    question=("다음은 함수 [[f(x) = log(4, x)]]에 대한 설명이다. □ 안에\n알맞은 것을 쓰시오.\n"
              "치역은 □ 전체의 집합이다."),
    choices=None, derived_answer="실수", figure=None, difficulty_est=1, confidence=0.9,
    note="치역은 실수 전체. 빠른정답 '양의 실수'(정의역 답)와 불일치.")

# p16 (id 3개) — 2008년 3월 고3 이과 10번
dup(["834cd73a", "4506f550", "3e150a83"], qtype="choice",
    question=("두 집합 [[A = setb(point(x, y), y = pow(3, x))]],\n"
              "[[B = setb(point(x, y), y = log(3, x))]]에 대하여 [[in(point(a, b), A)]],\n"
              "[[in(point(c, d), B)]]일 때, <보기>에서 옳은 것을 모두 고른 것은?\n<보기>\n"
              "ㄱ. [[in(point(pow(a,3), 3b), A)]]\n"
              "ㄴ. [[in(point(b, a), B)]]\n"
              "ㄷ. [[in(point(a + d, b c), A)]]"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2008년 3월 고3 이과 10번]. ㄱ ✗(3^(a³)≠3b), ㄴ ✓, ㄷ ✓ → ④. 빠른정답 '실수'는 무관(정렬 어긋남).")

# p21 — 합성함수 그래프 개형 (선지가 그래프)
add(id="21455b85", qtype="choice",
    question=("함수 [[f(x) = abs(log(3, abs(x)))]]와 함수 [[g(x) = x - 3]] ([[x != 3]])에\n"
              "대하여 함수 [[y]] = ([[comp(f, g)]])([[x]]) 의 그래프의 개형은?"),
    choices=["[그래프] 수직 점선(점근선)의 왼쪽에서만 정의된 감소 곡선, 점근선 부근에서 아래로 발산",
             "[그래프] 수직 점선의 오른쪽에서만 정의된 증가 곡선, 점근선 부근에서 아래로 발산",
             "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 아래로 발산, [[x]]절편 2개",
             "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 위로 발산, [[x]]축 위에서 두 점에 닿는 V자 모양",
             "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 아래로 발산, [[x]]축 아래에서 두 점에 닿는 ∧자 모양"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 선지 5개가 모두 그래프(텍스트 설명으로 대체) / 합성함수 적용 표기",
    note="y=|log₃|x−3||: x=3 대칭, 0 이상, x=3 부근 +∞, x=2,4에서 0 → ④ (빠른정답 없음, 풀이 답).")

# p24 — 합성함수 그래프 개형 (2013년 9월 고2 문과 18번/4점)
add(id="abe7bcf0", qtype="choice",
    question=("함수 [[f(x) = log(2, abs(x))]]와 함수 [[g(x) = x - 2]]\n"
              "([[x != 2]])에 대하여 함수 [[y]] = ([[comp(f, g)]])([[x]]) 의 그래프의\n"
              "개형은?"),
    choices=["[그래프] 수직 점선(점근선)의 왼쪽에서만 정의된 감소 곡선, 점근선 부근에서 아래로 발산",
             "[그래프] 수직 점선의 오른쪽에서만 정의된 증가 곡선, 점근선 부근에서 아래로 발산",
             "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 아래로 발산, [[x]]절편 2개, 양쪽 바깥으로 증가",
             "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 위로 발산, [[x]]축 위에서 두 점에 닿는 V자 모양",
             "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 아래로 발산, [[x]]축 아래에서 두 점에 닿는 ∧자 모양"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 선지 5개가 모두 그래프(텍스트 설명으로 대체) / 합성함수 적용 표기",
    note="출처 [2013년 9월 고2 문과 18번/4점]. y=log₂|x−2|: x=2 대칭, x=2 부근 −∞, x=1,3에서 0 → ③ (빠른정답 없음).")

# p32 — 2014년 6월 고3 이과 19번/4점
add(id="21016829", qtype="choice",
    question=("[[0 < a < 1 < b]]인 두 실수 [[a]], [[b]]에 대하여 두 함수\n"
              "[[f(x) = log(a, b x - 1)]], [[g(x) = log(b, a x - 1)]]\n"
              "이 있다. 곡선 [[y = f(x)]]와 [[x]]축의 교점이 곡선 [[y = g(x)]]의\n"
              "점근선 위에 있도록 하는 [[a]]와 [[b]] 사이의 관계식과 [[a]]의\n"
              "범위를 옳게 나타낸 것은?"),
    choices=["[[b = -2a + 2]] ([[0 < a < frac(1,2)]])", "[[b = 2a]] ([[0 < a < frac(1,2)]])",
             "[[b = 2a]] ([[frac(1,2) < a < 1]])", "[[b = 2a + 1]] ([[0 < a < frac(1,2)]])",
             "[[b = 2a + 1]] ([[frac(1,2) < a < 1]])"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2014년 6월 고3 이과 19번/4점]. f의 x절편 2/b = g의 점근선 1/a → b=2a, b>1 → 1/2<a<1 → ③ (빠른정답 없음).")

# p33 — 로그함수의 그래프 위의 점
add(id="66a0058a", qtype="short",
    question=("다음 그림과 같이 직선 [[x = a]] ([[0 < a < 1]])이\n"
              "두 곡선 [[y = log(frac(1, 25), x)]], [[y = log(5, x)]]와 만나는 점을 각각\n"
              "P, Q라 하고, 직선 [[x = b]] ([[b > 1]])이\n"
              "두 곡선 [[y = log(frac(1, 25), x)]], [[y = log(5, x)]]와 만나는 점을 각각\n"
              "R, S라 하자. 네 점 P, Q, R, S는 아래 조건을 만족한다.\n"
              "(가) [[ratio(seg(PQ), seg(SR)) = ratio(2, 1)]]\n"
              "(나) 선분 PR의 중점의 [[x]]좌표는 [[frac(14, 9)]]이다.\n"
              "이때 [[90(b - a)]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="260",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 감소 곡선 y=log_(1/25)x와 증가 곡선 y=log₅x(점 (1,0)에서 교차), 직선 x=a(왼쪽)·x=b(오른쪽), 교점 P(위)·Q(아래), S(위)·R(아래)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 두 로그곡선·직선 x=a, x=b·점 P, Q, R, S 좌표평면 그림",
    note="PQ=−(3/2)log₅a, SR=(3/2)log₅b, 2:1 → a=1/b²; a+b=28/9 → 9b³−28b²+9=0 → b=3, a=1/9 → 90(b−a)=260 = 빠른정답 ✓.")

# p42 — 2009년 11월 고3 이과 16번
add(id="839e18fe", qtype="choice",
    question=("자연수 [[n]] ([[n >= 2]])에 대하여 직선 [[y = -x + n]]과\n"
              "곡선 [[y = abs(log(2, x))]]가 만나는 서로 다른 두 점의 [[x]]좌표를\n"
              "각각 [[sub(a,n)]], [[sub(b,n)]] ([[sub(a,n) < sub(b,n)]])이라 할 때, 옳은 것만을\n"
              "<보기>에서 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(a,2) < frac(1, 4)]]\n"
              "ㄴ. [[0 < frac(sub(a, n+1), sub(a,n)) < 1]]\n"
              "ㄷ. [[1 - frac(log(2, n), n) < frac(sub(b,n), n) < 1]]"),
    choices=CH_A, derived_answer="④", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2009년 11월 고3 이과 16번]. ㄱ ✗(a₂∈(1/4,1/2)), ㄴ ✓(a_n 감소), ㄷ ✓(n−log₂n<b_n<n) → ④ (빠른정답 없음).")

# p45 — 로그값의 대소
add(id="a4326624", qtype="choice",
    question=("[[0 < a < b < 1]]일 때, 다음 중 가장 큰 값과 가장 작은 값을\n"
              "차례대로 나열한 것은?\n"
              "[[log(a, frac(b, a))]]   [[log(a, b)]]   [[log(b, a)]]   [[log(b, a b)]]"),
    choices=["[[log(b, a b)]], [[log(a, b)]]", "[[log(a, b)]], [[log(b, a b)]]",
             "[[log(b, a)]], [[log(a, frac(b, a))]]", "[[log(b, a b)]], [[log(a, frac(b, a))]]",
             "[[log(b, a)]], [[log(a, b)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="t=log_a b∈(0,1): log_a(b/a)=t−1<0, log_b a=1/t>1, log_b ab=1/t+1 최대 → ④ (빠른정답 없음). 상자 안 네 식은 공백으로 나열.")

# p46 — 로그함수 그래프와 대소
add(id="20d92c9d", qtype="choice",
    question=("다음 그림은 세 양수 [[a]], [[b]], [[c]]를 밑으로 하는 로그함수의\n그래프이다.\n"
              "[[pow(a, sub(x,1)) = pow(b, sub(x,2)) = pow(c, sub(x,3)) < 1]]일 때,\n"
              "[[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]]의 대소 관계를 옳게 나타낸 것은?"),
    choices=["[[sub(x,1) > sub(x,2) > sub(x,3)]]", "[[sub(x,2) > sub(x,1) > sub(x,3)]]",
             "[[sub(x,2) > sub(x,3) > sub(x,1)]]", "[[sub(x,3) > sub(x,1) > sub(x,2)]]",
             "[[sub(x,3) > sub(x,2) > sub(x,1)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: (1,0)을 지나는 세 로그곡선 — y=log_c x(가장 위, 증가), y=log_b x(증가, 그 아래), y=log_a x(감소)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 세 로그함수 그래프",
    note="그림에서 0<a<1, 1<c<b. 공통값 k<1: x₁=log_a k>0, x₃=log_c k<x₂=log_b k<0 → x₁>x₂>x₃ → ① (빠른정답 없음).")

# p47 — 로그 대소 보기
add(id="632bca7a", qtype="choice",
    question=("1이 아닌 두 양수 [[a]], [[b]]에 대하여 [[pow(a,2) < a < b < pow(b,2)]]일 때,\n"
              "보기에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[pow(a, a) < pow(a, pow(b,2))]]\n"
              "ㄴ. [[log(b, a) < 1]]\n"
              "ㄷ. [[log(a + 1, b + 1) × log(frac(1, a), b) > 0]]"),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="0<a<1<b. ㄱ ✗(밑 a<1, a<b²이면 a^a>a^(b²)), ㄴ ✓(음수), ㄷ ✓(양수·양수) → ⑤ (빠른정답 없음).")

# p89 — 산술·기하평균
add(id="0b8995cc", qtype="choice",
    question="[[x > 1]], [[y > 1]]일 때, [[log(x, pow(y, 16)) + log(sqrt(y), pow(x, 2))]]의 최솟값은?",
    choices=["[[4]]", "[[8]]", "[[12]]", "[[16]]", "[[20]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="16log_x y + 4log_y x ≥ 2√64 = 16 → ④. 빠른정답 20과 불일치.")

# p91 — 산술·기하평균
add(id="73ca657d", qtype="short",
    question=("[[x > 0]], [[y > 0]]일 때,\n"
              "[[log(7, 6x + 2y) + log(7, frac(6, x) + frac(1, 2y))]]의 최솟값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="(6x+2y)(6/x+1/(2y)) = 37 + 3x/y + 12y/x ≥ 49 → log₇49 = 2 = 빠른정답 ✓.")

# p98 — 2024년 9월 고2 18번/4점 (조각적 정의)
add(id="06f37ad8", qtype="choice",
    question=("함수 [[f(x)]] = { [[-pow(2, x) + 2]] ([[x < 1]]) ; [[log(2, x)]] ([[x >= 1]]) }에 대하여\n"
              "[[a - 1 <= x <= a + 1]]에서 함수 [[f(x)]]의 최댓값과 최솟값의\n"
              "차가 1이 되도록 하는 모든 실수 [[a]]의 값의 합은?"),
    choices=["[[3]]", "[[log(2, frac(32, 3))]]", "[[log(2, frac(40, 3))]]", "[[4]]", "[[log(2, frac(56, 3))]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="조각적(경우 나눔) 정의 f(x) — 텍스트 혼합으로 우회",
    note="출처 [2024년 9월 고2 18번/4점]. a≤0: 3·2^(a−1)=1 → a=1−log₂3; 0<a<2: a=1; a≥2: a=3 → 합 5−log₂3 = log₂(32/3) → ② (빠른정답 없음).")

# ───────────────────────── 수열의 귀납적 정의 ─────────────────────────
# p3 — 등차수열의 귀납적 정의
add(id="f85220f2", qtype="short",
    question=("다음과 같이 귀납적으로 정의된 등차수열 [[set(sub(a,n))]]의 공차를\n구하시오. ([[n]] = 1, 2, 3, ⋯)\n"
              "[[sub(a,1) = 15]], [[sub(a, n+1) = sub(a,n) + 7]]"),
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="공차 7 = 빠른정답 ✓.")

# p5 — 등차중항형 점화식과 합
add(id="42e03530", qtype="short",
    question=("수열 [[set(sub(a,n))]]이\n"
              "[[sub(a,1) = 3]], [[sub(a,2) = 6]], [[2 sub(a, n+1) = sub(a,n) + sub(a, n+2)]]\n"
              "([[n]] = 1, 2, 3, ⋯)\n"
              "로 정의되고 [[sum(k, 1, 20, frac(1, sub(a,k) sub(a, k+1))) = frac(q, p)]]일 때, [[p + q]]의 값을\n"
              "구하여라. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="209", figure=None, difficulty_est=2, confidence=0.9,
    note="a_n=3n, Σ1/(9k(k+1)) = (1/9)(1−1/21) = 20/189 → p+q=209. 빠른정답 5와 불일치.")

# p6 — 등차수열의 귀납적 정의
add(id="a4e739e9", qtype="short",
    question=("수열 [[set(sub(a,n))]]이\n"
              "[[pow(sub(a, n+1) + sub(a,n), 2) = 4 sub(a,n) sub(a, n+1) + 16]] ([[n]] = 1, 2, 3, ⋯)을\n"
              "만족시킨다. [[sub(a,1) = 100]]일 때, [[sub(a,30)]]을 구하시오.\n"
              "(단, [[sub(a,n) > sub(a, n+1)]])"),
    choices=None, derived_answer="-16", figure=None, difficulty_est=2, confidence=0.9,
    note="(a_(n+1)−a_n)²=16, 감소 → 공차 −4, a₃₀=100−116=−16. 빠른정답 7과 불일치.")

# p13 — 등비수열의 귀납적 정의
add(id="9295e14d", qtype="short",
    question=("다음과 같이 귀납적으로 정의된 등비수열 [[set(sub(a,n))]]의 공비를\n구하시오. (단, [[n]] = 1, 2, 3, ⋯)\n"
              "[[sub(a,1) = -6]], [[sub(a, n+1) / sub(a,n) = -9]]"),
    choices=None, derived_answer="-9", figure=None, difficulty_est=1, confidence=0.9,
    note="공비 −9 = 빠른정답 ✓. '÷'는 / 로.")

# p14
add(id="31085e11", qtype="short",
    question=("다음과 같이 귀납적으로 정의된 등비수열 [[set(sub(a,n))]]의 공비를\n구하시오. (단, [[n]] = 1, 2, 3, ⋯)\n"
              "[[sub(a,1) = frac(2, 3)]], [[frac(sub(a,n), sub(a, n+1)) = -9]]"),
    choices=None, derived_answer="frac(-1,9)", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n/a_(n+1)=−9 → 공비 −1/9 = 빠른정답 ✓.")

# p16
add(id="7b70d579", qtype="short",
    question=("다음과 같이 귀납적으로 정의된 등비수열 [[set(sub(a,n))]]의 공비를\n구하시오. (단, [[n]] = 1, 2, 3, ⋯)\n"
              "[[sub(a,1) = 1]], [[frac(sub(a, n+1), sub(a,n)) = 6]]"),
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="공비 6 = 빠른정답 ✓.")

# p17
add(id="d0c6ba05", qtype="short",
    question=("다음과 같이 귀납적으로 정의된 등비수열 [[set(sub(a,n))]]의 공비를\n구하시오. (단, [[n]] = 1, 2, 3, ⋯)\n"
              "[[sub(a,1) = 99]], [[sub(a, n+1) / sub(a,n) = 4]]"),
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="공비 4 = 빠른정답 ✓.")

# p18
add(id="544ec7bf", qtype="short",
    question=("다음과 같이 귀납적으로 정의된 등비수열 [[set(sub(a,n))]]의 공비를\n구하시오. (단, [[n]] = 1, 2, 3, ⋯)\n"
              "[[sub(a,1) = -1]], [[sub(a, n+1) = 5 sub(a,n)]]"),
    choices=None, derived_answer="5", figure=None, difficulty_est=1, confidence=0.9,
    note="공비 5 = 빠른정답 ✓.")

# p21 — 등비수열의 합
add(id="8241b367", qtype="short",
    question=("[[sub(a,1) = 3]], [[sub(a, n+1) = 2 sub(a,n)]]으로 정의된 수열 [[set(sub(a,n))]]에서\n"
              "[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,9)]]의 값을 구하시오."),
    choices=None, derived_answer="1533", figure=None, difficulty_est=1, confidence=0.9,
    note="3(2⁹−1)=1533. 빠른정답 5와 불일치(다음 쪽 p24의 빠른정답이 1533 — 정렬 어긋남).")

# p22
add(id="7e301904", qtype="short",
    question=("수열 [[set(sub(a,n))]]이\n"
              "[[sub(a,1) = frac(1, 3)]], [[sub(a, n+1) = 3 sub(a,n)]] ([[n]] = 1, 2, 3, ⋯)\n"
              "과 같이 귀납적으로 정의될 때, [[sub(a,12) = pow(3, k)]]을 만족시키는\n"
              "상수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=1, confidence=0.9,
    note="a_n=3^(n−2) → a₁₂=3¹⁰ → k=10. 빠른정답 −2와 불일치.")

# p24 — 등비중항형
add(id="702dcd97", qtype="short",
    question=("다음과 같이 정의된 수열 [[set(sub(a,n))]]에서 [[sub(a,7)]]의 값을 구하시오.\n(단, [[n]] = 1, 2, 3, ⋯)\n"
              "[[sub(a,1) = 2]], [[sub(a,2) = -6]], [[pow(sub(a, n+1), 2) = sub(a,n) sub(a, n+2)]]"),
    choices=None, derived_answer="1458", figure=None, difficulty_est=1, confidence=0.9,
    note="등비수열, 공비 −3 → a₇=2·(−3)⁶=1458. 빠른정답 1533과 불일치(정렬 어긋남).")

# p26 — a_(n+1)=a_n+f(n) 꼴
add(id="72c3b59e", qtype="short",
    question=("다음과 같이 정의된 수열 [[set(sub(a,n))]]의 제4항을 구하시오.\n(단, [[n]] = 1, 2, 3, ⋯)\n"
              "[[sub(a,1) = 1]], [[sub(a, n+1) = 4 sub(a,n) - n]]"),
    choices=None, derived_answer="37", figure=None, difficulty_est=1, confidence=0.9,
    note="a₂=3, a₃=10, a₄=37. 빠른정답 5와 불일치.")

# p28
add(id="af4a7852", qtype="choice",
    question=("[[sub(a,1) = 4]], [[sub(a, n+1) = sub(a,n) + f(n)]] ([[n]] = 1, 2, 3, ⋯)으로\n"
              "정의된 수열 [[set(sub(a,n))]]에 대하여 [[sum(k, 1, n, f(k)) = pow(n,2) - 4]]일 때,\n"
              "[[sub(a,101)]]의 값은?"),
    choices=["[[pow(100, 2)]]", "[[pow(100, 2) - 4]]", "[[pow(101, 2)]]", "[[pow(101, 2) - 4]]", "[[pow(101, 2) + 4]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="a₁₀₁ = a₁ + Σ_{k=1}^{100} f(k) = 4 + 100² − 4 = 100² → ①. 빠른정답 3과 불일치.")

# p38 — a_(n+1)=a_n·f(n) 꼴
add(id="81ebbf16", qtype="short",
    question=("[[sub(a,1) = 1]], [[sub(a, n+1) = frac(n + 3, n + 1) sub(a,n)]] ([[n]] = 1, 2, 3, ⋯)을\n"
              "만족하는 수열 [[set(sub(a,n))]]의 제 20항을 구하시오."),
    choices=None, derived_answer="77", figure=None, difficulty_est=2, confidence=0.9,
    note="a_n=(n+1)(n+2)/6 → a₂₀=21·22/6=77. 빠른정답 34와 불일치.")

# p40
add(id="02a68a69", qtype="short",
    question=("[[sub(a,1) = 1]], [[sub(a, n+1) = pow(5, n) sub(a,n)]] ([[n]] = 1, 2, 3, ⋯)으로 정의된\n"
              "수열 [[set(sub(a,n))]]에 대하여 [[log(5, sub(a,12))]]의 값을 구하시오."),
    choices=None, derived_answer="66", figure=None, difficulty_est=2, confidence=0.9,
    note="a₁₂=5^(1+2+…+11)=5⁶⁶ → 66. 빠른정답 3과 불일치.")

# p42 — 조각적 정의 c_n
add(id="3917ce0b", qtype="choice",
    question=("두 수열 [[set(sub(a,n))]], [[set(sub(b,n))]]은 첫째항이 모두 1이고\n"
              "[[sub(a, n+1) = 3 sub(a,n)]], [[sub(b, n+1) = (n + 2) sub(b,n)]] ([[n]] = 1, 2, 3, ⋯)\n"
              "과 같이 정의된다. 수열 [[set(sub(c,n))]]을\n"
              "[[sub(c,n)]] = { [[sub(a,n)]] ([[sub(a,n) < sub(b,n)]]) ; [[sub(b,n)]] ([[sub(a,n) >= sub(b,n)]]) }이라 할 때, [[sum(n, 1, 30, sub(c,n))]]의 값은?"),
    choices=["[[pow(3, 31) + 1]]", "[[pow(3, 31) - 1]]", "[[pow(3, 30) - 1]]",
             "[[frac(pow(3, 30) - 1, 2)]]", "[[frac(pow(3, 30) + 1, 2)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="조각적(경우 나눔) 정의 c_n — 텍스트 혼합으로 우회",
    note="a_n=3^(n−1), b_n=(n+1)!/2; c₁=1, c₂=3, n≥3은 a_n → 4+(3³⁰−9)/2=(3³⁰−1)/2 → ④. 빠른정답 2와 불일치.")

# p46
add(id="8c178b8b", qtype="short",
    question=("수열 [[set(sub(a,n))]]이 [[sub(a,1) = 1]],\n"
              "[[sqrt(n) sub(a, n+1) = sqrt(n + 1) sub(a,n)]] ([[n]] = 1, 2, 3, ⋯)으로 정의될\n"
              "때, [[sum(k, 1, 10, pow(frac(1, sub(a,k) sub(a, k+1)), 2))]]의 값을 구하시오."),
    choices=None, derived_answer="frac(10,11)", figure=None, difficulty_est=2, confidence=0.9,
    note="a_n=√n → Σ1/(k(k+1)) = 1−1/11 = 10/11 = 빠른정답 ✓.")

# p50 — 여러 가지 수열
add(id="8e6b683e", qtype="short",
    question=("수열 [[set(sub(a,n))]]이 귀납적으로\n"
              "[[sub(a,1) = -1]], [[sub(a, n+1) = pow(n, 2) - sub(a,n)]] ([[n]] = 1, 2, 3, ⋯)\n"
              "과 같이 정의될 때, [[sub(a,4)]]를 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="a₂=2, a₃=2, a₄=7 = 빠른정답 ✓.")

# p57 — 2015년 10월 고3 이과 15번/4점 (빈칸)
add(id="8d7dd350", qtype="choice",
    question=("수열 [[set(sub(a,n))]]은 [[sub(a,1) = 1]], [[sub(a,2) = 0]]이고,\n"
              "[[(n + 1)(n + 2) sub(a, n+2) - pow(n, 2) sub(a,n) = 0]] ([[n >= 1]])\n"
              "을 만족시킨다. 다음은 일반항 [[sub(a,n)]]을 구하는 과정의\n일부이다.\n\n"
              "[[n = 2m - 1]] ([[m]]은 자연수)일 때,\n"
              "주어진 식을 정리하면\n"
              "[[frac(sub(a, n+2), sub(a,n)) = frac(pow(n, 2), (n + 1)(n + 2))]]\n"
              "이므로\n"
              "[[frac(sub(a,3), sub(a,1)) = frac(pow(1, 2), 2 × 3)]]\n"
              "[[frac(sub(a,5), sub(a,3)) = frac(pow(3, 2), 4 × 5)]]\n"
              "⋮\n"
              "[[frac(sub(a, 2m+1), sub(a, 2m-1))]] = (가)\n"
              "이다. 좌변과 우변을 각각 곱하여 정리하면\n"
              "[[sub(a, 2m+1)]] = ([[1 × 3 × 5]] × ⋯ × [[(2m - 1)]])/([[2 × 4 × 6]] × ⋯ × [[2m]]) × (나)\n"
              "= [[frac(comb(2m, m), pow(4, m))]] × (나)\n"
              "이다.\n\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(m)]], [[g(m)]]이라\n"
              "할 때, [[f(5) × g(4)]]의 값은?"),
    choices=["[[frac(7, 110)]]", "[[frac(4, 55)]]", "[[frac(9, 110)]]", "[[frac(1, 11)]]", "[[frac(1, 10)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2015년 10월 고3 이과 15번/4점]. (가)=(2m−1)²/(2m(2m+1)), (나)=1/(2m+1); f(5)=81/110, g(4)=1/9 → 9/110 → ③ = 빠른정답 ✓. 긴 분수 곱은 텍스트 조각.")

# p63 — 같은 수가 반복되는 수열
add(id="aa03ae1b", qtype="short",
    question=("다음과 같이 정의되는 수열 [[set(sub(a,n))]]이 있다.\n"
              "[[sub(a,1) = 1]], [[sub(a,2) = 3]], [[sub(a,3) = 9]], [[sub(a, n-1) sub(a, n+1) = sub(a,n) sub(a, n+2)]] ([[n]] = 2, 3, 4, ⋯)\n"
              "이때 [[sum(k, 1, 30, sub(a,k))]]의 값을 구하시오."),
    choices=None, derived_answer="116", figure=None, difficulty_est=2, confidence=0.9,
    note="1, 3, 9, 3 반복(주기 4, 합 16) → 7·16+1+3=116. 빠른정답 5와 불일치. 연립 중괄호는 콤마 나열.")

# p64
add(id="f65525ec", qtype="short",
    question=("수열 [[set(sub(a,n))]]이 귀납적으로\n"
              "[[sub(a,1) = 3]], [[sub(a,n) sub(a, n+1) = 24]] ([[n]] = 1, 2, 3, ⋯)으로 정의될 때,\n"
              "[[sub(a,11)]]을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="3, 8 반복 → a₁₁=3. 빠른정답 5와 불일치.")

# p66 — 나머지 수열
add(id="cf4746a8", qtype="choice",
    question=("수열 [[set(sub(a,n))]]이\n"
              "[[sub(a,1) = 6]],\n"
              "[[sub(a, n+1)]] = ([[4 sub(a,n)]]을 7로 나누었을 때의 나머지)\n"
              "([[n]] = 1, 2, 3, ⋯)\n"
              "과 같이 정의될 때, [[sub(a,61) + sub(a,62) + sub(a,63)]]의 값은?"),
    choices=["[[10]]", "[[12]]", "[[14]]", "[[16]]", "[[18]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="6, 3, 5 반복(주기 3) → a₆₁+a₆₂+a₆₃=6+3+5=14 → ③ = 빠른정답 ✓.")

# p72 — 2014년 9월 고3 이과 12번/3점 (빈칸, 조각적 정의 포함)
add(id="ff5049bf", qtype="choice",
    question=("첫째항이 1인 수열 [[set(sub(a,n))]]에 대하여 [[sub(S,n) = sum(k, 1, n, sub(a,k))]]라 할 때,\n"
              "[[frac(sub(S, n+1), n + 1) = sum(k, 1, n, sub(S,k))]] ([[n >= 1]]) ⋯⋯ (∗)\n"
              "이 성립한다. 다음은 일반항 [[sub(a,n)]]을 구하는 과정이다.\n\n"
              "주어진 식 (∗)에 의하여\n"
              "[[frac(sub(S,n), n) = sum(k, 1, n - 1, sub(S,k))]] ([[n >= 2]]) ⋯⋯ ㉠\n"
              "이다. (∗)에서 ㉠을 빼서 정리하면\n"
              "[[frac(sub(S, n+1), sub(S,n))]] = (가)/[[n]] ([[n >= 2]])\n"
              "이다. ㉠으로부터 [[sub(S,2) = 2]]이고,\n"
              "[[sub(S,n) = frac(sub(S,n), sub(S, n-1)) × frac(sub(S, n-1), sub(S, n-2))]] × ⋯ × [[frac(sub(S,3), sub(S,2)) × sub(S,2)]] ([[n >= 3]])\n"
              "이므로\n"
              "[[sub(S,n) = fact(n)]] × (나) ([[n >= 3]])\n"
              "이다. 그러므로 [[sub(a,n)]]은\n"
              "[[sub(a,n)]] = { [[1]] ([[n]] = 1, 2) ; [[frac(pow(n, 2) - n + 1, 2) × fact(n - 1)]] ([[n >= 3]]) }\n"
              "이다.\n\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(n)]], [[g(n)]]\n"
              "이라 할 때, [[f(4) × g(20)]]의 값은?"),
    choices=["[[225]]", "[[250]]", "[[275]]", "[[300]]", "[[325]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    needs_review="조각적(경우 나눔) 정의 a_n — 텍스트 혼합으로 우회 / 빈칸 상자 (가)/n 텍스트 조각",
    note="출처 [2014년 9월 고3 이과 12번/3점]. S_(n+1)/S_n=(n+1)²/n → (가)=(n+1)², S_n=n!·n/2 → (나)=n/2; f(4)=25, g(20)=10 → 250 → ② = 빠른정답 ✓.")

# p74 — 2015년 9월 고3 문과 17번 변형 (빈칸)
add(id="f07e761e", qtype="choice",
    question=("모든 항이 양수인 수열 [[set(sub(a,n))]]은 [[sub(a,1) = 5]]이고\n"
              "[[pow(sub(a, n+1), n + 1)]] = ([[sub(a,1) + pow(sub(a,2), 2) + pow(sub(a,3), 3)]] + ⋯ + [[pow(sub(a,n), n)]])/([[n + 1]])\n"
              "([[n >= 1]])\n"
              "을 만족시킨다.\n"
              "다음은 일반항 [[sub(a,n)]]을 구하는 과정의 일부이다.\n\n"
              "[[sub(b,n) = pow(sub(a,n), n)]]이라 하면 [[sub(b,1) = 5]]이고 주어진 식으로부터\n"
              "[[sub(b, n+1)]] = ([[sub(b,1) + sub(b,2)]] + ⋯ + [[sub(b,n)]])/([[n + 1]]) ([[n >= 1]])이다.\n"
              "[[sub(S,n) = sum(k, 1, n, sub(b,k))]]라 하면\n"
              "[[sub(S, n+1)]] = (가) × [[sub(S,n)]]\n"
              "이다.\n"
              "[[sub(S,1) = 5]]이고,\n"
              "[[sub(S,n) = sub(S,1) × frac(sub(S,2), sub(S,1)) × frac(sub(S,3), sub(S,2))]] × ⋯ × [[frac(sub(S,n), sub(S, n-1))]] ([[n >= 2]])\n"
              "를 이용하여 [[sub(S,n)]]을 구하면\n"
              "[[sub(S,n)]] = (나) ([[n >= 1]])이다.\n"
              "⋮\n\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(n)]], [[g(n)]]이라 할 때,\n"
              "[[f(2) × g(2)]]의 값은?"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2015년 9월 고3 문과 17번 변형]. S_(n+1)=S_n+S_n/(n+1) → (가)=(n+2)/(n+1), S_n=5(n+1)/2=(나); f(2)=4/3, g(2)=15/2 → 10 → ⑤. 빠른정답 4와 불일치. 줄임표 포함 분수는 텍스트 조각.")

# p76 — a_n과 S_n의 관계
add(id="fb9a1689", qtype="short",
    question=("모든 항이 양수인 수열 [[set(sub(a,n))]]의 첫째항부터 제[[n]]항까지의\n"
              "합을 [[sub(S,n)]]이라 하면\n"
              "[[sub(S,n) = frac(1, 2)(sub(a,n) + frac(1, sub(a,n)))]] ([[n]] = 1, 2, 3, ⋯)이 성립한다.\n"
              "[[sub(a,25) = p - q sqrt(6)]]일 때, 두 자연수 [[p]], [[q]]에 대하여 [[p q]]의\n"
              "값을 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=3, confidence=0.9,
    note="S_n=√n, a_n=√n−√(n−1) → a₂₅=5−2√6 → p=5, q=2 → pq=10. 빠른정답 4와 불일치.")

# p78 — 2015년 11월 고3 이과 17번 변형 (빈칸)
add(id="15f381fb", qtype="choice",
    question=("모든 항이 양수인 수열 [[set(sub(a,n))]]은 [[sub(a,1) = 1]], [[sub(a,2) = 3]]이고,\n"
              "[[sub(S,n) = sum(k, 1, n, sub(a,k))]]라 할 때,\n"
              "[[sub(a, n+1) = frac(pow(sub(S,n), 2), sub(S, n-1)) + (4n - 1) sub(S,n)]] ([[n >= 2]])를 만족시킨다.\n"
              "다음은 일반항 [[sub(a,n)]]을 구하는 과정이다.\n\n"
              "[[sub(a, n+1) = sub(S, n+1) - sub(S,n)]]이므로 주어진 식으로부터\n"
              "[[sub(S, n+1) = frac(pow(sub(S,n), 2), sub(S, n-1)) + 4n sub(S,n)]] ([[n >= 2]])\n"
              "이다. 양변을 [[sub(S,n)]]으로 나누면\n"
              "[[frac(sub(S, n+1), sub(S,n)) = frac(sub(S,n), sub(S, n-1)) + 4n]]\n"
              "이다. [[sub(b,n) = frac(sub(S, n+1), sub(S,n))]]이라 하면 [[sub(b,1) = 4]]이고\n"
              "[[sub(b,n) = sub(b, n-1) + 4n]] ([[n >= 2]])\n"
              "이다. 수열 [[set(sub(b,n))]]의 일반항을 구하면\n"
              "[[sub(b,n)]] = (가) × [[(n + 1)]] ([[n >= 1]])\n"
              "이므로\n"
              "[[sub(S,n)]] = (가) × [[pow(fact(n - 1), 2) × pow(2, n - 2)]] ([[n >= 1]])\n"
              "이다. 따라서 [[sub(a,1) = 1]]이고, [[n >= 2]]일 때\n"
              "[[sub(a,n) = sub(S,n) - sub(S, n-1)]]\n"
              "= (나) × [[pow(fact(n - 2), 2) × pow(2, n - 2)]]\n"
              "이다.\n\n"
              "위의 (가)와 (나)에 알맞은 식을 각각 [[f(n)]], [[g(n)]]이라\n"
              "할 때, [[f(7) + g(5)]]의 값은?"),
    choices=["[[110]]", "[[125]]", "[[140]]", "[[155]]", "[[170]]"],
    derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2015년 11월 고3 이과 17번 변형]. b_n=2n(n+1) → (가)=2n; a_n=(n−1)(2n²−2n−1)·((n−2)!)²·2^(n−2) → (나)=(n−1)(2n²−2n−1); f(7)=14, g(5)=156 → 170 → ⑤. 빠른정답 1과 불일치.")

# p82 — 2017년 10월 고3 문과 29번/4점 (무게중심)
add(id="2a1e2b27", qtype="short",
    question=("자연수 [[n]]에 대하여 좌표평면 위의 점 [[sub(P,n)]]의 좌표를\n"
              "[[point(n, a n - a)]]라 하자. 두 점 [[sub(Q,n)]], [[sub(Q, n+1)]]에 대하여\n"
              "점 [[sub(P,n)]]이 삼각형 [[sub(Q,n)]][[sub(Q, n+1)]][[sub(Q, n+2)]]의 무게중심이 되도록\n"
              "점 [[sub(Q, n+2)]]를 정한다. 두 점 [[sub(Q,1)]], [[sub(Q,2)]]의 좌표가 각각\n"
              "[[point(0, 0)]], [[point(1, -1)]]이고 점 [[sub(Q,10)]]의 좌표가 [[point(9, 90)]]이다.\n"
              "점 [[sub(Q,13)]]의 좌표를 [[point(p, q)]]라 할 때, [[p + q]]의 값을\n"
              "구하시오. (단, [[a > 1]])"),
    choices=None, derived_answer="132", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="첨자 점 라벨(삼각형 Q_nQ_(n+1)Q_(n+2)) — 텍스트 혼합",
    note="출처 [2017년 10월 고3 문과 29번/4점]. Q_(n+2)=3P_n−Q_n−Q_(n+1): x_n=n−1, y₁₀=9a=90 → a=10, Q₁₃=(12, 120) → 132. 빠른정답 1과 불일치(다음 쪽 빠른정답이 132).")

# p85 — 순서쌍 규칙
add(id="2fb2b0cb", qtype="short",
    question=("자연수 [[n]]에 대하여 순서쌍 [[point(sub(x,n), sub(y,n))]]을 다음 규칙에 따라\n정한다.\n"
              "(가) [[point(sub(x,1), sub(y,1)) = point(2, 2)]]\n"
              "(나) [[n]]이 홀수이면\n"
              "[[point(sub(x, n+1), sub(y, n+1)) = point(sub(x,n), pow(sub(y,n) - 3, 2))]]이고,\n"
              "[[n]]이 짝수이면\n"
              "[[point(sub(x, n+1), sub(y, n+1)) = point(pow(sub(x,n) - 3, 2), sub(y,n))]]이다.\n"
              "순서쌍 [[point(sub(x,2022), sub(y,2022))]]에서 [[sub(x,2022) + sub(y,2022)]]의 값을\n구하시오."),
    choices=None, derived_answer="5", figure=None, difficulty_est=3, confidence=0.9,
    note="(2,2)→(2,1)→(1,1)→(1,4)→(4,4)→(4,1)→(1,1)… 주기 4; n=2022 → (4,1) → 5 (파이썬 확인). 빠른정답 132와 불일치(정렬 어긋남).")

# p93 — 실생활 (농도)
add(id="b7c4ecfc", qtype="short",
    question=("농도가 20 %인 설탕물 90 g이 들어 있는 그릇이 있다.\n"
              "이 그릇에서 설탕물 30 g을 덜어 낸 다음 농도가 10 %인\n"
              "설탕물 30 g을 다시 넣는 것을 1회 시행이라 하자. [[n]]회\n"
              "시행 후 그릇에 담긴 설탕물의 농도를 [[sub(a,n)]] %라 할 때,\n"
              "[[sub(a, n+1) = p sub(a,n) + q]] ([[n]] = 1, 2, 3, ⋯)가 성립한다. 이때\n"
              "상수 [[p]], [[q]]에 대하여 [[p + q]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="a_(n+1)=(2/3)a_n+10/3 → p+q=4. 빠른정답 680과 불일치.")

# p95 — 2004년 10월 고3 이과 이산수학 28번
add(id="53c14029", qtype="choice",
    question=("A상자에 똑같이 생긴 구슬이 [[n]]개 들어 있다. 이 구슬들을\n"
              "다음과 같은 방법으로 B상자로 옮기려고 한다.\n"
              "Ⅰ. 한 번에 한 개 또는 두 개씩만 옮길 수 있다.\n"
              "Ⅱ. 두 개씩 연속해서 옮길 수는 없다.\n"
              "이와 같은 방법으로 [[n]]개의 구슬을 옮기는 방법의 수를\n"
              "[[sub(a,n)]]이라고 할 때, 다음은 [[sub(a,n)]]의 점화 관계를 구하는\n과정이다.\n\n"
              "[[n]]이 4 이상의 자연수일 때, 처음에 한 개를\n"
              "옮긴 다음 나머지 구슬을 옮기는 경우의 수는\n(가) 이다.\n"
              "한편, 처음에 두 개를 옮긴 다음 나머지 구슬을\n"
              "옮기는 경우의 수는 (나) 이다.\n"
              "따라서 [[sub(a,n)]] = (다)\n\n"
              "이때 (가), (나), (다)에 알맞은 것을 순서대로 적은 것은?"),
    choices=["[[sub(a, n-1)]], [[sub(a, n-2)]], [[sub(a, n-1) + sub(a, n-2)]]",
             "[[sub(a, n-1)]], [[sub(a, n-2)]], [[sub(a, n-1) × sub(a, n-2)]]",
             "[[sub(a, n-1)]], [[sub(a, n-3)]], [[sub(a, n-1) + sub(a, n-3)]]",
             "[[sub(a, n-2)]], [[sub(a, n-3)]], [[sub(a, n-2) + sub(a, n-3)]]",
             "[[sub(a, n-2)]], [[sub(a, n-3)]], [[sub(a, n-2) × sub(a, n-3)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2004년 10월 고3 이과 이산수학 28번]. 두 개 옮긴 뒤엔 반드시 한 개 → a_(n−3); a_n=a_(n−1)+a_(n−3) → ③. 빠른정답 96과 불일치.")

# ───────────────────────── 상용로그 ─────────────────────────
# p2 — 약수의 상용로그 합
add(id="af159267", qtype="short",
    question=("1000의 모든 양의 약수의 개수를 [[m]]이라 하고,\n"
              "1000의 모든 양의 약수를 작은 것부터 차례대로\n"
              "[[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,m)]]이라 할 때,\n"
              "[[log(sub(a,1)) + log(sub(a,2)) + log(sub(a,3))]] + ⋯ + [[log(sub(a,m))]]의 값을 구하시오."),
    choices=None, derived_answer="24", figure=None, difficulty_est=2, confidence=0.9,
    note="1000=2³5³, m=16, 약수의 곱 1000⁸=10²⁴ → 24 = 빠른정답 ✓.")

# p8 — 2006년 11월 고2 이과 12번
add(id="ea457d0d", qtype="choice",
    question=("100의 모든 양의 약수들을 [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,9)]]라 할 때,\n"
              "[[log(10, sub(a,1)) + log(10, sub(a,2)) + log(10, sub(a,3))]] + ⋯ + [[log(10, sub(a,9))]]의 값은?"),
    choices=["[[9]]", "[[10]]", "[[11]]", "[[12]]", "[[13]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2006년 11월 고2 이과 12번]. 약수의 곱 100^(9/2)=10⁹ → 9 → ①. 빠른정답 450과 불일치. 밑 10 표기는 log(10, …)로 보존.")

# p57 — 지표·가수 조건
add(id="bdcc57a9", qtype="short",
    question=("자연수 [[n]]에 대하여\n"
              "[[log(n) = f(n) + g(n)]] ([[f(n)]]은 정수, [[0 <= g(n) < 1]])\n"
              "이라 하자. 세 자연수 [[x]], [[y]], [[z]]가 다음 조건을 모두 만족시킬\n"
              "때, [[frac(x, 70) + frac(y, 14) + z]]의 값을 구하시오.\n"
              "(가) [[f(x) = f(y) + 1 = f(z) + 2]]\n"
              "(나) [[g(x) = g(y) = g(z)]]\n"
              "(다) [[x + y + z = 14763]]"),
    choices=None, derived_answer="418", figure=None, difficulty_est=3, confidence=0.9,
    note="가수 같음 → x=100z, y=10z, 111z=14763 → z=133, x=13300, y=1330 → 190+95+133=418 = 빠른정답 ✓.")

# p59 — 로그값 조건
add(id="7cda4507", qtype="short",
    question=("자연수 [[N]] ([[1 <= N <= 300]])과 음이 아닌 두 정수 [[alpha]], [[beta]]가\n"
              "[[frac(1, 2) log(N) = alpha log(2) + beta log(5)]]를 만족할 때, 자연수 [[N]]이\n"
              "될 수 있는 모든 값의 합을 구하시오."),
    choices=None, derived_answer="466", figure=None, difficulty_est=3, confidence=0.85,
    note="N=4^α·25^β ≤ 300: 1,4,16,64,256,25,100 → 합 466. 빠른정답 714와 불일치.")

# p67 — 지진 에너지
add(id="87ae7278", qtype="choice",
    question=("지진의 에너지 [[E]]와 지진의 규모 [[M]] 사이에는 다음의\n"
              "관계식이 성립한다고 한다.\n"
              "[[log(E) = 11.8 + 1.5 M]]\n"
              "이때 규모가 8인 지진의 에너지는 규모가 6인 지진의\n"
              "에너지의 몇 배인지 구하면?"),
    choices=["[[100 sqrt(10)]]배", "[[1000]]배", "[[1000 sqrt(10)]]배", "[[10000]]배", "[[10000 sqrt(10)]]배"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="log E 차이 1.5·2=3 → 10³=1000배 → ② = 빠른정답 ✓.")

# p89 — 톱니바퀴 장치 (장식 삽화)
add(id="7ad5e04b", qtype="choice",
    question=("A축을 돌려서 발생한 동력을 체인을 통하여 B축에\n"
              "전달하는 장치가 있다. A축에는 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], [[sub(A,4)]],\n"
              "B축에는 [[sub(B,1)]], [[sub(B,2)]], [[sub(B,3)]], ⋯, [[sub(B,9)]]의 크기가 서로 다른\n"
              "톱니바퀴가 달려 있다. A축을 일정한 속력으로 돌릴 때,\n"
              "B축의 속력은 다음과 같다.\n"
              "Ⅰ. [[sub(A, i+1)]]과 [[sub(B,j)]]를 연결할 때의 속력은 [[sub(A,i)]]와 [[sub(B,j)]]를\n"
              "연결할 때의 속력보다 10 % 증가한다.\n"
              "([[i]] = 1, 2, 3, [[j]] = 1, 2, 3, ⋯, 9)\n"
              "Ⅱ. [[sub(A,i)]]와 [[sub(B, j+1)]]을 연결할 때의 속력은 [[sub(A,i)]]와 [[sub(B,j)]]를\n"
              "연결할 때의 속력보다 15 % 증가한다.\n"
              "([[i]] = 1, 2, 3, 4, [[j]] = 1, 2, 3, ⋯, 8)\n"
              "이때 B축의 속력의 최댓값은 최솟값의 몇 배인가?\n"
              "(단, [[log(1.1) = 0.04]], [[log(1.15) = 0.06]], [[log(2) = 0.30]])"),
    choices=["[[1.15]]", "[[1.2]]", "[[2]]", "[[2.3]]", "[[4]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "장식 삽화: A축·B축의 톱니바퀴들과 체인으로 연결된 장치 그림(수치 정보 없음)"}}],
    difficulty_est=3, confidence=0.85,
    note="최대/최소 = 1.1³·1.15⁸, log = 0.12+0.48 = 0.60 = 2log2 → 4배 → ⑤. 빠른정답 15와 불일치.")

# p96 — 2009년 4월 고3 문과 29번
add(id="d2f41930", qtype="choice",
    question=("어떤 농산물은 유통과정을 한 번 거칠 때마다 일정한\n"
              "비율로 가격이 인상된다. 이 농산물의 가격 형성 과정을\n"
              "조사한 결과 유통과정을 다섯 번 거친 소비자 가격은\n"
              "원산지 생산 가격의 2.24배였다. 유통과정을 한 번만\n"
              "거친다면 이때의 소비자 가격은 다섯 번 거친 소비자\n"
              "가격의 약 몇 %인가?\n"
              "(단, [[log(2.24) = 0.35]], [[log(1.17) = 0.07]]로 계산한다.)"),
    choices=["[[32]]", "[[37]]", "[[42]]", "[[47]]", "[[52]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2009년 4월 고3 문과 29번]. r⁵=2.24 → log r=0.07 → r=1.17; 1.17/2.24≈0.52 → 52 % → ⑤. 빠른정답 2와 불일치.")

# ───────────────────────── 등차수열 ─────────────────────────
# p14 — 2025년 9월 고3 18번/3점
add(id="fb9e116a", qtype="short",
    question=("등차수열 [[set(sub(a,n))]]에 대하여 [[sub(a,3) = 6]], [[2 sub(a,5) - sub(a,4) = 15]]일 때,\n"
              "[[sub(a,11)]]의 값을 구하시오."),
    choices=None, derived_answer="30", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2025년 9월 고3 18번/3점]. 2a₅−a₄=a₆=15, a₃=6 → d=3, a₁₁=30. 빠른정답 2와 불일치.")

# p46 — 등차수열의 합(1)
add(id="3cf4a0e3", qtype="short",
    question=("첫째항이 40이고 공차가 [[-2d]]인 등차수열 [[set(sub(a,n))]]에 대하여\n"
              "등식 [[sub(a,m) + sub(a, m+1) + sub(a, m+2)]] + ⋯ + [[sub(a, m+k) = 0]]을\n"
              "만족시키는 두 자연수 [[m]], [[k]]가 존재하도록 하는\n"
              "자연수 [[d]]의 개수를 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.85,
    note="합=0 ⇔ a_m+a_(m+k)=0 ⇔ d(2m+k−2)=40 → d는 40의 약수(m=1, k=40/d 가능) → 8개. 빠른정답 2와 불일치.")

# p47
add(id="4a2a770d", qtype="short",
    question=("등차수열 [[-8]], [[-4]], [[0]], ⋯, [[12]], ⋯에 대하여\n"
              "[[(-8) + (-4) + 0]] + ⋯ + [[12]]를 구하시오."),
    choices=None, derived_answer="12", figure=None, difficulty_est=1, confidence=0.9,
    note="−8, −4, 0, 4, 8, 12의 합 = 12 = 빠른정답 ✓.")

# p53 — 두 수 사이에 수를 넣은 등차수열
add(id="5476661c", qtype="short",
    question=("등차수열 [[3]], [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,n)]], [[33]]의 합이 216일\n"
              "때, 자연수 [[n]]과 공차 [[d]]에 대하여 [[n + 11d]]의 값을\n구하여라."),
    choices=None, derived_answer="40", figure=None, difficulty_est=2, confidence=0.9,
    note="(n+2)·36/2=216 → n=10, d=30/11 → n+11d=40. 빠른정답 4와 불일치.")

# p54
add(id="1a089743", qtype="short",
    question=("두 수 [[-8]]과 [[31]] 사이에 [[n]]개의 수를 넣어서 만든\n"
              "수열 [[-8]], [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,n)]], [[31]]이 이 순서대로\n"
              "등차수열을 이루고 그 합이 161일 때,\n"
              "자연수 [[n]]과 공차 [[d]]에 대하여 [[n + d]]의 값을 구하시오."),
    choices=None, derived_answer="15", figure=None, difficulty_est=2, confidence=0.9,
    note="(n+2)·23/2=161 → n=12, d=39/13=3 → n+d=15. 빠른정답 3과 불일치.")

# p55
add(id="2488f4b8", qtype="choice",
    question=("수열 [[-10]], [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,n)]], [[36]]이 등차수열을 이루고\n"
              "[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,n) = 169]]일 때, [[n]]의 값은?"),
    choices=["[[7]]", "[[9]]", "[[11]]", "[[13]]", "[[15]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="전체 합 13(n+2), 양 끝 26 빼면 13n=169 → n=13 → ④. 빠른정답 6과 불일치.")

# p56 — 수선의 발 (도형)
add(id="53ba5ea7", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]] 위에 같은 간격으로\n"
              "16개의 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,16)]]을 잡고, 각 점에서\n"
              "직선 [[m]]에 내린 수선의 발을 차례대로 [[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], ⋯,\n"
              "[[sub(Q,16)]]이라 하자. [[sub(P,1)]][[sub(Q,1)]] = 12, [[sub(P,16)]][[sub(Q,16)]] = 40일 때,\n"
              "[[sub(P,2)]][[sub(Q,2)]] + [[sub(P,3)]][[sub(Q,3)]] + [[sub(P,4)]][[sub(Q,4)]] + ⋯ + [[sub(P,15)]][[sub(Q,15)]]의 값은?"),
    choices=["[[360]]", "[[364]]", "[[368]]", "[[372]]", "[[376]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "직선 l 위의 점 P₁~P₁₆에서 직선 m에 내린 수선 P₁Q₁=12, P₁₆Q₁₆=40 (사다리꼴 모양, 직각 표시)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 두 직선과 수선의 발 그림 / 첨자 점 라벨 선분(윗줄 P₁Q₁ 등)을 텍스트 혼합으로",
    note="등차수열 12, …, 40의 가운데 14개 항의 합 = 14·26 = 364 → ②. 빠른정답 40과 불일치.")

# p57
add(id="9bb1cd32", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]] 위에 같은 간격으로\n"
              "12개의 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,12)]]를 잡고, 각 점에서\n"
              "직선 [[m]]에 내린 수선의 발을 차례대로 [[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], ⋯,\n"
              "[[sub(Q,12)]]라 하자. [[sub(P,1)]][[sub(Q,1)]] = 16, [[sub(P,12)]][[sub(Q,12)]] = 30일 때,\n"
              "[[sub(P,2)]][[sub(Q,2)]] + [[sub(P,3)]][[sub(Q,3)]] + [[sub(P,4)]][[sub(Q,4)]] + ⋯ + [[sub(P,11)]][[sub(Q,11)]]의 값은?"),
    choices=["[[210]]", "[[220]]", "[[230]]", "[[240]]", "[[250]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직선 l 위의 점 P₁~P₁₂에서 직선 m에 내린 수선 P₁Q₁=16, P₁₂Q₁₂=30 (사다리꼴 모양, 직각 표시)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 두 직선과 수선의 발 그림 / 첨자 점 라벨 선분(윗줄)을 텍스트 혼합으로",
    note="가운데 10개 항의 합 = 10·23 = 230 → ③ = 빠른정답 ✓.")

# p58
add(id="44dc6f21", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]] 위에 같은 간격으로\n"
              "12개의 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,12)]]를 잡고, 각 점에서\n"
              "직선 [[m]]에 내린 수선의 발을 차례대로 [[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], ⋯,\n"
              "[[sub(Q,12)]]라 하자. [[sub(P,1)]][[sub(Q,1)]] = 10, [[sub(P,12)]][[sub(Q,12)]] = 28일 때,\n"
              "[[sub(P,2)]][[sub(Q,2)]] + [[sub(P,3)]][[sub(Q,3)]] + [[sub(P,4)]][[sub(Q,4)]] + ⋯ + [[sub(P,11)]][[sub(Q,11)]]의 값은?"),
    choices=["[[170]]", "[[180]]", "[[190]]", "[[200]]", "[[210]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직선 l 위의 점 P₁~P₁₂에서 직선 m에 내린 수선 P₁Q₁=10, P₁₂Q₁₂=28 (사다리꼴 모양, 직각 표시)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 두 직선과 수선의 발 그림 / 첨자 점 라벨 선분(윗줄)을 텍스트 혼합으로",
    note="가운데 10개 항의 합 = 10·19 = 190 → ③. 빠른정답 4와 불일치.")

# p61 — 부분의 합 보기
add(id="c7646548", qtype="choice",
    question=("등차수열 [[set(sub(a,n))]]의 첫째항부터 제[[n]]항까지의 합을 [[sub(S,n)]]이라\n"
              "할 때, [[sub(a,1) > 0]]이고 [[sub(S,10) = sub(S,20)]]이다. 다음 보기 중 옳은\n"
              "것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(a,10) + sub(a,11) + sub(a,12)]] + ⋯ + [[sub(a,20) = 0]]\n"
              "ㄴ. [[abs(sub(a,14)) = abs(sub(a,17))]]\n"
              "ㄷ. [[n = 15]]일 때, [[sub(S,n)]]은 최댓값을 갖는다."),
    choices=CH_A, derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="a₁₁+…+a₂₀=0 → a₁₅+a₁₆=0, d<0. ㄱ ✗(a₁₀>0), ㄴ ✓(a₁₄=−3d/2, a₁₇=3d/2), ㄷ ✓ → ④ = 빠른정답 ✓.")

# p62
add(id="6bb3412a", qtype="short",
    question=("[[n]]개의 항으로 이루어진 등차수열 [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,n)]]이\n"
              "다음 조건을 만족한다.\n"
              "(가) 처음 4개 항의 합은 24이다.\n"
              "(나) 마지막 4개 항의 합은 140이다.\n"
              "(다) [[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,n) = 246]]\n"
              "[[n]]의 값을 구하시오."),
    choices=None, derived_answer="12", figure=None, difficulty_est=2, confidence=0.9,
    note="4(a₁+a_n)=164 → a₁+a_n=41, n·41/2=246 → n=12. 빠른정답 177과 불일치.")

# p70 — 합의 최대
add(id="365dfedd", qtype="short",
    question=("[[sub(a,6) = 10]], [[sub(a,15) = -8]]인 등차수열 [[set(sub(a,n))]]에서 첫째항부터\n"
              "제[[n]]항까지의 합을 [[sub(S,n)]]이라 할 때, [[sub(S,n)]]이 최대가 되는 [[n]]의\n"
              "최댓값을 구하시오."),
    choices=None, derived_answer="11", figure=None, difficulty_est=2, confidence=0.9,
    note="d=−2, a_n=22−2n, a₁₁=0 → S₁₀=S₁₁ 최대 → n 최댓값 11. 빠른정답 '- 17'과 불일치.")

# p74 — 2009년 4월 고3 문과 21번
add(id="63272f56", qtype="short",
    question=("등차수열 [[set(sub(a,n))]]에서 [[sub(a,3) = 40]], [[sub(a,8) = 30]]일 때,\n"
              "|[[sub(a,2) + sub(a,4)]] + ⋯ + [[sub(a, 2n)]]|이 최소가 되는 자연수 [[n]]의 값을\n구하시오."),
    choices=None, derived_answer="22", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2009년 4월 고3 문과 21번]. d=−2, a_(2k)=46−4k, 합 2n(22−n) → n=22에서 0. 빠른정답 3과 불일치. 절댓값 기호는 텍스트.")

# p75
add(id="f9c915af", qtype="short",
    question=("등차수열 [[set(sub(a,n))]]에서 [[sub(a,4) = 30]], [[sub(a,7) = 21]]일 때,\n"
              "|[[sub(a,1) + sub(a,3) + sub(a,5)]] + ⋯ + [[sub(a, 2n-1)]]|의 값이 최소가 되도록 하는\n"
              "자연수 [[n]]의 값을 구하시오."),
    choices=None, derived_answer="14", figure=None, difficulty_est=3, confidence=0.9,
    note="d=−3, a_(2k−1)=45−6k, 합 3n(14−n) → n=14에서 0. 빠른정답 2와 불일치.")

# p76
add(id="a78759a8", qtype="choice",
    question=("등차수열 [[set(sub(a,n))]]에서 [[sub(a,7) = 33]], [[sub(a,11) = 9]]일 때,\n"
              "|[[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,n)]]|이 최소가 되는 자연수 [[n]]의 값은?"),
    choices=["[[22]]", "[[24]]", "[[26]]", "[[28]]", "[[30]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="d=−6, a_n=75−6n, S_n=3n(24−n) → n=24에서 0 → ②. 빠른정답 '- 17'과 불일치.")

# p80 — 나머지가 같은 자연수의 합
add(id="4565d9be", qtype="choice",
    question=("6으로 나누어 5가 남고, 8로 나누어 3이 남는\n"
              "자연수를 크기 순으로 나열하여 수열 [[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,n)]]\n"
              "이라고 하자. 이때 [[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,8)]]의 값은?"),
    choices=["[[758]]", "[[759]]", "[[760]]", "[[761]]", "[[762]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="x≡11 (mod 24): 11, 35, … 8항 합 = 88+24·28 = 760 → ③. 빠른정답 5와 불일치.")

# p82
add(id="a55da10b", qtype="short",
    question=("4로 나누었을 때의 나머지가 3이고, 5로 나누었을 때의\n"
              "나머지가 3인 자연수를 작은 것부터 차례대로 나열하여\n"
              "수열 [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯이라 하자. 이때\n"
              "[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,10)]]의 값을 구하시오."),
    choices=None, derived_answer="930", figure=None, difficulty_est=2, confidence=0.9,
    note="x≡3 (mod 20): 3, 23, … 10항 합 = 30+20·45 = 930. 빠른정답 2와 불일치.")

# p83
add(id="4e149613", qtype="choice",
    question=("4로 나누면 3이 남고, 6으로 나누면 5가 남는 자연수를\n"
              "크기순으로 나열하여 [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,n)]]이라 하자. 이때\n"
              "[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,10)]]의 값은?"),
    choices=["[[620]]", "[[630]]", "[[640]]", "[[650]]", "[[660]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="x≡11 (mod 12): 11, 23, … 10항 합 = 110+12·45 = 650 → ④. 빠른정답 3과 불일치.")
