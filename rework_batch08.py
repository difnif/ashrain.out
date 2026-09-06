# -*- coding: utf-8 -*-
# batch08 (74문항: esc_sonnet_h3-3_4of6 35, esc_sonnet_h3-3_5of6 8, esc_sonnet_h3-3_6of6 10, esc_sonnet_m1-1_1of3 6, m1-1_2of3 5, m1-1_3of3 9, esc_opus_m1-2_1of1 1) — v1.5 문법 재작업
# 핵심 교체(고3 기하): 프라임·첨자 점 라벨 → seg(PF'), seg(OH1), angle(PFF'), vec(OP'), vec(OA1), vec(O1P), seg(A1A2), seg(FP0)
#            좌표 붙은 첨자 점 → app(sub(F,1), 4, 0) / 단독 점 이름 F′, P′, O′, O″ 와 '직선 H₁H₂'·'선분 PF′'(윗줄 없음)은 텍스트 그대로
#            길이의 곱 PF·PF′ → seg(PF) × seg(PF') / 비 → ratio(seg(AF'), seg(FF')) = ratio(1, 6) / 가변 첨자 OA⃗ₖ는 sub(vec(OA), k) 유지
# 도형(좌표평면·구·원기둥 등)은 unsupported(raw) 유지 — 도형만 남은 항목은 통과
# 여전히 보류(중1): 답이 원문자(㉠·㉡·㉢) 4건, 답 '+3000'·'+23'의 양의 부호 2건, 선지가 모두 그래프 1건, 정보가 그림에만 있음 2건(연산 상자·수직선),
#            사용자 정의 연산·기호(⊗ ◇ ⟨x⟩ ★ ◎ ◉ ▼ ◆ {a}) 9건 / 고3: 한 이미지에 별개 문항 2개(id 1개) 1건
ITEMS = []
def add(**kw): ITEMS.append(kw)

# ================= esc_sonnet_h3-3_4of6 =================
# 0. 1bc1beb5 — 정사영 p61: OH₁=OH₂=2 윗줄 → seg(OH1)=seg(OH2)
add(id="1bc1beb5", qtype="choice",
    question="좌표공간에 서로 평행한 두 평면 [[alpha]], [[beta]]와 중심이 O이고 반지름의 길이가 [[sqrt(13)]]인 구 [[S]]가 있다. 점 O에서 두 평면 [[alpha]], [[beta]]에 내린 수선의 발을 각각 [[sub(H,1)]], [[sub(H,2)]]라 하면 [[seg(OH1) = seg(OH2) = 2]]이다. 구 [[S]]가 평면 [[alpha]]와 만나서 생기는 원 위를 움직이는 점을 P, 구 [[S]]가 평면 [[beta]]와 만나서 생기는 원 위를 움직이는 점을 Q라 하자.\n삼각형 POQ의 평면 [[beta]] 위로의 정사영의 넓이가 최대일 때, 평면 POQ와 평면 [[beta]]가 이루는 각의 크기를 [[theta]]라 하자. [[cos(theta)]]의 값은? (단, 세 점 O, P, Q는 한 직선 위에 있지 않고, 직선 PQ와 직선 [[sub(H,1)]][[sub(H,2)]]는 서로 평행하지 않다.)",
    choices=["[[frac(2 sqrt(17), 17)]]", "[[frac(5 sqrt(17), 34)]]", "[[frac(3 sqrt(17), 17)]]", "[[frac(7 sqrt(17), 34)]]", "[[frac(4 sqrt(17), 17)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간: 구 S와 서로 평행한 두 평면 α(위)·β(아래), 중심 O, 수선의 발 H₁(α 위)·H₂(β 위), 점선 OH₁·OH₂ 그림"}}],
    confidence=0.85,
    note="출처 [2025년 10월 고3 기하 28번/4점]. 선분 OH₁=OH₂=2를 seg(OH1)=seg(OH2)로; 직선 H₁H₂(윗줄 없음)는 sub 텍스트 혼합. 답 ③ 유지")

# 1. e21bf112 — 정사영 p69 (변형: 반지름 5, OH=3)
add(id="e21bf112", qtype="choice",
    question="좌표공간에 서로 평행한 두 평면 [[alpha]], [[beta]]와 중심이 O이고 반지름의 길이가 5인 구 [[S]]가 있다. 점 O에서 두 평면 [[alpha]], [[beta]]에 내린 수선의 발을 각각 [[sub(H,1)]], [[sub(H,2)]]라 하면 [[seg(OH1) = seg(OH2) = 3]]이다. 구 [[S]]가 평면 [[alpha]]와 만나서 생기는 원 위를 움직이는 점을 P, 구 [[S]]가 평면 [[beta]]와 만나서 생기는 원 위를 움직이는 점을 Q라 하자.\n삼각형 POQ의 평면 [[beta]] 위로의 정사영의 넓이가 최대일 때, 평면 POQ와 평면 [[beta]]가 이루는 각의 크기를 [[theta]]라 하자. [[cos(theta)]]의 값은? (단, 세 점 O, P, Q는 한 직선 위에 있지 않고, 직선 PQ와 직선 [[sub(H,1)]][[sub(H,2)]]는 서로 평행하지 않다.)",
    choices=["[[frac(sqrt(34), 34)]]", "[[frac(sqrt(17), 17)]]", "[[frac(sqrt(34), 17)]]", "[[frac(2 sqrt(17), 17)]]", "[[frac(2 sqrt(34), 17)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간: 구 S와 서로 평행한 두 평면 α(위)·β(아래), 중심 O, 수선의 발 H₁(α 위)·H₂(β 위), 점선 OH₁·OH₂ 그림"}}],
    confidence=0.85,
    note="출처 [2025년 10월 고3 기하 28번 변형]. 선분 OH₁=OH₂=3을 seg(OH1)=seg(OH2)로. 답 ⑤ 유지(빠른정답 3과 불일치는 1차와 동일)")

# 2. 06733463 — 정사영 p89: 평면 O₁O₂O₃(기호 없음)은 sub 텍스트 혼합 그대로 → 통과
add(id="06733463", qtype="short",
    question="다음 그림과 같이 원기둥의 밑면 위에 놓여 있는 반지름의 길이가 1인 두 구 [[sub(S,1)]], [[sub(S,2)]]가 서로 한 점에서 만나고 모두 원기둥의 옆면에 접한다. 두 구 [[sub(S,1)]], [[sub(S,2)]] 위에 반지름의 길이가 1인 두 구 [[sub(T,1)]], [[sub(T,2)]]가 각각 아래쪽에 있는 두 구와 각각 한 점에서 만나면서 모두 원기둥의 옆면에 접한다. 또, 두 구 [[sub(T,1)]], [[sub(T,2)]] 위에 반지름의 길이가 1인 두 구 [[sub(U,1)]], [[sub(U,2)]]가 각각 아래쪽에 있는 두 구와 각각 한 점에서 만나면서 모두 원기둥의 옆면에 접한다.\n세 구 [[sub(S,1)]], [[sub(T,1)]], [[sub(U,2)]]의 중심을 각각 [[sub(O,1)]], [[sub(O,2)]], [[sub(O,3)]]라 할 때, 평면 [[sub(O,1)]][[sub(O,2)]][[sub(O,3)]]과 원기둥의 밑면이 이루는 예각의 크기를 [[theta]]라 하자. 이때 [[6 pow(cos(theta), 2)]]의 값을 구하시오.\n(단, 원기둥의 높이는 6보다 크다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "원기둥 안에 반지름 1인 구 6개가 3층으로 쌓인 그림: 아래 S₂(왼쪽)·S₁(오른쪽), 가운데 T₁(앞)·T₂(뒤), 위 U₂(왼쪽)·U₁(오른쪽)"}}],
    confidence=0.85,
    note="평면 O₁O₂O₃은 기호 없는 점 이름 나열이라 sub 텍스트 혼합 유지(문법 안). 답 2 유지(빠른정답 32와 불일치는 1차와 동일)")

# 3. 88eae011 — 정사영 p93 (2층 변형)
add(id="88eae011", qtype="short",
    question="다음 그림과 같이 원기둥의 밑면 위에 놓여 있는 반지름의 길이가 1인 두 구 [[sub(S,1)]], [[sub(S,2)]]가 서로 한 점에서 만나고 모두 원기둥의 옆면에 접한다. 두 구 [[sub(S,1)]], [[sub(S,2)]] 위에 반지름의 길이가 1인 두 구 [[sub(T,1)]], [[sub(T,2)]]가 각각 아래쪽에 있는 두 구와 각각 한 점에서 만나면서 모두 원기둥의 옆면에 접한다. 세 구 [[sub(S,1)]], [[sub(T,1)]], [[sub(T,2)]]의 중심을 각각 [[sub(O,1)]], [[sub(O,2)]], [[sub(O,3)]]라 할 때, 평면 [[sub(O,1)]][[sub(O,2)]][[sub(O,3)]]과 원기둥의 밑면이 이루는 예각의 크기를 [[theta]]라 하자. 이때 [[9 pow(cos(theta), 2)]]의 값을 구하시오.\n(단, 원기둥의 높이는 4보다 크다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "원기둥 안에 반지름 1인 구 4개가 2층으로 쌓인 그림: 아래 S₂(왼쪽)·S₁(오른쪽), 위 T₁(앞)·T₂(뒤)"}}],
    confidence=0.85,
    note="평면 O₁O₂O₃은 sub 텍스트 혼합 유지(문법 안). 답 3 유지")

# 4. 6a350f45 — 이차곡선 p6: PP′=QP′ 윗줄 → seg(PP')=seg(QP'); 점 F′·P′, '선분 F′P'(윗줄 없음)는 텍스트
add(id="6a350f45", qtype="short",
    question="두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[frac(pow(x,2), 4) - frac(pow(y,2), 5) = 1]]이 있다. 직선 [[x = c]]가 이 쌍곡선과 만나는 점 중 제1사분면 위의 점을 P, 제4사분면 위의 점을 P′이라 하자. 선분 F′P 위에 [[seg(PP') = seg(QP')]]인 점 Q를 잡자. 두 점 P, P′을 초점으로 하고 점 Q를 지나는 타원의 장축의 길이는 [[frac(q, p)]]이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/4−y²/5=1, 초점 F·F′, 직선 x=c와의 교점 P(제1사분면)·P′(제4사분면), 선분 F′P 위의 점 Q, 선분 QP′ 그림"}}],
    confidence=0.85,
    note="출처 [2025년 3월 고3 기하 29번/4점]. PP′=QP′ 윗줄을 seg(PP')=seg(QP')로. 답 128 재확인(c=3, P(3,5/2), QP=50/13, 장축 115/13) — 빠른정답 52와 불일치는 1차와 동일")

