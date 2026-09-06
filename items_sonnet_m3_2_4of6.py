# -*- coding: utf-8 -*-
# esc_sonnet_m3-2_4of6 — 이미지 기준 전사 (82 항목 / 80쪽)
# 원에 내접하는 사각형 p34~p96, 원의 접선과 현이 이루는 각 p1~p90: 전부 정보성 기하 도형(원·각 표시) → unsupported + needs_review
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))
def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
def D5(*a): return [f"[[deg({x})]]" for x in a]
FIG = "도형 표현 불가: "
PR = " / 프라임 점 라벨"

# ======================= 원에 내접하는 사각형 =======================
# ---------------- p34
add(id="55d2dc65", qtype="short",
    question=("다음 그림과 같이 사각형 ABCD가 원에 내접하고 [[angle(DAC) = deg(32)]], [[angle(DCA) = deg(28)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(120)",
    figure=U("원에 내접하는 사각형 ABCD(A 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC. B에서 왼쪽으로 CB의 연장선(직선). "
             "∠DAC=32°(A), ∠DCA=28°(C), ∠x는 B에서 BA와 CB의 연장선 사이의 외각"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+내접사각형+외각 도형",
    note="∠ADC=180−32−28=120 → 외각 ∠x=∠ADC=120°. 빠른정답 2와 불일치.")

# ---------------- p35
add(id="d39147d2", qtype="short",
    question=("다음 그림에서 [[arc(ABC)]]의 길이는 원주의 [[frac(3,5)]], [[arc(BCD)]]의 길이는 원주의 [[frac(1,6)]]일 때, "
              "[[angle(ADC) + angle(DCE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(138)",
    figure=U("원 위의 점 A(위), B(왼쪽 아래), C(아래), D(오른쪽 아래). 선분 AB, AD, BC, CD. C에서 BC의 연장선 위 점 E(오른쪽, • 표시)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+내접사각형+외각 도형",
    note="∠ADC=½·(3/5·360)=108, ∠DCE=∠BAD=½·(1/6·360)=30 → 138°. 빠른정답 2와 불일치.")

# ---------------- p36
add(id="9fce198d", qtype="short",
    question="다음 그림에서 [[angle(DCE)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(100)",
    figure=U("원에 내접하는 사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC·BD. ∠DAC=35°(A), ∠BDC=65°(D). "
             "BC의 연장선 위 점 E(C 오른쪽, • 표시), ∠DCE 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+내접사각형+대각선+외각 도형",
    note="∠BAC=∠BDC=65 → ∠BAD=100 → 외각 ∠DCE=∠BAD=100°. 빠른정답 2와 불일치.")

# ---------------- p37
add(id="3e1f9181", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]가 원 O에 내접하고 [[angle(BAD) = deg(86)]]일 때, "
              "[[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(274)",
    figure=U("원 O에 내접하는 □ABCD(A 왼쪽 위, D 오른쪽 위, B·C 아래). 반지름 OB, OD. ∠BAD=86°(A). "
             "∠y는 O에서 OB·OD 사이 A쪽(우각) 표시, ∠x는 C에서 CD와 BC의 연장선(E 방향) 사이의 외각"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+내접사각형+중심각+외각 도형",
    note="∠x=∠BAD=86, ∠y=360−2·86=188 → 274° = 빠른정답 ✓.")

# ---------------- p42
add(id="8ccb514d", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 원에 내접하고 [[angle(BPC) = deg(23)]], [[angle(BQA) = deg(35)]], "
              "[[angle(ABC) = deg(x)]]일 때, [[angle(x)]]의 크기를 구하시오. (단, 단위는 생략한다.)"),
    choices=None, derived_answer="61",
    figure=U("원에 내접하는 □ABCD. 직선 BA와 CD의 연장선이 P(위)에서, 직선 BC와 AD의 연장선이 Q(오른쪽)에서 만남. "
             "∠BPC=23°(P), ∠BQA=35°(Q), ∠ABC=x(B)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+내접사각형+두 연장선 교점 도형",
    note="∠PCB=157−x, ∠QAB=145−x, 내접 조건 (145−x)+(157−x)... → 2x=122, x=61. 빠른정답 7과 불일치.")

# ---------------- p43
add(id="c7c79622", qtype="choice",
    question=("다음 그림에서 [[quad(EBCF)]]는 원에 내접하고 [[angle(BAC) = deg(40)]], [[angle(BCA) = deg(40)]]일 때, "
              "[[angle(x)]]의 크기는?"),
    choices=D5(45, 50, 55, 60, 65), derived_answer="④",
    figure=U("원 위의 네 점 E, B, C, F. △ABC(A 위, B 아래, C 오른쪽 아래), E는 AB 위, F는 AC 위. "
             "직선 D-E-F와 직선 D-B-C가 D(왼쪽 아래)에서 만남. ∠BAC=40°, ∠BCA=40°, ∠x=∠EDB"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+삼각형+내접사각형 도형",
    note="∠ABC=100 → ∠EFC=80 → ∠AFE=100 → ∠AEF=40=∠DEB, ∠DBE=80 → x=60 → ④. 빠른정답 5와 불일치.")

# ---------------- p45
add(id="fc297d30", qtype="choice",
    question="다음 [[quad(ABCD)]]가 원에 내접할 때, [[angle(x)]]의 크기는?",
    choices=D5(50, 52, 54, 56, 58), derived_answer="③",
    figure=U("원에 내접하는 □ABCD. 직선 BA와 CD의 연장선이 F(위)에서, 직선 BC와 AD의 연장선이 E(오른쪽)에서 만남. "
             "∠F=32°, ∠E=40°, ∠x=∠ABC"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+내접사각형+두 연장선 교점 도형",
    note="x=(180−32−40)/2=54 → ③. 빠른정답 61과 불일치.")

# ---------------- p47
add(id="5f7e8c03", qtype="short",
    question=("다음 그림에서 사각형 ABCD가 원에 내접하고 [[angle(BPC) = deg(40)]], [[angle(AQB) = deg(36)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(52)",
    figure=U("원에 내접하는 사각형 ABCD. 직선 BA와 CD의 연장선이 P(위)에서, 직선 BC와 AD의 연장선이 Q(오른쪽)에서 만남. "
             "∠BPC=40°, ∠AQB=36°, ∠x=∠ABC"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+내접사각형+두 연장선 교점 도형",
    note="x=(180−40−36)/2=52 = 빠른정답 ✓.")

# ---------------- p51
add(id="d807e7b8", qtype="choice",
    question=("다음 그림과 같이 원 O에 내접하는 칠각형 ABCDEFG에서 [[seg(AB) = seg(BC) = seg(CD)]], "
              "[[angle(AGF) = deg(135)]], [[angle(DEF) = deg(117)]]일 때, [[angle(x)]]의 크기는?"),
    choices=D5(45, 46, 47, 48, 49), derived_answer="④",
    figure=U("원 O에 내접하는 칠각형 ABCDEFG(A 위, 시계 방향으로 G, F, E, D, C, B). AB=BC=CD(같은 길이 표시). "
             "반지름 OC, OD, ∠x=∠COD. ∠AGF=135°, ∠DEF=117°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+내접칠각형+중심각 도형",
    note="호 ABCDEF=270, 호 DCBAGF=234 → 6a+(360−3a)=504, a=48 → ④ = 빠른정답 ✓.")

# ---------------- p55
add(id="f8f1c00e", qtype="choice",
    question=("다음 그림과 같이 원 O에 내접하는 육각형 ABCDEF에서 [[angle(D) = deg(150)]], [[angle(F) = deg(95)]]일 때, "
              "[[angle(AOC)]]의 크기는?"),
    choices=D5(100, 110, 120, 130, 140), derived_answer="④",
    figure=U("원 O에 내접하는 육각형 ABCDEF(F 위, A 왼쪽 위, B 왼쪽 아래, C 아래, D 오른쪽 아래, E 오른쪽). "
             "반지름 OA, OC, ∠AOC 표시(B쪽). ∠F=95°, ∠D=150°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+내접육각형+중심각 도형",
    note="호 CBAFE=300, 호 EDCBA=190 → 호 AB+BC=130 → ∠AOC=130 → ④. 빠른정답 5와 불일치.")

# ---------------- p56
add(id="4a194a90", qtype="short",
    question="다음 그림에서 [[angle(ABC) = deg(135)]]이고 [[angle(AED) = deg(110)]]라 할 때, [[angle(CAD)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(65)",
    figure=U("원 위의 점 A(위), B(왼쪽 위), C(왼쪽), D(아래), E(오른쪽). 선분 AB, BC, AC, AD, AE, ED. ∠ABC=135°, ∠AED=110°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+내접오각형 도형",
    note="호 ABC=90, 호 AED=140 → 호 CD=130 → ∠CAD=65°. 빠른정답 3과 불일치.")

# ---------------- p57
add(id="bc9f0d62", qtype="short",
    question=("다음 그림과 같이 오각형 ABCDE가 원 O에 내접하고 [[angle(A) = deg(80)]], [[angle(D) = deg(130)]]일 때, "
              "[[angle(BOC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=U("원 O에 내접하는 오각형 ABCDE(A 왼쪽 위, E 오른쪽 위, D 오른쪽, C 오른쪽 아래, B 왼쪽 아래). 반지름 OB, OC, ∠BOC 표시. "
             "∠A=80°, ∠D=130°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+내접오각형+중심각 도형",
    note="호 EDCB=160, 호 CBAE=260 → 호 BC=60 → 60° = 빠른정답 ✓.")

# ---------------- p59
add(id="75da7277", qtype="short",
    question=("다음 그림의 오각형 ABCDE가 중심이 O인 원에 내접하고 [[angle(B) = deg(117)]], [[angle(COD) = deg(84)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(105)",
    figure=U("오각형 ABCDE(A 왼쪽 위, E 오른쪽 위, D 오른쪽, C 아래, B 왼쪽; 원은 그려져 있지 않음). 내부의 점 O에서 OC, OD. "
             "∠B=117°, ∠COD=84°, ∠x=∠E"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "오각형+중심각 도형",
    note="호 CDEA=234, 호 CD=84 → 호 DE+EA=150 → ∠E=½(360−150)=105°. 빠른정답 65와 불일치.")

# ---------------- p60
add(id="a8712d14", qtype="short",
    question=("다음 그림과 같이 오각형 ABCDE가 원 O에 내접하고 [[angle(COD) = deg(60)]]일 때, "
              "[[angle(B) + angle(E)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(210)",
    figure=U("원 O에 내접하는 오각형 ABCDE(A 위, B 왼쪽, C 왼쪽 아래, D 오른쪽 아래, E 오른쪽). 반지름 OC, OD, ∠COD=60°. ∠B, ∠E 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+내접오각형+중심각 도형",
    note="∠B+∠E=½(360+60)=210°. 빠른정답 60과 불일치.")

# ---------------- p61
add(id="9bcf7bc1", qtype="short",
    question=("다음 그림과 같이 오각형 ABCDE가 원 O에 내접하고 [[angle(COD) = deg(100)]]일 때, "
              "[[angle(B) + angle(E)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(230)",
    figure=U("원 O에 내접하는 오각형 ABCDE(A 위, B 왼쪽, C 왼쪽 아래, D 오른쪽 아래, E 오른쪽 위). 중심(• 표시)에서 OC, OD, ∠COD=100°. ∠B, ∠E 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+내접오각형+중심각 도형",
    note="∠B+∠E=½(360+100)=230° = 빠른정답 ✓.")

# ---------------- p64 (O′)
add(id="595aa80d", qtype="short",
    question="다음 그림의 두 원 O, O′에서 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(87)",
    figure=U("두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 직선 A-P-D(위), 직선 B-Q-C-R(아래). 선분 AB, DC. "
             "∠x=∠ABQ(B), ∠PDC=92°(D), ∠DCR=87°(C 외각)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+내접사각형 2개 도형" + PR,
    note="∠PQC=88, ∠DPQ=87 → ∠APQ=93 → x=180−93=87°. 빠른정답 230과 불일치.")

# ---------------- p65 (O′)
add(id="516ff14a", qtype="choice",
    question=("다음 그림에서 두 점 P, Q는 두 원 O, O′의 교점이다. [[angle(BAP) = deg(100)]]일 때, "
              "∠PDC + ∠PO′C의 크기는?"),
    choices=D5(220, 225, 230, 235, 240), derived_answer="⑤",
    figure=U("두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 직선 A-P-D(위), 선분 AB, BQ, QC, CD. "
             "∠BAP=100°(A), O′에서 O′P, O′C와 ∠PO′C 표시(Q쪽)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+내접사각형 2개+중심각 도형" + PR,
    note="∠PQC=100 → ∠PDC=80, ∠PO′C=160 → 240 → ⑤. 빠른정답 218과 불일치.")

# ---------------- p66 (O′)
add(id="761ba37e", qtype="short",
    question=("다음 그림과 같이 두 원 O, O′이 두 점 P, Q에서 만나고 [[angle(PDC) = deg(100)]]일 때, "
              "[[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(260)",
    figure=U("두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 선분 AB, AP, PD, DC, BQ, QC, PQ. 반지름 OB, OP. "
             "∠x=∠BOP(O, Q쪽 표시), ∠y=∠PQB(Q), ∠PDC=100°(D)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+내접사각형 2개+중심각 도형" + PR,
    note="∠PQC=80 → y=100, ∠BAP=80 → x=∠BOP=160 → 260°. 빠른정답 120과 불일치.")

# ---------------- p68 (O′)
add(id="4bcc5ade", qtype="choice",
    question=("다음 그림에서 두 원 O, O′이 두 점 P, Q에서 만날 때, 두 점 P, Q를 지나는 직선이 두 원 O, O′과 만나는 점을 "
              "A, B, C, D라 하자. [[angle(A) = deg(92)]]일 때, ∠PO′C의 크기는?"),
    choices=D5(172, 173, 174, 175, 176), derived_answer="⑤",
    figure=U("두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 직선 A-P-D(위), B-Q-C(아래), 선분 AB, DC. "
             "∠A=92°, O′에서 O′P, O′C와 ∠PO′C 표시(Q쪽)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+내접사각형 2개+중심각 도형" + PR,
    note="∠PQC=92 → ∠PDC=88 → ∠PO′C=176 → ⑤ = 빠른정답 ✓. (원문 문장 그대로 전사)")

# ---------------- p69 (O′)
add(id="5c7181a9", qtype="choice",
    question=("다음 그림에서 두 점 P, Q는 두 원 O, O′의 교점이다. [[angle(BAP) = deg(95)]]일 때, "
              "∠PDC + ∠PO′C의 크기는?"),
    choices=D5(240, 245, 250, 255, 260), derived_answer="④",
    figure=U("두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 직선 A-P-D(위), 선분 AB, BQ, QC, CD. "
             "∠BAP=95°(A), ∠D 표시, O′에서 O′P, O′C와 ∠PO′C 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+내접사각형 2개+중심각 도형" + PR,
    note="∠PQC=95 → ∠PDC=85, ∠PO′C=170 → 255 → ④. 빠른정답 260과 불일치.")

# ---------------- p70
add(id="2f2d5ec2", qtype="choice",
    question=("다음 그림에서 두 원은 두 점 C, D에서 만난다. 한 원의 두 현 AD, BC의 연장선의 교점을 P, 다른 원과 만나는 점을 "
              "각각 E, F라 하면 [[angle(EFC) = deg(105)]], [[angle(BAD) = deg(115)]]일 때, [[angle(P)]]의 크기는?"),
    choices=D5(5, 7.5, 10, 12.5, 15), derived_answer="③",
    figure=U("두 원이 두 점 C, D에서 만남(왼쪽 원에 A, B, C, D; 오른쪽 원에 D, C, F, E). 점 P(왼쪽 멀리)에서 두 직선 P-A-D-E, P-B-C-F. "
             "선분 AB, EF. ∠BAD=115°(A), ∠EFC=105°(F), ∠P 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+두 할선 도형",
    note="∠BCD=65 → ∠DCF=115 → ∠DEF=65 → ∠P=180−65−105=10 → ③. 빠른정답 2와 불일치.")

# ---------------- p71
add(id="7a32a431", qtype="choice",
    question="다음 그림에서 [[angle(DBP)]]의 크기는?",
    choices=D5(80, 75, 70, 65, 60), derived_answer="⑤",
    figure=U("큰 원(중심 O)과 작은 원(중심도 O로 표기)이 두 점 P(아래), Q(오른쪽 위)에서 만남. 직선 B-P-A(아래), 직선 D-Q-C(위). "
             "선분 BD(큰 원의 현), 선분 AC(작은 원의 현). ∠PAC=120°(A)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+내접사각형 2개 도형",
    note="∠PQC=60 → ∠DQP=120 → ∠DBP=60 → ⑤ = 빠른정답 ✓. 그림의 두 중심이 모두 O로 표기됨.")

# ---------------- p73 (O₁ O₂ O₃)
add(id="ad6ba70b", qtype="choice",
    question=("다음 그림과 같이 두 원 [[sub(O,1)]], [[sub(O,2)]]는 두 점 P, Q에서 만나고 두 원 [[sub(O,1)]], [[sub(O,3)]]는 "
              "두 점 Q, R에서 만난다.\n[[ratio(angle(PAR), angle(RED)) = ratio(5,7)]], [[angle(EDQ) = angle(RED) - deg(20)]]일 때, "
              "[[angle(x)]]의 크기는?"),
    choices=D5(94, 95, 96, 97, 98), derived_answer="②",
    figure=U("원 O₁(위 왼쪽, 큰 원)에 A, P, Q, R; 원 O₂(아래, 작은 원)에 P, B, C, Q; 원 O₃(오른쪽)에 R, E, D, Q. "
             "직선 A-P-B, 직선 A-R-E, 직선 R-Q-C, 직선 D-Q-P. 선분 BC, ED. ∠x=∠QCB(C)"),
    difficulty_est=4, confidence=0.75, needs_review=FIG + "세 원+내접사각형 3개 도형",
    note="∠PAR=5k, ∠RED=7k; D,Q,P 한 직선 → (180−7k)+(180−5k)=180, k=15 → x=200−7k=95 → ② = 빠른정답 ✓.")

# ---------------- p87 (선지가 그림)
add(id="b6c36ca8", qtype="choice",
    question="다음 [[quad(ABCD)]] 중 원에 내접하지 않는 것은?",
    choices=["(그림) [[angle(A) = deg(120)]], [[angle(C) = deg(60)]]인 □ABCD",
             "(그림) 대각선 AC를 그은 □ABCD, [[angle(BAC) = deg(50)]], [[angle(ADC) = deg(110)]], [[angle(ACB) = deg(50)]]",
             "(그림) 대각선 AC, BD를 그은 □ABCD, [[angle(ADB) = deg(43)]], [[angle(ACB) = deg(43)]]",
             "(그림) 대각선 AC, BD를 그은 □ABCD, [[angle(BAC) = deg(50)]], [[angle(BDC) = deg(50)]]",
             "(그림) □ABCD, A에서의 외각(BA의 연장선과 AD 사이) [[deg(80)]], C에서의 외각(BC의 연장선과 CD 사이) [[deg(100)]]"],
    derived_answer="②",
    figure=U("선지 ①~⑤ 각각 사각형 ABCD 그림: ① ∠A=120°, ∠C=60°; ② 대각선 AC, ∠BAC=50°, ∠ADC=110°, ∠ACB=50°; "
             "③ 대각선 AC·BD, ∠ADB=43°, ∠ACB=43°; ④ 대각선 AC·BD, ∠BAC=50°, ∠BDC=50°; ⑤ A의 외각 80°, C의 외각 100°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "선지 5개가 각 표시된 사각형 그림(선지는 그림 설명으로 전사)",
    note="② ∠B=80, ∠D=110 → 합 190≠180 → 내접 안 함 → ② = 빠른정답 ✓. 나머지는 내접(①③④⑤).")

# ---------------- p94
add(id="bcce2e46", qtype="short",
    question="다음 그림에서 [[quad(ABCD)]]가 원에 내접하도록 하는 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(72)",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 아래). BC의 연장선(C 오른쪽). ∠A=72°, ∠B=106°, "
             "∠x는 C에서 CD와 BC의 연장선 사이의 외각"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사각형+외각 도형",
    note="내접 조건: 외각 ∠x=∠A=72°. 빠른정답 120과 불일치.")

# ---------------- p96
add(id="4e3b2424", qtype="short",
    question="다음 그림에서 [[quad(ABCD)]]가 원에 내접하도록 하는 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(113)",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래). BC의 연장선(C 오른쪽). ∠A=113°, ∠D=119°, "
             "∠x는 C에서 CD와 BC의 연장선 사이의 외각"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사각형+외각 도형",
    note="내접 조건: 외각 ∠x=∠A=113°. 빠른정답 81과 불일치.")

# ======================= 원의 접선과 현이 이루는 각 =======================
# ---------------- p1 (TT′)
add(id="e01ff95d", qtype="choice",
    question=("다음 그림에서 직선 TT′은 원의 접선이고 점 B는 접점이다. [[arc(AB) = 3 arc(BC)]]이고 [[angle(ABT) = deg(60)]]일 때, "
              "[[angle(CAB)]]의 크기는?"),
    choices=D5(16, 17, 18, 19, 20), derived_answer="⑤",
    figure=U("원, 아래쪽 접선 T-B-T′(B 접점, T 왼쪽, T′ 오른쪽). 원 위의 점 A(왼쪽 위), C(오른쪽 아래). 현 AB, AC, BC. "
             "∠ABT=60°(B 왼쪽), ∠CAB 표시(A)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+삼각형 도형" + PR,
    note="∠ACB=∠ABT=60 → 호 AB=120, 호 BC=40 → ∠CAB=20 → ⑤ = 빠른정답 ✓.")

# ---------------- p2
add(id="9c693d4a", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB)]]를 지름으로 하는 원 O에서 [[angle(OCP) = angle(ODP) = deg(10)]], [[angle(AOC) = deg(70)]]일 때, "
              "[[angle(DOB)]]의 크기는?"),
    choices=D5(30, 35, 40, 45, 50), derived_answer="⑤",
    figure=U("지름 AB(A 왼쪽, B 오른쪽) 위에 중심 O와 점 P(O 오른쪽)가 있는 반원. 호 위의 점 C(왼쪽 위), D(오른쪽 위). "
             "선분 OC, OD, CP, DP. ∠OCP=10°, ∠ODP=10°, ∠AOC=70°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "반원+삼각형 2개 도형",
    note="∠COP=110 → ∠OPC=60 → ∠OPD=120 → ∠DOP=50 → ⑤ = 빠른정답 ✓.")

# ---------------- p3
add(id="06fcdd63", qtype="short",
    question=("다음 그림과 같이 [[seg(AB)]]를 지름으로 하는 반원 O에서 [[angle(OCP) = angle(ODP) = deg(15)]], [[angle(AOC) = deg(65)]]일 때, "
              "[[angle(DOB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(35)",
    figure=U("지름 AB(A 왼쪽, B 오른쪽) 위에 중심 O와 점 P(O 오른쪽)가 있는 반원. 호 위의 점 C(왼쪽 위), D(오른쪽 위). "
             "선분 OC, OD, CP, DP. ∠OCP=15°, ∠ODP=15°, ∠AOC=65°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "반원+삼각형 2개 도형",
    note="∠COP=115 → ∠OPC=50 → ∠OPD=130 → ∠DOB=35° = 빠른정답 ✓.")

# ---------------- p4
add(id="25e6ef1b", qtype="short",
    question="다음 그림에서 직선 AT가 원 O의 접선이고 점 A가 그 접점이다. [[angle(ABC) = deg(98)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(98)",
    figure=U("원 O, 아래쪽 접선(접점 A, T는 A 오른쪽). 원 위의 점 C(위), B(오른쪽). 현 AC, AB, BC. ∠ABC=98°(B), "
             "∠x는 A에서 접선의 왼쪽 부분과 AC 사이"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+삼각형 도형",
    note="접선과 현이 이루는 각: x=∠ABC=98°. 빠른정답 5와 불일치.")

# ---------------- p8
add(id="45bd7b2d", qtype="short",
    question=("다음 그림과 같이 중심이 점 C이고 [[seg(MN)]]을 지름으로 하는 반원이 있다. 반원 위에 세 점 A, B, P에 대하여 "
              "[[angle(CAP) = angle(CBP) = deg(14)]], [[angle(MCA) = deg(50)]]일 때, [[angle(BCP)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(22)",
    figure=U("지름 MN(M 왼쪽, N 오른쪽) 위에 중심 C와 점 P(C 오른쪽)가 있는 반원. 호 위의 점 A(왼쪽 위), B(오른쪽). "
             "선분 CA, CB, AP, BP. ∠CAP=14°, ∠CBP=14°, ∠MCA=50°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "반원+삼각형 2개 도형",
    note="∠ACP=130 → ∠APC=36 → ∠BPC=144 → ∠BCP=22°. 빠른정답 3과 불일치.")

# ---------------- p9
add(id="bb1d02c7", qtype="short",
    question=("다음 그림에서 [[line(CT)]]는 원 O의 접선이고 [[ratio(arc(AB), arc(BC), arc(CA)) = ratio(2,3,4)]]일 때, "
              "[[angle(ACT)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(80)",
    figure=U("원 O, 원 위의 점 A(위), B(왼쪽), C(아래). 현 AB, BC, CA. C에서의 접선(직선), T는 C 오른쪽 위"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+삼각형 도형",
    note="호 CA=160 → ∠ACT=∠ABC=80°. 빠른정답 50과 불일치.")

# ---------------- p11 (id 3개) [2019년 3월 고1 21번/4점]
_p11 = dict(qtype="choice",
    question=("그림과 같이 점 O를 중심으로 하고 반지름의 길이가 각각 1, 3인 두 원 [[sub(O,1)]], [[sub(O,2)]]가 있다. "
              "원 [[sub(O,2)]] 위의 한 점 A에서 원 [[sub(O,1)]]에 그은 두 접선이 원 [[sub(O,2)]]와 만나는 점 중에서 A가 아닌 점을 "
              "각각 B, C라 하자. 또 점 C에서 원 [[sub(O,2)]]에 접하는 직선이 직선 AB와 만나는 점을 P라 하자. "
              "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[seg(AB) = 4 sqrt(2)]]\nㄴ. [[ratio(seg(AP), seg(CP)) = ratio(5,3)]]\nㄷ. [[seg(BP) = frac(16 sqrt(2), 5)]]"),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="③",
    figure=U("중심 O인 두 원 O₁(작은 원), O₂(큰 원). 큰 원 위의 점 A(왼쪽)에서 작은 원에 그은 두 접선이 큰 원과 B(오른쪽, 직선 A-B 수평), "
             "C(오른쪽 위)에서 만남. C에서 큰 원에 접하는 직선이 직선 AB와 P(오른쪽)에서 만남"),
    difficulty_est=4, confidence=0.85, needs_review=FIG + "두 동심원+접선 3개 도형",
    note="출처 [2019년 3월 고1 21번/4점]. AB=2√(9−1)=4√2 ㄱ✓; BC=8√2/3 → PA:PC=3:2 ㄴ✗; PB=16√2/5 ㄷ✓ → ③ = 빠른정답 ✓.")
dup(["3cfe2e9e", "af96aa56", "a683e972"], **_p11)

# ---------------- p12
add(id="3df17998", qtype="short",
    question="다음 그림에서 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(40)",
    figure=U("원, 아래쪽 접선(접점 A, T는 A 오른쪽). 원 위의 점 C(왼쪽 위), B(오른쪽). 현 AB, AC, BC. ∠BAT=40°(A), ∠x=∠ACB(C)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "원+접선+삼각형 도형",
    note="x=∠BAT=40° = 빠른정답 ✓.")

# ---------------- p13
add(id="f145d17c", qtype="short",
    question="다음 그림에서 직선 AT는 원의 접선이고 점 A는 접점일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(72)",
    figure=U("원, 아래쪽 접선(접점 A, T는 A 오른쪽). 원 위의 점 B(오른쪽 위), C(왼쪽). 현 AB, AC, BC. ∠ABC=37°(B), ∠ACB=72°(C), ∠x=∠BAT(A)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "원+접선+삼각형 도형",
    note="x=∠ACB=72°. 빠른정답 66과 불일치.")

# ---------------- p14
add(id="957144b2", qtype="choice",
    question=("다음 그림과 같이 점 P에서 원에 접하는 직선과 현 AB의 연장선의 교점을 T라 하자. [[seg(PT) = seg(PB)]]이고 "
              "[[angle(PTA) = deg(44)]]일 때, [[angle(PAB)]]의 크기는?"),
    choices=D5(76, 80, 84, 88, 92), derived_answer="④",
    figure=U("원, 원 위의 점 P(위), A(아래), B(오른쪽 아래). P에서의 접선과 직선 B-A의 연장선이 T(왼쪽)에서 만남. "
             "선분 PA, PB. PT=PB(같은 길이 표시), ∠PTA=44°(T), ∠PAB 표시(A)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+할선 도형",
    note="∠PBT=44=∠TPA → ∠PAB=44+44=88 → ④. 빠른정답 3과 불일치.")

# ---------------- p15
add(id="3530b9bf", qtype="short",
    question="다음 그림에서 직선 PT가 원의 접선이고 점 P는 접점일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(117)",
    figure=U("원, 위쪽 접선(접점 P, T는 P 왼쪽). 원 위의 점 B(오른쪽 위), A(오른쪽 아래). 현 PA, PB, AB. ∠TPA=117°(P), ∠x=∠PBA(B)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+삼각형 도형",
    note="x=∠TPA=117°. 빠른정답 40과 불일치.")

# ---------------- p16 (TT′)
add(id="f1dc9f5c", qtype="short",
    question="다음 그림에서 직선 TT′이 원의 접선이고 점 B가 그 접점이다. [[angle(CBT) = deg(60)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(120)",
    figure=U("원 O, 아래쪽 접선 T-B-T′(B 접점, T 왼쪽, T′ 오른쪽). 원 위의 점 A(왼쪽 위), C(오른쪽 위). 현 AB, AC, BC. 반지름 OB, OC. "
             "60°는 B에서 BC와 BT′ 사이에 표시, ∠x=∠BOC(O)"),
    difficulty_est=2, confidence=0.75, needs_review=FIG + "원+접선+삼각형+중심각 도형" + PR,
    note="원문은 ∠CBT=60°이나 그림상 BC와 BT′ 사이 60° → ∠OBC=30 → x=120°. 빠른정답 72와 불일치.")

# ---------------- p17
add(id="d0e47510", qtype="short",
    question="다음 그림에서 직선 AT는 원 O의 접선이고 점 A는 접점이다. [[angle(AOB) = deg(66)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(33)",
    figure=U("원 O, 아래쪽 접선(접점 A, T는 A 오른쪽). 원 위의 점 B(오른쪽). 반지름 OA, OB, 현 AB. ∠AOB=66°, ∠x=∠BAT(A)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "원+접선+중심각 도형",
    note="x=½∠AOB=33° = 빠른정답 ✓.")

# ---------------- p20 (TT′)
add(id="8026f55d", qtype="short",
    question="다음 그림에서 직선 TT′이 원 O의 접선이고 점 P가 접점일 때, [[angle(CBP)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(15)",
    figure=U("원 O, 위쪽 접선 T-P-T′(P 접점). 원 위의 점 C(왼쪽 위), A(오른쪽 위), B(왼쪽 아래). 선분 PA, PB, BC, BA, OA, OC. "
             "∠APT′=25°, ∠AOC=80°(O), ∠x=∠CBP(B)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+중심각+원주각 도형" + PR,
    note="∠ABP=∠APT′=25, ∠ABC=½·80=40 → ∠CBP=40−25=15°. 빠른정답 33과 불일치.")

# ---------------- p22 (TT′)
add(id="30728dbc", qtype="choice",
    question=("다음 그림에서 직선 TT′은 원 O의 접선이고 점 A는 접점이다. [[angle(BOC) = deg(144)]], ∠BAT′ = [[deg(72)]]일 때, "
              "[[angle(ABC)]]의 크기는?"),
    choices=D5(33, 34, 35, 36, 37), derived_answer="④",
    figure=U("원 O, 아래쪽 접선 T-A-T′(A 접점). 원 위의 점 B(오른쪽 위), C(왼쪽). 현 AB, AC, BC, 반지름 OB, OC. ∠BOC=144°(O), ∠BAT′=72°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+중심각+삼각형 도형" + PR,
    note="∠BAC=72, ∠ACB=∠BAT′=72 → ∠ABC=36 → ④. 빠른정답 52와 불일치.")

# ---------------- p25 (TT′)
add(id="a2c7ddff", qtype="choice",
    question=("다음 그림에서 직선 TT′은 원 O의 접선이고 점 A는 접점이다. [[angle(BOC) = deg(142)]], ∠BAT′ = [[deg(70)]]일 때, "
              "[[angle(ABC)]]의 크기는?"),
    choices=D5(39, 40, 41, 42, 43), derived_answer="①",
    figure=U("원 O, 아래쪽 접선 T-A-T′(A 접점). 원 위의 점 B(오른쪽 위), C(왼쪽). 현 AB, AC, BC, 반지름 OB, OC. ∠BOC=142°(O), ∠BAT′=70°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+중심각+삼각형 도형" + PR,
    note="∠BAC=71, ∠ACB=70 → ∠ABC=39 → ①. 빠른정답 4와 불일치.")

# ---------------- p27
add(id="cfedddfe", qtype="short",
    question="다음 그림에서 직선 AT는 원 O의 접선이고 점 A는 접점이다. [[angle(AOB) = deg(80)]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="40",
    figure=U("원 O, 아래쪽 접선(접점 A, T는 A 오른쪽). 원 위의 점 B(오른쪽). 반지름 OA, OB, 현 AB. ∠AOB=80°, A에서 AB와 AT 사이 x°"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "원+접선+중심각 도형",
    note="x=½·80=40 = 빠른정답 ✓.")

# ---------------- p29
add(id="cc13658f", qtype="short",
    question="다음 그림에서 직선 BD는 원 O의 접선이고 [[angle(CBD) = deg(60)]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="120",
    figure=U("원 O, 아래쪽 접선(접점 B, D는 B 오른쪽). 원 위의 점 A(왼쪽 위), C(오른쪽 위). 현 AB, AC, BC, 반지름 OB, OC. "
             "∠CBD=60°(B), O에서 OB와 OC 사이 x°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+삼각형+중심각 도형",
    note="∠OBC=30, OB=OC → ∠BOC=120 → x=120. 빠른정답 165와 불일치.")

# ---------------- p30
add(id="46295718", qtype="short",
    question="다음 그림에서 직선 BD는 원 O의 접선이고 [[angle(CBD) = deg(72)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(18)",
    figure=U("원 O, 아래쪽 접선(접점 B, D는 B 오른쪽). 원 위의 점 A(왼쪽 위), C(오른쪽 위). 현 AB, AC, BC, 반지름 OB, OC. "
             "∠CBD=72°(B), ∠x는 C에서 CO와 CB 사이"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+삼각형+반지름 도형",
    note="∠OBC=90−72=18=∠OCB → x=18°. 빠른정답 40과 불일치.")

# ---------------- p32
add(id="64fc1e7b", qtype="short",
    question=("다음 그림에서 두 점 A, B는 점 P에서 원에 그은 두 접선의 접점이다. [[par(seg(AD), seg(PB))]]이고 [[angle(P) = deg(60)]]일 때, "
              "[[angle(BCD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(120)",
    figure=U("점 P(왼쪽)에서 원에 그은 두 접선(접점 A 위, B 아래). 원 위의 점 D(오른쪽), C(아래 B와 D 사이). 선분 AD, BD, BC, CD. "
             "AD∥PB(화살표 표시), ∠P=60°, ∠BCD 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+두 접선+내접사각형 도형",
    note="△PAB 정삼각형, ∠DAB=∠ABP=60 → ∠BCD=180−∠BAD=120°. 빠른정답 30과 불일치.")

# ---------------- p34
add(id="8f950213", qtype="short",
    question=("다음 그림에서 [[line(AT)]]는 접점 A를 지나는 원 O의 접선이고 [[quad(ADCB)]]가 원에 내접할 때, "
              "[[angle(ABC) = deg(82)]], [[angle(ATD) = deg(55)]]이다.\n이때 [[angle(CAD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(39)",
    figure=U("원 O, 아래쪽 접선(접점 A, T는 A 오른쪽). 원 위의 점 B(왼쪽), C(위), D(오른쪽). 현 AB, BC, CA, AD, CD. 직선 C-D-T. "
             "∠ABC=82°(B), ∠ATD=55°(T), ∠CAD 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+내접사각형+할선 도형",
    note="∠ADC=98 → ∠ADT=82 → ∠DAT=43=∠ACD → ∠CAD=180−98−43=39°. 빠른정답 115와 불일치.")

# ---------------- p36
add(id="a40cbfd9", qtype="choice",
    question=("다음 그림과 같이 [[quad(ABCD)]]는 원 O에 내접하고 [[seg(CD)]]의 연장선과 점 A에서의 접선의 교점을 P라 하자. "
              "[[angle(ABC) = deg(85)]], [[angle(APD) = deg(45)]]일 때, [[arc(CD)]]의 원주각의 크기는?"),
    choices=D5(30, 35, 40, 45, 50), derived_answer="②",
    figure=U("원 O에 내접하는 □ABCD(A 아래, B 오른쪽, C 위, D 왼쪽). A에서의 접선(수평)과 직선 C-D의 연장선이 P(왼쪽 아래)에서 만남. "
             "∠ABC=85°(B), ∠APD=45°(P)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+내접사각형+할선 도형",
    note="∠ADP=85 → ∠DAP=50=∠ACD → ∠CAD=180−95−50=35 → ②. 빠른정답 30과 불일치.")

# ---------------- p40
add(id="3499f8b7", qtype="choice",
    question="다음 그림에서 직선 [[l]]이 원 O의 접선일 때, [[angle(y) - angle(x)]]의 크기는?",
    choices=D5(40, 45, 50, 55, 60), derived_answer="④",
    figure=U("원(중심 • 표시), 아래쪽 접선 l(접점 B, T는 B 오른쪽). 원 위의 점 A(왼쪽), D(위), C(오른쪽). 현 AD, DC, AC, AB, BC. "
             "∠DAC=36°, ∠DCA=61°, ∠CBT=41°, ∠x=∠ACB(C), ∠y=∠ABC(B)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+내접사각형+대각선 도형",
    note="∠ADC=83 → y=97, ∠CAB=41 → x=42 → y−x=55 → ④. 빠른정답 58과 불일치.")

# ---------------- p41
add(id="abb67c8e", qtype="choice",
    question=("다음 그림에서 직선 BT는 원 O의 접선이고 점 B는 접점이다. [[seg(BC) = seg(CD)]]이고 [[angle(ABD) = deg(39)]], "
              "[[angle(CBD) = deg(33)]]일 때, [[angle(ABT)]]의 크기는?"),
    choices=D5(66, 69, 72, 75, 78), derived_answer="④",
    figure=U("원 O, 아래쪽 접선(접점 B, T는 B 왼쪽). 원 위의 점 A(왼쪽 위), D(오른쪽 위), C(오른쪽). 현 AB, AD, BD, BC, CD. "
             "BC=CD(같은 길이 표시), ∠ABD=39°, ∠CBD=33°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+내접사각형+대각선 도형",
    note="∠CDB=33, ∠ADC=180−72=108 → ∠ADB=75=∠ABT → ④ = 빠른정답 ✓.")

# ---------------- p42
add(id="9f888520", qtype="choice",
    question=("다음 그림에서 직선 BT는 원 O의 접선이고 점 B는 접점이다. [[seg(BC) = seg(CD)]]이고 [[angle(ABD) = deg(42)]], "
              "[[angle(CBD) = deg(36)]]일 때, [[angle(ABT)]]의 크기는?"),
    choices=D5(66, 69, 72, 75, 78), derived_answer="①",
    figure=U("원 O, 아래쪽 접선(접점 B, T는 B 왼쪽). 원 위의 점 A(왼쪽 위), D(위), C(오른쪽). 현 AB, AD, BD, BC, CD. "
             "BC=CD(같은 길이 표시), ∠ABD=42°, ∠CBD=36°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+내접사각형+대각선 도형",
    note="∠CDB=36, ∠ADC=180−78=102 → ∠ADB=66=∠ABT → ①. 빠른정답 2와 불일치.")

# ---------------- p43
add(id="a075f6e1", qtype="short",
    question=("다음 그림과 같이 [[quad(ABCD)]]는 원 O에 내접하고 직선 AT는 원 O의 접선이다. [[angle(BCD) = deg(117)]], "
              "[[ratio(arc(AB), arc(AD)) = ratio(8,5)]]일 때, [[angle(DAT)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(45)",
    figure=U("원 O에 내접하는 □ABCD(A 오른쪽 위, B 왼쪽, C 아래, D 오른쪽 아래). A에서의 접선(기울어진 직선), T는 A 오른쪽 아래. ∠BCD=117°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+내접사각형 도형",
    note="호 BAD=234, 호 AD=234·5/13=90 → ∠DAT=45°. 빠른정답 4와 불일치.")

# ---------------- p44
add(id="b0b4f935", qtype="short",
    question=("다음 그림과 같이 원에 내접하는 [[quad(ABCD)]]에서 [[seg(AB)]]의 연장선과 점 C를 접점으로 하는 접선의 교점을 P라 하자. "
              "[[seg(AB) = seg(AC)]]이고 [[angle(P) = deg(42)]]일 때, [[angle(ADC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(106)",
    figure=U("원에 내접하는 □ABCD(A 위, B 왼쪽, C 아래, D 오른쪽). 직선 A-B의 연장선과 C에서의 접선(수평)이 P(왼쪽 아래)에서 만남. "
             "대각선 AC, AB=AC(같은 길이 표시), ∠P=42°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+내접사각형+할선 도형",
    note="∠CAB=α: 42+α+(180+α)/2=180 → α=32 → ∠ABC=74 → ∠ADC=106°. 빠른정답 4와 불일치.")

# ---------------- p45
add(id="6b179895", qtype="short",
    question=("다음 그림과 같이 원에 내접하는 [[quad(ABCD)]]에서 [[seg(AB)]]의 연장선과 점 C를 접점으로 하는 접선의 교점을 P라 하자. "
              "[[seg(AB) = seg(AC)]]이고 [[angle(P) = deg(30)]]일 때, [[angle(ADC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(110)",
    figure=U("원에 내접하는 □ABCD(A 오른쪽 위, B 왼쪽, C 아래, D 오른쪽). 직선 A-B의 연장선과 C에서의 접선(수평)이 P(왼쪽 아래)에서 만남. "
             "대각선 AC, AB=AC(같은 길이 표시), ∠P=30°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+내접사각형+할선 도형",
    note="∠CAB=α: 30+α+(180+α)/2=180 → α=40 → ∠ABC=70 → ∠ADC=110°. 빠른정답 1과 불일치.")

# ---------------- p47
add(id="21dcdd22", qtype="short",
    question=("다음 그림에서 직선 EC는 네 점 A, B, C, D를 지나는 원 O의 접선이고 [[seg(BD)]]는 지름이다. [[seg(AC)]]와 [[seg(BD)]]의 교점을 "
              "P라 하면 [[par(seg(AD), seg(EC))]]이고 [[angle(BCE) = deg(26)]]일 때, [[angle(APD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(78)",
    figure=U("원 O, 아래쪽 접선 E-C(접점 C, E는 C 왼쪽, 오른쪽으로 화살표). 원 위의 점 A(왼쪽 위), D(오른쪽 위), B(왼쪽 아래). "
             "지름 BD(O 지남), 현 AC, AD, BC. AC와 BD의 교점 P. AD∥EC(화살표 표시), ∠BCE=26°, ∠APD 표시"),
    difficulty_est=4, confidence=0.8, needs_review=FIG + "원+접선+지름+현+평행 도형",
    note="호 BC=52, ∠DAC=∠ADC(AD∥EC)=64 → 호 AB=76, 호 AD=104 → ∠APD=½(104+52)=78° = 빠른정답 ✓.")

# ---------------- p48
add(id="2189fc8f", qtype="short",
    question=("다음 그림에서 직선 PB는 원 O의 접선이고 [[seg(AC)]]는 원 O의 지름이다. [[angle(ABT) = deg(70)]]일 때, "
              "[[angle(y) - angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(30)",
    figure=U("원 O, 아래쪽 접선 T-B-P(접점 B, T 왼쪽, P 오른쪽). 원 위의 점 A(왼쪽 위), C(오른쪽 아래), 지름 AC(O 지남). 현 AB, 선분 AP. "
             "∠ABT=70°, ∠x=∠BAC(A), ∠y=∠BPC(P)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+지름+삼각형 도형",
    note="∠ACB=70, ∠ABC=90 → x=20; ∠ABP=110 → y=50 → y−x=30°. 빠른정답 50과 불일치.")

# ---------------- p49
add(id="e0fa3a31", qtype="short",
    question=("다음 그림에서 직선 TE는 원 O의 접선이고 점 T는 그 접점일 때, [[par(seg(AC), seg(TE))]]이다. 원 O의 지름 AB와 [[seg(CT)]]의 "
              "교점을 D라 하면 [[angle(ADC) = deg(78)]]일 때, [[angle(ACD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(64)",
    figure=U("원 O, 아래쪽 접선 T-E(접점 T, E는 T 오른쪽, 화살표). 원 위의 점 A(왼쪽 위), C(오른쪽 위), B(오른쪽 아래). "
             "지름 AB(O 지남), 현 AC(화살표, TE와 평행), CT, TB. AB와 CT의 교점 D. ∠ADC=78°, ∠ACD 표시"),
    difficulty_est=4, confidence=0.8, needs_review=FIG + "원+접선+지름+현+평행 도형",
    note="∠ACT=∠CTE=α, 호 AT=2α; 90+α−호BC=78, 4α−호BC=180 → α=64°. 빠른정답 2와 불일치.")

# ---------------- p52 (TT′)
add(id="3f5a1067", qtype="choice",
    question="다음 그림에서 직선 TT′이 원 O의 접선이고, 점 P는 원의 접점일 때, [[angle(BPT)]]의 크기는?",
    choices=D5(40, 45, 50, 55, 60), derived_answer="②",
    figure=U("원 O, 위쪽 접선 T-P-T′(P 접점, T 왼쪽, T′ 오른쪽). 지름 BA(B 왼쪽, A 오른쪽, O 지남). 현 BP. ∠PBA=45°(B)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+지름 도형" + PR,
    note="∠BPA=90, ∠PAB=45 → ∠BPT=∠PAB=45 → ② = 빠른정답 ✓.")

# ---------------- p53
add(id="99f208f6", qtype="choice",
    question=("다음 그림에서 [[seg(AC)]]는 원 O의 지름이고 [[line(TB)]]는 접선이다. [[ratio(arc(AB), arc(BC)) = ratio(1,2)]]일 때, "
              "[[angle(ABT)]]의 크기는?"),
    choices=D5(25, 30, 35, 40, 45), derived_answer="②",
    figure=U("원 O, 아래쪽 접선(접점 B, T는 B 왼쪽). 원 위의 점 A(왼쪽 아래), C(오른쪽 위), 지름 AC(O 지남). 현 AB, BC"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+지름 도형",
    note="호 AB=60 → ∠ABT=30 → ②. 빠른정답 5와 불일치.")

# ---------------- p55
add(id="e75c9cfe", qtype="choice",
    question="다음 그림에서 직선 AT가 원 O의 접선일 때, [[angle(x)]]의 크기는?",
    choices=D5(25, 40, 55, 60, 65), derived_answer="⑤",
    figure=U("원 O, 아래쪽 접선(접점 A, T는 A 오른쪽). 원 위의 점 B(오른쪽 위), C(왼쪽 아래), 지름 BC(O 지남). 현 AB, AC. "
             "∠ABC=25°(B), ∠x=∠BAT(A)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+지름 도형",
    note="∠BAC=90 → ∠ACB=65=x → ⑤. 빠른정답 2와 불일치.")

# ---------------- p56
add(id="1ffc6077", qtype="short",
    question=("다음 그림과 같이 [[seg(AB)]]를 지름으로 하는 반원 위의 점 C에 대하여 [[angle(CAB) = deg(16)]]이다. 점 B에서 큰 반원과 "
              "내접하는 작은 반원에 대하여 [[seg(AC)]]는 작은 반원의 접선이고 점 P는 그 접점이다. 점 P에서 [[seg(AB)]]에 내린 수선의 "
              "발을 H라 할 때, [[angle(CHB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(53)",
    figure=U("지름 AB(A 왼쪽, B 오른쪽)인 큰 반원, B에서 내접하는 작은 반원(지름은 AB 위). 큰 반원 위의 점 C(오른쪽 위), "
             "선분 AC(작은 반원과 P에서 접함), CB. P에서 AB에 내린 수선의 발 H(직각 표시), 선분 CH. ∠CAB=16°"),
    difficulty_est=4, confidence=0.8, needs_review=FIG + "두 반원+접선+수선 도형",
    note="tan∠CHB=(1+sin16°)/cos16°=tan53° → 53°. 빠른정답 2와 불일치.")

# ---------------- p57
add(id="1cfc02b9", qtype="short",
    question=("다음 그림에서 [[seg(AB)]]는 반원 O의 지름이고 [[seg(AD)]]는 [[seg(BC)]]를 지름으로 하는 반원의 접선이다. "
              "[[angle(ABP) = deg(20)]]일 때, [[angle(PAB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(50)",
    figure=U("지름 AB(A 왼쪽, B 오른쪽, 중심 O)인 반원과 BC(C는 AB 위, A 쪽)를 지름으로 하는 작은 반원. 큰 반원 위의 점 D, "
             "선분 AD가 작은 반원과 P에서 접함. 선분 BP. ∠ABP=20°, ∠PAB 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 반원+접선 도형",
    note="∠APC=∠PBC=20, ∠CPB=90 → ∠APB=110 → ∠PAB=50° = 빠른정답 ✓.")

# ---------------- p58 (TT′)
add(id="1d1a17f0", qtype="short",
    question="다음 그림에서 직선 TT′이 원의 접선이고 점 B가 접점이다. ∠CBT′ = [[deg(61)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(29)",
    figure=U("원 O, 오른쪽의 기울어진 접선 T-B-T′(B 접점, T′ 위, T 아래). 원 위의 점 C(위), A(아래), 지름 CA(O 지남). 현 CB, AB. "
             "∠CBT′=61°, ∠x=∠ACB(C)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "원+접선+지름 도형" + PR,
    note="∠CAB=61, ∠CBA=90 → x=29°. 빠른정답 2와 불일치.")

# ---------------- p59
add(id="16152820", qtype="short",
    question=("다음 그림에서 직선 PC는 원 O의 접선이고 [[seg(AB)]]는 원 O의 지름이다. [[angle(ACT) = deg(58)]]일 때, "
              "[[angle(x) - angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(6)",
    figure=U("원 O, 아래쪽 접선 P-C-T(접점 C, P 왼쪽, T 오른쪽). 원 위의 점 A(오른쪽 위), B(왼쪽), 지름 AB(O 지남), 직선 P-B-A. 현 AC. "
             "∠ACT=58°, ∠x=∠BAC(A), ∠y=∠APC(P)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+접선+지름+할선 도형",
    note="∠ABC=58, ∠ACB=90 → x=32; ∠ACP=122 → y=26 → x−y=6°. 빠른정답 53과 불일치.")

# ---------------- p62
add(id="1d4d500c", qtype="choice",
    question=("다음 그림에서 원 O는 [[tri(ABC)]]의 외접원이고 [[seg(PC)]], [[seg(PD)]]는 원 O의 접선이다. 두 점 C, E가 접점이고 "
              "[[angle(DCE) = deg(22)]], [[angle(CDE) = deg(26)]]일 때, [[angle(x) + angle(y)]]의 크기는?"),
    choices=D5(154, 156, 158, 160, 162), derived_answer="①",
    figure=U("원 O에 내접하는 △ABC(A 왼쪽 위, B 왼쪽 아래, C 오른쪽). 점 P(오른쪽 아래)에서 접선 PC와 접선 PD(접점 E, D는 왼쪽 아래). "
             "직선 D-B-C, 선분 CE. ∠x=∠BAC(A, 색칠), ∠y=∠CPE(P, 색칠), ∠DCE=22°, ∠CDE=26°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+삼각형+두 접선 도형",
    note="∠CED=132 → ∠PCE=48 → y=84; ∠PCB=48+22=70=x → 154 → ①. 빠른정답 6과 불일치.")

# ---------------- p65
add(id="d33ee8e0", qtype="short",
    question=("다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이면서 [[tri(DEF)]]의 외접원이다. D, E, F는 접점이고 "
              "[[angle(BAC) = deg(42)]], [[angle(DFE) = deg(54)]]일 때, [[angle(BCA)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(66)",
    figure=U("△ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)의 내접원 O, 접점 D(AB 위), E(BC 위), F(CA 위). △DEF. ∠BAC=42°, ∠DFE=54°, ∠C 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형+내접원+내접삼각형 도형",
    note="∠ADF=69=∠DEF → ∠FDE=57=∠CFE → ∠C=180−114=66°. 빠른정답 1과 불일치.")

# ---------------- p66
add(id="d8e54fd6", qtype="short",
    question=("다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이며 [[tri(GEF)]]의 외접원이다. [[angle(B) = deg(40)]], "
              "[[angle(EFG) = deg(50)]]일 때, [[angle(FGE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=U("△ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)의 내접원 O, 접점 F(AB 위), E(AC 위), G(BC 위). △GEF. ∠B=40°, ∠EFG=50°, ∠FGE 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형+내접원+내접삼각형 도형",
    note="∠BFG=∠BGF=70=∠GEF → ∠FGE=180−70−50=60°. 빠른정답 4와 불일치.")

# ---------------- p67
add(id="ac5980ff", qtype="short",
    question=("다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이면서 [[tri(DEF)]]의 외접원이다. [[angle(A) = deg(58)]], "
              "[[angle(EFD) = deg(66)]]일 때, [[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(135)",
    figure=U("△ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)의 내접원 O, 접점 F(AB 위), E(AC 위), D(BC 위). △DEF. ∠A=58°, ∠EFD=66°, "
             "∠x=∠FDE(D), ∠y=∠B"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형+내접원+내접삼각형 도형",
    note="∠AFE=61=x, ∠FED=53=∠BDF → y=74 → 135° = 빠른정답 ✓.")

# ---------------- p69 (PT′, AT′)
add(id="3eb7db79", qtype="choice",
    question=("다음 그림에서 [[ray(PT)]], 반직선 PT′은 원의 접선이고 두 점 T, T′은 접점이다. [[arc(AT)]] = 호 AT′이고 "
              "∠TPT′ = [[deg(32)]]일 때, [[angle(x)]]의 크기는?"),
    choices=D5(50, 51, 52, 53, 54), derived_answer="④",
    figure=U("점 P(왼쪽)에서 원에 그은 두 접선(접점 T 위, T′ 아래). 원 위의 점 A(오른쪽). 현 TT′, TA, T′A. AT=AT′(같은 길이 표시). "
             "∠TPT′=32°, ∠x=∠AT′T(T′)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "원+두 접선+삼각형 도형" + PR,
    note="원문 표기: PT, PT′ 위 반직선 화살표, AT·AT′ 위 호 기호. ∠PT′T=74=∠TAT′ → x=53 → ④. 빠른정답 60과 불일치.")

# ---------------- p72 (O′)
add(id="f41cdcd9", qtype="choice",
    question=("다음 그림에서 [[line(PT)]]가 원 O의 접선이고, 두 점 A, B는 두 원의 교점이다. [[ray(PA)]], [[ray(PB)]]와 원 O′이 "
              "만나는 점을 각각 C, D라 할 때, [[angle(APT)]]의 크기는?"),
    choices=D5(66, 67, 68, 69, 70), derived_answer="②",
    figure=U("작은 원 O(왼쪽 아래)와 큰 원 O′(오른쪽 위)이 두 점 A, B에서 만남. 원 O 위의 점 P(왼쪽 아래)에서의 접선(T는 P 왼쪽 위). "
             "반직선 P-A-C, P-B-D. 선분 CD. ∠ACD=67°(C), ∠BDC=72°(D)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+접선+두 할선 도형" + PR,
    note="∠ABP=∠ACD=67 → ∠APT=∠ABP=67 → ② = 빠른정답 ✓.")

# ---------------- p73
add(id="5ffd8b0d", qtype="short",
    question=("다음 그림과 같이 두 원이 점 P에서 접하고 [[angle(CDB) = deg(53)]]일 때, [[angle(x)]]의 크기를 구하시오.\n"
              "(단, 세 점 A, P, C는 한 직선 위에 있다.)"),
    choices=None, derived_answer="deg(37)",
    figure=U("점 P에서 외접하는 두 원(왼쪽 원의 중심 O). 직선 A-P-C, 직선 B-P-D. 왼쪽 원 위의 점 A(위), B(아래), 오른쪽 원 위의 점 D(위), C(아래). "
             "선분 AB, DC, OA, OP. ∠CDB=53°(D), ∠x=∠OAP(A)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "외접하는 두 원+두 직선 도형",
    note="∠ABP=∠CDP=53 → ∠AOP=106 → x=(180−106)/2=37° = 빠른정답 ✓.")

# ---------------- p74
add(id="2ade1a4c", qtype="short",
    question=("다음 그림과 같이 두 원이 점 P에서 접하고 [[angle(CDB) = deg(50)]]일 때, [[angle(x)]]의 크기를 구하시오.\n"
              "(단, 세 점 A, P, C는 한 직선 위에 있다.)"),
    choices=None, derived_answer="deg(40)",
    figure=U("점 P에서 외접하는 두 원(왼쪽 원의 중심 O). 직선 A-P-C, 직선 B-P-D. 왼쪽 원 위의 점 A(위), B(아래), 오른쪽 원 위의 점 D(위), C(아래). "
             "선분 AB, DC, OA, OP. ∠CDB=50°(D), ∠x=∠OAP(A)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "외접하는 두 원+두 직선 도형",
    note="∠ABP=∠CDP=50 → ∠AOP=100 → x=40°. 빠른정답 43과 불일치.")

# ---------------- p76 (O′)
add(id="68d8f579", qtype="short",
    question="다음 그림에서 직선 PQ가 두 원 O, O′의 공통인 접선이고 점 T가 접점일 때, [[angle(DCT)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(36)",
    figure=U("점 T에서 외접하는 두 원 O(왼쪽), O′(오른쪽)과 T에서의 공통접선 P-T-Q(세로, P 위, Q 아래). 직선 A-T-C, B-T-D. "
             "왼쪽 원 위의 A(위), B(아래), 오른쪽 원 위의 D(위), C(아래). 선분 AB, DC. ∠BAT=36°(A), ∠TDC=80°(D), ∠DCT 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "외접하는 두 원+공통접선 도형" + PR,
    note="∠BTQ=∠BAT=36=∠DTP=∠DCT → 36°. 빠른정답 37과 불일치.")

# ---------------- p78 (O′)
add(id="37912684", qtype="short",
    question="다음 그림에서 직선 PQ가 두 원 O, O′의 공통인 접선이고 점 T가 접점일 때, [[angle(BTQ)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(39)",
    figure=U("점 T에서 외접하는 두 원 O(왼쪽), O′(오른쪽)과 T에서의 공통접선 P-T-Q(세로, P 위, Q 아래). 직선 A-T-C, B-T-D. "
             "왼쪽 원 위의 A(위), B(아래), 오른쪽 원 위의 D(위), C(아래). 선분 AB, DC. ∠BAT=39°(A), ∠TDC=68°(D)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "외접하는 두 원+공통접선 도형" + PR,
    note="∠BTQ=∠BAT=39°. 빠른정답 60과 불일치.")

# ---------------- p81 (O′)
add(id="2fd13393", qtype="short",
    question=("다음 그림과 같이 점 P에서 외접하는 두 원 O, O′에서 [[angle(PAC) = deg(80)]], [[angle(PDB) = deg(40)]]일 때, "
              "[[angle(BPD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=U("점 P에서 외접하는 두 원 O(왼쪽, 큰 원), O′(오른쪽). P에서의 공통접선(세로, T 아래). 직선 A-P-B, C-P-D. "
             "왼쪽 원 위의 A(위), C(왼쪽 아래), 오른쪽 원 위의 D(오른쪽 위), B(아래). 선분 AC, DB. ∠PAC=80°, ∠PDB=40°, ∠BPD 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "외접하는 두 원+공통접선 도형" + PR,
    note="∠PBD=∠PAC=80 → ∠BPD=180−80−40=60° = 빠른정답 ✓.")

# ---------------- p83
add(id="3dbf8135", qtype="short",
    question=("다음 그림에서 두 원은 두 점 P, Q에서 만나고 직선 AB는 두 원의 공통인 접선이다.\n[[angle(APB) = deg(44)]]일 때, "
              "[[angle(AQB)]]의 크기를 구하시오.\n(단, 두 점 A, B는 접점이다.)"),
    choices=None, derived_answer="deg(136)",
    figure=U("두 원이 두 점 P(위), Q(아래)에서 만남. 아래쪽 공통접선 위의 접점 A(왼쪽 원), B(오른쪽 원). 선분 PA, PB, QA, QB. ∠APB=44°, ∠AQB 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+공통접선 도형",
    note="∠QAB+∠QBA=∠APQ+∠BPQ=44 → ∠AQB=136°. 빠른정답 2와 불일치.")

# ---------------- p84
add(id="1c2eef8c", qtype="short",
    question=("다음 그림에서 두 원은 두 점 P, Q에서 만나고 직선 AB는 두 원의 공통인 접선이다.\n[[angle(APB) = deg(30)]]일 때, "
              "[[angle(AQB)]]의 크기를 구하시오.\n(단, 두 점 A, B는 접점이다.)"),
    choices=None, derived_answer="deg(150)",
    figure=U("두 원이 두 점 P(위), Q(아래)에서 만남. 아래쪽 공통접선 위의 접점 A(왼쪽 원), B(오른쪽 원). 선분 PA, PB, QA, QB. ∠APB=30°, ∠AQB 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "두 원+공통접선 도형",
    note="∠AQB=180−30=150°. 빠른정답 60과 불일치.")

# ---------------- p85 (O′)
add(id="084d585c", qtype="short",
    question=("다음 그림과 같이 점 P에서 외접하는 두 원이 있다. [[line(ST)]]는 원 O와 원 O′ 위의 점 P에 접하는 접선이고 "
              "[[angle(BAP) = deg(62)]], [[angle(CPD) = deg(58)]]일 때, [[angle(PDC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=U("점 P에서 외접하는 두 원 O(왼쪽), O′(오른쪽)과 P에서의 공통접선 S-P-T(세로, S 위, T 아래). 직선 A-P-C, B-P-D. "
             "왼쪽 원 위의 A(위), B(아래), 오른쪽 원 위의 D(위), C(아래). 선분 AB, DC. ∠BAP=62°, ∠CPD=58°, ∠PDC 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "외접하는 두 원+공통접선 도형" + PR,
    note="∠DCP=∠BAP=62 → ∠PDC=180−58−62=60°. 빠른정답 '4, 5'와 불일치.")

# ---------------- p86 (TT′)
add(id="87dde9e5", qtype="choice",
    question=("다음 그림에서 직선 TT′은 점 A에서 두 원과 접하고 큰 원의 현 BC는 작은 원과 점 D에서 접한다.\n"
              "[[angle(CBA) = deg(20)]], ∠BAT′ = [[deg(60)]]일 때, [[angle(y) - angle(x)]]의 크기는?"),
    choices=D5(5, 10, 15, 20, 25), derived_answer="②",
    figure=U("아래쪽 직선 T-A-T′에 점 A에서 접하는 큰 원과 작은 원(작은 원은 큰 원 안). 큰 원의 현 BC(B 오른쪽 위, C 왼쪽 아래)가 작은 원과 D에서 접함. "
             "선분 AB, AC, AD. ∠CBA=20°, ∠BAT′=60°, ∠x=∠CAD(A), ∠y=∠ACB(C)"),
    difficulty_est=4, confidence=0.8, needs_review=FIG + "두 원(내접)+접선+현 도형" + PR,
    note="y=∠BAT′=60, ∠CAT=20; BC와 TT′의 교점 E에서 EA=ED → ∠EAD=70 → x=50 → y−x=10 → ②. 빠른정답 136과 불일치.")

# ---------------- p90 (TT′)
add(id="1353d3ad", qtype="short",
    question=("다음 그림에서 직선 TT′은 점 A에서 두 원과 접하고 큰 원의 현 BC는 작은 원과 점 D에서 접한다.\n"
              "[[angle(CBA) = deg(20)]], ∠BAT′ = [[deg(68)]]일 때, [[angle(y) - angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(22)",
    figure=U("아래쪽 직선 T-A-T′에 점 A에서 접하는 큰 원과 작은 원(작은 원은 큰 원 안). 큰 원의 현 BC(B 오른쪽 위, C 왼쪽 아래)가 작은 원과 D에서 접함. "
             "선분 AB, AC, AD. ∠CBA=20°, ∠BAT′=68°, ∠x=∠CAD(A), ∠y=∠ACB(C)"),
    difficulty_est=4, confidence=0.8, needs_review=FIG + "두 원(내접)+접선+현 도형" + PR,
    note="y=68, ∠CAT=20, ∠ACE=112 → ∠AEC=48 → ∠EAD=66 → x=46 → y−x=22°. 빠른정답 2와 불일치.")
