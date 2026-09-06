# -*- coding: utf-8 -*-
# esc_sonnet_m2-2_2of5 — 이미지 기준 전사 (83 항목 / 80쪽) — 중2-2 삼각형의 닮음 조건·확률·평행선과 선분의 길이의 비·닮은 도형
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))
def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]

FIG = "도형 표현 불가: "

# ═══════════════ 삼각형의 닮음 조건 ═══════════════
# p36
add(id="f61f5df4", qtype="short",
    question=("다음 그림의 [[tri(ABC)]]에서 [[angle(BAE) = angle(CBF) = angle(ACD)]]이고, [[seg(AC) = 6]] cm, [[seg(DF) = 3]] cm, "
              "[[seg(DE) = seg(EF) = 4]] cm일 때, [[tri(ABC)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="22 cm",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 세 선분 AE·BF·CD가 내부에서 만나 삼각형 DEF를 이룸"
             "(D는 AE·CD 위 A 근처, E는 AE·BF 위 B 근처, F는 BF·CD 위 C 근처), ∠BAE·∠CBF·∠ACD에 점 표시, "
             "DE=4 cm·DF=3 cm·EF=4 cm·AC=6 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "삼각형·세 선분 복합 도형",
    note="△DEF∽△ABC(D↔A, E↔B, F↔C), 닮음비 DF:AC=1:2 → 둘레 2×(4+4+3)=22 cm = 빠른정답 ✓.")

# p41
add(id="f0c6ffa9", qtype="short",
    question=("다음 그림과 같은 정삼각형 ABC에서 [[angle(BDE) = deg(60)]] 이고 [[seg(AD) = 16]] cm, [[seg(CD) = 4]] cm일 때, "
              "[[seg(CE)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(16,5) cm",
    figure=U("정삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AC 위의 점 D(AD=16 cm, DC=4 cm 점선 호), BC 위의 점 E(C 근처), "
             "선분 BD·DE, ∠BDE=60° 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "정삼각형·내부 선분 도형",
    note="△ABD∽△CDE(AA): AB:CD=AD:CE → 20:4=16:CE → CE=16/5 cm. 빠른정답 없음.")

# p42
add(id="53a5efe1", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[angle(A) = angle(CED)]]이고 [[seg(AD) = 2]] cm, [[seg(CD) = 10]] cm, [[seg(CE) = 8]] cm일 때, "
              "[[seg(BE)]]의 길이는?"),
    choices=["[[5]] cm", "[[5.5]] cm", "[[6]] cm", "[[6.5]] cm", "[[7]] cm"], derived_answer="⑤",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AC 위의 점 D(AD=2 cm, DC=10 cm), BC 위의 점 E(EC=8 cm), 선분 DE, "
             "∠A·∠CED에 점 표시, 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·내부 선분 도형",
    note="△CED∽△CAB: 8:12=10:BC → BC=15, BE=7 cm → ⑤ = 빠른정답 ✓.")

# p49
add(id="48491e20", qtype="choice",
    question=("다음 그림과 같이 한 변의 길이가 [[16]] cm인 정사각형 ABCD에서 [[ratio(seg(DE), seg(EO)) = ratio(5, 3)]]이다. "
              "[[seg(CE)]]의 연장선과 [[seg(AD)]]의 교점을 F라 할 때, [[seg(DF)]]의 길이는? (단, 점 O는 두 대각선의 교점이다.)"),
    choices=["[[frac(78,11)]] cm", "[[frac(79,11)]] cm", "[[frac(80,11)]] cm", "[[frac(81,11)]] cm", "[[frac(82,11)]] cm"],
    derived_answer="③",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC·BD와 교점 O, BD 위의 점 E(O와 D 사이), "
             "C에서 E를 지나 AD와 만나는 점 F, 왼쪽 변 16 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "정사각형·대각선·연장선 복합 도형",
    note="좌표 B(0,0): E=(11,11), 직선 CE와 AD(y=16)의 교점 F=(96/11,16) → DF=80/11 cm → ③. 빠른정답 26 cm과 불일치(정렬 어긋남 의심).")

# p51
add(id="02ca5d91", qtype="short",
    question=("다음 그림에서 [[par(seg(AB), seg(ED))]], [[par(seg(AE), seg(BC))]]이고 [[seg(BC) = 27]] cm, [[seg(AE) = 12]] cm, "
              "[[seg(AC) = 36]] cm일 때, [[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="20 cm",
    figure=U("A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래(직각삼각형 모양), A의 오른쪽에 E(AE=12 cm), AC 위의 점 D(ED∥AB, 화살표 표시), "
             "AC=36 cm·BC=27 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "평행선·삼각형 복합 도형",
    note="△AED∽△CBA(E↔B): AE:CB=AD:CA → 12:27=AD:36 → AD=16, CD=20 cm. 빠른정답 3과 불일치(정렬 어긋남 의심).")

# p52
add(id="cbc6e974", qtype="short",
    question=("다음 그림의 정사각형 ABCD에서 [[seg(CD)]] 위의 한 점 E를 잡고 [[seg(BE)]]의 연장선과 [[seg(AD)]]의 연장선의 교점을 F라 하자. "
              "[[seg(AF) = 12]] cm, [[seg(BC) = 9]] cm, [[seg(EF) = frac(15,4)]] cm일 때, [[seg(BE)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(45,4) cm",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), CD 위의 점 E, BE의 연장선과 AD의 연장선의 교점 F(D 오른쪽), "
             "AF=12 cm·BC=9 cm·EF=15/4 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "정사각형·연장선 도형",
    note="△FDE∽△FAB: FD:FA=3:12 → FB=4·EF=15 → BE=15−15/4=45/4 cm. 빠른정답 없음.")

# p55
add(id="9cf45ea6", qtype="short",
    question=("다음 그림과 같은 직각삼각형 ABC에서 [[angle(A)]]의 이등분선이 [[seg(BC)]]와 만나는 점을 E, 점 E에서 [[seg(AB)]]에 내린 수선의 발을 D라 하자. "
              "[[seg(AC) = 15]] cm, [[seg(BD) = 24]] cm, [[seg(BE) = 26]] cm일 때, [[x]]의 값을 구하시오."),
    choices=None, derived_answer="10",
    figure=U("직각삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, C에 직각 표시), A의 각 이등분선(점 2개)이 BC와 만나는 점 E, "
             "E에서 AB에 내린 수선의 발 D(직각 표시), BD=24 cm·BE=26 cm·AC=15 cm·EC=x cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "직각삼각형·각 이등분선·수선 복합 도형(EC=x cm는 그림에만 있음)",
    note="DE=EC=x, △BDE∽△BCA: x:15=24:(26+x) → x²+26x−360=0 → x=10 = 빠른정답 ✓.")

# p56
add(id="8d85dddf", qtype="short",
    question=("다음 그림과 같은 직사각형 ABCD에서 대각선 AC는 [[seg(PQ)]]를 수직이등분하고 점 O는 [[seg(PQ)]]와 [[seg(AC)]]의 교점이다. "
              "[[seg(AB) = 8]] cm, [[seg(BC) = 6]] cm, [[seg(AO) = 5]] cm일 때, [[tri(OCP)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="15 cm",
    figure=U("직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; AB=8 cm 세로, BC=6 cm 가로), 대각선 AC, "
             "CD 위의 점 P와 AB 위의 점 Q를 잇는 PQ가 AC와 O에서 수직으로 만남(직각 표시, OP=OQ 등호 표시), AO=5 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "직사각형·수직이등분선 복합 도형",
    note="AC=10, OC=5, ∠OCP=∠ACD=∠BAC → △COP∽△ABC: 5:8=OP:6=CP:10 → OP=15/4, CP=25/4 → 둘레 15 cm = 빠른정답 ✓.")

# p58
add(id="03ba84f3", qtype="choice",
    question="다음 그림에서 [[perp(seg(AB), seg(CE))]], [[perp(seg(AC), seg(BD))]] 일 때, [[seg(BE)]] 의 길이는?",
    choices=["[[15]]", "[[16]]", "[[17]]", "[[20]]", "[[21]]"], derived_answer="③",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 E(C에서 내린 수선의 발, 직각 표시), "
             "AC 위의 점 D(B에서 내린 수선의 발, 직각 표시), AE=4·AD=6·DC=8 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·두 수선 도형(치수 4·6·8은 그림에만 있음)",
    note="△AEC∽△ADB: AE:AD=AC:AB → 4:6=14:AB → AB=21, BE=17 → ③ = 빠른정답 ✓.")

# p59
add(id="7748080f", qtype="short",
    question="다음 그림과 같이 [[angle(A) = deg(90)]] 인 직각삼각형 ABC에서 [[perp(seg(AD), seg(BC))]]일 때, [[x + y]]의 값을 구하시오.",
    choices=None, derived_answer="12",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각 표시), A에서 BC에 내린 수선의 발 D(직각 표시), "
             "AB=x cm·AD=4 cm·AC=5 cm·BD=y cm·DC=3 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·수선 도형(치수 x·4·5·y·3 cm는 그림에만 있음)",
    note="AD²=BD·DC → y=16/3; AB²=BD·BC → x=20/3 → x+y=12 = 빠른정답 ✓.")

# p61
add(id="f117592f", qtype="choice",
    question=("다음 그림과 같이 [[angle(C) = deg(90)]] 이고 [[seg(BC) = 12]] cm, [[seg(AC) = 36]] cm인 직각삼각형 ABC의 변 AB 위의 점 D에서 "
              "[[seg(BC)]], [[seg(AC)]]에 내린 수선의 발을 각각 E, F라 하자. [[quad(DECF)]]가 정사각형일 때, [[quad(DECF)]]의 넓이는?"),
    choices=["[[49]] cm²", "[[64]] cm²", "[[81]] cm²", "[[100]] cm²", "[[121]] cm²"], derived_answer="③",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, C에 직각), AB 위의 점 D, D에서 BC·AC에 내린 수선의 발 E·F(직각 표시), "
             "정사각형 DECF 음영, AC=36 cm·BC=12 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형 내접 정사각형 도형",
    note="한 변 s: (12−s):12=s:36 → s=9 → 81 cm² → ③ = 빠른정답 ✓.")

# p62
add(id="03c138ed", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 5]] cm, [[seg(BC) = 10]] cm인 직사각형 ABCD와 한 변의 길이가 [[20]] cm인 정사각형 ECFG가 있다. "
              "[[seg(BD)]]의 연장선과 [[seg(GF)]]의 교점을 H라 할 때, 사각형 EDHG의 넓이를 구하시오. (단, 세 점 B, C, F는 한 직선 위에 있다.)"),
    choices=None, derived_answer="200 cm²",
    figure=U("직사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위; AB=5 cm, BC=10 cm)와 그 오른쪽에 붙은 정사각형 ECFG"
             "(C 왼쪽 아래, F 오른쪽 아래, G 오른쪽 위, E 왼쪽 위; CF=20 cm), D는 CE 위, BD의 연장선이 GF와 만나는 점 H, 사각형 EDHG 음영"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "직사각형·정사각형 복합 도형",
    note="직선 BD 기울기 1/2 → FH=15, HG=5, ED=15 → 사다리꼴 EDHG=(15+5)/2×20=200 cm². 빠른정답 없음.")

# p65
add(id="3fb46169", qtype="choice",
    question=("다음 그림과 같이 [[angle(B) = deg(90)]] 인 직각삼각형 ABC의 두 점 A, C에서 점 B를 지나는 직선에 내린 수선의 발을 각각 D, E라 하자. "
              "[[seg(AD) = 24]] cm, [[seg(BE) = 48]] cm, [[seg(CE) = 20]] cm일 때, [[seg(BD)]]의 길이는?"),
    choices=["[[8]] cm", "[[10]] cm", "[[12]] cm", "[[14]] cm", "[[16]] cm"], derived_answer="②",
    figure=U("직각삼각형 ABC(A 왼쪽 위, C 오른쪽 위, B 아래쪽 직선 위, B에 직각 표시), B를 지나는 수평 직선 위의 수선의 발 D(A 아래)·E(C 아래) 직각 표시, "
             "AD=24 cm·BE=48 cm·CE=20 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·두 수선 도형",
    note="△ADB∽△BEC: AD:BE=DB:EC → 24:48=BD:20 → BD=10 cm → ② = 빠른정답 ✓.")

# p71
add(id="12a640b7", qtype="short",
    question=("다음 그림과 같이 정사각형 ABCD의 두 변 BC, CD 위의 두 점 E, F에서 대각선 AC에 내린 수선의 발을 각각 P, Q라 하자. "
              "[[angle(EAF) = deg(45)]] 이고 [[seg(AP) = 15]] cm, [[seg(AQ) = 20]] cm일 때, [[quad(ABCD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="300 cm²",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, 전체 음영), 대각선 AC, BC 위의 점 E와 CD 위의 점 F, "
             "선분 AE·AF(∠EAF=45° 표시), E·F에서 AC에 내린 수선의 발 P·Q(직각 표시), AP=15 cm·AQ=20 cm 치수(점선 호)"),
    difficulty_est=4, confidence=0.75,
    needs_review=FIG + "정사각형·대각선·두 수선 복합 도형",
    note="∠EAF=45°이면 AP·AQ=(한 변)² → 넓이 15×20=300 cm². 빠른정답 1과 불일치(정렬 어긋남 의심).")

# p78
add(id="4196e2d3", qtype="choice",
    question="다음 그림의 [[tri(ABC)]]에서 [[angle(BAC) = angle(ADC) = deg(90)]], [[seg(AC) = 12]] cm, [[seg(CD) = 8]] cm일 때, [[seg(BD)]]의 길이는?",
    choices=["[[14]] cm", "[[13]] cm", "[[12]] cm", "[[11]] cm", "[[10]] cm"], derived_answer="⑤",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각), A에서 BC에 내린 수선의 발 D(직각), AC=12 cm·DC=8 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·수선 도형",
    note="AC²=CD·CB → CB=18, BD=10 cm → ⑤ = 빠른정답 ✓.")

# p80
add(id="fed65524", qtype="short",
    question="다음 그림과 같이 [[angle(A) = deg(90)]] 인 직각삼각형 ABC에서 [[perp(seg(AH), seg(BC))]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="15",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각), A에서 BC에 내린 수선의 발 H(직각), AH=x cm·HC=25 cm·BC=34 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·수선 도형(치수 x·25·34 cm는 그림에만 있음)",
    note="BH=9, x²=BH·HC=225 → x=15 = 빠른정답 ✓.")

# p81
add(id="fdb8d348", qtype="short",
    question="다음 그림과 같이 [[angle(A) = deg(90)]] 인 직각삼각형 ABC에서 [[perp(seg(AH), seg(BC))]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="5",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각), A에서 BC에 내린 수선의 발 H(직각), AB=6·BH=4·HC=x 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·수선 도형(치수 6·4·x는 그림에만 있음)",
    note="AB²=BH·BC → 36=4(4+x) → x=5 = 빠른정답 ✓.")

# p82
add(id="cda96d23", qtype="short",
    question="다음 그림과 같이 [[angle(C) = deg(90)]] 인 직각삼각형 ABC에서 [[perp(seg(CH), seg(AB))]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="6",
    figure=U("직각삼각형 ABC(C 위, A 왼쪽 아래, B 오른쪽 아래, C에 직각), C에서 AB에 내린 수선의 발 H(직각), AC=x cm·AH=4 cm·AB=9 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·수선 도형(치수 x·4·9 cm는 그림에만 있음)",
    note="AC²=AH·AB=36 → x=6 = 빠른정답 ✓.")

# p84
add(id="4acb948b", qtype="short",
    question="다음 그림에서 [[seg(BC) = 5]], [[seg(AC) = 3]], [[angle(ABC) = angle(CAD)]] 일 때, [[x]] 의 값을 구하시오.",
    choices=None, derived_answer="frac(9,5)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), A에서 BC에 내린 수선의 발 D(직각 표시), ∠ABC·∠CAD에 점 표시, "
             "AC=3·BC=5·DC=x 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·수선 도형(DC=x는 그림에만 있음)",
    note="∠BAC=90°이므로 AC²=CD·CB → 9=5x → x=9/5 = 빠른정답 ✓.")

# p85
add(id="a1a4654e", qtype="short",
    question="다음 그림과 같이 [[angle(A) = deg(90)]] 인 직각삼각형 ABC에서 [[perp(seg(AH), seg(BC))]]일 때, [[x + y]]의 값을 구하시오.",
    choices=None, derived_answer="frac(56,5)",
    figure=U("직각삼각형 ABC(B 오른쪽 위, A 오른쪽 아래(직각), C 왼쪽 아래), A에서 BC에 내린 수선의 발 H(직각), "
             "AB=6 cm·CA=8 cm·CB=10 cm·CH=x·AH=y 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·수선 도형(치수 6·8·10 cm·x·y는 그림에만 있음)",
    note="AC²=CH·CB → x=32/5; AH=AB·AC/BC=24/5 → x+y=56/5 = 빠른정답 ✓.")

# p86
add(id="68c993cc", qtype="choice",
    question="다음 그림에서 [[angle(BAC) = deg(90)]], [[angle(ADC) = deg(90)]] 일 때, [[tri(ABC)]]의 넓이는?",
    choices=["[[80]]", "[[96]]", "[[120]]", "[[135]]", "[[150]]"], derived_answer="⑤",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각, 내부 음영), A에서 BC에 내린 수선의 발 D(직각), AC=15·DC=9 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·수선 도형(치수 15·9는 그림에만 있음)",
    note="AC²=DC·BC → BC=25, AD=12 → 넓이 ½·25·12=150 → ⑤ = 빠른정답 ✓.")

# p91 — 종이접기, B′
add(id="040e6f4c", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]] 인 직각삼각형 모양의 종이 ABC에서 [[seg(AB)]]의 중점을 D, 점 D에서 [[seg(BC)]]에 내린 수선의 발을 E라 하자. "
              "이 종이를 [[seg(DE)]]를 접는 선으로 하여 꼭짓점 B가 [[seg(BC)]] 위의 점 B′에 오도록 접었다. "
              "[[seg(AB) = 6]] cm, [[seg(BC) = 10]] cm일 때, B′C의 길이를 구하시오."),
    choices=None, derived_answer="frac(32,5) cm",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각, 음영), AB의 중점 D(등호 표시), D에서 BC에 내린 수선의 발 E(직각), "
             "접힌 뒤 B가 옮겨간 BC 위의 점 B′, AB=6 cm·BC=10 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.75,
    needs_review="프라임 점 라벨(B′, 선분 B′C는 텍스트) / " + FIG + "직각삼각형 접기 도형",
    note="DB=3, BE=DB·AB/BC=9/5, BB′=2BE=18/5 → B′C=10−18/5=32/5 cm. 빠른정답 없음.")

