# -*- coding: utf-8 -*-
# batch02 (72문항: h1-2 6of7·7of7 보류분 + h2-1 opus/sonnet 보류분) — v1.5 문법 재작업
# 핵심 교체: (f∘g)(x)→app(comp(f,g), x) / fⁿ(x)→iter(f, n, x) (인자 없는 fⁿ 정의는 pow(f,n) 유지, (f∘fⁿ)(x)→app(comp(f, pow(f,n)), x))
#            조각적 정의→cases(식, 조건, …) / 첨자 라벨 선분·각→seg(P1Q1)·angle(O1O2O3) / α(t)→alpha(t) / 줄임표→cdots / 빈칸→box(n)
# 도형(대응 그림·그래프·좌표평면)은 unsupported(raw) 유지 — 도형만 남은 항목은 통과.
# 여전히 보류: 한글 조건의 경우 나눔(4의 배수/무리수/홀짝), 한 이미지에 별개 문항, 이미지 하단 잘림, 선지가 그래프 그림.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= esc_sonnet_h1-2_6of7 — 함수의 합성 =================
# 0. 958c43ec — p10: (f∘f∘f)(0)+(f∘f)(0) → app. 대응 그림 unsupported → 통과
add(id="958c43ec", qtype="choice",
    question="함수 [[f]]: [[X]]→[[X]]가 다음 그림과 같을 때,\n[[app(comp(comp(f, f), f), 0) + app(comp(f, f), 0)]]의 값은?",
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→X, X={-1, 0, 1}. 화살표 -1→0, 0→1, 1→-1"}}],
    confidence=0.85,
    note="합성 적용을 app으로. 대응 그림은 unsupported(raw). 답 ② 유지(f(f(f(0)))=0, f(f(0))=−1 → −1)")

# 1. 7844d5cd — p11: (f∘g)(6) → app
add(id="7844d5cd", qtype="short",
    question="두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[Z]]가 다음 그림과 같을 때, [[app(comp(f, g), 6)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 2개. f: X={1,3,5,7}→Y={2,4,6,8}: 1→4, 3→6, 5→2, 7→8. g: Y={2,4,6,8}→Z={1,3,5,7}: 2→1, 4→7, 6→5, 8→3"}}],
    confidence=0.85,
    note="합성 적용을 app으로. 대응 그림 unsupported(raw). 답 2 유지(g(6)=5, f(5)=2)")

# 2. dec2e6fa — p12: (g∘f)(7) → app
add(id="dec2e6fa", qtype="short",
    question="두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[X]]가 다음 그림과 같을 때,\n[[app(comp(g, f), 7)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 2개. f: X={1,3,5,7}→Y={x,y,z,w}: 1→z, 3→w, 5→x, 7→y. g: Y→X={1,3,5,7}: x→5, y→7, z→3, w→5 (1은 대응 없음)"}}],
    confidence=0.85,
    note="합성 적용을 app으로. 대응 그림 unsupported(raw). 답 7 유지(f(7)=y, g(y)=7)")

# 3. 9aff9aab — p13: (f∘g)(5) → app
add(id="9aff9aab", qtype="short",
    question="두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[X]]가 다음 그림과 같을 때,\n[[app(comp(f, g), 5)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 2개. f: X={1,2,3,4}→Y={5,6,7,8}: 1→6, 2→7, 3→5, 4→8. g: Y={5,6,7,8}→X={1,2,3,4}: 5→4, 6→3, 7→2, 8→1"}}],
    confidence=0.85,
    note="합성 적용을 app으로. 대응 그림 unsupported(raw). 답 8 유지(g(5)=4, f(4)=8; 빠른정답 2와 불일치는 초안대로)")

# 4. f761c03b — p14: (g∘f)(2) → app
add(id="f761c03b", qtype="short",
    question="두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[X]]가 다음 그림과 같을 때,\n[[app(comp(g, f), 2)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 2개. f: X={2,3,5,7}→Y={p,q,r,s}: 2→q, 3→s, 5→q, 7→q. g: Y={p,q,r,s}→X={2,3,5,7}: p→7, q→3, r→3, s→2"}}],
    confidence=0.85,
    note="합성 적용을 app으로. 대응 그림 unsupported(raw). 답 3 유지(f(2)=q, g(q)=3)")

# 5~7. 49b676f9 / 30dd13bc / 0588e1da — p15(한 이미지에 id 3개): (f∘f)(x)=x, (f∘f∘f)(x)=x → app
dup(["49b676f9", "30dd13bc", "0588e1da"], qtype="choice",
    question="집합 [[X = set(1, 2, 3, 4, 5, 6)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 있다. 함수 [[f]]가 일대일대응일 때,\n보기 중에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(1) × f(2) × f(3) = 10]]이면\n[[f(4) + f(5) + f(6) = 13]]이다.\nㄴ. 집합 [[X]]의 모든 원소 [[x]]에 대하여\n[[app(comp(f, f), x) = x]]이면 [[f(a) = a]]인\n집합 [[X]]의 원소 [[a]]가 존재한다.\nㄷ. 집합 [[X]]의 모든 원소 [[x]]에 대하여\n[[app(comp(comp(f, f), f), x) = x]]이면 [[f(b) = b]]인\n집합 [[X]]의 원소 [[b]]가 존재한다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2017년 3월 고2 문과 20번 변형]. 합성 적용을 app으로. 한 이미지에 id 3개 → 동일 전사. 답 ① 유지(ㄴ: 2-순환 3개, ㄷ: 3-순환 2개가 반례)")

# 8. 305abdee — p19: (f∘g)(x)=(g∘f)(x) → app
add(id="305abdee", qtype="choice",
    question="두 함수 [[f(x) = x + a]], [[g(x) = pow(x,2) - 1]]일 때, 모든 실수 [[x]]에 대하여 [[app(comp(f, g), x) = app(comp(g, f), x)]]가 성립하도록 실수 [[a]]의 값을 정하면?",
    choices=["[[0]]", "[[-1]]", "[[-2]]", "[[1]]", "[[4]]"],
    figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 ① 유지(x²−1+a=(x+a)²−1 → a=0)")

# 9. a3ca14db — p25: 텍스트 혼합 없음(f∘g=g∘f는 comp 등식). 대응 그림만 unsupported → 통과
add(id="a3ca14db", qtype="short",
    question="집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여\n두 함수 [[f]]: [[X]]→[[X]], [[g]]: [[X]]→[[X]]가 있다. 함수 [[f]]가 다음 그림과 같이 정의되고 두 함수 [[f]], [[g]]가 [[comp(f, g) = comp(g, f)]]를 만족한다. [[g(1) = 5]]일 때, [[g(3)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→X, X={1,2,3,4,5}. 화살표 1→3, 2→4, 3→5, 4→1, 5→2"}}],
    confidence=0.85,
    note="문법 문제 없음(대응 그림만 unsupported). 답 2 유지(g(3)=g(f(1))=f(g(1))=f(5)=2)")

# 10. aa7c1652 — p26: 대응 그림만 unsupported → 통과
add(id="aa7c1652", qtype="choice",
    question="집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여\n함수 [[f]] : [[X]] → [[X]] 가 아래 그림과 같고,\n[[g]] : [[X]] → [[X]] 가 [[g(1) = 3]], [[comp(f, g) = comp(g, f)]] 를\n만족할 때, [[g(5)]] 의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→X, X={1,2,3,4,5}. 화살표 1→2, 2→3, 3→4, 4→5, 5→1"}}],
    confidence=0.85,
    note="문법 문제 없음(대응 그림만 unsupported). 답 ② 유지(g(k+1)=f(g(k)) → g(5)=2)")

# 11. a4b62373 — p27: 대응 그림만 unsupported → 통과
add(id="a4b62373", qtype="choice",
    question="함수 [[f]]: [[X]]→[[Y]]가 다음 그림과 같고, 함수 [[g]]: [[X]]→[[Y]]가\n[[g(1) = 2]], [[comp(f, g) = comp(g, f)]]를 만족할 때, [[g(1) - g(3)]]의\n값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→Y, X={0,1,2,3}, Y={0,1,2,3}. 화살표 0→2, 1→3, 2→0, 3→1"}}],
    confidence=0.85,
    note="문법 문제 없음(대응 그림만 unsupported). 답 ② 유지(g(3)=f(g(1))=f(2)=0 → 2)")

