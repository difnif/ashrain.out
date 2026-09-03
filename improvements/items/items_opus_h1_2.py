# -*- coding: utf-8 -*-
# esc_opus_h1-2_1of1 — 이미지 기준 전사 (25 항목 / 19쪽)
ITEMS = []
CH_G = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# 집합의 개념과 표현 p18 (id 3개)
_p18 = {
    "qtype": "choice",
    "question": ("집합 [[M]]을\n[[M]] = { [[mat(2,2, x,y, z,w)]] | [[x]], [[y]], [[z]], [[w]]는 [[x < y < z < w]]인 실수 }\n"
                 "라 하자. [[in(X, M)]]인 [[X = mat(2,2, a,b, c,d)]]에 대하여 네 점 [[point(a, b)]], [[point(c, d)]], "
                 "[[point(a, c)]], [[point(b, d)]]를 꼭짓점으로 하는 사각형의 넓이를 [[S(X)]]라 할 때, "
                 "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
                 "ㄱ. [[A = mat(2,2, 1,2, 3,4)]]일 때, [[S(A) = frac(3,2)]]\n"
                 "ㄴ. [[in(A, M)]]이면 [[S(k A) = pow(k,2) S(A)]] (단, [[k]]는 양의 실수)\n"
                 "ㄷ. [[B = mat(2,2, 1,1, 1,1)]]에 대하여 [[in(A, M)]]이면 [[S(A + m B) = S(A)]] (단, [[m]]은 실수)"),
    "choices": CH_G, "derived_answer": "⑤", "quick_answer": None, "figure": None, "difficulty_est": 4, "confidence": 0.85,
    "note": "출처 [2011년 7월 고3 문과 15번/4점]. ㄱ 넓이 3/2 ✓, ㄴ 닮음비 k² ✓, ㄷ 모든 점 (m,m) 평행이동 ✓ → ⑤ (빠른정답 없음, 풀이 답).",
}
for i in ("1424b605", "47b1e24c", "3b6d2e39"):
    ITEMS.append(dict(_p18, id=i))

# p20
ITEMS.append({
    "id": "f25c38e8", "qtype": "choice",
    "question": ("이차정사각행렬 [[A]], [[B]]에 대하여 [[C(A, B) = A B - B A]] 라 하자.\n"
                 "정수 [[k]]에 대하여 이차정사각행렬의 집합 [[sub(M,k)]]를\n"
                 "[[sub(M,k)]] = { [[(sub(a,i,j))]] | [[i]] = 1, 2, [[j]] = 1, 2에 대하여 [[i - j != k]]이면 [[sub(a,i,j) = 0]] }\n"
                 "으로 정의할 때, 옳은 내용만을 <보기>에서 있는 대로 고른 것은? (단, [[O]]는 영행렬이고 [[E]]는 단위행렬이다.)\n<보기>\n"
                 "ㄱ. [[A]], [[in(B, sub(M,0))]]이면 [[C(A, B) = O]]이다.\n"
                 "ㄴ. [[abs(k) >= 2]]이면 [[sub(M,k) = set(O, E)]]이다.\n"
                 "ㄷ. [[abs(k) < 2]]일 때, [[A]], [[in(B, sub(M,k))]]이면 [[C(A, B) = O]]이다."),
    "choices": ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    "derived_answer": "③", "quick_answer": None, "figure": None, "difficulty_est": 4, "confidence": 0.85,
    "note": "출처 [2010년 6월 고2 이과 14번]. M₀=대각행렬(가환) ㄱ✓, |k|≥2이면 M_k={O} ㄴ✗, k=±1은 단일 성분 행렬끼리 가환 ㄷ✓ → ③.",
})

