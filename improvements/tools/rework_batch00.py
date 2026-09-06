# -*- coding: utf-8 -*-
# batch00 (h1-1·h1-2 보류분 40문항) — v1.5 문법 재작업
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# 0. 3df2f98a — 선분 AA′(프라임 라벨) + 빈칸 상자 → seg(AA'), box(1)/box(2)
add(id="3df2f98a", qtype="short",
    question="자연수 [[n]]에 대하여 이차함수 [[y = 2 pow(x,2)]]의 그래프와 직선 [[y = n x]]의 교점 중 원점이 아닌 점을 A, 이차함수 [[y = 2 pow(x,2)]]의 그래프와 직선 [[y = (n + 2) x]]의 교점 중 원점이 아닌 점을 B라 하자. 다음은 삼각형 OAB의 넓이를 [[S(n)]]이라 할 때, [[S(n) > 100]]을 만족시키는 [[n]]의 최솟값을 구하는 과정이다. (단, O는 원점이다.)\n\n이차함수 [[y = 2 pow(x,2)]]의 그래프와 직선 [[y = n x]]의 교점 A의 [[x]]좌표를 구하면 [[2 pow(x,2) = n x]] ([[a != 0]])에서\n[[x = frac(n,2)]]\n점 A를 지나고 [[x]]축에 수직인 직선이 직선 [[y = (n + 2) x]]와 만나는 점을 A′이라 하자. 선분 AA′의 길이는\n[[seg(AA') = box(1) - frac(pow(n,2),2)]] 이므로\n삼각형 OAB의 넓이 [[S(n)]]은\n[[S(n) = frac(1,2) × n × (box(2))]]\n따라서 [[S(n) > 100]]을 만족시키는 자연수 [[n]]의 최솟값은 (다) 이다.\n\n위의 (가), (나)에 알맞은 식을 각각 [[f(n)]], [[g(n)]]이라 하고, (다)에 알맞은 수를 [[k]]라 할 때, [[f(k) + g(k)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2018년 11월 고1 29번/4점]. 선분 AA′→seg(AA'), 빈칸 (가)(나)→box(1)/box(2)(식 안), (다)는 문장 속이라 텍스트. 원문 '(a ≠ 0)' 그대로. 답 231 유지")

# 1. 40136dab — 올림 기호 <x>: v1.5에도 없음 → 텍스트 혼합 유지, 보류
add(id="40136dab", qtype="choice",
    question="[[x]]보다 작거나 같은 정수 중에서 최대의 정수를 [[floor(x)]], [[x]]보다 크거나 같은 정수 중에서 최소의 정수를 <[[x]]>로 나타낼 때, 방정식 [[floor(x)]] + <[[x]]> = 7의 해를 구하면?",
    choices=["[[frac(7,2)]]", "[[3 <= x <= 4]]", "[[3 <= x < 4]]", "[[3 < x <= 4]]", "[[3 < x < 4]]"],
    figure=None, confidence=0.75,
    needs_review="문법 범위 밖: 사용자 정의 기호 <x>(올림) — v1.5에도 대응 함수 없음, 텍스트 혼합 유지",
    note="답 ⑤ 유지(2[x]+1=7 → 3<x<4)")

