# -*- coding: utf-8 -*-
# batch03 (52문항: h2-2 수학II opus 1of1 + sonnet 1of3 보류분) — v1.5 문법 재작업
# 핵심 교체: f′(x)→app(prime(f), x) / 조각적 정의→cases(식, 조건, …) / α(t)·β(t)→alpha(t)·beta(t)(정적분 위끝·아래끝 포함)
#            빈칸 (가)(나)(다)→box(1)(2)(3)(식 안) / 줄임표→cdots / 원문 중괄호 {…}는 소괄호
# 도형(함수 그래프)은 unsupported(raw) 유지 — 도형만 남은 항목은 통과.
# 여전히 보류: 한 이미지에 별개 문항 2개(id 1개) 1건.
# 이미지 재확인으로 초안 선지 오기 3건 정정(46·47: ④ 'ㄱ, ㄷ', 50: ② 'ㄴ').
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= esc_opus_h2-2_1of1 =================
# 0. 65460330 — 접선의 방정식 p99: 같은 이미지에 문항 2개, id 1개 → 위 문항 전사 유지, 보류 유지
add(id="65460330", qtype="choice",
    question="최고차항의 계수가 1이고 [[lim(x, 0, frac(f(x), x)) = 1]]인 사차함수 [[f(x)]]와 실수 전체의 집합에서 연속인 함수 [[g(x)]]가 모든 실수 [[x]]에 대하여 [[(g(x) - x)(g(x) - f(x)) = 0]]을 만족시킨다. 함수 [[g(x)]]가 다음 조건을 만족시킬 때, 모든 [[frac(g(-2), g(3))]]의 값의 합은?\n(가) [[lim(x, 2, frac(g(x) - g(2), x - 2))]]의 값은 존재하지 않는다.\n(나) [[x >= a]]인 모든 실수 [[x]]에 대하여 [[g(-x) = -g(x)]]를 만족시키는 실수 [[a]]의 최솟값은 4이다.",
    choices=["[[-frac(41,3)]]", "[[-13]]", "[[-frac(37,3)]]", "[[-frac(35,3)]]", "[[-11]]"],
    figure=None, confidence=0.75,
    needs_review="같은 이미지에 별개 문항 2개(위: [2025년 5월 고3 15번/4점], 아래: [2021년 사관학교 22번 변형] 주관식)인데 id 1개 — 위 문항만 전사",
    note="문법 문제 없음(원문 중괄호는 소괄호). 아래 문항: 일차함수 f, g(x)=∫₀ˣ(x−4)f(s)ds, 직선 y=tx와 y=g(x)의 교점 개수 h(t), 'g(k)=0인 모든 실수 k에 대하여 h(t)는 t=−k에서 불연속' → g(6)의 합. 답 ⑤ 유지")

# 1~2. 99c9c81f / a6a86532 — 정적분 p10(한 이미지에 id 2개): f′(2)=0 → app
dup(["99c9c81f", "a6a86532"], qtype="choice",
    question="최고차항의 계수가 1이고 [[app(prime(f), 2) = 0]]인 이차함수 [[f(x)]]가 모든 자연수 [[n]]에 대하여 [[dinteg(4, n, f(x), x) >= 0]]을 만족시킬 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(2) < 0]]\nㄴ. [[dinteg(4, 3, f(x), x) > dinteg(4, 2, f(x), x)]]\nㄷ. [[6 <= dinteg(4, 6, f(x), x) <= 14]]",
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2023년 10월 고3 14번/4점]. f′(2)를 app(prime(f), 2)로. 한 이미지에 id 2개 → 동일 전사. 답 ③ 유지")

# 3. 162bdd19 — 정적분 p31: 조각 정의 → cases
add(id="162bdd19", qtype="choice",
    question="최고차항의 계수가 1인 삼차함수 [[f(x)]]와 상수 [[k]] ([[k >= 0]])에 대하여 함수 [[g(x) = cases(3x - k, x <= k, f(x), x > k)]]가 다음 조건을 만족시킨다.\n(가) 함수 [[g(x)]]는 실수 전체의 집합에서 증가하고 미분가능하다.\n(나) 모든 실수 [[x]]에 대하여\n[[dinteg(0, x, g(t)(abs(t(t - 2)) + t(t - 2)), t) >= 0]]이고\n[[dinteg(3, x, g(t)(abs((t - 2)(t + 1)) - (t - 2)(t + 1)), t) >= 0]]\n이다.\n[[g(k + 4)]]의 최솟값은?",
    choices=["[[35]]", "[[40]]", "[[45]]", "[[50]]", "[[55]]"],
    figure=None, confidence=0.85,
    note="[2024년 6월 고3 15번 변형]. 조각 정의를 cases로(원문 중괄호는 소괄호). 답 ② 유지")

# 4. 100cec5e — 정적분 p43: 조각 정의 → cases
add(id="100cec5e", qtype="short",
    question="[[t >= 4 - 2 sqrt(2)]]인 실수 [[t]]에 대하여 실수 전체의 집합에서 정의된 함수 [[f(x)]]가 [[f(x) = cases(2 pow(x,2) + t x, x < 0, -2 pow(x,2) + t x, x >= 0)]] 일 때, 다음 조건을 만족시키는 실수 [[k]]의 최솟값을 [[g(t)]]라 하자.\n(가) 닫힌구간 [[itv(k - 1, k, cc)]]에서 함수 [[f(x)]]는 [[x = k]]에서 최댓값을 갖는다.\n(나) 닫힌구간 [[itv(k, k + 1, cc)]]에서 함수 [[f(x)]]는 [[x = k + 1]]에서 최솟값을 갖는다.\n[[6 dinteg(frac(3,2), 3, pow(4 g(t) - 2, 2), t)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2020년 7월 고3 문과 30번 변형]. 조각 정의를 cases로. 답 23 유지")