# 5. 48e268b7 — 이차곡선 p9: cos(∠PFF′) → cos((angle(PFF')))
add(id="48e268b7", qtype="short",
    question="초점이 [[F(p, 0)]] ([[p > 0]])이고 준선이 [[x = -p]]인 포물선이 있다. 점 F′[[point(-p, 0)]]에 대하여 [[cos((angle(PFF'))) = frac(7, 13)]]을 만족시키는 이 포물선 위의 점 중 제1사분면에 있는 점을 P라 하고, 선분 PF′의 중점을 R이라 하자. 두 점 O, F′을 초점으로 하고 점 R을 지나는 쌍곡선에 대하여 선분 PF′과 쌍곡선이 만나는 점 중 R이 아닌 점을 Q라 하자.\n삼각형 QOR의 둘레의 길이가 17일 때, 삼각형 PRO의 넓이를 [[S]]라 하자. [[pow(S, 2)]]의 값을 구하시오.\n(단, O는 원점이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선(초점 F, 준선 x=−p), 두 갈래 쌍곡선(초점 O·F′), 점 P(제1사분면)·R(PF′ 중점)·Q, 선분 PF′·PF 그림"}}],
    confidence=0.8,
    note="출처 [2026년 7월 고3 기하 29번 변형]. ∠PFF′를 angle(PFF')로. 답 750 유지(빠른정답 4와 불일치는 1차와 동일)")

# 6. 8ea3dba5 — 이차곡선 p11: PF′=16 윗줄 → seg(PF')
add(id="8ea3dba5", qtype="short",
    question="다음 그림과 같이 타원 [[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), pow(b,2)) = 1]]과\n쌍곡선 [[frac(pow(x,2), pow(b,2)) - frac(pow(y,2), pow(c,2)) = 1]]은 두 초점 F, F′을 공유한다.\n이 두 곡선의 한 교점 P에 대하여 [[seg(PF) = 4]], [[seg(PF') = 16]]일 때, [[pow(c, 2)]]의 값을 구하시오. (단, [[a]], [[b]], [[c]]는 상수)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 타원과 쌍곡선이 초점 F·F′을 공유, 제1사분면 교점 P와 선분 PF·PF′ 그림"}}],
    confidence=0.9,
    note="PF′=16 윗줄을 seg(PF')로. 답 28 유지")

# 7. e9be9648 — 이차곡선 p20: PF·PF′ → seg(PF) × seg(PF')
add(id="e9be9648", qtype="short",
    question="다음 그림과 같이 두 점 [[A(6, 0)]], [[B(-6, 0)]]을 장축의 양 끝 점으로 하는 타원의 두 초점을 F, F′이라 하고, 초점이 F이고 꼭짓점이 원점인 포물선이 타원과 만나는 두 점을 각각 P, Q라 하자. [[seg(PQ) = 4 sqrt(6)]]일 때,\n[[seg(PF) × seg(PF')]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 장축 양 끝 A·B인 타원, 초점 F′·F, 꼭짓점 원점·초점 F인 포물선, 교점 P(위)·Q(아래), 선분 PF·PF′·PQ 그림"}}],
    confidence=0.9,
    note="길이의 곱 PF·PF′을 seg(PF) × seg(PF')로. 답 35 유지(빠른정답 5와 불일치는 1차와 동일)")

# 8. ee5ae668 — 이차곡선 p21 (원문항: cos=1/5, 둘레 14)
add(id="ee5ae668", qtype="short",
    question="초점이 [[F(p, 0)]] ([[p > 0]])이고 준선이 [[x = -p]]인 포물선이 있다. 점 F′[[point(-p, 0)]]에 대하여 [[cos((angle(PFF'))) = frac(1, 5)]]을 만족시키는 이 포물선 위의 점 중 제1사분면에 있는 점을 P라 하고, 선분 PF′의 중점을 R이라 하자. 두 점 O, F′을 초점으로 하고 점 R을 지나는 쌍곡선에 대하여 선분 PF′과 쌍곡선이 만나는 점 중 R이 아닌 점을 Q라 하자.\n삼각형 QOR의 둘레의 길이가 14일 때, 삼각형 PRO의 넓이를 [[S]]라 하자. [[pow(S, 2)]]의 값을 구하시오.\n(단, O는 원점이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선(초점 F, 준선 x=−p), 두 갈래 쌍곡선(초점 O·F′), 점 P(제1사분면)·R(PF′ 중점)·Q, 선분 PF′·PF 그림"}}],
    confidence=0.8,
    note="출처 [2026년 7월 고3 기하 29번/4점]. ∠PFF′를 angle(PFF')로. 답 216 유지(빠른정답 4와 불일치는 1차와 동일)")

# 9. 1cc1862e — 이차곡선 p23
add(id="1cc1862e", qtype="short",
    question="다음 그림과 같이 두 점 [[A(5, 0)]], [[B(-5, 0)]]을 장축의 양 끝 점으로 하는 타원의 두 초점을 F, F′이라 하고, 초점이 F이고 꼭짓점이 원점인 포물선이 타원과 만나는 두 점을 각각 P, Q라 하자. [[seg(PQ) = 2 sqrt(10)]]일 때,\n[[seg(PF) × seg(PF')]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 장축 양 끝 A·B인 타원, 초점 F′·F, 꼭짓점 원점·초점 F인 포물선, 교점 P(위)·Q(아래), 선분 PF·PF′·PQ 그림"}}],
    confidence=0.9,
    note="길이의 곱 PF·PF′을 seg(PF) × seg(PF')로. 답 99/4 유지")

# 10. 0ed2a7b9 — 이차곡선 p28: PF′²−PF² → pow(seg(PF'),2) - pow(seg(PF),2)
add(id="0ed2a7b9", qtype="short",
    question="다음 그림과 같이 두 초점 F, F′을 공유하는\n타원 [[frac(pow(x,2), 36) + frac(pow(y,2), 11) = 1]]과 쌍곡선 [[frac(pow(x,2), 16) - frac(pow(y,2), 9) = 1]]이\n서로 다른 네 점에서 만난다. 타원과 쌍곡선의 교점 중 제1사분면에 있는 점 P에 대하여 [[pow(seg(PF'), 2) - pow(seg(PF), 2)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 타원 x²/36+y²/11=1과 쌍곡선 x²/16−y²/9=1(공통 초점 F′·F), 제1사분면 교점 P, 선분 PF·PF′ 그림"}}],
    confidence=0.9,
    note="PF′²−PF²를 pow(seg(PF'),2)−pow(seg(PF),2)로. 답 96 유지(빠른정답 5와 불일치는 1차와 동일)")

# 11. c5014261 — 이차곡선 p30
add(id="c5014261", qtype="short",
    question="다음 그림과 같이 두 초점 F, F′을 공유하는\n타원 [[frac(pow(x,2), 49) + frac(pow(y,2), 33) = 1]]과 쌍곡선 [[frac(pow(x,2), 4) - frac(pow(y,2), 12) = 1]]이\n서로 다른 네 점에서 만난다. 타원과 쌍곡선의 교점 중 제1사분면에 있는 점 P에 대하여 [[pow(seg(PF'), 2) - pow(seg(PF), 2)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 타원 x²/49+y²/33=1과 쌍곡선 x²/4−y²/12=1(공통 초점 F′·F), 제1사분면 교점 P, 선분 PF·PF′ 그림"}}],
    confidence=0.9,
    note="PF′²−PF²를 pow(seg(PF'),2)−pow(seg(PF),2)로. 답 56 유지(빠른정답 72와 불일치는 1차와 동일)")

# 12. 6bd16ab5 — 이차곡선 p33 (변형: x²/9−y²/7=1)
add(id="6bd16ab5", qtype="short",
    question="두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), 7) = 1]]이 있다. 직선 [[x = c]]가 이 쌍곡선과 만나는 점 중 제1사분면 위의 점을 P, 제4사분면 위의 점을 P′이라 하자. 선분 F′P 위에 [[seg(PP') = seg(QP')]]인 점 Q를 잡자. 두 점 P, P′을 초점으로 하고 점 Q를 지나는 타원의 장축의 길이는 [[frac(q, p)]]이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/9−y²/7=1, 초점 F·F′, 직선 x=c와의 교점 P(제1사분면)·P′(제4사분면), 선분 F′P 위의 점 Q, 선분 QP′ 그림"}}],
    confidence=0.85,
    note="출처 [2025년 3월 고3 기하 29번 변형]. PP′=QP′ 윗줄을 seg(PP')=seg(QP')로. 답 207 유지(빠른정답 56과 불일치는 1차와 동일)")

# 13. fe4681d2 — 이차곡선 p34: ∠F′FP → angle(F'FP); 답 미도출(초안대로 None)
add(id="fe4681d2", qtype="short",
    question="두 초점이 [[F(0, 3)]], F′[[point(0, -3)]]이고, 장축의 길이가 9인 타원이 있다. 이 타원 위에 있는 제1사분면 위의 점 중 [[angle(F'FP) = frac(pi, 3)]]를 만족시키는 점 P에 대하여 직선 FP가 [[x]]축과 만나는 점을 Q라 하자. 점 Q를 초점으로 하고 준선이 [[x = a]] ([[a < 0]])인 포물선이 점 P를 지난다. 직선 FP가 이 포물선과 만나는 점 중 P가 아닌 점을 R이라 할 때, [[seg(PR) = p + q sqrt(3)]]이다. [[p + q]]의 값을 구하시오. (단, [[a]]는 상수이고, [[p]], [[q]]는 유리수이다.)",
    figure=None,
    confidence=0.8,
    note="출처 [2025년 3월 고3 기하 30번 변형]. ∠F′FP를 angle(F'FP)로. 답 미도출(초안대로): PF=15/4, Q(3√3,0), PQ=9/4이면 a≈1>0이 되어 조건 a<0과 어긋남 — 변형 정합성 의심")

# 14. 7c3bce99 — 이차곡선 p38: FF′=PF′ 윗줄 → seg(FF')=seg(PF')
add(id="7c3bce99", qtype="short",
    question="좌표평면에서 초점이 [[A(a, 0)]] ([[a > 0]])이고 꼭짓점이 원점인 포물선과 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > a]])인 타원의 교점 중 제1사분면 위의 점을 P라 하자.\n[[seg(AF) = 4]], [[seg(PA) = seg(PF)]], [[seg(FF') = seg(PF')]]일 때, 타원의 장축의 길이는 [[p + q sqrt(7)]]이다. [[p + q]]의 값을 구하시오.\n(단, [[p]], [[q]]는 유리수이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 꼭짓점 원점·초점 A인 포물선과 초점 F′·F인 타원, 제1사분면 교점 P, PA=PF 표시(등호 표시), 선분 PF′ 그림"}}],
    confidence=0.9,
    note="출처 [2017년 9월 고3 이과 27번 변형]. FF′=PF′ 윗줄을 seg(FF')=seg(PF')로. 답 14 유지(빠른정답 12와 불일치는 1차와 동일)")