# 2. 33ea1858 — C′은 단독 점 이름(텍스트 허용), 도형은 unsupported → 통과
add(id="33ea1858", qtype="choice",
    question="다음 그림과 같이 반원에 내접하는 가장 큰 원 [[C]]와 반원에 내접하고 원 [[C]]에 외접하는 원 C′이 있다. [[seg(AB) = 16]]일 때, 두 원 [[C]], C′의 반지름의 길이를 두 근으로 하고 [[pow(x,2)]]의 계수가 1인 이차방정식은?",
    choices=["[[pow(x,2) - 8x + 12 = 0]]", "[[pow(x,2) - 8 sqrt(2) x + 16 = 0]]", "[[pow(x,2) - 12x + 32 = 0]]", "[[pow(x,2) - 12 sqrt(2) x + 64 = 0]]", "[[pow(x,2) - 16x + 32 = 0]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "반원 안에 큰 원 C(반원의 지름과 점 A에서 접함, A는 반원의 중심 위치)와 작은 원 C′(지름과 점 B에서 접하고 반원·원 C에 접함), 두 원의 중심에서 지름에 내린 수선(직각 표시), AB=16"}}],
    confidence=0.8,
    note="C′은 단독 점 이름이라 텍스트. 도형 unsupported(정보는 raw에). 답 ④ 유지(R=16√2, 반지름 8√2·4√2)")

# 3. e4f93b49 — Q₁(x) → app(sub(Q,1), x)
add(id="e4f93b49", qtype="choice",
    question="다항식 [[P(x)]]를 [[8x - 2]]로 나누었을 때의 몫을 [[app(sub(Q,1), x)]], 나머지를 [[sub(R,1)]]이라 하고 [[x - frac(1,4)]]로 나누었을 때의 몫을 [[app(sub(Q,2), x)]], 나머지를 [[sub(R,2)]]라 할 때, [[frac(app(sub(Q,2), x), app(sub(Q,1), x)) + frac(sub(R,1), sub(R,2))]]의 값은?\n(단, [[app(sub(Q,1), x) != 0]], [[sub(R,1) != 0]])",
    choices=["[[8]]", "[[9]]", "[[10]]", "[[11]]", "[[12]]"],
    figure=None, confidence=0.85,
    note="첨자 함수 Q₁(x)를 app(sub(Q,1), x)로. 답 ② 유지(Q₂=8Q₁, R₂=R₁ → 9)")

# 4. 43c2f901 — 동일 패턴
add(id="43c2f901", qtype="short",
    question="다항식 [[P(x)]]를 [[10x - 2]]로 나누었을 때의 몫을 [[app(sub(Q,1), x)]], 나머지를 [[sub(R,1)]]이라 하고 [[x - frac(1,5)]]로 나누었을 때의 몫을 [[app(sub(Q,2), x)]], 나머지를 [[sub(R,2)]]라 할 때, [[frac(app(sub(Q,2), x), app(sub(Q,1), x)) + frac(sub(R,2), sub(R,1))]]의 값을 구하시오. (단, [[app(sub(Q,1), x) != 0]], [[sub(R,1) != 0]])",
    choices=None, figure=None, confidence=0.85,
    note="첨자 함수 Q₁(x)를 app(sub(Q,1), x)로. 답 11 유지(Q₂=10Q₁, R₂=R₁ → 11)")

# 5. f1b545c4 — 조각적 정의 → cases
add(id="f1b545c4", qtype="short",
    question="행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j) = cases(2 pow(i,2) - pow(j,2), i >= j, sub(a,j,i), i < j)]]\n(단, [[i]] = 1, 2, 3, [[j]] = 1, 2, 3)일 때, 행렬 [[A]]의 제1행의 모든 성분의 합을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔 정의를 cases로. 답 25 유지(1+7+17)")

# 6. f75cf502 — cases
add(id="f75cf502", qtype="choice",
    question="이차함수 [[f(x) = pow(x,2) - 3x + 4]]에 대하여 [[3 × 3]] 행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가 [[sub(a,i,j) = cases(1, abs(f(i)) = j, 2, abs(f(i)) != j)]]일 때,\n행렬 [[A]]는?",
    choices=["[[mat(3,3, 2,1,2, 2,1,2, 2,2,2)]]", "[[mat(3,3, 1,2,2, 2,2,1, 2,2,2)]]", "[[mat(3,3, 1,2,2, 2,2,1, 2,2,1)]]", "[[mat(3,3, 2,2,1, 2,2,1, 2,2,1)]]", "[[mat(3,3, 2,2,2, 2,1,2, 2,2,1)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔 정의를 cases로. 답 ① 유지(f(1)=f(2)=2, f(3)=4)")

# 7. 11d780f5 — cases
add(id="11d780f5", qtype="choice",
    question="이차함수 [[f(x) = 2 pow(x,2) - 3x + 2]]에 대하여 [[3 × 3]] 행렬 [[A]]의 ([[i]], [[j]]) 성분 [[sub(a,i,j)]]가 [[sub(a,i,j) = cases(1, abs(f(i)) = pow(j,2), -1, abs(f(i)) != pow(j,2))]]일 때, 행렬 [[A]]는?",
    choices=["[[mat(3,3, -1,1,-1, 1,-1,-1, -1,-1,-1)]]", "[[mat(3,3, 1,-1,-1, -1,-1,1, 1,-1,-1)]]", "[[mat(3,3, 1,-1,-1, -1,1,-1, -1,-1,-1)]]", "[[mat(3,3, -1,1,-1, 1,-1,-1, -1,-1,-1)]]", "[[mat(3,3, 1,-1,-1, -1,-1,1, -1,-1,-1)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔 정의를 cases로. 답 ③ 유지(f(1)=1, f(2)=4, f(3)=11). 원문 선지 ①·④ 동일(원문 그대로)")

# 8. 6bbe9ed6 — cases의 식이 한글 문장(경로의 수) → cases 불가, 보류 유지
add(id="6bbe9ed6", qtype="short",
    question="세 공원 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]을 연결하는 산책로가 다음 그림과 같다. 행렬 [[A]]의 [[point(i, j)]] 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j)]] = { (공원 [[sub(P,i)]]에서 공원 [[sub(P,j)]]로 가는 경로의 수) ([[i != j]]) ; 0 ([[i = j]]) }\n일 때, 행렬 [[A]]의 모든 성분의 합을 구하시오.\n(단, [[i]] = 1, 2, 3, [[j]] = 1, 2, 3)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "세 공원 P₁, P₂, P₃ 삽화가 가로로 놓이고 P₁–P₂ 사이에 산책로 3개(위 곡선·가운데 직선·아래 곡선), P₂–P₃ 사이에 산책로 3개가 그려져 있음(P₁–P₃ 직접 연결 없음)"}}],
    confidence=0.75,
    needs_review="경우 나눔 정의의 식이 한글 문장(경로의 수)이라 cases로 쓸 수 없음 — 텍스트 혼합 유지; 경로 수는 그림에서만 판독(P₁–P₂ 3개, P₂–P₃ 3개)",
    note="답 30 유지(a12=a21=a23=a32=3, a13=a31=9)")

# 9. 1c800bda — 텍스트는 문법 안, 도형은 unsupported(교점 판독 확인) → 통과
add(id="1c800bda", qtype="choice",
    question="아래 그림과 같이 삼각형 [[sub(P,1)]], 사각형 [[sub(P,2)]], 원 [[sub(P,3)]]이 있다. 삼차정사각행렬 [[A]]의 [[point(i, j)]] 성분 [[sub(a,i,j)]]가 다음을 만족시킬 때, 행렬 [[A]]는?\n(가) [[i = j]]일 때, [[sub(a,i,j) = 0]]\n(나) [[i != j]]일 때, [[sub(a,i,j)]]는 도형 [[sub(P,i)]]와 도형 [[sub(P,j)]]의 교점의 개수이다.",
    choices=["[[mat(3,3, 0,3,4, 3,0,5, 4,5,0)]]", "[[mat(3,3, 0,5,4, 5,0,3, 4,3,0)]]", "[[mat(3,3, 0,5,4, 5,0,5, 4,5,0)]]", "[[mat(3,3, 0,4,5, 4,0,4, 5,4,0)]]", "[[mat(3,3, 0,4,5, 4,0,5, 5,5,0)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 P₁(위 꼭짓점은 직사각형 위쪽 바깥, 왼쪽 아래 꼭짓점은 직사각형 P₂의 왼쪽 아래 꼭짓점과 일치, 오른쪽 아래 꼭짓점은 직사각형 아래쪽 바깥), 직사각형 P₂, 원 P₃(직사각형의 윗변·오른쪽 변에 접하고 아랫변과 두 점에서 만나 아래로 튀어나옴; 삼각형의 왼쪽 변에 접하고 오른쪽 변·아랫변과는 각각 두 점에서 만남). 교점 수: P₁∩P₂ 4, P₁∩P₃ 5, P₂∩P₃ 4"}}],
    confidence=0.75,
    note="본문은 문법 안. 확대 판독으로 교점 수(4, 5, 4) 재확인 → 답 ④ 유지. 도형 정보는 raw 설명에")

# 10. 5bb4250a — b_ij 조각적 정의 → cases
add(id="5bb4250a", qtype="short",
    question="두 이차정사각행렬 [[A]], [[B]]의 [[point(i, j)]] 성분 [[sub(a,i,j)]], [[sub(b,i,j)]]가\n[[sub(a,i,j) = 2p i - q j]], [[sub(b,i,j) = cases(frac(1,3) i - frac(1,6) j + 2, i != j, frac(1,2)(2i + j), i = j)]]이고\n[[A = B]]일 때, 상수 [[p]], [[q]]에 대하여 [[8p q]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔 정의를 cases로. 답 -2 유지(p=1/2, q=-1/2)")

# 11. 843dce17 — 전치행렬 Bᵗ 표기는 v1.5에도 없음(pow 우회) + 대응 흐름도 정보가 그림에만 → 보류 유지
add(id="843dce17", qtype="choice",
    question="백의 자리의 수, 십의 자리의 수, 일의 자리의 수가 각각 [[a]], [[b]], [[c]]인 세 자리 자연수 [[n]]에 행렬 [[A = mat(2,2, a, b, c, b + c)]]를 대응시키는 것을 [그림 1]과 같이 나타내자.\n그리고 행렬 [[B = mat(2,2, p, q, r, s)]]에 대하여 행렬 [[pow(B, t)]]를\n[[pow(B, t) = mat(2,2, p, r, q, s)]]라 할 때 행렬 [[B]]에 행렬 [[pow(B, t)]]를 대응시키는 것을 [그림 2]와 같이 나타내자.\n아래 그림에서 행렬 [[X = mat(2,2, 7, 1, 9, 10)]]일 때\n자연수 [[n]]의 값은?",
    choices=["[[179]]", "[[197]]", "[[719]]", "[[791]]", "[[971]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "[그림 1] 원 n — 회색 마름모 — 사각형 A (세로 연결). [그림 2] 사각형 B — 회색 육각형 — 사각형 Bᵗ (가로 연결). 아래 그림: 원 n — 마름모 — 빈 사각형 — 육각형 — 빈 사각형 — 육각형 — 사각형 X (마름모 1회, 육각형 2회 적용)"}}],
    confidence=0.75,
    needs_review="문법 범위 밖: 전치행렬 Bᵗ 표기 없음(pow(B, t)로 우회, 뜻이 다름) / 대응 흐름도(연산 순서)가 그림에만 있음",
    note="[2006년 9월 고2 이과 13번]. 답 ③ 유지(전치 두 번 → A=X → n=719)")

# 12. 758f0c98 — cases
add(id="758f0c98", qtype="short",
    question="함수 [[f(x) = cases(x + 10, x < 0, pow(x,2) - 8x + 10, x >= 0)]]에 대하여\n[[h(x) = pow(f(x), 2) - 2f(x) + 3]] ([[-5 <= x <= 3]])이라 하자. 함수 [[h(x)]]가 [[x = k]]에서 최댓값 [[M]]을 가질 때, [[M - k]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔 정의를 cases로. 답 83 유지(f 치역 [-5,10], x=0에서 h=83)")

# 13. b6b4e691 — Pₙ(x) → app(sub(P,n), x), 줄임표 cdots
add(id="b6b4e691", qtype="short",
    question="자연수 [[n]]에 대하여 [[n]]차 다항식\n[[app(sub(P,n), x) = (x - 1)(x - 2)(x - 3) × cdots × (x - n)]]이라 할 때,\n[[3 pow(x,3) + 2 pow(x,2) - 5x + 2 = a + b app(sub(P,1), x) + c app(sub(P,2), x) + d app(sub(P,3), x)]]는 [[x]]에 대한\n항등식이다. 상수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a + b + c + d]]의\n값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="첨자 함수 Pₙ(x)를 app(sub(P,n), x)로, 줄임표는 cdots(곱 기호 ×로 연결). 답 47 유지(d=3, c=20, b=22, a=2)")

# 14. f412f176 — cases
add(id="f412f176", qtype="choice",
    question="최고차항의 계수가 [[a]] ([[a < 0]])인\n두 이차함수 [[f(x)]], [[g(x)]]에 대하여 [[f(3) = g(3)]]이다.\n함수 [[h(x)]]를 [[h(x) = cases(f(x), x <= 3, g(x), x > 3)]]이라 할 때,\n함수 [[h(x)]]가 다음 조건을 만족시킨다.\n(가) 함수 [[y = h(x)]]의 그래프와 직선 [[y = f(0)]]이 만나는 점의 [[x]]좌표는 0, 4, 12뿐이다.\n(나) 두 실수 [[alpha]], [[beta]] ([[alpha < 3 < beta]])에 대하여 함수 [[y = h(x)]]의 그래프와 직선 [[y = 2x - 8]]이 만나는 점의 [[x]]좌표는 [[alpha]], 3, [[beta]]이다.\n[[alpha + beta = 6]]일 때, [[h(-2) + h(5)]]의 값은?",
    choices=["[[15]]", "[[16]]", "[[17]]", "[[18]]", "[[19]]"],
    figure=None, confidence=0.85,
    note="[2025년 9월 고1 20번/4점]. 경우 나눔 정의를 cases로. 답 ③ 유지(a=-1, f(0)=7 → 17)")

# 15·16. edbc609a, 7dce5be6 — 사용자 정의 연산 ◎: v1.5에도 없음 → 보류 유지 (같은 이미지 id 2개)
dup(["edbc609a", "7dce5be6"], qtype="choice",
    question="실수 [[x]], [[y]]에 대하여 [[x]]◎[[y]]를 행렬 [[mat(2,2, -x, y, y, -x)]]라 할 때,\n다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. 임의의 실수 [[a]], [[b]]에 대하여 [[a]]◎[[b]] = [[b]]◎[[a]]\nㄴ. 임의의 실수 [[a]], [[b]], [[c]], [[d]]에 대하여\n([[a]]◎[[b]]) − ([[c]]◎[[d]]) = ([[a - c]])◎([[b - d]])\nㄷ. 임의의 실수 [[a]], [[b]], [[k]]에 대하여\n([[k a]])◎([[k b]]) = [[k]]([[a]]◎[[b]])",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.75,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 ◎ — v1.5에도 대응 표기 없음, 등식을 텍스트 혼합으로 유지",
    note="같은 이미지에 id 2개. 답 ④ 유지(ㄱ✗ ㄴ✓ ㄷ✓)")

# 17. fdedb1e0 — 첨자 점 라벨 선분 → seg(P1C), seg(CP2); 도형 unsupported → 통과
add(id="fdedb1e0", qtype="choice",
    question="그림과 같이 직선 위에 [[seg(AB) = 6]]인 두 점 A, B가 있다. 선분 AB 위의 점 C에 대하여 선분 AC의 중점을 [[sub(P,1)]], 선분 CB의 중점을 [[sub(P,2)]]라 하고 [[seg(P1C) = a]], [[seg(CP2) = b]]라 하자. 점 [[sub(P,1)]]을 중심으로 하고 반지름의 길이가 [[a + frac(1,2)]]인 반원 [[sub(O,1)]], 점 [[sub(P,2)]]를 중심으로 하고 반지름의 길이가 [[b + frac(1,2)]]인 반원 [[sub(O,2)]]를 각각 그린 후, 선분 [[sub(P,1)]][[sub(P,2)]]를 지름으로 하는 반원을 그린다. 두 반원 [[sub(O,1)]]과 [[sub(O,2)]]의 교점이 호 [[sub(P,1)]][[sub(P,2)]] 위에 있을 때, [[a b]]의 값은? (단, [[a < b]])",
    choices=["[[frac(5,4)]]", "[[frac(7,4)]]", "[[frac(9,4)]]", "[[frac(11,4)]]", "[[frac(13,4)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직선 위에 왼쪽부터 A, P₁, C, P₂, B(AB=6); P₁ 중심 반원 O₁, P₂ 중심 반원 O₂(더 큼), 선분 P₁P₂를 지름으로 하는 반원(가는 선); 세 반원이 한 점에서 만남"}}],
    confidence=0.8,
    note="[2018년 6월 고1 19번/4점]. 첨자 점 라벨 선분을 seg(P1C)·seg(CP2)로. 답 ② 유지(a+b=3, (a+1/2)²+(b+1/2)²=9 → ab=7/4)")

# 18. 667e05e5 — 동일 패턴
add(id="667e05e5", qtype="choice",
    question="그림과 같이 직선 위에 [[seg(AB) = 16]]인 두 점 A, B가 있다. 선분 AB 위의 점 C에 대하여 선분 AC의 중점을 [[sub(P,1)]], 선분 CB의 중점을 [[sub(P,2)]]라 하고 [[seg(P1C) = a]], [[seg(CP2) = b]]라 하자. 점 [[sub(P,1)]]을 중심으로 하고 반지름의 길이가 [[a + frac(3,2)]]인 반원 [[sub(O,1)]], 점 [[sub(P,2)]]를 중심으로 하고 반지름의 길이가 [[b + frac(3,2)]]인 반원 [[sub(O,2)]]를 각각 그린 후, 선분 [[sub(P,1)]][[sub(P,2)]]를 지름으로 하는 반원을 그린다. 두 반원 [[sub(O,1)]]과 [[sub(O,2)]]의 교점이 호 [[sub(P,1)]][[sub(P,2)]] 위에 있을 때, [[a b]]의 값은? (단, [[a < b]])",
    choices=["[[12]]", "[[frac(51,4)]]", "[[frac(27,2)]]", "[[frac(57,4)]]", "[[15]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직선 위에 왼쪽부터 A, P₁, C, P₂, B(AB=16); P₁ 중심 반원 O₁, P₂ 중심 반원 O₂(더 큼), 선분 P₁P₂를 지름으로 하는 반원; 세 반원이 한 점에서 만남"}}],
    confidence=0.8,
    note="첨자 점 라벨 선분을 seg(P1C)·seg(CP2)로. 답 ④ 유지(a+b=8, a²+b²=71/2 → ab=57/4)")