# p95
add(id="f79031cc", qtype="short",
    question=("다음 그림과 같이 직사각형 모양의 종이 ABCD를 꼭짓점 B가 [[seg(AD)]] 위의 점 F에 오도록 접었다. "
              "[[seg(AE) = 6]] cm, [[seg(AF) = 8]] cm, [[seg(BC) = 20]] cm일 때, [[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="16 cm",
    figure=U("직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래(점선), C 오른쪽 아래), AB 위의 점 E와 C를 잇는 접는 선 EC, "
             "B가 옮겨간 AD 위의 점 F, 선분 EF·FC, AE=6 cm·AF=8 cm·BC=20 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직사각형 접기 도형",
    note="EF=EB=10 → AB=16 → CD=16 cm = 빠른정답 ✓ (△AEF∽△DFC: 6:12=8:DC로도 확인).")

# p96
add(id="802cd4b2", qtype="short",
    question=("다음 그림과 같이 [[seg(AD) = 10]]인 직사각형 ABCD의 두 변 AD, BC의 중점을 각각 E, F라 하면 [[sim(quad(ABCD), quad(AEFB))]]이다. "
              "[[quad(ABCD)]]를 [[seg(DF)]]를 접는 선으로 하여 점 C가 점 G에 오도록 접었을 때, 점 G에서 [[seg(AB)]], [[seg(AD)]]에 내린 수선의 발을 각각 H, I라 하자. "
              "이때 [[seg(AI)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(10,3)",
    figure=U("직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래(점선)), AD의 중점 E·BC의 중점 F, 접는 선 DF, "
             "C가 옮겨간 내부의 점 G(회전 화살표), G에서 AB·AD에 내린 수선의 발 H·I(직각 표시), 접힌 부분 음영, AD=10 치수(점선 호)"),
    difficulty_est=4, confidence=0.75,
    needs_review=FIG + "직사각형 접기 복합 도형",
    note="AB²=AE·AD=50; C를 직선 DF에 대칭이동한 G의 가로 좌표 = AD/3 → AI=10/3 = 빠른정답 ✓.")

# p97
add(id="7fb7925b", qtype="short",
    question=("다음 그림과 같이 [[seg(AD) = 12]]인 직사각형 ABCD의 두 변 AD, BC의 중점을 각각 E, F라 하면 [[sim(quad(ABCD), quad(AEFB))]]이다. "
              "[[quad(ABCD)]]를 [[seg(DF)]]를 접는 선으로 하여 점 C가 점 G에 오도록 접었을 때, 점 G에서 [[seg(AB)]], [[seg(AD)]]에 내린 수선의 발을 각각 H, I라 하자. "
              "이때 [[seg(AI)]]의 길이를 구하시오."),
    choices=None, derived_answer="4",
    figure=U("직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래(점선)), AD의 중점 E·BC의 중점 F, 접는 선 DF, "
             "C가 옮겨간 내부의 점 G(회전 화살표), G에서 AB·AD에 내린 수선의 발 H·I(직각 표시), 접힌 부분 음영, AD=12 치수(점선 호)"),
    difficulty_est=4, confidence=0.75,
    needs_review=FIG + "직사각형 접기 복합 도형",
    note="AB²=AE·AD=72; G의 가로 좌표 = AD/3 → AI=4 = 빠른정답 ✓.")

# ═══════════════ 확률의 뜻과 성질 ═══════════════
# p57
add(id="49f27940", qtype="short",
    question=("두 개의 주사위 A, B를 동시에 던져서 나오는 두 눈의 수를 각각 [[a]], [[b]]라 할 때, 일차함수 [[y = a x + b]]의 그래프가 "
              "점 [[point(2, 11)]]을 지날 확률을 구하시오."),
    choices=None, derived_answer="frac(1,12)", figure=None, difficulty_est=2, confidence=0.9,
    note="2a+b=11: (3,5),(4,3),(5,1) → 3/36=1/12 = 빠른정답 ✓.")

# p61
add(id="da4dc711", qtype="short",
    question=("A, B 두 개의 주사위를 던져 나온 눈의 수를 각각 [[a]], [[b]]라 하자. 이때 [[x]]에 대한 일차방정식 [[a x = b]]의 해가 정수가 될 확률을 구하시오."),
    choices=None, derived_answer="frac(7,18)", figure=None, difficulty_est=2, confidence=0.9,
    note="b/a가 정수: 6+3+2+1+1+1=14 → 14/36=7/18 = 빠른정답 ✓.")

# p62
add(id="8cd826f1", qtype="short",
    question=("A, B 두 개의 주사위를 동시에 던질 때, A주사위에서 나온 눈의 수를 [[a]], B주사위에서 나온 눈의 수를 [[b]]라 하자. "
              "이때 연립방정식 [[x + 3y = 5]], [[a x + b y = 8]]의 해가 존재하지 않을 확률을 구하시오."),
    choices=None, derived_answer="frac(1,18)", figure=None, difficulty_est=2, confidence=0.9,
    note="해 없음 ⇔ b=3a(a/1=b/3≠8/5): (1,3),(2,6) → 2/36=1/18 = 빠른정답 ✓. 연립방정식 중괄호는 콤마 나열.")

# p63
add(id="a9a454a8", qtype="short",
    question=("한 개의 주사위를 두 번 던져서 첫 번째에 나온 눈의 수를 [[a]], 두 번째에 나온 눈의 수를 [[b]]라 할 때, "
              "연립방정식 [[x + 2y = 1]], [[3x + a y = b]]의 해가 존재하지 않을 확률을 구하시오."),
    choices=None, derived_answer="frac(5,36)", figure=None, difficulty_est=2, confidence=0.9,
    note="a=6, b≠3 → 5/36 = 빠른정답 ✓. 연립방정식 중괄호는 콤마 나열.")

# p64
add(id="294d5b2a", qtype="short",
    question=("한 개의 주사위를 두 번 던져서 첫 번째에 나온 눈의 수를 [[a]], 두 번째에 나온 눈의 수를 [[b]]라 할 때, "
              "연립방정식 [[2x + 4y = 5]], [[x + a y = b]]의 해가 존재하지 않을 확률을 구하시오."),
    choices=None, derived_answer="frac(1,6)", figure=None, difficulty_est=2, confidence=0.9,
    note="a=2(b는 임의, 5/2≠정수) → 6/36=1/6 = 빠른정답 ✓. 연립방정식 중괄호는 콤마 나열.")

# ═══════════════ 평행선과 선분의 길이의 비 ═══════════════
# p5
add(id="266fd67b", qtype="choice",
    question="아래 그림과 같은 [[tri(ABC)]]에서 [[par(seg(DE), seg(AC))]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[ratio(seg(AB), seg(AD)) = ratio(seg(BC), seg(CE))]]",
             "[[ratio(seg(BD), seg(AB)) = ratio(seg(BE), seg(BC))]]",
             "[[ratio(seg(BC), seg(BE)) = ratio(seg(AC), seg(DE))]]",
             "[[ratio(seg(BD), seg(DA)) = ratio(seg(DE), seg(AC))]]",
             "[[ratio(seg(BD), seg(DA)) = ratio(seg(BE), seg(EC))]]"],
    derived_answer="④",
    figure=U("삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 D와 BC 위의 점 E를 잇는 DE가 AC와 평행(화살표 표시)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "삼각형·평행선 도형",
    note="DE:AC=BD:BA이므로 ④가 거짓. 빠른정답 없음.")

# p9
add(id="4f1b719d", qtype="choice",
    question="다음 그림에서 [[par(seg(BC), seg(DE))]]일 때, [[tri(ABC)]]의 둘레의 길이는?",
    choices=["[[36]] cm", "[[38]] cm", "[[40]] cm", "[[42]] cm", "[[44]] cm"], derived_answer="①",
    figure=U("나비 모양: 위쪽 선분 ED(ED=5 cm, 화살표)와 아래쪽 선분 BC(화살표), B–A–D·C–A–E가 각각 한 직선(A는 교점), "
             "EA=3 cm·AD=4 cm·AC=9 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "나비 모양 두 삼각형 도형(치수 5·3·4·9 cm는 그림에만 있음)",
    note="△ADE∽△ABC(AE:AC=1:3): AB=12, BC=15 → 둘레 12+15+9=36 cm → ①. 빠른정답 없음.")

# p19
add(id="dfe71935", qtype="short",
    question="다음 그림에서 [[par(seg(DE), seg(BC))]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="frac(10,3)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AB 위의 점 D·AC 위의 점 E(DE∥BC), A에서 내린 선분이 DE·BC와 만나는 점 P·Q, "
             "DP=3·PE=2·BQ=5·QC=x 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·평행선 도형(치수 3·2·5·x는 그림에만 있음)",
    note="DP:PE=BQ:QC → 3:2=5:x → x=10/3 = 빠른정답 ✓.")

# p21
add(id="2f37644b", qtype="short",
    question="다음 그림과 같은 삼각형에서 [[par(seg(DE), seg(BC))]] 일 때, [[frac(x, y)]] 의 값을 구하여라.",
    choices=None, derived_answer="frac(5,7)",
    figure=U("삼각형 ADE(A 위, D 왼쪽 아래, E 오른쪽 아래), AD 위의 점 B·AE 위의 점 C(BC∥DE), A에서 아래로 내린 선분, "
             "AB=10·BD=4·BC=x·DE=y 치수(점선 호)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "삼각형·평행선 도형(치수 10·4·x·y는 그림에만 있음)",
    note="x/y=AB/AD=10/14=5/7 = 빠른정답 ✓.")

# p22
add(id="6fe62e0a", qtype="choice",
    question=("다음 그림에서 [[ratio(seg(BP), seg(PC)) = ratio(3, 2)]], [[ratio(seg(AQ), seg(QC)) = ratio(3, 4)]] 이다. "
              "[[seg(AR) = 9]]cm 일 때, [[seg(RP)]] 의 길이는?"),
    choices=["[[6.2]]cm", "[[7.2]]cm", "[[8]]cm", "[[9]]cm", "[[9.2]]cm"], derived_answer="②",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), BC 위의 점 P, AC 위의 점 Q, AP와 BQ의 교점 R, AR=9 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "삼각형·두 선분 교점 도형",
    note="질량점 A=4, B=2, C=3 → AR:RP=5:4 → RP=36/5=7.2 cm → ②. 빠른정답 없음.")

# p26 (id 2개) — 선지 5개가 그림
dup(["48837e7a", "d63b12c2"], qtype="choice",
    question="다음 그림에서 [[par(seg(DE), seg(BC))]]인 것은?",
    choices=["(그림) 삼각형 ABC(B 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(AD) = 20]], [[seg(DB) = 4]], [[seg(AE) = 15]], [[seg(EC) = 5]]",
             "(그림) 삼각형 ADE에서 AD 위의 점 B, AE 위의 점 C: [[seg(DB) = 2]], [[seg(BA) = 4]], [[seg(DE) = 8]], [[seg(BC) = 6]]",
             "(그림) 두 선분 BD, CE가 점 A에서 만나는 나비 모양: [[seg(BA) = 3]], [[seg(CA) = 4]], [[seg(AE) = 10]], [[seg(AD) = 6]]",
             "(그림) 삼각형 ABC(A 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(BA) = 8]], [[seg(BD) = 3]], [[seg(AE) = 4]], [[seg(EC) = 1]]",
             "(그림) 두 선분 EC, DB가 점 A에서 만나는 나비 모양: [[seg(EA) = 20]], [[seg(AC) = 4]], [[seg(DA) = 15]], [[seg(AB) = 3]]"],
    derived_answer="⑤",
    figure=U("선지 ①~⑤가 각각 도형: ① △ABC(A 왼쪽 아래, B 위, C 오른쪽 아래), D∈AB, E∈AC, AD=20·DB=4·AE=15·EC=5 "
             "② D–B–A 가로 배열(DB=2, BA=4), C∈AE, DE=8, BC=6 ③ 나비 모양(B–A–D, C–A–E 직선), BA=3·CA=4·AE=10·AD=6 "
             "④ △ABC(B 왼쪽 아래, A 오른쪽 위, C 오른쪽 아래), D∈BA, E∈AC, BA=8·BD=3·AE=4·EC=1 "
             "⑤ 나비 모양(E–A–C, D–A–B 직선), EA=20·AC=4·DA=15·AB=3 (치수는 점선 호)"),
    difficulty_est=2, confidence=0.75,
    needs_review="선지 5개가 도형 그림(그림 설명 텍스트로 대체) / " + FIG + "삼각형·나비 모양 도형 5개",
    note="⑤: AE:AC=AD:AB=5:1 → DE∥BC. ①~④는 대응 비가 다름. 빠른정답 없음.")

# p28 (id 3개) — 선지 5개가 그림
dup(["dd9a2e1c", "9b33e483", "f10ce79e"], qtype="choice",
    question="다음 중에서 [[par(seg(BC), seg(DE))]] 인 것은?",
    choices=["(그림) 삼각형 ADE(A 위)에서 AD 위의 점 B, AE 위의 점 C: [[seg(AB) = 3]], [[seg(BD) = 1.5]], [[seg(AC) = 4]], [[seg(CE) = 3]]",
             "(그림) 삼각형 ABC(C 위)에서 AC 위의 점 E, AB 위의 점 D: [[seg(AE) = 6]], [[seg(EC) = 4]], [[seg(AD) = 5]], [[seg(DB) = 3]]",
             "(그림) 두 선분 BD, CE가 점 A에서 만나는 나비 모양: [[seg(BA) = 6]], [[seg(CA) = 9]], [[seg(AE) = 15]], [[seg(AD) = 10]]",
             "(그림) 삼각형 ABC(A 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(AD) = 8]], [[seg(AB) = 12]], [[seg(AE) = 6]], [[seg(AC) = 10]]",
             "(그림) 두 선분 EC, DB가 점 A에서 만나는 나비 모양: [[seg(EA) = 4]], [[seg(AD) = 3]], [[seg(AB) = 5]], [[seg(AC) = 6]]"],
    derived_answer="③",
    figure=U("선지 ①~⑤가 각각 도형: ① △ADE(A 위, D 왼쪽 아래, E 오른쪽 아래), B∈AD, C∈AE, AB=3·BD=1.5·AC=4·CE=3 "
             "② △ABC(C 위, A 왼쪽 아래, B 오른쪽 아래), E∈AC, D∈AB, AE=6·EC=4·AD=5·DB=3 "
             "③ 나비 모양(B–A–D, C–A–E 직선), BA=6·CA=9·AE=15·AD=10 "
             "④ △ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D∈AB, E∈AC, AD=8·AB=12·AE=6·AC=10 "
             "⑤ 나비 모양(E–A–C, D–A–B 직선), EA=4·AD=3·AB=5·AC=6 (치수는 점선 호)"),
    difficulty_est=2, confidence=0.75,
    needs_review="선지 5개가 도형 그림(그림 설명 텍스트로 대체) / " + FIG + "삼각형·나비 모양 도형 5개",
    note="③: AB:AD=AC:AE=3:5 → BC∥DE. 나머지는 대응 비가 다름. 빠른정답 없음.")

# p31
add(id="145bb3fc", qtype="short",
    question="다음 그림에서 [[seg(AD)]]는 [[angle(A)]]의 이등분선일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="frac(5,2)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), A의 각 이등분선(점 2개)이 BC와 만나는 점 D, AB=6·AC=5·BD=3·DC=x 치수(점선 호)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "삼각형·각 이등분선 도형(치수 6·5·3·x는 그림에만 있음)",
    note="AB:AC=BD:DC → 6:5=3:x → x=5/2 = 빠른정답 ✓.")

# p34
add(id="7e9d9493", qtype="short",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AD)]]는 [[angle(A)]]의 이등분선이다. 점 C를 지나고 [[seg(AD)]]에 평행한 직선이 "
              "[[seg(BA)]]의 연장선과 만나는 점을 E라 할 때, [[x y]]의 값을 구하시오."),
    choices=None, derived_answer="12",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), A의 각 이등분선(점 2개)이 BC와 만나는 점 D, "
             "C를 지나 AD와 평행한 직선이 BA의 연장선과 만나는 점 E(A 위쪽), AB=6 cm·AC=4 cm·BD=x cm·DC=2 cm·AE=y cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·각 이등분선·평행선 도형(치수 6·4·x·2·y cm는 그림에만 있음)",
    note="x:2=6:4 → x=3; AE=AC(이등변) → y=4 → xy=12 = 빠른정답 ✓.")