# 15. 5879febc — 이차곡선 p39: |PF−PF′|=10 → abs(seg(PF)-seg(PF')), AF′:FF′=1:6 → ratio
add(id="5879febc", qtype="choice",
    question="그림과 같이 두 점 [[F(k, 0)]], F′[[point(-k, 0)]]을 초점으로 하는 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]]과 점 F를 초점으로 하는 포물선 [[pow(y,2) = 56(x + c)]]가 있다.\n쌍곡선 위의 임의의 점 P에 대하여 [[abs(seg(PF) - seg(PF')) = 10]]이 성립하고, 포물선의 꼭짓점 A에 대하여 [[ratio(seg(AF'), seg(FF')) = ratio(1, 6)]]이 성립한다.\n이때, [[frac(pow(c,2), pow(a,2) - pow(b,2))]]의 값은? (단, [[0 < k < c]]이다.)",
    choices=["[[frac(53, 14)]]", "[[frac(55, 14)]]", "[[frac(30, 7)]]", "[[frac(32, 7)]]", "[[frac(34, 7)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/a²−y²/b²=1(초점 F′·F), 포물선 y²=56(x+c)(꼭짓점 A, 초점 F), 쌍곡선 위의 점 P 그림"}}],
    confidence=0.9,
    note="출처 [2009년 10월 고3 이과 8번]. |PF−PF′|를 abs(seg(PF)−seg(PF'))로, 비 AF′:FF′=1:6을 ratio로. 답 ④ 유지(빠른정답 30과 불일치는 1차와 동일)")

# 16. 7e2a876f — 이차곡선 p47 (원문항: AF=2, p²+q²)
add(id="7e2a876f", qtype="short",
    question="좌표평면에서 초점이 [[A(a, 0)]] ([[a > 0]])이고 꼭짓점이 원점인 포물선과 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > a]])인 타원의 교점 중 제1사분면 위의 점을 P라 하자.\n[[seg(AF) = 2]], [[seg(PA) = seg(PF)]], [[seg(FF') = seg(PF')]]일 때, 타원의 장축의 길이는 [[p + q sqrt(7)]]이다. [[pow(p,2) + pow(q,2)]]의 값을 구하시오.\n(단, [[p]], [[q]]는 유리수이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 꼭짓점 원점·초점 A인 포물선과 초점 F′·F인 타원, 제1사분면 교점 P, PA=PF 표시(등호 표시), 선분 PF′ 그림"}}],
    confidence=0.9,
    note="출처 [2017년 9월 고3 이과 27번/4점]. FF′=PF′ 윗줄을 seg(FF')=seg(PF')로. 답 29 유지")

# 17. 8cffa12f — 이차곡선 p49: PF×PF′ → seg(PF) × seg(PF')
add(id="8cffa12f", qtype="short",
    question="좌표평면에서 두 점 [[A(5, 0)]], [[B(-5, 0)]]에 대하여 장축이 선분 AB인 타원의 두 초점을 F, F′이라 하자. 초점이 F이고 꼭짓점이 원점인 포물선이 타원과 만나는 두 점을 각각 P, Q라 하자, [[seg(PQ) = 2 sqrt(10)]]일 때, 두 선분 PF와 PF′의 길이의 곱 [[seg(PF) × seg(PF')]]의 값은 [[frac(q, p)]]이다. [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 장축 양 끝 A·B인 타원, 초점 F′·F, 꼭짓점 원점·초점 F인 포물선, 교점 P(위)·Q(아래), 선분 PF·PF′·PQ 그림"}}],
    confidence=0.9,
    note="출처 [2010년 9월 고3 이과 20번]. PF×PF′을 seg(PF) × seg(PF')로. 답 103 유지(빠른정답 4와 불일치는 1차와 동일)")

# 18. d2c2f033 — 이차곡선 p50 (변형: pq)
add(id="d2c2f033", qtype="short",
    question="좌표평면에서 초점이 [[A(a, 0)]] ([[a > 0]])이고 꼭짓점이 원점인 포물선과 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > a]])인 타원의 교점 중 제1사분면 위의 점을 P라 하자.\n[[seg(AF) = 4]], [[seg(PA) = seg(PF)]], [[seg(FF') = seg(PF')]]일 때, 타원의 장축의 길이는 [[p + q sqrt(7)]]이다. [[p q]]의 값을 구하시오.\n(단, [[p]], [[q]]는 유리수이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 꼭짓점 원점·초점 A인 포물선과 초점 F′·F인 타원, 제1사분면 교점 P, PA=PF 표시(등호 표시), 선분 PF′ 그림"}}],
    confidence=0.9,
    note="출처 [2017년 9월 고3 이과 27번 변형]. FF′=PF′ 윗줄을 seg(FF')=seg(PF')로. 답 40 유지(빠른정답 29와 불일치는 1차와 동일)")

# 19. e3868b59 — 이차곡선 p51: PF′−PF → seg(PF') - seg(PF)
add(id="e3868b59", qtype="short",
    question="다음 그림과 같이 두 점 [[A(6, 0)]]과 [[B(-6, 0)]]에 대하여 장축이 선분 AB인 타원의 두 초점을 F와 F′이라 하고, 초점이 F이고 꼭짓점이 원점인 포물선이 타원과 만나는 두 점을 각각 P와 Q라 하자. [[seg(PQ) = 4 sqrt(6)]]일 때,\n[[seg(PF') - seg(PF)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 장축 양 끝 A·B인 타원, 초점 F′·F, 꼭짓점 원점·초점 F인 포물선, 교점 P(위)·Q(아래), 선분 PF·PF′·PQ 그림"}}],
    confidence=0.9,
    note="PF′−PF를 seg(PF')−seg(PF)로. 답 2 유지")

# 20. a98181f2 — 이차곡선 p52: sin(∠AFF′) → sin((angle(AFF'))), 단서의 ∠AFF′ → angle(AFF')
add(id="a98181f2", qtype="choice",
    question="다음 그림과 같이 [[F(p, 0)]]을 초점으로 하는 포물선 [[pow(y,2) = 4 p x]]와 [[F(p, 0)]]과 F′[[point(-p, 0)]]을 초점으로 하는 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]] ([[a > 0]], [[b > 0]])이 제1사분면에서 만나는 점을 A라 하자.\n[[seg(AF) = 5]], [[sin((angle(AFF'))) = frac(2 sqrt(6), 5)]]일 때, [[a b]]의 값은?\n(단, [[angle(AFF')]]은 예각이다.)",
    choices=["[[1]]", "[[sqrt(2)]]", "[[sqrt(5)]]", "[[2 sqrt(2)]]", "[[sqrt(11)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y²=4px와 쌍곡선 x²/a²−y²/b²=1(초점 F′·F), 제1사분면 교점 A, 선분 AF(길이 5) 점선 그림"}}],
    confidence=0.9,
    note="∠AFF′를 angle(AFF')로. 답 ④ 유지")

# 21. 47fc504e — 벡터의 덧셈과 뺄셈 p2: |PF→+PF′→| → abs(vec(PF) + vec(PF'))
add(id="47fc504e", qtype="choice",
    question="타원 [[frac(pow(x,2), 25) + frac(pow(y,2), 16) = 1]] 위의 점 P와 두 초점 F, F′에 대하여 [[abs(vec(PF) + vec(PF'))]]의 최댓값은?",
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    figure=None,
    confidence=0.9,
    note="출처 [2017년 10월 고3 이과 10번 변형]. 벡터 PF′→을 vec(PF')로. 답 ⑤ 유지")

# 22. afeb49d5 — 벡터의 덧셈과 뺄셈 p44
add(id="afeb49d5", qtype="choice",
    question="타원 [[frac(pow(x,2), 9) + frac(pow(y,2), 5) = 1]] 위의 점 P와 두 초점 F, F′에 대하여 [[abs(vec(PF) + vec(PF'))]]의 최댓값은?",
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    figure=None,
    confidence=0.9,
    note="출처 [2017년 10월 고3 이과 10번/3점]. 벡터 PF′→을 vec(PF')로. 답 ② 유지(빠른정답 3과 불일치는 1차와 동일)")

# 23. be6fc533 — 타원 p28: ∠FPF′=π/2 → angle(FPF')
add(id="be6fc533", qtype="choice",
    question="다음 그림과 같이 좌표평면에 [[x]]축 위의 두 점 F, F′과 점 [[P(0, n)]] ([[n > 0]])이 있다. 삼각형 PF′F가 [[angle(FPF') = frac(pi, 2)]]인 직각이등변삼각형이고, 두 점 F, F′을 초점으로 하고 점 P를 지나는 타원과 직선 PF′이 만나는 점 중 점 P가 아닌 점을 Q라 하자. 삼각형 FPQ의 둘레의 길이가 12일 때, 삼각형 FPQ의 넓이는?",
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 초점 F′·F인 타원, y축 위의 점 P(직각 표시), 직선 PF′과 타원의 교점 Q(제3사분면), 삼각형 FPQ 음영 그림"}}],
    confidence=0.9,
    note="출처 [2015년 10월 고3 이과 14번 변형]. ∠FPF′를 angle(FPF')로. 답 ③ 유지(빠른정답 5와 불일치는 1차와 동일)")

# 24. 9aaca6f4 — 타원 p29: FQ:F′Q=1:4 → ratio(seg(FQ), seg(F'Q)) = ratio(1, 4)
add(id="9aaca6f4", qtype="choice",
    question="그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]]을 초점으로 하는 타원이 있다. 타원 위의 점 중 제1사분면에 있는 점 P에 대하여 직선 PF가 타원과 만나는 점 중 점 P가 아닌 점을 Q라 하자. [[seg(OQ) = seg(OF)]], [[ratio(seg(FQ), seg(F'Q)) = ratio(1, 4)]]이고 삼각형 PF′Q의 내접원의 반지름의 길이가 2일 때, 양수 [[c]]의 값은? (단, O는 원점이다.)",
    choices=["[[frac(17, 3)]]", "[[frac(7 sqrt(17), 5)]]", "[[frac(3 sqrt(17), 2)]]", "[[frac(51, 8)]]", "[[frac(8 sqrt(17), 5)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 초점 F′·F인 타원, 제1사분면 점 P, 직선 PF와 타원의 교점 Q(제4사분면), 삼각형 PF′Q와 그 내접원 그림"}}],
    confidence=0.9,
    note="출처 [2022년 4월 고3 기하 28번/4점]. 비 FQ:F′Q=1:4를 ratio(seg(FQ), seg(F'Q))로. 답 ③ 유지(빠른정답 2와 불일치는 1차와 동일)")