# 12. 0c07e597 — p31: (f∘f)(a) → app, 빈칸 (가)(나)(다) → box(1)(2)(3). 이름 없는 빈 상자 2개는 텍스트 □ 유지
add(id="0c07e597", qtype="choice",
    question="그림과 같이 한 변의 길이가 1인 정육각형 ABCDEF가 있다. 점 P는 점 A에서 출발하여 점 F까지 화살표 방향으로 정육각형 ABCDEF의 변을 따라 움직인다. 점 P가 점 A로부터 움직인 거리가 [[x]] ([[0 < x < 5]])일 때, 삼각형 PFA의 넓이를 [[f(x)]]라 하자. 다음은 함수 [[f(x)]]에 대하여 [[app(comp(f, f), a) = frac(9, 32)]]인 모든 실수 [[a]]의 값의 곱을 구하는 과정이다.\n[[app(comp(f, f), a) = f(f(a)) = frac(9, 32)]]에서\n[[f(a) = b]]라 하면 [[f(b) = frac(9, 32)]]이고,\n함수 [[f(x)]]의 최댓값은 [[box(1)]] 이므로\n[[0 < b <= box(1)]] 이다.\n점 P가 점 A로부터 움직인 거리가 [[b]]인 점을 Q라 하면 삼각형 QFA의 넓이는 [[frac(9, 32)]]이다.\n점 Q에서 직선 FA에 내린 수선의 발을 H라 하면\n[[seg(QH) = frac(9, 16)]]이므로 [[b = box(2)]] 이다.\n같은 방법으로 [[f(a) = box(2)]] 를 만족시키는\n[[a]] ([[0 < a < 5]])의 값을 구하면\n[[a]] = □ 또는 [[a]] = □ 이다.\n따라서 [[app(comp(f, f), a) = frac(9, 32)]]를 만족시키는\n모든 실수 [[a]]의 값의 곱은 [[box(3)]] 이다.\n위의 (가), (나), (다)에 알맞은 수를 각각 [[p]], [[q]], [[r]]라 할 때,\n[[frac(r, p q)]]의 값은?",
    choices=["[[frac(26, 3)]]", "[[frac(28, 3)]]", "[[10]]", "[[frac(32, 3)]]", "[[frac(34, 3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "정육각형 ABCDEF(A 오른쪽 아래, B 오른쪽, C 오른쪽 위, D 왼쪽 위, E 왼쪽, F 왼쪽 아래), 변을 따라 A→B→C→D→E→F 방향 화살표, 변 BC 위의 점 P, 삼각형 PFA 음영, FA=1 표시"}}],
    confidence=0.85,
    note="[2022년 3월 고2 21번/4점]. 합성 적용을 app으로, 빈칸 (가)(나)(다)를 box(1)(2)(3)으로(이름 없는 빈 상자 2개는 텍스트 □). 답 ② 유지((가)=√3/2, (나)=3√3/8, (다)=21/4 → 28/3)")

# 13. c0d842a8 — p33: 위 문항의 변형(한 변 2)
add(id="c0d842a8", qtype="choice",
    question="아래 그림과 같이 한 변의 길이가 2인\n정육각형 ABCDEF가 있다. 점 P는 점 A에서 출발하여 점 F까지 화살표 방향으로 정육각형 ABCDEF의 변을 따라 움직인다. 점 P가 점 A로부터 움직인 거리가\n[[x]] ([[0 < x < 10]])일 때, 삼각형 PFA의 넓이를 [[f(x)]]라 하자.\n다음은 함수 [[f(x)]]에 대하여 [[app(comp(f, f), a) = frac(27, 16)]]인 모든\n실수 [[a]]의 값의 곱을 구하는 과정이다.\n[[app(comp(f, f), a) = f(f(a)) = frac(27, 16)]]에서\n[[f(a) = b]]라 하면 [[f(b) = frac(27, 16)]]이고,\n함수 [[f(x)]]의 최댓값은 [[box(1)]] 이므로\n[[0 < b <= box(1)]] 이다.\n점 P가 점 A로부터 움직인 거리가 [[b]]인 점을 Q라 하면 삼각형 QFA의 넓이는 [[frac(27, 16)]]이다.\n점 Q에서 직선 FA에 내린 수선의 발을 H라 하면\n[[seg(QH) = frac(27, 16)]]이므로 [[b = box(2)]] 이다.\n같은 방법으로 [[f(a) = box(2)]] 를 만족시키는\n[[a]] ([[0 < a < 10]])의 값을 구하면\n[[a]] = □ 또는 [[a]] = □ 이다.\n따라서 [[app(comp(f, f), a) = frac(27, 16)]]을 만족시키는\n모든 실수 [[a]]의 값의 곱은 [[box(3)]] 이다.\n위의 (가), (나), (다)에 알맞은 수를 각각 [[p]], [[q]], [[r]]라 할 때,\n[[frac(r, p q)]]의 값은?",
    choices=["[[frac(7, 3)]]", "[[frac(29, 12)]]", "[[frac(5, 2)]]", "[[frac(31, 12)]]", "[[frac(8, 3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "정육각형 ABCDEF(A 오른쪽 아래, B 오른쪽, C 오른쪽 위, D 왼쪽 위, E 왼쪽, F 왼쪽 아래), 변을 따라 A→B→C→D→E→F 방향 화살표, 변 BC 위의 점 P, 삼각형 PFA 음영, FA=2 표시"}}],
    confidence=0.85,
    note="[2022년 3월 고2 21번 변형]. 합성 적용을 app으로, 빈칸을 box로. 답 ④ 유지((가)=2√3, (나)=9√3/8, (다)=(9/4)(31/4)=279/16 → 31/12 재확인)")

# 14. c01c58f0 — p48: (h∘g)(x), (h∘g∘f)(x) → app
add(id="c01c58f0", qtype="short",
    question="세 함수 [[f]], [[g]], [[h]]에 대하여\n[[app(comp(h, g), x) = -x + 7]], [[app(comp(comp(h, g), f), x) = frac(1, 3) x + 5]]일 때,\n[[f(12)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로((h∘g∘f)는 comp(comp(h,g),f)). 답 −2 유지(−f(x)+7=x/3+5 → f(12)=−2)")

# 15. dfdf912e — p51: (f∘g)(x)=h(x) → app
add(id="dfdf912e", qtype="short",
    question="세 함수 [[f(x)]], [[g(x) = frac(3x + 1, 2)]], [[h(x) = 9x + 1]]에\n대하여 [[app(comp(f, g), x) = h(x)]]일 때, [[f(1)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 4 유지(g(1/3)=1 → f(1)=h(1/3)=4)")

# 16. 6c774c25 — p56: f²⁰⁰⁶(2) → iter (정의 f¹=f, fⁿ⁺¹=f∘fⁿ은 pow(f,n) 등식 유지)
add(id="6c774c25", qtype="choice",
    question="실수 전체의 집합 [[R]]에서 [[R]]로의 함수 [[f]]가\n[[f]]: [[x]]→[[x + 1]]로 주어질 때, [[iter(f, 2006, 2)]]의 값은 얼마인가?\n(단, [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]], [[n]]은 자연수)",
    choices=["[[2002]]", "[[2004]]", "[[2006]]", "[[2008]]", "[[2010]]"],
    figure=None, confidence=0.85,
    note="거듭 합성 적용을 iter로(인자 없는 fⁿ 정의는 pow(f,n) 유지). 답 ④ 유지(2+2006=2008)")

# 17. 5a48301e — p58: f⁵⁰(−1/2) → iter. 그래프 unsupported → 통과
add(id="5a48301e", qtype="short",
    question="[[-1 <= x <= 1]]에서 정의된 함수 [[y = f(x)]]의 그래프가\n다음 그림과 같고\n[[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]] = 1, 2, 3, ⋯)일 때,\n[[iter(f, 50, -frac(1, 2))]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: 점 (-1, 1) 검은 점, -1<x≤0에서 y=-1 (x=-1 흰 점, x=0 검은 점), 0<x≤1에서 y=0 (x=0 흰 점, x=1 검은 점); 점선으로 (-1,1)에서 축까지 표시"}}],
    confidence=0.85,
    note="거듭 합성 적용을 iter로. 그래프 unsupported(raw). 답 1 유지(−1/2→−1→1→0→−1 … 주기 3)")

# 18. 39f7495d — p59: f¹⁰⁰(1/3) → iter
add(id="39f7495d", qtype="short",
    question="[[0 < x <= 3]]에서 정의된\n함수 [[y = f(x)]]의 그래프가 다음 그림과 같고\n[[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]] = 1, 2, 3, ⋯ )일 때,\n[[iter(f, 100, frac(1, 3))]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: 0<x≤1에서 y=2 (x=0 흰 점, x=1 검은 점), 1<x≤2에서 y=3 (x=1 흰 점, x=2 검은 점), 2<x≤3에서 y=1 (x=2 흰 점, x=3 검은 점); 눈금 1,2,3"}}],
    confidence=0.85,
    note="거듭 합성 적용을 iter로. 그래프 unsupported(raw). 답 2 유지(1/3→2→3→1→2 … 주기 3)")

# 19. 272c8366 — p60: f¹(x)=f(x), fⁿ⁺¹(x)=f(fⁿ(x)), f¹⁰⁰(3)−f²⁰⁰(1) → iter
add(id="272c8366", qtype="choice",
    question="집합 [[X = set(1, 2, 3)]]에 대하여 함수 [[f]]: [[X]]→[[X]]를\n다음과 같이 정의한다.\n[[iter(f, 1, x) = f(x)]], [[iter(f, n + 1, x) = f(iter(f, n, x))]]\n([[n]] = 1, 2, 3, ⋯)라고 할 때, [[iter(f, 100, 3) - iter(f, 200, 1)]]의\n값은?",
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→X, X={1,2,3}. 화살표 1→2, 2→3, 3→1"}}],
    confidence=0.85,
    note="거듭 합성 적용을 iter로. 대응 그림 unsupported(raw). 답 ① 유지(3-순환: f¹⁰⁰(3)=1, f²⁰⁰(1)=3 → −2)")

# 20. 9c40ac48 — p62: fᵏ(4)=1024 → iter
add(id="9c40ac48", qtype="choice",
    question="함수 [[f(x) = 2x]]에 대하여\n[[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]] = 1, 2, 3, ⋯)\n일 때, [[iter(f, k, 4) = 1024]]를 만족시키는 자연수 [[k]]의 값은?",
    choices=["[[7]]", "[[8]]", "[[9]]", "[[10]]", "[[11]]"],
    figure=None, confidence=0.85,
    note="거듭 합성 적용을 iter로. 답 ② 유지(2ᵏ·4=2¹⁰ → k=8)")

# 21. ec33cbb7 — p63: fⁿ(100)=0 → iter. 경우 나눔 조건이 한글 문장(4의 배수) → 여전히 보류
add(id="ec33cbb7", qtype="choice",
    question="자연수 전체의 집합에서 정의된 함수 [[f(x)]]가\n[[f(x)]] = { [[frac(x, 4) + 5]] ([[x]]는 4의 배수이다.) ; [[x - 5]] ([[x]]는 4의 배수가 아니다.) }\n이고 [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(pow(f, n), f)]]로 정의할 때,\n[[iter(f, n, 100) = 0]]을 만족시키는 자연수 [[n]]의 값은?",
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    figure=None, confidence=0.75,
    needs_review="경우 나눔 정의의 조건이 한글 문장(x는 4의 배수이다/아니다)이라 cases로 쓸 수 없음 — 텍스트 혼합 유지",
    note="거듭 합성 적용 fⁿ(100)은 iter로 교체. 답 ③ 유지(100→30→25→20→10→5→0, n=6)")

