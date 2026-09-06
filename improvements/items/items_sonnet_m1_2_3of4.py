# -*- coding: utf-8 -*-
# esc_sonnet_m1-2_3of4 — 이미지 기준 전사 (80 항목 / 80쪽: 평행선의 성질 35, 다각형의 내각과 외각 15, 부채꼴 7, 도수분포다각형 1, 삼각형의 합동 22)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
def DEGS(*v): return [f"[[deg({x})]]" for x in v]

# =====================================================================
# 평행선의 성질
# =====================================================================

# ---------------- p36
add(id="70514db2", qtype="choice",
    question="다음 그림에서 [[par(l, n)]], [[par(m, k)]]일 때, [[angle(x) + angle(y)]]의 크기는?",
    choices=DEGS(145, 150, 155, 160, 165), derived_answer="①",
    figure=U("가로 직선 4개 l, m, n, k(위→아래)를 가로지르는 두 직선. 첫째 직선(왼쪽 위→오른쪽 아래): l과의 교점 위 오른쪽 100°, m과의 교점 아래 오른쪽 x(초록), k와의 교점 아래 오른쪽 80°. 둘째 직선(왼쪽 아래→오른쪽 위): l과의 교점 위 오른쪽 y(분홍), n과의 교점 아래 오른쪽 115°"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선 4개·횡단선 2개 각 표시 도형",
    note="m∥k → x=80°(동위각), l∥n → y=180°−115°=65° → 145° ①. 빠른정답 deg(52)와 불일치.")

# ---------------- p38
add(id="b22ce399", qtype="choice",
    question=("다음 그림에서 [[par(seg(AB), seg(CD))]], [[par(seg(AD), seg(BC))]]이고 [[angle(BAF) = angle(DAF)]], "
              "[[3 angle(ABC) = 2 angle(DAB)]], [[5 angle(ECG) = 3 angle(GCF)]]일 때, [[angle(CGE)]]의 크기는?"),
    choices=DEGS(81, 83, 89, 93, 99), derived_answer="⑤",
    figure=U("평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), BC의 연장선 위 점 F, 선분 AF와 CD의 교점 E, C에서 오른쪽 위로 그은 반직선과 AF의 교점 G, A에 같은 각 표시(점 2개), G에 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형·교차 선분 복합 도형",
    note="∠ABC=72°, ∠DAB=108°, ∠BAF=54°, ∠DCF=72° → ∠GCF=45°, ∠AFB=54° → ∠CGF=81°, ∠CGE=99° ⑤. 빠른정답 deg(10)과 불일치.")

# ---------------- p39
add(id="704f75a3", qtype="short",
    question="다음 그림에서 [[par(l, k)]], [[par(m, n)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(55)",
    figure=U("l(왼쪽 가로)이 끝점에서 135°(아래)로 꺾여 오른쪽 아래 점 Q로 내려오고, Q에서 m이 왼쪽 아래로, k가 오른쪽 가로로 뻗음(m과 k 사이 160°, 아래). Q에서 오른쪽 위로 선분이 올라가 끝점에서 120°(아래 오른쪽)로 꺾여 n이 오른쪽 위로 뻗음. x는 Q 위쪽 두 선분 사이"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 꺾인 평행선 각 표시 도형",
    note="l∥k → ∠(k, QP)=135°, m∥n → ∠(k, QR)=80° → x=135°−80°=55°. 빠른정답 '1'과 불일치.")

# ---------------- p40
add(id="8dcedd84", qtype="short",
    question="다음 그림에서 [[par(l, m)]], [[par(k, n)]]일 때, [[angle(x)]]의 모든 엇각의 크기의 합을 구하시오.",
    choices=None, derived_answer=None,
    figure=U("거의 세로인 평행선 l, m(왼쪽·오른쪽)과 가로 평행선 k, n(위·아래), 왼쪽 위에서 오른쪽 아래로 내려가는 대각선 한 개. l과 k의 교점 왼쪽 위 80°, m과 대각선의 교점 아래 오른쪽 x, 대각선과 n의 교점 위 왼쪽 40°"),
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 평행선 4개·대각선 각 표시 도형",
    note="엇각의 범위(내부 엇각만/모든 교점) 해석에 따라 240° 또는 280°로 갈려 답 미도출. 빠른정답 deg(270).")

# ---------------- p42
add(id="6f05b59d", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x)]]의 크기는?",
    choices=DEGS(45, 50, 55, 60, 65), derived_answer="⑤",
    figure=U("평행선 l(위), m(아래). l 위 한 점에서 두 직선이 m으로 내려가 삼각형을 만듦. 왼쪽 직선과 m의 교점 위 왼쪽 135°, 오른쪽 직선과 m의 교점 아래 오른쪽 70°, l 위 꼭짓점 아래에 x"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·삼각형 각 표시 도형",
    note="밑각 45°, 70° → x=65° ⑤. 빠른정답 deg(55)와 불일치.")

# ---------------- p43
add(id="e233f49e", qtype="choice",
    question="다음 그림에서 [[par(l, n)]], [[par(m, n)]]일 때, [[angle(x)]]의 크기는?",
    choices=DEGS(30, 35, 40, 45, 50), derived_answer="③",
    figure=U("가로 평행선 l, m, n(위→아래). l 위 한 점에서 두 직선이 교차해 아래로 내려감. 왼쪽 직선과 n의 교점 위 왼쪽 100°, 오른쪽 직선과 m의 교점 아래 오른쪽 60°, l 위 교점 아래 두 직선 사이 x(초록)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선 3개·삼각형 각 표시 도형",
    note="x=180°−80°−60°=40° ③. 빠른정답 deg(480)과 불일치.")

# ---------------- p45
add(id="a95132be", qtype="short",
    question=("다음 그림과 같은 삼각형 ABC에서 [[angle(B)]]와 [[angle(C)]]의 이등분선의 교점을 P라 하자. "
              "[[angle(ADE) = deg(76)]], [[angle(AED) = deg(56)]]이고 [[par(seg(BC), seg(DE))]]일 때, [[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(114)",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 AB 위, E는 AC 위, DE∥BC, P는 DE 위의 점으로 BP·CP가 각각 ∠B·∠C의 이등분선(B에 점 2개, C에 × 2개 표시). ∠ADE=76°, ∠AED=56°, x=∠BPC(P 아래)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·평행선·각의 이등분선 복합 도형",
    note="∠B=76°, ∠C=56° → x=180°−38°−28°=114°. 빠른정답 '5'와 불일치.")

# ---------------- p47
add(id="292640c7", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x)]]의 크기는?",
    choices=DEGS(15, 20, 25, 30, 35), derived_answer="④",
    figure=U("평행선 l(위), m(아래). l 위쪽 꼭짓점(각 40°)에서 두 변이 내려와 m 위에 밑변을 둔 삼각형. 오른쪽 변과 l의 교점 아래 오른쪽 x°+5°, 왼쪽 변과 m의 교점 위 오른쪽(삼각형 내각) 3x°+15°"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·삼각형 각 표시 도형",
    note="40+(3x+15)+(x+5)=180 → x=30 ④. 빠른정답 deg(85)와 불일치.")

# ---------------- p48
add(id="fa8e8c8c", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]이고, [[angle(BAC) = 2 angle(CAD)]], [[angle(ABD) = 2 angle(DBC)]]일 때, [[angle(x)]]의 크기는?",
    choices=DEGS(45, 60, 75, 90, 115), derived_answer="②",
    figure=U("평행선 l(위, 점 A·D), m(아래, 점 B·C). 선분 AB, AC, BD; AC와 BD의 교점 E, x는 E의 오른쪽(∠CED)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·교차 선분 도형",
    note="3a+3b=180 → ∠AEB=180−2(a+b)=60°=x(맞꼭지각) ②. 빠른정답 deg(114)와 불일치.")

# ---------------- p49
add(id="b624c81f", qtype="short",
    question=("다음 그림에서 XX′∥YY′이고 [[angle(CAB)]] = 5∠CAX′, [[angle(CBA)]] = 5∠CBY′일 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(30)",
    figure=U("가로 직선 XX′(위, A 포함), YY′(아래, B 포함), A와 B를 지나는 횡단선, 오른쪽 점 C와 삼각형 ABC, x=∠ACB"),
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 평행선·삼각형 도형 / 프라임 점 라벨(X′, Y′) 문법 범위 밖 — 직선 기호·각 표기를 텍스트 혼합",
    note="원문은 XX′, YY′ 위에 직선 기호(양쪽 화살표). 6a+6b=180 → x=180−5(a+b)=30°. 빠른정답 deg(110)과 불일치.")

# ---------------- p50
add(id="489c67c1", qtype="choice",
    question=("다음 그림에서 [[par(l, m)]]이고 [[angle(PAB) = angle(BAD)]], [[angle(DCB) = angle(BCQ)]], "
              "[[angle(ADC) = deg(134)]]일 때, [[angle(x)]]의 크기는?"),
    choices=DEGS(59, 61, 63, 65, 67), derived_answer="⑤",
    figure=U("평행선 l(위, 점 P·A), m(아래, 점 Q·C). 화살촉 모양 사각형 ABCD: B 왼쪽(x), D 오른쪽 안쪽(134°, 오른쪽), A에 점 2개·C에 × 2개 같은 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·오목사각형 각 표시 도형",
    note="2a+2c=134 → x=a+c=67° ⑤. 빠른정답 '4'와 불일치.")

# ---------------- p51
add(id="73a40b56", qtype="short",
    question="다음 그림에서 [[par(l, m)]]이고 [[angle(PAB) = angle(BAD)]], [[angle(DCB) = angle(BCQ)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(67)",
    figure=U("평행선 l(위, 점 A·P), m(아래, 점 C·Q). 화살촉 모양 사각형 ABCD: D 왼쪽 안쪽(∠ADC=134°, 왼쪽에 표시), B 오른쪽(x), A에 점 2개·C에 ○ 2개 같은 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·오목사각형 각 표시 도형(134°는 그림에만 있음)",
    note="그림의 ∠ADC=134° → 2a+2c=134 → x=67°. 빠른정답 '2'와 불일치.")

# ---------------- p52
add(id="bbfe9568", qtype="short",
    question=("다음 그림에서 [[par(l, m)]]이고 [[angle(BAC) = frac(4,5) angle(BAD)]], [[angle(ABC) = frac(4,5) angle(ABE)]]일 때, "
              "[[angle(ACB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(36)",
    figure=U("평행선 l(위, 점 D·A), m(아래, 점 E·B), A와 B를 지나는 횡단선, 왼쪽 점 C와 삼각형 ABC, C에 각 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·삼각형 도형",
    note="∠BAD+∠ABE=180 → ∠BAC+∠ABC=144 → ∠ACB=36°. 빠른정답 deg(30)과 불일치.")

# ---------------- p53
add(id="46c0f1a5", qtype="short",
    question="다음 그림에서 [[par(l, n)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=U("평행선 l(위), n(아래). l 위 한 점 V에서 두 직선이 교차하며 위쪽 두 반직선 사이 50°. V에서 왼쪽 아래로 꺾은선이 내려가 꺾인 점(오른쪽 140°)을 지나 n과 만남(n 아래 왼쪽 110°). V에서 오른쪽 아래로 내려가는 직선과 l 사이(아래 오른쪽) x"),
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 평행선·꺾은선·교차 직선 각 표시 도형",
    note="∠(l, V→꺾인점)=110°(보조 평행선), 50° 빼서 x=60°. 빠른정답 '5'와 불일치.")

# ---------------- p54
add(id="0189f372", qtype="choice",
    question=("다음 그림에서 [[par(line(AB), line(CD))]]이고 [[angle(PQR) = deg(90)]], "
              "[[ratio(angle(BPQ), angle(DRQ)) = ratio(1, 5)]]일 때, [[angle(APQ)]]의 크기는?"),
    choices=DEGS(155, 160, 165, 170, 175), derived_answer="③",
    figure=U("가로 직선 AB(위, 점 A·P·B), CD(아래, 점 C·R·D), P에서 오른쪽 아래 Q로, Q에서 왼쪽 아래 R로 꺾인 선, Q에 직각 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·직각 꺾은선 도형",
    note="∠BPQ+∠DRQ=90° → ∠BPQ=15° → ∠APQ=165° ③. 빠른정답 deg(67)과 불일치.")

# ---------------- p58
add(id="09bf7b71", qtype="short",
    question="다음 그림에서 [[l]]∥l′일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(65)",
    figure=U("평행선 l(위), l′(아래). l에서 35°(아래 왼쪽)로 내려온 선이 왼쪽 점에서 꺾임(x, 오른쪽), 오른쪽 아래 점으로 내려가 다시 꺾임(80°, 왼쪽), l′로 내려가 만남(위 오른쪽 50°)"),
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 평행선 사이 지그재그 각 표시 도형 / 프라임 라벨(l′) 문법 범위 밖 — 텍스트 혼합",
    note="x=35°+(80°−50°)=65°. 빠른정답 deg(230)과 불일치.")

# ---------------- p59
add(id="10b64846", qtype="short",
    question="다음 그림에서 [[par(l, m)]]일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="85",
    figure=U("오른쪽 위로 기울어진 평행선 l(위), m(아래). l과 만나는 선분(교점 위 오른쪽 45°)이 내려가 직각으로 꺾이고, 다시 꺾인 점(왼쪽 아래 x°)을 지나 m과 만남(교점 아래 왼쪽 40°)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 기울어진 평행선·직각 지그재그 도형",
    note="x=45+40=85. 빠른정답 deg(190)과 불일치.")

# ---------------- p61
add(id="3c666175", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x) + angle(y)]]의 크기는?",
    choices=DEGS(95, 96, 97, 98, 99), derived_answer="③",
    figure=U("평행선 l(위), m(아래). l에서 32°(아래 왼쪽)로 내려온 선이 왼쪽 점에서 꺾임(x, 오른쪽), 오른쪽 아래 점에서 다시 꺾임(65°, 왼쪽), m과 만남(위 오른쪽 y)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선 사이 지그재그 각 표시 도형",
    note="x=32°+(65°−y) → x+y=97° ③. 빠른정답 deg(65)와 불일치.")

# ---------------- p63
add(id="d224b224", qtype="choice",
    question="다음 그림에서 [[par(l, m)]], [[par(p, q)]]일 때, [[angle(x) + angle(y)]]의 크기는?",
    choices=DEGS(140, 145, 150, 155, 160), derived_answer=None,
    figure=U("가로 평행선 l(위), m(아래), 오른쪽 위로 기울어진 평행선 p, q. p와 l의 교점 아래 왼쪽 60°, 그 교점에서 오른쪽 아래로 내려가는 직선(l과 25°)이 q의 위 끝점 X와 만남(X 아래 오른쪽 x). q 위 점 Y에서 오른쪽 아래로 선분이 m과 만남(교점 위 오른쪽 125°), Y 위 오른쪽 y"),
    difficulty_est=3, confidence=0.7,
    needs_review="도형 표현 불가: 평행선 2쌍·삼각형 복합 각 표시 도형",
    note="그림대로 계산하면 x=95°, y=115°(합 210°)로 선지에 없어 답 미도출. 빠른정답 '50'.")

# ---------------- p65
add(id="38b29052", qtype="choice",
    question="그림에서 두 직선 [[l]]과 [[m]]은 서로 평행하다. [[angle(x) - angle(y)]]의 크기는?",
    choices=DEGS(90, 105, 120, 135, 150), derived_answer="③",
    figure=U("평행선 l(위), m(아래). l에서 35°(아래 왼쪽)로 내려온 선이 왼쪽 점에서 꺾임(95°, 오른쪽), 아래 점에서 다시 꺾임(x, 위 오른쪽), m과 만남(위 왼쪽 y)"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 평행선 사이 지그재그 각 표시 도형",
    note="출처 [2006년 3월 고1 8번]. x=120°+y → x−y=120° ③. 빠른정답 '3' ✓.")

# ---------------- p67
add(id="e57ce8f3", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x)]]의 크기는?",
    choices=DEGS(90, 95, 100, 105, 110), derived_answer="③",
    figure=U("평행선 l(위), m(아래). l에서 30°(아래 왼쪽)로 내려온 선이 꺾임(135°, 오른쪽), 아래 점에서 다시 꺾임(x, 오른쪽), m과 만남(위 왼쪽 25°)"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 평행선 사이 지그재그 각 표시 도형",
    note="보조 평행선: 첫 꺾인 점에서 135°−30°=105° → x=(180°−105°)+25°=100° ③. 빠른정답 '3' ✓.")

# ---------------- p68
add(id="f027734f", qtype="short",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(a) + angle(b) + angle(c) + angle(d)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(540)",
    figure=U("평행선 l(위), m(아래). l에서 왼쪽 아래로 내려가는 꺾은선: l과의 교점 아래 오른쪽 a, 첫 꺾인 점 오른쪽 b, 둘째 꺾인 점 오른쪽 c, m과의 교점 위 오른쪽 d"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 평행선 사이 꺾은선 각 표시 도형",
    note="평행선 사이 내각 4개 합 = 180°×3 = 540°. 빠른정답 deg(540) ✓.")

# ---------------- p69
add(id="6ee08a0b", qtype="short",
    question="다음 그림에서 [[par(l, m)]]일 때,\n[[angle(a) + angle(b) + angle(c) + angle(d) + angle(e) + angle(f)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(900)",
    figure=U("평행선 l(위), m(아래). l에서 왼쪽 아래로 내려가는 꺾은선(꺾인 점 4개): l과의 교점 아래 오른쪽 a, 꺾인 점들 오른쪽에 b, c, d, e, m과의 교점 위 오른쪽 f"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 평행선 사이 꺾은선 각 표시 도형",
    note="내각 6개 합 = 180°×5 = 900°. 빠른정답 deg(900) ✓.")

# ---------------- p71
add(id="5b8d4473", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x)]]의 크기는?",
    choices=DEGS(42, 46, 50, 54, 58), derived_answer="②",
    figure=U("거의 세로인 평행선 l(왼쪽), m(오른쪽). l 위 점 P에서 왼쪽 아래 점 A로 선분(P에서 l 아래쪽과 32°), A에서 41°로 벌어진 선분이 오른쪽 위로 l을 지나 점 Q(직각 표시)까지, Q에서 오른쪽 아래 점 C(x)로, C에서 오른쪽 위 m 위 점 D로(D에서 m 아래쪽과 29°)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 세로 평행선·직각 꺾은선 각 표시 도형",
    note="방향각 계산: x=46° ②. 빠른정답 deg(540)과 불일치.")

# ---------------- p72
add(id="5eaf592f", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x)]]의 크기는?",
    choices=DEGS(17, 18, 19, 20, 21), derived_answer="②",
    figure=U("왼쪽 가로 반직선 l의 오른쪽 끝점 E에서 꺾은선이 왼쪽 위로 출발(l과 x), 점 D(5∠x)에서 위로, 꼭대기 A(4∠x)에서 오른쪽 아래로, B(9∠x)에서 더 아래로, C(7∠x)에서 m이 오른쪽 가로로 뻗음"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행 반직선 사이 꺾은선 각 표시 도형",
    note="방향각 누적: m과 마지막 변 사이 각 17x−180°=7x → x=18° ②. 빠른정답 deg(900)과 불일치.")

# ---------------- p75
add(id="90b27d57", qtype="choice",
    question=("다음 그림에서 [[par(l, m)]]이고 [[angle(CED) = 2 angle(BAC)]], [[angle(ACF) = 5 angle(ECF)]]이다. "
              "[[angle(BAC) + angle(ECF) = deg(75)]]일 때, [[angle(BAC)]]의 크기는?"),
    choices=DEGS(35, 37, 40, 41, 43), derived_answer="③",
    figure=U("평행선 l(위, 점 A·B), m(아래, 점 D·E·F). 선분 AC, BC가 아래 점 C에서 만나고 C에서 CE, CF가 m으로 내려감. A에 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·교차 선분 도형",
    note="∠ACF=180°−a+e=5e, a+e=75 → e=35°, a=40° ③. 빠른정답 '2'와 불일치.")

# ---------------- p76
add(id="d07e8a3f", qtype="short",
    question="다음 그림에서 [[par(l, m)]]이고 [[ratio(angle(x), angle(y)) = ratio(5, 4)]]일 때, [[angle(x) - angle(y)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(20)",
    figure=U("평행선 l(위), m(아래). l을 지나는 직선(l 위 오른쪽 x)이 아래로 내려가 점에서 40°로 꺾여 오른쪽 위로, 15°로 꺾여 아래로, 직각으로 꺾여 오른쪽으로, 55°로 꺾여 왼쪽 아래로 m을 지나 아래 점(60°)에서 왼쪽 위로 올라가 m과 만남(m 아래 오른쪽 y)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·다중 꺾은선 각 표시 도형",
    note="꺾은선 각을 모두 따라가면 x+y=180° → x=100°, y=80° → 20°. 빠른정답 deg(25)와 불일치.")

# ---------------- p77
add(id="4171eca5", qtype="choice",
    question=("다음 그림에서 [[par(l, m)]]이고 [[angle(CED) = 2 angle(BAC)]], [[angle(ACF) = 4 angle(ECF)]]이다. "
              "[[angle(BAC) + angle(ECF) = deg(98)]]일 때, [[angle(BAC)]]의 크기는?"),
    choices=DEGS(53, 54, 55, 56, 57), derived_answer="⑤",
    figure=U("평행선 l(위, 점 A·B), m(아래, 점 D·E·F). 선분 AC, BC가 아래 점 C에서 만나고 C에서 CE, CF가 m으로 내려감. A에 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·교차 선분 도형",
    note="180°−a=3e, a+e=98 → e=41°, a=57° ⑤. 빠른정답 deg(40)과 불일치.")

# ---------------- p79
add(id="bd821200", qtype="short",
    question="다음 그림에서 [[par(l, m)]]이고, [[quad(ABCD)]]가 정사각형일 때, [[x]]의 값을 구하시오.",
    choices=None, derived_answer="25",
    figure=U("평행선 l(위), m(아래). 정사각형 ABCD가 기울어져 A는 l 위, C는 m 위, B 왼쪽, D 오른쪽. A에서 l 오른쪽과 AD 사이 x°+10°, C에서 m 오른쪽과 CD 사이 2x°+5°"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행선 사이 기울어진 정사각형 도형",
    note="(x+10)+(2x+5)=90 → x=25. 빠른정답 deg(20)과 불일치.")

# ---------------- p83
add(id="3a376d43", qtype="short",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(77)",
    figure=U("평행선 l(위), m(아래). l 위 점에서 왼쪽 아래로 내려가는 직선(l 아래 왼쪽 22°)이 점 A를 지나 연장되고, A에서 그 연장선과 30° 벌어진 선분이 왼쪽 아래 점 B(오른쪽 x)로, B에서 오른쪽 아래로 m을 지나는 직선(m 위 오른쪽 155°)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·꺾은선 각 표시 도형",
    note="B→A 방향 52°, B→Q 방향 −25° → x=77°. 빠른정답 deg(60)과 불일치.")

# ---------------- p84
add(id="28069448", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(a) + angle(b) + angle(c) + angle(d)]]의 값은?",
    choices=DEGS(135, 136, 137, 138, 139), derived_answer="⑤",
    figure=U("평행선 l(위), m(아래). l을 지나 오른쪽 위로 뻗는 직선(l 위 오른쪽 a)이 왼쪽 아래로 내려가며 세 번 꺾임. 각 꺾인 점마다 이전 방향 연장선과 새 방향 사이에 b, c, d 표시, 마지막 선이 m과 만나 아래 오른쪽 41°"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·꺾은선 외각 표시 도형",
    note="a+b+c+d = 180°−41° = 139° ⑤. 빠른정답 deg(25)와 불일치.")

# ---------------- p86
add(id="0445f9b0", qtype="short",
    question=("교섭이가 A지점에서 출발하여 B지점까지 공원을 도는데 다음 그림과 같이 방향을 네 번 바꾸었다. "
              "[[par(l, m)]]일 때, [[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(87)",
    figure=U("평행선 l(위, 점 A, 사람 그림)과 m(아래, 점 B). A에서 왼쪽으로 가다 43° 꺾어 왼쪽 아래로, 31° 더 꺾어 아래로, 13° 더 꺾어 내려가 m과 만난 뒤 오른쪽으로 B까지. 각 꺾인 점에 이전 방향 점선과 각 표시, m 위 꺾인 점에 x"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 경로 꺾은선·평행선 각 표시 도형(사람 삽화 포함)",
    note="43°+31°+13°=87°=x. 빠른정답 deg(77)과 불일치.")

# ---------------- p88
add(id="cea1aadd", qtype="choice",
    question="다음 그림에서 [[par(l, m)]]일 때, [[angle(a) + angle(b) + angle(c) + angle(d)]]의 크기는?",
    choices=DEGS(140, 150, 160, 170, 180), derived_answer="①",
    figure=U("평행선 l(위), m(아래). l 위 점에서 왼쪽 아래로 내려가는 꺾은선: l과의 교점 아래 왼쪽 a, 꺾인 점마다 이전 방향 연장선과의 각 b, c, d, 마지막 선이 오른쪽 아래로 m과 만나 위 왼쪽 40°"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행선·꺾은선 외각 표시 도형",
    note="a+b+c+d = 180°−40° = 140° ①. 빠른정답 deg(118)과 불일치.")

# ---------------- p94
add(id="bec9b65a", qtype="short",
    question="다음 그림과 같이 폭이 일정한 종이테이프를 좌우대칭인 모양으로 접으면 [[angle(DGE) = deg(80)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(65)",
    figure=U("초록 종이테이프: 위 변 AB, 점선 CF(C, D, E, F 순) 아래 변, 왼쪽은 접는 선 AC로 접혀 아래로(끝 H), 오른쪽은 BF로 접혀 아래로(끝 I), 두 접힌 부분이 G에서 만남(∠DGE=80°). C와 F에 x 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 접은 종이테이프 도형",
    note="∠GDE=50° → 2x=180°−50° → x=65°. 빠른정답 deg(122)와 불일치.")

# ---------------- p97
add(id="d907f1e0", qtype="short",
    question="다음 그림과 같은 직사각형 모양의 종이 테이프를 접었다. [[angle(DAB) = deg(60)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=U("분홍 직사각형 테이프 EAD(위 변, D쪽은 점선), 아래 변 위 점 C, B. 접는 선 AB로 오른쪽 부분을 아래로 접어 연한 분홍 사각형이 됨. A에서 AD와 AB 사이 60°, C에서 CA와 CB 사이 x"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 접은 종이테이프 도형",
    note="∠CAB=60°(접음), ∠ABC=60°(엇각) → x=60°. 빠른정답 deg(65)와 불일치.")

# =====================================================================
# 다각형의 내각과 외각
# =====================================================================

# ---------------- p12
add(id="4a5d6c90", qtype="short",
    question=("다음 그림과 같이 반지름의 길이가 7인 원 O가 있다. 이 원의 원주를 12등분 한 점을 차례대로 "
              "[[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A,12)]]라 할 때, 이 점들을 순서대로 연결하여 만든 다각형의 "
              "대각선 중에서 길이가 14보다 짧은 대각선의 개수를 구하시오."),
    choices=None, derived_answer="48",
    figure=U("원 O, 반지름 7(점선 OA₄), 원 위의 점 A₁(위), A₂, A₃, A₄(왼쪽), A₁₂(오른쪽 위) 표시, 이웃한 점을 잇는 선분, 나머지는 ⋮"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원 위 12등분점 도형",
    note="정12각형 대각선 54개 중 지름(길이 14) 6개를 빼면 48. 빠른정답 '16'과 불일치.")

# ---------------- p27
add(id="8432e87e", qtype="short",
    question=("4 이상의 자연수 [[n]]에 대하여 [[f(n)]] = (정[[n]]각형의 서로 다른 길이의 대각선의 개수)라 할 때, "
              "[[f(n + 1) = -f(n) + 11]]을 만족시키는 자연수 [[n]]의 값을 구하시오."),
    choices=None, derived_answer="13", figure=None,
    difficulty_est=3, confidence=0.85,
    note="f(n)=[n/2]−1 → f(n)+f(n+1)=n−2=11 → n=13 (f(13)=5, f(14)=6). 빠른정답 '4'와 불일치.")

# ---------------- p38
add(id="5299deaf", qtype="choice",
    question="다음 그림에서 [[angle(x)]]의 크기는?",
    choices=DEGS(35, 40, 45, 50, 55), derived_answer="②",
    figure=U("사각형 ABCD(B 왼쪽 아래, C 오른쪽 아래, A는 B 위쪽, D는 A 오른쪽). BA의 연장선(A 위로)과 AD 사이 40°, ∠ADC=110°, ∠ABC=70°, x=∠BCD"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 사각형 각 표시 도형",
    note="∠A=140° → x=360−140−70−110=40° ②. 빠른정답 없음.")

# ---------------- p43
add(id="2433f30a", qtype="short",
    question=("다음 그림에서 점선은 빛이 네 개의 평면거울 [[seg(AB)]], [[seg(BC)]], [[seg(CD)]], [[seg(DA)]]에서 반사된 것을 나타낸다. "
              "[[angle(x)]] : [[angle(y)]] : [[angle(z)]] : [[angle(w)]] = 2 : 4 : 5 : 7일 때, [[angle(C)]]의 크기를 구하시오. "
              "(단, 입사각과 반사각의 크기는 같다.)"),
    choices=None, derived_answer="deg(90)",
    figure=U("사각형 ABCD(A 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), 내부 점선 빛 경로가 AB(x), DA(w), CD(z), BC(y) 위의 점에서 반사되며 닫힌 사각형을 이룸"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형·반사 경로 도형",
    note="각 꼭짓점 삼각형에서 x+y+z+w=180° → y=40°, z=50° → ∠C=180−40−50=90°. 빠른정답 없음.")

# ---------------- p44
add(id="560ce3d0", qtype="short",
    question=("다음 그림에서 점선은 빛이 네 개의 평면거울 [[seg(AB)]], [[seg(BC)]], [[seg(CD)]], [[seg(DA)]]에서 반사된 것을 나타낸다. "
              "[[angle(x)]] : [[angle(y)]] : [[angle(z)]] : [[angle(w)]] = 1 : 4 : 6 : 7일 때, [[angle(C)]]의 크기를 구하시오. "
              "(단, 입사각과 반사각의 크기는 같다.)"),
    choices=None, derived_answer="deg(80)",
    figure=U("사각형 ABCD(A 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽, CD 짧음), 내부 점선 빛 경로가 AB(x), DA(w), CD(z), BC(y) 위의 점에서 반사되며 닫힌 사각형을 이룸"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형·반사 경로 도형",
    note="x+y+z+w=180° → y=40°, z=60° → ∠C=80°. 빠른정답 '1'과 불일치.")

# ---------------- p45
add(id="ba000b41", qtype="short",
    question=("다음 그림에서 점선은 빛이 네 개의 평면거울 [[seg(AB)]], [[seg(BC)]], [[seg(CD)]], [[seg(DA)]]에서 반사된 것을 나타낸다. "
              "[[angle(x)]] : [[angle(y)]] : [[angle(z)]] : [[angle(w)]] = 1 : 3 : 5 : 7일 때, [[angle(C)]]의 크기를 구하시오. "
              "(단, 입사각과 반사각의 크기는 같다.)"),
    choices=None, derived_answer="deg(90)",
    figure=U("사각형 ABCD(A 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽), 내부 점선 빛 경로가 AB(x), DA(w), CD(z), BC(y) 위의 점에서 반사되며 닫힌 사각형을 이룸"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형·반사 경로 도형",
    note="x+y+z+w=180° → y+z=180×8/16=90° → ∠C=90°. 빠른정답 '2'와 불일치.")

# ---------------- p46
add(id="7bc02189", qtype="short",
    question="다음 그림에서 [[angle(x)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(88)",
    figure=U("사각형(왼쪽 변 세로). 왼쪽 위 꼭짓점 외각 100°(왼쪽 변 연장선과 윗변 사이), 왼쪽 아래 외각 87°, 오른쪽 아래 외각 85°(오른쪽 변 연장선과 아랫변 사이), 오른쪽 위 외각 x(윗변 연장선과 오른쪽 변 사이)"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 사각형 외각 표시 도형",
    note="외각의 합 360° → x=360−100−87−85=88°. 빠른정답 없음.")

# ---------------- p49
add(id="e0f4be7b", qtype="choice",
    question="다음 그림에서 [[angle(x)]]의 크기는?",
    choices=DEGS(80, 85, 90, 95, 100), derived_answer=None,
    figure=U("육각형. 위 왼쪽 꼭짓점 내각 130°, 위 오른쪽 꼭짓점 외각 45°, 오른쪽 꼭짓점 외각 95°, 아래 오른쪽 꼭짓점 외각 45°, 아래 왼쪽 꼭짓점 내각 125°, 왼쪽 꼭짓점 외각 x"),
    difficulty_est=2, confidence=0.7,
    needs_review="도형 표현 불가: 육각형 내각·외각 표시 도형",
    note="외각 합으로 계산하면 x=360−(50+45+95+45+55)=70°가 되어 선지에 없음 → 답 미도출. 빠른정답 없음.")

# ---------------- p51
add(id="a71d68da", qtype="choice",
    question="다음 그림에서 [[angle(x)]]의 크기는?",
    choices=DEGS(65, 68, 71, 74, 77), derived_answer="⑤",
    figure=U("육각형. 위 꼭짓점 직각 표시, 위 왼쪽 꼭짓점 내각 125°, 왼쪽 꼭짓점 외각 45°, 오른쪽 위 꼭짓점 내각 137°, 오른쪽 아래 꼭짓점 외각 50°, 아래 꼭짓점 외각 x(분홍)"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 육각형 내각·외각 표시 도형",
    note="외각 합: 90+55+45+43+50+x=360 → x=77° ⑤. 빠른정답 없음.")

# ---------------- p58
add(id="6952d4be", qtype="short",
    question=("다음 그림에서 [[angle(JOF) = deg(80)]]일 때,\n"
              "[[(angle(A) + angle(B) + angle(C) + angle(D) + angle(E) + angle(F)) - (angle(G) + angle(H) + angle(I) + angle(J))]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(280)",
    figure=U("육각형 ABCDEF(A 아래 왼쪽, B 왼쪽, C 위 왼쪽, D 위 오른쪽, E 오른쪽, F 아래 오른쪽) 안에 오각형 GHIJO(G 왼쪽, H 위 왼쪽, I 위 오른쪽, J 오른쪽, O 아래). A–O–J, F–O–G가 각각 한 직선, ∠JOF=80°, 각 꼭짓점에 각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 육각형 안 오각형 복합 도형",
    note="720° − (540° − ∠GOJ) = 720 − (540 − 100) = 280°. 빠른정답 없음.")

# ---------------- p81
add(id="9715d390", qtype="short",
    question=("다음 그림은 정삼각형 ABC의 두 변 AB, BC 위에 [[seg(BD) = seg(CE)]]가 되도록 두 점 D, E를 잡은 것이다. "
              "[[seg(AE)]], [[seg(CD)]]의 교점을 F라 할 때, [[angle(EFD)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(120)",
    figure=U("정삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D는 AB 위, E는 BC 위(BD=CE 같은 길이 표시), 선분 AE와 CD의 교점 F, F에 각 표시"),
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 정삼각형·교차 선분 도형",
    note="△ABE≡△CAD(SAS) → ∠AFC=180−∠BAC=120°=∠EFD. 빠른정답 없음.")

# ---------------- p90
add(id="2b06253f", qtype="short",
    question=("다음 그림과 같은 정육각형에서 [[seg(CG) = seg(DH)]]가 되도록 [[seg(CD)]], [[seg(DE)]] 위에 각각 두 점 G, H를 잡았을 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(120)",
    figure=U("정육각형 ABCDEF(A 위, B 왼쪽 위, C 왼쪽 아래, D 아래, E 오른쪽 아래, F 오른쪽 위), G는 CD 위, H는 DE 위(CG=DH 같은 길이 표시), 선분 BG와 CH의 교점 I, x는 I의 위 오른쪽(∠BIH)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정육각형·교차 선분 도형",
    note="△BCG≡△CDH(SAS) → ∠BIC=60° → x=∠BIH=120°. 빠른정답 없음.")

# ---------------- p91
add(id="1b23eb7f", qtype="short",
    question=("다음 그림과 같은 정팔각형에서 [[seg(CI) = seg(DJ)]]가 되도록 [[seg(CD)]], [[seg(DE)]] 위에 각각 두 점 I, J를 잡았을 때, "
              "[[angle(x)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(135)",
    figure=U("정팔각형 ABCDEFGH(A 위 왼쪽, H 위 오른쪽, G 오른쪽 위, F 오른쪽 아래, E 아래 오른쪽, D 아래 왼쪽, C 왼쪽 아래, B 왼쪽 위), I는 CD 위, J는 DE 위(CI=DJ 같은 길이 표시), 선분 BI와 CJ의 교점 K, x는 K의 위 오른쪽(∠BKJ)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정팔각형·교차 선분 도형",
    note="△BCI≡△CDJ(SAS) → ∠BKC=45° → x=∠BKJ=135°. 빠른정답 '4개'와 불일치.")

# ---------------- p93
add(id="0621bce8", qtype="choice",
    question="다음 그림과 같이 정오각형 ABCDE의 두 변 [[seg(CD)]]와 [[seg(AE)]]의 연장선의 교점을 F라 할 때, [[angle(x)]]의 크기는?",
    choices=DEGS(36, 40, 55, 60, 77), derived_answer="①",
    figure=U("정오각형 ABCDE(A 위, B 오른쪽 위, C 오른쪽 아래, D 아래 왼쪽, E 왼쪽 위), CD와 AE의 연장선이 왼쪽 점 F에서 만남, x=∠DFE"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 정오각형·연장선 도형",
    note="외각 72°×2 → x=180−144=36° ①. 빠른정답 없음.")

# ---------------- p95
add(id="3d4a1a92", qtype="choice",
    question=("아래의 그림과 같이 정오각형 ABCDE의 한 변 [[seg(BC)]]와 정팔각형 DEFGHIJK의 한 변 [[seg(JK)]]의 연장선의 교점을 "
              "L이라 할 때, 다음 중 옳지 않은 것은?"),
    choices=["[[angle(a) = deg(108)]]", "[[angle(b) = deg(135)]]", "[[angle(c) = deg(72)]]", "[[angle(d) = deg(45)]]", "[[angle(e) = deg(120)]]"],
    derived_answer="⑤",
    figure=U("정오각형 ABCDE(왼쪽)와 정팔각형 DEFGHIJK(오른쪽)가 변 DE를 공유. BC와 JK의 연장선의 교점 L(아래). a=∠ABC, b=∠DEF, c=∠DCL(C의 외각), d=∠DKL(K의 외각), e=∠CLK"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정오각형·정팔각형 복합 도형",
    note="사각형 CDKL에서 e=360−72−117−45=126° → ⑤ 틀림. 빠른정답 없음.")

# =====================================================================
# 부채꼴의 호의 길이와 넓이
# =====================================================================

# ---------------- p42
add(id="80cfd9aa", qtype="choice",
    question=("다음 그림에서 [[seg(AB) = seg(BC) = seg(CD)]]이고, [[seg(AD)]]는 원의 지름이다. [[seg(AD) = 15]] cm일 때, "
              "색칠한 부분의 둘레의 길이는?"),
    choices=["[[9 pi]] cm", "[[11 pi]] cm", "[[13 pi]] cm", "[[15 pi]] cm", "[[17 pi]] cm"], derived_answer="④",
    figure=U("지름 AD의 원, 지름 위 점 A, B, C, D 등간격(같은 길이 표시). AC를 지름으로 하는 위쪽 반원, BD를 지름으로 하는 아래쪽 반원, AB 아래 작은 반원, CD 위 작은 반원으로 둘러싸인 S자 모양 색칠"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 원·반원 복합 도형",
    note="5π+5π+2.5π+2.5π=15π ④. 빠른정답 '4' ✓.")

# ---------------- p55
add(id="65dffe93", qtype="choice",
    question="다음 그림과 같이 반지름의 길이가 3 cm인 반원과 [[angle(CAB) = deg(45)]]인 부채꼴에서 색칠한 부분의 넓이는?",
    choices=["[[(frac(9,2) pi - 9)]] cm²", "[[(frac(9,2) pi - 16)]] cm²", "[[(frac(9,4) pi + frac(9,2))]] cm²",
             "[[(frac(9,4) pi - frac(9,2))]] cm²", "[[(9 pi - 3)]] cm²"],
    derived_answer="④",
    figure=U("지름 AB(중심 O, OB=3cm)의 반원과 중심 A, 반지름 AB, 중심각 45°의 부채꼴 ABC. AC가 반원과 만나는 점 D. 호 CB, 호 DB, 선분 DC로 둘러싸인 부분 색칠(초록)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 반원·부채꼴 복합 도형",
    note="부채꼴(r=6, 45°)=9π/2, 빼는 부분(△ADB+활꼴)=9/2+9π/4 → 9π/4−9/2 ④. 빠른정답 '3'과 불일치.")

# ---------------- p57
add(id="4d18d8e6", qtype="choice",
    question="다음 그림은 직각삼각형 ABC의 각 변을 지름으로 하는 반원을 그린 것이다. 이때 색칠한 부분의 넓이는?",
    choices=["[[(48 - pi)]] cm²", "48 cm²", "54 cm²", "[[48 pi]] cm²", "[[54 pi]] cm²"], derived_answer="③",
    figure=U("직각삼각형 ABC(A 위, 직각, B 왼쪽 아래, C 오른쪽 아래), AB=9cm, AC=12cm, BC=15cm(점선 치수). AB, AC를 지름으로 하는 바깥쪽 반원과 BC를 지름으로 하는 반원 사이의 두 초승달 모양 색칠"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 직각삼각형·반원 3개 도형",
    note="히포크라테스의 초승달 → 삼각형 넓이 (1/2)·9·12=54 ③. 빠른정답 '4'와 불일치.")

# ---------------- p59
add(id="3d5394c4", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(30)]]이고 [[seg(AC) = 10]] cm, [[seg(BC) = 5]] cm인 직각삼각형 ABC를 꼭짓점 C를 중심으로 하여 "
              "[[par(seg(AC), seg(ED))]]가 되도록 회전시켰다. 색칠한 부분의 넓이가 [[a pi]] cm²일 때, [[4a]]의 값을 구하시오."),
    choices=None, derived_answer="125",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래 직각, C 오른쪽 아래), ∠A=30°, AC=10cm, BC=5cm. C를 중심으로 회전한 삼각형 DEC(E 직각, D 오른쪽 아래, ∠D=30°). A→D 점선 호(반지름 10), B→E 점선 호(반지름 5, 화살표). 두 호와 두 삼각형 사이 부분 색칠(분홍)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 회전한 직각삼각형·부채꼴 도형",
    note="회전각 150°, 넓이=(150/360)π(10²−5²)=125π/4 → a=125/4, 4a=125. 빠른정답 '3'과 불일치.")

# ---------------- p74
add(id="620dc80e", qtype="short",
    question=("다음 그림과 같이 반지름의 길이가 9 cm인 반원 O와 반지름의 길이가 6 cm인 반원 O′이 있다. 색칠한 두 부분의 넓이가 같을 때, "
              "[[angle(AOB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(80)",
    figure=U("지름 AC(중심 O, OA=9cm)의 큰 반원과 C를 오른쪽 끝으로 하는 반지름 6cm(중심 O′)의 작은 반원. 큰 반원 위 점 B, 부채꼴 AOB 중 작은 반원 밖 부분과 작은 반원 중 부채꼴 밖 부분 색칠(분홍)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 반원 2개·부채꼴 복합 도형",
    note="부채꼴 AOB=반원 O′=18π → 81π·θ/360=18π → θ=80°. 빠른정답 '3'과 불일치.")

# ---------------- p75
add(id="e4108c6f", qtype="short",
    question=("다음 그림과 같이 반지름의 길이가 8 cm인 반원 O와 반지름의 길이가 6 cm인 반원 O′이 있다. 색칠한 두 부분의 넓이가 같을 때, "
              "[[angle(AOB)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(101.25)",
    figure=U("지름 AC(중심 O, OA=8cm)의 큰 반원과 C를 오른쪽 끝으로 하는 반지름 6cm(중심 O′)의 작은 반원. 큰 반원 위 점 B, 부채꼴 AOB 중 작은 반원 밖 부분과 작은 반원 중 부채꼴 밖 부분 색칠(하늘색)"),
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 반원 2개·부채꼴 복합 도형",
    note="부채꼴 AOB=반원 O′=18π → 64π·θ/360=18π → θ=101.25°(정수 아님, 수치 변형 문항). 빠른정답 '4'와 불일치.")

# ---------------- p92
add(id="25b0c65c", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]] 위의 직각삼각형 ABC를 점 C를 중심으로 점 A가 점 A′에 오도록 회전시켰다. "
              "[[seg(AC) = 9]] cm, [[angle(ABC) = deg(50)]]일 때, 점 A가 움직인 거리는?"),
    choices=["[[5 pi]] cm", "[[6 pi]] cm", "[[7 pi]] cm", "[[8 pi]] cm", "[[9 pi]] cm"], derived_answer="③",
    figure=U("직선 l 위에 B, C, A′. 직각삼각형 ABC(A 위, 직각, ∠B=50°, AC=9cm 점선 치수)와 회전 후 삼각형(A′에서 직각, C를 공유), A에서 A′ 방향 화살표"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 회전한 직각삼각형 도형",
    note="∠ACB=40° → 회전각 140° → 2π·9·140/360=7π ③. 빠른정답 '4'와 불일치. 프라임 점 A′은 본문 텍스트로만 등장.")

# =====================================================================
# 히스토그램과 도수분포다각형
# =====================================================================

# ---------------- p98
add(id="1bc93ec1", qtype="choice",
    question=("다음은 어느 동아리의 여학생과 남학생의 수행 평가 점수를 조사하여 나타낸 도수분포다각형인데 일부가 구멍이 뚫려 보이지 않는다. "
              "여학생과 남학생 수는 서로 같고 점수가 25점 미만인 여학생은 동아리 전체 학생의 10%이다. "
              "남학생의 그래프와 가로축으로 둘러싸인 부분을 도수분포다각형의 가장 높은 점에서 가로축에 그은 수선으로 나누었을 때, "
              "왼쪽 도형의 넓이를 [[A]], 오른쪽 도형의 넓이를 [[B]]라 하자. [[A]] : [[B]]를 가장 간단한 자연수의 비로 나타내면 "
              "[[m]] : [[n]]이라 할 때, [[m + n]]의 값은?"),
    choices=["7", "8", "9", "10", "11"], derived_answer="①",
    figure=U("도수분포다각형: 가로축 점수 15~45(계급 폭 5), 세로축 명 0~12. 여학생(빨강): (17.5, 2), (22.5, 구멍), (27.5, 12), (32.5, 10), (37.5, 6), (42.5, 0). 남학생(파랑): (17.5, 0), (22.5, 3), (27.5, 6), (32.5, 12), (37.5, 9), (42.5, 구멍), (47.5, 0). 32.5에서 수선으로 나눈 왼쪽 A(초록), 오른쪽 B(보라)"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 도수분포다각형 그래프(구멍 포함)",
    note="여 20~25 구간 5명, 전체 70명, 남 40~45 구간 5명; A=75, B=100 → 3:4 → 7 ①. 빠른정답 없음.")

# =====================================================================
# 삼각형의 합동
# =====================================================================

# ---------------- p10
add(id="ed56c7fe", qtype="short",
    question="다음 그림에서 두 사각형 ABCD와 EFGH가 합동일 때, [[angle(D)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(100)",
    figure=U("사각형 ABCD(A 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래): AB=6cm, BC=9cm(점선 치수), ∠A=120°, C에 직각 표시. 사각형 EFGH(H 왼쪽 위, E 오른쪽 위, G 왼쪽 아래, F 오른쪽 아래): ∠F=50°"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 합동인 두 사각형 치수·각 표시 도형",
    note="∠B=∠F=50° → ∠D=360−120−50−90=100°. 빠른정답 '2'와 불일치.")

# ---------------- p12
add(id="090b93ba", qtype="short",
    question=("[[tri(ABC)]]와 [[tri(DEF)]]가 다음 세 조건을 만족시킬 때, [[angle(D)]]의 크기를 구하시오.\n"
              "(가) [[cong(tri(ABC), tri(DEF))]]\n(나) [[seg(AB) = seg(AC)]]\n(다) [[angle(C) = deg(65)]]"),
    choices=None, derived_answer="deg(50)", figure=None,
    difficulty_est=2, confidence=0.9,
    note="∠B=∠C=65° → ∠A=50°=∠D. 빠른정답 '3'과 불일치.")

# ---------------- p13
add(id="db98ca25", qtype="choice",
    question="다음 그림에서 [[cong(tri(ABC), tri(DEF))]]일 때, [[tri(ABC)]]의 넓이는?",
    choices=["6 cm²", "9 cm²", "12 cm²", "15 cm²", "18 cm²"], derived_answer="①",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래): AC=5cm, BC=3cm(점선 치수). 삼각형 DEF(E 위, D 왼쪽 아래, F 오른쪽): DE=4cm, E에 직각 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 합동인 두 삼각형 치수 도형",
    note="∠B=∠E=90°, AB=DE=4 → (1/2)·4·3=6 ①. 빠른정답 없음.")

# ---------------- p15
add(id="b936bf93", qtype="short",
    question=("다음 그림에서 [[seg(AB) = seg(AC)]]이고 [[angle(A) = deg(46)]]이다. 점 E는 [[seg(AC)]] 위의 점이고 "
              "[[cong(tri(ABC), tri(DEC))]]일 때, [[angle(ABE)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(10.5)",
    figure=U("이등변삼각형 ABC(A 위, B 왼쪽 아래, C 아래 가운데), ∠A=46°, E는 AC 위, D는 E 오른쪽(ED 가로), 삼각형 DEC, 선분 BE, B에 ∠ABE 표시"),
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 이등변삼각형·합동 삼각형 복합 도형",
    note="∠B=∠C=67°, CE=CB → ∠CBE=56.5° → ∠ABE=10.5°(정수 아님). 빠른정답 없음.")

# ---------------- p19
add(id="bcdf3a0a", qtype="choice",
    question="다음 그림에서 [[cong(tri(ABC), tri(DEF))]]일 때, [[angle(D)]]의 크기는?",
    choices=DEGS(40, 55, 65, 70, 75), derived_answer="⑤",
    figure=U("삼각형 ABC(A 위, B 왼쪽, C 오른쪽): ∠B=40°, ∠C=65°, BC=6cm. 삼각형 DEF(D 위, F 왼쪽, E 오른쪽): ∠E=40°, FE=6cm"),
    difficulty_est=1, confidence=0.9,
    needs_review="도형 표현 불가: 합동인 두 삼각형 각·치수 도형",
    note="∠D=∠A=180−40−65=75° ⑤. 빠른정답 '3 cm'와 불일치.")

# ---------------- p20
add(id="0d983463", qtype="short",
    question="다음 그림에서 [[cong(tri(ABC), tri(DEF))]]일 때, [[seg(DF)]]와 [[seg(EF)]]의 길이의 합을 구하시오.",
    choices=None, derived_answer="9.5 cm",
    figure=U("삼각형 ABC(A 위, B 왼쪽, C 오른쪽): AB=4cm, AC=4.5cm, BC=5cm, ∠B=59°, ∠C=49°. 삼각형 DEF(D 위, E 왼쪽, F 오른쪽): DE=4cm, ∠D=72°"),
    difficulty_est=1, confidence=0.9,
    needs_review="도형 표현 불가: 합동인 두 삼각형 각·치수 도형",
    note="DF=AC=4.5, EF=BC=5 → 9.5cm. 빠른정답 '50'과 불일치.")

# ---------------- p21
add(id="2535e18e", qtype="short",
    question="다음 그림에서 [[cong(tri(ABC), tri(DFE))]]일 때, [[angle(D)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(85)",
    figure=U("삼각형 ABC(A 위, B 왼쪽, C 오른쪽): AB=4.5cm, BC=5cm, ∠B=30°, ∠C=65°. 삼각형 DEF(D 위, E 왼쪽, F 오른쪽): DF=4.5cm, EF=5cm, ∠F=30°"),
    difficulty_est=1, confidence=0.9,
    needs_review="도형 표현 불가: 합동인 두 삼각형 각·치수 도형",
    note="∠D=∠A=180−30−65=85°. 빠른정답 '2'와 불일치.")

# ---------------- p22
add(id="7fc76d0b", qtype="choice",
    question="다음 그림에서 [[seg(AB) = seg(DC)]]이고 [[seg(AC) = seg(BD)]]일 때, 합동인 삼각형은 모두 몇 쌍인가?",
    choices=["1쌍", "2쌍", "3쌍", "4쌍", "5쌍"], derived_answer="③",
    figure=U("등변사다리꼴 모양 사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB=DC 같은 길이 표시, 대각선 AC와 BD의 교점 E"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각형·대각선 도형",
    note="△ABC≡△DCB, △ABD≡△DCA, △ABE≡△DCE → 3쌍 ③. 빠른정답 '5'와 불일치.")

# ---------------- p32
add(id="47c201c5", qtype="choice",
    question="다음 중 [[cong(tri(ABC), tri(DEF))]]가 성립하는 조건이 아닌 것은?",
    choices=["[[seg(AB) = seg(DE)]], [[seg(BC) = seg(EF)]], [[seg(CA) = seg(FD)]]",
             "[[seg(AB) = seg(DE)]], [[seg(BC) = seg(EF)]], [[angle(B) = angle(E)]]",
             "[[seg(AC) = seg(DF)]], [[angle(A) = angle(D)]], [[angle(C) = angle(F)]]",
             "[[seg(BC) = seg(EF)]], [[seg(CA) = seg(FD)]], [[angle(A) = angle(D)]]",
             "[[seg(BC) = seg(EF)]], [[angle(B) = angle(E)]], [[angle(C) = angle(F)]]"],
    derived_answer="④", figure=None,
    difficulty_est=2, confidence=0.9,
    note="④는 두 변과 끼인각이 아닌 각(SSA) → 합동 조건 아님. 빠른정답 '4' ✓.")

# ---------------- p34
add(id="c58320e5", qtype="choice",
    question=("아래 그림에서 [[seg(AC) = seg(DF)]], [[seg(BC) = seg(EF)]]일 때, 다음 중 [[cong(tri(ABC), tri(DEF))]]이기 위해 필요한 "
              "나머지 한 조건과 합동 조건을 짝지은 것으로 옳은 것을 모두 고르면? (정답 2개)"),
    choices=["[[seg(AB) = seg(DE)]], SSS 합동", "[[seg(AB) = seg(DF)]], SSS 합동", "[[angle(A) = angle(D)]], SAS 합동",
             "[[angle(C) = angle(F)]], SAS 합동", "[[angle(C) = angle(F)]], ASA 합동"],
    derived_answer="①, ④",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, AC 세로·BC 가로)와 삼각형 DEF(D 위, E 왼쪽 아래, F 오른쪽 아래). AC·DF 한 줄 표시, BC·EF 두 줄 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 두 삼각형 같은 길이 표시 도형",
    note="①(SSS), ④(끼인각 SAS) 옳음. 빠른정답 '2, 4, 5'와 불일치.")

# ---------------- p36
add(id="3895a4c0", qtype="choice",
    question=("[[tri(ABC)]]와 [[tri(DEF)]]에서 [[seg(AB) = seg(DE)]], [[angle(A) = angle(D)]]일 때, "
              "[[cong(tri(ABC), tri(DEF))]]이기 위한 나머지 한 조건이 될 수 있는 것을 모두 고르면? (정답 3개)"),
    choices=["[[seg(BC) = seg(EF)]]", "[[seg(AC) = seg(DF)]]", "[[angle(B) = angle(E)]]", "[[angle(C) = angle(F)]]", "[[seg(AC) = seg(EF)]]"],
    derived_answer="②, ③, ④",
    figure=U("삼각형 ABC(C 위, A 왼쪽 아래, B 오른쪽 아래)와 삼각형 DEF(F 위, D 왼쪽 아래, E 오른쪽 아래). A와 D에 각 표시, AB·DE 같은 길이 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 두 삼각형 각·길이 표시 도형",
    note="②SAS, ③ASA, ④(두 각 → ASA). 빠른정답 '3'과 불일치(부분).")

# ---------------- p38
add(id="9c9eb4fb", qtype="choice",
    question=("아래 그림의 [[tri(ABC)]]와 [[tri(DEF)]]에서 [[seg(AB) = seg(DE)]], [[angle(A) = angle(D)]]일 때, 다음 중 "
              "[[cong(tri(ABC), tri(DEF))]]가 되기 위한 조건이 아닌 것을 모두 고르면? (정답 2개)"),
    choices=["[[seg(BC) = seg(EF)]]", "[[seg(CA) = seg(FD)]]", "[[angle(B) = angle(E)]]", "[[angle(C) = angle(F)]]", "[[angle(A) = angle(F)]]"],
    derived_answer="①, ⑤",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽)와 삼각형 DEF(D 위, E 왼쪽 아래, F 오른쪽). A와 D에 각 표시, AB·DE 같은 길이 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 두 삼각형 각·길이 표시 도형",
    note="①(SSA), ⑤(대응하지 않는 각)는 조건 아님. 빠른정답 '5'와 부분 일치.")

# ---------------- p39
add(id="267e2b9a", qtype="choice",
    question=("아래 그림의 두 삼각형에서 [[seg(AB) = seg(DE)]]이다. 다음 중 [[cong(tri(ABC), tri(DEF))]]가 되기 위하여 "
              "더 필요한 조건이 아닌 것은?"),
    choices=["[[seg(BC) = seg(EF)]], [[seg(AC) = seg(DF)]]", "[[seg(BC) = seg(EF)]], [[angle(B) = angle(E)]]",
             "[[angle(A) = angle(D)]], [[angle(B) = angle(E)]]", "[[seg(AC) = seg(DF)]], [[angle(A) = angle(D)]]",
             "[[seg(BC) = seg(EF)]], [[angle(C) = angle(F)]]"],
    derived_answer="⑤",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)와 삼각형 DEF(D 위, E 왼쪽 아래, F 오른쪽 아래). AB·DE 같은 길이 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 두 삼각형 길이 표시 도형",
    note="⑤는 SSA → 합동 조건 아님. 빠른정답 '2, 3, 4'와 불일치.")

# ---------------- p40
add(id="c78c0116", qtype="choice",
    question=("다음 그림의 [[tri(ABC)]]와 [[tri(DEF)]]는 [[seg(AB) = seg(DE)]], [[angle(A) = angle(D)]]인 삼각형이다. "
              "여기에 어떤 조건이 더 주어지면 두 삼각형은 합동이 된다. 다음 중 조건이 될 수 없는 것은?"),
    choices=["[[angle(B) = angle(E)]]", "[[seg(BC) = seg(EF)]]", "[[seg(AC) = seg(DF)]]", "[[angle(C) = angle(F)]]",
             "[[seg(AC) = seg(DF)]], [[seg(BC) = seg(EF)]]"],
    derived_answer="②",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)와 삼각형 DEF(D 위, E 왼쪽 아래, F 오른쪽 아래). A와 D에 점 표시(같은 각), AB·DE 같은 길이 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 두 삼각형 각·길이 표시 도형",
    note="②는 SSA → 조건 불가. 빠른정답 '1, 3'과 불일치.")

# ---------------- p42
add(id="1a1477bc", qtype="short",
    question=("아래 그림에서 [[seg(AB) = seg(DE)]], [[seg(AC) = seg(DF)]]일 때, 다음 보기 중 [[tri(ABC)]]와 [[tri(DEF)]]가 SSS 합동이 되기 위해 "
              "필요한 나머지 한 조건을 고르시오.\n<보기>\n"
              "ㄱ. [[seg(BC) = seg(DE)]]\nㄴ. [[angle(B) = angle(E)]]\nㄷ. [[angle(A) = angle(D)]]\nㄹ. [[angle(C) = angle(F)]]\nㅁ. [[seg(BC) = seg(EF)]]"),
    choices=None, derived_answer="ㅁ",
    figure=U("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)와 삼각형 DEF(D 위, E 왼쪽 아래, F 오른쪽 아래). AB·DE 두 줄 표시, AC·DF 한 줄 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 두 삼각형 길이 표시 도형",
    note="나머지 한 변 BC=EF → ㅁ. 빠른정답 '5'(=다섯째 항목 ㅁ).")

# ---------------- p43
add(id="4abb47a4", qtype="choice",
    question=("다음은 [[angle(XOY)]]와 크기가 같고 반직선 PQ를 한 변으로 하는 각을 작도하였을 때, [[cong(tri(AOB), tri(CPD))]]임을 보이는 과정이다. "
              "(가), (나), (다)에 알맞은 것을 차례대로 구한 것은?\n"
              "[[tri(AOB)]]와 [[tri(CPD)]]에서\n"
              "[[seg(OA)]] = (가), [[seg(OB) = seg(PD)]], [[seg(AB)]] = (나)\n"
              "∴ [[cong(tri(AOB), tri(CPD))]] ((다) 합동)"),
    choices=["[[seg(PC)]], [[seg(CD)]], SSS", "[[seg(PC)]], [[seg(CD)]], SAS", "[[seg(PC)]], [[seg(PD)]], ASA",
             "[[seg(PQ)]], [[seg(CD)]], SSS", "[[seg(PQ)]], [[seg(PD)]], SAS"],
    derived_answer="①",
    figure=U("작도 그림: 각 XOY(O 왼쪽, X 위 오른쪽, Y 오른쪽)에서 O 중심 호가 OX·OY와 만나는 점 A·B, 반직선 PQ(P 왼쪽)에서 P 중심 같은 반지름 호와 D, D 중심 AB 길이 호와 만나는 점 C, 반직선 PC"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 각의 작도 그림",
    note="OA=PC, AB=CD, SSS ①. 빠른정답 '2'와 불일치.")

# ---------------- p44
add(id="91f0251a", qtype="short",
    question=("다음 그림은 삼각형 2개를 붙여놓은 도형이다. 두 삼각형이 합동이고 [[seg(BC) = seg(AB) + 3]]일 때, "
              "삼각형 ABC와 삼각형 EBD의 합동조건을 구하시오."),
    choices=None, derived_answer="SSS 합동",
    figure=U("점 B(왼쪽), A(위), C(오른쪽), E(BC 위), D(오른쪽 아래). 삼각형 ABC와 삼각형 EBD, 점선 치수 AB=7, AC=4, EC=3, ED=4, BD=10"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 붙여 놓은 두 삼각형 치수 도형",
    note="BC=10=BD, BE=7=AB, ED=4=AC → 세 변이 각각 같음(SSS). 빠른정답 없음.")

# ---------------- p45
add(id="3e187a17", qtype="choice",
    question="아래 그림과 같은 사각형 ABCD에서 [[seg(AB) = seg(AD)]], [[seg(BC) = seg(DC)]]일 때, 다음 중 옳지 않은 것을 모두 고르면? (정답 2개)",
    choices=["[[seg(AB) = seg(AD)]]", "[[angle(BAD) = 2 angle(BCA)]]", "[[angle(BCA) = angle(DCA)]]", "[[angle(BAC) = angle(ACD)]]",
             "[[tri(ABC) = tri(ADC)]]"],
    derived_answer="②, ④",
    figure=U("연꼴 모양 사각형 ABCD(A 위, B 왼쪽, D 오른쪽, C 아래), 대각선 AC, AB·AD 두 줄 표시, BC·DC 한 줄 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 연꼴 사각형·대각선 도형",
    note="△ABC≡△ADC(SSS) → ②(∠BAD=2∠BAC가 맞음), ④(대응각 아님) 틀림. ⑤는 원문대로 '=' 표기. 빠른정답 없음.")

# ---------------- p46
add(id="cc8c7a6d", qtype="choice",
    question="다음 그림과 같이 원 O와 직선 [[l]]의 교점을 A, B라 하고 선분 AB의 중점을 M이라 할 때, [[angle(OMB)]]의 크기는?",
    choices=DEGS(70, 75, 80, 85, 90), derived_answer="⑤",
    figure=U("원 O와 아래쪽을 가로지르는 직선 l, 교점 A(왼쪽)·B(오른쪽), AB의 중점 M(AM=MB 표시), 선분 OA, OB, OM, M에 각 표시"),
    difficulty_est=1, confidence=0.9,
    needs_review="도형 표현 불가: 원·현·중점 도형",
    note="△OAM≡△OBM → ∠OMB=90° ⑤. 빠른정답 '5' ✓.")

# ---------------- p49
add(id="573bd81c", qtype="choice",
    question=("다음 그림은 [[angle(XOY)]]의 이등분선 OC를 작도한 것이다. [[cong(tri(AOC), tri(BOC))]]를 이용하여 "
              "[[angle(AOC) = angle(BOC)]]임을 설명하려고 한다. 이때, 사용되는 삼각형의 합동조건은?"),
    choices=["세 변의 길이가 각각 같다.", "세 각의 크기가 각각 같다.", "두 변의 길이가 같고 한 각의 크기가 같다.",
             "두 변의 길이가 같고 그 끼인 각의 크기가 같다.", "한 변의 길이가 같고 그 양 끝각의 크기가 같다."],
    derived_answer="①",
    figure=U("각 XOY(O 왼쪽, X 위 오른쪽, Y 오른쪽), O 중심 호가 OX·OY와 만나는 점 A·B, A·B 중심 호의 교점 C, 반직선 OC, 선분 AC·BC"),
    difficulty_est=2, confidence=0.9,
    needs_review="도형 표현 불가: 각의 이등분선 작도 그림",
    note="OA=OB, AC=BC, OC 공통 → SSS ①. 빠른정답 '1' ✓.")

# ---------------- p51
add(id="20e829c9", qtype="choice",
    question=("다음은 [[angle(XOY)]]와 크기가 같고 반직선 PQ를 한 변으로 하는 각을 작도하였을 때, [[cong(tri(AOB), tri(CPD))]]임을 보이는 과정이다. "
              "(가), (나), (다)에 알맞은 것을 차례대로 구한 것은?\n"
              "[[tri(AOB)]]와 [[tri(CPD)]]에서\n"
              "[[seg(OA) = seg(PC)]], [[seg(OB)]] = (가), [[seg(AB)]] = (나)\n"
              "∴ [[cong(tri(AOB), tri(CPD))]] ((다) 합동)"),
    choices=["[[seg(PD)]], [[seg(CD)]], SAS", "[[seg(PD)]], [[seg(CD)]], SSS", "[[seg(PC)]], [[seg(PD)]], ASA",
             "[[seg(PQ)]], [[seg(CD)]], SSS", "[[seg(PQ)]], [[seg(PD)]], SAS"],
    derived_answer="②",
    figure=U("작도 그림: 각 XOY(O 왼쪽, X 위 오른쪽, Y 오른쪽)에서 O 중심 호가 OX·OY와 만나는 점 A·B, 반직선 PQ(P 왼쪽)에서 P 중심 같은 반지름 호와 D, D 중심 AB 길이 호와 만나는 점 C, 반직선 PC"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 각의 작도 그림",
    note="OB=PD, AB=CD, SSS ②. 빠른정답 '2' ✓.")

# ---------------- p52
add(id="f5203509", qtype="short",
    question="다음 두 삼각형은 [[cong(tri(ABC), tri(CDA))]]일 때, 사용된 합동조건을 쓰시오.",
    choices=None, derived_answer="SSS 합동",
    figure=U("평행사변형 모양 사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC. AB·CD 한 줄 표시, AD·BC 두 줄 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 사각형·대각선 같은 길이 표시 도형",
    note="AB=CD, BC=DA, AC 공통 → SSS. 빠른정답 '1'과 불일치(①=SSS 뜻일 수 있음).")
