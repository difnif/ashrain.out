# -*- coding: utf-8 -*-
# esc_sonnet_m2-2_5of5 — 이미지 기준 전사 (35 항목 / 35쪽) — 중2-2 평행사변형·피타고라스 정리
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

FIG_PAR = "평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)"
REV_FIG = "도형 표현 불가: "

# ── 평행사변형 p89 (내부의 한 점)
add(id="2ea122ec", qtype="short",
    question=("다음 그림과 같이 평행사변형 ABCD의 내부에 한 점 P에 대하여 [[tri(PAB)]]의 넓이가 [[20]] cm²이다. "
              "[[ratio(tri(PAB), tri(PCD)) = ratio(5, 6)]]일 때, [[quad(ABCD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="88 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", 내부의 점 P와 네 꼭짓점을 잇는 선분 PA·PB·PC·PD, 평행사변형 전체 음영"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "평행사변형 내부 점·선분 도형",
    note="△PCD=24, □ABCD=2(△PAB+△PCD)=2·44=88 cm². 빠른정답 없음.")

# ── p90 (내부의 두 점)
add(id="272db88d", qtype="choice",
    question=("다음 그림과 같이 평행사변형 ABCD의 내부의 두 점 P, Q에 대하여 [[tri(PAB) = tri(QCD) = 15]], "
              "[[tri(PDA) = tri(QBC) = 6]]일 때, [[quad(AQCP)]]의 넓이는?"),
    choices=["[[10]]", "[[12]]", "[[14]]", "[[16]]", "[[18]]"], derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", 내부의 두 점 P(위쪽)·Q(아래쪽), 선분 AP·BP·DP·AQ·BQ·CQ·DQ·CP 등, 사각형 AQCP 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "평행사변형 내부 두 점 복합 도형",
    note="□ABCD=2(15+6)=42, □ABCQ=6+6, □CDAP=6+6 → □AQCP=42−24=18 → ⑤. 빠른정답 없음.")

# ── p91 (AP 연장선과 BC의 교점)
add(id="1fb0a247", qtype="short",
    question=("다음 그림과 같이 평행사변형 ABCD의 내부의 한 점 P에 대하여 [[seg(AP)]]의 연장선과 [[seg(BC)]]의 교점을 Q라 하자. "
              "[[tri(DPQ) = 4 tri(DAP)]]이고 [[tri(PBC) = 32]] cm²일 때, [[quad(ABCD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="80 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", A 근처 내부의 점 P, AP의 연장선이 BC와 만나는 점 Q, 선분 PB·PC·PD·DQ, 전체 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "평행사변형·연장선 교점 복합 도형",
    note="AP:PQ=1:4 → P에서 BC까지 거리는 높이의 4/5, △PBC=(4/5)·(S/2)=32 → S=80 cm². 빠른정답 10과 불일치(정렬 어긋남 의심).")

# ── p92
add(id="457f9eb7", qtype="short",
    question=("다음 그림과 같이 평행사변형 ABCD의 내부의 한 점 P에 대하여 [[seg(AP)]]의 연장선과 [[seg(BC)]]의 교점을 Q라 하자. "
              "[[tri(DPQ) = 2 tri(DAP)]], [[tri(PBC) = 30]] cm²일 때, [[quad(ABCD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="90 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_PAR + ", A 근처 내부의 점 P, AP의 연장선이 BC와 만나는 점 Q, 선분 PB·PC·PD·DQ, 전체 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "평행사변형·연장선 교점 복합 도형",
    note="AP:PQ=1:2 → △PBC=(2/3)·(S/2)=30 → S=90 cm². 빠른정답 없음.")

# ── p98 (평행사변형 종이 접기)
add(id="28d4b99e", qtype="short",
    question=("다음 그림은 평행사변형 ABCD를 대각선 BD를 접는 선으로 하여 점 C가 점 E에 오도록 접은 것이다. "
              "[[seg(DE)]]와 [[seg(BA)]]의 연장선의 교점을 F라 하고 [[angle(BDC) = deg(32)]]일 때, [[angle(AFE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(116)",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래·점선)를 대각선 BD로 접어 C가 옮겨간 점 E(A 위쪽), DE와 BA의 연장선의 교점 F(A 위), D에 32° 표시, △BDE 음영, F 부근 각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "평행사변형 접기 도형",
    note="∠FBD=∠ABD=∠BDC=32°(엇각), ∠FDB=∠BDC=32°(접기) → ∠AFE=∠BFD=180°−64°=116°. 빠른정답 없음.")

# ── 피타고라스 p7 (각의 이등분선)
add(id="fb752f60", qtype="short",
    question=("다음 그림과 같이 [[angle(C) = deg(90)]]인 직각삼각형 ABC에서 [[angle(A)]]의 이등분선이 [[seg(BC)]]와 만나는 점을 D라 하자. "
              "[[seg(AB) = 15]] cm, [[seg(AC) = 9]] cm일 때, [[tri(ABD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="frac(135,4) cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, C에 직각 표시), A의 각 이등분선(A에 점 2개)이 BC와 만나는 점 D, △ABD 음영, AB=15 cm·AC=9 cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·각의 이등분선 도형",
    note="BC=12, BD:DC=15:9 → BD=15/2, △ABD=½·(15/2)·9=135/4 cm². 빠른정답 없음.")

# ── p14
add(id="00540241", qtype="short",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[perp(seg(AB), seg(CD))]]이고 [[seg(AC) = 10]] cm, [[seg(BC) = 17]] cm, [[seg(BD) = 15]] cm일 때, "
              "[[tri(ADC)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="24 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), C에서 AB에 내린 수선의 발 D(직각 표시), BD=15 cm·AC=10 cm·BC=17 cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "삼각형·수선 도형",
    note="CD=√(17²−15²)=8, AD=√(10²−8²)=6 → 둘레 6+8+10=24 cm. 빠른정답 20 cm과 불일치(정렬 어긋남 의심).")

# ── p15 (첨자 점 라벨)
add(id="10542218", qtype="short",
    question=("다음 그림에서 AB₁ = AA₂, AB₂ = AA₃, AB₃ = AA₄일 때, AA₄의 길이를 구하시오."),
    choices=None, derived_answer="6",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형(오른쪽 아래 A, 오른쪽 위 B, AB=3, B에 직각 표시), 밑변 위에 A에서 왼쪽으로 A₁(A₁A=3), A₂, A₃, A₄, 윗변 위에 B₁, B₂, B₃(각각 A₁, A₂, A₃ 바로 위), A에서 B₁·B₂·B₃로 선분, AB₁·AB₂·AB₃를 반지름으로 하는 호로 밑변 위에 A₂·A₃·A₄를 잡음, A₁·A₂·A₃·A₄에 직각 표시"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="첨자 점 라벨(A₁~A₄, B₁~B₃) seg 표기 불가(선분 기호를 텍스트로 대체) / " + REV_FIG + "직사각형·호 복합 도형",
    note="AB₁=√(3²+3²)=√18, AB₂=√(18+9)=√27, AB₃=√(27+9)=6 → AA₄=6. 빠른정답 40과 불일치(정렬 어긋남 의심).")

# ── p17
add(id="a62f4c78", qtype="short",
    question=("다음 그림에서 [[seg(AB) = seg(BC) = seg(CD) = seg(DE) = 2]] cm일 때, [[seg(AE)]]의 길이를 구하시오."),
    choices=None, derived_answer="4 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "A(아래 가운데)에서 B(오른쪽), C(B 위), D(C 왼쪽 위), E(D 왼쪽)로 이어지는 나선형 꺾은선, B·C·D에 직각 표시, 선분 AC·AD·AE, 각 변 2 cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형 연쇄 도형",
    note="AC²=8, AD²=12, AE²=16 → AE=4 cm. 빠른정답 24 cm과 불일치(정렬 어긋남 의심).")

# ── p19·p20·p21 (직각이등변삼각형 6개로 분할)
FIG_6TRI = ("직각이등변삼각형 ABC(A 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, C가 직각), 빗변 AB 위의 점 D에서 AC에 내린 수선의 발 E(직각 표시)와 "
            "AB에 수직인 선분 DG(G는 BC 위, D에 직각 표시), E에서 DG에 내린 수선의 발 F(직각 표시), EF 위의 점 H에서 HG⊥BC(G에 직각 표시)·HC, "
            "H에 직각 표시; AB 치수(점선 호)")
add(id="1eb981d0", qtype="short",
    question=("다음 그림은 [[angle(C) = deg(90)]]인 직각이등변삼각형 ABC를 6개의 직각이등변삼각형으로 나눈 것이다. "
              "[[seg(AB) = 20]]일 때, [[seg(FG)]]의 길이를 구하시오."),
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_6TRI + " AB=20"}}],
    difficulty_est=4, confidence=0.75,
    needs_review=REV_FIG + "직각이등변삼각형 6개 분할 도형",
    note="좌표로 풀면 AE=(3/5)AC, FG=AB/10=2(풀이 답, 검토 요망). 빠른정답 27과 불일치(정렬 어긋남 의심).")
