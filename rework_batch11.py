# -*- coding: utf-8 -*-
# batch11 (36문항) — v1.5 r2 문법 재작업 (사용자 정의 연산·약속 기호 / 프라임 상수 잔여 회수)
# 핵심 교체: 이항연산 ◎★△⊗◇◉▼◆∘○□ → op(dcirc|star|tri|otimes|diamond|fisheye|bdtri|bdiamond|ring|circ|sq, a, b) — 정의식·계산식 전부 [[ ]] 안(원문 중괄호는 소괄호)
#            약속 괄호 ⟨x⟩·<x>·{x}·⟨a, b⟩·[a, b]·<a, b> → nota(angle|lt|brace|sq, …) / P[x] → idx(P, x) / 전치 Bᵗ → tr(B) / 프라임 상수 a′, b′, c′ → a' x + b' y = c'
#            정의가 한글 문장인 ★(c0d134e4, c7632096)은 정의 문장을 텍스트로 두고 계산식만 op(star)
# 텍스트혼합 통과(tags=["텍스트혼합"]): 조건이 한글 문장인 경우 나눔 3건(ad241856, d25f4656, 3babd113) — 정의부 중괄호·조건만 텍스트, 계산식은 전부 식 안
# 그림정보_이미지: 843dce17(대응 흐름도), 4881c5dc·6ebd200f(교점이 그래프에만) — 원본 해상도로 잘라 out/v15/figs/{id8}.png 첨부(기존 unsupported는 유지)
# 답은 모두 초안 값 유지(전 항목 재검산 일치).
ITEMS = []
def add(**kw): ITEMS.append(kw)
EXTRAS = []
def add_extra(**kw): EXTRAS.append(kw)

# ================= esc_sonnet_h1-1_1of4 =================
# 0. 40136dab — seq 6: 올림 기호 <x>
add(id='40136dab', qtype='choice',
    question='[[x]]보다 작거나 같은 정수 중에서 최대의 정수를 [[floor(x)]], [[x]]보다 크거나 같은 정수 중에서 최소의 정수를 [[nota(lt, x)]]로 나타낼 때, 방정식 [[floor(x) + nota(lt, x) = 7]]의 해를 구하면?',
    choices=['[[frac(7,2)]]', '[[3 <= x <= 4]]', '[[3 <= x < 4]]', '[[3 < x <= 4]]', '[[3 < x < 4]]'],
    figure=None,
    confidence=0.85,
    note='올림 기호 <x>를 nota(lt, x)로 쓰고 방정식 [x]+<x>=7을 한 식으로. 답 ⑤ 유지(2[x]+1=7 → [x]=3, x 비정수 → 3<x<4; 빠른정답 2와 불일치는 초안대로)')

# ================= esc_sonnet_h1-1_2of4 =================
# 1. 843dce17 — seq 99: 전치행렬 Bᵗ + 대응 흐름도(그림에만)
add(id='843dce17', qtype='choice',
    question='백의 자리의 수, 십의 자리의 수, 일의 자리의 수가 각각 [[a]], [[b]], [[c]]인 세 자리 자연수 [[n]]에 행렬 [[A = mat(2,2, a, b, c, b + c)]]를 대응시키는 것을 [그림 1]과 같이 나타내자.\n그리고 행렬 [[B = mat(2,2, p, q, r, s)]]에 대하여 행렬 [[tr(B)]]를\n[[tr(B) = mat(2,2, p, r, q, s)]]라 할 때 행렬 [[B]]에 행렬 [[tr(B)]]를 대응시키는 것을 [그림 2]와 같이 나타내자.\n아래 그림에서 행렬 [[X = mat(2,2, 7, 1, 9, 10)]]일 때\n자연수 [[n]]의 값은?',
    choices=['[[179]]', '[[197]]', '[[719]]', '[[791]]', '[[971]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '[그림 1] 원 n — 회색 마름모 — 사각형 A (세로 연결). [그림 2] 사각형 B — 회색 육각형 — 사각형 Bᵗ (가로 연결). 아래 그림: 원 n — 마름모 — 빈 사각형 — 육각형 — 빈 사각형 — 육각형 — 사각형 X (마름모 1회, 육각형 2회 적용)'}},
            {'fn': 'image', 'args': {'src': 'figs/843dce17.png', 'raw': '대응 흐름도: [그림 1] 원 n — 회색 마름모 — 사각형 A (세로). [그림 2] 사각형 B — 회색 육각형 — 사각형 Bᵗ (가로). 아래 그림: 원 n — 회색 마름모 — 빈 사각형 — 회색 육각형 — 빈 사각형 — 회색 육각형 — 사각형 X (마름모 1회, 육각형 2회)'}}],
    tags=['그림정보_이미지'],
    confidence=0.85,
    note='[2006년 9월 고2 이과 13번]. 전치행렬을 tr(B)로 교체; 대응 흐름도([그림 1]·[그림 2]·아래 그림)는 원본 해상도로 잘라 figs/843dce17.png 첨부(정보가 그림에만). 답 ③ 유지(전치 두 번 → A=X → a=7,b=1,c=9 → n=719; 빠른정답 216과 불일치는 초안대로)')