# p23 (id 3개)
_p23 = {
    "qtype": "choice",
    "question": ("행렬 [[P = mat(2,2, 1,0, -2,-1)]]일 때, 집합 [[S]]를\n"
                 "[[S]] = { [[A]] | [[A P = P A]], [[A]]는 이차정사각행렬 }\n"
                 "이라 하자. 옳은 것만을 <보기>에서 있는 대로 고른 것은?\n<보기>\n"
                 "ㄱ. [[in(A, S)]], [[in(B, S)]]이면 [[in(A B, S)]]이다.\n"
                 "ㄴ. [[in(mat(2,2, a,b, c,d), S)]]이면 [[b = 0]]이다.\n"
                 "ㄷ. [[in(A, S)]], [[in(B, S)]]이면 [[A B = B A]]이다."),
    "choices": CH_G, "derived_answer": "⑤", "quick_answer": None, "figure": None, "difficulty_est": 4, "confidence": 0.85,
    "note": "출처 [2012년 6월 고2 문과 15번/4점]. P²=E, 가환행렬은 aE+bP 꼴 → ㄱ✓ ㄴ✓(b=0) ㄷ✓ → ⑤.",
}
for i in ("7c70ecd9", "7aa8264a", "1847f98d"):
    ITEMS.append(dict(_p23, id=i))

# p97
ITEMS.append({
    "id": "55d83dd2", "qtype": "short",
    "question": ("세 자연수 [[a]], [[b]], [[c]] ([[a < b < c]])에 대하여 집합 [[A = set(a, b, c)]]이고 "
                 "집합 [[B]] = { [[x + y]] | [[in(x, A)]], [[in(y, A)]] }의 모든 원소의 합이 100이다. "
                 "이때 집합 [[A]]의 개수를 구하시오."),
    "choices": None, "derived_answer": "49", "quick_answer": "49", "figure": None, "difficulty_est": 4,
    "note": "원소 6개일 때 a+b+c=25 → 40개, 2b=a+c(원소 5개)일 때 b=10 → 9개 → 49 = 빠른정답 ✓.",
})

# 대칭이동 p19 — 복합 도형 → review
ITEMS.append({
    "id": "17f69b70", "qtype": "choice",
    "question": ("좌표평면 위의 제1사분면에 있는 점 A를 중심으로 하고 원점 O를 지나는 원 [[sub(C,1)]]이 있다. "
                 "원 [[sub(C,1)]]을 원점 O에 대하여 대칭이동한 원을 [[sub(C,2)]]라 할 때, 두 원 [[sub(C,1)]], [[sub(C,2)]]가 다음 조건을 만족시킨다.\n"
                 "삼각형 OPQ의 외접원의 중심이 선분 PQ 위에 있도록 하는 원 [[sub(C,1)]] 위의 점 P와 원 [[sub(C,2)]] 위의 점 Q에 대하여 [[seg(PQ) = 10]]이다.\n"
                 "원 [[sub(C,2)]]가 [[x]]축과 만나는 점 중 O가 아닌 점을 B라 할 때, 원 [[sub(C,2)]] 위의 점 B에서의 접선을 [[l]]이라 하자. "
                 "직선 [[l]]의 기울기가 [[frac(3,4)]]일 때, 점 A와 직선 [[l]] 사이의 거리는?"),
    "choices": ["[[frac(9,5)]]", "[[2]]", "[[frac(11,5)]]", "[[frac(12,5)]]", "[[frac(13,5)]]"],
    "derived_answer": "③", "quick_answer": "2",
    "figure": [{"fn": "unsupported", "args": {"raw": "좌표평면: 원점을 지나는 두 원 C₁(중심 A, 제1사분면)·C₂(원점 대칭), 점 P(C₁ 위)·Q(C₂ 위)·B(C₂와 x축 교점), 접선 l, 삼각형 OPQ 음영"}}],
    "difficulty_est": 5, "confidence": 0.8,
    "needs_review": "도형 표현 불가: 원 2개+접선+삼각형 복합 좌표평면 도형",
    "note": "∠POQ=90° ⇒ PQ=2r=10, r=5; A=(3,4), B=(-6,0), l: 3x-4y+18=0 → 거리 11/5 → ③. 빠른정답 2와 불일치.",
})

