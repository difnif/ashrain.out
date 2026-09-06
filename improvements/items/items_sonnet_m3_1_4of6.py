# -*- coding: utf-8 -*-
# esc_sonnet_m3-1_4of6 — 이미지 기준 전사 (81 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))
def U(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]
FIG = "도형 표현 불가: "

# ======================= 인수분해를 이용한 이차방정식의 풀이 =======================
# p85
add(id="ec7df17f", qtype="short",
    question=("이차방정식 [[2 pow(x,2) - 7x = -3]]의 두 근 중 큰 근은 이차방정식 [[pow(x,2) + (m + 2) x + (m - 3) = 0]]의 근이고 "
              "작은 근은 이차방정식 [[2 pow(x,2) + n x - 1 = 0]]의 근일 때, [[m - n]]의 값을 구하시오. (단, [[m]], [[n]]은 상수이다.)"),
    choices=None, derived_answer="-4", figure=None, difficulty_est=2,
    note="2x²−7x+3=0 → x=3, 1/2. x=3 대입 → 4m+12=0, m=−3; x=1/2 대입 → n=1 → m−n=−4 (빠른정답 'neg 4'와 같은 값).")

# p91
add(id="c702b0ba", qtype="choice",
    question=("[[x]]에 대한 이차방정식 [[3 pow(x,2) - 4k x + pow(k,2) = 0]]에서 [[x]]의 계수와 상수항을 바꾸어 풀면 한 근이 [[x = -frac(4,3)]]이다. "
              "처음 주어진 이차방정식의 근이 모두 음수가 되도록 하는 실수 [[k]]의 값은?"),
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    derived_answer="②", figure=None, difficulty_est=3,
    note="바꾼 식 3x²+k²x−4k=0에 x=−4/3 대입 → k²+3k−4=0 → k=−4 또는 1. 원식 근 k/3, k가 모두 음수 → k=−4 → ② = 빠른정답 ✓.")

# p92
add(id="567dee78", qtype="choice",
    question=("[[x]]에 대한 이차방정식 [[4 pow(x,2) - 5k x + pow(k,2) = 0]]에서 [[x]]의 계수와 상수항을 바꾸어 풀면 한 근이 [[x = -frac(5,4)]]이다. "
              "처음 주어진 이차방정식의 근이 모두 음수가 되도록 하는 실수 [[k]]의 값은?"),
    choices=["[[-5]]", "[[-4]]", "[[-3]]", "[[-2]]", "[[-1]]"],
    derived_answer="①", figure=None, difficulty_est=3,
    note="바꾼 식 4x²+k²x−5k=0에 x=−5/4 대입 → k²+4k−5=0 → k=−5 또는 1. 원식 근 k/4, k가 모두 음수 → k=−5 → ①. 빠른정답 5와 불일치.")

