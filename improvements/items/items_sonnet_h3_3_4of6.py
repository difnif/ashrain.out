# -*- coding: utf-8 -*-
# esc_sonnet_h3-3_4of6 — 이미지 기준 전사 (80 항목 / 80쪽, 단원 h3-3 기하: 정사영·이차곡선·벡터·타원·쌍곡선의 접선)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def fig(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]

# ───────────────────────── 정사영 ─────────────────────────
_p61_body = ("좌표공간에 서로 평행한 두 평면 [[alpha]], [[beta]]와 중심이 O이고 반지름의 길이가 {R}인 구 [[S]]가 있다. "
             "점 O에서 두 평면 [[alpha]], [[beta]]에 내린 수선의 발을 각각 [[sub(H,1)]], [[sub(H,2)]]라 하면 "
             "O[[sub(H,1)]] = O[[sub(H,2)]] = {H}이다. 구 [[S]]가 평면 [[alpha]]와 만나서 생기는 원 위를 움직이는 점을 P, "
             "구 [[S]]가 평면 [[beta]]와 만나서 생기는 원 위를 움직이는 점을 Q라 하자.\n"
             "삼각형 POQ의 평면 [[beta]] 위로의 정사영의 넓이가 최대일 때, 평면 POQ와 평면 [[beta]]가 이루는 각의 크기를 [[theta]]라 하자. "
             "[[cos(theta)]]의 값은? (단, 세 점 O, P, Q는 한 직선 위에 있지 않고, 직선 PQ와 직선 [[sub(H,1)]][[sub(H,2)]]는 서로 평행하지 않다.)")
_p61_fig = fig("좌표공간: 구 S와 서로 평행한 두 평면 α(위)·β(아래), 중심 O, 수선의 발 H₁(α 위)·H₂(β 위), 점선 OH₁·OH₂ 그림")
_p61_rev = "도형 표현 불가: 구 S와 평행한 두 평면 α·β 그림 / 첨자 점 라벨(선분 OH₁, OH₂ 윗줄 표기 생략, 직선 H₁H₂ 텍스트 혼합)"

add(id="1bc1beb5", qtype="choice",
    question=_p61_body.format(R="[[sqrt(13)]]", H="2"),
    choices=["[[frac(2 sqrt(17), 17)]]", "[[frac(5 sqrt(17), 34)]]", "[[frac(3 sqrt(17), 17)]]", "[[frac(7 sqrt(17), 34)]]", "[[frac(4 sqrt(17), 17)]]"],
    derived_answer="③", figure=_p61_fig, difficulty_est=4, confidence=0.8, needs_review=_p61_rev,
    note="출처 [2025년 10월 고3 기하 28번/4점]. 단면원 반지름 3, 정사영 넓이 최대(직교) 9/2, △POQ 넓이 3√17/2 → cosθ = 3/√17 = 3√17/17 → ③.")

add(id="e21bf112", qtype="choice",
    question=_p61_body.format(R="5", H="3"),
    choices=["[[frac(sqrt(34), 34)]]", "[[frac(sqrt(17), 17)]]", "[[frac(sqrt(34), 17)]]", "[[frac(2 sqrt(17), 17)]]", "[[frac(2 sqrt(34), 17)]]"],
    derived_answer="⑤", figure=_p61_fig, difficulty_est=4, confidence=0.8, needs_review=_p61_rev,
    note="출처 [2025년 10월 고3 기하 28번 변형]. 단면원 반지름 4, 정사영 최대 8, △POQ 넓이 2√34 → cosθ = 4/√34 = 2√34/17 → ⑤. 빠른정답 3과 불일치.")

