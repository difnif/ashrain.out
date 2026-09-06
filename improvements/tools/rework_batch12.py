# -*- coding: utf-8 -*-
# batch12 (30항목) — r2 잔여 보류 회수 라운드 (2026-09-05)
# 유형별 처리:
#   · 문자 순환소수·자릿수(11건): recdec(0, ab)/recdec(0, a0bc)/recdec(0, ab, cd), dig(a, b, c, d), 세로셈 dig(...)로 교체.
#     r2로도 불가한 첨자 순환마디 0.ȧ₁a₂⋯ȧₙ(ac9cb337), 밑줄 '(n−1)개' 순환마디(bbbb37e5), 비표준 순환점 인쇄 선지(a4ee2c72)는 텍스트 혼합 통과.
#   · 답 기호 ㉠㉡㉢(11건): derived_answer에 원문자 그대로(초안 ㄷ → ㉢ 복원).
#   · 양의 부호 답(2건): "+3000", "+23".
#   · 조건이 한글 문장인 경우 나눔(6건): 텍스트 혼합 통과(tags=["텍스트혼합"]); 6bbe9ed6은 경로 수가 그림에만 있어 figs/6bbe9ed6.png 추가.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= 문자 순환소수 · 자릿수 =================
# 0. ac9cb337 — opus_m2-1 seq 69: 순환마디가 첨자 문자열(0.ȧ₁a₂a₃⋯ȧₙ) — r2 recdec으로도 불가 → 텍스트 혼합 통과
add(id='ac9cb337', qtype='short',
    question='순환마디가 [[n]]인 순환소수 0.ȧ₁a₂a₃ ⋯ ȧₙ에 대하여 순환마디의 첫 번째 숫자를 순환마디의 마지막 자리로 옮겨 만든 순환소수 0.ȧ₂a₃a₄ ⋯ aₙȧ₁이 처음 수의 [[frac(13,3)]]배가 된다고 한다. 처음 수를 [[frac(q, p)]]라 할 때, [[p + q]]의 값을 구하시오. (단, [[1 <= i <= n]]에 대하여 [[sub(a,i)]]는 [[0 <= sub(a,i) <= 9]]인 정수, [[p]], [[q]]는 서로소인 자연수이다.)',
    choices=None, figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: 첨자·줄임표가 든 순환소수 0.ȧ₁a₂a₃⋯ȧₙ, 0.ȧ₂a₃a₄⋯aₙȧ₁ 두 곳(유니코드 결합 점, r2 recdec 범위 밖). 나머지 수식은 모두 파싱. 답 20 유지(10x−a₁=13x/3 → x=3a₁/17, 첫 자리 조건으로 a₁=1 → 3/17)')

# 1. bbbb37e5 — sonnet_h3-2_3of4 seq 52: 일반항 0.4̇00⋯00̇ 밑에 밑줄 '(n−1)개' → 텍스트 혼합 통과
add(id='bbbb37e5', qtype='choice',
    question='순환소수로 이루어진 수열 [[set(sub(a,n))]]의 각 항이\n[[sub(a,1) = recdec(0,4)]], [[sub(a,2) = recdec(0,40)]], [[sub(a,3) = recdec(0,400)]], ⋯,\n[[sub(a,n)]] = 0.4̇00⋯00̇ (0이 [[n - 1]]개), ⋯일 때, [[sum(n, 1, inf, (frac(1, sub(a, n+1)) - frac(1, sub(a,n))))]]의 값은?',
    choices=['[[0]]', '[[frac(1,4)]]', '[[frac(1,2)]]', '[[frac(3,4)]]', '[[1]]'],
    figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note="텍스트 부분: 일반항 0.4̇00⋯00̇(순환마디 안 줄임표) — 이미지의 밑줄 '(n−1)개'는 '(0이 n−1개)'로 옮김. a₁~a₃·급수는 파싱. 답 ② 유지(1/aₙ₊₁−1/aₙ=9/(4·10ⁿ) → 합 1/4)")

# 2. a4ee2c72 — sonnet_m2-1_1of4 seq 71: 선지 ②③④ 순환점이 비표준 위치(인쇄 그대로) → 텍스트 혼합 통과
add(id='a4ee2c72', qtype='choice',
    question='다음 중 순환소수의 표현이 올바른 것은?',
    choices=['[[2.333]]⋯ = [[recdec(2, 3)]]', '[[0.123123]]⋯ = 0.1̇2̇3̇', '[[15.49549549]] = 15̇.4.9̇', '[[3.4324324]]⋯ = 3̇.4̇3̇2̇', '[[1.2212212]]⋯ = [[recdec(1.2, 21)]]'],
    figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: 선지 ② 0.1̇2̇3̇, ③ 15̇.4.9̇(소수점 2개·점 위치 인쇄 그대로), ④ 3̇.4̇3̇2̇ — 비표준 순환점이라 recdec 불가, 유니코드 결합 점으로 유지. ①⑤는 recdec. 답 ① 유지(⑤는 1.22̇1̇로 틀린 표기; 빠른정답 3과 불일치는 1차와 동일)')

# 3~5. 856bb476 / 7cd9846a / 890f7408 — sonnet_m2-1_3of4 seq 15·16·17: abcd·ab → dig, 0.abċḋ → recdec(0, ab, cd)
add(id='856bb476', qtype='short',
    question='서로 다른 한 자리 자연수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[dig(a, b, c, d) = 1000a + 100b + 10c + d]]이고 [[dig(a, b) = 10a + b]]라 하자. [[frac(4315, 9900) = frac(dig(a, b, c, d) - dig(a, b), 9900) = recdec(0, ab, cd)]]일 때, [[abs(a - b + c - d)]]의 값을 구하시오.',
    choices=None, figure=None,
    confidence=0.85, needs_review=None,
    note='자릿수 나열 abcd·ab → dig(a, b, c, d)·dig(a, b), 문자 순환소수 0.abċḋ → recdec(0, ab, cd)로 전부 수식화. 답 2 유지(990a+99b+10c+d=4315 → 4358 → |4−3+5−8|=2; 빠른정답 83과 불일치는 1차와 동일)')
add(id='7cd9846a', qtype='short',
    question='서로 다른 한 자리 자연수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[dig(a, b, c, d) = 1000a + 100b + 10c + d]]이고 [[dig(a, b) = 10a + b]]라 하자. [[frac(3651, 9900) = frac(dig(a, b, c, d) - dig(a, b), 9900) = recdec(0, ab, cd)]]일 때, [[abs(a + b - c + d)]]의 값을 구하시오.',
    choices=None, figure=None,
    confidence=0.85, needs_review=None,
    note='자릿수 나열 → dig, 0.abċḋ → recdec(0, ab, cd)로 전부 수식화. 답 8 유지(990a+99b+10c+d=3651 → 3687 → |3+6−8+7|=8; 빠른정답 237과 불일치는 1차와 동일)')
add(id='890f7408', qtype='short',
    question='서로 다른 한 자리 자연수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[dig(a, b, c, d) = 1000a + 100b + 10c + d]]이고 [[dig(a, b) = 10a + b]]라 하자. [[frac(5246, 9900) = frac(dig(a, b, c, d) - dig(a, b), 9900) = recdec(0, ab, cd)]]일 때, [[abs(a - b + c + d)]]의 값을 구하시오.',
    choices=None, figure=None,
    confidence=0.85, needs_review=None,
    note='자릿수 나열 → dig, 0.abċḋ → recdec(0, ab, cd)로 전부 수식화. 답 20 유지(990a+99b+10c+d=5246 → 5298 → |5−2+9+8|=20; 빠른정답 5와 불일치는 1차와 동일)')

# 6. 2930680a — sonnet_m2-1_3of4 seq 38: 0.ȧḃ + 0.ḃȧ = 0.5̇ → recdec(0, ab) + recdec(0, ba)
add(id='2930680a', qtype='choice',
    question='한 자리 자연수 [[a]], [[b]]에 대하여 [[recdec(0, ab) + recdec(0, ba) = recdec(0, 5)]]가 성립할 때, [[a + b]]의 값은?',
    choices=['[[4]]', '[[5]]', '[[6]]', '[[7]]', '[[8]]'],
    figure=None,
    confidence=0.85, needs_review=None,
    note='문자 순환소수 0.ȧḃ, 0.ḃȧ → recdec(0, ab), recdec(0, ba)로 한 식에 수식화. 답 ② 유지(11(a+b)/99=5/9 → a+b=5; 빠른정답 ✓)')

# 7~9. 01c545d6 / 58010922 / d1756fad — sonnet_m2-1_3of4 seq 44·46·47: 0.ȧ0bċ 꼴 → recdec(0, a0bc)
add(id='01c545d6', qtype='short',
    question='[[A = recdec(0, a0bc)]], [[B = recdec(0, acb0)]]일 때, 다음 부등식을 만족시키는 [[c]]의 값을 구하시오.\n(단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.044 < B - A < 0.055]]',
    choices=None, figure=None,
    confidence=0.85, needs_review=None,
    note='문자·숫자 혼합 순환마디 0.ȧ0bċ, 0.ȧcb0̇ → recdec(0, a0bc), recdec(0, acb0). 답 5 유지(B−A=99c/9999=c/101 → 4.44<c<5.56; 빠른정답 −2와 불일치는 1차와 동일)')
add(id='58010922', qtype='short',
    question='[[A = recdec(0, ac0b)]], [[B = recdec(0, a0cb)]]일 때, 다음 부등식을 만족하는 [[c]]의 값을 구하시오.\n(단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.02 < A - B < 0.03]]',
    choices=None, figure=None,
    confidence=0.85, needs_review=None,
    note='0.ȧc0ḃ, 0.ȧ0cḃ → recdec(0, ac0b), recdec(0, a0cb). 답 3 유지(A−B=90c/9999 → 2.22<c<3.33; 빠른정답 ✓)')
add(id='d1756fad', qtype='short',
    question='[[A = recdec(0, ba0c)]], [[B = recdec(0, b0ac)]]일 때, 다음 부등식을 만족하는 [[a]]의 값을 구하시오. (단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.07 < A - B < 0.08]]',
    choices=None, figure=None,
    confidence=0.85, needs_review=None,
    note='0.ḃa0ċ, 0.ḃ0aċ → recdec(0, ba0c), recdec(0, b0ac). 답 8 유지(A−B=90a/9999 → 7.78<a<8.89; 빠른정답 5와 불일치는 1차와 동일)')

# 10. 9dba8172 — sonnet_m2-1_1of4 seq 11: 세로셈 20B5−1BA6=A39 → dig(...) 한 식; 답 새로 채움
add(id='9dba8172', qtype='short',
    question='다음 뺄셈을 만족시키는 한 자리 자연수 [[A]], [[B]]에 대하여 [[A B]]의 값을 구하시오.\n[[dig(2, 0, B, 5) - dig(1, B, A, 6) = dig(A, 3, 9)]]',
    choices=None, derived_answer='21', figure=None,
    confidence=0.8, needs_review=None,
    note="이미지의 세로셈(20B5 − 1BA6 = A39)을 dig(...) 가로식으로 전사. 답 새로 채움: 일의 자리 15−6=9, 십의 자리 B−1−A=3, 백의 자리 10−B=A → A=3, B=7(2075−1736=339 확인; 다른 해 없음). 'AB'는 문구에 '두 자리 자연수 AB'가 없어 곱 A×B로 읽어 21(두 자리 수로 읽으면 37). 빠른정답 68은 어느 해석과도 맞지 않아 정렬 오류로 봄")

# ================= 답 기호 ㉠㉡㉢ (원문자 답 허용) =================
# 11~14. 50e113ca / 0e0cc900 / be0e75ee / bd557e09 — sonnet_h1-2_2of7 seq 41: 같은 이미지에 id 4개(문항 1개) — 옳은 것은 ㉢
dup(['50e113ca', '0e0cc900', 'be0e75ee', 'bd557e09'], qtype='short',
    question='다음은 원소나열법으로 표현된 집합을 조건제시법으로 나타낸 것이다. 보기 중에서 옳은 것을 있는 대로 고르시오.\n<보기>\n㉠ {전자레인지, 전화기, 화분, 침대, 이불} = { [[x]] | [[x]]는 전자제품 }\n㉡ [[set(1, 2, 3, 4)]] = { [[x]] | [[x]]는 자연수를 4로 나누었을 때, 나머지 }\n㉢ [[set(1, 3, 5, 7, 9)]] = { [[x]] | [[x]]는 10 이하의 홀수 }\n㉣ [[set(frac(1,2), frac(1,3))]] = {0과 1 사이의 분수}',
    choices=None, derived_answer='㉢', figure=None,
    confidence=0.85, needs_review=None,
    note='원문자 답 허용으로 answer 채움: ㉠ 화분·침대·이불은 전자제품 아님, ㉡ 4로 나눈 나머지는 0~3, ㉣ 0과 1 사이의 분수는 무수히 많음 → 옳은 것 ㉢뿐. 같은 이미지에 id 4개(문항 1개)라 같은 내용으로 id마다 기재. 빠른정답 없음')

# 15. ff3cd74a — sonnet_m1-1_1of3 seq 14: 교환법칙 사용 위치 ㉠; (+3)은 단항 +라 텍스트 → 텍스트 혼합 통과
add(id='ff3cd74a', qtype='short',
    question='다음 계산 과정 중 덧셈에 대한 교환법칙이 사용된 곳을 구하시오.\n[[(-1)]] + {(+3) + [[(-8)]]}\n= [[(-1)]] + {[[(-8)]] + (+3)}  ← ㉠\n= {[[(-1)]] + [[(-8)]]} + (+3)  ← ㉡\n= [[-(1 + 8)]] + (+3)  ← ㉢\n= [[(-9)]] + (+3)  ← ㉣\n= [[-6]]  ← ㉤',
    choices=None, derived_answer='㉠', figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: 양의 부호 수 (+3)(식 안 단항 +는 문법 밖)과 중괄호 { }. 음수·합은 파싱. 답 ㉠ 새로 채움(1행→2행에서 (+3)+(−8)을 (−8)+(+3)으로 바꾼 곳이 교환법칙; ㉡은 결합법칙). 빠른정답 3과 대응 불명')

# 16. e551107c — sonnet_m1-1_2of3 seq 53: 양변에 2를 곱한 곳 ㉡
add(id='e551107c', qtype='short',
    question="다음 등식의 성질을 이용하여 일차방정식 [[0.5x - 5 = frac(5,2) + 3x]]의 해를 구하는 과정이다. 이때 등식의 성질 '[[a = b]]이면 [[a c = b c]]이다.'를 이용한 곳을 고르시오. (단, [[c]]는 자연수)\n[[0.5x - 5 = frac(5,2) + 3x]]\n↓ ㉠\n[[frac(1,2) x - 5 = frac(5,2) + 3x]]\n↓ ㉡\n[[x - 10 = 5 + 6x]]\n↓ ㉢\n[[x - 6x - 10 = 5]]\n↓ ㉣\n[[-5x = 5 + 10]]\n↓ ㉤\n[[-5x = 15]]",
    choices=None, derived_answer='㉡', figure=None,
    confidence=0.85, needs_review=None,
    note='본문은 문법 안(변경 없음). 답 ㉡ 새로 채움: ½x−5=5/2+3x → x−10=5+6x가 양변에 2를 곱한 단계(㉠ 0.5→½ 변환, ㉢㉣ 이항, ㉤ 계산). 빠른정답 없음')

# 17. 1ce3008b — sonnet_m1-1_2of3 seq 54: 양변을 3으로 나눈 곳 ㉢
add(id='1ce3008b', qtype='short',
    question="다음 방정식의 풀이 과정에서 등식의 성질 '[[a = b]]이면 [[frac(a, c) = frac(b, c)]]이다.'를 이용한 곳을 고르시오. (단, [[c]]는 자연수)\n[[frac(3,7) x + 2 = 5]]\n↓㉠\n[[3x + 14 = 35]]\n↓㉡\n[[3x = 21]]\n↓㉢\n∴ [[x = 7]]",
    choices=None, derived_answer='㉢', figure=None,
    confidence=0.85, needs_review=None,
    note='본문은 문법 안(변경 없음). 답 ㉢ 새로 채움: 3x=21 → x=7이 양변을 3으로 나눈 단계(㉠ 양변×7, ㉡ 양변−14). 빠른정답 없음')

# 18. fcc0b4a7 — sonnet_m1-1_3of3 seq 75: 연산 상자의 네 등식을 텍스트·수식으로 전사, 그림은 figs/fcc0b4a7.png 추가
add(id='fcc0b4a7', qtype='short',
    question='아래 그림은 가로로 덧셈식과 곱셈식, 세로로 뺄셈식과 나눗셈식을 나타낸 것이다. 다음 식을 계산하시오.\n[[frac(2,5)]] + ㉠ = [[-2]]\n[[frac(2,5)]] − ㉡ = [[-1.8]]\n[[-2]] ÷ ㉢ = [[frac(2,3)]]\n[[-1.8]] × ㉣ = [[frac(2,3)]]\n(㉢)² − (㉠ × ㉡ + ㉠ ÷ ㉣)',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '상자 계산 그림(화살표로 방향 표시): 가로 윗줄 2/5 + ㉠ = −2, 가로 아랫줄 −1.8 × ㉣ = 2/3, 세로 왼쪽 2/5 − ㉡ = −1.8, 세로 오른쪽 −2 ÷ ㉢ = 2/3. 그 아래 상자에 (㉢)² − (㉠ × ㉡ + ㉠ ÷ ㉣)'}},
            {'fn': 'image', 'args': {'src': 'figs/fcc0b4a7.png', 'raw': '연산 상자 그림: 윗줄 2/5 [+] ㉠ [=] −2, 왼쪽 세로 2/5 [−] ㉡ [=] −1.8, 오른쪽 세로 −2 [÷] ㉢ [=] 2/3, 아랫줄 −1.8 [×] ㉣ [=] 2/3 (화살표는 왼쪽→오른쪽, 위→아래)'}}],
    tags=['텍스트혼합', '그림정보_이미지'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: 빈칸 기호 ㉠~㉣과 그 자리를 포함한 계산식 (㉢)² − (㉠ × ㉡ + ㉠ ÷ ㉣); 상자의 네 등식은 수치 조각([[frac(2,5)]] 등)만 마커. 그림 영역을 원본 해상도로 잘라 figs/fcc0b4a7.png 추가(기존 unsupported 유지). 답 39/5 유지(㉠=−12/5, ㉡=11/5, ㉢=−3, ㉣=−10/27 → 9−6/5; 빠른정답 ✓)')

# 19. 9334ad53 — sonnet_m2-1_1of4 seq 36: 함수가 아닌 것 ㉡
add(id='9334ad53', qtype='short',
    question='다음에서 [[y]] 를 [[x]] 의 함수라고 할 수 없는 것을 구하여라.\n㉠ 한 팩에 1000원인 우유를 [[x]] 팩 살 때 지불 금액 [[y]] 원\n㉡ 자연수 [[x]] 와 그 배수 [[y]]\n㉢ 넓이가 20cm² 인 삼각형의 밑변의 길이 [[x]]cm 와 높이 [[y]]cm',
    choices=None, derived_answer='㉡', figure=None,
    confidence=0.85, needs_review=None,
    note='본문은 문법 안(변경 없음). 답 ㉡ 새로 채움: 자연수 x의 배수 y는 하나로 정해지지 않음(㉠ y=1000x, ㉢ y=40/x는 함수). 빠른정답 3, 4와 대응 불명')

# 20. c670c281 — sonnet_m2-2_4of5 seq 42: 옳지 않은 것 ㉢(ASA → SAS) — 초안 ㄷ을 이미지대로 ㉢으로 복원
add(id='c670c281', qtype='short',
    question="다음은 '두 대각선이 서로 다른 것을 이등분하면 평행사변형이 된다.'를 증명하는 과정이다. ㉠~㉤ 중 옳지 않은 것을 고르시오.\n[가정] [[quad(ABCD)]]에서 [[seg(OA) = seg(OC)]], [[seg(OB) = seg(OD)]]\n[결론] [[par(seg(AB), seg(CD))]], [[par(seg(AD), seg(BC))]]\n[증명] [[tri(OAB)]]와 [[tri(OCD)]]에서\n㉠ [[seg(OA) = seg(OC)]], [[seg(OB) = seg(OD)]]\n[[angle(AOB) = angle(COD)]] (㉡ 맞꼭지각)\n따라서 [[cong(tri(OAB), tri(OCD))]] (㉢ ASA 합동)\n[[angle(OAB) = angle(OCD)]]\n㉣ ∴ [[par(seg(AB), seg(CD))]] ⋯ ①\n같은 방법으로 [[cong(tri(OAD), tri(OCB))]]이므로\n㉤ [[angle(OAD) = angle(OCB)]]\n∴ [[par(seg(AD), seg(BC))]] ⋯ ②\n①, ②에 의하여 [[quad(ABCD)]]는 평행사변형이다.",
    choices=None, derived_answer='㉢',
    figure=[{'fn': 'unsupported', 'args': {'raw': '평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC·BD의 교점 O'}}],
    confidence=0.85, needs_review=None,
    note='답을 초안의 ㄷ에서 이미지 기호 ㉢으로 복원(두 변과 그 끼인각이 같으므로 SAS 합동이어야 함 → ㉢ ASA 합동이 옳지 않음). 본문은 문법 안. 빠른정답 20과 불일치는 1차와 동일')

# 21. 3b755ae4 — sonnet_m3-1_4of6 seq 2: 처음 틀린 곳 ㉢
add(id='3b755ae4', qtype='short',
    question='[[y = 2 pow(x,2) + 4x - 1]]을 [[y = a pow(x - p, 2) + q]]의 꼴로 고치는 과정 중 처음 틀린 곳을 찾으시오.\n[[y = 2 pow(x,2) + 4x - 1]]\n= [[2(pow(x,2) + 2x) - 1]] ⋯㉠\n= [[2(pow(x,2) + 2x + 1 - 1) - 1]] ⋯㉡\n= [[2 pow(x + 1, 2) - 3 - 1]] ⋯㉢\n= [[2 pow(x + 1, 2) - 4]] ⋯㉣',
    choices=None, derived_answer='㉢', figure=None,
    confidence=0.85, needs_review=None,
    note='본문은 문법 안(변경 없음). 답 ㉢ 새로 채움: 2(x²+2x+1−1)−1 = 2(x+1)²−2−1이어야 하는데 −3−1로 씀. 빠른정답 5와 대응 불명')

# ================= 양의 부호 답 =================
# 22. fe5c4e92 — sonnet_m1-1_2of3 seq 14: 답 +3000
add(id='fe5c4e92', qtype='short',
    question='다음 수를 양의 부호 + 또는 음의 부호 −를 사용하여 나타냈을 때, □ 안에 알맞은 수를 써넣으시오.\n[[3000]]원 입금 ⇨ □원',
    choices=None, derived_answer='+3000', figure=None,
    confidence=0.85, needs_review=None,
    note='양의 부호 답 허용으로 답을 +3000(입금 → 양의 부호)으로 기재. 빈칸 □은 원문에 (가) 표기가 없어 텍스트 유지. 빠른정답 3과 불일치는 1차와 동일')

# 23. a21f762f — sonnet_m1-1_2of3 seq 46: 답 +23
add(id='a21f762f', qtype='short',
    question='0보다 23만큼 큰 수를 부호 +또는 −를 사용하여 나타내시오.',
    choices=None, derived_answer='+23', figure=None,
    confidence=0.85, needs_review=None,
    note="양의 부호 답 허용으로 답을 +23으로 기재(빠른정답 'add 23'과 같은 취지)")

# ================= 조건이 한글 문장인 경우 나눔 → 텍스트 혼합 통과 =================
# 24. 6bbe9ed6 — sonnet_h1-1_2of4 seq 74: 성분 정의의 식이 한글(경로의 수); 경로 수는 그림에만 → figs/6bbe9ed6.png 추가
add(id='6bbe9ed6', qtype='short',
    question='세 공원 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]을 연결하는 산책로가 다음 그림과 같다. 행렬 [[A]]의 [[point(i, j)]] 성분 [[sub(a,i,j)]]가\n[[sub(a,i,j)]] = { (공원 [[sub(P,i)]]에서 공원 [[sub(P,j)]]로 가는 경로의 수) ([[i != j]]), [[0]] ([[i = j]]) }\n일 때, 행렬 [[A]]의 모든 성분의 합을 구하시오.\n(단, [[i]] = 1, 2, 3, [[j]] = 1, 2, 3)',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '세 공원 P₁, P₂, P₃ 삽화가 가로로 놓이고 P₁–P₂ 사이에 산책로 3개(위 곡선·가운데 직선·아래 곡선), P₂–P₃ 사이에 산책로 3개가 그려져 있음(P₁–P₃ 직접 연결 없음)'}},
            {'fn': 'image', 'args': {'src': 'figs/6bbe9ed6.png', 'raw': '세 공원 P₁, P₂, P₃ 삽화: P₁–P₂ 사이 산책로 3개, P₂–P₃ 사이 산책로 3개(P₁–P₃ 직접 연결 없음)'}}],
    tags=['텍스트혼합', '그림정보_이미지'],
    confidence=0.8, needs_review=None,
    note='텍스트 부분: 경우 나눔의 첫 식이 한글 문장(공원 Pᵢ에서 Pⱼ로 가는 경로의 수)이라 cases 불가 → { … (i ≠ j), 0 (i = j) } 텍스트 혼합. 경로 수는 그림에만 있어 그림 영역을 원본 해상도로 잘라 figs/6bbe9ed6.png 추가. 답 30 유지(a₁₂=a₂₁=a₂₃=a₃₂=3, a₁₃=a₃₁=9; 빠른정답 45와 불일치는 1차와 동일)')