# 집합의 연산 p17
ITEMS.append({
    "id": "b6881441", "qtype": "short",
    "question": ("집합 [[S]] = { [[x]] | [[x < 100]], [[x]]는 자연수 }의 부분집합 [[A]]가 다음 조건을 만족할 때, "
                 "[[comp(A)]]의 원소 중 가장 큰 수를 구하시오.\n"
                 "(가) [[in(4, A)]], [[in(5, A)]]\n"
                 "(나) [[in(p, A)]], [[in(q, A)]]이면 [[in(p + q, A)]]"),
    "choices": None, "derived_answer": "11", "quick_answer": "11", "figure": None, "difficulty_est": 3,
    "note": "4a+5b로 표현 불가한 최대 자연수 11 = 빠른정답 ✓.",
})

# p22
ITEMS.append({
    "id": "31836289", "qtype": "short",
    "question": ("전체집합 [[U]] = { [[x]] | [[x]]는 15 이하의 자연수 }의 두 부분집합 [[A]], [[B]]가 다음 조건을 만족시킨다.\n"
                 "(가) [[card(A) = card(B) = 6]], [[card(inter(A, B)) = 1]]\n"
                 "(나) 집합 [[A]]의 임의의 서로 다른 두 원소의 합은 6의 배수가 아니다.\n"
                 "(다) 집합 [[B]]의 임의의 서로 다른 두 원소의 합은 7의 배수가 아니다.\n"
                 "집합 [[A]]의 모든 원소의 합을 [[S(A)]], 집합 [[B]]의 모든 원소의 합을 [[S(B)]]라 할 때, [[S(A) - S(B)]]의 최댓값을 구하시오."),
    "choices": None, "derived_answer": "37", "quick_answer": "X", "figure": None, "difficulty_est": 5, "confidence": 0.75,
    "note": "출처 [2020년 11월 고1 29번 변형]. 빠른정답 'X'(값 아님). 풀이: A={7,8,12,13,14,15}(69), B={1,2,3,7,9,10}(32), 교집합 {7} → 37 (검토 필요).",
})

# p32 (id 2개)
_p32 = {
    "qtype": "short",
    "question": ("전체집합 [[U]] = { [[x]] | [[x]]는 18 이하의 자연수 }의 부분집합 [[P]] = { [[x]] | [[x]]는 18 이하의 소수 }에 대하여 "
                 "다음 조건을 만족시키는 [[U]]의 부분집합 [[X]]의 개수를 구하시오.\n"
                 "(가) [[card(X - P) × card(union(X, comp(P))) = 13]]\n"
                 "(나) 집합 [[X]]의 모든 원소의 곱이 [[M]]일 때, [[M]]의 양의 약수의 개수는 12이다."),
    "choices": None, "derived_answer": "78", "quick_answer": "5", "figure": None, "difficulty_est": 5, "confidence": 0.8,
    "note": "출처 [2025년 3월 고2 29번 변형]. n(X−P)=1, n(X∩P)=2; 합성수 c별 약수 12개 경우 합 15+10+15+10+1+10+10+6+1=78. 빠른정답 5와 불일치(옆 문항 p35의 빠른정답이 78).",
}
for i in ("42289289", "9c70114f"):
    ITEMS.append(dict(_p32, id=i))

# p35
ITEMS.append({
    "id": "28cc824f", "qtype": "short",
    "question": ("전체집합 [[U]] = { [[x]] | [[x]]는 15 이하의 자연수 }의 부분집합 [[P]] = { [[x]] | [[x]]는 15 이하의 소수 }에 대하여 "
                 "다음 조건을 만족시키는 [[U]]의 부분집합 [[X]]의 개수를 구하시오.\n"
                 "(가) [[card(X - P) × card(union(X, comp(P))) = 11]]\n"
                 "(나) 집합 [[X]]의 모든 원소의 곱이 [[M]]일 때, [[M]]의 양의 약수의 개수는 16이다."),
    "choices": None, "derived_answer": "38", "quick_answer": "78", "figure": None, "difficulty_est": 5, "confidence": 0.8,
    "note": "출처 [2025년 3월 고2 29번/4점]. n(X−P)=1, n(X∩P)=2; c=6,8,10,12,14,15 → 6+10+6+4+6+6=38. 빠른정답 78과 불일치.",
})