# p40
add(id="750f40df", qtype="short",
    question="다음 그림과 같은 [[tri(ABC)]] 에서 [[angle(BAD) = angle(CAD) = deg(45)]] 일 때, [[tri(ABD)]] 의 넓이를 구하여라.",
    choices=None, derived_answer="frac(96,7) cm²",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각 표시), A의 각 이등분선(점 2개)이 BC와 만나는 점 D, AB=8 cm·AC=6 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "직각삼각형·각 이등분선 도형(치수 8·6 cm는 그림에만 있음)",
    note="△ABC=24, BD:DC=8:6=4:3 → △ABD=24·4/7=96/7 cm². 빠른정답 없음.")

# p41
add(id="2eeda7ae", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 [[4]] cm인 마름모 ABCD에서 [[seg(CD)]] 위의 한 점 E에 대하여 [[seg(AD)]]와 [[seg(BE)]]의 연장선의 교점을 F, "
              "[[seg(AC)]]와 [[seg(BE)]]의 교점을 G라 하자. [[seg(DF) = 1]] cm일 때, [[ratio(tri(BCG), tri(CEG))]]를 가장 간단한 자연수의 비로 나타내면 "
              "[[ratio(a, b)]]이다. 이때 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="20",
    figure=U("마름모 ABCD(A 위, B 왼쪽, C 아래, D 오른쪽), 대각선 AC, CD 위의 점 E, BE의 연장선과 AD의 연장선의 교점 F(D 오른쪽), "
             "AC와 BE의 교점 G, AB=4 cm·DF=1 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "마름모·연장선 복합 도형",
    note="DE:EC=DF:BC=1:4 → CE=16/5; CG는 ∠BCE의 이등분선 → BG:GE=CB:CE=5:4 → ab=20 = 빠른정답 ✓.")

# p42
add(id="0297bfb3", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 [[8]] cm인 마름모 ABCD에서 [[seg(CD)]] 위의 한 점 E에 대하여 [[seg(AD)]]와 [[seg(BE)]]의 연장선의 교점을 F, "
              "[[seg(AC)]]와 [[seg(BE)]]의 교점을 G라 하자. [[seg(DF) = 3]] cm일 때, [[ratio(tri(BCG), tri(CEG))]]를 가장 간단한 자연수의 비로 나타내면 "
              "[[ratio(a, b)]]이다. 이때 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="88",
    figure=U("마름모 ABCD(A 위, B 왼쪽, C 아래, D 오른쪽), 대각선 AC, CD 위의 점 E, BE의 연장선과 AD의 연장선의 교점 F(D 오른쪽), "
             "AC와 BE의 교점 G, AB=8 cm·DF=3 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "마름모·연장선 복합 도형",
    note="DE:EC=3:8 → CE=64/11; BG:GE=CB:CE=8:64/11=11:8 → ab=88 = 빠른정답 ✓.")

# p47
add(id="6bd9512f", qtype="short",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AD)]]는 [[angle(A)]]의 외각의 이등분선이다. [[seg(AB) = 6]] cm, [[seg(AC) = 9]] cm, "
              "[[seg(DB) = 8]] cm일 때, [[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="4 cm",
    figure=U("삼각형 ABC(A 위, B 아래 가운데, C 오른쪽 아래), BC의 연장선(B 왼쪽) 위의 점 D, A의 외각의 이등분선 AD(점 2개), "
             "AB=6 cm·AC=9 cm·DB=8 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·외각 이등분선 도형",
    note="AB:AC=DB:DC → 6:9=8:DC → DC=12 → BC=4 cm = 빠른정답 ✓.")