add(id="217cb20c", qtype="short",
    question=("다음 그림은 [[angle(C) = deg(90)]]인 직각이등변삼각형 ABC를 6개의 직각이등변삼각형으로 나눈 것이다. "
              "[[seg(AB) = 30]]일 때, [[seg(FG)]]의 길이를 구하시오."),
    choices=None, derived_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_6TRI + " AB=30"}}],
    difficulty_est=4, confidence=0.75,
    needs_review=REV_FIG + "직각이등변삼각형 6개 분할 도형",
    note="FG=AB/10=3(풀이 답, 검토 요망). 빠른정답 4 cm과 불일치(정렬 어긋남 의심).")
add(id="dbce1811", qtype="short",
    question=("다음 그림은 [[angle(C) = deg(90)]]인 직각이등변삼각형 ABC를 6개의 직각이등변삼각형으로 나눈 것이다. "
              "[[seg(AB) = 50]]일 때, [[seg(FG)]]의 길이를 구하시오."),
    choices=None, derived_answer="5",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_6TRI + " AB=50"}}],
    difficulty_est=4, confidence=0.75,
    needs_review=REV_FIG + "직각이등변삼각형 6개 분할 도형",
    note="FG=AB/10=5(풀이 답, 검토 요망). 빠른정답 9개와 불일치(정렬 어긋남 의심).")

