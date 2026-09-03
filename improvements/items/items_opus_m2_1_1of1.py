# -*- coding: utf-8 -*-
# esc_opus_m2-1_1of1 — 이미지 기준 전사 (4 항목 / 4쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ---------------- 함수와 함숫값 p15
add(id="527ccccf", qtype="short",
    question=("두 변수 [[x]], [[y]]에 대하여 2, 3, 4인 [[x]]가 1, 2, 3, 4, 5, 6, 7인 [[y]] 중의 어느 하나에 반드시 대응하는 함수를 "
              "[[y = f(x)]]라 할 때, [[x]]의 모든 수 [[a]]에 대하여 [[a + f(a)]]가 짝수가 되는 함수의 개수를 구하시오."),
    choices=None, derived_answer="36", figure=None, difficulty_est=2, confidence=0.85,
    note="f(a)와 a의 홀짝이 같아야 함: f(2)∈{2,4,6}, f(3)∈{1,3,5,7}, f(4)∈{2,4,6} → 3×4×3=36. 빠른정답 3과 불일치.")

# ---------------- 유리수의 소수 표현 p26 (피보나치 정사각형 도형)
add(id="2a6f85e9", qtype="short",
    question=("다음 그림과 같이 한 변의 길이가 1인 색칠된 정사각형을 기준으로 정사각형 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], [[sub(A,4)]], [[sub(A,5)]], ⋯를 "
              "규칙적으로 차례대로 붙여 나갈 때, 정사각형 [[sub(A,n)]]의 한 변의 길이를 [[sub(a,n)]]이라 하자. "
              "[[frac(sub(a,n+1), sub(a,n))]]을 정수나 유한소수로 나타낼 수 없도록 하는 15 이하의 자연수 [[n]]의 값의 합을 구하시오."),
    choices=None, derived_answer="108",
    figure=[{"fn": "unsupported", "args": {"raw": "좌상단에 한 변 1인 색칠된 정사각형(가로·세로 1 치수 표시). 그 오른쪽에 A₁(한 변 1), 아래에 A₂(한 변 2), 오른쪽에 A₃(한 변 3), 아래에 A₄(한 변 5), 오른쪽에 A₅(한 변 8)를 나선형으로 붙여 큰 직사각형을 이룸. 오른쪽·아래에 ⋯ 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 피보나치 정사각형 나선 배치 도형(규칙이 그림에 있음)",
    note="aₙ=1,2,3,5,8,13,…(피보나치, 이웃항 서로소). aₙ이 2·5 외 소인수를 가지는 n=3,6,7,…,15 → 합 108 = 빠른정답 ✓.")

# ---------------- 여러 가지 연립방정식의 풀이 p62 (비례식)
add(id="cbd4323b", qtype="short",
    question=("비례식\n[[ratio((3x + y + a), (-x + 2y - b), (4x + 2y)) = ratio(4, 3, 5)]]에 대하여 [[x = 6 - a]], [[y = b + 11]]일 때, "
              "두 상수 [[a]], [[b]]에 대하여 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="-21", figure=None, difficulty_est=3, confidence=0.85,
    note="대입 후 29−2a+b=4k, 16+a+b=3k, 46−4a+2b=5k → k=4, a=3, b=−7 → ab=−21 (x=3, y=4에서 16:12:20 확인). 빠른정답 3과 불일치(a의 값).")

# ---------------- 순환소수의 분수 표현 p69 (문자 순환마디)
add(id="ac9cb337", qtype="short",
    question=("순환마디가 [[n]]인 순환소수 0.ȧ₁a₂a₃ ⋯ ȧₙ에 대하여 순환마디의 첫 번째 숫자를 순환마디의 마지막 자리로 옮겨 만든 순환소수 "
              "0.ȧ₂a₃a₄ ⋯ aₙȧ₁이 처음 수의 [[frac(13,3)]]배가 된다고 한다. 처음 수를 [[frac(q, p)]]라 할 때, [[p + q]]의 값을 구하시오. "
              "(단, [[1 <= i <= n]]에 대하여 [[sub(a,i)]]는 [[0 <= sub(a,i) <= 9]]인 정수, [[p]], [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="20", figure=None, difficulty_est=4, confidence=0.75,
    needs_review="문법 범위 밖: 문자 순환마디 표기 0.ȧ₁a₂a₃⋯ȧₙ(순환점)을 유니코드 텍스트로 전사",
    note="x=처음 수, 10x−a₁=(13/3)x → x=3a₁/17; 첫 자리 조건에서 a₁=1 → 3/17 → p+q=20 = 빠른정답 ✓.")
