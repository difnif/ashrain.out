# -*- coding: utf-8 -*-
# esc_sonnet_m1-2_2of4 — 이미지 기준 전사 (83 항목 / 80쪽; 중1-2 원과 부채꼴·줄기와 잎·다각형·다면체·점선면·구·작도·뿔·평행선)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
FIG = "도형 표현 불가: "

# ======================= 원과 부채꼴 =======================
# p41
add(id="4d9b9d87", qtype="short",
    question=("다음 그림의 반원 O에서 [[par(seg(AB), seg(CD))]]이고 [[angle(AOB) = deg(150)]]일 때, "
              "[[arc(AB)]]의 길이는 [[arc(AC)]]의 길이의 몇 배인지 구하시오."),
    choices=None, derived_answer="10",
    figure=U("반원 O(지름 CD 수평, C 왼쪽·D 오른쪽, 중심 O). 호 위의 점 A(왼쪽 위)·B(오른쪽 위), 현 AB∥CD(화살표 표시), 선분 OA·OB, ∠AOB=150°"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "반원 안 평행 현·중심각 도형",
    note="AB∥CD → ∠AOC=∠BOD=15°, 150:15=10배. 빠른정답 2와 불일치.")

# p47
add(id="e40cf44e", qtype="choice",
    question=("다음 그림과 같이 [[seg(CD)]]가 지름인 원 O에서 [[par(seg(AB), seg(CD))]]이고 [[angle(AOB) = deg(90)]]일 때, "
              "[[ratio(arc(AC), arc(AB), arc(BD))]]는?"),
    choices=["[[ratio(1, 1, 1)]]", "[[ratio(1, 2, 1)]]", "[[ratio(2, 2, 1)]]", "[[ratio(2, 3, 1)]]", "[[ratio(2, 3, 2)]]"],
    derived_answer="②",
    figure=U("원 O, 지름 CD 수평(C 왼쪽·D 오른쪽). 위쪽 현 AB∥CD(화살표 표시), 선분 OA·OB, ∠AOB=90°(직각 표시)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "원 안 평행 현·직각 중심각 도형",
    note="∠AOC=∠BOD=45° → 45:90:45=1:2:1 → ②. 빠른정답 '10cm'과 불일치.")

# p49
add(id="c11230b9", qtype="choice",
    question=("다음 그림의 원 O에서 [[par(seg(AD), seg(OC))]], [[angle(AOC) = deg(36)]], [[arc(AC) = 7]] cm일 때, "
              "[[arc(AD)]]의 길이는?"),
    choices=["[[14]] cm", "[[15]] cm", "[[18]] cm", "[[21]] cm", "[[24]] cm"],
    derived_answer="④",
    figure=U("원 O, 지름 AB 수평(A 왼쪽·B 오른쪽). A에서 오른쪽 위로 현 AD, O에서 왼쪽 아래로 반지름 OC, AD∥OC(화살표 표시), ∠AOC=36°, 호 AC=7cm 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "원 안 평행 현·반지름 도형",
    note="∠DAO=∠AOC=36°(엇각), △OAD 이등변 → ∠AOD=108°, 호 AD=7×108/36=21 → ④. 빠른정답 '12cm'과 불일치.")

# p51
add(id="a5c99642", qtype="choice",
    question=("다음 그림의 원 O에서 [[par(seg(AD), seg(CO))]]이고 [[angle(AOC) = deg(15)]], [[arc(AC) = 2]] cm일 때, "
              "[[arc(AD)]]의 길이는?"),
    choices=["[[16]] cm", "[[17]] cm", "[[18]] cm", "[[19]] cm", "[[20]] cm"],
    derived_answer="⑤",
    figure=U("원 O, 지름 AB 수평(A 왼쪽·B 오른쪽). A에서 오른쪽 위로 현 AD, O에서 왼쪽 아래로 반지름 OC, AD∥CO(화살표 표시), ∠AOC=15°, 호 AC=2cm 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "원 안 평행 현·반지름 도형",
    note="∠DAO=15°, ∠AOD=150°, 호 AD=2×150/15=20 → ⑤. 빠른정답 '6cm'과 불일치.")

# p59
add(id="988c5df1", qtype="short",
    question=("다음 그림의 원 O에서 점 P는 [[ray(BA)]]와 [[ray(DC)]]의 교점이고, [[angle(P) = deg(30)]], "
              "[[seg(OC) = seg(CP) = seg(CD)]], [[arc(BD) = 12]] cm일 때, [[arc(AC)]]의 길이를 구하시오."),
    choices=None, derived_answer="4 cm",
    figure=U("원 O, 지름 BA(B 오른쪽 위, A 왼쪽 아래)의 연장선과 현 DC(D 오른쪽 아래, C 왼쪽 아래)의 연장선이 왼쪽 아래 점 P에서 만남. ∠P=30°, OC=CP=CD(같은 길이 표시), 호 BD=12cm 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "원·지름 연장선·현 연장선 교점 도형",
    note="∠COP=30°, ∠OCD=60°, △OCD 정삼각형 → ∠BOD=90°, 호 AC=12×30/90=4 cm. 빠른정답 3과 불일치.")

# p60
add(id="763c2289", qtype="short",
    question=("다음 그림과 같이 원 O의 지름 AB의 연장선과 현 CD의 연장선의 교점을 P라 하자. "
              "[[seg(DO) = seg(DP)]], [[angle(P) = deg(30)]]일 때, [[angle(AOC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(90)",
    figure=U("원 O, 지름 AB(A 왼쪽 위, B 오른쪽 아래)의 연장선과 현 CD(C 왼쪽 아래, D 오른쪽 아래)의 연장선이 오른쪽 아래 점 P에서 만남. DO=DP(같은 길이 표시), ∠P=30°"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "원·지름 연장선·현 연장선 교점 도형",
    note="∠DOP=30°, ∠ODC=∠OCD=60°, ∠COD=60° → ∠AOC=180−60−30=90°. 빠른정답 없음.")

# p63
add(id="9b853139", qtype="choice",
    question=("다음 그림과 같이 원 O의 지름 AB의 연장선과 현 CD의 연장선의 교점을 P라 하자. "
              "[[seg(DO) = seg(DP)]], [[angle(AOC) = deg(48)]], [[arc(AC) = 12]] cm일 때, [[arc(CD)]]의 길이는?"),
    choices=["[[27]] cm", "[[28]] cm", "[[29]] cm", "[[30]] cm", "[[31]] cm"],
    derived_answer="③",
    figure=U("원 O, 지름 AB 수평(A 왼쪽·B 오른쪽)의 연장선과 현 CD(C 왼쪽 위, D 오른쪽)의 연장선이 오른쪽 점 P에서 만남. DO=DP(같은 길이 표시), ∠AOC=48°, 호 AC=12cm 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "원·지름 연장선·현 연장선 교점 도형",
    note="∠P=x → ∠AOC=3x=48°, x=16°, ∠COD=180−4x=116°, 호 CD=12×116/48=29 → ③. 빠른정답 없음.")

# p64
add(id="a182d747", qtype="short",
    question=("다음 그림에서 점 P는 원 O의 지름 BA와 현 DC의 연장선의 교점이고 [[seg(PC) = seg(CO)]], [[angle(P) = deg(18)]], "
              "[[arc(AC) = 3]] cm일 때, [[arc(BD)]]의 길이를 구하시오."),
    choices=None, derived_answer="9 cm",
    figure=U("원 O, 지름 BA(B 오른쪽 위, A 왼쪽 아래)의 연장선과 현 DC(D 오른쪽 아래, C 왼쪽 아래)의 연장선이 왼쪽 점 P에서 만남. PC=CO(같은 길이 표시), ∠P=18°"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "원·지름 연장선·현 연장선 교점 도형",
    note="∠AOC=18°, ∠OCD=∠ODC=36°, ∠COD=108° → ∠BOD=54°, 호 BD=3×54/18=9 cm. 빠른정답 2와 불일치.")

# p65
add(id="19521531", qtype="choice",
    question=("다음 그림과 같이 원 O의 지름 AB의 연장선과 현 CD의 연장선의 교점을 P라 하자. "
              "[[seg(DO) = seg(DP)]], [[angle(AOC) = deg(72)]], [[arc(AC) = 18]] cm일 때, [[arc(CD)]]의 길이는?"),
    choices=["[[20]] cm", "[[21]] cm", "[[22]] cm", "[[23]] cm", "[[24]] cm"],
    derived_answer="②",
    figure=U("원 O, 지름 AB 수평(A 왼쪽·B 오른쪽)의 연장선과 현 CD(C 왼쪽 위, D 오른쪽)의 연장선이 오른쪽 점 P에서 만남. DO=DP(같은 길이 표시), ∠AOC=72°, 호 AC=18cm 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "원·지름 연장선·현 연장선 교점 도형",
    note="∠P=x → 3x=72°, x=24°, ∠COD=84°, 호 CD=18×84/72=21 → ②. 빠른정답 '6cm'과 불일치.")

# p81
add(id="62497449", qtype="short",
    question=("다음 그림의 원 O에서 반지름의 길이는 [[5]] cm, [[seg(EH) = 8]] cm이고 [[angle(EOH) = angle(FOG)]]일 때, "
              "[[seg(FG)]]의 길이를 구하시오."),
    choices=None, derived_answer="8 cm",
    figure=U("원 O. 위쪽 현 EH(8cm 표시), 아래쪽 현 FG, 반지름 OE·OH·OF·OG(OH=5cm 표시), ∠EOH=∠FOG(같은 각 표시)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "원 안 두 현·중심각 도형",
    note="같은 중심각 → 같은 현, FG=8 cm. 빠른정답 3과 불일치.")

# p82
add(id="1e84dc69", qtype="short",
    question=("다음 그림과 같이 반지름의 길이가 [[5]] cm인 원 O에서 [[angle(AOB) = angle(COD)]]이고 [[seg(AB) = 7]] cm일 때, "
              "[[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="7 cm",
    figure=U("원 O. 위쪽 현 AB(7cm 표시), 아래쪽 현 DC, 반지름 OA·OB·OC·OD(OB=5cm 표시), ∠AOB=∠COD(같은 각 표시)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "원 안 두 현·중심각 도형",
    note="같은 중심각 → 같은 현, CD=7 cm. 빠른정답 4와 불일치.")

# p84
add(id="41c5af76", qtype="short",
    question=("다음 그림의 원 O에서 반지름의 길이는 [[3]] cm, [[seg(AB) = 5]] cm이고 [[angle(AOB) = angle(COD)]]일 때, "
              "[[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="5 cm",
    figure=U("원 O. 위쪽 현 AB(5cm 표시), 아래쪽 현 DC, 반지름 OA·OB·OC·OD(OB=3cm 표시), ∠AOB=∠COD(같은 각 표시)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "원 안 두 현·중심각 도형",
    note="같은 중심각 → 같은 현, CD=5 cm. 빠른정답 '8cm'과 불일치.")

# p89
add(id="2452223e", qtype="short",
    question=("다음 그림의 원 O에서 [[seg(AE)]]가 지름이고 [[seg(AB) = seg(CD)]], [[angle(BOE) = deg(132)]]일 때, "
              "[[angle(COD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(48)",
    figure=U("원 O, 지름 AE 수직(A 위·E 아래). 오른쪽 위 점 B, 왼쪽 점 C, 왼쪽 아래 점 D. 현 AB·CD(같은 길이 표시), 반지름 OB·OC·OD, ∠BOE=132°"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "원 안 지름·두 현 도형",
    note="∠AOB=180°−132°=48°, AB=CD → ∠COD=48°. 빠른정답 12와 불일치.")

# p92
add(id="af91584a", qtype="choice",
    question="다음 원을 보고 [[2 angle(AOD) = angle(BOC)]]일 때 옳은 것을 모두 고르면? (정답 2개)",
    choices=["[[seg(OA) = seg(OC)]]", "[[2 arc(AD) = arc(BC)]]", "[[2 seg(AD) = seg(BC)]]",
             "[[2 tri(ODA) = tri(OBC)]]", "[[2 seg(OB) = seg(DB)]]"],
    derived_answer="①, ②",
    figure=U("원 O. 왼쪽 위 A, 위 오른쪽 B, 왼쪽 아래 D, 아래 오른쪽 C. 반지름 OA·OD·OB·OC, 현 BC"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "원 안 중심각 도형",
    note="반지름 같음 ①, 호는 중심각에 정비례 ②. 현·삼각형 넓이는 비례하지 않음, ⑤ 근거 없음 → ①, ②. 빠른정답 없음.")

# p94
add(id="69cdaf18", qtype="choice",
    question="아래 그림에서 4개의 각의 크기는 모두 같다. 다음 중 옳지 않은 것은?",
    choices=["[[seg(AB) = seg(DE)]]", "(부채꼴 OAD의 넓이) = (부채꼴 OAB의 넓이) × 3", "[[tri(OAB) = tri(ODE)]]",
             "[[frac(1,3) arc(BCE) = arc(AB)]]", "[[frac(2,3) seg(BE) = seg(AC)]]"],
    derived_answer="⑤",
    figure=U("원 O 위에 시계 방향으로 A(위), B, C, D, E(왼쪽 아래). 반지름 OA·OB·OC·OD·OE와 현 AB·BC·CD·DE. ∠AOB=∠BOC=∠COD=∠DOE(같은 각 표시 ○ 4개)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "원을 같은 중심각 4개로 나눈 도형",
    note="현의 길이는 중심각에 정비례하지 않으므로 ⑤가 옳지 않음. 빠른정답 없음.")

# p98
add(id="d838f743", qtype="choice",
    question=("아래 그림의 원 O에서 [[angle(AOD) = deg(45)]], [[angle(BOC) = deg(135)]]일 때, 다음 중 옳지 않은 것은?"),
    choices=["[[seg(AO) = seg(CO)]]", "[[seg(BO) = seg(DO)]]", "[[seg(AD) != seg(BC)]]",
             "[[arc(BC) = 3 arc(AD)]]", "[[arc(CD) = frac(1,2) arc(BC)]]"],
    derived_answer="⑤",
    figure=U("원 O. 위쪽 현 AD(A 왼쪽 위, D 오른쪽 위), 아래쪽 현 BC(B 왼쪽, C 오른쪽 아래). 반지름 OA·OD·OB·OC, ∠AOD=45°, ∠BOC=135°"),
    difficulty_est=2, confidence=0.75,
    needs_review=FIG + "원 안 두 현·중심각 도형",
    note="∠COD는 주어지지 않아 ⑤는 알 수 없음(①~④ 옳음) → ⑤. 빠른정답 3과 불일치.")

# ======================= 줄기와 잎 그림 =======================
# p17
add(id="2c3068cf", qtype="short",
    question=("다음은 어느 반 학생들의 키를 조사하여 나타낸 것이다. □ 안에 알맞은 수를 써넣으시오.\n"
              "(단위: cm)\n"
              "15|9는 □ cm를 나타낸다."),
    choices=None, derived_answer="159",
    figure=[{"fn": "table", "args": {"rows": [["177", "169", "172", "163", "148"],
                                              ["155", "180", "170", "185", "159"],
                                              ["153", "173", "182", "168", "187"]]}}],
    difficulty_est=1, confidence=0.9,
    note="줄기 15, 잎 9 → 159 cm. 빠른정답 2와 불일치.")

# p65
add(id="50b38799", qtype="choice",
    question=("아래는 혜은이네 학교 선생님들의 나이를 조사하여 나타낸 줄기와 잎 그림이다. 다음 중 옳지 않은 것은?\n"
              "(2|5는 25세)"),
    choices=["학교 선생님은 모두 15명이다.", "가장 젊은 선생님의 나이는 25세이다.", "40대인 선생님은 5명이다.",
             "선생님 나이의 평균은 40세이다.", "30대인 선생님은 전체의 20%이다."],
    derived_answer="④",
    figure=[{"fn": "table", "args": {"head": ["줄기", "잎"],
                                     "rows": [["2", "5 7 9"], ["3", "0 1 8"], ["4", "1 4 6 6 9"], ["5", "0 1 2 6"]]}}],
    difficulty_est=2, confidence=0.9,
    note="15명, 합 615 → 평균 41세이므로 ④ 거짓. 30대 3/15=20% ✓. 빠른정답 4 ✓.")

# ======================= 다각형 =======================
# p30
add(id="0e2e17e7", qtype="choice",
    question="다음 그림에서 [[angle(x)]]의 크기는?",
    choices=["[[deg(105)]]", "[[deg(115)]]", "[[deg(125)]]", "[[deg(135)]]", "[[deg(145)]]"],
    derived_answer="③",
    figure=U("삼각형. 오른쪽 아래 꼭짓점의 내각 55°, 밑변의 오른쪽 연장선과 이루는 외각 x"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "삼각형 외각 도형(55°가 그림에만 있음)",
    note="x=180°−55°=125° → ③. 빠른정답 없음.")

# p49
add(id="7e465ea5", qtype="choice",
    question="다음 그림과 같은 [[tri(ABC)]]에서 [[angle(x) + angle(y)]]의 크기는?",
    choices=["[[deg(150)]]", "[[deg(160)]]", "[[deg(170)]]", "[[deg(180)]]", "[[deg(190)]]"],
    derived_answer="③",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 밑변 BC를 양쪽으로 연장. B의 왼쪽 외각 130°, 내각 ∠ABC=x; C의 내각 60°, 오른쪽 외각 y"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "삼각형 내각·외각 도형(130°·60°가 그림에만 있음)",
    note="x=50°, y=120° → 170° → ③. 빠른정답 없음.")

# p57 — 선지 5개가 모두 그림
add(id="818da9cd", qtype="choice",
    question="다음 중 [[angle(x)]]의 크기가 가장 큰 것은?",
    choices=["(그림) 삼각형: 한 내각 [[deg(60)]]과 이웃한 외각 [[angle(x)]]",
             "(그림) 사각형: 한 내각 [[deg(70)]]과 이웃한 외각 [[angle(x)]]",
             "(그림) 사각형: 한 내각 [[deg(45)]]과 이웃한 외각 [[angle(x)]]",
             "(그림) 오각형: 한 내각 [[deg(85)]]과 이웃한 외각 [[angle(x)]]",
             "(그림) 오각형: 한 내각 [[deg(110)]]과 이웃한 외각 [[angle(x)]]"],
    derived_answer="③",
    figure=U("선지 ①~⑤가 각각 다각형 그림: ① 삼각형(내각 60°, 외각 x) ② 사각형(내각 70°, 외각 x) ③ 사각형(내각 45°, 외각 x) ④ 오각형(내각 85°, 외각 x) ⑤ 오각형(내각 110°, 외각 x)"),
    difficulty_est=1, confidence=0.7,
    needs_review=FIG + "선지 5개가 다각형 그림 / 선지를 그림 설명 텍스트로 대체(텍스트 혼합)",
    note="외각 x=180°−내각: 120°, 110°, 135°, 95°, 70° → ③. 빠른정답 deg(60)과 불일치.")

# p66
add(id="4f83d7fa", qtype="choice",
    question="다음 중 정사각형에 대한 설명으로 옳지 않은 것을 고르면?",
    choices=["변의 개수는 4이다.", "모든 내각의 크기는 같다.", "모든 변의 길이는 같다.",
             "한 꼭짓점에서 내각과 외각의 크기의 합은 [[deg(360)]]이다.", "모든 대각선의 길이가 같다."],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="내각+외각=180° → ④. 빠른정답 없음.")

# p67
add(id="41b44925", qtype="short",
    question="다음 □ 안에 알맞은 말을 써넣으시오.\n아홉 내각의 크기가 같은 정다각형을 □이라 한다.",
    choices=None, derived_answer="정구각형", figure=None, difficulty_est=1, confidence=0.9,
    note="빠른정답 '정구각형' ✓.")

# ======================= 다면체 =======================
# p98
add(id="70de1b82", qtype="short",
    question=("다음 그림과 같은 정육면체에서 점 I는 [[seg(CG)]]의 중점이다. 이 정육면체를 세 점 D, I, F를 지나는 평면으로 자를 때 "
              "나누어지는 두 입체도형의 면의 개수의 합을 구하시오."),
    choices=None, derived_answer="12",
    figure=U("정육면체 ABCD-EFGH(윗면 ABCD: A 뒤왼쪽·D 뒤오른쪽·B 앞왼쪽·C 앞오른쪽, 아랫면 EFGH 대응: E 뒤왼쪽·H 뒤오른쪽·F 앞왼쪽·G 앞오른쪽). 모서리 CG의 중점 I, 오른쪽 옆면 CDHG 진한 색"),
    difficulty_est=3, confidence=0.75,
    needs_review=FIG + "정육면체·중점 도형",
    note="절단면은 마름모 DIFJ(J는 AE의 중점) → 두 입체 모두 면 6개, 합 12. 빠른정답 5와 불일치.")

# ======================= 점, 선, 면 =======================
# p24
add(id="d64a1c9a", qtype="choice",
    question="다음 그림에서 [[ray(BD)]]와 같은 것은?",
    choices=["[[ray(AB)]]", "[[ray(CD)]]", "[[line(BD)]]", "[[ray(BC)]]", "[[ray(DB)]]"],
    derived_answer="④",
    figure=U("오른쪽 위로 기울어진 한 직선 위에 왼쪽부터 네 점 A, B, C, D"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "직선 위 네 점 도형",
    note="시점 B, 방향 D → 반직선 BC → ④. 빠른정답 10과 불일치.")

# p30
add(id="3cb6e4af", qtype="choice",
    question="아래 그림과 같이 직선 위에 네 점 A, B, C, D가 있을 때, 다음 중 옳지 않은 것은?",
    choices=["[[line(AC) = line(CD)]]", "[[ray(BC) = ray(CD)]]", "[[seg(BC) = seg(CB)]]",
             "[[ray(AB) = ray(AC)]]", "[[line(BC) = line(CB)]]"],
    derived_answer="②",
    figure=U("수평 직선 위에 왼쪽부터 네 점 A, B, C, D"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "직선 위 네 점 도형",
    note="시점이 다른 반직선 BC≠CD → ②. 빠른정답 3과 불일치.")

# p43
add(id="3846c144", qtype="short",
    question=("수직선 위에 있는 8개의 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,8)]]의 좌표는 각각 1, 2, 3, ⋯, 8이다. "
              "이 8개의 점 중에서 두 점을 이어 선분을 만들 때, 길이가 합성수인 선분의 개수를 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="길이 4인 선분 4개, 6인 선분 2개 → 6. 빠른정답 60과 불일치.")

# p67
add(id="0914e9cc", qtype="short",
    question=("다음 그림에서 [[seg(AP) = seg(PQ)]], [[3 seg(AP) = seg(QB)]]일 때, □ 안에 알맞은 수를 써넣으시오.\n"
              "[[seg(AQ)]] = □ [[seg(AB)]]"),
    choices=None, derived_answer="frac(2,5)",
    figure=U("선분 AB 위에 왼쪽부터 A, P, Q, B. AP=PQ 같은 길이 표시"),
    difficulty_est=1, confidence=0.85,
    note="AP=a → AQ=2a, AB=5a → 2/5. 빠른정답 frac(2,5) ✓.")

# p70
add(id="eb77b6ea", qtype="short",
    question=("다음 그림에서 점 M은 [[seg(AB)]]의 중점이고, 점 N은 [[seg(MB)]]의 중점일 때, □ 안에 알맞은 수를 써넣으시오.\n"
              "[[seg(NB)]] = □ [[seg(MB)]]"),
    choices=None, derived_answer="frac(1,2)",
    figure=U("선분 AB 위에 왼쪽부터 A, M, N, B. MN=NB 같은 길이 표시"),
    difficulty_est=1, confidence=0.85,
    note="N은 MB의 중점 → 1/2. 빠른정답 frac(1,2) ✓.")

# p71
add(id="b3d7ad06", qtype="choice",
    question=("[[seg(AB)]]의 중점이 M이고, [[seg(AM)]], [[seg(MB)]]의 중점을 각각 P, Q라 할 때, 다음 중 옳지 않은 것은?"),
    choices=["[[seg(AM) = seg(BM)]]", "[[seg(AB) = 2 seg(PQ)]]", "[[seg(AM) = frac(1,2) seg(AB)]]",
             "[[seg(PM) = 2 seg(PQ)]]", "[[seg(AB) = 4 seg(PM)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="PQ=2PM이므로 ④ 거짓. 빠른정답 4 ✓.")

# p74
add(id="d76653fb", qtype="choice",
    question=("다음 조건을 모두 만족시키는 서로 다른 다섯 개의 점 A, B, C, D, E 중에서 왼쪽에서 두 번째 점은?\n"
              "(가) 다섯 개의 점 A, B, C, D, E는 한 직선 위에 있고 점 A는 맨 왼쪽에 있다.\n"
              "(나) 점 B는 선분 AC의 중점이다.\n"
              "(다) [[seg(AE) = frac(1,3) seg(AD)]]\n"
              "(라) 다섯 개의 점 중에서 이웃한 두 점 사이의 거리는 모두 같다."),
    choices=["A", "B", "C", "D", "E"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="A(0), E(1), B(2), D(3), C(4) → 두 번째는 E → ⑤. 빠른정답 5 ✓.")

# p78
add(id="a9b0012a", qtype="short",
    question=("[[seg(AB)]]의 삼등분점을 각각 P, Q라 하고 [[seg(AP)]]의 중점을 M이라 할 때, "
              "[[frac(seg(AM) + seg(QB), seg(MP))]]의 값을 구하시오.\n(단, 점 P가 점 Q보다 점 A에 가깝다.)"),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="AB=6 → AM=1, QB=2, MP=1 → 3. 빠른정답 1과 불일치.")

# p79
add(id="9066e6ae", qtype="choice",
    question=("다음 그림에서 점 M은 [[seg(AB)]]의 중점, 점 N은 [[seg(MB)]]의 중점일 때, □ 안에 들어갈 알맞은 수를 차례대로 나열한 것은?\n"
              "(1) [[seg(MB) = frac(1,2) seg(AB) = frac(1,2) × 16]] = □(cm)\n"
              "(2) [[seg(MN) = frac(1,2) seg(MB)]] = [[frac(1,2)]] × □ = □(cm)"),
    choices=["4, 8, 4", "4, 16, 8", "8, 4, 2", "8, 8, 4", "8, 16, 8"],
    derived_answer="④",
    figure=U("선분 AB(길이 16cm 표시) 위에 왼쪽부터 A, M, N, B"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "선분 위 중점 도형(AB=16cm가 그림에만 있음)",
    note="MB=8, MN=(1/2)×8=4 → 8, 8, 4 → ④. 빠른정답 4 ✓.")

# p83
add(id="3c6dced5", qtype="choice",
    question="아래 그림에서 점 M은 [[seg(AB)]]의 중점이고 점 N은 [[seg(MB)]]의 중점일 때, 다음 중 옳은 것은?",
    choices=["[[frac(1,2) seg(AM) = seg(AB)]]", "[[seg(AM) = seg(NB)]]", "[[seg(AB) = 5 seg(MN)]]",
             "[[3 seg(MN) = seg(MB)]]", "[[seg(AN) = 3 seg(NB)]]"],
    derived_answer="⑤",
    figure=U("선분 AB 위에 왼쪽부터 A, M, N, B"),
    difficulty_est=1, confidence=0.85,
    note="AB=4 → AM=2, MN=NB=1, AN=3 → ⑤. 빠른정답 '4cm'과 불일치.")

# p86
add(id="521dd82d", qtype="short",
    question="선분 AB의 중점이 M이고, [[seg(AM) = 2x - 2]], [[seg(BM) = 5x - 11]]일 때, [[seg(AB)]]의 길이를 구하시오.",
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="2x−2=5x−11 → x=3, AM=4, AB=8. 빠른정답 5와 불일치.")

# p90
add(id="c62b6a72", qtype="short",
    question=("다음 그림과 같이 7개의 점 A, B, C, D, L, M, N이 한 직선 위에 있고 세 점 L, M, N은 각각 [[seg(AB)]], [[seg(BC)]], "
              "[[seg(CD)]]의 중점이다. [[seg(BC) = 4 seg(AB)]], [[seg(CD) = 2 seg(BC)]], [[seg(LM) = 10]] cm일 때, "
              "[[seg(CN)]]의 길이를 구하시오."),
    choices=None, derived_answer="16 cm",
    figure=U("수평 직선 위에 왼쪽부터 A, L, B, M, C, N, D. LM=10cm 표시"),
    difficulty_est=2, confidence=0.85,
    note="AB=a → LM=a/2+2a=10, a=4; CN=CD/2=4a=16 cm. 빠른정답 4와 불일치.")

# p91
add(id="b866a847", qtype="short",
    question=("다음 그림에서 [[seg(AB) = frac(1,6) seg(AC)]], [[seg(DE) = frac(1,5) seg(CD)]]일 때, "
              "[[seg(BD)]]의 길이는 [[seg(AE)]]의 길이의 몇 배인지 구하시오."),
    choices=None, derived_answer="frac(5,6)",
    figure=U("수평 직선 위에 왼쪽부터 A, B, C, D, E"),
    difficulty_est=2, confidence=0.85,
    note="AC=6a, CD=5b → BD=5a+5b, AE=6a+6b → 5/6배. 빠른정답 없음.")

# p92
add(id="fe872137", qtype="short",
    question=("다음 그림에서 [[seg(AB) = frac(1,5) seg(AC)]], [[seg(DE) = frac(1,4) seg(CD)]]일 때, "
              "[[seg(BD)]]의 길이는 [[seg(AE)]]의 길이의 몇 배인지 구하시오."),
    choices=None, derived_answer="frac(4,5)",
    figure=U("수평 직선 위에 왼쪽부터 A, B, C, D, E"),
    difficulty_est=2, confidence=0.85,
    note="AC=5a, CD=4b → BD=4a+4b, AE=5a+5b → 4/5배. 빠른정답 없음.")

# p93
add(id="31e5e480", qtype="short",
    question=("다음 그림에서 [[3 seg(AD) = 2 seg(DB)]], [[seg(BC) = 2 seg(BE)]]이고 [[seg(AB) = 15]] cm, [[seg(DE) = 24]] cm일 때, "
              "[[seg(EC)]]의 길이를 구하시오."),
    choices=None, derived_answer="15 cm",
    figure=U("수평 직선 위에 왼쪽부터 A, D, B, E, C. AB=15cm, DE=24cm 표시"),
    difficulty_est=2, confidence=0.85,
    note="AD=6, DB=9, BE=15, BC=30 → EC=15 cm. 빠른정답 '15cm' ✓.")

# p94
add(id="c8c95344", qtype="short",
    question=("길이가 [[42]] cm인 선분 AB 위에 [[seg(AE) = 2 seg(EB)]]인 점 E를 잡고 [[seg(AB)]]의 연장선 위에 [[seg(AC) = 2 seg(BC)]]인 "
              "점 C를 잡았다. [[seg(AB)]]의 중점을 D, [[seg(EC)]]의 중점을 F라 할 때, [[seg(DF)]]의 길이를 구하시오."),
    choices=None, derived_answer="35 cm", figure=None, difficulty_est=3, confidence=0.9,
    note="A=0, B=42, E=28, C=84, D=21, F=56 → DF=35 cm. 빠른정답 '35cm' ✓.")

# p96
add(id="ded8d758", qtype="short",
    question=("다음 그림과 같이 두 직선 도로 위에 8개의 가게 A ~ H가 있다. 이때 주어진 조건을 이용하여 현정이가 자주 가는 단골 가게를 고르시오.\n"
              "(가) 현정이의 단골 가게는 [[line(CD)]] 위에 있다.\n"
              "(나) [[seg(AC)]], [[seg(AD)]], [[seg(BE)]]의 중점에는 각각 가게 B, C, D가 있다.\n"
              "(다) 현정이의 단골 가게에서 가게 E까지의 거리는 현정이의 단골 가게에서 가게 A까지의 거리의 [[frac(5,2)]]배이다."),
    choices=None, derived_answer="C",
    figure=U("지도 삽화: 가로 도로 위에 왼쪽부터 가게 A, B, C, D, E; C를 지나는 비스듬한 도로 위에 위쪽으로 G, F, 아래쪽으로 H"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "두 직선 도로 위 가게 8개 배치 그림",
    note="B=1 → C=2, D=4, E=7; 위치 x에서 7−x=(5/2)x → x=2 → 가게 C. 빠른정답 C ✓.")

# p99 — 한 이미지에 두 문항 (draft_a 대응: de02e11c=위 문항, 18566e8f=아래 문항)
add(id="de02e11c", qtype="short",
    question=("다음 그림에서 두 점 M, N은 각각 [[seg(AB)]], [[seg(BC)]]의 중점이고, [[ratio(seg(AB), seg(BC)) = ratio(4, 3)]]이다. "
              "[[seg(MN) = 14]] cm일 때, [[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="12 cm",
    figure=U("수평 직선 위에 왼쪽부터 A, M, B, N, C. MN=14cm 표시"),
    difficulty_est=2, confidence=0.85,
    note="p99 위 문항. AB=4a, BC=3a → MN=3.5a=14, a=4 → BC=12 cm. 빠른정답 C(다른 문항 값)와 불일치.")

add(id="18566e8f", qtype="short",
    question=("다음 그림에서 점 L, M, N은 각각 [[seg(AB)]], [[seg(BC)]], [[seg(CD)]]의 중점이다. "
              "[[ratio(seg(AB), seg(BC), seg(CD)) = ratio(1, 2, 3)]]이고 [[seg(LM) = 3]] cm일 때, [[seg(AD)]]의 길이를 구하시오."),
    choices=None, derived_answer="12 cm",
    figure=U("수평 직선 위에 왼쪽부터 A, L, B, M, C, N, D. LM=3cm 표시"),
    difficulty_est=2, confidence=0.85,
    note="p99 아래 문항. AB=a → LM=a/2+a=3, a=2 → AD=6a=12 cm. 빠른정답 C(다른 문항 값)와 불일치.")

# ======================= 구의 겉넓이와 부피 =======================
# p10 — 같은 이미지에 id 3개(문항은 1개)
dup(["5705f008", "4110a7b6", "0609ea24"], qtype="choice",
    question=("다음 그림과 같은 구에 대하여 □ 안에 알맞은 수를 차례로 쓴 것은?\n"
              "(반지름의 길이) = [[r]] = □ (cm)\n"
              "(겉넓이) = □ (cm²)"),
    choices=["[[10]], [[100 pi]]", "[[10]], [[200 pi]]", "[[10]], [[400 pi]]", "[[20]], [[200 pi]]", "[[20]], [[400 pi]]"],
    derived_answer="③",
    figure=U("구(지름 20cm 표시)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "구 그림(지름 20cm가 그림에만 있음)",
    note="같은 이미지 id 3개, 한 문항. r=10, 겉넓이 4π×100=400π → ③. 빠른정답 '29통'과 불일치.")

# p11
add(id="ccefaae3", qtype="choice",
    question="다음 그림과 같이 반지름의 길이가 [[7]] cm인 구의 겉넓이는?",
    choices=["[[49 pi]] cm²", "[[70 pi]] cm²", "[[88 pi]] cm²", "[[98 pi]] cm²", "[[196 pi]] cm²"],
    derived_answer="⑤",
    figure=U("구(반지름 7cm 표시)"),
    difficulty_est=1, confidence=0.85,
    note="4π×49=196π → ⑤. 빠른정답 '39통'과 불일치.")

# p22
add(id="524c97c5", qtype="short",
    question="다음 □ 안에 알맞은 것을 써넣으시오.\n반지름의 길이가 [[r]]인 구의 부피는 □ × [[pi]] × [[pow(r,3)]]이다.",
    choices=None, derived_answer="frac(4,3)", figure=None, difficulty_est=1, confidence=0.9,
    note="구의 부피 (4/3)πr³. 빠른정답 frac(4,3) ✓.")

# ======================= 삼각형의 작도 =======================
# p11
add(id="6e47e2f5", qtype="choice",
    question="다음 그림에서 직선 [[l]] 위에 [[2 seg(AB) = seg(CD)]]인 두 점 C, D를 작도하는 데 사용되는 것은?",
    choices=["컴퍼스", "눈금이 없는 자", "삼각자", "눈금이 있는 자", "각도기"],
    derived_answer="①",
    figure=U("위쪽에 선분 AB, 아래쪽에 직선 l 위의 두 점 C, D"),
    difficulty_est=1, confidence=0.85,
    note="길이 옮기기 → 컴퍼스 ①. 빠른정답 없음.")

# p14
add(id="3a478017", qtype="choice",
    question=("다음과 같이 직선 [[l]] 위의 두 점 A, B가 있다. [[seg(AB) = seg(BC)]]가 되도록 하는 점 C를 작도하려 할 때, "
              "사용하는 작도 도구는?"),
    choices=["눈금 있는 자", "눈금 없는 자", "컴퍼스", "삼각자", "각도기"],
    derived_answer="③",
    figure=U("수평 직선 l 위의 두 점 A, B"),
    difficulty_est=1, confidence=0.85,
    note="길이 옮기기 → 컴퍼스 ③. 빠른정답 없음.")

# p17
add(id="5ca8c4c9", qtype="choice",
    question="아래 그림은 [[angle(XOY)]]와 크기가 같은 각을 선분 AB 위에 작도하는 과정이다. 다음 중 옳지 않은 것은?",
    choices=["[[seg(OC) = seg(OD)]]", "[[seg(CD) = seg(EF)]]", "[[seg(OC) = seg(AF)]]", "[[seg(OC) = seg(CD)]]",
             "[[angle(COD) = angle(EAF)]]"],
    derived_answer="④",
    figure=U("왼쪽: ∠XOY, O 중심 호(ㄴ)가 OX·OY와 만나는 점 C·D, C 중심 호(ㄱ). 화살표. 오른콝: 선분 AB, A 중심 호(ㄷ)가 AB와 만나는 점 F, 호 ㄷ과 F 중심 호(ㄹ)의 교점 E, 반직선 AE(ㅁ)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "크기가 같은 각의 작도 과정 도형",
    note="OC=OD=AE=AF, CD=EF; OC=CD는 근거 없음 → ④. 빠른정답 없음.")

# p19
add(id="4ee976fa", qtype="choice",
    question="아래 그림은 [[angle(XOY)]]의 이등분선을 작도한 것이다. 다음 중 옳지 않은 것을 모두 고르면? (정답 2개)",
    choices=["[[seg(OA) = seg(OB)]]", "[[seg(OP) = seg(OY)]]", "[[seg(OX) = seg(OY)]]", "[[seg(PA) = seg(PB)]]",
             "[[angle(AOB) = 2 angle(AOP)]]"],
    derived_answer="②, ③",
    figure=U("∠XOY(O 왼쪽, X 오른쪽 위, Y 오른쪽). O 중심 호가 OX·OY와 만나는 점 A·B, A·B 중심 호의 교점 P, 반직선 OP"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "각의 이등분선 작도 도형",
    note="OA=OB, PA=PB, OP는 이등분선; OP=OY, OX=OY는 근거 없음 → ②, ③. 빠른정답 없음.")

# p20
add(id="fb9e7492", qtype="choice",
    question="아래 그림은 [[angle(AOB)]]와 같은 [[angle(QPR)]]의 작도 과정을 나타낸 것이다. 다음 중 옳지 않은 것은?",
    choices=["[[seg(OA) = seg(PQ)]]", "[[seg(AB) = seg(QR)]]", "[[angle(AOB) = angle(QPR)]]", "[[seg(PR) = seg(QR)]]",
             "[[angle(OAB) = angle(PQR)]]"],
    derived_answer="④",
    figure=U("왼쪽: ∠AOB(O 왼쪽), O 중심 호가 OA·OB와 만나는 점 A·B, A 근처 호 표시 ①·③. 화살표. 오른쪽: ∠QPR(P 왼쪽), P 중심 호가 만나는 점 Q·R, Q 근처 호 표시 ②·④·⑤"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "크기가 같은 각의 작도 과정 도형",
    note="OA=OB=PQ=PR, AB=QR → 두 삼각형 합동; PR=QR은 근거 없음 → ④. 빠른정답 없음.")

# p26
add(id="cc44b062", qtype="choice",
    question="아래 그림은 크기가 [[deg(90)]]인 [[angle(XOY)]]의 삼등분선을 작도하는 과정이다. 다음 중 옳지 않은 것은?",
    choices=["작도 순서는 ㄱ→ㄴ→ㄷ이다.", "[[seg(OB) = seg(OA)]]", "[[seg(BP) = seg(QA)]]", "[[angle(BOP) = deg(30)]]",
             "[[angle(POQ) = deg(30)]]"],
    derived_answer="①",
    figure=U("직각 ∠XOY(O 왼쪽 아래, Y 위, X 오른쪽). O 중심 호(ㄴ)가 OY·OX와 만나는 점 B·A, B 중심 호와 A 중심 호(ㄱ)가 호 ㄴ과 만나는 점 P·Q, 반직선 OP·OQ(ㄷ)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각의 삼등분선 작도 도형",
    note="순서는 ㄴ→ㄱ→ㄷ이므로 ① 거짓. 빠른정답 없음.")

# p38
add(id="017b4d51", qtype="choice",
    question=("아래 그림은 직선 [[l]] 위에 있지 않은 한 점 P를 지나고 직선 [[l]]과 평행한 직선 [[m]]을 작도한 것이다. "
              "다음 중 옳지 않은 것은?"),
    choices=["[[angle(PAB) = angle(QPA)]]", "[[seg(AP) = seg(PQ)]]", "[[seg(AP) = seg(BP)]]", "[[seg(AP) = seg(AB)]]",
             "[[seg(PB) = seg(QA)]]"],
    derived_answer="③",
    figure=U("아래 수평 직선 l 위의 점 B(왼쪽)·A(오른쪽), 위 수평 직선 m 위의 점 P(왼쪽)·Q(오른쪽). A 중심 호(B·P 지남), P 중심 호와 Q 중심 호의 교점 Q 근처 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "평행선 작도(엇각) 도형",
    note="AB=AP=PQ, BP=QA, 엇각 같음; AP=BP는 근거 없음 → ③. 빠른정답 6과 불일치.")

# p40
add(id="191d7460", qtype="choice",
    question=("아래 그림은 직선 [[l]] 위에 있지 않은 한 점 P를 지나고 직선 [[l]]과 평행한 직선 [[m]]을 작도한 것이다. "
              "다음 중 옳지 않은 것은?"),
    choices=["[[seg(PC) = seg(PD)]]", "[[seg(AB) = seg(CD)]]", "[[seg(QA) = seg(QB)]]", "[[angle(AQB) = angle(CPD)]]",
             "[[angle(AQB) = angle(QAB)]]"],
    derived_answer="⑤",
    figure=U("아래 수평 직선 l과 위 수평 직선 m, 두 직선을 지나는 비스듬한 직선. l과의 교점 Q, m과의 교점 P. Q 중심 호가 직선·l과 만나는 점 A·B, P 중심 호가 만나는 점 C·D, C 중심 호로 D 결정"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "평행선 작도(동위각) 도형",
    note="QA=QB=PC=PD, AB=CD, ∠AQB=∠CPD; ∠AQB=∠QAB는 근거 없음 → ⑤. 빠른정답 없음.")

# p44
add(id="8d81e69b", qtype="choice",
    question=("다음 그림은 직선 [[l]] 밖의 한 점 P를 지나고, 직선 [[l]]에 평행한 직선을 작도한 것이다. 다음 중 옳지 않은 것은?"),
    choices=["[[seg(AB) = seg(CD)]]", "[[seg(DP) = seg(DC)]]", "[[seg(QA) = seg(QB)]]", "[[seg(DP) = seg(PC)]]",
             "[[angle(CPD) = angle(AQB)]]"],
    derived_answer="②",
    figure=U("아래 수평 직선 l과 위 수평 직선, 두 직선을 지나는 비스듬한 직선. l과의 교점 Q, 위 직선과의 교점 P. Q 중심 호가 만나는 점 A·B, P 중심 호가 만나는 점 C·D, C 중심 호로 D 결정"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "평행선 작도(동위각) 도형",
    note="DP=PC, AB=CD, QA=QB, ∠CPD=∠AQB; DP=DC는 근거 없음 → ②. 빠른정답 없음.")

# p51
add(id="deca2829", qtype="short",
    question="다음 그림의 삼각형 PQR에서 [[angle(R)]]의 대변의 길이를 구하시오.",
    choices=None, derived_answer="12 cm",
    figure=U("삼각형 PQR(P 오른쪽 위, Q 왼쪽, R 오른쪽 아래). PQ=12cm, QR=9cm, ∠R=79° 표시"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "삼각형 도형(변 12cm·9cm, ∠R=79°가 그림에만 있음)",
    note="∠R의 대변 PQ=12 cm. 빠른정답 없음.")

# p52
add(id="e747590c", qtype="short",
    question="다음 그림의 삼각형 DEF에서 [[angle(E)]]의 대변의 길이를 구하시오.",
    choices=None, derived_answer="8 cm",
    figure=U("삼각형 DEF(F 오른쪽 위, D 왼쪽, E 오른쪽 아래). DF=8cm, DE=7cm, ∠E=56° 표시"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "삼각형 도형(변 8cm·7cm, ∠E=56°가 그림에만 있음)",
    note="∠E의 대변 DF=8 cm. 빠른정답 없음.")

# p56
add(id="b88b62dc", qtype="choice",
    question="다음 그림의 [[tri(ABC)]]에서 [[angle(B)]]의 대변과 [[seg(BC)]]의 대각을 차례로 쓴 것은?",
    choices=["[[seg(AB)]], [[angle(A)]]", "[[seg(AB)]], [[angle(C)]]", "[[seg(AC)]], [[angle(A)]]",
             "[[seg(AC)]], [[angle(B)]]", "[[seg(BC)]], [[angle(A)]]"],
    derived_answer="③",
    figure=U("삼각형 ABC(A 왼쪽 위, B 오른쪽 위, C 오른쪽 아래)"),
    difficulty_est=1, confidence=0.85,
    note="∠B의 대변 AC, BC의 대각 ∠A → ③. 빠른정답 '7 cm'과 불일치.")

# p74
add(id="8e4ef6d5", qtype="choice",
    question=("두 변의 길이 [[a]], [[b]]와 [[angle(C)]]가 주어진 [[tri(ABC)]]를 아래 그림과 같이 작도하였다. 선분 [[a]]를 가장 먼저 "
              "작도하였을 때, 다음 보기에서 작도 순서를 바르게 나열한 것은?\n<보기>\n"
              "ㄱ. [[seg(AC) = b]]인 점 A를 잡는다.\n"
              "ㄴ. [[angle(C)]]의 크기를 작도한다.\n"
              "ㄷ. 점 A와 점 B를 잇는다."),
    choices=["ㄱ－ㄴ－ㄷ", "ㄱ－ㄷ－ㄴ", "ㄴ－ㄱ－ㄷ", "ㄴ－ㄷ－ㄱ", "ㄷ－ㄴ－ㄱ"],
    derived_answer="③",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래). BC=a, AC=b(점선 표시), ∠C 표시"),
    difficulty_est=2, confidence=0.85,
    note="a → ∠C → 점 A → AB 잇기: ㄴ－ㄱ－ㄷ → ③. 빠른정답 없음.")

# p77
add(id="3ca3ac0b", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 변 AB와 변 AC의 길이와 [[angle(A)]]의 크기가 주어졌을 때, "
              "[[tri(ABC)]]를 작도하는 과정에서 가장 마지막 순서에 해당하는 것은?"),
    choices=["[[seg(AB)]]를 긋는다.", "[[seg(AC)]]를 긋는다.", "[[angle(A)]]를 작도한다.", "[[seg(BC)]]를 긋는다.",
             "[[angle(C)]]를 작도한다."],
    derived_answer="④",
    figure=U("삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 위쪽), ∠A 표시"),
    difficulty_est=1, confidence=0.85,
    note="두 변과 끼인각 작도의 마지막은 BC 잇기 → ④. 빠른정답 없음.")

# p83
add(id="f3a0677d", qtype="choice",
    question="다음 중 [[tri(ABC)]]가 하나로 결정되는 것은?",
    choices=["[[seg(AB) = 10]] cm, [[seg(BC) = 4]] cm, [[seg(CA) = 6]] cm",
             "[[seg(AB) = 4]] cm, [[seg(BC) = 5]] cm, [[angle(C) = deg(45)]]",
             "[[seg(AB) = 7]] cm, [[seg(BC) = 4]] cm, [[angle(A) = deg(30)]]",
             "[[seg(BC) = 5]] cm, [[angle(B) = deg(70)]], [[angle(C) = deg(50)]]",
             "[[angle(A) = deg(30)]], [[angle(B) = deg(30)]], [[angle(C) = deg(120)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="①은 10=4+6, ②③은 끼인각 아님, ⑤는 각만 → ④. 빠른정답 없음.")

# p84
add(id="492d1aa7", qtype="choice",
    question="다음 중 [[tri(ABC)]]가 하나로 결정되는 것을 모두 고르면? (정답 2개)",
    choices=["[[seg(AB) = 6]] cm, [[seg(BC) = 5]] cm, [[angle(A) = deg(45)]]",
             "[[seg(AB) = 3]] cm, [[seg(BC) = 4]] cm, [[seg(AC) = 6]] cm",
             "[[seg(AB) = 3]] cm, [[seg(BC) = 4]] cm, [[angle(B) = deg(50)]]",
             "[[seg(AB) = 4]] cm, [[seg(BC) = 5]] cm, [[angle(C) = deg(45)]]",
             "[[angle(A) = deg(30)]], [[angle(B) = deg(40)]], [[angle(C) = deg(110)]]"],
    derived_answer="②, ③", figure=None, difficulty_est=2, confidence=0.9,
    note="② SSS(3+4>6), ③ 두 변과 끼인각 → ②, ③. 빠른정답 없음.")

# p85
add(id="afc98de4", qtype="choice",
    question="다음 중 [[tri(ABC)]]가 하나로 작도되는 것을 모두 고르면? (정답 2개)",
    choices=["[[angle(A) = deg(90)]], [[angle(B) = deg(60)]], [[angle(C) = deg(30)]]",
             "[[seg(BC) = 7]] cm, [[angle(B) = deg(120)]], [[angle(C) = deg(30)]]",
             "[[seg(AB) = 7]] cm, [[seg(BC) = 6]] cm, [[angle(A) = deg(40)]]",
             "[[seg(AB) = 4]] cm, [[seg(BC) = 6]] cm, [[seg(CA) = 10]] cm",
             "[[seg(AB) = 6]] cm, [[seg(BC) = 5]] cm, [[angle(B) = deg(80)]]"],
    derived_answer="②, ⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="② 한 변과 양 끝각, ⑤ 두 변과 끼인각 → ②, ⑤. ④는 4+6=10. 빠른정답 없음.")

# p87
add(id="f4b9229c", qtype="choice",
    question="다음 중 [[tri(ABC)]]가 하나로 정해지는 것은?",
    choices=["[[seg(AB) = 3]] cm, [[seg(BC) = 12]] cm, [[seg(CA) = 9]] cm",
             "[[seg(AB) = 4]] cm, [[seg(BC) = 3]] cm, [[angle(A) = deg(35)]]",
             "[[seg(BC) = 5]] cm, [[seg(AC) = 4]] cm, [[angle(B) = deg(50)]]",
             "[[seg(AC) = 6]] cm, [[angle(B) = deg(80)]], [[angle(C) = deg(40)]]",
             "[[angle(A) = deg(30)]], [[angle(B) = deg(60)]], [[angle(C) = deg(90)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="① 3+9=12, ②③ 끼인각 아님, ⑤ 각만; ④는 ∠A=60°로 한 변과 양 끝각 → ④. 빠른정답 없음.")

# p88
add(id="70976de8", qtype="choice",
    question="다음 중 [[tri(ABC)]]가 하나로 정해지는 것을 모두 고르면? (정답 2개)",
    choices=["[[seg(AB) = 11]] cm, [[seg(BC) = 4]] cm, [[seg(CA) = 9]] cm",
             "[[seg(BC) = 8]] cm, [[angle(B) = deg(65)]], [[angle(C) = deg(40)]]",
             "[[seg(AB) = 12]] cm, [[seg(BC) = 5]] cm, [[seg(CA) = 7]] cm",
             "[[angle(A) = deg(30)]], [[seg(AB) = 8]] cm, [[seg(BC) = 5]] cm",
             "[[angle(A) = deg(80)]], [[angle(B) = deg(40)]], [[angle(C) = deg(60)]]"],
    derived_answer="①, ②", figure=None, difficulty_est=2, confidence=0.9,
    note="① SSS(4+9>11), ② 한 변과 양 끝각; ③ 5+7=12, ④ 끼인각 아님, ⑤ 각만 → ①, ②. 빠른정답 없음.")

# p90
add(id="82af7ae8", qtype="choice",
    question=("[[seg(BC)]]의 길이가 주어졌을 때, [[tri(ABC)]]가 하나로 결정되기 위해 더 필요한 조건으로 옳은 것을 모두 고르면? "
              "(정답 2개)"),
    choices=["[[angle(A)]], [[angle(C)]]", "[[angle(A)]], [[seg(AC)]]", "[[angle(B)]], [[seg(AC)]]",
             "[[angle(C)]], [[seg(AB)]]", "[[seg(AB)]], [[seg(AC)]]"],
    derived_answer="①, ⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="① 두 각(∠B 결정)+한 변, ⑤ SSS; ②③④는 끼인각 아님 → ①, ⑤. 빠른정답 없음.")

# p93
add(id="af73ed3d", qtype="choice",
    question=("다음 보기 중 삼각형이 하나로 결정되는 조건이 아닌 것을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[seg(AB) = 2]], [[seg(BC) = 3]], [[seg(CA) = 7]]\n"
              "ㄴ. [[seg(AB) = 5]], [[seg(BC) = 4]], [[angle(B) = deg(50)]]\n"
              "ㄷ. [[seg(AC) = 8]], [[seg(BC) = 7]], [[angle(C) = deg(85)]]\n"
              "ㄹ. [[seg(AB) = 3]], [[angle(A) = deg(100)]], [[angle(B) = deg(90)]]\n"
              "ㅁ. [[seg(BC) = 2]], [[angle(A) = deg(1)]], [[angle(B) = deg(5)]]"),
    choices=["ㄱ, ㄴ", "ㄱ, ㄹ", "ㄴ, ㄹ", "ㄷ, ㅁ", "ㄹ, ㅁ"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄱ 2+3<7, ㄹ 100°+90°>180° → 결정 안 됨 → ②. 빠른정답 없음.")

# p95
add(id="3498d058", qtype="choice",
    question="다음 중 [[seg(AC) = 3]] cm일 때, 삼각형 ABC가 하나로 결정되지 않는 것은?",
    choices=["[[seg(AB) = 3]] cm, [[seg(BC) = 4]] cm", "[[seg(BC) = 4]] cm, [[angle(C) = deg(45)]]",
             "[[angle(B) = deg(30)]], [[angle(C) = deg(60)]]", "[[angle(A) = deg(75)]], [[seg(AB) = 3]] cm",
             "[[angle(A) = deg(75)]], [[angle(C) = deg(105)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="⑤ 75°+105°=180°로 삼각형 불가 → ⑤. 빠른정답 없음.")

# p97
add(id="b5a7c0cf", qtype="short",
    question=("[[angle(B) = deg(70)]], [[seg(BC) = 8]] cm, [[angle(C) = deg(130)]]로 주어진 [[tri(ABC)]]를 작도할 때, "
              "그려지는 삼각형의 개수를 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=1, confidence=0.9,
    note="70°+130°>180° → 0개. 빠른정답 없음.")

# ======================= 뿔의 겉넓이와 부피 =======================
# p58
add(id="e5d9c1f7", qtype="short",
    question=("다음 그림과 같이 [[seg(AD) = 8]] cm, [[seg(DH) = 6]] cm인 직육면체를 두 꼭짓점 D, G와 [[seg(BC)]]의 중점 M을 지나는 "
              "평면으로 자를 때 생기는 삼각뿔의 부피가 [[28]] cm³일 때, [[seg(AB)]]의 길이를 구하시오."),
    choices=None, derived_answer="7 cm",
    figure=U("직육면체 ABCD-EFGH(윗면 ABCD: A 뒤왼쪽·D 뒤오른쪽·B 앞왼쪽·C 앞오른쪽, 아랫면 EFGH 대응). BC의 중점 M, 절단면 삼각형 DMG, AD=8cm·DH=6cm 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직육면체 절단 도형",
    note="삼각뿔 C-DMG: (1/3)×(1/2×4×AB)×6=4AB=28 → AB=7 cm. 빠른정답 '7 cm' ✓.")

# ======================= 평행선의 성질 =======================
# p4
add(id="86910cc7", qtype="short",
    question="다음 그림에서 [[angle(b)]]의 동위각의 크기를 구하시오.",
    choices=None, derived_answer="deg(101)",
    figure=U("두 직선(평행 표시 없음)과 한 횡단선. 위 교점: 위오른쪽 94°, 위왼쪽 a, 아래왼쪽 b, 아래오른쪽 c. 아래 교점: 위왼쪽 79°, 위오른쪽 f, 아래왼쪽 d, 아래오른쪽 e"),
    difficulty_est=2, confidence=0.75,
    needs_review=FIG + "두 직선과 횡단선 각 표시 도형",
    note="∠b(아래왼쪽)의 동위각은 ∠d, ∠d=180°−79°=101°. 빠른정답 4와 불일치.")

# p6
add(id="231fba49", qtype="short",
    question="다음 그림에서 [[angle(a)]]의 동위각의 크기를 구하시오.",
    choices=None, derived_answer="deg(50)",
    figure=U("두 직선(평행 표시 없음)과 한 횡단선. 위 교점: 위왼쪽 100°, 위오른쪽 a, 아래왼쪽 c, 아래오른쪽 b. 아래 교점: 위왼쪽 e, 위오른쪽 d, 아래왼쪽 f, 아래오른쪽 130°"),
    difficulty_est=2, confidence=0.75,
    needs_review=FIG + "두 직선과 횡단선 각 표시 도형",
    note="∠a(위오른쪽)의 동위각은 ∠d, ∠d=180°−130°=50°. 빠른정답 deg(71)과 불일치.")

# p12
add(id="9d653358", qtype="short",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(120)",
    figure=U("평행한 두 수평선 l(위), m(아래)과 횡단선. l과의 교점 아래왼쪽에 x, m과의 교점 위오른쪽에 120°"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "평행선과 횡단선 각 표시 도형",
    note="엇각 → x=120°. 빠른정답 deg(120) ✓.")

# p13
add(id="0aca6149", qtype="short",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=U("평행한 두 수평선 l(위), m(아래)과 횡단선. l과의 교점 아래왼쪽에 x, m과의 교점 위오른쪽에 60°"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "평행선과 횡단선 각 표시 도형",
    note="엇각 → x=60°. 빠른정답 '동위각'과 불일치.")

# p16
add(id="fde4226c", qtype="choice",
    question="아래의 그림에서 [[par(l, m)]]일 때, 다음 중 나머지 넷과 크기가 다른 각은?",
    choices=["[[angle(a)]]", "[[angle(c)]]", "[[angle(e)]]", "[[angle(g)]]", "[[angle(h)]]"],
    derived_answer="⑤",
    figure=U("평행한 두 수평선 l(위), m(아래)과 횡단선 n. l 교점: 위왼쪽 b, 위오른쪽 a, 아래왼쪽 c, 아래오른쪽 d. m 교점: 위왼쪽 f, 위오른쪽 e, 아래왼쪽 g, 아래오른쪽 h"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "평행선과 횡단선 각 표시 도형",
    note="a=c=e=g(맞꼭지각·동위각), h는 보각 → ⑤. 빠른정답 deg(60)과 불일치.")

# p26
add(id="0bd1b20e", qtype="short",
    question="다음 두 직선 [[l]]과 [[m]]이 평행하기 위한 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(40)",
    figure=U("두 수평선 l(위), m(아래)과 횡단선. l과의 교점 아래오른쪽에 40°, m과의 교점 위왼쪽에 x"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "두 직선과 횡단선 각 표시 도형",
    note="엇각이 같아야 평행 → x=40°. 빠른정답 '1, 5'와 불일치.")

# p30
add(id="77d8b8a5", qtype="choice",
    question="다음 중 아래 그림에 대한 설명으로 옳지 않은 것은?",
    choices=["[[par(l, m)]]이면 [[angle(a) = angle(e)]]이다.", "[[angle(c) = angle(e)]]이면 [[par(l, m)]]이다.",
             "[[angle(d) = angle(f)]]이면 [[par(l, m)]]이다.", "[[par(l, m)]]이면 [[angle(b) + angle(f) = deg(180)]]이다.",
             "[[angle(c) + angle(h) = deg(180)]]이면 [[par(l, m)]]이다."],
    derived_answer="④",
    figure=U("두 수평선 l(위), m(아래)과 횡단선. l 교점: 위왼쪽 a, 위오른쪽 d, 아래왼쪽 b, 아래오른쪽 c. m 교점: 위왼쪽 e, 위오른쪽 h, 아래왼쪽 f, 아래오른쪽 g"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "두 직선과 횡단선 각 표시 도형",
    note="b와 f는 동위각(같음)이므로 합이 180°일 이유 없음 → ④. 빠른정답 1과 불일치.")

# p31
add(id="f2f17230", qtype="short",
    question="다음 그림에서 [[par(l, m)]], [[par(p, q)]]일 때, [[angle(x) - angle(y)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(120)",
    figure=U("두 쌍의 평행선 l∥m(오른쪽 위로 올라감), p∥q(오른쪽 아래로 내려감)이 평행사변형을 이룸. m과 p의 교점 위쪽 각 150°, l과 q의 교점(왼쪽) 아래쪽 각 x, m과 q의 교점(아래) 오른쪽 각 y"),
    difficulty_est=2, confidence=0.75,
    needs_review=FIG + "두 쌍의 평행선 각 표시 도형",
    note="x=150°(맞꼭지·동위각), y=30° → x−y=120°. 빠른정답 2와 불일치.")

# p32
add(id="ade1f970", qtype="short",
    question="다음 그림에서 [[par(l, m)]], [[par(p, q)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(75)",
    figure=U("수평선 l(위)·m(아래), 오른쪽 위로 기울어진 p(왼쪽)·q(오른쪽). l과 p의 교점 아래왼쪽 75°, m과 q의 교점 위오른쪽 x"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "두 쌍의 평행선 각 표시 도형",
    note="75°의 맞꼭지각을 동위각으로 옮기면 x=75°. 빠른정답 '3, 4'와 불일치.")

# p34
add(id="54207739", qtype="short",
    question="다음 그림에서 [[par(l, m)]], [[par(p, q)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(105)",
    figure=U("수평선 l(위)·m(아래), 오른쪽 아래로 기울어진 p(왼쪽)·q(오른쪽). l과 p의 교점 아래왼쪽 105°, m과 q의 교점 아래왼쪽 x"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "두 쌍의 평행선 각 표시 도형",
    note="같은 위치의 각(동위각 두 번) → x=105°. 빠른정답 deg(120)과 불일치.")

# p35
add(id="c2c02604", qtype="short",
    question="다음 그림에서 [[par(k, l)]], [[par(m, n)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(10)",
    figure=U("살짝 오른쪽 위로 기울어진 k(위)·l(아래), 급하게 오른쪽 위로 기울어진 m(왼쪽)·n(오른쪽). k와 m의 교점 아래왼쪽 5x, l과 n의 교점 위왼쪽 13x"),
    difficulty_est=2, confidence=0.75,
    needs_review=FIG + "두 쌍의 평행선 각 표시 도형",
    note="13x=180°−5x → x=10°. 빠른정답 deg(75)와 불일치.")