# 명제 p41
ITEMS.append({
    "id": "2dc1c294", "qtype": "short",
    "question": ("실수 [[x]]에 대한 두 조건\n[[p]]: [[(pow(x,2) - a x + 2a)(pow(x,2) - x - 6) < 0]],\n"
                 "[[q]]: [[pow(x,2) - x - 6 < 0]]에 대하여 명제 [[imp(p, q)]]가 참이 되도록 하는 실수 [[a]]의 최댓값을 [[M]], "
                 "최솟값을 [[m]]이라 할 때, [[M + m]]의 값을 구하시오."),
    "choices": None, "derived_answer": "7", "quick_answer": "7", "figure": None, "difficulty_est": 4,
    "note": "x²−ax+2a≥0 on (−∞,−2]∪[3,∞) ⇔ −1≤a≤8 → M+m=7 = 빠른정답 ✓.",
})

# 원의 방정식 p28
ITEMS.append({
    "id": "9bffdb72", "qtype": "choice",
    "question": ("좌표평면 위의 세 점 A, B, C에 대하여 두 점 A, B의 좌표는 각각 [[point(0, a)]], [[point(4, 0)]]이고, "
                 "삼각형 ABC는 [[seg(AC) = seg(BC)]]인 직각이등변삼각형이다. [[-2 <= a <= 3]]일 때, 선분 OC의 길이의 최댓값을 [[M]], "
                 "최솟값을 [[m]]이라 하자. [[frac(M, m)]]의 값은? (단, O는 원점이다.)"),
    "choices": ["[[frac(20,3)]]", "[[7]]", "[[frac(22,3)]]", "[[frac(23,3)]]", "[[8]]"],
    "derived_answer": "②", "quick_answer": "2", "figure": None, "difficulty_est": 3,
    "note": "C=(2±a/2, 2±a/2) → OC=√2|2±a/2|, 최대 3.5√2, 최소 0.5√2 → 7 → ② = 빠른정답 ✓.",
})

# 원의 방정식 p29
ITEMS.append({
    "id": "7bbe710a", "qtype": "choice",
    "question": ("좌표평면 위의 세 점 A, B, C에 대하여 두 점 A, B의 좌표는 각각 [[point(0, 4)]], [[point(a, 0)]]이고 "
                 "삼각형 ABC는 [[seg(AC) = seg(BC)]]인 직각이등변삼각형이다. [[0 <= a <= 4]]일 때, 점 C의 자취의 길이는?"),
    "choices": ["[[sqrt(2)]]", "[[2 sqrt(2)]]", "[[3 sqrt(2)]]", "[[4 sqrt(2)]]", "[[5 sqrt(2)]]"],
    "derived_answer": "④", "quick_answer": "2", "figure": None, "difficulty_est": 3, "confidence": 0.85,
    "note": "출처 [2018년 9월 고1 21번 변형]. C=(a/2+2, a/2+2) 또는 (a/2−2, 2−a/2): 자취 두 선분 각 2√2 → 4√2 → ④. 빠른정답 2와 불일치.",
})

# 원의 방정식 p71
ITEMS.append({
    "id": "200627e3", "qtype": "short",
    "question": ("좌표평면 위에 두 원\n[[sub(C,1)]]: [[pow(x,2) + pow(y - 4, 2) = 4]]\n"
                 "[[sub(C,2)]]: [[pow(x - 6, 2) + pow(y - 4 + 6 sqrt(3), 2) = 16]]\n"
                 "이 있다. 원 [[sub(C,1)]] 위를 움직이는 점 [[P(sub(x,1), sub(y,1))]]과 원 [[sub(C,2)]] 위를 움직이는 점 [[Q(sub(x,2), sub(y,2))]]가 다음 조건을 만족시킨다.\n"
                 "(가) [[0 <= sub(x,1) <= 1]], [[frac(2 sub(x,1) + sub(x,2), 3) = 2]]\n"
                 "(나) [[sub(y,1) <= 4]], [[sub(y,2) >= 4 - 6 sqrt(3)]]\n"
                 "선분 PQ가 그리는 도형의 넓이가 [[a - b pi]]일 때, [[a + 9b]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수이다.)"),
    "choices": None, "derived_answer": "25", "quick_answer": "25", "figure": None, "difficulty_est": 5,
    "note": "출처 [2017년 9월 고1 30번/4점]. PQ는 정점 R(2, 4−2√3)을 1:2로 지남 → 넓이 (2−π/3)+4(2−π/3)=10−5π/3 → a+9b=25 = 빠른정답 ✓.",
})