# 25. 5459d9e3 — 타원 p38: BF′−BA=(1/3)AF′ → seg(BF') - seg(BA) = frac(1,3) seg(AF')
add(id="5459d9e3", qtype="short",
    question="다음 그림과 같이 두 초점이\n[[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 타원 [[sub(E,1)]]이 있다.\n타원 [[sub(E,1)]]의 꼭짓점 중 [[x]]좌표가 양수인 점을 A라 하고, 두 점 A, F를 초점으로 하고 점 F′을 지나는 타원을 [[sub(E,2)]]라 하자. 두 타원 [[sub(E,1)]], [[sub(E,2)]]의 교점 중 [[y]]좌표가 양수인 점 B에 대하여 [[seg(BF') - seg(BA) = frac(1, 3) seg(AF')]]이 성립한다. 타원 [[sub(E,2)]]의 단축의 길이가 [[4 sqrt(7)]]일 때, [[9 pow(c, 2)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 큰 타원 E₁(초점 F′·F, 오른쪽 꼭짓점 A)과 타원 E₂(초점 A·F, F′ 통과), 교점 B(위), 선분 BF′·BA 그림"}}],
    confidence=0.9,
    note="출처 [2024년 5월 고3 기하 30번 변형]. BF′−BA=(1/3)AF′ 윗줄을 seg로. 답 21 유지(빠른정답 5와 불일치는 1차와 동일)")

# 26. 74919f53 — 타원 p39 (원문항: 둘레 12√2; 원문에 점 이름 P 없이 '점 (0, n)'으로 인쇄됨 — 그대로)
add(id="74919f53", qtype="choice",
    question="그림과 같이 좌표평면에 [[x]]축 위의 두 점 F, F′과 점 [[point(0, n)]] ([[n > 0]])이 있다. 삼각형 PF′F가 [[angle(FPF') = frac(pi, 2)]]인 직각이등변삼각형일 때, 두 점 F, F′을 초점으로 하고 점 P를 지나는 타원과 직선 PF′이 만나는 점 중 점 P가 아닌 점을 Q라 하자. 삼각형 FPQ의 둘레의 길이가 [[12 sqrt(2)]]일 때, 삼각형 FPQ의 넓이는?",
    choices=["[[11]]", "[[12]]", "[[13]]", "[[14]]", "[[15]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: x축 위의 두 점 F′·F와 y축 위의 점 P(직각 표시)로 이루어진 직각이등변삼각형 PF′F 그림"}}],
    confidence=0.9,
    note="출처 [2015년 10월 고3 이과 14번/4점]. ∠FPF′를 angle(FPF')로; 원문의 '점 (0, n)'(P 표기 누락)은 그대로. 답 ② 유지(빠른정답 4와 불일치는 1차와 동일)")

# 27. 6c3e46c0 — 타원 p40: AF′=13 윗줄 → seg(AF')
add(id="6c3e46c0", qtype="choice",
    question="타원 [[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), 13) = 1]]의 두 초점을 F, F′이라 하자.\n점 F를 지나고 [[x]]축에 수직인 직선 위의 점 A가 [[seg(AF') = 13]], [[seg(AF) = 5]]를 만족시킨다. 선분 AF′과 타원이 만나는 점을 P라 할 때, 삼각형 PF′F의 둘레의 길이는?\n(단, [[a]]는 [[a > sqrt(13)]]인 상수이다.)",
    choices=["[[20]]", "[[22]]", "[[24]]", "[[26]]", "[[28]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 초점 F′·F인 타원, F를 지나는 수직선 위의 점 A, 선분 AF′과 타원의 교점 P, 선분 PF, F에서 직각 표시 그림"}}],
    confidence=0.9,
    note="출처 [2022년 9월 고3 기하 25번 변형]. AF′=13 윗줄을 seg(AF')로. 답 ④ 유지(빠른정답 2와 불일치는 1차와 동일)")

# 28. 8b9bc61f — 타원 p42: GP+PF′=2√5, QG+QG′ → seg(PF'), seg(QG')
add(id="8b9bc61f", qtype="choice",
    question="다음 그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원 [[sub(C,1)]]: [[frac(pow(x,2), pow(a,2)) + pow(y,2) = 1]]과 두 점 [[G(0, d)]], G′[[point(0, -d)]] ([[d > 1]])을 초점으로 하고 타원 [[sub(C,1)]]의 두 꼭짓점을 지나는 타원 [[sub(C,2)]]가 있다. 직선 FG가 타원 [[sub(C,1)]]과 제1사분면에서 만나는 점을 P라 하고, 직선 F′P가 타원 [[sub(C,2)]]와 제1사분면에서 만나는 점을 Q라 하자.\n[[seg(GP) = seg(PF)]]이고 [[seg(GP) + seg(PF') = 2 sqrt(5)]]일 때, [[seg(QG) + seg(QG')]]의 값은? (단, [[a]]는 양수이다.)",
    choices=["[[frac(sqrt(205), 5)]]", "[[frac(2 sqrt(205), 5)]]", "[[frac(3 sqrt(205), 5)]]", "[[frac(4 sqrt(205), 5)]]", "[[sqrt(205)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 가로로 긴 타원 C₁(초점 F′·F)과 세로로 긴 타원 C₂(초점 G·G′), 점 P(C₁ 위)·Q(C₂ 위), 선분 GP·GQ·F′Q·FQ 그림"}}],
    confidence=0.9,
    note="출처 [2025년 6월 고3 기하 28번 변형]. PF′·QG′ 윗줄을 seg(PF')·seg(QG')로. 답 ② 유지")

# 29. 2be5d1d4 — 타원 p62: cos(∠FF′A) → cos((angle(FF'A))), F′Q−AQ → seg(F'Q) - seg(AQ)
add(id="2be5d1d4", qtype="choice",
    question="두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])이고 장축의 길이가 32인 타원을 [[sub(C,1)]]이라 하자. 점 F를 지나고 [[x]]축에 수직인 직선이 타원 [[sub(C,1)]]과 제1사분면에서 만나는 점을 A라 하고, 두 초점이 F, A이고 점 [[P(16, 0)]]을 지나는 타원을 [[sub(C,2)]]라 하자. 두 타원 [[sub(C,1)]]과 [[sub(C,2)]]가 만나는 점 중 점 P가 아닌 점을 Q라 하자. [[cos((angle(FF'A))) = frac(24, 25)]]일 때,\n[[seg(F'Q) - seg(AQ)]]의 값은?",
    choices=["[[28 - sqrt(65)]]", "[[37 - 2 sqrt(65)]]", "[[30 - sqrt(65)]]", "[[39 - 2 sqrt(65)]]", "[[32 - sqrt(65)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 큰 타원 C₁(초점 F′·F, 오른쪽 꼭짓점 P(16,0))과 작은 타원 C₂(초점 F·A), F를 지나는 수직선 위의 점 A, 교점 Q, 직각 표시 그림"}}],
    confidence=0.9,
    note="출처 [2024년 3월 고3 기하 28번 변형]. ∠FF′A를 angle(FF'A)로, F′Q−AQ 윗줄을 seg로. 답 ① 유지(빠른정답 18과 불일치는 1차와 동일)")

# 30. c78e6374 — 타원 p63: F′R−PR=6 → seg(F'R) - seg(PR) = 6
add(id="c78e6374", qtype="short",
    question="두 점 [[F(0, 4)]], F′[[point(0, -4)]]를 초점으로 하는 타원 [[sub(C,1)]]에 대하여 점 F를 지나고 [[x]]축과 평행한 직선이 타원 [[sub(C,1)]]과 만나는 점 중 제1사분면 위에 있는 점을 P, 선분 PF′과 [[x]]축이 만나는 점을 Q라 하자. 두 점 P, F를 초점으로 하고 점 Q가 꼭짓점인 타원 [[sub(C,2)]]에 대하여\n두 타원 [[sub(C,1)]], [[sub(C,2)]]가 만나는 점 중 [[x]]축에 가까운 점을 R이라 하자.\n[[seg(F'R) - seg(PR) = 6]]일 때, 두 타원 [[sub(C,1)]], [[sub(C,2)]]의 장축의 길이의 합을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 세로로 긴 타원 C₁(초점 F·F′ y축 위)과 타원 C₂(초점 P·F), 점 P(F와 같은 높이), 선분 PF′과 x축의 교점 Q, 교점 R(x축 근처) 그림"}}],
    confidence=0.9,
    note="출처 [2025년 9월 고3 기하 29번 변형]. F′R−PR 윗줄을 seg(F'R)−seg(PR)로. 답 26 유지(빠른정답 160과 불일치는 1차와 동일)")

# 31. e064c42b — 타원 p70 (원문항: F(0,6), 7√2, 곱)
add(id="e064c42b", qtype="short",
    question="두 점 [[F(0, 6)]], F′[[point(0, -6)]]를 초점으로 하는 타원 [[sub(C,1)]]에 대하여 점 F를 지나고 [[x]]축과 평행한 직선이 타원 [[sub(C,1)]]과 만나는 점 중 제1사분면 위에 있는 점을 P, 선분 PF′과 [[x]]축이 만나는 점을 Q라 하자. 두 점 P, F를 초점으로 하고 점 Q가 꼭짓점인 타원 [[sub(C,2)]]에 대하여 두 타원 [[sub(C,1)]], [[sub(C,2)]]가 만나는 점 중 [[x]]축에 가까운 점을 R이라 하자.\n[[seg(F'R) - seg(PR) = 7 sqrt(2)]]일 때, 두 타원 [[sub(C,1)]], [[sub(C,2)]]의 장축의 길이의 곱을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 세로로 긴 타원 C₁(초점 F·F′ y축 위)과 타원 C₂(초점 P·F), 점 P(F와 같은 높이), 선분 PF′과 x축의 교점 Q, 교점 R(x축 근처) 그림"}}],
    confidence=0.9,
    note="출처 [2025년 9월 고3 기하 29번/4점]. F′R−PR 윗줄을 seg(F'R)−seg(PR)로. 답 396 유지(빠른정답 23과 불일치는 1차와 동일)")

# 32. f8baf748 — 타원 p74: PF+PF′=6 → seg(PF) + seg(PF') = 6
add(id="f8baf748", qtype="choice",
    question="두 점 [[F(1, 0)]], F′[[point(-1, 0)]]에 대하여 점 P가 [[seg(PF) + seg(PF') = 6]]을 만족시킬 때, 점 P가 나타내는 도형의 방정식은?",
    choices=["[[frac(pow(x,2), 9) + frac(pow(y,2), 8) = 1]]", "[[frac(pow(x,2), 9) + frac(pow(y,2), 6) = 1]]", "[[frac(pow(x,2), 9) + frac(pow(y,2), 4) = 1]]", "[[frac(pow(x,2), 8) + frac(pow(y,2), 9) = 1]]", "[[frac(pow(x,2), 6) + frac(pow(y,2), 9) = 1]]"],
    figure=None,
    confidence=0.9,
    note="PF+PF′=6 윗줄을 seg(PF)+seg(PF')로. 답 ① 유지(빠른정답 63과 불일치는 1차와 동일)")

