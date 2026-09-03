# -*- coding: utf-8 -*-
# esc_sonnet_m3-2_6of6 — 이미지 기준 전사 (23 항목 / 21쪽)
# 삼각비의 활용(1) 길이 p71~p99: 전부 정보성 기하 도형(삼각형·평행사변형) → unsupported + needs_review
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ---------------- 삼각비의 활용(1) 길이 p71 (회전체, 45°·60°, AC=12)
add(id="c6118a07", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(45)]], [[angle(B) = deg(60)]], [[seg(AC) = 12]]인 [[tri(ABC)]]를 "
              "직선 AB를 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피는 [[(a sqrt(2) + b sqrt(6)) pi]]이다. "
              "이때 [[frac(a,b)]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수이다.)"),
    choices=None, derived_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": "세로 직선 l(회전축, 위쪽에 회전 화살표) 위에 A(위)·B(아래). 오른쪽에 점 C. 삼각형 ABC 색칠(연두). ∠A=45°(A에 표시), ∠B=60°(B에 표시), AC=12(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 회전축 직선+삼각형 도형",
    note="C에서 AB에 내린 수선 h=6√2, AH=6√2, BH=2√6 → V=(1/3)π·72·(6√2+2√6)=(144√2+48√6)π → a/b=3 = 빠른정답 ✓.")

# ---------------- p72 (평행사변형, AB=2√3)
add(id="d6cb4142", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = 2 sqrt(3)]], [[angle(ABC) = deg(45)]], [[angle(ACB) = deg(60)]]인 평행사변형 ABCD에서 "
              "[[tan(angle(CBD))]]의 값은?"),
    choices=["[[frac(6 - sqrt(3), 11)]]", "[[frac(6 - sqrt(2), 11)]]", "[[frac(7 - sqrt(3), 11)]]",
             "[[frac(7 - sqrt(2), 11)]]", "[[frac(6, 11)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(B 좌하, C 우하, A 좌상, D 우상). 대각선 AC·BD. AB=2√3(점선 치수), ∠ABC=45°(B에 표시), ∠ACB=60°(C에 표시)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형+대각선 도형",
    note="A에서 BC에 내린 수선 √6, BH=√6, CH=√2 → D=(2√6+√2, √6) → tan∠CBD=√3/(2√3+1)=(6−√3)/11 → ① (빠른정답 없음, 풀이 답).")

# ---------------- p73 (평행사변형, AB=6√2)
add(id="6ad68128", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = 6 sqrt(2)]], [[angle(ABC) = deg(45)]], [[angle(ACB) = deg(60)]]인 평행사변형 ABCD에서 "
              "[[tan(angle(CBD))]]의 값은?"),
    choices=["[[frac(5 - sqrt(3), 22)]]", "[[frac(5 - sqrt(2), 22)]]", "[[frac(6 - sqrt(3), 11)]]",
             "[[frac(6 - sqrt(2), 11)]]", "[[frac(7 - sqrt(2), 11)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(B 좌하, C 우하, A 좌상, D 우상). 대각선 AC·BD. AB=6√2(점선 치수), ∠ABC=45°(B에 표시), ∠ACB=60°(C에 표시)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형+대각선 도형",
    note="수선 6, BH=6, CH=2√3 → D=(12+2√3, 6) → tan=3/(6+√3)=(6−√3)/11 → ③ (빠른정답 없음, 풀이 답).")

# ---------------- p74 (평행사변형, AB=√6)
add(id="0fe47cf3", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = sqrt(6)]], [[angle(ABC) = deg(45)]], [[angle(ACB) = deg(60)]]인 평행사변형 ABCD에서 "
              "[[tan(angle(CBD))]]의 값은?"),
    choices=["[[frac(5 - sqrt(5), 22)]]", "[[frac(3, 22)]]", "[[frac(6 - sqrt(5), 22)]]",
             "[[frac(2, 11)]]", "[[frac(6 - sqrt(3), 11)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(B 좌하, C 우하, A 좌상, D 우상). 대각선 AC·BD. AB=√6(점선 치수), ∠ABC=45°(B에 표시), ∠ACB=60°(C에 표시)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형+대각선 도형",
    note="수선 √3, BH=√3, CH=1 → D=(2√3+1, √3) → tan=√3/(2√3+1)=(6−√3)/11 → ⑤. 빠른정답 3과 불일치.")

