# -*- coding: utf-8 -*-
# esc_sonnet_h3-3_3of6 — 이미지 기준 전사 (81 항목 / 80쪽, 단원 h3-3 기하: 구·평면·포물선·정사영)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def fig(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]

# ───────────────────────── 구의 방정식 ─────────────────────────
add(id="35a9ae2f", qtype="short",
    question="점 [[A(0, -3, -2)]]에서 구 [[pow(x,2) + pow(y,2) + pow(z,2) - 4x + 4y + k = 0]]에 그은 접선의 길이가 2일 때, 상수 [[k]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="중심 (2,-2,0), r²=8-k, AC²=9 → 9-(8-k)=4 → k=3.")

add(id="3528d8f7", qtype="choice",
    question="좌표공간에 [[seg(OA) = 9]]인 점 A가 있다. 점 A를 중심으로 하고 반지름의 길이가 10인 구 [[S]]와 xy평면이 만나서 생기는 원의 넓이가 [[91 pi]]이다. 구 [[S]]와 [[z]]축이 만나는 두 점을 각각 B, C라 할 때, 선분 BC의 길이는? (단, O는 원점이다.)",
    choices=["[[2 sqrt(19)]]", "[[2 sqrt(22)]]", "[[10]]", "[[4 sqrt(7)]]", "[[2 sqrt(31)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2021년 10월 고3 기하 27번 변형]. A의 z좌표 ±3, A와 z축 거리² = 72 → BC = 2√(100-72) = 4√7.")

add(id="47df1ff0", qtype="choice",
    question="중심이 점 [[C(-3, 4, 12)]]이고 [[z]]축에 접하는 구가 있다. 이 구 위를 움직이는 점 P와 원점 O 사이의 거리의 최댓값은?",
    choices=["[[16]]", "[[18]]", "[[20]]", "[[22]]", "[[24]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="r = √(9+16) = 5, OC = 13 → 최댓값 18. 빠른정답 25와 불일치(정렬 어긋남 추정).")

add(id="c391b285", qtype="choice",
    question="점 [[vcomp(-3, a, -1)]]이 네 점 [[vcomp(0, 0, 0)]], [[vcomp(-4, 0, 0)]], [[vcomp(0, 6, 0)]], [[vcomp(0, -2, 2)]]를 지나는 구 위의 점일 때, 모든 [[a]]의 값의 합은?",
    choices=["[[3]]", "[[4]]", "[[5]]", "[[6]]", "[[7]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="구 x²+y²+z²+4x-6y-10z=0 → a²-6a+8=0 → 합 6.")

add(id="bb2626b3", qtype="choice",
    question="점 [[vcomp(-2, a, -2)]]가 네 점 [[vcomp(0, 0, 0)]], [[vcomp(-10, 0, 0)]], [[vcomp(0, 2, 0)]], [[vcomp(0, 4, 2)]]를 지나는 구 위의 점일 때, 모든 [[a]]의 값의 합은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="구 x²+y²+z²+10x-2y-6z=0 → a²-2a=0 → 합 2.")

add(id="75ebaaa0", qtype="choice",
    question="구 [[pow(x,2) + pow(y,2) + pow(z,2) - 2x + 8y + 6z = 10]]의 중심의 좌표가 [[vcomp(a, b, c)]]이고 반지름의 길이가 [[r]]일 때, [[a + b + c - r]]의 값은?",
    choices=["[[-15]]", "[[-14]]", "[[-13]]", "[[-12]]", "[[-11]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="중심 (1,-4,-3), r=6 → -12.")

add(id="d3309ca6", qtype="choice",
    question="구 [[pow(x,2) + pow(y,2) + pow(z,2) + 4x - 6y + 2z = 2]]의\n중심의 좌표가 [[vcomp(a, b, c)]]이고 반지름의 길이가 [[r]]일 때,\n[[a + b + c - r]]의 값은?",
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="중심 (-2,3,-1), r=4 → -4.")

add(id="d415ffcd", qtype="choice",
    question="구 [[pow(x,2) + pow(y,2) + pow(z,2) + 8x - 4y + 10z = 19]]의\n중심의 좌표가 [[vcomp(a, b, c)]]이고 반지름의 길이가 [[r]]일 때,\n[[a + b + c - r]]의 값은?",
    choices=["[[-15]]", "[[-14]]", "[[-13]]", "[[-12]]", "[[-11]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="중심 (-4,2,-5), r=8 → -15. 빠른정답 2와 불일치.")

add(id="e84963e4", qtype="short",
    question="구 [[pow(x,2) + pow(y,2) + pow(z,2) - 10x + 2y + k z = k]]의 부피가 최소일 때, 이 구의 중심의 좌표는 [[vcomp(a, b, c)]]이고 반지름의 길이는 [[r]]이다. 이때 [[a + b + c + r]]의 값을 구하시오.\n(단, [[k]]는 상수이다.)",
    choices=None, derived_answer="10", figure=None, difficulty_est=3, confidence=0.9,
    note="r² = (k/2+1)²+25 → k=-2, 중심 (5,-1,1), r=5 → 10. 빠른정답 15와 불일치.")

add(id="967977a5", qtype="short",
    question="구 [[pow(x,2) + pow(y,2) + pow(z,2) - 8x + 4y + k z = k]]의 부피가 최소일 때, 이 구의 중심의 좌표는 [[vcomp(a, b, c)]]이고 반지름의 길이는 [[r]]이다. 이때 [[a + b + c + pow(r,2)]]의 값을 구하시오.\n(단, [[k]]는 상수이다.)",
    choices=None, derived_answer="22", figure=None, difficulty_est=3, confidence=0.9,
    note="r² = (k/2+1)²+19 → k=-2, 중심 (4,-2,1), r²=19 → 22. 빠른정답 10과 불일치.")

add(id="5da7f235", qtype="short",
    question=("좌표공간에 두 개의 구 [[sub(S,1)]]: [[pow(x,2) + pow(y,2) + pow(z - 2, 2) = 4]], [[sub(S,2)]]: [[pow(x,2) + pow(y,2) + pow(z + 7, 2) = 49]]가 있다.\n"
              "점 [[A(sqrt(5), 0, 0)]]을 지나고 zx평면에 수직이며 구 [[sub(S,1)]]과 [[z]]좌표가 양수인 한 점에서 접하는 평면을 [[alpha]]라 하자. "
              "구 [[sub(S,2)]]가 평면 [[alpha]]와 만나서 생기는 원을 [[C]]라 할 때, 원 [[C]] 위의 점 중 [[z]]좌표가 최소인 점을 B라 하고 구 [[sub(S,2)]]와 점 B에서 접하는 평면을 [[beta]]라 하자.\n"
              "원 [[C]]의 평면 [[beta]] 위로의 정사영의 넓이가 [[frac(q,p) pi]]일 때, [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="127",
    figure=fig("좌표공간 x·y·z축과 두 구: 작은 구 S₁(위, 중심 (0,0,2))과 큰 구 S₂(아래, 중심 (0,0,-7))가 원점 O 부근에서 접하는 그림"),
    difficulty_est=5, confidence=0.8,
    needs_review="도형 표현 불가: 좌표공간의 두 구 S₁·S₂ 그림",
    note="출처 [2022년 9월 고3 기하 29번/4점]. α: x+(√5/20)z=√5, 원 C 반지름² 40, 두 평면 cos=3/7 → 넓이 120π/7 → 127. 빠른정답 3과 불일치.")

add(id="9a92086c", qtype="short",
    question=("좌표공간에 구 [[S]]: [[pow(x,2) + pow(y,2) + pow(z - sqrt(5), 2) = 9]]가 xy평면과 만나서 생기는 원을 [[C]]라 하자. 구 [[S]] 위의 네 점 A, B, C, D가 다음 조건을 만족시킨다.\n"
              "(가) 선분 AB는 원 [[C]]의 지름이다.\n(나) 직선 AB는 평면 BCD에 수직이다.\n(다) [[seg(BC) = seg(BD) = sqrt(15)]]\n"
              "삼각형 ABC의 평면 ABD 위로의 정사영의 넓이를 [[k]]라 할 때, [[pow(k,2)]]의 값을 구하시오."),
    choices=None, derived_answer="15",
    figure=fig("구 S가 xy평면과 만나 원 C를 이루고, 원 C의 지름 AB와 구 위의 점 C, D로 사면체 ABCD를 그린 그림(S, C, xy평면 표시)"),
    difficulty_est=5, confidence=0.8,
    needs_review="도형 표현 불가: 구 S·원 C·사면체 ABCD 그림",
    note="출처 [2023년 10월 고3 기하 30번/4점]. 원 C 반지름 2, 평면 BCD(x=2) 위 원 반지름 √5, ∠CBD 대응 중심각 120°, △ABC=2√15, 두 평면 cos=1/2 → k=√15, k²=15. 빠른정답 4와 불일치.")

add(id="75cf14b8", qtype="short",
    question=("좌표공간에 구 [[S]]: [[pow(x,2) + pow(y,2) + pow(z - sqrt(2), 2) = 4]]가 xy평면과 만나서 생기는 원을 [[C]]라 하자. 구 [[S]] 위의 네 점 A, B, C, D가 다음 조건을 만족시킨다.\n"
              "(가) 선분 AB는 원 [[C]]의 지름이다.\n(나) 직선 AB는 평면 BCD에 수직이다.\n(다) [[seg(BC) = seg(BD) = sqrt(6)]]\n"
              "삼각형 ABC의 평면 ABD 위로의 정사영의 넓이를 [[k]]라 할 때, [[2 pow(k,2)]]의 값을 구하시오."),
    choices=None, derived_answer="6",
    figure=fig("구 S가 xy평면과 만나 원 C를 이루고, 원 C의 지름 AB와 구 위의 점 C, D로 사면체 ABCD를 그린 그림(S, C, xy평면 표시)"),
    difficulty_est=5, confidence=0.8,
    needs_review="도형 표현 불가: 구 S·원 C·사면체 ABCD 그림",
    note="출처 [2023년 10월 고3 기하 30번 변형]. 원 C 반지름 √2, 평면 BCD 위 원 반지름 √2, △ABC=2√3, cos=1/2 → k=√3, 2k²=6. 빠른정답 15와 불일치.")

add(id="76015eac", qtype="short",
    question=("좌표공간에 반구 [[pow(x - 8, 2) + pow(y - 6, 2) + pow(z, 2) = 16]] ([[z >= 0]])이 있다. [[y]]축을 포함하는 평면 [[alpha]]가 반구와 접할 때, [[alpha]]와 xy평면이 이루는 각을 [[theta]]라 하자.\n"
              "이때 [[20 pow(cos(theta), 2)]]의 값을 구하시오. (단, [[0 < theta < frac(pi, 2)]])"),
    choices=None, derived_answer="15", figure=None, difficulty_est=3, confidence=0.85,
    note="같은 이미지 위쪽 문항(아래쪽은 id a6325b56). 중심 (8,6,0), r=4: 8sinθ=4 → cos²θ=3/4 → 15. 빠른정답 6과 불일치.")

add(id="a6325b56", qtype="short",
    question=("좌표공간에 반구 [[pow(x - 9, 2) + pow(y - 7, 2) + pow(z, 2) = 36]] ([[z >= 0]])이 있다. [[y]]축을 포함하는 평면 [[alpha]]가 반구와 접할 때, [[alpha]]와 xy평면이 이루는 각을 [[theta]]라 하자.\n"
              "이때 [[108 pow(cos(theta), 2)]]의 값을 구하시오. (단, [[0 < theta < frac(pi, 2)]])"),
    choices=None, derived_answer="60", figure=None, difficulty_est=3, confidence=0.85,
    note="같은 이미지 아래쪽 문항(위쪽은 id 76015eac). 중심 (9,7,0), r=6: 9sinθ=6 → cos²θ=5/9 → 60. 빠른정답 6과 불일치.")

# ───────────────────────── 평면과 구의 방정식 ─────────────────────────
add(id="787756a3", qtype="short",
    question="점 [[vcomp(2, -3, 1)]]을 지나고 법선벡터가 [[vec(n) = vcomp(1, 2, -1)]]인 평면의 방정식이 [[x + a y + b z + c = 0]]일 때, [[a + b + c]]의 값을 구하시오. (단, [[a]], [[b]], [[c]]는 상수이다.)",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="x+2y-z+5=0 → 2-1+5=6.")

add(id="f95ae781", qtype="choice",
    question="두 점 [[A(1, 2, 0)]], [[B(3, -1, 4)]]를 지나는 직선에 수직이고 점 [[vcomp(2, 1, -1)]]을 지나는 평면의 방정식은?",
    choices=["[[2x - 3y + 4z - 3 = 0]]", "[[2x - 3y + 4z + 3 = 0]]", "[[2x + 3y - 4z - 3 = 0]]", "[[4x - 3y + 2z - 3 = 0]]", "[[4x + 3y - 2z + 3 = 0]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="법선 (2,-3,4), 4-3-4+d=0 → d=3. 빠른정답 6과 불일치.")

add(id="a872f80e", qtype="short",
    question=("좌표공간에서 직선 [[l]]: [[x - 1 = frac(y, 2) = 1 - z]]와 평면 [[alpha]]가 점 [[A(1, 0, 1)]]에서 수직으로 만난다. 평면 [[alpha]] 위의 점 [[B(-1, a, a)]]와 직선 [[l]] 위의 점 C에 대하여 "
              "삼각형 ABC가 이등변삼각형일 때, 점 C에서 원점까지의 거리는 [[d]]이다. [[pow(d,2)]]의 값을 구하시오."),
    choices=None, derived_answer="7",
    figure=fig("평면 α와 그에 수직인 직선 l(교점 A), l 위의 점 C, α 위의 점 B를 이은 직각삼각형 ABC; A에 직각 표시, AB와 AC에 같은 길이 표시"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 평면 α·수직 직선 l·삼각형 ABC 그림",
    note="출처 [2013년 9월 고3 이과 28번/4점]. α: x+2y-z=0 → a=1, AB=√5=AC → t²=5/6, d²=2+6t²=7. 빠른정답 9와 불일치.")

add(id="94a507eb", qtype="choice",
    question=("다음 그림과 같이 직선 [[l]]: [[frac(x - 1, 2) = y - 1 = frac(1 - z, 2)]]와 평면 [[alpha]]가 점 [[A(1, 1, 1)]]에서 수직으로 만난다. "
              "평면 [[alpha]] 위의 점 [[B(4, a, 1)]]과 직선 [[l]] 위의 점 C에 대하여 삼각형 ABC가 [[seg(AB) = seg(AC)]]인 이등변삼각형일 때, 선분 BC의 길이는?"),
    choices=["[[5 sqrt(2)]]", "[[2 sqrt(15)]]", "[[sqrt(70)]]", "[[4 sqrt(5)]]", "[[3 sqrt(10)]]"],
    derived_answer="⑤",
    figure=fig("평면 α(음영)와 그에 수직인 직선 l(교점 A), l 위의 점 C, α 위의 점 B를 이은 삼각형 ABC; A에 직각 표시, AB와 AC에 같은 길이 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평면 α·수직 직선 l·삼각형 ABC 그림",
    note="α: 2x+y-2z-1=0 → a=-5, AB=3√5 → BC=√90=3√10.")

add(id="712aeb32", qtype="choice",
    question="좌표공간에서 점 [[vcomp(2, 0, 5)]]를 지나고\n직선 [[x - 1 = 2 - y = frac(z + 1, 2)]]을 포함하는 평면이\n[[x]]축과 만나는 점의 [[x]]좌표는?",
    choices=["[[frac(9,2)]]", "[[4]]", "[[frac(7,2)]]", "[[3]]", "[[frac(5,2)]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2018년 11월 고3 이과 13번/3점]. 법선 (2,4,1), 2x+4y+z-9=0 → x=9/2.")

add(id="7ad0af68", qtype="short",
    question="두 직선 [[sub(l,1)]]: [[x + 1 = frac(y - 2, 2) = frac(z, 2)]],\n[[sub(l,2)]]: [[frac(x - 3, 2) = -y - 1 = z - 2]]를 포함하는 평면의\n법선벡터가 [[vec(n) = vcomp(a, b, 1)]]일 때, [[a b]]의 값을 구하시오.",
    choices=None, derived_answer="frac(12,25)", figure=None, difficulty_est=3, confidence=0.9,
    note="(1,2,2)×(2,-1,1)=(4,3,-5) → (-4/5,-3/5,1) → ab=12/25.")

add(id="59266585", qtype="short",
    question="점 [[A(-1, 3, 0)]]을 지나고\n직선 [[l]]: [[frac(x + 1, 2) = frac(y - 1, 3) = -z]]를 포함하는 평면의\n방정식은 [[a x + b y + c z + 1 = 0]]이다. 이때 [[a + b + c]]의 값을 구하시오. (단, [[a]], [[b]], [[c]]는 상수이다.)",
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="법선 (2,3,-1)×(0,2,0)=(2,0,4) → x+2z+1=0 → 3.")

add(id="de19f988", qtype="short",
    question=("좌표공간에서 중심이 [[C(1, 2, 1)]]이고 반지름의 길이가 [[sqrt(3)]]인 구가 두 평면 [[alpha]], [[beta]]와 접하는 점을 각각 P, Q라 하자. "
              "두 평면 [[alpha]], [[beta]]의 교선의 방정식이 [[x = -y = z]]일 때, 삼각형 CPQ의 넓이는 [[S]]이다. [[100 S]]의 값을 구하시오."),
    choices=None, derived_answer="150", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2013년 10월 고3 이과 29번/4점]. C에서 교선까지 거리 √6, ∠PCQ=90° → S=3/2 → 150.")

add(id="feac1367", qtype="choice",
    question="두 평면 [[x + 3y - z + 4 = 0]], [[x - 2y + 4z - 1 = 0]]의\n교선과 직선 [[frac(x + 2, 3) = frac(y - 3, 2) = 1 - z]]를 포함하는 평면이\n점 [[vcomp(3, a, -1)]]을 지날 때, [[a]]의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="평면 3x-y+7z+2=0 (k=2) → 9-a-7+2=0 → a=4. 빠른정답 2와 불일치.")

add(id="dd93d93c", qtype="choice",
    question="두 평면 [[x + y + z = 1]], [[2x + y - z = -2]]가 만나서\n생기는 교선이 xy평면, yz평면과 만나는 점을 각각\nP, Q라 할 때, 선분 PQ의 길이는?",
    choices=["[[frac(3 sqrt(6), 2)]]", "[[frac(6 sqrt(2), 2)]]", "[[frac(3 sqrt(10), 2)]]", "[[frac(6 sqrt(3), 2)]]", "[[frac(3 sqrt(14), 2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="P(-3,4,0), Q(0,-1/2,3/2) → PQ=√(63/2)=3√14/2. 빠른정답 1과 불일치.")

add(id="e5b011b6", qtype="choice",
    question="직선 [[frac(x - 1, 5) = frac(y - 3, 2) = z + 2]]가 평면 [[z = -1]]과 만나는\n점의 좌표를 [[vcomp(a, b, c)]]라 할 때, [[a + b + c]]의 값은?",
    choices=["[[8]]", "[[10]]", "[[12]]", "[[14]]", "[[16]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="t=1 → (6,5,-1) → 10.")

add(id="7d0d6e11", qtype="short",
    question="좌표공간의 원점 O에서\n두 평면 [[alpha]]: [[2x - 4y - z - 11 = 0]],\n[[beta]]: [[3x - 3y + 2z - 14 = 0]]에 내린 수선의 발을 각각\nH, H′이라 할 때, [[vec(OH)]] · vec(OH′)의 값을 구하시오.",
    choices=None, derived_answer="frac(16,3)", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="프라임 점 라벨(H′): 벡터 OH′를 텍스트 혼합으로 표기",
    note="OH=(11/21)(2,-4,-1), OH′=(7/11)(3,-3,2) → 내적 (7/21)·16 = 16/3.")

add(id="6434d39a", qtype="short",
    question="좌표공간의 점 [[A(1, 3, 0)]]에서 평면 [[sqrt(3) y - z = 0]]에\n내린 수선의 발을 B라 할 때, [[dot(vec(OA), vec(OB))]]를 구하시오.\n(단, O는 원점이다.)",
    choices=None, derived_answer="frac(13,4)", figure=None, difficulty_est=2, confidence=0.9,
    note="B=(1, 3/4, 3√3/4) → 1+9/4 = 13/4.")

add(id="42e3e94c", qtype="short",
    question="좌표공간에서 평면 [[2x - 2y + z + 5 = 0]]과 xy평면이\n이루는 각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(1,3)", figure=None, difficulty_est=1, confidence=0.9,
    note="cosθ = |1|/3 = 1/3.")

add(id="ac01c09d", qtype="short",
    question="평면 [[alpha]]: [[a x - 8y - 4z - 7 = 0]]과\n직선 [[l]]: [[frac(x + 1, 2) = frac(y - 5, b) = 2 - z]]가 서로 수직일 때,\n실수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="(a,-8,-4)∥(2,b,-1) → a=8, b=-2 → 6.")

add(id="006cb93d", qtype="choice",
    question=("좌표공간에서 직선 [[l]]: [[frac(x, 2) = 6 - y = z - 6]]과\n평면 [[alpha]]가 점 [[P(2, 5, 7)]]에서 수직으로 만난다.\n"
              "직선 [[l]] 위의 점 [[A(a, b, c)]]와 평면 [[alpha]] 위의 점 Q에 대하여\n[[dot(vec(AP), vec(AQ)) = 6]]일 때, [[a + b + c]]의 값은? (단, [[a > 0]])"),
    choices=["[[15]]", "[[16]]", "[[17]]", "[[18]]", "[[19]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2014년 11월 고3 이과 19번/4점]. AP·AQ=|AP|²=6(t-1)²=6 → t=2 → A(4,4,8) → 16. 빠른정답 6과 불일치.")

add(id="db665a34", qtype="short",
    question="두 점 [[A(4, 6, -2)]], [[B(-1, 3, 1)]]이\n평면 [[alpha]]: [[x - 3y + 2z = 3]]에 대하여 같은 쪽에 있다.\n평면 [[alpha]] 위의 점 P에 대하여 [[seg(AP) + seg(BP)]]의 최솟값이 [[m]]일\n때, [[pow(m,2)]]의 값을 구하시오.",
    choices=None, derived_answer="109", figure=None, difficulty_est=3, confidence=0.9,
    note="A의 대칭점 (7,-3,4), B까지 거리² = 64+36+9 = 109.")

add(id="0c77c77a", qtype="short",
    question="점 [[vcomp(3, 1, -4)]]와 평면 [[x - 4y - 8z - 13 = 0]] 사이의\n거리를 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.9,
    note="|3-4+32-13|/9 = 2. 빠른정답 4와 불일치(다음 문항과 뒤바뀐 듯).")

add(id="ef0543e6", qtype="short",
    question="점 [[vcomp(2, 3, -1)]]과 평면 [[x - 2y + 2z - 6 = 0]] 사이의\n거리를 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="|2-6-2-6|/3 = 4. 빠른정답 2와 불일치(앞 문항과 뒤바뀐 듯).")

add(id="24ec5d36", qtype="choice",
    question="두 점 [[A(3, -1, 4)]], [[P(x, y, z)]]의 위치벡터를 각각\n[[vec(a)]], [[vec(p)]]라 할 때, [[dot(vec(p) - vec(a), vec(p) - vec(a)) = 9]]를 만족시키는\n점 P가 나타내는 도형은?",
    choices=["중심이 점 [[vcomp(frac(3,2), -frac(1,2), 2)]]이고 반지름의 길이가 3인 구",
             "중심이 점 [[vcomp(3, -1, 4)]]이고 반지름의 길이가 3인 구",
             "중심이 점 [[vcomp(3, -1, 4)]]이고 반지름의 길이가 9인 구",
             "중심이 점 [[vcomp(6, -2, 8)]]이고 반지름의 길이가 3인 구",
             "중심이 점 [[vcomp(6, -2, 8)]]이고 반지름의 길이가 9인 구"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="|p-a|²=9 → 중심 A, 반지름 3. 빠른정답 29와 불일치.")

add(id="483156b6", qtype="choice",
    question="평면 [[a]]와\n구 [[C]]: [[pow(x,2) + pow(y,2) + pow(z,2) - 2x + 2y + 2z - 3 = 0]]이\n점 [[A(2, 0, -3)]]에서 접할 때, 평면 [[a]]에 평행하고\n구 [[C]]와 접하는 평면의 방정식은?",
    choices=["[[x + y + 2z = 0]]", "[[x + y - 2z + 4 = 0]]", "[[x + y - 2z = 0]]", "[[x - y + z + 1 = 0]]", "[[x - y - z - 1 = 0]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2005년 9월 고3 이과 12번]. 중심 (1,-1,-1), 법선 (1,1,-2), 반대쪽 접점 (0,-2,1) → x+y-2z+4=0.")

add(id="5cd2052d", qtype="short",
    question="점 [[A(3, -2, -4)]]와 벡터 [[vec(n) = vcomp(2, -1, -2)]]에\n대하여 점 P가 [[dot(vec(AP), vec(n)) = 0]]을 만족시킬 때, 선분 OP의\n길이의 최솟값을 구하시오. (단, O는 원점이다.)",
    choices=None, derived_answer="frac(16,3)", figure=None, difficulty_est=2, confidence=0.75,
    needs_review="이미지에 별개 문항 2개 인쇄(둘째: 위치벡터 a, b, x의 자취 <보기> ㄱㄴㄷ 선택형), id는 1개 — 빠른정답 16/3에 대응하는 첫째 문항만 전사",
    note=("평면 2x-y-2z-16=0, 원점과 거리 16/3. 둘째 문항: 「좌표공간의 세 점 A, B, P의 위치벡터를 각각 a, b, x라 할 때, 옳은 것만을 보기에서 있는 대로 고른 것은? "
          "ㄱ. x = b + t(a - b) (단, t는 실수)를 만족시키는 점 P의 자취는 두 점 A, B를 지나는 직선이다. ㄴ. |x - a| = 4를 만족시키는 점 P의 자취는 점 A를 중심으로 하는 구이다. "
          "ㄷ. (x - a)·(b - a) = 0을 만족시키는 점 P의 자취는 점 A를 지나고 직선 AB에 수직인 평면이다. ① ㄱ ② ㄴ ③ ㄱ, ㄴ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ」(답 ⑤)."))

# ───────────────────────── 포물선 ─────────────────────────
add(id="8e5bf629", qtype="choice",
    question=("두 양수 [[a]], [[p]]에 대하여 포물선 [[pow(y - a, 2) = 4 p x]]의 초점을 [[sub(F,1)]]이라 하고, 포물선 [[pow(y,2) = -4x]]의 초점을 [[sub(F,2)]]라 하자. "
              "선분 F₁F₂가 두 포물선과 만나는 점을 각각 P, Q라 할 때, F₁F₂ = 3, [[seg(PQ) = 1]]이다. [[pow(a,2) + pow(p,2)]]의 값은?"),
    choices=["[[6]]", "[[frac(25,4)]]", "[[frac(13,2)]]", "[[frac(27,4)]]", "[[7]]"],
    derived_answer="⑤",
    figure=fig("좌표평면: 오른쪽으로 열린 포물선 (y−a)²=4px(초점 F₁)와 왼쪽으로 열린 포물선 y²=−4x(초점 F₂, x축 위), 선분 F₁F₂가 두 포물선과 만나는 점 P, Q"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 두 포물선과 선분 F₁F₂ 좌표평면 그림 / 첨자 점 라벨(선분 F₁F₂ 윗줄 표기 생략)",
    note="출처 [2021년 11월 고3 기하 28번/4점]. F₁P+QF₂=2, x좌표 차 (p+1)/3 = 1-p → p=1/2, a²=27/4 → 7. 빠른정답 90과 불일치.")

add(id="de779bd2", qtype="choice",
    question=("실수 [[p]] ([[p >= 1]])과 함수 [[f(x) = pow(x + a, 2)]]에 대하여\n두 포물선 [[sub(C,1)]]: [[pow(y,2) = 4x]], [[sub(C,2)]]: [[pow(y - 3, 2) = 4p (x - f(p))]]\n가 제1사분면에서 만나는 점을 A라 하자.\n"
              "두 포물선 [[sub(C,1)]], [[sub(C,2)]]의 초점을 각각 [[sub(F,1)]], [[sub(F,2)]]라 할 때,\nAF₁ = AF₂를 만족시키는 [[p]]가 오직 하나가 되도록 하는\n상수 [[a]]의 값은?"),
    choices=["[[-frac(3,4)]]", "[[-frac(5,8)]]", "[[-frac(1,2)]]", "[[-frac(3,8)]]", "[[-frac(1,4)]]"],
    derived_answer="①",
    figure=fig("좌표평면: 원점을 꼭짓점으로 하는 포물선 C₁(초점 F₁, x축 위)과 오른쪽으로 열린 포물선 C₂(초점 F₂), 제1사분면 교점 A"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 두 포물선 C₁·C₂ 좌표평면 그림 / 첨자 점 라벨(선분 AF₁, AF₂ 윗줄 표기 생략)",
    note="출처 [2022년 9월 고3 기하 28번/4점]. AF₁=AF₂ ⇔ f(p)=p-1 ⇔ p²+(2a-1)p+a²+1=0, 판별식 -4a-3=0 → a=-3/4 (p=5/4).")

add(id="994fc2da", qtype="short",
    question=("초점이 F인 포물선 [[pow(y,2) = 12x]] 위의 점 중 제1사분면에 있는 점 P를 지나고 [[x]]축과 평행한 직선이 포물선 [[pow(y,2) = 12x]]의 준선과 만나는 점을 F′이라 하자. "
              "점 F′을 초점, 점 P를 꼭짓점으로 하는 포물선이 포물선 [[pow(y,2) = 12x]]와 만나는 점 중 P가 아닌 점을 Q라 하자. 사각형 PF′QF의 둘레의 길이가 16일 때, 삼각형 PF′Q의 넓이는 [[frac(q,p) sqrt(3)]]이다. "
              "[[p + q]]의 값을 구하시오. (단, 점 P의 [[x]]좌표는 3보다 작고, [[p]]와 [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="39",
    figure=fig("좌표평면: 포물선 y²=12x, 초점 F, 준선 위의 점 F′, 포물선 위의 점 P(제1사분면)·Q, 삼각형 PF′Q 음영, 사각형 PF′QF"),
    difficulty_est=5, confidence=0.75,
    needs_review="도형 표현 불가: 포물선·삼각형 PF′Q 음영 좌표평면 그림 / 프라임 점 라벨(F′)",
    note="출처 [2022년 6월 고3 기하 29번 변형]. 수치 풀이: P(1, 2√3), 넓이 32√3/7 → p+q=39. 빠른정답 '- 5'와 불일치.")

add(id="5972d747", qtype="choice",
    question=("실수 [[p]] ([[p > 1]])과 함수 [[f(x) = pow(x + 2a, 2)]]에 대하여\n두 포물선\n[[sub(C,1)]]: [[pow(y,2) = 12x]], [[sub(C,2)]]: [[pow(y - 4, 2) = 12p (x - f(p))]]가\n제1사분면에서 만나는 점을 A라 하자.\n"
              "두 포물선 [[sub(C,1)]], [[sub(C,2)]]의 초점을 각각 [[sub(F,1)]], [[sub(F,2)]]라 할 때,\nAF₁ = AF₂를 만족시키는 [[p]]가 오직 하나가 되도록 하는\n상수 [[a]]의 값은?"),
    choices=["[[-frac(5,16)]]", "[[-frac(1,4)]]", "[[-frac(3,16)]]", "[[-frac(1,8)]]", "[[-frac(1,16)]]"],
    derived_answer="④",
    figure=fig("좌표평면: 원점을 꼭짓점으로 하는 포물선 C₁(초점 F₁, x축 위)과 오른쪽으로 열린 포물선 C₂(초점 F₂), 제1사분면 교점 A"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 두 포물선 C₁·C₂ 좌표평면 그림 / 첨자 점 라벨(선분 AF₁, AF₂ 윗줄 표기 생략)",
    note="출처 [2022년 9월 고3 기하 28번 변형]. f(p)=3p-3 ⇔ p²+(4a-3)p+4a²+3=0, 판별식 -24a-3=0 → a=-1/8 (p=7/4). 빠른정답 39와 불일치.")

add(id="e3e5103a", qtype="choice",
    question="꼭짓점이 점 [[point(-1, 0)]]이고 준선이 직선 [[x = -3]]인\n포물선의 방정식이 [[pow(y,2) = a x + b]]일 때,\n두 상수 [[a]], [[b]]의 합 [[a + b]]의 값은?",
    choices=["[[14]]", "[[16]]", "[[18]]", "[[20]]", "[[22]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2021년 3월 고3 기하 25번/3점]. p=2 → y²=8x+8 → 16.")

add(id="e459f577", qtype="choice",
    question=("양수 [[p]]에 대하여 두 포물선 [[pow(x,2) = 8(y + 2)]], [[pow(y,2) = 4 p x]]가 만나는 점 중 제1사분면 위의 점을 P라 하자. "
              "점 P에서 포물선 [[pow(x,2) = 8(y + 2)]]의 준선에 내린 수선의 발 H와 포물선 [[pow(x,2) = 8(y + 2)]]의 초점 F에 대하여 [[seg(PH) + seg(PF) = 40]]일 때, [[p]]의 값은?"),
    choices=["[[frac(16,3)]]", "[[6]]", "[[frac(20,3)]]", "[[frac(22,3)]]", "[[8]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2022년 10월 고3 기하 27번/3점]. PH=PF=20 → P(12,16) → 256=48p → 16/3.")

add(id="4e8cbfa5", qtype="short",
    question="좌표평면에서 초점이 F인 포물선 [[pow(x,2) = 4y]] 위의 점 A가\n[[seg(AF) = 10]]을 만족시킨다. 점 [[B(0, -1)]]에 대하여\n[[seg(AB) = a]]일 때, [[pow(a,2)]]의 값을 구하시오.",
    choices=None, derived_answer="136", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2016년 9월 고3 이과 25번/3점]. A.y=9, x²=36 → AB²=36+100=136.")

add(id="11acc6a7", qtype="choice",
    question=("그림과 같이 점 F가 초점인 포물선 [[pow(y,2) = 4 p x]] 위의 점 P를 지나고 [[y]]축에 수직인 직선이 포물선 [[pow(y,2) = -4 p x]]와 만나는 점을 Q라 하자. "
              "[[seg(OP) = seg(PF)]]이고 [[seg(PQ) = 6]]일 때, 선분 PF의 길이는? (단, O는 원점이고, [[p]]는 양수이다.)"),
    choices=["[[7]]", "[[8]]", "[[9]]", "[[10]]", "[[11]]"],
    derived_answer="③",
    figure=fig("좌표평면: 원점을 꼭짓점으로 하는 두 포물선 y²=4px(오른쪽)·y²=−4px(왼쪽), y축에 수직인 직선 위의 점 P(오른쪽 포물선)·Q(왼쪽 포물선), 초점 F(x축 위), 선분 OP·PF"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 두 포물선과 점 P·Q·F 좌표평면 그림",
    note="출처 [2019년 10월 고3 이과 11번/3점]. P.x=3, (3+p)²=9+12p → p=6 → PF=9.")

add(id="507eb50e", qtype="choice",
    question=("그림과 같이 꼭짓점이 원점 O이고\n초점이 [[F(p, 0)]] ([[p > 0]])인 포물선이 있다.\n포물선 위의 점 A에서 [[x]]축, [[y]]축에 내린 수선의 발을\n각각 B, C라 하자. [[seg(FA) = 8]]이고 사각형 OFAC의 넓이와\n"
              "삼각형 FBA의 넓이의 비가 [[ratio(2, 1)]]일 때, 삼각형 ACF의\n넓이는? (단, 점 A는 제1사분면 위의 점이고, 점 A의\n[[x]]좌표는 [[p]]보다 크다.)"),
    choices=["[[frac(27,2)]]", "[[9 sqrt(3)]]", "[[18]]", "[[12 sqrt(3)]]", "[[24]]"],
    derived_answer="④",
    figure=fig("좌표평면: 원점 O를 꼭짓점으로 하는 포물선, 초점 F(x축 위), 포물선 위의 점 A, A에서 x축·y축에 내린 수선의 발 B·C(직각 표시), 선분 AF"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 점 A·B·C·F 좌표평면 그림",
    note="출처 [2021년 4월 고3 기하 26번/3점]. x₀+p=8, x₀-p=4 → x₀=6, p=2, y₀=4√3 → 넓이 12√3.")

add(id="d01d5c4f", qtype="short",
    question="포물선 [[pow(y,2) = 8x]]의 초점 F와 포물선 위의 점 A에 대하여\n[[seg(AF) = 6]]일 때, 점 A의 [[x]]좌표를 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="x+2=6 → 4.")

add(id="20a963a1", qtype="short",
    question="포물선 [[pow(y,2) = 12x]]의 초점 F와 포물선 위의 점 A에 대하여\n[[seg(AF) = 9]]일 때, 점 A의 [[x]]좌표를 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="x+3=9 → 6.")

add(id="851d8af6", qtype="choice",
    question=("초점이 F인 포물선 [[C]]: [[pow(y,2) = 4x]] 위의 점 중\n제1사분면에 있는 점 P가 있다. 선분 PF를 지름으로\n하는 원을 [[O]]라 할 때, 원 [[O]]는 포물선 [[C]]와 서로 다른\n두 점에서 만난다. 원 [[O]]가 포물선 [[C]]와 만나는 점 중\n"
              "P가 아닌 점을 Q, 점 P에서 포물선 [[C]]의 준선에 내린\n수선의 발을 H라 하자.\n[[angle(QHP) = alpha]], [[angle(HPQ) = beta]]라 할 때, [[frac(tan(beta), tan(alpha)) = 3]]이다.\n[[frac(seg(QH), seg(PQ))]]의 값은?"),
    choices=["[[frac(4 sqrt(6), 7)]]", "[[frac(3 sqrt(11), 7)]]", "[[frac(sqrt(102), 7)]]", "[[frac(sqrt(105), 7)]]", "[[frac(6 sqrt(3), 7)]]"],
    derived_answer="④",
    figure=fig("좌표평면: 포물선 y²=4x, 초점 F, 준선, 선분 PF를 지름으로 하는 원, 포물선과 원의 교점 P·Q, P에서 준선에 내린 수선의 발 H(직각 표시), 각 α(H)·β(P) 표시"),
    difficulty_est=5, confidence=0.75,
    needs_review="도형 표현 불가: 포물선·원·점 P·Q·H·F 좌표평면 그림",
    note="출처 [2023년 4월 고3 기하 28번/4점]. 수치 풀이: QH/PQ=√105/7 → ④.")

add(id="74e6d179", qtype="short",
    question=("포물선 [[pow(y,2) = 4x]]와 직선 [[y = frac(3,4) x - frac(3,4)]]이 만나는 점 중\n제1사분면 위에 있는 점을 A라 하자. 양수 [[a]]에 대하여\n포물선 [[pow(y - 3a, 2) = 4(x - 4a)]]가 점 A를 지날 때,\n"
              "직선 [[y = frac(3,4) x - frac(3,4)]]과 포물선 [[pow(y - 3a, 2) = 4(x - 4a)]]가\n만나는 점 중 A가 아닌 점을 B라 하자. 두 점 A, B에서\n직선 [[x = -1]]에 내린 수선의 발을 각각 C, D라 할 때,\n"
              "[[seg(AC) + seg(BD) - seg(AB) = k]]이다. [[9k]]의 값을 구하시오."),
    choices=None, derived_answer="160",
    figure=fig("좌표평면: 두 포물선 y²=4x와 (y−3a)²=4(x−4a), 직선 y=(3/4)x−3/4, 교점 A·B, 직선 x=−1 위의 수선의 발 C·D(직각 표시, 점선)"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 두 포물선·직선·수선의 발 C·D 좌표평면 그림",
    note="출처 [2021년 6월 고3 기하 29번 변형]. A(9,6), a=20/9, 직선이 두 초점을 지남 → k=10+(B.x+1)-(B.x-61/9)=160/9 → 160.")

add(id="deffd0c5", qtype="short",
    question=("그림과 같이 꼭짓점이 원점 O이고 초점이\n[[F(p, 0)]] ([[p > 0]])인 포물선이 있다. 점 F를 지나고\n기울기가 [[-frac(4,3)]]인 직선이 포물선과 만나는 점 중\n제1사분면에 있는 점을 P라 하자. 직선 FP 위의 점을\n"
              "중심으로 하는 원 [[C]]가 점 P를 지나고 포물선의 준선에\n접한다. 원 [[C]]의 반지름의 길이가 3일 때, [[25 p]]의 값을\n구하시오.\n(단, 원 [[C]]의 중심의 [[x]]좌표는 점 P의 [[x]]좌표보다 작다.)"),
    choices=None, derived_answer="96",
    figure=fig("좌표평면: 원점 O를 꼭짓점으로 하는 포물선, 초점 F, 준선(세로선), F를 지나는 기울기 −4/3 직선, 교점 P(제1사분면), P를 지나고 준선에 접하는 원 C"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 포물선·직선·원 C 좌표평면 그림",
    note="출처 [2023년 3월 고3 기하 29번/4점]. P(p/4, p), 중심의 x좌표 p/4-9/5, 준선까지 5p/4-9/5=3 → p=96/25 → 96.")

add(id="c8a48711", qtype="choice",
    question=("그림과 같이 초점이 [[F(2, 0)]]이고 [[x]]축을 축으로 하는\n포물선이 원점 O를 지나는 직선과 제1사분면 위의\n두 점 A, B에서 만난다. 점 A에서 [[y]]축에 내린 수선의\n발을 H라 하자. [[seg(AF) = seg(AH)]], [[ratio(seg(AF), seg(BF)) = ratio(1, 4)]]일 때,\n선분 AF의 길이는?"),
    choices=["[[frac(13,12)]]", "[[frac(7,6)]]", "[[frac(5,4)]]", "[[frac(4,3)]]", "[[frac(17,12)]]"],
    derived_answer="③",
    figure=fig("좌표평면: x축을 축으로 하고 초점 F를 갖는 포물선(꼭짓점은 O와 F 사이), 원점 O를 지나는 직선과의 교점 A·B(제1사분면), A에서 y축에 내린 수선의 발 H(직각 표시), 선분 AF·BF"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 포물선·직선·점 A·B·H·F 좌표평면 그림",
    note="출처 [2023년 10월 고3 기하 26번/3점]. AF=AH → 준선이 y축, y²=4(x-1); x₂=4x₁, 4x₁²=5x₁ → AF=5/4.")

add(id="c74ce72c", qtype="choice",
    question=("양수 [[p]]에 대하여 좌표평면 위에 초점이 F인\n포물선 [[pow(y,2) = 4 p x]]가 있다.\n이 포물선이 세 직선 [[x = p]], [[x = 2p]], [[x = 3p]]와 만나는\n제1사분면 위의 점을 각각 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]이라 하자.\n"
              "FP₁ + FP₂ + FP₃ = 27일 때, [[p]]의 값은?"),
    choices=["[[2]]", "[[frac(5,2)]]", "[[3]]", "[[frac(7,2)]]", "[[4]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="첨자 점 라벨(선분 FP₁, FP₂, FP₃ 윗줄 표기 생략)",
    note="출처 [2023년 9월 고3 기하 27번/3점]. 2p+3p+4p=27 → p=3.")

add(id="c6cc7666", qtype="choice",
    question=("다음 그림과 같이 포물선 [[pow(y,2) = 20x]] 위의 네 점 A, B, C,\nD를 꼭짓점으로 하는 사각형 ABCD에 대하여\n두 선분 AB와 CD가 각각 [[y]]축과 평행하다.\n"
              "사각형 ABCD의 두 대각선의 교점이 포물선의 초점 F와\n일치하고 [[seg(DF) = 15]]일 때, 사각형 ABCD의 넓이는?"),
    choices=["[[frac(125 sqrt(2), 2)]]", "[[75 sqrt(2)]]", "[[100 sqrt(2)]]", "[[frac(225 sqrt(2), 2)]]", "[[125 sqrt(2)]]"],
    derived_answer="④",
    figure=fig("좌표평면: 포물선 y²=20x, 초점 F(x축 위), 포물선 위의 네 점 A·B(왼쪽, y축에 평행한 변 AB)·D·C(오른쪽, y축에 평행한 변 CD)로 이루어진 사각형 ABCD와 F에서 만나는 두 대각선"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 사각형 ABCD 좌표평면 그림",
    note="D(10,10√2), B(5/2,-5√2) → 사다리꼴 넓이 (10√2+20√2)/2·(15/2)=225√2/2.")

add(id="43c3e80b", qtype="choice",
    question="다음 그림과 같이 포물선 [[pow(y,2) = 24x]]의 초점 F를 지나는\n직선과 포물선이 만나는 두 점 A, B에서 준선 [[l]]에 내린\n수선의 발을 각각 C, D라 하자. [[seg(AC) = 8]]일 때, 선분 BD의\n길이는?",
    choices=["[[16]]", "[[18]]", "[[20]]", "[[22]]", "[[24]]"],
    derived_answer="⑤",
    figure=fig("좌표평면: 포물선 y²=24x, 초점 F, 준선 l(세로선), F를 지나는 직선과 포물선의 교점 A·B, 준선 위의 수선의 발 C·D(직각 표시)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 포물선·준선·점 A·B·C·D 좌표평면 그림",
    note="1/AF+1/BF=1/p (p=6): 1/8+1/BF=1/6 → BF=BD=24.")

add(id="eebd96b7", qtype="choice",
    question=("초점이 F인 포물선 [[C]]: [[pow(y,2) = 8x]] 위의 점 중\n제1사분면에 있는 점 P가 있다. 선분 PF를 지름으로\n하는 원을 [[O]]라 할 때, 원 [[O]]는 포물선 [[C]]와 서로\n다른 두 점에서 만난다. 원 [[O]]가 포물선 [[C]]와 만나는\n"
              "점 중 P가 아닌 점을 Q, 점 P에서 포물선 [[C]]의\n준선에 내린 수선의 발을 H라 하자.\n[[angle(QHP) = alpha]], [[angle(HPQ) = beta]]라 할 때, [[frac(tan(beta), tan(alpha)) = 5]]이다.\n[[frac(seg(QH), seg(PQ))]]의 값은?"),
    choices=["[[frac(2 sqrt(95), 11)]]", "[[frac(sqrt(385), 11)]]", "[[frac(sqrt(390), 11)]]", "[[frac(sqrt(395), 11)]]", "[[frac(20, 11)]]"],
    derived_answer="②",
    figure=fig("좌표평면: 포물선 y²=8x, 초점 F, 준선, 선분 PF를 지름으로 하는 원, 포물선과 원의 교점 P·Q, P에서 준선에 내린 수선의 발 H(직각 표시), 각 α(H)·β(P) 표시"),
    difficulty_est=5, confidence=0.75,
    needs_review="도형 표현 불가: 포물선·원·점 P·Q·H·F 좌표평면 그림",
    note="출처 [2023년 4월 고3 기하 28번 변형]. 수치 풀이: QH/PQ=√385/11 → ②.")

add(id="267c895d", qtype="choice",
    question=("포물선 [[pow(y,2) = 4 p x]] ([[p > 0]])의 초점 F를 지나는 직선이\n포물선과 서로 다른 두 점 A, B에서 만날 때,\n두 점 A, B에서 포물선의 준선에 내린 수선의 발을 각각\nC, D라 하자. [[ratio(seg(AC), seg(BD)) = ratio(3, 2)]]이고 사각형 ACDB의\n"
              "넓이가 [[frac(125, 4) sqrt(6)]]일 때, 선분 AB의 길이는?\n(단, 점 A는 제1사분면에 있다.)"),
    choices=["[[11]]", "[[frac(23,2)]]", "[[12]]", "[[frac(25,2)]]", "[[13]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2023년 7월 고3 기하 26번 변형]. AF=3k, BF=2k, cosθ=1/5, 넓이 5√6k²=125√6/4 → k=5/2 → AB=25/2.")

add(id="04aa4438", qtype="short",
    question=("다음 그림과 같이 초점이 F인 포물선 [[pow(y,2) = 4 p x]] ([[p > 0]])\n위의 한 점 A에서 포물선의 준선에 내린 수선의 발을 B라\n하고, 선분 BF와 포물선이 만나는 점을 C라 하자.\n"
              "[[seg(AB) = seg(BF)]]이고 [[seg(BC) + 2 seg(CF) = 16]]일 때, 양수 [[p]]의 값을\n구하시오."),
    choices=None, derived_answer="3",
    figure=fig("좌표평면: 포물선 y²=4px, 초점 F(x축 위), 준선(세로선) 위의 점 B(직각 표시), 포물선 위의 점 A(AB는 x축에 평행), 선분 BF와 포물선의 교점 C"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 포물선·준선·점 A·B·C·F 좌표평면 그림",
    note="△ABF 정삼각형, BF=4p, BC=8p/3, CF=4p/3 → 16p/3=16 → p=3.")

add(id="4c3c8254", qtype="choice",
    question=("초점이 F인 포물선 [[pow(y,2) = 12x]] 위의 한 점 A에서 포물선의\n준선에 내린 수선의 발을 B라 하고, 직선 BF와 포물선이\n만나는 두 점을 각각 C, D라 하자. [[seg(BC) = 2 seg(CD)]]일 때,\n삼각형 ABD의 넓이는?\n(단, [[seg(CF) < seg(DF)]]이고, 점 A는 원점이 아니다.)"),
    choices=["[[frac(1005 sqrt(6), 2)]]", "[[555 sqrt(6)]]", "[[frac(1115 sqrt(6), 2)]]", "[[560 sqrt(6)]]", "[[frac(1125 sqrt(6), 2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=4, confidence=0.9,
    note="출처 [2023년 11월 고3 기하 27번 변형]. cosθ=1/5 → B(-3,12√6), A(72,12√6), D(9/2,-3√6) → 넓이 75·15√6/2. 빠른정답 810과 불일치.")

add(id="bc7a67e6", qtype="short",
    question="다음 그림과 같이 포물선 [[pow(y,2) = -16x]] 위를 움직이는\n점 P와 두 점 [[A(-4, 0)]], [[B(-6, 6)]]에 대하여\n[[seg(AP) + seg(BP)]]의 최솟값을 구하시오.\n(단, 점 P는 제2사분면 위의 점이다.)",
    choices=None, derived_answer="10",
    figure=fig("좌표평면: 왼쪽으로 열린 포물선 y²=−16x, 점 A(−4, 0)(x축 위), 점 B(−6, 6), 포물선 위의 점 P(제2사분면), 선분 PA·PB"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 점 A·B·P 좌표평면 그림",
    note="A는 초점, 준선 x=4 → 최솟값 = B에서 준선까지 거리 10. 빠른정답 13과 불일치.")

add(id="d8c387b4", qtype="choice",
    question="다음 그림과 같이 점 [[A(7, 6)]]과 포물선 [[pow(y,2) = 16x]] 위를\n움직이는 점 P가 있다. 포물선의 초점을 F라 할 때,\n[[seg(AP) + seg(PF)]]의 최솟값은?",
    choices=["[[9]]", "[[10]]", "[[11]]", "[[12]]", "[[13]]"],
    derived_answer="③",
    figure=fig("좌표평면: 포물선 y²=16x, 초점 F(x축 위), 점 A(7, 6), 포물선 위의 점 P, 선분 AP·PF"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 점 A·P·F 좌표평면 그림",
    note="준선 x=-4 → 7+4=11.")

add(id="39cee4de", qtype="choice",
    question="그림과 같이 초점이 F인 포물선 [[pow(y,2) = 4x]] 위의 임의의 점\nP와 점 [[A(2, 2)]]에 대하여 [[seg(PA) + seg(PF)]]의 최솟값은?",
    choices=["[[2]]", "[[frac(5,2)]]", "[[3]]", "[[frac(7,2)]]", "[[4]]"],
    derived_answer="③",
    figure=fig("좌표평면: 포물선 y²=4x, 초점 F(x축 위), 점 A(2, 2), 포물선 위의 점 P, 선분 PA·PF"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 점 A·P·F 좌표평면 그림",
    note="준선 x=-1 → 2+1=3.")

add(id="fc8f04a4", qtype="choice",
    question="그림과 같이 초점이 F인 포물선 [[pow(x,2) = 10y]] 위의 임의의 점\nP와 점 [[A(-4, 4)]]에 대하여 [[seg(PA) + seg(PF)]]의 최솟값은?",
    choices=["[[5]]", "[[frac(11,2)]]", "[[6]]", "[[frac(13,2)]]", "[[7]]"],
    derived_answer="④",
    figure=fig("좌표평면: 위로 열린 포물선 x²=10y, 초점 F(y축 위), 점 A(−4, 4), 포물선 위의 점 P, 선분 PA·PF"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 점 A·P·F 좌표평면 그림",
    note="준선 y=-5/2 → 4+5/2=13/2.")

add(id="c8955697", qtype="short",
    question="다음 그림과 같이 포물선 [[pow(y,2) = 6x]] 위의 점 P와\n두 점 [[A(frac(3,2), 0)]], [[B(5, 2)]]에 대하여 [[seg(PA) + seg(PB)]]의\n최솟값을 구하시오.",
    choices=None, derived_answer="frac(13,2)",
    figure=fig("좌표평면: 포물선 y²=6x, x축 위의 점 A(3/2, 0), 점 B(5, 2), 포물선 위의 점 P, 선분 PA(수직선)·PB"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 포물선과 점 A·B·P 좌표평면 그림",
    note="A는 초점, 준선 x=-3/2 → 5+3/2=13/2.")

add(id="8d3d5fe9", qtype="choice",
    question="점 [[F(2, 0)]]과 직선 [[x = -2]]에 대하여 좌표평면 위의 한 점\n[[P(x, y)]]에서 직선 [[x = -2]]에 내린 수선의 발을 H라 하자.\n[[seg(PF) = seg(PH)]]를 만족시키는 도형의 방정식은?",
    choices=["[[pow(y,2) = -8x]]", "[[pow(y,2) = -4x]]", "[[pow(y,2) = 4x]]", "[[pow(y,2) = 8x]]", "[[pow(y,2) = 12x]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="초점 (2,0), 준선 x=-2 → y²=8x.")

add(id="e8afcd11", qtype="choice",
    question="점 [[F(0, -3)]]과 직선 [[y = 3]]에 대하여 좌표평면 위의 한\n점 [[P(x, y)]]에서 직선 [[y = 3]]에 내린 수선의 발을 H라\n하자. [[seg(PF) = seg(PH)]]를 만족시키는 도형의 방정식은?",
    choices=["[[pow(x,2) = -12y]]", "[[pow(x,2) = -8y]]", "[[pow(x,2) = -4y]]", "[[pow(x,2) = 8y]]", "[[pow(x,2) = 12y]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="초점 (0,-3), 준선 y=3 → x²=-12y.")

add(id="d4991b59", qtype="short",
    question=("다음 그림은 초점이 F이고 꼭짓점이 O인 포물선 모양의\n태양열 집열판의 단면이다. 포물선 위의 두 점 A, B는\n직선 OF에 대하여 대칭이고 직선 AB와 직선 OF의\n교점을 H라 할 때, [[seg(AH) = seg(BH) = 4]] m, [[seg(OH) = 1]] m이다.\n"
              "이 포물선의 꼭짓점 O와 초점 F 사이의 거리는 몇 m인지\n구하시오."),
    choices=None, derived_answer="4",
    figure=fig("포물선 모양 집열판 단면: 꼭짓점 O, 초점 F(수신 막대), 포물선 위의 대칭점 A·B, 직선 AB와 OF의 교점 H(직각 표시), AH=BH=4, OH=1 표시"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 포물선 집열판 단면 그림",
    note="y²=4px에 (1, 4) 대입 → p=4 → 4 m.")

add(id="5fb72e73", qtype="short",
    question=("다음 그림은 포물선 모양의 위성 안테나의 단면이다.\n전파가 위성 안테나의 점 P에 도달하면 직각으로 반사된\n후 초점의 위치에 있는 수신기 F를 지나 반대편의 점 Q를\n거쳐 다시 직각으로 되돌아 나간다고 한다. [[seg(PQ) = 20]]일 때,\n"
              "삼각형 OPQ의 넓이를 구하시오.\n(단, 점 O는 포물선의 꼭짓점의 위치에 있다.)"),
    choices=None, derived_answer="50",
    figure=fig("포물선 모양 안테나 단면: 꼭짓점 O, 초점 F, 포물선 위의 점 P·Q(선분 PQ가 F를 지나며 축 OF에 수직, 직각 표시), P·Q에서 직각으로 들어오고 나가는 전파 화살표"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 포물선 안테나 단면 그림",
    note="PQ가 축에 수직인 초점현 → 4p=20, OF=5 → 넓이 (1/2)·20·5=50.")

# ───────────────────────── 정사영 ─────────────────────────
add(id="6dd2c50c", qtype="short",
    question="다음 그림과 같은 정육면체에서 선분 CG의 평면 EFGH\n위로의 정사영을 구하시오.",
    choices=None, derived_answer="점 G",
    figure=fig("정육면체 ABCD-EFGH(윗면 ABCD, 아랫면 EFGH, 모서리 AE·BF·CG·DH, 앞면 BFGC 음영)"),
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 정육면체 ABCD-EFGH 그림",
    note="CG ⊥ 평면 EFGH → 정사영은 점 G. 빠른정답 4와 불일치(답 표기 문항).")

add(id="0aa529b3", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB와 평면 [[alpha]]가 이루는 각의 크기를 [[theta]]라 하자.\nA′B′ = 3, [[theta = deg(60)]]일 때, 선분 AB의 길이를 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="프라임 점 라벨(선분 A′B′ 윗줄 표기 생략)",
    note="AB = 3/cos60° = 6.")

add(id="d8ed08f7", qtype="choice",
    question="선분 A′B′은 길이가 6인 선분 AB의 평면 [[alpha]] 위로의\n정사영이고, 직선 AB와 평면 [[alpha]]가 이루는 각의 크기가\n[[deg(30)]]일 때, 선분 A′B′의 길이는?",
    choices=["[[sqrt(2)]]", "[[2]]", "[[3]]", "[[3 sqrt(2)]]", "[[3 sqrt(3)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="프라임 점 라벨(선분 A′B′ 윗줄 표기 생략)",
    note="6cos30° = 3√3.")

add(id="11c1449e", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB가 평면 [[alpha]]와 이루는 각의 크기를 [[theta]]라 하자.\nA′B′ = [[8 sqrt(2)]], [[theta = deg(45)]]일 때, 선분 AB의 길이를\n구하시오.",
    choices=None, derived_answer="16", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="프라임 점 라벨(선분 A′B′ 윗줄 표기 생략)",
    note="8√2/cos45° = 16. 빠른정답 3과 불일치.")

add(id="9eb87782", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB와 평면 [[alpha]]가 이루는 예각의 크기를 [[theta]]라 하자.\n[[theta = deg(60)]], A′B′ = 7일 때, 선분 AB의 길이를 구하시오.",
    choices=None, derived_answer="14", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="프라임 점 라벨(선분 A′B′ 윗줄 표기 생략)",
    note="7/cos60° = 14. 빠른정답 6과 불일치.")

add(id="567bae39", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = seg(AD) = 12]], [[seg(BF) = 7]]인\n직육면체에서 선분 DG의 평면 AEGC 위로의 정사영의\n길이를 구하시오.",
    choices=None, derived_answer="11",
    figure=fig("직육면체 ABCD-EFGH(AB=AD=12, BF=7 표시), 대각 평면 AEGC 음영, 대각선 DG"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직육면체와 대각 평면 AEGC 그림",
    note="D의 정사영 (6,6,7), G(12,12,0) → √(36+36+49)=11. 빠른정답 17과 불일치.")

add(id="72d031bb", qtype="choice",
    question=("그림과 같이 한 변의 길이가 2인 정사각형 BCDE를\n밑면으로 하고 [[seg(AB) = seg(AC) = seg(AD) = seg(AE)]]인 사각뿔\nA-BCDE가 있다. 직선 AC와 평면 BCDE가 이루는\n각의 크기가 [[frac(pi, 3)]]일 때, 삼각형 ABC의 넓이는?"),
    choices=["[[2]]", "[[sqrt(5)]]", "[[sqrt(6)]]", "[[sqrt(7)]]", "[[2 sqrt(2)]]"],
    derived_answer="④",
    figure=fig("정사각뿔 A-BCDE(밑면 정사각형 BCDE, 꼭짓점 A, 보이지 않는 모서리 AE·BE·DE는 점선)"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각뿔 A-BCDE 그림",
    note="출처 [2025년 10월 고3 기하 25번/3점]. 밑면 중심까지 √2, AC=2√2 → 높이 √7, 넓이 √7. 빠른정답 3과 불일치.")

add(id="42394853", qtype="short",
    question=("그림과 같이 [[seg(AB) = 9]], [[seg(BC) = 12]], [[cos(angle(ABC)) = frac(sqrt(3), 3)]]\n인 사면체 ABCD에 대하여 점 A의 평면 BCD 위로의\n정사영을 P라 하고 점 A에서 선분 BC에 내린\n수선의 발을 Q라 하자. [[cos(angle(AQP)) = frac(sqrt(3), 6)]]일 때,\n"
              "삼각형 BCP의 넓이는 [[k]]이다. [[pow(k,2)]]의 값을 구하시오."),
    choices=None, derived_answer="162",
    figure=fig("사면체 ABCD, A에서 평면 BCD에 내린 수선의 발 P(점선), A에서 BC에 내린 수선의 발 Q(직각 표시), 삼각형 BCP 음영"),
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 사면체 ABCD와 정사영 P·수선의 발 Q 그림",
    note="출처 [2015년 9월 고3 이과 26번/4점]. AQ=3√6, PQ=3√2/2 → 넓이 9√2 → k²=162. 빠른정답 11과 불일치.")

add(id="9398f9cc", qtype="short",
    question="평면 [[alpha]] 위에 있는 도형의 넓이를 [[S]], 이 도형의 평면 [[beta]]\n위로의 정사영의 넓이를 [[prime(S)]]이라 하고, 두 평면 [[alpha]], [[beta]]가\n이루는 각의 크기를 [[theta]]라 하자. [[prime(S) = 8]], [[theta = deg(60)]]일 때,\n[[S]]의 값을 구하시오.",
    choices=None, derived_answer="16", figure=None, difficulty_est=1, confidence=0.9,
    note="S = 8/cos60° = 16.")

add(id="45023bb7", qtype="short",
    question="평면 [[alpha]] 위에 있는 도형의 넓이를 [[S]], 이 도형의\n평면 [[beta]] 위로의 정사영의 넓이를 [[prime(S)]]이라 하고,\n두 평면 [[alpha]], [[beta]]가 이루는 각의 크기를 [[theta]]라 하자.\n[[prime(S) = 3 sqrt(3)]], [[theta = deg(30)]]일 때, [[S]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="S = 3√3/cos30° = 6.")

add(id="64f0ba14", qtype="short",
    question="평면 [[alpha]] 위에 있는 도형의 넓이를 [[S]], 이 도형의 평면 [[beta]]\n위로의 정사영의 넓이를 [[prime(S)]]이라 하고, 두 평면 [[alpha]], [[beta]]가\n이루는 각의 크기를 [[theta]]라 하자. [[S = 12]], [[prime(S) = 6]]일 때, [[theta]]의\n크기를 구하시오.",
    choices=None, derived_answer="deg(60)", figure=None, difficulty_est=1, confidence=0.9,
    note="cosθ = 6/12 = 1/2 → θ = 60°.")

add(id="c54bccaf", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB와 평면 [[alpha]]가 이루는 예각의 크기를 [[theta]]라 하자.\n[[seg(AB) = 12]], A′B′ = 3일 때, [[cos(theta)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(1,4)", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="프라임 점 라벨(선분 A′B′ 윗줄 표기 생략)",
    note="cosθ = 3/12 = 1/4.")

add(id="52eea367", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB와 평면 [[alpha]]가 이루는 예각의 크기를 [[theta]]라고 하면,\n[[seg(AB) = 12]], A′B′ = 8일 때, [[cos(theta)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(2,3)", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="프라임 점 라벨(선분 A′B′ 윗줄 표기 생략)",
    note="cosθ = 8/12 = 2/3.")