# 19·20. 0dc6852b, 460e3796 — A_k(n) → app(sub(A,k), n), 조건제시법 setb (같은 이미지 id 2개)
dup(["0dc6852b", "460e3796"], qtype="choice",
    question="두 자연수 [[a]], [[b]]의 최소공배수를 [[L(a, b)]]라 하자. 집합 [[U]] = { [[x]] | [[x]]는 100 이하의 자연수 }의 부분집합 [[app(sub(A,k), n)]]을 [[app(sub(A,k), n) = setb(x, L(n, x) = k)]] ([[k]], [[n]]은 자연수)라 할 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[in(12, app(sub(A,24), 8))]]\nㄴ. [[app(sub(A,20), 2) = app(sub(A,20), 4)]]\nㄷ. 집합 [[app(sub(A,36), 12)]]의 모든 원소의 합은 63이다.",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="같은 이미지에 id 2개. 첨자 함수 A_k(n)을 app(sub(A,k), n)으로. 답 ③ 유지(ㄱ✓ ㄴ✗ ㄷ✓)")

# 21. e7798212 — D′은 단독 점 이름(텍스트), 도형 unsupported → 통과
add(id="e7798212", qtype="choice",
    question="한 변의 길이가 2인 정사각형 모양의 종이 ABCD가 있다. [[angle(ECD) = deg(30)]]인 변 AD 위의 점 E에 대하여 다음 그림과 같이 선분 CE를 기준으로 아래 부분의 종이를 접었을 때, 점 D′과 선분 AC 사이의 거리는?",
    choices=["[[frac(sqrt(6) + sqrt(2), 4)]]", "[[frac(sqrt(6) - sqrt(2), 2)]]", "[[frac(sqrt(3) + 1, 4)]]", "[[frac(sqrt(3) - 1, 2)]]", "[[frac(sqrt(2), 2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(B 왼쪽 위, A 오른쪽 위, C 왼쪽 아래, D 오른쪽 아래). E는 AD 위, CE를 접는 선으로 D가 D′(정사각형 내부)로 접힘. ∠ECD=30° 표시, 대각선 AC 점선, CD·DE 점선"}}],
    confidence=0.8,
    note="D′은 단독 점 이름이라 텍스트. 답 ② 유지(D′=(1,√3), 거리 (√6−√2)/2)")