# p99 (이미지에 별개 문항 2개, id 1개 → draft_a 대응인 아래쪽 선택형 문항 전사)
add(id="8f0caeab", qtype="choice",
    question=("이차방정식 [[pow(x,2) - x - 6 = 0]]의 두 근 중 작은 근이 이차방정식 [[2 pow(x,2) + b x - 2 = 0]]의 근이라고 할 때, [[b]]의 값은?"),
    choices=["[[-3]]", "[[-1]]", "[[1]]", "[[2]]", "[[3]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.75,
    needs_review="이미지에 별개 문항 2개 인쇄(id 1개) — draft_a 대응인 아래쪽 선택형 문항만 전사; 위쪽 문항 '이차방정식 2x²−13x+15=0의 두 근 중에서 큰 근이 3x²−11x+a=0의 근이라 할 때, a의 값을 구하시오.'(답 −20)는 미전사",
    note="x²−x−6=0 → x=3, −2; 작은 근 −2 대입 → 8−2b−2=0 → b=3 → ⑤. 빠른정답 1과 불일치.")

# ======================= 이차함수 y=ax²+bx+c의 그래프 =======================
# p2 (틀린 곳 찾기 — 답 기호 ㉢은 answer 문법 밖)
add(id="3b755ae4", qtype="short",
    question=("[[y = 2 pow(x,2) + 4x - 1]]을 [[y = a pow(x - p, 2) + q]]의 꼴로 고치는 과정 중 처음 틀린 곳을 찾으시오.\n"
              "[[y = 2 pow(x,2) + 4x - 1]]\n"
              "= [[2(pow(x,2) + 2x) - 1]] ⋯㉠\n"
              "= [[2(pow(x,2) + 2x + 1 - 1) - 1]] ⋯㉡\n"
              "= [[2 pow(x + 1, 2) - 3 - 1]] ⋯㉢\n"
              "= [[2 pow(x + 1, 2) - 4]] ⋯㉣"),
    choices=None, derived_answer=None, figure=None, difficulty_est=2, confidence=0.75,
    needs_review="문법 범위 밖: 답 '㉢'(원문자 기호)은 answer 문법에서 허용되지 않아 미기입",
    note="㉢에서 2(x+1)²−2−1이어야 하는데 −3−1로 씀 → 처음 틀린 곳 ㉢. 빠른정답 5와 불일치.")

# p6
add(id="701e3246", qtype="choice",
    question=("다음은 이차함수 [[y = -2 pow(x,2) + 12x - 3]]을 [[y = a pow(x - p, 2) + q]] 꼴로 변형하는 과정이다. (가)~(마)에 알맞은 수가 아닌 것은?\n"
              "[[y = -2 pow(x,2) + 12x - 3]]\n"
              "= −2([[pow(x,2)]] − (가) [[x]]) − 3\n"
              "= −2([[pow(x,2)]] − (가) [[x]] + (나) − (나)) − 3\n"
              "= −2([[x]] − (다))² + (라) − 3\n"
              "= −2([[x]] − (다))² + (마)"),
    choices=["(가) [[6]]", "(나) [[9]]", "(다) [[3]]", "(라) [[9]]", "(마) [[15]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="(가)6 (나)9 (다)3 (라)18 (마)15 → (라)가 틀림 → ④. 빠른정답 −12와 불일치. 빈칸 상자는 텍스트 조각으로 전사.")

# p14
add(id="8978cc4f", qtype="short",
    question=("이차함수 [[y = a pow(x,2) + 4a x + pow(a,2) + 10a + 10]]의 그래프의 꼭짓점의 좌표가 [[point(-2, 1)]]일 때, 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="-3", figure=None, difficulty_est=2,
    note="축 x=−2는 항상 성립, y(−2)=a²+6a+10=1 → (a+3)²=0 → a=−3 = 빠른정답 ✓.")

# p16
add(id="fe9afd72", qtype="short",
    question=("이차함수 [[y = pow(x,2) - 2a x + 1]]의 그래프와 [[y = 3 pow(x,2) - 12x + b]]의 그래프의 꼭짓점이 일치할 때, "
              "상수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="11", figure=None, difficulty_est=2,
    note="꼭짓점 (a, 1−a²)와 (2, b−12) 일치 → a=2, b=9 → 11. 빠른정답 5와 불일치.")

# p27
add(id="17e6406a", qtype="choice",
    question=("이차함수 [[y = -2 pow(x,2) + 4x]]의 그래프와 [[x]]축과의 교점의 [[x]]좌표를 [[a]], [[y]]축과의 교점의 [[y]]좌표를 [[b]]라 할 때, "
              "[[a]]와 [[b]]의 값을 구하면?"),
    choices=["[[a = -2]] 또는 [[0]], [[b = 0]]",
             "[[a = -5]] 또는 [[-1]], [[b = -5]]",
             "[[a = -1]] 또는 [[-3]], [[b = frac(3,2)]]",
             "[[a = 1]] 또는 [[5]], [[b = 5]]",
             "[[a = 0]] 또는 [[2]], [[b = 0]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="−2x(x−2)=0 → a=0 또는 2, b=0 → ⑤ = 빠른정답 ✓.")

# p28
add(id="ce15a190", qtype="choice",
    question=("다음은 이차함수 [[y = -2 pow(x,2) + x + 1]]의 그래프에서 [[x]]축과의 두 교점 A, B의 좌표를 구하는 과정이다. "
              "ⓐ~ⓔ에 알맞은 수를 바르게 짝 지은 것은?\n"
              "[[y = -2 pow(x,2) + x + 1]]에 [[y = 0]]을 대입하면\n"
              "[[-2 pow(x,2) + x + 1 = 0]], ([[2x]] + ⓐ)([[x - 1]]) = 0\n"
              "∴ [[x]] = ⓑ 또는 [[x]] = ⓒ\n"
              "∴ A(ⓓ, 0), B(ⓔ, 0)"),
    choices=["ⓐ [[-1]]", "ⓑ [[-frac(1,2)]]", "ⓒ [[frac(1,2)]]", "ⓓ [[-1]]", "ⓔ [[frac(1,2)]]"],
    derived_answer="②",
    figure=U("좌표평면: 위로 볼록한 포물선 y=−2x²+x+1, x축과의 두 교점 A(y축 왼쪽)·B(y축 오른쪽), 원점 O"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG + "이차함수 그래프",
    note="(2x+1)(x−1)=0 → ⓐ1, ⓑ−1/2, ⓒ1, ⓓ−1/2, ⓔ1 → 옳은 짝 ②. 빠른정답 3과 불일치. 빈칸 상자는 텍스트 조각.")

# p29
add(id="888ccb75", qtype="choice",
    question=("이차함수 [[y = a pow(x,2) + b x + c]]의 그래프는 [[x]]축과 두 점 A, B에서 만나고 [[seg(AB) = 6]]이다. "
              "꼭짓점의 좌표가 [[point(-1, 18)]]일 때, 이 이차함수의 그래프와 [[y]]축의 교점의 좌표는?"),
    choices=["[[point(0, 10)]]", "[[point(0, 12)]]", "[[point(0, 14)]]", "[[point(0, 16)]]", "[[point(0, 18)]]"],
    derived_answer="④", figure=None, difficulty_est=3,
    note="y=a(x+1)²+18, x절편 −1±3 → 9a+18=0, a=−2 → y절편 16 → ④. 빠른정답 1과 불일치.")

# p35
add(id="ce847a38", qtype="choice",
    question=("다음 그림과 같이 이차함수 [[y = -pow(x,2) + 6x + k]]의 그래프의 꼭짓점을 A, [[x]]축과의 교점 중 [[x]]좌표가 음수인 점을 B라 하고, "
              "[[seg(AB)]]와 [[y]]축의 교점을 C라 하자. [[ratio(seg(AC), seg(CB)) = ratio(1, 2)]]일 때, 상수 [[k]]의 값은?"),
    choices=["[[60]]", "[[64]]", "[[68]]", "[[72]]", "[[76]]"],
    derived_answer="④",
    figure=U("좌표평면: 위로 볼록한 포물선(꼭짓점 A가 제1사분면), x축과의 왼쪽 교점 B(음수), 선분 AB가 y축과 만나는 점 C, 원점 O"),
    difficulty_est=3, confidence=0.85,
    needs_review=FIG + "이차함수 그래프와 선분",
    note="A(3, 9+k), C가 AB를 1:2로 내분 → xB=−6 → −36−36+k=0 → k=72 → ④ = 빠른정답 ✓.")

# p36
add(id="95d4416f", qtype="choice",
    question=("다음 그림과 같이 이차함수 [[y = -pow(x,2) + 2x + k]]의 그래프의 꼭짓점을 A, [[x]]축과의 교점 중 [[x]]좌표가 음수인 점을 B라 하고 "
              "[[seg(AB)]]와 [[y]]축의 교점을 C라 하자. [[ratio(seg(AC), seg(CB)) = ratio(1, 3)]]일 때, 상수 [[k]]의 값은?"),
    choices=["[[9]]", "[[12]]", "[[15]]", "[[18]]", "[[21]]"],
    derived_answer="③",
    figure=U("좌표평면: 위로 볼록한 포물선(꼭짓점 A가 제1사분면), x축과의 왼쪽 교점 B(음수), 선분 AB가 y축과 만나는 점 C, 원점 O"),
    difficulty_est=3, confidence=0.85,
    needs_review=FIG + "이차함수 그래프와 선분",
    note="A(1, 1+k), C가 AB를 1:3으로 내분 → xB=−3 → −9−6+k=0 → k=15 → ③. 빠른정답 6과 불일치.")

# p46
add(id="0ad4e13a", qtype="choice",
    question=("이차함수 [[y = -4 pow(x,2) + k x - 3]]의 그래프가 점 [[point(-1, -15)]]를 지날 때, 이 그래프의 꼭짓점의 좌표는? (단, [[k]]는 상수)"),
    choices=["[[point(-4, -1)]]", "[[point(-2, 1)]]", "[[point(1, 1)]]", "[[point(1, 4)]]", "[[point(4, 1)]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="−4−k−3=−15 → k=8; y=−4(x−1)²+1 → (1, 1) → ③ = 빠른정답 ✓.")

# p52
add(id="0f9ee0f0", qtype="short",
    question=("주사위를 세 번 던져서 나타나는 수를 차례대로 [[a]], [[b]], [[c]]라 할 때, 이차함수 [[y = a pow(x,2) + b x - 5c]]의 그래프가 점 [[point(1, 0)]]을 지나고 "
              "꼭짓점의 [[x]]좌표가 [[-2]]가 될 확률을 구하시오."),
    choices=None, derived_answer="frac(1,216)", figure=None, difficulty_est=3,
    note="a+b=5c, b=4a → a=c, b=4a → (1,4,1)뿐 → 1/216 = 빠른정답 ✓.")

# p54
add(id="69cce58d", qtype="choice",
    question=("이차함수 [[y = 3 pow(x,2) - a x + 16]]의 그래프가 점 [[point(1, 1)]]을 지날 때, 이 그래프의 축의 방정식은? (단, [[a]]는 상수)"),
    choices=["[[x = 1]]", "[[x = 2]]", "[[x = 3]]", "[[x = 4]]", "[[x = 5]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="3−a+16=1 → a=18, 축 x=18/6=3 → ③ = 빠른정답 ✓.")

# p55
add(id="82385ad3", qtype="choice",
    question=("이차함수 [[y = 2 pow(x,2) - 4a x + 3b]]의 그래프가 점 [[point(-1, 3)]]을 지나고 꼭짓점이 직선 [[y = -x - 1]] 위에 있을 때, "
              "상수 [[a]], [[b]]에 대하여 [[a + b]]의 값은? (단, [[a > 0]])"),
    choices=["[[frac(1,6)]]", "[[frac(1,5)]]", "[[frac(1,4)]]", "[[frac(1,3)]]", "[[frac(1,2)]]"],
    derived_answer="①", figure=None, difficulty_est=3,
    note="4a+3b=1, 꼭짓점 (a, −2a²+3b)가 y=−x−1 위 → 2a²+3a−2=0 → a=1/2, b=−1/3 → a+b=1/6 → ① = 빠른정답 ✓.")

# p70
add(id="18bb1e36", qtype="short",
    question=("이차함수 [[y = pow(x,2) - 8x + 4]]의 그래프에 대하여 다음 □ 안에 알맞은 것을 쓰시오.\n"
              "[[x < 4]]일 때, [[x]]의 값이 증가하면 [[y]]의 값은 □한다."),
    choices=None, derived_answer="감소", figure=None, difficulty_est=1,
    note="y=(x−4)²−12, 축 x=4 왼쪽에서 감소 → '감소'. 빠른정답 2와 불일치.")

# p86 (문항·선지 모두 그래프 그림)
add(id="7619c8af", qtype="choice",
    question=("[[y = -pow(x,2) + b x + c]]의 그래프가 다음 그림과 같을 때, 다음 중 [[y = pow(x,2) + c x + b]]의 그래프는?"),
    choices=["(그래프) 아래로 볼록, 축이 [[y]]축이고 꼭짓점이 [[x]]축 아래(원점 아래)인 포물선",
             "(그래프) 아래로 볼록, 꼭짓점이 [[x]]축 위의 점([[x > 0]])이고 [[y]]절편이 양수인 포물선",
             "(그래프) 위로 볼록, 축이 [[y]]축 오른쪽에 있고 원점 부근에서 [[x]]축과 만나는 포물선",
             "(그래프) 아래로 볼록, 꼭짓점이 제3사분면에 있고 원점을 지나는 포물선",
             "(그래프) 아래로 볼록, 축이 [[y]]축이고 꼭짓점이 [[x]]축 위쪽([[y]]절편 양수)인 포물선"],
    derived_answer=None,
    figure=U("좌표평면: 위로 볼록한 포물선 y=−x²+bx+c, 축이 y축 오른쪽, 원점 O를 지나는 것으로 보임(왼쪽 x절편이 O). 선지 ①~⑤는 포물선 그림(선지 텍스트에 서술)"),
    difficulty_est=3, confidence=0.75,
    needs_review=FIG + "문항·선지 5개가 모두 이차함수 그래프 그림(선지는 텍스트 서술)",
    note="b>0. 그림상 원점을 지나면 c=0 → y=x²+b(축 y축, 꼭짓점 위) → ⑤; y절편이 음수(c<0)로 보면 축 x>0·y절편 양수 → ②. 그림 판독이 갈려 답 미도출. 빠른정답 2.")

# p87
add(id="2162744b", qtype="short",
    question=("[[a > 0]], [[b > 0]], [[c > 0]]일 때,\n이차함수 [[y = a pow(x,2) + b x + c]]의 그래프가 항상 지나지 않는 사분면을 구하시오."),
    choices=None, derived_answer="제4사분면", figure=None, difficulty_est=2,
    note="x>0이면 y>0 → 제4사분면을 지나지 않음 = 빠른정답 ✓.")

# p90
add(id="ee1a25b9", qtype="choice",
    question=("포물선 [[y = -2 pow(x,2) - b x + c]]에서 [[b < 0]], [[c > 0]]이면 꼭짓점은 제 몇 사분면 위에 있는가?"),
    choices=["원점", "제1사분면", "제2사분면", "제3사분면", "제4사분면"],
    derived_answer="②", figure=None, difficulty_est=2,
    note="꼭짓점 x=−b/4>0, y=c+b²/8>0 → 제1사분면 → ②. 빠른정답 '제4사분면'과 불일치.")

# p97
add(id="aa3ba3ab", qtype="choice",
    question=("두 이차함수 [[f(x) = a pow(x,2) - 4a x + 3a + 1]], [[g(x) = -2 pow(x,2) - 4a x]]의 그래프의 꼭짓점을 각각 A, B라 하자. "
              "이차함수 [[y = f(x)]]의 그래프가 [[y]]축과 만나는 점 C에 대하여 사각형 OACB의 넓이가 4일 때, 양수 [[a]]의 값은? (단, O는 원점이다.)"),
    choices=["[[frac(1,6)]]", "[[frac(1,3)]]", "[[frac(1,2)]]", "[[frac(2,3)]]", "[[frac(5,6)]]"],
    derived_answer="④",
    figure=U("좌표평면: 아래로 볼록한 y=f(x)(꼭짓점 A가 제1사분면, y절편 C), 위로 볼록한 y=g(x)(원점 O를 지나고 꼭짓점 B가 제2사분면), 사각형 OACB의 변 OA·AC·CB·BO"),
    difficulty_est=4, confidence=0.85,
    needs_review=FIG + "두 이차함수 그래프와 사각형",
    note="출처 [2023년 3월 고1 17번 변형]. A(2, 1−a), B(−a, 2a²), C(0, 3a+1); 넓이=½(3a+1)(2+a)=4 → 3a²+7a−6=0 → a=2/3 → ④ = 빠른정답 ✓.")

# ======================= 실수의 대소 관계 =======================
# p2
add(id="61744724", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 한 변의 길이가 1인 정사각형이고, [[seg(AC) = seg(AP)]]이다. "
              "점 P에 대응하는 수를 [[a + sqrt(b)]]라고 할 때, 유리수 [[a]], [[b]]의 곱 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="-6",
    figure=U("수직선(눈금 −3, −2, −1) 위에 정사각형 ABCD(A가 −3, B가 −2, D·C는 위쪽), 대각선 AC, A를 중심으로 C를 지나는 호가 수직선과 만나는 점 P(−2와 −1 사이)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG + "수직선 위 정사각형과 호",
    note="AC=√2, P=−3+√2 → a=−3, b=2 → ab=−6 = 빠른정답 ✓.")

# p11
add(id="e6a08cf1", qtype="choice",
    question=("다음 그림과 같이 넓이가 각각 5, 10인 두 정사각형 ABCD, EFGH의 점 B, F가 수직선 위의 점 [[-1]], 7에 놓여 있다. "
              "[[seg(BC) = seg(BP)]], [[seg(FE) = seg(FQ)]]일 때, 점 P, Q에 대응하는 수를 차례로 나열한 것은?"),
    choices=["[[-1 - sqrt(5)]], [[7 - sqrt(10)]]",
             "[[-1 + sqrt(5)]], [[7 - sqrt(10)]]",
             "[[-1 - sqrt(5)]], [[7 + sqrt(10)]]",
             "[[1 + sqrt(5)]], [[7 + sqrt(10)]]",
             "[[1 - sqrt(5)]], [[7 + sqrt(10)]]"],
    derived_answer="②",
    figure=U("수직선 위에 마름모꼴로 놓인 두 정사각형: ABCD(B가 −1, 넓이 5)와 EFGH(F가 7, 넓이 10). B 중심으로 C를 지나는 호가 오른쪽 점 P, F 중심으로 E를 지나는 호가 왼쪽 점 Q와 만남"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG + "수직선 위 정사각형 2개와 호",
    note="BC=√5 → P=−1+√5, FE=√10 → Q=7−√10 → ② = 빠른정답 ✓.")

# p12
add(id="b8111c20", qtype="choice",
    question=("다음 그림에서 사각형 ABCD는 한 변의 길이가 1인 정사각형이다. 점 P에 대응하는 수가 [[5 - 3 sqrt(2)]]이고 "
              "[[seg(AC) = seg(AQ)]], [[seg(DB) = seg(BP)]]일 때, 점 Q에 대응하는 수는?"),
    choices=["[[5 - sqrt(2)]]", "[[5 - 2 sqrt(2)]]", "[[4 - sqrt(2)]]", "[[4 - 2 sqrt(2)]]", "[[3 - 2 sqrt(2)]]"],
    derived_answer="③",
    figure=U("수직선 위 정사각형 ABCD(A·B가 수직선 위, D·C 위쪽), 대각선 AC·BD. B 중심으로 D를 지나는 호가 왼쪽 점 P, A 중심으로 C를 지나는 호가 오른쪽 점 Q와 만남"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG + "수직선 위 정사각형과 호",
    note="B=P+√2=5−2√2, A=4−2√2, Q=A+√2=4−√2 → ③ = 빠른정답 ✓.")

# p13
add(id="8d875483", qtype="choice",
    question=("아래 그림과 같이 수직선 위에 한 변의 길이가 1인 정사각형 ABCD를 그렸다. [[seg(BD) = seg(BP)]]가 되도록 수직선 위에 점 P를 정할 때, "
              "세 점 P, A, B에 대응하는 수를 각각 [[p]], [[a]], [[b]]라 하자. 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[p]]가 유리수이면 [[a]], [[b]]는 유리수이다.\n"
              "ㄴ. [[p]]가 무리수이면 [[a]]는 무리수이다.\n"
              "ㄷ. [[b]]가 유리수이면 [[p]]는 무리수이다."),
    choices=["ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"],
    derived_answer="②",
    figure=U("수직선 위 정사각형 ABCD(A·B가 수직선 위, D·C 위쪽, 대각선 표시), B 중심으로 D를 지나는 호가 A 왼쪽의 점 P와 만남"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG + "수직선 위 정사각형과 호",
    note="p=b−√2, a=b−1. ㄱ✗(b=p+√2 무리수), ㄴ✗(p=1−√2이면 a=0), ㄷ✓ → ② = 빠른정답 ✓.")

# p14
add(id="a5bde763", qtype="choice",
    question=("다음 그림과 같이 한 눈금의 길이가 1인 모눈종이 위에 수직선과 [[tri(ABC)]]를 그리고 [[seg(AB) = seg(PB)]], [[seg(CB) = seg(QB)]]가 되도록 "
              "수직선 위에 두 점 P, Q를 정할 때, 두 점의 좌표 [[P(a)]], [[Q(b)]]의 좌표에 대하여 [[b - a]]의 값은? (단, [[a]], [[b]]는 상수)"),
    choices=["[[1 + sqrt(5)]]", "[[2 + sqrt(5)]]", "[[sqrt(5) + sqrt(10)]]", "[[1 + sqrt(10)]]", "[[2 + sqrt(10)]]"],
    derived_answer="③",
    figure=U("모눈종이 위 수직선(눈금 1~8), 삼각형 ABC: A(2, 1), C(7, 1), B(5, 0)(수직선 위). B 중심 호로 A→P(2 부근 왼쪽), C→Q(7 부근 오른쪽)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG + "모눈종이 위 삼각형과 호",
    note="AB=√10, CB=√5 → a=5−√10, b=5+√5 → b−a=√5+√10 → ③. 빠른정답 2와 불일치.")

# p49 (기호 <a, b>는 텍스트)
add(id="defa43ac", qtype="short",
    question=("자연수의 양의 제곱근 1, [[sqrt(2)]], [[sqrt(3)]], 2, ⋯에 대응하는 점을 수직선 위에 다음 그림과 같이 차례대로 나타낸다. "
              "아래 수직선에서 [[a]], [[b]] 사이에 있는 점의 개수를 <[[a]], [[b]]>라 하면 <1, 2> = 2, <2, 3> = 4이다. "
              "이때 <2000, 2001>의 값을 구하시오."),
    choices=None, derived_answer="4000",
    figure=U("수직선 위에 점 1, √2, √3, 2, √5, √6, √7, √8, 3이 차례로 찍혀 있음(√6, √8은 위쪽에 표기)"),
    difficulty_est=2, confidence=0.8,
    needs_review="문법 범위 밖: 약속 기호 <a, b>(사이 점의 개수)는 텍스트 혼합 / " + FIG + "수직선 위 제곱근 점 나열",
    note="2000²<n<2001² → 2001²−2000²−1=4000. 빠른정답 1과 불일치.")

# ======================= 곱셈 공식의 변형 =======================
# p4
add(id="ff8273bb", qtype="short",
    question="[[a = sqrt(7) + 2]], [[b = sqrt(7) - 2]]일 때, [[a b]]의 값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1,
    note="ab=7−4=3 (빠른정답 없음).")

# p12
add(id="e72ef183", qtype="choice",
    question=("다음 그림은 한 칸의 가로와 세로의 길이가 각각 1인 모눈종이 위에 수직선을 그린 것이다. [[seg(PQ) = seg(PA)]], [[seg(PS) = seg(PB)]]이고 "
              "점 A에 대응하는 수를 [[a]], 점 B에 대응하는 수를 [[b]]라 할 때, [[a b]]의 값은?"),
    choices=["[[-4 sqrt(10)]]", "[[-10]]", "[[-6]]", "[[6]]", "[[4 sqrt(10)]]"],
    derived_answer="③",
    figure=U("모눈종이 위 수직선(눈금 −2~6), P는 2, Q는 (−1, 1), S는 (3, 3), 선분 PQ·PS. P 중심 호로 Q→A(−1 부근 왼쪽), S→B(5 부근 오른쪽)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG + "모눈종이 위 수직선과 호",
    note="PQ=PS=√10 → a=2−√10, b=2+√10 → ab=4−10=−6 → ③ = 빠른정답 ✓.")

# p13
add(id="f67ce89b", qtype="choice",
    question=("다음 그림은 한 칸의 가로와 세로의 길이가 각각 1인 모눈종이 위에 수직선을 그린 것이다. [[seg(PQ) = seg(PA)]], [[seg(PS) = seg(PB)]]이고 "
              "점 A에 대응하는 수를 [[a]], 점 B에 대응하는 수를 [[b]]라 할 때, [[a b]]의 값은?"),
    choices=["[[-8]]", "[[-2 sqrt(5)]]", "[[-4]]", "[[4]]", "[[8]]"],
    derived_answer="④",
    figure=U("모눈종이 위 수직선(눈금 −1~6), P는 3, Q는 (1, 1), S는 (4, 2), 선분 PQ·PS. P 중심 호로 Q→A(1 부근 왼쪽), S→B(5 부근 오른쪽)"),
    difficulty_est=2, confidence=0.85,
    needs_review=FIG + "모눈종이 위 수직선과 호",
    note="PQ=PS=√5 → a=3−√5, b=3+√5 → ab=9−5=4 → ④. 빠른정답 0과 불일치.")

# p14
add(id="ba26816d", qtype="short",
    question="[[x + y = 3]], [[x y = -5]]일 때, [[pow(x,2) + pow(y,2)]]의 값을 구하시오.",
    choices=None, derived_answer="19", figure=None, difficulty_est=1,
    note="9−2(−5)=19. 빠른정답 5와 불일치.")

# p22
add(id="ff76adbc", qtype="short",
    question="[[a - b = 5]], [[a b = 5]]일 때, [[-pow(a,3) b + pow(a,2) pow(b,2) - a pow(b,3)]]의 값을 구하시오.",
    choices=None, derived_answer="-150", figure=None, difficulty_est=2,
    note="−ab(a²−ab+b²)=−ab((a−b)²+ab)=−5(25+5)=−150 = 빠른정답 ✓.")

# p23
add(id="47a7dfb8", qtype="short",
    question="[[(x + 3)(y + 3) = 20]], [[x y = 2]]일 때, [[pow(x - y, 2)]]의 값을 구하시오.",
    choices=None, derived_answer="1", figure=None, difficulty_est=2,
    note="xy+3(x+y)+9=20 → x+y=3 → (x−y)²=9−8=1 = 빠른정답 ✓.")

# p24
add(id="70319de9", qtype="short",
    question="[[a + b = 3]], [[a b = 1]]일 때, [[pow(a,4) + pow(b,4)]]의 값을 구하시오.",
    choices=None, derived_answer="47", figure=None, difficulty_est=2,
    note="a²+b²=7 → a⁴+b⁴=49−2=47 = 빠른정답 ✓.")

# p25
add(id="8bb5c758", qtype="short",
    question="[[a + b = 3]], [[a b = 2]], [[x + y = 4]], [[x y = 3]]일 때,\n[[(a x + b y)(b x + a y)]]의 값을 구하시오.",
    choices=None, derived_answer="35", figure=None, difficulty_est=2,
    note="ab(x²+y²)+xy(a²+b²)=2·10+3·5=35. 빠른정답 −150과 불일치.")

# p26
add(id="2c33d352", qtype="short",
    question="[[a + b = 5]], [[a b = 4]], [[x + y = 7]], [[x y = 12]]일 때,\n[[(a x + b y)(b x + a y)]]의 값을 구하시오.",
    choices=None, derived_answer="304", figure=None, difficulty_est=2,
    note="ab(x²+y²)+xy(a²+b²)=4·25+12·17=304. 빠른정답 1과 불일치.")

# p67
add(id="d70754c7", qtype="short",
    question=("[[pow(x,2) + pow(y,2) = 10]], [[x y = -1]]일 때,\n"
              "[[pow(pow(x - frac(1,x), n) + pow(y - frac(1,y), n), 2) - pow(pow(x - frac(1,x), n) - pow(y - frac(1,y), n), 2) = 2048]]"
              "을 만족시키는 [[n]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=3,
    note="(A+B)²−(A−B)²=4AB, AB=((x−1/x)(y−1/y))ⁿ=(xy+1/(xy)−(x²+y²)/(xy))ⁿ=8ⁿ → 4·8ⁿ=2048 → n=3 = 빠른정답 ✓. 원문 중괄호는 소괄호로.")

# p94
add(id="e36f07d2", qtype="short",
    question=("[[sqrt(6)]]의 소수 부분을 [[f(1)]]이라 하고 [[frac(1, f(1))]]의 소수 부분을 [[f(2)]], [[frac(1, f(2))]]의 소수 부분을 [[f(3)]], "
              "[[frac(1, f(3))]]의 소수 부분을 [[f(4)]], ⋯라 하자.\n"
              "[[f(1) + f(2) + f(3)]] + ⋯ + [[f(100) = m + n sqrt(6)]]일 때, 유리수 [[m]], [[n]]에 대하여 [[m + n]]의 값을 구하시오."),
    choices=None, derived_answer="-75", figure=None, difficulty_est=3,
    note="f(홀수)=√6−2, f(짝수)=√6/2−1 → 합=75√6−150 → m+n=−75. 빠른정답 4와 불일치.")

# p95
add(id="dd413c82", qtype="short",
    question=("[[sqrt(11)]]의 소수 부분을 [[f(1)]]이라 하고 [[frac(1, f(1))]]의 소수 부분을 [[f(2)]], [[frac(1, f(2))]]의 소수 부분을 [[f(3)]], "
              "[[frac(1, f(3))]]의 소수 부분을 [[f(4)]], ⋯라 하자.\n"
              "[[f(1) + f(2) + f(3)]] + ⋯ + [[f(80) = m + n sqrt(11)]]일 때, 유리수 [[m]], [[n]]에 대하여 [[m + n]]의 값을 구하시오."),
    choices=None, derived_answer="-120", figure=None, difficulty_est=3,
    note="f(홀수)=√11−3, f(짝수)=(√11−3)/2 → 합=60√11−180 → m+n=−120 = 빠른정답 ✓.")

# p96
add(id="b5251806", qtype="short",
    question=("[[sqrt(3)]]의 소수 부분을 [[f(1)]]이라 하고 [[frac(1, f(1))]]의 소수 부분을 [[f(2)]], [[frac(1, f(2))]]의 소수 부분을 [[f(3)]], "
              "[[frac(1, f(3))]]의 소수 부분을 [[f(4)]], ⋯라 하자.\n"
              "[[f(1) + f(2) + f(3)]] + ⋯ + [[f(60) = m + n sqrt(3)]]일 때, 유리수 [[m]], [[n]]에 대하여 [[n - m]]의 값을 구하시오."),
    choices=None, derived_answer="90", figure=None, difficulty_est=3,
    note="f(홀수)=√3−1, f(짝수)=(√3−1)/2 → 합=45√3−45 → n−m=90 = 빠른정답 ✓.")

# p99 (이미지에 별개 문항 2개, id 2개 → draft_a 대응대로 분리)
add(id="d323fcbe", qtype="short",
    question=("[[frac(1, 1 + sqrt(2)) + frac(1, sqrt(2) + sqrt(3)) + frac(1, sqrt(3) + sqrt(4))]] + ⋯ + [[frac(1, sqrt(79) + sqrt(80))]]의 "
              "소수 부분을 [[a]]라 할 때, [[pow(a,2) + 16a + 2]]의 값을 구하시오."),
    choices=None, derived_answer="18", figure=None, difficulty_est=3,
    note="이미지 위쪽 문항(같은 쪽 아래쪽 문항은 e619fc88). 합=√80−1, 정수 부분 7 → a=√80−8 → (a+8)²=80 → a²+16a=16 → 18. 빠른정답 90과 불일치.")
add(id="e619fc88", qtype="short",
    question=("[[frac(1, 1 + sqrt(2)) + frac(1, sqrt(2) + sqrt(3)) + frac(1, sqrt(3) + sqrt(4))]] + ⋯ + [[frac(1, sqrt(9) + sqrt(10))]]의 "
              "소수 부분을 [[a]]라 할 때, [[2 pow(a,2) + 12a + 1]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=3,
    note="이미지 아래쪽 문항(같은 쪽 위쪽 문항은 d323fcbe). 합=√10−1, 정수 부분 2 → a=√10−3 → (a+3)²=10 → 2(a²+6a)+1=3. 빠른정답 90과 불일치.")

# ======================= 이차함수 y=a(x-p)²+q의 그래프 =======================
# p9
add(id="1628aaa7", qtype="short",
    question=("이차함수 [[y = -2 pow(x + 5, 2) + 2]]의 그래프는 [[y = -2 pow(x,2)]]의 그래프를 [[x]]축의 방향으로 [[p]]만큼, "
              "[[y]]축의 방향으로 [[q]]만큼 평행이동한 것이다. 이때 [[p q]]의 값을 구하시오."),
    choices=None, derived_answer="-10", figure=None, difficulty_est=1,
    note="p=−5, q=2 → pq=−10. 빠른정답 4와 불일치.")

# p27 (선지가 그래프 그림)
add(id="b173473b", qtype="choice",
    question="다음 중 이차함수 [[y = 2 pow(x - 1, 2) + 1]]의 그래프로 옳은 것은?",
    choices=["(그래프) 아래로 볼록한 포물선, 꼭짓점 [[point(2, 1)]]",
             "(그래프) 아래로 볼록한 포물선, 꼭짓점 [[point(-1, 1)]]",
             "(그래프) 아래로 볼록한 포물선, 꼭짓점 [[point(-1, -1)]]",
             "(그래프) 아래로 볼록한 포물선, 꼭짓점 [[point(1, 1)]]",
             "(그래프) 아래로 볼록한 포물선, 꼭짓점 [[point(1, -1)]]"],
    derived_answer="④",
    figure=U("선지 ①~⑤가 좌표평면 위 포물선 그림(모두 아래로 볼록, 꼭짓점 좌표를 점선으로 표시): ①(2,1) ②(−1,1) ③(−1,−1) ④(1,1) ⑤(1,−1)"),
    difficulty_est=1, confidence=0.85,
    needs_review=FIG + "선지 5개가 이차함수 그래프 그림(텍스트 서술)",
    note="꼭짓점 (1, 1), 아래로 볼록 → ④ = 빠른정답 ✓.")

# p29 (선지가 그래프 그림)
add(id="cfd11524", qtype="choice",
    question="다음 중 이차함수 [[y = -frac(1,2) pow(x + 1, 2) - 3]]의 그래프로 옳은 것은?",
    choices=["(그래프) 위로 볼록한 포물선, 꼭짓점 [[point(-1, -3)]]",
             "(그래프) 위로 볼록한 포물선, 꼭짓점 [[point(1, -3)]]",
             "(그래프) 아래로 볼록한 포물선, 꼭짓점 [[point(-1, -3)]]",
             "(그래프) 아래로 볼록한 포물선, 꼭짓점 [[point(1, -3)]]",
             "(그래프) 위로 볼록한 포물선, 꼭짓점 [[point(1, 3)]]"],
    derived_answer="①",
    figure=U("선지 ①~⑤가 좌표평면 위 포물선 그림(꼭짓점 좌표를 점선으로 표시): ①위로 볼록 (−1,−3) ②위로 볼록 (1,−3) ③아래로 볼록 (−1,−3) ④아래로 볼록 (1,−3) ⑤위로 볼록 (1,3)"),
    difficulty_est=1, confidence=0.85,
    needs_review=FIG + "선지 5개가 이차함수 그래프 그림(텍스트 서술)",
    note="꼭짓점 (−1, −3), 위로 볼록 → ① = 빠른정답 ✓.")

# p43
add(id="74245ed9", qtype="choice",
    question="다음 중 이차함수 [[y = -3 pow(x - 2, 2) + 4]]의 그래프 위의 점은?",
    choices=["[[point(-3, -21)]]", "[[point(-1, -5)]]", "[[point(0, 4)]]", "[[point(1, -1)]]", "[[point(3, 1)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="x=3 → −3+4=1 → ⑤ = 빠른정답 ✓.")

# p63 (○× 판정형)
add(id="1c1cb285", qtype="short",
    question=("다음 설명이 옳으면 '○'를, 옳지 않으면 '×'를 고르시오.\n"
              "이차함수 [[y = 3 pow(x - frac(2,3), 2) + frac(1,3)]]의 그래프는 [[x > frac(2,3)]]일 때, [[x]]의 값이 증가하면 [[y]]의 값은 감소한다.\n"
              "① ○ ② ×"),
    choices=None, derived_answer="②", figure=None, difficulty_est=1, confidence=0.8,
    needs_review="선지 2개(○× 판정형, 5지 규격 밖) — 보기를 본문에 텍스트로 포함",
    note="아래로 볼록, 축 x=2/3 오른쪽에서는 증가 → 설명은 틀림 → ② ×. 빠른정답 1과 불일치.")

# p86 (문항·선지 그림)
add(id="bb4a363a", qtype="choice",
    question="일차함수 [[y = a x + b]]의 그래프가 다음 그림과 같을 때, 이차함수 [[y = a pow(x + b, 2) - a]]의 그래프로 적당한 것은?",
    choices=["(그래프) 아래로 볼록, 꼭짓점이 [[x]]축 위의 점([[x > 0]])이고 [[y]]절편이 양수인 포물선",
             "(그래프) 아래로 볼록, 꼭짓점이 제3사분면에 있는 포물선",
             "(그래프) 위로 볼록, 꼭짓점이 제2사분면에 있는 포물선",
             "(그래프) 위로 볼록, 꼭짓점이 제4사분면에 있는 포물선",
             "(그래프) 아래로 볼록, 꼭짓점이 원점인 포물선"],
    derived_answer="③",
    figure=U("좌표평면: 오른쪽 아래로 내려가는 직선(y절편 양수, x절편 양수). 선지 ①~⑤는 포물선 그림(선지 텍스트에 서술)"),
    difficulty_est=2, confidence=0.8,
    needs_review=FIG + "문항·선지 5개가 모두 함수 그래프 그림(선지는 텍스트 서술)",
    note="a<0, b>0 → 위로 볼록, 꼭짓점 (−b, −a)는 제2사분면 → ③. 빠른정답 4와 불일치.")

# p92
add(id="312ad218", qtype="choice",
    question=("다음 조건을 모두 만족하는 이차함수의 그래프의 식은?\n"
              "• 아래로 볼록한 포물선이다.\n• 직선 [[x = 1]]을 축으로 한다.\n• 꼭짓점의 좌표가 [[point(1, 0)]]이다."),
    choices=["[[y = pow(x,2) + 1]]", "[[y = -2 pow(x + 1, 2)]]", "[[y = -pow(x - 1, 2)]]", "[[y = 3(pow(x,2) - 1)]]", "[[y = frac(2,3) pow(x - 1, 2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="a>0, 꼭짓점 (1, 0) → ⑤. 빠른정답 1과 불일치.")

# p97
add(id="7826e8c6", qtype="choice",
    question=("다음 중 주어진 조건을 모두 만족시키는 포물선을 그래프로 하는 이차함수의 식은?\n"
              "(가) 아래로 볼록한 포물선이다.\n(나) [[y = -3 pow(x - 1, 2)]]의 그래프와 폭이 같다.\n(다) 꼭짓점은 제3사분면 위에 있다."),
    choices=["[[y = pow(x + 2, 2) - 1]]", "[[y = 3 pow(x + 2, 2) - 3]]", "[[y = 3 pow(x - 4, 2) - 2]]", "[[y = -3 pow(x + 1, 2) - 2]]", "[[y = -3 pow(x - 1, 2) - 4]]"],
    derived_answer="②", figure=None, difficulty_est=1,
    note="a=3, 꼭짓점 (−2, −3) 제3사분면 → ② = 빠른정답 ✓.")

# ======================= 이차방정식 구하기 =======================
# p1
add(id="58b90462", qtype="short",
    question="이차방정식 [[2 pow(x,2) - a x + b = 0]]의 두 근이 [[x = 1]] 또는 [[x = 2]]일 때, [[a + b]]의 값을 구하시오.",
    choices=None, derived_answer="10", figure=None, difficulty_est=1,
    note="2(x−1)(x−2)=2x²−6x+4 → a=6, b=4 → 10 = 빠른정답 ✓.")

# p2
add(id="14f60472", qtype="choice",
    question="[[frac(1,2)]], [[-frac(1,3)]]이 이차방정식 [[6 pow(x,2) + a x + b = 0]]의 두 근일 때, [[a + b]]의 값은?",
    choices=["[[2]]", "[[1]]", "[[0]]", "[[-1]]", "[[-2]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="(2x−1)(3x+1)=6x²−x−1 → a=−1, b=−1 → −2 → ⑤ = 빠른정답 ✓.")

# p6
add(id="784ece76", qtype="choice",
    question="이차방정식 [[2 pow(x,2) - a x + 2b - 4 = 0]]이 중근 [[x = -2]]를 가질 때, 상수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?",
    choices=["[[2]]", "[[-2]]", "[[1]]", "[[-1]]", "[[4]]"],
    derived_answer="②", figure=None, difficulty_est=2,
    note="2(x+2)²=2x²+8x+8 → a=−8, 2b−4=8 → b=6 → a+b=−2 → ②. 빠른정답 1과 불일치.")

# p13
add(id="8c18ec02", qtype="choice",
    question="[[pow(x,2)]]의 계수가 1이고 [[x = 3]]을 중근으로 갖는 이차방정식이 [[pow(x,2) + (a + b) x + a - b = 0]]일 때, 상수 [[a]], [[b]]의 값은?",
    choices=["[[a = -frac(3,2)]], [[b = -frac(15,2)]]",
             "[[a = -frac(3,2)]], [[b = frac(15,2)]]",
             "[[a = frac(3,2)]], [[b = -frac(15,2)]]",
             "[[a = 3]], [[b = frac(15,2)]]",
             "[[a = 3]], [[b = -frac(15,2)]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="(x−3)²=x²−6x+9 → a+b=−6, a−b=9 → a=3/2, b=−15/2 → ③. 빠른정답 1과 불일치.")

# p15
add(id="762ea115", qtype="choice",
    question="이차방정식 [[pow(x,2) + a x + b = 0]]의 해가 [[-3]], [[-2]]일 때,\n[[b pow(x,2) + a x + 1 = 0]]의 해를 구하면?",
    choices=["[[-frac(1,4)]], [[-frac(1,3)]]",
             "[[-frac(1,3)]], [[-frac(1,2)]]",
             "[[frac(1,4)]], [[-frac(1,3)]]",
             "[[frac(1,4)]], [[frac(1,3)]]",
             "[[frac(1,2)]], [[frac(1,3)]]"],
    derived_answer="②", figure=None, difficulty_est=2,
    note="a=5, b=6 → 6x²+5x+1=(2x+1)(3x+1)=0 → x=−1/2, −1/3 → ②. 빠른정답 5와 불일치.")

# p57
add(id="f21b78ef", qtype="short",
    question=("[[pow(x,2)]]의 계수가 3인 이차방정식이 있다. [[x]]의 계수를 바꾸었더니 두 근이 1과 2가 되었고, 상수항을 바꾸었더니 두 근이 4와 [[-frac(1,3)]]이 되었다. "
              "처음 주어진 이차방정식의 두 근 중 큰 근을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=3,
    note="상수항 3·1·2=6, x계수 −3(4−1/3)=−11 → 3x²−11x+6=(3x−2)(x−3)=0 → 큰 근 3 = 빠른정답 ✓.")

# p61
add(id="758e2c09", qtype="choice",
    question=("이차방정식 [[pow(x,2) + a x + b = 0]]에서 일차항의 계수와 상수항을 서로 바꾸어 풀었더니 해가 [[x = -3]] 또는 [[x = 4]]이었다. "
              "이때 처음 이차방정식의 해는? (단, [[a]], [[b]]는 상수)"),
    choices=["[[x = -4]] 또는 [[x = -3]]", "[[x = -4]] 또는 [[x = 3]]", "[[x = pm(-6, sqrt(37))]]", "[[x = pm(3, sqrt(37))]]", "[[x = pm(6, sqrt(37))]]"],
    derived_answer="⑤", figure=None, difficulty_est=2,
    note="바꾼 식 (x+3)(x−4)=x²−x−12 → b=−1, a=−12 → x²−12x−1=0 → x=6±√37 → ⑤ = 빠른정답 ✓.")

# p62
add(id="231230f4", qtype="choice",
    question=("이차방정식 [[pow(x,2) + a x + b = 0]]에서 일차항의 계수와 상수항을 서로 바꾸어 풀었더니 해가 [[x = -1]] 또는 [[x = 5]]이었다. "
              "이때 처음 이차방정식의 해는? (단, [[a]], [[b]]는 상수)"),
    choices=["[[x = -5]] 또는 [[x = -1]]", "[[x = -5]] 또는 [[x = 1]]", "[[x = frac(pm(-5, sqrt(41)), 2)]]", "[[x = frac(pm(5, sqrt(41)), 2)]]", "[[x = pm(5, sqrt(41))]]"],
    derived_answer="④", figure=None, difficulty_est=2,
    note="바꾼 식 (x+1)(x−5)=x²−4x−5 → b=−4, a=−5 → x²−5x−4=0 → x=(5±√41)/2 → ④ = 빠른정답 ✓.")

# p63
add(id="180bc55d", qtype="choice",
    question=("이차방정식 [[pow(x,2) + a x + b = 0]]의 근을 구하는데 소연이는 일차항의 계수를 잘못 보고 풀어서 두 근이 [[x = pm(1, sqrt(2))]]가 나왔고, "
              "소희는 상수항을 잘못 보고 풀어서 두 근이 [[x = pm(2, sqrt(6))]]이 나왔다. 이때 [[a b]]의 값은?"),
    choices=["[[-4]]", "[[-2]]", "[[1]]", "[[2]]", "[[4]]"],
    derived_answer="⑤", figure=None, difficulty_est=2,
    note="b=(1+√2)(1−√2)=−1, a=−(2+√6+2−√6)=−4 → ab=4 → ⑤. 빠른정답 4와 불일치.")

# p86
add(id="ff0981e8", qtype="short",
    question="계수가 유리수이고 한 근이 [[5 - 2 sqrt(3)]]인 이차방정식을 [[4 pow(x,2) + b x + c = 0]]의 꼴로 나타낼 때, [[c - b]]의 값을 구하시오.",
    choices=None, derived_answer="92", figure=None, difficulty_est=2,
    note="근 5±2√3: 합 10, 곱 13 → 4x²−40x+52=0 → c−b=52+40=92. 빠른정답 1과 불일치.")

# p89
add(id="6e81eaba", qtype="short",
    question=("이차방정식 [[4 pow(x,2) - 2a x + b = 0]]의 한 근이 [[frac(1 + sqrt(2), 2)]]일 때, 이차방정식 [[a pow(x,2) + 3b x - a = 0]]의 두 근의 제곱의 합을 구하시오. "
              "(단, [[a]], [[b]]는 유리수)"),
    choices=None, derived_answer="frac(17,4)", figure=None, difficulty_est=3,
    note="근 (1±√2)/2: 합 1, 곱 −1/4 → 4x²−4x−1=0 → a=2, b=−1 → 2x²+3x−2=0: 합 −3/2, 곱 −1 → 제곱합 9/4+2=17/4 = 빠른정답 ✓.")

# ======================= 이차방정식의 근의 판별 =======================
# p1
add(id="5490614a", qtype="choice",
    question=("다음 보기 중 [[x]]에 대한 이차방정식 [[pow(x,2) + a x + b = 0]]에 대한 설명으로 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[a = -6]], [[b = 3]]이면 서로 다른 두 근을 갖는다.\n"
              "ㄴ. [[a = 0]], [[b = -25]]이면 서로 다른 두 근을 갖는다.\n"
              "ㄷ. [[a = 3]], [[b = 5]]이면 중근을 갖는다.\n"
              "ㄹ. [[b < 0]]이면 근을 갖지 않는다."),
    choices=["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄹ", "ㄱ, ㄷ, ㄹ", "ㄴ, ㄷ, ㄹ"],
    derived_answer="①", figure=None, difficulty_est=2,
    note="ㄱ D=24>0 ✓, ㄴ x²=25 ✓, ㄷ D=−11<0 ✗, ㄹ b<0이면 D>0 ✗ → ① = 빠른정답 ✓.")

# p50
add(id="7aee2537", qtype="choice",
    question="이차방정식 [[25 pow(x,2) - 10a x - a + 12 = 0]]이 음수인 중근을 갖도록 하는 상수 [[a]]의 값은?",
    choices=["[[-6]]", "[[-5]]", "[[-4]]", "[[3]]", "[[4]]"],
    derived_answer="③", figure=None, difficulty_est=2,
    note="D/4=25(a²+a−12)=0 → a=−4 또는 3; 중근 x=a/5<0 → a=−4 → ③. 빠른정답 4와 불일치.")

# p55
add(id="6efe9beb", qtype="choice",
    question="이차방정식 [[4 pow(x,2) + 2a x - a + 15 = 0]]이 음수인 중근을 갖도록 하는 상수 [[a]]의 값은?",
    choices=["[[-6]]", "[[-3]]", "[[0]]", "[[3]]", "[[6]]"],
    derived_answer="⑤", figure=None, difficulty_est=2,
    note="D/4=a²+4a−60=0 → a=−10 또는 6; 중근 x=−a/4<0 → a=6 → ⑤. 빠른정답 12와 불일치.")

# p76
add(id="3ce9ad1b", qtype="short",
    question=("[[x]]에 관한 이차방정식\n[[(1 + pow(a + b, 2)) pow(x,2) - 2(1 - a - b) x + 2 = 0]]의 근이 실수일 때, 실수 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="-1", figure=None, difficulty_est=3,
    note="t=a+b: D/4=(1−t)²−2(1+t²)=−(t+1)²≥0 → t=−1. 빠른정답 1과 불일치. 원문 중괄호 {1+(a+b)²}는 소괄호로.")

# p87
add(id="ee3efebe", qtype="short",
    question=("이차방정식 [[a pow(x,2) + b x + c = 0]]을 만족시키는 두 실근을 [[p]], [[q]]라 할 때 [[pow(p - q, 2) != 0]]이 성립한다. "
              "실수 [[x]]에 대하여 이차방정식 [[b pow(x,2) + 2(a - 2c) x - b = 0]]의 해의 개수와 "
              "이차방정식 [[pow(x,2) + 2(a + c) x + 6(a c - pow(a,2)) - pow(b,2) = 0]]의 해의 개수의 합을 구하시오. (단, [[a]], [[b]], [[c]]는 실수)"),
    choices=None, derived_answer="4", figure=None, difficulty_est=3,
    note="b²−4ac>0. 첫째 D/4=(a−2c)²+b²>0 → 2개, 둘째 D/4=7a²−4ac+c²+b²>7a²+c²>0 → 2개 → 합 4 = 빠른정답 ✓.")

# p91 (사용자 정의 연산 ◎)
add(id="343af482", qtype="choice",
    question=("두 실수 [[a]], [[b]]에 대하여 [[a]]◎[[b]] = [[-a + b + a b]]일 때, ([[3x - 1]])◎([[x + 2]]) = [[k]]가 근을 갖도록 하는 상수 [[k]]의 값 중 가장 작은 값은?"),
    choices=["[[-frac(1,2)]]", "[[-frac(1,4)]]", "[[0]]", "[[frac(1,4)]]", "[[frac(1,2)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 사용자 정의 연산 ◎ → 텍스트 혼합 전사",
    note="(3x−1)◎(x+2)=3x²+3x+1=k → D=9−12(1−k)≥0 → k≥1/4 → ④ = 빠른정답 ✓.")

# ======================= 이차함수의 뜻 =======================
# p13
add(id="b1253f5a", qtype="choice",
    question="다음 중 이차함수가 아닌 것을 모두 고르면? (정답 2개)",
    choices=["[[3 pow(x,2) + 1 = 0]]", "[[y = -pow(x,2) + 5x + 2]]", "[[y = (x - 1)(x + 3) - pow(x,2)]]", "[[y = a pow(x,2) + b x + c]] ([[a != 0]])", "[[y = frac(2,5) pow(x,2) - frac(7,8)]]"],
    derived_answer="①, ③", figure=None, difficulty_est=1,
    note="① 함수가 아닌 방정식, ③ x² 소거 → 일차함수 → ①, ③. 빠른정답 2와 불일치.")

# p31
add(id="b98fb30e", qtype="choice",
    question="다음 설명에서 □ 안에 들어갈 말로 알맞은 것을 고르면?\n이차함수 [[y = a pow(x,2) + b x + c]]가 성립하기 위한 조건은 □이다.",
    choices=["[[frac(a, c) < 0]]", "[[b > 0]]", "[[a != 0]]", "[[a b > 0]]", "[[a > 0]]"],
    derived_answer="③", figure=None, difficulty_est=1,
    note="a≠0 → ③ = 빠른정답 ✓.")

# p32
add(id="48490adf", qtype="choice",
    question="함수 [[y = 4 pow(x,2) + 1 - 2x(a x + 1)]]이 이차함수일 때, 다음 중 [[a]]의 값이 될 수 없는 것은?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=1,
    note="(4−2a)x²−2x+1 → a≠2 → ②. 빠른정답 1과 불일치.")

# p34
add(id="cdca3834", qtype="choice",
    question="함수 [[y = pow(4x + 3, 2) - x(a x + 2)]]가 이차함수가 되도록 하는 상수 [[a]]의 조건은?",
    choices=["[[a > 4]]", "[[a = 4]]", "[[a != 4]]", "[[a = 16]]", "[[a != 16]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="(16−a)x²+22x+9 → a≠16 → ⑤. 빠른정답 3과 불일치.")

# p38
add(id="79f7eef8", qtype="choice",
    question="[[y = m(m - 2) pow(x,2) - 8 pow(x,2) + 5]]이 [[x]]에 대한 이차함수일 때, 다음 중 상수 [[m]]이 값이 될 수 없는 것을 모두 고르면? (정답 2개)",
    choices=["[[-2]]", "[[0]]", "[[2]]", "[[4]]", "[[6]]"],
    derived_answer="①, ④", figure=None, difficulty_est=1,
    note="m²−2m−8=(m−4)(m+2)≠0 → m≠4, −2 → ①, ④ = 빠른정답 '1, 4' ✓ (원문 '상수 m이 값이' 그대로).")

# p41
add(id="78720f0e", qtype="choice",
    question="[[y = (pow(k,2) + 2k - 8) pow(x,2) - 3x + 9]]가 [[x]]에 대한 이차함수일 때, 다음 중 실수 [[k]]의 값이 될 수 없는 것을 모두 고르면? (정답 2개)",
    choices=["[[-4]]", "[[-2]]", "[[0]]", "[[2]]", "[[4]]"],
    derived_answer="①, ④", figure=None, difficulty_est=1,
    note="(k+4)(k−2)≠0 → k≠−4, 2 → ①, ④ = 빠른정답 '1, 4' ✓.")

# p43
add(id="a814815b", qtype="choice",
    question="다음 중 [[y = 2k pow(x,2) - 3(x - 2 pow(x,2))]]이 [[x]]에 대한 이차함수가 되도록 하는 실수 [[k]]의 조건은?",
    choices=["[[k != -6]]", "[[k != -3]]", "[[k != 0]]", "[[k != 3]]", "[[k != 6]]"],
    derived_answer="②", figure=None, difficulty_est=1,
    note="(2k+6)x²−3x → k≠−3 → ②. 빠른정답 '1, 5'와 불일치.")

# p46
add(id="179067ff", qtype="choice",
    question="함수 [[y = 6 pow(x,2) - x(1 - 2a x)]]가 이차함수일 때, 다음 중 [[a]]의 값이 될 수 없는 것은?",
    choices=["[[-3]]", "[[-2]]", "[[1]]", "[[2]]", "[[3]]"],
    derived_answer="①", figure=None, difficulty_est=1,
    note="(6+2a)x²−x → a≠−3 → ①. 빠른정답 2와 불일치.")

# p55
add(id="d48e7271", qtype="choice",
    question="함수 [[y = pow(3x + 1, 2) - x(a x + 1)]]이 이차함수가 되도록 하는 상수 [[a]]의 조건은?",
    choices=["[[a > 3]]", "[[a > 9]]", "[[a < 3]]", "[[a = 9]]", "[[a != 9]]"],
    derived_answer="⑤", figure=None, difficulty_est=1,
    note="(9−a)x²+5x+1 → a≠9 → ⑤. 빠른정답 −2와 불일치.")

# p61
add(id="d3ff9503", qtype="short",
    question=("함수 [[y = ((a - 1) x + 3)(a x - b)(x - 4)]]가 [[x]]의 이차함수가 되도록 하는 4 이하의 음이 아닌 두 정수 [[a]], [[b]]의 순서쌍 [[point(a, b)]]의 개수를 구하시오."),
    choices=None, derived_answer="9", figure=None, difficulty_est=3,
    note="a=1이면 3(x−b)(x−4) → b 5개; a=0이면 (−x+3)(−b)(x−4) → b≠0 4개; 그 외는 삼차 → 9 = 빠른정답 ✓. 원문 중괄호 {(a−1)x+3}은 소괄호로.")

# p82
add(id="e67d6bb8", qtype="short",
    question="이차함수 [[f(x) = -pow(x,2) + 5x - 3]]에 대하여 [[f(frac(1,5))]]을 구하시오.",
    choices=None, derived_answer="frac(-51,25)", figure=None, difficulty_est=1,
    note="−1/25+1−3=−51/25 = 빠른정답 ✓.")

# p90
add(id="2293b369", qtype="choice",
    question="이차함수 [[f(x) = -3 pow(x,2) - a x + 6]]에서 [[f(2) = -4]]일 때, 상수 [[a]]의 값은?",
    choices=["[[-3]]", "[[-2]]", "[[-1]]", "[[1]]", "[[2]]"],
    derived_answer="③", figure=None, difficulty_est=1,
    note="−12−2a+6=−4 → a=−1 → ③. 빠른정답 2와 불일치.")

# ======================= 제곱근의 뜻과 성질 =======================
# p1
add(id="a85fe12c", qtype="choice",
    question="[[pow(a,2) = 15]]을 만족시키는 [[a]]의 값을 모두 구한 것은?",
    choices=["[[-sqrt(15)]]", "[[sqrt(15)]]", "[[pm(15)]]", "[[pm(sqrt(15))]]", "[[15]]"],
    derived_answer="④", figure=None, difficulty_est=1,
    note="a=±√15 → ④ = 빠른정답 ✓.")
