# -*- coding: utf-8 -*-
# esc_sonnet_m1-1_1of3 — 이미지 기준 전사 (91 항목 / 80쪽)
# 규약: 양의 부호가 붙은 수 (+a)는 mathir에 단항 +가 없어 텍스트 혼합 "(+[[frac(a,b)]])" / "(+3)"으로 적음.
#       약속 연산 기호(△, ▲, ◎, ★ …)와 빈칸 □, 원문자 ㉠~㉤은 마커 밖 텍스트.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= 최대공약수와 최소공배수의 관계 =================
# p27
add(id="fb782cd1", qtype="short",
    question=("두 자연수 [[A]], [[B]]의 최대공약수를 [[A]] • [[B]]로, 최소공배수는 [[A]]△[[B]]로 나타낼 때, "
              "다음 조건을 모두 만족시키는 두 자연수 [[x]], [[y]]의 합 [[x + y]]의 값을 구하시오.\n"
              "(가) [[x]]는 [[A]] • 30 = 5를 만족시키는 자연수 [[A]] 중 두 번째로 작은 수이다.\n"
              "(나) [[y]]는 [[B]]△9 = 45를 만족시키는 자연수 [[B]] 중 두 번째로 작은 수이다."),
    choices=None, derived_answer="40", figure=None, difficulty_est=3, confidence=0.85,
    note="gcd(A,30)=5인 A=5,25,35,… → x=25; lcm(B,9)=45인 B=5,15,45 → y=15; x+y=40. 빠른정답 21과 불일치. 약속 기호 •, △는 텍스트.")

