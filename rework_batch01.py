# -*- coding: utf-8 -*-
# batch01 (h1-2 보류분 45문항, esc_sonnet_h1-2_5of7) — v1.5 문법 재작업
# 핵심 교체: (f∘g)(x)→app(comp(f,g), x) / f⁻¹(k)→app(inv(f), k) / (g∘f)⁻¹(k)→app(inv((comp(g,f))), k)
#            fⁿ(x)→iter(f, n, x) / 조각적 정의→cases(식, 조건, …) / 프라임 라벨→seg(AP')
# 도형(대응 그림·그래프)은 unsupported(raw) 유지 — 도형만 남은 항목은 통과(PROGRESS 2026-09-04 00:30 규칙)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ---------------- 원의 방정식과 그래프 ----------------
# 0. 883c59b9 — p76: AP′ 위줄 → seg(AP'). 선지 5개가 자취 그림이라 여전히 보류
add(id="883c59b9", qtype="choice",
    question="다음 그림과 같이 중심이 O이고 반지름의 길이가 [[r]]인 원 [[C]]와 이 원 위의 한 점 A에서 접하는 직선 [[l]]이 있다.\n점 P가 직선 [[l]] 위를 움직일 때, [[seg(AP') = r × frac(seg(AP), seg(OP))]] 를 만족시키는 선분 OP 위의 점 P′의 자취를 가장 옳게 나타낸 것은? (단, 점선은 원 [[C]]이다.)",
    choices=["(그림) 선분 OA", "(그림) 선분 OA를 대각선으로 하는 정사각형", "(그림) 선분 OA를 긴 대각선으로 하는 마름모", "(그림) 선분 OA를 지름으로 하는 원", "(그림) 두 점 O, A를 양 끝으로 하는 볼록한 두 호(렌즈 모양)"],
    figure=[{"fn": "unsupported", "args": {"raw": "원 C(중심 O, 반지름 r), 접점 A, 접선 l 위의 점 P, 선분 OP 위의 점 P′; 선지 ①~⑤는 점선 원 C 안에 그린 자취 그림"}}],
    confidence=0.75,
    needs_review="선지 ①~⑤가 자취 그림 — 문법·텍스트로 표현 불가(설명문으로 대체)",
    note="프라임 라벨 AP′를 seg(AP')로 교체. 답 ④ 유지(P′는 A에서 OP에 내린 수선의 발 → OA를 지름으로 하는 원)")

# 1. 5a15878a — p78: OP·OP′ → seg(OP) × seg(OP'). 선지 그림이라 보류
add(id="5a15878a", qtype="choice",
    question="중심이 O이고 반지름의 길이가 [[r]]인 원 [[C]]와 이 원 위의 한 점 A에서 접하는 직선 [[l]]이 있다.\n점 P가 직선 [[l]] 위를 움직일 때, [[seg(OP) × seg(OP') = pow(r,2)]]을 만족시키는 선분 OP 위의 점 P′의 자취를 가장 옳게 나타낸 것은? (단, 점선은 원 [[C]]이다.)",
    choices=["(그림) 선분 OA", "(그림) 두 점 O, A를 양 끝으로 하는 볼록한 두 호(렌즈 모양)", "(그림) 선분 OA를 지름으로 하는 원", "(그림) 선분 OA를 대각선으로 하는 정사각형", "(그림) 선분 OA를 긴 대각선으로 하는 마름모"],
    figure=[{"fn": "unsupported", "args": {"raw": "원 C(중심 O, 반지름 r), 접점 A, 접선 l 위의 점 P, 선분 OP 위의 점 P′; 선지 ①~⑤는 점선 원 C 안에 그린 자취 그림"}}],
    confidence=0.75,
    needs_review="선지 ①~⑤가 자취 그림 — 문법·텍스트로 표현 불가(설명문으로 대체)",
    note="[2004년 6월 고2 이과 19번]. 프라임 라벨 OP′를 seg(OP')로 교체. 답 ③ 유지(반전 → OA를 지름으로 하는 원)")

# ---------------- 역함수 ----------------
# 2. db7ba651 — p6: f⁻¹(3) → app(inv(f), 3). 대응 그림 unsupported(raw)
add(id="db7ba651", qtype="choice",
    question="다음 그림은 함수 [[f]]: [[X]]→[[X]]를 나타낸 것이다.\n[[app(inv(f), 3)]]의 값은?",
    choices=["1", "2", "3", "4", "5"],
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={1,2,3,4,5}→X, f: 1→3, 2→1, 3→5, 4→2, 5→4"}}],
    confidence=0.85,
    note="[2026년 3월 고2 4번 변형]. f⁻¹(3)→app(inv(f), 3); 대응 그림은 unsupported(raw). 답 ① 유지(f(1)=3)")

