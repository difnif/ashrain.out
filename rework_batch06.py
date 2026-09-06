# -*- coding: utf-8 -*-
# batch06 (79문항: esc_sonnet_h3-2_3of4 45, esc_sonnet_h3-2_4of4 34) — v1.5 문법 재작업
# 핵심 교체: f′(a)→app(prime(f), a), f″(x)→app(prime(f, 2), x), (g∘f)(x)→app(comp(g, f), x), fⁿ(x)→iter(f, n, x)
#            조각적 정의→cases(식, 조건, …)('x≤0, x≥2'는 같은 식 두 쌍) / 줄임표→cdots 연산자 연결 / 빈칸 □→box(n)
#            고정 첨자 점 라벨: 선분 윗줄→seg(OC1), ∠→angle(OP1A2), △→tri(OA0A1), 점 이름은 [[sub(A,1)]] 텍스트 혼합, 좌표 붙은 점은 app(sub(A,1), x, y)
#            가변 첨자 라벨(Pₙ, AₖBₖ …)은 sub 텍스트 혼합(선분 윗줄 생략) → 통과
# 도형(그래프·원·삼각형 등)은 unsupported(raw) 유지 — 도형만 남은 항목은 통과
# 여전히 보류: 한 이미지에 별개 문항 2개(id 1개) 1건(c438667b), 일반항 순환소수 0.4̇00⋯00̇ 표기 문법 밖 1건(bbbb37e5)
ITEMS = []
def add(**kw): ITEMS.append(kw)

# ================= esc_sonnet_h3-2_3of4 =================
# 0. 8dcc42af — 등비수열의 극한 p71: fⁿ(x)→iter, f¹=f·f^{n+1}=f∘fⁿ 은 x를 붙여 iter로
add(id="8dcc42af", qtype="choice",
    question="그림은 함수 [[f(x) = 1 - abs(2x - 1)]] ([[0 <= x <= 1]])의 그래프이다.\n자연수 [[n]]에 대하여 집합 [[sub(A,n)]]을\n[[sub(A,n)]] = { [[x]] | [[iter(f, n, x) = 0]], [[0 <= x <= 1]] }이라 할 때, 집합 [[sub(A,n)]]의 원소의 개수를 [[sub(a,n)]]이라 하자.\n예를 들어 [[sub(A,1) = set(0, 1)]], [[sub(A,2) = set(0, frac(1,2), 1)]]이므로 [[sub(a,1) = 2]], [[sub(a,2) = 3]]이다. 이때 [[lim(n, inf, frac(sub(a,n) sub(a,n+1), pow(4,n)))]]의 값은?\n(단, [[iter(f, 1, x) = f(x)]], [[iter(f, n + 1, x) = f(iter(f, n, x))]] ([[n]] = 1, 2, 3, ⋯)이다.)",
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 꺾은선 그래프, (0,0)-(1/2,1)-(1,0), 점선으로 x=1/2, y=1, x=1 표시"}}],
    confidence=0.85,
    note="fⁿ(x)=0을 iter(f, n, x)로; 원문 'f¹=f, f^{n+1}=f∘fⁿ'(인자 없음)은 x를 붙여 iter(f,1,x)=f(x), iter(f,n+1,x)=f(iter(f,n,x))로 표기. 집합 조건 2개라 중괄호·세로줄은 텍스트. 답 ② 유지")

# 1. 163e7d8c — 등비수열의 극한 p72: 선분 윗줄 OC₁→seg(OC1), 첨자 점 이름→sub 텍스트 혼합
add(id="163e7d8c", qtype="choice",
    question="그림과 같이 크기가 [[deg(60)]]인 [[angle(AOB)]]의 이등분선 위에 [[seg(OC1) = 4]]인 점 [[sub(C,1)]]을 잡아 점 [[sub(C,1)]]을 중심으로 하고 반직선 OA와 OB에 접하는 원 [[sub(C,1)]]을 그릴 때, 원 [[sub(C,1)]]과 반직선 OA, OB와의 접점을 각각 [[sub(P,1)]], [[sub(Q,1)]]이라 하자.\n점 [[sub(C,1)]]을 지나고 반직선 OA와 OB에 접하는 두 원 중에서 큰 원의 중심을 [[sub(C,2)]], 원 [[sub(C,2)]]와 반직선 OA, OB와의 접점을 각각 [[sub(P,2)]], [[sub(Q,2)]]라 하고, 원 [[sub(C,1)]]과 원 [[sub(C,2)]]가 만나는 점을 각각 [[sub(A,1)]], [[sub(B,1)]]이라 할 때, 사각형 [[sub(A,1)]][[sub(C,1)]][[sub(B,1)]][[sub(C,2)]]의 넓이를 [[sub(S,1)]]이라 하자.\n점 [[sub(C,2)]]를 지나고 반직선 OA와 OB에 접하는 두 원 중에서 큰 원의 중심을 [[sub(C,3)]], 원 [[sub(C,3)]]과 반직선 OA, OB와의 접점을 각각 [[sub(P,3)]], [[sub(Q,3)]]이라 하고, 원 [[sub(C,2)]]와 원 [[sub(C,3)]]이 만나는 점을 각각 [[sub(A,2)]], [[sub(B,2)]]라 할 때, 사각형 [[sub(A,2)]][[sub(C,2)]][[sub(B,2)]][[sub(C,3)]]의 넓이를 [[sub(S,2)]]라 하자.\n이와 같은 과정을 계속하여 [[n]]번째 얻은 도형의 넓이를 [[sub(S,n)]]이라 할 때, [[lim(n, inf, frac(sub(S,n), pow(4,n) + pow(2,n)))]]의 값은?",
    choices=["[[frac(sqrt(5),8)]]", "[[frac(sqrt(5),4)]]", "[[frac(sqrt(15),8)]]", "[[frac(sqrt(15),4)]]", "[[frac(sqrt(15),2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "각 AOB(60°)의 이등분선 위 중심 C₁,C₂,C₃의 세 원(반직선 OA·OB에 접함), 접점 P₁~P₃·Q₁~Q₃, 교점 A₁,B₁,A₂,B₂, 사각형 A₁C₁B₁C₂·A₂C₂B₂C₃ 음영"}}],
    confidence=0.85,
    note="선분 윗줄 OC₁=4를 seg(OC1)로, 첨자 점·원 이름은 sub 텍스트 혼합. 답 ⑤ 유지")

# 2. 28f215d6 — 등비수열의 극한 p74: 가변 첨자 라벨(Oₙ, Pₙ, Qₙ)→sub 텍스트 혼합(윗줄 없음)
add(id="28f215d6", qtype="short",
    question="다음 그림과 같이 한 변의 길이가 8인 정삼각형 ABC와 점 A를 지나고 직선 BC와 평행한 직선 [[l]]이 있다. 자연수 [[n]]에 대하여 중심 [[sub(O,n)]]이 변 AC 위에 있고 반지름의 길이가 [[2 sqrt(3) × pow(frac(1,5), n - 1)]]인 원이 직선 AB와 직선 [[l]]에 모두 접한다. 이 원과 직선 AB가 접하는 점을 [[sub(P,n)]], 직선 [[sub(O,n) sub(P,n)]]과 직선 [[l]]이 만나는 점을 [[sub(Q,n)]]이라 하자.\n삼각형 B[[sub(O,n)]][[sub(Q,n)]]의 넓이를 [[sub(S,n)]]이라 하면, [[lim(n, inf, pow(5, n - 1) sub(S,n)) = k]]이다. 이때 [[pow(k,2)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 ABC, A를 지나는 수평선 l, 변 AC 위 중심 Oₙ의 원(AB·l에 접함), 접점 Pₙ, l 위의 점 Qₙ, 선분 BOₙ·BQₙ"}}],
    confidence=0.85,
    note="가변 첨자 점 라벨(Oₙ, Pₙ, Qₙ)을 sub 텍스트 혼합으로(원문에 윗줄 없음). 답 768 유지(빠른정답 2와 불일치는 1차와 동일)")

# 3. 83fc8116 — 등비수열의 극한 p83: 가변 첨자 선분 ABₙ, ACₙ → 곱 표기(윗줄 생략)
add(id="83fc8116", qtype="short",
    question="자연수 [[n]]에 대하여 [[angle(A) = deg(45)]], [[A sub(B,n) = pow(2,n)]], [[A sub(C,n) = pow(2, n + 1)]]인 삼각형 A[[sub(B,n)]][[sub(C,n)]]의 넓이를 [[sub(S,n)]], 변 [[sub(B,n)]][[sub(C,n)]]의 길이를 [[sub(a,n)]]이라 할 때,\n[[lim(n, inf, pow(frac(sub(a,n) + sub(S,n), sub(a,2n)), 2)) = p + q sqrt(2)]]이다. 두 유리수 [[p]], [[q]]에 대하여 [[34(p + q)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABₙCₙ: ∠A=45°, ABₙ=2ⁿ, ACₙ=2^(n+1), BₙCₙ=aₙ 표시"}}],
    confidence=0.85,
    note="가변 첨자 선분 ABₙ·ACₙ(윗줄)은 A sub(B,n) 곱 표기(윗줄 생략). 답 7 유지")

# 4. d409a1d5 — 몫의 미분법 p13: f′(2)→app(prime(f), 2)
add(id="d409a1d5", qtype="choice",
    question="1보다 큰 실수 [[t]]에 대하여 다음 그림과 같이 점 [[P(2t + frac(1,2t), 0)]]에서 원 [[pow(x,2) + pow(y,2) = frac(1, 4 pow(t,2))]]에 접선을 그었을 때, 원과 접선이 제1사분면에서 만나는 점을 Q, 원 위의 점 [[point(0, -frac(1,2t))]]을 R라 하자.\n[[seg(OP) × seg(OQ)]]를 [[f(t)]]라 할 때, [[app(prime(f), 2)]]의 값은?",
    choices=["[[-1]]", "[[-frac(1,2)]]", "[[-frac(1,4)]]", "[[-frac(1,8)]]", "[[-frac(1,16)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 중심 원, x축 위 점 P에서 원에 그은 접선, 접점 Q(제1사분면), 원 위 점 R(y축 아래), 선분 QR"}}],
    confidence=0.85,
    note="[2015년 4월 고3 이과 13번 변형]. f′(2)를 app(prime(f), 2)로. 답 ⑤ 유지")

# 5. 26fab94c — 몫의 미분법 p40: 줄임표→cdots, f′(1)→app
add(id="26fab94c", qtype="short",
    question="함수 [[f(x) = frac(1,x) + frac(2,pow(x,2)) + frac(3,pow(x,3)) + cdots + frac(7,pow(x,7))]]에 대하여\n[[app(prime(f), 1)]]의 값을 구하시오.",
    figure=None, confidence=0.85,
    note="줄임표를 cdots로 한 식에 연결, f′(1)을 app(prime(f), 1)로. 답 -140 유지(빠른정답 -550과 불일치는 1차와 동일)")

# 6. d4af49cf — 몫의 미분법 p41
add(id="d4af49cf", qtype="short",
    question="함수 [[f(x) = frac(10,x) + frac(9,pow(x,2)) + frac(8,pow(x,3)) + cdots + frac(1,pow(x,10))]]에 대하여\n[[app(prime(f), 1)]]의 값을 구하시오.",
    figure=None, confidence=0.85,
    note="줄임표를 cdots로, f′(1)을 app(prime(f), 1)로. 답 -220 유지")

# 7. 84863d5c — 몫의 미분법 p43
add(id="84863d5c", qtype="choice",
    question="함수 [[f(x) = frac(1,x) + frac(1,pow(x,2)) + frac(1,pow(x,3)) + cdots + frac(1,pow(x,10))]]에 대하여\n[[app(prime(f), 1)]]의 값은?",
    choices=["[[-55]]", "[[-50]]", "[[-40]]", "[[55]]", "[[65]]"],
    figure=None, confidence=0.85,
    note="줄임표를 cdots로, f′(1)을 app(prime(f), 1)로. 답 ① 유지(빠른정답 -140과 불일치는 1차와 동일)")

# 8. 0a0e003a — 몫의 미분법 p59: 무한급수 꼴 함수 → cdots 연결, -9f′(2)
add(id="0a0e003a", qtype="short",
    question="함수\n[[f(x) = 1 + pow(2, -2 log(2,x)) + pow(2, -4 log(2,x)) + cdots + pow(2, -2n log(2,x)) + cdots]]\n에 대하여 [[-9 app(prime(f), 2)]]의 값을 구하시오. (단, [[x > 1]])",
    figure=None, confidence=0.85,
    note="줄임표(중간·끝)를 cdots로 한 식에 연결, f′(2)를 app(prime(f), 2)로. 답 4 유지")

# 9. dd37d5d6 — 몫의 미분법 p60: 첫 줄이 f(x)=로 시작(머리말 '함수' 없음)하나 문항 내용은 완전
add(id="dd37d5d6", qtype="short",
    question="[[f(x) = 1 + pow(3, -log(3,x)) + pow(3, -2 log(3,x)) + cdots + pow(3, -n log(3,x)) + cdots]]\n에 대하여 [[abs(frac(1, app(prime(f), 3)))]]의 값을 구하시오. (단, [[x > 1]])",
    figure=None, confidence=0.8,
    note="줄임표를 cdots로, f′(3)을 app(prime(f), 3)으로. 이미지가 f(x)=로 바로 시작(머리말 '함수' 없음)하나 식·물음·조건이 모두 보여 내용 완전. 답 4 유지")

# 10. 281d906d — 몫의 미분법 p67: h′(π/6)
add(id="281d906d", qtype="choice",
    question="다음 그림과 같이 [[seg(BC) = 2]], [[angle(ABC) = frac(pi,2)]], [[angle(ACB) = 2 theta]]인 삼각형 ABC에 내접하는 원의 반지름의 길이를 [[r(theta)]]라 하자. [[h(theta) = frac(r(theta), tan(theta))]]일 때, [[app(prime(h), frac(pi,6))]]의 값은? (단, [[0 < theta < frac(pi,4)]])",
    choices=["[[2 sqrt(3) - 8]]", "[[2 sqrt(3) - 4]]", "[[4 sqrt(3) - 8]]", "[[4 sqrt(3) - 4]]", "[[4 sqrt(3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(∠B 직각, BC=2, ∠C=2θ)와 내접원(중심 O, 반지름 r(θ))"}}],
    confidence=0.85,
    note="[2017년 10월 고3 이과 12번 변형]. h′(π/6)을 app(prime(h), frac(pi,6))으로. 답 ③ 유지")