# ── p23 (직각삼각형의 닮음)
add(id="0b555a4d", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 [[perp(seg(AH), seg(BC))]]일 때, [[x - y]]의 값을 구하시오."),
    choices=None, derived_answer="frac(9,5)",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각 표시), A에서 BC에 내린 수선의 발 H(직각 표시), AB=x cm, AC=12 cm, AH=y cm, BC=15 cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·수선 도형(치수 x, 12, y, 15는 그림에만 있음)",
    note="x=√(15²−12²)=9, y=9·12/15=36/5 → x−y=9/5 = 빠른정답 ✓.")

# ── p25
add(id="5f2a8968", qtype="short",
    question=("다음 그림과 같은 직각삼각형 ABC에서 점 M은 [[seg(BC)]]의 중점이고 [[perp(seg(AH), seg(BC))]], [[perp(seg(PH), seg(AM))]]이다. "
              "[[seg(AB) = 15]], [[seg(AC) = 20]]일 때, [[seg(PH)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(84,25)",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각 표시), BC의 중점 M(BM=MC 표시), A에서 BC에 내린 수선의 발 H(직각 표시, M 왼쪽), 선분 AM, H에서 AM에 내린 수선의 발 P(직각 표시), AB=15·AC=20 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·중선·수선 복합 도형",
    note="BC=25, AH=12, BH=9, AM=25/2, HM=7/2 → PH=AH·HM/AM=84/25 = 빠른정답 ✓.")

# ── p26·p27·p28
FIG_HQ = ("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각 표시), BC의 중점 M, A에서 BC에 내린 수선의 발 H(직각 표시, M 오른쪽), "
          "선분 AM, H에서 AM에 내린 수선의 발 Q(직각 표시)")
add(id="70687e35", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 점 M은 [[seg(BC)]]의 중점이고 [[perp(seg(AH), seg(BC))]], [[perp(seg(HQ), seg(AM))]]이다. "
              "[[seg(AH) = 15]] cm, [[seg(MH) = 8]] cm일 때, [[seg(AQ) - seg(CH)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(72,17) cm",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_HQ + "; AH=15 cm(점선), MH=8 cm 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·중선·수선 복합 도형",
    note="AM=17=MC, AQ=AH²/AM=225/17, CH=17−8=9 → 225/17−9=72/17 cm. 빠른정답 없음.")