# 3. 6abd92e8 — p12: (f∘f)(x)+2f⁻¹(x)=3x → app
add(id="6abd92e8", qtype="short",
    question="집합 [[X = set(1, 2, 3, 4, 5, 6)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 역함수가 존재하고, 다음 조건을 모두 만족시킨다.\n(가) [[x]] = 1, 2, 5일 때, [[app(comp(f, f), x) + 2 app(inv(f), x) = 3x]]이다.\n(나) [[f(5) != 5]]\n[[f(3) × (f(4) + f(6))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2018년 11월 고1 30번 변형]. 합성·역함수 적용을 app으로. 원문 중괄호 {f(4)+f(6)}는 소괄호. 답 48 유지")

# 4. 8c560099 — p13: g(x) 경우 나눔 → cases, g⁻¹(1) → app
add(id="8c560099", qtype="choice",
    question="최고차항의 계수가 양수인 이차함수 [[f(x)]]에 대하여 함수 [[g(x)]]를 다음과 같이 정의하자.\n[[g(x) = cases(-x + 4, x < -2, f(x), -2 <= x <= 1, -x - 2, x > 1)]]\n함수 [[g(x)]]의 치역이 실수 전체의 집합이고, 함수 [[g(x)]]의 역함수가 존재할 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(-2) + f(1) = 3]]\nㄴ. [[g(0) = -1]], [[g(1) = -3]]이면 곡선 [[y = f(x)]]의 꼭짓점의 [[x]]좌표는 [[frac(5,2)]]이다.\nㄷ. 곡선 [[y = f(x)]]의 꼭짓점의 [[x]]좌표가 [[-2]]이면 [[app(inv(g), 1) = 0]]이다.",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2019년 3월 고2 문과 21번/4점]. 경우 나눔을 cases로, g⁻¹(1)을 app(inv(g), 1)로. 답 ③ 유지")

# 5. 6bcb11fa — p14: (f∘f)(x)+f⁻¹(x)=2x → app
add(id="6bcb11fa", qtype="short",
    question="집합 [[X = set(1, 2, 3, 4, 5, 6, 7)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 역함수가 존재하고,\n다음 조건을 만족시킨다.\n(가) [[x]] = 1, 2, 6일 때 [[app(comp(f, f), x) + app(inv(f), x) = 2x]]이다.\n(나) [[f(3) + f(5) = 10]]\n[[f(6) != 6]]일 때, [[f(4) × (f(6) + f(7))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2018년 11월 고1 30번/4점]. 합성·역함수 적용을 app으로. 원문 중괄호는 소괄호. 답 50 유지(전수 확인)")

