# -*- coding: utf-8 -*-
# esc_sonnet_h2-2_2of3 — 이미지 기준 전사 (83 항목 / 80쪽, 수학II: 평균값 정리·함수의 극한·연속·부정적분·속도와 거리·증감·그래프·넓이)
# 표기 관행: 도함수 적용 f′(x)는 prime(f)(x)로 씀(파서는 곱으로 해석) → needs_review 표시.
#            첨자 함수 적용 v₁(t)·Fₙ(x)는 sub(v,1)(t)·sub(F,n)(x)로 씀(파서는 곱으로 해석) → needs_review 표시.
#            조각적 정의 { … (조건) ; … (조건) }는 텍스트 혼합 → needs_review 표시.
#            d/dx ∫ … dx 는 dydx(integ(…, x), x)로 씀(뜻 동일, 표시만 다름).
#            정보를 담은 기하 도형·그래프는 unsupported(raw 설명) + needs_review.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

PW = "문법 범위 밖: 조각적 정의(중괄호 경우 나눔) → 텍스트 혼합 전사"
PR = "문법 범위 밖: 도함수 적용 표기 f′(x)를 prime(f)(x)로 전사(파서는 곱으로 해석)"
PS = "문법 범위 밖: 첨자 함수 적용 표기(v₁(t)·Fₙ(x) 등)를 sub(v,1)(t) 꼴로 전사(파서는 곱으로 해석)"
CH_ABC = ["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"]

