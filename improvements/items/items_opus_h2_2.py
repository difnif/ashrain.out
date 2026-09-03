# -*- coding: utf-8 -*-
# esc_opus_h2-2_1of1 — 이미지 기준 전사 (32 항목 / 30쪽, 수학II)
# 표기 관행: 도함수 적용 f′(x)는 prime(f)(x)로 씀(파서는 곱으로 해석) → needs_review 표시.
#            조각적 정의 { … (조건) ; … (조건) }는 텍스트 혼합 → needs_review 표시.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_G5 = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
PW = "문법 범위 밖: 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사"
PR = "문법 범위 밖: 도함수 적용 표기 f′(x)를 prime(f)(x)로 전사(파서는 곱으로 해석)"

# ───────────────────────── 접선의 방정식 p99 (같은 이미지에 문항 2개 — 위 문항 전사)
add(id="65460330", qtype="choice",
    question=("최고차항의 계수가 1이고 [[lim(x, 0, frac(f(x), x)) = 1]]인 사차함수 [[f(x)]]와 실수 전체의 집합에서 연속인 함수 [[g(x)]]가 "
              "모든 실수 [[x]]에 대하여 [[(g(x) - x)(g(x) - f(x)) = 0]]을 만족시킨다. 함수 [[g(x)]]가 다음 조건을 만족시킬 때, "
              "모든 [[frac(g(-2), g(3))]]의 값의 합은?\n"
              "(가) [[lim(x, 2, frac(g(x) - g(2), x - 2))]]의 값은 존재하지 않는다.\n"
              "(나) [[x >= a]]인 모든 실수 [[x]]에 대하여 [[g(-x) = -g(x)]]를 만족시키는 실수 [[a]]의 최솟값은 4이다."),
    choices=["[[-frac(41,3)]]", "[[-13]]", "[[-frac(37,3)]]", "[[-frac(35,3)]]", "[[-11]]"],
    derived_answer="⑤", figure=None, difficulty_est=5, confidence=0.75,
    needs_review="같은 이미지에 문항 2개(위: 2025년 5월 고3 15번, 아래: 2021년 사관학교 22번 변형) — 위 문항을 전사, 아래 문항은 note 참조 / 원문 중괄호 {g(x)−x}{g(x)−f(x)}는 소괄호로",
    note=("출처 [2025년 5월 고3 15번/4점]. 아래 문항(주관식): 일차함수 f에 대해 g(x)=∫₀ˣ(x−4)f(s)ds, 직선 y=tx와 곡선 y=g(x)의 교점 개수 h(t); "
          "조건 'g(k)=0인 모든 실수 k에 대하여 h(t)는 t=−k에서 불연속' → 모든 g(x)에 대한 g(6)의 합(풀이 72+(−6)=66). "
          "위 문항 풀이: 전환점 {0,2,4}→1/3, {−4,0,2}→−34/3, 합 −11 → ⑤. 빠른정답 3과 불일치."))

# ───────────────────────── 정적분 p10 (id 2개)
dup(["99c9c81f", "a6a86532"], qtype="choice",
    question=("최고차항의 계수가 1이고 [[prime(f)(2) = 0]]인 이차함수 [[f(x)]]가 모든 자연수 [[n]]에 대하여 "
              "[[dinteg(4, n, f(x), x) >= 0]]을 만족시킬 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(2) < 0]]\n"
              "ㄴ. [[dinteg(4, 3, f(x), x) > dinteg(4, 2, f(x), x)]]\n"
              "ㄷ. [[6 <= dinteg(4, 6, f(x), x) <= 14]]"),
    choices=CH_G5, derived_answer="③", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PR,
    note="출처 [2023년 10월 고3 14번/4점]. f=(x−2)²+k, −19/3≤k≤−8/3: ㄱ✓ ㄴ✗(∫₂³f=1/3+k<0) ㄷ✓(6~40/3) → ③ = 빠른정답 ✓.")

# ───────────────────────── 정적분 p21
add(id="1d851f22", qtype="short",
    question=("수열 [[set(sub(a,n))]]이 모든 자연수 [[n]]에 대하여\n"
              "[[sub(a,1) = 0]], [[n sub(a,n+1) - (n - 1) sub(a,n) = dinteg(n - 1, n, 3 pow(t,2) + 2t, t)]]일 때,\n"
              "[[sum(k, 1, 10, sub(a,k))]]의 값을 구하시오."),
    choices=None, derived_answer="330", figure=None, difficulty_est=3, confidence=0.85,
    note="우변=3n²−n → (n−1)aₙ=(n−1)²n → aₙ=n(n−1), Σ₁¹⁰=385−55=330. 빠른정답 40과 불일치.")