# 33. bd5b6eb0 — 쌍곡선의 접선의 방정식 p26: PF·PF′=8 → seg(PF) × seg(PF') = 8
add(id="bd5b6eb0", qtype="choice",
    question="양수 [[a]]에 대하여 두 초점이 F, F′인\n쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(a,2)) = -1]] 위의 점 [[point(a, sqrt(2) a)]]에서의 접선이 [[y]]축과 만나는 점을 P라 하자. [[seg(PF) × seg(PF') = 8]]일 때, [[a]]의 값은?",
    choices=["[[sqrt(3)]]", "[[frac(4 sqrt(3), 3)]]", "[[frac(5 sqrt(3), 3)]]", "[[2 sqrt(3)]]", "[[frac(7 sqrt(3), 3)]]"],
    figure=None,
    confidence=0.9,
    note="출처 [2025년 11월 고3 기하 26번/3점]. 길이의 곱 PF·PF′을 seg(PF) × seg(PF')로. 답 ② 유지(빠른정답 1과 불일치는 1차와 동일)")

# 34. 7c33dcb6 — 쌍곡선의 접선의 방정식 p77: PF′=FF′ → seg(PF') = seg(FF')
add(id="7c33dcb6", qtype="choice",
    question="두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인\n쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), k) = 1]] 위의 제1사분면에 있는 점 P에서의 접선이 [[x]]축과 만나는 점의 [[x]]좌표가 2이다. [[seg(PF') = seg(FF')]]일 때, 양수 [[k]]의 값은?",
    choices=["[[18]]", "[[21]]", "[[24]]", "[[27]]", "[[30]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/9−y²/k=1(초점 F′·F), 제1사분면 점 P, P에서의 접선(x축과 x=2에서 만남), 선분 PF′ 그림"}}],
    confidence=0.9,
    note="출처 [2022년 7월 고3 기하 26번 변형]. PF′=FF′ 윗줄을 seg(PF')=seg(FF')로. 답 ④ 유지(빠른정답 1과 불일치는 1차와 동일)")

# ================= esc_sonnet_h3-3_5of6 =================
# 35. a6681072 — 쌍곡선의 접선의 방정식 p84: 프라임 점 F′은 단독 점 이름(텍스트), '선분 PF′'은 윗줄 없음 → 문법 안, 그대로 통과
add(id="a6681072", qtype="short",
    question="다음 그림과 같이 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 48) = 1]] 위의 점 [[P(8, k)]] ([[k > 0]])에서의 접선이 [[x]]축과 만나는 점을 Q라 하자. 두 점 F, F′을 초점으로 하고 점 Q를 한 꼭짓점으로 하는 쌍곡선이 선분 PF′과 만나는 두 점을 R, S라 하자. [[seg(RS) + seg(SF) = seg(RF) + 8]]일 때, [[pow(a,2) + pow(k,2)]]의 값을 구하시오. (단, [[a]]는 양수이고, 점 R의 [[x]]좌표는 점 S의 [[x]]좌표보다 크다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/a²−y²/48=1(초점 F, F′), 두 초점을 공유하고 Q를 꼭짓점으로 하는 두 번째 쌍곡선, 점 P에서의 접선(x축과 Q에서 만남), 선분 PF′ 위의 점 R, S"}}],
    confidence=0.85,
    note="출처 [2023년 4월 고3 기하 29번 변형]. 단독 점 F′은 텍스트, 선분 PF′(윗줄 없음)도 텍스트 — 문법 안. 답 160 유지(빠른정답 2와 불일치는 1차와 동일)")

# 36. 4c2063db — 쌍곡선의 접선의 방정식 p86: F₁(4,0) → app(sub(F,1),4,0); PF₂−PF₁=6 윗줄 → seg(PF2)−seg(PF1)
add(id="4c2063db", qtype="short",
    question="두 점 [[app(sub(F,1), 4, 0)]], [[app(sub(F,2), -6, 0)]]에 대하여 포물선 [[pow(y,2) = 16x]] 위의 점 중 제1사분면에 있는 점 P가 [[seg(PF2) - seg(PF1) = 6]]을 만족시킨다. 포물선 [[pow(y,2) = 16x]] 위의 점 P에서의 접선이 [[x]]축과 만나는 점을 [[sub(F,3)]]이라 하면 두 점 [[sub(F,1)]], [[sub(F,3)]]을 초점으로 하는 타원의 한 꼭짓점은 선분 P[[sub(F,3)]] 위에 있다. 이 타원의 장축의 길이가 [[2a]]일 때, [[pow(a,2)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y²=16x, 제1사분면 위의 점 P와 P에서의 접선, 접선이 x축과 만나는 점 F₃(음의 x축), x축 위의 점 F₂(−6,0), F₁(4,0), 원점 O"}}],
    confidence=0.85,
    note="출처 [2022년 10월 고3 기하 29번/4점]. 좌표 붙은 첨자 점을 app(sub(F,1),4,0)로, PF₂−PF₁ 윗줄을 seg(PF2)−seg(PF1)로; '선분 PF₃'(윗줄 없음)는 텍스트. 답 54 유지(빠른정답 2와 불일치는 1차와 동일)")

# 37. 254b0db1 — 쌍곡선의 접선의 방정식 p92 (변형: F₁(6,0), F₂(−12,0), y²=24x, 12, (20/21)a²)
add(id="254b0db1", qtype="short",
    question="두 점 [[app(sub(F,1), 6, 0)]], [[app(sub(F,2), -12, 0)]]에 대하여 포물선 [[pow(y,2) = 24x]] 위의 점 중 제1사분면에 있는 점 P가 [[seg(PF2) - seg(PF1) = 12]]를 만족시킨다. 포물선 [[pow(y,2) = 24x]] 위의 점 P에서의 접선이 [[x]]축과 만나는 점을 [[sub(F,3)]]이라 하면 두 점 [[sub(F,1)]], [[sub(F,3)]]을 초점으로 하는 타원의 한 꼭짓점은 선분 P[[sub(F,3)]] 위에 있다. 이 타원의 장축의 길이가 [[2a]]일 때, [[frac(20,21) pow(a,2)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y²=24x, 제1사분면 위의 점 P와 P에서의 접선, 접선이 x축과 만나는 점 F₃(음의 x축), x축 위의 점 F₂(−12,0), F₁(6,0), 원점 O"}}],
    confidence=0.85,
    note="출처 [2022년 10월 고3 기하 29번 변형]. 좌표 붙은 첨자 점을 app(sub(F,1),6,0)로, PF₂−PF₁ 윗줄을 seg(PF2)−seg(PF1)로. 답 147 유지(빠른정답 80과 불일치는 1차와 동일)")

# 38. cac51041 — 타원의 접선의 방정식 p73: P₀(a,b) → app(sub(P,0),a,b); BF+FP₀+P₀A 윗줄 → seg(BF)+seg(FP0)+seg(P0A)
add(id="cac51041", qtype="choice",
    question="그림과 같이 두 초점이 [[F(1, 0)]], F′[[point(-1, 0)]]이고 단축의 길이가 [[2 sqrt(5)]]인 타원과 [[y]]축 위의 점 A가 있다. 점 A를 [[x]]축에 대하여 대칭이동한 점을 B라 하자. 제1사분면에서 이 타원 위를 움직이는 점 P에 대하여 네 선분 AB, BF, FP, PA로 둘러싸인 도형의 넓이가 최대가 되도록 하는 점 P를 [[app(sub(P,0), a, b)]]라 하자. [[seg(BF) + seg(FP0) + seg(P0A) = 2 sqrt(6)]]일 때, [[a b]]의 값은?\n(단, 점 A의 [[y]]좌표는 양수이고, [[seg(AB) < 2 sqrt(5)]]이다.)",
    choices=["[[frac(11 sqrt(2), 8)]]", "[[frac(3 sqrt(2), 2)]]", "[[frac(13 sqrt(2), 8)]]", "[[frac(7 sqrt(2), 4)]]", "[[frac(15 sqrt(2), 8)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 초점 F(1,0), F′(−1,0)인 타원, y축 위의 점 A와 대칭점 B, 제1사분면 위의 점 P, 사각형 ABFP 음영"}}],
    confidence=0.85,
    note="출처 [2025년 5월 고3 기하 28번/4점]. P₀(a, b)를 app(sub(P,0), a, b)로, 첨자 선분 FP₀·P₀A 윗줄을 seg(FP0)·seg(P0A)로. 답 ⑤ 유지")

# 39. bb861f78 — 타원의 접선의 방정식 p81 (변형: F(0,1), 2√2, AF+FP₀+P₀B=2√3)
add(id="bb861f78", qtype="choice",
    question="다음 그림과 같이 두 초점이 [[F(0, 1)]], F′[[point(0, -1)]]이고 단축의 길이가 [[2 sqrt(2)]]인 타원과 [[x]]축 위의 점 A가 있다. 점 A를 [[y]]축에 대하여 대칭이동한 점을 B라 하자. 제1사분면에서 이 타원 위를 움직이는 점 P에 대하여 네 선분 AB, BP, PF, FA로 둘러싸인 도형의 넓이가 최대가 되도록 하는 점 P를 [[app(sub(P,0), a, b)]]라 하자.\n[[seg(AF) + seg(FP0) + seg(P0B) = 2 sqrt(3)]]일 때, [[a b]]의 값은?\n(단, 점 A의 [[x]]좌표는 음수이고, [[seg(AB) < 2 sqrt(2)]]이다.)",
    choices=["[[frac(3 sqrt(3), 4)]]", "[[frac(2 sqrt(3), 3)]]", "[[frac(7 sqrt(3), 12)]]", "[[frac(sqrt(3), 2)]]", "[[frac(5 sqrt(3), 12)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 초점 F(0,1), F′(0,−1)인 세로로 긴 타원, x축 위의 점 A(음의 x축)와 대칭점 B, 제1사분면 위의 점 P, 사각형 ABPF 음영"}}],
    confidence=0.85,
    note="출처 [2025년 5월 고3 기하 28번 변형]. P₀(a, b)를 app(sub(P,0), a, b)로, FP₀·P₀B 윗줄을 seg(FP0)·seg(P0B)로. 답 ② 유지")

# 40. b1c5add2 — 타원의 접선의 방정식 p85: PF+PF′=AB → seg(PF) + seg(PF') = seg(AB)
add(id="b1c5add2", qtype="choice",
    question="두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원 [[frac(pow(x,2), 108) + frac(pow(y,2), 4 pow(b,2)) = 1]] 위에 있는 제1사분면 위의 점 [[P(9, b)]]에서의 접선이 [[x]]축, [[y]]축과 만나는 점을 각각 A, B라 하자. [[seg(PF) + seg(PF') = seg(AB)]]일 때, [[pow(b,2) c]]의 값은?",
    choices=["[[92]]", "[[96]]", "[[100]]", "[[104]]", "[[108]]"],
    figure=None,
    confidence=0.9,
    note="출처 [2026년 7월 고3 기하 26번 변형]. PF′ 윗줄을 seg(PF')로. 답 ⑤ 유지(빠른정답 1과 불일치는 1차와 동일)")

