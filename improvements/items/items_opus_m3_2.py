# -*- coding: utf-8 -*-
# esc_opus_m3-2_1of1 — 이미지 기준 전사 (11 항목 / 11쪽). 전부 정보성 기하 도형 → unsupported + needs_review
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ---------------- 예각의 삼각비의 값 p3 (사분원)
add(id="c6e42dba", qtype="choice",
    question=("아래 그림과 같이 정사각형 ABCD 안에 점 B를 중심으로 하고 [[seg(AB)]]를 반지름으로 하는 사분원을 그리고 "
              "[[seg(BR)]]와 [[arc(AC)]]의 교점을 P, 점 P에서 변 BC에 내린 수선의 발을 Q라 하자. "
              "[[angle(PBQ) = angle(x)]]라 할 때, 다음 중 [[frac(seg(PR), seg(QC))]]의 값과 같은 것은?"),
    choices=["[[sin(x)]]", "[[cos(x)]]", "[[tan(x)]]", "[[frac(1, sin(x))]]", "[[frac(1, cos(x))]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). B 중심·반지름 AB인 사분원(호 AC). R은 변 CD 위, 선분 BR과 호 AC의 교점 P, P에서 BC에 내린 수선의 발 Q. ∠PBQ=x(B에 표시), 직각 표시 B·Q·C"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형+사분원+수선 복합 도형",
    note="BP=BC=1이라 하면 BR=1/cos x, PR=1/cos x−1, QC=1−cos x → PR/QC=1/cos x → ⑤ = 빠른정답 ✓.")

# ---------------- p4 (직사각형 AB=2)
add(id="f533eed1", qtype="choice",
    question=("아래 그림과 같이 [[seg(AB) = 2]]인 직사각형 ABCD에서 점 B를 중심으로 하고 [[seg(AB)]]를 반지름으로 하는 사분원 ABH를 그렸다. "
              "[[angle(BGH) = angle(x)]]라 할 때, 다음 중 [[frac(tan(x) - sin(x), sin(x))]]의 값을 나타내는 것은?"),
    choices=["[[frac(1,2) seg(AD)]]", "[[frac(1,2) seg(CF)]]", "[[frac(1,2) seg(DE)]]", "[[seg(CF)]]", "[[seg(DE)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상), AB=2(좌측 점선 치수). B 중심·반지름 AB인 사분원 ABH(H는 변 BC 위). 대각선 BD, BD와 호의 교점 E, E에서 BC에 내린 수선의 발 F, H에서 BC에 수직인 선분과 BD의 교점 G. ∠BGH=x(G에 표시), 직각 표시 F·H·C"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형+사분원+대각선 복합 도형",
    note="∠BGH=x ⇒ BC=2tan x, BF=2sin x, BD=2/cos x. (tan x−sin x)/sin x = 1/cos x − 1 = (BD−2)/2 = ½DE → ③. 빠른정답 1(½AD=tan x)과 불일치.")

# ---------------- p5 (직사각형 AB=1)
add(id="2b89b8f4", qtype="choice",
    question=("아래 그림과 같이 [[seg(AB) = 1]]인 직사각형 ABCD에서 점 B를 중심으로 하고 [[seg(AB)]]를 반지름으로 하는 사분원 ABH를 그렸다. "
              "[[angle(BGH) = angle(x)]]라 할 때, 다음 중 [[tan(x) - sin(x)]]의 값을 나타내는 것은?"),
    choices=["[[frac(1,2) seg(AD)]]", "[[frac(1,2) seg(CF)]]", "[[frac(1,2) seg(DE)]]", "[[seg(CF)]]", "[[seg(DE)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상), AB=1(좌측 점선 치수). B 중심·반지름 AB인 사분원 ABH(H는 변 BC 위). 대각선 BD, BD와 호의 교점 E, E에서 BC에 내린 수선의 발 F, H에서 BC에 수직인 선분과 BD의 교점 G. ∠BGH=x(G에 표시), 직각 표시 F·H·C"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형+사분원+대각선 복합 도형",
    note="∠BGH=x ⇒ AD=BC=tan x, BF=sin x → tan x−sin x = BC−BF = CF → ④. 빠른정답 '4, 5'(복수 표기)와 형식 불일치.")

# ---------------- 삼각비의 표 p94~p96 (같은 문항, 수치·표만 다름)
_TAB_Q = ("다음 그림과 같이 제1사분면에 점 O를 중심으로 반지름의 길이가 1인 사분원이 있다. "
          "[[perp(seg(OC), seg(BC))]], [[perp(seg(OE), seg(DE))]], [[angle(BOC) = angle(x)]]일 때, "
          "주어진 삼각비표를 이용하여 삼각형 BED의 넓이를 구하시오.")
def _tab_fig(yval, rows):
    return [{"fn": "unsupported", "args": {"raw": f"좌표평면 제1사분면. 원점 O 중심·반지름 1인 사분원(A(0,1)~E(1,0)). 호 위의 점 B(y좌표 {yval}, y축에서 점선), B에서 x축에 내린 수선의 발 C, E에서 x축에 수직인 직선과 반직선 OB의 교점 D. ∠BOC=x, 삼각형 BED 색칠, 직각 표시 C·E"}},
            {"fn": "table", "args": {"head": ["각도", "sin", "cos", "tan"],
                                     "rows": [[f"[[deg({d})]]", f"[[{s}]]", f"[[{c}]]", f"[[{t}]]"] for d, s, c, t in rows]}}]
_ROWS_A = [(41, "0.6561", "0.7547", "0.8693"), (43, "0.6820", "0.7314", "0.9325"), (45, "0.7071", "0.7071", "1.0000"),
           (47, "0.7314", "0.6820", "1.0724"), (49, "0.7547", "0.6561", "1.1504")]
_ROWS_B = [(43, "0.6820", "0.7314", "0.9325"), (44, "0.6947", "0.7193", "0.9657"), (45, "0.7071", "0.7071", "1.0000"),
           (46, "0.7193", "0.6947", "1.0355"), (47, "0.7314", "0.6820", "1.0724")]

add(id="853a4ff0", qtype="short", question=_TAB_Q, choices=None, derived_answer="0.12523475",
    figure=_tab_fig("0.6820", _ROWS_A), difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원+삼각형 색칠 도형(표는 table로 기재)",
    note="sin x=0.6820 → x=43°. 넓이=½·DE·CE=½·tan43°·(1−cos43°)=½×0.9325×0.2686=0.12523475. 빠른정답 1322와 불일치.")

add(id="7f390ca1", qtype="short", question=_TAB_Q, choices=None, derived_answer="0.158069075",
    figure=_tab_fig("0.7193", _ROWS_B), difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원+삼각형 색칠 도형(표는 table로 기재)",
    note="sin x=0.7193 → x=46°. 넓이=½·tan46°·(1−cos46°)=½×1.0355×0.3053=0.158069075. 빠른정답 7.193과 불일치.")

add(id="ac7a8123", qtype="short", question=_TAB_Q, choices=None, derived_answer="0.135535995",
    figure=_tab_fig("0.6947", _ROWS_B), difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원+삼각형 색칠 도형(표는 table로 기재)",
    note="sin x=0.6947 → x=44°. 넓이=½·tan44°·(1−cos44°)=½×0.9657×0.2807=0.135535995. 빠른정답 1과 불일치.")

# ---------------- 삼각비 p53, p54 (직각삼각형의 닮음과 삼각비)
def _sq_q(ad, cd):
    return (f"다음 그림과 같이 [[angle(B) = angle(D) = deg(90)]], [[seg(AD) = {ad}]], [[seg(CD) = {cd}]]인 사각형 ABCD의 꼭짓점 D에서 "
            "변 BC에 내린 수선의 발을 H라 하자. [[seg(AC)]]는 [[angle(C)]]의 이등분선이고 [[seg(AC)]], [[seg(DH)]]의 교점을 E라 하고 "
            "[[angle(CDH) = angle(x)]]일 때, [[sin(x)]]의 값을 구하시오.")
def _sq_fig(ad, cd):
    return [{"fn": "unsupported", "args": {"raw": f"사각형 ABCD(B 좌하, C 우하, A 좌상, D 상단 꼭짓점), ∠B=∠D=90°, AD={ad}·CD={cd}(점선 치수). D에서 BC에 내린 수선 DH, 대각선 AC와 DH의 교점 E, ∠CDH=x(D에 표시), C에서 ∠ACB=∠ACD 등각 점 표시, 직각 표시 B·D·H"}}]

add(id="d0ef2a3a", qtype="short", question=_sq_q(4, 8), choices=None, derived_answer="frac(3,5)",
    figure=_sq_fig(4, 8), difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+수선+각의 이등분선 복합 도형",
    note="θ=∠ACD, tanθ=4/8=1/2, ∠DCH=2θ, x=90°−2θ → sin x=cos2θ=(1−1/4)/(1+1/4)=3/5 = 빠른정답 ✓.")

add(id="4a4ac723", qtype="short", question=_sq_q(2, 6), choices=None, derived_answer="frac(4,5)",
    figure=_sq_fig(2, 6), difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+수선+각의 이등분선 복합 도형",
    note="tanθ=2/6=1/3, x=90°−2θ → sin x=cos2θ=(1−1/9)/(1+1/9)=4/5 = 빠른정답 ✓.")

# ---------------- 원의 접선(2) p52 (원에 외접하는 사각형, 한 내각 90°)
add(id="12ea4218", qtype="choice",
    question=("다음 그림과 같이 원 O에 외접하는 사각형 ABCD에 대하여 [[seg(BC) = 30]], [[seg(AD) = 10]], [[seg(OA) = 4 sqrt(5)]], "
              "[[seg(OD) = 10]], [[angle(BCD) = deg(90)]]일 때, 색칠한 부분의 넓이는?"),
    choices=["[[300 - 36 pi]]", "[[300 - 64 pi]]", "[[320 - 36 pi]]", "[[320 - 64 pi]]", "[[320 - 81 pi]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 외접하는 사각형 ABCD(B 좌하, C 우하·직각 표시, D 우상, A 상단). 치수 AD=10(점선 호), OA=4√5, OD=10(점선 호), BC=30(점선 호). 사각형 내부에서 원을 제외한 부분 색칠"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원에 외접하는 사각형+색칠 영역 복합 도형",
    note="반지름 r=8(√(80−r²)+√(100−r²)=10 → 4+6). CD=8+6=14, AB=22+4=26, 넓이=r·s=8·40=320 → 320−64π → ④ = 빠른정답 ✓.")

# ---------------- 원에 내접하는 사각형 p38
add(id="d3d82be9", qtype="short",
    question=("다음 그림과 같이 원 O는 [[seg(AB) = seg(AC) = 5]], [[seg(BC) = 6]]인 이등변삼각형 ABC의 외접원이다. "
              "[[arc(AC)]] 위의 점 P에 대하여 [[seg(AP)]]와 [[seg(BC)]]의 연장선의 교점을 Q라 하면 "
              "[[ratio(seg(AP), seg(PQ)) = ratio(1, 2)]]이고 [[seg(BQ) = a + sqrt(b)]]일 때, [[a + b]]의 값을 구하시오. "
              "(단, [[a]], [[b]]는 유리수이다.)"),
    choices=None, derived_answer="62",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(중심 점 표시)와 내접 이등변삼각형 ABC(A 상단, B 좌, C 우; AB=AC=5 등변 표시·점선 치수, BC=6 점선 치수). 호 AC 위의 점 P(우상), 직선 AP와 직선 BC의 연장선의 교점 Q(C 오른쪽 원 밖)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접삼각형+연장선 복합 도형",
    note="QC=c, AP=t: 방멱 c(c+6)=2t·3t, △QAC 코사인법칙(cos∠ACQ=−3/5) 9t²=c²+6c+25 → t²=25/3, c=−3+√59, BQ=3+√59 → a+b=62. 빠른정답 1과 불일치.")

# ---------------- 원주각 p42 (반원)
add(id="a4d4974a", qtype="choice",
    question=("아래 그림과 같이 정사각형 ABCD의 외접원의 호 AD 위에 한 점 P를 잡고 선분 PD의 연장선 위에 [[seg(PB) = seg(PE)]]가 되도록 하는 점을 E라 하자. "
              "호 CD와 선분 BE의 교점을 F라 할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[angle(BPD) = deg(90)]]\n"
              "ㄴ. [[angle(PBA) = angle(DBF)]]\n"
              "ㄷ. [[seg(BF) = seg(CP)]]"),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상)와 그 외접원. 호 AD 위의 점 P(상단), 선분 PD의 연장선 위의 점 E(원 밖 우측), 선분 BE와 호 CD의 교점 F. 선분 AP·PB·PC·PD·DE·BD·BE 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형+외접원+보조선 복합 도형",
    note="ㄱ BD가 지름 ✓, ㄴ △PBE 직각이등변 ⇒ ∠PBE=45°=∠ABD ⇒ ∠PBA=∠DBF ✓, ㄷ 호AP=호DF ⇒ 호BCF=호CDP ⇒ BF=CP ✓ → ⑤ (빠른정답 없음, 수치 검산).")
