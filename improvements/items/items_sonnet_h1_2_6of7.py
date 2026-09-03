# -*- coding: utf-8 -*-
# esc_sonnet_h1-2_6of7 — 이미지 기준 전사 (83 항목 / 80쪽: 함수의 합성 31 + 선분의 내분 28 + 원과 직선 12 + 함수의 개념 12)
# 표기 관행: 합성함수 적용 (f∘g)(x)는 ([[comp(f, g)]])([[x]]) 텍스트 혼합 → needs_review.
#            fⁿ(x) 꼴은 [[pow(f, n)]]([[x]]) 텍스트 혼합 → needs_review. 조각적 정의는 { … ; … } 텍스트 → needs_review.
#            대응 그림·함수 그래프·좌표평면 도형은 unsupported(raw 설명) + needs_review.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_NUM = lambda *v: ["[[%s]]" % x for x in v]
CH_GND = ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ===================== 함수의 합성 =====================
# p10
add(id="958c43ec", qtype="choice",
    question="함수 [[f]]: [[X]]→[[X]]가 다음 그림과 같을 때,\n([[comp(comp(f, f), f)]])([[0]]) + ([[comp(f, f)]])([[0]])의 값은?",
    choices=CH_NUM("-2", "-1", "0", "1", "2"),
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→X, X={-1, 0, 1}. 화살표 -1→0, 0→1, 1→-1"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음) / 합성함수 적용 표기 텍스트 혼합",
    note="f(-1)=0, f(0)=1, f(1)=-1 → (f∘f∘f)(0)=f(f(1))=f(-1)=0, (f∘f)(0)=f(1)=-1 → 합 -1 → ② = 빠른정답 ✓.")

# p11
add(id="7844d5cd", qtype="short",
    question="두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[Z]]가 다음 그림과 같을 때, ([[comp(f, g)]])([[6]])의 값을 구하시오.",
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 2개. f: X={1,3,5,7}→Y={2,4,6,8}: 1→4, 3→6, 5→2, 7→8. g: Y={2,4,6,8}→Z={1,3,5,7}: 2→1, 4→7, 6→5, 8→3"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음) / 합성함수 적용 표기 텍스트 혼합",
    note="g(6)=5, f(5)=2 → 2 = 빠른정답 ✓.")

# p12
add(id="dec2e6fa", qtype="short",
    question="두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[X]]가 다음 그림과 같을 때,\n([[comp(g, f)]])([[7]])의 값을 구하시오.",
    choices=None, derived_answer="7",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 2개. f: X={1,3,5,7}→Y={x,y,z,w}: 1→z, 3→w, 5→x, 7→y. g: Y→X={1,3,5,7}: x→5, y→7, z→3, w→5 (1은 대응 없음)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음) / 합성함수 적용 표기 텍스트 혼합",
    note="f(7)=y, g(y)=7 → 7 = 빠른정답 ✓.")

# p13
add(id="9aff9aab", qtype="short",
    question="두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[X]]가 다음 그림과 같을 때,\n([[comp(f, g)]])([[5]])의 값을 구하시오.",
    choices=None, derived_answer="8",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 2개. f: X={1,2,3,4}→Y={5,6,7,8}: 1→6, 2→7, 3→5, 4→8. g: Y={5,6,7,8}→X={1,2,3,4}: 5→4, 6→3, 7→2, 8→1"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음) / 합성함수 적용 표기 텍스트 혼합",
    note="g(5)=4, f(4)=8 → 8. 빠른정답 2와 불일치.")

# p14
add(id="f761c03b", qtype="short",
    question="두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[X]]가 다음 그림과 같을 때,\n([[comp(g, f)]])([[2]])의 값을 구하시오.",
    choices=None, derived_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 2개. f: X={2,3,5,7}→Y={p,q,r,s}: 2→q, 3→s, 5→q, 7→q. g: Y={p,q,r,s}→X={2,3,5,7}: p→7, q→3, r→3, s→2"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음) / 합성함수 적용 표기 텍스트 혼합",
    note="f(2)=q, g(q)=3 → 3. 빠른정답 2와 불일치.")

# p15 (id 3개 — 같은 문항; draft_a가 보기 ㄴ·ㄷ을 별개 항목으로 쪼갰던 것)
dup(["49b676f9", "30dd13bc", "0588e1da"], qtype="choice",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 있다. 함수 [[f]]가 일대일대응일 때,\n"
              "보기 중에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(1) × f(2) × f(3) = 10]]이면\n[[f(4) + f(5) + f(6) = 13]]이다.\n"
              "ㄴ. 집합 [[X]]의 모든 원소 [[x]]에 대하여\n([[comp(f, f)]])([[x]]) = [[x]]이면 [[f(a) = a]]인\n집합 [[X]]의 원소 [[a]]가 존재한다.\n"
              "ㄷ. 집합 [[X]]의 모든 원소 [[x]]에 대하여\n([[comp(comp(f, f), f)]])([[x]]) = [[x]]이면 [[f(b) = b]]인\n집합 [[X]]의 원소 [[b]]가 존재한다."),
    choices=CH_GND, derived_answer="①", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 합성함수 적용 표기 (f∘f)(x) 텍스트 혼합",
    note="출처 [2017년 3월 고2 문과 20번 변형]. ㄱ {f(1),f(2),f(3)}={1,2,5} → 나머지 합 13 ✓; ㄴ 고정점 없는 대합(2-순환 3개) 반례 ✗; ㄷ 3-순환 2개 반례 ✗ → ①. 빠른정답 7과 불일치. 한 이미지에 id 3개 → 동일 전사.")

# p19
add(id="305abdee", qtype="choice",
    question="두 함수 [[f(x) = x + a]], [[g(x) = pow(x,2) - 1]]일 때, 모든 실수 [[x]]에 대하여 ([[comp(f, g)]])([[x]]) = ([[comp(g, f)]])([[x]])가 성립하도록 실수 [[a]]의 값을 정하면?",
    choices=CH_NUM("0", "-1", "-2", "1", "4"),
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 합성함수 적용 표기 (f∘g)(x) 텍스트 혼합",
    note="x²-1+a = (x+a)²-1 → 2a=0, a²=a → a=0 → ① = 빠른정답 ✓.")

# p25
add(id="a3ca14db", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여\n두 함수 [[f]]: [[X]]→[[X]], [[g]]: [[X]]→[[X]]가 있다. 함수 [[f]]가 다음 그림과 같이 정의되고 두 함수 [[f]], [[g]]가 "
              "[[comp(f, g) = comp(g, f)]]를 만족한다. [[g(1) = 5]]일 때, [[g(3)]]의 값을 구하시오."),
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→X, X={1,2,3,4,5}. 화살표 1→3, 2→4, 3→5, 4→1, 5→2"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음)",
    note="g(3)=g(f(1))=f(g(1))=f(5)=2. 빠른정답 14와 불일치.")

# p26
add(id="aa7c1652", qtype="choice",
    question=("집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여\n함수 [[f]] : [[X]] → [[X]] 가 아래 그림과 같고,\n[[g]] : [[X]] → [[X]] 가 [[g(1) = 3]], [[comp(f, g) = comp(g, f)]] 를\n"
              "만족할 때, [[g(5)]] 의 값은?"),
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→X, X={1,2,3,4,5}. 화살표 1→2, 2→3, 3→4, 4→5, 5→1"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음)",
    note="g(2)=f(3)=4, g(3)=f(4)=5, g(4)=f(5)=1, g(5)=f(1)=2 → ②. 빠른정답 1과 불일치.")

# p27
add(id="a4b62373", qtype="choice",
    question=("함수 [[f]]: [[X]]→[[Y]]가 다음 그림과 같고, 함수 [[g]]: [[X]]→[[Y]]가\n[[g(1) = 2]], [[comp(f, g) = comp(g, f)]]를 만족할 때, [[g(1) - g(3)]]의\n값은?"),
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→Y, X={0,1,2,3}, Y={0,1,2,3}. 화살표 0→2, 1→3, 2→0, 3→1"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음)",
    note="g(3)=g(f(1))=f(g(1))=f(2)=0 → g(1)-g(3)=2 → ② = 빠른정답 ✓.")

# p31
add(id="0c07e597", qtype="choice",
    question=("그림과 같이 한 변의 길이가 1인 정육각형 ABCDEF가 있다. 점 P는 점 A에서 출발하여 점 F까지 화살표 방향으로 정육각형 ABCDEF의 변을 따라 움직인다. "
              "점 P가 점 A로부터 움직인 거리가 [[x]] ([[0 < x < 5]])일 때, 삼각형 PFA의 넓이를 [[f(x)]]라 하자. 다음은 함수 [[f(x)]]에 대하여 "
              "([[comp(f, f)]])([[a]]) = [[frac(9, 32)]]인 모든 실수 [[a]]의 값의 곱을 구하는 과정이다.\n"
              "([[comp(f, f)]])([[a]]) = [[f(f(a)) = frac(9, 32)]]에서\n[[f(a) = b]]라 하면 [[f(b) = frac(9, 32)]]이고,\n"
              "함수 [[f(x)]]의 최댓값은 (가) 이므로\n[[0 < b]] ≤ (가) 이다.\n"
              "점 P가 점 A로부터 움직인 거리가 [[b]]인 점을 Q라 하면 삼각형 QFA의 넓이는 [[frac(9, 32)]]이다.\n"
              "점 Q에서 직선 FA에 내린 수선의 발을 H라 하면\n[[seg(QH) = frac(9, 16)]]이므로 [[b]] = (나) 이다.\n"
              "같은 방법으로 [[f(a)]] = (나) 를 만족시키는\n[[a]] ([[0 < a < 5]])의 값을 구하면\n[[a]] = □ 또는 [[a]] = □ 이다.\n"
              "따라서 ([[comp(f, f)]])([[a]]) = [[frac(9, 32)]]를 만족시키는\n모든 실수 [[a]]의 값의 곱은 (다) 이다.\n"
              "위의 (가), (나), (다)에 알맞은 수를 각각 [[p]], [[q]], [[r]]라 할 때,\n[[frac(r, p q)]]의 값은?"),
    choices=CH_NUM("frac(26, 3)", "frac(28, 3)", "10", "frac(32, 3)", "frac(34, 3)"),
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정육각형 ABCDEF(A 오른쪽 아래, B 오른쪽, C 오른쪽 위, D 왼쪽 위, E 왼쪽, F 왼쪽 아래), 변을 따라 A→B→C→D→E→F 방향 화살표, 변 BC 위의 점 P, 삼각형 PFA 음영, FA=1 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정육각형 위 점의 이동 그림 / 합성함수 적용 표기·빈칸 상자 텍스트 혼합",
    note="출처 [2022년 3월 고2 21번/4점]. (가)=√3/2, (나)=3√3/8, (다)=(3/2)(7/2)=21/4 → r/(pq)=(21/4)/(9/16)=28/3 → ② = 빠른정답 ✓.")