# 22. c7193146 — p64: 경우 나눔 → cases, fⁿ(x) → iter
add(id="c7193146", qtype="choice",
    question="집합 [[A = set(1, 2, 3, 4, 5)]]에 대하여 함수 [[f]]: [[A]]→[[A]]를\n[[f(x) = cases(x - 1, x >= 2, 5, x = 1)]]로 정의하자.\n[[iter(f, 1, x) = f(x)]], [[iter(f, n + 1, x) = f(iter(f, n, x))]] ([[n]] = 1, 2, 3, ⋯)\n라 할 때, [[iter(f, 2020, 2) + iter(f, 2023, 4)]]의 값은?",
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 거듭 합성 적용을 iter로. 답 ① 유지(5-순환: f²⁰²⁰(2)=2, f²⁰²³(4)=1)")

# 23. f8f7b689 — p67: fⁿ(x)=(f∘f∘⋯∘f)(x) → iter = app(comp(…cdots…)), 줄임표 합 → cdots. 그래프 unsupported → 통과
add(id="f8f7b689", qtype="choice",
    question="[[R = setb(x, 0 <= x <= 1)]]이라 할 때, [[R]]에서 [[R]]로의 함수 [[y = f(x)]] 의 그래프가 다음 그림과 같다.(단, [[iter(f, n, x) = app(comp(comp(comp(f, f), cdots), f), x)]] : [[f]] 개수 [[n]]개)\n<그래프>\n이 때, [[f(frac(1, 4)) + iter(f, 2, frac(1, 4)) + iter(f, 3, frac(1, 4)) + cdots + iter(f, 99, frac(1, 4))]] 의\n값을 구하면? (단, [[f(frac(1, 4)) = frac(1, 2)]], [[f(frac(1, 2)) = frac(3, 4)]], [[f(frac(3, 4)) = frac(1, 4)]] )",
    choices=["[[frac(99, 2)]]", "[[frac(95, 2)]]", "[[frac(93, 2)]]", "[[frac(91, 2)]]", "[[frac(89, 2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 f(x)의 그래프(0≤x≤1): 원점에서 출발해 (1/4, 1/2)를 지나 (1/2, 3/4)에서 극대, (3/4, 1/4)에서 극소, (1, 1)까지 올라가는 곡선; 축 눈금 1/4, 1/2, 3/4, 1과 점선 격자"}}],
    confidence=0.85,
    note="fⁿ(x) 정의를 iter = app(comp(…∘cdots∘f), x)로, 줄임표 합을 cdots로. 그래프 unsupported(raw). 답 ① 유지(주기 3, 33주기×3/2=99/2)")

# 24. 3725851e — p69: fⁿ 적용 → iter. 경우 나눔 조건이 한글(무리수/유리수) → 여전히 보류
add(id="3725851e", qtype="short",
    question="양의 실수 [[x]]에 대하여 함수\n[[f(x)]] = { [[pow(x, 4)]] ([[x]]는 무리수) ; [[sqrt(x)]] ([[x]]는 유리수) }\n라 하자. [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]]은 자연수)라 할 때,\n[[iter(f, 3n - 2, 1) + iter(f, 3n - 1, sqrt(2)) + iter(f, 3n, 3)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.75,
    needs_review="경우 나눔 정의의 조건이 한글 문장(x는 무리수/유리수)이라 cases로 쓸 수 없음 — 텍스트 혼합 유지",
    note="거듭 합성 적용을 iter로 교체. 답 6 유지(1+2+3)")

# 25. f31d5d58 — p75: 3구간·2구간 경우 나눔 → cases, (f∘g)(x) → app
add(id="f31d5d58", qtype="choice",
    question="실수 전체의 집합에서 정의된 함수 [[f(x)]]가 다음 조건을 만족시킨다.\n(가) [[f(x) = cases(2, 0 <= x < 2, -2x + 6, 2 <= x < 3, 0, 3 <= x <= 4)]]\n(나) 모든 실수 [[x]]에 대하여\n[[f(-x) = f(x)]]이고, [[f(x) = f(x - 8)]]이다.\n실수 전체의 집합에서 정의된 함수\n[[g(x) = cases(frac(abs(x), x) + n, x != 0, n, x = 0)]]\n에 대하여 함수 [[app(comp(f, g), x)]]가 상수함수가 되도록 하는\n60 이하의 자연수 [[n]]의 개수는?",
    choices=["[[30]]", "[[32]]", "[[34]]", "[[36]]", "[[38]]"],
    figure=None, confidence=0.85,
    note="[2019년 6월 고3 문과 21번/4점]. 경우 나눔을 cases로, 합성 적용을 app으로. 답 ① 유지(f(n−1)=f(n)=f(n+1)인 n 30개)")

# 26. 902dd056 — p78: 경우 나눔 → cases
add(id="902dd056", qtype="short",
    question="두 함수 [[f(x) = x + 6]],\n[[g(x) = cases(-2x - 5, x < 0, pow(x, 2) - 6 a x - 5, x >= 0)]]에 대하여\n합성함수 [[comp(f, g)]]의 치역이 [[setb(y, y >= -35)]]일 때, 상수 [[a]]의\n값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 2 유지(g 최솟값 −41=−9a²−5, a>0)")

# 27. d476c238 — p82: 경우 나눔 → cases
add(id="d476c238", qtype="short",
    question="두 함수 [[f(x) = x + 10]],\n[[g(x) = cases(-3x - 7, x < 0, pow(x, 2) - 8 a x - 7, x >= 0)]]에 대하여\n합성함수 [[comp(f, g)]]의 치역이 [[setb(y, y >= -61)]]일 때, 상수 [[a]]의\n값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 2 유지(g 최솟값 −71=−16a²−7, a>0)")

# 28. d02a9b02 — p84: 경우 나눔 → cases, (g∘f)(x) → app
add(id="d02a9b02", qtype="short",
    question="두 함수\n[[f(x) = cases(pow(x, 2) + 4 a x + 5, x < 0, x + 5, x >= 0)]], [[g(x) = x + 4]]에\n대하여 합성함수 [[app(comp(g, f), x)]]의 치역이 [[setb(y, y >= 5)]]일 때,\n[[f(a)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 합성 적용을 app으로. 답 6 유지(f 최솟값 1=5−4a², a>0 → a=1, f(1)=6)")

# 29. 112ee041 — p93: (f∘f)(x)=kx−k+3 → app. 그래프 unsupported → 통과
add(id="112ee041", qtype="short",
    question="[[0 <= x <= 4]]에서 정의된 함수 [[y = f(x)]]의 그래프가\n다음 그림과 같을 때, 방정식 [[app(comp(f, f), x) = k x - k + 3]]의\n서로 다른 실근이 3개가 되도록 하는 실수 [[k]]의 값의 범위는\n[[a < k <= b]]이다. 이때 상수 [[a]], [[b]]에 대하여 [[b - a]]의 값을\n구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: 원점 O에서 (2,4)까지 올라간 뒤 (4,2)까지 내려가는 꺾은선; 눈금 2, 4와 점선 표시"}}],
    confidence=0.85,
    note="합성 적용을 app으로. 그래프 unsupported(raw). 답 4/3 유지(−1<k≤1/3)")

# ================= esc_sonnet_h1-2_6of7 — 선분의 내분 / 원과 직선 / 함수의 개념 =================
# 30. 34584a34 — 내분 p43: 빈칸 (가)~(마) → box(1)~(5)(식 안). 좌표평면 그림 unsupported → 통과
add(id="34584a34", qtype="choice",
    question="다음은 직사각형 ABCD와 임의의 점 P에 대하여\n[[pow(seg(AP), 2) + pow(seg(CP), 2) = pow(seg(BP), 2) + pow(seg(DP), 2)]]이 성립함을 보인 것이다.\n(가)~(마)에 들어갈 말 중 옳지 않은 것은?\n다음 그림과 같이 직사각형 ABCD의 한 점 B를 원점으로, BC를 [[x]]축 잡으면 [[A point(0, b)]], [[B point(0, 0)]], [[C point(a, 0)]], [[D point(a, b)]]로 놓을 수 있다.\n이때 점 P의 좌표를 [[P point(x, y)]]라고 하면\n[[pow(seg(AP), 2) + pow(seg(CP), 2)]]\n= [[box(1) + pow(x - a, 2) + pow(y, 2)]]\n= [[2 pow(x, 2) + 2 pow(y, 2) - 2 a x - 2 b y + box(2)]] ⋯ ㉠\n[[pow(seg(BP), 2) + pow(seg(DP), 2)]]\n= [[pow(x, 2) + pow(y, 2) + box(3)]]\n= [[2 pow(x, 2) + 2 pow(y, 2) + box(4) + pow(a, 2) + pow(b, 2)]] ⋯ ㉡\n㉠, ㉡로부터 [[pow(seg(AP), 2) + pow(seg(CP), 2) = box(5)]]",
    choices=["(가) : [[pow(x, 2) + pow(y + b, 2)]]", "(나) : [[pow(a, 2) + pow(b, 2)]]", "(다) : [[pow(x - a, 2) + pow(y - b, 2)]]", "(라) : [[-2 a x - 2 b y]]", "(마) : [[pow(seg(BP), 2) + pow(seg(DP), 2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 직사각형 ABCD(B(0,0) 원점, C(a,0), D(a,b), A(0,b)), 내부의 점 P(x,y), P에서 네 꼭짓점으로 선분"}}],
    confidence=0.85,
    note="빈칸 (가)~(마)를 box(1)~(5)로(식 안). 좌표평면 그림 unsupported(raw). 답 ① 유지((가)=x²+(y−b)²이므로 ①이 틀림)")

# 31. ea1aab30 — 내분 p45: 빈칸 → box. 좌표평면 그림 unsupported → 통과
add(id="ea1aab30", qtype="choice",
    question="다음은 직사각형 ABCD와 임의의 점 P에 대하여\n[[pow(seg(AP), 2) + pow(seg(CP), 2) = pow(seg(BP), 2) + pow(seg(DP), 2)]]이 성립함을 보인 것이다.\n다음 중 (가)~(마)에 들어갈 말로 옳지 않은 것은?\n다음 그림과 같이 직사각형 ABCD의 한 변 BC를 [[x]]축, [[seg(BC)]]의 수직이등분선을 [[y]]축으로 잡으면 [[A point(-a, b)]], [[B point(-a, 0)]], [[C point(a, 0)]], [[D point(a, b)]]로 놓을 수 있다.\n이때 점 P의 좌표를 [[P point(x, y)]]라 하면\n[[pow(seg(AP), 2) + pow(seg(CP), 2) = box(1) + box(2)]]\n= [[2(pow(x, 2) + pow(y, 2) + pow(a, 2) - b y) + pow(b, 2)]] ⋯ ㉠\n[[pow(seg(BP), 2) + pow(seg(DP), 2) = box(3) + box(4)]]\n= [[2(pow(x, 2) + pow(y, 2) + pow(a, 2) - b y) + pow(b, 2)]] ⋯ ㉡\n㉠, ㉡에 의하여 [[pow(seg(AP), 2) + pow(seg(CP), 2) = box(5)]]",
    choices=["(가): [[pow(x + a, 2) + pow(y + b, 2)]]", "(나): [[pow(x - a, 2) + pow(y, 2)]]", "(다): [[pow(x + a, 2) + pow(y, 2)]]", "(라): [[pow(x - a, 2) + pow(y - b, 2)]]", "(마): [[pow(seg(BP), 2) + pow(seg(DP), 2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 직사각형 ABCD(A(-a,b), B(-a,0), C(a,0), D(a,b)), y축이 BC의 수직이등분선, 내부의 점 P(x,y), P에서 네 꼭짓점으로 선분"}}],
    confidence=0.85,
    note="빈칸 (가)~(마)를 box(1)~(5)로(식 안). 좌표평면 그림 unsupported(raw). 답 ① 유지((가)=(x+a)²+(y−b)²이므로 ①이 틀림)")

