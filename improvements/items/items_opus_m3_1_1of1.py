# -*- coding: utf-8 -*-
# esc_opus_m3-1_1of1 — 이미지 기준 전사 (6 항목 / 6쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ---------------- 곱셈 공식을 이용한 수의 계산 p99 (이미지에 문항 2개: 위쪽 ⟨x⟩ 문항을 전사)
add(id="1c88b31d", qtype="short",
    question=("기호 ⟨[[x]]⟩를 [[x]]에 가장 가까운 정수라 할 때,\n"
              "⟨[[frac(sqrt(5), sqrt(5) + 1)]]⟩ + ⟨[[frac(sqrt(5), sqrt(5) - 1)]]⟩의 값을 구하시오.\n"
              "(단, [[sqrt(5)]]의 값은 2.236으로 계산한다.)"),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.75,
    needs_review="문법 범위 밖: 기호 ⟨x⟩(가장 가까운 정수)는 텍스트 혼합 / 이미지에 문항 2개 포함 — 아래쪽 문항 '(√10+√6)/(√10−√6)=a+b√15일 때 유리수 a, b에 대하여 a+b의 값'(답 5)은 미전사, 대상 문항 확인 필요",
    note="√5/(√5+1)=(5−√5)/4≈0.691→1, √5/(√5−1)=(5+√5)/4≈1.809→2 → 3. 아래쪽 문항은 4+√15 → a+b=5. 빠른정답 9는 둘 다와 불일치.")

# ---------------- 인수분해 공식의 활용 p58
add(id="cd927c2d", qtype="short",
    question=("[[x]], [[y]]는 실수이고 [[pow(x,2) + pow(y,2) = 1]]일 때,\n"
              "[[sqrt(pow(1 + frac(x y, 2), 2)) + sqrt(pow(1 - frac(x y, 2), 2))]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.85,
    note="x²+y²=1 ⇒ |xy|≤1/2 ⇒ 1±xy/2>0 → 합 2. 빠른정답 38과 불일치.")

# ---------------- 곱셈 공식 p26 (연속한 합과 차의 곱)
add(id="5ba8f6d6", qtype="short",
    question=("세 자연수 [[a]], [[b]], [[c]]에 대하여\n"
              "[[(1 + frac(1, x)) × (1 + frac(1, pow(x,2))) × (1 + frac(1, pow(x,4))) × (1 + frac(1, pow(x,8))) × (1 + frac(1, pow(x,16))) × (1 + frac(1, pow(x,32))) "
              "= frac(pow(x,a) - 1, pow(x,b) - pow(x,c))]]\n"
              "일 때, [[a + b - c]]의 값을 구하시오."),
    choices=None, derived_answer="65", figure=None, difficulty_est=3,
    note="t=1/x: 곱=(1−t⁶⁴)/(1−t)=(x⁶⁴−1)/(x⁶⁴−x⁶³) → a=64, b=64, c=63 → 65 = 빠른정답 ✓.")

# ---------------- 곱셈 공식의 변형 p27
add(id="a0f1ddd9", qtype="short",
    question=("[[x + y = 5]], [[x y = 6]]일 때,\n[[(x + 3)(y + 3)(x - 3)(y - 3)]]의 값을 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=2,
    note="(x²−9)(y²−9)=x²y²−9(x²+y²)+81=36−9·13+81=0 = 빠른정답 ✓.")

# ---------------- 곱셈 공식의 변형 p28
add(id="e924ff82", qtype="short",
    question=("[[x + y = 3]], [[x y = 2]]일 때,\n[[(x + 5)(y + 5)(x - 5)(y - 5)]]의 값을 구하시오."),
    choices=None, derived_answer="504", figure=None, difficulty_est=2, confidence=0.85,
    note="(x²−25)(y²−25)=x²y²−25(x²+y²)+625=4−25·5+625=504 (x,y=1,2 대입 6·7·(−4)·(−3)=504). 빠른정답 35와 불일치.")

# ---------------- 이차함수 y=ax²의 그래프 p81
add(id="b0f64ce5", qtype="short",
    question=("이차함수 [[y = 2 pow(x,2)]]의 그래프 위의 두 점 [[A(3, 18)]], [[B(a, b)]]와 [[y]]축에 대하여 대칭인 점을 각각 C, D라 하고 "
              "원점을 O라 한다. [[tri(ABC)]]와 [[tri(BOD)]]의 넓이의 비가 [[ratio(24, pow(a,2))]]일 때, [[a]]의 값을 구하시오. (단, [[0 < a < 3]])"),
    choices=None, derived_answer="1", figure=None, difficulty_est=3,
    note="△ABC=3(18−2a²)=54−6a², △BOD=½·2a·2a²=2a³; (54−6a²):2a³=24:a² → a²+8a−9=0 → a=1 = 빠른정답 ✓.")
