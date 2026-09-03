# -*- coding: utf-8 -*-
# esc_sonnet_h2-1_3of4 — 이미지 기준 전사 (82 항목 / 80쪽) — 이미지 80장 전부 직접 판독
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def unsup(raw):
    return [{"fn": "unsupported", "args": {"raw": raw}}]

# ───────────────────────── 등차수열 ─────────────────────────
# p84 — 나머지가 같은 자연수의 합
add(id="4dfb3ef6", qtype="choice",
    question=("6으로 나누면 4가 남고, 10으로 나누면 4가 남는 자연수를 크기순으로 나열하여 "
              "[[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,n)]]이라 하자. "
              "이때 [[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,8)]]의 값은?"),
    choices=["[[870]]", "[[872]]", "[[874]]", "[[876]]", "[[878]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="aₙ = 30n − 26 → 4+34+…+214 = 872 → ②. 빠른정답 5와 불일치.")

# p87 — 등차수열의 합의 활용(3)
add(id="cffc0f28", qtype="short",
    question=("등차수열 [[set(sub(a,n))]]에 대하여\n"
              "[[sub(b, 2k-1) = sub(a,1) - 2 sub(a,3) + 3 sub(a,5)]] − ⋯ + [[pow(-1, k+1) × k sub(a, 2k-1)]],\n"
              "[[sub(b, 2k) = -sub(a,2) + 2 sub(a,4) - 3 sub(a,6)]] + ⋯ + [[pow(-1, k) × k sub(a, 2k)]]\n"
              "로 정의되는 수열 [[set(sub(b,n))]]이\n"
              "[[sub(b,1) + sub(b,2) + sub(b,3) + sub(b,4) + sub(b,5) + sub(b,6) = -20]]을 만족할 때,\n"
              "수열 [[set(sub(a,n))]]의 공차를 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=3, confidence=0.9,
    note="b₁~b₆ 합 = 3(a₁−a₂)+4(a₄−a₃)+3(a₅−a₆) = −2d = −20 → d = 10 = 빠른정답 ✓.")

# p88 — 등차수열의 합의 활용(3)
add(id="694cce4e", qtype="short",
    question=("등차수열 [[set(sub(a,n))]]에 대하여\n"
              "[[sub(b, 2k-1) = -sub(a,1) + 3 sub(a,3) - 5 sub(a,5)]] + ⋯ + [[pow(-1, k)(2k - 1) sub(a, 2k-1)]]\n"
              "[[sub(b, 2k) = sub(a,2) - 3 sub(a,4) + 5 sub(a,6)]] − ⋯ + [[pow(-1, k+1)(2k - 1) sub(a, 2k)]]\n"
              "로 정의되는 수열 [[set(sub(b,n))]]이\n"
              "[[sub(b,1) + sub(b,2) + sub(b,3) + sub(b,4) + sub(b,5) + sub(b,6) = 20]]을 만족시킬 때,\n"
              "수열 [[set(sub(a,n))]]의 공차를 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=3, confidence=0.9,
    note="b₁~b₆ 합 = −3a₁+3a₂+6a₃−6a₄−5a₅+5a₆ = 3d−6d+5d = 2d = 20 → d = 10. 빠른정답 15와 불일치.")

# p98 — 합과 일반항 (보기)
add(id="1c71c21c", qtype="choice",
    question=("첫째항부터 제[[n]]항까지의 합 [[sub(S,n)]]이 [[sub(S,n) = pow(n,2) + 2n - 3]]으로 나타내어지는 수열 "
              "[[set(sub(a,n))]]에 대하여 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sub(a,2) = 5]]\n"
              "ㄴ. [[sub(a,5) - sub(a,3) = sub(a,6) - sub(a,4)]]\n"
              "ㄷ. [[sub(a,n) > 100]]을 만족시키는 자연수 [[n]]의 최솟값은 49이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="a₁=0, aₙ=2n+1(n≥2): ㄱ✓ ㄴ✓(4=4) ㄷ✗(최솟값 50) → ②. 빠른정답 15와 불일치.")

# ───────────────────────── 일반각과 호도법 ─────────────────────────
# p26 — 육십분법과 호도법 (계기판)
add(id="e4c5e022", qtype="choice",
    question=("그림과 같이 81 MHz에서 625 MHz까지의 주파수를 나타내는 반원 모양의 어떤 계기판이 있다.\n"
              "81 MHz를 가리키던 바늘이 시계방향으로 [[theta]](라디안)만큼 회전했을 때 가리키는 주파수를 [[f]] MHz라 하면\n"
              "[[f = k pow(a, theta)]] ([[k]], [[a]]는 상수, [[0 <= theta <= pi]])\n"
              "인 관계가 성립한다.\n"
              "[[theta = frac(3,4) pi]]일 때, 바늘이 가리키는 주파수는?"),
    choices=["[[275]] MHz", "[[300]] MHz", "[[325]] MHz", "[[350]] MHz", "[[375]] MHz"],
    derived_answer="⑤",
    figure=unsup("반원 모양 계기판 삽화: 왼쪽 끝 81 MHz, 오른쪽 끝 625 MHz, 중심에서 각 θ만큼 회전한 바늘"),
    difficulty_est=2, confidence=0.85,
    note="k=81, a^π=(5/3)⁴ → f = 81·(5/3)³ = 375 → ⑤ = 빠른정답 ✓. 계기판 그림은 설명 삽화(정보는 본문에 모두 있음).")

# p47 — 두 동경의 위치 관계(1)
add(id="cf4c4cd6", qtype="short",
    question=("좌표평면에서 크기가 [[(3n - 1) pi + pow(-1, n) × frac(n, 4) pi]]인 각을 나타내는 동경을 [[O sub(P,n)]]이라 하자.\n"
              "동경 [[O sub(P,2)]], [[O sub(P,3)]], [[O sub(P,4)]], ⋯, [[O sub(P,170)]] 중에서 "
              "동경 [[O sub(P,1)]]과 일치하는 동경의 개수를 구하시오. (단, [[O]]는 원점이다.)"),
    choices=None, derived_answer="21", figure=None, difficulty_est=3, confidence=0.9,
    note="전수 확인(n=2~170, 2π 차) 21개 = 빠른정답 ✓. 동경 OPₙ 라벨은 O·Pₙ 병치로 표기.")

# p55 — 두 동경의 위치 관계(2)
add(id="eaff1f73", qtype="choice",
    question=("두 각 [[alpha]], [[beta]]를 나타내는 동경이 직선 [[y = x]]에 대하여 대칭일 때, "
              "다음 중 [[alpha + beta]]의 값이 될 수 있는 것은?"),
    choices=["[[deg(-630)]]", "[[deg(-360)]]", "[[deg(-90)]]", "[[deg(0)]]", "[[deg(180)]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="α+β = 360°·n + 90° → −630° = −720°+90° → ①. 빠른정답 2와 불일치.")

# p78 — 부채꼴의 호의 길이와 넓이의 활용 (정삼각형 2개 외접 원)
add(id="c5f3f9a1", qtype="choice",
    question=("그림과 같이 [[tri(ABC)]]와 [[tri(CDE)]]는 한 변의 길이가 [[a]]인 정삼각형이고, [[angle(ACE) = frac(2,3) pi]]이다. "
              "반지름의 길이가 [[sqrt(3)]]인 원 [[P]]가 [[tri(ABC)]]와 [[tri(CDE)]]의 둘레를 외접하면서 시계 방향으로 한 바퀴 돌아 "
              "처음 출발한 자리로 왔을 때, 원 [[P]]의 중심이 움직인 거리가 [[23 + frac(8 sqrt(3), 3) pi]]이다. [[a]]의 값은?"),
    choices=["[[4]]", "[[frac(9,2)]]", "[[5]]", "[[frac(11,2)]]", "[[6]]"],
    derived_answer="②",
    figure=unsup("정삼각형 ABC(위)와 CDE(아래)가 꼭짓점 C를 공유, B·C·E 일직선, ∠ACE = 2π/3, 변 a 표시, 꼭짓점 A에 반지름 √3인 원 P가 외접"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정삼각형 2개 + 외접 원 P 복합 도형",
    note="출처 [2008년 6월 고2 이과 18번]. 볼록 꼭짓점 4개 호 8√3π/3, 직선부 6a−4 = 23 → a = 9/2 → ② = 빠른정답 ✓.")

# p81 — 원뿔
add(id="00fec22e", qtype="choice",
    question="다음 그림과 같은 원뿔에서 옆넓이가 밑넓이의 [[sqrt(2)]]배일 때, [[angle(ABO)]]의 크기는?",
    choices=["[[frac(pi,3)]]", "[[frac(pi,4)]]", "[[frac(pi,6)]]", "[[frac(pi,9)]]", "[[frac(pi,12)]]"],
    derived_answer="②",
    figure=unsup("원뿔: 꼭짓점 A, 밑면의 중심 O, 밑면 둘레 위의 점 B, AO⊥OB(직각 표시)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원뿔 입체도형(A 꼭짓점·O 밑면 중심·B 밑면 위의 점)",
    note="πrl = √2·πr² → l = √2 r → cos∠ABO = 1/√2 → π/4 → ② = 빠른정답 ✓.")

# p88 — 회전하는 두 선분 (색 반전)
add(id="177f8d6d", qtype="short",
    question=("길이가 10인 [[seg(AB)]]를 지름으로 하는 원 [[O]] 위를 움직이는 두 점 P, Q가 있다. "
              "두 선분 OP, OQ는 각각 두 선분 OA, OB에서 동시에 출발하여 점 O를 중심으로 시계 방향으로 회전한다. "
              "한 바퀴를 도는 데 선분 OP는 24초, 선분 OQ는 48초가 걸리고, 원의 내부는 처음에는 흰색이지만 "
              "두 선분 OP, OQ가 회전하면서 지나간 부분은 흰색은 검은색으로, 검은색은 흰색으로 바뀐다. "
              "두 선분 OP, OQ가 출발한 지 1000초 후, 검은색 부분의 넓이를 [[S pi]]라 할 때, [[2S]]의 값을 구하시오."),
    choices=None, derived_answer="25",
    figure=unsup("원 O(지름 AB, A 왼쪽·B 오른쪽), 점 P(왼쪽 위)·Q(오른쪽 아래), 시계 방향 화살표, 부채꼴 AOP·BOQ 검은색"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 원과 회전 선분·검은 부채꼴 그림",
    note="각속도 π/12, π/24; 1000초 후 통과 횟수 홀수인 영역 각 π(2π/3 + π/3) → S = 25/2, 2S = 25 (수치 시뮬레이션 일치). 빠른정답 6과 불일치.")

# ───────────────────────── 삼각함수 ─────────────────────────
# p8 — 삼각함수의 정의(1)
add(id="b2082e3a", qtype="short",
    question=("다음 그림과 같이 제2사분면에 있는 점 [[P(a, frac(8,3))]]에 대하여 [[seg(OP)]]를 동경으로 하는 각의 크기를 "
              "[[theta]]라 하면 [[tan(theta) = -frac(4,3)]]이다. [[seg(OP) = r]]라 할 때, [[a + r]]의 값을 구하시오."),
    choices=None, derived_answer="frac(4,3)",
    figure=unsup("좌표평면: 제2사분면의 점 P(a, 8/3), 원점 O에서 P까지 선분(길이 r), x축 양의 방향에서 OP까지의 각 θ"),
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 동경 그림",
    note="a = −2, r = 10/3 → a + r = 4/3 = 빠른정답 ✓.")

# p9 — 삼각함수의 정의(1) (단위원 접선)
add(id="31425c99", qtype="short",
    question=("다음 그림과 같이 반지름의 길이가 1인 원 위에 [[angle(AOB) = theta]]인 두 점 A, B가 있다. "
              "점 A에서의 접선이 [[seg(OB)]]의 연장선과 만나는 점을 P, 점 B에서 [[seg(OA)]]에 내린 수선의 발을 Q라 할 때, "
              "[[seg(OQ) = 3 seg(AP) × seg(BQ)]]이다. [[9 pow(tan(theta), 2)]]의 값을 구하시오.\n"
              "(단, [[0 < theta < frac(pi,2)]]이고, 원의 중심은 O이다.)"),
    choices=None, derived_answer="3",
    figure=unsup("반지름 1인 원(중심 O), 점 A(오른쪽)·B(호 위), 접선 위 점 P, OA 위 수선의 발 Q, ∠AOB = θ, 직각 표시 2개"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원·접선·수선 복합 도형",
    note="OQ = cosθ, AP = tanθ, BQ = sinθ → cos²θ = 3sin²θ → 9tan²θ = 3 = 빠른정답 ✓.")

# p15 — 삼각함수의 정의(2) (점 P_n)
add(id="764ae7e2", qtype="choice",
    question=("자연수 [[n]]에 대하여 [[sub(A,n)]]을 [[sub(A,n) = 5 + pow(-1, n)]]이라 하자.\n"
              "좌표평면 위의 점 [[sub(P,n)]]의 좌표를\n"
              "[[point(sub(A,n) cos(frac(2n pi, 3)), sub(A,n) sin(frac(2n pi, 3)))]]라 할 때, 다음 중 [[sub(P,2022)]]와 같은 점은?"),
    choices=["[[sub(P,2)]]", "[[sub(P,3)]]", "[[sub(P,4)]]", "[[sub(P,5)]]", "[[sub(P,6)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="A₂₀₂₂ = 6, 각 1348π → P₂₀₂₂ = (6, 0) = P₆ → ⑤. 빠른정답 4와 불일치.")

# p16 — 삼각함수의 정의(2) (집합 X)
add(id="e9ef9206", qtype="short",
    question=("한 개의 주사위를 던져서 나오는 눈의 수를 원소로 가지는 집합 [[A]]에 대하여 집합 [[X]]를\n"
              "[[X]] = { [[x]] | [[x = sin(frac(a,6) pi)]], [[in(a, A)]] }\n"
              "라 하자. 집합 [[X]]의 원소의 개수를 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2013년 3월 고2 문과 27번/4점]. X = {1/2, √3/2, 1, 0} → 4. 빠른정답 3과 불일치.")

# p28 — 삼각함수의 값의 부호 (조각적 정의)
add(id="247673f2", qtype="short",
    question=("[[f(x)]] = { [[1]] ([[x < 0]]) ; [[-2]] ([[x >= 0]]) }일 때, 다음 식을 만족시키는 각 [[theta]]는 "
              "제 몇 사분면의 각인지 구하시오.\n"
              "[[2 f(sin(theta)) f(cos(theta)) + f(tan(theta)) = 0]]"),
    choices=None, derived_answer="제3사분면", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔) → 텍스트 혼합 전사",
    note="f(sinθ)f(cosθ)=1(둘 다 음수, 제3사분면)이고 f(tanθ)=−2(tanθ>0) → 2−2=0 ✓ → 제3사분면. 빠른정답 3(사분면 번호)과 표기만 다름.")

# p43 — 삼각함수 사이의 관계(1) (id 2개)
dup(["a9318315", "3d295bed"], qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["[[frac(cos(theta), 1 + sin(theta)) + frac(sin(theta), cos(theta)) = frac(1, cos(theta))]]",
             "[[(2 - 2 pow(cos(theta), 2))(1 + frac(1, pow(tan(theta), 2))) = 2]]",
             "[[pow(cos(theta), 4) - pow(sin(theta), 4) = 2 pow(cos(theta), 2) - 1]]",
             "[[(sin(theta) + 1)(cos(theta) + 1)(1 - sin(theta))(cos(theta) - 1) = pow(sin(theta), 2) pow(cos(theta), 2)]]",
             "[[pow(sin(theta), 2)(pow(sin(theta), 2) + pow(cos(theta), 2) + frac(2, pow(tan(theta), 2))) = 1 + pow(cos(theta), 2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="④ 좌변 = (1−sin²θ)(cos²θ−1) = −sin²θcos²θ ≠ 우변 → ④ = 빠른정답 ✓. 나머지는 항등식.")

# p81 — 삼각함수 사이의 관계의 활용 (원 위의 점)
add(id="2e9bf03f", qtype="short",
    question=("다음 그림과 같이 선분 AB를 지름으로 하는 원 위에 [[angle(ABC) = theta]]가 되도록 점 C를 잡는다. "
              "점 C를 지나고 선분 AB와 평행한 직선이 원과 만나는 점을 D, 선분 AD와 선분 BC의 교점을 E라 하면 "
              "삼각형 ECD의 넓이는 삼각형 EAB의 넓이의 [[frac(4,9)]]배일 때, [[6 pow(cos(theta), 2)]]의 값을 구하시오. "
              "(단, [[0 < theta < frac(pi,4)]])"),
    choices=None, derived_answer="5",
    figure=unsup("원(지름 AB 수평), 아래쪽 호 위의 점 C·D(CD ∥ AB), AD와 BC의 교점 E, ∠ABC = θ 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원·평행 현·교점 복합 도형",
    note="닮음비 CD/AB = cos2θ = 2/3 → cos²θ = 5/6 → 6cos²θ = 5 = 빠른정답 ✓.")

# p82 — 원 위를 움직이는 물체
add(id="ad8568ca", qtype="short",
    question=("좌표평면 위를 움직이는 어느 물체의 시각 [[t]]에서의 위치 [[point(x, y)]]가 [[x = 8 + 11 cos(t)]], "
              "[[y = 23 - 11 sin(t)]]로 주어져 있다. 이 물체가 원점에서 가장 멀리 떨어져 있을 때와 가장 가까이 있을 때의 "
              "두 거리의 차를 구하시오."),
    choices=None, derived_answer="22", figure=None, difficulty_est=2, confidence=0.9,
    note="중심 (8, 23), 반지름 11인 원 위의 점 → (d+11) − (d−11) = 22. 빠른정답 4와 불일치.")

# ───────────────────────── 합의 기호 ∑ ─────────────────────────
# p2 — 옳지 않은 것
add(id="3da58a5e", qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["[[3 + 6 + 9]] + ⋯ + [[60 = sum(k, 1, 20, 3k)]]",
             "[[pow(1,2) + pow(2,2) + pow(3,2)]] + ⋯ + [[pow(n,2) = sum(k, 1, n, pow(k,2))]]",
             "[[1 + 2 + pow(2,2)]] + ⋯ + [[pow(2,9) = sum(k, 1, 10, pow(2, k-1))]]",
             "[[1 × 2 + 2 × pow(2,2) + 3 × pow(2,3)]] + ⋯ + [[n × pow(2,n) = sum(k, 1, n, k × pow(2,k))]]",
             "[[1 × 3 + 2 × 5 + 3 × 7]] + ⋯ + [[10 × 21 = sum(k, 1, 21, k(2k + 1))]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="⑤는 k=1~10이어야 함 → ⑤ = 빠른정답 ✓. 줄임표는 마커 밖 텍스트.")

# p3 — 옳은 것
add(id="998c5f0a", qtype="choice",
    question="다음 중 옳은 것은?",
    choices=["[[1 + 4 + 7]] + ⋯ + [[(3n - 5) = sum(k, 1, n, (3k - 5))]]",
             "[[2 + 4 + 6]] + ⋯ + [[2(n + 1) = sum(k, 1, n, 2(k + 1))]]",
             "[[3 + 5 + 7]] + ⋯ + [[(2n - 1) = sum(k, 1, n, (2k + 1))]]",
             "[[4 + 5 + 6]] + ⋯ + [[(n + 3) = sum(k, 1, n, (k + 3))]]",
             "[[3 + 4 + 5]] + ⋯ + [[n = sum(k, 1, n, k)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="④만 첫째항(4)·끝항(n+3) 일치 → ④ = 빠른정답 ✓.")

# p22 — 0,1,2 값을 갖는 수열
add(id="ca563706", qtype="short",
    question=("[[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]], ⋯, [[sub(x,n)]]은 0, 1, 2의 값 중 어느 하나를 갖는다. "
              "[[sum(i, 1, n, sub(x,i)) = 16]], [[sum(i, 1, n, pow(sub(x,i), 2)) = 26]]일 때, "
              "[[sum(i, 1, n, pow(sub(x,i), 4))]]의 값을 구하시오."),
    choices=None, derived_answer="86", figure=None, difficulty_est=2, confidence=0.9,
    note="1의 개수 p, 2의 개수 q: p+2q=16, p+4q=26 → q=5, p=6 → p+16q = 86. 빠른정답 30과 불일치.")

# p37 — 3^(-k) cos kπ 합
add(id="fc38c422", qtype="choice",
    question="[[sum(k, 1, 30, pow(3, -k) cos(k pi))]]의 값은?",
    choices=["[[-frac(1,2)(1 - pow(frac(1,3), 30))]]",
             "[[-frac(1,3)(1 - pow(frac(1,3), 30))]]",
             "[[-frac(1,4)(1 - pow(frac(1,3), 30))]]",
             "[[-2(1 - pow(frac(1,3), 30))]]",
             "[[-4(1 - pow(frac(1,3), 30))]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="Σ(−1/3)^k = (−1/3)(1−(1/3)³⁰)/(4/3) = −(1/4)(1−(1/3)³⁰) → ③ = 빠른정답 ✓. 중괄호는 소괄호로.")

# p40 — 2^(n-1) + (-1)^(n-1)
add(id="bafbb48d", qtype="choice",
    question=("수열 [[set(sub(a,n))]]에서 [[sub(a,n) = pow(2, n-1) + pow(-1, n-1)]]일 때,\n"
              "[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,10)]]의 값은?"),
    choices=["[[pow(2,10) - 3]]", "[[pow(2,10) - 1]]", "[[pow(2,10)]]", "[[pow(2,10) + 1]]", "[[pow(2,10) + 3]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="Σ2^(n−1) = 2¹⁰−1, Σ(−1)^(n−1)(10항) = 0 → 2¹⁰ − 1 → ②. 빠른정답 3과 불일치.")

# p76 — 4 + 44 + 444 + …
add(id="029df4ff", qtype="choice",
    question=("[[4 + 44 + 444]] + ⋯ + 444⋯4 (20개) = [[frac(a × pow(10, 20) - b, 81)]]\n"
              "일 때, [[a + b]]의 값은? (단, [[a]], [[b]]는 자연수)"),
    choices=["[[710]]", "[[740]]", "[[800]]", "[[820]]", "[[910]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="(4/9)Σ(10^k−1) = (40·10²⁰ − 760)/81 → a+b = 800 → ③. 빠른정답 25와 불일치. '444⋯4' 아래 '20개' 묶음 표시는 텍스트로.")

# ───────────────────────── 로그함수의 활용 ─────────────────────────
# p6 — 로그방정식(1)
add(id="acfb2ade", qtype="short",
    question=("직선 [[x = k]]가 두 곡선 [[y = log(5, x)]], [[y = -log(5, 6 - x)]]와 만나는 점을 각각 A, B라 하자. "
              "[[seg(AB) = 1]]이 되도록 하는 모든 실수 [[k]]의 값의 곱을 구하시오. (단, [[0 < k < 6]])"),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.9,
    note="|log₅(k(6−k))| = 1 → k(6−k) = 5(근의 곱 5) 또는 1/5(근의 곱 1/5) → 전체 곱 1. 빠른정답 7과 불일치.")

# p25 — 로그 연립방정식
add(id="a5b98a89", qtype="short",
    question=("연립방정식 [[log(2, x) + log(3, y) = 7]], [[log(3, x) × log(2, y) = 12]]의 해를 "
              "[[x = alpha]], [[y = beta]]라 할 때, [[beta - alpha]]의 최댓값을 구하시오."),
    choices=None, derived_answer="73", figure=None, difficulty_est=3, confidence=0.9,
    note="log₂x=a, log₃y=b: a+b=7, ab=12 → (x,y)=(8,81),(16,27) → 최댓값 81−8 = 73. 빠른정답 2와 불일치. 연립 중괄호는 콤마 나열.")

# p29 — 로그 연립방정식
add(id="83604bbd", qtype="short",
    question=("연립방정식 [[log(3, x) + log(5, y) = 5]], [[log(3, x) × log(5, y) = 6]]의 해가 "
              "[[x = alpha]], [[y = beta]]일 때, [[alpha - beta]]의 값을 구하시오. (단, [[alpha > beta]])"),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="(log₃x, log₅y) = (3,2) → (27, 25) → α−β = 2 = 빠른정답 ✓. 연립 중괄호는 콤마 나열.")

# p43 — 절대 등급과 광도
add(id="3e698888", qtype="choice",
    question=("별의 밝기를 나타내는 방법으로 절대 등급과 광도가 있다. 임의의 두 별 [[A]], [[B]]에 대하여 별 [[A]]의 절대 등급과 광도를 "
              "각각 [[sub(M,A)]], [[sub(L,A)]]라 하고, 별 [[B]]의 절대 등급과 광도를 각각 [[sub(M,B)]], [[sub(L,B)]]라 하면 "
              "다음과 같은 관계식이 성립한다고 한다.\n"
              "[[sub(M,A) - sub(M,B) = -2.5 log(frac(sub(L,A), sub(L,B)))]] (단, 광도의 단위는 W이다.)\n"
              "절대 등급이 6.2인 별의 광도가 [[L]]일 때, 절대 등급이 2.2인 별의 광도는 [[k L]]이다. 상수 [[k]]의 값은?"),
    choices=["[[pow(10, frac(4,5))]]", "[[10]]", "[[pow(10, frac(6,5))]]", "[[pow(10, frac(7,5))]]", "[[pow(10, frac(8,5))]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2020년 6월 고2 13번 변형]. 2.2−6.2 = −2.5 log k → log k = 8/5 → ⑤. 빠른정답 4와 불일치.")

# p72 — 로그부등식 연립 (가우스 기호)
add(id="7df3caa2", qtype="choice",
    question=("두 집합\n"
              "[[A = setb(x, pow(floor(log(5, x)), 2) - 4 floor(log(5, x)) + 3 < 0)]]\n"
              "[[B = setb(x, log(0.2, frac(x, 4) - 5) >= -2)]]\n"
              "에서 [[inter(A, B) = setb(x, pow(x,2) + a x + b <= 0)]]일 때, [[a + b]]의 값은? "
              "(단, [[a]], [[b]]는 상수이고, [[floor(x)]]는 [[x]]보다 크지 않은 최대의 정수이다.)"),
    choices=["[[2805]]", "[[2830]]", "[[2855]]", "[[2880]]", "[[2905]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="A: [log₅x]=2 → 25≤x<125, B: 20<x≤120 → 25≤x≤120 → (x−25)(x−120) → a+b = −145+3000 = 2855 → ③ = 빠른정답 ✓.")

# p90 — 로그부등식의 활용 (서로 다른 두 실근)
add(id="65c59c45", qtype="short",
    question=("방정식 [[(log(x) + log(5))(log(x) + log(125)) = -pow(log(k), 2)]]이 서로 다른 두 실근을 갖도록 하는 "
              "양수 [[k]]의 값의 범위가 [[alpha < k < beta]]일 때, [[alpha beta]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.9,
    note="t=log x: t²+4Lt+3L²+(log k)²=0 (L=log5), D>0 → (log k)² < L² → 1/5 < k < 5 → αβ = 1. 빠른정답 8과 불일치.")

# ───────────────────────── 사인법칙과 코사인법칙 ─────────────────────────
# p1 — 사인법칙 (보기에서 찾기)
add(id="df2201ec", qtype="short",
    question=("삼각형 ABC에서 [[c = 4]], [[B = deg(60)]], [[C = deg(30)]]일 때, 다음 보기 중 [[b]]의 값을 찾으시오.\n<보기>\n"
              "ㄱ. [[4]]\nㄴ. [[4 sqrt(2)]]\nㄷ. [[4 sqrt(3)]]\nㄹ. [[8]]\nㅁ. [[8 sqrt(3)]]"),
    choices=None, derived_answer="ㄷ", figure=None, difficulty_est=1, confidence=0.9,
    note="b = c·sinB/sinC = 4·(√3/2)/(1/2) = 4√3 → ㄷ. 빠른정답 'E'(값 아님)와 불일치.")

# p4 — 사인법칙 (각의 이등분 아님, BD:DC)
add(id="dd73ef76", qtype="short",
    question=("다음 그림과 같은 삼각형 ABC에서 변 BC 위에 점 D를 잡을 때, [[seg(AB) = 4]], [[seg(AC) = 3]], "
              "[[angle(BAD) = deg(45)]], [[angle(DAC) = deg(30)]]이다. [[ratio(seg(BD), seg(DC)) = ratio(k, 3 sqrt(2))]]일 때, "
              "자연수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="8",
    figure=unsup("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), BC 위의 점 D, AB = 4, AC = 3, ∠BAD = 45°, ∠DAC = 30°"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형과 내부 선분 AD 그림",
    note="BD:DC = AB·sin45° : AC·sin30° = 2√2 : 3/2 = 8 : 3√2 → k = 8. 빠른정답 'E'(값 아님)와 불일치.")

# p6 — 사인법칙 (∠B)
add(id="9ed46dd1", qtype="short",
    question=("삼각형 ABC에 대하여 다음을 구하시오.\n"
              "[[a = 9]], [[b = 3 sqrt(3)]], [[A = deg(120)]]일 때, [[angle(B)]]의 크기"),
    choices=None, derived_answer="deg(30)", figure=None, difficulty_est=1, confidence=0.9,
    note="sinB = b·sinA/a = 1/2, B < 60° → 30°. 빠른정답 없음.")

# p15 — 사인법칙의 변형 (비례식)
add(id="d00adabd", qtype="choice",
    question=("[[tri(ABC)]]에서 [[ratio((2a - b), (2b - c), (2c - a)) = ratio(9, 1, 4)]]일 때, "
              "[[ratio(sin(A), sin(B), sin(C))]]는?"),
    choices=["[[ratio(3, 6, 7)]]", "[[ratio(5, 6, 8)]]", "[[ratio(5, 7, 3)]]", "[[ratio(6, 3, 5)]]", "[[ratio(6, 4, 7)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="2a−b=9k, 2b−c=k, 2c−a=4k → a:b:c = 6:3:5 → ④. 빠른정답 없음.")

# p16 — 사인법칙의 변형 (연립 조건)
add(id="bd0bf94c", qtype="choice",
    question="[[tri(ABC)]]에서 [[a + b - 2c = 0]], [[a - 3b + c = 0]]일 때, [[ratio(sin(A), sin(B), sin(C))]]는?",
    choices=["[[ratio(3, 5, 4)]]", "[[ratio(4, 3, 5)]]", "[[ratio(5, 3, 4)]]", "[[ratio(5, 7, 3)]]", "[[ratio(7, 5, 3)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="a = 5c/4, b = 3c/4 → 5:3:4 → ③. 빠른정답 없음.")

# p22 — 삼각형의 모양 결정(1)
add(id="dd2b37d5", qtype="choice",
    question="삼각형 ABC에서 [[a sin(A) = c sin(C)]]가 성립할 때, 삼각형 ABC는 어떤 삼각형인가?",
    choices=["정삼각형", "[[a = c]]인 이등변삼각형", "[[b = c]]인 이등변삼각형",
             "[[angle(A) = deg(90)]]인 직각삼각형", "[[angle(C) = deg(90)]]인 직각삼각형"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="a² = c² → a = c → ②. 빠른정답 137(정렬 어긋남)과 불일치.")

# p23 — 삼각형의 모양 결정(1)
add(id="89c795f2", qtype="choice",
    question="[[tri(ABC)]]에서 [[a sin(A) = b sin(B)]]가 성립할 때, [[tri(ABC)]]는 어떤 삼각형인가?",
    choices=["정삼각형", "[[a = c]]인 이등변삼각형", "[[a = b]]인 이등변삼각형",
             "[[angle(A) = deg(90)]]인 직각삼각형", "[[angle(B) = deg(90)]]인 직각삼각형"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="a² = b² → a = b → ③. 빠른정답 15와 불일치.")

# p29 — 사인법칙의 활용 (울타리)
add(id="ca4c76fd", qtype="choice",
    question=("다음 그림과 같이 세 지점 A, B, C에서 두 지점 A, B 사이의 거리는 65 m이고, [[angle(ABC) = deg(103)]], "
              "[[angle(CAB) = deg(46)]]이다. 세 지점 A, B, C를 울타리로 이으려고 할 때, 두 지점 B, C 사이의 거리는?\n"
              "(단, [[sin(deg(31)) = 0.52]], [[sin(deg(46)) = 0.72]]로 계산한다.)"),
    choices=["[[80]] m", "[[85]] m", "[[90]] m", "[[95]] m", "[[100]] m"],
    derived_answer="③",
    figure=unsup("삼각형 ABC(C 왼쪽 위, B 오른쪽 위, A 오른쪽 아래), AB = 65 m, ∠B = 103°, ∠A = 46°"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 측량 그림",
    note="C = 31°, BC = 65·0.72/0.52 = 90 → ③. 빠른정답 없음.")

# p30 — 사인법칙의 활용 (배)
add(id="c2eec843", qtype="choice",
    question=("다음 그림과 같이 배 A는 배 B에서 정북 방향으로 620m 떨어져 있다. 두 배 A, B가 동시에 정북에서 동쪽으로 "
              "각각 [[deg(43)]], [[deg(25)]] 방향으로 이동하여 지점 C에서 조업했을 때, 배 A가 지점 C까지 이동한 거리는?\n"
              "(단, [[sin(deg(18)) = 0.31]], [[sin(deg(25)) = 0.42]], [[sin(deg(43)) = 0.68]]로 계산한다.)"),
    choices=["[[760]]m", "[[800]]m", "[[840]]m", "[[880]]m", "[[920]]m"],
    derived_answer="③",
    figure=unsup("방위 표시(N·E·S·W), 배 A(위)·B(아래)가 남북으로 620 m, A에서 북 기준 43°, B에서 북 기준 25° 방향의 선분이 C에서 만남"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 방위·배 위치 삽화",
    note="∠A = 137°, ∠B = 25°, ∠C = 18° → AC = 620·0.42/0.31 = 840 → ③. 빠른정답 없음.")

# p31 — 사인법칙의 활용 (울타리, l)
add(id="ec2ac94b", qtype="short",
    question=("다음 그림과 같이 세 지점 A, B, C에서 두 지점 A, B 사이의 거리는 290 m이고, [[angle(ABC) = deg(100)]], "
              "[[angle(CAB) = deg(54)]]이다. 세 지점 A, B, C를 울타리로 이으려고 할 때, 두 지점 B, C 사이의 거리가 [[l]] m라 한다. "
              "이때 [[l]]의 값을 구하시오.\n(단, [[sin(deg(54)) = 0.81]], [[sin(deg(26)) = 0.45]]로 계산한다.)"),
    choices=None, derived_answer="522",
    figure=unsup("삼각형 ABC(C 왼쪽 위, B 오른쪽 위, A 오른쪽 아래), AB = 290 m, ∠B = 100°, ∠A = 54°"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 측량 그림",
    note="C = 26°, BC = 290·0.81/0.45 = 522 = 빠른정답 ✓.")

# p32 — 사인법칙의 활용 (외접원 넓이)
add(id="4d17e04d", qtype="choice",
    question=("다음 그림과 같이 [[50 sqrt(2)]] m 떨어진 두 지점 A, B에서 정자가 있는 C지점을 바라보고 측량하였더니 "
              "[[angle(CAB) = deg(105)]], [[angle(CBA) = deg(30)]]이었다. 세 지점 A, B, C를 연결하는 원 모양의 잔디밭을 "
              "만들려고 할 때, 잔디밭의 넓이는?"),
    choices=["[[625 pi]] m²", "[[2500 pi]] m²", "[[3600 pi]] m²", "[[4900 pi]] m²", "[[6400 pi]] m²"],
    derived_answer="②",
    figure=unsup("삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽), AB = 50√2 m, ∠A = 105°, ∠B = 30°"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 측량 그림",
    note="C = 45°, 2R = 50√2/sin45° = 100 → R = 50 → 2500π → ②. 빠른정답 없음.")

# p35 — 코사인법칙 (보기에서 찾기)
add(id="675885a4", qtype="short",
    question=("삼각형 ABC에서 [[b = 8]], [[c = 10]], [[A = deg(120)]]일 때, 다음 보기 중 [[a]]의 값을 찾으시오.\n<보기>\n"
              "ㄱ. [[2 sqrt(61)]]\nㄴ. [[12]]\nㄷ. [[10]]\nㄹ. [[6 sqrt(2)]]\nㅁ. [[sqrt(61)]]"),
    choices=None, derived_answer="ㄱ", figure=None, difficulty_est=1, confidence=0.9,
    note="a² = 64+100+80 = 244 → a = 2√61 → ㄱ. 빠른정답 없음.")

# p43 — 코사인법칙의 변형 (정사각형 내분점)
add(id="4d0dfd22", qtype="choice",
    question=("다음 그림과 같이 정사각형 ABCD의 두 변 AD, CD를 [[ratio(1, 3)]]으로 내분하는 점을 각각 E, F라 하자.\n"
              "[[angle(EBF) = theta]]라 할 때, [[cos(theta)]]의 값은?"),
    choices=["[[frac(4, 17)]]", "[[frac(sqrt(30), 17)]]", "[[frac(8, 17)]]", "[[frac(sqrt(83), 17)]]", "[[frac(10 sqrt(2), 17)]]"],
    derived_answer="③",
    figure=unsup("정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), AD 위의 점 E(A 쪽), CD 위의 점 F(C 쪽), 선분 BE·BF, ∠EBF = θ"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형과 내부 선분 그림",
    note="한 변 4: BE=(1,4), BF=(4,1) → cosθ = 8/17 → ③. 빠른정답 없음.")

# p45 — 코사인법칙의 변형 (사다리꼴 대각선)
add(id="6947ddd2", qtype="choice",
    question=("다음 그림과 같이 [[seg(AD)]]와 [[seg(BC)]]가 평행한 사다리꼴 ABCD에서 [[seg(AB) = 17]], [[seg(BC) = 25]], "
              "[[seg(CD) = 10]], [[seg(DA) = 4]]일 때, [[seg(AC)]]의 길이는?"),
    choices=["[[4 sqrt(10)]]", "[[2 sqrt(41)]]", "[[2 sqrt(42)]]", "[[2 sqrt(43)]]", "[[4 sqrt(11)]]"],
    derived_answer="②",
    figure=unsup("사다리꼴 ABCD(A·D 위, B·C 아래, AD ∥ BC), AB = 17, BC = 25, CD = 10, AD = 4, 대각선 AC"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사다리꼴 그림",
    note="B(0,0), C(25,0), A(15,8) → AC² = 100+64 = 164 → 2√41 → ②. 빠른정답 없음.")

# p47 — 최대각·최소각 (정사각뿔, sin²θ)
add(id="a9aba9e1", qtype="choice",
    question=("그림과 같이 모든 모서리의 길이가 2인 정사각뿔이 있다. 모서리 OC 위를 움직이는 점 P에 대하여 [[angle(BPD) = theta]]라 할 때, "
              "[[pow(sin(theta), 2)]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 하자.\n[[M - m]]의 값은?"),
    choices=["[[frac(1, 9)]]", "[[frac(2, 9)]]", "[[frac(1, 3)]]", "[[frac(4, 9)]]", "[[frac(5, 9)]]"],
    derived_answer="①",
    figure=unsup("정사각뿔 O-ABCD(모든 모서리 2), 모서리 OC 위의 점 P, 선분 PB·PD, ∠BPD = θ"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각뿔 입체도형",
    note="BD = 2√2; P가 끝점이면 θ = 90°(sin²=1), PB 최소 √3일 때 cosθ = −1/3 → sin² = 8/9 → M−m = 1/9 → ①. 빠른정답 없음.")

# p51 — 최대각·최소각 (정사각뿔, sinθ 곱)
add(id="ef79b7b2", qtype="choice",
    question=("다음 그림과 같이 모든 모서리의 길이가 1인 정사각뿔이 있다. 모서리 EC 위를 움직이는 점 P에 대하여 "
              "[[angle(BPD) = theta]]라고 할 때, [[sin(theta)]]의 최댓값과 최솟값의 곱은?"),
    choices=["[[-frac(2 sqrt(2), 3)]]", "[[-frac(sqrt(2), 3)]]", "[[0]]", "[[frac(sqrt(2), 3)]]", "[[frac(2 sqrt(2), 3)]]"],
    derived_answer="⑤",
    figure=unsup("정사각뿔 E-ABCD(모든 모서리 1), 모서리 EC 위의 점 P, 선분 PB·PD, ∠BPD = θ"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각뿔 입체도형",
    note="최댓값 1(끝점, 직각), 최솟값: PB 최소 √3/2일 때 cosθ = −1/3 → sinθ = 2√2/3 → 곱 2√2/3 → ⑤. 빠른정답 없음.")

# p55 — 사인법칙과 코사인법칙 (A의 값)
add(id="be6710b3", qtype="short",
    question="[[ratio(sin(A), sin(B), sin(C)) = ratio(13, 7, 8)]]일 때, [[A]]의 값을 구하시오.",
    choices=None, derived_answer="deg(120)", figure=None, difficulty_est=2, confidence=0.75,
    needs_review="이미지 상단 잘림 의심(첫 줄이 위 가장자리에 붙어 있음; '삼각형 ABC에서' 등 앞부분 누락 가능) — 보이는 부분만 전사",
    note="a:b:c = 13:7:8 → cosA = (49+64−169)/112 = −1/2 → A = 120°. 빠른정답 없음.")

# p57 — 반원과 두 현 (AC·AE)
add(id="695f83ea", qtype="choice",
    question=("다음 그림과 같이 선분 AB를 지름으로 하는 반원의 호 AB 위에 두 점 C, D가 있다. 선분 AB의 중점 O에 대하여 "
              "두 선분 AD, CO가 점 E에서 만나고, [[seg(CE) = 2 sqrt(2)]], [[seg(ED) = 3]], [[angle(CEA) = frac(3,4) pi]]이다.\n"
              "[[seg(AC) × seg(AE)]]의 값은?"),
    choices=["[[5 sqrt(5)]]", "[[6 sqrt(5)]]", "[[6 sqrt(10)]]", "[[8 sqrt(5)]]", "[[8 sqrt(10)]]"],
    derived_answer="⑤",
    figure=unsup("반원(지름 AB, 중심 O), 호 위의 점 C(위)·D(오른쪽), 선분 AC·AD·CD·CO, AD와 CO의 교점 E, ∠CEA = 3π/4"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 반원·현·교점 복합 도형",
    note="출처 [2022년 9월 고3 13번 변형]. △OED 코사인법칙 → R = 5√2/2, OE = √2/2, AE = 4, AC = 2√10 → 8√10 → ⑤ (수치 검산 일치). 빠른정답 없음.")

# p60 — 내접 삼각형과 각의 이등분선 (보기) (id 2개)
dup(["cb583953", "6888b5ab"], qtype="choice",
    question=("반지름의 길이가 [[sqrt(3)]]인 원 [[C]]에 내접하는 삼각형 ABC에 대하여 [[angle(BAC)]]의 이등분선이 원 [[C]]와 만나는 점 중 "
              "A가 아닌 점을 D라 하고, 두 선분 BC, AD의 교점을 E라 하자. [[seg(BD) = sqrt(3)]]일 때, <보기>에서 옳은 것만을 "
              "있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[sin(angle(DBE)) = frac(1, 2)]]\n"
              "ㄴ. [[pow(seg(AB), 2) + pow(seg(AC), 2) = seg(AB) × seg(AC) + 9]]\n"
              "ㄷ. 삼각형 ABC의 넓이가 삼각형 BDE의 넓이의 4배가 되도록 하는 모든 [[seg(BE)]]의 값의 합은 [[frac(9, 4)]]이다."),
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤",
    figure=unsup("원 C에 내접하는 삼각형 ABC(A 왼쪽 아래, B 오른쪽 아래, C 위), ∠A의 이등분선 AD(D는 오른쪽 호 위), AD와 BC의 교점 E, 선분 BD"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원·내접삼각형·이등분선 복합 도형",
    note="출처 [2022년 11월 고2 20번/4점]. ∠BAD = 30° → ㄱ✓, BC = 3, A = 60° → ㄴ✓, ㄷ: sin2C = √3/6인 두 경우 BE 합 = 9/4 ✓ → ⑤. 빠른정답 없음.")

# p61 — 삼각형의 모양 결정(2)
add(id="88fb10f6", qtype="choice",
    question="[[tri(ABC)]]에서 [[sin(A) = 2 sin(B) cos(C)]]가 성립할 때,\n[[tri(ABC)]]는 어떤 삼각형인가?",
    choices=["[[a = b]]인 이등변삼각형", "[[b = c]]인 이등변삼각형", "정삼각형",
             "[[B = deg(90)]]인 직각삼각형", "[[C = deg(90)]]인 직각삼각형"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="a = 2b·(a²+b²−c²)/(2ab) → b² = c² → b = c → ②. 빠른정답 없음.")

# p62 — 삼각형의 모양 결정(2)
add(id="ae7e18fa", qtype="choice",
    question="삼각형 ABC에서 [[sin(A) = sin(B) cos(C)]]가 성립할 때,\n이 삼각형은 어떤 삼각형인가?",
    choices=["[[A = deg(90)]]인 직각삼각형", "[[B = deg(90)]]인 직각삼각형", "[[C = deg(90)]]인 직각삼각형",
             "[[a = b]]인 이등변삼각형", "[[b = c]]인 이등변삼각형"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="2a² = a²+b²−c² → b² = a²+c² → B = 90° → ②. 빠른정답 없음.")

# p68 — 코사인법칙의 활용 (다리)
add(id="dae7bf9c", qtype="short",
    question=("다음 그림과 같이 지면에서 [[20 sqrt(3)]] m 위에 있는 두 지점 A, B를 잇는 다리가 있다. 지면 위의 지점 C에서 "
              "지점 A를 올려본 각의 크기는 [[deg(60)]]이고, 지점 B를 올려본 각의 크기는 [[deg(30)]]이다. [[angle(ACB) = deg(30)]]일 때, "
              "두 지점 A, B 사이의 거리는 몇 m인지 구하시오."),
    choices=None, derived_answer="40",
    figure=unsup("아치 3개짜리 다리 위의 두 지점 A(왼쪽)·B(오른쪽), 높이 20√3 m, 지면 위 점 C에서 A·B를 올려본 각 60°·30°, ∠ACB = 30°, 직각 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 다리 삽화 + 공간 삼각형 그림",
    note="CA = 40, CB = 40√3 → AB² = 1600 + 4800 − 2·40·40√3·cos30° = 1600 → 40 m. 빠른정답 60과 불일치.")

# p74 — 삼각형의 넓이 (이등분 선분 PQ 최솟값)
add(id="3f297873", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 8]], [[seg(AC) = 9]]이고, [[angle(A) = deg(60)]]인 삼각형 ABC가 있다.\n"
              "두 선분 AB, AC위에 각각 점 P, Q를 잡을 때, 삼각형 ABC의 넓이가 이등분되는 선분 PQ의 길이의 최솟값을 구하시오."),
    choices=None, derived_answer="6",
    figure=unsup("삼각형 ABC(A 위, ∠A = 60°, AB = 8, AC = 9), AB 위의 점 P, AC 위의 점 Q, 선분 PQ"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형과 내부 선분 PQ 그림",
    note="AP·AQ = 36, PQ² = AP²+AQ²−AP·AQ ≥ AP·AQ = 36 → 최솟값 6(AP=AQ=6). 빠른정답 60과 불일치.")

# p80 — 사각형의 넓이(1)
add(id="3f98233b", qtype="choice",
    question=("그림과 같이 [[seg(AB) = 5]], [[seg(BC) = 8]], [[seg(CD) = seg(DA) = 3]]이고 [[A = frac(2,3) pi]]인 "
              "사각형 ABCD의 넓이는?"),
    choices=["[[frac(31 sqrt(3), 4)]]", "[[frac(33 sqrt(3), 4)]]", "[[frac(35 sqrt(3), 4)]]", "[[frac(37 sqrt(3), 4)]]", "[[frac(39 sqrt(3), 4)]]"],
    derived_answer="⑤",
    figure=unsup("사각형 ABCD(A 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), AB = 5, BC = 8, CD = DA = 3, ∠A = 2π/3"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각형 그림",
    note="BD = 7, △BCD: cosC = 1/2 → 넓이 15√3/4 + 24√3/4 = 39√3/4 → ⑤. 빠른정답 없음.")

# p82 — 원에 내접하는 사각형 (S²/54)
add(id="8b5b3868", qtype="short",
    question=("다음 그림과 같이 반지름의 길이가 [[6 sqrt(2)]]인 원에 내접하는 사각형 ABCD에 대하여 [[seg(AB) = seg(CD) = 4 sqrt(2)]], "
              "[[seg(BD) = 9 sqrt(3)]]일 때, 사각형 ABCD의 넓이를 [[S]]라 하자.\n[[frac(pow(S, 2), 54)]]의 값을 구하시오."),
    choices=None, derived_answer="108",
    figure=unsup("원에 내접하는 사각형 ABCD(A 왼쪽 아래, B 아래, C 오른쪽, D 위), AB = CD = 4√2, 대각선 BD = 9√3, 내부 음영"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 원과 내접 사각형 그림",
    note="출처 [2019년 11월 고2 이과 28번 변형]. AB = CD → 등변사다리꼴, sinA = 3√6/8, AD+BC = 12√6 → S = 54√2 → S²/54 = 108 (수치 검산 일치). 빠른정답 143과 불일치.")

# p83 — 도형 ABCDE의 넓이
add(id="8911770e", qtype="short",
    question=("다음 그림과 같이 도형 ABCDE에서 [[angle(ACB) = angle(ACD) = deg(60)]], [[seg(AC) = seg(DE) = 3]], "
              "[[seg(BC) = seg(CD) = 5]], [[seg(AE) = 7]]이다.\n"
              "이 도형 ABCDE의 넓이를 [[S]]라 하자. [[pow(S, 2) = frac(q, p)]]일 때, [[p + q]]의 값을 구하시오.\n"
              "(단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="4579",
    figure=unsup("오각형 ABCDE(B 왼쪽 위, C 왼쪽 아래, D 아래, E 오른쪽, A 가운데 위), 선분 AC·AD, ∠ACB = ∠ACD = 60°, AC = 3, BC = CD = 5, DE = 3, AE = 7"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 오각형과 내부 선분 그림",
    note="△ACB = △ACD = 15√3/4, AD = √19, △ADE = 9√3/4 → S = 39√3/4, S² = 4563/16 → 4579. 빠른정답 없음(다음 문항 p86의 빠른정답 4579가 이 값).")

# p86 — 반원 위의 점 (보기)
add(id="5f3a0193", qtype="choice",
    question=("길이가 24인 선분 AB를 지름으로 하는 반원의 호 AB 위에 점 C를 [[seg(BC) = 8]]이 되도록 잡는다. "
              "점 D가 호 AC 위의 점일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은? (단, 점 D는 점 A와 점 C가 아닌 점이다.)\n<보기>\n"
              "ㄱ. [[sin(angle(CBA)) = frac(2 sqrt(2), 3)]]\n"
              "ㄴ. [[seg(CD) = 12]]일 때, [[seg(AD) = -4 + 8 sqrt(6)]]\n"
              "ㄷ. 사각형 ABCD의 넓이의 최댓값은 [[128 sqrt(2)]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤",
    figure=unsup("반원(지름 AB, A 왼쪽·B 오른쪽), 호 위의 점 C(오른쪽 위)·D(왼쪽 위), 선분 AD·DC·CB"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 반원과 내접 사각형 그림",
    note="출처 [2022년 7월 고3 14번 변형]. AC = 16√2 → ㄱ✓; cos∠ADC = −1/3 → AD²+8AD−368=0 → ㄴ✓; 최대 64√2+64√2 → ㄷ✓ → ⑤. 빠른정답 4579(정렬 어긋남)와 불일치.")

# p88 — 평행사변형의 넓이
add(id="7481f638", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[seg(AB) = 5]], [[seg(BC) = 10]], [[C = deg(150)]]일 때, "
              "이 평행사변형의 넓이를 구하시오."),
    choices=None, derived_answer="25",
    figure=unsup("평행사변형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), AB = 5, BC = 10, ∠C = 150°, 내부 음영"),
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형 그림",
    note="5·10·sin150° = 25. 빠른정답 없음.")

# p90 — 평행사변형의 넓이 (대각선)
add(id="ea8d69b5", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 5]], [[seg(BC) = 3]]인 평행사변형 ABCD에서 [[seg(AC) = sqrt(58)]]일 때, "
              "사각형 ABCD의 넓이를 구하시오."),
    choices=None, derived_answer="9",
    figure=unsup("평행사변형 ABCD(A 왼쪽 위, D 위, B 아래, C 오른쪽 아래), AB = 5, BC = 3, 대각선 AC = √58, 내부 음영"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형 그림",
    note="cosB = (25+9−58)/30 = −4/5, sinB = 3/5 → 5·3·(3/5) = 9. 빠른정답 24와 불일치.")

# p91 — 평행사변형의 넓이 (B의 크기)
add(id="098a7b8b", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 4]], [[seg(BC) = 6]]이고 넓이가 [[12 sqrt(3)]]인 평행사변형 ABCD에서 [[B]]의 크기를 구하시오.\n"
              "(단, [[B]]는 예각이다.)"),
    choices=None, derived_answer="deg(60)",
    figure=unsup("평행사변형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), AB = 4, BC = 6"),
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형 그림",
    note="24 sinB = 12√3 → sinB = √3/2, 예각 → 60°. 빠른정답 없음.")

# p99 — 사각형의 넓이(2) 대각선 이용 (이미지에 문항 2개, id 1개)
add(id="586d76ad", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[seg(AB) = 4]], [[seg(AD) = 9]]이고 두 대각선 AC와 BD가 이루는 각의 크기가 "
              "[[deg(135)]]일 때, 평행사변형 ABCD의 넓이를 구하시오."),
    choices=None, derived_answer="frac(65,2)",
    figure=unsup("평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB = 4, AD = 9, 두 대각선의 교각 135°, 내부 음영"),
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 평행사변형·대각선 그림 / 이미지에 별개 문항 2개 인쇄(아래 문항: AB=1, BC=2, B=π/3인 평행사변형의 두 대각선이 이루는 각 θ에 대한 sin²θ 선지형 ①1/7~⑤5/7, 답 ④) — id 1개라 빠른정답(65/2)에 맞는 위 문항만 전사",
    note="pq cosα = 65/4(반대각선 반씩 p, q), 넓이 = 2pq sinα = 65/2 = 빠른정답 ✓.")

# ───────────────────────── 등비수열 ─────────────────────────
# p1 — 등비수열의 일반항 (공비)
add(id="3291937b", qtype="short",
    question=("다음을 만족시키는 등비수열 [[set(sub(a,n))]]의 공비를 구하시오.\n(단, 공비는 양의 실수이다.)\n"
              "[[sub(a,1) = 10]], [[sub(a,4) = 0.01]]"),
    choices=None, derived_answer="0.1", figure=None, difficulty_est=1, confidence=0.9,
    note="r³ = 0.001 → r = 0.1 = 빠른정답 ✓.")

# p7 — 빈칸에 알맞은 수
add(id="f84db681", qtype="short",
    question=("다음 수열이 등비수열이 되도록 □ 안에 알맞은 수를 써넣으시오.\n"
              "[[25]], [[5]], □, [[frac(1,5)]], [[frac(1,25)]], ⋯"),
    choices=None, derived_answer="1", figure=None, difficulty_est=1, confidence=0.9,
    note="공비 1/5 → □ = 1 = 빠른정답 ✓. 빈칸 상자는 텍스트 □.")

# p16 — 조건을 만족시키는 항
add(id="aefe97c6", qtype="choice",
    question=("[[sub(a,3) = 4]], [[sub(a,5) = 8]]이고 공비가 양수인 등비수열 [[set(sub(a,n))]]에 대하여 "
              "[[pow(sub(a,n), 2) > 1000]]을 만족시키는 자연수 [[n]]의 최솟값은?"),
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="r = √2, aₙ² = 16·2^(n−3) = 2^(n+1) > 1000 → n+1 ≥ 10 → n = 9 → ⑤. 빠른정답 8과 불일치.")

# p27 — 등비중항
add(id="dac21f06", qtype="choice",
    question=("등비수열 [[set(sub(a,n))]]에 대하여 [[sub(a,3) = sqrt(5)]]일 때,\n"
              "[[sub(a,1) × sub(a,2) × sub(a,4) × sub(a,5)]]의 값은?"),
    choices=["[[sqrt(5)]]", "[[5]]", "[[5 sqrt(5)]]", "[[25]]", "[[25 sqrt(5)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2011년 6월 고3 문과 8번/3점]. a₁a₅ = a₂a₄ = a₃² = 5 → 25 → ④ = 빠른정답 ✓.")

# p34 — 등차중항과 등비중항
add(id="de379777", qtype="choice",
    question=("네 실수 [[a]], [[x]], [[y]], [[b]]가 이 순서대로 등차수열을 이루고, 네 실수 [[a]], [[p]], [[q]], [[b]]가 이 순서대로 "
              "등비수열을 이룬다. [[x + y = 7]], [[p q = 5]]일 때, 실수 [[a]], [[b]]에 대하여 [[pow(a,3) + pow(b,3)]]의 값은?"),
    choices=["[[208]]", "[[218]]", "[[228]]", "[[238]]", "[[248]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a+b = 7, ab = 5 → a³+b³ = 343 − 105 = 238 → ④ = 빠른정답 ✓.")

# p49 — 등차수열과 등비수열
add(id="b7951f28", qtype="short",
    question=("등차수열 [[set(sub(a,n))]]과 공비가 1보다 작은 등비수열 [[set(sub(b,n))]]이\n"
              "[[sub(a,1) + sub(a,8) = 8]], [[sub(b,2) sub(b,7) = 12]], [[sub(a,4) = sub(b,4)]], [[sub(a,5) = sub(b,5)]]\n"
              "를 모두 만족시킬 때, [[sub(a,1)]]의 값을 구하시오."),
    choices=None, derived_answer="18", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2016년 10월 고3 문과 27번/4점]. b₄+b₅ = 8, b₄b₅ = 12, r<1 → b₄=6, b₅=2 → d=−4 → a₁ = 18. 빠른정답 117과 불일치.")

# p55 — 등비수열의 활용 (평행사변형 접기)
add(id="b63fade3", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 21]]인 평행사변형 ABCD가 있다. 이 도형을 대각선 BD를 접는 선으로 하여 접어서 생기는 "
              "삼각형 EBC의 넓이가 평행사변형 ABCD의 넓이의 [[frac(3, 14)]]이고, [[seg(CE)]], [[seg(EB)]], [[seg(BD)]]의 길이가 "
              "이 순서대로 등비수열을 이룰 때, [[pow(seg(AD), 2)]]의 값을 구하시오."),
    choices=None, derived_answer="249",
    figure=unsup("평행사변형 ABCD(A 왼쪽 아래, B 오른쪽 아래, D 왼쪽 위, C 오른쪽 위)를 대각선 BD로 접은 그림, A의 대응점 A′(위), 접힌 변 BA′가 DC와 만나는 점 E, AB = 21"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 평행사변형 접기 그림(프라임 점 A′ 포함)",
    note="EB = ED, CE:CD = 3/7 → CE = 9, EB = 12, BD = 16 → cos∠BEC = −1/9 → BC² = AD² = 249 (좌표 검산 일치). 빠른정답 100과 불일치.")

# p59 — 등비수열의 합(1) (로그 항)
add(id="2d541ee9", qtype="choice",
    question=("등비수열 [[log(3, 9)]], [[log(3, pow(9, 3))]], [[log(3, pow(9, 9))]], [[log(3, pow(9, 27))]], ⋯의\n"
              "첫째항부터 제10항까지의 합은?"),
    choices=["[[pow(2, 9) - 1]]", "[[pow(2, 10) - 1]]", "[[pow(3, 9) - 1]]", "[[pow(3, 10) - 1]]", "[[2 × pow(3, 10) - 1]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="항: 2, 6, 18, 54, … = 2·3^(n−1) → S₁₀ = 3¹⁰ − 1 → ④. 빠른정답 2와 불일치.")

# p74 — 등비수열의 합(3) (|2 − Sₙ| < 0.01)
add(id="45102bac", qtype="choice",
    question=("등비수열 [[1]], [[frac(1,2)]], [[frac(1,4)]], ⋯에서 첫째항부터 제[[n]]항까지의 합을 [[sub(S,n)]]이라 할 때, "
              "[[abs(2 - sub(S,n)) < 0.01]]을 만족시키는 [[n]]의 최솟값은?"),
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="|2−Sₙ| = (1/2)^(n−1) < 0.01 → 2^(n−1) > 100 → n = 8 → ③. 빠른정답 4와 불일치.")

# p75 — 등비수열의 합(3) (13S₁+S₃+S₄=0)
add(id="683d2ebc", qtype="short",
    question=("첫째항이 양수인 등비수열 [[set(sub(a,n))]]의 첫째항부터 제[[n]]항까지의 합을 [[sub(S,n)]]이라 하자.\n"
              "[[sub(a,2) = -12]], [[13 sub(S,1) + sub(S,3) + sub(S,4) = 0]]일 때, [[sub(a,5)]]의 값을 구하시오."),
    choices=None, derived_answer="324", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2025년 9월 고2 26번 변형]. r³+2r²+2r+15 = (r+3)(r²−r+5) = 0 → r = −3, a₁ = 4 → a₅ = 324. 빠른정답 3과 불일치.")

# ───────────────────────── 거듭제곱과 거듭제곱근 ─────────────────────────
# p6 — 거듭제곱근 (집합 C의 원소 개수)
add(id="f8c82d41", qtype="short",
    question=("실수 전체의 집합의 부분집합 [[A]], [[B]], [[C]]를\n"
              "[[A = set(-5, -4, 4, 5)]],\n"
              "[[B = setb(abs(a), in(a, A))]],\n"
              "[[C]] = { [[x]] | [[x = root(b, a)]], [[in(a, A)]], [[in(b, B)]] }\n"
              "라 할 때, 집합 [[C]]의 원소의 개수를 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.85,
    note="B = {4, 5}; b=4(짝수)는 a>0일 때만 실수 → ⁴√4, ⁴√5, ⁵√(−5), ⁵√(−4), ⁵√4, ⁵√5 → 6개. 빠른정답 3과 불일치.")

# p15 — 거듭제곱근 (n(A)=7, n(B)=11)
add(id="bec97e04", qtype="short",
    question=("집합 [[U]] = { [[x]] | [[-8 <= x <= 8]], [[x]]는 정수 }의 공집합이 아닌 부분집합 [[X]]에 대하여 두 집합 [[A]], [[B]]를\n"
              "[[A]] = { [[a]] | [[a]]는 [[x]]의 실수인 다섯제곱근, [[in(x, X)]] },\n"
              "[[B]] = { [[b]] | [[b]]는 [[x]]의 실수인 제곱근, [[in(x, X)]] }라 하자.\n"
              "[[card(A) = 7]], [[card(B) = 11]]이 되도록 하는 집합 [[X]]의 모든 원소의 합의 최댓값을 구하시오."),
    choices=None, derived_answer="29", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2024년 5월 고3 19번 변형]. n(X) = 7; n(B) = 2·(양수 개수) + (0 포함) = 11 → 양수 5개, 0, 음수 1개 → 8+7+6+5+4+0−1 = 29. 빠른정답 −4와 불일치.")

# p29 — 거듭제곱근의 계산 (조각적 정의, 순서쌍 개수)
add(id="6b57a62e", qtype="choice",
    question=("자연수 [[n]]에 대하여 [[f(n)]]이 다음과 같다.\n"
              "[[f(n)]] = { [[root(4, 9 × pow(2, n+1))]] ([[n]]이 홀수) ; [[root(4, 4 × pow(3, n))]] ([[n]]이 짝수) }\n"
              "10 이하의 두 자연수 [[p]], [[q]]에 대하여 [[f(p) × f(q)]]가 자연수가 되도록 하는 모든 순서쌍 [[point(p, q)]]의 개수는?"),
    choices=["[[36]]", "[[38]]", "[[40]]", "[[42]]", "[[44]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(홀수/짝수 경우 나눔) → 텍스트 혼합 전사",
    note="출처 [2019년 6월 고2 이과 21번/4점]. 홀홀 13 + 짝짝 13 + 홀짝 9 + 짝홀 9 = 44(전수 확인) → ⑤. 빠른정답 없음.")

# p51 — 문자를 포함한 거듭제곱근의 계산
add(id="24a8a4d1", qtype="choice",
    question=("[[a > 0]], [[b > 0]]일 때, [[root(4, 2 a pow(b, 2)) × root(12, 2 pow(a, 9) pow(b, 4)) ÷ root(6, 2 pow(a, 2) pow(b, 3))]]을\n"
              "간단히 하면?"),
    choices=["[[sqrt(a b)]]", "[[root(3, pow(a, 2) b)]]", "[[root(4, 2 pow(a, 3) pow(b, 2))]]",
             "[[root(6, 2 pow(a, 4) pow(b, 2))]]", "[[root(12, 4 pow(a, 7) pow(b, 4))]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="지수(12분모): 2→2/12=1/6, a→8/12=2/3, b→4/12=1/3 → ⁶√(2a⁴b²) → ④. 빠른정답 없음.")

# p53 — 문자를 포함한 거듭제곱근의 계산 (단답)
add(id="26feb440", qtype="short",
    question="[[a > 0]], [[b > 0]]일 때, [[root(5, 1024 pow(a, 4) pow(b, 3)) × root(10, pow(a, 2) pow(b, 4))]]을 간단히 하시오.",
    choices=None, derived_answer="4 a b", figure=None, difficulty_est=1, confidence=0.9,
    note="1024^(1/5)·a^(4/5+1/5)·b^(3/5+2/5) = 4ab. 빠른정답 4(계수만 기재)와 표기 불일치.")

# p57 — 문자를 포함한 거듭제곱근의 계산
add(id="569a6499", qtype="choice",
    question=("[[a > 0]], [[b > 0]]일 때, [[root(2, 2 a b) × root(12, pow(a, 6) pow(b, 2)) ÷ root(6, 8 a pow(b, 3))]]을 간단히\n하면?"),
    choices=["[[sqrt(pow(a, 5) b)]]", "[[root(3, pow(a, 5) b)]]", "[[root(6, pow(a, 5) b)]]",
             "[[root(6, pow(a, 10) b)]]", "[[root(12, pow(a, 10) b)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="2: 1/2−1/2 = 0, a: 1/2+1/2−1/6 = 5/6, b: 1/2+1/6−1/2 = 1/6 → ⁶√(a⁵b) → ③. 빠른정답 없음. 원문의 ²√는 root(2, …)로.")

# p58 — 문자를 포함한 거듭제곱근의 계산
add(id="7de9a409", qtype="choice",
    question=("[[a > 0]], [[b > 0]]일 때, [[root(4, 4 pow(a, 2) b) × root(12, pow(a, 3) pow(b, 4)) ÷ root(6, 8 a pow(b, 3))]]을\n"
              "간단히 하면?"),
    choices=["[[sqrt(a pow(b, 3))]]", "[[root(3, a pow(b, 2))]]", "[[root(4, pow(a, 3) b)]]",
             "[[root(6, pow(a, 4) b)]]", "[[root(12, pow(a, 7) b)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="2: 1/2−1/2 = 0, a: 1/2+1/4−1/6 = 7/12, b: 1/4+1/3−1/2 = 1/12 → ¹²√(a⁷b) → ⑤. 빠른정답 없음.")

# p59 — 문자를 포함한 거듭제곱근의 계산
add(id="8da6c914", qtype="choice",
    question=("[[a > 0]], [[b > 0]]일 때, [[sqrt(pow(a, 4) b) × root(6, pow(a, 4) b) ÷ root(3, pow(a, 5) pow(b, 2))]]을\n"
              "간단히 하면?"),
    choices=["[[a b]]", "[[b sqrt(a)]]", "[[b]]", "[[a]]", "[[pow(a, 2) b]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a: 2+2/3−5/3 = 1, b: 1/2+1/6−2/3 = 0 → a → ④. 빠른정답 없음.")

# ───────────────────────── 로그의 뜻과 성질 ─────────────────────────
# p3 — 로그의 정의 (집합 A_k)
add(id="4c4f6472", qtype="short",
    question=("자연수 [[k]]에 대하여 집합 [[sub(A,k)]]를\n"
              "[[sub(A,k)]] = { [[frac(b, a)]] | [[log(a, b) = frac(k, 2)]], [[a]]와 [[b]]는 2 이상 100 이하의 자연수 }\n"
              "라 할 때, [[card(sub(A,3)) + card(sub(A,4))]]의 값을 구하시오."),
    choices=None, derived_answer="12", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2018년 6월 고2 이과 29번/4점]. k=3: a=m², b=m³(m=2,3,4) → 3개; k=4: b=a²(a=2~10) → 9개 → 12 = 빠른정답 ✓.")