# 41. 3517ae96 — 타원의 접선의 방정식 p88: RS+RF′ → seg(RS) + seg(RF')
add(id="3517ae96", qtype="choice",
    question="다음 그림과 같이 두 점 [[F(0, c)]], F′[[point(0, -c)]] ([[c > 0]])을 초점으로 하는 타원 [[frac(pow(x,2), 12) + frac(pow(y,2), 16) = 1]] 위의 점 [[P(-3, 2)]]에서 타원에 접하는 직선을 [[l]]이라 하자. 점 F를 지나고 [[l]]과 평행한 직선이 타원과 만나는 점 중 제3사분면 위에 있는 점을 Q라 하자. 두 직선 F′Q와 [[l]]이 만나는 점을 R, [[l]]과 [[y]]축이 만나는 점을 S라 할 때, [[seg(RS) + seg(RF')]]의 값은?",
    choices=["[[24]]", "[[23]]", "[[22]]", "[[21]]", "[[20]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 타원 x²/12+y²/16=1, 초점 F(0,c)·F′(0,−c), 점 P(−3,2)에서의 접선 l(y축과 S에서 만남), F를 지나 l에 평행한 직선과 제3사분면 교점 Q, 직선 F′Q와 l의 교점 R"}}],
    confidence=0.85,
    note="출처 [2021년 9월 고3 기하 28번 변형]. RF′ 윗줄을 seg(RF')로; '직선 F′Q'(윗줄 없음)는 텍스트. 답 ⑤ 유지(빠른정답 4와 불일치는 1차와 동일)")

# 42. 88a78d72 — 타원의 접선의 방정식 p96 (원문항: 48, P(6,b))
add(id="88a78d72", qtype="choice",
    question="두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원 [[frac(pow(x,2), 48) + frac(pow(y,2), 4 pow(b,2)) = 1]] 위에 있는 제1사분면 위의 점 [[P(6, b)]]에서의 접선이 [[x]]축, [[y]]축과 만나는 점을 각각 A, B라 하자. [[seg(PF) + seg(PF') = seg(AB)]]일 때, [[pow(b,2) c]]의 값은?",
    choices=["[[20]]", "[[24]]", "[[28]]", "[[32]]", "[[36]]"],
    figure=None,
    confidence=0.9,
    note="출처 [2026년 7월 고3 기하 26번/3점]. PF′ 윗줄을 seg(PF')로. 답 ④ 유지(빠른정답 5와 불일치는 1차와 동일)")

# ================= esc_sonnet_h3-3_6of6 =================
# 43·44. 5fbc421d, b6d1079e — 벡터의 내적 p19 (같은 이미지 id 2개): OP′→ → vec(OP'), 내적 → dot
_Q19 = "좌표평면 위에 원점 O를 시점으로 하는 서로 다른 임의의 두 벡터 [[vec(OP)]], [[vec(OQ)]]가 있다. 두 벡터의 종점 P, Q를 [[x]]축의 방향으로 4만큼, [[y]]축의 방향으로 3만큼 평행이동시킨 점을 각각 P′, Q′이라 할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[abs(vec(OP) - vec(OP')) = 5]]\nㄴ. [[abs(vec(OP) - vec(OQ)) = abs(vec(OP') - vec(OQ'))]]\nㄷ. [[dot(vec(OP), vec(OQ)) = dot(vec(OP'), vec(OQ'))]]"
for _i in ("5fbc421d", "b6d1079e"):
    add(id=_i, qtype="choice", question=_Q19,
        choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
        figure=None, confidence=0.9,
        note="프라임 벡터 OP′→·OQ′→을 vec(OP')·vec(OQ')로, 내적을 dot로. 같은 이미지 id 2개. 답 ③ 유지(빠른정답 0과 불일치는 1차와 동일)")

# 45. 78750a42 — 벡터의 내적 p22 (원문항: (3, 1), √10)
add(id="78750a42", qtype="choice",
    question="좌표평면 위에 원점 O를 시점으로 하는 서로 다른 임의의 두 벡터 [[vec(OP)]], [[vec(OQ)]]가 있다. 두 벡터의 종점 P, Q를 [[x]]축 방향으로 3만큼, [[y]]축 방향으로 1만큼 평행이동시킨 점을 각각 P′, Q′이라 할 때, <보기>에서 항상 옳은 것을 모두 고른 것은?\n<보기>\nㄱ. [[abs(vec(OP) - vec(OP')) = sqrt(10)]]\nㄴ. [[abs(vec(OP) - vec(OQ)) = abs(vec(OP') - vec(OQ'))]]\nㄷ. [[dot(vec(OP), vec(OQ)) = dot(vec(OP'), vec(OQ'))]]",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.9,
    note="출처 [2005년 11월 고3 이과 4번]. 프라임 벡터 OP′→·OQ′→을 vec(OP')·vec(OQ')로. 답 ③ 유지")