# p48
add(id="b74581d9", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[angle(A)]]의 외각의 이등분선과 [[seg(BC)]]의 연장선의 교점을 D라 할 때, "
              "[[frac(seg(BD), seg(BC))]]의 값은?"),
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"], derived_answer="②",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 아래 가운데), BC의 연장선(C 오른쪽) 위의 점 D, A의 외각의 이등분선 AD(점 표시), "
             "AB=5 cm·AC=4 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·외각 이등분선 도형(치수 5·4 cm는 그림에만 있음)",
    note="BD:CD=AB:AC=5:4 → BC=BD−CD=1단위 → BD/BC=5 → ②. 빠른정답 없음.")

# p49
add(id="845fb026", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[angle(A)]]의 외각의 이등분선과 [[seg(BC)]]의 연장선의 교점을 D라 할 때, "
              "[[frac(seg(BD), seg(BC))]]의 값은?"),
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"], derived_answer="⑤",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 아래 가운데), BC의 연장선(C 오른쪽) 위의 점 D, A의 외각의 이등분선 AD(점 표시), "
             "AB=8 cm·AC=7 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·외각 이등분선 도형(치수 8·7 cm는 그림에만 있음)",
    note="BD:CD=8:7 → BC=1단위 → BD/BC=8 → ⑤. 빠른정답 없음.")

