# -*- coding: utf-8 -*-
# esc_sonnet_m1-2_1of4 — 이미지 기준 전사 (81 항목 / 80쪽, 중1-2 기본 도형·회전체·각·삼각형·원과 부채꼴·대푯값)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
FIG = "도형 표현 불가: "

# ---------------- 기둥의 겉넓이와 부피 p92
add(id="fc6146b8", qtype="short",
    question=("수학 책에 소개된 회전체의 부피와 관련된 내용의 일부분이다.\n"
              "[그림1]과 같이 색칠된 직사각형을 직선 [[l]]을 축으로 하여 1회전시켜 만든 회전체는 [그림2]와 같다.\n"
              "이 회전체의 부피는 큰 원기둥의 부피에서 가운데 작은 원기둥의 부피를 빼서 구할 수 있으므로\n"
              "[[V = pi pow(b,2) c - pi pow(a,2) c]]\n= [[pi × (b + a) (b - a) c]]\n= [[2 pi × frac(a + b, 2) × (b - a) c]]\n⋮\n"
              "그림과 같이 직선 [[m]]에 대하여 대칭이고 넓이가 23인 색칠된 직사각형과 직선 [[m]]에 평행하고 직선 [[m]]으로부터 "
              "3만큼 떨어져 있는 직선 [[l]]이 있다. 이 직사각형을 직선 [[l]]을 축으로 하여 1회전시켜 만든 회전체의 부피는 [[V]]이다. "
              "[[frac(V, pi)]]의 값을 구하시오."),
    choices=None, derived_answer="138",
    figure=U("[그림1] 세로 회전축 l과 축에서 a, b 떨어진 두 변(높이 c)을 가진 색칠 직사각형; [그림2] 가운데가 빈 원기둥; "
             "아래 그림: 세로 직선 l, l에서 3만큼 떨어진 평행선 m, m에 대칭인 색칠 직사각형"),
    difficulty_est=3, confidence=0.85,
    needs_review=FIG + "회전축·직사각형 도형 3개(스프링 노트 삽화 포함)",
    note="출처 [2012년 3월 고1 30번/4점]. V = 2π × 3 × 23 = 138π → 138. 빠른정답 2와 불일치.")