# 5. cc813a4c — 정적분 p50: 조각 정의 → cases
add(id="cc813a4c", qtype="short",
    question="최고차항의 계수가 1인 삼차함수 [[f(x)]]에 대하여 실수 전체의 집합에서 정의된 함수 [[g(x) = cases(f(x), x >= 0, -f(-x), x < 0)]]가 다음 조건을 만족시킨다.\n(가) 함수 [[g(x)]]는 실수 전체의 집합에서 연속이다.\n(나) 함수 [[abs(g(x))]]의 미분가능하지 않은 점의 개수를 [[a]]라 하고 방정식 [[abs(g(x)) = t]] ([[t]]는 실수)의 서로 다른 실근의 개수를 [[h(t)]]라 할 때, 함수 [[h(t)]]가 불연속인 점의 개수를 [[b]]라 하면 [[a + b = 4]]이다.\n(다) [[dinteg(1, 2, g(x), x) = -frac(13,4)]]\n[[f(5)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="조각 정의를 cases로. 답 50 유지(빠른정답 3과 불일치는 초안대로)")

# 6. 3b618242 — 정적분 p51: f′(x), f′(β) → app
add(id="3b618242", qtype="short",
    question="삼차함수 [[f(x)]]가 다음 조건을 만족한다.\n(가) 모든 실수 [[x]]에 대하여 [[f(-x) = -f(x)]]이다.\n(나) [[f(alpha) = 0]], [[dinteg(0, alpha, f(x), x) = frac(81,4)]]인 양수 [[alpha]]가 존재한다.\n(다) [[x >= -2]]인 모든 실수 [[x]]에 대하여 [[f(x) <= app(prime(f), x) + 18]]이고, [[f(beta) = app(prime(f), beta) + 18]]인 양수 [[beta]]가 존재한다.\n[[9(pow(alpha,2) + pow(beta,2))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(x), f′(β)를 app(prime(f), ·)으로. 답 162 유지")

# 7. 59cc175e — 정적분 p77: 조각 정의 2개 → cases
add(id="59cc175e", qtype="choice",
    question="함수 [[f(x)]]가\n[[f(x) = cases(-pow(x,2), x < 0, pow(x,2) - x, x >= 0)]]\n이고, 양수 [[a]]에 대하여 함수 [[g(x)]]를\n[[g(x) = cases(a x + a, x < -1, 0, -1 <= x < 1, a x - a, x >= 1)]]\n이라 하자. 함수 [[h(x) = dinteg(0, x, g(t) - f(t), t)]]가 오직 하나의 극값을 갖도록 하는 [[a]]의 최댓값을 [[k]]라 하자.\n[[a = k]]일 때, [[k + h(3)]]의 값은?",
    choices=["[[frac(9,2)]]", "[[frac(11,2)]]", "[[frac(13,2)]]", "[[frac(15,2)]]", "[[frac(17,2)]]"],
    figure=None, confidence=0.85,
    note="[2025년 11월 고3 15번/4점]. 조각 정의 2개를 cases로. 답 ④ 유지(빠른정답 3과 불일치는 초안대로)")

# 8. 73bd0fbf — 정적분 p81: α(t), β(t) → alpha(t), beta(t); 이를 위끝·아래끝으로 갖는 정적분 → dinteg
add(id="73bd0fbf", qtype="choice",
    question="[[p > 2]]인 상수 [[p]]에 대하여 함수 [[f(x) = pow(x,2) - p x]]가 있다. 실수 [[t]] ([[t > -2p]])에 대하여 함수 [[y = abs(f(x))]]의 그래프와 직선 [[y = 2x + t]]가 만나는 점의 [[x]]좌표 중 가장 작은 값을 [[alpha(t)]], 가장 큰 값을 [[beta(t)]]라 하자.\n열린구간 [[itv(-2p, inf, oo)]]에서 정의된 함수\n[[g(t) = dinteg(alpha(t), beta(t), (abs(f(x)) - (2x + t)), x)]]의 최댓값이 4일 때,\n[[p]]의 값은?",
    choices=["[[6]]", "[[7]]", "[[8]]", "[[9]]", "[[10]]"],
    figure=None, confidence=0.85,
    note="[2026년 5월 고3 15번 변형]. 그리스 문자 함수 α(t), β(t)를 alpha(t)·beta(t)로 쓰고 정적분의 위끝·아래끝에 넣음(원문 중괄호는 소괄호). 답 ③ 유지")

# 9. b63b8dc0 — 정적분 p86: g′(x) → app
add(id="b63b8dc0", qtype="short",
    question="두 상수 [[a]], [[b]] ([[b != 1]])과 이차함수 [[f(x)]]에 대하여 함수 [[g(x)]]가 다음 조건을 만족시킨다.\n(가) 함수 [[g(x)]]는 실수 전체의 집합에서 미분가능하고, 도함수 [[app(prime(g), x)]]는 실수 전체의 집합에서 연속이다.\n(나) [[abs(x) < 2]]일 때, [[g(x) = dinteg(0, x, -t + a, t)]]이고, [[abs(x) >= 2]]일 때, [[abs(app(prime(g), x)) = f(x)]]이다.\n(다) 함수 [[g(x)]]는 [[x = 1]], [[x = b]]에서 극값을 갖는다.\n[[g(k) = 0]]을 만족시키는 모든 실수 [[k]]의 값의 합이 [[p + q sqrt(3)]] 일 때, [[p q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 유리수이다.)",
    choices=None, figure=None, confidence=0.8,
    note="[2023년 4월 고3 22번/4점]. g′(x)를 app(prime(g), x)로. 답 32 유지(빠른정답 54와 불일치는 초안대로)")

# 10. 200a4ab8 — 정적분 p87: 조각 정의(정적분 포함) → cases
add(id="200a4ab8", qtype="choice",
    question="최고차항의 계수가 1인 이차함수 [[f(x)]]에 대하여 함수 [[g(x) = cases(f(x + 2), x < 0, dinteg(0, x, t f(t), t), x >= 0)]]이 실수 전체의 집합에서 미분가능하다. 실수 [[a]]에 대하여 함수 [[h(x)]]를 [[h(x) = abs(g(x) - g(a))]]라 할 때, 함수 [[h(x)]]가 [[x = k]]에서 미분가능하지 않은 실수 [[k]]의 개수가 1이 되도록 하는 모든 [[a]]의 값의 곱은?",
    choices=["[[-frac(4 sqrt(3), 3)]]", "[[-frac(7 sqrt(3), 6)]]", "[[-sqrt(3)]]", "[[-frac(5 sqrt(3), 6)]]", "[[-frac(2 sqrt(3), 3)]]"],
    figure=None, confidence=0.85,
    note="[2022년 7월 고3 15번/4점]. 조각 정의를 cases로. 답 ① 유지")

# 11. c20cd59e — 정적분 p88: g′(x) → app
add(id="c20cd59e", qtype="short",
    question="두 상수 [[a]], [[b]] ([[b != 2]])와 이차함수 [[f(x)]]에 대하여 함수 [[g(x)]]가 다음 조건을 만족시킨다.\n(가) 함수 [[g(x)]]는 실수 전체의 집합에서 미분가능하고, 도함수 [[app(prime(g), x)]]는 실수 전체의 집합에서 연속이다.\n(나) [[abs(x) < 3]]일 때, [[g(x) = dinteg(1, x, -2t + a, t)]]이고, [[abs(x) >= 3]]일 때, [[abs(app(prime(g), x)) = f(x)]]이다.\n(다) 함수 [[g(x)]]는 [[x = 2]], [[x = b]]에서 극값을 갖는다.\n[[g(k) = 0]]을 만족시키는 모든 실수 [[k]]의 값의 곱이 [[p + q sqrt(5)]] 일 때, [[frac(p q, 9)]]의 값을 구하시오. (단, [[p]]와 [[q]]는 유리수이다.)",
    choices=None, figure=None, confidence=0.8,
    note="[2023년 4월 고3 22번 변형]. g′(x)를 app(prime(g), x)로. 답 18 유지(빠른정답 5와 불일치는 초안대로)")

# 12. b409afc7 — 극한의 성질 p61: 조각 정의 2개 → cases
add(id="b409afc7", qtype="short",
    question="양수 [[m]]과 0이 아닌 실수 [[a]]에 대하여 두 함수\n[[f(x) = cases(pow(x,2) - (a + 1)x - pow(a,2) + 1, x <= 3m, -3x + 4a, x > 3m)]],\n[[g(x) = cases(a x - 2a, x <= m + 4, 2x + a, x > m + 4)]]가 다음 조건을 모두 만족시킨다.\n(가) [[lim(x, alpha, f(x), -) != lim(x, alpha, f(x), +)]],\n[[lim(x, beta, g(x), -) != lim(x, beta, g(x), +)]]인 실수 [[alpha]], [[beta]]가 존재한다.\n(나) 모든 실수 [[k]]에 대하여 [[lim(x, k, frac(f(x), g(x)))]]의 값이 존재한다.\n[[m + g(pow(a,2))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2022년 9월 고2 29번 변형]. 조각 정의 2개를 cases로. 답 17 유지")

# 13. 3bf30426 — 연속 p54: 조각 정의(3구간) → cases
add(id="3bf30426", qtype="short",
    question="두 자연수 [[a]], [[b]] ([[a < b < 8]])에 대하여 함수 [[f(x)]]는\n[[f(x) = cases(abs(x + 3) - 1, x < a, x - 10, a <= x < b, abs(x - 9) - 1, x >= b)]]이다. 함수 [[f(x)]]와 양수 [[k]]는 다음 조건을 만족시킨다.\n(가) 함수 [[f(x) f(x + k)]]는 실수 전체의 집합에서 연속이다.\n(나) [[f(k) < 0]]\n[[f(a) × f(b) × f(k)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2024년 7월 고3 22번/4점]. 조각 정의를 cases로(곱점 ·은 ×). 답 96 유지(빠른정답 1과 불일치는 초안대로)")

# 14. 231a3625 — 연속 p73: 조각 정의 → cases. 첫 식의 조건 두 개(x<−a, −a<x<1)는 구간별로 나눠 씀
add(id="231a3625", qtype="short",
    question="두 양수 [[a]], [[b]]와 최고차항의 계수가 1인 이차함수 [[f(x)]]에 대하여 집합 { [[x]] | [[x != -a]], [[x]]는 실수 }에서 정의된 함수 [[g(x)]]를 [[g(x) = cases(frac(b x, x + a), x < -a, frac(b x, x + a), -a < x < 1, f(x), x >= 1)]] 이라 할 때, 함수 [[g(x)]]는 [[x = 1]]에서 연속이다. 실수 [[t]]에 대하여 함수 [[y = abs(g(x))]]의 그래프와 직선 [[y = t]]가 만나는 점의 개수를 [[h(t)]]라 할 때, 함수 [[h(t)]]가 다음 조건을 만족시킨다.\n(가) 임의의 두 양수 [[sub(t,1)]], [[sub(t,2)]]에 대하여 [[sub(t,1) < sub(t,2)]]이면 [[h(sub(t,1)) >= h(sub(t,2))]]이다.\n(나) 함수 [[h(t)]]는 [[t = 0]], [[t = alpha]], [[t = beta]] ([[0 < alpha < beta]])에서만 불연속이며 [[h(0) = alpha]], [[h(alpha) = beta - 1]]이다.\n[[f(a - b)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    note="[2024년 10월 고2 30번/4점]. 조각 정의를 cases로 — 원문은 첫 식에 조건 두 개 '(x<−a, −a<x<1)'을 한 줄에 쓴 것을 같은 식·구간 둘로 나눠 표기. 정의역 집합(한글 조건)은 텍스트 유지. 답 75 유지")

# 15. c2d3ee37 — 연속 p74: 14와 같은 구조(변형)
add(id="c2d3ee37", qtype="short",
    question="두 양수 [[a]], [[b]]와 최고차항의 계수가 1인 이차함수 [[f(x)]]에 대하여 집합 { [[x]] | [[x != -a]], [[x]]는 실수 }에서 정의된 함수 [[g(x)]]를\n[[g(x) = cases(-frac(1, x + a) + b, x < -a, -frac(1, x + a) + b, -a < x < 1, f(x), x >= 1)]] 이라 할 때, 함수 [[g(x)]]는 [[x = 1]]에서 연속이다. 실수 [[t]]에 대하여 함수 [[y = abs(g(x))]]의 그래프와 직선 [[y = t]]가 만나는 점의 개수를 [[h(t)]]라 할 때, 함수 [[h(t)]]가 다음 조건을 만족시킨다.\n(가) 임의의 두 양수 [[sub(t,1)]], [[sub(t,2)]]에 대하여 [[sub(t,1) < sub(t,2)]]이면 [[h(sub(t,1)) >= h(sub(t,2))]]이다.\n(나) 함수 [[h(t)]]는 [[t = alpha]], [[t = beta]], [[t = gamma]] ([[alpha < beta < gamma]])에서만 불연속이며\n[[h(alpha) = beta]], [[h(beta) = 2b - 2]]이다.\n[[f(x)]]의 최솟값을 [[m]]이라 할 때 [[-4m]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    note="[2024년 10월 고2 30번 변형]. 조각 정의를 cases로 — 원문 첫 식의 조건 두 개 '(x<−a, −a<x<1)'을 같은 식·구간 둘로 나눠 표기. 정의역 집합(한글 조건)은 텍스트 유지. 답 14 유지")

# 16. 8e03889a — 연속 p80: 조각 정의(조건이 f(x)<k 꼴) → cases
add(id="8e03889a", qtype="short",
    question="두 실수 [[a]], [[b]]에 대하여 정의역이 [[setb(x, x >= 0)]]인 함수\n[[f(x) = frac(-a x - b + 1, a x + b)]] ([[a b > 0]])\n이 있다. 실수 [[k]]에 대하여 정의역이 [[setb(x, x >= 0)]]인 함수\n[[g(x) = cases(2k - f(x), f(x) < k, f(x), f(x) >= k)]]\n가 다음 조건을 만족시킨다.\n(가) [[lim(x, inf, abs(g(x))) = frac(1,2)]]\n(나) [[abs(g(0)) = 1]]\n(다) 함수 [[y = abs(g(x))]]의 그래프와 직선 [[y = -k]]는 두 점 [[point(frac(1,28), -k)]], [[point(alpha, -k)]]에서만 만난다. (단, [[alpha > frac(1,28)]])\n직선 [[y = m(x - 4 alpha) + frac(3,4)]]이 함수 [[y = abs(g(x))]]의 그래프와 만나는 서로 다른 점의 개수를 [[h(m)]]이라 할 때, 함수 [[h(m)]]이 불연속이 되는 모든 실수 [[m]]의 값의 합은 [[M]]이다. [[252 M]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2018년 4월 고3 문과 30번/4점]. 조각 정의를 cases로. 답 19 유지")

# 17. 11556edd — 부정적분 p62: 조각 정의 → cases
add(id="11556edd", qtype="short",
    question="최고차항의 계수가 1이고 [[x = 3]]에서 극댓값 8을 갖는 삼차함수 [[f(x)]]가 있다. 실수 [[t]]에 대하여 함수 [[g(x)]]를\n[[g(x) = cases(f(x), x >= t, -f(x) + 2f(t), x < t)]]라 할 때,\n방정식 [[g(x) = 0]]의 서로 다른 실근의 개수를 [[h(t)]]라 하자. 함수 [[h(t)]]가 [[t = a]]에서 불연속인 [[a]]의 값이 두 개일 때, [[f(8)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2022년 9월 고3 22번/4점]. 조각 정의를 cases로. 답 58 유지")

# 18. 56242511 — 함수의 그래프 p36: f′(10) → app
add(id="56242511", qtype="short",
    question="정수 [[a]] ([[a != 0]])에 대하여 함수 [[f(x)]]를 [[f(x) = pow(x,3) - 2a pow(x,2)]]이라 하자. 다음 조건을 만족시키는 모든 정수 [[k]]의 값의 곱이 [[-12]]가 되도록 하는 [[a]]에 대하여 [[app(prime(f), 10)]]의 값을 구하시오.\n함수 [[f(x)]]에 대하여\n[[frac(f(sub(x,1)) - f(sub(x,2)), sub(x,1) - sub(x,2)) × frac(f(sub(x,2)) - f(sub(x,3)), sub(x,2) - sub(x,3)) < 0]]을\n만족시키는 세 실수 [[sub(x,1)]], [[sub(x,2)]], [[sub(x,3)]]이 열린구간 [[itv(k, k + frac(3,2), oo)]]에 존재한다.",
    choices=None, figure=None, confidence=0.8,
    note="[2023년 6월 고3 22번/4점]. f′(10)을 app(prime(f), 10)으로(원문 중괄호·곱점은 소괄호·×). 답 380 유지(빠른정답 2와 불일치는 초안대로)")

# 19. fb559b75 — 함수의 그래프 p44: 조각 정의 → cases
add(id="fb559b75", qtype="short",
    question="함수 [[f(x) = cases((3 - a) pow(x,3), x >= 0, 0, x < 0)]]에 대하여 함수 [[g(x)]]를 [[g(x) = pow(abs(x), 4) - pow(abs(x), 3) + f(x)]]로 정의하자. 함수 [[g(x)]]가 극댓값을 갖도록 하는 정수 [[a]]의 최솟값을 [[sub(a,1)]]이라 하고, [[a = sub(a,1)]]일 때 함수 [[g(x)]]가 극솟값을 갖는 모든 [[x]]의 값의 합을 [[m]]이라 하자. [[sub(a,1) + 4m]]의 값을 구하시오. (단, [[a != 3]])",
    choices=None, figure=None, confidence=0.85,
    note="조각 정의를 cases로. 답 7 유지(빠른정답 2와 불일치는 초안대로)")

# 20. b9efa8cb — 함수의 그래프 p64: 조각 정의 → cases, h′(−3)+h′(4) → app
add(id="b9efa8cb", qtype="short",
    question="이차함수 [[f(x)]]는 [[x = -1]]에서 극대이고, 삼차함수 [[g(x)]]는 이차항의 계수가 0이다.\n함수 [[h(x) = cases(f(x), x <= 0, g(x), x > 0)]] 가 실수 전체의 집합에서 미분가능하고, 다음 조건을 만족시킬 때,\n[[app(prime(h), -3) + app(prime(h), 4)]]의 값을 구하시오.\n(가) 방정식 [[h(x) = h(0)]]의 모든 실근의 합은 1이다.\n(나) 닫힌구간 [[itv(-2, 3, cc)]]에서 함수 [[h(x)]]의 최댓값과 최솟값의 차는 [[3 + 4 sqrt(3)]]이다.",
    choices=None, figure=None, confidence=0.8,
    note="[2020년 6월 고3 문과 30번/4점]. 조각 정의를 cases로, h′(−3)+h′(4)를 app으로. 답 38 유지(빠른정답 2와 불일치는 초안대로)")

# 21. c4fce2f4 — 미분계수 p95: 조각 정의 → cases
add(id="c4fce2f4", qtype="short",
    question="두 자연수 [[a]], [[b]]에 대하여 두 함수 [[f(x)]], [[g(x)]]를\n[[f(x) = cases(x + 5, x < 5, abs(2x - a), x >= 5)]],\n[[g(x) = (x - 5)(x - b)]]라 하자. 함수 [[f(x) g(x)]]가 실수 전체의 집합에서 미분가능하도록 하는 [[a]], [[b]]의 모든 순서쌍 [[point(a, b)]]의 개수를 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2022년 11월 고2 29번/4점]. 조각 정의를 cases로. 답 11 유지(빠른정답 4와 불일치는 초안대로)")

# ================= esc_sonnet_h2-2_1of3 =================
# 22. d0adff9f — 접선의 방정식 p25: f′(t)g′(t) → app, 빈칸 (가)(나)(다) → box(1)(2)(3)(식 안), 점 Q 좌표 (1, (다)) → point(1, box(3))
add(id="d0adff9f", qtype="choice",
    question="서로 다른 두 점에서 만나는 두 곡선\n[[sub(C,1)]]: [[y = pow(x,2) - 2x + 2]], [[sub(C,2)]]: [[y = -pow(x,2) + a x + b]]\n의 한 교점을 P라 하고, 점 P에서 두 곡선 [[sub(C,1)]], [[sub(C,2)]]에\n접하는 직선을 각각 [[l]], [[m]]이라 하자.\n두 접선 [[l]], [[m]]이 서로 수직일 때, 곡선 [[sub(C,2)]]는\n두 실수 [[a]], [[b]]의 값에 관계없이 일정한 점 Q를 지난다.\n다음은 점 Q의 좌표를 구하는 과정이다.\n[[f(x) = pow(x,2) - 2x + 2]], [[g(x) = -pow(x,2) + a x + b]]라\n하고, 두 곡선 [[sub(C,1)]], [[sub(C,2)]]의 한 교점 P의 [[x]]좌표를\n[[t]]라 하자.\n두 접선 [[l]], [[m]]이 서로 수직이므로\n[[app(prime(f), t) app(prime(g), t) = -1]]에서\n[[4 pow(t,2) - 2(a + 2) t + box(1) = 0]] ⋯⋯ ㉠\n[[f(t) = g(t)]]에서\n[[2 pow(t,2) - (a + 2) t + 2 - b = 0]] ⋯⋯ ㉡\n㉠, ㉡에서 [[b = box(2) - a]]를\n[[y = -pow(x,2) + a x + b]]에 대입하고\n[[a]]에 관하여 정리하면,\n[[a(x - 1) - pow(x,2) - y + box(2) = 0]] ⋯⋯ ㉢\n㉢에서 [[x - 1 = 0]], [[-pow(x,2) - y + box(2) = 0]]을\n만족시키는 [[x]]와 [[y]]의 값을 구하면 점 Q의 좌표는\n[[point(1, box(3))]]이다.\n위의 (가)에 알맞은 식을 [[h(a)]]라 하고, (나)와 (다)에\n알맞은 수를 각각 [[alpha]], [[beta]]라 할 때, [[h(alpha) × h(beta)]]의 값은?",
    choices=["[[4]]", "[[8]]", "[[12]]", "[[16]]", "[[20]]"],
    figure=None, confidence=0.85,
    note="[2016년 10월 고3 문과 18번/4점]. f′(t)g′(t)를 app으로, 식 안 빈칸 (가)(나)(다)를 box(1)(2)(3)으로(문장 속 (가)(나)(다)는 텍스트). 답 ② 유지")

# 23. 2a69f954 — 접선의 방정식 p79: 2g′(2)−f′(2), f′(2)<g′(2) → app
add(id="2a69f954", qtype="choice",
    question="두 곡선 [[y = f(x)]], [[y = g(x)]]가 점 [[point(2, 2k)]] ([[k != 0]])에서\n만나고, 이 점에서의 접선은 서로 수직이다.\n곡선 [[y = f(x) pow(g(x), 2)]] 위의 점 [[point(2, 8 pow(k,3))]]에서의 접선의\n방정식이 [[y = 8 pow(k,3)]]일 때, [[2 app(prime(g), 2) - app(prime(f), 2)]]의 값은?\n(단, [[app(prime(f), 2) < app(prime(g), 2)]])",
    choices=["[[frac(sqrt(2), 2)]]", "[[sqrt(2)]]", "[[frac(3 sqrt(2), 2)]]", "[[2 sqrt(2)]]", "[[frac(5 sqrt(2), 2)]]"],
    figure=None, confidence=0.85,
    note="f′(2), g′(2)를 app으로(원문 중괄호 {g(x)}²는 pow). 답 ④ 유지")

# 24. 622556dc — 접선의 방정식 p80: 조각 정의 → cases, g′(t)=3 → app
add(id="622556dc", qtype="choice",
    question="최고차항의 계수가 1인 사차함수 [[f(x)]]에 대하여\n함수 [[g(x) = cases(f(x + 1) - 3, x < -1, f(x), x >= -1)]]은 실수 전체의\n집합에서 미분가능하고, 곡선 [[y = g(x)]] 위의\n점 [[point(0, g(0))]]에서의 접선의 방정식이 [[y = 3x + 2]]이다.\n[[app(prime(g), t) = 3]]인 서로 다른 모든 실수 [[t]]의 값의 합은?",
    choices=["[[-5]]", "[[-frac(11,2)]]", "[[-6]]", "[[-frac(13,2)]]", "[[-7]]"],
    figure=None, confidence=0.85,
    note="[2024년 10월 고3 14번 변형]. 조각 정의를 cases로, g′(t)를 app(prime(g), t)로. 답 ① 유지")

# 25. 11e9e6b6 — 정적분 p12: ∫f′(x)dx → app. 삼차함수 그래프 unsupported → 통과
add(id="11e9e6b6", qtype="choice",
    question="그림과 같이 삼차함수 [[y = f(x)]]가\n[[f(-1) = f(1) = f(2) = 0]], [[f(0) = 2]]\n를 만족시킬 때, [[dinteg(0, 2, app(prime(f), x), x)]]의 값은?",
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 삼차함수 y=f(x) 그래프 — x절편 −1, 1, 2, y절편 2(x=0 부근에서 극대), 1과 2 사이에서 극소, 원점 O"}}],
    confidence=0.85,
    note="[2012년 10월 고3 문과 10번/3점]. 피적분함수 f′(x)를 app(prime(f), x)로. 그래프는 unsupported(raw). 답 ① 유지")

# 26. 2434071b — 정적분 p26: 조각 정의 → cases
add(id="2434071b", qtype="choice",
    question="함수 [[f(x) = cases(pow(x + 1, 2), x >= 1, frac(9,2) x - frac(1,2), x < 1)]]에 대하여\n정적분 [[dinteg(0, 2, f(x), x)]]의 값은?",
    choices=["[[frac(97,12)]]", "[[frac(49,6)]]", "[[frac(33,4)]]", "[[frac(25,3)]]", "[[frac(101,12)]]"],
    figure=None, confidence=0.85,
    note="조각 정의를 cases로. 답 ① 유지(빠른정답 16과 불일치는 초안대로)")

# 27. e5ddcb85 — 정적분 p27: 조각 정의 → cases (원문 조건 x≥2 / x≤2 그대로)
add(id="e5ddcb85", qtype="short",
    question="함수 [[f(x) = cases(7x, x >= 2, 3 pow(x,2) + 2, x <= 2)]]에 대하여\n[[dinteg(0, a, f(x), x) = 54]]를 만족시키는 상수 [[a]]의 값을 구하시오.\n(단, [[a > 2]])",
    choices=None, figure=None, confidence=0.85,
    note="조각 정의를 cases로(원문 조건 x≥2, x≤2 그대로 — 경계 2에서 두 식 값 일치). 답 4 유지")

# 28. f3e04e06 — 정적분 p30: 조건 (가)의 조각 정의 → cases
add(id="f3e04e06", qtype="choice",
    question="닫힌 구간 [[itv(0, 1, cc)]]에서 연속인 함수 [[f(x)]]가\n[[f(0) = 0]], [[f(1) = 1]], [[dinteg(0, 1, f(x), x) = frac(1,3)]]을 만족시킨다.\n실수 전체의 집합에서 정의된 함수 [[g(x)]]가 다음 조건을\n만족시킬 때, [[dinteg(1, 6, g(x), x)]]의 값은?\n(가) [[g(x) = cases(-f(x - 1) + 1, 1 < x < 2, f(x), 0 <= x <= 1)]]\n(나) 모든 실수 [[x]]에 대하여 [[g(x - 2) = g(x)]]이다.",
    choices=["[[frac(5,3)]]", "[[2]]", "[[frac(7,3)]]", "[[frac(8,3)]]", "[[3]]"],
    figure=None, confidence=0.85,
    note="조각 정의를 cases로(원문 행 순서 그대로). 답 ④ 유지")

# 29. 1beeedb3 — 정적분 p39: g′(0)=0 → app, 조각 정의 → cases
add(id="1beeedb3", qtype="short",
    question="최고차항의 계수가 2이고 [[f(0) = 0]]인 삼차함수 [[f(x)]]와\n양의 실수 [[p]]에 대하여 함수 [[g(x)]]가 다음 조건을\n만족시킨다.\n(가) [[app(prime(g), 0) = 0]]\n(나) [[g(x) = cases(f(x - p) - f(-p), x < 0, f(x + p) - f(p), x >= 0)]]\n[[dinteg(0, 2p, g(x), x) = 96]]일 때, [[f(4)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2023년 3월 고3 20번 변형]. g′(0)을 app으로, 조각 정의를 cases로. 답 80 유지")

# 30. 28aaa2cc — 정적분 p41: 29와 같은 구조(원본 기출)
add(id="28aaa2cc", qtype="short",
    question="최고차항의 계수가 1이고 [[f(0) = 1]]인 삼차함수 [[f(x)]]와\n양의 실수 [[p]]에 대하여 함수 [[g(x)]]가 다음 조건을\n만족시킨다.\n(가) [[app(prime(g), 0) = 0]]\n(나) [[g(x) = cases(f(x - p) - f(-p), x < 0, f(x + p) - f(p), x >= 0)]]\n[[dinteg(0, p, g(x), x) = 20]]일 때, [[f(5)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2023년 3월 고3 20번/4점]. g′(0)을 app으로, 조각 정의를 cases로. 답 66 유지")

# 31. 5a4dc8e1 — 정적분 p48: 도함수 f′(x), |f′(x)| → app
add(id="5a4dc8e1", qtype="choice",
    question="최고차항의 계수가 양수인 사차함수 [[f(x)]]의\n도함수 [[app(prime(f), x)]]에 대하여 방정식 [[app(prime(f), x) = 0]]이\n세 실근 [[alpha]], 0, [[beta]] ([[alpha < 0 < beta]])를 갖는다.\n[[S = dinteg(alpha, 0, abs(app(prime(f), x)), x)]], [[T = dinteg(0, beta, abs(app(prime(f), x)), x)]]\n라 할 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\nㄱ. 함수 [[f(x)]]는 [[x = 0]]에서 극댓값을 갖는다.\nㄴ. [[alpha + beta = 0]]이면 [[S = T]]이다.\nㄷ. [[S < T]]이고 [[f(alpha) = 0]]이면 방정식 [[f(x) = 0]]의\n양의 실근의 개수는 2이다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="[2018년 11월 고2 이과 17번/4점]. f′(x)를 app(prime(f), x)로(정적분 피적분함수 포함). 답 ⑤ 유지(빠른정답 162와 불일치는 초안대로)")

# 32. c538bfb1 — 정적분 p49: f′(x), f′(−a)=f′(a) → app
add(id="c538bfb1", qtype="short",
    question="다항함수 [[f(x)]]와 그 도함수 [[app(prime(f), x)]]가 임의의 실수 [[a]]에\n대하여 두 등식 [[dinteg(-a, a, f(x), x) = 8a]],\n[[app(prime(f), -a) = app(prime(f), a)]]를 만족한다. 이때 [[f(0)]]의 값을\n구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(x), f′(−a)=f′(a)를 app으로. 답 4 유지(빠른정답 3과 불일치는 초안대로)")

# 33. 6d5c2d3c — 정적분 p57: 조각 정의 → cases
add(id="6d5c2d3c", qtype="short",
    question="실수 전체의 집합에서 정의된 연속함수 [[f(x)]]가\n임의의 실수 [[x]]에 대하여 [[f(x) = f(x + 4)]]를\n만족시키고 [[f(x) = cases(-4x + 8, 0 <= x < 2, pow(x,2) - 2x, 2 <= x < 4)]]일 때,\n정적분 [[dinteg(9, 11, f(x), x)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="조각 정의를 cases로. 답 10/3 유지")

# 34. 809ad3b9 — 정적분 p58: 조각 정의(3구간) → cases. 주기함수 그래프 unsupported → 통과
add(id="809ad3b9", qtype="choice",
    question="함수 [[f(x)]]는 모든 실수 [[x]]에 대하여\n[[f(x + 3) = f(x)]]를 만족시키고\n[[f(x) = cases(2x, 0 <= x < 1, 2, 1 <= x < 2, -2x + 6, 2 <= x < 3)]]이다.\n[[dinteg(-a, a, f(x), x) = 18]]일 때, 상수 [[a]]의 값은?",
    choices=["[[7]]", "[[10]]", "[[14]]", "[[16]]", "[[18]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 주기 3인 사다리꼴 톱니 모양 그래프 y=f(x)(높이 2, y=2 점선), x축 눈금 −5~5, 원점 O"}}],
    confidence=0.85,
    note="조각 정의를 cases로. 그래프는 unsupported(raw). 답 ① 유지(빠른정답 3과 불일치는 초안대로)")

# 35. 1f7ebb6a — 정적분 p68: f(0)+f′(0) → app
add(id="1f7ebb6a", qtype="short",
    question="[[f(x) = dinteg(0, x, pow(t,2) + 2t, t)]]일 때, [[f(0) + app(prime(f), 0)]]의 값을\n구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="f′(0)을 app(prime(f), 0)으로. 답 0 유지(빠른정답 2와 불일치는 초안대로)")

# 36. 2eb718f6 — 정적분 p84: 조각 정의 → cases. 그래프 unsupported → 통과
add(id="2eb718f6", qtype="short",
    question="구간 [[itv(0, 4, cc)]]에서 정의된 함수 [[f(x)]]는\n[[f(x) = cases(-x(x - 2), 0 <= x < 2, x - 2, 2 <= x <= 4)]] 이다.\n실수 [[a]] ([[0 <= a <= 2]])에 대하여 [[dinteg(a, a + 2, f(x), x)]]의\n최솟값은 [[frac(q,p)]] 이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — 0≤x<2에서 위로 볼록한 포물선 호(0, 2에서 0), 2≤x≤4에서 (2,0)부터 (4,2)까지 직선, 점선 눈금 2, 4, 원점 O"}}],
    confidence=0.85,
    note="조각 정의를 cases로. 그래프는 unsupported(raw). 답 13 유지(빠른정답 1과 불일치는 초안대로)")

# 37. 681d7fb8 — 함수의 극한 p22: 조각 정의(x=2 조건 포함) → cases. 계단형 그래프 unsupported → 통과
add(id="681d7fb8", qtype="short",
    question="함수 [[y = f(x)]]의 그래프가 그림과 같다.\n함수 [[g(x) = cases(x, x < 2, 0, x = 2, 2x - 6, x > 2)]]에 대하여\n[[lim(x, a, (f(x) - 3) × g(a))]]의 값이 존재하도록 하는 모든\n양수 [[a]]의 값의 합을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y=f(x) 그래프 — x<a에서 y=a+1 수평(x=a에서 열린 점), x≥a에서 y=−a 수평(x=a에서 닫힌 점), x=a 점선, y축 눈금 a+1·−a, 원점 O"}}],
    confidence=0.85,
    note="조각 정의를 cases로(원문 [{f(x)−3}·g(a)]의 괄호·곱점은 소괄호·×). 그래프는 unsupported(raw). 답 5 유지(빠른정답 27과 불일치는 초안대로)")