# 11. 3ee5423d — 몫의 미분법 p68: f′(π/3)
add(id="3ee5423d", qtype="short",
    question="다음 그림과 같이 [[seg(BC) = 2]], [[angle(ABC) = theta]], [[angle(ACB) = frac(pi,3)]]인 삼각형의 한 꼭짓점 A에서 선분 [[seg(BC)]]에 내린 수선의 길이를 [[f(theta)]]라 할 때, [[app(prime(f), frac(pi,3))]]의 값을 구하시오.\n(단, [[0 < theta < frac(pi,2)]])",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(BC=2, ∠B=θ, ∠C=π/3), A에서 BC에 내린 수선 AH=f(θ)"}}],
    confidence=0.85,
    note="f′(π/3)을 app(prime(f), frac(pi,3))으로. 답 2 유지")

# 12. 63202c07 — 몫의 미분법 p72: h′(π/6)
add(id="63202c07", qtype="choice",
    question="그림과 같이 [[seg(BC) = 1]], [[angle(ABC) = frac(pi,3)]], [[angle(ACB) = 2 theta]]인 삼각형 ABC에 내접하는 원의 반지름의 길이를 [[r(theta)]]라 하자. [[h(theta) = frac(r(theta), tan(theta))]]일 때, [[app(prime(h), frac(pi,6))]]의 값은?\n(단, [[0 < theta < frac(pi,3)]])",
    choices=["[[-sqrt(3)]]", "[[-frac(sqrt(3),3)]]", "[[frac(sqrt(3),6)]]", "[[frac(sqrt(3),3)]]", "[[sqrt(3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(BC=1, ∠B=π/3, ∠C=2θ)와 내접원(반지름 r(θ))"}}],
    confidence=0.85,
    note="[2017년 10월 고3 이과 12번/3점]. h′(π/6)을 app(prime(h), frac(pi,6))으로. 답 ② 유지")

# 13. 55e9bba0 — 몫의 미분법 p85: h′(π/4)
add(id="55e9bba0", qtype="choice",
    question="다음 그림과 같이 [[seg(BC) = 3]], [[angle(ABC) = frac(pi,6)]], [[angle(ACB) = 2 theta]]인 삼각형 ABC에 내접하는 원의 반지름의 길이를 [[r(theta)]]라 하자.\n[[h(theta) = frac(r(theta), tan(theta))]]일 때, [[app(prime(h), frac(pi,4))]]의 값은?\n(단, [[0 < theta < frac(pi,2)]]이고, [[tan(frac(pi,12)) = 0.25]]로 계산한다.)",
    choices=["[[-frac(24,25)]]", "[[-frac(12,25)]]", "[[0]]", "[[frac(12,25)]]", "[[frac(24,25)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(BC=3, ∠B=π/6, ∠C=2θ)와 내접원(반지름 r(θ))"}}],
    confidence=0.85,
    note="h′(π/4)를 app(prime(h), frac(pi,4))로. 답 ① 유지")

# 14. ca9b028e — 몫의 미분법 p91: 조각 정의 → cases
add(id="ca9b028e", qtype="short",
    question="함수 [[f(x) = cases(4 pow(e,x) + a x + b, x >= 0, 2 tan(x), x < 0)]]가 [[x = 0]]에서 미분가능할 때, 상수 [[a]], [[b]]에 대하여 [[a b]]의 값을 구하시오.",
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 8 유지(b=-4, a=-2)")

# 15. 0ad0e62a — 몫의 미분법 p94: 1/f′(π/3)
add(id="0ad0e62a", qtype="choice",
    question="다음 그림과 같이 점 O를 중심으로 하고 반지름의 길이가 4, [[angle(AOB) = frac(pi,2)]]인 부채꼴 OAB의 호 AB 위에 [[angle(POA) = x]] ([[0 < x < frac(pi,2)]])인 점 P를 잡는다. 중심이 선분 OB 위에 있고 점 B를 지나며 선분 OP에 접하는 원의 반지름의 길이를 [[f(x)]]라 할 때, [[frac(1, app(prime(f), frac(pi,3)))]]의 값은?",
    choices=["[[-frac(sqrt(3),4)]]", "[[-frac(3 sqrt(3),8)]]", "[[-frac(sqrt(3),2)]]", "[[-frac(5 sqrt(3),8)]]", "[[-frac(3 sqrt(3),4)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "사분원 OAB(반지름 4), 호 위 점 P(∠POA=x), OB 위 중심으로 B를 지나고 OP에 접하는 원"}}],
    confidence=0.85,
    note="f′(π/3)을 app(prime(f), frac(pi,3))으로. 답 ② 유지(빠른정답 4와 불일치는 1차와 동일)")

# 16. c438667b — 몫의 미분법 p99: 한 이미지에 별개 문항 2개(id 1개) → 보류 유지(하단 문항 전사, 표기는 v1.5로 정리)
add(id="c438667b", qtype="choice",
    question="실수 전체의 집합에서 미분가능한 함수 [[f(x)]]에 대하여 함수 [[g(x)]]를 [[g(x) = frac(f(x) cos(2x), pow(e,x))]]라 하자.\n[[app(prime(g), pi) = pow(e,pi) g(pi)]]일 때, [[frac(app(prime(f), pi), f(pi))]]의 값은? (단, [[f(pi) != 0]])",
    choices=["[[pow(e, -2 pi)]]", "[[1]]", "[[pow(e, -pi) + 1]]", "[[pow(e,pi) + 1]]", "[[pow(e, 2 pi)]]"],
    figure=None, confidence=0.75,
    needs_review="같은 이미지에 별개 문항 2개(id 1개): 상단 — BC=2, ∠ABC=π/3, ∠ACB=2θ(0<θ<π/3)인 삼각형의 내접원 반지름 r(θ), h(θ)=r(θ)/tanθ일 때 h′(π/6)의 값(선지 ①−1/2 ②−√3/3 ③−√3/2 ④−(2/3)√3 ⑤−√3, 그림 있음) / 하단 g(x) 문항을 전사함",
    note="g′(π)·f′(π)를 app(prime(·), pi)로 정리. 답 ④ 유지(빠른정답 240은 두 문항 어느 쪽에도 해당 없음)")

# 17. 3313274c — 접선의 방정식 p40: cases + h′(1/2e)·h′(a) → app; 조건 상자는 줄바꿈 텍스트
add(id="3313274c", qtype="choice",
    question="양수 [[t]]에 대하여 구간 [[itv(1, inf, co)]]에서 정의된 함수 [[f(x)]]가\n[[f(x) = cases(ln(x), 1 <= x < e, -t + ln(x), x >= e)]]\n일 때, 다음 조건을 만족시키는 일차함수 [[g(x)]] 중에서 직선 [[y = g(x)]]의 기울기의 최솟값을 [[h(t)]]라 하자.\n1 이상의 모든 실수 [[x]]에 대하여 [[(x - e)(g(x) - f(x)) >= 0]]이다.\n미분가능한 함수 [[h(t)]]에 대하여 양수 [[a]]가 [[h(a) = frac(1, e + 2)]]을 만족한다. [[app(prime(h), frac(1, 2e)) × app(prime(h), a)]]의 값은?",
    choices=["[[frac(1, pow(e + 1, 2))]]", "[[frac(1, e(e + 1))]]", "[[frac(1, pow(e,2))]]", "[[frac(1, (e - 1)(e + 1))]]", "[[frac(1, e(e - 1))]]"],
    derived_answer="④",
    figure=None, confidence=0.8,
    note="[2017년 11월 고3 이과 21번/4점]. 경우 나눔을 cases로, h′(1/2e)·h′(a)를 app(prime(h), ·)로(원문 '·'는 ×). 답 새로 도출: t≤1/e에서 h(t)=(1−t)/(e−1), t>1/e에서 h−ln h=1+t → h′(1/2e)=−1/(e−1), h(a)=1/(e+2)이면 h′(a)=−1/(e+1) → 곱 1/((e−1)(e+1)) → ④")

# 18. 540eb24f — 접선의 방정식 p62: cases
add(id="540eb24f", qtype="choice",
    question="실수 [[k]]에 대하여 함수 [[f(x)]]는\n[[f(x) = cases(frac(2, 1 - x), x < 1, -pow(x - 2, 2) + k, x >= 1)]]이다. 실수 [[t]]에 대하여 직선 [[y = x + t]]와 함수 [[y = f(x)]]의 그래프가 만나는 점의 개수를 [[g(t)]]라 하자. 함수 [[g(t)]]가 [[t = a]]에서 불연속인 [[a]]의 값이 한 개일 때, [[k]]의 값은?",
    choices=["[[sqrt(2) - frac(3,4)]]", "[[2 sqrt(2) - frac(3,4)]]", "[[sqrt(2) + frac(3,4)]]", "[[2 sqrt(2) + frac(3,4)]]", "[[3 sqrt(2) + frac(3,4)]]"],
    figure=None, confidence=0.8,
    note="경우 나눔을 cases로. 답 ④ 유지(빠른정답 49와 불일치는 1차와 동일)")

# 19. 2ba8a0a3 — 지수·로그함수의 극한과 미분 p19: cases('x≤0, x≥2'는 같은 식 두 쌍)
add(id="2ba8a0a3", qtype="short",
    question="함수 [[f(x)]]가\n[[f(x) = cases(pow(e,x), x <= 0, pow(e,x), x >= 2, ln(x + 1), 0 < x < 2)]]\n이고, 함수 [[y = g(x)]]의 그래프가 다음 그림과 같다.\n[[lim(x, 2, f(g(x)), -) + lim(x, 0, g(f(x)), -)]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "y=g(x) 그래프: x<0에서 원점(채운 점)으로 올라가는 곡선, 0<x<2에서 (0,2)(열린 점)~(2,0)(열린 점) 선분, x≥2에서 (2,2)(채운 점)부터 증가하는 곡선"}}],
    confidence=0.8,
    note="경우 나눔을 cases로(원문 조건 'x≤0, x≥2'는 eˣ를 두 쌍으로 나눔). 답 1 유지(빠른정답 3과 불일치는 1차와 동일)")

# 20. 62aee887 — 지수·로그함수의 극한과 미분 p20: cases(같은 식 두 쌍)
add(id="62aee887", qtype="choice",
    question="함수 [[f(x)]]가\n[[f(x) = cases(pow(e,x), x <= 0, pow(e,x), x >= 2, ln(x + 1), 0 < x < 2)]]\n이고, 함수 [[y = g(x)]]의 그래프가 그림과 같다.\n[[lim(x, 2, f(g(x)), +) + lim(x, 0, g(f(x)), +)]]의 값은?",
    choices=["[[e]]", "[[e + 1]]", "[[e + 2]]", "[[pow(e,2) + 1]]", "[[pow(e,2) + 2]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "y=g(x) 그래프: x<0에서 원점(채운 점)으로 올라가는 곡선, 0<x<2에서 (0,2)(열린 점)~(2,0)(열린 점) 선분, x≥2에서 (2,2)(채운 점)부터 증가하는 곡선"}}],
    confidence=0.8,
    note="[2016년 3월 고3 이과 12번/3점]. 경우 나눔을 cases로(조건 'x≤0, x≥2'는 eˣ를 두 쌍으로). 답 ⑤ 유지(빠른정답 4와 불일치는 1차와 동일)")

# 21. 986b7a50 — p63: cases
add(id="986b7a50", qtype="choice",
    question="함수 [[f(x) = cases(frac(pow(e, a x) - 1, 3x), x < 0, pow(x,2) + 3x + 2, x >= 0)]]이 실수 전체의 집합에서 연속일 때, 상수 [[a]]의 값은? (단, [[a != 0]])",
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    figure=None, confidence=0.85,
    note="[2017년 7월 고3 이과 6번/3점]. 경우 나눔을 cases로. 답 ① 유지(빠른정답 3과 불일치는 1차와 동일)")

# 22. a98e4dec — p64: cases + (g∘f)(x)→app(comp(g, f), x)
add(id="a98e4dec", qtype="choice",
    question="두 함수\n[[f(x) = cases(a x, x < 2, -4x + 10, x >= 2)]], [[g(x) = pow(3,x) + pow(3,-x)]]\n에 대하여 합성함수 [[app(comp(g, f), x)]]가 실수 전체의 집합에서 연속이 되도록 하는 모든 실수 [[a]]의 값의 합은?",
    choices=["[[-1]]", "[[0]]", "[[1]]", "[[2]]", "[[3]]"],
    figure=None, confidence=0.85,
    note="[2015년 6월 고3 이과 16번 변형]. 경우 나눔을 cases로, (g∘f)(x)를 app(comp(g, f), x)로. 답 ② 유지(빠른정답 1과 불일치는 1차와 동일)")

# 23. eca349ce — p66
add(id="eca349ce", qtype="short",
    question="두 함수\n[[f(x) = cases(a x, x < 1, 4x - 3, x >= 1)]], [[g(x) = pow(2,x) - pow(2,-x)]]\n에 대하여 합성함수 [[app(comp(g, f), x)]]가 실수 전체의 집합에서 연속이 되도록 하는 실수 [[a]]의 값을 구하시오.",
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로, (g∘f)(x)를 app(comp(g, f), x)로. 답 1 유지")

# 24. 93fc789e — p67
add(id="93fc789e", qtype="choice",
    question="두 함수\n[[f(x) = cases(a x, x < 1, -3x + 4, x >= 1)]], [[g(x) = pow(2,x) + pow(2,-x)]]\n에 대하여 합성함수 [[app(comp(g, f), x)]]가 실수 전체의 집합에서 연속이 되도록 하는 모든 실수 [[a]]의 값의 곱은?",
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    figure=None, confidence=0.85,
    note="[2015년 6월 고3 이과 16번/4점]. 경우 나눔을 cases로, (g∘f)(x)를 app(comp(g, f), x)로. 답 ⑤ 유지")

# 25. a9d37043 — p68
add(id="a9d37043", qtype="choice",
    question="함수 [[f(x) = cases(frac(pow(e, a x) - 1, 4x), x < 0, pow(x,2) + 2x - 1, x >= 0)]]이 실수 전체의 집합에서 연속일 때, 상수 [[a]]의 값은? (단, [[a != 0]])",
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    figure=None, confidence=0.85,
    note="[2017년 7월 고3 이과 6번 변형]. 경우 나눔을 cases로. 답 ② 유지(빠른정답 1과 불일치는 1차와 동일)")

# 26. bae28594 — p92: 줄임표 든 극한식을 lim + cdots 한 식으로
add(id="bae28594", qtype="choice",
    question="자연수 [[n]]에 대하여\n[[f(n) = lim(x, 0, frac(pow(e, 4x) + pow(e, 8x) + pow(e, 12x) + cdots + pow(e, 4 n x) - n, x))]]\n일 때, [[sum(n, 1, inf, frac(1, f(n)))]]의 합은?",
    choices=["[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]", "[[1]]", "[[2]]"],
    figure=None, confidence=0.85,
    note="텍스트로 쓰였던 lim·분수·줄임표를 lim(x, 0, frac(… + cdots + …, x)) 한 식으로(원문 중괄호는 분자로). 답 ③ 유지(빠른정답 4와 불일치는 1차와 동일)")

# 27. 33f31f31 — p98: g(x) 조각 정의 → cases
add(id="33f31f31", qtype="choice",
    question="함수 [[f(x) = pow(e, 4x) - 2 a x]] ([[a]]는 상수)와 상수 [[k]]에 대하여\n함수 [[g(x) = cases(f(x), x >= k, -f(x), x < k)]]가 실수 전체의 집합에서 연속이고 역함수를 가질 때, [[a k]]의 값은?",
    choices=["[[frac(e,4)]]", "[[frac(e,2)]]", "[[pow(e, frac(1,2))]]", "[[e]]", "[[pow(e,2)]]"],
    figure=None, confidence=0.8,
    note="[2024년 10월 고3 미적분 27번 변형]. 경우 나눔을 cases로. 답 ② 유지(빠른정답 5와 불일치는 1차와 동일)")

# 28. 25d7c435 — p99: cases
add(id="25d7c435", qtype="choice",
    question="함수 [[f(x) = cases((3x + 1) pow(e,x), x <= 0, a x + 1, x > 0)]]이\n[[x = 0]]에서 미분가능할 때, 상수 [[a]]의 값은?",
    choices=["[[1]]", "[[4]]", "[[7]]", "[[10]]", "[[13]]"],
    figure=None, confidence=0.85,
    note="[2016년 11월 고2 이과 8번/3점]. 경우 나눔을 cases로. 답 ② 유지(빠른정답 3과 불일치는 1차와 동일)")

# 29. bbbb37e5 — 등비급수 p52: 일반항 순환소수 0.4̇00⋯00̇(0이 n−1개) 표기 문법 밖 → 보류 유지
add(id="bbbb37e5", qtype="choice",
    question="순환소수로 이루어진 수열 [[set(sub(a,n))]]의 각 항이\n[[sub(a,1) = recdec(0,4)]], [[sub(a,2) = recdec(0,40)]], [[sub(a,3) = recdec(0,400)]], ⋯,\n[[sub(a,n)]] = 0.4̇00⋯00̇ (0이 [[n - 1]]개), ⋯일 때, [[sum(n, 1, inf, (frac(1, sub(a, n+1)) - frac(1, sub(a,n))))]]의 값은?",
    choices=["[[0]]", "[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]"],
    figure=None, confidence=0.75,
    needs_review="일반항 순환소수 0.4̇00⋯00̇(밑줄 '(n−1)개', 순환마디 안에 줄임표) 표기가 recdec 문법 밖 — 텍스트 유지",
    note="이미지 재확인: aₙ=0.4̇00⋯00̇ 밑에 '(n−1)개' 밑줄. 답 ② 유지")

# 30. 59122624 — 등비급수 p63: 선분 윗줄→seg(OA0)·seg(A0A1)·seg(A1B1)·seg(A1A2), △→tri(OA0A1), 점 A₀(10,0)→app(sub(A,0),10,0)
add(id="59122624", qtype="short",
    question="다음 그림과 같이 원점 O와 점 [[app(sub(A,0), 10, 0)]]에 대하여 제1사분면 위에 [[seg(OA0)]]를 한 변으로 하는 정삼각형 O[[sub(A,0)]][[sub(A,1)]]을 만들고 [[seg(A0A1)]]을 [[ratio(1,2)]]로 내분하는 점을 [[sub(B,1)]]이라 한다. 또 [[tri(OA0A1)]] 밖에 [[seg(A1B1)]]을 한 변으로 하는 정삼각형 [[sub(A,1)]][[sub(B,1)]][[sub(A,2)]]를 만들고 [[seg(A1A2)]]를 [[ratio(1,2)]]로 내분하는 점을 [[sub(B,2)]]라 한다. 이와 같은 과정을 한없이 반복하면 점 [[sub(A,n)]]은 점 [[point(a, b)]]에 한없이 가까워진다. 이때 [[a]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: O, A₀(10,0), 정삼각형 OA₀A₁, 내분점 B₁, 정삼각형 A₁B₁A₂, B₂, A₃, B₃, A₄ … 나선형으로 이어지는 정삼각형들"}}],
    confidence=0.85,
    note="[2004년 3월 고3 이과 27번]. 선분 윗줄을 seg(OA0)·seg(A0A1)·seg(A1B1)·seg(A1A2)로, △OA₀A₁을 tri(OA0A1)로, 점 A₀(10, 0)을 app(sub(A,0), 10, 0)으로. 답 13 유지")

# 31. 8e4185e4 — 등비급수 p64
add(id="8e4185e4", qtype="short",
    question="다음 그림과 같이 원점 O와 점 [[app(sub(A,0), 14, 0)]]에 대하여 제1사분면 위에 [[seg(OA0)]]을 한 변으로 하는 정삼각형 O[[sub(A,0)]][[sub(A,1)]]을 만들고 [[seg(A0A1)]]을 [[ratio(1,3)]]으로 내분하는 점을 [[sub(B,1)]]이라 한다. 또, [[tri(OA0A1)]] 밖에 [[seg(A1B1)]]을 한 변으로 하는 정삼각형 [[sub(A,1)]][[sub(B,1)]][[sub(A,2)]]를 만들고 [[seg(A1A2)]]를 [[ratio(1,3)]]으로 내분하는 점을 [[sub(B,2)]]라 한다. 이와 같은 과정을 한없이 반복하면 점 [[sub(A,n)]]은 점 [[point(a, b)]]에 한없이 가까워진다. [[a]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: O, A₀(14,0), 정삼각형 OA₀A₁, 내분점 B₁, 정삼각형 A₁B₁A₂, B₂, A₃, B₃, A₄ … 나선형으로 이어지는 정삼각형들"}}],
    confidence=0.85,
    note="선분 윗줄을 seg(…)로, △OA₀A₁을 tri(OA0A1)로, 점 A₀(14, 0)을 app(sub(A,0), 14, 0)으로. 답 22 유지(빠른정답 1과 불일치는 1차와 동일)")