# 2·3. edbc609a / 7dce5be6 — seq 1 (같은 이미지 id 2개, 동일 내용): 이항연산 ◎
for _i in ('edbc609a', '7dce5be6'):
    add(id=_i, qtype='choice',
        question='실수 [[x]], [[y]]에 대하여 [[op(dcirc, x, y)]]를 행렬 [[mat(2,2, -x, y, y, -x)]]라 할 때,\n다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. 임의의 실수 [[a]], [[b]]에 대하여 [[op(dcirc, a, b) = op(dcirc, b, a)]]\nㄴ. 임의의 실수 [[a]], [[b]], [[c]], [[d]]에 대하여\n[[(op(dcirc, a, b)) - (op(dcirc, c, d)) = op(dcirc, (a - c), (b - d))]]\nㄷ. 임의의 실수 [[a]], [[b]], [[k]]에 대하여\n[[op(dcirc, (k a), (k b)) = k(op(dcirc, a, b))]]',
        choices=['ㄱ', 'ㄴ', 'ㄱ, ㄴ', 'ㄴ, ㄷ', 'ㄱ, ㄴ, ㄷ'],
        figure=None,
        confidence=0.85,
        note='같은 이미지에 id 2개(동일 내용). ◎를 op(dcirc)로 쓰고 보기 ㄱ~ㄷ의 등식을 전부 식 안에(ㄷ의 k(a◎b)는 원문 그대로). 답 ④ 유지(ㄱ✗ ㄴ✓ ㄷ✓; 빠른정답 4 ✓)')

# ================= esc_sonnet_h1-2_3of7 =================
# 4. ad241856 — seq 9: 꺾쇠 기호 ⟨a, b⟩ + 조건이 한글 문장인 경우 나눔 → 텍스트혼합
add(id='ad241856', qtype='choice',
    question='두 조건 [[a]], [[b]]에 대하여 [[nota(angle, a, b)]]를\n[[nota(lt, a, b)]] = { 1 ([[a]]가 [[b]]이기 위한 충분조건), 0 ([[a]]가 [[b]]이기 위한 필요충분조건), [[-1]] ([[a]]가 [[b]]이기 위한 필요조건) }\n으로 정의한다. 세 집합 [[A]], [[B]], [[X]]에 대하여 조건 [[p]], [[q]], [[r]]이 다음과 같을 때,\n[[p]]: [[subset(X, (inter(A, B)))]]\n[[q]]: [[subset(X, (union(A, B)))]]\n[[r]]: [[subset(X, A)]] 또는 [[subset(X, B)]]\n[[nota(angle, p, q) - 2 nota(angle, q, r) - 3 nota(angle, r, p)]]의 값은?',
    choices=['[[-6]]', '[[-4]]', '[[0]]', '[[4]]', '[[6]]'],
    figure=None,
    tags=['텍스트혼합'],
    confidence=0.8,
    note='[2007년 6월 고1 7번]. 꺾쇠 기호를 nota(angle, a, b)로(정의 줄은 원문 인쇄대로 <a, b> → nota(lt)), 마지막 계산식은 한 식으로. 텍스트 부분: 정의부의 중괄호와 세 조건(충분/필요충분/필요조건)이 한글 문장이라 "= { 1 (…), 0 (…), −1 (…) }"만 텍스트. 답 ⑤ 유지(⟨p,q⟩=1, ⟨q,r⟩=−1, ⟨r,p⟩=−1 → 1+2+3=6)')