# p33
add(id="c0d842a8", qtype="choice",
    question=("아래 그림과 같이 한 변의 길이가 2인\n정육각형 ABCDEF가 있다. 점 P는 점 A에서 출발하여 점 F까지 화살표 방향으로 정육각형 ABCDEF의 변을 따라 움직인다. "
              "점 P가 점 A로부터 움직인 거리가\n[[x]] ([[0 < x < 10]])일 때, 삼각형 PFA의 넓이를 [[f(x)]]라 하자.\n다음은 함수 [[f(x)]]에 대하여 "
              "([[comp(f, f)]])([[a]]) = [[frac(27, 16)]]인 모든\n실수 [[a]]의 값의 곱을 구하는 과정이다.\n"
              "([[comp(f, f)]])([[a]]) = [[f(f(a)) = frac(27, 16)]]에서\n[[f(a) = b]]라 하면 [[f(b) = frac(27, 16)]]이고,\n"
              "함수 [[f(x)]]의 최댓값은 (가) 이므로\n[[0 < b]] ≤ (가) 이다.\n"
              "점 P가 점 A로부터 움직인 거리가 [[b]]인 점을 Q라 하면 삼각형 QFA의 넓이는 [[frac(27, 16)]]이다.\n"
              "점 Q에서 직선 FA에 내린 수선의 발을 H라 하면\n[[seg(QH) = frac(27, 16)]]이므로 [[b]] = (나) 이다.\n"
              "같은 방법으로 [[f(a)]] = (나) 를 만족시키는\n[[a]] ([[0 < a < 10]])의 값을 구하면\n[[a]] = □ 또는 [[a]] = □ 이다.\n"
              "따라서 ([[comp(f, f)]])([[a]]) = [[frac(27, 16)]]을 만족시키는\n모든 실수 [[a]]의 값의 곱은 (다) 이다.\n"
              "위의 (가), (나), (다)에 알맞은 수를 각각 [[p]], [[q]], [[r]]라 할 때,\n[[frac(r, p q)]]의 값은?"),
    choices=CH_NUM("frac(7, 3)", "frac(29, 12)", "frac(5, 2)", "frac(31, 12)", "frac(8, 3)"),
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "정육각형 ABCDEF(A 오른쪽 아래, B 오른쪽, C 오른쪽 위, D 왼쪽 위, E 왼쪽, F 왼쪽 아래), 변을 따라 A→B→C→D→E→F 방향 화살표, 변 BC 위의 점 P, 삼각형 PFA 음영, FA=2 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 정육각형 위 점의 이동 그림 / 합성함수 적용 표기·빈칸 상자 텍스트 혼합",
    note="출처 [2022년 3월 고2 21번 변형]. (가)=2√3, (나)=9√3/8, (다)=(9/4)(31/4)=279/16 → r/(pq)=(279/16)/(27/4)=31/12 → ④. 빠른정답 3과 불일치.")

# p48
add(id="c01c58f0", qtype="short",
    question="세 함수 [[f]], [[g]], [[h]]에 대하여\n([[comp(h, g)]])([[x]]) = [[-x + 7]], ([[comp(comp(h, g), f)]])([[x]]) = [[frac(1, 3) x + 5]]일 때,\n[[f(12)]]의 값을 구하시오.",
    choices=None, derived_answer="-2", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 합성함수 적용 표기 (h∘g)(x), (h∘g∘f)(x) 텍스트 혼합",
    note="-f(x)+7 = x/3+5 → f(x)=2-x/3 → f(12)=-2. 빠른정답 'neg 5'와 불일치.")

# p51
add(id="dfdf912e", qtype="short",
    question="세 함수 [[f(x)]], [[g(x) = frac(3x + 1, 2)]], [[h(x) = 9x + 1]]에\n대하여 ([[comp(f, g)]])([[x]]) = [[h(x)]]일 때, [[f(1)]]의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 합성함수 적용 표기 (f∘g)(x) 텍스트 혼합",
    note="g(x)=1 → x=1/3 → f(1)=h(1/3)=4 = 빠른정답 ✓.")

# p56
add(id="6c774c25", qtype="choice",
    question=("실수 전체의 집합 [[R]]에서 [[R]]로의 함수 [[f]]가\n[[f]]: [[x]]→[[x + 1]]로 주어질 때, [[pow(f, 2006)]]([[2]])의 값은 얼마인가?\n"
              "(단, [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]], [[n]]은 자연수)"),
    choices=CH_NUM("2002", "2004", "2006", "2008", "2010"),
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 합성함수 거듭제곱 fⁿ(x) 적용 표기 텍스트 혼합",
    note="f^2006(2)=2+2006=2008 → ④. 빠른정답 5와 불일치.")

# p58
add(id="5a48301e", qtype="short",
    question=("[[-1 <= x <= 1]]에서 정의된 함수 [[y = f(x)]]의 그래프가\n다음 그림과 같고\n[[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]] = 1, 2, 3, ⋯)일 때,\n"
              "[[pow(f, 50)]]([[-frac(1, 2)]])의 값을 구하시오."),
    choices=None, derived_answer="1",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: 점 (-1, 1) 검은 점, -1<x≤0에서 y=-1 (x=-1 흰 점, x=0 검은 점), 0<x≤1에서 y=0 (x=0 흰 점, x=1 검은 점); 점선으로 (-1,1)에서 축까지 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프(함숫값이 그림에만 있음) / fⁿ 적용 표기 텍스트 혼합",
    note="f(-1/2)=-1, f(-1)=1, f(1)=0, f(0)=-1 → 주기 3: n≡2 (mod 3)이면 1 → f^50(-1/2)=1. 빠른정답 5와 불일치.")

# p59
add(id="39f7495d", qtype="short",
    question=("[[0 < x <= 3]]에서 정의된\n함수 [[y = f(x)]]의 그래프가 다음 그림과 같고\n[[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]] = 1, 2, 3, ⋯ )일 때,\n"
              "[[pow(f, 100)]]([[frac(1, 3)]])의 값을 구하시오."),
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: 0<x≤1에서 y=2 (x=0 흰 점, x=1 검은 점), 1<x≤2에서 y=3 (x=1 흰 점, x=2 검은 점), 2<x≤3에서 y=1 (x=2 흰 점, x=3 검은 점); 눈금 1,2,3"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프(함숫값이 그림에만 있음) / fⁿ 적용 표기 텍스트 혼합",
    note="f(1/3)=2, f(2)=3, f(3)=1, f(1)=2 → 주기 3: n≡1 (mod 3)이면 2 → f^100(1/3)=2. 빠른정답 4와 불일치.")

# p60
add(id="272c8366", qtype="choice",
    question=("집합 [[X = set(1, 2, 3)]]에 대하여 함수 [[f]]: [[X]]→[[X]]를\n다음과 같이 정의한다.\n"
              "[[pow(f, 1)]]([[x]]) = [[f(x)]], [[pow(f, n + 1)]]([[x]]) = [[f]]([[pow(f, n)]]([[x]]))\n([[n]] = 1, 2, 3, ⋯)라고 할 때, [[pow(f, 100)]]([[3]]) − [[pow(f, 200)]]([[1]])의\n값은?"),
    choices=CH_NUM("-2", "-1", "0", "1", "2"),
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림 f: X→X, X={1,2,3}. 화살표 1→2, 2→3, 3→1"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 대응 그림(함수의 대응이 그림에만 있음) / fⁿ 적용 표기 텍스트 혼합",
    note="f: 1→2→3→1 (3-순환). f^100(3)=f(3)=1, f^200(1)=f²(1)=3 → -2 → ①. 빠른정답 0과 불일치.")

# p62
add(id="9c40ac48", qtype="choice",
    question=("함수 [[f(x) = 2x]]에 대하여\n[[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]] = 1, 2, 3, ⋯)\n"
              "일 때, [[pow(f, k)]]([[4]]) = 1024를 만족시키는 자연수 [[k]]의 값은?"),
    choices=CH_NUM("7", "8", "9", "10", "11"),
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 합성함수 거듭제곱 fᵏ(x) 적용 표기 텍스트 혼합",
    note="2^k·4=2^10 → k=8 → ② = 빠른정답 ✓.")

# p63
add(id="ec33cbb7", qtype="choice",
    question=("자연수 전체의 집합에서 정의된 함수 [[f(x)]]가\n[[f(x)]] = { [[frac(x, 4) + 5]] ([[x]]는 4의 배수이다.) ; [[x - 5]] ([[x]]는 4의 배수가 아니다.) }\n"
              "이고 [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(pow(f, n), f)]]로 정의할 때,\n[[pow(f, n)]]([[100]]) = 0을 만족시키는 자연수 [[n]]의 값은?"),
    choices=CH_NUM("2", "4", "6", "8", "10"),
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔)·fⁿ 적용 표기 텍스트 혼합",
    note="100→30→25→20→10→5→0 → n=6 → ③. 빠른정답 1과 불일치.")

