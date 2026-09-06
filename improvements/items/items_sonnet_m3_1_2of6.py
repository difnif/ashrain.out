# -*- coding: utf-8 -*-
# esc_sonnet_m3-1_2of6 — 이미지 기준 전사 (86 항목 / 80쪽)
# 단원 m3-1: 완전제곱식을 이용한 이차방정식의 풀이 / 인수분해 공식의 활용 / 제곱근의 곱셈과 나눗셈 / 이차함수의 최댓값과 최솟값 / 곱셈 공식 / 인수분해 공식
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ======================= 완전제곱식을 이용한 이차방정식의 풀이 =======================
# p34
add(id="8f4874dc", qtype="short",
    question=("이차방정식 [[(2x + 6)(x - 1) = 8]]을 [[pow(x - a, 2) = b]]의 꼴로 고칠 때, [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="-8", figure=None, difficulty_est=2,
    note="2x²+4x−14=0 → x²+2x−7=0 → (x+1)²=8 → a=−1, b=8 → ab=−8. 빠른정답 9와 불일치.")

# p35
add(id="cc191ac9", qtype="short",
    question=("이차방정식 [[pow(x,2) - 8x + 11 = 0]]의 해가 [[x = pm(a, sqrt(b))]]일 때,\n"
              "유리수 [[a]], [[b]]에 대하여 [[a - b]]의 값을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2,
    note="(x−4)²=5 → x=4±√5 → a−b=−1. 빠른정답 36과 불일치.")

# p36
add(id="90b987a8", qtype="short",
    question=("이차방정식 [[pow(x,2) - 6x + 6 = 0]]의 해가 [[x = pm(a, sqrt(b))]]일 때,\n"
              "유리수 [[a]], [[b]]에 대하여 [[a - b]]의 값을 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=2,
    note="(x−3)²=3 → x=3±√3 → a−b=0. 빠른정답 3과 불일치.")

# p39
add(id="d4199678", qtype="short",
    question=("이차방정식 [[pow(x,2) - 4x = p]]를 완전제곱식을 이용하여 풀었더니 해가 [[x = pm(q, sqrt(8))]]이었다. "
              "이때 유리수 [[p]], [[q]]에 대하여 [[p q]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2,
    note="(x−2)²=p+4=8 → p=4, q=2 → pq=8. 빠른정답 0과 불일치.")

# p41
add(id="63a8e53a", qtype="short",
    question=("이차방정식 [[2 pow(x,2) + 12x - 18 = 0]]을 완전제곱식을 이용하여 풀었더니 해가 [[x = pm(a, 3 sqrt(b))]]가 되었다.\n"
              "정수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2,
    note="x²+6x−9=0 → (x+3)²=18 → x=−3±3√2 → a+b=−1 = 빠른정답 ✓.")

# p42
add(id="f07858a7", qtype="short",
    question=("이차방정식 [[2 pow(x,2) - 8x - k = 0]]의 해가 [[x = pm(2, sqrt(7))]]일 때, 상수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2,
    note="x²−4x−k/2=0 → (x−2)²=4+k/2=7 → k=6. 빠른정답 8과 불일치.")

# p44
add(id="57eb1e1f", qtype="short",
    question=("이차방정식 [[3 pow(x,2) - 12x - 6 = 0]]을 [[pow(x + a, 2) = b]]의 꼴로 나타내어 풀었더니 해가 [[x = pm(c, sqrt(d))]]이었다.\n"
              "유리수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a b c d]]의 값을 구하시오."),
    choices=None, derived_answer="-144", figure=None, difficulty_est=2,
    note="x²−4x−2=0 → (x−2)²=6 → a=−2, b=6, c=2, d=6 → abcd=−144. 빠른정답 −1과 불일치.")

# p45
add(id="6c31d043", qtype="short",
    question=("이차방정식 [[3 pow(x,2) + 18x - 9 = 0]]을 완전제곱식을 이용하여 풀었더니 해가 [[x = pm(a, 2 sqrt(b))]]가 되었다.\n"
              "정수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="0", figure=None, difficulty_est=2,
    note="x²+6x−3=0 → (x+3)²=12 → x=−3±2√3 → a+b=0. 빠른정답 6과 불일치.")

# p46
add(id="980049e6", qtype="choice",
    question=("이차방정식 [[2 pow(x,2) + 4x - 4 = 0]]을 완전제곱식을 이용하여 풀었더니 해가 [[x = pm(A, sqrt(B))]]이었다. "
              "이때 유리수 [[A]], [[B]]에 대하여 [[A + B]]의 값은?"),
    choices=["1", "2", "3", "4", "5"], derived_answer="②", figure=None, difficulty_est=2,
    note="x²+2x−2=0 → (x+1)²=3 → A=−1, B=3 → 2 → ②. 빠른정답 3과 불일치.")

# p47
add(id="87b69c03", qtype="choice",
    question=("이차방정식 [[3 pow(x,2) + 12x - 6 = 0]]을 완전제곱식을 이용하여 풀었더니 해가 [[x = pm(A, sqrt(B))]]이었다. "
              "이때 유리수 [[A]], [[B]]에 대하여 [[A + B]]의 값은?"),
    choices=["1", "2", "3", "4", "5"], derived_answer="④", figure=None, difficulty_est=2,
    note="x²+4x−2=0 → (x+2)²=6 → A=−2, B=6 → 4 → ④ = 빠른정답 ✓.")

# p56
add(id="90f314e3", qtype="short",
    question=("이차방정식 [[pow(x,2) - 4 a x + 5 = 0]]을 완전제곱식을 이용하여 풀었더니 해가 [[x = pm(-4, sqrt(b))]]이었다. "
              "이때 유리수 [[a]], [[b]]에 대하여 [[b - a]]의 값을 구하시오."),
    choices=None, derived_answer="13", figure=None, difficulty_est=2,
    note="(x−2a)²=4a²−5 → 2a=−4 → a=−2, b=11 → b−a=13. 빠른정답 1과 불일치.")

# p62 (원판 그림)
add(id="573a21e5", qtype="short",
    question=("다음 그림과 같이 한 자리 숫자가 하나씩 적힌 원판에 화살을 던져 맞힌 칸의 숫자를 이차방정식 "
              "[[pow(x,2) - 8x]] − □ = 0의 □ 안에 써놓고 이차방정식을 풀어 자연수인 해 중 가장 큰 수의 크기만큼 상품을 받는 "
              "놀이를 한다고 하자. 원판의 어떤 숫자가 적힌 칸을 맞혀야 가장 많은 상품을 받을 수 있는지 구하시오.\n"
              "(단, 이차방정식을 풀어 자연수인 해가 나오지 않는 경우는 상품을 받지 못한다.)"),
    choices=None, derived_answer="9",
    figure=[{"fn": "unsupported", "args": {"raw": "8등분 원판(색칠). 시계 방향으로 위 오른쪽부터 0, 1, 2, 3, 9, 8, 7, 6이 적혀 있음(오른쪽 반원 위→아래 0·1·2·3, 왼쪽 반원 아래→위 9·8·7·6)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 숫자 0~3·6~9가 적힌 8칸 원판 그림",
    note="x=4±√(16+n): n=9 → x=9(최대), n=0 → x=8, 나머지는 무리수 → 9. 빠른정답 5와 불일치.")

# p63
add(id="a0ad19c5", qtype="choice",
    question=("이차방정식 [[frac(4,3) pow(x,2) = 4x - 1]]의 해가 [[x = frac(pm(A, sqrt(B)), 2)]]일 때,\n"
              "[[A + B]]의 값은? (단, [[A]], [[B]]는 유리수)"),
    choices=["[[-12]]", "[[-9]]", "3", "9", "12"], derived_answer="④", figure=None, difficulty_est=3,
    note="4x²−12x+3=0 → (x−3/2)²=3/2 → x=(3±√6)/2 → A+B=9 → ④. 빠른정답 1과 불일치.")

# p65
add(id="a5076598", qtype="short",
    question=("이차방정식 [[2 pow(x,2) - 4x - a - 1 = 0]]을 완전제곱식을 이용하여 풀었더니 해가 [[x = pm(1, sqrt(3))]]이었다.\n"
              "이때 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=2,
    note="(x−1)²=1+(a+1)/2=3 → a=3 = 빠른정답 ✓.")

# p67
add(id="eb96d899", qtype="short",
    question=("이차방정식 [[pow(x,2) + 4 a x + b = 0]]의 근이 [[x = pm(2, 2 sqrt(3))]]일 때, 상수 [[a]], [[b]]에 대하여 [[a - b]]의 값을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=2,
    note="(x+2a)²=4a²−b → −2a=2, 4a²−b=12 → a=−1, b=−8 → a−b=7 = 빠른정답 ✓.")

# ======================= 인수분해 공식의 활용 =======================
# p14 (증명 + 빈칸)
add(id="c4077880", qtype="essay",
    question=("연속한 네 자연수의 곱에 1을 더한 수는 어떤 자연수의 제곱이 됨을 증명하고, 다음 □ 안에 알맞은 수를 쓰시오.\n"
              "[[6 × 7 × 8 × 9 + 1]] = □²"),
    choices=None, derived_answer="55", figure=None, difficulty_est=3, confidence=0.85,
    note="n(n+1)(n+2)(n+3)+1=(n²+3n+1)² → 6·7·8·9+1=3025=55². 빠른정답 없음(증명 요구 서술형, 빈칸 답 55).")

# p24
add(id="3ad5f3e4", qtype="short",
    question=("자연수 [[a]], [[b]]에 대하여\n[[399 × 401 + 1 = pow(a,2)]], [[sqrt(20 × 21 × 22 × 23 + 1) = b]]일 때, [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="861", figure=None, difficulty_est=3,
    note="399·401+1=400² → a=400; 20·21·22·23+1=(400+60+1)²=461² → b=461 → 861. 빠른정답 5와 불일치.")

# p35 (수직선+정사각형 그림)
add(id="ec0b1cd9", qtype="short",
    question=("다음 그림과 같이 넓이가 7인 정사각형 ABCD에 대하여 [[seg(AB) = seg(AP)]], [[seg(AD) = seg(AQ)]]가 되도록 수직선 위에 두 점 P, Q를 정할 때, "
              "두 점 P, Q에 대응하는 수를 각각 [[a]], [[b]]라 하자. [[pow(a,3) - pow(a,2) b - a pow(b,2) + pow(b,3)]]의 값을 구하시오."),
    choices=None, derived_answer="168",
    figure=[{"fn": "unsupported", "args": {"raw": "수직선 위의 점 A(3)를 아래 꼭짓점으로 하는 정사각형 ABCD(C 위, D 왼쪽, B 오른쪽, 색칠). B에서 오른쪽 P로, D에서 왼쪽 Q로 점선 호. 수직선에 Q, 3, P 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 수직선+정사각형+호 도형",
    note="a=3+√7, b=3−√7 → (a−b)²(a+b)=28·6=168. 빠른정답 2와 불일치.")

# p68
add(id="5d9ecb5e", qtype="short",
    question=("[[x + y = 7]]이고 [[pow(x,2) - 2 pow(y,2) - x y + 4x + 4y = 14]]일 때,\n"
              "[[frac(pow(x,2) - 4 pow(y,2) + x + 6y - 2, x + 2y - 1)]]의 값을 구하시오.\n(단, [[x + 2y != 1]])"),
    choices=None, derived_answer="0", figure=None, difficulty_est=3,
    note="(x+y)(x−2y+4)=14 → x−2y=−2; 분자=(x+2y−1)(x−2y+2) → x−2y+2=0. 빠른정답 4와 불일치.")

# p70 (직사각형 삽화)
add(id="afd47e43", qtype="choice",
    question=("다음 그림과 같이 직사각형의 넓이가 [[3 pow(x,2) - 8 x y + 4 pow(y,2)]]일 때 직사각형의 둘레의 길이는?"),
    choices=["[[4x]]", "[[8x]]", "[[8x + 4y]]", "[[8x - 8y]]", "[[8y]]"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형(색칠) 내부에 3x²−8xy+4y² 표기"}}],
    difficulty_est=2, confidence=0.85,
    note="(3x−2y)(x−2y) → 둘레 2(4x−4y)=8x−8y → ④. 빠른정답 2와 불일치. 그림은 장식(식만 표기).")

# p81
add(id="a049c7ef", qtype="choice",
    question=("밑면의 가로와 세로가 각각 [[3x - 1]], [[x - 2y]]인 직육면체의 부피가 [[3 pow(x,3) - 7 pow(x,2) - 6 pow(x,2) y + 2x + 14 x y - 4y]]이다.\n"
              "이때 이 직육면체의 높이를 구하면?"),
    choices=["[[x - 2]]", "[[x - 1]]", "[[x + 1]]", "[[x + 2]]", "[[2x + 1]]"], derived_answer="①", figure=None, difficulty_est=3,
    note="(3x−1)(x−2y)(x−2) 전개 일치 → ① = 빠른정답 ✓.")

# ======================= 제곱근의 곱셈과 나눗셈 =======================
# p6 (모눈종이 수직선 그림)
add(id="be66df0d", qtype="choice",
    question=("다음 그림과 같이 한 눈금의 길이가 1인 모눈종이 위에 수직선과 두 직각삼각형 ABO, COD를 그리고 "
              "[[seg(AO) = seg(PO)]], [[seg(CO) = seg(QO)]]가 되도록 수직선 위에 두 점 P, Q를 정할 때, 두 점 P, Q에 대응하는 수의 곱은?"),
    choices=["[[-sqrt(14)]]", "[[-2 sqrt(3)]]", "[[-sqrt(10)]]", "[[-2 sqrt(2)]]", "[[-sqrt(6)]]"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "모눈종이(눈금 1) 위 수직선(−3~2). 직각삼각형 ABO: A(−2, 1), B(−2, 0), O(0, 0), ∠B 직각(색칠). 직각삼각형 COD: C(1, 1), D(1, 0), O(색칠). A에서 왼쪽 P로, C에서 오른쪽 Q로 붉은 호"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 모눈종이 수직선+직각삼각형 2개 도형",
    note="AO=√5 → P=−√5, CO=√2 → Q=√2 → 곱 −√10 → ③. 빠른정답 4와 불일치.")

# p11 (id 4개, 같은 문항)
dup(["21f1dc05", "dc8e6c81", "f644da52", "eabc3504"], qtype="choice",
    question="다음 □ 안에 들어갈 수 중 가장 큰 것은?",
    choices=["[[sqrt(20)]] = □[[sqrt(5)]]", "[[-sqrt(45)]] = [[-3]]√□", "[[sqrt(63)]] = □[[sqrt(7)]]",
             "[[sqrt(96)]] = 4√□", "[[sqrt(176)]] = □[[sqrt(11)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.85,
    note="□: 2, 5, 3, 6, 4 → 가장 큰 것 ④ = 빠른정답 ✓. 빈칸 □·√는 텍스트 혼합.")

# p22
add(id="24692a13", qtype="short",
    question=("[[a < 0]], [[b < 0]], [[sqrt(a b) = 7]]일 때, [[a sqrt(frac(b,a)) - 2b sqrt(frac(a,b))]]의 값을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=3,
    note="a<0: a√(b/a)=−√(ab)=−7, b<0: −2b√(a/b)=2√(ab)=14 → 7. 빠른정답 4와 불일치.")

# p37 (id 3개, 같은 문항)
dup(["14e72bc7", "7f509804", "ff9fb399"], qtype="choice",
    question="다음 중 □ 안에 알맞은 수가 가장 작은 것은?",
    choices=["[[2 sqrt(5)]] = √□", "[[sqrt(50)]] = □[[sqrt(2)]]", "[[-sqrt(48)]] = [[-4]]√□",
             "[[sqrt(108)]] = □[[sqrt(3)]]", "[[frac(sqrt(7), 5)]] = √(7/□)"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.85,
    note="□: 20, 5, 3, 6, 25 → 가장 작은 것 ③ = 빠른정답 ✓. 빈칸 □·√는 텍스트 혼합.")

# p38
add(id="b9de74cc", qtype="choice",
    question=("[[a > 0]], [[b > 0]], [[a b = 2]]일 때, [[a sqrt(frac(27b, a)) - frac(2, b) sqrt(frac(3b, a))]]의 값은?"),
    choices=["[[-sqrt(3)]]", "[[2 sqrt(6)]]", "5", "[[6 sqrt(2)]]", "[[5 sqrt(3)]]"], derived_answer="②", figure=None, difficulty_est=3,
    note="√(27ab)=3√6, 2√(3/(ab))=√6 → 2√6 → ②. 빠른정답 4와 불일치.")

# p41
add(id="36ae49f4", qtype="choice",
    question=("[[p > 0]], [[q > 0]], [[p q = 3]]일 때,\n"
              "[[p sqrt(frac(3q, p)) - frac(1, p) sqrt(frac(12p, q)) + q sqrt(frac(27p, q))]]의 값은?"),
    choices=["[[-16]]", "[[-14]]", "[[-10]]", "10", "14"], derived_answer="④", figure=None, difficulty_est=3,
    note="√(3pq)=3, √(12/(pq))=2, √(27pq)=9 → 3−2+9=10 → ④ = 빠른정답 ✓.")

# p43 (빈칸 상자 식)
add(id="14fd6ff0", qtype="short",
    question=("다음 □ 안에 알맞은 수를 모두 더하시오.\n"
              "[[sqrt(0.13)]] = √(13/□) = √(13/□²) = [[sqrt(13)]]/□"),
    choices=None, derived_answer="120", figure=None, difficulty_est=2, confidence=0.85,
    note="√(13/100)=√(13/10²)=√13/10 → 100+10+10=120. 빠른정답 27과 불일치. 빈칸 □ 식은 텍스트 혼합.")

# p76 (삼각형+수선 그림)
add(id="83e67909", qtype="choice",
    question=("다음 그림과 같이 [[seg(BC) = 3 sqrt(2)]] cm인 삼각형 ABC의 넓이가 [[3 sqrt(6)]] cm²일 때, [[seg(AH)]]의 길이는?"),
    choices=["[[2 sqrt(3)]] cm", "[[sqrt(14)]] cm", "4 cm", "[[2 sqrt(5)]] cm", "[[2 sqrt(6)]] cm"], derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(색칠, A 위·B 왼쪽 아래·C 오른쪽 아래). A에서 BC에 내린 수선의 발 H(직각 표시). BC=3√2 cm(아래 점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+수선 도형",
    note="½·3√2·AH=3√6 → AH=2√3 → ①. 빠른정답 3과 불일치.")

# p77 (정사각형 4개 배열 그림)
add(id="b7f352ab", qtype="choice",
    question=("다음 그림에서 네 정사각형 A, B, C, D의 각각의 넓이 [[sub(S,1)]], [[sub(S,2)]], [[sub(S,3)]], [[sub(S,4)]]에 대하여 "
              "[[sub(S,1) = 1]], [[sub(S,2) = frac(1,3) sub(S,1)]], [[sub(S,3) = frac(1,3) sub(S,2)]], [[sub(S,4) = frac(1,3) sub(S,3)]]일 때, "
              "정사각형 D의 한 변의 길이는?"),
    choices=["[[frac(1,9)]]", "[[frac(1,3)]]", "[[frac(sqrt(3), 9)]]", "[[frac(sqrt(3), 3)]]", "[[frac(sqrt(3), 2)]]"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 A(S₁)·B(S₂)·C(S₃)·D(S₄)가 왼쪽부터 크기 순으로 밑변을 맞춰 나란히 붙어 있음"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 4개 배열 도형",
    note="S₄=1/27 → 변 √(1/27)=√3/9 → ③ = 빠른정답 ✓.")

# ======================= 이차함수의 최댓값과 최솟값 =======================
# p24
add(id="a0c0e199", qtype="short",
    question=("이차함수 [[y = pow(x,2) + 6 a x - b]]의 그래프의 꼭짓점이 직선 [[y = -x + 1]] 위에 있을 때, [[b]]의 최댓값을 구하시오.\n"
              "(단, [[a]], [[b]]는 상수)"),
    choices=None, derived_answer="-frac(3,4)", figure=None, difficulty_est=3,
    note="꼭짓점 (−3a, −9a²−b) → b=−9a²−3a−1=−9(a+1/6)²−3/4 → 최댓값 −3/4 = 빠른정답 ✓.")

# p25 (그래프 그림)
add(id="87e6fbf0", qtype="short",
    question=("다음 그림과 같이 이차함수 [[y = frac(1,4) pow(x,2) + x + k]]의 그래프가 [[x]]축과 만나는 두 점을 A, B라 할 때, [[seg(AB) = 8]]이다. "
              "이 이차함수의 최솟값을 [[m]]이라 할 때, 상수 [[k]], [[m]]에 대하여 [[k + m]]의 값을 구하시오."),
    choices=None, derived_answer="-7",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 아래로 볼록한 포물선이 x축과 A(왼쪽)·B(오른쪽)에서 만남, 원점 O, 꼭짓점은 x축 아래"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 이차함수 그래프",
    note="축 x=−2, A=−6, B=2 → k=−3, m=−4 → −7 = 빠른정답 ✓.")

# p26 (그래프 그림)
add(id="0d14018c", qtype="short",
    question=("다음 그림과 같이 이차함수 [[y = frac(1,2) pow(x,2) + 2x + k]]의 그래프가 [[x]]축과 만나는 두 점을 A, B라 할 때, "
              "[[seg(AB) = 12]]이다. 이 이차함수의 최솟값을 [[m]]이라 할 때, 상수 [[k]], [[m]]에 대하여 [[k + m]]의 값을 구하시오."),
    choices=None, derived_answer="-34",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 아래로 볼록한 포물선이 x축과 A(왼쪽)·B(오른쪽)에서 만남, 원점 O, 꼭짓점은 x축 아래"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 이차함수 그래프",
    note="축 x=−2, A=−8, B=4 → k=−16, m=−18 → −34 = 빠른정답 ✓.")

# p30
add(id="c079dea7", qtype="short",
    question=("이차함수 [[y = -2 pow(x,2) + k x + 1]]의 그래프가 점 [[point(2, 5)]]를 지날 때, 이 이차함수의 최댓값을 구하시오. (단, [[k]]는 실수)"),
    choices=None, derived_answer="frac(11,2)", figure=None, difficulty_est=2,
    note="k=6 → y=−2(x−3/2)²+11/2 → 11/2 = 빠른정답 ✓.")

# p31
add(id="291412e2", qtype="short",
    question=("이차함수 [[y = 2 pow(x,2) + a x + b]]의 그래프가 [[x]]축과 두 점 [[point(-4, 0)]], [[point(1, 0)]]에서 만난다. "
              "이 이차함수의 최솟값을 [[m]]이라 할 때, [[a + b - m]]의 값을 구하시오.\n(단, [[a]], [[b]]는 실수)"),
    choices=None, derived_answer="frac(21,2)", figure=None, difficulty_est=3,
    note="y=2(x+4)(x−1)=2x²+6x−8 → a=6, b=−8, m=−25/2 → 21/2 = 빠른정답 ✓.")

# p38
add(id="eb58901f", qtype="short",
    question=("이차함수 [[y = -3 pow(x,2) - 12 p x - 6p]]의 최댓값이 18일 때, 이 그래프의 꼭짓점의 [[x]]좌표를 구하시오. (단, [[p < 0]])"),
    choices=None, derived_answer="2", figure=None, difficulty_est=3,
    note="y=−3(x+2p)²+12p²−6p → 12p²−6p=18 → p=−1(p<0) → 꼭짓점 x=−2p=2. 빠른정답 9와 불일치.")

# p44
add(id="c82b4356", qtype="short",
    question=("이차함수 [[y = -pow(x,2) + 2 k x - 2 pow(k,2) + 3k - 1]]의 최댓값이 [[-5]]가 되도록 하는 모든 실수 [[k]]의 값의 곱을 구하시오."),
    choices=None, derived_answer="-4", figure=None, difficulty_est=3,
    note="최댓값 −k²+3k−1=−5 → k²−3k−4=0 → 곱 −4. 빠른정답 13과 불일치.")

# p48
add(id="eb6c3d6d", qtype="short",
    question=("이차함수 [[f(x) = pow(x,2) - 4 k x + 5k]]의 최솟값이 [[-6]]이 되도록 하는 모든 실수 [[k]]의 값의 곱을 구하시오."),
    choices=None, derived_answer="-frac(3,2)", figure=None, difficulty_est=3,
    note="최솟값 −4k²+5k=−6 → 4k²−5k−6=0 → 곱 −3/2. 빠른정답 3/2와 부호 불일치.")

# p51 (조건 상자)
add(id="4661cb32", qtype="choice",
    question=("이차함수 [[f(x) = a pow(x,2) + b x + c]]가 다음 조건을 모두 만족할 때, [[f(2)]]의 값은? (단, [[a]], [[b]], [[c]]는 상수이다.)\n"
              "(가) [[y = f(x)]]의 그래프가 점 [[point(1, -2)]]를 지난다.\n"
              "(나) [[y = f(x)]]의 그래프의 축의 방정식은 [[x = -1]]이다.\n"
              "(다) [[f(x)]]의 최댓값은 2이다."),
    choices=["[[-7]]", "[[-5]]", "[[-3]]", "[[-1]]", "1"], derived_answer="①", figure=None, difficulty_est=3,
    note="f(x)=a(x+1)²+2, f(1)=4a+2=−2 → a=−1 → f(2)=−7 → ① = 빠른정답 ✓.")

# p55
add(id="e5afa78e", qtype="choice",
    question=("이차함수 [[y = pow(x,2) + 2 a x + b]]가 [[x = -1]]에서 최솟값 [[-5]]를 가질 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?"),
    choices=["[[-5]]", "[[-3]]", "[[-1]]", "1", "3"], derived_answer="②", figure=None, difficulty_est=2,
    note="축 x=−a=−1 → a=1; b−1=−5 → b=−4 → a+b=−3 → ②. 빠른정답 1과 불일치.")

# p58
add(id="1289e5ff", qtype="choice",
    question=("이차함수 [[y = -3 pow(x,2) - a x + 1]]이 [[x = 1]]에서 최댓값 [[b]]를 가질 때, [[a + b]]의 값은? (단, [[a]]는 상수이다.)"),
    choices=["[[-3]]", "[[-2]]", "[[-1]]", "1", "2"], derived_answer="②", figure=None, difficulty_est=2,
    note="축 x=−a/6=1 → a=−6; b=−3+6+1=4 → a+b=−2 → ② = 빠른정답 ✓.")

# p60
add(id="bdf17e13", qtype="choice",
    question=("이차함수 [[y = a pow(x,2) + b x + c]]가 [[x = 3]]에서 최솟값 [[-18]]을 갖는다. 이 이차함수의 그래프가 제3사분면을 지나지 않을 "
              "때, [[a]]의 값의 범위는? (단, [[a]], [[b]], [[c]]는 실수)"),
    choices=["[[a <= -2]]", "[[a <= 2]]", "[[a >= -2]]", "[[a >= 1]]", "[[a >= 2]]"], derived_answer="⑤", figure=None, difficulty_est=3,
    note="y=a(x−3)²−18 (a>0), x=0에서 9a−18≥0 → a≥2 → ⑤. 빠른정답 4와 불일치.")

# p61
add(id="44b87a85", qtype="short",
    question=("이차함수 [[y = -3 pow(x,2) + a x + b]]의 축의 방정식이 [[x = -1]]이고 최댓값이 4일 때, 상수 [[a]], [[b]]에 대하여\n"
              "[[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="-5", figure=None, difficulty_est=2,
    note="a/6=−1 → a=−6; 3+b=4 → b=1 → −5 = 빠른정답 ✓.")

# p70
add(id="fc5a2c7f", qtype="choice",
    question=("[[x = -2]]에서 최솟값 3을 갖는 이차함수의 그래프를 [[x]]축의 방향으로 1만큼, [[y]]축의 방향으로 [[m]]만큼 평행이동하였더니 "
              "이차함수 [[y = 2 pow(x,2) + n x + 9]]의 그래프와 완전히 포개졌다. 이때 [[m]], [[n]]에 대하여 [[pow(m,2) + pow(n,2)]]의 값은? "
              "(단, [[n]]은 상수)"),
    choices=["25", "26", "29", "32", "41"], derived_answer="④", figure=None, difficulty_est=3,
    note="2(x+1)²+3+m=2x²+4x+5+m → n=4, m=4 → 32 → ④. 빠른정답 3과 불일치.")

# p72
add(id="0d97a1ed", qtype="choice",
    question=("[[x = -4]]에서 최솟값 7을 갖는 이차함수의 그래프를 [[x]]축의 방향으로 2만큼, [[y]]축의 방향으로 [[m]]만큼 평행이동하였더니 "
              "이차함수 [[y = 2 pow(x,2) + n x + 12]]의 그래프와 완전히 포개졌다. 이때 [[m]], [[n]]에 대하여 [[pow(m,2) + pow(n,2)]]의 값은?"),
    choices=["41", "58", "65", "68", "73"], derived_answer="⑤", figure=None, difficulty_est=3,
    note="2(x+2)²+7+m=2x²+8x+15+m → n=8, m=−3 → 73 → ⑤ = 빠른정답 ✓.")

# p84
add(id="a51b7a28", qtype="short",
    question=("이차함수 [[f(x) = 2 pow(x,2) - 4 a x - pow(a,2) - 6a + 3]]의 최솟값을 [[g(a)]]라 할 때, [[g(a)]]의 최댓값을 구하시오.\n"
              "(단, [[a]]는 상수이다.)"),
    choices=None, derived_answer="6", figure=None, difficulty_est=3,
    note="g(a)=−3a²−6a+3=−3(a+1)²+6 → 6. 빠른정답 2와 불일치.")

# p85
add(id="3b0af5f9", qtype="short",
    question=("이차함수 [[y = pow(x,2) - 2 a x + 4a - 4]]의 최솟값을 [[m]]이라 할 때, [[m]]의 최댓값을 구하시오. (단, [[a]]는 실수이다.)"),
    choices=None, derived_answer="0", figure=None, difficulty_est=3,
    note="m=−a²+4a−4=−(a−2)² → 0. 빠른정답 5와 불일치.")

# p86
add(id="561a68ff", qtype="short",
    question=("이차함수 [[f(x) = 2 pow(x,2) - 4 a x + pow(a,2) - 6a + 3]]의 최솟값을 [[g(a)]]라 할 때, [[g(a)]]의 최댓값을 구하시오.\n"
              "(단, [[a]]는 상수이다.)"),
    choices=None, derived_answer="12", figure=None, difficulty_est=3,
    note="g(a)=−a²−6a+3=−(a+3)²+12 → 12. 빠른정답 4와 불일치.")

# p88
add(id="bc41291e", qtype="short",
    question=("이차함수 [[y = 2 pow(x,2) - 4 a x + 6a + 9]]의 최솟값을 [[m]]이라 할 때, [[m]]의 최댓값을 구하시오. (단, [[a]]는 실수이다.)"),
    choices=None, derived_answer="frac(27,2)", figure=None, difficulty_est=3,
    note="m=−2a²+6a+9=−2(a−3/2)²+27/2 → 27/2 = 빠른정답 ✓.")

# p90
add(id="710900b9", qtype="short",
    question=("이차함수 [[y = pow(x,2) + 2 a x - pow(a,2) + 12a - 10]]의 최솟값을 [[f(a)]]라 할 때, [[f(a)]]의 최댓값을 구하시오. (단, [[a]]는 실수)"),
    choices=None, derived_answer="8", figure=None, difficulty_est=3,
    note="f(a)=−2a²+12a−10=−2(a−3)²+8 → 8 = 빠른정답 ✓.")

# p91
add(id="89c33297", qtype="short",
    question=("이차함수 [[y = -pow(x,2) - 2 a x + 4a - 4]]의 최댓값을 [[M]]이라 할 때, [[M]]의 최솟값을 구하시오. (단, [[a]]는 실수이다.)"),
    choices=None, derived_answer="-8", figure=None, difficulty_est=3,
    note="M=a²+4a−4=(a+2)²−8 → −8 = 빠른정답 ✓.")

# p96
add(id="f8538d7e", qtype="short",
    question=("이차함수 [[y = pow(x,2) - 2 a x + 2a - 1]]의 최솟값을 [[m]]이라 할 때, [[m]]의 최댓값을 구하시오. (단, [[a]]는 실수이다.)"),
    choices=None, derived_answer="0", figure=None, difficulty_est=3,
    note="m=−a²+2a−1=−(a−1)² → 0. 빠른정답 −22와 불일치.")

# p98
add(id="5e2aee76", qtype="short",
    question=("이차함수 [[y = -pow(x,2) - 4 k x + 16k]]의 최댓값을 [[M]]이라 할 때, [[M]]의 값이 최소가 되도록 하는 상수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="-2", figure=None, difficulty_est=3,
    note="M=4k²+16k=4(k+2)²−16 → k=−2. 빠른정답 0과 불일치.")

# p99 — 이미지에 별개 문항 2개, id 2개 (draft 대응: 50e59ede=위 8k, 546d0344=아래 12k)
add(id="50e59ede", qtype="short",
    question=("이차함수 [[y = -pow(x,2) - 2 k x + 8k]]의 최댓값을 [[M]]이라 할 때, [[M]]의 값이 최소가 되도록 하는 상수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="-4", figure=None, difficulty_est=3, confidence=0.85,
    note="이미지 위쪽 문항. M=k²+8k=(k+4)²−16 → k=−4. 빠른정답 0과 불일치.")
add(id="546d0344", qtype="short",
    question=("이차함수 [[y = -pow(x,2) - 2 k x + 12k]]의 최댓값을 [[M]]이라 할 때, [[M]]의 값이 최소가 되도록 하는 상수 [[k]]의 값을 구하시오."),
    choices=None, derived_answer="-6", figure=None, difficulty_est=3, confidence=0.85,
    note="이미지 아래쪽 문항. M=k²+12k=(k+6)²−36 → k=−6. 빠른정답 0과 불일치.")

# ======================= 곱셈 공식 =======================
# p1
add(id="70dfb9da", qtype="choice",
    question="[[pow(3x + 2a, 2) = 9 pow(x,2) + b x + 16]]일 때, [[a b]]의 값은?",
    choices=["24", "30", "36", "42", "48"], derived_answer="⑤", figure=None, difficulty_est=2,
    note="4a²=16, b=12a → ab=12a²=48 → ⑤ = 빠른정답 ✓.")

# p3
add(id="c615e3c3", qtype="short",
    question="[[pow(7x + A, 2) = 49 pow(x,2) + B x + 9]]일 때, 양수 [[A]], [[B]]에 대하여 [[A + B]]의 값을 구하시오.",
    choices=None, derived_answer="45", figure=None, difficulty_est=2,
    note="A=3, B=42 → 45 = 빠른정답 ✓.")

# p5
add(id="64de6736", qtype="short",
    question=("[[pow(2 a x + 3b, 2)]]을 전개한 식에서 [[pow(x,2)]]의 계수가 16, 상수항이 16일 때, [[x]]의 계수를 구하시오. "
              "(단, [[a]], [[b]]는 양수이다.)"),
    choices=None, derived_answer="32", figure=None, difficulty_est=2,
    note="4a²=16 → a=2, 9b²=16 → b=4/3 → x계수 12ab=32. 빠른정답 49와 불일치.")

# p7
add(id="263fea5c", qtype="short",
    question=("자연수 [[n]]에 대하여\n[[f(n)]] = ([[3 pow(n,2)]]을 4로 나누었을 때의 나머지)라 하고\n"
              "[[n]]이 홀수일 때, [[f(n)]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=2,
    note="n=2k+1 → 3n²=12k²+12k+3 → 나머지 3 = 빠른정답 ✓. 함수 정의는 한글 텍스트 혼합.")

# p8
add(id="217db5ad", qtype="short",
    question=("자연수 [[n]]에 대하여\n[[f(n)]] = ([[pow(n,2)]]을 4로 나누었을 때의 나머지)라 할 때,\n"
              "[[f(1) + f(2) + f(3)]] + ⋯ + [[f(15)]]의 값을 구하시오."),
    choices=None, derived_answer="8", figure=None, difficulty_est=2,
    note="홀수 n → 1, 짝수 n → 0; 1~15 중 홀수 8개 → 8 = 빠른정답 ✓.")

# p11
add(id="7d471ea9", qtype="choice",
    question="다음 중 [[pow(-3 - 9x, 2)]]과 전개식이 같은 것은?",
    choices=["[[-3 pow(1 + 3x, 2)]]", "[[3 pow(1 - 3x, 2)]]", "[[9 pow(1 - 3x, 2)]]", "[[9 pow(1 + 3x, 2)]]", "[[-9 pow(1 + 3x, 2)]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="(−3−9x)²=(3+9x)²=9(1+3x)² → ④ = 빠른정답 ✓.")

# p13
add(id="891b2d28", qtype="choice",
    question="[[pow(4x - 3y, 2)]]을 전개하면 [[A pow(x,2) + B x y + C pow(y,2)]]이다. 이때\n[[A + B + C]]의 값은?",
    choices=["[[-3]]", "[[-2]]", "[[-1]]", "0", "1"], derived_answer="⑤", figure=None, difficulty_est=2,
    note="16−24+9=1 → ⑤. 빠른정답 3과 불일치.")

# p15
add(id="ff53b84f", qtype="short",
    question="[[pow(3x - A, 2) = 9 pow(x,2) - 24x + B]]일 때, [[A]], [[B]]의 합 [[A + B]]의 값을 구하여라.",
    choices=None, derived_answer="20", figure=None, difficulty_est=2,
    note="6A=24 → A=4, B=16 → 20. 빠른정답 5와 불일치.")

# p18
add(id="834937ae", qtype="choice",
    question="[[(-2x + y)(-2x - y)]]를 전개하면?",
    choices=["[[-4 pow(x,2) - pow(y,2)]]", "[[-4 pow(x,2) + 3 x y + pow(y,2)]]", "[[4 pow(x,2) + 3 x y - pow(y,2)]]",
             "[[4 pow(x,2) - pow(y,2)]]", "[[4 pow(x,2) + pow(y,2)]]"],
    derived_answer="④", figure=None, difficulty_est=1,
    note="(−2x)²−y²=4x²−y² → ④. 빠른정답 20과 불일치.")

# p19
add(id="a2dac928", qtype="short",
    question=("[[(5x + y)(y - 5x) = A pow(x,2) + B x y + C pow(y,2)]]일 때,\n"
              "상수 [[A]], [[B]], [[C]]에 대하여 [[A - B + C]]의 값을 구하시오."),
    choices=None, derived_answer="-24", figure=None, difficulty_est=2,
    note="y²−25x² → A=−25, B=0, C=1 → −24. 빠른정답 4와 불일치.")

# p41
add(id="21b17ae1", qtype="short",
    question=("[[(x + a)(x + b) = pow(x,2) + P x - 15]]일 때, [[P]]의 값이 될 수 있는 가장 작은 수를 구하시오.\n"
              "(단, [[a]], [[b]], [[P]]는 정수이다.)"),
    choices=None, derived_answer="-14", figure=None, difficulty_est=2,
    note="ab=−15, P=a+b ∈ {±14, ±2} → 최소 −14 = 빠른정답 ✓.")

# p43
add(id="6a7fc0a7", qtype="choice",
    question=("[[(3x + A)(B x - 5) = 6 pow(x,2) + C x - 20]]일 때,\n[[A + B - C]]의 값은? (단, [[A]], [[B]], [[C]]는 상수)"),
    choices=["[[-25]]", "[[-1]]", "6", "13", "27"], derived_answer="④", figure=None, difficulty_est=2,
    note="B=2, A=4, C=−15+8=−7 → 4+2+7=13 → ④. 빠른정답 −32와 불일치.")

# p66
add(id="c9329814", qtype="choice",
    question="[[(x + 1)(x + 3y + 1)]]을 전개하면?",
    choices=["[[pow(x,2) + x + 1 + x y + y]]", "[[pow(x,2) + 2x + 1 + x y + 2y]]", "[[pow(x,2) + 2x + 1 + 3 x y + 2y]]",
             "[[pow(x,2) + 2x + 1 + 3 x y + 3y]]", "[[pow(x,2) + 3x + 1 + 2 x y + 2y]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="x²+3xy+x+x+3y+1=x²+2x+1+3xy+3y → ④. 빠른정답 3과 불일치.")

# p67
add(id="5ebc2b52", qtype="choice",
    question="[[pow(2x - y + 3, 2)]]을 전개한 것은?",
    choices=["[[4 pow(x,2) - pow(y,2) + 9]]", "[[4 pow(x,2) + pow(y,2) + 9]]", "[[4 pow(x,2) - 2 x y - pow(y,2) + 6x - 3y + 9]]",
             "[[4 pow(x,2) - 2 x y + pow(y,2) + 6x - 3y + 9]]", "[[4 pow(x,2) - 4 x y + pow(y,2) + 12x - 6y + 9]]"],
    derived_answer="⑤", figure=None, difficulty_est=2,
    note="4x²+y²+9−4xy+12x−6y → ⑤ = 빠른정답 ✓.")

# p73
add(id="d787cc18", qtype="short",
    question=("[[pow(3x - y + 2, 2) = 9 pow(x,2) + a x y + pow(y,2) + 12x + b y + c]]일 때,\n"
              "상수 [[a]], [[b]], [[c]]에 대하여 [[a - b + c]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2,
    note="a=−6, b=−4, c=4 → −6+4+4=2 = 빠른정답 ✓.")

# p84 (분할 직사각형 그림)
add(id="0594613a", qtype="choice",
    question="다음 그림의 직사각형에서 색칠한 부분의 넓이는?",
    choices=["[[5 pow(a,2) - 10 a b + 2 pow(b,2)]]", "[[5 pow(a,2) - 10 a b + 4 pow(b,2)]]", "[[10 pow(a,2) + a b - 4 pow(b,2)]]",
             "[[15 pow(a,2) - 11 a b + 4 pow(b,2)]]", "[[15 pow(a,2) + 11 a b + 4 pow(b,2)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "가로 5a, 세로 3a인 직사각형. 왼쪽에서 2b 떨어진 세로선과 위에서 b 떨어진 가로선으로 4분할. 왼쪽 위(2b×b)와 오른쪽 아래((5a−2b)×(3a−b)) 두 부분 색칠"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 분할 직사각형 색칠 도형",
    note="2b²+(5a−2b)(3a−b)=15a²−11ab+4b² → ④. 빠른정답 1과 불일치.")

# p85 (정사각형 변형 그림)
add(id="5998b11a", qtype="choice",
    question=("다음 그림과 같이 한 변의 길이가 [[2a]]인 정사각형에서 세로의 길이는 [[b]]만큼 늘이고 가로의 길이는 [[b]]만큼 줄여 "
              "만든 직사각형의 넓이는?"),
    choices=["[[4 pow(a,2) - 4 a b + pow(b,2)]]", "[[4 pow(a,2) - pow(b,2)]]", "[[4 pow(a,2) + pow(b,2)]]",
             "[[4 pow(a,2) + 2 a b + pow(b,2)]]", "[[4 pow(a,2) + 4 a b + pow(b,2)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "한 변 2a인 정사각형(위·왼쪽에 2a 치수). 오른쪽 b만큼 줄이고 아래로 b만큼 늘인 직사각형(가로 2a−b, 세로 2a+b) 색칠(연두), 오른쪽 위 b·왼쪽 아래 b 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 변형 직사각형 도형",
    note="(2a−b)(2a+b)=4a²−b² → ② = 빠른정답 ✓.")

# p87 (종이 접기 그림)
add(id="febf21d5", qtype="choice",
    question=("다음 그림과 같이 가로의 길이가 [[2x]] cm, 세로의 길이가 [[3y]] cm 인 직사각형 ABCD 모양의 종이를 접어 정사각형 ABFE 와 "
              "정사각형 EGHD 를 잘라내었을 때, 남은 종이의 넓이를 [[x]], [[y]] 의 식으로 바르게 나타낸 것은?"),
    choices=["[[4 pow(x,2) + 18 x y + 18 pow(y,2)]]", "[[4 pow(x,2) - 18 x y + 18 pow(y,2)]]", "[[4 pow(x,2) - 18 x y - 18 pow(y,2)]]",
             "[[-4 pow(x,2) - 18 x y + 18 pow(y,2)]]", "[[-4 pow(x,2) + 18 x y - 18 pow(y,2)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상), 가로 2x cm·세로 3y cm 점선 치수. 정사각형 ABFE(E는 AD 위, F는 BC 위, 대각선 BE)와 정사각형 EGHD(G는 EF 위, H는 DC 위, 대각선 EH). 남은 부분 GFCH 색칠(연두)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형 접기 도형",
    note="남은 부분 (2x−3y)(6y−2x)=−4x²+18xy−18y² → ⑤ = 빠른정답 ✓.")

# p88 (종이 접기 그림)
add(id="26a04145", qtype="choice",
    question="가로의 길이가 [[a]], 세로의 길이가 [[b]]인 직사각형 모양의 종이를 다음 그림과 같이 접었을 때, 사각형 EFGH의 넓이는?",
    choices=["[[-2 pow(a,2) + 3 a b - 4 pow(b,2)]]", "[[-2 pow(a,2) + 3 a b - pow(b,2)]]", "[[-pow(a,2) + 3 a b - 2 pow(b,2)]]",
             "[[pow(a,2) - 3 a b - 2 pow(b,2)]]", "[[pow(a,2) + 3 a b + pow(b,2)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, D 우상, C 우하, B 좌하; AD=a, DC=b 점선 치수)를 A에서 45° 선 AH(H는 BC 위)로 접어 D가 B 아래 I로 옴(색칠). 다시 B에서 45° 선 BF(F는 IG 위)로 접어 E(BH 위)·F·G·H가 만드는 사각형 EFGH 색칠. B–I, I–F, D–C, H–C는 점선"}}],
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 종이 접기 도형",
    note="BH=b, BE=BI=a−b → EH=2b−a, EF=a−b → (2b−a)(a−b)=−a²+3ab−2b² → ③. 빠른정답 −96과 불일치.")

# p90 (정사각형 배열 그림)
add(id="41ea7b2b", qtype="short",
    question=("한 변의 길이가 각각 [[a]], [[b]]인 두 정사각형을 다음 그림과 같이 붙여 놓았다. [[seg(AD)]]의 중점을 B라 할 때, "
              "[[seg(AB)]], [[seg(BC)]]를 각각 한 변으로 하는 정사각형의 넓이를 각각 [[sub(S,1)]], [[sub(S,2)]]라 하자. "
              "[[sub(S,1) - sub(S,2) = 24]]일 때, [[a b]]의 값을 구하시오. (단, [[0 < b < a]])"),
    choices=None, derived_answer="24",
    figure=[{"fn": "unsupported", "args": {"raw": "밑변 위에 한 변 a인 정사각형(A~C)과 한 변 b인 작은 정사각형(C~D)이 나란히 붙어 있음. B는 AD의 중점. AB를 한 변으로 하는 정사각형 S₁(연두)과 BC를 한 변으로 하는 정사각형 S₂(하늘) 색칠. 아래에 a(A~C), b(C~D) 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사각형 배열 도형",
    note="AB=(a+b)/2, BC=(a−b)/2 → S₁−S₂=ab=24. 빠른정답 5와 불일치.")

# p94 (원 3개 그림)
add(id="7e3e9bcd", qtype="choice",
    question=("다음 그림에서 [[seg(AC)]]는 큰 원의 지름이고 나머지 원의 지름은 각각 [[seg(AB) = 2a]], [[seg(BC) = 2b]]일 때, "
              "색칠한 부분의 넓이 [[S]]를 [[a]], [[b]]에 대한 식으로 나타낸 것은?"),
    choices=["[[S = a b pi]]", "[[S = 2 a b pi]]", "[[S = 4 a b pi]]", "[[S = 8 a b pi]]", "[[S = 16 a b pi]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원(지름 AC) 안에 지름 AB=2a인 작은 원(왼쪽)과 지름 BC=2b인 원(오른쪽)이 B에서 접함. 두 작은 원 바깥의 큰 원 내부 색칠"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원 3개 도형",
    note="π(a+b)²−πa²−πb²=2abπ → ②. 빠른정답 −96과 불일치.")

# p96 (길 낸 직사각형 그림)
add(id="f58b419b", qtype="short",
    question=("다음 그림은 가로의 길이, 세로의 길이가 각각 [[5a]], [[3a]]인 직사각형 모양의 폭이 1인 길을 낸 것이다. 색칠한 부분의 "
              "넓이가 [[p pow(a,2) + q a + r]]일 때, 상수 [[p]], [[q]], [[r]]에 대하여\n[[p + q + r]]의 값을 구하시오."),
    choices=None, derived_answer="8",
    figure=[{"fn": "unsupported", "args": {"raw": "가로 5a, 세로 3a인 직사각형(점선 치수). 폭 1인 가로 길 하나와 폭 1인 세로 길 하나가 십자로 교차(오른쪽에 1, 아래에 1 표시). 길을 제외한 네 부분 색칠(연두)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 십자 길 낸 직사각형 도형",
    note="(5a−1)(3a−1)=15a²−8a+1 → p+q+r=8. 빠른정답 5와 불일치.")

# p99 — 이미지에 별개 문항 2개(위: 세 원 색칠 넓이 선택형 / 아래: 반원 arbelos 단답형), id는 1개 → 위쪽 문항 전사
add(id="f729ac0e", qtype="choice",
    question="다음 그림과 같이 세 원의 중심이 한 직선 위에 있을 때, 색칠한 부분의 넓이는?",
    choices=["[[9 pi x y]]", "[[12 pi x y]]", "[[6 pi x y + pow(y,2)]]", "[[9 pi x y + 6 pow(y,2)]]", "[[12 pi x y + 9 pow(y,2)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "큰 원 안에 반지름 2x인 원(왼쪽)과 반지름 3y인 원(오른쪽)이 내접하며 서로 외접, 세 중심이 수평 지름 위(점 표시). 두 작은 원 바깥의 큰 원 내부 색칠"}}],
    difficulty_est=2, confidence=0.75,
    needs_review=("도형 표현 불가: 원 3개 도형 / 이미지에 별개 문항 2개 인쇄(id는 1개) — 아래쪽 문항 '선분 AB를 지름으로 하는 반원, 호 AB 위의 점 P에서 내린 수선의 발 Q, "
                  "호 AQ·QB로 둘러싸인 도형의 넓이 S₁, PQ를 지름으로 하는 반원의 넓이 S₂, AQ−QB=2√57, S₁−S₂=3π일 때 AB의 길이'(답 18)는 미전사, 대상 문항 확인 필요"),
    note="위쪽: π(2x+3y)²−4πx²−9πy²=12πxy → ② = 빠른정답 2와 일치. 아래쪽: AQ=2p, QB=2q → S₁−S₂=πpq/2=3π, p−q=√57 → p+q=9 → AB=18.")

# ======================= 인수분해 공식 =======================
# p3
add(id="6475ed5b", qtype="short",
    question="다음 □ 안에 알맞은 수를 써넣으시오.\n[[pow(x,2) + 12x]] + □ = [[pow(x + 6, 2)]]",
    choices=None, derived_answer="36", figure=None, difficulty_est=1, confidence=0.85,
    note="(x+6)²=x²+12x+36 → 36 = 빠른정답 ✓. 빈칸 □는 텍스트 혼합.")

# p4
add(id="5eb85e9d", qtype="choice",
    question="[[4 pow(x,2) - A x y + 25 pow(y,2) = pow(B x - C y, 2)]]에서 세 양수 [[A]], [[B]], [[C]]의 값의 합은?",
    choices=["25", "26", "27", "28", "29"], derived_answer="③", figure=None, difficulty_est=2,
    note="B=2, C=5, A=20 → 27 → ③. 빠른정답 5와 불일치.")

# p5 (규칙 상자)
add(id="a3d370a9", qtype="choice",
    question=("다음은 왼쪽의 두 다항식으로부터 어떤 규칙에 의하여 오른쪽 다항식을 구한 것이다. □ 안의 다항식이 될 수 있는 것은?\n"
              "(가) [[pow(x,2)]], [[6x + 9]] → [[x + 3]]\n"
              "(나) [[25 pow(x,2) + 1]], [[-10x]] → [[5x - 1]]\n"
              "(다) [[-pow(x,2) - 10x + 3]], [[5 pow(x,2) + 6x - 2]] → □"),
    choices=["[[2x - 5]]", "[[2x - 3]]", "[[2x - 1]]", "[[4x - 3]]", "[[4x - 1]]"], derived_answer="③", figure=None, difficulty_est=2,
    note="두 식의 합을 인수분해한 완전제곱식의 밑: 4x²−4x+1=(2x−1)² → ③. 빠른정답 6과 불일치.")
