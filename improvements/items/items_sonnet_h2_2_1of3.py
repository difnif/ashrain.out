# -*- coding: utf-8 -*-
# esc_sonnet_h2-2_1of3 — 이미지 기준 전사 (82 항목 / 80쪽, 수학II: 접선의 방정식·정적분·함수의 극한·도함수·평균값 정리)
# 표기 관행: 도함수 적용 f′(x)는 prime(f)(x)로 씀(파서는 곱으로 해석) → needs_review 표시.
#            조각적 정의 { … (조건) ; … (조건) }는 텍스트 혼합 → needs_review 표시.
#            정보를 담은 기하 도형·그래프는 unsupported(raw 설명) + needs_review.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

PW = "문법 범위 밖: 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사"
PR = "문법 범위 밖: 도함수 적용 표기 f′(x)를 prime(f)(x)로 전사(파서는 곱으로 해석)"
CH_G1 = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"]
CH_G2 = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
CH_G3 = ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ═══════════════════════════ 접선의 방정식 ═══════════════════════════
# p12 — 접선의 기울기의 최댓값
add(id="c973d111", qtype="choice",
    question=("곡선 [[y = -pow(x,3) + 6 pow(x,2) - 4x + 12]]의 접선의 기울기의\n"
              "최댓값이 [[k]], 이때의 접점의 좌표를 [[point(a, b)]]라 할 때,\n"
              "[[a + b + k]]의 값은?"),
    choices=["[[10]]", "[[20]]", "[[30]]", "[[40]]", "[[50]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="y′=−3x²+12x−4, x=2에서 최댓값 8, 접점 (2,20) → 2+20+8=30 → ③ = 빠른정답 ✓. 출처 머리말 없음.")

# p25 — 접선과 수직인 직선 (빈칸 과정형)
add(id="d0adff9f", qtype="choice",
    question=("서로 다른 두 점에서 만나는 두 곡선\n"
              "[[sub(C,1)]]: [[y = pow(x,2) - 2x + 2]], [[sub(C,2)]]: [[y = -pow(x,2) + a x + b]]\n"
              "의 한 교점을 P라 하고, 점 P에서 두 곡선 [[sub(C,1)]], [[sub(C,2)]]에\n"
              "접하는 직선을 각각 [[l]], [[m]]이라 하자.\n"
              "두 접선 [[l]], [[m]]이 서로 수직일 때, 곡선 [[sub(C,2)]]는\n"
              "두 실수 [[a]], [[b]]의 값에 관계없이 일정한 점 Q를 지난다.\n"
              "다음은 점 Q의 좌표를 구하는 과정이다.\n"
              "[[f(x) = pow(x,2) - 2x + 2]], [[g(x) = -pow(x,2) + a x + b]]라\n"
              "하고, 두 곡선 [[sub(C,1)]], [[sub(C,2)]]의 한 교점 P의 [[x]]좌표를\n"
              "[[t]]라 하자.\n"
              "두 접선 [[l]], [[m]]이 서로 수직이므로\n"
              "[[prime(f)(t) prime(g)(t) = -1]]에서\n"
              "[[4 pow(t,2) - 2(a + 2) t]] + ((가)) = 0 ⋯⋯ ㉠\n"
              "[[f(t) = g(t)]]에서\n"
              "[[2 pow(t,2) - (a + 2) t + 2 - b = 0]] ⋯⋯ ㉡\n"
              "㉠, ㉡에서 [[b]] = ((나)) − [[a]]를\n"
              "[[y = -pow(x,2) + a x + b]]에 대입하고\n"
              "[[a]]에 관하여 정리하면,\n"
              "[[a(x - 1) - pow(x,2) - y]] + ((나)) = 0 ⋯⋯ ㉢\n"
              "㉢에서 [[x - 1 = 0]], [[-pow(x,2) - y]] + ((나)) = 0을\n"
              "만족시키는 [[x]]와 [[y]]의 값을 구하면 점 Q의 좌표는\n"
              "(1, (다))이다.\n"
              "위의 (가)에 알맞은 식을 [[h(a)]]라 하고, (나)와 (다)에\n"
              "알맞은 수를 각각 [[alpha]], [[beta]]라 할 때, [[h(alpha) × h(beta)]]의 값은?"),
    choices=["[[4]]", "[[8]]", "[[12]]", "[[16]]", "[[20]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PR + " / 빈칸 상자 (가)(나)(다)는 텍스트 조각 전사",
    note="출처 [2016년 10월 고3 문과 18번/4점]. (가)=2a−1, (나)=5/2, (다)=3/2 → h(5/2)·h(3/2)=4·2=8 → ② = 빠른정답 ✓.")

# p76 — 공통인 접선 (그래프 도형)
add(id="c873de45", qtype="choice",
    question=("다음 그림과 같이 두 곡선\n"
              "[[y = pow(x,2) + 1]], [[y = -pow(x,2) + 4x - 1]]\n"
              "이 한 점에서 접하고, 이 점에서 두 곡선에 공통인\n"
              "접선을 [[l]]이라 하자. 직선 [[l]]에 수직이고 두 곡선에\n"
              "접하는 직선을 각각 [[m]], [[n]]이라 하고,\n"
              "직선 [[m]], [[n]]의 접점을 각각 A, B라고 할 때, 선분\n"
              "[[seg(AB)]]의 중점의 좌표는?"),
    choices=["[[point(frac(1,2), 1)]]", "[[point(1, 2)]]", "[[point(frac(5,4), frac(5,4))]]",
             "[[point(frac(3,2), frac(3,2))]]", "[[point(frac(5,2), frac(5,2))]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y=x²+1(아래로 볼록)과 y=−x²+4x−1(위로 볼록)이 한 점에서 접함, 공통접선 l, l에 수직인 접선 m(접점 A, y=x²+1 위)·n(접점 B, y=−x²+4x−1 위), 직각 표시, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 두 포물선·공통접선·수직 접선 좌표평면 그래프",
    note="접점 (1,2), l 기울기 2 → m,n 기울기 −1/2: A(−1/4,17/16), B(9/4,47/16) → 중점 (1,2) → ②. 빠른정답 '-2'와 불일치(정렬 의심). 출처 머리말 없음.")

# p79 — 두 곡선의 교점에서의 접선
add(id="2a69f954", qtype="choice",
    question=("두 곡선 [[y = f(x)]], [[y = g(x)]]가 점 [[point(2, 2k)]] ([[k != 0]])에서\n"
              "만나고, 이 점에서의 접선은 서로 수직이다.\n"
              "곡선 [[y = f(x) pow(g(x), 2)]] 위의 점 [[point(2, 8 pow(k,3))]]에서의 접선의\n"
              "방정식이 [[y = 8 pow(k,3)]]일 때, [[2 prime(g)(2) - prime(f)(2)]]의 값은?\n"
              "(단, [[prime(f)(2) < prime(g)(2)]])"),
    choices=["[[frac(sqrt(2), 2)]]", "[[sqrt(2)]]", "[[frac(3 sqrt(2), 2)]]", "[[2 sqrt(2)]]", "[[frac(5 sqrt(2), 2)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PR,
    note="h′(2)=4k²f′(2)+8k²g′(2)=0 → f′(2)=−2g′(2), f′g′=−1 → g′(2)=√2/2, f′(2)=−√2 → 2g′−f′=2√2 → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p80 — 조각 정의 사차함수의 접선 (2024년 10월 고3 14번 변형)
add(id="622556dc", qtype="choice",
    question=("최고차항의 계수가 1인 사차함수 [[f(x)]]에 대하여\n"
              "함수 [[g(x)]] = { [[f(x + 1) - 3]] ([[x < -1]]) ; [[f(x)]] ([[x >= -1]]) }은 실수 전체의\n"
              "집합에서 미분가능하고, 곡선 [[y = g(x)]] 위의\n"
              "점 [[point(0, g(0))]]에서의 접선의 방정식이 [[y = 3x + 2]]이다.\n"
              "[[prime(g)(t) = 3]]인 서로 다른 모든 실수 [[t]]의 값의 합은?"),
    choices=["[[-5]]", "[[-frac(11,2)]]", "[[-6]]", "[[-frac(13,2)]]", "[[-7]]"],
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PW + " / " + PR,
    note="출처 [2024년 10월 고3 14번 변형]. f(0)=2, f′(0)=3, f(−1)=−1, f′(−1)=3 → f=x⁴+2x³+x²+3x+2; f′(t)=3 ⇔ t=0,−1/2,−1, x<−1 쪽 t=−3/2,−2 → 합 −5 → ① = 빠른정답 ✓.")

# p83 — 두 곡선의 교점에서의 접선 (단답)
add(id="6b1b4cd4", qtype="short",
    question=("두 곡선 [[y = pow(x,2) - 1]], [[y = a pow(x,2) + 2x + 3]]의 한 교점에서\n"
              "각각의 곡선에 그은 접선을 각각 [[sub(l,1)]], [[sub(l,2)]]라 하자.\n"
              "[[sub(l,1)]], [[sub(l,2)]]의 기울기를 각각 [[sub(m,1)]], [[sub(m,2)]]라 할 때,\n"
              "[[sub(m,1) - sub(m,2) = 6]]을 만족시키는 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.9,
    note="교점 x=t: 2t−(2at+2)=6 → t(1−a)=4, (1−a)t²−2t−4=0 → t=2, a=−1 = 빠른정답 ✓. 출처 머리말 없음.")

# p87 — 접선과 좌표축으로 둘러싸인 도형 (정사각형·포물선 그림)
add(id="7c2a4433", qtype="short",
    question=("다음 그림과 같이 정사각형 ABCD의 꼭짓점 A, C는\n"
              "[[y]]축 위에 있고, 꼭짓점 B, D는 [[x]]축 위에 있다.\n"
              "[[seg(AB)]], [[seg(AD)]]가 각각 곡선 [[y = -pow(x,2) + 4]]에 접할 때,\n"
              "사각형 ABCD의 넓이를 구하시오."),
    choices=None, derived_answer="frac(289,8)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y=−x²+4(꼭짓점 (0,4) 표시), 정사각형 ABCD(A: y축 위쪽, C: y축 아래쪽, B: x축 왼쪽, D: x축 오른쪽, 대각선 교점 원점 O) 초록 음영, 변 AB·AD가 포물선에 접함"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 정사각형 좌표평면 그림",
    note="A(0,a): 직선 y=−x+a가 접함 → 판별식 1−4(a−4)=0 → a=17/4, 넓이 2a²=289/8 = 빠른정답 ✓. 출처 머리말 없음.")

# p94 — 접선의 방정식의 활용 (2018년 11월 고2 이과 18번 변형, 그래프 도형)
add(id="b586b0b1", qtype="choice",
    question=("다음 그림과 같은 좌표평면에서 곡선 [[y = frac(1,2) pow(x,2)]] 위의\n"
              "점 [[P(t, frac(1,2) pow(t,2))]] ([[0 < t < 1]])에서의 접선 [[l]]이 [[x]]축과 만나는\n"
              "점을 Q, 점 P에서 [[x]]축에 내린 수선의 발을 R라 할 때,\n"
              "삼각형 PQR의 넓이를 [[f(t)]]라 하자. 또한, 점 P를 지나고\n"
              "기울기가 [[-1]]인 직선 [[m]]이 곡선 [[y = sqrt(2x)]]와 만나는 점을\n"
              "A라 할 때, 선분 PA를 대각선으로 하는\n"
              "정사각형 PCAB의 넓이를 [[g(t)]]라 하자.\n"
              "이때 [[lim(t, 0, frac(t × g(t), f(t)), +)]]의 값은?"),
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=½x²와 y=√(2x)(서로 역함수 관계), 점 P에서의 접선 l(x축과 Q에서 만남), 수선의 발 R(직각 표시), 직각삼각형 PQR 하늘색 음영, P를 지나는 기울기 −1 직선 m, 정사각형 PCAB 초록 음영(A는 y=√(2x) 위), 원점 O"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 두 곡선·접선·정사각형 좌표평면 그림",
    note="출처 [2018년 11월 고2 이과 18번 변형]. Q(t/2,0), f=t³/8; A(t²/2,t)(y=x 대칭), g=(t−t²/2)² → t·g/f=8(1−t/2)² → 8 → ④. 빠른정답 38과 불일치.")

# ═══════════════════════════ 정적분 ═══════════════════════════
# p5 — 정적분의 정의
add(id="e1a54691", qtype="short",
    question="[[dinteg(5, 5, 2 pow(x,3) - 3 pow(x,2) + 7, x)]]의 값을 구하시오.",
    choices=None, derived_answer="0", figure=None, difficulty_est=1, confidence=0.9,
    note="위끝과 아래끝이 같으므로 0. 빠른정답 없음. 출처 머리말 없음.")

# p7 — 미적분의 기본정리
add(id="6fb0e06b", qtype="short",
    question=("함수 [[f(x) = 10 pow(x,2) - 8x + 3]]에 대하여\n"
              "정적분 [[dinteg(0, 3, pow(x,2) f(x), x)]]의 값을 구하시오."),
    choices=None, derived_answer="351", figure=None, difficulty_est=1, confidence=0.9,
    note="∫₀³(10x⁴−8x³+3x²)dx = [2x⁵−2x⁴+x³]₀³ = 486−162+27 = 351. 빠른정답 없음. 출처 머리말 없음.")

# p8 — 미적분의 기본정리
add(id="fc00eeda", qtype="choice",
    question=("함수 [[f(x) = pow(x,2) + 7x + 4]]일 때,\n"
              "정적분 [[dinteg(0, 1, pow(x,3) f(x), x)]]의 값은?"),
    choices=["[[frac(71,30)]]", "[[frac(73,30)]]", "[[frac(5,2)]]", "[[frac(77,30)]]", "[[frac(79,30)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="∫₀¹(x⁵+7x⁴+4x³)dx = 1/6+7/5+1 = 77/30 → ④. 빠른정답 없음. 출처 머리말 없음.")

# p9 — 미적분의 기본정리
add(id="7921391c", qtype="short",
    question=("이차함수 [[f(x) = a pow(x,2) + b x + c]]에 대하여\n"
              "[[y = f(x)]]의 그래프가 두 점 [[point(0, -3)]], [[point(3, 0)]]을 지나고\n"
              "[[dinteg(0, 1, f(x), x) = -frac(4,3)]]일 때, 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.9,
    note="c=−3, 3a+b=1, a/3+b/2−3=−4/3 → 2a+3b=10 → a=−1. 빠른정답 없음. 출처 머리말 없음.")

# p11 — 미적분의 기본정리
add(id="05205f61", qtype="short",
    question="[[dinteg(2, -1, 4 pow(x,3) - 3 pow(x,2) + 2x, x)]]의 값을 구하시오.",
    choices=None, derived_answer="-9", figure=None, difficulty_est=1, confidence=0.9,
    note="[x⁴−x³+x²]₂^(−1) = 3−12 = −9 = 빠른정답 ✓. 출처 머리말 없음.")

# p12 — 기본정리의 활용 (삼차함수 그래프, 2012년 10월 고3 문과 10번)
add(id="11e9e6b6", qtype="choice",
    question=("그림과 같이 삼차함수 [[y = f(x)]]가\n"
              "[[f(-1) = f(1) = f(2) = 0]], [[f(0) = 2]]\n"
              "를 만족시킬 때, [[dinteg(0, 2, prime(f)(x), x)]]의 값은?"),
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 삼차함수 y=f(x) 그래프 — x절편 −1, 1, 2, y절편 2(x=0 부근에서 극대), 1과 2 사이에서 극소, 원점 O"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 삼차함수 그래프 / " + PR,
    note="출처 [2012년 10월 고3 문과 10번/3점]. ∫₀²f′(x)dx = f(2)−f(0) = 0−2 = −2 → ① = 빠른정답 ✓.")

# p13 — 기본정리의 활용 (id 2개, 같은 문항)
dup(["049ea740", "155ec2c3"], qtype="choice",
    question=("이차함수 [[f(x) = a pow(x,2) + b x]]가 다음 조건을 모두 만족할 때,\n"
              "[[f(-2)]]의 값은? (단 [[a]], [[b]]는 상수이다.)\n"
              "(가) [[lim(x, 2, frac(f(x) - f(2), pow(x,2) - 4)) = 1]]\n"
              "(나) [[dinteg(0, 2, f(x), x) = frac(16,3)]]"),
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[2]]", "[[4]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="(가) f′(2)/4=1 → 4a+b=4; (나) 8a/3+2b=16/3 → 4a+3b=8 → a=1/2, b=2 → f(−2)=2−4=−2 → ①. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p18 — 적분 구간이 같은 경우
add(id="56435942", qtype="short",
    question=("[[dinteg(1, 3, 6 pow(x,2) + 3x - 4, x) - dinteg(1, 3, 3x + 2, x)]]의 값을\n"
              "구하시오."),
    choices=None, derived_answer="40", figure=None, difficulty_est=1, confidence=0.9,
    note="∫₁³(6x²−6)dx = [2x³−6x]₁³ = 36−(−4) = 40. 빠른정답 0과 불일치. 출처 머리말 없음.")

# p26 — 구간에 따라 다르게 정의된 함수
add(id="2434071b", qtype="choice",
    question=("함수 [[f(x)]] = { [[pow(x + 1, 2)]] ([[x >= 1]]) ; [[frac(9,2) x - frac(1,2)]] ([[x < 1]]) }에 대하여\n"
              "정적분 [[dinteg(0, 2, f(x), x)]]의 값은?"),
    choices=["[[frac(97,12)]]", "[[frac(49,6)]]", "[[frac(33,4)]]", "[[frac(25,3)]]", "[[frac(101,12)]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="∫₀¹(9x/2−1/2)dx=7/4, ∫₁²(x+1)²dx=19/3 → 97/12 → ①. 빠른정답 16과 불일치. 출처 머리말 없음.")

# p27 — 구간에 따라 다르게 정의된 함수
add(id="e5ddcb85", qtype="short",
    question=("함수 [[f(x)]] = { [[7x]] ([[x >= 2]]) ; [[3 pow(x,2) + 2]] ([[x <= 2]]) }에 대하여\n"
              "[[dinteg(0, a, f(x), x) = 54]]를 만족시키는 상수 [[a]]의 값을 구하시오.\n"
              "(단, [[a > 2]])"),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="∫₀²(3x²+2)dx=12, 12+7(a²−4)/2=54 → a²=16 → a=4 = 빠른정답 ✓. 출처 머리말 없음.")

# p29 — 절댓값 최댓값 함수의 정적분
add(id="2b112c91", qtype="choice",
    question=("함수 [[f(x) = pow(x,3) - 12x - 8]]에 대하여\n"
              "[[-2 <= x <= t]]에서 [[abs(f(x))]]의 최댓값을 [[g(t)]]라고 할 때,\n"
              "정적분 [[dinteg(-2, 2, g(t), t)]]는? (단, [[t >= -2]])"),
    choices=["[[44]]", "[[48]]", "[[52]]", "[[56]]", "[[60]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="f(−2)=8, |f|가 다시 8이 되는 x=0 → g(t)=8 (−2≤t≤0), g(t)=−f(t) (0≤t≤2) → 16+36=52 → ③. 빠른정답 1과 불일치. 출처 머리말 없음.")

# p30 — 조건으로 정의된 주기함수의 정적분
add(id="f3e04e06", qtype="choice",
    question=("닫힌 구간 [[itv(0, 1, cc)]]에서 연속인 함수 [[f(x)]]가\n"
              "[[f(0) = 0]], [[f(1) = 1]], [[dinteg(0, 1, f(x), x) = frac(1,3)]]을 만족시킨다.\n"
              "실수 전체의 집합에서 정의된 함수 [[g(x)]]가 다음 조건을\n"
              "만족시킬 때, [[dinteg(1, 6, g(x), x)]]의 값은?\n"
              "(가) [[g(x)]] = { [[-f(x - 1) + 1]] ([[1 < x < 2]]) ; [[f(x)]] ([[0 <= x <= 1]]) }\n"
              "(나) 모든 실수 [[x]]에 대하여 [[g(x - 2) = g(x)]]이다."),
    choices=["[[frac(5,3)]]", "[[2]]", "[[frac(7,3)]]", "[[frac(8,3)]]", "[[3]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PW,
    note="∫₁²g=1−1/3=2/3, 한 주기 ∫₀²g=1 → ∫₁⁶g = 2/3+2 = 8/3 → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p35 — 절댓값 정적분 조건 (2015년 11월 고3 문과 29번)
add(id="9e3c9070", qtype="short",
    question=("이차함수 [[f(x)]]가 [[f(0) = 0]]이고 다음 조건을 만족시킨다.\n"
              "(가) [[dinteg(0, 2, abs(f(x)), x) = -dinteg(0, 2, f(x), x) = 4]]\n"
              "(나) [[dinteg(2, 3, abs(f(x)), x) = dinteg(2, 3, f(x), x)]]\n"
              "[[f(5)]]의 값을 구하시오."),
    choices=None, derived_answer="45", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2015년 11월 고3 문과 29번/4점]. f=ax(x−2) (a>0), −4a/3=−4 → a=3 → f(5)=45. 빠른정답 5와 불일치(자릿수 누락 의심).")

# p39 — 정적분의 계산(5) (2023년 3월 고3 20번 변형)
add(id="1beeedb3", qtype="short",
    question=("최고차항의 계수가 2이고 [[f(0) = 0]]인 삼차함수 [[f(x)]]와\n"
              "양의 실수 [[p]]에 대하여 함수 [[g(x)]]가 다음 조건을\n"
              "만족시킨다.\n"
              "(가) [[prime(g)(0) = 0]]\n"
              "(나) [[g(x)]] = { [[f(x - p) - f(-p)]] ([[x < 0]]) ; [[f(x + p) - f(p)]] ([[x >= 0]]) }\n"
              "[[dinteg(0, 2p, g(x), x) = 96]]일 때, [[f(4)]]의 값을 구하시오."),
    choices=None, derived_answer="80", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PR + " / " + PW,
    note="출처 [2023년 3월 고3 20번 변형]. f′(p)=f′(−p)=0 → f=2x³−6p²x; ∫₀^(2p)g=24p⁴=96 → p²=2 → f(4)=128−48=80 = 빠른정답 ✓.")

# p41 — 정적분의 계산(5) (2023년 3월 고3 20번)
add(id="28aaa2cc", qtype="short",
    question=("최고차항의 계수가 1이고 [[f(0) = 1]]인 삼차함수 [[f(x)]]와\n"
              "양의 실수 [[p]]에 대하여 함수 [[g(x)]]가 다음 조건을\n"
              "만족시킨다.\n"
              "(가) [[prime(g)(0) = 0]]\n"
              "(나) [[g(x)]] = { [[f(x - p) - f(-p)]] ([[x < 0]]) ; [[f(x + p) - f(p)]] ([[x >= 0]]) }\n"
              "[[dinteg(0, p, g(x), x) = 20]]일 때, [[f(5)]]의 값을 구하시오."),
    choices=None, derived_answer="66", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PR + " / " + PW,
    note="출처 [2023년 3월 고3 20번/4점]. f=x³−3p²x+1; ∫₀^p g=5p⁴/4=20 → p=2 → f(5)=125−60+1=66 = 빠른정답 ✓.")

# p47 — 우함수·기함수의 정적분
add(id="d5b788c1", qtype="short",
    question=("[[dinteg(-a, a, 3 pow(x,3) - 5x + 6, x) = 36]]일 때, 상수 [[a]]의 값을\n"
              "구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="기함수 항 소거 → 12a=36 → a=3 = 빠른정답 ✓. 출처 머리말 없음.")

# p48 — 사차함수 도함수의 정적분 <보기> (2018년 11월 고2 이과 17번)
add(id="5a4dc8e1", qtype="choice",
    question=("최고차항의 계수가 양수인 사차함수 [[f(x)]]의\n"
              "도함수 [[prime(f)(x)]]에 대하여 방정식 [[prime(f)(x) = 0]]이\n"
              "세 실근 [[alpha]], 0, [[beta]] ([[alpha < 0 < beta]])를 갖는다.\n"
              "[[S = dinteg(alpha, 0, abs(prime(f)(x)), x)]], [[T = dinteg(0, beta, abs(prime(f)(x)), x)]]\n"
              "라 할 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 함수 [[f(x)]]는 [[x = 0]]에서 극댓값을 갖는다.\n"
              "ㄴ. [[alpha + beta = 0]]이면 [[S = T]]이다.\n"
              "ㄷ. [[S < T]]이고 [[f(alpha) = 0]]이면 방정식 [[f(x) = 0]]의\n"
              "양의 실근의 개수는 2이다."),
    choices=CH_G2, derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PR,
    note="출처 [2018년 11월 고2 이과 17번/4점]. ㄱ 극소·극대·극소 구조 ✓, ㄴ f 우함수 → S=T ✓, ㄷ f(α)=0(중근), f(0)>0, f(β)<0 → 양의 실근 2개 ✓ → ⑤. 빠른정답 162와 불일치(정렬 의심).")

# p49 — 우함수·기함수 (피적분함수 미지)
add(id="c538bfb1", qtype="short",
    question=("다항함수 [[f(x)]]와 그 도함수 [[prime(f)(x)]]가 임의의 실수 [[a]]에\n"
              "대하여 두 등식 [[dinteg(-a, a, f(x), x) = 8a]],\n"
              "[[prime(f)(-a) = prime(f)(a)]]를 만족한다. 이때 [[f(0)]]의 값을\n"
              "구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PR,
    note="f′ 우함수 → f=기함수+c, ∫₋ₐᵃf=2ac=8a → c=f(0)=4. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p55 — 주기함수의 정적분
add(id="d844400d", qtype="choice",
    question=("연속함수 [[f(x)]]가 모든 실수 [[x]]에 대하여\n"
              "[[f(x + 5) = f(x)]], [[dinteg(1, 6, f(x), x) = 10]]을 만족시킬 때,\n"
              "정적분 [[dinteg(1, 21, f(x), x)]]의 값은?"),
    choices=["[[10]]", "[[20]]", "[[30]]", "[[40]]", "[[50]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="주기 5, 구간 길이 20 = 4주기 → 40 → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p57 — 주기함수의 정적분 (조각 정의)
add(id="6d5c2d3c", qtype="short",
    question=("실수 전체의 집합에서 정의된 연속함수 [[f(x)]]가\n"
              "임의의 실수 [[x]]에 대하여 [[f(x) = f(x + 4)]]를\n"
              "만족시키고 [[f(x)]] = { [[-4x + 8]] ([[0 <= x < 2]]) ; [[pow(x,2) - 2x]] ([[2 <= x < 4]]) }일 때,\n"
              "정적분 [[dinteg(9, 11, f(x), x)]]의 값을 구하시오."),
    choices=None, derived_answer="frac(10,3)", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="∫₉¹¹f=∫₁³f = ∫₁²(−4x+8)+∫₂³(x²−2x) = 2+4/3 = 10/3 = 빠른정답 ✓. 출처 머리말 없음.")

# p58 — 주기함수의 정적분 (그래프 도형 + 조각 정의)
add(id="809ad3b9", qtype="choice",
    question=("함수 [[f(x)]]는 모든 실수 [[x]]에 대하여\n"
              "[[f(x + 3) = f(x)]]를 만족시키고\n"
              "[[f(x)]] = { [[2x]] ([[0 <= x < 1]]) ; [[2]] ([[1 <= x < 2]]) ; [[-2x + 6]] ([[2 <= x < 3]]) }이다.\n"
              "[[dinteg(-a, a, f(x), x) = 18]]일 때, 상수 [[a]]의 값은?"),
    choices=["[[7]]", "[[10]]", "[[14]]", "[[16]]", "[[18]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 주기 3인 사다리꼴 톱니 모양 그래프 y=f(x)(높이 2, y=2 점선), x축 눈금 −5~5, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=PW + " / 도형 표현 불가: 주기함수 그래프",
    note="한 주기 넓이 4, ∫₋₆⁶f=16, 나머지 2(a−6)²=2 → a=7 → ①. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p60 — 정적분을 포함한 등식(1)
add(id="3d0d66d6", qtype="choice",
    question=("다항함수 [[f(x)]]가 [[f(x) = 3 pow(x,2) + dinteg(0, 2, (2x - 1) f(t), t)]]를\n"
              "만족시킬 때, [[f(1)]]의 값은?"),
    choices=["[[-9]]", "[[-7]]", "[[-5]]", "[[-3]]", "[[-1]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="k=∫₀²f → f=3x²+(2x−1)k, k=8+2k → k=−8 → f(1)=3−8=−5 → ③ = 빠른정답 ✓. 출처 머리말 없음.")

# p61 — 정적분을 포함한 등식(1)
add(id="8063e29a", qtype="short",
    question=("두 함수 [[f(x)]], [[g(x)]]가 [[f(x) = 3 pow(x,2) + x + dinteg(0, 2, f(t), t)]],\n"
              "[[g(x) = 2 pow(x,2) + 2x - 4]]일 때, [[f(x) < g(x)]]를 만족시키는\n"
              "모든 자연수 [[x]]의 값의 합을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="k=10+2k → k=−10, f=3x²+x−10; f<g ⇔ x²−x−6<0 ⇔ −2<x<3 → 1+2=3 = 빠른정답 ✓. 출처 머리말 없음.")

# p62 — 정적분을 포함한 등식(1)
add(id="452bd19f", qtype="choice",
    question=("함수 [[f(x)]]에 대하여 [[f(x) = x - a + 2 dinteg(0, 1, pow(f(t), 2), t)]]가\n"
              "성립할 때, 상수 [[a]]의 최솟값은?"),
    choices=["[[frac(11,24)]]", "[[frac(13,24)]]", "[[frac(5,8)]]", "[[frac(17,24)]]", "[[frac(19,24)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="f=x+c, c=−a+2(c²+c+1/3) → a=2c²+c+2/3 ≥ 13/24 (c=−1/4) → ②. 빠른정답 279와 불일치. 출처 머리말 없음.")

# p63 — 정적분을 포함한 등식(2)
add(id="c9ca6d5c", qtype="choice",
    question=("모든 실수 [[x]]에 대하여 다항함수 [[f(x)]]가\n"
              "[[pow(x,2) f(x) = 3 pow(x,5) - 2 pow(x,4) + 2 dinteg(1, x, t f(t), t)]]를 만족시킬 때,\n"
              "[[f(-1)]]의 값은?"),
    choices=["[[-15]]", "[[-13]]", "[[-11]]", "[[-9]]", "[[-7]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="양변 미분: x²f′=15x⁴−8x³ → f′=15x²−8x, f(1)=1 → f=5x³−4x² → f(−1)=−9 → ④. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p65 — 정적분을 포함한 등식(2)
add(id="dada4e4c", qtype="short",
    question=("임의의 실수 [[x]]에 대하여 다항함수 [[f(x)]]가\n"
              "[[dinteg(0, x, f(t), t) = frac(16,3) pow(x,3) - 9 pow(x,2) + 4x dinteg(0, 1, t f(t), t)]]를\n"
              "만족시킬 때, [[dinteg(0, 1, t f(t), t) + f(1)]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.9,
    note="k=∫₀¹tf → f=16x²−18x+4k, k=4−6+2k → k=2, f(1)=6 → 8 = 빠른정답 ✓. 출처 머리말 없음.")

# p68 — 정적분을 포함한 등식(2)
add(id="1f7ebb6a", qtype="short",
    question=("[[f(x) = dinteg(0, x, pow(t,2) + 2t, t)]]일 때, [[f(0) + prime(f)(0)]]의 값을\n"
              "구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PR,
    note="f(0)=0, f′(x)=x²+2x → f′(0)=0 → 0. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p69 — 정적분을 포함한 등식(3)
add(id="b76514e7", qtype="short",
    question=("[[dinteg(2, x, (x - t) f(t), t) = pow(x,3) + a pow(x,2) + 4]]을 만족하는\n"
              "미분가능한 함수 [[f(x)]]에 대하여 [[f(2) = b]]라 할 때,\n"
              "상수 [[a]], [[b]]의 합 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.85,
    note="x=2 대입 → 8+4a+4=0 → a=−3; 두 번 미분 f(x)=6x+2a=6x−6 → b=f(2)=6 → a+b=3. 빠른정답 21과 불일치. 출처 머리말 없음.")

# p75 — 정적분으로 정의된 함수의 극대·극소 (삼차함수 그래프)
add(id="240e7fc7", qtype="choice",
    question=("삼차함수 [[y = f(x)]]의 그래프가 다음 그림과 같을 때,\n"
              "[[g(x) = dinteg(2, x, f(t), t)]]는 [[x = alpha]]에서 극댓값을 갖는다.\n"
              "[[alpha + g(alpha)]]의 값은?"),
    choices=["[[22]]", "[[frac(68,3)]]", "[[frac(70,3)]]", "[[24]]", "[[frac(74,3)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 삼차함수 y=f(x) 그래프 — x절편 −5, −2, 2, y절편 −10(원점 오른쪽에서 극소), −5와 −2 사이에서 극대, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼차함수 그래프",
    note="f=½(x+5)(x+2)(x−2), g′=f 부호 +→− 인 α=−2, g(−2)=−∫₋₂²f=80/3 → −2+80/3=74/3 → ⑤. 빠른정답 21과 불일치. 출처 머리말 없음.")

# p84 — 정적분으로 정의된 함수의 최대·최소 (조각 정의 + 그래프)
add(id="2eb718f6", qtype="short",
    question=("구간 [[itv(0, 4, cc)]]에서 정의된 함수 [[f(x)]]는\n"
              "[[f(x)]] = { [[-x(x - 2)]] ([[0 <= x < 2]]) ; [[x - 2]] ([[2 <= x <= 4]]) } 이다.\n"
              "실수 [[a]] ([[0 <= a <= 2]])에 대하여 [[dinteg(a, a + 2, f(x), x)]]의\n"
              "최솟값은 [[frac(q,p)]] 이다. [[p + q]]의 값을 구하시오.\n"
              "(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="13",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — 0≤x<2에서 위로 볼록한 포물선 호(0, 2에서 0), 2≤x≤4에서 (2,0)부터 (4,2)까지 직선, 점선 눈금 2, 4, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=PW + " / 도형 표현 불가: 조각 함수 그래프",
    note="F(a)=∫ₐ^(a+2)f, F′(a)=f(a+2)−f(a)=a²−a → a=1에서 최소, ∫₁³f=2/3+1/2=7/6 → p+q=13. 빠른정답 1과 불일치. 출처 머리말 없음.")

# p90 — 정적분으로 정의된 함수의 그래프 <보기>
add(id="f804e357", qtype="choice",
    question=("연속함수 [[f(x)]]에 대하여 [[F(x) = dinteg(0, x, f(t), t)]]일 때,\n"
              "[[x >= 0]]에서 [[y = F(x)]]의 그래프는 아래 그림과 같다.\n"
              "다음 보기 중 항상 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(x) = 0]]을 만족시키는 [[x]]의 값은\n"
              "[[sub(x,1)]], [[sub(x,3)]], [[sub(x,5)]], [[sub(x,7)]]이다.\n"
              "ㄴ. [[f(sub(x,2)) f(sub(x,8)) > 0]]\n"
              "ㄷ. [[x > sub(x,7)]]일 때, [[f(x) > 0]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=F(x) 그래프(x≥0) — x₁에서 극대, x₂ x절편, x₃ 극소, x₄ x절편, x₅ 극대, x₆ x절편, x₇ 극소, x₈ x절편 후 급증가; 극점에서 x축까지 점선, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정적분으로 정의된 함수의 그래프",
    note="F′=f: ㄱ 극점 x₁,x₃,x₅,x₇ ✓, ㄴ f(x₂)<0<f(x₈) → 음수 ✗, ㄷ x>x₇에서 F 증가 ✓ → ③. 빠른정답 1과 불일치. 출처 머리말 없음.")

# p96 — 정적분으로 정의된 함수의 극한(1)
add(id="1c7791ac", qtype="short",
    question=("[[lim(h, 0, frac(1,h) dinteg(-1, -1 + h, a x - 3 pow(x,2), x)) = -5]]를 만족시키는\n"
              "상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.85,
    note="극한값 = 피적분함수의 x=−1 값 = −a−3 = −5 → a=2. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p99 — 정적분으로 정의된 함수의 극한(2): 같은 이미지에 별개 문항 2개 (위: Σ 단답, 아래: 선택형)
add(id="5416c5da", qtype="short",
    question="[[sum(k, 1, 15, lim(x, 1, frac(1, x - 1) dinteg(1, x, 2t(k - t), t)))]]의 값을 구하시오.",
    choices=None, derived_answer="210", figure=None, difficulty_est=3, confidence=0.85,
    note="각 항 = 피적분함수의 t=1 값 2(k−1) → 2·(0+1+…+14)=210. 빠른정답 2와 불일치. 같은 이미지 위쪽 문항. 출처 머리말 없음.")

add(id="5d823975", qtype="choice",
    question=("[[lim(x, 2, frac(1, pow(x,2) - 4) dinteg(2, x, (4x - t)(pow(t,2) + a t), t)) = 36]]일 때,\n"
              "상수 [[a]]의 값은?"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="G(x)=4x∫₂ˣ(t²+at)dt−∫₂ˣt(t²+at)dt, G′(2)=6(4+2a); 극한 G′(2)/4=6+3a=36 → a=10 → ⑤. 빠른정답 2와 불일치. 같은 이미지 아래쪽 문항. 출처 머리말 없음.")

# ═══════════════════════════ 함수의 극한 ═══════════════════════════
# p22 — 극한값의 존재 (계단 그래프 + 조각 정의)
add(id="681d7fb8", qtype="short",
    question=("함수 [[y = f(x)]]의 그래프가 그림과 같다.\n"
              "함수 [[g(x)]] = { [[x]] ([[x < 2]]) ; [[0]] ([[x = 2]]) ; [[2x - 6]] ([[x > 2]]) }에 대하여\n"
              "[[lim(x, a, (f(x) - 3) × g(a))]]의 값이 존재하도록 하는 모든\n"
              "양수 [[a]]의 값의 합을 구하시오."),
    choices=None, derived_answer="5",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — x<a에서 y=a+1 수평(x=a에서 열린 점), x≥a에서 y=−a 수평(x=a에서 닫힌 점), x=a 점선, y축 눈금 a+1·−a, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review=PW + " / 도형 표현 불가: 계단형 함수 그래프",
    note="양수 a에서 lim f 존재 불가(a+1≠−a) → g(a)=0 필요: a=2(정의), a=3(2a−6=0) → 합 5. 빠른정답 27과 불일치. 출처 머리말 없음.")

# p27 — 극한값의 존재
add(id="2d675887", qtype="short",
    question=("함수 [[f(x)]] = { [[4 - x]] ([[abs(x) >= 2]]) ; [[10 - pow(x,2)]] ([[abs(x) < 2]]) }에 대하여\n"
              "[[lim(x, a, f(x))]]의 값이 존재하지 않을 때, 상수 [[a]]의 값을\n"
              "구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="x=2: 2≠6 불연속, x=−2: 6=6 → a=2 = 빠른정답 ✓. 출처 머리말 없음.")

# p43 — 극한값 구하기 (그래프, 2018년 11월 고2 이과 4번)
add(id="c5defce5", qtype="choice",
    question=("함수 [[y = f(x)]]의 그래프가 그림과 같다.\n"
              "[[lim(x, 0, f(x), -) + lim(x, 1, f(x), +)]]의 값은?"),
    choices=["[[-1]]", "[[0]]", "[[1]]", "[[2]]", "[[3]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — x<0에서 기울기 −1 직선((−1,0) 지나 (0,−1) 열린 점), (0,2) 닫힌 점, 0<x<1에서 (0,0) 열린 점부터 (1,1) 열린 점까지 증가 곡선, (1,0) 닫힌 점, x>1에서 (1,2) 열린 점부터 감소 곡선((2,0) 지남), 점선 눈금 1, 2"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프",
    note="출처 [2018년 11월 고2 이과 4번/3점]. −1+2=1 → ③. 빠른정답 5와 불일치.")

# p47 — 소수 개수 함수의 극한 (2010년 6월 고3 이과 24번)
add(id="8360295b", qtype="short",
    question=("[[x]]가 양수일 때, [[x]]보다 작은 자연수 중에서\n"
              "소수의 개수를 [[f(x)]]라 하고, 함수 [[g(x)]]를\n"
              "[[g(x)]] = { [[f(x)]] ([[x > 2 f(x)]]) ; [[frac(1, f(x))]] ([[x <= 2 f(x)]]) }라고 하자.\n"
              "예를 들어, [[f(frac(7,2)) = 2]]이고 [[frac(7,2) < 2 f(frac(7,2))]]이므로\n"
              "[[g(frac(7,2)) = frac(1,2)]]이다. [[lim(x, 8, g(x), +) = alpha]], [[lim(x, 8, g(x), -) = beta]]라고\n"
              "할 때, [[frac(alpha, beta)]]의 값을 구하시오."),
    choices=None, derived_answer="16", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PW,
    note="출처 [2010년 6월 고3 이과 24번]. x→8⁺: f=4, x>8 → g=4; x→8⁻: f=4, x≤8 → g=1/4 → 16 = 빠른정답 ✓.")

# p48 — 기함수·주기함수 그래프의 극한
add(id="f7873339", qtype="choice",
    question=("함수 [[f(x)]]의 그래프는 [[0 <= x <= 3]]에서 다음 그림과\n"
              "같고, 함수 [[f(x)]]는 모든 실수 [[x]]에 대하여\n"
              "[[f(-x) = -f(x)]]와 [[f(x - 3) = f(x + 3)]]를\n"
              "만족시킨다. 이때 [[lim(x, 101, f(x), -) + f(100)]]의 값은?"),
    choices=["[[-3]]", "[[-1]]", "[[0]]", "[[1]]", "[[3]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 0≤x≤3에서 y=f(x) — 원점 닫힌 점, (0,−1) 열린 점에서 (1,0) 닫힌 점까지 증가 곡선, (1,1) 열린 점에서 (2,2)까지 증가 후 (3,1) 열린 점까지 감소하는 꺾은선, 점선 눈금 1, 2, 3"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프",
    note="주기 6·기함수: f(100)=f(4)=f(−2)=−f(2)=−2, lim x→101⁻ = lim x→−1⁻ f = −lim u→1⁺ f(u) = −1 → −3 → ①. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p53 — 접선의 개수 함수의 극한 <보기>
add(id="cb34a45f", qtype="choice",
    question=("좌표평면 위의 점 [[point(t, 0)]]에서 원 [[pow(x,2) + pow(y,2) - 2y - 3 = 0]]에\n"
              "그은 접선의 개수를 [[f(t)]]라 할 때, |보기|에서 옳은 것만을\n"
              "있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(0) = 0]]\n"
              "ㄴ. [[lim(t, sqrt(3), f(t))]]의 값이 존재한다.\n"
              "ㄷ. [[lim(t, sqrt(3), f(pow(t,2)), -) = 2]]"),
    choices=CH_G1, derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="원 중심 (0,1), 반지름 2: |t|<√3 → 0, |t|=√3 → 1, |t|>√3 → 2. ㄱ✓ ㄴ(0≠2)✗ ㄷ t²→3⁻>√3 → 2 ✓ → ④. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p56 — 두 정사각형과 직선의 교점 개수 (좌표평면 도형)
add(id="8b8a446a", qtype="short",
    question=("다음 그림과 같이 대각선의 중심이 [[point(-2, -2)]]이고\n"
              "한 변의 길이가 [[2 sqrt(2)]]인 정사각형을 [[sub(R,1)]], 대각선의\n"
              "중심이 [[point(3, 3)]]이고 한 변의 길이가 [[3 sqrt(2)]]인 정사각형을\n"
              "[[sub(R,2)]]라 하자. 점 [[P(-10, -4)]]를 지나고 기울기가 [[t]]인\n"
              "직선 [[l]]이 두 정사각형 [[sub(R,1)]], [[sub(R,2)]]와 만나는 서로 다른\n"
              "점의 개수를 [[f(t)]]라 하자. [[lim(t, a, f(t), +) != lim(t, a, f(t), -)]]를\n"
              "만족시키는 실수 [[a]]의 값을 작은 것부터 차례대로\n"
              "[[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,n)]]이라 할 때, [[13n]]([[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,n)]])의\n"
              "값을 구하시오.\n"
              "(단, [[sub(R,1)]], [[sub(R,2)]]의 두 꼭짓점은 각각 [[x]]축 또는 [[y]]축 위에 있다.)"),
    choices=None, derived_answer="82",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 마름모꼴로 놓인 정사각형 R₁(중심 (−2,−2), 꼭짓점이 축 위)과 R₂(중심 (3,3)), 점 P(−10,−4)에서 출발해 두 정사각형을 지나는 직선 l, 점선 눈금 −10, −2, 3(x축)·3, −2, −4(y축), 원점 O"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 두 정사각형과 직선 좌표평면 그림",
    note="P와 꼭짓점을 잇는 직선 중 정사각형의 지지선(한 점 접촉)인 경우만 불연속: a=0, 4/13, 1/2, 10/13 → n=4, 합 41/26 → 13·4·41/26=82. 빠른정답 4와 불일치(다음 문항 답과 정렬 어긋남 의심). 출처 머리말 없음.")

# p57 — 두 정사각형과 직선의 교점 개수 (좌표평면 도형)
add(id="433741f4", qtype="short",
    question=("다음 그림과 같이 대각선의 중심이 [[point(1, -1)]]이고\n"
              "한 변의 길이가 [[sqrt(2)]]인 정사각형을 [[sub(R,1)]], 대각선의 중심이\n"
              "[[point(-2, 2)]]이고 한 변의 길이가 [[2 sqrt(2)]]인 정사각형을\n"
              "[[sub(R,2)]]라 하자. 점 [[P(5, -2)]]를 지나고 기울기가 [[t]]인\n"
              "직선 [[l]]이 두 정사각형 [[sub(R,1)]], [[sub(R,2)]]와 만나는 서로 다른\n"
              "점의 개수를 [[f(t)]]라 하자. [[lim(t, a, f(t), +) != lim(t, a, f(t), -)]]를\n"
              "만족시키는 실수 [[a]]의 값을 작은 것부터 차례대로\n"
              "[[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,n)]]이라 할 때,\n"
              "[[-7n]]([[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,n)]])의 값을 구하시오.\n"
              "(단, [[sub(R,1)]], [[sub(R,2)]]의 두 꼭짓점은 각각 [[x]]축 또는 [[y]]축 위에 있다.)"),
    choices=None, derived_answer="46",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 마름모꼴 정사각형 R₂(중심 (−2,2), 큰 것)와 R₁(중심 (1,−1), 작은 것), 점 P(5,−2)에서 왼쪽 위로 뻗는 직선 l, 점선 눈금 −2, 1, 5(x축)·2, −1, −2(y축), 원점 O"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 두 정사각형과 직선 좌표평면 그림",
    note="지지선이 되는 기울기 a=−6/7, −1/2, −2/7, 0 → n=4, 합 −23/14 → −28·(−23/14)=46 = 빠른정답 ✓. 출처 머리말 없음.")

# p59 — 극한값 구하기 (그래프, 2022년 6월 고3 4번 변형)
add(id="e9e52fa4", qtype="choice",
    question=("함수 [[y = f(x)]]의 그래프가 다음 그림과 같다.\n"
              "[[lim(x, 0, f(x), +) + lim(x, 2, f(x), -)]]의 값은?"),
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — x<0에서 기울기 −1 직선((−2,0) 지나 (0,−2) 열린 점), 0≤x<1에서 y=2 수평((0,2) 닫힌 점, (1,2) 열린 점), (1,−2) 닫힌 점, 1<x<2에서 (1,1) 열린 점부터 (2,0) 열린 점까지 감소 직선(계속 감소), (2,1) 닫힌 점, 점선 눈금"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프",
    note="출처 [2022년 6월 고3 4번 변형]. lim x→0⁺=2, lim x→2⁻=0 → 2 → ⑤. 빠른정답 82와 불일치.")

# p60 — 소수 개수 함수의 극한 (변형)
add(id="459a0665", qtype="short",
    question=("[[x]]가 양수일 때, [[x]]보다 작은 자연수 중에서\n"
              "소수의 개수를 [[f(x)]]라 하고, 함수 [[g(x)]]를\n"
              "[[g(x)]] = { [[2 f(x)]] ([[x > 2 f(x)]]) ; [[frac(1, 2 f(x))]] ([[x <= 2 f(x)]]) }라고 하자.\n"
              "예를 들어 [[f(frac(9,2)) = 2]]이고 [[frac(9,2) > 2 f(frac(9,2))]]이므로\n"
              "[[g(frac(9,2)) = 4]]이다. [[lim(x, 6, g(x), +) = alpha]], [[lim(x, 6, g(x), -) = beta]]라고\n"
              "할 때, [[frac(alpha, beta)]]의 값을 구하시오."),
    choices=None, derived_answer="36", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PW,
    note="x→6⁺: f=3, x>6 → g=6; x→6⁻: f=3, x≤6 → g=1/6 → 36. 빠른정답 46과 불일치. 출처 머리말 없음.")

# p67 — 절댓값 기호를 포함한 함수의 극한
add(id="579487f9", qtype="short",
    question=("함수 [[f(x)]] = { [[abs(3x - 9)]] ([[x >= 1]]) ; [[-4 pow(x,2) + 2]] ([[x < 1]]) }에 대하여\n"
              "[[lim(x, 1, f(x), -) + lim(x, 1, f(x), +) + lim(x, 5, f(x))]]의 값을 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PW,
    note="−2+6+6=10 = 빠른정답 ✓. 출처 머리말 없음.")

# p69 — 절댓값 그래프와 직선의 교점 개수 함수의 극한
add(id="f640f333", qtype="short",
    question=("두 함수 [[f(x) = abs(pow(x,2) - 1) + 2]], [[g(x) = -abs(pow(x,2) - 1) - 2]]\n"
              "에 대하여 점 [[P(-2, 0)]]을 지나고 기울기가 [[a]]인 직선과\n"
              "함수 [[y = f(x)]] 또는 함수 [[y = g(x)]]의 그래프가\n"
              "[[x > -2]]에서 만나는 점의 개수를 [[h(a)]]라 하자.\n"
              "이때, [[lim(a, k, h(a), +) + lim(a, k, h(a), -) = 2]]를 만족시키는\n"
              "실수 [[k]]의 개수를 구하시오. (단, [[a]]는 실수이다.)"),
    choices=None, derived_answer=None, figure=None, difficulty_est=4, confidence=0.85,
    note="답 미도출(직선과 두 절댓값 그래프의 교점 개수 분석 필요). 빠른정답 4. 출처 머리말 없음.")

# p70 — 절댓값 그래프와 직선의 교점 개수 함수의 극한
add(id="a6e90b49", qtype="short",
    question=("두 함수 [[f(x) = abs(pow(x,2) - 1) + 4]],\n"
              "[[g(x) = -abs(pow(x,2) - 1) - 4]]에 대하여 점 [[P(-3, 0)]]을 지나고\n"
              "기울기가 [[a]]인 직선과 함수 [[y = f(x)]] 또는\n"
              "함수 [[y = g(x)]]의 그래프가 [[x > -3]]에서 만나는 점의\n"
              "개수를 [[h(a)]]라 하자. 이때\n"
              "[[lim(a, k, h(a), +) + lim(a, k, h(a), -) = 2]]를 만족시키는\n"
              "실수 [[k]]의 개수를 구하시오. (단, [[a]]는 실수이다.)"),
    choices=None, derived_answer=None, figure=None, difficulty_est=4, confidence=0.85,
    note="답 미도출(직선과 두 절댓값 그래프의 교점 개수 분석 필요). 빠른정답 2. 출처 머리말 없음.")

# p77 — 절댓값 기호를 포함한 함수의 극한
add(id="c6260038", qtype="short",
    question=("[[lim(x, -1, frac(pow(x,2) + x, abs(pow(x,2) - 1)), +) = a]], [[lim(x, 0, frac(x + abs(x), x), +) = b]]라 할 때,\n"
              "실수 [[a]], [[b]]에 대하여 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.85,
    note="x→−1⁺: |x²−1|=1−x² → x/(1−x) → −1/2=a; x→0⁺: 2x/x=2=b → ab=−1. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p82 — 합성함수의 극한 (그래프)
add(id="44207ab9", qtype="choice",
    question=("함수 [[y = f(x)]]의 그래프가 다음 그림과 같을 때,\n"
              "[[lim(x, 0, f(x - 1), -) + lim(x, -1, f(-x), -)]]의 값은?"),
    choices=["[[-3]]", "[[-2]]", "[[0]]", "[[2]]", "[[3]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — x<−1에서 y=2 수평((−1,2) 열린 점), (−1,−1) 닫힌 점, −1<x<1에서 (−1,2)부터 원점 지나 (1,−2)까지 기울기 −2 직선, (1,1) 닫힌 점, x>1에서 y=−2 수평((1,−2) 열린 점), 점선 눈금 −1, 1, 2, −2"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프",
    note="x−1→−1⁻ → 2; −x→1⁺ → −2 → 합 0 → ③. 빠른정답 311과 불일치. 출처 머리말 없음.")

# p84 — 합성함수의 극한 <보기> (그래프)
add(id="26657195", qtype="choice",
    question=("함수 [[y = f(x)]]의 그래프가 그림과 같을 때, 다음 보기 중\n"
              "옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[lim(x, -1, f(f(x)), +) = 1]]\n"
              "ㄴ. [[lim(x, 1, f(f(x)), -) = 2]]\n"
              "ㄷ. [[lim(x, 0, f(f(x)), +) = 1]]"),
    choices=CH_G3, derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — x≤−1에서 y=2 수평((−1,2) 닫힌 점), (−1,1) 열린 점에서 (0,2) 닫힌 점까지 증가, (0,3) 열린 점에서 (1,2) 닫힌 점까지 감소, (1,1) 열린 점에서 (2,2)까지 증가 후 (3,1) 열린 점까지 감소, x≥3에서 y=3 수평((3,3) 닫힌 점), 점선 눈금 1, 2, 3"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프",
    note="ㄱ f(x)→1⁺, f(1⁺)=1 ✓; ㄴ f(x)→2⁺, f(2⁺)=2 ✓; ㄷ f(x)→3⁻, f(3⁻)=1 ✓ → ⑤. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p86 — 합성함수의 극한 (그래프)
add(id="990980bd", qtype="choice",
    question=("함수 [[y = f(x)]]의 그래프가 아래의 그림과 같을 때,\n"
              "[[f(2) = a]], [[lim(x, 3, f(x), +) = b]], [[lim(x, 2, f(f(x))) = c]] 일 때,\n"
              "[[a + b + c]]의 값을 구하면?"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — x<1에서 감소 곡선이 (1,1) 닫힌 점에 도달, (1,1)에서 (2,3) 열린 점까지 증가 직선, (2,1) 닫힌 점, (2,3) 열린 점에서 (3,2) 열린 점까지 감소 직선, x≥3에서 y=3 수평((3,3) 닫힌 점), 점선 눈금 1, 2, 3"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프",
    note="a=1, b=3, x→2에서 f(x)→3⁻ → f(3⁻)=2=c → 6 → ①. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p91 — 합성함수의 극한 (그래프)
add(id="fb425853", qtype="choice",
    question=("함수 [[y = f(x)]]의 그래프가 다음 그림과 같고,\n"
              "함수 [[g(x) = pow(x + 3, 2)]]일 때,\n"
              "[[lim(x, 0, g(f(x)), +) + lim(x, -1, g(f(x)), -)]]의 값은?"),
    choices=["[[15]]", "[[16]]", "[[17]]", "[[18]]", "[[20]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — x<−1에서 기울기 음의 직선이 (−1,−2) 닫힌 점까지 감소, (−1,−1) 열린 점에서 원점까지 증가 직선, (0,1) 열린 점에서 (1,0) 닫힌 점까지 감소 직선, x>1에서 y=1 수평((1,1) 열린 점), 점선 눈금 −1, 1, −2"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프",
    note="x→0⁺: f→1 → g(1)=16; x→−1⁻: f→−2 → g(−2)=1 → 17 → ③ = 빠른정답 ✓. 출처 머리말 없음.")

# p92 — 가우스 기호 합성함수의 극한
add(id="c5fb7e4d", qtype="short",
    question=("두 함수 [[f(x) = abs(x) - 4]], [[g(x) = floor(x)]]에 대하여\n"
              "[[lim(x, -1, g(frac(1,x)), +) = lim(x, k, g(f(x)), +)]]\n"
              "를 만족시키는 모든 정수 [[k]]의 값의 합을 구하시오.\n"
              "(단, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)"),
    choices=None, derived_answer="-1", figure=None, difficulty_est=3, confidence=0.85,
    note="좌변: 1/x→−1⁻ → [−1⁻]=−2; 우변 k≥0: k−4=−2 → k=2, k<0: −k−5=−2 → k=−3 → 합 −1. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p94 — 가우스 기호 합성함수의 극한
add(id="42a1af03", qtype="short",
    question=("두 함수 [[f(x) = abs(x) - 1]], [[g(x) = floor(x)]]에 대하여\n"
              "[[lim(x, 2, g(frac(1,x)), -) = lim(x, k, g(f(x)), -)]]를 만족시키는\n"
              "모든 정수 [[k]]의 값의 곱을 구하시오.\n"
              "(단, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)"),
    choices=None, derived_answer="-2", figure=None, difficulty_est=3, confidence=0.85,
    note="좌변: 1/x→(1/2)⁺ → 0; 우변 k>0: k−2=0 → k=2, k≤0: −k−1=0 → k=−1 → 곱 −2. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p98 — 합성함수의 극한 (그래프 2개)
add(id="87d47f0e", qtype="short",
    question=("두 함수 [[y = f(x)]], [[y = g(x)]]의 그래프가 다음 그림과\n"
              "같을 때, [[lim(x, 1, g(f(x)), +) + lim(x, 2, f(g(x)), -)]]의 값을\n"
              "구하시오."),
    choices=None, derived_answer="-2",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 2개: y=f(x) — x<1에서 y=−2 수평((1,−2) 열린 점), (1,2) 닫힌 점부터 감소 직선(x=2에서 x축 통과); y=g(x) — 꼭짓점 (2,0)인 아래로 벌어진 절댓값 꼴 그래프(x≠2에서 음수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 두 함수 그래프",
    note="x→1⁺: f→2⁻ → g(2⁻)=0; x→2⁻: g→0⁻ → f(0⁻)=−2 → −2. 빠른정답 4와 불일치. 출처 머리말 없음.")

# ═══════════════════════════ 도함수 ═══════════════════════════
# p5 — 도함수의 정의 (빈칸 과정형)
add(id="bbf92e65", qtype="choice",
    question=("미분가능한 함수 [[f(x)]]에 대하여 다음은 도함수의\n"
              "정의를 이용하여 [[y = x f(x)]]의 도함수를 구하는\n"
              "과정이다.\n"
              "[[x f(x) = g(x)]]로 놓으면 [[y = g(x)]]에서\n"
              "[[prime(y) = lim(h, 0, frac(g(x + h) - g(x), h))]]\n"
              "= [[lim(h, 0, frac((x + h) f(x + h) - x f(x), h))]]\n"
              "= lim([[h]]→0) { [[(x + h)(f(x + h) - f(x))]] + ((가)) } / [[h]]\n"
              "= [[x prime(f)(x)]] + ((나))\n"
              "위의 과정에서 (가), (나)에 알맞은 것을 순서대로 적은\n"
              "것은?"),
    choices=["(가) [[-x f(x)]], (나) [[-f(x)]]", "(가) [[x f(x)]], (나) [[f(x)]]", "(가) [[-h f(x)]], (나) [[-f(x)]]",
             "(가) [[h f(x)]], (나) [[f(x)]]", "(가) [[h f(x)]], (나) [[2 f(x)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 빈칸 상자 (가)(나)가 극한식 내부에 있어 텍스트 조각 전사 / " + PR,
    note="(x+h)f(x+h)−xf(x) = (x+h){f(x+h)−f(x)}+hf(x) → (가)=hf(x), (나)=f(x) → ④. 빠른정답 6과 불일치. 출처 머리말 없음.")

# p7 — 도함수의 정의 (빈칸 채우기)
add(id="38f8fdca", qtype="short",
    question=("다음 빈 칸에 알맞은 말을 써넣으시오.\n"
              "실수 전체에서 미분가능한 함수 [[f(x)]]의 도함수는\n"
              "[[prime(f)(x)]] = lim([[h]]→0) { [[f(x + h) - f(x)]] } / (□) 이다."),
    choices=None, derived_answer="h", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 빈칸 상자가 분수의 분모 자리에 있어 텍스트 조각 전사 / " + PR,
    note="도함수의 정의에서 분모는 h. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p9 — 도함수의 정의 (x^{n+2}+x, 빈칸 과정형)
add(id="e3cded4e", qtype="choice",
    question=("다항함수 [[f(x) = pow(x, n + 2) + x]]의 도함수를 구하는 과정이다.\n"
              "[[prime(f)(x)]]\n"
              "= lim([[t]]→[[x]]) ((가)) / ([[t - x]])\n"
              "= lim([[t]]→[[x]]) [[(t - x)]]([[t]]^((나)) + [[x pow(t, n)]] + ⋯ + [[x]]^((나)) + 1) / ([[t - x]])\n"
              "= lim([[t]]→[[x]]) ([[t]]^((나)) + [[x pow(t, n)]] + ⋯ + [[x]]^((나)) + 1)\n"
              "= (다)\n"
              "위의 과정에서 (가), (나), (다)에 알맞은 것을 차례대로\n"
              "나열한 것은?"),
    choices=["[[(pow(t, n + 2) + t) - (pow(x, n + 2) + x)]], [[n + 1]], [[(n + 2) pow(x, n + 1) + 1]]",
             "[[(pow(t, n + 2) + t) - (pow(x, n + 2) + x)]], [[n + 1]], [[(n + 1) pow(x, n) + 1]]",
             "[[(pow(t, n + 2) + t) - (pow(x, n + 2) + x)]], [[n + 2]], [[(n + 2) pow(x, n + 1) + 1]]",
             "[[(pow(t, n + 2) + t) + (pow(x, n + 2) + x)]], [[n + 2]], [[(n + 1) pow(x, n) + 1]]",
             "[[(pow(t, n + 2) + t) + (pow(x, n + 2) + x)]], [[n + 2]], [[(n + 2) pow(x, n + 1) + 1]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 빈칸 상자 (나)가 지수 자리·극한식 내부에 있어 텍스트 조각 전사 / " + PR,
    note="t^(n+2)−x^(n+2)=(t−x)(t^(n+1)+xtⁿ+…+x^(n+1)) → (가)=(t^(n+2)+t)−(x^(n+2)+x), (나)=n+1, (다)=(n+2)x^(n+1)+1 → ①. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p10 — 도함수의 정의 (xⁿ+3x, 빈칸 과정형)
add(id="44859cca", qtype="choice",
    question=("다항함수 [[f(x) = pow(x, n) + 3x]]의 도함수를 구하는 과정이다.\n"
              "[[prime(f)(x)]]\n"
              "= lim([[t]]→[[x]]) ((가)) / ([[t - x]])\n"
              "= lim([[t]]→[[x]]) ((나))([[pow(t, n - 1) + x pow(t, n - 2)]] + ⋯ + [[pow(x, n - 1) + 3]]) / ([[t - x]])\n"
              "= lim([[t]]→[[x]]) ([[pow(t, n - 1) + x pow(t, n - 2)]] + ⋯ + [[pow(x, n - 1) + 3]])\n"
              "= (다)\n"
              "위의 과정에서 (가), (나), (다)에 알맞은 것을 차례대로\n"
              "나열한 것은?"),
    choices=["[[(pow(t, n) + 3t) - (pow(x, n) + 3x)]], [[t - x]], [[pow(x, n - 1) + 3]]",
             "[[(pow(t, n) + 3t) - (pow(x, n) + 3x)]], [[t - x]], [[n pow(x, n - 1) + 3]]",
             "[[(pow(t, n) + 3t) - (pow(x, n) + 3x)]], [[t + x]], [[(n - 1) pow(x, n - 1) + 1]]",
             "[[(pow(t, n) + 3t) + (pow(x, n) + 3x)]], [[t - x]], [[pow(x, n - 1) + 3]]",
             "[[(pow(t, n) + 3t) + (pow(x, n) + 3x)]], [[t + x]], [[n pow(x, n - 1) + 3]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 빈칸 상자 (가)(나)(다)가 극한식 내부에 있어 텍스트 조각 전사 / " + PR,
    note="(가)=(tⁿ+3t)−(xⁿ+3x), (나)=t−x, (다)=nx^(n−1)+3 → ② = 빠른정답 ✓. 출처 머리말 없음.")

# p16 — 관계식이 주어질 때 도함수 <보기>
add(id="73e02bc5", qtype="choice",
    question=("미분가능한 함수 [[f(x)]]가 임의의 두 실수 [[x]], [[y]]에 대하여\n"
              "[[f(x + y) = f(x) + f(y) + 6 x y]]를 만족하고\n"
              "[[prime(f)(0) = 3]]일 때, 다음 보기 중 항상 옳은 것만을 있는 대로\n"
              "고른 것은?\n<보기>\n"
              "ㄱ. [[f(x) + f(-x) = 6 pow(x,2)]]\n"
              "ㄴ. [[prime(f)(x) = 6x + 3]]\n"
              "ㄷ. 모든 실수 [[a]]에 대하여 [[f(a) = lim(x, a, f(x))]]이다."),
    choices=CH_G2, derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PR,
    note="f(0)=0; ㄱ f(x)+f(−x)=f(0)+6x² ✓; ㄴ f′(x)=lim(f(h)+6xh)/h=f′(0)+6x ✓; ㄷ 미분가능→연속 ✓ → ⑤. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p17 — 관계식이 주어질 때 도함수 <보기>
add(id="7f79a860", qtype="choice",
    question=("미분가능한 함수 [[f(x)]]가 임의의 두 실수 [[x]], [[y]]에 대하여\n"
              "[[f(x + y) = f(x) + f(y) + 4 x y]]를 만족하고\n"
              "[[prime(f)(0) = 2]]일 때, 다음 보기 중 옳은 것만을 있는 대로 고른\n"
              "것은?\n<보기>\n"
              "ㄱ. [[f(x) + f(-x) = 4 pow(x,2)]]\n"
              "ㄴ. [[prime(f)(x) = -4x + 2]]\n"
              "ㄷ. 모든 실수 [[a]]에 대하여 [[f(a) = lim(x, a, f(x))]]이다."),
    choices=CH_G2, derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PR,
    note="ㄱ ✓(4x²); ㄴ f′(x)=4x+2이므로 ✗; ㄷ ✓ → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p31 — 곱의 미분법
add(id="21474587", qtype="choice",
    question=("함수 [[f(x) = pow(3 pow(x,2) + 2x, 3)]]에 대하여 [[prime(f)(-1) + prime(f)(1)]]의\n"
              "값은?"),
    choices=["[[574]]", "[[578]]", "[[581]]", "[[584]]", "[[588]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PR,
    note="f′=3(3x²+2x)²(6x+2): f′(1)=3·25·8=600, f′(−1)=3·1·(−4)=−12 → 588 → ⑤ = 빠른정답 ✓. 출처 머리말 없음.")

# p71 — 접선의 기울기를 이용한 미정계수
add(id="bf2965cd", qtype="choice",
    question=("함수 [[f(x) = 2 pow(x,2) + a x + 3]]에 대하여 [[y = f(x)]]의\n"
              "그래프 위의 점 [[point(1, 8)]]에서의 접선의 기울기가 [[m]]일 때,\n"
              "상수 [[a]], [[m]]에 대하여 [[a + m]]의 값은?"),
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="f(1)=5+a=8 → a=3; f′(1)=4+a=7=m → 10 → ⑤ = 빠른정답 ✓. 출처 머리말 없음.")

# p76 — 접선의 기울기를 이용한 미정계수
add(id="92034faf", qtype="short",
    question=("함수 [[f(x) = pow(x,2) - 3x]]의 그래프 위의 점 [[point(a, b)]]에서의\n"
              "접선의 기울기가 3일 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의\n"
              "값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="2a−3=3 → a=3, b=9−9=0 → 3 = 빠른정답 ✓. 출처 머리말 없음.")

# ═══════════════════════════ 평균값 정리 ═══════════════════════════
# p22 — 롤의 정리
add(id="0d0621f4", qtype="choice",
    question=("함수 [[f(x) = k x - 4 pow(x,2)]]에 대하여 닫힌구간 [[itv(0, 4, cc)]]에서\n"
              "롤의 정리를 만족시키는 상수의 값이 2일 때, 상수 [[k]]의\n"
              "값은?"),
    choices=["[[12]]", "[[16]]", "[[20]]", "[[24]]", "[[28]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="f(0)=f(4) → 4k−64=0 → k=16 (f′(2)=k−16=0 ✓) → ② = 빠른정답 ✓. 출처 머리말 없음.")

# p30 — 롤의 정리 (실근 개수)
add(id="425d0d42", qtype="choice",
    question=("실수 [[sub(a,0)]], [[sub(a,1)]], ⋯, [[sub(a, n - 1)]]에 대하여 방정식\n"
              "[[pow(x, n) + sub(a, n - 1) pow(x, n - 1)]] + ⋯ + [[sub(a,1) x + sub(a,0) = 0]]의 실근의 개수가\n"
              "[[k]]개 일 때, 방정식\n"
              "[[n pow(x, n - 1) + (n - 1) sub(a, n - 1) pow(x, n - 2)]] + ⋯ + [[sub(a,1) = 0]]의 실근의\n"
              "개수는 [[m]]이다. 다음 중 옳은 것은?"),
    choices=["[[m = k]]", "[[m >= k - 1]]", "[[m = n - 1]]", "[[m < n - 1]]", "[[m = n - k]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    note="롤의 정리: 서로 다른 실근 사이마다 도함수의 실근이 적어도 하나 → m ≥ k−1 → ②. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p32 — 롤의 정리 <보기> (조각 정의)
add(id="c1be9f9d", qtype="choice",
    question=("[[f(1) - f(-1) = 2 prime(f)(c)]]를 만족시키는 [[c]]가\n"
              "열린구간 [[itv(-1, 1, oo)]]에 존재하는 함수인 것만을\n"
              "보기에서 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(x) = abs(x) - 2]]\n"
              "ㄴ. [[f(x)]] = { [[-3x - 2]] ([[x < -1]]) ; [[1]] ([[-1 <= x < 1]]) ; [[3x - 2]] ([[x >= 1]]) }\n"
              "ㄷ. [[f(x) = -pow(x,2) + 5]]"),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.8,
    needs_review=PR + " / " + PW,
    note="ㄱ f′=±1≠0 ✗; ㄴ f(1)=f(−1)=1, (−1,1)에서 f′=0 ✓; ㄷ f′(c)=−2c=0 → c=0 ✓ → ⑤. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p33 — 롤의 정리 <보기> (조각 정의)
add(id="86e470ea", qtype="choice",
    question=("함수 [[f(x)]]에 대하여 [[f(2) - f(-1) = 3 prime(f)(c)]]를\n"
              "만족시키는 [[c]]가 열린구간 [[itv(-1, 2, oo)]]에 존재하는 함수인\n"
              "것만을 보기에서 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(x) = abs(2x - 1) - 1]]\n"
              "ㄴ. [[f(x)]] = { [[-3x - 4]] ([[x <= -1]]) ; [[-1]] ([[-1 < x < 2]]) ; [[3x - 7]] ([[x >= 2]]) }\n"
              "ㄷ. [[f(x) = -pow(x,2) + x + 3]]"),
    choices=CH_G1, derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.8,
    needs_review=PR + " / " + PW,
    note="ㄱ f(2)=f(−1)=2, f′=±2≠0 ✗; ㄴ f(2)=f(−1)=−1, (−1,2)에서 f′=0 ✓; ㄷ f(2)=f(−1)=1, c=1/2 ✓ → ⑤. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p40 — 평균값 정리 (기울기 집합)
add(id="958617c4", qtype="short",
    question=("함수 [[f(x) = frac(2,3) pow(x,3) - 4 pow(x,2) + 10x]]에 대하여 집합 [[S]]를\n"
              "[[S]] = { [[a]] | [[a = frac(f(sub(x,2)) - f(sub(x,1)), sub(x,2) - sub(x,1))]], [[3 <= sub(x,1) < sub(x,2) <= 4]] }로\n"
              "정의할 때, 집합 [[S]]의 원소 [[a]]의 값의 범위는\n"
              "[[m < a < n]]이다. [[m + n]]의 값을 구하시오."),
    choices=None, derived_answer="14", figure=None, difficulty_est=3, confidence=0.85,
    note="f′=2(x−2)²+2 증가, f′(3)=4, f′(4)=10 → 4<a<10 → 14. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p42 — 롤의 정리·평균값 정리
add(id="6a2f37ec", qtype="short",
    question=("함수 [[f(x) = -pow(x,2) + 2 k x]]에 대하여 닫힌구간 [[itv(0, 4, cc)]]에서\n"
              "롤의 정리를 만족시키는 실수가 2이고,\n"
              "닫힌구간 [[itv(1, 9, cc)]]에서 평균값 정리를 만족시키는 실수를\n"
              "[[c]]라 할 때, [[k + c]]의 값을 구하시오. (단, [[k]]는 상수)"),
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.85,
    note="f(0)=f(4) → k=2; 이차함수의 평균값 정리 c=(1+9)/2=5 → 7. 빠른정답 6과 불일치. 출처 머리말 없음.")

# p47 — 평균값 정리
add(id="9ef91e12", qtype="short",
    question=("함수 [[f(x)]]는 구간 [[1 <= x <= 3]]에서 미분가능하고,\n"
              "[[f(1) = 3]], [[f(3) = 2]]이다. [[g(x) = x f(x)]]이면\n"
              "[[prime(g)(c) = k]]인 [[c]] ([[1 < c < 3]])가 존재한다.\n"
              "이때 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="frac(3,2)", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PR,
    note="g(1)=3, g(3)=6 → 평균변화율 3/2 = 빠른정답 ✓. 출처 머리말 없음.")

# p53 — 평균값 정리 (기울기 집합의 자연수 원소)
add(id="bb3efb38", qtype="choice",
    question=("함수 [[f(x) = 3 pow(x,3) - 2 pow(x,2) + 1]]에 대하여 집합 [[A]]를\n"
              "[[A]] = { [[x]] | [[x = frac(f(sub(x,2)) - f(sub(x,1)), sub(x,2) - sub(x,1))]], [[1 < sub(x,1) < sub(x,2) < 3]] }이라\n"
              "할 때, 집합 [[A]]의 자연수인 원소의 개수는?"),
    choices=["[[60]]", "[[63]]", "[[66]]", "[[69]]", "[[72]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="f′=9x²−4x 증가, f′(1)=5, f′(3)=69 → 기울기 범위 (5, 69) → 6~68의 63개 → ②. 빠른정답 5와 불일치. 출처 머리말 없음.")

# p54 — 평균값 정리 (기울기 집합의 자연수 원소)
add(id="b809b5d1", qtype="choice",
    question=("함수 [[f(x) = -pow(x,3) + 8x + 7]]에 대하여 집합 [[A]]를\n"
              "[[A]] = { [[t]] | [[t = frac(f(sub(x,2)) - f(sub(x,1)), sub(x,2) - sub(x,1))]], [[0 < sub(x,1) < sub(x,2) < 3]] }이라\n"
              "할 때, 집합 [[A]]의 자연수인 원소의 개수는?"),
    choices=["[[1]]", "[[3]]", "[[5]]", "[[7]]", "[[9]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="f′=−3x²+8 감소, f′(0)=8, f′(3)=−19 → 기울기 범위 (−19, 8) → 1~7의 7개 → ④. 빠른정답 2와 불일치. 출처 머리말 없음.")