# 6. 1c3adb35 — p16: 경우 나눔 → cases
add(id="1c3adb35", qtype="choice",
    question="함수 [[f(x) = cases(x + 2, x >= 0, a x + b, x < 0)]]의 역함수가 존재하기 위한 실수 [[a]], [[b]]의 조건은?",
    choices=["[[a > 0]], [[b > 0]]", "[[a > 0]], [[b = 2]]", "[[a > 0]], [[b = 1]]", "[[a < 0]], [[b < 0]]", "[[a < 0]], [[b = -2]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 ② 유지(a>0, b=2)")

# 7. 7dd3c195 — p21: f⁻¹(x) 경우 나눔 → app(inv(f), x) = cases(…)
add(id="7dd3c195", qtype="choice",
    question="두 집합 [[X = setb(x, x >= -2)]], [[Y = setb(y, y >= 8)]]에 대하여 [[X]]에서 [[Y]]로의 함수 [[f(x) = 2 abs(x + 2) + abs(x - 6)]]의 역함수가\n[[app(inv(f), x) = cases(x + a, 8 <= x < b, c x + d, x >= b)]]일 때, [[a + b + c + d]]의 값은? (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)",
    choices=["[[frac(19,3)]]", "[[frac(20,3)]]", "7", "[[frac(22,3)]]", "8"],
    figure=None, confidence=0.85,
    note="역함수 적용 + 경우 나눔을 app(inv(f), x) = cases(…)로. 답 ③ 유지(a=−10, b=16, c=1/3, d=2/3)")

# 8. 07b3c854 — p26: f⁻¹(x) = ax + b → app
add(id="07b3c854", qtype="choice",
    question="실수 전체의 집합에서 정의된 함수 [[f]]에 대하여 [[f(3x + 2) = 6x + 5]]이고 함수 [[f(x)]]의 역함수가 [[app(inv(f), x) = a x + b]]이다. 이때 상수 [[a]], [[b]]에 대하여 [[4a b]]의 값은?",
    choices=["[[-4]]", "[[-1]]", "1", "2", "4"],
    figure=None, confidence=0.85,
    note="f⁻¹(x)를 app(inv(f), x)로. 답 ② 유지(f(t)=2t+1 → a=1/2, b=−1/2)")

# 9. 936bd6c0 — p32: (g∘f)(3)=4, (f⁻¹∘g⁻¹)(6) → app
add(id="936bd6c0", qtype="short",
    question="세 집합 [[X = set(1, 2, 3)]], [[Y = set(3, 4, 5)]], [[Z = set(2, 4, 6)]]에 대하여 두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[Z]]가 일대일대응이고, [[f(1) = 4]], [[g(3) = 2]], [[app(comp(g, f), 3) = 4]]일 때,\n[[app(comp(inv(f), inv(g)), 6)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 1 유지(f(3)=5, g(5)=4, g(4)=6 → f⁻¹(g⁻¹(6))=f⁻¹(4)=1)")

# 10. ee10c781 — p34: 경우 나눔(조건 x = 1, 2) → cases + in(x, set(1,2)); gⁿ(x) → iter
add(id="ee10c781", qtype="choice",
    question="집합 [[X = set(1, 2, 3, 4)]]에 대하여 [[X]]에서 [[X]]로의 함수 [[f]]가\n[[f(x) = cases(pow(x,2), in(x, set(1, 2)), x + a, in(x, set(3, 4)))]] ([[a]]는 상수)\n이고, 함수 [[f]]의 역함수 [[g]]가 존재한다.\n[[iter(g, 1, x) = g(x)]], [[iter(g, n + 1, x) = g(iter(g, n, x))]] ([[n]] = 1, 2, 3, ⋯)\n라 할 때, [[a + iter(g, 10, 2) + iter(g, 11, 2)]]의 값은?",
    choices=["4", "5", "6", "7", "8"],
    figure=None, confidence=0.8,
    note="[2015년 11월 고2 문과 19번/4점]. 원문 조건 '(x = 1, 2)', '(x = 3, 4)'는 cases 조건이 식 하나여야 해서 in(x, set(1, 2))·in(x, set(3, 4))로 표기(뜻 동일). gⁿ(x)는 iter. 답 ③ 유지(a=−1, g¹⁰(2)=3, g¹¹(2)=4)")

# 11. 10d2d23b — p37: (g∘f)(3)+(g∘f)⁻¹(9) → app. 대응 그림 unsupported(raw)
add(id="10d2d23b", qtype="choice",
    question="그림은 두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[X]]를 나타낸 것이다.\n[[app(comp(g, f), 3) + app(inv((comp(g, f))), 9)]]의 값은?",
    choices=["6", "9", "12", "15", "18"],
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={3,6,9}, Y={1,4,7}; f: 3→1, 6→7, 9→4; g: 1→6, 4→3, 7→9"}}],
    confidence=0.85,
    note="[2022년 11월 고1 9번/3점]. 합성·역합성 적용을 app으로; 대응 그림은 unsupported(raw). 답 ③ 유지(6+6=12)")

# 12. 28f9c1d2 — p39: f²(x)=f(f(x)), g²⁰(1)+… → iter
add(id="28f9c1d2", qtype="short",
    question="함수 [[f]]에 대하여\n[[iter(f, 2, x) = f(f(x))]], [[iter(f, 3, x) = f(f(f(x)))]]로 정의하자.\n집합 [[X = set(1, 2, 3, 4)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 두 조건 [[f(2) = 4]], [[f(4) = 3]], [[pow(f,4) = I]] ([[I]]는 항등함수)를 만족한다. 함수 [[f]]의 역함수를 [[g]]라 할 때,\n[[iter(g, 20, 1) + iter(g, 23, 2) + iter(g, 26, 3)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="거듭 합성 적용을 iter로(인자 없는 f⁴=I는 pow(f,4) 유지). 답 7 유지(f: 2→4→3→1→2 4-순환 → 1+4+2)")

# 13. ad6865a0 — p40: 보기 ㄱㄴㄷ의 (f∘f)(f(a)), f⁻¹(a), (f∘f)⁻¹(a) → app
add(id="ad6865a0", qtype="choice",
    question="집합 [[X]] = { [[x]] | [[x]]는 실수 }에 대하여 [[X]]에서 [[X]]로의 함수 [[f]]가 다음 조건을 모두 만족시킨다.\n(가) [[f]]의 역함수가 존재한다.\n(나) [[in(sub(x,1), X)]], [[in(sub(x,2), X)]]일 때, [[sub(x,1) > sub(x,2)]]이면 [[f(sub(x,1)) > f(sub(x,2))]]이다.\n다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n(단, [[a < b]])\n<보기>\nㄱ. [[app(comp(f, f), f(a)) > app(comp(f, f), f(b))]]\nㄴ. [[app(inv(f), a) > app(inv(f), b)]]\nㄷ. [[app(inv((comp(f, f))), a) < app(inv((comp(f, f))), b)]]",
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="합성·역함수 적용을 app으로. 답 ③ 유지(f 증가 → ㄷ만 참)")

# 14. 4626cafc — p52: (f⁻¹∘f)(7) → app. 대응 그림 unsupported(raw)
add(id="4626cafc", qtype="short",
    question="다음 그림과 같은 함수 [[f]]: [[X]]→[[Y]]에서\n[[app(comp(inv(f), f), 7)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={6,7,8}, Y={1,2,3}; f: 6→3, 7→1, 8→2"}}],
    confidence=0.85,
    note="합성 적용을 app으로; 대응 그림은 unsupported(raw). 답 7 유지(f⁻¹∘f는 항등)")