# ═════════════════════════ 평균값 정리
# p73 — 그래프가 주어진 경우(보기 3개)
add(id="19250d01", qtype="choice",
    question=("[[frac(f(1) - f(-1), 2) = prime(f)(c)]]인 [[c]]가 열린구간 [[itv(-1, 1, oo)]]에\n"
              "존재하는 함수인 것만을 보기에서 있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[f(x) = -pow(x,2) abs(x)]]\n"
              "ㄴ. [[f(x) = sqrt(pow(x + 4, 2))]]\n"
              "ㄷ. [[f(x) = pow(x,2) - 2 abs(x)]]"),
    choices=CH_ABC, derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PR,
    note="ㄱ: −x²|x|는 미분가능, 평균변화율 −1 = f′(c)인 c=1/√3 ✓; ㄴ: |x+4|=x+4 ✓; ㄷ: x=0에서 미분불가, 평균변화율 0 → c=±1 구간 밖 ✗ → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p74 — 같은 틀, 보기 다름
add(id="3e73cc1a", qtype="choice",
    question=("[[frac(f(1) - f(-1), 2) = prime(f)(c)]]인 [[c]]가 열린구간 [[itv(-1, 1, oo)]]에\n"
              "존재하는 함수인 것만을 보기에서 있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[f(x) = -x abs(x)]]\n"
              "ㄴ. [[f(x) = -sqrt(x + 2)]]\n"
              "ㄷ. [[f(x) = x + sqrt(pow(x,2))]]"),
    choices=CH_ABC, derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PR,
    note="ㄱ: −x|x| 미분가능, 평균변화율 −1 = −2c → c=1/2 ✓; ㄴ: (−1,1)에서 미분가능·연속 → 평균값 정리 ✓; ㄷ: x+|x|, 평균변화율 1인데 f′는 0 또는 2 ✗ → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p75 — 조각 정의 함수의 평균값 정리 c의 개수
add(id="11ff3746", qtype="short",
    question=("[[f(x)]] = { [[pow(x,2) - 8x + 16]] ([[x >= 0]]) ; [[-pow(x,2) - 8x + 16]] ([[x < 0]]) }에 대하여\n"
              "닫힌구간 [[itv(-5, 6, cc)]]에서 평균값의 정리를 만족시키는\n"
              "상수 [[c]]의 개수를 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PW,
    note="f(−5)=31, f(6)=4, 평균변화율 −27/11; x=0에서 f′=−8로 미분가능; 2c−8=−27/11 → c=61/22, −2c−8=−27/11 → c=−61/22 → 2개. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p92 — 그래프에서 평균값 정리 c의 개수 (그래프 도형)
add(id="78ea83e8", qtype="choice",
    question=("함수 [[y = f(x)]]의 그래프가 다음 그림과 같을 때,\n"
              "[[frac(f(b) - f(a), b - a) = prime(f)(c)]]\n"
              "를 만족시키는 상수 [[c]]의 개수는? (단, [[a < c < b]])"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 곡선 y=f(x): x=a(원점 왼쪽)에서 점 찍고 올라가 극대, 내려가 극소(원점 오른쪽), 다시 올라가 극대(b 직전) 후 x=b에서 점 찍고 급감; 두 점 (a,f(a)), (b,f(b))를 잇는 직선, a·b에서 x축까지 점선"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 함수 y=f(x)의 그래프(좌표평면) / " + PR,
    note="현과 평행한 접선: 첫 증가 구간 1개 + 두 번째 증가 구간(현을 아래→위로 가로지름) 2개 = 3 → ③. 빠른정답 5와 불일치(그래프 판독 기반). 출처 머리말 없음.")

# ═════════════════════════ 함수의 극한에 대한 성질 / 극한의 활용
# p4 — 이차함수 조건 (가)(나)
add(id="8e28ad27", qtype="short",
    question=("최고차항의 계수가 양수인 이차함수 [[f(x)]]가 다음 조건을\n"
              "만족시킨다.\n"
              "(가) [[lim(x, 0, frac(sqrt(pow(x,2)) - f(x), x + f(x)), -) × lim(x, 0, frac(sqrt(pow(x,2)) - f(x), x + f(x)), +) = -2]]\n"
              "(나) [[lim(x, a, frac(f(x - 4) f(x + 1), sqrt(pow(x,2)) - 3))]]의 값이 존재하지 않는\n"
              "실수 [[a]]의 개수는 1이다.\n"
              "[[f(24)]]의 값을 구하시오."),
    choices=None, derived_answer="40", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2024년 9월 고2 28번/4점]. (가) f(0)=0, 좌극한 −1·우극한 (1−q)/(1+q) = −2 → f=px²−x/3; (나) x=−3에서는 항상 불존재 → x=3에서 존재하려면 f(4)=0 → p=1/12 → f(24)=48−8=40. 빠른정답 2와 불일치.")

# p91 — 직선 y=x+3 위의 점 P, 수선의 발 Q (좌표평면 도형)
add(id="7c03d246", qtype="choice",
    question=("다음 그림과 같이 직선 [[y = x + 3]] 위에 두 점 [[A(-3, 0)]]과\n"
              "[[P(t, t + 3)]]이 있다. 점 P를 지나고 직선 [[y = x + 3]]에\n"
              "수직인 직선이 [[y]]축과 만나는 점을 Q라 할 때,\n"
              "[[lim(t, inf, frac(pow(seg(AQ), 2), pow(seg(AP), 2)))]]의 값은?"),
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[1]]", "[[2]]", "[[4]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 직선 y=x+3(x축과 A에서 만남), 그 위의 점 P, P를 지나 y=x+3에 수직인 직선(직각 표시)이 y축과 만나는 점 Q, 선분 AQ; 원점 O 표시"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 직선·수선·점 A, P, Q가 있는 좌표평면 도형",
    note="Q=(0, 2t+3): AQ²=4t²+12t+18, AP²=2(t+3)² → 비 → 2 → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p92 — 원과 포물선, 삼각형 PAQ 넓이의 극한 (좌표평면 도형)
add(id="6e6f78c4", qtype="short",
    question=("다음 그림과 같이 좌표평면에서 원 [[pow(x,2) + pow(y,2) = 10]]과\n"
              "곡선 [[y = 3 pow(x,2)]]이 제1사분면에서 만나는 점을 A라 하자.\n"
              "이때 실수 [[t]] ([[0 < t < 3]])에 대하여 직선 [[y = t x]]가\n"
              "원 [[pow(x,2) + pow(y,2) = 10]], 곡선 [[y = 3 pow(x,2)]]과 제1사분면에서 만나는\n"
              "점을 각각 P, Q라 하자. 삼각형 PAQ의 넓이를 [[S(t)]]라\n"
              "할 때, [[lim(t, 3, frac(S(t), pow(3 - t, 2)), -) = k]]이다. [[60k]]의 값을 구하시오.\n"
              "(단, 점 O는 원점이다.)"),
    choices=None, derived_answer="19",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 제1사분면: 원 x²+y²=10, 포물선 y=3x², 직선 y=tx; 원과 포물선의 교점 A, 직선과 원의 교점 P, 직선과 포물선의 교점 Q, 삼각형 PAQ 음영, 원점 O"}}],
    difficulty_est=4, confidence=0.85,
    needs_review="도형 표현 불가: 원·포물선·직선과 삼각형 PAQ 음영이 있는 좌표평면 도형",
    note="출처 [2020년 11월 고2 28번 변형]. A=(1,3), P=(r, tr) (r=√(10/(1+t²))), Q=(t/3, t²/3); s=3−t 전개 → S ≈ (19/60)s² → k=19/60 → 60k=19 = 빠른정답 ✓.")

# p94 — 곡선 y=√(4x−3), 두 삼각형 넓이 비의 극한 (좌표평면 도형)
add(id="a62d49aa", qtype="short",
    question=("그림과 같이 곡선 [[y = sqrt(4x - 3)]] 위에 두 점 [[A(1, 1)]]과\n"
              "[[P(t, sqrt(4t - 3))]]이 있다. 점 A에서 [[x]]축에 내린\n"
              "수선의 발을 B, 점 P에서 [[y]]축에 내린 수선의 발을 Q라\n"
              "할 때, 삼각형 PAB와 삼각형 PQA의 넓이를 각각\n"
              "[[S(t)]], [[T(t)]]라 하자. [[lim(t, 1, frac(T(t), S(t)), +)]]의 값을 구하시오.\n"
              "(단, [[t > 1]])"),
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=√(4x−3) 위의 점 A와 P, A에서 x축에 내린 수선의 발 B(직각 표시), P에서 y축에 내린 수선의 발 Q(직각 표시), 삼각형 PAB와 PQA 음영, 원점 O"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 곡선과 두 삼각형(음영)이 있는 좌표평면 도형",
    note="출처 [2018년 11월 고2 문과 28번/4점]. S=(t−1)/2, T=t(√(4t−3)−1)/2 → T/S = 4t/(√(4t−3)+1) → 2. 빠른정답 4와 불일치.")

# p95 — 두 곡선 y=√5x, y=√3x와 직선 x=k (좌표평면 도형)
add(id="c462ccb8", qtype="choice",
    question=("다음 그림과 같이 두 곡선 [[y = sqrt(5x)]], [[y = sqrt(3x)]]와\n"
              "직선 [[x = k]] ([[k > 0]])의 교점을 각각 A, B라 할 때,\n"
              "[[lim(k, inf, seg(OA) - seg(OB))]]의 값은? (단, O는 원점이다.)"),
    choices=["[[frac(1,6)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]", "[[1]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 제1사분면: 원점에서 출발하는 두 곡선 y=√5x(위), y=√3x(아래), 수직선 x=k와의 교점 A(위), B(아래), 선분 OA, OB"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 두 곡선과 직선 x=k, 선분 OA·OB가 있는 좌표평면 도형",
    note="OA−OB = 2k/(√(k²+5k)+√(k²+3k)) → 1 → ⑤ = 빠른정답 ✓. 출처 머리말 없음.")

# p96 — 곡선 y=2/x와 두 직선, AB/BC 극한 (좌표평면 도형)
add(id="c6467ae7", qtype="short",
    question=("다음 그림과 같이 곡선 [[y = frac(2, x)]] ([[x > 0]])과 두 직선 [[x = 2]],\n"
              "[[x = t]]의 교점을 각각 A, B라 하고, 점 B에서 직선\n"
              "[[x = 2]]에 내린 수선의 발을 C라 하자. 이때 [[lim(t, inf, frac(seg(AB), seg(BC)))]]의\n"
              "값을 구하시오. (단, [[t > 2]])"),
    choices=None, derived_answer="1",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 제1사분면: 곡선 y=2/x, 수직선 x=2와 x=t, 교점 A(x=2 위)와 B(x=t 위), B에서 x=2에 내린 수선의 발 C(직각 표시), 원점 O"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 곡선·두 수직선·수선의 발이 있는 좌표평면 도형",
    note="A=(2,1), B=(t,2/t), C=(2,2/t): BC=t−2, AB=√((t−2)²+(1−2/t)²) → 비 → 1 = 빠른정답 ✓. 출처 머리말 없음.")

# p99 — 두 원 C₁, C₂와 직선 PQ, OR의 극한 (좌표평면 도형; 같은 쪽에 별개 문항 하나 더 인쇄됨)
add(id="32b59dd1", qtype="short",
    question=("그림과 같이 원점 O를 중심으로 하고 반지름의 길이가 [[r]]인\n"
              "원 [[sub(C,1)]]이 [[y]]축의 양의 방향과 만나는 점을 P,\n"
              "중심의 좌표가 [[point(2, 0)]]이고 반지름의 길이가 2인 원 [[sub(C,2)]]가\n"
              "[[sub(C,1)]]과 제1사분면에서 만나는 점을 Q라고 하자.\n"
              "두 점 P, Q를 지나는 직선이 [[x]]축과 만나는 점을\n"
              "R이라 할 때, [[lim(r, 0, seg(OR), +)]]의 값을 구하시오."),
    choices=None, derived_answer="8",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 중심 반지름 r인 원 C₁(y축 교점 P), 중심 (2,0) 반지름 2인 원 C₂, 두 원의 제1사분면 교점 Q, 직선 PQ가 x축과 만나는 점 R, 중심 2 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 두 원과 직선 PQ가 있는 좌표평면 도형",
    note="Q=(r²/4, r√(1−r²/16)), PQ의 x절편 = 4(√(1−r²/16)+1) → 8. 빠른정답 1과 불일치. 같은 이미지 아래에 별개 문항(포물선 y=x²/2 위의 점 P와 OP에 수직인 직선의 y절편 f(t)의 극한, 답 2)이 더 인쇄돼 있으나 id가 하나뿐이라 draft 대응대로 첫 문항만 전사. 출처 머리말 없음.")

# ═════════════════════════ 함수의 연속 (구간의 뜻)
# p1 — 두 함수의 정의역 구간 기호
add(id="a1f22e19", qtype="choice",
    question=("다음 두 함수의 정의역을 구간의 기호로 올바르게 짝지은\n"
              "것은?\n"
              "[[f(x) = abs(x) + 1]], [[g(x) = sqrt(2 - x)]]"),
    choices=["[[itv(1, inf, co)]], [[itv(-inf, 2, oo)]]",
             "[[itv(0, inf, co)]], [[itv(2, inf, oo)]]",
             "[[itv(-inf, inf, oo)]], [[itv(-inf, 2, oc)]]",
             "[[itv(1, inf, co)]], [[itv(-inf, 2, oc)]]",
             "[[itv(-inf, inf, oo)]], [[itv(2, inf, oo)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="f: 실수 전체 (−∞, ∞), g: x≤2 → (−∞, 2] → ③ = 빠른정답 ✓. 출처 머리말 없음.")

# p3 — f(x)=1/(x−6)의 정의역
add(id="8a7ea57f", qtype="choice",
    question=("다음 중 함수 [[f(x) = frac(1, x - 6)]]의 정의역을 구간의 기호로\n"
              "바르게 나타낸 것은?"),
    choices=["[[itv(-inf, -6, oo)]]",
             "[[itv(-inf, -6, oo)]], [[itv(-6, inf, oo)]]",
             "[[itv(6, inf, oo)]]",
             "[[itv(-inf, 6, oo)]], [[itv(6, inf, oo)]]",
             "[[itv(-inf, inf, oo)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="x≠6 → (−∞, 6), (6, ∞) → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p7 — x=1에서 연속인 함수 (선지에 조각 정의)
add(id="df171387", qtype="choice",
    question=("다음 중 [[x = 1]]에서 연속인 함수는?\n"
              "(단, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)"),
    choices=["[[f(x) = 4 pow(floor(x), 2)]]",
             "[[f(x) = frac(1, x - 1)]]",
             "[[f(x)]] = { [[pow(x - 1, 2)]] ([[x != 1]]) ; [[1]] ([[x = 1]]) }",
             "[[f(x)]] = { [[frac(pow(x,2) - 1, x - 1)]] ([[x != 1]]) ; [[2]] ([[x = 1]]) }",
             "[[f(x)]] = { [[frac(4 abs(x - 1), x - 1)]] ([[x != 1]]) ; [[4]] ([[x = 1]]) }"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="④: 극한 2 = f(1) ✓; ①②는 x=1에서 불연속·정의 안 됨, ③ 극한 0≠1, ⑤ 좌우극한 ∓4 → ④. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p8 — x=2에서 불연속인 함수 모두 (정답 3개) — id 2개
dup(["0c3d90f2", "159ea7cc"], qtype="choice",
    question=("다음 중 [[x = 2]]에서 불연속인 함수를 모두 고르면?\n"
              "(단, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)\n"
              "(정답 3개)"),
    choices=["[[f(x) = x abs(x - 2)]]",
             "[[f(x) = x - floor(x)]]",
             "[[f(x)]] = { [[frac(pow(x,2) + 2x - 8, pow(x,2) - 2x)]] ([[x != 2]]) ; [[3]] ([[x = 2]]) }",
             "[[f(x)]] = { [[pow(x - 2, 2) + 3]] ([[x != 2]]) ; [[2]] ([[x = 2]]) }",
             "[[f(x)]] = { [[frac(abs(x - 2), x - 2)]] ([[x != 2]]) ; [[1]] ([[x = 2]]) }"],
    derived_answer="②, ④, ⑤", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="① 연속, ② x−[x]는 정수에서 불연속, ③ 극한 (x+4)/x→3 = f(2) 연속, ④ 극한 3≠2, ⑤ 좌우극한 ∓1 → ②, ④, ⑤ (정답 3개; 빠른정답 5는 그중 하나). 출처 머리말 없음.")

# p10 — x=0에서 연속인 함수
add(id="2bfb83cb", qtype="choice",
    question="다음 중 [[x = 0]]에서 연속인 함수는?",
    choices=["[[f(x) = -frac(3, pow(x,2))]]",
             "[[f(x) = sqrt(x + 1)]]",
             "[[f(x) = frac(10, x) - 9]]",
             "[[f(x)]] = { [[frac(abs(x), x)]] ([[x != 0]]) ; [[1]] ([[x = 0]]) }",
             "[[f(x)]] = { [[pow(x,2) - 1]] ([[x >= 0]]) ; [[-pow(x,2) + 2]] ([[x < 0]]) }"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PW,
    note="②만 x=0에서 정의되고 연속 → ② = 빠른정답 ✓. 출처 머리말 없음.")

# p11 — 모든 실수에서 연속인 함수(보기)
add(id="3e19ea11", qtype="choice",
    question=("모든 실수 [[x]]에서 연속인 함수인 것만을 보기에서 있는 대로\n"
              "고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[f(x) = pow(x,2) abs(x)]]\n"
              "ㄴ. [[f(x) = frac(2 pow(x,2) + 5x - 3, x + 3)]]\n"
              "ㄷ. [[f(x)]] = { [[frac(pow(x,2) + 5x + 6, x + 2)]] ([[x != -2]]) ; [[1]] ([[x = -2]]) }"),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="ㄱ ✓, ㄴ x=−3에서 정의 안 됨 ✗, ㄷ 극한 (x+3)→1 = f(−2) ✓ → ⑤ = 빠른정답 ✓. 출처 머리말 없음.")

# p12 — 2022년 3월 고3 12번 (조각 정의 + 조건 (가)(나))
add(id="8ba42773", qtype="choice",
    question=("[[a > 2]]인 상수 [[a]]에 대하여 함수 [[f(x)]]를\n"
              "[[f(x)]] = { [[pow(x,2) - 4x + 3]] ([[x <= 2]]) ; [[-pow(x,2) + a x]] ([[x > 2]]) }라 하자.\n"
              "최고차항의 계수가 1인 삼차함수 [[g(x)]]에 대하여\n"
              "실수 전체의 집합에서 연속인 함수 [[h(x)]]가\n"
              "다음 조건을 만족시킬 때, [[h(1) + h(3)]]의 값은?\n"
              "(가) [[x != 1]], [[x != a]]일 때, [[h(x) = frac(g(x), f(x))]]이다.\n"
              "(나) [[h(1) = h(a)]]"),
    choices=["[[-frac(15,6)]]", "[[-frac(7,3)]]", "[[-frac(13,6)]]", "[[-2]]", "[[-frac(11,6)]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PW,
    note="출처 [2022년 3월 고3 12번/4점]. g=(x−1)(x−2)(x−a), h(1)=(1−a)/2=h(a)=−(a−1)(a−2)/a → a=4; h(1)=−3/2, h(3)=−2/3 → −13/6 → ③ = 빠른정답 ✓.")

# p13 — 위 문항의 변형 — id 2개
dup(["c18d0ca1", "710ca9ce"], qtype="choice",
    question=("[[a > 3]]인 상수 [[a]]에 대하여 함수 [[f(x)]]를\n"
              "[[f(x)]] = { [[pow(x,2) - 6x + 5]] ([[x <= 3]]) ; [[-pow(x,2) + a x]] ([[x > 3]]) }이라 하자.\n"
              "최고차항의 계수가 1인 삼차함수 [[g(x)]]에 대하여\n"
              "실수 전체의 집합에서 연속인 함수 [[h(x)]]가\n"
              "다음 조건을 만족시킬 때, [[h(1) + h(5)]]의 값은?\n"
              "(가) [[x != 1]], [[x != a]]일 때, [[h(x) = frac(g(x), f(x))]]이다.\n"
              "(나) [[h(1) = h(a)]]"),
    choices=["[[-frac(21,5)]]", "[[-frac(41,10)]]", "[[-4]]", "[[-frac(39,10)]]", "[[-frac(19,5)]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PW,
    note="출처 [2022년 3월 고3 12번 변형]. g=(x−1)(x−3)(x−a), h(1)=(1−a)/2=h(a)=−(a−1)(a−3)/a → a=6; h(1)=−5/2, h(5)=−8/5 → −41/10 → ② = 빠른정답 ✓.")

# p16 — x=−1에서 연속인 함수
add(id="184c1695", qtype="choice",
    question=("다음 중 [[x = -1]]에서 연속인 함수는?\n"
              "(단, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)"),
    choices=["[[f(x) = sqrt(x)]]",
             "[[f(x) = pow(floor(x), 2)]]",
             "[[f(x) = frac(2, x + 1)]]",
             "[[f(x)]] = { [[frac(3 abs(x + 1), x + 1)]] ([[x != -1]]) ; [[0]] ([[x = -1]]) }",
             "[[f(x)]] = { [[frac(pow(x,2) - 1, x + 1)]] ([[x != -1]]) ; [[-2]] ([[x = -1]]) }"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="⑤: 극한 (x−1)→−2 = f(−1) ✓; ② [x]²은 정수 −1에서 불연속 → ⑤. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p39 — 합성함수의 연속 (보기가 그래프 3개)
add(id="e22e754a", qtype="choice",
    question=("닫힌구간 [[itv(0, 4, cc)]]에서 정의된 함수 [[y = f(x)]]에 대하여\n"
              "함수 [[g(x)]]를 [[g(x)]] = { [[pow(f(x), 2)]] ([[0 <= x <= 2]]) ; ([[comp(f, f)]])([[x]]) ([[2 < x <= 4]]) }\n"
              "라 하자. 다음 보기 중 함수 [[g(x)]]가 닫힌구간 [[itv(0, 4, cc)]]에서\n"
              "불연속이 되도록 하는 함수 [[y = f(x)]]의 그래프로 옳은\n"
              "것만을 있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. (그래프 ㄱ)\n"
              "ㄴ. (그래프 ㄴ)\n"
              "ㄷ. (그래프 ㄷ)"),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "보기 그래프 3개(모두 [0,4] 위의 y=f(x), 격자 점선). ㄱ: (0,3)에서 감소해 (1,1), (2,0)에서 최소, (3,2) 극대, (4,1)까지 연속. ㄴ: (0,0)에서 (1,1) 극대, (2,0) 최소, 증가해 (3,2)(채운 점), x=3에서 (3,3) 빈 점부터 (4,4)까지 증가. ㄷ: (0,3)에서 감소해 (1,1), 1.5에서 0 최소, (2,1), (3,2)(채운 점), x=3에서 (3,3) 빈 점부터 (4,4)까지 증가"}}],
    difficulty_est=4, confidence=0.7,
    needs_review="도형 표현 불가: 보기 ㄱ·ㄴ·ㄷ가 함수 그래프 3개 / " + PW + " / 합성함수 적용 (f∘f)(x) 표기",
    note="ㄱ: x→2+에서 f(f(x))→f(0)=3 ≠ g(2)=0 불연속 ✓; ㄴ: x=3에서 g(3)=f(2)=0, 우극한 f(3+)=3 불연속 ✓; ㄷ: x=3에서 g(3)=f(2)=1, 우극한 3 불연속 ✓ → ⑤ (그래프 판독 기반, 검토 필요). 빠른정답 73은 값 아님. 출처 머리말 없음.")

# p40 — 두 조각 함수의 합성 (보기)
add(id="940a9d3b", qtype="choice",
    question=("실수 전체의 집합에서 정의된 두 함수\n"
              "[[f(x)]] = { [[2]] ([[x > -1]]) ; [[1]] ([[x = -1]]) ; [[0]] ([[x < -1]]) }, "
              "[[g(x)]] = { [[frac(abs(x + 1), x + 1)]] ([[x != -1]]) ; [[0]] ([[x = -1]]) }\n"
              "에 대하여 옳은 것만을 보기에서 있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[f(f(x))]]는 실수 전체의 집합에서 연속이다.\n"
              "ㄴ. [[lim(x, -1, f(g(x)))]]의 값이 존재한다.\n"
              "ㄷ. [[g(f(x))]]는 [[x = -1]]에서 연속이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PW,
    note="ㄱ: f(f(x))=2 상수 ✓; ㄴ: 좌극한 f(−1)=1, 우극한 f(1)=2 ✗; ㄷ: g(f(x))=1 상수 ✓ → ④. 빠른정답 5와 불일치. 출처 머리말 없음.")

# p52 — 2016년 4월 고3 문과 6번 변형
add(id="12ccfc71", qtype="choice",
    question=("함수\n"
              "[[f(x)]] = { [[a x - 9]] ([[x <= 2]]) ; [[3x - a]] ([[x > 2]]) }\n"
              "가 실수 전체의 집합에서 연속일 때, 상수 [[a]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PW,
    note="출처 [2016년 4월 고3 문과 6번 변형]. 2a−9=6−a → a=5 → ⑤ = 빠른정답 ✓.")

# p57 — 2017년 7월 고3 문과 24번 변형
add(id="8f41c800", qtype="short",
    question=("함수 [[f(x)]] = { [[-2x + 4]] ([[x < 1]]) ; [[pow(x,2) + a x - 3]] ([[x >= 1]]) }이 실수 전체의\n"
              "집합에서 연속일 때, 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PW,
    note="출처 [2017년 7월 고3 문과 24번 변형]. 2 = 1+a−3 → a=4 = 빠른정답 ✓.")

# p59
add(id="697cb4d0", qtype="choice",
    question=("함수 [[f(x)]] = { [[2 pow(x,2) - 3x + 4]] ([[x < 3]]) ; [[x + a]] ([[x >= 3]]) }이 실수 전체의\n"
              "집합에서 연속일 때, 상수 [[a]]의 값은?"),
    choices=["[[4]]", "[[6]]", "[[8]]", "[[10]]", "[[12]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PW,
    note="13 = 3+a → a=10 → ④. 빠른정답 −3과 불일치. 출처 머리말 없음.")

# p61 — 2016년 4월 고3 문과 6번
add(id="41d7b923", qtype="choice",
    question=("함수 [[f(x)]] = { [[a x - 4]] ([[x < 1]]) ; [[2x - a]] ([[x >= 1]]) }이 실수 전체의 집합에서\n"
              "연속일 때, 상수 [[a]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PW,
    note="출처 [2016년 4월 고3 문과 6번/3점]. a−4=2−a → a=3 → ③ = 빠른정답 ✓.")

# p66 — 2023년 7월 고3 14번
add(id="765905e6", qtype="choice",
    question=("최고차항의 계수가 1이고 [[f(-3) = f(0)]]인\n"
              "삼차함수 [[f(x)]]에 대하여 함수 [[g(x)]]를\n"
              "[[g(x)]] = { [[f(x)]] ([[x < -3]] 또는 [[x >= 0]]) ; [[-f(x)]] ([[-3 <= x < 0]]) }\n"
              "이라 하자. 함수 [[g(x) g(x - 3)]]이 [[x = k]]에서 불연속인\n"
              "실수 [[k]]의 값이 한 개일 때, <보기>에서 옳은 것만을 있는\n"
              "대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. 함수 [[g(x) g(x - 3)]]은 [[x = 0]]에서 연속이다.\n"
              "ㄴ. [[f(-6) × f(3) = 0]]\n"
              "ㄷ. 함수 [[g(x) g(x - 3)]]이 [[x = k]]에서 불연속인\n"
              "실수 [[k]]가 음수일 때\n"
              "집합 { [[x]] | [[f(x) = 0]], [[x]]는 실수 }의 모든 원소의\n"
              "합이 [[-1]]이면 [[g(-1) = -48]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=5, confidence=0.8,
    needs_review=PW,
    note="출처 [2023년 7월 고3 14번/4점]. c=f(0): x=0에서는 항상 연속(ㄱ ✓); 불연속 후보 x=−3(c·f(−6)≠0), x=3(c·f(3)≠0) 중 하나만 → f(−6)f(3)=0 (ㄴ ✓); k=−3이면 f(3)=0, 근의 합 −1 → f=(x−3)²(x+4) → g(−1)=−f(−1)=−48 (ㄷ ✓) → ⑤. 빠른정답 11은 값 아님.")

# p67 — 2018년 6월 고2 이과 27번
add(id="df4992ae", qtype="short",
    question=("함수\n"
              "[[f(x)]] = { [[x(x - 2)]] ([[x <= 1]]) ; [[x(x - 2) + 16]] ([[x > 1]]) }\n"
              "에 대하여 함수 [[f(x)(f(x) - a)]]가 실수 전체의 집합에서\n"
              "연속이 되도록 하는 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="14", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="출처 [2018년 6월 고2 이과 27번/4점]. f(1)=−1, f(1+)=15: (−1)(−1−a)=15(15−a) → a=14 = 빠른정답 ✓.")

# p69 — 2021년 6월 고3 8번
add(id="e94ee10e", qtype="choice",
    question=("함수 [[f(x)]] = { [[-2x + 6]] ([[x < a]]) ; [[2x - a]] ([[x >= a]]) }에 대하여\n"
              "함수 [[pow(f(x), 2)]]이 실수 전체의 집합에서 연속이 되도록\n"
              "하는 모든 상수 [[a]]의 값의 합은?"),
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="출처 [2021년 6월 고3 8번/3점]. (−2a+6)²=a² → a=2, 6 → 합 8 → ④. 빠른정답 5와 불일치.")

# p70 — f(x)g(x) 연속, a의 합
add(id="a823a7ba", qtype="short",
    question=("두 함수\n"
              "[[f(x)]] = { [[x + 2]] ([[x <= a]]) ; [[pow(x,2) + 2x]] ([[x > a]]) }, [[g(x) = x - (3a + 1)]]에\n"
              "대하여 함수 [[f(x) g(x)]]가 실수 전체의 집합에서 연속이\n"
              "되도록 하는 모든 실수 [[a]]의 값의 합을 구하시오."),
    choices=None, derived_answer="frac(-3,2)", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="g(a)=0 (a=−1/2) 또는 a+2=a²+2a (a=−2, 1) → 합 −3/2 = 빠른정답 ✓. 출처 머리말 없음.")

# p82 — 2023년 9월 고3 15번
add(id="8ae0e6db", qtype="choice",
    question=("최고차항의 계수가 1인 삼차함수 [[f(x)]]에 대하여\n"
              "함수 [[g(x)]]를\n"
              "[[g(x)]] = { [[frac(f(x + 3)(f(x) + 1), f(x))]] ([[f(x) != 0]]) ; [[3]] ([[f(x) = 0]]) }이라 하자.\n"
              "[[lim(x, 3, g(x)) = g(3) - 1]]일 때, [[g(5)]]의 값은?"),
    choices=["[[14]]", "[[16]]", "[[18]]", "[[20]]", "[[22]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PW,
    note="출처 [2023년 9월 고3 15번/4점]. f(3)=0, g(3)=3, lim g=2 → f(x+3)/f(x)→2 → f=(x−3)(x−4)(x−6) → g(5)=40·(−1)/(−2)=20 → ④. 빠른정답 80과 불일치.")

# ═════════════════════════ 연속함수의 성질 (사잇값 정리)
# p41 — 증명 과정 빈칸 (가)(나)(다)
add(id="a8c875ec", qtype="choice",
    question=("다음은 함수 [[f(x) = -pow(x,2) + 5]]에 대하여 [[f(c) = 3]]인 [[c]]가\n"
              "열린구간 [[itv(-2, 1, oo)]]에 적어도 하나 존재함을 보이는\n"
              "과정이다.\n"
              "함수 [[f(x) = -pow(x,2) + 5]]은 열린구간 [[itv(-inf, inf, oo)]]에서\n"
              "(가) 이므로 닫힌구간 [[itv(-2, 1, cc)]]에서도 (가)\n"
              "이다.\n"
              "또, [[f(-2) != f(1)]]이고\n"
              "[[f(-2) < 3 < f(1)]]이므로 (나) 의 정리에\n"
              "의하여 [[f(c) = 3]]인 [[c]]가 열린구간 [[itv(-2, 1, oo)]]에\n"
              "적어도 (다) 존재한다.\n"
              "위의 과정에서 (가), (나), (다)에 알맞은 것은?\n"
              "(가) (나) (다)"),
    choices=["연속, 평균값, 1개", "불연속, 평균값, 2개", "연속, 최대·최소, 2개", "불연속, 사잇값, 2개", "연속, 사잇값, 1개"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="연속 / 사잇값 / 1개 → ⑤ = 빠른정답 ✓. 선지는 (가),(나),(다) 순으로 콤마 나열. 출처 머리말 없음.")

# p49 — 2017년 9월 고2 문과 20번 변형
add(id="c1a1eb14", qtype="choice",
    question=("3이 아닌 양수 [[a]]에 대하여 함수\n"
              "[[f(x)]] = { [[pow(x - a, 2)]] ([[x <= a]]) ; [[(x - 3)(x - a)]] ([[x > a]]) }\n"
              "가 다음 조건을 만족시킬 때, [[f(3a)]]의 값은?\n"
              "(가) [[f(c) = 0]]인 [[c]]가 0과 [[frac(3 + a, 2)]] 사이에\n"
              "적어도 하나 존재한다.\n"
              "(나) 세 점 [[point(3, f(3))]], [[point(a, f(a))]],\n"
              "[[point(frac(3 + a, 2), f(frac(3 + a, 2)))]]를 꼭짓점으로 하는\n"
              "삼각형의 넓이는 [[frac(1,8)]] 이다."),
    choices=["[[3]]", "[[6]]", "[[12]]", "[[24]]", "[[48]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PW,
    note="출처 [2017년 9월 고2 문과 20번 변형]. (가) → a<3; f(3)=f(a)=0, f((3+a)/2)=−(3−a)²/4 → 넓이 (3−a)³/8=1/8 → a=2 → f(6)=3·4=12 → ③. 빠른정답 4와 불일치.")

# p54 — 2016년 4월 고3 문과 30번
add(id="aef686b6", qtype="short",
    question=("함수 [[f(x) = pow(x,2) - 8x + a]]에 대하여 함수 [[g(x)]]를\n"
              "[[g(x)]] = { [[2x + 5a]] ([[x >= a]]) ; [[f(x + 4)]] ([[x < a]]) }라 할 때, 다음 조건을\n"
              "만족시키는 모든 실수 [[a]]의 값의 곱을 구하시오.\n"
              "(가) 방정식 [[f(x) = 0]]은 열린 구간 [[itv(0, 2, oo)]]에서 적어도\n"
              "하나의 실근을 갖는다.\n"
              "(나) 함수 [[f(x) g(x)]]는 [[x = a]]에서 연속이다."),
    choices=None, derived_answer="56", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PW,
    note="출처 [2016년 4월 고3 문과 30번/4점]. (가) f(0)>0>f(2) → 0<a<12; (나) f(a)(a−8)(a+2)=0, f(a)=a(a−7) → a=7, 8 → 곱 56. 빠른정답 3과 불일치.")

# ═════════════════════════ 부정적분
# p9 — d/dx ∫(3x³+4x+5)dx, f′(1)
add(id="c8d5dc9d", qtype="short",
    question=("함수 [[f(x)]]에 대하여 [[f(x) = dydx(integ(3 pow(x,3) + 4x + 5, x), x)]]일\n"
              "때, [[prime(f)(1)]]의 값을 구하시오."),
    choices=None, derived_answer="13", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PR,
    note="f=3x³+4x+5, f′=9x²+4 → f′(1)=13. 빠른정답 4와 불일치. d/dx∫…dx는 dydx(integ(…,x),x)로 전사. 출처 머리말 없음.")

# p10
add(id="9c42633f", qtype="short",
    question=("함수 [[f(x)]]에 대하여 [[f(x) = dydx(integ(5 pow(x,3) + 2x + 1, x), x)]]일\n"
              "때, [[prime(f)(1)]]의 값을 구하시오."),
    choices=None, derived_answer="17", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PR,
    note="f=5x³+2x+1, f′=15x²+2 → f′(1)=17 = 빠른정답 ✓. d/dx∫…dx는 dydx(integ(…,x),x)로 전사. 출처 머리말 없음.")

# p12
add(id="f765a289", qtype="short",
    question=("함수 [[f(x)]]에 대하여\n"
              "[[dydx(integ(f(x), x), x) = 4 pow(x,2) - 9x + 11]]이 성립할 때,\n"
              "[[f(1)]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.85,
    note="f(x)=4x²−9x+11 → f(1)=6 = 빠른정답 ✓. d/dx∫f(x)dx는 dydx(integ(f(x),x),x)로 전사(뜻 동일). 출처 머리말 없음.")

# p13
add(id="1bdf9683", qtype="short",
    question=("함수 [[f(x)]]에 대하여 [[f(x) = dydx(integ(pow(x,3) - 2x + 3, x), x)]]일\n"
              "때, [[prime(f)(2)]]의 값을 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PR,
    note="f=x³−2x+3, f′=3x²−2 → f′(2)=10. 빠른정답 17과 불일치. 출처 머리말 없음.")

# p14 — 방정식의 모든 근의 합
add(id="1b507bb8", qtype="choice",
    question=("방정식\n"
              "[[dydx(integ(-3 pow(x,2) - 12x, x), x) + dydx(integ(pow(x,3) - 26x, x), x) = 0]]\n"
              "의 모든 근의 합은?"),
    choices=["[[3]]", "[[9]]", "[[15]]", "[[21]]", "[[27]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="x³−3x²−38x=x(x²−3x−38)=0 → 근의 합 0+3=3 → ① = 빠른정답 ✓. d/dx∫…dx는 dydx(integ(…,x),x)로 전사. 출처 머리말 없음.")

# p20 — g=d/dx∫f, h=∫(d/dx f)
add(id="56974752", qtype="short",
    question=("함수 [[f(x) = pow(x,2) + x]]에 대하여 두 함수 [[g(x)]], [[h(x)]]를\n"
              "[[g(x) = dydx(integ(f(x), x), x)]], [[h(x) = integ(dydx(f(x), x), x)]]로\n"
              "정의하자. [[h(2) = 3]]일 때, [[g(2) + h(3)]]의 값을 구하시오."),
    choices=None, derived_answer="15", figure=None, difficulty_est=2, confidence=0.85,
    note="g=f → g(2)=6; h=x²+x+C, h(2)=3 → C=−3 → h(3)=9 → 15. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p21 — F(x)=∫[d/dx∫{d/dx f(x)}dx]dx
add(id="e80cf744", qtype="choice",
    question=("함수 [[f(x) = 10 pow(x,10) + 9 pow(x,9)]] + ⋯ + [[2 pow(x,2) + x]]에 대하여\n"
              "[[F(x) = integ(dydx(integ(dydx(f(x), x), x), x), x)]]이고\n"
              "[[F(0) = 2]]일 때, [[F(1)]]의 값은?"),
    choices=["[[51]]", "[[53]]", "[[55]]", "[[57]]", "[[59]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="F=f+C, F(0)=C=2 → F(1)=55+2=57 → ④. 빠른정답 1과 불일치. 줄임표는 마커 밖 텍스트. 출처 머리말 없음.")

# p22 — 등식에서 f(0)
add(id="22a5425e", qtype="choice",
    question=("다항함수 [[f(x)]]에 대하여\n"
              "[[dydx(integ(f(x) - 2 pow(x,3) + 4x, x), x) = integ(dydx(2f(x) + 3 pow(x,2), x), x)]]\n"
              "가 성립한다. [[f(1) = -12]]일 때, [[f(0)]]의 값은?"),
    choices=["[[-8]]", "[[-9]]", "[[-10]]", "[[-11]]", "[[-12]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="f−2x³+4x = 2f+3x²+C → f=−2x³−3x²+4x−C, f(1)=−1−C=−12 → C=11 → f(0)=−11 → ④. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p28 — d/dx{∫xf(x)dx}
add(id="0f578bae", qtype="short",
    question=("함수 [[f(x)]]가\n"
              "[[dydx(integ(x f(x), x), x) = pow(x,5) + pow(x,4) + pow(x,3) + pow(x,2) + x]]를\n"
              "만족시킬 때, [[f(2)]]의 값을 구하시오."),
    choices=None, derived_answer="31", figure=None, difficulty_est=1, confidence=0.85,
    note="xf(x)=x⁵+…+x → f=x⁴+x³+x²+x+1 → f(2)=31. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p29 — 원점 대칭 + ∫{2f+ff′}dx 조건
add(id="1ad2af91", qtype="short",
    question=("최고차항의 계수가 양수인 다항함수 [[f(x)]]가 다음 조건을\n"
              "모두 만족할 때, [[f(a)]]의 값을 구하시오.\n"
              "(단, [[a]]는 상수이고, [[C]]는 적분상수이다.)\n"
              "(가) 함수 [[y = f(x)]]의 그래프는 원점에 대하여\n"
              "대칭이다.\n"
              "(나) [[integ(2f(x) + f(x) prime(f)(x), x) = frac(1,2) pow(x,6) - frac(7,2) pow(x,4) + a pow(x,2) + C]]"),
    choices=None, derived_answer="48", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PR,
    note="f=px³+qx: 3p²=3, 4pq+2p=−14, q²+2q=2a → p=1, q=−4, a=4 → f(4)=64−16=48. 빠른정답 3과 불일치. 출처 머리말 없음.")

# p36 — Fₙ(x)=Σ(k∫x^{k−1}dx)
add(id="34170754", qtype="choice",
    question=("함수 [[sub(F,n)(x) = sum(k, 1, n + 1, (k integ(pow(x, k - 1), x)))]]에 대하여\n"
              "[[sub(F,n)(0) = 0]]일 때, [[sub(F,n)(1)]]의 값은? (단, [[n]] = 1, 2, 3, ⋯)"),
    choices=["[[frac(n,2)]]", "[[frac(n + 1, 2)]]", "[[n - 1]]", "[[n]]", "[[n + 1]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PS,
    note="k∫x^{k−1}dx=x^k+C → Fₙ(x)=x+x²+…+x^{n+1} (C=0) → Fₙ(1)=n+1 → ⑤. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p50 — 6∫f = 2xf − 3f
add(id="95a52f80", qtype="choice",
    question=("다항함수 [[f(x)]]에 대하여\n"
              "[[6 integ(f(x), x) = 2x f(x) - 3f(x)]]가 성립하고\n"
              "[[f(0) = frac(9,4)]] 일 때, [[f(frac(1,2))]]의 값은?"),
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="미분: 4f=(2x−3)f′ → f=c(2x−3)², f(0)=9c=9/4 → c=1/4 → f(1/2)=1 → ④. 빠른정답 5와 불일치. 출처 머리말 없음.")

# p53 — Fₙ, Gₙ 수열 정의
add(id="e6324ec4", qtype="short",
    question=("함수 [[f(x) = -x + 1]]에 대하여 함수 [[sub(F,n)(x)]]는 다음 조건을\n"
              "모두 만족시킨다.\n"
              "(가) [[sub(F,1)(x) = integ(f(x), x)]], [[sub(F,1)(0) = -1]]\n"
              "(나) [[sub(F, n + 1)(x) = integ(sub(F,n)(x), x)]],\n"
              "[[sub(F, n + 1)(0) = pow(-1, n + 1)]]\n"
              "[[sub(G,n)(x) = sub(F,n)(x) + sub(F, n + 1)(x)]]일 때, [[frac(prime(sub(G,98))(1), sub(G,98)(1))]]의\n"
              "값을 구하시오. (단, [[n]] = 1, 2, 3, ⋯)"),
    choices=None, derived_answer="100", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PS + " / " + PR,
    note="Fₙ(x)=−Σ_{m=0}^{n+1}(−1)^{n+1−m}x^m/m! → Gₙ(x)=−x^{n+2}/(n+2)! → Gₙ′(1)/Gₙ(1)=n+2 → 100 (파이썬 확인). 빠른정답 4와 불일치. 출처 머리말 없음.")

# p56 — 조각 도함수에서 f(−2)
add(id="ced862e3", qtype="short",
    question=("모든 실수 [[x]]에 대하여 연속인 함수 [[f(x)]]의\n"
              "도함수 [[prime(f)(x)]]가 [[prime(f)(x)]] = { [[-2x + 1]] ([[x > 1]]) ; [[3 pow(x,2) - 4]] ([[x < 1]]) }이고\n"
              "[[f(0) = 2]]일 때, [[f(-2)]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW + " / " + PR,
    note="x<1: f=x³−4x+2 → f(−2)=−8+8+2=2. 빠른정답 100과 불일치. 출처 머리말 없음.")

# p68 — 접선의 기울기 조건
add(id="59453b4a", qtype="short",
    question=("함수 [[f(x) = integ(k pow(x,2) - 2x + 1, x)]]에 대하여\n"
              "곡선 [[y = f(x)]] 위의 점 [[point(1, 3)]]에서의 접선의 기울기가\n"
              "2일 때, [[f(3)]]의 값을 구하시오. (단, [[k]]는 상수이다.)"),
    choices=None, derived_answer="23", figure=None, difficulty_est=2, confidence=0.85,
    note="f′(1)=k−1=2 → k=3; f=x³−x²+x+C, f(1)=3 → C=2 → f(3)=23. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p79 — 증분 Δy=(ax+5)Δx−2(Δx)²
add(id="a6c6a1e3", qtype="choice",
    question=("미분가능한 함수 [[y = f(x)]]에서 [[x]]의 증분을 [[delta x]], [[delta x]]에\n"
              "대한 [[y]]의 증분을 [[delta y]]라 할 때,\n"
              "[[delta y = (a x + 5) delta x - 2 pow(delta x, 2)]]\n"
              "이 성립한다. [[f(0) = 0]], [[f(1) = 0]]일 때, [[f(2)]]의 값은?\n"
              "(단, [[delta x != 0]]이고 [[a]]는 상수이다.)"),
    choices=["[[-12]]", "[[-10]]", "[[-8]]", "[[-6]]", "[[-4]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    note="f′=ax+5 → f=ax²/2+5x, f(1)=0 → a=−10 → f(2)=−20+10=−10 → ② = 빠른정답 ✓. Δ는 delta로 전사. 출처 머리말 없음.")

# p80 — 증분 Δy=(ax+1)Δx−2(Δx)²
add(id="87d87052", qtype="choice",
    question=("미분가능한 함수 [[y = f(x)]]에서 [[x]]의 증분을 [[delta x]], [[delta x]]에\n"
              "대한 [[y]]의 증분을 [[delta y]]라 할 때,\n"
              "[[delta y = (a x + 1) delta x - 2 pow(delta x, 2)]]\n"
              "이 성립한다. [[f(0) = 0]], [[f(1) = 0]]일 때, [[f(-1)]]의 값은?\n"
              "(단, [[delta x != 0]]이고 [[a]]는 상수이다.)"),
    choices=["[[-10]]", "[[-8]]", "[[-6]]", "[[-4]]", "[[-2]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    note="f′=ax+1 → f=ax²/2+x, f(1)=0 → a=−2 → f=−x²+x → f(−1)=−2 → ⑤ = 빠른정답 ✓. Δ는 delta로 전사. 출처 머리말 없음.")

# p83 — f(x+y)=f(x)+f(y)+6xy(x+y)+1 (보기)
add(id="b2925b8a", qtype="choice",
    question=("다항함수 [[f(x)]]가 모든 실수 [[x]], [[y]]에 대하여\n"
              "[[f(x + y) = f(x) + f(y) + 6x y(x + y) + 1]]일 때, 옳은\n"
              "것만을 보기에서 있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[prime(f)(0) = f(1)]]\n"
              "ㄴ. [[prime(f)(0) = 0]]이면 함수 [[f(x)]]는 극값을 갖지\n"
              "않는다.\n"
              "ㄷ. 함수 [[f(x)]]가 극값을 가질 때, 극댓값과\n"
              "극솟값의 합은 [[-2]]이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PR,
    note="f(0)=−1, f′(x)=f′(0)+6x² → f=2x³+ax−1: ㄱ f(1)=a+1≠a ✗, ㄴ a=0이면 극값 없음 ✓, ㄷ 극값 합 = 2(x₁³+x₂³)+a(x₁+x₂)−2=−2 ✓ → ④ = 빠른정답 ✓. 출처 머리말 없음.")

# p98 — 도서관 연료 소모량 (4x+3)
add(id="30f3cf2d", qtype="choice",
    question=("어느 도서관의 온도를 [[x]] °C ([[x >= 10]])로 유지시킬 때,\n"
              "1시간당 연료 소모량은 [[y]] mL라 한다. 이 도서관의 온도를\n"
              "[[delta x]] °C만큼 높이면 1시간당 연료 소모량이 [[delta y]] mL만큼\n"
              "늘어난다고 할 때,\n"
              "[[delta y = (4x + 3) delta x + k pow(delta x, 2)]] ([[k]]는 상수)\n"
              "이 성립한다. 도서관의 온도를 20 °C로 유지시킬 때,\n"
              "1시간당 연료 소모량은?\n"
              "(단, 이 도서관의 온도가 10 °C이하일 때에는 연료 소모가\n"
              "없다.)"),
    choices=["350 mL", "420 mL", "490 mL", "560 mL", "630 mL"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    note="dy/dx=4x+3 → y=2x²+3x+C, y(10)=0 → C=−230 → y(20)=630 → ⑤. 빠른정답 23과 불일치. Δ는 delta로 전사. 출처 머리말 없음.")

# p99 — 도서관 연료 소모량 (3x+4) (같은 쪽 아래에 별개 문항 하나 더 인쇄됨)
add(id="3d1cb9f1", qtype="choice",
    question=("어느 도서관의 온도를 [[x]] °C ([[x >= 10]])으로 유지시킬 때,\n"
              "1시간당 연료 소모량은 [[y]] mL라 한다. 이 도서관의 온도를\n"
              "[[delta x]] °C만큼 높이면 1시간당 연료 소모량이 [[delta y]] mL만큼\n"
              "늘어난다고 할 때,\n"
              "[[delta y = (3x + 4) delta x + k pow(delta x, 2)]] ([[k]]는 상수)\n"
              "이 성립한다. 도서관의 온도를 20 °C로 유지시킬 때,\n"
              "1시간당 연료 소모량은?\n"
              "(단, 이 도서관의 온도가 10 °C이하일 때에는 연료 소모가\n"
              "없다.)"),
    choices=["350 mL", "420 mL", "490 mL", "560 mL", "630 mL"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="dy/dx=3x+4 → y=(3/2)x²+4x+C, y(10)=0 → C=−190 → y(20)=490 → ③. 빠른정답 410과 불일치. 같은 이미지 아래에 별개 문항(모종나무 높이 dh/dt=3.5t+5, 4년 후 60cm → 12년 후 높이, 답 324cm)이 더 인쇄돼 있으나 id가 하나뿐이라 draft 대응대로 첫 문항만 전사. 출처 머리말 없음.")

# ═════════════════════════ 속도와 거리
# p4 — 두 점 P, Q가 2번 만나는 정수 k의 개수
add(id="7a66e82f", qtype="choice",
    question=("수직선 위를 움직이는 두 점 P, Q의 시각 [[t]] ([[t > 0]])에서의\n"
              "속도를 각각 [[sub(v,1)(t)]], [[sub(v,2)(t)]]라 할 때, [[sub(v,1)(t) = 3 pow(t,2) - 7t + 2]],\n"
              "[[sub(v,2)(t) = 2t + 2]]이다. 시각 [[t = 0]]에서의 점 P의 위치는\n"
              "4이고 점 Q의 위치는 [[k]]일 때, 두 점 P, Q가 동시에\n"
              "출발한 후 2번 만나도록 하는 정수 [[k]]의 개수는?"),
    choices=["[[11]]", "[[12]]", "[[13]]", "[[14]]", "[[15]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PS,
    note="x_P−x_Q = t³−(9/2)t²+4−k: h(t)=t³−(9/2)t²+4는 (0,3) 감소·(3,∞) 증가, h(3)=−19/2, h(0)=4 → −19/2<k<4 → 정수 −9~3의 13개 → ③. 빠른정답 8과 불일치. 출처 머리말 없음.")

# p34 — 2017년 11월 고2 이과 18번 (빈칸 (가)(나)(다))
add(id="6edf187f", qtype="choice",
    question=("원점을 동시에 출발하여 수직선 위를 움직이는\n"
              "두 점 P, Q의 시각 [[t]]에서의 속도가 각각\n"
              "[[sub(v,1)(t) = frac(1,2) pow(t,2) - 3t]], [[sub(v,2)(t) = -frac(1,2) pow(t,2) + t]]\n"
              "이다. 다음은 두 점 P, Q가 출발 후 처음으로 만날 때까지\n"
              "두 점 P, Q 사이의 거리의 최댓값을 구하는 과정이다.\n"
              "두 점 P, Q의 시각 [[t]]에서의 위치를 각각\n"
              "[[sub(x,1)(t)]], [[sub(x,2)(t)]]라 하면\n"
              "[[sub(x,1)(t) = frac(1,6) pow(t,3) - frac(3,2) pow(t,2)]]\n"
              "[[sub(x,2)(t)]] = (가)\n"
              "출발 후 처음으로 두 점 P, Q가 만나는 시각은\n"
              "[[t = 6]]이다.\n"
              "[[0 < t <= 6]]에서 두 점 P, Q 사이의 거리를 [[l(t)]]라\n"
              "하면\n"
              "[[l(t)]]는 [[t]] = (나) 일 때 극대이면서 최대이므로\n"
              "[[l(t)]]의 최댓값은 (다) 이다.\n"
              "위의 (가)에 알맞은 식을 [[f(t)]]라 하고, (나), (다)에 알맞은\n"
              "수를 각각 [[a]], [[b]]라 할 때, [[frac(a × b, f(2))]]의 값은?"),
    choices=["[[60]]", "[[62]]", "[[64]]", "[[66]]", "[[68]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PS,
    note="출처 [2017년 11월 고2 이과 18번/4점]. (가) −t³/6+t²/2, f(2)=2/3; l=−t³/3+2t², (나) a=4, (다) b=32/3 → ab/f(2)=64 → ③. 빠른정답 '180m'은 값 아님.")

# p38 — 2021년 11월 고3 14번 — id 2개
dup(["32f8d4fc", "25d13969"], qtype="choice",
    question=("수직선 위를 움직이는 점 P의 시각 [[t]]에서의 위치 [[x(t)]]가\n"
              "두 상수 [[a]], [[b]]에 대하여 [[x(t) = t(t - 1)(a t + b)]] ([[a != 0]])\n"
              "이다. 점 P의 시각 [[t]]에서의 속도 [[v(t)]]가\n"
              "[[dinteg(0, 1, abs(v(t)), t) = 2]]를 만족시킬 때, <보기>에서 옳은 것만을\n"
              "있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[dinteg(0, 1, v(t), t) = 0]]\n"
              "ㄴ. [[abs(x(sub(t,1))) > 1]]인 [[sub(t,1)]]이 열린구간 [[itv(0, 1, oo)]]에\n"
              "존재한다.\n"
              "ㄷ. [[0 <= t <= 1]]인 모든 [[t]]에 대하여 [[abs(x(t)) < 1]]이면\n"
              "[[x(sub(t,2)) = 0]]인 [[sub(t,2)]]가 열린구간 [[itv(0, 1, oo)]]에 존재한다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2021년 11월 고3 14번/4점]. ㄱ x(1)−x(0)=0 ✓; ㄴ (0,1)에 영점이 있으면 극값 크기의 합이 1이라 |x|<1 가능 ✗; ㄷ 영점이 없으면 이동거리 2|M|=2 → |M|=1 모순 ✓ → ③. 빠른정답 frac(25,2)는 값 아님.")

# p49 — 위 문항의 변형 (t(t−3), 구간 [0,3])
add(id="16e2ad9a", qtype="choice",
    question=("수직선 위를 움직이는 점 P의 시각 [[t]]에서의 위치 [[x(t)]]가\n"
              "두 상수 [[a]], [[b]]에 대하여\n"
              "[[x(t) = t(t - 3)(a t + b)]] ([[a != 0]])이다.\n"
              "점 P의 시각 [[t]]에서의 속도 [[v(t)]]가 [[dinteg(0, 3, abs(v(t)), t) = 6]]을\n"
              "만족시킬 때, 보기에서 옳은 것만을 있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[dinteg(0, 3, v(t), t) = 0]]\n"
              "ㄴ. [[abs(x(sub(t,1))) > 3]]인 [[sub(t,1)]]이 열린구간 [[itv(0, 3, oo)]]에\n"
              "존재한다.\n"
              "ㄷ. [[0 <= t <= 3]]인 모든 [[t]]에 대하여 [[abs(x(t)) < 3]]이면\n"
              "[[x(sub(t,2)) = 0]]인 [[sub(t,2)]]가 열린구간 [[itv(0, 3, oo)]]에 존재한다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    note="2021년 11월 고3 14번 변형(출처 머리말 없음). ㄱ x(3)=x(0)=0 ✓; ㄴ 영점이 있으면 극값 크기 합 3 → |x|<3 가능 ✗; ㄷ 영점 없으면 2|M|=6 → |M|=3 모순 ✓ → ③. 빠른정답 '11km'은 값 아님.")

# p88 — 2011년 9월 고3 문과 21번 (속도 그래프)
add(id="9dc3444a", qtype="choice",
    question=("같은 높이의 지면에서 동시에 출발하여\n"
              "지면과 수직인 방향으로 올라가는 두 물체 A, B가 있다.\n"
              "그림은 시각 [[t]]([[0 <= t <= c]])에서 물체 A의 속도 [[f(t)]]와\n"
              "물체 B의 속도 [[g(t)]]를 나타낸 것이다.\n"
              "[[dinteg(0, c, f(t), t) = dinteg(0, c, g(t), t)]]이고 [[0 <= t <= c]]일 때,\n"
              "옳은 것만을 <보기>에서 있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[t = a]]일 때, 물체 A는 물체 B보다 높은 위치에\n"
              "있다.\n"
              "ㄴ. [[t = b]]일 때, 물체 A와 물체 B의 높이의 차가\n"
              "최대이다.\n"
              "ㄷ. [[t = c]]일 때, 물체 A와 물체B는 같은 높이에 있다."),
    choices=["ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "t–y 좌표평면: 곡선 y=f(t)는 원점에서 출발해 t=a에서 최대, 감소하여 t=c에서 0; 직선 y=g(t)는 원점에서 출발하는 증가 직선으로 t=b에서 f와 만남; a, b, c에서 점선"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 두 속도 그래프 y=f(t), y=g(t)(좌표평면)",
    note="출처 [2011년 9월 고3 문과 21번/4점]. (0,b)에서 f>g → ㄱ ✓; 높이 차는 t=b까지 증가 후 감소 → ㄴ ✓; 정적분 같음 → ㄷ ✓ → ⑤. 빠른정답 2와 불일치.")

# p89 — 속도 그래프, t=5~7 이동 거리
add(id="a07c8468", qtype="short",
    question=("원점을 출발하여 수직선 위를 움직이는 점 P의\n"
              "시각 [[t]]에서의 속도 [[v(t)]]를 나타내는 그래프가 다음 그림과\n"
              "같다.\n"
              "[[dinteg(0, 4, v(t), t) = dinteg(4, 7, abs(v(t)), t) = 6]]이고 점 P의\n"
              "시각 [[t = 5]]에서의 위치가 4일 때, 시각 [[t = 5]]에서\n"
              "[[t = 7]]까지 점 P가 움직인 거리를 구하시오."),
    choices=None, derived_answer="4",
    figure=[{"fn": "unsupported", "args": {"raw": "t–y 좌표평면 위 y=v(t): 원점에서 출발해 양수 구간 (0,4)(극대 후 감소), (4,6)에서 음수(t=5에서 최소, 점선), t=6에서 0, (6,7)에서 양수로 증가(t=7에서 점선)"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 속도 y=v(t)의 그래프(좌표평면)",
    note="x(5)=6+∫₄⁵v=4 → ∫₄⁵v=−2; [4,6] 대칭으로 보아 ∫₅⁶v=−2, ∫₆⁷v=6−4=2 → 거리 2+2=4 (그래프 대칭 가정). 빠른정답 32와 불일치. 출처 머리말 없음.")

# p90 — 속도 그래프 (보기)
add(id="0ec81078", qtype="choice",
    question=("다음은 원점을 출발하여 수직선 위를 움직이는 점 P의\n"
              "시각 [[t]]([[0 <= t <= d]])에서의 속도 [[v(t)]]를 나타내는\n"
              "그래프이다.\n"
              "[[dinteg(0, a, abs(v(t)), t) = dinteg(a, d, abs(v(t)), t)]]일 때, 다음 보기 중\n"
              "옳은 것만을 있는 대로 고른 것은?\n"
              "(단, [[0 < a < b < c < d]])\n"
              "<보기>\n"
              "ㄱ. 점 P는 움직이는 동안 운동 방향이 세 번\n"
              "바뀌었다.\n"
              "ㄴ. [[dinteg(0, d, v(t), t) < 0]]\n"
              "ㄷ. [[-dinteg(0, b, v(t), t) = dinteg(b, d, abs(v(t)), t)]]"),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "t–v(t) 좌표평면: 원점에서 출발한 곡선이 (0,a)에서 음수, t=a에서 0, (a,c)에서 양수(t=b에서 최대, 점선), t=c에서 0, (c,d)에서 음수, t=d까지(점선)"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 속도 v(t)의 그래프(좌표평면)",
    note="방향 전환은 t=a, c의 2번 → ㄱ ✗; S₁=S₂+S₃이면 ∫₀ᵈv=−2S₃<0 ㄴ ✓; ㄷ 양변 모두 ∫ᵦᶜv+S₃ ✓ → ④. 빠른정답 2와 불일치. 출처 머리말 없음.")

# p92 — 속도 그래프, t=3~5 이동 거리
add(id="9b51fabd", qtype="short",
    question=("원점을 출발하여 수직선 위를 움직이는 점 P의\n"
              "시각 [[t]]에서의 속도 [[v(t)]]의 그래프가 다음 그림과 같다.\n"
              "[[dinteg(0, 2, v(t), t) = dinteg(2, 5, abs(v(t)), t) = 5]]이고 [[t = 3]]에서의 점 P의\n"
              "위치가 3일 때, [[t = 3]]에서 [[t = 5]]까지 점 P가 움직인\n"
              "거리를 구하시오."),
    choices=None, derived_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": "t–v(t) 좌표평면: 원점에서 출발해 (0,2)에서 양수(극대 후 감소), (2,4)에서 음수(t=3에서 최소, 점선), t=4에서 0, (4,5)에서 양수로 증가(t=5에서 점선)"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 속도 v(t)의 그래프(좌표평면)",
    note="x(3)=5+∫₂³v=3 → ∫₂³v=−2; [2,4] 대칭으로 보아 ∫₃⁴v=−2, ∫₄⁵v=5−4=1 → 거리 2+1=3 (그래프 대칭 가정). 빠른정답 4와 불일치. 출처 머리말 없음.")

# p95 — 속도 그래프 (보기 ㄱ~ㄹ)
add(id="b9c5d438", qtype="choice",
    question=("원점을 출발하여 수직선 위를 움직이는 점 P의\n"
              "시각 [[t]] ([[0 <= t <= h]])에서의 속도 [[v(t)]]의 그래프가 아래\n"
              "그림과 같고, [[dinteg(0, a, v(t), t) = dinteg(a, g, abs(v(t)), t)]],\n"
              "[[dinteg(a, e, abs(v(t)), t) = dinteg(e, h, v(t), t)]]일 때, 다음 보기 중 항상 옳은\n"
              "것만을 있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[dinteg(0, c, v(t), t) = dinteg(c, g, abs(v(t)), t)]]\n"
              "ㄴ. 점 P는 출발 후 운동 방향을 4번 바꾼다.\n"
              "ㄷ. [[dinteg(0, e, v(t), t) = dinteg(a, e, abs(v(t)), t) + dinteg(g, h, abs(v(t)), t)]]\n"
              "ㄹ. 점 P는 출발 후 다시 원점을 지난다."),
    choices=["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄷ, ㄹ", "ㄴ, ㄷ, ㄹ"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "t–v(t) 좌표평면: 원점에서 출발해 (0,a)에서 양수(큰 산), (a,e)에서 음수(t=b 극소, t=c에서 t축에 접함, t=d 극소; 점선), (e,g)에서 양수(t=f 최대, 점선), (g,h)에서 음수(t=h 점선)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 속도 v(t)의 그래프(좌표평면; t=c에서 접하는 정보 포함)",
    note="A₁=N₁+N₂+P₂, N₁+N₂=P₂−N₃: ㄱ A₁−N₁=N₂+P₂ ✓; ㄴ 방향 전환 a, e, g의 3번(c는 접점) ✗; ㄷ 양변 P₂ ✓; ㄹ 위치 최소 x(e)=P₂>0 ✗ → ②. 빠른정답 3과 불일치. 적분 한계 e는 파서에서 상수 e로 읽히나 표시는 동일. 출처 머리말 없음.")

# p99 — 조각 속도, 최소 이동거리 f(x)의 정적분
add(id="18ab835c", qtype="choice",
    question=("수직선 위에서 원점을 출발하여 움직이는 점 P의\n"
              "시각 [[t]]([[0 <= t <= 5]])일 때의 속도 [[v(t)]]가 다음과 같다.\n"
              "[[v(t)]] = { [[4t]] ([[0 <= t < 1]]) ; [[-2t + 6]] ([[1 <= t < 3]]) ; [[t - 3]] ([[3 <= t <= 5]]) }\n"
              "실수 [[x]] ([[0 < x < 3]])에 대하여 점 P가\n"
              "시각 [[t = 0]]에서 [[t = x]]까지 움직인 거리,\n"
              "시각 [[t = x]]에서 [[t = x + 2]]까지 움직인 거리,\n"
              "시각 [[t = x + 2]]에서 [[t = 5]]까지 움직인 거리\n"
              "중에서 최소인 값을 [[f(x)]]라고 하자. [[f(0) = 0]]일 때,\n"
              "[[2 dinteg(0, 2, f(x), x)]]의 값은?"),
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PW,
    note="v≥0: s(t)=2t² (t<1), −t²+6t−3 (1≤t<3), 6+(t−3)²/2 (t≥3); (0,1)에서 f=2x², [1,2]에서 f=2−(x−1)²/2 → ∫₀²f=5/2 → 2∫=5 → ③ = 빠른정답 ✓. 출처 머리말 없음.")

# ═════════════════════════ 함수의 증가와 감소, 극대와 극소
# p8 — 2013년 9월 고3 문과 21번
add(id="17844967", qtype="choice",
    question=("사차함수 [[f(x)]] 의 도함수 [[prime(f)(x)]] 가\n"
              "[[prime(f)(x) = (x + 1)(pow(x,2) + a x + b)]]\n"
              "이다. 함수 [[y = f(x)]] 가 구간 [[itv(-inf, 0, oo)]] 에서 감소하고\n"
              "구간 [[itv(2, inf, oo)]] 에서 증가하도록 하는 실수 [[a]], [[b]] 의\n"
              "순서쌍 [[point(a, b)]] 에 대하여, [[pow(a,2) + pow(b,2)]] 의 최댓값을 [[M]],\n"
              "최솟값을 [[m]] 이라 하자. [[M + m]] 의 값은?"),
    choices=["[[frac(21,4)]]", "[[frac(43,8)]]", "[[frac(11,2)]]", "[[frac(45,8)]]", "[[frac(23,4)]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PR,
    note="출처 [2013년 9월 고3 문과 21번/4점]. x=−1에서 부호가 안 바뀌려면 f′=(x+1)²(x+b), −2≤b≤0, a=b+1 → a²+b²=2b²+2b+1: 최대 5(b=−2), 최소 1/2(b=−1/2) → 11/2 → ③. 빠른정답 1과 불일치.")

# p18 — 삼차함수가 증가할 조건
add(id="31927356", qtype="choice",
    question=("함수 [[f(x) = frac(1,3) pow(x,3) + a pow(x,2) - (a - 6) x + 1]]이\n"
              "[[sub(x,1) < sub(x,2)]]인 임의의 실수 [[sub(x,1)]], [[sub(x,2)]]에 대하여 항상\n"
              "[[f(sub(x,1)) < f(sub(x,2))]]가 성립하도록 하는 실수 [[a]]의 값의\n"
              "범위는 [[alpha <= a <= beta]]이다. 이때 [[alpha + beta]]의 값은?"),
    choices=["[[-2]]", "[[-1]]", "[[1]]", "[[2]]", "[[3]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    note="f′=x²+2ax−(a−6)≥0 항상 → a²+a−6≤0 → −3≤a≤2 → α+β=−1 → ②. 빠른정답 4와 불일치. 출처 머리말 없음.")

# p30 — 2023년 9월 고3 13번 (조각 정의)
add(id="08f7ee20", qtype="choice",
    question=("두 실수 [[a]], [[b]]에 대하여\n"
              "함수 [[f(x)]] = { [[-frac(1,3) pow(x,3) - a pow(x,2) - b x]] ([[x < 0]]) ; [[frac(1,3) pow(x,3) + a pow(x,2) - b x]] ([[x >= 0]]) }이\n"
              "구간 [[itv(-inf, -1, oc)]]에서 감소하고 구간 [[itv(-1, inf, co)]]에서\n"
              "증가할 때, [[a + b]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 하자.\n"
              "[[M - m]]의 값은?"),
    choices=["[[frac(3,2) + 3 sqrt(2)]]", "[[3 + 3 sqrt(2)]]", "[[frac(9,2) + 3 sqrt(2)]]", "[[6 + 3 sqrt(2)]]", "[[frac(15,2) + 3 sqrt(2)]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    needs_review=PW,
    note="출처 [2023년 9월 고3 13번/4점]. x<0: x²+2ax+b=(x+1)(x−r), r≥0 → a=(1−r)/2, b=−r; x≥0: x²+(1−r)x+r≥0 → r≤3+2√2 → a+b=1/2−3r/2: M=1/2, m=−4−3√2 → M−m=9/2+3√2 → ③. 빠른정답 4와 불일치.")

# p40 — 도함수의 그래프로 증감 판단 (그래프 도형)
add(id="ba35e6d9", qtype="choice",
    question=("다항함수 [[y = f(x)]]의 도함수 [[y = prime(f)(x)]]의 그래프가\n"
              "아래 그림과 같을 때, 다음 중 옳은 것은?"),
    choices=["[[f(x)]]는 구간 [[itv(-inf, -2, oo)]]에서 증가한다.",
             "[[f(x)]]는 구간 [[itv(0, 1, oo)]]에서 감소한다.",
             "[[f(x)]]는 구간 [[itv(2, 3, oo)]]에서 증가한다.",
             "[[f(x)]]는 구간 [[itv(3, 6, oo)]]에서 증가하다가 감소한다.",
             "[[f(x)]]는 구간 [[itv(6, inf, oo)]]에서 감소한다."],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f′(x)의 그래프: x=−2, 1, 3, 6에서 x축과 만남; (−∞,−2)와 (1,3)(x=2에서 극소, 점선), (6,∞)에서 음수; (−2,1), (3,6)에서 양수"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 도함수 y=f′(x)의 그래프(좌표평면) / " + PR,
    note="f′<0: (−∞,−2), (1,3), (6,∞); f′>0: (−2,1), (3,6) → ⑤만 옳음. 빠른정답 3과 불일치. 출처 머리말 없음.")

# ═════════════════════════ 함수의 그래프
# p52 — 사차함수가 극솟값을 갖지 않을 조건
add(id="c0150b52", qtype="short",
    question=("함수 [[f(x) = -3 pow(x,4) - 8 pow(x,3) + 6(a + 3) pow(x,2) - 12 a x + 5]]가\n"
              "극솟값을 갖지 않도록 하는 자연수 [[a]]의 개수를 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.85,
    note="f′=−12(x−1)(x²+3x−a): 극솟값 없으려면 x²+3x−a가 x=1을 근으로(a=4) 또는 실근 없음(a≤−9/4, 자연수 아님) → a=4의 1개 = 빠른정답 ✓. 출처 머리말 없음.")

# p61 — g(x)={2 (x<0); f(x) (x≥0)} 미분가능 (보기)
add(id="af8cd741", qtype="choice",
    question=("삼차함수 [[f(x)]]의 최고차항의 계수가 1이고 함수 [[g(x)]]는\n"
              "[[g(x)]] = { [[2]] ([[x < 0]]) ; [[f(x)]] ([[x >= 0]]) }이다.\n"
              "[[g(x)]]가 실수 전체의 집합에서 미분가능하고 [[g(x)]]의\n"
              "최솟값이 2보다 작을 때, 다음 보기 중에서 옳은 것을\n"
              "있는 대로 고른 것은?\n"
              "<보기>\n"
              "ㄱ. [[g(0) + prime(g)(0) = 2]]\n"
              "ㄴ. [[g(1) < 3]]\n"
              "ㄷ. [[g(x)]]의 최솟값이 [[frac(3,2)]] 일 때, [[g(2) = 2]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PW + " / " + PR,
    note="f=x³+ax²+2 (f(0)=2, f′(0)=0), 최솟값<2 → a<0: ㄱ ✓, ㄴ g(1)=3+a<3 ✓, ㄷ 최솟값 4a³/27+2=3/2 → a=−3/2 → g(2)=4≠2 ✗ → ② = 빠른정답 ✓. 출처 머리말 없음.")

# p71 — OP²+AP²의 최솟값 (포물선 y=x²+1)
add(id="e58e2e9c", qtype="choice",
    question=("좌표평면 위의 두 점 [[O(0, 0)]], [[A(10, 0)]]에 대하여\n"
              "점 P가 포물선 [[y = pow(x,2) + 1]] 위를 움직일 때,\n"
              "[[pow(seg(OP), 2) + pow(seg(AP), 2)]]의 최솟값은?"),
    choices=["[[70]]", "[[80]]", "[[90]]", "[[100]]", "[[110]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="P=(t,t²+1): 합=2t⁴+6t²−20t+102, 도함수 4(t−1)(2t²+2t+5) → t=1에서 최소 90 → ③ = 빠른정답 ✓. 출처 머리말 없음.")

# p72 — AP²+BP²의 최솟값 (곡선 y=x²−2)
add(id="de5fda80", qtype="short",
    question=("두 점 [[A(0, -3)]], [[B(10, -3)]]에 대하여 점 P가\n"
              "곡선 [[y = pow(x,2) - 2]]위를 움직일 때,\n"
              "[[pow(seg(AP), 2) + pow(seg(BP), 2)]]의 최솟값을 구하시오."),
    choices=None, derived_answer="90", figure=None, difficulty_est=2, confidence=0.9,
    note="P=(t,t²−2): 합=2(t²+1)²+2t²−20t+100=2t⁴+6t²−20t+102 → t=1에서 최소 90 = 빠른정답 ✓. 출처 머리말 없음.")

# p74 — OP²+AP²의 최솟값 (곡선 y=x²−2x+2)
add(id="eab44f31", qtype="choice",
    question=("곡선 [[y = pow(x,2) - 2x + 2]] 위를 움직이는 점 P와 점\n"
              "[[A(2, 0)]]에 대하여 [[pow(seg(OP), 2) + pow(seg(AP), 2)]]의 최솟값은? (단,\n"
              "O는 원점이다.)"),
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="u=(t−1)²: 합=2(u+1)²+2u+2, u=0(t=1)에서 최소 4 → ② = 빠른정답 ✓. 출처 머리말 없음.")

# ═════════════════════════ 넓이
# p18 — 곡선과 직선 사이의 넓이 (좌표평면 도형)
add(id="15975a72", qtype="choice",
    question=("다음 그림과 같이 좌표평면 위의 점 [[A(-2, 0)]]을 지나고\n"
              "기울기가 양수인 직선 [[l]]이 곡선 [[y = 2 pow(x,2)]]과 만나는 두 점을\n"
              "각각 P, Q라 하자. [[ratio(seg(AP), seg(AQ)) = ratio(4, 9)]]일 때, 직선 [[l]]과\n"
              "곡선 [[y = 2 pow(x,2)]]으로 둘러싸인 도형의 넓이는?\n"
              "(단, 점 Q는 제1사분면 위의 점이다.)"),
    choices=["[[frac(41,27)]]", "[[frac(124,81)]]", "[[frac(125,81)]]", "[[frac(14,9)]]", "[[frac(127,81)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y=2x², 점 A(−2,0)을 지나는 기울기 양수인 직선 l이 포물선과 P(제2사분면 쪽), Q(제1사분면)에서 만남, 직선과 포물선 사이 영역 음영, 원점 O"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 포물선·직선·음영 영역이 있는 좌표평면 도형",
    note="x_P+2 : x_Q+2 = 4:9 → x_P=−2/3, x_Q=1, 기울기 2/3 → 넓이 2·(5/3)³/6=125/81 → ③ = 빠른정답 ✓. 출처 머리말 없음.")

# p82 — 역함수의 정적분 (f=x³+3x)
add(id="cbcb1924", qtype="choice",
    question=("함수 [[f(x) = pow(x,3) + 3x]]의 역함수를 [[g(x)]]라 한다.\n"
              "이때, [[dinteg(4, 14, g(x), x) - dinteg(-2, -1, f(x), x)]]의 값은?"),
    choices=["[[20]]", "[[22]]", "[[24]]", "[[26]]", "[[28]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="f(1)=4, f(2)=14: ∫₄¹⁴g=28−4−∫₁²f=63/4, ∫₋₂⁻¹f=−33/4 → 차 24 → ③. 빠른정답 12와 불일치. 출처 머리말 없음.")

# p84 — 역함수의 정적분 (f=x³+2x²+x)
add(id="916b30ac", qtype="short",
    question=("[[x > 0]]에서 정의된 함수 [[f(x) = pow(x,3) + 2 pow(x,2) + x]]와\n"
              "그 역함수 [[g(x)]]에 대하여 정적분\n"
              "[[dinteg(0, 1, f(x), x) + dinteg(0, 4, g(x), x)]]를 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.85,
    note="f(0)=0, f(1)=4 → 합 = 1·4 = 4. 빠른정답 1과 불일치. 출처 머리말 없음.")

# p86 — 역함수의 정적분 (f=x³+4)
add(id="36fe51e7", qtype="short",
    question=("함수 [[f(x) = pow(x,3) + 4]]의 역함수를 [[g(x)]]라 할 때,\n"
              "[[dinteg(0, 2, f(x), x) + dinteg(f(0), f(2), g(x), x)]]의 값을 구하시오."),
    choices=None, derived_answer="24", figure=None, difficulty_est=2, confidence=0.85,
    note="합 = 2·f(2) − 0·f(0) = 2·12 = 24. 빠른정답 5와 불일치. 출처 머리말 없음.")

# p87 — 역함수의 정적분 = 34 조건
add(id="cd7b9307", qtype="short",
    question=("함수 [[f(x) = pow(x,2) + x]] ([[x >= 0]])의 역함수를 [[g(x)]]라 할 때,\n"
              "[[dinteg(a, a + 2, f(x), x) + dinteg(f(a), f(a + 2), g(x), x) = 34]]를 만족시키는\n"
              "양수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.85,
    note="(a+2)f(a+2)−af(a)=6a²+16a+12=34 → 3a²+8a−11=0 → a=1 = 빠른정답 ✓. 출처 머리말 없음.")

# p88 — 역함수의 정적분 (f=x²+4)
add(id="2071b807", qtype="short",
    question=("함수 [[f(x) = pow(x,2) + 4]] ([[x >= 0]])의 역함수를 [[g(x)]]라 할 때,\n"
              "정적분 [[dinteg(0, 4, f(x), x) + dinteg(4, 20, g(x), x)]]의 값을 구하시오."),
    choices=None, derived_answer="80", figure=None, difficulty_est=2, confidence=0.9,
    note="f(0)=4, f(4)=20 → 합 = 4·20 − 0·4 = 80 = 빠른정답 ✓. 출처 머리말 없음.")

# p89 — 연속함수와 역함수의 정적분 k
add(id="bbf1d53d", qtype="choice",
    question=("[[f(3) = 3]], [[f(11) = 11]]인 연속함수 [[f(x)]]에 대하여\n"
              "[[dinteg(3, 11, f(x), x) = sub(S,1)]]이라 하자. [[f(x)]]의 역함수 [[g(x)]]에\n"
              "대하여 [[dinteg(3, 11, g(x), x) = k - sub(S,1)]] 일 때, 상수 [[k]]의 값은?"),
    choices=["[[111]]", "[[112]]", "[[113]]", "[[114]]", "[[115]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="∫f+∫g = 11·11 − 3·3 = 112 → ② = 빠른정답 ✓. 출처 머리말 없음.")
