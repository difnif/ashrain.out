# -*- coding: utf-8 -*-
# esc_sonnet_m3-1_3of6 — 이미지 기준 전사 (89 항목 / 80쪽)
# 인수분해 공식 · 이차함수의 식 구하기 · 이차방정식과 그 해 · 이차방정식의 활용 · y=ax²+q · y=a(x-p)² · 인수분해를 이용한 이차방정식의 풀이
# 규약: 빈칸 상자는 □(텍스트), (가)(나)…는 텍스트. 이차함수 그래프 그림은 unsupported + "도형 표현 불가" 한 구절.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))
def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
def M(*xs): return ["[[%s]]" % x for x in xs]
FIG = "도형 표현 불가: "

# ======================================================================
# 인수분해 공식
# ======================================================================
# ---------------- p6
add(id="243f4c74", qtype="choice",
    question="[[9 pow(x,2) + A x y + 16 pow(y,2) = pow(B x + C y, 2)]]일 때, 이를 만족하는 세 자연수 [[A]], [[B]], [[C]]의 합은?",
    choices=M("28", "29", "30", "31", "32"), derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="B=3, C=4, A=2·3·4=24 → 합 31 → ④. 빠른정답 36과 불일치.")

# ---------------- p7
add(id="712913e4", qtype="choice",
    question="[[16 pow(x,2) - 24 x y + 9 pow(y,2)]]을 인수분해하면?",
    choices=M("pow(x - 3y, 2)", "pow(x + 3y, 2)", "pow(3x + 4y, 2)", "pow(4x + 3y, 2)", "pow(4x - 3y, 2)"),
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="(4x−3y)² → ⑤ = 빠른정답 ✓.")