# 15. 19dc88f3 — p54: (f∘f⁻¹)(3) → app. 대응 그림 unsupported(raw)
add(id="19dc88f3", qtype="short",
    question="다음 그림과 같은 함수 [[f]]: [[X]]→[[Y]]에 대하여\n[[app(comp(f, inv(f)), 3)]]을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={0,1,2,3}, Y={1,2,3,4}; f: 0→3, 1→1, 2→2, 3→4"}}],
    confidence=0.85,
    note="합성 적용을 app으로; 대응 그림은 unsupported(raw). 답 3 유지(f∘f⁻¹는 Y 위 항등)")

# 16. 46c17db8 — p57: (f⁻¹∘g)⁻¹(6) → app
add(id="46c17db8", qtype="short",
    question="두 함수 [[f(x) = frac(1,3) x + 2]], [[g(x) = 2x - 6]]에 대하여\n[[app(inv((comp(inv(f), g))), 6)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="역합성 적용을 app으로. 답 5 유지(g⁻¹(f(6))=g⁻¹(4)=5)")

# 17. e347572f — p58: (다) ½f(a)=(f∘f⁻¹)(a), f(2)·f⁻¹(2) → app
add(id="e347572f", qtype="short",
    question="두 집합 [[X = set(1, 2, 3, 4)]], [[Y = set(2, 4, 6, 8)]]에 대하여 함수 [[f]]: [[X]]→[[Y]]가 다음 조건을 만족시킨다.\n(가) 함수 [[f]]는 일대일대응이다.\n(나) [[f(1) != 2]]\n(다) 등식 [[frac(1,2) f(a) = app(comp(f, inv(f)), a)]]를 만족시키는 [[a]]의 개수는 2이다.\n[[f(2) × app(inv(f), 2)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2018년 10월 고3 문과 28번/4점]. 합성·역함수 적용을 app으로(원문 곱셈점 ·는 ×). 답 12 유지(f(2)=4, f⁻¹(2)=3)")

# 18. dba86109 — p60: 위 변형
add(id="dba86109", qtype="short",
    question="두 집합 [[X = set(1, 2, 3, 4)]], [[Y = set(1, 2, 3, 4)]]에 대하여 함수 [[f]]: [[X]]→[[Y]]가 다음 조건을 만족시킨다.\n(가) 함수 [[f]]는 일대일대응이다.\n(나) [[f(3) != 3]]\n(다) 등식 [[frac(1,2) f(a) = app(comp(f, inv(f)), a)]]를 만족시키는 [[a]]의 개수는 2이다.\n[[f(4) × app(inv(f), 4)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2018년 10월 고3 문과 28번 변형]. 합성·역함수 적용을 app으로(원문 곱셈점 ·는 ×). 답 6 유지(f(4)=3, f⁻¹(4)=2)")

# 19. 93c7a12f — p61: 경우 나눔 → cases, (f∘f)(3)+f⁻¹(−6) → app
add(id="93c7a12f", qtype="short",
    question="함수 [[f(x) = cases(3x, x >= 2, -pow(x,2) + 5x, x < 2)]]에 대하여\n[[app(comp(f, f), 3) + app(inv(f), -6)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 합성·역함수 적용을 app으로. 답 26 유지(27+(−1))")

# 20. 0237664f — p62: 경우 나눔 → cases, (f⁻¹∘f⁻¹)(6) → app
add(id="0237664f", qtype="choice",
    question="실수 전체의 집합에서 정의된\n함수 [[f(x) = cases(x + k, x < 1, 2x + 3, x >= 1)]]의 역함수가 존재할 때,\n[[app(comp(inv(f), inv(f)), 6)]]의 값은? (단, [[k]]는 상수이다.)",
    choices=["[[-frac(1,2)]]", "[[-1]]", "[[-frac(3,2)]]", "[[-2]]", "[[-frac(5,2)]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 역합성 적용을 app으로. 답 ⑤ 유지(k=4 → f⁻¹(6)=3/2, f⁻¹(3/2)=−5/2)")

# 21. 293d737a — p64: 경우 나눔 → cases, f(−1)+f⁻¹(7) → app
add(id="293d737a", qtype="short",
    question="함수 [[f(x) = cases(x + 5, x >= 1, 2x + 4, x < 1)]]에 대하여\n[[f(-1) + app(inv(f), 7)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 역함수 적용을 app으로. 답 4 유지(2+2)")

# 22. b8cb66cd — p65: (f∘f)(x)=f(x)−2x → app
add(id="b8cb66cd", qtype="short",
    question="집합 [[X = set(1, 2, 3, 4, 5, 6, 7, 8, 9)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족한다.\n(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n(나) [[1 <= x <= 4]]일 때,\n[[app(comp(f, f), x) = f(x) - 2x]]이다.\n[[f(2) + f(3) + f(4) + f(5)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 29 유지(전수 확인: f=(6,7,8,9,5,4,3,2,1))")

# 23. c5426f2a — p66
add(id="c5426f2a", qtype="short",
    question="집합 [[X = set(1, 2, 3, 4, 5, 6)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족한다.\n(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n(나) [[1 <= x <= 3]]일 때,\n[[app(comp(f, f), x) = 2f(x) - 3x - 2]]이다.\n[[f(2) + f(3) + f(4)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 14 유지(전수 확인: f=(4,5,6,3,2,1))")

# 24. ec74440a — p67
add(id="ec74440a", qtype="short",
    question="집합 [[X = set(1, 2, 3, 4, 5, 6, 7)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족한다.\n(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n(나) [[1 <= x <= 3]]일 때,\n[[app(comp(f, f), x) = f(x) - 2x]]이다.\n[[f(2) + f(3) + f(4) + f(5)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 20 유지(전수 확인: f=(5,6,7,4,3,2,1))")

# 25. 3578dadc — p69: 경우 나눔 → cases, f⁻¹(x) → app, {x | f(x)=f⁻¹(x)} → setb
add(id="3578dadc", qtype="short",
    question="함수 [[f(x) = cases(pow(x,2) - 6x + 10, x < 2, k(x - 2) + 2, x >= 2)]]에 대하여\n역함수 [[app(inv(f), x)]]가 존재한다.\n[[setb(x, f(x) = app(inv(f), x)) = set(2, a, a + 4)]]일 때,\n[[18(pow(k,2) + pow(a,2))]]의 값을 구하시오. (단, [[k]]는 상수이다.)",
    choices=None, figure=None, confidence=0.8,
    note="경우 나눔을 cases로, 역함수 적용을 app으로, 조건제시 집합을 setb로. 답 20 유지(a=1, k=−1/3)")

# 26. 3e574db4 — p70
add(id="3e574db4", qtype="short",
    question="집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족시킨다.\n(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n(나) [[1 <= x <= 2]]일 때,\n[[app(comp(f, f), x) = f(x) - 2x]]이다.\n[[f(2) + f(3) + f(4)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2017년 3월 고2 이과 28번 변형]. 합성 적용을 app으로. 답 10 유지(전수 확인: f=(4,5,3,2,1))")

# 27. bb68c861 — p71: (f⁻¹∘(g∘f⁻¹)⁻¹∘f)(x) → app
add(id="bb68c861", qtype="short",
    question="두 함수 [[f(x) = x + 2]], [[g(x) = -2x + 3]]에 대하여\n[[app(comp(comp(inv(f), inv((comp(g, inv(f))))), f), x) = a x + b]]일 때, [[b - a]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 1 유지(g⁻¹∘f = (1−x)/2 → a=−1/2, b=1/2)")

# 28. 05731868 — p72: (f∘(g∘f)⁻¹)(3) → app
add(id="05731868", qtype="short",
    question="역함수가 존재하는 두 함수 [[f(x)]], [[g(x) = -3x - 6]]에 대하여 [[app(comp(f, inv((comp(g, f)))), 3)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성 적용을 app으로. 답 -3 유지(g⁻¹(3)=−3)")

# 29. 2576aa0b — p77: (g∘f⁻¹)(1)=3, (g∘f⁻¹)⁻¹(1)=7, f(1)+g⁻¹(1) → app
add(id="2576aa0b", qtype="short",
    question="집합 [[X = set(1, 3, 7)]]에 대하여 [[X]]에서 [[X]]로의 함수 [[f]], [[g]]의 역함수가 모두 존재하고 [[f(7) = 1]], [[g(3) = 1]], [[app(comp(g, inv(f)), 1) = 3]],\n[[app(inv((comp(g, inv(f)))), 1) = 7]]일 때, [[f(1) + app(inv(g), 1)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="합성·역함수 적용을 app으로. 답 6 유지(f(1)=3, g⁻¹(1)=3)")

# 30. 0afe7e37 — p78: 경우 나눔 → cases, (f∘(f⁻¹∘g)⁻¹)(2) → app
add(id="0afe7e37", qtype="choice",
    question="실수 전체의 집합에서 정의된 두 함수 [[f]], [[g]]가\n[[f(x) = cases(4x + 3, x >= 1, 3x + 4, x < 1)]], [[g(x) = -2x + 3]]일 때,\n[[app(comp(f, inv((comp(inv(f), g)))), 2)]]의 값은?",
    choices=["[[-10]]", "[[-8]]", "[[-6]]", "[[-4]]", "[[-2]]"],
    figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 합성 적용을 app으로. 답 ② 유지(f(g⁻¹(f(2)))=f(−4)=−8)")

# 31. b7153db3 — p80: 조건제시 집합(조건 2개)은 텍스트 혼합, 합성 적용은 app. 그림 정보(1→6, 5→4)는 본문에도 있음
add(id="b7153db3", qtype="choice",
    question="세 집합 [[X = set(1, 2, 3)]], [[Y = set(5, 6, 7)]], [[Z = set(3, 4, 5)]]에 대하여 다음 그림과 같이 일대일대응인 두 함수 [[f]], [[g]]가 [[f(1) = 6]], [[g(5) = 4]]를 만족시킨다.\n{ [[x]] | [[app(comp(g, f), x) = 4]], [[in(x, X)]] } = { [[x]] | [[app(comp(inv(f), inv(g)), x) = 2]], [[in(x, Z)]] } = [[set(3)]]일 때, [[app(comp(comp(g, inv((comp(f, g)))), g), k) = 3]]이다. [[f(2) + g(7) + k]]의 값은?",
    choices=["13", "14", "15", "16", "17"],
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={1,2,3} →f→ Y={5,6,7} →g→ Z={3,4,5}; 화살표 1→6, 5→4만 표시"}}],
    confidence=0.8,
    note="합성·역합성 적용을 app으로; 조건 2개짜리 집합은 텍스트 혼합(GUIDE §4). 답 ④ 유지(f(2)=7, g(7)=3, k=6)")

# 32. 23babf00 — p81: y = f⁻¹(x) → app
add(id="23babf00", qtype="choice",
    question="함수 [[f(x) = pow(x,2) - 2x]] ([[x >= 1]], [[y >= -1]])의 그래프와 그 역함수 [[y = app(inv(f), x)]]의 그래프가 만나는 점의 좌표를 [[point(a, b)]]라고 할 때, [[a + b]]의 값은?",
    choices=["2", "4", "6", "8", "10"],
    figure=None, confidence=0.85,
    note="역함수 적용을 app으로. 답 ③ 유지(교점 (3, 3))")

# 33. dc57d4d2 — p91: f⁻¹(x), f⁻¹(5)+f⁻¹(9) → app. 점 그래프 unsupported(raw)
add(id="dc57d4d2", qtype="short",
    question="집합 [[X = set(1, 3, 5, 7, 9)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 있다. 다음 그림은 함수 [[y = f(x)]]의 그래프의 일부를 나타낸 것이다. 함수 [[f(x)]]의 역함수 [[app(inv(f), x)]]가 존재할 때, [[app(inv(f), 5) + app(inv(f), 9)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(격자 1,3,5,7,9): 그래프 위의 점 (3,1), (7,7), (9,3) 표시"}}],
    confidence=0.85,
    note="역함수 적용을 app으로; 점 그래프는 unsupported(raw). 답 6 유지(f(1), f(5)∈{5,9} → 1+5)")

# 34. d6c7a6af — p92: (f∘f)⁻¹(b) → app. 그래프 unsupported(raw)
add(id="d6c7a6af", qtype="short",
    question="다음 그림은 두 함수 [[y = f(x)]]와 [[y = x]]의 그래프이다.\n이때 [[app(inv((comp(f, f))), b)]]의 값을 구하시오.\n(단, 모든 점선은 [[x]]축 또는 [[y]]축에 평행하다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 증가하는 곡선 y=f(x)와 직선 y=x, x축 위 점 a,b,c,d,e; 점선으로 f(b)=a, f(c)=b, f(d)=c, f(e)=d 임을 표시"}}],
    confidence=0.8,
    note="역합성 적용을 app으로; 그래프는 unsupported(raw). 답 d 유지(f(f(d))=b)")

