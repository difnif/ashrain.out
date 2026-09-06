# -*- coding: utf-8 -*-
# esc_sonnet_m2-2_4of5 — 이미지 기준 전사 (81 항목 / 80쪽) — 중2-2 삼각형의 외심과 내심 · 평행사변형
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
FIG = "도형 표현 불가: "
DEG5 = lambda *v: ["[[deg(%d)]]" % x for x in v]
TRI_ABC = "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)"
PAR = "평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)"

# ══════════════ 삼각형의 외심과 내심 ══════════════
# ── p18 직각삼각형의 외심(1)
add(id="107f0c62", qtype="short",
    question=("다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에서 점 M은 [[seg(AC)]]의 중점이고 [[perp(seg(AC), seg(BD))]]이다. "
              "[[seg(AD) = 10]] cm, [[seg(CD) = 22]] cm일 때, [[seg(BM)]]의 길이를 구하시오."),
    choices=None, derived_answer="16 cm",
    figure=U("직각삼각형 ABC(A 왼쪽 위, B 왼쪽 아래·직각 표시, C 오른쪽 아래), 빗변 AC의 중점 M, B에서 AC에 내린 수선의 발 D(직각 표시), 선분 BM·BD, AD=10 cm·DC=22 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·중점·수선 도형",
    note="BM=½AC=½(10+22)=16 cm. 빠른정답 9 cm과 불일치.")

# ── p20
add(id="ced28441", qtype="short",
    question=("다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에서 점 M은 빗변의 중점이다. [[angle(BMC) = deg(110)]]일 때, "
              "[[angle(A)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(55)",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래·직각 표시, C 오른쪽 아래), 빗변 AC의 중점 M(AM=MC 표시), 선분 BM, M에 110°(∠BMC) 표시, A에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·빗변 중점 도형",
    note="MA=MB, ∠AMB=70° → ∠A=(180°−70°)/2=55°. 빠른정답 6 cm과 불일치.")

# ── p21
add(id="27c91201", qtype="short",
    question=("다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC의 빗변 AC의 중점을 O라 하자. [[angle(AOB) = deg(66)]]일 때, "
              "[[angle(C)]] 의 크기를 구하시오."),
    choices=None, derived_answer="deg(33)",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래·직각 표시, C 오른쪽 아래), 빗변 AC의 중점 O(AO=OC 표시), 선분 BO, O에 66°(∠AOB) 표시, C에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·빗변 중점 도형",
    note="OB=OC, ∠BOC=114° → ∠C=33°. 빠른정답 16 cm과 불일치.")