add(id="3c774ea0", qtype="choice",
    question="다음 그림과 같이 반지름의 길이가 3 m인 구 모양의 애드벌룬이 지면 위에 떠 있다. 태양 광선이 지면과 [[deg(30)]]의 각을 이루면서 비출 때, 지면 위에 생긴 애드벌룬의 그림자의 넓이는?",
    choices=["[[9 sqrt(2) pi]] m²", "[[9 sqrt(3) pi]] m²", "[[18 pi]] m²", "[[12 sqrt(3) pi]] m²", "[[18 sqrt(2) pi]] m²"],
    derived_answer="③", figure=fig("지면 위에 떠 있는 구(애드벌룬)와 30° 방향의 평행한 태양 광선, 지면 위 그림자 범위 점선 그림"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 애드벌룬·태양 광선(30°)·지면 그림자 삽화",
    note="대원 넓이 9π = 그림자 넓이 × sin30° → 18π m² → ③. 빠른정답 5와 불일치.")

_p89_head = ("다음 그림과 같이 원기둥의 밑면 위에 놓여 있는 반지름의 길이가 1인 두 구 [[sub(S,1)]], [[sub(S,2)]]가 서로 한 점에서 만나고 모두 원기둥의 옆면에 접한다. "
             "두 구 [[sub(S,1)]], [[sub(S,2)]] 위에 반지름의 길이가 1인 두 구 [[sub(T,1)]], [[sub(T,2)]]가 각각 아래쪽에 있는 두 구와 각각 한 점에서 만나면서 모두 원기둥의 옆면에 접한다. ")

add(id="06733463", qtype="short",
    question=(_p89_head + "또, 두 구 [[sub(T,1)]], [[sub(T,2)]] 위에 반지름의 길이가 1인 두 구 [[sub(U,1)]], [[sub(U,2)]]가 각각 아래쪽에 있는 두 구와 각각 한 점에서 만나면서 모두 원기둥의 옆면에 접한다.\n"
              "세 구 [[sub(S,1)]], [[sub(T,1)]], [[sub(U,2)]]의 중심을 각각 [[sub(O,1)]], [[sub(O,2)]], [[sub(O,3)]]라 할 때, "
              "평면 [[sub(O,1)]][[sub(O,2)]][[sub(O,3)]]과 원기둥의 밑면이 이루는 예각의 크기를 [[theta]]라 하자. 이때 [[6 pow(cos(theta), 2)]]의 값을 구하시오.\n"
              "(단, 원기둥의 높이는 6보다 크다.)"),
    choices=None, derived_answer="2",
    figure=fig("원기둥 안에 반지름 1인 구 6개가 3층으로 쌓인 그림: 아래 S₂(왼쪽)·S₁(오른쪽), 가운데 T₁(앞)·T₂(뒤), 위 U₂(왼쪽)·U₁(오른쪽)"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원기둥 안에 쌓인 구 S₁·S₂·T₁·T₂·U₁·U₂ 그림 / 첨자 점 라벨(평면 O₁O₂O₃ 텍스트 혼합)",
    note="원기둥 반지름 2; O₁(1,0,1), O₂(0,1,1+√2), O₃(-1,0,1+2√2) → 법선 (2√2,0,2) → cos²θ = 1/3 → 6cos²θ = 2. 빠른정답 32와 불일치.")

add(id="88eae011", qtype="short",
    question=(_p89_head + "세 구 [[sub(S,1)]], [[sub(T,1)]], [[sub(T,2)]]의 중심을 각각 [[sub(O,1)]], [[sub(O,2)]], [[sub(O,3)]]라 할 때, "
              "평면 [[sub(O,1)]][[sub(O,2)]][[sub(O,3)]]과 원기둥의 밑면이 이루는 예각의 크기를 [[theta]]라 하자. 이때 [[9 pow(cos(theta), 2)]]의 값을 구하시오.\n"
              "(단, 원기둥의 높이는 4보다 크다.)"),
    choices=None, derived_answer="3",
    figure=fig("원기둥 안에 반지름 1인 구 4개가 2층으로 쌓인 그림: 아래 S₂(왼쪽)·S₁(오른쪽), 위 T₁(앞)·T₂(뒤)"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원기둥 안에 쌓인 구 S₁·S₂·T₁·T₂ 그림 / 첨자 점 라벨(평면 O₁O₂O₃ 텍스트 혼합)",
    note="O₁(1,0,1), O₂(0,1,1+√2), O₃(0,-1,1+√2) → 법선 (2√2,0,2) → cos²θ = 1/3 → 9cos²θ = 3.")

# ───────────────────────── 이차곡선 (정의 동시 이용) ─────────────────────────
add(id="0d877585", qtype="short",
    question=("좌표평면에 곡선 [[abs(pow(y,2) - 1) = frac(pow(x,2), pow(a,2))]]과 네 점 [[A(0, c + 1)]], [[B(0, -c - 1)]], [[C(c, 0)]], [[D(-c, 0)]]이 있다. "
              "곡선 위의 점 중 [[y]]좌표의 절댓값이 1보다 작거나 같은 모든 점 P에 대하여 [[seg(PC) + seg(PD) = sqrt(5)]]이다. "
              "곡선 위의 점 Q가 제1사분면에 있고 [[seg(AQ) = 10]]일 때, 삼각형 ABQ의 둘레의 길이를 구하시오. (단, [[a]]와 [[c]]는 양수이다.)"),
    choices=None, derived_answer="25", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2024년 6월 고3 기하 29번/4점]. 타원부 2a=√5 → c=1/2; 쌍곡선부 초점 (0,±3/2)=A,B, QB−QA=2 → 10+12+3 = 25. 빠른정답 4와 불일치.")

_p6_body = ("두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 {HYP}이 있다. 직선 [[x = c]]가 이 쌍곡선과 만나는 점 중 제1사분면 위의 점을 P, 제4사분면 위의 점을 P′이라 하자. "
            "선분 F′P 위에 PP′ = QP′인 점 Q를 잡자. 두 점 P, P′을 초점으로 하고 점 Q를 지나는 타원의 장축의 길이는 [[frac(q, p)]]이다. [[p + q]]의 값을 구하시오.\n"
            "(단, [[p]]와 [[q]]는 서로소인 자연수이다.)")
_p6_rev = "도형 표현 불가: 쌍곡선·직선 x=c·점 P, P′, Q, F, F′ 좌표평면 그림 / 프라임 점 라벨(선분 PP′, QP′ 윗줄 표기 생략, 선분 F′P 텍스트 혼합)"

add(id="6a350f45", qtype="short",
    question=_p6_body.format(HYP="[[frac(pow(x,2), 4) - frac(pow(y,2), 5) = 1]]"),
    choices=None, derived_answer="128",
    figure=fig("좌표평면: 쌍곡선 x²/4−y²/5=1, 초점 F·F′, 직선 x=c와의 교점 P(제1사분면)·P′(제4사분면), 선분 F′P 위의 점 Q, 선분 QP′ 그림"),
    difficulty_est=4, confidence=0.8, needs_review=_p6_rev,
    note="출처 [2025년 3월 고3 기하 29번/4점]. c=3, P(3,5/2), PP′=5, F′P=13/2, QP = 50/13 → 장축 50/13+5 = 115/13 → 128. 빠른정답 52와 불일치.")

add(id="6e6cc84e", qtype="short",
    question=("두 초점이 [[sub(F,1)]][[point(c, 0)]], [[sub(F,2)]][[point(-c, 0)]] ([[c > 0]])인 타원이 [[x]]축과 두 점 [[A(5, 0)]], [[B(-5, 0)]]에서 만난다. "
              "선분 BO가 주축이고 점 [[sub(F,1)]]이 한 초점인 쌍곡선의 초점 중 [[sub(F,1)]]이 아닌 점을 [[sub(F,3)]]라 하자. "
              "쌍곡선이 타원과 제1사분면에서 만나는 점을 P라 할 때, 삼각형 P[[sub(F,3)]][[sub(F,2)]]의 둘레의 길이를 구하시오.\n(단, O는 원점이다.)"),
    choices=None, derived_answer="20",
    figure=fig("좌표평면: 타원(x축 교점 A(5,0)·B(−5,0)), 초점 F₁·F₂, 쌍곡선(주축 BO, 초점 F₁·F₃), 제1사분면 교점 P 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 타원·쌍곡선·점 F₁, F₂, F₃, A, B, P 좌표평면 그림",
    note="출처 [2021년 3월 고3 기하 29번 변형]. 쌍곡선 주축 5: PF₃−PF₁=5, PF₁+PF₂=10, F₃F₂=5 → 둘레 20. 빠른정답 5와 불일치.")

_p9_body = ("초점이 [[F(p, 0)]] ([[p > 0]])이고 준선이 [[x = -p]]인 포물선이 있다. 점 F′[[point(-p, 0)]]에 대하여 cos(∠PFF′) = {COS}을 만족시키는 이 포물선 위의 점 중 제1사분면에 있는 점을 P라 하고, "
            "선분 PF′의 중점을 R이라 하자. 두 점 O, F′을 초점으로 하고 점 R을 지나는 쌍곡선에 대하여 선분 PF′과 쌍곡선이 만나는 점 중 R이 아닌 점을 Q라 하자.\n"
            "삼각형 QOR의 둘레의 길이가 {PER}일 때, 삼각형 PRO의 넓이를 [[S]]라 하자. [[pow(S, 2)]]의 값을 구하시오.\n(단, O는 원점이다.)")
_p9_fig = fig("좌표평면: 포물선(초점 F, 준선 x=−p), 두 갈래 쌍곡선(초점 O·F′), 점 P(제1사분면)·R(PF′ 중점)·Q, 선분 PF′·PF 그림")
_p9_rev = "도형 표현 불가: 포물선·준선·쌍곡선·점 P, Q, R, F, F′ 좌표평면 그림 / 프라임 점 라벨(∠PFF′ 텍스트 혼합)"

add(id="48e268b7", qtype="short",
    question=_p9_body.format(COS="[[frac(7, 13)]]", PER="17"),
    choices=None, derived_answer="750", figure=_p9_fig, difficulty_est=5, confidence=0.75, needs_review=_p9_rev,
    note="출처 [2026년 7월 고3 기하 29번 변형]. PF=13p/10, P(3p/10, √30p/5), R(−7p/20, √30p/10), 둘레 = 17p/10 = 17 → p=10, S=5√30 → S²=750. 빠른정답 4와 불일치.")

add(id="8ea3dba5", qtype="short",
    question=("다음 그림과 같이 타원 [[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), pow(b,2)) = 1]]과\n쌍곡선 [[frac(pow(x,2), pow(b,2)) - frac(pow(y,2), pow(c,2)) = 1]]은 두 초점 F, F′을 공유한다.\n"
              "이 두 곡선의 한 교점 P에 대하여 [[seg(PF) = 4]], PF′ = 16일 때, [[pow(c, 2)]]의 값을 구하시오. (단, [[a]], [[b]], [[c]]는 상수)"),
    choices=None, derived_answer="28",
    figure=fig("좌표평면: 타원과 쌍곡선이 초점 F·F′을 공유, 제1사분면 교점 P와 선분 PF·PF′ 그림"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 타원·쌍곡선·점 P, F, F′ 좌표평면 그림 / 프라임 점 라벨(선분 PF′ 윗줄 표기 생략)",
    note="a=10, b=6, 초점거리² 100−36 = 64 = 36+c² → c² = 28.")

add(id="72bb800a", qtype="choice",
    question=("타원 [[frac(pow(x,2), 16) + frac(pow(y,2), 12) = 1]]과 포물선 [[pow(y,2) = 8x]]의 한 교점을 A라 하고 직선 [[x = -2]]와 [[x]]축의 교점을 B라 하자.\n"
              "점 A에서 직선 [[x = -2]]에 내린 수선의 발을 H라 할 때, [[seg(AB) + seg(AH)]]의 값은?"),
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"],
    derived_answer="⑤", figure=fig("좌표평면: 타원 x²/16+y²/12=1, 포물선 y²=8x, 직선 x=−2, 교점 A, 수선의 발 H, x축 교점 B 그림"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 타원·포물선·직선 x=−2·점 A, B, H 좌표평면 그림",
    note="B(−2,0)와 (2,0)은 타원의 초점, AH = A(2,0) 거리 → AB+AH = 2a = 8 → ⑤. 빠른정답 24와 불일치.")

add(id="ef200315", qtype="choice",
    question=("좌표평면에서 두 점 [[F(3, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원과 포물선 [[pow(y,2) = 12x]]가 제1사분면에서 만나는 점을 P라 하자. "
              "[[seg(PF) = 6]]이고 포물선 [[pow(y,2) = 12x]] 위의 점 P에서의 접선이 점 F′을 지날 때, 타원의 단축의 길이를 [[k]]라 하자. 이때 [[pow(k, 2)]]의 값은?"),
    choices=["[[24 + 24 sqrt(2)]]", "[[36 + 24 sqrt(2)]]", "[[36 + 36 sqrt(2)]]", "[[72 + 36 sqrt(2)]]", "[[72 + 72 sqrt(2)]]"],
    derived_answer="⑤", figure=fig("좌표평면: 타원(초점 F′·F), 포물선 y²=12x, 제1사분면 교점 P, P에서의 접선(F′ 통과), P에서 x축에 내린 수선 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 타원·포물선·접선·점 P, F, F′ 좌표평면 그림",
    note="출처 [2021년 4월 고3 기하 28번 변형]. P(3,6), 접선 y=x+3 → c=3, PF′=6√2, a=3+3√2, b²=18+18√2 → k²=4b² = 72+72√2 → ⑤.")

_p18_body = ("다음 그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원 {ELL}과 두 점 F, F′을 초점으로 하는 쌍곡선 {HYP}이 제1사분면에서 만나는 점을 P라 하자. "
             "[[seg(PF) = 3]]일 때, [[pow(a,2) + pow(b,2)]]의 값은?\n(단, [[a]], [[b]]는 상수이다.)")
_p18_rev = "도형 표현 불가: 타원·쌍곡선·점 P, F, F′ 좌표평면 그림"

add(id="18a21c3a", qtype="choice",
    question=_p18_body.format(ELL="[[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), 8) = 1]]", HYP="[[frac(pow(x,2), 25) - frac(pow(y,2), pow(b,2)) = 1]]"),
    choices=["[[89]]", "[[91]]", "[[93]]", "[[95]]", "[[97]]"],
    derived_answer="④", figure=fig("좌표평면: 타원 x²/a²+y²/8=1과 쌍곡선 x²/25−y²/b²=1, 초점 F′·F, 제1사분면 교점 P, 선분 PF 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p18_rev,
    note="출처 [2021년 4월 고3 기하 27번 변형]. PF′=13, a=8, c²=56, b²=31 → 95 → ④.")

_p20_body = ("다음 그림과 같이 두 점 [[A({A}, 0)]], [[B(-{A}, 0)]]을 장축의 양 끝 점으로 하는 타원의 두 초점을 F, F′이라 하고, "
             "초점이 F이고 꼭짓점이 원점인 포물선이 타원과 만나는 두 점을 각각 P, Q라 하자. [[seg(PQ) = {PQ}]]일 때,\n[[seg(PF)]] · PF′의 값을 구하시오.")
_p20_fig = "좌표평면: 장축 양 끝 A·B인 타원, 초점 F′·F, 꼭짓점 원점·초점 F인 포물선, 교점 P(위)·Q(아래), 선분 PF·PF′·PQ 그림"
_p20_rev = "도형 표현 불가: 타원·포물선·점 P, Q, F, F′ 좌표평면 그림 / 프라임 점 라벨(선분 PF′ 윗줄 표기 생략)"

add(id="e9be9648", qtype="short",
    question=_p20_body.format(A="6", PQ="4 sqrt(6)"),
    choices=None, derived_answer="35", figure=fig(_p20_fig), difficulty_est=3, confidence=0.85, needs_review=_p20_rev,
    note="PF′²−PF² = 4c·x_P = y_P² = 24, PF′+PF = 12 → PF′−PF = 2 → 7·5 = 35. 빠른정답 5와 불일치.")

add(id="ee5ae668", qtype="short",
    question=_p9_body.format(COS="[[frac(1, 5)]]", PER="14"),
    choices=None, derived_answer="216", figure=_p9_fig, difficulty_est=5, confidence=0.75, needs_review=_p9_rev,
    note="출처 [2026년 7월 고3 기하 29번/4점]. PF=5p/3, P(2p/3, 2√6p/3), R(−p/6, √6p/3), 둘레 = 7p/3 = 14 → p=6, S=6√6 → S²=216. 빠른정답 4와 불일치.")

add(id="1cc1862e", qtype="short",
    question=_p20_body.format(A="5", PQ="2 sqrt(10)"),
    choices=None, derived_answer="frac(99,4)", figure=fig(_p20_fig), difficulty_est=3, confidence=0.85, needs_review=_p20_rev,
    note="PF′²−PF² = y_P² = 10, PF′+PF = 10 → PF′−PF = 1 → (11/2)(9/2) = 99/4.")

_p28_body = ("다음 그림과 같이 두 초점 F, F′을 공유하는\n타원 {ELL}과 쌍곡선 {HYP}이\n서로 다른 네 점에서 만난다. 타원과 쌍곡선의 교점 중 제1사분면에 있는 점 P에 대하여 "
             "PF′² − [[pow(seg(PF), 2)]]의 값을 구하시오.")
_p28_rev = "도형 표현 불가: 타원·쌍곡선·점 P, F, F′ 좌표평면 그림 / 프라임 점 라벨(PF′² 윗줄 표기 생략)"

add(id="0ed2a7b9", qtype="short",
    question=_p28_body.format(ELL="[[frac(pow(x,2), 36) + frac(pow(y,2), 11) = 1]]", HYP="[[frac(pow(x,2), 16) - frac(pow(y,2), 9) = 1]]"),
    choices=None, derived_answer="96",
    figure=fig("좌표평면: 타원 x²/36+y²/11=1과 쌍곡선 x²/16−y²/9=1(공통 초점 F′·F), 제1사분면 교점 P, 선분 PF·PF′ 그림"),
    difficulty_est=2, confidence=0.85, needs_review=_p28_rev,
    note="PF+PF′=12, PF′−PF=8 → PF′=10, PF=2 → 100−4 = 96. 빠른정답 5와 불일치.")

add(id="c5014261", qtype="short",
    question=_p28_body.format(ELL="[[frac(pow(x,2), 49) + frac(pow(y,2), 33) = 1]]", HYP="[[frac(pow(x,2), 4) - frac(pow(y,2), 12) = 1]]"),
    choices=None, derived_answer="56",
    figure=fig("좌표평면: 타원 x²/49+y²/33=1과 쌍곡선 x²/4−y²/12=1(공통 초점 F′·F), 제1사분면 교점 P, 선분 PF·PF′ 그림"),
    difficulty_est=2, confidence=0.85, needs_review=_p28_rev,
    note="PF+PF′=14, PF′−PF=4 → 4·14 = 56. 빠른정답 72와 불일치.")

add(id="5a4e50ca", qtype="choice",
    question=("그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원 [[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), 7) = 1]]과 두 점 F, F′을 초점으로 하는 쌍곡선 "
              "[[frac(pow(x,2), 4) - frac(pow(y,2), pow(b,2)) = 1]]이 제1사분면에서 만나는 점을 P라 하자. [[seg(PF) = 3]]일 때, [[pow(a,2) + pow(b,2)]]의 값은?\n(단, [[a]], [[b]]는 상수이다.)"),
    choices=["[[31]]", "[[33]]", "[[35]]", "[[37]]", "[[39]]"],
    derived_answer="⑤", figure=fig("좌표평면: 타원 x²/a²+y²/7=1과 쌍곡선 x²/4−y²/b²=1, 초점 F′·F, 제1사분면 교점 P, 선분 PF 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p18_rev,
    note="출처 [2021년 4월 고3 기하 27번/3점]. PF′=7, a=5, c²=18, b²=14 → 39 → ⑤.")

add(id="6bd16ab5", qtype="short",
    question=_p6_body.format(HYP="[[frac(pow(x,2), 9) - frac(pow(y,2), 7) = 1]]"),
    choices=None, derived_answer="207",
    figure=fig("좌표평면: 쌍곡선 x²/9−y²/7=1, 초점 F·F′, 직선 x=c와의 교점 P(제1사분면)·P′(제4사분면), 선분 F′P 위의 점 Q, 선분 QP′ 그림"),
    difficulty_est=4, confidence=0.8, needs_review=_p6_rev,
    note="출처 [2025년 3월 고3 기하 29번 변형]. c=4, P(4,7/3), PP′=14/3, F′P=25/3, QP=196/75 → 장축 182/25 → 207. 빠른정답 56과 불일치.")

add(id="fe4681d2", qtype="short",
    question=("두 초점이 [[F(0, 3)]], F′[[point(0, -3)]]이고, 장축의 길이가 9인 타원이 있다. 이 타원 위에 있는 제1사분면 위의 점 중 ∠F′FP = [[frac(pi, 3)]]를 만족시키는 점 P에 대하여 "
              "직선 FP가 [[x]]축과 만나는 점을 Q라 하자. 점 Q를 초점으로 하고 준선이 [[x = a]] ([[a < 0]])인 포물선이 점 P를 지난다. 직선 FP가 이 포물선과 만나는 점 중 P가 아닌 점을 R이라 할 때, "
              "[[seg(PR) = p + q sqrt(3)]]이다. [[p + q]]의 값을 구하시오. (단, [[a]]는 상수이고, [[p]], [[q]]는 유리수이다.)"),
    choices=None, derived_answer=None, figure=None, difficulty_est=5, confidence=0.75,
    needs_review="프라임 점 라벨(∠F′FP 텍스트 혼합) / 답 미도출",
    note="출처 [2025년 3월 고3 기하 30번 변형]. PF=15/4, Q(3√3,0), PQ=9/4 → 준선 x=a에서 a≈1>0이 되어 조건 a<0과 어긋남(변형 정합성 검토 필요). 답 미도출.")

_p38_body = ("좌표평면에서 초점이 [[A(a, 0)]] ([[a > 0]])이고 꼭짓점이 원점인 포물선과 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > a]])인 타원의 교점 중 제1사분면 위의 점을 P라 하자.\n"
             "[[seg(AF) = {AF}]], [[seg(PA) = seg(PF)]], FF′ = PF′일 때, 타원의 장축의 길이는 [[p + q sqrt(7)]]이다. {ASK}의 값을 구하시오.\n(단, [[p]], [[q]]는 유리수이다.)")
_p38_fig = fig("좌표평면: 꼭짓점 원점·초점 A인 포물선과 초점 F′·F인 타원, 제1사분면 교점 P, PA=PF 표시(등호 표시), 선분 PF′ 그림")
_p38_rev = "도형 표현 불가: 포물선·타원·점 P, A, F, F′ 좌표평면 그림 / 프라임 점 라벨(선분 FF′, PF′ 윗줄 표기 생략)"

add(id="7c3bce99", qtype="short",
    question=_p38_body.format(AF="4", ASK="[[p + q]]"),
    choices=None, derived_answer="14", figure=_p38_fig, difficulty_est=4, confidence=0.85, needs_review=_p38_rev,
    note="출처 [2017년 9월 고3 이과 27번 변형]. x_P=a+2, PF=2a+2, PF′=2c=2a+8 → a²=7 → 장축 10+4√7 → p+q=14. 빠른정답 12와 불일치.")

add(id="5879febc", qtype="choice",
    question=("그림과 같이 두 점 [[F(k, 0)]], F′[[point(-k, 0)]]을 초점으로 하는 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]]과 점 F를 초점으로 하는 포물선 [[pow(y,2) = 56(x + c)]]가 있다.\n"
              "쌍곡선 위의 임의의 점 P에 대하여 |[[seg(PF)]] − PF′| = 10이 성립하고, 포물선의 꼭짓점 A에 대하여 AF′ : FF′ = 1 : 6이 성립한다.\n"
              "이때, [[frac(pow(c,2), pow(a,2) - pow(b,2))]]의 값은? (단, [[0 < k < c]]이다.)"),
    choices=["[[frac(53, 14)]]", "[[frac(55, 14)]]", "[[frac(30, 7)]]", "[[frac(32, 7)]]", "[[frac(34, 7)]]"],
    derived_answer="④", figure=fig("좌표평면: 쌍곡선 x²/a²−y²/b²=1(초점 F′·F), 포물선 y²=56(x+c)(꼭짓점 A, 초점 F), 쌍곡선 위의 점 P 그림"),
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 쌍곡선·포물선·점 P, A, F, F′ 좌표평면 그림 / 프라임 점 라벨(|PF−PF′|, AF′:FF′ 윗줄 표기 생략)",
    note="출처 [2009년 10월 고3 이과 8번]. k=14−c, (c−k):2k=1:6 → c=8, k=6, a=5, b²=11 → 64/14 = 32/7 → ④. 빠른정답 30과 불일치.")

_p45_body = ("그림과 같이 두 점 [[F({C}, 0)]], F′[[point(-{C}, 0)]]을 초점으로 하는 쌍곡선 [[C]]: [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]]이 있다. "
             "점 F를 초점으로 하고 [[y]]축을 준선으로 하는 포물선이 쌍곡선 [[C]]와 만나는 점 중 제1사분면 위의 점을 P라 하자. "
             "점 P에서 [[y]]축에 내린 수선의 발을 H라 할 때, [[ratio(seg(PH), seg(HF)) = ratio({R1}, {R2})]]이다.\n{ASK}")
_p45_fig = "좌표평면: 쌍곡선 C(초점 F′·F)와 포물선(초점 F, 준선 y축), 제1사분면 교점 P, y축 위 수선의 발 H, 선분 PH·HF 그림"
_p45_rev = "도형 표현 불가: 쌍곡선·포물선·점 P, H, F, F′ 좌표평면 그림"

add(id="c9658283", qtype="short",
    question=_p45_body.format(C="4", R1="3", R2="2 sqrt(2)", ASK="[[pow(a,2) pow(b,2)]]의 값을 구하시오. (단, [[a > b > 0]])"),
    choices=None, derived_answer="63", figure=fig(_p45_fig), difficulty_est=4, confidence=0.85, needs_review=_p45_rev,
    note="출처 [2024년 9월 고3 기하 29번/4점]. PH=PF=3t, HF=2√2t → t=3, P(9,2√14), PF′=15 → a=3, b²=7 → 63. 빠른정답 5와 불일치.")

add(id="8f82180d", qtype="short",
    question=_p45_body.format(C="3", R1="4", R2="2 sqrt(3)", ASK="[[pow(b,2) = p sqrt(10) - q]]라 할 때, 정수 [[p]], [[q]]에 대하여 [[p + q]]의 값을 구하시오. (단, [[a > b > 0]])"),
    choices=None, derived_answer="63", figure=fig(_p45_fig), difficulty_est=4, confidence=0.85, needs_review=_p45_rev,
    note="출처 [2024년 9월 고3 기하 29번 변형]. t=2, P(8,√39), PF=8, PF′=4√10 → a=2√10−4, b²=9−a² = 16√10−47 → 63. 빠른정답 9와 불일치.")

add(id="7e2a876f", qtype="short",
    question=_p38_body.format(AF="2", ASK="[[pow(p,2) + pow(q,2)]]"),
    choices=None, derived_answer="29", figure=_p38_fig, difficulty_est=4, confidence=0.85, needs_review=_p38_rev,
    note="출처 [2017년 9월 고3 이과 27번/4점]. x_P=a+1, PF=2a+1, PF′=2a+4 → a²=7/4 → 장축 5+2√7 → 25+4 = 29.")

add(id="8cffa12f", qtype="short",
    question=("좌표평면에서 두 점 [[A(5, 0)]], [[B(-5, 0)]]에 대하여 장축이 선분 AB인 타원의 두 초점을 F, F′이라 하자. 초점이 F이고 꼭짓점이 원점인 포물선이 타원과 만나는 두 점을 각각 P, Q라 하자, "
              "[[seg(PQ) = 2 sqrt(10)]]일 때, 두 선분 PF와 PF′의 길이의 곱 [[seg(PF)]] × PF′의 값은 [[frac(q, p)]]이다. [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="103", figure=fig(_p20_fig), difficulty_est=3, confidence=0.85, needs_review=_p20_rev,
    note="출처 [2010년 9월 고3 이과 20번]. PF′−PF=1, PF′+PF=10 → 곱 99/4 → 103. 빠른정답 4와 불일치.")

add(id="d2c2f033", qtype="short",
    question=_p38_body.format(AF="4", ASK="[[p q]]"),
    choices=None, derived_answer="40", figure=_p38_fig, difficulty_est=4, confidence=0.85, needs_review=_p38_rev,
    note="출처 [2017년 9월 고3 이과 27번 변형]. a=√7, 장축 10+4√7 → pq = 40. 빠른정답 29와 불일치.")

add(id="e3868b59", qtype="short",
    question=("다음 그림과 같이 두 점 [[A(6, 0)]]과 [[B(-6, 0)]]에 대하여 장축이 선분 AB인 타원의 두 초점을 F와 F′이라 하고, 초점이 F이고 꼭짓점이 원점인 포물선이 타원과 만나는 두 점을 각각 P와 Q라 하자. "
              "[[seg(PQ) = 4 sqrt(6)]]일 때,\nPF′ − [[seg(PF)]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=fig(_p20_fig), difficulty_est=2, confidence=0.85, needs_review=_p20_rev,
    note="PF′²−PF² = y_P² = 24, PF′+PF = 12 → 차 2.")

add(id="a98181f2", qtype="choice",
    question=("다음 그림과 같이 [[F(p, 0)]]을 초점으로 하는 포물선 [[pow(y,2) = 4 p x]]와 [[F(p, 0)]]과 F′[[point(-p, 0)]]을 초점으로 하는 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]] ([[a > 0]], [[b > 0]])이 "
              "제1사분면에서 만나는 점을 A라 하자.\n[[seg(AF) = 5]], sin(∠AFF′) = [[frac(2 sqrt(6), 5)]]일 때, [[a b]]의 값은?\n(단, ∠AFF′은 예각이다.)"),
    choices=["[[1]]", "[[sqrt(2)]]", "[[sqrt(5)]]", "[[2 sqrt(2)]]", "[[sqrt(11)]]"],
    derived_answer="④", figure=fig("좌표평면: 포물선 y²=4px와 쌍곡선 x²/a²−y²/b²=1(초점 F′·F), 제1사분면 교점 A, 선분 AF(길이 5) 점선 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 포물선·쌍곡선·점 A, F, F′ 좌표평면 그림 / 프라임 점 라벨(∠AFF′ 텍스트 혼합)",
    note="cos=1/5, A(p−1, 2√6), 2p−1=5 → p=3, AF′=7 → a=1, b=2√2 → ab = 2√2 → ④.")

add(id="056270b1", qtype="short",
    question="[[x]], [[y]]에 대한 이차방정식 [[(k + 3) pow(x,2) + (k - 4) pow(y,2) - 6x + 10y + 1 = 0]]이 쌍곡선을 나타내도록 하는 모든 정수 [[k]]의 개수를 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="(k+3)(k−4)<0 → k=−2,…,3 (퇴화 없음) → 6개. 빠른정답 4와 불일치.")

# ───────────────────────── 벡터의 덧셈과 뺄셈 ─────────────────────────
_p2_body = "타원 {ELL} 위의 점 P와 두 초점 F, F′에 대하여 |[[vec(PF)]] + PF′→|의 최댓값은?"
_p2_rev = "프라임 점 라벨(벡터 PF′ 화살표 표기 생략, 텍스트 혼합)"

add(id="47fc504e", qtype="choice",
    question=_p2_body.format(ELL="[[frac(pow(x,2), 25) + frac(pow(y,2), 16) = 1]]"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85, needs_review=_p2_rev,
    note="출처 [2017년 10월 고3 이과 10번 변형]. PF→+PF′→ = 2PO→ → 최댓값 2a = 10 → ⑤.")

_p4_body = ("다음 그림과 같이 [[seg(AB) = {AB}]], [[seg(BC) = {BC}]]인 직사각형 ABCD에 대하여 네 선분 AB, CD, {DA}, BD의 중점을 각각 E, F, G, H라 하자. "
            "선분 CF를 지름으로 하는 원 위의 점 P에 대하여 [[abs(vec(EG) + vec(HP))]]의 최솟값은?")
_p4_fig = "직사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), 중점 E(AB)·F(CD)·G(AD)·H(BD), 대각선 BD, 선분 CF를 지름으로 하는 원, 벡터 EG·HP 화살표 그림"
_p4_rev = "도형 표현 불가: 직사각형 ABCD·중점 E, F, G, H·원·벡터 EG, HP 그림"

add(id="8f602432", qtype="choice",
    question=_p4_body.format(AB="4", BC="3", DA="DA"),
    choices=["[[2]]", "[[sqrt(10) - 1]]", "[[sqrt(11) - 1]]", "[[2 sqrt(3) - 1]]", "[[sqrt(13) - 1]]"],
    derived_answer="②", figure=fig(_p4_fig), difficulty_est=3, confidence=0.85, needs_review=_p4_rev,
    note="출처 [2016년 10월 고3 이과 18번 변형]. B 원점, EG→ = (3/2, 2) = BH→ → EG→+HP→ = BP→, 원 중심 (3,1) 반지름 1 → √10−1 → ②. 빠른정답 1과 불일치.")

_p5_body = ("삼각형 ABC에서{BR}[[seg({S}) = {L}]], [[angle(B) = deg({B})]], [[angle(C) = deg({C})]]{BR2}이다. 점 P가 [[vec(PB) + vec(PC) = vec(0)]]를 {SAT} 때,\n"
            "[[pow(abs(vec(PA)), 2)]]의 값은?")

add(id="8095205d", qtype="choice",
    question=_p5_body.format(BR="\n", S="AB", L="2", B="90", C="30", BR2="\n", SAT="만족시킬"),
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2011년 11월 고3 이과 8번/3점]. P는 BC의 중점, BC=2√3, PB=√3 → PA² = 4+3 = 7 → ③. 빠른정답 5와 불일치.")

add(id="490ed3fb", qtype="choice",
    question=_p5_body.format(BR=" ", S="AC", L="6", B="60", C="90", BR2="", SAT="만족할"),
    choices=["[[36]]", "[[37]]", "[[38]]", "[[39]]", "[[40]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="P는 BC의 중점, BC=2√3, PC=√3 → PA² = 36+3 = 39 → ④.")

add(id="2ce14717", qtype="short",
    question="타원 [[frac(pow(x,2), 9) + frac(pow(y,2), 4) = 1]] 위의 한 점 P와 두 초점 F, F′에 대하여 [[abs(vec(OF) + vec(OP)) = 2]]일 때, [[abs(vec(PF))]]의 값은 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="OF→ = −OF′→ → |F′P→| = 2 → PF = 6−2 = 4. (원문 '값은 구하시오' 그대로)")

add(id="369059e6", qtype="choice",
    question=_p4_body.format(AB="12", BC="9", DA="AD"),
    choices=["[[12]]", "[[3 sqrt(10) - 3]]", "[[3 sqrt(11) - 3]]", "[[4 sqrt(3) - 3]]", "[[3 sqrt(13) - 3]]"],
    derived_answer="②", figure=fig(_p4_fig), difficulty_est=3, confidence=0.85, needs_review=_p4_rev,
    note="B 원점, EG→+HP→ = BP→, 원 중심 (9,3) 반지름 3 → √90−3 = 3√10−3 → ②. 빠른정답 5와 불일치.")

add(id="3ff9de7b", qtype="choice",
    question="아래 그림과 같은 정육각형 ABCDEF에서\n[[vec(AB) = vec(a)]], [[vec(BC) = vec(b)]], [[vec(CD) = vec(c)]]라 할 때,\n다음 중 벡터 [[-vec(a) + vec(b) + vec(c)]]와 서로 같은 벡터는?",
    choices=["[[vec(EC)]]", "[[vec(DF)]]", "[[vec(AD)]]", "[[vec(AE)]]", "[[vec(BE)]]"],
    derived_answer="⑤", figure=fig("정육각형 ABCDEF(A 위, B 왼쪽 위, C 왼쪽 아래, D 아래, E 오른쪽 아래, F 오른쪽 위)와 변 AB·BC·CD 위의 벡터 a·b·c 화살표 그림"),
    difficulty_est=1, confidence=0.85, needs_review="도형 표현 불가: 정육각형 ABCDEF와 벡터 a, b, c 그림",
    note="−a→ = DE→, b→+c→ = BD→ → BD→+DE→ = BE→ → ⑤.")

add(id="05d4422f", qtype="short",
    question=("직선 [[2x + y = 0]] 위를 움직이는 점 P와 타원 [[2 pow(x,2) + pow(y,2) = 3]] 위를 움직이는 점 Q에 대하여 [[vec(OX) = vec(OP) + vec(OQ)]]를 만족시키고, "
              "[[x]]좌표와 [[y]]좌표가 모두 0 이상인 모든 점 X가 나타내는 영역의 넓이는 [[frac(q, p)]]이다.\n[[p + q]]의 값을 구하시오.\n(단, O는 원점이고, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="13", figure=fig("좌표평면: 원점을 지나는 직선 2x+y=0과 원점 중심 타원 2x²+y²=3 그림"),
    difficulty_est=4, confidence=0.75, needs_review="도형 표현 불가: 직선 2x+y=0과 타원 2x²+y²=3 좌표평면 그림",
    note="출처 [2023년 6월 고3 기하 30번/4점]. X의 영역은 접선 2x+y=±3 사이 띠 → 제1사분면 부분 삼각형 넓이 9/4 → 13(전사 원문 기준 풀이, 검토 필요). 빠른정답 5와 불일치.")

add(id="c84a9568", qtype="choice",
    question=("쌍곡선 [[pow(x,2) - frac(pow(y,2), 3) = 1]]의 두 초점을 F, F′이라 하자. 이 쌍곡선 위의 점 P가 [[abs(vec(OF) - vec(OP)) = 2]]을 만족시킬 때, 점 P의 좌표가 [[point(a, b)]]이다. "
              "이 때, 상수 [[frac(9 pow(b,2), pow(a,2))]]의 값은?\n(단, O는 원점이다.)"),
    choices=["[[9]]", "[[12]]", "[[15]]", "[[18]]", "[[21]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="PF=2, PF′=4 → a=3/2, b²=15/4 → 9b²/a² = 15 → ③.")

add(id="afeb49d5", qtype="choice",
    question=_p2_body.format(ELL="[[frac(pow(x,2), 9) + frac(pow(y,2), 5) = 1]]"),
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.85, needs_review=_p2_rev,
    note="출처 [2017년 10월 고3 이과 10번/3점]. |2PO→| 최댓값 2a = 6 → ②. 빠른정답 3과 불일치.")

add(id="1e9424ff", qtype="short",
    question="다음 그림과 같이 반지름의 길이가 3인 원에 내접하는 정육각형 ABCDEF에서 [[vec(BC) + vec(AF) - vec(BA)]]의 크기를 구하시오.",
    choices=None, derived_answer="6", figure=fig("반지름 3인 원에 내접하는 정육각형 ABCDEF(A 위, B 왼쪽 위, C 왼쪽 아래, D 아래, E 오른쪽 아래, F 오른쪽 위), 중심에서 A까지 반지름 3 점선 그림"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 원에 내접하는 정육각형 ABCDEF 그림",
    note="AB→+AF→ = AO→·… = (0,−3), +BC→ = (0,−3) → (0,−6) → 크기 6. 빠른정답 2와 불일치.")

add(id="e7d6119b", qtype="choice",
    question="서로 다른 세 점 A, B, C에 대하여 다음 중 옳지 않은 것은?",
    choices=["[[vec(BC) + vec(CA) = vec(BA)]]", "[[vec(AB) - vec(CB) = vec(AC)]]", "[[vec(AC) + vec(CA) = vec(0)]]", "[[vec(AC) - vec(CB) = vec(BA)]]", "[[vec(AB) + vec(BC) + vec(CA) = vec(0)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="④ AC→−CB→ = AC→+BC→ ≠ BA→ → ④.")

add(id="7d8805d6", qtype="short",
    question="한 평면 위의 사각형 ABCD와 임의의 점 P에 대하여 [[vec(PA) + vec(PC) = vec(PB) + vec(PD)]], [[abs(vec(AB)) = abs(vec(AD))]]가 성립할 때, 사각형 ABCD는 어떤 사각형인지 말하시오.",
    choices=None, derived_answer="마름모", figure=None, difficulty_est=2, confidence=0.85,
    note="대각선의 중점 일치(평행사변형) + 이웃한 두 변 길이 같음 → 마름모. 빠른정답 5와 불일치.")

# ───────────────────────── 타원 ─────────────────────────
_p28e_body = ("{LEAD}좌표평면에 [[x]]축 위의 두 점 F, F′과 점 {PT} ([[n > 0]])이 있다. 삼각형 PF′F가 ∠FPF′ = [[frac(pi, 2)]]인 직각이등변삼각형{CONJ}, "
              "두 점 F, F′을 초점으로 하고 점 P를 지나는 타원과 직선 PF′이 만나는 점 중 점 P가 아닌 점을 Q라 하자. 삼각형 FPQ의 둘레의 길이가 {PER}일 때, 삼각형 FPQ의 넓이는?")
_p28e_rev = "도형 표현 불가: 삼각형 PF′F·타원 좌표평면 그림 / 프라임 점 라벨(∠FPF′ 텍스트 혼합)"

add(id="be6fc533", qtype="choice",
    question=_p28e_body.format(LEAD="다음 그림과 같이 ", PT="[[P(0, n)]]", CONJ="이고", PER="12"),
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"],
    derived_answer="③", figure=fig("좌표평면: 초점 F′·F인 타원, y축 위의 점 P(직각 표시), 직선 PF′과 타원의 교점 Q(제3사분면), 삼각형 FPQ 음영 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p28e_rev,
    note="출처 [2015년 10월 고3 이과 14번 변형]. 둘레 = 4a = 12 → PF=3, F′Q=1, PQ=4 → 넓이 6 → ③. 빠른정답 5와 불일치.")

add(id="9aaca6f4", qtype="choice",
    question=("그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]]을 초점으로 하는 타원이 있다. 타원 위의 점 중 제1사분면에 있는 점 P에 대하여 직선 PF가 타원과 만나는 점 중 점 P가 아닌 점을 Q라 하자. "
              "[[seg(OQ) = seg(OF)]], [[seg(FQ)]] : F′Q = 1 : 4이고 삼각형 PF′Q의 내접원의 반지름의 길이가 2일 때, 양수 [[c]]의 값은? (단, O는 원점이다.)"),
    choices=["[[frac(17, 3)]]", "[[frac(7 sqrt(17), 5)]]", "[[frac(3 sqrt(17), 2)]]", "[[frac(51, 8)]]", "[[frac(8 sqrt(17), 5)]]"],
    derived_answer="③", figure=fig("좌표평면: 초점 F′·F인 타원, 제1사분면 점 P, 직선 PF와 타원의 교점 Q(제4사분면), 삼각형 PF′Q와 그 내접원 그림"),
    difficulty_est=4, confidence=0.85, needs_review="도형 표현 불가: 타원·삼각형 PF′Q·내접원 좌표평면 그림 / 프라임 점 라벨(FQ:F′Q 윗줄 표기 생략)",
    note="출처 [2022년 4월 고3 기하 28번/4점]. ∠FQF′=90°, FQ=t, F′Q=4t, PF=2t/3, 내접원 r = 2t/3 = 2 → t=3, 2c = 3√17 → ③. 빠른정답 2와 불일치.")

add(id="b629a85f", qtype="short",
    question=("다음 그림과 같이 두 점 [[F(9, 0)]], F′[[point(-9, 0)]]을 초점으로 하는 타원과 점 F를 지나는 직선이 만나는 두 점을 각각 A, B라 하자. "
              "삼각형 AF′B의 둘레의 길이가 60일 때, 이 타원의 단축의 길이를 구하시오."),
    choices=None, derived_answer="24", figure=fig("좌표평면: 초점 F′(−9,0)·F(9,0)인 타원, F를 지나는 직선과 타원의 교점 A(제1사분면)·B(제4사분면), 삼각형 AF′B 그림"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 타원·삼각형 AF′B 좌표평면 그림",
    note="4a = 60 → a = 15, b² = 225−81 = 144 → 단축 24. 빠른정답 3과 불일치.")

add(id="ddb1b4b0", qtype="choice",
    question=("다음 그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원과 꼭짓점이 원점 O이고 점 F를 초점으로 하는 포물선이 있다. "
              "타원과 포물선이 만나는 점 중 제1사분면 위의 점을 P라 하고, 점 P에서 직선 [[x = -c]]에 내린 수선의 발을 Q라 하자.\n"
              "[[seg(FP) = 15]]이고 삼각형 FPQ의 넓이가 60일 때, 타원의 장축의 길이는?"),
    choices=["[[30]]", "[[32]]", "[[34]]", "[[36]]", "[[38]]"],
    derived_answer="②", figure=fig("좌표평면: 초점 F′·F인 타원, 꼭짓점 원점·초점 F인 포물선, 직선 x=−c, 교점 P, 수선의 발 Q, 선분 PF·QF 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 타원·포물선·직선 x=−c·점 P, Q, F, F′ 좌표평면 그림",
    note="출처 [2022년 4월 고3 기하 25번 변형]. PQ=PF=15, 높이 y_P=8, PF′=√(15²+8²)=17 → 장축 32 → ②.")

add(id="5459d9e3", qtype="short",
    question=("다음 그림과 같이 두 초점이\n[[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 타원 [[sub(E,1)]]이 있다.\n타원 [[sub(E,1)]]의 꼭짓점 중 [[x]]좌표가 양수인 점을 A라 하고, "
              "두 점 A, F를 초점으로 하고 점 F′을 지나는 타원을 [[sub(E,2)]]라 하자. 두 타원 [[sub(E,1)]], [[sub(E,2)]]의 교점 중 [[y]]좌표가 양수인 점 B에 대하여 "
              "BF′ − [[seg(BA)]] = [[frac(1, 3)]]AF′이 성립한다. 타원 [[sub(E,2)]]의 단축의 길이가 [[4 sqrt(7)]]일 때, [[9 pow(c, 2)]]의 값을 구하시오."),
    choices=None, derived_answer="21", figure=fig("좌표평면: 큰 타원 E₁(초점 F′·F, 오른쪽 꼭짓점 A)과 타원 E₂(초점 A·F, F′ 통과), 교점 B(위), 선분 BF′·BA 그림"),
    difficulty_est=4, confidence=0.85, needs_review="도형 표현 불가: 두 타원 E₁·E₂·점 A, B, F, F′ 좌표평면 그림 / 프라임 점 라벨(선분 BF′, AF′ 윗줄 표기 생략)",
    note="출처 [2024년 5월 고3 기하 30번 변형]. a=5c, E₂: 장반경 4c, 초점거리 2c → 단축 4√3c = 4√7 → c² = 7/3 → 9c² = 21. 빠른정답 5와 불일치.")

add(id="74919f53", qtype="choice",
    question=_p28e_body.format(LEAD="그림과 같이 ", PT="[[point(0, n)]]", CONJ="일 때", PER="[[12 sqrt(2)]]"),
    choices=["[[11]]", "[[12]]", "[[13]]", "[[14]]", "[[15]]"],
    derived_answer="②", figure=fig("좌표평면: x축 위의 두 점 F′·F와 y축 위의 점 P(직각 표시)로 이루어진 직각이등변삼각형 PF′F 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p28e_rev,
    note="출처 [2015년 10월 고3 이과 14번/4점]. 4a = 12√2 → PF=3√2, F′Q=√2, PQ=4√2 → 넓이 12 → ②. 빠른정답 4와 불일치.")

add(id="6c3e46c0", qtype="choice",
    question=("타원 [[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), 13) = 1]]의 두 초점을 F, F′이라 하자.\n점 F를 지나고 [[x]]축에 수직인 직선 위의 점 A가 AF′ = 13, [[seg(AF) = 5]]를 만족시킨다. "
              "선분 AF′과 타원이 만나는 점을 P라 할 때, 삼각형 PF′F의 둘레의 길이는?\n(단, [[a]]는 [[a > sqrt(13)]]인 상수이다.)"),
    choices=["[[20]]", "[[22]]", "[[24]]", "[[26]]", "[[28]]"],
    derived_answer="④", figure=fig("좌표평면: 초점 F′·F인 타원, F를 지나는 수직선 위의 점 A, 선분 AF′과 타원의 교점 P, 선분 PF, F에서 직각 표시 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 타원·수직선·점 A, P, F, F′ 좌표평면 그림 / 프라임 점 라벨(선분 AF′ 윗줄 표기 생략)",
    note="출처 [2022년 9월 고3 기하 25번 변형]. FF′=12, a²=13+36 → a=7 → 둘레 14+12 = 26 → ④. 빠른정답 2와 불일치.")

add(id="8b9bc61f", qtype="choice",
    question=("다음 그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원 [[sub(C,1)]]: [[frac(pow(x,2), pow(a,2)) + pow(y,2) = 1]]과 "
              "두 점 [[G(0, d)]], G′[[point(0, -d)]] ([[d > 1]])을 초점으로 하고 타원 [[sub(C,1)]]의 두 꼭짓점을 지나는 타원 [[sub(C,2)]]가 있다. "
              "직선 FG가 타원 [[sub(C,1)]]과 제1사분면에서 만나는 점을 P라 하고, 직선 F′P가 타원 [[sub(C,2)]]와 제1사분면에서 만나는 점을 Q라 하자.\n"
              "[[seg(GP) = seg(PF)]]이고 [[seg(GP)]] + PF′ = [[2 sqrt(5)]]일 때, [[seg(QG)]] + QG′의 값은? (단, [[a]]는 양수이다.)"),
    choices=["[[frac(sqrt(205), 5)]]", "[[frac(2 sqrt(205), 5)]]", "[[frac(3 sqrt(205), 5)]]", "[[frac(4 sqrt(205), 5)]]", "[[sqrt(205)]]"],
    derived_answer="②", figure=fig("좌표평면: 가로로 긴 타원 C₁(초점 F′·F)과 세로로 긴 타원 C₂(초점 G·G′), 점 P(C₁ 위)·Q(C₂ 위), 선분 GP·GQ·F′Q·FQ 그림"),
    difficulty_est=4, confidence=0.85, needs_review="도형 표현 불가: 두 타원 C₁·C₂·점 P, Q, F, F′, G, G′ 좌표평면 그림 / 프라임 점 라벨(선분 PF′, QG′ 윗줄 표기 생략)",
    note="출처 [2025년 6월 고3 기하 28번 변형]. 2a=2√5, c=2, P는 FG의 중점 (1, d/2) → d²=16/5 → QG+QG′ = 2√(5+16/5) = 2√205/5 → ②.")

add(id="c4747fee", qtype="short",
    question=("그림과 같이 [[y]]축 위의 점 [[A(0, a)]]와 두 점 F, F′을 초점으로 하는 타원 [[frac(pow(x,2), 25) + frac(pow(y,2), 9) = 1]] 위를 움직이는 점 P가 있다. "
              "[[seg(AP) - seg(FP)]]의 최솟값이 1일 때, [[pow(a, 2)]]의 값을 구하시오."),
    choices=None, derived_answer="105", figure=fig("좌표평면: 타원 x²/25+y²/9=1(초점 F′·F), y축 위의 점 A, 타원 위의 점 P, 선분 AP·PF 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 타원·점 A, P, F, F′ 좌표평면 그림",
    note="출처 [2013년 11월 고3 이과 27번/4점]. AP−FP = AP+F′P−10 ≥ AF′−10 = 1 → AF′=11 → a² = 121−16 = 105. 빠른정답 4와 불일치.")

add(id="7da6d4f9", qtype="short",
    question=("한 초점이 [[F(c, 0)]] ([[c > 0]])인 타원 [[frac(pow(x,2), 9) + frac(pow(y,2), 5) = 1]]과 중심의 좌표가 [[point(2, 3)]]이고 반지름의 길이가 [[r]]인 원이 있다. "
              "타원 위의 점 P와 원 위의 점 Q에 대하여 [[seg(PQ) - seg(PF)]]의 최솟값이 6일 때, [[r]]의 값을 구하시오."),
    choices=None, derived_answer="17", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2023년 9월 고3 기하 29번/4점]. PQ−PF = PQ+PF′−6 ≥ (r−CF′)−6 = r−11 (원이 타원을 포함) = 6 → r = 17. 빠른정답 2와 불일치.")

_p48_body = ("두 초점이 F, F′인 타원 {ELL}이 있다.\n원 {CIR} 위의 점 P에 대하여 직선 F′P가 이 타원과 만나는 점 중 [[y]]좌표가 양수인 점을 Q라 하자.\n"
             "[[seg(PQ) + seg(FQ)]]의 최댓값을 구하시오.")
_p48_rev = "도형 표현 불가: 타원·원·점 P, Q, F, F′ 좌표평면 그림"

add(id="0635f095", qtype="short",
    question=_p48_body.format(ELL="[[frac(pow(x,2), 49) + frac(pow(y,2), 33) = 1]]", CIR="[[pow(x,2) + pow(y - 3, 2) = 4]]"),
    choices=None, derived_answer="11", figure=fig("좌표평면: 타원 x²/49+y²/33=1(초점 F′·F), 타원 내부의 원 x²+(y−3)²=4, 원 위의 점 P, 직선 F′P와 타원의 교점 Q, 선분 FQ 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p48_rev,
    note="출처 [2018년 11월 고3 이과 28번/4점]. PQ+FQ = 14−F′P, F′P 최솟값 = 5−2 = 3 → 11. 빠른정답 1과 불일치.")

add(id="3da08b06", qtype="short",
    question=_p48_body.format(ELL="[[frac(pow(x,2), 100) + frac(pow(y,2), 52) = 1]]", CIR="[[pow(x,2) + pow(y - 4, 2) = 9]]"),
    choices=None, derived_answer="15", figure=fig("좌표평면: 타원 x²/100+y²/52=1(초점 F′·F), 타원 내부의 원 x²+(y−4)²=9, 원 위의 점 P, 직선 F′P와 타원의 교점 Q, 선분 FQ 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p48_rev,
    note="c=4√3, F′C = 8, F′P 최솟값 5 → 20−5 = 15. 빠른정답 3과 불일치.")

add(id="c58423de", qtype="choice",
    question=("두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])이고 장축의 길이가 2인 타원이 있다. 이 타원 위에 있는 제2사분면 위의 점 P에 대하여 직선 F′P가 [[y]]축과 점 Q에서 만난다. "
              "직선 FP가 선분 F′Q의 수직이등분선일 때, [[c]]의 값은?"),
    choices=["[[3 - 2 sqrt(2)]]", "[[sqrt(2) - 1]]", "[[2 sqrt(2) - 3]]", "[[sqrt(3) - 1]]", "[[2 sqrt(2) - 2]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2025년 3월 고3 기하 26번/3점]. FQ=FF′=2c → Q(0,√3c), P는 F′Q의 중점, PF′=c, PF=√3c → c(1+√3)=2 → c=√3−1 → ④. 빠른정답 2와 불일치.")

add(id="2be5d1d4", qtype="choice",
    question=("두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])이고 장축의 길이가 32인 타원을 [[sub(C,1)]]이라 하자. 점 F를 지나고 [[x]]축에 수직인 직선이 타원 [[sub(C,1)]]과 제1사분면에서 만나는 점을 A라 하고, "
              "두 초점이 F, A이고 점 [[P(16, 0)]]을 지나는 타원을 [[sub(C,2)]]라 하자. 두 타원 [[sub(C,1)]]과 [[sub(C,2)]]가 만나는 점 중 점 P가 아닌 점을 Q라 하자. "
              "cos(∠FF′A) = [[frac(24, 25)]]일 때,\nF′Q − [[seg(AQ)]]의 값은?"),
    choices=["[[28 - sqrt(65)]]", "[[37 - 2 sqrt(65)]]", "[[30 - sqrt(65)]]", "[[39 - 2 sqrt(65)]]", "[[32 - sqrt(65)]]"],
    derived_answer="①", figure=fig("좌표평면: 큰 타원 C₁(초점 F′·F, 오른쪽 꼭짓점 P(16,0))과 작은 타원 C₂(초점 F·A), F를 지나는 수직선 위의 점 A, 교점 Q, 직각 표시 그림"),
    difficulty_est=4, confidence=0.85, needs_review="도형 표현 불가: 두 타원 C₁·C₂·점 A, P, Q, F, F′ 좌표평면 그림 / 프라임 점 라벨(∠FF′A, 선분 F′Q 텍스트 혼합)",
    note="출처 [2024년 3월 고3 기하 28번 변형]. AF′=25, FF′=24, AF=7, c=12; C₂ 장축 = 4+√65 → F′Q−AQ = 32−(4+√65) = 28−√65 → ①. 빠른정답 18과 불일치.")

_p63_body = ("두 점 [[F(0, {C})]], F′[[point(0, -{C})]]를 초점으로 하는 타원 [[sub(C,1)]]에 대하여 점 F를 지나고 [[x]]축과 평행한 직선이 타원 [[sub(C,1)]]과 만나는 점 중 제1사분면 위에 있는 점을 P, "
             "선분 PF′과 [[x]]축이 만나는 점을 Q라 하자. 두 점 P, F를 초점으로 하고 점 Q가 꼭짓점인 타원 [[sub(C,2)]]에 대하여{BR}두 타원 [[sub(C,1)]], [[sub(C,2)]]가 만나는 점 중 [[x]]축에 가까운 점을 R이라 하자.\n"
             "F′R − [[seg(PR)]] = {D}일 때, 두 타원 [[sub(C,1)]], [[sub(C,2)]]의 장축의 길이의 {ASK}을 구하시오.")
_p63_fig = "좌표평면: 세로로 긴 타원 C₁(초점 F·F′ y축 위)과 타원 C₂(초점 P·F), 점 P(F와 같은 높이), 선분 PF′과 x축의 교점 Q, 교점 R(x축 근처) 그림"
_p63_rev = "도형 표현 불가: 두 타원 C₁·C₂·점 P, Q, R, F, F′ 좌표평면 그림 / 프라임 점 라벨(선분 F′R 윗줄 표기 생략)"

add(id="c78e6374", qtype="short",
    question=_p63_body.format(C="4", BR="\n", D="6", ASK="합"),
    choices=None, derived_answer="26", figure=fig(_p63_fig), difficulty_est=4, confidence=0.85, needs_review=_p63_rev,
    note="출처 [2025년 9월 고3 기하 29번 변형]. P(p,4), Q는 PF′ 중점, 2a₂=PF′, F′R−PR = 2a₁−2a₂ = p = 6 → PF′=10 → 16+10 = 26. 빠른정답 160과 불일치.")

add(id="e064c42b", qtype="short",
    question=_p63_body.format(C="6", BR=" ", D="[[7 sqrt(2)]]", ASK="곱"),
    choices=None, derived_answer="396", figure=fig(_p63_fig), difficulty_est=4, confidence=0.85, needs_review=_p63_rev,
    note="출처 [2025년 9월 고3 기하 29번/4점]. p=7√2, PF′=√(98+144)=11√2 → 장축 18√2·11√2 = 396. 빠른정답 23과 불일치.")

add(id="f8baf748", qtype="choice",
    question="두 점 [[F(1, 0)]], F′[[point(-1, 0)]]에 대하여 점 P가 [[seg(PF)]] + PF′ = 6을 만족시킬 때, 점 P가 나타내는 도형의 방정식은?",
    choices=["[[frac(pow(x,2), 9) + frac(pow(y,2), 8) = 1]]", "[[frac(pow(x,2), 9) + frac(pow(y,2), 6) = 1]]", "[[frac(pow(x,2), 9) + frac(pow(y,2), 4) = 1]]",
             "[[frac(pow(x,2), 8) + frac(pow(y,2), 9) = 1]]", "[[frac(pow(x,2), 6) + frac(pow(y,2), 9) = 1]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.85, needs_review="프라임 점 라벨(선분 PF′ 윗줄 표기 생략)",
    note="a=3, c=1, b²=8 → x²/9+y²/8=1 → ①. 빠른정답 63과 불일치.")

add(id="bfd11f73", qtype="choice",
    question="두 점 [[A(0, 2)]], [[B(0, -2)]]에 대하여 점 P가 [[seg(PA) + seg(PB) = 2 sqrt(5)]]를 만족시킬 때, 점 P가 나타내는 도형의 방정식은?",
    choices=["[[pow(x,2) + frac(pow(y,2), 5) = 1]]", "[[frac(pow(x,2), 5) + pow(y,2) = 1]]", "[[frac(pow(x,2), 2) + frac(pow(y,2), 5) = 1]]",
             "[[frac(pow(x,2), 5) + frac(pow(y,2), 2) = 1]]", "[[frac(pow(x,2), 3) + frac(pow(y,2), 5) = 1]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="장축 y축, a=√5, c=2, b²=1 → x²+y²/5=1 → ①. 빠른정답 3과 불일치.")

_p78_body = ("[[x]]축 위의 점 A와 [[y]]축 위의 점 B에 대하여 [[seg(AB) = {L}]]일 때, 선분 AB를 [[ratio(2, 1)]]로 내분하는 점 P의 자취의 방정식은 [[p pow(x,2) + q pow(y,2) = {K}]]이다. "
             "상수 [[p]], [[q]]에 대하여 {ASK}의 값을 구하시오.")

add(id="f9bee809", qtype="short",
    question=_p78_body.format(L="12", K="64", ASK="[[p + q]]"),
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="A(s,0), B(0,t), P=(s/3, 2t/3), s²+t²=144 → 9x²+9y²/4=144 → 4x²+y²=64 → p+q = 5. 빠른정답 4와 불일치.")

add(id="5a36bdfd", qtype="choice",
    question="두 점 [[A(0, 0)]], [[B(4, 0)]]에 대하여 [[seg(PA) + seg(PB) = 6]]을 만족시키는 점 [[P(x, y)]]가 나타내는 도형의 단축의 길이와 장축의 길이의 곱은?",
    choices=["[[6 sqrt(5)]]", "[[8 sqrt(5)]]", "[[10 sqrt(5)]]", "[[12 sqrt(5)]]", "[[14 sqrt(5)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a=3, c=2, b=√5 → 6·2√5 = 12√5 → ④. 빠른정답 2와 불일치.")

add(id="93e6c48c", qtype="short",
    question=_p78_body.format(L="6", K="16", ASK="[[p - q]]"),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="P=(s/3, 2t/3), s²+t²=36 → 4x²+y²=16 → p−q = 3. 빠른정답 36과 불일치.")

_p87_ch = "[[subset(X, setb(point(x, y), frac(pow(x - {A}, 2), 9) {SIGN} frac(pow({Y}, 2), 5) = 1))]]"
add(id="27aeb8b6", qtype="choice",
    question=("좌표평면에서 원 [[pow(x,2) + pow(y,2) = 36]] 위를 움직이는 점 [[P(a, b)]]와 점 [[A(4, 0)]]에 대하여 다음 조건을 만족시키는 점 Q 전체의 집합을 [[X]]라 하자. (단, [[b != 0]])\n"
              "(가) 점 Q는 선분 OP 위에 있다.\n(나) 점 Q를 지나고 직선 AP에 평행한 직선이 [[angle(OQA)]]를 이등분한다.\n집합의 포함관계로 옳은 것은?"),
    choices=[_p87_ch.format(A="1", SIGN="-", Y="y - 1"), _p87_ch.format(A="2", SIGN="+", Y="y - 1"), _p87_ch.format(A="1", SIGN="-", Y="y"),
             _p87_ch.format(A="1", SIGN="+", Y="y"), _p87_ch.format(A="2", SIGN="+", Y="y")],
    derived_answer="⑤", figure=fig("좌표평면: 원 x²+y²=36, 원 위의 점 P, 선분 OP 위의 점 Q, 점 A(4,0), 선분 QA·PA, Q에서의 각 이등분 표시(점 2개) 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 원·점 P, Q, A·각 이등분 표시 좌표평면 그림",
    note="출처 [2008년 9월 고3 이과 8번]. 이등분선∥AP → QA=QP → OQ+QA = OP = 6 → 초점 O, A 타원 (x−2)²/9+y²/5=1 → ⑤.")

# ───────────────────────── 쌍곡선의 접선의 방정식 ─────────────────────────
add(id="7e1c4995", qtype="choice",
    question=("쌍곡선 [[7 pow(x,2) - 3 pow(y,2) = 21]]에 접하고 [[x]]축의 양의 방향과 이루는 각의 크기가 [[deg(60)]]인 직선의 방정식이 [[y = m x + n]]일 때, [[pow(m,2) + pow(n,2)]]의 값은?\n"
              "(단, [[m]], [[n]]은 상수이다.)"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="x²/3−y²/7=1, m=√3, n²=3·3−7=2 → 3+2 = 5 → ⑤.")

add(id="bd5b6eb0", qtype="choice",
    question=("양수 [[a]]에 대하여 두 초점이 F, F′인\n쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(a,2)) = -1]] 위의 점 [[point(a, sqrt(2) a)]]에서의 접선이 [[y]]축과 만나는 점을 P라 하자. "
              "[[seg(PF)]] · PF′ = 8일 때, [[a]]의 값은?"),
    choices=["[[sqrt(3)]]", "[[frac(4 sqrt(3), 3)]]", "[[frac(5 sqrt(3), 3)]]", "[[2 sqrt(3)]]", "[[frac(7 sqrt(3), 3)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85, needs_review="프라임 점 라벨(선분 PF′ 윗줄 표기 생략)",
    note="출처 [2025년 11월 고3 기하 26번/3점]. 접선 x−√2y=−a → P(0, a/√2), 초점 (0,±√2a) → PF·PF′ = (a/√2)(3a/√2) = 3a²/2 = 8 → a = 4√3/3 → ②. 빠른정답 1과 불일치.")

add(id="a349012e", qtype="short",
    question=("다음 그림과 같이 꼭짓점의 좌표가 [[point(3 sqrt(2), 0)]], [[point(-3 sqrt(2), 0)]]이고 두 초점이 [[F(6, 0)]], F′[[point(-6, 0)]]인 쌍곡선이 있다. "
              "이 쌍곡선의 제1사분면 위의 점 P에서의 접선을 [[l]]이라 하고, 원점 O를 지나고 접선 [[l]]과 점 Q에서 수직으로 만나는 직선이 쌍곡선과 제2사분면에서 만나는 점을 R라 하자. "
              "이때 [[seg(OQ)]] · [[seg(OR)]]의 값을 구하시오."),
    choices=None, derived_answer="18",
    figure=fig("좌표평면: 쌍곡선(꼭짓점 ±3√2, 초점 F′(−6,0)·F(6,0)), 제1사분면 점 P에서의 접선 l, 원점에서 l에 내린 수선의 발 Q(직각 표시), 수선의 연장과 쌍곡선의 제2사분면 교점 R 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 쌍곡선·접선 l·점 P, Q, R, F, F′ 좌표평면 그림",
    note="x²−y²=18: 접선 x₀x−y₀y=18, OQ = 18/√(x₀²+y₀²), R = (−x₀, y₀) → OR = √(x₀²+y₀²) → 곱 18.")

_p53_body = ("쌍곡선 {HYP} 위의 점 {PT}에서의 접선 [[l]]에 대하여 원점 O를 지나고 직선 [[l]]에 수직인 직선이 직선 [[l]]과 만나는 점을 H, 쌍곡선과 제1사분면에서 만나는 점을 Q라 {WHEN} "
             "[[frac(seg(OH), seg(OQ))]]의 값{TAIL}")
_p53_rev = "도형 표현 불가: 쌍곡선·접선 l·점 P, H, Q 좌표평면 그림"

add(id="4865807a", qtype="short",
    question=_p53_body.format(HYP="[[pow(x,2) - frac(pow(y,2), 3) = 1]]", PT="[[P(-2, 3)]]", WHEN="할 때,", TAIL="은 [[a sqrt(33)]]이다.\n[[30a]]의 값을 구하시오. (단, [[a]]는 유리수)"),
    choices=None, derived_answer="2", figure=fig("좌표평면: 쌍곡선 x²−y²/3=1, 제2사분면 점 P에서의 접선 l, 원점을 지나 l에 수직인 직선, 수선의 발 H(직각 표시), 제1사분면 교점 Q 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p53_rev,
    note="접선 2x+y=−1, OH=1/√5; 직선 y=x/2와 쌍곡선: t²=3/11, OQ=√(15/11) → 비 √33/15 → a=1/15 → 30a = 2. 빠른정답 1과 불일치.")

add(id="321c793e", qtype="short",
    question=("쌍곡선 [[pow(x,2) - pow(y,2) = 32]] 위의 점 [[P(-6, 2)]]에서의 접선 [[l]]에 대하여 원점 O에서 [[l]]에 내린 수선의 발을 H, 직선 OH와 이 쌍곡선이 제1사분면에서 만나는 점을 Q라 하자.\n"
              "두 선분 OH와 OQ의 길이의 곱 [[seg(OH)]] · [[seg(OQ)]]를 구하시오."),
    choices=None, derived_answer="32", figure=fig("좌표평면: 쌍곡선 x²−y²=32, 제2사분면 점 P(−6,2)에서의 접선 l, 원점에서 l에 내린 수선의 발 H(직각 표시), 직선 OH와 쌍곡선의 제1사분면 교점 Q 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p53_rev,
    note="접선 3x+y=−16, OH=16/√10; 직선 y=x/3와 쌍곡선: Q(6,2), OQ=2√10 → 곱 32. 빠른정답 2와 불일치.")

add(id="884ec30d", qtype="short",
    question=_p53_body.format(HYP="[[pow(x,2) - frac(pow(y,2), 4) = 1]]", PT="[[P(-sqrt(2), 2)]]", WHEN="하자.", TAIL="을 [[frac(b sqrt(31), a)]]라 할 때, [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="10", figure=fig("좌표평면: 쌍곡선 x²−y²/4=1, 제2사분면 점 P에서의 접선 l, 원점을 지나 l에 수직인 직선, 수선의 발 H(직각 표시), 제1사분면 교점 Q 그림"),
    difficulty_est=3, confidence=0.85, needs_review=_p53_rev,
    note="접선 2√2x+y=−2, OH=2/3; t²=4/31, OQ=6/√31 → 비 √31/9 → a+b = 10.")

add(id="91d1d4ae", qtype="short",
    question=("그림과 같이 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 27) = 1]] 위의 점 [[P(frac(9, 2), k)]] ([[k > 0]])에서의 접선이 "
              "[[x]]축과 만나는 점을 Q라 하자. 두 점 F, F′을 초점으로 하고 점 Q를 한 꼭짓점으로 하는 쌍곡선이 선분 PF′과 만나는 두 점을 R, S라 하자.\n"
              "[[seg(RS) + seg(SF) = seg(RF) + 8]]일 때, [[4(pow(a,2) + pow(k,2))]]의 값을 구하시오.\n(단, [[a]]는 양수이고, 점 R의 [[x]]좌표는 점 S의 [[x]]좌표보다 크다.)"),
    choices=None, derived_answer="171",
    figure=fig("좌표평면: 쌍곡선 x²/a²−y²/27=1(초점 F′·F), 점 P에서의 접선과 x축의 교점 Q, Q를 꼭짓점으로 하는 두 번째 쌍곡선, 선분 PF′과의 교점 R(오른쪽)·S(왼쪽), 선분 RF·SF·PF 그림"),
    difficulty_est=4, confidence=0.85, needs_review="도형 표현 불가: 두 쌍곡선·접선·점 P, Q, R, S, F, F′ 좌표평면 그림",
    note="출처 [2023년 4월 고3 기하 29번/4점]. Q(2a²/9,0)=꼭짓점, (RF′−RF)+(SF−SF′) = 4a₂ = 8 → a₂=2 → a²=9, k²=135/4 → 4(9+135/4) = 171.")

_p72_body = ("두 초점이 [[F(0, c)]], F′[[point(0, -c)]] ([[c > 0]])인\n쌍곡선 {HYP} 위의 점 P가 제2사분면에 있다.\n삼각형 PF′F의 둘레의 길이가 {PER}일 때, 이 쌍곡선 위의 점 P에서의 접선의 {ASK}은?")

add(id="98d968cf", qtype="choice",
    question=_p72_body.format(HYP="[[frac(pow(x,2), 11) - frac(pow(y,2), 25) = -1]]", PER="36", ASK="[[y]]절편"),
    choices=["[[1]]", "[[frac(3, 2)]]", "[[2]]", "[[frac(5, 2)]]", "[[3]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2025년 9월 고3 기하 27번 변형]. c=6, PF′=17, PF=7 → P(−√33, 10), 접선 y절편 25/10 = 5/2 → ④.")

add(id="d143dddc", qtype="short",
    question=("다음 그림과 같이 곡선 [[pow(x,2) - pow(y,2) = 8]] ([[x > 0]]) 위의 점 P에서 [[x]]축에 내린 수선의 발을 H라 하고, 점 P에서의 접선이 [[x]]축과 만나는 점을 Q라 할 때,\n"
              "[[seg(OH)]] · [[seg(OQ)]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=fig("좌표평면: 쌍곡선 x²−y²=8의 오른쪽 가지, 점 P, x축 위 수선의 발 H(직각 표시), P에서의 접선과 x축의 교점 Q 그림"),
    difficulty_est=2, confidence=0.85, needs_review="도형 표현 불가: 쌍곡선·접선·점 P, H, Q 좌표평면 그림",
    note="접선 x₀x−y₀y=8 → OQ = 8/x₀, OH = x₀ → 곱 8. 빠른정답 4와 불일치.")

add(id="7c33dcb6", qtype="choice",
    question=("두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인\n쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), k) = 1]] 위의 제1사분면에 있는 점 P에서의 접선이 [[x]]축과 만나는 점의 [[x]]좌표가 2이다. "
              "PF′ = FF′일 때, 양수 [[k]]의 값은?"),
    choices=["[[18]]", "[[21]]", "[[24]]", "[[27]]", "[[30]]"],
    derived_answer="④", figure=fig("좌표평면: 쌍곡선 x²/9−y²/k=1(초점 F′·F), 제1사분면 점 P, P에서의 접선(x축과 x=2에서 만남), 선분 PF′ 그림"),
    difficulty_est=3, confidence=0.85, needs_review="도형 표현 불가: 쌍곡선·접선·점 P, F, F′ 좌표평면 그림 / 프라임 점 라벨(선분 PF′, FF′ 윗줄 표기 생략)",
    note="출처 [2022년 7월 고3 기하 26번 변형]. 9/x₀=2 → x₀=9/2, PF′=2c, PF=3c/2−3 = 2c−6 → c=6 → k=27 → ④. 빠른정답 1과 불일치.")

_p80_body = ("다음 그림과 같이 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]] 위의\n점 [[P({X}, k)]] ([[k > 0]])에서의 접선이 [[x]]축과 만나는 점을 Q, [[y]]축과 만나는 점을 R라 하자. "
             "점 [[S({X}, 0)]]에 대하여 삼각형 QOR의 넓이를 [[sub(A,1)]], 삼각형 PRS의 넓이를 [[sub(A,2)]]라 하자. [[ratio(sub(A,1), sub(A,2)) = ratio({R1}, {R2})]]일 때, 이 쌍곡선의 주축의 길이는?\n"
             "(단, O는 원점이고, [[a]], [[b]]는 상수이다.)")
_p80_fig = "좌표평면: 쌍곡선 x²/a²−y²/b²=1, 오른쪽 가지 위의 점 P에서의 접선, x축 교점 Q, y축 교점 R(음의 방향), 점 S(x축), 삼각형 QOR과 삼각형 PRS 음영 그림"
_p80_rev = "도형 표현 불가: 쌍곡선·접선·삼각형 QOR, PRS 음영 좌표평면 그림"

add(id="ae303fea", qtype="choice",
    question=_p80_body.format(X="3", R1="4", R2="3"),
    choices=["[[4]]", "[[2 sqrt(5)]]", "[[2 sqrt(6)]]", "[[2 sqrt(7)]]", "[[4 sqrt(2)]]"],
    derived_answer="③", figure=fig(_p80_fig), difficulty_est=3, confidence=0.85, needs_review=_p80_rev,
    note="Q(a²/3,0), R(0,−b²/k); A₁=a²b²/(6k), A₂=3k/2 → a²b²=12k², k²=b²(9−a²)/a² → a⁴+12a²−108=0 → a²=6 → 2√6 → ③. 빠른정답 4와 불일치.")

add(id="41de44c0", qtype="choice",
    question=_p80_body.format(X="2", R1="9", R2="4"),
    choices=["[[2 sqrt(2)]]", "[[2 sqrt(3)]]", "[[4]]", "[[2 sqrt(5)]]", "[[2 sqrt(6)]]"],
    derived_answer="②", figure=fig(_p80_fig), difficulty_est=3, confidence=0.85, needs_review=_p80_rev,
    note="A₁=a²b²/(4k), A₂=k → a²b²=9k² → a⁴+9a²−36=0 → a²=3 → 2√3 → ②.")

add(id="4a1d6d3a", qtype="choice",
    question=_p80_body.format(X="5", R1="16", R2="5"),
    choices=["[[4 sqrt(3)]]", "[[8]]", "[[4 sqrt(5)]]", "[[4 sqrt(6)]]", "[[4 sqrt(7)]]"],
    derived_answer="③", figure=fig(_p80_fig), difficulty_est=3, confidence=0.85, needs_review=_p80_rev,
    note="A₁=a²b²/(10k), A₂=5k/2 → a²b²=80k² → a⁴+80a²−2000=0 → a²=20 → 4√5 → ③. 빠른정답 2와 불일치.")

add(id="160b20bc", qtype="choice",
    question=_p72_body.format(HYP="[[frac(pow(x,2), 9) - frac(pow(y,2), 16) = -1]]", PER="30", ASK="기울기"),
    choices=["[[-frac(7 sqrt(3), 9)]]", "[[-frac(2 sqrt(3), 3)]]", "[[-frac(5 sqrt(3), 9)]]", "[[-frac(4 sqrt(3), 9)]]", "[[-frac(sqrt(3), 3)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2025년 9월 고3 기하 27번/3점]. c=5, PF′=14, PF=6 → P(−3√3, 8), 접선 −(√3/3)x−y/2=−1 → 기울기 −2√3/3 → ②. 빠른정답 3과 불일치.")
