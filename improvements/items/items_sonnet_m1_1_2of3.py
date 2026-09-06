# -*- coding: utf-8 -*-
# esc_sonnet_m1-1_2of3 — 이미지 기준 전사 (85 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ================= 양의 부호와 음의 부호 =================
# p5
add(id="0df64e4e", qtype="choice",
    question="다음 중 양의 부호 + 또는 음의 부호 −를 사용하여 나타낸 것으로 옳지 않은 것은?",
    choices=["출발 3일 후: +[[3]]일",
             "출발 5일 전: [[-5]]일",
             "[[2]]kg 증가: +[[2]]kg",
             "[[3.5]]kg 감소: +[[3.5]]kg",
             "수입 1000원: +[[1000]]원"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="④ 3.5kg 감소는 −3.5kg → ④ (빠른정답 없음). 양의 부호 +는 마커 밖 텍스트.")

# p9
add(id="249f7470", qtype="short",
    question="다음 수를 양의 부호 + 또는 음의 부호 −를 사용하여 나타냈을 때, □ 안에 알맞은 수를 써넣으시오.\n[[pct(8)]] 인하 ⇨ □%",
    choices=None, derived_answer="-8", figure=None, difficulty_est=1, confidence=0.9,
    note="8% 인하 → −8% → □ = −8 (빠른정답 없음). 빈칸 □는 텍스트.")

# p11
add(id="7f966c6c", qtype="short",
    question="다음 수 중 음수의 개수를 구하시오.\n[[-7]], +[[4]], [[-frac(1,3)]], +[[2.3]], [[0]], [[-frac(5,6)]]",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="음수 −7, −1/3, −5/6 → 3개. 빠른정답 4와 불일치. 양의 부호 +는 텍스트.")

# p14
add(id="fe5c4e92", qtype="short",
    question="다음 수를 양의 부호 + 또는 음의 부호 −를 사용하여 나타냈을 때, □ 안에 알맞은 수를 써넣으시오.\n[[3000]]원 입금 ⇨ □원",
    choices=None, derived_answer="3000", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 답 '+3000'의 양의 부호 +는 답 문법으로 표기 불가(3000으로 기재)",
    note="입금 → +3000원. 빠른정답 3과 불일치.")

# p16
add(id="ff724b52", qtype="choice",
    question="다음 중 양의 부호 + 또는 음의 부호 −를 사용하여 나타낸 것으로 옳지 않은 것은?",
    choices=["출발 2시간 후: +[[2]]시간",
             "[[5]]m 상승: +[[5]]m",
             "[[8]]kg 감소: [[-8]]kg",
             "지출 1000원: +[[1000]]원",
             "0보다 2 작은 수: [[-2]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="지출 1000원은 −1000원 → ④. 빠른정답 'neg 10000'과 불일치. 양의 부호 +는 텍스트.")

# p20 (id 3개)
dup(["b2185075", "43afe389", "1f14a349"], qtype="choice",
    question="다음 중 밑줄 친 부분을 부호 +, −를 사용하여 나타낸 것으로 옳지 않은 것은?",
    choices=["어느 산의 높이는 해발 [[1820]]m이다. ⇨ +[[1820]]m",
             "오늘 낮 최저 기온은 영하 [[3]]℃이다. ⇨ [[-3]]℃",
             "약속 시간보다 [[30]]분 전에 도착하였다. ⇨ +[[30]]분",
             "오늘 지각한 학생 수가 어제보다 [[3]]명 늘었다. ⇨ +[[3]]명",
             "순이익이 지난 달보다 [[10]]만 원 증가하였다. ⇨ +[[10]]만 원"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="30분 전은 −30분 → ③. 빠른정답 5와 불일치. 밑줄 표시는 생략, 양의 부호 +는 텍스트.")

# p22
add(id="75fb8ca7", qtype="choice",
    question="다음 중 부호 +, −를 사용하여 나타낸 것으로 옳지 않은 것은?",
    choices=["[[600]]원 손해: [[-600]]원",
             "출발 [[10]]분 후: [[-10]]분",
             "영상 [[20]]℃: +[[20]]℃",
             "[[8]]m 하강: [[-8]]m",
             "[[5]]kg 감량: [[-5]]kg"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="출발 10분 후는 +10분 → ② = 빠른정답 ✓. 양의 부호 +는 텍스트.")

# p28
add(id="84d8f1a5", qtype="choice",
    question="다음 중 +, −부호를 사용하여 나타낸 것으로 옳지 않은 것은?",
    choices=["영상 [[6]]℃를 +[[6]]℃라 하면 영하 [[2]]℃는 [[-2]]℃이다.",
             "출발 1시간 후를 +[[1]]시간이라 하면 출발 2시간 전은 [[-2]]시간이다.",
             "전출생 수 7명을 [[-7]]명이라 하면 전입생 수 13명은 +[[13]]명이다.",
             "수입 7000원을 +[[7000]]원이라 하면 지출 3000원은 [[-3000]]원이다.",
             "우리 학교에서 서쪽으로 [[50]]m 떨어진 지점을 [[-50]]m라 하면 동쪽으로 [[200]]m 떨어진 지점은 [[-200]]m이다."],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="동쪽 200m는 +200m → ⑤. 빠른정답 3과 불일치. 양의 부호 +는 텍스트.")

# p43
add(id="ddb95f80", qtype="choice",
    question="다음 중 밑줄 친 부분을 부호 +, −를 사용하여 나타낸 것으로 옳지 않은 것은?",
    choices=["작년보다 키가 [[3]]cm 컸다. ⇨ +[[3]]cm",
             "오늘 낮의 최고 기온은 영상 [[15]]℃이다. ⇨ +[[15]]℃",
             "오늘 매출이 어제보다 [[15]]만 원 감소하였다. ⇨ [[-15]]만 원",
             "수업 시간이 시작된 지 [[20]]분 후에 교실에 들어갔다. ⇨ [[-20]]분",
             "모든 직원의 연봉이 작년보다 [[pct(10)]] 올랐다. ⇨ +[[pct(10)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="20분 후는 +20분 → ④ = 빠른정답 ✓. 밑줄 표시는 생략, 양의 부호 +는 텍스트.")

# p46
add(id="a21f762f", qtype="short",
    question="0보다 23만큼 큰 수를 부호 +또는 −를 사용하여 나타내시오.",
    choices=None, derived_answer="23", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="문법 범위 밖: 답 '+23'의 양의 부호 +는 답 문법으로 표기 불가(23으로 기재)",
    note="0보다 23만큼 큰 수 → +23. 빠른정답 'add 23'(+23)과 같은 취지.")

# p47
add(id="faae2adf", qtype="choice",
    question="다음 중 밑줄 친 부분을 부호 +, −를 사용하여 나타낸 것으로 옳지 않은 것은?",
    choices=["약속 시간 [[30]]분 전이다. ⇨ [[-30]]분",
             "학교 옆 산의 높이는 해발 [[1500]]m이다. ⇨ +[[1500]]m",
             "오늘 아침의 최고 기온은 영상 [[24]]℃이다. ⇨ +[[24]]℃",
             "동연이의 몸무게가 작년보다 [[3.4]]kg 감소하였다. ⇨ +[[3.4]]kg",
             "이번 달 매출이 지난달 매출보다 [[10]]만 원 증가하였다. ⇨ +[[10]]만 원"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="3.4kg 감소는 −3.4kg → ④ = 빠른정답 ✓. 밑줄 표시는 생략, 양의 부호 +는 텍스트.")

# ================= 문자를 사용한 식 =================
# p25
add(id="d4b0978c", qtype="choice",
    question="밑변의 길이가 [[x]], 높이의 길이가 [[y]]인 삼각형의 밑변의 길이를 [[pct(20)]] 늘이고 높이를 [[pct(20)]] 줄이면 넓이는 어떻게 변화하는가?",
    choices=["[[pct(2)]] 증가", "[[pct(2)]] 감소", "[[pct(4)]] 증가", "[[pct(4)]] 감소", "변화 없다."],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="(1.2x)(0.8y)/2 = 0.96·(xy/2) → 4% 감소 → ④ = 빠른정답 ✓.")

# p30 (직육면체 그림)
add(id="84887e6e", qtype="choice",
    question="다음 중 아래 그림과 같은 직육면체의 겉넓이를 문자를 사용한 식으로 바르게 나타낸 것은?",
    choices=["[[6a + 6b]]", "[[6(a b + b c + c a)]]", "[[6a + 6b + 2 a b]]", "[[pow(a,2) + pow(b,2) + 12]]", "[[12a + 12b + 2 a b]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체(분홍색): 밑면의 가로 a, 세로 b, 높이 6 (점선으로 치수 표시)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 치수 a, b, 6이 표시된 직육면체",
    note="겉넓이 2(ab + 6a + 6b) = 12a + 12b + 2ab → ⑤. 빠른정답 4와 불일치.")

# p81
add(id="e02038e9", qtype="choice",
    question="[[pct(a)]]의 소금물 [[400]]g과 [[pct(b)]]의 소금물 [[300]]g을 섞은 소금물에 들어 있는 소금의 양을 문자를 사용한 식으로 나타낸 것은?",
    choices=["[[12 a b]] g", "[[frac(3b, 4a)]] g", "[[frac(4a, 3b)]] g", "[[(4a + 3b)]] g", "[[frac(4a + 3b, 100)]] g"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="400a/100 + 300b/100 = 4a + 3b → ④ = 빠른정답 ✓.")

# p92
add(id="ad9a1746", qtype="choice",
    question="다음 문자를 사용한 식으로 나타낸 것 중 옳지 않은 것은?",
    choices=["두 수 [[a]]와 [[b]]의 평균 → [[frac(a + b, 2)]]",
             "[[8]]kg의 [[pct(a)]] → [[0.08 a]]kg",
             "500원짜리 아이스크림 [[y]]개의 가격 → [[500 y]]원",
             "[[a]]개에 3000원인 공책 1권의 가격 → [[3000 a]]원",
             "시속 [[3]]km로 [[x]]시간 동안 간 거리 → [[3x]]km"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="④ 공책 1권 가격은 3000/a원 → ④. 빠른정답 3과 불일치.")

# ================= 방정식과 항등식 =================
# p1
add(id="6d7f69f1", qtype="choice",
    question="다음 등식에서 좌변과 우변을 각각 옳게 나타낸 것은?\n[[x + 3y = frac(3,2) x - 2]]",
    choices=["좌변: [[x]], 우변: [[frac(3,2) x - 2]]",
             "좌변: [[x]], 우변: [[-2]]",
             "좌변: [[x + 3y]], 우변: [[-2]]",
             "좌변: [[3y]], 우변: [[-2]]",
             "좌변: [[x + 3y]], 우변: [[frac(3,2) x - 2]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="좌변 x+3y, 우변 (3/2)x−2 → ⑤ = 빠른정답 ✓.")

# p2
add(id="d757b6f4", qtype="choice",
    question="다음 등식에서 좌변과 우변을 각각 나타내면?\n[[5x - 2 = 3]]",
    choices=["좌변: [[x]], 우변: [[3]]",
             "좌변: [[5x]], 우변: [[3]]",
             "좌변: [[5x]], 우변: [[-2]]",
             "좌변: [[5x - 2]], 우변: [[3]]",
             "좌변: [[x - 2]], 우변: [[3]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="좌변 5x−2, 우변 3 → ④ = 빠른정답 ✓.")

# p84
add(id="1369091b", qtype="choice",
    question="다음 등식이 항등식이 되도록 상수 [[a]], [[b]]의 값은?\n[[3 + 2(x + 1) = a x + b]]",
    choices=["[[a = 1]], [[b = 3]]", "[[a = 1]], [[b = 5]]", "[[a = 2]], [[b = 3]]", "[[a = 2]], [[b = 5]]", "[[a = 2]], [[b = 6]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="좌변 = 2x + 5 → a=2, b=5 → ④. 빠른정답 9와 불일치.")

# p89
add(id="50b63424", qtype="choice",
    question="등식 [[a x - 6 = 4x + 3b]]가 모든 [[x]]에 대하여 항상 참이 될 때, [[a + b]]의 값은? (단, [[a]], [[b]]는 상수)",
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="a=4, 3b=−6 → b=−2 → a+b=2 → ⑤. 빠른정답 '2'는 값 2(=⑤)로 보임.")

# ================= 다항식과 일차식 =================
# p12
add(id="e499daed", qtype="short",
    question=("[[pow(x,2)]]의 계수가 3, [[x]]의 계수가 [[a]], 상수항이 [[c]]인 [[x]]에 대한 이차식이 "
              "[[3 pow(x, b) + (c - 4) x - (b - 5)]]일 때, 이를 만족시키는 정수 [[a]], [[b]], [[c]]에 대하여 [[a b c]]의 값을 구하시오."),
    choices=None, derived_answer="-6", figure=None, difficulty_est=2, confidence=0.9,
    note="b=2, 상수항 −(b−5)=3=c, a=c−4=−1 → abc=−6. 빠른정답 5와 불일치.")

# ================= 정비례 =================
# p9
add(id="3bf4ffd5", qtype="choice",
    question="다음 중 [[x]]의 값이 2배, 3배, 4배, ⋯가 될 때, [[y]]의 값도 2배, 3배, 4배, ⋯가 되는 것을 모두 고르면? (정답 2개)",
    choices=["[[y = x]]", "[[frac(y, x) = 2]]", "[[y = x + 5]]", "[[x y = 0]]", "[[y - x = 2]]"],
    derived_answer="①, ②", figure=None, difficulty_est=1, confidence=0.9,
    note="정비례 y=x, y=2x → ①, ②. 빠른정답 2와 불일치(부분 일치).")

# p32 (선지가 그래프)
add(id="87be4fdc", qtype="choice",
    question="[[x]]의 범위가 [[-2]], [[-1]], [[0]], [[1]], [[2]]일 때, [[y = -2x]]의 그래프는?",
    choices=["(그림) 좌표평면 위의 점 5개: [[point(-2, -4)]], [[point(-1, -2)]], [[point(0, 0)]], [[point(1, 2)]], [[point(2, 4)]]",
             "(그림) 원점과 점 [[point(1, 2)]]를 지나는 직선",
             "(그림) 좌표평면 위의 점 5개: [[point(-2, 4)]], [[point(-1, 2)]], [[point(0, 0)]], [[point(1, -2)]], [[point(2, -4)]]",
             "(그림) 원점과 점 [[point(2, -1)]]을 지나는 직선",
             "(그림) 원점과 점 [[point(1, -2)]]를 지나는 직선"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "선지 ①~⑤가 각각 모눈 좌표평면 그림(눈금 −2, 2 표시). ① 점 (−2,−4),(−1,−2),(0,0),(1,2),(2,4) ② 원점을 지나는 직선 y=2x ③ 점 (−2,4),(−1,2),(0,0),(1,−2),(2,−4) ④ 원점을 지나는 직선 y=−x/2 ⑤ 원점을 지나는 직선 y=−2x"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 선지 5개가 모두 좌표평면 그래프(점·직선) / 선지 문구는 그림을 읽어 서술한 텍스트(원문 선지 아님)",
    note="x가 5개 값이므로 점 5개, y=−2x → (−2,4),…,(2,−4) → ③. 빠른정답 1과 불일치.")

# p70 (좌표평면 그림)
add(id="45be26c5", qtype="short",
    question=("다음 그림과 같이 두 정비례 관계 [[y = a x]], [[y = b x]]의 그래프가 제1사분면과 제3사분면을 지난다. "
              "[[y]]축 위의 점 A와 [[y = a x]], [[y = b x]]의 그래프 위의 점 B, C에 대하여 세 점 A, B, C는 [[x]]축에 평행한 직선 위에 있고 "
              "선분 AB의 길이와 선분 BC의 길이의 비가 [[ratio(5, 6)]]일 때, [[frac(b, a)]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="frac(5,11)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(원점 O): 원점을 지나는 두 직선 y=ax(더 가파름), y=bx. y축 위의 점 A에서 x축에 평행하게 그은 선분이 y=ax와 B, y=bx와 C에서 만남(왼쪽부터 A, B, C)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 두 정비례 그래프와 수평 선분 ABC",
    note="A(0,k)일 때 B의 x좌표 k/a, C의 x좌표 k/b → (k/a):(k/b−k/a)=5:6 → 11/a=5/b → b/a=5/11 = 빠른정답 ✓.")

# p71 (좌표평면 그림)
add(id="8f8d4455", qtype="short",
    question=("다음 그림과 같이 두 정비례 관계 [[y = a x]], [[y = b x]]의 그래프가 제1사분면과 제3사분면을 지난다. "
              "[[y]]축 위의 점 A와 [[y = a x]], [[y = b x]]의 그래프 위의 점 B, C에 대하여 세 점 A, B, C는 [[x]]축에 평행한 직선 위에 있고 "
              "선분 AB의 길이와 선분 BC의 길이의 비가 [[ratio(3, 4)]]일 때, [[frac(b, a)]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="frac(3,7)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(원점 O): 원점을 지나는 두 직선 y=ax(더 가파름), y=bx. y축 위의 점 A에서 x축에 평행하게 그은 선분이 y=ax와 B, y=bx와 C에서 만남(왼쪽부터 A, B, C)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 두 정비례 그래프와 수평 선분 ABC",
    note="(k/a):(k/b−k/a)=3:4 → 7/a=3/b → b/a=3/7 = 빠른정답 ✓.")

# p72 (좌표평면 그림)
add(id="f63d3925", qtype="short",
    question=("아래의 그림과 같이 정비례 관계 [[y = -frac(1,2) x]]의 그래프 위의 [[y]]좌표가 [[-3]]인 점 A와 정비례 관계 [[y = a x]]의 그래프 위의 점 B를 이은 "
              "선분 AB가 [[y]]축에 평행할 때, 선분 AB와 [[x]]축이 만나는 점을 P라 하자.\n"
              "선분 BP의 길이가 선분 AP의 길이의 2배일 때, 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="1",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(원점 O): 원점을 지나는 직선 y=ax(오른쪽 위)와 y=−(1/2)x(오른쪽 아래). x축 위의 점 P에서 세운 수직 선분 위에 B(y=ax 위, 위쪽)와 A(y=−x/2 위, 아래쪽). A의 y좌표 −3을 y축에 점선으로 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 두 정비례 그래프와 수직 선분 AB",
    note="A(6,−3), P(6,0), AP=3 → BP=6 → B(6,6) → a=1 = 빠른정답 ✓.")

# ================= 최대공약수와 최소공배수의 응용 =================
# p60
add(id="8eff9955", qtype="choice",
    question="1이 아닌 자연수 [[a]]로 214, 916, 151, 448을 나누었더니 그 나머지가 [[b]]로 같다. 이때 [[point(a, b)]]의 꼴로 나타내었을 때의 개수는?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="네 수의 차의 최대공약수 9 → a=3(b=1), a=9(b=7) → 2개 → ②. 빠른정답 32와 불일치. 순서쌍 (a, b)는 point로 표기.")

# ================= 일차식과 수의 곱셈, 나눗셈 =================
# p31
add(id="56bf06b9", qtype="short",
    question="[[(-2x - frac(8,5) y) × (-10) = a x + b y]]일 때, 상수 [[a]], [[b]]에 대하여 [[a - b]]의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="20x + 16y → a−b = 4. 빠른정답 '6x'와 불일치.")

# p32
add(id="e3ebe5b5", qtype="short",
    question="[[(4x - frac(5,3) y) × (-6) = a x + b y]]일 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="-14", figure=None, difficulty_est=1, confidence=0.9,
    note="−24x + 10y → a+b = −14. 빠른정답 −15와 불일치.")

# p34
add(id="78b5e415", qtype="short",
    question="[[(10x - 5) × (-frac(2,5)) = a x + b]]일 때, 상수 [[a]], [[b]]에 대하여 [[b - a]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="−4x + 2 → b−a = 6. 빠른정답 4와 불일치.")

# p36
add(id="cd262388", qtype="short",
    question="[[(9x - 15) ÷ (-frac(3,2))]]을 간단히 하면 [[a x + b]]일 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="(9x−15)×(−2/3) = −6x + 10 → a+b = 4. 빠른정답 21과 불일치.")

# p37
add(id="ca2946f1", qtype="short",
    question="[[(3x - frac(9,4) y) × (-12) = a x + b y]]일 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="-9", figure=None, difficulty_est=1, confidence=0.9,
    note="−36x + 27y → a+b = −9. 빠른정답 6과 불일치.")

# p39
add(id="98569aad", qtype="short",
    question="[[(3x - 6) ÷ (-frac(3,4)) = a x + b]]일 때, [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="(3x−6)×(−4/3) = −4x + 8 → a+b = 4 = 빠른정답 ✓.")

# p48
add(id="3a5fc01f", qtype="short",
    question="[[(15x - 9) × (-frac(4,3)) = a x + b]]일 때, 상수 [[a]], [[b]]에 대하여 [[b - a]]의 값을 구하시오.",
    choices=None, derived_answer="32", figure=None, difficulty_est=1, confidence=0.9,
    note="−20x + 12 → b−a = 32 = 빠른정답 ✓.")

# p54 (공원 그림)
add(id="942a386c", qtype="choice",
    question=("가로, 세로의 길이가 각각 [[15]]m, [[21]]m인 직사각형 모양의 공원에 다음 그림과 같이 폭이 각각 일정한 길을 내어 화단을 만들었다. "
              "화단의 넓이를 [[a]]를 사용한 식으로 나타내면?"),
    choices=["[[180]] m²", "[[24a]] m²", "[[(90 - 24a)]] m²", "[[(180 - 24a)]] m²", "[[(180 + 24a)]] m²"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 공원(가로 15m, 세로 21m): 가로 방향 길 3개(폭 각 3m)와 세로 방향 길 2개(폭 각 a m)가 격자 모양으로 나 있고, 나머지 4×3=12칸이 화단(초록색)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 길이 난 직사각형 공원 격자 그림",
    note="(15−2a)(21−9) = 180 − 24a → ④. 빠른정답 −50과 불일치. 단위 m²는 텍스트.")

# p55 (공원 그림)
add(id="5d57b9cf", qtype="choice",
    question=("가로, 세로의 길이가 각각 [[21]]m, [[18]]m인 직사각형 모양의 공원에 다음 그림과 같이 폭이 각각 일정한 길을 내어 화단을 만들었다. "
              "화단의 넓이를 [[a]]를 사용한 식으로 나타내면?"),
    choices=["[[189]] m²", "[[18a]] m²", "[[(63 - 18a)]] m²", "[[(189 - 18a)]] m²", "[[(189 + 18a)]] m²"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 공원(가로 21m, 세로 18m): 가로 방향 길 3개(폭 각 3m)와 세로 방향 길 2개(폭 각 a m)가 격자 모양으로 나 있고, 나머지 4×3=12칸이 화단(초록색)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 길이 난 직사각형 공원 격자 그림",
    note="(21−2a)(18−9) = 189 − 18a → ④. 빠른정답 −27과 불일치. 단위 m²는 텍스트.")

# p57 (사다리꼴 그림)
add(id="8e54d5fc", qtype="short",
    question="아래 그림과 같은 사다리꼴의 넓이를 [[a]]를 사용한 식으로 나타낼 때, 상수항을 구하시오.",
    choices=None, derived_answer="36",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴(파란색): 윗변 a cm, 아랫변 12 cm, 왼쪽 변(높이) 6 cm가 두 밑변에 수직(직각 표시 2개), 오른쪽 변은 빗변"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 치수가 표시된 사다리꼴",
    note="(a + 12)×6÷2 = 3a + 36 → 상수항 36. 빠른정답 4와 불일치.")

# p64 (사다리꼴 그림)
add(id="c63be07a", qtype="short",
    question="다음 그림과 같은 사다리꼴의 넓이를 [[a]]를 사용한 식으로 나타낼 때, 상수항을 구하시오.",
    choices=None, derived_answer="60",
    figure=[{"fn": "unsupported", "args": {"raw": "사다리꼴(보라색): 윗변 a, 아랫변 12, 오른쪽 변(높이) 10이 두 밑변에 수직(직각 표시 2개), 왼쪽 변은 빗변"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 치수가 표시된 사다리꼴",
    note="(a + 12)×10÷2 = 5a + 60 → 상수항 60. 빠른정답 42와 불일치.")

# ================= 등식의 성질 =================
# p11
add(id="52d05d6f", qtype="short",
    question="등식의 성질을 이용하여 다음 등식이 성립하도록 □ 안에 알맞은 수를 구하시오.\n[[5a + 15 = 5(b - 4)]]이면 [[a - 2 = b]] − □",
    choices=None, derived_answer="9", figure=None, difficulty_est=1, confidence=0.9,
    note="양변을 5로 나누면 a+3 = b−4, 양변에서 5를 빼면 a−2 = b−9 → 9 = 빠른정답 ✓. 빈칸 □는 텍스트.")

# p13
add(id="79394055", qtype="short",
    question="등식의 성질을 이용하여 다음 등식이 성립하도록 □ 안에 알맞은 수를 구하시오.\n[[2a + 6 = 2(b - 2)]]이면 [[a - 1 = b]] − □",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="a+3 = b−2 → a−1 = b−6 → 6 (빠른정답 없음). 빈칸 □는 텍스트.")

# p15
add(id="66ed65d8", qtype="short",
    question="[[a = b]]일 때, 다음 등식이 성립하도록 □ 안에 알맞은 수를 써넣으시오.\n[[a + 8 = b]] + □",
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="양변에 8을 더함 → 8 = 빠른정답 ✓. 빈칸 □는 텍스트.")

# p16
add(id="c7aba3f4", qtype="short",
    question="[[a = b]]일 때, 다음 등식이 성립하도록 □ 안에 알맞은 수를 써넣으시오.\n[[a + 13 = b]] + □",
    choices=None, derived_answer="13", figure=None, difficulty_est=1, confidence=0.9,
    note="양변에 13을 더함 → 13. 빠른정답 6과 불일치. 빈칸 □는 텍스트.")

# p18
add(id="2f31141c", qtype="short",
    question="[[a = b]]일 때, 다음 등식이 성립하도록 □ 안에 알맞은 수를 써넣으시오.\n[[-a + 4 = -b]] + □",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="−a+4 = −b+4 → 4. 빠른정답 8과 불일치. 빈칸 □는 텍스트.")

# p31
add(id="8815409c", qtype="choice",
    question="다음 중 옳지 않은 것은?",
    choices=["[[a c = b c]]이면 [[a = b]]이다.",
             "[[frac(a,5) = frac(b,4)]]이면 [[4a = 5b]]이다.",
             "[[a = b]]이면 [[a + c = b + c]]이다.",
             "[[3a = 3b]]이면 [[7 - a = 7 - b]]이다.",
             "[[frac(a,2) = frac(b,3)]]이면 [[frac(a - 4, 2) = frac(b - 6, 3)]]이다."],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="① c=0이면 성립하지 않음 → ① (빠른정답 없음).")

# p35 (양팔저울 그림)
add(id="ecf73a67", qtype="short",
    question=("다음 보기 중 아래 그림에서 알 수 있는 등식의 성질을 고르시오.\n<보기>\n"
              "ㄱ. [[a = b]]이면 [[a c = b c]]\n"
              "ㄴ. [[a = b]]이면 [[a + c = b + c]]\n"
              "ㄷ. [[a = b]]이면 [[a - c = b - c]]\n"
              "ㄹ. [[a = b]]이면 [[frac(a, c) = frac(b, c)]] (단, [[c != 0]])"),
    choices=None, derived_answer="ㄱ",
    figure=[{"fn": "unsupported", "args": {"raw": "양팔저울 그림 2개를 화살표(→)로 연결: 왼쪽 저울은 구슬 1개와 정육면체 블록 4개(2×2)가 평형, 오른쓱 저울은 구슬 2개와 블록 8개(2×4)가 평형"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 양팔저울 평형 그림",
    note="양쪽을 각각 2배 → 양변에 같은 수를 곱함 → ㄱ (빠른정답 없음).")

# p49 (풀이 과정 상자)
add(id="59b8e865", qtype="choice",
    question=("다음은 방정식의 해를 구하는 과정이다. ㉠ 과정에 이용된 등식의 성질을 고르면? (단, [[c >= 1]])\n"
              "[[frac(2x + 5, 3)]] = [[-1]]\n↓ ㉠\n[[2x + 5]] = [[-3]]\n↓ ㉡\n[[2x]] = [[-8]]\n↓ ㉢\n[[x]] = [[-4]]"),
    choices=["[[a = b]]이면 [[a + c = b + c]]이다.",
             "[[a = b]]이면 [[a - c = b - c]]이다.",
             "[[a = b]]이면 [[a c = b c]]이다.",
             "[[a = b]]이면 [[frac(a, c) = frac(b, c)]]이다.",
             "[[a = b]]이면 [[b = a]]이다."],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.85,
    note="㉠: 양변에 3을 곱함 → ③. 빠른정답 'x = 3'은 오정렬(해는 x=−4). 오정렬 빠른정답 대입 검산을 피하기 위해 과정의 등식은 '='를 마커 밖에 두었음(표시는 동일). 화살표 ㉠㉡㉢는 텍스트.")

# p53 (풀이 과정 상자, 원문자 답)
add(id="e551107c", qtype="short",
    question=("다음 등식의 성질을 이용하여 일차방정식 [[0.5x - 5 = frac(5,2) + 3x]]의 해를 구하는 과정이다. "
              "이때 등식의 성질 '[[a = b]]이면 [[a c = b c]]이다.'를 이용한 곳을 고르시오. (단, [[c]]는 자연수)\n"
              "[[0.5x - 5 = frac(5,2) + 3x]]\n↓ ㉠\n[[frac(1,2) x - 5 = frac(5,2) + 3x]]\n↓ ㉡\n[[x - 10 = 5 + 6x]]\n↓ ㉢\n"
              "[[x - 6x - 10 = 5]]\n↓ ㉣\n[[-5x = 5 + 10]]\n↓ ㉤\n[[-5x = 15]]"),
    choices=None, derived_answer=None, figure=None, difficulty_est=1, confidence=0.8,
    needs_review="답 표기 문법 범위 밖: 답은 원문자 ㉡(양변에 2를 곱한 곳)이나 답 문법에 원문자 없음",
    note="㉡에서 양변에 2를 곱함 → ㉡ (빠른정답 없음). 화살표 ㉠~㉤는 텍스트.")

# p54 (풀이 과정 상자, 원문자 답)
add(id="1ce3008b", qtype="short",
    question=("다음 방정식의 풀이 과정에서 등식의 성질 '[[a = b]]이면 [[frac(a, c) = frac(b, c)]]이다.'를 이용한 곳을 고르시오. (단, [[c]]는 자연수)\n"
              "[[frac(3,7) x + 2 = 5]]\n↓㉠\n[[3x + 14 = 35]]\n↓㉡\n[[3x = 21]]\n↓㉢\n∴ [[x = 7]]"),
    choices=None, derived_answer=None, figure=None, difficulty_est=1, confidence=0.8,
    needs_review="답 표기 문법 범위 밖: 답은 원문자 ㉢(양변을 3으로 나눈 곳)이나 답 문법에 원문자 없음",
    note="㉢에서 양변을 3으로 나눔 → ㉢ (빠른정답 없음). 화살표 ㉠~㉢는 텍스트.")

# p69
add(id="63ffa80c", qtype="choice",
    question="방정식 [[2x - 3 = 4]]에서 좌변의 [[-3]]을 이항한다는 것과 같은 뜻은?",
    choices=["양변에 [[-3]]을 더한다.", "양변에서 [[3]]을 뺀다.", "양변에 [[3]]을 더한다.", "양변에서 [[-3]]을 곱한다.", "양변을 [[3]]으로 나눈다."],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="−3 이항 = 양변에 3을 더함 → ③ (빠른정답 없음).")

# p83
add(id="ad374a5f", qtype="choice",
    question="다음 중 등식 [[7x - 2 = 9]]에서 밑줄 친 항을 이항한 것과 결과가 같은 것은? (밑줄 친 항: [[-2]])",
    choices=["양변에 [[2]]를 더한다.", "양변에 [[-2]]를 더한다.", "양변에서 [[2]]를 뺀다.", "양변을 [[2]]로 곱한다.", "양변에 [[2]]를 나눈다."],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="−2 이항 = 양변에 2를 더함 → ① (빠른정답 없음). 원문의 밑줄(−2 아래)은 괄호 주석으로 표시.")

# p87
add(id="dc05d54e", qtype="choice",
    question="다음 중 방정식 [[4 + 9x = -5]]에서 좌변의 [[4]]를 이항한 것과 같은 것은?",
    choices=["양변에 [[-4]]를 더한다.", "양변에 [[4]]를 더한다.", "양변에 [[-4]]를 곱한다.", "양변에 [[4]]를 곱한다.", "양변을 [[4]]로 나눈다."],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="4 이항 = 양변에 −4를 더함 → ① (빠른정답 없음).")

# p89
add(id="948ab93b", qtype="choice",
    question="등식 [[x + 6 = -6 - x]]를 이항만을 이용하여 [[a x = b]] ([[a > 0]])의 꼴로 나타내었을 때, 상수 [[a]], [[b]]에 대하여 [[a b]]의 값은?",
    choices=["[[-24]]", "[[-12]]", "[[-6]]", "[[12]]", "[[24]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="2x = −12 → ab = −24 → ① (빠른정답 없음).")

# p91
add(id="c396f3b9", qtype="short",
    question="방정식 [[5x - 3 = -6x + 4]]를 이항만을 이용하여 [[a x = b]] ([[a > 0]])의 꼴로 고쳤을 때, [[frac(a, b)]]의 값을 구하시오. (단, [[a]], [[b]]는 상수)",
    choices=None, derived_answer="frac(11,7)", figure=None, difficulty_est=1, confidence=0.9,
    note="11x = 7 → a/b = 11/7 = 빠른정답 ✓.")

# p95
add(id="2d51f155", qtype="choice",
    question="등식 [[6x - 8 = 3x + 16]]을 이항만을 이용하여 [[a x = b]] ([[a > 0]])의 꼴로 나타내었을 때, 상수 [[a]], [[b]]에 대하여 [[frac(b, a)]]의 값은?",
    choices=["[[frac(10,3)]]", "[[4]]", "[[frac(16,3)]]", "[[8]]", "[[frac(17,2)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="3x = 24 → b/a = 8 → ④ (빠른정답 없음).")

# p96
add(id="50981dd8", qtype="short",
    question="등식 [[4x + 1 = 2x - 5]]를 이항만을 이용하여 [[a x = b]] ([[a > 0]])의 꼴로 나타내었을 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="-4", figure=None, difficulty_est=1, confidence=0.9,
    note="2x = −6 → a+b = −4 = 빠른정답 ✓.")

# ================= 소인수분해 =================
# p4
add(id="70e76ebd", qtype="short",
    question="다음 □ 안에 알맞은 수를 써넣으시오.\n[[13 × 13 × 13 × 13 × 13]] = □⁵",
    choices=None, derived_answer="13", figure=None, difficulty_est=1, confidence=0.9,
    note="13⁵ → □ = 13. 빠른정답 4와 불일치. 빈칸 □와 지수 5는 텍스트.")

# p5
add(id="efb64792", qtype="short",
    question="다음 □ 안에 알맞은 수를 써넣으시오.\n[[17 × 17 × 17]] = [[17]]^□",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="17³ → □ = 3. 빠른정답 5와 불일치. 빈칸 □(지수 자리)는 텍스트.")

# p6
add(id="c0b58235", qtype="short",
    question="다음 □ 안에 알맞은 수를 써넣으시오.\n[[11 × 11 × 11]] = [[11]]^□",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="11³ → □ = 3. 빠른정답 4와 불일치. 빈칸 □(지수 자리)는 텍스트.")

# p9
add(id="87b97558", qtype="short",
    question="다음 □ 안에 알맞은 수를 써넣으시오.\n[[19 × 19 × 19 × 19 × 19]] = □⁵",
    choices=None, derived_answer="19", figure=None, difficulty_est=1, confidence=0.9,
    note="19⁵ → □ = 19. 빠른정답 3과 불일치. 빈칸 □와 지수 5는 텍스트.")

# p12
add(id="068f0ac6", qtype="short",
    question="다음 □ 안에 알맞은 수들의 합을 구하시오.\n[[5 × 5 × 5 × 5 × 11 × 11]] = [[5]]^□ × [[11]]^□",
    choices=None, derived_answer="6", figure=None, difficulty_est=1, confidence=0.9,
    note="5⁴ × 11² → 4 + 2 = 6. 빠른정답 19와 불일치. 빈칸 □(지수 자리)는 텍스트.")

# p60
add(id="fd60667e", qtype="choice",
    question=("자연수 [[n]]의 모든 소인수의 합을 〈[[n]]〉이라 하자. 예를 들어 〈[[10]]〉 = [[2 + 5 = 7]]이다. "
              "다음 중 〈[[n]]〉 = [[10]]을 만족시키는 [[n]]의 값이 될 수 없는 것은?"),
    choices=["[[21]]", "[[30]]", "[[36]]", "[[63]]", "[[90]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="21→3+7, 30→2+3+5, 63→3+7, 90→2+3+5는 10, 36=2²·3²→5 → ③. 빠른정답 40과 불일치. 기호 〈 〉는 텍스트.")

# p79
add(id="f8afc978", qtype="short",
    question="[[48 × a = pow(b, 2)]]을 만족시키는 [[a]], [[b]]가 모두 가장 작은 자연수가 되도록 할 때, [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="15", figure=None, difficulty_est=1, confidence=0.9,
    note="48 = 2⁴·3 → a=3, b=12 → 15. 빠른정답 5와 불일치.")

# ================= 공배수와 최소공배수 =================
# p34
add(id="08e5b56f", qtype="choice",
    question="다음 중 두 수 [[pow(2,2) × 3]], [[pow(2,3) × 3 × pow(5,2)]]의 최대공약수와 최소공배수를 차례로 구한 것은?",
    choices=["[[2 × 3]], [[pow(2,3) × 3 × pow(5,2)]]",
             "[[pow(2,2) × 3]], [[pow(2,3) × 3 × pow(5,2)]]",
             "[[pow(2,3) × 3]], [[pow(2,3) × pow(3,2) × pow(5,2)]]",
             "[[pow(2,2) × 3]], [[pow(2,3) × pow(3,2) × pow(5,2)]]",
             "[[2 × 3]], [[2 × 3 × 5]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="최대공약수 2²×3, 최소공배수 2³×3×5² → ②. 빠른정답 5와 불일치.")

# ================= 일차방정식의 풀이 =================
# p8
add(id="a0cd8e51", qtype="choice",
    question="다음 중 방정식 [[pow(x,2) + 6x + 2 = (2a - 1) pow(x,2) + b x + 7]]이 [[x]]에 대한 일차방정식이 되기 위한 조건은?\n(단, [[a]], [[b]]는 상수)",
    choices=["[[a != -1]], [[b = -6]]", "[[a = -1]], [[b = -6]]", "[[a != 1]], [[b != 6]]", "[[a = 1]], [[b != 6]]", "[[a != 1]], [[b = 6]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="이항하면 (2−2a)x² + (6−b)x − 5 = 0 → 이차항 소거 a=1, 일차항 b≠6 → ④. 빠른정답 1과 불일치.")

# p51
add(id="ea944d24", qtype="short",
    question="유리수 [[a]], [[b]]에 대하여 [[a]]◎[[b]] = [[a + 3b]]라 할 때,\n[[(3x + 1)]]◎[[(5 - x)]] = [[2x + 2]]를 만족시키는 [[x]]의 값을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.9,
    note="(3x+1) + 3(5−x) = 16 = 2x+2 → x = 7 = 빠른정답 ✓. 연산 기호 ◎는 텍스트.")

# p52 (id 3개)
dup(["c85a7c35", "7b2a6ce3", "4d00f70b"], qtype="short",
    question=("두 자연수 [[A]], [[B]]에 대하여\n[[A]]◇[[B]] = ([[A]]와 [[B]]의 최대공약수),\n[[A]]◆[[B]] = ([[A]]와 [[B]]의 최소공배수)로 나타내기로 하자.\n"
              "다음 조건을 만족시키는 [[x]], [[y]]에 대하여 [[x + y]]의 값을 구하시오.\n"
              "(가) [[8x]] − ([[12]]◇[[30]]) × [[x]] = [[x + 2]]\n(나) ([[6]]◆[[8]]) + [[4y]] = [[14 - y]]"),
    choices=None, derived_answer="0", figure=None, difficulty_est=2, confidence=0.9,
    note="12◇30=6: 8x−6x=x+2 → x=2. 6◆8=24: 24+4y=14−y → y=−2 → x+y=0 = 빠른정답 ✓. 연산 기호 ◇◆는 텍스트.")

# p53 (id 2개)
dup(["be4ab5cb", "f3cc30bb"], qtype="short",
    question=("두 자연수 [[A]], [[B]]에 대하여\n[[A]]◇[[B]] = ([[A]]와 [[B]]의 최대공약수),\n[[A]]◆[[B]] = ([[A]]와 [[B]]의 최소공배수)\n로 나타내기로 하자. "
              "다음 조건을 만족시키는 [[x]], [[y]]에 대하여 [[x + y]]의 값을 구하시오.\n"
              "(가) [[5x]] − ([[35]]◇[[56]]) × [[x]] = [[3x - 10]]\n(나) ([[12]]◆[[20]]) + [[7y]] = [[4 - y]]"),
    choices=None, derived_answer="-5", figure=None, difficulty_est=2, confidence=0.9,
    note="35◇56=7: 5x−7x=3x−10 → x=2. 12◆20=60: 60+7y=4−y → y=−7 → x+y=−5 = 빠른정답 'neg 5' ✓. 연산 기호 ◇◆는 텍스트.")

# p76
add(id="e0ee98da", qtype="short",
    question="[[x]]에 대한 일차방정식 [[a x - 2 = b x - 10]]의 해는 [[3x = 2(x + 1)]]의 해의 2배이다. 이때 [[a - b]]의 값을 구하시오. (단, [[a]], [[b]]는 상수)",
    choices=None, derived_answer="-2", figure=None, difficulty_est=2, confidence=0.9,
    note="3x=2x+2 → x=2, 해 4: 4a−2=4b−10 → a−b=−2 = 빠른정답 'neg 2' ✓.")

# p81
add(id="a7f4c512", qtype="choice",
    question="[[x]]에 대한 등식 [[a x + b = 0]]의 해가 존재하지 않기 위한 상수 [[a]], [[b]]의 조건은?",
    choices=["[[a = 0]], [[b = 0]]", "[[a = 0]], [[b != 0]]", "[[a != 0]], [[b = 0]]", "[[a != 0]], [[b != 0]]", "[[a != 0]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="해가 없으려면 a=0, b≠0 → ② = 빠른정답 ✓.")

# p84
add(id="6e45b732", qtype="choice",
    question="[[x]]에 대한 방정식 [[5x - b = a x + 1]]의 해가 없기 위한 상수 [[a]], [[b]]의 조건은?",
    choices=["[[a = 5]], [[b = -1]]", "[[a = 5]], [[b != -1]]", "[[a != 5]], [[b = -1]]", "[[a != 5]], [[b = 1]]", "[[a = 5]], [[b = 1]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="(5−a)x = 1+b: 해가 없으려면 a=5, b≠−1 → ② = 빠른정답 ✓.")

# p87
add(id="30b95bb0", qtype="choice",
    question="방정식 [[(a - 3) x + 5 = 3]]의 해는 없고, 방정식 [[b x + 2 = c]]의 해는 무수히 많을 때, [[a + b + c]]의 값은?\n(단, [[a]], [[b]], [[c]]는 상수)",
    choices=["[[5]]", "[[6]]", "[[7]]", "[[8]]", "[[9]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="a=3, b=0, c=2 → 5 → ①. 빠른정답 2와 불일치.")

# p88
add(id="f700b488", qtype="choice",
    question=("[[x]]에 대한 방정식 [[4(x - a) = 16 b x + 1]]의 해가 무수히 많을 때, "
              "[[frac(1,a) + frac(b, pow(a,2)) + frac(pow(b,2), pow(a,3))]] + ⋯ + [[frac(pow(b,14), pow(a,15))]]의 값은?\n(단, [[a]], [[b]]는 상수)"),
    choices=["[[-4]]", "[[-2]]", "[[0]]", "[[2]]", "[[4]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="b=1/4, a=−1/4, b/a=−1, 1/a=−4: 15항 교대합 (−4)(1−1+…+1)=−4 → ①. 빠른정답 2와 불일치. 줄임표는 텍스트.")

# p89
add(id="c77b6476", qtype="choice",
    question=("[[x]]에 대한 방정식 [[2(x - a) = 4 b x + 1]]의 해가 무수히 많을 때, "
              "[[frac(1,a) + frac(b, pow(a,2)) + frac(pow(b,2), pow(a,3))]] + ⋯ + [[frac(pow(b,19), pow(a,20))]]의 값은? (단, [[a]], [[b]]는 상수)"),
    choices=["[[-1]]", "[[0]]", "[[1]]", "[[2]]", "[[3]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="b=1/2, a=−1/2, b/a=−1, 1/a=−2: 20항 교대합 0 → ②. 빠른정답 'neg 8'과 불일치. 줄임표는 텍스트.")

# p90
add(id="7ec81d0c", qtype="choice",
    question=("[[x]]에 대한 방정식 [[3(x - a) = 9 b x + 1]]의 해가 무수히 많을 때, "
              "[[frac(1,a) + frac(b, pow(a,2)) + frac(pow(b,2), pow(a,3))]] + ⋯ + [[frac(pow(b,9), pow(a,10))]]의 값은? (단, [[a]], [[b]]는 상수)"),
    choices=["[[-3]]", "[[-1]]", "[[0]]", "[[1]]", "[[3]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="b=1/3, a=−1/3, b/a=−1, 1/a=−3: 10항 교대합 0 → ③. 빠른정답 1과 불일치. 줄임표는 텍스트.")

# ================= 덧셈, 뺄셈, 곱셈, 나눗셈의 혼합 계산 =================
# p4
add(id="4ff26702", qtype="choice",
    question=("다음 보기의 계산에서 (가), (나), (다)에 이용된 계산법칙이 순서대로 올바르게 짝 지어진 것은?\n<보기>\n"
              "[[(-3) × 12 + (-4) + (-7) × 12 + (-6)]]\n"
              "= [[(-3) × 12 + (-7) × 12 + (-4) + (-6)]] ⋯ (가)\n"
              "= {[[(-3) + (-7)]]} × [[12 + (-4) + (-6)]] ⋯ (나)\n"
              "= [[-120 + (-4) + (-6)]]\n"
              "= [[-120]] + {[[(-4) + (-6)]]} ⋯ (다)\n"
              "= [[-130]]"),
    choices=["(가) 덧셈의 교환법칙, (나) 분배법칙, (다) 덧셈의 결합법칙",
             "(가) 덧셈의 결합법칙, (나) 분배법칙, (다) 덧셈의 교환법칙",
             "(가) 곱셈의 교환법칙, (나) 분배법칙, (다) 덧셈의 결합법칙",
             "(가) 덧셈의 교환법칙, (나) 덧셈의 결합법칙, (다) 분배법칙",
             "(가) 덧셈의 결합법칙, (나) 덧셈의 교환법칙, (다) 분배법칙"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.85,
    note="(가) 항 순서 바꿈=덧셈의 교환법칙, (나) 분배법칙, (다) 묶음=덧셈의 결합법칙 → ①. 빠른정답 4와 불일치. 화살표 (가)(나)(다)는 해당 줄 끝에 텍스트로, 중괄호는 텍스트.")

# p8
add(id="5c4ef324", qtype="choice",
    question=("다음 계산 과정에서 처음으로 틀린 곳은?\n"
              "[[-pow(6, 2)]] + {[[pow(3, 2)]] − (+3)² × 6} ÷ 3\n"
              "= [[-36 + (9 - 9 × 6) ÷ 3]] ⋯ ㉠\n"
              "= [[-36 + (9 - 54) ÷ 3]] ⋯ ㉡\n"
              "= [[-36 + (-45) ÷ 3]] ⋯ ㉢\n"
              "= [[-81 ÷ 3]] ⋯ ㉣\n"
              "= [[-27]] ⋯ ㉤"),
    choices=["㉠", "㉡", "㉢", "㉣", "㉤"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="㉣: −36+(−45)÷3 = −36+(−15) = −51인데 −81÷3으로 먼저 더함 → ④. 빠른정답 2와 불일치. 양의 부호 (+3)², 중괄호, 화살표 ㉠~㉤은 텍스트.")

# p14 (연산 순서 화살표 그림)
add(id="16cc0ee6", qtype="choice",
    question=("다음 식을 계산할 때, 세 번째로 계산해야 할 것은?\n"
              "[[5 - 24]] ÷ [{[[pow(-3, 2) + (-5)]]} × [[2]]]\n"
              "(화살표 ㉠: −, ㉡: ÷, ㉢: 거듭제곱, ㉣: +, ㉤: ×)"),
    choices=["㉠", "㉡", "㉢", "㉣", "㉤"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "식 아래 위쪽 화살표 5개: ㉠→5−24의 −, ㉡→÷, ㉢→(−3)²의 지수 2, ㉣→+, ㉤→×"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 식의 연산 기호를 가리키는 화살표 ㉠~㉤",
    note="순서 ㉢(거듭제곱)→㉣(+)→㉤(×)→㉡(÷)→㉠(−) → 세 번째 ㉤ → ⑤ = 빠른정답 ✓. 대괄호·중괄호는 텍스트.")

# p15 (연산 순서 화살표 그림)
add(id="e0076f62", qtype="choice",
    question=("다음 식에서 3번째로 계산해야 하는 것은?\n"
              "[[-4 + 28]] ÷ {(+3) − [[pow(-2, 2)]]} × [[4]]\n"
              "(화살표 ㉠: +, ㉡: ÷, ㉢: −, ㉣: 거듭제곱, ㉤: ×)"),
    choices=["㉠", "㉡", "㉢", "㉣", "㉤"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "식 아래 위쪽 화살표 5개: ㉠→−4+28의 +, ㉡→÷, ㉢→중괄호 안의 −, ㉣→(−2)²의 지수 2, ㉤→×. (−2)²에 밑줄"}}],
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 식의 연산 기호를 가리키는 화살표 ㉠~㉤",
    note="순서 ㉣(거듭제곱)→㉢(−)→㉡(÷)→㉤(×)→㉠(+) → 세 번째 ㉡ → ②. 빠른정답 4와 불일치. 양의 부호 (+3)·중괄호는 텍스트.")

# p25
add(id="a0ac6659", qtype="short",
    question="다음 □ 안에 알맞은 수를 구하시오.\n[[(-frac(3,2))]] × □ ÷ [[(frac(1,3) - frac(5,6))]] = [[-1]]",
    choices=None, derived_answer="-frac(1,3)", figure=None, difficulty_est=2, confidence=0.9,
    note="1/3−5/6=−1/2 → (−3/2)×□×(−2)=3□=−1 → □=−1/3 = 빠른정답 ✓. 빈칸 □는 텍스트.")

# p27
add(id="79c3530a", qtype="short",
    question="다음 □ 안에 알맞은 수를 구하시오.\n[[(-frac(2,3))]] × □ ÷ [[(frac(1,2) - frac(1,3))]] = [[2]]",
    choices=None, derived_answer="-frac(1,2)", figure=None, difficulty_est=2, confidence=0.9,
    note="1/2−1/3=1/6 → (−2/3)×□×6=−4□=2 → □=−1/2 = 빠른정답 ✓. 빈칸 □는 텍스트.")

# p31
add(id="dc686ced", qtype="short",
    question="[[(frac(1,2) - 1) × (frac(1,3) - 1) × (frac(1,4) - 1)]] × ⋯ × [[(frac(1,15) - 1)]]을 계산하시오.",
    choices=None, derived_answer="frac(1,15)", figure=None, difficulty_est=2, confidence=0.9,
    note="(−1/2)(−2/3)⋯(−14/15): 음수 14개 곱 → +1/15 = 빠른정답 ✓. 줄임표는 텍스트.")