# 25~26. 8930c983 / d149ceed — sonnet_h1-2_4of7 seq 47·48: f(p, q) 정의의 조건이 한글(p→q가 참/거짓)
add(id='8930c983', qtype='short',
    question='두 조건 [[p]], [[q]]에 대하여 [[f(p, q)]]를 다음과 같이 정의하자.\n[[f(p, q)]] = { [[1]] ([[imp(p, q)]]가 참), [[-1]] ([[imp(p, q)]]가 거짓) }\n실수 전체의 집합에서 정의된 세 조건 [[p]], [[q]], [[r]]가 다음과\n같을 때, [[f(p, neg(q)) + 2 × f(q, r) + 3 × f(neg(r), p)]]의\n값을 구하시오.\n[[p]]: [[x]]는 4의 배수가 아니다.\n[[q]]: [[pow(x,2)]]은 4의 배수가 아니다.\n[[r]]: [[sqrt(x)]] 는 4의 배수가 아니다.',
    choices=None, figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: f(p, q)의 경우 나눔 조건 (p→q가 참)/(p→q가 거짓)이 한글 문장이라 cases 불가 → { 1 (…), −1 (…) } 텍스트 혼합; 조건 p, q, r의 한글 서술. 답 −2 유지(f(p,~q)=−1, f(q,r)=1, f(~r,p)=−1 → −1+2−3; 빠른정답 ✓)')
add(id='d149ceed', qtype='short',
    question='두 조건 [[p]], [[q]]에 대하여 [[f(p, q)]]를 다음과 같이 정의하자.\n[[f(p, q)]] = { [[1]] ([[imp(p, q)]]가 참), [[-1]] ([[imp(p, q)]]가 거짓) }\n실수 전체의 집합에서 정의된 세 조건 [[p]], [[q]], [[r]]가 다음과\n같을 때, [[f(p, neg(q)) + 2 × f(neg(q), neg(r)) + 3 × f(r, p)]]의\n값을 구하시오.\n[[p]]: [[x]]는 3의 배수이다.\n[[q]]: [[pow(x,3)]]은 3의 배수이다.\n[[r]]: [[sqrt(x)]] 는 3의 배수이다.',
    choices=None, figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: f(p, q)의 경우 나눔 조건(p→q가 참/거짓)이 한글 문장 → 텍스트 혼합; 조건 p, q, r의 한글 서술. 답 4 유지(f(p,~q)=−1, f(~q,~r)=1, f(r,p)=1 → −1+2+3). 빠른정답 없음')

# 27. ec33cbb7 — sonnet_h1-2_6of7 seq 63: 조건이 한글(x는 4의 배수이다/아니다)
add(id='ec33cbb7', qtype='choice',
    question='자연수 전체의 집합에서 정의된 함수 [[f(x)]]가\n[[f(x)]] = { [[frac(x, 4) + 5]] ([[x]]는 4의 배수이다.), [[x - 5]] ([[x]]는 4의 배수가 아니다.) }\n이고 [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(pow(f, n), f)]]로 정의할 때,\n[[iter(f, n, 100) = 0]]을 만족시키는 자연수 [[n]]의 값은?',
    choices=['[[2]]', '[[4]]', '[[6]]', '[[8]]', '[[10]]'],
    figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: 경우 나눔 조건 (x는 4의 배수이다.)/(x는 4의 배수가 아니다.)가 한글 문장 → { …, … } 텍스트 혼합. 거듭 합성 fⁿ(100)은 iter. 답 ③ 유지(100→30→25→20→10→5→0, n=6; 빠른정답 1과 불일치는 1차와 동일)')

# 28. 3725851e — sonnet_h1-2_6of7 seq 69: 조건이 한글(x는 무리수/유리수)
add(id='3725851e', qtype='short',
    question='양의 실수 [[x]]에 대하여 함수\n[[f(x)]] = { [[pow(x, 4)]] ([[x]]는 무리수), [[sqrt(x)]] ([[x]]는 유리수) }\n라 하자. [[pow(f, 1) = f]], [[pow(f, n + 1) = comp(f, pow(f, n))]] ([[n]]은 자연수)라 할 때,\n[[iter(f, 3n - 2, 1) + iter(f, 3n - 1, sqrt(2)) + iter(f, 3n, 3)]]의 값을 구하시오.',
    choices=None, figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: 경우 나눔 조건 (x는 무리수)/(x는 유리수)가 한글 문장 → 텍스트 혼합. 거듭 합성은 iter. 답 6 유지(fᵏ(1)=1, √2→4→2 주기 3이라 f^(3n−1)(√2)=2, 3→√3→9→3이라 f^(3n)(3)=3; 빠른정답 1과 불일치는 1차와 동일)')

# 29. 6b57a62e — sonnet_h2-1_3of4 seq 29: 조건이 한글(n이 홀수/짝수) — [2019년 6월 고2 이과 21번/4점]
add(id='6b57a62e', qtype='choice',
    question='자연수 [[n]]에 대하여 [[f(n)]]이 다음과 같다.\n[[f(n)]] = { [[root(4, 9 × pow(2, n+1))]] ([[n]]이 홀수), [[root(4, 4 × pow(3, n))]] ([[n]]이 짝수) }\n10 이하의 두 자연수 [[p]], [[q]]에 대하여 [[f(p) × f(q)]]가 자연수가 되도록 하는 모든 순서쌍 [[point(p, q)]]의 개수는?',
    choices=['[[36]]', '[[38]]', '[[40]]', '[[42]]', '[[44]]'],
    figure=None, tags=['텍스트혼합'],
    confidence=0.85, needs_review=None,
    note='텍스트 부분: 경우 나눔 조건 (n이 홀수)/(n이 짝수)가 한글 문장 → 텍스트 혼합. 출처 머리말 [2019년 6월 고2 이과 21번/4점]. 답 ⑤ 유지(전수 확인 44). 빠른정답 없음')
