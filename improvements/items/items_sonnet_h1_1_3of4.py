# -*- coding: utf-8 -*-
# esc_sonnet_h1-1_3of4 — 이미지 기준 전사 (80 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_G5 = ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_G5b = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
MA = "mat(2,2, sub(a,1,1), sub(a,1,2), sub(a,2,1), sub(a,2,2))"
MB = "mat(2,2, sub(b,1,1), sub(b,1,2), sub(b,2,1), sub(b,2,2))"

# ───────────────────────── 행렬의 연산 ─────────────────────────
# p40
add(id="06eefd19", qtype="choice",
    question=("이차방정식 [[pow(x,2) - 2x + 2 = 0]]의 두 근을 [[alpha]], [[beta]]라 할 때, "
              "행렬 [[X = mat(2,2, alpha + beta - 1, frac(1, alpha) + frac(1, beta), 0, 0)]]에 대하여 "
              "행렬 [[X + pow(X,2) + pow(X,3)]] + ⋯ + [[pow(X,14)]]은?"),
    choices=["[[mat(2,2, 7,0, 7,0)]]", "[[mat(2,2, 7,7, 0,0)]]", "[[mat(2,2, 0,0, 14,14)]]",
             "[[mat(2,2, 14,0, 14,0)]]", "[[mat(2,2, 14,14, 0,0)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="α+β=2, αβ=2 → X=(1 1;0 0), X²=X → 합 14X=(14 14;0 0) → ⑤. 빠른정답 3과 불일치.")

# p42
add(id="83b8f731", qtype="short",
    question=("행렬 [[A = mat(2,2, 1,0, 5,1)]]과 자연수 [[n]]에 대하여 [[pow(A,n)]]의 모든 성분의 합을 "
              "[[sub(a,n)]]이라 할 때, [[sub(a,n) >= 40]]을 만족시키는 [[n]]의 최솟값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="Aⁿ=(1 0;5n 1), 2+5n≥40 → n≥7.6 → 8. 빠른정답 202와 불일치.")

# p43
add(id="3fc7d8a3", qtype="choice",
    question=("표는 2013학년도 수시 모집에서 어느 대학 A 학과와 B 학과의 선발 인원수와 경쟁률을 나타낸 것이다.\n"
              "경쟁률은 (지원자 수)/(선발 인원 수)의 값이고, 일반 전형과 특별 전형에 동시에 지원할 수 없으며, "
              "A 학과와 B 학과에 동시에 지원할 수 없다고 한다. 2013학년도 수시 모집에서 이 대학 A, B 두 학과의 "
              "일반 전형 지원자 수의 합을 [[m]], B 학과의 일반 전형과 특별 전형 지원자 수의 합을 [[n]]이라 하자. "
              "두 행렬 [[P = mat(2,2, 30,40, 10,20)]], [[Q = mat(2,2, 5.1,21.4, 10.7,11.5)]]에 대하여 "
              "[[m + n]]의 값과 같은 것은?"),
    choices=["행렬 [[P Q]]의 (1, 1)성분과 (2, 2)성분의 합",
             "행렬 [[P Q]]의 (1, 1)성분과 행렬 [[Q P]]의 (1, 1)성분의 합",
             "행렬 [[P Q]]의 (1, 1)성분과 행렬 [[Q P]]의 (2, 2)성분의 합",
             "행렬 [[P Q]]의 (2, 2)성분과 행렬 [[Q P]]의 (1, 1)성분의 합",
             "행렬 [[P Q]]의 (2, 2)성분과 행렬 [[Q P]]의 (2, 2)성분의 합"],
    derived_answer="③",
    figure=[{"fn": "table", "args": {"caption": "<선발 인원수>", "head": ["구분", "A 학과", "B 학과"],
                                     "rows": [["일반 전형", "30", "40"], ["특별 전형", "10", "20"]]}},
            {"fn": "table", "args": {"caption": "<경쟁률>", "head": ["구분", "일반 전형", "특별 전형"],
                                     "rows": [["A 학과", "5.1", "21.4"], ["B 학과", "10.7", "11.5"]]}}],
    difficulty_est=3, confidence=0.9,
    note="출처 [2013년 6월 고2 문과 9번/3점]. m=30·5.1+40·10.7=PQ(1,1), n=40·10.7+20·11.5=QP(2,2) → ③. 빠른정답 5와 불일치.")

# p44
add(id="e577f233", qtype="choice",
    question=("어떤 회사에서 새로 추진하려는 사업에 대하여 전체 사원을 대상으로 세 차례에 걸쳐 찬반 의견을 조사하였다. "
              "1차 조사 결과 찬성이 60%, 반대가 40%였다. 아래 표는 사업 설명회 이후 2차 조사 결과 1차 조사와 달리 "
              "찬반 의견을 바꾼 비율과 사원 토론회 이후 3차 조사 결과 2차 조사와 달리 찬반 의견을 바꾼 비율을 각각 나타낸 것이다.\n"
              "[[A = mat(1,2, 0.6, 0.4)]], [[B = mat(2,2, 0.8,0.2, 0.3,0.7)]], [[C = mat(2,2, 0.9,0.1, 0.4,0.6)]]일 때, "
              "3차 조사 결과 전체 사원 중에서 찬성하는 사원들의 비율을 나타내는 것은? (단, 기권한 사원은 없다.)"),
    choices=["[[A B C]]의 (1, 1)성분", "[[A B C]]의 (1, 2)성분", "[[A C B]]의 (1, 1)성분",
             "[[A C B]]의 (1, 2)성분", "[[A pow(B,2)]]의 (1, 1)성분"],
    derived_answer="①",
    figure=[{"fn": "table", "args": {"head": ["변화 \\ 조사", "직전조사에서 찬성한 사원 중 반대로 의견을 바꾼 비율",
                                              "직전조사에서 반대한 사원 중 찬성으로 의견을 바꾼 비율"],
                                     "rows": [["2차 조사 결과", "20%", "30%"], ["3차 조사 결과", "10%", "40%"]]}}],
    difficulty_est=3, confidence=0.9,
    note="출처 [2009년 10월 고3 문과 27번]. 2차 찬성 비율=AB(1,1), 3차=ABC(1,1) → ①. 빠른정답 -15와 불일치.")

# p46
add(id="63e357ed", qtype="choice",
    question=("다음 표는 S회사와 L회사의 TV와 냉장고 한 대당 가격을 나타낸 것이다. 할인 기간동안 S회사는 기존 가격의 20%, "
              "L회사는 30% 할인하여 TV와 냉장고를 판매한다. 이 할인 기간 동안 S회사의 TV 한 대와 L회사의 TV 한 대 가격의 합을 나타낸 것은?"),
    choices=["행렬 [[mat(2,2, a,b, c,d) mat(2,2, 0.8,0.7, 0.8,0.7)]]의 (1, 1) 성분",
             "행렬 [[mat(2,2, a,b, c,d) mat(2,2, 0.8,0.7, 0.8,0.7)]]의 (1, 2) 성분",
             "행렬 [[mat(2,2, a,b, c,d) mat(2,1, 0.8, 0.7)]]의 (1, 1) 성분",
             "행렬 [[mat(2,2, a,b, c,d) mat(2,1, 0.8, 0.7)]]의 (2, 1) 성분",
             "행렬 [[mat(1,2, 0.8, 0.7) mat(2,1, a, c)]]의 (1, 1) 성분"],
    derived_answer="③",
    figure=[{"fn": "table", "args": {"head": ["", "S회사", "L회사"],
                                     "rows": [["TV", "a(원)", "b(원)"], ["냉장고", "c(원)", "d(원)"]]}}],
    difficulty_est=2, confidence=0.9,
    note="0.8a+0.7b = (a b;c d)(0.8;0.7)의 (1,1) 성분 → ③ = 빠른정답 ✓.")

# p47
add(id="d4c786a2", qtype="choice",
    question=("다음은 지난해에 어느 회사에서 생산한 두 제품 (가)와 (나)의 제품 한 개당 제조원가와 판매 가격 및 그 해 판매량을 나타낸 표이다.\n"
              f"위의 표를 각각 행렬 [[A = {MA}]]와 [[B = {MB}]]로 나타내고, 이 두 행렬의 곱 [[A B]]를 [[A B = mat(2,2, a,b, c,d)]]라 하자. "
              "제품 한 개당 판매 이익금을 판매 가격에서 제조원가를 뺀 값으로 정의할 때, <보기>에서 옳은 것을 모두 고른 것은?\n<보기>\n"
              "ㄱ. [[a + b]]는 지난해 상반기에 판매된 제품의 제조원가 총액이다.\n"
              "ㄴ. [[c + d]]는 지난해 1년 동안에 판매된 제품의 판매 총액이다.\n"
              "ㄷ. [[d - b]]는 지난해 하반기에 판매된 제품의 판매 이익금 총액이다."),
    choices=CH_G5, derived_answer="④",
    figure=[{"fn": "table", "args": {"head": ["가격 \\ 제품명", "(가)", "(나)"],
                                     "rows": [["제조원가", "a₁₁", "a₁₂"], ["판매 가격", "a₂₁", "a₂₂"]]}},
            {"fn": "table", "args": {"head": ["제품명 \\ 판매량", "상반기", "하반기"],
                                     "rows": [["(가)", "b₁₁", "b₁₂"], ["(나)", "b₂₁", "b₂₂"]]}}],
    difficulty_est=3, confidence=0.9,
    note="출처 [2004년 11월 고3 문과 8번]. a,b=상·하반기 제조원가 총액, c,d=상·하반기 판매 총액 → ㄱ✗ ㄴ✓ ㄷ✓ → ④ = 빠른정답 ✓.")

# p48
add(id="dc378a7f", qtype="choice",
    question=("다음은 지난해에 어느 실험실에서 실험한 두 미생물 (가)와 (나)의 미생물 1마리당 실험 전후 발광량 및 시기별 배양된 미생물 수를 나타낸 표이다.\n"
              f"위의 표를 각각 행렬 [[A = {MA}]]와 [[B = {MB}]]로 나타내고, 이 두 행렬의 곱 [[A B]]를 [[A B = mat(2,2, a,b, c,d)]]라 하자. "
              "미생물 1마리당 Gap수치를 실험 후 발광량에서 실험 전 발광량을 뺀 값으로 정의할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[a + b]]는 지난해 8월, 12월에 실험한 미생물의 실험 전 발광량 총량이다.\n"
              "ㄴ. [[c + d]]는 지난해 12월 동안에 실험한 미생물의 실험 후 발광량 총량이다.\n"
              "ㄷ. [[c - a]]는 지난해 8월에 실험한 미생물의 Gap수치 총량이다."),
    choices=CH_G5, derived_answer="③",
    figure=[{"fn": "table", "args": {"head": ["발광량 \\ 미생물", "(가)", "(나)"],
                                     "rows": [["실험 전 발광량", "a₁₁", "a₁₂"], ["실험 후 발광량", "a₂₁", "a₂₂"]]}},
            {"fn": "table", "args": {"head": ["미생물 \\ 시기", "8월", "12월"],
                                     "rows": [["(가)", "b₁₁", "b₁₂"], ["(나)", "b₂₁", "b₂₂"]]}}],
    difficulty_est=3, confidence=0.9,
    note="a,b=8월·12월 실험 전 총량, c,d=8월·12월 실험 후 총량 → ㄱ✓ ㄴ✗(8월 포함) ㄷ✓ → ③. 빠른정답 2와 불일치.")

# p49
add(id="380b8de3", qtype="choice",
    question=("어떤 사람이 두 곳의 과수원 A, B에서 사과와 복숭아를 재배하고 있다. [표 1]은 과수원의 작물의 그루수를 나타낸 것이고, "
              "[표 2]는 과수원의 작물 한 그루당 열매의 평균 개수를 나타낸 것이다.\n"
              f"[[{MA} {MB} = mat(2,2, a,b, c,d)]], [[{MA} mat(2,1, 1, 1) = mat(2,1, p, q)]]라 할 때, "
              "두 과수원에서 생산된 사과의 총 개수는 (가) 이고, 두 과수원의 복숭아 한 그루당 열매의 평균 개수는 (나) 이다. "
              "(가), (나)에 알맞은 것을 순서대로 적은 것은?"),
    choices=["[[a]], [[frac(a,p)]]", "[[a]], [[frac(b,q)]]", "[[a]], [[frac(d,q)]]", "[[b]], [[frac(c,p)]]", "[[b]], [[frac(c,q)]]"],
    derived_answer="③",
    figure=[{"fn": "table", "args": {"caption": "[표 1] (단위 : 그루)", "head": ["", "A", "B"],
                                     "rows": [["사과", "a₁₁", "a₁₂"], ["복숭아", "a₂₁", "a₂₂"]]}},
            {"fn": "table", "args": {"caption": "[표 2] (단위 : 개)", "head": ["", "사과", "복숭아"],
                                     "rows": [["A", "b₁₁", "b₁₂"], ["B", "b₂₁", "b₂₂"]]}}],
    difficulty_est=3, confidence=0.9,
    note="출처 [2005년 3월 고3 문과 17번]. 사과 총 개수 a, 복숭아 총 개수 d, 복숭아 그루수 q → (가)=a, (나)=d/q → ③. 빠른정답 2와 불일치.")

# p51
add(id="3cb01375", qtype="choice",
    question=("두 행렬 [[A]], [[B]]에 대하여 [[pow(A,2) + pow(B,2) = mat(2,2, 4,-4, 1,4)]], "
              "[[pow(A - B, 2) = mat(2,2, 1,0, -2,9)]]일 때, [[pow(A + B, 2)]]의 (2, 1) 성분은?"),
    choices=["3", "4", "5", "6", "7"], derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(A+B)²=2(A²+B²)−(A−B)² → (2,1) 성분 2·1−(−2)=4 → ② = 빠른정답 ✓.")

# p53
add(id="3b90aea0", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 3,1, 2,4)]], [[B = mat(2,2, -2,-1, -2,-3)]]에 대하여 행렬 [[pow(A,2) + A B]]의 모든 성분의 합은?"),
    choices=["10", "12", "14", "16", "18"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2005년 7월 고3 이과 3번]. A²+AB=A(A+B)=AE=A → 합 10 → ①. 빠른정답 2와 불일치.")

# p54
add(id="d284c935", qtype="short",
    question=("세 행렬 [[A = mat(2,2, 1,0, -2,2)]], [[B = mat(2,2, 4,1, 0,2)]], [[C = mat(2,2, -2,1, -1,3)]]에 대하여 "
              "행렬 [[A(B + C) + (C - A) B - C(A + B)]]의 모든 성분의 합을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="식=AC−CA=(2 −1;9 −2) → 합 8. 빠른정답 2와 불일치.")

# p55
add(id="3bf1f430", qtype="choice",
    question=("세 행렬 [[A = mat(2,2, 2,3, -2,5)]], [[B = mat(2,2, 4,2, 3,9)]], [[C = mat(2,2, 2,-2, 4,7)]]에 대하여 "
              "행렬 [[A(B - C)]]의 모든 성분의 합은?"),
    choices=["6", "7", "8", "9", "10"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="B−C=(2 4;−1 2), A(B−C)=(1 14;−9 2) → 합 8 → ③. 빠른정답 2와 불일치.")

# p56
add(id="c550c786", qtype="choice",
    question=("세 행렬 [[A]], [[B]], [[C]]에 대하여 [[A + B = mat(2,2, 1,3, 0,1)]], [[C = mat(2,2, 3,-1, 1,4)]]를 만족한다. "
              "행렬 [[C A]]의 (1, 2) 성분이 10일 때, [[C B]]의 (1, 2) 성분은?"),
    choices=["[[-4]]", "[[-2]]", "[[-1]]", "2", "4"], derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="C(A+B)의 (1,2) 성분 8 = CA(1,2)+CB(1,2) → CB(1,2)=−2 → ②. 빠른정답 1과 불일치.")

# p57
add(id="6ade25dd", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 2,0, 1,4)]], [[B = mat(2,2, 0,0, 1,0)]]에 대하여 행렬 [[pow(A,2) + A B]]의 모든 성분의 합은?"),
    choices=["25", "30", "35", "40", "45"], derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2014년 7월 고3 이과 2번/2점]. A(A+B)=(4 0;10 16) → 합 30 → ② = 빠른정답 ✓.")

# p59
add(id="c644a4f6", qtype="short",
    question=("두 행렬 [[A = mat(2,2, a,b, c,d)]], [[X = mat(2,2, 0,2, k,0)]]에 대하여 "
              "[[pow(A + X, 2) = pow(A,2) + 2 A X + pow(X,2)]], [[pow(A,2) = 4A]], [[pow(X,3) = 8X]]가 성립할 때, "
              "양수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a b c d k]]의 값을 구하시오. (단, [[k]]는 상수이다.)"),
    choices=None, derived_answer="64", figure=None, difficulty_est=3, confidence=0.9,
    note="X²=2kE, X³=8X → k=4; AX=XA → c=2b, a=d; A²=4A → a=2, b=√2 → abcdk=64. 빠른정답 2와 불일치(옆 문항 p62의 빠른정답이 64).")

# p60
add(id="6d50632e", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 4,1, 3,1)]], [[B = mat(2,2, 1,-1, -3,x)]]가 "
              "[[pow(A + B, 2) = pow(A,2) + 2 A B + pow(B,2)]]을 만족시킬 때, 실수 [[x]]의 값은?"),
    choices=["2", "4", "6", "8", "10"], derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="AB=BA → x−4=0 → x=4 → ② = 빠른정답 ✓.")

