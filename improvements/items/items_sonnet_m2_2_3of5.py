# -*- coding: utf-8 -*-
# esc_sonnet_m2-2_3of5 — 이미지 기준 전사 (80 항목 / 80쪽) — 중2-2 닮은 도형·피타고라스 정리의 활용·여러 가지 사각형·삼각형의 외심
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

REV_FIG = "도형 표현 불가: "
FIG_PAR = "평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)"
FIG_TRAP = "등변사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, AD∥BC)"

# ════════════ 닮은 도형 ════════════
# p48
add(id="9ba018ea", qtype="short",
    question=("다음 그림과 같은 직사각형 ABCD에서 [[sim(quad(ABCD), sim(quad(DAEF), quad(AEHG)))]]이고 "
              "[[seg(BC) = 15]] cm, [[seg(CD) = 25]] cm일 때, [[seg(HF)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(48,5) cm",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, 세로가 긴 직사각형), AB 위의 점 E와 CD 위의 점 F를 잇는 가로선 EF, AD 위의 점 G에서 EF에 내린 세로선 GH(H는 EF 위), BC=15cm·CD=25cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직사각형 분할 도형",
    note="닮음비 3/5씩: AE=9, EH=27/5, HF=EF−EH=15−27/5=48/5 cm. 빠른정답 없음.")

# p51
add(id="1f3bb4a4", qtype="short",
    question=("다음 그림에서 [[sim(tri(ABC), tri(DEF))]]이다. [[seg(AC) = 8]] cm, [[seg(DF) = 12]] cm, "
              "[[seg(DE) = 9]] cm일 때, [[seg(AB)]]의 길이를 구하시오."),
    choices=None, derived_answer="6 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽 삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, AC=8cm), 오른쪽 큰 삼각형 DEF(D 위, F 왼쪽 아래, E 오른쪽 아래, DF=12cm·DE=9cm 치수(점선 호))"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "닮은 두 삼각형 도형",
    note="닮음비 8:12=2:3, AB=9·2/3=6 cm = 빠른정답 ✓.")

# p52
add(id="f17baa67", qtype="short",
    question=("다음 그림과 같은 직사각형 ABCD에서 [[sim(quad(ABCD), quad(BEFA))]]이고 [[seg(AB) = 8]] cm, "
              "[[seg(BE) = 6]] cm일 때, [[seg(CE)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(14,3) cm",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), BC 위의 점 E와 AD 위의 점 F를 잇는 세로선 EF, AB=8cm·BE=6cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직사각형 분할 도형",
    note="AB:BE=4:3, BC:EF(=8)=4:3 → BC=32/3, CE=32/3−6=14/3 cm. 빠른정답 없음.")

# p54
add(id="21ade2c3", qtype="short",
    question=("다음 그림에서 [[sim(tri(ABC), tri(AED))]]이고 [[seg(AD) = 4]], [[seg(AE) = 2]], [[seg(DB) = 2]]일 때, "
              "[[seg(EC)]]의 길이를 구하시오."),
    choices=None, derived_answer="10",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 멀리), AB 위의 점 D(AD=4, DB=2), AC 위의 점 E(AE=2), 선분 DE, 치수는 점선 호"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "삼각형 내부 선분 도형",
    note="AB:AE=6:2=3, AC=3·AD=12, EC=12−2=10 = 빠른정답 ✓.")

# p55
add(id="90bcb0dd", qtype="short",
    question=("다음 그림에서 [[sim(tri(ABC), tri(AED))]]이고 [[seg(AD) = 3]] cm, [[seg(AE) = 4]] cm, [[seg(BD) = 5]] cm일 때, "
              "[[seg(EC)]]의 길이를 구하시오."),
    choices=None, derived_answer="2 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 D(AD=3cm, BD=5cm), AC 위의 점 E(AE=4cm), 선분 DE, 치수는 점선 호"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "삼각형 내부 선분 도형",
    note="AB:AE=8:4=2, AC=2·AD=6, EC=6−4=2 cm = 빠른정답 ✓.")

# p56
add(id="59994883", qtype="short",
    question=("다음 그림에서 [[sim(tri(ABC), tri(DEF))]]이고 [[seg(AB) = 2 seg(DE)]]일 때, [[x + y]]의 값을 구하시오."),
    choices=None, derived_answer="101",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽 삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, ∠A=55°, ∠B=30°, BC=12cm), 오른쪽 작은 삼각형 DEF(F 위, D 왼쪽 아래, E 오른쪽 아래, ∠F=x°, FE=y cm 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "닮은 두 삼각형 각·치수 도형",
    note="x=∠C=180−55−30=95, y=EF=BC/2=6 → x+y=101 = 빠른정답 ✓.")

