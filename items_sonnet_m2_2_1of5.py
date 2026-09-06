# -*- coding: utf-8 -*-
# esc_sonnet_m2-2_1of5 — 이미지 기준 전사 (87 항목 / 80쪽) — 중2-2 삼각형의 무게중심·닮은 도형·이등변삼각형·삼각형의 닮음 조건
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
FIG = "도형 표현 불가: "
ISO = "이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)"
PAR = "평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)"
DEG5 = lambda a, b, c, d, e: [f"[[deg({a})]]", f"[[deg({b})]]", f"[[deg({c})]]", f"[[deg({d})]]", f"[[deg({e})]]"]

# ════════ 삼각형의 무게중심 ════════
# p5 — 등변사다리꼴 중점
add(id="421cfbdd", qtype="choice",
    question=("다음 그림과 같은 등변사다리꼴 ABCD에서 [[seg(AD)]], [[seg(BD)]], [[seg(BC)]]의 중점을 각각 P, Q, R라 하고 "
              "[[angle(ABD) = deg(30)]], [[angle(BDC) = deg(70)]]일 때, [[angle(QPR)]]의 크기는?"),
    choices=DEG5(10, 15, 20, 25, 30), derived_answer="③",
    figure=U("등변사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD의 중점 P, 대각선 BD의 중점 Q, BC의 중점 R, 선분 PQ·PR·BD, B에 30°·D에 70° 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "등변사다리꼴·중점 연결 도형",
    note="PQ=AB/2=DC/2=QR, ∠PQR=30°+110°=140° → ∠QPR=20° → ③ = 빠른정답 ✓.")

# p6 — 각의 이등분선에 내린 수선
add(id="9fa58943", qtype="short",
    question=("다음 그림과 같은 [[tri(ABC)]]의 점 B에서 [[angle(A)]]의 이등분선에 내린 수선의 발을 D라 하고 점 D를 지나고 [[seg(AC)]]에 평행한 직선과 "
              "[[seg(BC)]]의 교점을 E라 하자. [[seg(AB) = 10]] cm, [[seg(BE) = 6]] cm, [[seg(DE) = 4]] cm일 때, [[seg(AC) + seg(CE)]]의 길이를 구하시오."),
    choices=None, derived_answer="24 cm",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), A의 각 이등분선(A에 같은 각 표시)에 B에서 내린 수선의 발 D(직각 표시), D를 지나 AC에 평행한 선분 DE(E는 BC 위), AB=10 cm·BE=6 cm·DE=4 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·이등분선·수선 도형",
    note="BD의 연장선과 AC의 교점 F: AF=AB=10, D는 BF의 중점, DE∥FC → FC=8, AC=18, CE=BE=6 → 24 cm. 빠른정답 75와 불일치.")

# p7·p8·p9 — 평행사변형 각 변의 중점, QR
FIG_PQRS = (PAR + ", AB·BC·CD·DA의 중점 E·F·G·H, 선분 AG·BH·EC·DF가 만드는 내부 평행사변형 PQRS(P=AG∩BH, Q=BH∩EC, R=EC∩DF, S=DF∩AG)")
add(id="488aea10", qtype="short",
    question="다음 그림에서 평행사변형 ABCD의 각 변의 중점을 각각 E, F, G, H라 할 때, [[seg(AG) = 30]] cm, [[seg(BH) = 40]] cm이다. [[seg(QR)]]의 길이를 구하시오.",
    choices=None, derived_answer="12 cm", figure=U(FIG_PQRS),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·중점 연결 복합 도형",
    note="EC∥AG, EQ:QR:RC=1:2:2 → QR=(2/5)AG=12 cm. 빠른정답 5 cm와 불일치.")
add(id="c0d92a10", qtype="short",
    question="다음 그림에서 평행사변형 ABCD의 각 변의 중점을 각각 E, F, G, H라 할 때, [[seg(AG) = 25]] cm, [[seg(BH) = 35]] cm이다. [[seg(QR)]]의 길이를 구하시오.",
    choices=None, derived_answer="10 cm", figure=U(FIG_PQRS),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·중점 연결 복합 도형",
    note="QR=(2/5)AG=10 cm. 빠른정답 3과 불일치.")
add(id="da673307", qtype="short",
    question="다음 그림에서 평행사변형 ABCD의 각 변의 중점을 각각 E, F, G, H라 할 때, [[seg(AG) = 20]] cm, [[seg(BH) = 32]] cm이다. [[seg(QR)]]의 길이를 구하시오.",
    choices=None, derived_answer="8 cm", figure=U(FIG_PQRS),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·중점 연결 복합 도형",
    note="QR=(2/5)AG=8 cm. 빠른정답 24 cm와 불일치.")

# p13
add(id="6b2b34c4", qtype="short",
    question="다음 그림에서 [[seg(AB) = seg(BC)]], [[seg(BF) = seg(FE)]], [[seg(CD) = 7]] cm일 때, [[seg(CE)]]의 길이를 구하시오.",
    choices=None, derived_answer="frac(21,2) cm",
    figure=U("삼각형 ACE(A 위, C 왼쪽 아래, E 오른쪽 아래), AC의 중점 B(AB=BC 표시), CE 위의 점 D와 선분 AD, BE와 AD의 교점 F(BF=FE 표시), CD=7 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·중점 보조선 도형",
    note="B를 지나 CE에 평행한 선과 AD의 교점 G: BG=CD/2=7/2, △BGF≡△EDF → DE=7/2 → CE=21/2 cm. 빠른정답 없음.")

# p18
add(id="8526de31", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AC)]]의 중점을 D, [[seg(BD)]]의 중점을 E라 하고, [[seg(AE)]]의 연장선과 [[seg(BC)]]의 교점을 F라 하자. "
              "이때 [[ratio(seg(AE), seg(AF))]]를 가장 간단한 자연수의 비로 나타낸 것은?"),
    choices=["[[ratio(2,3)]]", "[[ratio(1,2)]]", "[[ratio(3,4)]]", "[[ratio(4,5)]]", "[[ratio(3,5)]]"], derived_answer="③",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AC의 중점 D(AD=DC 표시), BD의 중점 E(BE=ED 표시), AE의 연장선과 BC의 교점 F"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·중점 보조선 도형",
    note="D에서 AF에 평행한 선분 DG(G는 BC 위): DG=AF/2, EF=DG/2=AF/4 → AE:AF=3:4 → ③ = 빠른정답 ✓.")

# p27
add(id="8796205d", qtype="choice",
    question="아래 그림과 같은 [[tri(ABC)]]에서 세 점 D, E, F가 각각 [[seg(AB)]], [[seg(BC)]], [[seg(CA)]]의 중점일 때, 다음 중 옳지 않은 것은?",
    choices=["[[angle(BED) = angle(C)]]", "[[tri(ABC) = 4 tri(DEF)]]", "[[seg(DE) = seg(DF)]]", "[[par(seg(DE), seg(AC))]]", "[[angle(B) = angle(DFE)]]"],
    derived_answer="③",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 세 변의 중점 D(AB)·E(BC)·F(CA)와 삼각형 DEF, 같은 길이 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·중점 삼각형 도형",
    note="DE=AC/2, DF=BC/2로 일반적으로 다름 → ③. 빠른정답 4와 불일치.")

# p31
add(id="3b88abc0", qtype="short",
    question="다음 그림에서 사각형 ABCD의 각 변의 중점을 E, F, G, H라 할 때, [[seg(AC) = 10]], [[seg(BD) = 8]]이다. 사각형 EFGH의 둘레의 길이를 구하시오.",
    choices=None, derived_answer="18",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 각 변의 중점 E(AB)·F(BC)·G(CD)·H(DA)를 이은 사각형 EFGH, 대각선 AC·BD"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사각형·중점 사각형 도형",
    note="EF=HG=AC/2=5, EH=FG=BD/2=4 → 둘레 18. 빠른정답 54 cm와 불일치.")

