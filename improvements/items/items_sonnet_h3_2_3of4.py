# -*- coding: utf-8 -*-
# esc_sonnet_h3-2_3of4 — 이미지 기준 전사 (81 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def UNS(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]

# ───────────────────────── 등비수열의 극한 ─────────────────────────
add(id="8dcc42af", qtype="choice",
    question=("그림은 함수 [[f(x) = 1 - abs(2x - 1)]] ([[0 <= x <= 1]])의 그래프이다.\n"
              "자연수 [[n]]에 대하여 집합 [[sub(A,n)]]을\n"
              "[[sub(A,n)]] = { [[x]] | [[pow(f,n)]]([[x]]) = 0, [[0 <= x <= 1]] }이라 할 때, 집합 [[sub(A,n)]]의 원소의 개수를 [[sub(a,n)]]이라 하자.\n"
              "예를 들어 [[sub(A,1) = set(0, 1)]], [[sub(A,2) = set(0, frac(1,2), 1)]]이므로 [[sub(a,1) = 2]], [[sub(a,2) = 3]]이다. "
              "이때 [[lim(n, inf, frac(sub(a,n) sub(a,n+1), pow(4,n)))]]의 값은?\n"
              "(단, [[pow(f,1) = f]], [[pow(f,n+1) = comp(f, pow(f,n))]] ([[n]] = 1, 2, 3, ⋯)이다.)"),
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]"],
    derived_answer="②",
    figure=UNS("좌표평면: y=f(x) 꺾은선 그래프, (0,0)-(1/2,1)-(1,0), 점선으로 x=1/2, y=1, x=1 표시"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프 / 합성 반복 fⁿ(x) 적용 표기 문법 밖",
    note="aₙ=2^(n-1)+1 → aₙaₙ₊₁/4ⁿ → 1/2 → ②.")