# p57
add(id="a293fa40", qtype="choice",
    question=("다음 그림의 두 직육면체가 서로 닮은 도형이고 [[sim(quad(ABCD), quad(IJKL))]]일 때, 두 직육면체의 닮음비는?"),
    choices=["[[ratio(1, 2)]]", "[[ratio(1, 4)]]", "[[ratio(3, 4)]]", "[[ratio(2, 3)]]", "[[ratio(1, 1)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "작은 직육면체 ABCD-EFGH(윗면 ABCD, 아랫면 EFGH, FG=4, DH=6 치수)와 큰 직육면체 IJKL-MNOP(윗면 IJKL, 아랫면 MNOP, NO=8, OP=6 치수), 보이지 않는 모서리는 점선"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "두 직육면체 치수 도형",
    note="FG:NO=4:8=1:2 → ① = 빠른정답 ✓.")

# p60 (도형 없음)
add(id="beb80c88", qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["닮은 두 도형에서 대응각의 크기는 각각 같다.",
             "닮은 두 도형의 넓이는 같다.",
             "닮은 두 입체도형에서 대응면의 넓이의 비는 일정하다.",
             "닮은 두 입체도형에서 닮음비는 대응하는 모서리의 길이의 비이다.",
             "닮은 두 입체도형에서 대응하는 모서리의 길이의 비는 일정하다."],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="닮은 두 도형의 넓이는 일반적으로 다르다 → ②. 빠른정답 1과 불일치(정렬 어긋남 의심).")

# p61
add(id="bd6c3b00", qtype="choice",
    question=("아래 그림에서 두 사각뿔 P, Q는 닮은 도형이다. [[sim(quad(BCDE), quad(GHIJ))]]일 때, 다음 중 옳은 것은?"),
    choices=["두 사각뿔 P, Q의 닮음비는 [[ratio(3, 4)]]이다.",
             "[[seg(AE) = seg(FJ)]]",
             "[[angle(ACD) = angle(FHI)]]",
             "[[sim(tri(ACD), tri(FIJ))]]",
             "[[ratio(seg(DE), seg(IJ)) = ratio(1, 2)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽 작은 사각뿔 P(꼭짓점 A, 밑면 BCDE, AC=10cm 치수)와 오른쪽 큰 사각뿔 Q(꼭짓점 F, 밑면 GHIJ, FH=15cm 치수), 옆면 음영, 보이지 않는 모서리 점선"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "두 사각뿔 치수 도형",
    note="닮음비 10:15=2:3, 대응각 ∠ACD=∠FHI → ③ = 빠른정답 ✓.")

# p76 (프라임 라벨)
add(id="bee5fb4b", qtype="choice",
    question=("다음 그림에서 두 삼각뿔 V−ABC와 V′−A′B′C′는 닮은 도형이다. [[seg(AB) = 6]] cm, [[seg(VC) = 18]] cm, "
              "A′B′ = 9 cm, [[angle(ACB) = deg(60)]]일 때, V′C′의 길이와 ∠A′C′B′의 크기는?"),
    choices=["V′C′ = [[21]] cm, ∠A′C′B′ = [[deg(60)]]",
             "V′C′ = [[24]] cm, ∠A′C′B′ = [[deg(30)]]",
             "V′C′ = [[24]] cm, ∠A′C′B′ = [[deg(60)]]",
             "V′C′ = [[27]] cm, ∠A′C′B′ = [[deg(30)]]",
             "V′C′ = [[27]] cm, ∠A′C′B′ = [[deg(60)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽 작은 삼각뿔 V−ABC(꼭짓점 V 위, 밑면 ABC, AB=6cm·VC=18cm 치수)와 오른쪽 큰 삼각뿔 V′−A′B′C′(A′B′=9cm 치수), 옆면 초록 음영; 선지는 V′C′·∠A′C′B′ 두 열 표"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(A′B′, V′C′, ∠A′C′B′ 텍스트 혼합) / " + REV_FIG + "두 삼각뿔 치수 도형",
    note="닮음비 6:9=2:3 → V′C′=27 cm, ∠A′C′B′=∠ACB=60° → ⑤ = 빠른정답 ✓.")

# p78 (프라임 라벨)
add(id="ae76a82f", qtype="choice",
    question=("다음 그림에서 두 삼각뿔 V−ABC 와 V′−A′B′C′는 닮은 도형이다. [[seg(AB) = 4]] cm, [[seg(VC) = 12]] cm, "
              "A′B′ = 6 cm, [[angle(ACB) = deg(52)]] 일 때,\nV′C′ 의 길이와 ∠A′C′B′ 의 크기를 바르게 묶어둔 것은?"),
    choices=["[[16]] cm, [[deg(50)]]", "[[16]] cm, [[deg(52)]]", "[[17]] cm, [[deg(52)]]",
             "[[18]] cm, [[deg(50)]]", "[[18]] cm, [[deg(52)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "왼쪽 작은 삼각뿔 V−ABC(꼭짓점 V 위, 밑면 ABC, AB=4cm·VC=12cm 치수)와 오른쪽 큰 삼각뿔 V′−A′B′C′(A′B′=6cm 치수)"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(A′B′, V′C′, ∠A′C′B′ 텍스트 혼합) / " + REV_FIG + "두 삼각뿔 치수 도형",
    note="닮음비 4:6=2:3 → V′C′=18 cm, ∠A′C′B′=52° → ⑤ = 빠른정답 ✓.")

# ════════════ 피타고라스 정리의 활용 ════════════
# p3
add(id="b80c36be", qtype="choice",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 [[seg(BC) = 11]], [[seg(BE) = 9]], [[seg(CD) = 10]]일 때, "
              "[[pow(seg(DE),2)]]의 값은?"),
    choices=["[[57]]", "[[58]]", "[[59]]", "[[60]]", "[[61]]"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, 직각 표시, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 D, AC 위의 점 E, 선분 DE·BE·CD, BE=9·CD=10·BC=11 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·내부 선분 도형",
    note="DE²+BC²=BE²+CD² → DE²=81+100−121=60 → ④. 빠른정답 없음.")

# p4
add(id="fd7a8252", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 [[seg(BC) = 10]], [[seg(BE) = 7]], [[seg(CD) = 8]]일 때, "
              "[[pow(x,2)]]의 값을 구하시오."),
    choices=None, derived_answer="13",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, 직각 표시, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 D, AC 위의 점 E, DE=x, 선분 BE·CD, BE=7·CD=8·BC=10 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·내부 선분 도형",
    note="x=DE, x²=49+64−100=13. 빠른정답 없음.")

# p6
add(id="5d0a605d", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AD) = 4]], [[seg(AE) = 7]], [[seg(BC) = 14]]일 때, "
              "[[pow(seg(BE),2) + pow(seg(CD),2)]]의 값을 구하시오."),
    choices=None, derived_answer="261",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, 직각 표시, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 D(AD=4), AC 위의 점 E(AE=7), 선분 DE·BE·CD, BC=14 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·내부 선분 도형",
    note="BE²+CD²=DE²+BC²=(16+49)+196=261. 빠른정답 없음.")

# p8
add(id="b19f1713", qtype="choice",
    question=("다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AE) = 7]] cm일 때, "
              "[[pow(seg(CD),2) - pow(seg(DE),2)]]의 값은?\n(단, 단위는 생략)"),
    choices=["[[100]]", "[[120]]", "[[150]]", "[[180]]", "[[210]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 왼쪽 위, B 왼쪽 아래 직각 표시, C 오른쪽 아래), AB 위의 점 D, BC 위의 점 E, 선분 AE·CD·DE, AB=5cm·BC=12cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·내부 선분 도형(AB=5cm·BC=12cm는 그림에만 있음)",
    note="AC=13, CD²−DE²=AC²−AE²=169−49=120 → ②. 빠른정답 없음.")

# p11
add(id="d073542b", qtype="choice",
    question="다음 그림의 [[quad(ABCD)]]에서 [[pow(seg(AD),2) + pow(seg(BC),2)]]의 값은?",
    choices=["[[41]]", "[[46]]", "[[51]]", "[[56]]", "[[61]]"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 두 대각선 AC·BD가 직교(교점에 직각 표시), AB=6·CD=5 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "대각선 직교 사각형 도형(직교 조건·치수는 그림에만 있음)",
    note="AD²+BC²=AB²+CD²=36+25=61 → ⑤. 빠른정답 2와 불일치(정렬 어긋남 의심).")

# p12
add(id="214eeff3", qtype="short",
    question=("다음과 같은 사각형 ABCD에서 [[perp(seg(AC), seg(BD))]]이고 [[seg(AO) = 2]], [[seg(BO) = 4]], [[seg(CD) = 7]]일 때, "
              "[[pow(seg(AD),2) + pow(seg(BC),2)]]를 구하시오."),
    choices=None, derived_answer="69",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 왼쪽 위, D 위 오른쪽, B 왼쪽 아래, C 오른쪽 아래), 대각선 교점 O에 직각 표시, AO=2·BO=4·CD=7 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "대각선 직교 사각형 도형",
    note="AB²=4+16=20, AD²+BC²=AB²+CD²=20+49=69 = 빠른정답 ✓.")

# p13
add(id="2ff3669a", qtype="short",
    question=("다음 그림에서 [[angle(AOD) = deg(90)]]이고 [[seg(AD) = 10]] cm, [[seg(BC) = 8]] cm일 때, "
              "[[pow(x,2) + pow(y,2)]]의 값을 구하시오."),
    choices=None, derived_answer="164",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 왼쪽 위, D 오른쪽, B 왼쪽 아래, C 오른쪽 아래), 대각선 교점 O에 직각 표시, AB=x cm·CD=y cm·AD=10cm·BC=8cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "대각선 직교 사각형 도형(x=AB, y=CD는 그림에만 있음)",
    note="x²+y²=AB²+CD²=AD²+BC²=100+64=164. 빠른정답 19와 불일치(정렬 어긋남 의심).")