# 32. d34a83ad — 등비급수 p68: 첨자 점·원 이름→sub 텍스트 혼합('호 OA₁'은 원문에 호 기호 없음)
add(id="d34a83ad", qtype="choice",
    question="그림과 같이 중심이 [[point(1, 0)]]이고 반지름의 길이가 1인 원 [[sub(O,1)]]이 있다. 원 [[sub(O,1)]]이 직선 [[y = frac(1, sqrt(3)) x]]와 만나는 점 중에서 원점이 아닌 점을 [[sub(A,1)]]이라 하고 직선 [[y = frac(1, sqrt(3)) x]]의 위 쪽에 있는 호 O[[sub(A,1)]]의 길이를 [[sub(l,1)]]이라 하자.\n중심이 [[point(sub(l,1), 0)]]이고 반지름의 길이가 [[sub(l,1)]]인 원 [[sub(O,2)]]를 그린다. 원 [[sub(O,2)]]가 직선 [[y = frac(1, sqrt(3)) x]]와 만나는 점 중에서 원점이 아닌 점을 [[sub(A,2)]]라 하고 직선 [[y = frac(1, sqrt(3)) x]]의 위 쪽에 있는 호 O[[sub(A,2)]]의 길이를 [[sub(l,2)]]라 하자.\n이와 같은 과정을 계속하여 [[n]]번째 얻은 호의 길이를 [[sub(l,n)]]이라 할 때, [[sum(n, 1, inf, frac(1, sub(l,n)))]]의 값은?",
    choices=["[[frac(1, pi - 3)]]", "[[frac(2, pi - 3)]]", "[[frac(1, 2 pi - 3)]]", "[[frac(2, 2 pi - 3)]]", "[[frac(3, 2 pi - 3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점을 지나는 원 O₁, O₂, O₃(중심 x축 위), 직선 y=x/√3, 교점 A₁, A₂, A₃, 직선 위쪽 호 OA₁·OA₂·OA₃ 굵게"}}],
    confidence=0.85,
    note="[2012년 10월 고3 문과 21번/4점]. 첨자 점·원 이름을 sub 텍스트 혼합으로(원문 '호 OA₁'은 기호 없이 낱말). 답 ⑤ 유지(빠른정답 1과 불일치는 1차와 동일)")

# 33. 0b421061 — 등비급수 p69: 선분·호 기호→seg(OA1)·arc(OA2), Σ⌒OAₙ→sum(n,1,inf, arc(OAn))(n은 라벨 문자)
add(id="0b421061", qtype="choice",
    question="그림과 같이 [[x]]축 위의 점 [[app(sub(A,1), 6 pi - 12, 0)]]에 대하여 [[seg(OA1)]]을 지름으로 하는 반원을 제1사분면에 그리고, [[seg(OA1) = arc(OA2)]]인 점 [[sub(A,2)]]를 [[y]]축 위에 잡아 [[seg(OA2)]]를 지름으로 하는 반원을 제2사분면에 그린다.\n또, [[seg(OA2) = arc(OA3)]]인 점 [[sub(A,3)]]를 [[x]]축 위에 잡아 [[seg(OA3)]]를 지름으로 하는 반원을 제3사분면에 그리고, [[seg(OA3) = arc(OA4)]]인 점 [[sub(A,4)]]를 [[y]]축 위에 잡아 [[seg(OA4)]]를 지름으로 하는 반원을 제4사분면에 그린다. 같은 방법으로 제1사분면, 제2사분면, ⋯에 반원을 계속하여 그려나갈 때, 반원들의 호의 길이의 합 [[sum(n, 1, inf, arc(OAn))]]의 값은?\n(단, [[seg(OAn)]]은 [[arc(OAn)]]을 지름으로 하는 반원의 호이고 [[n]] = 1, 2, 3, ⋯이다.)",
    choices=["[[9 pi]]", "[[8 pi + 1]]", "[[pow(pi,2) + 10]]", "[[2 pow(pi,2) + 3]]", "[[3 pow(pi,2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O에서 시작해 A₁(x축 양), A₂(y축 양), A₃(x축 음), A₄(y축 음), A₅, A₆ … 를 지름 끝으로 하는 반원들이 각 사분면에 나선형으로 작아짐"}}],
    confidence=0.8,
    note="[2006년 3월 고3 이과 29번]. 윗줄 선분→seg(OA1)…, 호 기호→arc(OA2)…; 가변 첨자 ⌒OAₙ은 arc(OAn)(n을 라벨 문자로, 첨자 표시 불가)로 써서 Σ를 sum 식으로. 원문 단서 '(단, ‾OAₙ은 ⌒OAₙ을 지름으로 하는 반원의 호이고'는 확대 확인 결과 기호가 그대로(원문 그대로 전사). 답 ⑤ 유지(빠른정답 27과 불일치는 1차와 동일)")

# 34. 70ba5f0e — 등비급수 p70: seg(A1B1)·perp(seg(AC), seg(A1B1))·seg(CB1)·seg(A1C), 합→cdots
add(id="70ba5f0e", qtype="choice",
    question="그림과 같이 [[seg(AB) = 1]], [[seg(AC) = 2]]인 직각삼각형 ABC에서 꼭짓점 A를 중심, [[seg(AB)]]를 반지름으로 하는 원을 그렸을 때, [[seg(AC)]]와 만나는 점을 [[sub(A,1)]], [[perp(seg(AC), seg(A1B1))]]이면서 [[seg(BC)]] 위에 있는 점을 [[sub(B,1)]], 다시 꼭짓점 [[sub(B,1)]]을 중심, [[seg(A1B1)]]을 반지름으로 하는 원을 그렸을 때, [[seg(CB1)]]과 만나는 점을 [[sub(B,2)]], [[perp(seg(CB1), seg(A2B2))]]이면서 [[seg(A1C)]] 위에 있는 점을 [[sub(A,2)]]라 하자.\n위와 같은 과정을 계속 반복해 나갈 때,\n[[seg(AB) + seg(A1B1) + seg(A2B2) + cdots]]의 값은?",
    choices=["[[frac(3 + sqrt(3), 2)]]", "[[frac(3,2) + sqrt(3)]]", "[[frac(3 + 3 sqrt(3), 2)]]", "[[2 + frac(sqrt(3),2)]]", "[[2 + sqrt(3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(∠B 직각, AB=1, AC=2), A 중심 반지름 1 호와 AC의 교점 A₁, A₁B₁⊥AC(B₁은 BC 위), B₁ 중심 호와 교점 B₂, A₂B₂⊥CB₁, A₃, B₃ …"}}],
    confidence=0.85,
    note="첨자 점 선분 윗줄을 seg(A1B1)·seg(CB1)·seg(A1C)로, ⊥를 perp로, 합을 cdots로 한 식에. 답 ① 유지(빠른정답 3과 불일치는 1차와 동일)")