# p64
add(id="c7193146", qtype="choice",
    question=("집합 [[A = set(1, 2, 3, 4, 5)]]에 대하여 함수 [[f]]: [[A]]→[[A]]를\n[[f(x)]] = { [[x - 1]] ([[x >= 2]]) ; [[5]] ([[x = 1]]) }로 정의하자.\n"
              "[[pow(f, 1)]]([[x]]) = [[f(x)]], [[pow(f, n + 1)]]([[x]]) = [[f]]([[pow(f, n)]]([[x]])) ([[n]] = 1, 2, 3, ⋯)\n"
              "라 할 때, [[pow(f, 2020)]]([[2]]) + [[pow(f, 2023)]]([[4]])의 값은?"),
    choices=CH_NUM("3", "4", "5", "6", "7"),
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔)·fⁿ 적용 표기 텍스트 혼합",
    note="5-순환 x→x-1(1→5). 2020≡0 → f^2020(2)=2, 2023≡3 → f^2023(4)=1 → 합 3 → ①. 빠른정답 5와 불일치.")

# p67
add(id="f8f7b689", qtype="choice",
    question=("[[R = setb(x, 0 <= x <= 1)]]이라 할 때, [[R]]에서 [[R]]로의 함수 [[y = f(x)]] 의 그래프가 다음 그림과 같다.(단, [[pow(f, n)]]([[x]]) = ([[f]]∘[[f]]∘⋯∘[[f]])([[x]]) : [[f]] 개수 [[n]]개)\n<그래프>\n"
              "이 때, [[f(frac(1, 4))]] + [[pow(f, 2)]]([[frac(1, 4)]]) + [[pow(f, 3)]]([[frac(1, 4)]]) + ⋯ + [[pow(f, 99)]]([[frac(1, 4)]]) 의\n"
              "값을 구하면? (단, [[f(frac(1, 4)) = frac(1, 2)]], [[f(frac(1, 2)) = frac(3, 4)]], [[f(frac(3, 4)) = frac(1, 4)]] )"),
    choices=CH_NUM("frac(99, 2)", "frac(95, 2)", "frac(93, 2)", "frac(91, 2)", "frac(89, 2)"),
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 f(x)의 그래프(0≤x≤1): 원점에서 출발해 (1/4, 1/2)를 지나 (1/2, 3/4)에서 극대, (3/4, 1/4)에서 극소, (1, 1)까지 올라가는 곡선; 축 눈금 1/4, 1/2, 3/4, 1과 점선 격자"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프 / fⁿ 적용 표기 텍스트 혼합",
    note="1/4→1/2→3/4→1/4 주기 3, 한 주기 합 3/2, 99항 = 33주기 → 99/2 → ① = 빠른정답 ✓.")

# p69
add(id="3725851e", qtype="short",
    question=("양의 실수 [[x]]에 대하여 함수\n[[f(x)]] = { [[pow(x, 4)]] ([[x]]는 무리수) ; [[sqrt(x)]] ([[x]]는 유리수) }\n"
              "라 하자. [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]]은 자연수)라 할 때,\n"
              "[[pow(f, 3n - 2)]]([[1]]) + [[pow(f, 3n - 1)]]([[sqrt(2)]]) + [[pow(f, 3n)]]([[3]])의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔)·fⁿ 적용 표기 텍스트 혼합",
    note="f^k(1)=1; √2→4→2→√2 주기 3이므로 f^(3n-1)(√2)=2; 3→√3→9→3이므로 f^(3n)(3)=3 → 합 6. 빠른정답 1과 불일치.")

# p75
add(id="f31d5d58", qtype="choice",
    question=("실수 전체의 집합에서 정의된 함수 [[f(x)]]가 다음 조건을 만족시킨다.\n"
              "(가) [[f(x)]] = { [[2]] ([[0 <= x < 2]]) ; [[-2x + 6]] ([[2 <= x < 3]]) ; [[0]] ([[3 <= x <= 4]]) }\n"
              "(나) 모든 실수 [[x]]에 대하여\n[[f(-x) = f(x)]]이고, [[f(x) = f(x - 8)]]이다.\n"
              "실수 전체의 집합에서 정의된 함수\n[[g(x)]] = { [[frac(abs(x), x) + n]] ([[x != 0]]) ; [[n]] ([[x = 0]]) }\n"
              "에 대하여 함수 ([[comp(f, g)]])([[x]])가 상수함수가 되도록 하는\n60 이하의 자연수 [[n]]의 개수는?"),
    choices=CH_NUM("30", "32", "34", "36", "38"),
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔)·합성함수 적용 표기 텍스트 혼합",
    note="출처 [2019년 6월 고3 문과 21번/4점]. f(n-1)=f(n)=f(n+1)인 n (주기 8·우함수) 전수 확인 → 30개 → ① = 빠른정답 ✓.")