# 46. 6462357d — 벡터의 내적 p74: OA₁→ 등 고정 첨자 → vec(OA1); 가변 첨자 OAₖ→는 sub(vec(OA), k) 유지
add(id="6462357d", qtype="choice",
    question="좌표평면에서 원점 O가 중심이고 반지름의 길이가 1인 원 위의 세 점 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]]에 대하여\n[[abs(vec(OX)) <= 1]]이고, [[dot(vec(OX), sub(vec(OA), k)) >= 0]] ([[k]] = 1, 2, 3)\n을 만족시키는 모든 점 X의 집합이 나타내는 도형을 [[D]]라 하자. <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[vec(OA1) = vec(OA2) = vec(OA3)]]이면 [[D]]의 넓이는 [[frac(pi,2)]]이다.\nㄴ. [[vec(OA2) = -vec(OA1)]]이고, [[vec(OA3) = vec(OA1)]]이면 [[D]]의 길이는 2인 선분이다.\nㄷ. [[dot(vec(OA1), vec(OA2)) = 0]]인 경우에, [[D]]의 넓이가 [[frac(pi,4)]]이면 점 [[sub(A,3)]]은 [[D]]에 포함되어 있다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="출처 [2017년 9월 고3 이과 19번/4점]. 고정 첨자 벡터 OA₁→~OA₃→을 vec(OA1)~vec(OA3)로; 가변 첨자 OAₖ→는 sub(vec(OA), k) 우회 유지. 답 ⑤ 유지(빠른정답 1과 불일치는 1차와 동일)")

# 47~50. 3803b558, bd2a6a3f, c95eea8f, 0a59e7d6 — 벡터의 내적 p76 (같은 이미지 id 4개)
_Q76 = "좌표평면에서 원점 O가 중심이고 반지름의 길이가 1인 원 위의 세 점 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]]에 대하여 [[abs(vec(OX)) <= 1]]이고 [[dot(vec(OX), sub(vec(OA), k)) >= 0]] ([[k]] = 1, 2, 3)을 만족시키는 모든 점 X의 집합이 나타내는 도형을 [[D]]라 하자. 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[vec(OA1) = vec(OA2) = vec(OA3)]]이면 [[D]]의 넓이는 [[frac(pi,2)]]이다.\nㄴ. [[vec(OA2) = -vec(OA1)]]일 때, [[D]]가 길이가 2인 선분이기 위해서는 [[vec(OA3) = vec(OA1)]] 또는 [[vec(OA3) = vec(OA2)]]이어야 한다.\nㄷ. [[dot(vec(OA1), vec(OA2)) = 0]], [[vec(OA3) = -vec(OA1)]]이면 [[D]]는 길이가 [[frac(3,2)]]인 선분이다."
for _i in ("3803b558", "bd2a6a3f", "c95eea8f", "0a59e7d6"):
    add(id=_i, qtype="choice", question=_Q76,
        choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
        figure=None, confidence=0.85,
        note="고정 첨자 벡터 OA₁→~OA₃→을 vec(OA1)~vec(OA3)로; 가변 첨자 OAₖ→는 sub(vec(OA), k) 우회 유지. 같은 이미지 id 4개. 답 ③ 유지(ㄱ·ㄴ 참, ㄷ은 길이 1인 선분 — 빠른정답 27과 불일치는 1차와 동일)")

# 51. 328d10cd — 벡터의 내적 p78: 선분 A₁A₂ 윗줄 → seg(A1A2)
add(id="328d10cd", qtype="choice",
    question="좌표평면에서 원점 O가 중심이고 반지름의 길이가 1인 원 위의 세 점 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]]에 대하여 [[abs(vec(OX)) <= 1]]이고, [[dot(vec(OX), sub(vec(OA), k)) >= 0]] ([[k]] = 1, 2, 3)을 만족시키는 모든 점 X의 집합이 나타내는 도형을 [[D]]라 하자. 다음 보기 중에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[vec(OA1) = vec(OA2) = vec(OA3)]]이면 [[D]]의 넓이는 [[frac(pi,4)]]이다.\nㄴ. [[seg(A1A2)]]가 원의 지름일 때, [[vec(OA3) = vec(OA1)]]이면 [[D]]는 길이가 2인 선분이다.\nㄷ. [[dot(vec(OA1), vec(OA2)) = 0]]인 경우에 ([[D]]의 넓이) = [[frac(pi,4)]]를 만족하는 점 [[sub(A,3)]]의 자취의 길이는 [[frac(pi,2)]]이다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="출처 [2017년 9월 고3 이과 19번 변형]. 고정 첨자 벡터를 vec(OA1)~vec(OA3)로, 선분 A₁A₂ 윗줄을 seg(A1A2)로; 가변 첨자 OAₖ→는 sub(vec(OA), k) 우회 유지. 답 ④ 유지(빠른정답 3과 불일치는 1차와 동일)")

# 52. e1c7b39f — 벡터의 내적 p99: O₁P→·O₂Q→ → dot(vec(O1P), vec(O2Q)) — 그러나 같은 이미지에 별개 문항 2개(id 1개) → 보류 유지
add(id="e1c7b39f", qtype="choice",
    question="평면 위의 두 점 [[sub(O,1)]], [[sub(O,2)]] 사이의 거리가 2일 때 [[sub(O,1)]], [[sub(O,2)]]를 각각 중심으로 하고 반지름의 길이가 2인 두 원의 교점을 A, B라 하자. 호 A[[sub(O,2)]]B 위의 점 P와 호 A[[sub(O,1)]]B 위의 점 Q에 대하여 두 벡터 [[vec(O1P)]], [[vec(O2Q)]]의 내적 [[dot(vec(O1P), vec(O2Q))]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, [[M + m]]의 값은?",
    choices=["[[-4]]", "[[-2]]", "[[0]]", "[[2]]", "[[4]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "중심 O₁(좌), O₂(우)인 반지름 2의 두 원이 위아래 교점 A(위), B(아래)에서 만남; O₁에서 원 O₁의 오른쪽 호 위의 점 P로, O₂에서 원 O₂의 왼쪽 호 위의 점 Q로 향하는 화살표"}}],
    confidence=0.8,
    needs_review="같은 이미지에 별개 문항 2개(id 1개): 상단 두 원·내적 문항을 전사함 / 하단 — 한 변의 길이가 6인 정삼각형 ABC의 꼭짓점 A에서 변 BC에 내린 수선의 발 H, 점 P가 선분 AH 위를 움직일 때 |PA⃗·PB⃗|의 최댓값 q/p, p+q(서로소 자연수)를 구하는 단답형(답 31) — id 없음",
    note="첨자 벡터 O₁P→·O₂Q→을 vec(O1P)·vec(O2Q)·dot로 고침(문법 안). 답 ② 유지(빠른정답 7은 두 문항 어느 쪽과도 불일치)")

# ================= esc_sonnet_m1-1_1of3 =================
# 53. ff3cd74a — 유리수의 덧셈과 뺄셈 p14: 답이 원문자 ㉠ — 답 문법 밖 → 보류 유지 (본문은 문법 안)
add(id="ff3cd74a", qtype="short",
    question="다음 계산 과정 중 덧셈에 대한 교환법칙이 사용된 곳을 구하시오.\n[[(-1)]] + {(+3) + [[(-8)]]}\n= [[(-1)]] + {[[(-8)]] + (+3)}  ← ㉠\n= {[[(-1)]] + [[(-8)]]} + (+3)  ← ㉡\n= [[-(1 + 8)]] + (+3)  ← ㉢\n= [[(-9)]] + (+3)  ← ㉣\n= [[-6]]  ← ㉤",
    figure=None, confidence=0.8,
    needs_review="답 기호 ㉠이 답 문법(ㄱㄴㄷ·①~⑤·수식) 범위 밖이라 answer 미기재 — 교환법칙은 1행→2행(㉠)",
    note="양의 부호 (+3)은 텍스트 혼합(v1.5에도 단항 + 없음). 빠른정답 3과 대응 불명")

# 54. ff10cc81 — 절댓값 p75: 경우 나눔 → cases; 사용자 정의 이항연산 ⊗는 v1.5에도 없음 → 보류 유지
add(id="ff10cc81", qtype="short",
    question="절댓값이 서로 다른 두 수 [[a]], [[b]]에 대하여\n[[a]]⊗[[b]] = [[cases(abs(a), abs(a) < abs(b), abs(b), abs(a) > abs(b))]]라 할 때,\n[[(-frac(7,18))]]⊗{[[(-frac(11,2))]]⊗[[(-frac(9,5))]]}의 값을 구하시오.",
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ⊗ — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지",
    note="경우 나눔 정의는 cases로 고침. a⊗b=min(|a|,|b|): (−11/2)⊗(−9/5)=9/5, (−7/18)⊗(9/5)=7/18. 답 7/18 유지(빠른정답과 일치)")

# 55. 53614914 — 절댓값 p76: ◇ 사용자 정의 연산 → 보류 유지 (경우 나눔은 cases)
add(id="53614914", qtype="short",
    question="절댓값이 서로 다른 두 수 [[a]], [[b]]에 대하여\n[[a]]◇[[b]] = [[cases(abs(a), abs(a) > abs(b), abs(b), abs(a) < abs(b))]]라 할 때,\n{[[(-frac(8,5))]]◇[[(-frac(11,4))]]}◇[[(-frac(16,3))]]의 값을 구하시오.",
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ◇ — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지",
    note="경우 나눔 정의는 cases로 고침. a◇b=max(|a|,|b|): 11/4◇(−16/3)=16/3. 답 16/3 유지(빠른정답과 일치)")

# 56. d25f4656 — 정수와 유리수 p40: 약속 기호 ⟨x⟩ + 조건이 한글 문장인 경우 나눔 → cases 불가, 보류 유지
add(id="d25f4656", qtype="choice",
    question="수 [[x]]에 대하여\n⟨[[x]]⟩ = { 0 ([[x]]는 정수) ; 1 ([[x]]는 정수가 아닌 유리수) }로 약속할 때,\n다음 중 ⟨[[-frac(3,5)]]⟩ + ⟨[[0]]⟩ + ⟨[[2.6]]⟩ + ⟨[[x]]⟩ = 3을\n만족시키는 [[x]]가 될 수 없는 것은?",
    choices=["[[-frac(5,4)]]", "[[-0.1]]", "[[frac(6,2)]]", "[[frac(2,7)]]", "[[2.9]]"],
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 꺾쇠 기호 ⟨x⟩ 및 조건이 한글 문장(x는 정수 / 정수가 아닌 유리수)인 경우 나눔(cases 불가) — 텍스트 혼합 유지",
    note="1+0+1+⟨x⟩=3 → ⟨x⟩=1 → x는 정수가 아닌 유리수; 6/2=3은 정수. 답 ③ 유지(빠른정답 2와 불일치는 1차와 동일)")

# 57. 3babd113 — 정수와 유리수 p66: ⟨x⟩ + 한글 조건 경우 나눔 → 보류 유지
add(id="3babd113", qtype="short",
    question="유리수 [[x]]에 대하여\n⟨[[x]]⟩ = { 0 ([[x]]는 정수) ; 1 ([[x]]는 정수가 아닌 유리수) }\n라 할 때, ⟨[[-frac(2,3)]]⟩ + ⟨[[-2]]⟩ + ⟨[[3.4]]⟩ + ⟨[[0]]⟩의 값을 구하시오.",
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 꺾쇠 기호 ⟨x⟩ 및 조건이 한글 문장(x는 정수 / 정수가 아닌 유리수)인 경우 나눔(cases 불가) — 텍스트 혼합 유지",
    note="1+0+1+0=2. 답 2 유지(빠른정답과 일치)")

# 58. 959c1000 — 유리수의 곱셈과 나눗셈 p12: 위치 표시 ①~④(4개)라 choice 스키마 불가 → short, 답 ②(답 문법 안) → 통과
add(id="959c1000", qtype="short",
    question="다음 계산 과정에서 곱셈의 결합법칙이 이용된 곳은?\n(+4) × [[(-3)]] × (+0.5)\n= (+4) × (+0.5) × [[(-3)]]  ← ①\n= {(+4) × (+0.5)} × [[(-3)]]  ← ②\n= (+2) × [[(-3)]]  ← ③\n= [[-6]]  ← ④",
    figure=None, confidence=0.8,
    note="단계 화살표 표시가 ①~④ 4개라 choice(5개) 스키마 대신 short로 두고 답 ②(답 문법 안의 선지 기호)로 둠. 2→3행 중괄호 묶기가 결합법칙. 양의 부호 (+4)는 텍스트 혼합. 답 ② 유지(빠른정답 없음)")

# ================= esc_sonnet_m1-1_2of3 =================
# 59. fe5c4e92 — 양의 부호와 음의 부호 p14: 답 '+3000'의 양의 부호를 답 문법으로 못 씀 → 보류 유지
add(id="fe5c4e92", qtype="short",
    question="다음 수를 양의 부호 + 또는 음의 부호 −를 사용하여 나타냈을 때, □ 안에 알맞은 수를 써넣으시오.\n[[3000]]원 입금 ⇨ □원",
    figure=None, confidence=0.8,
    needs_review="답 '+3000'의 양의 부호 +가 답 문법(단항 + 없음) 범위 밖 — 3000으로 기재하면 부호 표기라는 문항의 요지가 사라짐",
    note="빈칸 □은 원문에 (가) 표기가 없어 box(n)을 쓰지 않고 텍스트 유지. 답 3000(=+3000) 유지(빠른정답 3과 불일치는 1차와 동일)")

# 60. a21f762f — 양의 부호와 음의 부호 p46: 답 '+23' → 보류 유지
add(id="a21f762f", qtype="short",
    question="0보다 23만큼 큰 수를 부호 +또는 −를 사용하여 나타내시오.",
    figure=None, confidence=0.8,
    needs_review="답 '+23'의 양의 부호 +가 답 문법(단항 + 없음) 범위 밖 — 23으로 기재하면 부호 표기라는 문항의 요지가 사라짐",
    note="답 23(=+23) 유지(빠른정답 'add 23'과 같은 취지)")

# 61. 87be4fdc — 정비례 p32: 선지 ①~⑤가 모두 좌표평면 그래프 → 보류 유지
add(id="87be4fdc", qtype="choice",
    question="[[x]]의 범위가 [[-2]], [[-1]], [[0]], [[1]], [[2]]일 때, [[y = -2x]]의 그래프는?",
    choices=["(그림) 좌표평면 위의 점 5개: [[point(-2, -4)]], [[point(-1, -2)]], [[point(0, 0)]], [[point(1, 2)]], [[point(2, 4)]]", "(그림) 원점과 점 [[point(1, 2)]]를 지나는 직선", "(그림) 좌표평면 위의 점 5개: [[point(-2, 4)]], [[point(-1, 2)]], [[point(0, 0)]], [[point(1, -2)]], [[point(2, -4)]]", "(그림) 원점과 점 [[point(2, -1)]]을 지나는 직선", "(그림) 원점과 점 [[point(1, -2)]]를 지나는 직선"],
    figure=[{"fn": "unsupported", "args": {"raw": "선지 ①~⑤가 각각 모눈 좌표평면 그림(눈금 −2, 2 표시). ① 점 (−2,−4),(−1,−2),(0,0),(1,2),(2,4) ② 원점을 지나는 직선 y=2x ③ 점 (−2,4),(−1,2),(0,0),(1,−2),(2,−4) ④ 원점을 지나는 직선 y=−x/2 ⑤ 원점을 지나는 직선 y=−2x"}}],
    confidence=0.8,
    needs_review="선지 ①~⑤가 모두 좌표평면 그래프 그림 — 문법·텍스트로 표현 불가(설명문으로 대체)",
    note="x가 5개 값이므로 점 5개, y=−2x → (−2,4),…,(2,−4). 답 ③ 유지(빠른정답 1과 불일치는 1차와 동일)")

# 62. e551107c — 등식의 성질 p53: 답이 원문자 ㉡ → 보류 유지
add(id="e551107c", qtype="short",
    question="다음 등식의 성질을 이용하여 일차방정식 [[0.5x - 5 = frac(5,2) + 3x]]의 해를 구하는 과정이다. 이때 등식의 성질 '[[a = b]]이면 [[a c = b c]]이다.'를 이용한 곳을 고르시오. (단, [[c]]는 자연수)\n[[0.5x - 5 = frac(5,2) + 3x]]\n↓ ㉠\n[[frac(1,2) x - 5 = frac(5,2) + 3x]]\n↓ ㉡\n[[x - 10 = 5 + 6x]]\n↓ ㉢\n[[x - 6x - 10 = 5]]\n↓ ㉣\n[[-5x = 5 + 10]]\n↓ ㉤\n[[-5x = 15]]",
    figure=None, confidence=0.8,
    needs_review="답 기호 ㉡(양변에 2를 곱한 곳)이 답 문법(ㄱㄴㄷ·①~⑤·수식) 범위 밖이라 answer 미기재",
    note="본문은 문법 안. 빠른정답 없음")

# 63. 1ce3008b — 등식의 성질 p54: 답이 원문자 ㉢ → 보류 유지
add(id="1ce3008b", qtype="short",
    question="다음 방정식의 풀이 과정에서 등식의 성질 '[[a = b]]이면 [[frac(a, c) = frac(b, c)]]이다.'를 이용한 곳을 고르시오. (단, [[c]]는 자연수)\n[[frac(3,7) x + 2 = 5]]\n↓㉠\n[[3x + 14 = 35]]\n↓㉡\n[[3x = 21]]\n↓㉢\n∴ [[x = 7]]",
    figure=None, confidence=0.8,
    needs_review="답 기호 ㉢(양변을 3으로 나눈 곳)이 답 문법(ㄱㄴㄷ·①~⑤·수식) 범위 밖이라 answer 미기재",
    note="본문은 문법 안. 빠른정답 없음")

# ================= esc_sonnet_m1-1_3of3 =================
# 64. fcc0b4a7 — 혼합 계산 p75: 네 등식이 연산 상자 그림에만 있고 빈칸이 원문자 ㉠~㉣ → 보류 유지
add(id="fcc0b4a7", qtype="short",
    question="아래 그림은 가로로 덧셈식과 곱셈식, 세로로 뺄셈식과 나눗셈식을 나타낸 것이다. 다음 식을 계산하시오.\n(㉢)² − (㉠ × ㉡ + ㉠ ÷ ㉣)",
    figure=[{"fn": "unsupported", "args": {"raw": "상자 계산 그림(화살표로 방향 표시): 가로 윗줄 2/5 + ㉠ = −2, 가로 아랫줄 −1.8 × ㉣ = 2/3, 세로 왼쪽 2/5 − ㉡ = −1.8, 세로 오른쪽 −2 ÷ ㉢ = 2/3. 그 아래 상자에 (㉢)² − (㉠ × ㉡ + ㉠ ÷ ㉣)"}}],
    confidence=0.8,
    needs_review="정보가 그림에만 있음(연산 상자의 네 등식 2/5+㉠=−2, 2/5−㉡=−1.8, −2÷㉢=2/3, −1.8×㉣=2/3) / 빈칸 기호가 원문자 ㉠~㉣(box(n)의 (가)(나) 표기와 다름)이라 계산식도 텍스트",
    note="㉠=−12/5, ㉡=11/5, ㉢=−3, ㉣=−10/27 → 9−6/5=39/5. 답 39/5 유지(빠른정답과 일치)")

# 65. 477729e7 — 수직선 p31: 점 A, B의 위치(등분 눈금)가 그림에만 있음 → 보류 유지
add(id="477729e7", qtype="choice",
    question="다음 수직선 위에 점 A, B에 대응하는 수를 부호 +, −를 사용하여 바르게 나타낸 것은?",
    choices=["A: [[-frac(3,5)]], B: +[[frac(7,4)]]", "A: [[-frac(3,5)]], B: +[[frac(11,4)]]", "A: [[-frac(8,5)]], B: +[[frac(7,4)]]", "A: [[-frac(8,5)]], B: +[[frac(11,4)]]", "A: [[-1.3]], B: +[[2.3]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "수직선(양쪽 화살표), 눈금 −2, −1, 0, +1, +2, +3. −2와 −1 사이를 5등분(등간격 표시)하여 −2에서 두 칸 오른쪽에 점 A. +2와 +3 사이를 4등분(등간격 표시)하여 +2에서 세 칸 오른쪽에 점 B"}}],
    confidence=0.8,
    needs_review="정보가 그림에만 있음(등분 눈금 수직선 위 점 A, B의 위치 — 도형 표현 불가) / 선지의 양의 부호 +는 텍스트",
    note="A=−2+2/5=−8/5, B=+2+3/4=+11/4. 답 ④ 유지(빠른정답 2와 불일치는 1차와 동일)")

# 66. c0d134e4 — 일차식의 덧셈과 뺄셈 p30: 사용자 정의 연산 ★ → 보류 유지
add(id="c0d134e4", qtype="short",
    question="[[x]]에 대한 일차식 [[A]]에서 [[x]]의 계수는 [[-2]]이다.\n[[A]] ★ [[a]] = ([[x = a]]일 때, [[A]]의 식의 값)이라 할 때,\n[[A]] ★ [[(-1)]] + [[A]] ★ [[2]] − [[A]] ★ [[(-2)]] − [[A]] ★ [[5]]의 값을 구하시오.",
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ★(정의가 한글 문장) — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지",
    note="A=−2x+c: (2+c)+(−4+c)−(4+c)−(−10+c)=4. 답 4 유지(빠른정답 14와 불일치는 1차와 동일)")

# 67. c7632096 — 일차식의 덧셈과 뺄셈 p32: ★ → 보류 유지
add(id="c7632096", qtype="short",
    question="[[x]]에 대한 일차식 [[A]]에서 [[x]]의 계수는 [[-5]]이다.\n[[A]] ★ [[a]] = ([[x = a]]일 때, [[A]]의 식의 값)이라 할 때,\n[[A]] ★ [[(-1)]] + [[A]] ★ [[3]] − [[A]] ★ [[(-5)]] − [[A]] ★ [[7]]의 값을 구하시오.",
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ★(정의가 한글 문장) — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지",
    note="A=−5x+c: (5+c)+(−15+c)−(25+c)−(−35+c)=0. 답 0 유지(빠른정답 없음)")

# 68. c3f5bc90 — 일차식의 덧셈과 뺄셈 p59: ★, ◎ → 보류 유지
add(id="c3f5bc90", qtype="choice",
    question="두 단항식 [[A]], [[B]]에 대하여 [[A]]★[[B]] = [[-A + 2B]],\n[[A]]◎[[B]] = [[-2A + 3B]]라 할 때,\n2{([[3x]])★[[y]]} − {[[x]]◎([[-y]])}를 계산한 것은?",
    choices=["[[-4x + 5y]]", "[[-4x + 7y]]", "[[-4x + 9y]]", "[[-2x + 5y]]", "[[-2x + 7y]]"],
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ★, ◎ — v1.5에도 대응 표기 없음, 정의식·계산식(중괄호 포함)을 텍스트 혼합으로 유지",
    note="(3x)★y=−3x+2y, x◎(−y)=−2x−3y → 2(−3x+2y)−(−2x−3y)=−4x+7y. 답 ② 유지(빠른정답 없음)")

# 69. b4aaf009 — 일차식의 덧셈과 뺄셈 p60: ◉, ▼ → 보류 유지
add(id="b4aaf009", qtype="short",
    question="두 단항식 [[A]], [[B]]에 대하여 ([[A]]◉[[B]]) = [[4A - 3B]],\n([[A]]▼[[B]]) = [[B - 2A]]라 할 때, 2([[2x]]◉[[y]]) − ([[x]]▼[[3y]])를 계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱을 구하시오.",
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ◉, ▼ — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지",
    note="2x◉y=8x−3y, x▼3y=3y−2x → 18x−9y → 18×(−9)=−162. 답 −162 유지(빠른정답 없음)")

# 70. b3b71280 — 일차식의 덧셈과 뺄셈 p61: ★, ◎ → 보류 유지
add(id="b3b71280", qtype="short",
    question="두 단항식 [[A]], [[B]]에 대하여 ([[A]]★[[B]]) = [[3A - frac(1,2) B]],\n([[A]]◎[[B]]) = [[2B - A]]라 할 때,\n2{([[x + 2y]])★([[3y - x]])} + {([[x - y]])◎([[2x + 3y]])}를 계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱을 구하시오.",
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ★, ◎ — v1.5에도 대응 표기 없음, 정의식·계산식(중괄호 포함)을 텍스트 혼합으로 유지",
    note="(x+2y)★(3y−x)=7x/2+9y/2 → ×2=7x+9y; (x−y)◎(2x+3y)=3x+7y → 10x+16y → 160. 답 160 유지(빠른정답 없음)")

# 71. ec503ead — 일차식의 덧셈과 뺄셈 p62: ◎, ◆ → 보류 유지
add(id="ec503ead", qtype="choice",
    question="두 단항식 [[A]], [[B]]에 대하여 ([[A]]◎[[B]]) = [[3A - 2B]],\n([[A]]◆[[B]]) = [[B - A]]라 할 때, 2([[x]]◎[[3y]]) − ([[2x]]◆[[y]])를 계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱은?",
    choices=["[[-120]]", "[[-104]]", "[[-91]]", "[[91]]", "[[104]]"],
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ◎, ◆ — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지",
    note="x◎3y=3x−6y, 2x◆y=y−2x → 8x−13y → −104. 답 ② 유지(빠른정답 없음)")

# 72. 41ffd03a — 소인수분해를 이용하여 약수 구하기 p37: 사용자 정의 기호 ⟨a⟩, {a} → 보류 유지
add(id="41ffd03a", qtype="short",
    question="자연수 [[a]]의 약수의 개수를 ⟨[[a]]⟩, 자연수 [[a]]의 모든 약수의 합을 {[[a]]}라 하자. ⟨[[72]]⟩ = [[x]], {[[x]]} = [[y]]일 때, [[x + y]]의 값을 구하시오.",
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 기호 ⟨a⟩(약수의 개수)·{a}(약수의 합) — v1.5에도 대응 표기 없음, 텍스트 혼합 유지",
    note="72=2³·3² → x=12, 12의 약수의 합 28 → 40. 답 40 유지(빠른정답 3과 불일치는 1차와 동일)")

# ================= esc_opus_m1-2_1of1 =================
# 73. 11965fe5 — 부채꼴의 호의 길이와 넓이 p66: 프라임 점 O′, O″는 단독 점 이름(텍스트) → 문법 안, 도형은 unsupported → 통과
add(id="11965fe5", qtype="choice",
    question="다음 그림과 같이 원 O의 지름 BC 위에 두 원 O′, O″의 중심이 있다. [[seg(BC) = 16]] cm이고 [[angle(AOB) = angle(COD) = deg(45)]]일 때, 색칠한 부분의 넓이는?",
    choices=["[[8(pi - 3)]] cm²", "[[10(pi - 4)]] cm²", "[[12(pi - 2)]] cm²", "[[14(pi - 4)]] cm²", "[[16(pi - 2)]] cm²"],
    figure=[{"fn": "unsupported", "args": {"raw": "중심 O, 지름 BC(수평, B 왼쪽·C 오른쪽)인 큰 원. BO·OC를 지름으로 하는 두 작은 원(중심 O′, O″). 큰 원 위의 점 A(좌상)·D(우상), ∠AOB=∠COD=45°. 색칠: 부채꼴 AOB·COD에서 작은 원 바깥 부분과, 반직선 OA·OD와 작은 원 호 사이의 활꼴(O 근처 잎 모양)"}}],
    confidence=0.85,
    note="단독 점 이름 O′, O″는 텍스트(문법 안). 답 ⑤ 재확인: 한쪽 = (부채꼴 8π − 작은 원 내부 (4π+8)) + 현 OE 활꼴 (4π−8) = 8π−16, 양쪽 16(π−2) — 빠른정답 3과 불일치는 1차와 동일")