# p51
add(id="86be6773", qtype="short",
    question=("다음 그림에서 [[seg(AD)]]는 [[angle(BAC)]]의 이등분선이고 [[seg(AE)]]는 [[angle(CAF)]]의 이등분선이다. "
              "[[seg(AB) = 10]], [[seg(AC) = 6]], [[seg(BD) = 5]]일 때, [[x]]의 값을 구하시오."),
    choices=None, derived_answer="12",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 아래), BC의 연장선 위의 점 E(C 오른쪽), BA의 연장선 위의 점 F(A 위쪽), "
             "내각 이등분선 AD(D는 BC 위)와 외각 이등분선 AE(각 표시), AB=10·AC=6·BD=5·CE=x 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "삼각형·내각·외각 이등분선 도형(CE=x는 그림에만 있음)",
    note="DC=3, BC=8; BE:CE=10:6 → (8+x):x=5:3 → x=12 = 빠른정답 ✓.")

# p57
add(id="529e1c1e", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AB) = 15]] cm, [[seg(AC) = 12]] cm이다. [[angle(A)]]의 외각의 이등분선과 [[seg(BC)]]의 "
              "연장선의 교점을 D라 할 때, [[tri(ABC)]]와 [[tri(ACD)]]의 넓이의 비는?"),
    choices=["[[ratio(1, 3)]]", "[[ratio(1, 4)]]", "[[ratio(2, 3)]]", "[[ratio(2, 5)]]", "[[ratio(3, 4)]]"], derived_answer="②",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 아래; △ABC 초록 음영), BC의 연장선 위의 점 D(C 오른쪽), 외각 이등분선 AD(점 표시), "
             "△ACD 보라 음영, AB=15 cm·AC=12 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "삼각형·외각 이등분선 도형",
    note="BD:CD=15:12=5:4 → BC:CD=1:4 → ②. 빠른정답 없음.")

# p60
add(id="03313d65", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = 15]] cm, [[seg(CA) = 10]] cm인 [[tri(ABC)]]에서 [[angle(A)]]의 이등분선과 [[seg(BC)]]가 만나는 점을 D라 하고 "
              "[[angle(A)]]의 외각의 이등분선과 [[seg(BC)]]의 연장선이 만나는 점을 E라 할 때, 삼각형 ACE의 넓이가 [[20]] cm²이다. "
              "이때 삼각형 ADE의 넓이는?"),
    choices=["[[22]] cm²", "[[24]] cm²", "[[26]] cm²", "[[28]] cm²", "[[30]] cm²"], derived_answer="②",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 아래), 내각 이등분선 AD(D는 BC 위, ∘ 표시 2개)와 외각 이등분선 AE(E는 BC의 연장선 위, 점 표시), "
             "△ADE 음영, AB=15 cm·AC=10 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "삼각형·내각·외각 이등분선 도형",
    note="BC=5k: DC=2k, CE=10k → DE=12k; △ACE=20 → △ADE=24 cm² → ②. 빠른정답 없음.")

# p61
add(id="015682ef", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = 12]] cm, [[seg(CA) = 9]] cm인 [[tri(ABC)]]에서 [[angle(A)]]의 이등분선과 [[seg(BC)]]가 만나는 점을 D라 하고 "
              "[[angle(A)]]의 외각의 이등분선과 [[seg(BC)]]의 연장선이 만나는 점을 E라 할 때, 삼각형 ACE의 넓이가 [[27]] cm²이다. "
              "이때 삼각형 ADE의 넓이는?"),
    choices=["[[frac(215,7)]] cm²", "[[frac(216,7)]] cm²", "[[31]] cm²", "[[frac(218,7)]] cm²", "[[frac(219,7)]] cm²"], derived_answer="②",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 아래), 내각 이등분선 AD(D는 BC 위, ∘ 표시 2개)와 외각 이등분선 AE(E는 BC의 연장선 위, 점 표시), "
             "△ADE 음영, AB=12 cm·AC=9 cm 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "삼각형·내각·외각 이등분선 도형",
    note="BC=7k: DC=3k, CE=21k → DE=24k; △ACE=27 → △ADE=27·24/21=216/7 cm² → ②. 빠른정답 8과 불일치(정렬 어긋남 의심).")

