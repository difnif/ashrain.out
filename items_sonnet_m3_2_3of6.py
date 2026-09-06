# -*- coding: utf-8 -*-
# esc_sonnet_m3-2_3of6 — 이미지 기준 전사 (82 항목 / 80쪽)
# 원의 현(p96·p99), 원의 접선(2)(내접원·외접사각형), 원의 접선(1)(접선과 반지름·접선의 성질), 원에 내접하는 사각형
# 전부 정보성 기하 도형(원+삼각형/사각형, 각·치수 표시) → unsupported + needs_review "도형 표현 불가"
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= 원의 현 =================
# p96 (원 O, ∠LOM=100°, OM=ON)
add(id="53ceb0e3", qtype="choice",
    question=("다음 그림과 같은 원 O에서 [[angle(LOM) = deg(100)]]이고 [[seg(OM) = seg(ON)]]일 때, [[angle(A)]]의 크기는?"),
    choices=["[[deg(10)]]", "[[deg(15)]]", "[[deg(20)]]", "[[deg(25)]]", "[[deg(30)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 삼각형 ABC(A 위, B 좌하, C 우하). O에서 AB·AC·BC에 내린 수선의 발 M·N·L(직각 표시), OM=ON(같은 길이 표시). ∠LOM=100°(호로 표시), ∠A 부분 음영"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접삼각형+수선 도형",
    note="□BMOL에서 ∠B=180°−100°=80°, OM=ON이면 AB=AC → ∠A=180°−2·80°=20° → ③ (빠른정답 없음, 풀이 답).")

# p99 (이미지에 별개 문항 2개 인쇄, id 1개 — draft_a 대응인 위쪽 문항(둘레) 전사)
add(id="35311c9f", qtype="short",
    question=("다음 그림의 원 O에서 [[perp(seg(AB), seg(OD))]], [[perp(seg(BC), seg(OE))]], [[perp(seg(CA), seg(OF))]]이고 "
              "[[seg(OD) = seg(OE) = seg(OF)]]이다. [[seg(AC) = 7]] cm일 때, [[tri(ABC)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="21 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 삼각형 ABC(A 좌상, B 좌하, C 우). O에서 AB·BC·CA에 내린 수선의 발 D·E·F(직각 표시), OD=OE=OF(같은 길이 표시). AC=7cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 원+내접삼각형+수선 도형 / 이미지 하단에 별개 문항(OM=ON, AB=12cm, ∠BAC=60°인 원 O에서 옳지 않은 것 고르기, 선지 ①AC=12cm ②AM=6cm ③∠OBM=30° ④OB=4√2cm ⑤△OMB=6√3cm²) 함께 인쇄됨(id 없음) — 위쪽 문항만 전사",
    note="OD=OE=OF → AB=BC=CA=7 → 둘레 21cm (빠른정답 없음, 풀이 답).")

# ================= 원의 접선(2) =================
# p1 (내접원, AB=11, AC=8, AE=3)
add(id="eb90d888", qtype="choice",
    question=("다음 그림과 같이 원 O가 [[tri(ABC)]]에 내접하고 세 점 D, E, F는 접점이다. [[seg(AB) = 11]] cm, [[seg(AC) = 8]] cm, "
              "[[seg(AE) = 3]] cm일 때, [[seg(BC)]]의 길이는?"),
    choices=["9 cm", "10 cm", "12 cm", "13 cm", "14 cm"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 좌하, C 우하)에 내접하는 원 O. 접점 F(AB 위)·E(AC 위)·D(BC 위). AB=11cm, AC=8cm, AE=3cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+내접원 도형",
    note="AF=AE=3 → BF=BD=8, CE=CD=5 → BC=13 → ④ = 빠른정답 ✓.")

# p9 (내접원, AB=6, AC=7, AD=2, BC=x)
add(id="4554a1ba", qtype="short",
    question=("다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이고 세 점 D, E, F는 접점일 때, [[x]]의 값을 구하시오."),
    choices=None, derived_answer="9",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 좌하, C 우하)에 내접하는 원 O. 접점 D(AB 위)·F(AC 위)·E(BC 위). AD=2, AB=6, AC=7(점선 치수), BC=x(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+내접원 도형",
    note="AD=AF=2 → BD=BE=4, CF=CE=5 → x=9. 빠른정답 '7 cm'와 불일치.")

# p15 (내접원, AB=8, AC=7, BC=9)
add(id="10790d5b", qtype="choice",
    question=("다음 그림과 같이 [[tri(ABC)]]의 내접원 O가 [[tri(ABC)]]의 각 변과 점 D, E, F에서 접할 때, "
              "[[seg(AF) + seg(BD) + seg(CE)]]는?"),
    choices=["10 cm", "11 cm", "12 cm", "13 cm", "14 cm"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 좌하, C 우하)에 내접하는 원 O. 접점 D(AB 위)·F(AC 위)·E(BC 위). AB=8cm, AC=7cm, BC=9cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+내접원 도형",
    note="AF+BD+CE = 둘레의 절반 = (8+7+9)/2 = 12 → ③. 빠른정답 '9 cm'와 불일치.")

# p28 (∠C=90° 직각삼각형 내접원, AB=13, BC=12)
add(id="e15eb0a4", qtype="short",
    question=("다음 그림에서 원 O는 [[angle(C) = deg(90)]]인 직각삼각형 ABC의 내접원이고 세 점 D, E, F는 접점이다. "
              "[[seg(AB) = 13]], [[seg(BC) = 12]]일 때, 내접원 O의 반지름의 길이를 구하시오."),
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(B 좌, C 우하 직각, A 우상)에 내접하는 원 O. 접점 D(AB 위)·E(BC 위)·F(AC 위). AB=13, BC=12(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형+내접원 도형",
    note="AC=5 → r=(5+12−13)/2=2. 빠른정답 3과 불일치.")

# p29 (∠A=90° 직각삼각형 내접원, BE=3, CE=10)
add(id="5972fa33", qtype="short",
    question=("다음 그림에서 원 O는 [[angle(A) = deg(90)]]인 직각삼각형 ABC의 내접원이고 점 D, E, F는 접점이다. "
              "[[seg(BE) = 3]] cm, [[seg(CE) = 10]] cm일 때, 원 O의 반지름의 길이를 구하시오."),
    choices=None, derived_answer="2 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위 직각, B 좌하, C 우하)에 내접하는 원 O. 접점 D(AB 위)·F(AC 위)·E(BC 위). BE=3cm, CE=10cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형+내접원 도형",
    note="AD=AF=r, (r+3)²+(r+10)²=13² → r²+13r−30=0 → r=2. 빠른정답 5와 불일치.")

# p33 (∠C=90° 직각삼각형 내접원, AB=13, BC=12, 둘레)
add(id="1e3e3c1a", qtype="choice",
    question=("다음 그림에서 원 O는 [[angle(C) = deg(90)]]인 직각삼각형 ABC의 내접원이다. [[seg(AB) = 13]] cm, [[seg(BC) = 12]] cm일 때, "
              "원 O의 둘레의 길이는?"),
    choices=["[[pi]] cm", "[[2 pi]] cm", "[[4 pi]] cm", "[[6 pi]] cm", "[[8 pi]] cm"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(B 좌, C 우하 직각, A 우상)에 내접하는 원 O. AB=13cm, BC=12cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형+내접원 도형",
    note="AC=5, r=(5+12−13)/2=2 → 둘레 4π → ③. 빠른정답 '4 cm'와 불일치.")

# p34 (직사각형 접기, △CDE 내접원)
add(id="2ea2295e", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = 5]] cm, [[seg(BC) = 13]] cm인 직사각형 ABCD를 꼭짓점 B가 [[seg(AD)]] 위의 점 E에 오도록 "
              "[[seg(FC)]]를 접는 선으로 하여 접었다. 원 O는 [[tri(CDE)]]의 내접원이고 세 점 G, H, I는 접점일 때, 원 O의 반지름의 길이는?"),
    choices=["[[frac(1,2)]] cm", "1 cm", "[[frac(3,2)]] cm", "2 cm", "[[frac(5,2)]] cm"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). AB 위의 점 F와 C를 잇는 접는 선 FC, B가 AD 위의 점 E로 접힘(삼각형 EFC 음영). 삼각형 CDE에 내접하는 원 O, 접점 G(DE 위)·I(CD 위)·H(CE 위). AB=5cm, BC=13cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형 접기+내접원 도형",
    note="CE=BC=13, CD=5 → DE=12 → r=(5+12−13)/2=2 → ④. 빠른정답 3과 불일치.")

# p40 (외접사각형 둘레, AP=9, BQ=6, CD=13)
add(id="df86a002", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 원 O에 외접하고 네 점 P, Q, R, S는 접점이다. [[seg(AP) = 9]] cm, [[seg(BQ) = 6]] cm, "
              "[[seg(CD) = 13]] cm일 때, [[quad(ABCD)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="56 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 외접하는 사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). 접점 P(AB 위)·Q(BC 위)·R(CD 위)·S(AD 위). AP=9cm, BQ=6cm, CD=13cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+외접사각형 도형",
    note="PB=BQ=6 → AB=15, 둘레=2(AB+CD)=2(15+13)=56cm. 빠른정답 '7 cm'와 불일치.")