# 32. d452d130 — 내분 p48: ((가))² → pow(box(1), 2). 삼각형 그림 unsupported → 통과
add(id="d452d130", qtype="choice",
    question="다음은 예각삼각형 ABC에서 변 BC의 중점을 M이라 할 때,\n[[pow(seg(AB), 2) + pow(seg(AC), 2) = 2(pow(seg(BM), 2) + pow(seg(AM), 2))]]\n이 성립함을 증명한 것이다.\n[증명]\n점 A에서 선분 BC에 내린 수선의 발을 H라 하자.\n직각삼각형 ABH에서\n[[pow(seg(AB), 2) = pow(seg(BH), 2) + pow(seg(AH), 2)]]\n= [[pow(box(1), 2) + pow(seg(AH), 2)]]\n= [[pow(seg(BM), 2) + 2 seg(BM) × seg(MH) + pow(box(2), 2)]] ⋯ ㉠\n직각삼각형 AHC에서\n[[pow(seg(AC), 2) = pow(seg(CH), 2) + pow(seg(AH), 2)]]\n= [[pow(box(3), 2) + pow(seg(AH), 2)]]\n= [[pow(seg(CM), 2) - 2 seg(CM) × seg(MH) + pow(box(2), 2)]] ⋯ ㉡\n㉠, ㉡에서\n[[pow(seg(AB), 2) + pow(seg(AC), 2) = 2(pow(seg(BM), 2) + pow(seg(AM), 2))]]이다.\n이 증명에서 (가), (나), (다)에 알맞은 것은?",
    choices=["(가) [[seg(BC) + seg(CH)]], (나) [[seg(AM)]], (다) [[seg(BH) - seg(BM)]]", "(가) [[seg(BC) + seg(CH)]], (나) [[seg(AH)]], (다) [[seg(BH) - seg(BM)]]", "(가) [[seg(BM) + seg(MH)]], (나) [[seg(AM)]], (다) [[seg(BH) - seg(BM)]]", "(가) [[seg(BM) + seg(MH)]], (나) [[seg(AH)]], (다) [[seg(CM) - seg(MH)]]", "(가) [[seg(BM) + seg(MH)]], (나) [[seg(AM)]], (다) [[seg(CM) - seg(MH)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "예각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 변 BC 위에 중점 M과 수선의 발 H(M이 H보다 B쪽), 선분 AM, AH(직각 표시)"}}],
    confidence=0.85,
    note="[2007년 11월 고1 11번]. 빈칸의 제곱 ((가))²를 pow(box(1), 2)로(곱점 ·은 ×). 선지의 (가)(나)(다) 표는 한 줄 나열. 답 ⑤ 유지((가)=BM+MH, (나)=AM, (다)=CM−MH)")

# 33. d336c96c — 내분 p62: 윗줄 BC₁, BC₂ → seg(BC1)·seg(BC2)
add(id="d336c96c", qtype="choice",
    question="두 점 [[A point(-3, -4)]], [[B point(5, 2)]]에 대하여 서로 다른 두\n점 [[sub(C,1)]], [[sub(C,2)]]가 다음 조건을 만족시킬 때, 삼각형 O[[sub(C,1)]][[sub(C,2)]]의\n넓이는? (단, O는 원점이고, 점 [[sub(C,1)]]의 [[x]]좌표는 점 [[sub(C,2)]]의\n[[x]]좌표보다 작다.)\n(가) 두 점 [[sub(C,1)]], [[sub(C,2)]]는 모두 직선 AB 위의 점이다.\n(나) [[seg(AB) = 3 seg(BC1)]], [[seg(AB) = 3 seg(BC2)]]",
    choices=["[[frac(13, 3)]]", "[[frac(14, 3)]]", "[[5]]", "[[frac(16, 3)]]", "[[frac(17, 3)]]"],
    figure=None, confidence=0.85,
    note="첨자 점 라벨 선분을 seg(BC1)·seg(BC2)로(단독 점 이름 C₁·C₂는 sub 텍스트). 답 ② 유지(C₁(7/3,0), C₂(23/3,4) → 14/3)")

# 34. e71f5480 — 원과 직선 p48: '선분 H₁H₂'는 윗줄 없음(텍스트 sub 유지, 파싱 통과). 그림만 unsupported → 통과
add(id="e71f5480", qtype="short",
    question="좌표평면 위에 두 원\n[[sub(C,1)]]: [[pow(x + 4, 2) + pow(y, 2) = 4]], [[sub(C,2)]]: [[pow(x - 4, 2) + pow(y, 2) = 1]]과\n두 원 [[sub(C,1)]], [[sub(C,2)]]와 서로 만나지 않는\n직선 [[l]]: [[y = a x]] ([[a > 0]])이 있다. 원 [[sub(C,1)]] 위의 점 P에서\n직선 [[l]]에 내린 수선의 발을 [[sub(H,1)]], 원 [[sub(C,2)]] 위의 점 Q에서\n직선 [[l]]에 내린 수선의 발을 [[sub(H,2)]]라 하자. 선분 [[sub(H,1)]][[sub(H,2)]]의\n길이의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, [[M m = 23]]인\n[[a]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: x축 음의 부분에 중심을 둔 큰 원 C₁(왼쪽), x축 양의 부분에 중심을 둔 작은 원 C₂(오른쪽), 원점을 지나는 직선 y=ax(기울기 양수)"}}],
    confidence=0.85,
    note="[2020년 9월 고1 27번 변형]. 이미지 확인: '선분 H₁H₂'에 윗줄 없음 → 단독 점 이름 텍스트 유지(파싱 통과), 그림만 unsupported. 답 1 유지(d=8/√(1+a²), d²−9=23 → a=1)")

# 35. cfdf6670 — 함수의 개념 p6: 선지 ⑤ 경우 나눔 → cases
add(id="cfdf6670", qtype="choice",
    question="두 집합 [[X = set(-1, 0, 1)]], [[Y = set(0, 1, 2, 3)]]에\n대하여 다음 대응 중 [[X]]에서 [[Y]]로의 함수가 아닌 것을\n모두 고르면?",
    choices=["[[x]] → [[abs(x) + 1]]", "[[x]] → [[x + 2]]", "[[x]] → [[pow(x, 3) + 3]]", "[[x]] → [[pow(x, 2) + x + 1]]", "[[x]] → [[cases(x - 1, x >= 0, -x - 1, x < 0)]]"],
    figure=None, confidence=0.85,
    note="선지 ⑤의 경우 나눔을 cases로. 답 '③, ⑤' 유지(③ x=1→4∉Y, ⑤ x=0→−1∉Y)")

