# -*- coding: utf-8 -*-
# esc_sonnet_m3-2_2of6 — 이미지 기준 전사 (81 항목 / 80쪽) : 삼각비 48쪽(49 id) + 원의 현 32쪽
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))
def fig(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
FR = "도형 표현 불가: "

# ───────────── 삼각비 ─────────────
# p13
add(id="2871fa7d", qtype="short",
    question="다음 그림과 같은 [[angle(C) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AB) = 15]]이고 [[sin(A) = frac(4,5)]]일 때, [[seg(AC)]]의 길이를 구하시오.",
    choices=None, derived_answer="9",
    figure=fig("직각삼각형 ABC(∠C=90°, C 왼쪽 아래·B 오른쪽 아래·A 위), 빗변 AB=15 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형(치수·직각 표시)",
    note="BC=12, AC=9.")

# p14
add(id="1356e1a2", qtype="short",
    question="다음 그림과 같은 [[angle(C) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AB) = 8]]이고 [[cos(A) = frac(sqrt(7), 4)]]일 때, [[seg(BC)]]의 길이를 구하시오.",
    choices=None, derived_answer="6",
    figure=fig("직각삼각형 ABC(∠C=90°), 빗변 AB=8 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형(치수·직각 표시)",
    note="AC=2√7, BC=√(64−28)=6.")

# p15
add(id="e53fae88", qtype="short",
    question="다음 그림과 같은 [[angle(C) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AB) = 12]]이고 [[sin(A) = frac(sqrt(5), 3)]]일 때, [[seg(AC)]]의 길이를 구하시오.",
    choices=None, derived_answer="8",
    figure=fig("직각삼각형 ABC(∠C=90°), 빗변 AB=12 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형(치수·직각 표시)",
    note="BC=4√5, AC=√(144−80)=8.")

# p16
add(id="647248c1", qtype="choice",
    question="다음 그림과 같은 직각삼각형 ABC에서 [[seg(AB) = 15]], [[sin(A) = frac(3,5)]]일 때, [[x + y]]의 값은?",
    choices=["20", "21", "22", "23", "24"], derived_answer="②",
    figure=fig("직각삼각형 ABC(∠C=90°), AB=15, AC=x, BC=y 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형(치수·직각 표시)",
    note="y=BC=9, x=AC=12 → 21 → ②. 빠른정답 3과 불일치.")

# p20
add(id="ea5484a8", qtype="choice",
    question="다음 그림과 같이 [[angle(C) = deg(90)]]인 직각삼각형 ABC에서 [[tan(A) = frac(3,2)]], [[seg(AC) = 6]] cm일 때, [[seg(BC)]]의 길이는?",
    choices=["6 cm", "7 cm", "8 cm", "9 cm", "10 cm"], derived_answer="④",
    figure=fig("직각삼각형 ABC(∠C=90°, B 왼쪽·C 오른쪽 아래·A 위), AC=6cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형(치수·직각 표시)",
    note="BC=AC·tanA=9 → ④. 빠른정답 15와 불일치.")

# p22
add(id="79a344fd", qtype="choice",
    question="다음 그림과 같이 [[angle(C) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AB) = 8]] cm, [[sin(B) = frac(3,4)]]일 때, [[seg(BC)]]의 길이는?",
    choices=["6 cm", "[[2 sqrt(7)]] cm", "5 cm", "[[2 sqrt(6)]] cm", "4 cm"], derived_answer="②",
    figure=fig("직각삼각형 ABC(∠C=90°, B 왼쪽 아래·C 오른쪽 아래·A 위), 빗변 AB=8cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형(치수·직각 표시)",
    note="AC=6, BC=√(64−36)=2√7 → ②. 빠른정답 54와 불일치.")

# p24
add(id="5d49d9d8", qtype="short",
    question="[[angle(B) = deg(90)]]인 직각삼각형 ABC에서 [[seg(BC) = 6]], [[sin(A) = frac(3,4)]]일 때, 선분 AC의 길이를 구하시오.",
    choices=None, derived_answer="8",
    figure=fig("직각삼각형 ABC(∠B=90°, A 왼쪽 아래·B 오른쪽 아래·C 위), BC=6 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형(치수·직각 표시)",
    note="출처 [2024년 3월 고1 23번 변형]. sinA=BC/AC → AC=8. 빠른정답 1과 불일치.")

# p27
add(id="f8dec093", qtype="short",
    question="[[ratio(sin(A), cos(A)) = ratio(8, 1)]]일 때, [[frac(tan(A) + 1, tan(A) - 1)]]의 값을 구하시오. (단, [[deg(0) < A < deg(90)]])",
    choices=None, derived_answer="frac(9,7)", figure=None, difficulty_est=2, confidence=0.9,
    note="tanA=8 → 9/7.")

# p28
add(id="78996fa7", qtype="short",
    question="[[ratio(sin(A), cos(A)) = ratio(3, 4)]]일 때, [[frac(tan(A) + 1, tan(A) - 1)]]의 값을 구하시오. (단, [[deg(0) < A < deg(90)]])",
    choices=None, derived_answer="-7", figure=None, difficulty_est=2, confidence=0.9,
    note="tanA=3/4 → (7/4)/(−1/4)=−7.")

# p31
add(id="552f2216", qtype="short",
    question="다음 그림과 같이 [[angle(C) = deg(90)]]이고 [[seg(AC) = 15]]인 삼각형 ABC에서 [[seg(AD) = seg(BD)]]이다. [[angle(ABC) = x]], [[angle(ADC) = y]]라 하면 [[tan(x) = frac(3,5)]]일 때, [[cos(y)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(8,17)",
    figure=fig("삼각형 ABC(∠C=90°, B 왼쪽·C 오른쪽 아래·A 위), 변 BC 위의 점 D, AD=BD 등호 표시, ∠B=x, ∠ADC=y, AC=15"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "삼각형+내부 선분(각·치수 표시)",
    note="BC=25, BD=AD=17, DC=8 → cos y=8/17.")

# p36
add(id="ab3623b5", qtype="choice",
    question="아래 그림에서 [[angle(C) = deg(90)]], [[perp(seg(AB), seg(CD))]]이고 [[angle(B) = x]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[sin(x) = frac(seg(AC), seg(AB))]]", "[[cos(x) = frac(seg(CD), seg(AC))]]", "[[tan(x) = frac(seg(CD), seg(AD))]]",
             "[[sin(x) = frac(seg(AD), seg(AC))]]", "[[cos(x) = frac(seg(BD), seg(BC))]]"],
    derived_answer="③",
    figure=fig("직각삼각형 ABC(∠C=90°, B 왼쪽·C 오른쪽 아래·A 위), 점 D는 AB 위의 수선의 발(CD⊥AB), ∠B=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형+수선(각 표시)",
    note="∠ACD=x이므로 tanx=AD/CD, ③이 틀림.")

# p37
add(id="61c0a048", qtype="short",
    question="다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 [[perp(seg(AD), seg(BC))]]이고 [[angle(BAD) = x]], [[angle(CAD) = y]]일 때, [[tan(x) + cos(y)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(32,15)",
    figure=fig("직각삼각형 ABC(∠A=90°, A 위, B 왼쪽·C 오른쪽 아래), D는 BC 위의 수선의 발, ∠BAD=x, ∠CAD=y, AC=3, BC=5"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "직각삼각형+수선(각·치수 표시)",
    note="AB=4, x=∠C, y=∠B → 4/3+4/5=32/15.")

# p38
add(id="8b3e2a33", qtype="choice",
    question="다음 그림과 같이 직사각형 ABCD의 꼭짓점 A에서 대각선 BD에 내린 수선의 발을 H라 하자. [[seg(AB) = 5]], [[seg(BC) = 12]]이고 [[angle(DAH) = x]]라 할 때, [[sin(x) + cos(x)]]의 값은?",
    choices=["[[frac(9,13)]]", "[[frac(11,13)]]", "1", "[[frac(15,13)]]", "[[frac(17,13)]]"], derived_answer="⑤",
    figure=fig("직사각형 ABCD(A 왼쪽 위·B 왼쪽 아래·C 오른쪽 아래·D 오른쪽 위), 대각선 BD, A에서 BD에 내린 수선의 발 H, ∠DAH=x, AB=5, BC=12"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "직사각형+대각선·수선(각·치수 표시)",
    note="x=∠ABD, sinx=12/13, cosx=5/13 → 17/13 → ⑤.")

# p40
add(id="ec4a8515", qtype="choice",
    question="다음 그림과 같이 [[angle(A) = deg(90)]]인 삼각형 ABC에서 [[perp(seg(AH), seg(BC))]]이고 [[seg(AB) = 4]], [[seg(BC) = 5]]일 때, [[sin(x)]]의 값은?",
    choices=["[[frac(3,5)]]", "[[frac(3,4)]]", "[[frac(4,5)]]", "[[frac(5,4)]]", "[[frac(4,3)]]"], derived_answer="①",
    figure=fig("직각삼각형 ABC(∠A=90°, A 위), H는 BC 위의 수선의 발, ∠HAC=x, AB=4, BC=5"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형+수선(각·치수 표시)",
    note="x=∠HAC=∠B, sinB=AC/BC=3/5 → ①.")

# p43
add(id="4bf46346", qtype="short",
    question="다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 [[perp(seg(AH), seg(BC))]]이고 [[angle(HAC) = x]]라 할 때, [[cos(x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(7,9)",
    figure=fig("직각삼각형 ABC(∠A=90°, A 위), H는 BC 위의 수선의 발, ∠HAC=x, AB=7, AC=4√2"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형+수선(각·치수 표시)",
    note="BC=9, x=∠B, cosB=7/9.")

# p44 (id 2개, 문항 1개)
dup(["844da690", "3388a615"], qtype="choice",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]이고 [[seg(AB) = 5]], [[seg(AC) = 12]]인 직각삼각형 ABC에 대하여 점 A에서 선분 BC에 내린 수선의 발을 H라 하자. "
              "선분 HC 위의 점 D에 대하여 [[tan(angle(ADH)) = 3]]일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[seg(AH) = frac(60,13)]]\nㄴ. [[seg(BD) = frac(45,13)]]\nㄷ. [[seg(AB) = seg(BD)]]"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="③",
    figure=fig("직각삼각형 ABC(∠A=90°, A 위, B 왼쪽·C 오른쪽 아래), BC 위의 점 H(수선의 발)·D, AB=5, AC=12 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "직각삼각형+수선·내부 선분(치수 표시)",
    note="출처 [2017년 3월 고1 19번 변형]. BC=13, AH=60/13 ㄱ✓, HD=20/13, BH=25/13 → BD=45/13 ㄴ✓, ㄷ✗ → ③.")

# p46
add(id="fc94d389", qtype="short",
    question="다음 그림과 같은 [[tri(ABC)]]에서 [[sin(x) × cos(x) × tan(x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(144,169)",
    figure=fig("삼각형 ABC(∠A=90°, B 왼쪽 아래·C 오른쪽 아래·A 오른쪽 위), AB=12, AC=5, AB 위의 점 D에서 BC에 내린 수선의 발 E(DE⊥BC), ∠BDE=x"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "직각삼각형+수선(각·치수 표시)",
    note="x=∠C, BC=13 → (12/13)(5/13)(12/5)=144/169.")

# p48
add(id="6d300bc8", qtype="choice",
    question="다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 [[perp(seg(BC), seg(DE))]], [[seg(AB) = 15]], [[seg(AC) = 8]]이고 [[angle(BDE) = x]]라 할 때, [[sin(x)]]의 값은?",
    choices=["[[frac(7,17)]]", "[[frac(8,17)]]", "[[frac(8,15)]]", "[[frac(15,17)]]", "[[frac(15,8)]]"], derived_answer="④",
    figure=fig("직각삼각형 ABC(∠A=90°), AB 위의 점 D, BC 위의 점 E(DE⊥BC), ∠BDE=x, AB=15, AC=8"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형+수선(각·치수 표시)",
    note="x=∠C, BC=17 → sinC=15/17 → ④.")

# p49
add(id="4b49e675", qtype="choice",
    question="다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 [[perp(seg(DE), seg(BC))]], [[seg(BC) = 10]], [[seg(AC) = 6]]일 때, [[sin(x) + cos(x) + tan(x)]]의 값은?",
    choices=["[[frac(4,5)]]", "[[frac(5,3)]]", "[[frac(12,5)]]", "[[frac(39,15)]]", "[[frac(41,15)]]"], derived_answer="⑤",
    figure=fig("직각삼각형 ABC(∠A=90°), AB 위의 점 E, BC 위의 점 D(DE⊥BC), ∠BED=x, BC=10, AC=6"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "직각삼각형+수선(각·치수 표시)",
    note="x=∠C, AB=8 → 4/5+3/5+4/3=41/15 → ⑤.")

# p51
add(id="c00f3015", qtype="choice",
    question="다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC의 꼭짓점 A에서 변 BC에 내린 수선의 발을 D, 점 D에서 [[seg(AC)]]에 내린 수선의 발을 E라 하자. [[angle(BAD) = x]]라 할 때, 다음 중 [[tan(x)]]를 나타내는 것이 아닌 것은?",
    choices=["[[frac(seg(BD), seg(AD))]]", "[[frac(seg(CD), seg(AD))]]", "[[frac(seg(AB), seg(AC))]]", "[[frac(seg(AE), seg(DE))]]", "[[frac(seg(DE), seg(CE))]]"],
    derived_answer="②",
    figure=fig("직각삼각형 ABC(∠A=90°, A 위, B 왼쪽·C 오른쪽 아래), BC 위의 수선의 발 D, AC 위의 수선의 발 E, ∠BAD=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형+수선 2개(각 표시)",
    note="x=∠C=∠ADE; CD/AD=tan(∠DAC)=tanB → ②.")

# p55
add(id="06d44477", qtype="choice",
    question="다음 그림에서 [[perp(seg(AB), seg(AC))]], [[perp(seg(AD), seg(BC))]], [[perp(seg(AC), seg(DE))]]이다. [[angle(BAD) = x]], [[angle(CAD) = y]]라 할 때, [[(cos(x) + sin(y)) × tan(y)]]의 값은?",
    choices=["[[frac(sqrt(5), 5)]]", "[[frac(sqrt(5), 4)]]", "[[frac(sqrt(5), 3)]]", "[[frac(sqrt(5), 2)]]", "[[sqrt(5)]]"], derived_answer="①",
    figure=fig("직각삼각형 ABC(∠A=90°, B 왼쪽·C 오른쪽 아래·A 위), BC 위의 수선의 발 D, AC 위의 수선의 발 E, ∠BAD=x, ∠CAD=y, AE=12, EC=3"),
    difficulty_est=3, confidence=0.85, needs_review=FR + "직각삼각형+수선 2개(각·치수 표시)",
    note="AC=15, CD=3√5, AD=6√5; cosx=cosC=√5/5, siny=√5/5, tany=1/2 → √5/5 → ①.")

# p56
add(id="6cc3d48c", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]]과 [[x]]축, [[y]]축의 교점을 각각 A, B라 할 때, 직각삼각형 AOB에서 [[tan(A) = frac(24, 7)]]이다. "
              "또, 원점 O에서 직선 [[l]]에 내린 수선의 발 H에 대하여 [[seg(OH) = frac(168, 5)]]일 때, 직선 [[l]]은 점 [[point(7, k)]]를 지난다. "
              "이때 상수 [[k]]의 값은? (단, 점 H는 제2사분면 위의 점이다.)"),
    choices=["140", "144", "148", "152", "156"], derived_answer="②",
    figure=fig("좌표평면: 직선 l이 x축의 음의 부분과 점 A, y축의 양의 부분과 점 B에서 만남, 원점 O에서 l에 내린 수선의 발 H(제2사분면), OH=168/5 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "좌표평면 직선+수선(치수 표시)",
    note="OA=7t, OB=24t, OH=168t/25 → t=5, l: y=(24/7)x+120 → k=144 → ②.")

# p57
add(id="ed03f3f9", qtype="choice",
    question=("다음 그림에서 두 점 A, B는 각각 직선 [[y = m x + n]]과 [[x]]축, [[y]]축의 교점이고 [[perp(seg(AB), seg(OH))]], [[seg(OH) = 1]]이다. "
              "[[angle(BAO) = a]]라 하면 [[tan(a) = frac(15, 8)]]일 때, 양수 [[m]], [[n]]에 대하여 [[m + n]]의 값은? (단, O는 원점이다.)"),
    choices=["[[frac(29, 8)]]", "[[frac(15, 4)]]", "[[frac(31, 8)]]", "4", "[[frac(33, 8)]]"], derived_answer="④",
    figure=fig("좌표평면: 직선 y=mx+n이 x축의 음의 부분과 A, y축의 양의 부분과 B에서 만남, 원점 O에서 내린 수선의 발 H, OH=1, ∠BAO=a 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "좌표평면 직선+수선(각·치수 표시)",
    note="m=15/8, OA=8t, OB=15t, OH=120t/17=1 → n=OB=17/8 → m+n=4 → ④.")

# p58
add(id="8f613bee", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]]과 [[x]]축, [[y]]축의 교점을 각각 A, B라 할 때, 직각삼각형 AOB에서 [[tan(A) = frac(4, 3)]]이다. "
              "또, 원점 O에서 직선 [[l]]에 내린 수선의 발 H에 대하여 [[seg(OH) = 12]]일 때, 직선 [[l]]은 점 [[point(3, k)]]를 지난다. "
              "이때 상수 [[k]]의 값은? (단, 점 H는 제2사분면 위의 점이다.)"),
    choices=["21", "22", "23", "24", "25"], derived_answer="④",
    figure=fig("좌표평면: 직선 l이 x축의 음의 부분과 A, y축의 양의 부분과 B에서 만남, 원점 O에서 l에 내린 수선의 발 H(제2사분면), OH=12 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "좌표평면 직선+수선(치수 표시)",
    note="OA=15, OB=20, l: y=(4/3)x+20 → k=24 → ④. 빠른정답 144/169와 불일치.")

# p66
add(id="d0344679", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]]과 [[x]]축, [[y]]축의 교점을 각각 A, B라 할 때, 직각삼각형 AOB에서 [[tan(A) = frac(15, 8)]]이다. "
              "또, 원점 O에서 직선 [[l]]에 내린 수선의 발 H에 대하여 [[seg(OH) = 32]]일 때, 직선 [[l]]은 점 [[point(-8, k)]]를 지난다. "
              "이때 상수 [[k]]의 값은? (단, 점 H는 제1사분면 위의 점이다.)"),
    choices=["81", "82", "83", "84", "85"], derived_answer="③",
    figure=fig("좌표평면: 직선 l이 x축의 양의 부분과 A, y축의 양의 부분과 B에서 만남(기울기 음수), 원점 O에서 l에 내린 수선의 발 H(제1사분면), OH=32 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "좌표평면 직선+수선(치수 표시)",
    note="t=68/15, OB=68, l: y=−(15/8)x+68 → k=15+68=83 → ③.")

# p67
add(id="2cce129f", qtype="short",
    question="다음 그림과 같이 기울기가 3이고 점 [[point(-3, 6)]]을 지나는 직선이 [[x]]축, [[y]]축과 만나는 점을 각각 A, B라 하자. [[angle(BAO) = deg(a)]]라 할 때, [[sin(deg(a)) × cos(deg(a))]]의 값을 구하시오. (단, O는 원점)",
    choices=None, derived_answer="frac(3,10)",
    figure=fig("좌표평면: 기울기 3인 직선이 x축과 A, y축과 B에서 만남, 점 (−3, 6) 표시, ∠BAO=a° 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "좌표평면 직선(각·좌표 표시)",
    note="tan a°=3 → sin·cos=3/10.")

# p68
add(id="9bcf7692", qtype="short",
    question="다음 그림과 같이 [[par(seg(AD), seg(BC))]]이고 [[seg(AB) = seg(DC) = 10]]인 등변사다리꼴 ABCD에서 [[seg(AD) = 8]], [[seg(BC) = 20]]일 때, [[tan(B)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(4,3)",
    figure=fig("등변사다리꼴 ABCD(윗변 AD=8, 아랫변 BC=20, 옆변 AB=DC=10 표시)"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "등변사다리꼴(치수 표시)",
    note="밑변 차 6, 높이 8 → tanB=4/3.")

# p69
add(id="e0463f85", qtype="choice",
    question=("다음 그림과 같이 [[ratio(seg(AB), seg(AD)) = ratio(2, 3)]]인 직사각형 ABCD에서 두 변 AB, CD의 중점을 각각 E, F라 하고 변 AD를 삼등분한 점 중 점 D에 가까운 점을 G라 하자. "
              "두 선분 AF, EG가 이루는 각을 [[angle(x)]]라 할 때, [[pow(sin(x), 2)]]의 값은?"),
    choices=["[[frac(1,4)]]", "[[frac(3,8)]]", "[[frac(1,2)]]", "[[frac(5,8)]]", "[[frac(3,4)]]"], derived_answer="③",
    figure=fig("직사각형 ABCD(A 왼쪽 위·B 왼쪽 아래·C 오른쪽 아래·D 오른쪽 위), AB·CD의 중점 E·F, AD의 삼등분점(D쪽) G, 선분 AF·EG의 교각 x, 등분 눈금 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "직사각형+내부 선분(등분·각 표시)",
    note="AB=2, AD=3: AF=(3,−1), EG=(2,1) → cos x=1/√2, sin²x=1/2 → ③.")

# p74
add(id="92800f6c", qtype="short",
    question="다음 그림과 같은 직각삼각형 ABC에서 점 D는 [[seg(BC)]]의 중점이다. [[angle(DAB) = x]]라 할 때, [[sin(x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(1,2)",
    figure=fig("직각삼각형 ABC(∠B=90°, A 왼쪽 아래·B 오른쪽 아래·C 오른쪽 위), BC의 중점 D(등호 표시), AC=5√7, AB=5√3, ∠DAB=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직각삼각형+중선(각·치수 표시)",
    note="BC=10, BD=5, AD=10 → sinx=1/2.")

# p75
add(id="d4d12594", qtype="short",
    question="다음 그림에서 [[seg(BD) = seg(DC) = 20]], [[angle(B) = angle(E) = deg(90)]]이고 [[sin(x) = frac(4,5)]]일 때, [[tan(y)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(12,41)",
    figure=fig("A 왼쪽 위, B 왼쪽 아래(직각), 직선 BC 위의 점 D(BD=DC=20), C 오른쪽; 선분 AD를 연장한 선 위의 점 E(∠E=90°, CE⊥AE), ∠BAD=x, ∠DAC=y, AC 연결"),
    difficulty_est=3, confidence=0.85, needs_review=FR + "삼각형 복합(각·치수·직각 표시)",
    note="AD=25, AB=15; △ABD∽△CED → DE=16, CE=12, AE=41 → tany=12/41. 빠른정답 12/11과 불일치(p76 동형 문항은 6/17로 일치).")

# p76
add(id="583a7b39", qtype="short",
    question="다음 그림에서 [[seg(BD) = seg(DC) = 15]], [[angle(B) = angle(E) = deg(90)]]이고 [[sin(x) = frac(3,5)]]일 때, [[tan(y)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(6,17)",
    figure=fig("A 왼쪽 위, B 왼쪽 아래(직각), 직선 BC 위의 점 D(BD=DC=15), C 오른쪽; 선분 AD를 연장한 선 위의 점 E(∠E=90°), ∠BAD=x, ∠DAC=y, AC 연결"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "삼각형 복합(각·치수·직각 표시)",
    note="AD=25, AB=20; DE=20, CE=12, AE=34 → tany=12/34=6/17.")

# p78
add(id="385c4532", qtype="choice",
    question="다음 그림과 같은 직사각형 모양의 종이 ABCD를 [[seg(PQ)]]를 접는 선으로 하여 접었더니 점 A와 점 C가 겹쳐졌다. [[angle(CPQ) = x]]라 할 때, [[tan(x)]]의 값은?",
    choices=["[[frac(1,7)]]", "[[frac(sqrt(7), 7)]]", "1", "[[sqrt(7)]]", "7"], derived_answer="④",
    figure=fig("직사각형 ABCD(AB=√7cm 세로, 윗변 AD 위의 점 P(AP=4cm), 아랫변 BC 위의 점 Q)를 PQ로 접어 A가 C에 겹친 그림(접힌 부분 색칠, 꼭짓점 R), ∠CPQ=x"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "종이 접기 도형(치수·각 표시)",
    note="PC=PA=4, PD=3, AD=7, AC=2√14, M=AC 중점: PM=√2, CM=√14 → tanx=√7 → ④.")

# p79
add(id="aa45ecdb", qtype="short",
    question="다음 그림의 직각삼각형 ABC에서 [[seg(BC)]]의 중점을 D라 하고 [[angle(ADB) = x]], [[angle(C) = y]]라 할 때, [[sin(x) × cos(y)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(2,3)",
    figure=fig("직각삼각형 ABC(∠B=90°, A 왼쪽 위·B 왼쪽 아래·C 오른쪽 아래), BC의 중점 D(등호 표시), AB=2√3, AC=6, ∠ADB=x, ∠C=y"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "직각삼각형+중선(각·치수 표시)",
    note="BC=2√6, BD=√6, AD=3√2 → sinx=√6/3, cosy=√6/3 → 2/3.")

# p80
add(id="38181e47", qtype="choice",
    question="다음 그림은 한 변의 길이가 2인 정육면체이다. [[angle(CEG) = x]]일 때, [[sin(x) + cos(x)]]의 값은?",
    choices=["[[frac(sqrt(3), 3)]]", "[[frac(2 sqrt(3), 3)]]", "[[frac(2, 3)]]", "[[frac(sqrt(3) + sqrt(6), 3)]]", "[[frac(sqrt(6) - sqrt(3), 3)]]"], derived_answer="④",
    figure=fig("정육면체 ABCD-EFGH(윗면 ABCD, 아랫면 EFGH), 대각선 CE·EG 표시, ∠CEG=x, ∠CGE 직각 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "정육면체 입체도형(각 표시)",
    note="EG=2√2, CG=2, CE=2√3 → √3/3+√6/3 → ④.")

# p81
add(id="75b97310", qtype="short",
    question="다음 그림과 같은 직육면체에서 [[angle(AGE)]]의 크기를 [[x]]라 할 때, [[sin(x) + cos(x) = sqrt(a)]]를 만족하는 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="2",
    figure=fig("직육면체 ABCD-EFGH, FG=3, GH=4, CG=5 표시, 대각선 AG·EG, ∠AGE=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직육면체 입체도형(치수·각 표시)",
    note="EG=5, AE=5 → x=45°, sin+cos=√2 → a=2.")

# p82
add(id="1ec257d6", qtype="choice",
    question="다음 그림과 같이 한 모서리의 길이가 10인 정육면체의 점 D에서 [[seg(BH)]]에 내린 수선의 발을 N이라 하고 [[angle(NDH) = x]]라 할 때, [[sin(x) × cos(x) × tan(x)]]의 값은?",
    choices=["[[frac(sqrt(6), 3)]]", "[[frac(sqrt(2), 2)]]", "[[frac(sqrt(3), 3)]]", "[[frac(1,2)]]", "[[frac(1,3)]]"], derived_answer="⑤",
    figure=fig("정육면체 ABCD-EFGH, 대각선 BH·BD·DH, D에서 BH에 내린 수선의 발 N, ∠NDH=x"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "정육면체 입체도형(각 표시)",
    note="x=∠DBH: sin=1/√3, cos=√2/√3, tan=1/√2 → 1/3 → ⑤.")

# p83
add(id="f7801b52", qtype="choice",
    question="다음 그림과 같은 정육면체에서 [[angle(ECG) = x]]일 때, [[sin(x)]]의 값은?",
    choices=["[[frac(sqrt(3), 3)]]", "[[frac(sqrt(6), 3)]]", "[[frac(sqrt(3), 2)]]", "[[frac(sqrt(5), 2)]]", "[[frac(sqrt(6), 2)]]"], derived_answer="②",
    figure=fig("정육면체 ABCD-EFGH, 대각선 CE·EG 표시, ∠ECG=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "정육면체 입체도형(각 표시)",
    note="EG=√2a, CE=√3a → sinx=√6/3 → ②.")

# p84
add(id="eafbc589", qtype="choice",
    question="다음 그림과 같은 직육면체에서 [[angle(AGE) = x]]라 할 때, [[cos(x)]]의 값은?",
    choices=["[[frac(sqrt(2), 3)]]", "[[frac(1,2)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(2), 2)]]", "[[frac(sqrt(3), 2)]]"], derived_answer="④",
    figure=fig("직육면체 ABCD-EFGH, FG=12cm, GH=5cm, DH=13cm 표시, 대각선 AG·EG, ∠AGE=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직육면체 입체도형(치수·각 표시)",
    note="EG=13=AE → cosx=√2/2 → ④. 빠른정답 3과 불일치.")

# p85
add(id="4c118027", qtype="choice",
    question="다음 그림과 같은 직육면체에서 [[angle(AGE) = x]]라 할 때, [[cos(x)]]의 값은?",
    choices=["[[frac(sqrt(2), 3)]]", "[[frac(1,2)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(2), 2)]]", "[[frac(sqrt(3), 2)]]"], derived_answer="④",
    figure=fig("직육면체 ABCD-EFGH, FG=15cm, GH=8cm, DH=17cm 표시, 대각선 AG·EG, ∠AGE=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "직육면체 입체도형(치수·각 표시)",
    note="EG=17=AE → cosx=√2/2 → ④. 빠른정답 5와 불일치.")

# p87
add(id="7919b2f6", qtype="choice",
    question="다음 그림과 같이 한 변의 길이가 6인 정육면체의 점 D에서 [[seg(BH)]]에 내린 수선의 발을 N이라 하고 [[angle(NDH) = x]]라 할 때, [[sin(x)]]의 값은?",
    choices=["[[frac(1,3)]]", "[[frac(1,2)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(2), 2)]]", "[[frac(sqrt(6), 3)]]"], derived_answer="③",
    figure=fig("정육면체 ABCD-EFGH(한 변 6 표시), 대각선 BH·BD·DH, D에서 BH에 내린 수선의 발 N, ∠NDH=x"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "정육면체 입체도형(치수·각 표시)",
    note="x=∠DBH, sin=DH/BH=1/√3=√3/3 → ③.")

# p88
add(id="68489606", qtype="choice",
    question="다음 그림과 같이 한 변의 길이가 4인 정육면체의 점 D에서 [[seg(BH)]]에 내린 수선의 발을 N이라 하고 [[angle(NDH) = x]]라 할 때, [[cos(x)]]의 값은?",
    choices=["[[frac(1,3)]]", "[[frac(sqrt(6), 6)]]", "[[frac(1,2)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(6), 3)]]"], derived_answer="⑤",
    figure=fig("정육면체 ABCD-EFGH(한 변 4 표시), 대각선 BH·BD·DH, D에서 BH에 내린 수선의 발 N, ∠NDH=x"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "정육면체 입체도형(치수·각 표시)",
    note="x=∠DBH, cos=BD/BH=√2/√3=√6/3 → ⑤.")

# p89
add(id="b2e12903", qtype="choice",
    question="다음 그림과 같이 한 모서리의 길이가 4인 정육면체에서 [[perp(seg(FI), seg(BH))]]이고, [[angle(HFI) = x]]라 할 때, [[sin(x) × cos(x)]]의 값은?",
    choices=["[[frac(1,3)]]", "[[frac(sqrt(2), 3)]]", "[[frac(sqrt(3), 3)]]", "[[frac(2,3)]]", "[[frac(sqrt(5), 3)]]"], derived_answer="②",
    figure=fig("정육면체 ABCD-EFGH(AD=4 표시), 대각선 BH·FH, F에서 BH에 내린 수선의 발 I, ∠HFI=x"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "정육면체 입체도형(치수·각 표시)",
    note="x=∠FBH: sin=√6/3, cos=√3/3 → √2/3 → ②. 빠른정답 3과 불일치.")

# p90
add(id="db761c2b", qtype="choice",
    question="다음 그림과 같이 한 모서리의 길이가 6인 정육면체에서 [[perp(seg(FI), seg(BH))]]이고, [[angle(HFI) = x]]라 할 때, [[sin(x) × tan(x)]]의 값은?",
    choices=["[[frac(sqrt(3), 6)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(3), 2)]]", "[[frac(2 sqrt(3), 3)]]", "[[frac(5 sqrt(3), 6)]]"], derived_answer="④",
    figure=fig("정육면체 ABCD-EFGH(AD=6 표시), 대각선 BH·FH, F에서 BH에 내린 수선의 발 I, ∠HFI=x"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "정육면체 입체도형(치수·각 표시)",
    note="x=∠FBH: sin=√6/3, tan=√2 → 2√3/3 → ④. 빠른정답 3과 불일치.")

# p93
add(id="895a6dbc", qtype="choice",
    question="아래 그림과 같이 반지름의 길이가 1인 원 위의 점 C에서 지름 AB에 내린 수선의 발을 D라 할 때, 다음 중 옳지 않은 것은?",
    choices=["[[seg(CD) = sin(deg(40))]]", "[[seg(BD) = 1 - cos(deg(40))]]", "[[seg(AC) = frac(sin(deg(20)), sin(deg(40)))]]",
             "[[tri(CAD) = frac(1,2) sin(deg(40)) × (1 + cos(deg(40)))]]", "[[tri(CAO) = frac(1,2) sin(deg(40))]]"],
    derived_answer="③",
    figure=fig("원(중심 O, 반지름 1), 지름 AB, 원 위의 점 C, C에서 AB에 내린 수선의 발 D(B 쪽), ∠CAB=20°, AO=1 표시, 선분 OC"),
    difficulty_est=3, confidence=0.85, needs_review=FR + "원+삼각형(각·치수 표시)",
    note="∠COB=40°; AC=2cos20°≠sin20°/sin40°=1/(2cos20°) → ③. 빠른정답 4와 불일치.")

# p94
add(id="32445ff6", qtype="short",
    question="다음 그림과 같은 원 O에서 [[seg(AB)]]는 지름이고 [[seg(OB) = sqrt(2)]], [[seg(BC) = 2]]이다. [[angle(CAO) = x]]라 할 때, [[tan(x)]]의 값을 구하시오.",
    choices=None, derived_answer="1",
    figure=fig("원(중심 O), 지름 AB, 원 위의 점 C, 삼각형 ABC, OB=√2, BC=2 표시, ∠CAO=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+삼각형(각·치수 표시)",
    note="AB=2√2, ∠C=90°, AC=2 → tanx=1.")

# p95
add(id="08a43bd4", qtype="short",
    question="다음 그림과 같은 점 O를 중심으로 하는 원에서 [[sin(x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(1,2)",
    figure=fig("원(중심 O), 지름 AB, 원 위의 점 C, AC=3√6, BC=3√2 표시, ∠CAB=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+삼각형(각·치수 표시)",
    note="AB=6√2 → sinx=BC/AB=1/2.")

# p96
add(id="866e3d91", qtype="short",
    question="다음 그림과 같이 점 O를 중심으로 하는 원에서 [[cos(x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(4,7)",
    figure=fig("원(중심 O), 지름 AB, 원 위의 점 C, AC=√33, BC=4 표시, ∠CBA=x"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+삼각형(각·치수 표시)",
    note="AB=7 → cosx=BC/AB=4/7. 빠른정답 1/7과 불일치.")

# p99
add(id="46c58842", qtype="short",
    question="다음 그림과 같이 반지름의 길이가 5 cm인 원 O에 내접하는 이등변삼각형 ABC에서 [[seg(AB) = seg(AC)]], [[seg(BC) = 8]] cm일 때, [[sin(angle(BAC))]]의 값을 구하시오. (단, [[deg(0) < angle(BAC) < deg(90)]])",
    choices=None, derived_answer="frac(4,5)",
    figure=fig("원(중심 O, 반지름 5cm 표시)에 내접하는 이등변삼각형 ABC(A 위, AB=AC 등호 표시), BC=8cm"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "원+내접 삼각형(치수 표시)",
    note="OM=3, AM=8, AB=4√5 → sinA=2·(1/√5)(2/√5)=4/5.")

# ───────────── 원의 현 ─────────────
# p6
add(id="78bc88a6", qtype="choice",
    question="다음 그림의 원 O에서 [[perp(seg(AB), seg(OH))]]이고 [[seg(AH) = 4]] cm, [[seg(OB) = 5]] cm일 때, [[tri(OHB)]]의 둘레의 길이는?",
    choices=["10 cm", "12 cm", "14 cm", "16 cm", "18 cm"], derived_answer="②",
    figure=fig("원(중심 O), 현 AB, O에서 AB에 내린 수선의 발 H, AH=4cm, OB=5cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+현·수선(치수 표시)",
    note="HB=4, OH=3 → 12 → ②. 빠른정답 10과 불일치.")

# p8
add(id="5ed19db9", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 [[seg(AB) = 18]], [[seg(BC) = 16]]인 직사각형이다. 두 변 BC, CD는 원과 두 점 P, Q에서 접하고 두 변 AB, AD는 각각 원과 두 점 E, F에서 만나며 꼭짓점 A는 원 위의 점이다. "
              "[[seg(EB) = 2]]일 때, [[seg(DF)]]의 길이를 구하시오."),
    choices=None, derived_answer="4",
    figure=fig("직사각형 ABCD(A 왼쪽 위·B 왼쪽 아래·C 오른쪽 아래·D 오른쪽 위) 안의 원: BC와 P, CD와 Q에서 접하고 AB와 E, AD와 F에서 만나며 A를 지남, EB=2 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "직사각형+원(접점·치수 표시)",
    note="반지름 r=10, 중심(6,10) → F=(12,18), DF=4.")

# p15
add(id="b46ae8d7", qtype="choice",
    question=("다음 보기 중 □ 안에 알맞은 말을 차례대로 구하면?\n"
              "원의 중심에서 현에 내린 □은 그 현을 이등분하고, 현의 수직이등분선은 그 원의 □을 지난다.\n"
              "<보기>\nㄱ. 지름\nㄴ. 반지름\nㄷ. 중심\nㄹ. 수선"),
    choices=["ㄱ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ", "ㄹ, ㄴ", "ㄹ, ㄷ"], derived_answer="⑤",
    figure=None, difficulty_est=1, confidence=0.9,
    note="수선·중심 → ㄹ, ㄷ → ⑤. 빠른정답 7과 불일치.")

# p18
add(id="a3b10f17", qtype="short",
    question="다음 그림에서 [[perp(seg(AB), seg(OM))]], [[seg(AB) = 10]] cm, [[seg(MC) = 3]] cm일 때, 원 O의 지름의 길이를 구하시오.",
    choices=None, derived_answer="frac(34,3) cm",
    figure=fig("원(중심 O), 현 AB, O에서 AB에 내린 수선의 발 M, OM의 연장이 원과 만나는 점 C, AB=10cm, MC=3cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+현·수선(치수 표시)",
    note="r²=25+(r−3)² → r=17/3, 지름 34/3 cm.")

# p19
add(id="da7e5d67", qtype="short",
    question="다음 그림과 같은 [[seg(AB) = seg(AC) = 4 sqrt(3)]], [[seg(BC) = 2 sqrt(39)]]인 이등변삼각형 ABC의 외접원의 반지름의 길이를 구하시오.",
    choices=None, derived_answer="8",
    figure=fig("원(중심 O)에 내접하는 이등변삼각형 ABC(A 아래, BC 위쪽 현), AB=AC 등호 표시, BC=2√39, AB=4√3 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "원+내접 삼각형(치수 표시)",
    note="BM=√39, AM=3 → R: (R−3)²+39=R² → R=8.")

# p22
add(id="2a1298a2", qtype="choice",
    question="다음 그림에서 원 O는 [[seg(AC) = 2 sqrt(14)]] cm, [[seg(AB) = seg(BC) = 3 sqrt(2)]] cm인 이등변삼각형 ABC의 외접원일 때, 원 O의 넓이는?",
    choices=["[[9 pi]] cm²", "[[frac(49,4) pi]] cm²", "[[16 pi]] cm²", "[[frac(81,4) pi]] cm²", "[[25 pi]] cm²"], derived_answer="④",
    figure=fig("원(중심 O, 색칠)에 내접하는 이등변삼각형 ABC(B 아래, AC 위쪽 현), AC=2√14cm, AB=BC=3√2cm 표시"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "원+내접 삼각형(치수 표시)",
    note="AM=√14, BM=2 → R=9/2 → 81π/4 → ④.")

# p23
add(id="aac78a03", qtype="choice",
    question="다음 그림과 같이 반지름의 길이가 25 cm인 원 O에서 [[perp(seg(AB), seg(OC))]]이고 [[seg(AB) = 40]] cm일 때, [[seg(BC)]]의 길이는?",
    choices=["[[10 sqrt(3)]] cm", "[[15 sqrt(2)]] cm", "[[10 sqrt(5)]] cm", "[[15 sqrt(3)]] cm", "[[20 sqrt(2)]] cm"], derived_answer="③",
    figure=fig("원(중심 O, 반지름 25cm), 세로 현 AB(40cm), O에서 AB에 수직인 반지름 OC(C는 원 위), 선분 BC"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+현·반지름(치수 표시)",
    note="OM=15, MC=10, BM=20 → BC=10√5 → ③.")

# p30
add(id="66b22712", qtype="short",
    question="다음 그림과 같이 반지름의 길이가 7 cm인 원에 내접하는 [[quad(ABCD)]]가 있다. 변 BC는 원의 중심 O를 지나고 [[seg(AD) = seg(CD) = 4]] cm이다. [[seg(AC)]]와 [[seg(OD)]]의 교점을 P라 할 때, [[seg(OP)]]의 길이를 구하시오.",
    choices=None, derived_answer="frac(41,7) cm",
    figure=fig("원(중심 O)에 내접하는 사각형 ABCD, BC는 지름, D는 A·C 사이 호 위, 선분 AC·OD의 교점 P"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "원+내접 사각형(교점 표시)",
    note="OD⊥AC, OP²−DP²=49−16=33, OP+DP=7 → OP=41/7 cm.")

# p32
add(id="22d56d22", qtype="short",
    question="다음 그림과 같이 반지름의 길이가 10 cm인 원에 내접하는 [[quad(ABCD)]]가 있다. 변 BC는 원의 중심 O를 지나고 [[seg(AD) = seg(CD) = 6]] cm이다. [[seg(AC)]]와 [[seg(OD)]]의 교점을 P라 할 때, [[seg(OP)]]의 길이를 구하시오.",
    choices=None, derived_answer="frac(41,5) cm",
    figure=fig("원(중심 O)에 내접하는 사각형 ABCD, BC는 지름, D는 A·C 사이 호 위, 선분 AC·OD의 교점 P"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "원+내접 사각형(교점 표시)",
    note="OP²−DP²=100−36=64, OP+DP=10 → OP=41/5 cm.")

# p33
add(id="6a9aafb2", qtype="choice",
    question="다음 그림의 원 O에서 [[seg(OA) = 15]] cm, [[seg(CM) = 6]] cm일 때, [[seg(AB)]]의 길이는?",
    choices=["16 cm", "18 cm", "20 cm", "22 cm", "24 cm"], derived_answer="⑤",
    figure=fig("원(중심 O), 현 AB, O에서 AB에 내린 수선의 발 M(직각 표시), OM의 연장이 원과 만나는 점 C, OA=15cm, CM=6cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+현·수선(치수 표시)",
    note="OM=9, AM=12 → AB=24 → ⑤.")

# p38
add(id="b8f06ca9", qtype="choice",
    question=("그림과 같이 구름다리의 두 지점을 각각 A, B라 하자. 이 구름다리를 따라 두 지점 A, B를 연결하면 반지름의 길이가 6 m인 원의 일부가 된다. "
              "선분 AB의 중점을 M, 점 M을 지나고 선분 AB에 수직인 직선이 호 AB와 만나는 점을 N이라 하자. [[seg(AB) = 8]] m일 때, [[seg(MN) = a]] m이다. [[a]]의 값은? (단, [[a < 6]])"),
    choices=["[[5 - 2 sqrt(5)]]", "[[6 - 2 sqrt(5)]]", "[[7 - 2 sqrt(5)]]", "[[5 - sqrt(5)]]", "[[6 - sqrt(5)]]"], derived_answer="②",
    figure=fig("구름다리(아치형 사다리) 삽화: 양 끝 A·B, AB의 중점 M, M에서 수직으로 호와 만나는 점 N(직각 표시), AB=8m 표시, 사람 그림"),
    difficulty_est=3, confidence=0.9, needs_review=FR + "구름다리 호+수선(치수·직각 표시)",
    note="출처 [2017년 3월 고1 14번/4점]. OM=√(36−16)=2√5, MN=6−2√5 → ②.")

# p39
add(id="6e5be96b", qtype="choice",
    question="다음 그림에서 [[arc(AB)]]는 원의 일부분이다. [[seg(AB) = 4 sqrt(5)]] cm, [[seg(CD) = 2]] cm, [[perp(seg(CD), seg(AB))]], [[seg(AD) = seg(BD)]]일 때, 이 원의 반지름의 길이는?",
    choices=["5 cm", "[[5 sqrt(5)]] cm", "6 cm", "[[6 sqrt(2)]] cm", "7 cm"], derived_answer="③",
    figure=fig("호 AB(원의 일부), 현 AB의 중점 D, D에서 호까지의 수선 CD=2cm(직각 표시), AB=4√5cm, AD=BD 등호 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "호+현·수선(치수 표시)",
    note="AD=2√5, r²=20+(r−2)² → r=6 → ③.")

# p43
add(id="2b6fe5d6", qtype="short",
    question="다음 그림에서 [[arc(AB)]]는 원의 일부분이다. [[seg(CD)]]가 [[seg(AB)]]를 수직이등분하고, [[seg(AD) = 8]] cm, [[seg(CD) = 5]] cm일 때, 이 원의 반지름의 길이를 구하시오.",
    choices=None, derived_answer="frac(89,10) cm",
    figure=fig("호 AB(활꼴, 색칠), 현 AB의 중점 D, CD⊥AB(C는 호 위), AD=8cm, CD=5cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "활꼴+수선(치수 표시)",
    note="r²=64+(r−5)² → r=89/10 cm.")

# p45
add(id="b6078937", qtype="choice",
    question="다음 그림에서 [[arc(AB)]]는 원의 일부이다. [[seg(AM) = seg(BM) = 4]] cm, [[seg(CM) = 3]] cm이고 [[perp(seg(AB), seg(CM))]]일 때, 이 원의 반지름의 길이는?",
    choices=["4 cm", "[[frac(25,6)]] cm", "[[frac(13,3)]] cm", "5 cm", "6 cm"], derived_answer="②",
    figure=fig("호 AB(아래로 볼록한 원의 일부), 현 AB의 중점 M, M에서 아래 호까지의 수선 CM=3cm(직각 표시), AM=BM=4cm"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "호+현·수선(치수 표시)",
    note="r²=16+(r−3)² → r=25/6 → ②.")

# p46
add(id="fb481a60", qtype="short",
    question="다음 그림은 원의 일부분이다. [[seg(AB) = 6 sqrt(3)]], [[seg(MH) = 3]]일 때, 이 원의 반지름의 길이를 구하시오.",
    choices=None, derived_answer="6",
    figure=fig("호 AB(원의 일부), 현 AB의 중점 H(등호 표시), H에서 호까지의 수선 MH=3(직각 표시), AB=6√3 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "호+현·수선(치수 표시)",
    note="AH=3√3, r²=27+(r−3)² → r=6.")

# p51
add(id="b1badd03", qtype="choice",
    question=("다음 그림과 같이 두 지점 A, B를 연결하면 반지름의 길이가 10인 원의 일부가 된다. 선분 AB의 중점을 M, 점 M을 지나고 선분 AB에 수직인 직선이 호 AB와 만나는 점을 N이라 하자. "
              "[[seg(MN) = 2]]일 때, [[seg(AB) = a]]이다. [[a]]의 값은?"),
    choices=["8", "10", "12", "14", "16"], derived_answer="③",
    figure=fig("호 AB(원의 일부), 현 AB의 중점 M(등호 표시), MN⊥AB(N은 호 위), MN=2 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "호+현·수선(치수 표시)",
    note="출처 [2017년 3월 고1 14번 변형]. OM=8, AM=6 → AB=12 → ③.")

# p57
add(id="a27e3f11", qtype="short",
    question="다음 그림과 같이 원 모양의 종이를 원 위의 한 점이 원의 중심 O와 겹치도록 [[seg(AB)]]를 접는 선으로 하여 접었을 때, [[seg(OM) = 2 sqrt(3)]]이었다. 이때 [[seg(AB)]]의 길이를 구하시오.",
    choices=None, derived_answer="12",
    figure=fig("원(중심 O)을 현 AB로 접어 호가 O를 지나는 그림(접힌 부분 색칠), O에서 AB에 내린 수선의 발 M(직각 표시), OM=2√3 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원 접기 도형(치수 표시)",
    note="r=2·OM=4√3, AM=6 → AB=12.")

# p59
add(id="739da6a9", qtype="short",
    question="다음 그림과 같이 호가 원의 중심을 지나도록 접었을 때, [[angle(AOB)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(120)",
    figure=fig("원(중심 O)을 현 AB로 접어 호가 O를 지나는 그림(접힌 호 점선), 점 O 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원 접기 도형",
    note="OM=r/2 → ∠AOB=120°.")

# p62
add(id="bd95efd7", qtype="short",
    question="다음 그림과 같이 반지름의 길이가 4인 원 O의 원주 위의 한 점이 원의 중심에 겹쳐지도록 접었을 때, [[angle(AOB)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(120)",
    figure=fig("원(중심 O, 반지름 4 표시)을 현 AB로 접어 호가 O를 지나는 그림(접힌 호 점선), ∠AOB 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원 접기 도형(치수 표시)",
    note="OM=2=r/2 → ∠AOB=120°.")

# p68
add(id="861f7ce2", qtype="short",
    question="다음 그림과 같이 원의 중심 O에서 [[seg(AB)]], [[seg(CD)]]에 내린 수선의 발을 각각 M, N이라 하자. [[seg(OA) = 5]], [[seg(OM) = seg(ON) = 4]]일 때, [[seg(AB) + seg(CD)]]의 길이를 구하시오.",
    choices=None, derived_answer="12",
    figure=fig("원(중심 O), 두 현 AB·CD, 수선의 발 M·N(직각 표시), OA=5, OM=4, ON=4 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+두 현·수선(치수 표시)",
    note="AM=3 → AB=CD=6 → 12. 빠른정답 60 cm와 불일치.")

# p69
add(id="f2a31061", qtype="short",
    question="다음 그림의 원 O에서 [[perp(seg(AB), seg(OM))]], [[perp(seg(CD), seg(ON))]]이고 [[seg(OM) = seg(ON)]]이다. [[seg(AM) = 9]] cm일 때, [[x + y]]의 값을 구하시오.",
    choices=None, derived_answer="27",
    figure=fig("원(중심 O), 두 현 AB·DC, 수선의 발 M·N(OM=ON 등호·직각 표시), AM=9cm, MB=x cm, DC=y cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+두 현·수선(치수 표시)",
    note="x=MB=9, y=DC=AB=18 → 27.")

# p71
add(id="8c008cef", qtype="short",
    question=("다음 그림과 같이 지름의 길이가 34 cm인 원 모양의 석쇠가 있다. 길이가 같은 두 굵은 철사 [[seg(AB)]], [[seg(CD)]]는 서로 평행하고 그 사이의 간격은 16 cm이다. "
              "이때 두 굵은 철사 [[seg(AB)]]와 [[seg(CD)]]의 길이의 합을 구하시오. (단, 철사의 굵기는 생각하지 않는다.)"),
    choices=None, derived_answer="60 cm",
    figure=fig("원 모양 석쇠 삽화(지름 34cm 표시), 평행한 두 굵은 철사 AB(위)·CD(아래), 간격 16cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "석쇠 원+평행 현(치수 표시)",
    note="r=17, 중심에서 8 떨어진 현 = 2·15=30 → 합 60 cm.")

# p75
add(id="2ae1da0b", qtype="choice",
    question="다음 그림의 원 O에서 [[perp(seg(AB), seg(OE))]]이고 [[seg(AB) = seg(CD)]]이다. [[seg(OE) = 5]] cm, [[seg(BE) = 6]] cm일 때, [[tri(OCD)]]의 넓이는?",
    choices=["24 cm²", "26 cm²", "28 cm²", "30 cm²", "32 cm²"], derived_answer="④",
    figure=fig("원(중심 O), 세로 현 AB와 수선의 발 E(직각 표시), 현 CD, 삼각형 OCD 색칠, OE=5cm, BE=6cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+두 현·삼각형(치수 표시)",
    note="AB=CD=12, O~CD 거리 5 → 30 → ④.")

# p78
add(id="66e747cf", qtype="choice",
    question="다음 그림과 같이 원 O에서 [[seg(OM) = seg(ON) = 3]]이고, [[seg(AO) = 5]]일 때, [[seg(CD)]]의 길이는?",
    choices=["5", "6", "7", "8", "9"], derived_answer="④",
    figure=fig("원(중심 O), 두 현 AB·DC, 수선의 발 M·N(직각 표시), OM=3, ON=3, AO=5 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+두 현·수선(치수 표시)",
    note="AM=4 → AB=CD=8 → ④. 빠른정답 18과 불일치.")

# p84
add(id="91398130", qtype="choice",
    question="다음 그림에서 [[tri(ABC)]]가 [[seg(AB) = seg(AC)]]인 이등변삼각형일 때, [[tri(ABO)]]의 넓이는?",
    choices=["3", "[[3 sqrt(2)]]", "6", "[[6 sqrt(2)]]", "12"], derived_answer="③",
    figure=fig("원(중심 O)에 내접하는 이등변삼각형 ABC(A 위), 삼각형 ABO 색칠, AB=6, AC=6 표시, O에서 AC에 내린 수선(직각 표시) 길이 2"),
    difficulty_est=3, confidence=0.85, needs_review=FR + "원+내접 삼각형(치수 표시)",
    note="AB=AC이므로 O에서 AB까지의 거리도 2 → ½·6·2=6 → ③. 빠른정답 18과 불일치.")

# p85
add(id="d1cb9b76", qtype="short",
    question="다음 그림에서 [[tri(ABC)]]는 [[seg(AB) = seg(BC)]]인 이등변삼각형이고 [[perp(seg(AB), seg(OD))]]이다. [[seg(AB) = 10]], [[seg(BC) = 10]], [[seg(OD) = 3]]일 때, [[tri(OBC)]]의 넓이를 구하시오.",
    choices=None, derived_answer="15",
    figure=fig("원(중심 O)에 내접하는 삼각형 ABC(A 왼쪽 위·C 오른쪽 위·B 아래), AB 위의 수선의 발 D(직각 표시), 삼각형 OBC 색칠, AB=10, BC=10, OD=3 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+내접 삼각형(치수 표시)",
    note="O~BC 거리=OD=3 → ½·10·3=15.")

# p86
add(id="8d63cd3c", qtype="choice",
    question="다음 그림과 같이 [[seg(AB) = seg(BC)]]인 이등변삼각형 ABC에서 [[seg(BC) = 10]] cm, [[seg(OM) = sqrt(5)]] cm일 때, [[tri(COB)]]의 넓이는?",
    choices=["5 cm²", "[[5 sqrt(3)]] cm²", "10 cm²", "[[5 sqrt(5)]] cm²", "[[5 sqrt(6)]] cm²"], derived_answer="④",
    figure=fig("원(중심 O)에 내접하는 삼각형 ABC(C 위, A 왼쪽·B 오른쪽 아래), AB 위의 수선의 발 M(직각 표시), 삼각형 COB 색칠, BC=10cm, OM=√5cm 표시"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+내접 삼각형(치수 표시)",
    note="O~BC 거리=√5 → ½·10·√5=5√5 → ④.")

# p88
add(id="df492dd8", qtype="short",
    question="다음 그림과 같이 원 O의 중심에서 두 현 AB, AC에 내린 수선의 발을 각각 M, N이라 하고 [[seg(OM) = seg(ON)]], [[angle(A) = deg(36)]]일 때, [[angle(AOC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(144)",
    figure=fig("원(중심 O)에 내접하는 삼각형 ABC(A 위), 수선의 발 M(AB 위)·N(AC 위), OM=ON 등호·직각 표시, ∠A=36°, 선분 OC"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+내접 삼각형(각 표시)",
    note="AB=AC, ∠OAC=18° → ∠AOC=144°.")

# p89
add(id="1e1f8d8b", qtype="short",
    question="다음 그림에서 [[seg(OM) = seg(ON)]]이고 [[angle(BAC) = deg(76)]]일 때, [[angle(ABC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(52)",
    figure=fig("원(중심 O)에 내접하는 삼각형 ABC(A 위), 수선의 발 M(AB 위)·N(AC 위), OM=ON 등호·직각 표시, ∠BAC=76°"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+내접 삼각형(각 표시)",
    note="AB=AC → ∠ABC=52°.")

# p90
add(id="1ead5564", qtype="choice",
    question="다음 그림과 같이 삼각형 [[tri(ABC)]]의 외접원의 중심 O에서 세 변에 내린 수선의 길이가 모두 같고 [[seg(AB) = 6 sqrt(3)]] cm일 때, 원 O의 넓이는?",
    choices=["[[12 pi]] cm²", "[[18 pi]] cm²", "[[24 pi]] cm²", "[[30 pi]] cm²", "[[36 pi]] cm²"], derived_answer="⑤",
    figure=fig("원(중심 O, 색칠)에 내접하는 삼각형 ABC(A 위), 세 변의 수선의 발 D(AB)·E(BC)·F(CA), OD=OE=OF 등호·직각 표시, AB=6√3cm"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+내접 삼각형(치수 표시)",
    note="정삼각형, R=6√3/√3=6 → 36π → ⑤.")

# p91
add(id="ddcc2e24", qtype="short",
    question="다음 그림과 같이 원 O의 중심에서 두 현 AB, AC에 내린 수선의 발을 각각 M, N이라 하고 [[seg(OM) = seg(ON)]], [[angle(BAC) = deg(70)]]일 때, [[angle(ABC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(55)",
    figure=fig("원(중심 O)에 내접하는 삼각형 ABC(A 위), 수선의 발 M(AB 위)·N(AC 위), OM=ON 등호·직각 표시, ∠BAC=70°"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+내접 삼각형(각 표시)",
    note="AB=AC → ∠ABC=55°.")

# p94
add(id="725f361c", qtype="choice",
    question=("다음 그림과 같이 원 O와 이 원에 내접하는 삼각형 ABC에서 점 O에서 삼각형의 세 선분 AB, BC, CA에 내린 수선을 발 각각 M, H, N이라 하고, "
              "[[seg(OM) = seg(ON)]], [[angle(HON) = deg(115)]]일 때, [[angle(A)]]의 크기는?"),
    choices=["[[deg(46)]]", "[[deg(47)]]", "[[deg(48)]]", "[[deg(49)]]", "[[deg(50)]]"], derived_answer="⑤",
    figure=fig("원(중심 O)에 내접하는 삼각형 ABC(A 위), 수선의 발 M(AB)·H(BC)·N(CA), 선분 OM·OH·ON"),
    difficulty_est=2, confidence=0.9, needs_review=FR + "원+내접 삼각형(수선 표시)",
    note="원문 '수선을 발' 그대로. ∠C=180°−115°=65°, AB=AC → ∠A=50° → ⑤.")
