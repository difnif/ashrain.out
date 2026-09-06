# -*- coding: utf-8 -*-
# batch14 (23항목, 모두 "같은 이미지에 별개 문항 2개인데 id 1개") — r2 재작업 (2026-09-05)
# 규칙: id는 quick_answer와 답이 맞는 쪽 문항에 귀속(맞는 쪽 없음·둘 다 → 위 문항). 귀속 문항 → ITEMS(tags=["두문항_id1개"]),
#       다른 쪽 문항 → EXTRAS(add_extra, 이미지 원문 그대로 v1.5 문법 전사). 모든 이미지를 Read로 재확인(확대 /tmp/rw14_*.png).
# 귀속 판정(23): 위 문항 20건(그중 초안 교체 5건: d22d1b34·c438667b·bb8d92fd·0e8f1729·8f0caeab) / 아래 문항 3건(c8fb9377·1c5f71e1 초안 교체, f62dc9bf 초안 유지)
#   ※ f62dc9bf 위 문항 계수는 순환소수(0.4̇, 1.4̇, 0.05̇, 0.6̇ — 확대 확인) → recdec로 전사, 답 −14(reason의 −61/5는 순환점 누락 계산)
ITEMS = []
def add(**kw): ITEMS.append(kw)
EXTRAS = []
def add_extra(**kw): EXTRAS.append(kw)