# p15
add(id="2e8a3130", qtype="short",
    question=("다음 그림과 같이 두 대각선이 직교하는 [[quad(ABCD)]]에서 [[seg(BC) = 6]], [[seg(DA) = 4]]일 때, "
              "다음 □ 안에 알맞은 수를 써넣으시오.\n[[pow(seg(AB),2) + pow(seg(CD),2)]] = □"),
    choices=None, derived_answer="52",
    figure=[{"fn": "unsupported", "args": {"raw": "마름모꼴 사각형 ABCD(A 위, B 왼쪽, C 아래, D 오른쪽), 대각선 AC·BD 직교(교점에 직각 표시), AD=4·BC=6 치수(점선 호); 아래 상자 안에 AB²+CD²=□"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "대각선 직교 사각형 도형",
    note="AB²+CD²=BC²+DA²=36+16=52. 빠른정답 69와 불일치(정렬 어긋남 의심).")

# p19
add(id="30f9bcfe", qtype="choice",
    question=("다음 그림에서 [[seg(AB) = 10]] cm, [[seg(BC) = 5]] cm, [[seg(DA) = 9]] cm일 때, [[pow(seg(CD),2)]]의 길이는?"),
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 위, B 아래 왼쪽, C 아래 오른쪽, D 오른쪽 중간), B에 직각 표시(AB⊥BC), 대각선 AC·BD의 교점에 직각 표시(AC⊥BD), AB=10cm·BC=5cm·DA=9cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.75,
    needs_review=REV_FIG + "대각선 직교 사각형 도형(직교 조건은 그림에만 있음)",
    note="AC⊥BD → AB²+CD²=BC²+DA² → CD²=25+81−100=6 → ④. 원문 'CD²의 길이는?' 그대로. 빠른정답 54와 불일치(정렬 어긋남 의심).")

# p23
add(id="d62312b2", qtype="choice",
    question=("다음 그림과 같이 직사각형 ABCD의 내부에 있는 점 P에 대하여 [[seg(AP) = 3]], [[seg(CP) = 6]], [[seg(DP) = 5]]일 때, "
              "[[pow(x,2)]]의 값은?"),
    choices=["[[18]]", "[[20]]", "[[22]]", "[[24]]", "[[26]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내부의 점 P와 네 꼭짓점을 잇는 선분, AP=3·DP=5·CP=6·BP=x 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직사각형 내부 점 도형(x=BP는 그림에만 있음)",
    note="x²=AP²+CP²−DP²=9+36−25=20 → ② = 빠른정답 ✓.")

# p25
add(id="1d649407", qtype="short",
    question=("다음 그림과 같이 직사각형 ABCD의 내부의 한 점 P에 대하여 [[seg(AP) = 3]] cm, [[seg(CP) = 12]] cm, [[seg(DP) = 9]] cm이고 "
              "[[angle(APB) = deg(90)]]일 때, [[seg(AB)]]의 길이를 구하시오."),
    choices=None, derived_answer="9 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 윗변 가까이 내부의 점 P(P에 직각 표시), 선분 PA·PB·PC·PD, AP=3cm·DP=9cm·CP=12cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직사각형 내부 점 도형",
    note="BP²=9+144−81=72, AB²=9+72=81 → AB=9 cm. 빠른정답 24와 불일치(정렬 어긋남 의심).")

# p26
add(id="294efe41", qtype="short",
    question=("다음 그림과 같이 직사각형 ABCD의 내부에 한 점 P가 있다. [[seg(BP) = 4]], [[seg(CP) = 3]]일 때, "
              "[[pow(seg(AP),2) - pow(seg(DP),2)]]의 값을 구하시오."),
    choices=None, derived_answer="7",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내부의 점 P와 네 꼭짓점을 잇는 선분, BP=4·CP=3 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직사각형 내부 점 도형",
    note="AP²−DP²=BP²−CP²=16−9=7. 원문은 'AP²−DP²' 전체에 윗줄. 빠른정답 2와 불일치(정렬 어긋남 의심).")

# p27
add(id="b812407e", qtype="short",
    question=("다음 그림과 같이 직사각형 ABCD의 내부의 한 점 P에 대하여 [[seg(AP) = 4]], [[seg(CP) = 10]]일 때, "
              "[[pow(seg(BP),2) + pow(seg(DP),2)]]의 값을 구하시오."),
    choices=None, derived_answer="116",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내부의 점 P와 네 꼭짓점을 잇는 선분, AP=4·CP=10 치수(점선 호)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "직사각형 내부 점 도형",
    note="BP²+DP²=AP²+CP²=16+100=116. 빠른정답 10과 불일치(정렬 어긋남 의심).")

# p31
add(id="54a064d9", qtype="choice",
    question=("다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC의 세 변 AB, BC, CA를 각각 지름으로 하는 세 반원의 넓이를 각각 "
              "[[sub(S,1)]], [[sub(S,2)]], [[sub(S,3)]]이라 하자. [[sub(S,3) = 8 pi]] cm²일 때, [[sub(S,1) + sub(S,2) + sub(S,3)]]의 값은?"),
    choices=["[[10 pi]] cm²", "[[12 pi]] cm²", "[[14 pi]] cm²", "[[16 pi]] cm²", "[[18 pi]] cm²"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, B 왼쪽 아래 직각 표시, C 오른쪽 아래), AB 왼쪽 반원 S₁, BC 아래 반원 S₂, CA 오른쪽 위 반원 S₃, 반원 분홍 음영"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형 세 반원 도형",
    note="S₁+S₂=S₃=8π → 합 16π cm² → ④. 빠른정답 193과 불일치(정렬 어긋남 의심).")

# p40
add(id="3cf6220a", qtype="short",
    question=("다음 그림은 [[angle(B) = deg(90)]]인 직각삼각형 ABC의 세 변을 각각 지름으로 하는 반원을 그린 것이다. "
              "[[seg(AB)]], [[seg(AC)]]를 지름으로 하는 반원의 넓이가 각각 [[8 pi]] cm², [[frac(25,2) pi]] cm²일 때, "
              "[[tri(ABC)]]의 넓이를 구하시오."),
    choices=None, derived_answer="24 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, B 왼쪽 아래 직각 표시, C 오른쪽 아래, 삼각형 음영), AB 왼쪽 반원(8π cm²), AC 오른쪽 반원(25/2 π cm²), BC 아래 반원"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형 세 반원 도형",
    note="AB²/8=8 → AB=8, AC²/8=25/2 → AC=10, BC=6 → 넓이 24 cm². 빠른정답 4와 불일치(정렬 어긋남 의심).")

# p41
add(id="4ed8d459", qtype="short",
    question=("다음 그림에서 [[tri(ABO)]]는 [[seg(OB) = 16]] cm인 직각이등변삼각형이다. 점 O를 중심으로 하고 [[seg(OB)]]를 반지름으로 하는 사분원과 "
              "[[seg(AB)]]를 지름으로 하는 반원을 그렸을 때 만들어지는 도형의 넓이를 [[sub(S,1)]], [[tri(ABO)]]의 넓이를 [[sub(S,2)]]라 할 때, "
              "[[sub(S,1) + sub(S,2)]]의 값을 구하시오."),
    choices=None, derived_answer="256",
    figure=[{"fn": "unsupported", "args": {"raw": "직각이등변삼각형 ABO(O 오른쪽 아래 직각 표시, B 왼쪽 아래, A 오른쪽 위, OA=OB 등호 표시, OB=16cm 치수), O 중심 사분원 호 BA와 AB를 지름으로 하는 반원 사이의 초승달 모양 S₁(분홍), 삼각형 S₂(하늘색)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "사분원·반원·삼각형 복합 도형",
    note="히포크라테스: S₁=S₂=½·16·16=128 → S₁+S₂=256. 빠른정답 없음.")

# p45
add(id="f1867113", qtype="short",
    question=("다음 그림은 직각삼각형 ABC에서 [[seg(AB)]], [[seg(AC)]], [[seg(BC)]]를 각각 지름으로 하는 반원을 그린 것이다. "
              "색칠한 부분의 넓이가 40일 때, [[pow(seg(BC),2)]]의 값을 구하시오."),
    choices=None, derived_answer="416",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 오른쪽 위 직각 표시, B 왼쪽 아래, C 오른쪽 아래), AB·AC를 지름으로 하는 반원과 BC를 지름으로 하는 반원 사이의 두 초승달 부분 음영, AC=4 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형 세 반원 도형(AC=4는 그림에만 있음)",
    note="색칠 부분=△ABC=½·AB·4=40 → AB=20, BC²=400+16=416. 빠른정답 13cm과 불일치(정렬 어긋남 의심).")

# p48
add(id="05b26b08", qtype="short",
    question=("다음 그림은 직사각형 ABCD의 각 변을 지름으로 하는 반원과 [[quad(ABCD)]]의 대각선을 지름으로 하는 원을 그린 것이다. "
              "[[sub(S,1) + sub(S,2) + sub(S,3) + sub(S,4)]]의 넓이를 구하시오."),
    choices=None, derived_answer="48 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "45° 기울어진 직사각형 ABCD(A 위, D 오른쪽, C 아래, B 왼쪽), 대각선 AC·BD를 지름으로 하는 원, 네 변 바깥의 반원과 원 사이 초승달 S₁(왼쪽 위)·S₂(오른쪽 위)·S₃(왼쪽 아래)·S₄(오른쪽 아래) 하늘색 음영, AD=6cm·AB=8cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직사각형·반원·원 복합 도형(AB=8cm·AD=6cm는 그림에만 있음)",
    note="초승달 넓이 합 = 직사각형 넓이 = 6·8 = 48 cm². 빠른정답 416과 불일치(정렬 어긋남 의심).")

# p50
add(id="32e64260", qtype="short",
    question=("다음 그림은 직각삼각형 ABC의 세 변을 각각 지름으로 하는 반원을 그린 것이다. [[seg(AB) = 6]] cm, [[seg(AC) = 9]] cm일 때, "
              "색칠한 부분의 넓이를 구하시오."),
    choices=None, derived_answer="27 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위 직각 표시, B 왼쪽 아래, C 오른쪽 아래), AB·AC 반원과 BC 반원 사이 두 초승달 분홍 음영, AB=6cm·AC=9cm 치수(점선 호)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형 세 반원 도형",
    note="색칠 부분=△ABC=½·6·9=27 cm². 빠른정답 28과 불일치(정렬 어긋남 의심).")

# p57 (피타고라스 나무)
add(id="452fc2ef", qtype="short",
    question=("다음 그림은 직각삼각형 ABC의 세 변을 각각 한 변으로 하는 세 정사각형을 그리고 [[seg(DE)]], [[seg(HI)]]를 빗변으로 하는 직각삼각형 DJE, HKI를 그린 다음 "
              "다시 이 삼각형들의 나머지 두 변을 각각 한 변으로 하는 네 정사각형을 그린 것이다. [[seg(AB) = 6]] cm, [[seg(AC) = 8]] cm일 때, "
              "색칠한 부분의 넓이를 구하시오."),
    choices=None, derived_answer="300 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위 직각, B 왼쪽 아래, C 오른쪽 아래, AB=6cm·AC=8cm 치수), 아래 정사각형 BCGF, 왼쪽 정사각형 ABED, 오른쪽 정사각형 ACHI, DE 위 직각삼각형 DJE와 정사각형 JMLD·NOEJ, HI 위 직각삼각형 HKI와 정사각형 KSRI·QPHK; 정사각형 7개 분홍 음영, 삼각형은 흰색"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "피타고라스 나무 도형",
    note="정사각형 넓이 합 36+64+100+36+64=300 cm². 빠른정답 없음.")

# p64 (종이접기)
add(id="a522a616", qtype="short",
    question=("다음 그림은 직사각형 ABCD를 꼭짓점 B가 점 D에 오도록 접은 것이다. [[seg(AB) = 8]] cm, [[seg(QD) = 10]] cm일 때, "
              "[[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="16 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; A·B 쪽은 점선), 접는 선 PQ(P는 BC 위, Q는 AD 위), 접힌 꼭짓점 R(Q 위쪽, 직각 표시), 선분 RD·QD·PD, AB=8cm·QD=10cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직사각형 접기 도형",
    note="RD=AB=8, QR=AQ=6 → BC=AD=AQ+QD=16 cm = 빠른정답 ✓.")

# p74 (구·판)
add(id="c649c675", qtype="short",
    question=("다음 [그림 1]은 삼각형 모양의 구멍이 있는 판 P에 반지름의 길이가 5 cm인 구를 올려놓은 것이고 [그림 2]는 [그림 1]을 판 P의 윗면과 일치하는 면으로 자를 때 생기는 단면을 나타낸 것이다. "
              "[[seg(AB) = 8]] cm, [[seg(BC) = 15]] cm, [[seg(CA) = 17]] cm이고 [[tri(ABC)]]의 넓이는 60 cm²이다. "
              "[그림 1]의 판 P의 윗면에 구멍이 없다고 할 때, 윗면에서 구의 가장 높은 점까지의 거리를 구하시오."),
    choices=None, derived_answer="9 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "[그림 1] 삼각형 구멍 ABC가 있는 판 P 위에 놓인 구(중심 O); [그림 2] 직각삼각형 ABC(A 위, B 왼쪽 아래 직각, C 오른쪽 아래, AB=8cm·BC=15cm·CA=17cm 치수)와 내접원(반지름 점선 표시)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "구·판 입체도와 단면 내접원 도형",
    note="내접원 반지름 r=60/((8+15+17)/2)=3, 중심~윗면 거리 √(25−9)=4 → 4+5=9 cm. 빠른정답 4와 불일치(정렬 어긋남 의심).")

# p85 (직육면체 최단거리)
add(id="0aa154a6", qtype="short",
    question=("다음 그림과 같이 [[seg(BC) = seg(AD) = 10]], [[seg(AB) = 7]], [[seg(AE) = 4]] 인 직육면체의 한 꼭짓점 B에서 두 모서리 [[seg(CD)]], [[seg(GH)]]를 거쳐 "
              "꼭짓점 E에 이르는 최단 거리를 구하시오."),
    choices=None, derived_answer="25",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체 ABCD-EFGH(윗면 ABCD, 아랫면 EFGH, 하늘색), B에서 CD 위의 점을 거쳐 GH 위의 점을 지나 E에 이르는 경로(굵은 실선·점선)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직육면체 최단 경로 도형",
    note="전개: 가로 10+4+10=24, 세로 7 → √(24²+7²)=25. 빠른정답 20cm과 불일치(정렬 어긋남 의심).")

# p87
add(id="fcfd0032", qtype="short",
    question=("다음 그림과 같은 직육면체에서 [[seg(DH) = 9]] cm, [[seg(GH) = 4]] cm, [[seg(FG) = 4]] cm이다. 꼭짓점 B에서 출발하여 겉면을 따라 "
              "[[seg(CG)]], [[seg(DH)]]를 지나 점 E에 이르는 최단 거리를 구하시오."),
    choices=None, derived_answer="15 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "세로로 긴 직육면체 ABCD-EFGH(윗면 ABCD, 아랫면 EFGH, 보라색), B에서 CG·DH를 지나 E에 이르는 붉은 경로, DH=9cm·GH=4cm·FG=4cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직육면체 최단 경로 도형",
    note="옆면 전개: 가로 4+4+4=12, 세로 9 → √(144+81)=15 cm. 빠른정답 3과 불일치(정렬 어긋남 의심).")

# p94 (원뿔대)
add(id="78a716ff", qtype="short",
    question=("다음 그림과 같은 원뿔대에서 [[seg(AB) = 16]] cm, 윗면의 반지름의 길이는 4 cm, 밑면의 반지름의 길이는 8 cm이다. "
              "점 M이 모선 AB의 중점일 때, 점 B를 출발하여 원뿔대의 옆면을 따라 점 M에 이르는 최단 거리를 구하시오."),
    choices=None, derived_answer="40 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "원뿔대(윗면 반지름 4cm, 밑면 반지름 8cm, 분홍), 모선 AB=16cm(A 위, B 아래 왼쪽), AB의 중점 M, B에서 옆면을 한 바퀴 돌아 M에 이르는 곡선 경로"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "원뿔대 최단 경로 도형",
    note="전체 원뿔 모선 32, 전개 부채꼴 중심각 90°, OM=24 → √(32²+24²)=40 cm. 빠른정답 20cm과 불일치(정렬 어긋남 의심).")

# ════════════ 여러 가지 사각형 ════════════
# p9
add(id="60f5f5b9", qtype="choice",
    question="다음 그림의 평행사변형 ABCD가 직사각형이 되기 위한 조건이 아닌 것은? (단, 점 O 는 두 대각선의 교점이다.)",
    choices=["[[seg(AC) = seg(BD)]]", "[[seg(AO) = seg(BO)]]", "[[angle(B) = angle(D)]]", "[[angle(C) = angle(D)]]", "[[angle(A) = deg(90)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", 두 대각선 AC·BD와 교점 O"}}],
    difficulty_est=2, confidence=0.85,
    note="∠B=∠D는 평행사변형이면 항상 성립 → 조건 아님 ③. 빠른정답 없음.")

# p16
add(id="3a487c37", qtype="choice",
    question="다음 그림과 같은 마름모 ABCD에서 [[seg(AO) = 4]], [[seg(DO) = 5]]일 때, 마름모의 넓이는?",
    choices=["[[25]]", "[[30]]", "[[35]]", "[[40]]", "[[45]]"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "마름모 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 두 대각선의 교점 O, AO=4·DO=5 치수(점선 호)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "마름모 대각선 치수 도형",
    note="넓이 ½·8·10=40 → ④. 빠른정답 없음.")

# p17
add(id="5f11b856", qtype="short",
    question=("다음 그림과 같은 마름모 ABCD에서 두 대각선의 교점을 O라 하자. [[seg(BC) = 12]] cm, [[angle(OCB) = deg(30)]]일 때, "
              "[[x - y]]의 값을 구하시오."),
    choices=None, derived_answer="6",
    figure=[{"fn": "unsupported", "args": {"raw": "마름모 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 교점 O, DC=x cm·DO=y cm·BC=12cm 치수(점선 호), C에 30° 표시(∠OCB)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "마름모 치수 도형(x=DC, y=DO는 그림에만 있음)",
    note="x=CD=12, △BCD 정삼각형 → BD=12, y=DO=6 → x−y=6. 빠른정답 2와 불일치(정렬 어긋남 의심).")

# p19
add(id="c6c2b00f", qtype="short",
    question="다음 그림과 같은 평행사변형 ABCD에서 대각선 AC가 [[angle(A)]]의 이등분선일 때, [[quad(ABCD)]]는 어떤 사각형인지 말하시오.",
    choices=None, derived_answer="마름모",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", 대각선 AC, A에서 ∠BAC=∠CAD 표시(작은 원 2개)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "평행사변형 각의 이등분선 도형",
    note="∠BAC=∠DAC=∠BCA → AB=BC → 마름모. 빠른정답 4와 불일치(정렬 어긋남 의심).")

# p20
add(id="bd75e867", qtype="choice",
    question="다음 그림과 같은 평행사변형 ABCD에서 [[seg(AD) = 4]] cm, [[angle(ACB) = angle(ACD)]]일 때, [[quad(ABCD)]]의 둘레는?",
    choices=["[[12]] cm", "[[13]] cm", "[[14]] cm", "[[15]] cm", "[[16]] cm"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", 대각선 AC, C에서 ∠ACB=∠ACD 표시(점 2개)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "평행사변형 각의 이등분선 도형",
    note="마름모 → 둘레 4·4=16 cm → ⑤. 빠른정답 6과 불일치(정렬 어긋남 의심).")

# p21
add(id="413e7081", qtype="short",
    question="다음 그림의 평행사변형 ABCD에서 [[angle(DAC) = deg(60)]], [[angle(DBC) = deg(30)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(30)",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", 두 대각선 AC·BD와 교점 O, A에 60°(∠DAC), B에 30°(∠DBC), D에 x(∠BDC 위치) 표시"}}],
    difficulty_est=2, confidence=0.75,
    needs_review=REV_FIG + "평행사변형 대각선 각 도형(x의 위치는 그림에만 있음)",
    note="∠ACB=60°, ∠OBC=30° → AC⊥BD → 마름모 → ∠BDC=∠DBC=30°. 빠른정답 14와 불일치(정렬 어긋남 의심).")

# p26
add(id="a45ddb70", qtype="choice",
    question="다음 그림과 같은 직사각형 ABCD에서 [[quad(PQRS)]]는 정사각형이고 [[angle(DPS) = deg(25)]]일 때, [[angle(QBR)]]의 크기는?",
    choices=["[[deg(15)]]", "[[deg(18)]]", "[[deg(20)]]", "[[deg(22)]]", "[[deg(25)]]"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "가로로 긴 직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 BD, AD 위의 점 P·BC 위의 점 R·BD 위의 점 Q, S로 이루어진 정사각형 PQRS(변 등호·직각 표시), P에 25° 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직사각형 안 정사각형 도형",
    note="∠PSD=135°, ∠PDS=180−25−135=20° → ∠QBR=∠PDB=20°(엇각) → ③. 빠른정답 194와 불일치(정렬 어긋남 의심).")

# p31
add(id="1598e0d6", qtype="choice",
    question="다음 그림의 평행사변형 ABCD가 정사각형이 되기 위한 조건을 모두 고르면? (정답 2개)",
    choices=["[[perp(seg(AC), seg(DB))]], [[angle(ABC) = deg(90)]]",
             "[[seg(AO) = seg(BO)]], [[angle(ADO) = angle(DAO)]]",
             "[[perp(seg(AC), seg(DB))]], [[seg(AB) = seg(AD)]]",
             "[[seg(OA) = seg(OD)]], [[seg(AB) = seg(AD)]]",
             "[[seg(AC) = seg(DB)]], [[angle(ABC) = deg(90)]]"],
    derived_answer="①, ④",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", 두 대각선 AC·BD와 교점 O"}}],
    difficulty_est=2, confidence=0.85,
    note="①(마름모+직사각형)·④(직사각형+마름모) → 정사각형. ②⑤ 직사각형, ③ 마름모. 빠른정답 60과 불일치(정렬 어긋남 의심).")

# p32 (도형 없음)
add(id="316c7250", qtype="choice",
    question="다음 중 평행사변형 ABCD가 정사각형이 되기 위한 조건은? (단, 점 O는 두 대각선의 교점이다.)",
    choices=["[[angle(A) + angle(C) = deg(180)]]", "[[perp(seg(AC), seg(BD))]]",
             "[[seg(AB) = seg(AD)]], [[seg(AB) = seg(BC)]]", "[[seg(AO) = seg(CO)]], [[seg(BO) = seg(DO)]]",
             "[[angle(A) = deg(90)]], [[seg(AB) = seg(BC)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="⑤ 직사각형+마름모 → 정사각형. 빠른정답 4와 불일치(정렬 어긋남 의심).")

# p34
add(id="6b67cdab", qtype="choice",
    question="다음 그림의 평행사변형 ABCD가 다음 조건을 만족할 때, 정사각형이 되는 것은?",
    choices=["[[perp(seg(AC), seg(BC))]]", "[[angle(A) = deg(90)]], [[seg(AC) = seg(BD)]]",
             "[[seg(AB) = seg(DC)]], [[seg(AC) = seg(BD)]]", "[[angle(A) = deg(90)]], [[perp(seg(AC), seg(BD))]]",
             "[[par(seg(AD), seg(BC))]], [[seg(AC) = seg(BD)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + " 외곽선만"}}],
    difficulty_est=2, confidence=0.85,
    note="④ 직사각형+마름모 → 정사각형. 빠른정답 '1, 4'와 불일치(정렬 어긋남 의심).")

# p39
add(id="0572aaae", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD에서 [[seg(AB) = seg(AD)]]이고 [[angle(DBC) = deg(35)]]일 때, "
              "[[angle(BAC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(75)",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", 두 대각선 AC·BD와 교점 O, AB·AD 등호 표시, B에 35° 표시(∠DBC), A에 각 표시(∠BAC)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 대각선 각 도형",
    note="∠ABD=∠ADB=35°, ∠B=70°, ∠ACB=35° → ∠BAC=75°. 빠른정답 4와 불일치(정렬 어긋남 의심).")

# p40
add(id="c0198f15", qtype="short",
    question=("다음 그림의 등변사다리꼴 ABCD에서 [[seg(AB) = seg(AD) = seg(DC)]]이고 [[angle(ACD) = deg(30)]]일 때, "
              "[[angle(B)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", 대각선 AC, AB·AD·DC 등호 표시, C에 30° 표시(∠ACD), B에 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 대각선 각 도형",
    note="∠DAC=∠DCA=30°=∠ACB → ∠C=60°=∠B. 빠른정답 11 cm과 불일치(정렬 어긋남 의심).")

# p41
add(id="bfe26396", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD에서 [[seg(AB) = seg(AD)]]이고 [[angle(C) = deg(70)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(35)",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", 대각선 BD, AB·AD 등호 표시, D에 x 표시(∠ADB), C에 70° 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 대각선 각 도형(x=∠ADB는 그림에만 있음)",
    note="∠B=70°, ∠ABD=∠ADB=∠DBC → x=35°. 빠른정답 10과 불일치(정렬 어긋남 의심).")

# p43
add(id="e3927296", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD에서 [[seg(AD) = 10]] cm, [[seg(CD) = 14]] cm, "
              "[[angle(A) = deg(120)]]일 때, [[quad(ABCD)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="62 cm",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", A에 120° 표시, AD=10cm·CD=14cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 치수 도형",
    note="∠B=∠C=60°, BC=10+14=24 → 둘레 14+24+14+10=62 cm. 빠른정답 60과 불일치(정렬 어긋남 의심).")

# p45
add(id="bd5b3b22", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD에서 [[seg(AB) = seg(AD) = seg(CD)]]이고 [[seg(BC) = 2 seg(AD)]]일 때, "
              "[[angle(BAC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(90)",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", 대각선 AC, AB·AD·CD 등호 표시, A에 각 표시(∠BAC)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 대각선 각 도형",
    note="BC 중점 E: AE=BE=EC → ∠BAC=90°. 빠른정답 5와 불일치(정렬 어긋남 의심).")

# p46
add(id="f1a6007f", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 [[par(seg(AD), seg(BC))]]인 사다리꼴이다. [[seg(AB) = seg(AD) = seg(CD) = frac(1,2) seg(BC)]]일 때, "
              "[[angle(DBC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(30)",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", 대각선 BD, AB·AD·CD 등호 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 대각선 도형",
    note="∠B=60°, AB=AD → ∠ABD=∠ADB=∠DBC → ∠DBC=30°. 빠른정답 62 cm과 불일치(정렬 어긋남 의심).")

# p47
add(id="ec9c8f28", qtype="short",
    question=("다음 그림과 같은 등변사다리꼴 ABCD에서 [[seg(AB) = seg(AD)]]이고 [[seg(BC) = 2 seg(AD)]]일 때, [[angle(C)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", AD=4cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 치수 도형",
    note="AB=AD=CD=BC/2 → △DEC 정삼각형(E는 BC 중점) → ∠C=60°. 빠른정답 26 cm과 불일치(정렬 어긋남 의심).")

# p49
add(id="74d045e2", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD의 꼭짓점 A에서 [[seg(BC)]]에 내린 수선의 발을 E라 하자. "
              "[[seg(AD) = 8]] cm, [[seg(BE) = 3]] cm일 때, [[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="14 cm",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", A에서 BC에 내린 수선 AE(E에 직각 표시), AD=8cm·BE=3cm 치수(점선 호)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 수선 도형",
    note="BC=3+8+3=14 cm = 빠른정답 ✓.")

# p50
add(id="094c6bdf", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD에서 두 대각선의 교점을 O, 점 O를 지나고 [[seg(CD)]]에 수직인 직선이 "
              "[[seg(AB)]], [[seg(CD)]]와 만나는 점을 각각 E, F라 하고 점 A에서 [[seg(BC)]]에 내린 수선의 발을 G라 하자. "
              "[[angle(AOD) = deg(90)]], [[seg(AB) = 10]] cm, [[seg(AD) = 2]] cm, [[seg(BC) = 14]] cm일 때, [[seg(EO) + seg(BG)]]의 길이를 구하시오."),
    choices=None, derived_answer="11 cm",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + "(윗변이 짧음), 두 대각선과 교점 O(직각 표시), O를 지나 CD에 수직인 선분 EF(E는 AB 위, F는 CD 위 직각 표시), A에서 BC에 내린 수선 AG(G에 직각 표시), AB=10cm·AD=2cm·BC=14cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 대각선·수선 복합 도형",
    note="BG=(14−2)/2=6, E는 AB의 중점(∠AOB=90°) → EO=AB/2=5 → 11 cm = 빠른정답 ✓.")

# p51
add(id="e1fa8e01", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD에서 두 대각선의 교점을 O, 점 O를 지나고 [[seg(CD)]]에 수직인 직선이 "
              "[[seg(AB)]], [[seg(CD)]]와 만나는 점을 각각 E, F라 하고 점 A에서 [[seg(BC)]]에 내린 수선의 발을 G라 하자. "
              "[[angle(AOD) = deg(90)]], [[seg(AB) = 13]] cm, [[seg(AD) = 7]] cm, [[seg(BC) = 17]] cm일 때, [[seg(EO) + seg(BG)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(23,2) cm",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", 두 대각선과 교점 O(직각 표시), O를 지나 CD에 수직인 선분 EF(E는 AB 위, F는 CD 위 직각 표시), A에서 BC에 내린 수선 AG(G에 직각 표시), AB=13cm·AD=7cm·BC=17cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 대각선·수선 복합 도형",
    note="BG=(17−7)/2=5, EO=AB/2=13/2 → 23/2 cm. 빠른정답 없음.")

# p53
add(id="aaf32b0b", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD의 꼭짓점 A에서 [[seg(BC)]]에 내린 수선의 발을 E라 하자. "
              "[[angle(C) = deg(65)]]일 때, [[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(140)",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP + ", 수선 AE(E에 직각 표시), A에 x(∠BAE)·D에 y(∠ADC) 표시, C에 65° 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "등변사다리꼴 수선 각 도형(x=∠BAE, y=∠ADC는 그림에만 있음)",
    note="∠B=65° → x=25°, y=180−65=115° → 140° = 빠른정답 ✓.")

# p54
add(id="d5239b4c", qtype="short",
    question="다음 그림과 같은 평행사변형 ABCD가 [[seg(CO) = seg(DO)]]를 만족시키면 어떤 사각형이 되는지 말하시오. (단, 점 O는 두 대각선의 교점이다.)",
    choices=None, derived_answer="직사각형",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", 두 대각선 AC·BD와 교점 O"}}],
    difficulty_est=1, confidence=0.85,
    note="CO=DO → AC=BD → 직사각형 = 빠른정답 ✓.")

# p55
add(id="260d70ea", qtype="short",
    question="다음 그림과 같은 평행사변형 ABCD가 [[seg(AD) = seg(CD)]]를 만족하면 어떤 사각형이 되는지 구하시오.",
    choices=None, derived_answer="마름모",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + " 외곽선만"}}],
    difficulty_est=1, confidence=0.85,
    note="이웃한 두 변이 같은 평행사변형 → 마름모. 빠른정답 1과 불일치(정렬 어긋남 의심).")

# p56
add(id="b4d1e9f5", qtype="short",
    question=("다음 그림과 같은 직사각형 ABCD에서 대각선 BD의 수직이등분선이 [[seg(AD)]], [[seg(BC)]]와 만나는 점을 각각 E, F라 하자. "
              "[[seg(AE) = 5]] cm, [[seg(BC) = 12]] cm일 때, [[quad(BFDE)]]의 둘레의 길이를 구하시오.\n(단, O는 [[seg(BD)]]와 [[seg(EF)]]의 교점이다.)"),
    choices=None, derived_answer="28 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "가로로 긴 직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 BD, BD의 수직이등분선 EF(E는 AD 위, F는 BC 위, 교점 O에 직각·등호 표시), 선분 BE·DF, AE=5cm·BC=12cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직사각형·수직이등분선 도형",
    note="□BFDE는 마름모, ED=12−5=7 → 둘레 28 cm. 빠른정답 140과 불일치(정렬 어긋남 의심).")

# p57
add(id="0f95ff8c", qtype="short",
    question=("다음 그림과 같이 정사각형 ABCD의 각 변 위에 [[seg(EB) = seg(FC) = seg(GD) = seg(HA)]]가 되도록 점 E, F, G, H를 잡을 때, "
              "[[quad(EFGH)]]는 어떤 사각형인지 말하시오."),
    choices=None, derived_answer="정사각형",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB 위 E·BC 위 F·CD 위 G·DA 위 H, 사각형 EFGH, EB·FC·GD·HA 등호 표시"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "정사각형 안 사각형 도형",
    note="네 직각삼각형 합동 → EF=FG=GH=HE, ∠HEF=90° → 정사각형. 빠른정답 '직사각형'과 불일치.")

# p67
add(id="b8f9ed69", qtype="short",
    question=("다음 그림에서 [[par(l, m)]]일 때, (가) ~ (마)의 사각형 중 두 대각선의 길이가 같은 것은 [[a]]개, "
              "두 대각선이 서로를 수직이등분하는 것은 [[b]]개이다. [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="5",
    figure=[{"fn": "unsupported", "args": {"raw": "평행선 l(위)·m(아래) 사이의 초록 사각형 5개: (가) 평행사변형(양 옆변 화살표), (나) 직사각형(직각 4개), (다) 정사각형(직각 4개·변 등호), (라) 등변사다리꼴(밑각 점 표시), (마) 마름모(네 변 등호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "다섯 사각형 표시 도형",
    note="a=3(직사각형·정사각형·등변사다리꼴), b=2(정사각형·마름모) → 5 = 빠른정답 ✓.")

# p68
add(id="5511b0ed", qtype="short",
    question=("다음 그림에서 [[par(l, m)]]일 때, (가) ~ (마)의 사각형 중 두 대각선의 길이가 같은 것은 [[a]]개, 두 대각선이 서로를 이등분하는 것은 [[b]]개, "
              "두 대각선이 서로를 수직이등분하는 것은 [[c]]개이다. [[a - b + c]]의 값을 구하시오."),
    choices=None, derived_answer="1",
    figure=[{"fn": "unsupported", "args": {"raw": "평행선 l(위)·m(아래) 사이의 보라 사각형 5개: (가) 평행사변형(양 옆변 화살표), (나) 직사각형(직각 4개), (다) 정사각형(직각 4개·변 등호), (라) 등변사다리꼴(밑각 점 표시), (마) 마름모(네 변 등호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "다섯 사각형 표시 도형",
    note="a=3, b=4(평행사변형·직사각형·정사각형·마름모), c=2 → 3−4+2=1 = 빠른정답 ✓.")

# p73
add(id="9ff9fad9", qtype="choice",
    question="다음 그림과 같이 정사각형 ABCD 의 네 변의 중점을 연결하여 만든 사각형의 성질이 아닌 것은?",
    choices=["네 변의 길이가 모두 같다.", "두 대각선의 길이는 다르다.", "네 각의 크기가 모두 같다.",
             "두 대각선이 서로 수직이등분한다.", "두 쌍의 대변이 각각 평행하다."],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 네 변의 중점 H(AD)·G(DC)·F(BC)·E(AB)를 이은 사각형 EFGH"}}],
    difficulty_est=1, confidence=0.85,
    note="중점 연결 사각형은 정사각형 → 대각선 길이 같음 → ②가 성질 아님 = 빠른정답 ✓.")

# p77
add(id="ee28483d", qtype="choice",
    question="다음 그림과 같이 [[par(seg(AC), seg(DE))]]일 때, 서로 넓이가 같은 도형끼리 짝 지은 것으로 옳지 않은 것은?",
    choices=["[[tri(ADE) = tri(DCE)]]", "[[tri(AFD) = tri(FCE)]]", "[[quad(ABCD) = tri(ABE)]]",
             "[[tri(ACD) = tri(ACE)]]", "[[tri(ACF) = tri(DFE)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 위, D 오른쪽 위, B 왼쪽 아래, C 아래)와 BC의 연장선 위의 점 E, 선분 AC·DE(평행 화살표)·AE·CD, AE와 CD의 교점 F"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "평행선과 삼각형 넓이 도형",
    note="AC∥DE → △ACD=△ACE, △AFD=△FCE, □ABCD=△ABE, △ADE=△DCE 모두 성립; ⑤는 근거 없음 → ⑤ = 빠른정답 ✓.")

# p78
add(id="31352e65", qtype="choice",
    question="아래 그림의 [[quad(ABCD)]]에서 [[par(seg(AC), seg(DE))]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[tri(AFD) = tri(DFE)]]", "[[tri(ACD) = tri(ACE)]]", "[[tri(ADF) = tri(CEF)]]",
             "[[tri(AED) = tri(CED)]]", "[[quad(ABCD) = tri(ABE)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 위, D 오른쪽 위, B 왼쪽 아래, C 아래)와 BC의 연장선 위의 점 E, 선분 AC·DE(평행 화살표)·AE·CD, AE와 CD의 교점 F"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "평행선과 삼각형 넓이 도형",
    note="①은 근거 없음, 나머지는 AC∥DE에서 성립 → ① = 빠른정답 ✓.")

# p81
add(id="471eb087", qtype="short",
    question="다음 그림에서 [[par(l, m)]]이고 [[seg(BC) = 12]], [[seg(DH) = 7]]일 때, [[tri(ABC)]]의 넓이를 구하시오.",
    choices=None, derived_answer="42",
    figure=[{"fn": "unsupported", "args": {"raw": "평행선 l(위, A·D)·m(아래, B·H·C), 삼각형 ABC(분홍 음영), 선분 DB·DC, D에서 m에 내린 수선 DH=7(직각 표시), BC=12 치수(점선 호)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "평행선과 삼각형 넓이 도형",
    note="△ABC=△DBC=½·12·7=42. 빠른정답 1과 불일치(정렬 어긋남 의심).")

# p85
add(id="f6d99d16", qtype="choice",
    question=("다음 그림과 같이 [[tri(ABC)]]에서 [[ratio(seg(BD), seg(DC)) = ratio(3, 5)]]이고, [[tri(ABC)]]의 넓이가 56 cm²일 때, "
              "[[tri(ADC)]]의 넓이는?"),
    choices=["[[30]] cm²", "[[32]] cm²", "[[35]] cm²", "[[38]] cm²", "[[40]] cm²"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), BC 위의 점 D, 선분 AD, △ADC 음영"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "삼각형 넓이 비 도형",
    note="△ADC=56·5/8=35 cm² → ③. 빠른정답 45와 불일치(정렬 어긋남 의심).")

# p89
add(id="5699ef42", qtype="choice",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[par(seg(EF), seg(BD))]]이고, [[ratio(seg(AF), seg(FD)) = ratio(2, 3)]]이다. "
              "[[quad(ABCD)]]의 넓이가 40 cm²일 때, [[tri(DEB)]]의 넓이는?"),
    choices=["[[8]] cm²", "[[10]] cm²", "[[12]] cm²", "[[15]] cm²", "[[18]] cm²"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", AB 위의 점 E와 AD 위의 점 F를 잇는 선분 EF(BD와 평행 화살표), 대각선 BD, 선분 ED, △DEB 초록 음영"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "평행사변형·평행선 넓이 도형",
    note="△DEB=△DFB=(3/5)·△ABD=(3/5)·20=12 cm² → ③. 빠른정답 2와 불일치(정렬 어긋남 의심).")

# p93
add(id="7e22eaa4", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[ratio(seg(DE), seg(EC)) = ratio(7, 3)]]이고 [[seg(BC)]]의 연장선과 [[seg(AE)]]의 연장선의 교점을 F라 하자. "
              "[[quad(ABCD)]]의 넓이가 40 cm²일 때, [[tri(DEF)]]의 넓이를 구하시오."),
    choices=None, derived_answer="6 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", CD 위의 점 E, AE의 연장선과 BC의 연장선의 교점 F(C의 오른쪽), 선분 DF, △DEF 보라 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "평행사변형·연장선 교점 도형",
    note="△ADE=(7/10)·20=14, EF:AE=3:7 → △DEF=14·3/7=6 cm². 빠른정답 2와 불일치(정렬 어긋남 의심).")

# p96
add(id="41301c4a", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]] 인 사다리꼴 ABCD 에서 [[tri(DCO)]] 의 넓이가 40 일 때, "
              "[[tri(ABC)]] 의 넓이를 구하여라.\n(단, [[2 seg(AO) = seg(CO)]] )"),
    choices=None, derived_answer="120",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, AD∥BC), 두 대각선 AC·BD와 교점 O"}}],
    difficulty_est=2, confidence=0.85,
    note="△ABO=△DCO=40, AO:OC=1:2 → △OBC=80 → △ABC=120 = 빠른정답 ✓. 도형은 라벨만(치수 없음).")

# p97
add(id="4a1497b8", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 두 대각선의 교점을 O라 하자. [[tri(ABC)]]의 넓이가 36 cm², "
              "[[tri(DOC)]]의 넓이가 12 cm²일 때, [[tri(OBC)]]의 넓이를 구하시오."),
    choices=None, derived_answer="24 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, AD∥BC 화살표), 두 대각선 AC·BD와 교점 O, △OBC 하늘색 음영"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "사다리꼴 대각선 넓이 도형",
    note="△DBC=△ABC=36 → △OBC=36−12=24 cm². 빠른정답 없음.")

# p98
add(id="b5b9c4d9", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 두 대각선의 교점을 O라 하자. [[tri(ABO) = 6]] cm², "
              "[[tri(OBC) = 8]] cm²일 때, [[quad(ABCD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="frac(49,2) cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 두 대각선 AC·BD와 교점 O, 전체 분홍 음영"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "사다리꼴 대각선 넓이 도형",
    note="△DCO=6, AO:OC=3:4 → △AOD=6·3/4=9/2 → 합 6+8+6+9/2=49/2 cm². 빠른정답 없음.")

# ════════════ 삼각형의 외심과 내심 ════════════
# p4
add(id="f0a41362", qtype="choice",
    question="다음 그림에서 점 O는 [[tri(ABC)]]의 외심이고 [[angle(ABO) = deg(52)]], [[angle(BOC) = deg(154)]] 이다. [[angle(x)]]의 크기는?",
    choices=["[[deg(120)]]", "[[deg(125)]]", "[[deg(130)]]", "[[deg(135)]]", "[[deg(140)]]"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 내부의 외심 O와 선분 OA·OB·OC, B에 52°(∠ABO), O 아래쪽에 154°(∠BOC), O 오른쪽 위에 x(∠AOC) 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "삼각형 외심 각 도형(x=∠AOC는 그림에만 있음)",
    note="∠OBC=13°, ∠B=65° → ∠AOC=2∠B=130° → ③. 빠른정답 없음.")

# p7
add(id="9808710b", qtype="short",
    question=("다음 그림에서 점 O가 [[tri(ABC)]]의 외심이고 [[angle(OBA) = deg(54)]], [[angle(OCA) = deg(27)]]일 때, "
              "[[angle(BOC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(54)",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 오른쪽 위)와 삼각형 밖 왼쪽 위의 외심 O, 선분 OA·OB·OC, B에 54°(∠OBA), C에 27°(∠OCA) 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "둔각삼각형 외심 각 도형",
    note="∠BAC=54−27=27° → ∠BOC=54°. 빠른정답 없음.")

# p10
add(id="b8e596b2", qtype="short",
    question=("다음 그림에서 점 O가 [[tri(ABC)]]의 외심이고 [[angle(OBA) = deg(65)]], [[angle(OCA) = deg(25)]]일 때, "
              "[[angle(OBC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(50)",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 오른쪽 위)와 삼각형 밖 왼쪽 위의 외심 O, 선분 OA·OB·OC, B에 65°(∠OBA), C에 25°(∠OCA) 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "둔각삼각형 외심 각 도형",
    note="∠A=65−25=40°, ∠BOC=80° → ∠OBC=50°. 빠른정답 '54 deg(x)'와 불일치(정렬 어긋남 의심).")

# p12
add(id="b096e6cd", qtype="short",
    question=("다음 그림에서 점 O가 [[tri(ABC)]]의 외심이고 [[angle(OBA) = deg(48)]], [[angle(OCA) = deg(30)]]일 때, "
              "[[angle(OBC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(72)",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 오른쪽 위)와 삼각형 밖 위쪽의 외심 O, 선분 OA·OB·OC, B에 48°(∠OBA), C에 30°(∠OCA) 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "둔각삼각형 외심 각 도형",
    note="∠A=48−30=18°, ∠BOC=36° → ∠OBC=72°. 빠른정답 '118 deg(x)'와 불일치(정렬 어긋남 의심).")

# p13
add(id="e3711dad", qtype="short",
    question=("다음 그림과 같이 [[tri(ABC)]]의 꼭짓점 A에서 [[seg(BC)]]에 내린 수선의 발을 D라 하고 [[seg(AC)]]의 중점 M을 지나면서 [[seg(AB)]]에 평행한 직선과 "
              "[[seg(BC)]]의 교점을 E라 하자. [[angle(B) = 2 angle(C)]]이고 [[seg(AB) = 30]] cm, [[seg(ME) = 15]] cm일 때, "
              "[[seg(DE)]]의 길이를 구하시오."),
    choices=None, derived_answer="15 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 수선 AD(D에 직각 표시), AC의 중점 M(등호 표시), ME∥AB(화살표), AB=30cm·ME=15cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "삼각형 수선·중점 도형",
    note="M은 직각△ADC의 외심 → MD=MC, ∠MDE=∠C, ∠MEC=∠B=2∠C → ∠DME=∠C → DE=ME=15 cm. 빠른정답 '50 deg(x)'와 불일치(정렬 어긋남 의심).")

# p14
add(id="91e711ef", qtype="choice",
    question=("다음 그림에서 [[tri(ABC)]]는 [[angle(A) = deg(90)]]인 직각삼각형이다. 점 M은 [[seg(BC)]]의 중점이고 점 D는 점 A에서 [[seg(BC)]]에 내린 수선의 발, "
              "점 E는 점 D에서 [[seg(AM)]]에 내린 수선의 발이다. [[seg(AB) = 4]] cm, [[seg(AC) = 3]] cm, [[seg(BC) = 5]] cm, [[seg(BD) = frac(16,5)]] cm일 때, "
              "[[seg(DE)]]의 길이는?"),
    choices=["[[frac(76,125)]] cm", "[[frac(16,25)]] cm", "[[frac(84,125)]] cm", "[[frac(88,125)]] cm", "[[frac(92,125)]] cm"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위 직각 표시, B 왼쪽 아래, C 오른쪽 아래), BC의 중점 M(등호 표시), 수선 AD(D에 직각 표시), D에서 AM에 내린 수선 DE(E에 직각 표시), AB=4cm·AC=3cm·BC=5cm·BD=16/5cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형 외심·수선 복합 도형",
    note="AM=5/2, AD=12/5, DM=16/5−5/2=7/10 → DE=AD·DM/AM=84/125 cm → ③ = 빠른정답 ✓.")

# p17
add(id="1e141b9c", qtype="short",
    question="다음 그림에서 점 D는 [[angle(A) = deg(90)]]인 직각삼각형 ABC의 빗변의 중점이다. [[seg(BD) = 6]] cm일 때, [[seg(AD)]]의 길이를 구하시오.",
    choices=None, derived_answer="6 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위 직각 표시, B 왼쪽 아래, C 오른쪽 아래), 빗변 BC의 중점 D(BD·DC 등호 표시), 선분 AD, BD=6cm 치수(점선 호)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형 빗변 중점 도형",
    note="빗변의 중점은 외심 → AD=BD=6 cm. 빠른정답 3과 불일치(정렬 어긋남 의심).")