# 36~37. 71c3475d / cbd91a53 — 함수의 개념 p55(한 이미지에 id 2개): h(x) 경우 나눔 → cases
dup(["71c3475d", "cbd91a53"], qtype="choice",
    question="두 실수 [[a]], [[b]]와 두 함수 [[f(x) = -pow(x, 2) - 4x + 4]],\n[[g(x) = pow(x, 2) - 4x - 4]]에 대하여 함수 [[h(x)]]를\n[[h(x) = cases(f(x), x < a, g(x + 2b), x >= a)]]라 하자. 함수 [[h(x)]]가\n실수 전체의 집합에서 실수 전체의 집합으로의\n일대일대응이 되도록 하는 [[a]], [[b]]의 모든 순서쌍 [[point(a, b)]]만을\n원소로 하는 집합을 [[A]]라 할 때, 다음 보기 중 옳은 것만을\n있는 대로 고른 것은?\n<보기>\nㄱ. [[in(point(-1, k), A)]]를 만족시키는 실수 [[k]]는 존재하지\n않는다.\nㄴ. [[in(point(-2, 4), A)]]\nㄷ. 집합 [[B]] = { [[m + b]] | [[in(point(m, b), A)]]이고 [[m]]은 정수 }\n에 대하여 [[in(frac(-1 + sqrt(15), 2), B)]]이다.",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로(집합 B의 한글 조건은 텍스트 혼합). 한 이미지에 id 2개 → 동일 전사. 답 ⑤ 유지")

# 38. 81050c19 — 함수의 개념 p61: h(x) 경우 나눔 → cases
add(id="81050c19", qtype="choice",
    question="두 실수 [[a]], [[b]]와 두 함수 [[f(x) = -pow(x, 2) - 4x - 2]],\n[[g(x) = pow(x, 2) - 4x + 2]]에 대하여 함수 [[h(x)]]를\n[[h(x) = cases(f(x), x < a, g(x + b), x >= a)]]라 하자.\n함수 [[h(x)]]가 실수 전체의 집합에서 실수 전체의\n집합으로의 일대일대응이 되도록 하는 [[a]], [[b]]의 모든 순서쌍\n[[point(a, b)]]만을 원소로 하는 집합을 [[A]]라 할 때, 다음 보기 중\n옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[in(point(-3, k), A)]]를 만족시키는 실수 [[k]]는 존재한다.\nㄴ. [[in(point(-2, 6), A)]]\nㄷ. 집합 { [[m b]] | [[in(point(m, b), A)]]이고 [[m]]은 정수 }의 모든\n원소 중 정수의 합은 [[-36]]이다.",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2022년 11월 고1 21번 변형]. 경우 나눔을 cases로(집합의 한글 조건은 텍스트 혼합). 답 ⑤ 유지")

# ================= esc_sonnet_h1-2_7of7 =================
# 39. 50c56465 — 함수의 개념 p63: 선지 ⑤ 경우 나눔 → cases
add(id="50c56465", qtype="choice",
    question="집합 [[X = set(-1, 0, 1)]]에 대하여 함수 [[f]]가 [[X]]에서 [[X]]로의 함수일 때, 다음 중 항등함수인 것은?",
    choices=["[[f(x) = abs(x)]]", "[[f(x) = pow(x,2)]]", "[[f(x) = -x]]", "[[f(x) = pow(x,3)]]", "[[f(x) = cases(sqrt(x), x >= 0, sqrt(-x), x < 0)]]"],
    figure=None, confidence=0.85,
    note="선지 ⑤의 경우 나눔을 cases로. 답 ④ 유지(x³=x on {−1,0,1})")

# 40. 0465605c — 함수의 개념 p97: f¹(x)=f(x), fⁿ⁺¹(x)=(f∘fⁿ)(x) → iter·app(comp(f, pow(f,n)), x), y=fⁿ(x) → iter
add(id="0465605c", qtype="short",
    question="함수 [[f(x) = -abs(x + 1) + 1]]에 대하여\n[[iter(f, 1, x) = f(x)]], [[iter(f, n + 1, x) = app(comp(f, pow(f, n)), x)]]\n([[n]] = 1, 2, 3, ⋯)\n으로 정의할 때, [[y = iter(f, n, x)]]의 그래프와 [[x]]축으로 둘러싸인 도형의 넓이는 [[a n + b]]이다. 이때 상수 [[a]], [[b]]에 대하여 [[pow(a,2) + pow(b,2)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="거듭 합성 적용을 iter로, (f∘fⁿ)(x)는 app(comp(f, pow(f,n)), x)로. 답 5 유지(넓이 2n−1 → a=2, b=−1)")

# 41. 13cc5969 — 평행이동 p46: 원 C′은 단독 이름 → 텍스트(prime(C) 제거)
add(id="13cc5969", qtype="short",
    question="두 양수 [[a]], [[b]]에 대하여 원 [[C]]: [[pow(x - 1, 2) + pow(y, 2) = pow(r, 2)]]을\n[[x]]축의 방향으로 [[a]]만큼, [[y]]축의 방향으로 [[b]]만큼 평행이동한\n원을 C′이라 할 때, 두 원 [[C]], C′이 다음 조건을 만족시킨다.\n(가) 원 C′은 원 [[C]]의 중심을 지난다.\n(나) 직선 [[4x - 3y + 21 = 0]]은 두 원 [[C]], C′에 모두\n접한다.\n[[a + b + r]]의 값을 구하시오. (단, [[r]]는 양수이다.)",
    choices=None, figure=None, confidence=0.85,
    note="[2022년 3월 고2 27번/4점]. 도함수 기호 prime(C)를 지우고 C′은 단독 점(원) 이름이라 텍스트로. 답 12 유지(r=5, a=3, b=4 재확인)")

# 42. ee519531 — 평행이동 p53: 원 C′ → 텍스트
add(id="ee519531", qtype="short",
    question="두 실수 [[a]], [[b]]에 대하여 원 [[C]]: [[pow(x - 2, 2) + pow(y, 2) = pow(r, 2)]]을\n[[x]]축의 방향으로 [[a]]만큼, [[y]]축의 방향으로 [[b]]만큼 평행이동한\n원을 C′이라 할 때, 두 원 [[C]], C′이 다음 조건을 만족시킨다.\n(가) 원 C′은 원 [[C]]의 중심을 지난다.\n(나) 직선 [[3x + 4y + 14 = 0]]은 두 원 [[C]], C′에 모두\n접한다.\n[[2a + b + r]]의 값을 구하시오. (단, [[a]], [[r]]는 양수이다.)",
    choices=None, figure=None, confidence=0.85,
    note="[2022년 3월 고2 27번 변형]. prime(C)를 지우고 C′은 텍스트로. 원문 '(단, a ,r는 양수이다.)' 띄어쓰기 보정 유지. 답 8 유지(r=4, a=16/5, b=−12/5 재확인)")

# ================= esc_opus_h2-1_1of1 =================
# 43. b7b42bcd — 삼각함수의 그래프 p83: α(t), β(t) → alpha(t)·beta(t); 조건제시법 → setb
add(id="b7b42bcd", qtype="choice",
    question="[[-1 <= t <= 1]]인 실수 [[t]]에 대하여\n[[x]]에 대한 방정식 [[(sin(frac(pi x, 2)) - t)(cos(frac(pi x, 2)) - t) = 0]]의\n실근 중에서 집합 [[setb(x, 0 <= x < 4)]]에 속하는 가장 작은 값을 [[alpha(t)]], 가장 큰 값을 [[beta(t)]]라 하자. <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[-1 <= t < 0]]인 모든 실수 [[t]]에 대하여 [[alpha(t) + beta(t) = 5]]이다.\nㄴ. [[setb(t, beta(t) - alpha(t) = beta(0) - alpha(0)) = setb(t, 0 <= t <= frac(sqrt(2), 2))]]\nㄷ. [[alpha(sub(t,1)) = alpha(sub(t,2))]]인 두 실수 [[sub(t,1)]], [[sub(t,2)]]에 대하여 [[sub(t,2) - sub(t,1) = frac(1,2)]] 이면 [[sub(t,1) sub(t,2) = frac(1,3)]] 이다.",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2021년 6월 고3 15번/4점]. 그리스 문자 함수 적용을 alpha(t)·beta(t)로, 집합은 setb로. 답 ② 유지(ㄷ: t₁t₂=3/8)")

# 44. 18ac8550 — 지수함수 p89: 경우 나눔 → cases
add(id="18ac8550", qtype="short",
    question="양의 실수 [[a]]에 대하여 함수 [[f(x)]]를\n[[f(x) = cases(pow(3, x) + pow(3, -a) - 2, x < a, pow(3, -x) + pow(3, a) - 2, x >= a)]]\n라 할 때, 함수 [[f(x)]]가 다음 조건을 만족시키도록 하는 [[a]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 하자.\n함수 [[y = abs(f(x))]]의 그래프와 직선 [[y = k]]가 서로 다른 두 점에서 만나도록 하는 양수 [[k]]는 오직 하나뿐이다.\n[[pow(9, M + m) = p + 4 sqrt(q)]] 일 때, [[p q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 자연수이다.)",
    choices=None, figure=None, confidence=0.8,
    note="[2022년 11월 고2 30번 변형]. 경우 나눔을 cases로. 답 12 유지(9^(M+m)=6+4√2)")

# 45. 7a3c7cd6 — 로그함수 p40: 경우 나눔 → cases ('또는' 집합은 텍스트 혼합)
add(id="7a3c7cd6", qtype="choice",
    question="함수 [[f(x) = cases(pow(3, x + 1), x <= 1, 9 - 3 log(3, x), x > 1)]]에 대하여\n다음 조건을 만족시키는 모든 양수 [[k]]의 값의 집합이\n{ [[k]] | [[0 < k <= alpha]] 또는 [[beta < k < gamma]] }일 때, [[alpha + beta + gamma]]의\n값은? (단, [[alpha]], [[beta]], [[gamma]]는 상수이다.)\n함수 [[y = abs(f(x) - k)]]의 그래프가\n두 직선 [[y = p]], [[y = 2p]]와 만나는 점의 개수가 각각\n3, 2가 되도록 하는 양수 [[p]]가 존재한다.",
    choices=["[[17]]", "[[18]]", "[[19]]", "[[20]]", "[[21]]"],
    figure=None, confidence=0.8,
    note="[2026년 6월 고2 21번 변형]. 경우 나눔을 cases로('또는' 조건의 집합은 텍스트 혼합). 답 미도출(초안 None 유지)")

# 46. 84f3ab83 — ∑ p20: 경우 나눔 → cases
add(id="84f3ab83", qtype="short",
    question="자연수 [[k]]에 대하여\n함수 [[f(x) = cases(-pow(x,2) + 16, x <= 4, k sqrt(x - 4), x > 4)]]일 때, 다음 조건을\n만족시키는 정사각형의 내부 또는 변 위에 있는\n곡선 [[y = f(x)]] 위의 점 [[point(x, y)]] 중 [[x]], [[y]]의 값이 모두\n정수인 점의 개수를 [[sub(a,n)]] ([[n]] = 1, 2, 3, ⋯)이라 하자.\n(가) 정사각형의 두 대각선의 교점의 좌표는\n[[point(n, f(n))]]이다.\n(나) 정사각형의 각 변은 [[x]]축 또는 [[y]]축에 평행하고\n한 변의 길이는 4이다.\n[[g(k) = sum(n, 1, 8, sub(a,n))]]이라 할 때, [[g(k) = 11]]을 만족시키는\n모든 [[k]]의 값의 합을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    note="경우 나눔을 cases로. 답 미도출(초안 None 유지, 빠른정답 3 미검증)")

# 47. e865ebd9 — ∑ p80: 3구간(첫 조건 'x<0 또는 x>4'는 구간 2개로 분리) → cases 4쌍, (f∘f)(x) → app. 그래프 unsupported → 통과
add(id="e865ebd9", qtype="short",
    question="함수 [[f(x)]]는\n[[f(x) = cases(x, x < 0, -2x + 4, 0 <= x < 2, x - 2, 2 <= x <= 4, x, x > 4)]]\n이고, 함수 [[y = f(x)]]의 그래프는 다음 그림과 같다.\n[[x]]에 대한 방정식 [[app(comp(f, f), x) + frac(1,2) f(x) = n]]의 서로\n다른 실근의 개수를 [[sub(a,n)]]이라 할 때, [[sum(n, 1, 10, sub(a,n))]]의 값을\n구하시오. (단, [[n]]은 자연수이다.)",
    choices=None, derived_answer="14",
    figure=[{"fn": "unsupported", "args": {"raw": "y=f(x) 그래프: x<0에서 y=x(원점 열린 점), (0,4)에서 (2,0)까지 내려가는 선분, (2,0)에서 (4,2)까지 선분(닫힌 점), x>4에서 y=x(점 (4,4) 열린 점); 점선으로 y=4, y=2, x=4 표시"}}],
    confidence=0.8,
    note="경우 나눔을 cases로(원문 'x (x<0 또는 x>4)'는 x<0과 x>4 두 쌍으로 분리), 합성 적용을 app으로. 답 새로 도출 14(구간별 g(x)=f(f(x))+f(x)/2 선형 분석·정확 계산: a₁..a₁₀=2,3,3,2,0,0,1,1,1,1) — 빠른정답 98과 불일치")

# 48. 02a189a7 — 사인·코사인 p36: ∠O₁O₂O₃·윗줄 O₁A·O₂A² → angle(O1O2O3)·seg(O1A)·pow(seg(O2A),2). 도형 unsupported → 통과
add(id="02a189a7", qtype="short",
    question="그림과 같이 넓이가 84이고, [[angle(O1O2O3) = deg(90)]]인\n직각삼각형 [[sub(O,1)]][[sub(O,2)]][[sub(O,3)]]가 있다. 중심이 [[sub(O,1)]]인 원 [[sub(C,1)]]과\n중심이 [[sub(O,2)]]인 원 [[sub(C,2)]]가 선분 [[sub(O,1)]][[sub(O,2)]] 위의 한 점에서 만나고,\n원 [[sub(C,2)]]와 중심이 [[sub(O,3)]]인 원 [[sub(C,3)]]이 선분 [[sub(O,2)]][[sub(O,3)]] 위의 한 점에서\n만난다. 두 원 [[sub(C,1)]], [[sub(C,3)]]이 선분 [[sub(O,1)]][[sub(O,3)]] 위의 한 점 A에서\n만나고, [[seg(O1A) = 21]]일 때 [[pow(seg(O2A), 2) = frac(q, p)]] 이다. [[p + q]]의 값을\n구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None, derived_answer="1258",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 C₁(중심 O₁)과 작은 두 원 C₂(중심 O₂)·C₃(중심 O₃)이 서로 외접, 직각삼각형 O₁O₂O₃(O₂에서 직각), 점 A는 O₁O₃ 위, 선분 O₁A 길이 21 표시"}}],
    confidence=0.8,
    note="첨자 점 라벨을 angle(O1O2O3)·seg(O1A)·seg(O2A)로(선분 O₁O₂ 등 윗줄 없는 것은 텍스트). 답 새로 도출 1258(반지름 21,3,4 → O₂A²=1233/25) — 빠른정답 없음")