# ---------------- p99 (한 이미지에 별개 문항 2개, id 1개 → draft_a 대응인 두 번째 문항)
add(id="bb8d92fd", qtype="choice",
    question=("좌표평면 위의 네 점 A[[point(2, 4)]], B[[point(2, 2)]], C[[point(6, 2)]], D[[point(6, 4)]]에 대하여 사각형 ABCD를 "
              "[[x]]축을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 [[sub(V,x)]], [[y]]축을 회전축으로 하여 1회전 시킬 때 "
              "생기는 회전체의 부피를 [[sub(V,y)]]라 하자. 이때 [[ratio(sub(V,x), sub(V,y))]]는?"),
    choices=["[[ratio(2, 3)]]", "[[ratio(3, 2)]]", "[[ratio(3, 4)]]", "[[ratio(4, 3)]]", "[[ratio(4, 5)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.75,
    needs_review=("한 이미지에 별개 문항 2개(id 1개) — draft_a 대응인 두 번째 문항(A(2, 4), B(2, 2), C(6, 2), D(6, 4))으로 전사. "
                  "첫 문항은 A(3, 5), B(3, 1), C(5, 1), D(5, 5), 선지 2:1/2:3/3:2/3:4/4:3, 답 ④(=빠른정답 4)"),
    note="두 번째 문항: V_x = π(16−4)·4 = 48π, V_y = π(36−4)·2 = 64π → 3:4 → ③.")

# ---------------- 대푯값 p20
add(id="a398ae92", qtype="short",
    question=("자료 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], ⋯, [[sub(x,10)]]에 대하여 다음 과정을 차례로 시행하였다. "
              "위의 과정을 시행한 결과 [[sub(x,1)]]과 [[sub(x,2)]]의 평균이 5이고, 자료가 하나씩 추가될 때마다 평균이 2씩 증가하였다. "
              "이때 [[sub(x,10)]]의 값을 구하시오.\n"
              "처음 두 수 [[sub(x,1)]]과 [[sub(x,2)]]의 평균을 구한다.\n"
              "[[sub(x,3)]]을 추가하여 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]]의 평균을 구한다.\n"
              "[[sub(x,4)]]를 추가하여 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]]의 평균을 구한다.\n"
              "⋯\n"
              "[[sub(x,10)]]을 추가하여 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], ⋯, [[sub(x,10)]]의 평균을 구한다."),
    choices=None, derived_answer="39", figure=None, difficulty_est=3,
    note="n개 평균 = 5 + 2(n−2): 9개 평균 19, 10개 평균 21 → x₁₀ = 210 − 171 = 39. 빠른정답 5와 불일치.")

# ---------------- 대푯값 p75
add(id="182778cf", qtype="short",
    question=("평균이 5이고 중앙값이 6인 서로 다른 3개의 자연수가 있다. 이 세 자연수 중 가장 작은 수를 [[a]], 가장 큰 수를 [[b]]라 할 때, "
              "[[a]], [[b]]의 순서쌍 [[point(a, b)]]의 개수를 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2,
    note="a + b = 9, a < 6 < b → (1, 8), (2, 7) → 2 = 빠른정답 ✓.")

# ---------------- 회전체 p66
add(id="7e1d2556", qtype="choice",
    question=("다음 그림과 같은 전개도로 만든 입체도형의 이름과 이 입체도형을 회전축을 포함하는 평면으로 자를 때 생기는 단면의 모양을 "
              "짝 지은 것으로 옳은 것은?"),
    choices=["원뿔 - 이등변삼각형", "원뿔대 - 사다리꼴", "원기둥 - 직사각형", "구 - 원", "원뿔대 - 원"],
    derived_answer="②",
    figure=U("전개도: 위에 큰 원, 가운데 부채꼴에서 작은 부채꼴을 뺀 띠 모양 옆면, 아래에 작은 원(원뿔대의 전개도)"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "원뿔대 전개도",
    note="원뿔대, 축을 포함한 단면은 사다리꼴 → ② = 빠른정답 ✓.")

# ---------------- 회전체 p71
add(id="1328e34d", qtype="choice",
    question="다음 중 아래 그림의 전개도로 만들어지는 입체도형에 대한 설명으로 옳지 않은 것은?",
    choices=["높이는 12 cm이다.", "두 밑면은 평행하다.", "밑면의 둘레의 길이는 [[10 pi]] cm이다.",
             "어떤 평면으로 잘라도 단면은 직사각형이다.", "만들어지는 입체도형은 원기둥이다."],
    derived_answer="④",
    figure=U("원기둥의 전개도: 가로 10π cm, 세로 12 cm인 직사각형과 위·아래에 원 2개"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "원기둥 전개도(치수 10π cm·12 cm는 그림에만)",
    note="밑면에 평행하게 자르면 단면은 원 → ④. 빠른정답 '8 cm'와 불일치.")

# ---------------- 회전체 p80
add(id="6387a0d8", qtype="short",
    question="다음 그림과 같은 원뿔의 전개도에서 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(100)",
    figure=U("원뿔의 전개도: 반지름 18 cm, 중심각 x인 부채꼴과 반지름 5 cm인 밑면 원"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "원뿔 전개도(반지름 18 cm·5 cm는 그림에만)",
    note="2π·18·x/360 = 2π·5 → x = 100°. 빠른정답 4와 불일치.")

# ---------------- 회전체 p82
add(id="264d2cf7", qtype="short",
    question=("매초 3 cm의 속력으로 쉬지 않고 움직이는 두 개미 A, B가 있다. 다음 그림과 같이 [[seg(OP) = 4k]] cm이고 밑면의 반지름의 길이가 "
              "[[k]] cm인 원뿔에서 개미 A는 점 P에서 출발하여 옆면을 돌아 다시 점 P로 되돌아오는 가장 짧은 선을 따라 움직인다. "
              "이 선의 길이의 절반인 지점을 점 P′이라 하면 OP′ = 15 cm일 때, 개미 B는 점 O에서 출발하여 OP′을 따라 왕복하며 움직인다. "
              "두 개미 A, B가 동시에 출발하여 두 번째 만날 때까지 걸리는 시간은 몇 초인지 구하시오. "
              "(단, [[k]]는 상수이고, 두 개미 A, B의 크기는 생각하지 않는다.)"),
    choices=None, derived_answer="15",
    figure=U("원뿔: 꼭짓점 O, 모선 OP = 4k cm, 밑면 반지름 k cm, 옆면 위 P에서 출발해 P로 돌아오는 최단 곡선, 그 중점 P′, OP′ = 15 cm"),
    difficulty_est=4, confidence=0.75,
    needs_review="프라임 점 라벨(P′) 문법 범위 밖: 선분 OP′(윗줄) 텍스트 혼합 / " + FIG + "원뿔 위 최단 경로 도형",
    note="전개도 부채꼴 90°, PP′ = OP′ = 15 → A의 경로 30 cm; 두 개미는 P′에서만 만남(t = 5, 15, …) → 15초. 빠른정답 120과 불일치.")

# ---------------- 점, 직선, 평면의 위치 관계 p13
add(id="04b88cae", qtype="choice",
    question="다음 중 아래 그림의 사다리꼴에 대한 설명으로 옳지 않은 것은?",
    choices=["[[line(AD)]]와 [[line(BC)]]는 평행하다.", "[[line(AB)]]와 [[line(CD)]]는 만난다.", "점 C는 [[line(AD)]] 위에 있다.",
             "[[line(BC)]]와 [[line(CD)]]는 점 C에서 만난다.", "점 D는 [[line(AD)]]와 [[line(CD)]]의 교점이다."],
    derived_answer="③",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, AD ∥ BC)"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "사다리꼴 ABCD 도형",
    note="점 C는 직선 AD 위에 없음 → ③. 빠른정답 5와 불일치.")

# ---------------- p63
add(id="9a38d9c8", qtype="choice",
    question=("아래 그림에서 [[perp(l, P)]]이고 점 H는 직선 [[l]] 위의 점 A에서 평면 [[P]]에 내린 수선의 발이다. "
              "점 A와 평면 [[P]] 사이의 거리가 5 cm일 때, 다음 중 옳지 않은 것은? (단, 두 직선 [[m]], [[n]]은 평면 [[P]] 위에 있다.)"),
    choices=["[[perp(l, n)]]", "[[perp(l, m)]]", "[[perp(seg(AH), m)]]", "[[perp(m, n)]]", "[[seg(AH) = 5]] cm"],
    derived_answer="④",
    figure=U("평면 P(평행사변형), P 위의 두 직선 m, n이 점 H에서 만남, H를 지나 P에 수직인 직선 l, l 위의 점 A(P 위쪽), H에 직각 표시"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "평면·수직 직선 공간도형",
    note="m ⊥ n은 알 수 없음 → ④. 빠른정답 '10cm'와 불일치.")

# ---------------- p65
add(id="66ed4bdd", qtype="choice",
    question=("아래 그림과 같이 두 평면 [[P]], [[Q]]가 있다. [[angle(AOB) = angle(AOC) = deg(90)]]일 때, "
              "다음 보기에서 옳지 않은 것을 모두 고르면? (정답 2개)"),
    choices=["[[perp(P, Q)]]", "[[perp(line(AO), line(CO))]]", "[[perp(seg(BD), seg(AO))]]", "[[angle(OAB) = angle(OBA)]]", "[[seg(BO) = seg(CO)]]"],
    derived_answer="④, ⑤",
    figure=U("수평 평면 P와 그 위에 세워진 평면 Q가 직선 BD에서 만남, O는 BD 위의 점, A는 Q 위(O의 위쪽), C는 P 위, 선분 AO·OC, O에 직각 표시"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "두 평면 공간도형",
    note="AO ⊥ P → ①②③ 참, ④⑤는 알 수 없음 → ④, ⑤ = 빠른정답 ✓.")

# ---------------- p71
add(id="0059bb10", qtype="short",
    question=("다음 그림은 직육면체를 [[seg(AE) = seg(DH)]], [[seg(BF) = seg(CG)]], [[seg(AE) != seg(BF)]]가 되도록 잘라 만든 입체도형이다. "
              "이 입체도형에서 각 모서리를 연장한 직선을 그을 때, 직선 AD와 평행한 직선의 개수를 [[a]], 면 CGHD와 수직인 면의 개수를 [[b]]라 하자. "
              "이때 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="12",
    figure=U("직육면체를 비스듬히 잘라 만든 입체(점선은 잘려 나간 부분): 윗면 ABCD(A·D가 B·C보다 높음), 아랫면 EFGH, 세로 모서리 AE·BF·CG·DH"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "잘린 직육면체 공간도형",
    note="AD ∥ BC, EH, FG → a = 3; 면 CGHD와 수직인 면 ABCD, EFGH, BFGC, AEHD → b = 4 → 12. 빠른정답 4와 불일치.")

# ---------------- p72
add(id="68e59606", qtype="short",
    question=("다음 그림은 직육면체를 [[seg(AD) = seg(BC)]], [[seg(EH) = seg(FG)]], [[seg(AD) != seg(EH)]]가 되도록 잘라 만든 입체도형이다. "
              "이 입체도형에서 각 모서리를 연장한 직선을 그을 때, 직선 CG와 평행한 직선의 개수를 [[a]], 면 BFGC와 수직인 면의 개수를 [[b]]라 하자. "
              "이때 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="9",
    figure=U("직육면체를 비스듬히 잘라 만든 입체(점선은 잘려 나간 부분): 윗면 ABCD, 아랫면 EFGH, 오른쪽 면 CDHG가 경사짐, 세로 모서리 AE·BF·CG·DH"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "잘린 직육면체 공간도형",
    note="CG ∥ AE, BF, DH → a = 3; 면 BFGC와 수직인 면 ABFE, ABCD, EFGH → b = 3 → 9. 빠른정답 2와 불일치.")

# ---------------- p73
add(id="140549d0", qtype="short",
    question=("다음 그림은 삼각기둥을 [[seg(AD) = seg(CF)]], [[seg(AD) != seg(BE)]]가 되도록 잘라 만든 입체도형이다. "
              "이 입체도형에서 각 모서리를 연장한 직선을 그을 때, 직선 BE와 평행한 직선의 개수를 [[a]], 면 DEF와 수직인 면의 개수를 [[b]]라 하자. "
              "이때 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="6",
    figure=U("삼각기둥을 비스듬히 잘라 만든 입체(점선은 잘려 나간 부분): 윗면 ABC(A에 직각 표시), 아랫면 DEF, 세로 모서리 AD·BE·CF"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "잘린 삼각기둥 공간도형",
    note="BE ∥ AD, CF → a = 2; 면 DEF와 수직인 면은 옆면 3개 → b = 3 → 6. 빠른정답 2와 불일치.")

# ---------------- p91
add(id="ad257630", qtype="choice",
    question="한 평면 위에 세 직선 [[l]], [[m]], [[n]]이 있다. [[par(l, m)]], [[perp(l, n)]]일 때, 두 직선 [[m]]과 [[n]]의 위치 관계는?",
    choices=["[[par(m, n)]]", "일치한다.", "[[perp(m, n)]]", "두 점에서 만난다.", "꼬인 위치에 있다."],
    derived_answer="③", figure=None, difficulty_est=1,
    note="l ∥ m, l ⊥ n → m ⊥ n → ③. 빠른정답 5와 불일치.")

# ---------------- p99
add(id="cfd7b31f", qtype="choice",
    question="[[l]], [[m]], [[n]]은 서로 다른 직선이고, [[P]]는 평면일 때, 다음 중 참인 것은?",
    choices=["[[perp(l, P)]], [[perp(m, P)]]이면 [[par(l, m)]]이다.", "[[perp(l, P)]], [[perp(m, P)]]이면 [[perp(l, m)]]이다.",
             "[[perp(l, m)]], [[perp(l, n)]]이면 [[par(m, n)]]이다.", "[[perp(l, m)]], [[perp(l, n)]]이면 [[perp(m, n)]]이다.",
             "[[par(l, P)]], [[perp(m, P)]]이면 [[par(l, m)]]이다."],
    derived_answer="①", figure=None, difficulty_est=2,
    note="원문은 평행을 '//'로 표기. 한 평면에 수직인 두 직선은 평행 → ①. 빠른정답 4와 불일치.")

# ---------------- 각 p2 (선지 4개)
add(id="d1d7781a", qtype="short",
    question="다음 그림을 보고 □ 안에 들어갈 알맞은 것을 고르시오.\n[[angle(DOE)]]는 □이다.\n① 예각 ② 직각 ③ 둔각 ④ 평각",
    choices=None, derived_answer="①",
    figure=U("직선 BC(가로, B 왼쪽·C 오른쪽) 위의 점 O, O에서 위로 수직인 반직선 OE(직각 표시), 왼쪽 위로 반직선 OA, 오른쪽 위로 반직선 OD"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 4개(5지 규격 밖) — 보기를 본문에 텍스트로 포함 / " + FIG + "각 도형",
    note="OD는 OE와 OC 사이 → ∠DOE는 예각 → ① = 빠른정답 ✓.")

# ---------------- 각 p4 (선지 4개)
add(id="4dcf86ce", qtype="short",
    question="다음 그림을 보고 □ 안에 들어갈 알맞은 것을 고르시오.\n[[angle(POQ)]]는 □이다.\n① 평각 ② 둔각 ③ 직각 ④ 예각",
    choices=None, derived_answer="①",
    figure=U("직선 PQ(세로, P 위·Q 아래) 위의 점 O, O에서 오른쪽으로 수직인 반직선 OS(직각 표시), 오른쪽 위로 반직선 OT, 오른쪽 아래로 반직선 OR"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 4개(5지 규격 밖) — 보기를 본문에 텍스트로 포함 / " + FIG + "각 도형",
    note="P, O, Q 한 직선 위 → 평각 → ①. 빠른정답 5와 불일치.")

# ---------------- 각 p5 (선지 4개)
add(id="0869dc1c", qtype="short",
    question="다음 그림을 보고 □ 안에 들어갈 알맞은 것을 고르시오.\n[[angle(POQ)]]는 □이다.\n① 예각 ② 직각 ③ 둔각 ④ 평각",
    choices=None, derived_answer="④",
    figure=U("직선 PQ(세로, Q 위·P 아래) 위의 점 O, O에서 왼쪽으로 수직인 반직선 OS(직각 표시), 왼쪽 위로 반직선 OR"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 4개(5지 규격 밖) — 보기를 본문에 텍스트로 포함 / " + FIG + "각 도형",
    note="P, O, Q 한 직선 위 → 평각 → ④. 빠른정답 1과 불일치.")

# ---------------- 각 p8
add(id="21c5034b", qtype="short",
    question="다음 그림에서 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(26)",
    figure=U("직각(꼭짓점에 직각 표시)을 한 반직선으로 나눈 그림: 위쪽 각 2x+12°, 아래쪽 각 x"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "각 표시 도형(2x+12°, x는 그림에만)",
    note="(2x + 12) + x = 90 → x = 26°. 빠른정답 4와 불일치.")

# ---------------- 각 p12
add(id="6ea63a7b", qtype="short",
    question=("다음 그림에서 [[angle(AOC) = angle(BOD) = deg(90)]], [[angle(AOB) + angle(COD) = deg(50)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(65)",
    figure=U("점 O에서 나가는 네 반직선 OA(왼쪽 위), OB(위), OC(오른쪽 위), OD(오른쪽); ∠AOC·∠BOD에 직각 표시, ∠BOC = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "네 반직선 각 도형",
    note="∠AOB + ∠COD + 2x = 180 → x = 65°. 빠른정답 2와 불일치.")

# ---------------- 각 p14
add(id="9572e2ed", qtype="short",
    question=("다음 그림에서 [[perp(seg(OA), seg(OC))]], [[perp(seg(OB), seg(OD))]], [[angle(x) + angle(z) = deg(40)]]일 때, "
              "[[angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(70)",
    figure=U("점 O에서 나가는 네 반직선 OA(왼쪽 위), OB(위), OC(오른쪽 위), OD(오른쪽); ∠AOB = x, ∠BOC = y, ∠COD = z, 직각 표시 2개"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "네 반직선 각 도형",
    note="x + y = y + z = 90 → 2y = 140 → y = 70°. 빠른정답 1과 불일치.")

# ---------------- 각 p15
add(id="79f9a395", qtype="short",
    question="다음 그림에서 [[angle(BOC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(34)",
    figure=U("점 O에서 위로 반직선 OA, 오른쪽으로 반직선 OC(∠AOC 직각 표시), 오른쪽 위로 반직선 OB; ∠AOB = 3x°+5°, ∠BOC = 2x°"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "각 표시 도형(3x°+5°, 2x°는 그림에만)",
    note="5x + 5 = 90 → x = 17 → ∠BOC = 34°. 빠른정답 deg(65)와 불일치.")

# ---------------- 각 p23
add(id="2efcce9e", qtype="short",
    question="다음 그림에서 [[angle(AOB)]]가 평각일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(27)",
    figure=U("직선 AB 위의 점 O, O에서 위로 수직인 반직선(직각 표시), 왼쪽 위로 반직선; 왼쪽 각 63°, 두 반직선 사이 각 x"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "각 표시 도형(63°는 그림에만)",
    note="63 + x + 90 = 180 → x = 27°. 빠른정답 deg(67)과 불일치.")

# ---------------- 각 p28
add(id="0ff35e1a", qtype="choice",
    question="아래 그림에서 [[ratio(angle(a), angle(b), angle(c)) = ratio(1, 2, 2)]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[angle(a) = deg(36)]]", "[[angle(b) = deg(72)]]", "[[angle(c) = deg(82)]]",
             "[[angle(a) + angle(b) + angle(c) = deg(180)]]", "[[angle(c)]]는 예각이다."],
    derived_answer="③",
    figure=U("직선 위의 한 점에서 두 반직선이 나가 평각을 왼쪽부터 세 각 a, b, c로 나눔"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "평각 분할 도형",
    note="a = 36, b = c = 72 → ③ = 빠른정답 ✓.")

# ---------------- 각 p31
add(id="3cc34c60", qtype="choice",
    question=("다음 그림은 직사각형 모양의 종이를 [[seg(DE)]]를 접는 선으로 하여 접은 것이다. ∠BEC′ : ∠DEC′ = 4 : 3일 때, "
              "∠BEC′의 크기는?"),
    choices=["[[deg(36)]]", "[[deg(54)]]", "[[deg(72)]]", "[[deg(80)]]", "[[deg(90)]]"],
    derived_answer="③",
    figure=U("직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)를 DE(E는 BC 위)로 접어 C가 C′으로 이동, 점선 EC·CD, E에 각 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review="프라임 점 라벨(C′) 문법 범위 밖: 각 텍스트 혼합 / " + FIG + "종이 접기 도형",
    note="4k + 3k + 3k = 180 → ∠BEC′ = 72° → ③ = 빠른정답 ✓.")

# ---------------- 각 p33
add(id="b8f46bdf", qtype="short",
    question="다음 그림에서 [[angle(COD) = frac(1,5) angle(AOD)]]일 때, [[angle(BOD)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(67.5)",
    figure=U("직선 AB 위의 점 O, O에서 위로 수직인 반직선 OC(직각 표시), OC의 오른쪽에 반직선 OD"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "각 도형",
    note="∠COD = (90 + ∠COD)/5 → ∠COD = 22.5 → ∠BOD = 67.5° = 빠른정답 ✓.")

# ---------------- 각 p35
add(id="a24b6974", qtype="short",
    question="다음 그림에서 [[angle(AOD) = 3 angle(BOC)]]일 때, [[angle(BOC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(22.5)",
    figure=U("직선 DC(세로, D 위·C 아래) 위의 점 O, 왼쪽 위로 반직선 OA, 왼쪽 아래로 반직선 OB, ∠AOB에 직각 표시"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "각 도형(직각 표시는 그림에만)",
    note="3∠BOC + 90 + ∠BOC = 180 → 22.5°. 빠른정답 14와 불일치.")

# ---------------- 각 p37
add(id="52165fc3", qtype="short",
    question=("다음 그림에서 [[angle(DOE) = deg(90)]], [[angle(AOB) = 4 angle(BOC)]], [[angle(COE) = 3 angle(COD)]]일 때, "
              "[[angle(BOD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(54)",
    figure=U("직선 AE 위의 점 O, O에서 위로 수직인 반직선 OD(직각 표시), 왼쪽 위로 반직선 OB, OC(OB가 더 바깥쪽)"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "각 도형",
    note="∠COD = 45, ∠BOC = 9 → ∠BOD = 54°. 빠른정답 deg(45)와 불일치.")

# ---------------- 각 p38
add(id="7934fa20", qtype="short",
    question=("다음 그림의 네 반직선 O[[sub(A,1)]], O[[sub(A,2)]], O[[sub(A,3)]], O[[sub(A,4)]] 중에서 두 반직선을 변으로 하고 점 O를 "
              "꼭짓점으로 하는 모든 각에 대하여 작은 쪽의 각의 크기의 합이 [[deg(470)]]이고 [[angle(c) = 2 angle(a)]], [[3 angle(b) = 5 angle(a)]]일 때, "
              "∠[[sub(A,1)]]O[[sub(A,4)]]의 크기를 구하시오. (단, [[deg(0)]] < ∠[[sub(A,1)]]O[[sub(A,4)]] < [[deg(180)]])"),
    choices=None, derived_answer="deg(140)",
    figure=U("점 O에서 나가는 네 반직선 OA₁(오른쪽), OA₂(오른쪽 위), OA₃(위), OA₄(왼쪽 위); 이웃한 각 a = ∠A₁OA₂, b = ∠A₂OA₃, c = ∠A₃OA₄"),
    difficulty_est=3, confidence=0.8,
    needs_review="첨자 점 라벨(A₁~A₄) 문법 범위 밖: 반직선(화살표 표기)·각 텍스트 혼합 / " + FIG + "네 반직선 도형",
    note="3a + 4b + 3c = 470, c = 2a, b = 5a/3 → a = 30, b = 50, c = 60 → 140°. 빠른정답 deg(22.5)와 불일치.")

# ---------------- 각 p39
add(id="17272910", qtype="short",
    question=("다음 그림의 네 반직선 O[[sub(A,1)]], O[[sub(A,2)]], O[[sub(A,3)]], O[[sub(A,4)]] 중에서 두 반직선을 변으로 하고 점 O를 "
              "꼭짓점으로 하는 모든 각에 대하여 작은 쪽의 각의 크기의 합이 [[deg(430)]]이고 [[angle(c) = 2 angle(a)]], [[3 angle(b) = 4 angle(a)]]일 때, "
              "∠[[sub(A,1)]]O[[sub(A,4)]]의 크기를 구하시오. (단, [[deg(0)]] < ∠[[sub(A,1)]]O[[sub(A,4)]] < [[deg(180)]])"),
    choices=None, derived_answer="deg(130)",
    figure=U("점 O에서 나가는 네 반직선 OA₁(오른쪽), OA₂(오른쪽 위), OA₃(위), OA₄(왼쪽 위); 이웃한 각 a = ∠A₁OA₂, b = ∠A₂OA₃, c = ∠A₃OA₄"),
    difficulty_est=3, confidence=0.8,
    needs_review="첨자 점 라벨(A₁~A₄) 문법 범위 밖: 반직선(화살표 표기)·각 텍스트 혼합 / " + FIG + "네 반직선 도형",
    note="3a + 4b + 3c = 430, c = 2a, b = 4a/3 → a = 30, b = 40, c = 60 → 130°. 빠른정답 deg(120)과 불일치.")

# ---------------- 각 p40
add(id="f4ea7ec4", qtype="short",
    question=("다음 그림에서 [[angle(AOC) = deg(90)]]이고 [[angle(AOD) = 7 angle(COD)]], [[angle(DOE) = frac(1,3) angle(DOB)]]일 때, "
              "[[angle(COE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(40)",
    figure=U("직선 AB 위의 점 O, O에서 위로 수직인 반직선 OC(직각 표시), OC의 오른쪽에 반직선 OD, OE가 차례로"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "각 도형",
    note="∠COD = 15, ∠DOB = 75, ∠DOE = 25 → ∠COE = 40°. 빠른정답 deg(54)와 불일치.")

# ---------------- 각 p47
add(id="f9a682c9", qtype="short",
    question=("다음 그림과 같은 원 O에서 [[angle(POQ) = deg(30)]]이고 두 반직선 OA, OB는 각각 일정한 속도로 점 O를 중심으로 "
              "시곗바늘이 도는 방향으로 회전한다. 원 O를 1회전하는 데 [[ray(OA)]]는 30분이 걸리고 [[ray(OB)]]는 50분이 걸린다. "
              "두 반직선이 현재의 위치에서 동시에 출발하여 처음으로 [[angle(AOB) = deg(90)]]가 될 때까지 걸리는 시간은 몇 분인지 구하시오."),
    choices=None, derived_answer="25",
    figure=U("원 O, 중심에서 위쪽 원 위의 점 P로 향하는 반직선 OA(A는 OP 위)와 오른쪽 위 원 위의 점 Q로 향하는 반직선 OB(B는 OQ 위), ∠POQ = 30°"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "원 안 두 반직선 도형",
    note="OA 12°/분, OB 7.2°/분; OA가 30° 뒤에서 출발 → 4.8t − 30 = 90 → t = 25분. 빠른정답 4와 불일치.")

# ---------------- 각 p48
add(id="a17a27ee", qtype="short",
    question=("다음 그림과 같은 원 O에서 [[angle(POQ) = deg(20)]]이고 두 반직선 OA, OB는 각각 일정한 속도로 점 O를 중심으로 "
              "시곗바늘이 도는 방향으로 회전한다. 원 O를 1회전하는 데 [[ray(OA)]]는 45분이 걸리고 [[ray(OB)]]는 60분이 걸린다. "
              "두 반직선이 현재의 위치에서 동시에 출발하여 처음으로 [[angle(AOB) = deg(100)]]가 될 때까지 걸리는 시간은 몇 분인지 구하시오."),
    choices=None, derived_answer="60",
    figure=U("원 O, 중심에서 위쪽 원 위의 점 P로 향하는 반직선 OA(A는 OP 위)와 오른쪽 위 원 위의 점 Q로 향하는 반직선 OB(B는 OQ 위), ∠POQ = 20°"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "원 안 두 반직선 도형",
    note="OA 8°/분, OB 6°/분; 2t − 20 = 100 → t = 60분. 빠른정답 2와 불일치.")

# ---------------- 각 p49
add(id="a9c435d9", qtype="short",
    question=("다음 그림과 같은 원 O에서 [[angle(POQ) = deg(40)]]이고 두 반직선 OA, OB는 각각 일정한 속도로 점 O를 중심으로 "
              "시곗바늘이 도는 방향으로 회전한다. 원 O를 1회전하는 데 [[ray(OA)]]는 20분이 걸리고 [[ray(OB)]]는 40분이 걸린다. "
              "두 반직선이 현재의 위치에서 동시에 출발하여 처음으로 [[angle(AOB) = deg(95)]]가 될 때까지 걸리는 시간은 몇 분인지 구하시오."),
    choices=None, derived_answer="15",
    figure=U("원 O, 중심에서 위쪽 원 위의 점 P로 향하는 반직선 OA(A는 OP 위)와 오른쪽 위 원 위의 점 Q로 향하는 반직선 OB(B는 OQ 위), ∠POQ = 40°"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "원 안 두 반직선 도형",
    note="OA 18°/분, OB 9°/분; 9t − 40 = 95 → t = 15분. 빠른정답 2와 불일치.")

# ---------------- 각 p53
add(id="c3436c01", qtype="short",
    question=("다음 그림과 같이 네 직선 AB, CD, EF, GH가 점 O에서 만나고 [[ratio(angle(AOC), angle(COB)) = ratio(1, 3)]], "
              "[[angle(AOE) = 4 angle(COE)]], [[angle(EOB) = 3 angle(EOG)]]일 때, [[angle(HOD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(55)",
    figure=U("점 O에서 만나는 네 직선: AB(가로, A 왼쪽·B 오른쪽), CD(C 왼쪽 위·D 오른쪽 아래), EF(E 위 왼쪽·F 아래 오른쪽), GH(G 위·H 아래)"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "네 직선 교차 도형",
    note="∠AOC = 45, ∠COE = 15, ∠EOG = 40 → ∠GOC = 55 = ∠HOD(맞꼭지각). 빠른정답 1과 불일치.")

# ---------------- 각 p57 (선지 4개만 보임)
add(id="f302bd2c", qtype="short",
    question=("다음 그림에서 [[angle(x)]], [[angle(y)]]의 크기는?\n"
              "① [[angle(x) = deg(68)]], [[angle(y) = deg(68)]] ② [[angle(x) = deg(68)]], [[angle(y) = deg(78)]] "
              "③ [[angle(x) = deg(78)]], [[angle(y) = deg(68)]] ④ [[angle(x) = deg(78)]], [[angle(y) = deg(78)]]"),
    choices=None, derived_answer="①",
    figure=U("두 직선이 한 점에서 교차, 왼쪽 각 112°, 위쪽 각 y, 아래쪽 각 x"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 4개만 보임(5지 규격 밖, 이미지 하단 잘림 가능) — 보기를 본문에 텍스트로 포함 / " + FIG + "두 직선 교차 도형",
    note="x = y = 180 − 112 = 68° → ①. 빠른정답 deg(66)과 불일치.")

# ---------------- 각 p59 (선지 3개만 보임)
add(id="8d29ed09", qtype="short",
    question="다음 그림과 같은 사다리꼴 ABCD에서 [[seg(BC)]]와 직교하는 변은?\n① [[seg(AB)]] ② [[seg(AD)]] ③ [[seg(CD)]]",
    choices=None, derived_answer="①",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 3 cm, AB = 6 cm, BC = 6 cm, A·B에 직각 표시"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 3개만 보임(이미지 하단 잘림 가능) — 보기를 본문에 텍스트로 포함 / " + FIG + "사다리꼴 치수 도형",
    note="∠B = 90° → AB ⊥ BC → ①. 빠른정답 deg(15)와 불일치.")

# ---------------- 각 p62
add(id="d323e0fe", qtype="choice",
    question="다음 그림을 보고 설명한 것으로 옳지 않은 것은?",
    choices=["[[perp(l, m)]]", "직선 AB는 직선 PQ의 수선이다.", "[[angle(AMQ)]]의 크기는 [[deg(90)]]이다.",
             "선분 PM의 수직이등분선은 직선 AB이다.", "점 M은 점 B에서 직선 PQ에 내린 수선의 발이다."],
    derived_answer="④",
    figure=U("세로 직선 l(P 위, Q 아래)과 가로 직선 m(A 왼쪽, B 오른쪽)이 점 M에서 수직으로 만남(직각 표시), AM = MB(한 줄 표시), PM = MQ(두 줄 표시)"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "수직 직선·등분 표시 도형",
    note="AB는 PQ의 수직이등분선(PM의 것이 아님) → ④. 빠른정답 1과 불일치.")

# ---------------- 각 p63 (id 2개, ○× 판정형)
dup(["03fef3c1", "a2f64b7d"], qtype="short",
    question=("다음 그림과 같은 사다리꼴 ABCD에 대한 설명으로 옳은 것은 '○'를, 옳지 않은 것은 '×'를 고르시오.\n"
              "[[perp(seg(AB), seg(AD))]]\n① ○ ② ×"),
    choices=None, derived_answer="①",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 24 cm, AB = 20 cm, DC = 30 cm, BC = 26 cm, A·D에 직각 표시"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 2개(○× 판정형, 5지 규격 밖) — 보기를 본문에 텍스트로 포함 / " + FIG + "사다리꼴 치수 도형",
    note="A에 직각 표시 → AB ⊥ AD 옳음 → ① = 빠른정답 ✓.")

# ---------------- 각 p64
add(id="cd30823a", qtype="short",
    question=("다음 그림과 같은 사다리꼴 ABCD에 대한 설명으로 옳은 것은 '○'를, 옳지 않은 것은 '×'를 고르시오.\n"
              "[[perp(seg(BC), seg(CD))]]\n① ○ ② ×"),
    choices=None, derived_answer="②",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 15 cm, AB = 12 cm, DC = 10 cm, BC = 17 cm, A·D에 직각 표시"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 2개(○× 판정형, 5지 규격 밖) — 보기를 본문에 텍스트로 포함 / " + FIG + "사다리꼴 치수 도형",
    note="직각은 A·D에만 있고 BC는 경사 → 옳지 않음 → ② = 빠른정답 ✓.")

# ---------------- 각 p65
add(id="b8a93ef2", qtype="short",
    question=("다음 그림과 같은 사다리꼴 ABCD에 대한 설명으로 옳은 것은 '○'를, 옳지 않은 것은 '×'를 고르시오.\n"
              "[[perp(seg(AD), seg(CD))]]\n① ○ ② ×"),
    choices=None, derived_answer="②",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 16 cm, AB = 12 cm, BC = 11 cm, CD = 13 cm, A·B에 직각 표시"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 2개(○× 판정형, 5지 규격 밖) — 보기를 본문에 텍스트로 포함 / " + FIG + "사다리꼴 치수 도형",
    note="직각은 A·B에만 있고 CD는 경사 → 옳지 않음 → ② = 빠른정답 ✓.")

# ---------------- 각 p73
add(id="51f45682", qtype="choice",
    question="다음 그림과 같은 사다리꼴 ABCD의 넓이가 32 cm²일 때, 점 A에서 [[line(BC)]]까지의 거리는?",
    choices=["3 cm", "4 cm", "5 cm", "6 cm", "7 cm"],
    derived_answer="②",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 7 cm, BC = 9 cm, A·B에 직각 표시, 내부 색칠"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "사다리꼴 치수 도형(7 cm·9 cm는 그림에만)",
    note="(7 + 9)h/2 = 32 → h = 4 cm → ②. 빠른정답 '15 cm'와 불일치.")

# ---------------- 각 p84
add(id="4def92d0", qtype="short",
    question=("다음 그림과 같이 세 직선 AB, CD, EF가 한 점 O에서 만나고 [[angle(AOF) = deg(90)]], [[angle(AOC) = angle(EOG)]], "
              "[[ratio(angle(BOD), angle(COE)) = ratio(1, 4)]]일 때, [[angle(GOB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(72)",
    figure=U("점 O에서 만나는 세 직선 AB(가로), CD(C 왼쪽 위·D 오른쪽 아래), EF(세로, E 위·F 아래)와 반직선 OG(오른쪽 위, OE 가까이), ∠AOF에 직각 표시"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "세 직선·반직선 교차 도형",
    note="∠AOC = ∠BOD = 18, ∠COE = 72 → ∠EOG = 18 → ∠GOB = 72°. 빠른정답 45와 불일치.")

# ---------------- 각 p90
add(id="0627150b", qtype="short",
    question="다음 그림에서 [[angle(COD)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(61)",
    figure=U("점 O에서 만나는 두 직선 AC(A 위·C 아래)와 BE(B 왼쪽·E 오른쪽), 반직선 OF(오른쪽 위), OD(오른쪽 아래); "
             "∠AOF = x°, ∠FOE = 3x°−15°, ∠EOD = 2x°−10°, ∠BOC = 81°"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "각 표시 도형(x°, 3x°−15°, 2x°−10°, 81°는 그림에만)",
    note="∠AOE = 4x − 15 = 81 → x = 24, ∠EOD = 38 → ∠COD = 180 − 81 − 38 = 61°. 빠른정답 deg(40)과 불일치.")

# ---------------- 삼각형의 내각과 외각 p1
add(id="41a39dfe", qtype="choice",
    question="다음 그림과 같이 [[seg(AC)]]와 [[seg(BD)]]의 교점을 E라 할 때, [[angle(x)]]의 크기는?",
    choices=["[[deg(90)]]", "[[deg(95)]]", "[[deg(100)]]", "[[deg(105)]]", "[[deg(110)]]"],
    derived_answer="③",
    figure=U("B(왼쪽 아래)·C(오른쪽 아래)에 직각 표시, A는 B의 위, D는 C의 위(더 높음), 선분 AC와 BD의 교점 E; ∠BAC = 60°, ∠BDC = 40°, ∠BEC = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "직각삼각형 2개 겹침 도형(60°, 40°는 그림에만)",
    note="∠ACB = 30, ∠DBC = 50 → x = 100° → ③ = 빠른정답 ✓.")

# ---------------- p2
add(id="965715f4", qtype="short",
    question=("다음 그림에서 [[cong(tri(ABC), tri(EBD))]]이고 [[angle(CAB) = deg(42)]], [[angle(EBA) = deg(34)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(34)",
    figure=U("A(왼쪽 아래), B(오른쪽 아래), C(위 가운데), D(오른쪽 위), E(왼쪽 위); 삼각형 ABC와 EBD가 겹침, ∠CAB = 42°(A), ∠EBA = 34°(B, BA와 BE 사이), ∠CBD = x"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "합동 삼각형 겹침 도형",
    note="∠ABC = ∠EBD → x = ∠CBD = ∠ABE = 34°(42°는 미사용). 빠른정답 31과 불일치.")

# ---------------- p4
add(id="e40cf02c", qtype="short",
    question=("[[angle(C) = deg(90)]]인 삼각형 모양의 종이 ABC를 [[seg(BD)]]를 접는 선으로 하여 접었을 때 점 A가 이동한 점을 A′라 하고, "
              "BA′과 [[seg(AC)]]의 교점을 E라 하자. 다시 [[seg(BE)]]를 접는 선으로 하여 종이를 접었더니 다음 그림과 같이 점 C가 "
              "[[seg(BD)]] 위의 점 C′과 겹쳐졌다. [[angle(BDE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(54)",
    figure=U("직각삼각형 ABC(C에 직각, B 왼쪽 아래, C 오른쪽 아래, A 위), ∠A = 36°, D·E는 AC 위, A′은 BE의 연장선 위(오른쪽), C′은 BD 위, 접힌 부분 색칠"),
    difficulty_est=3, confidence=0.8,
    needs_review="프라임 점 라벨(A′, C′) 문법 범위 밖: 선분 BA′ 텍스트 혼합 / " + FIG + "종이 접기 도형(36°는 그림에만)",
    note="∠B = 54가 삼등분 → ∠ABD = 18, ∠ADB = 126 → ∠BDE = 54°. 빠른정답 3과 불일치.")

# ---------------- p7
add(id="3c713b46", qtype="choice",
    question="다음 그림에서 [[angle(x)]]의 크기는?",
    choices=["[[deg(25)]]", "[[deg(30)]]", "[[deg(35)]]", "[[deg(40)]]", "[[deg(45)]]"],
    derived_answer="③",
    figure=U("삼각형 ABC(A 위, B 아래 왼쪽, C 아래 오른쪽): ∠A = x, ∠B = 3∠x, ∠C = 2∠x − 30°"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "삼각형 각 표시 도형(3∠x, 2∠x−30°는 그림에만)",
    note="6x − 30 = 180 → x = 35° → ③. 빠른정답 54와 불일치.")

# ---------------- p11
add(id="f61d33ab", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[angle(CAD) = 2 angle(BAD)]]이고 [[angle(B) = deg(46)]], [[angle(C) = deg(62)]]일 때, "
              "[[angle(ADC)]]의 크기는?"),
    choices=["[[deg(64)]]", "[[deg(66)]]", "[[deg(68)]]", "[[deg(70)]]", "[[deg(72)]]"],
    derived_answer="④",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 BC 위, 선분 AD, ∠B = 46°, ∠C = 62°, D에 각 표시"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "삼각형 도형",
    note="∠A = 72 → ∠CAD = 48 → ∠ADC = 70° → ④. 빠른정답 24와 불일치.")

# ---------------- p22
add(id="59b2bb9e", qtype="choice",
    question="다음 그림에서 [[angle(x)]]와 [[angle(y)]]의 크기는?",
    choices=["[[angle(x) = deg(20)]], [[angle(y) = deg(115)]]", "[[angle(x) = deg(25)]], [[angle(y) = deg(110)]]",
             "[[angle(x) = deg(25)]], [[angle(y) = deg(105)]]", "[[angle(x) = deg(30)]], [[angle(y) = deg(105)]]",
             "[[angle(x) = deg(30)]], [[angle(y) = deg(100)]]"],
    derived_answer="③",
    figure=U("직각삼각형 ABE(B에 직각, A 위, E 오른쪽), D는 AB 위, C는 BE 위, 선분 AC와 DE의 교점 F; ∠BAC = 50°, ∠DEB = 15°, ∠ADF = y, ∠AFD = x"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·교차 선분 도형(50°, 15°는 그림에만)",
    note="∠BDE = 75 → y = 105, x = 180 − 50 − 105 = 25° → ③. 빠른정답 2와 불일치.")

# ---------------- p24
add(id="a92df3f5", qtype="short",
    question=("다음 그림에서 [[par(line(AB), line(CD))]]이고, [[angle(ABC) = deg(40)]], [[angle(ADC) = deg(65)]]일 때, "
              "[[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(245)",
    figure=U("세로 평행선 2개: 왼쪽 직선 위에 A(위)·B(아래), 오른쪽 직선 위에 C(위)·D(아래), 선분 AD와 BC가 교차; "
             "∠ABC = 40°(B), ∠ADC = 65°(D), 교점의 위쪽 각(AD와 BC 사이) x, C에서 CB와 위쪽 직선 사이의 각 y"),
    difficulty_est=2, confidence=0.75, needs_review=FIG + "평행선·교차 선분 도형(x, y 위치는 그림에만)",
    note="∠BAD = 65(엇각) → 교점 아래각 75, x = 105; ∠BCD = 40(엇각) → y = 140 → 245°(그림의 x·y 위치 판독 기준). 빠른정답 55와 불일치.")

# ---------------- p25
add(id="65a9461b", qtype="choice",
    question="다음 그림에서 [[angle(DCB) = angle(ACD)]]일 때, [[angle(x)]]의 크기는?",
    choices=["[[deg(60)]]", "[[deg(65)]]", "[[deg(70)]]", "[[deg(75)]]", "[[deg(80)]]"],
    derived_answer="④",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 AB 위, 선분 CD(∠C 이등분, 점 표시), ∠B = 60°, A의 외각 ∠CAE = 150°(E는 BA의 연장선 위), ∠BDC = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "삼각형·외각 도형(60°, 150°는 그림에만)",
    note="∠A = 30, ∠C = 90 → ∠DCB = 45 → x = 75° → ④. 빠른정답 3과 불일치.")

# ---------------- p26
add(id="242b34da", qtype="choice",
    question="다음 그림에서 선분 AD가 [[angle(A)]]의 이등분선일 때, [[angle(x)]]의 크기와 [[angle(DAC)]]의 크기의 차는?",
    choices=["[[deg(10)]]", "[[deg(20)]]", "[[deg(30)]]", "[[deg(40)]]", "[[deg(50)]]"],
    derived_answer="④",
    figure=U("삼각형 ABC(A 왼쪽 아래, B 위, C 오른쪽 아래), D는 BC 위, AD가 ∠A 이등분(점 표시), ∠B = 60°, C의 외각 140°, ∠ADB = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "삼각형·외각 도형(60°, 140°는 그림에만)",
    note="∠C = 40, ∠A = 80 → ∠DAC = 40, x = 80 → 차 40° → ④. 빠른정답 50과 불일치.")

# ---------------- p37
add(id="6efbd37f", qtype="short",
    question="다음 그림과 같은 [[tri(ABC)]]에 대하여 [[angle(DCB) + angle(DBC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(65)",
    figure=U("삼각형 ABC(A 오른쪽 위, B 왼쪽, C 오른쪽 아래), 내부 점 D, 선분 BD·CD, ∠BDC = 115°"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "삼각형 내부 점 도형(115°는 그림에만)",
    note="180 − 115 = 65°. 빠른정답 87.5와 불일치.")

# ---------------- p38
add(id="6f01f9b7", qtype="short",
    question="다음 그림과 같은 [[tri(ABC)]]에 대하여 [[angle(DAB) + angle(DBA)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(55)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 내부 점 D, 선분 AD·BD, ∠ADB = 125°"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "삼각형 내부 점 도형(125°는 그림에만)",
    note="180 − 125 = 55°. 빠른정답 100과 불일치.")

# ---------------- p40
add(id="6c0c7289", qtype="short",
    question=("다음 그림의 [[tri(ABC)]]에서 [[seg(IB)]]와 [[seg(IC)]]는 각각 [[angle(B)]]와 [[angle(C)]]의 이등분선이고 "
              "[[angle(BIC) = deg(115)]]일 때, [[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(50)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 내부 점 I, 선분 IB·IC(각 이등분 표시), ∠BIC = 115°, ∠A = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "삼각형 내각 이등분선 도형",
    note="90 + x/2 = 115 → x = 50°. 빠른정답 65와 불일치.")

# ---------------- p41
add(id="0ee9e26d", qtype="choice",
    question=("다음 그림의 [[tri(ABC)]]에서 점 D는 [[angle(B)]]와 [[angle(C)]]의 이등분선의 교점이다. [[angle(A) = deg(82)]]일 때, "
              "[[angle(x)]]의 크기는?"),
    choices=["[[deg(120)]]", "[[deg(125)]]", "[[deg(127)]]", "[[deg(129)]]", "[[deg(131)]]"],
    derived_answer="⑤",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 내부 점 D, 선분 BD·CD(각 이등분 표시), ∠A = 82°, ∠BDC = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "삼각형 내각 이등분선 도형",
    note="x = 90 + 41 = 131° → ⑤. 빠른정답 55와 불일치.")

# ---------------- p46
add(id="07d7bff7", qtype="short",
    question="다음 그림의 [[tri(ABC)]]에 대하여 [[angle(BIC) + angle(BPC) + angle(BQC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(215)",
    figure=U("삼각형 ABC(A 위, B 왼콍 아래, C 오른쪽 아래), ∠A = 70°; I는 ∠B·∠C의 내각 이등분선(•, ○ 표시)의 교점, "
             "P(아래)는 ∠B·∠C의 외각 이등분선(△, × 표시)의 교점, Q(오른쪽 위)는 ∠B의 내각 이등분선의 연장(B–I–Q)과 ∠C의 외각 이등분선(P–C–Q)의 교점"),
    difficulty_est=3, confidence=0.75, needs_review=FIG + "내각·외각 이등분선 복합 도형(70°·각 표시는 그림에만)",
    note="∠BIC = 125, ∠BPC = 55, ∠BQC = 35 → 215°(그림 구성 판독 기준). 빠른정답 35와 불일치.")

# ---------------- p48
add(id="811d702b", qtype="choice",
    question=("다음 그림의 사각형 ABCD에서 [[seg(BA)]], [[seg(CD)]]의 연장선의 교점을 E, [[seg(BC)]]와 [[seg(AD)]]의 연장선의 교점을 F, "
              "[[angle(E)]], [[angle(F)]]의 이등분선의 교점을 P라 할 때, [[angle(EPF)]]의 크기는?"),
    choices=["[[deg(84)]]", "[[deg(86)]]", "[[deg(88)]]", "[[deg(92)]]", "[[deg(94)]]"],
    derived_answer="④",
    figure=U("큰 삼각형 EBF(E 위, B 왼쪽 아래, F 오른쪽 아래) 안의 사각형 ABCD: A는 EB 위, C는 BF 위, D는 EC와 AF의 교점; "
             "∠BAD = 92°, ∠BCD = 84°, ∠E·∠F의 이등분선(•, × 표시)이 P에서 만남, G는 FP와 EC의 교점"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "사각형·연장선·이등분선 복합 도형(92°, 84°는 그림에만)",
    note="∠EPF = (∠B + ∠D)/2 = (360 − 92 − 84)/2 = 92°(좌표 수치 검산) → ④. 빠른정답 102와 불일치.")

# ---------------- p57
add(id="3b2f4510", qtype="short",
    question=("다음 그림과 같이 [[tri(ABC)]]에서 [[angle(B)]]와 [[angle(C)]]의 외각의 이등분선의 교점을 D라 할 때, "
              "[[angle(BDC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=U("삼각형 ABC(A 왼쪽 아래, B 위, C 오른쪽 아래), ∠A = 60°, E는 AB의 연장선 위, F는 AC의 연장선 위, ∠EBC·∠BCF의 이등분선(○, × 표시)이 D에서 만남"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "삼각형 외각 이등분선 도형(60°는 그림에만)",
    note="∠BDC = 90 − 30 = 60°. 빠른정답 5와 불일치.")

# ---------------- p58
add(id="091ddfc5", qtype="short",
    question=("다음 그림과 같이 [[angle(CBE)]]를 이등분한 직선과 [[angle(BCF)]]를 이등분한 직선의 교점을 D라 할 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(52)",
    figure=U("삼각형 ABC(A 오른쪽 아래, B 오른쪽 위, C 왼쪽 아래), ∠A = 76°, E는 AB의 연장선 위(B 위쪽), F는 AC의 연장선 위(C 왼쪽), "
             "외각 이등분선(•, ○ 표시)의 교점 D(왼쪽 위), ∠BDC = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "삼각형 외각 이등분선 도형(76°는 그림에만)",
    note="x = 90 − 38 = 52°. 빠른정답 3과 불일치.")

# ---------------- p60
add(id="d1a62500", qtype="short",
    question=("다음 그림과 같은 삼각형 ABC에서 [[2 angle(ECF) = angle(FCB)]], [[2 angle(FBD) = angle(FBC)]]이고 [[angle(F) = deg(50)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(15)",
    figure=U("삼각형 ABC(A 왼쪽, B 아래, C 오른쪽 위), E는 AC의 연장선 위(C 너머), D는 AB의 연장선 위(B 너머), 점 F(오른쪽)에 선분 CF·BF, ∠BFC = 50°, ∠A = x"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "삼각형 외각 삼등분선 도형",
    note="외각 3p, 3q; 2p + 2q = 130 → 3p + 3q = 195 = 180 + x → x = 15°. 빠른정답 60과 불일치.")

# ---------------- p63
add(id="113bbb8b", qtype="short",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[angle(A)]]의 외각의 이등분선과 [[angle(B)]]의 외각의 이등분선의 교점을 I라 하고 "
              "[[angle(AIB) = deg(60)]]일 때, [[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=U("삼각형 ABC(A 위, B 아래, C 오른쪽), D는 CA의 연장선 위, E는 CB의 연장선 위, ∠DAB·∠ABE의 이등분선(×, • 표시)이 왼쪽 점 I에서 만남, ∠AIB = 60°, ∠C = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "삼각형 외각 이등분선 도형",
    note="90 − x/2 = 60 → x = 60°. 빠른정답 15와 불일치.")

# ---------------- p64
add(id="b62dbe5e", qtype="short",
    question=("다음 그림의 두 삼각형 ABC와 DBC에서 [[angle(ABD) = angle(DBC)]], [[angle(ICA) = angle(ICB)]], [[angle(ACD) = angle(DCE)]]이고 "
              "[[angle(BIC) = deg(132)]]일 때, [[angle(x) - angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(42)",
    figure=U("B(왼쪽 아래), C(오른쪽 아래), E는 BC의 연장선 위, A(위), D(오른쪽 위); BD가 ∠B 이등분(• 표시), I는 BD와 CI의 교점(CI는 ∠ACB 이등분, × 표시), "
             "CD는 ∠ACE 이등분(△ 표시), ∠BIC = 132°, ∠BAC = x, ∠BDC = y"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "내각·외각 이등분선 복합 도형",
    note="x = 2(132 − 90) = 84, y = x/2 = 42 → 42°. 빠른정답 20과 불일치.")

# ---------------- p67
add(id="b3d2b01f", qtype="choice",
    question=("다음 그림의 [[tri(ABC)]]에서 [[angle(B)]]의 이등분선과 [[angle(C)]]의 외각의 이등분선의 교점을 P라 하자. "
              "[[angle(BAC) = deg(68)]]일 때, [[angle(x)]]의 크기는?"),
    choices=["[[deg(28)]]", "[[deg(33)]]", "[[deg(34)]]", "[[deg(38)]]", "[[deg(44)]]"],
    derived_answer="③",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 아래), D는 BC의 연장선 위, P는 오른쪽 위; BP가 ∠B 이등분(○ 표시), CP가 ∠ACD 이등분(• 표시), ∠BAC = 68°, ∠BPC = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "내각·외각 이등분선 도형",
    note="x = 68/2 = 34° → ③. 빠른정답 42와 불일치.")

# ---------------- p72
add(id="096ff0a9", qtype="short",
    question=("다음 그림에서 [[angle(ABD) = angle(DBE) = angle(EBC)]], [[angle(ACD) = angle(DCE) = angle(ECP)]]이고 [[angle(BDC) = deg(48)]]일 때, "
              "[[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(96)",
    figure=U("B(왼쪽 아래), C(아래), P는 BC의 연장선 위, A(위), D(A의 오른쪽 위), E(오른쪽); BD·BE가 ∠ABC 삼등분(• 표시), CD·CE가 외각 ∠ACP 삼등분(× 표시), "
             "∠BDC = 48°, ∠BAC = x, ∠BEC = y"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "내각·외각 삼등분선 도형",
    note="c − b = 24 → x = 3(c − b) = 72, y = c − b = 24 → 96° = 빠른정답 ✓.")

# ---------------- p74
add(id="5848cb54", qtype="short",
    question=("다음 그림에서 [[angle(ABD) = angle(DBE) = angle(EBC)]], [[angle(ACD) = angle(DCE) = angle(ECP)]]이고 [[angle(BDC) = deg(40)]]일 때, "
              "[[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(80)",
    figure=U("B(왼쪽 아래), C(아래), P는 BC의 연장선 위, A(왼쪽 위), D(위), E(오른쪽 위); BD·BE가 ∠ABC 삼등분(• 표시), CD·CE가 외각 ∠ACP 삼등분(× 표시), "
             "∠BDC = 40°, ∠BAC = x, ∠BEC = y"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "내각·외각 삼등분선 도형",
    note="c − b = 20 → x = 60, y = 20 → 80°. 빠른정답 3과 불일치.")

# ---------------- p78
add(id="bd013c76", qtype="short",
    question="다음 그림에서 [[seg(AB) = seg(AC) = seg(CD)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(100)",
    figure=U("B, C, D가 한 직선 위(왼쪽부터), A는 위; AB = AC = CD(두 줄 표시), D의 외각 160°, ∠BAC = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "이등변삼각형 연결 도형(160°는 그림에만)",
    note="∠ADC = 20 = ∠CAD → ∠ACB = 40 = ∠ABC → x = 100°. 빠른정답 4와 불일치.")

# ---------------- p79
add(id="88252aad", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AB) = seg(AC)]], [[seg(BC) = seg(BD)]]이고 [[angle(A) = deg(52)]]일 때, "
              "[[angle(x)]]의 크기는?"),
    choices=["[[deg(10)]]", "[[deg(11)]]", "[[deg(12)]]", "[[deg(13)]]", "[[deg(14)]]"],
    derived_answer="③",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 AC 위, 선분 BD; AB = AC(두 줄), BC = BD(한 줄), ∠A = 52°, ∠ABD = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "이등변삼각형 도형",
    note="∠B = ∠C = 64, ∠BDC = 64 → ∠DBC = 52 → x = 12° → ③ = 빠른정답 ✓.")

# ---------------- p82
add(id="a92c96a6", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AB) = seg(AC) = seg(BD)]]이다. [[angle(ABE) = angle(x)]]라 할 때, "
              "[[angle(DAC)]]의 크기를 [[angle(x)]]를 사용하여 나타내면?"),
    choices=["[[deg(180) - 2 angle(x)]]", "[[deg(90) - frac(3,2) angle(x)]]", "[[2 angle(x) - deg(90)]]",
             "[[2 angle(x) - deg(180)]]", "[[frac(3,2) angle(x) - deg(180)]]"],
    derived_answer="⑤",
    figure=U("삼각형 ABC(C 왼쪽 아래, A 오른쪽 아래, B 오른쪽 위), D는 BC 위, E는 CB의 연장선 위(B 너머), 선분 AD; AB = AC = BD 표시, B의 외각 ∠ABE = x"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "이등변삼각형·외각 도형",
    note="∠ABC = ∠C = 180 − x, ∠BAC = 2x − 180, ∠BAD = x/2 → ∠DAC = (3/2)x − 180 → ⑤. 빠른정답 3과 불일치.")

# ---------------- p84
add(id="48966dce", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[angle(C)]]의 외각의 크기가 [[deg(140)]]일 때, "
              "[[angle(x)]]의 크기는?"),
    choices=["[[deg(65)]]", "[[deg(70)]]", "[[deg(75)]]", "[[deg(80)]]", "[[deg(85)]]"],
    derived_answer="④",
    figure=U("이등변삼각형 ABC(B 왼쪽 아래, C 오른쪽 아래, A 위), BA의 연장선이 A 너머로 뻗음, A의 외각 x, C의 외각 140°, AB = AC 표시"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "이등변삼각형·외각 도형",
    note="∠B = ∠C = 40 → x = 80° → ④ = 빠른정답 ✓.")

# ---------------- p87
add(id="06064ba6", qtype="short",
    question="다음 그림에서 [[seg(AB) = seg(AC) = seg(CD)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=U("B, C, D가 한 직선 위(왼쪽부터), A는 위; AB = AC = CD(두 줄 표시), D의 외각 150°, ∠BAC = x"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "이등변삼각형 연결 도형(150°는 그림에만)",
    note="∠ADC = 30 = ∠CAD → ∠ACB = 60 = ∠ABC → x = 60°. 빠른정답 4와 불일치.")

# ---------------- p89
add(id="f0506283", qtype="short",
    question="다음 그림에서 [[angle(AJF)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(75)",
    figure=U("별 모양: 꼭짓점 A(위), B(왼쪽), E(오른쪽), C(왼쪽 아래), D(오른쪽 아래); 교점 F(AC∩BE), G(AC∩BD), H(BD∩CE), I(CE∩AD), J(AD∩BE); "
             "∠B = 20°, ∠E = 30°, ∠C = 40°, ∠D = 55°"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "별 모양 도형(각 4개는 그림에만)",
    note="∠A = 35, △FCE에서 ∠CFE = 110 → ∠AFJ = 70 → ∠AJF = 75°. 빠른정답 108과 불일치.")

# ---------------- 원과 부채꼴 p22
add(id="2b55c194", qtype="choice",
    question="다음 그림의 원 O에서 [[arc(AB) = 6]] cm, [[arc(CD) = 14]] cm일 때, [[x]]의 값은?",
    choices=["32", "33", "34", "35", "36"],
    derived_answer="⑤",
    figure=U("원 O, 호 AB(왼쪽 위, 6 cm)와 호 CD(오른쪽, 14 cm), ∠AOB = x°, ∠COD = 3x°−24°"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "원·중심각 도형(x°, 3x°−24°는 그림에만)",
    note="6 : 14 = x : (3x − 24) → x = 36 → ⑤. 빠른정답 2와 불일치.")

# ---------------- p24
add(id="b79ebc0a", qtype="choice",
    question=("다음 그림의 원 O에서 [[seg(AC)]]는 지름이고 [[arc(AB) = 21]] cm, [[angle(AOB) = deg(140)]]일 때, "
              "[[arc(BC)]]의 길이는?"),
    choices=["5 cm", "5.5 cm", "6 cm", "6.5 cm", "7 cm"],
    derived_answer="③",
    figure=U("원 O, 지름 AC(A 왼쪽 위, C 오른쪽 아래), B는 오른쪽 아래 원 위, 호 AB = 21 cm(위쪽 큰 호), ∠AOB = 140°"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "원·지름·중심각 도형",
    note="∠BOC = 40 → 21 × 40/140 = 6 cm → ③ = 빠른정답 ✓.")

# ---------------- p25
add(id="f3716552", qtype="choice",
    question="다음 그림과 같이 [[seg(AB)]]가 지름인 원 O에서 [[angle(BAC) = deg(30)]]일 때, [[ratio(arc(AC), arc(BC))]]는?",
    choices=["[[ratio(5, 3)]]", "[[ratio(2, 1)]]", "[[ratio(7, 3)]]", "[[ratio(8, 5)]]", "[[ratio(9, 5)]]"],
    derived_answer="②",
    figure=U("원 O, 지름 AB(가로), C는 오른쪽 위 원 위, 선분 AC, ∠BAC = 30°"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "원·지름 도형",
    note="∠BOC = 60, ∠AOC = 120 → 2 : 1 → ②. 빠른정답 5와 불일치.")

# ---------------- p27
add(id="fd519532", qtype="short",
    question="다음 그림의 원 O에서 [[ratio(arc(AB), arc(BC), arc(CA)) = ratio(2, 4, 3)]]일 때, [[angle(COA)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(120)",
    figure=U("원 O, 원 위의 점 A(위), B(왼쪽), C(오른쪽 아래), 반지름 OA·OB·OC, ∠COA 표시"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "원·중심각 도형",
    note="360 × 3/9 = 120°. 빠른정답 3과 불일치.")

# ---------------- p31
add(id="452cca7e", qtype="short",
    question=("다음 그림과 같은 원 O에서 [[seg(AC)]]는 원 O의 지름이고 [[ratio(arc(AB), arc(BC), arc(DE)) = ratio(7, 5, 4)]]일 때, "
              "[[angle(DOE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=U("원 O, 지름 AC(가로), B는 아래쪽 원 위, D(오른쪽 위)·E(왼쪽 위)는 위쪽 원 위, 반지름 OB·OD·OE, ∠DOE 표시"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "원·지름·중심각 도형",
    note="호 AB + 호 BC = 반원 → 12 : 180 → 1 = 15° → ∠DOE = 60°. 빠른정답 없음.")

# ---------------- p40
add(id="c9420db2", qtype="short",
    question=("다음 그림의 원 O에서 [[par(seg(AB), seg(CD))]], [[angle(AOB) = deg(132)]]이고 원 O의 둘레의 길이가 45 cm일 때, "
              "[[arc(BD)]]의 길이를 구하시오."),
    choices=None, derived_answer="3 cm",
    figure=U("원 O, 지름 CD(가로), 현 AB(위쪽, CD와 평행, 화살표 표시), 반지름 OA·OB, ∠AOB = 132°"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "원·평행 현 도형",
    note="∠OBA = 24 = ∠BOD(엇각) → 45 × 24/360 = 3 cm. 빠른정답 2와 불일치.")