# 35. b338a6b8 — 등비급수 p71: ∠D₁OA₁→angle(D1OA1), 첨자 점→sub 텍스트 혼합
add(id="b338a6b8", qtype="choice",
    question="그림과 같이 한 변의 길이가 [[a]]인 정사각형 O[[sub(B,1)]][[sub(C,1)]][[sub(A,0)]]이 있다. 삼각형 O[[sub(A,1)]][[sub(D,1)]]이 [[angle(D1OA1) = deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,1)]][[sub(C,1)]], [[sub(A,0)]][[sub(C,1)]] 위에 각각 점 [[sub(A,1)]], [[sub(D,1)]]을 잡고 변 O[[sub(A,1)]]의 길이를 [[sub(l,1)]]이라 하자.\n선분 O[[sub(A,1)]]을 한 변으로 하는 정사각형 O[[sub(B,2)]][[sub(C,2)]][[sub(A,1)]]에서 삼각형 O[[sub(A,2)]][[sub(D,2)]]가 [[angle(D2OA2) = deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,2)]][[sub(C,2)]], [[sub(A,1)]][[sub(C,2)]] 위에 각각 점 [[sub(A,2)]], [[sub(D,2)]]를 잡고 변 O[[sub(A,2)]]의 길이를 [[sub(l,2)]]라 하자.\n선분 O[[sub(A,2)]]를 한 변으로 하는 정사각형 O[[sub(B,3)]][[sub(C,3)]][[sub(A,2)]]에서 삼각형 O[[sub(A,3)]][[sub(D,3)]]이 [[angle(D3OA3) = deg(30)]]인 이등변삼각형이 되도록 변 [[sub(B,3)]][[sub(C,3)]], [[sub(A,2)]][[sub(C,3)]] 위에 각각 점 [[sub(A,3)]], [[sub(D,3)]]을 잡고 변 O[[sub(A,3)]]의 길이를 [[sub(l,3)]]이라 하자.\n이와 같은 과정을 계속하여 얻은 이등변삼각형 O[[sub(A,n)]][[sub(D,n)]]에서 변 O[[sub(A,n)]]의 길이를 [[sub(l,n)]]이라 하자. [[sum(n, 1, inf, frac(1, sub(l,n))) = 2 + sqrt(3)]]일 때, [[a]]의 값은?",
    choices=["[[sqrt(3)]]", "[[1 + sqrt(3)]]", "[[2 sqrt(3)]]", "[[2 + sqrt(3)]]", "[[3 sqrt(3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "점 O를 공유하며 회전·확대되는 정사각형 OB₁C₁A₀, OB₂C₂A₁, OB₃C₃A₂ …, 각 정사각형 안의 이등변삼각형 OA₁D₁, OA₂D₂, OA₃D₃ 음영, 변 길이 a, l₁, l₂, l₃ 표시"}}],
    confidence=0.85,
    note="∠D₁OA₁ 등을 angle(D1OA1)로, 첨자 점 이름을 sub 텍스트 혼합으로. 답 ① 유지")

# 36. 43ea3ac3 — 등비급수 p73: ∠OP₁A₂→angle(OP1A2), 첨자 점 이름→sub
add(id="43ea3ac3", qtype="choice",
    question="그림과 같이 중심이 O이고 반지름의 길이가 [[2 sqrt(3)]]인 원 [[sub(O,1)]]의 6등분점을 각각 [[sub(A,1)]], [[sub(B,1)]], [[sub(C,1)]], [[sub(D,1)]], [[sub(E,1)]], [[sub(F,1)]]이라 하자. 중심각의 크기가 [[deg(60)]]인 부채꼴 O[[sub(A,1)]][[sub(B,1)]]의 호 [[sub(A,1)]][[sub(B,1)]]의 이등분점을 [[sub(P,1)]]이라 하고, 선분 O[[sub(A,1)]] 위에 [[angle(OP1A2) = deg(45)]]가 되도록 점 [[sub(A,2)]]를 정한다.\n중심이 O이고 선분 O[[sub(A,2)]]를 반지름으로 하는 원 [[sub(O,2)]]가 5개의 선분 O[[sub(B,1)]], O[[sub(C,1)]], O[[sub(D,1)]], O[[sub(E,1)]], O[[sub(F,1)]]과 만나는 점을 각각 [[sub(B,2)]], [[sub(C,2)]], [[sub(D,2)]], [[sub(E,2)]], [[sub(F,2)]]라 하고, 원 [[sub(O,2)]]의 외부에 정육각형 [[sub(A,2)]][[sub(B,2)]][[sub(C,2)]][[sub(D,2)]][[sub(E,2)]][[sub(F,2)]]의 각 변을 지름으로 하는 6개의 반원을 그리고, 이 6개의 반원의 호의 길이의 합을 [[sub(l,1)]]이라 하자.\n중심각의 크기가 [[deg(60)]]인 부채꼴 O[[sub(A,2)]][[sub(B,2)]]의 호 [[sub(A,2)]][[sub(B,2)]]의 이등분점을 [[sub(P,2)]]라 하고, 선분 O[[sub(A,2)]] 위에 [[angle(OP2A3) = deg(45)]]가 되도록 점 [[sub(A,3)]]을 정한다.\n중심이 O이고 선분 O[[sub(A,3)]]을 반지름으로 하는 원 [[sub(O,3)]]이 5개의 선분 O[[sub(B,2)]], O[[sub(C,2)]], O[[sub(D,2)]], O[[sub(E,2)]], O[[sub(F,2)]]와 만나는 점을 각각 [[sub(B,3)]], [[sub(C,3)]], [[sub(D,3)]], [[sub(E,3)]], [[sub(F,3)]]이라 하고, 원 [[sub(O,3)]]의 외부에 정육각형 [[sub(A,3)]][[sub(B,3)]][[sub(C,3)]][[sub(D,3)]][[sub(E,3)]][[sub(F,3)]]의 각 변을 지름으로 하는 6개의 반원을 그리고, 이 6개의 반원의 호의 길이의 합을 [[sub(l,2)]]라 하자.\n이와 같은 과정을 계속하여 [[n]]번째 얻은 6개의 반원의 호의 길이의 합을 [[sub(l,n)]]이라 할 때, [[sum(n, 1, inf, sub(l,n))]]의 값은?",
    choices=["[[6(1 + sqrt(3)) pi]]", "[[6(2 + sqrt(3)) pi]]", "[[6(3 + sqrt(3)) pi]]", "[[12(2 + sqrt(3)) pi]]", "[[12(3 + sqrt(3)) pi]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "동심원 O₁, O₂, O₃과 6등분점, 내접 정육각형 A₂B₂…F₂, A₃B₃…F₃, 각 변을 지름으로 하는 반원(호 l₁, l₂), 점 P₁, P₂"}}],
    confidence=0.85,
    note="∠OP₁A₂·∠OP₂A₃을 angle(…)로, 첨자 점·원 이름을 sub 텍스트 혼합으로. 답 ③ 유지")

# 37. 7017d341 — 등비급수 p75: seg(A1B1)=1, seg(A1D1)=2, 첨자 점→sub; ♡는 도형 이름(텍스트)
add(id="7017d341", qtype="choice",
    question="그림과 같이 [[seg(A1B1) = 1]], [[seg(A1D1) = 2]]인 직사각형 [[sub(A,1)]][[sub(B,1)]][[sub(C,1)]][[sub(D,1)]]에 대하여 선분 [[sub(A,1)]][[sub(D,1)]]의 중점을 M이라 하자. 선분 [[sub(A,1)]][[sub(D,1)]]을 지름으로 하는 반원과 선분 [[sub(A,1)]]M과 선분 M[[sub(D,1)]]을 각각 지름으로 하는 두 반원을 그려서 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,1)]]이라 하자.\n선분 M[[sub(B,1)]]과 선분 M[[sub(C,1)]]이 선분 [[sub(A,1)]][[sub(D,1)]]을 지름으로 하는 반원과 만나는 점을 각각 [[sub(B,2)]], [[sub(C,2)]]라 하고, 점 [[sub(B,2)]]와 점 [[sub(C,2)]]에서 선분 [[sub(A,1)]][[sub(D,1)]]에 내린 수선의 발을 각각 [[sub(A,2)]], [[sub(D,2)]]라 하자. 선분 [[sub(A,2)]][[sub(D,2)]]를 지름으로 하는 반원과 선분 [[sub(A,2)]]M과 선분 M[[sub(D,2)]]를 각각 지름으로 하는 두 반원을 그려서 새로 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,2)]]라 하자.\n이와 같은 과정을 계속하여 [[n]]번째 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,n)]]이라 할 때, [[sum(n, 1, inf, sub(l,n))]]의 값은?",
    choices=["[[(1 + sqrt(2)) pi]]", "[[(2 + sqrt(2)) pi]]", "[[(3 + 2 sqrt(2)) pi]]", "[[(4 + 2 sqrt(2)) pi]]", "[[(5 + 3 sqrt(2)) pi]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 A₁B₁C₁D₁(위변 A₁D₁, 중점 M), 큰 반원(아래)과 두 작은 반원(위)으로 된 하트 모양이 점점 작아지며 겹쳐 그려짐, MB₁·MC₁과 반원의 교점 B₂, C₂, 수선의 발 A₂, D₂"}}],
    confidence=0.85,
    note="[2013년 11월 고2 이과 15번/4점]. 윗줄 선분 A₁B₁=1, A₁D₁=2를 seg로, 첨자 점 이름을 sub 텍스트 혼합으로(♡는 원문 도형 이름, 텍스트). 답 ④ 유지(빠른정답 27과 불일치는 1차와 동일)")

# 38. 54f59415 — 등비급수 p79
add(id="54f59415", qtype="choice",
    question="그림과 같이 [[seg(A1B1) = sqrt(2)]], [[seg(A1D1) = 2 sqrt(2)]]인 직사각형 [[sub(A,1)]][[sub(B,1)]][[sub(C,1)]][[sub(D,1)]]에 대하여 선분 [[sub(A,1)]][[sub(D,1)]]의 중점을 M이라 하자. 선분 [[sub(A,1)]][[sub(D,1)]]을 지름으로 하는 반원과 선분 [[sub(A,1)]]M과 선분 M[[sub(D,1)]]을 각각 지름으로 하는 두 반원을 그려서 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,1)]]이라 하자. 선분 M[[sub(B,1)]]과 선분 M[[sub(C,1)]]이 선분 [[sub(A,1)]][[sub(D,1)]]을 지름으로 하는 반원과 만나는 점을 각각 [[sub(B,2)]], [[sub(C,2)]]라 하고, 점 [[sub(B,2)]]와 점 [[sub(C,2)]]에서 선분 [[sub(A,1)]][[sub(D,1)]]에 내린 수선의 발을 각각 [[sub(A,2)]], [[sub(D,2)]]라 하자. 선분 [[sub(A,2)]][[sub(D,2)]]를 지름으로 하는 반원과 선분 [[sub(A,2)]]M과 선분 M[[sub(D,2)]]를 각각 지름으로 하는 두 반원을 그려서 새로 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,2)]]라 하자.\n이와 같은 과정을 계속하여 [[n]]번째 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,n)]]이라 할 때, [[sum(n, 1, inf, sub(l,n))]]의 값은?",
    choices=["[[(2 + 2 sqrt(2)) pi]]", "[[(3 + 2 sqrt(2)) pi]]", "[[(3 + 4 sqrt(2)) pi]]", "[[(4 + 2 sqrt(2)) pi]]", "[[(4 + 4 sqrt(2)) pi]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 A₁B₁C₁D₁(위변 A₁D₁, 중점 M), 큰 반원(아래)과 두 작은 반원(위)으로 된 하트 모양이 점점 작아지며 겹쳐 그려짐, 교점 B₂, C₂, 수선의 발 A₂, D₂"}}],
    confidence=0.85,
    note="윗줄 선분 A₁B₁=√2, A₁D₁=2√2를 seg로, 첨자 점 이름을 sub 텍스트 혼합으로(♡는 텍스트). 답 ⑤ 유지(빠른정답 2와 불일치는 1차와 동일)")

# 39. 65159906 — 등비급수 p81: 좌표 붙은 첨자 점→app(sub(A,1), 0, 3), 나머지 첨자 점→sub('호 B₁A₁D₁'은 낱말)
add(id="65159906", qtype="choice",
    question="그림과 같이 원점을 중심으로 하고 반지름의 길이가 3인 원 [[sub(O,1)]]을 그리고, 원 [[sub(O,1)]]이 좌표축과 만나는 네 점을 각각 [[app(sub(A,1), 0, 3)]], [[app(sub(B,1), -3, 0)]], [[app(sub(C,1), 0, -3)]], [[app(sub(D,1), 3, 0)]]이라 하자.\n두 점 [[sub(B,1)]], [[sub(D,1)]]을 모두 지나고 두 점 [[sub(A,1)]], [[sub(C,1)]]을 각각 중심으로 하는 두 원이 원 [[sub(O,1)]]의 내부에서 [[y]]축과 만나는 점을 각각 [[sub(C,2)]], [[sub(A,2)]]라 하자.\n호 [[sub(B,1)]][[sub(A,1)]][[sub(D,1)]]과 호 [[sub(B,1)]][[sub(A,2)]][[sub(D,1)]]로 둘러싸인 도형의 넓이를 [[sub(S,1)]], 호 [[sub(B,1)]][[sub(C,1)]][[sub(D,1)]]과 호 [[sub(B,1)]][[sub(C,2)]][[sub(D,1)]]로 둘러싸인 도형의 넓이를 [[sub(T,1)]]이라 하자.\n선분 [[sub(A,2)]][[sub(C,2)]]를 지름으로 하는 원 [[sub(O,2)]]를 그리고, 원 [[sub(O,2)]]가 [[x]]축과 만나는 두 점을 각각 [[sub(B,2)]], [[sub(D,2)]]라 하자.\n두 점 [[sub(B,2)]], [[sub(D,2)]]를 모두 지나고 두 점 [[sub(A,2)]], [[sub(C,2)]]를 각각 중심으로 하는 두 원이 원 [[sub(O,2)]]의 내부에서 [[y]]축과 만나는 점을 각각 [[sub(C,3)]], [[sub(A,3)]]이라 하자. 호 [[sub(B,2)]][[sub(A,2)]][[sub(D,2)]]과 호 [[sub(B,2)]][[sub(A,3)]][[sub(D,2)]]로 둘러싸인 도형의 넓이를 [[sub(S,2)]], 호 [[sub(B,2)]][[sub(C,2)]][[sub(D,2)]]과 호 [[sub(B,2)]][[sub(C,3)]][[sub(D,2)]]로 둘러싸인 도형의 넓이를 [[sub(T,2)]]라 하자.\n이와 같은 과정을 계속하여 [[n]]번째 얻은 호 [[sub(B,n)]][[sub(A,n)]][[sub(D,n)]]과 호 [[sub(B,n)]][[sub(A,n+1)]][[sub(D,n)]]으로 둘러싸인 도형의 넓이를 [[sub(S,n)]], 호 [[sub(B,n)]][[sub(C,n)]][[sub(D,n)]]과 호 [[sub(B,n)]][[sub(C,n+1)]][[sub(D,n)]]로 둘러싸인 도형의 넓이를 [[sub(T,n)]]이라 할 때, [[sum(n, 1, inf, (sub(S,n) + sub(T,n)))]]의 값은?",
    choices=["[[6(sqrt(2) + 1)]]", "[[6(sqrt(3) + 1)]]", "[[6(sqrt(5) + 1)]]", "[[9(sqrt(2) + 1)]]", "[[9(sqrt(3) + 1)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 중심 반지름 3 원 O₁과 A₁(0,3), B₁(-3,0), C₁(0,-3), D₁(3,0), A₁·C₁ 중심 호 B₁A₂D₁·B₁C₂D₁, 초승달 모양 영역 S₁·T₁ 음영, 안쪽으로 반복되는 작은 원들"}}],
    confidence=0.85,
    note="[2009년 11월 고3 문과 15번]. 좌표 붙은 첨자 점 A₁(0, 3) 등을 app(sub(A,1), 0, 3)으로, 첨자 점·원 이름을 sub 텍스트 혼합으로(원문 '호 B₁A₁D₁'은 기호 없이 낱말). 답 ④ 유지")