# 49. ed49d2f5 — 사인·코사인 p37: 위 문항의 변형(넓이 60, O₁A=12)
add(id="ed49d2f5", qtype="short",
    question="그림과 같이 넓이가 60이고, [[angle(O1O2O3) = deg(90)]]인\n직각삼각형 [[sub(O,1)]][[sub(O,2)]][[sub(O,3)]]가 있다. 중심이 [[sub(O,1)]]인 원 [[sub(C,1)]]과\n중심이 [[sub(O,2)]]인 원 [[sub(C,2)]]가 선분 [[sub(O,1)]][[sub(O,2)]] 위의 한 점에서 만나고,\n원 [[sub(C,2)]]와 중심이 [[sub(O,3)]]인 원 [[sub(C,3)]]이 선분 [[sub(O,2)]][[sub(O,3)]] 위의 한 점에서\n만난다. 두 원 [[sub(C,1)]], [[sub(C,3)]]이 선분 [[sub(O,1)]][[sub(O,3)]] 위의 한 점 A에서\n만나고, [[seg(O1A) = 12]]일 때 [[pow(seg(O2A), 2) = frac(q, p)]] 이다. [[p + q]]의 값을\n구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None, derived_answer="890",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 C₁(중심 O₁)과 작은 두 원 C₂(중심 O₂)·C₃(중심 O₃)이 서로 외접, 직각삼각형 O₁O₂O₃(O₂에서 직각), 점 A는 O₁O₃ 위, 선분 O₁A 길이 표시"}}],
    confidence=0.8,
    note="첨자 점 라벨을 angle·seg로. 답 새로 도출 890(반지름 12,3,5 → O₂A²=873/17) = 빠른정답 890 ✓")

# ================= esc_sonnet_h2-1_1of4 =================
# 50. a09c741f — 여러 가지 수열의 합 p92: 가변 첨자 라벨(사각형 OQₖPₖRₖ)은 라벨 문법 범위 밖 → sub 텍스트 유지(파싱 통과). 도형만 unsupported → 통과
add(id="a09c741f", qtype="choice",
    question="자연수 [[n]]에 대하여 함수 [[f(x)]]가 다음과 같다.\n[[f(x) = frac(x + 2 pow(n, 2) + n, x - n)]]\n[[n = k]] ([[k]] = 1, 2, 3, ⋯)일 때, 곡선 [[y = f(x)]]의 제1사분면 위의 점 중에서 [[x]]축, [[y]]축까지의 거리가 같게 되는 점을 [[sub(P, k)]]라 하고, 점 [[sub(P, k)]]에서 [[x]]축, [[y]]축에 내린 수선의 발을 각각 [[sub(Q, k)]], [[sub(R, k)]]라 하자. 사각형 O[[sub(Q, k)]][[sub(P, k)]][[sub(R, k)]]의 넓이를 [[sub(A, k)]]라 할 때, [[sum(k, 1, 10, sub(A, k))]]의 값은?",
    choices=["[[1770]]", "[[1780]]", "[[1790]]", "[[1800]]", "[[1810]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 유리함수 y=f(x)의 그래프(점근선 x=n, y=1 점선), 제1사분면 점 P_k와 수선의 발 Q_k(x축)·R_k(y축), 정사각형 OQ_kP_kR_k 회색 음영 A_k"}}],
    confidence=0.85,
    note="[2015년 9월 고2 이과 14번/4점]. 가변 첨자 k의 점 라벨은 seg/quad 라벨에 못 넣어 sub 텍스트 유지(파싱 통과), 도형만 unsupported. 답 ① 유지(A_k=(2k+1)² → 1770)")

# 51. b1bb6c17 — 수열의 일반항 p24: (f∘g)(k)=383 → app
add(id="b1bb6c17", qtype="short",
    question="자연수의 집합에서 정의되는 두 함수 [[f]]와 [[g]]는\n[[f(n + 1) = f(n) + 3]], [[f(5) = 23]]\n[[g(n + 1) = 5 g(n)]], [[g(1) = 5]]\n를 만족한다. [[app(comp(f, g), k) = 383]]일 때, [[20k]]의 값을 구하시오. (단, [[comp(f, g)]]는 [[f]]와 [[g]]의 합성함수이다.)",
    choices=None, figure=None, confidence=0.85,
    note="[2005년 11월 고2 문과 23번]. 합성 적용을 app으로. 답 60 유지(3·5ᵏ+8=383 → k=3)")

# 52. e4ba9d37 — 삼각함수의 그래프 p17: 경우 나눔 → cases
add(id="e4ba9d37", qtype="choice",
    question="두 상수 [[a]] ([[a != 0]]), [[b]]에 대하여 닫힌구간 [[itv(0, 2pi, cc)]]에서 정의된 함수 [[f(x) = cases(3 sin(x), 0 <= x < pi, a cos(x) + b, pi <= x <= 2pi)]]가 있다. [[0 <= t <= 2pi]]인 실수 [[t]]에 대하여 [[x]]에 대한 방정식 [[f(x) = f(t)]]를 만족시키는 모든 [[x]]의 값의 합이 [[frac(7, 4) pi]]가 되도록 하는 서로 다른 모든 실수 [[t]]의 개수가 4일 때, [[pow(a, 2) + pow(b, 2)]]의 값은?",
    choices=["[[frac(13, 2)]]", "[[frac(27, 4)]]", "[[7]]", "[[frac(29, 4)]]", "[[frac(15, 2)]]"],
    figure=None, confidence=0.8,
    note="[2026년 3월 고3 14번/4점]. 경우 나눔을 cases로. 답 미도출(초안 None 유지)")

# 53. 14bca041 — 삼각함수의 그래프 p99: 문법 문제 없음. 한 이미지에 별개 문항(id 없음)이 더 있어 보류 유지
add(id="14bca041", qtype="choice",
    question="[[0 < theta < frac(pi, 2)]]일 때, [[x]]에 대한 방정식\n[[(2x + sin(theta))(x + 3 sin(theta)) = k x sin(theta) + pow(cos(theta), 2)]]의 서로 다른 두 근을 [[alpha]], [[beta]]라 하자. [[pow(alpha, 2) + pow(beta, 2) = 1]]이 되도록 하는 모든 실수 [[k]]의 값의 합은?",
    choices=["[[8]]", "[[10]]", "[[12]]", "[[14]]", "[[16]]"],
    figure=None, confidence=0.8,
    needs_review="이미지에 별개 문항(이차방정식 x²−2x+2sin²θ−2cos²θ=0이 서로 다른 부호의 실근을 갖도록 하는 θ, 선지 0·π/6·7π/8·11π/8·2π) 1개가 더 인쇄됨(id 없음) — 상단 문항만 전사",
    note="문법 수정 없음(v1.5 재검산 통과). 답 ④ 유지((k−7)²=16 → k=3, 11 → 14)")

# 54. d22d1b34 — 지수함수의 활용 p99: 문법 문제 없음. 이미지 상단에 별개 문항 → 보류 유지
add(id="d22d1b34", qtype="choice",
    question="어느 연구소에서는 매년 두 부서 A, B에 대한 실험 지원비를 전년도에 비해 각각 [[pct(20)]], [[pct(28)]]씩 늘려간다고 한다. 현재 두 부서 A, B의 실험 지원비가 각각 2000만 원, 1000만 원일 때, 부서 B의 실험 지원비가 부서 A의 실험 지원비를 처음으로 초과하는 해는 지금으로부터 몇 년 후인가?\n(단, [[log(2) = 0.3]], [[log(3) = 0.48]]로 계산한다.)",
    choices=["12년", "14년", "16년", "18년", "20년"],
    figure=None, confidence=0.8,
    needs_review="이미지 상단에 별개 문항(세균 A·B 배양, 합이 96 이상이 되는 최소 시간 — 단답형, 답 3시간)이 함께 인쇄됨(id 없음) — 선지형 지원비 문항으로 전사",
    note="문법 수정 없음(v1.5 재검산 통과). 답 ③ 유지(n·0.02>0.3 → n=16)")