# 22. 8f73411e — 빈칸 (나)가 분자·등식 안 → box(2)/box(1); 도형 unsupported → 통과
add(id="8f73411e", qtype="choice",
    question="좌표평면의 제1사분면에 있는 두 점 A, B와 원점 O에 대하여 삼각형 OAB의 무게중심 G의 좌표는 [[point(8, 4)]]이고, 점 B와 직선 OA 사이의 거리는 [[6 sqrt(2)]]이다.\n다음은 직선 OB의 기울기가 직선 OA의 기울기보다 클 때, 직선 OA의 기울기를 구하는 과정이다.\n선분 OA의 중점을 M이라 하자.\n점 G가 삼각형 OAB의 무게중심이므로\n[[ratio(seg(BG), seg(GM)) = ratio(2, 1)]]이고,\n점 B와 직선 OA 사이의 거리가 [[6 sqrt(2)]]이므로\n점 G와 직선 OA 사이의 거리는 (가) 이다.\n직선 OA의 기울기를 [[m]]이라 하면\n점 G와 직선 OA 사이의 거리는\n[[frac(box(2), sqrt(pow(m,2) + pow(-1,2)))]] 이고 (가) 와 같다.\n즉, [[box(2) = box(1) × sqrt(pow(m,2) + 1)]] 이다.\n양변을 제곱하여 [[m]]의 값을 구하면\n[[m]] = □ 또는 [[m]] = □ 이다.\n이때 직선 OG의 기울기가 [[frac(1, 2)]] 이므로\n직선 OA의 기울기는 (다) 이다.\n위의 (가), (다)에 알맞은 수를 각각 [[p]], [[q]]라 하고,\n(나)에 알맞은 식을 [[f(m)]]이라 할 때, [[frac(f(q), pow(p,2))]]의 값은?",
    choices=["[[frac(2, 7)]]", "[[frac(5, 14)]]", "[[frac(3, 7)]]", "[[frac(1, 2)]]", "[[frac(4, 7)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(풀이 상자 안): 원점 O, 제1사분면의 점 A(오른쪽 아래)·B(위쪽), 삼각형 OAB, 무게중심 G(8,4), 선분 OA의 중점 M, 선분 BM"}}],
    confidence=0.8,
    note="[2020년 3월 고2 18번/4점]. 식 안의 빈칸 (가)(나)를 box(1)/box(2)로(문장 속 (가)(다)는 텍스트, 원문 '·'는 ×). 답 ② 유지((가)=2√2, (나)=|8m−4|, (다)=1/7 → 5/14)")

