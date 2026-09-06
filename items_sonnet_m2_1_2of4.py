# -*- coding: utf-8 -*-
# esc_sonnet_m2-1_2of4 — 이미지 기준 전사 (84 항목 / 80쪽)
# 표기 관행: 연립방정식 중괄호는 두 식을 콤마로 나열(GUIDE §4), 두 연립방정식이 나올 때만 텍스트 { }로 묶음.
#            식 안의 그룹 중괄호·대괄호는 소괄호로(마커 안 금지), 빈칸 상자는 □ 텍스트,
#            단항식으로 나누는 나눗셈(÷ 8x²y² 등)은 파서가 좌결합이므로 나누는 단항식을 괄호로 묶음.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

FIG = "도형 표현 불가: "

# ======================= 다항식의 곱셈과 나눗셈 =======================
# p38 빈칸
add(id="cea180b1", qtype="choice",
    question=("다음 □ 안에 알맞은 식을 구하면?\n"
              "[[(-24 pow(x,3) pow(y,2) + 8 pow(x,2) pow(y,3)) ÷ (8 pow(x,2) pow(y,2))]] "
              "+ [[(20 pow(x,2) y - 4x pow(y,2) - 16x y)]] ÷ □ = [[2x - 4]]"),
    choices=["[[x y]]", "[[2 pow(x,2) y]]", "[[-3x pow(y,2)]]", "[[4x y]]", "[[5x]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="첫 항 = −3x + y → 나머지 항 = 5x − y − 4 → □ = 4xy → ④. 빠른정답 3과 불일치. 빈칸 상자는 □ 텍스트, 나누는 단항식은 괄호로.")

# p39
add(id="59329197", qtype="choice",
    question="[[5x(2x - 3y + 1) - 4x(y - 4x)]]를 간단히 하면?",
    choices=["[[6 pow(x,2) - 11x y + 5x]]", "[[10 pow(x,2) - 19x y + 5x]]", "[[10 pow(x,2) - 11x y + 5x]]",
             "[[16 pow(x,2) - 19x y + 5x]]", "[[26 pow(x,2) - 19x y + 5x]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="10x² − 15xy + 5x − 4xy + 16x² = 26x² − 19xy + 5x → ⑤. 빠른정답 1과 불일치.")

# p41
add(id="4d5a10e5", qtype="choice",
    question="[[6x(2x - 3y + 1) - 2x(3y - x)]]를 간단히 한 것은?",
    choices=["[[-14 pow(x,2) - 24x y + 6x]]", "[[-14 pow(x,2) + 24x y - 6x]]", "[[14 pow(x,2) - 24x y - 6x]]",
             "[[14 pow(x,2) - 24x y + 6x]]", "[[14 pow(x,2) + 24x y + 6x]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="12x² − 18xy + 6x − 6xy + 2x² = 14x² − 24xy + 6x → ④ = 빠른정답 ✓.")

# p42
add(id="22650155", qtype="choice",
    question="[[-2x(4x - 3y + 8) - frac(1,4) x(4y - 16x)]]를 간단히 한 것은?",
    choices=["[[-4 pow(x,2) - 5x y - 16x]]", "[[-4 pow(x,2) + 5x y - 16x]]", "[[4 pow(x,2) - 5x y - 16x]]",
             "[[4 pow(x,2) + 5x y - 16x]]", "[[4 pow(x,2) + 5x y + 16x]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="−8x² + 6xy − 16x − xy + 4x² = −4x² + 5xy − 16x → ②. 빠른정답 5와 불일치.")

# p43
add(id="e46e027a", qtype="choice",
    question="[[-x(-4x + 1) - 3(pow(x,2) + x - 2)]]를 간단히 한 것은?",
    choices=["[[-7 pow(x,2) - 2x + 6]]", "[[-pow(x,2) + 4x - 6]]", "[[pow(x,2) - 4x + 6]]",
             "[[pow(x,2) + 4x + 6]]", "[[7 pow(x,2) + 2x - 6]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="4x² − x − 3x² − 3x + 6 = x² − 4x + 6 → ③. 빠른정답 5와 불일치.")

# p44
add(id="3374b2ba", qtype="choice",
    question="[[2x(4x - y + 4) - 6x(2y - 2x)]]를 간단히 한 것은?",
    choices=["[[-20 pow(x,2) + 14x y - 8x]]", "[[-2 pow(x,2) - 10x y - 8x]]", "[[2 pow(x,2) - 10x y + 8x]]",
             "[[2 pow(x,2) + 10x y + 8x]]", "[[20 pow(x,2) - 14x y + 8x]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="8x² − 2xy + 8x − 12xy + 12x² = 20x² − 14xy + 8x → ⑤. 빠른정답 4와 불일치.")

# p48
add(id="a73e8078", qtype="choice",
    question="[[5x(-y + 2) + (45 pow(x,2) y - 36x y - 27 pow(x,2)) ÷ (9x)]]를 간단히 하면?",
    choices=["[[7x - 4y]]", "[[8x - 3y]]", "[[10x - 4y]]", "[[12x - 3y]]", "[[14x - 3y]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="−5xy + 10x + 5xy − 4y − 3x = 7x − 4y → ①. 빠른정답 3과 불일치. 나누는 단항식 9x는 괄호로.")

# p49
add(id="72e268e7", qtype="short",
    question="다음 식을 간단히 하시오.\n[[frac(12 pow(a,2) b + 24a pow(b,2), 6a b) - frac(10a b - 15 pow(b,2), 5b)]]",
    choices=None, derived_answer="7b", figure=None, difficulty_est=1, confidence=0.9,
    note="(2a + 4b) − (2a − 3b) = 7b. 빠른정답 1과 불일치.")

# p54
add(id="29f80ebb", qtype="short",
    question=("[[2x(x - 3) - (pow(x,2) - x(-3x + 2)) ÷ (-x)]]를 간단히 하면 [[a pow(x,2) + b x + c]]가 될 때, "
              "[[a + b + c]]의 값을 구하시오. (단, [[a]], [[b]], [[c]]는 상수)"),
    choices=None, derived_answer="-2", figure=None, difficulty_est=2, confidence=0.9,
    note="(4x² − 2x) ÷ (−x) = −4x + 2 → 2x² − 6x + 4x − 2 = 2x² − 2x − 2 → a+b+c = −2 = 빠른정답 ✓. 원문 중괄호는 소괄호로.")

# p58 집 평면도
add(id="fba1ac85", qtype="short",
    question=("진이의 집의 구조는 다음 그림과 같다. 거실의 넓이가 [[p pow(a,2) + q a + r]]일 때, 상수 [[p]], [[q]], [[r]]에 대하여 "
              "[[p + q + r]]의 값을 구하시오.\n(단, 집, 방, 현관, 욕실은 모두 직사각형 모양이고 벽의 두께는 생각하지 않는다.)"),
    choices=None, derived_answer="33",
    figure=[{"fn": "unsupported", "args": {"raw": "집 평면도(직사각형, 가로 7a+3, 세로 5a). 왼쪽 위 현관(가로 3, 세로 1), 왼쪽 아래 방(3a×3a), 그 오른쪽 아래 욕실(가로 2, 세로 a), 오른쪽 아래 방(가로 a, 세로 3a). 나머지 색칠 부분이 거실"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "치수가 그림에만 있는 집 평면도",
    note="(7a+3)·5a − 3 − 9a² − 2a − 3a² = 23a² + 13a − 3 → 33. 빠른정답 4와 불일치.")

# p59 집 평면도
add(id="a703ed13", qtype="short",
    question=("진이의 집의 구조는 다음 그림과 같다. 거실의 넓이가 [[p pow(a,2) + q a + r]]일 때, 상수 [[p]], [[q]], [[r]]에 대하여 "
              "[[p + q + r]]의 값을 구하시오. (단, 집, 방, 현관, 부엌, 화장실은 모두 직사각형 모양이고, 벽의 두께는 생각하지 않는다.)"),
    choices=None, derived_answer="31",
    figure=[{"fn": "unsupported", "args": {"raw": "집 평면도(직사각형, 가로 9a+1, 세로 6a). 왼쪽 위 현관(2×2), 왼쪽 아래 부엌(가로 2, 세로 2a), 아래 가운데 방(3a×3a), 그 오른쪽 화장실(가로 2, 세로 3a), 오른쪽 방(가로 a, 세로 5a+1). 나머지 색칠 부분이 거실"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "치수가 그림에만 있는 집 평면도",
    note="(9a+1)·6a − 4 − 4a − 9a² − 6a − a(5a+1) = 40a² − 5a − 4 → 31. 빠른정답 5와 불일치.")

# p66
add(id="7c636e03", qtype="choice",
    question="밑면의 반지름의 길이가 [[3x]]이고, 높이가 [[4x + 5x y]]인 원기둥의 겉넓이는?",
    choices=["[[24 pi pow(x,2) + 18 pi pow(x,2) y]]", "[[24 pi pow(x,2) + 30 pi pow(x,2) y]]", "[[40 pi pow(x,2) + 24 pi pow(x,2) y]]",
             "[[42 pi pow(x,2) + 15 pi pow(x,2) y]]", "[[42 pi pow(x,2) + 30 pi pow(x,2) y]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="2π·9x² + 2π·3x(4x + 5xy) = 42πx² + 30πx²y → ⑤ = 빠른정답 ✓.")

# p68 두 직육면체
add(id="3a5ea8a1", qtype="choice",
    question="다음 그림과 같이 두 직육면체로 만든 입체도형의 부피가 [[60 pow(x,3) + 30x pow(y,2)]]일 때, [[h]]를 [[x]], [[y]]의 식으로 나타내면?",
    choices=["[[pow(x,2) + pow(y,2)]]", "[[pow(x,2) + 2 pow(y,2)]]", "[[2 pow(x,2) - pow(y,2)]]",
             "[[2 pow(x,2) + pow(y,2)]]", "[[2 pow(x,2) + 2 pow(y,2)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "가로 3x, 세로 3인 큰 직육면체 위에 가로 x, 높이 h인 가늘고 긴 직육면체를 올린 입체(분홍 음영). 전체 높이 4h"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "치수가 그림에만 있는 직육면체 결합 입체",
    note="3x·h + 3x·3·3h = 30xh = 60x³ + 30xy² → h = 2x² + y² → ④ = 빠른정답 ✓.")

# p71
add(id="7e97604a", qtype="choice",
    question=("다음 그림은 부피가 [[16 pow(x,2) + 24x y]]인 큰 직육면체 위에 부피가 [[10 pow(x,2) + 4x y]]인 작은 직육면체를 올려놓은 것이다. "
              "이때 [[h]]의 값은?"),
    choices=["[[4x + 3y]]", "[[4x + 5y]]", "[[7x + 2y]]", "[[7x + 5y]]", "[[9x + 7y]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "가로 4x, 세로 2인 큰 직육면체의 왼쪽 위에 가로 x인 작은 직육면체를 올린 입체(분홍 음영). 전체 높이 h"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "치수가 그림에만 있는 직육면체 결합 입체",
    note="큰 높이 (16x²+24xy)/(8x) = 2x + 3y, 작은 높이 (10x²+4xy)/(2x) = 5x + 2y → h = 7x + 5y → ④ = 빠른정답 ✓.")

# p72 사각뿔대
add(id="f8a20092", qtype="choice",
    question="다음 그림과 같은 사각뿔대의 부피는?",
    choices=["[[-2 pow(x,2) - frac(11,2) x y - 32 pow(y,2)]]", "[[-2 pow(x,2) + frac(11,2) x y - 32 pow(y,2)]]",
             "[[-2 pow(x,2) + frac(11,2) x y + 32 pow(y,2)]]", "[[-4 pow(x,2) + frac(5,2) x y - 64 pow(y,2)]]",
             "[[-4 pow(x,2) + frac(5,2) x y + 64 pow(y,2)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "사각뿔대(녹색 음영)와 그 위 잘려 나간 사각뿔(점선). 윗면 가로 x − 3/4 y, 세로 6; 아랫면 가로 1/4 x + 2y, 세로 12; 꼭짓점에서 윗면까지 높이 x, 아랫면까지 높이 4y"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "치수가 그림에만 있는 사각뿔대",
    note="(1/3)·12(x/4 + 2y)·4y − (1/3)·6(x − 3y/4)·x = −2x² + (11/2)xy + 32y² → ③. 빠른정답 4와 불일치.")

# p74 사각뿔대
add(id="76aff228", qtype="choice",
    question="다음 그림과 같은 사각뿔대의 부피는?",
    choices=["[[-2 pow(x,2) - 20x y - 18 pow(y,2)]]", "[[-2 pow(x,2) + 20x y + 18 pow(y,2)]]", "[[-2 pow(x,2) - 20x y - 36 pow(y,2)]]",
             "[[-2 pow(x,2) + 20x y - 36 pow(y,2)]]", "[[-2 pow(x,2) + 20x y + 36 pow(y,2)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "사각뿔대(보라 음영)와 그 위 잘려 나간 사각뿔. 윗면 가로 x − y, 세로 3; 아랫면 가로 1/2 x + y, 세로 9; 꼭짓점에서 윗면까지 높이 2x, 아랫면까지 높이 12y"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "치수가 그림에만 있는 사각뿔대",
    note="(1/3)·9(x/2 + y)·12y − (1/3)·3(x − y)·2x = −2x² + 20xy + 36y² → ⑤. 빠른정답 4와 불일치.")

# p76 직육면체 속 사각뿔
add(id="add829ec", qtype="choice",
    question=("다음 그림과 같은 직육면체에서 [[ratio(seg(AF), seg(FB)) = ratio(3, 5)]], [[ratio(seg(BG), seg(GC)) = ratio(2, 1)]], "
              "[[ratio(seg(CH), seg(HD)) = ratio(1, 1)]], [[ratio(seg(DE), seg(EA)) = ratio(1, 2)]]이고 점 I는 [[seg(JK)]] 위의 점일 때, "
              "색칠한 입체도형의 부피는?"),
    choices=["[[18 pow(a,2) b]]", "[[frac(37,2) a pow(b,2)]]", "[[19 pow(a,2) b]]", "[[frac(39,2) a pow(b,2)]]", "[[20a pow(b,2)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체(가로 3a, 세로 8b, 높이 5b). 윗면 ABCD(A 뒤왼쪽, B 앞왼쪽, C 앞오른쪽, D 뒤오른쪽)의 변 위 점 F(AB 위), G(BC 위), H(CD 위), E(AD 위)와 밑면 모서리 JK 위의 점 I를 꼭짓점으로 하는 사각뿔 I-FGHE가 색칠됨"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "직육면체 속 사각뿔 입체도형",
    note="AB=CD=8b, BC=AD=3a; 사각형 FGHE = 24ab − (3ab + 5ab + 2ab + 2ab) = 12ab, 높이 5b → (1/3)·12ab·5b = 20ab² → ⑤ = 빠른정답 ✓.")

# p77 직육면체 속 사각뿔
add(id="140fa68c", qtype="choice",
    question=("다음 그림과 같은 직육면체에서 [[ratio(seg(AF), seg(FB)) = ratio(2, 3)]], [[ratio(seg(BG), seg(GC)) = ratio(1, 2)]], "
              "[[ratio(seg(CH), seg(HD)) = ratio(1, 4)]], [[ratio(seg(DE), seg(EA)) = ratio(2, 1)]]이고 점 I는 [[seg(JK)]] 위의 점일 때, "
              "색칠한 입체도형의 부피는?"),
    choices=["[[9 pow(a,2) b]]", "[[frac(28,3) a pow(b,2)]]", "[[frac(29,3) pow(a,2) b]]", "[[10a pow(b,2)]]", "[[frac(31,3) pow(a,2) b]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체(가로 3a, 세로 5b, 높이 4b). 윗면 ABCD(A 뒤왼쪽, B 앞왼쪽, C 앞오른쪽, D 뒤오른쪽)의 변 위 점 F(AB 위), G(BC 위), H(CD 위), E(AD 위)와 밑면 모서리 JK 위의 점 I를 꼭짓점으로 하는 사각뿔 I-FGHE가 색칠됨(하늘색)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "직육면체 속 사각뿔 입체도형",
    note="AB=CD=5b, BC=AD=3a; FGHE = 15ab − (ab + 3ab/2 + ab + 4ab) = 15ab/2, 높이 4b → (1/3)(15ab/2)(4b) = 10ab² → ④. 빠른정답 5와 불일치.")

# p84 식의 값
add(id="e89d517c", qtype="short",
    question="[[x = frac(9,11)]], [[y = 3]]일 때,\n[[3x - (2y + (-6 pow(x,2) + 18x y) ÷ (9x))]]의 값을 구하시오.",
    choices=None, derived_answer="-9", figure=None, difficulty_est=2, confidence=0.9,
    note="(−6x² + 18xy) ÷ 9x = −2x/3 + 2y → 3x − 4y + 2x/3 = 11x/3 − 4y = 3 − 12 = −9. 빠른정답 3과 불일치. 원문 중괄호는 소괄호로, 나누는 단항식은 괄호로.")

# p88
add(id="a68b39fa", qtype="choice",
    question="[[x = frac(1,2)]], [[y = frac(1,3)]], [[z = 6]]일 때, [[frac(pow(x,2) y z - 2x y + x pow(y,2) z, x y z)]]의 값은?",
    choices=["[[frac(1,2)]]", "[[frac(1,3)]]", "[[frac(1,6)]]", "[[frac(5,6)]]", "[[0]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="x − 2/z + y = 1/2 − 1/3 + 1/3 = 1/2 → ① = 빠른정답 ✓.")

# p99 (이미지에 문항 2개 인쇄, id 1개) — 하단 선택형 전사
add(id="f62dc9bf", qtype="choice",
    question=("[[A = (-4 pow(x,2) pow(y,2) + frac(3,2) x pow(y,3)) ÷ (frac(3,2) x pow(y,2))]],\n"
              "[[B = frac(5,4)(2x - frac(8,5) y)]]일 때,\n"
              "[[B - (2A - 3B - (5A - 2B))]]를 [[x]], [[y]]에 대한 식으로 바르게 나타낸 것은?"),
    choices=["[[-18x + frac(27,4) y]]", "[[-13x + frac(11,4) y]]", "[[-8x + 3y]]", "[[-7x - 9y]]", "[[-3x - y]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.75,
    needs_review="이미지에 별개 문항 2개 인쇄(id는 1개): 상단 'A▲B, A▼B 연산 → 2m+n' 문항은 미전사, 하단 선택형(빠른정답 ⑤ 일치)만 전사",
    note=("A = −8x/3 + y, B = 5x/2 − 2y; 식 = 3A + 2B = −3x − y → ⑤ = 빠른정답 ✓. 원문 중괄호는 소괄호로. "
          "상단 문항 원문: 두 다항식 A=0.4x+1.4y, B=0.05x+0.6y에 대하여 A▲B=3A−5B, A▼B=A+3B라 하자. (A▲B)▲(A▼B)=mx+ny일 때, 상수 m, n에 대하여 2m+n의 값을 구하시오. (풀면 2m+n = −61/5)"))

# ======================= 다항식의 덧셈과 뺄셈 =======================
# p14
add(id="b717d7ac", qtype="choice",
    question=("[[(frac(2,3) x - frac(1,2) y) - (frac(1,6) x - frac(5,4) y) = a x + b y]]일 때,\n"
              "상수 [[a]], [[b]]에 대하여 [[a - b]]의 값은?"),
    choices=["[[-frac(1,4)]]", "[[-frac(1,2)]]", "[[0]]", "[[frac(1,2)]]", "[[1]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="a = 1/2, b = 3/4 → a − b = −1/4 → ① = 빠른정답 ✓.")

# p48
add(id="8e9a040f", qtype="short",
    question="[[11y - (4y - 9x - (3x - (x - y))) = a x + b y]]일 때,\n[[a b]]의 값을 구하시오. (단, [[a]], [[b]]는 상수)",
    choices=None, derived_answer="88", figure=None, difficulty_est=2, confidence=0.9,
    note="3x − (x − y) = 2x + y; 4y − 9x − (2x + y) = −11x + 3y; 11y − (−11x + 3y) = 11x + 8y → ab = 88. 빠른정답 4와 불일치. 원문 대괄호·중괄호는 소괄호로.")

# p53
add(id="1d6548c9", qtype="choice",
    question="[[(2x + 3) - (3 pow(x,2) - (1 - 7x)) = a pow(x,2) + b x + c]]일 때,\n[[a + b + c]]의 값은?",
    choices=["[[-1]]", "[[-2]]", "[[-3]]", "[[-4]]", "[[-5]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="2x + 3 − 3x² + 1 − 7x = −3x² − 5x + 4 → a+b+c = −4 → ④. 빠른정답 1과 불일치. 원문 중괄호는 소괄호로.")

# p72 빈칸
add(id="8e96fc8b", qtype="choice",
    question="[[4 pow(x,2) - 2y + 1]] − □ = [[-pow(x,2) + 3y - 4]]에서\n□ 안에 알맞은 식은?",
    choices=["[[-5 pow(x,2) + 5y - 5]]", "[[-5 pow(x,2) + y - 3]]", "[[5 pow(x,2) + y - 3]]", "[[5 pow(x,2) + y + 5]]", "[[5 pow(x,2) - 5y + 5]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="□ = (4x² − 2y + 1) − (−x² + 3y − 4) = 5x² − 5y + 5 → ⑤. 빠른정답 3과 불일치. 빈칸 상자는 □ 텍스트.")

# p73 빈칸
add(id="8ed680c8", qtype="choice",
    question="[[-4a]] − { [[3a + 5b]] − 2([[a - 2b]] − □) } = [[-a - 11b]]\n일 때, □ 안에 알맞은 식은?",
    choices=["[[-4a - b]]", "[[-2a - 3b]]", "[[-2a + b]]", "[[2a + 3b]]", "[[3a + 3b]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="□ = P: −4a − (a + 9b + 2P) = −5a − 9b − 2P = −a − 11b → P = −2a + b → ③ = 빠른정답 ✓. 빈칸 상자 □와 중괄호는 마커 밖 텍스트.")

# p74 빈칸
add(id="f2a3f1be", qtype="choice",
    question="[[3x]] − 2{ [[x + 2y]] − ([[y - 3x]] − □) } = [[-7x - 6y]]일 때,\n□ 안에 알맞은 식은?",
    choices=["[[-2x - y]]", "[[-2x + y]]", "[[x + y]]", "[[x + 2y]]", "[[3x + 3y]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="□ = P: 3x − 2(4x + y + P) = −5x − 2y − 2P = −7x − 6y → P = x + 2y → ④. 빠른정답 2와 불일치. 빈칸 상자 □와 중괄호는 마커 밖 텍스트.")

# p75 빈칸
add(id="a94283ab", qtype="choice",
    question="[[pow(x,2)]] − { [[5x]] − ([[x + 3 pow(x,2)]] − □) } = [[2 pow(x,2) - x - 5]]에서\n□ 안에 알맞은 식을 구하면?",
    choices=["[[-pow(x,2) - 3x - 5]]", "[[-2 pow(x,2) + 3x - 5]]", "[[3 pow(x,2) - 3x + 5]]", "[[2 pow(x,2) - 5x + 5]]", "[[2 pow(x,2) - 3x + 5]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="□ = P: x² − (4x − 3x² + P) = 4x² − 4x − P = 2x² − x − 5 → P = 2x² − 3x + 5 → ⑤ = 빠른정답 ✓. 빈칸 상자 □와 중괄호는 마커 밖 텍스트.")

# p76 빈칸
add(id="9b9db7ed", qtype="choice",
    question="[[-7 pow(x,2) + 10y + 13]] − □ = [[4 pow(x,2) - 4y + 7]]에서\n□ 안에 알맞은 식은?",
    choices=["[[-11 pow(x,2) - 10y + 6]]", "[[-11 pow(x,2) - 6y - 6]]", "[[-11 pow(x,2) + 10y - 6]]", "[[-11 pow(x,2) + 14y + 6]]", "[[11 pow(x,2) - 4y - 7]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="□ = (−7x² + 10y + 13) − (4x² − 4y + 7) = −11x² + 14y + 6 → ④. 빠른정답 3과 불일치. 빈칸 상자는 □ 텍스트.")

# p77 빈칸
add(id="8b2ba1c3", qtype="choice",
    question="[[7a]] − { [[3a - 4b]] − ([[2a + b]] − □) } = [[5a + b]]일 때,\n□ 안에 알맞은 식은?",
    choices=["[[-a - 4b]]", "[[-a + 4b]]", "[[a - b]]", "[[a - 4b]]", "[[a + 4b]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="□ = P: 7a − (a − 5b + P) = 6a + 5b − P = 5a + b → P = a + 4b → ⑤. 빠른정답 4와 불일치. 빈칸 상자 □와 중괄호는 마커 밖 텍스트.")

# p79 빈칸
add(id="9893930f", qtype="choice",
    question=("[[-2 pow(x,2)]] − [ [[3x + 4 pow(x,2)]] − { [[5 pow(x,2)]] − (□ − [[x]]) } ]를 간단히 하면 [[-7 pow(x,2) - 3x]]일 때, "
              "□ 안에 알맞은 식은?"),
    choices=["[[-6 pow(x,2) - x]]", "[[-6 pow(x,2) + x]]", "[[6 pow(x,2) - x]]", "[[6 pow(x,2)]]", "[[6 pow(x,2) + x]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="□ = P: −2x² − (−x² + 2x + P) = −x² − 2x − P = −7x² − 3x → P = 6x² + x → ⑤. 빠른정답 4와 불일치. 빈칸 상자 □와 대괄호·중괄호는 마커 밖 텍스트.")

# p80 빈칸
add(id="9a77c418", qtype="choice",
    question=("[[4 pow(x,2)]] − [ [[2x + 7 pow(x,2)]] − { [[3 pow(x,2)]] − (□ − [[x]]) } ]를 간단히 하면 [[-2 pow(x,2) - 3x]]일 때, "
              "□ 안에 알맞은 식은?"),
    choices=["[[-2 pow(x,2) - x]]", "[[-2 pow(x,2) + 2x]]", "[[2 pow(x,2) - 2x]]", "[[2 pow(x,2) + x]]", "[[2 pow(x,2) + 2x]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="□ = P: 4x² − (4x² + x + P) = −x − P = −2x² − 3x → P = 2x² + 2x → ⑤ = 빠른정답 ✓. 빈칸 상자 □와 대괄호·중괄호는 마커 밖 텍스트.")

# p81 빈칸
add(id="0b42f707", qtype="choice",
    question=("[[-3 pow(x,2)]] − [ [[4x + 2 pow(x,2)]] − { [[6 pow(x,2)]] − (□ + [[x]]) } ]를 간단히 하면 [[-4 pow(x,2) + x]]일 때, "
              "□ 안에 알맞은 식은?"),
    choices=["[[3 pow(x,2) - 6x]]", "[[3 pow(x,2) + 2x]]", "[[5 pow(x,2) - 6x]]", "[[5 pow(x,2)]]", "[[5 pow(x,2) + 2x]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="□ = P: −3x² − (−4x² + 5x + P) = x² − 5x − P = −4x² + x → P = 5x² − 6x → ③. 빠른정답 2와 불일치. 빈칸 상자 □와 대괄호·중괄호는 마커 밖 텍스트.")

# p83 빈칸
add(id="b98d5528", qtype="choice",
    question="[[x]] − [ [[5x - 3y]] − { [[4x + 2y]] − ([[y]] − □) } ] = [[x + 2y]]\n일 때, □ 안에 알맞은 식은?",
    choices=["[[x - 4y]]", "[[x - 2y]]", "[[x - y]]", "[[-x + 2y]]", "[[-x + y]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="□ = P: x − (x − 4y − P) = 4y + P = x + 2y → P = x − 2y → ②. 빠른정답 5와 불일치. 빈칸 상자 □와 대괄호·중괄호는 마커 밖 텍스트.")

# p85 표
add(id="e349e09e", qtype="short",
    question=("다음 표의 가로 방향의 규칙은 왼쪽의 두 칸의 식을 더하여 마지막 칸에 적는 것이고, 세로 방향의 규칙은 위쪽의 두 칸 중 위 칸의 식에서 "
              "아래 칸의 식을 빼서 마지막 칸에 적는 것이다. (나)에 들어갈 식에서 (마)에 들어갈 식을 뺀 결과가 [[a pow(x,2) + b x + c]]일 때, "
              "상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="3",
    figure=[{"fn": "table", "args": {"rows": [["[[5 pow(x,2) - 3x + 14]]", "(가)", "[[2 pow(x,2) - 3x + 4]]"],
                                              ["[[2 pow(x,2) - 2x + 9]]", "(나)", "(다)"],
                                              ["(라)", "(마)", "[[2 pow(x,2) - 5x + 2]]"]]}}],
    difficulty_est=3, confidence=0.9,
    note="(가) = −3x² − 10, (라) = 3x² − x + 5, (마) = −x² − 4x − 3, (나) = (가) − (마) = −2x² + 4x − 7 → (나) − (마) = −x² + 8x − 4 → 3. 빠른정답 2와 불일치.")

# ======================= 여러 가지 연립방정식의 풀이 =======================
# p5 대입법 과정
add(id="e231b3de", qtype="choice",
    question=("다음은 연립방정식 [[-2x + y = 5]], [[x - y = -2]] 을 대입법으로 푸는 과정이다. ( )안에 들어갈 수나 식으로 옳은 것은?\n"
              "[[-2x + y = 5]] ⋯ ㉠, [[x - y = -2]] ⋯ ㉡ 에서\n"
              "㉠식을 [[y]]에 관하여 풀면, ( ① ) ⋯ ㉢\n"
              "㉢식을 ㉡식에 대입하여 [[y]]를 소거하면 ( ② )\n"
              "이것을 풀면 [[x]] = ( ③ )\n"
              "이 값을 ㉢식에 대입하여 풀면\n"
              "[[y]] = 2 × ( ④ ) + 5 = ( ⑤ )"),
    choices=["[[x = frac(y - 5, 2)]]", "[[x - 2x + 5 = -2]]", "[[3]]", "[[-3]]", "[[1]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="① y = 2x + 5여야 함 ✗, ② x − (2x + 5) = −2 → x − 2x − 5 ✗, ③ x = −3 ✗, ④ 2 × (−3) ✓, ⑤ y = −1 ✗ → ④ (빠른정답 없음). 연립 중괄호는 콤마 나열, 빈칸 ( ① ) 등은 텍스트.")

# p10 가감법
add(id="0dabdd6a", qtype="choice",
    question="연립방정식 [[3x - 4y = 1]] ⋯ ㉠, [[2x + 5y = 16]] ⋯ ㉡ 을 가감법으로 풀려고 한다. [[y]]를 소거하는 데 필요한 계산식은?",
    choices=["㉠×5 − ㉡×4", "㉠×5 + ㉡×4", "㉠×2 − ㉡×3", "㉠×3 + ㉡×2", "㉠×2 + ㉡×3"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="−4y·5 + 5y·4 = 0 → ㉠×5 + ㉡×4 → ②. 빠른정답 −19와 불일치(선지 범위 밖). 선지 ㉠㉡ 연산은 텍스트.")

# p11
add(id="353522ea", qtype="choice",
    question="다음 연립방정식을 가감법으로 풀 때, [[x]]를 소거하기 위해 알맞은 것은?\n[[5x - 3y = 7]] ⋯⋯ ㉠, [[2x + 2y = 6]] ⋯⋯ ㉡",
    choices=["㉠×2 + ㉡×3", "㉠×2 − ㉡×3", "㉠×3 + ㉡×2", "㉠×3 − ㉡×2", "㉠×2 − ㉡×5"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="5x·2 − 2x·5 = 0 → ㉠×2 − ㉡×5 → ⑤. 빠른정답 4와 불일치.")

# p12
add(id="3a985277", qtype="choice",
    question="연립방정식 [[3x + 2y = 5]] ⋯ ㉠, [[2x - 3y = 6]] ⋯ ㉡ 에서 [[y]]를 소거하는 식은?",
    choices=["㉠×2 − ㉡×3", "㉠×2 + ㉡×3", "㉠×3 − ㉡×2", "㉠×3 + ㉡×2", "㉠×3 − ㉡×4"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="2y·3 + (−3y)·2 = 0 → ㉠×3 + ㉡×2 → ④. 빠른정답 5와 불일치.")

# p13
add(id="ea9f9b2a", qtype="choice",
    question="다음의 연립방정식을 풀 때 가감법을 이용하여 [[x]]를 소거하려고 한다. 올바른 것은?\n[[-x + 2y = 5]] ⋯ ㉠, [[2x + y = 10]] ⋯ ㉡",
    choices=["㉠×㉡", "㉠ − ㉡", "㉠×2 + ㉡", "㉠ + ㉡×2", "㉠×2 − ㉡"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="−x·2 + 2x = 0 → ㉠×2 + ㉡ → ③. 빠른정답 2와 불일치.")

# p24 괄호
add(id="1f985689", qtype="choice",
    question="연립방정식 [[3x + 2(y - 1) = 3]], [[3(x - 2y) + 5y = 2]]의 해가 [[x = a]],\n[[y = b]]일 때, [[a b]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="3x + 2y = 5, 3x − y = 2 → x = 1, y = 1 → ab = 1 → ①. 빠른정답 3과 불일치.")

# p38 순환소수 계수
add(id="8a5403e6", qtype="choice",
    question="연립방정식 [[recdec(0,5) x - recdec(0,4) y = -recdec(1,4)]], [[recdec(2,9) x - recdec(3,9) y + 7 = 0]]을 풀면?",
    choices=["[[x = -3]], [[y = -frac(3,2)]]", "[[x = -3]], [[y = -frac(1,2)]]", "[[x = -1]], [[y = frac(3,2)]]",
             "[[x = -1]], [[y = -frac(1,2)]]", "[[x = 3]], [[y = -frac(3,2)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="5x − 4y = −13, 3x − 4y = −7 (2.9̇ = 3, 3.9̇ = 4) → x = −3, y = −1/2 → ②. 빠른정답 5와 불일치. 순환소수는 recdec(정수부, 순환마디).")

# p41 순환소수 계수
add(id="d98e5cda", qtype="choice",
    question=("다음 연립방정식을 만족시키는 [[x]], [[y]]의 순서쌍을 [[point(p, q)]]라 할 때, [[p q]]의 값은?\n"
              "[[recdec(0,4) x - recdec(0,6) y = recdec(0,8)]] ⋯ ㉠, [[0.5(x - y) + 0.4(y - x) = 0.2]] ⋯ ㉡"),
    choices=["[[-8]]", "[[-4]]", "[[0]]", "[[4]]", "[[8]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="㉠: 2x − 3y = 4, ㉡: x − y = 2 → x = 2, y = 0 → pq = 0 → ③. 빠른정답 2와 불일치.")

# p46 비례식
add(id="2bf04ca9", qtype="choice",
    question=("연립방정식 [[ratio(1, (y - 5)) = ratio(3, (x + 4))]], [[frac(y,7) - frac(3x + 4, 5) = -1]] 의 해가 "
              "[[8x - k y = -5]]를 만족할 때, 상수 [[k]]의 값은?"),
    choices=["[[-5]]", "[[-3]]", "[[-1]]", "[[1]]", "[[3]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="x + 4 = 3(y − 5), 5y − 21x = −7 → x = 2, y = 7 → 16 − 7k = −5 → k = 3 → ⑤ = 빠른정답 ✓.")

# p58 해를 알 때
add(id="710397fc", qtype="choice",
    question="연립방정식 [[x - b y = 0]], [[a x + 4y = 60]] 의 해가 [[point(12, 6)]] 일 때,\n[[2a - 3b]] 의 값을 구하면?",
    choices=["[[15]]", "[[12]]", "[[7]]", "[[0]]", "[[-6]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="b = 2, a = 3 → 2a − 3b = 0 → ④. 빠른정답 8과 불일치.")

# p60
add(id="fe62bfd2", qtype="choice",
    question="[[x]], [[y]]의 순서쌍 [[point(-1, 3)]]가 연립방정식 [[4x - a y = 2]], [[b x + 2y = 8]] 의\n해일 때, 상수 [[a]], [[b]]의 값은?",
    choices=["[[a = -2]], [[b = -2]]", "[[a = -2]], [[b = 2]]", "[[a = 2]], [[b = -6]]", "[[a = 2]], [[b = -2]]", "[[a = 2]], [[b = 2]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="−4 − 3a = 2 → a = −2; −b + 6 = 8 → b = −2 → ①. 빠른정답 −1과 불일치.")

# p61
add(id="e572775e", qtype="short",
    question=("연립방정식 [[frac(x,a) + frac(y,b) = frac(1,b)]], [[frac(x,b) + frac(y,a) = -frac(7, a b)]] 의 해가 [[x = -3]], [[y = 2]]일 "
              "때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.9,
    note="−3/a + 1/b = 0 → a = 3b; −3a + 2b = −7 → b = 1, a = 3 → a + b = 4 = 빠른정답 ✓.")

# p65 해와 조건식
add(id="ce264ce4", qtype="choice",
    question=("연립방정식 [[3x - (8x - 2y) = -8]], [[x - k y = -10]] 의 해가 일차방정식\n"
              "[[frac(x,4) - frac(y,6) = frac(1,3)]]을 만족시킬 때, 상수 [[k]]의 값은?"),
    choices=["[[4]]", "[[6]]", "[[8]]", "[[10]]", "[[12]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="−5x + 2y = −8, 3x − 2y = 4 → x = 2, y = 1 → 2 − k = −10 → k = 12 → ⑤ = 빠른정답 ✓.")

# p69 절댓값
add(id="7670c1d0", qtype="choice",
    question="연립방정식 [[x + abs(y) = 9]], [[x - abs(y) = 3]]을 만족시키는 [[x]], [[y]]의 값이\n[[x y z = 18]]을 만족시킬 때, [[z]]의 값은?",
    choices=["[[-1]] 또는 [[1]]", "[[-1]] 또는 [[2]]", "[[-1]] 또는 [[3]]", "[[1]] 또는 [[2]]", "[[1]] 또는 [[3]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="x = 6, y = ±3 → z = 18/(±18) = ±1 → ① = 빠른정답 ✓.")

# p70 지수 조건
add(id="c391bebf", qtype="choice",
    question=("연립방정식 [[3x + k y = 2]], [[2x - 5y = 39]]의 자연수인 해 [[point(x, y)]]가\n"
              "[[pow(3,x) × pow(9,y) = pow(27,8)]]을 만족시킬 때, 상수 [[k]]의 값은?"),
    choices=["[[-16]]", "[[-29]]", "[[-32]]", "[[-58]]", "[[-64]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="x + 2y = 24, 2x − 5y = 39 → x = 22, y = 1 → 66 + k = 2 → k = −64 → ⑤. 빠른정답 7과 불일치.")

# p73 절댓값·정수해
add(id="a99942eb", qtype="short",
    question=("연립방정식 [[abs(x) + abs(y) = 6]], [[abs(x) + 3 abs(y) = frac(2a + 42, 5)]] 를 만족시키는\n"
              "[[x]], [[y]]가 모두 정수일 때, 가능한 모든 자연수 [[a]]의 값의 합을 구하시오."),
    choices=None, derived_answer="70", figure=None, difficulty_est=3, confidence=0.9,
    note="|y| = (a + 6)/5 ∈ {0,…,6} 정수 → a = 5|y| − 6 자연수 → a = 4, 9, 14, 19, 24 → 합 70 = 빠른정답 ✓.")

# p80 잘못 본 계수
add(id="b9b8d9bb", qtype="choice",
    question=("연립방정식 [[a x + b y = -5]], [[5x + c y = 7]] 을 푸는데 [[c]]를 잘못 보아\n"
              "[[x = 0]], [[y = 1]]을 얻었다. 바르게 풀면 [[x = 3]], [[y = 4]]일 때,\n[[a + b + c]]의 값은?"),
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="b = −5, 3a − 20 = −5 → a = 5, 15 + 4c = 7 → c = −2 → a+b+c = −2 → ①. 빠른정답 4와 불일치.")

# p82
add(id="0adae813", qtype="short",
    question=("연립방정식 [[a x + b y = 4]], [[c x - y = 10]]을 푸는데 [[c]]를 [[d]]로\n"
              "잘못 보고 풀었더니 해가 [[x = 5]], [[y = 10]]이 되었다. 바르게\n"
              "풀었을 때의 해가 [[x = -3]], [[y = 2]]일 때, [[a + b + c + d]]의\n"
              "값을 구하시오. (단, [[a]], [[b]], [[c]], [[d]]는 상수)"),
    choices=None, derived_answer="0", figure=None, difficulty_est=3, confidence=0.9,
    note="5a + 10b = 4, −3a + 2b = 4 → a = −4/5, b = 4/5; d = 4, c = −4 → 합 0 = 빠른정답 ✓.")

# p83
add(id="e958a504", qtype="short",
    question=("연립방정식 [[a x + b y = 2]], [[c x - y = 9]]를 푸는데 [[c]]를 [[d]]로\n"
              "잘못 보고 풀었더니 해가 [[x = 6]], [[y = 9]]가 되었다. 바르게\n"
              "풀었을 때의 해가 [[x = -1]], [[y = 3]]일 때, [[a + b - c - d]]의\n"
              "값을 구하시오. (단, [[a]], [[b]], [[c]], [[d]]는 상수)"),
    choices=None, derived_answer="frac(245,27)", figure=None, difficulty_est=3, confidence=0.9,
    note="6a + 9b = 2, −a + 3b = 2 → a = −4/9, b = 14/27; d = 3, c = −12 → 2/27 + 9 = 245/27 = 빠른정답 ✓.")

# p84 해가 같은 두 연립
add(id="10df8160", qtype="short",
    question=("두 연립방정식 { [[3y = a x + 9]], [[5(x + y) - 2(3x - y) = 5]] },\n"
              "{ [[5x - 4y = b]], [[ratio((x + 4y), (2x + 5)) = ratio(2, 3)]] }의 해가 서로 같을 때, 상수 [[a]],\n"
              "[[b]]에 대하여 [[b - a]]의 값을 구하시오."),
    choices=None, derived_answer="9", figure=None, difficulty_est=3, confidence=0.9,
    note="−x + 7y = 5, −x + 12y = 10 → x = 2, y = 1 → a = −3, b = 6 → b − a = 9 = 빠른정답 ✓. 두 연립의 중괄호는 텍스트 { }.")

# p87
add(id="b6da0555", qtype="choice",
    question=("[[x]], [[y]]에 관한 두 연립방정식\n"
              "{ [[3x + 4y = 8]], [[a x - b y = 5]] }, { [[b x + a y = 3]], [[x + 3y = 1]] }의 해가 같을 때,\n"
              "상수 [[a]], [[b]]의 값은?"),
    choices=["[[a = 1]], [[b = 2]]", "[[a = 1]], [[b = 1]]", "[[a = 1]], [[b = -1]]", "[[a = -1]], [[b = 1]]", "[[a = -2]], [[b = -1]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="3x + 4y = 8, x + 3y = 1 → x = 4, y = −1 → 4a + b = 5, 4b − a = 3 → a = b = 1 → ② = 빠른정답 ✓. 두 연립의 중괄호는 텍스트 { }.")

# p89 (id 2개)
dup(["77cdd35f", "ae9f19a0"], qtype="short",
    question=("연립방정식 [[3x - 5y = -18]], [[-x + a y = 32]]를 만족시키는 [[x]], [[y]]의 값을\n"
              "각각 2배 하면 연립방정식 [[x - 3y = -28]], [[b x + 2y = -48]]의 해가\n"
              "된다고 할 때, 상수 [[a]], [[b]]에 대하여 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="-54", figure=None, difficulty_est=3, confidence=0.9,
    note="(2x, 2y)가 둘째 연립의 해 → x − 3y = −14, 3x − 5y = −18 → x = 4, y = 6 → a = 6; 8b + 24 = −48 → b = −9 → ab = −54. 빠른정답 1과 불일치. 같은 쪽 id 2개.")

# p92 해가 무수히 많은 경우
add(id="b82d0528", qtype="short",
    question=("해가 무수히 많은 [[x]], [[y]]에 관한 연립방정식\n"
              "[[a x + b y + c = 0]], [[c x + a y + b = 0]]을 만족하는 [[x]], [[y]]에 대하여 [[x + y]]의\n"
              "값을 구하시오. (단, [[a]], [[b]], [[c]]는 0이 아니다.)"),
    choices=None, derived_answer="-1", figure=None, difficulty_est=3, confidence=0.85,
    note="a/c = b/a = c/b = k → k³ = 1 → a = b = c → a(x + y + 1) = 0 → x + y = −1. 빠른정답 −54와 불일치.")

# p93
add(id="65fca94c", qtype="short",
    question="연립방정식 [[6x + a y = 4]], [[b x - 8y = 8]]의 해가 무수히 많을 때, 상수 [[a]],\n[[b]]에 대하여 [[a b]]의 값을 구하시오.",
    choices=None, derived_answer="-48", figure=None, difficulty_est=2, confidence=0.9,
    note="6/b = a/(−8) = 4/8 → b = 12, a = −4 → ab = −48. 빠른정답 5와 불일치.")

# p94
add(id="b9f2ea59", qtype="choice",
    question="다음 연립방정식 중 해가 무수히 많은 것은?",
    choices=["[[x - 3y = 3]], [[4x - 12y = -1]]", "[[x - 2y = 3]], [[5x - 10y = -15]]", "[[2x + y = 5]], [[x - 2y = 10]]",
             "[[3x + 2y = 4]], [[2x + 3y = -2]]", "[[x = 3y - 5]], [[4x - 2(x + 3y) = -10]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="⑤ 둘째 식 2x − 6y = −10 ⇔ x − 3y = −5 = 첫째 식 → 해 무수히 많음 → ⑤. 빠른정답 15와 불일치(선지 범위 밖). 선지의 연립 중괄호는 콤마 나열.")

# p96
add(id="4a2567b4", qtype="choice",
    question="연립방정식 [[x + y = b]], [[a x + 2y = -4]] 의 해가 무수히 많을 때,\n상수 [[a]], [[b]]의 값은?",
    choices=["[[a = 1]], [[b = -1]]", "[[a = 1]], [[b = -2]]", "[[a = 2]], [[b = -1]]", "[[a = 2]], [[b = -2]]", "[[a = 3]], [[b = -3]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a/1 = 2/1 = −4/b → a = 2, b = −2 → ④. 빠른정답 −48과 불일치(선지 범위 밖).")

# p99 해가 없는 경우
add(id="3c87d125", qtype="choice",
    question="연립방정식 [[y = a x + 1]], [[y = -x - 2]]의 해가 없을 때, 상수 [[a]]의 값은?",
    choices=["[[0]]", "[[-1]]", "[[2]]", "[[frac(1,2)]]", "[[-frac(1,2)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="기울기 같고 y절편 다름 → a = −1 → ②. 빠른정답 4와 불일치.")

# ======================= 지수법칙 =======================
# p10 빈칸
add(id="68b1aba5", qtype="short",
    question="다음 □ 안에 알맞은 수를 써넣으시오.\n([[pow(x,4)]])^□ = [[pow(x,8)]]",
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.9,
    note="(x⁴)² = x⁸ → 2. 빠른정답 4와 불일치. 지수 자리 빈칸 상자는 ^□ 텍스트.")

# p11
add(id="456602cc", qtype="choice",
    question="[[pow(pow(pow(a,3),2),7)]]을 간단히 하면?",
    choices=["[[pow(a,21)]]", "[[pow(a,24)]]", "[[pow(a,27)]]", "[[pow(a,28)]]", "[[pow(a,42)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="a^(3·2·7) = a⁴² → ⑤. 빠른정답 3과 불일치. 원문 중괄호 {(a³)²}⁷는 pow 중첩으로.")

# p22 (id 4개) 빈칸 비교
dup(["ca097046", "4f8aa353", "6b52598d", "d2244bdb"], qtype="choice",
    question="다음 중 □ 안에 알맞은 수가 가장 큰 것은?",
    choices=["[[pow(a,6) ÷ pow(a,4)]] = [[a]]^□", "[[pow(pow(a,2),4) ÷ pow(a,2)]] = [[a]]^□", "[[pow(a,15) ÷ pow(a,3) ÷ pow(a,5)]] = [[a]]^□",
             "[[pow(pow(a,6),2) ÷ pow(pow(a,3),3)]] = [[a]]^□", "[[pow(a,11) ÷ pow(pow(a,2),3) ÷ a]] = [[a]]^□"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="□ = 2, 6, 7, 3, 4 → ③. 빠른정답 1과 불일치. 같은 쪽 id 4개. 지수 자리 빈칸 상자는 ^□ 텍스트.")

# p25 곱의 거듭제곱
add(id="9cbeb218", qtype="short",
    question=("네 자연수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[pow(pow(x,a) pow(y,b) pow(z,c), d) = pow(x,12) pow(y,30) pow(z,42)]]이 "
              "성립할 때, [[a + b + c]]의 값 중 가장 작은 값을 구하시오."),
    choices=None, derived_answer="14", figure=None, difficulty_est=2, confidence=0.9,
    note="ad = 12, bd = 30, cd = 42 → d 최대 = gcd = 6 → a+b+c = 2+5+7 = 14. 빠른정답 3과 불일치.")

# p84 일의 자리
add(id="391a7506", qtype="short",
    question=("자연수 [[n]]의 일의 자리의 숫자를 < [[n]] >이라 하자.\n"
              "[[a = pow(pow(3,3),5)]], [[b = pow(3,6) × pow(3,4)]]일 때, < [[a]] > + < [[b]] >의 값을\n구하시오."),
    choices=None, derived_answer="16", figure=None, difficulty_est=2, confidence=0.9,
    note="a = 3¹⁵ → 일의 자리 7, b = 3¹⁰ → 9 → 16. 빠른정답 2와 불일치. 기호 <n>은 마커 밖 텍스트.")

# p85
add(id="80248c1c", qtype="short",
    question=("자연수 [[n]]에 대하여 [[pow(2,n) + pow(7,n) + pow(9,n)]]의 일의 자리 숫자를\n"
              "[[sub(a,n)]]이라 하자. [[frac(sub(a,1), 10) + frac(sub(a,2), pow(10,2)) + frac(sub(a,3), pow(10,3))]] + ⋯ = [[frac(q,p)]] 일 때,\n"
              "[[p - q]]의 값을 구하시오. (단, [[p]], [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="1591", figure=None, difficulty_est=3, confidence=0.9,
    note="aₙ = 8, 4, 0, 8 반복 → 0.8̇408̇ = 8408/9999(기약) → p − q = 1591. 빠른정답 6과 불일치. 줄임표 ⋯는 텍스트.")

# ======================= 일차방정식(미지수가 2개) =======================
# p10
add(id="08b0693a", qtype="choice",
    question="다음에서 미지수가 2개인 일차방정식을 모두 고른 것은?\n(정답 2개)",
    choices=["[[x - 1 = 0]]", "[[2x - 1 = x]]", "[[y = 2x + 2]]", "[[x y = 1]]", "[[x - y = 1]]"],
    derived_answer="③, ⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="③, ⑤만 미지수 2개인 일차방정식(④는 xy 항). 빠른정답 2와 불일치. 복수 정답 문항.")

# p40
add(id="85f2cbf0", qtype="choice",
    question="다음 중 [[x]], [[y]]가 자연수일 때,\n일차방정식 [[2x + y = 9]]의 해가 아닌 것은?",
    choices=["[[point(1, 7)]]", "[[point(2, 5)]]", "[[point(3, 3)]]", "[[point(4, 1)]]", "[[point(5, 1)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="(5, 1): 10 + 1 = 11 ≠ 9 → ⑤ = 빠른정답 ✓.")

# p53
add(id="6debbfeb", qtype="choice",
    question=("[[x]], [[y]]가 자연수일 때, 일차방정식 [[3x + 2y = 17]]의 해를\n[[x = a]], [[y = b]]라 하자. 다음 중 [[b - a]]의 값이 될 수 있는\n"
              "것을 모두 고르면? (정답 2개)"),
    choices=["[[-4]]", "[[-2]]", "[[2]]", "[[4]]", "[[6]]"],
    derived_answer="①, ⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="해 (1,7), (3,4), (5,1) → b − a = 6, 1, −4 → ①, ⑤. 빠른정답 3과 불일치. 복수 정답 문항.")

# p62
add(id="8fbc70a4", qtype="short",
    question=("[[x = 1]], [[y = -3]]이 [[x]], [[y]]에 대한 일차방정식\n[[(5a + 3b) x + 2(a - b) y = 0]]의 해일 때, 일차방정식\n"
              "[[a x - 6b = 2b y - 3a]]를 만족시키는 [[x]], [[y]]에 대하여\n[[9x - 2y]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이고\n[[b != 0]]이다.)"),
    choices=None, derived_answer="-21", figure=None, difficulty_est=3, confidence=0.9,
    note="5a + 3b − 6a + 6b = 0 → a = 9b → 9bx − 6b = 2by − 27b → 9x − 2y = −21. 빠른정답 15와 불일치.")

# p64
add(id="8d46ad0e", qtype="choice",
    question=("[[x]], [[y]]에 관한 일차방정식\n[[2 pow(a,2) - 2a(x + 4) + 2x - 4y = 0]]이 [[point(a, -3)]], [[point(b, 2)]]를\n"
              "해로 가질 때, 상수 [[a]], [[b]]에 대하여 [[3a + 2b]]의 값은?"),
    choices=["[[-10]]", "[[-5]]", "[[1]]", "[[5]]", "[[10]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="(a, −3) 대입: −6a + 12 = 0 → a = 2 → 식 x + 2y = −4 → (b, 2): b = −8 → 3a + 2b = −10 → ①. 빠른정답 3과 불일치.")

# p66
add(id="82ecb8ed", qtype="short",
    question=("[[x]], [[y]]가 자연수일 때, 방정식 [[frac(x + 3, 2) = frac(7 - y, 3)]]의 해가\n"
              "[[a x + b y = 5]]를 만족시킨다. 이때 상수 [[a]], [[b]]에 대하여\n[[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="3x + 2y = 5의 자연수 해 (1, 1) → a + b = 5. 빠른정답 3과 불일치.")

# p77 연산 기호
add(id="585b063b", qtype="choice",
    question=("연산 ⊙을 [[x]] ⊙ [[y]] = [[2x + y]]라 정의할 때, 자연수 [[x]], [[y]]에\n"
              "대하여 [[x]] ⊙ [[2y]] = 4 ⊙ 2의 해를 모두 고르면?"),
    choices=["[[point(1, 5)]]", "[[point(2, 3)]]", "[[point(3, 3)]]", "[[point(4, 1)]]", "[[point(5, 6)]]"],
    derived_answer="②, ④", figure=None, difficulty_est=2, confidence=0.9,
    note="2x + 2y = 10 → x + y = 5 → (2, 3), (4, 1) → ②, ④ = 빠른정답 '2, 4' ✓. 연산 기호 ⊙은 텍스트. 복수 정답 문항.")

# p78
add(id="053be5bb", qtype="choice",
    question="두 자연수 [[a]], [[b]]에 대하여 [[a]] ◉ [[b]] = [[3a - b]]라고 할 때,\n[[5x]] ◉ [[4y]] = 4 ◉ 5의 해는? (단, [[x]], [[y]]는 자연수)",
    choices=["[[point(-1, -2)]]", "[[point(1, -2)]]", "[[point(1, 2)]]", "[[point(2, 1)]]", "[[point(-2, 1)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="15x − 4y = 7 → 자연수 해 (1, 2) → ③ = 빠른정답 ✓. 연산 기호 ◉은 텍스트.")

# p80
add(id="2cad4854", qtype="choice",
    question=("두 정수 [[m]], [[n]]에 대하여 [[m]] △ [[n]] = [[4m - 3n]]라 정의할 때,\n"
              "다음 [[m]], [[n]]의 순서쌍 [[point(m, n)]] 중 [[x]] △ [[3y]] = 6 △ ([[-2]])의\n해인 것은?"),
    choices=["[[point(2, 1)]]", "[[point(-1, 3)]]", "[[point(0, 4)]]", "[[point(3, -2)]]", "[[point(4, -2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="4x − 9y = 30 → (3, −2)만 성립 → ④. 빠른정답 '2, 4'와 불일치. 연산 기호 △은 텍스트.")

# p90
add(id="980bb4de", qtype="choice",
    question=("두 수 [[a]], [[b]]에 대하여 연산 ◉을\n[[a]] ◉ [[b]] = [[2a + 3b]]로 약속하고 자연수 [[x]], [[y]]에 대한\n"
              "방정식 ([[x + 1]]) ◉ ([[y - 1]]) = 8의 해를 [[point(m, n)]]이라 할\n때, [[m n]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="2x + 3y = 9 → 자연수 해 (3, 1) → mn = 3 → ③. 빠른정답 6과 불일치. 연산 기호 ◉은 텍스트.")

# p91
add(id="70a3e97c", qtype="choice",
    question=("두 수 [[a]], [[b]]에 대하여 연산 ◉을\n[[a]] ◉ [[b]] = [[4a + 5b]]로 약속하고 자연수 [[x]], [[y]]에 대한 방정식\n"
              "([[x - 1]]) ◉ ([[y + 2]]) = 19의 해를 [[x = m]], [[y = n]]이라 할 때,\n[[m n]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="4x + 5y = 13 → 자연수 해 (2, 1) → mn = 2 → ②. 빠른정답 5와 불일치. 연산 기호 ◉은 텍스트.")

# p94 성질
add(id="21b12e8c", qtype="choice",
    question="[[x]], [[y]]가 자연수일 때, 다음 중 [[3x + 2y = 25]]에 대한 설명으로 옳지 않은 것을 모두 고르면? (정답 2개)",
    choices=["미지수가 2개인 일차방정식이다.", "[[x = 5]]일 때, [[y = 6]]이다.", "해는 5쌍이다.",
             "[[y]]에 대하여 정리하면 [[y = -frac(3,2) x + frac(25,2)]]이다.", "[[x]], [[y]]가 모든 수일 때, 해의 순서쌍 [[point(x, y)]]는 무수히 많다."],
    derived_answer="②, ③", figure=None, difficulty_est=2, confidence=0.9,
    note="② x = 5 → y = 5 ✗, ③ 해 (1,11), (3,8), (5,5), (7,2) 4쌍 ✗ → ②, ③. 빠른정답 2와 부분 일치. 복수 정답 문항.")
