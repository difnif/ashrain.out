# -*- coding: utf-8 -*-
# esc_sonnet_h3-3_1of6 — 이미지 기준 전사 (80 항목 / 80쪽, 단원 h3-3 공간좌표·위치벡터·삼수선)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

FIG_REVIEW = "도형 표현 불가"
PRIME = "프라임/첨자 점 라벨"

# ===================== 선분의 내분점 =====================
# p1
add(id="f66916c2", qtype="choice",
    question="좌표공간에서 두 점 [[A(a, 1, 3)]], [[B(a + 6, 4, 12)]]에 대하여 선분 AB를 [[ratio(1, 2)]]로 내분하는 점의 좌표가 [[vcomp(5, 2, b)]]이다. [[a + b]]의 값은?",
    choices=["7", "8", "9", "10", "11"], derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2012년 11월 고3 이과 3번/2점]. 내분점 (a+2, 2, 6) → a=3, b=6 → 9.")

# p2
add(id="1cfa592c", qtype="short",
    question="세 점 [[A(6, 0, 0)]], [[B(0, 8, 0)]], [[C(0, 8, 5)]]를 꼭짓점으로 하는 삼각형 ABC에서 [[angle(B)]]의 이등분선이 변 AC와 만나는 점을 P라 하자. 점 P의 좌표를 [[vcomp(a, b, c)]]라 할 때, [[a + b + 2c]]의 값을 구하시오.",
    choices=None, derived_answer="14", figure=None, difficulty_est=2, confidence=0.9,
    note="AB=10, BC=5 → AP:PC=2:1 → P(2, 16/3, 10/3) → 2+16/3+20/3=14.")