# 23~26. 50e113ca, 0e0cc900, be0e75ee, bd557e09 — 답 기호 ㉢: 답 문법 범위 밖 → 보류 유지 (같은 이미지 id 4개)
dup(["50e113ca", "0e0cc900", "be0e75ee", "bd557e09"], qtype="short",
    question="다음은 원소나열법으로 표현된 집합을 조건제시법으로 나타낸 것이다. 보기 중에서 옳은 것을 있는 대로 고르시오.\n<보기>\n㉠ {전자레인지, 전화기, 화분, 침대, 이불} = { [[x]] | [[x]]는 전자제품 }\n㉡ [[set(1, 2, 3, 4)]] = { [[x]] | [[x]]는 자연수를 4로 나누었을 때, 나머지 }\n㉢ [[set(1, 3, 5, 7, 9)]] = { [[x]] | [[x]]는 10 이하의 홀수 }\n㉣ [[set(frac(1,2), frac(1,3))]] = {0과 1 사이의 분수}",
    choices=None, figure=None, confidence=0.75,
    needs_review="답 기호 ㉢이 답 문법(ㄱㄴㄷ·①~⑤) 범위 밖이라 answer 미기재(옳은 것은 ㉢뿐)",
    note="같은 이미지에 id 4개(문항 1개). 본문은 문법 안")