# p61
add(id="ddb25344", qtype="choice",
    question=("두 이차정사각행렬 [[A = mat(2,2, 1,0, 2,0)]], [[B = mat(2,2, 0,x, 2y,-3)]]이 "
              "[[pow(A + B, 2) = pow(A,2) + 2 A B + pow(B,2)]]을 만족시킬 때, [[x + y]]의 값은?"),
    choices=["1", "2", "3", "4", "5"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2011년 9월 고2 문과 6번/3점]. AB=BA → x=0, y=3 → ③ = 빠른정답 ✓.")

# p62
add(id="bf3b475f", qtype="short",
    question=("두 행렬 [[A = mat(2,2, 3,-1, -3,2)]], [[B = mat(2,2, x,1, y,3)]]에 대하여 "
              "[[pow(A + B, 2) = pow(A,2) + 2 A B + pow(B,2)]]이 성립할 때, 상수 [[x]], [[y]]에 대하여 [[x y]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="AB=BA → x=2, y=3 → xy=6. 빠른정답 64와 불일치.")

# p63
add(id="9f7fc1a9", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, a,b, c,d)]], [[B = mat(2,2, a + 3, b - 1, c + 6, d - 2)]]에 대하여 "
              "[[pow(A - B, 2) = pow(A,2) - 2 A B + pow(B,2)]], [[pow(A,2) - pow(B,2) = mat(2,2, -15,5, -30,10)]]일 때, "
              "행렬 [[A mat(2,1, 1, 2)]]의 모든 성분의 합은?"),
    choices=["2", "4", "6", "8", "10"], derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="B=A+C, C=(3 −1;6 −2), C²=C, A²−B²=−2AC−C → AC=(6 −2;12 −4) → a+2b=2, c+2d=4 → 합 6 → ③. 빠른정답 2와 불일치.")