# p32
add(id="4144ce3a", qtype="short",
    question="다음 그림에서 [[quad(ABCD)]]는 대각선의 길이가 [[15]] cm인 직사각형이다. 점 P, Q, R, S가 [[quad(ABCD)]]의 각 변의 중점일 때, [[quad(PQRS)]]의 둘레의 길이를 구하시오.",
    choices=None, derived_answer="30 cm",
    figure=U("직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 각 변의 중점 P(AB)·Q(BC)·R(CD)·S(DA)를 이은 마름모 PQRS, 대각선 AC(점선)에 15 cm 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직사각형·중점 사각형 도형",
    note="각 변 = 대각선/2 = 15/2 → 둘레 30 cm. 빠른정답 1과 불일치.")

# p33
add(id="698c5ed0", qtype="short",
    question="다음 그림과 같은 [[quad(ABCD)]]에서 네 변의 중점을 각각 E, F, G, H라 하자. [[quad(EFGH)]]의 둘레의 길이가 [[36]]일 때, [[seg(AC) + seg(BD)]]의 길이를 구하시오.",
    choices=None, derived_answer="36",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 각 변의 중점 E(AB)·F(BC)·G(CD)·H(DA)를 이은 사각형 EFGH, 대각선 AC·BD"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사각형·중점 사각형 도형",
    note="□EFGH의 둘레 = AC+BD → 36. 빠른정답 5와 불일치.")

# p41
add(id="3ed00bb7", qtype="short",
    question="다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 [[seg(AB)]], [[seg(DC)]]의 중점을 각각 M, N이라 할 때, [[seg(MQ)]]의 길이를 구하시오.",
    choices=None, derived_answer="10 cm",
    figure=U("사다리꼴 ABCD(AD 위, BC 아래), AD=14 cm·BC=20 cm 치수(점선 호), AB의 중점 M, DC의 중점 N, 대각선 AC·BD, MN과 BD의 교점 P, MN과 AC의 교점 Q"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사다리꼴·중점 연결 도형",
    note="△ABC에서 M은 AB의 중점, MQ∥BC → MQ=BC/2=10 cm. 빠른정답 9 cm와 불일치.")

# p42
add(id="569d1cda", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 두 점 M, N은 각각 [[seg(AB)]], [[seg(DC)]]의 중점이다. "
              "[[seg(AD) = 4]] cm, [[seg(MN) = 6]] cm일 때, [[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="8 cm",
    figure=U("사다리꼴 ABCD(AD 위, BC 아래, AD∥BC 화살표), AB의 중점 M·DC의 중점 N(같은 길이 표시), AD=4 cm·MN=6 cm 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "사다리꼴 치수 도형",
    note="MN=(AD+BC)/2 → BC=8 cm. 빠른정답 10과 불일치.")

# p45
add(id="92807a5c", qtype="short",
    question=("다음 그림의 [[tri(ABC)]]에서 [[seg(AD) = seg(DC)]], [[seg(AE) = seg(EF) = seg(FB)]]이다. 점 P가 [[seg(DF)]]와 [[seg(CE)]]의 교점일 때, "
              "[[tri(ABC)]]의 넓이는 [[tri(PCD)]]의 넓이의 몇 배인지 구하시오."),
    choices=None, derived_answer="9배",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AC의 중점 D, AB의 삼등분점 E(A 쪽)·F, 선분 DF와 CE의 교점 P, 같은 길이 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·분점 보조선 도형",
    note="좌표 계산: △PCD=△ABC/9 → 9배. 빠른정답 8 cm와 불일치.")

# p52
add(id="ffa05b4a", qtype="short",
    question="다음 그림에서 점 G가 [[tri(ABC)]]의 무게중심일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="5",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AC 위의 점 D와 중선 BD 위의 무게중심 G, AD=5·DC=x 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "삼각형·무게중심 치수 도형",
    note="D는 AC의 중점 → x=5. 빠른정답 12 cm와 불일치.")

# p53
add(id="cad2b88a", qtype="choice",
    question="다음 그림과 같은 [[tri(ABC)]]에서 두 중선 [[seg(AD)]], [[seg(BE)]]의 교점을 G라 하자. [[seg(AD) = 12]] cm일 때, [[seg(AG)]]의 길이는?",
    choices=["[[6]] cm", "[[frac(13,2)]] cm", "[[7]] cm", "[[frac(15,2)]] cm", "[[8]] cm"], derived_answer="⑤",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 중선 AD(D는 BC 위)·BE(E는 AC 위)의 교점 G, AD=12 cm 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "삼각형·중선 도형",
    note="AG=(2/3)AD=8 cm → ⑤. 빠른정답 10 cm와 불일치.")

# p55 (프라임 G′)
add(id="49b32dfa", qtype="choice",
    question="다음 그림에서 점 G와 G′은 각각 [[tri(ABC)]]와 [[tri(GBC)]]의 무게중심이고, G′D = 2일 때, [[seg(AG)]]의 길이는?",
    choices=["[[10]]", "[[12]]", "[[14]]", "[[16]]", "[[18]]"], derived_answer="②",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 중선 AD(D는 BC의 중점) 위의 무게중심 G와 △GBC의 무게중심 G′, 선분 GB·GC·G′B·G′C"),
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(G′D 선분 기호를 텍스트로 대체) / " + FIG + "삼각형·무게중심 도형",
    note="G′D=GD/3=2 → GD=6, AG=2GD=12 → ②. 빠른정답 5와 불일치.")

# p57 (프라임 G′)
add(id="718059ce", qtype="choice",
    question="다음 그림에서 점 G는 [[tri(ABC)]]의 무게중심이고, 점 G′은 [[tri(GBC)]]의 무게중심이다. [[seg(AD) = 12]] cm일 때, GG′의 길이는?",
    choices=["[[frac(2,3)]] cm", "[[frac(4,3)]] cm", "[[2]] cm", "[[frac(8,3)]] cm", "[[frac(10,3)]] cm"], derived_answer="④",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 중선 AD(D는 BC의 중점) 위의 무게중심 G와 △GBC의 무게중심 G′, 선분 GB·GC·G′B·G′C, AD=12 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(GG′ 선분 기호를 텍스트로 대체) / " + FIG + "삼각형·무게중심 도형",
    note="GD=4, GG′=(2/3)GD=8/3 → ④. 빠른정답 17과 불일치.")

# p59 (프라임 G′)
add(id="fdae7650", qtype="short",
    question=("다음 그림에서 [[seg(BM)]]은 [[tri(ABC)]]의 중선이고 두 점 G, G′은 각각 [[tri(ABC)]], [[tri(AGC)]]의 무게중심이다. "
              "G′M = 5 cm일 때, BG′의 길이를 구하시오."),
    choices=None, derived_answer="40 cm",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AC의 중점 M과 중선 BM, BM 위의 무게중심 G와 △AGC의 무게중심 G′(GM 위), 선분 AG·GC, G′M=5 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(G′M, BG′ 선분 기호를 텍스트로 대체) / " + FIG + "삼각형·무게중심 도형",
    note="GM=3G′M=15, BG=2GM=30, GG′=10 → BG′=40 cm = 빠른정답 ✓.")

# p61
add(id="5ea0d635", qtype="short",
    question="다음 그림에서 점 G는 [[tri(ABC)]]의 무게중심이고 [[par(seg(AD), seg(EF))]]이다. [[seg(AG) = 12]] cm일 때, [[seg(EF)]]의 길이를 구하시오",
    choices=None, derived_answer="9 cm",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 중선 AD(D는 BC 위) 위의 무게중심 G, AB의 중점 E(CE가 G를 지남), E에서 BC 위의 점 F로 AD에 평행한 선분 EF(화살표 표시), AG=12 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·무게중심·평행선 도형",
    note="AD=18, △BAD에서 E는 AB의 중점 → EF=AD/2=9 cm. 빠른정답 27 cm와 불일치. 원문 끝에 마침표 없음.")

# p71 (프라임 G′)
add(id="efe51061", qtype="short",
    question=("다음 그림의 [[seg(BC) = 8]] cm인 이등변삼각형 ABC에서 밑변 BC의 중점을 D, [[tri(ABD)]]와 [[tri(ACD)]]의 무게중심을 각각 G, G′이라고 한다. "
              "이때, GG′의 길이를 구하시오."),
    choices=None, derived_answer="frac(8,3) cm",
    figure=U(ISO + ", BC의 중점 D와 선분 AD, △ABD의 무게중심 G(왼쪽)·△ACD의 무게중심 G′(오른쪽)와 선분 GG′, BC=8 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(GG′ 선분 기호를 텍스트로 대체) / " + FIG + "이등변삼각형·무게중심 도형",
    note="G, G′은 AD에서 각각 BD/3=4/3만큼 떨어짐 → GG′=8/3 cm. 빠른정답 없음.")

# p74 (프라임 G′)
add(id="2908d225", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 세 점 M, N, H는 각각 [[seg(AB)]], [[seg(DC)]], [[seg(BC)]]의 중점이고 "
              "두 점 G, G′은 각각 [[tri(ABC)]], [[tri(DBC)]]의 무게중심이다. [[seg(MN) = frac(45,2)]] cm, [[seg(BC) = 30]] cm일 때, GG′의 길이를 구하시오."),
    choices=None, derived_answer="5 cm",
    figure=U("사다리꼴 ABCD(AD 위, BC 아래), AB·DC·BC의 중점 M·N·H(같은 길이 표시), 선분 MN·AH·DH·AC·BD, AH 위의 G와 DH 위의 G′을 이은 선분 GG′, MN=45/2 cm·BC=30 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.75,
    needs_review="프라임 점 라벨(GG′ 선분 기호를 텍스트로 대체) / " + FIG + "사다리꼴·무게중심 복합 도형",
    note="AD=45−30=15, GG′∥AD, GG′=AD/3=5 cm = 빠른정답 ✓.")

# p76 (프라임 G′)
add(id="662490b8", qtype="short",
    question="다음 그림의 [[tri(ABC)]]에서 두 점 G, G′은 각각 [[tri(ABM)]], [[tri(AMC)]]의 무게중심이고 [[seg(BC) = 24]]일 때, GG′의 길이를 구하시오.",
    choices=None, derived_answer="8",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), BC 위의 점 M과 선분 AM, △ABM의 무게중심 G(왼쪽)·△AMC의 무게중심 G′(오른쪽)와 선분 GG′, BC=24 치수(점선 호)"),
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(GG′ 선분 기호를 텍스트로 대체) / " + FIG + "삼각형·무게중심 도형",
    note="GG′=BC/3=8. 빠른정답 2 cm와 불일치.")

# p88 (프라임 G′)
add(id="43c02b3d", qtype="choice",
    question="아래 그림에서 [[seg(AD)]]는 [[tri(ABC)]]의 중선이고 두 점 G, G′은 각각 [[tri(ABC)]], [[tri(GBC)]]의 무게중심이다. 다음 중 옳지 않은 것은?",
    choices=["GG′ : [[seg(GD)]] = 1 : 2", "GG′ : G′D = 2 : 1", "[[seg(AG)]] : GG′ = 3 : 1", "[[6 tri(GBD) = tri(ABC)]]", "△G′BD = [[frac(1,9) tri(ABD)]]"],
    derived_answer="①",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 중선 AD(D는 BC 위) 위의 무게중심 G와 △GBC의 무게중심 G′, 선분 GB·GC·G′B·G′C"),
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(G′ 포함 선분·삼각형 기호를 텍스트로 대체) / " + FIG + "삼각형·무게중심 도형",
    note="GG′=(2/3)GD → GG′:GD=2:3이므로 ① 틀림 = 빠른정답 ✓.")

# p96
add(id="fbe713d7", qtype="short",
    question=("다음 그림과 같이 평행사변형 ABCD에서 점 E는 [[seg(BC)]]의 중점이고 점 P는 [[seg(AE)]]와 [[seg(BD)]]의 교점이다. "
              "[[quad(ABCD) = 48]] cm²일 때, [[tri(APO)]]의 넓이를 구하시오."),
    choices=None, derived_answer="4 cm²",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, BC의 중점 E(BE=EC 표시), AE와 BD의 교점 P, △APO 음영"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·무게중심 도형",
    note="P는 △ABC의 무게중심 → △APO=△ABC/6=24/6=4 cm². 빠른정답 5와 불일치.")

# p97
add(id="c975e8ec", qtype="short",
    question=("다음 그림과 같이 평행사변형 ABCD에서 점 M은 [[seg(BC)]]의 중점이고, 점 P는 [[seg(BD)]]와 [[seg(AM)]]의 교점이다. "
              "[[tri(ABP) = 5]] cm²일 때, [[quad(ABCD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="30 cm²",
    figure=U(PAR + ", 대각선 AC·BD의 교점 O, BC의 중점 M(BM=MC 표시), AM과 BD의 교점 P, 평행사변형 전체 음영"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "평행사변형·무게중심 도형",
    note="P는 △ABC의 무게중심 → △ABC=3·5=15, □ABCD=30 cm² = 빠른정답(30 cm2) ✓(단위 표기만 다름).")

# ════════ 닮은 도형의 넓이와 부피 ════════
# p4
add(id="0761b972", qtype="short",
    question="다음 그림의 [[tri(ABC)]]에 대하여 [[par(seg(BC), seg(DE))]]이고, [[quad(DBCE)]]의 넓이가 [[25]] cm²일 때, [[tri(ABC)]]의 넓이를 구하시오.",
    choices=None, derived_answer="45 cm²",
    figure=U("삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 D·AC 위의 점 E, DE∥BC(화살표 표시), AD=8 cm·DB=4 cm 치수(점선 호), 전체 음영"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·평행선 치수 도형",
    note="△ADE:△ABC=4:9 → □DBCE=(5/9)△ABC=25 → 45 cm². 빠른정답 4와 불일치.")

# p6
add(id="9e69ec91", qtype="choice",
    question=("다음 그림에서 [[quad(ABCD)]]는 [[par(seg(AD), seg(BC))]]인 사다리꼴이다. [[tri(OBC)]]의 넓이가 [[50]] cm²일 때, [[tri(ODA)]]의 넓이는? "
              "(단, 점 O는 두 대각선의 교점이다.)"),
    choices=["[[16]] cm²", "[[17]] cm²", "[[18]] cm²", "[[19]] cm²", "[[20]] cm²"], derived_answer="③",
    figure=U("사다리꼴 ABCD(AD 위, BC 아래, 화살표로 평행 표시), 대각선 AC·BD의 교점 O, △ODA 음영, AD=9 cm·BC=15 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "사다리꼴·대각선 치수 도형",
    note="닮음비 9:15=3:5, 넓이비 9:25 → 18 cm² → ③. 빠른정답 60 cm와 불일치.")

# p9
add(id="9bd5e80f", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[seg(AB)]], [[seg(CD)]]의 중점을 각각 E, F라 하고 [[seg(BC)]] 위의 점 G에 대하여 "
              "[[seg(AG)]], [[seg(DG)]]가 [[seg(EF)]]와 만나는 점을 각각 H, I라 하자. [[quad(ABCD)]]의 넓이가 [[72]] cm²일 때, [[tri(GIH)]]의 넓이를 구하시오."),
    choices=None, derived_answer="9 cm²",
    figure=U(PAR + ", AB의 중점 E·CD의 중점 F(같은 길이 표시)와 선분 EF, BC 위의 점 G, AG·DG가 EF와 만나는 점 H·I, △GIH 음영"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "평행사변형·중점 연결 도형",
    note="H, I는 AG, DG의 중점 → △GIH=△GAD/4=36/4=9 cm². 빠른정답 3과 불일치.")

# p83 (프라임 B′C′A′)
add(id="9db9452c", qtype="short",
    question=("다음 그림과 같이 눈높이가 [[1.6]] m인 송현이가 어떤 탑으로부터 [[20]] m 떨어진 곳에서 탑의 끝 A지점을 올려다본 각인 [[angle(B)]]의 크기와 "
              "∠B′의 크기가 같도록 축도를 그렸더니 B′C′ = 5 cm, A′C′ = 4 cm이었을 때, [[seg(AC)]]의 길이를 구하시오."),
    choices=None, derived_answer="16 m",
    figure=U("왼쪽: 탑과 사람 그림, 눈높이 B(1.6 m), 탑의 끝 A, 눈높이 수평선과 탑의 교점 C(직각 표시), BC=20 m 치수(점선 호); 화살표 오른쪽: 축도 직각삼각형 A′B′C′(C′ 직각), B′C′=5 cm·A′C′=4 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.75,
    needs_review="프라임 점 라벨(∠B′, B′C′, A′C′을 텍스트로 대체) / " + FIG + "탑·축도 그림",
    note="BC:B′C′=AC:A′C′ → AC=20·4/5=16 m. 빠른정답 28 m와 불일치.")

# p88
add(id="f9a3423e", qtype="choice",
    question=("평지에 수직으로 서 있는 전신주의 그림자는 다음 그림과 같고 길이 [[1]] m의 막대를 지면에 수직으로 세우면 그림자의 길이는 [[1.2]] m이다. "
              "[[seg(BD) = 3]] m, [[seg(CD) = 2]] m일 때, 전신주의 높이는? (단, 벽면은 지면과 수직이다.)"),
    choices=["[[3]] m", "[[3.5]] m", "[[4]] m", "[[4.5]] m", "[[5]] m"], derived_answer="④",
    figure=U("전신주 AB(A 위 끝, B 지면)와 벽면, 그림자가 지면 BD=3 m·벽면 DC=2 m로 꺾임, A에서 C로 이어지는 선; 오른쪽에 막대 EF=1 m와 그림자 FG=1.2 m인 직각삼각형 EFG(F 직각)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "전신주·그림자 삽화 도형",
    note="벽면 그림자 2 m ↔ 지면 2.4 m → 전체 5.4 m, 높이=5.4/1.2=4.5 m → ④ = 빠른정답 ✓.")

# ════════ 이등변삼각형의 성질 ════════
# p3 (선지 ④⑤ 잘림)
add(id="5d0d1373", qtype="choice",
    question=("다음은 정삼각형의 세 내각의 크기가 모두 같음을 보이는 과정이다. (가), (나), (다)에 알맞은 것으로 옳지 않은 것을 고르면?\n"
              "[[tri(ABC)]]가 정삼각형일 때,\n[[tri(ABC)]]는 [[seg(AB) = seg(AC)]]인 이등변삼각형이므로\n(가) = [[angle(C)]] ⋯ ㉠\n"
              "또, [[tri(ABC)]]는 (나) = [[seg(BC)]]인\n이등변삼각형이므로\n[[angle(A) = angle(C)]] ⋯ ㉡\n㉠, ㉡에서 [[angle(A) = angle(B)]] = (다)"),
    choices=["(가) [[angle(B)]]", "(나) [[seg(AC)]]", "(다) [[angle(C)]]", "(이미지 하단 잘림)", "(이미지 하단 잘림)"], derived_answer="②",
    figure=U("정삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 세 변에 같은 길이 표시"),
    difficulty_est=1, confidence=0.7,
    needs_review="이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움) / " + FIG + "정삼각형 그림",
    note="(나)는 BA이어야 하므로 ② = 빠른정답 ✓(보이는 선지 기준).")

# p5
add(id="66f24987", qtype="choice",
    question=("다음은 '이등변삼각형의 두 밑각의 크기는 같다.'를 보이는 과정이다. (가)~(마)에 알맞은 것으로 옳지 않은 것을 모두 고르면? (정답 2개)\n"
              "[[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서\n[[angle(A)]]의 이등분선과 [[seg(BC)]]의 교점을 D라 하자.\n"
              "[[tri(ABD)]]와 [[tri(ACD)]]에서\n[[seg(AB) = seg(AC)]] ⋯ ㉠\n[[seg(AD)]]는 공통 ⋯ ㉡\n또, (가)는 [[angle(A)]]의 이등분선이므로\n"
              "[[angle(BAD)]] = (나) ⋯ ㉢\n㉠, ㉡, ㉢에 의해\n[[tri(ABD)]] ≡ (다) ((라) 합동)\n∴ (마) = [[angle(C)]]"),
    choices=["(가) [[seg(BC)]]", "(나) [[angle(CAD)]]", "(다) [[tri(ACD)]]", "(라) ASA", "(마) [[angle(B)]]"], derived_answer="①, ④",
    figure=U(ISO + ", AB=AC 표시, A의 각 이등분선 AD(D는 BC 위), A에 같은 각 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 그림",
    note="(가)=AD, (라)=SAS → ①, ④ = 빠른정답(1, 4) ✓.")

# p9
add(id="20c2f4ff", qtype="choice",
    question="다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 [[tri(ABC)]]에서 [[angle(A) = deg(58)]]일 때, [[angle(x)]]의 크기는?",
    choices=DEG5(118, 119, 120, 121, 122), derived_answer="②",
    figure=U(ISO + ", AB=AC 표시, A에 58°, BC의 연장선(C 오른쪽)과 CA가 이루는 외각을 x로 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형 외각 도형",
    note="∠C=61° → x=180°−61°=119° → ②. 빠른정답 3과 불일치.")

# p11
add(id="641d7b0a", qtype="short",
    question="다음 그림에서 [[tri(ABC)]]가 [[seg(AB) = seg(AC)]]인 이등변삼각형일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(125)",
    figure=U("삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 위), AB=AC 표시, A에 70°, BC의 연장선 위의 점 D(C 위쪽), ∠ACD를 x로 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형 외각 도형",
    note="∠ACB=55° → x=125°. 빠른정답 deg(126)과 불일치.")

# p12
add(id="dfff4332", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[seg(AD)]]는 [[angle(A)]]의 이등분선일 때, [[angle(ADB)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(90)",
    figure=U(ISO + ", AB=6 cm·AC=6 cm·BC=7 cm 치수(점선 호), A의 이등분선 AD(D는 BC 위), A에 같은 각 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 치수 도형",
    note="꼭지각의 이등분선은 밑변을 수직이등분 → 90°. 빠른정답 2와 불일치.")

# p14
add(id="2c4fe29d", qtype="choice",
    question="다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AB) = seg(BC)]], [[angle(ABD) = angle(CBD)]]일 때, [[x]]의 값은?",
    choices=["[[3.5]]", "[[4]]", "[[4.5]]", "[[5]]", "[[5.5]]"], derived_answer="④",
    figure=U("직각이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, B에 직각 표시, AB=BC 표시), 빗변 AC 위의 점 D와 BD(D에 직각 표시), AD=2.5 cm·AC=x cm 치수(점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "직각이등변삼각형 치수 도형",
    note="BD는 AC를 수직이등분 → x=2·2.5=5 → ④. 빠른정답 deg(125)와 불일치.")

# p16 (id 3개, 같은 문항)
dup(["b5865c2e", "7bb1d887", "d3db21f8"], qtype="choice",
    question=("아래 그림과 같은 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 꼭지각 [[angle(A)]]의 이등분선을 그어 밑변 BC와의 교점을 D라 하자. "
              "다음은 선분 AD 위에 한 점 P를 잡았을 때, [[seg(BP) = seg(CP)]]임을 증명한 것이다. □ 안에 차례로 들어갈 말은?\n"
              "[[tri(BPD)]]와 [[tri(CPD)]]에서 [[seg(BD)]] = □이고\n[[angle(BDP)]] = □ = [[deg(90)]], [[seg(PD)]]는 공통이므로\n"
              "[[cong(tri(BPD), tri(CPD))]] (SAS 합동)\n따라서 [[seg(BP) = seg(CP)]]이다."),
    choices=["[[seg(PD)]], [[angle(CDP)]]", "[[seg(CD)]], [[angle(CDP)]]", "[[seg(AD)]], [[angle(CPD)]]", "[[seg(PC)]], [[angle(CPD)]]", "[[seg(CD)]], [[angle(PCD)]]"],
    derived_answer="②",
    figure=U(ISO + ", A의 이등분선 AD(D는 BC의 중점, BD=DC 표시), AD 위의 점 P와 선분 PB·PC"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 그림",
    note="BD=CD, ∠BDP=∠CDP=90° → ②. 빠른정답 4와 불일치.")

# p19
add(id="38d86b43", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[angle(A)]]의 이등분선과 [[seg(BC)]]의 교점을 H라 하고 [[seg(BC)]]의 연장선 위의 점 D에 대하여 "
              "[[angle(DEH) = deg(54)]]가 되도록 [[seg(AH)]] 위에 점 E를 잡는다. [[angle(D)]]의 이등분선과 [[seg(AB)]], [[seg(AC)]]의 교점을 각각 F, G라 하면 "
              "[[angle(DGC) = deg(96)]]일 때, [[angle(DFB)]]의 크기는?"),
    choices=DEG5(46, 48, 50, 52, 54), derived_answer="②",
    figure=U(ISO + ", A의 이등분선 AH(H는 BC 위, A에 같은 각 표시), AH 위의 점 E, BC의 연장선 위(B 왼쪽)의 점 D, 선분 DE(E에 54°), D의 이등분선이 AB·AC와 만나는 점 F·G(D에 같은 각 표시, G에 96°)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 복합 도형",
    note="∠EDH=36° → ∠FDB=18°, ∠C=180−96−18=66°=∠B → ∠DFB=180−18−114=48° → ② = 빠른정답 ✓.")

# p20
add(id="d26bb9ca", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 모양의 종이를 [[seg(DE)]]를 접는 선으로 하여 접었더니 점 A가 점 B와 겹쳐졌다. "
              "[[angle(EBC) = deg(15)]]일 때, [[angle(A)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(50)",
    figure=U("이등변삼각형 ABC(A 위·점선, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 D·AC 위의 점 E, 접는 선 DE로 A가 B에 겹침(△DBE 음영), B에 15° 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형 접기 도형",
    note="∠DBE=∠A=a, ∠B=a+15=(180−a)/2 → a=50°. 빠른정답 32와 불일치.")

# p21
add(id="57e827c5", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 꼭짓점 B가 점 D에 오도록 접었을 때, [[angle(ACD) = deg(30)]]이다. "
              "[[angle(CDE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(70)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래·점선, C 오른쪽 아래), 접는 선 CE(E는 AB 위)로 B가 AB 위의 점 D로 옮겨짐, △ADC·△DEC 음영, C에 30° 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형 접기 도형",
    note="∠CDE=∠B=b, ∠ADC=2b−30=180−b → b=70°. 빠른정답 18과 불일치.")

# p22
add(id="3c406d1d", qtype="short",
    question=("다음 그림에서 [[tri(ABC)]]는 [[seg(AB) = seg(AC)]]인 이등변삼각형이다. [[seg(BF) = seg(CD)]], [[seg(BD) = seg(CE)]], [[angle(A) = deg(52)]]일 때, "
              "[[angle(DFE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(58)",
    figure=U(ISO + ", AB 위의 점 F, BC 위의 점 D, AC 위의 점 E, 삼각형 FDE, BF=CD·BD=CE 같은 길이 표시, A에 52°, F에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형 내접 삼각형 도형",
    note="△FBD≡△DCE → ∠FDE=∠B=64°, FD=DE → ∠DFE=58°. 빠른정답 2와 불일치.")

# p23
add(id="e313cb7e", qtype="short",
    question=("다음 그림의 [[tri(ABC)]]는 [[seg(AB) = seg(AC)]]인 이등변삼각형이다. 점 D는 변 BC위의 점으로 [[angle(BAC) = 3 angle(BAD)]]이고 "
              "점 E는 점 C에서 [[seg(AD)]] 위에 내린 수선의 발이다. [[angle(DCE) = deg(13)]]일 때, [[angle(BAC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(78)",
    figure=U(ISO + ", BC 위의 점 D와 선분 AD, C에서 AD에 내린 수선의 발 E(직각 표시), A에 각 표시 2개, C에 13°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "이등변삼각형·수선 도형",
    note="∠BAD=a: 90−2a+13=90−1.5a → a=26 → ∠BAC=78°. 빠른정답 deg(50)과 불일치.")

# p24
add(id="d2df95ce", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[seg(BD)]]와 [[seg(CE)]]의 교점을 P라 하자. [[seg(AD) = seg(AE)]]이고 "
              "[[angle(A) = deg(42)]], [[angle(EBP) = deg(28)]]일 때, [[angle(CPD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(82)",
    figure=U(ISO + ", AB 위의 점 E·AC 위의 점 D(AE=AD 표시), BD와 CE의 교점 P, A에 42°, B에 28°, ∠CPD 음영"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형·교점 도형",
    note="△ABD≡△ACE → ∠ACE=28°, ∠B=∠C=69° → ∠CPD=41°+41°=82°. 빠른정답 deg(70)과 불일치.")

# p26
add(id="4450eab3", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 변 BC 위에 [[angle(BAD) = frac(1,3) angle(BAC)]]가 되도록 점 D를 잡고 "
              "꼭짓점 C에서 [[seg(AD)]]에 내린 수선의 발을 E라 하자. [[angle(DCE) = deg(18)]]일 때, [[angle(BAD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(36)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, AB=AC 표시), BC 위의 점 D와 선분 AD, C에서 AD에 내린 수선의 발 E(직각 표시), C에 18°"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "이등변삼각형·수선 도형",
    note="∠BAD=a: 90−2a+18=90−1.5a → a=36°. 빠른정답 deg(78)과 불일치.")

# p27
add(id="0dd5501f", qtype="choice",
    question="다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[seg(BC) = seg(BD)]]이고 [[angle(A) = deg(56)]]일 때, [[angle(ABD)]]의 크기는?",
    choices=DEG5(5, 6, 7, 8, 9), derived_answer="②",
    figure=U(ISO + ", AC 위의 점 D(A 바로 아래)와 선분 BD, BC=BD 표시, A에 56°, B에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형 도형",
    note="∠C=62°=∠BDC → ∠DBC=56° → ∠ABD=6° → ②. 빠른정답 deg(82)와 불일치.")

# p28
add(id="41339bcd", qtype="short",
    question="다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AB) = seg(BD) = seg(DC)]]이고 [[angle(DCB) = deg(37)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(111)",
    figure=U("삼각형 ABC(A 위 왼쪽, B 아래 왼쪽, C 아래 오른쪽), AC 위의 점 D와 선분 BD, AB=BD=DC 같은 길이 표시, C에 37°, CB의 연장선(B 왼쪽)과 BA가 이루는 각 x"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이웃한 이등변삼각형 외각 도형",
    note="∠DBC=37°, ∠A=∠ADB=74° → x=74°+37°=111°. 빠른정답 2와 불일치.")

# p29
add(id="dca4a886", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[seg(AD) = seg(DB) = seg(BC)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(36)",
    figure=U(ISO + ", AC 위의 점 D와 선분 BD, AD=DB=BC 같은 길이 표시, A의 각을 x로 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이웃한 이등변삼각형 도형",
    note="∠A=x, ∠B=∠C=2x, 5x=180° → x=36° = 빠른정답 ✓.")

# p30
add(id="fcbee6cc", qtype="choice",
    question="다음 그림에서 [[seg(AB) = seg(AC) = seg(CD)]]이고 [[angle(DCE) = deg(123)]]일 때, [[angle(B)]]의 크기는?",
    choices=DEG5(37, 38, 39, 40, 41), derived_answer="⑤",
    figure=U("B(왼쪽 아래)에서 오른쪽으로 C, E가 놓인 직선, BA의 연장선 위의 점 D(A 위), 선분 AC·CD, AB=AC=CD 같은 길이 표시, C에 123°, B의 각 음영"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이웃한 이등변삼각형 외각 도형",
    note="∠B=b, ∠DCE=3b=123° → b=41° → ⑤. 빠른정답 2와 불일치.")

# p31
add(id="9fae0130", qtype="short",
    question="다음 그림에서 [[seg(AB) = seg(AC) = seg(CD)]]이고 [[angle(B) = deg(23)]]일 때, [[angle(DCE)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(69)",
    figure=U("B(왼쪽 아래)에서 오른쪽으로 C, E가 놓인 직선, BA의 연장선 위의 점 D(A 위), 선분 AC·CD, AB=AC=CD 같은 길이 표시, B에 23°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이웃한 이등변삼각형 외각 도형",
    note="∠DCE=3∠B=69°. 빠른정답 deg(111)과 불일치.")

# p32
add(id="3ae67062", qtype="short",
    question="다음 그림에서 [[seg(AB) = seg(AC) = seg(CD) = seg(DE)]]이다. [[angle(B) = deg(25)]]일 때, [[angle(CDE)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(30)",
    figure=U("B(왼쪽 아래)에서 오른쪽으로 C, E가 놓인 직선과 BA·D를 지나는 직선, 선분 AC·CD·DE, AB=AC=CD=DE 같은 길이 표시, B에 25°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이웃한 이등변삼각형 도형",
    note="∠ACB=25°, ∠ADC=50°, ∠DCE=∠DEC=75° → ∠CDE=30°. 빠른정답 deg(36)과 불일치.")

# p34
add(id="b3476ad2", qtype="short",
    question="다음 그림과 같은 [[tri(ABC)]]에서 [[seg(BE) = seg(DE) = seg(AD) = seg(AC)]]일 때, [[angle(ACB)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(75)",
    figure=U("삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 E, BC 위의 점 D, 선분 ED·AD, BE=DE=AD=AC 같은 길이 표시, A에 ∠BAC=80°, C에 각 표시"),
    difficulty_est=3, confidence=0.75, needs_review=FIG + "이웃한 이등변삼각형 도형",
    note="∠B=b: ∠BAC=180−4b=80 → b=25, ∠ACB=3b=75°. 80°는 ∠BAC 전체로 판독. 빠른정답 deg(69)와 불일치.")

# p35
add(id="dc4fafaa", qtype="short",
    question="다음 그림의 [[tri(AED)]]에서 [[seg(AB) = seg(BC) = seg(CD) = seg(DE)]]이고 [[angle(ADE) = deg(88)]]일 때, [[angle(A)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(23)",
    figure=U("삼각형 AED(A 왼쪽 아래, E 오른쪽 아래, D 오른쪽 위), AD 위의 점 B, AE 위의 점 C, 선분 BC·CD, AB=BC=CD=DE 같은 길이 표시, D에 88°, A에 각 표시"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "이웃한 이등변삼각형 도형",
    note="∠A=a: ∠ADE=180−4a=88 → a=23°. 빠른정답 deg(30)과 불일치.")

# p37
add(id="37e8a320", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]], [[seg(FG) = seg(FH)]]인 [[tri(ABC)]], [[tri(FGH)]]에서 [[angle(C)]]의 외각의 이등분선과 [[angle(B)]]의 "
              "이등분선의 교점을 D라 하고 [[angle(H)]]의 외각의 이등분선과 [[angle(G)]]를 그림과 같이 [[ratio(2,1)]]로 나눈 선의 교점을 I라 하자. "
              "[[angle(A) = angle(F) = deg(24)]]일 때, [[y - x]]의 값은?"),
    choices=DEG5(13, 14, 15, 16, 17), derived_answer="①",
    figure=U("왼쪽: 이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, BC의 연장선 위 E), A에 24°, B의 이등분선(같은 각 표시)과 C의 외각 이등분선(같은 각 표시)의 교점 D(위 오른쪽), ∠BDC=x; "
             "오른쪽: 이등변삼각형 FGH(F 위, G 왼쪽 아래, H 오른쪽 아래, GH의 연장선 위 E), F에 24°, G의 각을 2:1로 나누는 선(위쪽 2, 아래쪽 1)과 H의 외각 이등분선의 교점 I, ∠GIH=y"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "이등변삼각형 두 개·이등분선 복합 도형",
    note="x=51°−39°=12°, y=51°−26°=25° → y−x=13° → ①. 빠른정답 deg(75)와 불일치.")

# p41
add(id="cb4ce600", qtype="short",
    question="다음 그림에서 [[tri(ABC)]]는 [[seg(AB) = seg(AC)]]인 이등변삼각형이다. [[angle(B)]]의 이등분선이 [[seg(AC)]]와 만나는 점을 D라 할 때, [[x]]의 길이를 구하시오.",
    choices=None, derived_answer="8 cm",
    figure=U(ISO + ", A에 36°, B의 이등분선 BD(D는 AC 위, B에 같은 각 표시), AD=x·BC=8 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 치수 도형",
    note="∠ABD=36°=∠A → AD=BD, ∠BDC=72°=∠C → BD=BC=8 → x=8 cm. 빠른정답 2와 불일치.")

# p42
add(id="7c069c6d", qtype="short",
    question="[[seg(AB) = seg(AC)]], [[angle(A) = deg(80)]]인 이등변삼각형 ABC에서 [[angle(B)]]의 이등분선과 [[seg(AC)]]의 교점을 D라고 할 때, [[angle(BDC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(105)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), A에 80°, B의 이등분선 BD(D는 AC 위, B에 같은 각 표시), D에 각 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 도형",
    note="∠ABD=25° → ∠BDC=80°+25°=105°. 빠른정답 deg(120)과 불일치. 첫 줄이 이미지 상단에 붙어 있으나 문장은 완결.")

# p47
add(id="5ee5ba94", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 [[par(seg(AD), seg(BC))]]인 사다리꼴이다. 점 F는 점 D에서 [[seg(BC)]]에 내린 수선의 발이고 점 G는 점 E에서 [[seg(AB)]]에 내린 수선의 발이다. "
              "[[perp(seg(BO), seg(DC))]], [[seg(DF) = seg(FC)]], [[angle(GOF) = deg(46)]]일 때, [[angle(AOG)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(44)",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, B에 직각), D에서 BC에 내린 수선의 발 F(직각 표시), DC 위의 점 O(BO⊥DC, O에 직각 표시)와 점 E, "
             "E에서 AB에 내린 수선의 발 G(직각 표시, GE는 BC에 평행), 선분 AO·GO·BO·FO, ∠GOF=46° 표시"),
    difficulty_est=3, confidence=0.75, needs_review=FIG + "사다리꼴·수선 복합 도형",
    note="∠C=45° → OB=OC, △ABO≡△FCO → ∠AOF=∠BOC=90° → ∠AOG=90°−46°=44°. 빠른정답 3과 불일치.")

# p48
add(id="70887a06", qtype="choice",
    question=("다음 그림과 같이 정사각형 ABCD와 부채꼴 BCD가 있다. 호 BD 위의 점 P에 대하여 [[perp(seg(PM), seg(BC))]], [[seg(BM) = seg(CM)]]일 때, "
              "[[angle(PAB)]]의 크기는?"),
    choices=DEG5(72, 73, 74, 75, 76), derived_answer="④",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), C를 중심으로 하는 부채꼴 BCD의 호 BD, 호 위의 점 P, BC의 중점 M(BM=CM 표시)과 PM(M에 직각 표시), 선분 AP, A에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "정사각형·부채꼴 도형",
    note="PB=PC=BC → △PBC 정삼각형, ∠ABP=30°, AB=BP → ∠PAB=75° → ④. 빠른정답 deg(35)와 불일치.")

# p50
add(id="cfaee868", qtype="short",
    question="다음 그림과 같은 정오각형 ABCDE에서 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(36)",
    figure=U("정오각형 ABCDE(A 위, B 왼쪽, C 왼쪽 아래, D 오른쪽 아래, E 오른쪽), 대각선 BD, ∠CBD를 x로 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "정오각형·대각선 도형",
    note="∠C=108°, BC=CD → x=36°. 빠른정답 deg(44)와 불일치.")

# p51
add(id="bc9464a4", qtype="choice",
    question="다음 그림과 같은 정사각형 ABCD에서 [[tri(APD)]]가 정삼각형일 때, [[angle(PBC)]]의 크기는?",
    choices=DEG5(15, 20, 25, 30, 35), derived_answer="①",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내부 아래쪽의 점 P와 정삼각형 APD, 선분 PB·PC, B에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "정사각형·정삼각형 도형",
    note="∠ABP=75° → ∠PBC=15° → ①. 빠른정답 4와 불일치.")

# p58
add(id="a66cde49", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC) = 12]] cm인 이등변삼각형 ABC에서 [[seg(AB)]]의 중점 M을 지나고 [[seg(BC)]]에 수직인 직선이 [[seg(BC)]]와 만나는 점을 P, "
              "[[seg(AC)]]의 연장선과 만나는 점을 Q라 할 때, [[seg(AQ)]]의 길이는?"),
    choices=["[[3]] cm", "[[4]] cm", "[[5]] cm", "[[6]] cm", "[[7]] cm"], derived_answer="④",
    figure=U(ISO + ", AB의 중점 M(AM=MB 표시), M을 지나 BC에 수직인 직선이 BC와 만나는 점 P(직각 표시)와 CA의 연장선과 만나는 점 Q(A 위), AC=12 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이등변삼각형·수직선 도형",
    note="∠AMQ=∠BMP=90°−∠B=∠Q → AQ=AM=6 cm → ④. 빠른정답 4 cm와 불일치.")

# p60
add(id="3c721ef0", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 꼭짓점 B, C에서 대변에 내린 수선의 발을 각각 D, E라 할 때, [[seg(BD) = seg(CE)]]임을 증명하는 과정이다. "
              "(가)~(마)에 들어갈 것으로 옳지 않은 것은?\n(가정)\n(1) [[seg(AB)]] = (가)\n(2) B, C에서 대변에 내린 수선의 발을 각각 D, E라 한다.\n"
              "(결론) [[seg(BD)]] = (나)\n(증명) [[tri(EBC)]]와 [[tri(DCB)]]에서\n[[angle(BDC)]] = (다) = [[deg(90)]] ⋯ ㉠\n[[angle(B)]] = (라) ⋯ ㉡\n"
              "(마)는 공통 ⋯ ㉢\n[[cong(tri(EBC), tri(DCB))]]\n∴ [[seg(BD) = seg(CE)]]"),
    choices=["(가) [[seg(AC)]]", "(나) [[seg(CE)]]", "(다) [[angle(BDA)]]", "(라) [[angle(C)]]", "(마) [[seg(BC)]]"], derived_answer="③",
    figure=U(ISO + ", B에서 AC에 내린 수선의 발 D, C에서 AB에 내린 수선의 발 E(각각 직각 표시), 선분 BD·CE"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·수선 그림",
    note="(다)=∠CEB → ③. 빠른정답 4와 불일치.")

# p61 (id 2개, 같은 문항)
dup(["6453fb33", "f3ea6233"], qtype="choice",
    question=("다음은 '[[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[angle(B)]], [[angle(C)]]의 이등분선의 교점을 P라 하면 [[tri(PBC)]]도 이등변삼각형이다.'를 설명하는 과정이다. "
              "(가)~(마)에 알맞은 것으로 옳지 않은 것은?\n[[seg(AB) = seg(AC)]]이므로\n[[angle(ABC)]] = (가),\n[[angle(PBC)]] = (나)[[angle(ABC)]],\n"
              "[[angle(PCB)]] = (나)[[angle(ACB)]]\n∴ (다)\n즉, [[tri(PBC)]]의 두 내각의 크기가 같으므로 (라)이다.\n따라서 (마)는 이등변삼각형이다."),
    choices=["(가) [[angle(ACB)]]", "(나) [[2]]", "(다) [[angle(PBC) = angle(PCB)]]", "(라) [[seg(PB) = seg(PC)]]", "(마) [[tri(PBC)]]"], derived_answer="②",
    figure=U(ISO + ", AB=AC 표시, B·C의 이등분선(같은 각 표시)의 교점 P"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 그림",
    note="(나)=1/2 → ②. 빠른정답 4와 불일치.")

# p62 (id 2개, 같은 문항)
dup(["753c1c4f", "b64688c7"], qtype="choice",
    question=("다음은 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[angle(B)]]와 [[angle(C)]]의 이등분선의 교점을 P라 할 때, [[tri(PBC)]]가 이등변삼각형임을 증명하는 과정이다. "
              "(가)~(마)에 들어갈 것으로 옳지 않은 것은?\n[[tri(ABC)]]에서 [[angle(B)]] = (가) 이므로\n[[angle(PBC)]] = (나) × [[angle(B)]] = [[frac(1,2)]] × (다)\n= (라)\n"
              "따라서 [[tri(PBC)]]는 (마)이다."),
    choices=["(가) [[angle(C)]]", "(나) [[2]]", "(다) [[angle(C)]]", "(라) [[angle(PCB)]]", "(마) 이등변삼각형"], derived_answer="②",
    figure=U(ISO + ", AB=AC 표시, B·C의 이등분선(같은 각 표시)의 교점 P"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 그림",
    note="(나)=1/2 → ②. 빠른정답 6 cm와 불일치.")

# p63 (id 4개, 같은 문항)
dup(["2bdb7807", "52929897", "c4a9aa88", "3ac7d70b"], qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC에서 [[angle(B)]]와 [[angle(C)]]의 이등분선의 교점을 D라 할 때, [[seg(DB) = seg(DC)]]임을 설명하는 과정이다. "
              "(가)~(마)에 알맞은 것으로 옳지 않은 것은?\n[[tri(ABC)]]에서 (가) = [[angle(ACB)]]이므로\n[[angle(DBC) = frac(1,2) angle(ABC)]] = [[frac(1,2)]](나) = (다)\n"
              "따라서 [[tri(DBC)]]는 (라)인 (마)삼각형이다."),
    choices=["(가) [[angle(ABC)]]", "(나) [[angle(ACB)]]", "(다) [[angle(DCB)]]", "(라) [[seg(DB) = seg(DC)]]", "(마) 정"], derived_answer="⑤",
    figure=U(ISO + ", AB=AC 표시, B·C의 이등분선(같은 각 표시)의 교점 D"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "이등변삼각형·이등분선 그림",
    note="(마)=이등변 → ⑤. 빠른정답 3과 불일치.")

# p67
add(id="4cec1045", qtype="short",
    question=("다음 그림과 같이 직사각형 모양의 종이를 [[seg(AC)]]를 접는 선으로 하여 접었다. [[seg(AC) = 11]] cm이고 [[tri(ABC)]]의 둘레의 길이가 [[51]] cm일 때, "
              "[[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="20 cm",
    figure=U("직사각형 종이(점선 윤곽)를 접는 선 AC(A 윗변 위, C 아랫변 위)로 접은 그림, B는 아랫변 위의 점(왼쪽), △ABC와 접힌 부분 음영, AC=11 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "종이 접기 도형",
    note="접기 → AB=BC(이등변) → 2BC+11=51 → BC=20 cm = 빠른정답 ✓.")

# p68
add(id="d9e4d2aa", qtype="short",
    question="폭이 [[8]] cm인 직사각형 모양의 종이를 다음 그림과 같이 접었다. [[seg(AB) = 11]] cm일 때, [[tri(ABC)]]의 넓이를 구하시오.",
    choices=None, derived_answer="44 cm²",
    figure=U("폭 8 cm인 직사각형 종이(점선 윤곽)를 접은 그림, 접는 선 BC(B 아랫변, C 윗변), A는 윗변 위의 점, △ABC 음영, AB=11 cm·폭 8 cm 치수, 아랫변 오른쪽 점 D"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "종이 접기 도형",
    note="접기 → AC=AB=11, 높이 8 → 넓이 44 cm². 빠른정답 없음.")

# p78
add(id="93f1a835", qtype="short",
    question=("다음 그림과 같이 [[angle(B) = deg(90)]]이고 [[seg(AB) = seg(BC)]]인 직각이등변삼각형 ABC의 꼭짓점 B를 지나는 직선 [[l]]이 있다. "
              "두 꼭짓점 A, C에서 직선 [[l]]에 내린 수선의 발을 각각 D, E라 할 때, [[seg(DE)]]의 길이를 구하시오."),
    choices=None, derived_answer="11 cm",
    figure=U("수평 직선 l 위의 점 D·B·E, 위쪽의 직각이등변삼각형 ABC(B 직각, AB=BC 표시), A에서 l에 내린 수선의 발 D, C에서 내린 수선의 발 E(직각 표시), AD=4 cm·DB=7 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각이등변삼각형·수선 도형",
    note="△ADB≡△BEC(RHA) → BE=AD=4, DE=7+4=11 cm. 빠른정답 4, 5와 불일치.")

# p79
add(id="5e97c0d6", qtype="short",
    question=("다음 그림과 같이 [[tri(CDE)]]는 [[seg(CD) = seg(DE)]]이고 [[angle(D) = deg(90)]]인 직각이등변삼각형이다. "
              "[[angle(CBD) = angle(DAE) = deg(90)]], [[seg(CB) = 3]] m, [[seg(AE) = 5]] m일 때, [[seg(AB)]]의 길이를 구하시오."),
    choices=None, derived_answer="8 m",
    figure=U("수평선 위의 점 B·D·A, 위쪽에 C(B 위)·E(A 위), 직각이등변삼각형 CDE(D 직각, CD=DE 표시), B·A에 직각 표시, CB=3 m·AE=5 m 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각이등변삼각형·수선 도형",
    note="△CBD≡△DAE(RHA) → BD=5, DA=3 → AB=8 m. 빠른정답 1, 4와 불일치.")

# p80
add(id="9875451b", qtype="short",
    question=("다음 그림과 같이 [[angle(C) = deg(90)]]인 직각삼각형 ABC에서 [[angle(B)]]의 이등분선이 [[seg(AC)]]와 만나는 점을 D라 하자. "
              "[[perp(seg(AB), seg(DE))]]일 때, [[seg(AE)]]의 길이를 구하시오."),
    choices=None, derived_answer="5 cm",
    figure=U("직각삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래·직각), B의 이등분선 BD(D는 AC 위, B에 같은 각 표시), D에서 AB에 내린 수선의 발 E(직각 표시), AB=20 cm·BC=15 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "직각삼각형·이등분선 치수 도형",
    note="△BCD≡△BED(RHA) → BE=BC=15 → AE=5 cm. 빠른정답 15와 불일치.")

# p86
add(id="d134aca6", qtype="choice",
    question=("다음 그림의 [[tri(ABC)]]에서 [[seg(AC)]]의 중점을 M이라 하고, 점 M에서 [[seg(AB)]], [[seg(BC)]]에 내린 수선의 발을 각각 D, E라 하자. "
              "[[angle(A) = deg(35)]]이고 [[seg(MD) = seg(ME)]]일 때, [[angle(B)]]의 크기는?"),
    choices=DEG5(100, 105, 110, 115, 120), derived_answer="③",
    figure=U("삼각형 ABC(A 왼쪽 위, B 아래 왼쪽, C 오른쪽 아래), AC의 중점 M(AM=MC 표시), M에서 AB·BC에 내린 수선의 발 D·E(직각 표시, MD=ME 표시), A에 35°, B에 각 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형·수선 도형",
    note="△MDA≡△MEC(RHS) → ∠C=35° → ∠B=110° → ③ = 빠른정답 ✓.")

# p88
add(id="346a3001", qtype="short",
    question=("다음 그림과 같이 [[angle(C) = deg(90)]]이고 [[seg(AC) = seg(BC)]]인 직각이등변삼각형 ABC가 있다. [[seg(AC) = seg(AD)]], [[perp(seg(AB), seg(DE))]]이고 "
              "[[seg(BD) = 5]] cm일 때, [[x + y]]의 값을 구하시오."),
    choices=None, derived_answer="72.5",
    figure=U("직각이등변삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래·직각, AC=BC 표시), AB 위의 점 D(AD=AC 표시, D에 직각 표시), BC 위의 점 E와 선분 DE·AE, "
             "BD=5 cm·EC=x cm 치수(점선 호), ∠AED=y° 표시"),
    difficulty_est=3, confidence=0.75, needs_review=FIG + "직각이등변삼각형·수선 치수 도형",
    note="△ADE≡△ACE(RHS), △DBE 직각이등변 → x=DE=BD=5, y=∠AED=(180−45)/2=67.5 → x+y=72.5(y° 위치를 ∠AED로 판독). 빠른정답 30과 불일치.")

# p91
add(id="7883c8f9", qtype="short",
    question=("다음 그림과 같은 정사각형 ABCD에서 점 P는 [[seg(AB)]] 위의 점이고, 점 Q는 [[seg(BC)]]의 연장선 위에 [[seg(DP) = seg(DQ)]]인 점이다. "
              "[[angle(ADP) = deg(32)]]일 때, [[angle(BQP)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(13)",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 P, BC의 연장선 위(C 오른쪽)의 점 Q, 선분 DP·DQ(같은 길이 표시)·PQ, D에 32°"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "정사각형·합동 삼각형 도형",
    note="△DAP≡△DCQ → ∠PDQ=90°, ∠DQP=45°, ∠DQC=58° → ∠BQP=13° = 빠른정답 ✓.")

# p95
add(id="aa7c4bba", qtype="short",
    question=("다음 그림과 같이 [[angle(AOB)]]의 이등분선 위의 한 점 P에서 각의 두 변 OA, OB에 내린 수선의 발을 각각 C, D라 할 때, [[x + y]]의 값을 구하시오."),
    choices=None, derived_answer="75",
    figure=U("O에서 뻗은 두 반직선 OA(위)·OB(아래)와 그 이등분선(O에 같은 각 표시), 이등분선 위의 점 P, P에서 OA·OB에 내린 수선의 발 C·D(직각 표시), PC=5 cm·PD=y cm 치수, ∠OPC=x°, ∠DOP=20° 표시"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "각의 이등분선·수선 치수 도형",
    note="x=90−20=70, y=PC=5 → 75 = 빠른정답 ✓.")

# p98
add(id="4b7506ff", qtype="short",
    question=("다음 그림의 [[tri(ABC)]]에서 [[angle(A)]]의 외각의 이등분선과 [[angle(C)]]의 외각의 이등분선의 교점을 P라 하고 점 P에서 [[seg(AB)]]와 [[seg(BC)]]의 연장선에 "
              "내린 수선의 발을 각각 D, E라 하자. [[seg(AC) = 15]] cm, [[seg(DP) = 12]] cm일 때, [[tri(PDA)]]와 [[tri(PEC)]]의 넓이의 합을 구하시오."),
    choices=None, derived_answer="90 cm²",
    figure=U("삼각형 ABC(A 위 왼쪽, B 왼쪽 아래, C 오른쪽 아래), BA의 연장선 위의 D(A 위)와 BC의 연장선 위의 E(C 오른쪽), A·C의 외각 이등분선(같은 각 표시)의 교점 P(오른쪽), "
             "D·E에 직각 표시, △PDA·△PEC 음영, DP=12 cm·AC=15 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8, needs_review=FIG + "삼각형·외각 이등분선 도형",
    note="P는 방접원의 중심(PD=PE=PF, F는 AC 위 수선의 발) → 합=△PAC=½·15·12=90 cm². 빠른정답 없음.")

# p99 (이미지에 문항 2개, id 1개 — draft_a 대응인 위쪽 문항 전사)
add(id="29079440", qtype="short",
    question=("다음 그림의 [[tri(ABC)]]에서 [[angle(A)]]의 외각의 이등분선과 [[angle(C)]]의 외각의 이등분선의 교점을 P라 하고 점 P에서 [[seg(AB)]]와 [[seg(BC)]]의 연장선에 "
              "내린 수선의 발을 각각 D, E라 하자. [[seg(AC) = 11]] cm, [[seg(DP) = 8]] cm일 때, [[tri(PDA)]]와 [[tri(PEC)]]의 넓이의 합을 구하시오."),
    choices=None, derived_answer="44 cm²",
    figure=U("삼각형 ABC(A 위 왼쪽, B 왼쪽 아래, C 오른쪽 아래), BA의 연장선 위의 D(A 위)와 BC의 연장선 위의 E(C 오른쪽), A·C의 외각 이등분선(같은 각 표시)의 교점 P(오른쪽), "
             "D·E에 직각 표시, △PDA·△PEC 음영, DP=8 cm·AC=11 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.75,
    needs_review=("이미지에 별개 문항(아래쪽 '다음 그림에서 x의 값을 구하시오.' — ∠AOB 안의 점 P, PA⊥OA·PB⊥OB, PA=10 cm, PB=10 cm, OB=16 cm, OA=x cm; 답 16) 1개가 더 인쇄됨(id 1개) — 위쪽 문항만 전사 / "
                  + FIG + "삼각형·외각 이등분선 도형"),
    note="합=△PAC=½·11·8=44 cm². 빠른정답 없음.")

# ════════ 삼각형의 닮음 조건 ════════
# p1
add(id="6498090e", qtype="choice",
    question="다음 두 삼각형은 서로 닮음이다.\n삼각형의 닮음 조건 중 어떤 것을 만족하는가?",
    choices=["세 쌍의 대응변의 길이가 각각 같다.", "세 쌍의 대응변의 길이의 비가 각각 같다.", "두 쌍의 대응변의 길이가 각각 같고 그 끼인각의 크기가 같다.",
             "두 쌍의 대응변의 길이의 비가 각각 같고 그 끼인각의 크기가 같다.", "두 쌍의 대응각의 크기가 각각 같다."],
    derived_answer="④",
    figure=U("두 삼각형: 큰 삼각형은 두 변 10·8과 끼인각 70°, 작은 삼각형은 두 변 5·4와 끼인각 70°(치수는 점선 호)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "두 삼각형 치수 도형",
    note="10:5=8:4, 끼인각 70° 공통 → SAS 닮음 ④ = 빠른정답 ✓.")

# p16
add(id="5c857224", qtype="choice",
    question="다음 그림에서 [[3a = 2d]], [[3b = 2e]]일 때, 한 가지 조건을 추가하면 [[sim(tri(ABC), tri(DEF))]]가 된다. 이때 필요한 조건은?",
    choices=["[[c = f]]", "[[2c = 3f]]", "[[angle(C) = angle(F)]]", "[[angle(C) = 2 angle(F)]]", "[[2 angle(C) = 3 angle(F)]]"], derived_answer="③",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래; BC=a, CA=b, AB=c)와 더 큰 삼각형 DEF(D 위, E 왼쪽 아래, F 오른쪽 아래; EF=d, FD=e, DE=f), 변 길이는 점선 호로 표시"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "두 삼각형 변 이름 도형",
    note="a:d=b:e=2:3 → 끼인각 ∠C=∠F(SAS 닮음) → ③ = 빠른정답 ✓.")

# p31
add(id="f0038d74", qtype="choice",
    question=("아래 그림과 같은 [[tri(ABC)]]에서 [[angle(B) = angle(ACD)]]이고 [[seg(AD) = 4]] cm, [[seg(BC) = 10]] cm, [[seg(AC) = 8]] cm일 때, "
              "다음 중 옳지 않은 것은?"),
    choices=["[[sim(tri(ABC), tri(ACD))]]", "[[angle(ACB) = angle(ADC)]]", "[[ratio(seg(AD), seg(CD)) = ratio(seg(AC), seg(BC))]]",
             "[[ratio(seg(AB), seg(AC)) = ratio(2, 1)]]", "[[seg(CD) = 6]] cm"],
    derived_answer="⑤",
    figure=U("삼각형 ABC(A 오른쪽 위, B 왼쪽, C 아래 오른쪽), AB 위의 점 D와 선분 CD, ∠B와 ∠ACD에 같은 각 표시, AD=4 cm·AC=8 cm·BC=10 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형 닮음 치수 도형",
    note="AB:AC=AC:AD → AB=16, BC:CD=2:1 → CD=5 → ⑤ 틀림 = 빠른정답 ✓.")

# p32
add(id="298ace7b", qtype="short",
    question="다음 그림과 같은 [[tri(ABC)]]에서 [[angle(ABC) = angle(DAC)]]이고 [[seg(AC) = 7]], [[seg(DC) = 5]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="frac(49,5)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), BC 위의 점 D와 선분 AD, ∠B와 ∠DAC에 같은 각 표시, AC=7·DC=5·BC=x 치수(점선 호)"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "삼각형 닮음 치수 도형",
    note="△ABC∽△DAC → 7:5=x:7 → x=49/5 = 빠른정답 ✓.")