# 27. 87001f24 — σ 지원(v1.5) → 관계식 전체를 식으로
add(id="87001f24", qtype="choice",
    question="별에서 단위시간동안 방출되는 복사에너지의 양을 별의 광도라 한다. 별의 표면 온도를 [[T]], 별의 반지름의 길이를 [[R]], 별의 광도를 [[L]]이라 하면 다음과 같은 관계식이 성립한다고 한다.\n[[pow(T,2) = frac(1, R) sqrt(frac(L, 4 pi sigma))]]\n(단, [[sigma]]는 슈테판-볼츠만 상수이다.)\n두 별 A, B에 대하여 별 A의 표면 온도는 별 B의 표면 온도의 [[frac(1,2)]]배이고, 별 A의 반지름의 길이는 별 B의 반지름의 길이의 36배 일 때, 별 A의 광도는 별 B의 광도의 [[k]]배이다. [[k]]의 값은?",
    choices=["49", "64", "81", "100", "121"],
    figure=None, confidence=0.85,
    note="[2015년 11월 고1 16번/4점]. σ를 sigma로 써서 관계식을 한 식으로. 답 ③ 유지(L ∝ T⁴R² → 81)")

# 28. 7102f165 — cases, 치역 setb
add(id="7102f165", qtype="short",
    question="실수 전체의 집합에서 정의된 함수 [[f]]가\n[[f(x) = cases(frac(x + 5, x - 2), x > 3, sqrt(3 - x) + k, x <= 3)]]\n일 때, 함수 [[f]]는 다음 조건을 만족시킨다.\n(가) 함수 [[f]]의 치역은 [[setb(y, y > 1)]]이다.\n(나) 임의의 두 실수 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n[[f(p) f(-1) = 15]]일 때, 상수 [[p]]의 값을 구하시오.\n(단, [[k]]는 상수)",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔 정의를 cases로, 치역은 setb. 답 16 유지(k=8, f(-1)=10, f(p)=3/2)")

# 29. 273bbd0f — cases
add(id="273bbd0f", qtype="choice",
    question="함수 [[f(x) = cases(-pow(x - a, 2) + b, x <= a, -sqrt(x - a) + b, x > a)]]와 서로 다른 세 실수 [[alpha]], [[beta]], [[gamma]]가 다음 조건을 만족시킨다.\n(가) 방정식 [[(f(x) - alpha)(f(x) - beta) = 0]]을 만족시키는 실수 [[x]]의 값은 [[alpha]], [[beta]], [[gamma]]뿐이다.\n(나) [[f(alpha) = alpha]], [[f(beta) = beta]]\n[[alpha + beta + gamma = 15]]일 때, [[f(alpha + beta)]]의 값은? (단, [[a]], [[b]]는 상수이다.)",
    choices=["1", "2", "3", "4", "5"],
    figure=None, confidence=0.85,
    note="[2023년 3월 고2 20번/4점]. 경우 나눔 정의를 cases로(원문 중괄호 {f(x)−α}{f(x)−β}는 소괄호). 답 ③ 유지(a=5, f(9)=3)")

# 30. 78965e1f — cases + (f⁻¹∘f⁻¹)(a) → app(comp(inv(f), inv(f)), a)
add(id="78965e1f", qtype="choice",
    question="함수 [[f(x) = cases(-sqrt(x) + 1, x >= 1, sqrt(2 - x), x < 1)]]에 대하여 [[app(comp(inv(f), inv(f)), a) = 9]]를 만족하는 상수 [[a]]의 값은?",
    choices=["[[-1]]", "0", "1", "2", "3"],
    figure=None, confidence=0.85,
    note="경우 나눔 정의를 cases로, 합성 적용을 app으로. 답 ④ 유지(f⁻¹(a)=f(9)=-2 → a=f(-2)=2)")

# 31. 9935fe9a — 동일 패턴
add(id="9935fe9a", qtype="short",
    question="함수 [[f]]를 [[f(x) = cases(1 - sqrt(x), x >= 0, sqrt(1 - x), x < 0)]]으로 정의할 때, [[app(comp(inv(f), inv(f)), a) = 16]]을 만족시키는 상수 [[a]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔 정의를 cases로, 합성 적용을 app으로. 답 2 유지(f⁻¹(a)=f(16)=-3 → a=f(-3)=2)")

# 32. e62608af — (g∘f)(x) → app(comp(g, f), x), 줄임표 cdots
add(id="e62608af", qtype="choice",
    question="유리함수 [[y = frac(x - 5, 2n x - 240 n)]]의 그래프의 두 점근선 [[x = k]], [[y = f(n)]]과 이차함수 [[y = frac(1,2) pow(x,2) - frac(1,2)]] ([[x >= 0]])의 역함수 [[y = g(x)]]에 대하여 [[h(x) = app(comp(g, f), x)]]라 할 때, [[h(1) × h(2) × h(3) × cdots × h(k)]]의 값은?\n(단, [[n]]은 자연수이다.)",
    choices=["10", "11", "12", "13", "14"],
    figure=None, confidence=0.85,
    note="합성 적용을 app으로, 줄임표는 cdots. 답 ② 유지(k=120, h(n)=√((n+1)/n) → 곱 11)")

# 33. b7cb29e6 — 본문은 문법 안, 도형 unsupported → 통과
add(id="b7cb29e6", qtype="choice",
    question="그림과 같이 제1사분면에 있는 곡선 [[y = frac(2, x)]] 위의 서로 다른 두 점 [[A point(a, frac(2, a))]], [[B point(b, frac(2, b))]]에 대하여 직선 AB가 [[x]]축과 만나는 점을 C, 선분 AB의 중점을 D라 하자.\n<보기>에서 옳은 것만을 있는 대로 고른 것은? (단, [[a < b]]이고, O는 원점이다.)\n<보기>\nㄱ. 점 C의 [[x]]좌표는 [[a + b]]이다.\nㄴ. 두 직선 AB와 OD의 기울기의 합은 0이다.\nㄷ. [[seg(AB) = 2 seg(OA)]]일 때, [[angle(AOC) = frac(3,2) angle(AOD)]]이다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 제1사분면 곡선 y=2/x 위의 점 A(왼쪽 위), B(오른쪽 아래), 직선 AB와 x축의 교점 C, AB의 중점 D, 선분 OA·OD·OC"}}],
    confidence=0.8,
    note="[2014년 3월 고2 이과 18번/4점]. 본문·보기 모두 문법 안, 도형은 unsupported. 답 ⑤ 유지")