# 55. 655842bf — 수학적 귀납법 p81: 줄임표 → cdots, 빈칸 (가)(나) → box. 이미지 하단 잘림(선지 ④⑤ 안 보임) → 보류 유지
add(id="655842bf", qtype="choice",
    question="다음은 2 이상의 모든 자연수 [[n]]에 대하여\n[[1 + frac(1, pow(2, 2)) + frac(1, pow(3, 2)) + cdots + frac(1, pow(n, 2)) < 2 - frac(1, n)]]임을\n수학적 귀납법으로 증명한 것이다.\n\n<증명>\n(ⅰ) [[n = box(1)]] 일 때,\n(좌변)=[[1 + frac(1, pow(2, 2)) = frac(5, 4) < 2 - frac(1, 2) = frac(3, 2)]]=(우변)\n따라서, [[n = box(1)]] 일 때, 주어진 식은 성립한다.\n(ⅱ) [[n = k]] ([[n >= 2]])일 때, 주어진 식이 성립한다고 가정하면\n[[1 + frac(1, pow(2, 2)) + frac(1, pow(3, 2)) + cdots + frac(1, pow(k, 2)) < 2 - frac(1, k)]]이다.\n위 식의 양변에 [[frac(1, pow(k + 1, 2))]]을 더하면\n[[1 + frac(1, pow(2, 2)) + frac(1, pow(3, 2)) + cdots + frac(1, pow(k, 2)) + frac(1, pow(k + 1, 2)) < 2 - frac(1, k) + frac(1, pow(k + 1, 2))]]\n그런데\n[[(-frac(1, k) + frac(1, pow(k + 1, 2))) - box(2) = -frac(1, k pow(k + 1, 2)) < 0]] 이므로\n[[2 - frac(1, k) + frac(1, pow(k + 1, 2)) < 2 - frac(1, k + 1)]]이다.\n따라서, [[n = k + 1]]일 때에도 성립한다.\n(ⅰ), (ⅱ)에 의하여 [[n >= 2]]인 모든 자연수 [[n]]에 대하여\n[[1 + frac(1, pow(2, 2)) + frac(1, pow(3, 2)) + cdots + frac(1, pow(n, 2)) < 2 - frac(1, n)]]이 성립한다.\n\n이 증명 과정에서 (가), (나)에 알맞은 내용을 바르게 짝지은 것은?",
    choices=["(가) [[1]], (나) [[frac(1, k + 1)]]", "(가) [[1]], (나) [[-frac(1, k + 1)]]", "(가) [[2]], (나) [[-frac(1, k + 1)]]", "(이미지 하단 잘림)", "(이미지 하단 잘림)"],
    figure=None, confidence=0.75,
    needs_review="이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움)",
    note="[2004년 11월 고2 이과 13번]. 줄임표를 cdots로, 빈칸 (가)(나)를 box로(원문 중괄호 {…}−(나)는 소괄호). 답 ③ 유지((가)=2, (나)=−1/(k+1); 보이는 선지 기준)")

# ================= esc_sonnet_h2-1_2of4 =================
# 56. fe1ef907 — 지수함수 p30: 가변 첨자 라벨(삼각형 OPₖQₖ)은 sub 텍스트 유지. 도형만 unsupported → 통과
add(id="fe1ef907", qtype="short",
    question="그림과 같이 두 곡선 [[y = pow(2, x)]], [[y = pow(2, x - 2)]]과 직선 [[y = k]]의\n교점을 각각 [[sub(P,k)]], [[sub(Q,k)]]라 하고, 삼각형 O[[sub(P,k)]][[sub(Q,k)]]의 넓이를\n[[sub(A,k)]]라 하자.\n[[sub(A,1) + sub(A,4) + sub(A,7) + sub(A,10)]]의 값을 구하시오.\n(단, [[k]]는 자연수이고, O는 원점이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 곡선 y=2^x, y=2^(x−2)와 직선 y=k, 교점 P_k, Q_k, 삼각형 OP_kQ_k 음영, O 원점"}}],
    confidence=0.85,
    note="[2010년 10월 고3 문과 20번]. 가변 첨자 k의 점 라벨은 tri 라벨에 못 넣어 sub 텍스트 유지(파싱 통과), 도형만 unsupported. 답 22 유지(A_k=k → 1+4+7+10)")

# 57. 9fd1c42b — 지수함수 p66: (f∘g)(x) → app
add(id="9fd1c42b", qtype="short",
    question="두 함수 [[f(x) = pow(4, x)]], [[g(x) = pow(x,2) - 6x + 7]]에 대하여\n함수 [[app(comp(f, g), x)]]는 [[x = a]]일 때 최솟값 [[m]]을 갖는다.\n이때 [[frac(a, m)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 48 유지(a=3, m=4⁻²=1/16)")

# 58. 21455b85 — 로그함수 p21: y=(f∘g)(x) → app. 선지 5개가 모두 그래프 → 보류 유지
add(id="21455b85", qtype="choice",
    question="함수 [[f(x) = abs(log(3, abs(x)))]]와 함수 [[g(x) = x - 3]] ([[x != 3]])에\n대하여 함수 [[y = app(comp(f, g), x)]] 의 그래프의 개형은?",
    choices=["[그래프] 수직 점선(점근선)의 왼쪽에서만 정의된 감소 곡선, 점근선 부근에서 아래로 발산", "[그래프] 수직 점선의 오른쪽에서만 정의된 증가 곡선, 점근선 부근에서 아래로 발산", "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 아래로 발산, [[x]]절편 2개", "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 위로 발산, [[x]]축 위에서 두 점에 닿는 V자 모양", "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 아래로 발산, [[x]]축 아래에서 두 점에 닿는 ∧자 모양"],
    figure=None, confidence=0.75,
    needs_review="선지 ①~⑤가 모두 그래프 그림 — 문법·텍스트로 표현 불가(설명문으로 대체)",
    note="합성 적용을 app으로. 답 ④ 유지(y=|log₃|x−3||)")

# 59. abe7bcf0 — 로그함수 p24: y=(f∘g)(x) → app. 선지 그래프 → 보류 유지
add(id="abe7bcf0", qtype="choice",
    question="함수 [[f(x) = log(2, abs(x))]]와 함수 [[g(x) = x - 2]]\n([[x != 2]])에 대하여 함수 [[y = app(comp(f, g), x)]] 의 그래프의\n개형은?",
    choices=["[그래프] 수직 점선(점근선)의 왼쪽에서만 정의된 감소 곡선, 점근선 부근에서 아래로 발산", "[그래프] 수직 점선의 오른쪽에서만 정의된 증가 곡선, 점근선 부근에서 아래로 발산", "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 아래로 발산, [[x]]절편 2개, 양쪽 바깥으로 증가", "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 위로 발산, [[x]]축 위에서 두 점에 닿는 V자 모양", "[그래프] 수직 점선 양쪽에서 정의, 점근선 부근에서 아래로 발산, [[x]]축 아래에서 두 점에 닿는 ∧자 모양"],
    figure=None, confidence=0.75,
    needs_review="선지 ①~⑤가 모두 그래프 그림 — 문법·텍스트로 표현 불가(설명문으로 대체)",
    note="[2013년 9월 고2 문과 18번/4점]. 합성 적용을 app으로. 답 ③ 유지(y=log₂|x−2|)")

# 60. 06f37ad8 — 로그함수 p98: 경우 나눔 → cases
add(id="06f37ad8", qtype="choice",
    question="함수 [[f(x) = cases(-pow(2, x) + 2, x < 1, log(2, x), x >= 1)]]에 대하여\n[[a - 1 <= x <= a + 1]]에서 함수 [[f(x)]]의 최댓값과 최솟값의\n차가 1이 되도록 하는 모든 실수 [[a]]의 값의 합은?",
    choices=["[[3]]", "[[log(2, frac(32, 3))]]", "[[log(2, frac(40, 3))]]", "[[4]]", "[[log(2, frac(56, 3))]]"],
    figure=None, confidence=0.85,
    note="[2024년 9월 고2 18번/4점]. 경우 나눔을 cases로. 답 ② 유지(5−log₂3=log₂(32/3))")