# ───────────────────────── 정적분 p31 (조각적 정의)
add(id="162bdd19", qtype="choice",
    question=("최고차항의 계수가 1인 삼차함수 [[f(x)]]와 상수 [[k]] ([[k >= 0]])에 대하여 "
              "함수 [[g(x)]] = { [[3x - k]] ([[x <= k]]) ; [[f(x)]] ([[x > k]]) }가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[g(x)]]는 실수 전체의 집합에서 증가하고 미분가능하다.\n"
              "(나) 모든 실수 [[x]]에 대하여\n"
              "[[dinteg(0, x, g(t)(abs(t(t - 2)) + t(t - 2)), t) >= 0]]이고\n"
              "[[dinteg(3, x, g(t)(abs((t - 2)(t + 1)) - (t - 2)(t + 1)), t) >= 0]]\n이다.\n"
              "[[g(k + 4)]]의 최솟값은?"),
    choices=["[[35]]", "[[40]]", "[[45]]", "[[50]]", "[[55]]"],
    derived_answer="②", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PW,
    note="출처 [2024년 6월 고3 15번 변형]. 조건(나)⇔g(2)=0 → k=6, f(6)=12, f′(6)=3, f′≥0 → f(10)=88+16a≥40 → ② = 빠른정답 ✓.")

# ───────────────────────── 정적분 p43 (조각적 정의)
add(id="100cec5e", qtype="short",
    question=("[[t >= 4 - 2 sqrt(2)]]인 실수 [[t]]에 대하여 실수 전체의 집합에서 정의된 함수 [[f(x)]]가 "
              "[[f(x)]] = { [[2 pow(x,2) + t x]] ([[x < 0]]) ; [[-2 pow(x,2) + t x]] ([[x >= 0]]) } 일 때, "
              "다음 조건을 만족시키는 실수 [[k]]의 최솟값을 [[g(t)]]라 하자.\n"
              "(가) 닫힌구간 [[itv(k - 1, k, cc)]]에서 함수 [[f(x)]]는 [[x = k]]에서 최댓값을 갖는다.\n"
              "(나) 닫힌구간 [[itv(k, k + 1, cc)]]에서 함수 [[f(x)]]는 [[x = k + 1]]에서 최솟값을 갖는다.\n"
              "[[6 dinteg(frac(3,2), 3, pow(4 g(t) - 2, 2), t)]]의 값을 구하시오."),
    choices=None, derived_answer="23", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PW,
    note="출처 [2020년 7월 고3 문과 30번 변형]. g(t)=(1−√(t−1))/2 (t≤2), (t−2)/4 (t≥2) → 6(3/2+7/3)=23 = 빠른정답 ✓.")

# ───────────────────────── 정적분 p50 (조각적 정의)
add(id="cc813a4c", qtype="short",
    question=("최고차항의 계수가 1인 삼차함수 [[f(x)]]에 대하여 실수 전체의 집합에서 정의된 함수 "
              "[[g(x)]] = { [[f(x)]] ([[x >= 0]]) ; [[-f(-x)]] ([[x < 0]]) }가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[g(x)]]는 실수 전체의 집합에서 연속이다.\n"
              "(나) 함수 [[abs(g(x))]]의 미분가능하지 않은 점의 개수를 [[a]]라 하고 방정식 [[abs(g(x)) = t]] ([[t]]는 실수)의 "
              "서로 다른 실근의 개수를 [[h(t)]]라 할 때, 함수 [[h(t)]]가 불연속인 점의 개수를 [[b]]라 하면 [[a + b = 4]]이다.\n"
              "(다) [[dinteg(1, 2, g(x), x) = -frac(13,4)]]\n"
              "[[f(5)]]의 값을 구하시오."),
    choices=None, derived_answer="50", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PW,
    note="f(0)=0, f=x³+px²+qx, 14p+9q=−42; a+b=4는 q=0,p<0(a=2,b=2)뿐 → f=x³−3x² → f(5)=50. 빠른정답 3과 불일치.")

# ───────────────────────── 정적분 p51 (도함수 적용)
add(id="3b618242", qtype="short",
    question=("삼차함수 [[f(x)]]가 다음 조건을 만족한다.\n"
              "(가) 모든 실수 [[x]]에 대하여 [[f(-x) = -f(x)]]이다.\n"
              "(나) [[f(alpha) = 0]], [[dinteg(0, alpha, f(x), x) = frac(81,4)]]인 양수 [[alpha]]가 존재한다.\n"
              "(다) [[x >= -2]]인 모든 실수 [[x]]에 대하여 [[f(x) <= prime(f)(x) + 18]]이고, "
              "[[f(beta) = prime(f)(beta) + 18]]인 양수 [[beta]]가 존재한다.\n"
              "[[9(pow(alpha,2) + pow(beta,2))]]의 값을 구하시오."),
    choices=None, derived_answer="162", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PR,
    note="f=−x³+9x, α=3, β=3 (h=f′+18−f=(x−3)²(x+3)) → 9·18=162 = 빠른정답 ✓.")