# ---------------- p12
add(id="79149744", qtype="choice",
    question="[[frac(1,2) pow(x,2) - 3x]] + □가 완전제곱식이 되기 위한 □의 값은?",
    choices=M("9", "frac(9,2)", "frac(9,4)", "6", "4"), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(1/2)(x²−6x+9) → □=9/2 → ② = 빠른정답 ✓.")

# ---------------- p13
add(id="fbf877f8", qtype="short",
    question="[[36 pow(x,2) + a x + 4]]가 완전제곱식일 때, 양수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="24", figure=None, difficulty_est=1, confidence=0.9,
    note="a=2·6·2=24. 빠른정답 25와 불일치.")

# ---------------- p22
add(id="f950f205", qtype="choice",
    question="[[-3 pow(a,2) + 12 pow(b,2) = k(m a + n b)(m a - n b)]]일 때,\n세 정수 [[k]], [[m]], [[n]]의 곱 [[k m n]]의 값은? (단, [[n > 0]])",
    choices=M("5", "6", "-6", "-4", "-5"), derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="−3(a+2b)(a−2b) → k=−3, m=1, n=2 → kmn=−6 → ③ (m=−1도 형식상 가능하나 통상 m=1). 빠른정답 1과 불일치.")

# ---------------- p27
add(id="209868b8", qtype="short",
    question="[[9 pow(x,2) - 64 pow(y,2) = (A x + B y)(A x - B y)]]일 때, [[A + B]]의 값을 구하시오.\n(단, [[A > 0]], [[B > 0]]이고 [[A]], [[B]]는 상수)",
    choices=None, derived_answer="11", figure=None, difficulty_est=1, confidence=0.9,
    note="A=3, B=8 → 11 = 빠른정답 ✓.")

# ---------------- p50
add(id="5f578f49", qtype="choice",
    question="다항식 [[a pow(x,2) + b x - 30]]을 인수분해하면\n[[(x + 6)(2x + c)]]일 때, [[a + b + c]]의 값은?\n(단, [[a]], [[b]], [[c]]는 상수)",
    choices=M("1", "2", "3", "4", "5"), derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="6c=−30 → c=−5, a=2, b=7 → 4 → ④. 빠른정답 9와 불일치.")

# ---------------- p51
add(id="2829c48b", qtype="short",
    question="[[x]], [[y]]에 관한 등식 [[3 pow(x,2) + 20 x y - 7 pow(y,2) = 0]]이\n[[x y > 0]]을 만족할 때, [[frac(y, x)]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="(3x−y)(x+7y)=0, xy>0 → y=3x → y/x=3 = 빠른정답 ✓.")

# ---------------- p54
add(id="6024bae6", qtype="choice",
    question="다음 중 [[9 pow(x,2) + 16 x y - 4 pow(y,2)]]의 인수는?",
    choices=M("x - 2y", "x + 2y", "3x + 2y", "9x - 4y", "9x + 2y"), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(9x−2y)(x+2y) → 인수 x+2y → ②. 빠른정답 3과 불일치.")

# ---------------- p56
add(id="4fb26b75", qtype="short",
    question="[[6 pow(x,2) - 7 x y - 3 pow(y,2) = (a x + b y)(c x + y)]]가 성립할 때,\n정수 [[a]], [[b]], [[c]]에 대하여 [[a - b + c]]의 값을 구하시오.",
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="(2x−3y)(3x+y) → a=2, b=−3, c=3 → 8. 빠른정답 2와 불일치.")

# ---------------- p57
add(id="5bd55177", qtype="short",
    question="[[10 pow(x,2) - 13 x y - 3 pow(y,2) = (a x + b y)(c x + y)]]가 성립할 때,\n정수 [[a]], [[b]], [[c]]에 대하여 [[a - b + c]]의 값을 구하시오.",
    choices=None, derived_answer="10", figure=None, difficulty_est=2, confidence=0.9,
    note="(2x−3y)(5x+y) → a=2, b=−3, c=5 → 10 = 빠른정답 ✓.")

# ---------------- p59
add(id="9c15899e", qtype="choice",
    question="[[7 pow(x,2) + a x y + 21 pow(y,2)]]을 인수분해하면 [[(x - 3y)(7x + b y)]]일\n때, [[a - b]]의 값은? (단, [[a]], [[b]]는 상수)",
    choices=M("-27", "-25", "-23", "-21", "-19"), derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="−3b=21 → b=−7, a=b−21=−28 → a−b=−21 → ④. 빠른정답 8과 불일치.")

# ---------------- p62
add(id="1851a077", qtype="choice",
    question="다음 중 인수분해가 바르게 된 것은?",
    choices=M("4 pow(a,2) - 2 a b = 2a(a - b)", "pow(x,2) + 20x - 100 = pow(x + 10, 2)", "-pow(x,2) + 1 = (x + 1)(-x - 1)",
              "pow(x,2) - 7x + 12 = (x - 2)(x - 6)", "10 pow(x,2) + 23x - 21 = (x + 3)(10x - 7)"),
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="⑤ (x+3)(10x−7)=10x²+23x−21 ✓, 나머지 오류 → ⑤. 빠른정답 4와 불일치.")

# ---------------- p64 (id 5개)
dup(["fe2d6eab", "8bc6af45", "feb426b3", "dc944a26", "e3669b5c"], qtype="choice",
    question="다음 중 □ 안에 알맞은 수가 가장 작은 것은?",
    choices=["[[3 x y + 12x]] = [[3x]]([[y]] + □)",
             "[[16 pow(x,2) - 8x + 1]] = (□[[x]] − 1)²",
             "[[36 pow(x,2) - 25 pow(y,2)]] = [[(6x + 5y)]]([[6x]] − □[[y]])",
             "[[pow(x,2) + 2x - 8]] = [[(x - 2)]]([[x]] + □)",
             "[[10 pow(x,2) + 13 x y - 3 pow(y,2)]] = [[(5x - y)]]([[2x]] + □[[y]])"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    note="□: ① 4 ② 4 ③ 5 ④ 4 ⑤ 3 → 가장 작은 것 ⑤. 빠른정답 2와 불일치. 빈칸 상자는 □ 텍스트로 조각 표기.")

# ---------------- p65 (id 5개, 보기 ㄱ~ㅁ에서 고르는 단답형)
dup(["838f3871", "da3689f6", "63694dfe", "3a238307", "a9d946c7"], qtype="short",
    question=("다음 보기의 식을 인수분해하였을 때, 빈 칸에 들어갈 값이 다른 것을 고르시오.\n<보기>\n"
              "ㄱ. [[2 pow(x,2) + 4x + 2]] = [[2]]([[x]] + □)²\n"
              "ㄴ. [[pow(x,2) - 6x + 9]] = (□[[x]] − 3)²\n"
              "ㄷ. [[3 pow(x,2) + 6x - 9]] = [[3(x + 3)]]([[x]] − □)\n"
              "ㄹ. [[6 pow(x,2) - x - 1]] = ([[2x]] − □)[[(3x + 1)]]\n"
              "ㅁ. [[pow(x,2) - 7x + 10]] = [[(x - 5)]]([[x]] − □)"),
    choices=None, derived_answer="ㅁ", figure=None, difficulty_est=2, confidence=0.85,
    note="ㄱ 1, ㄴ 1, ㄷ 1, ㄹ 1, ㅁ 2 → ㅁ. 빠른정답 5(다섯째 항목)와 표기만 다름. 빈칸 상자는 □ 텍스트로 조각 표기.")

# ---------------- p75
add(id="15d80be7", qtype="choice",
    question="두 이차식 [[16 pow(x,2) - 4 pow(y,2)]], [[2 pow(x,2) + 5 x y - 3 pow(y,2)]]의 공통인수는?",
    choices=M("2x - y", "2x + y", "x + 3y", "4(2x - y)", "x + y"), derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="4(2x+y)(2x−y), (2x−y)(x+3y) → 공통인수 2x−y → ①. 빠른정답 2와 불일치.")

# ---------------- p81
add(id="8b0c11b7", qtype="short",
    question="[[8 pow(x,2) + a x y - 21 pow(y,2)]]이 [[4x + 3y]]로 나누어떨어질 때,\n상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="-22", figure=None, difficulty_est=2, confidence=0.9,
    note="(4x+3y)(2x−7y)=8x²−22xy−21y² → a=−22 = 빠른정답 ✓.")

# ---------------- p86 (대화 상자 + 비밀번호 칸)
add(id="414251eb", qtype="short",
    question=("다음 지현이와 준석이의 대화를 읽고 지현이네 집 현관문 비밀번호를 구하시오.\n"
              "지현: 우리 집 현관문 비밀번호는 [[A]] [[B]] [[C]] [[D]] 네 개의 숫자로 이루어져 있어.\n"
              "준석: 힌트 좀 줘.\n"
              "지현: [[(A x - B)(x + 6)]]을 전개하면 [[3 pow(x,2) + 16x - 12]]이고 [[pow(x,2) + C x - 7]]을 인수분해하면 [[(x + D)(x - 1)]]이야."),
    choices=None, derived_answer="3267",
    figure=[{"fn": "table", "args": {"rows": [["A", "B", "C", "D"]]}}],
    difficulty_est=2, confidence=0.9,
    note="A=3, B=2, D=7, C=6 → 3267 = 빠른정답 ✓. 비밀번호 네 칸(A|B|C|D)은 1행 표로.")

# ---------------- p89
add(id="83cc170d", qtype="choice",
    question="[[pow(a,2)]] + □[[a]] − 24가 [[a]]의 계수가 1이고 상수항이 정수인\n두 일차식의 곱으로 인수분해될 때, □ 안에 들어갈 수\n없는 정수는?",
    choices=M("-23", "10", "-6", "-5", "2"), derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="곱이 −24인 두 정수의 합: ±23, ±10, ±5, ±2 → −6 불가 → ③ = 빠른정답 ✓.")

# ======================================================================
# 이차함수의 식 구하기
# ======================================================================
# ---------------- p3
add(id="a3a9f8ea", qtype="short",
    question="다음 그림과 같이 이차함수 [[y = -frac(1,3) pow(x,2) + a x + b]]의\n그래프가 [[x]]축과 두 점 [[point(-3, 0)]], [[point(k, 0)]]에서 만날 때, [[k]]의\n값을 구하시오. (단, [[a]], [[b]]는 상수)",
    choices=None, derived_answer="6",
    figure=U("좌표평면: 위로 볼록한 포물선, y절편 6, x절편 −3(왼쪽)과 k(오른쪽), 원점 O"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "이차함수 그래프(y절편 6이 그림에만 표시)",
    note="b=6, (−3,0) 대입 a=1 → y=−(1/3)(x+3)(x−6) → k=6 = 빠른정답 ✓.")

# ---------------- p5
add(id="b8555747", qtype="short",
    question="다음 그림과 같이 이차함수 [[y = -frac(1,2) pow(x,2) + a x + b]]의\n그래프가 [[x]]축과 두 점 [[point(k, 0)]], [[point(4, 0)]]에서 만날 때, [[k]]의\n값을 구하시오. (단, [[a]], [[b]]는 상수)",
    choices=None, derived_answer="-6",
    figure=U("좌표평면: 위로 볼록한 포물선, y절편 12, x절편 k(왼쪽)과 4(오른쪽), 원점 O"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "이차함수 그래프(y절편 12가 그림에만 표시)",
    note="b=12, (4,0) 대입 a=−1 → y=−(1/2)(x+6)(x−4) → k=−6. 빠른정답 −1과 불일치.")

# ---------------- p8
add(id="4881331f", qtype="choice",
    question="이차함수 [[y = -pow(x,2) + a x + b]]의 그래프가 [[x]]축과 두 점\n[[point(-1, 0)]], [[point(-4, 0)]]에서 만날 때, 꼭짓점의 좌표는?",
    choices=M("point(-frac(1,2), frac(1,4))", "point(-frac(1,3), frac(5,4))", "point(-5, frac(9,4))", "point(-2, 3)", "point(-frac(5,2), frac(9,4))"),
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="y=−(x+1)(x+4)=−(x+5/2)²+9/4 → 꼭짓점 (−5/2, 9/4) → ⑤. 빠른정답 2와 불일치.")

# ---------------- p14
add(id="5531638b", qtype="choice",
    question="이차함수 [[y = a pow(x,2) + q]]의 그래프가 두 점 [[point(1, -1)]],\n[[point(2, -7)]]을 지날 때, [[a q]]의 값은? (단, [[a]], [[q]]는 상수)",
    choices=M("-2", "-1", "0", "1", "2"), derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="a+q=−1, 4a+q=−7 → a=−2, q=1 → aq=−2 → ①. 빠른정답 2와 불일치.")

# ---------------- p21
add(id="e1733c2c", qtype="short",
    question="다음 그림은 이차함수 [[y = a pow(x - p, 2) + q]]의 그래프이다.\n[[a p q]]의 값을 구하시오.",
    choices=None, derived_answer="-4",
    figure=U("좌표평면: 아래로 볼록한 포물선, 꼭짓점 (2, −3)(x=2·y=−3 점선 표시), 점 (5, 3)(점선 표시)을 지남, 원점 O 부근을 지남"),
    difficulty_est=2, confidence=0.8, needs_review=FIG + "이차함수 그래프(꼭짓점 (2,−3)·점 (5,3)이 그림에만 표시)",
    note="p=2, q=−3, (5,3) 대입 9a−3=3 → a=2/3 → apq=−4. 빠른정답 3과 불일치.")

# ---------------- p34 (과정 상자)
add(id="555a3cf7", qtype="choice",
    question=("다음은 축의 방정식이 [[x = 1]]이고, 두 점 [[point(3, 6)]], [[point(5, 0)]]을\n지나는 포물선을 그래프로 하는 이차함수의 식을 구하는\n"
              "과정이다. (가)~(마)에 들어갈 값 또는 식이 바르지 않게\n짝지어진 것은?\n"
              "이차함수의 식을 [[y]] = [[a]]([[x]] − (가))² + [[q]]로\n놓자.\n"
              "위의 식에 두 점의 좌표를 각각 대입하면\n"
              "[[6]] = (나)[[a]] + [[q]], [[0]] = (다)[[a]] + [[q]]\n"
              "[[a = -frac(1,2)]], [[q]] = (라)\n"
              "따라서 이차함수의 식은 (마)"),
    choices=["(가) [[1]]", "(나) [[4]]", "(다) [[16]]", "(라) [[-8]]", "(마) [[y = -frac(1,2) pow(x - 1, 2) + 8]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)1 (나)4 (다)16, 6=4a+q, 0=16a+q → a=−1/2, q=8 → (라)는 8이어야 함 → ④. 빠른정답 1과 불일치. 빈칸 (가)~(마)는 텍스트 조각 표기.")

# ---------------- p40
add(id="d45293f8", qtype="choice",
    question="다음 그림은 직선 [[x = -1]]을 축으로 하는 이차함수\n[[y = a pow(x,2) + b x + c]]의 그래프이다. 이때 상수 [[a]], [[b]], [[c]]에\n대하여 [[a b c]]의 값은?",
    choices=M("-8", "-2", "2", "4", "8"), derived_answer="③",
    figure=U("좌표평면: 위로 볼록한 포물선, 축 x=−1(세로 점선, 위에 x=−1 표시), y절편 4, x절편 −4 표시, 원점 O"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "이차함수 그래프(y절편 4·x절편 −4가 그림에만 표시)",
    note="x절편 −4, 2 → y=−(1/2)(x+4)(x−2) → a=−1/2, b=−1, c=4 → abc=2 → ③. 빠른정답 1과 불일치.")

# ---------------- p41
add(id="d66b22a5", qtype="short",
    question="이차함수 [[y = pow(x,2) + b x + c]]의 그래프는 축의 방정식이\n[[x = -3]]이고 원점을 지난다. 이때 상수 [[b]], [[c]]에 대하여\n[[b + c]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="−b/2=−3 → b=6, c=0 → 6 = 빠른정답 ✓.")

# ---------------- p51
add(id="cca512bf", qtype="short",
    question="이차함수 [[y = a pow(x,2) + b x + c]]의 그래프가 세 점\n[[point(0, 12)]], [[point(-2, -2b)]], [[point(1, 1 - 4a)]]를 지날 때,\n[[a - b + c]]의 값을 구하여라.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="c=12, 4a−2b+12=−2b → a=−3, a+b+c=1−4a → b=4 → a−b+c=5 = 빠른정답 ✓.")

# ---------------- p52
add(id="96f22316", qtype="short",
    question="이차함수 [[y = a pow(x,2) + b x + c]]의 그래프가 세 점 [[point(0, 2)]],\n[[point(1, b + 5)]], [[point(-1, 4a - 1)]]을 지날 때, [[a + b + c]]의 값을\n구하시오.",
    choices=None, derived_answer="-1", figure=None, difficulty_est=2, confidence=0.9,
    note="c=2, a+b+2=b+5 → a=3, a−b+2=4a−1 → b=−6 → a+b+c=−1 = 빠른정답 ✓.")

# ---------------- p56 (과정 상자)
add(id="e36649e6", qtype="choice",
    question=("다음은 세 점 [[point(0, 4)]], [[point(2, -2)]], [[point(6, 10)]]을 지나는\n포물선을 그래프로 하는 이차함수의 식을\n"
              "[[y = a pow(x,2) + b x + c]] 꼴로 나타내는 과정이다. (가)~(마)에\n들어갈 값 또는 식이 바르지 않게 짝지어진 것은?\n(단, [[a]], [[b]], [[c]]는 상수)\n"
              "이차함수의 식을 [[y = a pow(x,2) + b x + c]]로 놓으면\n"
              "이 그래프가 점 [[point(0, 4)]]를 지나므로 [[c]] = (가)\n"
              "즉, [[y = a pow(x,2) + b x]] + (가) 의 그래프가\n"
              "점 [[point(2, -2)]]를 지나므로 [[-2 = 4a + 2b]] + (가)\n"
              "∴ (나)[[a]] + [[b]] = [[-3]]\n"
              "점 [[point(6, 10)]]을 지나므로\n"
              "[[10 = 36a + 6b]] + (가)\n"
              "∴ (다)[[a]] + [[b]] = [[1]]\n"
              "[[a]], [[b]]에 대한 두 식을 연립하면 풀면\n"
              "[[a = 1]], [[b]] = (라)\n"
              "따라서 이차함수의 식은 (마)"),
    choices=["(가) [[4]]", "(나) [[2]]", "(다) [[6]]", "(라) [[-3]]", "(마) [[y = pow(x,2) - 5x + 4]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(가)4 (나)2 (다)6, 2a+b=−3, 6a+b=1 → a=1, b=−5 → (라)는 −5 → ④ = 빠른정답 ✓. 원문 '연립하면 풀면' 그대로. 빈칸은 텍스트 조각 표기.")

# ---------------- p91
add(id="6daa2dde", qtype="short",
    question=("다음 그림과 같이 두 이차함수 [[y = pow(x - 1, 2)]],\n[[y = a pow(x - p, 2) + q]]의 그래프가 서로의 꼭짓점을 지난다.\n"
              "[[y = a pow(x - p, 2) + q]]의 그래프의 꼭짓점을 A, 점 A에서\n[[x]]축과 평행한 직선을 그어 [[y = pow(x - 1, 2)]]의 그래프와\n"
              "만나는 점을 B라 할 때, [[seg(AB) = 6]]이다. 상수 [[a]], [[p]], [[q]]에\n대하여 [[a p q]]의 값을 구하시오. (단, [[p < 1]])"),
    choices=None, derived_answer="18",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=(x−1)²(꼭짓점 x축 위)과 위로 볼록한 포물선 y=a(x−p)²+q(꼭짓점 A, 제2사분면)가 서로의 꼭짓점을 지남, A에서 x축에 평행한 선분 AB(B는 y=(x−1)² 위 오른쪽), 원점 O"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "두 포물선+선분 AB 그래프",
    note="A(p,q), q=(p−1)², B(2−p,q), AB=2−2p=6 → p=−2, q=9, (1,0) 대입 a=−1 → apq=18 = 빠른정답 ✓.")

# ---------------- p92
add(id="16bcbf60", qtype="short",
    question=("다음 그림과 같이 두 이차함수 [[y = 2 pow(x - 2, 2)]],\n[[y = a pow(x - p, 2) + q]]의 그래프가 서로의 꼭짓점을 지난다.\n"
              "[[y = a pow(x - p, 2) + q]]의 그래프의 꼭짓점을 A, 점 A에서\n[[x]]축과 평행한 직선을 그어 [[y = 2 pow(x - 2, 2)]]의 그래프와\n"
              "만나는 점을 B라 할 때, [[seg(AB) = 5]]이다. 상수 [[a]], [[p]], [[q]]에\n대하여 [[8 a p q]]의 값을 구하시오. (단, [[p < 2]])"),
    choices=None, derived_answer="100",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=2(x−2)²(꼭짓점 x축 위)과 위로 볼록한 포물선 y=a(x−p)²+q(꼭짓점 A, y축 바로 왼쪽 위)가 서로의 꼭짓점을 지남, A에서 x축에 평행한 선분 AB(B는 y=2(x−2)² 위 오른쪽), 원점 O"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "두 포물선+선분 AB 그래프",
    note="A(p,q), q=2(p−2)², B(4−p,q), AB=4−2p=5 → p=−1/2, q=25/2, (2,0) 대입 a=−2 → 8apq=100 = 빠른정답 ✓.")

# ---------------- p93
add(id="8b22a827", qtype="short",
    question=("다음 그림과 같이 두 이차함수 [[y = pow(x - 3, 2)]],\n[[y = a pow(x - p, 2) + q]]의 그래프가 서로의 꼭짓점을 지난다.\n"
              "[[y = a pow(x - p, 2) + q]]의 그래프의 꼭짓점을 A, 점 A에서\n[[x]]축과 평행한 직선을 그어 [[y = pow(x - 3, 2)]]의 그래프와\n"
              "만나는 점을 B라 할 때, [[seg(AB) = 4]]이다. 상수 [[a]], [[p]], [[q]]에\n대하여 [[a p q]]의 값을 구하시오. (단, [[p < 3]])"),
    choices=None, derived_answer="-4",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=(x−3)²(꼭짓점 x축 위)과 위로 볼록한 포물선 y=a(x−p)²+q(꼭짓점 A, 제1사분면 y축 근처)가 서로의 꼭짓점을 지남, A에서 x축에 평행한 선분 AB(B는 y=(x−3)² 위 오른쪽), 원점 O"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "두 포물선+선분 AB 그래프",
    note="A(p,q), q=(p−3)², B(6−p,q), AB=6−2p=4 → p=1, q=4, (3,0) 대입 a=−1 → apq=−4 = 빠른정답 ✓.")

# ---------------- p98 [2024년 3월 고1 29번/4점]
add(id="86227965", qtype="short",
    question=("그림과 같이 양수 [[a]]에 대하여 꼭짓점이 [[A(-3, -a)]]이고\n점 [[B(1, 0)]]을 지나는 이차함수 [[y = f(x)]]의 그래프와\n"
              "꼭짓점이 [[C(3, 3a)]]인 이차함수 [[y = g(x)]]의 그래프가\n있다. 점 A에서 [[x]]축에 내린 수선의 발을 D라 할 때,\n"
              "사각형 ABCD의 넓이는 16이다. 이차함수 [[y = g(x)]]의\n그래프가 [[y]]축과 만나는 점이 선분 CD 위에 있을 때,\n"
              "[[f(-1) × g(-3)]]의 값을 구하시오."),
    choices=None, derived_answer="9",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=f(x)(꼭짓점 A, x축 아래 왼쪽)와 위로 볼록한 포물선 y=g(x)(꼭짓점 C, 제1사분면), D는 A에서 x축에 내린 수선의 발(직각 표시), B는 x축 위 원점 오른쪽, 사각형 ABCD(변 AB·BC·CD·DA)와 선분 CD·AC 표시, 원점 O"),
    difficulty_est=4, confidence=0.85, needs_review=FIG + "두 포물선+사각형 ABCD 그래프",
    note="출처 [2024년 3월 고1 29번/4점]. □ABCD 넓이 8a=16 → a=2, f(x)=(1/8)(x+3)²−2 → f(−1)=−3/2, CD: y=x+3 → g(0)=3 → g(x)=−(1/3)(x−3)²+6 → g(−3)=−6 → 곱 9 = 빠른정답 ✓.")

# ---------------- p99
add(id="720cc400", qtype="short",
    question=("다음 그림과 같이 직선 [[y = k]]가 두 이차함수\n[[y = -pow(x + 2, 2) + 7]], [[y = -pow(x - p, 2) + q]]의 그래프와 세\n"
              "점 A, B, C에서 만난다. 점 B는 [[y]]축 위에 있고\n[[frac(1,2) seg(AB) = seg(BC)]]일 때, [[k + p + q]]의 값을 구하시오.\n"
              "(단, [[k]], [[p]], [[q]]는 상수이고 [[p > 0]], [[q > 0]]이다.)"),
    choices=None, derived_answer="8",
    figure=U("좌표평면: 위로 볼록한 큰 포물선 y=−(x+2)²+7(왼쪽)과 위로 볼록한 작은 포물선 y=−(x−p)²+q(오른쪽), 수평 직선 y=k가 A(왼쪽 포물선 위), B(y축 위, 두 포물선의 교점), C(오른쪽 포물선 위)에서 만남, 원점 O"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "두 포물선+직선 y=k 그래프",
    note="B(0,3) → k=3, A(−4,3), AB=4 → BC=2 → C(2,3) → 축 p=1, q=4 → k+p+q=8 = 빠른정답 ✓.")

# ======================================================================
# 이차방정식과 그 해
# ======================================================================
# ---------------- p1 (○× 판정형)
add(id="adfb907b", qtype="short",
    question="다음 식이 이차방정식이면 '○'를, 아니면 '×'를 고르시오.\n[[pow(x,2) - 4x = 2 pow(x,3)]]\n① ○ ② ×",
    choices=None, derived_answer="②", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="선지 2개(○× 판정형, 5지 규격 밖) — 보기를 본문에 텍스트로 포함",
    note="2x³−x²+4x=0 삼차 → 이차방정식 아님 → × → ② = 빠른정답 ✓.")

# ---------------- p8
add(id="91b4c690", qtype="choice",
    question="다음 중 방정식 [[(a x + 1)(2x - 3) = 6 pow(x,2) + 2x]]가 [[x]]에\n대한 이차방정식이 되도록 하는 상수 [[a]]의 값이 아닌 것은?",
    choices=M("-2", "-1", "1", "2", "3"), derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="(2a−6)x²+… → a≠3 → ⑤ = 빠른정답 ✓.")

# ---------------- p11
add(id="f2a1f199", qtype="choice",
    question="이차방정식 [[(2x + 1)(5x - 2) = 3x(x + 4)]]를\n[[7 pow(x,2) + a x + b = 0]]의 꼴로 나타낼 때, 상수 [[a]], [[b]]에\n대하여 [[a - b]]의 값은?",
    choices=M("-9", "-7", "-5", "-3", "-1"), derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="10x²+x−2=3x²+12x → 7x²−11x−2=0 → a−b=−9 → ① = 빠른정답 ✓.")

# ---------------- p15
add(id="97f4965c", qtype="short",
    question="이차방정식 [[pow(x - 2, 2) = (2x + 3)(x - 1)]]을\n[[pow(x,2) + a x + b = 0]]의 꼴로 나타낼 때, [[a - b]]의 값을\n구하시오. (단, [[a]], [[b]]는 정수)",
    choices=None, derived_answer="12", figure=None, difficulty_est=2, confidence=0.9,
    note="x²−4x+4=2x²+x−3 → x²+5x−7=0 → a−b=12 = 빠른정답 ✓.")

# ---------------- p39 (id 2개, 정답 2개)
dup(["0d3164c0", "67d1a175"], qtype="choice",
    question="다음 이차방정식 중에서 [ ] 안의 수가 해가 되는 것을\n모두 고르면? (정답 2개)",
    choices=["[[pow(x - 3, 2) = 4x]] [1]", "[[(x + 2)(x - 3) = 14]] [−1]", "[[pow(x,2) + 2x - 3 = 0]] [3]",
             "[[pow(x,2) = -4x + 12]] [−2]", "[[2x(x - 3) = 0]] [0]"],
    derived_answer="①, ⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="① x=1: 4=4 ✓ ② −4≠14 ③ 12≠0 ④ 4≠20 ⑤ 0=0 ✓ → ①, ⑤. 빠른정답 1(하나만 기재)과 부분 일치. [ ]는 텍스트.")

# ---------------- p45
add(id="2e260e3b", qtype="choice",
    question="[[x]]가 [[-2]], [[-1]], 0, 1, 2일 때,\n이차방정식 [[(x + 2)(x - 4) = -3x - 2]]의 해는?",
    choices=M("x = -2", "x = -1", "x = 0", "x = 1", "x = 2"), derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="x²+x−6=0 → x=2 (−3은 범위 밖) → ⑤. 빠른정답 3과 불일치.")

# ---------------- p53
add(id="07ee0de1", qtype="short",
    question="[[x]]에 관한 이차방정식 [[2 a pow(x,2) + p x - a p + 4q = 0]]이 [[a]]의\n값에 관계없이 항상 [[x = 1]]의 근을 가질 때, [[p + q]]의 값을\n구하시오.",
    choices=None, derived_answer="frac(3,2)", figure=None, difficulty_est=3, confidence=0.9,
    note="x=1 대입 a(2−p)+(p+4q)=0 항등 → p=2, q=−1/2 → 3/2 = 빠른정답 ✓.")

# ---------------- p61 [2010년 3월 고1 3번]
add(id="bf46ce4c", qtype="choice",
    question="이차방정식 [[2 pow(x,2) + m x - 10 = 0]]의\n한 근이 2일 때, 상수 [[m]]의 값은?",
    choices=M("-frac(5,2)", "-2", "1", "2", "frac(5,2)"), derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2010년 3월 고1 3번]. 8+2m−10=0 → m=1 → ③ = 빠른정답 ✓.")

# ---------------- p69
add(id="25127e73", qtype="short",
    question="이차방정식 [[3 pow(x,2) + a x + b = 0]]의 두 근이 1, 3일 때,\n[[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="-3", figure=None, difficulty_est=2, confidence=0.9,
    note="3(x−1)(x−3)=3x²−12x+9 → a=−12, b=9 → −3. 빠른정답 6과 불일치.")

# ---------------- p71
add(id="0d3c5cc2", qtype="short",
    question="이차방정식 [[2 pow(x,2) + m x - n = 0]]의 한 근이 [[x = -1]]이고\n이차방정식 [[2 pow(x,2) + 3 m x + 2n = 0]]의 한 근이 [[x = 2]]일 때,\n상수 [[m]], [[n]]에 대하여 [[m n]]의 값을 구하시오.",
    choices=None, derived_answer="-15", figure=None, difficulty_est=2, confidence=0.9,
    note="m+n=2, 3m+n=−4 → m=−3, n=5 → mn=−15 = 빠른정답 ✓.")

# ---------------- p75
add(id="7b28c3e3", qtype="short",
    question="이차방정식 [[4 pow(x,2) + a x + 5 = 0]]의 한 근이 [[x = frac(1,2)]]이고\n이차방정식 [[5 pow(x,2) - x + b = 0]]의 한 근이 [[x = 1]]일 때,\n[[b - a]]의 값을 구하시오. (단, [[a]], [[b]]는 상수)",
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="1+a/2+5=0 → a=−12, 5−1+b=0 → b=−4 → b−a=8. 빠른정답 6과 불일치.")

# ---------------- p80
add(id="2a4c7850", qtype="choice",
    question="[[pow(x,2) - sqrt(7) x + 1 = 0]]의 한 근을 [[alpha]]라 할 때, [[alpha - frac(1, alpha)]]의\n값은?",
    choices=M("pm(1)", "0", "pm(sqrt(3))", "pm(sqrt(2))", "pm(sqrt(7))"), derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="α+1/α=√7 → (α−1/α)²=7−4=3 → ±√3 → ③. 빠른정답 4와 불일치.")

# ---------------- p98
add(id="3c6fb798", qtype="short",
    question="이차방정식 [[3 pow(x,2) + 4x - 2 = 0]]의 두 근을 [[alpha]], [[beta]]라 하고\n[[f(n) = pow(alpha, n) + pow(beta, n)]]이라 할 때,\n[[3f(n + 2) + 4f(n + 1) - 2f(n)]]의 값을 구하시오.\n(단, [[n]]은 자연수이다.)",
    choices=None, derived_answer="0", figure=None, difficulty_est=3, confidence=0.9,
    note="αⁿ(3α²+4α−2)+βⁿ(3β²+4β−2)=0 → 0. 빠른정답 4와 불일치.")

# ---------------- p99 (이미지에 별개 문항 2개, id는 1개 → 첫 문항 전사)
add(id="bf92a8db", qtype="short",
    question="이차방정식 [[5 pow(x,2) + x - 1 = 0]]의 두 근을 [[alpha]], [[beta]]라 하고\n[[f(n) = pow(alpha, n) + pow(beta, n)]]이라 할 때,\n[[5f(n + 2) + f(n + 1) - f(n)]]의 값을 구하시오.\n(단, [[n]]은 자연수이다.)",
    choices=None, derived_answer="0", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="이미지에 별개 문항 2개(id 1개): 첫 문항만 전사 — 둘째 문항(이차방정식 5x²−(4a+3)x−5=0의 한 근 x=k에 대하여 k−1/k=a일 때 상수 a의 값은? ①1 ②2 ③3 ④4 ⑤5, 답 ③) 미전사",
    note="αⁿ(5α²+α−1)+βⁿ(5β²+β−1)=0 → 0. 빠른정답 1과 불일치.")

# ======================================================================
# 이차방정식의 활용
# ======================================================================
# ---------------- p5 (무한 연분수)
add(id="620bdeb9", qtype="short",
    question="5 + 6/(5 + 6/(5 + 6/(5 + ⋯)))의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.75,
    needs_review="문법 범위 밖: 무한 연분수(줄임표 ⋯가 최내측 분모 안에 있어 frac 중첩으로 표기 불가) — 텍스트 혼합 표기",
    note="원문은 5 + 6/(5 + 6/(5 + 6/(5 + ⋯))) 꼴의 겹분수. x=5+6/x → x²−5x−6=0 → x=6(양수). 빠른정답 '심우각형'은 정렬 오류.")

# ---------------- p39
add(id="f3b5e3f8", qtype="choice",
    question=("다음은 언니는 동생보다 3살 많고 동생의 나이의 제곱은\n언니의 나이의 4배와 같을 때, 동생의 나이를 구하는\n이차방정식을 세우는 과정이다. (가), (나), (다)에 알맞은\n것을 차례대로 나열하면?\n"
              "동생의 나이를 [[x]]살이라 하면 언니의 나이는\n(가) 살이다.\n"
              "[[x]]에 대한 이차방정식을 세우면\n[[pow(x,2)]] = [[4]]((나))이므로\n[[pow(x,2) - 4x]] − (다) = 0이다."),
    choices=["[[x + 1]], [[x + 1]], [[4]]", "[[x + 3]], [[x - 3]], [[12]]", "[[x + 3]], [[x + 3]], [[12]]",
             "[[4x]], [[4x]], [[4]]", "[[4x]], [[4x]], [[12]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="언니 x+3, x²=4(x+3) → x²−4x−12=0 → ③. 빠른정답 15와 불일치. 빈칸은 텍스트 조각 표기.")

# ---------------- p40
add(id="63cea0f2", qtype="choice",
    question=("다음은 언니는 동생보다 4살 많고 동생의 나이의 제곱은\n언니의 나이의 2배와 같을 때, 동생의 나이를 구하는\n이차방정식을 세우는 과정이다. □ 안에 알맞은 것을\n차례대로 나열하면?\n"
              "동생의 나이를 [[x]]살이라 하면 언니의 나이는\n□살이다.\n"
              "[[x]]에 대한 이차방정식을 세우면\n[[pow(x,2)]] = [[2]](□)이므로\n[[pow(x,2) - 2x]] − □ = 0이다."),
    choices=["[[x + 2]], [[x + 2]], [[6]]", "[[x + 4]], [[x + 4]], [[8]]", "[[x + 4]], [[x - 4]], [[8]]",
             "[[4x]], [[4x]], [[6]]", "[[4x]], [[4x]], [[8]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="언니 x+4, x²=2(x+4) → x²−2x−8=0 → ②. 빠른정답 '팔각형'은 정렬 오류. 빈칸은 □ 텍스트.")

# ---------------- p41
add(id="7edcdade", qtype="choice",
    question=("다음은 언니는 동생보다 6살 많고 동생의 나이의 제곱은\n언니의 나이의 3배와 같을 때, 동생의 나이를 구하는\n이차방정식을 세우는 과정이다. □ 안에 알맞은 것을\n차례대로 나열하면?\n"
              "동생의 나이를 [[x]]살이라 하면 언니의 나이는\n□살이다.\n"
              "[[x]]에 대한 이차방정식을 세우면\n[[pow(x,2)]] = [[3]](□)이므로\n[[pow(x,2) - 3x]] − □ = 0이다."),
    choices=["[[x - 6]], [[x - 6]], [[-18]]", "[[x - 6]], [[x + 6]], [[-18]]", "[[x + 6]], [[x + 6]], [[9]]",
             "[[x + 6]], [[x + 6]], [[18]]", "[[6x]], [[6x]], [[18]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="언니 x+6, x²=3(x+6) → x²−3x−18=0 → ④ = 빠른정답 ✓. 빈칸은 □ 텍스트.")

# ---------------- p56 (직각삼각형 도형)
add(id="94767976", qtype="choice",
    question=("다음 그림과 같이 [[angle(C) = deg(90)]], [[seg(BC) = 10]] cm,\n[[seg(AC) = 16]] cm인 직각삼각형이 있다. 빗변 AB 위의 한 점\n"
              "P에서 [[seg(BC)]], [[seg(AC)]]에 내린 수선의 발을 각각 Q, R라 할 때,\n삼각형 PQR의 넓이가 [[20]] cm²가 되도록 하는 [[seg(PQ)]]의\n길이는?"),
    choices=["[[2]] cm", "[[4]] cm", "[[6]] cm", "[[8]] cm", "[[10]] cm"], derived_answer="④",
    figure=U("직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, C에 직각 표시), BC=10cm(아래 점선 치수), AC=16cm(오른쪽 점선 치수), 빗변 AB 위의 점 P에서 BC·AC에 내린 수선의 발 Q·R(직각 표시), △PQR 연두 음영"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "직각삼각형+수선 도형",
    note="PQ=h, PR=CQ=10−5h/8, (1/2)h(10−5h/8)=20 → h²−16h+64=0 → h=8 → ④. 빠른정답 7과 불일치.")

# ---------------- p85 (직사각형 동점 도형)
add(id="520d94c8", qtype="choice",
    question=("다음 그림과 같은 직사각형 ABCD에서 점 P는 점 A를\n출발하여 점 B까지 변 AB 위를 매초 [[2]] cm의 속력으로,\n"
              "점 Q는 점 B를 출발하여 점 C까지 변 BC 위를\n매초 [[4]] cm의 속력으로 움직인다. 두 점 P, Q가 동시에\n"
              "출발하였을 때, 출발한 지 몇 초 후에 오각형 APQCD의\n넓이가 처음으로 [[171]] cm²가 되는가?"),
    choices=["[[2]]초", "[[2.5]]초", "[[3]]초", "[[3.5]]초", "[[4]]초"], derived_answer="③",
    figure=U("직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD=15cm(위 점선 치수), DC=15cm(오른쪽 점선 치수), P는 AB 위(아래 방향 화살표), Q는 BC 위(오른쪽 방향 화살표), 오각형 APQCD 보라 음영"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "직사각형·동점 도형(변의 길이 15cm가 그림에만 표시)",
    note="정사각형 15×15: 225−(1/2)(15−2t)(4t)=171 → 2t²−15t+27=0 → t=3(4.5는 Q가 C 도달 후) → 처음 3초 → ③ = 빠른정답 ✓.")

# ======================================================================
# 이차함수 y=ax²+q의 그래프
# ======================================================================
# ---------------- p21
add(id="e6260b89", qtype="choice",
    question="이차함수 [[y = 2 pow(x,2) + 1]]의 그래프에서 축의 방정식과\n꼭짓점의 좌표를 차례대로 구하면?",
    choices=["[[x = 2]], [[point(1, 0)]]", "[[x = 1]], [[point(0, 2)]]", "[[x = 0]], [[point(0, 1)]]",
             "[[x = 0]], [[point(1, 0)]]", "[[x = 0]], [[point(2, 1)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="축 x=0, 꼭짓점 (0,1) → ③. 빠른정답 2와 불일치.")

# ---------------- p22
add(id="b0af7ecb", qtype="choice",
    question="이차함수 [[y = -pow(x,2) + 4]]의 그래프에서 꼭짓점의 좌표와\n축의 방정식을 구하면?",
    choices=["꼭짓점의 좌표 : [[point(0, 4)]], 축의 방정식 : [[x = 4]]",
             "꼭짓점의 좌표 : [[point(0, -4)]], 축의 방정식 : [[x = -4]]",
             "꼭짓점의 좌표 : [[point(0, 4)]], 축의 방정식 : [[x = 0]]",
             "꼭짓점의 좌표 : [[point(4, 0)]], 축의 방정식 : [[x = 4]]",
             "꼭짓점의 좌표 : [[point(4, 0)]], 축의 방정식 : [[x = 0]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="꼭짓점 (0,4), 축 x=0 → ③. 빠른정답 −4와 불일치.")

# ---------------- p38 (선지가 그래프 그림)
add(id="4e6634df", qtype="choice",
    question="다음 중 이차함수 [[y = frac(1,2) pow(x,2) - 2]]의 그래프로 옳은 것은?",
    choices=["(그림) 아래로 볼록한 포물선, 꼭짓점 [[point(0, 2)]]",
             "(그림) 위로 볼록한 포물선, 꼭짓점 [[point(0, 2)]]",
             "(그림) 아래로 볼록한 포물선, 꼭짓점 [[point(0, -2)]]",
             "(그림) 위로 볼록한 포물선, 꼭짓점 [[point(0, -2)]]",
             "(그림) 아래로 볼록한 포물선, 꼭짓점 [[point(-2, 0)]]"],
    derived_answer="③",
    figure=U("선지 ①~⑤가 각각 좌표평면 그래프 그림(원점 O, x·y축). ① 아래로 볼록, y축 위 2에 꼭짓점 ② 위로 볼록, 꼭짓점 (0,2) ③ 아래로 볼록, 꼭짓점 (0,−2) ④ 위로 볼록, 꼭짓점 (0,−2) ⑤ 아래로 볼록, 꼭짓점 (−2,0)"),
    difficulty_est=1, confidence=0.8, needs_review=FIG + "선지 5개가 모두 이차함수 그래프 그림(그림을 읽어 서술한 문구로 대체)",
    note="아래로 볼록, 꼭짓점 (0,−2) → ③. 빠른정답 1과 불일치.")

# ---------------- p41 (㉠~㉣ 그래프 고르기)
add(id="d679e9af", qtype="short",
    question="[[a < 0]], [[q < 0]]일 때, ㉠~㉣ 중 [[y = -a pow(x,2) + q]]의 그래프로\n알맞은 것을 고르시오. (단, [[a]], [[q]]는 상수)",
    choices=None, derived_answer=None,
    figure=U("좌표평면 위 포물선 4개(원점 O): ㉠ 초록, 아래로 볼록, 꼭짓점이 y축의 양의 부분 ㉡ 보라, 아래로 볼록, 꼭짓점이 y축의 음의 부분 ㉢ 빨강, 위로 볼록, 꼭짓점이 y축의 양의 부분 ㉣ 하늘색, 위로 볼록, 꼭짓점이 y축의 음의 부분"),
    difficulty_est=2, confidence=0.75,
    needs_review=FIG + "㉠~㉣ 포물선 4개 그래프 / 답 기호 ㉡이 답 문법 범위 밖이라 답 미도출 처리",
    note="−a>0 아래로 볼록, q<0 꼭짓점 아래 → ㉡(보라). 빠른정답 1과 불일치.")

# ---------------- p54
add(id="50b499af", qtype="short",
    question="다음 그림은 이차함수 [[y = 5 pow(x,2) + k]]의 그래프이다.\n[[seg(AB) = 8]]일 때, 상수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="-80",
    figure=U("좌표평면: 아래로 볼록한 좁은 포물선 y=5x²+k, x축과 A(왼쪽)·B(오른쪽)에서 만남, 꼭짓점 (0,k)는 x축 아래(k 표시), 원점 O"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "이차함수 그래프(x축 교점 A·B)",
    note="A, B는 y축 대칭 → x절편 ±4 → 5·16+k=0 → k=−80. 빠른정답 54와 불일치.")

# ---------------- p79
add(id="fd348e78", qtype="choice",
    question="이차함수 [[y = -pow(x,2) + 3]]의 그래프에 대한 다음 설명 중\n옳은 것은?",
    choices=["꼭짓점은 원점이다.", "대칭축이 [[y]]축이다.", "점 [[point(3, 0)]]을 지난다.", "아래로 볼록한 포물선이다.",
             "이차함수 [[y = pow(x,2) + 3]]의 그래프와 [[x]]축에 대하여\n대칭이다."],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="꼭짓점 (0,3), 축 y축 → ② = 빠른정답 ✓ (⑤는 y=−x²−3과 대칭).")

# ---------------- p87 (모눈 그래프 + 상자)
add(id="d616ac37", qtype="choice",
    question=("다음 [[y = -frac(1,2) pow(x,2) + 3]]의 그래프를 보고 (A)~(E)에\n알맞은 것으로 바르게 짝 지어진 것은?\n"
              "(1) 이차함수 [[y = -frac(1,2) pow(x,2)]]의 그래프를 [[y]]축의 방향으로 (A) 만큼 평행이동한 것이다.\n"
              "(2) 꼭짓점의 좌표는 (B) 이다.\n"
              "(3) 축의 방정식은 (C) 이다.\n"
              "(4) (D) 로 볼록한 그래프이다.\n"
              "(5) [[x]]의 값이 증가할 때, [[y]]의 값은 감소하는 [[x]]의 값의 범위는 (E) 이다."),
    choices=["(A) [[2]]", "(B) [[point(3, 0)]]", "(C) [[y = 0]]", "(D) 아래", "(E) [[x > 0]]"],
    derived_answer="⑤",
    figure=U("모눈 좌표평면: 위로 볼록한 포물선 y=−(1/2)x²+3, 꼭짓점 (0,3), x축과 약 ±2.4에서 만남, 원점 O"),
    difficulty_est=1, confidence=0.85, needs_review=FIG + "이차함수 그래프(모눈)",
    note="(A)3 (B)(0,3) (C)x=0 (D)위 (E)x>0 → ⑤ = 빠른정답 ✓. 빈칸 (A)~(E)는 텍스트.")

# ======================================================================
# 이차함수 y=a(x-p)²의 그래프
# ======================================================================
# ---------------- p18
add(id="76b90fb4", qtype="choice",
    question="이차함수 [[y = frac(1,3) pow(x + 2, 2)]]의 그래프에서 축의 방정식과\n꼭짓점의 좌표를 차례대로 구하면?",
    choices=["[[x = 2]], [[point(2, 0)]]", "[[x = 2]], [[point(-2, 0)]]", "[[x = -2]], [[point(2, 0)]]",
             "[[x = -2]], [[point(-2, 0)]]", "[[x = -2]], [[point(0, -2)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="축 x=−2, 꼭짓점 (−2,0) → ④ = 빠른정답 ✓.")

# ---------------- p24
add(id="4f6e0db9", qtype="choice",
    question="이차함수 [[y = 2 pow(x,2)]]의 그래프를 [[x]]축의 방향으로 5만큼\n평행이동한 그래프를 나타내는 이차함수의 식과 그\n꼭짓점의 좌표를 바르게 짝 지은 것은?",
    choices=["[[y = -2 pow(x - 5, 2)]], [[point(5, 0)]]", "[[y = -2 pow(x + 5, 2)]], [[point(5, 0)]]",
             "[[y = 2 pow(x - 5, 2)]], [[point(-5, 0)]]", "[[y = 2 pow(x - 5, 2)]], [[point(0, 5)]]",
             "[[y = 2 pow(x - 5, 2)]], [[point(5, 0)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="y=2(x−5)², 꼭짓점 (5,0) → ⑤. 빠른정답 1과 불일치.")

# ---------------- p44
add(id="1d82ab6e", qtype="choice",
    question="다음 그림과 같이 두 이차함수 [[y = -pow(x,2) + 9]],\n[[y = a pow(x - p, 2)]]의 그래프가 서로의 꼭짓점을 지난다. 이때\n상수 [[a]], [[p]]에 대하여 [[p - a]]의 값은? (단, [[p > 0]])",
    choices=M("1", "2", "3", "4", "5"), derived_answer="②",
    figure=U("좌표평면: 위로 볼록한 포물선 y=−x²+9(꼭짓점 y축 위)와 아래로 볼록한 포물선 y=a(x−p)²(꼭짓점 x축 위 양의 부분)가 서로의 꼭짓점을 지남, 원점 O"),
    difficulty_est=2, confidence=0.85, needs_review=FIG + "두 포물선 그래프",
    note="(p,0)이 y=−x²+9 위 → p=3, (0,9)가 y=a(x−3)² 위 → a=1 → p−a=2 → ②. 빠른정답 −27과 불일치.")

# ---------------- p61
add(id="b3658aaa", qtype="short",
    question=("다음 그림과 같이 이차함수 [[y = pow(x - 4, 2)]]의 그래프가\n[[y]]축과 만나는 점 A에서 [[x]]축에 평행한 직선을 그어\n"
              "그래프와 만나는 점을 B라 하자. 주사위를 두 번 던져서\n나오는 눈의 수를 각각 [[a]], [[b]]라 할 때, 일차함수\n"
              "[[y = frac(3,4) x + a b]]의 그래프가 선분 AB와 만날 확률을\n구하시오."),
    choices=None, derived_answer="frac(1,4)",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=(x−4)²(꼭짓점 x축 위), y축과 만나는 점 A, A에서 x축에 평행한 선분 AB(B는 포물선 위 오른쪽), 원점 O"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "포물선+선분 AB 그래프",
    note="A(0,16), B(8,16); 직선이 y=16과 0≤x≤8에서 만나려면 10≤ab≤16 → (a,b) 9가지 → 9/36=1/4 = 빠른정답 ✓.")

# ---------------- p62
add(id="88b734b0", qtype="short",
    question=("다음 그림과 같이 직선 [[y = x + m]]과 [[x]]축, [[y]]축의 교점을\n각각 A, B라 하고 포물선 [[y = pow(x - 4, 2)]]과 직선\n"
              "[[y = x + m]]의 교점 중 포물선의 축의 오른쪽에 있는 점을\nC라 하자. [[seg(AC) = frac(9,2) seg(AB)]]일 때, 상수 [[m]]의 값을 구하시오.\n(단, [[m > 0]])"),
    choices=None, derived_answer="2",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=(x−4)²과 기울기 1인 직선 y=x+m, A(x축 위, 원점 왼쪽), B(y축 위), C(포물선 축 오른쪽의 교점), 원점 O"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "포물선+직선 그래프",
    note="A(−m,0), B(0,m), C의 x좌표 7m/2, (7m/2−4)²=9m/2 → 49m²−130m+64=0 → m=2(32/49는 축 왼쪽) = 빠른정답 ✓.")

# ---------------- p63
add(id="8e4feaa7", qtype="short",
    question=("다음 그림과 같이 직선 [[y = x + m]]과 [[x]]축, [[y]]축의 교점을\n각각 A, B라 하고 포물선 [[y = pow(x - 5, 2)]]과 직선\n"
              "[[y = x + m]]의 교점 중 포물선의 축의 오른쪽에 있는 점을\nC라 하자. [[seg(AC) = 9 seg(AB)]]일 때, 상수 [[m]]의 값을 구하시오.\n(단, [[m > 0]])"),
    choices=None, derived_answer="1",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=(x−5)²과 기울기 1인 직선 y=x+m, A(x축 위, 원점 왼쪽), B(y축 위), C(포물선 축 오른쪽의 교점), 원점 O"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "포물선+직선 그래프",
    note="C의 x좌표 8m, (8m−5)²=9m → (64m−25)(m−1)=0 → m=1(25/64는 축 왼쪽) = 빠른정답 ✓.")

# ---------------- p64
add(id="c81d0e16", qtype="short",
    question=("다음 그림과 같이 직선 [[y = x + m]]과 [[x]]축, [[y]]축의 교점을\n각각 A, B라 하고 포물선 [[y = pow(x - 6, 2)]]과 직선\n"
              "[[y = x + m]]의 교점 중 포물선의 축의 오른쪽에 있는 점을\nC라 하자. [[seg(AC) = frac(8,3) seg(AB)]]일 때, 상수 [[m]]의 값을 구하시오.\n(단, [[m > 0]])"),
    choices=None, derived_answer="6",
    figure=U("좌표평면: 아래로 볼록한 포물선 y=(x−6)²과 기울기 1인 직선 y=x+m, A(x축 위, 원점 왼쪽), B(y축 위), C(포물선 축 오른쪽의 교점), 원점 O"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "포물선+직선 그래프",
    note="C의 x좌표 5m/3, (5m/3−6)²=8m/3 → 25m²−204m+324=0 → m=6(2.16은 축 왼쪽) = 빠른정답 ✓.")

# ---------------- p94
add(id="def484a8", qtype="choice",
    question="이차함수 [[y = 2 pow(x - 3, 2)]]의 그래프에 대한 설명 중 옳지\n않은 것은?",
    choices=["아래로 볼록한 그래프이다.", "꼭짓점은 [[point(3, 0)]]이다.", "[[y]]의 값의 범위는 [[y >= 3]]이다.",
             "[[y]]축과 [[point(0, 18)]]에서 만난다.", "축의 방정식은 [[x = 3]]이다."],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="y의 범위는 y≥0 → ③ 거짓. 빠른정답 5와 불일치.")

# ======================================================================
# 인수분해를 이용한 이차방정식의 풀이
# ======================================================================
# ---------------- p11
add(id="3f03b8e8", qtype="choice",
    question="다음 중 [[A B = 0]]이 아닌 것을 고르면?",
    choices=["[[A = 0]], [[B = 0]]", "[[A != 0]], [[B != 0]]", "[[A = 0]], [[B != 0]]", "[[-A = B = 0]]", "[[A != 0]], [[B = 0]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="둘 다 0이 아니면 AB≠0 → ② = 빠른정답 ✓.")

# ---------------- p14
add(id="1006513e", qtype="choice",
    question="이차방정식 [[(x + 2)(x - 3) = 0]]을 풀면?",
    choices=["[[x = -2]] 또는 [[x = -3]]", "[[x = -2]] 또는 [[x = 3]]", "[[x = 2]] 또는 [[x = 3]]",
             "[[x = 2]] 또는 [[x = -3]]", "[[x = 0]] 또는 [[x = 3]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="x=−2 또는 x=3 → ② = 빠른정답 ✓.")

# ---------------- p27 (일차함수 조건 → 이차방정식)
add(id="8184f8d4", qtype="short",
    question="일차함수 [[y = m x - (3m + 3)]]의 그래프가\n점 [[point(m + 2, m)]]을 지나고 제2사분면을 지나지 않을 때,\n상수 [[m]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="대입 m²−2m−3=0 → m=3 또는 −1; 제2사분면을 지나지 않으려면 m=3(기울기 3, y절편 −12) = 빠른정답 ✓.")

# ---------------- p32
add(id="0446b14c", qtype="choice",
    question="[[f(n) = frac(pow(n,2), pow(n,2) - 1)]]이라 하자.\n[[a = f(2) × f(3)]] × ⋯ × [[f(499)]]라 할 때, 다음 중\n이차방정식 [[250 a pow(x,2) - x - 498 = 0]]의 해가 될 수 있는\n것은?",
    choices=M("-499", "-498", "1", "498", "499"), derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="곱=2·499/500 → a=499/250 → 499x²−x−498=(499x+498)(x−1)=0 → x=1 → ③. 빠른정답 'neg 1'과 불일치.")

# ---------------- p33
add(id="90d3f5df", qtype="choice",
    question="[[f(n) = frac(pow(n,2), pow(n,2) - 1)]]에 대하여\n[[a = f(2) × f(3)]] × ⋯ × [[f(99)]]라 할 때, 다음 중\n이차방정식 [[50 a pow(x,2) - x - 98 = 0]]의 해가 될 수 있는 것은?",
    choices=M("-99", "-98", "1", "98", "99"), derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="a=2·99/100=99/50 → 99x²−x−98=(99x+98)(x−1)=0 → x=1 → ③. 빠른정답 4와 불일치.")

# ---------------- p34
add(id="4662f089", qtype="choice",
    question="[[f(n) = frac(pow(n,2), pow(n,2) - 1)]]에 대하여\n[[a = f(2) × f(3)]] × ⋯ × [[f(199)]]라 할 때, 다음 중\n이차방정식 [[100 a pow(x,2) + x - 198 = 0]]의 해가 될 수 있는\n것은?",
    choices=M("-199", "-198", "-1", "1", "198"), derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="a=2·199/200=199/100 → 199x²+x−198=(199x−198)(x+1)=0 → x=−1 → ③. 빠른정답 1과 불일치.")

# ---------------- p35 (수직선 도형)
add(id="36e6df2b", qtype="short",
    question=("다음 그림과 같이 수직선 위의 세 점 A, B, C가 나타내는\n수는 각각 [[4 - 3a]], [[a]], [[2a + 3]]이다. 선분 AB와 선분 BC의\n"
              "길이의 비가 [[ratio(4, 3)]]일 때, [[x]]에 대한 이차방정식\n[[pow(x,2) + a x - 10 = 0]]의 두 근이 [[alpha]], [[beta]]이다. 이때 [[pow(alpha,2) + pow(beta,2)]]의\n"
              "값을 구하시오. (단, [[a]]는 [[a > 1]]인 상수이고 [[alpha > beta]]이다.)"),
    choices=None, derived_answer="29",
    figure=U("양쪽 화살표 수직선 위에 왼쪽부터 점 A(아래 4−3a), B(아래 a), C(아래 2a+3)"),
    difficulty_est=3, confidence=0.85, needs_review=FIG + "수직선 위 세 점 도형",
    note="AB=4a−4, BC=a+3, (4a−4):(a+3)=4:3 → a=3 → x²+3x−10=0 → α=2, β=−5 → α²+β²=29. 빠른정답 3과 불일치.")

# ---------------- p69
add(id="c07a6a85", qtype="short",
    question=("[[f(x) = frac(1, sqrt(x + 1) + sqrt(x))]]이고, [[k = f(49) + f(50) + f(51)]] + ⋯ + [[f(79) + f(80)]]이다.\n"
              "[[k]]가 [[x]]에 관한 이차방정식 [[(a + 5) pow(x,2) + (pow(a,2) - 2) x + 4(a - 2) = 0]]의 한 근일 때, 다른 한 근을 구하여라."),
    choices=None, derived_answer="-frac(8,3)", figure=None, difficulty_est=4, confidence=0.85,
    note="f(x)=√(x+1)−√x → k=√81−√49=2, x=2 대입 2(a+2)²=0 → a=−2 → 3x²+2x−16=(3x+8)(x−2)=0 → 다른 근 −8/3 (빠른정답 없음, 풀이 답).")

# ---------------- p70
add(id="ba99ebe0", qtype="short",
    question=("[[f(x) = frac(1, sqrt(x + 1) + sqrt(x))]]이고\n[[k = f(1) + f(2)]] + ⋯ + [[f(23) + f(24)]]이다.\n"
              "[[k]]가 [[x]]에 관한 이차방정식\n[[(a + 1) pow(x,2) + (pow(a,2) - 2) x + 8 = 0]]의 한 근일 때,\n다른 한 근을 구하시오."),
    choices=None, derived_answer="-2", figure=None, difficulty_est=4, confidence=0.85,
    note="k=√25−√1=4, x=4 대입 4(a+2)²=0 → a=−2 → −x²+2x+8=0 → (x−4)(x+2)=0 → 다른 근 −2. 빠른정답 7과 불일치.")

# ---------------- p82
add(id="d96fafda", qtype="short",
    question="[[A = pow(x,2) - 4x - 5]], [[B = pow(x,2) + 4x - 45]]에 대하여\n[[A + B = 0]], [[A B != 0]]을 만족시키는 [[x]]의 값을\n구하시오.",
    choices=None, derived_answer="-5", figure=None, difficulty_est=3, confidence=0.9,
    note="A+B=2x²−50=0 → x=±5; x=5이면 A=0(AB=0) → x=−5. 빠른정답 2와 불일치.")