# p44 (등변사다리꼴 외접, AD=8√2, BC=24√2, 내접원 넓이)
add(id="1180e1c2", qtype="choice",
    question=("다음 그림과 같이 원 O에 외접하는 등변사다리꼴 ABCD가 있다. [[seg(AD) = 8 sqrt(2)]] cm, [[seg(BC) = 24 sqrt(2)]] cm일 때, "
              "내접원 O의 넓이는?"),
    choices=["[[69 pi]] cm²", "[[69 sqrt(2) pi]] cm²", "[[96 pi]] cm²", "[[96 sqrt(2) pi]] cm²", "[[96 sqrt(6) pi]] cm²"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "등변사다리꼴 ABCD(A 좌상, D 우상, B 좌하, C 우하)에 내접하는 원 O(음영). AD=8√2cm(위 점선 치수), BC=24√2cm(아래 점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 등변사다리꼴+내접원 도형",
    note="AB+CD=AD+BC → AB=16√2, 높이²=(16√2)²−(8√2)²=384 → h=8√6, r=4√6 → 넓이 96π → ③. 빠른정답 2와 불일치.")

# p45 (등변사다리꼴 외접, AD=18, BC=32, 반지름)
add(id="2c5c310a", qtype="choice",
    question=("다음 그림과 같이 원 O에 외접하는 등변사다리꼴 ABCD에서 [[seg(AD) = 18]] cm, [[seg(BC) = 32]] cm일 때, 원 O의 반지름의 길이는?"),
    choices=["12 cm", "13 cm", "14 cm", "15 cm", "18 cm"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "등변사다리꼴 ABCD(A 좌상, D 우상, B 좌하, C 우하)에 내접하는 원 O. O에서 AD에 이르는 반지름 x(점선). AD=18cm, BC=32cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 등변사다리꼴+내접원 도형",
    note="AB=CD=25, 높이²=25²−7²=576 → h=24 → r=12 → ①. 빠른정답 '4 m'와 불일치.")

# p49 (외접사각형, AB=6, AD=3, DC=4, BC=x)
add(id="dd5b324b", qtype="choice",
    question=("다음 그림과 같이 원 O는 사각형 ABCD의 내접원이다. [[seg(AB) = 6]] cm, [[seg(AD) = 3]] cm, [[seg(DC) = 4]] cm일 때, [[x]]의 값은?"),
    choices=["6", "7", "8", "9", "10"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 외접하는 사각형 ABCD(A 위, D 우상, B 좌하, C 우하). AB=6cm, AD=3cm, DC=4cm, BC=x cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+외접사각형 도형",
    note="AB+DC=AD+BC → 10=3+x → x=7 → ②. 빠른정답 '6 cm'와 불일치.")

# p55 (∠A=∠B=90° 사각형 내접원, AD=20, BC=30)
add(id="81fc402b", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = angle(B) = deg(90)]]인 사각형 ABCD에 원 O가 내접한다. [[seg(AD) = 20]] cm, [[seg(BC) = 30]] cm일 때, "
              "원 O의 반지름의 길이를 구하시오."),
    choices=None, derived_answer="12 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌상, B 좌하 — 둘 다 직각 표시, D 우상, C 우하)에 내접하는 원 O. AD=20cm(위 점선 치수), BC=30cm(아래 점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+내접원 도형",
    note="AB=2r, CD=50−2r, CD²=(2r)²+10² → r=12cm. 빠른정답 4와 불일치.")

# p56 (외접사각형, AD=14, BD=17, CD=15, ∠C=90°)
add(id="02dbeaa3", qtype="short",
    question=("다음 그림과 같이 [[quad(ABCD)]]가 원에 외접하고 있다. [[seg(AD) = 14]] cm, [[seg(BD) = 17]] cm, [[seg(CD) = 15]] cm, "
              "[[angle(C) = deg(90)]]일 때, [[seg(AB)]]의 길이를 구하시오."),
    choices=None, derived_answer="7 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 외접하는 사각형 ABCD(A 좌, B 좌하, C 우하 직각 표시, D 우상). 대각선 BD. AD=14cm, BD=17cm, CD=15cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+외접사각형+대각선 도형",
    note="BC=√(17²−15²)=8, AB+CD=AD+BC → AB=14+8−15=7cm. 빠른정답 '2 cm'와 불일치.")

# p57 (∠C=∠D=90° 외접사각형, AB=15, CD=12, BC=18, DE)
add(id="1a099b6a", qtype="short",
    question=("다음 그림에서 원 O가 사각형 ABCD에 내접하고 네 점 E, F, G, H는 접점이다. [[angle(C) = angle(D) = deg(90)]]일 때, "
              "[[seg(DE)]]의 길이를 구하시오."),
    choices=None, derived_answer="6 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌상, D 우상 직각, B 좌하, C 우하 직각)에 내접하는 원 O. 접점 E(AD 위)·F(AB 위)·G(BC 위)·H(CD 위). AB=15cm, CD=12cm, BC=18cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+내접원 도형",
    note="CD=12=2r → r=6, DE=DH=6cm = 빠른정답 ✓.")

# p58 (외접사각형, ∠B=90°, AD=10, AC=20, BC=16)
add(id="b3df3144", qtype="choice",
    question=("다음 그림과 같이 [[quad(ABCD)]]는 원 O에 외접한다. [[angle(B) = deg(90)]]이고 [[seg(AD) = 10]] cm, [[seg(AC) = 20]] cm, "
              "[[seg(BC) = 16]] cm일 때, [[seg(CD)]]의 길이는?"),
    choices=["10 cm", "12 cm", "14 cm", "16 cm", "18 cm"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 외접하는 사각형 ABCD(A 좌상, D 우상, B 좌하 직각 표시, C 우하). 대각선 AC. AD=10cm, AC=20cm, BC=16cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+외접사각형+대각선 도형",
    note="AB=√(20²−16²)=12, AB+CD=AD+BC → CD=26−12=14 → ③. 빠른정답 4와 불일치.")

# p60 (∠A=∠B=90° 사다리꼴 외접, AB=6, BC=12, 둘레)
add(id="2a43d3b4", qtype="choice",
    question=("다음 그림과 같이 [[angle(A) = angle(B) = deg(90)]]인 사다리꼴 ABCD가 원 O에 외접한다. [[seg(AB) = 6]] cm, [[seg(BC) = 12]] cm일 때, "
              "[[quad(ABCD)]]의 둘레의 길이는?"),
    choices=["28 cm", "32 cm", "36 cm", "40 cm", "44 cm"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 좌상, B 좌하 — 둘 다 직각 표시, D 위, C 우하)에 내접하는 원 O. AB=6cm(좌 점선 치수), BC=12cm(아래 점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사다리꼴+내접원 도형",
    note="AD=x, CD=x+6, (x+6)²=(12−x)²+36 → x=4, CD=10 → 둘레 32 → ②. 빠른정답 '6 cm'와 불일치.")

# p61 (외접사각형, ∠A=∠B=90°, AD=6, AB=8, DC=10, CQ)
add(id="3a1fe684", qtype="choice",
    question=("다음 그림에서 [[quad(ABCD)]]가 원 O에 외접하고 네 점 P, Q, R, S는 각각 원 O의 접점일 때, [[seg(CQ)]]의 길이는?"),
    choices=["5 cm", "6 cm", "7 cm", "8 cm", "9 cm"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 외접하는 사각형 ABCD(A 좌상, B 좌하 — 둘 다 직각 표시, D 우상, C 우하, 음영). 접점 S(AD 위)·P(AB 위)·Q(BC 위)·R(CD 위). AD=6cm, AB=8cm, DC=10cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+외접사각형 도형",
    note="r=4 → AS=4, DS=DR=2, CR=CQ=8 → ④ = 빠른정답 ✓.")

# p62 (∠A=∠B=90° 사각형 내접원, AD=10, BC=15)
add(id="c7ed1fc7", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = angle(B) = deg(90)]]인 사각형 ABCD에 원 O가 내접한다. [[seg(AD) = 10]] cm, [[seg(BC) = 15]] cm일 때, "
              "원 O의 반지름의 길이를 구하시오."),
    choices=None, derived_answer="6 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌상, B 좌하 — 둘 다 직각 표시, D 우상, C 우하)에 내접하는 원 O. AD=10cm(위 점선 치수), BC=15cm(아래 점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+내접원 도형",
    note="AB=2r, CD=25−2r, CD²=4r²+5² → r=6cm. 빠른정답 '11 cm'와 불일치.")

# p64 (∠A=∠B=90° 사다리꼴, 반지름 3, CD=11, 넓이)
add(id="fbbdd05f", qtype="short",
    question=("다음 그림에서 [[angle(A) = angle(B) = deg(90)]]인 사다리꼴 ABCD가 반지름의 길이가 3 cm인 원 O에 외접한다. "
              "[[seg(CD) = 11]] cm일 때, [[quad(ABCD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="51 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 좌상, B 좌하 — 둘 다 직각 표시, D 위, C 우하, 음영)에 내접하는 원 O. CD=11cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사다리꼴+내접원 도형",
    note="AB=6, AD+BC=AB+CD=17 → 넓이 (1/2)·17·6=51cm² (빠른정답 없음, 풀이 답).")