# ---------------- 유리함수의 그래프 ----------------
# 35. 3d3cfa68 — p4: 사용자 정의 이항연산 △ — v1.5에도 표기 없음 → 텍스트 혼합 유지, 보류
add(id="3d3cfa68", qtype="choice",
    question="두 다항식 [[A]], [[B]]에 대하여 [[A]]△[[B]]를\n[[A]]△[[B]] = [[frac(A, A + B)]] 로 정의할 때,\n{[[(2x - 4)]]△[[(pow(x,2) - 4)]]} + {[[(pow(x,2) + 2x)]]△[[2x]]}를 간단히 하면?",
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "1", "[[x]]", "[[frac(1, pow(x,2))]]"],
    figure=None, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 이항연산 △ — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지",
    note="답 ③ 유지(2/(x+4) + (x+2)/(x+4) = 1)")

# 36. b1497a8a — p53: 경우 나눔 → cases (도형 없음)
add(id="b1497a8a", qtype="short",
    question="좌표평면 위에 함수 [[f(x) = cases(frac(4, x), x > 0, frac(9, x), x < 0)]]의 그래프와 직선 [[y = -x]]가 있다. 함수 [[y = f(x)]]의 그래프 위의 점 P를 지나고 [[x]]축에 수직인 직선이 직선 [[y = -x]]와 만나는 점을 Q, 점 Q를 지나고 [[y]]축에 수직인 직선이 [[y = f(x)]]와 만나는 점을 R라 할 때, 선분 PQ와 선분 QR의 길이의 곱 [[seg(PQ) × seg(QR)]]의 최솟값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로. 답 25 유지(t²+36/t²+13 ≥ 25)")