add(id="8b6e4f9a", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 점 M은 [[seg(BC)]]의 중점이고 [[perp(seg(AH), seg(BC))]], [[perp(seg(HQ), seg(AM))]]이다. "
              "[[seg(AH) = 12]] cm, [[seg(MH) = 5]] cm일 때, [[seg(AQ) - seg(CH)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(40,13) cm",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_HQ + "; AH=12 cm(점선), MH=5 cm 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·중선·수선 복합 도형",
    note="AM=13=MC, AQ=144/13, CH=13−5=8 → 144/13−8=40/13 cm. 빠른정답 없음.")
add(id="7e9d24a9", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 직각삼각형 ABC에서 점 M은 [[seg(BC)]]의 중점이고 [[perp(seg(AH), seg(BC))]], [[perp(seg(HQ), seg(AM))]]이다. "
              "[[seg(AH) = 16]] cm, [[seg(MH) = 12]] cm일 때, [[seg(AQ) + seg(CH)]]의 길이를 구하시오."),
    choices=None, derived_answer="frac(104,5) cm",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_HQ + "; AH=16 cm(점선), MH=12 cm 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형·중선·수선 복합 도형",
    note="AM=20=MC, AQ=256/20=64/5, CH=20−12=8 → 64/5+8=104/5 cm. 빠른정답 없음.")

# ── p29 (사각형, 대각선)
add(id="a047f1c6", qtype="short",
    question=("다음 그림과 같이 [[angle(B) = angle(D) = deg(90)]]인 [[quad(ABCD)]]에서 [[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="40 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 왼쪽, D 위, B 왼쪽 아래, C 오른쪽 아래), B·D에 직각 표시, AD=30 cm, AB=14 cm, BC=48 cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "사각형 도형(치수 30·14·48 cm는 그림에만 있음)",
    note="AC=√(14²+48²)=50, CD=√(50²−30²)=40 cm = 빠른정답 ✓.")

# ── p30
add(id="643ab745", qtype="short",
    question=("다음 그림의 [[quad(ABCD)]]에서 [[seg(AB) = 8]] cm, [[seg(BC) = 17]] cm, [[seg(CD) = 9]] cm, [[seg(DA) = 12]] cm이고 [[angle(D) = deg(90)]]일 때, "
              "[[quad(ABCD)]]의 넓이를 구하시오."),
    choices=None, derived_answer="114 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), D에 직각 표시, AD=12 cm·AB=8 cm·CD=9 cm·BC=17 cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "사각형 도형",
    note="AC=15, 8²+15²=17² → ∠BAC=90°, 넓이=½·12·9+½·8·15=54+60=114 cm². 빠른정답 없음.")

# ── p32
add(id="4a26b299", qtype="choice",
    question=("다음 그림의 [[quad(ABCD)]]에서 [[angle(A) = angle(C) = deg(90)]]이고 [[seg(AD) = 5]], [[seg(BC) = 6]], [[seg(CD) = 8]]일 때, "
              "[[pow(seg(AB), 2)]]의 값은?"),
    choices=["[[60]]", "[[75]]", "[[90]]", "[[105]]", "[[120]]"], derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "점선 원에 내접한 사각형 ABCD(A 위, D 오른쪽, C 아래, B 왼쪽), A·C에 직각 표시, AB=x, AD=5, BC=6, CD=8"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "원에 내접하는 사각형 도형",
    note="BD²=6²+8²=100, AB²=100−25=75 → ② = 빠른정답(2) ✓.")

# ── p33
add(id="b3c76c03", qtype="short",
    question=("다음 그림과 같이 [[angle(B) = angle(D) = deg(90)]]인 [[quad(ABCD)]]에서 [[seg(CD)]]의 길이를 구하시오."),
    choices=None, derived_answer="15 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 왼쪽, D 위, B 왼쪽 아래, C 오른쪽 아래), B·D에 직각 표시, AD=20 cm, AB=7 cm, BC=24 cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "사각형 도형(치수 20·7·24 cm는 그림에만 있음)",
    note="AC=√(7²+24²)=25, CD=√(25²−20²)=15 cm = 빠른정답 ✓.")