# 5. 4109eceb — seq 16: P[x] 첨자 괄호
add(id='4109eceb', qtype='short',
    question='집합 [[P]]에 대하여 [[idx(P, x)]]를\n(1) [[in(x, P)]]이면 [[idx(P, x) = set(-x + 1, 0, x - 1)]]\n(2) [[notin(x, P)]]이면 [[idx(P, x) = set(1, x, pow(x,2))]]이라고 정의한다.\n두 집합 [[A]] = { [[x]] | [[x]]는 소수인 자연수 },\n[[B]] = { [[3x - 1]] | [[x]]는 자연수 }일 때, 집합\n[[union(idx((A - B), 2), idx((B - A), 8))]]의 원소의 총합을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='P[x]를 idx(P, x)로, (A−B)[2]∪(B−A)[8]을 union(idx(…), idx(…)) 한 식으로. 집합 A, B의 조건이 한글이라 조건제시법 중괄호·세로줄은 텍스트(가이드 §4). 답 7 유지((A−B)[2]={1,2,4}, (B−A)[8]={−7,0,7}; 빠른정답 2와 불일치는 초안대로)')

# ================= esc_sonnet_h1-2_5of7 =================
# 6. 3d3cfa68 — seq 4: 이항연산 △
add(id='3d3cfa68', qtype='choice',
    question='두 다항식 [[A]], [[B]]에 대하여 [[op(tri, A, B)]]를\n[[op(tri, A, B) = frac(A, A + B)]] 로 정의할 때,\n[[(op(tri, (2x - 4), (pow(x,2) - 4))) + (op(tri, (pow(x,2) + 2x), 2x))]]를 간단히 하면?',
    choices=['[[frac(1,4)]]', '[[frac(1,2)]]', '[[1]]', '[[x]]', '[[frac(1, pow(x,2))]]'],
    figure=None,
    confidence=0.85,
    note='△를 op(tri)로 쓰고 정의식·계산식을 식 안에(원문 중괄호는 소괄호). 답 ③ 유지(2/(x+4)+(x+2)/(x+4)=1; 빠른정답 1은 값 기준)')

# ================= esc_sonnet_m1-1_1of3 =================
# 7. ff10cc81 — seq 75: 이항연산 ⊗ (경우 나눔 정의)
add(id='ff10cc81', qtype='short',
    question='절댓값이 서로 다른 두 수 [[a]], [[b]]에 대하여\n[[op(otimes, a, b) = cases(abs(a), abs(a) < abs(b), abs(b), abs(a) > abs(b))]]라 할 때,\n[[op(otimes, (-frac(7,18)), (op(otimes, (-frac(11,2)), (-frac(9,5)))))]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='⊗를 op(otimes)로, 경우 나눔 정의(cases)와 계산식을 식 안에(원문 중괄호는 소괄호). 답 7/18 유지((−11/2)⊗(−9/5)=9/5, (−7/18)⊗(9/5)=7/18; 빠른정답 ✓)')

# 8. 53614914 — seq 76: 이항연산 ◇ (경우 나눔 정의)
add(id='53614914', qtype='short',
    question='절댓값이 서로 다른 두 수 [[a]], [[b]]에 대하여\n[[op(diamond, a, b) = cases(abs(a), abs(a) > abs(b), abs(b), abs(a) < abs(b))]]라 할 때,\n[[op(diamond, (op(diamond, (-frac(8,5)), (-frac(11,4)))), (-frac(16,3)))]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='◇를 op(diamond)로, 경우 나눔 정의(cases)와 계산식을 식 안에(원문 중괄호는 소괄호). 답 16/3 유지((−8/5)◇(−11/4)=11/4, (11/4)◇(−16/3)=16/3; 빠른정답 ✓)')

# 9. d25f4656 — seq 40: 꺾쇠 기호 ⟨x⟩ + 조건이 한글 문장인 경우 나눔 → 텍스트혼합
add(id='d25f4656', qtype='choice',
    question='수 [[x]]에 대하여\n[[nota(angle, x)]] = { 0 ([[x]]는 정수), 1 ([[x]]는 정수가 아닌 유리수) }로 약속할 때,\n다음 중 [[nota(angle, -frac(3,5)) + nota(angle, 0) + nota(angle, 2.6) + nota(angle, x) = 3]]을\n만족시키는 [[x]]가 될 수 없는 것은?',
    choices=['[[-frac(5,4)]]', '[[-0.1]]', '[[frac(6,2)]]', '[[frac(2,7)]]', '[[2.9]]'],
    figure=None,
    tags=['텍스트혼합'],
    confidence=0.8,
    note='꺾쇠 기호를 nota(angle, x)로, 방정식은 한 식으로. 텍스트 부분: 정의부 "= { 0 (x는 정수), 1 (x는 정수가 아닌 유리수) }"(조건이 한글 문장). 답 ③ 유지(1+0+1+⟨x⟩=3 → ⟨x⟩=1 → 6/2=3은 정수라 불가; 빠른정답 2와 불일치는 초안대로)')

# 10. 3babd113 — seq 66: 꺾쇠 기호 ⟨x⟩ + 조건이 한글 문장인 경우 나눔 → 텍스트혼합
add(id='3babd113', qtype='short',
    question='유리수 [[x]]에 대하여\n[[nota(angle, x)]] = { 0 ([[x]]는 정수), 1 ([[x]]는 정수가 아닌 유리수) }\n라 할 때, [[nota(angle, -frac(2,3)) + nota(angle, -2) + nota(angle, 3.4) + nota(angle, 0)]]의 값을 구하시오.',
    choices=None,
    figure=None,
    tags=['텍스트혼합'],
    confidence=0.8,
    note='꺾쇠 기호를 nota(angle, x)로, 계산식은 한 식으로. 텍스트 부분: 정의부 "= { 0 (x는 정수), 1 (x는 정수가 아닌 유리수) }"(조건이 한글 문장). 답 2 유지(1+0+1+0; 빠른정답 ✓)')

# ================= esc_sonnet_m1-1_3of3 =================
# 11. c0d134e4 — seq 30: 이항연산 ★(정의가 한글 문장 → 정의는 텍스트, 계산식만 op)
add(id='c0d134e4', qtype='short',
    question='[[x]]에 대한 일차식 [[A]]에서 [[x]]의 계수는 [[-2]]이다.\n[[op(star, A, a)]] = ([[x = a]]일 때, [[A]]의 식의 값)이라 할 때,\n[[op(star, A, (-1)) + op(star, A, 2) - op(star, A, (-2)) - op(star, A, 5)]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='★를 op(star)로: 정의 "(x=a일 때, A의 식의 값)"은 한글 문장이라 텍스트, 계산식은 한 식으로. 답 4 유지(A=−2x+c: (2+c)+(−4+c)−(4+c)−(−10+c)=4; 빠른정답 14와 불일치는 초안대로)')

# 12. c7632096 — seq 32: 이항연산 ★(정의가 한글 문장)
add(id='c7632096', qtype='short',
    question='[[x]]에 대한 일차식 [[A]]에서 [[x]]의 계수는 [[-5]]이다.\n[[op(star, A, a)]] = ([[x = a]]일 때, [[A]]의 식의 값)이라 할 때,\n[[op(star, A, (-1)) + op(star, A, 3) - op(star, A, (-5)) - op(star, A, 7)]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='★를 op(star)로: 정의 "(x=a일 때, A의 식의 값)"은 한글 문장이라 텍스트, 계산식은 한 식으로. 답 0 유지(A=−5x+c: (5+c)+(−15+c)−(25+c)−(−35+c)=0; 빠른정답 없음)')

# 13. c3f5bc90 — seq 59: 이항연산 ★, ◎
add(id='c3f5bc90', qtype='choice',
    question='두 단항식 [[A]], [[B]]에 대하여 [[op(star, A, B) = -A + 2B]],\n[[op(dcirc, A, B) = -2A + 3B]]라 할 때,\n[[2(op(star, (3x), y)) - (op(dcirc, x, (-y)))]]를 계산한 것은?',
    choices=['[[-4x + 5y]]', '[[-4x + 7y]]', '[[-4x + 9y]]', '[[-2x + 5y]]', '[[-2x + 7y]]'],
    figure=None,
    confidence=0.85,
    note='★·◎를 op(star)·op(dcirc)로, 정의식·계산식을 식 안에(원문 중괄호는 소괄호). 답 ② 유지((3x)★y=−3x+2y, x◎(−y)=−2x−3y → −4x+7y; 빠른정답 없음)')

# 14. b4aaf009 — seq 60: 이항연산 ◉, ▼
add(id='b4aaf009', qtype='short',
    question='두 단항식 [[A]], [[B]]에 대하여 [[(op(fisheye, A, B)) = 4A - 3B]],\n[[(op(bdtri, A, B)) = B - 2A]]라 할 때, [[2(op(fisheye, 2x, y)) - (op(bdtri, x, 3y))]]를 계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='◉·▼를 op(fisheye)·op(bdtri)로, 정의식·계산식을 식 안에(원문 소괄호 유지). 답 −162 유지(2x◉y=8x−3y, x▼3y=3y−2x → 18x−9y → 18×(−9); 빠른정답 없음)')

# 15. b3b71280 — seq 61: 이항연산 ★, ◎
add(id='b3b71280', qtype='short',
    question='두 단항식 [[A]], [[B]]에 대하여 [[(op(star, A, B)) = 3A - frac(1,2) B]],\n[[(op(dcirc, A, B)) = 2B - A]]라 할 때,\n[[2(op(star, (x + 2y), (3y - x))) + (op(dcirc, (x - y), (2x + 3y)))]]를\n계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='★·◎를 op(star)·op(dcirc)로, 정의식·계산식을 식 안에(원문 중괄호는 소괄호). 답 160 유지(2(7x/2+9y/2)+(3x+7y)=10x+16y → 160; 빠른정답 없음)')

# 16. ec503ead — seq 62: 이항연산 ◎, ◆
add(id='ec503ead', qtype='choice',
    question='두 단항식 [[A]], [[B]]에 대하여 [[(op(dcirc, A, B)) = 3A - 2B]],\n[[(op(bdiamond, A, B)) = B - A]]라 할 때, [[2(op(dcirc, x, 3y)) - (op(bdiamond, 2x, y))]]를 계산한 식에서 [[x]]의 계수와 [[y]]의 계수의 곱은?',
    choices=['[[-120]]', '[[-104]]', '[[-91]]', '[[91]]', '[[104]]'],
    figure=None,
    confidence=0.85,
    note='◎·◆를 op(dcirc)·op(bdiamond)로, 정의식·계산식을 식 안에(원문 소괄호 유지). 답 ② 유지(x◎3y=3x−6y, 2x◆y=y−2x → 8x−13y → −104; 빠른정답 없음)')

# 17. 41ffd03a — seq 37: 약속 기호 ⟨a⟩(약수의 개수)·{a}(약수의 합)
add(id='41ffd03a', qtype='short',
    question='자연수 [[a]]의 약수의 개수를 [[nota(angle, a)]], 자연수 [[a]]의 모든 약수의 합을 [[nota(brace, a)]]라 하자. [[nota(angle, 72) = x]], [[nota(brace, x) = y]]일 때, [[x + y]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='⟨a⟩를 nota(angle, a), {a}를 nota(brace, a)로. 답 40 유지(72=2³·3² → x=12, 12의 약수의 합 28 → 40; 빠른정답 3과 불일치는 초안대로)')

# ================= esc_sonnet_m2-1_3of4 =================
# 18. caef767c — seq 39: 이항연산 ◎ (경우 나눔 정의)
add(id='caef767c', qtype='short',
    question='두 수 [[a]], [[b]]에 대하여 [[op(dcirc, a, b) = cases(-1, a > b, 0, a = b, 1, a < b)]]로 정의할 때, [[op(dcirc, (op(dcirc, 0.5, recdec(0, 5))), (op(dcirc, 1.3, recdec(1.2, 9))))]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='◎를 op(dcirc)로, 경우 나눔 정의(cases)와 계산식을 식 안에. 답 −1 유지(0.5<0.5̇ → 1, 1.3=1.29̇ → 0, 1◎0=−1; 빠른정답 ✓)')

# 19. 6d12b521 — seq 40: 이항연산 ∘ (경우 나눔 정의)
add(id='6d12b521', qtype='short',
    question='[[op(ring, a, b)]]를 [[cases(1, a = b, 0, a != b)]]이라 하면 [[a = recdec(0.1, 9)]], [[b = 0.2]], [[c = recdec(0, 01)]], [[d = frac(1, 90)]]일 때, [[op(ring, (op(ring, a, b)), (op(ring, c, d)))]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='∘를 op(ring)으로, 경우 나눔(a=b이면 1, a≠b이면 0)은 cases, 계산식은 한 식으로. 답 0 유지(a=0.2=b → 1; c=1/99≠1/90 → 0; 1∘0=0; 빠른정답 3과 불일치는 초안대로)')

# 20. 46c6384a — seq 33: 이항연산 ○·□ (분수 형태 계산식)
add(id='46c6384a', qtype='short',
    question='두 문자 [[a]], [[b]]에 대하여 기호 ○, □를 [[op(circ, a, b) = a pow(b,2)]], [[op(sq, a, b) = 4a b]]라 약속할 때, [[frac(op(circ, a, (op(sq, b, a))), op(sq, b, (op(circ, b, a))))]]를 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='○·□를 op(circ)·op(sq)로, 정의식과 분수 형태 계산식을 식 안에("기호 ○, □를"의 낱 기호는 텍스트). 답 4a 유지(16a³b²/(4a²b²); 빠른정답 3과 불일치는 초안대로)')

# 21. ae6535ac — seq 58: 이항연산 △·◎
add(id='ae6535ac', qtype='choice',
    question='두 식 [[a]], [[b]]에 대하여 △, ◎를 [[op(tri, a, b) = a pow(b,2)]], [[op(dcirc, a, b) = 3 pow(a,2) b]]로 약속하자. 이때 다음을 만족시키는 두 식 [[A]], [[B]]에 대하여 [[5 pow(A,2) ÷ (2B)]]를 계산하면?\n[[op(tri, A, 2x) = 8 pow(x,3) pow(y,2)]], [[op(dcirc, y, B) = 15 pow(x,2) pow(y,3)]]',
    choices=['[[frac(2, x pow(y,3))]]', '[[frac(1, 2 pow(x,2) y)]]', '[[frac(1, 2 pow(y,3))]]', '[[frac(x pow(y,3), 2)]]', '[[2 pow(y,3)]]'],
    figure=None,
    confidence=0.85,
    note='△·◎를 op(tri)·op(dcirc)로, 정의식·조건식을 식 안에(낱 기호 "△, ◎를"은 텍스트; 5A²÷2B는 초안대로 ÷(2B)). 답 ⑤ 유지(A=2xy², B=5x²y → 2y³; 빠른정답 5 ✓)')

# ================= esc_sonnet_m3-1_1of6 =================
# 22. 2ff38624 — seq 88: 약속 기호 ⟨a, b⟩(최대공약수)·[a, b](최소공배수)
add(id='2ff38624', qtype='short',
    question='두 자연수 [[a]], [[b]]의 최대공약수를 [[nota(angle, a, b)]]라 하고 최소공배수를 [[nota(sq, a, b)]]라 하자. [[x]]에 대한 이차방정식 [[nota(angle, a, b) pow(x,2) - nota(sq, a, b) x + 10 = 0]]의 두 근이 1, 5일 때, [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)',
    choices=None,
    figure=None,
    confidence=0.85,
    note='⟨a, b⟩를 nota(angle, a, b), [a, b]를 nota(sq, a, b)로 쓰고 이차방정식을 한 식으로. 답 10 유지(근 1, 5 → gcd 2, lcm 12 → (4, 6); 빠른정답 38과 불일치는 초안대로)')

# 23. 9c48e8fd — seq 89
add(id='9c48e8fd', qtype='short',
    question='두 자연수 [[a]], [[b]]의 최대공약수를 [[nota(angle, a, b)]]라 하고 최소공배수를 [[nota(sq, a, b)]]라 하자. [[x]]에 대한 이차방정식 [[nota(angle, a, b) pow(x,2) - nota(sq, a, b) x + 24 = 0]]의 두 근이 2, 4일 때, [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)',
    choices=None,
    figure=None,
    confidence=0.85,
    note='⟨a, b⟩를 nota(angle, a, b), [a, b]를 nota(sq, a, b)로 쓰고 이차방정식을 한 식으로. 답 15 유지(근 2, 4 → gcd 3, lcm 18 → (6, 9); 빠른정답 2와 불일치는 초안대로)')

# 24. d705aba8 — seq 90
add(id='d705aba8', qtype='short',
    question='두 자연수 [[a]], [[b]]의 최대공약수를 [[nota(angle, a, b)]]라 하고 최소공배수를 [[nota(sq, a, b)]]라 하자. [[x]]에 대한 이차방정식 [[nota(angle, a, b) pow(x,2) - nota(sq, a, b) x + 54 = 0]]의 두 근이 3, 9일 때, [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)',
    choices=None,
    figure=None,
    confidence=0.85,
    note='⟨a, b⟩를 nota(angle, a, b), [a, b]를 nota(sq, a, b)로 쓰고 이차방정식을 한 식으로. 답 14 유지(근 3, 9 → gcd 2, lcm 24 → (6, 8); 빠른정답 4와 불일치는 초안대로)')

# 25. e2eccd2a — seq 93: ⟨x⟩(x보다 작은 소수의 개수)
add(id='e2eccd2a', qtype='short',
    question='[[nota(angle, x)]]를 자연수 [[x]]보다 작은 소수의 개수라 할 때, 방정식 [[4 pow(nota(angle, x), 2) - 29 nota(angle, x) - 24 = 0]]을 만족시키는 모든 자연수 [[x]]의 값의 합을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='⟨x⟩를 nota(angle, x)로 쓰고 방정식을 한 식으로. 답 86 유지(⟨x⟩=8 → x=20~23 → 86; 빠른정답 14와 불일치는 초안대로)')

# 26. 9834d721 — seq 94: <x>(x 이하의 소수의 개수)
add(id='9834d721', qtype='choice',
    question='자연수 [[x]]에 대하여 [[nota(lt, x)]]는 [[x]] 이하의 소수의 개수라 할 때, 다음 중 [[pow(nota(lt, x), 2) - 2 nota(lt, x) - 24 = 0]]을 만족시키는 자연수 [[x]]가 될 수 없는 것은?',
    choices=['[[13]]', '[[14]]', '[[15]]', '[[16]]', '[[17]]'],
    figure=None,
    confidence=0.85,
    note='<x>를 nota(lt, x)로 쓰고 방정식을 한 식으로. 답 ⑤ 유지(<x>=6 → x=13~16, <17>=7; 빠른정답 38과 불일치는 초안대로)')

# 27. e62ac95b — seq 96
add(id='e62ac95b', qtype='choice',
    question='자연수 [[x]]에 대하여 [[nota(lt, x)]]는 [[x]] 이하의 소수의 개수라 할 때, 다음 중 [[pow(nota(lt, x), 2) + nota(lt, x) - 20 = 0]]을 만족시키는 자연수 [[x]]가 될 수 없는 것은?',
    choices=['[[6]]', '[[7]]', '[[8]]', '[[9]]', '[[10]]'],
    figure=None,
    confidence=0.85,
    note='<x>를 nota(lt, x)로 쓰고 방정식을 한 식으로. 답 ① 유지(<x>=4 → x=7~10, <6>=3; 빠른정답 86과 불일치는 초안대로)')

# 28. b64f5373 — seq 98: ⟨x⟩(약수의 개수)
add(id='b64f5373', qtype='choice',
    question='자연수 [[x]]의 약수의 개수를 [[nota(angle, x)]]로 나타낼 때,\n등식 [[pow(nota(angle, x), 2) + 2 nota(angle, x) - 8 = 0]]을 만족시키는 20 이하의 자연수 [[x]]의 개수는?',
    choices=['[[4]]', '[[5]]', '[[6]]', '[[7]]', '[[8]]'],
    figure=None,
    confidence=0.85,
    note='⟨x⟩를 nota(angle, x)로 쓰고 등식을 한 식으로. 답 ⑤ 유지(⟨x⟩=2 → 20 이하 소수 8개; 빠른정답 2와 불일치는 초안대로)')

# 29. 150ffcdb — seq 99 (같은 이미지 하단 문항): {x}(약수의 개수)
add(id='150ffcdb', qtype='short',
    question='자연수 [[x]]의 약수의 개수를 [[nota(brace, x)]]로 나타낼 때,\n등식 [[pow(nota(brace, x), 2) - 26 nota(brace, x) - 27 = 0]]을 만족시키는 가장 작은 자연수 [[x]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='같은 이미지 하단 문항. {x}를 nota(brace, x)로 쓰고 등식을 한 식으로. 답 900 유지({x}=27 → 2²·3²·5²=900; 빠른정답 1과 불일치는 초안대로)')

# 30. edd27c48 — seq 99 (같은 이미지 상단 문항)
add(id='edd27c48', qtype='short',
    question='자연수 [[x]]의 약수의 개수를 [[nota(brace, x)]]로 나타낼 때,\n등식 [[pow(nota(brace, x), 2) - 3 nota(brace, x) - 18 = 0]]을 만족시키는 가장 작은 자연수 [[x]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note='같은 이미지 상단 문항. {x}를 nota(brace, x)로 쓰고 등식을 한 식으로. 답 12 유지({x}=6 → 12; 빠른정답 1과 불일치는 초안대로)')

# ================= esc_sonnet_m3-1_4of6 =================
# 31. defa43ac — seq 49: 약속 기호 <a, b>(사이의 점의 개수)
add(id='defa43ac', qtype='short',
    question='자연수의 양의 제곱근 [[1]], [[sqrt(2)]], [[sqrt(3)]], [[2]], ⋯에 대응하는 점을 수직선 위에 다음 그림과 같이 차례대로 나타낸다. 아래 수직선에서 [[a]], [[b]] 사이에 있는 점의 개수를 [[nota(lt, a, b)]]라 하면 [[nota(lt, 1, 2) = 2]], [[nota(lt, 2, 3) = 4]]이다. 이때 [[nota(lt, 2000, 2001)]]의 값을 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '수직선 위에 점 1, √2, √3, 2, √5, √6, √7, √8, 3이 차례로 찍혀 있음(√6, √8은 위쪽에 표기)'}}],
    confidence=0.85,
    note='<a, b>를 nota(lt, a, b)로 쓰고 예시 등식·물음을 식 안에(수열 나열의 줄임표는 텍스트). 수직선 그림은 unsupported(raw) 유지(내용이 본문에 있음). 답 4000 유지(<n, n+1>=2n; 빠른정답 1과 불일치는 초안대로)')

# 32. 343af482 — seq 91: 이항연산 ◎
add(id='343af482', qtype='choice',
    question='두 실수 [[a]], [[b]]에 대하여 [[op(dcirc, a, b) = -a + b + a b]]일 때, [[op(dcirc, (3x - 1), (x + 2)) = k]]가 근을 갖도록 하는 상수 [[k]]의 값 중 가장 작은 값은?',
    choices=['[[-frac(1,2)]]', '[[-frac(1,4)]]', '[[0]]', '[[frac(1,4)]]', '[[frac(1,2)]]'],
    figure=None,
    confidence=0.85,
    note='◎를 op(dcirc)로, 정의식·방정식을 식 안에. 답 ④ 유지(3x²+3x+1=k → D=12k−3≥0 → k≥1/4; 빠른정답 4 ✓)')

# ================= esc_sonnet_m2-1_1of4 =================
# 33. 4881c5dc — seq 3: 프라임 상수 a′, b′, c′ + 교점이 그래프에만
add(id='4881c5dc', qtype='choice',
    question="다음 그림은 연립방정식 [[a x + b y = c]], [[a' x + b' y = c']]을 그래프로 나타낸 것이다. 이 연립방정식의 해를 [[point(m, n)]]라고 할 때, [[pow(m,2) + 2n]]의 값은?",
    choices=['[[5]]', '[[6]]', '[[7]]', '[[8]]', '[[9]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '좌표평면: 증가 직선 ax+by=c(점 (−2, 1), (0, 5) 통과)와 감소 직선 a′x+b′y=c′(점 (−3, 5) 통과)가 점 (−1, 3)에서 만남. x축 −3, −2, −1과 y축 1, 3, 5에 점선 좌표 표시'}},
            {'fn': 'image', 'args': {'src': 'figs/4881c5dc.png', 'raw': '좌표평면 그래프: 증가 직선 ax+by=c(점 (−2, 1), (0, 5) 통과)와 감소 직선 a′x+b′y=c′(점 (−3, 5) 통과)가 점 (−1, 3)에서 만남. x축 −3, −2, −1과 y축 1, 3, 5에 점선 좌표 표시, 원점 O'}}],
    tags=['그림정보_이미지'],
    confidence=0.85,
    note="프라임 상수를 a' x + b' y = c'(변수 프라임)로 교체(연립의 중괄호는 콤마 나열). 교점 정보가 그래프에만 있어 원본 해상도로 잘라 figs/4881c5dc.png 첨부(unsupported는 유지). 답 ③ 유지(교점 (−1, 3) → 1+6=7; 빠른정답 3 ✓)")

# 34. 6ebd200f — seq 5: 프라임 상수 + 교점이 그래프에만
add(id='6ebd200f', qtype='choice',
    question="[[x]], [[y]] 에 관한 연립방정식 [[a x + b y = c]] ⋯㉠, [[a' x + b' y = c']] ⋯㉡ 을 다음 그림과 같이 그래프를 이용하여 풀었다. 해가 [[point(m, n)]]일 때,\n[[m + n]]의 값은?",
    choices=['[[-3]]', '[[-2]]', '[[-1]]', '[[1]]', '[[2]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '좌표평면: 증가 직선 ㉠(y절편 2)과 감소 직선 ㉡이 점 (−2, 1)에서 만남(점선으로 x=−2, y=1 표시), 원점 O'}},
            {'fn': 'image', 'args': {'src': 'figs/6ebd200f.png', 'raw': '좌표평면 그래프: 증가 직선 ㉠(y절편 2)과 감소 직선 ㉡이 점 (−2, 1)에서 만남(점선으로 x=−2, y=1 표시), 원점 O'}}],
    tags=['그림정보_이미지'],
    confidence=0.85,
    note="프라임 상수를 a' x + b' y = c'(변수 프라임)로 교체(㉠㉡ 줄 표지는 텍스트). 교점 정보가 그래프에만 있어 원본 해상도로 잘라 figs/6ebd200f.png 첨부(unsupported는 유지). 답 ③ 유지(교점 (−2, 1) → m+n=−1; 빠른정답 3 ✓)")

# 35. 35d63ad8 — seq 56: 프라임 상수
add(id='35d63ad8', qtype='short',
    question="[[x]], [[y]] 에 대한 두 일차방정식 [[a x + b y + c = 0]], [[a' x + b' y + c' = 0]]의 그래프가 한 점에서 만날 때, 다음 보기 중 연립방정식 [[a x + b y + c = 0]], [[a' x + b' y + c' = 0]]의 해로 알맞은 것을 고르시오.\n<보기>\nㄱ. 해가 없다.\nㄴ. 한 쌍의 해를 갖는다.\nㄷ. 해가 무수히 많다.",
    choices=None,
    figure=None,
    confidence=0.85,
    note="프라임 상수를 a' x + b' y + c' = 0(변수 프라임)으로 교체(연립의 중괄호는 콤마 나열). 답 ㄴ 유지(한 점에서 만남 → 한 쌍의 해; 빠른정답 없음)")
