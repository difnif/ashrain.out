# -*- coding: utf-8 -*-
# esc_sonnet_h3-3_6of6 — 이미지 기준 전사 (38 항목 / 32쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_G = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ───────────── 벡터의 실수배 ─────────────
# p86
add(id="1b1958b8", qtype="short",
    question=("다음 그림과 같이 삼각형 ABC의 무게중심 G를 지나는 직선이 두 변 AB, AC와 만나는 점을 각각 P, Q라 하자. "
              "[[ratio(abs(vec(AP)), abs(vec(PB))) = ratio(3, 1)]]일 때, [[2 vec(AQ) = k vec(QC)]]를 만족시키는 "
              "실수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC, 변 AB 위의 점 P와 변 AC 위의 점 Q를 잇는 직선이 무게중심 G(점 표시)를 지남"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 ABC와 무게중심 G를 지나는 직선 PQ",
    note="AP=(3/4)AB, G∈PQ ⇒ AQ=(3/5)AC, QC=(2/5)AC ⇒ 2AQ=3QC ⇒ k=3.")

# p87
add(id="17a0c50e", qtype="short",
    question=("다음 그림과 같이 삼각형 ABC의 무게중심 G를 지나는 직선이 두 변 AB, AC와 만나는 점을 각각 P, Q라 하자. "
              "[[ratio(abs(vec(AP)), abs(vec(PB))) = ratio(4, 1)]]일 때, [[vec(AQ) = k vec(QC)]]를 만족시키는 "
              "실수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="frac(4,3)",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC, 변 AB 위의 점 P와 변 AC 위의 점 Q를 잇는 직선이 무게중심 G(점 표시)를 지남"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 ABC와 무게중심 G를 지나는 직선 PQ",
    note="AP=(4/5)AB, 1/m+1/n=3 ⇒ AQ=(4/7)AC, QC=(3/7)AC ⇒ k=4/3 (빠른정답 1/3과 불일치).")

# p97
add(id="13d70a3d", qtype="choice",
    question=("정혁이와 준식이가 같은 지점에서 동시에 출발하여 정혁이는 북쪽으로 [[3]]km/h의 속력으로 걸어가고, "
              "준식이는 동쪽으로 [[4]]km/h의 속력으로 걸어가고 있다. 정혁이가 걸어가면서 준식이를 바라볼 때 느끼는 준식이의 속력은?"),
    choices=["[[3]]km/h", "[[4]]km/h", "[[5]]km/h", "[[6]]km/h", "[[7]]km/h"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="상대속도 (4, -3) 크기 5 ⇒ ③.")

# ───────────── 벡터의 내적 ─────────────
# p3
add(id="219a89d7", qtype="choice",
    question=("그림과 같이 한 변의 길이가 1인 정사각형 ABCD에서 "
              "[[dot((vec(AB) + k vec(BC)), (vec(AC) + 3k vec(CD))) = 0]]일 때, 실수 [[k]]의 값은?"),
    choices=["[[1]]", "[[frac(1,2)]]", "[[frac(1,3)]]", "[[frac(1,4)]]", "[[frac(1,5)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD (A 좌상, D 우상, B 좌하, C 우하)"}}],
    difficulty_est=2, confidence=0.85,
    note="출처 [2023년 6월 고3 기하 25번/3점]. 좌표화하면 k+1-3k=0 ⇒ k=1/2 ⇒ ②.")

# p10
add(id="e2a6c868", qtype="choice",
    question=("다음 그림과 같이 삼각형 ABC에 대하여 꼭짓점 C에서 선분 AB에 내린 수선의 발을 H라 하자. "
              "삼각형 ABC가 다음 조건을 모두 만족시킬 때, [[dot(vec(CA), vec(CH))]]의 값은?\n"
              "(가) 점 H가 선분 AB를 [[ratio(1, 2)]]으로 내분한다.\n"
              "(나) [[dot(vec(AB), vec(AC)) = 27]]\n"
              "(다) 삼각형 ABC의 넓이는 18이다."),
    choices=["[[16]]", "[[17]]", "[[18]]", "[[19]]", "[[20]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(밑변 AB, 꼭짓점 C 위쪽), C에서 AB에 내린 수선의 발 H와 직각 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 ABC와 수선의 발 H",
    note="AH=a, HB=2a: AB·AC=3a·a=27 ⇒ a=3; 넓이 (1/2)·9·h=18 ⇒ h=4; CA·CH=CH²=16 ⇒ ①.")

# p11
add(id="2d824950", qtype="short",
    question=("그림과 같이 [[seg(AB) = 10]]인 삼각형 ABC에 내접하는 원의 중심을 I라 하고, 점 I에서 변 BC에 내린 수선의 발을 D라 "
              "하자. [[seg(BD) = 4]]일 때, [[dot(vec(BA), vec(BI))]]의 값을 구하시오."),
    choices=None, derived_answer="40",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC와 내접원(중심 I), I에서 BC에 내린 수선의 발 D(직각 표시), B에서 I로 향하는 화살표, AB=10, BD=4 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형과 내접원, 내심 I, 수선의 발 D",
    note="BI는 ∠B의 이등분선, BI의 BA 방향 정사영 길이 = BD = 4 ⇒ BA·BI = 10·4 = 40.")

# p18
add(id="4120f451", qtype="short",
    question=("두 벡터 [[vec(a) = vcomp(4, 1)]], [[vec(b) = vcomp(-2, k)]]에 대하여 "
              "[[dot(vec(a), vec(b)) = 0]]을 만족시키는 실수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2016년 6월 고3 이과 23번/3점]. -8+k=0 ⇒ k=8 (빠른정답 5와 불일치).")

# p19 (id 2개) — 프라임 점 라벨
dup(["5fbc421d", "b6d1079e"], qtype="choice",
    question=("좌표평면 위에 원점 O를 시점으로 하는 서로 다른 임의의 두 벡터 [[vec(OP)]], [[vec(OQ)]]가 있다. "
              "두 벡터의 종점 P, Q를 [[x]]축의 방향으로 4만큼, [[y]]축의 방향으로 3만큼 평행이동시킨 점을 각각 P′, Q′이라 할 때, "
              "다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. |[[vec(OP)]] − [[vec(OP)]]′| = 5\n"
              "ㄴ. |[[vec(OP)]] − [[vec(OQ)]]| = |[[vec(OP)]]′ − [[vec(OQ)]]′|\n"
              "ㄷ. [[dot(vec(OP), vec(OQ))]] = [[vec(OP)]]′ · [[vec(OQ)]]′"),
    choices=CH_G, derived_answer="③", figure=None, difficulty_est=3, confidence=0.75,
    needs_review="프라임 점 라벨 벡터(OP′, OQ′)를 텍스트 혼합으로 표기",
    note="평행이동 벡터 (4,3): ㄱ |(4,3)|=5 ✓, ㄴ 차 벡터 불변 ✓, ㄷ 내적은 일반적으로 달라짐 ✗ ⇒ ③ (빠른정답 0과 불일치).")

# p20
add(id="b04c59fa", qtype="short",
    question="다음 두 벡터의 내적을 구하시오.\n[[vec(a) = vcomp(2, 5, -1)]], [[vec(b) = vcomp(7, -2, -4)]]",
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="14-10+4=8 (빠른정답 5와 불일치).")

# p22
add(id="78750a42", qtype="choice",
    question=("좌표평면 위에 원점 O를 시점으로 하는 서로 다른 임의의 두 벡터 [[vec(OP)]], [[vec(OQ)]]가 있다. "
              "두 벡터의 종점 P, Q를 [[x]]축 방향으로 3만큼, [[y]]축 방향으로 1만큼 평행이동시킨 점을 각각 P′, Q′이라 할 때, "
              "<보기>에서 항상 옳은 것을 모두 고른 것은?\n<보기>\n"
              "ㄱ. |[[vec(OP)]] − [[vec(OP)]]′| = [[sqrt(10)]]\n"
              "ㄴ. |[[vec(OP)]] − [[vec(OQ)]]| = |[[vec(OP)]]′ − [[vec(OQ)]]′|\n"
              "ㄷ. [[dot(vec(OP), vec(OQ))]] = [[vec(OP)]]′ · [[vec(OQ)]]′"),
    choices=CH_G, derived_answer="③", figure=None, difficulty_est=3, confidence=0.75,
    needs_review="프라임 점 라벨 벡터(OP′, OQ′)를 텍스트 혼합으로 표기",
    note="출처 [2005년 11월 고3 이과 4번]. 평행이동 벡터 (3,1): ㄱ √10 ✓, ㄴ ✓, ㄷ ✗ ⇒ ③.")

# p35
add(id="e4a5c0da", qtype="choice",
    question=("평면에서 그림의 오각형 ABCDE가\n[[seg(AB) = seg(BC)]], [[seg(AE) = seg(ED)]], [[angle(B) = angle(E) = deg(90)]]\n"
              "를 만족시킬 때, 옳은 것만을 <보기>에서 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 선분 BE의 중점 M에 대하여 [[vec(AB) + vec(AE)]]와 [[vec(AM)]]은 서로 평행하다.\n"
              "ㄴ. [[dot(vec(AB), vec(AE)) = -dot(vec(BC), vec(ED))]]\n"
              "ㄷ. [[abs(vec(BC) + vec(ED)) = abs(vec(BE))]]"),
    choices=CH_G, derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "오각형 ABCDE (A 위, B 좌, E 우, C 좌하, D 우하), 꼭짓점 B와 E에 직각 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 오각형 ABCDE(직각 표시)",
    note="출처 [2009년 11월 고3 이과 14번]. ㄱ AB+AE=2AM ✓, ㄴ BC·ED = R(AB)·R⁻¹(AE) = -AB·AE ✓, ㄷ BC+ED = R(AB-AE)=R(EB) ⇒ 크기 BE ✓ ⇒ ⑤ (빠른정답 71과 불일치).")

# p41
add(id="95f169ce", qtype="choice",
    question=("두 벡터 [[vec(a) = vcomp(2, 2, 1)]], [[vec(b) = vcomp(1, 4, -1)]]이 이루는 각의 크기 [[theta]]의 값은? "
              "(단, [[0 <= theta <= pi]]이다.)"),
    choices=["[[frac(pi,6)]]", "[[frac(pi,4)]]", "[[frac(pi,3)]]", "[[frac(pi,2)]]", "[[frac(2,3) pi]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2006년 9월 고3 이과 3번]. a·b=9, |a|=3, |b|=3√2 ⇒ cosθ=1/√2 ⇒ π/4 ⇒ ②.")

# p72
add(id="548e86e0", qtype="choice",
    question=("삼각형 OAB에 대하여 [[vec(OA) = vec(a)]], [[vec(OB) = vec(b)]]라 하자.\n"
              "[[abs(vec(a) + vec(b)) = 6]], [[abs(2 vec(a) - vec(b)) = 9]], [[dot((vec(a) + vec(b)), (vec(a) - vec(b))) = 0]]일 때, "
              "삼각형 OAB의 넓이는?"),
    choices=["[[4 sqrt(2)]]", "[[5 sqrt(2)]]", "[[6 sqrt(2)]]", "[[7 sqrt(2)]]", "[[8 sqrt(2)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2025년 6월 고3 기하 27번/3점]. |a|=|b|, |a|²=17, a·b=1 ⇒ 넓이 (1/2)√(289-1)=6√2 ⇒ ③.")

# p74 — 첨자 점 A₁, A₂, A₃
add(id="6462357d", qtype="choice",
    question=("좌표평면에서 원점 O가 중심이고 반지름의 길이가 1인 원 위의 세 점 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]]에 대하여\n"
              "[[abs(vec(OX)) <= 1]]이고, [[dot(vec(OX), sub(vec(OA), k)) >= 0]] ([[k]] = 1, 2, 3)\n"
              "을 만족시키는 모든 점 X의 집합이 나타내는 도형을 [[D]]라 하자. <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(vec(OA), 1) = sub(vec(OA), 2) = sub(vec(OA), 3)]]이면 [[D]]의 넓이는 [[frac(pi,2)]]이다.\n"
              "ㄴ. [[sub(vec(OA), 2) = -sub(vec(OA), 1)]]이고, [[sub(vec(OA), 3) = sub(vec(OA), 1)]]이면 [[D]]의 길이는 2인 선분이다.\n"
              "ㄷ. [[dot(sub(vec(OA), 1), sub(vec(OA), 2)) = 0]]인 경우에, [[D]]의 넓이가 [[frac(pi,4)]]이면 점 [[sub(A,3)]]은 [[D]]에 포함되어 있다."),
    choices=CH_G, derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.75,
    needs_review="첨자 점 라벨 벡터 OA₁, OA₂, OA₃을 sub(vec(OA),k)로 우회 표기",
    note="출처 [2017년 9월 고3 이과 19번/4점]. ㄱ 반원 π/2 ✓, ㄴ OA₁에 수직인 지름 선분 ✓, ㄷ A₃이 사분호 위 ⇒ D에 포함 ✓ ⇒ ⑤ (빠른정답 1과 불일치).")

# p76 (id 4개)
dup(["3803b558", "bd2a6a3f", "c95eea8f", "0a59e7d6"], qtype="choice",
    question=("좌표평면에서 원점 O가 중심이고 반지름의 길이가 1인 원 위의 세 점 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]]에 대하여 "
              "[[abs(vec(OX)) <= 1]]이고 [[dot(vec(OX), sub(vec(OA), k)) >= 0]] ([[k]] = 1, 2, 3)을 "
              "만족시키는 모든 점 X의 집합이 나타내는 도형을 [[D]]라 하자. 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(vec(OA), 1) = sub(vec(OA), 2) = sub(vec(OA), 3)]]이면 [[D]]의 넓이는 [[frac(pi,2)]]이다.\n"
              "ㄴ. [[sub(vec(OA), 2) = -sub(vec(OA), 1)]]일 때, [[D]]가 길이가 2인 선분이기 위해서는 "
              "[[sub(vec(OA), 3) = sub(vec(OA), 1)]] 또는 [[sub(vec(OA), 3) = sub(vec(OA), 2)]]이어야 한다.\n"
              "ㄷ. [[dot(sub(vec(OA), 1), sub(vec(OA), 2)) = 0]], [[sub(vec(OA), 3) = -sub(vec(OA), 1)]]이면 "
              "[[D]]는 길이가 [[frac(3,2)]]인 선분이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.75,
    needs_review="첨자 점 라벨 벡터 OA₁, OA₂, OA₃을 sub(vec(OA),k)로 우회 표기",
    note="ㄱ ✓, ㄴ OA₃≠±OA₁이면 반직선 쪽만 남아 길이 1 ⇒ ✓, ㄷ 길이 1인 선분 ✗ ⇒ ③ (빠른정답 27과 불일치).")

# p78
add(id="328d10cd", qtype="choice",
    question=("좌표평면에서 원점 O가 중심이고 반지름의 길이가 1인 원 위의 세 점 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]]에 대하여 "
              "[[abs(vec(OX)) <= 1]]이고, [[dot(vec(OX), sub(vec(OA), k)) >= 0]] ([[k]] = 1, 2, 3)을 만족시키는 모든 점 X의 "
              "집합이 나타내는 도형을 [[D]]라 하자. 다음 보기 중에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(vec(OA), 1) = sub(vec(OA), 2) = sub(vec(OA), 3)]]이면 [[D]]의 넓이는 [[frac(pi,4)]]이다.\n"
              "ㄴ. [[sub(A,1)]][[sub(A,2)]]가 원의 지름일 때, [[sub(vec(OA), 3) = sub(vec(OA), 1)]]이면 [[D]]는 길이가 2인 선분이다.\n"
              "ㄷ. [[dot(sub(vec(OA), 1), sub(vec(OA), 2)) = 0]]인 경우에 ([[D]]의 넓이) = [[frac(pi,4)]]를 "
              "만족하는 점 [[sub(A,3)]]의 자취의 길이는 [[frac(pi,2)]]이다."),
    choices=CH_G, derived_answer="④", figure=None, difficulty_est=4, confidence=0.75,
    needs_review="첨자 점 라벨 벡터 OA₁, OA₂, OA₃을 sub(vec(OA),k)로 우회 표기, 선분 A₁A₂의 윗줄 생략",
    note="출처 [2017년 9월 고3 이과 19번 변형]. ㄱ 반원 넓이 π/2 ✗, ㄴ ✓, ㄷ A₃은 사분호(길이 π/2) 위 ✓ ⇒ ④ (빠른정답 3과 불일치).")

# p80
add(id="2f7c6efe", qtype="choice",
    question=("좌표평면에서 두 점 [[A(2, 0)]], [[B(2, 1)]]에 대하여 두 점 P, Q가 [[abs(vec(OP)) = 2]], [[abs(vec(BQ)) = 5]], "
              "[[dot(vec(AP), (vec(QA) + vec(QP))) = 0]]을 만족시킨다. [[abs(vec(PQ))]]의 값이 최소가 되도록 하는 두 점 P, Q에 대하여 "
              "[[dot(vec(AP), vec(BQ))]]의 값은? (단, O는 원점이고, [[abs(vec(AP)) > 0]]이다.)"),
    choices=["[[frac(34,5)]]", "[[frac(36,5)]]", "[[frac(38,5)]]", "[[8]]", "[[frac(42,5)]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2024년 6월 고3 기하 28번 변형]. Q는 AP의 수직이등분선(O 지남) 위, |PQ|=|QA| 최소 4 ⇒ Q(2,-4), P(-6/5,-8/5) ⇒ AP·BQ=8 ⇒ ④.")

# p87
add(id="60517cc3", qtype="choice",
    question=("좌표평면 위의 점 [[A(4, 2)]]에 대하여 [[dot((vec(OP) - vec(OA)), vec(OA)) = 0]]을 만족시키는 점 P가 나타내는 "
              "도형이 [[x]]축, [[y]]축과 만나는 점을 각각 B, C라 할 때, 삼각형 OBC의 넓이는? (단, O는 원점이다.)"),
    choices=["[[21]]", "[[22]]", "[[23]]", "[[24]]", "[[25]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2024년 7월 고3 기하 25번/3점]. 직선 2x+y=10 ⇒ B(5,0), C(0,10) ⇒ 넓이 25 ⇒ ⑤.")

# p92
add(id="54d70b68", qtype="choice",
    question=("좌표평면에서 세 벡터 [[vec(a) = vcomp(1, 0)]], [[vec(b) = vcomp(2, 3)]], [[vec(c) = vcomp(5, 2)]]에 대하여 "
              "두 벡터 [[vec(p)]], [[vec(q)]]가 [[dot(vec(p), vec(a)) = dot(vec(a), vec(b))]], [[abs(vec(q) - vec(c)) = 2]]를 "
              "만족시킬 때, [[abs(vec(p) - vec(q))]]의 최솟값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2021년 9월 고3 기하 25번 변형]. p는 직선 x=2 위, q는 중심 (5,2) 반지름 2인 원 위 ⇒ 최솟값 3-2=1 ⇒ ① (빠른정답 100과 불일치).")

# p94
add(id="84c439b1", qtype="short",
    question=("좌표평면에 [[seg(AB) = 6]], [[seg(AD) = 4]], [[cos(angle(ABC)) = frac(1,4)]]인 평행사변형 ABCD가 있다.\n"
              "[[abs(vec(PA) + vec(PB) + vec(PC) + vec(PD)) = frac(1,2) abs(vec(BD))]]를 만족시키는 점 P에 대하여 "
              "[[vec(AQ) = vec(AC) - vec(AP)]]를 만족시키는 점을 Q라 하자. [[dot(vec(PB), vec(DQ))]]의 최댓값을 구하시오."),
    choices=None, derived_answer="25",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD (A 좌상, D 우상, B 좌하, C 우하)"}}],
    difficulty_est=4, confidence=0.8,
    note="출처 [2025년 7월 고3 기하 30번/4점]. M=중심: |PM|=|BD|/8, BD²=36+16+12=64 ⇒ |PM|=1; Q=2M-P ⇒ DQ=PB ⇒ PB·DQ=|PB|² ≤ (4+1)²=25 (빠른정답 3과 불일치).")

# p99 — 첨자 점 O₁, O₂ (이미지 하단에 별개 문항(정삼각형 ABC, p+q) 하나가 더 인쇄돼 있으나 id 없음)
add(id="e1c7b39f", qtype="choice",
    question=("평면 위의 두 점 [[sub(O,1)]], [[sub(O,2)]] 사이의 거리가 2일 때 [[sub(O,1)]], [[sub(O,2)]]를 각각 중심으로 하고 "
              "반지름의 길이가 2인 두 원의 교점을 A, B라 하자. 호 A[[sub(O,2)]]B 위의 점 P와 호 A[[sub(O,1)]]B 위의 점 Q에 대하여 "
              "두 벡터 [[sub(O,1)]]P⃗, [[sub(O,2)]]Q⃗의 내적 [[sub(O,1)]]P⃗ · [[sub(O,2)]]Q⃗의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, "
              "[[M + m]]의 값은?"),
    choices=["[[-4]]", "[[-2]]", "[[0]]", "[[2]]", "[[4]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "중심 O₁(좌), O₂(우)인 반지름 2의 두 원이 위아래 교점 A(위), B(아래)에서 만남; O₁에서 원 O₁의 오른쪽 호 위의 점 P로, O₂에서 원 O₂의 왼쪽 호 위의 점 Q로 향하는 화살표"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="첨자 점 라벨 벡터 O₁P, O₂Q 텍스트 혼합 / 도형 표현 불가: 두 원과 교점·화살표 / 이미지 하단에 별개 문항(정삼각형 ABC, p+q) 추가 인쇄(id 없음)",
    note="O₁P=2(cosθ,sinθ) θ∈[-60°,60°], O₂Q=2(cosφ,sinφ) φ∈[120°,240°] ⇒ 내적 4cos(θ-φ)∈[-4,2] ⇒ M+m=-2 ⇒ ② (빠른정답 7과 불일치).")

# ───────────── 직선과 평면의 위치 관계 ─────────────
# p19
add(id="ab4f1a07", qtype="choice",
    question=("그림과 같이 [[seg(AC) = seg(BD) = 3]]인 사면체 ABCD를 직선 AC와 직선 BD에 평행한 평면으로 자를 때 생기는 단면은 "
              "사각형이다. 이 사각형의 둘레의 길이는?"),
    choices=["[[4]]", "[[6]]", "[[8]]", "[[10]]", "[[12]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 ABCD(A 위, B 좌, D 우, C 아래)와 AC, BD에 평행한 평면으로 자른 단면 사각형(음영)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사면체와 단면 사각형",
    note="단면은 평행사변형, 둘레 = 2(3t+3(1-t)) = 6 ⇒ ② (빠른정답 5와 불일치).")

# p26
add(id="04a3a149", qtype="short",
    question=("다음 그림과 같이 한 평면 위에 있지 않은 네 점 A, B, C, D를 차례로 이어서 만든 사면체의 각 변의 중점을 각각 "
              "E, F, G, H라 하자. [[seg(AC) = 6]], [[seg(BD) = 5]]일 때, 사각형 EFGH의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="11",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 ABCD(B 좌, A 우상, C 우하, D 안쪽), AB·BC·CD·DA의 중점 E, F, G, H를 이은 사각형 EFGH(음영), BD=5, AC=6 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사면체와 중점 사각형 EFGH",
    note="EF=GH=AC/2=3, FG=HE=BD/2=5/2 ⇒ 둘레 11 (빠른정답 25와 불일치).")

# p55
add(id="0363b45f", qtype="short",
    question=("두 평면씩 서로 만나는 서로 다른 다섯 평면 [[alpha]], [[beta]], [[gamma]], [[delta]], [[lam]]에 대하여 "
              "[[alpha]]와 [[beta]]의 교선을 [[sub(l,1)]], [[alpha]]와 [[gamma]]의 교선을 [[sub(l,2)]], [[alpha]]와 [[delta]]의 교선을 [[sub(l,3)]], "
              "[[alpha]]와 [[lam]]의 교선을 [[sub(l,4)]], [[beta]]와 [[gamma]]의 교선을 [[sub(l,5)]], [[beta]]와 [[delta]]의 교선을 [[sub(l,6)]], "
              "[[beta]]와 [[lam]]의 교선을 [[sub(l,7)]], [[gamma]]와 [[delta]]의 교선을 [[sub(l,8)]], [[gamma]]와 [[lam]]의 교선을 [[sub(l,9)]], "
              "[[delta]]와 [[lam]]의 교선을 [[sub(l,10)]]이라 할 때, [[sub(l,1)]], [[sub(l,2)]], [[sub(l,3)]], ⋯, [[sub(l,10)]]이 모두 서로 평행하다. "
              "다섯 평면 [[alpha]], [[beta]], [[gamma]], [[delta]], [[lam]]에 의하여 공간은 몇 개로 분할되는지 구하시오."),
    choices=None, derived_answer="16", figure=None, difficulty_est=3, confidence=0.85,
    note="교선이 모두 평행 ⇒ 단면에서 일반 위치의 직선 5개 ⇒ 1+5+C(5,2)=16 (빠른정답 9와 불일치).")

# p57
add(id="74f11399", qtype="choice",
    question=("그림은 [[seg(AC) = seg(AE) = seg(BE)]]이고 [[angle(DAC) = angle(CAB) = deg(90)]]인 사면체의 전개도이다.\n"
              "이 전개도로 사면체를 만들 때, 세 점 D, E, F가 합쳐지는 점을 P라 하자. 사면체 PABC에 대하여 옳은 것만을 <보기>에서 "
              "있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[seg(CP) = sqrt(2) seg(BP)]]\n"
              "ㄴ. 직선 AB와 직선 CP는 꼬인 위치에 있다.\n"
              "ㄷ. 선분 AB의 중점을 M이라 할 때, 직선 PM과 직선 BC는 서로 수직이다."),
    choices=CH_G, derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 전개도: 가운데 삼각형 ABC(A에서 직각 표시, C 위·A 아래·B 우), 바깥에 D(좌), F(우상), E(아래)가 붙은 삼각형 ACD, CBF, ABE; 점선 CA, CB"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 사면체 전개도",
    note="출처 [2011년 9월 고3 이과 15번/4점]. PA=PB=AC=a, AC⊥면PAB: ㄱ CP=√2a=√2BP ✓, ㄴ 대변 꼬인 위치 ✓, ㄷ PM⊥AB, PM⊥AC ⇒ PM⊥면ABC ✓ ⇒ ⑤ (빠른정답 6과 불일치).")

# p61 (id 2개)
dup(["6ec1a2d9", "af89c2d7"], qtype="choice",
    question=("다음 그림은 [[seg(BC) = seg(BE) = seg(CE)]], [[angle(ABC) = angle(CFA) = deg(90)]]인 사면체의 전개도이다. "
              "이 전개도로 사면체를 만들 때, 세 점 D, E, F가 합쳐지는 점을 P라 하자. 다음 보기 중 사면체 PABC에 대하여 "
              "옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[cong(tri(ABC), tri(APC))]]\n"
              "ㄴ. 선분 BP의 중점을 M이라 할 때, 직선 CM과 직선 AB는 꼬인 위치에 있다.\n"
              "ㄷ. 직선 AC와 직선 BP는 서로 수직이다."),
    choices=CH_G, derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 전개도: 가운데 삼각형 ABC(B에서 직각 표시, A 위·B 좌하·C 우하), 바깥에 D(좌), F(우상, 직각 표시), E(아래)가 붙은 삼각형 ABD, ACF, BCE; 점선 AB, AC"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 사면체 전개도",
    note="PB=PC=BC=a, PA=AB(직각삼각형 AFC·ABC의 빗변 공통): ㄱ SSS 합동 ✓, ㄴ CM⊂면PBC, AB∩면PBC={B} ⇒ 꼬인 위치 ✓, ㄷ A, C가 BP의 수직이등분면 위 ⇒ AC⊥BP ✓ ⇒ ⑤.")

# p67
add(id="2d39eb3c", qtype="short",
    question=("다음 그림과 같이 [[perp(seg(AD), seg(BC))]], [[seg(AD) = 12]], [[seg(BC) = 18]]인 사면체 ABCD에서 두 선분 AD와 BC의 "
              "중점을 각각 M, N이라 하자. [[seg(MN) = 10]]이고 [[perp(seg(AD), seg(MN))]], [[perp(seg(BC), seg(MN))]]일 때, "
              "사면체 ABCD의 부피를 구하시오."),
    choices=None, derived_answer="360",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 ABCD(A 위, B 좌, D 우, C 아래), AD의 중점 M, BC의 중점 N, MN=10(직각 표시), AD=12, BC=18(같은 길이 표시)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사면체와 중점 M, N",
    note="V=(1/6)·AD·BC·MN·sin90°=(1/6)·12·18·10=360.")

# p72
add(id="8f9c4a9c", qtype="choice",
    question=("서로 다른 세 평면 [[alpha]], [[beta]], [[gamma]]와 서로 다른 세 직선 [[l]], [[m]], [[n]]의 위치관계에 대한 다음 <보기>의 명제 중 "
              "항상 참인 것의 개수는?\n(단, ∥는 평행, ⊥는 수직을 의미한다.)\n[보 기]\n"
              "• [[perp(alpha, beta)]], [[perp(alpha, gamma)]]이면 [[par(beta, gamma)]]\n"
              "• [[perp(l, m)]], [[perp(m, n)]]이면 [[par(l, n)]]\n"
              "• [[par(l, alpha)]], [[par(l, beta)]]이면 [[par(alpha, beta)]]\n"
              "• [[perp(l, alpha)]], [[par(l, beta)]]이면 [[perp(alpha, beta)]]\n"
              "• [[par(l, m)]], [[par(m, alpha)]]이면 [[par(l, alpha)]]"),
    choices=["1개", "2개", "3개", "4개", "5개"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="네 번째(l⊥α, l∥β ⇒ α⊥β)만 참 ⇒ 1개 ⇒ ①.")

# p77
add(id="f30564e2", qtype="choice",
    question=("공간에서 서로 다른 두 직선 [[l]], [[m]]과 서로 다른 세 평면 [[alpha]], [[beta]], [[gamma]]에 대하여 다음 중 옳지 않은 "
              "것을 모두 고르면? (정답 2개)"),
    choices=["[[perp(l, m)]], [[par(l, alpha)]]이면 [[perp(m, alpha)]]이다.",
             "[[perp(l, alpha)]], [[perp(l, beta)]]이면 [[par(alpha, beta)]]이다.",
             "[[perp(alpha, beta)]], [[par(alpha, gamma)]]이면 [[perp(beta, gamma)]]이다.",
             "[[par(l, alpha)]], [[par(alpha, beta)]]이면 [[par(l, beta)]]이다.",
             "[[par(l, alpha)]], [[perp(alpha, beta)]]이면 [[perp(l, beta)]]이다."],
    derived_answer=None, figure=None, difficulty_est=2, confidence=0.85,
    note="①·⑤는 거짓, ②·③은 참, ④는 l⊂β 가능해 항상 참이 아님 — '정답 2개'와 어긋나 답 미도출(빠른정답 1).")

# p79
add(id="e6911b62", qtype="choice",
    question=("공간에서 서로 다른 두 직선 [[l]], [[m]]과 서로 다른 세 평면 [[alpha]], [[beta]], [[gamma]]에 대하여 [[perp(l, alpha)]]이고 "
              "[[par(alpha, beta)]]일 때, 다음 보기 중 항상 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 직선 [[l]]과 수직인 평면 [[gamma]]는 평면 [[beta]]와 수직이다.\n"
              "ㄴ. 평면 [[beta]]와 수직인 직선 [[m]]은 직선 [[l]]과 평행이다.\n"
              "ㄷ. 직선 [[l]]과 평행한 평면 [[gamma]]는 평면 [[alpha]]와 수직이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="l⊥β: ㄱ γ⊥l ⇒ γ∥β ✗, ㄴ m⊥β, l⊥β ⇒ m∥l ✓, ㄷ γ∥l, l⊥α ⇒ γ⊥α ✓ ⇒ ④ (빠른정답 없음).")

# p81
add(id="fd1fbd58", qtype="choice",
    question=("공간에서 서로 다른 두 직선 [[l]], [[m]]과 서로 다른 세 평면 [[alpha]], [[beta]], [[gamma]]에 대하여 [[par(l, alpha)]]이고 "
              "[[par(alpha, beta)]]일 때, 다음 보기 중 항상 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[perp(l, beta)]]\n"
              "ㄴ. 평면 [[beta]]와 수직인 직선 [[m]]은 직선 [[l]]과 수직이다.\n"
              "ㄷ. 직선 [[l]]과 평행한 평면 [[gamma]]는 평면 [[alpha]]와 수직이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="l∥β(또는 l⊂β): ㄱ ✗, ㄴ m⊥β ⇒ m⊥l ✓, ㄷ γ∥α 가능 ✗ ⇒ ②.")

# p82 (id 2개)
dup(["55f21c06", "ce7561ab"], qtype="short",
    question=("서로 다른 세 직선 [[l]], [[m]], [[n]]과 서로 다른 세 평면 [[alpha]], [[beta]], [[gamma]]에 대하여 다음 보기 중 항상 옳은 것의 "
              "개수를 구하시오.\n<보기>\n"
              "ㄱ. [[perp(l, m)]]이고 [[perp(m, n)]]이면 [[perp(l, n)]]이다.\n"
              "ㄴ. [[perp(alpha, beta)]]이고 [[perp(alpha, gamma)]]이면 [[perp(beta, gamma)]]이다.\n"
              "ㄷ. [[perp(l, alpha)]]이고 [[perp(l, beta)]]이면 [[par(alpha, beta)]]이다.\n"
              "ㄹ. [[perp(l, alpha)]]이고 [[par(l, beta)]]이면 [[par(alpha, beta)]]이다.\n"
              "ㅁ. [[par(l, alpha)]]이고 [[par(l, beta)]]이면 [[par(alpha, beta)]]이다."),
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄷ만 항상 참(ㄹ은 α⊥β) ⇒ 1개 (빠른정답 4와 불일치).")