# ── p34 (사다리꼴)
add(id="85bb97f9", qtype="short",
    question=("다음 그림과 같은 사다리꼴 ABCD의 넓이를 구하시오."),
    choices=None, derived_answer="285 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), D·C에 직각 표시, AD=15 cm, AB=17 cm, BC=23 cm 치수(점선 호), 내부 음영"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "사다리꼴 도형(치수 15·17·23 cm는 그림에만 있음)",
    note="A에서 BC에 수선: BH=23−15=8, 높이=√(17²−8²)=15 → ½(15+23)·15=285 cm². 빠른정답 없음.")

# ── p39·p40 (사다리꼴, 수선)
FIG_TRAP = ("사다리꼴 ABCD(D 위 왼쪽, C 위 오른쪽, B 아래 오른쪽, A 아래 왼쪽, B·C에 직각 표시), BC 위의 점 F, F에서 AD에 내린 수선의 발 E(직각 표시), "
            "점선 DF·AF")
add(id="9c4d6b03", qtype="short",
    question=("다음 그림과 같은 사다리꼴 ABCD에서 [[angle(B) = angle(C) = angle(DEF) = deg(90)]]이다.\n"
              "[[seg(EF) = seg(CF) = seg(BF)]]이고 [[seg(CD) = 9]], [[seg(AB) = 25]]일 때, [[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="30",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "사다리꼴·수선 복합 도형",
    note="RHS 합동으로 DE=DC=9, AE=AB=25 → AD=34; D에서 AB에 수선: 밑변 차 16, BC=√(34²−16²)=30. 빠른정답 10초와 불일치(정렬 어긋남).")
add(id="132093b6", qtype="short",
    question=("다음 그림과 같은 사다리꼴 ABCD에서 [[angle(B) = angle(C) = angle(DEF) = deg(90)]]이다.\n"
              "[[seg(EF) = seg(CF) = seg(BF)]]이고 [[seg(CD) = 4]], [[seg(AB) = 9]]일 때, [[seg(BC)]]의 길이를 구하시오."),
    choices=None, derived_answer="12",
    figure=[{"fn": "unsupported", "args": {"raw": FIG_TRAP}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "사다리꼴·수선 복합 도형",
    note="DE=DC=4, AE=AB=9 → AD=13, 밑변 차 5, BC=√(13²−5²)=12. 빠른정답 없음.")

# ── p46 (사분원, 직사각형의 대각선)
add(id="a2d498bd", qtype="choice",
    question=("다음 그림과 같이 반지름의 길이가 [[10]] cm인 사분원 위의 점 C에서 [[seg(OA)]], [[seg(OB)]]에 내린 수선의 발을 각각 D, E라 하자. "
              "[[seg(EO) = 8]] cm일 때, [[quad(ODCE)]]의 둘레의 길이는?"),
    choices=["[[20]] cm", "[[24]] cm", "[[28]] cm", "[[32]] cm", "[[36]] cm"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "중심 O(왼쪽 아래), B(위)·A(오른쪽)인 사분원, 호 위의 점 C, C에서 OA·OB에 내린 수선의 발 D·E, 직사각형 ODCE, EO=8 cm·OA=10 cm 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "사분원·직사각형 도형",
    note="OC=10, CE=√(100−64)=6 → 둘레 2(8+6)=28 cm → ③ = 빠른정답(3) ✓.")

# ── p49 (이등변삼각형의 넓이)
add(id="e4850446", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC) = 13]] cm, [[seg(BC) = 10]] cm인 이등변삼각형 ABC의 넓이를 구하시오."),
    choices=None, derived_answer="60 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AB=13 cm·AC=13 cm·BC=10 cm 치수(점선 호), 내부 음영"}}],
    difficulty_est=1, confidence=0.85,
    needs_review=REV_FIG + "이등변삼각형 도형",
    note="높이 √(13²−5²)=12 → ½·10·12=60 cm². 빠른정답 없음.")