# p3
add(id="37ff581e", qtype="choice",
    question="두 점 [[A(3, 5, 1)]], [[B(4, -2, 3)]]에 대하여 [[seg(AP) + seg(BP)]]의 값이 최소가 되게 하는 [[y z]]평면 위의 점을 P라 할 때, [[frac(seg(BP), seg(AP))]]의 값은?",
    choices=["[[frac(2,3)]]", "1", "[[frac(4,3)]]", "[[frac(5,3)]]", "2"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="A를 yz평면에 대칭 A′(-3,5,1); x좌표 비 3:4 → BP/AP=4/3.")

# p4
add(id="a689773d", qtype="choice",
    question="두 점 [[A(-2, -1, 5)]], [[B(-4, 3, 2)]]에 대하여 [[seg(AP) + seg(BP)]]의 값이 최소가 되게 하는 [[y z]]평면 위의 점을 P라 할 때, [[frac(seg(BP), seg(AP))]]의 값은?",
    choices=["[[frac(1,2)]]", "1", "[[frac(3,2)]]", "2", "[[frac(5,2)]]"], derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="A 대칭점 (2,-1,5); x좌표 비 2:4 → BP/AP=2.")

# p5
add(id="6bb088dd", qtype="choice",
    question="좌표공간의 두 점 [[A(a, 1, -1)]], [[B(-5, b, 3)]]에 대하여 선분 AB의 중점의 좌표가 [[vcomp(8, 3, 1)]]일 때, [[a + b]]의 값은?",
    choices=["20", "22", "24", "26", "28"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2022년 9월 고3 기하 23번/2점]. a=21, b=5 → 26.")

# p6
add(id="8a3008c0", qtype="choice",
    question="좌표공간에서 두 점 [[A(a, 5, 2)]], [[B(-2, 0, 7)]]에 대하여 선분 AB를 [[ratio(3, 2)]]로 내분하는 점의 좌표가 [[vcomp(0, b, 5)]]이다. [[a + b]]의 값은?",
    choices=["1", "2", "3", "4", "5"], derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2013년 11월 고3 이과 3번/2점]. (2a-6)/5=0 → a=3, b=2 → 5.")

# p11
add(id="c93ddbc4", qtype="choice",
    question="좌표공간에서 두 점 [[A(2, a, -2)]], [[B(5, -3, b)]]에 대하여 선분 AB를 [[ratio(2, 1)]]로 내분하는 점이 [[x]]축 위에 있을 때, [[a + b]]의 값은?",
    choices=["10", "9", "8", "7", "6"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2014년 11월 고3 이과 5번/3점]. (a-6)/3=0, (2b-2)/3=0 → a=6, b=1 → 7.")

# p12
add(id="86ca906c", qtype="choice",
    question="좌표공간의 점 [[A(3, -1, a)]]를 [[x y]]평면에 대하여 대칭이동한 점을 B라 하자. 점 [[C(-3, b, 4)]]에 대하여 선분 BC를 [[ratio(1, 2)]]로 내분하는 점이 [[x]]축 위에 있을 때, [[a + b]]의 값은?",
    choices=["4", "5", "6", "7", "8"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2024년 10월 고3 기하 24번/3점]. B(3,-1,-a); (2B+C)/3 → b=2, a=2 → 4.")

# p14
add(id="52bf4368", qtype="choice",
    question="좌표공간에서 세 점 [[A(1, 0, 0)]], [[B(2, 2, 0)]], [[C(0, 0, 2 sqrt(2))]]를 꼭짓점으로 하는 삼각형 ABC의 꼭짓점 C를 지나고 [[angle(ACB)]]를 이등분하는 직선이 변 AB와 만나는 점을 [[D(a, b, c)]]라 할 때, [[a + b + c]]의 값은?",
    choices=["[[frac(16,7)]]", "[[frac(17,7)]]", "[[frac(18,7)]]", "[[frac(19,7)]]", "[[frac(20,7)]]"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="CA=3, CB=4 → AD:DB=3:4 → D(10/7, 6/7, 0) → 16/7.")

# p17
add(id="c74e5929", qtype="choice",
    question="좌표공간의 두 점 [[A(-2, 1, 4)]], [[B(4, -1, 2)]]에 대하여 선분 AB가 [[x y]]평면과 만나는 점을 P라 할 때, 선분 AP의 길이는?",
    choices=["[[8 sqrt(2)]]", "12", "[[4 sqrt(10)]]", "[[4 sqrt(11)]]", "[[8 sqrt(3)]]"], derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="출처 [2021년 10월 고3 기하 24번 변형]. 직선 AB와 xy평면의 교점 P(10,-3,0) → AP=√176=4√11 (선분 AB 자체는 z>0이라 xy평면과 만나지 않음, 원문 그대로 전사).")

# p18
add(id="a0cc9596", qtype="choice",
    question="좌표공간의 두 점 [[A(a, -2, 6)]], [[B(9, 2, b)]]에 대하여 선분 AB의 중점의 좌표가 [[vcomp(4, 0, 7)]]일 때, [[a + b]]의 값은?",
    choices=["1", "3", "5", "7", "9"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2023년 11월 고3 기하 23번/2점]. a=-1, b=8 → 7.")

# p19
add(id="2183ea25", qtype="choice",
    question="좌표공간에서 두 점 [[A(4, 0, 2)]], [[B(2, 3, a)]]에 대하여 선분 AB를 [[ratio(2, 1)]]로 내분하는 점이 [[x y]]평면 위에 있을 때, [[a]]의 값은?",
    choices=["-2", "-1", "0", "1", "2"], derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2013년 7월 고3 이과 3번/2점]. z: (2+2a)/3=0 → a=-1.")

# p22
add(id="6c8fe855", qtype="choice",
    question="좌표공간의 두 점 [[O(0, 0, 0)]], [[A(6, 3, 9)]]에 대하여 선분 OA를 [[ratio(1, 2)]]로 내분하는 점 P의 좌표가 [[vcomp(a, b, c)]]이다. [[a + b + c]]의 값은?",
    choices=["3", "4", "5", "6", "7"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2018년 7월 고3 이과 3번/2점]. P(2,1,3) → 6.")

# p25
add(id="1cce8564", qtype="choice",
    question="좌표공간의 세 점 [[A(3, 0, 0)]], [[B(0, 3, 0)]], [[C(0, 0, 3)]]에 대하여 선분 BC를 [[ratio(2, 1)]]로 내분하는 점을 P, 선분 AC를 [[ratio(1, 2)]]로 내분하는 점을 Q라 하자. 점 P, Q의 [[x y]]평면 위로의 정사영을 각각 P′, Q′이라 할 때, 삼각형 OP′Q′의 넓이는? (단, O는 원점이다.)",
    choices=["1", "2", "3", "4", "5"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.8,
    needs_review=PRIME + "(P′, Q′) 텍스트 혼합",
    note="출처 [2005년 9월 고3 이과 14번]. P(0,1,2), Q(2,0,1) → P′(0,1,0), Q′(2,0,0) → 넓이 1.")

# p26 (p1과 동일 문항, 머리말 없음)
add(id="de73b91c", qtype="choice",
    question="좌표공간에서 두 점 [[A(a, 1, 3)]], [[B(a + 6, 4, 12)]]에 대하여 선분 AB를 [[ratio(1, 2)]]로 내분하는 점의 좌표가 [[vcomp(5, 2, b)]]이다. [[a + b]]의 값은?",
    choices=["7", "8", "9", "10", "11"], derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="a=3, b=6 → 9.")

# p29
add(id="24145d85", qtype="choice",
    question="두 점 [[A(2, a, -6)]], [[B(3, -6, b)]]에 대하여 선분 AB를 [[ratio(2, 3)]]으로 내분하는 점이 [[x]]축 위에 있을 때, [[a + b]]의 값은?",
    choices=["10", "11", "12", "13", "14"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="(3A+2B)/5: 3a-12=0, -18+2b=0 → a=4, b=9 → 13.")

# p33
add(id="1bda5201", qtype="choice",
    question="두 점 [[A(8, 1, 5)]], [[B(4, -3, 1)]]에 대하여 선분 AB가 [[z x]]평면과 만나는 점을 P라 할 때, 점 P의 좌표는?",
    choices=["[[vcomp(5, 0, 3)]]", "[[vcomp(5, 0, 2)]]", "[[vcomp(7, 0, 2)]]", "[[vcomp(7, 0, 4)]]", "[[vcomp(9, 0, 4)]]"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="y=0인 점: AP:PB=1:3 → P(7,0,4).")

# p34
add(id="0c3bf245", qtype="short",
    question="점 [[A(1, -2, 3)]]에 대하여 점 [[P(2, 1, 4)]]의 대칭점이 P′[[vcomp(a, b, c)]]일 때, [[a + b + c]]의 값을 구하시오.",
    choices=None, derived_answer="-3", figure=None, difficulty_est=1, confidence=0.8,
    needs_review=PRIME + "(P′) 텍스트 혼합",
    note="P′=2A-P=(0,-5,2) → -3.")

# p35
add(id="884b7797", qtype="choice",
    question="점 [[P(2, 7, 0)]]을 점 [[A(3, 8, -1)]]에 대하여 대칭이동한 점 P′의 좌표는?",
    choices=["[[vcomp(3, 6, -1)]]", "[[vcomp(3, 8, -3)]]", "[[vcomp(4, 8, -1)]]", "[[vcomp(4, 9, -2)]]", "[[vcomp(5, 10, -3)]]"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.8,
    needs_review=PRIME + "(P′) 텍스트 혼합",
    note="P′=2A-P=(4,9,-2).")

# p37
add(id="6ebbe839", qtype="short",
    question="네 점 [[O(0, 0, 0)]], [[A(a, 7, 3)]], [[B(-4, b, 1)]], [[C(2, -3, c)]]가 [[seg(OA)]]와 [[seg(OC)]]를 이웃하는 두 변으로 하는 평행사변형의 꼭짓점일 때, [[a + b + c]]의 값을 구하시오.",
    choices=None, derived_answer="-4", figure=None, difficulty_est=1, confidence=0.9,
    note="B=A+C → a=-6, b=4, c=-2 → -4.")

# p38
add(id="ed26259b", qtype="short",
    question="네 점 [[O(0, 0, 0)]], [[A(a, 4, 2)]], [[B(-1, b, 7)]], [[C(3, -2, c)]]가 [[seg(OA)]]와 [[seg(OC)]]를 이웃하는 두 변으로 하는 평행사변형의 꼭짓점일 때, [[a + b + c]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="B=A+C → a=-4, b=2, c=5 → 3.")

# p40
add(id="e0677996", qtype="choice",
    question="네 점\n[[A(0, 2, a)]], [[B(-4, 2, 0)]], [[C(-2, 0, b)]], [[D(c, 0, 2)]]\n에 대하여 사각형 ABCD가 마름모일 때, [[a b c]]의 값은?",
    choices=["-12", "-9", "-6", "-3", "0"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="A+C=B+D → c=2, a+b=2; AB=BC → b-a=4 → a=-1, b=3 → abc=-6.")

# p41
add(id="b74e84e4", qtype="choice",
    question="네 점 A, B, C, D를 꼭짓점으로 하는 평행사변형 ABCD에서 [[A(-1, 3, 5)]], [[C(3, 5, -1)]]이다. 네 선분 AB, BC, CD, DA의 중점을 각각 P, Q, R, S라 할 때, 사각형 PQRS의 두 대각선의 교점의 좌표는?",
    choices=["[[vcomp(0, 4, 3)]]", "[[vcomp(1, 4, 2)]]", "[[vcomp(1, 4, 4)]]", "[[vcomp(2, 8, 2)]]", "[[vcomp(2, 8, 4)]]"], derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="교점 = AC의 중점 (1,4,2).")

# p43
add(id="1126c215", qtype="choice",
    question="점 [[A(2, -6, 3)]]을 [[z x]]평면에 대하여 대칭이동한 후 원점에 대하여 대칭이동한 점을 P라 하자.\n점 P를 점 [[vcomp(a, b, c)]]에 대하여 대칭이동한 점이 [[Q(8, 4, -1)]]일 때, [[a + b + c]]의 값은?",
    choices=["-2", "-1", "0", "1", "2"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="P(-2,-6,-3); (a,b,c)=PQ 중점 (3,-1,-2) → 0.")

# p44
add(id="9fd40701", qtype="choice",
    question="점 [[P(3, 5, 0)]]을 점 [[A(4, 1, 1)]]에 대하여 대칭이동한 점 P′의 좌표는?",
    choices=["[[vcomp(-5, -3, 2)]]", "[[vcomp(-5, -3, -2)]]", "[[vcomp(5, -3, -2)]]", "[[vcomp(5, -3, 2)]]", "[[vcomp(5, 3, 2)]]"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.8,
    needs_review=PRIME + "(P′) 텍스트 혼합",
    note="P′=2A-P=(5,-3,2).")

# p45
add(id="80b048db", qtype="choice",
    question="점 [[A(5, -4, 2)]]를 [[x y]]평면에 대하여 대칭이동한 후 원점에 대하여 대칭이동한 점을 P라 하자. 점 P를 점 [[vcomp(a, b, c)]]에 대하여 대칭이동한 점이 [[Q(7, 2, -2)]]일 때, [[a + b + c]]의 값은?",
    choices=["1", "2", "3", "4", "5"], derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="P(-5,4,2); 중점 (1,3,0) → 4.")

# p47
add(id="0200a8ff", qtype="short",
    question="네 점 [[O(0, 0, 0)]], [[A(a, 3, 1)]], [[B(-2, b, 5)]], [[C(4, -1, c)]]가 [[seg(OA)]]와 [[seg(OC)]]를 이웃하는 두 변으로 하는 평행사변형의 꼭짓점일 때, [[a + 2b + 3c]]의 값을 구하시오.",
    choices=None, derived_answer="10", figure=None, difficulty_est=1, confidence=0.9,
    note="B=A+C → a=-6, b=2, c=4 → -6+4+12=10.")

# p49
add(id="d634f615", qtype="choice",
    question="다음 그림과 같이 한 모서리의 길이가 2와 3인 두 정육면체를 꼭짓점 O와 두 모서리가 겹치도록 붙여 놓았다. 두 정육면체에서 대각선 OA를 [[ratio(1, 2)]]로 내분하는 점을 P, 대각선 OB를 [[ratio(1, 5)]]로 내분하는 점을 Q라고 하자.\n[[pow(seg(PQ), 2) = frac(q, p)]]일 때, [[p + q]]의 값은?\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=["25", "26", "27", "28", "29"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "한 모서리의 길이가 2인 정육면체(왼쪽)와 3인 정육면체(오른쪽)를 꼭짓점 O에서 세로 모서리·안쪽 모서리가 겹치도록 붙인 입체도형. 작은 정육면체의 대각선 OA 위의 점 P, 큰 정육면체의 대각선 OB 위의 점 Q, 선분 PQ 표시. 아래에 길이 2, 3 표기"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 두 정육면체를 붙인 입체도형(대각선 OA, OB와 점 P, Q)",
    note="O 원점, A(-2,2,2), B(3,3,3) → P(-2/3,2/3,2/3), Q(1/2,1/2,1/2) → PQ²=51/36=17/12 → p+q=29.")

# p52
add(id="569ff281", qtype="choice",
    question="다음 그림과 같이 [[seg(AB) = seg(AD) = 1]], [[seg(AE) = 2]]인 직육면체에서 점 P와 점 Q가 매초 1의 속력으로 각각 꼭짓점 C, G에서 동시에 출발하여 점 P는 C→B→A→D→C, 점 Q는 G→H→E→F→G로 각각 한 번씩 회전한다. 선분 PQ의 중점을 R라 할 때, 점 R가 움직인 거리는?",
    choices=["[[sqrt(2)]]", "[[2 sqrt(2)]]", "[[pi]]", "[[sqrt(2) pi]]", "[[2 pi]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체 ABCD-EFGH(윗면 ABCD: A 뒤왼쪽, D 뒤오른쪽, B 앞왼쪽, C 앞오른쪽; 아랫면 EFGH 대응). 윗면 C-D 모서리 위 점 P, 아랫면 F-G 모서리 위 점 Q, 선분 PQ와 그 중점 R, 이동 방향 화살표"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체와 동점 P, Q, 중점 R",
    note="P, Q는 서로 반대 방향으로 정사각형을 돌아 R는 대각선 방향 길이 √2/2인 선분을 4번 왕복 → 2√2.")

# p58
add(id="8728a183", qtype="choice",
    question="네 점 A, B, C, D를 꼭짓점으로 하는 평행사변형 ABCD에서 [[A(-8, -6, 3)]], [[C(2, -2, 5)]]이다.\n네 선분 AB, BC, CD, DA의 중점을 각각 P, Q, R, S라 할 때, 사각형 PQRS의 두 대각선의 교점의 좌표는?",
    choices=["[[vcomp(3, -4, 4)]]", "[[vcomp(-3, 4, 4)]]", "[[vcomp(-3, -4, 4)]]", "[[vcomp(2, -4, 2)]]", "[[vcomp(2, -3, 2)]]"], derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="교점 = AC의 중점 (-3,-4,4).")

# p61
add(id="41d26f8a", qtype="short",
    question="네 점 [[A(-2, 1, 2)]], [[B(a, -2, -1)]], [[C(b, -3, -4)]], [[D(1, 0, -1)]]에 대하여 사각형 ABCD가 마름모일 때, [[a b]]의 값을 구하시오. (단, [[a < -2]])",
    choices=None, derived_answer="0", figure=None, difficulty_est=2, confidence=0.9,
    note="A+C=B+D → b=a+3; AB=AD → (a+2)²=1, a<-2 → a=-3, b=0 → ab=0.")

# ===================== 삼각형의 무게중심 =====================
# p69
add(id="aa3db65b", qtype="choice",
    question="좌표공간에서 세 점 [[A(a, 0, 5)]], [[B(1, b, -3)]], [[C(1, 1, 1)]]을 꼭짓점으로 하는 삼각형의 무게중심의 좌표가 [[vcomp(2, 2, 1)]]일 때, [[a + b]]의 값은?",
    choices=["6", "7", "8", "9", "10"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2015년 11월 고3 이과 3번/2점]. a=4, b=5 → 9.")

# p71
add(id="c1d383d8", qtype="choice",
    question="그림과 같이 좌표공간에서 한 변의 길이가 4인 정육면체를 한 변의 길이가 2인 8개의 정육면체로 나누었다. 이 중 그림의 세 정육면체 A, B, C안에 반지름의 길이가 1인 구가 각각 내접하고 있다.\n3개의 구의 중심을 연결한 삼각형의 무게중심의 좌표를 [[vcomp(p, q, r)]]라 할 때, [[p + q + r]]의 값은?",
    choices=["6", "[[frac(19,3)]]", "[[frac(20,3)]]", "7", "[[frac(22,3)]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간(x축 앞쪽, y축 오른쪽, z축 위)에 한 변 4인 정육면체를 2×2×2로 나눈 그림. 앞면(x=4) 위-왼쪽 칸 A, 앞면 아래-오른쪽 칸 B, 오른쪽 면(y=4) 아래-뒤쪽 칸 C. 축에 4 표기"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 2×2×2로 나눈 정육면체 좌표공간 그림(칸 A, B, C 위치)",
    note="출처 [2007년 9월 고3 이과 8번]. 중심 A(3,1,3), B(3,3,1), C(1,3,1) → 무게중심 (7/3,7/3,5/3) → 19/3.")

# p72
add(id="fa27d584", qtype="short",
    question="좌표공간의 세 점 [[A(a, -2, 3)]], [[B(1, b, 4)]], [[C(0, 4, 2)]]를 꼭짓점으로 하는 삼각형 ABC의 무게중심의 좌표가 [[vcomp(1, 0, 3)]]일 때, [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="0", figure=None, difficulty_est=1, confidence=0.9,
    note="a=2, b=-2 → 0.")

# p73
add(id="f523412b", qtype="short",
    question="좌표공간의\n세 점 [[A(a, 2, -7)]], [[B(4, b, 6)]], [[C(0, -1, -5)]]를 꼭짓점으로 하는 삼각형 ABC의 무게중심의 좌표가 [[vcomp(3, 2, -2)]]일 때, [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="10", figure=None, difficulty_est=1, confidence=0.9,
    note="a=5, b=5 → 10.")

# p74
add(id="a55a7b0f", qtype="choice",
    question="좌표공간의 점 [[A(9, -4, 6)]]과 [[z x]]평면에 대하여 대칭인 점을 P, [[z]]축에 대하여 대칭인 점을 Q, 원점에 대하여 대칭인 점을 R라 하자. 삼각형 PQR의 무게중심의 좌표가 [[vcomp(a, b, c)]]일 때, [[a + b + c]]의 값은?",
    choices=["1", "2", "3", "4", "5"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="P(9,4,6), Q(-9,4,6), R(-9,4,-6) → G(-3,4,2) → 3.")

# p75
add(id="8b20ed12", qtype="choice",
    question="좌표공간의 점 [[A(6, -3, 2)]]와 [[x y]]평면에 대하여 대칭인 점을 P, [[y]]축에 대하여 대칭인 점을 Q, 원점에 대하여 대칭인 점을 R라 하자. 삼각형 PQR의 무게중심의 좌표가 [[vcomp(a, b, c)]]일 때, [[a + b + c]]의 값은?",
    choices=["-5", "-4", "-3", "-2", "-1"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="P(6,-3,-2), Q(-6,-3,-2), R(-6,3,-2) → G(-2,-1,-2) → -5.")

# p77
add(id="9ded6fea", qtype="choice",
    question="좌표공간에서 세 점 [[A(0, -1, -2)]], [[B(2, 4, 2)]], [[C(4, 6, -3)]]을 꼭짓점으로 하는 삼각형 ABC의 무게중심 G의 좌표가 [[vcomp(a, b, c)]]일 때, [[a + b + c]]의 값은?",
    choices=["1", "2", "3", "4", "5"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="G(2,3,-1) → 4.")

# p78
add(id="b9ce68fb", qtype="choice",
    question="좌표공간에서 두 점 [[A(1, 2, -1)]], [[B(5, -4, 6)]]에 대하여 삼각형 ABC의 무게중심의 좌표가 [[vcomp(2, 1, -2)]]이다. 꼭짓점 C의 좌표가 [[vcomp(a, b, c)]]일 때, [[a + b + c]]의 값은?",
    choices=["-10", "-8", "-6", "-4", "-2"], derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="C=3G-A-B=(0,5,-11) → -6.")

# p80
add(id="c7a3776e", qtype="choice",
    question="세 점 [[A(a, -5, 1)]], [[B(2, b, -2)]], [[C(0, 8, c)]]를 꼭짓점으로 하는 삼각형 ABC의 무게중심의 좌표가 [[vcomp(2, 2, 1)]]일 때, [[a - b + c]]의 값은?",
    choices=["3", "4", "5", "6", "7"], derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="a=4, b=3, c=4 → 5.")

# p81
add(id="7c49fabb", qtype="choice",
    question="세 점 [[A(a, b, 1)]], [[B(b, a, 3)]], [[C(2, -4, -1)]]을 꼭짓점으로 하는 삼각형 ABC의 무게중심의 좌표가 [[vcomp(4, 2, c)]]일 때, [[a + b - c]]의 값은?",
    choices=["5", "6", "7", "8", "9"], derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="a+b=10, c=1 → 9.")

# p83
add(id="70493f4a", qtype="choice",
    question="세 점 A, B, C를 꼭짓점으로 하는 삼각형 ABC에서 [[A(-4, 3, 5)]], [[B(0, 5, 2)]]이고, 삼각형 ABC의 무게중심의 좌표가 [[vcomp(-1, 2, 3)]]일 때, 점 C의 좌표는?",
    choices=["[[vcomp(-2, -1, 3)]]", "[[vcomp(-1, 2, 4)]]", "[[vcomp(0, -2, 5)]]", "[[vcomp(1, -2, 2)]]", "[[vcomp(2, 1, -3)]]"], derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="C=3G-A-B=(1,-2,2).")

# p85
add(id="c72d4563", qtype="short",
    question="세 점 A, B, C를 꼭짓점으로 하는 삼각형 ABC에서 선분 AB의 중점이 [[M(3, 4, 5)]], 삼각형 ABC의 무게중심이 [[G(3, 1, 2)]]이다. 점 C의 좌표를 [[vcomp(a, b, c)]]라 할 때, [[a b c]]의 값을 구하시오.",
    choices=None, derived_answer="60", figure=None, difficulty_est=2, confidence=0.9,
    note="C=3G-2M=(3,-5,-4) → abc=60.")

# p86
add(id="45627168", qtype="short",
    question="세 점 A, B, C를 꼭짓점으로 하는 삼각형 ABC에서 선분 AB의 중점이 [[M(1, 2, 3)]], 삼각형 ABC의 무게중심이 [[G(2, 1, 3)]]이다. 점 C의 좌표를 [[vcomp(a, b, c)]]라 할 때, [[a b c]]의 값을 구하시오.",
    choices=None, derived_answer="-12", figure=None, difficulty_est=2, confidence=0.9,
    note="C=3G-2M=(4,-1,3) → abc=-12.")

# p89
add(id="dc91eb54", qtype="choice",
    question="삼각형 ABC에서 선분 BC의 중점 M의 좌표가 [[vcomp(-3, 2, 5)]], 삼각형 ABC의 무게중심 G의 좌표가 [[vcomp(4, 1, -2)]]일 때, 점 A의 좌표는?",
    choices=["[[vcomp(18, 1, 16)]]", "[[vcomp(18, 1, -16)]]", "[[vcomp(18, -1, -16)]]", "[[vcomp(-18, 1, 16)]]", "[[vcomp(-18, -1, 16)]]"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="A=3G-2M=(18,-1,-16).")

# p90
add(id="13a8f0fe", qtype="short",
    question="세 점 A, B, C를 꼭짓점으로 하는 삼각형 ABC에서 선분 AB의 중점이 [[M(2, 3, 4)]], 삼각형 ABC의 무게중심이 [[G(4, 1, 3)]]이다. 점 C의 좌표를 [[vcomp(a, b, c)]]라 할 때, [[a c + b]]의 값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="C=3G-2M=(8,-3,1) → ac+b=8-3=5.")

# p92
add(id="e84403c5", qtype="choice",
    question="다음 그림과 같이 정사면체 OABC의 면 OAC가 [[x y]]평면 위에 있다. [[O(0, 0, 0)]], [[A(0, 6, 0)]], [[B(a, b, c)]]일 때, [[a b c]]의 값은? (단, [[a > 0]], [[b > 0]], [[c > 0]])",
    choices=["[[frac(50 sqrt(2), 3)]]", "[[17 sqrt(2)]]", "[[frac(52 sqrt(2), 3)]]", "[[frac(53 sqrt(2), 3)]]", "[[18 sqrt(2)]]"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간(x축 앞쪽, y축 오른쪽, z축 위)에 놓인 정사면체 OABC: O 원점, A는 y축 위, C는 xy평면 제1사분면, B는 위쪽(z>0). 면 음영"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 좌표공간의 정사면체 OABC",
    note="한 모서리 6, C(3√3,3,0), B(√3,3,2√6) → abc=√3·3·2√6=18√2.")

# p93
add(id="43bde913", qtype="short",
    question="다음 그림과 같이 밑면의 가로, 세로의 길이가 각각 3, 4이고 높이가 2인 직육면체가 있다. 삼각형 DEG의 무게중심이 직육면체의 대각선 HB를 [[ratio(m, 2)]]로 내분할 때, 양수 [[m]]의 값을 구하시오.",
    choices=None, derived_answer="1",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체 ABCD-EFGH(윗면 ABCD, 아랫면 EFGH; E 앞왼쪽 아래, F 앞오른쪽 아래, G 뒤오른쪽 아래, H 뒤왼쪽 아래). EF=3, FG=4, AE=2 표기. 삼각형 DEG의 변과 대각선 HB 표시"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체와 삼각형 DEG, 대각선 HB",
    note="E(0,0,0), F(3,0,0), G(3,4,0), H(0,4,0), B(3,0,2), D(0,4,2); 무게중심 (1,8/3,2/3) = HB를 1:2로 내분 → m=1.")

# p94
add(id="77e0ba5b", qtype="short",
    question="다음 그림과 같이 한 모서리의 길이가 4인 정사면체 OABC의 면 OBC가 [[x y]]평면 위에 있다. 점 A의 좌표가 [[vcomp(a, b, c)]]일 때, [[pow(a,2) + pow(b,2) + pow(c,2)]]의 값을 구하시오. (단, [[a > 0]], [[b > 0]], [[c > 0]])",
    choices=None, derived_answer="16",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간(x축 앞쪽, y축 오른쪽, z축 위)에 놓인 정사면체 OABC: O 원점, B·C는 xy평면 위, A는 위쪽. 모서리 길이 4 표기, 면 음영"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 좌표공간의 정사면체 OABC",
    note="a²+b²+c²=OA²=16.")

# ===================== 위치벡터 =====================
# p1
add(id="66e7ed70", qtype="choice",
    question="세 점 A, B, C의 위치벡터를 각각 [[vec(a)]], [[vec(b)]], [[vec(c)]]라 할 때, [[vec(AB) + 3 vec(BC)]]를 [[vec(a)]], [[vec(b)]], [[vec(c)]]로 나타낸 것은?",
    choices=["[[-vec(a) + 2 vec(b) + vec(c)]]", "[[-vec(a) + 2 vec(b) + 3 vec(c)]]", "[[-vec(a) - 2 vec(b) + 3 vec(c)]]", "[[vec(a) + vec(b) + vec(c)]]", "[[vec(a) - 2 vec(b) + 3 vec(c)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="(b-a)+3(c-b) = -a-2b+3c.")

# p11
add(id="83517804", qtype="choice",
    question="한 직선 위에 있는 세 점 O, A, B가 [[3 seg(AB) = seg(OB)]]를 만족시킨다. 점 O에 대한 점 A의 위치벡터 [[vec(a)]]에 대하여 점 B의 위치벡터가 [[k vec(a)]]일 때, 모든 실수 [[k]]의 값의 합은?",
    choices=["[[frac(3,2)]]", "[[frac(7,4)]]", "2", "[[frac(9,4)]]", "[[frac(5,2)]]"], derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="3|k-1|=|k| → k=3/2 또는 3/4 → 합 9/4.")

# p13
add(id="5d1bc742", qtype="short",
    question="한 직선 위에 있는 세 점 O, A, B에 대하여 [[3 seg(OA) = seg(OB)]]이고 점 A의 위치벡터가 [[vec(a)]]일 때, [[vec(AB) = k vec(a)]]를 만족시키는 모든 실수 [[k]]의 값의 합을 구하시오.",
    choices=None, derived_answer="-2", figure=None, difficulty_est=2, confidence=0.9,
    note="B=±3a → AB=2a 또는 -4a → k 합 -2.")

# p17
add(id="ff187ba7", qtype="short",
    question="세 점 A, B, C의 위치벡터를 각각 [[vec(a)]], [[vec(b)]], [[vec(c)]]라 하고 삼각형 ABC의 무게중심을 G라 하자. [[seg(AB)]]를 [[ratio(1, 3)]]으로 내분하는 점을 P라 할 때, [[vec(GP) = p vec(a) + q vec(b) + r vec(c)]]이다. 실수 [[p]], [[q]], [[r]]에 대하여 [[p + q + r]]의 값을 구하시오.",
    choices=None, derived_answer="0", figure=None, difficulty_est=2, confidence=0.9,
    note="GP=(3a+b)/4-(a+b+c)/3 = 5/12 a - 1/12 b - 1/3 c → 합 0.")

# p21
add(id="cccd7133", qtype="short",
    question="삼각형 ABC의 무게중심 G에 대하여 [[vec(GA) = vec(a) - 2 vec(b)]], [[vec(GB) = vec(a) + vec(b)]]라 하라 때, [[vec(BC) = m vec(a) + n vec(b)]]이다.\n이때 실수 [[m]], [[n]]에 대하여 [[m + n]]의 값을 구하시오.",
    choices=None, derived_answer="-3", figure=None, difficulty_est=2, confidence=0.9,
    note="GC=-(GA+GB)=-2a+b, BC=GC-GB=-3a → m=-3, n=0 → -3. 원문 '라 하라 때'(오타) 그대로 전사.")

# p39
add(id="aea63f87", qtype="short",
    question="다음 그림과 같이 삼각형 ABC에서 선분 BC의 중점을 D라 하면 [[4 vec(AE) = 5 vec(AC)]], [[vec(AF) = l vec(AD)]] ([[l > 1]])을 만족시키는 두 점 E, F와 점 B는 한 직선 위에 있다.\n두 삼각형 AEF, BDF의 넓이를 각각 [[sub(S,1)]], [[sub(S,2)]]라 할 때, [[frac(sub(S,1), sub(S,2))]]의 값을 구하시오.",
    choices=None, derived_answer="frac(25,2)",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 왼쪽, B 위, C 아래). BC의 중점 D(BD=DC 표시), AC의 연장선 위 점 E, AD의 연장선 위 점 F, B·F·E 한 직선. 삼각형 AEF 초록 음영, 삼각형 BDF 보라 음영"}}],
    difficulty_est=4, confidence=0.85,
    needs_review=FIG_REVIEW + ": 삼각형 ABC와 점 D, E, F 및 음영 삼각형",
    note="A 원점, F=(5/9)(b+c), l=10/9; S₁=(25/36)T, S₂=(1/18)T → 25/2.")

# p43
add(id="8a113752", qtype="short",
    question="다음 그림과 같은 삼각형 ABC에서 점 M은 선분 BC의 중점이고, 점 G는 삼각형 ABC의 무게중심이다.\n[[vec(AB) = vec(a)]], [[vec(AC) = vec(b)]]라 할 때, [[vec(BG) = m vec(a) + n vec(b)]]이다. 실수 [[m]], [[n]]에 대하여 [[2m + 7n]]의 값을 구하시오.",
    choices=None, derived_answer="1",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), BC의 중점 M(BM=MC 표시), 중선 AM 위의 무게중심 G, 벡터 AB=a, AC=b, BG 화살표"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 삼각형과 벡터 화살표 그림",
    note="BG=(a+b)/3-a=-2/3 a+1/3 b → 2m+7n=-4/3+7/3=1.")

# p48
add(id="d2185d19", qtype="choice",
    question="그림과 같은 삼각형 ABC에서 [[angle(BAD) = angle(CAD)]]이고 [[seg(AB) = 5]], [[seg(AC) = 3]]이다. [[vec(AD) = m vec(AB) + n vec(AC)]]일 때, 두 실수 [[m]], [[n]]에 대하여 [[m - n]]의 값은?",
    choices=["[[-frac(1,8)]]", "[[-frac(1,4)]]", "0", "[[frac(1,4)]]", "[[frac(1,8)]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AB=5, AC=3 표기, 각 A의 이등분선이 BC와 만나는 점 D, 같은 각 표시"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 삼각형과 각의 이등분선 그림",
    note="BD:DC=5:3 → AD=(3AB+5AC)/8 → m-n=-1/4.")

# p53
add(id="86f7419b", qtype="short",
    question="다음 그림과 같은 삼각형 OAB에서 두 변 OA, OB의 중점을 각각 M, N이라 하고 [[seg(AN)]]과 [[seg(BM)]]의 교점을 G라 하자. [[vec(OA) = vec(a)]], [[vec(OB) = vec(b)]]라 할 때, [[vec(AG) = x vec(a) + y vec(b)]]를 만족시키는 실수 [[x]], [[y]]에 대하여 [[x - y]]의 값을 구하시오.",
    choices=None, derived_answer="-1",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 OAB(O 위, A 왼쪽 아래, B 오른쪽 아래), OA·OB의 중점 M, N(같은 길이 표시), 선분 AN과 BM의 교점 G, 벡터 a, b와 AG 화살표"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 삼각형과 벡터 화살표 그림",
    note="G 무게중심, AG=(a+b)/3-a → x=-2/3, y=1/3 → x-y=-1.")

# p66
add(id="07e11ab8", qtype="choice",
    question="평면 위의 점 P와 삼각형 ABC에 대하여 [[vec(PA) + vec(PB) + 2 vec(PC) = vec(0)]]일 때, 옳은 것만을 보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. 점 P는 삼각형 ABC의 내부에 있다.\nㄴ. [[ratio(tri(PAB), tri(PBC), tri(PCA)) = ratio(2, 1, 1)]]\nㄷ. [[abs(vec(PA)) = abs(vec(PB))]]이면 [[perp(vec(AB), vec(CP))]]이다.",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="P=(A+B+2C)/4 내부 ㄱ✓, 넓이비 2:1:1 ㄴ✓, P=(M+C)/2(M은 AB 중점)이므로 PA=PB ⇒ C가 AB의 수직이등분선 위 ⇒ AB⊥CP ㄷ✓ → ⑤.")

# p83
add(id="946ceefc", qtype="short",
    question="두 초점이 [[F(10, 0)]], F′[[point(-10, 0)]]이고, 주축의 길이가 15인 쌍곡선이 있다. 쌍곡선 위의 [[seg(PF)]] < PF′인 점 P에 대하여 점 Q가 ([[abs(vec(FP)) + 2]])F′Q→ = [[13 vec(QP)]]를 만족시킨다. 점 [[A(-22, -5)]]에 대하여 [[abs(vec(AQ))]]의 최댓값을 구하시오.",
    choices=None, derived_answer="26", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 PF′, 벡터 F′Q) 텍스트 혼합",
    note="출처 [2024년 6월 고3 기하 30번 변형]. F′Q=13(|FP|+15)/(|FP|+15)=13 → Q는 F′ 중심 반지름 13 원 위, |AF′|=13 → 최댓값 26.")

# p84
add(id="2a167cd3", qtype="short",
    question="두 초점이 [[F(5, 0)]], F′[[point(-5, 0)]]이고, 주축의 길이가 6인 쌍곡선이 있다. 쌍곡선 위의 [[seg(PF)]] < PF′인 점 P에 대하여 점 Q가 ([[abs(vec(FP)) + 1]])F′Q→ = [[5 vec(QP)]]를 만족시킨다.\n점 [[A(-9, -3)]]에 대하여 [[abs(vec(AQ))]]의 최댓값을 구하시오.",
    choices=None, derived_answer="10", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 PF′, 벡터 F′Q) 텍스트 혼합",
    note="출처 [2024년 6월 고3 기하 30번/4점]. F′Q=5 → Q는 F′ 중심 반지름 5 원 위, |AF′|=5 → 최댓값 10.")

# ===================== 삼수선 정리 =====================
# p2
add(id="a93bd0ec", qtype="choice",
    question="그림과 같이 평면 [[alpha]] 위에 넓이가 24인 삼각형 ABC가 있다. 평면 [[alpha]] 위에 있지 않은 점 P에서 평면 [[alpha]]에 내린 수선의 발을 H, 직선 AB에 내린 수선의 발을 Q라 하자.\n점 H가 삼각형 ABC의 무게중심이고,\n[[seg(PH) = 4]], [[seg(AB) = 8]]일 때, 선분 PQ의 길이는?",
    choices=["[[3 sqrt(2)]]", "[[2 sqrt(5)]]", "[[sqrt(22)]]", "[[2 sqrt(6)]]", "[[sqrt(26)]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "평면 α 위의 삼각형 ABC, 평면 밖의 점 P에서 내린 수선의 발 H(삼각형 내부, 직각 표시), 선분 AB 위의 수선의 발 Q(직각 표시), 선분 PH·PQ 표시"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 평면 위 삼각형과 수선 그림",
    note="출처 [2018년 9월 고3 이과 12번/3점]. C에서 AB까지 거리 6 → HQ=2 → PQ=√(16+4)=2√5.")

# p3
add(id="661e67dd", qtype="choice",
    question="평면 [[alpha]] 위에 있는 서로 다른 두 점 A, B를 지나는 직선을 [[l]]이라 하고, 평면 [[alpha]] 위에 있지 않은 점 P에서 평면 [[alpha]]에 내린 수선의 발을 H라 하자. [[seg(AB) = seg(PA) = seg(PB) = 6]], [[seg(PH) = 4]]일 때, 점 H와 직선 [[l]] 사이의 거리는?",
    choices=["[[sqrt(11)]]", "[[2 sqrt(3)]]", "[[sqrt(13)]]", "[[sqrt(14)]]", "[[sqrt(15)]]"], derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "평면 α 위의 직선 l과 그 위의 두 점 A, B, 평면 밖의 점 P와 수선의 발 H, 점선 PA·PB·PH"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 평면 위 직선과 수선 그림",
    note="출처 [2014년 11월 고3 이과 12번/3점]. AB 중점 M, PM=3√3, HM=√(27-16)=√11.")

# p9
add(id="263b2885", qtype="short",
    question="평면 [[alpha]] 위에 [[angle(A) = deg(90)]]이고 [[seg(BC) = 4 sqrt(2)]]인 직각이등변삼각형 ABC가 있다. 평면 [[alpha]] 밖의 한 점 P에서 평면 [[alpha]]에 내린 수선의 발이 A이고 점 P에서 이 평면까지의 거리가 1일 때, 점 P에서 직선 BC까지의 거리를 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="A에서 BC까지 거리 2√2, PA=1 → √(1+8)=3.")

# p10
add(id="30aa01bf", qtype="short",
    question="공간에서 평면 [[alpha]] 위에 세 변의 길이가\n[[seg(AB) = seg(AC) = 10]], [[seg(BC) = 12]]인 삼각형 ABC가 있다.\n점 A를 지나고 평면 [[alpha]]에 수직인 직선 [[l]] 위의 점 D에 대하여 [[seg(AD) = 6]]이 되도록 점 D를 잡을 때, [[tri(DBC)]]의 넓이를 구하시오.",
    choices=None, derived_answer="60", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2006년 10월 고3 이과 24번]. A에서 BC까지 8, D에서 BC까지 10 → 60.")

# p13
add(id="1e91293c", qtype="short",
    question="좌표공간에서 서로 수직인 두 평면 [[alpha]]와 [[beta]]가 있다.\n평면 [[alpha]] 위의 두 점 A, B에 대하여 [[seg(AB) = 12]]이고 직선 AB는 평면 [[beta]]에 평행하다. 점 A와 평면 [[beta]] 사이의 거리가 6이고, 평면 [[beta]] 위의 점 P와 평면 [[alpha]] 사이의 거리는 8일 때 삼각형 PAB의 넓이를 구하시오.",
    choices=None, derived_answer="60", figure=None, difficulty_est=2, confidence=0.9,
    note="P에서 직선 AB까지 거리 √(36+64)=10 → 넓이 60.")

# p16
add(id="070863b7", qtype="choice",
    question="다음 그림과 같이 평면 [[alpha]] 위에 있는\n서로 다른 두 점 A, B를 지나는 직선을 [[l]]이라 하고, 평면 [[alpha]] 위에 있지 않은 점 P에서 평면 [[alpha]]에 내린 수선의 발을 H라 하자. [[seg(AB) = seg(PA) = seg(PB) = 10]], [[seg(PH) = 4]]일 때, 점 H와 직선 [[l]] 사이의 거리는?",
    choices=["[[2 sqrt(14)]]", "[[sqrt(57)]]", "[[sqrt(58)]]", "[[sqrt(59)]]", "[[2 sqrt(15)]]"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "평면 α 위의 직선 l과 그 위의 두 점 A, B, 평면 밖의 점 P와 수선의 발 H, 점선 PA·PB·PH"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 평면 위 직선과 수선 그림",
    note="PM=5√3(M은 AB 중점), HM=√(75-16)=√59.")

# p18
add(id="7d38f92e", qtype="choice",
    question="길이가 6인 선분 AB를 지름으로 하는 구 위에 점 C가 있다. 점 A를 지나고 직선 AB에 수직인 직선 [[l]]이 직선 BC에 수직이다. 직선 [[l]] 위의 점 D에 대하여 [[seg(BD) = 9]], [[seg(CD) = 7]]일 때, 선분 AC의 길이는?\n(단, 점 C는 선분 AB 위에 있지 않다.)",
    choices=["[[sqrt(3)]]", "2", "[[sqrt(5)]]", "[[sqrt(6)]]", "[[sqrt(7)]]"], derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2016년 10월 고3 이과 15번 변형]. l⊥평면 ABC, AD²=81-36=45, AC²=49-45=4 → 2.")

# p19
add(id="6d9e4974", qtype="choice",
    question="좌표공간에 [[seg(AB) = 8]], [[seg(BC) = 6]], [[angle(ABC) = frac(pi, 2)]]인 직각삼각형 ABC와 선분 AC를 지름으로 하는 구 [[S]]가 있다. 직선 AB를 포함하고 평면 ABC에 수직인 평면이 구 [[S]]와 만나서 생기는 원을 [[O]]라 하자. 원 [[O]] 위의 점 중 직선 AC까지의 거리가 4인 서로 다른 두 점을 P, Q라 할 때, 선분 PQ의 길이는?",
    choices=["[[sqrt(43)]]", "[[sqrt(47)]]", "[[sqrt(51)]]", "[[sqrt(55)]]", "[[sqrt(59)]]"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "구 S(초록 음영) 위의 세 점 A, B, C와 삼각형 ABC, 직선 AB를 포함하는 수직 평면이 구와 만나는 원 O(A, B를 지남)"}}],
    difficulty_est=4, confidence=0.85,
    needs_review=FIG_REVIEW + ": 구와 삼각형, 절단 원 그림",
    note="출처 [2024년 11월 고3 기하 28번/4점]. B 원점, A(8,0,0), C(0,6,0); 원 O: 중심 (4,0,0) 반지름 4, y=0. 거리 조건 → x=11/2, z=±√55/2 → PQ=√55.")

# p27
add(id="7ee212bf", qtype="choice",
    question="밑면의 반지름의 길이가 2, 높이가 2인 원기둥이 있다.\n이 원기둥의 한 밑면의 둘레 위의 한 점 P에서 다른 밑면에 내린 수선의 발을 P′이라 하고, 점 P를 포함하는 밑면의 중심을 O라 하자. 점 P′을 포함하는 밑면의 둘레 위의 서로 다른 두 점 A, B에 대하여 점 O에서 선분 AB에 내린 수선의 발을 H라 하자. BP′ = 4, [[seg(OH) = sqrt(5)]]일 때, 삼각형 PAH의 넓이는?",
    choices=["[[frac(sqrt(6), 2)]]", "[[frac(3 sqrt(6), 4)]]", "[[sqrt(6)]]", "[[frac(5 sqrt(6), 4)]]", "[[frac(3 sqrt(6), 2)]]"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원기둥. 윗면 둘레 위 점 P와 윗면 중심 O, 아랫면의 P′(직각 표시), 아랫면 둘레 위 점 A, B와 선분 AB 위의 수선의 발 H(직각 표시), 삼각형 PAH 음영"}}],
    difficulty_est=4, confidence=0.8,
    needs_review=FIG_REVIEW + ": 원기둥과 삼각형 PAH 그림 / " + PRIME + "(P′, 선분 BP′) 텍스트 혼합",
    note="출처 [2024년 7월 고3 기하 27번 변형]. BP′ 지름, O′H=1 → AB=2√3, P′A=2, PA=2√2, AH=√3 → 넓이 √6.")

# p29
add(id="f016ed69", qtype="choice",
    question="그림과 같이 [[seg(BC) = 6]], [[angle(BAC) = deg(90)]]인 삼각형 ABC에 대하여 점 A를 지나고 평면 ABC에 수직인 직선 위에 [[seg(AD) = 3]]인 점 D가 있다. 삼각형 BCD의 넓이가 12일 때, 사면체 DABC의 부피는?",
    choices=["[[3 sqrt(6)]]", "[[2 sqrt(15)]]", "[[3 sqrt(7)]]", "[[6 sqrt(2)]]", "[[4 sqrt(5)]]"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 DABC: 밑면 삼각형 ABC(A에서 직각 표시, BC=6), A 위로 수직인 DA=3, 면 음영"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 사면체 그림",
    note="D에서 BC까지 4, A에서 BC까지 √7 → △ABC=3√7 → 부피 3√7.")

# p30
add(id="4959e6f9", qtype="choice",
    question="그림과 같이 지름의 길이가 5인 두 원 [[sub(C,1)]], [[sub(C,2)]]를 두 밑면으로 하는 원기둥이 있고, 원 [[sub(C,1)]] 위의 [[seg(AB) = 5]]인 두 점 A, B와 원 [[sub(C,2)]] 위의 [[seg(CD) = 3]]인 두 점 C, D에 대하여 [[seg(AD) = seg(BC)]]이다. 점 D에서 원 [[sub(C,1)]]을 포함하는 평면에 내린 수선의 발을 H라 하자. 사각형 ABCD의 넓이가 삼각형 ABH의 넓이의 4배일 때, 이 원기둥의 높이는?",
    choices=["[[3 sqrt(2)]]", "[[sqrt(19)]]", "[[2 sqrt(5)]]", "[[sqrt(21)]]", "[[sqrt(22)]]"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원기둥. 아랫면 원 C₁ 위의 점 A, B, 윗면 원 C₂ 위의 점 C, D, D에서 아랫면에 내린 수선의 발 H, 선분 AD·BC·AH·BH 표시"}}],
    difficulty_est=4, confidence=0.85,
    needs_review=FIG_REVIEW + ": 원기둥과 사각형 ABCD 그림",
    note="출처 [2025년 11월 고3 기하 27번/3점]. AB 지름, HC′=3 → H는 AB에서 거리 2, △ABH=5, 등변사다리꼴 높이 5 → h²=25-4=21.")

# p33
add(id="b311d4c2", qtype="short",
    question="[[seg(AB) = 8]], [[angle(ACB) = deg(90)]]인 삼각형 ABC에 대하여 점 C를 지나고 평면 ABC에 수직인 직선 위에 [[seg(CD) = 4]]인 점 D가 있다. 삼각형 ABD의 넓이가 20일 때, 삼각형 ABC의 넓이를 구하시오.",
    choices=None, derived_answer="12",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 DABC: 밑면 삼각형 ABC(C에서 직각 표시), C 위로 수직인 점선 DC, 모서리 DA·DB"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 사면체 그림",
    note="출처 [2017년 9월 고3 이과 25번/3점]. D에서 AB까지 5 → C에서 AB까지 3 → 넓이 12.")

# p37
add(id="2c5bffff", qtype="choice",
    question="그림과 같이 두 평면 [[alpha]], [[beta]]의 교선 위에 두 점 A, P가 있고, 두 평면 [[alpha]], [[beta]] 위에 각각 두 점 Q, R가 있다.\n[[angle(QAP) = deg(45)]], [[angle(RAP) = deg(30)]]이고, [[perp(seg(AP), seg(PQ))]], [[perp(seg(AP), seg(PR))]], [[seg(AQ) = 3 sqrt(2)]], [[seg(QR) = sqrt(6)]]이다. 두 평면 [[alpha]], [[beta]]가 이루는 예각의 크기를 [[theta]]라 할 때, [[sin(theta)]]의 값은?",
    choices=["[[frac(sqrt(6), 3)]]", "[[frac(2,3)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(2), 3)]]", "[[frac(1,3)]]"], derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "교선을 공유하는 두 평면 α(위), β(아래). 교선 위의 점 A, P, α 위의 점 Q, β 위의 점 R. 각 45°(QAP), 30°(RAP), P에서 직각 표시, AQ=3√2, QR=√6 표기"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 두 평면과 이면각 그림",
    note="PQ=AP=3, PR=√3, cos θ=(9+3-6)/(2·3·√3)=1/√3 → sin θ=√6/3.")

# p38
add(id="086f982c", qtype="short",
    question="그림과 같이 두 평면 [[alpha]], [[beta]]의 교선 위의 두 점 A, B와 평면 [[alpha]] 위의 점 P, 평면 [[beta]] 위의 점 Q에 대하여 [[angle(PAB) = deg(30)]], [[angle(QAB) = deg(60)]], [[perp(seg(PB), seg(AB))]], [[perp(seg(QB), seg(AB))]]이고, [[seg(AB) = sqrt(3)]], [[seg(PQ) = sqrt(14)]]이다. 두 평면 [[alpha]], [[beta]]가 이루는 각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(2,3)",
    figure=[{"fn": "unsupported", "args": {"raw": "교선을 공유하는 두 평면 α(위), β(아래). 교선 위의 점 A, B, α 위의 점 P, β 위의 점 Q. 각 30°(PAB), 60°(QAB), B에서 직각 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=FIG_REVIEW + ": 두 평면과 이면각 그림",
    note="PB=1, QB=3, cos∠PBQ=(1+9-14)/6=-2/3 → 두 평면이 이루는 각(예각) cos θ=2/3 (빠른정답 2/3 일치).")

# p40
add(id="168d4246", qtype="choice",
    question="다음 그림과 같이 두 평면 [[alpha]], [[beta]]의 교선 위에 두 점 A, P가 있고, 두 평면 [[alpha]], [[beta]] 위에 각각 두 점 Q, R가 있다.\n[[angle(QAP) = deg(60)]], [[angle(RAP) = deg(45)]]이고,\n[[perp(seg(AP), seg(PQ))]], [[perp(seg(AP), seg(PR))]], [[seg(AQ) = 4 sqrt(3)]], [[seg(QR) = 2 sqrt(6)]]이다.\n두 평면 [[alpha]] [[beta]]가 이루는 예각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값은?",
    choices=["[[frac(sqrt(6), 3)]]", "[[frac(2,3)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(2), 3)]]", "[[frac(1,3)]]"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "교선을 공유하는 두 평면 α(위), β(아래). 교선 위의 점 A, P, α 위의 점 Q, β 위의 점 R. 각 60°(QAP), 45°(RAP), P에서 직각 표시, AQ=4√3, QR=2√6 표기"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 두 평면과 이면각 그림",
    note="AP=2√3, PQ=6, PR=2√3; cos θ=(36+12-24)/(2·6·2√3)=1/√3=√3/3. 원문 '두 평면 α β가'(쉼표 없음) 그대로.")

# p41
add(id="cf43dbe6", qtype="choice",
    question="다음 그림과 같이 두 평면 [[alpha]], [[beta]]의 교선 위에 두 점 A, P가 있고, 두 평면 [[alpha]], [[beta]] 위에 각각 두 점 Q, R가 있다.\n[[angle(QAP) = deg(45)]], [[angle(RAP) = deg(60)]]이고, [[perp(seg(AP), seg(PQ))]], [[perp(seg(AP), seg(PR))]], [[seg(AQ) = seg(QR) = 4 sqrt(2)]]이다. 두 평면 [[alpha]], [[beta]]가 이루는 예각의 크기를 [[theta]]라 할 때, [[sin(theta)]]의 값은?",
    choices=["[[frac(1,3)]]", "[[frac(sqrt(2), 3)]]", "[[frac(sqrt(3), 3)]]", "[[frac(2,3)]]", "[[frac(sqrt(6), 3)]]"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "교선을 공유하는 두 평면 α(위), β(아래). 교선 위의 점 A, P, α 위의 점 Q, β 위의 점 R. 각 45°(QAP), 60°(RAP), P에서 직각 표시, AQ=4√2, QR=4√2 표기"}}],
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 두 평면과 이면각 그림",
    note="AP=PQ=4, PR=4√3; cos θ=(16+48-32)/(2·4·4√3)=1/√3 → sin θ=√6/3.")

# p47
add(id="dcabaab5", qtype="choice",
    question="다음 그림과 같이 평면 [[alpha]] 밖의 한 점 A에서 [[alpha]] 위의 직선 [[l]]과 평면 [[alpha]]에 내린 수선의 발을 각각 M, N이라 하자. [[seg(AM) = 8]], [[seg(AN) = 4]]일 때, 점 A와 직선 [[l]]에 의하여 결정되는 평면이 평면 [[alpha]]와 이루는 각의 크기는?",
    choices=["[[deg(15)]]", "[[deg(30)]]", "[[deg(45)]]", "[[deg(60)]]", "[[deg(75)]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "평면 α 위의 직선 l과 그 위의 수선의 발 M(직각 표시), 평면 밖의 점 A와 수선의 발 N(직각 표시), AM=8, AN=4 표기"}}],
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 평면과 수선 그림",
    note="sin∠AMN=4/8=1/2 → 30°.")

# p50
add(id="e6b3273c", qtype="choice",
    question="다음 그림과 같이 서로 다른 두 평면 [[alpha]], [[beta]]의 교선 위에 [[seg(AB) = 27]]인 두 점 A, B가 있다. 선분 AB를 지름으로 하는 원 [[sub(C,1)]]이 평면 [[alpha]] 위에 있고, 선분 AB를 장축으로 하고 두 점 F, F′을 초점으로 하는 타원 [[sub(C,2)]]가 평면 [[beta]] 위에 있다. 원 [[sub(C,1)]] 위의 한 점 P에서 평면 [[beta]]에 내린 수선의 발을 H라 할 때, HF′ < [[seg(HF)]]이고 ∠HFF′ = [[frac(pi, 6)]]이다.\n직선 HF와 타원 [[sub(C,2)]]가 만나는 점 중 점 H와 가까운 점을 Q라 하면 [[seg(FH) < seg(FQ)]]이다. 점 H를 중심으로 하고 점 Q를 지나는 평면 [[beta]] 위의 원은 반지름의 길이가 6이고 직선 AB에 접한다. 두 평면 [[alpha]], [[beta]]가 이루는 각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값은?\n(단, 점 P는 평면 [[beta]] 위에 있지 않다.)",
    choices=["[[frac(sqrt(2), 3)]]", "[[frac(2 sqrt(74), 37)]]", "[[frac(2 sqrt(19), 19)]]", "[[frac(2 sqrt(78), 39)]]", "[[frac(sqrt(5), 5)]]"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "교선 AB를 공유하는 두 평면 α(아래), β(위). α 위의 원 C₁(지름 AB)과 그 위의 점 P, β 위의 타원 C₂(장축 AB, 초점 F, F′), P에서 β에 내린 수선의 발 H, 직선 HF와 타원의 교점 Q, H 중심 원(점선), 이면각 θ 표시"}}],
    difficulty_est=5, confidence=0.8,
    needs_review=FIG_REVIEW + ": 두 평면 위의 원·타원 복합 입체도형 / " + PRIME + "(F′, 선분 HF′, ∠HFF′) 텍스트 혼합",
    note="출처 [2023년 11월 고3 기하 28번 변형]. 원문(AB=18, r=4)의 3/2배 확대 → F′Q=13→ 비례, c=9√3/2, H는 AB에서 6, K=(-3√3/2,0), PK²=351/2 → cos θ=6/√(351/2)=2√78/39.")

# p51
add(id="3492b871", qtype="choice",
    question="그림과 같이 서로 다른 두 평면 [[alpha]], [[beta]]의 교선 위에 [[seg(AB) = 18]]인 두 점 A, B가 있다. 선분 AB를 지름으로 하는 원 [[sub(C,1)]]이 평면 [[alpha]] 위에 있고, 선분 AB를 장축으로 하고 두 점 F, F′을 초점으로 하는 타원 [[sub(C,2)]]가 평면 [[beta]] 위에 있다. 원 [[sub(C,1)]] 위의 한 점 P에서 평면 [[beta]]에 내린 수선의 발을 H라 할 때, HF′ < [[seg(HF)]]이고 ∠HFF′ = [[frac(pi, 6)]]이다.\n직선 HF와 타원 [[sub(C,2)]]가 만나는 점 중 점 H와 가까운 점을 Q라 하면 [[seg(FH) < seg(FQ)]]이다. 점 H를 중심으로 하고 점 Q를 지나는 평면 [[beta]] 위의 원은 반지름의 길이가 4이고 직선 AB에 접한다. 두 평면 [[alpha]], [[beta]]가 이루는 각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값은?\n(단, 점 P는 평면 [[beta]] 위에 있지 않다.)",
    choices=["[[frac(2 sqrt(66), 33)]]", "[[frac(4 sqrt(69), 69)]]", "[[frac(sqrt(2), 3)]]", "[[frac(4 sqrt(3), 15)]]", "[[frac(2 sqrt(78), 39)]]"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "교선 AB를 공유하는 두 평면 α(아래), β(위). α 위의 원 C₁(지름 AB)과 그 위의 점 P, β 위의 타원 C₂(장축 AB, 초점 F, F′), P에서 β에 내린 수선의 발 H, 직선 HF와 타원의 교점 Q, H 중심 원(점선), 이면각 θ 표시"}}],
    difficulty_est=5, confidence=0.8,
    needs_review=FIG_REVIEW + ": 두 평면 위의 원·타원 복합 입체도형 / " + PRIME + "(F′, 선분 HF′, ∠HFF′) 텍스트 혼합",
    note="출처 [2023년 11월 고3 기하 28번/4점]. HF=8, Q=(3H-F)/2, QF=12, QF′=6 → c=3√3, H(-√3,4); PK²=81-3=78, HK=4 → cos θ=4/√78=2√78/39.")