# 40. 86b2d142 — 등비급수 p82: 첨자 원 이름(C₁, Cₙ, Cₙ₊₁)→sub
add(id="86b2d142", qtype="choice",
    question="그림과 같이 원점 O와 점 [[point(2, 0)]]을 지름의 양 끝으로 하는 원을 [[sub(C,1)]]이라 하자. 또, 원 [[sub(C,1)]]과 직선 [[y = x]]가 만나는 두 점을 지름의 양 끝으로 하는 원을 [[sub(C,2)]], 원 [[sub(C,2)]]와 [[y]]축이 만나는 두 점을 지름의 양 끝으로 하는 원을 [[sub(C,3)]]이라 하자. 또, 원 [[sub(C,3)]]과 직선 [[y = -x]]가 만나는 두 점을 지름의 양 끝으로 하는 원을 [[sub(C,4)]], 원 [[sub(C,4)]]와 [[x]]축이 만나는 두 점을 지름의 양 끝으로 하는 원을 [[sub(C,5)]]라 하자.\n이와 같은 방법으로 중심이 차례로 직선 [[y = x]], [[y]]축, 직선 [[y = -x]], [[x]]축, ⋯ 위에 있는 원 [[sub(C,6)]], [[sub(C,7)]], [[sub(C,8)]], [[sub(C,9)]], ⋯를 한없이 만들어 갈 때, 원 [[sub(C,n)]]의 내부와 원 [[sub(C,n+1)]]의 외부의 공통부분(어두운 부분)의 넓이를 [[sub(S,n)]] ([[n]] = 1, 2, 3, ⋯)이라 하자. 이때 [[sum(n, 1, inf, sub(S,n))]]의 값은?",
    choices=["[[pi + 1]]", "[[frac(3,2) pi]]", "[[frac(5,4)(pi + 1)]]", "[[frac(3,2)(pi + 1)]]", "[[2 pi]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 4개 패널: 원 C₁(지름 O~(2,0))과 y=x 위 원 C₂(S₁ 음영), C₃(S₂ 음영), y=-x 위 C₄(S₃ 음영), C₅(S₄ 음영) — 원점을 지나며 점점 작아지는 원들"}}],
    confidence=0.85,
    note="[2008년 3월 고3 이과 17번]. 첨자 원 이름을 sub 텍스트 혼합으로(열거의 줄임표는 텍스트). 답 ① 유지(빠른정답 5와 불일치는 1차와 동일)")

# 41. b86d59fd — 수열의 극한 p91: 가변 첨자 선분식 극한을 lim(frac(A sub(C,n) - O sub(C,n), sub(B,1) sub(D,n)))로(윗줄 생략)
add(id="b86d59fd", qtype="choice",
    question="다음 그림과 같이 가로의 길이가 [[n]], 세로의 길이가 60인 직사각형 AO[[sub(C,n)]][[sub(B,n)]]에 대하여 대각선 A[[sub(C,n)]]과 선분 [[sub(B,1)]][[sub(C,1)]]의 교점을 [[sub(D,n)]]이라 한다.\n이때 [[lim(n, inf, frac(A sub(C,n) - O sub(C,n), sub(B,1) sub(D,n)))]]의 값은? (단, [[n]]은 자연수이다.)",
    choices=["[[12]]", "[[15]]", "[[20]]", "[[30]]", "[[60]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 AOCₙBₙ(A 좌상, O 좌하, Cₙ 우하, Bₙ 우상, 세로 60), 위변 위 B₁(AB₁=1), B₂ …, 아래변 위 C₁(D₁), C₂ …, 대각선 ACₙ과 B₁C₁의 교점 Dₙ, D₂ … 표시"}}],
    confidence=0.85,
    note="텍스트였던 극한식을 lim(n, inf, frac(…))로; 가변 첨자 선분 ACₙ·OCₙ·B₁Dₙ은 곱 표기(윗줄 생략). 답 ④ 유지")

# 42. 1137471e — 삼각함수의 덧셈정리 p74: ∠P₁OP₂→angle(P1OP2)
add(id="1137471e", qtype="choice",
    question="두 직선 [[y = x + a]], [[y = frac(1,5) x + b]]가 원 [[pow(x,2) + pow(y,2) = pow(r,2)]]에 접하는 점을 각각 [[sub(P,1)]], [[sub(P,2)]]라 하고 [[angle(P1OP2) = alpha]]일 때, [[tan(alpha)]]의 값은? (단, [[a < 0]], [[b < 0]])",
    choices=["[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(5,6)]]", "[[1]]", "[[frac(7,6)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 중심 원 x²+y²=r², 접선 y=x+a, y=x/5+b(모두 원 아래쪽에서 접함), 접점 P₁, P₂, 각 α"}}],
    confidence=0.85,
    note="∠P₁OP₂=α를 angle(P1OP2) = alpha로, 첨자 점을 sub로. 답 ② 유지(빠른정답 32와 불일치는 1차와 동일)")

# 43. 2e1223c3 — 삼각함수의 덧셈정리 p84: 원 이름 C₁, C₂→sub
add(id="2e1223c3", qtype="short",
    question="다음 그림과 같이 중심이 점 [[A(2, 0)]]이고 반지름의 길이가 2인 원 [[sub(C,1)]]과 중심이 점 [[B(-3, 0)]]이고 반지름의 길이가 3인 원 [[sub(C,2)]]가 있다. [[y]]축 위의 점 [[P(0, a)]] ([[a > 3]])에서 원 [[sub(C,1)]]에 그은 접선 중 [[y]]축이 아닌 직선이 원 [[sub(C,1)]]과 접하는 점을 Q, 원 [[sub(C,2)]]에 그은 접선 중 [[y]]축이 아닌 직선이 원 [[sub(C,2)]]와 접하는 점을 R라 하고 [[angle(RPQ) = theta]]라 하자.\n[[tan(theta) = frac(3,4)]]일 때, [[pow(a,2) - 15a]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: x축 위 중심 A(2,0) 반지름 2 원 C₁, B(-3,0) 반지름 3 원 C₂(원점에서 외접), y축 위 점 P에서 두 원에 그은 접선, 접점 Q, R, 각 θ"}}],
    confidence=0.85,
    note="[2019년 4월 고3 이과 29번 변형]. 첨자 원 이름 C₁, C₂를 sub 텍스트 혼합으로. 답 6 유지(빠른정답 3과 불일치는 1차와 동일)")

# 44. 88632709 — 삼각함수의 덧셈정리 p86: 원 이름 C₁, C₂→sub
add(id="88632709", qtype="choice",
    question="점 O를 중심으로 하고 반지름의 길이가 각각 1, 2인 두 원 [[sub(C,1)]], [[sub(C,2)]]가 있다. 원 [[sub(C,1)]] 위의 두 점 P, Q와 원 [[sub(C,2)]] 위의 점 R에 대하여 [[angle(QOP) = alpha]], [[angle(ROQ) = beta]]라 하자.\n[[perp(seg(OQ), seg(QR))]]이고 [[sin(alpha) = frac(sqrt(3),3)]]일 때, [[cos(alpha + beta)]]의 값은?\n(단, [[0 < alpha < frac(pi,2)]], [[0 < beta < frac(pi,2)]])",
    choices=["[[frac(sqrt(3) - 3, 6)]]", "[[frac(sqrt(6) - sqrt(3), 6)]]", "[[frac(sqrt(6) - 3, 6)]]", "[[frac(sqrt(6) - 2 sqrt(3), 6)]]", "[[frac(sqrt(6) - 3 sqrt(2), 6)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "동심원 C₁(반지름 1), C₂(반지름 2), C₁ 위 점 P(오른쪽), Q, C₂ 위 점 R, 각 α=∠QOP, β=∠ROQ, Q에서 직각 표시(OQ⊥QR)"}}],
    confidence=0.85,
    note="[2017년 3월 고3 이과 10번 변형]. 첨자 원 이름 C₁, C₂를 sub 텍스트 혼합으로. 답 ③ 유지(빠른정답 15와 불일치는 1차와 동일)")

# ================= esc_sonnet_h3-2_4of4 =================
# 45. a6825c71 — 여러 가지 함수의 적분 p2: f′(1/2)→app(prime(f), frac(1,2))
add(id="a6825c71", qtype="choice",
    question="실수 전체의 집합에서 미분가능한 함수 [[f(x)]]가 다음 조건을 만족시킨다.\n(가) [[x > 0]]일 때 [[f(x) = a x pow(e, 2x) + b pow(x,2)]]\n(나) [[sub(x,1) < sub(x,2) < 0]]인 임의의 두 실수 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[f(sub(x,2)) - f(sub(x,1)) = 3 sub(x,2) - 3 sub(x,1)]]\n[[f(frac(1,2)) = 2e]]일 때, [[app(prime(f), frac(1,2))]]의 값은? (단, [[a]], [[b]]는 상수이다.)",
    choices=["[[2e]]", "[[4e]]", "[[6e]]", "[[8e]]", "[[10e]]"],
    figure=None, confidence=0.85,
    note="[2019년 10월 고3 이과 17번/4점]. f′(1/2)를 app(prime(f), frac(1,2))로. 답 ④ 유지")

# 46. 4c956d62 — p15: 도함수 조각 정의 → app(prime(f), x) = cases(…)
add(id="4c956d62", qtype="choice",
    question="함수 [[f(x)]]가 모든 실수에서 연속일 때, 도함수 [[app(prime(f), x)]]가 [[app(prime(f), x) = cases(pow(e, x - 1), x <= 1, frac(1,x), x > 1)]]이다.\n[[f(-1) = e + frac(1, pow(e,2))]]일 때, [[f(e)]]의 값은?",
    choices=["[[e - 2]]", "[[e - 1]]", "[[e]]", "[[e + 1]]", "[[e + 2]]"],
    figure=None, confidence=0.85,
    note="[2016년 3월 고3 이과 7번/3점]. f′(x)를 app(prime(f), x)로, 경우 나눔을 cases로. 답 ⑤ 유지(빠른정답 4와 불일치는 1차와 동일)")

# 47. cdcef23a — p37: f′(0), f′(a)≤f′(b), f″(x)
add(id="cdcef23a", qtype="choice",
    question="실수 전체의 집합에서 미분가능하고, 다음 조건을 만족시키는 모든 함수 [[f(x)]]에 대하여 [[dinteg(0, 2, f(x), x)]]의 최솟값은?\n(가) [[f(0) = 1]], [[app(prime(f), 0) = 1]]\n(나) [[0 < a < b < 2]]이면 [[app(prime(f), a) <= app(prime(f), b)]]이다.\n(다) 구간 [[itv(0, 1, oo)]]에서 [[app(prime(f, 2), x) = pow(e, x)]]이다.",
    choices=["[[frac(1,2) e - 1]]", "[[frac(3,2) e - 1]]", "[[frac(5,2) e - 1]]", "[[frac(7,2) e - 2]]", "[[frac(9,2) e - 2]]"],
    figure=None, confidence=0.85,
    note="[2010년 11월 고3 이과 미분과 적분 29번]. f′(0)·f′(a)·f′(b)를 app(prime(f), ·)로, f″(x)를 app(prime(f, 2), x)로. 답 ③ 유지")

# 48. fb80dd71 — 정적분과 급수의 합 p6: 빈칸 □→box(1)로 극한식을 한 식에
add(id="fb80dd71", qtype="choice",
    question="다음은 곡선 [[y = pow(x,2)]]과 [[x]]축 및 직선 [[x = 2]]로 둘러싸인 부분의 넓이를 구분구적법을 이용하여 구하는 과정이다. □ 안에 알맞은 식은?\n닫힌 구간 [[itv(0, 2, cc)]]를 [[n]]등분하면 양 끝점을 포함한 각 분점의 [[x]]좌표는 각각 0, [[frac(2,n)]], [[frac(4,n)]], ⋯, [[frac(2(n - 1), n)]], [[frac(2n, n)]] (= 2)이고 다음 그림의 색칠한 직사각형의 넓이의 합을 [[sub(S,n)]]이라 하면 구하는 넓이 [[S]]는\n[[S = lim(n, inf, sub(S,n)) = lim(n, inf, box(1)) = frac(8,3)]]",
    choices=["[[sum(k, 0, n - 1, frac(4k, n))]]", "[[sum(k, 0, n - 1, frac(4 pow(k,2), pow(n,2)))]]", "[[sum(k, 0, n - 1, frac(8 pow(k,2), pow(n,2)))]]", "[[sum(k, 0, n - 1, frac(8 pow(k,2), pow(n,3)))]]", "[[sum(k, 0, n - 1, frac(8 pow(k,3), pow(n,3)))]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "곡선 y=x²와 [0,2]를 n등분한 분점 2/n, 4/n, 6/n, 8/n, 10/n, …, 2(n−1)/n, 2n/n(=2) 위에 세운 색칠한 직사각형들(높이는 왼쪽 끝점의 함숫값), y=4 점선 표시"}}],
    confidence=0.85,
    note="극한식 속 빈칸 상자(원문은 이름 없는 □)를 box(1)로 하여 S = lim Sₙ = lim □ = 8/3을 한 식에. 답 ④ 유지(빠른정답 1과 불일치는 1차와 동일)")

# 49. 8bc42ce6 — p42: 좌표 붙은 점 A(−1,0)→[[A(-1, 0)]], 가변 첨자 라벨(D_k, P_k, Q_k)은 sub 텍스트 혼합
add(id="8bc42ce6", qtype="short",
    question="그림과 같이 곡선 [[y = -pow(x,2) + 1]] 위에 세 점 [[A(-1, 0)]], [[B(1, 0)]], [[C(0, 1)]]이 있다. 2 이상의 자연수 [[n]]에 대하여 선분 OC를 [[n]]등분할 때, 양 끝점을 포함한 각 분점을 차례로 O = [[sub(D,0)]], [[sub(D,1)]], [[sub(D,2)]], ⋯, [[sub(D, n - 1)]], [[sub(D,n)]] = C라 하자. 직선 A[[sub(D,k)]]가 곡선과 만나는 점 중 A가 아닌 점을 [[sub(P,k)]]라 하고, 점 [[sub(P,k)]]에서 [[x]]축에 내린 수선의 발을 [[sub(Q,k)]]라 하자. ([[k]] = 1, 2, ⋯, [[n]])\n삼각형 A[[sub(P,k)]][[sub(Q,k)]]의 넓이를 [[sub(S,k)]]라 할 때,\n[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(S,k))) = alpha]]\n이다. [[24 alpha]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y=−x²+1, A(−1,0)·B(1,0)·C(0,1)(=D_n), y축 위의 분점 D₁, D₂, …, D_k, …, D_{n−1}, 직선 AD_k와 곡선의 교점 P_k, 수선의 발 Q_k(직각 표시)"}}],
    confidence=0.85,
    note="[2014년 4월 고3 이과 28번/4점]. 좌표 붙은 점을 A(-1, 0) 적용형으로; 가변 첨자 점 라벨(D_k, P_k, Q_k)은 sub 텍스트 혼합(윗줄 없음). 답 11 유지(빠른정답 5와 불일치는 1차와 동일)")