# ── p51
add(id="a1481614", qtype="short",
    question=("다음 그림의 [[tri(ABC)]]는 [[seg(AB) = seg(AC) = 10]], [[seg(BC) = 16]]인 이등변삼각형이다. "
              "[[seg(AD)]]는 [[tri(ABC)]]의 높이이고 [[seg(DE)]]는 [[angle(ADB)]]의 이등분선이다. [[tri(AED)]]의 넓이를 구하시오."),
    choices=None, derived_answer="frac(72,7)",
    figure=[{"fn": "unsupported", "args": {"raw": "이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), A에서 BC에 내린 높이 AD(D에 각 이등분 표시 점 2개), AB 위의 점 E와 선분 DE, △AED 음영, AB=10·AC=10·BC=16 치수(점선 호)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "이등변삼각형·각의 이등분선 도형",
    note="AD=6, BD=8, AE:EB=6:8 → △AED=(3/7)·24=72/7 = 빠른정답 ✓.")

# ── p62 (피타고라스의 방법)
add(id="234fb14e", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 [[10]] cm인 정사각형 ABCD에서 [[seg(AE) = seg(BF) = seg(CG) = seg(DH) = 4]] cm일 때, "
              "[[quad(EFGH)]]의 넓이를 구하시오."),
    choices=None, derived_answer="52 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, 네 꼭짓점 직각 표시), 변 위의 점 E(AB), F(BC), G(CD), H(DA), 내부의 사각형 EFGH 음영, AE=4 cm·AD=10 cm 치수(점선 호), 같은 길이 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "정사각형 내접 정사각형 도형",
    note="EFGH=4²+6²=52 cm². 빠른정답 없음.")

# ── p66
add(id="7a25650e", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(90)]]인 [[tri(AEH)]]와 이와 합동인 세 개의 삼각형을 이용하여 정사각형 ABCD를 만들었다. "
              "이때 정사각형 EFGH의 넓이를 구하시오."),
    choices=None, derived_answer="74",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래, 네 꼭짓점 직각 표시), 변 위의 점 E(AB), F(BC), G(CD), H(AD), 내부의 정사각형 EFGH 음영, AH=7·HD=5 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "정사각형 내접 정사각형 도형(치수 7·5는 그림에만 있음)",
    note="AE=HD=5, EH²=7²+5²=74. 빠른정답 5 cm과 불일치(정렬 어긋남 의심).")

# ── p73 (가필드의 방법)
add(id="577c3b14", qtype="short",
    question=("다음 그림에서 직각삼각형 ABC와 CDE는 합동이고 세 점 B, C, D는 한 직선 위에 있다. [[seg(BC) = 6]] cm이고 "
              "[[tri(ACE)]]의 넓이가 [[20]] cm²일 때, 사다리꼴 ABDE의 넓이를 구하시오."),
    choices=None, derived_answer="32 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABDE(B 왼쪽 아래, D 오른쪽 아래, A 왼쪽 위, E 오른쪽 위, B·D에 직각 표시), BD 위의 점 C, 선분 AC·CE, BC=6 cm 치수(점선 호), 내부 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "가필드 사다리꼴 도형",
    note="∠ACE=90°, ½AC²=20 → AC²=40, AB²=40−36=4, AB=2=CD, DE=6 → 넓이 ½(2+6)·8=32 cm². 빠른정답 없음.")

# ── p74
add(id="316ce246", qtype="choice",
    question=("다음 그림에서 [[cong(tri(ABE), tri(ECD))]]이고 [[seg(AB) = 8]] cm, [[tri(AED) = 50]] cm²일 때, [[quad(ABCD)]]의 넓이는?"),
    choices=["[[92]] cm²", "[[94]] cm²", "[[96]] cm²", "[[98]] cm²", "[[100]] cm²"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위(A보다 낮음), B 왼쪽 아래, C 오른쪽 아래, B·C에 직각 표시), BC 위의 점 E, 선분 AE·DE, AB=8 cm 치수(점선 호), 내부 음영"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=REV_FIG + "가필드 사다리꼴 도형",
    note="½AE²=50 → AE=10, BE=6=CD, EC=8 → □ABCD=½(8+6)·14=98 cm² → ④. 빠른정답 89와 불일치(정렬 어긋남 의심).")