# 61. 3917ce0b — 수열의 귀납적 정의 p42: cₙ 경우 나눔 → cases
add(id="3917ce0b", qtype="choice",
    question="두 수열 [[set(sub(a,n))]], [[set(sub(b,n))]]은 첫째항이 모두 1이고\n[[sub(a, n+1) = 3 sub(a,n)]], [[sub(b, n+1) = (n + 2) sub(b,n)]] ([[n]] = 1, 2, 3, ⋯)\n과 같이 정의된다. 수열 [[set(sub(c,n))]]을\n[[sub(c,n) = cases(sub(a,n), sub(a,n) < sub(b,n), sub(b,n), sub(a,n) >= sub(b,n))]]이라 할 때, [[sum(n, 1, 30, sub(c,n))]]의 값은?",
    choices=["[[pow(3, 31) + 1]]", "[[pow(3, 31) - 1]]", "[[pow(3, 30) - 1]]", "[[frac(pow(3, 30) - 1, 2)]]", "[[frac(pow(3, 30) + 1, 2)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 ④ 유지(c₁=1, c₂=3, n≥3은 3ⁿ⁻¹ → (3³⁰−1)/2)")

# 62. ff5049bf — 수열의 귀납적 정의 p72: (가)/n·n!×(나) → box, 곱 줄임표 → cdots, aₙ 경우 나눔(n=1,2 열거는 in(n, set(1,2))) → cases
add(id="ff5049bf", qtype="choice",
    question="첫째항이 1인 수열 [[set(sub(a,n))]]에 대하여 [[sub(S,n) = sum(k, 1, n, sub(a,k))]]라 할 때,\n[[frac(sub(S, n+1), n + 1) = sum(k, 1, n, sub(S,k))]] ([[n >= 1]]) ⋯⋯ (∗)\n이 성립한다. 다음은 일반항 [[sub(a,n)]]을 구하는 과정이다.\n\n주어진 식 (∗)에 의하여\n[[frac(sub(S,n), n) = sum(k, 1, n - 1, sub(S,k))]] ([[n >= 2]]) ⋯⋯ ㉠\n이다. (∗)에서 ㉠을 빼서 정리하면\n[[frac(sub(S, n+1), sub(S,n)) = frac(box(1), n)]] ([[n >= 2]])\n이다. ㉠으로부터 [[sub(S,2) = 2]]이고,\n[[sub(S,n) = frac(sub(S,n), sub(S, n-1)) × frac(sub(S, n-1), sub(S, n-2)) × cdots × frac(sub(S,3), sub(S,2)) × sub(S,2)]] ([[n >= 3]])\n이므로\n[[sub(S,n) = fact(n) × box(2)]] ([[n >= 3]])\n이다. 그러므로 [[sub(a,n)]]은\n[[sub(a,n) = cases(1, in(n, set(1, 2)), frac(pow(n, 2) - n + 1, 2) × fact(n - 1), n >= 3)]]\n이다.\n\n위의 (가), (나)에 알맞은 식을 각각 [[f(n)]], [[g(n)]]\n이라 할 때, [[f(4) × g(20)]]의 값은?",
    choices=["[[225]]", "[[250]]", "[[275]]", "[[300]]", "[[325]]"],
    figure=None, confidence=0.85,
    note="[2014년 9월 고3 이과 12번/3점]. 빈칸을 box로, 곱 줄임표를 cdots로, 경우 나눔을 cases로(조건 'n=1, 2'는 in(n, set(1,2))). 답 ② 유지((가)=(n+1)², (나)=n/2 → 25×10)")

# 63. 2a1e2b27 — 수열의 귀납적 정의 p82: 가변 첨자 라벨(삼각형 QₙQₙ₊₁Qₙ₊₂)은 sub 텍스트 유지(파싱 통과) → 통과
add(id="2a1e2b27", qtype="short",
    question="자연수 [[n]]에 대하여 좌표평면 위의 점 [[sub(P,n)]]의 좌표를\n[[point(n, a n - a)]]라 하자. 두 점 [[sub(Q,n)]], [[sub(Q, n+1)]]에 대하여\n점 [[sub(P,n)]]이 삼각형 [[sub(Q,n)]][[sub(Q, n+1)]][[sub(Q, n+2)]]의 무게중심이 되도록\n점 [[sub(Q, n+2)]]를 정한다. 두 점 [[sub(Q,1)]], [[sub(Q,2)]]의 좌표가 각각\n[[point(0, 0)]], [[point(1, -1)]]이고 점 [[sub(Q,10)]]의 좌표가 [[point(9, 90)]]이다.\n점 [[sub(Q,13)]]의 좌표를 [[point(p, q)]]라 할 때, [[p + q]]의 값을\n구하시오. (단, [[a > 1]])",
    choices=None, figure=None, confidence=0.85,
    note="[2017년 10월 고3 문과 29번/4점]. 가변 첨자(n, n+1, n+2)의 점 라벨은 tri 라벨 문법 범위 밖이라 sub 텍스트 유지(파싱 통과, 도형 없음). 답 132 유지(a=10, Q₁₃=(12,120))")

# 64. 53ba5ea7 — 등차수열 p56: 윗줄 P₁Q₁ 등 → seg(P1Q1), 줄임표 합 → cdots. 도형 unsupported → 통과
add(id="53ba5ea7", qtype="choice",
    question="다음 그림과 같이 직선 [[l]] 위에 같은 간격으로\n16개의 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,16)]]을 잡고, 각 점에서\n직선 [[m]]에 내린 수선의 발을 차례대로 [[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], ⋯,\n[[sub(Q,16)]]이라 하자. [[seg(P1Q1) = 12]], [[seg(P16Q16) = 40]]일 때,\n[[seg(P2Q2) + seg(P3Q3) + seg(P4Q4) + cdots + seg(P15Q15)]]의 값은?",
    choices=["[[360]]", "[[364]]", "[[368]]", "[[372]]", "[[376]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직선 l 위의 점 P₁~P₁₆에서 직선 m에 내린 수선 P₁Q₁=12, P₁₆Q₁₆=40 (사다리꼴 모양, 직각 표시)"}}],
    confidence=0.85,
    note="첨자 점 라벨 선분을 seg(P1Q1) 등으로, 줄임표 합을 cdots로. 도형 unsupported(raw). 답 ② 유지(가운데 14항 합 14·26=364)")

# 65. 9bb1cd32 — 등차수열 p57: seg + cdots
add(id="9bb1cd32", qtype="choice",
    question="다음 그림과 같이 직선 [[l]] 위에 같은 간격으로\n12개의 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,12)]]를 잡고, 각 점에서\n직선 [[m]]에 내린 수선의 발을 차례대로 [[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], ⋯,\n[[sub(Q,12)]]라 하자. [[seg(P1Q1) = 16]], [[seg(P12Q12) = 30]]일 때,\n[[seg(P2Q2) + seg(P3Q3) + seg(P4Q4) + cdots + seg(P11Q11)]]의 값은?",
    choices=["[[210]]", "[[220]]", "[[230]]", "[[240]]", "[[250]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직선 l 위의 점 P₁~P₁₂에서 직선 m에 내린 수선 P₁Q₁=16, P₁₂Q₁₂=30 (사다리꼴 모양, 직각 표시)"}}],
    confidence=0.85,
    note="첨자 점 라벨 선분을 seg로, 줄임표 합을 cdots로. 도형 unsupported(raw). 답 ③ 유지(10·23=230)")

# 66. 44dc6f21 — 등차수열 p58: seg + cdots
add(id="44dc6f21", qtype="choice",
    question="다음 그림과 같이 직선 [[l]] 위에 같은 간격으로\n12개의 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]], ⋯, [[sub(P,12)]]를 잡고, 각 점에서\n직선 [[m]]에 내린 수선의 발을 차례대로 [[sub(Q,1)]], [[sub(Q,2)]], [[sub(Q,3)]], ⋯,\n[[sub(Q,12)]]라 하자. [[seg(P1Q1) = 10]], [[seg(P12Q12) = 28]]일 때,\n[[seg(P2Q2) + seg(P3Q3) + seg(P4Q4) + cdots + seg(P11Q11)]]의 값은?",
    choices=["[[170]]", "[[180]]", "[[190]]", "[[200]]", "[[210]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "직선 l 위의 점 P₁~P₁₂에서 직선 m에 내린 수선 P₁Q₁=10, P₁₂Q₁₂=28 (사다리꼴 모양, 직각 표시)"}}],
    confidence=0.85,
    note="첨자 점 라벨 선분을 seg로, 줄임표 합을 cdots로. 도형 unsupported(raw). 답 ③ 유지(10·19=190)")

# ================= esc_sonnet_h2-1_3of4 =================
# 67. 247673f2 — 삼각함수 p28: 경우 나눔 → cases
add(id="247673f2", qtype="short",
    question="[[f(x) = cases(1, x < 0, -2, x >= 0)]]일 때, 다음 식을 만족시키는 각 [[theta]]는 제 몇 사분면의 각인지 구하시오.\n[[2 f(sin(theta)) f(cos(theta)) + f(tan(theta)) = 0]]",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 '제3사분면' 유지(sinθ<0, cosθ<0, tanθ>0; 빠른정답 3은 표기 차이)")

# 68. be6710b3 — 사인·코사인 p55: 상단 잘림 의심 → 확대 확인 결과 다른 문항과 같은 상단 여백(글자 잘림 없음), 문장 완결 → 통과
add(id="be6710b3", qtype="short",
    question="[[ratio(sin(A), sin(B), sin(C)) = ratio(13, 7, 8)]]일 때, [[A]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    note="상단 잘림 의심은 확대 확인 결과 여백이 정상(다른 문항과 동일)이고 문장이 완결되어 잘림 아님으로 판단. 답 120° 유지(a:b:c=13:7:8 → cos A=−1/2)")

# 69. 586d76ad — 사인·코사인 p99: 문법 문제 없음. 한 이미지에 별개 문항 2개(id 1개) → 보류 유지
add(id="586d76ad", qtype="short",
    question="다음 그림과 같은 평행사변형 ABCD에서 [[seg(AB) = 4]], [[seg(AD) = 9]]이고 두 대각선 AC와 BD가 이루는 각의 크기가 [[deg(135)]]일 때, 평행사변형 ABCD의 넓이를 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AB = 4, AD = 9, 두 대각선의 교각 135°, 내부 음영"}}],
    confidence=0.75,
    needs_review="이미지에 별개 문항 2개 인쇄(아래 문항: AB=1, BC=2, B=π/3인 평행사변형의 두 대각선이 이루는 각 θ에 대한 sin²θ 선지형 ①1/7~⑤5/7, 답 ④) — id 1개라 빠른정답(65/2)에 맞는 위 문항만 전사",
    note="문법 수정 없음(v1.5 재검산 통과). 답 65/2 유지")

# 70. b63fade3 — 등비수열 p55: 문법 문제 없음(A′은 그림 설명에만). 도형만 unsupported → 통과
add(id="b63fade3", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = 21]]인 평행사변형 ABCD가 있다. 이 도형을 대각선 BD를 접는 선으로 하여 접어서 생기는 삼각형 EBC의 넓이가 평행사변형 ABCD의 넓이의 [[frac(3, 14)]]이고, [[seg(CE)]], [[seg(EB)]], [[seg(BD)]]의 길이가 이 순서대로 등비수열을 이룰 때, [[pow(seg(AD), 2)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(A 왼쪽 아래, B 오른쪽 아래, D 왼쪽 위, C 오른쪽 위)를 대각선 BD로 접은 그림, A의 대응점 A′(위), 접힌 변 BA′가 DC와 만나는 점 E, AB = 21"}}],
    confidence=0.85,
    note="문법 문제 없음(프라임 점 A′은 그림 설명에만 등장). 도형 unsupported(raw). 답 249 유지(CE=9, EB=12, BD=16 → cos∠BEC=−1/9)")

# 71. 6b57a62e — 거듭제곱근 p29: 경우 나눔 조건이 한글(n이 홀수/짝수) → cases 불가, 보류 유지
add(id="6b57a62e", qtype="choice",
    question="자연수 [[n]]에 대하여 [[f(n)]]이 다음과 같다.\n[[f(n)]] = { [[root(4, 9 × pow(2, n+1))]] ([[n]]이 홀수) ; [[root(4, 4 × pow(3, n))]] ([[n]]이 짝수) }\n10 이하의 두 자연수 [[p]], [[q]]에 대하여 [[f(p) × f(q)]]가 자연수가 되도록 하는 모든 순서쌍 [[point(p, q)]]의 개수는?",
    choices=["[[36]]", "[[38]]", "[[40]]", "[[42]]", "[[44]]"],
    figure=None, confidence=0.75,
    needs_review="경우 나눔 정의의 조건이 한글 문장(n이 홀수/짝수)이라 cases로 쓸 수 없음 — 텍스트 혼합 유지",
    note="[2019년 6월 고2 이과 21번/4점]. 답 ⑤ 유지(전수 확인 44)")