# p65 (∠DAB=∠ABC=90°, AD=8, BC=12, 반지름)
add(id="77748028", qtype="choice",
    question=("다음 그림과 같이 원 O는 [[quad(ABCD)]]의 각 변과 접한다. [[angle(DAB) = angle(ABC) = deg(90)]]이고, [[seg(AD) = 8]] cm, "
              "[[seg(BC) = 12]] cm일 때, 원 O의 반지름의 길이는?"),
    choices=["[[frac(16,5)]] cm", "4 cm", "[[frac(24,5)]] cm", "[[2 sqrt(5)]] cm", "[[2 sqrt(6)]] cm"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌상, B 좌하 — 둘 다 직각 표시, D 우상, C 우하)에 내접하는 원 O. AD=8cm(위 점선 치수), BC=12cm(아래 점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+내접원 도형",
    note="AB=2r, CD=20−2r, CD²=4r²+4² → 400−80r=16 → r=24/5 → ③ = 빠른정답 ✓.")

# p70 (직사각형+원, r=2, AE=3, BC)
add(id="99aa2c28", qtype="short",
    question=("다음 그림과 같이 원 O는 직사각형 ABCD와 세 점 P, Q, R에서 접하고 [[seg(EC)]]와 점 S에서 접한다. "
              "원 O의 반지름의 길이는 2 cm이고, [[seg(AE) = 3]] cm일 때, [[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="6 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). 원 O가 AD·AB·BC와 각각 P·Q·R에서 접하고, AD 위의 점 E와 C를 잇는 선분 EC와 S에서 접함. AE=3cm(점선 치수), OQ=2cm(반지름)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형+원+접선 도형",
    note="AB=4, PE=ES=1, RC=SC=x−2, EC=x−1, (x−1)²=(x−3)²+4² → x=6cm = 빠른정답 ✓.")

# p73 (직사각형+원, r=10, AE=15, BC)
add(id="f30ddf91", qtype="short",
    question=("다음 그림과 같이 원 O는 직사각형 ABCD와 세 점 P, Q, R에서 접하고 [[seg(EC)]]와 점 S에서 접한다. "
              "원 O의 반지름의 길이는 10 cm이고 [[seg(AE) = 15]] cm일 때, [[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="30 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). 원 O가 AD·AB·BC와 각각 P·Q·R에서 접하고, AD 위의 점 E와 C를 잇는 선분 EC와 S에서 접함. AE=15cm(점선 치수), OQ=10cm(반지름)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형+원+접선 도형",
    note="AB=20, PE=ES=5, RC=SC=x−10, EC=x−5, (x−5)²=(x−15)²+20² → x=30cm = 빠른정답 ✓.")

# p76 (직사각형 세 변에 접하는 원, CF 접선, CF=b/a)
add(id="f5b790e7", qtype="short",
    question=("다음 그림과 같이 직사각형 ABCD의 세 변에 접하는 원 O가 있다. [[seg(CF)]]가 원 O의 접선일 때, [[seg(CF) = frac(b,a)]]라 할 때, "
              "[[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 서로소)"),
    choices=None, derived_answer="29",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). 원 O가 AD·AB·BC에 각각 E·(AB 중점)·H에서 접함. AD 위의 점 F에서 C로 그은 접선 CF. AE=4, AB=8, BC=10(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형+원+접선 도형",
    note="r=4, CH=6, EF=t → (t+6)²=(6−t)²+8² → t=8/3, CF=26/3 → a+b=29 = 빠른정답 ✓.")

# p80 (직사각형 둘레 34, 두 내접원 O·O′, □GOHO′ 넓이)
add(id="433c3ae8", qtype="choice",
    question=("다음 그림과 같은 직사각형 ABCD의 둘레의 길이는 34 cm이고 두 원 O, O′은 각각 [[tri(ABC)]], [[tri(ACD)]]의 내접원이다. "
              "두 원의 반지름의 길이가 2 cm로 같고 점 G, H는 각각 두 원 O, O′과 [[seg(AC)]]의 접점일 때, □GOHO′의 넓이는?"),
    choices=["11 cm²", "12 cm²", "13 cm²", "14 cm²", "15 cm²"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "가로로 긴 직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상)와 대각선 AC. 삼각형 ABC의 내접원 O(왼쪽 아래)·삼각형 ACD의 내접원 O′(오른쪽 위). AC와의 접점 G(O 쪽)·H(O′ 쪽). 사각형 GOHO′ 음영"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 직사각형+대각선+내접원 2개 도형 / 프라임 점 라벨(O′)",
    note="a+b=17, r=2 → AC=13, AB·BC=5·12. AG=3, CH=3 → GH=7, 평행사변형 넓이 7·2=14 → ④ = 빠른정답 ✓.")

# ================= 원의 접선(1) =================
# p3 (PO=7, PT=5, 원의 넓이)
add(id="76334b87", qtype="choice",
    question=("다음 그림과 같이 원 O 밖의 한 점 P에서 이 원에 그은 접선의 접점을 T라 하자. [[seg(PO) = 7]] cm, [[seg(PT) = 5]] cm일 때, 원 O의 넓이는?"),
    choices=["[[20 pi]] cm²", "[[21 pi]] cm²", "[[22 pi]] cm²", "[[23 pi]] cm²", "[[24 pi]] cm²"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). PO=7cm(점선 치수), 접선 PT(접점 T 아래쪽), PT=5cm(점선 치수)"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 원+접선 도형",
    note="r²=7²−5²=24 → 넓이 24π → ⑤ = 빠른정답 ✓.")

# p4 (∠AOP=40°, ∠x)
add(id="29fcb4ac", qtype="short",
    question=("다음 그림에서 [[seg(PA)]]는 원 O의 접선이고 점 A는 그 접점일 때, [[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(50)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O)와 원 밖의 점 P(우측). 접선 PA(접점 A 아래쪽), 선분 OA·OP. ∠AOP=40°, ∠OPA=x"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 원+접선 도형",
    note="∠OAP=90° → x=180°−90°−40°=50°. 빠른정답 65와 불일치.")

# p5 (지름 8√3, ∠PBT=30°, PT)
add(id="b8bdc826", qtype="short",
    question=("다음 그림과 같이 점 P에서 지름의 길이가 [[8 sqrt(3)]] cm인 원 O에 그은 접선의 접점을 T라 하고 점 P와 원 O의 중심을 지나는 직선이 "
              "원과 만나는 두 점을 각각 A, B라 하자. [[angle(PBT) = deg(30)]]일 때, [[seg(PT)]]의 길이를 구하시오."),
    choices=None, derived_answer="12 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O와 원 밖의 점 P(좌하). 직선 PB가 원과 A·B에서 만남(A 가까운 쪽, B 우상). 접선 PT(접점 T 아래). 지름 AB=8√3cm(점선 치수), ∠PBT=30°"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+접선+지름 도형",
    note="OB=OT → ∠OTB=30°, ∠TOP=60°, PT=OT·tan60°=4√3·√3=12cm. 빠른정답 50과 불일치.")

# p7 (반지름 10, PO=17, △POT 넓이)
add(id="29ea2a99", qtype="choice",
    question=("다음은 반지름이 10 cm인 원 O와 [[seg(PT)]]가 원 O에 접하고 [[seg(PO)]]의 길이가 17 cm인 삼각형 POT를 그린 것이다. "
              "삼각형 POT의 넓이는?"),
    choices=["[[10 sqrt(21)]] cm²", "[[11 sqrt(21)]] cm²", "[[12 sqrt(21)]] cm²", "[[13 sqrt(21)]] cm²", "[[15 sqrt(21)]] cm²"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O), 접점 T(원 아래쪽), 원 밖의 점 P(우하). 삼각형 POT 음영. OT=10cm, PO=17cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 원+접선 삼각형 도형",
    note="PT=√(17²−10²)=√189=3√21 → 넓이 (1/2)·10·3√21=15√21 → ⑤ = 빠른정답 ✓.")

# p8 (세 원 반지름 3, EF=x, √(ax) 자연수)
add(id="beaf6939", qtype="short",
    question=("다음 그림에서 세 원 O, P, Q의 반지름의 길이는 모두 3이고 두 원 O, P는 한 점 B에서 만나고 두 원 P, Q는 한 점 C에서 만난다. "
              "반직선 AG는 점 G에서 접하는 원 Q의 접선이고 이 접선이 원 P와 만나는 두 점을 각각 E, F라 하자. [[seg(EF) = x]]일 때, "
              "[[sqrt(a x)]]가 자연수가 되도록 하는 자연수 [[a]]의 값 중 가장 작은 수를 구하시오.\n"
              "(단, 점 A, O, B, P, C, Q, D는 한 직선 위의 점이다.)"),
    choices=None, derived_answer="30",
    figure=[{"fn": "unsupported", "args": {"raw": "한 직선 위에 A, O, B, P, C, Q, D 순으로 놓인 세 원 O·P·Q(반지름 3, 서로 외접). A는 원 O의 왼쪽 끝점. A에서 그은 반직선 AG가 원 P와 E·F에서 만나고 원 Q에 G에서 접함. AO=3, EF=x(점선 치수)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 세 원+접선 도형",
    note="AQ=15, QG=3 → sinθ=1/5, P와 AG의 거리 9/5 → EF=2√(9−81/25)=24/5 → √(24a/5) 자연수 최소 a=30 = 빠른정답 ✓.")

# p10 (PT=4, BP=2, 반지름)
add(id="528beaa8", qtype="short",
    question=("다음 그림에서 [[seg(PT)]]는 원 O의 접선이고 점 T는 접점이다. [[seg(PT) = 4]] cm, [[seg(BP) = 2]] cm일 때, 원 O의 반지름의 길이를 구하시오."),
    choices=None, derived_answer="3 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O, 지름 AB(A 좌, B 우)의 연장선 위 점 P(우측). 접선 PT(접점 T 우상), 선분 OT. PT=4cm, BP=2cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 원+접선+지름 도형",
    note="r²+4²=(r+2)² → r=3cm = 빠른정답 ✓.")

# p13 (세 원 반지름 5, EF=x, √(ax) 자연수)
add(id="e2b4ee2e", qtype="short",
    question=("다음 그림에서 세 원 O, P, Q의 반지름의 길이는 모두 5이고 두 원 O, P는 한 점 B에서 만나고 두 원 P, Q는 한 점 C에서 만난다. "
              "직선 AG는 점 G에서 접하는 원 Q의 접선이고 이 접선이 원 P와 만나는 두 점을 각각 E, F라 하자. [[seg(EF) = x]]일 때, "
              "[[sqrt(a x)]]가 자연수가 되도록 하는 자연수 [[a]]의 값 중 가장 작은 수를 구하시오.\n"
              "(단, 점 A, O, B, P, C, Q, D는 한 직선 위의 점이다.)"),
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": "한 직선 위에 A, O, B, P, C, Q, D 순으로 놓인 세 원 O·P·Q(반지름 5, 서로 외접). A는 원 O의 왼쪽 끝점. A에서 그은 직선 AG가 원 P와 E·F에서 만나고 원 Q에 G에서 접함. AO=5, EF=x(점선 치수)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 세 원+접선 도형",
    note="AQ=25, QG=5 → sinθ=1/5, P와 AG의 거리 3 → EF=2·4=8 → √(8a) 자연수 최소 a=2. 빠른정답 '3 cm'와 불일치.")

# p14 (∠POT=55°, ∠OPT)
add(id="2a3a79c5", qtype="short",
    question=("다음 그림의 원 O에서 [[seg(PT)]]는 원 O의 접선이고 점 T는 그 접점이다. [[angle(POT) = deg(55)]]일 때, [[angle(OPT)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(35)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). 접선 PT(접점 T 아래), 선분 OT·OP. ∠POT=55°"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 원+접선 도형",
    note="∠OTP=90° → ∠OPT=35°. 빠른정답 2와 불일치.")

# p17 (두 원 공통접선, ∠PAQ=48°, ∠QBO′)
add(id="5f6aa547", qtype="short",
    question=("다음 그림에서 [[seg(AB)]], [[seg(PQ)]]는 두 원 O, O′의 공통인 접선이고, 세 점 A, B, Q는 접점이다. [[angle(PAQ) = deg(48)]]일 때, "
              "∠QBO′의 크기를 구하시오."),
    choices=None, derived_answer="deg(48)",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽 원 O(작은 원)와 오른쪽 원 O′(큰 원)이 점 Q에서 외접. 위쪽 공통접선 AB(A는 원 O의 접점, B는 원 O′의 접점), Q에서의 공통접선 PQ(P는 AB 위). 선분 AQ·BQ·BO′. ∠PAQ=48°"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 두 원+공통접선 도형 / 프라임 점 라벨(O′)",
    note="PA=PQ=PB → ∠PQA=48°, ∠AQB=90°, ∠PBQ=42° → ∠QBO′=90°−42°=48° = 빠른정답 ✓.")

# p18 (∠APB=72°, x)
add(id="36d1d433", qtype="short",
    question=("다음 그림에서 두 점 A, B는 점 P에서 원 O에 그은 두 접선의 접점이다. [[angle(APB) = deg(72)]]일 때, [[x]]의 값을 구하시오."),
    choices=None, derived_answer="54",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). 접선 PA(접점 A 위)·PB(접점 B 아래), 현 AB. ∠APB=72°, ∠PAB=x°"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="PA=PB → x=(180−72)/2=54. 빠른정답 18과 불일치.")

# p20 (∠PBA=72°, ∠x)
add(id="dfc04dd6", qtype="short",
    question=("다음 그림에서 [[seg(PA)]], [[seg(PB)]]는 원 O의 접선이고 두 점 A, B는 각각 그 접점일 때, [[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(36)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 좌측)와 원 밖의 점 P(우측). 접선 PA(접점 A 위)·PB(접점 B 아래), 현 AB. ∠PBA=72°, ∠APB=x"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="PA=PB → ∠PAB=72° → x=180°−144°=36°. 빠른정답 48과 불일치.")

# p22 (두 원 공통접선 PQ·TR, ∠RPT=39°, ∠TQR)
add(id="bbf17cd4", qtype="choice",
    question=("다음 그림에서 [[seg(PQ)]]와 [[seg(TR)]]는 두 원 O, O′의 공통인 접선이고 세 점 P, Q, R는 접점이다. [[angle(RPT) = deg(39)]]일 때, "
              "[[angle(TQR)]]의 크기는?"),
    choices=["[[deg(42)]]", "[[deg(45)]]", "[[deg(48)]]", "[[deg(51)]]", "[[deg(54)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽 큰 원 O와 오른쪽 작은 원 O′이 점 R에서 외접. 아래쪽 공통접선 PQ(P는 원 O의 접점, Q는 원 O′의 접점), R에서의 공통접선 TR(T는 PQ 위). 선분 PR·QR. ∠RPT=39°, ∠TQR 부분 음영"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 두 원+공통접선 도형 / 프라임 점 라벨(O′)",
    note="TP=TR=TQ → ∠TRP=39°, ∠PRQ=90°, ∠TRQ=51°=∠TQR → ④. 빠른정답 50과 불일치.")

# p24 (두 원이 직선 PT에 T에서 접, AB 공통접선, 옳지 않은 것)
add(id="354ac045", qtype="choice",
    question=("다음 그림과 같이 두 원 O, O′이 직선 PT와 점 T에서 각각 접하고 직선 AB가 두 원 O, O′의 공통인 접선일 때, 다음 중 옳지 않은 것은?"),
    choices=["[[seg(PA) = seg(PT)]]", "[[seg(PA) = frac(1,2) seg(AB)]]", "[[angle(PTB) = angle(PBT)]]", "[[angle(PAT) = deg(60)]]", "[[angle(ATB) = deg(90)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽 원 O와 오른쪽 원 O′이 점 T에서 외접, T에서의 공통접선(세로 직선 PT). 위쪽 공통접선 AB(A는 원 O의 접점, B는 원 O′의 접점, P는 AB 위). 선분 AT·BT"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 두 원+공통접선 도형 / 프라임 점 라벨(O′)",
    note="PA=PT=PB → ①②③⑤ 성립, ∠PAT=60°는 일반적으로 성립하지 않음 → ④. 빠른정답 5와 불일치.")

# p26 (호 AC:BC=3:2, ∠ODB)
add(id="1dcd4cbc", qtype="short",
    question=("다음 그림과 같이 원 밖의 점 P에서 원 O에 그은 두 접선의 접점을 A, B라 하면 [[arc(AB)]] 위의 점 C에 대하여 "
              "[[ratio(arc(AC), arc(BC)) = ratio(3, 2)]]이다. [[seg(OC)]]의 연장선과 [[seg(PB)]]의 교점을 D라 할 때, [[angle(ODB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(42)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O와 원 밖의 점 P(좌하). 접선 PA(접점 A 좌상)·PB(접점 B 아래). 호 AB 위의 점 C, OC의 연장선이 PB와 D에서 만남. ∠APB=60°"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선+호 도형",
    note="∠APB=60°(그림) → ∠AOB=120°, ∠BOC=120°·2/5=48° → ∠ODB=90°−48°=42°. 빠른정답 30과 불일치.")

# p31 (∠APB=60°, PA=3, OH)
add(id="fb0db384", qtype="choice",
    question=("다음 그림에서 [[seg(AP)]], [[seg(BP)]]는 원 O의 접선이고 두 점 A, B는 접점이다. [[angle(APB) = deg(60)]], [[seg(PA) = 3]]이고 "
              "점 O에서 [[seg(AB)]]에 내린 수선의 발을 H라 할 때, [[seg(OH)]]의 길이는?"),
    choices=["[[frac(sqrt(2), 4)]]", "[[frac(sqrt(3), 4)]]", "[[frac(sqrt(2), 2)]]", "[[frac(sqrt(3), 2)]]", "[[frac(sqrt(6), 2)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O)와 원 밖의 점 P(우하). 접선 PA(접점 A 우상)·PB(접점 B 아래), 현 AB, O에서 AB에 내린 수선의 발 H(직각 표시). PA=3(점선 치수), ∠APB=60°"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선+수선 도형",
    note="△PAB 정삼각형, AH=3/2, ∠OAH=30° → OH=(3/2)tan30°=√3/2 → ④ = 빠른정답 ✓.")

# p32 (∠APB=60°, PA=18, OH)
add(id="773a275b", qtype="choice",
    question=("다음 그림에서 [[seg(AP)]], [[seg(BP)]]는 원 O의 접선이고 두 점 A, B는 접점이다. [[angle(APB) = deg(60)]], [[seg(PA) = 18]]이고 "
              "점 O에서 [[seg(AB)]]에 내린 수선의 발을 H라 할 때, [[seg(OH)]]의 길이는?"),
    choices=["[[2 sqrt(2)]]", "[[2 sqrt(3)]]", "[[3 sqrt(2)]]", "[[3 sqrt(3)]]", "[[4 sqrt(2)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O)와 원 밖의 점 P(우하). 접선 PA(접점 A 우상)·PB(접점 B 아래), 현 AB, O에서 AB에 내린 수선의 발 H(직각 표시). PA=18(점선 치수), ∠APB=60°"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선+수선 도형",
    note="AH=9, ∠OAH=30° → OH=9·tan30°=3√3 → ④. 빠른정답 65와 불일치.")

# p33 (∠APB=60°, PA=24, OH)
add(id="9f47f62d", qtype="choice",
    question=("다음 그림에서 [[seg(AP)]], [[seg(BP)]]는 원 O의 접선이고 두 점 A, B는 접점이다. [[angle(APB) = deg(60)]], [[seg(PA) = 24]]이고 "
              "점 O에서 [[seg(AB)]]에 내린 수선의 발을 H라 할 때, [[seg(OH)]]의 길이는?"),
    choices=["[[2 sqrt(2)]]", "[[3 sqrt(2)]]", "[[3 sqrt(6)]]", "[[4 sqrt(2)]]", "[[4 sqrt(3)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O)와 원 밖의 점 P(우하). 접선 PA(접점 A 우상)·PB(접점 B 아래), 현 AB, O에서 AB에 내린 수선의 발 H(직각 표시). PA=24(점선 치수), ∠APB=60°"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선+수선 도형",
    note="AH=12, ∠OAH=30° → OH=12·tan30°=4√3 → ⑤. 빠른정답 2와 불일치.")

# p35 (∠AOB=120°, AO=12, 옳지 않은 것)
add(id="6dcbb0c0", qtype="choice",
    question=("아래 그림에서 [[seg(PA)]], [[seg(PB)]]는 원 밖의 한 점 P에서 원 O에 그은 접선이고 두 점 A, B는 접점이다. "
              "[[angle(AOB) = deg(120)]], [[seg(AO) = 12]] cm일 때, 다음 중 옳지 않은 것은?"),
    choices=["[[angle(APB) = deg(60)]]", "[[angle(APO) = angle(OAB) = deg(30)]]", "[[seg(AB) = 12]] cm", "[[seg(PO) = 24]] cm", "[[seg(PA) = 12 sqrt(3)]] cm"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). 접선 PA(접점 A 위)·PB(접점 B 아래), 현 AB와 PO의 교점 M, 선분 OA·OB. AO=12cm(점선 치수), ∠AOB=120°"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="AB=2·12·sin60°=12√3 ≠ 12 → ③이 틀림. 빠른정답 4와 불일치.")

# p37 (∠APB=60°, OA=6, 옳지 않은 것)
add(id="30918203", qtype="choice",
    question=("아래 그림에서 두 점 A, B는 점 P에서 원 O에 그은 두 접선의 접점이다. [[angle(APB) = deg(60)]], [[seg(OA) = 6]] cm일 때, "
              "다음 중 옳지 않은 것은?"),
    choices=["[[seg(PO) = 12]] cm", "[[seg(PB) = 6 sqrt(3)]] cm", "[[seg(AB) = 6 sqrt(3)]] cm", "[[quad(APBO) = 36]] cm²", "[[angle(OAB) = deg(30)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). 접선 PA(접점 A 위)·PB(접점 B 아래), 현 AB(PO와 직각 표시), 선분 OA·OB·PO. OA=6cm(점선 치수), ∠APB=60°"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="□APBO=2·(1/2)·6·6√3=36√3 ≠ 36 → ④ = 빠른정답 ✓.")

# p40 (2017년 3월 고1 20번, 두 원+접선, (가)(나)(다) — id 2개, 같은 문항)
dup(["45084433", "9aca8659"], qtype="choice",
    question=("그림과 같이 선분 AB를 지름으로 하는 원 O와 선분 AB 위의 점 C에 대하여 선분 BC를 지름으로 하는 원 O′이 있다. "
              "점 A에서 원 O′에 그은 두 접선이 원 O′과 만나는 점을 각각 D, E라 하고, 원 O와 만나는 점을 각각 F, G라 하자. "
              "다음은 두 선분 DE, AB의 교점을 H라 하고 [[angle(DAE) = deg(40)]]일 때, [[angle(FHG)]]의 크기를 구하는 과정이다.\n"
              "원 O′의 중심을 I라 할 때,\n"
              "[[angle(DFB) = angle(DHB) = deg(90)]] …… ㉠\n"
              "선분 DB는 공통인 변 …… ㉡\n"
              "[[angle(DIH)]] = (가) × [[angle(DBH)]]이고\n"
              "[[par(seg(DI), seg(FB))]]이므로\n"
              "[[angle(DBF) = angle(DBH)]] …… ㉢\n"
              "㉠, ㉡, ㉢에 의해 [[cong(tri(DFB), tri(DHB))]]이다.\n"
              "한편, [[seg(AD) = seg(AE)]]이므로 [[angle(ADH)]] = (나)°\n"
              "[[angle(DHF)]] = [[frac(1,2)]] × (나)°\n"
              "따라서 [[angle(FHG)]] = (다)°이다.\n"
              "위의 (가), (나), (다)에 알맞은 수를 각각 [[a]], [[b]], [[c]]라 할 때, [[frac(a c, b)]]의 값은?"),
    choices=["[[frac(18,7)]]", "[[frac(20,7)]]", "[[frac(22,7)]]", "[[frac(24,7)]]", "[[frac(26,7)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 O(지름 AB, A 위·B 아래)와 그 안에서 B에서 내접하는 작은 원 O′(지름 BC, C는 AB 위). A에서 원 O′에 그은 두 접선(접점 D 좌·E 우)이 원 O와 F(좌하)·G(우하)에서 만남. 현 DE와 AB의 교점 H. 선분 DB·EB·FH·GH·FB·GB. ∠DAE=40°"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 두 원+접선+현 복합 도형 / 프라임 점 라벨(O′)",
    note="출처 [2017년 3월 고1 20번/4점]. (가)=2, (나)=70, (다)=110 → ac/b=220/70=22/7 → ③(좌표 수치 검산 ✓). 빠른정답 4와 불일치.")

# p41 (반지름 4, PA=4√3, AB)
add(id="0e072c6d", qtype="choice",
    question=("다음 그림에서 두 직선 PA, PB는 반지름의 길이가 4 cm인 원 O의 접선이고 두 점 A, B는 접점이다. [[seg(PA) = 4 sqrt(3)]] cm일 때, "
              "[[seg(AB)]]의 길이는?"),
    choices=["6 cm", "[[2 sqrt(10)]] cm", "[[2 sqrt(11)]] cm", "[[4 sqrt(3)]] cm", "[[2 sqrt(13)]] cm"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). 접선 PA(접점 A 위)·PB(접점 B 아래), 현 AB, 선분 OA. PA=4√3cm, OA=4cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="PO=8, ∠APO=30° → ∠APB=60°, △PAB 정삼각형 → AB=4√3 → ④ = 빠른정답 ✓.")

# p42 (∠AOB=120°, PB=6√6, 옳지 않은 것)
add(id="a1bbe201", qtype="choice",
    question=("아래 그림과 같이 점 P에서 원 O에 그은 두 접선의 접점이 A, B이고 [[angle(AOB) = deg(120)]], [[seg(PB) = 6 sqrt(6)]] cm일 때, "
              "다음 중 옳지 않은 것은?"),
    choices=["[[seg(OP) = 12 sqrt(2)]] cm", "[[seg(AP) = 6 sqrt(6)]] cm", "[[seg(AB) = 6 sqrt(6)]] cm", "[[arc(AB) = 4 sqrt(2) pi]] cm",
             "([[quad(OAPB)]]의 둘레의 길이) = [[16 sqrt(6)]] cm"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 위)와 원 밖의 점 P(아래). 접선 PA(접점 A 좌)·PB(접점 B 우), 현 AB, 선분 OA·OB. ∠AOB=120°, PB=6√6cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="OB=6√6·tan30°=6√2, OP=12√2, AB=AP=6√6, 호 AB=2π·6√2/3=4√2π, 둘레=12√2+12√6 ≠ 16√6 → ⑤. 빠른정답 40과 불일치.")

# p46 (OA=6, OP=√85, □OAPB 넓이)
add(id="262b2ed9", qtype="short",
    question=("다음 그림과 같이 점 P에서 원 O에 그은 두 접선의 접점을 각각 A, B라 하자. [[seg(OA) = 6]] cm, [[seg(OP) = sqrt(85)]] cm일 때, "
              "사각형 OAPB의 넓이를 구하시오."),
    choices=None, derived_answer="42 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). 접선 PA(접점 A 위)·PB(접점 B 아래), 사각형 OAPB 음영(대각선 PO). OA=6cm, OP=√85cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="PA=√(85−36)=7 → 넓이 2·(1/2)·6·7=42cm². 빠른정답 5와 불일치.")

# p47 (OA=6, ∠APB:∠AOB=1:2, 색칠 부분 넓이)
add(id="394019e7", qtype="choice",
    question=("다음 그림과 같이 점 P에서 원 O에 그은 두 접선의 접점을 A, B라 하자. [[seg(OA) = 6]] cm이고, "
              "[[ratio(angle(APB), angle(AOB)) = ratio(1, 2)]]일 때, 색칠한 부분의 넓이는?"),
    choices=["[[(6 sqrt(3) - 2 pi)]] cm²", "[[(12 sqrt(3) - 4 pi)]] cm²", "[[(24 sqrt(3) - 8 pi)]] cm²", "[[(36 sqrt(3) - 12 pi)]] cm²", "[[(48 sqrt(3) - 16 pi)]] cm²"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). 접선 PA(접점 A 위)·PB(접점 B 아래), 선분 OA·OB. OA=6cm(점선 치수). 두 접선과 호 AB로 둘러싸인 부분 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선+음영 도형",
    note="∠APB=60°, ∠AOB=120°, PA=6√3 → □OAPB=36√3, 부채꼴=12π → 36√3−12π → ④ = 빠른정답 ✓.")

# p50 (∠APB=60°, PA=18, △AOB 넓이)
add(id="d59c23dc", qtype="choice",
    question=("다음 그림에서 두 직선 PA, PB는 원 O의 접선이고 두 점 A, B는 접점이다. [[angle(APB) = deg(60)]], [[seg(PA) = 18]] cm일 때, "
              "[[tri(AOB)]]의 넓이는?"),
    choices=["[[21 sqrt(3)]] cm²", "[[23 sqrt(3)]] cm²", "[[25 sqrt(3)]] cm²", "[[27 sqrt(3)]] cm²", "[[29 sqrt(3)]] cm²"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 좌측)와 원 밖의 점 P(우측). 접선 PA(접점 A 위)·PB(접점 B 아래), 삼각형 AOB 음영. PA=18cm(점선 치수), ∠APB=60°"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="OA=18·tan30°=6√3, ∠AOB=120° → (1/2)(6√3)²sin120°=27√3 → ④ = 빠른정답 ✓.")

# p51 (∠APB=60°, OA=4, △APB 넓이)
add(id="27c593c6", qtype="choice",
    question=("다음 그림과 같이 원 밖의 한 점 P에서 원 O에 그은 두 접선이 각각 점 A, B에 접한다. [[angle(APB) = deg(60)]], [[seg(OA) = 4]] cm일 때, "
              "[[tri(APB)]]의 넓이는?"),
    choices=["12 cm²", "[[12 sqrt(2)]] cm²", "[[12 sqrt(3)]] cm²", "24 cm²", "[[12 sqrt(5)]] cm²"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 P(좌측). 접선 PA(접점 A 위)·PB(접점 B 아래), 삼각형 APB 음영, 선분 OA·OB. OA=4cm(점선 치수), ∠APB=60°"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="PA=4√3, 정삼각형 넓이 (√3/4)·48=12√3 → ③ = 빠른정답 ✓.")

# p55 (∠AOB=120°, PB=4√6, 옳지 않은 것)
add(id="0ab04af7", qtype="choice",
    question=("아래 그림과 같이 점 P에서 원 O에 그은 두 접선의 접점이 A, B이고 [[angle(AOB) = deg(120)]], [[seg(PB) = 4 sqrt(6)]] cm일 때, "
              "다음 중 옳지 않은 것은?"),
    choices=["[[seg(OP) = 8 sqrt(2)]] cm", "[[seg(AP) = 4 sqrt(6)]] cm", "[[seg(AB) = 4 sqrt(6)]] cm",
             "(부채꼴 AOB의 넓이) = [[frac(32 sqrt(6), 3) pi]] cm²", "([[quad(OAPB)]]의 둘레) = [[(8 sqrt(2) + 8 sqrt(6))]] cm"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 아래)와 원 밖의 점 P(위). 접선 PB(접점 B 좌)·PA(접점 A 우), 현 AB, 선분 OA·OB. ∠AOB=120°, PB=4√6cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="OB=4√2, OP=8√2, AB=AP=4√6, 부채꼴 넓이=π(4√2)²/3=32π/3 ≠ 32√6π/3 → ④, 둘레 8√2+8√6 ✓. 빠른정답 5와 불일치.")

# p57 (∠AOB=120°, PB=3√3, 옳지 않은 것)
add(id="d331c59f", qtype="choice",
    question=("아래 그림과 같이 점 P에서 원 O에 그은 두 접선의 접점이 각각 A, B이고 [[angle(AOB) = deg(120)]], [[seg(PB) = 3 sqrt(3)]]일 때, "
              "다음 중 옳지 않은 것은?"),
    choices=["[[seg(OA) = 3]]", "[[seg(OP) = 6]]", "[[arc(AB) = 2 pi]]", "[[tri(APB) = frac(27 sqrt(3), 4)]]", "[[quad(OAPB) = frac(9 sqrt(3), 2)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 위)와 원 밖의 점 P(아래). 접선 PA(접점 A 좌, 직각 표시)·PB(접점 B 우, 직각 표시), 선분 OA·OB·OP. ∠AOP=60°, ∠AOB=120°, ∠APB=60°(P에 표시), PB=3√3(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="OA=3, OP=6, 호 AB=2π·3/3=2π, △APB=(√3/4)·27=27√3/4, □OAPB=2·(1/2)·3·3√3=9√3 ≠ 9√3/2 → ⑤ = 빠른정답 ✓.")

# p62 (방접원형, AB=14, AC=10, BC=12, CE=x)
add(id="f597500f", qtype="choice",
    question=("다음 그림에서 세점 D, E, F는 접점이다.\n[[seg(AB) = 14]], [[seg(AC) = 10]], [[seg(BC) = 12]]일 때, [[seg(CE)]]의 길이는?"),
    choices=["5", "6", "7", "8", "9"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 아래)와 원 밖의 점 A(위). A에서 그은 두 접선(접점 D 좌·E 우) 위에 각각 점 B·C가 있고, 선분 BC가 원에 F에서 접함. AB=14, AC=10, BC=12(점선 치수), CE=x"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+세 접선 도형",
    note="AD=AE → 14+BF=10+CE, BF+CF=12, CE=CF → x=8 → ④ = 빠른정답 ✓.")

# p64 (내접원 O r=3, 방접원 O′ r=11, OO′=17, AC)
add(id="15cf7055", qtype="short",
    question=("다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이고 점 D, E, F는 접접이다. 또, 원 O′은 [[seg(AB)]], [[seg(BC)]]의 연장선과 각각 점 P, Q에서 접하고 "
              "[[seg(AC)]]와 점 H에서 접한다. 두 원 O, O′의 반지름의 길이는 각각 3 cm, 11 cm이고 OO′ = 17 cm일 때, [[seg(AC)]]의 길이를 구하시오."),
    choices=None, derived_answer="15 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "각 B(좌하)에서 뻗은 두 반직선 사이에 삼각형 ABC(A 좌상, C 우하). 작은 내접원 O(접점 D(AB)·E(BC)·F(AC)), 큰 원 O′이 AB의 연장선 P·BC의 연장선 Q·AC의 H에서 접함. 선분 OO′=17cm(점선 치수), O′Q=11cm, OE=3cm"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 삼각형+내접원+방접원 도형 / 프라임 점 라벨(O′)",
    note="원문 '접접이다' 그대로. EQ=√(17²−(11−3)²)=15, BQ−BE=s−(s−AC)=AC → AC=15cm. 빠른정답 4와 불일치.")

# p65 (내접원 r=2, 방접원 r=11, OO′=15, AC)
add(id="971a1014", qtype="short",
    question=("다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이고 점 D, E, F는 접접이다. 또, 원 O′은 [[seg(AB)]], [[seg(BC)]]의 연장선과 각각 점 P, Q에서 접하고 "
              "[[seg(AC)]]와 점 H에서 접한다. 두 원 O, O′의 반지름의 길이는 각각 2 cm, 11 cm이고 OO′ = 15 cm일 때, [[seg(AC)]]의 길이를 구하시오."),
    choices=None, derived_answer="12 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "각 B(좌하)에서 뻗은 두 반직선 사이에 작은 삼각형 ABC. 작은 내접원 O(접점 D(AB)·E(BC)·F(AC)), 큰 원 O′이 AB의 연장선 P·BC의 연장선 Q·AC의 H에서 접함. OO′=15cm(점선 치수), O′Q=11cm, OE=2cm"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 삼각형+내접원+방접원 도형 / 프라임 점 라벨(O′)",
    note="원문 '접접이다' 그대로. EQ=√(15²−9²)=12=AC → 12cm. 빠른정답 4와 불일치.")

# p66 (내접원 r=6, 방접원 r=16, OO′=26, AC)
add(id="530975c8", qtype="short",
    question=("다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이고 점 D, E, F는 접접이다. 또, 원 O′은 [[seg(AB)]], [[seg(BC)]]의 연장선과 각각 점 P, Q에서 접하고 "
              "[[seg(AC)]]와 점 H에서 접한다. 두 원 O, O′의 반지름의 길이는 각각 6 cm, 16 cm이고 OO′ = 26 cm일 때, [[seg(AC)]]의 길이를 구하시오."),
    choices=None, derived_answer="24 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "각 B(좌하)에서 뻗은 두 반직선 사이에 삼각형 ABC. 작은 내접원 O(접점 D(AB)·E(BC)·F(AC)), 큰 원 O′이 AB의 연장선 P·BC의 연장선 Q·AC의 H에서 접함. OO′=26cm(점선 치수), O′Q=16cm, OE=6cm"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 삼각형+내접원+방접원 도형 / 프라임 점 라벨(O′)",
    note="원문 '접접이다' 그대로. EQ=√(26²−10²)=24=AC → 24cm. 빠른정답 3과 불일치.")

# p67 (AD·AF·BC 접선, AB=13, BC=11, CA=10, 빈칸 — id 2개, 같은 문항)
dup(["7658ca04", "e01b25a7"], qtype="choice",
    question=("다음 그림과 같이 [[seg(AD)]], [[seg(AF)]], [[seg(BC)]]는 원 O의 접선이고 점 D, E, F는 접점일 때, [[seg(AF)]]의 길이를 구하는 과정이다. "
              "□ 안에 알맞은 수를 차례대로 구한 것은?\n"
              "[[seg(BD) = seg(BE)]], [[seg(CE) = seg(CF)]]이므로\n"
              "[[seg(AD) + seg(AF) = seg(AB) + seg(BC) + seg(CA)]] = □\n"
              "이때 [[seg(AD) = seg(AF)]]이므로 [[seg(AF)]] = □"),
    choices=["28, 14", "30, 15", "32, 16", "34, 17", "36, 18"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 A(좌하). A에서 그은 두 접선 AD(접점 D 위, B는 AD 위)·AF(접점 F 아래, C는 AF 위), 선분 BC가 원에 E에서 접함. AB=13, BC=11, CA=10(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+세 접선 도형",
    note="AD+AF=13+11+10=34, AF=17 → ④ = 빠른정답 ✓.")

# p68 (AD·AF·BC 접선, AB=15, BC=13, CA=12, 빈칸)
add(id="0587e9bd", qtype="choice",
    question=("다음 그림과 같이 [[seg(AD)]], [[seg(AF)]], [[seg(BC)]]는 원 O의 접선이고 점 D, E, F는 접점일 때, [[seg(AF)]]의 길이를 구하는 과정이다. "
              "□ 안에 알맞은 수를 차례대로 구한 것은?\n"
              "[[seg(BD) = seg(BE)]], [[seg(CE) = seg(CF)]]이므로\n"
              "[[seg(AD) + seg(AF) = seg(AB) + seg(BC) + seg(CA)]] = □\n"
              "이때 [[seg(AD) = seg(AF)]]이므로 [[seg(AF)]] = □"),
    choices=["36, 18", "38, 19", "40, 20", "42, 21", "44, 22"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 A(좌하). A에서 그은 두 접선 AD(접점 D 위, B는 AD 위)·AF(접점 F 아래, C는 AF 위), 선분 BC가 원에 E에서 접함. AB=15, BC=13, CA=12(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+세 접선 도형",
    note="AD+AF=15+13+12=40, AF=20 → ③ = 빠른정답 ✓.")

# p72 (AD·BC·AF 접선, AO=17, OD=8, △ABC 둘레)
add(id="d6be4b0c", qtype="choice",
    question=("다음 그림에서 세 선분 AD, BC, AF는 원 O의 접선이고 점 D, E, F는 접점이다. [[seg(AO) = 17]] cm, [[seg(OD) = 8]] cm일 때, "
              "[[tri(ABC)]]의 둘레의 길이는?"),
    choices=["30 cm", "25 cm", "20 cm", "15 cm", "10 cm"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 O 우측)와 원 밖의 점 A(좌측). A에서 그은 두 접선 AD(접점 D 위, B는 AD 위)·AF(접점 F 아래, C는 AF 위), 선분 BC가 원에 E에서 접함. 선분 AO·OD·OE·OF. AO=17cm, OD=8cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+세 접선 도형",
    note="AD=√(17²−8²)=15 → 둘레=AD+AF=30cm → ① = 빠른정답 ✓.")

# p83 (반원 접선, AC=4, BD=9, PQ)
add(id="6ecbe8c9", qtype="choice",
    question=("다음 그림과 같이 원 O의 지름의 양 끝 점 A, B에서 그은 두 접선과 원 위의 한 점 P에서 그은 접선이 만나는 점을 각각 C, D라 하고 "
              "[[seg(AD)]]와 [[seg(BC)]]의 교점을 Q라 하자. [[seg(AC) = 4]], [[seg(BD) = 9]]일 때, [[seg(PQ)]]의 길이는?"),
    choices=["[[frac(36,13)]]", "[[frac(37,13)]]", "[[frac(38,13)]]", "3", "[[frac(40,13)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(지름 AB 가로, A 좌·B 우). A·B에서의 접선(세로 직선 2개), 원 위의 점 P(좌상)에서의 접선이 두 세로 접선과 C(좌)·D(우상)에서 만남. 선분 AD와 BC의 교점 Q, 선분 PQ. AC=4, BD=9(점선 치수)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원+세 접선+교점 도형",
    note="CP=4, PD=9, AC∥BD → CQ:QB=4:9=CP:PD → PQ∥BD, PQ=9·4/13=36/13 → ① = 빠른정답 ✓.")

# ================= 원에 내접하는 사각형 =================
# p3 (AB⊥CD, ∠PAB=28°, ∠QMN)
add(id="33a2cd1d", qtype="short",
    question=("다음 그림과 같이 원 O에서 [[seg(AB)]]와 [[seg(CD)]]가 수직으로 만나고 [[seg(AP)]]와 [[seg(CO)]], [[seg(DP)]]와 [[seg(BC)]]의 교점을 각각 M, N이라 한다. "
              "[[seg(AP)]]와 [[seg(BC)]]의 교점을 Q라 하고 [[angle(PAB) = deg(28)]]일 때, [[angle(QMN)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(28)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O, 지름 AB(세로, A 위·B 아래)와 현 CD(가로, C 좌·D 우)가 직각으로 만남(직각 표시). 원 위의 점 P(C 아래쪽 좌측). 선분 AP·CO·DP·BC·CP. AP∩CO=M, DP∩BC=N, AP∩BC=Q. ∠PAB=28°"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+현+교점 복합 도형",
    note="∠QMN=∠PAB=28°(좌표 수치 검산, 현 CD 위치와 무관) = 빠른정답 ✓.")

# p5 (∠BAC=60°, ∠BPC=115°, ∠PCD=55°, 옳지 않은 것)
add(id="261a3bfe", qtype="choice",
    question=("아래 그림에서 점 P는 [[seg(AC)]]와 [[seg(BD)]]의 교점이고 [[angle(BAC) = deg(60)]], [[angle(BPC) = deg(115)]], [[angle(PCD) = deg(55)]]일 때, "
              "다음 중 옳지 않은 것은?"),
    choices=["[[angle(PBA) = deg(55)]]", "[[angle(PDC) = deg(60)]]", "[[angle(APB) = deg(65)]]", "[[angle(CPD) = deg(65)]]", "네 점 A, B, C, D는 한 원 위에 있지 않다."],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "네 점 A(위)·B(좌하)·C(우하)·D(우). 선분 AC와 BD의 교점 P. 선분 AB·BC·CD. ∠BAC=60°, ∠BPC=115°, ∠PCD=55°"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 두 삼각형+교점 도형",
    note="∠APB=65°, ∠PBA=55°, ∠CPD=65°, ∠PDC=60°=∠BAC → 네 점이 한 원 위에 있음 → ⑤가 틀림. 빠른정답 30과 불일치.")

# p6 (□ABCO, ∠AOB=2∠ACB, OA=5, OD=3, DB=2, OC)
add(id="2cf426c9", qtype="short",
    question=("다음 그림의 [[quad(ABCO)]]에서 [[angle(AOB) = 2 angle(ACB)]]이다. 두 대각선 AC와 OB의 교점을 D라 하면 [[seg(OA) = 5]], [[seg(OD) = 3]], "
              "[[seg(DB) = 2]]일 때, [[seg(OC)]]의 길이를 구하시오."),
    choices=None, derived_answer="5",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCO(A 좌하, B 우하, C 우, O 위). 대각선 AC와 OB의 교점 D. OA=5, OD=3, DB=2(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+대각선 도형",
    note="OA=OB=5, ∠AOB=2∠ACB → O는 A, B, C를 지나는 원의 중심 → OC=5. 빠른정답 28과 불일치.")

# p8 (네 점 한 원, ∠x−∠y)
add(id="356f1959", qtype="choice",
    question=("다음 그림에서 네 점 A, B, C, D가 한 원 위에 있을 때, [[angle(x) - angle(y)]]의 크기는?"),
    choices=["[[deg(30)]]", "[[deg(35)]]", "[[deg(40)]]", "[[deg(45)]]", "[[deg(50)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "네 점 A(위)·B(좌하)·C(우하)·D(우). 선분 AB·BC·CD·AC·BD, AC∩BD=E. ∠ABD=60°, ∠AEB=65°, ∠ADB=45°, ∠BDC=x, ∠DBC=y"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 네 점+대각선 도형",
    note="∠BAC=55°=x(∠BDC), ∠CAD=180°−60°−45°−55°=20°=y(∠DBC) → x−y=35° → ②. 빠른정답 '1, 5'와 불일치.")

# p9 (네 점 한 원, ∠x)
add(id="4fa5bf9d", qtype="short",
    question=("다음 그림에서 네 점 A, B, C, D가 한 원 위에 있을 때, [[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(122)",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하), 대각선 AC·BD의 교점 P. ∠ADB=64°, ∠DBC=58°, ∠DPC=x"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+대각선 도형",
    note="∠ACB=∠ADB=64° → ∠BPC=180°−58°−64°=58° → x=∠DPC=122°. 빠른정답 5와 불일치.")

# p12 (반원, ∠OCP=∠ODP=14°, ∠AOC=43°, ∠DOB=x°, a/x 유한소수)
add(id="d92edf00", qtype="short",
    question=("다음 그림과 같이 [[seg(AB)]]를 지름으로 하는 반원 O에서 점 P는 [[seg(AB)]] 위의 점이다. [[angle(OCP) = angle(ODP) = deg(14)]], "
              "[[angle(AOC) = deg(43)]]이고 [[angle(DOB) = x]]°일 때,\n분수 [[frac(a, x)]]가 유한소수가 되도록 하는 가장 작은 자연수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": "지름 AB(A 좌·B 우)의 반원 O. 호 위의 점 C(좌상)·D(우). 지름 위의 점 P(O 오른쪽). 선분 OC·OD·CP·DP·CD. ∠OCP=14°, ∠ODP=14°, ∠AOC=43°, ∠DOB=x°"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 반원+교점 복합 도형",
    note="O, C, D, P 한 원 위 → ∠CDP=180°−137°=43°, ∠CDO=29°=∠OCD → ∠COD=122°, x=15 → a/15 유한소수 최소 a=3 = 빠른정답 ✓.")

# p14 (이등변삼각형 내접, ∠BCD=80°, BD=CE, ∠CAE)
add(id="e1d97df6", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC가 원에 내접한다. 점 C에서 [[angle(BCD) = deg(80)]]가 되도록 현 CD를 긋고 "
              "그 연장선 위에 [[seg(BD) = seg(CE)]]가 되도록 점 E를 잡을 때, [[angle(CAE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(100)",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 이등변삼각형 ABC(A 위, B 좌하, C 우하). 현 CD(D는 A 오른쪽 위 원 위), CD의 연장선 위 원 밖의 점 E(위). 선분 AD·AE·BD. ∠BCD=80°"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접삼각형+현 도형",
    note="∠ABD=∠ACD, AB=AC, BD=CE → △ABD≡△ACE → ∠CAE=∠BAD=180°−80°=100°(좌표 수치 검산). 빠른정답 '1, 5'와 불일치.")

# p15 (이등변삼각형 내접, ∠BCD=76°, BD=CE, ∠CAE)
add(id="bbfb9bc0", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC가 원에 내접한다. 점 C에서 [[angle(BCD) = deg(76)]]가 되도록 현 CD를 긋고 "
              "그 연장선 위에 [[seg(BD) = seg(CE)]]가 되도록 점 E를 잡을 때, [[angle(CAE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(104)",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 이등변삼각형 ABC(A 위, B 좌하, C 우하). 현 CD(D는 A 오른쪽 위 원 위), CD의 연장선 위 원 밖의 점 E(위). 선분 AD·AE·BD. ∠BCD=76°"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접삼각형+현 도형",
    note="△ABD≡△ACE → ∠CAE=∠BAD=180°−76°=104°. 빠른정답 3과 불일치.")

# p18 (AB=AC, ∠BAC=56°, ∠APB)
add(id="b3acba34", qtype="short",
    question=("다음 그림에서 [[seg(AB) = seg(AC)]], [[angle(BAC) = deg(56)]]일 때, [[angle(APB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(118)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 이등변삼각형 ABC(A 위, B 좌하, C 우하, AB=AC 표시). 호 AB 위의 점 P(좌), 선분 PA·PB. ∠BAC=56°"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접삼각형 도형",
    note="∠ACB=62° → ∠APB=180°−62°=118°. 빠른정답 104와 불일치.")

# p19 (오각형 ABCPD, DP∥BC, ∠P=42°, ∠BAC)
add(id="8ddefc13", qtype="short",
    question=("다음 그림과 같은 오각형 ABCPD에서 [[par(seg(DP), seg(BC))]]이고 [[angle(P) = deg(42)]]이다. 네 점 A, B, C, D를 지나는 원이 "
              "[[seg(PC)]]와 [[seg(PD)]]에 접할 때, [[angle(BAC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(42)",
    figure=[{"fn": "unsupported", "args": {"raw": "오각형 ABCPD(A 좌, B 좌하, C 아래, P 우, D 위). 선분 AC·DC. DP∥BC(화살표 표시). ∠P=42°"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 오각형+대각선 도형",
    note="PC=PD → ∠PCD=∠PDC=69°, DP∥BC → ∠BCD=69°, 접선과 현 ∠DBC=69° → ∠BDC=42°=∠BAC. 빠른정답 70과 불일치.")

# p20 (두 접선 ∠APB=30°, ∠x−∠y)
add(id="b5b0d7d5", qtype="choice",
    question=("다음 그림에서 두 점 A, B는 점 P에서 원 O에 그은 두 접선의 접점이다. [[angle(APB) = deg(30)]]일 때, [[angle(x) - angle(y)]]의 크기는?"),
    choices=["[[deg(10)]]", "[[deg(20)]]", "[[deg(30)]]", "[[deg(40)]]", "[[deg(50)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O와 원 밖의 점 P(좌). 접선 PA(접점 A 위)·PB(접점 B 아래). 원에 내접하는 사각형 ADBC(D는 P 쪽 호 AB 위, C는 반대쪽 호 위). ∠ADB=x, ∠ACB=y, ∠APB=30°"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선+내접사각형 도형",
    note="∠AOB=150° → y=75°, x=105° → x−y=30° → ③. 빠른정답 2와 불일치.")

# p21 (AD 지름, ∠CAD=36°, ∠ABC)
add(id="429ff068", qtype="short",
    question=("다음 그림에서 [[seg(AD)]]는 원 O의 지름이고 [[angle(CAD) = deg(36)]]일 때, [[angle(ABC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(126)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O, 지름 AD(가로, A 좌·D 우). 원 위의 점 B(좌하)·C(아래). 사각형 ABCD, 선분 AC. ∠CAD=36°, ∠ABC 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+내접사각형 도형",
    note="∠ACD=90° → ∠ADC=54° → ∠ABC=180°−54°=126°. 빠른정답 118과 불일치.")

# p24 (□ABCD 내접, AB=AD, ∠C=70°, ∠AED)
add(id="7500888a", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 원에 내접하고 [[seg(AB) = seg(AD)]], [[angle(C) = deg(70)]]일 때, [[angle(AED)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(145)",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하, AB=AD 표시). 호 AD 위의 점 E(위), 선분 EA·ED. ∠C=70°"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접사각형 도형",
    note="∠BAD=110°, ∠ABD=35° → ∠AED=180°−35°=145°. 빠른정답 126과 불일치.")

# p25 (□ABCD 내접, AB=AD, ∠C=80°, ∠AED)
add(id="72b27d78", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 원에 내접하고 [[seg(AB) = seg(AD)]], [[angle(C) = deg(80)]]일 때, [[angle(AED)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(140)",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 사각형 ABCD(A 좌상, D 우, B 좌하, C 우하, AB=AD 표시). 호 AD 위의 점 E(위), 선분 EA·ED. ∠A=100°, ∠C=80°"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접사각형 도형",
    note="∠BAD=100°, ∠ABD=40° → ∠AED=180°−40°=140°. 빠른정답 3과 불일치.")

# p27 (∠BAC=86°, ∠ABC=51°, 이등분선, 원, ∠AFB)
add(id="cb5b6e8b", qtype="short",
    question=("다음 그림과 같이 [[angle(BAC) = deg(86)]], [[angle(ABC) = deg(51)]]인 [[tri(ABC)]]에서 [[angle(BAC)]]의 이등분선과 [[seg(BC)]]의 교점을 D라 하자. "
              "두 점 C, D를 지나는 원과 [[seg(AC)]]의 교점을 E, [[seg(BE)]]의 교점을 F라 할 때, [[angle(AFB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(86)",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 좌하, C 우하). A의 이등분선 AD(D는 BC 위). C, D를 지나는 원이 AC와 E, BE와 F에서 만남. 선분 AF. ∠BAC=86°, ∠ABC=51°"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+원+교점 복합 도형",
    note="∠DAE=43°, ∠DFE=180°−∠DCE=137° → A, D, F, E 한 원 위 → ∠AFB=∠ADB=86°(좌표 수치 검산) = 빠른정답 ✓.")

# p28 (두 원 C·F에서 만남, ∠ACD=98°, ∠APE)
add(id="a5e5b858", qtype="short",
    question=("다음 그림과 같이 두 점 C, F에서 만나는 두 원이 있다. [[angle(ACD) = deg(98)]]일 때, [[angle(APE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(82)",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원(좌)과 작은 원(우)이 C(아래)·F(위)에서 만남. 큰 원 위의 점 B(좌)·A(우상), 작은 원 위의 점 E(위)·D(우). 직선 BA의 연장선과 직선 DE의 연장선이 원 밖의 점 P(위)에서 만남. 직선 BE는 F를 지남. 선분 AC·CD. ∠ACD=98°"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 두 원+교점+직선 복합 도형",
    note="∠BAC=∠BFC=∠EDC → ∠PAC+∠PDC=180° → □APDC 내접 → ∠APE=180°−98°=82°. 빠른정답 2와 불일치.")

# p31 (□ABCD 내접, ∠P=42°, 110°, x·y)
add(id="19137ab0", qtype="choice",
    question=("다음 그림에서 [[quad(ABCD)]]가 원에 내접할 때, [[angle(x)]], [[angle(y)]]의 크기를 각각 구한 것은?"),
    choices=["[[angle(x) = deg(68)]], [[angle(y) = deg(68)]]", "[[angle(x) = deg(68)]], [[angle(y) = deg(70)]]", "[[angle(x) = deg(68)]], [[angle(y) = deg(72)]]",
             "[[angle(x) = deg(70)]], [[angle(y) = deg(68)]]", "[[angle(x) = deg(70)]], [[angle(y) = deg(70)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 사각형 ABCD(A 좌상, D 위, B 좌하, C 우하). DA의 연장선과 CB의 연장선이 원 밖의 점 P(좌)에서 만남. ∠APB=42°, ∠ABC=110°, ∠BCD=x, ∠ADC=y"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접사각형+연장선 도형",
    note="y=180°−110°=70°, ∠PBA=70° → ∠PAB=68° → x=∠BCD=68° → ② = 빠른정답 ✓.")

# p32 (호 ADC 3/4, 호 BCD 3/8, ∠ADC+∠DCE)
add(id="f82a7731", qtype="choice",
    question=("다음 그림에서 호 ADC의 길이는 원주의 [[frac(3,4)]], 호 BCD의 길이는 원주의 [[frac(3,8)]]일 때, [[angle(ADC) + angle(DCE)]]의 크기는?"),
    choices=["[[deg(107.5)]]", "[[deg(112.5)]]", "[[deg(117.5)]]", "[[deg(122.5)]]", "[[deg(127.5)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 사각형 ABCD(A 좌, B 좌하, C 아래, D 우상). 선분 AD는 O를 지남. BC의 연장선 위 원 밖의 점 E(우)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접사각형+연장선 도형",
    note="∠ADC=(1/2)·90°=45°(호 ABC=1/4), ∠DCE=∠BAD=(1/2)·135°=67.5° → 112.5° → ②. 빠른정답 75와 불일치.")