# ── p76 (바스카라의 방법, 색종이 접기)
add(id="11f518ec", qtype="short",
    question=("다음 그림과 같이 둘레의 길이가 [[28]] cm인 정사각형 모양의 색종이 ABCD에서 [[seg(AE) = seg(BF) = seg(CG) = seg(DH)]]가 되도록 "
              "네 점 E, F, G, H를 정한 후, [[seg(EF)]], [[seg(FG)]], [[seg(GH)]], [[seg(HE)]]를 접는 선으로 하여 네 모퉁이를 접었더니 넓이가 "
              "[[9]] cm²인 사각형 A′B′C′D′이 만들어졌다. 이때 사각형 EFGH의 넓이를 구하시오."),
    choices=None, derived_answer="29 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(점선, A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 변 위의 점 E(AB), F(BC), G(CD), H(DA)(같은 길이 표시), 사각형 EFGH 음영, 네 모퉁이를 안쪽으로 접은 화살표와 접힌 꼭짓점 A′, B′, C′, D′, 가운데 작은 정사각형 A′B′C′D′ 진한 음영"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="프라임 점 라벨(A′B′C′D′) 표기 불가(텍스트) / " + REV_FIG + "색종이 접기 도형",
    note="한 변 7, AE=a, EB=7−a: 가운데 정사각형 (2a−7)²=9 → {a, 7−a}={2, 5} → EFGH=4+25=29 cm². 빠른정답 없음.")

# ── p77
add(id="2be3c1e0", qtype="short",
    question=("다음 그림에서 4개의 직각삼각형은 모두 합동이고 [[seg(AB) = 13]] cm, [[seg(AE) = 12]] cm일 때, 사각형 EFGH의 넓이를 구하시오."),
    choices=None, derived_answer="49 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 내부의 합동인 직각삼각형 4개(ABE, BCF, CDG, DAH; E·F·G·H에 직각 표시)와 가운데 정사각형 EFGH 음영, AB=13·AE=12 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "바스카라 정사각형 도형",
    note="BE=√(13²−12²)=5=AH, EH=12−5=7 → 49 cm². 빠른정답 4와 불일치(정렬 어긋남 의심).")

# ── p92 (변의 길이에 따른 삼각형의 종류)
add(id="3a490b99", qtype="choice",
    question=("다음 그림에서 [[seg(AB) = 12]], [[seg(BC) = 13]], [[seg(CD) = 4]], [[seg(DA) = 3]]이고 [[angle(BAC) = deg(90)]]일 때, "
              "[[tri(ACD)]]는 어떤 삼각형인가?"),
    choices=["정삼각형", "이등변삼각형", "예각삼각형", "직각삼각형", "둔각삼각형"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(B 왼쪽 아래, C 오른쪽 아래, A 오른쪽 위, A에 직각 표시)와 그 오른쪽에 붙은 삼각형 ACD(D 오른쪽), AB=12·BC=13·AD=3·CD=4 치수(점선 호)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review=REV_FIG + "직각삼각형 결합 도형",
    note="AC=√(13²−12²)=5, 3²+4²=5² → △ACD는 직각삼각형 → ④. 빠른정답 '문각삼각형'(⑤ 둔각삼각형?)과 불일치.")

# ── p96 (각의 크기에 따른 변의 길이) — 도형 없음
add(id="f43d4ac1", qtype="choice",
    question=("[[tri(ABC)]]에서 [[seg(AB) = c]], [[seg(BC) = a]], [[seg(AC) = b]]라 할 때, 다음 중 옳지 않은 것은?"),
    choices=["[[angle(B) = deg(120)]]이면 [[pow(b,2) > pow(a,2) + pow(c,2)]]이다.",
             "[[angle(C) = deg(90)]]이면 [[pow(c,2) = pow(a,2) + pow(b,2)]]이다.",
             "[[angle(A) = deg(90)]]이면 [[pow(a,2) = pow(b,2) + pow(c,2)]]이다.",
             "[[angle(B) = deg(90)]]이면 [[pow(b,2) = pow(a,2) + pow(c,2)]]이다.",
             "[[pow(c,2) < pow(a,2) + pow(b,2)]]이면 [[angle(C) > deg(90)]]이다."],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    note="①~④ 참, ⑤는 c²<a²+b²이면 ∠C<90°이므로 거짓 → ⑤. 빠른정답 2와 불일치(정렬 어긋남 의심).")
