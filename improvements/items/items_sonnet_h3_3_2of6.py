# -*- coding: utf-8 -*-
# esc_sonnet_h3-3_2of6 — 이미지 기준 전사 (81 항목 / 80쪽, 단원 h3-3 기하: 삼수선·벡터의 성분·직선의 방정식·쌍곡선·구의 방정식)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def FIG(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
FIG_REVIEW = "도형 표현 불가"
PRIME = "프라임/첨자 점 라벨"

# ===================== 삼수선 정리 =====================
# p52
add(id="ca3ff96d", qtype="short",
    question="다음 그림과 같이 평면 [[alpha]] 위의 선분 AB는 길이가 [[6 sqrt(2)]]이고 두 평면 [[alpha]], [[beta]]의 교선 [[l]]과 [[deg(30)]]의 각을 이룬다. 점 B에서 평면 [[beta]]에 내린 수선의 발을 C라 하면 [[seg(BC) = 4]]이다. 두 평면 [[alpha]], [[beta]]가 이루는 각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값을 구하시오.\n(단, 점 A는 두 평면 [[alpha]], [[beta]]의 교선 [[l]] 위에 있다.)",
    choices=None, derived_answer="frac(1,3)",
    figure=FIG("두 평면 α(위)·β(아래)와 교선 l, l 위의 점 A, α 위의 선분 AB=6√2가 l과 30°를 이룸, B에서 β에 내린 수선의 발 C(BC=4)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 두 평면·교선·수선의 발 입체 그림",
    note="B에서 l까지 거리 6√2·sin30°=3√2, sinθ=4/(3√2)=2√2/3 → cosθ=1/3 = 빠른정답 ✓.")

# p54
add(id="ee15792b", qtype="short",
    question="다음 그림과 같은 직육면체에서 [[seg(AD) = 1]], [[seg(AE) = sqrt(3)]], [[seg(DC) = 1]]이다. 평면 AFGD와 평면 EFGH가 이루는 각의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=FIG("직육면체 ABCD-EFGH(AD=1, AE=√3, DC=1), 평면 AFGD 음영"),
    difficulty_est=1, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체 입체 그림",
    note="교선 FG에 AF⊥, EF⊥ → ∠AFE, tan=√3/1 → 60°. 빠른정답 없음.")

# p55
add(id="794f7988", qtype="choice",
    question="다음 그림과 같이 [[seg(AB) = sqrt(5)]], [[seg(BC) = 2]]인 정사각뿔에서 평면 ABC와 평면 BCDE가 이루는 각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값은?",
    choices=["[[frac(1,3)]]", "[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(sqrt(2),2)]]", "[[frac(sqrt(3),2)]]"], derived_answer="②",
    figure=FIG("정사각뿔 A-BCDE(AB=√5, BC=2), 면 ABC 음영"),
    difficulty_est=1, confidence=0.85,
    needs_review=FIG_REVIEW + ": 정사각뿔 입체 그림",
    note="BC 중점 M: AM=2, OM=1 → cosθ=1/2 → ② = 빠른정답 ✓.")

# p58
add(id="ed03564e", qtype="short",
    question="다음 그림과 같은 직육면체에서 [[seg(AB) = 6]], [[seg(AD) = 8]], [[seg(BF) = 6 sqrt(3)]]이다. 평면 BEHC와 평면 EFGH가 이루는 각의 크기를 구하시오.",
    choices=None, derived_answer="deg(60)",
    figure=FIG("직육면체 ABCD-EFGH(AB=6, AD=8, BF=6√3), 평면 BEHC 음영"),
    difficulty_est=1, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체 입체 그림",
    note="교선 EH에 BE⊥, FE⊥ → ∠BEF, tan=6√3/6=√3 → 60°. 빠른정답 없음.")

# p66
add(id="3442fa84", qtype="short",
    question="다음 그림과 같은 직육면체에서 [[seg(AD) = 3]], [[seg(AE) = 2 sqrt(3)]], [[seg(DC) = 6]]이다. 평면 AFGD와 평면 EFGH가 이루는 각의 크기를 구하시오.",
    choices=None, derived_answer="deg(30)",
    figure=FIG("직육면체 ABCD-EFGH(AD=3, AE=2√3, DC=6), 평면 AFGD 음영"),
    difficulty_est=1, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체 입체 그림",
    note="∠AFE: tan=2√3/6=1/√3 → 30°. 빠른정답 없음.")

# p68
add(id="d4366abf", qtype="short",
    question="다음 그림과 같이 한 변의 길이가 8인 정사각형 ABCD에 두 선분 AB, CD를 각각 지름으로 하는 두 반원이 붙어 있는 모양의 종이가 있다. 반원의 호 AB를 이등분하는 점을 P라 하고, 반원의 호 CD의 삼등분점 중 점 D에 가까운 점을 Q라 하자. 이 종이에서 두 선분 AB와 CD를 접는 선으로 하여 두 반원을 접어 올렸을 때 두 점 P, Q에서 평면 ABCD에 내린 수선의 발을 각각 G, H라 하면 두 점 G, H는 정사각형 ABCD의 내부에 놓여 있고, [[seg(PG) = 2 sqrt(3)]], [[seg(QH) = sqrt(3)]]이다.\n두 평면 PAQ와 ABCD가 이루는 각의 크기가 [[theta]]일 때, [[7 pow(sin(theta), 2)]]의 값을 구하시오.\n(단, 종이의 두께는 고려하지 않는다.)",
    choices=None, derived_answer="3",
    figure=FIG("(위) 정사각형 ABCD 양쪽에 AB·CD를 지름으로 하는 반원이 붙은 종이, 호 AB의 이등분점 P, 호 CD의 삼등분점 Q; (아래) 두 반원을 접어 올린 입체, P·Q에서 평면 ABCD에 내린 수선의 발 G·H"),
    difficulty_est=4, confidence=0.85,
    needs_review=FIG_REVIEW + ": 반원 붙은 종이 전개도·접어 올린 입체 그림",
    note="출처 [2021년 9월 고3 기하 29번 변형]. A(0,8,0) 기준 P(2,4,2√3), Q(5,6,√3) → 평면 PAQ 법선 (0,√3,2) → cos²θ=4/7, 7sin²θ=3. 빠른정답 2와 불일치.")

# p70
add(id="6a6aac99", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = seg(AC) = 12]], [[seg(BD) = seg(CD) = 8]], [[seg(BC) = 4]], [[seg(AD) = 2 sqrt(15)]]인 사면체에 대하여 평면 ABC와 평면 BCD가 이루는 각의 크기를 [[theta]]라 할 때, [[pow(cos(theta), 2)]]의 값을 [[frac(q,p)]]라 하자. 서로소인 자연수 [[p]], [[q]]에 대하여 [[p + q]]의 값을 구하시오.",
    choices=None, derived_answer="19",
    figure=FIG("사면체 ABCD(AB=AC 표시, BD=CD 표시), 밑면 BCD 위에 꼭짓점 A"),
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 사면체 입체 그림",
    note="BC 중점 M: AM=2√35, DM=2√15, AD=2√15 → cos∠AMD=140/(40√21) → cos²θ=7/12 → 19. 빠른정답 5와 불일치.")

# p72
add(id="4e3def04", qtype="short",
    question="그림과 같이 한 변의 길이가 8인 정사각형 ABCD에 두 선분 AB, CD를 각각 지름으로 하는 두 반원이 붙어 있는 모양의 종이가 있다. 반원의 호 AB의 삼등분점 중 점 B에 가까운 점을 P라 하고, 반원의 호 CD를 이등분하는 점을 Q라 하자. 이 종이에서 두 선분 AB와 CD를 접는 선으로 하여 두 반원을 접어 올렸을 때 두 점 P, Q에서 평면 ABCD에 내린 수선의 발을 각각 G, H라 하면 두 점 G, H는 정사각형 ABCD의 내부에 놓여 있고, [[seg(PG) = sqrt(3)]], [[seg(QH) = 2 sqrt(3)]]이다. 두 평면 PCQ와 ABCD가 이루는 각의 크기가 [[theta]]일 때, [[70 pow(cos(theta), 2)]]의 값을 구하시오.\n(단, 종이의 두께는 고려하지 않는다.)",
    choices=None, derived_answer="40",
    figure=FIG("(위) 정사각형 ABCD 양쪽에 AB·CD를 지름으로 하는 반원이 붙은 종이, 호 AB의 삼등분점 P, 호 CD의 이등분점 Q; (아래) 두 반원을 접어 올린 입체, P·Q에서 평면 ABCD에 내린 수선의 발 G·H"),
    difficulty_est=4, confidence=0.85,
    needs_review=FIG_REVIEW + ": 반원 붙은 종이 전개도·접어 올린 입체 그림",
    note="출처 [2021년 9월 고3 기하 29번/4점]. cos²θ=4/7 → 70cos²θ=40 = 빠른정답 ✓.")

