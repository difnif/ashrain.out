# -*- coding: utf-8 -*-
# esc_sonnet_m2-1_1of4 — 이미지 기준 전사 (82 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= 일차부등식 =================
# p6 일차부등식의 조건
add(id="ec0945ad", qtype="choice",
    question="부등식 [[5 pow(x,2) + a x <= b pow(x,2) - 2x + 5]]가 일차부등식이 되도록 하는 상수 [[a]], [[b]]의 조건은?",
    choices=["[[a = -2]], [[b != 5]]", "[[a != -2]], [[b = 5]]", "[[a = -2]], [[b = 5]]",
             "[[a != 2]], [[b != 5]]", "[[a != 2]], [[b = -5]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(5−b)x²+(a+2)x−5≤0 → b=5, a≠−2 → ②. 빠른정답 4와 불일치.")

# p7
add(id="a885903c", qtype="choice",
    question="부등식 [[4 pow(x,2) + a x <= b pow(x,2) - 3x + 1]]이 일차부등식이 되도록 하는 상수 [[a]], [[b]]의 조건은?",
    choices=["[[a = -3]], [[b = 4]]", "[[a != -3]], [[b = 4]]", "[[a = -3]], [[b != 4]]",
             "[[a != -3]], [[b != 4]]", "[[a != 3]], [[b != 4]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(4−b)x²+(a+3)x−1≤0 → b=4, a≠−3 → ②. 빠른정답 '4, 5'와 불일치.")

# p8
add(id="f6f1f121", qtype="choice",
    question="부등식 [[2 pow(x,2) + a x <= b pow(x,2) - 4x + 3]]이 일차부등식이 되도록 하는 상수 [[a]], [[b]]의 조건은?",
    choices=["[[a = -4]], [[b = 2]]", "[[a = -4]], [[b != 2]]", "[[a != -4]], [[b = 2]]",
             "[[a != 4]], [[b != 2]]", "[[a != 4]], [[b != -2]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="(2−b)x²+(a+4)x−3≤0 → b=2, a≠−4 → ③. 빠른정답 2와 불일치.")

# p45 x의 계수가 문자인 일차부등식
add(id="01f47134", qtype="choice",
    question="[[a < 2]]일 때, [[x]]에 관한 일차부등식 [[a x + 4 < 2x + 2a]]의 해는?",
    choices=["[[x < -2]]", "[[x > -2]]", "[[x < 2]]", "[[x > 2]]", "[[x > 1]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(a−2)x < 2(a−2), a−2<0 → x>2 → ④. 빠른정답 3과 불일치.")

# p46
add(id="7a199a93", qtype="choice",
    question="[[a < 1]]일 때, [[x]]에 대한 일차부등식 [[a x - 3 > x + 5]]를 풀면?",
    choices=["[[x > frac(8, a - 1)]]", "[[x > frac(a - 1, 8)]]", "[[x < frac(8, a - 1)]]",
             "[[x < -frac(8, a - 1)]]", "[[x < frac(8, a)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="(a−1)x > 8, a−1<0 → x < 8/(a−1) → ③. 빠른정답 4와 불일치.")

# ================= 함수와 함숫값 =================
# p5 함수의 뜻
add(id="b4dda2de", qtype="choice",
    question="다음 중 함수가 아닌 것은?",
    choices=["[[y = 2x + 1]]", "[[y = -frac(3, x)]] ([[x != 0]])", "[[y = pow(x,3)]]",
             "[[y]] = ([[x]]의 배수)", "[[y]] = ([[x]]의 절댓값)"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="x의 배수는 여러 개 대응 → 함수 아님 → ④ = 빠른정답 ✓.")

# p11 (id 3개) — 보기 상자 ㉠~㉤
dup(["2f6cf23d", "fe6ebfbc", "b2940f74"], qtype="choice",
    question=("[[x]]의 값이 4, 5, 6이고, [[y]]의 값이 1, 2, 3, 4, 5, 6 일 때, 다음 보기에서 [[y]] 가 [[x]] 의 함수인 것을 모두 고르면?\n"
              "㉠ [[x + y]] = (5의 배수)\n"
              "㉡ [[x - 2 = y]]\n"
              "㉢ [[x y]] = 짝수\n"
              "㉣ [[y]] = ([[x]] 의 약수의 개수)\n"
              "㉤ [[y]] = ([[x]] 보다 작은 소수)"),
    choices=["㉠, ㉡", "㉡", "㉢, ㉣", "㉡, ㉣", "㉠, ㉡, ㉤"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="㉠ x=4→y=1,6 ✗, ㉡ ✓, ㉢ x=4→모든 y ✗, ㉣ 4→3,5→2,6→4 ✓, ㉤ x=4→2,3 ✗ → ㉡,㉣ = ④. 빠른정답 3과 불일치. 보기 기호 ㉠~㉤은 텍스트.")

# p17
add(id="21a705e7", qtype="short",
    question=("두 변수 [[x]], [[y]]에 대하여 [[x]] = [[a]], 2, 3, 4, 5이고 [[y]] = 8, 9일 때, [[x]]를 [[x + y]]가 소수가 되도록 [[y]]에 대응시킨다. "
              "이때 함수가 되기 위한 모든 [[a]]의 값의 합을 구하시오.\n(단, [[a]]는 [[6 <= a <= 9]]인 자연수)"),
    choices=None, derived_answer="17", figure=None, difficulty_est=2, confidence=0.9,
    note="a=6(14,15 ✗), 7(15,16 ✗), 8(17 ✓), 9(17 ✓) → 8+9=17. 빠른정답 '4, 5'와 불일치.")

# p25 함수
add(id="2574c001", qtype="short",
    question=("다음 보기 중에서 [[y]]가 [[x]]의 함수인 것의 개수를 구하시오.\n<보기>\n"
              "ㄱ. [[ratio(x, y) = ratio(1, 3)]]을 만족하는 두 수 [[x]], [[y]]\n"
              "ㄴ. 곱이 2인 두 양수 [[x]], [[y]]\n"
              "ㄷ. 자연수 [[x]]와 2의 최소공배수 [[y]]\n"
              "ㄹ. 몸무게가 [[x]]kg인 사람의 키 [[y]]cm\n"
              "ㅁ. 지름의 길이가 [[x]]cm인 원의 둘레의 길이 [[y]]cm (원주율 : 3.14)\n"
              "ㅂ. 둘레의 길이가 [[x]]cm인 삼각형의 넓이 [[y]]cm²"),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄱ y=3x, ㄴ y=2/x, ㄷ 최소공배수, ㅁ y=3.14x 함수 / ㄹ, ㅂ 아님 → 4개. 빠른정답 2와 불일치.")

# p36 — 정답 ㉡(원문자)은 answer 문법 밖
add(id="9334ad53", qtype="short",
    question=("다음에서 [[y]] 를 [[x]] 의 함수라고 할 수 없는 것을 구하여라.\n"
              "㉠ 한 팩에 1000원인 우유를 [[x]] 팩 살 때 지불 금액 [[y]] 원\n"
              "㉡ 자연수 [[x]] 와 그 배수 [[y]]\n"
              "㉢ 넓이가 20cm² 인 삼각형의 밑변의 길이 [[x]]cm 와 높이 [[y]]cm"),
    choices=None, derived_answer=None, figure=None, difficulty_est=1, confidence=0.8,
    needs_review="답 표기 문법 밖: 정답 ㉡(원문자 기호)을 answer 문법으로 표현 불가 → 답 미기재",
    note="㉠ y=1000x, ㉢ y=40/x 함수 / ㉡ 배수는 여러 개 → 답 ㉡. 빠른정답 '3, 4'와 불일치.")

# p58 함숫값
add(id="2365e541", qtype="short",
    question=("다음 보기의 함수 중에서 [[f(4) = 2]]를 만족시키는 것은 모두 몇 개인지 구하시오.\n<보기>\n"
              "ㄱ. [[f(x) = 3x]]\nㄴ. [[f(x) = frac(x, 2)]]\nㄷ. [[f(x) = -frac(2, x)]]\nㄹ. [[f(x) = frac(8, x)]]"),
    choices=None, derived_answer="2개", figure=None, difficulty_est=1, confidence=0.9,
    note="ㄴ 4/2=2 ✓, ㄹ 8/4=2 ✓ → 2개. 빠른정답 '29개'와 불일치.")

# p70
add(id="8c5ac13c", qtype="short",
    question="함수 [[f(x) = frac(4, x)]]에 대하여 다음을 만족시키는 상수 [[a]]의 값을 구하시오.\n[[f(a) = -frac(1, 2)]]",
    choices=None, derived_answer="-8", figure=None, difficulty_est=1, confidence=0.9,
    note="4/a=−1/2 → a=−8 = 빠른정답 ✓.")

# p81 f(x)=(조건)꼴
add(id="930b86aa", qtype="short",
    question="함수 [[f(x)]] = (자연수 [[x]]를 7로 나눈 나머지)라 할 때, [[f(49) + f(51) + f(52)]]의 값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=1, confidence=0.9,
    note="0+2+3=5. 빠른정답 2와 불일치.")

# p83
add(id="c1bd249e", qtype="choice",
    question=("함수 [[f(x)]] = 2×(자연수 [[x]] 를 3 으로 나눈 나머지)라 할 때,\n"
              "[[f(1) + f(2) + f(3)]] + ⋯ + [[f(29) + f(30)]] 의 값은?"),
    choices=["[[40]]", "[[45]]", "[[50]]", "[[55]]", "[[60]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="3개씩 묶어 2(1+2+0)=6, 10묶음 → 60 → ⑤. 빠른정답 4와 불일치.")

# p85
add(id="41434e78", qtype="short",
    question=("자연수 [[x]]에 대하여 함수 [[y = f(x)]]를 [[y]] = ([[x]]보다 작은 소수의 개수)라 할 때, "
              "[[f(x) = 4]]를 만족시키는 모든 [[x]]의 값의 합을 구하시오."),
    choices=None, derived_answer="38", figure=None, difficulty_est=2, confidence=0.9,
    note="x보다 작은 소수가 2,3,5,7 → x=8,9,10,11 → 합 38. 빠른정답 18과 불일치.")

# p87
add(id="b8639535", qtype="choice",
    question="함수 [[f(x)]] = (자연수 [[x]]를 5로 나눈 나머지)라 할 때, [[f(1) + f(2) + f(3)]]⋯+[[f(50)]]의 값은?",
    choices=["[[90]]", "[[95]]", "[[100]]", "[[105]]", "[[110]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="5개씩 1+2+3+4+0=10, 10묶음 → 100 → ③ = 빠른정답 ✓.")

# p89
add(id="f185399f", qtype="choice",
    question="함수 [[f(x)]] = (자연수 [[x]]를 4로 나눈 나머지)라 할 때, [[f(1) + f(2) + f(3)]] + ⋯ + [[f(49) + f(50)]]의 값은?",
    choices=["[[71]]", "[[72]]", "[[73]]", "[[74]]", "[[75]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="4개씩 6, 12묶음=72, f(49)+f(50)=1+2 → 75 → ⑤. 빠른정답 379와 불일치.")

# p93
add(id="6733932e", qtype="short",
    question="함수 [[f(x)]] = (자연수 [[x]]와 30의 최대공약수)에 대하여 [[f(5) + f(14)]]의 값을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=1, confidence=0.9,
    note="5+2=7. 빠른정답 499와 불일치.")

# p96
add(id="16c4eb6d", qtype="short",
    question=("자연수 [[x]]에 대하여 함수 [[y = f(x)]]에서 [[f(x)]] = (자연수 [[x]] 이하의 소수의 개수)이고 두 수 [[a]], [[b]]에 "
              "대하여 [[a >= b]]일 때 [[S(a, b) = S(b, a) = a]]이다. 이때 [[S(6, f(x)) = 6]]을 만족시키는 자연수 [[x]]의 개수를 구하시오."),
    choices=None, derived_answer="16", figure=None, difficulty_est=3, confidence=0.85,
    note="S는 max → f(x)≤6 → x≤16(17은 7번째 소수) → 16개. 빠른정답 7과 불일치.")

# p99 — 한 이미지에 별개 문항 2개(f(20), f(30)), id 1개
add(id="068b87c7", qtype="choice",
    question="함수 [[f(x)]] = ([[x]] 이하의 소수의 개수)일 때, [[f(20)]]의 값은?",
    choices=["[[7]]", "[[8]]", "[[9]]", "[[10]]", "[[11]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="한 이미지에 별개 문항 2개(f(20)·f(30)) 인쇄, id 1개 → 첫 문항(f(20))만 전사",
    note="20 이하 소수 8개 → ②. 둘째 문항(f(30)=10 → ④)은 미전사. 빠른정답 16과 불일치.")

# ================= 유리수의 소수 표현 =================
# p5 유리수의 분류
add(id="903f607b", qtype="choice",
    question="[[m]], [[n]]은 정수일 때, 다음 중 [[frac(n, m)]]의 꼴로 나타낼 수 없는 수를 모두 고르면? (정답 2개)",
    choices=["[[0.25]]", "[[recdec(0, 24)]]", "[[1]]", "[[2.423415]]⋯", "[[pi]]"],
    derived_answer="④, ⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="순환하지 않는 무한소수 2.423415⋯와 π는 유리수 아님 → ④, ⑤. 빠른정답 '1, 4'와 불일치.")

# p8 소수의 분류
add(id="500d7c60", qtype="short",
    question="다음 수가 유한소수이면 '유'를, 무한소수이면 '무'를 (    ) 안에 써넣으시오.\n[[8.129129]]⋯ (    )",
    choices=None, derived_answer="무", figure=None, difficulty_est=1, confidence=0.9,
    note="8.129129⋯는 무한소수 → 무. 빠른정답 '4, 5'와 불일치.")

# p15 분수를 유한소수로
add(id="b786a6bf", qtype="short",
    question=("다음은 분수 [[frac(13, 250)]]을 소수로 나타내는 과정이다. [[frac(b c, a)]]의 값을 구하시오.\n"
              "[[frac(13, 250) = frac(13 × a, 250 × a) = frac(52, b) = c]]"),
    choices=None, derived_answer="13", figure=None, difficulty_est=1, confidence=0.9,
    note="a=4, b=1000, c=0.052 → bc/a=52/4=13. 빠른정답 2와 불일치.")

# p25 유한소수로 나타낼 수 있는 분수 (피보나치 정사각형 그림)
add(id="69e87dc1", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 1인 색칠된 정사각형을 기준으로 정사각형 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], [[sub(A,4)]], [[sub(A,5)]], ⋯를 "
              "규칙적으로 차례대로 붙여 나갈 때, 정사각형 [[sub(A,n)]]의 한 변의 길이를 [[sub(a,n)]]이라 하자. "
              "[[frac(sub(a, n+1), sub(a, n))]]을 정수나 유한소수로 나타낼 수 없도록 하는 8 이하의 자연수 [[n]]의 값의 합을 구하시오."),
    choices=None, derived_answer="24",
    figure=[{"fn": "unsupported", "args": {"raw": "한 변 1인 색칠 정사각형(왼쪽 위) 오른쪽에 A₁(한 변 1), 그 아래 A₂, 오른쪽 A₃, 아래 A₄, 오른쪽 A₅를 나선형으로 붙여 큰 직사각형을 이루는 그림. 오른쪽에 ⋯, 아래에 ⋮ 표시"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 피보나치 정사각형 나선 배치 그림",
    note="aₙ: 1,2,3,5,8,13,21,34,55 → 5/3, 21/13, 34/21, 55/34 불가 → n=3,6,7,8 합 24 = 빠른정답 ✓.")

# p69 순환마디
add(id="0a1a7318", qtype="short",
    question=("자연수 [[n]]에 대하여 [[sub(a,n)]]을 [[pow(2,n)]]의 일의 자리의 숫자라고 정의하고, [[sub(b,n)]]을 [[pow(3,n)]]의 일의 자리의 숫자라고 정의할 때, "
              "소수 0.[[sub(a,1)]][[sub(b,1)]][[sub(a,2)]][[sub(b,2)]][[sub(a,3)]][[sub(b,3)]] ⋯ [[sub(a,n)]][[sub(b,n)]] ⋯의 순환마디를 이루는 숫자의 합을 구하시오."),
    choices=None, derived_answer="40", figure=None, difficulty_est=3, confidence=0.85,
    note="aₙ: 2,4,8,6 / bₙ: 3,9,7,1 → 순환마디 23498761 → 합 40 = 빠른정답 ✓. 소수 자릿수 나열은 첨자 기호를 텍스트로 이어 붙임.")

# p71 순환소수의 표현 — 인쇄된 순환점 위치가 비표준(②③④)
add(id="a4ee2c72", qtype="choice",
    question="다음 중 순환소수의 표현이 올바른 것은?",
    choices=["[[2.333]]⋯ = [[recdec(2, 3)]]", "[[0.123123]]⋯ = 0.1̇2̇3̇", "[[15.49549549]] = 15̇.4.9̇",
             "[[3.4324324]]⋯ = 3̇.4̇3̇2̇", "[[1.2212212]]⋯ = [[recdec(1.2, 21)]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 순환점이 비표준 위치(②③④, 인쇄 그대로)라 유니코드 결합 점 텍스트로 전사",
    note="①만 올바른 표기(2.3̇). ②는 세 자리 모두 점, ③은 '15̇.4.9̇'로 인쇄, ④는 3̇.4̇3̇2̇, ⑤는 1.22̇1̇(순환마디 221이어야 함). 빠른정답 3과 불일치.")

# ================= 연립방정식의 활용(1) =================
# p11 세로 뺄셈 (자릿수 문자)
add(id="9dba8172", qtype="short",
    question=("다음 뺄셈을 만족시키는 한 자리 자연수 [[A]], [[B]]에 대하여 [[A B]]의 값을 구하시오.\n"
              "2 0 [[B]] 5\n− 1 [[B]] [[A]] 6\n= [[A]] 3 9"),
    choices=None, derived_answer=None, figure=None, difficulty_est=3, confidence=0.75,
    needs_review="문법 범위 밖: 세로셈(자릿수에 문자 20B5 − 1BA6 = A39) 표기를 텍스트로 전사",
    note="2075−1736=339 → A=3, B=7; AB가 곱이면 21, 두 자리 수 AB면 37 — 해석 불확실하여 답 미도출. 빠른정답 68과도 불일치.")

# ================= 일차함수와 그 그래프 =================
# p14 일차함수가 될 조건
add(id="e0f79ce2", qtype="choice",
    question="등식 [[9x(2 - 3a x) + 18b x - 3c y = 0]]이 [[x]]에 대한 일차함수가 되도록 하는 상수 [[a]], [[b]], [[c]]의 조건은?",
    choices=["[[a = 0]], [[b != -1]], [[c != 0]]", "[[a = 0]], [[b != 1]], [[c != 0]]", "[[a = 0]], [[b = -1]], [[c != 0]]",
             "[[a != 0]], [[b != -1]], [[c = 0]]", "[[a != 0]], [[b = -1]], [[c = 0]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="−27ax²+18(1+b)x−3cy=0 → a=0, b≠−1, c≠0 → ① = 빠른정답 ✓.")

# p15
add(id="385641d9", qtype="choice",
    question="[[4x(5 - 3a x) + 20b x - 2c y = 0]]이 [[x]]에 대한 일차함수가 되도록 하는 상수 [[a]], [[b]], [[c]]의 조건은?",
    choices=["[[a = 0]], [[b = -1]], [[c != 0]]", "[[a = 0]], [[b != -1]], [[c != 0]]", "[[a = 0]], [[b = 1]], [[c != 0]]",
             "[[a != 0]], [[b != -1]], [[c = 0]]", "[[a != 0]], [[b = 1]], [[c = 0]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="−12ax²+20(1+b)x−2cy=0 → a=0, b≠−1, c≠0 → ②. 빠른정답 5와 불일치.")

# p41 x절편, y절편
add(id="735362f6", qtype="choice",
    question="일차함수 [[y = -2x - 4]]의 그래프의 [[x]]절편과 [[y]]절편을 각각 구하면?",
    choices=["[[x]]절편 : [[-2]], [[y]]절편 : [[-2]]", "[[x]]절편 : [[-2]], [[y]]절편 : [[2]]", "[[x]]절편 : [[2]], [[y]]절편 : [[4]]",
             "[[x]]절편 : [[2]], [[y]]절편 : [[-4]]", "[[x]]절편 : [[-2]], [[y]]절편 : [[-4]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="x절편 −2, y절편 −4 → ⑤ = 빠른정답 ✓.")

# p50 x절편·y절편으로 미지수 (그래프 그림)
add(id="9eda0d1b", qtype="short",
    question=("아래 그림의 그래프와 평행한 일차함수 [[y = 2a x + 4a - 3]]의 그래프를 [[y]]축의 방향으로 [[b]]만큼 평행이동하였더니 "
              "[[x]]절편이 [[frac(4, 5)]]가 되었다. 이때 상수 [[a]], [[b]]에 대하여 [[4a + b]]의 값을 구하시오."),
    choices=None, derived_answer="4",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 점 (−3, 1)과 (1, −4)를 지나는 감소하는 직선(두 점의 좌표를 점선으로 표시), 원점 O"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 위 직선 그래프",
    note="기울기 −5/4=2a → a=−5/8; x절편 4/5 → b=13/2 → 4a+b=4 = 빠른정답 ✓.")

# p58 기울기
add(id="ea7a8b7a", qtype="short",
    question=("일차함수 [[y = f(x)]]가 [[x]]의 값이 [[-5]]에서 [[-2]]까지 증가할 때 [[y]]의 값은 [[k]]만큼 증가하고 서로 다른 상수 [[a]], [[b]]에 대하여 "
              "[[f(a) - 2a = f(b) - 2b]]를 만족시킨다. 이때 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 2, Δx=3 → k=6 = 빠른정답 ✓.")

# p92 좌표축과 둘러싸인 넓이 (그림)
add(id="2d521d2a", qtype="short",
    question=("아래 그림과 같이 일차함수 [[y = -frac(2, 3) a x + 6]]의 그래프가 [[x]]축, [[y]]축과 만나는 점을 각각 A, B라 하자. "
              "[[tri(AOB)]]의 넓이가 9일 때, 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="-3",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 증가하는 직선 y=−(2/3)ax+6이 x축과 A(k, 0)(원점 왼쪽), y축과 B(0, 6)에서 만나고 △AOB가 하늘색으로 색칠됨"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 위 직선과 삼각형 음영",
    note="½·|k|·6=9 → k=−3(그림상 A는 원점 왼쪽); ak=9 → a=−3. 빠른정답 3과 불일치(부호).")

# p96 두 직선과 x축 넓이
add(id="d14f2e75", qtype="short",
    question="두 일차함수 [[y = -3x + 6]], [[y = a x + 6]]의 그래프와 [[x]]축으로 둘러싸인 도형의 넓이가 15일 때, 양수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="½·6·(2+6/a)=15 → a=2. 빠른정답 '- 3'과 불일치.")

# ================= 일차함수의 그래프와 일차방정식 =================
# p10 기울기가 주어진 경우
add(id="0be94759", qtype="choice",
    question="두 점 [[point(4, -2)]], [[point(6, 8)]]을 지나는 직선과 일차방정식 [[a x - 3y + 9 = 0]]의 그래프가 서로 평행할 때, 상수 [[a]]의 값은?",
    choices=["[[3]]", "[[6]]", "[[9]]", "[[12]]", "[[15]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 5 = a/3 → a=15 → ⑤ = 빠른정답 ✓.")

# p11 (그래프 그림)
add(id="47f229a1", qtype="short",
    question="다음 그림은 일차함수 [[y = a x + b]]의 그래프이다. 이 그래프와 일차함수 [[m x + 2y = 1]]의 그래프가 서로 평행일 때, [[m]]의 값을 구하여라.",
    choices=None, derived_answer="-1",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: x절편 2, y절편 −1인 증가하는 직선, 원점 O"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 위 직선 그래프",
    note="기울기 1/2 = −m/2 → m=−1 = 빠른정답 ✓.")

# p16 기울기와 y절편
add(id="7ae0b629", qtype="choice",
    question="일차방정식 [[a x + (2 - 3b) y + 5 = 0]]의 그래프의 기울기가 3, [[y]]절편이 5일 때, 상수 [[a]], [[b]]에 대하여 [[frac(a, b)]]의 값은?",
    choices=["[[-1]]", "[[1]]", "[[3]]", "[[5]]", "[[7]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="2−3b=−1 → b=1, a=3 → a/b=3 → ③ = 빠른정답 ✓.")

# p28 점이 주어진 경우
add(id="62bdebce", qtype="choice",
    question="일차방정식 [[3x + k y - 8 = 0]]의 그래프가 점 [[point(-4, -5)]]를 지날 때, 이 그래프의 기울기와 [[y]]절편은? (단, [[k]]는 상수이다.)",
    choices=["기울기 : [[-frac(4, 3)]], [[y]]절편 : [[-2]]", "기울기 : [[-frac(3, 4)]], [[y]]절편 : [[-2]]", "기울기 : [[-frac(3, 4)]], [[y]]절편 : [[2]]",
             "기울기 : [[frac(3, 4)]], [[y]]절편 : [[-2]]", "기울기 : [[frac(3, 4)]], [[y]]절편 : [[2]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="k=−4 → y=(3/4)x−2 → ④. 빠른정답 7과 불일치.")

# p30 그래프가 주어진 경우 (그림)
add(id="13f503c2", qtype="short",
    question="다음 그래프가 일차방정식 [[a x + 3y = 13]] 의 그래프일 때, [[a]] 의 값을 구하여라.",
    choices=None, derived_answer="2",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 점 (2, 3)을 지나는 감소하는 직선(좌표를 점선으로 표시), 원점 O"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 위 직선 그래프",
    note="2a+9=13 → a=2. 빠른정답 1과 불일치.")

# p40 직선의 방정식 (조건 상자)
add(id="1b3970a7", qtype="short",
    question=("일차방정식 [[a x + y + b = 0]]의 그래프 위의 두 점 [[point(a, f(a))]], [[point(b, f(b))]]에 대하여 다음 조건을 만족할 때, "
              "[[f(3)]]의 값을 구하시오. (단, [[y = f(x)]])\n(가) [[frac(f(b) - f(a), b - a) = 2]]\n(나) [[f(0) = 6]]"),
    choices=None, derived_answer="12", figure=None, difficulty_est=2, confidence=0.9,
    note="기울기 −a=2, −b=6 → f(x)=2x+6 → f(3)=12 = 빠른정답 ✓.")

# p91 직선으로 둘러싸인 넓이 (그림)
add(id="69d6c07c", qtype="short",
    question=("다음 그림과 같이 직선 [[x = a]]가 [[x]]축과 만나는 점을 A, 직선 [[5x - 3y = 0]]과 만나는 점을 B라 하자. "
              "[[seg(AB) = 5]]일 때, 삼각형 OAB의 넓이를 구하시오. (단, O는 원점이다.)"),
    choices=None, derived_answer="frac(15,2)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점을 지나는 직선 5x−3y=0과 수직선 x=a, A(a, 0), B(두 직선의 교점), △OAB 하늘색 음영"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 위 직선·삼각형 음영",
    note="B(a, 5a/3), AB=5a/3=5 → a=3 → 넓이 ½·3·5=15/2 = 빠른정답 ✓.")

# p98 직선이 선분과 만날 조건
add(id="130753f8", qtype="short",
    question=("네 점 O[[point(0, 0)]], A[[point(6, 2)]], B[[point(4, 6)]], C[[point(2, 6)]]을 꼭짓점으로 하는 [[quad(OABC)]]가 있다. "
              "직선 [[y = m x]]가 [[seg(AB)]] 와 만나도록 정수 [[m]]의 값을 구하여라."),
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.9,
    note="OA 기울기 1/3 ≤ m ≤ OB 기울기 3/2 → 정수 m=1. 빠른정답 3과 불일치.")

# ================= 연립일차방정식 =================
# p1 연립방정식 세우기
add(id="72f5b3d2", qtype="short",
    question=("다음을 [[x]], [[y]]에 대한 연립방정식으로 나타내면 [[1500x + a y = 8000]], [[x + b y = c]] 일 때, 상수 [[a]], [[b]], [[c]]에 대하여 "
              "[[a + b + c]]의 값을 구하시오.\n"
              "입장료가 어른은 1500원, 학생은 700원인 박물관에 8000원을 내고 어른 [[x]]명과 학생 [[y]]명을 합한 8명이 들어갔다."),
    choices=None, derived_answer="709", figure=None, difficulty_est=1, confidence=0.9,
    note="a=700, b=1, c=8 → 709 = 빠른정답 ✓. 연립방정식 중괄호는 두 식 나열.")

# p2
add(id="0b1d10b2", qtype="short",
    question=("다음을 [[x]], [[y]]에 대한 연립방정식을 나타내면 [[x + y = a]], [[b x + c y = 40]] 일 때, 상수 [[a]], [[b]], [[c]]에 대하여 "
              "[[a + b + c]]의 값을 구하시오.\n"
              "자영이네 회사에서는 점심시간마다 2분짜리 음악 [[x]]곡과 3분짜리 음악 [[y]]곡을 합하여 총 15곡의 음악을 40분 동안 틀어준다."),
    choices=None, derived_answer="20", figure=None, difficulty_est=1, confidence=0.9,
    note="a=15, b=2, c=3 → 20 = 빠른정답 ✓.")

# p7
add(id="3b4661f6", qtype="choice",
    question=("가로의 길이가 세로의 길이보다 5cm 더 긴 직사각형이 있다. 둘레의 길이가 18cm 일 때, 이 직사각형의 세로의 길이를 [[x]]cm, 가로의 길이를 [[y]]cm 라 한다면, "
              "[[x]] 와 [[y]] 사이의 관계를 연립방정식으로 나타낸 것은?"),
    choices=["[[x = y + 5]], [[2x + y = 18]]", "[[x = y + 5]], [[2(x + y) = 18]]", "[[x = y + 5]], [[x + y = 18]]",
             "[[y = x + 5]], [[2(x + y) = 18]]", "[[y = x + 5]], [[x + y = 18]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="가로 y=x+5, 둘레 2(x+y)=18 → ④. 빠른정답 없음.")

# p9
add(id="de9d90d2", qtype="choice",
    question=("지호네 반 학생 25명이 체험 학습을 하러 가기 위해 버스를 탔는데 요금의 총액이 28000원이었다. 버스 요금을 교통 카드로 지불하면 1050원이고 현금으로 지불하면 "
              "1300원이다. 버스 요금을 교통 카드와 현금으로 지불한 학생 수를 각각 [[x]], [[y]]라 할 때, 다음 중 [[x]], [[y]]에 대한 연립방정식으로 옳은 것은?"),
    choices=["[[x + y = 25]], [[21x + 26y = 230]]", "[[x + y = 25]], [[21x + 26y = 560]]", "[[x + y = 25]], [[21x + 26y = 1120]]",
             "[[x + y = 25]], [[26x + 21y = 230]]", "[[x + y = 25]], [[26x + 21y = 560]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="1050x+1300y=28000 ÷50 → 21x+26y=560 → ②. 빠른정답 19와 불일치.")

# p20
add(id="1365371e", qtype="choice",
    question=("전체 학생이 33명인 현우네 반에서 남학생의 [[frac(3, 5)]]과 여학생의 [[frac(1, 3)]]이 참가하여 총 15명의 학생이 합창 대회에 나가려고 한다. "
              "이 반의 남학생 수를 [[x]], 여학생 수를 [[y]]라 할 때, [[x]], [[y]]에 대한 연립방정식으로 옳은 것은?"),
    choices=["[[x + y = 15]], [[frac(3, 5) x + frac(1, 3) y = 15]]", "[[x + y = 15]], [[frac(3, 5) x + frac(1, 3) y = 33]]",
             "[[x + y = 33]], [[frac(2, 5) x + frac(1, 3) y = 15]]", "[[x + y = 33]], [[frac(3, 5) x + frac(1, 3) y = 15]]",
             "[[x + y = 33]], [[frac(3, 5) x + frac(1, 3) y = 33]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="x+y=33, (3/5)x+(1/3)y=15 → ④. 빠른정답 없음.")

# p21
add(id="4a8923a3", qtype="choice",
    question=("주현이와 지은이가 가위바위보를 하여 이긴 사람은 2계단을 올라가고 진 사람은 1계단을 내려가기로 하였다. 얼마 후 주현이는 처음 위치보다 6계단을 "
              "올라가 있었고 지은이는 처음 위치와 같은 위치에 있었다. 주현이와 지은이가 이긴 횟수를 각각 [[x]], [[y]]라 할 때, 다음 중 [[x]], [[y]]에 대한 "
              "연립방정식으로 옳은 것은? (단, 비기는 경우는 없다.)"),
    choices=["[[-2x + y = 6]], [[-x + 2y = 0]]", "[[-2x + y = 6]], [[x - 2y = 0]]", "[[2x - y = 6]], [[-x + 2y = 0]]",
             "[[2x - y = 6]], [[-x - 2y = 0]]", "[[2x + y = 6]], [[-x - 2y = 0]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="주현 2x−y=6, 지은 2y−x=0 → ③. 빠른정답 없음.")

# p37 연립방정식의 해
add(id="af73a89f", qtype="short",
    question=("[[x]], [[y]]가 자연수일 때, 일차방정식 [[x + 3y = 10]]의 해의 개수를 [[a]], 일차방정식 [[5x + y = 22]]의 해의 개수를 [[b]], "
              "연립방정식 [[x + 3y = 10]], [[5x + y = 22]]의 해의 개수를 [[c]]라 하자. [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="a=3 (7,1),(4,2),(1,3); b=4; 연립 해 (4,2) → c=1 → 8. 빠른정답 없음.")

# p46
add(id="f7d1b2fb", qtype="choice",
    question="자연수 [[x]], [[y]]에 대하여 연립방정식 [[2x - y = 5]], [[x - 2y = -2]]의 해를 [[point(m, n)]]이라 할 때, [[2m - n]]의 값은?",
    choices=["[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="x=4, y=3 → 2·4−3=5 → ④. 빠른정답 없음.")

# p50
add(id="97064325", qtype="choice",
    question="[[x]], [[y]]가 자연수일 때, 연립방정식 [[3x - 2y = 9]], [[2x - 3y = 1]]의 해는?",
    choices=["[[x = 2]], [[y = 1]]", "[[x = 5]], [[y = 3]]", "[[x = 7]], [[y = 6]]", "[[x = 8]], [[y = 5]]", "[[x = 9]], [[y = 9]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="5x=25 → x=5, y=3 → ②. 빠른정답 1과 불일치.")

# p54
add(id="7a9f51a6", qtype="choice",
    question="[[x = 1]], [[y = 2]]를 해로 갖는 연립방정식은 어느 것인가?",
    choices=["[[-3x = 2y + 8]], [[y = x + 1]]", "[[x + y = 4]], [[x - y = 2]]", "[[y = -x]], [[y = -2x + 4]]",
             "[[2x + 3y = 8]], [[x + 2y = 5]]", "[[x + y = 8]], [[2x + y = 11]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="(1,2) 대입: ④ 2+6=8, 1+4=5 ✓. 빠른정답 없음.")

# p57
add(id="0d1990c8", qtype="choice",
    question="[[x]], [[y]]가 자연수일 때, 다음 연립방정식의 해는?\n[[2x + y = 5]], [[x + y = 4]]",
    choices=["[[x = 2]], [[y = 1]]", "[[x = 1]], [[y = 2]]", "[[x = 1]], [[y = 3]]", "[[x = 3]], [[y = 1]]", "[[x = 2]], [[y = 2]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="x=1, y=3 → ③. 빠른정답 없음.")

# p59
add(id="f30015be", qtype="choice",
    question="다음 연립방정식 중 [[x = 1]], [[y = -2]]를 해로 갖는 것은?",
    choices=["[[x + y = -1]], [[x - y = 2]]", "[[3x + y = 1]], [[x - 2y = -5]]", "[[y = x - 3]], [[y = 2x]]",
             "[[x = y + 3]], [[x = 2y]]", "[[2x + y = 0]], [[x - y = 3]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="(1,−2) 대입: ⑤ 2−2=0, 1+2=3 ✓. 빠른정답 없음.")

# ================= 일차함수의 그래프와 연립방정식 =================
# p1 교점 (그림)
add(id="fd37c82b", qtype="short",
    question=("두 일차방정식 [[x - 4y + 4 = 0]], [[3x + 4y = 0]]의 그래프와 좌표축에 평행한 두 직선 [[l]], [[m]]이 다음 그림과 같을 때, "
              "[[p q]]의 값을 구하시오."),
    choices=None, derived_answer="6",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 증가 직선 x−4y+4=0과 원점을 지나는 감소 직선 3x+4y=0, 수직선 l(x−4y+4=0의 x절편 통과), 수평선 m(l과 3x+4y=0의 교점 통과), 두 직선의 교점의 y좌표를 p로 표시(y축까지 점선), m과 x−4y+4=0의 교점의 x좌표 q(x축까지 점선)"}}],
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 위 네 직선 복합 그래프",
    note="l: x=−4, m: y=3 → q=8; 교점 (−1, 3/4) → p=3/4 → pq=6 = 빠른정답 ✓.")

# p3 (그림, 프라임 상수)
add(id="4881c5dc", qtype="choice",
    question=("다음 그림은 연립방정식 [[a x + b y = c]], [[prime(a) x + prime(b) y = prime(c)]]을 그래프로 나타낸 것이다. "
              "이 연립방정식의 해를 [[point(m, n)]]라고 할 때, [[pow(m,2) + 2n]]의 값은?"),
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 증가 직선 ax+by=c(점 (−2, 1), (0, 5) 통과)와 감소 직선 a′x+b′y=c′(점 (−3, 5) 통과)가 점 (−1, 3)에서 만남. x축 −3, −2, −1과 y축 1, 3, 5에 점선 좌표 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 두 직선 그래프 / 문법 범위 밖: 상수 a′, b′, c′의 프라임 표기를 prime()으로 우회",
    note="교점 (−1, 3) → 1+6=7 → ③ = 빠른정답 ✓.")

# p5 (그림, 프라임 상수, ㉠㉡ 라벨)
add(id="6ebd200f", qtype="choice",
    question=("[[x]], [[y]] 에 관한 연립방정식 [[a x + b y = c]] ⋯㉠, [[prime(a) x + prime(b) y = prime(c)]] ⋯㉡ 을 다음 그림과 같이 그래프를 이용하여 풀었다. "
              "해가 [[point(m, n)]]일 때,\n[[m + n]]의 값은?"),
    choices=["[[-3]]", "[[-2]]", "[[-1]]", "[[1]]", "[[2]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 증가 직선 ㉠(y절편 2)과 감소 직선 ㉡이 점 (−2, 1)에서 만남(점선으로 x=−2, y=1 표시), 원점 O"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 두 직선 그래프 / 문법 범위 밖: 상수 a′, b′, c′의 프라임 표기를 prime()으로 우회",
    note="교점 (−2, 1) → m+n=−1 → ③ = 빠른정답 ✓.")

# p12 (그림)
add(id="0e58dc78", qtype="choice",
    question="[[x]], [[y]] 에 관한 연립방정식 [[x + y - a = 0]], [[b x - y - 2 = 0]] 의 그래프가 다음과 같을 때, [[a + b]] 의 값은?",
    choices=["[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 감소 직선(y절편 4, x절편 4)과 증가 직선(y절편 −2)이 점 (2, 2)에서 만남(점선 표시), 원점 O"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 두 직선 그래프",
    note="a=4, b=2 → 6 → ⑤ = 빠른정답 ✓.")

# p13
add(id="a3106c7c", qtype="choice",
    question="연립방정식 [[x + a y = 2a]], [[b x + 3y = 6]] 을 풀기 위하여 그래프를 그렸더니 그 교점의 좌표가 [[point(4, -2)]]이었다. 이때, [[a b]] 의 값은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="4−2a=2a → a=1; 4b−6=6 → b=3 → ab=3 → ③. 빠른정답 4와 불일치.")

# p14
add(id="2662d4bb", qtype="choice",
    question="[[x]], [[y]] 에 관한 연립방정식 [[m x + n y = -4]], [[n x - 2m y = -2]] 의 그래프의 교점의 좌표가 [[point(2, 1)]] 일 때, [[m]], [[n]] 의 값을 구하면?",
    choices=["[[m = 1]], [[n = 2]]", "[[m = 2]], [[n = 1]]", "[[m = -1]], [[n = -2]]", "[[m = 1]], [[n = 3]]", "[[m = 2]], [[n = -1]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="2m+n=−4, 2n−2m=−2 → m=−1, n=−2 → ③. 빠른정답 4와 불일치.")

# p17 (그림)
add(id="8ffca536", qtype="short",
    question=("다음 그림은 연립방정식 [[x + y = 3]], [[a x - 3y = 3]]의 해를 구하기 위하여 두 일차방정식의 그래프를 그린 것이다. "
              "이때 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="9",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 감소 직선 x+y=3과 증가 직선 ax−3y=3이 x좌표 1인 점에서 만남(점선으로 x=1과 y좌표 표시), 원점 O"}}],
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 좌표평면 두 직선 그래프",
    note="교점 (1, 2) → a−6=3 → a=9 = 빠른정답 ✓.")

# p26 교점을 지나는 직선
add(id="b1b9b403", qtype="choice",
    question="두 직선 [[y = -2x + 6]], [[y = a x - 2]]의 교점이 두 점 [[point(0, 2)]], [[point(-1, 3)]]을 지나는 직선 위에 있을 때, 상수 [[a]]의 값은?",
    choices=["[[-1]]", "[[0]]", "[[1]]", "[[2]]", "[[3]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="직선 y=−x+2와 y=−2x+6의 교점 (4, −2) → −2=4a−2 → a=0 → ②. 빠른정답 3과 불일치.")

# p27
add(id="e41f2bc8", qtype="choice",
    question="두 직선 [[x - 2y = 11]], [[a x - y = -2]]의 교점을 일차함수 [[y = -3x + 12]]의 그래프가 지날 때, 상수 [[a]]의 값은?",
    choices=["[[-3]]", "[[-2]]", "[[-1]]", "[[1]]", "[[2]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="교점 (5, −3) → 5a+3=−2 → a=−1 → ③ = 빠른정답 ✓.")

# p33 삼각형이 생기지 않을 조건
add(id="fe23c240", qtype="short",
    question="세 직선 [[2x + y - 8 = 0]], [[3x - y + 3 = 0]], [[a x - y + 9 = 0]]으로 둘러싸인 삼각형이 만들어지지 않도록 하는 모든 [[a]]의 값의 합을 구하시오.",
    choices=None, derived_answer="-2", figure=None, difficulty_est=3, confidence=0.9,
    note="평행 a=−2, 3; 교점 (1, 6) 통과 a=−3 → 합 −2. 빠른정답 'neg 2'(=−2) 표기만 다름.")

# p37
add(id="3d2e9f20", qtype="short",
    question=("다음 세 일차방정식의 그래프가 삼각형을 이루지 않도록 하는 모든 [[a]]의 값의 합이 [[frac(q, p)]] 일 때, [[p + q]]의 값을 구하시오. "
              "(단, [[a != 0]]이고 [[p]], [[q]]는 서로소)\n[[x + y - 5 = 0]], [[2x - y - 1 = 0]], [[x + a y - 8 = 0]]"),
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.9,
    note="a=1, −1/2 (평행), a=2 (교점 (2,3) 통과) → 합 5/2 → p+q=7 = 빠른정답 ✓.")

# p50 한 점에서 만나는 세 직선
add(id="d92e5127", qtype="choice",
    question=("세 직선 [[x - 2y = -1]], [[3x + y = 11]], [[a x + (3a - 2) y = -13]]이 한 점에서 만날 때, 다음 중 직선 [[a x + (3a - 2) y = -13]] 위의 점은? "
              "(단, [[a]]는 상수이다.)"),
    choices=["[[point(-3, 2)]]", "[[point(-2, 3)]]", "[[point(-1, 4)]]", "[[point(0, 5)]]", "[[point(1, 6)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="교점 (3, 2) → a=−1 → 직선 x+5y=13 → (−2, 3) ✓ → ②. 빠른정답 3과 불일치.")

# p52 해의 개수
add(id="1bba9b82", qtype="choice",
    question="두 직선 [[a x + y = 5]], [[2x - y = b]]의 교점이 무수히 많을 때, [[a - b]]의 값은?",
    choices=["[[-3]]", "[[-2]]", "[[1]]", "[[3]]", "[[7]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a/2=1/(−1)=5/b → a=−2, b=−5 → a−b=3 → ④. 빠른정답 6과 불일치.")

# p56 (프라임 상수, 보기 ㄱㄴㄷ)
add(id="35d63ad8", qtype="short",
    question=("[[x]], [[y]] 에 대한 두 일차방정식 [[a x + b y + c = 0]], [[prime(a) x + prime(b) y + prime(c) = 0]]의 그래프가 한 점에서 만날 때, "
              "다음 보기 중 연립방정식 [[a x + b y + c = 0]], [[prime(a) x + prime(b) y + prime(c) = 0]]의 해로 알맞은 것을 고르시오.\n<보기>\n"
              "ㄱ. 해가 없다.\nㄴ. 한 쌍의 해를 갖는다.\nㄷ. 해가 무수히 많다."),
    choices=None, derived_answer="ㄴ", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 상수 a′, b′, c′의 프라임 표기를 prime()으로 우회",
    note="한 점에서 만남 → 해 한 쌍 → ㄴ. 빠른정답 없음.")

# p60
add(id="dc142f1e", qtype="choice",
    question="연립방정식 [[a x + 4y = 15]], [[2x - y = 7]]의 해가 존재하지 않을 때, [[a]]의 값은?",
    choices=["[[8]]", "[[4]]", "[[0]]", "[[-8]]", "[[-4]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a/2=4/(−1) → a=−8 → ④. 빠른정답 4와 불일치.")

# ================= 다항식의 곱셈과 나눗셈 =================
# p3 단항식×다항식
add(id="8866fb6f", qtype="choice",
    question="[[-3x(x - 2y - 1) = A pow(x,2) + B x y + C x]]일 때, 상수 [[A]], [[B]], [[C]]에 대하여 [[A + B + C]]의 값은?",
    choices=["[[-6]]", "[[-5]]", "[[0]]", "[[3]]", "[[6]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="−3x²+6xy+3x → A+B+C=6 → ⑤ = 빠른정답 ✓.")

# p5
add(id="7c737b92", qtype="choice",
    question="[[-2x(pow(x,2) + 3x - 1) = a pow(x,3) + b pow(x,2) + c x]]일 때, [[a + b + c]]의 값은? (단, [[a]], [[b]], [[c]]는 상수)",
    choices=["[[-6]]", "[[-3]]", "[[-1]]", "[[0]]", "[[1]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="−2x³−6x²+2x → −6 → ①. 빠른정답 5와 불일치.")

# p11 다항식÷단항식
add(id="6e73b465", qtype="choice",
    question="[[(6 pow(x,2) y - 4x pow(y,2)) / (-frac(2, 3) x y)]]를 간단히 하면?",
    choices=["[[9x + 6y]]", "[[9x + 6 pow(y,2)]]", "[[-9x + 6y]]", "[[-9 pow(x,3) pow(y,2) + 6 pow(x,2) pow(y,3)]]", "[[9 pow(x,3) pow(y,2) - 6 pow(x,2) pow(y,3)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="×(−3/(2xy)) → −9x+6y → ③. 빠른정답 2와 불일치.")

# p22 어떤 다항식
add(id="ea7c0b3e", qtype="choice",
    question="어떤 다항식을 [[2x]]로 나눈 결과가 [[-4x + 3y + frac(1, 2)]] 일 때, 어떤 다항식은? (단, [[x != 0]])",
    choices=["[[-2 pow(x,2) + frac(3, 2) x y]]", "[[-8 pow(x,2) + 6x y + x]]", "[[-frac(1, 2) pow(x,2) + frac(2, 3) x y]]",
             "[[-2 pow(x,2) + 6x y + x]]", "[[8 pow(x,2) + 6x y - 1]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="2x(−4x+3y+½)=−8x²+6xy+x → ②. 빠른정답 12와 불일치.")

# p26
add(id="8f373c1b", qtype="choice",
    question="어떤 다항식을 [[-3x y]]로 나누어야 하는데 잘못하여 곱했더니 [[9 pow(x,2) y - x y]]가 되었다. 이때 어떤 다항식은?",
    choices=["[[3x + frac(1, 3)]]", "[[-3x + frac(1, 3)]]", "[[3x - frac(1, 3)]]", "[[frac(1, 3) x + frac(1, 3)]]", "[[-frac(1, 3) x + frac(1, 3)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="(9x²y−xy)÷(−3xy)=−3x+1/3 → ② = 빠른정답 ✓.")

# p29 빈 칸
add(id="7366ae55", qtype="choice",
    question="□ ÷ [[3a b]] = [[2a pow(b,2) - 2b + 1]]일 때, □ 안에 알맞은 식은?",
    choices=["[[-a pow(b,2) - 4 pow(a,2) b + 3a b]]", "[[-3 pow(a,2) pow(b,3) + 4 pow(a,2) b + 6a b]]", "[[3 pow(a,3) pow(b,2) - 4a pow(b,2) + 6a pow(b,2)]]",
             "[[6 pow(a,2) pow(b,3) - 6a pow(b,2) + 3a b]]", "[[6 pow(a,2) pow(b,3) + 6a pow(b,2) + 3a b]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="3ab(2ab²−2b+1)=6a²b³−6ab²+3ab → ④. 빠른정답 2와 불일치. 빈칸 상자는 □ 텍스트.")

# p30
add(id="ce81e397", qtype="choice",
    question="□ ÷ [[4a b]] = [[3a pow(b,2) - 2b + 2]]일 때, □ 안에 알맞은 식은?",
    choices=["[[12 pow(a,2) pow(b,2) - 8a b - 8a b]]", "[[12 pow(a,2) pow(b,2) - 8 pow(a,2) b + 8a b]]", "[[12 pow(a,2) pow(b,3) - 8a pow(b,2) + 8a b]]",
             "[[12 pow(a,2) pow(b,3) - 8a pow(b,2) - 8a b]]", "[[12 pow(a,2) pow(b,3) + 8a pow(b,2) + 8a b]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="4ab(3ab²−2b+2)=12a²b³−8ab²+8ab → ③. 빠른정답 5와 불일치.")

# p33 (풀이 과정 상자, ⓐⓑⓒ 표 선지)
add(id="3fd8fb0c", qtype="choice",
    question=("다음은 □ 안에 알맞은 식을 구하는 과정이다. ⓐ~ⓒ에 알맞은 것으로 바르게 짝 지어진 것은?\n"
              "□ ÷ [[2x y]] = [[pow(x,2) y + 3x y - 5]]\n"
              "□ = ([[pow(x,2) y + 3x y - 5]]) × ⓐ\n"
              "= ⓑ + [[6 pow(x,2) pow(y,2)]] − ⓒ"),
    choices=["ⓐ [[x y]], ⓑ [[2 pow(x,2) pow(y,3)]], ⓒ [[10x y]]", "ⓐ [[x y]], ⓑ [[2 pow(x,3) pow(y,2)]], ⓒ [[10x y]]",
             "ⓐ [[2x y]], ⓑ [[pow(x,2) pow(y,3)]], ⓒ [[5x y]]", "ⓐ [[2x y]], ⓑ [[2 pow(x,3) pow(y,2)]], ⓒ [[5x y]]",
             "ⓐ [[2x y]], ⓑ [[2 pow(x,3) pow(y,2)]], ⓒ [[10x y]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="ⓐ 2xy, ⓑ 2x³y², ⓒ 10xy → ⑤. 빠른정답 3과 불일치. 선지의 ⓐⓑⓒ 표는 한 줄로 병기.")

# p34
add(id="eb833020", qtype="choice",
    question="다음 □ 안에 알맞은 식은?\n□ ÷ [[4 pow(a,2) b]] = [[3 pow(a,2) b - 2a b + 5]]",
    choices=["[[3 pow(a,4) pow(b,2) - 2 pow(a,3) pow(b,2) + 5 pow(a,2) b]]", "[[12 pow(a,4) pow(b,2) - 8 pow(a,3) pow(b,2) + 20 pow(a,2) b]]",
             "[[12 pow(a,4) pow(b,2) + 8 pow(a,3) pow(b,2) - 20 pow(a,2) b]]", "[[12 pow(a,2) pow(b,2) + 8 pow(a,2) b + 10 pow(a,2) b]]",
             "[[24 pow(a,4) pow(b,2) - 16 pow(a,3) pow(b,2) + 40 pow(a,2) b]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="4a²b(3a²b−2ab+5)=12a⁴b²−8a³b²+20a²b → ②. 빠른정답 1과 불일치.")

# p35
add(id="45a7b817", qtype="choice",
    question="[[(2a pow(b,2) + 4 pow(a,2) pow(b,3) - 3a b)]] ÷ □ = [[frac(1, 3) a b]]일 때, □ 안에 알맞은 식을 구하면?",
    choices=["[[4a + 12a pow(b,2) - 9]]", "[[6b + 6a pow(b,2) - 9]]", "[[6b + 12a pow(b,2) - 9]]", "[[4b + 6a pow(b,2) - 3]]", "[[6b + 8a pow(b,2) + 9]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="(2ab²+4a²b³−3ab)÷(ab/3)=6b+12ab²−9 → ③. 빠른정답 5와 불일치.")

# p36
add(id="b6ccbc47", qtype="choice",
    question=("다항식 [[A]]를 [[pow(a,2) b]]로 나누었더니 [[5a b + 2]]가 되었다. [[(A + 3 pow(a,3) pow(b,2))]] ÷ □ = [[2 pow(a,2) b]]일 때, "
              "□ 안에 알맞은 식은?"),
    choices=["[[4a b + 1]]", "[[8a b + 2]]", "[[2 pow(a,2) b + 1]]", "[[2a b + 4 pow(a,2) b]]", "[[4a b + 2 pow(a,2) b]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="A=5a³b²+2a²b → (8a³b²+2a²b)÷(2a²b)=4ab+1 → ①. 빠른정답 5와 불일치.")