# 50. 6ec71ce8 — p46: P_k(좌표)→app(sub(P,k), …), 가변 첨자 라벨→sub
add(id="6ec71ce8", qtype="short",
    question="그림과 같이 2 이상의 자연수 [[n]]에 대하여 곡선 [[y = sin(frac(x,2))]] 위의 점 [[app(sub(P,k), frac(2k pi, n), sin(frac(k pi, n)))]] ([[k]] = 1, 2, 3, ⋯, [[n]])에서의 접선이 [[y]]축과 만나는 점을 [[sub(Q,k)]]라 하고, 점 [[sub(P,k)]] ([[k]] = 1, 2, 3, ⋯, [[n - 1]])에서 [[x]]축에 내린 수선의 발을 [[sub(R,k)]]라 하자. 두 삼각형 O[[sub(P,k)]][[sub(Q,k)]], O[[sub(P,k)]][[sub(R,k)]]의 넓이를 각각 [[sub(S,k)]], [[sub(T,k)]]라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n, (sub(S,k) - sub(T,k))))]]의 값을 구하시오. (단, [[sub(T,n) = 0]]이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "곡선 y=sin(x/2)(0~2π 부근), 곡선 위의 점 P_k에서의 접선과 y축의 교점 Q_k, P_k에서 x축에 내린 수선의 발 R_k(직각 표시), 원점 O, 선분 OP_k, x축의 2π 표시"}}],
    confidence=0.85,
    note="좌표 붙은 첨자 점 P_k(2kπ/n, sin(kπ/n))를 app(sub(P,k), …)로; 가변 첨자 점 라벨은 sub 텍스트 혼합. 답 2 유지(빠른정답 3과 불일치는 1차와 동일)")

# 51. bbbc1fba — p47: P₀(0,0)·Pₙ(4,0)→app(sub(P,·), …), l_k = P_kQ_k(윗줄)는 곱 표기(윗줄 생략)
add(id="bbbc1fba", qtype="choice",
    question="함수 [[f(x) = a pow(x,2) + b]] ([[a > 0]], [[b > 0]])이 있다. 자연수 [[n]]에 대하여 두 점 [[point(0, 0)]], [[point(4, 0)]]을 잇는 선분을 [[n]]등분한 각 분점 (양 끝점도 포함)을 차례대로 [[app(sub(P,0), 0, 0)]], [[sub(P,1)]], [[sub(P,2)]], ⋯, [[app(sub(P,n), 4, 0)]]이라 하자. 점 [[sub(P,k)]] ([[k]] = 0, 1, 2, ⋯, [[n]])을 지나면서 [[x]]축에 수직인 직선과 곡선 [[y = f(x)]]의 교점을 [[sub(Q,k)]]라 하자.\n[[sub(l,k) = sub(P,k) sub(Q,k)]]라 하면 [[sub(l,1) + sub(l,n) = frac(18 pow(n,2) + 16, pow(n,2))]]일 때,\n[[lim(n, inf, frac(4,n) sum(k, 1, n, sqrt(sub(l,k) - 1) pow(e, sub(l,k))))]]의 값은?",
    choices=["[[frac(pow(e,16) - 1, 2)]]", "[[frac(pow(e,17) - e, 2)]]", "[[frac(pow(e,17) - 1, 2)]]", "[[frac(pow(e,16), 2)]]", "[[pow(e,17) + 1]]"],
    figure=None, confidence=0.85,
    note="좌표 붙은 첨자 점 P₀(0, 0)·Pₙ(4, 0)을 app(sub(P,·), …)로; l_k = P_kQ_k(윗줄)는 sub(P,k) sub(Q,k) 곱 표기(윗줄 생략)로 한 식에. 답 ② 유지")

# 52. 9cd31371 — p48: A_k(x_k, f(x_k))→app(sub(A,k), …); 분모 B_kC_k(윗줄)는 곱 표기(윗줄 생략)
add(id="9cd31371", qtype="choice",
    question="[[n]] 이하의 자연수 [[k]]에 대하여 [[sub(x,k) = frac(k,n)]]라 하자.\n함수 [[f(x) = pow(e, 3x) - pow(e, x) + 2e x]]에 대하여 곡선 [[y = f(x)]] 위의 점 [[app(sub(A,k), sub(x,k), f(sub(x,k)))]]에서의 접선이 [[x]]축과 만나는 점을 [[sub(B,k)]]라 하고 점 [[sub(A,k)]]에서 [[x]]축에 내린 수선의 발을 [[sub(C,k)]]라 하자. [[lim(n, inf, frac(1,n) sum(k, 1, n, frac(pow(f(sub(x,k)), 3), sub(B,k) sub(C,k))))]]의 값은?\n(단, [[n]]은 자연수이다.)",
    choices=["[[frac(pow(pow(e,4) - e, 4), 4)]]", "[[frac(pow(pow(e,3) - e, 3), 3)]]", "[[pow(e,3)]]", "[[frac(pow(pow(e,3) + e, 3), 3)]]", "[[frac(pow(pow(e,4) + e, 4), 4)]]"],
    figure=None, confidence=0.85,
    note="좌표 붙은 첨자 점 A_k(x_k, f(x_k))를 app(sub(A,k), …)로; 분모 B_kC_k(윗줄)는 곱 표기(윗줄 생략), 분자 {f(x_k)}³은 pow. 답 ④ 유지(빠른정답 3과 불일치는 1차와 동일)")

# 53. 5d964b32 — p49: 가변 첨자 라벨(A_k, B_k)→sub 텍스트 혼합(그대로 통과)
add(id="5d964b32", qtype="short",
    question="그림과 같이 2 이상인 자연수 [[n]]에 대하여 닫힌 구간 [[itv(1, 2, cc)]]를 [[n]]등분한 각 분점(양 끝점도 포함)을 차례로\n[[1 = sub(x,0)]], [[sub(x,1)]], [[sub(x,2)]], ⋯, [[sub(x, n - 1)]], [[sub(x,n) = 2]]\n라 하자. 점 [[point(sub(x,k), 0)]] ([[k]] = 1, 2, 3, ⋯, [[n]])을 지나고 기울기가 [[-2]]인 직선이 곡선 [[y = pow(x,2) + 1]]과 제1사분면에서 만나는 점을 [[sub(A,k)]], [[y]]축과 만나는 점을 [[sub(B,k)]]라 하자. 삼각형 O[[sub(A,k)]][[sub(B,k)]]의 넓이를 [[sub(S,k)]]라 할 때,\n[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(S,k))) = p + q sqrt(2)]]\n이다. [[10(p + q)]]의 값을 구하시오.\n(단, [[O]]는 원점이고, [[p]], [[q]]는 유리수이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=x²+1, (x_k,0)을 지나는 기울기 −2인 직선, 곡선과의 교점 A_k, y축과의 교점 B_k, 삼각형 OA_kB_k 음영, x축의 1·x_k·2 점선 표시"}}],
    confidence=0.85,
    note="가변 첨자 점 라벨(A_k, B_k)은 sub 텍스트 혼합(윗줄 없음) — 도형만 unsupported. 답 13 유지(빠른정답 2와 불일치는 1차와 동일)")

# 54. 60c3747c — p50: 가변 첨자 라벨(P_n)→sub(그대로 통과)
add(id="60c3747c", qtype="choice",
    question="다음 그림과 같이 곡선 [[y = x cos(x)]] ([[x >= 0]])와 직선 [[y = x]]가 접하는 점을 원점 O에 가까운 순서대로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,n)]]이라 하자. 곡선 [[y = x cos(x)]] ([[x >= 0]])와 선분 [[sub(P, n - 1)]][[sub(P,n)]] ([[n]]은 자연수)으로 둘러싸인 도형의 넓이를 [[sub(A,n)]]이라 할 때, [[lim(n, inf, frac(1, pow(n,2)) sum(k, 1, n, sub(A,k)))]]의 값은?\n(단, 원점 O는 [[sub(P,0)]]이라 하자.)",
    choices=["[[pow(pi,2)]]", "[[2 pow(pi,2)]]", "[[3 pow(pi,2)]]", "[[4 pow(pi,2)]]", "[[5 pow(pi,2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=x cos x와 직선 y=x, 접점 P₀(=O), P₁, P₂, 곡선과 선분 P₀P₁·P₁P₂로 둘러싸인 영역 A₁·A₂ 음영"}}],
    confidence=0.85,
    note="첨자 점 라벨(Pₙ)은 sub 텍스트 혼합 — 도형만 unsupported. 답 ② 유지")

# 55. 97a8448c — p54
add(id="97a8448c", qtype="short",
    question="다음 그림과 같이 길이가 8인 선분 AB를 지름으로 하는 반원의 호 AB를 [[n]]등분한 각 분점을 점 A에 가까운 것부터 차례대로 [[sub(P,k)]] ([[k]] = 1, 2, 3, ⋯, [[n - 1]])이라 한다.\n삼각형 AB[[sub(P,k)]]의 넓이를 [[sub(S,k)]]라 할 때, [[lim(n, inf, frac(pi,n) sum(k, 1, n - 1, sub(S,k)))]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "지름 AB=8(중심 O, AO=4 표시)인 반원, 호 위의 분점 P₁, P₂, …, P_k, …, P_{n−1}, 삼각형 ABP_k 음영"}}],
    confidence=0.85,
    note="가변 첨자 점 라벨(P_k)은 sub 텍스트 혼합 — 도형만 unsupported. 답 32 유지(빠른정답 4와 불일치는 1차와 동일)")

# 56. 2cc5ae4b — p57: Aₙ(2, 0)→app(sub(A,n), 2, 0); Σ 안 A_kB_k(윗줄)는 곱 표기(윗줄 생략)
add(id="2cc5ae4b", qtype="short",
    question="다음 그림과 같이 [[x]]축 위의 닫힌 구간 [[itv(0, 2, cc)]]를 [[n]]등분한 점을 앞에서부터 차례대로 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A, n - 1)]]이라 하고, 점 [[sub(A,k)]] ([[1 <= k <= n - 1]])을 지나고 [[y]]축에 평행한 직선이 곡선 [[y = pow(x,2)]]과 만나는 점을 [[sub(B,k)]]라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n, sub(A,k) sub(B,k)))]]의 값을 구하시오. (단, [[app(sub(A,n), 2, 0)]]이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=x², x축 위의 분점 A₁, A₂, A₃, …, A_{n−1}, A_n(x=2)과 곡선 위의 점 B₁, B₂, B₃, …, B_{n−1}, B_n(y=4 점선), 세로 선분 A_kB_k"}}],
    confidence=0.85,
    note="좌표 붙은 첨자 점 Aₙ(2, 0)을 app(sub(A,n), 2, 0)으로; Σ 안 선분 A_kB_k(윗줄)는 곱 표기(윗줄 생략). 답 4/3 유지")

# 57. 80a825e4 — p58
add(id="80a825e4", qtype="choice",
    question="다음 그림과 같이 [[x]]축 위의 구간 [[itv(0, 3, cc)]]을 [[n]]등분한 점을 앞에서부터 차례대로 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], ⋯, [[sub(A, n - 1)]]이라 하고, 점 [[sub(A,k)]]를 지나고 [[y]]축에 평행한 직선이 곡선 [[y = pow(x,2)]]과 만나는 점을 [[sub(B,k)]]라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n, sub(A,k) sub(B,k)))]]의 값은?\n(단, 점 [[sub(A,n)]]의 좌표는 [[point(3, 0)]]이다.)",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=x², x축 위의 분점 A₁, A₂, A₃, …, A_{n−1}, A_n(x=3)과 곡선 위의 점 B₁, B₂, B₃, …, B_{n−1}, B_n(y=9 점선), 세로 선분 A_kB_k"}}],
    confidence=0.85,
    note="Σ 안 선분 A_kB_k(윗줄)는 곱 표기(윗줄 생략), 첨자 점 라벨은 sub 텍스트 혼합. 답 ③ 유지")

