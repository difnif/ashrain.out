# -*- coding: utf-8 -*-
# esc_sonnet_m1-2_4of4 — 이미지 기준 전사 (20 항목 / 20쪽, 삼각형의 합동)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]

# ---------------- 삼각형의 합동 조건(2) SAS합동 p55
add(id="91676789", qtype="short",
    question=("다음 그림과 같은 정사각형 ABCD에서 [[seg(PA) = seg(PD)]], [[angle(ABP) = deg(28)]]일 때, "
              "[[angle(BPC)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(56)",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 변 AD 위쪽에 점 P, PA=PD 같은 길이 표시, 선분 PB·PC, ∠ABP=28° 표시(B), P에 각 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 위 이등변삼각형 복합 도형",
    note="△PAB≡△PDC(SAS) → PB=PC, ∠PBC=∠PCB=62° → ∠BPC=56°. 빠른정답 'SSS 합동'과 불일치(정렬 어긋남).")

# ---------------- p57
add(id="549079fb", qtype="choice",
    question="다음 그림에서 [[seg(AB) = seg(AC)]], [[seg(BD) = seg(CE)]]일 때 옳지 않은 것은?",
    choices=["[[cong(tri(ABE), tri(ACD))]]", "[[cong(tri(DBF), tri(ECF))]]", "[[seg(BF) = seg(EF)]]",
             "[[angle(ABF) = angle(ACF)]]", "[[cong(tri(ABF), tri(ACF))]]"],
    derived_answer="③",
    figure=U("점 A(왼쪽), D(오른쪽 위), E(오른쪽 아래); B는 AD 위, C는 AE 위, 선분 BE와 CD의 교점 F. AB=AC(이중 표시), BD=CE(단일 표시)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·교점 복합 도형",
    note="△ABE≡△ACD(SAS), △DBF≡△ECF(ASA) → BF=CF(EF 아님) → ③. 빠른정답 2와 불일치.")

# ---------------- p58
add(id="5139eb75", qtype="choice",
    question=("아래 그림과 같은 사각형 ABCD에서 [[seg(AO) = seg(DO)]], [[seg(BO) = seg(CO)]]일 때, 다음 중 옳은 것을 모두 고르면? "
              "(단, 점 O는 두 대각선의 교점이다.)"),
    choices=["[[cong(tri(AOD), tri(COB))]]", "[[cong(tri(ABD), tri(CDB))]]", "[[cong(tri(AOB), tri(DOC))]]",
             "[[cong(tri(ABC), tri(DCB))]]", "[[cong(tri(AOD), tri(COD))]]"],
    derived_answer="③, ④",
    figure=U("사다리꼴 모양 사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC·BD의 교점 O"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형·대각선 복합 도형",
    note="△AOB≡△DOC(SAS, 맞꼭지각), AC=BD·∠ACB=∠DBC → △ABC≡△DCB(SAS) → ③, ④. 빠른정답 없음.")

# ---------------- p59
add(id="014b29b4", qtype="short",
    question="다음 그림에서 [[seg(OA) = seg(OB)]], [[seg(AC) = seg(BD)]]일 때, [[angle(DAO)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(125)",
    figure=U("점 O(왼쪽), C(오른쪽 위), D(오른쪽 아래); A는 OC 위, B는 OD 위, 선분 AD와 BC의 교점 E. OA=OB(단일 표시), AC=BD(이중 표시), ∠AOB=30°(O), ∠OCB=25°(C), A에 각 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·교점 복합 도형(각도 30°·25°가 그림에만 있음)",
    note="OC=OD, ∠O 공통 → △OCB≡△ODA(SAS) → ∠ODA=25°, ∠DAO=180−30−25=125°. 빠른정답 없음.")

# ---------------- p60
add(id="338ea0fc", qtype="choice",
    question=("아래 그림에서 [[seg(AB) = seg(BC)]], [[seg(AD) = seg(CE)]]일 때, 다음 중 [[tri(ACD)]]와 [[tri(CAE)]]가 합동이 되는 조건이 "
              "아닌 것은? (정답 2개)"),
    choices=["[[seg(AD) = seg(CE)]]", "[[seg(AB) = seg(BC)]]", "[[angle(A) = angle(C)]]", "[[seg(AC)]]는 공통", "[[angle(B)]]는 공통"],
    derived_answer="②, ⑤",
    figure=U("삼각형 ABC(A 왼쪽 위, C 오른쪽 위, B 아래), D는 AB 위, E는 CB 위, 선분 AE와 CD가 교차. AD=CE 같은 길이 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·교차 선분 도형",
    note="△ACD≡△CAE(SAS)의 조건은 AD=CE, ∠A=∠C, AC 공통 → 아닌 것 ②, ⑤. 빠른정답 '3, 4'와 불일치.")

# ---------------- p61
add(id="b7082dad", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 꼭짓점 B에서 변 AC에 내린 수선의 발을 D라 하자. "
              "또한, 변 AC 위에 [[seg(CD) = seg(DE)]]가 되도록 점 E를 잡고 변 AB 위에 [[seg(BF) = seg(CE)]]가 되도록 점 F를 잡으면 "
              "[[angle(CBD) = deg(27)]]일 때, [[angle(BCF)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(54)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 AC 위(직각 표시, BD⊥AC), E는 AC 위 D의 위쪽(CD=DE 같은 길이 표시), F는 AB 위, 선분 BD·BE·CF, ∠CBD=27°(B), C에 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 이등변삼각형·수선·교차 선분 복합 도형",
    note="∠BCA=63°, BD는 CE의 수직이등분선 → BE=BC, ∠EBC=54°; △FBC≡△ECB(SAS) → ∠BCF=∠CBE=54°. 빠른정답 '3, 4'와 불일치.")

# ---------------- p63
add(id="922d2ce5", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 꼭짓점 B에서 변 AC에 내린 수선의 발을 D라 하자. "
              "또한, 변 AC 위에 [[seg(CD) = seg(DE)]]가 되도록 점 E를 잡고 변 AB 위에 [[seg(BF) = seg(CE)]]가 되도록 점 F를 잡으면 "
              "[[angle(CBD) = deg(24)]]일 때, [[angle(BCF)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(48)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 AC 위(직각 표시, BD⊥AC), E는 AC 위 D의 위쪽(CD=DE 같은 길이 표시), F는 AB 위, 선분 BD·BE·CF, ∠CBD=24°(B), C에 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 이등변삼각형·수선·교차 선분 복합 도형",
    note="∠BCA=66°, BE=BC → ∠EBC=48°; △FBC≡△ECB(SAS) → ∠BCF=48°. 빠른정답 '2, 5'와 불일치.")

# ---------------- 삼각형의 합동 조건(3) ASA합동 p67
add(id="2b7777b8", qtype="short",
    question=("다음 그림에서 점 M은 [[seg(AB)]]의 중점이고 [[angle(ABQ) = deg(25)]], [[angle(APM) = deg(50)]], [[seg(AP) = seg(BQ)]]이다. "
              "이때 [[angle(PMA)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(75)",
    figure=U("점 A(왼쪽 아래), B(오른쪽 아래), M은 AB의 중점(같은 길이 표시), P(위), Q는 선분 PM 위(P와 M 사이), 선분 AP·PM·BQ, AP=BQ 같은 길이 표시, ∠APM=50°(P), ∠ABQ=25°(B), M에 각 표시"),
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 삼각형·중점·교차 선분 도형",
    note="사인법칙으로 AP=BQ ⇔ sin∠BQM=sin50° → ∠BQM=50°, ∠BMQ=105°, ∠PMA=75°(유일). 중학 풀이 경로 불명, 답 검토 요망. 빠른정답 없음.")

# ---------------- p70
add(id="4dd86a15", qtype="short",
    question=("다음 그림에서 [[par(l, m)]]이다. 점 M이 [[seg(AB)]]의 중점이고 [[cong(tri(AMC), tri(BMD))]]임을 설명할 때, "
              "사용되는 합동조건을 구하시오."),
    choices=None, derived_answer="ASA 합동",
    figure=U("평행한 두 직선 m(위, 점 A·C)과 l(아래, 점 D·B), 선분 AB와 CD의 교점 M, AM=BM 같은 길이 표시"),
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·교차 선분 도형",
    note="AM=BM, 엇각 두 쌍 → ASA 합동 = 빠른정답 ✓.")

# ---------------- p74
add(id="c2573a06", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 직각이등변삼각형 ABC의 꼭짓점 A를 지나는 직선 [[l]] 위에 두 점 B, C에서 내린 "
              "수선의 발을 각각 D, E라 하자. [[seg(CE) = 5]] cm, [[seg(DE) = 16]] cm일 때, [[seg(BD)]]의 길이는?"),
    choices=["[[9]] cm", "[[11]] cm", "[[13]] cm", "[[15]] cm", "[[17]] cm"],
    derived_answer="②",
    figure=U("A를 지나는 기울어진 직선 l, l 위의 점 D(A의 왼쪽)·E(A의 오른쪽), B(왼쪽 아래)·C(오른쪽 아래), 직각 표시 D·A·E, AB=AC 같은 길이 표시, 선분 BD·CE"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각이등변삼각형·수선 복합 도형",
    note="△ADB≡△CEA(RHA) → AD=CE=5, BD=AE=16−5=11 → ② = 빠른정답 ✓.")

# ---------------- 삼각형의 합동의 활용(1) 정삼각형 p79
add(id="304c96c6", qtype="choice",
    question=("아래 그림에서 [[tri(ACD)]], [[tri(CBE)]]가 정삼각형이고, [[seg(BD)]]와 [[seg(AE)]]의 교점을 P라 할 때, "
              "다음 설명 중 옳지 않은 것은?"),
    choices=["[[seg(AC) + seg(CE) = seg(DC) + seg(CB)]]", "[[angle(ACE) = angle(DCB)]]", "[[cong(tri(CQB), tri(EQB))]]",
             "[[angle(APD) = deg(60)]]", "[[cong(tri(ACE), tri(DCB))]]"],
    derived_answer="③",
    figure=U("한 직선 위의 점 A(왼쪽)·C·B(오른쪽), 위쪽에 정삼각형 ACD(같은 길이 단일 표시)와 정삼각형 CBE(원 표시), 선분 BD와 AE의 교점 P, 선분 BD와 CE의 교점 Q"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형 2개·교점 복합 도형",
    note="△ACE≡△DCB(SAS), ∠APD=60°; △CQB≡△EQB는 근거 없음 → ③. 빠른정답 없음.")

# ---------------- p82
add(id="97a867f6", qtype="short",
    question=("다음 그림과 같이 정삼각형 ABC의 한 변 BC 위에 점 D를 잡고 [[seg(AD)]]를 한 변으로 하는 정삼각형 ADE를 그렸다. "
              "[[seg(AB) = 12]] cm, [[seg(CD) = 4]] cm일 때, [[seg(CE)]]의 길이를 구하시오."),
    choices=None, derived_answer="8 cm",
    figure=U("정삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 BC 위(C 근처), 정삼각형 ADE(E 오른쪽), 선분 AE·DE·CE, AB=12 cm(점선 호), CD=4 cm(점선 호)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형 2개 복합 도형",
    note="△ABD≡△ACE(SAS) → CE=BD=12−4=8 cm. 빠른정답 3과 불일치.")

# ---------------- p83
add(id="789f94dd", qtype="short",
    question=("다음 그림과 같이 정삼각형 ABC의 한 변 BC 위에 점 D를 잡고 [[seg(AD)]]를 한 변으로 하는 정삼각형 ADE를 그렸다. "
              "[[seg(AB) = 16]] cm, [[seg(CD) = 6]] cm일 때, [[seg(CE)]]의 길이를 구하시오."),
    choices=None, derived_answer="10 cm",
    figure=U("정삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 BC 위(C 근처), 정삼각형 ADE(E 오른쪽), 선분 AE·DE·CE, AB=16 cm(점선 호), CD=6 cm"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형 2개 복합 도형",
    note="△ABD≡△ACE(SAS) → CE=BD=16−6=10 cm. 빠른정답 없음.")

# ---------------- p87
add(id="4701d96a", qtype="short",
    question=("다음 그림의 [[tri(ABC)]]에서 [[seg(AC) = seg(DC)]]인 점 D가 [[seg(BC)]] 위에 있다. [[seg(BC) = 12]] cm, "
              "[[angle(ACB) = deg(100)]], [[angle(BAD) = deg(10)]]일 때, [[seg(AD)]]의 길이를 구하시오."),
    choices=None, derived_answer="12 cm",
    figure=U("삼각형 ABC(B 왼쪽 아래, C 오른쪽 아래, A 오른쪽 위), D는 BC 위, 선분 AD, ∠BAD=10°(A), ∠ACB=100°(C), BC=12 cm(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·내부 선분 도형",
    note="∠CAD=∠CDA=40°, ∠B=30°, ∠ADB=140°; 사인법칙으로 BD+DC=AD(2sin10°+sin40°/sin100°=1) → AD=BC=12 cm. 빠른정답 '7 cm'와 불일치.")

# ---------------- p88
add(id="270040fa", qtype="short",
    question=("다음 그림과 같이 정삼각형 ABC의 [[seg(AB)]] 위의 점 D에서 그은 직선이 [[seg(AC)]]의 연장선과 만나는 점을 E, "
              "[[seg(BC)]]와 만나는 점을 F라 하자. [[seg(BD) = seg(CE) = 6]](cm), [[seg(DE) = 20]] cm일 때, [[seg(DF)]]의 길이를 구하시오."),
    choices=None, derived_answer="10 cm",
    figure=U("정삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 AB 위, E는 AC의 연장선 위(C 아래쪽), 직선 DE와 BC의 교점 F, BD=6 cm·CE=6 cm·DE=20 cm(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형·연장선·교점 복합 도형",
    note="D에서 AC에 평행한 선분 DG(G는 BC 위) → △DBG 정삼각형, DG=CE → △DGF≡△ECF(ASA) → DF=EF=10 cm. 빠른정답 2와 불일치.")

# ---------------- 삼각형의 합동의 활용(2) 정사각형 p89
add(id="d846378d", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 8인 정사각형 ABCD에서 삼각형 PBC는 [[angle(PBC) = angle(PCB) = deg(15)]]인 이등변삼각형이다. "
              "두 삼각형 PBC와 QAB가 합동일 때, 선분 AP의 길이를 구하시오."),
    choices=None, derived_answer="8",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD=8(점선 호), 내부의 점 P(아래쪽 중앙)·Q(왼쪽), 선분 AP·DP·BP·CP·AQ·BQ·PQ, ∠PBC=∠PCB=15° 표시"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 내부 삼각형 복합 도형",
    note="△QBP 정삼각형(∠QBP=60°, QB=PB) → QA=QP, ∠AQP=150° → ∠QAP=15°, ∠PAD=60° → △APD 정삼각형 → AP=8. 빠른정답 '5 cm'와 불일치.")

# ---------------- p90
add(id="354e4604", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 7인 정사각형 ABCD에서 삼각형 PBC는 [[angle(PBC) = angle(PCB) = deg(15)]]인 이등변삼각형이다. "
              "두 삼각형 PBC와 QAB가 합동일 때, 선분 AP의 길이를 구하시오."),
    choices=None, derived_answer="7",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD=7(점선 호), 내부의 점 P(아래쪽 중앙)·Q(왼쪽), 선분 AP·DP·BP·CP·AQ·BQ·PQ, ∠PBC=∠PCB=15° 표시"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 내부 삼각형 복합 도형",
    note="△QBP 정삼각형 → △APD 정삼각형 → AP=AD=7. 빠른정답 '12 cm'와 불일치.")

# ---------------- p93 (빈칸 (가)~(마))
add(id="7ebdbab3", qtype="choice",
    question=("다음은 아래 그림과 같은 정사각형 ABCD와 정삼각형 EBC에 대하여 [[tri(EAB) = tri(EDC)]]임을 설명하는 과정이다. "
              "(가)~(마)에 알맞은 것으로 옳지 않은 것을 모두 고르면? (정답 2개)\n"
              "[[tri(EAB)]]와 [[tri(EDC)]]에서\n"
              "(가) = [[seg(DC)]], (나) = [[seg(EC)]],\n"
              "(다) = [[angle(ABC) - angle(EBC)]]\n"
              "= [[angle(DCB)]] − (라)\n"
              "= (마)\n"
              "∴ [[cong(tri(EAB), tri(EDC))]] (SAS 합동)"),
    choices=["(가) [[seg(AB)]]", "(나) [[seg(EB)]]", "(다) [[angle(AEB)]]", "(라) [[angle(ECB)]]", "(마) [[angle(DEC)]]"],
    derived_answer="③, ⑤",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내부 위쪽의 점 E, 정삼각형 EBC, 선분 AE·DE"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 내부 정삼각형 도형",
    note="(다)=∠ABE, (마)=∠DCE가 옳음 → 틀린 것 ③(∠AEB), ⑤(∠DEC). 본문 '△EAB= △EDC'는 원문 그대로(= 기호). 빠른정답 7과 불일치.")

# ---------------- p98
add(id="07916f0b", qtype="choice",
    question=("다음 그림에서 [[quad(ABCD)]]와 [[quad(EFGC)]]는 정사각형이고 [[angle(ABG) = deg(66)]], [[angle(GCB) = deg(34)]]일 때, "
              "[[angle(DEF)]]의 크기는?"),
    choices=["[[deg(30)]]", "[[deg(32)]]", "[[deg(34)]]", "[[deg(36)]]", "[[deg(38)]]"],
    derived_answer="②",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), C를 꼭짓점으로 하는 기울어진 정사각형 EFGC(G는 ABCD 내부, F는 G 위쪽, E는 변 CD 오른쪽 바깥), 선분 BG·DE, ∠ABG=66°(B), ∠GCB=34°(C), E에 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 2개 복합 도형",
    note="△BCG≡△DCE(SAS) → ∠CDE=24°, ∠CED=122° → ∠DEF=122−90=32° → ②. 빠른정답 없음.")

# ---------------- p99
add(id="466c8934", qtype="short",
    question=("다음 그림에서 두 사각형 ABCD, CEFG는 모두 정사각형이고 [[seg(AG) = seg(DG)]]이다. [[seg(AB) = 10]]일 때, "
              "사각형 GCED의 넓이를 구하시오."),
    choices=None, derived_answer="75",
    figure=U("정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), G는 AD의 중점(같은 길이 표시), 기울어진 정사각형 CEFG(E 오른쪽, F 오른쪽 위), 선분 BG·DE, 사각형 GCED 보라색 음영, AB=10(점선 호)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 2개·음영 사각형 복합 도형",
    note="좌표 A(0,10) B(0,0) C(10,0) D(10,10) G(5,10) E(20,5): △GCD=25, △CDE=50 → 75. 빠른정답 50과 불일치.")
