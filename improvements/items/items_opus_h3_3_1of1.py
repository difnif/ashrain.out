# -*- coding: utf-8 -*-
# esc_opus_h3-3_1of1 — 이미지 기준 전사 (74 항목 / 72쪽; 포물선 p38·직선과 평면의 위치 관계 p45는 id 2개)
# 주: 파서(mathir.py v1.4)의 토크나이저가 'point3'을 'point'+'3'으로 쪼개므로 3차원 좌표는 vcomp(x,y,z)로 적음(표시 동일).
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

FIG = lambda raw: [{"fn": "unsupported", "args": {"raw": raw}}]

# ───────────────────────── 선분의 내분점 ─────────────────────────
# p7
add(id="02494a6f", qtype="choice",
    question=("좌표공간에 원점 O와 점 A[[vcomp(4, -8, 4)]]를 꼭짓점으로 하는 다음 그림과 같은 정육면체가 있다. "
              "선분 BC를 [[ratio(2, 1)]]로 내분하는 점을 L, 선분 DE를 [[ratio(2, 3)]]으로 내분하는 점을 M, "
              "평면 GLM이 선분 OA와 만나는 점을 N이라 하자. 점 N의 좌표가 [[vcomp(a, b, c)]]일 때, [[a + b + c]]의 값은?"),
    choices=["[[-frac(8, 15)]]", "[[-frac(4, 15)]]", "[[0]]", "[[frac(4, 15)]]", "[[frac(8, 15)]]"],
    derived_answer="③",
    figure=FIG("정육면체(꼭짓점 O, A, B, C, D, E, F, G): 점 L(BC 위), M(DE 위), N(OA 위), 평면 GLM 단면 음영"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표공간 정육면체·단면 음영",
    note="N은 선분 OA 위의 점이므로 N=t(4,−8,4) → a+b+c=0 → ③ = 빠른정답 ✓.")

# p53
add(id="db2cda87", qtype="short",
    question=("그림과 같이 좌표공간의 원점 O와 점 A[[vcomp(0, 0, 5)]]를 두 꼭짓점으로 하는 정육면체 ABCD−EFOG가 있다. "
              "[[angle(ADO)]]의 이등분선이 선분 AO와 만나는 점을 P라 할 때, 점 P의 [[z]]좌표는 [[p + q sqrt(2)]] 이다. "
              "[[pow(p,2) + pow(q,2)]]의 값을 구하시오. (단, [[p]], [[q]]는 유리수이다.)"),
    choices=None, derived_answer="125",
    figure=FIG("좌표공간(x, y, z축)의 정육면체 ABCD−EFOG: O가 원점, A가 z축 위 (0,0,5), 점 P가 대각선 AO 위, 선분 DP·DO 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표공간 정육면체",
    note="AD:DO=1:√2 → AP=5(√2−1) → P의 z좌표 10−5√2 → p²+q²=125 (빠른정답 3과 불일치).")

# ───────────────────────── 위치벡터 ─────────────────────────
_p37_head = ("두 점 A, B의 위치벡터를 각각 [[vec(a)]], [[vec(b)]]라 할 때, 두 점 A, B를 지나는 직선 [[l]] 위의 임의의 점 P의 위치벡터 [[vec(p)]]는\n"
             "[[vec(p) = (1 - t) vec(a) + t vec(b)]] ([[t]]는 실수)로 나타낼 수 있다.\n"
             "다음 그림과 같이 직선 [[l]]을 ㉠~㉤의 5개의 부분으로 나누었을 때, 옳은 것만을 보기에서 있는 대로 고른 것은? "
             "(단, [[seg(CA) = seg(AB) = seg(BD)]]이고, 네 점 A, B, C, D는 ㉠~㉤의 어떤 부분에도 포함되지 않는다.)\n<보기>\n")
_p37_fig = FIG("좌표평면: 원점 O에서 벡터 a→(→A), b→(→B), 직선 l 위에 순서대로 C, A, B, D. l을 ㉠(C 왼쪽)·㉡(C~A)·㉢(A~B)·㉣(B~D)·㉤(D 오른쪽)의 5부분으로 표시")
# p37
add(id="cc390715", qtype="choice",
    question=(_p37_head +
              "ㄱ. 점 P가 ㉣에 있도록 하는 [[t]]의 값의 범위는 [[1 < t < 2]]이다.\n"
              "ㄴ. [[t < 0]]이면 점 P는 ㉠에 있다.\n"
              "ㄷ. 직선 [[l]] 위의 점 Q의 위치벡터가 [[(1 - sub(t,1)) vec(a) + sub(t,1) vec(b)]] ([[sub(t,1)]]은 실수)일 때, "
              "[[seg(PQ)]]의 중점 M이 ㉡에 있으려면 [[0 < t + sub(t,1) < 2]]이다."),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    derived_answer="①", figure=_p37_fig, difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 직선 l의 5개 구간(㉠~㉤) 표시",
    note="㉣: 1<t<2 ㄱ✓; t<0이면 ㉠ 또는 ㉡ ㄴ✗; 중점의 매개변수 (t+t₁)/2가 ㉡(−1~0)이려면 −2<t+t₁<0 ㄷ✗ → ① = 빠른정답 ✓.")

# p38
add(id="a4e64f25", qtype="choice",
    question=(_p37_head +
              "ㄱ. 점 P가 ㉢에 있도록 하는 [[t]]의 값의 범위는 [[0 < t < 1]]이다.\n"
              "ㄴ. [[t < 2]]이면 점 P는 ㉤에 있지 않다.\n"
              "ㄷ. 직선 [[l]] 위의 점 Q의 위치벡터가 [[(1 - sub(t,1)) vec(a) + sub(t,1) vec(b)]] ([[sub(t,1)]]은 실수)일 때, "
              "[[3 < 2t + sub(t,1) < 6]]이면 선분 PQ를 [[ratio(1, 2)]]로 내분하는 점 R는 ㉣에 있다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤", figure=_p37_fig, difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 직선 l의 5개 구간(㉠~㉤) 표시",
    note="ㄱ✓ ㄴ✓(㉤은 t>2); R의 매개변수 (2t+t₁)/3 ∈ (1,2) → ㉣ ㄷ✓ → ⑤ = 빠른정답 ✓.")

# p63
add(id="dacedef4", qtype="short",
    question=("삼각형 OAB의 변 AB 위의 점 [[sub(P,k)]] ([[k]]는 자연수)에 대하여 [[vec(OA) = vec(a)]], [[vec(OB) = vec(b)]], "
              "[[sub(vec(OP), k) = sub(vec(p), k)]]라 하자. [[seg(AB) = 27]]이고 "
              "[[sub(vec(p), k) = (1 - frac(1, pow(3,k))) vec(a) + frac(1, pow(3,k)) vec(b)]]일 때,\n"
              "[[abs(sub(vec(AP), 1)) + abs(sub(vec(AP), 2)) + abs(sub(vec(AP), 3)) + abs(sub(vec(AP), 4))]] 의 값을 구하시오."),
    choices=None, derived_answer="frac(40, 3)",
    figure=FIG("삼각형 OAB: O에서 A로 벡터 a→, B로 벡터 b→, 변 AB 위의 점 P_k로 벡터 p_k→, AB=27 표시"),
    difficulty_est=2, confidence=0.75,
    needs_review="첨자 점 라벨(P_k, OP_k→, AP₁→ 등)을 sub(vec(..), k)로 우회 / 도형(삼각형·벡터)",
    note="AP_k = 27/3^k → 9+3+1+1/3 = 40/3 = 빠른정답 ✓.")

# p64
add(id="98ad6fdd", qtype="short",
    question=("다음 그림과 같이 삼각형 ABC에서 [[seg(AB)]]의 중점을 D, [[seg(AC)]]를 [[ratio(2, 1)]]로 내분하는 점을 E, "
              "[[seg(DE)]]의 중점을 F, [[seg(AF)]]의 연장선과 [[seg(BC)]]가 만나는 점을 G라고 하자.\n"
              "[[frac(tri(ADF) + tri(BGF) + tri(CEF), tri(AFE) + tri(BFD) + tri(CFG)) = frac(n, m)]] 일 때, [[m + n]]의 값을 구하시오.\n"
              "(단, [[m]], [[n]]은 서로소인 자연수이다.)"),
    choices=None, derived_answer="84",
    figure=FIG("삼각형 ABC: D(AB 위), E(AC 위), F(DE 위), G(BC 위), 선분 AG·BF·CF·DE; 삼각형 ADF, BGF, CEF 음영"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 내부 분할·음영",
    note="좌표 계산: 분자 41/168, 분모 43/168 → 41/43 → m+n=84 (빠른정답 3과 불일치).")

# p65
add(id="b4db7275", qtype="short",
    question=("다음 그림과 같이 삼각형 ABC에서 [[seg(AB)]]를 [[ratio(4, 1)]]으로 내분하는 점을 D, [[seg(AC)]]의 중점을 E, "
              "[[seg(DE)]]을 [[ratio(3, 2)]]로 내분하는 점을 F, [[seg(AF)]]의 연장선과 [[seg(BC)]]가 만나는 점을 G라고 하자. "
              "[[frac(tri(ADF) + tri(BGF) + tri(CEF), tri(AFE) + tri(BFD) + tri(CFG)) = frac(n, m)]] 일 때, [[m + n]]의 값을 구하시오.\n"
              "(단, [[m]], [[n]]은 서로소인 자연수이다.)"),
    choices=None, derived_answer="310",
    figure=FIG("삼각형 ABC: D(AB 위), E(AC 위), F(DE 위), G(BC 위), 선분 AG·BF·CF·DE; 삼각형 ADF, BGF, CEF 음영"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 내부 분할·음영",
    note="좌표 계산: 181/129 → m+n=310 = 빠른정답 ✓.")

# ───────────────────────── 삼수선 정리 ─────────────────────────
# p21 — [2018년 11월 고3 이과 19번/4점]
add(id="4e591b6f", qtype="choice",
    question=("한 변의 길이가 12인 정삼각형 BCD를 한 면으로 하는 사면체 ABCD의 꼭짓점 A에서 평면 BCD에 내린 수선의 발을 H라 할 때, "
              "점 H는 삼각형 BCD의 내부에 놓여 있다. 삼각형 CDH의 넓이는 삼각형 BCH의 넓이의 3배, 삼각형 DBH의 넓이는 삼각형 BCH의 넓이의 2배이고 "
              "[[seg(AH) = 3]]이다. 선분 BD의 중점을 M, 점 A에서 선분 CM에 내린 수선의 발을 Q라 할 때, 선분 AQ의 길이는?"),
    choices=["[[sqrt(11)]]", "[[2 sqrt(3)]]", "[[sqrt(13)]]", "[[sqrt(14)]]", "[[sqrt(15)]]"],
    derived_answer="③",
    figure=FIG("사면체 ABCD: 밑면 BCD, 꼭짓점 A에서 밑면에 내린 수선의 발 H(직각 표시)"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 사면체",
    note="출처 [2018년 11월 고3 이과 19번/4점]. H에서 BC·CD까지 거리 √3, 3√3 → H에서 CM까지 거리 2 → AQ=√(9+4)=√13 → ③ (빠른정답 2와 불일치).")

# p24
add(id="2c3edd67", qtype="choice",
    question=("한 변의 길이가 16인 정삼각형 BCD를 한 면으로 하는 사면체 ABCD의 꼭짓점 A에서 평면 BCD에 내린 수선의 발을 H라 할 때, "
              "점 H는 삼각형 BCD의 내부에 놓여 있다. 삼각형 CDH의 넓이는 삼각형 BCH의 넓이의 4배, 삼각형 DBH의 넓이는 삼각형 BCH의 넓이의 3배이고 "
              "[[seg(AH) = 5]]이다. 선분 BD의 중점을 M, 점 A에서 선분 CM에 내린 수선의 발을 Q라 할 때, 선분 AQ의 길이는?"),
    choices=["[[sqrt(26)]]", "[[2 sqrt(7)]]", "[[sqrt(30)]]", "[[4 sqrt(2)]]", "[[sqrt(34)]]"],
    derived_answer="⑤",
    figure=FIG("사면체 ABCD(면 음영): 밑면 BCD, 꼭짓점 A에서 밑면에 내린 수선의 발 H(직각 표시)"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 사면체",
    note="H에서 BC·CD까지 거리 √3, 4√3 → H에서 CM까지 거리 3 → AQ=√(25+9)=√34 → ⑤ (빠른정답 3과 불일치).")

# p43
add(id="c417ccde", qtype="choice",
    question=("그림과 같이 [[seg(AB) = 1]], [[seg(BC) = 2]]인 직사각형 ABCD 모양의 종이가 있다. 선분 BC 위의 점 P와 선분 AD 위의 점 Q에 대하여 "
              "선분 PQ를 접는 선으로 하여 점 C의 평면 ABPQ 위로의 수선의 발이 점 A가 되도록 종이를 접었다. "
              "평면 ABPQ와 평면 CDQP가 이루는 각을 [[theta]]라 할 때, [[cos(theta)]]의 최솟값은?"),
    choices=["[[frac(1, 4)]]", "[[frac(1, 5)]]", "[[frac(1, 6)]]", "[[frac(1, 7)]]", "[[frac(1, 8)]]"],
    derived_answer="①",
    figure=FIG("직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상): 변 BC 위의 점 P(B 근처)와 변 AD 위의 점 Q를 잇는 점선(접는 선)"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 직사각형 위 접는 선 PQ",
    note="PQ⊥AC, cosθ=AF/CF(F=AC∩PQ); P=B일 때 최소 1/4 → ① (빠른정답 3과 불일치, 검토 필요).")

# p44
add(id="87d2be36", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 3]], [[seg(BC) = 4 sqrt(3)]] 인 직사각형 모양의 종이 ABCD가 있다. 선분 BC를 [[ratio(1, 3)]]으로 내분하는 점을 P라 할 때, "
              "선분 DP를 접는 선으로 하여 종이를 접고 두 선분 PC와 AD의 교점을 E라 하자. 다시 선분 EP를 접는 선으로 하여 점 A의 평면 DEP 위로의 정사영이 "
              "선분 DP 위에 있도록 접자. 이때 두 평면 APE와 DEP가 이루는 각을 [[theta]]라 할 때, [[30 cos(theta)]]의 값을 구하시오. (단, 종이의 두께는 무시한다.)"),
    choices=None, derived_answer="10",
    figure=FIG("두 단계 그림: (위) 직사각형 ABCD를 DP로 접어 C가 옮겨진 모습(원래 위치 C′ 점선), 교점 E; (아래) EP로 다시 접어 A가 들린 모습(A′, B′ 점선, 수선 표시)"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 종이접기 2단계 입체도(프라임 라벨 A′, B′, C′)",
    note="P=(√3,0), E=(2√3,3), △APE 정삼각형(변 2√3) → cosθ=1/3 → 30cosθ=10 (빠른정답 5와 불일치, 검토 필요).")

# p45
add(id="c47a61b2", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 4]], [[seg(BC) = 6 sqrt(3)]] 인 직사각형 모양의 종이 ABCD가 있다. 선분 BC를 [[ratio(1, 2)]]로 내분하는 점을 P라 할 때, "
              "선분 DP를 접는 선으로 하여 종이를 접고 두 선분 PC와 AD의 교점을 E라 하자. 다시 선분 EP를 접는 선으로 하여 점 A의 평면 DEP 위로의 정사영이 "
              "선분 DP 위에 있도록 접자. 이때 두 평면 APE와 DEP가 이루는 각을 [[theta]]라 할 때, [[30 cos(theta)]]의 값을 구하시오.\n"
              "(단, 종이의 두께는 무시한다.)"),
    choices=None, derived_answer="6",
    figure=FIG("두 단계 그림: (위) 직사각형 ABCD를 DP로 접어 C가 옮겨진 모습(원래 위치 C′ 점선), 교점 E; (아래) EP로 다시 접어 A가 들린 모습(A′, B′ 점선, 수선 표시)"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 종이접기 2단계 입체도(프라임 라벨 A′, B′, C′)",
    note="P=(2√3,0), E=(10√3/3,4), A에서 EP까지 거리 5, 정사영점까지 1 → cosθ=1/5 → 6 (빠른정답 5와 불일치, 검토 필요).")

# p77
add(id="8127b972", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(BD) = 13]], [[seg(AD) = sqrt(26)]] 인 평행사변형 ABCD 모양의 종이를 대각선 BD를 접는 선으로 하여 "
              "삼각형 ABD를 접어 올렸다. 점 A에서 평면 BCD에 내린 수선의 발을 H라 하면 직선 BH는 선분 CD의 중점 M을 지난다. "
              "두 평면 ABD와 BCD가 이루는 예각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값은?\n"
              "(단, 점 H는 삼각형 BCD의 외부에 있고, 종이의 두께는 고려하지 않는다.)"),
    choices=["[[frac(sqrt(31), 7)]]", "[[frac(4 sqrt(2), 7)]]", "[[frac(sqrt(34), 7)]]", "[[frac(sqrt(35), 7)]]", "[[frac(6, 7)]]"],
    derived_answer="⑤",
    figure=FIG("[그림 1] 평행사변형 ABCD와 점선 대각선 BD; [그림 2] BD로 접어 올린 삼각형 ABD(음영), A에서 내린 수선의 발 H, CD의 중점 M"),
    difficulty_est=4, confidence=0.85,
    needs_review="도형 표현 불가: 접은 평행사변형 입체도",
    note="A에서 BD까지 거리 5, H=(12,30/7) → cosθ=(30/7)/5=6/7 → ⑤ = 빠른정답 ✓.")

# p79
add(id="d6aa0c9b", qtype="short",
    question=("다음 그림과 같이 직선 [[l]]을 교선으로 하고 이루는 각의 크기가 [[frac(pi, 4)]] 인 두 평면 [[alpha]]와 [[beta]]가 있고, "
              "평면 [[alpha]] 위의 점 A와 평면 [[beta]] 위의 점 B가 있다. 두 점 A, B에서 직선 [[l]]에 내린 수선의 발을 각각 C, D라 하자. "
              "[[seg(AB) = 4]], [[seg(AD) = 5]]이고, 직선 AB와 평면 [[beta]]가 이루는 각의 크기가 [[frac(pi, 3)]] 일 때, "
              "사면체 ABCD의 부피는 [[a]]이다. [[12a]]의 값을 구하시오."),
    choices=None, derived_answer="36",
    figure=FIG("교선 l에서 π/4로 만나는 두 평면 α(위, A 포함)·β(아래, B 포함), A·B에서 l에 내린 수선의 발 C, D, 점선 보조선"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 이면각 입체도",
    note="A의 높이 2√3, AC=2√6, CD=1, BD=3√3(그림상 B가 A의 정사영보다 l에서 먼 쪽) → 부피 3 → 36 = 빠른정답 ✓ (BD=√3인 경우 12).")

# p83
add(id="944ec8e1", qtype="short",
    question=("그림과 같이 직선 [[l]]을 교선으로 하고 이루는 각의 크기가 [[deg(45)]]인 두 평면 [[alpha]]와 [[beta]]가 있고, "
              "평면 [[alpha]] 위의 점 A와 평면 [[beta]] 위의 점 B가 있다. 두 점 A, B에서 직선 [[l]]에 내린 수선의 발을 각각 C, D라 하자. "
              "[[seg(AB) = 2]], [[seg(AD) = sqrt(3)]] 이고 직선 AB와 평면 [[beta]]가 이루는 각의 크기가 [[deg(30)]]일 때, "
              "사면체 ABCD의 부피는 [[a + b sqrt(2)]] 이다. [[36(a + b)]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수이다.)"),
    choices=None, derived_answer="12",
    figure=FIG("교선 l에서 45°로 만나는 두 평면 α(A 포함)·β(B 포함), 수선의 발 C, D, 점선 보조선"),
    difficulty_est=4, confidence=0.7,
    needs_review="도형 표현 불가: 이면각 입체도",
    note="A의 높이 1, AC=√2, CD=1, BD=1+√2 → 부피 (1+√2)/6 → a=b=1/6 → 12 (빠른정답 1과 불일치; BD=√2−1인 경우 0).")

# p85
add(id="dff8de4b", qtype="short",
    question=("그림과 같이 평면 [[alpha]] 위의 점 A, C에 대하여 점 A에서 평면 [[beta]]에 내린 수선의 발을 H, 두 평면 [[alpha]], [[beta]]의 교선 [[l]]에 "
              "내린 수선의 발을 B라 하면 [[seg(AH) = seg(BH)]]이고 두 삼각형 ABH와 ABC는 서로 합동이다. 직선 BC와 평면 [[beta]]가 이루는 각의 크기 [[theta]]에 대하여 "
              "[[pow(cos(theta), 2) = frac(q, p)]] 일 때, [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="7",
    figure=FIG("교선 l로 만나는 두 평면 α(A, C 포함)·β(H 포함): A에서 β에 내린 수선의 발 H, l에 내린 수선의 발 B, 삼각형 ABH·ABC, 직각 표시"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 이면각 입체도",
    note="이면각 45°, AH=BH=1, AC=BC=1 → C=(±1/√2,1/2,1/2) → sinθ=1/2 → cos²θ=3/4 → 7 (빠른정답 5와 불일치).")

# p86
add(id="739bf5bb", qtype="short",
    question=("다음 그림과 같이 직선 [[l]]을 교선으로 하고 이루는 각의 크기가 [[frac(pi, 6)]] 인 두 평면 [[alpha]]와 [[beta]]가 있고, "
              "평면 [[alpha]] 위의 점 A와 평면 [[beta]] 위의 점 B가 있다. 두 점 A, B에서 직선 [[l]]에 내린 수선의 발을 각각 C, D라 하자. "
              "[[seg(AB) = 2]], [[seg(AD) = 3]]이고, 직선 AB와 평면 [[beta]]가 이루는 각의 크기가 [[frac(pi, 4)]] 일 때, "
              "사면체 ABCD의 부피는 [[a sqrt(2) + b sqrt(3)]] 이다. [[36(a + b)]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수이다.)"),
    choices=None, derived_answer="18",
    figure=FIG("교선 l에서 π/6으로 만나는 두 평면 α(A 포함)·β(B 포함), 수선의 발 C, D, 점선 보조선"),
    difficulty_est=4, confidence=0.7,
    needs_review="도형 표현 불가: 이면각 입체도",
    note="A의 높이 √2, AC=2√2, CD=1, BD=√6+1 → 부피 (2√3+√2)/6 → a=1/6, b=1/3 → 18 (빠른정답 12와 불일치; BD=√6−1인 경우 6).")

# ───────────────────────── 직선의 방정식 (자취의 방정식) ─────────────────────────
# p92 — [2018년 9월 고3 이과 29번/4점]
add(id="7fd00511", qtype="short",
    question=("좌표공간에서 점 A[[vcomp(3, frac(1,2), 2)]]와 평면 [[z = 1]] 위의 세 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]이\n"
              "[[dot(vec(OA), sub(vec(OP), 1)) = frac(11, 3)]],\n[[dot(vec(OA), sub(vec(OP), 2)) = 1]],\n[[dot(vec(OA), sub(vec(OP), 3)) = -frac(7, 4)]]\n"
              "을 만족시킨다. 점 [[vcomp(0, k, 0)]]을 지나고 방향벡터가 [[vcomp(1, -6, 0)]]인 직선을 [[l]]이라 하고, 직선 [[l]]에 의해 나누어지는 xy평면의 두 영역을 각각 "
              "[[alpha]], [[beta]]라 하자. 세 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]에서 xy평면에 내린 수선의 발이 모두 [[alpha]]에만 포함되거나 모두 [[beta]]에만 포함되도록 하는 "
              "양의 정수 [[k]]의 최솟값을 [[m]], 음의 정수 [[k]]의 최댓값을 [[M]]이라 할 때, [[m - M]]의 값을 구하시오. (단 O는 원점이다.)"),
    choices=None, derived_answer="12", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="첨자 점 라벨 벡터(OP₁→ 등)를 sub(vec(OP),1)로 우회",
    note="출처 [2018년 9월 고3 이과 29번/4점]. 수선의 발은 6x+y=10/3, −2, −15/2 위 → k>10/3 또는 k<−15/2 → m=4, M=−8 → 12 (빠른정답 2와 불일치).")

# p95
_p95_tail = ("의 두 교점을 각각 [[sub(S,n)]], [[sub(T,n)]]이라 하자. 두 벡터 [[vec(AB)]]와 [[sub(S,n)]][[sub(T,n)]]→이 서로 수직이 되도록 하는 [[n]]의 값을 [[k]]라 할 때,\n"
             "[[abs(sub(vec(OS), 1) + sub(vec(OT), 1))]] + [[abs(sub(vec(OS), 2) + sub(vec(OT), 2))]] + ⋯ + [[abs(sub(vec(OS), k) + sub(vec(OT), k))]]\n"
             "의 값은 ")
add(id="d2063d54", qtype="short",
    question=("좌표평면에서 두 점 A[[point(2, 6)]], B[[point(8, 2)]]에 대하여 [[dot((vec(OP) - vec(OA)), (vec(OP) - vec(OB))) = 0]]을 만족시키는 점 P가 나타내는 도형과 "
              "직선 [[frac(x - 5, n + 1) = frac(y - 4, n + 5)]] ([[n]] = 1, 2, 3, ⋯)" + _p95_tail +
              "[[a sqrt(41)]] 이다. 자연수 [[a]]의 값을 구하시오. (단, O는 원점이다.)"),
    choices=None, derived_answer="14", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="첨자 점 라벨 벡터(SₙTₙ→, OS₁→ 등) 텍스트 혼합",
    note="지름 AB인 원(중심 (5,4), 반지름 √13), 직선은 중심을 지남 → |OS+OT|=2√41; AB⊥방향 ⇔ 2n−14=0, k=7 → 14√41 → a=14 (빠른정답 12와 불일치).")

# p96
add(id="e653b63d", qtype="short",
    question=("좌표평면에서 두 점 A[[point(3, 8)]], B[[point(5, 2)]]에 대하여 [[dot((vec(OP) - vec(OA)), (vec(OP) - vec(OB))) = 0]]을 만족시키는 점 P가 나타내는 도형과 "
              "직선 [[frac(x - 4, n + 8) = frac(y - 5, n)]] ([[n]] = 1, 2, 3, ⋯)" + _p95_tail +
              "[[a sqrt(41)]] 이다. 자연수 [[a]]의 값을 구하시오. (단, O는 원점이다.)"),
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="첨자 점 라벨 벡터(SₙTₙ→, OS₁→ 등) 텍스트 혼합",
    note="중심 (4,5), |OS+OT|=2√41; AB=(2,−6)⊥(n+8,n) ⇔ 16−4n=0, k=4 → 8√41 → a=8 (빠른정답 3과 불일치).")

# p97
add(id="8096a92b", qtype="short",
    question=("좌표평면에서 두 점 A[[point(2, 3)]], B[[point(6, 1)]]에 대하여 [[dot((vec(OP) - vec(OA)), (vec(OP) - vec(OB))) = 0]]을 만족시키는 점 P가 나타내는 도형과 "
              "직선 [[frac(x - 4, n + 1) = frac(y - 2, n + 7)]] ([[n]] = 1, 2, 3, ⋯)" + _p95_tail +
              "[[a sqrt(5)]] 이다. 자연수 [[a]]의 값을 구하시오. (단, O는 원점이다.)"),
    choices=None, derived_answer="20", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="첨자 점 라벨 벡터(SₙTₙ→, OS₁→ 등) 텍스트 혼합",
    note="중심 (4,2), |OS+OT|=4√5; AB=(4,−2)⊥(n+1,n+7) ⇔ 2n−10=0, k=5 → 20√5 → a=20 = 빠른정답 ✓.")

# ───────────────────────── 쌍곡선 ─────────────────────────
# p75
add(id="485d041c", qtype="short",
    question=("다음 그림과 같이 두 초점이 F, F′인 쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), 81) = 1]]의 점근선에 중심이 C[[point(0, r)]] ([[r > 0]])인 원이 접하고, "
              "선분 CF는 점근선과 수직으로 만나고 있다. 중심이 원점 O이고 점 C를 지나는 원이 쌍곡선과 제1사분면에서 만나는 점을 P라 할 때, "
              "[[seg(PF)]] · [[seg(PF)]]′의 값을 구하시오.\n(단, 점 F의 [[x]]좌표는 양수이다.)"),
    choices=None, derived_answer="82",
    figure=FIG("좌표평면: 쌍곡선 x²/9−y²/81=1과 점근선(점선), 초점 F′·F(x축), y축 위의 점 C를 중심으로 점근선에 접하는 작은 원, 원점 중심·C를 지나는 원, 제1사분면 교점 P, 선분 PF·PF′·CF"),
    difficulty_est=3, confidence=0.75,
    needs_review="프라임 라벨(F′, 선분 PF′) 텍스트 혼합 / 도형 표현 불가: 쌍곡선·원 복합 좌표평면",
    note="c=3√10, CF⊥(y=3x) → r=√10 → P: x²=91/10 → PF·PF′=e²x²−a²=91−9=82 (빠른정답 4와 불일치).")

# ───────────────────────── 구의 방정식 ─────────────────────────
# p25 — [2007년 9월 고3 이과 23번]
add(id="1dd99307", qtype="short",
    question=("좌표공간에서 [[x y]]평면 위의 원 [[pow(x,2) + pow(y,2) = 1]]을 [[C]]라 하고, 원 [[C]] 위의 점 P와 점 A[[vcomp(0, 0, 3)]]을 잇는 선분이 "
              "구 [[pow(x,2) + pow(y,2) + pow(z - 2, 2) = 1]]과 만나는 점을 Q라 하자. 점 P가 원 [[C]] 위를 한 바퀴 돌 때, 점 Q가 나타내는 도형 전체의 길이는 "
              "[[frac(b, a) pi]]이다. [[a + b]]의 값을 구하시오. (단, 점 Q는 점 A가 아니고, [[a]], [[b]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="11",
    figure=FIG("좌표공간: xy평면 위 원점 중심 원, 그 위쪽 z축 위에 중심 (0,0,2)인 구(꼭대기 점 A(0,0,3))"),
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 좌표공간 구·원",
    note="출처 [2007년 9월 고3 이과 23번]. P=(1,0,0)일 때 Q=(3/5,0,6/5) → 반지름 3/5인 원, 길이 6π/5 → a+b=11 (빠른정답 5와 불일치).")

# p28
add(id="f70c2ff8", qtype="choice",
    question=("두 점 A[[vcomp(-2, 3, -4)]], B[[vcomp(8, 8, 6)]]으로부터의 거리의 비가 [[ratio(3, 2)]]인 점들의 집합이 나타내는 도형을 [[S]]라 할 때, "
              "다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 도형 [[S]]의 겉넓이는 [[1296 pi]]이다,\n"
              "ㄴ. 도형 [[S]] 위의 점과 원점 O 사이의 거리의 최솟값은 15이다.\n"
              "ㄷ. 점 Q[[vcomp(16, 42, 14)]]의 위치에 전구가 켜져 있을 때, zx평면에 생기는 도형 [[S]]의 그림자의 둘레의 길이는 [[63 pi]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="아폴로니우스 구: 중심 (16,12,14), 반지름 18 → ㄱ 1296π ✓; 원점까지 최소 √596−18≈6.4 ㄴ✗; Q에서 y축 방향 거리 30, 그림자 원 반지름 63/2 → 둘레 63π ㄷ✓ → ③ (빠른정답 4와 불일치). ㄱ 끝의 쉼표는 원문 그대로.")

# p91 — [2021년 11월 고3 기하 30번/4점]
add(id="9efebff1", qtype="short",
    question=("좌표공간에 중심이 C[[vcomp(2, sqrt(5), 5)]]이고 점 P[[vcomp(0, 0, 1)]]을 지나는 구 [[S]]: [[pow(x - 2, 2) + pow(y - sqrt(5), 2) + pow(z - 5, 2) = 25]]가 있다. "
              "구 [[S]]가 평면 OPC와 만나서 생기는 원 위를 움직이는 점 Q, 구 [[S]] 위를 움직이는 점 R에 대하여 두 점 Q, R의 xy평면 위로의 정사영을 각각 "
              "[[sub(Q,1)]], [[sub(R,1)]]이라 하자. 삼각형 O[[sub(Q,1)]][[sub(R,1)]]의 넓이가 최대가 되도록 하는 두 점 Q, R에 대하여 삼각형 O[[sub(Q,1)]][[sub(R,1)]]의 "
              "평면 PQR 위로의 정사영의 넓이는 [[frac(q, p) sqrt(6)]] 이다. [[p + q]]의 값을 구하시오.\n"
              "(단, O는 원점이고 세 점 O, [[sub(Q,1)]], [[sub(R,1)]]은 한 직선 위에 있지 않으며, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="23",
    figure=FIG("좌표공간: z축 근처에 놓인 구(적도 원 점선), z축 위의 점 P(0,0,1), 원점 O"),
    difficulty_est=5, confidence=0.85,
    needs_review="첨자 점 라벨(Q₁, R₁, 삼각형 OQ₁R₁) 텍스트 혼합 / 도형 표현 불가: 좌표공간 구",
    note="출처 [2021년 11월 고3 기하 30번/4점]. 최대 넓이 20, cosθ=√6/3 → (20/3)√6 → 23 = 빠른정답 ✓.")

# p94 — [2021년 11월 고3 기하 30번 변형]
add(id="8edc5750", qtype="short",
    question=("좌표공간에 중심이 C[[vcomp(4, 3, 15)]]이고 점 P[[vcomp(0, 0, 3)]]을 지나는 구 [[S]]: [[pow(x - 4, 2) + pow(y - 3, 2) + pow(z - 15, 2) = 169]]가 있다. "
              "구 [[S]]가 평면 OPC와 만나서 생기는 원 위를 움직이는 점 Q, 구 [[S]] 위를 움직이는 점 R에 대하여 두 점 Q, R의 xy평면 위로의 정사영을 각각 "
              "[[sub(Q,1)]], [[sub(R,1)]]이라 하자. 삼각형 O[[sub(Q,1)]][[sub(R,1)]]의 넓이가 최대가 되도록 하는 두 점 Q, R에 대하여 삼각형 O[[sub(Q,1)]][[sub(R,1)]]의 "
              "평면 PQR 위로의 정사영의 넓이는 [[frac(q, p) sqrt(17)]] 이다. [[p + q]]의 값을 구하시오.\n"
              "(단, O는 원점이고 세 점 O, [[sub(Q,1)]], [[sub(R,1)]]은 한 직선 위에 있지 않으며, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="368",
    figure=FIG("좌표공간: z축 근처에 놓인 큰 구(적도 원 점선), z축 위의 점 P(0,0,3), 원점 O"),
    difficulty_est=5, confidence=0.75,
    needs_review="첨자 점 라벨(Q₁, R₁, 삼각형 OQ₁R₁) 텍스트 혼합 / 도형 표현 불가: 좌표공간 구",
    note="출처 [2021년 11월 고3 기하 30번 변형]. 최대 넓이 (1/2)·18·13=117, 평면 PQR 법선 (−2,−14,15) → cosθ=3/√17 → 351√17/17 → p+q=368 (빠른정답 23은 원문항 답, 불일치).")

# ───────────────────────── 평면과 구의 방정식 ─────────────────────────
# p29
add(id="821193ce", qtype="short",
    question=("좌표공간에 세 점 A[[vcomp(3, 0, 0)]], B[[vcomp(0, 6, 0)]], C[[vcomp(0, 0, 3)]]과 직선 [[l]]: [[frac(x - 3, 3) = frac(y - 6, b) = frac(z - 3, 3)]] 이 있다. "
              "직선 [[l]]이 삼각형 ABC의 내부와 그 둘레를 지날 때, 모든 자연수 [[b]]의 값의 합을 구하시오."),
    choices=None, derived_answer="78", figure=None, difficulty_est=3, confidence=0.9,
    note="교점 (3−36/(12+b), 6−12b/(12+b), 3−36/(12+b)) ≥ 0 ⇔ b ≤ 12 → 1+…+12 = 78 = 빠른정답 ✓. 3차원 좌표는 vcomp로 표기.")

# p86 — [2015년 9월 고3 이과 29번/4점]
add(id="acd22ec0", qtype="short",
    question=("좌표공간에 두개의 구\n[[sub(S,1)]]: [[pow(x,2) + pow(y,2) + pow(z - 3, 2) = 1]],\n[[sub(S,2)]]: [[pow(x,2) + pow(y,2) + pow(z + 3, 2) = 4]]\n"
              "가 있다. 점 P[[vcomp(frac(1,2), frac(sqrt(3), 6), 0)]]을 포함하고 [[sub(S,1)]]과 [[sub(S,2)]]에 동시에 접하는 평면을 [[alpha]]라 하자. "
              "점 Q[[vcomp(k, -sqrt(3), 2)]]가 평면 [[alpha]] 위의 점일 때 [[120k]]의 값을 구하시오."),
    choices=None, derived_answer="40",
    figure=FIG("좌표공간: z축 위에 놓인 두 구(위쪽 작은 구 중심 (0,0,3), 아래쪽 큰 구 중심 (0,0,−3)), 원점 O"),
    difficulty_est=4, confidence=0.85,
    needs_review="도형 표현 불가: 좌표공간 두 구",
    note="출처 [2015년 9월 고3 이과 29번/4점]. 접평면 3x+√3y+2z−2=0 → k=1/3 → 120k=40 (빠른정답 4와 불일치, '40'의 절단 의심).")

# p87 — [2008년 11월 고3 이과 25번]
add(id="cf144578", qtype="short",
    question=("좌표공간에서 구 [[S]]: [[pow(x,2) + pow(y,2) + pow(z,2) = 4]]와 평면 [[alpha]]: [[y - sqrt(3) z = 2]] 가 만나서 생기는 원을 [[C]]라 하자. "
              "원 [[C]] 위의 점 A[[vcomp(0, 2, 0)]]에 대하여 원 [[C]]의 지름의 양 끝점 P, Q를 [[seg(AP) = seg(AQ)]]가 되도록 잡고, "
              "점 P를 지나고 평면 [[alpha]]에 수직인 직선이 구 [[S]]와 만나는 또 다른 점을 R라 하자. 삼각형 ARQ의 넓이를 [[s]]라 할 때, [[pow(s,2)]]의 값을 구하시오."),
    choices=None, derived_answer="15",
    figure=FIG("구 S와 평면 α의 교선 원 C(점선), 원 위의 점 A·P·Q(PQ 지름), P에서 α에 수직인 직선이 구와 만나는 점 R, 삼각형 ARQ 점선"),
    difficulty_est=4, confidence=0.85,
    needs_review="도형 표현 불가: 구·평면 교선 입체도",
    note="출처 [2008년 11월 고3 이과 25번]. 원 C 반지름 √3, PR=2 ⊥ α → 넓이² = 60/4 = 15 = 빠른정답 ✓.")

# p89
add(id="6ca5f223", qtype="choice",
    question=("직선 [[frac(x - 2, 3) = 10 - y = frac(z - 2, 4)]] 와 평면 [[x + 2y + 3z = 2]]의 교점을 A라 할 때, "
              "[[dot(vec(OP), vec(OA)) = pow(abs(vec(OP)), 2)]]을 만족시키는 점 P가 나타내는 도형과 평면 [[x + 2y - z = 1]]이 만나서 생기는 도형의 둘레의 길이는? "
              "(단, O는 원점이다.)"),
    choices=["[[2 sqrt(13) pi]]", "[[8 pi]]", "[[2 sqrt(19) pi]]", "[[2 sqrt(22) pi]]", "[[10 pi]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="A=(−4,12,−6); 구: 중심 (−2,6,−3), 반지름 7; 평면까지 거리 2√6 → 원 반지름 5 → 10π → ⑤ = 빠른정답 ✓.")

# p97 — [2013년 11월 고3 이과 29번/4점]
add(id="f2ca4aba", qtype="short",
    question=("좌표공간에서 구 [[pow(x,2) + pow(y,2) + pow(z,2) = 4]] 위를 움직이는 두 점 P, Q가 있다. 두 점 P, Q에서 평면 [[y = 4]]에 내린 수선의 발을 각각 "
              "[[sub(P,1)]], [[sub(Q,1)]]이라 하고, 평면 [[y + sqrt(3) z + 8 = 0]]에 내린 수선의 발을 각각 [[sub(P,2)]], [[sub(Q,2)]]라 하자. "
              "[[2 pow(abs(vec(PQ)), 2) - pow(abs(sub(vec(PQ), 1)), 2) - pow(abs(sub(vec(PQ), 2)), 2)]]의 최댓값을 구하시오."),
    choices=None, derived_answer="24",
    figure=FIG("구 위의 두 점 P, Q와 벡터 PQ→; 평면 y=4 위의 정사영 P₁, Q₁과 벡터 P₁Q₁→; 평면 y+√3z+8=0 위의 정사영 P₂, Q₂와 벡터 P₂Q₂→"),
    difficulty_est=4, confidence=0.85,
    needs_review="첨자 점 라벨 벡터(P₁Q₁→, P₂Q₂→)를 sub(vec(PQ),1)로 우회 / 도형 표현 불가: 구·두 평면 입체도",
    note="출처 [2013년 11월 고3 이과 29번/4점]. 식 = (v·n₁)²+(v·n₂)², 최대 고윳값 3/2 × 16 = 24 = 빠른정답 ✓.")

# ───────────────────────── 포물선 ─────────────────────────
# p34 — [2014년 6월 고3 이과 28번/4점]
add(id="3971dd4c", qtype="short",
    question=("좌표평면에서 포물선 [[sub(C,1)]]: [[pow(x,2) = 4y]]의 초점을 [[sub(F,1)]], 포물선 [[sub(C,2)]]: [[pow(y,2) = 8x]]의 초점을 [[sub(F,2)]]라 하자. "
              "점 P는 다음 조건을 만족시킨다.\n"
              "(가) 중심이 [[sub(C,1)]] 위에 있고 점 [[sub(F,1)]]을 지나는 원과 중심이 [[sub(C,2)]] 위에 있고 점 [[sub(F,2)]]를 지나는 원의 교점이다.\n"
              "(나) 제3사분면에 있는 점이다.\n"
              "원점 O에 대하여 [[pow(seg(OP), 2)]]의 최댓값을 구하시오."),
    choices=None, derived_answer="5",
    figure=FIG("좌표평면: 두 포물선 x²=4y, y²=8x와 초점 F₁(y축), F₂(x축), 각 포물선 위에 중심을 둔 두 원, 제3사분면의 교점 P"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 포물선·원 복합 좌표평면",
    note="출처 [2014년 6월 고3 이과 28번/4점]. 각 원은 준선 y=−1, x=−2에 접하므로 P는 x≥−2, y≥−1 → 최대 OP²=5 (P(−2,−1)) (빠른정답 25와 불일치).")

# p36
add(id="9af11f85", qtype="short",
    question=("좌표평면에서 포물선 [[sub(C,1)]]: [[pow(x,2) = 16y]]의 초점을 [[sub(F,1)]], 포물선 [[sub(C,2)]]: [[pow(y,2) = 8x]]의 초점을 [[sub(F,2)]]라 하자. "
              "점 P는 다음 조건을 만족한다.\n"
              "(가) 중심이 [[sub(C,1)]] 위에 있고 점 [[sub(F,1)]]을 지나는 원과 중심이 [[sub(C,2)]] 위에 있고 점 [[sub(F,2)]]를 지나는 원의 교점이다.\n"
              "(나) 제3사분면에 있는 점이다.\n"
              "원점 O에 대하여 [[pow(seg(OP), 2)]]의 최댓값을 구하시오."),
    choices=None, derived_answer="20",
    figure=FIG("좌표평면: 두 포물선 x²=16y, y²=8x와 초점 F₁, F₂, 각 포물선 위에 중심을 둔 두 원, 제3사분면의 교점 P"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 포물선·원 복합 좌표평면",
    note="준선 y=−4, x=−2 → P(−2,−4)에서 최대 OP²=20 (빠른정답 없음).")

# p38 (id 2개) — [2022년 3월 고3 기하 30번 변형]
dup(["48c30ebc", "3caa758b"], qtype="short",
    question=("다음 그림과 같이 꼭짓점이 [[sub(A,1)]]이고 초점이 [[sub(F,1)]]인 포물선 [[sub(P,1)]]과 꼭짓점이 [[sub(A,2)]]이고 초점이 [[sub(F,2)]]인 포물선 [[sub(P,2)]]가 있다. "
              "두 포물선의 준선은 모두 직선 [[sub(F,1)]][[sub(F,2)]]와 평행하고, 두 선분 [[sub(A,1)]][[sub(A,2)]], [[sub(F,1)]][[sub(F,2)]]의 중점은 서로 일치한다. "
              "두 포물선 [[sub(P,1)]], [[sub(P,2)]]가 서로 다른 두 점에서 만날 때 두 점 중에서 점 [[sub(A,2)]]에 가까운 점을 B라 하자. "
              "포물선 [[sub(P,1)]]이 직선 [[sub(F,1)]][[sub(F,2)]]와 만나는 점을 C라 할 때, 두 점 B, C가 다음 조건을 모두 만족시킨다.\n"
              "(가) [[sub(A,1)]]C = [[sqrt(5)]]\n"
              "(나) 2 · [[sub(F,1)]]B − [[sub(F,2)]]B = [[frac(11, 4)]]\n"
              "삼각형 B[[sub(F,2)]][[sub(F,1)]]의 넓이가 [[frac(sqrt(a) - sqrt(b), 8)]] 일 때, [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="15",
    figure=FIG("세로 직선 F₁F₂(F₁ 아래, F₂ 위) 위에 두 초점, 왼쪽으로 열린 포물선 P₂(꼭짓점 A₂ 오른쪽)와 오른쪽으로 열린 포물선 P₁(꼭짓점 A₁ 왼쪽)이 교차, 위쪽 교점 B, P₁과 직선 F₁F₂의 교점 C, 선분 BF₁"),
    difficulty_est=5, confidence=0.75,
    needs_review="첨자 점 라벨(A₁C, F₁B, 삼각형 BF₂F₁ 등) 텍스트 혼합 / 도형 표현 불가: 두 포물선",
    note="출처 [2022년 3월 고3 기하 30번 변형]. 초점거리 u=1, x_B=1/4, 넓이 v/4=(√5−√3)/8 → a=5, b=3 → ab=15 (빠른정답 '1 36'과 불일치).")

# ───────────────────────── 정사영 ─────────────────────────
# p42 — [2021년 10월 고3 기하 30번 변형]
add(id="e5f1c833", qtype="short",
    question=("한 변의 길이가 8인 정삼각형 ABC를 한 면으로 하는 사면체 ABCD의 꼭짓점 A에서 평면 BCD에 내린 수선의 발을 H라 할 때, "
              "점 H는 삼각형 BCD의 내부에 놓여 있다. 직선 DH가 선분 BC와 만나는 점을 E라 할 때, 점 E가 다음 조건을 만족시킨다.\n"
              "(가) [[angle(AEH) = angle(DAH)]]\n"
              "(나) 점 E는 선분 CD를 지름으로 하는 원 위의 점이고 [[seg(DE) = 12]]이다.\n"
              "삼각형 AEH의 평면 ABD 위로의 정사영의 넓이는 [[p sqrt(q)]] 이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 자연수이다.)"),
    choices=None, derived_answer="10",
    figure=FIG("사면체 ABCD: 꼭짓점 A에서 밑면 BCD에 내린 수선의 발 H(직각 표시), 점선 BD"),
    difficulty_est=5, confidence=0.75,
    needs_review="도형 표현 불가: 사면체",
    note="출처 [2021년 10월 고3 기하 30번 변형]. DE⊥BC, E=BC 중점, EH=4, AH=4√2, △AEH=8√2, 평면 ADE와 ABD의 각 cos=√3/2 → 4√6 → 10 (빠른정답 4와 불일치).")

# p44 — [2023년 7월 고3 기하 30번/4점]
add(id="f9d440ac", qtype="short",
    question=("공간에 중심이 O이고 반지름의 길이가 4인 구가 있다. 구 위의 서로 다른 세 점 A, B, C가 [[seg(AB) = 8]], [[seg(BC) = 2 sqrt(2)]] 를 만족시킨다. "
              "평면 ABC 위에 있지 않은 구 위의 점 D에서 평면 ABC에 내린 수선의 발을 H라 할 때, 점 D가 다음 조건을 만족시킨다.\n"
              "(가) 두 직선 OC, OD가 서로 수직이다.\n"
              "(나) 두 직선 AD, OH가 서로 수직이다.\n"
              "삼각형 DAH의 평면 DOC 위로의 정사영의 넓이를 [[S]]라 할 때, [[8S]]의 값을 구하시오. (단, 점 H는 점 O가 아니다.)"),
    choices=None, derived_answer="36",
    figure=FIG("구(중심 O): 지름 AB, 구 위의 점 C, D, D에서 평면 ABC에 내린 수선의 발 H(직각 표시), 선분 DA·DO·OC·BC"),
    difficulty_est=5, confidence=0.85,
    needs_review="도형 표현 불가: 구 위 사면체",
    note="출처 [2023년 7월 고3 기하 30번/4점]. 기출 정답 36 = 빠른정답 ✓.")

# p47 — [2022년 7월 고3 기하 30번 변형]
add(id="757b83b0", qtype="short",
    question=("공간에서 중심이 O이고 반지름의 길이가 2인 구와 점 O를 지나는 평면 [[alpha]]가 있다. 평면 [[alpha]]와 구가 만나서 생기는 원 위의 서로 다른 세 점 A, B, C에 대하여 "
              "두 직선 OA, BC가 서로 수직일 때, 구 위의 점 P가 다음 조건을 만족시킨다.\n"
              "(가) [[angle(PAO) = frac(pi, 4)]]\n"
              "(나) 점 P의 평면 [[alpha]] 위로의 정사영은 선분 OA 위에 있다.\n"
              "[[cos(angle(PAB)) = frac(sqrt(6), 4)]] 일 때, 삼각형 PAB의 평면 PAC 위로의 정사영의 넓이를 [[S]]라 하자. [[5 pow(S,2)]]의 값을 구하시오. "
              "(단, [[0 < angle(BAC) < frac(pi, 2)]])"),
    choices=None, derived_answer="3",
    figure=FIG("구와 중심 O를 지나는 평면 α(대원 점선), 대원 위의 점 A, B, C, 구 꼭대기 근처의 점 P, 선분 PA·PB·PC·AB·AC"),
    difficulty_est=5, confidence=0.85,
    needs_review="도형 표현 불가: 구·평면 입체도",
    note="출처 [2022년 7월 고3 기하 30번 변형]. P=(0,0,2), B=(−1,−√3,0), C=(−1,√3,0) → △PAB=√15, cosθ=1/5 → S=√15/5 → 5S²=3 = 빠른정답 ✓.")

# p58 — [2026년 7월 고3 기하 30번 변형]
_p58_head = ("공간에 [[seg(AB) = 10 sqrt(5)]] 인 선분 AB를 지름으로 하는 구 [[S]]가 있다. 구 [[S]] 위의 두 점 C, D에 대하여 네 점 A, B, C, D는 평면 [[alpha]] 위에 있고, "
             "[[seg(AD) = seg(BC) = 10]]이다. 구 [[S]] 위의 점 P가 다음 조건을 만족시킨다.\n"
             "(가) 점 P의 평면 [[alpha]] 위로의 정사영은 선분 BD 위에 있다.\n")
_p58_tail = ("평면 PAB와 평면 PBC가 이루는 예각의 크기를 [[theta]]라 할 때, [[pow(cos(theta), 2) = frac(q, p)]]이다. [[p + q]]의 값을 구하시오.\n"
             "(단, [[seg(CD) < seg(AB)]]이고, [[p]]와 [[q]]는 서로소인 자연수이다.)")
_p58_fig = FIG("구 S(적도 대원 위에 A, B, C, D), 구 위쪽의 점 P, 사면체 P-ABC·P-ABD 면 음영, 점선 PD·AD·DC")
add(id="98622425", qtype="short",
    question=_p58_head + "(나) 평면 PAD와 평면 [[alpha]]가 이루는 예각의 크기는 [[frac(pi, 3)]] 이다.\n" + _p58_tail,
    choices=None, derived_answer="27", figure=_p58_fig, difficulty_est=5, confidence=0.8,
    needs_review="도형 표현 불가: 구 위 사면체",
    note="출처 [2026년 7월 고3 기하 30번 변형]. H=(−√5,3√5,0), P 높이 5√3 → cos²θ=1/26 → 27 = 빠른정답 ✓.")

# p65 — [2024년 7월 고3 기하 30번 변형]
_p65_body = ("공간에 점 P를 포함하는 평면 [[alpha]]가 있다. 평면 [[alpha]] 위에 있지 않은 서로 다른 두 점 A, B의 평면 [[alpha]] 위로의 정사영을 각각 A′, B′이라 할 때, ")
_p65_fig = FIG("평면 α 위의 점 P, A′, B′, M(PB′의 중점); α 위쪽의 점 A(A′ 바로 위), B(B′ 바로 위); 선분 AB·AP·AB′·BM, 직각 표시")
add(id="dec5e075", qtype="short",
    question=(_p65_body + "[[seg(AA)]]′ = [[6]], A′P = A′B′ = [[3]], [[seg(PB)]]′ = [[4]]이다.\n"
              "선분 PB′의 중점 M에 대하여 [[angle(MAB) = frac(pi, 2)]] 일 때, 직선 BM과 평면 APB′이 이루는 예각의 크기를 [[theta]]라 하자.\n"
              "[[pow(tan(theta), 2) = frac(q, p)]] 일 때, [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="365", figure=_p65_fig, difficulty_est=5, confidence=0.75,
    needs_review="프라임 라벨(A′, B′, 선분 AA′·A′P·A′B′·PB′) 텍스트 혼합 / 도형 표현 불가: 정사영 입체도",
    note="출처 [2024년 7월 고3 기하 30번 변형]. B의 높이 41/6, sin²θ=41/365 → tan²θ=41/324 → 365 = 빠른정답 ✓.")

# p66 — [2024년 7월 고3 기하 30번/4점]
add(id="ed0f5ab8", qtype="short",
    question=(_p65_body + "[[seg(AA)]]′ = [[9]], A′P = A′B′ = [[5]], [[seg(PB)]]′ = [[8]]이다. 선분 PB′의 중점 M에 대하여 "
              "[[angle(MAB) = frac(pi, 2)]] 일 때, 직선 BM과 평면 APB′이 이루는 예각의 크기를 [[theta]]라 하자. "
              "[[pow(cos(theta), 2) = frac(q, p)]] 일 때, [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="111", figure=_p65_fig, difficulty_est=5, confidence=0.8,
    needs_review="프라임 라벨(A′, B′, 선분 AA′·A′P·A′B′·PB′) 텍스트 혼합 / 도형 표현 불가: 정사영 입체도",
    note="출처 [2024년 7월 고3 기하 30번/4점]. B의 높이 10, sin²θ=5/58 → cos²θ=53/58 → 111 = 빠른정답 ✓.")

# p68 — [2026년 7월 고3 기하 30번/4점]
add(id="92ecef41", qtype="short",
    question=_p58_head + "(나) 평면 PAD와 평면 [[alpha]]가 이루는 예각의 크기는 [[frac(pi, 4)]] 이다.\n" + _p58_tail,
    choices=None, derived_answer="52", figure=_p58_fig, difficulty_est=5, confidence=0.75,
    needs_review="도형 표현 불가: 구 위 사면체",
    note="출처 [2026년 7월 고3 기하 30번/4점]. H=(√5,2√5,0), P 높이 10 → cos²θ=1/51 → 52 (빠른정답 5와 불일치, '52'의 절단 의심).")

# p86 — [2011년 11월 고3 이과 29번/4점]
add(id="25452c7e", qtype="short",
    question=("그림과 같이 밑면의 반지름의 길이가 7인 원기둥과 밑면의 반지름의 길이가 5이고 높이가 12인 원뿔이 평면 [[alpha]]위에 놓여 있고, "
              "원뿔의 밑면의 둘레가 원기둥의 밑면의 둘레에 내접한다. 평면 [[alpha]]와 만나는 원기둥의 밑면의 중심을 O, 원뿔의 꼭짓점을 A라 하자. "
              "중심이 B이고 반지름의 길이가 4인 구 [[S]]가 다음 조건을 만족시킨다.\n"
              "(가) 구 [[S]]는 원기둥과 원뿔에 모두 접한다.\n"
              "(나) 두 점 A,B의 평면 [[alpha]] 위로의 정사영이 각각 A′, B′일 때, ∠A′OB′ = [[deg(180)]]이다.\n"
              "직선 AB와 평면 [[alpha]]가 이루는 예각의 크기를 [[theta]]라 할 때, [[tan(theta) = p]]이다. [[100p]]의 값을 구하시오. "
              "(단, 원뿔의 밑면의 중심과 점 A′은 일치한다.)"),
    choices=None, derived_answer="34",
    figure=FIG("평면 α 위의 원기둥 안에 원뿔(밑면이 원기둥 밑면에 내접)과 구가 놓인 입체도"),
    difficulty_est=4, confidence=0.85,
    needs_review="프라임 라벨(A′, B′, ∠A′OB′) 텍스트 혼합 / 도형 표현 불가: 원기둥·원뿔·구 입체도",
    note="출처 [2011년 11월 고3 이과 29번/4점]. 기출 정답 34 = 빠른정답 ✓.")

# ───────────────────────── 이차곡선 ─────────────────────────
# p3 — [2026년 3월 고3 기하 30번/4점]
add(id="7027d1b6", qtype="short",
    question=("다음 그림과 같이 두 점 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 2 pow(a,2)) = 1]]이 있다. "
              "이 쌍곡선의 꼭짓점 중 [[x]]좌표가 음수인 점을 A라 하고, 점 F′을 지나고 [[x]]축에 수직인 직선이 이 쌍곡선과 만나는 점 중 제2사분면에 있는 점을 P라 하자. "
              "점 A에서 선분 PF에 내린 수선의 발을 H라 하자. 두 점 A, F를 초점으로 하고 점 H를 지나는 타원이 이 쌍곡선과 만나는 점 중 제4사분면에 있는 점을 Q라 하자.\n"
              "[[seg(AQ)]] + F′Q = [[6 + 8 sqrt(3)]] 일 때, 이 타원의 장축의 길이는 [[p + q sqrt(3)]] 이다. [[pow(p,2) + pow(q,2)]]의 값을 구하시오.\n"
              "(단, [[a]]는 양수이고, [[p]]와 [[q]]는 유리수이다.)"),
    choices=None, derived_answer="52",
    figure=FIG("좌표평면: 쌍곡선 x²/a²−y²/(2a²)=1, 초점 F′·F, 꼭짓점 A, F′ 위의 점 P, 선분 PF와 A에서 내린 수선의 발 H(직각), 초점 A·F인 타원, 제4사분면 교점 Q, 선분 AQ·F′Q"),
    difficulty_est=5, confidence=0.8,
    needs_review="프라임 라벨(F′, 선분 F′Q) 텍스트 혼합 / 도형 표현 불가: 쌍곡선·타원 복합",
    note="출처 [2026년 3월 고3 기하 30번/4점]. AH=a(√3+1)/2, HF=a(3+√3)/2 → 장축 a(2+√3); a(4+√3)=6+8√3 → a=2√3 → 6+4√3 → 52 = 빠른정답 ✓.")

# p22 — [2023년 3월 고3 기하 30번/4점]
_p22_body = ("두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 타원 [[C]]가 있다. 타원 [[C]]가 두 직선 [[x = c]], [[x = -c]]와 만나는 점 중 [[y]]좌표가 양수인 점을 각각 A, B라 하자. "
             "두 초점이 A, B이고 점 F를 지나는 쌍곡선이 직선 [[x = c]]와 만나는 점 중 F가 아닌 점을 P라 하고, 이 쌍곡선이 두 직선 BF, BP와 만나는 점 중 [[x]]좌표가 음수인 점을 각각 Q, R라 하자. "
             "세 점 P, Q, R가 다음 조건을 만족시킨다.\n")
_p22_fig = FIG("좌표평면: 초점 F′·F인 타원 C, x=c 위의 점 A와 P, x=−c 위의 점 B, 초점 A·B인 쌍곡선, 직선 BF·BP와 쌍곡선의 교점 Q, R")
add(id="d2b82d64", qtype="short",
    question=("그림과 같이 " + _p22_body +
              "(가) 삼각형 BFP는 정삼각형이다.\n"
              "(나) 타원 [[C]]의 장축의 길이와 삼각형 BQR의 둘레의 길이의 차는 3이다.\n"
              "[[60 seg(AF)]]의 값을 구하시오."),
    choices=None, derived_answer="100", figure=_p22_fig, difficulty_est=5, confidence=0.85,
    needs_review="프라임 라벨(F′) 텍스트 혼합 / 도형 표현 불가: 타원·쌍곡선 복합",
    note="출처 [2023년 3월 고3 기하 30번/4점]. AF=m, 둘레 6m/5, 장축 3m, 차 9m/5=3 → m=5/3 → 100 = 빠른정답 ✓.")

# p36 — [2023년 3월 고3 기하 30번 변형]
add(id="3ea80e15", qtype="short",
    question=("아래 그림과 같이 " + _p22_body +
              "(가) 삼각형 BFP는 [[seg(BF) = seg(BP)]]이고, [[seg(BF) = frac(3, 4) seg(PF)]] 인 이등변삼각형이다.\n"
              "(나) 타원 [[C]]의 장축의 길이와 삼각형 BQR의 둘레의 길이의 차는 [[frac(5, 2)]] 이다.\n"
              "[[15 seg(AF)]]의 값을 구하시오."),
    choices=None, derived_answer="30", figure=_p22_fig, difficulty_est=5, confidence=0.75,
    needs_review="프라임 라벨(F′) 텍스트 혼합 / 도형 표현 불가: 타원·쌍곡선 복합",
    note="출처 [2023년 3월 고3 기하 30번 변형]. AF=m일 때 BF=3m/2, 2a_h=m/2, 둘레 5m/4, 장축 5m/2, 차 5m/4=5/2 → m=2 → 15AF=30 (빠른정답 207과 불일치).")

# p41
_p41_cond = ("점 A가 다음 조건을 만족할 때, 선분 AF의 길이를 구하시오. (단, [[a]]는 양수이다.)\n"
             "(가) [[seg(AF)]]′ − [[seg(AF)]] = [[2a]]\n"
             "(나) 점 A의 [[x]]좌표는 점 F의 [[x]]좌표보다 작다.\n")
add(id="1c760caf", qtype="short",
    question=("두 초점 F, F′이 [[y]]축에 대하여 대칭이고, 직선 [[y = 4 sqrt(3) x]]가 한 점근선인 쌍곡선이 포물선 [[pow(y,2) = 36a(x + 2a)]]와 만나는 점 중 "
              "제1사분면에 있는 점을 A라 하자. " + _p41_cond + "(다) 삼각형 AF′F의 넓이는 84이다."),
    choices=None, derived_answer="13", figure=None, difficulty_est=4, confidence=0.85,
    needs_review="프라임 라벨(F′, 선분 AF′, 삼각형 AF′F) 텍스트 혼합",
    note="c=7a가 포물선의 초점; A=(2a,12a), 넓이 (1/2)·14a·12a=84a²=84 → a=1 → AF=x_A+11a=13 = 빠른정답 ✓.")

# p42
add(id="7bb671ba", qtype="short",
    question=("두 초점 F, F′이 [[y]]축에 대하여 대칭이고, 직선 [[y = 2 sqrt(2) x]]가 한 점근선인 쌍곡선이 포물선 [[pow(y,2) = 12 a x]]와 만나는 점 중 "
              "제1사분면에 있는 점을 A라 하자. " + _p41_cond + "(다) 삼각형 AF′F의 넓이는 [[6 sqrt(6)]] 이다."),
    choices=None, derived_answer="5", figure=None, difficulty_est=4, confidence=0.85,
    needs_review="프라임 라벨(F′, 선분 AF′, 삼각형 AF′F) 텍스트 혼합",
    note="c=3a가 포물선의 초점; A=(2a,2√6a), 넓이 6√6a²=6√6 → a=1 → AF=x_A+3a=5 (빠른정답 4와 불일치).")

# p43
add(id="04febd1f", qtype="short",
    question=("두 초점 F, F′이 [[y]]축에 대하여 대칭이고, 직선 [[y = 2 sqrt(6) x]]가 한 점근선인 쌍곡선이 포물선 [[pow(y,2) = 24a(x + a)]]와 만나는 점 중 "
              "제1사분면에 있는 점을 A라 하자. " + _p41_cond + "(다) 삼각형 AF′F의 넓이는 [[30 sqrt(2)]] 이다."),
    choices=None, derived_answer="9", figure=None, difficulty_est=4, confidence=0.85,
    needs_review="프라임 라벨(F′, 선분 AF′, 삼각형 AF′F) 텍스트 혼합",
    note="c=5a가 포물선의 초점; A=(2a,6√2a), 넓이 30√2a²=30√2 → a=1 → AF=x_A+7a=9 (빠른정답 4와 불일치).")

# ───────────────────────── 벡터의 덧셈과 뺄셈 ─────────────────────────
# p18
add(id="427838c0", qtype="choice",
    question=("다음 그림과 같이 길이가 4인 선분 AB를 지름으로 하는 원과 이 원에 내접하는 정삼각형 ACD가 있다. "
              "선분 AB와 선분 CD의 교점을 E라 할 때, 변 AD 위의 점 P에 대하여 [[abs(vec(CP) + vec(EB))]] 의 최솟값은?"),
    choices=["[[frac(3, 2)]]", "[[2]]", "[[frac(5, 2)]]", "[[3]]", "[[frac(7, 2)]]"],
    derived_answer="③",
    figure=FIG("지름 AB인 원에 내접한 정삼각형 ACD(D 위, C 아래), AB와 CD의 교점 E, 변 AD 위의 점 P, 화살표 C→P와 E→B"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원·정삼각형·벡터",
    note="A(−2,0), C(1,−√3), D(1,√3), E(1,0); CP+EB = P−(0,−√3) → 점 (0,−√3)에서 직선 AD까지 거리 5/2 → ③ (빠른정답 2와 불일치).")

# p21
_p21_body = ("인 직사각형 ABCD와 선분 AD를 지름으로 하는 원이 있다. 이 원 위의 점 P에 대하여 [[abs(vec(AB) + vec(AP))]] 의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, "
             "[[M m]]의 값을 구하시오.")
add(id="a0387006", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = 9]], [[seg(AD) = 6]]" + _p21_body,
    choices=None, derived_answer="81",
    figure=FIG("직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상)와 AD를 지름으로 하는 원(위쪽), 원 위의 점 P, 화살표 A→P, 치수 9(AB), 6(AD)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형·원·벡터",
    note="AB+AP = P−(0,9)(A 원점, B=(0,−9)); 원 중심 (3,0) 반지름 3, 중심까지 3√10 → Mm=90−9=81 (빠른정답 3과 불일치).")

# p22
add(id="4a0a9cc8", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = 10]], [[seg(AD) = 8]]" + _p21_body,
    choices=None, derived_answer="100",
    figure=FIG("직사각형 ABCD와 AD를 지름으로 하는 원(위쪽), 원 위의 점 P, 화살표 A→P, 치수 10(AB), 8(AD)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형·원·벡터",
    note="원 중심 (4,0) 반지름 4, (0,10)까지 √116 → Mm=116−16=100 (빠른정답 2와 불일치).")

# p23
add(id="673b249e", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = 7]], [[seg(AD) = 4]]" + _p21_body,
    choices=None, derived_answer="49",
    figure=FIG("직사각형 ABCD와 AD를 지름으로 하는 원(위쪽), 원 위의 점 P, 화살표 A→P, 치수 7(AB), 4(AD)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형·원·벡터",
    note="원 중심 (2,0) 반지름 2, (0,7)까지 √53 → Mm=53−4=49 = 빠른정답 ✓.")

# ───────────────────────── 타원 ─────────────────────────
# p60
_p60_body = ("을 초점으로 하는 타원 위의 서로 다른 두 점 P, Q에 대하여 원점 O에서 선분 PF와 선분 QF′에 내린 수선의 발을 각각 H와 I라 하자. "
             "점 H와 점 I가 각각 선분 PF와 선분 QF′의 중점이고, ")
_p60_tail = ("일 때, 이 타원의 장축의 길이를 [[l]]이라 하자. [[pow(l,2)]]의 값을 구하시오. (단, [[seg(OH) != seg(OI)]])")
_p60_fig = FIG("좌표평면 위 타원과 초점 F′·F, 제1사분면의 점 P와 선분 PF 위의 중점 H(OH⊥PF 직각), 제4사분면의 점 Q와 선분 QF′ 위의 중점 I(OI⊥QF′ 직각), 같은 길이 표시")
add(id="75364b1c", qtype="short",
    question="두 점 F[[point(4, 0)]], F′[[point(-4, 0)]]" + _p60_body + "[[dot(seg(OH), seg(OI)) = 12]]" + _p60_tail,
    choices=None, derived_answer="160", figure=_p60_fig, difficulty_est=4, confidence=0.65,
    needs_review="프라임 라벨(F′, 선분 QF′) 텍스트 혼합 / 도형 표현 불가: 타원·수선 / 문항 결함 의심",
    note="OP=OF=4 → ∠FPF′=90°, OH=PF′/2, OI=QF/2 → PF′·QF=48, l²=4c²+2·48=160 (출제 의도 추정). 그러나 PF²+PF′²=64와 곱 48은 양립 불가(판별식 음수) — 빠른정답 26과도 불일치.")

# p61
add(id="87aedd07", qtype="short",
    question="두 점 F[[point(6, 0)]], F′[[point(-6, 0)]]" + _p60_body + "[[dot(seg(OH), seg(OI)) = 14]]" + _p60_tail,
    choices=None, derived_answer="256", figure=_p60_fig, difficulty_est=4, confidence=0.8,
    needs_review="프라임 라벨(F′, 선분 QF′) 텍스트 혼합 / 도형 표현 불가: 타원·수선",
    note="OP=OF=6 → ∠FPF′=90°, OH=PF′/2, OI=QF/2 → PF′·QF=56 → l²=144+112=256 = 빠른정답 ✓.")

# p64 — [2026년 6월 고3 기하 28번/4점]
_p64_body = ("두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]]([[c > 0]])인 타원 [[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), pow(b,2)) = 1]]이 있다. "
             "이 타원 위에 있는 제1사분면 위의 점 P와 이 타원 위에 있는 제4사분면 위의 점 Q에 대하여 점 F가 선분 PQ 위에 있고 ")
_p64_fig = FIG("좌표평면 위 타원, 초점 F′·F, 제1사분면의 점 P와 제4사분면의 점 Q를 잇는 선분 PQ가 F를 지남, 선분 F′Q")
add(id="980cff30", qtype="choice",
    question=(_p64_body + "[[frac(seg(PF), seg(QF)) = frac(1, 2)]], [[frac(seg(PF), seg(FF))]]′ = [[frac(sqrt(6), 16)]] 이다. "
              "삼각형 FF′Q의 넓이가 [[4 sqrt(5)]] 일 때, [[pow(b,2)]]의 값은? (단, [[a]]와 [[b]]는 양수이다.)"),
    choices=["[[frac(13, 2)]]", "[[7]]", "[[frac(15, 2)]]", "[[8]]", "[[frac(17, 2)]]"],
    derived_answer="④", figure=_p64_fig, difficulty_est=4, confidence=0.75,
    needs_review="프라임 라벨(F′, 선분 FF′, 삼각형 FF′Q) 텍스트 혼합 / 도형 표현 불가: 타원",
    note="출처 [2026년 6월 고3 기하 28번/4점]. PF=k, c=(4√6/3)k → a=4k, b²=16k²/3, 넓이 (8√5/3)k²=4√5 → k²=3/2 → b²=8 → ④ (빠른정답 256과 불일치).")

# p71 — [2021년 4월 고3 기하 30번/4점]
add(id="05fb5120", qtype="short",
    question=("그림과 같이 두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 타원 [[frac(pow(x,2), 16) + frac(pow(y,2), 7) = 1]] 위의 점 P에 대하여 "
              "직선 FP와 직선 F′P에 동시에 접하고 중심이 선분 F′F 위에 있는 원 [[C]]가 있다. 원 [[C]]의 중심을 C, 직선 F′P가 원 [[C]]와 만나는 점을 Q라 할 때, "
              "[[2 seg(PQ) = seg(PF)]] 이다. [[24 seg(CP)]] 의 값을 구하시오. (단, 점 P는 제1사분면 위의 점이다.)"),
    choices=None, derived_answer="63",
    figure=FIG("좌표평면 위 타원 x²/16+y²/7=1, 초점 F′·F, 제1사분면 위쪽의 점 P, 직선 PF·PF′에 접하고 중심 C가 x축 위에 있는 원, 직선 F′P와 원의 교점 Q"),
    difficulty_est=5, confidence=0.85,
    needs_review="프라임 라벨(F′) 텍스트 혼합 / 도형 표현 불가: 타원·원·접선",
    note="출처 [2021년 4월 고3 기하 30번/4점]. 기출 정답 63 = 빠른정답 ✓.")

# p72 — [2026년 6월 고3 기하 28번 변형]
add(id="c792bb13", qtype="choice",
    question=(_p64_body + "[[frac(seg(PF), seg(QF)) = frac(1, 2)]], [[frac(seg(PF), seg(FF))]]′ = [[frac(sqrt(5), 10)]] 이다. "
              "삼각형 FF′Q의 넓이가 12일 때, [[pow(b,2)]]의 값은? (단, [[a]]와 [[b]]는 양수이다.)"),
    choices=["[[10]]", "[[11]]", "[[12]]", "[[13]]", "[[14]]"],
    derived_answer="③", figure=_p64_fig, difficulty_est=4, confidence=0.8,
    needs_review="프라임 라벨(F′, 선분 FF′, 삼각형 FF′Q) 텍스트 혼합 / 도형 표현 불가: 타원",
    note="출처 [2026년 6월 고3 기하 28번 변형]. c=√5k → a=3k, b²=4k², 넓이 4k²=12 → b²=12 → ③ = 빠른정답 ✓.")

# p82
add(id="d1fd84c3", qtype="short",
    question=("원 [[pow(x,2) + pow(y,2) = 100]]에 내접하면서 원 [[pow(x - 4, 2) + pow(y,2) = 4]]에 외접하는 원의 중심 P가 그리는 도형을 [[E]]라 하자. "
              "두 점 O[[point(0, 0)]], O′[[point(4, 0)]]에 대하여 [[seg(PO)]] · [[seg(PO)]]′ 의 최댓값을 구하시오."),
    choices=None, derived_answer="36", figure=None, difficulty_est=2, confidence=0.85,
    needs_review="프라임 라벨(O′, 선분 PO′) 텍스트 혼합",
    note="PO=10−r, PO′=2+r → 합 12(타원) → 곱 최대 36 (빠른정답 4와 불일치).")

# ───────────────────────── 쌍곡선의 접선의 방정식 ─────────────────────────
# p46 — [2022년 4월 고3 기하 30번/4점]
_p46_body = ("을 초점으로 하는 쌍곡선 ")
_p46_mid = (" 쌍곡선 위의 점 중 제2사분면에 있는 점 P에 대하여 삼각형 F′FP는 넓이가 ")
_p46_tail = ("직선 PF′과 평행하고 쌍곡선에 접하는 두 직선을 각각 [[sub(l,1)]], [[sub(l,2)]]라 하자. 두 직선 [[sub(l,1)]], [[sub(l,2)]]가 [[x]]축과 만나는 점을 각각 "
             "[[sub(Q,1)]], [[sub(Q,2)]]라 할 때, ")
_p46_fig = FIG("좌표평면: 쌍곡선, 초점 F′·F, 제2사분면의 점 P(∠F′PF 직각 표시), 직선 PF′·PF, PF′과 평행한 두 접선 l₁, l₂와 x축 교점 Q₁, Q₂")
add(id="113150ef", qtype="short",
    question=("그림과 같이 두 점 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])" + _p46_body + "[[frac(pow(x,2), 10) - frac(pow(y,2), pow(a,2)) = 1]]이 있다." +
              _p46_mid + "15이고 ∠F′PF = [[frac(pi, 2)]] 인 직각삼각형이다. " + _p46_tail +
              "[[sub(Q,1)]][[sub(Q,2)]] = [[frac(q, p) sqrt(3)]] 이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이고, [[a]]는 양수이다.)"),
    choices=None, derived_answer="13", figure=_p46_fig, difficulty_est=5, confidence=0.8,
    needs_review="프라임 라벨(F′, ∠F′PF, 삼각형 F′FP)·첨자 점 라벨(선분 Q₁Q₂) 텍스트 혼합 / 도형 표현 불가: 쌍곡선·접선",
    note="출처 [2022년 4월 고3 기하 30번/4점]. c=5, a²=15, P(−4,3), 기울기 3인 접선 y=3x±5√3 → Q₁Q₂=10√3/3 → 13 (빠른정답 2와 불일치).")

# p60 — [2022년 4월 고3 기하 30번 변형]
add(id="c6852541", qtype="short",
    question=("다음 그림과 같이 두 점 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])" + _p46_body + "[[frac(pow(x,2), 24) - frac(pow(y,2), pow(a,2)) = 1]]이 있다." +
              _p46_mid + "36이고 ∠F′PF = [[frac(pi, 2)]] 인 직각삼각형이다. " + _p46_tail +
              "[[sub(Q,1)]][[sub(Q,2)]] = [[p sqrt(q)]] 이다. [[p q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 10보다 작은 자연수이고, [[a]]는 양수이다.)"),
    choices=None, derived_answer="20", figure=_p46_fig, difficulty_est=5, confidence=0.8,
    needs_review="프라임 라벨(F′, ∠F′PF, 삼각형 F′FP)·첨자 점 라벨(선분 Q₁Q₂) 텍스트 혼합 / 도형 표현 불가: 쌍곡선·접선",
    note="출처 [2022년 4월 고3 기하 30번 변형]. c²=60, a²=36, PF′=2√6, 기울기 3인 접선 y=3x±6√5 → Q₁Q₂=4√5 → pq=20 (빠른정답 10과 불일치).")

# p88 — [2026년 5월 고3 기하 30번 변형]
_p88_head = ("두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[pow(x,2) - frac(pow(y,2), pow(a,2)) = 1]] 위의 점 중 제2사분면에 있는 점 P에 대하여 직선 PF가 타원 ")
add(id="a20fae19", qtype="short",
    question=(_p88_head + "[[pow(x,2) + frac(pow(y,2), 4 pow(b,2)) = 1]] ([[0 < b < frac(1, 2)]])과 점 Q에서 접한다. 점 Q의 [[y]]좌표가 [[4 pow(b,2)]]이고 "
              "[[seg(PQ)]] = [[seg(PF)]]′ + [[4 pow(b,2)]]일 때, [[60(pow(a,2) + pow(b,2))]]의 값을 구하시오.\n(단, [[a]]는 양수이다.)"),
    choices=None, derived_answer="130", figure=None, difficulty_est=5, confidence=0.75,
    needs_review="프라임 라벨(F′, 선분 PF′) 텍스트 혼합",
    note="출처 [2026년 5월 고3 기하 30번 변형]. 접선 x/c+y=1, 4b²=1−1/c², 조건 ⇔ 2=(c²−1)(√(c²+1)+1)/c² → c²=3, a²=2, b²=1/6 → 130 (빠른정답 4와 불일치).")

# p89 — [2026년 5월 고3 기하 30번/4점]
add(id="7ce03a39", qtype="short",
    question=(_p88_head + "[[pow(x,2) + frac(pow(y,2), pow(b,2)) = 1]] ([[0 < b < 1]])과 점 Q에서 접한다. 점 Q의 [[y]]좌표가 [[pow(b,2)]]이고 "
              "[[seg(PQ)]] = [[seg(PF)]]′ + [[pow(b,2)]]일 때, [[30(pow(a,2) + pow(b,2))]]의 값을 구하시오.\n(단, [[a]]는 양수이다.)"),
    choices=None, derived_answer="80", figure=None, difficulty_est=5, confidence=0.75,
    needs_review="프라임 라벨(F′, 선분 PF′) 텍스트 혼합",
    note="출처 [2026년 5월 고3 기하 30번/4점]. 접선 x/c+y=1, b²=1−1/c², 조건 ⇔ 2=(c²−1)(√(c²+1)+1)/c² → c²=3, a²=2, b²=2/3 → 80 (빠른정답 54와 불일치, 검토 필요).")

# ───────────────────────── 벡터의 실수배 ─────────────────────────
# p41 — [2025년 5월 고3 기하 30번/4점]
add(id="e24dad71", qtype="short",
    question=("그림과 같이 [[seg(AD) = 8 sqrt(3)]] 인 직사각형 ABCD가 있다. 두 점 E, F가 점 E는 선분 AD 위를, 점 F는 선분 BC 위를 [[angle(CFE) = deg(60)]] 를 만족시키며 움직인다. "
              "선분 EF를 [[ratio(1, 2)]]로 내분하는 점을 G라 할 때, 점 G가 다음 조건을 만족시킨다.\n"
              "[[abs(vec(GA) + vec(GC))]] 의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, [[ratio(M, m) = ratio(sqrt(13), 1)]]이다.\n"
              "[[abs(vec(GA) + vec(GC))]] 의 값이 최대일 때의 점 G를 [[sub(G,1)]], 최소일 때의 점 G를 [[sub(G,2)]]라 하자. "
              "삼각형 B[[sub(G,1)]][[sub(G,2)]]의 넓이를 [[S]]라 할 때, [[pow(S,2)]]의 값을 구하시오. (단, [[seg(AB) <= 18]])"),
    choices=None, derived_answer="243",
    figure=FIG("직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상): 변 AD 위의 점 E, 변 BC 위의 점 F, 선분 EF, ∠CFE=60° 표시"),
    difficulty_est=5, confidence=0.85,
    needs_review="첨자 점 라벨(G₁, G₂, 삼각형 BG₁G₂) 텍스트 혼합 / 도형 표현 불가: 직사각형·선분 EF",
    note="출처 [2025년 5월 고3 기하 30번/4점]. 기출 정답 243 = 빠른정답 ✓.")

# p49
add(id="66b2530f", qtype="choice",
    question=("다음 그림과 같이 평면 위에 반지름의 길이가 3인 네 개의 원 [[sub(C,1)]], [[sub(C,2)]], [[sub(C,3)]], [[sub(C,4)]]가 서로 외접하고 있고 "
              "두 원 [[sub(C,1)]], [[sub(C,2)]]의 접점을 A, 두 원 [[sub(C,3)]], [[sub(C,4)]]의 접점을 B라고 하자. "
              "원 [[sub(C,3)]] 위를 움직이는 점 P와 원 [[sub(C,4)]] 위를 움직이는 점 Q에 대하여 [[abs(vec(AB) + vec(AP) + vec(AQ))]] 의 최댓값은?"),
    choices=["[[12]]", "[[15]]", "[[18]]", "[[21]]", "[[24]]"],
    derived_answer="⑤",
    figure=FIG("반지름 3인 네 원: C₁(왼쪽), C₂(아래), C₃(위), C₄(오른쪽)가 마름모꼴로 외접(C₂와 C₃도 접함); C₁·C₂의 접점 A, C₃·C₄의 접점 B, 화살표 A→B, A→P(C₃ 위), A→Q(C₄ 위)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 네 원의 배치(외접 관계가 그림에만 있음)",
    note="중심이 마름모(정삼각형 2개) 배치: AB+AP+AQ = (B+O₃+O₄−3A) + 3u + 3v, 상수 벡터 크기 18 → 최대 24 → ⑤ (빠른정답 없음).")

# p89
_p89_body = ("아래 그림과 같이 정삼각형 ABC가 있다. 선분 AB의 중점을 E라 할 때 선분 BC 위의 점 F와 삼각형 ABC의 외부에 있는 점 D를 두 점 C, E를 꼭짓점으로 하는 "
             "사각형 CDEF가 직사각형이 되도록 잡자.\n두 선분 DE와 AC의 교점을 G라 할 때, 다음 조건을 모두 만족시키는 두 점 P, Q가 사각형 CGEF의 내부에 있도록 하는 "
             "모든 자연수 [[k]]의 합을 구하시오.\n")
_p89_fig = FIG("정삼각형 ABC(A 위), AB의 중점 E, BC 위의 점 F, 외부의 점 D로 직사각형 CDEF, DE와 AC의 교점 G, 사각형 CGEF 음영")
add(id="23c6edc9", qtype="short",
    question=(_p89_body + "(가) [[13 vec(PA) - 3 vec(PB) - vec(PC) = k vec(FA)]]\n(나) [[18 vec(QG) - 6 vec(QE) = -k vec(DF)]]"),
    choices=None, derived_answer="30", figure=_p89_fig, difficulty_est=4, confidence=0.85,
    needs_review="도형 표현 불가: 정삼각형·직사각형 복합",
    note="B(−1,0), C(1,0), A(0,√3): (가) P=((4−k)/18, √3(13−k)/9) 내부 ⇔ k=9~12; (나) Q=(1−k/8, √3(12−k)/24) ⇔ k=5~11 → 9+10+11=30 = 빠른정답 ✓. 조건 상자는 그림 아래에 위치.")

# p90
add(id="ee9009fb", qtype="short",
    question=(_p89_body + "(가) [[11 vec(PA) - 3 vec(PB) - vec(PC) = k vec(FA)]]\n(나) [[15 vec(QG) - 5 vec(QE) = -k vec(DF)]]"),
    choices=None, derived_answer="17", figure=_p89_fig, difficulty_est=4, confidence=0.85,
    needs_review="도형 표현 불가: 정삼각형·직사각형 복합",
    note="(가) P=((4−k)/14, √3(11−k)/7) ⇔ k=8~10; (나) Q=(1−3k/20, √3(10−k)/20) ⇔ k=4~9 → 8+9=17 = 빠른정답 ✓. 조건 상자는 그림 아래에 위치.")

# ───────────────────────── 벡터의 내적 ─────────────────────────
# p1
add(id="a5ec4a85", qtype="short",
    question=("좌표평면에서 원 [[pow(x - 3, 2) + pow(y - 1, 2) = 2]] 위의 두 점 P, Q가 [[angle(OPQ) = deg(90)]], [[seg(OP) = seg(PQ)]]를 만족시킨다. "
              "[[dot(vec(OP), vec(OQ))]]의 서로 다른 모든 값의 합을 구하시오. (단, O는 원점이다.)"),
    choices=None, derived_answer="12", figure=None, difficulty_est=3, confidence=0.9,
    note="OP·OQ=|OP|²; Q는 O를 P 중심으로 ±90° 회전 → 해 4개, |OP|² ∈ {4, 8} → 합 12 = 빠른정답 ✓.")

# p2
add(id="f0710e89", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 6인 정삼각형 ABC에서 선분 AB의 중점을 M, 선분 AC의 중점을 N이라 하고 선분 MN 위를 움직이는 점을 P라 하자. "
              "삼각형 ABC의 변 또는 내부의 두 점 Q, R는 [[seg(BQ) = 2]], [[seg(CR) = 2]]를 만족시키며 움직이고 있다. "
              "[[dot((vec(AP) + vec(BQ)), vec(CR))]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, [[pow(M m, 2)]]의 값을 구하시오."),
    choices=None, derived_answer="76",
    figure=FIG("정삼각형 ABC(A 위), 중점 M(AB)·N(AC)과 선분 MN 위의 점 P(화살표 A→P), B·C를 중심으로 반지름 2인 호 위의 점 Q, R(화살표 B→Q, C→R)"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형·호·벡터",
    note="수치 최적화: M=1, m=−2√19 → (Mm)²=76 = 빠른정답 ✓.")

# p85 — [2017년 9월 고3 이과 29번/4점]
add(id="07008598", qtype="short",
    question=("좌표공간에 세 점 O[[vcomp(0, 0, 0)]], A[[vcomp(1, 0, 0)]], B[[vcomp(0, 0, 2)]]가 있다. 점 P가 [[dot(vec(OB), vec(OP)) = 0]], [[abs(vec(OP)) <= 4]]를 만족시키며 움직일 때,\n"
              "[[abs(vec(PQ)) = 1]], [[dot(vec(PQ), vec(OA)) >= frac(sqrt(3), 2)]]\n"
              "을 만족시키는 점 Q에 대하여 [[abs(vec(BQ))]]의 최댓값과 최솟값을 각각 [[M]], [[m]]이라 하자. "
              "[[M + m = a + b sqrt(5)]] 일 때, [[6(a + b)]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수이다.)"),
    choices=None, derived_answer="27", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2017년 9월 고3 이과 29번/4점]. M=2√5+1(u=(2,0,−1)/√5), m=3/2(Q=(0,0,1/2)) → a=5/2, b=2 → 27 (빠른정답 5와 불일치).")

# p91 — [2026년 7월 고3 기하 28번 변형]
add(id="42b41a40", qtype="choice",
    question=("좌표평면에 [[seg(AB) = 8]], [[seg(AD) = 6]]인 직사각형 ABCD가 있다. 선분 CD 위의 한 점 P와 직사각형 ABCD 내부의 한 점 Q가 다음 조건을 만족시킨다.\n"
              "(가) [[dot(vec(PA), vec(PQ)) = pow(abs(vec(PQ)), 2)]]\n"
              "(나) [[10 vec(BQ) = vec(BA) + 4 vec(AD)]]\n"
              "[[dot((vec(AR) + vec(QR)), (vec(PR) + vec(QR))) = 0]]을 만족시키는 점 R에 대하여 [[dot(vec(BR), vec(QP))]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, "
              "[[M + m]]의 값은?"),
    choices=["[[26]]", "[[frac(131, 5)]]", "[[frac(132, 5)]]", "[[frac(133, 5)]]", "[[frac(134, 5)]]"],
    derived_answer="③",
    figure=FIG("직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상)만 그려진 그림"),
    difficulty_est=4, confidence=0.85,
    note="출처 [2026년 7월 고3 기하 28번 변형]. B 원점: Q=(2.4,0.8), P=(6,2), R은 지름 M₁M₂인 원(중심 (2.7,2.9)) → M+m=2·13.2=132/5 → ③ = 빠른정답 ✓. 그림은 라벨만 있는 직사각형(장식).")

# p97 — [2024년 11월 고3 기하 30번 변형]
add(id="596aa225", qtype="short",
    question=("좌표평면에 한 변의 길이가 6인 정사각형 ABCD가 있다. [[abs(vec(XB) + vec(XC)) = abs(vec(XB) - vec(XC))]] 를 만족시키는 점 X가 나타내는 도형을 [[S]]라 하자. "
              "도형 [[S]] 위의 점 P에 대하여 [[6 vec(PQ) = vec(PB) + 3 vec(PD)]]를 만족시키는 점을 Q라 할 때, [[dot(vec(AC), vec(AQ))]]의 최댓값과 최솟값을 각각 [[M]], [[m]]이라 하자. "
              "[[M m]]의 값을 구하시오."),
    choices=None, derived_answer="1692",
    figure=FIG("정사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상)만 그려진 그림"),
    difficulty_est=4, confidence=0.85,
    note="출처 [2024년 11월 고3 기하 30번 변형]. S: 지름 BC인 원, Q=P/3+(3,3) → AC·AQ=42+6(cos t−sin t) → Mm=42²−72=1692 = 빠른정답 ✓. 그림은 라벨만 있는 정사각형(장식).")

# ───────────────────────── 직선과 평면의 위치 관계 ─────────────────────────
# p45 (id 2개)
dup(["edb9eb88", "93a16bc4"], qtype="short",
    question=("아래 그림과 같이 평면 [[alpha]] 위에 중심이 A이고 반지름의 길이가 3인 원 [[C]]가 있다. 점 A를 지나고 평면 [[alpha]]에 수직인 직선 위의 점 B에 대하여 "
              "[[seg(AB) = 4]]이다. 원 [[C]] 위의 점 P에 대하여 원 [[D]]가 다음 조건을 만족한다.\n"
              "(가) 선분 BP는 원 [[D]]의 지름이다.\n"
              "(나) 점 A에서 원 [[D]]를 포함하는 평면에 내린 수선의 발 H는 선분 BP 위에 있다.\n"
              "평면 [[alpha]] 위에 [[seg(AX) = frac(55, 6)]] 인 점 X가 있다. 점 P가 원 [[C]] 위를 움직일 때, 원 [[D]] 위의 점 Q에 대하여 선분 XQ의 길이의 최댓값은 "
              "[[frac(q, p)]] 이다. [[p + q]]의 값을 구하시오. (단, [[p]], [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="40",
    figure=FIG("평면 α 위의 원 C(중심 A), A 위쪽 수직선 위의 점 B, 원 C 위의 점 P, BP를 지름으로 하는 기울어진 원 D, A에서 원 D의 평면에 내린 수선의 발 H(직각), α 위의 점 X"),
    difficulty_est=5, confidence=0.75,
    needs_review="도형 표현 불가: 공간 원·수선 입체도",
    note="BP=5, 원 D는 평면 ABP에 수직인 평면 위 반지름 5/2; 수치 최적화로 최댓값 37/3 → p+q=40 (빠른정답 11과 불일치, 검토 필요).")
