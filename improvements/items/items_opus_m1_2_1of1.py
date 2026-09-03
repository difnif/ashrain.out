# -*- coding: utf-8 -*-
# esc_opus_m1-2_1of1 — 이미지 기준 전사 (5 항목 / 5쪽). 전부 정보성 기하 도형 → unsupported + needs_review
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ---------------- 각 p30 (평각을 네 각으로 나눈 도형)
add(id="faea537d", qtype="short",
    question=("다음 그림에서\n"
              "[[ratio(angle(x), angle(y)) = ratio(angle(y), angle(z)) = ratio(angle(z), angle(w)) = ratio(3, 4)]]일 때,\n"
              "[[2 angle(x) - angle(y) + 2 angle(z) - angle(w)]]의 크기를 구하시오.\n"
              "(단, 단위는 생략한다.)"),
    choices=None, derived_answer="frac(360,7)",
    figure=[{"fn": "unsupported", "args": {"raw": "직선 위의 한 점에서 위쪽으로 세 반직선이 나와 평각을 네 각으로 나눔. 왼쪽부터 차례로 ∠x, ∠y, ∠z, ∠w 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평각을 네 각 x, y, z, w로 나눈 도형",
    note="x:y:z:w=27:36:48:64, 합 180 → 단위각 36/35. 2x−y+2z−w=50×36/35=360/7 = 빠른정답 ✓.")

# ---------------- 평행선의 성질 p56 (평행선 사이 꺾인 선, 각의 삼등분)
add(id="5d9408b3", qtype="short",
    question=("다음 그림에서 [[par(l, m)]]이고\n"
              "[[angle(EAF) = angle(FAG) = angle(GAC)]],\n"
              "[[angle(EBF) = angle(FBG) = angle(GBD)]], [[angle(AGB) = deg(38)]]일 때,\n"
              "[[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(190)",
    figure=[{"fn": "unsupported", "args": {"raw": "평행한 두 수평선 l(위, 점 A·C)·m(아래, 점 B·D). A와 B에서 각각 세 선분이 나와 안쪽 꼭짓점 E, F, G(왼쪽부터)에서 만남. A에서 ∠EAF=∠FAG=∠GAC(• 3개), B에서 ∠EBF=∠FBG=∠GBD(× 3개). ∠AEB=x, ∠AFB=y, ∠AGB=38°"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선 사이 꺾인 선 복합 도형",
    note="∠GAC=a, ∠GBD=b ⇒ a+b=38°, y=2(a+b)=76°, x=3(a+b)=114° → x+y=190°. 빠른정답 60°와 불일치.")

# ---------------- 평행선의 성질 p89 (평면거울 반사, 12°·20°)
_MIRROR_Q = ("일정한 방향으로 진행하는 빛이 평면거울에 닿아 반사될 때 생기는 입사각과 반사각의 크기는 항상 같다. "
             "다음 그림에서 [[par(l, m)]]이고 빛이 직선 [[l]]에 수직으로 들어가서 직선 [[l]]과 이루는 각의 크기가 [[deg({a})]]인 평면거울과 "
             "직선 [[m]]과 이루는 각의 크기가 [[deg({b})]]인 평면거울에 연이어 반사된다고 한다. 이때 [[angle(x)]]의 크기를 구하시오.\n"
             "(단, 평면거울의 두께는 무시한다.)")
def _mirror_fig(a, b):
    return [{"fn": "unsupported", "args": {"raw": f"평행한 두 수직선 m(왼쪽)·l(오른쪽). 점 A에서 오른쪽으로 l에 수직하게 들어온 빛이 l 위의 점 G에서 거울 HE(l과 {a}°, H 좌상·E 우하)에 반사되어 m 위의 점 C로, C에서 거울 BD(m과 {b}°, B 좌상·D 우하)에 반사되어 거울 HE 위의 점 F로 진행한 뒤 F에서 다시 반사. x는 F에서 선분 FG(거울 위쪽)와 광선 FC 사이의 각. 진행 방향 화살표 표시"}}]

add(id="dd729147", qtype="short", question=_MIRROR_Q.format(a=12, b=20),
    choices=None, derived_answer="deg(94)", figure=_mirror_fig(12, 20),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 평행선+두 평면거울+광선 경로 복합 도형",
    note="G 반사 후 광선은 수평과 24°, C 반사(거울 20°) 후 수평과 16° → F에서 광선 FC와 거울 FE가 이루는 각 86°, x=∠GFC=180°−86°=94°. 빠른정답 87°와 불일치.")

# ---------------- 평행선의 성질 p90 (평면거울 반사, 24°·30°)
add(id="6847e1be", qtype="short", question=_MIRROR_Q.format(a=24, b=30),
    choices=None, derived_answer="deg(78)", figure=_mirror_fig(24, 30),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 평행선+두 평면거울+광선 경로 복합 도형",
    note="G 반사 후 수평과 48°, C 반사(거울 30°) 후 수평과 12° → F에서 ∠GFC=78°(거울과 이루는 각 102°). 빠른정답 180°와 불일치.")

# ---------------- 부채꼴의 호의 길이와 넓이 p66 (원 안의 두 원, 색칠 부분)
add(id="11965fe5", qtype="choice",
    question=("다음 그림과 같이 원 O의 지름 BC 위에 두 원 O′, O″의 중심이 있다. [[seg(BC) = 16]] cm이고 "
              "[[angle(AOB) = angle(COD) = deg(45)]]일 때, 색칠한 부분의 넓이는?"),
    choices=["[[8(pi - 3)]] cm²", "[[10(pi - 4)]] cm²", "[[12(pi - 2)]] cm²", "[[14(pi - 4)]] cm²", "[[16(pi - 2)]] cm²"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "중심 O, 지름 BC(수평, B 왼쪽·C 오른쪽)인 큰 원. BO·OC를 지름으로 하는 두 작은 원(중심 O′, O″). 큰 원 위의 점 A(좌상)·D(우상), ∠AOB=∠COD=45°. 색칠: 부채꼴 AOB·COD에서 작은 원 바깥 부분과, 반직선 OA·OD와 작은 원 호 사이의 활꼴(O 근처 잎 모양)"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 원 안의 두 원+색칠 영역 복합 도형 / 프라임 라벨 O′, O″는 텍스트",
    note="반지름 8·4. 한쪽 색칠 = (부채꼴 8π − (4π+8)) + 활꼴 (4π−8) = 8π−16, 양쪽 16π−32=16(π−2) → ⑤. 빠른정답 3과 불일치(색칠 영역 해석에 따라 달라질 수 있음).")