# p78
add(id="902dd056", qtype="short",
    question=("두 함수 [[f(x) = x + 6]],\n[[g(x)]] = { [[-2x - 5]] ([[x < 0]]) ; [[pow(x, 2) - 6 a x - 5]] ([[x >= 0]]) }에 대하여\n"
              "합성함수 [[comp(f, g)]]의 치역이 [[setb(y, y >= -35)]]일 때, 상수 [[a]]의\n값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔) 텍스트 혼합",
    note="g의 최솟값 -41 = -9a²-5 (a>0) → a=2. 빠른정답 1과 불일치.")

# p82
add(id="d476c238", qtype="short",
    question=("두 함수 [[f(x) = x + 10]],\n[[g(x)]] = { [[-3x - 7]] ([[x < 0]]) ; [[pow(x, 2) - 8 a x - 7]] ([[x >= 0]]) }에 대하여\n"
              "합성함수 [[comp(f, g)]]의 치역이 [[setb(y, y >= -61)]]일 때, 상수 [[a]]의\n값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔) 텍스트 혼합",
    note="g의 최솟값 -71 = -16a²-7 (a>0) → a=2 = 빠른정답 ✓.")

# p84
add(id="d02a9b02", qtype="short",
    question=("두 함수\n[[f(x)]] = { [[pow(x, 2) + 4 a x + 5]] ([[x < 0]]) ; [[x + 5]] ([[x >= 0]]) }, [[g(x) = x + 4]]에\n"
              "대하여 합성함수 ([[comp(g, f)]])([[x]])의 치역이 [[setb(y, y >= 5)]]일 때,\n[[f(a)]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔)·합성함수 적용 표기 텍스트 혼합",
    note="f의 최솟값 1 = 5-4a² (a>0) → a=1 → f(1)=6. 빠른정답 4와 불일치.")

# p85
add(id="ac042f4d", qtype="choice",
    question=("[[0 <= x <= 4]]에서 정의된 두 함수 [[y = f(x)]], [[y = g(x)]]의\n그래프가 아래와 같다. 다음 중 함수 [[y]] = ([[comp(g, f)]])([[x]])의\n그래프의 개형은?\n[그림 1] [[y = f(x)]] / [그림 2] [[y = g(x)]]"),
    choices=["그래프: 원점에서 출발해 가파르게 오르다 꺾여 완만하게 올라 가운데에서 최대가 되고, 대칭으로 내려와 [[x]]축에 닿는 개형",
             "그래프: [[y]]축 위 높은 점에서 출발해 내려와 [[x]]축에 닿았다가 다시 올라가는 V자 개형",
             "그래프: 원점에서 출발해 올라가 봉우리, 가운데에서 살짝 내려앉았다가 다시 봉우리, 내려와 [[x]]축에 닿는 M자 개형",
             "그래프: [[y]]축 위 높은 점에서 출발해 [[x]]축까지 내려와 가운데에서 작은 봉우리를 이루고 다시 [[x]]축에 닿았다가 올라가는 W자 개형",
             "그래프: 원점에서 출발해 봉우리, 가운데에서 [[x]]축에 닿고 다시 봉우리를 이룬 뒤 [[x]]축에 닿는 두 봉우리 개형"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "[그림 1] y=f(x): (0,4)에서 (2,0)으로 내려가 (4,4)로 올라가는 V자 꺾은선. [그림 2] y=g(x): (0,4)에서 (2,3)으로 완만히 내려가 (4,0)으로 내려가는 꺾은선. 선지 ①~⑤는 그래프 개형 그림(선지 텍스트에 서술)"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 문항·선지 5개가 모두 그래프 그림(텍스트로 서술)",
    note="x=0: g(4)=0, x=1: g(2)=3, x=2: g(0)=4, 대칭 → 가파르게→완만하게 오르는 산 모양 → ①. 빠른정답 2와 불일치.")

# p93
add(id="112ee041", qtype="short",
    question=("[[0 <= x <= 4]]에서 정의된 함수 [[y = f(x)]]의 그래프가\n다음 그림과 같을 때, 방정식 ([[comp(f, f)]])([[x]]) = [[k x - k + 3]]의\n"
              "서로 다른 실근이 3개가 되도록 하는 실수 [[k]]의 값의 범위는\n[[a < k <= b]]이다. 이때 상수 [[a]], [[b]]에 대하여 [[b - a]]의 값을\n구하시오."),
    choices=None, derived_answer="frac(4, 3)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 y=f(x)의 그래프: 원점 O에서 (2,4)까지 올라간 뒤 (4,2)까지 내려가는 꺾은선; 눈금 2, 4와 점선 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프(함수가 그림에만 있음) / 합성함수 적용 표기 텍스트 혼합",
    note="(f∘f)의 그래프 (0,0)-(1,4)-(2,2)-(4,4), 직선은 (1,3) 지남 → -1<k≤1/3 → b-a=4/3 = 빠른정답 ✓.")

# ===================== 선분의 내분, 내분점의 좌표 =====================
# p9
add(id="52a9a0d1", qtype="short",
    question="네 점 [[A point(a, -2)]], [[B point(2, -a)]], [[C point(0, 0)]], [[D point(-2, -2)]]\n에 대하여 [[seg(AB) = 2 seg(CD)]]일 때, 양수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.85,
    note="AB²=2(a-2)²=32 → a=6 (양수). 빠른정답 4와 불일치.")

# p22
add(id="58cea9aa", qtype="short",
    question="좌표평면 위의 한 점 [[A point(3, -1)]]을 꼭짓점으로 하는\n삼각형 ABC의 외심은 변 BC위에 있고 좌표가\n[[point(-1, 2)]]일 때, [[pow(seg(AB), 2) + pow(seg(AC), 2)]]의 값을 구하시오.",
    choices=None, derived_answer="100", figure=None, difficulty_est=2, confidence=0.85,
    note="외심이 BC 위 → ∠A=90°, AB²+AC²=BC²=(2R)², R=5 → 100. 빠른정답 2와 불일치.")

# p28
add(id="44823c43", qtype="choice",
    question="두 점 [[O point(0, 0)]], [[A point(5, 12)]]와 임의의 점 P에 대하여\n[[seg(OP) + seg(PA)]]의 최솟값은?",
    choices=CH_NUM("10", "11", "12", "13", "14"),
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.85,
    note="OP+PA ≥ OA=13 → ④. 빠른정답 5와 불일치.")

# p29
add(id="4fbf7815", qtype="short",
    question="두 점 [[A point(a + 2, -5)]], [[B point(2a, 3 - a)]]와 임의의 점 P에\n대하여 [[seg(AP) + seg(PB)]]의 값이 최소일 때의 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.85,
    note="최솟값 AB, AB²=(a-2)²+(8-a)² 최소 → a=5 = 빠른정답 ✓.")

# p33
add(id="149bc79e", qtype="choice",
    question=("다음 그림과 같이 일직선 위의 세 점 A, B, C에 치킨집이 있고, 어느 한 지점에 양계장을 세우려고 한다. 닭 운반비용은 양계장에서 각 치킨집에 이르는 거리의 제곱의 합에 비례한다고 할 때, "
              "운반비용을 최소로 하는 양계장의 위치는? (단, [[2 seg(AB) = 3 seg(BC)]])"),
    choices=["[[seg(AB)]]의 중점", "[[seg(BC)]]의 중점", "[[seg(AC)]]의 중점", "[[seg(AB)]]를 [[ratio(8, 1)]]로 내분하는 점", "[[seg(BC)]]를 [[ratio(1, 2)]]로 내분하는 점"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "삽화: 왼쪽 아래에서 오른쪽 위로 향하는 직선 위에 집 모양 그림 세 개가 차례로 A, B, C"}}],
    difficulty_est=2, confidence=0.85,
    note="세 점의 무게중심: A=0, B=3, C=5 → 8/3 = AB를 8:1로 내분 → ④. 빠른정답 5와 불일치. 삽화는 장식 그림으로 처리.")

# p34
add(id="c6b0e013", qtype="short",
    question="세 점 [[A point(5, 4)]], [[B point(0, 2)]], [[C point(0, -2)]]를 꼭짓점으로 하는\n삼각형 ABC가 있다. 변 BC 위를 움직이는 점 P에\n대하여 [[pow(seg(AP), 2) + pow(seg(BP), 2)]]의 최솟값을 구하시오.",
    choices=None, derived_answer="29", figure=None, difficulty_est=2, confidence=0.85,
    note="P(0,t), -2≤t≤2: 2t²-12t+45는 t=2에서 최소 29. 빠른정답 5와 불일치.")

# p35
add(id="02edb145", qtype="choice",
    question="두 점 [[A point(1, 5)]], [[B point(5, 3)]]에 대하여 [[pow(seg(AP), 2) + pow(seg(BP), 2)]]의 값이\n최소가 되는 점 P의 좌표는?",
    choices=CH_NUM("point(4, 5)", "point(3, 4)", "point(2, 3)", "point(1, 2)", "point(0, 1)"),
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.85,
    note="AB의 중점 (3, 4) → ②. 빠른정답 3과 불일치.")

# p36
add(id="fdbf7f3e", qtype="short",
    question="두 점 [[A point(-2, 1)]], [[B point(8, 2)]]와 [[x]]축 위의 점 P에 대하여\n[[pow(seg(AP), 2) + pow(seg(BP), 2)]]의 최솟값을 구하시오.",
    choices=None, derived_answer="55", figure=None, difficulty_est=2, confidence=0.85,
    note="P(t,0): 2t²-12t+73, t=3에서 최소 55. 빠른정답 4와 불일치.")

# p37
add(id="1225ae4c", qtype="choice",
    question="두 점 [[A point(3, 1)]], [[B point(-1, 3)]]와 [[x]]축 위의 점 P에\n대하여 [[pow(seg(AP), 2) + pow(seg(BP), 2)]]의 최솟값은?",
    choices=CH_NUM("10", "12", "14", "16", "18"),
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="P(t,0): 2t²-4t+20, t=1에서 최소 18 → ⑤ = 빠른정답 ✓.")

# p41
add(id="9b2d8df1", qtype="choice",
    question=("다음 그림과 같이 세 도로가 만나는 지점을 각각 A, B, C라 할 때, 삼각형 ABC는 직각이등변삼각형이고 "
              "[[seg(AC) = seg(AB) = 2]]km, [[seg(BC) = 2 sqrt(2)]]km이다. 민아와 승우가 동시에 출발하여 민아는 A지점에서 C지점 방향으로 시속 1km의 속력으로 걷고 "
              "승우는 C지점에서 B지점 방향으로 시속 [[sqrt(2)]]km의 속력으로 걸을 때, 두 사람 사이의 직선거리의 최솟값은?"),
    choices=CH_NUM("frac(2 sqrt(3), 5)", "frac(2 sqrt(5), 5)", "frac(2 sqrt(7), 7)", "frac(3 sqrt(3), 5)", "frac(4 sqrt(5), 5)"),
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "세 직선 도로가 만나 이루는 삼각형 ABC: A 위(직각 표시), B 왼쪽 아래, C 오른쪽 아래. AB=2km, BC=2√2km 점선 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직각이등변삼각형 도로 그림",
    note="A 원점, 민아 (0,t), 승우 (t, 2-t) → 거리² 5t²-8t+4 최소 4/5 → 2√5/5 → ② = 빠른정답 ✓.")

# p42
add(id="8facbd43", qtype="short",
    question=("다음 그림과 같이 좌표평면 위의 두 점 [[A point(0, 3)]], [[B point(5, 0)]]을\n잇는 선분 AB를 한 변으로 하는 정사각형 ABCD에 대하여\n"
              "[[pow(seg(OC), 2)]]의 값을 구하시오.\n(단, O는 원점이고 점 C는 제1사분면 위의 점이다.)"),
    choices=None, derived_answer="89",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: A(0, 3)은 y축 위, B(5, 0)은 x축 위, 정사각형 ABCD가 제1사분면 쪽으로 세워짐(C 오른쪽 위, D 위쪽), 네 꼭짓점에 직각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 정사각형 그림",
    note="C = B + (3, 5) = (8, 5) → OC²=89. 빠른정답 2와 불일치.")

# p43
add(id="34584a34", qtype="choice",
    question=("다음은 직사각형 ABCD와 임의의 점 P에 대하여\n[[pow(seg(AP), 2) + pow(seg(CP), 2) = pow(seg(BP), 2) + pow(seg(DP), 2)]]이 성립함을 보인 것이다.\n(가)~(마)에 들어갈 말 중 옳지 않은 것은?\n"
              "다음 그림과 같이 직사각형 ABCD의 한 점 B를 원점으로, BC를 [[x]]축 잡으면 [[A point(0, b)]], [[B point(0, 0)]], [[C point(a, 0)]], [[D point(a, b)]]로 놓을 수 있다.\n"
              "이때 점 P의 좌표를 [[P point(x, y)]]라고 하면\n[[pow(seg(AP), 2) + pow(seg(CP), 2)]]\n= (가) + [[pow(x - a, 2) + pow(y, 2)]]\n= [[2 pow(x, 2) + 2 pow(y, 2) - 2 a x - 2 b y]] + (나) ⋯ ㉠\n"
              "[[pow(seg(BP), 2) + pow(seg(DP), 2)]]\n= [[pow(x, 2) + pow(y, 2)]] + (다)\n= [[2 pow(x, 2) + 2 pow(y, 2)]] + (라) + [[pow(a, 2) + pow(b, 2)]] ⋯ ㉡\n"
              "㉠, ㉡로부터 [[pow(seg(AP), 2) + pow(seg(CP), 2)]] = (마)"),
    choices=["(가) : [[pow(x, 2) + pow(y + b, 2)]]", "(나) : [[pow(a, 2) + pow(b, 2)]]", "(다) : [[pow(x - a, 2) + pow(y - b, 2)]]",
             "(라) : [[-2 a x - 2 b y]]", "(마) : [[pow(seg(BP), 2) + pow(seg(DP), 2)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 직사각형 ABCD(B(0,0) 원점, C(a,0), D(a,b), A(0,b)), 내부의 점 P(x,y), P에서 네 꼭짓점으로 선분"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 직사각형 그림 / 빈칸 상자 텍스트 혼합",
    note="(가)=AP²=x²+(y-b)² 이므로 ①이 틀림. 빠른정답 3과 불일치.")

# p45
add(id="ea1aab30", qtype="choice",
    question=("다음은 직사각형 ABCD와 임의의 점 P에 대하여\n[[pow(seg(AP), 2) + pow(seg(CP), 2) = pow(seg(BP), 2) + pow(seg(DP), 2)]]이 성립함을 보인 것이다.\n다음 중 (가)~(마)에 들어갈 말로 옳지 않은 것은?\n"
              "다음 그림과 같이 직사각형 ABCD의 한 변 BC를 [[x]]축, [[seg(BC)]]의 수직이등분선을 [[y]]축으로 잡으면 [[A point(-a, b)]], [[B point(-a, 0)]], [[C point(a, 0)]], [[D point(a, b)]]로 놓을 수 있다.\n"
              "이때 점 P의 좌표를 [[P point(x, y)]]라 하면\n[[pow(seg(AP), 2) + pow(seg(CP), 2)]] = (가) + (나)\n= [[2(pow(x, 2) + pow(y, 2) + pow(a, 2) - b y) + pow(b, 2)]] ⋯ ㉠\n"
              "[[pow(seg(BP), 2) + pow(seg(DP), 2)]] = (다) + (라)\n= [[2(pow(x, 2) + pow(y, 2) + pow(a, 2) - b y) + pow(b, 2)]] ⋯ ㉡\n"
              "㉠, ㉡에 의하여 [[pow(seg(AP), 2) + pow(seg(CP), 2)]] = (마)"),
    choices=["(가): [[pow(x + a, 2) + pow(y + b, 2)]]", "(나): [[pow(x - a, 2) + pow(y, 2)]]", "(다): [[pow(x + a, 2) + pow(y, 2)]]",
             "(라): [[pow(x - a, 2) + pow(y - b, 2)]]", "(마): [[pow(seg(BP), 2) + pow(seg(DP), 2)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 직사각형 ABCD(A(-a,b), B(-a,0), C(a,0), D(a,b)), y축이 BC의 수직이등분선, 내부의 점 P(x,y), P에서 네 꼭짓점으로 선분"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 직사각형 그림 / 빈칸 상자 텍스트 혼합",
    note="(가)=AP²=(x+a)²+(y-b)² 이므로 ①이 틀림. 빠른정답 89와 불일치.")

# p46
add(id="a0446b47", qtype="choice",
    question=("아래 그림은 한 변의 길이가 4인 정사각형 ABCD의\n내부에 한 변의 길이가 2인 정사각형 EFGH를 [[seg(AB)]]와\n[[seg(EF)]]가 평행하도록 그린 것이다. 네 사다리꼴 ABFE,\n"
              "BCGF, CDHG, DAEH의 넓이를 각각 [[sub(S,1)]], [[sub(S,2)]], [[sub(S,3)]],\n[[sub(S,4)]]라 할 때, 다음 보기 중 항상 옳은 것만을 있는 대로\n고른 것은?\n<보기>\n"
              "ㄱ. [[pow(seg(AE), 2) + pow(seg(CG), 2) = pow(seg(BF), 2) + pow(seg(DH), 2)]]\n"
              "ㄴ. [[seg(AE) = seg(BF)]]이면 [[seg(CG) = seg(DH)]]이다.\n"
              "ㄷ. [[sub(S,1) + sub(S,3) = sub(S,2) + sub(S,4)]]"),
    choices=["ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위) 안에 작은 정사각형 EFGH(E 왼쪽 위, F 왼쪽 아래, G 오른쪽 아래, H 오른쪽 위), 대응 꼭짓점끼리 선분 AE, BF, CG, DH로 연결. 사다리꼴 영역에 S₁(왼쪽), S₂(아래), S₃(오른쪽), S₄(위) 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 속 정사각형 그림",
    note="E(p, q+2), F(p, q) 좌표 설정: ㄱ 양변 모두 p²+q²+(2-p)²+(2-q)² ✓, ㄴ q=1이면 CG=DH ✓, ㄷ S₁+S₃=6=S₂+S₄ ✓ → ⑤. 빠른정답 1과 불일치.")

# p48
add(id="d452d130", qtype="choice",
    question=("다음은 예각삼각형 ABC에서 변 BC의 중점을 M이라 할 때,\n[[pow(seg(AB), 2) + pow(seg(AC), 2) = 2(pow(seg(BM), 2) + pow(seg(AM), 2))]]\n이 성립함을 증명한 것이다.\n"
              "[증명]\n점 A에서 선분 BC에 내린 수선의 발을 H라 하자.\n"
              "직각삼각형 ABH에서\n[[pow(seg(AB), 2) = pow(seg(BH), 2) + pow(seg(AH), 2)]]\n= ( (가) )² + [[pow(seg(AH), 2)]]\n= [[pow(seg(BM), 2) + 2 seg(BM) × seg(MH)]] + ( (나) )² ⋯ ㉠\n"
              "직각삼각형 AHC에서\n[[pow(seg(AC), 2) = pow(seg(CH), 2) + pow(seg(AH), 2)]]\n= ( (다) )² + [[pow(seg(AH), 2)]]\n= [[pow(seg(CM), 2) - 2 seg(CM) × seg(MH)]] + ( (나) )² ⋯ ㉡\n"
              "㉠, ㉡에서\n[[pow(seg(AB), 2) + pow(seg(AC), 2) = 2(pow(seg(BM), 2) + pow(seg(AM), 2))]]이다.\n"
              "이 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) [[seg(BC) + seg(CH)]], (나) [[seg(AM)]], (다) [[seg(BH) - seg(BM)]]",
             "(가) [[seg(BC) + seg(CH)]], (나) [[seg(AH)]], (다) [[seg(BH) - seg(BM)]]",
             "(가) [[seg(BM) + seg(MH)]], (나) [[seg(AM)]], (다) [[seg(BH) - seg(BM)]]",
             "(가) [[seg(BM) + seg(MH)]], (나) [[seg(AH)]], (다) [[seg(CM) - seg(MH)]]",
             "(가) [[seg(BM) + seg(MH)]], (나) [[seg(AM)]], (다) [[seg(CM) - seg(MH)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "예각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 변 BC 위에 중점 M과 수선의 발 H(M이 H보다 B쪽), 선분 AM, AH(직각 표시)"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 삼각형 그림 / 빈칸 상자의 제곱 ( (가) )² 텍스트 혼합",
    note="출처 [2007년 11월 고1 11번]. (가)=BM+MH, (나)=AM, (다)=CM-MH → ⑤. 빠른정답 1과 불일치. 선지는 (가)(나)(다) 표 형식을 한 줄로 나열.")

# p49
add(id="2d78d1af", qtype="short",
    question=("다음 그림과 같은 삼각형 ABC에서 [[seg(AB) = 14]], [[seg(BC) = 18]],\n[[seg(CA) = 12]]이고, 변 BC의 삼등분점 중 점 B에 가까운\n점부터 차례로 M, N이라 하자. 이때 [[pow(seg(AM), 2) + pow(seg(AN), 2)]]의\n값을 구하시오."),
    choices=None, derived_answer="196",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 변 BC 위의 삼등분점 M, N(같은 길이 표시), 선분 AM, AN; AB=14, CA=12, BC=18 점선 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 그림",
    note="스튜어트 정리: AM²=320/3, AN²=268/3 → 합 196. 빠른정답 3과 불일치.")

# p50
add(id="3715b4aa", qtype="short",
    question=("다음 그림과 같은 삼각형 ABC에서 [[seg(AB) = 2 sqrt(5)]],\n[[seg(BC) = 3 sqrt(10)]], [[seg(CA) = 3 sqrt(3)]]이고, 변 BC의 삼등분점 중\n점 B에 가까운 점부터 차례로 M, N이라 하자. 이때\n"
              "[[pow(seg(AM), 2) + pow(seg(AN), 2)]]의 값을 구하시오."),
    choices=None, derived_answer="7",
    figure=[{"fn": "unsupported", "args": {"raw": "납작한 삼각형 ABC(A 위 가운데, B 왼쪽, C 오른쪽), 변 BC 위의 삼등분점 M, N(같은 길이 표시), 선분 AM, AN; AB=2√5, CA=3√3, BC=3√10 점선 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 그림",
    note="스튜어트 정리: AM²=7/3, AN²=14/3 → 합 7. 빠른정답 112와 불일치.")

# p51
add(id="46cf2c36", qtype="short",
    question="다음 그림과 같이 삼각형 ABC의 무게중심 G에 대하여\n[[seg(AG) = 10]], [[seg(BG) = 8]], [[seg(CG) = 12]]일 때, 변 BC의 길이를\n[[l]]이라 하자. [[pow(l, 2)]]의 값을 구하시오.",
    choices=None, derived_answer="316",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래)와 세 중선, 무게중심 G; AG=10, BG=8, CG=12 점선 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형과 중선 그림",
    note="중선 15, 12, 18 → a²=(4/9)(2·144+2·324-225)=316 = 빠른정답 ✓.")

# p54
add(id="2c4a743c", qtype="short",
    question="수직선 위의 두 점 [[A(a)]], [[B(12)]]에 대하여 [[seg(AB)]]의 중점이\n[[M(3)]]일 때, [[a]]의 값을 구하시오.",
    choices=None, derived_answer="-6", figure=None, difficulty_est=1, confidence=0.85,
    note="(a+12)/2=3 → a=-6. 빠른정답 316과 불일치(앞 문항 답이 밀린 듯).")

# p62
add(id="d336c96c", qtype="choice",
    question=("두 점 [[A point(-3, -4)]], [[B point(5, 2)]]에 대하여 서로 다른 두\n점 [[sub(C,1)]], [[sub(C,2)]]가 다음 조건을 만족시킬 때, 삼각형 O[[sub(C,1)]][[sub(C,2)]]의\n넓이는? "
              "(단, O는 원점이고, 점 [[sub(C,1)]]의 [[x]]좌표는 점 [[sub(C,2)]]의\n[[x]]좌표보다 작다.)\n"
              "(가) 두 점 [[sub(C,1)]], [[sub(C,2)]]는 모두 직선 AB 위의 점이다.\n(나) [[seg(AB)]] = 3B[[sub(C,1)]], [[seg(AB)]] = 3B[[sub(C,2)]]"),
    choices=CH_NUM("frac(13, 3)", "frac(14, 3)", "5", "frac(16, 3)", "frac(17, 3)"),
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="첨자 점 라벨 C₁, C₂: 선분 BC₁, BC₂의 윗줄(seg) 표기 불가 → 텍스트 혼합",
    note="AB=10, BC₁=BC₂=10/3 → C₁(7/3, 0), C₂(23/3, 4) → 넓이 14/3 → ② = 빠른정답 ✓.")

# p63
add(id="989c49fd", qtype="choice",
    question=("세 꼭짓점의 좌표가 [[A point(0, 3)]], [[B point(-5, -9)]],\n[[C point(4, 0)]]인 삼각형 ABC가 있다. 그림과 같이\n[[seg(AC) = seg(AD)]]가 되도록 점 D를 선분 AB위에 잡는다.\n"
              "점 A를 지나면서 선분 DC와 평행인 직선이 선분 BC의\n연장선과 만나는 점을 P라 하자. 이 때, 점 P의 좌표는?"),
    choices=CH_NUM("point(frac(61, 8), frac(29, 8))", "point(frac(65, 8), frac(33, 8))", "point(frac(69, 8), frac(37, 8))", "point(frac(73, 8), frac(41, 8))", "point(frac(77, 8), frac(45, 8))"),
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(B 왼쪽 아래, A 위, C 오른쪽) 음영, 선분 AB 위의 점 D(AD=AC 같은 길이 표시), 선분 DC와 A를 지나는 평행선(화살표 표시)이 BC의 연장선과 만나는 점 P(오른쪽 위)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형과 평행선 그림",
    note="출처 [2013년 9월 고1 18번/4점]. AD=5, AB=13 → BP=(13/8)BC → P=(77/8, 45/8) → ⑤. 빠른정답 3과 불일치.")

# p72
add(id="661d3264", qtype="choice",
    question="세 점 [[A point(0, 0)]], [[B point(1, 0)]], [[C point(1, 2)]]에 대하여\n[[pow(seg(PA), 2) + pow(seg(PB), 2) + pow(seg(PC), 2)]]의 값이 최소가 되도록 하는 점 P의\n좌표는?",
    choices=CH_NUM("P point(-frac(2, 3), frac(1, 3))", "P point(-frac(1, 3), -frac(2, 3))", "P point(frac(1, 3), frac(1, 3))", "P point(frac(2, 3), frac(2, 3))", "P point(frac(2, 3), 1)"),
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="무게중심 (2/3, 2/3) → ④ = 빠른정답 ✓.")

# p80
add(id="fe47742b", qtype="choice",
    question=("세 꼭짓점이 [[A point(-1, -1)]], [[B point(4, 3)]], [[C point(0, 1)]]인\n[[tri(ABC)]]에서 [[seg(AB)]], [[seg(BC)]], [[seg(CA)]]를 [[ratio(2, 3)]]으로 내분하는 점을\n"
              "각각 D, E, F라 하자. [[tri(DEF)]]의 무게중심을 [[point(a, b)]]라 할\n때, [[a + b]]의 값은?"),
    choices=CH_NUM("-2", "-1", "0", "1", "2"),
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    note="△DEF의 무게중심 = △ABC의 무게중심 (1, 1) → a+b=2 → ⑤. 빠른정답 2와 불일치(선지 번호 기준).")

# p82
add(id="e303eaff", qtype="choice",
    question=("다음 그림과 같이 좌표평면 위의 세 점 [[A point(0, a)]], [[B point(-4, 0)]],\n[[C point(1, 0)]]을 꼭짓점으로 하는 삼각형 ABC가 있다.\n"
              "[[angle(ABC)]]의 이등분선이 선분 AC와 수직일 때, 양수 [[a]]의\n값은?"),
    choices=CH_NUM("sqrt(6)", "sqrt(7)", "2 sqrt(2)", "3", "sqrt(10)"),
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: A는 y축 위, B는 x축 음의 부분, C는 x축 양의 부분, 삼각형 ABC와 B에서 나가는 각의 이등분선(같은 각 표시)이 AC와 직각으로 만남"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 삼각형과 각의 이등분선 그림",
    note="출처 [2020년 9월 고1 12번 변형]. 이등분선⊥AC → BA=BC=5 → 16+a²=25 → a=3 → ④. 빠른정답 2와 불일치.")

# p88
add(id="7a4aac0f", qtype="short",
    question="삼각형 ABC에서 변 BC를 [[ratio(2, 1)]]로 내분하는 점을 D라\n할 때, [[pow(seg(AB), 2) + 2 pow(seg(AC), 2) = k(pow(seg(AD), 2) + 2 pow(seg(DC), 2))]]을 만족시키는\n상수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.85,
    note="스튜어트 정리 → k=3 = 빠른정답 ✓.")

# p91
add(id="570b7480", qtype="choice",
    question=("두 직선 [[sub(l,1)]]: [[2x + y + 2 = 0]], [[sub(l,2)]]: [[x - 2y - 4 = 0]]의\n교점을 A, 두 직선 [[sub(l,1)]], [[sub(l,2)]]가 [[x]]축과 만나는 점을 각각\nB, C라 하자. 제1사분면에 있는 점 P와 삼각형 ABC의\n외접원 위의 점 Q가 다음 조건을 만족시킨다.\n"
              "(가) 점 Q는 삼각형 PBC의 무게중심이다.\n(나) 삼각형 PBC의 넓이는 삼각형 ABC의 넓이의\n3배이다.\n"
              "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 두 직선 [[sub(l,1)]], [[sub(l,2)]]는 서로 수직이다.\nㄴ. 점 Q의 [[y]]좌표는 2이다.\nㄷ. 점 P의 [[x]]좌표와 [[y]]좌표의 합은 10이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2022년 3월 고2 20번/4점]. A(0,-2), B(-1,0), C(4,0), 외접원 중심 (3/2,0) r=5/2; P의 y=6 → Q의 y=2 ✓; Q(3,2) → P(6,6) 합 12 → ㄷ ✗ → ③ = 빠른정답 ✓.")

# p97
add(id="a9376873", qtype="choice",
    question="두 점 [[A point(3, 0)]], [[B point(0, 2)]]에 대하여 [[pow(seg(PA), 2) - pow(seg(PB), 2) = 5]]를\n만족하는 점 P의 자취의 방정식은?",
    choices=CH_NUM("-3x + 2y + 9 = 0", "3x + 2y = 0", "6x - 4y + 9 = 0", "-3x + 2y = 0", "-6x + 4y - 5 = 0"),
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="-6x+4y+5=5 → -3x+2y=0 → ④ = 빠른정답 ✓.")

# p98
add(id="7bc73914", qtype="choice",
    question="아래 그림과 같이 한 변의 길이가 8인 정사각형 ABCD의\n내부의 점 P에 대하여 [[pow(seg(AP), 2) - pow(seg(BP), 2) = 32]]가 성립할 때,\n다음 중 점 P의 자취를 나타내는 것은?",
    choices=["정사각형 ABCD 안에서 변 AB에 수직이고(직각 표시) 변 BC에 평행한, B쪽에 가까운 가로 선분",
             "정사각형 ABCD 안에서 B와 C에서 출발해 가운데 위 한 점에서 만나는 꺾은선(∧ 모양)",
             "정사각형 ABCD 안에서 왼쪽 아래(B 근처)에서 오른쪽 위(D 근처)로 올라가는 기울어진 선분",
             "정사각형 ABCD 안에서 B와 C를 잇는 위로 볼록한 낮은 호",
             "정사각형 ABCD 안에서 왼쪽 아래에서 시작해 위로 볼록하게 올라갔다 오른쪽에서 내려오는 곡선"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 왼쪽 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위), AB=8, BC=8 점선 표시. 선지 ①~⑤는 정사각형 안에 자취를 그린 그림(선지 텍스트에 서술)"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 선지 5개가 모두 자취 그림(텍스트로 서술)",
    note="B 원점, A(0,8): AP²-BP²=-16y+64=32 → y=2 (AB에 수직인 직선) → ①. 빠른정답 20과 불일치.")

# ===================== 좌표평면에서 원과 직선의 위치 관계 =====================
# p2
add(id="b1662504", qtype="choice",
    question=("다음 그림과 같이\n두 원 [[sub(C,1)]]: [[pow(x, 2) + pow(y, 2) = 4]], [[sub(C,2)]]: [[pow(x, 2) + pow(y, 2) = 10]]이 있다.\n"
              "원 [[sub(C,1)]]에 접하는 직선 [[l]]의 방정식은 [[a x + b y + 2 = 0]]이다.\n"
              "직선 [[l]]에 평행하고 원 [[sub(C,2)]]에 접하는 두 직선을 각각 [[sub(l,1)]], [[sub(l,2)]]라\n"
              "하자. 점 [[sub(P,1)]][[point(sub(x,1), sub(y,1))]]은 직선 [[sub(l,1)]]위에 있고, [[sub(P,2)]][[point(sub(x,2), sub(y,2))]]는\n"
              "직선 [[sub(l,2)]]와 원 [[sub(C,2)]]의 접점이다.\n"
              "[[(a sub(x,1) + b sub(y,1) + 2)(a sub(x,2) + b sub(y,2) + 2)]]의 값은?"),
    choices=CH_NUM("-6", "-5", "-4", "-3", "-2"),
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O 중심의 두 동심원 C₁(안쪽), C₂(바깥쪽), 기울기 양수인 세 평행선 l₁(왼쪽 위, C₂와 접점 P₁), l(가운데, C₁에 접함), l₂(오른쪽 아래, C₂와 접점 P₂)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 동심원 두 개와 평행한 접선 세 개 그림",
    note="a²+b²=1, l₁·l₂: ax+by±√10=0 → (2-√10)(2+√10)=-6 → ① = 빠른정답 ✓.")

# p8
add(id="778bb054", qtype="choice",
    question="원 [[pow(x, 2) + pow(y, 2) + 3 a x + 3 b y - 25 = 0]]이 직선 [[y = m x]]와\n만나는 두 점을 P, Q라 할 때, [[seg(OP) × seg(OQ)]]의 값은?\n(단, [[a]], [[b]], [[m]]은 실수이고, O는 원점이다.)",
    choices=CH_NUM("23", "24", "25", "26", "27"),
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="원점의 방멱 |−25|=25 → ③. 빠른정답 1과 불일치.")

# p14
add(id="c9e9fa68", qtype="choice",
    question=("좌표평면에서 원 [[C]]: [[pow(x, 2) + pow(y, 2) - 4x - 2 a y + pow(a, 2) - 9 = 0]]\n이 다음 조건을 만족시킨다.\n"
              "(가) 원 [[C]]는 원점을 지난다.\n(나) 원 [[C]]는 직선 [[y = -2]]와 서로 다른 두 점에서\n만난다.\n"
              "원 [[C]]와 직선 [[y = -2]]가 만나는 두 점 사이의 거리는?\n(단, [[a]]는 상수이다.)"),
    choices=CH_NUM("4 sqrt(2)", "6", "2 sqrt(10)", "2 sqrt(11)", "4 sqrt(3)"),
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2019년 3월 고2 문과 17번/4점]. a=±3, (나)에서 a=-3, 중심 (2,-3) r=√13, 거리 1 → 현 2√12=4√3 → ⑤. 빠른정답 1과 불일치.")

# p25
add(id="d4c25e8c", qtype="choice",
    question=("좌표평면에서 원 [[C]]: [[pow(x, 2) + pow(y, 2) - 6x - 2 a y + pow(a, 2) - 25 = 0]]\n이 다음 조건을 만족시킨다.\n"
              "(가) 원 [[C]]는 원점을 지난다.\n(나) 원 [[C]]는 직선 [[y = -1]]과 서로 다른 두 점에서\n만난다.\n"
              "원 [[C]]와 직선 [[y = -1]]이 만나는 두 점 사이의 거리는?\n(단, [[a]]는 상수이다.)"),
    choices=CH_NUM("8", "2 sqrt(17)", "6 sqrt(2)", "2 sqrt(19)", "4 sqrt(5)"),
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2019년 3월 고2 문과 17번 변형]. a=-5, 중심 (3,-5) r=√34, 거리 4 → 현 2√18=6√2 → ③ = 빠른정답 ✓.")

# p26
add(id="d689d068", qtype="short",
    question=("원 [[pow(x, 2) + pow(y, 2) - 12x + 20 = 0]] 밖의 점 P에서 이 원에 그은\n접선의 접점을 T라 하자. 점 [[A point(2, 6)]]에 대하여\n"
              "[[seg(PT) = seg(PA)]]를 만족시키는 점 P의 자취의 방정식이\n[[2x - a y + b = 0]]이다. [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="15", figure=None, difficulty_est=3, confidence=0.9,
    note="PT²=x²+y²-12x+20 = PA² → 2x-3y+5=0 → a=3, b=5 → 15 = 빠른정답 ✓.")

# p44
add(id="5c148ce4", qtype="choice",
    question=("실수 [[t]] ([[t > 0]])에 대하여 좌표평면 위에\n네 점 [[A point(1, 4)]], [[B point(5, 4)]], [[C point(2t, 0)]], [[D point(0, t)]]가 있다.\n"
              "선분 CD 위에 [[angle(APB) = deg(90)]]인 점 P가 존재하도록\n하는 [[t]]의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, [[M - m]]의\n값은?"),
    choices=CH_NUM("2 sqrt(5)", "frac(5 sqrt(5), 2)", "3 sqrt(5)", "frac(7 sqrt(5), 2)", "4 sqrt(5)"),
    derived_answer="①", figure=None, difficulty_est=4, confidence=0.8,
    note="출처 [2023년 11월 고1 20번/4점]. P는 AB를 지름으로 하는 원 (x-3)²+(y-4)²=4 위; 직선 CD: x+2y=2t와의 거리 |11-2t|/√5 ≤ 2 → t=(11±2√5)/2 (접점이 선분 CD 위에 있음 확인) → M-m=2√5 → ①. 빠른정답 30과 불일치.")

# p48
add(id="e71f5480", qtype="short",
    question=("좌표평면 위에 두 원\n[[sub(C,1)]]: [[pow(x + 4, 2) + pow(y, 2) = 4]], [[sub(C,2)]]: [[pow(x - 4, 2) + pow(y, 2) = 1]]과\n두 원 [[sub(C,1)]], [[sub(C,2)]]와 서로 만나지 않는\n"
              "직선 [[l]]: [[y = a x]] ([[a > 0]])이 있다. 원 [[sub(C,1)]] 위의 점 P에서\n직선 [[l]]에 내린 수선의 발을 [[sub(H,1)]], 원 [[sub(C,2)]] 위의 점 Q에서\n"
              "직선 [[l]]에 내린 수선의 발을 [[sub(H,2)]]라 하자. 선분 [[sub(H,1)]][[sub(H,2)]]의\n길이의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, [[M m = 23]]인\n[[a]]의 값을 구하시오."),
    choices=None, derived_answer="1",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: x축 음의 부분에 중심을 둔 큰 원 C₁(왼쪽), x축 양의 부분에 중심을 둔 작은 원 C₂(오른쪽), 원점을 지나는 직선 y=ax(기울기 양수)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 두 원과 직선 그림 / 첨자 점 라벨 H₁, H₂(선분 H₁H₂ 텍스트 혼합)",
    note="출처 [2020년 9월 고1 27번 변형]. 두 중심의 정사영 거리 d=8/√(1+a²), M=d+3, m=d-3 → d²-9=23 → d²=32 → a=1. 빠른정답 5와 불일치.")

# p50
add(id="7b8a6578", qtype="short",
    question=("행렬 [[A = mat(2,2, 2 - x, y + 1, y + 1, x - 2)]]가 있다. [[pow(A, 2) = 25 E]]를\n만족시키는 [[x]], [[y]]에 대하여 점 [[point(x, y)]]를 좌표평면 위에\n"
              "나타낼 때 만들어지는 도형을 [[S]]라 하자. 도형 [[S]] 위의\n점에서 직선 [[x - y + 9 = 0]] 까지의 거리의 최솟값을 [[m]],\n최댓값을 [[M]]이라 할 때, [[m M]]의 값을 구하시오."),
    choices=None, derived_answer="47", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2011년 9월 고2 이과 27번/4점]. A²=((x-2)²+(y+1)²)E → 원 중심 (2,-1) r=5, 중심-직선 거리 6√2 → mM=72-25=47. 빠른정답 2와 불일치. 행렬(구 교육과정) 소재이나 핵심은 원과 직선 거리.")

# p84
add(id="ccaeebf8", qtype="short",
    question="다음 그림과 같이 점 [[P point(3, 1)]]에서 원 [[pow(x, 2) + pow(y, 2) = 1]]에\n그은 두 접선의 접점을 각각 [[A point(0, 1)]], B라 할 때,\n점 A와 직선 BP 사이의 거리를 구하시오.",
    choices=None, derived_answer="frac(9, 5)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O 중심 반지름 1인 원, 점 P(3,1), 접선 y=1(접점 A(0,1))과 또 다른 접선(접점 B, 제4사분면), 삼각형 PAB 음영, P에서 x축까지 점선"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원과 접선 그림",
    note="B(3/5,-4/5), 직선 BP: 3x-4y-5=0 → 거리 9/5 = 빠른정답 ✓.")

# p92
add(id="e1c4c3db", qtype="choice",
    question=("그림과 같이 좌표평면에 원 [[C]]: [[pow(x, 2) + pow(y, 2) = 4]]와\n점 [[A point(-2, 0)]]이 있다. 원 [[C]] 위의 제1사분면 위의\n"
              "점 P에서의 접선이 [[x]]축과 만나는 점을 B, 점 P에서\n[[x]]축에 내린 수선의 발을 H라 하자. [[2 seg(AH) = seg(HB)]]일 때,\n삼각형 PAB의 넓이는?"),
    choices=CH_NUM("frac(10 sqrt(2), 3)", "4 sqrt(2)", "frac(14 sqrt(2), 3)", "frac(16 sqrt(2), 3)", "6 sqrt(2)"),
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O 중심 원 C, x축 위의 점 A(왼쪽 교점), 제1사분면의 점 P, P에서의 접선이 x축과 만나는 점 B(오른쪽 멀리), P에서 x축에 내린 수선의 발 H(직각 표시), 선분 AP"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원과 접선·삼각형 그림",
    note="출처 [2020년 11월 고1 20번/4점]. P(p,q): B(4/p,0), 2(p+2)=4/p-p → p=2/3, q=4√2/3, AB=8 → 넓이 16√2/3 → ④. 빠른정답 60과 불일치.")

# p93
add(id="c456a20c", qtype="short",
    question=("원 [[O]]가 [[x]]축과 두 점 A, B에서 만나고, [[y]]축과\n두 점 C, D에서 만난다. 네 점 A, B, C, D와 원 [[O]]가\n다음 조건을 만족시킬 때, 사각형 ACBD의 넓이를 [[S]]라\n하자. [[pow(S, 2)]]의 값을 구하시오.\n"
              "(단, 점 A의 [[x]]좌표는 점 B의 [[x]]좌표보다 작고, 점 C의\n[[y]]좌표는 점 D의 [[y]]좌표보다 작다.)\n"
              "(가) 선분 AB를 [[ratio(1, 3)]]으로 내분하는 점은\n선분 CD의 중점이다.\n(나) 원 [[O]]가 직선 [[3x + 4y + 14 = 0]]에 접한다."),
    choices=None, derived_answer="768", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2025년 10월 고1 28번 변형]. 중심 (h,0), r=2h, |3h+14|/5=2h → h=2, r=4 → A(-2,0), B(6,0), CD=4√3 → S=16√3 → S²=768 = 빠른정답 ✓.")

# p96
add(id="9bf487dc", qtype="choice",
    question=("다음 그림과 같이 좌표평면에 원 [[C]]: [[pow(x, 2) + pow(y, 2) = 9]]와\n점 [[A point(-3, 0)]]이 있다. 원 [[C]]위의 제1사분면 위의 점\n"
              "P에서의 접선이 [[x]]축과 만나는 점을 B, 점 P에서 [[x]]축에\n내린 수선의 발을 H라 하자. [[3 seg(AH) = seg(HB)]]일 때,\n삼각형 PAB의 넓이는?"),
    choices=CH_NUM("frac(41 sqrt(15), 8)", "frac(21 sqrt(15), 4)", "frac(43 sqrt(15), 8)", "frac(11 sqrt(15), 2)", "frac(45 sqrt(15), 8)"),
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점 O 중심 원 C, x축 위의 점 A(왼쪽 교점), 제1사분면의 점 P, P에서의 접선이 x축과 만나는 점 B(오른쪽 멀리), P에서 x축에 내린 수선의 발 H(직각 표시), 선분 AP"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원과 접선·삼각형 그림",
    note="출처 [2020년 11월 고1 20번 변형]. P(p,q): 3(p+3)=9/p-p → p=3/4, q=3√15/4, AB=15 → 넓이 45√15/8 → ⑤. 빠른정답 1과 불일치.")

# ===================== 함수의 개념과 그래프 =====================
# p5
add(id="5ede9f22", qtype="choice",
    question="두 집합 [[X = set(-1, 0, 1)]], [[Y = set(0, 1, 2)]]에\n대하여 다음 중 [[X]]에서 [[Y]]로의 함수인 것을 모두\n고르면? (정답 2개)",
    choices=["[[x]] → [[x + 2]]", "[[x]] → [[x]]", "[[x]] → [[pow(x, 2) + 1]]", "[[x]] → [[abs(x) - 1]]", "[[x]] → [[pow(x, 2)]]"],
    derived_answer="③, ⑤", figure=None, difficulty_est=1, confidence=0.85,
    note="③ 상: 2,1,2 ⊂ Y ✓, ⑤ 상: 1,0,1 ✓; ① 3∉Y, ② -1∉Y, ④ -1∉Y → ③, ⑤ (정답 2개, 빠른정답 없음).")

# p6
add(id="cfdf6670", qtype="choice",
    question="두 집합 [[X = set(-1, 0, 1)]], [[Y = set(0, 1, 2, 3)]]에\n대하여 다음 대응 중 [[X]]에서 [[Y]]로의 함수가 아닌 것을\n모두 고르면?",
    choices=["[[x]] → [[abs(x) + 1]]", "[[x]] → [[x + 2]]", "[[x]] → [[pow(x, 3) + 3]]", "[[x]] → [[pow(x, 2) + x + 1]]",
             "[[x]] → { [[x - 1]] ([[x >= 0]]) ; [[-x - 1]] ([[x < 0]]) }"],
    derived_answer="③, ⑤", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 선지 ⑤의 조각적 정의(경우 나눔) 텍스트 혼합",
    note="③ x=1 → 4∉Y, ⑤ x=0 → -1∉Y → 함수 아님 ③, ⑤ (빠른정답 없음).")

# p18
add(id="50bdf5f2", qtype="choice",
    question="집합 [[A]] = {0, 1, 2, ⋯}에 대하여 함수 [[f]]: [[A]]→[[A]]를\n[[f(x)]] = ([[3 pow(x, 2)]]을 6으로 나누었을 때의 나머지)로 정의할 때,\n함수 [[f]]의 치역은?",
    choices=CH_NUM("set(0)", "set(3)", "set(0, 1)", "set(0, 3)", "set(0, 1, 2)"),
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.85,
    note="x 짝수 → 0, 홀수 → 3 → {0, 3} → ④. 빠른정답 19와 불일치.")

# p21
add(id="c6798587", qtype="choice",
    question="[[X = set(0, 1, 2, 3, 4, 5)]], [[Y]] = { [[y]] | [[y]]는 정수 }일 때,\n함수 [[f]]: [[X]]→[[Y]]가 [[f(x)]] = ([[pow(x, 2)]]을 5로 나눈 나머지)로\n정의할 때, 함수 [[f]]의 치역에 있는 모든 원소의 합은?",
    choices=CH_NUM("5", "6", "7", "8", "9"),
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.85,
    note="x²을 5로 나눈 나머지: 0,1,4,4,1,0 → 치역 {0,1,4} 합 5 → ① (빠른정답 없음).")

# p22
add(id="4bb1672a", qtype="choice",
    question="임의의 두 양수 [[x]], [[y]]에 대하여 [[f(x y) = f(x) + f(y)]]\n이고 [[f(3) = 1]]일 때, [[f(27)]]의 값은?",
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.85,
    note="f(27)=3f(3)=3 → ③ (빠른정답 없음).")

# p29
add(id="b536f150", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6, 7, 8)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[f]]의 치역의 원소의 개수는 7이다.\n(나) [[f(1) + f(2) + f(3) + f(4) + f(5) + f(6) + f(7) + f(8) = 42]]\n(다) 함수 [[f]]의 치역의 원소 중 최댓값과 최솟값의\n차는 6이다.\n"
              "집합 [[X]]의 어떤 두 원소 [[a]], [[b]]에 대하여 [[f(a) = f(b) = n]]\n을 만족하는 자연수 [[n]]의 값을 구하시오. (단, [[a != b]])"),
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2018년 11월 고1 28번/4점]. 치역 {2,…,8}(합 35) + 중복값 n = 42 → n=7 ({1,…,7}이면 n=14 불가). 빠른정답 없음.")

# p31
add(id="9e245d91", qtype="choice",
    question=("다음 보기 중 정의역이 [[set(-2, 0, 2)]]인 두 함수 [[f]], [[g]]가\n[[f = g]]를 만족하는 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(x) = pow(x, 2)]], [[g(x) = 2x]]\nㄴ. [[f(x) = 2 abs(x)]], [[g(x) = 2 sqrt(pow(x, 2))]]\nㄷ. [[f(x) = sqrt(pow(x, 2))]], [[g(x) = x]]"),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.85,
    note="ㄱ x=-2: 4≠-4 ✗, ㄴ 2|x|=2√x² ✓, ㄷ x=-2: 2≠-2 ✗ → ② (빠른정답 없음).")

# p54
add(id="15daba44", qtype="short",
    question=("집합 [[X = set(3, 4, 5, 6, 7, 8, 9)]]에 대하여\n함수 [[f]] : [[X]] → [[X]]는 일대일 대응이다. [[3 <= n <= 7]]인\n"
              "모든 자연수 [[n]]에 대하여 [[f(n) f(n + 2)]]의 값이\n짝수일 때, [[f(3) + f(4)]]의 최댓값을 구하시오."),
    choices=None, derived_answer="17", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2018년 3월 고2 이과 27번 변형]. 전수 확인(순열 5040개): 최댓값 17 (f(3)=8, f(4)=9). 빠른정답 없음.")

# p55 (id 2개 — 같은 문항; draft_a가 보기를 별개 항목으로 쪼갰던 것)
dup(["71c3475d", "cbd91a53"], qtype="choice",
    question=("두 실수 [[a]], [[b]]와 두 함수 [[f(x) = -pow(x, 2) - 4x + 4]],\n[[g(x) = pow(x, 2) - 4x - 4]]에 대하여 함수 [[h(x)]]를\n"
              "[[h(x)]] = { [[f(x)]] ([[x < a]]) ; [[g(x + 2b)]] ([[x >= a]]) }라 하자. 함수 [[h(x)]]가\n"
              "실수 전체의 집합에서 실수 전체의 집합으로의\n일대일대응이 되도록 하는 [[a]], [[b]]의 모든 순서쌍 [[point(a, b)]]만을\n"
              "원소로 하는 집합을 [[A]]라 할 때, 다음 보기 중 옳은 것만을\n있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[in(point(-1, k), A)]]를 만족시키는 실수 [[k]]는 존재하지\n않는다.\n"
              "ㄴ. [[in(point(-2, 4), A)]]\n"
              "ㄷ. 집합 [[B]] = { [[m + b]] | [[in(point(m, b), A)]]이고 [[m]]은 정수 }\n에 대하여 [[in(frac(-1 + sqrt(15), 2), B)]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔) 텍스트 혼합",
    note="a≤-2, a+2b≥2, g(a+2b)=f(a)=8-(a+2)² → -6≤a≤-2. ㄱ a=-1은 f가 단조 아님 ✓, ㄴ (-2,4): g(6)=8=f(-2) ✓, ㄷ m=-3일 때 m+b=(-1+√15)/2 ✓ → ⑤. 빠른정답 'E'와 불일치(표기 문제). 한 이미지에 id 2개 → 동일 전사.")

# p57
add(id="97e21e9d", qtype="short",
    question=("집합 [[X = set(7, 8, 9, 10, 11)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]는 일대일대응이다. [[7 <= n <= 9]]인\n"
              "모든 자연수 [[n]]에 대하여 [[f(n) f(n + 2)]]의 값이 짝수일 때,\n[[f(7) f(11)]]의 최댓값을 구하시오."),
    choices=None, derived_answer="99", figure=None, difficulty_est=3, confidence=0.9,
    note="전수 확인(순열 120개): f(9) 짝수 등 → 최댓값 9×11=99 = 빠른정답 ✓.")

# p61
add(id="81050c19", qtype="choice",
    question=("두 실수 [[a]], [[b]]와 두 함수 [[f(x) = -pow(x, 2) - 4x - 2]],\n[[g(x) = pow(x, 2) - 4x + 2]]에 대하여 함수 [[h(x)]]를\n"
              "[[h(x)]] = { [[f(x)]] ([[x < a]]) ; [[g(x + b)]] ([[x >= a]]) }라 하자.\n"
              "함수 [[h(x)]]가 실수 전체의 집합에서 실수 전체의\n집합으로의 일대일대응이 되도록 하는 [[a]], [[b]]의 모든 순서쌍\n"
              "[[point(a, b)]]만을 원소로 하는 집합을 [[A]]라 할 때, 다음 보기 중\n옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[in(point(-3, k), A)]]를 만족시키는 실수 [[k]]는 존재한다.\n"
              "ㄴ. [[in(point(-2, 6), A)]]\n"
              "ㄷ. 집합 { [[m b]] | [[in(point(m, b), A)]]이고 [[m]]은 정수 }의 모든\n원소 중 정수의 합은 [[-36]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="문법 범위 밖: 조각적 정의(경우 나눔) 텍스트 혼합",
    note="출처 [2022년 11월 고1 21번 변형]. -4≤a≤-2, b=2+√(4-(a+2)²)-a. ㄱ a=-3: b=5+√3 ✓, ㄴ (-2,6) ✓, ㄷ m=-4: -24, m=-2: -12 (m=-3은 무리수) → 합 -36 ✓ → ⑤. 빠른정답 없음.")