# 함수의 합성 p68 (id 2개)
_p68 = {
    "qtype": "choice",
    "question": ("자연수 전체의 집합 [[N]]에 대하여 함수 [[f]]: [[N]]→[[N]]을 다음과 같이 정의하자.\n"
                 "[[f(x)]] = ([[x]]의 양의 약수의 개수)\n"
                 "자연수 [[n]]에 대하여 집합 [[sub(Y,n)]]이\n"
                 "[[sub(Y,n)]] = { [[x]] | [[f(x) = n]], [[in(x, N)]] }일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
                 "ㄱ. 함수 [[f]]의 공역과 치역은 서로 같다.\n"
                 "ㄴ. 함수 [[g]]: [[sub(Y,2)]]→[[sub(Y,100)]]을 [[g(x) = pow(x,99)]]으로 정의할 때, 함수 [[g]]는 일대일대응이다.\n"
                 "ㄷ. 부등식 ([[comp(f, f)]])([[x]]) < 3을 만족시키는 20 이하의 자연수 [[x]]의 개수는 12이다."),
    "choices": ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    "derived_answer": "④", "quick_answer": "4", "figure": None, "difficulty_est": 4, "confidence": 0.85,
    "note": "ㄱ✓(치역=N), ㄴ✗(p⁴q⁴r³ 등 원상 없음), ㄷ✓(d(d(x))<3: 1,소수8,4,9,16 → 12) → ④ = 빠른정답 ✓. (f∘f)(x) 적용 표기는 문법에 없어 '(…)(x) < 3'을 텍스트 혼합으로 전사.",
}
for i in ("04d76aca", "95023144"):
    ITEMS.append(dict(_p68, id=i))

# 원과 직선 p94
ITEMS.append({
    "id": "9e635a05", "qtype": "short",
    "question": ("두 실수 [[a]], [[b]]에 대하여 이차함수 [[f(x) = a pow(x - b, 2)]]이 있다. 중심이 함수 [[y = f(x)]]의 그래프 위에 있고 "
                 "직선 [[y = frac(4,3) x]]와 [[x]]축에 동시에 접하는 서로 다른 원의 개수는 3이다. 이 세 원의 중심의 [[x]]좌표를 각각 "
                 "[[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]]이라 할 때, 세 실수 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]]이 다음 조건을 만족시킨다.\n"
                 "(가) [[sub(x,1) sub(x,2) sub(x,3) > 0]]\n"
                 "(나) 세 점 [[point(sub(x,1), f(sub(x,1)))]], [[point(sub(x,2), f(sub(x,2)))]], [[point(sub(x,3), f(sub(x,3)))]]을 "
                 "꼭짓점으로 하는 삼각형의 무게중심의 [[y]]좌표는 [[-frac(7,3)]]이다.\n"
                 "[[f(4) × f(6)]]의 값을 구하시오."),
    "choices": None, "derived_answer": "9", "quick_answer": "7", "figure": None, "difficulty_est": 5, "confidence": 0.8,
    "note": "출처 [2024년 9월 고1 30번/4점]. 중심은 y=±x/2 위; y=−x/2 접·y=x/2 교차, a=−1/16, b=−2 → f(4)f(6)=(−9/4)(−4)=9. 빠른정답 7과 불일치.",
})