# 37. 19ed18b1 — p87: f¹⁰⁰(x) → iter; 정의 나열(f¹=f, f²=f∘f¹, …)은 pow(f,n) 등식 나열 유지
add(id="19ed18b1", qtype="short",
    question="함수 [[f(x) = frac(x, 1 - x)]]에 대하여 [[pow(f,1) = f]], [[pow(f,2) = comp(f, pow(f,1))]],\n[[pow(f,3) = comp(f, pow(f,2))]], ⋯, [[pow(f,n) = comp(f, pow(f, n - 1))]] ([[n]] = 2, 3, ⋯)로\n정의한다. [[iter(f, 100, x) = frac(a x + b, c x + d)]]일 때, 상수 [[a]], [[b]], [[c]], [[d]]에\n대하여 [[a + b - c + d]]의 값을 구하시오.\n(단, [[a]], [[b]], [[c]], [[d]]는 서로소이고, [[a > 0]]이다.)",
    choices=None, figure=None, confidence=0.85,
    note="거듭 합성 적용 f¹⁰⁰(x)를 iter로(인자 없는 fⁿ 정의는 pow(f,n) 유지). 답 102 유지(f¹⁰⁰=x/(−100x+1))")

# 38. a6fa80da — p88: f¹(x), fⁿ⁺¹(x)=(f∘fⁿ)(x), f¹⁵(x) → iter/app
add(id="a6fa80da", qtype="choice",
    question="유리함수 [[f(x) = frac(x, 1 + x)]]에 대하여\n[[iter(f, 1, x) = f(x)]], [[iter(f, n + 1, x) = app(comp(f, pow(f, n)), x)]] ([[n]]은 자연수)\n로 정의한다. [[iter(f, 15, x) = frac(a x + b, c x + 1)]]일 때,\n실수 [[a]], [[b]], [[c]]의 합 [[a + b + c]]의 값은?",
    choices=["12", "13", "14", "15", "16"],
    figure=None, confidence=0.85,
    note="거듭 합성 적용을 iter로, (f∘fⁿ)(x)를 app(comp(f, pow(f,n)), x)로. 답 ⑤ 유지(f¹⁵=x/(15x+1))")

