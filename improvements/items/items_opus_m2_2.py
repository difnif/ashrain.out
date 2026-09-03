# -*- coding: utf-8 -*-
# esc_opus_m2-2_1of1 — 이미지 기준 전사 (16 항목 / 16쪽, 모두 기하 도형 포함)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ── 삼각형의 무게중심 p83 (2020년 3월 고1 29번 변형)
add(id="9d7a9554", qtype="short",
    question=("[[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 무게중심을 G라 하고, 두 삼각형 GAB, GCA의 무게중심을 각각 P, Q라 하자. "
              "삼각형 APQ의 넓이가 45일 때, 삼각형 ABC의 넓이를 구하시오."),
    choices=None, derived_answer="243",
    figure=[{"fn": "unsupported", "args": {"raw": "이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 내부의 무게중심 G와 선분 GA·GB·GC, G 위쪽의 삼각형 APQ(P 왼쪽, Q 오른쪽, PQ는 BC와 평행)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·무게중심 복합 도형",
    note="출처 [2020년 3월 고1 29번 변형]. △APQ=(5/27)△ABC → 45×27/5=243 = 빠른정답 ✓.")

# ── 삼각형의 무게중심 p84 (2020년 3월 고1 29번/4점)
add(id="ffbbe5f2", qtype="short",
    question=("[[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 무게중심을 G라 하고, 두 삼각형 GAB, GCA의 무게중심을 각각 P, Q라 하자. "
              "삼각형 APQ의 넓이가 30일 때, 삼각형 ABC의 넓이를 구하시오."),
    choices=None, derived_answer="162",
    figure=[{"fn": "unsupported", "args": {"raw": "이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 내부의 무게중심 G와 선분 GA·GB·GC, G 위쪽의 삼각형 APQ(P 왼쪽, Q 오른쪽, PQ는 BC와 평행)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·무게중심 복합 도형",
    note="출처 [2020년 3월 고1 29번/4점]. △APQ=(5/27)△ABC → 30×27/5=162 = 빠른정답 ✓.")

# ── 이등변삼각형의 성질 p85 (RHS 합동)
add(id="e295d9fe", qtype="short",
    question=("다음 그림과 같이 사각형 ABCD에서 [[seg(AB) = 5]], [[seg(BC) = 7]], [[angle(BAD) = deg(90)]]이다. "
              "점 D에서 선분 BC에 내린 수선의 발을 H라 할 때, [[seg(AD) = seg(HD)]]이고 사각형 ABCD의 넓이가 18이다. "
              "사각형 ABHD의 두 대각선의 길이의 곱을 구하시오."),
    choices=None, derived_answer="30",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), A에 직각 표시, D에서 BC에 내린 수선의 발 H(직각 표시), 선분 BD; AB=5, BC=7 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형·수선·대각선 복합 도형",
    note="RHS 합동 △ABD≡△HBD → BH=5, HC=2; 넓이 5·AD+AD=18 → AD=3; 연 ABHD 넓이 15=½·(대각선 곱) → 30. 빠른정답 없음.")

# ── 이등변삼각형의 성질 p96 (각의 이등분선의 성질)
add(id="3f78c8dc", qtype="short",
    question=("다음 그림과 같이 점 H는 [[seg(BC)]]의 중점이고, 점 D는 [[angle(A)]]의 이등분선과 [[seg(BC)]]의 수직이등분선의 교점이다. "
              "점 D에서 두 직선 AB, AC에 내린 수선의 발을 각각 E, F라 하자.\n"
              "[[seg(AB) = 5]] cm, [[seg(DE) = 3]] cm, [[seg(AF) = 4]] cm일 때, [[tri(ADC)]]의 넓이를 구하시오."),
    choices=None, derived_answer="frac(9,2) cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽, C 오른쪽), BC의 중점 H(직각 표시), ∠A의 이등분선(A에 ○ 두 개)과 BC의 수직이등분선의 교점 D(BC 아래), E는 변 AB 위(직각 표시), F는 AC의 연장선 위(직각 표시), 선분 DB·DC·DE·DF·AD, △ADC 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·이등분선·수선 복합 도형",
    note="DE=DF=3, DB=DC → △DBE≡△DCF(RHS) BE=CF; AE=AF=4 → BE=1, AC=AF−CF=3 → △ADC=½·3·3=9/2 cm². 빠른정답 없음.")

# ── 평행선과 선분의 길이의 비 p45
add(id="ebbda950", qtype="short",
    question=("다음 그림의 평행사변형 ABCD 에서 [[ratio(seg(AD), seg(DQ), seg(QC)) = ratio(9, 6, 2)]] 이고 [[angle(D)]] 의 이등분선이 [[seg(BC)]] 와 "
              "만나는 점을 P 라고 할 때, [[quad(ABCQ)]] 의 넓이는 [[tri(DOQ)]] 의 넓이의 몇 배인지 구하여라."),
    choices=None, derived_answer="frac(25,6)",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), P는 BC 위(B 근처), Q는 CD 위(C 근처), 선분 AQ와 DP의 교점 O, D에 각의 이등분 표시(점 2개)"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 평행사변형·각의 이등분선·교점 복합 도형",
    note="AD∥BC → CP=CD=8, BP=1; AO:OQ=3:2 → △DOQ=(3/20)·평행사변형, □ABCQ=(5/8)·평행사변형 → 25/6배(풀이 답, 값이 특이하여 검토 요망). 빠른정답 없음.")

# ── 평행선과 선분의 길이의 비 p72
add(id="46634d7c", qtype="short",
    question=("다음 그림과 같은 사다리꼴 ABCD에서 [[par(par(seg(AD), seg(BC)), seg(EF))]]이고 [[seg(AD) = 9]] cm, [[seg(BC) = 14]] cm, "
              "[[seg(AB) = 12]] cm, [[seg(CD) = 13]] cm이다. [[quad(AEFD)]]와 [[quad(EBCF)]]의 둘레의 길이가 같을 때, [[seg(EF)]]의 길이를 구하시오."),
    choices=None, derived_answer="12 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB⊥BC(A·E·B에 직각 표시), E는 AB 위, F는 CD 위, AD·EF·BC에 평행 화살표; AD=9 cm, BC=14 cm, AB=12 cm, CD=13 cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사다리꼴·평행선 복합 도형 (AD∥BC∥EF는 par 중첩으로 표기)",
    note="AE=x: 9+x+13x/12 = (12−x)+14+13(12−x)/12 → x=36/5, EF=9+5·(3/5)=12 cm = 빠른정답 ✓.")

# ── 평행선과 선분의 길이의 비 p95 (2022년 3월 고1 30번 변형)
add(id="555a00ab", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 두 대각선의 교점을 E라 하자. "
              "점 E를 지나고 선분 AD와 평행한 직선이 선분 CD와 만나는 점을 F라 하고, 두 선분 AC, BF의 교점을 G라 하자.\n"
              "[[seg(AD) = 5]], [[seg(EF) = 4]]일 때, 사다리꼴 ABCD의 넓이는 삼각형 EGF의 넓이의 [[k]]배이다. [[8k]]의 값을 구하시오."),
    choices=None, derived_answer="375",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(윗변 AD 짧고 아랫변 BC 긺), 대각선 AC·BD의 교점 E, E를 지나 AD에 평행한 선분 EF(F는 CD 위), 선분 BF와 AC의 교점 G, 삼각형 EGF 음영"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 사다리꼴·대각선·평행선 복합 도형",
    note="출처 [2022년 3월 고1 30번 변형]. EF=BC·5/(5+BC)=4 → BC=20; △EGF=(1/25)△CGB, △CGB=(5/6)△EBC=(5/6)(16/25)S → k=375/8, 8k=375 = 빠른정답 ✓.")

# ── 경우의 수 p78
add(id="280bfbb9", qtype="short",
    question=("다음 그림과 같은 직선 사이에 거리가 [[6]] cm로 평행한 두 직선 [[l]], [[m]]이 있다. 직선 [[l]] 위에는 9개의 점이 [[1]] cm 간격으로 놓여 있고 "
              "직선 [[m]] 위에는 4개의 점이 [[3]] cm 간격으로 놓여 있다, 주어진 점 중에서 세 점을 연결하여 삼각형을 만들 때, "
              "삼각형의 넓이가 [[9]] cm² 이상이 되는 경우의 수를 구하시오."),
    choices=None, derived_answer="138",
    figure=[{"fn": "unsupported", "args": {"raw": "평행한 두 직선 l(위)·m(아래), 사이 거리 6 cm(직각 표시), l 위에 점 9개(1 cm 간격 표시), m 위에 점 4개(3 cm 간격 표시)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행한 두 직선 위 점 배치 도형",
    note="넓이=3×밑변 ≥ 9 → 밑변 ≥ 3: l 위 두 점(거리≥3) 21쌍×4=84, m 위 두 점 6쌍×9=54 → 138(전수 확인). 원문 '있다,'(쉼표) 그대로. 빠른정답 3과 불일치.")

# ── 피타고라스 정리의 활용 p59 (피타고라스 나무)
add(id="096ff8bd", qtype="short",
    question=("다음 그림은 [[angle(A) = deg(90)]]이고 [[seg(AB) = 15]] m, [[seg(AC) = 8]] m인 직각삼각형 ABC와 그 세 변을 각각 한 변으로 하는 "
              "정사각형을 계속 이어 붙여 그린 ‘피타고라스의 나무’ 이다. 이 그림을 벽에 그리고 정사각형에만 페인트로 칠하려고 한다. "
              "페인트 한 통으로 [[51]] m²를 칠할 수 있다고 할 때, 필요한 페인트는 최소 몇 통인지 구하시오.\n(단, 모든 직각삼각형은 서로 닮음이다.)"),
    choices=None, derived_answer="28통",
    figure=[{"fn": "unsupported", "args": {"raw": "피타고라스 나무(음영 정사각형 23개): BC 위 정사각형(0단), AB·AC 위 정사각형(1단), 각 정사각형 위 직각삼각형(직각 표시)의 두 변에 정사각형 2개씩 부착; AB쪽 가지는 4단까지(2단 2개·3단 4개·4단 8개), AC쪽 가지는 3단까지(2단 2개·3단 4개)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 피타고라스 나무(정사각형 23개) 도형",
    note="BC=17, 한 단의 넓이 합 289; 0~3단 완전(4×289=1156)+4단은 AB쪽 가지만(15²=225) → 1381 m², 1381/51≈27.1 → 28통 = 빠른정답 ✓.")

# ── 피타고라스 정리의 활용 p73 (구·판 단면)
add(id="867d1f64", qtype="short",
    question=("다음 [그림 1]은 삼각형 모양의 구멍이 있는 판 P에 반지름의 길이가 [[5]] cm인 구를 올려놓은 것이고 [그림 2]는 [그림 1]을 판 P의 윗면과 "
              "일치하는 면으로 자를 때 생기는 단면을 나타낸 것이다. [[seg(AB) = 11]] cm, [[seg(BC) = 13]] cm, [[seg(CA) = 20]] cm이고 [[tri(ABC)]]의 넓이는 "
              "[[66]] cm²이다. [그림 1]의 판 P의 윗면에 구멍이 없다고 할 때, 윗면에서 구의 가장 높은 점까지의 거리를 구하시오."),
    choices=None, derived_answer="9 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "[그림 1] 삼각형 구멍(꼭짓점 A, B, C)이 있는 판 P 위에 놓인 구(중심 O); [그림 2] 단면: △ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)와 세 변에 접하는 원, 원의 중심에서 각 변에 수선(점선); AB=11 cm, BC=13 cm, CA=20 cm 치수(점선 호)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 구·판 입체도와 삼각형 내접원 단면도",
    note="단면원=내접원 r=2·66/44=3, 중심 높이 √(5²−3²)=4 → 4+5=9 cm. 빠른정답 25cm와 불일치.")

# ── 피타고라스 정리의 활용 p79 (구·판 단면, 수치 변형)
add(id="d9d0523a", qtype="short",
    question=("다음 [그림 1]은 삼각형 모양의 구멍이 있는 판 P에 반지름의 길이가 [[25]] cm인 구를 올려놓은 것이고 [그림 2]는 [그림 1]을 판 P의 윗면과 "
              "일치하는 면으로 자를 때 생기는 단면을 나타낸 것이다. [[seg(AB) = 20]] cm, [[seg(BC) = 34]] cm, [[seg(CA) = 42]] cm이고 [[tri(ABC)]]의 넓이는 "
              "[[336]] cm²이다. [그림 1]의 판 P의 윗면에 구멍이 없다고 할 때, 윗면에서 구의 가장 높은 점까지의 거리를 구하시오."),
    choices=None, derived_answer="49 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "[그림 1] 삼각형 구멍(꼭짓점 A, B, C)이 있는 판 P 위에 놓인 구(중심 O); [그림 2] 단면: △ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)와 세 변에 접하는 원, 원의 중심에서 각 변에 수선(점선); AB=20 cm, BC=34 cm, CA=42 cm 치수(점선 호)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 구·판 입체도와 삼각형 내접원 단면도",
    note="단면원=내접원 r=2·336/96=7, 중심 높이 √(25²−7²)=24 → 24+25=49 cm. 빠른정답 4와 불일치.")

# ── 피타고라스 정리의 활용 p96 (원뿔대 최단 거리)
add(id="c92e9d42", qtype="short",
    question=("다음 그림과 같은 원뿔대에서 [[seg(AB) = 20]] cm, 윗면인 원의 반지름의 길이는 [[5]] cm, 아랫면인 원의 반지름의 길이는 [[10]] cm이다. "
              "점 A에서 [[seg(AB)]]의 중점 M까지 겉면을 따라 실을 팽팽하게 한 바퀴 감았을 때, 이 실의 길이를 구하시오."),
    choices=None, derived_answer="50 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "원뿔대(윗면 반지름 5 cm, 아랫면 반지름 10 cm), 모선 AB(A 아랫면 앞쪽, B 윗면), AB의 중점 M, 위로 점선 연장하여 꼭짓점 O, A에서 M까지 옆면을 한 바퀴 감는 실(붉은 곡선), 축과 아랫면에 직각 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원뿔대 입체도(실 감기)",
    note="OB=20, OA=40, 전개도 부채꼴 중심각 90° → 실 길이 √(40²+30²)=50 cm. 빠른정답 40cm와 불일치.")

# ── 여러 가지 사각형 p42 (등변사다리꼴, 좌표평면)
add(id="f66390f9", qtype="choice",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]], [[seg(AB) = seg(CD)]]인 등변사다리꼴 ABCD가 좌표평면 위에 있다. 점 A는 [[y]]축 위에, "
              "두 점 B, C는 [[x]]축 위에 있고 점 D의 좌표는 [[point(4, 6)]]이다. [[seg(AO)]] 위의 한 점 E에 대하여 삼각형 AED의 넓이가 8, "
              "삼각형 AEC의 넓이가 16일 때, 두 점 B, D를 지나는 일차함수의 그래프의 기울기는?"),
    choices=["[[frac(5,12)]]", "[[frac(1,2)]]", "[[frac(7,12)]]", "[[frac(2,3)]]", "[[frac(3,4)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: A는 y축 양의 부분, B는 x축 음의 부분, C는 x축 양의 부분, D(4, 6), E는 선분 AO 위, 등변사다리꼴 ABCD와 선분 AC·EC·ED"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 등변사다리꼴 복합 도형",
    note="A(0,6), △AED=½·AE·4=8 → AE=4, E(0,2); △AEC=½·4·OC=16 → C(8,0), B(−4,0) → 기울기 6/8=3/4 → ⑤. 빠른정답 '75'와 불일치(형식 상이).")

# ── 삼각형의 외심과 내심 p22 (직각삼각형의 외심·각)
add(id="a794c101", qtype="short",
    question=("다음 그림에서 점 O는 삼각형 ABC의 외심이고, 점 A에서 선분 BC에 내린 수선의 발을 H, 선분 AC의 중점을 M이라 할 때, "
              "[[angle(BAH) = deg(45)]], [[angle(BCO) = deg(14)]]이다. [[angle(HMO)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(28)",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽, C 오른쪽), A에서 BC에 내린 수선의 발 H(직각 표시), AC의 중점 M(같은 길이 표시), 외심 O(BC 아래쪽), 선분 OB·OC·OM·HM·AH, ∠BAH=45°, ∠BCO=14° 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·외심·수선 복합 도형",
    note="∠B=45°; 직각삼각형 AHC에서 MH=MC → ∠HMC=180°−2∠C, OM⊥AC → ∠HMO=|90°−∠HMC|=28°(O가 내부(∠C=59°)·외부(∠C=31°) 어느 경우든 28°). 빠른정답 12와 불일치.")

# ── 삼각형의 외심과 내심 p41 (삼각형의 내심)
add(id="31a9065f", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 [[seg(AB) = seg(AD)]], [[seg(BD) = seg(BC)]]이다. "
              "두 점 I, J는 각각 [[tri(ABD)]], [[tri(DBC)]]의 내심이고 [[seg(AI)]]와 [[seg(DJ)]]의 연장선의 교점을 E라 하자. "
              "[[angle(IBJ) = deg(48)]]일 때, [[angle(AED)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(57)",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD∥BC 화살표, AB=AD·BD=BC 같은 길이 표시, 대각선 BD, △ABD의 내심 I·△DBC의 내심 J, AI와 DJ의 연장선의 교점 E, 선분 BI·BJ, ∠IBJ=48° 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사다리꼴·내심 복합 도형",
    note="∠ABC=96°, ∠ABD=∠ADB=∠DBC=48°, ∠BAD=84°, ∠BDC=66° → ∠DAE=42°, ∠ADE=48°+33°=81° → ∠AED=57°. 빠른정답 '116 deg(x)'와 불일치.")

# ── 피타고라스 정리 p94 (색칠한 부분의 넓이)
add(id="17ae6093", qtype="short",
    question=("다음 그림과 같이 모양과 크기가 같은 사각형 4개가 한 점에서 만난다. [[angle(B) = deg(90)]]이고 [[seg(AB) = 8]] cm, "
              "[[seg(BC) = 6]] cm, [[seg(CD) = 26]] cm, [[seg(AD) = 24]] cm일 때, 색칠한 부분의 넓이를 구하시오."),
    choices=None, derived_answer="576 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "합동인 사각형 4개가 점 D에서 만나 바람개비 모양(초록 음영); 왼쪽 아래 사각형 ABCD: B에 직각 표시, AB=8 cm, BC=6 cm, CD=26 cm, AD=24 cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 합동 사각형 4개 바람개비 도형",
    note="AC=10, 10²+24²=26² → ∠CAD=90°, 한 사각형 넓이 24+120=144 → 4개 576 cm². 빠른정답 3과 불일치.")