# ---------------- p75 (회전체, 30°·45°, AC=6)
add(id="512ee91e", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(30)]], [[angle(B) = deg(45)]], [[seg(AC) = 6]]인 [[tri(ABC)]]를 "
              "직선 AB를 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피는 [[(a sqrt(3) + b) pi]]이다. "
              "이때 [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수이다.)"),
    choices=None, derived_answer="18",
    figure=[{"fn": "unsupported", "args": {"raw": "세로 직선 l(회전축, 위쪽에 회전 화살표) 위에 A(위)·B(아래). 오른쪽에 점 C. 삼각형 ABC 색칠(분홍). ∠A=30°(A에 표시), ∠B=45°(B에 표시), AC=6(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 회전축 직선+삼각형 도형",
    note="h=3, AH=3√3, BH=3 → V=(1/3)π·9·(3√3+3)=(9√3+9)π → a+b=18 (빠른정답 없음, 풀이 답).")

# ---------------- p76 (회전체, 60°·45°, AC=6√3)
add(id="9c5eb1b2", qtype="short",
    question=("다음 그림과 같이 [[angle(A) = deg(60)]], [[angle(B) = deg(45)]], [[seg(AC) = 6 sqrt(3)]]인 [[tri(ABC)]]를 "
              "직선 AB를 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피는 [[(a sqrt(3) + b) pi]]이다. "
              "이때 유리수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="324",
    figure=[{"fn": "unsupported", "args": {"raw": "세로 직선 l(회전축, 위쪽에 회전 화살표) 위에 A(위)·B(아래). 오른쪽에 점 C. 삼각형 ABC 색칠(하늘색). ∠A=60°(A에 표시), ∠B=45°(B에 표시), AC=6√3(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 회전축 직선+삼각형 도형",
    note="h=9, AH=3√3, BH=9 → V=(1/3)π·81·(3√3+9)=(81√3+243)π → a+b=324 (빠른정답 없음, 풀이 답).")

# ---------------- 예각삼각형의 높이 p79
add(id="6233fd5c", qtype="choice",
    question="다음 그림에서 [[angle(B) = deg(45)]]이고 [[angle(C) = deg(30)]]일 때, [[seg(AH)]]의 길이는?",
    choices=["[[8(sqrt(2) - 1)]] cm", "[[8(sqrt(3) - 1)]] cm", "[[8]] cm", "[[8(sqrt(5) - 1)]] cm", "[[8(sqrt(6) - 1)]] cm"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(B 좌, C 우, A 위). A에서 BC에 내린 수선의 발 H(직각 표시). ∠B=45°, ∠C=30°, BC=16cm(아래 점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+수선 도형",
    note="h(1+√3)=16 → h=8(√3−1) → ②. 빠른정답 324와 불일치(정렬 어긋남).")

# ---------------- p84 (BC=8, △ADM 넓이)
add(id="990b00d0", qtype="choice",
    question=("다음 그림의 [[tri(ABC)]]에서 [[angle(B) = deg(45)]], [[angle(C) = deg(30)]]이고 [[seg(BC) = 8]]이다. "
              "[[perp(seg(AD), seg(BC))]]이고 점 M이 [[seg(BC)]]의 중점일 때, [[tri(ADM)]]의 넓이는?"),
    choices=["[[frac(3 sqrt(3) - 5, 2)]]", "[[3 sqrt(3) - 5]]", "[[2(3 sqrt(3) - 5)]]", "[[4(3 sqrt(3) - 5)]]", "[[8(3 sqrt(3) - 5)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(B 좌, C 우, A 위). A에서 BC에 내린 수선의 발 D(직각 표시), BC의 중점 M(D의 오른쪽). 삼각형 ADM 색칠(연두). ∠B=45°, ∠C=30°, BC=8(아래 점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+수선+중점 도형",
    note="AD=4(√3−1), DM=4−4(√3−1)=4(2−√3) → 넓이 8(3√3−5) → ⑤ (빠른정답 없음, 풀이 답).")

# ---------------- p86 (BC=10, △ADM 넓이)
add(id="b3f5b656", qtype="choice",
    question=("다음 그림의 [[tri(ABC)]]에서 [[angle(B) = deg(45)]], [[angle(C) = deg(30)]]이고 [[seg(BC) = 10]]이다. "
              "[[perp(seg(AD), seg(BC))]]이고 점 M이 [[seg(BC)]]의 중점일 때, [[tri(ADM)]]의 넓이는?"),
    choices=["[[frac(5(3 sqrt(3) - 5), 4)]]", "[[frac(5(3 sqrt(3) - 5), 2)]]", "[[5(3 sqrt(3) - 5)]]",
             "[[frac(15(3 sqrt(3) - 5), 2)]]", "[[frac(25(3 sqrt(3) - 5), 2)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(B 좌, C 우, A 위). A에서 BC에 내린 수선의 발 D(직각 표시), BC의 중점 M(D의 오른쪽). 삼각형 ADM 색칠(보라). ∠B=45°, ∠C=30°, BC=10(아래 점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+수선+중점 도형",
    note="AD=5(√3−1), DM=5(2−√3) → 넓이 (25/2)(3√3−5) → ⑤. 빠른정답 '7.04 m'과 불일치(정렬 어긋남).")

# ---------------- 둔각삼각형의 높이 p90
add(id="e93d082a", qtype="short",
    question=("다음 그림과 같이 한 내각의 크기가 [[deg(23)]]인 삼각형 ABC의 넓이를 구하려고 한다. "
              "점 A에서 변 BC의 연장선 위에 내린 수선의 발을 H, [[seg(AH) = x]]라 할 때, [[tri(ABC)]]의 넓이를 구하시오. "
              "(단, [[tan(deg(23)) = 0.4]]로 계산한다.)"),
    choices=None, derived_answer="27",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC 색칠(연두): B 좌하, C 우하, A 우상. BC 연장선 위 H(직각 표시), AH=x(점선 치수). ∠B=23°, ∠ACH=45°, BC=9(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형+연장선 수선 도형",
    note="BH=x/0.4=2.5x, CH=x → 1.5x=9, x=6 → 넓이 ½·9·6=27. 빠른정답 '120.5 m'과 불일치(정렬 어긋남).")

# ---------------- p91
add(id="f7b802fb", qtype="choice",
    question=("다음 그림과 같이 삼각형 ABC의 점 A에서 [[seg(BC)]]의 연장선에 내린 수선의 발을 H라 하자. "
              "[[angle(B) = deg(30)]], [[angle(ACH) = deg(45)]], [[seg(BC) = 18]] m일 때, [[seg(AH)]]의 길이는?"),
    choices=["[[9(sqrt(2) + 1)]] m", "[[9(sqrt(2) - 1)]] m", "[[9(sqrt(3) + 1)]] m", "[[9(sqrt(3) + 2)]] m", "[[9(sqrt(3) + 3)]] m"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC: B 좌하, C 우하, A 우상. BC 연장선 위 H(직각 표시), AH 점선. ∠B=30°, ∠ACH=45°, BC=18m(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형+연장선 수선 도형",
    note="h√3−h=18 → h=9(√3+1) → ③ (빠른정답 없음, 풀이 답).")

# ---------------- p94
add(id="bd85c4e7", qtype="choice",
    question="다음 그림에서 [[seg(BC) = 20]] cm, [[angle(BAC) = deg(15)]], [[angle(B) = deg(30)]]일 때, [[tri(ABC)]]의 넓이는?",
    choices=["[[100(sqrt(3) - sqrt(2))]] cm²", "[[100(sqrt(3) - 1)]] cm²", "[[100]] cm²", "[[100(sqrt(3) + 1)]] cm²", "[[100(sqrt(3) + sqrt(2))]] cm²"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC 색칠(보라): B 좌하, C 우하, A 우상. BC 연장선 위 H(직각 표시), AH 점선. ∠BAC=15°, ∠B=30°, BC=20cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형+연장선 수선 도형",
    note="∠ACH=45°, h(√3−1)=20 → h=10(√3+1) → 넓이 ½·20·h=100(√3+1) → ④ (빠른정답 없음, 풀이 답).")

# ---------------- p99 (한 쪽에 문항 2개, id 2개)
add(id="f4e70500", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[angle(ACB) = deg(120)]], [[seg(BC) = 9 sqrt(2)]] cm, "
              "[[tan(B) = frac(sqrt(3), 4)]]일 때, [[seg(AH)]]의 길이는?"),
    choices=["[[2 sqrt(6)]] cm", "[[frac(5 sqrt(6), 2)]] cm", "[[3 sqrt(6)]] cm", "[[frac(7 sqrt(6), 2)]] cm", "[[4 sqrt(6)]] cm"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC: B 좌하, C 우하, A 우상. BC 연장선 위 H(직각 표시). ∠ACB=120°(C에 표시), BC=9√2cm(점선 치수)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형+연장선 수선 도형",
    note="p99 위 문항. CH=h/√3, BH=4h/√3 → √3h=9√2 → h=3√6 → ③ (빠른정답 없음, 풀이 답).")

add(id="321e2248", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABH)]]에서 [[angle(ACB) = deg(135)]], [[seg(BC) = 5]] cm, "
              "[[tan(B) = frac(4, 9)]]일 때, [[seg(AH)]]의 길이는?"),
    choices=["[[3]] cm", "[[4]] cm", "[[5]] cm", "[[6]] cm", "[[7]] cm"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC: B 좌하, C 우하, A 우상. BC 연장선 위 H(직각 표시). ∠ACB=135°(C에 표시), BC=5cm(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형+연장선 수선 도형",
    note="p99 아래 문항(원문 '△ABH에서' 그대로). CH=h, BH=9h/4 → 5h/4=5 → h=4 → ② (빠른정답 없음, 풀이 답).")

# ---------------- 산포도 p10 (편차)
add(id="bc334e13", qtype="short",
    question="어떤 자료의 편차가 다음과 같을 때, [[x]]의 값을 구하시오.\n[[-5]], [[-2]], [[6]], [[x]], [[3]], [[-9]]",
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="편차 합 0: −5−2+6+3−9=−7 → x=7 = 빠른정답 ✓.")

# ---------------- 산포도 p57
add(id="b6dc6115", qtype="short",
    question=("4개의 변량 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]]의 평균과 표준편차가 각각 5와 [[sqrt(2)]]일 때, "
              "변량 [[pow(sub(x,1),2)]], [[pow(sub(x,2),2)]], [[pow(sub(x,3),2)]], [[pow(sub(x,4),2)]]의 평균을 구하시오."),
    choices=None, derived_answer="27", figure=None, difficulty_est=2, confidence=0.9,
    note="분산 2 = (x²의 평균) − 5² → 27 = 빠른정답 ✓.")

# ---------------- 산포도 p60
add(id="19a670ed", qtype="choice",
    question=("변량 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]], [[sub(x,5)]], [[sub(x,6)]], [[sub(x,7)]]의 평균을 [[m]], 표준편차를 [[s]]라 할 때, "
              "[[frac(sub(x,1) - m, s)]], [[frac(sub(x,2) - m, s)]], [[frac(sub(x,3) - m, s)]], [[frac(sub(x,4) - m, s)]], "
              "[[frac(sub(x,5) - m, s)]], [[frac(sub(x,6) - m, s)]], [[frac(sub(x,7) - m, s)]]의 평균과 표준편차를 차례대로 구하면?"),
    choices=["[[m]], [[s]]", "[[0]], [[s]]", "[[1]], [[s]]", "[[1]], [[0]]", "[[0]], [[1]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="표준화 변량: 평균 0, 표준편차 1 → ⑤ = 빠른정답 ✓.")

# ---------------- 산포도 p63
add(id="1f2011b8", qtype="short",
    question=("변량 [[sub(x,1)]], [[sub(x,2)]], ⋯, [[sub(x,n)]]의 표준편차가 5일 때, "
              "변량 [[2 sub(x,1) + 2]], [[2 sub(x,2) + 2]], ⋯, [[2 sub(x,n) + 2]]의 표준편차를 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=1, confidence=0.9,
    note="표준편차 |2|·5=10 = 빠른정답 ✓.")

# ---------------- 산포도 p65
add(id="131ef6d0", qtype="choice",
    question=("6개의 변량 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]], [[sub(x,5)]], [[sub(x,6)]]의 분산이 3일 때, "
              "6개의 변량 [[2 sub(x,1) - 2]], [[2 sub(x,2) - 2]], [[2 sub(x,3) - 2]], [[2 sub(x,4) - 2]], [[2 sub(x,5) - 2]], [[2 sub(x,6) - 2]]의 분산은?"),
    choices=["[[4]]", "[[6]]", "[[8]]", "[[10]]", "[[12]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="분산 2²·3=12 → ⑤. 빠른정답 4(④ 10)와 불일치.")

# ---------------- 산포도 p70 (두 집단 전체의 평균)
add(id="dd8290e5", qtype="short",
    question=("어느 학급의 남학생과 여학생을 대상으로 일주일 동안의 인터넷 사용시간을 조사하였더니 남학생, 여학생, "
              "전체 학생에 대한 인터넷 사용시간의 평균이 각각 10시간, 6시간, [[8.5]]시간이었다. "
              "이 학급의 남학생 수와 여학생 수의 비가 [[p]] : [[q]]일 때, [[p]]와 [[q]]의 곱을 구하시오. "
              "(단, [[p]], [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="15", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2010년 4월 고3 이과 확률과 통계 30번]. 10p+6q=8.5(p+q) → p:q=5:3 → pq=15 = 빠른정답 ✓.")

# ---------------- 산포도 p83 (두 집단 전체의 분산)
add(id="c57631cd", qtype="choice",
    question=("10개의 변량 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], ⋯, [[sub(x,10)]]이 있다. "
              "이 중에서 변량 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]]의 평균은 4, 분산은 3이고 "
              "변량 [[sub(x,4)]], [[sub(x,5)]], [[sub(x,6)]], ⋯, [[sub(x,10)]]의 평균은 4, 분산은 8일 때, 전체 10개의 변량의 분산은?"),
    choices=["[[6.2]]", "[[6.3]]", "[[6.4]]", "[[6.5]]", "[[6.6]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="평균이 같으므로 전체 분산=(3·3+7·8)/10=6.5 → ④. 빠른정답 52와 불일치(정렬 어긋남).")

# ---------------- 대푯값 p19 (id 2개, 같은 문항 — 과정 상자 포함)
dup(["59d4dd99", "899aad66"], qtype="short",
    question=("자료 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], ⋯, [[sub(x,10)]]에 대하여 다음 과정을 차례로 시행하였다. "
              "위의 과정을 시행한 결과 [[sub(x,1)]]과 [[sub(x,2)]]의 평균이 5이고, 자료가 하나씩 추가될 때마다 평균이 2씩 증가하였다. "
              "이때 [[sub(x,10)]]의 값을 구하여라.\n"
              "처음 두 수 [[sub(x,1)]]과 [[sub(x,2)]]의 평균을 구한다.\n"
              "[[sub(x,3)]]을 추가하여 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]]의 평균을 구한다.\n"
              "[[sub(x,4)]]를 추가하여 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], [[sub(x,4)]]의 평균을 구한다.\n"
              "⋯\n"
              "[[sub(x,10)]]을 추가하여 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], ⋯, [[sub(x,10)]]의 평균을 구한다."),
    choices=None, derived_answer="39", figure=None, difficulty_est=2, confidence=0.9,
    note="n개 평균 2n+1, 합 n(2n+1) → x_n=4n−1 → x₁₀=39 (빠른정답 없음, 풀이 답).")