# 39. f246cab3 — p89: f⁶(−1) → iter. 유리함수 그래프 unsupported(raw)
add(id="f246cab3", qtype="short",
    question="분모, 분자가 일차식인 [[f(x)]]에 대하여 [[x <= 0]]에서 정의된 함수 [[y = f(x)]]의 그래프가 다음 그림과 같다.\n[[pow(f,1) = f]], [[pow(f,n) = comp(f, pow(f, n - 1))]] ([[n]] = 2, 3, 4, ⋯)로 정의할 때, [[iter(f, 6, -1)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 점근선 x=1, y=−1(점선)인 유리함수 그래프, 원점을 지남; x≤0 부분은 실선, 나머지는 점선"}}],
    confidence=0.8,
    note="거듭 합성 적용을 iter로; 그래프는 unsupported(raw). 답 -frac(1,7) 유지(f(x)=x/(1−x) → fⁿ(x)=x/(1−nx))")

# ---------------- 함수의 합성 ----------------
# 40. 0527fa64 — p2: g 경우 나눔 → cases, (g∘f)(−12)+(f∘g)(5) → app
add(id="0527fa64", qtype="short",
    question="두 함수\n[[f(x) = frac(1,3) x + 2]], [[g(x) = cases(pow(x,2) - 13, x >= 0, -3x + 7, x < 0)]]\n에 대하여 [[app(comp(g, f), -12) + app(comp(f, g), 5)]]의 값을\n구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 합성 적용을 app으로. 답 19 유지(13+6)")

