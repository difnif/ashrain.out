# -*- coding: utf-8 -*-
# esc_sonnet_h1-1_1of4 — 이미지 기준 전사 (80 항목 / 80쪽, 중복 이미지 없음)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_2 = ["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ"]

# ───────── 이차방정식의 풀이 ─────────
# p2
add(id="c013f7a3", qtype="short",
    question="방정식 [[(pow(a,2) - 3) x - 1 = a(2x + 1)]]의 해가 존재하지 않기 위한 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="(a-3)(a+1)x = a+1 → a=3이면 0·x=4 해 없음 → 3.")

# p6
add(id="40136dab", qtype="choice",
    question=("[[x]]보다 작거나 같은 정수 중에서 최대의 정수를 [[floor(x)]], [[x]]보다 크거나 같은 정수 중에서 최소의 정수를 <[[x]]>로 나타낼 때, "
              "방정식 [[floor(x)]] + <[[x]]> = 7의 해를 구하면?"),
    choices=["[[frac(7,2)]]", "[[3 <= x <= 4]]", "[[3 <= x < 4]]", "[[3 < x <= 4]]", "[[3 < x < 4]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: 정의 기호 <x>(올림) 표현 불가 → 텍스트 혼합",
    note="x 정수면 2x=7 불가, 정수 아니면 2[x]+1=7 → [x]=3 → 3<x<4 → ⑤.")

# p42
add(id="e329dd7f", qtype="short",
    question=("그림은 어느 지역에 있는 토지를 정사각형 ABCD로 나타낸 것이다. 변 AD 위에 [[seg(AE) = 5]] m가 되는 점 E와 "
              "변 CD 위에 [[seg(CF) = 3]] m가 되는 점 F를 일직선으로 연결한 경계선을 만들었다. 오각형 ABCFE의 넓이가 [[129 pow(m,2)]]일 때, "
              "정사각형 ABCD의 넓이는 [[a pow(m,2)]]이다.\n[[a]]의 값을 구하시오."),
    choices=None, derived_answer="169",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상), 변 AD 위 점 E(AE=5m), 변 CD 위 점 F(CF=3m), 선분 EF로 잘린 오각형 ABCFE 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 위 오각형 음영 도형",
    note="출처 [2015년 3월 고1 27번/4점]. 한 변 s: s²−(s−5)(s−3)/2=129 → s²+8s−273=0 → s=13 → a=169.")

# p46
add(id="33ea1858", qtype="choice",
    question=("다음 그림과 같이 반원에 내접하는 가장 큰 원 [[C]]와 반원에 내접하고 원 [[C]]에 외접하는 원 C′이 있다. [[seg(AB) = 16]]일 때, "
              "두 원 [[C]], C′의 반지름의 길이를 두 근으로 하고 [[pow(x,2)]]의 계수가 1인 이차방정식은?"),
    choices=["[[pow(x,2) - 8x + 12 = 0]]", "[[pow(x,2) - 8 sqrt(2) x + 16 = 0]]", "[[pow(x,2) - 12x + 32 = 0]]",
             "[[pow(x,2) - 12 sqrt(2) x + 64 = 0]]", "[[pow(x,2) - 16x + 32 = 0]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "반원 안에 큰 원 C(지름 위 점 A에 접함)와 작은 원 C′(지름 위 점 B에 접함), 두 중심에서 지름에 내린 수선(직각 표시), AB=16"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 반원+내접원 2개 복합 도형 / 프라임 라벨 C′ 텍스트",
    note="반원 반지름 R: C 반지름 R/2, C′ 반지름 R/4, AB=R/√2=16 → R=16√2 → 두 근 8√2, 4√2 → 합 12√2, 곱 64 → ④.")

# p89
add(id="69a1b041", qtype="short",
    question="[[x]], [[y]]에 대한 이차식 [[pow(x,2) + 2x y - 2 pow(y,2) + 6x + 2y - a]]가 두 일차식의 곱으로 인수분해될 때, 실수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="frac(-23,3)", figure=None, difficulty_est=3, confidence=0.9,
    note="x에 대한 판별식 12y²+16y+36+4a가 완전제곱 → 256−48(36+4a)=0 → a=−23/3.")

# p92
add(id="b0e98270", qtype="short",
    question=("[[x]], [[y]]에 대한 이차식 [[2 pow(x,2) + 5x y - 3 pow(y,2) + k y + 8x + 6]]이 [[x]], [[y]]에 대한 두 일차식의 곱으로 인수분해될 때, "
              "정수 [[k]]의 값을 구하시오. (단, [[k > 10]])"),
    choices=None, derived_answer="17", figure=None, difficulty_est=3, confidence=0.9,
    note="(2x−y+p)(x+3y+q): 2q+p=8, pq=6, k=3p−q → (p,q)=(6,1) → k=17.")

# p93
add(id="c7567b00", qtype="short",
    question="[[x]], [[y]]에 대한 이차식 [[pow(x,2) + 3x y + 2 pow(y,2) + 8x + 3y - a]]가 두 일차식의 곱으로 인수분해될 때, 실수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="65", figure=None, difficulty_est=3, confidence=0.9,
    note="(x+y+p)(x+2y+q): p+q=8, 2p+q=3 → p=−5, q=13 → pq=−65=−a → a=65.")

# ───────── 다항식의 인수분해 ─────────
# p3
add(id="46bb49a2", qtype="choice",
    question="[[2a pow(x,2) y + 3a x pow(y,2)]]을 인수분해하면?",
    choices=["[[a x(2x + 3y)]]", "[[a y(2 pow(x,2) + 3 pow(y,2))]]", "[[a x y(2x + 3y)]]", "[[a x y(3x + 2y)]]", "[[a pow(x,2)(2 + 3y)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="공통인수 axy → axy(2x+3y) → ③.")

# p14
add(id="2c3dcf57", qtype="choice",
    question=("[[(pow(x,2) - x)(pow(x,2) + 3x + 2) - 3]]을 인수분해하면\n[[(pow(x,2) + a x + b)(pow(x,2) + c x + d)]]이다.\n"
              "이때, [[a + b + c + d]]의 값은? (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)"),
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2007년 11월 고1 16번]. t=x²+x: t(t−2)−3=(t−3)(t+1) → (x²+x−3)(x²+x+1) → 합 0 → ③.")

# p36
add(id="287d04e4", qtype="choice",
    question="다음 중 [[(a + b + c)(a b + b c + c a) - a b c]]의 인수가 아닌 것은?",
    choices=["[[a + b]]", "[[b + c]]", "[[c + a]]", "[[b - a]]", "[[-b - c]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="주어진 식 = (a+b)(b+c)(c+a) → b−a는 인수 아님 → ④ (빠른정답 2와 불일치).")

# p37
add(id="ac123916", qtype="short",
    question=("[[frac(2x y(-x + 2y) - x z(z - x) + 2y z(z - 2y), (x - 2y)(2y - z)(x - z))]]의 값을 구하시오. "
              "(단, [[x != 2y]], [[2y != z]], [[x != z]])"),
    choices=None, derived_answer="-1", figure=None, difficulty_est=3, confidence=0.9,
    note="분자 = −(x−2y)(2y−z)(x−z) → 값 −1 (sympy 확인).")

# p38
add(id="9b37beda", qtype="short",
    question="서로 다른 세 실수 [[a]], [[b]], [[c]]에 대하여\n[[frac(a b(a - b) + b c(b - c) + c a(c - a), (a - b)(b - c)(c - a))]]의 값을 구하시오.",
    choices=None, derived_answer="-1", figure=None, difficulty_est=3, confidence=0.9,
    note="분자 = −(a−b)(b−c)(c−a) → −1 (빠른정답 3과 불일치).")

# p46
add(id="db5f09ed", qtype="choice",
    question=("자연수 [[x]]에 대하여 [[pow(x,4) + pow(x,3) + pow(x,2) + x + 1]]이 어떤 자연수의 제곱이 되는 [[x]]의 개수를 구하는 과정이다.\n"
              "[[pow(x,4) + pow(x,3) + pow(x,2) + x + 1 = pow(y,2)]] ([[y]]는 자연수)라 하자.\n"
              "[[4 pow(x,4) + 4 pow(x,3) + 4 pow(x,2) + 4x + 4 = pow(2y,2)]]\n"
              "( (가) )² + [[(3 pow(x,2) + 4x + 4)]] = [[pow(2y,2)]] ⋯ ㉠\n"
              "[[pow(2 pow(x,2) + x + 1, 2) - (x - 3)(x + 1) = pow(2y,2)]] ⋯ ㉡\n"
              "[[(x - 3)(x + 1) > 0]] 이면\n㉡에서 [[2 pow(x,2) + x + 1 > 2y]] 이고\n㉠에서 (가) < [[2y]]이므로\n"
              "만족하는 자연수 [[y]]는 존재하지 않는다.\n따라서\n[[(x - 3)(x + 1) <= 0]] 이므로\n[[-1 <= x <= 3]] 이다.\n"
              "그러므로 [[pow(x,4) + pow(x,3) + pow(x,2) + x + 1]]을 어떤 자연수의 제곱이 되게 하는 자연수 [[x]]의 개수는 (나) 개이다.\n"
              "위의 과정에서 (가), (나)에 알맞은 것은?"),
    choices=["(가) [[2 pow(x,2) + 1]], (나) 1", "(가) [[2 pow(x,2) + 2x]], (나) 1", "(가) [[2 pow(x,2) + x]], (나) 1",
             "(가) [[2 pow(x,2) + 2x]], (나) 2", "(가) [[2 pow(x,2) + x]], (나) 2"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2007년 6월 고1 16번]. (가)=2x²+x, x=1,2,3 중 121=11²인 x=3뿐 → (나)=1 → ③ (빠른정답 5와 불일치).")

# p62
add(id="03a0b6d3", qtype="choice",
    question="두 실수 [[a]], [[b]]에 대하여 [[f(a, b) = pow(a,2) + 9a b]]라 할 때,\n[[3a × f(3a, b) + 3b × f(3b, a)]]를 인수분해 하면?",
    choices=["[[pow(2a + 3b, 3)]]", "[[pow(3a + 3b, 3)]]", "[[pow(3a + 4b, 3)]]", "[[pow(4a + 3b, 3)]]", "[[pow(4a + 4b, 3)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="27a³+81a²b+81ab²+27b³=27(a+b)³=(3a+3b)³ → ② (빠른정답 −22와 불일치).")

# p63
add(id="d537541b", qtype="short",
    question=("[[3x + 2y = 7]], [[y + 3z = 5]]를 만족시키는 [[x]], [[y]], [[z]]에 대하여 [ [[x]], [[y]], [[z]] ] = [[pow(x,2) + 2y z]]로 정의할 때,\n"
              "[ [[x]], [[y]], [[z]] ] + [ [[y]], [[z]], [[x]] ] + [ [[z]], [[x]], [[y]] ]의 값을 구하시오."),
    choices=None, derived_answer="16", figure=None, difficulty_est=2, confidence=0.85,
    note="새로운 연산 [x,y,z]는 텍스트 혼합. 합 = (x+y+z)², 두 식 더하면 x+y+z=4 → 16 (빠른정답 2와 불일치).")

# p64
add(id="cdb084a2", qtype="choice",
    question=("세 실수 [[x]], [[y]], [[z]]에 대하여 [ [[x]], [[y]], [[z]] ] = [[pow(x,2) - y z]]라 하자.\n"
              "[ [[x]], [[y]], [[2z]] ] + [ [[y]], [[2z]], [[-x]] ] + [ [[z]], [[x]], [[2y]] ]를 바르게 인수분해한 것은?"),
    choices=["[[pow(x + y + z, 2)]]", "[[pow(x + y - z, 2)]]", "[[pow(x - y + z, 2)]]", "[[pow(x - y - z, 2)]]", "[[(x - y + z)(x + y - z)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="새로운 연산 [x,y,z]는 텍스트 혼합. x²−2yz+y²+2zx+z²−2xy=(x−y+z)² → ③.")

# p65
add(id="b1883870", qtype="choice",
    question="[ [[a]], [[b]], [[c]] ] = [[pow(a,2)(b + c)]]일 때,\n[ [[a]], [[b]], [[c]] ] + [ [[b]], [[c]], [[a]] ] + [ [[c]], [[a]], [[b]] ] + [[2a b c]]의 인수인 것은?",
    choices=["[[a - b]]", "[[b + c]]", "[[c - a]]", "[[a + b + c]]", "[[a b c]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    note="새로운 연산 [a,b,c]는 텍스트 혼합. 식 = (a+b)(b+c)(c+a) → ②.")

# p68
add(id="aa56ebb9", qtype="choice",
    question=("두 실수 [[x]], [[y]]에 대하여 [[x]] ∗ [[y]] = [[x + y + x y]]라 하자.\n"
              "(1 ∗ [[a]]) ∗ [[b]] = 3을 만족시키는 정수 [[a]], [[b]]의 순서쌍 ([[a]], [[b]])의 개수는?"),
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2014년 3월 고2 문과 14번/4점]. 새 연산 ∗는 텍스트. 1∗a=1+2a, (1+2a)∗b=3 → (a+1)(b+1)=2 → 4개 → ②.")

# p90
add(id="df62313e", qtype="choice",
    question="[[a > b > c >= 2]]인 세 자연수 [[a]], [[b]], [[c]]에 대하여\n[[(a + b + c)(a b + b c + c a) - a b c = 594]]일 때, [[a b c]]의 값은?",
    choices=["[[42]]", "[[49]]", "[[56]]", "[[63]]", "[[70]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="(a+b)(b+c)(c+a)=594=6·9·11 → b+c=6, a+c=9, a+b=11 → (7,4,2) → abc=56 → ③.")

# p91
add(id="a2e16997", qtype="short",
    question="[[x + y = 6]], [[x y = 2]]일 때, [[pow(x,2) y + x pow(y,2)]]의 값을 구하시오.",
    choices=None, derived_answer="12", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2018년 6월 고1 22번/3점]. xy(x+y)=12.")

# p95
add(id="935bf994", qtype="choice",
    question=("한 모서리의 길이가 [[x]]인 정육면체 모양의 나무토막이 있다.\n[그림 1]과 같이 이 나무토막의 윗면의 중앙에서 한 변의 길이가 [[y]]인 정사각형의 모양으로 "
              "아랫면의 중앙까지 구멍을 뚫었다.\n구멍은 정사각기둥 모양이고, 각 모서리는 처음 정육면체의 모서리와 평행하다.\n"
              "이와 같은 방법으로 앞면에서 구멍을 뚫어 [그림 2]와 같은 입체도형을 얻었다.\n이때 [그림 2]의 입체도형의 부피를 [[x]], [[y]]로 나타내면?"),
    choices=["[[(x - y)(pow(x,2) + x y - pow(y,2))]]", "[[(x - y)(pow(x,2) + x y + pow(y,2))]]", "[[(x + y)(pow(x,2) + x y - pow(y,2))]]",
             "[[(x + y)(pow(x,2) + x y + pow(y,2))]]", "[[(x + y)(pow(x,2) + x y + 2 pow(y,2))]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "[그림 1] 한 모서리 x인 정육면체에 윗면 중앙에서 아랫면까지 한 변 y인 정사각기둥 구멍(점선), [그림 2] 앞면에서도 같은 구멍을 추가로 뚫은 입체(구멍 입구 음영)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 구멍 뚫린 정육면체 입체도형 그림 2개",
    note="부피 x³−2xy²+y³=(x−y)(x²+xy−y²) → ① (빠른정답 146과 불일치).")

# ───────── 다항식의 사칙연산 ─────────
# p26
add(id="900d1a21", qtype="choice",
    question="[[pow(x + 2y + 1, 2) = 2]]를 만족시키는 [[x]], [[y]]에 대하여\n[[pow(x,2) + 4 pow(y,2) + 4x y + 2x + 4y]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="t=x+2y: (t+1)²=2 → t²+2t=1 → ①.")

# p34
add(id="d7ac98b5", qtype="short",
    question="[[a + b = 6]], [[a b = -2]]일 때, [[pow(a - b, 2)]]의 값을 구하시오.",
    choices=None, derived_answer="44", figure=None, difficulty_est=1, confidence=0.9,
    note="(a+b)²−4ab=36+8=44 (빠른정답 3과 불일치).")

# p37
add(id="208af1a4", qtype="short",
    question="[[x - y = -2]], [[x y = 15]]일 때, 다음 식의 값을 구하시오.\n[[pow(x,3) - pow(y,3)]]",
    choices=None, derived_answer="-98", figure=None, difficulty_est=1, confidence=0.9,
    note="(x−y)³+3xy(x−y)=−8−90=−98. 식은 상자 안에 제시.")

# p64
add(id="6a56bd61", qtype="choice",
    question="다음 나눗셈의 몫과 나머지를 차례대로 나열한 것은?\n[[(4 pow(x,3) - pow(x,2) + 3x - 5) / (pow(x,2) - x + 1)]]",
    choices=["[[-4x - 3]], [[-2x - 8]]", "[[-4x - 3]], [[2x - 8]]", "[[4x + 3]], [[2x - 8]]", "[[4x - 3]], [[2x + 8]]", "[[4x + 3]], [[-2x - 8]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="(x²−x+1)(4x+3)=4x³−x²+x+3, 나머지 2x−8 → ③ (빠른정답 256과 불일치).")

# p77
add(id="44d1d231", qtype="choice",
    question=("다항식 [[f(x)]]를 [[x + frac(4,5)]]로 나누었을 때의 몫과 나머지를 각각 [[Q(x)]], [[R]]라 한다. "
              "다항식 [[f(x)]]를 [[5x + 4]]로 나누었을 때의 몫과 나머지를 차례대로 적은 것은?"),
    choices=["[[Q(x)]], [[R]]", "[[Q(x)]], [[frac(1,5) R]]", "[[frac(1,5) Q(x)]], [[R]]", "[[frac(1,5) Q(x)]], [[5R]]", "[[5Q(x)]], [[5R]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="f(x)=(x+4/5)Q(x)+R=(5x+4)·Q(x)/5+R → ③ (빠른정답 2와 불일치).")

# p80
add(id="e4f93b49", qtype="choice",
    question=("다항식 [[P(x)]]를 [[8x - 2]]로 나누었을 때의 몫을 [[sub(Q,1)(x)]], 나머지를 [[sub(R,1)]]이라 하고 [[x - frac(1,4)]]로 나누었을 때의 몫을 "
              "[[sub(Q,2)(x)]], 나머지를 [[sub(R,2)]]라 할 때, [[frac(sub(Q,2)(x), sub(Q,1)(x)) + frac(sub(R,1), sub(R,2))]]의 값은?\n"
              "(단, [[sub(Q,1)(x) != 0]], [[sub(R,1) != 0]])"),
    choices=["[[8]]", "[[9]]", "[[10]]", "[[11]]", "[[12]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 첨자 함수 Q₁(x) 표기가 병치 곱(sub(Q,1) × (x))으로 파싱됨",
    note="8x−2=8(x−1/4) → Q₂=8Q₁, R₂=R₁ → 8+1=9 → ② (빠른정답 3과 불일치).")

# p84
add(id="43c2f901", qtype="short",
    question=("다항식 [[P(x)]]를 [[10x - 2]]로 나누었을 때의 몫을 [[sub(Q,1)(x)]], 나머지를 [[sub(R,1)]]이라 하고 [[x - frac(1,5)]]로 나누었을 때의 몫을 "
              "[[sub(Q,2)(x)]], 나머지를 [[sub(R,2)]]라 할 때, [[frac(sub(Q,2)(x), sub(Q,1)(x)) + frac(sub(R,2), sub(R,1))]]의 값을 구하시오. "
              "(단, [[sub(Q,1)(x) != 0]], [[sub(R,1) != 0]])"),
    choices=None, derived_answer="11", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 첨자 함수 Q₁(x) 표기가 병치 곱(sub(Q,1) × (x))으로 파싱됨",
    note="10x−2=10(x−1/5) → Q₂=10Q₁, R₂=R₁ → 10+1=11 (빠른정답 2와 불일치).")

# p86
add(id="03c157ac", qtype="choice",
    question=("[[seg(AB) = c]], [[seg(BC) = a]], [[seg(CA) = b]]인 삼각형 ABC에서\n[[(a + b + c)(a + b - c) = (-a + b + c)(a - b + c)]]\n"
              "일 때, 삼각형 ABC는 어떤 삼각형인가?"),
    choices=["[[a = c]]인 이등변삼각형", "[[b = c]]인 이등변삼각형", "[[angle(A) = deg(90)]]인 직각삼각형",
             "[[angle(B) = deg(90)]]인 직각삼각형", "[[angle(C) = deg(90)]]인 직각삼각형"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="전개하면 a²+b²=c² → c=AB의 대각 ∠C=90° → ⑤ (빠른정답 3과 불일치).")

# p87
add(id="a5bc7be2", qtype="short",
    question=("정삼각형 ABC에서 두 변 AB와 AC의 중점을 각각 M, N이라 하자. 다음 그림과 같이 점 P는 반직선 MN이 삼각형 ABC의 외접원과 만나는 점이고 "
              "[[seg(NP) = 2]]이다.\n[[seg(MN) = x]]라 할 때, [[10(pow(x,2) + frac(16, pow(x,2)))]]의 값을 구하시오."),
    choices=None, derived_answer="120",
    figure=[{"fn": "unsupported", "args": {"raw": "외접원 안의 정삼각형 ABC(A 위), AB·AC의 중점 M·N, 반직선 MN이 원과 만나는 점 P, MN=x, NP=2 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+정삼각형+현 복합 도형",
    note="점 N의 방멱: x·x=2(x+2) → x−4/x=2 → x²+16/x²=12 → 120.")

# p89
add(id="320f6b94", qtype="short",
    question=("다음 조건을 모두 만족시키는 사면체 OABC에 대하여 [[pow(seg(OA),2) + pow(seg(OB),2) + pow(seg(OC),2)]]의 값을 구하시오.\n"
              "(가) [[perp(seg(OA), seg(OB))]], [[perp(seg(OB), seg(OC))]], [[perp(seg(OA), seg(OC))]]\n"
              "(나) [[seg(OA) + seg(OB) + seg(OC) = 17]]\n"
              "(다) 세 삼각형 OAB, OBC, OCA의 넓이의 합은 36이다."),
    choices=None, derived_answer="145",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 OABC: 꼭짓점 O에서 세 모서리 OA, OB, OC가 서로 수직(O에 직각 표시), 뒤쪽 모서리 점선"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사면체 입체도형",
    note="a+b+c=17, (ab+bc+ca)/2=36 → a²+b²+c²=289−144=145 (빠른정답 5와 불일치).")

# p91
add(id="3b23d109", qtype="short",
    question=("그림과 같이 [[angle(C) = deg(90)]]인 직각삼각형 ABC가 있다.\n[[seg(AB) = 2 sqrt(6)]]이고 삼각형 ABC의 넓이가 3일 때,\n"
              "[[pow(seg(AC),3) + pow(seg(BC),3)]]의 값을 구하시오."),
    choices=None, derived_answer="108",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: B 좌하, C 우하(직각 표시), A 우상"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="출처 [2019년 11월 고1 26번/4점]. a²+b²=24, ab=6 → a+b=6 → a³+b³=216−108=108.")

# p94
add(id="c21162ff", qtype="short",
    question="[[x + y = -2]], [[x y = 5]]일 때, [[pow(x,5) + pow(y,5) + pow(x,6) + pow(y,6)]]의 값을 구하시오.",
    choices=None, derived_answer="152", figure=None, difficulty_est=3, confidence=0.9,
    note="x⁵+y⁵=−82, x⁶+y⁶=234 → 152 (sympy 확인, 빠른정답 108과 불일치).")

# p95
add(id="e37970d5", qtype="short",
    question="[[x + y = -4]], [[x y = -3]]일 때, [[pow(x,5) + pow(y,5) + pow(x,6) + pow(y,6)]]의 값을 구하시오.",
    choices=None, derived_answer="7890", figure=None, difficulty_est=3, confidence=0.9,
    note="sympy 확인 7890 (빠른정답 2와 불일치).")

# p96
add(id="00028da5", qtype="short",
    question="[[x + y = -3]], [[x y = 1]]일 때, [[pow(x,5) + pow(y,5) + pow(x,6) + pow(y,6)]]의 값을 구하시오.",
    choices=None, derived_answer="199", figure=None, difficulty_est=3, confidence=0.9,
    note="sympy 확인 199 (빠른정답 2와 불일치).")

# ───────── 절댓값을 포함한 일차부등식 ─────────
# p89
add(id="dfb7cbb6", qtype="choice",
    question=("[[x]]에 대한 연립부등식 [[abs(a x - 3) < 15]], [[2x + 1 > 7]]을 만족시키는 자연수 [[x]]의 개수가 2일 때, "
              "모든 정수 [[a]]의 값의 곱은?"),
    choices=["[[-6]]", "[[-3]]", "[[0]]", "[[3]]", "[[6]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2025년 6월 고1 18번 변형]. x≥4, −12<ax<18 → a=3(x=4,5), a=−2(x=4,5) → 곱 −6 → ① (빠른정답 −3과 불일치).")

# ───────── 행렬 ─────────
# p1
add(id="84334d47", qtype="choice",
    question=("아래 표는 어느 전자 제품 대리점에서 5월, 6월, 7월에 판매된 냉장고, 청소기, 세탁기 판매 대수를 조사한 것이다.\n"
              "이를 행렬로 나타내면 [[A = mat(3,3, a,b,45, 50,35,c, 20,50,d)]]일 때, [[c]]의 의미는?"),
    choices=["냉장고의 7월 판매 대수", "청소기의 6월 판매 대수", "청소기의 7월 판매 대수", "세탁기의 6월 판매 대수", "세탁기의 7월 판매 대수"],
    derived_answer="③",
    figure=[{"fn": "table", "args": {"head": ["", "5월", "6월", "7월"],
                                     "rows": [["냉장고", "70", "60", "45"], ["청소기", "50", "35", "32"], ["세탁기", "20", "50", "65"]]}}],
    difficulty_est=1, confidence=0.9,
    note="c는 (2,3) 성분 = 청소기 7월 = 32 → ③.")

# p4
add(id="bbd64a78", qtype="short",
    question="행렬 [[mat(2,2, -3,10, 1,4)]]에 대하여 행의 개수를 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.9,
    note="2×2 행렬 → 행 2개 (빠른정답 3과 불일치).")

# p6
add(id="a4d96436", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 1,3, -2,0)]], [[B = mat(1,4, 2,-1,4,3)]]에 대하여 행렬 [[A]]는 [[m × n]] 행렬이고 행렬 [[B]]는 [[p × q]] 행렬이다. "
              "[[pow(m,n) + pow(p,q)]]의 값은?"),
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="2²+1⁴=5 → ② (빠른정답 4와 불일치).")

# p9
add(id="cb0b9418", qtype="choice",
    question=("두 행렬 [[A = mat(2,3, 1,2,3, -1,0,2)]], [[B = mat(3,1, 2,-1,4)]]에 대하여 행렬 [[A]]는 [[m × n]] 행렬이고 행렬 [[B]]는 [[p × q]] 행렬이다.\n"
              "[[pow(m,n) + pow(p,q)]]의 값은?"),
    choices=["[[5]]", "[[7]]", "[[9]]", "[[11]]", "[[13]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="2³+3¹=11 → ④ (빠른정답 3과 불일치).")

# p10
add(id="b2a2f533", qtype="short",
    question="행렬 [[mat(2,2, 4,1, 2,1)]]에 대하여 열의 개수를 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.9,
    note="2×2 → 열 2개.")

# p11
add(id="91a6200f", qtype="short",
    question="행렬 [[mat(3,3, 1,0,5, -2,3,7, 0,2,1)]]에 대하여 열의 개수를 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="3×3 → 열 3개.")

# p12
add(id="812b2c6d", qtype="short",
    question="행렬 [[mat(2,3, -2,9,4, 1,3,-1)]]에 대하여 열의 개수를 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="2×3 → 열 3개.")

# p13
add(id="8625f0d8", qtype="short",
    question="행렬 [[mat(2,3, -3,10,5, 1,4,-2)]]에 대하여 행의 개수를 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.9,
    note="2×3 → 행 2개.")

# p15
add(id="c37b3154", qtype="short",
    question="행렬 [[A = mat(2,2, 3,-1, 1,3)]]이라 할 때, 행렬 [[A]]의 제2행과 제1열이 만나는 곳의 성분을 쓰시오.",
    choices=None, derived_answer="1", figure=None, difficulty_est=1, confidence=0.9,
    note="(2,1) 성분 = 1 (빠른정답 3과 불일치).")

# p16
add(id="e4652902", qtype="short",
    question="행렬 [[A = mat(3,3, 3,-1,5, 0,2,-4, 5,0,1)]]에 대하여 제1열의 모든 성분의 합을 구하시오.",
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="3+0+5=8 (빠른정답 2와 불일치).")

# p18
add(id="41ad37ca", qtype="short",
    question="행렬 [[A = mat(3,3, 1,-2,4, 3,0,-2, 5,1,7)]]에 대하여 제3열의 모든 성분의 합을 구하시오.",
    choices=None, derived_answer="9", figure=None, difficulty_est=1, confidence=0.9,
    note="4−2+7=9 (빠른정답 1과 불일치).")

# p19
add(id="9b0906a4", qtype="short",
    question="행렬 [[mat(3,3, 7,8,2, 0,-3,2, -3,1,1)]]에 대하여 제3행의 모든 성분의 합을 구하시오.",
    choices=None, derived_answer="-1", figure=None, difficulty_est=1, confidence=0.9,
    note="−3+1+1=−1 (빠른정답 8과 불일치).")

# p20
add(id="9bb22309", qtype="short",
    question="행렬 [[mat(3,3, 2,1,9, 9,1,1, 2,0,3)]]에 대하여 제1행의 모든 성분의 합을 구하시오.",
    choices=None, derived_answer="12", figure=None, difficulty_est=1, confidence=0.9,
    note="2+1+9=12 (빠른정답 −1과 불일치).")

# p21
add(id="3838c6ff", qtype="short",
    question="행렬 [[mat(3,3, 1,9,8, 8,0,1, 1,9,-1)]]에 대하여 제2행의 모든 성분의 합을 구하시오.",
    choices=None, derived_answer="9", figure=None, difficulty_est=1, confidence=0.9,
    note="8+0+1=9.")

# p22
add(id="5d80e334", qtype="choice",
    question="다음 중 [[3 × 2]] 행렬을 고르면?",
    choices=["[[mat(1,3, 2,4,11)]]", "[[mat(2,3, -3,4,5, -4,7,9)]]", "[[mat(3,2, 2,-1, 4,3, 7,11)]]", "[[mat(3,1, -4,5,13)]]",
             "[[mat(3,3, 1,4,5, -2,3,8, 7,-1,9)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="3행 2열은 ③ (빠른정답 −1과 불일치).")

# p23
add(id="8836c0f3", qtype="choice",
    question="다음 중 [[3 × 1]] 행렬을 고르면?",
    choices=["[[mat(1,3, 1,0,-8)]]", "[[mat(3,2, 0,1, -3,-2, 9,3)]]", "[[mat(2,3, 4,-2,3, 1,7,5)]]", "[[mat(3,1, -1,3,-5)]]",
             "[[mat(3,3, 3,-1,5, 0,2,-4, 5,0,1)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="3행 1열은 ④ (빠른정답 12와 불일치).")

# p24
add(id="f177079b", qtype="short",
    question="행렬 [[A = mat(2,3, 3,-1,0, -3,7,5)]]에 대하여 제2행의 모든 성분의 합을 구하시오.",
    choices=None, derived_answer="9", figure=None, difficulty_est=1, confidence=0.9,
    note="−3+7+5=9.")

# p25
add(id="68f65ec5", qtype="short",
    question=("행렬 [[mat(2,3, pow(x,3),4,2x - 3, 2,5x + 1,-x)]]의 제2행의 모든 성분의 합과 제3열의 모든 성분의 합이 같을 때, "
              "실수 [[x]]의 값을 구하시오"),
    choices=None, derived_answer="-2", figure=None, difficulty_est=2, confidence=0.9,
    note="4x+3 = x−3 → x=−2 (빠른정답 3과 불일치). 원문 끝 마침표 없음.")

# p26
add(id="553e34c1", qtype="short",
    question=("행렬 [[A = mat(2,2, 4,-2, 6,-8)]]에서 ([[i]], [[j]]) 성분을 [[sub(a,i,j)]]라 할 때,\n"
              "[[sub(a,1,1) + sub(a,2,2)]]의 값을 구하시오. (단, [[i]] = 1, 2, [[j]] = 1, 2)"),
    choices=None, derived_answer="-4", figure=None, difficulty_est=1, confidence=0.9,
    note="4+(−8)=−4 (빠른정답 4와 불일치).")

# p27
add(id="290fdb13", qtype="choice",
    question=("이차정사각행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]를\n[[sub(a,i,j) = i + 3j]] ([[i]] = 1, 2, [[j]] = 1, 2)\n"
              "라 하자. 행렬 [[A]]의 (2, 1) 성분은?"),
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2014년 6월 고2 문과 3번/2점]. 2+3=5 → ②.")

# p28
add(id="22eaad34", qtype="choice",
    question=("이차정사각행렬 [[A]]의 ([[i]], [[j]])성분 [[sub(a,i,j)]]를\n[[sub(a,i,j) = 2i + 5j]] ([[i]] = 1, 2, [[j]] = 1, 2)라 하자. 행렬 [[A]]의\n"
              "(2, 2) 성분은?"),
    choices=["[[12]]", "[[14]]", "[[16]]", "[[18]]", "[[20]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="4+10=14 → ② (빠른정답 3과 불일치).")

# p29
add(id="c1991302", qtype="short",
    question=("[[3 × 3]] 행렬의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가 [[sub(a,i,j) = pow(-1, i + j) + 2i j]]일 때, "
              "[[sub(a,1,1) - sub(a,2,2) + sub(a,3,2) + sub(a,3,3)]]의 값을 구하시오."),
    choices=None, derived_answer="24", figure=None, difficulty_est=2, confidence=0.9,
    note="3−9+11+19=24 (빠른정답 −4와 불일치).")

# p30
add(id="b06ab21e", qtype="choice",
    question=("행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j) = -sub(a,j,i)]] ([[i]] = 1, 2, 3, [[j]] = 1, 2, 3)일 때, "
              "행렬 [[A]]가 될 수 있는 것만을 보기에서 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[mat(3,3, 1,2,0, -2,0,-3, 0,3,-1)]]\nㄴ. [[mat(3,3, 0,1,2, -1,0,1, -2,-1,0)]]\n"
              "ㄷ. [[mat(3,3, 0,-1,-1, 1,0,-2, 1,2,0)]]\nㄹ. [[mat(3,3, 0,1,0, 1,0,-2, 0,-2,0)]]"),
    choices=CH_2, derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="대각성분 0·반대칭: ㄱ 대각 1,−1 ✗, ㄴ ✓, ㄷ ✓, ㄹ a12=a21=1 ✗ → ③ (빠른정답 2와 불일치).")

# p31
add(id="5262352e", qtype="choice",
    question=("행렬 [[A = mat(2,2, 3x + y,x + y, x + 3y,x - y)]]의 ([[i]], [[j]]) 성분이 [[sub(a,i,j)]]일 때,\n"
              "[[sub(a,1,1) + sub(a,2,2) = 12]], [[sub(a,1,2) - sub(a,2,1) = 2]]이다. [[sub(a,1,2)]]의 값은?"),
    choices=["[[-2]]", "[[0]]", "[[2]]", "[[4]]", "[[6]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="4x=12 → x=3, −2y=2 → y=−1 → a12=x+y=2 → ③.")

# p32
add(id="b5aaaffc", qtype="choice",
    question=("행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j) = -sub(a,j,i)]] ([[i]] = 1, 2, 3, [[j]] = 1, 2, 3)일 때, "
              "행렬 [[A]]가 될 수 있는 것만을 보기에서 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[mat(3,3, 2,2,0, -1,0,-1, 0,1,-2)]]\nㄴ. [[mat(3,3, 0,-2,-1, 2,0,2, 1,-2,0)]]\n"
              "ㄷ. [[mat(3,3, 0,0,-1, 0,0,3, 1,-3,0)]]\nㄹ. [[mat(3,3, 0,1,0, 2,0,1, 0,-1,0)]]"),
    choices=CH_2, derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄱ 대각 2,−2 ✗, ㄴ ✓, ㄷ ✓, ㄹ a12=1≠−a21=−2 ✗ → ③ (빠른정답 24와 불일치).")

# p33
add(id="30365c59", qtype="short",
    question="행렬 [[A = mat(3,3, 5,2,0, -1,3,8, 1,7,-6)]]에 대하여 [[A = (sub(a,i,j))]]일 때,\n[[sub(a,3,2)]]를 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="(3,2) 성분 = 7 (빠른정답 3과 불일치).")

# p34
add(id="3ab61342", qtype="choice",
    question=("이차정사각행렬 [[A]]의 ([[i]], [[j]])성분 [[sub(a,i,j)]]를\n[[sub(a,i,j) = j(2i - 1)]] ([[i]] = 1, 2, [[j]] = 1, 2)라 하자. 행렬 [[A]]의\n"
              "(1, 2) 성분은?"),
    choices=["[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="a12 = 2·(2−1) = 2 → ① (빠른정답 3과 불일치).")

# p36
add(id="9e9e9475", qtype="short",
    question=("행렬 [[A = mat(3,3, 2,-1,5, 1,3,-2, -3,6,3)]]에 대하여 다음 조건을 만족하는 상수 [[alpha]], [[beta]]에 대하여 [[alpha + beta]]의 값을 구하시오.\n"
              "(가) 제2행의 성분의 합은 [[alpha]]이다.\n(나) 행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]에 대하여 [[i != j]]를 만족하는 모든 성분의 합은 [[beta]]이다."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="α=1+3−2=2, β=−1+5+1−2−3+6=6 → 8 (빠른정답 7과 불일치).")

# p40
add(id="47b2298c", qtype="choice",
    question="[[3 × 2]] 행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가 [[sub(a,i,j) = 3i - 2j + 1]]일 때, [[sub(a,2,2) + sub(a,3,1)]]의 값은?",
    choices=["[[11]]", "[[13]]", "[[15]]", "[[17]]", "[[19]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="a22=3, a31=8 → 11 → ① (빠른정답 4와 불일치).")

# p42
add(id="3873e64d", qtype="short",
    question=("이차정사각행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j) = 2i + j + 1]] ([[i]] = 1, 2, [[j]] = 1, 2)\n"
              "이다. 행렬 [[A]]의 모든 성분의 합을 구하시오."),
    choices=None, derived_answer="22", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2013년 9월 고2 문과 22번/3점]. 4+5+6+7=22 (빠른정답 5와 불일치).")

# p43
add(id="92d0d878", qtype="choice",
    question=("두 실수 [[x]], [[y]]에 대하여\n행렬 [[A = mat(3,3, 1,x + 3y,y - x, x,0,-2, 2x + 5y,4x + y,-1)]]의 ([[i]], [[j]]) 성분을\n"
              "[[sub(a,i,j)]]라 할 때, [[sub(a,1,2) = 5]], [[sub(a,3,1) = 9]]이다. [[3x + y]]의 값은?"),
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="x+3y=5, 2x+5y=9 → x=2, y=1 → 3x+y=7 → ⑤ (빠른정답 1과 불일치).")

# p46
add(id="263f4eda", qtype="short",
    question="행렬 [[A = mat(3,3, 1,8,3, 4,-6,-1, 7,2,-5)]]의 (3, 1) 성분을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="(3,1) 성분 = 7 (빠른정답 5와 불일치).")

# p48
add(id="dc209446", qtype="choice",
    question=("이차정사각행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]를\n[[sub(a,i,j) = pow(-1, i + j) + k i]]라 하자. 행렬 [[A]]의 모든 성분의 합이 24일 때, "
              "상수 [[k]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="부호항 합 0, k(1+1+2+2)=6k=24 → k=4 → ④.")

# p49
add(id="f1b545c4", qtype="short",
    question=("행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가\n"
              "[[sub(a,i,j)]] = [[2 pow(i,2) - pow(j,2)]] ([[i >= j]]), [[sub(a,j,i)]] ([[i < j]])\n"
              "(단, [[i]] = 1, 2, 3, [[j]] = 1, 2, 3)일 때, 행렬 [[A]]의 제1행의 모든 성분의 합을 구하시오."),
    choices=None, derived_answer="25", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의",
    note="a11=1, a12=a21=7, a13=a31=17 → 25 (빠른정답 7과 불일치).")

# p50
add(id="46b3b145", qtype="choice",
    question=("이차정사각행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j) = i - 2j + 3]]일 때, 이차정사각행렬 [[B]]의\n"
              "([[i]], [[j]]) 성분 [[sub(b,i,j)]]는 [[sub(b,i,j) = sub(a,j,i)]]를 만족시킨다.\n이때 행렬 [[B]]는?"),
    choices=["[[mat(2,2, 3,2, 0,0)]]", "[[mat(2,2, 3,2, 0,1)]]", "[[mat(2,2, 2,3, 0,0)]]", "[[mat(2,2, 2,3, 0,1)]]", "[[mat(2,2, 2,3, 1,0)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="A=(2,0;3,1) → B=Aᵀ=(2,3;0,1) → ④ (빠른정답 2와 불일치).")

# p51
add(id="c3ce205e", qtype="choice",
    question=("행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j)]] = ([[pow(i,2) + 2j]]의 양의 약수의 개수)일 때, 행렬 [[A]]는?\n"
              "(단, [[i]] = 1, 2, 3 [[j]] = 1, 2)"),
    choices=["[[mat(2,3, 2,3,2, 2,3,2)]]", "[[mat(2,3, 2,4,2, 2,4,2)]]", "[[mat(3,2, 2,2, 3,3, 2,2)]]", "[[mat(3,2, 2,2, 4,4, 2,2)]]",
             "[[mat(3,2, 2,3, 4,4, 3,2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="3,5,6,8,11,13의 약수 개수 2,2,4,4,2,2 → ④. 원문 '1, 2, 3 j=1, 2' 사이 쉼표 없음 그대로.")

# p52
add(id="4a8f007a", qtype="short",
    question=("행렬 [[A = mat(3,3, 0,2,3, 1,0,4, 3,5,0)]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]는 세 도시 [[sub(C,1)]], [[sub(C,2)]], [[sub(C,3)]]에 대하여 "
              "도시 [[sub(C,i)]]에서 도시 [[sub(C,j)]]로 가는 비행기 직항 노선의 수를 나타낸다. 이때 도시 [[sub(C,2)]]에서 출발하여 "
              "나머지 두 도시를 경유하여 다시 도시 [[sub(C,2)]]로 다시 돌아오는 경우의 수를 구하시오."),
    choices=None, derived_answer="39", figure=None, difficulty_est=2, confidence=0.9,
    note="C2→C1→C3→C2: 1·3·5=15, C2→C3→C1→C2: 4·3·2=24 → 39.")

# p53
add(id="348c9ff3", qtype="choice",
    question=("이차정사각행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]를\n이차함수 [[y = 2 pow(x,2) - 4(i + j) x + 19]]의 그래프와 [[x]]축이 "
              "만나는 점의 개수로 정의할 때, 행렬 [[A]]는?"),
    choices=["[[mat(2,2, 0,1, 1,1)]]", "[[mat(2,2, 0,1, 1,2)]]", "[[mat(2,2, 0,2, 2,1)]]", "[[mat(2,2, 0,0, 0,2)]]", "[[mat(2,2, 0,0, 0,1)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="D/4=4(i+j)²−38: i+j=2,3 → 음수(0개), i+j=4 → 양수(2개) → ④.")

# p55
add(id="25f1dd75", qtype="choice",
    question=("이차정사각행렬 [[A]]의 ([[m]], [[n]])성분을 [[sub(a,m,n)]]이라고 하자.\n"
              "[[sub(a,m,n)]]은 [[x]]에 대한 이차방정식 [[pow(x,2) + 2m x + 2n = 0]]이 서로 다른 두 실근을 가지면 [[sub(a,m,n) = 1]],\n"
              "중근을 가지면 [[sub(a,m,n) = 0]], 허근을 가지면 [[sub(a,m,n) = -1]]\n이라고 할 때, 행렬 [[A]]는?"),
    choices=["[[mat(2,2, -1,-1, 1,0)]]", "[[mat(2,2, -1,0, 1,1)]]", "[[mat(2,2, 0,1, -1,0)]]", "[[mat(2,2, 0,-1, -1,1)]]", "[[mat(2,2, 0,-1, 1,1)]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="D/4=m²−2n: (1,1)−1, (1,2)−1, (2,1)+1, (2,2)0 → ① (빠른정답 39와 불일치).")

# p56
add(id="a09d8c44", qtype="short",
    question=("행렬 [[A = mat(3,3, 0,2,1, 1,0,2, 2,5,0)]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]는 세 도시 [[sub(C,1)]], [[sub(C,2)]], [[sub(C,3)]]에 대하여 "
              "도시 [[sub(C,i)]]에서 도시 [[sub(C,j)]]로 가는 비행기 직항 노선의 수를 나타낸다. 이때 도시 [[sub(C,1)]]에서 출발하여 "
              "나머지 두 도시를 경유하여 다시 도시 [[sub(C,1)]]로 다시 돌아오는 경우의 수를 구하시오."),
    choices=None, derived_answer="13", figure=None, difficulty_est=2, confidence=0.9,
    note="C1→C2→C3→C1: 2·2·2=8, C1→C3→C2→C1: 1·5·1=5 → 13 (빠른정답 4와 불일치).")

# p57
add(id="f75cf502", qtype="choice",
    question=("이차함수 [[f(x) = pow(x,2) - 3x + 4]]에 대하여 [[3 × 3]] 행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가 "
              "[[sub(a,i,j)]] = 1 ([[abs(f(i)) = j]]), 2 ([[abs(f(i)) != j]])일 때,\n행렬 [[A]]는?"),
    choices=["[[mat(3,3, 2,1,2, 2,1,2, 2,2,2)]]", "[[mat(3,3, 1,2,2, 2,2,1, 2,2,2)]]", "[[mat(3,3, 1,2,2, 2,2,1, 2,2,1)]]",
             "[[mat(3,3, 2,2,1, 2,2,1, 2,2,1)]]", "[[mat(3,3, 2,2,2, 2,1,2, 2,2,1)]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의",
    note="f(1)=2, f(2)=2, f(3)=4 → 1행·2행 (2,1,2), 3행 (2,2,2) → ①.")

# p58
add(id="a77ef79c", qtype="choice",
    question=("이차정사각행렬 [[A]]의 ([[i]], [[j]])성분 [[sub(a,i,j)]]를 다음과 같이 정의할 때, 행렬 [[A]]의 모든 성분의 합은?\n"
              "[[sub(a,i,j)]] = (다항식 [[pow(x,3) + pow(x,2) - x + 2]]를 [[x + i - j]]로 나눈 나머지)"),
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="나머지 f(j−i): f(0)=2, f(1)=3, f(−1)=3, f(0)=2 → 10 → ⑤ (빠른정답 1과 불일치).")

# p61
add(id="ed9a988f", qtype="short",
    question=("다음 그림과 같이 1부터 100까지의 자연수가 배열되어 있는 숫자판에 4개의 수 (1, 2, 11, 12)를 포함하는 색칠된 정사각형이 놓여 있다. "
              "이 색칠된 정사각형을 오른쪽으로 [[m]]칸, 아래쪽으로 [[n]]칸 이동하였을 때, 이동된 정사각형 내부의 자연수를 그대로 괄호로 묶어서 나타내어 "
              "행렬 [[S(m, n)]]이라 하자.\n예를 들어 [[S(3, 2) = mat(2,2, 24,25, 34,35)]]이다.\n"
              "8 이하의 두 자연수 [[a]], [[b]]에 대하여 행렬 [[S(a, b)]]의 모든 성분의 합이 234일 때, [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="7",
    figure=[{"fn": "table", "args": {"rows": [[str(10 * r + c) for c in range(1, 11)] for r in range(10)]}},
            {"fn": "unsupported", "args": {"raw": "숫자판에서 1,2,11,12 칸과 24,25,34,35 칸이 색칠됨, 1에서 24 방향으로 화살표"}}],
    difficulty_est=3, confidence=0.85,
    note="좌상단 t: 4t+22=234 → t=53=1+a+10b → a=2, b=5 → 7. 숫자판은 표로, 색칠·화살표는 unsupported로 기록.")

# p62
add(id="11d780f5", qtype="choice",
    question=("이차함수 [[f(x) = 2 pow(x,2) - 3x + 2]]에 대하여 [[3 × 3]] 행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가 "
              "[[sub(a,i,j)]] = 1 ([[abs(f(i)) = pow(j,2)]]), [[-1]] ([[abs(f(i)) != pow(j,2)]])일 때, 행렬 [[A]]는?"),
    choices=["[[mat(3,3, -1,1,-1, 1,-1,-1, -1,-1,-1)]]", "[[mat(3,3, 1,-1,-1, -1,-1,1, 1,-1,-1)]]", "[[mat(3,3, 1,-1,-1, -1,1,-1, -1,-1,-1)]]",
             "[[mat(3,3, -1,1,-1, 1,-1,-1, -1,-1,-1)]]", "[[mat(3,3, 1,-1,-1, -1,-1,1, -1,-1,-1)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의",
    note="f(1)=1=1², f(2)=4=2², f(3)=11 → (1,−1,−1),(−1,1,−1),(−1,−1,−1) → ③ (빠른정답 4와 불일치). 원문 선지 ①과 ④가 동일(원문 오타, 그대로 전사).")