# p64
add(id="2616cd13", qtype="short",
    question=("이차정사각행렬 [[A]]에 대하여 [[A mat(2,1, 3, -2) = mat(2,1, -6, 4)]], [[A mat(2,1, -1, 3) = mat(2,1, 0, 0)]]이다. "
              "[[pow(A,60) mat(2,1, 2, 1) = mat(2,1, x, y)]]를 만족시키는 실수 [[x]], [[y]]에 대하여 [[-frac(2x, y)]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="(2;1)=(3;−2)+(−1;3), A⁶⁰(2;1)=2⁶⁰(3;−2) → −2x/y=3 = 빠른정답 ✓.")

# p70
add(id="9f4d8ceb", qtype="choice",
    question=("행렬 [[B = mat(2,2, 1,2, -1,1)]]에 대하여 [[A - B = E]]를 만족시키는 행렬 [[A]]는? (단, [[E]]는 단위행렬이다.)"),
    choices=["[[mat(2,2, 2,2, -1,2)]]", "[[mat(2,2, 0,-2, 1,0)]]", "[[mat(2,2, -1,-4, 2,-1)]]",
             "[[mat(2,2, 3,4, -2,3)]]", "[[mat(2,2, 2,4, 1,-2)]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2014년 6월 고2 문과 2번/2점]. A=B+E=(2 2;−1 2) → ①. 빠른정답 36과 불일치.")

# p74
add(id="1a987942", qtype="short",
    question=("이차정사각행렬 [[A]]에 대하여 [[pow(A,2) = mat(2,2, 1,-2, 2,0)]]일 때, "
              "[[(pow(A,2) - 2A + E)(pow(A,2) + 2A + E)]]의 모든 성분의 합을 구하시오. (단, [[E]]는 단위행렬)"),
    choices=None, derived_answer="-7", figure=None, difficulty_est=3, confidence=0.9,
    note="(A−E)²(A+E)²=(A²−E)²=(0 −2;2 −1)²=(−4 2;−2 −3) → 합 −7. 빠른정답 18과 불일치.")

# p75
add(id="adcf3aa5", qtype="short",
    question=("행렬 [[A = mat(2,2, a,2, b,4)]]가 [[pow(A,2) - 2A - 2E = O]]를 만족시킬 때, 상수 [[a]], [[b]]에 대하여 "
              "[[a + b]]의 값을 구하시오. (단, [[E]]는 단위행렬, [[O]]는 영행렬이다.)"),
    choices=None, derived_answer="-5", figure=None, difficulty_est=3, confidence=0.9,
    note="케일리-해밀턴: a+4=2, 4a−2b=−2 → a=−2, b=−3 → a+b=−5. 빠른정답 -4와 불일치.")

# p76
add(id="bb98ff97", qtype="choice",
    question=("두 이차정사각행렬 [[A = mat(2,2, 4,-1, -2,7)]], [[B = mat(2,2, -2,1, 2,-5)]]에 대하여 행렬 [[pow(A + B, 2)]]은?"),
    choices=["[[mat(2,2, -4,0, 0,-4)]]", "[[mat(2,2, -2,0, 0,-2)]]", "[[mat(2,2, 1,0, 0,1)]]",
             "[[mat(2,2, 2,0, 0,2)]]", "[[mat(2,2, 4,0, 0,4)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="A+B=2E → (A+B)²=4E → ⑤. 빠른정답 36과 불일치.")

# p77
add(id="bf1efd87", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 2,4, -3,5)]], [[B = mat(2,2, -1,2, 3,4)]]에 대하여 [[B A - B]]는?"),
    choices=["[[mat(2,2, -9,3, 4,7)]]", "[[mat(2,2, -8,2, -5,17)]]", "[[mat(2,2, -7,4, -9,28)]]",
             "[[mat(2,2, -5,7, -8,23)]]", "[[mat(2,2, -4,5, -2,27)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="BA=(−8 6;−6 32), BA−B=(−7 4;−9 28) → ③. 빠른정답 -7과 불일치.")

# p79
add(id="1a9fd32a", qtype="choice",
    question=("두 이차정사각행렬 [[A]], [[B]]가 [[A + B = 2E]], [[A B = O]]을 만족시킬 때, 다음 중 "
              "[[pow(A,100) + pow(A,99) B + pow(A,98) pow(B,2)]] + ⋯ + [[A pow(B,99) + pow(B,100)]]과 같은 행렬은? "
              "(단, [[E]]는 단위행렬, [[O]]는 영행렬이다.)"),
    choices=["[[O]]", "[[E]]", "[[A]]", "[[pow(2,100) E]]", "[[pow(2,100) A]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="B=2E−A → BA=AB=O, A²=2A, B²=2B → 합=A¹⁰⁰+B¹⁰⁰=2⁹⁹(A+B)=2¹⁰⁰E → ④. 빠른정답 5와 불일치.")

# p80
add(id="8b77d3fe", qtype="short",
    question=("행렬 [[A = mat(2,2, -2,-1, 3,1)]]에 대하여 [[pow(A,273) mat(2,1, x, y) = mat(2,1, 1, 2)]]일 때, "
              "상수 [[x]], [[y]]에 대하여 [[x y]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="A³=E → A²⁷³=E → (x,y)=(1,2) → xy=2. 빠른정답 3과 불일치.")

# p81
add(id="44b9945d", qtype="choice",
    question=("행렬 [[A = mat(2,2, -4,-3, 7,5)]]일 때, [[E + pow(A,2) + pow(A,4) + pow(A,6)]] + ⋯ + [[pow(A,100)]]을 간단히 하면?"),
    choices=["[[E]]", "[[A]]", "[[O]]", "[[-A]]", "[[-2A]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2010년 9월 고2 문과 11번]. A²−A+E=O → A³=−E, A⁶=E; 짝수 지수 51개=17주기(E+A²+A⁴=O) → O → ③ = 빠른정답 ✓.")

# p82
add(id="ae652016", qtype="short",
    question=("행렬 [[A = mat(2,2, -2,5, -1,2)]]에 대하여 "
              "[[A mat(2,1, a, b) + pow(A,2) mat(2,1, a, b) + pow(A,3) mat(2,1, a, b)]] + ⋯ + "
              "[[pow(A,250) mat(2,1, a, b) = A mat(2,1, 3, 7)]]일 때, [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="-15", figure=None, difficulty_est=3, confidence=0.9,
    note="A²=−E → 250항 합=A−E → (A−E)(a;b)=A(3;7) → a=−13, b=−2 → −15. 빠른정답 4와 불일치.")

# p83
add(id="261f5103", qtype="choice",
    question=("행렬 [[A = mat(2,2, -2,-a, a,2)]]에 대하여 다음 보기 중 옳은 것만을 있는 대로 고른 것은? "
              "(단, [[E]]는 단위행렬이고, [[O]]는 영행렬이다.)\n<보기>\n"
              "ㄱ. [[pow(A,2) = O]]이면 [[a = pm(2)]]이다.\n"
              "ㄴ. [[pow(A,4) = E]]를 만족시키는 서로 다른 실수 [[a]]의 개수는 4이다.\n"
              "ㄷ. 자연수 [[n]]이 홀수일 때, [[pow(A,n) = E]]를 만족시키는 실수 [[a]]가 존재하지 않는다."),
    choices=CH_G5b, derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="A²=(4−a²)E → ㄱ✓, (4−a²)²=1 → a=±√3,±√5 ㄴ✓, 홀수 거듭제곱은 (4−a²)^k A≠E ㄷ✓ → ⑤. 빠른정답 2와 불일치.")

# p84
add(id="8cf0b2a7", qtype="choice",
    question=("행렬 [[A = mat(2,2, -2,3, -1,2)]]에 대하여 등식 [[pow(A,2012) mat(2,1, p, q) = mat(2,1, -2, 3)]]이 성립할 때, "
              "두 실수 [[p]], [[q]]의 합 [[p + q]]의 값은?"),
    choices=["[[-5]]", "[[-1]]", "0", "1", "5"], derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2012년 6월 고2 이과 9번/3점]. A²=E → (p,q)=(−2,3) → p+q=1 → ④. 빠른정답 3과 불일치.")

# p85
add(id="3c12748f", qtype="short",
    question=("행렬 [[A = mat(2,2, 3,7, -1,-2)]]에 대하여 행렬 [[sub(B,n)]] ([[n]]은 자연수)가 다음 조건을 만족시킬 때, "
              "행렬 [[sub(B,2029)]]의 모든 성분의 합을 구하시오.\n"
              "(가) [[sub(B,1) = -A]]\n"
              "(나) [[sub(B,2k) = pow(A,2k) sub(B,2k-1)]] ([[k]] = 1, 2, 3, ⋯)\n"
              "(다) [[sub(B,2k+1) = sub(B,2k) pow(A,2k)]] ([[k]] = 1, 2, 3, ⋯)"),
    choices=None, derived_answer="-7", figure=None, difficulty_est=4, confidence=0.85,
    note="A³=−E, A⁶=E; B₂ₖ₊₁=−A^(1+2k(k+1)), k=1014 → 지수≡1 (mod 6) → B₂₀₂₉=−A → 합 −7. 빠른정답 -15와 불일치.")

# p91
add(id="4f8a2539", qtype="short",
    question=("행렬 [[A = mat(2,2, 0,1, -1,a)]]가 [[pow(A,2) + A + E = O]]를 만족시킬 때, [[pow(A,100)]]의 모든 성분의 합을 구하시오. "
              "(단, [[a]]는 상수, [[E]]는 단위행렬, [[O]]는 영행렬이다.)"),
    choices=None, derived_answer="-1", figure=None, difficulty_est=3, confidence=0.9,
    note="a=−1, A³=E → A¹⁰⁰=A=(0 1;−1 −1) → 합 −1 = 빠른정답 ✓.")

# p92
add(id="390a6e23", qtype="choice",
    question=("이차정사각행렬 [[A]], [[B]]가 [[A + B = -E]], [[A B = E]]를 만족시킬 때, "
              "[[(A + B) + (pow(A,2) + pow(B,2))]] + ⋯ + [[(pow(A,2011) + pow(B,2011))]]을 간단히 한 것은? (단, [[E]]는 단위행렬이다.)"),
    choices=["[[-2E]]", "[[-E]]", "[[E]]", "[[2E]]", "[[3E]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2010년 6월 고2 문과 10번]. A³=B³=E, Sₙ=Aⁿ+Bⁿ: −E, −E, 2E 주기 3(합 O), 2011=3·670+1 → −E → ② = 빠른정답 ✓.")

# p96 (행렬)
add(id="867da50a", qtype="choice",
    question=("이차정사각행렬 [[A]], [[B]]에 대하여 [[A + B = E]]가 성립할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은? "
              "(단, [[E]]는 단위행렬이고 [[O]]는 영행렬이다.)\n<보기>\n"
              "ㄱ. [[(A + B)(A - B) = pow(A,2) - pow(B,2)]]\n"
              "ㄴ. [[A B = B A]]\n"
              "ㄷ. [[pow(A B, 3) = pow(A,3) pow(B,3)]]"),
    choices=CH_G5b, derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="B=E−A → AB=BA → ㄱㄴㄷ 모두 성립 → ⑤. 빠른정답 16과 불일치.")

# ───────────────────────── 이차부등식과 연립이차부등식 ─────────────────────────
# p52
add(id="d2eecdcc", qtype="choice",
    question=("최고차항의 계수가 2인 이차함수 [[f(x)]]와 최고차항의 계수가 [[-1]]인 이차함수 [[g(x)]]가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[y = f(x)]]의 그래프가 직선 [[y = x]]와 원점이 아닌 서로 다른 두 점 P, Q에서 만난다.\n"
              "(나) 함수 [[y = g(x)]]의 그래프가 직선 [[y = x]]와 한 점 P에서만 만난다.\n"
              "(다) 점 P의 [[x]]좌표는 점 Q의 [[x]]좌표보다 작고, [[seg(OP) = seg(PQ)]]이다.\n"
              "부등식 [[f(x) + g(x) >= 0]]의 해가 모든 실수일 때, 점 P의 [[x]]좌표의 최댓값은? (단, O는 원점이다.)"),
    choices=["[[1 + sqrt(3)]]", "[[2 + sqrt(3)]]", "[[3 + sqrt(3)]]", "[[4 + sqrt(3)]]", "[[5 + sqrt(3)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2024년 6월 고1 21번/4점]. P(p,p), Q(2p,2p): f+g=x²−(4p−2)x+3p² ≥0 → p²−4p+1≤0 → 최대 2+√3 → ② = 빠른정답 ✓.")

# p62
add(id="d4b694cb", qtype="choice",
    question=("이차방정식 [[a pow(x,2) + b x + c = 0]]의 두 실근을 [[alpha]], [[beta]] ([[alpha < beta]])라 하고, "
              "부등식 [[a pow(x,2) + b x + c >= 0]]의 모든 해가 [[sqrt(2) <= x < 3]]의 범위 안에 있을 때, <보기> 중 옳은 것을 모두 고른 것은?\n<보기>\n"
              "㉠ [[alpha + beta > 2 sqrt(2)]]\n㉡ [[a c > 0]]\n㉢ [[4a + c < 2b]]"),
    choices=["㉠", "㉡", "㉠, ㉡", "㉠, ㉡, ㉢", "㉡, ㉢"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="a<0, √2≤α<β<3: ㉠✓, αβ>0 → ac>0 ㉡✓, 4a+c−2b=a(2+α)(2+β)<0 ㉢✓ → ④. 빠른정답 3과 불일치.")

# p77
add(id="79f4f215", qtype="short",
    question=("[[a < b < c]]를 만족시키는 세 실수 [[a]], [[b]], [[c]]에 대하여 연립부등식 [[(x - a)(x - b) > 0]], [[(x - b)(x - c) > 0]]의 해가 "
              "[[x < 2]] 또는 [[x > 5]]일 때, 이차부등식 [[pow(x,2) + 2 a x - c <= 0]]을 만족시키는 [[x]]값의 최댓값과 최솟값의 합을 구하시오."),
    choices=None, derived_answer="-4", figure=None, difficulty_est=3, confidence=0.9,
    note="해 x<a 또는 x>c → a=2, c=5; x²+4x−5≤0 → −5≤x≤1 → 합 −4. 빠른정답 25와 불일치.")

# p78
add(id="9d2d4329", qtype="short",
    question=("연립부등식 [[pow(x,2) + a x + b >= 0]], [[pow(x,2) + c x + d <= 0]]의 해가 [[1 <= x <= 2]] 또는 [[x = -2]]일 때, "
              "연립부등식 [[pow(x,2) + b x + a <= 0]], [[pow(x,2) - d x + c >= 0]]의 해를 구하시오. (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)"),
    choices=None, derived_answer="x = 1", figure=None, difficulty_est=3, confidence=0.85,
    note="x²+ax+b=(x+2)(x−1), x²+cx+d=(x+2)(x−2) → a=1,b=−2,c=0,d=−4; (x−1)²≤0 & x²+4x≥0 → x=1. 빠른정답 5와 불일치.")

# p80 (이차부등식)
add(id="2f4b2c6f", qtype="short",
    question=("연립이차부등식 [[pow(x,2) + 5x - 6 <= 0]], [[pow(x,2) - 6 k x - 7 pow(k,2) > 0]]의 해가 존재하도록 하는 정수 [[k]]의 개수를 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.85,
    note="−6≤x≤1, (x−7k)(x+k)>0: k=0(x≠0)·k=1~5(x<−k) 가능, k≥6·k<0 불가 → 6개. 빠른정답 -4와 불일치.")

# p86
add(id="32efe69f", qtype="short",
    question=("다음 그림과 같이 [[seg(AC) = seg(BC) = 18]]인 직각이등변삼각형 ABC가 있다. "
              "빗변 AB 위의 점 P에서 변 BC와 변 AC에 내린 수선의 발을 각각 Q, R라 할 때, 직사각형 PQCR의 넓이는 "
              "두 삼각형 APR와 PBQ의 각각의 넓이보다 크다. [[seg(QC) = a]]일 때, 모든 자연수 [[a]]의 값의 합을 구하시오."),
    choices=None, derived_answer="45",
    figure=[{"fn": "unsupported", "args": {"raw": "직각이등변삼각형 ABC(∠C=90°, AC=BC=18, A 위·B 왼쪽·C 오른쪽 아래), 빗변 AB 위의 점 P, P에서 BC·AC에 내린 수선의 발 Q·R, 직사각형 PQCR, QC=a 표시"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 직각이등변삼각형+내접 직사각형 도형",
    note="PQ=BQ=18−a, PR=AR=a: a(18−a)>a²/2 → a<12, a(18−a)>(18−a)²/2 → a>6 → a=7~11 합 45. 빠른정답 4와 불일치.")

# p96 (이차부등식)
add(id="c4ec901c", qtype="choice",
    question=("이차방정식 [[a pow(x,2) + b x + c = 0]]에서 [[a > 0]], [[b > 0]], [[pow(b,2) - 4 a c > 0]]일 때, 다음 설명 중 옳은 것은?"),
    choices=["두 근은 모두 음이다.", "음근을 가질 수 없다.", "적어도 한 개의 음근을 갖는다.", "두 근은 모두 양이다.", "양근 한 개, 음근 한 개를 갖는다."],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="서로 다른 두 실근, 합 −b/a<0 → 적어도 하나는 음수 → ③. 빠른정답 2와 불일치.")

# ───────────────────────── 미지수가 1개인 연립일차부등식 ─────────────────────────
# p21
add(id="7f6f4ce5", qtype="choice",
    question=("부등식 [[(a + b) x + (2a - b) > 0]]의 해가 [[x < -1]]일 때, 부등식 [[a x + b > 0]]의 해를 구하면?"),
    choices=["[[x < -frac(1,2)]]", "[[x < -frac(1,3)]]", "[[x > -frac(1,2)]]", "[[x > -frac(1,3)]]", "[[x > -1]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="a+b<0, a=2b → b<0; 2bx+b>0 → x<−1/2 → ① = 빠른정답 ✓.")

# p37
add(id="2f4756f0", qtype="short",
    question=("[[3x - 2y = 15]]일 때, 부등식 [[2x - 2 < y + 4 <= 3x + 6]]을 만족시키는 순서쌍 [[point(x, y)]] 중 "
              "[[x]], [[y]]가 모두 정수인 것은 몇 쌍인지 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.85,
    note="y=(3x−15)/2 대입 → −19/3≤x<−3, x 홀수 → x=−5, y=−15 1쌍. 빠른정답 mixed(1,1,2)와 불일치.")

# p39
add(id="9f78d3e8", qtype="choice",
    question=("[[a]], [[b]], [[c]], [[d]]는 정수이고, [[a < 2b]], [[b < 3c]], [[c < 4d]], [[d < 100]]을 만족시킬 때, [[a]]의 최댓값은?"),
    choices=["2367", "2375", "2391", "2399", "2400"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="d≤99, c≤395, b≤1184, a≤2367 → ①. 빠른정답 4와 불일치.")

# p53
add(id="65f47503", qtype="choice",
    question=("연립부등식 [[6x + 4 >= 10]], [[3x + 5 <= 2]]의 해를 구하시오."),
    choices=["[[x = 1]]", "[[x = 2]]", "해가 없다.", "[[x <= 1]]", "[[x <= 2]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="x≥1, x≤−1 → 해 없음 → ③ = 빠른정답 ✓.")

# p64
add(id="10af0e53", qtype="choice",
    question=("부등식 [[a + 7 <= a x + b <= 4b + 2a]]의 해가 [[2 <= x <= 8]]일 때, [[a]], [[b]]의 값을 각각 구하면?"),
    choices=["[[a = -2]], [[b = -1]]", "[[a = -1]], [[b = 0]]", "[[a = frac(1,3)]], [[b = frac(7,3)]]",
             "[[a = frac(7,3)]], [[b = frac(14,3)]]", "[[a = 2]], [[b = -1]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="a>0: b=7−a, b=2a → a=7/3, b=14/3 → ④ = 빠른정답 ✓.")

# p68
add(id="609c79b1", qtype="short",
    question=("연립부등식 [[a x + 3 <= -x - 3a]], [[b x + 8 < 2 a x + 4b]]의 해가 [[x < frac(12,7)]]일 때, "
              "실수 [[a]], [[b]]에 대하여 [[b - a]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.9,
    note="첫 부등식이 항상 성립해야 → a=−1; (b+2)x<4(b−2) → 4(b−2)/(b+2)=12/7 → b=5 → b−a=6 = 빠른정답 ✓.")

# p69
add(id="c98da5d7", qtype="choice",
    question=("다음 그림은 연립부등식 [[3 a x - b < a x + 2b]], [[4 c x + 3d >= 2 c x + d]]의 해를 수직선 위에 나타낸 것이다. "
              "이때 연립부등식 [[a x + 3b > 0]], [[c x - d <= 0]]의 해는? (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)"),
    choices=["[[-4 < x <= 4]]", "[[-3 < x <= 3]]", "[[-3 < x <= 4]]", "[[-2 < x <= 3]]", "[[-2 < x <= 4]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "수직선: −4(닫힌 점)에서 오른쪽으로 뻗는 범위와 2(열린 점)에서 왼쪽으로 뻗는 범위가 겹침(해 −4 ≤ x < 2)"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 수직선 위 연립부등식 해 표시",
    note="x<2 → a>0, 3b=4a; x≥−4 → c>0, d=4c; ax+4a>0 → x>−4, cx≤4c → x≤4 → ①. 빠른정답 -10과 불일치.")

# p79 (연립일차부등식)
add(id="a009f820", qtype="short",
    question=("연립방정식 [[2x + a y = 6]], [[-3 a x + 2y = -2]]에서 [[x > 0]], [[y > 0]]이기 위한 자연수 [[a]]의 최솟값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.8,
    note="x=(2a+12)/(3a²+4)>0, y=(18a−4)/(3a²+4)>0 → 모든 자연수 a에서 성립(a=1: x=y=2) → 최솟값 1. 빠른정답 5와 불일치(문항 자체가 부자연스러움).")

# ───────────────────────── 삼차방정식과 사차방정식의 풀이 ─────────────────────────
# p27
add(id="f7856a0a", qtype="choice",
    question=("다음은 자연수 [[n]]에 대하여 [[x]]에 대한 사차방정식 [[4 pow(x,4) - 4(n + 2) pow(x,2) + pow(n - 2, 2) = 0]]이 "
              "서로 다른 네 개의 정수해를 갖도록 하는 20 이하의 모든 [[n]]의 값을 구하는 과정이다.\n"
              "[[P(x) = 4 pow(x,4) - 4(n + 2) pow(x,2) + pow(n - 2, 2)]]이라 하자.\n"
              "[[pow(x,2) = X]]라 하면 주어진 방정식 [[P(x) = 0]]은\n"
              "[[4 pow(X,2) - 4(n + 2) X + pow(n - 2, 2) = 0]]이고\n"
              "근의 공식에 의하여\n"
              "[[X]] = ( [[n + 2]] ± √((가)) ) / 2 이다.\n"
              "따라서\n"
              "[[X = pow(sqrt(frac(n,2)) + 1, 2)]] 또는 [[X = pow(sqrt(frac(n,2)) - 1, 2)]]에서\n"
              "[[x = sqrt(frac(n,2)) + 1]] 또는 [[x = -sqrt(frac(n,2)) - 1]] 또는\n"
              "[[x = sqrt(frac(n,2)) - 1]] 또는 [[x = -sqrt(frac(n,2)) + 1]]이다.\n"
              "방정식 [[P(x) = 0]]이 정수해를 갖기 위해서는\n"
              "[[sqrt(frac(n,2))]] 이 자연수가 되어야 한다.\n"
              "따라서 자연수 [[n]]에 대하여 방정식 [[P(x) = 0]]이 서로 다른 네 개의 정수해를 갖도록 하는 20 이하의 모든 [[n]]의 값은 (나), (다) 이다.\n"
              "위의 (가)에 알맞은 식을 [[f(n)]]이라 하고, (나), (다)에 알맞은 수를 각각 [[a]], [[b]]라 할 때, [[f(b - a)]]의 값은? (단, [[a < b]])"),
    choices=["48", "56", "64", "72", "80"], derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2023년 6월 고1 18번/4점]. (가)=8n, √(n/2) 자연수·네 근 서로 다름 → n=8, 18 → f(10)=80 → ⑤ = 빠른정답 ✓.")

# p31
add(id="5878b3c1", qtype="short",
    question=("[[x]]에 대한 삼차방정식 [[pow(x,3) + a x + b = 0]]의 세 근이 [[-3]], 5, [[alpha]]일 때, "
              "[[abs(a) + abs(b) + abs(alpha)]]의 값을 구하시오. (단, [[a]], [[b]]는 상수)"),
    choices=None, derived_answer="51", figure=None, difficulty_est=2, confidence=0.9,
    note="근의 합 0 → α=−2, a=−19, b=−30 → 19+30+2=51 = 빠른정답 ✓.")

# p36
add(id="05a1c67e", qtype="choice",
    question=("다음은 [[x]]에 대한 방정식 [[(pow(x,2) + a x + a)(pow(x,2) + 2x + a) = 0]]의 근 중 서로 다른 허근의 개수가 2이기 위한 "
              "실수 [[a]]의 값의 범위를 구하는 과정이다.\n"
              "(ⅰ) [[a = 2]]인 경우\n"
              "주어진 방정식은 [[pow(pow(x,2) + 2x + 2, 2) = 0]]이다.\n"
              "이때 방정식 [[pow(x,2) + 2x + 2 = 0]]의 근은\n"
              "[[x]] = [[-1]] ± √((가)) [[i]] (단, [[i = sqrt(-1)]])이므로\n"
              "방정식 [[pow(pow(x,2) + 2x + 2, 2) = 0]]의 서로 다른 허근의 개수는 2이다.\n"
              "(ⅱ) [[a != 2]]인 경우\n"
              "방정식 [[pow(x,2) + a x + a = 0]]의 근은\n"
              "[[x]] = ( [[-a]] ± √((나)) ) / 2\n"
              "(a) (나) < 0일 때\n"
              "방정식 [[pow(x,2) + 2x + a = 0]]은 실근을 가져야 하므로 실수 [[a]]의 값의 범위는\n"
              "[[0 < a <= 1]]\n"
              "(b) (나) ≥ 0일 때\n"
              "방정식 [[pow(x,2) + 2x + a = 0]]은 허근을 가져야 하므로 실수 [[a]]의 값의 범위는\n"
              "[[a]] ≥ (다)\n"
              "(ⅰ), (ⅱ)에 의하여\n"
              "방정식 [[(pow(x,2) + a x + a)(pow(x,2) + 2x + a) = 0]]의 근 중 서로 다른 허근의 개수가 2이기 위한 실수 [[a]]의 값의 범위는\n"
              "[[0 < a <= 1]] 또는 [[a = 2]] 또는 [[a]] ≥ (다) 이다.\n"
              "위의 (가), (다)에 알맞은 수를 각각 [[p]], [[q]]라 하고, (나)에 알맞은 식을 [[f(a)]]라 할 때, [[p + q + f(5)]]의 값은?"),
    choices=["8", "9", "10", "11", "12"], derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2019년 6월 고1 19번 변형]. (가)=1, (나)=a²−4a, (다)=4 → 1+4+5=10 → ③ = 빠른정답 ✓.")

# p44
add(id="64774e69", qtype="choice",
    question=("다음은 [[x]]에 대한 방정식\n[[(pow(x,2) + a x + a)(pow(x,2) + x + a) = 0]]\n"
              "의 근 중 서로 다른 허근의 개수가 2이기 위한 실수 [[a]]의 값의 범위를 구하는 과정이다.\n"
              "(ⅰ) [[a = 1]]일 때,\n"
              "주어진 방정식은 [[pow(pow(x,2) + x + 1, 2) = 0]]이다.\n"
              "이때 방정식 [[pow(x,2) + x + 1 = 0]]의 근은\n"
              "[[x]] = ( [[-1]] ± √((가)) [[i]] ) / 2 (단, [[i = sqrt(-1)]])\n"
              "이므로 방정식 [[pow(pow(x,2) + x + 1, 2) = 0]]의 서로 다른 허근의 개수는 2이다.\n"
              "(ⅱ) [[a != 1]]일 때,\n"
              "방정식 [[pow(x,2) + a x + a = 0]]의 근은\n"
              "[[x]] = ( [[-a]] ± √((나)) ) / 2\n"
              "(a) (나) < 0일 때,\n"
              "방정식 [[pow(x,2) + x + a = 0]]은 실근을 가져야 하므로 실수 [[a]]의 값의 범위는\n"
              "[[0 < a <= frac(1,4)]]\n"
              "(b) (나) ≥ 0일 때,\n"
              "방정식 [[pow(x,2) + x + a = 0]]은 허근을 가져야 하므로 실수 [[a]]의 값의 범위는\n"
              "[[a]] ≥ (다)\n"
              "따라서 (ⅰ)과 (ⅱ)에 의하여\n"
              "방정식 [[(pow(x,2) + a x + a)(pow(x,2) + x + a) = 0]]의 근 중 서로 다른 허근의 개수가 2이기 위한 실수 [[a]]의 값의 범위는\n"
              "[[0 < a <= frac(1,4)]] 또는 [[a = 1]] 또는 [[a]] ≥ (다)\n이다.\n"
              "위의 (가), (다)에 알맞은 수를 각각 [[p]], [[q]]라 하고, (나)에 알맞은 식을 [[f(a)]]라 할 때, [[p + q + f(5)]]의 값은?"),
    choices=["8", "9", "10", "11", "12"], derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2019년 6월 고1 19번/4점]. (가)=3, (나)=a²−4a, (다)=4 → 3+4+5=12 → ⑤. 빠른정답 15와 불일치.")

# p93
add(id="f45d4333", qtype="choice",
    question=("양수 [[a]]에 대하여 [[seg(AB) = 7 pow(a,2) + 60a + 117]], [[seg(AD) = seg(AE) = a]]인 직육면체 ABCD-EFGH가 있다. "
              "선분 AB를 [[ratio(3, a)]]로 내분하는 점을 P, 선분 DC를 [[ratio(3, a)]]로 내분하는 점을 Q라 하자. "
              "직육면체 ABCD-EFGH에서 단면 PFGQ가 생기도록 삼각기둥 PFB-QGC를 잘라 내었다. "
              "사각기둥 AEFP-DHGQ의 부피를 [[sub(V,1)]], 삼각기둥 PFB-QGC의 부피를 [[sub(V,2)]]라 하자. "
              "[[sub(V,1) - sub(V,2) = 300]]일 때, 선분 AP의 길이는?"),
    choices=["143", "144", "145", "146", "147"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체 ABCD-EFGH(윗면 ABCD, 아랫면 EFGH, AB가 긴 모서리), AB 위 점 P·DC 위 점 Q, 단면 PFGQ로 잘라 사각기둥 AEFP-DHGQ(V₁)와 삼각기둥 PFB-QGC(V₂)로 분리한 그림"}}],
    difficulty_est=4, confidence=0.8, needs_review="도형 표현 불가: 직육면체 절단 입체도형",
    note="출처 [2024년 10월 고1 20번 변형]. AB=(a+3)(7a+39), AP=21a+117; V₁−V₂=a²·AP=300 → 7a³+39a²−100=0 → a=10/7 → AP=147 → ⑤. 빠른정답 -3과 불일치.")

# p96 (삼차)
add(id="59c7b235", qtype="short",
    question=("그림과 같이 원 밖의 점 P에서 원에 그은 접선의 접점을 A라 하고, 점 P를 지나는 직선이 원과 만나는 두 점을 B, C라 하자.\n"
              "[[seg(PB) = pow(x,2) - x + 4]], [[seg(BC) = 2x]], [[seg(PA) = 2 sqrt(6) x]]가 되도록 하는 모든 [[x]]의 값의 합을 구하시오."),
    choices=None, derived_answer="5",
    figure=[{"fn": "unsupported", "args": {"raw": "원과 원 밖의 점 P(왼쪽), 접점 A(원 아래쪽), P를 지나는 할선이 원과 만나는 점 B(가까운 쪽)·C(먼 쪽)"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 원·접선·할선 도형",
    note="출처 [2012년 9월 고1 27번/4점]. PA²=PB·PC → (x²+4)²−x²=24x² → x⁴−17x²+16=0 → x=1, 4 → 합 5 = 빠른정답 ✓.")

# ───────────────────────── 순열 ─────────────────────────
# p6
add(id="0bf422bc", qtype="short",
    question=("다음 □ 안에 알맞은 수를 구하시오.\n[[perm(7,4)]] = [[fact(7)]] / (□)!"),
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="₇P₄=7!/3! → 3. 빠른정답 5와 불일치.")

# ───────────────────────── 이차방정식과 이차함수의 관계 ─────────────────────────
# p7
add(id="2c88aff9", qtype="short",
    question=("이차함수 [[y = -pow(x,2) - (3 - a) x + 2 pow(b,2) - b]]의 그래프와 [[x]]축의 두 교점의 [[x]]좌표가 [[-2]], 3일 때, "
              "양수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="근의 합 a−3=1 → a=4, 곱 −(2b²−b)=−6 → b=2 → 6 = 빠른정답 ✓.")

# p16
add(id="3b5932e4", qtype="short",
    question=("이차함수 [[y = pow(x,2) + a x + a]]가 [[x]]축과 두 점 A, B에서 만날 때, [[seg(AB) = 2 sqrt(3)]]이 되도록 하는 양수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="(α−β)²=a²−4a=12 → a=6 = 빠른정답 ✓.")

# p18
add(id="d6cbe200", qtype="short",
    question=("이차함수 [[y = a pow(x,2) + b x + c]]의 그래프는 꼭짓점의 좌표가 [[point(-2, -1)]]이고, [[x]]축과 두 점 P, Q에서 만난다. "
              "[[seg(PQ) = 4]]일 때, 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="frac(5,4)", figure=None, difficulty_est=2, confidence=0.9,
    note="근 −4, 0 → y=(1/4)(x+2)²−1=x²/4+x → a+b+c=5/4 = 빠른정답 ✓.")

# p27 (이차함수)
add(id="ab0703a4", qtype="short",
    question=("다음 그림과 같이 이차함수 [[y = f(x)]]의 그래프가 [[x]]축과 서로 다른 두 점 [[point(alpha, 0)]], [[point(beta, 0)]]에서 만나고 "
              "[[alpha + beta = 7]]일 때, 방정식 [[f(3x - 1) = 0]]의 모든 실근의 합을 구하시오."),
    choices=None, derived_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": "위로 볼록한 이차함수 y=f(x)의 그래프, x축과의 교점 α(원점 왼쪽)·β(원점 오른쪽)"}}],
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 이차함수 그래프",
    note="3x−1=α, β → 근의 합 (α+β+2)/3=3 = 빠른정답 ✓.")

# p47 (이차함수)
add(id="72dc3aaa", qtype="choice",
    question=("이차항의 계수가 1인 이차함수 [[f(x)]]가 다음 조건을 모두 만족시킨다. 함수 [[y = f(x)]]의 그래프와 [[x]]축이 만나는 점의 좌표를 "
              "[[point(a, 0)]], [[point(b, 0)]]이라 할 때, 상수 [[a]], [[b]]에 대하여 [[pow(a,2) + pow(b,2)]]의 값은?\n"
              "(가) 모든 실수 [[x]]에 대하여 [[f(5 - x) = f(5 + x)]]\n"
              "(나) 이차방정식 [[f(x) = -4]]는 중근을 갖는다."),
    choices=["50", "53", "58", "65", "74"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="f(x)=(x−5)²−4 → 근 3, 7 → 9+49=58 → ③ = 빠른정답 ✓.")

# p56 (이차함수)
add(id="566a1a0b", qtype="short",
    question=("이차항의 계수가 1인 이차함수 [[f(x)]]가 다음 조건을 모두 만족시킨다. 함수 [[y = f(x)]]의 그래프와 [[x]]축이 만나는 점의 좌표를 "
              "[[point(a, 0)]], [[point(b, 0)]]이라 할 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.\n"
              "(가) 모든 실수 [[x]]에 대하여 [[f(4 + x) = f(4 - x)]]\n"
              "(나) 이차방정식 [[f(x) = -1]]은 중근을 갖는다."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="f(x)=(x−4)²−1 → 근 3, 5 → 합 8. 빠른정답 3과 불일치.")

# p59 (이차함수)
add(id="6d409202", qtype="choice",
    question=("이차함수 [[y = 2 pow(x,2)]]의 그래프 위의 두 점 A[[point(-t, 2 pow(t,2))]], B[[point(t, 2 pow(t,2))]] ([[t > 0]], [[t != 1]])에 대하여 "
              "선분 AB를 한 변으로 하고 두 점 C, D를 꼭짓점으로 갖는 정사각형 ACDB가 있다. 삼각형 AOB의 넓이를 [[sub(S,1)]], "
              "삼각형 COD의 넓이를 [[sub(S,2)]]라 하자. [[ratio(sub(S,1), sub(S,2)) = ratio(4, 1)]]을 만족시키는 모든 실수 [[t]]의 값의 합은? (단, O는 원점이다.)"),
    choices=["[[frac(31,15)]]", "[[frac(32,15)]]", "[[frac(11,5)]]", "[[frac(34,15)]]", "[[frac(7,3)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.8,
    note="출처 [2026년 6월 고1 19번 변형]. S₁=2t³, S₂=2t²|t±1|; S₁=4S₂ → t=4|t−1| → t=4/3, 4/5 (위쪽 정사각형은 불가) → 합 32/15 → ②. 빠른정답 8과 불일치.")

# ───────────────────────── 조합 ─────────────────────────
# p17
add(id="f7805633", qtype="short",
    question=("다음은 음이 아닌 정수 [[n]]에 대하여\n[[comb(n + 4, n + 1) - comb(n + 4, n)]] = (다) · [[comb(n + 5, 4)]]\n가 성립함을 증명하는 과정이다.\n"
              "[[comb(n + 4, n + 1) - comb(n + 4, n)]]\n"
              "= (가) · { [[frac(1, fact(n + 1) fact(3)) - frac(1, fact(n) fact(4))]] }\n"
              "= (가) · (나) / ( [[fact(n + 1) fact(4)]] )\n"
              "= (다) · [[comb(n + 5, 4)]]\n"
              "위의 과정에서 (가), (나), (다)에 알맞은 식을 각각 [[f(n)]], [[g(n)]], [[h(n)]]이라 할 때, [[frac(f(1), g(1) h(2))]]의 값을 구하시오."),
    choices=None, derived_answer="420", figure=None, difficulty_est=3, confidence=0.9,
    note="(가)=(n+4)!, (나)=3−n, (다)=(3−n)/(n+5) → f(1)=120, g(1)=2, h(2)=1/7 → 420 = 빠른정답 ✓.")

# p19
add(id="e801c34d", qtype="choice",
    question=("다음은 자연수 [[n]]에 대하여\n[[comb(n + 2, n) - comb(n + 2, n - 1)]] = (다) · [[comb(n + 3, 3)]]이 성립함을 증명하는 과정이다.\n"
              "[[comb(n + 2, n) - comb(n + 2, n - 1)]]\n"
              "= ((가))! { [[frac(1, fact(n) fact(2)) - frac(1, fact(n - 1) fact(3))]] }\n"
              "= ((가))! · (나) / ( [[fact(n) fact(3)]] )\n"
              "= (다) · [[frac(fact(n + 3), fact(n) fact(3))]]\n"
              "= (다) · [[comb(n + 3, 3)]]\n"
              "위의 과정에서 (가), (나), (다)에 알맞은 식을 각각 [[f(n)]], [[g(n)]], [[h(n)]]이라 할 때, [[frac(f(3) + g(2), h(1))]]의 값은?"),
    choices=["12", "14", "16", "18", "20"], derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="(가)=n+2, (나)=3−n, (다)=(3−n)/(n+3) → f(3)=5, g(2)=1, h(1)=1/2 → 12 → ①. 빠른정답 3과 불일치.")

# p30
add(id="7b9fb858", qtype="choice",
    question=("어느 학교에서는 '확률과 통계', '미적분', '기하'의 수학 과목 3개와 '물리학Ⅱ', '화학Ⅱ', '생명과학Ⅱ', '지구과학Ⅱ'의 과학 과목 4개를 "
              "선택 교육 과정으로 운영한다. 두 학생 A, B가 이 7개의 과목 중에서 다음 조건을 만족시키도록 과목을 선택하려고 한다.\n"
              "· A, B는 각자 1개 이상의 수학 과목을 포함한 3개의 과목을 선택한다.\n"
              "· A가 선택하는 3개의 과목과 B가 선택하는 3개의 과목 중에서 서로 일치하는 과목의 개수는 1이다.\n"
              "다음은 A, B가 과목을 선택하는 경우의 수를 구하는 과정이다.\n"
              "A, B가 선택하는 과목 중에서 서로 일치하는 과목이 수학 과목인 경우와 과학 과목인 경우로 나누어 구할 수 있다.\n"
              "(ⅰ) 서로 일치하는 과목이 수학 과목일 때\n"
              "3개의 수학 과목 중에서 1개를 선택하는 경우의 수는 [[comb(3,1) = 3]]\n"
              "위의 각 경우에 대하여 나머지 6개의 과목 중에서 A가 2개를 선택하고, 나머지 4개의 과목 중에서 B가 2개를 선택하는 경우의 수는 (가)\n"
              "이때의 경우의 수는 3 · (가)\n"
              "(ⅱ) 서로 일치하는 과목이 과학 과목일 때\n"
              "4개의 과학 과목 중에서 1개를 선택하는 경우의 수는 [[comb(4,1) = 4]]\n"
              "위의 각 경우에 대하여 나머지 6개의 과목 중에서 A, B는 수학 과목을 1개 이상 선택해야 하므로 다음 두 가지 경우로 나눌 수 있다.\n"
              "(a) A, B 모두 수학 과목 1개와 과학 과목 1개를 선택하는 경우의 수는\n"
              "[[(comb(3,1) × comb(3,1)) × (comb(2,1) × comb(2,1)) = 36]]\n"
              "(b) A, B 중 한 명은 수학 과목 2개를 선택하고, 다른 한 명은 수학 과목 1개와 과학 과목 1개를 선택하는 경우의 수는 (나)\n"
              "이때의 경우의 수는 4 · (36 + (나))\n"
              "(ⅰ), (ⅱ)에 의하여 구하는 경우의 수는 3 · (가) + 4 · (36 + (나))이다.\n"
              "위의 (가), (나)에 알맞은 수를 각각 [[p]], [[q]]라 할 때, [[p + q]]의 값은?"),
    choices=["102", "108", "114", "120", "126"], derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2021년 3월 고2 18번/4점]. (가)=₆C₂·₄C₂=90, (나)=2·₃C₂·(1·3)=18 → 108 → ②. 빠른정답 16과 불일치.")

# ───────────────────────── 미지수가 2개인 연립이차방정식 ─────────────────────────
# p4
add(id="6bb300d7", qtype="choice",
    question=("연립방정식 [[x - y - 2 = 0]], [[pow(x,2) - x y + 5y = 4]]의 해를 [[x = alpha]], [[y = beta]]라 할 때, [[alpha + beta]]의 값은?"),
    choices=["1", "2", "3", "4", "5"], derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 9월 고1 8번 변형]. x=y+2 대입 → 7y+4=4 → y=0, x=2 → 2 → ② (빠른정답 없음).")

# p5
add(id="727f3d15", qtype="choice",
    question=("연립방정식 [[2x - y = 1]], [[5 pow(x,2) - pow(y,2) = -5]]의 해를 [[x = alpha]], [[y = beta]]라 할 때, [[alpha - beta]]의 값은?"),
    choices=["1", "2", "3", "4", "5"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2023년 9월 고1 9번/3점]. y=2x−1 대입 → (x+2)²=0 → x=−2, y=−5 → α−β=3 → ③ (빠른정답 없음).")

# p13
add(id="add1643e", qtype="choice",
    question=("연립방정식 [[y = 3x - 4]], [[6x + pow(y,2) = 7]]의 해를 [[x = a]], [[y = b]]라 할 때, [[3a + 2b]]의 값은?"),
    choices=["[[-2]]", "[[-1]]", "0", "1", "2"], derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2017년 9월 고1 4번 변형]. 9x²−18x+9=0 → x=1, y=−1 → 3−2=1 → ④ = 빠른정답 ✓.")

# p15
add(id="6816a2bc", qtype="choice",
    question=("연립방정식 [[3x - y = 7]], [[4 pow(x,2) - x y - 5y = 19]]의 해를 [[x = alpha]], [[y = beta]]라 할 때, [[alpha + beta]]의 값은?"),
    choices=["6", "7", "8", "9", "10"], derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2025년 9월 고1 10번 변형]. y=3x−7 대입 → (x−4)²=0 → x=4, y=5 → 9 → ④. 빠른정답 19와 불일치.")

# p18 (연립이차)
add(id="fef4ad24", qtype="choice",
    question=("연립방정식 [[pow(x,2) - 3 x y + 2 pow(y,2) = 0]], [[pow(x,2) - pow(y,2) = 9]]의 해를 "
              "[[x = sub(alpha,1)]], [[y = sub(beta,1)]] 또는 [[x = sub(alpha,2)]], [[y = sub(beta,2)]]라 하자. "
              "[[sub(alpha,1) < sub(alpha,2)]]일 때, [[sub(beta,1) - sub(beta,2)]]의 값은?"),
    choices=["[[-2 sqrt(3)]]", "[[-2 sqrt(2)]]", "[[2 sqrt(2)]]", "[[2 sqrt(3)]]", "4"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2020년 3월 고2 13번/3점]. (x−y)(x−2y)=0, x=2y → y=±√3 → (−2√3,−√3),(2√3,√3) → β₁−β₂=−2√3 → ① (빠른정답 없음).")

# p22
add(id="5a678aab", qtype="choice",
    question=("다음 중 연립방정식 [[pow(x,2) - pow(y,2) = 0]], [[pow(x,2) - x y + 2 pow(y,2) = 8]]의 해가 아닌 것은?"),
    choices=["[[x = -2]], [[y = -2]]", "[[x = 2]], [[y = 2]]", "[[x = -sqrt(2)]], [[y = sqrt(2)]]",
             "[[x = sqrt(2)]], [[y = -sqrt(2)]]", "[[x = sqrt(2) i]], [[y = -sqrt(2) i]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="x=y → x=±2, x=−y → x=±√2 → 해는 ①~④, ⑤는 아님. 빠른정답 3과 불일치.")

# p27 (연립이차)
add(id="4a44d38f", qtype="choice",
    question=("다음 중 연립방정식 [[pow(x,2) - pow(y,2) = 0]], [[3 pow(x,2) - 4 x y + 3 pow(y,2) = 10]]의 해가 아닌 것은?"),
    choices=["[[x = -1]], [[y = -1]]", "[[x = -1]], [[y = 1]]", "[[x = sqrt(5)]], [[y = sqrt(5)]]",
             "[[x = -sqrt(5)]], [[y = -sqrt(5)]]", "[[x = 1]], [[y = -1]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="x=y → x=±√5, x=−y → x=±1 → (−1,−1)은 해가 아님 → ① (빠른정답 없음).")

# p29
add(id="92bbd1e9", qtype="choice",
    question=("다음 중 연립방정식 [[pow(x,2) + x y - 2 pow(y,2) = 0]], [[pow(x,2) + pow(y,2) = 25]]의 해가 아닌 것은?"),
    choices=["[[x = 2 sqrt(5)]], [[y = -sqrt(5)]]", "[[x = -2 sqrt(5)]], [[y = sqrt(5)]]",
             "[[x = frac(5 sqrt(2), 2)]], [[y = frac(5 sqrt(2), 2)]]",
             "[[x = -frac(5 sqrt(2), 2)]], [[y = frac(5 sqrt(2), 2)]]",
             "[[x = -frac(5 sqrt(2), 2)]], [[y = -frac(5 sqrt(2), 2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(x+2y)(x−y)=0: x=−2y → (±2√5, ∓√5), x=y → (±5√2/2, ±5√2/2) → ④는 해가 아님 (빠른정답 없음).")

# p31 (연립이차)
add(id="4ef8ff8a", qtype="short",
    question=("연립방정식 [[pow(x,2) - 4 pow(y,2) = 0]], [[pow(x,2) - x y + 2 pow(y,2) = 64]]의 해를 [[x = alpha]], [[y = beta]]라 할 때, "
              "[[alpha + beta]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 하자. 이때 [[M - m]]의 값을 구하시오."),
    choices=None, derived_answer="24", figure=None, difficulty_est=3, confidence=0.9,
    note="x=2y → (±8, ±4) 합 ±12; x=−2y → 합 ±2√2 → M−m=24 = 빠른정답 ✓.")

# p35
add(id="dca79e7b", qtype="short",
    question=("연립방정식 [[x y + 2x + 2y = -4]], [[pow(x,2) + pow(y,2) = 13]]의 해를 [[x = alpha]], [[y = beta]]라 할 때, "
              "[[abs(alpha - beta)]]의 최솟값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.9,
    note="s=x+y, p=xy: p=−4−2s, s²−2p=13 → s=1(p=−6: |α−β|=5), s=−5(p=6: |α−β|=1) → 최솟값 1 (빠른정답 없음).")

# p36
add(id="39d945e6", qtype="short",
    question=("연립방정식 [[-x y + x + y = 1]], [[pow(x,2) + 3 x y + pow(y,2) = 19]]의 해를 [[x = alpha]], [[y = beta]]라 할 때, "
              "[[abs(alpha - beta)]]의 최댓값을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.9,
    note="p=s−1, s²+p=19 → s=4(p=3: |α−β|=2), s=−5(p=−6: |α−β|=7) → 최댓값 7 (빠른정답 없음).")

# p38
add(id="aba30277", qtype="choice",
    question=("연립방정식 [[x y + x + y = 5]], [[pow(x,2) + x y + pow(y,2) = 7]]을 만족하는 순서쌍 [[point(x, y)]]의 개수는?"),
    choices=["0", "1", "2", "3", "4"], derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    note="s+p=5, s²−p=7 → s=3(p=2: (1,2),(2,1)), s=−4(p=9: 허근) → 실수 순서쌍 2개 → ③ (허수 해 포함 시 4개). 빠른정답 1과 불일치.")

# p39
add(id="ed7b6638", qtype="short",
    question=("연립방정식 [[x + y + x y = -7]], [[x + y - x y = 13]]의 해를 [[x = alpha]], [[y = beta]]라 할 때, "
              "[[pow(alpha,2) + pow(beta,2)]]의 값을 구하시오."),
    choices=None, derived_answer="29", figure=None, difficulty_est=2, confidence=0.9,
    note="x+y=3, xy=−10 → α²+β²=9+20=29. 빠른정답 7과 불일치.")