# 58. d79354f7 — p59
add(id="d79354f7", qtype="choice",
    question="다음 그림과 같이 [[x]]축 위의 구간 [[itv(2, 4, cc)]]를 [[n]]등분한 점을 앞에서부터 차례대로 [[sub(A,1)]], [[sub(A,2)]] [[sub(A,3)]], ⋯, [[sub(A, n - 1)]]이라 하고, 점 [[sub(A,k)]]를 지나고 [[y]]축에 평행한 직선이 곡선 [[y = frac(1,4) pow(x,3) - 2]]와 만나는 점을 [[sub(B,k)]]라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(A,k) sub(B,k)))]]의 값은?\n(단, 점 [[sub(A,n)]]의 좌표는 [[point(4, 0)]]이다.)",
    choices=["[[frac(9,2)]]", "[[5]]", "[[frac(11,2)]]", "[[6]]", "[[frac(13,2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=(1/4)x³−2(y절편 −2), x축 위의 분점 A₁, A₂, A₃, …, A_{n−1}, A_n(x=4)과 곡선 위의 점 B₁, B₂, B₃, …(y=14 점선), 세로 선분, x=2 표시"}}],
    confidence=0.85,
    note="Σ 안 선분 A_kB_k(윗줄)는 곱 표기(윗줄 생략). 원문 'A₁, A₂ A₃'(콤마 누락) 그대로. 답 ③ 유지")

# 59. 303db9f3 — p60: A(−1,0), B(1,0)→적용형
add(id="303db9f3", qtype="choice",
    question="다음 그림과 같이 좌표평면에서 두 점 [[A(-1, 0)]], [[B(1, 0)]]을 지름의 양 끝으로 하는 원 [[pow(x,2) + pow(y,2) = 1]]의 호 AB를 [[n]]등분하는 점을 [[sub(P,k)]] ([[k]] = 1, 2, 3, ⋯, [[n - 1]])이라 한다. 삼각형 A[[sub(P,k)]]B의 넓이를 [[sub(S,k)]]라 할 때,\n[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(S,k)))]]의 값은?",
    choices=["[[frac(1,pi)]]", "[[frac(2,pi)]]", "[[frac(3,pi)]]", "[[frac(4,pi)]]", "[[frac(5,pi)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 위쪽 반원 x²+y²=1, A(−1,0)·B(1,0)·원점 O, 호 위의 점 P_k, 삼각형 AP_kB 음영"}}],
    confidence=0.85,
    note="좌표 붙은 점을 A(-1, 0) 적용형으로; 가변 첨자 점 라벨(P_k)은 sub 텍스트 혼합. 답 ② 유지")

# 60. 4d46fd70 — p62
add(id="4d46fd70", qtype="short",
    question="다음 그림과 같이 한 변의 길이가 6인 정사각형 ABCD가 있다. 선분 CD를 [[ratio(5, 1)]]로 내분하는 점을 E라 하고 2 이상의 자연수 [[n]]과 [[1 <= k <= n - 1]]인 자연수 [[k]]에 대하여 선분 BE를 [[ratio(k, (n - k))]]로 내분하는 점을 [[sub(P,k)]], [[sub(P,n)]] = E라 하자. 삼각형 BC[[sub(P,k)]]의 넓이를 [[sub(S,k)]]라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n, pow(e, sub(S,k)))) = p pow(e,15) + q]]이다.\n두 유리수 [[p]], [[q]]에 대하여 [[60(p - q)]]의 값을 구하시오.\n(단, [[pow(e,15)]]은 무리수이다.)",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), 변 CD 위의 점 E, 선분 BE 위의 점 P_k, 삼각형 BCP_k 음영"}}],
    confidence=0.85,
    note="가변 첨자 점 라벨(P_k)은 sub 텍스트 혼합 — 도형만 unsupported. 답 8 유지(빠른정답 3과 불일치는 1차와 동일)")

# 61. 7b9aac7d — p63
add(id="7b9aac7d", qtype="short",
    question="다음 그림과 같이 중심각의 크기가 [[frac(pi,2)]]이고, 반지름의 길이가 6인 부채꼴 OAB가 있다. 2 이상의 자연수 [[n]]에 대하여 호 AB를 [[n]]등분한 각 분점을 점 A에서 가까운 것부터 순서대로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, n - 1)]]이라 하자.\n[[1 <= k <= n - 1]]인 자연수 [[k]]에 대하여 점 B에서 선분 O[[sub(P,k)]]에 내린 수선의 발을 [[sub(Q,k)]]라 하고, 삼각형 O[[sub(Q,k)]]B의 넓이를 [[sub(S,k)]]라 하자.\n[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(S,k))) = frac(alpha, pi)]]일 때, 상수 [[alpha]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "부채꼴 OAB(반지름 6, OA 가로·OB 세로, 중심각 π/2), 호 위의 분점 P₁, P₂, P₃, …, P_k, …, P_{n−1}, B에서 OP_k에 내린 수선의 발 Q_k(직각 표시), 삼각형 OQ_kB 음영"}}],
    confidence=0.85,
    note="가변 첨자 점 라벨(P_k, Q_k)은 sub 텍스트 혼합 — 도형만 unsupported. 답 18 유지(빠른정답 2와 불일치는 1차와 동일)")

# 62. 91774f21 — p65: Σ 안 AP_k²(윗줄)는 곱 표기(윗줄 생략)
add(id="91774f21", qtype="short",
    question="한 변의 길이가 1인 정삼각형 ABC에서 변 BC를 [[n]]등분하여 차례로 점 [[sub(P,0)]](= B), [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, n - 1)]], [[sub(P,n)]](= C)를 정할 때,\n[[lim(n, inf, frac(1,n) sum(k, 1, n, pow(A sub(P,k), 2)))]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 ABC(한 변 1, 점선 표시), 변 BC 위의 분점 P₁, P₂, …, P_{n−1}, B(=P₀), C(=P_n)"}}],
    confidence=0.85,
    note="Σ 안 선분 AP_k²(윗줄)는 A sub(P,k) 곱 표기(윗줄 생략). 답 5/6 유지")

# 63. 576909b3 — p66: Σ 안 OQ_k²(윗줄)는 곱 표기(윗줄 생략)
add(id="576909b3", qtype="choice",
    question="다음 그림과 같이 반지름의 길이가 1인 사분원의 호 AB를 5등분하는 점을 각각 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], [[sub(P,4)]]라 하자. 이와 같은 방법으로 사분원의 둘레를 [[n]]등분하여 각 분점을 [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, n - 1)]]라 하고 점 [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, n - 1)]]에서 반지름 OA에 내린 수선의 발을 각각 [[sub(Q,1)]], [[sub(Q,2)]], ⋯, [[sub(Q, n - 1)]]라 하자. [[f(n) = sum(k, 1, n - 1, pow(O sub(Q,k), 2))]]이라 할 때, [[lim(n, inf, frac(f(n), n))]]의 값은?",
    choices=["[[-2]]", "[[-frac(1,2)]]", "[[0]]", "[[frac(1,2)]]", "[[2]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "사분원 OAB(반지름 1, OB 세로·OA 가로), 호 위의 점 P₁, P₂, P₃, P₄와 OA에 내린 수선의 발 Q₁, Q₂, Q₃, Q₄(직각 표시)"}}],
    confidence=0.85,
    note="Σ 안 선분 OQ_k²(윗줄)는 O sub(Q,k) 곱 표기(윗줄 생략). 답 ④ 유지")

# 64. 8df80d3c — p67: OP_k², AP_k²(윗줄)는 곱 표기(윗줄 생략)
add(id="8df80d3c", qtype="choice",
    question="그림과 같이 한 변의 길이가 1인 정삼각형 OAB가 있다. 2 이상의 자연수 [[n]]과 [[1 <= k < n]]인 자연수 [[k]]에 대하여 선분 AB를 [[ratio(k, (n - k))]]로 내분하는 점을 [[sub(P,k)]]라 하자.\n[[sub(l,k) = pow(O sub(P,k), 2) - pow(A sub(P,k), 2)]]이라 할 때, [[lim(n, inf, frac(1,n) sum(k, 1, n - 1, pow(2, sub(l,k))))]]의 값은?",
    choices=["[[frac(1, ln(2))]]", "[[frac(2, ln(2))]]", "[[frac(3, ln(2))]]", "[[frac(4, ln(2))]]", "[[frac(5, ln(2))]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "정삼각형 OAB(O 왼쪽 아래, A 오른쪽 아래, B 위), 변 AB 위의 점 P₁, P₂, P₃, …, P_k, …, P_{n−1}, 선분 OP_k"}}],
    confidence=0.85,
    note="선분 OP_k²·AP_k²(윗줄)는 곱 표기(윗줄 생략). 답 ① 유지")

# 65. 01d47f62 — p74: Σ 안 B_kC_k²(윗줄)는 곱 표기(윗줄 생략)
add(id="01d47f62", qtype="choice",
    question="[[seg(AB) = 2]], [[seg(BC) = 1]], [[angle(B) = deg(90)]]인 직각삼각형 ABC의 변 AB를 [[n]]등분한 점을 다음 그림과 같이 점 A에서 가까운 순서대로 [[sub(B,1)]], [[sub(B,2)]], ⋯, [[sub(B, n - 1)]]이라 하고, 각 점에서 변 BC와 평행한 선분을 그었을 때 변 AC와 만나는 점을 각각 [[sub(C,1)]], [[sub(C,2)]], ⋯, [[sub(C, n - 1)]]이라 할 때, [[lim(n, inf, frac(2 pi, n) sum(k, 1, n - 1, pow(sub(B,k) sub(C,k), 2)))]]의 값은?",
    choices=["[[frac(pi,6)]]", "[[frac(pi,3)]]", "[[frac(pi,2)]]", "[[frac(2,3) pi]]", "[[pi]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, B 왼쪽 아래 직각, C 오른쪽 아래), AB 위의 분점 B₁, B₂, B₃, …, B_{n−2}, B_{n−1}과 AC 위의 점 C₁, C₂, C₃, …, C_{n−2}, C_{n−1}, BC에 평행한 선분 B_kC_k"}}],
    confidence=0.85,
    note="Σ 안 선분 B_kC_k²(윗줄)는 곱 표기(윗줄 생략). 답 ④ 유지(빠른정답 3과 불일치는 1차와 동일)")

# 66. 92b98315 — p75
add(id="92b98315", qtype="short",
    question="그림과 같이 한 변의 길이가 1인 정사각형 ABCD가 있다. 2 이상의 자연수 [[n]]에 대하여 변 BC를 [[n]]등분한 각 분점을 점 B에서 가까운 것부터 차례로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, n - 1)]]이라 하고, 변 CD를 [[n]]등분한 각 분점을 점 C에서 가까운 것부터 차례로 [[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], ⋯, [[sub(Q, n - 1)]]이라 하자.\n[[1 <= k <= n - 1]]인 자연수 [[k]]에 대하여 사각형 A[[sub(P,k)]][[sub(Q,k)]]D의 넓이를 [[sub(S,k)]]라 하자.\n[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(S,k))) = alpha]]일 때, [[150 alpha]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위, 한 변 1), BC 위의 점 P₁, P₂, P₃, …, P_k, …, P_{n−1}, CD 위의 점 Q₁, Q₂, Q₃, …, Q_k, …, Q_{n−1}, 사각형 AP_kQ_kD 음영"}}],
    confidence=0.85,
    note="[2013년 4월 고3 이과 29번/4점]. 가변 첨자 점 라벨(P_k, Q_k)은 sub 텍스트 혼합 — 도형만 unsupported. 답 100 유지(빠른정답 3과 불일치는 1차와 동일)")

# 67. d0f6dae1 — p76
add(id="d0f6dae1", qtype="short",
    question="그림과 같이 중심각의 크기가 [[frac(pi,2)]]이고, 반지름의 길이가 8인 부채꼴 OAB가 있다. 2 이상의 자연수 [[n]]에 대하여 호 AB를 [[n]]등분한 각 분점을 점 A에서 가까운 것부터 차례로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, n - 1)]]이라 하자. [[1 <= k <= n - 1]]인 자연수 [[k]]에 대하여 점 B에서 선분 O[[sub(P,k)]]에 내린 수선의 발을 [[sub(Q,k)]]라 하고, 삼각형 O[[sub(Q,k)]]B의 넓이를 [[sub(S,k)]]라 하자.\n[[lim(n, inf, frac(1,n) sum(k, 1, n - 1, sub(S,k))) = frac(alpha, pi)]]일 때, [[alpha]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "부채꼴 OAB(반지름 8, OA 가로·OB 세로, 중심각 π/2), 호 위의 분점 P₁, P₂, P₃, …, P_k, …, P_{n−1}, B에서 OP_k에 내린 수선의 발 Q_k(직각 표시), 삼각형 OQ_kB 음영"}}],
    confidence=0.85,
    note="[2015년 4월 고3 이과 28번/4점]. 가변 첨자 점 라벨(P_k, Q_k)은 sub 텍스트 혼합 — 도형만 unsupported. 답 32 유지(빠른정답 16과 불일치는 1차와 동일)")