# ── p25
add(id="4882c763", qtype="choice",
    question=("다음 그림과 같이 직사각형 ABCD의 꼭짓점 B에서 [[seg(CD)]] 위의 한 점 E를 지나는 직선을 그어 [[seg(AD)]]의 연장선과 만나는 점을 F라 하자. "
              "점 H는 [[seg(EF)]]의 중점이고 [[seg(BD) = seg(DH)]]이다. [[angle(BDC) = deg(36)]]일 때, [[angle(DEF)]]의 크기는?"),
    choices=DEG5(70, 71, 72, 73, 74), derived_answer="③",
    figure=U("세로로 긴 직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, A·C에 직각 표시), B에서 CD 위의 점 E를 지나 AD의 연장선(오른쪽)과 만나는 점 F, "
             "EF의 중점 H(EH=HF 표시), 선분 BD·DH(BD=DH 표시), D에 36°(∠BDC) 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "직사각형·연장선·중점 복합 도형",
    note="∠DEF=x: DH=HE → ∠HDE=x, BD=DH → ∠DBH=∠DHB=180°−2x, 36°+x+2(180°−2x)=180° → x=72° → ③. 빠른정답 28과 불일치.")

# ── p27 외심 응용(1)
add(id="9f29faed", qtype="short",
    question="다음 그림에서 점 O가 [[tri(ABC)]]의 외심이고 [[angle(OBC) = deg(30)]], [[angle(OCA) = deg(35)]]일 때, [[angle(OAB)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(25)",
    figure=U(TRI_ABC + ", 내부의 외심 O와 선분 OA·OB·OC, B에 30°(∠OBC), C에 35°(∠OCA), A에 각 표시(∠OAB)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심 도형",
    note="∠OAB+30°+35°=90° → 25°. 빠른정답 1과 불일치.")

# ── p28
add(id="c337728c", qtype="short",
    question="다음 그림에서 점 O는 [[tri(ABC)]]의 외심이다. [[angle(ABO) = deg(25)]], [[angle(OCB) = deg(20)]]일 때, [[angle(A)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(70)",
    figure=U(TRI_ABC + ", 내부의 외심 O와 선분 OA·OB·OC, B에 25°(∠ABO), C에 20°(∠OCB)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심 도형",
    note="∠OAC=90°−25°−20°=45°, ∠A=25°+45°=70°. 빠른정답 3과 불일치.")

# ── p30
add(id="4f0fcfe2", qtype="short",
    question="다음 그림에서 점 O는 [[tri(ABC)]]의 외심이다. [[angle(ACO) = deg(25)]], [[angle(BCO) = deg(17)]]일 때, [[angle(A) - angle(B)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(8)",
    figure=U(TRI_ABC + ", 내부의 외심 O(점), C에서 O로 향하는 화살표, C에 25°(∠ACO)·17°(∠BCO) 표시, A·B에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심 도형",
    note="∠OAB=∠OBA=48° → ∠A=73°, ∠B=65° → 8°. 빠른정답 25와 불일치.")

# ── p32
add(id="43f3b1b9", qtype="short",
    question="다음 그림에서 점 O가 [[tri(ABC)]]의 외심이다. [[angle(BAO) = deg(36)]], [[angle(OBC) = deg(28)]]일 때, [[angle(AOC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(128)",
    figure=U(TRI_ABC + ", 내부의 외심 O와 선분 OA·OB·OC, A에 36°(∠BAO), B에 28°(∠OBC), O에 각 표시(∠AOC)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심 도형",
    note="∠OAC=∠OCA=90°−36°−28°=26° → ∠AOC=128°. 빠른정답 4와 불일치.")

# ── p34 외심 응용(2) — 프라임 라벨
add(id="4ebd52cf", qtype="short",
    question=("다음 그림에서 점 O는 [[tri(ABC)]]의 외심이고 점 O′은 [[tri(AOC)]]의 외심이다. ∠O′CO = [[deg(24)]]일 때, "
              "[[angle(B)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(24)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 변 BC 위의 점 O(외심)와 선분 OA, △AOC 내부의 점 O′과 선분 O′O·O′C, C에 24°(∠O′CO) 표시, B의 각 음영"),
    difficulty_est=3, confidence=0.75,
    needs_review="프라임 점 라벨(O′) angle 표기 불가 — 텍스트 혼합 / " + FIG + "삼각형·외심 2개 도형",
    note="O′O=O′C → ∠OO′C=132°=2∠OAC → ∠OAC=66°, ∠B=90°−66°=24°(빠른정답 24와 일치).")

# ── p37
add(id="e7a72379", qtype="short",
    question=("다음 그림에서 점 O는 [[tri(ABC)]]의 외심이고 두 점 M, N은 각각 [[seg(OA)]], [[seg(BC)]]의 중점이다. [[angle(ABC) = 3 angle(OMN)]], "
              "[[angle(ACB) = 7 angle(OMN)]], [[angle(ONM) = deg(30)]]일 때, [[angle(MON)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(140)",
    figure=U("외접원 안의 삼각형 ABC(A 오른쪽 위, B 왼쪽, C 오른쪽), 외심 O(BC 위쪽 가까이), OA의 중점 M(OM=MA 표시), BC의 중점 N(BN=NC 표시), 선분 ON·MN·OB·OC"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "외접원·삼각형·중점 복합 도형",
    note="∠OMN=t: ∠A=180°−10t, ∠AON=180°−4t=150°−t → t=10°, ∠MON=140°. 빠른정답 24와 불일치.")

# ── p38
add(id="d8329bcb", qtype="short",
    question=("다음 그림에서 [[angle(C) = deg(32)]] 인 삼각형 ABC의 외심이 M이고 삼각형 ABM의 외심을 O라 할 때, [[angle(AOM)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(116)",
    figure=U("직각삼각형 ABC(A 왼쪽 위, B 왼쪽 아래·직각 표시, C 오른쪽 아래), 빗변 AC의 중점 M과 선분 BM, △ABM 내부의 점 O와 선분 OA·OM, C에 32° 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "직각삼각형·외심 2개 도형",
    note="∠A=58°, MA=MB → ∠ABM=58°, ∠AOM=2∠ABM=116°. 빠른정답 135와 불일치.")

# ── p39
add(id="a37e5c3a", qtype="choice",
    question="다음 그림에서 점 O는 [[tri(ABC)]]의 외심이고 [[angle(OAC) = deg(47)]], [[angle(OBC) = deg(18)]]이다. [[angle(x) - angle(y)]]의 값은?",
    choices=DEG5(45, 50, 55, 60, 65), derived_answer="⑤",
    figure=U(TRI_ABC + ", 내부의 외심 O와 선분 OA·OB, A에 47°(∠OAC), B에 18°(∠OBC), O에 ∠AOB = x(음영), C에 ∠ACB = y(음영)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심 도형",
    note="y=∠C=47°+18°=65°, x=∠AOB=2∠C=130° → x−y=65° → ⑤. 빠른정답 140과 불일치.")

# ── p42 내심
add(id="cea02a28", qtype="short",
    question="다음 그림에서 점 I는 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 내심이다. [[angle(A) = deg(60)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(30)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, AB=AC 표시), 내부의 내심 I와 선분 IB·IC, A에 60° 표시, B에 ∠IBC = x 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·내심 도형",
    note="∠B=60°, x=½∠B=30°. 빠른정답 5와 불일치.")

# ── p43
add(id="6192df35", qtype="short",
    question="다음 그림에서 점 I는 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 내심이다. [[angle(A) = deg(48)]]일 때, [[angle(IBC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(33)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, AB=AC 표시), 내부의 내심 I와 선분 IB·IC, A에 48° 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·내심 도형",
    note="∠B=66°, ∠IBC=33°. 빠른정답 70과 불일치.")

# ── p46
add(id="11b19cbe", qtype="choice",
    question="아래 그림에서 점 I는 [[tri(ABC)]]의 내심이다. 다음 중 옳지 않은 것을 모두 고르면? (정답 2개)",
    choices=["[[angle(IBE) = angle(ICE)]]", "[[seg(ID) = seg(IE) = seg(IF)]]", "[[angle(IBD) = angle(IBE)]]",
             "[[cong(tri(IBD), tri(IBE))]]", "[[seg(IA) = seg(IB) = seg(IC)]]"],
    derived_answer="①, ⑤",
    figure=U(TRI_ABC + ", 내심 I와 선분 IA·IB·IC, I에서 AB·BC·CA에 내린 수선의 발 D·E·F(직각 표시)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·내심·수선 도형",
    note="내심: ID=IE=IF, ∠IBD=∠IBE, △IBD≡△IBE(RHA). ①·⑤는 일반적으로 성립하지 않음 → ①, ⑤. 빠른정답 5(⑤만)와 불일치.")

# ── p50 내심 응용(1)
add(id="57c87a4a", qtype="short",
    question="다음 그림에서 점 I는 [[tri(ABC)]]의 내심일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=U(TRI_ABC + ", 내심 I와 선분 IA·IC, A에 34°(∠IAC), C에 26°(∠ICB), B에 ∠ABC = x"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·내심 도형(각 34°, 26°는 그림에만 있음)",
    note="∠A=68°, ∠C=52° → x=60°. 빠른정답 5와 불일치.")

# ── p52
add(id="288caa23", qtype="short",
    question="다음 그림에서 점 I가 [[tri(ABC)]]의 내심일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(58)",
    figure=U(TRI_ABC + ", 내심 I와 선분 IA·IB, A에 34°(∠BAI), B에 27°(∠IBC), C에 ∠ACB = x"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·내심 도형(각 34°, 27°는 그림에만 있음)",
    note="∠A=68°, ∠B=54° → x=58°. 빠른정답 45와 불일치.")

# ── p53 내심 응용(2)
add(id="4443398e", qtype="choice",
    question="다음 그림에서 점 I는 [[tri(ABC)]]의 내심이다. [[angle(A) = deg(50)]]일 때, [[angle(BIC)]]의 크기는?",
    choices=DEG5(100, 105, 110, 115, 120), derived_answer="④",
    figure=U("삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내심 I와 선분 IB·IC, A에 50° 표시, I에 각 표시(∠BIC)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "삼각형·내심 도형",
    note="∠BIC=90°+25°=115° → ④. 빠른정답 60과 불일치.")

# ── p54
add(id="9e2f166a", qtype="short",
    question="다음 그림에서 점 I 는 [[tri(ABC)]] 의 내심이다. [[angle(BIC) = deg(110)]] 일 때, [[angle(A)]] 의 크기를 구하시오.",
    choices=None, derived_answer="deg(40)",
    figure=U("삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내심 I와 선분 IB·IC, I에 110° 표시, A에 각 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "삼각형·내심 도형",
    note="∠A=2(110°−90°)=40°. 빠른정답 70과 불일치.")

# ── p55
add(id="8ab2bd44", qtype="short",
    question="다음 그림에서 점 I가 [[tri(ABC)]]의 내심일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(122)",
    figure=U(TRI_ABC + ", 내심 I와 선분 IB·IC, A에 64° 표시, I에 ∠BIC = x 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "삼각형·내심 도형(∠A=64°는 그림에만 있음)",
    note="x=90°+32°=122°. 빠른정답 58과 불일치.")

# ── p56
add(id="7b2a30f2", qtype="short",
    question="다음 그림에서 점 I는 [[tri(ABC)]]의 내심이고, [[angle(AIC) = deg(128)]], [[angle(BCI) = deg(22)]]일 때, [[angle(BAI)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(30)",
    figure=U(TRI_ABC + ", 내심 I와 선분 IA·IC, I에 128°(∠AIC), C에 22°(∠BCI), A의 각(∠BAI) 음영"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·내심 도형",
    note="∠B=2(128°−90°)=76°, ∠C=44°, ∠A=60° → ∠BAI=30°. 빠른정답 4와 불일치.")

# ── p61 내접원의 반지름
add(id="342f750c", qtype="short",
    question=("다음 그림에서 점 I는 [[angle(C) = deg(90)]]인 직각삼각형 ABC의 내심이다. [[seg(AB) = 25]] cm, [[seg(BC) = 20]] cm, [[seg(CA) = 15]] cm일 때, "
              "[[tri(IBC)]]의 넓이를 구하시오."),
    choices=None, derived_answer="50 cm²",
    figure=U("직각삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래·직각 표시), 내접원(중심 I), △IBC 음영, AB=25 cm·BC=20 cm·CA=15 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·내접원 도형",
    note="r=(20+15−25)/2=5, △IBC=½·20·5=50 cm² = 빠른정답 ✓.")

# ── p64
add(id="7c5416d6", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]이고 [[seg(AB) = 45]] cm, [[seg(BC) = 51]] cm, [[seg(CA) = 24]] cm인 직각삼각형 모양의 시계를 만들려고 한다. "
              "분침이 삼각형 밖으로 나가지 않도록 하면서 분침의 길이를 최대한 길게 만들 때, 분침의 최대 길이를 구하시오."),
    choices=None, derived_answer="9 cm",
    figure=U("직각삼각형 ABC(A 오른쪽 위·직각 표시, B 왼쪽 아래, C 오른쪽 아래) 음영, 내부에 원형 시계(중심 O, 시침·분침), AB=45 cm·BC=51 cm·CA=24 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·내접 시계 도형",
    note="내접원 반지름 (45+24−51)/2=9 cm = 빠른정답 ✓.")

# ── p65
add(id="4217eff9", qtype="short",
    question=("다음 그림에서 점 I는 [[tri(ABC)]]의 내심이다. [[seg(AB) = 5]], [[seg(BC) = 6]], [[seg(AC) = 7]]이고 [[tri(ABC)]]의 넓이가 18일 때, "
              "[[tri(ABC)]]의 내접원의 반지름의 길이를 구하시오."),
    choices=None, derived_answer="2",
    figure=U(TRI_ABC + ", 내접원(중심 I), I에서 BC에 내린 수선(직각 표시), AB=5·BC=6·AC=7 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "삼각형·내접원 도형",
    note="½r(5+6+7)=18 → r=2 = 빠른정답 ✓.")

# ── p67 내접원과 선분
add(id="cabaa4da", qtype="choice",
    question=("다음 그림에서 점 I는 [[tri(ABC)]]의 내심이고 세 점 D, E, F는 각각 내접원과 세 변 AB, BC, CA의 접점이다. "
              "[[seg(AF) = 9]] cm, [[seg(BD) = 10]] cm, [[seg(EC) = 11]] cm일 때, [[tri(ABC)]]의 둘레의 길이는?"),
    choices=["[[60]] cm", "[[65]] cm", "[[70]] cm", "[[75]] cm", "[[80]] cm"], derived_answer="①",
    figure=U(TRI_ABC + ", 내접원(중심 I)이 AB·BC·CA와 D·E·F에서 접함, AF=9 cm·BD=10 cm·EC=11 cm 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "삼각형·내접원·접점 도형",
    note="2(9+10+11)=60 cm → ① = 빠른정답 ✓.")

# ── p73
add(id="866c8711", qtype="short",
    question=("다음 그림에서 점 I는 [[tri(ABC)]]의 내심이고 점 I를 중심으로 하고 점 A와 점 B를 지나는 원이 있다. [[seg(AB) = 8]], [[seg(BC) = 15]]이고 "
              "[[seg(BC)]], [[seg(AC)]]가 이 원과 만나는 점을 각각 D, E라 할 때, [[seg(EC)]]의 길이를 구하시오."),
    choices=None, derived_answer="7",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래·원 밖), 중심 I인 원이 A·B를 지나고 BC와 D, AC와 E에서 만남, AB=8·BC=15 치수(점선 호)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·내심 중심 원 도형",
    note="I에서 각 변에 내린 수선이 현을 이등분 → BD=2(s−b), AE=2(s−a) → EC=b−(b−7)=7 = 빠른정답 ✓.")

# ── p81 외심과 내심 설명
add(id="1de1302d", qtype="short",
    question="다음 그림과 같이 [[tri(ABC)]]의 외심 O와 내심 I가 일치할 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=U(TRI_ABC + ", 내부의 점 O(I)와 선분 OB·OC, A에 ∠A = x 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "삼각형·외심=내심 도형",
    note="외심과 내심이 일치 → 정삼각형, x=60°. 빠른정답 2와 불일치.")

# ── p87 외심·내심 모두
add(id="3d22d688", qtype="choice",
    question="다음 그림에서 두 점 O, I는 각각 [[tri(ABC)]]의 외심과 내심이다. [[angle(BOC) = deg(104)]]일 때, [[angle(BIC)]]의 크기는?",
    choices=DEG5(104, 108, 112, 116, 120), derived_answer="④",
    figure=U(TRI_ABC + ", 내부의 점 O(위)·I(아래)와 선분 OB·OC·IB·IC, O에 104°(∠BOC), I에 각 표시(∠BIC)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심·내심 도형",
    note="∠A=52°, ∠BIC=90°+26°=116° → ④. 빠른정답 5와 불일치.")

# ── p88
add(id="5ec0b8f3", qtype="short",
    question="다음 그림과 같이 이등변삼각형 ABC의 외심, 내심을 각각 O, I라 하고 [[angle(OBI) = deg(x)]] 라 할 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="6",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, AB=AC 표시), A에 52° 표시, 내부의 점 O(위)·I(아래)와 선분 OB·OC·IB·IC"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형·외심·내심 도형(∠A=52°는 그림에만 있음)",
    note="∠B=64°, ∠OBC=90°−52°=38°, ∠IBC=32° → x=6. 빠른정답 2와 불일치.")

# ── p89
add(id="bc682d66", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 외심, 내심을 각각 O, I라 할 때, [[angle(IBO)]] 의 크기를 구하시오.",
    choices=None, derived_answer="deg(15)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, AB=AC 표시), A에 80° 표시, 내부의 점 I(위)·O(아래)와 선분 IB·IC·OB·OC, B에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형·외심·내심 도형(∠A=80°는 그림에만 있음)",
    note="∠B=50°, ∠IBC=25°, ∠OBC=90°−80°=10° → 15°. 빠른정답 5와 불일치.")

# ── p90
add(id="d61ea57f", qtype="short",
    question="다음 그림에서 점 O, I는 각각 [[tri(ABC)]]의 외심과 내심이다. [[angle(BIC) = deg(118)]]일 때, [[angle(OCB)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(34)",
    figure=U(TRI_ABC + ", 내부의 점 I(왼쪽)·O(오른쪽)와 선분 IB·IC·OB·OC, I에 118°(∠BIC), C에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심·내심 도형",
    note="∠A=2(118°−90°)=56°, ∠OCB=90°−56°=34°. 빠른정답 4와 불일치.")

# ── p91
add(id="f4e1a46f", qtype="short",
    question=("다음 그림에서 점 O, I는 각각 [[tri(ABC)]]의 외심과 내심이다. [[angle(IBA) = deg(32)]], [[angle(ICA) = deg(24)]]일 때, "
              "[[angle(BOC) - angle(BIC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(12)",
    figure=U(TRI_ABC + ", 내부의 점 I(위)·O(아래)와 선분 IB·IC·OB·OC, B에 32°(∠IBA), C에 24°(∠ICA)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심·내심 도형",
    note="∠A=68° → ∠BOC=136°, ∠BIC=124° → 12°. 빠른정답 6과 불일치.")

# ── p92
add(id="1827e580", qtype="choice",
    question=("다음 그림의 [[tri(ABC)]]에서 두 점 O, I는 각각 [[tri(ABC)]]의 외심과 내심이다. [[angle(B) = deg(60)]], [[angle(C) = deg(40)]]일 때, "
              "[[angle(OAI)]]의 크기는?"),
    choices=DEG5(10, 12, 14, 16, 18), derived_answer="①",
    figure=U(TRI_ABC + ", 내부의 점 I(왼쪽)·O(오른쪽)와 선분 AI·AO, A에 각 표시(∠OAI), B에 60°, C에 40°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·외심·내심 도형",
    note="∠A=80°, ∠OAC=90°−60°=30°, ∠IAC=40° → 10° → ①. 빠른정답 15와 불일치.")

# ── p93
add(id="f0441916", qtype="short",
    question=("다음 그림에서 두 점 O, I는 각각 [[tri(ABC)]]의 외심, 내심이고 점 D는 [[seg(CO)]]의 연장선과 [[seg(BI)]]의 교점이다. "
              "[[angle(A) = deg(78)]], [[angle(ACB) = deg(68)]]일 때, [[angle(BDO)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(151)",
    figure=U("삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내부의 점 I(위)·O(아래), 선분 BI, CO의 연장선이 BI와 만나는 점 D, A에 78°, C에 68°, D에 각 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·외심·내심·연장선 도형",
    note="∠B=34°, ∠DBC=17°, ∠OCB=90°−78°=12° → ∠BDO=∠BDC=180°−17°−12°=151°. 빠른정답 34와 불일치.")

# ── p94 직각삼각형의 외접원과 내접원
add(id="89d8a3d0", qtype="short",
    question=("다음 그림에서 [[tri(ABC)]]는 [[angle(C) = deg(90)]]인 직각삼각형이고, [[seg(AB) = 20]] cm, [[seg(BC) = 16]] cm, [[seg(CA) = 12]] cm이다. "
              "[[tri(ABC)]]의 내접원 I와 외접원 O의 반지름의 길이의 합을 구하시오."),
    choices=None, derived_answer="14 cm",
    figure=U("외접원(중심 O, AB의 중점) 안의 직각삼각형 ABC(A 오른쪽 위, B 왼쪽, C 오른쪽 아래·직각 표시), 내접원(중심 I), AB=20 cm·BC=16 cm·CA=12 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·외접원·내접원 도형",
    note="r=(16+12−20)/2=4, R=10 → 14 cm. 빠른정답 12와 불일치.")

# ── p95
add(id="088586ab", qtype="choice",
    question=("다음 그림은 직각삼각형 ABC의 내접원과 외접원을 각각 그린 것이다. [[seg(AB) = 10]] cm, [[seg(BC) = 8]] cm, [[seg(CA) = 6]] cm일 때, "
              "색칠한 부분의 넓이는?"),
    choices=["[[18 pi]] cm²", "[[19 pi]] cm²", "[[20 pi]] cm²", "[[21 pi]] cm²", "[[22 pi]] cm²"], derived_answer="④",
    figure=U("외접원(중심 O) 내부에서 내접원(중심 I) 바깥 부분 음영, 직각삼각형 ABC(A 오른쪽 위, B 왼쪽, C 오른쪽 아래·직각 표시), AB=10 cm·BC=8 cm·CA=6 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·외접원·내접원 음영 도형",
    note="R=5, r=2 → 25π−4π=21π → ④. 빠른정답 1과 불일치.")

# ── p97
add(id="752dad2a", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC의 외접원의 반지름의 길이는 10, 내접원의 반지름의 길이는 4이다. "
              "이때 [[tri(ABC)]]의 넓이를 구하시오."),
    choices=None, derived_answer="96",
    figure=U("외접원(중심 O, BC의 중점) 안의 직각삼각형 ABC(A 위, B 왼쪽, C 오른쪽, BC가 지름) 음영, 내접원(중심 O′)이 AB·BC·CA와 D·E·F에서 접함"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "직각삼각형·외접원·내접원 도형",
    note="BC=20, AB+AC=28, AB·AC=(28²−20²)/2=192 → 넓이 96. 빠른정답 14 cm과 불일치.")

# ══════════════ 평행사변형 ══════════════
# ── p2 평행사변형의 뜻
add(id="59775d26", qtype="choice",
    question="다음 그림과 같은 평행사변형 ABCD에서 [[angle(x) + angle(y)]]의 크기는?",
    choices=DEG5(80, 85, 90, 95, 100), derived_answer="①",
    figure=U(PAR + ", 두 대각선 AC·BD의 교점 O, A에 ∠DAC = x, B에 ∠ABD = y, D에 50°(∠BDC), C에 30°(∠BCA)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·대각선 각 표시 도형",
    note="x=∠BCA=30°(엇각), y=∠BDC=50°(엇각) → 80° → ①. 빠른정답 없음.")

# ── p4
add(id="de315b97", qtype="short",
    question="다음 그림의 평행사변형에서 [[angle(x)]] 의 크기를 구하시오.",
    choices=None, derived_answer=None,
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, B에 35°(∠ABD), C에 65°(∠BCA), O에 ∠AOB = x"),
    difficulty_est=2, confidence=0.7, needs_review=FIG + "평행사변형·대각선 각 표시 도형",
    note="답 미도출: x=∠AOB=∠DBC+65°인데 ∠DBC가 주어지지 않음(두 각 35°, 65°로는 도형이 성립하지 않는 것으로 보임). 빠른정답 없음.")

# ── p5
add(id="6f4b59b9", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 두 대각선의 교점을 O라 하자. [[angle(DAO) = deg(40)]], [[angle(OBC) = deg(54)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(94)",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, A에 40°(∠DAO), B에 54°(∠OBC), O에 ∠DOC = x"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·대각선 각 표시 도형",
    note="∠OCB=∠DAO=40°(엇각), x=∠DOC=54°+40°=94°. 빠른정답 없음.")

# ── p8 평행사변형의 성질 (○× 판정형)
add(id="9c9f3783", qtype="short",
    question=("아래 그림과 같은 평행사변형 ABCD에서 점 O는 두 대각선의 교점일 때, 다음 설명이 옳으면 '○'를, 옳지 않으면 '×'를 고르시오.\n"
              "[[seg(AC) = seg(BD)]]\n① ○ ② ×"),
    choices=None, derived_answer="②",
    figure=U(PAR + ", 두 대각선 AC·BD의 교점 O"),
    difficulty_est=1, confidence=0.8,
    needs_review="선지 2개(○× 판정형, 5지 규격 밖) — 보기를 본문에 텍스트로 포함 / " + FIG + "평행사변형·대각선 도형",
    note="평행사변형의 두 대각선의 길이는 일반적으로 다름 → × → ②. 빠른정답 없음.")

# ── p10
add(id="7efc8c54", qtype="choice",
    question="아래 그림의 [[quad(ABCD)]]가 평행사변형일 때, 다음 중 옳지 않은 것은?",
    choices=["[[par(seg(AD), seg(BC))]]", "[[par(seg(AB), seg(DC))]]", "[[seg(AO) = seg(CO)]]", "[[angle(BAD) = angle(BCD)]]",
             "[[angle(ABC) + angle(ADC) = deg(180)]]"],
    derived_answer="⑤",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·대각선 도형",
    note="대각은 서로 같으므로 ∠ABC=∠ADC(합이 180°인 것은 이웃한 두 각) → ⑤. 빠른정답 없음.")

# ── p12
add(id="d5d43e0d", qtype="choice",
    question="다음 그림과 같은 평행사변형 ABCD 에서 두 대각선의 교점을 O 라 할 때, 다음 중 옳지 않은 것은?",
    choices=["[[seg(AB) = seg(DC)]], [[seg(AD) = seg(BC)]]", "[[seg(AO) = seg(BO)]]", "[[seg(OA) = seg(OC)]], [[seg(OB) = seg(OD)]]",
             "[[angle(A) = angle(C)]], [[angle(B) = angle(D)]]", "[[angle(BCA) = angle(DAC)]]"],
    derived_answer="②",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·대각선 도형",
    note="대각선은 서로 다른 것을 이등분하지만 AO=BO는 일반적으로 성립하지 않음 → ②. 빠른정답 없음.")

# ── p14 성질의 증명 (id 2개, 선지 ④⑤ 잘림)
dup(["82c1f20b", "ec313eaa"], qtype="choice",
    question=("다음은 \"평행사변형은 두 쌍의 대변의 길이가 각각 같다.\"를 증명한 것이다. (가)~(다)에 알맞은 것으로 옳지 않은 것은?\n"
              "[[quad(ABCD)]]에서 대각선 AC를 그으면\n[[par(seg(AB), seg(CD))]]이므로\n[[angle(BAC) = angle(DCA)]] ⋯ ㉠\n"
              "[[par(seg(AD), seg(BC))]]이므로\n[[angle(ACB)]] = (가) ⋯ ㉡\n또, (나) 는 공통 ⋯ ㉢\n㉠, ㉡, ㉢에서\n"
              "[[tri(ABC)]] ≡ (다) (ASA 합동)\n∴ [[seg(AB) = seg(CD)]], [[seg(AD) = seg(BC)]]"),
    choices=["(가) [[angle(ACD)]]", "(나) [[seg(AC)]]", "(다) [[tri(CDA)]]", "(이미지 하단 잘림)", "(이미지 하단 잘림)"],
    derived_answer="①",
    figure=U(PAR + ", 대각선 AC"),
    difficulty_est=2, confidence=0.7,
    needs_review="이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움) / " + FIG + "평행사변형·대각선 도형",
    note="(가)는 ∠CAD(엇각)이므로 ① 옳지 않음(보이는 선지 기준). 같은 쪽에 id 2개. 빠른정답 없음.")

# ── p15
add(id="7bdd9809", qtype="choice",
    question=("다음은 평행사변형 ABCD에서 \"두 대각선은 서로 다른 것을 이등분한다.\"를 증명하는 과정이다. ①~⑤에 들어갈 것으로 옳지 않은 것은?\n"
              "[[tri(ABO)]]와 [[tri(CDO)]]에서\n평행사변형의 대변의 길이는 같으므로\n[[seg(AB) = seg(CD)]] ⋯ ㉠\n평행선의 엇각의 성질에서\n"
              "[[angle(ABO)]] = ① ⋯ ㉡\n[[angle(BAO)]] = ② ⋯ ㉢\n㉠, ㉡, ㉢으로부터\n[[tri(ABO)]] ≡ ③ ( ④ 합동)\n∴ ⑤"),
    choices=["[[angle(CDO)]]", "[[angle(DCO)]]", "[[tri(CDO)]]", "SAS", "[[seg(OA) = seg(OC)]], [[seg(OB) = seg(OD)]]"],
    derived_answer="④",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·대각선 도형",
    note="한 변과 양 끝 각 → ASA 합동이어야 하므로 ④ SAS가 옳지 않음. 빠른정답 없음.")

# ── p17
add(id="07743e67", qtype="choice",
    question=("다음은 '평행사변형에서 두 쌍의 대변의 길이는 각각 같다.'를 설명하는 과정이다. ①~⑤에 들어갈 것으로 옳지 않은 것은?\n"
              "다음 그림과 같이 점 B와 점 D를 이으면\n[[tri(ABD)]]와 [[tri(CDB)]]에서 [[seg(AB)]] ∥ ① 이므로\n② = [[angle(CDB)]] (엇각) ⋯ ㉠\n"
              "[[par(seg(AD), seg(BC))]]이므로\n[[angle(ADB)]] = ③ (엇각) ⋯ ㉡\n④ 는 공통 ⋯ ㉢\n㉠, ㉡, ㉢에 의하여\n"
              "[[cong(tri(ABD), tri(CDB))]] ( ⑤ 합동)\n∴ [[seg(AB) = seg(CD)]], [[seg(AD) = seg(BC)]]"),
    choices=["[[seg(CD)]]", "[[angle(ABD)]]", "[[angle(CDB)]]", "[[seg(BD)]]", "ASA"],
    derived_answer="③",
    figure=U(PAR + " 2개(본문 위: 대각선 없음, 상자 안: 대각선 BD와 B·D에 엇각 표시 ○·×)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·대각선 BD 도형",
    note="③은 ∠CBD(AD∥BC의 엇각)이어야 하므로 옳지 않음. 빠른정답 없음.")

# ── p20 대변의 길이 응용
_Q_PQ = ("다음 그림과 같이 [[seg(AB) = {a}]] cm, [[seg(AD) = {d}]] cm, [[seg(AC) = {c}]] cm인 평행사변형 ABCD의 변 BC 위에 움직이는 점 P가 있다. "
         "[[angle(PAD)]]의 이등분선이 변 BC 또는 그 연장선과 만나는 점을 Q라 하면 점 P가 변 BC 위를 점 B에서부터 C까지 움직일 때, "
         "점 Q가 변 BC 또는 그 연장선 위를 움직인 거리를 구하시오.")
_F_PQ = ("평행사변형 ABCD(A 위 왼쪽, D 위 오른쪽, B 아래 왼쪽, C 아래 오른쪽), 변 BC 위의 점 P(B 쪽)·Q(C 쪽), 선분 AP·AQ·AC, "
         "A에 각 이등분 표시(점 2개), AB={a} cm·AD={d} cm·AC={c} cm 치수(점선 호)")
add(id="9b2b0527", qtype="short", question=_Q_PQ.format(a=6, d=9, c=7),
    choices=None, derived_answer="10 cm", figure=U(_F_PQ.format(a=6, d=9, c=7)),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·움직이는 점·각의 이등분선 도형",
    note="∠DAQ=∠AQP → AP=PQ, BQ=BP+AP: P=B일 때 6, P=C일 때 9+7=16 → 10 cm. 빠른정답 없음.")

# ── p21
add(id="917e94ff", qtype="short", question=_Q_PQ.format(a=5, d=8, c=6),
    choices=None, derived_answer="9 cm", figure=U(_F_PQ.format(a=5, d=8, c=6)),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·움직이는 점·각의 이등분선 도형",
    note="BQ=BP+AP: P=B일 때 5, P=C일 때 8+6=14 → 9 cm. 빠른정답 없음.")

# ── p24
add(id="0da4110c", qtype="short",
    question=("다음 그림의 평행사변형 ABCD에서 [[seg(BE)]]는 [[angle(ABC)]]의 이등분선이다. [[seg(BC) = 10]] cm, [[seg(CD) = 7]] cm일 때, "
              "[[seg(DE)]]의 길이를 구하시오."),
    choices=None, derived_answer="3 cm",
    figure=U(PAR + ", AD 위의 점 E와 선분 BE, B에 각 이등분 표시(점 2개), BC=10 cm·CD=7 cm 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·각의 이등분선 도형",
    note="∠ABE=∠EBC=∠AEB → AE=AB=7, DE=10−7=3 cm. 빠른정답 9cm과 불일치.")

# ── p25
add(id="ef409483", qtype="short",
    question=("다음 그림과 같이 평행사변형 ABCD에서 [[angle(A)]]의 이등분선이 [[seg(BC)]]와 만나는 점을 E라 하자. "
              "[[seg(AB) = 9]] cm, [[seg(EC) = 3]] cm일 때, [[seg(AD)]]의 길이를 구하시오."),
    choices=None, derived_answer="12 cm",
    figure=U(PAR + ", BC 위의 점 E와 선분 AE, A에 각 이등분 표시(점 2개), AB=9 cm·EC=3 cm 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·각의 이등분선 도형",
    note="BE=AB=9 → AD=BC=9+3=12 cm. 빠른정답 7과 불일치.")

# ── p27 대각의 크기 응용
_Q_H = ("다음 그림과 같은 평행사변형 ABCD에서 CD의 중점을 E라 하고 점 A에서 [[seg(BE)]]에 내린 수선의 발을 H라 하자. "
        "[[angle(ABH) = deg({p})]], [[angle(ADH) = deg({q})]]일 때, [[angle(C)]]의 크기를 구하시오.")
_F_H = ("평행사변형 ABCD(A 위, D 오른쪽 위, B 왼쪽 아래, C 아래), CD의 중점 E(DE=EC 표시), 선분 BE와 A에서 BE에 내린 수선의 발 H(직각 표시), "
        "선분 DH, B에 {p}°(∠ABH), D에 {q}°(∠ADH)")
add(id="7ed66ceb", qtype="short", question=_Q_H.format(p=30, q=40),
    choices=None, derived_answer="deg(130)", figure=U(_F_H.format(p=30, q=40)),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·중점·수선 복합 도형",
    note="BE와 AD의 연장선의 교점 F: △BCE≡△FDE → DA=DF=DH, ∠DAH=∠DHA=70°, ∠BAH=60° → ∠A=∠C=130°. 빠른정답 3cm과 불일치.")

# ── p28
add(id="168d7e7f", qtype="short",
    question=("다음 그림과 같이 평행사변형 ABCD에서 점 E는 변 AB의 중점이고 점 F는 점 D에서 선분 EC에 내린 수선의 발이다. "
              "[[angle(FDC) = deg(14)]], [[angle(B) = deg(76)]]일 때, [[angle(AFE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(28)",
    figure=U(PAR + ", AB의 중점 E(AE=EB 표시), 선분 EC, D에서 EC에 내린 수선의 발 F(직각 표시), 선분 AF, D에 14°(∠FDC), B에 76°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·중점·수선 복합 도형",
    note="CE와 DA의 연장선의 교점 G: △EBC≡△EAG → AG=AD=AF, ∠AFE=∠AGE=∠BCE=104°−76°=28°. 빠른정답 12cm과 불일치.")

# ── p29
add(id="3e041a19", qtype="short", question=_Q_H.format(p=34, q=46),
    choices=None, derived_answer="deg(100)", figure=U(_F_H.format(p=34, q=46) + ", C에 각 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·중점·수선 복합 도형",
    note="DA=DH → ∠DAH=90°−46°=44°, ∠BAH=90°−34°=56° → ∠C=∠A=100°. 빠른정답 없음.")

# ── p30
add(id="a4f542e8", qtype="choice",
    question="다음 그림과 같은 평행사변형 ABCD에서 [[ratio(angle(A), angle(B)) = ratio(3, 2)]]일 때, [[angle(C)]]의 크기는?",
    choices=DEG5(96, 100, 104, 108, 112), derived_answer="④",
    figure=U(PAR + ", C에 각 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형 도형",
    note="∠A=180°×3/5=108°=∠C → ④. 빠른정답 없음.")

# ── p31
add(id="f0b0c2b5", qtype="choice",
    question="다음 그림과 같은 평행사변형 ABCD에서 [[angle(x)]]의 크기는?",
    choices=DEG5(70, 75, 80, 85, 90), derived_answer="②",
    figure=U(PAR + ", A에서 변 CD 위의 한 점(라벨 없음)으로 그은 선분, A에 35°(AD와 선분 사이), C에 110°(∠BCD), 그 점에서 선분과 CD(D 쪽)가 이루는 각 x"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·내부 선분 각 표시 도형",
    note="∠D=180°−110°=70°, x=180°−35°−70°=75° → ②. 빠른정답 없음.")

# ── p32
add(id="02bccd32", qtype="short",
    question="다음 그림과 같은 평행사변형 ABCD에서 [[ratio(angle(B), angle(C)) = ratio(2, 1)]]일 때, [[angle(A)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=U(PAR + ", A에 각 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형 도형",
    note="∠B=120° → ∠A=60°. 빠른정답 없음.")

# ── p34
add(id="911f69e6", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[angle(A)]]의 이등분선이 [[seg(CD)]]와 만나는 점을 E, 꼭짓점 B에서 [[seg(AE)]]에 내린 수선의 발을 F라 하자. "
              "[[angle(C) = deg(120)]]일 때, [[angle(FBC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(30)",
    figure=U("평행사변형 ABCD(A 위 왼쪽, D 위 오른쪽, B 아래 왼쪽, C 아래 오른쪽), A의 이등분선(점 2개)이 CD와 만나는 점 E, B에서 AE에 내린 수선의 발 F(직각 표시), C에 120°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·각의 이등분선·수선 도형",
    note="∠A=120°, ∠BAE=60°, ∠ABF=30°, ∠ABC=60° → ∠FBC=30°. 빠른정답 없음.")

# ── p35 대각선 응용
add(id="d94fd8cc", qtype="short",
    question=("그림과 같은 평행사변형 ABCD 에서 [[seg(OA) = 4]] cm, [[seg(OD) = 5]] cm 일 때, [[seg(AC) = x]] cm, [[seg(BD) = y]] cm 라고 한다. "
              "[[x + y]] 의 값을 구하시오. (단, 점 O 는 두 대각선의 교점)"),
    choices=None, derived_answer="18",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, OA=4 cm·OD=5 cm 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·대각선 치수 도형",
    note="x=8, y=10 → 18. 빠른정답 없음.")

# ── p37
add(id="e663bbdc", qtype="short",
    question="다음 그림과 같은 평행사변형 ABCD에서 [[seg(AB) = 9]], [[seg(BD) = 8]], [[seg(AC) = 14]]일 때, [[tri(OCD)]]의 둘레의 길이를 구하시오.",
    choices=None, derived_answer="20",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, AB=9·BD=8·AC=14 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·대각선 치수 도형",
    note="CD=9, OC=7, OD=4 → 20. 빠른정답 없음.")

# ── p40
add(id="1c18a5bc", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 두 대각선의 교점을 O라 하자. [[seg(AC) = 12]] cm, [[seg(BD) = 10]] cm, [[seg(BC) = 8]] cm일 때, "
              "[[tri(AOD)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="19 cm",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, AC=12 cm·BD=10 cm·BC=8 cm 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·대각선 치수 도형",
    note="AD=8, AO=6, DO=5 → 19 cm. 빠른정답 20과 불일치.")

# ── p41
add(id="28d28d7e", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 두 대각선의 교점 O를 지나는 직선이 [[seg(AD)]], [[seg(BC)]]와 만나는 점을 각각 E, F라 하자. "
              "[[seg(EF) = 16]] cm, [[seg(ED) = 10]] cm, [[seg(OD) = 12]] cm일 때, [[tri(OBF)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="30 cm",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, O를 지나는 직선이 AD와 E, BC와 F에서 만남, EF=16 cm·ED=10 cm·OD=12 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·대각선·교점 직선 도형",
    note="△OBF≡△ODE(ASA) → OB=12, OF=8, BF=10 → 30 cm. 빠른정답 없음.")

# ── p42 평행사변형이 되는 조건의 증명 (㉠~㉤ 답)
add(id="c670c281", qtype="short",
    question=("다음은 '두 대각선이 서로 다른 것을 이등분하면 평행사변형이 된다.'를 증명하는 과정이다. ㉠~㉤ 중 옳지 않은 것을 고르시오.\n"
              "[가정] [[quad(ABCD)]]에서 [[seg(OA) = seg(OC)]], [[seg(OB) = seg(OD)]]\n"
              "[결론] [[par(seg(AB), seg(CD))]], [[par(seg(AD), seg(BC))]]\n"
              "[증명] [[tri(OAB)]]와 [[tri(OCD)]]에서\n"
              "㉠ [[seg(OA) = seg(OC)]], [[seg(OB) = seg(OD)]]\n"
              "[[angle(AOB) = angle(COD)]] (㉡ 맞꼭지각)\n"
              "따라서 [[cong(tri(OAB), tri(OCD))]] (㉢ ASA 합동)\n"
              "[[angle(OAB) = angle(OCD)]]\n"
              "㉣ ∴ [[par(seg(AB), seg(CD))]] ⋯ ①\n"
              "같은 방법으로 [[cong(tri(OAD), tri(OCB))]]이므로\n"
              "㉤ [[angle(OAD) = angle(OCB)]]\n"
              "∴ [[par(seg(AD), seg(BC))]] ⋯ ②\n"
              "①, ②에 의하여 [[quad(ABCD)]]는 평행사변형이다."),
    choices=None, derived_answer="ㄷ",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O"),
    difficulty_est=2, confidence=0.75,
    needs_review="답 표기 문법 한계: 정답 기호 ㉢을 ㄷ으로 대체 / " + FIG + "평행사변형·대각선 도형",
    note="두 변과 끼인각 → SAS 합동이어야 하므로 ㉢(ASA 합동)이 옳지 않음. 빠른정답 20과 불일치.")

# ── p43
add(id="db247fef", qtype="choice",
    question=("다음은 '한 쌍의 대변이 평행하고 그 길이가 같은 사각형은 평행사변형이다.'를 증명하는 과정이다. 밑줄 친 부분 중 옳지 않은 것을 모두 고르면? (정답 2개)\n"
              "대각선 AC를 그으면\n[[tri(ABC)]] 와 [[tri(CDA)]]에서\n"
              "① [[seg(AD) = seg(BC)]] ⋯ ㉠\n"
              "② [[angle(DCA) = angle(BAC)]] (엇각) ⋯ ㉡\n"
              "③ [[seg(AC)]]는 공통 ⋯ ㉢\n"
              "㉠, ㉡, ㉢에 의해서\n[[cong(tri(ABC), tri(CDA))]] (④ SAS 합동)\n"
              "⑤ [[angle(DAC) = angle(BCA)]]이므로\n∴ [[par(seg(AB), seg(DC))]]\n"
              "따라서 두 쌍의 대변이 각각 평행하므로\n[[quad(ABCD)]]는 평행사변형이다."),
    choices=["[[seg(AD) = seg(BC)]]", "[[angle(DCA) = angle(BAC)]] (엇각)", "[[seg(AC)]]는 공통", "SAS 합동", "[[angle(DAC) = angle(BCA)]]"],
    derived_answer="②, ⑤",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD∥BC(화살표)·AD=BC(두 줄 표시), 대각선 AC"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사각형·대각선·평행 표시 도형",
    note="㉡은 ∠DAC=∠BCA(AD∥BC의 엇각), ⑤는 ∠DCA=∠BAC이어야 AB∥DC → ②, ⑤. 인쇄된 선지는 번호 ①~⑤만 있어 밑줄 내용으로 채움. 빠른정답 19cm과 불일치.")

# ── p44
add(id="27c983ac", qtype="choice",
    question=("다음은 '두 쌍의 대각의 크기가 각각 같은 사각형은 평행사변형이다.'를 설명하는 과정이다. (가)~(마)에 들어갈 것으로 옳지 않은 것은?\n"
              "[[quad(ABCD)]]에서 [[angle(A) = angle(C)]], (가)\n[[angle(A) = angle(C) = a]]\n(가) = [[b]]라 하면\n"
              "[[2a + 2b]] = (나)\n∴ [[a + b]] = (다)\n(라)의 합이 [[deg(180)]]이므로\n∴ [[par(seg(AB), seg(DC))]], (마)"),
    choices=["(가) [[angle(B) = angle(D)]]", "(나) [[deg(360)]]", "(다) [[deg(180)]]", "(라) 엇각", "(마) [[par(seg(AD), seg(BC))]]"],
    derived_answer="④",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), A·C에 × 표시, B·D에 ● 표시(같은 크기의 각)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사각형·같은 각 표시 도형",
    note="(라)는 동측내각(합 180°)이어야 하므로 ④ 엇각이 옳지 않음. 빠른정답 30cm과 불일치.")

# ── p45
add(id="5f4b64cc", qtype="choice",
    question=("다음은 '두 쌍의 대변의 길이가 각각 같은 사각형은 평행사변형이다.'를 증명하는 과정이다. □ 안에 알맞은 것은?\n"
              "[[seg(AB) = seg(CD)]], [[seg(AD) = seg(BC)]]인 [[quad(ABCD)]]에서\n점 A와 점 C를 이으면\n[[tri(ABC)]]와 [[tri(CDA)]]에서\n"
              "[[seg(AB) = seg(CD)]] (가정) ⋯ ㉠\n[[seg(BC) = seg(AD)]] (가정) ⋯ ㉡\n□는 공통 ⋯ ㉢\n"
              "㉠, ㉡, ㉢에 의하여 [[cong(tri(ABC), tri(CDA))]] (SSS합동)\n[[angle(BAC) = angle(DCA)]]이므로\n[[par(seg(AB), seg(CD))]] ⋯ ㉣\n"
              "[[angle(ACB) = angle(CAD)]]이므로\n[[par(seg(AD), seg(BC))]] ⋯ ㉤\n㉣, ㉤에 의하여 [[quad(ABCD)]]는 평행사변형이다."),
    choices=["[[seg(DC)]]", "[[seg(BC)]]", "[[seg(DA)]]", "[[seg(AC)]]", "[[seg(BA)]]"],
    derived_answer="④",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB=CD(한 줄)·AD=BC(두 줄) 표시, 대각선 AC"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "사각형·대각선·등변 표시 도형",
    note="공통인 변은 AC → ④. 빠른정답 없음.")

# ── p56 평행사변형이 되는 조건 (선지가 그림)
add(id="d15a39e6", qtype="choice",
    question="다음 사각형 중 평행사변형이 아닌 것은?",
    choices=["(그림) 세 각이 [[deg(40)]](왼쪽 아래), [[deg(140)]](왼쪽 위), [[deg(40)]](오른쪽 위)인 사각형",
             "(그림) 윗변·아랫변이 [[6]], 왼쪽·오른쪽 변이 [[5]]인 사각형",
             "(그림) 윗변·아랫변이 [[3]], 왼쪽 위 각 [[deg(120)]], 왼쪽 아래 각 [[deg(60)]]인 사각형",
             "(그림) 네 각이 모두 직각인 사각형",
             "(그림) 세 각이 [[deg(40)]](왼쪽 아래), [[deg(130)]](왼쪽 위), [[deg(40)]](오른쪽 위)인 사각형"],
    derived_answer="⑤",
    figure=U("선지 ①~⑤가 각각 사각형 그림: ① 각 40°(왼쪽 아래)·140°(왼쪽 위)·40°(오른쪽 위), ② 변 6(위)·5(왼쪽)·6(아래)·5(오른쪽) 점선 호 치수, "
             "③ 변 3(위)·3(아래), 각 120°(왼쪽 위)·60°(왼쪽 아래), ④ 네 꼭짓점 직각 표시, ⑤ 각 40°(왼쪽 아래)·130°(왼쪽 위)·40°(오른쪽 위)"),
    difficulty_est=2, confidence=0.75, needs_review=FIG + "선지가 사각형 그림 5개(각·변 표시)",
    note="⑤는 130°+40°≠180°로 대변이 평행하지 않음 → ⑤(①·②·④는 성질 충족, ③은 한 쌍의 대변이 평행하고 길이가 같음). 빠른정답 없음.")

# ── p57
add(id="2c754a16", qtype="choice",
    question=("아래 그림과 같이 [[angle(C) = deg(45)]]이고 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에 한 가지 조건만을 추가하여 평행사변형이 되게 하려고 한다. "
              "다음 중 가능한 조건을 모두 고르면? (정답 2개)"),
    choices=["[[angle(A) = angle(D)]]", "[[seg(AB) = seg(DC)]]", "[[angle(A) + angle(C) = deg(180)]]", "[[par(seg(AB), seg(DC))]]", "[[seg(AD) = seg(BC)]]"],
    derived_answer="④, ⑤",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD∥BC 화살표 표시, C에 45° 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사다리꼴 도형",
    note="④ 두 쌍의 대변이 평행, ⑤ 한 쌍의 대변이 평행하고 길이가 같음 → ④, ⑤(①②③은 등변사다리꼴이 될 수 있음). 빠른정답 없음.")

# ── p59
add(id="0d0b7a14", qtype="choice",
    question="다음 조건을 만족하는 [[quad(ABCD)]] 중 평행사변형이 아닌 것을 모두 고르면? (정답 2개)",
    choices=["[[angle(A) = deg(40)]], [[angle(B) = deg(140)]], [[angle(C) = deg(40)]]",
             "[[par(seg(AB), seg(DC))]], [[seg(AB) = 5]], [[seg(DC) = 5]]",
             "[[seg(AB) = 10]], [[seg(BC) = 5]], [[seg(CD) = 6]], [[seg(DA) = 6]]",
             "[[angle(A) = angle(C)]], [[par(seg(AB), seg(DC))]]",
             "[[par(seg(AB), seg(DC))]], [[seg(AC) = seg(BD)]]"],
    derived_answer="③, ⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="③ 대변의 길이가 다름, ⑤ 등변사다리꼴이 될 수 있음 → ③, ⑤(④는 ∠B=∠D도 성립). 빠른정답 없음.")

# ── p63 새롭게 만든 사각형
add(id="83b92bc8", qtype="short",
    question=("다음 그림과 같이 평행사변형 ABCD의 두 대각선의 교점을 O라 하고, [[seg(DC)]]의 연장선 위에 [[seg(CD) = seg(CE)]]가 되도록 점 E를 잡자. "
              "[[angle(BEO) = angle(OED) = deg(26)]]일 때, [[angle(ABD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(64)",
    figure=U("평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽·D 아래), 대각선 AC·BD의 교점 O, DC의 연장선 위(C 아래) 점 E(DC=CE 표시), "
             "선분 BE·OE, E에 26°·26°(∠BEO, ∠OED) 표시, B의 각(∠ABD) 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·연장선·교점 복합 도형",
    note="OC∥BE(중점 연결) → ∠COE=∠OEC=26°, CO=CE=CD → ∠CDO=(180°−52°)/2=64°=∠ABD(엇각). 빠른정답 없음.")

# ── p64
add(id="79396cdf", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[angle(BAC)]]의 이등분선과 [[angle(BCA)]]의 이등분선의 교점을 E, [[angle(D)]]의 이등분선과 "
              "[[angle(DCA)]]의 이등분선의 교점을 F라 할 때, [[quad(AECF)]]는 어떤 사각형인지 구하시오."),
    choices=None, derived_answer="평행사변형",
    figure=U("평행사변형 ABCD(A 위 왼쪽, D 위 오른쪽, B 아래 왼쪽, C 아래 오른쪽), 대각선 AC, △ABC 내부의 점 E와 △ACD 내부의 점 F, A·C·D에 각 이등분 표시(○·×·△·●), □AECF 음영"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·각의 이등분선 교점 도형",
    note="∠EAC=∠FCA, ∠ECA=∠FAC → AE∥CF, AF∥CE → 평행사변형 = 빠른정답 ✓.")

# ── p66
add(id="0d9e07bb", qtype="choice",
    question=("아래 그림의 평행사변형 ABCD에서 [[angle(A)]]와 [[angle(C)]]의 이등분선과 [[seg(BC)]], [[seg(AD)]]와의 교점을 E, F라고 할 때, "
              "다음 중 옳지 않은 것은?"),
    choices=["[[seg(AB) = seg(DF)]]", "[[angle(BEA) = angle(DFC)]]", "[[seg(AF) = seg(CE)]]", "[[seg(AE) = seg(CF)]]", "[[angle(AEC) = angle(BAD)]]"],
    derived_answer="⑤",
    figure=U("평행사변형 ABCD(A 왼쪽 위, F·D 오른쪽 위, B 왼쪽 아래, E·C 오른쪽 아래), 선분 AE·CF, A·C에 각 이등분 표시(●·×)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·각의 이등분선 도형",
    note="∠AEC=180°−½∠A로 일반적으로 ∠BAD와 다름 → ⑤. 빠른정답 없음.")

# ── p68
add(id="ce042db7", qtype="choice",
    question=("아래 그림과 같은 평행사변형 ABCD에서 두 대각선의 교점을 O라 하고 대각선 AC 위에 [[seg(AE) = seg(CF)]]가 되도록 두 점 E, F를 잡을 때, "
              "다음 보기는 [[quad(EBFD)]]가 평행사변형임을 증명하는 과정이다. (가), (나)에 알맞은 것을 순서대로 적은 것은?\n<보기>\n"
              "[[quad(ABCD)]]는 평행사변형이므로 [[seg(OB)]] = (가)\n가정에서 [[seg(AE) = seg(CF)]]이므로 [[seg(OE)]] = (나)\n"
              "따라서 두 대각선이 서로 다른 것을 이등분하므로 [[quad(EBFD)]]는 평행사변형이다."),
    choices=["[[seg(OC)]], [[seg(BF)]]", "[[seg(OC)]], [[seg(OF)]]", "[[seg(OD)]], [[seg(BF)]]", "[[seg(OD)]], [[seg(OC)]]", "[[seg(OD)]], [[seg(OF)]]"],
    derived_answer="⑤",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, AC 위의 점 E(A 쪽)·F(C 쪽)(AE=CF 표시), □EBFD 음영"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형·대각선 위 두 점 도형",
    note="OB=OD, OE=OF → ⑤. 빠른정답 없음.")

# ── p69 조건의 응용
add(id="6991bd9f", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[angle(A)]], [[angle(C)]]의 이등분선이 [[seg(BC)]], [[seg(AD)]]와 만나는 점을 각각 E, F라 하자. "
              "[[seg(AB) = 7]] cm, [[seg(BC) = 11]] cm이고, [[quad(ABCD)]]의 넓이가 [[66]] cm²일 때, [[quad(AECF)]]의 넓이를 구하시오."),
    choices=None, derived_answer="24 cm²",
    figure=U("평행사변형 ABCD(A 위 왼쪽, F·D 위 오른쪽, B 아래 왼쪽, E·C 아래 오른쪽), 선분 AE·CF, A·C에 각 이등분 표시, □AECF 음영, AB=7 cm·BC=11 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·각의 이등분선 음영 도형",
    note="BE=AB=7, EC=4, 높이 66/11=6 → □AECF=4×6=24 cm². 빠른정답 없음.")

# ── p71 (정삼각형 3개)
_Q_PQR = ("다음 그림에서 [[tri(PBA)]], [[tri(QBC)]], [[tri(RAC)]]는 [[tri(ABC)]]의 세 변을 각각 한 변으로 하는 정삼각형이다. "
          "[[angle(ACB) = deg(60)]], [[angle(BAC) = deg({a})]]일 때, [[angle(PQR)]]의 크기를 구하시오.")
_F_PQR = ("삼각형 ABC(A 위 가운데, B 왼쪽 아래, C 오른쪽 아래), AB 바깥쪽의 정삼각형 PBA(P 왼쪽 위), BC의 A 쪽에 그린 정삼각형 QBC(Q 위, A 근처), "
          "AC 바깥쪽의 정삼각형 RAC(R 오른쪽), 점선 PQ·QR, A에 {a}°, C에 60°")
add(id="120f1946", qtype="short", question=_Q_PQR.format(a=73),
    choices=None, derived_answer="deg(167)", figure=U(_F_PQR.format(a=73)),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·정삼각형 3개 복합 도형",
    note="△PBQ≡△ABC, △RCQ≡△ACB → PQ=AR, QR=AP → □APQR 평행사변형, ∠PQR=∠PAR=360°−60°−60°−73°=167°. 빠른정답 없음.")

# ── p72
add(id="b0c8904a", qtype="short",
    question=("다음 그림의 평행사변형 ABCD의 두 꼭짓점 B, D에서 대각선 AC에 내린 수선의 발을 각각 P, Q라 하자. "
              "[[angle(DPQ) = deg(60)]]일 때, [[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(30)",
    figure=U(PAR + ", 대각선 AC, B·D에서 AC에 내린 수선의 발 P·Q(직각 표시), 선분 PD·BQ, P에 60°(∠DPQ), B에 ∠PBQ = x"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·대각선·수선 도형",
    note="BP∥DQ, BP=DQ → □PBQD 평행사변형, x=∠PDQ=90°−60°=30°. 빠른정답 없음.")

# ── p73 (움직이는 점)
add(id="3e56eaa2", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 100]] cm인 평행사변형 ABCD에서 점 P는 [[seg(AB)]] 위를 초속 3 cm로 점 A에서 출발하여 B쪽으로, "
              "점 Q는 [[seg(CD)]] 위를 초속 4 cm로 점 C에서 출발하여 D쪽으로 움직이고 있다. 점 P가 출발하고 나서 3초 후에 점 Q가 출발할 때, "
              "[[par(seg(AQ), seg(PC))]]가 되는 것은 점 Q가 출발한 지 몇 초 후인지 구하시오."),
    choices=None, derived_answer="9초 후",
    figure=U(PAR + ", AB 위의 점 P(아래쪽 화살표), CD 위의 점 Q(위쪽 화살표), 선분 AQ·PC, AB=100 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·움직이는 점 도형",
    note="AP=QC일 때 □APCQ 평행사변형: 3(t+3)=4t → t=9(초). 빠른정답 3과 불일치.")

# ── p74
add(id="cf0fa77a", qtype="choice",
    question=("[[seg(AB) = 100]] m인 평행사변형 ABCD를 점 P는 점 A에서 점 B까지 매초 5 m의 속력으로, 점 Q는 점 C에서 점 D까지 매초 7 m의 속력으로 이동하고 있다. "
              "점 P가 점 A를 출발한 후 4초가 지났을 때 점 Q가 점 C를 출발한다면 [[quad(APCQ)]]가 평행사변형이 되는 것은 점 Q가 출발한 지 몇 초 후인가?"),
    choices=["5초 후", "8초 후", "10초 후", "12초 후", "15초 후"], derived_answer="③",
    figure=U(PAR + ", AB 위의 점 P(아래쪽 화살표), CD 위의 점 Q(위쪽 화살표), 점선 AQ·PC"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·움직이는 점 도형",
    note="AP=CQ: 5(t+4)=7t → t=10 → ③. 빠른정답 없음.")

# ── p76
add(id="3bbe73e5", qtype="short", question=_Q_PQR.format(a=77),
    choices=None, derived_answer="deg(163)", figure=U(_F_PQR.format(a=77)),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·정삼각형 3개 복합 도형",
    note="□APQR 평행사변형 → ∠PQR=∠PAR=360°−60°−60°−77°=163°. 빠른정답 9초 후와 불일치.")

# ── p77 넓이(1)
add(id="b6e0f4db", qtype="short",
    question=("다음 그림과 같이 넓이가 [[30]] cm²인 평행사변형 ABCD의 변 AB 위에 한 점 E를 잡고 [[seg(AG) = seg(BF)]]가 되도록 변 BC, AD 위에 각각 두 점 F, G를 잡는다. "
              "점 G를 지나고 [[seg(EF)]]와 평행한 직선이 [[seg(CD)]]와 만나는 점을 H라 할 때, [[quad(EFHG)]]의 넓이를 구하시오."),
    choices=None, derived_answer="15 cm²",
    figure=U("평행사변형 ABCD(A 왼쪽 위, G·D 오른쪽 위, B 왼쪽 아래, F·C 오른쪽 아래), AB 위의 점 E, AG=BF(두 줄 표시), EF∥GH(화살표), CD 위의 점 H, □EFHG 음영"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·내부 사각형 음영 도형",
    note="□ABFG·□GFCD가 평행사변형 → △EFG=½□ABFG, △GFH=½□GFCD → 합 ½×30=15 cm². 빠른정답 없음.")

# ── p85 넓이(2)
add(id="a61d4c58", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD의 내부의 한 점 P에 대하여 [[quad(ABCD)]]의 넓이가 [[64]] cm²일 때, "
              "[[tri(PBC)]]와 [[tri(PDA)]]의 넓이의 합을 구하시오."),
    choices=None, derived_answer="32 cm²",
    figure=U(PAR + ", 내부의 점 P와 선분 PA·PB·PC·PD, △PBC·△PDA 음영"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "평행사변형 내부 점·선분 도형",
    note="△PBC+△PDA=½□ABCD=32 cm². 빠른정답 4배와 불일치.")