# 34. 129c5d91 — O′·F′ 단독 점 이름(텍스트), 도형 unsupported → 통과
add(id="129c5d91", qtype="choice",
    question="그림과 같이 한 변의 길이가 12인 정사각형 OABC 모양의 종이를 점 O가 원점에, 두 점 A, C가 각각 [[x]]축, [[y]]축 위에 있도록 좌표평면 위에 놓았다. 두 점 D, E는 각각 두 선분 OC, AB를 [[ratio(2, 1)]]로 내분하는 점이고, 선분 OA 위의 점 F에 대하여 [[seg(OF) = 5]]이다.\n선분 OC 위의 점 P와 선분 AB 위의 점 Q에 대하여 선분 PQ를 접는 선으로 하여 종이를 접었더니 점 O는 선분 BC 위의 점 O′으로, 점 F는 선분 DE 위의 점 F′으로 옮겨졌다. 이때 좌표평면에서 직선 PQ의 방정식은 [[y = m x + n]]이다. [[m + n]]의 값은?\n(단, [[m]], [[n]]은 상수이고, 종이의 두께는 고려하지 않는다.)",
    choices=["6", "[[frac(25,4)]]", "[[frac(13,2)]]", "[[frac(27,4)]]", "7"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 정사각형 OABC(O 원점, A x축 위, C y축 위), D(OC 위)·E(AB 위)와 점선 DE, F(OA 위, OF=5), 접는 선 PQ(P는 OC 위 D 바로 아래, Q는 AB 위 아래쪽), 접힌 뒤 O′(BC 위)·F′(DE 위), 접는 방향 화살표"}}],
    confidence=0.8,
    note="[2016년 3월 고2 문과 21번/4점]. O′·F′은 단독 점 이름이라 텍스트. 답 ⑤ 유지(O′(6,12), F′(9,8) → x+2y=15 → m+n=7)")

# 35. cf06cf26 — △PP₁P₂ → tri(PP1P2)
add(id="cf06cf26", qtype="choice",
    question="직선 [[y = frac(1,2) x]] 위의 점 [[P point(a, b)]]를 [[x]]축, [[y]]축에 대하여 각각 대칭이동한 점을 [[sub(P,1)]], [[sub(P,2)]]라 하자. [[tri(PP1P2)]]의 넓이가 4일 때, 두 양수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?",
    choices=["1", "2", "3", "4", "5"],
    figure=None, confidence=0.85,
    note="첨자 점 라벨 삼각형을 tri(PP1P2)로. 답 ③ 유지(2ab=4, b=a/2 → a=2, b=1)")

# 36. ad241856 — ⟨a, b⟩ 꺾쇠 기호 + 한글 조건의 경우 나눔 → cases 불가, 보류 유지
add(id="ad241856", qtype="choice",
    question="두 조건 [[a]], [[b]]에 대하여 <[[a]], [[b]]>를\n<[[a]], [[b]]> = 1 ([[a]]가 [[b]]이기 위한 충분조건), 0 ([[a]]가 [[b]]이기 위한 필요충분조건), [[-1]] ([[a]]가 [[b]]이기 위한 필요조건)\n으로 정의한다. 세 집합 [[A]], [[B]], [[X]]에 대하여 조건 [[p]], [[q]], [[r]]이 다음과 같을 때,\n[[p]]: [[subset(X, (inter(A, B)))]]\n[[q]]: [[subset(X, (union(A, B)))]]\n[[r]]: [[subset(X, A)]] 또는 [[subset(X, B)]]\n<[[p]], [[q]]> − 2<[[q]], [[r]]> − 3<[[r]], [[p]]>의 값은?",
    choices=["[[-6]]", "[[-4]]", "[[0]]", "[[4]]", "[[6]]"],
    figure=None, confidence=0.75,
    needs_review="문법 범위 밖: 사용자 정의 꺾쇠 기호 ⟨a, b⟩ 및 조건이 한글 문장인 경우 나눔(cases 불가) — 텍스트 혼합 유지",
    note="[2007년 6월 고1 7번]. 원문의 괄호 (A∩B), (A∪B) 반영. 답 ⑤ 유지(1+2+3=6)")

# 37. 4109eceb — 집합 기호 P[x](대괄호) 정의: v1.5에도 없음 → 보류 유지
add(id="4109eceb", qtype="short",
    question="집합 [[P]]에 대하여 P[x]를\n(1) [[in(x, P)]]이면 P[x] = [[set(-x + 1, 0, x - 1)]]\n(2) [[notin(x, P)]]이면 P[x] = [[set(1, x, pow(x,2))]]이라고 정의한다.\n두 집합 [[A]] = { [[x]] | [[x]]는 소수인 자연수 },\n[[B]] = { [[3x - 1]] | [[x]]는 자연수 }일 때, 집합\n([[A - B]])[2] ∪ ([[B - A]])[8]의 원소의 총합을 구하시오.",
    choices=None, figure=None, confidence=0.75,
    needs_review="문법 범위 밖: 사용자 정의 집합 기호 P[x](대괄호) — v1.5에도 대응 표기 없음, 텍스트 혼합 유지",
    note="답 7 유지((A−B)[2]={1,2,4}, (B−A)[8]={−7,0,7})")

# 38. 8930c983 — f(p, q) 경우 나눔의 조건이 한글(참/거짓) → cases 불가, 보류 유지
add(id="8930c983", qtype="short",
    question="두 조건 [[p]], [[q]]에 대하여 [[f(p, q)]]를 다음과 같이 정의하자.\n[[f(p, q)]] = 1 ([[imp(p, q)]]가 참), [[-1]] ([[imp(p, q)]]가 거짓)\n실수 전체의 집합에서 정의된 세 조건 [[p]], [[q]], [[r]]가 다음과\n같을 때, [[f(p, neg(q)) + 2 × f(q, r) + 3 × f(neg(r), p)]]의\n값을 구하시오.\n[[p]]: [[x]]는 4의 배수가 아니다.\n[[q]]: [[pow(x,2)]]은 4의 배수가 아니다.\n[[r]]: [[sqrt(x)]] 는 4의 배수가 아니다.",
    choices=None, figure=None, confidence=0.75,
    needs_review="경우 나눔 정의의 조건이 한글 문장(p→q가 참/거짓)이라 cases로 쓸 수 없음 — 텍스트 혼합 유지",
    note="답 -2 유지(−1+2−3)")

# 39. d149ceed — 동일 패턴
add(id="d149ceed", qtype="short",
    question="두 조건 [[p]], [[q]]에 대하여 [[f(p, q)]]를 다음과 같이 정의하자.\n[[f(p, q)]] = 1 ([[imp(p, q)]]가 참), [[-1]] ([[imp(p, q)]]가 거짓)\n실수 전체의 집합에서 정의된 세 조건 [[p]], [[q]], [[r]]가 다음과\n같을 때, [[f(p, neg(q)) + 2 × f(neg(q), neg(r)) + 3 × f(r, p)]]의\n값을 구하시오.\n[[p]]: [[x]]는 3의 배수이다.\n[[q]]: [[pow(x,3)]]은 3의 배수이다.\n[[r]]: [[sqrt(x)]] 는 3의 배수이다.",
    choices=None, figure=None, confidence=0.75,
    needs_review="경우 나눔 정의의 조건이 한글 문장(p→q가 참/거짓)이라 cases로 쓸 수 없음 — 텍스트 혼합 유지",
    note="답 4 유지(−1+2+3)")