# 68. 37c54bce — p77
add(id="37c54bce", qtype="short",
    question="다음 그림과 같이 중심각의 크기가 [[frac(pi,2)]]이고, 반지름의 길이가 10인 부채꼴 OAB가 있다. 2 이상의 자연수 [[n]]에 대하여 호 AB를 [[2n]]등분한 각 분점을 점 A에서 가까운 것부터 차례로 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, 2n - 1)]] 이라 하자.\n[[1 <= k <= 2n - 1]]인 자연수 [[k]]에 대하여 점 B에서 선분 O[[sub(P,k)]]에 내린 수선의 발을 [[sub(Q,k)]]라 하고, 삼각형 O[[sub(Q,k)]]B의 넓이를 [[sub(S,k)]]라 하자. [[lim(n, inf, frac(1,n) sum(k, 1, 2n - 1, sub(S,k))) = frac(alpha, pi)]]일 때,\n[[alpha]]의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "부채꼴 OAB(반지름 10, OA 가로·OB 세로, 중심각 π/2), 호 위의 분점 P₁, P₂, P₃, …, P_k, …, P_{2n−1}, B에서 OP_k에 내린 수선의 발 Q_k(직각 표시), 삼각형 OQ_kB 음영"}}],
    confidence=0.85,
    note="[2015년 4월 고3 이과 28번 변형]. 가변 첨자 점 라벨(P_k, Q_k)은 sub 텍스트 혼합 — 도형만 unsupported. 답 100 유지(빠른정답 4와 불일치는 1차와 동일)")

# 69. c316b524 — p78: 텍스트였던 lim·줄임표를 lim(… + cdots + …) 한 식으로(P_kQ_k 윗줄은 곱 표기)
add(id="c316b524", qtype="short",
    question="[[seg(AD) = 1]], [[seg(AB) = sqrt(2)]], [[seg(BC) = 3]]인 등변사다리꼴 ABCD에서 변 AB를 [[n]]등분한 점을 각각 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P, n - 1)]]이라 하고 각 점에서 변 BC에 평행한 직선을 그어 변 CD와 만나는 점을 각각 [[sub(Q,1)]], [[sub(Q,2)]], ⋯, [[sub(Q, n - 1)]]이라 할 때,\n[[lim(n, inf, frac(1,n) (pow(sub(P,1) sub(Q,1), 3) + pow(sub(P,2) sub(Q,2), 3) + pow(sub(P,3) sub(Q,3), 3) + cdots + pow(sub(P,n) sub(Q,n), 3)))]]\n의 값을 구하시오.",
    figure=[{"fn": "unsupported", "args": {"raw": "등변사다리꼴 ABCD(AD 위쪽 짧은 변, BC 아래쪽 긴 변), AB 위의 점 P₁, P₂, …, P_{n−1}, B(=P_n), CD 위의 점 Q₁, Q₂, …, Q_{n−1}, C(=Q_n), BC에 평행한 선분 P_kQ_k"}}],
    confidence=0.85,
    note="[2007년 7월 고3 이과 23번]. 텍스트였던 극한을 lim(n, inf, frac(1,n)(… + cdots + …))로 한 식에; 선분 P_kQ_k³(윗줄)는 sub 곱 표기(윗줄 생략). 답 10 유지(빠른정답 100과 불일치는 1차와 동일)")

# 70. 31a8a84e — p79
add(id="31a8a84e", qtype="choice",
    question="그림과 같이 중심이 O, 반지름의 길이가 1이고 중심각의 크기가 [[frac(pi,2)]]인 부채꼴 OAB가 있다.\n자연수 [[n]]에 대하여 호 AB를 [[2n]]등분한 각 분점(양 끝점도 포함)을 차례로 [[sub(P,0)]](= A), [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P, 2n - 1)]], [[sub(P, 2n)]](= B)라 하자. 다음 물음에 답하시오.\n주어진 자연수 [[n]]에 대하여 [[sub(S,k)]] ([[1 <= k <= n]])을 삼각형 O[[sub(P, n - k)]][[sub(P, n + k)]]의 넓이라 할 때,\n[[lim(n, inf, frac(1,n) sum(k, 1, n, sub(S,k)))]]의 값은?",
    choices=["[[frac(1,pi)]]", "[[frac(13, 12 pi)]]", "[[frac(7, 6 pi)]]", "[[frac(5, 4 pi)]]", "[[frac(4, 3 pi)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "부채꼴 OAB(반지름 1, 중심각 π/2, OA 가로), 호 위의 분점 P₀(=A), P₁, …, P_{n−2}, P_{n−1}, P_n, P_{n+1}, P_{n+2}, …, P_{2n−1}, P_{2n}(=B)과 O에서 각 분점으로 그은 선분"}}],
    confidence=0.85,
    note="[2014년 9월 고3 이과 13번/3점]. 가변 첨자 점 라벨(P_{n−k}, P_{n+k})은 sub 텍스트 혼합 — 도형만 unsupported. 답 ① 유지(빠른정답 32와 불일치는 1차와 동일)")

# 71. 1d979d08 — 삼각함수의 극한과 미분 p67: 3구간 cases + (f∘g)(x)→app(comp(f, g), x)
add(id="1d979d08", qtype="choice",
    question="실수 전체의 집합에서 정의된 두 함수\n[[f(x) = pow(sin(x), 2) + a cos(x)]]\n[[g(x) = cases(0, x < -frac(pi,2), x, -frac(pi,2) <= x < pi, b x, x >= pi)]]\n에 대하여 <보기>에서 옳은 것만을 있는 대로 고른 것은?\n(단, [[a]], [[b]]는 실수이다.)\n<보기>\nㄱ. [[lim(x, -frac(pi,2), g(x), -) = 0]]\nㄴ. [[a = 2]]이면 합성함수 [[app(comp(f, g), x)]]는 [[x = -frac(pi,2)]]에서 연속이다.\nㄷ. [[a]]의 값에 관계없이 합성 함수 [[app(comp(f, g), x)]]가 [[x = pi]]에서 연속이면 [[b = 2n - 1]] ([[n]]은 정수)이다.",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2015년 3월 고3 이과 21번/4점]. 3구간 경우 나눔을 cases로, (f∘g)(x)를 app(comp(f, g), x)로. 답 ③ 유지")

# 72. 77b20513 — p94: cases
add(id="77b20513", qtype="short",
    question="함수 [[f(x) = cases(a sin(x) + (b + 1) cos(x) - 1, x >= 0, pow(e, 4x + 1), x < 0)]]이 모든 실수 [[x]]에서 미분가능할 때, 상수 [[a]], [[b]]에 대하여 [[frac(a,b)]]의 값을 구하시오.",
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 4 유지")

# 73. e3ee7eb2 — p95: cases
add(id="e3ee7eb2", qtype="short",
    question="함수 [[f(x) = cases(a cos(x) + b sin(x), x >= 0, pow(e, x), x < 0)]]이 [[x = 0]]에서 미분가능하도록 하는 상수 [[a]], [[b]]의 합 [[a + b]]의 값을 구하여라.",
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 2 유지")

# 74. 6a637d39 — p97: cases
add(id="6a637d39", qtype="choice",
    question="함수 [[f(x) = cases(2 pow(x,2) + a x + b, x < 0, sin(x), x >= 0)]]이 [[x = 0]]에서 미분가능하도록 하는 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 ① 유지")

# 75. ee4c0863 — 방정식과 부등식에의 활용 p81: f′(x) = (□(가)) × e^(−x²) → app + box(1); 문장 속 '(나)'는 텍스트
add(id="ee4c0863", qtype="choice",
    question="다음은 모든 실수 [[x]]에 대하여 [[2x - 1 >= k pow(e, pow(x,2))]]을 성립시키는 실수 [[k]]의 최댓값을 구하는 과정이다.\n[[f(x) = (2x - 1) pow(e, -pow(x,2))]]이라 하자.\n[[app(prime(f), x) = (box(1)) × pow(e, -pow(x,2))]]\n[[app(prime(f), x) = 0]]에서 [[x = -frac(1,2)]] 또는 [[x = 1]]\n함수 [[f(x)]]의 증가와 감소를 조사하면 함수 [[f(x)]]의 극솟값은 (나) 이다.\n또한 [[lim(x, inf, f(x)) = 0]], [[lim(x, -inf, f(x)) = 0]]이므로 함수 [[y = f(x)]]의 그래프의 개형을 그리면 함수 [[f(x)]]의 최솟값은 (나) 이다.\n따라서 [[2x - 1 >= k pow(e, pow(x,2))]]을 성립시키는 실수 [[k]]의 최댓값은 (나) 이다.\n위의 (가)에 알맞은 식을 [[g(x)]], (나)에 알맞은 수를 [[p]]라 할 때, [[g(2) × p]]의 값은?",
    choices=["[[frac(10, e)]]", "[[frac(15, e)]]", "[[frac(20, root(4, e))]]", "[[frac(25, root(4, e))]]", "[[frac(30, root(4, e))]]"],
    figure=None, confidence=0.85,
    note="[2016년 4월 고3 이과 14번/4점]. f′(x)를 app(prime(f), x)로, 식 속 빈칸 (가)를 box(1)로 한 식에(문장 속 '(나)'는 텍스트). 답 ③ 유지")

# 76. fcb5aed9 — p84
add(id="fcb5aed9", qtype="choice",
    question="다음은 모든 실수 [[x]]에 대하여 [[3x + frac(3,2) >= k pow(e, pow(x,2))]]을 성립시키는 실수 [[k]]의 최댓값을 구하는 과정이다.\n[[f(x) = (3x + frac(3,2)) pow(e, -pow(x,2))]]이라 하자.\n[[app(prime(f), x) = (box(1)) × pow(e, -pow(x,2))]]\n[[app(prime(f), x) = 0]]에서 [[x = -1]] 또는 [[x = frac(1,2)]]\n함수 [[f(x)]]의 증가와 감소를 조사하면 함수 [[f(x)]]의 극솟값은 (나) 이다.\n또한, [[lim(x, inf, f(x)) = 0]], [[lim(x, -inf, f(x)) = 0]]이므로 함수 [[y = f(x)]]의 그래프의 개형을 그리면 함수 [[f(x)]]의 최솟값은 (나) 이다.\n따라서 [[3x + frac(3,2) >= k pow(e, pow(x,2))]]을 성립시키는 실수 [[k]]의 최댓값은 (나) 이다.\n위의 (가)에 알맞은 식을 [[g(x)]], (나)에 알맞은 수를 [[p]]라 할 때, [[g(3) × p]]의 값은?",
    choices=["[[frac(30, e)]]", "[[frac(90, e)]]", "[[frac(30, root(4, e))]]", "[[frac(60, root(4, e))]]", "[[frac(90, root(4, e))]]"],
    figure=None, confidence=0.85,
    note="[2016년 4월 고3 이과 14번 변형]. f′(x)를 app(prime(f), x)로, 식 속 빈칸 (가)를 box(1)로(원문 '·'는 ×, 문장 속 '(나)'는 텍스트). 답 ② 유지(빠른정답 3과 불일치는 1차와 동일)")

# 77. 8fad3145 — p91: f′(x) 등식·부등식 → app
add(id="8fad3145", qtype="choice",
    question="다음은 [[n]]이 자연수이고 [[x > 1]]일 때, 부등식 [[pow(x, n + 1) + n > (n + 1) x]]가 성립하는 과정을 나타낸 것이다.\n[[f(x) = pow(x, n + 1) + n - (n + 1) x]]라 하면\n[[app(prime(f), x) = (n + 1) pow(x, n) - (n + 1) = (n + 1)(pow(x, n) - 1)]]\n[[n]]은 자연수이고 [[x > 1]]일 때, [[app(prime(f), x) > 0]]이므로 [[x > 1]]에서 함수 [[y = f(x)]]는 (가) 한다.\n이때 (나) = 0이므로 [[x > 1]]에서 (다) 이다.\n따라서 [[x > 1]]일 때,\n부등식 [[pow(x, n + 1) + n > (n + 1) x]]가 성립한다.\n위의 증명 과정 중 (가), (나), (다)에 알맞은 것을 차례로 적은 것으로 옳은 것은?",
    choices=["감소, [[f(1)]], [[f(x) < 0]]", "감소, [[f(0)]], [[f(x) < 0]]", "증가, [[f(1)]], [[f(x) > 0]]", "증가, [[f(0)]], [[f(x) > 0]]", "증가, [[f(1)]], [[f(x) < 0]]"],
    figure=None, confidence=0.85,
    note="f′(x)를 app(prime(f), x)로(빈칸 (가)(나)(다)는 문장 속이라 텍스트). 답 ③ 유지")

# 78. f2d2fc0a — p92: f′(x)=n{(가)^{n−1}−(x+1)^{n−1}} → app + pow(box(1), n-1); x=(나)→x = box(2); f((나))→f(box(2)); x=(라)→x = box(4)
add(id="f2d2fc0a", qtype="choice",
    question="다음은 [[a > 0]], [[b > 0]]이고, [[n]]이 2 이상의 자연수일 때 [[pow(a + b, n) <= pow(2, n - 1)(pow(a, n) + pow(b, n))]]임을 증명한 것이다.\n[[f(x) = pow(2, n - 1)(pow(x, n) + 1) - pow(x + 1, n)]]이라 하면\n[[app(prime(f), x) = n(pow(box(1), n - 1) - pow(x + 1, n - 1))]]\n이때 [[app(prime(f), x) = 0]]에서 [[x = box(2)]]이고,\n[[f(x)]]는 [[x = box(2)]]에서 (다) 이며 최소이다.\n따라서 함수 [[f(x)]]의 최솟값은\n[[f(box(2)) = pow(2, n - 1) × 2 - pow(2, n) = 0]]\n∴ [[f(x) >= 0]] (단, 등호는 [[x = 1]]일 때 성립)\n즉, [[pow(x + 1, n) <= pow(2, n - 1)(pow(x, n) + 1)]]\n위의 부등식에 [[x = box(4)]]를 대입하면 주어진 부등식을 얻는다.\n위의 과정에서 (가), (나), (다), (라)에 알맞은 것을 차례로 적은 것은?",
    choices=["[[x]], [[1]], 극소, [[a b]]", "[[x]], [[2]], 극대, [[a + b]]", "[[2x]], [[1]], 극소, [[frac(a,b)]]", "[[2x]], [[1]], 극대, [[frac(b,a)]]", "[[2x]], [[2]], 극소, [[frac(a,b)]]"],
    figure=None, confidence=0.85,
    note="f′(x)를 app(prime(f), x)로, 식 속 빈칸 (가)(나)(라)를 box(1)·box(2)·box(4)로(원문 중괄호는 괄호, '·'는 ×; 문장 속 '(다)'는 텍스트). 선지는 원문 (가)(나)(다)(라) 열 표를 콤마 나열로. 답 ③ 유지(빠른정답 neg(4)와 불일치는 1차와 동일)")