# ================= 0. 65460330 — esc_opus_h2-2_1of1 (위 문항 귀속, 초안 유지) =================
add(id='65460330', qtype='choice',
    question='최고차항의 계수가 1이고 [[lim(x, 0, frac(f(x), x)) = 1]]인 사차함수 [[f(x)]]와 실수 전체의 집합에서 연속인 함수 [[g(x)]]가 모든 실수 [[x]]에 대하여 [[(g(x) - x)(g(x) - f(x)) = 0]]을 만족시킨다. 함수 [[g(x)]]가 다음 조건을 만족시킬 때, 모든 [[frac(g(-2), g(3))]]의 값의 합은?\n(가) [[lim(x, 2, frac(g(x) - g(2), x - 2))]]의 값은 존재하지 않는다.\n(나) [[x >= a]]인 모든 실수 [[x]]에 대하여 [[g(-x) = -g(x)]]를 만족시키는 실수 [[a]]의 최솟값은 4이다.',
    choices=['[[-frac(41,3)]]', '[[-13]]', '[[-frac(37,3)]]', '[[-frac(35,3)]]', '[[-11]]'],
    derived_answer='⑤', figure=None, difficulty_est=5, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 3은 위 문항 답 ⑤(−11)·아래 문항 답 66 어느 쪽과도 불일치 → 위 문항. 출처 [2025년 5월 고3 15번/4점]. 답 ⑤ 재검산: f(x)−x=x²(x−2)(x∓4) 두 경우 g(−2)/g(3)=1/3, −34/3 → 합 −11(원문 중괄호는 소괄호로)')
add_extra(parent_id='65460330', position='하단', qtype='short',
    question='일차함수 [[f(x)]]에 대하여 함수 [[g(x)]]를\n[[g(x) = dinteg(0, x, (x - 4) f(s), s)]]라 하자. 실수 [[t]]에 대하여 직선 [[y = t x]]와 곡선 [[y = g(x)]]가 만나는 점의 개수를 [[h(t)]]라 할 때, 다음 조건을 만족시키는 모든 함수 [[g(x)]]에 대하여 [[g(6)]]의 값의 합을 구하시오.\n[[g(k) = 0]]을 만족시키는 모든 실수 [[k]]에 대하여 함수 [[h(t)]]는 [[t = -k]]에서 불연속이다.',
    choices=None, answer='66', figure=None, difficulty_est=5, confidence=0.8,
    note='출처 [2021년 사관학교 22번 변형]. 답은 직접 풀이: f(s)=as+b → g(x)=(a/2)x(x−4)(x−c), h(t)=1+#{x≠0: g(x)/x=t}의 불연속점은 포물선 g(x)/x의 꼭짓값과 x=0에서의 값 두 곳뿐 → {0, −4}가 돼야 하므로 c∈{0, 4}: f(s)=2s(g(6)=72), f(s)=−s/2+1(g(6)=−6) → 합 66(수치 확인)')

# ================= 1. c8fb9377 — esc_opus_h3-2_1of1 (아래 문항 귀속 → 초안 교체) =================
add(id='c8fb9377', qtype='choice',
    question='다음 그림과 같이 길이가 2인 선분 AB를 지름으로 하는 반원 모양의 색종이가 있다. 호 AB 위의 점 P에 대하여 두 점 A, P를 연결하는 선을 접는 선으로 하여 색종이를 접는다. [[angle(PAB) = theta]]일 때, 접은 도형에서 호 AP, 호 PB, 선분 AB로 둘러싸인 부분의 넓이를 [[S(theta)]]라 하자.\n[[app(prime(S), alpha) = 2]]일 때, [[cos(2 alpha)]]의 값은? (단, [[0 < theta < frac(pi,4)]])',
    choices=['[[frac(1,8)]]', '[[frac(1,4)]]', '[[frac(3,8)]]', '[[frac(1,2)]]', '[[frac(5,8)]]'],
    derived_answer='④',
    figure=[{'fn': 'unsupported', 'args': {'raw': '왼쪽: 지름 AB(A 좌, B 우)인 반원, 호 위의 점 P(우상), 점선 AP, A에서 ∠PAB=θ 표시. 가운데 화살표 →. 오른쪽: 선 AP로 접은 뒤의 모습 — 원래 호 AP는 점선, 접힌 호 AP는 A에서 AB 아래로 내려갔다가 AB와 만나 P까지 이어짐, 접힌 호 AP·호 PB·선분 AB로 둘러싸인 B 부근의 부분에 색칠(S(θ))'}}],
    difficulty_est=4, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 4와 아래 문항 답 ④ 일치(위 문항 답 25) → 아래 문항으로 초안 교체. 출처 [2017년 10월 고3 이과 21번 변형]. 답 ④ 풀이: 접힌 호가 AB와 만나는 점 (2cos2θ−1, 0), S(θ)=sin2θ−½sin4θ, S′(α)=2cos2α−2cos4α=2 → cos2α(1−2cos2α)=0, 0<2α<π/2 → cos2α=1/2')
add_extra(parent_id='c8fb9377', position='상단', qtype='short',
    question='다음 그림과 같이 [[y = -frac(1,2) x]] 위의 제2사분면에 있는 점 P에서 곡선 [[y = frac(1, x)]]에 그은 두 접선의 접점을 각각 A, B라 할 때, [[pow(seg(PA), 2) + pow(seg(PB), 2)]]의 최솟값은 [[p + q sqrt(2)]] 이다. [[p + q]]의 값을 구하시오. (단, [[p]], [[q]]는 자연수이다.)',
    choices=None, answer='25',
    figure=[{'fn': 'unsupported', 'args': {'raw': '좌표평면: 곡선 y=1/x(두 가지), 직선 y=−x/2, 제2사분면 위의 점 P에서 곡선에 그은 두 접선과 접점 A(제1사분면), B(제3사분면)'}}],
    difficulty_est=4, confidence=0.85,
    note='출처 [2017년 3월 고3 이과 30번 변형]. 직전 초안(위 문항) 그대로. 답 25: P=(−2s, s), 접점 a는 sa²−2a−2s=0의 두 근, PA²+PB² 최솟값 15+10√2(수치 확인) → 25')

# ================= 2. 14bca041 — esc_sonnet_h2-1_1of4 (위 문항 귀속, 초안 유지) =================
add(id='14bca041', qtype='choice',
    question='[[0 < theta < frac(pi, 2)]]일 때, [[x]]에 대한 방정식\n[[(2x + sin(theta))(x + 3 sin(theta)) = k x sin(theta) + pow(cos(theta), 2)]]의 서로 다른 두 근을 [[alpha]], [[beta]]라 하자. [[pow(alpha, 2) + pow(beta, 2) = 1]]이 되도록 하는 모든 실수 [[k]]의 값의 합은?',
    choices=['[[8]]', '[[10]]', '[[12]]', '[[14]]', '[[16]]'],
    derived_answer='④', figure=None, difficulty_est=3, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 3은 위 문항 답 ④·아래 문항 답 ④ 어느 쪽과도 불일치 → 위 문항. 답 ④ 유지(sin²θ{(k−7)²/4−4}=0 → k=3, 11 → 14)')
add_extra(parent_id='14bca041', position='하단', qtype='choice',
    question='다음 중 [[x]]에 대한\n이차방정식 [[pow(x,2) - 2x + 2 pow(sin(theta), 2) - 2 pow(cos(theta), 2) = 0]]이\n서로 다른 부호의 실근을 갖도록 하는 [[theta]]의 값으로 옳지 않은 것은? (단, [[0 <= theta <= 2 pi]])',
    choices=['[[0]]', '[[frac(pi, 6)]]', '[[frac(7,8) pi]]', '[[frac(11,8) pi]]', '[[2 pi]]'],
    answer='④', figure=None, difficulty_est=2, confidence=0.85,
    note='답은 직접 풀이: 두 근의 곱 2sin²θ−2cos²θ<0 ⇔ |tanθ|<1 ⇔ θ∈[0, π/4)∪(3π/4, 5π/4)∪(7π/4, 2π]; 11π/8(247.5°)만 불만족 → ④')

# ================= 3. d22d1b34 — esc_sonnet_h2-1_1of4 (위 문항 귀속 → 초안 교체) =================
add(id='d22d1b34', qtype='short',
    question='세균 A는 1시간마다 그 수가 4배가 되고, 세균 B는 1시간마다 그 수가 2배가 된다고 한다. 두 세균배양기에 각각 세균 A를 1마리, 세균 B를 4마리 넣었을 때, 두 세균배양기의 세균의 수의 합이 96 이상이 되게 하려면 최소 몇 시간이 지나야 하는지 구하시오.',
    choices=None, derived_answer='3시간', figure=None, difficulty_est=2, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 3이 위 문항 답 3시간·아래 문항 답 ③ 둘 다와 일치 → 규칙대로 위 문항(초안은 아래 문항이었음 → 교체). 답: n시간 후 4ⁿ+4·2ⁿ ≥ 96 → n=2는 32, n=3은 64+32=96 → 3시간(수식 없는 문장형)')
add_extra(parent_id='d22d1b34', position='하단', qtype='choice',
    question='어느 연구소에서는 매년 두 부서 A, B에 대한 실험 지원비를 전년도에 비해 각각 [[pct(20)]], [[pct(28)]]씩 늘려간다고 한다. 현재 두 부서 A, B의 실험 지원비가 각각 2000만 원, 1000만 원일 때, 부서 B의 실험 지원비가 부서 A의 실험 지원비를 처음으로 초과하는 해는 지금으로부터 몇 년 후인가?\n(단, [[log(2) = 0.3]], [[log(3) = 0.48]]로 계산한다.)',
    choices=['12년', '14년', '16년', '18년', '20년'],
    answer='③', figure=None, difficulty_est=2, confidence=0.85,
    note='직전 초안(아래 문항) 그대로. 답 ③: 2·1.2ⁿ<1.28ⁿ → n·log(16/15)=n·0.02>log2=0.3 → n>15 → 16년')

# ================= 4. 586d76ad — esc_sonnet_h2-1_3of4 (위 문항 귀속, 초안 유지) =================
add(id='586d76ad', qtype='short',
    question='다음 그림과 같은 평행사변형 ABCD에서 [[seg(AB) = 4]], [[seg(AD) = 9]]이고 두 대각선 AC와 BD가 이루는 각의 크기가 [[deg(135)]]일 때, 평행사변형 ABCD의 넓이를 구하시오.',
    choices=None, derived_answer='frac(65,2)',
    figure=[{'fn': 'unsupported', 'args': {'raw': '평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB = 4, AD = 9(점선 치수), 두 대각선의 교각 135°, 내부 음영'}}],
    difficulty_est=2, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 65/2와 위 문항 답 일치(아래 문항 답 ④) → 위 문항. 답 65/2 유지(반대각선 m, n: 81−16=2√2·mn → 넓이 √2·mn=65/2)')
add_extra(parent_id='586d76ad', position='하단', qtype='choice',
    question='그림과 같이 [[seg(AB) = 1]], [[seg(BC) = 2]], [[B = frac(pi, 3)]]인\n평행사변형 ABCD의 두 대각선이 이루는 각의 크기를 [[theta]]라 할 때, [[pow(sin(theta), 2)]]의 값은? (단, [[0 < theta < frac(pi, 2)]])',
    choices=['[[frac(1,7)]]', '[[frac(2,7)]]', '[[frac(3,7)]]', '[[frac(4,7)]]', '[[frac(5,7)]]'],
    answer='④',
    figure=[{'fn': 'unsupported', 'args': {'raw': '평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB=1, BC=2(점선 치수), B에 π/3 표시, 두 대각선 AC·BD의 교점에 θ 표시'}}],
    difficulty_est=3, confidence=0.85,
    note='답은 직접 풀이: AC²=1+4−2·2·½=3, BD²=1+4+2=7, 넓이 1·2·sin(π/3)=√3=½·√3·√7·sinθ → sinθ=2/√7 → sin²θ=4/7')

# ================= 5. 27c8d446 — esc_sonnet_h3-2_2of4 (위 문항 귀속, 초안 유지) =================
add(id='27c8d446', qtype='short',
    question='좌표평면 위를 움직이는 점 P의 시각 [[t]]에서의\n위치 [[point(x, y)]]가\n[[x = cos(t)]], [[y = 2 pow(sin(t), 2)]] ([[0 <= t <= frac(pi,2)]])이다. 점 P의\n위치가 [[point(0, 2)]]일 때, 가속도의 크기를 구하시오.',
    choices=None, derived_answer='4', figure=None, difficulty_est=2, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 4와 위 문항 답 4 일치(아래 문항 답 ①) → 위 문항. 답 4 유지(t=π/2, x″=−cos t=0, y=1−cos2t → y″=4cos2t=−4)')
add_extra(parent_id='27c8d446', position='하단', qtype='choice',
    question='좌표평면 위를 움직이는 점 [[P(x, y)]]의 시각 [[t]]에서의\n위치가 [[x = 2 pow(t,2) - 3t]], [[y = k pow(t,3) + t]]이다. [[t = 1]]에서의\n점 P의 가속도의 크기가 [[sqrt(52)]]일 때, 양수 [[k]]의 값은?',
    choices=['[[1]]', '[[2]]', '[[3]]', '[[4]]', '[[5]]'],
    answer='①', figure=None, difficulty_est=2, confidence=0.85,
    note='답은 직접 풀이: 가속도 (4, 6kt) → t=1에서 16+36k²=52 → k²=1, k>0 → k=1 → ①')

# ================= 6. c438667b — esc_sonnet_h3-2_3of4 (위 문항 귀속 → 초안 교체) =================
add(id='c438667b', qtype='choice',
    question='그림과 같이 [[seg(BC) = 2]], [[angle(ABC) = frac(pi,3)]],\n[[angle(ACB) = 2 theta]] ([[0 < theta < frac(pi,3)]])인 삼각형 ABC에 내접하는 원의 반지름의 길이를 [[r(theta)]]라 하자.\n[[h(theta) = frac(r(theta), tan(theta))]]일 때, [[app(prime(h), frac(pi,6))]]의 값은?',
    choices=['[[-frac(1,2)]]', '[[-frac(sqrt(3),3)]]', '[[-frac(sqrt(3),2)]]', '[[-frac(2,3) sqrt(3)]]', '[[-sqrt(3)]]'],
    derived_answer='④',
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)와 그 내접원. 원의 중심(점)에서 변 BC에 내린 반지름 r(θ)(세로 실선, 중심 옆 점선 호 표시), B에 π/3, C에 2θ 각 표시, BC=2(아래 점선 치수)'}}],
    difficulty_est=3, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 240은 위 문항 답 ④·아래 문항 답 ④ 어느 쪽과도 불일치 → 규칙대로 위 문항(초안은 아래 문항이었음 → 교체). 답 ④ 풀이: BC=r(cot(π/6)+cotθ) → r=2tanθ/(√3tanθ+1), h=2/(√3tanθ+1), h′=−2√3sec²θ/(√3tanθ+1)² → θ=π/6에서 −2√3·(4/3)/4=−(2/3)√3')
add_extra(parent_id='c438667b', position='하단', qtype='choice',
    question='실수 전체의 집합에서 미분가능한 함수 [[f(x)]]에 대하여 함수 [[g(x)]]를 [[g(x) = frac(f(x) cos(2x), pow(e,x))]]라 하자.\n[[app(prime(g), pi) = pow(e,pi) g(pi)]]일 때, [[frac(app(prime(f), pi), f(pi))]]의 값은? (단, [[f(pi) != 0]])',
    choices=['[[pow(e, -2 pi)]]', '[[1]]', '[[pow(e, -pi) + 1]]', '[[pow(e,pi) + 1]]', '[[pow(e, 2 pi)]]'],
    answer='④', figure=None, difficulty_est=3, confidence=0.85,
    note='직전 초안(아래 문항) 그대로(g′·f′는 app(prime(·), pi)). 답 ④: g′(π)=(f′(π)−f(π))/e^π=e^π·g(π)=f(π) → f′(π)/f(π)=e^π+1')

# ================= 7. d2c737b5 — esc_sonnet_h3-3_2of6 (위 문항 귀속, 초안 유지) =================
add(id='d2c737b5', qtype='short',
    question='세 점 [[A(1, 0, 2)]], [[B(2, 4, -1)]], [[C(3, 2, -1)]]에 대하여 [[abs(vec(PA) + vec(PB) + vec(PC)) = 9]]를 만족시키는 점 P가 나타내는 도형은 중심의 좌표가 [[point3(a, b, c)]]이고 반지름의 길이가 [[r]]인 구이다. 이때 [[a + b + c + r]]의 값을 구하시오.',
    choices=None, derived_answer='7', figure=None, difficulty_est=2, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 5는 위 문항 답 7·아래 문항 답 ①(3) 어느 쪽과도 불일치 → 위 문항. 답 7 유지(|3G−3P|=9, G=(2,2,0), r=3)')
add_extra(parent_id='d2c737b5', position='하단', qtype='choice',
    question='두 점 [[A(-1, 0)]], [[B(2, 0)]]에 대하여\n점 P가 [[pow(abs(vec(PA)), 2) = 4 pow(abs(vec(PB)), 2)]]을 만족할 때,\n삼각형 PAB의 넓이의 최댓값은?',
    choices=['[[3]]', '[[4]]', '[[5]]', '[[6]]', '[[7]]'],
    answer='①', figure=None, difficulty_est=2, confidence=0.85,
    note='답은 직접 풀이: (x+1)²+y²=4{(x−2)²+y²} → (x−3)²+y²=4, 높이 최대 2 → 넓이 최대 ½·3·2=3 → ①')

# ================= 8. 5cd2052d — esc_sonnet_h3-3_3of6 (위 문항 귀속, 초안 유지) =================
add(id='5cd2052d', qtype='short',
    question='점 [[A(3, -2, -4)]]와 벡터 [[vec(n) = vcomp(2, -1, -2)]]에\n대하여 점 P가 [[dot(vec(AP), vec(n)) = 0]]을 만족시킬 때, 선분 OP의\n길이의 최솟값을 구하시오. (단, O는 원점이다.)',
    choices=None, derived_answer='frac(16,3)', figure=None, difficulty_est=2, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 16/3과 위 문항 답 일치(아래 문항 답 ⑤) → 위 문항. 답 16/3 유지(평면 2x−y−2z−16=0과 원점의 거리)')
add_extra(parent_id='5cd2052d', position='하단', qtype='choice',
    question='좌표공간의 세 점 A, B, P의 위치벡터를 각각 [[vec(a)]], [[vec(b)]], [[vec(x)]]라 할 때, 옳은 것만을 보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. [[vec(x) = vec(b) + t (vec(a) - vec(b))]] (단, [[t]]는 실수)를 만족시키는 점 P의 자취는 두 점 A, B를 지나는 직선이다.\nㄴ. [[abs(vec(x) - vec(a)) = 4]]를 만족시키는 점 P의 자취는 점 A를 중심으로 하는 구이다.\nㄷ. [[dot((vec(x) - vec(a)), (vec(b) - vec(a))) = 0]]을 만족시키는 점 P의 자취는 점 A를 지나고 직선 AB에 수직인 평면이다.',
    choices=['ㄱ', 'ㄴ', 'ㄱ, ㄴ', 'ㄴ, ㄷ', 'ㄱ, ㄴ, ㄷ'],
    answer='⑤', figure=None, difficulty_est=2, confidence=0.85,
    note='답은 직접 풀이: ㄱ 직선 AB의 벡터방정식(참), ㄴ 중심 A·반지름 4인 구(참), ㄷ A를 지나고 AB에 수직인 평면(참) → ⑤')

# ================= 9. e1c7b39f — esc_sonnet_h3-3_6of6 (위 문항 귀속, 초안 유지) =================
add(id='e1c7b39f', qtype='choice',
    question='평면 위의 두 점 [[sub(O,1)]], [[sub(O,2)]] 사이의 거리가 2일 때 [[sub(O,1)]], [[sub(O,2)]]를 각각 중심으로 하고 반지름의 길이가 2인 두 원의 교점을 A, B라 하자. 호 A[[sub(O,2)]]B 위의 점 P와 호 A[[sub(O,1)]]B 위의 점 Q에 대하여 두 벡터 [[vec(O1P)]], [[vec(O2Q)]]의 내적 [[dot(vec(O1P), vec(O2Q))]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, [[M + m]]의 값은?',
    choices=['[[-4]]', '[[-2]]', '[[0]]', '[[2]]', '[[4]]'],
    derived_answer='②',
    figure=[{'fn': 'unsupported', 'args': {'raw': '중심 O₁(좌), O₂(우)인 반지름 2의 두 원이 위아래 교점 A(위), B(아래)에서 만남; O₁에서 원 O₁의 오른쪽 호 위의 점 P로, O₂에서 원 O₂의 왼쪽 호 위의 점 Q로 향하는 화살표'}}],
    difficulty_est=4, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 7은 위 문항 답 ②·아래 문항 답 31 어느 쪽과도 불일치 → 위 문항. 답 ② 유지(4cos(α−β), α∈[−60°,60°], β∈[120°,240°] → M=2, m=−4)')
add_extra(parent_id='e1c7b39f', position='하단', qtype='short',
    question='한 변의 길이가 6인 정삼각형 ABC의 꼭짓점 A에서 변 BC에 내린 수선의 발을 H라 하자. 점 P가 선분 AH 위를 움직일 때, [[abs(dot(vec(PA), vec(PB)))]]의 최댓값은 [[frac(q, p)]]이다.\n[[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)',
    choices=None, answer='31', figure=None, difficulty_est=3, confidence=0.85,
    note='답은 직접 풀이: H 원점, P=(0, t)(0≤t≤3√3) → PA·PB=t²−3√3t ∈ [−27/4, 0] → |·| 최댓값 27/4 → p+q=31')

# ================= 10. bb8d92fd — esc_sonnet_m1-2_1of4 (위 문항 귀속 → 초안 교체) =================
add(id='bb8d92fd', qtype='choice',
    question='좌표평면 위의 네 점 A[[point(3, 5)]], B[[point(3, 1)]], C[[point(5, 1)]], D[[point(5, 5)]]에 대하여 사각형 ABCD를 [[x]]축을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 [[sub(V,x)]], [[y]]축을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 [[sub(V,y)]]라 하자. 이때 [[ratio(sub(V,x), sub(V,y))]]는?',
    choices=['[[ratio(2, 1)]]', '[[ratio(2, 3)]]', '[[ratio(3, 2)]]', '[[ratio(3, 4)]]', '[[ratio(4, 3)]]'],
    derived_answer='④', figure=None, difficulty_est=3, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 4와 위 문항 답 ④(3:4) 일치(아래 문항 답 ③) → 위 문항(초안은 아래 문항이었음 → 교체). 답 ④ 풀이: V_x=π(5²−1²)·2=48π, V_y=π(5²−3²)·4=64π → 3:4')
add_extra(parent_id='bb8d92fd', position='하단', qtype='choice',
    question='좌표평면 위의 네 점 A[[point(2, 4)]], B[[point(2, 2)]], C[[point(6, 2)]], D[[point(6, 4)]]에 대하여 사각형 ABCD를 [[x]]축을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 [[sub(V,x)]], [[y]]축을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 [[sub(V,y)]]라 하자. 이때 [[ratio(sub(V,x), sub(V,y))]]는?',
    choices=['[[ratio(2, 3)]]', '[[ratio(3, 2)]]', '[[ratio(3, 4)]]', '[[ratio(4, 3)]]', '[[ratio(4, 5)]]'],
    answer='③', figure=None, difficulty_est=3, confidence=0.85,
    note='직전 초안(아래 문항) 그대로. 답 ③: V_x=π(4²−2²)·4=48π, V_y=π(6²−2²)·2=64π → 3:4')

# ================= 11. 068b87c7 — esc_sonnet_m2-1_1of4 (위 문항 귀속, 초안 유지) =================
add(id='068b87c7', qtype='choice',
    question='함수 [[f(x)]] = ([[x]] 이하의 소수의 개수)일 때, [[f(20)]]의 값은?',
    choices=['[[7]]', '[[8]]', '[[9]]', '[[10]]', '[[11]]'],
    derived_answer='②', figure=None, difficulty_est=1, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 16은 위 문항 답 ②·아래 문항 답 ④ 어느 쪽과도 불일치 → 위 문항. 답 ② 유지(20 이하 소수 8개)')
add_extra(parent_id='068b87c7', position='하단', qtype='choice',
    question='함수 [[f(x)]] = ([[x]] 이하의 소수의 개수)일 때, [[f(30)]]의 값은?',
    choices=['[[7]]', '[[8]]', '[[9]]', '[[10]]', '[[11]]'],
    answer='④', figure=None, difficulty_est=1, confidence=0.85,
    note='답은 직접 풀이: 30 이하의 소수 2, 3, 5, 7, 11, 13, 17, 19, 23, 29 → 10개 → ④')

# ================= 12. f62dc9bf — esc_sonnet_m2-1_2of4 (아래 문항 귀속, 초안 유지) =================
add(id='f62dc9bf', qtype='choice',
    question='[[A = (-4 pow(x,2) pow(y,2) + frac(3,2) x pow(y,3)) ÷ (frac(3,2) x pow(y,2))]],\n[[B = frac(5,4)(2x - frac(8,5) y)]]일 때,\n[[B - (2A - 3B - (5A - 2B))]]를 [[x]], [[y]]에 대한 식으로 바르게 나타낸 것은?',
    choices=['[[-18x + frac(27,4) y]]', '[[-13x + frac(11,4) y]]', '[[-8x + 3y]]', '[[-7x - 9y]]', '[[-3x - y]]'],
    derived_answer='⑤', figure=None, difficulty_est=2, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 5와 아래 문항 답 ⑤ 일치(위 문항 답 −14) → 아래 문항(초안 그대로). 답 ⑤ 유지(A=−8x/3+y, B=5x/2−2y → 3A+2B=−3x−y; 원문 중괄호는 소괄호로, 나눗셈의 제수는 괄호로 묶음)')
add_extra(parent_id='f62dc9bf', position='상단', qtype='short',
    question='두 다항식 [[A = recdec(0, 4) x + recdec(1, 4) y]], [[B = recdec(0, 0, 5) x + recdec(0, 6) y]]에 대하여 [[op(btri, A, B) = 3A - 5B]], [[op(bdtri, A, B) = A + 3B]]라 하자.\n[[op(btri, op(btri, A, B), op(bdtri, A, B)) = m x + n y]]일 때, 상수 [[m]], [[n]]에 대하여 [[2m + n]]의 값을 구하시오.',
    choices=None, answer='-14', figure=None, difficulty_est=3, confidence=0.8,
    note='계수는 순환소수 0.4̇, 1.4̇, 0.05̇, 0.6̇(이미지 확대로 순환점 확인; recdec(0,0,5)=0.05̇=1/18). 사용자 정의 연산 ▲=op(btri), ▼=op(bdtri). 답은 직접 풀이: A=(4/9)x+(13/9)y, B=(1/18)x+(2/3)y → A▲B=(19/18)x+y, A▼B=(11/18)x+(31/9)y → (A▲B)▲(A▼B)=(1/9)x−(128/9)y → 2m+n=−14(reason의 −61/5는 순환점을 뺀 계산)')

# ================= 13. 29079440 — esc_sonnet_m2-2_1of5 (위 문항 귀속, 초안 유지) =================
add(id='29079440', qtype='short',
    question='다음 그림의 [[tri(ABC)]]에서 [[angle(A)]]의 외각의 이등분선과 [[angle(C)]]의 외각의 이등분선의 교점을 P라 하고 점 P에서 [[seg(AB)]]와 [[seg(BC)]]의 연장선에 내린 수선의 발을 각각 D, E라 하자. [[seg(AC) = 11]] cm, [[seg(DP) = 8]] cm일 때, [[tri(PDA)]]와 [[tri(PEC)]]의 넓이의 합을 구하시오.',
    choices=None, derived_answer='44 cm²',
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위 왼쪽, B 왼쪽 아래, C 오른쪽 아래), BA의 연장선 위의 D(A 위)와 BC의 연장선 위의 E(C 오른쪽), A·C의 외각 이등분선(같은 각 표시)의 교점 P(오른쪽), D·E에 직각 표시, △PDA·△PEC 음영, DP=8 cm·AC=11 cm 치수(점선 호)'}}],
    difficulty_est=3, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 없음 → 위 문항. 답 44 cm² 유지(P는 방심: PD=PE=PF, △PDA≡△PFA, △PEC≡△PFC → 합=△PAC=½·11·8)')
add_extra(parent_id='29079440', position='하단', qtype='short',
    question='다음 그림에서 [[x]]의 값을 구하시오.',
    choices=None, answer='16',
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 O에서 나가는 두 반직선(위쪽 사선 OA 방향, 오른쪽 수평 OB 방향)과 그 사이의 점 P, 선분 OP. PA⊥OA(A에 직각 표시), PB⊥OB(B에 직각 표시), PA=10 cm, PB=10 cm, OB=16 cm, OA=x cm(모두 점선 호 치수)'}}],
    difficulty_est=2, confidence=0.8,
    note='정보가 그림에만 있음(raw에 전부 기재). 답은 직접 풀이: 직각삼각형 OAP·OBP에서 OP 공통, PA=PB → RHS 합동 → OA=OB=16')

# ================= 14. 0e8f1729 — esc_sonnet_m3-1_1of6 (위 문항 귀속 → 초안 교체) =================
add(id='0e8f1729', qtype='choice',
    question='다음 중 [[pow(x,2) - pow(y,2) - 8x + 2y + 15]]의 인수를 모두 고르면?\n(정답 2개)',
    choices=['[[x - y - 5]]', '[[x - y - 3]]', '[[x + y - 5]]', '[[x + y - 3]]', '[[x + y + 3]]'],
    derived_answer='②, ③', figure=None, difficulty_est=2, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 3은 위 문항 답 "②, ③"(정답 2개)·아래 문항 답 ④ 어느 쪽과도 정확히 일치하지 않음 → 규칙대로 위 문항(초안은 아래 문항이었음 → 교체). 답 풀이: (x−4)²−(y−1)²=(x−y−3)(x+y−5) → ②, ③')
add_extra(parent_id='0e8f1729', position='하단', qtype='choice',
    question='[[pow(x,2) + 5 x y + 2x - 5y - 3]]을 인수분해하면?',
    choices=['[[(x + 1)(x + 5y + 3)]]', '[[(x - 1)(x - 5y + 3)]]', '[[(x - 1)(x + 5y - 3)]]', '[[(x - 1)(x + 5y + 3)]]', '[[(x + 1)(x - 5y - 3)]]'],
    answer='④', figure=None, difficulty_est=2, confidence=0.85,
    note='직전 초안(아래 문항) 그대로. 답 ④: x²+(5y+2)x−(5y+3)=(x−1)(x+5y+3)')

# ================= 15. f729ac0e — esc_sonnet_m3-1_2of6 (위 문항 귀속, 초안 유지) =================
add(id='f729ac0e', qtype='choice',
    question='다음 그림과 같이 세 원의 중심이 한 직선 위에 있을 때, 색칠한 부분의 넓이는?',
    choices=['[[9 pi x y]]', '[[12 pi x y]]', '[[6 pi x y + pow(y,2)]]', '[[9 pi x y + 6 pow(y,2)]]', '[[12 pi x y + 9 pow(y,2)]]'],
    derived_answer='②',
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 안에 반지름 2x인 원(왼쪽)과 반지름 3y인 원(오른쪽)이 내접하며 서로 외접, 세 중심이 수평 지름 위(점 표시). 두 작은 원 바깥의 큰 원 내부 색칠'}}],
    difficulty_est=2, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 2와 위 문항 답 ② 일치(아래 문항 답 18) → 위 문항. 답 ② 유지(π(2x+3y)²−4πx²−9πy²=12πxy). 도형 unsupported 유지')
add_extra(parent_id='f729ac0e', position='하단', qtype='short',
    question='선분 AB를 지름으로 하는 반원이 있다. 다음 그림과 같이 호 AB 위의 점 P에서 선분 AB에 내린 수선의 발을 Q라 하고 호 AQ와 호 QB로 둘러싸인 (그림: 아치 모양) 모양 도형의 넓이를 [[sub(S,1)]], 선분 PQ를 지름으로 하는 반원의 넓이를 [[sub(S,2)]]라 하자. [[seg(AQ) - seg(QB) = 2 sqrt(57)]]이고\n[[sub(S,1) - sub(S,2) = 3 pi]]일 때,\n선분 AB의 길이를 구하시오.',
    choices=None, answer='18',
    figure=[{'fn': 'unsupported', 'args': {'raw': '지름 AB(A 좌, B 우)인 반원 안에 지름 AQ인 반원(큰 것)과 지름 QB인 작은 반원(Q는 AB 위 B 근처). P는 큰 호 위(Q 바로 위, PQ⊥AB 직각 표시). 세 호 사이의 아치 모양 부분이 S₁'}}],
    difficulty_est=3, confidence=0.8,
    note='본문 중 아치 모양 삽입 그림은 "(그림: 아치 모양)"으로 표기. 답은 직접 풀이: AQ=a, QB=b → S₁=πab/4(아르벨로스), PQ²=ab → S₂=πab/8, S₁−S₂=πab/8=3π → ab=24, (a+b)²=(2√57)²+4·24=324 → AB=18')

# ================= 16. bf92a8db — esc_sonnet_m3-1_3of6 (위 문항 귀속, 초안 유지) =================
add(id='bf92a8db', qtype='short',
    question='이차방정식 [[5 pow(x,2) + x - 1 = 0]]의 두 근을 [[alpha]], [[beta]]라 하고\n[[f(n) = pow(alpha, n) + pow(beta, n)]]이라 할 때,\n[[5f(n + 2) + f(n + 1) - f(n)]]의 값을 구하시오.\n(단, [[n]]은 자연수이다.)',
    choices=None, derived_answer='0', figure=None, difficulty_est=3, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 1은 위 문항 답 0·아래 문항 답 ③ 어느 쪽과도 불일치 → 위 문항. 답 0 유지(αⁿ(5α²+α−1)+βⁿ(5β²+β−1)=0)')
add_extra(parent_id='bf92a8db', position='하단', qtype='choice',
    question='이차방정식 [[5 pow(x,2) - (4a + 3) x - 5 = 0]]의 한 근 [[x = k]]에\n대하여 [[k - frac(1, k) = a]]가 성립한다. 이때 상수 [[a]]의 값은?',
    choices=['[[1]]', '[[2]]', '[[3]]', '[[4]]', '[[5]]'],
    answer='③', figure=None, difficulty_est=2, confidence=0.85,
    note='답은 직접 풀이: 5k²−(4a+3)k−5=0의 양변을 k로 나누면 5(k−1/k)=4a+3 → 5a=4a+3 → a=3 → ③')

# ================= 17. 8f0caeab — esc_sonnet_m3-1_4of6 (위 문항 귀속 → 초안 교체) =================
add(id='8f0caeab', qtype='short',
    question='이차방정식 [[2 pow(x,2) - 13x + 15 = 0]]의 두 근 중에서 큰 근이\n[[3 pow(x,2) - 11x + a = 0]]의 근이라 할 때, [[a]]의 값을 구하시오.',
    choices=None, derived_answer='-20', figure=None, difficulty_est=2, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 1은 위 문항 답 −20·아래 문항 답 ⑤ 어느 쪽과도 불일치 → 규칙대로 위 문항(초안은 아래 문항이었음 → 교체). 답 풀이: (2x−3)(x−5)=0 → 큰 근 5 → 75−55+a=0 → a=−20')
add_extra(parent_id='8f0caeab', position='하단', qtype='choice',
    question='이차방정식 [[pow(x,2) - x - 6 = 0]]의 두 근 중 작은 근이 이차방정식 [[2 pow(x,2) + b x - 2 = 0]]의 근이라고 할 때, [[b]]의 값은?',
    choices=['[[-3]]', '[[-1]]', '[[1]]', '[[2]]', '[[3]]'],
    answer='⑤', figure=None, difficulty_est=2, confidence=0.85,
    note='직전 초안(아래 문항) 그대로. 답 ⑤: (x−3)(x+2)=0 → 작은 근 −2 → 8−2b−2=0 → b=3')

# ================= 18. e627d40a — esc_sonnet_m3-2_1of6 (위 문항 귀속, 초안 유지) =================
add(id='e627d40a', qtype='choice',
    question='다음은 두 대각선의 길이가 [[p]], [[q]]이고 두 대각선이 이루는 예각의 크기가 [[x]]인 사각형의 넓이를 구하는 과정이다. (가), (나)에 알맞은 것을 차례로 쓴 것은?\n[[quad(ABCD)]]의 각 꼭짓점을 지나고 두 대각선에 각각 평행한 직선을 그어 [[quad(EFGH)]]를 만들면\n[[quad(ABCD) = box(1) quad(EFGH) = frac(1,2) p q box(2)]]',
    choices=['[[frac(1,4)]], [[sin(x)]]', '[[frac(1,4)]], [[cos(x)]]', '[[frac(1,2)]], [[sin(x)]]', '[[frac(1,2)]], [[cos(x)]]', '[[1]], [[sin(x)]]'],
    derived_answer='③',
    figure=[{'fn': 'unsupported', 'args': {'raw': '사각형 ABCD(색칠, 보라)의 대각선 AC=q, BD=p(점선 치수), 이루는 각 x. 각 꼭짓점을 지나 대각선에 평행한 직선으로 만든 평행사변형 EFGH(E 위, F 좌, G 아래, H 우), EF=q, FG=p, ∠F=x 표시, 평행 화살표 표시. 아래 상자에 (가)(나) 풀이 과정'}}],
    difficulty_est=2, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 3과 위 문항 답 ③ 일치(아래 문항 답 ①) → 위 문항. 빈칸 (가)(나)는 box(1)·box(2). 답 ③ 유지(□ABCD=½□EFGH=½·pq·sin x)')
add_extra(parent_id='e627d40a', position='하단', qtype='choice',
    question='다음 그림과 같은 사각형 ABCD의 넓이를 구하면?',
    choices=['[[12 sqrt(3)]]', '[[11 sqrt(3)]]', '[[10 sqrt(3)]]', '[[9 sqrt(3)]]', '[[8 sqrt(3)]]'],
    answer='①',
    figure=[{'fn': 'unsupported', 'args': {'raw': '사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하, 분홍 음영)와 두 대각선 AC·BD. 대각선 AC=8, BD=6(점선 호 치수), 두 대각선이 이루는 각 60°(교점에서 A·B 쪽 각에 표시)'}}],
    difficulty_est=2, confidence=0.8,
    note='정보(대각선 길이 6·8, 끼인각 60°)가 그림에만 있음(raw에 기재). 답은 직접 풀이: ½·6·8·sin60°=12√3 → ①')

# ================= 19. 35311c9f — esc_sonnet_m3-2_3of6 (위 문항 귀속, 초안 유지) =================
add(id='35311c9f', qtype='short',
    question='다음 그림의 원 O에서 [[perp(seg(AB), seg(OD))]], [[perp(seg(BC), seg(OE))]], [[perp(seg(CA), seg(OF))]]이고 [[seg(OD) = seg(OE) = seg(OF)]]이다. [[seg(AC) = 7]] cm일 때, [[tri(ABC)]]의 둘레의 길이를 구하시오.',
    choices=None, derived_answer='21 cm',
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O에 내접하는 삼각형 ABC(A 좌상, B 좌하, C 우). O에서 AB·BC·CA에 내린 수선의 발 D·E·F(직각 표시), OD=OE=OF(같은 길이 표시). AC=7cm(점선 치수)'}}],
    difficulty_est=2, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 없음 → 위 문항. 답 21 cm 유지(중심에서 같은 거리의 현은 길이가 같으므로 정삼각형 → 3·7)')
add_extra(parent_id='35311c9f', position='하단', qtype='choice',
    question='아래 그림과 같이 원 O의 중심에서 두 현 AB, AC에 내린 수선의 발을 각각 M, N이라 하면 [[seg(OM) = seg(ON)]]이고 [[seg(AB) = 12]] cm, [[angle(BAC) = deg(60)]]이다. 다음 중 옳지 않은 것은?',
    choices=['[[seg(AC) = 12]] cm', '[[seg(AM) = 6]] cm', '[[angle(OBM) = deg(30)]]', '[[seg(OB) = 4 sqrt(2)]] cm', '[[tri(OMB) = 6 sqrt(3)]] cm²'],
    answer='④',
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O에 내접하는 삼각형 ABC(A 위, B 좌하, C 우하). O에서 AB·AC에 내린 수선의 발 M·N(직각 표시), OM=ON(같은 길이 표시), A에 60° 표시, AB=12 cm(왼쪽 점선 호 치수)'}}],
    difficulty_est=2, confidence=0.85,
    note='답은 직접 풀이: OM=ON → AB=AC=12, ∠A=60° → 정삼각형, ∠OBM=30°, AM=6, OB=6/cos30°=4√3(≠4√2), △OMB=½·6·2√3=6√3 → 옳지 않은 것 ④')

# ================= 20. 1c5f71e1 — esc_sonnet_m3-2_5of6 (아래 문항 귀속 → 초안 교체) =================
add(id='1c5f71e1', qtype='choice',
    question='다음 그림과 같이 반지름의 길이가 각각 5, 10인\n두 원 O, O′이 점 P에서 접한다. 원 O′의 두 현 PA, PB가 원 O와 만나는 점을 각각 C, D라 할 때, [[quad(ACDB)]]의 넓이는 [[tri(PDC)]]의 넓이의 몇 배인가?',
    choices=['[[2]]배', '[[frac(5,2)]]배', '[[3]]배', '[[frac(7,2)]]배', '[[4]]배'],
    derived_answer='③',
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 O′(중심 O′, 점 표시) 안에 작은 원 O(중심 O, 점 표시)가 아래쪽 점 P에서 내접. 큰 원 위의 A(좌상)·B(우상), 현 PA·PB가 작은 원과 만나는 점 C(좌)·D(우). 선분 AB, CD'}}],
    difficulty_est=3, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 3과 아래 문항 답 ③(3배) 일치(위 문항 답 2 cm) → 아래 문항으로 초안 교체. 답 ③ 풀이: P 중심 닮음(반지름비 1:2)으로 CD∥AB, △PDC:△PAB=1:4 → □ACDB=3△PDC. 단독 점 이름 O′은 텍스트')
add_extra(parent_id='1c5f71e1', position='상단', qtype='short',
    question='다음 그림과 같이 두 원이 점 A에서 접하고 있다. 작은 원 위의 점 D에서 접하는 직선이 큰 원과 만나는 점을 각각 B, C라 하면 [[seg(AB) = 6]] cm, [[seg(BC) = 5]] cm, [[seg(AC) = 4]] cm일 때, [[seg(CD)]]의 길이를 구하시오.',
    choices=None, answer='2 cm',
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 안에 작은 원이 점 A(우상)에서 내접. 큰 원 위 B(좌)·C(아래), 작은 원 위 D(BC 위, 접점). 삼각형 ABC와 선분 AD. AB=6cm, BC=5cm, AC=4cm(호 모양 점선 치수)'}}],
    difficulty_est=3, confidence=0.85,
    note='직전 초안(위 문항) 그대로. 답 2 cm: 접선과 현이 이루는 각으로 AD가 ∠BAC를 이등분 → BD:DC=6:4 → CD=2')

# ================= 21. 6805bd8a — esc_sonnet_m3-2_5of6 (위 문항 귀속, 초안 유지) =================
add(id='6805bd8a', qtype='short',
    question='다음 그림에서 점 P는 [[seg(AC)]]와 [[seg(BD)]]의 교점이다. [[angle(ABD) = deg(40)]], [[angle(BPC) = deg(70)]]이고 [[arc(BC) = 5]] cm일 때, 원의 둘레의 길이를 구하시오.',
    choices=None, derived_answer='30 cm',
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 위 A(좌상)·D(우상)·B(좌하)·C(우하). 현 AC·BD가 P에서 교차, 선분 AB. ∠ABD=40°(B), ∠BPC=70°(P), 호 BC=5cm'}}],
    difficulty_est=2, tags=['두문항_id1개'], confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 4는 위 문항 답 30 cm·아래 문항 답 ⑤ 어느 쪽과도 불일치 → 위 문항. 답 30 cm 유지(∠ACB=70°−40°=30° → 호 BC는 원주의 60/360 → 5·6)')
add_extra(parent_id='6805bd8a', position='하단', qtype='choice',
    question='그림과 같이 반지름의 길이가 9 cm인 원 O에서 호 AB와 호 CD의 길이는 각각 [[4 pi]] cm, [[6 pi]] cm이고, 선분 AB와 선분 CD의 연장선이 만나서 이루는 예각의 크기가 [[deg(30)]]일 때, 호 AC의 길이는?',
    choices=['[[4 pi]] cm', '[[frac(17,4) pi]] cm', '[[frac(9,2) pi]] cm', '[[5 pi]] cm', '[[frac(11,2) pi]] cm'],
    answer='⑤',
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O(중심 O 점 표시). 위쪽 현 AB(A 좌상, B 우상)와 현 CD(C 좌하, D 우)의 연장선이 원 오른쪽 바깥의 한 점에서 만나 30°를 이룸. 호 AB=4π cm(위), 호 CD=6π cm(아래 오른쪽) 화살표 치수'}}],
    difficulty_est=3, confidence=0.85,
    note='출처 [2009년 3월 고1 20번]. 답은 직접 풀이: 원주 18π → 호 AB 80°, 호 CD 120°; 외부 교점의 각 30°=½(호 AC−호 BD), 호 AC+호 BD=160° → 호 AC=110° → 18π·110/360=11π/2 → ⑤')

# ================= 22. 1c88b31d — esc_opus_m3-1_1of1 (위 문항 귀속, 초안의 ⟨x⟩를 nota(angle)로 교체) =================
add(id='1c88b31d', qtype='short',
    question='기호 [[nota(angle, x)]]를 [[x]]에 가장 가까운 정수라 할 때,\n[[nota(angle, frac(sqrt(5), sqrt(5) + 1)) + nota(angle, frac(sqrt(5), sqrt(5) - 1))]]의 값을 구하시오.\n(단, [[sqrt(5)]]의 값은 2.236으로 계산한다.)',
    choices=None, derived_answer='3', figure=None, difficulty_est=2, tags=['두문항_id1개'],
    confidence=0.85, needs_review=None,
    note='id 귀속 근거: 빠른정답 9는 위 문항 답 3·아래 문항 답 5 어느 쪽과도 불일치 → 위 문항. 약속 기호 ⟨x⟩를 nota(angle, x)로 교체(정의문의 작은 "< x >"도 같은 기호). 답 3 유지(0.691→1, 1.809→2)')
add_extra(parent_id='1c88b31d', position='하단', qtype='short',
    question='[[frac(sqrt(10) + sqrt(6), sqrt(10) - sqrt(6)) = a + b sqrt(15)]]일 때, 유리수 [[a]], [[b]]에 대하여\n[[a + b]]의 값을 구하시오.',
    choices=None, answer='5', figure=None, difficulty_est=2, confidence=0.85,
    note='답은 직접 풀이: 분모 유리화 (√10+√6)²/4=(16+4√15)/4=4+√15 → a=4, b=1 → 5')