add(id="163e7d8c", qtype="choice",
    question=("그림과 같이 크기가 [[deg(60)]]인 [[angle(AOB)]]의 이등분선 위에 OC₁ = 4인 점 C₁을 잡아 점 C₁을 중심으로 하고 "
              "반직선 OA와 OB에 접하는 원 C₁을 그릴 때, 원 C₁과 반직선 OA, OB와의 접점을 각각 P₁, Q₁이라 하자.\n"
              "점 C₁을 지나고 반직선 OA와 OB에 접하는 두 원 중에서 큰 원의 중심을 C₂, 원 C₂와 반직선 OA, OB와의 접점을 각각 P₂, Q₂라 하고, "
              "원 C₁과 원 C₂가 만나는 점을 각각 A₁, B₁이라 할 때, 사각형 A₁C₁B₁C₂의 넓이를 [[sub(S,1)]]이라 하자.\n"
              "점 C₂를 지나고 반직선 OA와 OB에 접하는 두 원 중에서 큰 원의 중심을 C₃, 원 C₃과 반직선 OA, OB와의 접점을 각각 P₃, Q₃이라 하고, "
              "원 C₂와 원 C₃이 만나는 점을 각각 A₂, B₂라 할 때, 사각형 A₂C₂B₂C₃의 넓이를 [[sub(S,2)]]라 하자.\n"
              "이와 같은 과정을 계속하여 [[n]]번째 얻은 도형의 넓이를 [[sub(S,n)]]이라 할 때, [[lim(n, inf, frac(sub(S,n), pow(4,n) + pow(2,n)))]]의 값은?"),
    choices=["[[frac(sqrt(5),8)]]", "[[frac(sqrt(5),4)]]", "[[frac(sqrt(15),8)]]", "[[frac(sqrt(15),4)]]", "[[frac(sqrt(15),2)]]"],
    derived_answer="⑤",
    figure=UNS("각 AOB(60°)의 이등분선 위 중심 C₁,C₂,C₃의 세 원(반직선 OA·OB에 접함), 접점 P₁~P₃·Q₁~Q₃, 교점 A₁,B₁,A₂,B₂, 사각형 A₁C₁B₁C₂·A₂C₂B₂C₃ 음영"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원 3개+반직선 복합 도형 / 첨자 점 라벨(C₁, P₁ 등)·선분 윗줄(OC₁) 텍스트 처리",
    note="r₁=2, C₂: OC₂=8, r₂=4(닮음비 2), S₁=2√15 → Sₙ=2√15·4^(n-1) → 극한 √15/2 → ⑤.")

add(id="28f215d6", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 8인 정삼각형 ABC와 점 A를 지나고 직선 BC와 평행한 직선 [[l]]이 있다. "
              "자연수 [[n]]에 대하여 중심 Oₙ이 변 AC 위에 있고 반지름의 길이가 [[2 sqrt(3) × pow(frac(1,5), n - 1)]]인 원이 직선 AB와 직선 [[l]]에 모두 접한다. "
              "이 원과 직선 AB가 접하는 점을 Pₙ, 직선 OₙPₙ과 직선 [[l]]이 만나는 점을 Qₙ이라 하자.\n"
              "삼각형 BOₙQₙ의 넓이를 [[sub(S,n)]]이라 하면, [[lim(n, inf, pow(5, n - 1) sub(S,n)) = k]]이다. 이때 [[pow(k,2)]]의 값을 구하시오."),
    choices=None, derived_answer="768",
    figure=UNS("정삼각형 ABC, A를 지나는 수평선 l, 변 AC 위 중심 Oₙ의 원(AB·l에 접함), 접점 Pₙ, l 위의 점 Qₙ, 선분 BOₙ·BQₙ"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형+원+직선 복합 도형 / 첨자 점 라벨(Oₙ, Pₙ, Qₙ) 텍스트 처리",
    note="AOₙ=dₙ=4(1/5)^(n-1), Sₙ=4√3dₙ-√3dₙ²/4 → 5^(n-1)Sₙ→16√3=k, k²=768. 빠른정답 2와 불일치.")

add(id="687fbe1b", qtype="short",
    question=("자연수 [[m]]에 대하여 크기가 같은 정육면체 모양의 블록이 1에 1개, 2열에 2개, 3열에 3개, ⋯, [[m]]열에 [[m]]개 쌓여 있다. "
              "블록의 개수가 짝수인 열이 남아 있지 않을 때까지 다음 시행을 반복한다.\n"
              "블록의 개수가 짝수인 각 열에 대하여 그 열에 있는 블록의 개수의 [[frac(1,2)]]만큼의 블록을 그 열에서 들어낸다.\n"
              "블록을 들어내는 시행을 모두 마쳤을 때, 1열부터 [[m]]열까지 남아 있는 블록의 개수의 합을 [[f(m)]]이라 하자. "
              "예를 들어, [[f(2) = 2]], [[f(3) = 5]], [[f(4) = 6]]이다.\n"
              "[[lim(n, inf, frac(f(pow(2, n+1)) - f(pow(2,n)), f(pow(2, n+2)))) = frac(q,p)]]\n"
              "일 때, [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="19",
    figure=UNS("정육면체 블록 삽화: 1열 1개, 2열 1개, 3열 3개, 4열 1개, 5열 5개, 6열 3개, ⋯"),
    difficulty_est=4, confidence=0.85,
    note="출처 [2010년 11월 고3 이과 25번]. 원문 '1 에 1 개'(열 누락 오타) 그대로. f(m)=최대 홀수 약수 합, f(2ⁿ)=(4ⁿ+2)/3 → 극한 3/16 → 19.")

add(id="83fc8116", qtype="short",
    question=("자연수 [[n]]에 대하여 [[angle(A) = deg(45)]], ABₙ = [[pow(2,n)]], ACₙ = [[pow(2, n+1)]]인 삼각형 ABₙCₙ의 넓이를 [[sub(S,n)]], "
              "변 BₙCₙ의 길이를 [[sub(a,n)]]이라 할 때,\n"
              "[[lim(n, inf, pow(frac(sub(a,n) + sub(S,n), sub(a,2n)), 2)) = p + q sqrt(2)]]이다. 두 유리수 [[p]], [[q]]에 대하여 [[34(p + q)]]의 값을 구하시오."),
    choices=None, derived_answer="7",
    figure=UNS("삼각형 ABₙCₙ: ∠A=45°, ABₙ=2ⁿ, ACₙ=2^(n+1), BₙCₙ=aₙ 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 도형 / 첨자 점 라벨(Bₙ, Cₙ)·선분 윗줄 텍스트 처리",
    note="Sₙ=2^(2n)√2/2, aₙ²=4ⁿ(5-2√2) → 극한 (5+2√2)/34 → 34(p+q)=7.")

add(id="6f2fd7eb", qtype="choice",
    question=("자연수 [[n]]에 대하여\n[[seg(AB) = 3n - 1]], [[seg(AC) = 3n + 2]], [[angle(BAC) = frac(pi,6)]]인 삼각형 ABC가 있다. "
              "삼각형 ABC의 넓이를 [[sub(S,n)]]이라 할 때, [[sum(n, 1, inf, frac(3, 4 sub(S,n)))]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[1]]", "[[frac(3,2)]]", "[[2]]", "[[frac(5,2)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="Sₙ=(3n-1)(3n+2)/4 → 3/(4Sₙ)=1/(3n-1)-1/(3n+2) → 합 1/2 → ①. 빠른정답 7과 불일치(정렬 어긋남).")

# ───────────────────────── 함수의 몫의 미분법 ─────────────────────────
add(id="d409a1d5", qtype="choice",
    question=("1보다 큰 실수 [[t]]에 대하여 다음 그림과 같이 점 [[P(2t + frac(1,2t), 0)]]에서 원 [[pow(x,2) + pow(y,2) = frac(1, 4 pow(t,2))]]에 접선을 그었을 때, "
              "원과 접선이 제1사분면에서 만나는 점을 Q, 원 위의 점 [[point(0, -frac(1,2t))]]을 R라 하자.\n"
              "[[seg(OP) × seg(OQ)]]를 [[f(t)]]라 할 때, [[prime(f)(2)]]의 값은?"),
    choices=["[[-1]]", "[[-frac(1,2)]]", "[[-frac(1,4)]]", "[[-frac(1,8)]]", "[[-frac(1,16)]]"],
    derived_answer="⑤",
    figure=UNS("좌표평면: 원점 중심 원, x축 위 점 P에서 원에 그은 접선, 접점 Q(제1사분면), 원 위 점 R(y축 아래), 선분 QR"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 원+접선 도형 / f′(2) 도함수 적용 표기 prime(f)(2)",
    note="출처 [2015년 4월 고3 이과 13번 변형]. f(t)=(2t+1/(2t))·1/(2t)=1+1/(4t²), f′(2)=-1/16 → ⑤.")

add(id="f1a15edf", qtype="short",
    question=("함수 [[f(x) = frac(2,x) + frac(2,pow(x,2)) + frac(2,pow(x,3))]] + ⋯ + [[frac(2,pow(x,10))]]에 대하여\n"
              "[[lim(x, 0, frac(f(1 + 2x) - f(1 - 3x), x))]]의 값을 구하시오."),
    choices=None, derived_answer="-550", figure=None, difficulty_est=2, confidence=0.9,
    note="극한 = 5f′(1) = 5·(-2·55) = -550.")

add(id="26fab94c", qtype="short",
    question=("함수 [[f(x) = frac(1,x) + frac(2,pow(x,2)) + frac(3,pow(x,3))]] + ⋯ + [[frac(7,pow(x,7))]]에 대하여\n"
              "[[prime(f)(1)]]의 값을 구하시오."),
    choices=None, derived_answer="-140", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="f′(1) 도함수 적용 표기 prime(f)(1)",
    note="f′(1)=-(1²+2²+⋯+7²)=-140. 빠른정답 -550과 불일치(정렬 어긋남).")

add(id="d4af49cf", qtype="short",
    question=("함수 [[f(x) = frac(10,x) + frac(9,pow(x,2)) + frac(8,pow(x,3))]] + ⋯ + [[frac(1,pow(x,10))]]에 대하여\n"
              "[[prime(f)(1)]]의 값을 구하시오."),
    choices=None, derived_answer="-220", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="f′(1) 도함수 적용 표기 prime(f)(1)",
    note="f′(1)=-Σk(11-k)=-220.")

add(id="84863d5c", qtype="choice",
    question=("함수 [[f(x) = frac(1,x) + frac(1,pow(x,2)) + frac(1,pow(x,3))]] + ⋯ + [[frac(1,pow(x,10))]]에 대하여\n"
              "[[prime(f)(1)]]의 값은?"),
    choices=["[[-55]]", "[[-50]]", "[[-40]]", "[[55]]", "[[65]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="f′(1) 도함수 적용 표기 prime(f)(1)",
    note="f′(1)=-(1+2+⋯+10)=-55 → ①. 빠른정답 -140과 불일치(정렬 어긋남).")

add(id="0a0e003a", qtype="short",
    question=("함수\n[[f(x) = 1 + pow(2, -2 log(2,x)) + pow(2, -4 log(2,x))]] + ⋯ + [[pow(2, -2n log(2,x))]] + ⋯\n"
              "에 대하여 [[-9 prime(f)(2)]]의 값을 구하시오. (단, [[x > 1]])"),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="f′(2) 도함수 적용 표기 prime(f)(2)",
    note="f(x)=x²/(x²-1), f′(x)=-2x/(x²-1)², f′(2)=-4/9 → 4.")

add(id="dd37d5d6", qtype="short",
    question=("[[f(x) = 1 + pow(3, -log(3,x)) + pow(3, -2 log(3,x))]] + ⋯ + [[pow(3, -n log(3,x))]] + ⋯\n"
              "에 대하여 [[abs(frac(1, prime(f)(3)))]]의 값을 구하시오. (단, [[x > 1]])"),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.75,
    needs_review="이미지 상단 잘림 가능(첫 줄이 '함수' 머리말 없이 f(x)=로 시작) / f′(3) 도함수 적용 표기",
    note="f(x)=x/(x-1), f′(3)=-1/4 → |1/f′(3)|=4.")

add(id="281d906d", qtype="choice",
    question=("다음 그림과 같이 [[seg(BC) = 2]], [[angle(ABC) = frac(pi,2)]], [[angle(ACB) = 2 theta]]인 삼각형 ABC에 내접하는 원의 반지름의 길이를 [[r(theta)]]라 하자. "
              "[[h(theta) = frac(r(theta), tan(theta))]]일 때, [[prime(h)(frac(pi,6))]]의 값은? (단, [[0 < theta < frac(pi,4)]])"),
    choices=["[[2 sqrt(3) - 8]]", "[[2 sqrt(3) - 4]]", "[[4 sqrt(3) - 8]]", "[[4 sqrt(3) - 4]]", "[[4 sqrt(3)]]"],
    derived_answer="③",
    figure=UNS("직각삼각형 ABC(∠B 직각, BC=2, ∠C=2θ)와 내접원(중심 O, 반지름 r(θ))"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+내접원 / h′(π/6) 도함수 적용 표기",
    note="출처 [2017년 10월 고3 이과 12번 변형]. h(θ)=2/(1+tanθ), h′(π/6)=4√3-8 → ③.")

add(id="3ee5423d", qtype="short",
    question=("다음 그림과 같이 [[seg(BC) = 2]], [[angle(ABC) = theta]], [[angle(ACB) = frac(pi,3)]]인 삼각형의 한 꼭짓점 A에서 선분 [[seg(BC)]]에 내린 수선의 길이를 [[f(theta)]]라 할 때, "
              "[[prime(f)(frac(pi,3))]]의 값을 구하시오.\n(단, [[0 < theta < frac(pi,2)]])"),
    choices=None, derived_answer="2",
    figure=UNS("삼각형 ABC(BC=2, ∠B=θ, ∠C=π/3), A에서 BC에 내린 수선 AH=f(θ)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+수선 도형 / f′(π/3) 도함수 적용 표기",
    note="f(θ)=2√3tanθ/(√3+tanθ), f′(π/3)=2.")

add(id="63202c07", qtype="choice",
    question=("그림과 같이 [[seg(BC) = 1]], [[angle(ABC) = frac(pi,3)]], [[angle(ACB) = 2 theta]]인 삼각형 ABC에 내접하는 원의 반지름의 길이를 [[r(theta)]]라 하자. "
              "[[h(theta) = frac(r(theta), tan(theta))]]일 때, [[prime(h)(frac(pi,6))]]의 값은?\n(단, [[0 < theta < frac(pi,3)]])"),
    choices=["[[-sqrt(3)]]", "[[-frac(sqrt(3),3)]]", "[[frac(sqrt(3),6)]]", "[[frac(sqrt(3),3)]]", "[[sqrt(3)]]"],
    derived_answer="②",
    figure=UNS("삼각형 ABC(BC=1, ∠B=π/3, ∠C=2θ)와 내접원(반지름 r(θ))"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+내접원 / h′(π/6) 도함수 적용 표기",
    note="출처 [2017년 10월 고3 이과 12번/3점]. h(θ)=1/(√3tanθ+1), h′(π/6)=-√3/3 → ②.")

add(id="55e9bba0", qtype="choice",
    question=("다음 그림과 같이 [[seg(BC) = 3]], [[angle(ABC) = frac(pi,6)]], [[angle(ACB) = 2 theta]]인 삼각형 ABC에 내접하는 원의 반지름의 길이를 [[r(theta)]]라 하자.\n"
              "[[h(theta) = frac(r(theta), tan(theta))]]일 때, [[prime(h)(frac(pi,4))]]의 값은?\n"
              "(단, [[0 < theta < frac(pi,2)]]이고, [[tan(frac(pi,12)) = 0.25]]로 계산한다.)"),
    choices=["[[-frac(24,25)]]", "[[-frac(12,25)]]", "[[0]]", "[[frac(12,25)]]", "[[frac(24,25)]]"],
    derived_answer="①",
    figure=UNS("삼각형 ABC(BC=3, ∠B=π/6, ∠C=2θ)와 내접원(반지름 r(θ))"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+내접원 / h′(π/4) 도함수 적용 표기",
    note="h(θ)=3/(4tanθ+1), h′(π/4)=-24/25 → ①.")

add(id="ca9b028e", qtype="short",
    question=("함수 [[f(x)]] = { [[4 pow(e,x) + a x + b]] ([[x >= 0]]) ; [[2 tan(x)]] ([[x < 0]]) }가 [[x = 0]]에서 미분가능할 때, "
              "상수 [[a]], [[b]]에 대하여 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="조각적(경우 나눔) 정의 f(x) 문법 밖",
    note="연속 b=-4, 미분가능 a+4=2 → a=-2 → ab=8.")

add(id="0ad0e62a", qtype="choice",
    question=("다음 그림과 같이 점 O를 중심으로 하고 반지름의 길이가 4, [[angle(AOB) = frac(pi,2)]]인 부채꼴 OAB의 호 AB 위에 [[angle(POA) = x]] ([[0 < x < frac(pi,2)]])인 점 P를 잡는다. "
              "중심이 선분 OB 위에 있고 점 B를 지나며 선분 OP에 접하는 원의 반지름의 길이를 [[f(x)]]라 할 때, [[frac(1, prime(f)(frac(pi,3)))]]의 값은?"),
    choices=["[[-frac(sqrt(3),4)]]", "[[-frac(3 sqrt(3),8)]]", "[[-frac(sqrt(3),2)]]", "[[-frac(5 sqrt(3),8)]]", "[[-frac(3 sqrt(3),4)]]"],
    derived_answer="②",
    figure=UNS("사분원 OAB(반지름 4), 호 위 점 P(∠POA=x), OB 위 중심으로 B를 지나고 OP에 접하는 원"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 부채꼴+원 도형 / f′(π/3) 도함수 적용 표기",
    note="f(x)=4cosx/(1+cosx), f′(x)=-4sinx/(1+cosx)², f′(π/3)=-8√3/9 → 1/f′=-3√3/8 → ②. 빠른정답 4와 불일치.")

add(id="c438667b", qtype="choice",
    question=("실수 전체의 집합에서 미분가능한 함수 [[f(x)]]에 대하여 함수 [[g(x)]]를 [[g(x) = frac(f(x) cos(2x), pow(e,x))]]라 하자.\n"
              "[[prime(g)(pi) = pow(e,pi) g(pi)]]일 때, [[frac(prime(f)(pi), f(pi))]]의 값은? (단, [[f(pi) != 0]])"),
    choices=["[[pow(e, -2 pi)]]", "[[1]]", "[[pow(e, -pi) + 1]]", "[[pow(e,pi) + 1]]", "[[pow(e, 2 pi)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.75,
    needs_review="이미지에 문항 2개 인쇄(상단: BC=2, ∠B=π/3, ∠C=2θ 내접원 h′(π/6) 문항 + 하단: g(x) 문항), id 1개 → draft_a 대응대로 하단 문항 전사 / g′(π), f′(π) 도함수 적용 표기",
    note="g′(π)=(f′(π)-f(π))e^(-π)=e^π·f(π)e^(-π) → f′(π)/f(π)=e^π+1 → ④. 빠른정답 240은 두 문항 어느 쪽에도 해당 없음.")

# ───────────────────────── 접선의 방정식 ─────────────────────────
add(id="1b1e0df2", qtype="choice",
    question=("실수 [[t]] ([[0 < t < pi]])에 대하여 곡선 [[y = sin(x)]] 위의 점 [[P(t, sin(t))]]에서의 접선과 점 P를 지나고 기울기가 1인 직선이 이루는 예각의 크기를 [[theta]]라 할 때, "
              "[[lim(t, 0, frac(tan(theta), pow(t,2)), +)]]의 값은?"),
    choices=["[[frac(1,16)]]", "[[frac(1,8)]]", "[[frac(1,4)]]", "[[frac(1,2)]]", "[[1]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="tanθ=(1-cost)/(1+cost) → tanθ/t² → 1/4 → ③.")

add(id="c41fbac5", qtype="choice",
    question=("곡선 [[y = ln(x - 3) + 1]] 위의 점 [[point(4, 1)]]에서의 접선의 방정식이 [[y = a x + b]]일 때,\n"
              "두 상수 [[a]], [[b]]의 합 [[a + b]]의 값은?"),
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2016년 6월 고3 이과 11번/3점]. 기울기 1, y=x-3 → a+b=-2 → ①. 빠른정답 5와 불일치.")

add(id="e4231cff", qtype="choice",
    question=("[[a > 2]]인 상수 [[a]]에 대하여 두 곡선 [[y = pow(a, x - 1)]]과 [[y = pow(2,x)]]이 점 P에서 만난다. 점 P의 [[x]]좌표를 [[k]]라 하자.\n"
              "점 P에서 곡선 [[y = pow(2,x)]]에 접하는 직선이 [[x]]축과 만나는 점을 A, 점 P에서 곡선 [[y = pow(a, x - 1)]]에 접하는 직선이 [[x]]축과 만나는 점을 B라 하자. "
              "점 [[H(k, 0)]]에 대하여 [[seg(AH) = 3 seg(BH)]]일 때, [[a]]의 값은?"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="③",
    figure=UNS("좌표평면: 두 지수함수 y=a^(x-1), y=2^x 그래프와 교점 P, P에서 x축에 내린 점선(x=k)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 지수함수 그래프 2개",
    note="AH=1/ln2, BH=1/lna → lna=3ln2 → a=8 → ③.")

add(id="ec0ea30d", qtype="choice",
    question=("곡선 [[y = 2 cos(x)]] 위의 점 [[point(frac(pi,3), 1)]]을 지나고\n이 점에서의 접선과 수직인 직선의 방정식이\n"
              "[[y = a x + b]]일 때, 상수 [[a]], [[b]]에 대하여 [[a + frac(3,pi) b]]의 값은?"),
    choices=["[[-pi]]", "[[-frac(3,pi)]]", "[[-frac(2,pi)]]", "[[frac(2,pi)]]", "[[frac(3,pi)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="접선 기울기 -√3, 수직선 y=(1/√3)(x-π/3)+1 → a+(3/π)b=3/π → ⑤. 빠른정답 1과 불일치.")

add(id="3313274c", qtype="choice",
    question=("양수 [[t]]에 대하여 구간 [[itv(1, inf, co)]]에서 정의된 함수 [[f(x)]]가\n"
              "[[f(x)]] = { [[ln(x)]] ([[1 <= x < e]]) ; [[-t + ln(x)]] ([[x >= e]]) }\n"
              "일 때, 다음 조건을 만족시키는 일차함수 [[g(x)]] 중에서 직선 [[y = g(x)]]의 기울기의 최솟값을 [[h(t)]]라 하자.\n"
              "1 이상의 모든 실수 [[x]]에 대하여 [[(x - e)(g(x) - f(x)) >= 0]]이다.\n"
              "미분가능한 함수 [[h(t)]]에 대하여 양수 [[a]]가 [[h(a) = frac(1, e + 2)]]을 만족한다. [[prime(h)(frac(1,2e)) × prime(h)(a)]]의 값은?"),
    choices=["[[frac(1, pow(e + 1, 2))]]", "[[frac(1, e(e + 1))]]", "[[frac(1, pow(e,2))]]", "[[frac(1, (e - 1)(e + 1))]]", "[[frac(1, e(e - 1))]]"],
    derived_answer=None, figure=None, difficulty_est=5, confidence=0.75,
    needs_review="조각적 정의 f(x) 문법 밖 / h′ 도함수 적용 표기 / 조건 상자 {…}는 괄호로 대체",
    note="출처 [2017년 11월 고3 이과 21번/4점]. 답 미도출.")

add(id="540eb24f", qtype="choice",
    question=("실수 [[k]]에 대하여 함수 [[f(x)]]는\n"
              "[[f(x)]] = { [[frac(2, 1 - x)]] ([[x < 1]]) ; [[-pow(x - 2, 2) + k]] ([[x >= 1]]) }이다. "
              "실수 [[t]]에 대하여 직선 [[y = x + t]]와 함수 [[y = f(x)]]의 그래프가 만나는 점의 개수를 [[g(t)]]라 하자. "
              "함수 [[g(t)]]가 [[t = a]]에서 불연속인 [[a]]의 값이 한 개일 때, [[k]]의 값은?"),
    choices=["[[sqrt(2) - frac(3,4)]]", "[[2 sqrt(2) - frac(3,4)]]", "[[sqrt(2) + frac(3,4)]]", "[[2 sqrt(2) + frac(3,4)]]", "[[3 sqrt(2) + frac(3,4)]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.75,
    needs_review="조각적 정의 f(x) 문법 밖",
    note="좌측 접선 t=2√2-1, 우측 접선 t=k-7/4·끝점 t=k-2; k-7/4=2√2-1일 때 불연속점 1개 → k=2√2+3/4 → ④. 빠른정답 49와 불일치.")

add(id="bc9c772e", qtype="choice",
    question=("매개변수 [[t]] ([[0 < t < pi]])로 나타낸\n곡선 [[x = t - 2 cos(t)]], [[y = -t + 2 sin(t)]] 위의\n점 [[point(a, -a)]]에서의 접선의 기울기는?"),
    choices=["[[1 - 2 sqrt(2)]]", "[[2 - 2 sqrt(2)]]", "[[3 - 2 sqrt(2)]]", "[[4 - 2 sqrt(2)]]", "[[5 - 2 sqrt(2)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="x+y=0 → t=π/4, dy/dx=(-1+2cost)/(1+2sint)=3-2√2 → ③.")

add(id="b799ea3b", qtype="choice",
    question=("매개변수 [[t]] ([[0 < t < pi]])로 나타내어진\n곡선 [[x = sin(t) - cos(t)]], [[y = 4 cos(t) + sin(t)]] 위의\n"
              "점 [[point(a, b)]]에서의 접선의 기울기가 6일 때, [[a + b]]의 값은?"),
    choices=["[[-frac(sqrt(5),2)]]", "[[-frac(3 sqrt(5),5)]]", "[[-frac(7 sqrt(5),10)]]", "[[-frac(4 sqrt(5),5)]]", "[[-frac(9 sqrt(5),10)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2022년 10월 고3 미적분 25번 변형]. tant=-1/2 → sint=1/√5, cost=-2/√5 → a+b=-4/√5 → ④. 빠른정답 2와 불일치.")

add(id="9035ca43", qtype="choice",
    question=("매개변수 [[t]]로 나타내어진 곡선 [[x = pow(e, 4t)(1 + pow(sin(pi t), 2))]],\n[[y = pow(e, 4t)(1 - 3 pow(cos(pi t), 2))]]를 [[C]]라 하자. "
              "곡선 [[C]]가 직선 [[y = 3x - 5e]]와 만나는 점을 P라 할 때, 곡선 [[C]] 위의 점 P에서의 접선의 기울기는?"),
    choices=["[[frac(3 pi - 4, pi + 4)]]", "[[frac(3 pi - 2, pi + 6)]]", "[[frac(3 pi, pi + 8)]]", "[[frac(3 pi + 2, pi + 10)]]", "[[frac(3 pi + 4, pi + 12)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2025년 11월 고3 미적분 27번/3점]. y-3x=-5e^(4t)=-5e → t=1/4, 기울기 (3π-2)/(π+6) → ②.")

# ───────────────────────── 지수함수와 로그함수의 극한과 미분 ─────────────────────────
add(id="e98dbe8d", qtype="choice",
    question=("[[a > 0]], [[b > 0]], [[a != 1]], [[b != 1]]일 때, 함수\n"
              "[[f(x) = frac(pow(b,x) + log(a, x), pow(a,x) + log(b, x))]]\n"
              "에 대하여 <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[1 < a < b]]이면 [[x > 1]]인 모든 [[x]]에 대하여 [[f(x) > 1]]이다.\n"
              "ㄴ. [[b < a < 1]]이면 [[lim(x, inf, f(x)) = 0]]이다.\n"
              "ㄷ. [[lim(x, 0, f(x), +) = log(a, b)]]"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2008년 9월 고3 이과 미분과 적분 29번]. ㄱ✓, ㄴ 극한 ln b/ln a≠0 ✗, ㄷ✓ → ③. 원문 x→+0 표기.")

add(id="2ba8a0a3", qtype="short",
    question=("함수 [[f(x)]]가\n[[f(x)]] = { [[pow(e,x)]] ([[x <= 0]], [[x >= 2]]) ; [[ln(x + 1)]] ([[0 < x < 2]]) }\n"
              "이고, 함수 [[y = g(x)]]의 그래프가 다음 그림과 같다.\n"
              "[[lim(x, 2, f(g(x)), -) + lim(x, 0, g(f(x)), -)]]의 값을 구하시오."),
    choices=None, derived_answer="1",
    figure=UNS("y=g(x) 그래프: x<0에서 원점(채운 점)으로 올라가는 곡선, 0<x<2에서 (0,2)(열린 점)~(2,0)(열린 점) 선분, x≥2에서 (2,2)(채운 점)부터 증가하는 곡선"),
    difficulty_est=3, confidence=0.75,
    needs_review="조각적 정의 f(x) 문법 밖 / 도형 표현 불가: g(x) 그래프",
    note="g(2-)=0+ → f→0, f(0-)→1- → g(1)=1 → 합 1. 빠른정답 3과 불일치.")

add(id="62aee887", qtype="choice",
    question=("함수 [[f(x)]]가\n[[f(x)]] = { [[pow(e,x)]] ([[x <= 0]], [[x >= 2]]) ; [[ln(x + 1)]] ([[0 < x < 2]]) }\n"
              "이고, 함수 [[y = g(x)]]의 그래프가 그림과 같다.\n"
              "[[lim(x, 2, f(g(x)), +) + lim(x, 0, g(f(x)), +)]]의 값은?"),
    choices=["[[e]]", "[[e + 1]]", "[[e + 2]]", "[[pow(e,2) + 1]]", "[[pow(e,2) + 2]]"],
    derived_answer="⑤",
    figure=UNS("y=g(x) 그래프: x<0에서 원점(채운 점)으로 올라가는 곡선, 0<x<2에서 (0,2)(열린 점)~(2,0)(열린 점) 선분, x≥2에서 (2,2)(채운 점)부터 증가하는 곡선"),
    difficulty_est=3, confidence=0.75,
    needs_review="조각적 정의 f(x) 문법 밖 / 도형 표현 불가: g(x) 그래프",
    note="출처 [2016년 3월 고3 이과 12번/3점]. g(2+)→2+ → f→e², f(0+)→0+ → g→2 → e²+2 → ⑤. 빠른정답 4와 불일치.")

dup(["6fba4468", "5e6c3377"], qtype="choice",
    question=("다음 보기 중 [[lim(x, inf, pow(1 + frac(a,x), frac(x,b)))]]과 값이 같은 것만을 있는 대로 고른 것은?\n"
              "(단, [[a]], [[b]]는 0이 아닌 상수이고 [[a != 1]], [[b != 1]]이다.)\n<보기>\n"
              "ㄱ. [[lim(x, inf, pow(1 - frac(a,x), -b x))]]\n"
              "ㄴ. [[lim(x, 0, pow(1 + a x, frac(b,x)))]]\n"
              "ㄷ. [[lim(x, 0, pow(1 - frac(x,b), -frac(a,x)))]]"),
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="주어진 극한 e^(a/b); ㄱ e^(ab), ㄴ e^(ab), ㄷ e^(a/b) → ㄷ만 → ②. 빠른정답 3과 불일치.")

add(id="986b7a50", qtype="choice",
    question=("함수 [[f(x)]] = { [[frac(pow(e, a x) - 1, 3x)]] ([[x < 0]]) ; [[pow(x,2) + 3x + 2]] ([[x >= 0]]) }이 실수 전체의 집합에서 연속일 때, "
              "상수 [[a]]의 값은? (단, [[a != 0]])"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="조각적 정의 f(x) 문법 밖",
    note="출처 [2017년 7월 고3 이과 6번/3점]. a/3=2 → a=6 → ①. 빠른정답 3과 불일치.")

add(id="a98e4dec", qtype="choice",
    question=("두 함수\n[[f(x)]] = { [[a x]] ([[x < 2]]) ; [[-4x + 10]] ([[x >= 2]]) }, [[g(x) = pow(3,x) + pow(3,-x)]]\n"
              "에 대하여 합성함수 ([[comp(g, f)]])([[x]])가 실수 전체의 집합에서 연속이 되도록 하는 모든 실수 [[a]]의 값의 합은?"),
    choices=["[[-1]]", "[[0]]", "[[1]]", "[[2]]", "[[3]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="조각적 정의 f(x) 문법 밖 / 합성함수 적용 (g∘f)(x) 표기",
    note="출처 [2015년 6월 고3 이과 16번 변형]. g(2a)=g(2) → a=±1 → 합 0 → ②. 빠른정답 1과 불일치.")

add(id="eca349ce", qtype="short",
    question=("두 함수\n[[f(x)]] = { [[a x]] ([[x < 1]]) ; [[4x - 3]] ([[x >= 1]]) }, [[g(x) = pow(2,x) - pow(2,-x)]]\n"
              "에 대하여 합성함수 ([[comp(g, f)]])([[x]])가 실수 전체의 집합에서 연속이 되도록 하는 실수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="조각적 정의 f(x) 문법 밖 / 합성함수 적용 (g∘f)(x) 표기",
    note="g 단조증가 → g(a)=g(1) → a=1.")

add(id="93fc789e", qtype="choice",
    question=("두 함수\n[[f(x)]] = { [[a x]] ([[x < 1]]) ; [[-3x + 4]] ([[x >= 1]]) }, [[g(x) = pow(2,x) + pow(2,-x)]]\n"
              "에 대하여 합성함수 ([[comp(g, f)]])([[x]])가 실수 전체의 집합에서 연속이 되도록 하는 모든 실수 [[a]]의 값의 곱은?"),
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="조각적 정의 f(x) 문법 밖 / 합성함수 적용 (g∘f)(x) 표기",
    note="출처 [2015년 6월 고3 이과 16번/4점]. g(a)=g(1) → a=±1 → 곱 -1 → ⑤.")

add(id="a9d37043", qtype="choice",
    question=("함수 [[f(x)]] = { [[frac(pow(e, a x) - 1, 4x)]] ([[x < 0]]) ; [[pow(x,2) + 2x - 1]] ([[x >= 0]]) }이 실수 전체의 집합에서 연속일 때, "
              "상수 [[a]]의 값은? (단, [[a != 0]])"),
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="조각적 정의 f(x) 문법 밖",
    note="출처 [2017년 7월 고3 이과 6번 변형]. a/4=-1 → a=-4 → ②. 빠른정답 1과 불일치.")

add(id="f74353ab", qtype="choice",
    question=("곡선 [[y = pow(e, 3x) - 1]] 위의 점 [[P(2t, pow(e, 6t) - 1)]] ([[t > 0]])에 대하여 [[seg(PQ) - seg(OQ) = 0]]를 만족시키는 [[x]]축 위의 점 Q의 [[x]]좌표를 [[f(t)]]라 할 때, "
              "[[lim(t, 0, frac(f(t), t), +)]]의 값은?\n(단, O는 원점이다.)"),
    choices=["[[10]]", "[[9]]", "[[8]]", "[[7]]", "[[6]]"],
    derived_answer="①",
    figure=UNS("좌표평면: 곡선 y=e^(3x)-1, 곡선 위 점 P, x축 위 점 Q, 선분 PQ"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 지수곡선+선분 도형",
    note="출처 [2024년 5월 고3 미적분 25번 변형]. f(t)=t+(e^(6t)-1)²/(4t) → f(t)/t→1+9=10 → ①.")

add(id="305a4f86", qtype="choice",
    question=("양수 [[t]]에 대하여 다음 조건을 만족시키는 실수 [[k]]의 값을 [[f(t)]]라 하자.\n"
              "직선 [[x = k]]와 두 곡선 [[y = pow(e, frac(x,3))]], [[y = pow(e, frac(x,3) + 4t)]]이 만나는 점을 각각 P, Q라하고, "
              "점 Q를 지나고 [[y]]축에 수직인 직선이 곡선 [[y = pow(e, frac(x,3))]]과 만나는 점을 R라 할 때, [[seg(PQ) = seg(QR)]]이다.\n"
              "함수 [[f(t)]]에 대하여 [[lim(t, 0, f(t), +)]]의 값은?"),
    choices=["[[ln(4)]]", "[[ln(8)]]", "[[ln(9)]]", "[[ln(25)]]", "[[ln(27)]]"],
    derived_answer="⑤",
    figure=UNS("좌표평면: 두 지수곡선 y=e^(x/3), y=e^(x/3+4t), 수직선 x=k, 교점 P·Q, Q를 지나는 수평선과 곡선의 교점 R"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 지수곡선 2개+직선 도형",
    note="e^(k/3)=12t/(e^(4t)-1)→3 → k→3ln3=ln27 → ⑤. 빠른정답 1과 불일치.")

add(id="bae28594", qtype="choice",
    question=("자연수 [[n]]에 대하여\n"
              "[[f(n)]] = lim ([[x]]→0) { [[pow(e, 4x) + pow(e, 8x) + pow(e, 12x)]] + ⋯ + [[pow(e, 4 n x) - n]] } / [[x]]\n"
              "일 때, [[sum(n, 1, inf, frac(1, f(n)))]]의 합은?"),
    choices=["[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]", "[[1]]", "[[2]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="줄임표(⋯)가 포함된 극한식 — lim 기호·분수를 텍스트 혼합으로 표기",
    note="f(n)=4(1+⋯+n)=2n(n+1) → Σ1/(2n(n+1))=1/2 → ③. 빠른정답 4와 불일치.")

add(id="33f31f31", qtype="choice",
    question=("함수 [[f(x) = pow(e, 4x) - 2 a x]] ([[a]]는 상수)와 상수 [[k]]에 대하여\n"
              "함수 [[g(x)]] = { [[f(x)]] ([[x >= k]]) ; [[-f(x)]] ([[x < k]]) }가 실수 전체의 집합에서 연속이고 역함수를 가질 때, [[a k]]의 값은?"),
    choices=["[[frac(e,4)]]", "[[frac(e,2)]]", "[[pow(e, frac(1,2))]]", "[[e]]", "[[pow(e,2)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.75,
    needs_review="조각적 정의 g(x) 문법 밖",
    note="출처 [2024년 10월 고3 미적분 27번 변형]. f(k)=0, f′(k)=0 → k=1/4, a=2e → ak=e/2 → ②. 빠른정답 5와 불일치.")

add(id="25d7c435", qtype="choice",
    question=("함수 [[f(x)]] = { [[(3x + 1) pow(e,x)]] ([[x <= 0]]) ; [[a x + 1]] ([[x > 0]]) }이\n"
              "[[x = 0]]에서 미분가능할 때, 상수 [[a]]의 값은?"),
    choices=["[[1]]", "[[4]]", "[[7]]", "[[10]]", "[[13]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="조각적 정의 f(x) 문법 밖",
    note="출처 [2016년 11월 고2 이과 8번/3점]. f′(0-)=3+1=4 → a=4 → ②. 빠른정답 3과 불일치.")

# ───────────────────────── 등비급수 ─────────────────────────
add(id="1d3c9879", qtype="short",
    question=("수열 [[set(sub(a,n))]]이 모든 자연수 [[n]]에 대하여\n[[sub(a,1) = 3]], [[sub(a, n+1) = frac(2,3) sub(a,n)]]\n"
              "을 만족시킬 때, [[sum(n, 1, inf, sub(a, 2n - 1)) = frac(q,p)]]이다. [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="32", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2017년 3월 고3 문과 26번/4점]. a_(2n-1)=3(4/9)^(n-1) → 합 27/5 → 32.")

add(id="9a86dd1a", qtype="choice",
    question=("첫째항이 1인 무한등비수열 [[set(sub(a,n))]]에 대하여\n"
              "[[sum(n, 1, inf, sub(a,n)) = 3]]일 때, [[sum(n, 1, inf, (sub(a, 3n - 2) - sub(a, 3n - 1)))]]의 값은?"),
    choices=["[[frac(7,19)]]", "[[frac(8,19)]]", "[[frac(9,19)]]", "[[frac(10,19)]]", "[[frac(11,19)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2011년 3월 고3 문과 12번/3점]. r=2/3, (1-r)/(1-r³)=9/19 → ③. 빠른정답 90과 불일치.")

add(id="b1ace96f", qtype="choice",
    question=("두 급수 [[sum(n, 1, inf, sub(a,n))]], [[sum(n, 1, inf, sub(b,n))]]에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 수열 [[set(sub(a,n))]]이 등비수열이고 급수 [[sum(n, 1, inf, pow(sub(a,n), 5))]]이 수렴하면 급수 [[sum(n, 1, inf, sub(a,n))]]도 수렴한다.\n"
              "ㄴ. 급수 [[sum(n, 1, inf, sub(a,n))]]이 수렴하면 [[sum(n, 1, inf, pow(5, sub(a,n)))]]도 수렴한다.\n"
              "ㄷ. [[sum(n, 1, inf, sub(a,n))]], [[sum(n, 1, inf, sub(b,n))]]이 각각 상수인 값 [[p]], [[q]]에 수렴하면 [[sum(n, 1, inf, frac(sub(a,n), sub(b,n))) = frac(p,q)]]이다. (단, [[q != 0]])"),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="ㄱ✓(|r|<1), ㄴ 5^(aₙ)→1≠0 ✗, ㄷ ✗ → ①.")

add(id="ed07ffed", qtype="short",
    question=("수열 [[set(sub(a,n))]]이\n[[2 sub(a,1) + pow(2,2) sub(a,2) + pow(2,3) sub(a,3)]] + ⋯ + [[pow(2,n) sub(a,n) = pow(3,n) - 1]]\n"
              "([[n]] = 1, 2, 3, ⋯)\n을 만족시킬 때, [[sum(n, 1, inf, frac(sub(a,n), pow(3, n - 1)))]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.9,
    note="2ⁿaₙ=2·3^(n-1) → aₙ/3^(n-1)=(1/2)^(n-1) → 합 2.")

add(id="bbbb37e5", qtype="choice",
    question=("순환소수로 이루어진 수열 [[set(sub(a,n))]]의 각 항이\n"
              "[[sub(a,1) = recdec(0,4)]], [[sub(a,2) = recdec(0,40)]], [[sub(a,3) = recdec(0,400)]], ⋯,\n"
              "[[sub(a,n)]] = 0.4̇00⋯00̇ (0이 ([[n - 1]])개), ⋯일 때, [[sum(n, 1, inf, (frac(1, sub(a, n+1)) - frac(1, sub(a,n))))]]의 값은?"),
    choices=["[[0]]", "[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="일반항 순환소수 0.4̇00⋯00̇(밑줄 (n-1)개) 표기 문법 밖 — 텍스트 처리",
    note="1/aₙ=(10ⁿ-1)/(4·10^(n-1)) → 차 9/(4·10ⁿ) → 합 1/4 → ②.")

add(id="cc08d583", qtype="choice",
    question=("원 [[pow(x,2) + pow(y,2) = frac(1, pow(2,n))]]에 대하여 기울기가 [[-1]]이고 제1사분면을 지나는 접선이 [[x]]축과 만나는 점의 좌표를 [[point(sub(a,n), 0)]]이라 할 때, "
              "[[sum(n, 1, inf, sub(a,n))]]의 값은?"),
    choices=["[[2]]", "[[2 + sqrt(2)]]", "[[2 sqrt(2)]]", "[[4]]", "[[4 + sqrt(2)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2004년 9월 고3 문과 10번]. aₙ=√2·(1/√2)ⁿ → 합 2+√2 → ②.")

add(id="59122624", qtype="short",
    question=("다음 그림과 같이 원점 O와 점 A₀[[point(10, 0)]]에 대하여 제1사분면 위에 OA₀를 한 변으로 하는 정삼각형 OA₀A₁을 만들고 A₀A₁을 [[ratio(1,2)]]로 내분하는 점을 B₁이라 한다. "
              "또 △OA₀A₁ 밖에 A₁B₁을 한 변으로 하는 정삼각형 A₁B₁A₂를 만들고 A₁A₂를 [[ratio(1,2)]]로 내분하는 점을 B₂라 한다. "
              "이와 같은 과정을 한없이 반복하면 점 Aₙ은 점 [[point(a, b)]]에 한없이 가까워진다. 이때 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="13",
    figure=UNS("좌표평면: O, A₀(10,0), 정삼각형 OA₀A₁, 내분점 B₁, 정삼각형 A₁B₁A₂, B₂, A₃, B₃, A₄ … 나선형으로 이어지는 정삼각형들"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형 나선 도형 / 첨자 점 라벨(A₀, B₁ 등)·선분 윗줄 텍스트 처리",
    note="출처 [2004년 3월 고3 이과 27번]. 홀수 단계 벡터 10(4/9)^k e^(i120°), 짝수 단계 (20/3)(4/9)^k → 극한점 (13, 9√3) → a=13.")

add(id="8e4185e4", qtype="short",
    question=("다음 그림과 같이 원점 O와 점 A₀[[point(14, 0)]]에 대하여 제1사분면 위에 OA₀을 한 변으로 하는 정삼각형 OA₀A₁을 만들고 A₀A₁을 [[ratio(1,3)]]으로 내분하는 점을 B₁이라 한다. "
              "또, △OA₀A₁ 밖에 A₁B₁을 한 변으로 하는 정삼각형 A₁B₁A₂를 만들고 A₁A₂를 [[ratio(1,3)]]으로 내분하는 점을 B₂라 한다. "
              "이와 같은 과정을 한없이 반복하면 점 Aₙ은 점 [[point(a, b)]]에 한없이 가까워진다. [[a]]의 값을 구하시오."),
    choices=None, derived_answer="22",
    figure=UNS("좌표평면: O, A₀(14,0), 정삼각형 OA₀A₁, 내분점 B₁, 정삼각형 A₁B₁A₂, B₂, A₃, B₃, A₄ … 나선형으로 이어지는 정삼각형들"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형 나선 도형 / 첨자 점 라벨(A₀, B₁ 등)·선분 윗줄 텍스트 처리",
    note="홀수 단계 벡터 14(9/16)^k e^(i120°), 짝수 단계 (21/2)(9/16)^k → x=14-16+24=22. 빠른정답 1과 불일치.")

add(id="7744c80c", qtype="choice",
    question=("곡선 [[y = pow(4,x)]]을 [[x]]축의 방향으로 평행이동시켜 점 [[point(k, 3)]]을 지나도록 하는 곡선의 [[y]]절편을 [[sub(a,k)]]라 하자. "
              "[[sum(k, 1, inf, sub(a,k))]]의 값은?\n(단, [[k]]는 자연수)"),
    choices=["[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]", "[[frac(3,2)]]"],
    derived_answer="③",
    figure=UNS("좌표평면: y=4^x 그래프와 x축 방향으로 평행이동한 곡선(점 (k,3) 통과, y절편 aₖ), 이동 화살표"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 지수함수 그래프",
    note="aₖ=3/4^k → 합 1 → ③. 빠른정답 2와 불일치.")

add(id="fa1f1bb0", qtype="choice",
    question=("함수 [[y = pow(3,x)]]의 그래프를 [[x]]축의 방향으로 평행이동시켜 점 [[point(k, 2)]] ([[k]]는 자연수)를 지나도록 하는 곡선의 [[y]]절편을 [[sub(a,k)]]라 하자. "
              "이때 [[sum(k, 1, inf, sub(a,k))]]의 값은?"),
    choices=["[[frac(2,3)]]", "[[1]]", "[[frac(4,3)]]", "[[frac(3,2)]]", "[[2]]"],
    derived_answer="②",
    figure=UNS("좌표평면: y=3^x 그래프와 x축 방향으로 평행이동한 곡선(점 (k,2) 통과, y절편 aₖ), 이동 화살표"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 지수함수 그래프",
    note="출처 [2008년 3월 고3 이과 28번]. aₖ=2/3^k → 합 1 → ②. 빠른정답 13과 불일치.")

add(id="d34a83ad", qtype="choice",
    question=("그림과 같이 중심이 [[point(1, 0)]]이고 반지름의 길이가 1인 원 O₁이 있다. 원 O₁이 직선 [[y = frac(1, sqrt(3)) x]]와 만나는 점 중에서 원점이 아닌 점을 A₁이라 하고 "
              "직선 [[y = frac(1, sqrt(3)) x]]의 위 쪽에 있는 호 OA₁의 길이를 [[sub(l,1)]]이라 하자.\n"
              "중심이 [[point(sub(l,1), 0)]]이고 반지름의 길이가 [[sub(l,1)]]인 원 O₂를 그린다. 원 O₂가 직선 [[y = frac(1, sqrt(3)) x]]와 만나는 점 중에서 원점이 아닌 점을 A₂라 하고 "
              "직선 [[y = frac(1, sqrt(3)) x]]의 위 쪽에 있는 호 OA₂의 길이를 [[sub(l,2)]]라 하자.\n"
              "이와 같은 과정을 계속하여 [[n]]번째 얻은 호의 길이를 [[sub(l,n)]]이라 할 때, [[sum(n, 1, inf, frac(1, sub(l,n)))]]의 값은?"),
    choices=["[[frac(1, pi - 3)]]", "[[frac(2, pi - 3)]]", "[[frac(1, 2 pi - 3)]]", "[[frac(2, 2 pi - 3)]]", "[[frac(3, 2 pi - 3)]]"],
    derived_answer="⑤",
    figure=UNS("좌표평면: 원점을 지나는 원 O₁, O₂, O₃(중심 x축 위), 직선 y=x/√3, 교점 A₁, A₂, A₃, 직선 위쪽 호 OA₁·OA₂·OA₃ 굵게"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원 3개+직선 도형 / 첨자 점 라벨(O₁, A₁ 등) 텍스트 처리",
    note="출처 [2012년 10월 고3 문과 21번/4점]. 호 중심각 120° → l₁=2π/3, lₙ=(2π/3)ⁿ → Σ(3/2π)ⁿ=3/(2π-3) → ⑤. 빠른정답 1과 불일치.")

add(id="0b421061", qtype="choice",
    question=("그림과 같이 [[x]]축 위의 점 A₁[[point(6 pi - 12, 0)]]에 대하여 OA₁을 지름으로 하는 반원을 제1사분면에 그리고, "
              "OA₁ = ⌒OA₂인 점 A₂를 [[y]]축 위에 잡아 OA₂를 지름으로 하는 반원을 제2사분면에 그린다.\n"
              "또, OA₂ = ⌒OA₃인 점 A₃를 [[x]]축 위에 잡아 OA₃를 지름으로 하는 반원을 제3사분면에 그리고, "
              "OA₃ = ⌒OA₄인 점 A₄를 [[y]]축 위에 잡아 OA₄를 지름으로 하는 반원을 제4사분면에 그린다. "
              "같은 방법으로 제1사분면, 제2사분면, ⋯에 반원을 계속하여 그려나갈 때, 반원들의 호의 길이의 합 Σ[n=1..∞] ⌒OAₙ의 값은?\n"
              "(단, ⌒OAₙ은 OAₙ을 지름으로 하는 반원의 호이고 [[n]] = 1, 2, 3, ⋯이다.)"),
    choices=["[[9 pi]]", "[[8 pi + 1]]", "[[pow(pi,2) + 10]]", "[[2 pow(pi,2) + 3]]", "[[3 pow(pi,2)]]"],
    derived_answer="⑤",
    figure=UNS("좌표평면: 원점 O에서 시작해 A₁(x축 양), A₂(y축 양), A₃(x축 음), A₄(y축 음), A₅, A₆ … 를 지름 끝으로 하는 반원들이 각 사분면에 나선형으로 작아짐"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 반원 나선 도형 / 첨자 점 라벨(A₁ 등)·선분 윗줄(OAₙ)·호 기호(⌒OAₙ)·Σ⌒OAₙ 텍스트 처리",
    note="출처 [2006년 3월 고3 이과 29번]. ⌒OA₁=3π²-6π, 이후 공비 2/π → 합 3π² → ⑤. 빠른정답 27과 불일치.")

add(id="70ba5f0e", qtype="choice",
    question=("그림과 같이 [[seg(AB) = 1]], [[seg(AC) = 2]]인 직각삼각형 ABC에서 꼭짓점 A를 중심, [[seg(AB)]]를 반지름으로 하는 원을 그렸을 때, "
              "[[seg(AC)]]와 만나는 점을 A₁, AC ⊥ A₁B₁이면서 [[seg(BC)]] 위에 있는 점을 B₁, 다시 꼭짓점 B₁을 중심, A₁B₁을 반지름으로 하는 원을 그렸을 때, "
              "CB₁과 만나는 점을 B₂, CB₁ ⊥ A₂B₂이면서 A₁C 위에 있는 점을 A₂라 하자.\n"
              "위와 같은 과정을 계속 반복해 나갈 때,\n[[seg(AB)]] + A₁B₁ + A₂B₂ + ⋯의 값은?"),
    choices=["[[frac(3 + sqrt(3), 2)]]", "[[frac(3,2) + sqrt(3)]]", "[[frac(3 + 3 sqrt(3), 2)]]", "[[2 + frac(sqrt(3),2)]]", "[[2 + sqrt(3)]]"],
    derived_answer="①",
    figure=UNS("직각삼각형 ABC(∠B 직각, AB=1, AC=2), A 중심 반지름 1 호와 AC의 교점 A₁, A₁B₁⊥AC(B₁은 BC 위), B₁ 중심 호와 교점 B₂, A₂B₂⊥CB₁, A₃, B₃ …"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형+호 반복 도형 / 첨자 점 라벨(A₁, B₁ 등)·선분 윗줄·수직 기호 텍스트 처리",
    note="A₁B₁=1/√3, 공비 1/√3 → 합 1/(1-1/√3)=(3+√3)/2 → ①. 빠른정답 3과 불일치.")

add(id="b338a6b8", qtype="choice",
    question=("그림과 같이 한 변의 길이가 [[a]]인 정사각형 OB₁C₁A₀이 있다. 삼각형 OA₁D₁이 ∠D₁OA₁ = [[deg(30)]]인 이등변삼각형이 되도록 변 B₁C₁, A₀C₁ 위에 각각 점 A₁, D₁을 잡고 변 OA₁의 길이를 [[sub(l,1)]]이라 하자.\n"
              "선분 OA₁을 한 변으로 하는 정사각형 OB₂C₂A₁에서 삼각형 OA₂D₂가 ∠D₂OA₂ = [[deg(30)]]인 이등변삼각형이 되도록 변 B₂C₂, A₁C₂ 위에 각각 점 A₂, D₂를 잡고 변 OA₂의 길이를 [[sub(l,2)]]라 하자.\n"
              "선분 OA₂를 한 변으로 하는 정사각형 OB₃C₃A₂에서 삼각형 OA₃D₃이 ∠D₃OA₃ = [[deg(30)]]인 이등변삼각형이 되도록 변 B₃C₃, A₂C₃ 위에 각각 점 A₃, D₃을 잡고 변 OA₃의 길이를 [[sub(l,3)]]이라 하자.\n"
              "이와 같은 과정을 계속하여 얻은 이등변삼각형 OAₙDₙ에서 변 OAₙ의 길이를 [[sub(l,n)]]이라 하자. [[sum(n, 1, inf, frac(1, sub(l,n))) = 2 + sqrt(3)]]일 때, [[a]]의 값은?"),
    choices=["[[sqrt(3)]]", "[[1 + sqrt(3)]]", "[[2 sqrt(3)]]", "[[2 + sqrt(3)]]", "[[3 sqrt(3)]]"],
    derived_answer="①",
    figure=UNS("점 O를 공유하며 회전·확대되는 정사각형 OB₁C₁A₀, OB₂C₂A₁, OB₃C₃A₂ …, 각 정사각형 안의 이등변삼각형 OA₁D₁, OA₂D₂, OA₃D₃ 음영, 변 길이 a, l₁, l₂, l₃ 표시"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형+이등변삼각형 나선 도형 / 첨자 점 라벨(A₁, D₁ 등)·각 기호 텍스트 처리",
    note="lₙ=(2/√3)ⁿ a → Σ1/lₙ=√3(2+√3)/a=2+√3 → a=√3 → ①.")

add(id="43ea3ac3", qtype="choice",
    question=("그림과 같이 중심이 O이고 반지름의 길이가 [[2 sqrt(3)]]인 원 O₁의 6등분점을 각각 A₁, B₁, C₁, D₁, E₁, F₁이라 하자. "
              "중심각의 크기가 [[deg(60)]]인 부채꼴 OA₁B₁의 호 A₁B₁의 이등분점을 P₁이라 하고, 선분 OA₁ 위에 ∠OP₁A₂ = [[deg(45)]]가 되도록 점 A₂를 정한다.\n"
              "중심이 O이고 선분 OA₂를 반지름으로 하는 원 O₂가 5개의 선분 OB₁, OC₁, OD₁, OE₁, OF₁과 만나는 점을 각각 B₂, C₂, D₂, E₂, F₂라 하고, "
              "원 O₂의 외부에 정육각형 A₂B₂C₂D₂E₂F₂의 각 변을 지름으로 하는 6개의 반원을 그리고, 이 6개의 반원의 호의 길이의 합을 [[sub(l,1)]]이라 하자.\n"
              "중심각의 크기가 [[deg(60)]]인 부채꼴 OA₂B₂의 호 A₂B₂의 이등분점을 P₂라 하고, 선분 OA₂ 위에 ∠OP₂A₃ = [[deg(45)]]가 되도록 점 A₃을 정한다.\n"
              "중심이 O이고 선분 OA₃을 반지름으로 하는 원 O₃이 5개의 선분 OB₂, OC₂, OD₂, OE₂, OF₂와 만나는 점을 각각 B₃, C₃, D₃, E₃, F₃이라 하고, "
              "원 O₃의 외부에 정육각형 A₃B₃C₃D₃E₃F₃의 각 변을 지름으로 하는 6개의 반원을 그리고, 이 6개의 반원의 호의 길이의 합을 [[sub(l,2)]]라 하자.\n"
              "이와 같은 과정을 계속하여 [[n]]번째 얻은 6개의 반원의 호의 길이의 합을 [[sub(l,n)]]이라 할 때, [[sum(n, 1, inf, sub(l,n))]]의 값은?"),
    choices=["[[6(1 + sqrt(3)) pi]]", "[[6(2 + sqrt(3)) pi]]", "[[6(3 + sqrt(3)) pi]]", "[[12(2 + sqrt(3)) pi]]", "[[12(3 + sqrt(3)) pi]]"],
    derived_answer="③",
    figure=UNS("동심원 O₁, O₂, O₃과 6등분점, 내접 정육각형 A₂B₂…F₂, A₃B₃…F₃, 각 변을 지름으로 하는 반원(호 l₁, l₂), 점 P₁, P₂"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 동심원+정육각형+반원 복합 도형 / 첨자 점 라벨·각 기호 텍스트 처리",
    note="OA₂=R(√3-1), l₁=3π·R₂=6π(3-√3), 공비 √3-1 → 합 6(3+√3)π → ③.")

add(id="7017d341", qtype="choice",
    question=("그림과 같이 A₁B₁ = 1, A₁D₁ = 2인 직사각형 A₁B₁C₁D₁에 대하여 선분 A₁D₁의 중점을 M이라 하자. "
              "선분 A₁D₁을 지름으로 하는 반원과 선분 A₁M과 선분 MD₁을 각각 지름으로 하는 두 반원을 그려서 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,1)]]이라 하자.\n"
              "선분 MB₁과 선분 MC₁이 선분 A₁D₁을 지름으로 하는 반원과 만나는 점을 각각 B₂, C₂라 하고, 점 B₂와 점 C₂에서 선분 A₁D₁에 내린 수선의 발을 각각 A₂, D₂라 하자. "
              "선분 A₂D₂를 지름으로 하는 반원과 선분 A₂M과 선분 MD₂를 각각 지름으로 하는 두 반원을 그려서 새로 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,2)]]라 하자.\n"
              "이와 같은 과정을 계속하여 [[n]]번째 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,n)]]이라 할 때, [[sum(n, 1, inf, sub(l,n))]]의 값은?"),
    choices=["[[(1 + sqrt(2)) pi]]", "[[(2 + sqrt(2)) pi]]", "[[(3 + 2 sqrt(2)) pi]]", "[[(4 + 2 sqrt(2)) pi]]", "[[(5 + 3 sqrt(2)) pi]]"],
    derived_answer="④",
    figure=UNS("직사각형 A₁B₁C₁D₁(위변 A₁D₁, 중점 M), 큰 반원(아래)과 두 작은 반원(위)으로 된 하트 모양이 점점 작아지며 겹쳐 그려짐, MB₁·MC₁과 반원의 교점 B₂, C₂, 수선의 발 A₂, D₂"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 하트 모양 반원 반복 도형 / 첨자 점 라벨·선분 윗줄 텍스트 처리 / ♡ 기호",
    note="출처 [2013년 11월 고2 이과 15번/4점]. l₁=2π, 공비 √2/2 → 합 (4+2√2)π → ④. 빠른정답 27과 불일치.")

add(id="54f59415", qtype="choice",
    question=("그림과 같이 A₁B₁ = [[sqrt(2)]], A₁D₁ = [[2 sqrt(2)]]인 직사각형 A₁B₁C₁D₁에 대하여 선분 A₁D₁의 중점을 M이라 하자. "
              "선분 A₁D₁을 지름으로 하는 반원과 선분 A₁M과 선분 MD₁을 각각 지름으로 하는 두 반원을 그려서 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,1)]]이라 하자. "
              "선분 MB₁과 선분 MC₁이 선분 A₁D₁을 지름으로 하는 반원과 만나는 점을 각각 B₂, C₂라 하고, 점 B₂와 점 C₂에서 선분 A₁D₁에 내린 수선의 발을 각각 A₂, D₂라 하자. "
              "선분 A₂D₂를 지름으로 하는 반원과 선분 A₂M과 선분 MD₂를 각각 지름으로 하는 두 반원을 그려서 새로 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,2)]]라 하자.\n"
              "이와 같은 과정을 계속하여 [[n]]번째 얻은 ♡ 모양의 도형의 둘레의 길이를 [[sub(l,n)]]이라 할 때, [[sum(n, 1, inf, sub(l,n))]]의 값은?"),
    choices=["[[(2 + 2 sqrt(2)) pi]]", "[[(3 + 2 sqrt(2)) pi]]", "[[(3 + 4 sqrt(2)) pi]]", "[[(4 + 2 sqrt(2)) pi]]", "[[(4 + 4 sqrt(2)) pi]]"],
    derived_answer="⑤",
    figure=UNS("직사각형 A₁B₁C₁D₁(위변 A₁D₁, 중점 M), 큰 반원(아래)과 두 작은 반원(위)으로 된 하트 모양이 점점 작아지며 겹쳐 그려짐, 교점 B₂, C₂, 수선의 발 A₂, D₂"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 하트 모양 반원 반복 도형 / 첨자 점 라벨·선분 윗줄 텍스트 처리 / ♡ 기호",
    note="l₁=2√2π, 공비 √2/2 → 합 (4+4√2)π → ⑤. 빠른정답 2와 불일치.")

add(id="65159906", qtype="choice",
    question=("그림과 같이 원점을 중심으로 하고 반지름의 길이가 3인 원 O₁을 그리고, 원 O₁이 좌표축과 만나는 네 점을 각각 A₁[[point(0, 3)]], B₁[[point(-3, 0)]], C₁[[point(0, -3)]], D₁[[point(3, 0)]]이라 하자.\n"
              "두 점 B₁, D₁을 모두 지나고 두 점 A₁, C₁을 각각 중심으로 하는 두 원이 원 O₁의 내부에서 [[y]]축과 만나는 점을 각각 C₂, A₂라 하자.\n"
              "호 B₁A₁D₁과 호 B₁A₂D₁로 둘러싸인 도형의 넓이를 [[sub(S,1)]], 호 B₁C₁D₁과 호 B₁C₂D₁로 둘러싸인 도형의 넓이를 [[sub(T,1)]]이라 하자.\n"
              "선분 A₂C₂를 지름으로 하는 원 O₂를 그리고, 원 O₂가 [[x]]축과 만나는 두 점을 각각 B₂, D₂라 하자.\n"
              "두 점 B₂, D₂를 모두 지나고 두 점 A₂, C₂를 각각 중심으로 하는 두 원이 원 O₂의 내부에서 [[y]]축과 만나는 점을 각각 C₃, A₃이라 하자. "
              "호 B₂A₂D₂과 호 B₂A₃D₂로 둘러싸인 도형의 넓이를 [[sub(S,2)]], 호 B₂C₂D₂과 호 B₂C₃D₂로 둘러싸인 도형의 넓이를 [[sub(T,2)]]라 하자.\n"
              "이와 같은 과정을 계속하여 [[n]]번째 얻은 호 BₙAₙDₙ과 호 BₙAₙ₊₁Dₙ으로 둘러싸인 도형의 넓이를 [[sub(S,n)]], 호 BₙCₙDₙ과 호 BₙCₙ₊₁Dₙ로 둘러싸인 도형의 넓이를 [[sub(T,n)]]이라 할 때, "
              "[[sum(n, 1, inf, (sub(S,n) + sub(T,n)))]]의 값은?"),
    choices=["[[6(sqrt(2) + 1)]]", "[[6(sqrt(3) + 1)]]", "[[6(sqrt(5) + 1)]]", "[[9(sqrt(2) + 1)]]", "[[9(sqrt(3) + 1)]]"],
    derived_answer="④",
    figure=UNS("좌표평면: 원점 중심 반지름 3 원 O₁과 A₁(0,3), B₁(-3,0), C₁(0,-3), D₁(3,0), A₁·C₁ 중심 호 B₁A₂D₁·B₁C₂D₁, 초승달 모양 영역 S₁·T₁ 음영, 안쪽으로 반복되는 작은 원들"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원+호 반복 복합 도형 / 첨자 점 라벨(A₁, Bₙ, Aₙ₊₁ 등) 텍스트 처리",
    note="출처 [2009년 11월 고3 문과 15번]. S₁=T₁=9, 공비 (√2-1)² → 합 18/(2√2-2)=9(√2+1) → ④.")

add(id="86b2d142", qtype="choice",
    question=("그림과 같이 원점 O와 점 [[point(2, 0)]]을 지름의 양 끝으로 하는 원을 C₁이라 하자. 또, 원 C₁과 직선 [[y = x]]가 만나는 두 점을 지름의 양 끝으로 하는 원을 C₂, "
              "원 C₂와 [[y]]축이 만나는 두 점을 지름의 양 끝으로 하는 원을 C₃이라 하자. 또, 원 C₃과 직선 [[y = -x]]가 만나는 두 점을 지름의 양 끝으로 하는 원을 C₄, "
              "원 C₄와 [[x]]축이 만나는 두 점을 지름의 양 끝으로 하는 원을 C₅라 하자.\n"
              "이와 같은 방법으로 중심이 차례로 직선 [[y = x]], [[y]]축, 직선 [[y = -x]], [[x]]축, ⋯ 위에 있는 원 C₆, C₇, C₈, C₉, ⋯를 한없이 만들어 갈 때, "
              "원 Cₙ의 내부와 원 Cₙ₊₁의 외부의 공통부분(어두운 부분)의 넓이를 [[sub(S,n)]] ([[n]] = 1, 2, 3, ⋯)이라 하자. 이때 [[sum(n, 1, inf, sub(S,n))]]의 값은?"),
    choices=["[[pi + 1]]", "[[frac(3,2) pi]]", "[[frac(5,4)(pi + 1)]]", "[[frac(3,2)(pi + 1)]]", "[[2 pi]]"],
    derived_answer="①",
    figure=UNS("좌표평면 4개 패널: 원 C₁(지름 O~(2,0))과 y=x 위 원 C₂(S₁ 음영), C₃(S₂ 음영), y=-x 위 C₄(S₃ 음영), C₅(S₄ 음영) — 원점을 지나며 점점 작아지는 원들"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 원 연쇄 도형 4개 패널 / 첨자 라벨(C₁, Cₙ₊₁ 등) 텍스트 처리",
    note="출처 [2008년 3월 고3 이과 17번]. S₁=π/2+1/2, 넓이 공비 1/2 → 합 π+1 → ①. 빠른정답 5와 불일치.")

add(id="2c340db2", qtype="short",
    question=("두 정수 [[alpha]], [[beta]] ([[alpha > beta]])에 대하여 다음 조건을 만족시키는 수열 [[set(sub(a,n))]]이 있다.\n"
              "모든 자연수 [[n]]에 대하여\n[[sub(a,n) = alpha × sin(frac(n,2) pi) + beta × cos(frac(n,2) pi)]]이고\n[[sub(a,1) sub(a,2) sub(a,3) sub(a,4) = 4]]이다.\n"
              "수열 [[set(sub(a,n))]]과 [[sub(b,1) > 0]]인 등비수열 [[set(sub(b,n))]]에 대하여\n"
              "[[sum(n, 1, inf, (sub(a, 4n - 2) sub(b,n))) = sum(n, 1, inf, (sub(a, 4n - 3) sub(b, 2n))) = 6]]일 때,\n"
              "[[sub(b,1) sub(b,3) = frac(q,p)]]이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="109", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2025년 6월 고3 미적분 29번/4점]. α²β²=4, r=-β/(α+β); (α,β)=(-1,-2), r=-2/3, b₁=5 → b₁b₃=100/9 → 109.")

add(id="f94a6386", qtype="short",
    question=("두 정수 [[alpha]], [[beta]] ([[alpha > beta]], [[abs(alpha) != 1]], [[abs(beta) != 1]])에 대하여 다음 조건을 만족시키는 수열 [[set(sub(a,n))]]이 있다.\n"
              "모든 자연수 [[n]]에 대하여\n[[sub(a,n) = alpha × sin(frac(n,2) pi) + beta × cos(frac(n,2) pi)]]이고\n[[sub(a,1) sub(a,2) sub(a,3) sub(a,4) = 36]]이다.\n"
              "수열 [[set(sub(a,n))]]과 [[sub(b,1) > 0]]인 등비수열 [[set(sub(b,n))]]에 대하여\n"
              "[[sum(n, 1, inf, (sub(a, 4n - 2) sub(b,n))) = sum(n, 1, inf, (sub(a, 4n - 3) sub(b, 2n))) = 15]]일 때,\n"
              "[[sub(b,1) sub(b,3) = frac(q,p)]]이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="601", figure=None, difficulty_est=4, confidence=0.8,
    note="출처 [2025년 6월 고3 미적분 29번 변형]. α²β²=36, (α,β)=(-2,-3), r=-3/5, b₁=8 → b₁b₃=576/25 → 601. 빠른정답 54와 불일치.")

# ───────────────────────── 수열의 극한 ─────────────────────────
add(id="76e78554", qtype="short",
    question=("다음 수열의 극한값을 구하시오.\n[[1]], [[frac(2,3)]], [[frac(3,5)]], [[frac(4,7)]], ⋯, [[frac(n, 2n - 1)]], ⋯"),
    choices=None, derived_answer="frac(1,2)", figure=None, difficulty_est=1, confidence=0.9,
    note="n/(2n-1) → 1/2. 수열은 상자 안에 인쇄(장식).")

add(id="e144d99b", qtype="choice",
    question="다음 수열 중 수렴하는 것을 모두 고르면?",
    choices=["[[0]], [[3]], [[0]], [[3]], ⋯",
             "[[7]], [[7]], [[7]], [[7]], ⋯",
             "[[frac(1, sqrt(2))]], [[frac(2, sqrt(4))]], [[frac(3, sqrt(6))]], [[frac(4, sqrt(8))]], ⋯",
             "[[set(3 - frac(pow(-1, n), n))]]",
             "[[1]], [[-frac(1,2)]], [[frac(1,4)]], [[-frac(1,8)]], [[frac(1,16)]], [[-frac(1,32)]], ⋯"],
    derived_answer="②, ④, ⑤", figure=None, difficulty_est=1, confidence=0.85,
    note="① 진동, ② 수렴(7), ③ n/√(2n)→∞, ④ →3, ⑤ →0 → ②, ④, ⑤(복수 선택 문항). 빠른정답 3과 불일치.")

add(id="919d0e3b", qtype="choice",
    question=("자연수 [[n]]에 대하여 원점을 지나는 직선과 곡선 [[y = (x - n)(x - n - 1)]]이 제4사분면에서 접할 때, 접점의 [[x]]좌표를 [[sub(a,n)]], 직선의 기울기를 [[sub(b,n)]]이라 하자. "
              "다음은 [[lim(n, inf, sub(a,n) sub(b,n))]]의 값을 구하는 과정이다.\n"
              "원점을 지나고 기울기가 [[sub(b,n)]]인 직선의 방정식은 [[y = sub(b,n) x]]이다.\n"
              "이 직선이 곡선 [[y = (x - n)(x - n - 1)]]에 접하므로 이차방정식 [[sub(b,n) x = (x - n)(x - n - 1)]]의 근 [[x = sub(a,n)]]은 중근이다.\n"
              "그러므로 이차방정식\n[[pow(x,2) - (sub(b,n) + 2n + 1) x + n(n + 1) = 0]]\n에서 이차식\n[[pow(x,2) - (sub(b,n) + 2n + 1) x + n(n + 1)]]\n은 완전제곱식으로 나타내어진다.\n"
              "그런데 [[sub(a,n) > 0]]이므로\n[[pow(x,2) - (sub(b,n) + 2n + 1) x + n(n + 1) = pow(x - sqrt(n(n + 1)), 2)]]\n에서\n"
              "[[sub(a,n)]] = (가), [[sub(b,n)]] = (나)\n이다.\n따라서 [[lim(n, inf, sub(a,n) sub(b,n))]] = (다) 이다.\n"
              "위의 (가)와 (나)에 알맞은 식을 각각 [[f(n)]], [[g(n)]]이라 하고, (다)에 알맞은 값을 [[alpha]]라 할 때, [[2 f(-alpha) - g(-alpha)]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[1]]", "[[frac(3,2)]]", "[[2]]", "[[frac(5,2)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2019년 3월 고3 문과 18번 변형]. (가)√(n(n+1)), (나)2√(n(n+1))-2n-1, (다)-1/4 → 2f(1/4)-g(1/4)=3/2 → ③. 빠른정답 8과 불일치.")

add(id="8835e5dc", qtype="choice",
    question=("[[sub(a,1) = 3]], [[sub(a,2) = -4]]인 수열 [[set(sub(a,n))]]과 등차수열 [[set(sub(b,n))]]이 모든 자연수 [[n]]에 대하여 "
              "[[sum(k, 1, n, frac(sub(a,k), sub(b,k))) = frac(6, n + 1)]]을 만족시킬 때, [[lim(n, inf, sub(a,n) sub(b,n))]]의 값은?"),
    choices=["[[-54]]", "[[-frac(75,2)]]", "[[-24]]", "[[-frac(27,2)]]", "[[-6]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2023년 3월 고3 미적분 27번/3점]. b₁=1, b₂=4 → bₙ=3n-2, aₙ/bₙ=-6/(n(n+1)) → aₙbₙ→-54 → ①.")

add(id="16ec25ec", qtype="choice",
    question=("[[sub(a,1) = 3]], [[sub(a,2) = 6]]인 등차수열 [[set(sub(a,n))]]과 모든 항이 양수인 수열 [[set(sub(b,n))]]이 모든 자연수 [[n]]에 대하여\n"
              "[[sum(k, 1, n, sub(a,k) pow(sub(b,k), 2)) = 3(pow(n,3) - n + 1)]]을 만족시킬 때,\n"
              "[[lim(n, inf, frac(sub(a,n), sub(b,n) sub(b,3n)))]]의 값은?"),
    choices=["[[frac(sqrt(3),3)]]", "[[frac(2 sqrt(3),3)]]", "[[sqrt(3)]]", "[[frac(4 sqrt(3),3)]]", "[[frac(5 sqrt(3),3)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2024년 3월 고3 미적분 27번 변형]. aₙ=3n, bₙ²=3(n-1) (n≥2) → 극한 1/√3 → ①. 빠른정답 -1/2와 불일치.")

add(id="18cfdbb0", qtype="choice",
    question=("수열 [[set(sub(a,n))]]에 대하여 [[lim(n, inf, frac(n sub(a,n), pow(n,2) + 1)) = 2]]일 때,\n"
              "[[lim(n, inf, frac(2 pow(n,2), (sub(a,n) + n)(sub(a,n) - n)))]]의 값은? (단, 모든 자연수 [[n]]에 대하여 [[sub(a,n) + n != 0]], [[sub(a,n) - n != 0]]이다.)"),
    choices=["[[frac(1,6)]]", "[[frac(1,3)]]", "[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(5,6)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="aₙ/n→2 → 2/((2+1)(2-1))=2/3 → ④.")

add(id="de72edba", qtype="choice",
    question=("다음 보기 중 두 수열 [[set(sub(a,n))]], [[set(sub(b,n))]]에 대하여 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[lim(n, inf, sub(a,n)) = inf]], [[lim(n, inf, sub(b,n)) = 0]]이면 [[lim(n, inf, sub(a,n) sub(b,n)) = 0]]이다.\n"
              "ㄴ. [[lim(n, inf, sub(a,n)) = -inf]]이고 [[lim(n, inf, (sub(a,n) - sub(b,n))) = alpha]] ([[alpha]]는 상수)이면 [[lim(n, inf, frac(sub(b,n), sub(a,n))) = 1]]이다.\n"
              "ㄷ. [[lim(n, inf, sub(a,n)) = alpha]] ([[alpha]]는 상수)이고 [[lim(n, inf, (sub(a,n) + sub(b,n))) = 2 alpha]]이면 [[lim(n, inf, sub(b,n)) = alpha]]이다.\n"
              "ㄹ. [[lim(n, inf, sub(a,n)) = alpha]] ([[alpha]]는 상수)이고 [[lim(n, inf, sub(a,n) sub(b,n)) = pow(alpha, 2)]]이면 [[lim(n, inf, sub(b,n)) = alpha]]이다."),
    choices=["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="ㄱ ✗(n², 1/n), ㄴ ✓, ㄷ ✓, ㄹ ✗(α=0 반례) → ③. 빠른정답 5와 불일치.")

add(id="63fd8f54", qtype="short",
    question=("다음 그림과 같이 자연수 [[n]] ([[n >= 2]])에 대하여 중심이 C이고 반지름의 길이가 [[n]]인 원 O와 [[seg(AB) = 1]]을 만족시키는 원 O 위의 두 점 A, B가 있다. "
              "[[angle(BAC)]]를 이등분하는 직선이 원 O와 만나는 점 중 A가 아닌 점을 D라 하자. 점 B를 포함하지 않는 호 AD 위의 점 E에 대하여 [[ratio(seg(BD), seg(DE)) = ratio(2,1)]]일 때, "
              "삼각형 CDE의 넓이를 [[sub(S,n)]]이라 하면 [[lim(n, inf, frac(sub(S,n), pow(n,2))) = frac(q sqrt(7), p)]]이다. [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="9",
    figure=UNS("원 O(중심 C) 위의 점 A, B(아래쪽), 각 BAC의 이등분선과 원의 교점 D, 호 AD 위 점 E, 삼각형 CDE 음영, 선분 CA, CB, CD, BD"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 원+삼각형 복합 도형",
    note="출처 [2025년 3월 고3 미적분 29번 변형]. BD=√(n(2n-1)), sin(∠DCE/2)→√2/4 → Sₙ/n²→√7/8 → p+q=9. 빠른정답 4와 불일치.")

add(id="9bef96cc", qtype="choice",
    question=("자연수 [[n]]에 대하여 [[angle(A) = deg(90)]], [[seg(AB) = 3]], [[seg(CA) = n]]인 삼각형 ABC에서 [[angle(A)]]의 이등분선이 선분 BC와 만나는 점을 D라 하자. "
              "선분 CD의 길이를 [[sub(a,n)]]이라 할 때,\n[[lim(n, inf, (n - sub(a,n)))]]의 값은?"),
    choices=["[[1]]", "[[sqrt(3)]]", "[[3]]", "[[3 sqrt(3)]]", "[[9]]"],
    derived_answer="③",
    figure=UNS("직각삼각형 ABC(∠A 직각, AB=3, CA=n), A의 이등분선과 BC의 교점 D, 점선 호로 변 길이 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+이등분선 도형",
    note="출처 [2021년 3월 고3 미적분 28번 변형]. aₙ=n√(n²+9)/(n+3) → n-aₙ→3 → ③. 빠른정답 1과 불일치.")

add(id="b86d59fd", qtype="choice",
    question=("다음 그림과 같이 가로의 길이가 [[n]], 세로의 길이가 60인 직사각형 AOCₙBₙ에 대하여 대각선 ACₙ과 선분 B₁C₁의 교점을 Dₙ이라 한다.\n"
              "이때 lim[n→∞] (ACₙ − OCₙ) / B₁Dₙ의 값은? (단, [[n]]은 자연수이다.)"),
    choices=["[[12]]", "[[15]]", "[[20]]", "[[30]]", "[[60]]"],
    derived_answer="④",
    figure=UNS("직사각형 AOCₙBₙ(A 좌상, O 좌하, Cₙ 우하, Bₙ 우상, 세로 60), 위변 위 B₁(AB₁=1), B₂ …, 아래변 위 C₁(D₁), C₂ …, 대각선 ACₙ과 B₁C₁의 교점 Dₙ, D₂ … 표시"),
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 직사각형+대각선 도형 / 첨자 점 라벨(Cₙ, Bₙ, Dₙ, B₁)이 든 선분식 극한을 텍스트로 표기",
    note="ACₙ-OCₙ=3600/(√(n²+3600)+n)≈1800/n, B₁Dₙ=60/n → 30 → ④.")

# ───────────────────────── 삼각함수의 덧셈정리 ─────────────────────────
add(id="315203c8", qtype="short",
    question=("[[x]]에 대한 이차방정식 [[pow(x,2) + 2 sqrt(3) a x + pow(a,2) + 6 = 0]]이\n두 실근 [[tan(alpha)]], [[tan(beta)]]를 갖고 [[alpha + beta = frac(pi,6)]]일 때,\n"
              "상수 [[a]]의 값을 구하시오. (단, [[a != 1]])"),
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="tan(α+β)=2√3a/(a²+5)=1/√3 → a²-6a+5=0 → a=5 (a≠1).")

add(id="cfc94a4e", qtype="choice",
    question=("그림과 같이 곡선 [[y = frac(2,x)]] 위의\n두 점 [[A(-1, -2)]], [[B(1, 2)]]에 대하여\n[[angle(APB) = frac(pi,4)]]가 되도록 점 [[P(a, frac(2,a))]]를 정할 때,\n"
              "상수 [[a]]의 값은? (단, [[a > 1]])"),
    choices=["[[3 + sqrt(2)]]", "[[2 + 2 sqrt(2)]]", "[[4 + sqrt(2)]]", "[[4 sqrt(2)]]", "[[3 + 2 sqrt(2)]]"],
    derived_answer="②",
    figure=UNS("좌표평면: 쌍곡선 y=2/x, 점 A(제3사분면), B(제1사분면), 곡선 위 점 P(제1사분면 오른쪽), 선분 PA, PB"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 유리함수 그래프+선분 도형",
    note="출처 [2016년 11월 고2 이과 17번/4점]. 기울기 2/a, -2/a → tan=4a/(a²-4)=1 → a=2+2√2 → ②. 빠른정답 1과 불일치.")

add(id="1137471e", qtype="choice",
    question=("두 직선 [[y = x + a]], [[y = frac(1,5) x + b]]가 원 [[pow(x,2) + pow(y,2) = pow(r,2)]]에 접하는 점을 각각 P₁, P₂라 하고 ∠P₁OP₂ = [[alpha]]일 때, "
              "[[tan(alpha)]]의 값은? (단, [[a < 0]], [[b < 0]])"),
    choices=["[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(5,6)]]", "[[1]]", "[[frac(7,6)]]"],
    derived_answer="②",
    figure=UNS("좌표평면: 원점 중심 원 x²+y²=r², 접선 y=x+a, y=x/5+b(모두 원 아래쪽에서 접함), 접점 P₁, P₂, 각 α"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+접선 2개 도형 / 첨자 점 라벨(P₁, P₂) 각 기호 텍스트 처리",
    note="OP₁ 기울기 -1, OP₂ 기울기 -5 → tanα=|(-1+5)/(1+5)|=2/3 → ②. 빠른정답 32와 불일치.")

add(id="2e1223c3", qtype="short",
    question=("다음 그림과 같이 중심이 점 [[A(2, 0)]]이고 반지름의 길이가 2인 원 C₁과 중심이 점 [[B(-3, 0)]]이고 반지름의 길이가 3인 원 C₂가 있다. "
              "[[y]]축 위의 점 [[P(0, a)]] ([[a > 3]])에서 원 C₁에 그은 접선 중 [[y]]축이 아닌 직선이 원 C₁과 접하는 점을 Q, "
              "원 C₂에 그은 접선 중 [[y]]축이 아닌 직선이 원 C₂와 접하는 점을 R라 하고 [[angle(RPQ) = theta]]라 하자.\n"
              "[[tan(theta) = frac(3,4)]]일 때, [[pow(a,2) - 15a]]의 값을 구하시오."),
    choices=None, derived_answer="6",
    figure=UNS("좌표평면: x축 위 중심 A(2,0) 반지름 2 원 C₁, B(-3,0) 반지름 3 원 C₂(원점에서 외접), y축 위 점 P에서 두 원에 그은 접선, 접점 Q, R, 각 θ"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원 2개+접선 도형 / 첨자 라벨(C₁, C₂) 텍스트 처리",
    note="출처 [2019년 4월 고3 이과 29번 변형]. tan(θ/2)=5a/(a²-6)=1/3 → a²-15a=6. 빠른정답 3과 불일치.")

add(id="0182200a", qtype="short",
    question=("그림과 같이 좌표평면 위의 제2사분면에 있는 점 A를 지나고 기울기가 각각 [[sub(m,1)]], [[sub(m,2)]] ([[0 < sub(m,1) < sub(m,2) < 1]])인 두 직선을 [[sub(l,1)]], [[sub(l,2)]]라 하고, "
              "직선 [[sub(l,1)]]을 [[y]]축에 대하여 대칭이동한 직선을 [[sub(l,3)]]이라 하자.\n"
              "직선 [[sub(l,3)]]이 두 직선 [[sub(l,1)]], [[sub(l,2)]]과 만나는 점을 각각 B, C라 하면 삼각형 ABC가 다음 조건을 만족시킨다.\n"
              "(가) [[seg(AB) = 12]], [[seg(AC) = 9]]\n(나) 삼각형 ABC의 외접원의 반지름의 길이는 [[frac(15,2)]]이다.\n"
              "[[78 sub(m,1) sub(m,2)]]의 값을 구하시오."),
    choices=None, derived_answer="18",
    figure=UNS("좌표평면: 제2사분면 점 A를 지나는 직선 l₁, l₂, l₁을 y축 대칭한 l₃, 교점 B(y축 위), C, 삼각형 ABC"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 직선 3개+삼각형 좌표평면 도형",
    note="출처 [2022년 4월 고3 미적분 29번/4점]. sinB=3/5, sinC=4/5(C 둔각), tanA=7/24; tanB=2m₁/(1-m₁²)=3/4 → m₁=1/3, m₂=9/13 → 78m₁m₂=18. 빠른정답 1과 불일치.")

add(id="88632709", qtype="choice",
    question=("점 O를 중심으로 하고 반지름의 길이가 각각 1, 2인 두 원 C₁, C₂가 있다. 원 C₁ 위의 두 점 P, Q와 원 C₂ 위의 점 R에 대하여 [[angle(QOP) = alpha]], [[angle(ROQ) = beta]]라 하자.\n"
              "[[perp(seg(OQ), seg(QR))]]이고 [[sin(alpha) = frac(sqrt(3),3)]]일 때, [[cos(alpha + beta)]]의 값은?\n"
              "(단, [[0 < alpha < frac(pi,2)]], [[0 < beta < frac(pi,2)]])"),
    choices=["[[frac(sqrt(3) - 3, 6)]]", "[[frac(sqrt(6) - sqrt(3), 6)]]", "[[frac(sqrt(6) - 3, 6)]]", "[[frac(sqrt(6) - 2 sqrt(3), 6)]]", "[[frac(sqrt(6) - 3 sqrt(2), 6)]]"],
    derived_answer="③",
    figure=UNS("동심원 C₁(반지름 1), C₂(반지름 2), C₁ 위 점 P(오른쪽), Q, C₂ 위 점 R, 각 α=∠QOP, β=∠ROQ, Q에서 직각 표시(OQ⊥QR)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 동심원+삼각형 도형 / 첨자 라벨(C₁, C₂) 텍스트 처리",
    note="출처 [2017년 3월 고3 이과 10번 변형]. cosβ=1/2, cosα=√6/3 → cos(α+β)=(√6-3)/6 → ③. 빠른정답 15와 불일치.")