# p78
add(id="f0dec897", qtype="short",
    question="다음 그림과 같이 [[seg(AD) = seg(AE) = 2]], [[seg(CD) = 6]]인 직육면체에서 대각선 DF가 평면 AEHD, 평면 EFGH, 평면 DHGC와 이루는 각의 크기를 각각 [[alpha]], [[beta]], [[gamma]]라 할 때, [[frac(pow(cos(beta), 2) pow(cos(gamma), 2), pow(cos(alpha), 2))]]의 값을 구하시오.",
    choices=None, derived_answer="frac(50,11)",
    figure=FIG("직육면체 ABCD-EFGH(AD=2, AE=2, CD=6)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체 입체 그림",
    note="DF²=44; cos²α=8/44=2/11, cos²β=cos²γ=40/44=10/11 → (10/11)²/(2/11)=50/11 = 빠른정답 ✓.")

# p89
add(id="c4a61902", qtype="choice",
    question="좌표공간에 직선 AB를 포함하는 평면 [[alpha]]가 있다. 평면 [[alpha]] 위에 있지 않은 점 C에 대하여 직선 AB와 직선 AC가 이루는 예각의 크기를 [[sub(theta,1)]]이라 할 때 [[sin(sub(theta,1)) = frac(4,5)]]이고, 직선 AC와 평면 [[alpha]]가 이루는 예각의 크기는 [[frac(pi,2) - sub(theta,1)]]이다. 평면 ABC와 평면 [[alpha]]가 이루는 예각의 크기를 [[sub(theta,2)]]라 할 때, [[cos(sub(theta,2))]]의 값은?",
    choices=["[[frac(sqrt(7),4)]]", "[[frac(sqrt(7),5)]]", "[[frac(sqrt(7),6)]]", "[[frac(sqrt(7),7)]]", "[[frac(sqrt(7),8)]]"], derived_answer="①",
    figure=FIG("평면 α 위의 직선 AB(점 A, B)와 α 밖의 점 C를 지나는 직선 AC"),
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 평면 α와 두 직선 입체 그림",
    note="출처 [2022년 11월 고3 기하 27번/3점]. AC=5: 높이 3, C에서 AB까지 거리 4 → sinθ₂=3/4, cosθ₂=√7/4 → ①. 빠른정답 18과 불일치.")

# p90
add(id="05025a6e", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = seg(BF) = 2]], [[seg(AD) = 3]]인 직육면체에서 대각선 BH가 평면 EFGH, 평면 ABFE, 평면 BFGC와 이루는 각의 크기를 각각 [[alpha]], [[beta]], [[gamma]]라 할 때, [[pow(cos(alpha), 2) + pow(cos(beta), 2) + pow(cos(gamma), 2)]]의 값을 구하시오.",
    choices=None, derived_answer="2",
    figure=FIG("직육면체 ABCD-EFGH(AB=2, BF=2, AD=3), 대각선 BH"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체 입체 그림",
    note="sin²α+sin²β+sin²γ=1 → cos² 합 = 2. 빠른정답 3과 불일치.")

# p91
add(id="347a002a", qtype="choice",
    question="다음 그림과 같이 [[seg(AB) = 2]], [[seg(BF) = 3]], [[seg(AD) = 5]]인 직육면체에서 대각선 BH가 평면 EFGH, 평면 ABFE, 평면 BFGC와 이루는 각의 크기를 각각 [[alpha]], [[beta]], [[gamma]]라 할 때, [[pow(cos(alpha), 2) + pow(cos(beta), 2) + pow(cos(gamma), 2)]]의 값은?",
    choices=["1", "[[frac(3,2)]]", "2", "[[frac(5,2)]]", "3"], derived_answer="③",
    figure=FIG("직육면체 ABCD-EFGH(AB=2, BF=3, AD=5), 대각선 BH"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체 입체 그림",
    note="cos² 합 = 3−1 = 2 → ③ = 빠른정답 ✓.")

# p92
add(id="77110c6b", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = seg(BF) = 3]], [[seg(AD) = 4]]인 직육면체에서 대각선 BH가 평면 EFGH, 평면 ABFE, 평면 BFGC와 이루는 각의 크기를 각각 [[alpha]], [[beta]], [[gamma]]라 할 때, [[pow(cos(alpha), 2) + pow(cos(beta), 2) + pow(cos(gamma), 2)]]의 값을 구하시오.",
    choices=None, derived_answer="2",
    figure=FIG("직육면체 ABCD-EFGH(AB=3, BF=3, AD=4), 대각선 BH"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체 입체 그림",
    note="cos² 합 = 2. 빠른정답 1과 불일치.")

# p94
add(id="3dc95c6e", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = seg(BF) = 4]], [[seg(AD) = 5]]인 직육면체에서 대각선 BH가 평면 EFGH, 평면 ABFE, 평면 BFGC와 이루는 각의 크기를 각각 [[alpha]], [[beta]], [[gamma]]라 할 때, [[pow(cos(alpha), 2) + pow(cos(beta), 2) + pow(cos(gamma), 2)]]의 값을 구하시오.",
    choices=None, derived_answer="2",
    figure=FIG("직육면체 ABCD-EFGH(AB=4, BF=4, AD=5), 대각선 BH"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 직육면체 입체 그림",
    note="cos² 합 = 2. 빠른정답 3과 불일치.")

# ===================== 벡터의 성분 =====================
# p9
add(id="2b3c0188", qtype="short",
    question="두 벡터 [[vec(a) = vcomp(4t - 2, -1)]], [[vec(b) = vcomp(2, 1 + frac(3,t))]]에 대하여 [[pow(abs(vec(a) + vec(b)), 2)]]의 최솟값을 구하시오. (단, [[t > 0]])",
    choices=None, derived_answer="24", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2018년 7월 고3 이과 24번/3점]. a+b=(4t, 3/t) → 16t²+9/t² ≥ 24. 빠른정답 3과 불일치.")

# p65
add(id="10925ab0", qtype="choice",
    question="좌표평면 위의 세 점 [[A(-1, 2)]], [[B(2, 3)]], [[C(1, 4)]]에 대하여 [[vec(AB) = vec(CD)]]를 만족시키는 점 D의 좌표는?",
    choices=["[[point(3, 4)]]", "[[point(4, 5)]]", "[[point(5, 6)]]", "[[point(6, 7)]]", "[[point(7, 8)]]"], derived_answer="②",
    figure=None, difficulty_est=1, confidence=0.9,
    note="AB=(3,1) → D=C+(3,1)=(4,5) → ②. 빠른정답 12와 불일치.")

# p71
add(id="d16686b2", qtype="short",
    question="두 점 [[A(1, -1)]], [[B(3, -2)]]와 직선 [[y = x + 1]] 위를 움직이는 점 P에 대하여 [[abs(vec(AP) + vec(BP))]]의 최솟값을 [[frac(q,p) sqrt(2)]]라 하자. 이때 서로소인 자연수 [[p]], [[q]]에 대하여 [[p + q]]의 값을 구하시오.",
    choices=None, derived_answer="11", figure=None, difficulty_est=2, confidence=0.9,
    note="|AP+BP|=2|PM|, M(2,−3/2), 거리 9/(2√2) → 최솟값 9√2/2 → 11 = 빠른정답 ✓.")

# p76
add(id="c29ce60c", qtype="choice",
    question="네 점 [[A(5, 5)]], [[B(3, 6)]], [[C(7, -7)]], [[D(1, a)]]에 대하여 [[par(vec(AB), vec(CD))]]일 때, [[a]]의 값은?",
    choices=["[[-8]]", "[[-6]]", "[[-4]]", "[[-2]]", "0"], derived_answer="③",
    figure=None, difficulty_est=1, confidence=0.9,
    note="AB=(−2,1), CD=(−6,a+7)=3AB → a=−4 → ③. 빠른정답 0과 불일치.")

