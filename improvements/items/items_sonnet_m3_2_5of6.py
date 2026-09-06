# -*- coding: utf-8 -*-
# esc_sonnet_m3-2_5of6 — 이미지 기준 전사 (81 항목 / 80쪽)
# 원의 접선과 현이 이루는 각 p91~p99, 원주각 p5~p99, 삼각비의 활용(1) 길이 p1~p70
# 거의 전부 정보성 기하 도형(원·삼각형·입체) → unsupported + needs_review "도형 표현 불가"
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ======================= 원의 접선과 현이 이루는 각 =======================
# ---------------- p91
add(id="c65afc34", qtype="short",
    question=("다음 그림에서 직선 PQ는 두 원의 공통인 접선이고 점 T는 접점이다. "
              "[[angle(ABD) = deg(75)]]일 때, [[angle(x) + angle(y)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(150)",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 안에 작은 원이 점 T에서 내접, 세로 직선 PQ(공통 접선, P 위·Q 아래, T 접점). 큰 원 위 A(좌상)·B(좌하), 작은 원 위 C(선분 AT 위)·D(선분 BT 위). 세로 선분 AB·CD. ∠ABD=75°(B), x°(D, ∠CDT), y°(T, ∠CTP)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 내접하는 두 원+공통 접선+삼각형 도형",
    note="∠CTP=∠ATP=∠ABT=75°, x=∠CDT=∠CTP=75° → x+y=150° = 빠른정답 ✓.")

# ---------------- p93
add(id="b097107b", qtype="short",
    question=("다음 그림과 같이 두 원이 점 A에서 접하고 있다. 작은 원 위의 점 D에서 접하는 직선이 큰 원과 만나는 점을 "
              "각각 B, C라 하면 [[seg(AB) = 8]] cm, [[seg(BC) = 7]] cm, [[seg(AC) = 6]] cm일 때, [[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="3 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 안에 작은 원이 점 A(우상)에서 내접. 큰 원 위 B(좌)·C(아래), 작은 원 위 D(BC 위, 접점). 삼각형 ABC와 선분 AD. AB=8cm, BC=7cm, AC=6cm(호 모양 점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 내접하는 두 원+삼각형 도형",
    note="AD가 ∠BAC의 이등분선 → BD:DC=8:6 → CD=3cm. 빠른정답 22와 불일치(정렬 어긋남).")

# ---------------- p97
add(id="fef007fd", qtype="choice",
    question="아래 그림에서 점 P는 두 원의 접점이고 직선 TT′은 점 P를 지나는 접선이다. 다음 중 옳지 않은 것은?",
    choices=["[[angle(PDB) = angle(PCA)]]", "[[angle(BPT) = angle(ACP)]]", "[[angle(BPT) = angle(BDP)]]",
             "[[par(seg(AC), seg(BD))]]", "[[ratio(seg(BD), seg(AC)) = ratio(seg(AB), seg(BP))]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 안에 작은 원이 점 P(우)에서 내접, P를 지나는 접선 TT′(T 위, T′ 아래). 큰 원 위 A(좌상)·C(좌하), 작은 원 위 B(선분 AP 위)·D(선분 CP 위). 선분 AC·BD·AP·CP"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="프라임 점 라벨(T′) / 도형 표현 불가: 내접하는 두 원+접선 도형",
    note="△PBD∽△PAC → BD:AC=PB:PA이므로 ⑤가 틀림 = 빠른정답 ✓.")

# ---------------- p98
add(id="31e9960c", qtype="short",
    question=("다음 그림에서 직선 TT′은 두 원의 공통인 접선이다. [[angle(CAP) = deg(40)]], [[angle(BDC) = deg(100)]]일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(60)",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 안에 작은 원이 점 P(우)에서 내접, 세로 접선 TT′(T 위, T′ 아래). 큰 원 위 A(좌)·C(아래), 작은 원 위 B(선분 AP 위)·D(선분 CP 위). 선분 AC·BD. ∠CAP=40°(A), ∠BDC=100°(D), x(P, ∠BPD)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="프라임 점 라벨(T′) / 도형 표현 불가: 내접하는 두 원+공통 접선 도형",
    note="원문 'TT′' 위에 직선 기호(양쪽 화살표). ∠BDP=80°=∠BPT=∠ACP, △ACP에서 x=∠APC=60°. 빠른정답 2와 불일치(정렬 어긋남).")

# ---------------- p99 (한 쪽에 별개 문항 2개, id 1개 → 위 문항 전사)
add(id="1c5f71e1", qtype="short",
    question=("다음 그림과 같이 두 원이 점 A에서 접하고 있다. 작은 원 위의 점 D에서 접하는 직선이 큰 원과 만나는 점을 각각 "
              "B, C라 하면 [[seg(AB) = 6]] cm, [[seg(BC) = 5]] cm, [[seg(AC) = 4]] cm일 때, [[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="2 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 안에 작은 원이 점 A(우상)에서 내접. 큰 원 위 B(좌)·C(아래), 작은 원 위 D(BC 위, 접점). 삼각형 ABC와 선분 AD. AB=6cm, BC=5cm, AC=4cm(호 모양 점선 치수)"}}],
    difficulty_est=3, confidence=0.75,
    needs_review=("한 쪽에 별개 문항 2개, id 1개 — 위 문항만 전사(아래 문항: 반지름 5·10인 두 원 O·O′이 점 P에서 접하고 원 O′의 두 현 PA·PB가 원 O와 만나는 점 C·D, "
                  "□ACDB의 넓이는 △PDC의 넓이의 몇 배인가, 선택형 ①2배 ②5/2배 ③3배 ④7/2배 ⑤4배, 답 ③) / 도형 표현 불가: 내접하는 두 원+삼각형 도형"),
    note="위 문항: BD:DC=6:4 → CD=2cm. 빠른정답 3은 아래 문항의 답 ③과 일치.")

# ======================= 원주각 =======================
# ---------------- p5
add(id="e1f9a600", qtype="short",
    question="다음 그림에서 [[tri(ABC)]]가 원에 내접하는 삼각형이고 [[angle(ACB) = deg(40)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(50)",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O)에 내접하는 △ABC(A 좌하, B 우하, C 위). 반지름 OA·OB. ∠ACB=40°(C), x(A, ∠OAB)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접삼각형+중심 도형",
    note="∠AOB=80°, OA=OB → x=50° (빠른정답 없음, 풀이 답).")

# ---------------- p12
add(id="46e5d0bf", qtype="choice",
    question="다음 그림에서 [[angle(x)]]의 크기는?",
    choices=["[[deg(55)]]", "[[deg(60)]]", "[[deg(65)]]", "[[deg(70)]]", "[[deg(75)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O) 위 P(위)·A(좌)·C(우)·B(아래). 선분 PA·PC·OA·OC·BA·BC. x(P, ∠APC), 110°(B, ∠ABC)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+사각형+중심 도형",
    note="∠ABC=110° → ∠APC=180°−110°=70° → ④ = 빠른정답 ✓.")

# ---------------- p13
add(id="96e2d4e0", qtype="choice",
    question="다음 그림과 같은 원 O에서 [[angle(BCD) = deg(132)]]일 때, [[angle(x) + angle(y)]]의 크기는?",
    choices=["[[deg(290)]]", "[[deg(302)]]", "[[deg(308)]]", "[[deg(310)]]", "[[deg(312)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(위)·B(좌하)·C(아래)·D(우하). 선분 AB·AD·OB·OD·CB·CD. x(A, ∠BAD), y(O, 위쪽으로 표시한 우각 ∠BOD), 132°(C, ∠BCD)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+중심각(우각)+원주각 도형",
    note="x=180°−132°=48°, y(우각)=2×132°=264° → 312° → ⑤ (빠른정답 없음, 풀이 답).")

# ---------------- p16
add(id="74365316", qtype="short",
    question=("다음 그림에서 [[seg(PA) = seg(PB)]]이고, [[angle(PAB) = deg(25)]]일 때, [[angle(AOB)]]의 크기를 구하시오.\n"
              "(단, [[angle(AOB)]]는 [[arc(APB)]]의 중심각이다.)"),
    choices=None, derived_answer="deg(100)",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O) 위 A(좌상)·P(좌)·B(좌하). 선분 PA·PB(같음 표시)·AB·OA·OB. ∠PAB=25°(A)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+이등변삼각형+중심각 도형",
    note="∠PAB=25° → 호 PB=50°=호 PA → 호 APB=100° → ∠AOB=100°. 빠른정답 5와 불일치(정렬 어긋남).")

# ---------------- p20
add(id="d4d64abb", qtype="short",
    question="다음 그림에서 [[angle(APB) = deg(105)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(150)",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O) 위 A(좌)·B(우)·P(아래). 선분 OA·OB·PA·PB. 105°(P, ∠APB), x(O, 아래쪽 ∠AOB)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+중심각+원주각 도형",
    note="∠APB=105° → 우각 210° → x=360°−210°=150° (빠른정답 없음, 풀이 답).")

# ---------------- p24
add(id="597db725", qtype="short",
    question="다음 그림에서 점 A, B는 원 O에 접하는 접점이고 [[angle(ACB) = deg(60)]]일 때, [[angle(APB)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 밖의 점 P(우상)에서 그은 두 접선의 접점 A(위)·B(우하). 원 위 C(좌하). 선분 CA·CB. ∠ACB=60°(C), x(P, ∠APB)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="∠AOB=120° → ∠APB=60°. 빠른정답 71과 불일치(정렬 어긋남).")

# ---------------- p26
add(id="e07f4711", qtype="choice",
    question="다음 그림에서 [[seg(PA)]], [[seg(PB)]]는 원 O의 접선이고 [[angle(APB) = deg(48)]]일 때, [[angle(ACB)]]의 크기는?",
    choices=["[[deg(112)]]", "[[deg(113)]]", "[[deg(114)]]", "[[deg(115)]]", "[[deg(116)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(우) 밖의 점 P(좌)에서 그은 두 접선의 접점 A(위)·B(아래). P에 가까운 열호 AB 위의 점 C. 선분 CA·CB. ∠APB=48°(P)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="∠AOB=132°, C는 열호 위 → ∠ACB=(360°−132°)/2=114° → ③. 빠른정답 2와 불일치(정렬 어긋남).")

# ---------------- p27
add(id="90c124c7", qtype="choice",
    question="다음 그림에서 [[seg(PA)]], [[seg(PB)]]는 원 O의 접선이다. [[angle(APB) = deg(70)]]일 때, [[angle(ACB)]]의 크기는?",
    choices=["[[deg(45)]]", "[[deg(50)]]", "[[deg(55)]]", "[[deg(60)]]", "[[deg(65)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(우) 밖의 점 P(좌)에서 그은 두 접선의 접점 A(위)·B(아래). 원 위 C(우, 우호 위). 선분 CA·CB. ∠APB=70°(P)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="∠AOB=110° → ∠ACB=55° → ③ = 빠른정답 ✓.")

# ---------------- p28
add(id="113cbe1c", qtype="short",
    question="다음 그림에서 [[seg(PA)]], [[seg(PB)]]가 원 O의 접선이고 [[angle(ACB) = deg(70)]]일 때, [[angle(APB)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(40)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(우) 밖의 점 P(좌하)에서 그은 두 접선의 접점 A(위)·B(아래). 원 위 C(우). 선분 CA·CB. ∠ACB=70°(C), P에 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="∠AOB=140° → ∠APB=40°. 빠른정답 3과 불일치(정렬 어긋남).")

# ---------------- p29
add(id="bcec274a", qtype="short",
    question=("다음 그림과 같이 점 P에서 원 O에 그은 두 접선의 접점을 각각 A, B라 하고, [[arc(AB)]] 위의 한 점 Q에 대해서 "
              "[[angle(AQB) = deg(118)]]일 때, [[angle(APB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(56)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(우) 밖의 점 P(좌)에서 그은 두 접선의 접점 A(위)·B(아래). P에 가까운 열호 AB 위의 점 Q. 선분 QA·QB. ∠AQB=118°(Q), P에 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 접선 도형",
    note="∠AOB=360°−236°=124° → ∠APB=56°. 빠른정답 3과 불일치(정렬 어긋남).")

# ---------------- p34
add(id="ccbb37bc", qtype="choice",
    question="다음 그림과 같은 원 O에서 [[angle(APB) = deg(40)]], [[angle(BQC) = deg(23)]]일 때, [[angle(x)]]의 크기는?",
    choices=["[[deg(110)]]", "[[deg(114)]]", "[[deg(120)]]", "[[deg(126)]]", "[[deg(132)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 P(좌상)·Q(우상)·A(좌)·C(우)·B(아래). 선분 PA·PB·QB·QC·OA·OC. ∠APB=40°(P), ∠BQC=23°(Q), x(O, 아래쪽 ∠AOC)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+원주각 2개+중심각 도형",
    note="호 AB=80°, 호 BC=46° → x=∠AOC=126° → ④. 빠른정답 3과 불일치(정렬 어긋남).")

# ---------------- p38
add(id="f54c2d2e", qtype="choice",
    question="다음 그림과 같은 원 O에서 [[angle(AOC) = deg(120)]], [[angle(APB) = deg(26)]]일 때, [[angle(BQC)]]의 크기는?",
    choices=["[[deg(30)]]", "[[deg(32)]]", "[[deg(34)]]", "[[deg(36)]]", "[[deg(38)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 B(위)·A(좌상)·C(우상)·P(좌하)·Q(우하). 선분 OA·OC·PA·PB·QB·QC. ∠AOC=120°(O, 위쪽), ∠APB=26°(P), Q에 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+중심각+원주각 2개 도형",
    note="호 AB=52°, 호 BC=120°−52°=68° → ∠BQC=34° → ③. 빠른정답 4와 불일치(정렬 어긋남).")

# ---------------- p40
add(id="ac60cf06", qtype="choice",
    question=("다음 그림에서 점 I는 [[tri(ABC)]]의 내심이고 점 D는 [[seg(AI)]]의 연장선과 [[tri(ABC)]]의 외접원의 교점이다. "
              "[[seg(AI) = 6]] cm, [[seg(DI) = 9]] cm일 때, [[seg(CD)]]의 길이는?"),
    choices=["[[8]] cm", "[[9]] cm", "[[10]] cm", "[[11]] cm", "[[12]] cm"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 △ABC(A 위, B 좌, C 우). 내심 I, AI 연장선이 원과 만나는 점 D(아래). 선분 BD·CD. AI=6cm, DI=9cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+내심+삼각형 도형",
    note="DB=DC=DI=9cm → ② (빠른정답 없음, 풀이 답).")

# ---------------- p41
add(id="1a36d1ec", qtype="short",
    question="다음 그림에서 [[seg(AB)]]는 원 O의 지름이다. [[angle(BAC) = deg(51)]]일 때, [[angle(ADC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(39)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(좌하)·B(우상)·D(위)·C(우하). 지름 AB, 선분 AC·AD·DC. ∠BAC=51°(A)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+원주각 도형",
    note="∠ACB=90° → ∠ABC=39°=∠ADC (빠른정답 없음, 풀이 답).")

# ---------------- p44
add(id="ca42226c", qtype="choice",
    question="다음 그림과 같은 원 O에서 [[angle(ADC) = deg(42)]]일 때, [[angle(ABD)]]의 크기는?",
    choices=["[[deg(42)]]", "[[deg(44)]]", "[[deg(46)]]", "[[deg(48)]]", "[[deg(50)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(좌상)·C(우상)·D(좌하)·B(우하). 지름 AB·CD가 O에서 교차, 선분 AD·BC·DB. ∠ADC=42°(D), B에 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+두 지름+원주각 도형",
    note="∠ADB=90° → ∠BDC=48°, 호 AD=호 BC → ∠ABD=48° → ④ (빠른정답 없음, 풀이 답).")

# ---------------- p46
add(id="ea769f56", qtype="short",
    question="다음 그림에서 [[seg(BD)]]는 원 O의 지름이고, [[angle(BAC) = deg(50)]]일 때, [[angle(DBC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(40)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(좌상)·D(우상)·B(좌하)·C(우하). 지름 BD, 선분 AB·AC·BC·CD. ∠BAC=50°(A), B에 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+원주각 도형",
    note="∠BDC=50°, ∠BCD=90° → ∠DBC=40°. 빠른정답 5와 불일치(정렬 어긋남).")

# ---------------- p47
add(id="ff2fcea3", qtype="short",
    question="다음 그림에서 [[seg(AB)]]는 원 O의 지름이고 [[angle(BAC) = deg(34)]]일 때, [[angle(ADC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(56)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(좌)·B(우)·D(위)·C(아래). 지름 AB, 선분 AC·AD·DC. ∠BAC=34°(A), D에 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+원주각 도형",
    note="∠ACB=90° → ∠ABC=56°=∠ADC (빠른정답 없음, 풀이 답).")

# ---------------- p50
add(id="dc6a3a40", qtype="short",
    question="다음 그림에서 [[seg(AC)]]는 원 O의 지름이고 [[angle(ACD) = deg(38)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(52)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(좌상)·D(우상)·B(좌하)·C(우하). 지름 AC, 선분 AB·BC·BD·DC. ∠ACD=38°(C), x(B, ∠DBC)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+원주각 도형",
    note="∠ABD=∠ACD=38°, ∠ABC=90° → x=52° (빠른정답 없음, 풀이 답).")

# ---------------- p51
add(id="a02d26c5", qtype="short",
    question=("다음 그림과 같이 [[seg(BC) = 5]] cm인 예각삼각형 ABC에 외접하는 원 O의 반지름의 길이가 4 cm일 때, "
              "[[sin(A)]]의 값을 구하시오."),
    choices=None, derived_answer="frac(5,8)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 △ABC(A 위, B 좌하, C 우하). OB=4cm, BC=5cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+삼각형 도형",
    note="sin A = BC/2R = 5/8. 빠른정답 'ratio(5,8)'과 값은 같음(표기 차이).")

# ---------------- p53
add(id="7f6f8dd8", qtype="short",
    question=("다음 그림과 같이 [[seg(AB)]]를 지름으로 하는 반원 O 위의 점 C에서 [[seg(AB)]]에 내린 수선의 발을 D라 하자. "
              "[[seg(AB) = 13]], [[seg(BC) = 5]]일 때, [[sin(x) × cos(x)]]의 값을 구하시오."),
    choices=None, derived_answer="frac(60,169)",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O) 위 A(좌)·B(우)·C(우상). 지름 AB, 선분 AC·BC, C에서 AB에 내린 수선 CD(직각 표시). x(C, ∠ACD), BC=5, AB=13(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+수선 도형",
    note="x=∠ABC, AC=12 → sin x cos x = (12/13)(5/13) = 60/169. 빠른정답 'ratio(60,160)'과 불일치(오타로 보임).")

# ---------------- p54
add(id="b56208e6", qtype="choice",
    question=("다음 그림과 같이 반지름의 길이가 10 cm인 원 O에 내접하는 삼각형 ABC에서 [[seg(BC) = 12]] cm일 때, "
              "[[sin(A) + cos(A) + tan(A)]]의 값은?"),
    choices=["[[frac(21,20)]]", "[[frac(22,15)]]", "[[frac(43,20)]]", "[[frac(47,20)]]", "[[frac(41,15)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 △ABC(A 위, B 좌하, C 우하). OB=10cm, BC=12cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+삼각형 도형",
    note="sin A=3/5, cos A=4/5, tan A=3/4 → 43/20 → ③ = 빠른정답 ✓.")

# ---------------- p55
add(id="3b7e3758", qtype="choice",
    question=("다음 그림과 같이 반지름의 길이가 5인 원 O에 내접하는 [[tri(ABC)]]에 대하여 [[seg(BC) = 8]]일 때, "
              "[[sin(A) cos(A) tan(A)]]의 값은?"),
    choices=["[[frac(9,25)]]", "[[frac(16,25)]]", "[[1]]", "[[frac(25,16)]]", "[[frac(25,9)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 △ABC(A 좌상, B 좌하, C 우하). OB=5, BC=8(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+삼각형 도형",
    note="sin A=4/5 → sin²A=16/25 → ② = 빠른정답 ✓.")

# ---------------- p56
add(id="4dde99f3", qtype="choice",
    question="다음 그림과 같이 [[seg(BC) = 5]]인 예각삼각형 ABC에 외접하는 원 O의 반지름의 길이가 3일 때, [[sin(A)]]의 값은?",
    choices=["[[frac(1,2)]]", "[[frac(3,5)]]", "[[frac(sqrt(11),6)]]", "[[frac(sqrt(11),5)]]", "[[frac(5,6)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 △ABC(A 위, B 좌하, C 우하). OB=3, BC=5(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+삼각형 도형",
    note="sin A=5/6 → ⑤ = 빠른정답 ✓.")

# ---------------- p57
add(id="7fbdd673", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB)]]를 지름으로 하는 반원 O 위의 점 C에서 [[seg(AB)]]에 내린 수선의 발을 D라 하자. "
              "[[angle(ACD) = theta]], [[seg(AB) = 25]], [[seg(BC) = 15]]일 때, [[sin(theta) × cos(theta)]]의 값은?"),
    choices=["[[frac(12,25)]]", "[[frac(13,25)]]", "[[frac(14,25)]]", "[[frac(3,5)]]", "[[frac(16,25)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "반원(중심 O, 지름 AB: A 좌, B 우) 위의 점 C(우상). 선분 AC·BC, 수선 CD(직각 표시). θ(C, ∠ACD), BC=15, AB=25(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 반원+수선 도형",
    note="θ=∠ABC, AC=20 → (4/5)(3/5)=12/25 → ① = 빠른정답 ✓.")

# ---------------- p58
add(id="715c53c7", qtype="short",
    question=("다음 그림과 같이 반지름의 길이가 [[frac(13,2)]] cm인 원에 내접하는 삼각형 ABC에서 [[cos(A) × tan(A)]]의 값이 "
              "[[frac(a,b)]]이다. [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 서로소이다.)"),
    choices=None, derived_answer="18",
    figure=[{"fn": "unsupported", "args": {"raw": "분홍색 원(중심 O)에 내접하는 △ABC(B 좌상, C 좌하, A 우). OB=13/2 cm, BC=5cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+삼각형 도형",
    note="cos A·tan A=sin A=5/13 → a+b=18 = 빠른정답 ✓.")

# ---------------- p59
add(id="0d45af7a", qtype="short",
    question=("다음 그림과 같이 반지름의 길이가 8.5인 원 O에 내접하는 [[tri(ABC)]]에서 [[seg(BC) = 8]]일 때, "
              "[[cos(A) × frac(1, tan(A)) × sin(A)]]의 값을 구하시오."),
    choices=None, derived_answer="frac(225,289)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 △ABC(A 위, B 좌하, C 우하). OB=8.5, BC=8(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+삼각형 도형",
    note="sin A=8/17 → cos²A=225/289. 빠른정답 'ratio(225,289)'와 값은 같음(표기 차이).")

# ---------------- p63
add(id="11b6fd18", qtype="short",
    question="다음 그림에서 [[tri(OBC)]]의 넓이를 구하시오.",
    choices=None, derived_answer="9 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O)에 내접하는 △ABC(A 위, B 좌하, C 우하). ∠BAC=75°(A), OB=6cm(점선 치수), △OBC 색칠(보라)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+중심각 삼각형 도형",
    note="∠BOC=150° → 넓이 ½·6·6·sin150°=9cm² (빠른정답 없음, 풀이 답).")

# ---------------- p64
add(id="8cb018c6", qtype="choice",
    question=("다음 그림에서 [[seg(AB)]]는 원 O의 지름이고 [[seg(AC) = 12]] cm, [[tan(B) = frac(12,5)]]일 때, "
              "원 O의 반지름의 길이는?"),
    choices=["[[6]] cm", "[[6.5]] cm", "[[7]] cm", "[[7.5]] cm", "[[8]] cm"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(좌)·B(우)·C(우상). 지름 AB, 선분 AC·BC. AC=12cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+직각삼각형 도형",
    note="∠C=90°, BC=5 → AB=13 → r=6.5 → ②. 빠른정답 4와 불일치(정렬 어긋남).")

# ---------------- p65
add(id="e292dad3", qtype="choice",
    question="다음 그림과 같은 [[angle(A) = deg(60)]], [[seg(BC) = 12]] cm인 삼각형 ABC에 대하여 외접원 O의 지름의 길이는?",
    choices=["[[2 sqrt(3)]] cm", "[[3 sqrt(3)]] cm", "[[4 sqrt(3)]] cm", "[[6 sqrt(3)]] cm", "[[8 sqrt(3)]] cm"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O에 내접하는 △ABC(A 위, B 좌하, C 우하). ∠A=60°(A), BC=12cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 외접원+삼각형 도형",
    note="2R=12/sin60°=8√3 → ⑤ = 빠른정답 ✓.")

# ---------------- p71
add(id="fb53e4e9", qtype="short",
    question="다음 그림에서 [[arc(AB) = arc(CD)]]이고 [[angle(ACB) = deg(30)]]일 때, [[angle(DPC)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 위 A(좌)·D(우상)·B(좌하)·C(우하). 현 AC와 BD가 P에서 교차, 선분 BC. 호 AB·호 CD에 같음 표시(=). ∠ACB=30°(C), P에 각 표시(∠DPC)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+교차하는 두 현 도형",
    note="∠DBC=∠ACB=30° → ∠DPC=30°+30°=60° (빠른정답 없음, 풀이 답).")

# ---------------- p72
add(id="e5b58a93", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB)]]를 지름으로 하는 반원 O에서 [[arc(AD) = arc(CD)]]이고 점 P는 [[seg(AC)]]와 [[seg(BD)]]의 교점이다. "
              "[[angle(DBA) = deg(38)]]일 때, [[angle(CPB)]]의 크기는?"),
    choices=["[[deg(46)]]", "[[deg(48)]]", "[[deg(50)]]", "[[deg(51)]]", "[[deg(52)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "반원(중심 O, 지름 AB: A 좌, B 우) 위 D(좌상)·C(우상). 현 AC·BD가 P에서 교차. 호 AD·호 CD에 같음 표시(=). ∠DBA=38°(B), P에 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 반원+교차하는 두 현 도형",
    note="∠CAD=∠DBA=38°, ∠ADB=90° → ∠APD=52°=∠CPB → ⑤ = 빠른정답 ✓.")

# ---------------- p73
add(id="45528a3b", qtype="choice",
    question=("다음 그림과 같이 원에 내접하는 사각형 ABCD의 두 대각선의 교점을 P라 하자. [[arc(AB) = arc(AD)]]이고 [[seg(AB) = 2]], "
              "[[seg(BD) = 3]], [[seg(BC) = 2 seg(CD)]]일 때, [[seg(PC)]]의 길이는?"),
    choices=["[[1]]", "[[sqrt(2)]]", "[[sqrt(3)]]", "[[2]]", "[[sqrt(5)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 사각형 ABCD(A 좌상, D 우상, C 우, B 좌하). 대각선 AC·BD가 P에서 교차. 호 AB·호 AD에 같음 표시(=)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접사각형+대각선 도형",
    note="CP가 ∠BCD 이등분 → BP=2, PD=1; AB=AD=2, BD=3 → PA=√2 → PC=PB·PD/PA=√2 → ② = 빠른정답 ✓.")

# ---------------- p78
add(id="da32efa8", qtype="short",
    question="다음 그림에서 [[angle(BDC) = x]], [[arc(AB) = arc(BC)]]라 할 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(50)",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O) 위 A(좌)·B(아래)·C(우)·D(우상). 반지름 OA·OB, 선분 BD·DC. ∠AOB=100°(O), x(D, ∠BDC). 호 AB·호 BC에 같음 표시(=)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+중심각+원주각 도형",
    note="호 BC=호 AB=100° → x=50°. 빠른정답 60과 불일치(정렬 어긋남).")

# ---------------- p79
add(id="48132d15", qtype="short",
    question="다음 그림에서 [[arc(AB) = arc(AD) = arc(CD)]], [[angle(BPD) = deg(30)]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="7.5",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 밖의 점 P(좌)에서 두 직선: P–B–A(위쪽, A 우상), P–C–D(아래쪽, D 우하). 선분 BD. 호 AB(좌상)·호 AD(우)·호 CD(아래)에 같음 표시(=). ∠BPD=30°(P), ∠BDC=3x°(D)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+외부점에서 그은 두 할선 도형",
    note="세 호 각 105°, 호 BC=45° → ∠ABD=52.5°=30°+3x° → x=7.5. 빠른정답 7과 불일치(7.5 절삭 가능성).")

# ---------------- p82
add(id="a55df89f", qtype="choice",
    question="다음 그림에서 [[arc(BC) = 5]] cm이고, [[angle(ACD) = deg(20)]], [[angle(BPC) = deg(65)]]일 때, [[arc(AD)]]의 길이는?",
    choices=["[[10]] cm", "[[12]] cm", "[[frac(14,3)]] cm", "[[frac(16,5)]] cm", "[[frac(20,9)]] cm"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 위 A(위)·D(우상)·B(우하)·C(좌하). 현 AB와 CD가 P에서 교차, 선분 AC. ∠ACD=20°(C), ∠BPC=65°(P), 호 BC=5cm"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+교차하는 두 현 도형",
    note="∠BAC=65°−20°=45° → 호 AD=5×20/45=20/9 → ⑤. 빠른정답 7.5와 불일치(정렬 어긋남).")

# ---------------- p83
add(id="234e509a", qtype="choice",
    question=("다음 그림에서 점 P는 [[seg(AD)]], [[seg(BC)]]의 연장선의 교점이고 [[angle(ACB) = deg(30)]], [[arc(AB) = 5]] cm, "
              "[[arc(CD) = 10]] cm일 때, [[angle(x)]]의 크기는?"),
    choices=["[[deg(24)]]", "[[deg(26)]]", "[[deg(28)]]", "[[deg(30)]]", "[[deg(32)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원(우) 밖의 점 P(좌)에서 두 직선: P–A–D(위), P–B–C(아래). 선분 AC. ∠ACB=30°(C), x(P, ∠APC)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+외부점에서 그은 두 할선 도형",
    note="∠CAD=60° → x=60°−30°=30° → ④ (빠른정답 없음, 풀이 답).")

# ---------------- p84
add(id="c9dc7e1c", qtype="short",
    question="다음 그림에서 [[arc(PB) = frac(1,3) arc(PA)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(15)",
    figure=[{"fn": "unsupported", "args": {"raw": "원(중심 O) 위 A(좌)·B(우)·P(위). 반지름 OA·OB, 선분 PA·PB·AB. x(A, ∠PAB), 우각 ∠AOB=240°(O, 아래쪽)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+중심각(우각)+원주각 도형",
    note="호 APB=120° → 호 PB=30° → x=15°. 빠른정답 60과 불일치(정렬 어긋남).")

# ---------------- p87
add(id="d5ffca84", qtype="choice",
    question=("다음 그림에서 [[seg(AC)]]는 원 O의 지름이고 [[angle(BAC) = deg(18)]]이다. [[arc(AD) = 12]] cm, [[arc(BC) = 3]] cm일 때, "
              "[[angle(x)]]의 크기는?"),
    choices=["[[deg(14)]]", "[[deg(15)]]", "[[deg(16)]]", "[[deg(17)]]", "[[deg(18)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(위)·C(아래)·B(좌하)·D(우하). 지름 AC, 선분 AB·AD. ∠BAC=18°(A), x(A, ∠CAD), 호 AD=12cm(우측 화살표), 호 BC=3cm(아래 화살표)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+지름+호 길이 도형",
    note="∠ACD=18°×4=72°, ∠ADC=90° → x=18° → ⑤ = 빠른정답 ✓.")

# ---------------- p88
add(id="da9990d0", qtype="short",
    question=("다음 그림과 같이 원 O의 두 현 AB, CD의 연장선이 만나는 점을 P, 두 현 AD, BC가 만나는 점을 Q라 하자. "
              "[[ratio(arc(AC), arc(BD)) = ratio(3,5)]]이고 [[angle(BPD) = deg(24)]]일 때, [[angle(BQD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(96)",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(우) 밖의 점 P(좌)에서 두 직선: P–A–B(위), P–C–D(아래). 현 AD·BC가 Q에서 교차. ∠BPD=24°(P)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+할선 2개+교차하는 현 도형",
    note="호 AC·BD의 원주각 3k·5k, 5k−3k=24° → k=12° → ∠BQD=8k=96° (빠른정답 없음, 풀이 답).")

# ---------------- p92
add(id="0fd6acd8", qtype="choice",
    question=("다음 그림의 원 O에서 점 P는 두 현 AB, CD의 교점이고 [[angle(APD) = deg(45)]], [[arc(AD) + arc(BC) = 3 pi]]일 때, "
              "원 O의 둘레의 길이는?"),
    choices=["[[10 pi]]", "[[frac(21,2) pi]]", "[[11 pi]]", "[[frac(23,2) pi]]", "[[12 pi]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위 A(좌)·B(우)·C(우상)·D(좌하). 현 AB·CD가 P에서 교차. ∠APD=45°(P)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+교차하는 두 현 도형",
    note="호 AD+호 BC=90°에 해당 → 둘레=3π×4=12π → ⑤. 빠른정답 '32 cm'와 불일치(정렬 어긋남).")

# ---------------- p93
add(id="6fc8a406", qtype="choice",
    question=("다음 그림과 같이 두 현 AC, BD의 교점을 P라 하자. [[arc(AB)]] : [[arc(BC)]] : [[arc(CD)]] : [[arc(DA)]] = 5 : 2 : 4 : 7일 때, "
              "[[angle(x)]]의 크기는?"),
    choices=["[[deg(90)]]", "[[deg(91)]]", "[[deg(92)]]", "[[deg(93)]]", "[[deg(94)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "원 위 D(위)·C(우)·B(우하)·A(좌하). 현 AC·BD가 P에서 교차. x(P, ∠DPC)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+교차하는 두 현 도형",
    note="ratio는 인자 3개까지라 4항 비는 텍스트 콜론으로 표기. 한 눈금 20° → x=½(호 CD+호 AB)=½(80°+100°)=90° → ①. 빠른정답 20과 불일치(정렬 어긋남).")

# ---------------- p94
add(id="8372a738", qtype="short",
    question=("다음 그림에서 [[ratio(arc(AB), arc(BC), arc(CA)) = ratio(4,3,2)]]이다. [[angle(BAC) = deg(a)]], [[angle(ABC) = deg(b)]], "
              "[[angle(BCA) = deg(c)]]라 할 때, [[a - b + c]]의 값을 구하시오."),
    choices=None, derived_answer="100",
    figure=[{"fn": "unsupported", "args": {"raw": "원에 내접하는 △ABC(A 우상, B 좌하, C 우하). a°(A), b°(B), c°(C)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접삼각형 도형",
    note="a=60, b=40, c=80 → 100 (빠른정답 없음, 풀이 답).")

# ---------------- p96
add(id="b02e8608", qtype="choice",
    question=("다음 그림과 같이 지름의 길이가 2인 원 O 위에 16개의 점이 같은 간격으로 놓여 있고, 이 점을 각각 [[sub(P,0)]], [[sub(P,1)]], "
              "[[sub(P,2)]], ⋯, [[sub(P,15)]]라 하자. 선분 [[sub(P,0)]][[sub(P,k)]] ([[k]] = 1, 2, 3, ⋯, 8)의 길이를 [[sub(l,k)]]라 할 때, "
              "[[pow(sub(l,1),2) + pow(sub(l,2),2) + pow(sub(l,3),2)]] + ⋯ + [[pow(sub(l,8),2)]]의 값은?"),
    choices=["[[12]]", "[[14]]", "[[16]]", "[[18]]", "[[20]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O 위에 같은 간격의 점 16개. P₀(우), P₁(우상), P_k(위), P₈(좌). 지름 P₀P₈=2(점선 치수), 선분 P₀P_k=l_k(점선 표시)"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="첨자 점 라벨(선분 P₀Pₖ의 윗줄 표기를 seg로 표현 불가, 텍스트 '선분'으로 대체) / 도형 표현 불가: 원 위 16등분점 도형",
    note="l_k²=4sin²(kπ/16), 합=16−2Σcos(kπ/8)=18 → ④. 빠른정답 1과 불일치(정렬 어긋남).")

# ---------------- p99 (한 쪽에 별개 문항 2개, id 1개 → 위 문항 전사)
add(id="6805bd8a", qtype="short",
    question=("다음 그림에서 점 P는 [[seg(AC)]]와 [[seg(BD)]]의 교점이다. [[angle(ABD) = deg(40)]], [[angle(BPC) = deg(70)]]이고 "
              "[[arc(BC) = 5]] cm일 때, 원의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="30 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "원 위 A(좌상)·D(우상)·B(좌하)·C(우하). 현 AC·BD가 P에서 교차, 선분 AB. ∠ABD=40°(B), ∠BPC=70°(P), 호 BC=5cm"}}],
    difficulty_est=2, confidence=0.75,
    needs_review=("한 쪽에 별개 문항 2개, id 1개 — 위 문항만 전사(아래 문항: [2009년 3월 고1 20번] 반지름 9cm인 원 O에서 호 AB=4π cm·호 CD=6π cm, "
                  "선분 AB와 CD의 연장선이 이루는 예각 30°일 때 호 AC의 길이, 선택형 ①4π ②17/4π ③9/2π ④5π ⑤11/2π cm, 답 ⑤) / 도형 표현 불가: 원+교차하는 두 현 도형"),
    note="위 문항: ∠BAC=70°−40°=30° → 호 BC는 원주의 1/6 → 30cm. 빠른정답 4는 두 문항 어느 답과도 불일치.")

# ======================= 삼각비의 활용(1); 길이 =======================
# ---------------- p1
add(id="bdb37ac3", qtype="short",
    question=("다음 그림의 직각삼각형 ABC에서 [[x]]의 값을 구하시오.\n"
              "(단, [[sin(deg(34)) = 0.56]], [[cos(deg(34)) = 0.83]], [[tan(deg(34)) = 0.67]]로 계산한다.)"),
    choices=None, derived_answer="25",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: A 좌상, C 우상(직각 표시), B 우하. ∠A=34°(A), BC=14, AB=x(점선 치수)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="sin34°=14/x → x=14/0.56=25 = 빠른정답 ✓.")

# ---------------- p3
add(id="a172b16f", qtype="choice",
    question=("다음 그림과 같은 직각삼각형 ABC에서 [[angle(B) = deg(51)]], [[seg(AB) = 100]]일 때, [[tri(ABC)]]의 둘레의 길이는?\n"
              "(단, [[sin(deg(51)) = 0.78]], [[cos(deg(51)) = 0.63]]으로 계산한다.)"),
    choices=["[[238]]", "[[239]]", "[[240]]", "[[241]]", "[[242]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: B 좌하, C 우하(직각 표시), A 우상. ∠B=51°(B), AB=100, AC=x, BC=y(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="x=78, y=63 → 둘레 241 → ④ (빠른정답 없음, 풀이 답).")

# ---------------- p5
add(id="99a89c44", qtype="short",
    question=("다음 그림과 같이 [[tri(ABC)]]에서 [[angle(A) = deg(45)]], [[angle(B) = deg(105)]], [[seg(AB) = 12 sqrt(2)]]이고 "
              "꼭짓점 B에서 [[seg(AC)]]에 수선 BH를 그었다. 이때 [[seg(BH)]]의 길이를 구하시오."),
    choices=None, derived_answer="12",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC: A 좌상, B 좌하, C 우하. B에서 AC에 내린 수선 BH(직각 표시). ∠A=45°(A), ∠B=105°(B), AB=12√2(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+수선 도형",
    note="BH=12√2·sin45°=12. 빠른정답 '9 cm'와 불일치(정렬 어긋남).")

# ---------------- p6
add(id="659a5d98", qtype="choice",
    question=("다음 그림에서 [[angle(BCA) = angle(AED) = deg(90)]], [[angle(AEC) = deg(60)]]이고 [[seg(AE) = seg(ED)]], "
              "[[seg(CE) = sqrt(3)]]일 때, [[seg(AB)]]의 길이는?"),
    choices=["[[2 sqrt(2) + 2 sqrt(3)]]", "[[2 sqrt(3) + 2 sqrt(6)]]", "[[2 sqrt(2) + 2 sqrt(6)]]",
             "[[3 sqrt(2) + 3 sqrt(3)]]", "[[3 sqrt(2) + 3 sqrt(6)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "가늘고 긴 직각삼각형 ABC: B 좌, C 우(직각), A 우상. AB 위의 점 D, BC 위의 점 E. 선분 AE·DE(같음 표시, E에서 직각 표시). ∠AEC=60°(E), CE=√3(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형+내부 직각이등변삼각형 도형",
    note="AC=3, ∠B=15° → AB=3/sin15°=3√6+3√2 → ⑤ (빠른정답 없음, 풀이 답).")

# ---------------- p7
add(id="344a87c1", qtype="choice",
    question=("다음 그림과 같이 삼각형 ABC에서 변 BC의 중점을 M이라 할 때, [[angle(BMA) = deg(45)]], [[angle(MAB) = deg(90)]]이다. "
              "[[cos(C)]]의 값은?"),
    choices=["[[frac(sqrt(10),10)]]", "[[frac(sqrt(10),5)]]", "[[frac(3 sqrt(10),10)]]", "[[frac(2 sqrt(10),5)]]", "[[frac(sqrt(10),2)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC: B 좌, C 우, A 위(좌측). BC의 중점 M(같음 표시), 선분 AM. ∠MAB=90°(A, 직각 표시), ∠BMA=45°(M), C에 각 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+중선 도형",
    note="AB=1로 두면 BM=MC=√2, AC=√5, A에서 BC에 내린 수선으로 cos C=3/√10=3√10/10 → ③ (빠른정답 없음, 풀이 답).")

# ---------------- p9
add(id="dfaa944e", qtype="short",
    question=("다음 그림과 같은 직각삼각형 ABC에서 [[sin(B) = frac(2,3)]]일 때, [[seg(AC)]]의 길이를 구하는 과정이다. "
              "□ 안에 알맞은 수를 구하시오.\n[[seg(AC) = seg(AB) × sin(B)]]이므로 [[seg(AC)]] = □이다."),
    choices=None, derived_answer="8",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: B 좌하, C 우하(직각 표시), A 우상. AB=12(점선 치수)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="AC=12×2/3=8 (빠른정답 없음, 풀이 답).")

# ---------------- p10
add(id="d290f85e", qtype="choice",
    question=("다음 그림과 같은 직각삼각형 ABC에서 [[angle(A) = deg(60)]], [[angle(CDE) = deg(30)]], [[seg(AD) = 18]], [[seg(DE) = 9]]일 때, "
              "[[seg(BE)]]의 길이는?"),
    choices=["[[frac(9 sqrt(3), 2) + frac(9,2)]]", "[[frac(9 sqrt(3), 2) + 9]]", "[[9 sqrt(3) + frac(9,2)]]", "[[9 sqrt(3) + 9]]", "[[9 sqrt(3) + 12]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: A 좌상, B 좌하(직각 표시), C 우하. AC 위의 점 D, BC 위의 점 E, 선분 DE. ∠A=60°(A), ∠CDE=30°(D), AD=18, DE=9(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형+내부 선분 도형",
    note="EC=DE=9, DC=9√3 → AC=18+9√3, BC=AC·sin60°=9√3+27/2 → BE=9√3+9/2 → ③ (빠른정답 없음, 풀이 답).")

# ---------------- p12
add(id="53241a8a", qtype="choice",
    question=("아래 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에 대하여 다음 (가), (나) 안에 알맞은 것을 차례로 쓴 것은?\n"
              "[[cos(A)]] = (가) ⇨ [[c]] = (나)"),
    choices=["[[frac(a,b)]], [[a cos(A)]]", "[[frac(a,b)]], [[b cos(A)]]", "[[frac(c,b)]], [[a cos(A)]]",
             "[[frac(c,b)]], [[b cos(A)]]", "[[frac(b,c)]], [[b cos(A)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: A 위, B 좌하(직각 표시), C 우하. AB=c, BC=a, CA=b(점선 치수)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="cos A=c/b → c=b cos A → ④ (빠른정답 없음, 풀이 답).")

# ---------------- p13
add(id="5d5fedc7", qtype="choice",
    question=("다음 그림과 같은 직각삼각형에서 [[x - y]]의 값은?\n"
              "(단, [[sin(deg(55)) = 0.82]], [[cos(deg(55)) = 0.57]]로 계산한다.)"),
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: B 좌, C 우, A 위(직각 표시). ∠C=55°(C), AB=x, AC=y, BC=8(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="x=8×0.82=6.56, y=8×0.57=4.56 → x−y=2 → ① (빠른정답 없음, 풀이 답).")

# ---------------- p14
add(id="61ac6e3f", qtype="short",
    question=("다음 그림과 같이 [[seg(BE) = 8]] cm, [[seg(EF) = 10]] cm이고 [[angle(ABC) = deg(45)]], [[angle(BAC) = deg(90)]]인 "
              "삼각기둥의 부피를 구하시오."),
    choices=None, derived_answer="200 cm³",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각기둥(윗면 △ABC: A 위 꼭짓점, B 좌, C 우; 아랫면 △DEF). ∠ABC=45°(B), BE=8cm, EF=10cm(점선 치수), 옆면 색칠(보라)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각기둥 입체 도형",
    note="밑면 직각이등변삼각형(빗변 10) 넓이 25 → 부피 200cm³ (빠른정답 없음, 풀이 답).")

# ---------------- p15
add(id="0ae07358", qtype="choice",
    question=("다음 그림과 같이 [[angle(BAC) = deg(90)]], [[angle(ACB) = deg(30)]], [[seg(BC) = 4]] cm인 삼각기둥의 부피가 18 cm³일 때, "
              "삼각기둥의 높이는?"),
    choices=["[[2 sqrt(6)]] cm", "[[5]] cm", "[[3 sqrt(3)]] cm", "[[4 sqrt(2)]] cm", "[[6]] cm"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각기둥(윗면 △ABC: A 위, B 좌, C 우; 아랫면 △DEF, D에 직각 표시). ∠ACB=30°(C), BC=4cm(점선 치수), 색칠(분홍)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각기둥 입체 도형",
    note="밑넓이 ½·2·2√3=2√3 → h=18/(2√3)=3√3 → ③ (빠른정답 없음, 풀이 답).")

# ---------------- p16
add(id="79c01a4d", qtype="choice",
    question=("다음 그림의 사각뿔은 밑면이 한 변의 길이가 12 cm인 정사각형이고 옆면이 모두 합동인 이등변삼각형이다. "
              "꼭짓점 O에서 밑면에 내린 수선의 발을 H라 할 때, [[angle(OAH) = deg(30)]]이다. 이 사각뿔의 부피는? "
              "(단, 수선의 발 H는 [[quad(ABCD)]]의 두 대각선의 교점이다.)"),
    choices=["[[96 sqrt(2)]] cm³", "[[96 sqrt(3)]] cm³", "[[96 sqrt(6)]] cm³", "[[288 sqrt(3)]] cm³", "[[288 sqrt(6)]] cm³"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각뿔 O-ABCD(A 좌, B 앞, C 우, D 뒤). 대각선 AC·BD 점선, 교점 H, 수선 OH(직각 표시). ∠OAH=30°(A), AB=12cm, BC=12cm(점선 치수), 색칠(보라)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정사각뿔 입체 도형",
    note="AH=6√2, OH=6√2·tan30°=2√6 → V=⅓·144·2√6=96√6 → ③ (빠른정답 없음, 풀이 답).")

# ---------------- p17
add(id="bb26a0e0", qtype="choice",
    question=("다음 그림의 사각뿔은 밑면이 한 변의 길이가 18 cm인 정사각형이고 옆면이 모두 합동인 이등변삼각형이다. "
              "꼭짓점 O에서 밑면에 내린 수선의 발을 H라 하고 [[angle(OAH) = deg(45)]]일 때, 이 사각뿔의 부피는?\n"
              "(단, 점 H는 [[quad(ABCD)]]의 두 대각선의 교점이다.)"),
    choices=["[[481 sqrt(2)]] cm³", "[[481 sqrt(3)]] cm³", "[[481 sqrt(6)]] cm³", "[[972 sqrt(2)]] cm³", "[[972 sqrt(3)]] cm³"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각뿔 O-ABCD(A 좌, B 앞, C 우, D 뒤). 대각선 AC·BD 점선, 교점 H, 수선 OH(직각 표시). ∠OAH=45°(A), AB=18cm, BC=18cm(점선 치수), 색칠(하늘색)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정사각뿔 입체 도형",
    note="AH=OH=9√2 → V=⅓·324·9√2=972√2 → ④ (빠른정답 없음, 풀이 답).")

# ---------------- p19
add(id="7ddff858", qtype="choice",
    question="다음 그림과 같은 직육면체에서 [[seg(HG) = seg(FG) = 5]] cm, [[angle(BHF) = deg(30)]]일 때, 이 직육면체의 부피는?",
    choices=["[[frac(25 sqrt(6), 3)]] cm³", "[[frac(125 sqrt(6), 3)]] cm³", "[[frac(125 sqrt(6), 2)]] cm³", "[[68 sqrt(6)]] cm³", "[[125 sqrt(6)]] cm³"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체 ABCD-EFGH(윗면 ABCD, 아랫면 EFGH; B 좌앞 위, F 좌앞 아래, G 우앞 아래, H 우뒤 아래). 대각선 BH·FH. ∠BHF=30°(H), FG=5cm, GH=5cm(점선 치수), 색칠(분홍)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직육면체 입체 도형",
    note="FH=5√2, BF=5√2·tan30°=5√6/3 → V=25·5√6/3=125√6/3 → ② (빠른정답 없음, 풀이 답).")

# ---------------- p22
add(id="bbfec584", qtype="choice",
    question=("다음 그림과 같이 한 모서리의 길이가 6인 정육면체를 세 꼭짓점 B, C, D를 지나는 평면으로 잘라서 만든 삼각뿔의 꼭짓점 A에서 "
              "면 BCD에 내린 수선의 발을 H라 하자. [[angle(BAH) = deg(a)]]일 때, 이 삼각뿔의 부피를 [[deg(a)]]를 이용하여 나타내면?"),
    choices=["[[36 cos(deg(a))]]", "[[36 sqrt(2) cos(deg(a))]]", "[[36 sqrt(3) cos(deg(a))]]", "[[36 sqrt(2) sin(deg(a))]]", "[[36 sqrt(3) sin(deg(a))]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "정육면체(한 모서리 6)에서 꼭짓점 A(좌위)와 이웃 꼭짓점 B(좌아래)·C(우위)·D(뒤위)를 지나는 단면 BCD로 잘린 삼각뿔 A-BCD(청록색 색칠). A에서 면 BCD에 내린 수선 AH(직각 표시), ∠BAH=a°(A), 모서리 6(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정육면체 절단 삼각뿔 입체 도형",
    note="AH=6cos a°, △BCD 정삼각형(변 6√2) 넓이 18√3 → V=⅓·18√3·6cos a°=36√3 cos a° → ③ (빠른정답 없음, 풀이 답).")

# ---------------- p23
add(id="b1afad3b", qtype="choice",
    question=("다음 그림과 같이 한 모서리의 길이가 12인 정육면체를 세 꼭짓점 B, C, D를 지나는 평면으로 잘라서 만든 삼각뿔의 꼭짓점 A에서 "
              "면 BCD에 내린 수선의 발을 H라 하자. [[angle(BAH) = deg(a)]]일 때, 이 삼각뿔의 부피를 [[deg(a)]]를 이용하여 나타내면?"),
    choices=["[[288 sin(deg(a))]]", "[[288 sqrt(2) sin(deg(a))]]", "[[288 sqrt(3) sin(deg(a))]]", "[[288 sqrt(2) cos(deg(a))]]", "[[288 sqrt(3) cos(deg(a))]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "정육면체(한 모서리 12)에서 꼭짓점 A(좌위)와 이웃 꼭짓점 B(좌아래)·C(우위)·D(뒤위)를 지나는 단면 BCD로 잘린 삼각뿔 A-BCD(분홍색 색칠). A에서 면 BCD에 내린 수선 AH(직각 표시), ∠BAH=a°(A), 모서리 12(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정육면체 절단 삼각뿔 입체 도형",
    note="AH=12cos a°, △BCD 넓이 72√3 → V=⅓·72√3·12cos a°=288√3 cos a° → ⑤ (빠른정답 없음, 풀이 답).")

# ---------------- p24
add(id="d3941ce5", qtype="choice",
    question=("다음 그림과 같이 [[angle(BAC) = deg(90)]], [[angle(ACB) = deg(45)]], [[seg(BC) = 6 sqrt(2)]] cm, [[seg(BE) = 8]] cm인 "
              "삼각기둥의 겉넓이는?"),
    choices=["[[(124 + 48 sqrt(2))]] cm²", "[[(132 + 48 sqrt(2))]] cm²", "[[(140 + 48 sqrt(2))]] cm²",
             "[[(148 + 48 sqrt(2))]] cm²", "[[(156 + 48 sqrt(2))]] cm²"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각기둥(윗면 △ABC: A 위, B 좌, C 우; 아랫면 △DEF, D에 직각 표시). ∠ACB=45°(C), BC=6√2cm, BE=8cm(점선 치수), 색칠(연두)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각기둥 입체 도형",
    note="AB=AC=6 → 겉넓이 2·18+8(12+6√2)=132+48√2 → ② (빠른정답 없음, 풀이 답).")

# ---------------- p32
add(id="e47a92f9", qtype="choice",
    question=("다음 그림과 같이 실을 풀어 연을 띄웠을 때, 지면에 서서 연을 올려다본 각의 크기가 [[deg(28)]]이었다. 연을 띄운 사람의 눈높이가 "
              "1.5 m일 때, 지면에서 연까지의 높이는? (단, 연의 크기는 무시하고, [[sin(deg(28)) = 0.47]], [[cos(deg(28)) = 0.88]]로 계산한다.)"),
    choices=["[[36.8]] m", "[[37.6]] m", "[[39.1]] m", "[[40.4]] m", "[[41.8]] m"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "지면 위의 사람(좌)과 연(우상). 사람의 눈에서 연까지의 실(빗변)과 수평 점선, 연 아래 수직선(직각 표시). 올려다본 각 28°, 눈높이 1.5m, 지면의 수평 거리 70.4m(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 연·사람 실생활 직각삼각형 도형",
    note="수평거리 70.4m(그림) × tan28°(0.47/0.88) = 37.6m, +1.5m = 39.1m → ③. 빠른정답 18과 불일치(정렬 어긋남).")

# ---------------- p39
add(id="6dd4ec2e", qtype="choice",
    question=("다음 그림과 같이 지면으로부터 높이가 150 m인 전망대에서 직선 도로를 일정한 속력으로 달리고 있는 자동차를 내려다보고 있다. "
              "자동차가 B지점에 있을 때 전망대 D지점에서 자동차를 내려본각의 크기는 [[deg(45)]]이고 3초 후에 자동차가 A지점에 있을 때 "
              "자동차를 내려본 각도가 [[deg(30)]]이다. 이 자동차의 속력은?"),
    choices=["초속 [[(10 sqrt(3) - 10)]] m", "초속 [[(20 sqrt(3) - 20)]] m", "초속 [[(30 sqrt(3) - 30)]] m",
             "초속 [[(40 sqrt(3) - 40)]] m", "초속 [[(50 sqrt(3) - 50)]] m"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "지면 위 전망대(탑, 꼭대기 D, 아래 C, 높이 150m 치수)와 도로 위 자동차 A(좌)·B(D에 가까움). D에서 수평 점선, 내려본각 30°(A 방향)·45°(B 방향)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 전망대·자동차 실생활 직각삼각형 도형",
    note="CB=150, CA=150√3 → AB=150(√3−1)을 3초 → 초속 (50√3−50)m → ⑤ (빠른정답 없음, 풀이 답).")

# ---------------- p41
add(id="7bdf951c", qtype="choice",
    question=("다음 그림과 같이 실의 길이가 20 m인 추가 있다. [[angle(AOB) = deg(30)]]이고 이 추가 B의 위치에 있을 때, "
              "A를 기준으로 몇 m의 높이에 있는가?"),
    choices=["[[(20 - 10 sqrt(3))]] m", "[[(20 - 10 sqrt(2))]] m", "[[(20 - 5 sqrt(3))]] m", "[[(20 - sqrt(3))]] m", "[[5]] m"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "점 O에 매단 추: 최저점 A(수직 아래), 오른쪽 위치 B, 왼쪽 위치. 호 모양 점선 경로. ∠AOB=30°(O), OB=20m(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 추(진자) 실생활 도형",
    note="20−20cos30°=20−10√3 → ① (빠른정답 없음, 풀이 답).")

# ---------------- p42
add(id="4f3c1d56", qtype="choice",
    question=("다음 그림과 같이 시계의 추가 B지점과 B′지점 사이를 일정한 속도로 움직이고 있다. 추의 길이는 30 cm이고, "
              "[[angle(BOA)]] = ∠AOB′ = [[deg(45)]], ∠BOB′ = [[deg(90)]]이다. 추가 가장 높은 위치에 있을 때, 추는 A지점을 기준으로 하여 "
              "몇 cm의 높이에 있는가?"),
    choices=["[[15(2 - sqrt(2))]] cm", "[[20(2 - sqrt(2))]] cm", "[[25(2 - sqrt(2))]] cm", "[[30(2 - sqrt(2))]] cm", "[[35(2 - sqrt(2))]] cm"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "점 O에 매단 시계추: 최저점 A(수직 아래), 좌측 B, 우측 B′. 호 모양 점선 경로. ∠BOA=45°(O), OB=30cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="프라임 점 라벨(B′) / 도형 표현 불가: 시계추 실생활 도형",
    note="30−30cos45°=30−15√2=15(2−√2) → ① (빠른정답 없음, 풀이 답).")

# ---------------- p46
add(id="1cf28eb7", qtype="choice",
    question=("다음 그림과 같이 시계의 추가 B지점과 B′지점 사이를 일정한 속도로 움직이고 있다. 추의 길이는 40 cm이고 "
              "[[angle(BOA)]] = ∠AOB′ = [[deg(45)]]이다. 추가 가장 높은 위치에 있을 때, 추는 A지점을 기준으로 몇 cm 높이에 있는가? "
              "(단, 추의 크기는 무시한다.)"),
    choices=["[[20(2 - sqrt(2))]] cm", "[[25(2 - sqrt(2))]] cm", "[[30(2 - sqrt(2))]] cm", "[[35(2 - sqrt(2))]] cm", "[[40(2 - sqrt(2))]] cm"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "점 O에 매단 시계추: 최저점 A(수직 아래), 좌측 B, 우측 B′. 호 모양 점선 경로. ∠BOA=45°, ∠AOB′=45°(O), OB=40cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="프라임 점 라벨(B′) / 도형 표현 불가: 시계추 실생활 도형",
    note="40−40cos45°=40−20√2=20(2−√2) → ① (빠른정답 없음, 풀이 답).")

# ---------------- p52
add(id="afa834fc", qtype="choice",
    question=("다음 그림과 같은 정삼각형 ABC의 각 변 위의 세 점 D, E, F에 대하여 "
              "[[ratio(seg(AD), seg(DB)) = ratio(seg(BE), seg(EC)) = ratio(seg(CF), seg(FA)) = ratio(1,4)]], "
              "[[seg(BE) = 6]]일 때, [[seg(EF)]]의 길이는?"),
    choices=["[[3 sqrt(13)]]", "[[4 sqrt(13)]]", "[[5 sqrt(13)]]", "[[6 sqrt(13)]]", "[[7 sqrt(13)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 ABC(A 위, B 좌하, C 우하). AB 위의 D(A 근처), BC 위의 E(B 근처), CA 위의 F(C 근처). 선분 DE·EF·FD. BE=6(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형+내접삼각형 도형",
    note="한 변 30, EC=24, CF=6 → EF²=576+36−144=468 → 6√13 → ④ (빠른정답 없음, 풀이 답).")

# ---------------- p53
add(id="f4a19f34", qtype="choice",
    question=("다음 그림과 같은 정삼각형 ABC의 각 변 위의 세 점 D, E, F에 대하여 "
              "[[ratio(seg(AD), seg(DB)) = ratio(seg(BE), seg(EC)) = ratio(seg(CF), seg(FA)) = ratio(1,3)]], "
              "[[seg(BE) = 4]]일 때, [[seg(EF)]]의 길이는?"),
    choices=["[[sqrt(110)]]", "[[4 sqrt(7)]]", "[[sqrt(114)]]", "[[2 sqrt(29)]]", "[[sqrt(118)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 ABC(A 위, B 좌하, C 우하). AB 위의 D(A 근처), BC 위의 E(B 근처), CA 위의 F(C 근처). 선분 DE·EF·FD. BE=4(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형+내접삼각형 도형",
    note="한 변 16, EC=12, CF=4 → EF²=144+16−48=112 → 4√7 → ② (빠른정답 없음, 풀이 답).")

# ---------------- p55 (같은 이미지에 id 2개, 인쇄된 문항은 1개 → dup)
dup(["e7d463e3", "3b392842"], qtype="choice",
    question=("다음은 아래 그림과 같은 [[tri(ABC)]]에서 [[angle(B) = deg(60)]], [[seg(BC) = 6]], [[seg(AB) = 4]]일 때, "
              "[[seg(AC)]]의 길이를 구하는 과정이다. □ 안의 값이 옳지 않은 것은?\n"
              "점 A에서 [[seg(BC)]]에 내린 수선의 발을 H라 하면\n"
              "[[seg(AH)]] = 4 × (가) = 4 × (나) = [[2 sqrt(3)]]\n"
              "[[seg(BH)]] = 4 × (다) = 4 × (라) = 2,\n"
              "[[seg(CH) = 6 - 2 = 4]]\n"
              "∴ [[seg(AC)]] = √( (마)² + [[pow(4,2)]] ) = [[2 sqrt(7)]]"),
    choices=["(가) [[sin(deg(60))]]", "(나) [[frac(sqrt(3),2)]]", "(다) [[tan(deg(60))]]", "(라) [[frac(1,2)]]", "(마) [[2 sqrt(3)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC: B 좌하, C 우하, A 위(좌측). ∠B=60°(B), AB=4, BC=6(점선 치수). 아래에 풀이 과정 상자((가)~(마) 빈칸)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 도형",
    note="(다)는 cos60°이어야 함 → ③ (빠른정답 없음, 풀이 답). 같은 이미지에 id 2개이나 인쇄된 문항은 1개 → 동일 내용 dup.")

# ---------------- p57
add(id="ff6ce841", qtype="short",
    question=("다음 그림과 같이 숲의 폭 [[seg(AB)]]의 길이를 구하기 위하여 숲의 바깥쪽에 지점 C를 정하고 필요한 부분을 측정하였더니 "
              "[[seg(AC) = 4 sqrt(2)]] m, [[seg(BC) = (4 + 4 sqrt(3))]] m, [[angle(ACB) = deg(45)]]이었다. 이때 숲의 폭 [[seg(AB)]]의 길이를 구하시오."),
    choices=None, derived_answer="8 m",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC: C 위, A 좌하, B 우하(AB 구간에 숲 삽화). ∠ACB=45°(C), AC=4√2m, BC=(4+4√3)m(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+숲 삽화 도형",
    note="A에서 BC에 내린 수선 4, CH=4, BH=4√3 → AB=8m = 빠른정답 ✓.")

# ---------------- p59
add(id="1e41d110", qtype="short",
    question="다음 그림과 같은 [[tri(ABC)]]에서 [[angle(B) = deg(45)]], [[seg(AB) = 3 sqrt(2)]], [[seg(BC) = 7]]일 때, [[seg(AC)]]의 길이를 구하시오.",
    choices=None, derived_answer="5",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC: B 좌하, C 우하, A 위(좌측). ∠B=45°(B), AB=3√2, BC=7(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 도형",
    note="수선 AH=3, BH=3, CH=4 → AC=5 (빠른정답 없음, 풀이 답).")

# ---------------- p63
add(id="9277850f", qtype="choice",
    question="다음 그림에서 [[seg(AB) = 4]], [[seg(BC) = 6]], [[angle(ABC) = deg(60)]]일 때, [[seg(AC)]]의 길이는?",
    choices=["[[2 sqrt(6)]]", "[[sqrt(26)]]", "[[3 sqrt(3)]]", "[[2 sqrt(7)]]", "[[5]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC: A 좌상, C 우상, B 아래. ∠ABC=60°(B), AB=4, BC=6(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 도형",
    note="AC²=16+36−24=28 → 2√7 → ④ (빠른정답 없음, 풀이 답).")

# ---------------- p68
add(id="2ec7df69", qtype="choice",
    question=("다음 그림과 같이 도로의 양쪽에 위치한 두 지점 A, B 사이의 거리를 구하기 위하여 B지점과 같은 쪽에 C지점을 잡고 "
              "필요한 부분을 측량하였더니 [[angle(CAB) = deg(30)]], [[angle(CBA) = deg(60)]], [[seg(BC) = 40]] m이었다. "
              "이때 두 지점 A, B 사이의 거리는?"),
    choices=["[[60]] m", "[[70]] m", "[[80]] m", "[[90]] m", "[[100]] m"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC: A 좌, B 우, C 우상. A와 B 사이에 세로 도로(실선 2개+가운데 점선). ∠CAB=30°(A), ∠CBA=60°(B), BC=40m(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+도로 삽화 도형",
    note="∠C=90° → AB=40/sin30°=80m → ③. 빠른정답 8과 불일치(정렬 어긋남).")

# ---------------- p69
add(id="edfdaa7d", qtype="choice",
    question=("다음 그림과 같이 연못의 가장자리의 두 지점 A, B 사이의 거리를 구하기 위하여 연못의 바깥쪽 P지점에서 필요한 부분을 측량하였더니 "
              "[[seg(PB) = 20]] m, [[angle(PAB) = deg(75)]], [[angle(PBA) = deg(60)]]이었다. 이때 두 지점 A, B 사이의 거리는?"),
    choices=["[[20(sqrt(2) - 1)]] m", "[[20(sqrt(3) - 1)]] m", "[[20]] m", "[[20(sqrt(2) + 1)]] m", "[[20(sqrt(3) + 1)]] m"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "연못 삽화 위의 삼각형 PAB: P 위, A 좌하, B 우하. ∠PAB=75°(A), ∠PBA=60°(B), PB=20m(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+연못 삽화 도형",
    note="∠P=45°, AB=20·sin45°/sin75°=20(√3−1) → ② (빠른정답 없음, 풀이 답).")

# ---------------- p70
add(id="bb7a63ef", qtype="choice",
    question=("세 지점 A, B, C에 대하여 다음 그림과 같이 측량하였더니 [[seg(BC) = 120]] m, [[angle(B) = deg(75)]], [[angle(C) = deg(60)]]이었다. "
              "이때 두 지점 A, B 사이의 거리는?"),
    choices=["[[60]] m", "[[60 sqrt(2)]] m", "[[60 sqrt(3)]] m", "[[60 sqrt(6)]] m", "[[180]] m"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC: A 위, B 좌하, C 우하. 가운데를 가로지르는 강 삽화. ∠B=75°(B), ∠C=60°(C), BC=120m(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+강 삽화 도형",
    note="∠A=45°, AB=120·sin60°/sin45°=60√6 → ④ (빠른정답 없음, 풀이 답).")