# ───────────────────────── 정적분 p67
add(id="8112f49f", qtype="choice",
    question=("사차함수 [[f(x) = pow(x,4) + a pow(x,2) + b]]에 대하여 [[x >= 0]]에서 정의된 함수 "
              "[[g(x) = dinteg(-x, 3x, f(t) - abs(f(t)), t)]]가 다음 조건을 모두 만족시킨다.\n"
              "(가) [[0 < x < 1]]에서 [[g(x) = sub(c,1)]] ([[sub(c,1)]]은 상수)\n"
              "(나) [[1 < x < 7]]에서 [[g(x)]]는 감소한다.\n"
              "(다) [[x > 7]]에서 [[g(x) = sub(c,2)]] ([[sub(c,2)]]는 상수)\n"
              "[[f(sqrt(5))]]의 값은? (단, [[a]], [[b]]는 상수이다)"),
    choices=["[[172]]", "[[176]]", "[[180]]", "[[184]]", "[[188]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2018년 9월 고3 문과 21번 변형]. f<0 구간이 (3,7): f=(x²−9)(x²−49) → f(√5)=25−290+441=176 → ② = 빠른정답 ✓.")

# ───────────────────────── 정적분 p76
add(id="b602863c", qtype="short",
    question=("최고차항의 계수가 1인 삼차함수 [[f(x)]]가 모든 실수 [[x]]에 대하여 [[f(-x) = -f(x)]]를 만족시킨다. "
              "이때 실수 [[m]]에 대하여 두 함수 [[F(x)]], [[g(m)]]을\n"
              "[[F(x) = dinteg(-2, x, f(t), t)]],\n"
              "[[g(m)]] = (곡선 [[y = F(x)]]와 직선 [[y = m]]의 교점의 개수)\n"
              "와 같이 정의하자. [[F(x)]]는 [[-2 < x < 2]]에서 극댓값을 갖고, 함수 [[g(m)]]은 [[m < 0]]에서 연속일 때,\n"
              "[[F(6) + g(-6)]]의 값을 구하시오."),
    choices=None, derived_answer="256", figure=None, difficulty_est=4, confidence=0.85,
    note="f=x³+bx(b<0), F의 극솟값 −(b+4)²/4≥0 → b=−4, F=x⁴/4−2x²+4 → F(6)=256, g(−6)=0 → 256. 빠른정답 3과 불일치.")

# ───────────────────────── 정적분 p77 (조각적 정의)
add(id="59cc175e", qtype="choice",
    question=("함수 [[f(x)]]가\n[[f(x)]] = { [[-pow(x,2)]] ([[x < 0]]) ; [[pow(x,2) - x]] ([[x >= 0]]) }\n"
              "이고, 양수 [[a]]에 대하여 함수 [[g(x)]]를\n"
              "[[g(x)]] = { [[a x + a]] ([[x < -1]]) ; [[0]] ([[-1 <= x < 1]]) ; [[a x - a]] ([[x >= 1]]) }\n"
              "이라 하자. 함수 [[h(x) = dinteg(0, x, g(t) - f(t), t)]]가 오직 하나의 극값을 갖도록 하는 [[a]]의 최댓값을 [[k]]라 하자.\n"
              "[[a = k]]일 때, [[k + h(3)]]의 값은?"),
    choices=["[[frac(9,2)]]", "[[frac(11,2)]]", "[[frac(13,2)]]", "[[frac(15,2)]]", "[[frac(17,2)]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PW,
    note="출처 [2025년 11월 고3 15번/4점]. h′=g−f: x<−1에서 x²+ax+a≥0 ⇔ a≤4 → k=4, h(3)=1/6+10/3=7/2 → 15/2 → ④. 빠른정답 3과 불일치.")

# ───────────────────────── 정적분 p81 (그리스 문자 함수 α(t), β(t))
add(id="73bd0fbf", qtype="choice",
    question=("[[p > 2]]인 상수 [[p]]에 대하여 함수 [[f(x) = pow(x,2) - p x]]가 있다. 실수 [[t]] ([[t > -2p]])에 대하여 "
              "함수 [[y = abs(f(x))]]의 그래프와 직선 [[y = 2x + t]]가 만나는 점의 [[x]]좌표 중 가장 작은 값을 [[alpha]]([[t]]), "
              "가장 큰 값을 [[beta]]([[t]])라 하자.\n"
              "열린구간 [[itv(-2p, inf, oo)]]에서 정의된 함수\n"
              "[[g(t)]] = ∫_{[[alpha]]([[t]])}^{[[beta]]([[t]])} { [[abs(f(x)) - (2x + t)]] } dx의 최댓값이 4일 때,\n"
              "[[p]]의 값은?"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="③", figure=None, difficulty_est=5, confidence=0.75,
    needs_review="문법 범위 밖: 그리스 문자 함수 α(t), β(t)의 적용 표기 및 이를 위끝·아래끝으로 갖는 정적분 → 텍스트 혼합 전사",
    note="출처 [2026년 5월 고3 15번 변형]. g는 t=0에서 최대: g(0)=(p³−6p²−12p−8)/6=4 → p=8 → ③ = 빠른정답 ✓.")

# ───────────────────────── 정적분 p86 (도함수 적용)
add(id="b63b8dc0", qtype="short",
    question=("두 상수 [[a]], [[b]] ([[b != 1]])과 이차함수 [[f(x)]]에 대하여 함수 [[g(x)]]가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[g(x)]]는 실수 전체의 집합에서 미분가능하고, 도함수 [[prime(g)(x)]]는 실수 전체의 집합에서 연속이다.\n"
              "(나) [[abs(x) < 2]]일 때, [[g(x) = dinteg(0, x, -t + a, t)]]이고, [[abs(x) >= 2]]일 때, [[abs(prime(g)(x)) = f(x)]]이다.\n"
              "(다) 함수 [[g(x)]]는 [[x = 1]], [[x = b]]에서 극값을 갖는다.\n"
              "[[g(k) = 0]]을 만족시키는 모든 실수 [[k]]의 값의 합이 [[p + q sqrt(3)]] 일 때, [[p q]]의 값을 구하시오. "
              "(단, [[p]]와 [[q]]는 유리수이다.)"),
    choices=None, derived_answer="32", figure=None, difficulty_est=5, confidence=0.75,
    needs_review=PR,
    note="출처 [2023년 4월 고3 22번/4점]. a=1, f=m(x−b)², b=4+2√3, 영점 0, 2, 2b−2 → 합 8+4√3 → pq=32. 빠른정답 54와 불일치(검토 필요).")

# ───────────────────────── 정적분 p87 (조각적 정의)
add(id="200a4ab8", qtype="choice",
    question=("최고차항의 계수가 1인 이차함수 [[f(x)]]에 대하여 함수 "
              "[[g(x)]] = { [[f(x + 2)]] ([[x < 0]]) ; [[dinteg(0, x, t f(t), t)]] ([[x >= 0]]) }이 실수 전체의 집합에서 미분가능하다. "
              "실수 [[a]]에 대하여 함수 [[h(x)]]를 [[h(x) = abs(g(x) - g(a))]]라 할 때, 함수 [[h(x)]]가 [[x = k]]에서 "
              "미분가능하지 않은 실수 [[k]]의 개수가 1이 되도록 하는 모든 [[a]]의 값의 곱은?"),
    choices=["[[-frac(4 sqrt(3), 3)]]", "[[-frac(7 sqrt(3), 6)]]", "[[-sqrt(3)]]", "[[-frac(5 sqrt(3), 6)]]", "[[-frac(2 sqrt(3), 3)]]"],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PW,
    note="출처 [2022년 7월 고3 15번/4점]. f=(x−2)², g(2)=4/3: a=2 또는 a=−2√3/3 → 곱 −4√3/3 → ① = 빠른정답 ✓.")

# ───────────────────────── 정적분 p88 (도함수 적용)
add(id="c20cd59e", qtype="short",
    question=("두 상수 [[a]], [[b]] ([[b != 2]])와 이차함수 [[f(x)]]에 대하여 함수 [[g(x)]]가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[g(x)]]는 실수 전체의 집합에서 미분가능하고, 도함수 [[prime(g)(x)]]는 실수 전체의 집합에서 연속이다.\n"
              "(나) [[abs(x) < 3]]일 때, [[g(x) = dinteg(1, x, -2t + a, t)]]이고, [[abs(x) >= 3]]일 때, [[abs(prime(g)(x)) = f(x)]]이다.\n"
              "(다) 함수 [[g(x)]]는 [[x = 2]], [[x = b]]에서 극값을 갖는다.\n"
              "[[g(k) = 0]]을 만족시키는 모든 실수 [[k]]의 값의 곱이 [[p + q sqrt(5)]] 일 때, [[frac(p q, 9)]]의 값을 구하시오. "
              "(단, [[p]]와 [[q]]는 유리수이다.)"),
    choices=None, derived_answer="18", figure=None, difficulty_est=5, confidence=0.75,
    needs_review=PR,
    note="출처 [2023년 4월 고3 22번 변형]. a=4, g=−(x−1)(x−3), b=3(3+√5)/2, 영점 1, 3, 2b−3=6+3√5 → 곱 18+9√5 → pq/9=18. 빠른정답 5와 불일치.")

# ───────────────────────── 평균값 정리 p45
add(id="63170ec0", qtype="short",
    question=("집합 [[S]]를\n[[S]] = { [[m]] | [[m = pow(a,2) + a b + pow(b,2) - 6(a + b)]], [[2 <= a < b <= 5]] }\n"
              "로 정의하자. 평균값 정리를 이용하여 [[m]]의 값을 구할 때, 집합 [[S]]의 원소 중에서 정수의 개수를 구하시오."),
    choices=None, derived_answer="26", figure=None, difficulty_est=3, confidence=0.8,
    note="m=(f(b)−f(a))/(b−a), f(x)=x³−6x² → m=f′(c)=3c²−12c (2<c<5) → (−12,15) → 정수 −11~14 → 26. 빠른정답 7과 불일치.")

# ───────────────────────── 함수의 극한에 대한 성질 p61 (조각적 정의)
add(id="b409afc7", qtype="short",
    question=("양수 [[m]]과 0이 아닌 실수 [[a]]에 대하여 두 함수\n"
              "[[f(x)]] = { [[pow(x,2) - (a + 1)x - pow(a,2) + 1]] ([[x <= 3m]]) ; [[-3x + 4a]] ([[x > 3m]]) },\n"
              "[[g(x)]] = { [[a x - 2a]] ([[x <= m + 4]]) ; [[2x + a]] ([[x > m + 4]]) }가 다음 조건을 모두 만족시킨다.\n"
              "(가) [[lim(x, alpha, f(x), -) != lim(x, alpha, f(x), +)]],\n"
              "[[lim(x, beta, g(x), -) != lim(x, beta, g(x), +)]]인 실수 [[alpha]], [[beta]]가 존재한다.\n"
              "(나) 모든 실수 [[k]]에 대하여 [[lim(x, k, frac(f(x), g(x)))]]의 값이 존재한다.\n"
              "[[m + g(pow(a,2))]]의 값을 구하시오."),
    choices=None, derived_answer="17", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PW,
    note="출처 [2022년 9월 고2 29번 변형]. 3m=m+4 → m=2; g(2)=0 → f(2)=0 → a=1 또는 −3, x=6 극한 일치 → a=−3 → 2+g(9)=17 = 빠른정답 ✓.")

# ───────────────────────── 함수의 연속 p35 (도형)
add(id="41df3464", qtype="short",
    question=("그림과 같이 [[seg(AB) = 4]], [[seg(BC) = 3]], [[angle(B) = deg(90)]]인 삼각형 ABC의 변 AB 위를 움직이는 점 P를 "
              "중심으로 하고 반지름의 길이가 2인 원 [[O]]가 있다. [[seg(AP) = x]] ([[0 < x < 4]])라 할 때, 원 [[O]]가 삼각형 ABC와 "
              "만나는 서로 다른 점의 개수를 [[f(x)]]라 하자.\n"
              "함수 [[f(x)]]가 [[x = a]]에서 불연속이 되는 모든 실수 [[a]]의 값의 합은 [[frac(q, p)]]이다. [[p + q]]의 값을 구하시오.\n"
              "(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="19", figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(∠B=90°, AB 가로, C가 B 위)와 변 AB 위의 점 P(A 근처)를 중심으로 하는 원 O — 원이 변 AB·AC와 만나는 모습"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 직각삼각형과 원 복합 도형",
    note="출처 [2017년 4월 고3 문과 29번/4점]. 불연속점 x=2(원이 A, B 통과), x=10/3(AC 접함) → 합 16/3 → 19. 빠른정답 5와 불일치.")

# ───────────────────────── 함수의 연속 p36
add(id="23c29b2b", qtype="short",
    question=("이차함수 [[f(x) = pow(x,2) + x]]에 대하여 함수 [[g(x)]]가 다음 조건을 만족한다.\n"
              "(가) [[0 <= x < 1]]일 때, [[g(x) = f(x)]]이다.\n"
              "(나) [[2n - 1 <= x < 2n + 1]]일 때, [[g(x) = f(x - 2n) + 2n]]이다. (단, [[n]]은 자연수이다.)\n"
              "(다) 모든 실수 [[x]]에 대하여 [[g(-x) = g(x)]]이다.\n"
              "실수 [[t]]에 대하여 함수 [[y = g(x)]]의 그래프와 함수 [[y = 2 abs(x) - t]]의 그래프가 만나는 점의 개수를 [[h(t)]]라 하자. "
              "함수 [[h(t)]]가 [[t = alpha]]에서 불연속인 [[alpha]]의 값을 작은 수부터 크기순으로 나열한 것을 "
              "[[sub(alpha,1)]], [[sub(alpha,2)]], [[sub(alpha,3)]], ⋯라 할 때, [[4 sub(alpha,20)]]의 값을 구하시오."),
    choices=None, derived_answer="73", figure=None, difficulty_est=5, confidence=0.75,
    note="ψ(x)=2x−g(x)(x≥0)의 극값: 극소 2n, 극대 2n+1/4 → 불연속점 0, 1/4, 2, 9/4, … → α₂₀=18+1/4 → 73. 빠른정답 3과 불일치.")

# ───────────────────────── 함수의 연속 p54 (조각적 정의)
add(id="3bf30426", qtype="short",
    question=("두 자연수 [[a]], [[b]] ([[a < b < 8]])에 대하여 함수 [[f(x)]]는\n"
              "[[f(x)]] = { [[abs(x + 3) - 1]] ([[x < a]]) ; [[x - 10]] ([[a <= x < b]]) ; [[abs(x - 9) - 1]] ([[x >= b]]) }이다. "
              "함수 [[f(x)]]와 양수 [[k]]는 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[f(x) f(x + k)]]는 실수 전체의 집합에서 연속이다.\n"
              "(나) [[f(k) < 0]]\n"
              "[[f(a) × f(b) × f(k)]]의 값을 구하시오."),
    choices=None, derived_answer="96", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PW,
    note="출처 [2024년 7월 고3 22번/4점]. (a,b,k)=(2,4,6)은 f(6)>0 탈락, (2,6,4) → (−8)(2)(−6)=96. 빠른정답 1과 불일치.")

# ───────────────────────── 함수의 연속 p73 (조각적 정의)
add(id="231a3625", qtype="short",
    question=("두 양수 [[a]], [[b]]와 최고차항의 계수가 1인 이차함수 [[f(x)]]에 대하여 집합 { [[x]] | [[x != -a]], [[x]]는 실수 }에서 정의된 함수 "
              "[[g(x)]]를 [[g(x)]] = { [[frac(b x, x + a)]] ([[x < -a]], [[-a < x < 1]]) ; [[f(x)]] ([[x >= 1]]) } 이라 할 때, "
              "함수 [[g(x)]]는 [[x = 1]]에서 연속이다. 실수 [[t]]에 대하여 함수 [[y = abs(g(x))]]의 그래프와 직선 [[y = t]]가 만나는 점의 "
              "개수를 [[h(t)]]라 할 때, 함수 [[h(t)]]가 다음 조건을 만족시킨다.\n"
              "(가) 임의의 두 양수 [[sub(t,1)]], [[sub(t,2)]]에 대하여 [[sub(t,1) < sub(t,2)]]이면 [[h(sub(t,1)) >= h(sub(t,2))]]이다.\n"
              "(나) 함수 [[h(t)]]는 [[t = 0]], [[t = alpha]], [[t = beta]] ([[0 < alpha < beta]])에서만 불연속이며 "
              "[[h(0) = alpha]], [[h(alpha) = beta - 1]]이다.\n"
              "[[f(a - b)]]의 값을 구하시오."),
    choices=None, derived_answer="75", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PW,
    note="출처 [2024년 10월 고2 30번/4점]. α=h(0)=3=f(1)=b/(1+a), h(3)=5=b−1 → b=6, a=1, 봉우리 높이 b → f=x²−8x+10 → f(−5)=75 = 빠른정답 ✓.")

# ───────────────────────── 함수의 연속 p74 (조각적 정의)
add(id="c2d3ee37", qtype="short",
    question=("두 양수 [[a]], [[b]]와 최고차항의 계수가 1인 이차함수 [[f(x)]]에 대하여 집합 { [[x]] | [[x != -a]], [[x]]는 실수 }에서 정의된 함수 [[g(x)]]를\n"
              "[[g(x)]] = { [[-frac(1, x + a) + b]] ([[x < -a]], [[-a < x < 1]]) ; [[f(x)]] ([[x >= 1]]) } 이라 할 때, "
              "함수 [[g(x)]]는 [[x = 1]]에서 연속이다. 실수 [[t]]에 대하여 함수 [[y = abs(g(x))]]의 그래프와 직선 [[y = t]]가 만나는 점의 "
              "개수를 [[h(t)]]라 할 때, 함수 [[h(t)]]가 다음 조건을 만족시킨다.\n"
              "(가) 임의의 두 양수 [[sub(t,1)]], [[sub(t,2)]]에 대하여 [[sub(t,1) < sub(t,2)]]이면 [[h(sub(t,1)) >= h(sub(t,2))]]이다.\n"
              "(나) 함수 [[h(t)]]는 [[t = alpha]], [[t = beta]], [[t = gamma]] ([[alpha < beta < gamma]])에서만 불연속이며\n"
              "[[h(alpha) = beta]], [[h(beta) = 2b - 2]]이다.\n"
              "[[f(x)]]의 최솟값을 [[m]]이라 할 때 [[-4m]]의 값을 구하시오."),
    choices=None, derived_answer="14", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PW,
    note="출처 [2024년 10월 고2 30번 변형]. α=0, β=h(0)=3=f(1), h(3)=5=2b−2 → b=7/2, a=1, 봉우리 높이 b → m=−7/2 → 14 = 빠른정답 ✓.")

# ───────────────────────── 함수의 연속 p80 (조각적 정의)
add(id="8e03889a", qtype="short",
    question=("두 실수 [[a]], [[b]]에 대하여 정의역이 [[setb(x, x >= 0)]]인 함수\n"
              "[[f(x) = frac(-a x - b + 1, a x + b)]] ([[a b > 0]])\n"
              "이 있다. 실수 [[k]]에 대하여 정의역이 [[setb(x, x >= 0)]]인 함수\n"
              "[[g(x)]] = { [[2k - f(x)]] ([[f(x) < k]]) ; [[f(x)]] ([[f(x) >= k]]) }\n"
              "가 다음 조건을 만족시킨다.\n"
              "(가) [[lim(x, inf, abs(g(x))) = frac(1,2)]]\n"
              "(나) [[abs(g(0)) = 1]]\n"
              "(다) 함수 [[y = abs(g(x))]]의 그래프와 직선 [[y = -k]]는 두 점 [[point(frac(1,28), -k)]], [[point(alpha, -k)]]에서만 만난다. "
              "(단, [[alpha > frac(1,28)]])\n"
              "직선 [[y = m(x - 4 alpha) + frac(3,4)]]이 함수 [[y = abs(g(x))]]의 그래프와 만나는 서로 다른 점의 개수를 [[h(m)]]이라 할 때, "
              "함수 [[h(m)]]이 불연속이 되는 모든 실수 [[m]]의 값의 합은 [[M]]이다. [[252 M]]의 값을 구하시오."),
    choices=None, derived_answer="19", figure=None, difficulty_est=5, confidence=0.75,
    needs_review=PW,
    note="출처 [2018년 4월 고3 문과 30번/4점]. k=−3/4, a=2, b=1/2, α=7/4; 불연속 m=−1/28, 0, 1/9 → M=19/252 → 19 = 빠른정답 ✓.")

# ───────────────────────── 부정적분 p62 (조각적 정의)
add(id="11556edd", qtype="short",
    question=("최고차항의 계수가 1이고 [[x = 3]]에서 극댓값 8을 갖는 삼차함수 [[f(x)]]가 있다. 실수 [[t]]에 대하여 함수 [[g(x)]]를\n"
              "[[g(x)]] = { [[f(x)]] ([[x >= t]]) ; [[-f(x) + 2f(t)]] ([[x < t]]) }라 할 때,\n"
              "방정식 [[g(x) = 0]]의 서로 다른 실근의 개수를 [[h(t)]]라 하자. 함수 [[h(t)]]가 [[t = a]]에서 불연속인 [[a]]의 값이 "
              "두 개일 때, [[f(8)]]의 값을 구하시오."),
    choices=None, derived_answer="58", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PW,
    note="출처 [2022년 9월 고3 22번/4점]. f=(x−3)²(x−6)+8 → f(8)=58 = 빠른정답 ✓(기출 정답 기준).")

# ───────────────────────── 속도와 거리 p93 (id 2개, 그래프 도형)
dup(["21bc3d90", "effa8d43"], qtype="choice",
    question=("원점을 출발하여 수직선 위를 움직이는 두 점 A, B가 있다. 다음 그림은 시각 [[t]] ([[0 <= t <= 20]])에서의 점 A의 속도 "
              "[[f(t)]]의 그래프와 점 B의 속도 [[g(t)]]의 그래프를 나타낸 것이다.\n"
              "[[dinteg(0, 3, abs(f(t)), t) = dinteg(3, 5, abs(f(t)), t)]]이고 시각 [[t = 20]]에서 두 점 A, B는 같은 위치에 있을 때, "
              "다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[dinteg(5, 20, f(t), t) = dinteg(0, 20, g(t), t)]]\n"
              "ㄴ. [[5 < t < 15]]에서 두 점 A, B는 만나지 않는다.\n"
              "ㄷ. [[t = 15]]일 때, 두 점 A, B 사이의 거리가 최대이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄷ"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "속도 그래프(0≤t≤20): y=f(t)는 (0,3)에서 음, t=3에서 0, 이후 큰 봉우리 뒤 t=20에서 0; y=g(t)는 0 이상, t=5와 t=15(점선)에서 f와 만남, 두 작은 봉우리, t=20에서 0"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 두 속도 함수의 그래프(좌표평면)",
    note="ㄱ✓(∫₀⁵f=0), ㄴ✗(t=5에서 B가 앞, t=15에서 A가 앞 → 사이에서 만남), ㄷ✓(그래프상 (5,15) 면적 차가 큼) → ⑤. 빠른정답 4와 불일치.")

# ───────────────────────── 함수의 그래프 p36 (도함수 적용)
add(id="56242511", qtype="short",
    question=("정수 [[a]] ([[a != 0]])에 대하여 함수 [[f(x)]]를 [[f(x) = pow(x,3) - 2a pow(x,2)]]이라 하자. 다음 조건을 만족시키는 "
              "모든 정수 [[k]]의 값의 곱이 [[-12]]가 되도록 하는 [[a]]에 대하여 [[prime(f)(10)]]의 값을 구하시오.\n"
              "함수 [[f(x)]]에 대하여\n"
              "[[frac(f(sub(x,1)) - f(sub(x,2)), sub(x,1) - sub(x,2)) × frac(f(sub(x,2)) - f(sub(x,3)), sub(x,2) - sub(x,3)) < 0]]을\n"
              "만족시키는 세 실수 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]]이 열린구간 [[itv(k, k + frac(3,2), oo)]]에 존재한다."),
    choices=None, derived_answer="380", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PR,
    note="출처 [2023년 6월 고3 22번/4점]. 조건⇔(k, k+3/2)에 극점 0 또는 4a/3 포함: k∈{−1,−3,−4} → a=−2 → f′(10)=300+80=380. 빠른정답 2와 불일치.")

# ───────────────────────── 함수의 그래프 p44 (조각적 정의)
add(id="fb559b75", qtype="short",
    question=("함수 [[f(x)]] = { [[(3 - a) pow(x,3)]] ([[x >= 0]]) ; [[0]] ([[x < 0]]) }에 대하여 "
              "함수 [[g(x)]]를 [[g(x) = pow(abs(x), 4) - pow(abs(x), 3) + f(x)]]로 정의하자. "
              "함수 [[g(x)]]가 극댓값을 갖도록 하는 정수 [[a]]의 최솟값을 [[sub(a,1)]]이라 하고, [[a = sub(a,1)]]일 때 함수 [[g(x)]]가 "
              "극솟값을 갖는 모든 [[x]]의 값의 합을 [[m]]이라 하자. [[sub(a,1) + 4m]]의 값을 구하시오. (단, [[a != 3]])"),
    choices=None, derived_answer="7", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PW,
    note="x=0에서 극대 ⇔ a>2, a≠3 → a₁=4; 극소 x=−3/4, 3/2 → m=3/4 → 4+3=7. 빠른정답 2와 불일치.")

# ───────────────────────── 함수의 그래프 p64 (조각적 정의 + 도함수 적용)
add(id="b9efa8cb", qtype="short",
    question=("이차함수 [[f(x)]]는 [[x = -1]]에서 극대이고, 삼차함수 [[g(x)]]는 이차항의 계수가 0이다.\n"
              "함수 [[h(x)]] = { [[f(x)]] ([[x <= 0]]) ; [[g(x)]] ([[x > 0]]) } 가 실수 전체의 집합에서 미분가능하고, 다음 조건을 만족시킬 때,\n"
              "[[prime(h)(-3) + prime(h)(4)]]의 값을 구하시오.\n"
              "(가) 방정식 [[h(x) = h(0)]]의 모든 실근의 합은 1이다.\n"
              "(나) 닫힌구간 [[itv(-2, 3, cc)]]에서 함수 [[h(x)]]의 최댓값과 최솟값의 차는 [[3 + 4 sqrt(3)]]이다."),
    choices=None, derived_answer="38", figure=None, difficulty_est=5, confidence=0.75,
    needs_review=PW + " / " + PR,
    note="출처 [2020년 6월 고3 문과 30번/4점]. f=−p(x+1)²+q, g=(2p/9)x³−2px+c, 근 합 1 → √(2p/a)=3; 차 p(1+4√3/3)=3+4√3 → p=3 → 12+26=38. 빠른정답 2와 불일치.")

# ───────────────────────── 넓이 p21
add(id="007c7e71", qtype="short",
    question=("세 집합 [[A]], [[B]], [[C]]는\n"
              "[[A = setb(point(2 + 2 cos(theta), 2 + 2 sin(theta)), -frac(pi,3) <= theta <= frac(pi,3))]],\n"
              "[[B = setb(point(-2 + 2 cos(theta), 2 + 2 sin(theta)), frac(2,3) pi <= theta <= frac(4,3) pi)]]\n"
              "[[C]] = { [[point(a, b)]] | [[-3 <= a <= 3]], [[b = pm(2, sqrt(3))]] }이다.\n"
              "좌표평면에서 집합 [[union(union(A, B), C)]]의 모든 원소가 나타내는 도형을 [[X]]라 하고, 도형 [[X]]와 곡선 "
              "[[y = -sqrt(3) pow(x,2) + 2]]가 만나는 점의 [[y]]좌표를 [[c]]라 하자. 집합 [[X]]로 둘러싸인 부분의 넓이를 [[alpha]], "
              "곡선 [[y = -sqrt(3) pow(x,2) + 2]]와 직선 [[y = c]]로 둘러싸인 부분의 넓이를 [[beta]]라 하자.\n"
              "[[alpha - beta = frac(p pi + q sqrt(3), 3)]] 일 때, [[p + q]]의 값을 구하시오.\n"
              "(단, [[p]]와 [[q]]는 정수이다.)"),
    choices=None, derived_answer="34", figure=None, difficulty_est=4, confidence=0.8,
    note="출처 [2022년 경찰대 25번/5점]. c=2−√3, α=12√3+2(4π/3−√3)=10√3+8π/3, β=4√3/3 → (8π+26√3)/3 → 34. 빠른정답 3과 불일치.")

# ───────────────────────── 넓이 p22
add(id="e94a7785", qtype="short",
    question=("세 집합 [[A]], [[B]], [[C]]는\n"
              "[[A = setb(point(2 + 2 cos(theta), 2 + 2 sin(theta)), -frac(pi,3) <= theta <= frac(pi,3))]],\n"
              "[[B = setb(point(-2 + 2 cos(theta), 2 + 2 sin(theta)), frac(2 pi, 3) <= theta <= frac(4 pi, 3))]],\n"
              "[[C]] = { [[point(a, b)]] | [[-3 <= a <= 3]], [[b = pm(2, sqrt(3))]] }이다.\n"
              "좌표평면에서 집합 [[union(union(A, B), C)]]의 모든 원소가 나타내는 도형을 [[X]]라 하고, 도형 [[X]]와 곡선 "
              "[[y = -frac(sqrt(3), 4) pow(x,2) + 2]]가 만나는 점의 [[y]]좌표를 [[c]]라 하자. 집합 [[X]]로 둘러싸인 부분의 넓이를 [[alpha]], "
              "곡선 [[y = -frac(sqrt(3), 4) pow(x,2) + 2]]와 직선 [[y = c]]로 둘러싸인 부분의 넓이를 [[beta]]라 하자.\n"
              "[[alpha - beta = frac(p pi + q sqrt(3), 3)]] 일 때, [[p + q]]의 값을 구하시오.\n"
              "(단, [[p]]와 [[q]]는 정수이다.)"),
    choices=None, derived_answer="30", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2022년 경찰대 25번 변형]. c=2−√3(x=±2), α=10√3+8π/3, β=8√3/3 → (8π+22√3)/3 → 30 = 빠른정답 ✓.")

# ───────────────────────── 미분계수 p95 (조각적 정의)
add(id="c4fce2f4", qtype="short",
    question=("두 자연수 [[a]], [[b]]에 대하여 두 함수 [[f(x)]], [[g(x)]]를\n"
              "[[f(x)]] = { [[x + 5]] ([[x < 5]]) ; [[abs(2x - a)]] ([[x >= 5]]) },\n"
              "[[g(x) = (x - 5)(x - b)]]라 하자. 함수 [[f(x) g(x)]]가 실수 전체의 집합에서 미분가능하도록 하는 [[a]], [[b]]의 모든 "
              "순서쌍 [[point(a, b)]]의 개수를 구하시오."),
    choices=None, derived_answer="11", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PW,
    note="출처 [2022년 11월 고2 29번/4점]. x=5: b=5 또는 a=20; a≥11이면 꺾이는 점 a/2에서 g=0 → b=a/2 → (a,5) a=1~10 10개 + (20,10) → 11. 빠른정답 4와 불일치.")