# p78
add(id="7c9de852", qtype="choice",
    question="다음 그림과 같이 한 변의 길이가 4인 정사각형 ABCD에서 두 변 AB, BC의 중점을 각각 E, F, 변 CD를 [[ratio(3,1)]]로 내분하는 점을 G라 하자. 선분 AG 위를 움직이는 점 P에 대하여 [[abs(vec(EP) + vec(FP))]]의 최솟값은?",
    choices=["[[sqrt(17)]]", "[[frac(18 sqrt(17), 17)]]", "[[frac(20 sqrt(17), 17)]]", "[[frac(21 sqrt(17), 17)]]", "[[frac(22 sqrt(17), 17)]]"], derived_answer="⑤",
    figure=FIG("정사각형 ABCD(한 변 4, A 왼쪽 위·B 왼쪽 아래·C 오른쪽 아래·D 오른쪽 위), AB의 중점 E, BC의 중점 F, CD를 3:1로 내분하는 점 G, 선분 AG 위의 점 P, 벡터 EP·FP 화살표"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 정사각형과 벡터 화살표 그림",
    note="B 원점: M=EF 중점 (1,1), 직선 AG: x+4y−16=0, 거리 11/√17 → 2배 = 22√17/17 → ⑤. 빠른정답 6과 불일치.")

# p79
add(id="0c2f16db", qtype="choice",
    question="두 점 [[A(2, -4)]], [[B(1, -1)]]과 직선 [[y = x + 3]] 위를 움직이는 점 P에 대하여 [[abs(vec(AP) + vec(BP))]]의 최솟값은?",
    choices=["[[7 sqrt(2)]]", "[[7 sqrt(3)]]", "[[8 sqrt(2)]]", "[[8 sqrt(3)]]", "14"], derived_answer="①",
    figure=None, difficulty_est=2, confidence=0.9,
    note="M(3/2,−5/2), 거리 7/√2 → 2배 7√2 → ① = 빠른정답 ✓.")

# p80
add(id="f756ae47", qtype="short",
    question="두 공간벡터 [[vec(OA) = vcomp(1, 2, 2)]], [[vec(OB) = vcomp(4, 3, 0)]]과 선분 AB 위의 점 P에 대하여 직선 OP가 [[angle(AOB)]]를 이등분한다. 이때 벡터 [[vec(OP)]]의 모든 성분의 합을 구하시오.",
    choices=None, derived_answer="frac(23,4)", figure=None, difficulty_est=2, confidence=0.9,
    note="|OA|=3, |OB|=5 → AP:PB=3:5 → P=(5A+3B)/8=(17,19,10)/8 → 합 23/4 = 빠른정답 ✓.")

# p81
add(id="e80de18f", qtype="choice",
    question="좌표평면 위의 세 점 [[O(0, 0)]], [[A(2, 4)]], [[B(-4, 4)]]에 대하여 점 P가 [[dot((vec(OP) - vec(OA)), vec(OB)) = 0]]을 만족시킬 때, [[abs(vec(OP))]]의 최솟값은?",
    choices=["[[sqrt(2)]]", "[[sqrt(3)]]", "2", "[[sqrt(5)]]", "[[sqrt(6)]]"], derived_answer="①",
    figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2025년 7월 고3 기하 25번 변형]. AP⊥OB → P는 A를 지나고 OB에 수직인 직선 위, 거리 |OA·OB|/|OB|=8/(4√2)=√2 → ① = 빠른정답 ✓.")

# p84
add(id="c96a1043", qtype="short",
    question="두 점 [[O(0, 0, 0)]], [[A(2, -2, 1)]]에 대하여 [[abs(vec(OA)) abs(vec(AP)) = k]]를 만족시키는 점 P가 나타내는 도형의 부피가 [[frac(32,81) pi]]일 때, 실수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="|OA|=3 → 반지름 k/3, (4/3)π(k/3)³=32π/81 → k=2 = 빠른정답 ✓.")

# p87
add(id="cc02514e", qtype="choice",
    question="좌표평면 위의 두 점 [[A(-3, 4)]], [[B(1, 2)]]에 대하여 [[abs(vec(AP)) = abs(vec(BP))]]를 만족시키는 점 P가 나타내는 도형의 방정식은?",
    choices=["[[x - y + 5 = 0]]", "[[2x - y + 5 = 0]]", "[[x + y + 5 = 0]]", "[[2x + y + 5 = 0]]", "[[3x - y + 5 = 0]]"], derived_answer="②",
    figure=None, difficulty_est=1, confidence=0.9,
    note="AB의 수직이등분선: 중점 (−1,3), 법선 (4,−2) → 2x−y+5=0 → ② = 빠른정답 ✓.")

# p88
add(id="3e7e8ad8", qtype="choice",
    question="두 점 [[A(3, -1)]], [[B(-2, 6)]]에 대하여 [[abs(vec(AP)) = abs(vec(BP))]]를 만족시키는 점 P의 자취의 방정식은?",
    choices=["[[5x - 7y - 15 = 0]]", "[[5x - 7y + 15 = 0]]", "[[5x + 7y - 15 = 0]]", "[[10x - 14y - 15 = 0]]", "[[10x - 14y + 15 = 0]]"], derived_answer="②",
    figure=None, difficulty_est=1, confidence=0.9,
    note="(x−3)²+(y+1)²=(x+2)²+(y−6)² → 10x−14y+30=0 → 5x−7y+15=0 → ②. 빠른정답 52와 불일치.")

# p91
add(id="3531fde8", qtype="short",
    question="두 점 [[O(0, 0)]], [[A(2, -3)]]에 대하여 [[abs(vec(OA)) abs(vec(AP)) = k]]를 만족시키는 점 P가 나타내는 도형의 넓이가 [[4 pi]]일 때, [[pow(k,2)]]의 값을 구하시오.",
    choices=None, derived_answer="52", figure=None, difficulty_est=2, confidence=0.9,
    note="|OA|=√13 → 반지름 k/√13, π k²/13=4π → k²=52 = 빠른정답 ✓.")

# p99 (이미지에 별개 문항 2개, id 1개 — draft_a 대응인 첫째 문항(구)만 전사)
add(id="d2c737b5", qtype="short",
    question="세 점 [[A(1, 0, 2)]], [[B(2, 4, -1)]], [[C(3, 2, -1)]]에 대하여 [[abs(vec(PA) + vec(PB) + vec(PC)) = 9]]를 만족시키는 점 P가 나타내는 도형은 중심의 좌표가 [[vcomp(a, b, c)]]이고 반지름의 길이가 [[r]]인 구이다. 이때 [[a + b + c + r]]의 값을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="이미지에 별개 문항 2개 인쇄(둘째: 두 점 A(−1, 0), B(2, 0)에 대하여 점 P가 |PA|²=4|PB|²을 만족할 때 삼각형 PAB의 넓이의 최댓값, 선지 ①3 ②4 ③5 ④6 ⑤7 — 답 ①), id는 1개 — draft_a 대응인 첫째 문항(구)만 전사",
    note="|3P−(A+B+C)|=9 → 중심 G(2,2,0), 반지름 3 → 7. 빠른정답 5와 불일치(둘째 문항 답 ①과도 불일치).")

# ===================== 직선의 방정식 =====================
# p3
add(id="b0a97ff2", qtype="choice",
    question="점 [[A(-4, 3)]]을 지나고 방향벡터가 [[vec(u) = vcomp(a, b)]]인 직선이 원 [[pow(x + 3, 2) + pow(y - 6, 2) = 1]]과 만날 때, [[frac(a,b)]]의 최댓값은?\n(단, [[a > 0]], [[b > 0]])",
    choices=["[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(3,4)]]", "[[frac(4,5)]]", "1"], derived_answer="③",
    figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 m=b/a: |m−3|/√(m²+1) ≤ 1 → m ≥ 4/3 → a/b ≤ 3/4 → ③ = 빠른정답 ✓.")

# p13
add(id="a954d9b8", qtype="choice",
    question="함수 [[f(x) = frac(1, pow(x,2) - x)]]의 그래프는 다음 그림과 같다. 함수 [[y = f(x)]]의 그래프 위의 두 점 [[P(-1, f(-1))]], [[Q(frac(1,2), f(frac(1,2)))]]을 지나는 직선의 방향벡터 중 크기가 [[3 sqrt(10)]]인 벡터를 [[vec(u) = vcomp(a, b)]]라 하자. [[abs(a - b)]]의 값은?",
    choices=["10", "11", "12", "13", "14"], derived_answer="③",
    figure=FIG("함수 y=1/(x²−x)의 그래프(점근선 x=0, x=1 점선, x축 위 O·1 표시)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 함수 그래프",
    note="P(−1,1/2), Q(1/2,−4) → 방향 (1,−3), u=±(3,−9) → |a−b|=12 → ③. 빠른정답 17과 불일치.")

# p14
add(id="492f3c00", qtype="choice",
    question="함수 [[f(x) = frac(1, pow(x,2) - x)]]의 그래프는 다음 그림과 같다. 함수 [[y = f(x)]]의 그래프 위의 두 점 [[P(2, f(2))]], [[Q(frac(1,2), f(frac(1,2)))]]을 지나는 직선의 방향벡터 중 크기가 [[3 sqrt(10)]]인 벡터를 [[vec(u) = vcomp(a, b)]]라 하자. [[abs(a - b)]]의 값은?",
    choices=["6", "7", "8", "9", "10"], derived_answer="①",
    figure=FIG("함수 y=1/(x²−x)의 그래프(점근선 x=0, x=1 점선, x축 위 O·1 표시)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 함수 그래프",
    note="P(2,1/2), Q(1/2,−4) → 방향 (1,3), u=±(3,9) → |a−b|=6 → ①. 빠른정답 −1과 불일치.")

# p16 (같은 이미지에 id 2개 — 문항은 1개)
dup(["49bcaec6", "efcc87aa"], qtype="short",
    question="점 [[A(1, -1)]]과 제1사분면 위의 점 B, 제2사분면 위의 점 C, 제3사분면 위의 점 D를 꼭짓점으로 하는 사각형 ABCD는 [[seg(AB) = seg(AD)]]이고 다음 조건을 모두 만족시킨다. 점 C의 좌표가 [[point(p, q)]]일 때, [[5p + 10q]]의 값을 구하시오.\n(가) [[dot(vec(AB), vec(AD)) = 0]], [[dot(vec(CB), vec(CD)) = 0]]\n(나) [[vec(BD) = t vcomp(1, 2)]] ([[t]]는 실수)\n(다) 두 선분 AC, BD의 교점은 원점이다.",
    choices=None, derived_answer="4", figure=None, difficulty_est=4, confidence=0.85,
    note="B(b,2b), D(d,2d): b+d=−2/5, bd=−8/25 → B(2/5,4/5), D(−4/5,−8/5); C(c,−c)에서 CB⊥CD → c=−4/5 → C(−4/5,4/5) → 5p+10q=4. 빠른정답 3과 불일치.")

# p18
add(id="7f18cb10", qtype="short",
    question="점 [[A(-1, 1)]]과 제3사분면 위의 점 B, 제4사분면 위의 점 C, 제1사분면 위의 점 D를 꼭짓점으로 하는 사각형 ABCD는 [[seg(AB) = seg(AD)]]이고 다음 조건을 모두 만족한다. 점 C의 좌표가 [[point(p, q)]]일 때, [[15p + 5q]]의 값을 구하시오.\n(가) [[dot(vec(AB), vec(AD)) = 0]], [[dot(vec(CB), vec(CD)) = 0]]\n(나) [[vec(BD) = t vcomp(2, 1)]] ([[t]]는 실수)\n(다) 두 선분 AC, BD의 교점은 원점이다.",
    choices=None, derived_answer="8", figure=None, difficulty_est=4, confidence=0.85,
    note="B(2b,b), D(2d,d): b+d=−2/5, bd=−8/25 → B(−8/5,−4/5), D(4/5,2/5); C(c,−c)에서 CB⊥CD → c=4/5 → C(4/5,−4/5) → 15p+5q=8. 빠른정답 3과 불일치.")

# p19
add(id="5c5a76ca", qtype="short",
    question="좌표공간에 네 점 [[A(2, 0, 0)]], [[B(0, 1, 0)]], [[C(-3, 0, 0)]], [[D(0, 0, 2)]]를 꼭짓점으로 하는 사면체 ABCD가 있다. 모서리 BD 위를 움직이는 점 P에 대하여 [[pow(seg(PA), 2) + pow(seg(PC), 2)]]의 값을 최소로 하는 점 P의 좌표를 [[vcomp(a, b, c)]]라고 할 때, [[a + b + c = frac(q,p)]]이다. [[p + q]]의 값을 구하시오.\n(단, [[p]], [[q]]는 서로소인 자연수이다.)",
    choices=None, derived_answer="11", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2007년 11월 고3 이과 23번]. AC 중점 M(−1/2,0,0)에서 BD에 내린 수선의 발 P(0,4/5,2/5) → 6/5 → 11. 빠른정답 4와 불일치.")

# p24
add(id="51556536", qtype="choice",
    question="좌표공간에 두 점 [[A(0, -1, 1)]], [[B(1, 1, 0)]]이 있고, [[x y]]평면 위에 원 [[pow(x,2) + pow(y,2) = 13]]이 있다. 이 원 위의 점 [[vcomp(a, b, 0)]] ([[a < 0]])을 지나고 [[z]]축에 평행한 직선이 직선 AB와 만날 때, [[a + b]]의 값은?",
    choices=["[[-frac(47,10)]]", "[[-frac(23,5)]]", "[[-frac(9,2)]]", "[[-frac(22,5)]]", "[[-frac(43,10)]]"], derived_answer="②",
    figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2011년 9월 고3 이과 18번/4점]. AB의 xy평면 정사영 (s, 2s−1): 5s²−4s−12=0, a<0 → s=−6/5 → a+b=−23/5 → ② = 빠른정답 ✓.")

# p25
add(id="6fd53956", qtype="choice",
    question="함수 [[f(x) = frac(1, pow(x,2) - 2x)]]라 하자. 함수 [[y = f(x)]]의 그래프 위의 두 점 [[P(-1, f(-1))]], [[Q(1, f(1))]]을 지나는 직선의 방향벡터 중 크기가 [[sqrt(52)]]인 벡터를 [[vec(u) = vcomp(a, b)]]라 하자. 이때 [[abs(a - b)]]의 값은?",
    choices=["10", "12", "14", "16", "18"], derived_answer="①",
    figure=FIG("함수 y=1/(x²−2x)의 그래프(점근선 x=0, x=2 점선, x축 위 O·2 표시)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 함수 그래프",
    note="출처 [2016년 7월 고3 이과 13번 변형]. P(−1,1/3), Q(1,−1) → 방향 (3,−2), u=±(6,−4) → |a−b|=10 → ①. 빠른정답 −38과 불일치.")

# p35
add(id="244d60d7", qtype="choice",
    question="점 [[point(2, 3)]]을 지나고 방향벡터가 [[vec(u) = vcomp(1, -3)]]인 직선을 [[l]]이라 하자. 점 [[point(-2, 5)]]에서 두 직선 [[l]], [[m]]: [[frac(x - 2, 3) = frac(y - 2, 4)]]에 내린 수선의 발을 각각 A, B라 할 때, [[abs(dot(vec(OA), vec(OB)))]]의 값은?\n(단, O는 원점이다.)",
    choices=["11", "12", "13", "14", "15"], derived_answer="④",
    figure=None, difficulty_est=2, confidence=0.9,
    note="A(1,6), B(2,2) → OA·OB=14 → ④. 빠른정답 13과 불일치.")

# p43
add(id="f15ec6f6", qtype="choice",
    question="두 점 [[vcomp(1, -4, -10)]], [[vcomp(3, 1, 0)]]을 지나는 직선과 직선 [[frac(x + 5, 2) = frac(y + 15, 3) = z + 22]]의 교점의 좌표를 [[vcomp(p, q, r)]]라 할 때, [[p + q + r]]의 값은?",
    choices=["[[-10]]", "[[-20]]", "[[-30]]", "[[-40]]", "[[-50]]"], derived_answer="③",
    figure=None, difficulty_est=2, confidence=0.9,
    note="(1+2s, −4+5s, −10+10s)=(−5+2t, −15+3t, −22+t) → s=−1, t=2 → (−1,−9,−20) → −30 → ③. 빠른정답 10과 불일치.")

# p74
add(id="64302d1f", qtype="short",
    question="점 [[P(0, 7, -3)]]에서 직선 [[l]]: [[frac(x - 2, 2) = -frac(y + 3, 2) = 3 - z]]에 내린 수선의 발을 H라 할 때, 두 점 P, H를 지나는 직선의 방정식은 [[x + 2 = frac(y - b, a) = -frac(z - d, c)]]이다. 이때 [[a + b + c + d]]의 값을 구하시오. (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)",
    choices=None, derived_answer="13", figure=None, difficulty_est=3, confidence=0.9,
    note="H(−2,1,5), PH 방향 (1,3,−4) → x+2=(y−1)/3=−(z−5)/4 → a=3,b=1,c=4,d=5 → 13. 빠른정답 5와 불일치.")

# p84
add(id="1567ea5d", qtype="short",
    question="다음 그림과 같이 좌표공간 위에 한 모서리의 길이가 6인 정육면체가 있다. 선분 AF와 선분 BD 사이의 거리를 최소로 하는 선분 AF 위의 점의 좌표를 [[vcomp(a, b, c)]]라 할 때, [[a + 2b + 3c]]의 값을 구하시오. (단, O는 원점이다.)",
    choices=None, derived_answer="22",
    figure=FIG("좌표공간의 정육면체 ABCD-EFGH(모서리 6): H가 원점 O, E는 x축 위, G는 y축 위(OG=6), D는 z축 위; 위 면 ABCD, 대각선 AF·BD"),
    difficulty_est=3, confidence=0.85,
    needs_review=FIG_REVIEW + ": 좌표공간 정육면체 입체 그림",
    note="A(6,0,6), F(6,6,0), B(6,6,6), D(0,0,6): 최근접점 (6,2,4) → 6+4+12=22. 빠른정답 5와 불일치.")

# p87
add(id="71e31f64", qtype="short",
    question="직선 [[sub(l,1)]]: [[frac(x + 4, 3) = y - 1 = 1 - z]] 위의 한 점 P와 직선 [[sub(l,2)]]: [[x - 3 = frac(4 - y, 3) = frac(5 - z, 2)]] 위의 한 점 Q에 대하여 [[seg(PQ)]]의 길이가 최소가 되는 두 점 P, Q의 좌표는 각각 [[vcomp(a, b, c)]], [[vcomp(d, e, f)]]이다. 이때 [[a + b + c + d + e + f]]의 값을 구하시오. (단, 두 직선 [[sub(l,1)]], [[sub(l,2)]]는 꼬인 위치에 있다.)",
    choices=None, derived_answer="12", figure=None, difficulty_est=3, confidence=0.9,
    note="P(−4+3s,1+s,1−s), Q(3+t,4−3t,5−2t), PQ⊥d₁,d₂ → s=2,t=1 → P(2,3,−1), Q(4,1,3) → 12 = 빠른정답 ✓.")

# p90
add(id="18313271", qtype="choice",
    question="꼬인 위치에 있는 두 직선 [[sub(l,1)]]: [[x - 1 = y = frac(z,2)]], [[sub(l,2)]]: [[frac(x - 1, 2) = 3 - y = z]] 사이의 거리는?",
    choices=["[[sqrt(2)]]", "[[sqrt(3)]]", "2", "[[sqrt(5)]]", "[[sqrt(6)]]"], derived_answer="②",
    figure=None, difficulty_est=2, confidence=0.9,
    note="d₁=(1,1,2), d₂=(2,−1,1), n=(1,1,−1); 점 차 (0,3,0) → 3/√3=√3 → ②. 빠른정답 12와 불일치.")

# ===================== 쌍곡선 =====================
# p20
add(id="b921527d", qtype="choice",
    question="두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[C]]와 [[y]]축 위의 점 A가 있다. 쌍곡선 [[C]]가 선분 AF와 만나는 점을 P, 선분 AF′과 만나는 점을 P′이라 하자. 직선 AF는 쌍곡선 [[C]]의 한 점근선과 평행하고 [[seg(AP)]] : PP′ = [[ratio(5, 6)]], [[seg(PF) = 1]]일 때, 쌍곡선 [[C]]의 주축의 길이는?",
    choices=["[[frac(13,6)]]", "[[frac(9,4)]]", "[[frac(7,3)]]", "[[frac(29,12)]]", "[[frac(5,2)]]"], derived_answer="②",
    figure=FIG("좌표평면: 쌍곡선 C(초점 F′·F가 x축 위), y축 위의 점 A, 선분 AF·AF′과 쌍곡선의 교점 P·P′, 선분 PP′(x축에 평행)"),
    difficulty_est=4, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·삼각형 좌표평면 그림 / " + PRIME + "(F′, P′, 선분 AF′·PP′ 윗줄 생략)",
    note="출처 [2022년 11월 고3 기하 28번/4점]. AF=c²/a=5c/3 → c=5a/3, e=5/3; PF=e·x_P−a=1, AP/AF=x_P/c → a=9/8 → 주축 9/4 → ②. 빠른정답 4와 불일치.")

# p42
add(id="cb3baad3", qtype="short",
    question="다음 그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하고 주축의 길이가 8인 쌍곡선이 있다. 이 쌍곡선이 선분 FF′을 지름으로 하는 원과 제1사분면에서 만나는 점을 P라 하자. 선분 F′P가 쌍곡선과 만나는 점 중 점 P가 아닌 점을 Q라 하고, 선분 FQ가 쌍곡선과 만나는 점 중 점 Q가 아닌 점을 R이라 하자. 점 Q가 선분 F′P를 [[ratio(1, 3)]]으로 내분할 때, 삼각형 QF′R의 넓이를 [[frac(q,p)]]라 하자. 이때 [[q - 2p]]의 값을 구하시오. (단, [[p]], [[q]]는 서로소인 자연수이다.)",
    choices=None, derived_answer="934",
    figure=FIG("좌표평면: 쌍곡선(초점 F′·F), FF′을 지름으로 하는 원, 제1사분면 교점 P, 선분 F′P 위의 점 Q(왼쪽 가지), 선분 FQ 위의 점 R(오른쪽 가지), 선분 F′R"),
    difficulty_est=5, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·원·삼각형 복합 좌표평면 그림 / " + PRIME + "(F′, 선분 FF′·F′P, 삼각형 QF′R)",
    note="출처 [2024년 3월 고3 기하 30번 변형]. F′Q=t, QP=3t, PF=4t−8, FQ=t+8 → t=10/3; 넓이 QF′R = 80/9 − 1600/639 = 1360/213 → 1360−426=934 = 빠른정답 ✓.")

# p43
add(id="8edbaa5c", qtype="short",
    question="두 점 F, F′을 초점으로 하는 쌍곡선 [[frac(pow(x,2), 4) - frac(pow(y,2), 32) = 1]] 위의 점 A가 다음 조건을 만족시킨다.\n(가) [[seg(AF)]] < AF′\n(나) 선분 AF의 수직이등분선은 점 F′을 지난다.\n선분 AF의 중점 M에 대하여 직선 MF′과 쌍곡선의 교점 중 점 A에 가까운 점을 B라 할 때, 삼각형 BFM의 둘레의 길이는 [[k]]이다. [[pow(k,2)]]의 값을 구하시오.",
    choices=None, derived_answer="128", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 AF′ 윗줄 생략, 직선 MF′)",
    note="출처 [2022년 3월 고3 기하 29번/4점]. c=6, AF′=FF′=12, AF=8, MF′=8√2; BA=BF, BF′−BF=4 → 둘레 = MF′+MF = 8√2 → k²=128. 빠른정답 3과 불일치.")

# p45
add(id="1d8d85d1", qtype="short",
    question="점근선의 방정식이 [[y = pm(frac(3,4)) x]]이고 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선이 다음 조건을 만족시킨다.\n(가) 쌍곡선 위의 한 점 P에 대하여 PF′ = 24, [[12 <= seg(PF) <= 16]]이다.\n(나) [[x]]좌표가 양수인 꼭짓점 A에 대하여 선분 AF의 길이는 자연수이다.\n이 쌍곡선의 주축의 길이를 구하시오.",
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 PF′ 윗줄 생략)",
    note="출처 [2016년 11월 고3 이과 28번 변형]. a=4k, c=5k; PF=24−8k∈[12,16] → k∈[1,3/2]; AF=c−a=k 자연수 → k=1 → 주축 8. 빠른정답 128과 불일치.")

# p46
add(id="d64e8a96", qtype="choice",
    question="두 양수 [[a]], [[c]]에 대하여 두 점 [[F(c, 0)]], F′[[point(-c, 0)]]을 초점으로 하는 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 3) = 1]]이 있다. 두 직선 PF, PF′이 서로 수직이 되도록 하는 이 쌍곡선 위의 점 중 제1사분면 위의 점을 P, [[seg(PQ) = frac(a,3)]]인 선분 PF′ 위의 점을 Q라 하자. 직선 QF와 [[y]]축이 만나는 점을 A라 할 때, 점 A에서 두 직선 PF, PF′에 내린 수선의 발을 각각 R, S라 하자. [[seg(AR) = seg(AS)]]일 때, [[pow(a,2)]]의 값은?",
    choices=["[[frac(18,5)]]", "4", "[[frac(22,5)]]", "[[frac(24,5)]]", "[[frac(26,5)]]"], derived_answer="④",
    figure=FIG("좌표평면: 쌍곡선 x²/a²−y²/3=1(초점 F′·F), 제1사분면 점 P, 선분 PF′ 위의 점 Q, 직선 QF와 y축의 교점 A, A에서 직선 PF·PF′에 내린 수선의 발 R·S(직각 표시)"),
    difficulty_est=5, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·직선·수선의 발 복합 좌표평면 그림 / " + PRIME + "(F′, 직선 PF′, 선분 PF′)",
    note="출처 [2024년 7월 고3 기하 28번/4점]. PF=m, PF′=n: mn=6; A는 ∠FPF′의 외각 이등분선 위, AF=AF′ → m=a/2, n=5a/2 → 5a²/4=6 → a²=24/5 → ④. 빠른정답 128과 불일치.")

# p47
add(id="09161aac", qtype="short",
    question="점근선의 방정식이 [[y = pm(frac(4,3)) x]]이고 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선이 다음 조건을 만족시킨다.\n(가) 쌍곡선 위의 한 점 P에 대하여 PF′ = 30, [[16 <= seg(PF) <= 20]]이다.\n(나) [[x]]좌표가 양수인 꼭짓점 A에 대하여 선분 AF의 길이는 자연수이다.\n이 쌍곡선의 주축의 길이를 구하시오.",
    choices=None, derived_answer="12", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 PF′ 윗줄 생략)",
    note="출처 [2016년 11월 고3 이과 28번/4점]. a=3k, c=5k; PF=30−6k∈[16,20] → k∈[5/3,7/3]; AF=2k 자연수 → k=2 → 주축 12 = 빠른정답 ✓.")

# p54
add(id="e46bd2b9", qtype="choice",
    question="점근선의 방정식이 [[y = pm(frac(4 sqrt(2), 7)) x]]이고 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선이 다음 조건을 모두 만족시킨다.\n(가) 쌍곡선 위의 한 점 P에 대하여 PF′ = 30, [[10 <= seg(PF) <= 20]]\n(나) [[x]]좌표가 양수인 꼭짓점 A에 대하여 선분 AF의 길이는 자연수이다.\n이때 이 쌍곡선의 주축의 길이는?",
    choices=["6", "8", "10", "12", "14"], derived_answer="⑤",
    figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 PF′ 윗줄 생략)",
    note="a=7k, b=4√2k, c=9k; PF=30−14k∈[10,20] → k∈[5/7,10/7]; AF=2k 자연수 → k=1 → 주축 14 → ⑤. 빠른정답 4와 불일치.")

# p58
add(id="3d6b6352", qtype="short",
    question="쌍곡선 [[pow(x,2) - frac(pow(y,2), 8) = 1]]의 한 초점 [[F(3, 0)]]과 점 [[A(2, sqrt(11))]]에 대하여 쌍곡선 위의 점 P가 제1사분면 위에 있을 때, [[seg(AP) + seg(PF)]]의 최솟값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="PF=PF′−2 (F′(−3,0)) → AP+PF ≥ AF′−2 = 6−2 = 4. 빠른정답 7과 불일치.")

# p61
add(id="59b0958e", qtype="choice",
    question="평면에 한 변의 길이가 12인 정삼각형 ABC가 있다. [[seg(PC) - seg(PB) = 4]]를 만족시키는 점 P에 대하여 선분 PA의 길이가 최소일 때, 삼각형 PBC의 넓이는?",
    choices=["[[20 sqrt(3)]]", "[[24 sqrt(3)]]", "[[28 sqrt(3)]]", "[[32 sqrt(3)]]", "[[36 sqrt(3)]]"], derived_answer="④",
    figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2019년 11월 고3 이과 17번 변형]. B(−6,0), C(6,0): x²/4−y²/32=1 왼쪽 가지, PA 최소 시 y=16√3/3 → 넓이 (1/2)·12·16√3/3=32√3 → ④ = 빠른정답 ✓.")

# p63
add(id="e07f0839", qtype="short",
    question="그림과 같이 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])이고, 주축의 길이가 6인 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]]과 점 [[A(0, 5)]]를 중심으로 하고 반지름의 길이가 1인 원 [[C]]가 있다. 제1사분면에 있는 쌍곡선 위를 움직이는 점 P와 원 [[C]] 위를 움직이는 점 Q에 대하여 [[seg(PQ)]] + PF′의 최솟값이 12일 때, [[pow(a,2) + 3 pow(b,2)]]의 값을 구하시오. (단, [[a]]와 [[b]]는 상수이다.)",
    choices=None, derived_answer="54",
    figure=FIG("좌표평면: 쌍곡선 x²/a²−y²/b²=1(초점 F′·F), y축 위 점 A 중심의 원 C와 그 위의 점 Q, 제1사분면 쌍곡선 위의 점 P, 선분 PQ·PF′"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·원 좌표평면 그림 / " + PRIME + "(F′, 선분 PF′ 윗줄 생략)",
    note="출처 [2018년 4월 고3 이과 28번/4점]. PQ+PF′ ≥ PA−1+PF+6 ≥ AF+5 = 12 → AF=7 → c²=24, b²=15 → 9+45=54. 빠른정답 3과 불일치.")

# p64
add(id="d68eeab4", qtype="choice",
    question="평면에 한 변의 길이가 10인 정삼각형 ABC가 있다. [[seg(PB) - seg(PC) = 2]]를 만족시키는 점 P에 대하여 선분 PA의 길이가 최소일 때, 삼각형 PBC의 넓이는?",
    choices=["[[20 sqrt(3)]]", "[[21 sqrt(3)]]", "[[22 sqrt(3)]]", "[[23 sqrt(3)]]", "[[24 sqrt(3)]]"], derived_answer="⑤",
    figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2019년 11월 고3 이과 17번/4점]. B(−5,0), C(5,0): x²−y²/24=1 오른쪽 가지, PA 최소 시 y=24√3/5 → 넓이 24√3 → ⑤. 빠른정답 4와 불일치.")

# p65
add(id="cd96eeb7", qtype="short",
    question="다음 그림과 같이 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])이고, 주축의 길이가 8인 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]]과 점 [[A(0, 6)]]을 중심으로 하고 반지름의 길이가 2인 원 [[C]]가 있다.\n제1사분면에 있는 쌍곡선 위를 움직이는 점 P와 원 [[C]] 위를 움직이는 점 Q에 대하여 [[seg(PQ)]] + PF′의 최솟값이 16일 때, [[pow(a,2) + 2 pow(b,2)]]의 값을 구하시오. (단, [[a]]와 [[b]]는 상수이다.)",
    choices=None, derived_answer="112",
    figure=FIG("좌표평면: 쌍곡선 x²/a²−y²/b²=1(초점 F′·F), y축 위 점 A 중심의 원 C와 그 위의 점 Q, 제1사분면 쌍곡선 위의 점 P, 선분 PQ·PF′"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·원 좌표평면 그림 / " + PRIME + "(F′, 선분 PF′ 윗줄 생략)",
    note="출처 [2018년 4월 고3 이과 28번 변형]. PQ+PF′ ≥ PA−2+PF+8 ≥ AF+6 = 16 → AF=10 → c²=64, b²=48 → 16+96=112. 빠른정답 3과 불일치.")

# p66
add(id="f16edb50", qtype="choice",
    question="다음 그림과 같이 쌍곡선 [[frac(pow(x,2), 25) - frac(pow(y,2), 16) = 1]]의 두 초점을 F, F′이라 하고, 이 쌍곡선 위의 점 P를 중심으로 하고 선분 PF′을 반지름으로 하는 원을 [[C]]라 하자.\n원 [[C]] 위를 움직이는 점 Q에 대하여 선분 FQ의 길이의 최댓값이 18일 때, 원 [[C]]의 넓이는? (단, PF′ < [[seg(PF)]])",
    choices=["[[4 pi]]", "[[9 pi]]", "[[16 pi]]", "[[25 pi]]", "[[36 pi]]"], derived_answer="③",
    figure=FIG("좌표평면: 쌍곡선 x²/25−y²/16=1(초점 F′·F), 왼쪽 가지 위의 점 P를 중심으로 F′을 지나는 원 C, 원 위의 점 Q, 선분 FQ"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·원 좌표평면 그림 / " + PRIME + "(F′, 선분 PF′ 윗줄 생략)",
    note="출처 [2016년 6월 고3 이과 18번 변형]. FQ 최댓값 = PF+PF′ = 2PF′+10 = 18 → PF′=4 → 넓이 16π → ③. 빠른정답 54와 불일치.")

# p68
add(id="961e8cf5", qtype="choice",
    question="한 변의 길이가 2인 정육각형 ABCDEF와 쌍곡선 [[H]]가 다음 조건을 만족시킨다.\n(가) 쌍곡선 [[H]]의 초점은 점 A와 점 D이다.\n(나) 쌍곡선 [[H]]의 점근선은 직선 BE와 직선 CF이다.\n쌍곡선 [[H]]와 변 AB가 만나는 점을 P라 할 때, [[seg(DP) - seg(AP)]]의 값은?",
    choices=["[[frac(1,2)]]", "1", "[[sqrt(2)]]", "[[sqrt(3)]]", "2"], derived_answer="⑤",
    figure=FIG("정육각형 ABCDEF(A 오른쪽, D 왼쪽, B·C 위, E·F 아래)와 대각선 BE, CF"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 정육각형과 대각선 그림",
    note="출처 [2011년 10월 고3 이과 16번/4점]. c=2, b/a=√3 → a=1 → DP−AP=2a=2 → ⑤. 빠른정답 146과 불일치.")

# p69
add(id="0a149694", qtype="choice",
    question="한 변의 길이가 [[2 sqrt(2)]]인 정사각형 ABCD와 쌍곡선 [[H]]가 다음 조건을 만족한다.\n(가) 두 점 M, N은 각각 선분 AB, CD의 중점이다.\n(나) 쌍곡선 [[H]]의 초점은 점 M과 점 N이다.\n(다) 쌍곡선 [[H]]의 점근선은 직선 AC와 직선 BD이다.\n쌍곡선 [[H]]와 변 CD가 만나는 점을 P라 할 때, [[seg(MP) - seg(NP)]]의 값은?",
    choices=["[[frac(1,2)]]", "[[frac(sqrt(2),2)]]", "1", "[[sqrt(2)]]", "2"], derived_answer="⑤",
    figure=FIG("정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), AB의 중점 M, CD의 중점 N, 대각선 AC·BD"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG_REVIEW + ": 정사각형과 대각선 그림",
    note="c=√2, a=b → a=1 → MP−NP=2 → ⑤. 빠른정답 4와 불일치.")

# p71
add(id="445eb9ed", qtype="short",
    question="다음 그림과 같이 두 초점이 F, F′인 쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), 16) = 1]] 위의 점 P에 대하여 직선 FP와 직선 F′P에 동시에 접하고 중심이 [[y]]축 위에 있는 원 [[C]]가 있다. 직선 F′P와 원 [[C]]의 접점 Q에 대하여 F′Q = 8일 때, [[pow(seg(FP), 2)]] + F′P²의 값을 구하시오. (단, F′P < [[seg(FP)]])",
    choices=None, derived_answer="146",
    figure=FIG("좌표평면: 쌍곡선(초점 F′·F), 왼쪽 가지 위의 점 P, 직선 FP·F′P에 접하고 중심이 y축 위인 원 C, 직선 F′P와 원의 접점 Q"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·접하는 원 좌표평면 그림 / " + PRIME + "(F′, 선분 F′Q·F′P 윗줄 생략)",
    note="접선 길이 F′Q=FQ′=8: FP+F′P=16, FP−F′P=6 → FP=11, F′P=5 → 146 = 빠른정답 ✓.")

# p73
add(id="61d36153", qtype="choice",
    question="그림과 같이 초점이 각각 F, F′과 G, G′이고, 주축의 길이가 2, 중심이 원점 O인 두 쌍곡선이 제1사분면에서 만나는 점을 P, 제3사분면에서 만나는 점을 Q라 하자. [[seg(PG) × seg(QG) = 8]], [[seg(PF) × seg(QF) = 4]]일 때, 사각형 PGQF의 둘레의 길이는?\n(단, 점 F의 [[x]]좌표와 점 G의 [[y]]좌표는 양수이다.)",
    choices=["[[6 + 2 sqrt(2)]]", "[[6 + 2 sqrt(3)]]", "10", "[[6 + 2 sqrt(5)]]", "[[6 + 2 sqrt(6)]]"], derived_answer="④",
    figure=FIG("좌표평면: 초점 F′·F(x축)인 쌍곡선과 초점 G·G′(y축)인 쌍곡선(꼭짓점 ±1), 제1사분면 교점 P, 제3사분면 교점 Q, 사각형 PGQF"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG_REVIEW + ": 두 쌍곡선·사각형 좌표평면 그림 / " + PRIME + "(F′, G′)",
    note="출처 [2015년 6월 고3 이과 19번/4점]. Q=−P: PG·PG′=8, PG′−PG=2 → PG=2, PG′=4; PF·PF′=4, PF′−PF=2 → PF=√5−1, PF′=√5+1 → 둘레 6+2√5 → ④ = 빠른정답 ✓.")

# p74
add(id="51216d6b", qtype="short",
    question="그림과 같이 두 초점이 F, F′인 쌍곡선 [[frac(pow(x,2), 12) - frac(pow(y,2), 24) = 1]] 위의 점 P에 대하여 직선 FP와 직선 F′P에 동시에 접하고 중심이 [[y]]축 위에 있는 원 [[C]]가 있다. 직선 F′P와 원 [[C]]의 접점 Q에 대하여 F′Q = [[5 sqrt(3)]]일 때, [[pow(seg(FP), 2)]] + F′P²의 값을 구하시오. (단, F′P < [[seg(FP)]])",
    choices=None, derived_answer="174",
    figure=FIG("좌표평면: 쌍곡선(초점 F′·F), 왼쪽 가지 위의 점 P, 직선 FP·F′P에 접하고 중심이 y축 위인 원 C, 직선 F′P와 원의 접점 Q"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·접하는 원 좌표평면 그림 / " + PRIME + "(F′, 선분 F′Q·F′P 윗줄 생략)",
    note="FP+F′P=2·5√3=10√3, FP−F′P=4√3 → FP=7√3, F′P=3√3 → 147+27=174. 빠른정답 146과 불일치.")

# p77
add(id="ae9e548f", qtype="choice",
    question="그림과 같이 두 초점이 [[F(0, c)]], F′[[point(0, -c)]] ([[c > 0]])인 쌍곡선 [[frac(pow(x,2), 12) - frac(pow(y,2), 4) = -1]]이 있다. 쌍곡선 위의 제1사분면에 있는 점 P와 쌍곡선 위의 제3사분면에 있는 점 Q가 PF′ − QF′ = 5, [[seg(PF) = frac(2,3) seg(QF)]]를 만족시킬 때, [[seg(PF) + seg(QF)]]의 값은?",
    choices=["10", "[[frac(35,3)]]", "[[frac(40,3)]]", "15", "[[frac(50,3)]]"], derived_answer="④",
    figure=FIG("좌표평면: y축 위에 초점 F(위)·F′(아래)를 갖는 쌍곡선(위·아래 두 가지), 제1사분면 점 P(위 가지), 제3사분면 점 Q(아래 가지), 선분 PF·PF′·QF·QF′"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·사각형 좌표평면 그림 / " + PRIME + "(F′, 선분 PF′·QF′ 윗줄 생략)",
    note="출처 [2023년 3월 고3 기하 27번/3점]. a=2: PF′=PF+4, QF′=QF−4 → QF−PF=3, PF=(2/3)QF → QF=9, PF=6 → 15 → ④. 빠른정답 174와 불일치.")

# p78
add(id="f4dcdb52", qtype="short",
    question="다음 그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 쌍곡선이 있다. 이 쌍곡선 위의 제2사분면에 있는 점 P와 이 쌍곡선 위의 제3사분면에 있는 점 Q에 대하여 직선 PQ가 점 F′를 지나고 OF′ = [[seg(OP)]]이다.\n세 점 P, F, Q를 지나는 원의 넓이가 [[frac(169,4) pi]]이고 [[seg(FQ)]] : F′Q = [[ratio(13, 3)]]일 때, [[pow(c,2)]] · PF′의 값을 구하시오.\n(단, O는 원점이다.)",
    choices=None, derived_answer="74",
    figure=FIG("좌표평면: 쌍곡선(초점 F′·F), 왼쪽 가지 위의 점 P(제2사분면)·Q(제3사분면), F′을 지나는 직선 PQ, 세 점 P·F·Q를 지나는 원"),
    difficulty_est=4, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·원·직선 복합 좌표평면 그림 / " + PRIME + "(F′, 선분 OF′·F′Q·PF′ 윗줄 생략)",
    note="출처 [2025년 5월 고3 기하 29번 변형]. OP=c → ∠FPQ=90°, FQ=지름=13, F′Q=3 → a=5; PF′=u: (u+10)²+(u+3)²=169 → u=2, PF=12 → 4c²=148, c²=37 → 74. 빠른정답 2와 불일치.")

# p79
add(id="64742f13", qtype="short",
    question="그림과 같이 두 초점이 F, F′인 쌍곡선 [[frac(pow(x,2), 8) - frac(pow(y,2), 17) = 1]] 위의 점 P에 대하여 직선 FP와 직선 F′P에 동시에 접하고 중심이 [[y]]축 위에 있는 원 [[C]]가 있다. 직선 F′P와 원 [[C]]의 접점 Q에 대하여 F′Q = [[5 sqrt(2)]]일 때, [[pow(seg(FP), 2)]] + F′P²의 값을 구하시오. (단, F′P < [[seg(FP)]])",
    choices=None, derived_answer="116",
    figure=FIG("좌표평면: 쌍곡선(초점 F′·F), 왼쪽 가지 위의 점 P, 직선 FP·F′P에 접하고 중심이 y축 위인 원 C, 직선 F′P와 원의 접점 Q"),
    difficulty_est=3, confidence=0.8,
    needs_review=FIG_REVIEW + ": 쌍곡선·접하는 원 좌표평면 그림 / " + PRIME + "(F′, 선분 F′Q·F′P 윗줄 생략)",
    note="출처 [2017년 11월 고3 이과 27번/4점]. FP+F′P=10√2, FP−F′P=4√2 → FP=7√2, F′P=3√2 → 98+18=116. 빠른정답 68과 불일치.")

# p80
add(id="d7f18c94", qtype="choice",
    question="쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 15) = 1]]의 두 초점을 [[F(8, 0)]], F′[[point(-8, 0)]]이라 하자.\n쌍곡선 위의 점 P에 대하여 |[[seg(PF)]] − PF′|의 값은?",
    choices=["10", "11", "12", "13", "14"], derived_answer="⑤",
    figure=None, difficulty_est=1, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 PF′ 윗줄 생략, 절댓값 기호 텍스트)",
    note="출처 [2017년 7월 고3 이과 7번 변형]. a²=64−15=49 → 2a=14 → ⑤. 빠른정답 4와 불일치.")

# p81
add(id="cc9a62a5", qtype="choice",
    question="두 점 [[F(4, 3)]], F′[[point(-2, 3)]]에 대하여 |[[seg(PF)]] − PF′| = 4를 만족시키는 점 P의 자취의 방정식은?",
    choices=["[[frac(pow(x - 1, 2), 4) - frac(pow(y - 3, 2), 5) = -1]]", "[[frac(pow(x - 1, 2), 4) - frac(pow(y - 3, 2), 5) = 1]]", "[[frac(pow(x - 1, 2), 4) + frac(pow(y - 3, 2), 5) = 1]]", "[[frac(pow(x - 1, 2), 5) - frac(pow(y - 3, 2), 4) = 1]]", "[[frac(pow(x - 1, 2), 5) - frac(pow(y - 3, 2), 4) = -1]]"], derived_answer="②",
    figure=None, difficulty_est=1, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 PF′ 윗줄 생략, 절댓값 기호 텍스트)",
    note="중심 (1,3), c=3, a=2, b²=5 → (x−1)²/4−(y−3)²/5=1 → ② = 빠른정답 ✓.")

# p82
add(id="2104d5a6", qtype="choice",
    question="두 점 [[F(5, 0)]], F′[[point(-5, 0)]]에 대하여 점 P가 |[[seg(PF)]] − PF′| = 4를 만족시킬 때, 점 P가 나타내는 도형의 방정식은?",
    choices=["[[frac(pow(x,2), 4) - frac(pow(y,2), 5) = 1]]", "[[frac(pow(x,2), 4) - frac(pow(y,2), 21) = 1]]", "[[frac(pow(x,2), 4) - frac(pow(y,2), 21) = -1]]", "[[frac(pow(x,2), 16) - frac(pow(y,2), 21) = 1]]", "[[frac(pow(x,2), 16) - frac(pow(y,2), 21) = -1]]"], derived_answer="②",
    figure=None, difficulty_est=1, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 PF′ 윗줄 생략, 절댓값 기호 텍스트)",
    note="c=5, a=2, b²=21 → x²/4−y²/21=1 → ②. 빠른정답 116과 불일치.")

# p83
add(id="64211523", qtype="short",
    question="좌표평면 위의 두 점 [[A(10, 0)]], [[B(-10, 0)]]에 대하여 [[abs(seg(PA) - seg(PB)) = 16]]을 만족시키는 점 P가 나타내는 도형의 방정식이 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]]일 때, [[pow(a,2) - pow(b,2)]]의 값을 구하시오.\n(단, [[a]], [[b]]는 상수이다.)",
    choices=None, derived_answer="28", figure=None, difficulty_est=1, confidence=0.9,
    note="c=10, a=8 → a²=64, b²=36 → 28. 빠른정답 5와 불일치.")

# p93
add(id="2ffc5a15", qtype="choice",
    question="쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), 3) = 1]]의\n두 초점 [[point(2 sqrt(3), 0)]], [[point(-2 sqrt(3), 0)]]을 각각 F, F′이라 하자. 이 쌍곡선 위를 움직이는 점 [[P(x, y)]] ([[x > 0]])에 대하여 선분 F′P 위의 점 Q가 [[seg(FP) = seg(PQ)]]를 만족시킬 때, 점 Q가 나타내는 도형 전체의 길이는?",
    choices=["[[pi]]", "[[sqrt(3) pi]]", "[[2 pi]]", "[[3 pi]]", "[[2 sqrt(3) pi]]"], derived_answer="③",
    figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PRIME + "(F′, 선분 F′P)",
    note="출처 [2006년 9월 고3 이과 9번]. F′Q=F′P−FP=6 → F′ 중심 반지름 6 원 위, 점근선 기울기 ±1/√3 → 중심각 π/3 → 호 길이 2π → ③. 빠른정답 5와 불일치.")

# ===================== 구의 방정식 =====================
# p1
add(id="ac53b515", qtype="short",
    question="중심이 점 [[vcomp(-3, 1, -2)]]이고 점 [[vcomp(1, 3, -5)]]를 지나는 구의 방정식이 [[pow(x,2) + pow(y,2) + pow(z,2) + a x + b y + c z + d = 0]]일 때, 상수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a + b + c + d]]의 값을 구하시오.",
    choices=None, derived_answer="-7", figure=None, difficulty_est=1, confidence=0.9,
    note="r²=16+4+9=29 → (x+3)²+(y−1)²+(z+2)²=29 → a=6,b=−2,c=4,d=−15 → −7. 빠른정답 없음.")

# p7
add(id="22212b70", qtype="short",
    question="중심이 점 [[vcomp(3, -1, 4)]]이고 점 [[vcomp(1, -3, 5)]]를 지나는 구의 방정식이 [[pow(x,2) + pow(y,2) + pow(z,2) + a x + b y + c z + d = 0]]일 때, 상수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a + b + c + d]]의 값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=1, confidence=0.9,
    note="r²=4+4+1=9 → a=−6,b=2,c=−8,d=17 → 5. 빠른정답 없음.")

# p8
add(id="06bf81be", qtype="short",
    question="중심이 점 [[vcomp(1, -2, 3)]]이고 점 [[vcomp(-1, 1, 1)]]을 지나는 구의 방정식이 [[pow(x,2) + pow(y,2) + pow(z,2) + a x + b y + c z + d = 0]]일 때, 상수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a + b + c + d]]의 값을 구하시오.",
    choices=None, derived_answer="-7", figure=None, difficulty_est=1, confidence=0.9,
    note="r²=4+9+4=17 → a=−2,b=4,c=−6,d=−3 → −7. 빠른정답 없음.")

# p10
add(id="c3b2d8fe", qtype="choice",
    question="두 점 [[vcomp(3, 2, 0)]], [[vcomp(-7, 10, 6)]]을 지름의 양 끝 점으로 하는 구가 직선 [[l]]과 두 점 A, B에서 만나고, [[seg(AB) = 2 sqrt(14)]]이다. 구의 중심을 C라 할 때, 삼각형 ABC의 넓이는?",
    choices=["16", "[[5 sqrt(14)]]", "20", "[[6 sqrt(14)]]", "24"], derived_answer="④",
    figure=None, difficulty_est=2, confidence=0.9,
    note="C(−2,6,3), r=5√2; 현 절반 √14 → 거리 √(50−14)=6 → 넓이 6√14 → ④ = 빠른정답 ✓.")

# p11
add(id="76a63c40", qtype="short",
    question="두 점 [[A(2, 1, sqrt(15))]], [[B(4, 7, -sqrt(15))]]를 지름의 양 끝 점으로 하는 구 [[S]]가 있다. 구 [[S]] 위의 한 점 [[C(0, 0, 0)]]에 대하여 삼각형 ABC의 넓이를 구하시오.",
    choices=None, derived_answer="20", figure=None, difficulty_est=2, confidence=0.9,
    note="∠ACB=90°, CA=2√5, CB=4√5 → 넓이 20 = 빠른정답 ✓.")

# p12
add(id="4f0bd6be", qtype="choice",
    question="두 점 [[vcomp(7, -8, 4)]], [[vcomp(1, -3, -1)]]을 지름의 양 끝 점으로 하는 구가 직선 [[l]]과 두 점 A, B에서 만나고, [[seg(AB) = sqrt(22)]]이다. 구의 중심을 C라 할 때, 삼각형 ABC의 넓이는?",
    choices=["[[4 sqrt(5)]]", "[[2 sqrt(21)]]", "[[2 sqrt(22)]]", "[[3 sqrt(22)]]", "[[4 sqrt(22)]]"], derived_answer="③",
    figure=None, difficulty_est=2, confidence=0.9,
    note="r²=86/4=43/2, 현 절반² 11/2 → 거리 4 → 넓이 (1/2)·√22·4=2√22 → ③ = 빠른정답 ✓.")

# p18
add(id="6348c933", qtype="short",
    question="중심의 좌표가 [[vcomp(8, k, 5)]]이고 [[z]]축에 접하는 구의 반지름의 길이가 10일 때, 양수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="√(64+k²)=10 → k=6. 빠른정답 3과 불일치.")

# p20
add(id="2bb06821", qtype="short",
    question="중심의 좌표가 [[vcomp(3, -2, k)]]이고 [[y]]축에 접하는 구의 반지름의 길이가 5일 때, 양수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="√(9+k²)=5 → k=4. 빠른정답 3과 불일치.")

# p22
add(id="f8220b6b", qtype="choice",
    question="반지름의 길이가 8이고 [[x]]축, [[y]]축, [[z]]축에 동시에 접하는 구의 중심의 좌표를 [[vcomp(a, b, c)]]라 할 때, [[pow(a,2) + pow(b,2) + pow(c,2)]]의 값은?",
    choices=["48", "60", "72", "84", "96"], derived_answer="⑤",
    figure=None, difficulty_est=2, confidence=0.9,
    note="a²=b²=c²=32 → 96 → ⑤. 빠른정답 13과 불일치.")

# p26
add(id="7b4ec5d9", qtype="choice",
    question="점 [[A(4, -4, 5)]]와 구 [[pow(x,2) + pow(y,2) + pow(z,2) = 16]] 위의 점 B에 대하여 선분 AB의 중점의 자취는 구이다. 이 구의 중심의 좌표가 [[vcomp(a, b, c)]]이고 반지름의 길이가 [[r]]일 때, [[a + b + c + r]]의 값은?",
    choices=["3", "[[frac(7,2)]]", "4", "[[frac(9,2)]]", "5"], derived_answer="④",
    figure=None, difficulty_est=2, confidence=0.9,
    note="중점 M: |2M−A|=4 → 중심 (2,−2,5/2), r=2 → 9/2 → ④. 빠른정답 2와 불일치.")

# p33
add(id="df09cc47", qtype="choice",
    question="좌표공간에 두 점 [[A(a, 0, 0)]], [[B(0, 10 sqrt(2), 0)]]과 구 [[S]]: [[pow(x,2) + pow(y,2) + pow(z,2) = 100]]이 있다. [[angle(APO) = frac(pi,2)]]인 구 [[S]] 위의 모든 점 P가 나타내는 도형을 [[sub(C,1)]], [[angle(BQO) = frac(pi,2)]]인 구 [[S]] 위의 모든 점 Q가 나타내는 도형을 [[sub(C,2)]]라 하자. [[sub(C,1)]]과 [[sub(C,2)]]가 서로 다른 두 점 [[sub(N,1)]], [[sub(N,2)]]에서 만나고 cos(∠[[sub(N,1)]]O[[sub(N,2)]]) = [[frac(3,5)]]일 때, [[a]]의 값은?\n(단, [[a > 10 sqrt(2)]]이고, O는 원점이다.)",
    choices=["[[frac(10,3) sqrt(30)]]", "[[frac(15,4) sqrt(30)]]", "[[frac(25,6) sqrt(30)]]", "[[frac(55,12) sqrt(30)]]", "[[5 sqrt(30)]]"], derived_answer="①",
    figure=FIG("좌표공간: 원점 중심 구 S, x축 위의 점 A, y축 위의 점 B, 구 위의 점 P·Q, 구 위의 두 원 C₁·C₂(점선)"),
    difficulty_est=4, confidence=0.8,
    needs_review=FIG_REVIEW + ": 좌표공간의 구·원 입체 그림 / " + PRIME + "(∠N₁ON₂ 텍스트 혼합)",
    note="출처 [2024년 9월 고3 기하 28번/4점]. cos∠AOP=10/a, cos∠BOQ=1/√2; cos∠N₁ON₂=2(100/a²)+2(1/2)−1=200/a²=3/5 → a²=1000/3 → a=10√30/3 → ①. 빠른정답 5와 불일치.")

# p34
add(id="b7f4395c", qtype="choice",
    question="좌표공간에 두 점 [[A(a, 0, 0)]], [[B(0, 9, 0)]]과 구 [[S]]: [[pow(x,2) + pow(y,2) + pow(z,2) = 36]]이 있다. [[angle(APO) = frac(pi,2)]]인 구 [[S]] 위의 모든 점 P가 나타내는 도형을 [[sub(C,1)]], [[angle(BQO) = frac(pi,2)]]인 구 [[S]] 위의 모든 점 Q가 나타내는 도형을 [[sub(C,2)]]라 하자. [[sub(C,1)]]과 [[sub(C,2)]]가 서로 다른 두 점 [[sub(N,1)]], [[sub(N,2)]]에서 만나고 cos(∠[[sub(N,1)]]O[[sub(N,2)]]) = [[frac(5,9)]]일 때, [[a]]의 값은?\n(단, [[a > 9]]이고, O는 원점이다.)",
    choices=["[[4 sqrt(3)]]", "[[5 sqrt(3)]]", "[[6 sqrt(3)]]", "[[5 sqrt(5)]]", "[[6 sqrt(5)]]"], derived_answer="③",
    figure=FIG("좌표공간: 원점 중심 구 S, x축 위의 점 A, y축 위의 점 B, 구 위의 점 P·Q, 구 위의 두 원 C₁·C₂(점선)"),
    difficulty_est=4, confidence=0.8,
    needs_review=FIG_REVIEW + ": 좌표공간의 구·원 입체 그림 / " + PRIME + "(∠N₁ON₂ 텍스트 혼합)",
    note="출처 [2024년 9월 고3 기하 28번 변형]. cos∠N₁ON₂=2(36/a²)+2(4/9)−1=72/a²−1/9=5/9 → a²=108 → a=6√3 → ③. 빠른정답 4와 불일치.")

# p38
add(id="bc03bab4", qtype="short",
    question="점 [[P(3, 2, 1)]]에서 구 [[pow(x - 1, 2) + pow(y + 3, 2) + pow(z - 2, 2) = 14]]에 그은 접선의 길이를 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="PC²=4+25+1=30 → √(30−14)=4. 빠른정답 3과 불일치.")