# ================= 유리수의 덧셈과 뺄셈 =================
# p11
add(id="b6863f42", qtype="short",
    question=("[[a]] = (+[[frac(11,6)]]) + [[(-frac(5,4))]], [[b]] = [[(-13)]] + (+8)일 때,\n[[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="-frac(53,12)", figure=None, difficulty_est=2, confidence=0.85,
    note="a=22/12−15/12=7/12, b=−5 → a+b=−53/12. 빠른정답 53/12(부호 없음)과 불일치. 양의 부호 (+a)는 문법 미지원이라 텍스트 혼합.")

# p14 (교환법칙 위치 ㉠~㉤)
add(id="ff3cd74a", qtype="short",
    question=("다음 계산 과정 중 덧셈에 대한 교환법칙이 사용된 곳을 구하시오.\n"
              "[[(-1)]] + {(+3) + [[(-8)]]}\n"
              "= [[(-1)]] + {[[(-8)]] + (+3)}  ← ㉠\n"
              "= {[[(-1)]] + [[(-8)]]} + (+3)  ← ㉡\n"
              "= [[-(1 + 8)]] + (+3)  ← ㉢\n"
              "= [[(-9)]] + (+3)  ← ㉣\n"
              "= [[-6]]  ← ㉤"),
    choices=None, derived_answer=None, figure=None, difficulty_est=1, confidence=0.75,
    needs_review="답 표기 문법 범위 밖: 정답은 원문자 ㉠(1행→2행, (+3)+(−8)의 순서 교환)인데 ㉠은 답 허용 문자가 아님",
    note="㉠~㉤은 연속한 두 행 사이의 변형 단계를 가리키는 화살표 표시. 교환법칙은 ㉠. 빠른정답 3과 대응 불명. 양의 부호 (+3)은 텍스트 혼합.")

# p15 (결합법칙 위치 ①~⑤)
add(id="3721beeb", qtype="choice",
    question=("다음 계산 과정에서 덧셈에 대한 결합법칙이 이용된 곳은?\n"
              "[[(-frac(1,6))]] + (+0.4) + [[(-frac(5,6))]]\n"
              "= [[(-frac(1,6))]] + (+[[frac(2,5)]]) + [[(-frac(5,6))]]  ← ①\n"
              "= [[(-frac(1,6))]] + [[(-frac(5,6))]] + (+[[frac(2,5)]])  ← ②\n"
              "= {[[(-frac(1,6))]] + [[(-frac(5,6))]]} + (+[[frac(2,5)]])  ← ③\n"
              "= [[(-1)]] + (+[[frac(2,5)]])  ← ④\n"
              "= [[-frac(3,5)]]  ← ⑤"),
    choices=["①", "②", "③", "④", "⑤"], derived_answer="③", figure=None, difficulty_est=1, confidence=0.85,
    note="①~⑤는 연속한 두 행 사이의 변형 단계 화살표(선지 본문 없음 → 기호 자체를 선지로). 3→4행의 중괄호 묶기가 결합법칙 → ③ = 빠른정답 ✓. 양의 부호 (+a)는 텍스트 혼합.")

# p22
add(id="cd60a16f", qtype="short",
    question="덧셈의 계산법칙을 이용하여 (+2) + [[(-4)]] + (+7)을 계산하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=1, confidence=0.85,
    note="2−4+7=5 (빠른정답 없음). 양의 부호 (+a)는 텍스트 혼합.")

# p30
add(id="2eb59a59", qtype="short",
    question="(+3) − [[(-8)]]을 계산하시오.",
    choices=None, derived_answer="11", figure=None, difficulty_est=1, confidence=0.85,
    note="3+8=11 = 빠른정답 ✓. 양의 부호 (+3)은 텍스트 혼합.")

# p39
add(id="8fd376dc", qtype="short",
    question="[[(-9) - (-5)]] + (+7)을 계산하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.85,
    note="−9+5+7=3 = 빠른정답 ✓. 양의 부호 (+7)은 텍스트 혼합.")

# p44
add(id="34accb2b", qtype="choice",
    question="다음 중 계산 결과가 옳지 않은 것은?",
    choices=["(+7.6) + [[(-5)]] − [[(-2)]] − (+2.6) = +2",
             "[[(-4.3)]] − (+4) + [[(-9)]] − [[(-4.3)]] = [[-13]]",
             "(+[[frac(2,5)]]) − [[(-frac(1,4))]] + [[(-frac(1,5))]] = +[[frac(7,20)]]",
             "[[(-frac(3,4))]] − (+[[frac(1,4)]]) + [[(-frac(5,4))]] = [[-frac(9,4)]]",
             "[[(-frac(1,2))]] + [[(-frac(1,3))]] − [[(-2)]] = +[[frac(7,6)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="③ 2/5+1/4−1/5=9/20≠7/20 → ③ = 빠른정답 ✓ (①2 ②−13 ④−9/4 ⑤7/6 모두 옳음). 양의 부호 (+a)는 텍스트 혼합.")

# p48
add(id="e5a5873f", qtype="short",
    question=("다음 식의 ㉠, ㉡, ㉢에 세 수 [[-frac(1,2)]], [[frac(1,6)]], [[frac(1,12)]]을 한 번씩 넣어 계산한 결과 중 가장 작은 값을 구하시오.\n"
              "㉠ + ㉡ − ㉢"),
    choices=None, derived_answer="frac(-7,12)", figure=None, difficulty_est=2, confidence=0.9,
    note="㉢에 가장 큰 1/6 → −1/2+1/12−1/6=−7/12 = 빠른정답 ✓. ㉠㉡㉢ 빈칸 상자는 텍스트(도형 아님).")

# ================= 사분면 =================
# p10
add(id="c78b5486", qtype="short",
    question=("두 점 [[A(-2a + 6, a - 3b)]], [[B(2 - b, 4a + 3)]]이 각각 [[x]]축, [[y]]축 위에 있고, "
              "점 [[C(5 + c, 2 pow(b,2) - 2)]]는 어느 사분면에도 속하지 않는다. 이때 점 [[P(a, b c)]]는 어느 사분면 위에 있는지 구하시오."),
    choices=None, derived_answer="제4사분면", figure=None, difficulty_est=3, confidence=0.9,
    note="a−3b=0, 2−b=0 → b=2, a=6; C(5+c, 6)이 축 위 → c=−5; P(6, −10) → 제4사분면 (빠른정답 없음).")

# p11
add(id="a0f65d9c", qtype="short",
    question=("두 점 [[A(5 - a - b, 3a - 6)]], [[B(3b - 9, 3a + 6)]]가 각각 [[y]]축, [[x]]축 위에 있고, "
              "점 [[C(6 - 2c, pow(b,2) - a)]]는 어느 사분면에도 속하지 않는다. 이때 점 [[P(a c, b)]]는 어느 사분면 위에 있는지 구하시오."),
    choices=None, derived_answer="제2사분면", figure=None, difficulty_est=3, confidence=0.9,
    note="5−a−b=0, 3a+6=0 → a=−2, b=7; C(6−2c, 51) → c=3; P(−6, 7) → 제2사분면 (빠른정답 없음).")

# p26
add(id="fe141d81", qtype="short",
    question="점 [[point(a + b, frac(a, b))]]가 제2사분면 위의 점일 때,\n점 [[point(-a, a + b)]]는 제몇 사분면 위의 점인지 구하시오.",
    choices=None, derived_answer="제4사분면", figure=None, difficulty_est=2, confidence=0.9,
    note="a+b<0, a/b>0 → a<0, b<0 → (−a, a+b)=(+, −) → 제4사분면 (빠른정답 없음).")

# p27
add(id="dfd10fea", qtype="short",
    question="점 [[point(a + b, a b)]]가 제1사분면 위의 점일 때,\n점 [[point(-a, -frac(a, b))]]는 제몇 사분면 위의 점인지 구하시오.",
    choices=None, derived_answer="제3사분면", figure=None, difficulty_est=2, confidence=0.9,
    note="a+b>0, ab>0 → a>0, b>0 → (−a, −a/b)=(−, −) → 제3사분면. 빠른정답 '3'과 표기만 다름.")

# p28
add(id="52b83ded", qtype="choice",
    question="점 [[point(-a b, a - b)]]가 제1사분면 위에 있을 때, 다음 중 점의 좌표와 그 점이 속하는 사분면을 바르게 짝지은 것은?",
    choices=["[[point(a, b)]] ⇨ 제2사분면",
             "[[point(-a, b)]] ⇨ 제4사분면",
             "[[point(a - b, b - 3a)]] ⇨ 제3사분면",
             "[[point(pow(b,2) - a b, pow(a,2) - a b)]] ⇨ 제1사분면",
             "[[point(frac(-b, a - b), frac(b - a, a b))]] ⇨ 제2사분면"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="ab<0, a>b → a>0, b<0. ①제4 ②제3 ③제4 ④(+,+) 제1 ✓ ⑤(+,+) 제1 → ④. 빠른정답 '- 4'는 4의 부호 오기로 보임.")

# p30
add(id="3f9dc52e", qtype="short",
    question="점 [[point(-a + b, -a b)]]가 제2사분면 위의 점일 때,\n점 [[point(-a, a b)]]는 제몇 사분면 위의 점인지 구하시오.",
    choices=None, derived_answer="제3사분면", figure=None, difficulty_est=2, confidence=0.9,
    note="−a+b<0, −ab>0 → a>0, b<0 → (−a, ab)=(−, −) → 제3사분면 (빠른정답 없음).")

# p32 (한 이미지·문항 1개에 id 3개)
dup(["7c9ee5c6", "2214a67c", "870c0eea"], qtype="short",
    question=("점 [[point(a b d, b + c)]]가 제4사분면 위의 점이고\n점 [[point(a c d, a - d)]]가 제1사분면 위의 점일 때,\n"
              "점 [[point(a b, b c)]]는 제몇 사분면 위의 점인지 구하시오."),
    choices=None, derived_answer="제2사분면", figure=None, difficulty_est=3, confidence=0.85,
    note="abd>0, acd>0 → bc>0; b+c<0 → b,c<0; abd>0 → ad<0, a>d → a>0, d<0 → (ab, bc)=(−, +) → 제2사분면. 빠른정답 5와 불일치. 같은 이미지 id 3개 동일 전사.")

# p34
add(id="e2bc8816", qtype="short",
    question=("점 [[point(a b c, b + c)]]가 제3사분면 위의 점이고,\n점 [[point(a c d, d - a)]]가 제2사분면 위의 점일 때,\n"
              "점 [[point(a b, b d)]]는 제몇 사분면 위의 점인지 구하시오."),
    choices=None, derived_answer="제1사분면", figure=None, difficulty_est=3, confidence=0.85,
    note="abc<0, acd<0 → bd>0; 두 경우(b,d>0 → c<0,a>0 / b,d<0 → a<0) 모두 ab>0 → (+, +) → 제1사분면 (빠른정답 없음).")

# p52
add(id="ae689670", qtype="short",
    question="[[a > 0]], [[b > 0]]일 때, [[point(-a, b)]]는 어느 사분면 위에 있는지 구하시오.",
    choices=None, derived_answer="제2사분면", figure=None, difficulty_est=1, confidence=0.9,
    note="(−, +) → 제2사분면 (빠른정답 없음).")

# p62
add(id="e3609aeb", qtype="choice",
    question="[[a b < 0]], [[a < b]]일 때, 점 [[point(frac(a, b), b - a)]]와 같은 사분면 위의 점은?",
    choices=["[[point(-3, -2)]]", "[[point(2, 1)]]", "[[point(-1, 2)]]", "[[point(-1, -1)]]", "[[point(2, 0)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="a/b<0, b−a>0 → 제2사분면 → ③ (−1, 2) (빠른정답 없음).")

# p63
add(id="1b5f35a2", qtype="choice",
    question="[[a b < 0]], [[a < b]]일 때, 점 [[point(frac(b, a), b)]]와 같은 사분면 위의 점은?",
    choices=["[[point(3, 2)]]", "[[point(2, -4)]]", "[[point(-1, -2)]]", "[[point(-3, 4)]]", "[[point(2, 0)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a<0<b → b/a<0, b>0 → 제2사분면 → ④ (−3, 4). 빠른정답 1과 불일치.")

# p64
add(id="e1cd5ae2", qtype="short",
    question="[[-a - b > 0]], [[a b > 0]]일 때, 점 [[point(a, b)]]는 어느 사분면 위에 있는지 구하시오.",
    choices=None, derived_answer="제3사분면", figure=None, difficulty_est=2, confidence=0.9,
    note="a+b<0, ab>0 → a<0, b<0 → 제3사분면. 빠른정답 1과 불일치.")

# p67
add(id="57ed0170", qtype="choice",
    question="[[x y > 0]], [[x + y < 0]]일 때, 다음 중 점 [[point(-x, y)]]와 같은 사분면 위의 점은?",
    choices=["[[point(3, 4)]]", "[[point(7, 0)]]", "[[point(-2, -7)]]", "[[point(-2, 5)]]", "[[point(7, -2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="x<0, y<0 → (−x, y)=(+, −) 제4사분면 → ⑤ (7, −2) = 빠른정답 ✓.")

# p69
add(id="b7a8ec29", qtype="short",
    question="[[a + b < 0]], [[a b > 0]]일 때, 점 [[point(a, -b)]]는 어느 사분면 위에 있는지 구하시오.",
    choices=None, derived_answer="제2사분면", figure=None, difficulty_est=2, confidence=0.9,
    note="a<0, b<0 → (a, −b)=(−, +) → 제2사분면 (빠른정답 없음).")

# p70
add(id="5e422e35", qtype="choice",
    question="[[a b < 0]], [[b - a > 0]], [[abs(a) < abs(b)]]일 때,\n점 [[A(a + b, 2a - b)]]는 제 몇 사분면 위에 있는가?",
    choices=["제1사분면", "제2사분면", "제3사분면", "제4사분면", "어느 사분면에도 속하지 않는다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a<0<b, |a|<|b| → a+b>0, 2a−b<0 → 제4사분면 → ④ = 빠른정답 ✓.")

# p91
add(id="dd4a5c53", qtype="short",
    question=("점 [[A(-2, -3)]]과 [[x]]축, [[y]]축, 원점에 대하여 대칭인 점을 각각 B, C, D라 할 때, "
              "네 점 A, B, C, D를 꼭짓점으로 하는 직사각형 ACDB의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="20", figure=None, difficulty_est=2, confidence=0.9,
    note="B(−2,3), C(2,−3), D(2,3) → 가로 4, 세로 6 → 둘레 20. 빠른정답 3과 불일치.")

# ================= 식의 값 =================
# p26
add(id="20703ed4", qtype="short",
    question="[[x = 4]], [[y = -1]]일 때, [[pow(x,2) + 6x y]]의 값을 구하시오.",
    choices=None, derived_answer="-8", figure=None, difficulty_est=1, confidence=0.9,
    note="16−24=−8. 빠른정답 4와 불일치(다음 문항 p29 빠른정답이 −8로, 목록이 한 칸 어긋난 듯).")

# p29
add(id="5ec548a0", qtype="choice",
    question="[[a = 2]], [[b = -3]], [[c = -1]]일 때, [[frac(3a, b) - frac(a b - b c, b)]]의 값은?",
    choices=["[[-5]]", "[[-frac(11,3)]]", "[[-2]]", "[[-frac(1,3)]]", "[[0]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="3a/b=−2, (ab−bc)/b=(−6−3)/(−3)=3 → −2−3=−5 → ①. 빠른정답 −8과 불일치(목록 어긋남 추정).")

# p32
add(id="562c6cf0", qtype="choice",
    question=("[[x = -7]], [[y = -1]]일 때,\n"
              "[[-frac(-7 pow(y,n), x) + frac(-pow(7,2) pow(y,2n), pow(x,2)) - frac(-pow(7,3) pow(y,n+1), pow(x,3))]]의 값은?\n"
              "(단, [[n]]은 자연수이다.)"),
    choices=["[[-3]]", "[[-1]]", "[[1]]", "[[3]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="원문 '−7²'는 −(7²)로 읽음. 항별로 −yⁿ, −1, −yⁿ⁺¹ → −yⁿ(1+y)−1=−1 → ②. 빠른정답 1과 불일치(목록 어긋남 추정).")

# p33
add(id="3b15871d", qtype="choice",
    question=("[[x = -2]], [[y = -1]]일 때,\n"
              "[[-frac(-2 pow(y,n), x) + frac(-pow(2,2) pow(y,n+1), pow(x,2)) + frac(-pow(2,3) pow(y,2n), pow(x,3))]]의 값은?\n"
              "(단, [[n]]은 자연수이다.)"),
    choices=["[[-5]]", "[[-3]]", "[[-1]]", "[[1]]", "[[3]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="항별로 −yⁿ, −yⁿ⁺¹, +1 → 1−yⁿ(1+y)=1 → ④ = 빠른정답 ✓.")

# p37
add(id="32fbd9b3", qtype="choice",
    question=("[[x = -5]], [[y = -1]]일 때,\n"
              "[[frac(-5 pow(y,n), x) - frac(-pow(5,2) pow(y,2n), pow(x,2)) + frac(-pow(5,3) pow(y,n+3), pow(x,3))]]의 값은?\n"
              "(단, [[n]]은 자연수이다.)"),
    choices=["[[-3]]", "[[-1]]", "[[1]]", "[[3]]", "[[5]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="항별로 yⁿ, +1, yⁿ⁺³=−yⁿ → 1 → ③. 빠른정답 2와 불일치.")

# p51
add(id="b07551c8", qtype="choice",
    question="[[x = -frac(1,6)]]일 때, 다음 식의 값 중 가장 큰 것은?",
    choices=["[[-x]]", "[[pow(x,2)]]", "[[frac(1, x)]]", "[[frac(1, pow(x,2))]]", "[[2(-frac(1, x) - 3)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="①1/6 ②1/36 ③−6 ④36 ⑤6 → ④. 빠른정답 5와 불일치.")

# p58
add(id="04f15de4", qtype="choice",
    question="[[a = frac(3,2)]], [[b = -frac(1,4)]], [[c = -frac(2,3)]], [[d = 2]]일 때,\n[[frac(3, a) - frac(1, b) - frac(d, c)]]의 값은?",
    choices=["[[-5]]", "[[9]]", "[[-9]]", "[[frac(73,12)]]", "[[frac(41,12)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="2−(−4)−(−3)=9 → ②. 빠른정답 38과 불일치.")

# ================= 수의 대소 관계 =================
# p31 (id 2개)
dup(["8648b549", "d6a96dc8"], qtype="choice",
    question="다음 □ 안에 알맞은 부등호가 나머지 넷과 다른 하나는?",
    choices=["[[1]] □ [[4]]", "[[abs(2)]] □ [[abs(-5)]]", "[[-2]] □ [[3]]", "[[abs(-2)]] □ [[abs(-1)]]", "[[-4]] □ [[-1]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="①②③⑤ '<', ④ 2>1 '>' → ④ (빠른정답 없음). 빈칸 □는 텍스트. 같은 이미지 id 2개 동일 전사.")

# p32
add(id="a8d99da6", qtype="choice",
    question="다음 □ 안에 알맞은 부등호가 나머지 넷과 다른 하나는?",
    choices=["[[3]] □ [[5]]", "[[abs(3)]] □ [[abs(-6)]]", "[[-6]] □ [[0]]", "[[abs(-6)]] □ [[abs(-9)]]", "[[-2]] □ [[-5]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="①②③④ '<', ⑤ −2>−5 '>' → ⑤ (빠른정답 없음). 빈칸 □는 텍스트.")

# p34 (id 3개)
dup(["a0949bab", "a4582253", "61cbcd81"], qtype="choice",
    question="다음 □ 안에 들어갈 부등호의 방향이 나머지 넷과 다른 하나는?",
    choices=["[[-12]] □ [[-9]]", "[[-0.2]] □ [[frac(1,5)]]", "[[-frac(1,4)]] □ [[-frac(1,5)]]",
             "[[frac(3,2)]] □ [[abs(-frac(4,3))]]", "[[abs(-frac(3,4))]] □ [[abs(frac(6,7))]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="①②③⑤ '<', ④ 3/2>4/3 '>' → ④ (빠른정답 없음). 빈칸 □는 텍스트. 같은 이미지 id 3개 동일 전사.")

# p53
add(id="10cb3e8b", qtype="choice",
    question="절댓값이 같은 두 정수 [[a]], [[b]]에 대하여 [[a > b]]이고 [[a]]와 [[b]] 사이의 거리가 22일 때, [[a]], [[b]]의 값은?",
    choices=["[[a = 22]], [[b = 0]]", "[[a = -11]], [[b = 0]]", "[[a = 0]], [[b = -22]]", "[[a = -11]], [[b = 11]]", "[[a = 11]], [[b = -11]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="|a|=|b|=11, a>b → a=11, b=−11 → ⑤ (빠른정답 없음).")

# p70
add(id="dfcdd51a", qtype="choice",
    question=("[[a > b]]인 두 정수 [[a]], [[b]]에 대하여 [[abs(a) + abs(b) = 8]]이 되도록 하는 [[a]], [[b]]의 값을 [[point(a, b)]]로 나타낼 때, "
              "[[point(a, b)]]의 개수는?"),
    choices=["[[11]]", "[[12]]", "[[13]]", "[[14]]", "[[15]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="|a|+|b|=8인 정수쌍 32개 중 a=b인 2개 제외 후 절반 → 15 → ⑤ (빠른정답 없음).")

# p77
add(id="22348eec", qtype="choice",
    question="[[abs(a) + abs(b) = 4]]를 만족시키는 두 정수 [[a]], [[b]]를 [[point(a, b)]]로 나타낼 때, [[point(a, b)]]의 개수는?",
    choices=["[[8]]", "[[10]]", "[[12]]", "[[14]]", "[[16]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="4×4=16 → ⑤ (빠른정답 없음).")

# ================= 유리수의 계산의 활용 (새로운 연산 기호) =================
# p1
add(id="2f48da2a", qtype="choice",
    question=("두 수 [[a]], [[b]]에 대하여 [[a]]△[[b]] = [[a ÷ b - 1]],\n[[a]]▲[[b]] = [[a × b + 1]]이라 할 때, "
              "([[frac(3,8)]]△[[frac(9,4)]])▲([[frac(5,4)]]△[[frac(1,2)]])을 계산하면?"),
    choices=["[[-frac(5,4)]]", "[[-frac(1,4)]]", "[[frac(1,4)]]", "[[frac(3,4)]]", "[[frac(3,2)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="3/8△9/4=1/6−1=−5/6, 5/4△1/2=3/2 → (−5/6)(3/2)+1=−1/4 → ② (빠른정답 없음). 약속 기호 △▲는 텍스트.")

# p2
add(id="d5de51a0", qtype="short",
    question=("두 수 [[a]], [[b]]에 대하여 [[a]] ◇ [[b]] = [[a - b]], [[a]] ○ [[b]] = [[a ÷ b]]로 약속할 때, "
              "[[frac(1,8)]] ○ ([[frac(1,2)]] ◇ [[frac(1,16)]])을 계산하시오."),
    choices=None, derived_answer="frac(2,7)", figure=None, difficulty_est=2, confidence=0.9,
    note="1/2−1/16=7/16, 1/8÷7/16=2/7 (빠른정답 없음). 약속 기호는 텍스트.")

# p3
add(id="13d8ba10", qtype="choice",
    question=("두 유리수 [[a]], [[b]]에 대하여\n[[a]] • [[b]] = [[a × b + a]], [[a]] ∘ [[b]] = [[a × b]]라 할 때, 다음을 계산한 값은?\n"
              "([[3]] • [[frac(5,2)]]) ∘ {[[frac(4,3)]] • [[pow((-3), 2)]]}"),
    choices=["[[frac(10,3)]]", "[[18]]", "[[50]]", "[[100]]", "[[140]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="3•5/2=21/2, 4/3•9=40/3 → 21/2×40/3=140 → ⑤ (빠른정답 없음). 식 상자는 텍스트.")

# p4
add(id="eaba3bca", qtype="short",
    question=("두 유리수 [[a]], [[b]]에 대하여 [[a]] • [[b]] = [[a + b × a]],\n[[a]] ∘ [[b]] = [[a - b ÷ a]]라 할 때, 다음을 구하시오.\n"
              "([[6]] • [[frac(3,2)]]) ∘ ([[frac(7,4)]] • [[(-pow(2,2))]])"),
    choices=None, derived_answer="frac(307,20)", figure=None, difficulty_est=3, confidence=0.85,
    note="6•3/2=15, 7/4•(−4)=7/4−7=−21/4 → 15−(−21/4)÷15=15+7/20=307/20 (빠른정답 없음). 원문 (−2²)=−4.")

# p6
add(id="32c8471a", qtype="short",
    question=("두 수 [[a]], [[b]]에 대하여\n[[a]]◇[[b]] = [[a - b + a × b]], [[a]] ○ [[b]] = [[a ÷ b]]로 약속할 때,\n"
              "[[frac(1,16)]] ○ ([[frac(1,4)]] ◇ [[frac(1,8)]])을 계산하시오."),
    choices=None, derived_answer="frac(2,5)", figure=None, difficulty_est=2, confidence=0.9,
    note="1/4◇1/8=1/4−1/8+1/32=5/32 → 1/16÷5/32=2/5 (빠른정답 없음).")

# p7
add(id="9d7d706b", qtype="short",
    question=("두 수 [[a]], [[b]]에 대하여\n[[a]] ∘ [[b]] = [[a × b - 1]], [[a]]△[[b]] = [[a - b ÷ (-2)]]라 약속할 때,\n"
              "{[[(-2)]] ∘ [[4]]}△{[[(-5)]] ∘ [[(-1)]]}의 값을 구하시오."),
    choices=None, derived_answer="-7", figure=None, difficulty_est=2, confidence=0.9,
    note="(−2)∘4=−9, (−5)∘(−1)=4 → −9−4÷(−2)=−7 (빠른정답 없음).")

# p8
add(id="a04e9a64", qtype="short",
    question=("두 수 [[a]], [[b]]에 대하여\n[[a]]△[[b]] = [[a × b - 3]], [[a]]◎[[b]] = [[a ÷ b + 1]]로 약속할 때,\n"
              "{[[(-2)]]△[[frac(5,6)]]}◎{[[(-5)]]△[[(-2)]]}를 계산하시오."),
    choices=None, derived_answer="frac(1,3)", figure=None, difficulty_est=2, confidence=0.9,
    note="(−2)△5/6=−14/3, (−5)△(−2)=7 → (−14/3)÷7+1=1/3 (빠른정답 없음).")

# p11
add(id="eea54b1a", qtype="choice",
    question=("[[floor(x) = (1 - x) ÷ (1 + x)]]로 약속할 때,\n"
              "[[sub(a,1) = frac(4,9)]], [[sub(a,2) = floor(sub(a,1))]], [[sub(a,3) = floor(sub(a,2))]], [[sub(a,4) = floor(sub(a,3))]], ⋯, "
              "[[sub(a,n+1) = floor(sub(a,n))]]이다. 이때\n"
              "[[frac(1, sub(a,1)) - frac(1, sub(a,2)) + frac(1, sub(a,3)) - frac(1, sub(a,4)) + frac(1, sub(a,5)) - frac(1, sub(a,6))]] + ⋯ + "
              "[[frac(1, sub(a,39)) - frac(1, sub(a,40))]]의 값은?"),
    choices=["[[-13]]", "[[-11]]", "[[-9]]", "[[-7]]", "[[-5]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="[[x]]=x이므로 주기 2: a₁=4/9, a₂=5/13 반복 → 20(9/4−13/5)=−7 → ④ = 빠른정답 ✓. 약속 기호 [x]는 표시가 같은 floor(x)로 적음(floor 뜻 아님). 줄임표는 텍스트.")

# p12
add(id="01b1ca88", qtype="choice",
    question=("[[floor(x) = (1 - x) ÷ (1 + x)]]로 약속할 때,\n"
              "[[sub(a,1) = frac(2,5)]], [[sub(a,2) = floor(sub(a,1))]], [[sub(a,3) = floor(sub(a,2))]], [[sub(a,4) = floor(sub(a,3))]], ⋯, "
              "[[sub(a,n+1) = floor(sub(a,n))]]이다. 이때\n"
              "[[frac(1, sub(a,1)) - frac(1, sub(a,2)) + frac(1, sub(a,3)) - frac(1, sub(a,4)) + frac(1, sub(a,5)) - frac(1, sub(a,6))]] + ⋯ + "
              "[[frac(1, sub(a,59)) - frac(1, sub(a,60))]]의 값은?"),
    choices=["[[-3]]", "[[-1]]", "[[1]]", "[[3]]", "[[5]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="a₁=2/5, a₂=3/7 반복 → 30(5/2−7/3)=5 → ⑤ = 빠른정답 ✓. 약속 기호 [x]는 floor(x)로 표기(표시 동일). 줄임표는 텍스트.")

# p13
add(id="8040518c", qtype="choice",
    question=("[[floor(x) = (1 - x) ÷ (1 + x)]]로 약속할 때, [[sub(a,1) = frac(5,7)]],\n"
              "[[sub(a,2) = floor(sub(a,1))]], [[sub(a,3) = floor(sub(a,2))]], [[sub(a,4) = floor(sub(a,3))]], ⋯, "
              "[[sub(a,n+1) = floor(sub(a,n))]]이다. 이때\n"
              "[[frac(1, sub(a,1)) - frac(1, sub(a,2)) + frac(1, sub(a,3)) - frac(1, sub(a,4)) + frac(1, sub(a,5)) - frac(1, sub(a,6))]] + ⋯ + "
              "[[frac(1, sub(a,49)) - frac(1, sub(a,50))]]의 값은?"),
    choices=["[[-115]]", "[[-105]]", "[[-95]]", "[[-85]]", "[[-75]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="a₁=5/7, a₂=1/6 반복 → 25(7/5−6)=−115 → ①. 빠른정답 '15'와 불일치(−115의 절단으로 보임). 약속 기호 [x]는 floor(x)로 표기.")

# p15
add(id="f1eea95f", qtype="choice",
    question=("0이 아닌 두 유리수 [[a]], [[b]]에 대하여\n[[a]]○[[b]] = [[a ÷ b + 1]], [[a]]●[[b]] = [[a × b + a + b]]라 할 때,\n"
              "[[-frac(1,6)]] ○ ([[frac(1,3)]] ● [[frac(1,9)]])의 값은?"),
    choices=["[[frac(1,2)]]", "[[frac(7,13)]]", "[[frac(15,26)]]", "[[frac(8,13)]]", "[[frac(17,26)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="1/3●1/9=13/27 → (−1/6)÷(13/27)+1=17/26 → ⑤ = 빠른정답 ✓.")

# p17
add(id="69071818", qtype="choice",
    question=("서로 다른 두 유리수 [[a]], [[b]]에 대하여\n[[a]] ★ [[b]] = [[(a + b) ÷ 2]]라 할 때, "
              "[[(-frac(1,6))]] ★ {[[(-4)]] ★ [[3]]}을 계산하면?"),
    choices=["[[-frac(1,2)]]", "[[-frac(1,3)]]", "[[-frac(1,6)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="(−4)★3=−1/2 → (−1/6−1/2)÷2=−1/3 → ② = 빠른정답 ✓.")

# p18
add(id="af6de300", qtype="short",
    question=("서로 다른 두 유리수 [[a]], [[b]]에 대하여\n[[a]]◎[[b]] = [[3 ÷ (b - a)]]라 할 때, "
              "[[(-frac(3,5))]]◎[[(-frac(3,2))]]을 계산하시오."),
    choices=None, derived_answer="-frac(10,3)", figure=None, difficulty_est=2, confidence=0.9,
    note="b−a=−9/10 → 3÷(−9/10)=−10/3 (빠른정답 없음).")

# p20
add(id="51538cac", qtype="short",
    question=("서로 다른 두 유리수 [[a]], [[b]]에 대하여 [[a]]◈[[b]] = [[4 × (a - b)]]라 할 때, "
              "[[(-frac(1,2))]]◈(+[[frac(4,3)]])을 계산하시오."),
    choices=None, derived_answer="-frac(22,3)", figure=None, difficulty_est=2, confidence=0.85,
    note="4(−1/2−4/3)=−22/3. 빠른정답 22/3(부호 없음)과 불일치. 양의 부호 (+4/3)는 텍스트 혼합.")

# p21
add(id="16bf5ad9", qtype="short",
    question=("서로 다른 두 유리수 [[a]], [[b]]에 대하여 [[a]]⊙[[b]] = [[2 ÷ (a ÷ b)]]라 할 때, "
              "[[frac(2,3)]] ⊙ [[(-frac(4,9))]]을 계산하시오."),
    choices=None, derived_answer="-frac(4,3)", figure=None, difficulty_est=2, confidence=0.9,
    note="2/3÷(−4/9)=−3/2 → 2÷(−3/2)=−4/3 (빠른정답 없음).")

# p23
add(id="326e624d", qtype="short",
    question=("유리수 [[a]], [[b]]에 대하여 [[a]]◎[[b]] = [[frac(a + b, 2)]]로 약속할 때,\n"
              "([[frac(1,3)]]◎[[frac(3,2)]])◎[[(-frac(1,5))]]의 값을 구하시오."),
    choices=None, derived_answer="frac(43,120)", figure=None, difficulty_est=2, confidence=0.9,
    note="1/3◎3/2=11/12 → (11/12−1/5)/2=43/120 = 빠른정답 ✓.")

# p25
add(id="fac001b2", qtype="short",
    question=("두 유리수 [[a]], [[b]]에 대하여 [[a]] ∘ [[b]] = [[frac(a + b, 2)]]로 약속할 때,\n"
              "[[frac(1,2)]] ∘ {[[frac(1,3)]] ∘ [[(-frac(1,4))]]}을 계산하시오."),
    choices=None, derived_answer="frac(13,48)", figure=None, difficulty_est=2, confidence=0.9,
    note="1/3∘(−1/4)=1/24 → (1/2+1/24)/2=13/48 = 빠른정답 ✓.")

# p31 (문자로 주어진 수의 대소)
add(id="f7462d84", qtype="choice",
    question=("[[-1 < a < 0]]일 때, 다음 수를 큰 수부터 차례로 나타낸 것은?\n"
              "[[frac(1, a)]], [[-a]], [[a]], [[0]], [[-frac(1, a)]], [[pow(a,2)]]"),
    choices=["[[frac(1, a)]], [[a]], [[0]], [[-frac(1, a)]], [[-a]], [[pow(a,2)]]",
             "[[0]], [[frac(1, a)]], [[a]], [[-frac(1, a)]], [[-a]], [[pow(a,2)]]",
             "[[frac(1, a)]], [[-a]], [[0]], [[-frac(1, a)]], [[a]], [[pow(a,2)]]",
             "[[-frac(1, a)]], [[-a]], [[pow(a,2)]], [[0]], [[a]], [[frac(1, a)]]",
             "[[-frac(1, a)]], [[-a]], [[0]], [[a]], [[frac(1, a)]], [[pow(a,2)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a=−1/2 대입: −1/a=2 > −a=1/2 > a²=1/4 > 0 > a > 1/a=−2 → ④ = 빠른정답 ✓. 나열 콤마는 텍스트.")

# ================= 소수와 합성수 =================
# p74
add(id="e3079ed2", qtype="short",
    question="다음 □ 안에 알맞은 수를 써넣으시오.\n두 번째로 작은 소수는 □이다.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="소수 2, 3, 5, … → 3. 빠른정답 10과 불일치. 빈칸 □는 텍스트.")

# p86
add(id="a1531ad0", qtype="short",
    question="다음 □ 안에 알맞은 수를 써넣으시오.\n짝수인 소수는 □개이다.",
    choices=None, derived_answer="1", figure=None, difficulty_est=1, confidence=0.9,
    note="짝수인 소수는 2 하나 → 1. 빠른정답 '소수'와 불일치. 빈칸 □는 텍스트.")

# ================= 절댓값 (약속 연산) =================
# p75
add(id="ff10cc81", qtype="short",
    question=("절댓값이 서로 다른 두 수 [[a]], [[b]]에 대하여\n"
              "[[a]]⊗[[b]] = { [[abs(a)]] ([[abs(a) < abs(b)]]) ; [[abs(b)]] ([[abs(a) > abs(b)]]) }라 할 때,\n"
              "[[(-frac(7,18))]]⊗{[[(-frac(11,2))]]⊗[[(-frac(9,5))]]}의 값을 구하시오."),
    choices=None, derived_answer="frac(7,18)", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 → 중괄호·경우 조건을 텍스트 혼합으로 적음",
    note="a⊗b=min(|a|,|b|): (−11/2)⊗(−9/5)=9/5, (−7/18)⊗(9/5)=7/18 = 빠른정답 ✓.")

# p76
add(id="53614914", qtype="short",
    question=("절댓값이 서로 다른 두 수 [[a]], [[b]]에 대하여\n"
              "[[a]]◇[[b]] = { [[abs(a)]] ([[abs(a) > abs(b)]]) ; [[abs(b)]] ([[abs(a) < abs(b)]]) }라 할 때,\n"
              "{[[(-frac(8,5))]]◇[[(-frac(11,4))]]}◇[[(-frac(16,3))]]의 값을 구하시오."),
    choices=None, derived_answer="frac(16,3)", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의 → 중괄호·경우 조건을 텍스트 혼합으로 적음",
    note="a◇b=max(|a|,|b|): (−8/5)◇(−11/4)=11/4, 11/4◇(−16/3)=16/3 = 빠른정답 ✓.")

# p80
add(id="f06aa735", qtype="short",
    question=("절댓값이 서로 다른 두 유리수 [[a]], [[b]]에 대하여\n"
              "[[a]]▲[[b]] = ([[a]], [[b]]중 절댓값이 큰 수)\n"
              "[[a]]▼[[b]] = ([[a]], [[b]]중 절댓값이 작은 수)\n"
              "로 약속할 때, {[[frac(3,4)]]▲[[(-frac(3,2))]]}▲{[[(-frac(5,4))]]▼[[frac(5,3)]]}를 계산하시오."),
    choices=None, derived_answer="frac(-3,2)", figure=None, difficulty_est=2, confidence=0.9,
    note="3/4▲(−3/2)=−3/2, (−5/4)▼5/3=−5/4 → (−3/2)▲(−5/4)=−3/2 = 빠른정답 ✓. 약속 기호·한글 정의는 텍스트.")

# p81
add(id="2119060b", qtype="short",
    question=("절댓값이 서로 다른 두 수 [[a]], [[b]]에 대하여\n"
              "[[a]]△[[b]] = ([[a]], [[b]] 중 절댓값이 큰 수),\n"
              "[[a]]▽[[b]] = ([[a]], [[b]] 중 절댓값이 작은 수)라 약속할 때,\n"
              "{[[(-6)]]▽[[(-9)]]}▽{[[3]]△[[(-5)]]}를 구하시오."),
    choices=None, derived_answer="-5", figure=None, difficulty_est=2, confidence=0.9,
    note="(−6)▽(−9)=−6, 3△(−5)=−5 → (−6)▽(−5)=−5 = 빠른정답 ✓.")

# p82
add(id="a805d977", qtype="short",
    question=("절댓값이 서로 다른 두 수 [[a]], [[b]]에 대하여\n"
              "[[a]]△[[b]] = ([[a]], [[b]] 중 절댓값이 큰 수),\n"
              "[[a]]▽[[b]] = ([[a]], [[b]] 중 절댓값이 작은 수)라고 약속할 때,\n"
              "{[[(-5)]]△[[3]]}▽{[[3]]△[[(-2)]]}의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=2, confidence=0.9,
    note="(−5)△3=−5, 3△(−2)=3 → (−5)▽3=3 = 빠른정답 ✓.")

# ================= 거리, 속력, 시간 =================
# p84
add(id="b3ed5cd5", qtype="short",
    question=("일정한 속력으로 달리는 기차가 길이 500 m의 철교를 완전히 지나는데 3분, 700 m의 터널을 완전히 지나는데 4분이 걸린다. "
              "이때 기차의 속력을 구하시오."),
    choices=None, derived_answer="분속 200 m", figure=None, difficulty_est=2, confidence=0.9,
    note="500+L=3v, 700+L=4v → v=200 m/분(기차 길이 100 m). 빠른정답 4와 불일치.")

# ================= 정수와 유리수 =================
# p24
add(id="83bebe4b", qtype="choice",
    question="다음 수에 대한 설명으로 옳은 것은?\n[[-frac(6,2)]], [[0]], +[[1]], [[frac(3,5)]], [[-4]], +[[frac(15,3)]]",
    choices=["양수는 4개이다.", "음수는 3개이다.", "자연수는 3개이다.", "정수는 5개이다.", "0은 정수가 아니다."],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.85,
    note="양수 3개, 음수 2개, 자연수 2개(1, 15/3=5), 정수 5개(−3, 0, 1, −4, 5) → ④. 빠른정답 1과 불일치. 양의 부호 +는 텍스트 혼합.")

# p40
add(id="d25f4656", qtype="choice",
    question=("수 [[x]]에 대하여\n⟨[[x]]⟩ = { 0 ([[x]]는 정수) ; 1 ([[x]]는 정수가 아닌 유리수) }로 약속할 때,\n"
              "다음 중 ⟨[[-frac(3,5)]]⟩ + ⟨[[0]]⟩ + ⟨[[2.6]]⟩ + ⟨[[x]]⟩ = 3을\n만족시키는 [[x]]가 될 수 없는 것은?"),
    choices=["[[-frac(5,4)]]", "[[-0.1]]", "[[frac(6,2)]]", "[[frac(2,7)]]", "[[2.9]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의와 약속 기호 ⟨x⟩를 텍스트 혼합으로 적음",
    note="1+0+1+⟨x⟩=3 → ⟨x⟩=1 → x는 정수가 아닌 유리수. 6/2=3은 정수 → ③. 빠른정답 2와 불일치.")

# p60 (id 2개, 분류 계통도)
dup(["3ad170ef", "2cf5fb7d"], qtype="short",
    question=("다음 수 중에서 유리수 { 정수 { 양의 정수, 0, 음의 정수 }, □ }의 □ 안에 들어갈 수 있는 수의 개수를 구하시오.\n"
              "[[-5]], [[-2.3]], [[5.2]], [[frac(1,11)]], [[-frac(3,5)]], [[3]]"),
    choices=None, derived_answer="4",
    figure=[{"fn": "unsupported", "args": {"raw": "유리수 분류 계통도(중괄호 도표): 유리수 → { 정수 → { 양의 정수, 0, 음의 정수 }, □(빈칸) }. 아래 상자에 −5, −2.3, 5.2, 1/11, −3/5, 3"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 유리수 분류 계통도(중괄호 도표, 빈칸 □ 포함)",
    note="□=정수가 아닌 유리수: −2.3, 5.2, 1/11, −3/5 → 4개 = 빠른정답 ✓. 같은 이미지 id 2개 동일 전사.")

# p66
add(id="3babd113", qtype="short",
    question=("유리수 [[x]]에 대하여\n⟨[[x]]⟩ = { 0 ([[x]]는 정수) ; 1 ([[x]]는 정수가 아닌 유리수) }\n"
              "라 할 때, ⟨[[-frac(2,3)]]⟩ + ⟨[[-2]]⟩ + ⟨[[3.4]]⟩ + ⟨[[0]]⟩의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 한계: 조각적(경우 나눔) 정의와 약속 기호 ⟨x⟩를 텍스트 혼합으로 적음",
    note="1+0+1+0=2 = 빠른정답 ✓.")

# ================= 그래프 =================
# p30
add(id="71313f30", qtype="short",
    question=("다음은 시간 [[x]]와 집으로부터의 거리 [[y]] 사이의 관계를 나타낸 그래프이다. 그래프에 알맞은 상황을 보기에서 찾으시오.\n<보기>\n"
              "ㄱ. 성진이는 집에서 공부를 하고 있었다.\n"
              "ㄴ. 준성이는 백화점에서 일정한 속력으로 집으로 걸어오던 도중 식당에 들러 밥을 먹고 일정한 속력으로 집에 돌아왔다.\n"
              "ㄷ. 현성이는 집에서 출발하여 일정한 속력으로 노래방에 갔다.\n"
              "ㄹ. 경수는 집에서 출발하여 일정한 속력으로 서점에 가서 책을 읽고 일정한 속력으로 집에 돌아왔다."),
    choices=None, derived_answer="ㄹ",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(원점 O, 가로축 x, 세로축 y, 눈금 없음): 원점에서 출발해 일정하게 증가하는 직선 → 수평 구간 → 일정하게 감소하여 x축에 닿는 사다리꼴 모양 그래프"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 시간–거리 그래프(원점 출발 → 증가 → 수평 → 감소하여 0으로, 사다리꼴 모양)",
    note="집(거리 0)에서 출발, 멈춤(수평), 집으로 복귀 → ㄹ. 빠른정답 5와 불일치.")

# p41
add(id="3466fedf", qtype="short",
    question=("높이가 50 cm인 욕조에 물을 채우려고 한다. 경과 시간 [[x]]분에 따른 물의 높이를 [[y]] cm라 할 때, "
              "[[x]]와 [[y]] 사이의 관계를 그래프를 나타내면 다음 그림과 같다.\n□ 안에 알맞은 수를 써넣으시오.\n"
              "물을 채우기 시작한 지 □분까지 물의 높이가 일정하게 증가한다."),
    choices=None, derived_answer="15",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 그래프(모눈): x축 눈금 3, 6, 9, 12, 15, y축 눈금 10~50. 원점에서 점 (15, 50)까지 이어지는 직선(끝점에 점 표시)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 원점~(15, 50) 직선 그래프",
    note="그래프가 (15, 50)까지 직선 → 15분. 빠른정답 '48분'과 불일치.")

# p83
add(id="a770dd76", qtype="choice",
    question=("민지와 동생 민수는 집에서 2 km 떨어진 학교까지 일정한 속력으로 걸어간다고 한다. 민지와 민수가 집에서 학교까지 같은 경로로 이동할 때, "
              "민수가 출발한 시각으로부터 [[x]]분 후 민수와 민지가 집과 떨어진 거리를 각각 [[y]] km라 하자. "
              "아래 그림은 두 변수 [[x]], [[y]] 사이의 관계를 나타낸 그래프일 때, 다음 보기 중 그래프에 대한 설명으로 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 민지가 학교에 가는 데 걸린 시간은 15분이다.\n"
              "ㄴ. 민지가 민수보다 15분 빨리 학교에 도착했다.\n"
              "ㄷ. 민지의 속력은 민수의 속력의 3배이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 그래프(모눈, x(분) 0~30 눈금 5, y(km) 0~2 눈금 0.5): '민수' 직선은 원점에서 (30, 2)까지, '민지' 직선은 (5, 0)에서 (15, 2)까지. 두 직선은 (7.5, 0.5)에서 교차"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 두 직선(민지·민수) 시간–거리 그래프",
    note="민지 5분 출발→15분 도착(10분 소요, ㄱ 거짓), 민수 30분 도착(ㄴ 참), 속력 0.2 vs 1/15 → 3배(ㄷ 참) → ④. 빠른정답 5와 불일치.")

# ================= 부등호의 사용 =================
# p47
add(id="caab3e45", qtype="short",
    question=("다음 조건을 모두 만족시키는 두 정수 [[a]], [[b]]를 [[point(a, b)]]로 나타낼 때, [[point(a, b)]]의 개수를 구하시오.\n"
              "(가) [[frac(15, a)]], [[frac(35, a)]]는 양의 정수이다.\n"
              "(나) [[frac(1,7) < abs(frac(b, a)) <= frac(1,4)]]"),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.9,
    note="a∈{1, 5}; a=1이면 해 없음, a=5이면 5/7<|b|≤5/4 → b=±1 → 2개 = 빠른정답 ✓.")

# ================= 유리수의 곱셈과 나눗셈 =================
# p12 (결합법칙 위치 ①~④ — 화살표 4개)
add(id="959c1000", qtype="short",
    question=("다음 계산 과정에서 곱셈의 결합법칙이 이용된 곳은?\n"
              "(+4) × [[(-3)]] × (+0.5)\n"
              "= (+4) × (+0.5) × [[(-3)]]  ← ①\n"
              "= {(+4) × (+0.5)} × [[(-3)]]  ← ②\n"
              "= (+2) × [[(-3)]]  ← ③\n"
              "= [[-6]]  ← ④"),
    choices=None, derived_answer="②", figure=None, difficulty_est=1, confidence=0.75,
    needs_review="스키마 한계: 선지 위치 표시가 ①~④ 4개뿐이라 choice(5개) 불가 → short로 전사",
    note="①~④는 연속한 두 행 사이의 변형 단계 화살표. 2→3행 중괄호 묶기가 결합법칙 → ② (빠른정답 없음). 양의 부호 (+a)는 텍스트 혼합.")

# p16
add(id="5b199c93", qtype="short",
    question="곱셈의 계산 법칙을 이용하여 다음을 계산하시오.\n[[(-40) × (-33) × (-0.05)]] × (+[[frac(4,11)]])",
    choices=None, derived_answer="-24", figure=None, difficulty_est=1, confidence=0.85,
    note="(−40)(−0.05)=2, (−33)(4/11)=−12 → −24 (빠른정답 없음). 양의 부호 (+4/11)는 텍스트 혼합.")

# p24
add(id="c29b7e45", qtype="short",
    question=("5개의 유리수 [[-3]], [[-frac(1,2)]], +[[frac(2,3)]], [[-frac(3,4)]], +[[2]] 중 3개를 뽑아 곱한 값 중 "
              "가장 큰 값과 가장 작은 값의 합을 구하시오."),
    choices=None, derived_answer="frac(1,2)", figure=None, difficulty_est=2, confidence=0.85,
    note="최대 (−3)(−3/4)(2)=9/2, 최소 (−3)(2/3)(2)=−4 → 1/2 = 빠른정답 ✓. 양의 부호 +는 텍스트 혼합.")

# p62
add(id="4aaf224d", qtype="short",
    question="(+[[frac(10,7)]]) ÷ [[(-frac(5,4))]]를 계산하시오.",
    choices=None, derived_answer="-frac(8,7)", figure=None, difficulty_est=1, confidence=0.85,
    note="10/7×(−4/5)=−8/7 = 빠른정답 ✓. 양의 부호 (+10/7)는 텍스트 혼합.")

# p63
add(id="12925087", qtype="short",
    question="[[(-56)]] ÷ (+8)을 계산하시오.",
    choices=None, derived_answer="-7", figure=None, difficulty_est=1, confidence=0.85,
    note="−56÷8=−7 = 빠른정답 ✓. 양의 부호 (+8)은 텍스트 혼합.")

# p67 (한 이미지·문항 1개에 id 6개)
dup(["455f8aa4", "4a63324b", "b3713469", "d3f0382b", "58f244da", "d3a2da84"], qtype="choice",
    question="다음 □ 안에 들어갈 수 중 가장 작은 수는?",
    choices=["(+[[frac(1,3)]]) × □ = [[2]]",
             "(+[[frac(5,2)]]) × □ = [[5]]",
             "□ × [[pow((-2), 4)]] = [[-32]]",
             "□ ÷ (+2)² = [[frac(1,4)]]",
             "[[15]] × □ = [[45]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    note="①6 ②2 ③−32÷16=−2 ④1 ⑤3 → ③ (빠른정답 없음). 빈칸 □·양의 부호 (+a)는 텍스트. 같은 이미지 id 6개 동일 전사.")

# p85
add(id="64e75ac8", qtype="choice",
    question="[[a < 0]], [[b < 0]]일 때, 다음 중 항상 양수가 되는 것은?",
    choices=["[[a + b]]", "[[a - b]]", "[[a × b]]", "[[(-a) × b]]", "[[-pow(b,2)]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="음수×음수=양수 → ③ (빠른정답 없음).")

# ================= 양의 부호와 음의 부호 =================
# p1
add(id="b1cc567f", qtype="short",
    question="다음 수 중 음수의 개수를 구하시오.\n[[-1]], [[-2.9]], +[[frac(1,5)]], [[0]], +[[10]], [[7]]",
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.85,
    note="−1, −2.9 → 2개 (빠른정답 없음). 양의 부호 +는 텍스트 혼합.")