# p62
add(id="1218fe3b", qtype="choice",
    question="다음 그림에서 [[par(par(l, m), n)]]일 때, [[x y]]의 값은?",
    choices=["[[42]]", "[[43]]", "[[44]]", "[[45]]", "[[46]]"], derived_answer="④",
    figure=U("세 평행선 l, m, n(위에서 아래)과 l·m 사이의 한 점에서 교차하는 두 직선; 오른쪽 아래로 내려가는 직선: l~교점 8 cm, 교점~m 4 cm, m~n 10 cm; "
             "왼쪽 아래로 내려가는 직선: l~교점 x cm, 교점~m 3 cm, m~n y cm (점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "평행선·교차하는 두 직선 도형(치수는 그림에만 있음)",
    note="8:4=x:3 → x=6; 3:y=4:10 → y=15/2 → xy=45 → ④. 빠른정답 없음.")

# p63
add(id="d346f646", qtype="short",
    question="다음 그림에서 [[par(par(l, m), n)]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="5",
    figure=U("세 평행선 l, m, n과 m·n 사이에서 교차하는 두 직선; 왼쪽 직선: l~m 6, m~n 18; 오른쪽 직선: l~m x, m~n 15 (점선 호)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "평행선·교차하는 두 직선 도형(치수 6·18·x·15는 그림에만 있음)",
    note="6:18=x:15 → x=5. 빠른정답 없음.")

# p65
add(id="573d5103", qtype="short",
    question=("다음은 원근법을 이용하여 그린 그림이다. [[par(par(seg(AB), seg(FC)), seg(ED))]]이고 [[seg(AF) = 10]] cm, [[seg(FE) = 14]] cm, "
              "[[seg(BC) = 14]] cm일 때, [[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(98,5) cm",
    figure=U("원근법으로 그린 복도 그림: 오른쪽 벽의 위쪽 선 위에 점 A, F, E와 아래쪽 선 위에 점 B, C, D, 세로 선분 AB·FC·ED가 평행, "
             "AF=10 cm·FE=14 cm·BC=14 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "원근법 복도 그림 위 평행선 도형",
    note="AF:FE=BC:CD → 10:14=14:CD → CD=98/5 cm. 빠른정답 없음.")

# p66
add(id="eff3638c", qtype="choice",
    question="다음 그림에서 [[par(par(l, m), n)]]일 때, [[x]]의 값은?",
    choices=["[[6]]", "[[frac(13,2)]]", "[[7]]", "[[frac(15,2)]]", "[[8]]"], derived_answer="④",
    figure=U("세 평행선 l, m, n과 두 직선; 왼쪽 비스듬한 직선: l~m x, l~n 12; 오른쪽 세로 직선: l~m 5, m~n 3 (점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "평행선·두 직선 도형(치수 x·12·5·3은 그림에만 있음)",
    note="x:12=5:8 → x=15/2 → ④. 빠른정답 없음.")

# p67
add(id="3ce095c6", qtype="short",
    question="다음 그림에서 [[par(par(l, m), n)]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="12",
    figure=U("세 평행선 l, m, n과 두 직선; 왼쪽 직선: l~m 8, m~n 6; 오른쪽 비스듬한 직선: l~m x, l~n 21 (점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "평행선·두 직선 도형(치수 8·6·x·21은 그림에만 있음)",
    note="x:21=8:14 → x=12 = 빠른정답 ✓.")

# p69
add(id="c824e6df", qtype="choice",
    question=("[[seg(AD) = 7]] cm, [[seg(BC) = 10]] cm인 등변사다리꼴의 각 변을 삼등분하여 다음 그림과 같이 9개의 부분으로 나누었다. "
              "(가) 부분과 (나) 부분의 넓이의 비를 가장 간단한 자연수의 비로 나타내면 [[ratio(a, b)]]일 때, [[a + b]]의 값은?"),
    choices=["[[32]]", "[[34]]", "[[36]]", "[[38]]", "[[40]]"], derived_answer="②",
    figure=U("등변사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; AD=7 cm, BC=10 cm 점선 호), 각 변의 삼등분점을 이어 3×3=9개 조각으로 분할, "
             "왼쪽 위 조각 (가)·오른쪽 아래 조각 (나) 음영"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "등변사다리꼴 9분할 도형",
    note="가로선 길이 7, 8, 9, 10; (가)=(7/3+8/3)/2·h/3, (나)=(3+10/3)/2·h/3 → 15:19 → a+b=34 → ②. 빠른정답 없음.")

# p71 — 좌표평면
add(id="b91cc64b", qtype="short",
    question=("세 직선 [[y = 4]], [[y = -1]], [[y = a]]([[a < 0]]) 와 직선 [[y = b x + c]] ([[b > 0]]) 의 교점을 각각 A, B, C 라 하고, "
              "점 A 를 지나는 직선 [[x = 24]] 와 [[y = -1]], [[y = a]] 의 교점을 각각 D, E 라 할 때, [[seg(AD) = 5]], [[seg(DE) = 5]], [[seg(BD) = 3]] 이다. "
              "이때, [[a - b - c]] 의 값을 구하여라."),
    choices=None, derived_answer="frac(85,3)",
    figure=U("좌표평면: 세 수평 점선 y=4, y=−1, y=a(a<0)와 기울기 양수인 직선 y=bx+c의 교점 A(위), B, C(아래), "
             "A를 지나는 수직선 x=24가 y=−1·y=a와 만나는 점 D, E; AD=5·DE=5 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "좌표평면 직선 도형",
    note="A(24,4), D(24,−1), E(24,−6) → a=−6; B(21,−1) → b=5/3, c=−36 → a−b−c=85/3 = 빠른정답 ✓.")

# p73
add(id="f0bd4a72", qtype="choice",
    question="다음 그림과 같은 사다리꼴 ABCD에서 [[par(par(seg(AD), seg(EF)), seg(BC))]]일 때, [[seg(EF)]] 의 길이는?",
    choices=["[[9]] cm", "[[frac(19,2)]] cm", "[[10]] cm", "[[frac(21,2)]] cm", "[[11]] cm"], derived_answer="③",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; AD=8 cm, BC=12 cm, 평행 화살표), "
             "AB 위의 점 E와 DC 위의 점 F(DF=5 cm, FC=5 cm) 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "사다리꼴·평행선 도형(치수 8·12·5·5 cm는 그림에만 있음)",
    note="F는 DC의 중점 → EF=(8+12)/2=10 cm → ③. 빠른정답 없음.")

# p75
add(id="f3c9b682", qtype="choice",
    question="다음 그림에서 [[par(par(l, m), n)]]일 때, [[5x + 3y]]의 값은?",
    choices=["[[28]]", "[[32]]", "[[36]]", "[[40]]", "[[44]]"], derived_answer="⑤",
    figure=U("세 평행선 l, m, n과 두 직선(왼쪽 세로 직선: l~m 4, m~n 5; 오른쪽 비스듬한 직선: l~m x, m~n 6), "
             "두 직선 사이의 길이 l 위 4, m 위 y, n 위 10 (점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "평행선·두 직선 도형(치수는 그림에만 있음)",
    note="x=6·4/5=24/5; y=4+(10−4)·4/9=20/3 → 5x+3y=24+20=44 → ⑤. 빠른정답 없음.")

# p77
add(id="3a3e60bc", qtype="short",
    question="다음 그림과 같은 사다리꼴 ABCD에서 [[par(par(seg(AD), seg(EF)), seg(BC))]]일 때, [[seg(EF)]] 의 길이를 구하시오.",
    choices=None, derived_answer="17",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; AD=14, BC=21, 평행 화살표), "
             "AB 위의 점 E(AE=6, EB=8)와 DC 위의 점 F, 대각선 AC와 EF의 교점 G 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "사다리꼴·대각선·평행선 도형(치수 14·21·6·8은 그림에만 있음)",
    note="EG=21·6/14=9, GF=14·8/14=8 → EF=17. 빠른정답 15 cm과 불일치(정렬 어긋남 의심).")

# p82
add(id="ec980a29", qtype="short",
    question=("다음 그림의 사다리꼴 ABCD에서 [[par(par(seg(AD), seg(PQ)), seg(BC))]] 이고 [[seg(BP) = frac(3,7) seg(BD)]], "
              "[[seg(CQ) = frac(3,7) seg(AC)]]일 때, [[seg(PQ)]]의 길이를 구하시오."),
    choices=None, derived_answer="6",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; AD=14, BC=21, 평행 화살표), 대각선 AC·BD, "
             "BD 위의 점 P와 AC 위의 점 Q(PQ∥BC, 화살표) 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "사다리꼴·두 대각선 도형(치수 14·21은 그림에만 있음)",
    note="PQ의 연장선이 AB와 만나는 점 E: EP=(3/7)AD=6, EQ=(4/7)BC=12 → PQ=6 = 빠른정답 ✓.")

# p87
add(id="c87962e5", qtype="short",
    question=("그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD의 대각선의 교점 O를 지나 [[seg(BC)]]에 평행한 직선이 [[seg(AB)]], [[seg(DC)]]와 "
              "만나는 점을 각각 E, F라 할 때, [[seg(EO)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(6,5) cm",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; AD=2 cm, BC=3 cm), 대각선 AC·BD의 교점 O, "
             "O를 지나 BC에 평행한 선분 EF(E는 AB 위, F는 DC 위) 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "사다리꼴·두 대각선 도형(치수 2·3 cm는 그림에만 있음)",
    note="EO=AD·BC/(AD+BC)=6/5 cm. 빠른정답 없음.")

# p89
add(id="482fe969", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 점 O는 두 대각선의 교점이고 [[seg(EF)]]는 점 O를 지난다. "
              "[[par(seg(EF), seg(BC))]]이고 [[seg(EO) = 20]] cm, [[seg(BC) = 36]] cm일 때, [[seg(AD)]]의 길이를 구하시오."),
    choices=None, derived_answer="45 cm",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; 평행 화살표), 대각선 AC·BD의 교점 O, "
             "O를 지나는 EF(E는 AB 위, F는 DC 위), EO=20 cm·BC=36 cm 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "사다리꼴·두 대각선 도형",
    note="EO=AD·BC/(AD+BC) → 20=36·AD/(AD+36) → AD=45 cm = 빠른정답 ✓.")

# p90
add(id="e77c4465", qtype="choice",
    question=("아래 그림과 같은 사다리꼴 ABCD에서 [[par(par(seg(AD), seg(EF)), seg(BC))]]이고 두 대각선 AC, DB의 교점 O는 [[seg(EF)]] 위의 점이다. "
              "다음 중 옳지 않은 것은?"),
    choices=["[[ratio(seg(AO), seg(CO)) = ratio(seg(AD), seg(CB))]]", "[[sim(tri(AOD), tri(COB))]]", "[[sim(tri(ABC), tri(AEO))]]",
             "[[seg(EO) = seg(OF)]]", "[[seg(BO) = seg(CO)]]"],
    derived_answer="⑤",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC·BD의 교점 O, O를 지나는 EF(E는 AB 위, F는 DC 위), "
             "AD·EF·BC에 평행 화살표"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "사다리꼴·두 대각선 도형",
    note="⑤ BO=CO는 일반적으로 성립하지 않음(①~④ 성립). 빠른정답 없음.")

# p91
add(id="69dbe014", qtype="choice",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 [[seg(AC)]]와 [[seg(BD)]]의 교점 O를 지나면서 [[seg(AD)]]에 평행한 직선과 "
              "[[seg(AB)]], [[seg(CD)]]의 교점을 각각 E, F라 하고 [[seg(BD)]]와 [[seg(CE)]]의 교점 G를 지나면서 [[seg(EF)]]에 평행한 직선과 [[seg(AC)]]의 교점을 "
              "H라 하자. [[seg(AD) = 6]] cm, [[seg(BC) = 18]] cm일 때, [[seg(GH)]]의 길이는?"),
    choices=["[[frac(12,5)]] cm", "[[frac(14,5)]] cm", "[[frac(16,5)]] cm", "[[frac(18,5)]] cm", "[[4]] cm"], derived_answer="④",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; AD=6 cm, BC=18 cm, 평행 화살표), 대각선 AC·BD의 교점 O, "
             "O를 지나 AD에 평행한 EF(E는 AB 위, F는 CD 위), 선분 CE, BD와 CE의 교점 G, G를 지나 EF에 평행한 선분이 AC와 만나는 점 H 치수(점선 호)"),
    difficulty_est=4, confidence=0.75,
    needs_review=FIG + "사다리꼴·대각선·평행선 복합 도형",
    note="B 원점 좌표: O 높이 3h/4, G=(3/5)D(높이 3h/5), H는 AC 위 같은 높이 → GH=18/5 cm → ④. 빠른정답 없음.")

# p92
add(id="5f13e571", qtype="choice",
    question=("다음 그림과 같은 사다리꼴 ABCD에서 [[par(par(seg(AD), seg(EF)), seg(BC))]]이고 두 대각선 AC, DB의 교점 O는 [[seg(EF)]] 위의 점이다. "
              "다음 중 옳지 않은 것은?"),
    choices=["[[sim(tri(ABD), tri(FDO))]]", "[[ratio(seg(AO), seg(OC)) = ratio(seg(AD), seg(BC))]]",
             "[[ratio(seg(AO), seg(OD)) = ratio(seg(CO), seg(OB))]]", "[[sim(tri(AOD), tri(COB))]]", "[[seg(EO) = seg(OF)]]"],
    derived_answer="①",
    figure=U("사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC·BD의 교점 O, O를 지나는 EF(E는 AB 위, F는 DC 위), "
             "AD·EF·BC에 평행 화살표"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "사다리꼴·두 대각선 도형",
    note="△FDO∽△CDB이지 △ABD와는 일반적으로 닮음이 아님 → ①. ②~⑤ 성립. 빠른정답 없음.")

# p98
add(id="1b9e8927", qtype="short",
    question="다음 그림에서 [[par(par(seg(AB), seg(DC)), seg(PH))]] 이고 [[seg(PH) = 5]] cm, [[seg(DC) = 12]] cm일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="frac(60,7)",
    figure=U("B 왼쪽 아래, C 오른쪽 아래, A는 B 위(AB=x cm), D는 C 위(DC=12 cm), AC와 BD의 교점 P, P에서 BC에 내린 수선의 발 H(PH=5 cm), "
             "AB∥DC∥PH 치수(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "평행 세 선분·교점 도형(AB=x cm는 그림에만 있음)",
    note="1/x+1/12=1/5 → x=60/7 = 빠른정답 ✓.")

# ═══════════════ 닮은 도형 ═══════════════
# p4 — 프라임 라벨
add(id="2fa14567", qtype="choice",
    question=("다음 그림에서 □ABCD∽□A′B′C′D′일 때, [[seg(BC)]]에 대응하는 변과 ∠D′에 대응하는 각을 순서대로 나열한 것은?"),
    choices=["[[seg(CD)]], [[angle(A)]]", "[[seg(CD)]], [[angle(D)]]", "BC′, [[angle(D)]]", "A′B′, ∠D′", "B′C′, [[angle(D)]]"],
    derived_answer="⑤",
    figure=U("사각형 ABCD(A 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위)와 이를 확대한 같은 배치의 사각형 A′B′C′D′"),
    difficulty_est=1, confidence=0.75,
    needs_review="프라임 점 라벨(A′B′C′D′; 선분·각 기호를 텍스트로 대체) / " + FIG + "닮은 두 사각형 도형",
    note="BC↔B′C′, ∠D′↔∠D → ⑤. 선지 ③은 원문대로 'BC′'(윗줄). 빠른정답 3과 불일치(정렬 어긋남 의심).")

# p6
add(id="bd7359b3", qtype="choice",
    question="다음 그림에서 [[sim(quad(ABCD), quad(EFGH))]]일 때, 점 B의 대응점, [[seg(EF)]]의 대응변, [[angle(C)]]의 대응각은?",
    choices=["점 E, [[seg(AB)]], [[angle(G)]]", "점 E, [[seg(BC)]], [[angle(H)]]", "점 F, [[seg(AB)]], [[angle(G)]]",
             "점 F, [[seg(BC)]], [[angle(H)]]", "점 F, [[seg(AB)]], [[angle(H)]]"],
    derived_answer="③",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)와 축소한 사각형 EFGH(F 왼쪽 위, G 오른쪽 위, E 왼쪽 아래, H 오른쪽 아래)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "닮은 두 사각형 도형",
    note="B↔F, EF↔AB, ∠C↔∠G → ③. 빠른정답 5와 불일치(정렬 어긋남 의심).")

# p7
add(id="42b3bc99", qtype="short",
    question="다음 그림에서 [[sim(quad(ABCD), quad(EFGH))]]일 때, 점 B의 대응점을 구하시오.",
    choices=None, derived_answer="점 F",
    figure=U("평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)와 확대한 평행사변형 EFGH(E 왼쪽 위, H 오른쪽 위, F 왼쪽 아래, G 오른쪽 아래)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "닮은 두 평행사변형 도형",
    note="B↔F. 빠른정답 5와 불일치(정렬 어긋남 의심).")

# p9
add(id="6e079cbe", qtype="choice",
    question="아래 그림에서 [[sim(tri(ABC), tri(DEF))]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[angle(B)]]의 대응각은 [[angle(E)]]이다.", "[[angle(D)]]의 대응각은 [[angle(A)]]이다.", "[[seg(AB)]]의 대응변은 [[seg(DE)]]이다.",
             "[[seg(BC)]]의 대응변은 [[seg(DE)]]이다.", "[[seg(AC)]]의 대응변은 [[seg(DF)]]이다."],
    derived_answer="④",
    figure=U("삼각형 ABC(A 왼쪽 위, C 오른쪽, B 아래)와 삼각형 DEF(E 위, F 왼쪽 아래, D 오른쪽 아래)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "닮은 두 삼각형 도형",
    note="BC의 대응변은 EF → ④가 거짓. 빠른정답 3과 불일치(정렬 어긋남 의심).")

# p12
add(id="e5e448c0", qtype="short",
    question="다음 그림에서 [[sim(quad(ABCD), quad(EFGH))]]일 때, 점 C의 대응점을 구하시오.",
    choices=None, derived_answer="점 G",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)와 확대한 사각형 EFGH(E 왼쪽 위, H 오른쪽 위, F 왼쪽 아래, G 오른쪽 아래)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "닮은 두 사각형 도형",
    note="C↔G. 빠른정답 4와 불일치(정렬 어긋남 의심).")

# p27
add(id="a79d7674", qtype="choice",
    question=("다음 그림에서 [[quad(ABCD)]] 와 [[quad(EFGH)]] 는 서로 닮음이고 [[angle(A) = deg(100)]], [[angle(C) = deg(120)]], "
              "[[angle(H) = deg(70)]] 일 때, [[angle(F)]] 의 크기는?"),
    choices=["[[deg(40)]]", "[[deg(50)]]", "[[deg(60)]]", "[[deg(70)]]", "[[deg(80)]]"], derived_answer="④",
    figure=U("사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; ∠A=100°, ∠C=120° 표시)와 축소한 사각형 EFGH"
             "(E 왼쪽 위, H 오른쪽 위, F 왼쪽 아래, G 오른쪽 아래; ∠H=70° 표시, F에 각 표시)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "닮은 두 사각형 도형",
    note="∠D=∠H=70°, ∠B=360−100−120−70=70° → ∠F=∠B=70° → ④ = 빠른정답 ✓.")

# p28
add(id="d0236a3b", qtype="short",
    question="다음 그림의 두 부채꼴이 닮은 도형일 때, [[angle(DEF)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(90)",
    figure=U("부채꼴 ABC(중심 B, 반지름 BC=6 cm, 중심각에 직각 표시)와 부채꼴 DEF(중심 E, 반지름 EF=9 cm) 치수(점선 호)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "두 부채꼴 도형(직각 표시·6 cm·9 cm는 그림에만 있음)",
    note="닮은 부채꼴은 중심각이 같음 → ∠DEF=∠ABC=90°. 빠른정답 없음.")

# p30
add(id="69703978", qtype="short",
    question="다음 그림의 두 부채꼴이 닮은 도형일 때, [[angle(DEF)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(70)",
    figure=U("부채꼴 ABC(중심 B, 중심각 70°, 반지름 BC=3 cm)와 부채꼴 DEF(중심 E, 반지름 EF=5 cm) 치수(점선 호)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "두 부채꼴 도형(70°·3 cm·5 cm는 그림에만 있음)",
    note="∠DEF=∠ABC=70°. 빠른정답 없음.")

# p32 — 프라임 라벨, 모눈
add(id="394a904d", qtype="choice",
    question="다음 그림에서 △A′B′C′ 는 [[tri(ABC)]] 를 확대한 것이다. 두 삼각형에 대한 설명으로 옳은 것은?",
    choices=["[[seg(AB)]] : A′B′ = 2 : 1", "∠A′ = 2∠A", "[[seg(AC)]] : A′C′ = [[seg(BC)]] : B′C′",
             "[[tri(ABC)]] = 2△A′B′C′", "[[tri(ABC)]] : △A′B′C′ = 1 : 3"],
    derived_answer="③",
    figure=U("모눈종이 위의 직각삼각형 ABC(B 왼쪽 아래, C 오른쪽 아래, A 위; BC 5칸, AC 3칸)와 2배 확대한 직각삼각형 A′B′C′(B′C′ 10칸, A′C′ 6칸)"),
    difficulty_est=1, confidence=0.75,
    needs_review="프라임 점 라벨(A′B′C′; 선분·삼각형·각 기호와 비를 텍스트로 대체) / " + FIG + "모눈 위 두 직각삼각형 도형",
    note="닮음비 1:2 → ①·②·④·⑤ 거짓, ③ 참 = 빠른정답 ✓.")

# p34
add(id="ad23ce92", qtype="short",
    question="다음 그림에서 [[sim(tri(ABC), tri(DEF))]]일 때, [[angle(E)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(40)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래; ∠B=40° 표시)와 축소한 삼각형 DEF(D 위, E 왼쪽 아래, F 오른쪽 아래)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "닮은 두 삼각형 도형(∠B=40°는 그림에만 있음)",
    note="∠E=∠B=40°. 빠른정답 없음.")

# p38
add(id="6a113a4f", qtype="choice",
    question="다음 그림에서 [[sim(tri(ABC), tri(DEF))]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[seg(AC)]]에 대응하는 변은 [[seg(DF)]] 이다.", "[[angle(A)]]에 대응하는 각은 [[angle(D)]]이다.",
             "[[seg(BC) = 4]] cm, [[seg(EF) = 2]] cm일 때, 닮음비는 [[ratio(2, 1)]]이다.",
             "[[seg(AB) = seg(DE)]] 이면 두 삼각형의 넓이는 같다.", "[[tri(ABC)]]가 정삼각형이면 두 삼각형은 항상 합동이다."],
    derived_answer="⑤",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)와 축소한 삼각형 DEF(D 위, E 왼쪽 아래, F 오른쪽 아래)"),
    difficulty_est=1, confidence=0.8,
    needs_review=FIG + "닮은 두 삼각형 도형",
    note="⑤: 정삼각형끼리는 닮음이지만 항상 합동은 아님(④는 닮음비 1:1이므로 참). 빠른정답 4와 불일치(정렬 어긋남 의심).")

# p45
add(id="abe5f1a9", qtype="choice",
    question=("[[sub(A,4)]]용지를 다음 그림과 같이 반씩 접어보고 접을 때마다 종이의 크기를 각각 [[sub(A,5)]], [[sub(A,6)]], [[sub(A,7)]], ⋯이라고 할 때, "
              "[[sub(A,6)]]용지의 가로와 세로의 길이는? (단, [[sub(A,4)]]용지의 가로의 길이는 [[210]] mm, 세로의 길이는 [[297]] mm이다.)"),
    choices=["가로: [[210]] mm, 세로: [[297]] mm", "가로: [[210]] mm, 세로: [[frac(297,2)]] mm", "가로: [[105]] mm, 세로: [[frac(297,2)]] mm",
             "가로: [[105]] mm, 세로: [[frac(297,4)]] mm", "가로: [[105]] mm, 세로: [[frac(297,8)]] mm"],
    derived_answer="③",
    figure=U("세로로 긴 직사각형(A₄ 용지)을 반씩 접은 분할 그림: 아래 절반 A₅, 왼쪽 위 A₆, 오른쪽 위의 아래쪽 A₇, 그 위 A₈, ⋯"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "종이 접기 분할 도형",
    note="A₅: 148.5×210, A₆: 105×148.5 → 가로 105 mm, 세로 297/2 mm → ③ = 빠른정답 ✓. 첨자 A₄ 등은 sub 표기.")

# p46
add(id="fe8c5b46", qtype="choice",
    question=("다음 그림과 같이 A판 전지를 반으로 자르고, 그 반을 또 반으로 자르는 과정을 반복하면 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯의 용지를 얻을 수 있다. "
              "처음 A판 전지의 가로의 길이를 [[a]], 세로의 길이를 [[b]]라 할 때, 각 용지들이 서로 닮음이 되도록 하는 [[a]]와 [[b]] 사이의 관계식은?"),
    choices=["[[pow(a,2) = pow(b,2)]]", "[[pow(a,2) = 2 pow(b,2)]]", "[[pow(a,2) = 4 pow(b,2)]]", "[[2 pow(a,2) = pow(b,2)]]", "[[2 pow(a,2) = 3 pow(b,2)]]"],
    derived_answer="④",
    figure=U("가로 a, 세로 b인 직사각형 전지를 반씩 자른 분할 그림: 아래 절반 A₁, 왼쪽 위 A₂, 오른쪽 위의 위쪽 A₃, 그 아래 오른쪽 A₄, ⋯; "
             "a(아래)·b(왼쪽) 치수(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "종이 분할 도형",
    note="a:b=(b/2):a → 2a²=b² → ④ = 빠른정답 ✓.")

# p47
add(id="59a006c8", qtype="short",
    question=("다음 그림과 같은 직사각형 ABCD에서 [[sim(sim(quad(ABCD), quad(DAEF)), quad(AEHG))]]이고 [[seg(BC) = 48]] cm, [[seg(CD) = 64]] cm일 때, "
              "[[seg(HF)]] 의 길이를 구하시오."),
    choices=None, derived_answer="21 cm",
    figure=U("직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래; BC=48 cm, CD=64 cm 점선 호), "
             "AB 위의 점 E와 DC 위의 점 F를 잇는 가로 선분 EF, AD 위의 점 G와 EF 위의 점 H를 잇는 세로 선분 GH"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG + "직사각형 분할 도형",
    note="AE=48·48/64=36, EH=36·36/48=27 → HF=48−27=21 cm = 빠른정답 ✓.")