# 38. 2d675887 — 함수의 극한 p27: 조각 정의(|x| 조건) → cases
add(id="2d675887", qtype="short",
    question="함수 [[f(x) = cases(4 - x, abs(x) >= 2, 10 - pow(x,2), abs(x) < 2)]]에 대하여\n[[lim(x, a, f(x))]]의 값이 존재하지 않을 때, 상수 [[a]]의 값을\n구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="조각 정의를 cases로. 답 2 유지")

# 39. 8360295b — 함수의 극한 p47: 조각 정의(조건 x>2f(x)) → cases
add(id="8360295b", qtype="short",
    question="[[x]]가 양수일 때, [[x]]보다 작은 자연수 중에서\n소수의 개수를 [[f(x)]]라 하고, 함수 [[g(x)]]를\n[[g(x) = cases(f(x), x > 2 f(x), frac(1, f(x)), x <= 2 f(x))]]라고 하자.\n예를 들어, [[f(frac(7,2)) = 2]]이고 [[frac(7,2) < 2 f(frac(7,2))]]이므로\n[[g(frac(7,2)) = frac(1,2)]]이다. [[lim(x, 8, g(x), +) = alpha]], [[lim(x, 8, g(x), -) = beta]]라고\n할 때, [[frac(alpha, beta)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2010년 6월 고3 이과 24번]. 조각 정의를 cases로. 답 16 유지")

# 40. 459a0665 — 함수의 극한 p60: 39의 변형
add(id="459a0665", qtype="short",
    question="[[x]]가 양수일 때, [[x]]보다 작은 자연수 중에서\n소수의 개수를 [[f(x)]]라 하고, 함수 [[g(x)]]를\n[[g(x) = cases(2 f(x), x > 2 f(x), frac(1, 2 f(x)), x <= 2 f(x))]]라고 하자.\n예를 들어 [[f(frac(9,2)) = 2]]이고 [[frac(9,2) > 2 f(frac(9,2))]]이므로\n[[g(frac(9,2)) = 4]]이다. [[lim(x, 6, g(x), +) = alpha]], [[lim(x, 6, g(x), -) = beta]]라고\n할 때, [[frac(alpha, beta)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="조각 정의를 cases로. 답 36 유지(빠른정답 46과 불일치는 초안대로)")

# 41. 579487f9 — 함수의 극한 p67: 조각 정의 → cases
add(id="579487f9", qtype="short",
    question="함수 [[f(x) = cases(abs(3x - 9), x >= 1, -4 pow(x,2) + 2, x < 1)]]에 대하여\n[[lim(x, 1, f(x), -) + lim(x, 1, f(x), +) + lim(x, 5, f(x))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="조각 정의를 cases로. 답 10 유지")

# 42. bbf92e65 — 도함수 p5: 극한식 안 빈칸 (가)(나) → box(1)(2), xf′(x) → app
add(id="bbf92e65", qtype="choice",
    question="미분가능한 함수 [[f(x)]]에 대하여 다음은 도함수의\n정의를 이용하여 [[y = x f(x)]]의 도함수를 구하는\n과정이다.\n[[x f(x) = g(x)]]로 놓으면 [[y = g(x)]]에서\n[[prime(y) = lim(h, 0, frac(g(x + h) - g(x), h))]]\n= [[lim(h, 0, frac((x + h) f(x + h) - x f(x), h))]]\n= [[lim(h, 0, frac((x + h)(f(x + h) - f(x)) + box(1), h))]]\n= [[x app(prime(f), x) + box(2)]]\n위의 과정에서 (가), (나)에 알맞은 것을 순서대로 적은\n것은?",
    choices=["(가) [[-x f(x)]], (나) [[-f(x)]]", "(가) [[x f(x)]], (나) [[f(x)]]", "(가) [[-h f(x)]], (나) [[-f(x)]]", "(가) [[h f(x)]], (나) [[f(x)]]", "(가) [[h f(x)]], (나) [[2 f(x)]]"],
    figure=None, confidence=0.85,
    note="극한식 안 빈칸 (가)(나)를 box(1)(2)로, xf′(x)를 x app(prime(f), x)로(원문 중괄호는 소괄호). 선지의 (가)(나) 표는 한 줄 나열. 답 ④ 유지(빠른정답 6과 불일치는 초안대로)")

# 43. 38f8fdca — 도함수 p7: 분모 자리 빈칸 → box(1)(원문은 라벨 없는 빈 상자), f′(x) → app
add(id="38f8fdca", qtype="short",
    question="다음 빈 칸에 알맞은 말을 써넣으시오.\n실수 전체에서 미분가능한 함수 [[f(x)]]의 도함수는\n[[app(prime(f), x) = lim(h, 0, frac(f(x + h) - f(x), box(1)))]] 이다.",
    choices=None, figure=None, confidence=0.8,
    note="f′(x)를 app으로, 분모 자리 빈칸을 box(1)로 — 원문 빈 상자에는 (가) 라벨이 없음(box 표기상 □(가)로 표시됨). 답 h 유지(빠른정답 2와 불일치는 초안대로)")

# 44. e3cded4e — 도함수 p9: 빈칸 (가)(나)(다) → box(1)(2)(3)(지수 자리는 pow(t, box(2))), 줄임표 → cdots, f′(x) → app
add(id="e3cded4e", qtype="choice",
    question="다항함수 [[f(x) = pow(x, n + 2) + x]]의 도함수를 구하는 과정이다.\n[[app(prime(f), x)]]\n= [[lim(t, x, frac(box(1), t - x))]]\n= [[lim(t, x, frac((t - x)(pow(t, box(2)) + x pow(t, n) + cdots + pow(x, box(2)) + 1), t - x))]]\n= [[lim(t, x, pow(t, box(2)) + x pow(t, n) + cdots + pow(x, box(2)) + 1)]]\n= [[box(3)]]\n위의 과정에서 (가), (나), (다)에 알맞은 것을 차례대로\n나열한 것은?",
    choices=["[[(pow(t, n + 2) + t) - (pow(x, n + 2) + x)]], [[n + 1]], [[(n + 2) pow(x, n + 1) + 1]]", "[[(pow(t, n + 2) + t) - (pow(x, n + 2) + x)]], [[n + 1]], [[(n + 1) pow(x, n) + 1]]", "[[(pow(t, n + 2) + t) - (pow(x, n + 2) + x)]], [[n + 2]], [[(n + 2) pow(x, n + 1) + 1]]", "[[(pow(t, n + 2) + t) + (pow(x, n + 2) + x)]], [[n + 2]], [[(n + 1) pow(x, n) + 1]]", "[[(pow(t, n + 2) + t) + (pow(x, n + 2) + x)]], [[n + 2]], [[(n + 2) pow(x, n + 1) + 1]]"],
    figure=None, confidence=0.85,
    note="빈칸 (가)(나)(다)를 box(1)(2)(3)으로(지수 자리 t^(나)는 pow(t, box(2))), 줄임표는 cdots, f′(x)는 app. 답 ① 유지(빠른정답 4와 불일치는 초안대로)")

# 45. 44859cca — 도함수 p10: 빈칸 (가)(나)(다) → box(1)(2)(3)(인수 자리 (나)는 box(2)(…) 곱), 줄임표 → cdots, f′(x) → app
add(id="44859cca", qtype="choice",
    question="다항함수 [[f(x) = pow(x, n) + 3x]]의 도함수를 구하는 과정이다.\n[[app(prime(f), x)]]\n= [[lim(t, x, frac(box(1), t - x))]]\n= [[lim(t, x, frac(box(2)(pow(t, n - 1) + x pow(t, n - 2) + cdots + pow(x, n - 1) + 3), t - x))]]\n= [[lim(t, x, pow(t, n - 1) + x pow(t, n - 2) + cdots + pow(x, n - 1) + 3)]]\n= [[box(3)]]\n위의 과정에서 (가), (나), (다)에 알맞은 것을 차례대로\n나열한 것은?",
    choices=["[[(pow(t, n) + 3t) - (pow(x, n) + 3x)]], [[t - x]], [[pow(x, n - 1) + 3]]", "[[(pow(t, n) + 3t) - (pow(x, n) + 3x)]], [[t - x]], [[n pow(x, n - 1) + 3]]", "[[(pow(t, n) + 3t) - (pow(x, n) + 3x)]], [[t + x]], [[(n - 1) pow(x, n - 1) + 1]]", "[[(pow(t, n) + 3t) + (pow(x, n) + 3x)]], [[t - x]], [[pow(x, n - 1) + 3]]", "[[(pow(t, n) + 3t) + (pow(x, n) + 3x)]], [[t + x]], [[n pow(x, n - 1) + 3]]"],
    figure=None, confidence=0.85,
    note="빈칸 (가)(나)(다)를 box(1)(2)(3)으로(인수 자리 (나)는 box(2)와 괄호식의 곱), 줄임표는 cdots, f′(x)는 app. 답 ② 유지")

# 46. 73e02bc5 — 도함수 p16: f′(0)=3, f′(x)=6x+3 → app. 선지 ④ 원문 'ㄱ, ㄷ'로 정정(초안 'ㄴ, ㄷ' 오기)
add(id="73e02bc5", qtype="choice",
    question="미분가능한 함수 [[f(x)]]가 임의의 두 실수 [[x]], [[y]]에 대하여\n[[f(x + y) = f(x) + f(y) + 6 x y]]를 만족하고\n[[app(prime(f), 0) = 3]]일 때, 다음 보기 중 항상 옳은 것만을 있는 대로\n고른 것은?\n<보기>\nㄱ. [[f(x) + f(-x) = 6 pow(x,2)]]\nㄴ. [[app(prime(f), x) = 6x + 3]]\nㄷ. 모든 실수 [[a]]에 대하여 [[f(a) = lim(x, a, f(x))]]이다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="f′(0), f′(x)를 app으로. 이미지 재확인: 선지 ④는 'ㄱ, ㄷ'(초안 'ㄴ, ㄷ' 오기 정정). 답 ⑤ 유지(빠른정답 3과 불일치는 초안대로)")

# 47. 7f79a860 — 도함수 p17: 46의 변형. 선지 ④ 원문 'ㄱ, ㄷ'로 정정(초안 'ㄴ, ㄷ' 오기)
add(id="7f79a860", qtype="choice",
    question="미분가능한 함수 [[f(x)]]가 임의의 두 실수 [[x]], [[y]]에 대하여\n[[f(x + y) = f(x) + f(y) + 4 x y]]를 만족하고\n[[app(prime(f), 0) = 2]]일 때, 다음 보기 중 옳은 것만을 있는 대로 고른\n것은?\n<보기>\nㄱ. [[f(x) + f(-x) = 4 pow(x,2)]]\nㄴ. [[app(prime(f), x) = -4x + 2]]\nㄷ. 모든 실수 [[a]]에 대하여 [[f(a) = lim(x, a, f(x))]]이다.",
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="f′(0), f′(x)를 app으로. 이미지 재확인: 선지 ④는 'ㄱ, ㄷ'(초안 'ㄴ, ㄷ' 오기 정정). 답 ④(ㄱ, ㄷ) 유지 — 풀이(ㄱ✓ ㄴ✗ ㄷ✓)와 일치")

# 48. 21474587 — 도함수 p31: f′(−1)+f′(1) → app
add(id="21474587", qtype="choice",
    question="함수 [[f(x) = pow(3 pow(x,2) + 2x, 3)]]에 대하여 [[app(prime(f), -1) + app(prime(f), 1)]]의\n값은?",
    choices=["[[574]]", "[[578]]", "[[581]]", "[[584]]", "[[588]]"],
    figure=None, confidence=0.85,
    note="f′(−1)+f′(1)을 app으로. 답 ⑤ 유지")

# 49. c1be9f9d — 평균값 정리 p32: 2f′(c) → app, ㄴ의 조각 정의 → cases
add(id="c1be9f9d", qtype="choice",
    question="[[f(1) - f(-1) = 2 app(prime(f), c)]]를 만족시키는 [[c]]가\n열린구간 [[itv(-1, 1, oo)]]에 존재하는 함수인 것만을\n보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(x) = abs(x) - 2]]\nㄴ. [[f(x) = cases(-3x - 2, x < -1, 1, -1 <= x < 1, 3x - 2, x >= 1)]]\nㄷ. [[f(x) = -pow(x,2) + 5]]",
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="f′(c)를 app으로, ㄴ의 조각 정의를 cases로. 답 ⑤ 유지(빠른정답 3과 불일치는 초안대로)")

# 50. 86e470ea — 평균값 정리 p33: 3f′(c) → app, ㄴ의 조각 정의 → cases. 선지 ② 원문 'ㄴ'으로 정정(초안 'ㄷ' 오기)
add(id="86e470ea", qtype="choice",
    question="함수 [[f(x)]]에 대하여 [[f(2) - f(-1) = 3 app(prime(f), c)]]를\n만족시키는 [[c]]가 열린구간 [[itv(-1, 2, oo)]]에 존재하는 함수인\n것만을 보기에서 있는 대로 고른 것은?\n<보기>\nㄱ. [[f(x) = abs(2x - 1) - 1]]\nㄴ. [[f(x) = cases(-3x - 4, x <= -1, -1, -1 < x < 2, 3x - 7, x >= 2)]]\nㄷ. [[f(x) = -pow(x,2) + x + 3]]",
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"],
    figure=None, confidence=0.85,
    note="f′(c)를 app으로, ㄴ의 조각 정의를 cases로. 이미지 재확인: 선지 ②는 'ㄴ'(초안 'ㄷ' 오기 정정). 답 ⑤ 유지(빠른정답 2와 불일치는 초안대로)")

# 51. 9ef91e12 — 평균값 정리 p47: g′(c)=k → app
add(id="9ef91e12", qtype="short",
    question="함수 [[f(x)]]는 구간 [[1 <= x <= 3]]에서 미분가능하고,\n[[f(1) = 3]], [[f(3) = 2]]이다. [[g(x) = x f(x)]]이면\n[[app(prime(g), c) = k]]인 [[c]] ([[1 < c < 3]])가 존재한다.\n이때 [[k]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="g′(c)를 app(prime(g), c)로. 답 3/2 유지")