# 41. 513ef81d — p5: (f∘f∘g)(144) → app
add(id="513ef81d", qtype="choice",
    question="자연수 [[n]]에 대하여 두 함수 [[f(n)]], [[g(n)]]이\n[[f(n)]] = ([[n]]보다 작은 소수의 개수),\n[[g(n)]] = ([[sqrt(n)]]보다 작은 자연수의 개수)\n일 때, [[app(comp(comp(f, f), g), 144)]]의 값은?",
    choices=["2", "3", "4", "5", "6"],
    figure=None, confidence=0.85,
    note="합성 적용을 app으로(한글 정의문은 텍스트 혼합, GUIDE §4). 답 ① 유지(g(144)=11, f(11)=4, f(4)=2)")

# 42. dd13c390 — p8: f 경우 나눔 → cases, (g∘f)(x) → app
add(id="dd13c390", qtype="short",
    question="두 함수\n[[f(x) = cases(pow(x,2) + 4a x + 20, x < 0, x + 20, x >= 0)]], [[g(x) = x + 16]]\n에 대하여 합성함수 [[app(comp(g, f), x)]]의 치역이 [[setb(y, y >= 0)]]일\n때, 상수 [[a]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="경우 나눔을 cases로, 합성 적용을 app으로. 답 3 유지(20−4a²=−16, a>0)")

# 43·44. 0d78c693, 2ae4c66e — p9(같은 이미지에 id 2개): f 경우 나눔(3구간) → cases, 보기 ㄱㄴㄷ → app
dup(["0d78c693", "2ae4c66e"], qtype="choice",
    question="실수 전체의 집합에서 정의된 두 함수 [[f(x)]], [[g(x)]]가\n[[f(x) = cases(5, x > 5, x, abs(x) <= 5, -5, x < -5)]], [[g(x) = frac(2,5) pow(x,2) - 5]]\n일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[app(comp(f, g), 5) = 5]]\nㄴ. [[app(comp(g, f), -x) = app(comp(g, f), x)]]\nㄷ. [[app(comp(f, g), x) = app(comp(g, f), x)]]",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="같은 이미지에 id 2개(문항 1개). 경우 나눔을 cases로, 합성 적용을 app으로. 답 ⑤ 유지(ㄱㄴㄷ 모두 참)")