# 함수의 개념 p7
ITEMS.append({
    "id": "cc7da6d2", "qtype": "short",
    "question": ("자연수 전체의 부분집합 [[X]]가 상수 [[p]]에 대하여 다음 조건을 만족시킨다.\n"
                 "(가) [[card(X) = 2]]\n"
                 "(나) [[in(x, X)]]일 때,\n[[x]]가 홀수이면 [[in(frac(x + 1, 2), X)]],\n[[x]]가 짝수이면 [[in(frac(x + p, 2), X)]]이다.\n"
                 "[[in(6, X)]]일 때, 모든 상수 [[p]]의 값의 합을 구하시오."),
    "choices": None, "derived_answer": "18", "quick_answer": "18", "figure": None, "difficulty_est": 4,
    "note": "출처 [2017년 3월 고3 문과 30번 변형]. p∈{6,16,−4} → 18 = 빠른정답 ✓.",
})

# 함수의 개념 p82
ITEMS.append({
    "id": "3c70a472", "qtype": "short",
    "question": ("전체집합 [[U = set(1, 2, 3, 4, 5)]]의 두 부분집합 [[A]], [[B]]에 대하여 [[union(A, B) = U]], [[card(inter(A, B)) = 1]]이다. "
                 "함수 [[f]]: [[A]]→[[B]]가 일대일함수일 때, 함수 [[f]]의 개수를 구하시오."),
    "choices": None, "derived_answer": "445", "quick_answer": "420", "figure": None, "difficulty_est": 4, "confidence": 0.8,
    "note": "|A|=1: 5·5=25, |A|=2: 20·12=240, |A|=3: 30·6=180 → 445. 빠른정답 420과 불일치(|A|=1 경우 25 차이).",
})

# 함수의 개념 p83
ITEMS.append({
    "id": "aa680144", "qtype": "choice",
    "question": ("집합 [[X = set(1, 2, 3, 4)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족시킨다.\n"
                 "집합 [[X]]의 임의의 두 원소 [[a]], [[b]]에 대하여 [[f(a) >= b]]이면 [[f(a) >= f(b)]] 이다.\n"
                 "[[f(1) = 3]]일 때, [[f(2) + f(4)]]의 최솟값은?"),
    "choices": ["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    "derived_answer": "④", "quick_answer": "24", "figure": None, "difficulty_est": 4, "confidence": 0.85,
    "note": "출처 [2019년 10월 고3 문과 20번/4점]. f(2)=3, f(4)=3 강제 → 6 → ④. 빠른정답 24는 선지 범위 밖.",
})

# 평행이동 p86
ITEMS.append({
    "id": "6b0d32c7", "qtype": "short",
    "question": ("이차함수 [[y = f(x)]]가 있다. 중심이 함수 [[y = f(x)]]의 그래프 위에 있고 반지름의 길이가 2인 원 중에서 다음 조건을 만족시키는 "
                 "중심이 서로 다른 원의 개수는 5이다.\n"
                 "원을 [[x]]축의 방향으로 [[m]]만큼, [[y]]축의 방향으로 [[m]]만큼 평행이동한 원이 [[x]]축과 [[y]]축에 동시에 접하도록 하는 "
                 "실수 [[m]]의 값이 1개 이상 존재한다.\n"
                 "이 5개의 원의 중심의 [[x]]좌표를 작은 수부터 크기 순서대로 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]], [[sub(x,5)]]라 하자.\n"
                 "[[sub(x,1) = 0]], [[sub(x,2) + sub(x,3) + sub(x,4) + sub(x,5) = 30]]이고\n"
                 "[[sub(x,1) <= x <= sub(x,5)]]에서 함수 [[f(x)]]의 최솟값이 0보다 클 때,\n[[f(6)]]의 값을 구하시오."),
    "choices": None, "derived_answer": "2", "quick_answer": "26", "figure": None, "difficulty_est": 5, "confidence": 0.75,
    "note": "출처 [2023년 9월 고1 30번 변형]. 중심은 y=x, y=x±4 위; 접점 x=6, f(x)=(2/9)(x−6)²+x−4 → f(6)=2. 빠른정답 26과 불일치(검토 필요).",
})
