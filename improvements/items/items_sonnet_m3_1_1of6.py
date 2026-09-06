# -*- coding: utf-8 -*-
# esc_sonnet_m3-1_1of6 — 이미지 기준 전사 (85 항목 / 80쪽)
# 단원 m3-1: 복잡한 이차방정식의 풀이 / 이차방정식의 근의 공식 / 복잡한 식의 인수분해 / 곱셈 공식을 이용한 수의 계산 / 이차방정식의 중근 / 완전제곱식
# 규약: 빈칸 상자(ⓐ~ⓒ, (가)~(마), ㉠~㉤, □)와 약속 기호(∘, ⟨ ⟩, [ ], { }, < >)는 마커 밖 텍스트. 화살표 ⇨/→는 텍스트.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

C5 = lambda *v: [f"[[{x}]]" for x in v]
NOTE_GCD = "문법 범위 밖: 약속 기호 ⟨a, b⟩(최대공약수)·[a, b](최소공배수) 텍스트 혼합(방정식이 조각남)"

# ============================ 복잡한 이차방정식의 풀이 ============================
# p1
add(id="524f8a37", qtype="choice",
    question=("다음은 이차방정식의 해를 구하는 과정이다. ⓐ, ⓑ, ⓒ에 알맞은 것끼리 바르게 짝 지어진 것은?\n"
              "[[(x + 1)(x - 4) = -1]]에서\n"
              "식을 정리하면 [[pow(x,2)]] − ⓐ[[x]] − ⓑ = 0\n"
              "근의 공식을 이용하면\n"
              "[[x]] = ⓒ"),
    choices=["ⓐ: 4, ⓑ: 4, ⓒ: [[pm(1, 2 sqrt(2))]]",
             "ⓐ: 4, ⓑ: 3, ⓒ: [[pm(1, sqrt(7))]]",
             "ⓐ: 3, ⓑ: 3, ⓒ: [[frac(pm(-3, sqrt(21)), 2)]]",
             "ⓐ: 3, ⓑ: 4, ⓒ: [[-1]] 또는 [[4]]",
             "ⓐ: 3, ⓑ: 3, ⓒ: [[frac(pm(3, sqrt(21)), 2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="x²−3x−3=0 → x=(3±√21)/2 → ⑤ = 빠른정답 ✓. 선지 표(ⓐ ⓑ ⓒ 열)를 'ⓐ: , ⓑ: , ⓒ: ' 꼴로 적음.")

# p12
add(id="0f80c3ff", qtype="short",
    question=("다음 이차방정식의 두 근을 [[a]], [[b]]라고 할 때, [[2a - b]]의 값을 구하시오. (단, [[a > b]])\n"
              "[[3x(x + 1) = (x + 1)(x - 3) + 6]]"),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="2x²+5x−3=0 → x=1/2, −3 → 2·(1/2)−(−3)=4 = 빠른정답 ✓.")

# p14
add(id="527414c1", qtype="short",
    question=("이차방정식 [[(x - 1)(x + 5) = -2x - 1]]의 해가 [[pm(A, sqrt(B))]]일 때, [[A + B]]의 값을 구하시오.\n"
              "(단, [[A]], [[B]]는 유리수)"),
    choices=None, derived_answer="10", figure=None, difficulty_est=2, confidence=0.9,
    note="x²+6x−4=0 → x=−3±√13 → A+B=10. 빠른정답 1과 불일치(정렬 어긋남으로 보임).")

# p25
add(id="0f04e429", qtype="choice",
    question=("이차방정식 [[frac(x(x + 2), 3) = frac(x(x - 1), 5) - a]]의 근이 [[x = frac(pm(b, sqrt(109)), 4)]]일 때, "
              "유리수 [[a]], [[b]]에 대하여 [[2a - b]]의 값은?"),
    choices=C5(11, 12, 13, 14, 15), derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="2x²+13x+15a=0 → b=−13, 169−120a=109 → a=1/2 → 2a−b=14 → ④. 빠른정답 2와 불일치.")

# p26
add(id="1ff4da9c", qtype="choice",
    question=("이차방정식 [[frac((x + 1)(x + 4), 3) = frac(x(x + 3), 2)]]의 해가 [[x = frac(pm(p, sqrt(q)), 2)]]일 때, "
              "유리수 [[p]], [[q]]에 대하여 [[p + q]]의 값은?"),
    choices=C5(30, 32, 34, 36, 38), derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="x²−x−8=0 → x=(1±√33)/2 → p+q=34 → ③. 빠른정답 1과 불일치.")

# p32
add(id="2299d155", qtype="choice",
    question=("이차방정식 [[frac((x - 2)(x + 2), 4) = frac(x(x + 5), 6) + a]]의 근이 [[x = pm(b, sqrt(33))]]일 때, "
              "유리수 [[a]], [[b]]에 대하여 [[3a + b]]의 값은?"),
    choices=C5(3, 4, 5, 6, 7), derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="x²−10x−12−12a=0 → x=5±√(37+12a) → a=−1/3, b=5 → 3a+b=4 → ② = 빠른정답 ✓.")

# p36
add(id="8e279e4e", qtype="choice",
    question=("이차방정식 [[frac((x + 2)(x - 3), 5) = frac(x(x + 4), 4)]]의 두 근 중 큰 근을 [[a]]라 할 때, "
              "부등식 [[n < a < n + 1]]을 만족시키는 정수 [[n]]의 값은?"),
    choices=C5(-2, -1, 0, 1, 2), derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="x²+24x+24=0 → a=−12+2√30≈−1.05 → n=−2 → ① = 빠른정답 ✓.")

# p43 (한 이미지에 문항 1개, id 3개 → 동일 전사)
dup(["b7aa2945", "20a11e87", "c4196398"], qtype="choice",
    question="다음 중 이차방정식의 해가 옳지 않은 것은?",
    choices=["[[x(x + 3) = 5x - 1]] ⇨ [[x = 1]] (중근)",
             "[[0.1(x + 2)(x - 5) = 0.2x - frac(2,5)]] ⇨ [[x = 1]] 또는 [[x = 6]]",
             "[[pow(x - 2, 2) = 2 pow(x,2) - x + 6]] ⇨ [[x = -1]] 또는 [[x = -2]]",
             "[[(x - 2)(x - 3) = 2 pow(x,2)]] ⇨ [[x = 1]] 또는 [[x = -6]]",
             "[[pow(2x + 3, 2) = 3 pow(x,2) + 4x - 6]] ⇨ [[x = -5]] 또는 [[x = -3]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="②는 x²−5x−6=0 → x=−1 또는 6이므로 틀림 → ② = 빠른정답 ✓. 같은 이미지에 id 3개(draft_a가 선지를 쪼갰던 것) → 동일 내용으로 전부 넣음.")

# p46
add(id="75de0291", qtype="choice",
    question=("이차방정식 [[frac(1,4) pow(x,2) - 0.3x = frac(x,5) + 0.5]]의 해가 [[x = pm(A, sqrt(B))]]일 때, "
              "[[A + B]]의 값은?"),
    choices=C5(3, 4, 5, 6, 7), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="×20: 5x²−10x−10=0 → x=1±√3 → A+B=4 → ② = 빠른정답 ✓.")

# p47
add(id="13a9875c", qtype="short",
    question=("이차방정식 [[0.3 pow(x,2) - frac(3,5) x + frac(1,10) = 0]]의 해가 [[frac(pm(3, sqrt(a)), b)]]일 때, "
              "유리수 [[a]], [[b]]에 대하여 [[a - b]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="3x²−6x+1=0 → x=(3±√6)/3 → a−b=6−3=3 = 빠른정답 ✓.")

# p52
add(id="cd9e8083", qtype="choice",
    question="다음 중 이차방정식과 그 해가 바르게 짝 지어지지 않은 것은?",
    choices=["[[3 pow(x,2) - x + 2 = 4]] → [[x = -frac(2,3)]] 또는 [[x = 1]]",
             "[[(x + 1)(x - 5) = 3(x - 2)]] → [[x = frac(pm(7, 3 sqrt(5)), 2)]]",
             "[[frac(1,2) pow(x,2) - frac(5,12) x + frac(1,12) = 0]] → [[x = frac(1,3)]] 또는 [[x = frac(1,2)]]",
             "[[0.2 pow(x,2) - 0.05x - 0.15 = 0]] → [[x = -1]] 또는 [[x = frac(3,4)]]",
             "[[0.2 pow(x,2) = frac(3,5) x - 0.3]] → [[x = frac(pm(3, sqrt(3)), 2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="④는 4x²−x−3=0 → x=1 또는 −3/4이므로 틀림 → ④ = 빠른정답 ✓.")

# p53
add(id="a330cdd6", qtype="short",
    question=("이차방정식 [[frac(1,4) pow(x,2) - 0.3x + A = 0]]의 근이 [[x = frac(pm(B, sqrt(11)), 10)]]일 때, "
              "유리수 [[A]], [[B]]에 대하여 [[8 A B]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="×20: 5x²−6x+20A=0 → x=(6±√(36−400A))/10 → B=6, A=1/16 → 8AB=3 = 빠른정답 ✓.")

# p55
add(id="0111df4c", qtype="choice",
    question="이차방정식 [[0.3 pow(x,2) - x = 0.1]]을 풀면?",
    choices=["[[x]] = ±[[frac(2,3)]]",
             "[[x = frac(pm(2, sqrt(3)), 3)]]",
             "[[x = frac(pm(5, 2 sqrt(7)), 3)]]",
             "[[x = frac(pm(5, 3 sqrt(7)), 3)]]",
             "[[x = frac(pm(7, 2 sqrt(7)), 3)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="3x²−10x−1=0 → x=(10±√112)/6=(5±2√7)/3 → ③. 빠른정답 4와 불일치.")

# p56
add(id="9296c334", qtype="choice",
    question="이차방정식 [[0.3 pow(x,2) - 0.4x = 0.6]]을 풀면?",
    choices=["[[x = frac(pm(2, sqrt(11)), 3)]]",
             "[[x = frac(pm(1, sqrt(22)), 3)]]",
             "[[x = frac(pm(2, sqrt(22)), 2)]]",
             "[[x = frac(pm(2, sqrt(22)), 3)]]",
             "[[x = frac(pm(2, sqrt(23)), 3)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="3x²−4x−6=0 → x=(4±√88)/6=(2±√22)/3 → ④. 빠른정답 3과 불일치.")

# p66
add(id="28d65375", qtype="choice",
    question=("두 실수 [[x]], [[y]]에 대하여\n[[pow(x + y, 2) + 4(x + y) - 12 = 0]]이고 [[x y = 4]]일 때,\n"
              "[[pow(x,2) + pow(y,2)]]의 값은?"),
    choices=C5(22, 24, 26, 28, 30), derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="x+y=−6 또는 2; x+y=2는 실근 불가 → x²+y²=36−8=28 → ④ = 빠른정답 ✓.")

# p82
add(id="679e2900", qtype="choice",
    question=("실수 [[a]], [[b]]에 대하여 [[a]] ∘ [[b]] = [[a b + a + b]]일 때,\n"
              "([[x - 1]]) ∘ ([[x + 4]]) = [[5]]를 만족하는 모든 [[x]]의 값의 곱은?"),
    choices=C5(-6, -4, -2, 2, 4), derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="x²+5x−1=5 → x²+5x−6=0 → 곱 −6 → ①. 빠른정답 5와 불일치. 연산 기호 ∘는 텍스트.")

# p84
add(id="9ab89736", qtype="short",
    question=("실수 [[a]], [[b]]에 대하여 연산 ∘를 [[a]] ∘ [[b]] = [[a b - a - 2b - 3]]이라 할 때, "
              "([[x - 2]]) ∘ ([[x + 3]]) = [[-3]]을 만족하는 모든 [[x]]의 값의 곱을 구하시오."),
    choices=None, derived_answer="-10", figure=None, difficulty_est=2, confidence=0.9,
    note="x²−2x−13=−3 → x²−2x−10=0 → 곱 −10. 빠른정답 2와 불일치. 연산 기호 ∘는 텍스트.")

# p88
add(id="2ff38624", qtype="short",
    question=("두 자연수 [[a]], [[b]]의 최대공약수를 ⟨[[a]], [[b]]⟩라 하고 최소공배수를 [ [[a]], [[b]] ]라 하자. "
              "[[x]]에 대한 이차방정식 ⟨[[a]], [[b]]⟩[[pow(x,2)]] − [ [[a]], [[b]] ][[x]] + 10 = 0의 두 근이 1, 5일 때, "
              "[[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)"),
    choices=None, derived_answer="10", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=NOTE_GCD,
    note="근 1, 5 → 최대공약수 2, 최소공배수 12 → (a, b)=(4, 6) → a+b=10. 빠른정답 38과 불일치.")

# p89
add(id="9c48e8fd", qtype="short",
    question=("두 자연수 [[a]], [[b]]의 최대공약수를 ⟨[[a]], [[b]]⟩라 하고 최소공배수를 [ [[a]], [[b]] ]라 하자. "
              "[[x]]에 대한 이차방정식 ⟨[[a]], [[b]]⟩[[pow(x,2)]] − [ [[a]], [[b]] ][[x]] + 24 = 0의 두 근이 2, 4일 때, "
              "[[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)"),
    choices=None, derived_answer="15", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=NOTE_GCD,
    note="근 2, 4 → 최대공약수 3, 최소공배수 18 → (a, b)=(6, 9) → a+b=15. 빠른정답 2와 불일치.")

# p90
add(id="d705aba8", qtype="short",
    question=("두 자연수 [[a]], [[b]]의 최대공약수를 ⟨[[a]], [[b]]⟩라 하고 최소공배수를 [ [[a]], [[b]] ]라 하자. "
              "[[x]]에 대한 이차방정식 ⟨[[a]], [[b]]⟩[[pow(x,2)]] − [ [[a]], [[b]] ][[x]] + 54 = 0의 두 근이 3, 9일 때, "
              "[[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)"),
    choices=None, derived_answer="14", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=NOTE_GCD,
    note="근 3, 9 → 최대공약수 2, 최소공배수 24 → (a, b)=(6, 8) → a+b=14. 빠른정답 4와 불일치.")

# p93
add(id="e2eccd2a", qtype="short",
    question=("⟨[[x]]⟩를 자연수 [[x]]보다 작은 소수의 개수라 할 때, 방정식 4⟨[[x]]⟩² − 29⟨[[x]]⟩ − 24 = 0을 만족시키는 "
              "모든 자연수 [[x]]의 값의 합을 구하시오."),
    choices=None, derived_answer="86", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 ⟨x⟩(x보다 작은 소수의 개수) 텍스트 혼합(방정식이 조각남)",
    note="(4t+3)(t−8)=0 → ⟨x⟩=8 → x=20, 21, 22, 23 → 합 86. 빠른정답 14와 불일치.")

# p94
add(id="9834d721", qtype="choice",
    question=("자연수 [[x]]에 대하여 <[[x]]>는 [[x]] 이하의 소수의 개수라 할 때, 다음 중 <[[x]]>² − 2<[[x]]> − 24 = 0을 "
              "만족시키는 자연수 [[x]]가 될 수 없는 것은?"),
    choices=C5(13, 14, 15, 16, 17), derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 <x>(x 이하의 소수의 개수) 텍스트 혼합(방정식이 조각남)",
    note="(t−6)(t+4)=0 → <x>=6 → x=13~16; <17>=7 → ⑤. 빠른정답 38과 불일치.")

# p96
add(id="e62ac95b", qtype="choice",
    question=("자연수 [[x]]에 대하여 <[[x]]>는 [[x]] 이하의 소수의 개수라 할 때, 다음 중 <[[x]]>² + <[[x]]> − 20 = 0을 "
              "만족시키는 자연수 [[x]]가 될 수 없는 것은?"),
    choices=C5(6, 7, 8, 9, 10), derived_answer="①", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 <x>(x 이하의 소수의 개수) 텍스트 혼합(방정식이 조각남)",
    note="(t+5)(t−4)=0 → <x>=4 → x=7~10; <6>=3 → ①. 빠른정답 86과 불일치.")

# p98
add(id="b64f5373", qtype="choice",
    question=("자연수 [[x]]의 약수의 개수를 ⟨[[x]]⟩로 나타낼 때,\n등식 ⟨[[x]]⟩² + 2⟨[[x]]⟩ − 8 = 0을 만족시키는 20 이하의 "
              "자연수 [[x]]의 개수는?"),
    choices=C5(4, 5, 6, 7, 8), derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 ⟨x⟩(약수의 개수) 텍스트 혼합(방정식이 조각남)",
    note="(t+4)(t−2)=0 → ⟨x⟩=2 → 20 이하 소수 8개 → ⑤. 빠른정답 2와 불일치.")

# p99 (한 이미지에 별개 문항 2개, id 2개 → draft_a 대응대로 분리)
add(id="150ffcdb", qtype="short",
    question=("자연수 [[x]]의 약수의 개수를 {[[x]]}로 나타낼 때,\n등식 {[[x]]}² − 26{[[x]]} − 27 = 0을 만족시키는 가장 작은 "
              "자연수 [[x]]의 값을 구하시오."),
    choices=None, derived_answer="900", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 {x}(약수의 개수) 텍스트 혼합(방정식이 조각남)",
    note="이미지 하단 문항(같은 쪽 상단은 edd27c48). (t−27)(t+1)=0 → 약수 27개인 최소 자연수 2²·3²·5²=900. 빠른정답 1과 불일치.")
add(id="edd27c48", qtype="short",
    question=("자연수 [[x]]의 약수의 개수를 {[[x]]}로 나타낼 때,\n등식 {[[x]]}² − 3{[[x]]} − 18 = 0을 만족시키는 가장 작은 "
              "자연수 [[x]]의 값을 구하시오."),
    choices=None, derived_answer="12", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 {x}(약수의 개수) 텍스트 혼합(방정식이 조각남)",
    note="이미지 상단 문항(같은 쪽 하단은 150ffcdb). (t−6)(t+3)=0 → 약수 6개인 최소 자연수 12. 빠른정답 1과 불일치.")

# ============================ 이차방정식의 근의 공식 ============================
# p2
add(id="f6e2f288", qtype="choice",
    question=("이차방정식 [[-pow(x,2) + 5x = 2 pow(x,2) + 3x - 4]]의 근이 [[x = frac(pm(A, sqrt(B)), 3)]]일 때, "
              "유리수 [[A]], [[B]]에 대하여 [[A + B]]의 값은?"),
    choices=C5(12, 13, 14, 15, 16), derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="3x²−2x−4=0 → x=(1±√13)/3 → A+B=14 → ③ = 빠른정답 ✓.")

# p3
add(id="336a3653", qtype="short",
    question=("이차방정식 [[3 pow(x,2) - 12x + 1 = 0]]을 풀면 [[x = frac(pm(b, sqrt(c)), a)]]이다. "
              "자연수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값 중 가장 작은 수를 구하시오."),
    choices=None, derived_answer="42", figure=None, difficulty_est=2, confidence=0.9,
    note="x=(6±√33)/3 → 3+6+33=42 = 빠른정답 ✓.")

# p6 (한 이미지에 문항 1개, id 2개 → 동일 전사)
dup(["dec0bd7b", "c0b47097"], qtype="choice",
    question=("다음은 근의 공식을 이용하여 이차방정식 [[2 pow(x,2) + 3x - 1 = 0]]의 해를 구하는 과정이다. "
              "(가)～(마)에 들어갈 값이 바르게 짝지어진 것은?\n"
              "근의 공식에 [[a = 2]], [[b]] = (가), [[c = -1]]을 대입하면\n"
              "[[x]] = ( −(나) ± √( (다)² − 4 × (라) ) ) / ( 2 × (마) )\n"
              "= [[frac(pm(-3, sqrt(17)), 4)]]"),
    choices=["(가) : 3", "(나) : [[-6]]", "(다) : 9", "(라) : 2", "(마) : 4"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="(가)=3, (나)=3, (다)=3, (마)=2 → ①. 빠른정답 42와 불일치(정렬 어긋남). 근호 안 '4×(라) )'의 닫는 괄호는 인쇄 그대로; 빈칸 식은 텍스트 조각. 같은 이미지에 id 2개.")

# p8
add(id="99237f26", qtype="choice",
    question=("다음은 일차항의 계수가 짝수인 이차방정식 [[pow(x,2) + 4x - 7 = 0]]의 해를 구하는 과정이다. "
              "㉠～㉤에 들어갈 값이 바르게 짝지어진 것은?\n"
              "짝수 공식에 [[a = 1]], [[prime(b)]] = ㉠, [[c = -7]]을 대입하면\n"
              "[[x]] = ( −㉡ ± √( ㉢² − 1 × (㉣) ) ) / ㉤\n"
              "= [[pm(-2, sqrt(11))]]"),
    choices=["㉠ : 2", "㉡ : 4", "㉢ : 16", "㉣ : [[-28]]", "㉤ : 2"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="b′=2: ㉠=㉡=㉢=2, ㉣=−7, ㉤=1 → ①. 빠른정답 3과 불일치. b′는 prime(b), 빈칸 식은 텍스트 조각.")

# p9 (한 이미지에 문항 1개, id 2개 → 동일 전사)
dup(["9edba4ca", "70f0a118"], qtype="choice",
    question=("다음은 일차항의 계수가 짝수인 이차방정식 [[3 pow(x,2) - 10x + 5 = 0]]의 해를 구하는 과정이다. "
              "㉠～㉤에 들어갈 값이 바르게 짝지어진 것은?\n"
              "짝수 공식에 [[a = 3]], [[prime(b)]] = ㉠, [[c = 5]]를 대입하면\n"
              "[[x]] = ( −(㉡) ± √( (㉢)² − 3 × ㉣ ) ) / ㉤\n"
              "= [[frac(pm(5, sqrt(10)), 3)]]"),
    choices=["㉠ : 5", "㉡ : 10", "㉢ : [[-5]]", "㉣ : 3", "㉤ : 6"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="b′=−5: ㉠=㉡=㉢=−5, ㉣=5, ㉤=3 → ③. 빠른정답 1과 불일치. 같은 이미지에 id 2개.")

# p12
add(id="2fb09950", qtype="short",
    question="이차방정식 [[2 pow(x,2) - 4x - 3 = 0]]의 근이 [[x = frac(pm(A, sqrt(B)), 2)]]일 때, [[A + B]]의 값을 구하여라.",
    choices=None, derived_answer="12", figure=None, difficulty_est=2, confidence=0.9,
    note="x=(2±√10)/2 → 12 = 빠른정답 ✓.")

# p14
add(id="81d29fdb", qtype="choice",
    question="다음은 이차방정식의 해를 구한 것이다. 옳지 않은 것은?",
    choices=["[[2 pow(x,2) - 4x + 1 = 0]], [[x = frac(pm(2, sqrt(2)), 2)]]",
             "[[2 pow(x,2) - 6x - 5 = 0]], [[x = frac(pm(3, sqrt(19)), 2)]]",
             "[[pow(x,2) - 2x - 2 = 0]], [[x = pm(1, sqrt(3))]]",
             "[[pow(x,2) + 2x - 11 = 0]], [[x = frac(pm(-1, sqrt(15)), 2)]]",
             "[[2 pow(x,2) - 5x + 1 = 0]], [[x = frac(pm(5, sqrt(17)), 4)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="④는 x=−1±2√3이므로 틀림 → ④. 빠른정답 1과 불일치.")

# p16
add(id="c6d955e8", qtype="choice",
    question="이차방정식 [[pow(x,2) + 2x - 1 = 0]]의 근이 [[x = pm(-1, sqrt(A))]]일 때, [[A]]의 값은?",
    choices=C5(1, 2, 3, 5, 6), derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="x=−1±√2 → A=2 → ②. 빠른정답 7과 불일치.")

# p18
add(id="265981fc", qtype="short",
    question=("이차방정식 [[2 pow(x,2) - 8x + 1 = 0]]을 풀면 [[x = frac(pm(b, sqrt(c)), a)]]이다. "
              "자연수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값 중 가장 작은 수를 구하시오."),
    choices=None, derived_answer="20", figure=None, difficulty_est=2, confidence=0.9,
    note="x=(4±√14)/2 → 2+4+14=20. 빠른정답 1과 불일치.")

# p36
add(id="b3ab102d", qtype="choice",
    question=("이차방정식 [[2 pow(x,2) - 3x + A = 0]]의 근이 [[x = frac(pm(B, sqrt(17)), 4)]]일 때, [[A + B]]의 값은?\n"
              "(단, [[A]], [[B]]는 유리수)"),
    choices=C5(-4, -2, 2, 4, 6), derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="9−8A=17 → A=−1, B=3 → 2 → ③. 빠른정답 4와 불일치.")

# p37
add(id="791fdf80", qtype="choice",
    question=("이차방정식 [[3 pow(x,2) - 12x + A = 0]]의 근이 [[x = pm(B, frac(2 sqrt(6), 3))]]일 때, "
              "유리수 [[A]], [[B]]에 대하여 [[A - B]]의 값은?"),
    choices=C5(-6, -4, -2, 2, 4), derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="x=2±√(144−12A)/6, 2√6/3=√96/6 → A=4, B=2 → A−B=2 → ④ = 빠른정답 ✓.")

# p40
add(id="1f38ab46", qtype="choice",
    question=("이차방정식 [[pow(x,2) - 2 a x + b = 0]]의 근이 [[x = pm(-5, 2 sqrt(10))]]일 때, "
              "유리수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?"),
    choices=C5(-20, -18, -15, -12, -10), derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="x=a±√(a²−b) → a=−5, 25−b=40 → b=−15 → a+b=−20 → ①. 빠른정답 4와 불일치.")

# p41
add(id="d167de58", qtype="choice",
    question=("이차방정식 [[2 pow(x,2) - 8x + A = 0]]의 근이 [[x = pm(B, frac(sqrt(10), 2))]]일 때, "
              "유리수 [[A]], [[B]]에 대하여 [[A - B]]의 값은?"),
    choices=C5(1, 2, 3, 4, 5), derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="x=2±√(64−8A)/4, √10/2=√40/4 → A=3, B=2 → 1 → ① = 빠른정답 ✓.")

# p42
add(id="eacd1dee", qtype="choice",
    question=("이차방정식 [[2 pow(x,2) - 12x + A = 0]]의 근이 [[x = pm(B, frac(3 sqrt(2), 2))]]일 때, "
              "유리수 [[A]], [[B]]에 대하여 [[A - B]]의 값은?"),
    choices=C5(2, 4, 6, 8, 10), derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="x=3±√(144−8A)/4, 3√2/2=√72/4 → A=9, B=3 → 6 → ③. 빠른정답 4와 불일치.")

# p43
add(id="fc130fa9", qtype="short",
    question=("이차방정식 [[pow(x,2) + m x + 3 = 0]]의 해가 [[x = frac(pm(5, sqrt(n)), 2)]]일 때, "
              "[[m + n]]의 값을 구하시오. (단, [[m]]은 상수)"),
    choices=None, derived_answer="8", figure=None, difficulty_est=2, confidence=0.9,
    note="m=−5, n=25−12=13 → 8. 빠른정답 1과 불일치.")

# p46
add(id="deca96d6", qtype="short",
    question="이차방정식 [[3 pow(x,2) - 5x + A = 0]]의 근이 [[x = frac(pm(B, sqrt(13)), 6)]]일 때, [[A + B]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=2, confidence=0.9,
    note="B=5, 25−12A=13 → A=1 → 6. 빠른정답 8과 불일치.")

# p47
add(id="bd31778e", qtype="short",
    question="이차방정식 [[A pow(x,2) + 2x - 3 = 0]]의 두 근이 [[x = frac(pm(-1, sqrt(B)), 3)]]일 때, [[A - B]]의 값을 구하시오.",
    choices=None, derived_answer="-7", figure=None, difficulty_est=2, confidence=0.9,
    note="x=(−1±√(1+3A))/A → A=3, B=10 → −7 = 빠른정답 ✓.")

# p50
add(id="1bd00dba", qtype="short",
    question=("이차방정식 [[a pow(x,2) - 2x - 5 = 0]]의 근이 [[x = frac(pm(1, sqrt(b)), 3)]]일 때, "
              "[[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 유리수)"),
    choices=None, derived_answer="19", figure=None, difficulty_est=2, confidence=0.9,
    note="x=(1±√(1+5a))/a → a=3, b=16 → 19. 빠른정답 −7과 불일치.")

# p51
add(id="45a5c0c5", qtype="choice",
    question="이차방정식 [[3 pow(x,2) - 4x + p = 0]]의 근이 [[x = frac(pm(q, sqrt(7)), 3)]]일 때, [[p + q]]의 값은?",
    choices=C5(-2, -1, 0, 1, 2), derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="q=2, 4−3p=7 → p=−1 → 1 → ④ = 빠른정답 ✓.")

# p52
add(id="efbbfd04", qtype="choice",
    question="이차방정식 [[2 pow(x,2) - 5x + A = 0]]의 근이 [[x = frac(pm(B, sqrt(17)), 4)]]일 때, [[A + B]]의 값은?",
    choices=C5(2, 4, 6, 8, 10), derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="B=5, 25−8A=17 → A=1 → 6 → ③ = 빠른정답 ✓.")

# p53
add(id="546f969a", qtype="choice",
    question="이차방정식 [[3 pow(x,2) - 4x + p = 0]]의 근이 [[x = frac(pm(q, sqrt(13)), 3)]]일 때, [[p + q]]의 값은?",
    choices=C5(2, 1, 0, -1, -2), derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="q=2, 4−3p=13 → p=−3 → −1 → ④. 빠른정답 19와 불일치.")

# p54
add(id="881274dc", qtype="short",
    question=("이차방정식 [[a pow(x,2) + b x + c = 0]]의 근을 구하는데 근의 공식을 "
              "[[x = frac(pm(-b, sqrt(pow(b,2) - 4 a c)), a)]]로 잘못 외워서 어떤 이차방정식의 근을 구했더니 "
              "[[-10]], [[4]]가 나왔다. 이 이차방정식의 두 근의 곱을 구하시오."),
    choices=None, derived_answer="-10", figure=None, difficulty_est=3, confidence=0.9,
    note="잘못된 공식의 값은 참근의 2배 → 참근 −5, 2 → 곱 −10. 빠른정답 4와 불일치.")

# p55
add(id="8402f664", qtype="short",
    question=("이차방정식 [[7 pow(x,2) - 4x + A = 0]]의 근이 [[x = frac(pm(B, sqrt(C)), 7)]]이고 [[6A + C = 5]]일 때, "
              "[[A - B + C]]의 값을 구하시오. (단, [[A]], [[B]], [[C]]는 유리수이다.)"),
    choices=None, derived_answer="8", figure=None, difficulty_est=3, confidence=0.9,
    note="x=(2±√(4−7A))/7 → B=2, C=4−7A, 6A+C=5 → A=−1, C=11 → 8. 빠른정답 3과 불일치.")

# p62
add(id="7ef3cdd5", qtype="choice",
    question="이차방정식 [[3 pow(x,2) + A x + B = 0]]의 근이 [[pm(-4, sqrt(6))]]일 때,\n유리수 [[A]], [[B]]의 값은?",
    choices=["[[A = 12]], [[B = 20]]", "[[A = 12]], [[B = 30]]", "[[A = 24]], [[B = 20]]",
             "[[A = 24]], [[B = 30]]", "[[A = 24]], [[B = 36]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="근의 합 −8=−A/3, 곱 10=B/3 → A=24, B=30 → ④. 빠른정답 −1과 불일치.")

# p63
add(id="44bea7c1", qtype="short",
    question=("이차방정식 [[a pow(x,2) + b x + c = 0]]의 근을 구하는데 근의 공식을 "
              "[[x = frac(pm(-b, sqrt(pow(b,2) - 4 a c)), a)]]로 잘못 외워서 어떤 이차방정식의 근을 구했더니 "
              "[[-4]], [[1]]이 나왔다. 이 이차방정식의 두 근의 곱을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=3, confidence=0.9,
    note="참근 −2, 1/2 → 곱 −1 = 빠른정답 ✓.")

# p65
add(id="ba69728f", qtype="choice",
    question="이차방정식 [[pow(x,2) - 16x + a = 0]]의 해가 [[x = pm(8, sqrt(59))]]일 때, 상수 [[a]]의 값은?",
    choices=C5(1, 2, 3, 4, 5), derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="64−a=59 → a=5 → ⑤. 빠른정답 4와 불일치.")

# p66
add(id="8db7e127", qtype="choice",
    question="[[x = frac(pm(-3, sqrt(17)), 4)]]이 이차방정식 [[2 pow(x,2) + 3x + k = 0]]의 해일 때, 상수 [[k]]의 값은?",
    choices=C5(-1, 1, 2, -2, 3), derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="9−8k=17 → k=−1 → ① (빠른정답 '−1'은 값 표기로 보이며 ①과 일치).")

# p67
add(id="aa5c9c5a", qtype="choice",
    question="이차방정식 [[5 pow(x,2) - 4x + m = 0]]의 근이 [[x = frac(pm(2, sqrt(19)), 5)]]일 때, 상수 [[m]]의 값은?",
    choices=C5(-5, -4, -3, -2, -1), derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="4−5m=19 → m=−3 → ③ = 빠른정답 ✓.")

# p68
add(id="85590390", qtype="short",
    question="이차방정식 [[3 pow(x,2) + 7x + a = 0]]의 근이 [[frac(pm(-7, sqrt(13)), 6)]]일 때, 상수 [[a]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="49−12a=13 → a=3. 빠른정답 4와 불일치.")

# p75
add(id="2621b380", qtype="choice",
    question="이차방정식 [[2 pow(x,2) - 9x - a x + 3a + 8 = 0]]이 정수인 근을 가질 때, 정수 [[a]]의 값들의 합은?",
    choices=C5(6, 7, 8, 9, 10), derived_answer="①", figure=None, difficulty_est=4, confidence=0.85,
    note="a=(2x²−9x+8)/(x−3)=2x−3−1/(x−3) → x=4(a=4), x=2(a=2) → 합 6 → ①. 빠른정답 16과 불일치.")

# ============================ 복잡한 식의 인수분해 ============================
# p25
add(id="aa7ad22f", qtype="short",
    question=("[[(2x - y)(2x - y - 7z) + 12 pow(z,2)]]을 인수분해하면\n[[(2x + a y + b z)(c x - d y - 3z)]]일 때, "
              "상수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a + b + c + d]]의 값을 구하시오."),
    choices=None, derived_answer="-2", figure=None, difficulty_est=3, confidence=0.9,
    note="t=2x−y: (t−3z)(t−4z) → (2x−y−4z)(2x−y−3z) → a=−1, b=−4, c=2, d=1 → −2. 빠른정답 '2, 4'와 불일치.")

# p32
add(id="bccff4d0", qtype="choice",
    question=("[[pow(3x - y, 2) - pow(x + 2y, 2)]]을 인수분해하면\n[[(a x + y)(2x + b y)]]일 때, "
              "상수 [[a]], [[b]]에 대하여 [[a - b]]의 값은?"),
    choices=C5(3, 5, 7, 9, 11), derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="(2x−3y)(4x+y) → a=4, b=−3 → 7 → ③. 빠른정답 2와 불일치.")

# p33
add(id="28e09e70", qtype="short",
    question=("[[pow(4x - 3, 2) - pow(x + 7, 2)]]을 인수분해하였더니\n[[(5x + a)(b x + c)]]가 되었다. "
              "이때 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="-3", figure=None, difficulty_est=2, confidence=0.9,
    note="(3x−10)(5x+4) → a=4, b=3, c=−10 → −3. 빠른정답 5와 불일치.")

# p47
add(id="6a259be6", qtype="short",
    question=("[[(x - 3)(x - 1)(x + 3)(x + 5) + k = pow(pow(x,2) + a x + b, 2)]]일 때, "
              "상수 [[k]], [[a]], [[b]]에 대하여 [[k + a + b]]의 값을 구하시오."),
    choices=None, derived_answer="29", figure=None, difficulty_est=3, confidence=0.9,
    note="t=x²+2x: (t−15)(t−3)+k=(t−9)² → k=36, a=2, b=−9 → 29 = 빠른정답 ✓.")

# p48
add(id="dbb53a78", qtype="short",
    question=("[[(pow(x,2) + 2x)(pow(x,2) + 10x + 24) - 20]]\n= [[(pow(x,2) + a x + b)(pow(x,2) + c x + d)]]\n"
              "일 때, 상수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a + b + c + d]]의 값을 구하시오."),
    choices=None, derived_answer="20", figure=None, difficulty_est=3, confidence=0.9,
    note="x(x+2)(x+4)(x+6)−20, t=x²+6x: (t+10)(t−2) → 6+10+6−2=20. 빠른정답 1/6과 불일치.")

# p64
add(id="94eefe4f", qtype="choice",
    question="[[16 - pow(x,2) + 4 x y - 4 pow(y,2)]]을 인수분해하면?",
    choices=["[[(x + 2y - 4)(-x + 2y + 4)]]", "[[pow(x - 2y + 4, 2)]]", "[[(x - 2y + 4)(x + 2y - 4)]]",
             "[[(x - 2y + 4)(-x + 2y + 4)]]", "[[(-x - 2y + 4)(x + 2y + 4)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="16−(x−2y)²=(4−x+2y)(4+x−2y) → ④. 빠른정답 3과 불일치.")

# p67
add(id="2d53479a", qtype="choice",
    question=("[[25 pow(x,2) - 16 + 10 x y + pow(y,2)]]을 인수분해하였더니\n[[(a x + y + b)(a x + c y - 4)]]가 되었다.\n"
              "이때 상수 [[a]], [[b]], [[c]]에 대하여 [[a + b - c]]의 값은?"),
    choices=C5(8, 9, 10, 11, 12), derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="(5x+y)²−16=(5x+y+4)(5x+y−4) → a=5, b=4, c=1 → 8 → ① = 빠른정답 ✓.")

# p68
add(id="e43fb8bd", qtype="choice",
    question="[[121 pow(x,2) pow(y,2) - 16 pow(z,2) - 22 x y + 1]]을 인수분해하면?",
    choices=["[[pow(11 x y - 4z, 2)]]",
             "[[(11 x y + 4z - 1)(11 x y - 4z - 1)]]",
             "[[(11 x y + 4z + 1)(11 x y - 4z - 1)]]",
             "[[(11 x y + 4z + 1)(11 x y - 4z + 1)]]",
             "[[(11 x y - 4z + 1)(11 x y - 4z - 1)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(11xy−1)²−(4z)²=(11xy−1+4z)(11xy−1−4z) → ②. 빠른정답 4와 불일치.")

# p81
add(id="68f35af6", qtype="choice",
    question="[[pow(x,2) - 4 x y + 4 pow(y,2) + 2x - 4y - 15]]를 인수분해하면?",
    choices=["[[(x - 2y + 3)(x - 2y - 5)]]", "[[(x + 2y + 3)(x + 2y - 5)]]", "[[(x - 2y - 3)(x + 2y + 5)]]",
             "[[(x + 2y + 3)(x + 2y + 5)]]", "[[(x - 2y - 3)(x - 2y + 5)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="t=x−2y: t²+2t−15=(t+5)(t−3) → ⑤ = 빠른정답 ✓.")

# p88
add(id="328952fb", qtype="choice",
    question=("세 자연수 [[a]], [[b]], [[c]]에 대하여\n[[a b c + a b + b c + a c + a + b + c + 1 = 154]]일 때,\n"
              "[[a + b + c]]의 값은? (단, [[a < b < c]])"),
    choices=C5(11, 13, 15, 17, 19), derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="(a+1)(b+1)(c+1)=154=2·7·11 → a=1, b=6, c=10 → 17 → ④. 빠른정답 0과 불일치.")

# p89
add(id="6e62b809", qtype="choice",
    question=("세 자연수 [[a]], [[b]], [[c]]에 대하여\n[[a b c - a b + b c + a c - a - b + c - 1 = 273]]일 때,\n"
              "[[a + b + c]]의 값은? (단, [[a < b < c]])"),
    choices=C5(18, 20, 22, 24, 26), derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="(a+1)(b+1)(c−1)=273=3·7·13 → a=2, b=6, c=14 → 22 → ③. 빠른정답 5와 불일치.")

# p90
add(id="7ab118d5", qtype="choice",
    question=("세 자연수 [[a]], [[b]], [[c]]에 대하여\n[[a b c + a b + b c - a c - a + b - c - 1 = 595]]일 때,\n"
              "[[a + b + c]]의 값은? (단, [[a < b < c]])"),
    choices=C5(26, 28, 30, 32, 34), derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="(a+1)(b−1)(c+1)=595=5·7·17 → a=4, b=8, c=16 → 28 → ②. 빠른정답 5와 불일치.")

# p91
add(id="7a07eed7", qtype="short",
    question=("[[pow(x,2) - 4 x y + 3 pow(y,2) + 3x - 5y + 2]]를 인수분해하였더니\n[[(x - y + a)(x + b y + c)]]일 때, "
              "상수 [[a]], [[b]], [[c]]에 대하여 [[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=3, confidence=0.9,
    note="(x−y+1)(x−3y+2) → a=1, b=−3, c=2 → 0 = 빠른정답 ✓.")

# p92
add(id="51ba3d6b", qtype="choice",
    question="다음 중 [[pow(x,2) + 5 pow(y,2) + 6 x y - x - 9y - 2]]의 인수인 것은?",
    choices=["[[x - 2y - 1]]", "[[x - y + 2]]", "[[x + y + 2]]", "[[x + 5y - 1]]", "[[x + 5y + 1]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="(x+y−2)(x+5y+1) → ⑤. 빠른정답 3과 불일치.")

# p99 (이미지에 별개 문항 2개, id 1개 → draft_a·src_tag 대응인 하단 문항 전사)
add(id="0e8f1729", qtype="choice",
    question="[[pow(x,2) + 5 x y + 2x - 5y - 3]]을 인수분해하면?",
    choices=["[[(x + 1)(x + 5y + 3)]]", "[[(x - 1)(x - 5y + 3)]]", "[[(x - 1)(x + 5y - 3)]]",
             "[[(x - 1)(x + 5y + 3)]]", "[[(x + 1)(x - 5y - 3)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    needs_review="이미지에 별개 문항 2개 인쇄(id는 1개): 상단 'x²−y²−8x+2y+15의 인수를 모두 고르면?(정답 2개)' 문항은 미전사, 하단 문항(draft_a 대응)만 전사",
    note="x²+(5y+2)x−(5y+3)=(x−1)(x+5y+3) → ④. 빠른정답 3과 불일치. 상단 문항의 답은 ②③(x−y−3, x+y−5).")

# ============================ 곱셈 공식을 이용한 수의 계산 ============================
# p23
add(id="265b3061", qtype="choice",
    question="곱셈 공식 [[(x + a)(x + b) = pow(x,2) + (a + b) x + a b]]를 이용하여 계산하면 가장 편리한 것은?",
    choices=["[[5.3 × 4.7]]", "[[103 × 104]]", "[[pow(96,2)]]", "[[pow(101,2)]]", "[[102 × 98]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="103×104=(100+3)(100+4) → ②. 빠른정답 4와 불일치.")

# p71
add(id="0cf8e9d7", qtype="choice",
    question="[[a(5 + 6 sqrt(7)) + pow(3 sqrt(7) - 4, 2)]]을 계산한 결과가 유리수가 되도록 하는 유리수 [[a]]의 값은?",
    choices=C5(3, 4, 5, 6, 7), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="√7 계수 6a−24=0 → a=4 → ② = 빠른정답 ✓.")

# p98 (선지 ④⑤ 잘림)
add(id="38d139f1", qtype="choice",
    question=("다음 □ 안에 공통으로 들어갈 알맞은 수는?\n"
              "[[frac(1, sqrt(7) - 2)]] = ( [[1]] × (□) ) / ( ([[sqrt(7) - 2]])(□) ) = (□)/[[3]]"),
    choices=["[[-sqrt(7) + 2]]", "[[sqrt(7) - 2]]", "[[sqrt(7) + 2]]", "(이미지 하단 잘림)", "(이미지 하단 잘림)"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움)",
    note="분모 유리화: 공통 빈칸은 √7+2 → ③ = 빠른정답 ✓. 빈칸 □ 식은 텍스트 조각.")

# ============================ 이차방정식의 중근 ============================
# p6
add(id="131ecac9", qtype="choice",
    question="이차방정식 [[36 pow(x,2) + 6x + frac(1,4) = 0]]을 인수분해를 이용하여 풀면?",
    choices=["[[x = -frac(1,3)]] 또는 [[x = frac(1,2)]]",
             "[[x = -frac(1,2)]] 또는 [[x = frac(1,3)]]",
             "[[x = -frac(1,4)]] 또는 [[x = frac(1,6)]]",
             "[[x = -frac(1,6)]] (중근)",
             "[[x = -frac(1,12)]] (중근)"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="×4: (12x+1)²=0 → x=−1/12 (중근) → ⑤ (빠른정답 없음).")

# p28
add(id="4792c7ea", qtype="short",
    question=("이차방정식 [[pow(x,2) + a x + b = 0]]이 중근 [[x = -3]]을 가질 때,\n"
              "상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="15", figure=None, difficulty_est=1, confidence=0.9,
    note="(x+3)²=x²+6x+9 → a+b=15. 빠른정답 −2와 불일치.")

# p33
add(id="71f3225e", qtype="short",
    question=("[[frac(1,18) pow(x,2) - frac(1,3) x y + frac(1,2) pow(y,2) = 0]]일 때, [[frac(2x + y, x - 2y)]]의 값을 "
              "구하시오. (단, [[x != 0]], [[y != 0]])"),
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.9,
    note="×18: (x−3y)²=0 → x=3y → 7y/y=7 = 빠른정답 ✓.")

# p34
add(id="39e25231", qtype="short",
    question=("[[frac(1,25) pow(x,2) - frac(1,10) x y + frac(1,16) pow(y,2) = 0]]일 때, [[frac(x - 3y, 2x + y)]]의 값을 "
              "구하시오. (단, [[x != 0]], [[y != 0]])"),
    choices=None, derived_answer="-frac(1,2)", figure=None, difficulty_est=2, confidence=0.9,
    note="(x/5−y/4)²=0 → 4x=5y → (5y/4−3y)/(5y/2+y)=−1/2 = 빠른정답 frac(-1,2) ✓(표기만 다름).")

# p60
add(id="baebafd1", qtype="choice",
    question="이차방정식 [[2 pow(x,2) + a x + 8 = 0]]이 중근을 가질 때,\n양수 [[a]]의 값은?",
    choices=C5(1, 2, 4, 6, 8), derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="a²−64=0 → a=8 → ⑤. 빠른정답 −15와 불일치.")

# p91
add(id="7f5808fa", qtype="short",
    question=("두 이차방정식 [[2 pow(x,2) - 5 a x + 8 = 0]]과 [[pow(x,2) + b x + c = 0]]을 동시에 만족시키는 근은 "
              "[[x = -1]]이고, 이차방정식 [[pow(x,2) + b x + c = 0]]이 중근을 가질 때, 상수 [[a]], [[b]], [[c]]에 대하여 "
              "[[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.9,
    note="x=−1 대입: a=−2; (x+1)² → b=2, c=1 → 1 = 빠른정답 ✓.")

# ============================ 완전제곱식을 이용한 이차방정식의 풀이 ============================
# p2
add(id="dfe3cd61", qtype="choice",
    question=("이차방정식 [[(x - 1)(x - 5) = 4]]를 [[pow(x + a, 2) = b]]의 꼴로 나타낼 때, [[a + b]]의 값은? "
              "(단, [[a]], [[b]]는 상수)"),
    choices=C5(3, 5, 7, 9, 11), derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="x²−6x+1=0 → (x−3)²=8 → a=−3, b=8 → 5 → ② = 빠른정답 ✓.")
