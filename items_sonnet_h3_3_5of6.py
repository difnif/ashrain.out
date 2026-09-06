# -*- coding: utf-8 -*-
# esc_sonnet_h3-3_5of6 — 이미지 기준 전사 (81 항목 / 80쪽)
# 주: 파서(mathir.py v1.4)의 토크나이저가 'point3'을 'point'+'3'으로 쪼개므로 3차원 좌표는 vcomp(x,y,z)로 적음(표시 동일).
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))
def fig(raw): return [{"fn": "unsupported", "args": {"raw": raw}}]

# ───────────── 쌍곡선의 접선의 방정식 ─────────────
# p84
add(id="a6681072", qtype="short",
    question=("다음 그림과 같이 두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 "
              "[[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 48) = 1]] 위의 점 P[[point(8, k)]] ([[k > 0]])에서의 접선이 "
              "[[x]]축과 만나는 점을 Q라 하자. 두 점 F, F′을 초점으로 하고 점 Q를 한 꼭짓점으로 하는 쌍곡선이 "
              "선분 PF′과 만나는 두 점을 R, S라 하자. [[seg(RS) + seg(SF) = seg(RF) + 8]]일 때, [[pow(a,2) + pow(k,2)]]의 값을 "
              "구하시오. (단, [[a]]는 양수이고, 점 R의 [[x]]좌표는 점 S의 [[x]]좌표보다 크다.)"),
    choices=None, derived_answer="160",
    figure=fig("좌표평면: 쌍곡선 x²/a²−y²/48=1(초점 F, F′), 두 초점을 공유하고 Q를 꼭짓점으로 하는 두 번째 쌍곡선, 점 P에서의 접선(x축과 Q에서 만남), 선분 PF′ 위의 점 R, S"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 쌍곡선 2개+접선+선분 PF′ 좌표평면 도형 / 프라임 점 라벨(F′)을 텍스트 혼합으로 표기",
    note="출처 [2023년 4월 고3 기하 29번 변형]. Q(a²/8,0) ⇒ 둘째 쌍곡선 2a'=a²/4; (RF'−RF)+(SF−SF')=a²/2=8 ⇒ a²=16, k²=144 ⇒ 160 (빠른정답 2와 불일치).")

# p86
add(id="4c2063db", qtype="short",
    question=("두 점 [[sub(F,1)]][[point(4, 0)]], [[sub(F,2)]][[point(-6, 0)]]에 대하여 포물선 [[pow(y,2) = 16x]] 위의 점 중 "
              "제1사분면에 있는 점 P가 P[[sub(F,2)]] − P[[sub(F,1)]] = 6을 만족시킨다. 포물선 [[pow(y,2) = 16x]] 위의 점 P에서의 "
              "접선이 [[x]]축과 만나는 점을 [[sub(F,3)]]이라 하면 두 점 [[sub(F,1)]], [[sub(F,3)]]을 초점으로 하는 타원의 한 꼭짓점은 "
              "선분 P[[sub(F,3)]] 위에 있다. 이 타원의 장축의 길이가 [[2a]]일 때, [[pow(a,2)]]의 값을 구하시오."),
    choices=None, derived_answer="54",
    figure=fig("좌표평면: 포물선 y²=16x, 제1사분면 위의 점 P와 P에서의 접선, 접선이 x축과 만나는 점 F₃(음의 x축), x축 위의 점 F₂(−6,0), F₁(4,0), 원점 O"),
    difficulty_est=4, confidence=0.75,
    needs_review="첨자 점 라벨(F₁, F₂, F₃) — 선분 기호 PF₂−PF₁, PF₃를 텍스트 혼합으로 표기 / 도형 표현 불가: 포물선·접선·초점 좌표평면 도형",
    note="출처 [2022년 10월 고3 기하 29번/4점]. P(8,8√2), F₃(−8,0), 타원 중심(−2,0) c=6, 단축 꼭짓점(−2,3√2) b²=18 ⇒ a²=54 (빠른정답 2와 불일치).")

# p92
add(id="254b0db1", qtype="short",
    question=("두 점 [[sub(F,1)]][[point(6, 0)]], [[sub(F,2)]][[point(-12, 0)]]에 대하여 포물선 [[pow(y,2) = 24x]] 위의 점 중 "
              "제1사분면에 있는 점 P가 P[[sub(F,2)]] − P[[sub(F,1)]] = 12를 만족시킨다. 포물선 [[pow(y,2) = 24x]] 위의 점 P에서의 "
              "접선이 [[x]]축과 만나는 점을 [[sub(F,3)]]이라 하면 두 점 [[sub(F,1)]], [[sub(F,3)]]을 초점으로 하는 타원의 한 꼭짓점은 "
              "선분 P[[sub(F,3)]] 위에 있다. 이 타원의 장축의 길이가 [[2a]]일 때, [[frac(20,21) pow(a,2)]]의 값을 구하시오."),
    choices=None, derived_answer="147",
    figure=fig("좌표평면: 포물선 y²=24x, 제1사분면 위의 점 P와 P에서의 접선, 접선이 x축과 만나는 점 F₃(음의 x축), x축 위의 점 F₂(−12,0), F₁(6,0), 원점 O"),
    difficulty_est=4, confidence=0.75,
    needs_review="첨자 점 라벨(F₁, F₂, F₃) — 선분 기호 PF₂−PF₁, PF₃를 텍스트 혼합으로 표기 / 도형 표현 불가: 포물선·접선·초점 좌표평면 도형",
    note="출처 [2022년 10월 고3 기하 29번 변형]. P(15,6√10), F₃(−15,0), c=21/2, b²=44.1 ⇒ a²=154.35 ⇒ (20/21)a²=147 (빠른정답 80과 불일치).")

# ───────────── 타원의 접선의 방정식 ─────────────
# p38
add(id="5f157305", qtype="short",
    question=("점 A[[point(a, 0)]]에서 타원 [[3 pow(x,2) + 5 pow(y,2) = 24]]에 그은 접선의 접점을 P라 할 때, "
              "[[seg(AP) = seg(OP)]]가 성립한다. 이때 양수 [[a]]의 값을 구하시오. (단, O는 원점)"),
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="접점 x₁=8/a, AP=OP ⇒ x₁=a/2 ⇒ a²=16 ⇒ a=4 (빠른정답 5와 불일치).")

# p42
add(id="bff53f07", qtype="short",
    question=("점 A[[point(a, 0)]]에서 타원 [[4 pow(x,2) + 7 pow(y,2) = 8]]에 그은 접선의 접점을 P라 할 때, "
              "[[seg(AP) = seg(OP)]]가 성립한다. 이때 양수 [[a]]의 값을 구하시오. (단, O는 원점)"),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="접점 x₁=2/a, AP=OP ⇒ x₁=a/2 ⇒ a²=4 ⇒ a=2 (빠른정답 3과 불일치).")

# p51
add(id="5a82d58f", qtype="choice",
    question=("[[y]]축 위의 점 A에서 타원 [[C]]: [[frac(pow(x,2), 8) + pow(y,2) = 1]]에 그은 두 접선을 [[sub(l,1)]], [[sub(l,2)]]라 하고, "
              "두 직선 [[sub(l,1)]], [[sub(l,2)]]가 타원 [[C]]와 만나는 점을 각각 P, Q라 하자. 두 직선 [[sub(l,1)]], [[sub(l,2)]]가 서로 수직일 때, "
              "선분 PQ의 길이는? (단, 점 A의 [[y]]좌표는 1보다 크다.)"),
    choices=["[[4]]", "[[frac(13,3)]]", "[[frac(14,3)]]", "[[5]]", "[[frac(16,3)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2022년 4월 고3 기하 26번/3점]. 수직 접선 기울기 ±1, n²=8+1 ⇒ A(0,3), 접점 (∓8/3, 1/3) ⇒ PQ=16/3 ⇒ ⑤.")

# p73
add(id="cac51041", qtype="choice",
    question=("그림과 같이 두 초점이 F[[point(1, 0)]], F′[[point(-1, 0)]]이고 단축의 길이가 [[2 sqrt(5)]]인 타원과 [[y]]축 위의 점 A가 있다. "
              "점 A를 [[x]]축에 대하여 대칭이동한 점을 B라 하자. 제1사분면에서 이 타원 위를 움직이는 점 P에 대하여 네 선분 AB, BF, FP, PA로 "
              "둘러싸인 도형의 넓이가 최대가 되도록 하는 점 P를 [[sub(P,0)]][[point(a, b)]]라 하자. "
              "[[seg(BF)]] + F[[sub(P,0)]] + [[sub(P,0)]]A = [[2 sqrt(6)]]일 때, [[a b]]의 값은?\n"
              "(단, 점 A의 [[y]]좌표는 양수이고, [[seg(AB) < 2 sqrt(5)]]이다.)"),
    choices=["[[frac(11 sqrt(2), 8)]]", "[[frac(3 sqrt(2), 2)]]", "[[frac(13 sqrt(2), 8)]]", "[[frac(7 sqrt(2), 4)]]", "[[frac(15 sqrt(2), 8)]]"],
    derived_answer="⑤",
    figure=fig("좌표평면: 초점 F(1,0), F′(−1,0)인 타원, y축 위의 점 A와 대칭점 B, 제1사분면 위의 점 P, 사각형 ABFP 음영"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 타원·초점·사각형 ABFP 음영 좌표평면 도형 / 프라임·첨자 점 라벨(F′, P₀)을 텍스트 혼합으로 표기",
    note="출처 [2025년 5월 고3 기하 28번/4점]. x²/6+y²/5=1, 조건 ⇒ F′,A,P₀ 한 직선·P₀ 접선∥AF ⇒ a=3/2, b=5√2/4 ⇒ ab=15√2/8 ⇒ ⑤.")

# p81
add(id="bb861f78", qtype="choice",
    question=("다음 그림과 같이 두 초점이 F[[point(0, 1)]], F′[[point(0, -1)]]이고 단축의 길이가 [[2 sqrt(2)]]인 타원과 [[x]]축 위의 점 A가 있다. "
              "점 A를 [[y]]축에 대하여 대칭이동한 점을 B라 하자. 제1사분면에서 이 타원 위를 움직이는 점 P에 대하여 네 선분 AB, BP, PF, FA로 "
              "둘러싸인 도형의 넓이가 최대가 되도록 하는 점 P를 [[sub(P,0)]][[point(a, b)]]라 하자.\n"
              "[[seg(AF)]] + F[[sub(P,0)]] + [[sub(P,0)]]B = [[2 sqrt(3)]]일 때, [[a b]]의 값은?\n"
              "(단, 점 A의 [[x]]좌표는 음수이고, [[seg(AB) < 2 sqrt(2)]]이다.)"),
    choices=["[[frac(3 sqrt(3), 4)]]", "[[frac(2 sqrt(3), 3)]]", "[[frac(7 sqrt(3), 12)]]", "[[frac(sqrt(3), 2)]]", "[[frac(5 sqrt(3), 12)]]"],
    derived_answer="②",
    figure=fig("좌표평면: 초점 F(0,1), F′(0,−1)인 세로로 긴 타원, x축 위의 점 A(음의 x축)와 대칭점 B, 제1사분면 위의 점 P, 사각형 ABPF 음영"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 타원·초점·사각형 ABPF 음영 좌표평면 도형 / 프라임·첨자 점 라벨(F′, P₀)을 텍스트 혼합으로 표기",
    note="출처 [2025년 5월 고3 기하 28번 변형]. x²/2+y²/3=1, F′,B,P₀ 한 직선·P₀ 접선∥BF ⇒ b=1, a=2√3/3 ⇒ ab=2√3/3 ⇒ ②.")

# p85
add(id="b1c5add2", qtype="choice",
    question=("두 점 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원 [[frac(pow(x,2), 108) + frac(pow(y,2), 4 pow(b,2)) = 1]] 위에 있는 "
              "제1사분면 위의 점 P[[point(9, b)]]에서의 접선이 [[x]]축, [[y]]축과 만나는 점을 각각 A, B라 하자. "
              "[[seg(PF)]] + PF′ = [[seg(AB)]]일 때, [[pow(b,2) c]]의 값은?"),
    choices=["[[92]]", "[[96]]", "[[100]]", "[[104]]", "[[108]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="프라임 점 라벨(F′) — 선분 PF′을 텍스트 혼합으로 표기",
    note="출처 [2026년 7월 고3 기하 26번 변형]. 접선 x/12+y/(4b)=1, AB²=144+16b²=432 ⇒ b²=18, c²=108−72=36 ⇒ b²c=108 ⇒ ⑤ (빠른정답 1과 불일치).")

# p88
add(id="3517ae96", qtype="choice",
    question=("다음 그림과 같이 두 점 F[[point(0, c)]], F′[[point(0, -c)]] ([[c > 0]])을 초점으로 하는 타원 "
              "[[frac(pow(x,2), 12) + frac(pow(y,2), 16) = 1]] 위의 점 P[[point(-3, 2)]]에서 타원에 접하는 직선을 [[l]]이라 하자. "
              "점 F를 지나고 [[l]]과 평행한 직선이 타원과 만나는 점 중 제3사분면 위에 있는 점을 Q라 하자. "
              "두 직선 F′Q와 [[l]]이 만나는 점을 R, [[l]]과 [[y]]축이 만나는 점을 S라 할 때, [[seg(RS)]] + RF′의 값은?"),
    choices=["[[24]]", "[[23]]", "[[22]]", "[[21]]", "[[20]]"],
    derived_answer="⑤",
    figure=fig("좌표평면: 타원 x²/12+y²/16=1, 초점 F(0,c)·F′(0,−c), 점 P(−3,2)에서의 접선 l(y축과 S에서 만남), F를 지나 l에 평행한 직선과 제3사분면 교점 Q, 직선 F′Q와 l의 교점 R"),
    difficulty_est=4, confidence=0.75,
    needs_review="도형 표현 불가: 타원·접선 l·평행선·점 P, Q, R, S 좌표평면 도형 / 프라임 점 라벨(F′)을 텍스트 혼합으로 표기",
    note="출처 [2021년 9월 고3 기하 28번 변형]. c=2, l: y=2x+8, S(0,8); △F′FQ∽△F′SR(비 4:10) ⇒ RS+RF′=(5/2)(FQ+F′Q)=(5/2)·8=20 ⇒ ⑤ (빠른정답 4와 불일치).")

# p96
add(id="88a78d72", qtype="choice",
    question=("두 점 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 타원 [[frac(pow(x,2), 48) + frac(pow(y,2), 4 pow(b,2)) = 1]] 위에 있는 "
              "제1사분면 위의 점 P[[point(6, b)]]에서의 접선이 [[x]]축, [[y]]축과 만나는 점을 각각 A, B라 하자. "
              "[[seg(PF)]] + PF′ = [[seg(AB)]]일 때, [[pow(b,2) c]]의 값은?"),
    choices=["[[20]]", "[[24]]", "[[28]]", "[[32]]", "[[36]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="프라임 점 라벨(F′) — 선분 PF′을 텍스트 혼합으로 표기",
    note="출처 [2026년 7월 고3 기하 26번/3점]. 접선 x/8+y/(4b)=1, AB²=64+16b²=192 ⇒ b²=8, c²=48−32=16 ⇒ b²c=32 ⇒ ④ (빠른정답 5와 불일치).")

# ───────────── 벡터의 뜻 ─────────────
# p1
add(id="095ee4e9", qtype="short",
    question="다음 □ 안에 알맞은 것을 써넣으시오.\n크기가 □인 벡터를 단위벡터라고 한다.",
    choices=None, derived_answer="1", figure=None, difficulty_est=1, confidence=0.9,
    note="단위벡터의 정의: 크기가 1인 벡터.")

# p3
add(id="892e2398", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 12]], [[seg(AD) = 16]]인 직사각형 ABCD에서 [[abs(vec(AO))]]를 구하시오.\n"
              "(단, O는 두 대각선의 교점이다.)"),
    choices=None, derived_answer="10",
    figure=fig("직사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하)와 두 대각선, 교점 O, A에서 O로 향하는 화살표, AB=12·AD=16 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 직사각형과 두 대각선·벡터 화살표",
    note="대각선 AC=20 ⇒ |AO|=10.")

# p12
add(id="196daefb", qtype="short",
    question="다음 그림과 같은 직사각형 ABCD에서 [[seg(AB) = 8]], [[seg(AD) = 6]]일 때, [[abs(vec(CD))]]를 구하시오.",
    choices=None, derived_answer="8",
    figure=fig("직사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하), C에서 D로 향하는 화살표, AB=8·AD=6 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 직사각형과 벡터 화살표",
    note="|CD|=AB=8.")

# p13
add(id="dfe0903c", qtype="short",
    question="다음 그림과 같은 직사각형 ABCD에서 [[seg(AB) = 5]], [[seg(AD) = 12]]일 때, [[abs(vec(BD))]]를 구하시오.",
    choices=None, derived_answer="13",
    figure=fig("직사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하), B에서 D로 향하는 대각선 화살표, AB=5·AD=12 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 직사각형과 대각선 벡터 화살표",
    note="|BD|=√(25+144)=13 (빠른정답 5와 불일치).")

# p14
add(id="7885f44a", qtype="short",
    question="다음 그림과 같이 한 변의 길이가 6인 정삼각형 ABC에서 변 B의 중점을 D라 할 때, [[-vec(AC)]]의 크기를 구하시오.",
    choices=None, derived_answer="6",
    figure=fig("정삼각형 ABC(A 위, B 좌하, C 우하), 변 BC의 중점 D와 선분 AD, BD=DC 표시, AB=6 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 정삼각형과 중점 D·선분 AD",
    note="원문 '변 B의 중점'(오타로 보이나 그대로). |−AC|=|AC|=6 (빠른정답 5와 불일치).")

# p20
add(id="d4fa22ba", qtype="short",
    question=("다음 그림과 같이 [[seg(AB) = 10]], [[seg(AD) = 24]]인 직사각형 ABCD에서 [[abs(vec(AO))]]를 구하시오.\n"
              "(단, O는 두 대각선의 교점이다.)"),
    choices=None, derived_answer="13",
    figure=fig("직사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하)와 두 대각선, 교점 O, A에서 O로 향하는 화살표, AB=10·AD=24 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 직사각형과 두 대각선·벡터 화살표",
    note="대각선 AC=26 ⇒ |AO|=13 (빠른정답 12와 불일치).")

# p22
add(id="c4420920", qtype="short",
    question=("그림과 같이 [[seg(AB) = 3]], [[seg(AC) = 4]], [[angle(A) = deg(90)]]인 직각삼각형 ABC의 두 변 AB, AC 위에 각각 있는 두 점 P, Q가 "
              "다음 조건을 만족시킨다.\n"
              "(가) 두 벡터 [[vec(AB)]], [[vec(AQ)]]의 크기가 서로 같다.\n"
              "(나) 두 벡터 [[vec(CB)]], [[vec(QP)]]의 방향이 서로 같다.\n"
              "삼각형 APQ의 넓이가 [[frac(q,p)]]일 때, [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는서로소인 자연수이다.)"),
    choices=None, derived_answer="35",
    figure=fig("직각삼각형 ABC(A 위, 직각 표시, B 좌하, C 우하), 변 AB 위의 점 P, 변 AC 위의 점 Q, 선분 PQ, AB=3·AC=4 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 직각삼각형과 변 위의 점 P, Q·선분 PQ",
    note="AQ=3, PQ∥BC ⇒ AP=9/4 ⇒ 넓이 27/8 ⇒ p+q=35. 원문 '는서로소인' 띄어쓰기 그대로.")

# p24
add(id="77b089cc", qtype="choice",
    question=("다음 그림과 같이 [[angle(BCD) = deg(90)]]인 사다리꼴 ABCD의 꼭짓점 A에서 변 BC에 내린 수선의 발을 E, 변 CD의 중점을 F라 하고, "
              "두 선분 AC, EF의 교점을 G라 하자. [[seg(AB) = seg(AD) = 3]], [[seg(BC) = 5]]일 때, [[abs(vec(AG))]]의 값은?"),
    choices=["[[frac(sqrt(14), 2)]]", "[[2]]", "[[frac(5 sqrt(14), 9)]]", "[[frac(2 sqrt(14), 3)]]", "[[frac(8,3)]]"],
    derived_answer="④",
    figure=fig("사다리꼴 ABCD(AD∥BC, A 좌상, D 우상, B 좌하, C 우하, ∠C 직각), A에서 BC에 내린 수선의 발 E(직각 표시), CD의 중점 F, AC와 EF의 교점 G, A에서 G로 향하는 화살표, AB=3·AD=3·BC=5 표시"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사다리꼴과 수선·중점·교점 G",
    note="B(0,0),C(5,0),A(2,√5),D(5,√5),F(5,√5/2) ⇒ G=(4,√5/3), AG=(2/3)AC=2√14/3 ⇒ ④ (빠른정답 3과 불일치).")

# p25
add(id="12db95f5", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = 3]], [[seg(AD) = 2]], [[seg(AE) = 1]]인 직육면체에서 "
              "[[pow(abs(vec(AC)), 2) + pow(abs(vec(DF)), 2)]]의 값은?"),
    choices=["[[19]]", "[[21]]", "[[23]]", "[[25]]", "[[27]]"],
    derived_answer="⑤",
    figure=fig("직육면체 ABCD-EFGH(윗면 ABCD: A 앞왼, B 앞오른, C 뒤오른, D 뒤왼; 아랫면 EFGH), 대각선 AC(빨간 화살표)와 DF(파란 화살표), AB=3·AD=2·AE=1 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 직육면체와 두 대각선 벡터",
    note="|AC|²=9+4=13, |DF|²=9+4+1=14 ⇒ 27 ⇒ ⑤ (빠른정답 35와 불일치).")

# p26
add(id="89f31304", qtype="short",
    question="다음 그림과 같은 직육면체에서 [[seg(AB) = 4]], [[seg(AD) = 2]], [[seg(AE) = 3]]일 때, 벡터 [[vec(EB)]]의 크기를 구하시오.",
    choices=None, derived_answer="5",
    figure=fig("직육면체 ABCD-EFGH(윗면 ABCD: A 앞왼, B 앞오른, C 뒤오른, D 뒤왼; 아랫면 EFGH), AB=4·AD=2·AE=3 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 직육면체",
    note="|EB|=√(16+9)=5 (빠른정답 2와 불일치).")

# p31
add(id="2c6b5904", qtype="choice",
    question="그림과 같이 [[seg(AB) = 1]], [[seg(AD) = 2]]인 직사각형 ABCD에서 [[abs(vec(AC))]]의 값은?",
    choices=["[[frac(sqrt(5), 5)]]", "[[frac(2 sqrt(5), 5)]]", "[[frac(3 sqrt(5), 5)]]", "[[frac(4 sqrt(5), 5)]]", "[[sqrt(5)]]"],
    derived_answer="⑤",
    figure=fig("직사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하), A에서 C로 향하는 대각선 화살표"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 직사각형과 대각선 벡터 화살표",
    note="|AC|=√(1+4)=√5 ⇒ ⑤.")

# p33
add(id="7eccc665", qtype="choice",
    question="다음 그림과 같이 한 모서리의 길이가 4인 정팔면체에서 [[abs(vec(AH))]]의 값은?",
    choices=["[[2]]", "[[sqrt(6)]]", "[[2 sqrt(2)]]", "[[sqrt(10)]]", "[[2 sqrt(3)]]"],
    derived_answer="③",
    figure=fig("정팔면체(꼭짓점 A 위, F 아래, 가운데 정사각형 BCDE), 정사각형 BCDE의 대각선 교점 H(직각 표시), A에서 H로 향하는 화살표, 모서리 4 표시"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 정팔면체와 중심 H",
    note="AH=AF/2=정사각형 대각선의 절반=2√2 ⇒ ③ (빠른정답 5와 불일치).")

# p36
add(id="eff09352", qtype="short",
    question="다음 그림과 같은 직육면체에서 [[seg(AB) = 10]], [[seg(AD) = 7]], [[seg(AE) = 3]]일 때, 벡터 [[vec(GH)]]의 크기를 구하시오.",
    choices=None, derived_answer="10",
    figure=fig("직육면체 ABCD-EFGH(윗면 ABCD: A 앞왼, B 앞오른, C 뒤오른, D 뒤왼; 아랫면 EFGH), AB=10·AD=7·AE=3 표시"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 직육면체",
    note="|GH|=AB=10 (빠른정답 3과 불일치).")

# p38
add(id="b0cf18bc", qtype="choice",
    question="다음 그림과 같은 정팔면체에서 다음 중 벡터 [[vec(AB)]]와 크기가 같고 방향이 반대인 것은?",
    choices=["[[vec(AC)]]", "[[vec(CD)]]", "[[vec(FA)]]", "[[vec(FB)]]", "[[vec(FD)]]"],
    derived_answer="⑤",
    figure=fig("정팔면체(꼭짓점 A 위, F 아래, 가운데 정사각형 B(왼)-C(앞)-D(오른)-E(뒤)), A에서 B로 향하는 빨간 화살표"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 정팔면체와 벡터 화살표",
    note="AB=DF ⇒ −AB=FD ⇒ ⑤ (빠른정답 10과 불일치).")

# p40
add(id="4b1b0f46", qtype="choice",
    question="아래 그림과 같은 정육각형에서 세 대각선의 교점을 O라 할 때, 다음 중 서로 같은 벡터끼리 짝지은 것은?",
    choices=["[[vec(DO)]], [[vec(BC)]]", "[[vec(AF)]], [[vec(OB)]]", "[[vec(CD)]], [[vec(FE)]]", "[[vec(OB)]], [[vec(EO)]]", "[[vec(OF)]], [[vec(OC)]]"],
    derived_answer="④",
    figure=fig("정육각형 ABCDEF(A 위, B 좌상, C 좌하, D 아래, E 우하, F 우상)와 세 대각선 AD, BE, CF, 교점 O"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 정육각형과 세 대각선",
    note="OB=EO(B, E가 O에 대해 대칭) ⇒ ④ (빠른정답 3과 불일치).")

# p42
add(id="b69e5abc", qtype="choice",
    question="다음 그림과 같은 전개도를 접어서 만든 정육면체에서 [[vec(AD)]]와 서로 같은 벡터인 것은?",
    choices=["[[vec(BC)]]", "[[vec(BE)]]", "[[vec(DA)]]", "[[vec(EB)]]", "[[vec(FG)]]"],
    derived_answer="②",
    figure=fig("정육면체 전개도: 가로 3칸(왼쪽 위 B, A, H; 아래 C, D, E; F는 셋째 칸 우변 중간), 셋째 칸 위로 2칸(오른쪽 끝 위 G), 둘째 칸 아래로 1칸; A에서 D로 향하는 빨간 대각선 화살표"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정육면체 전개도와 벡터 화살표",
    note="접으면 A(1,1,0),D(2,0,0),B(1,1,1),E(2,0,1) ⇒ AD=BE=(1,−1,0) ⇒ ②.")

# p47
add(id="80c953e1", qtype="choice",
    question=("그림과 같은 마름모 ABCD의 4개의 꼭짓점을 시점과 종점으로 하는 벡터에 대하여 다음 중 벡터 [[vec(AB)]]와 같은 벡터는?"),
    choices=["[[vec(BC)]]", "[[vec(CD)]]", "[[vec(DA)]]", "[[vec(CB)]]", "[[vec(DC)]]"],
    derived_answer="⑤",
    figure=fig("마름모 ABCD(A 위, B 왼, C 아래, D 오른)"),
    difficulty_est=1, confidence=0.85,
    needs_review="도형 표현 불가: 마름모 ABCD",
    note="AB=DC ⇒ ⑤.")

# p54
add(id="6df0bf8c", qtype="choice",
    question=("다음 그림과 같은 삼각형 ABC에서 세 변 AB, BC, CA의 중점을 각각 D, E, F라 할 때, 벡터 [[vec(EB)]]와 서로 같은 벡터를 모두 고르면? (정답 2개)"),
    choices=["[[vec(CE)]]", "[[vec(FA)]]", "[[vec(CF)]]", "[[vec(FD)]]", "[[vec(DE)]]"],
    derived_answer="①, ④",
    figure=fig("직각삼각형 ABC(A 위, B 좌하, C 우하), AB의 중점 D, BC의 중점 E, CA의 중점 F, 선분 DF·DE·EF, E에서 B로 향하는 화살표"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 삼각형과 세 중점을 이은 선분",
    note="EB=CE(길이 BC/2, 왼쪽 방향), FD=−DF, DF∥BC 같은 방향 ⇒ FD=EB ⇒ ①, ④ (빠른정답 4는 한 개만 표기).")

# p55
add(id="51fd67e0", qtype="short",
    question=("다음 그림과 같은 정육각형 ABCDEF에서 세 대각선 AD, BE, CF의 교점 O에 대하여 [[vec(BC) = vec(a)]], [[vec(OE) = vec(b)]]라 하자.\n"
              "벡터 [[vec(a)]]와 서로 같은 벡터의 개수를 [[m]], 벡터 [[vec(b)]]와 크기는 같지만 방향이 반대인 벡터의 개수를 [[n]]이라 할 때, "
              "[[m + n]]의 값을 구하시오."),
    choices=None, derived_answer="7",
    figure=fig("정육각형 ABCDEF(A 위, B 좌상, C 좌하, D 아래, E 우하, F 우상)와 세 대각선 AD, BE, CF, 교점 O, B→C 화살표 a, O→E 화살표 b"),
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 정육각형과 세 대각선·벡터 화살표",
    note="a와 같은 벡터(자기 자신 제외): AO, OD, FE ⇒ m=3; b와 반대: EO, OB, FA, DC ⇒ n=4 ⇒ 7 (빠른정답 3과 불일치; 자기 자신 포함 여부 해석 차 가능).")

# ───────────── 공간에서 점의 좌표 ─────────────
# p4
add(id="58b5df86", qtype="choice",
    question=("다음 그림의 직육면체에서 꼭짓점 P를 [[y]]축에 대하여 대칭이동한 점의 좌표를 [[vcomp(a, b, c)]]라 할 때, "
              "[[a + 3b - 2c]]의 값은?"),
    choices=["[[22]]", "[[23]]", "[[24]]", "[[25]]", "[[26]]"],
    derived_answer="②",
    figure=fig("좌표공간의 직육면체: 한 꼭짓점이 원점 O, x축 방향 길이 2, y축 방향 길이 5, z축 방향 길이 5, 꼭짓점 P는 (2, 5, 5) 위치"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 좌표공간 직육면체와 꼭짓점 P",
    note="P(2,5,5) → y축 대칭 (−2,5,−5) ⇒ −2+15+10=23 ⇒ ② (빠른정답 −12와 불일치).")

# p8
add(id="97b82013", qtype="short",
    question=("밑면이 정사각형이고 모든 모서리의 길이가 같은 사각뿔 A−BCDE와 밑면이 정삼각형이고 높이가 사각뿔과 같은 삼각기둥 FGH−IBE를 "
              "한 모서리 BE를 공유하도록 붙여놓았다.\n"
              "이 입체도형을 다음 그림과 같이 점 B가 원점, 모서리 BE가 [[y]]축, 밑면 IBCDE가 xy평면 위에 오도록 좌표공간에 놓았더니 "
              "점 A의 [[z]]좌표가 [[9 sqrt(2)]]이었을 때, F[[vcomp(a, b, c)]]이다. [[pow(a,2) + pow(b,2) - pow(c,2)]]의 값을 구하시오.\n"
              "(단, 점 C의 [[x]]좌표와 점 D의 [[y]]좌표는 각각 양수이다.)"),
    choices=None, derived_answer="162",
    figure=fig("좌표공간: 원점 B, y축 위의 E, xy평면 위의 정사각형 BCDE(C는 x축 위)와 그 위의 사각뿔 꼭짓점 A, BE 반대쪽의 정삼각형 IBE 위에 놓인 삼각기둥 FGH−IBE(G는 B 위, H는 E 위, F는 I 위)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표공간의 사각뿔+삼각기둥 결합 입체",
    note="모서리 18(높이 9√2), I(−9√3, 9, 0), F(−9√3, 9, 9√2) ⇒ 243+81−162=162 (빠른정답 5와 불일치).")

# p11
add(id="ad5bf0d7", qtype="short",
    question=("점 A[[vcomp(-4, 3, 9)]]와 [[z]]축에 대하여 대칭인 점에서 xy평면에 내린 수선의 발의 좌표를 [[vcomp(a, b, c)]]라 할 때, "
              "[[a + b + c]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=1, confidence=0.9,
    note="(4,−3,9) → (4,−3,0) ⇒ 1.")

# p12
add(id="942f9854", qtype="choice",
    question=("다음 그림의 직육면체에서 꼭짓점 P를 [[z]]축에 대하여 대칭이동한 점의 좌표를 [[vcomp(a, b, c)]]라 할 때, "
              "[[2a + 3b - c]]의 값은?"),
    choices=["[[12]]", "[[6]]", "[[-6]]", "[[-12]]", "[[-18]]"],
    derived_answer="⑤",
    figure=fig("좌표공간의 직육면체: 한 꼭짓점이 원점 O, x축 방향 길이 3, y축 방향 길이 2, z축 방향 길이 6, 꼭짓점 P는 (3, 2, 6) 위치"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 좌표공간 직육면체와 꼭짓점 P",
    note="P(3,2,6) → z축 대칭 (−3,−2,6) ⇒ −6−6−6=−18 ⇒ ⑤.")

# p13
add(id="f3bdd355", qtype="short",
    question=("점 A[[vcomp(-1, 7, 5)]]를 zx평면에 대하여 대칭이동한 점을 B라 하고, 점 B를 [[y]]축에 대하여 대칭이동한 점을 "
              "C[[vcomp(a, b, c)]]라 할 때, [[a - b - c]]의 값을 구하시오."),
    choices=None, derived_answer="13", figure=None, difficulty_est=1, confidence=0.9,
    note="B(−1,−7,5), C(1,−7,−5) ⇒ 1+7+5=13 (빠른정답 3과 불일치).")

# p17
add(id="450659c8", qtype="short",
    question="점 A[[vcomp(-3, 6, 2)]]와 zx평면에 대하여 대칭인 점의 좌표를 [[vcomp(a, b, c)]]라 할 때, [[a b c]]의 값을 구하시오.",
    choices=None, derived_answer="36", figure=None, difficulty_est=1, confidence=0.9,
    note="(−3,−6,2) ⇒ abc=36.")

# p18
add(id="5fbfaeff", qtype="choice",
    question=("좌표공간의 점 P[[vcomp(2, 2, 3)]]을 yz평면에 대하여 대칭이동시킨 점을 Q라 하자.\n두 점 P와 Q 사이의 거리는?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2015년 9월 고3 이과 4번/3점]. Q(−2,2,3) ⇒ PQ=4 ⇒ ④ (빠른정답 5와 불일치).")

# p20
add(id="8fffb91f", qtype="choice",
    question="좌표공간의 점 A[[vcomp(8, 6, 2)]]를 xy평면에 대하여 대칭이동한 점을 B라 할 때, 선분 AB의 길이는?",
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2023년 9월 고3 기하 23번/2점]. B(8,6,−2) ⇒ AB=4 ⇒ ④ (빠른정답 36과 불일치).")

# p32
add(id="c329ad33", qtype="choice",
    question=("좌표공간의 점 A[[vcomp(4, 3, -9)]]를 xy평면에 대하여 대칭이동한 점을 B, 점 A를 원점에 대하여 대칭이동한 점을 C라 할 때, "
              "선분 BC의 길이는?"),
    choices=["[[10]]", "[[12]]", "[[14]]", "[[16]]", "[[18]]"],
    derived_answer="①", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2025년 9월 고3 기하 25번/3점]. B(4,3,9), C(−4,−3,9) ⇒ BC=√(64+36)=10 ⇒ ① (빠른정답 4와 불일치).")

# p35
add(id="05b88707", qtype="choice",
    question=("좌표공간의 두 점 A[[vcomp(1, 0, 3)]], B[[vcomp(-3, 3, 0)]]에서 같은 거리에 있는 [[y]]축 위의 점의 좌표가 [[vcomp(0, a, 0)]]일 때, "
              "[[a]]의 값은?"),
    choices=["[[frac(2,3)]]", "[[1]]", "[[frac(4,3)]]", "[[frac(5,3)]]", "[[2]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 11월 고3 이과 3번 변형]. a²+10=a²−6a+18 ⇒ a=4/3 ⇒ ③ (빠른정답 1과 불일치).")

# p36
add(id="1de33b61", qtype="choice",
    question=("좌표공간의 두 점 A[[vcomp(2, 0, 1)]], B[[vcomp(3, 2, 0)]]에서 같은 거리에 있는 [[y]]축 위의 점의 좌표가 [[vcomp(0, a, 0)]]일 때, "
              "[[a]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2019년 11월 고3 이과 3번/2점]. a²+5=a²−4a+13 ⇒ a=2 ⇒ ② (빠른정답 7과 불일치).")

# p40
add(id="29dd5a20", qtype="choice",
    question=("두 점 A[[vcomp(1, 2, -5)]], B[[vcomp(5, -2, 3)]]에서 같은 거리에 있는 [[y]]축 위의 점의 좌표는 [[vcomp(0, a, 0)]]이다. "
              "상수 [[a]]의 값은?"),
    choices=["[[-2]]", "[[-1]]", "[[0]]", "[[1]]", "[[2]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="a²−4a+30=a²+4a+38 ⇒ a=−1 ⇒ ②.")

# p41
add(id="f3b7dc2f", qtype="choice",
    question=("두 점 A[[vcomp(1, 2, 4)]], B[[vcomp(-2, 5, 1)]]과 [[y]]축 위의 점 P에 대하여 [[seg(AP) = seg(BP)]]일 때, "
              "점 P의 [[y]]좌표의 값은?"),
    choices=["[[frac(7,6)]]", "[[frac(6,5)]]", "[[frac(5,4)]]", "[[frac(4,3)]]", "[[frac(3,2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="a²−4a+21=a²−10a+30 ⇒ a=3/2 ⇒ ⑤.")

# p45
add(id="1f52ee5d", qtype="choice",
    question=("두 점 A[[vcomp(0, 3, 6)]], B[[vcomp(6, 0, 3)]]가 있다. 삼각형 ABC가 정삼각형이 되도록 xy평면 위에 점 C[[vcomp(a, b, 0)]]을 잡을 때, "
              "두 정수 [[a]], [[b]]에 대하여 [[a + b]]의 값은?"),
    choices=["[[-12]]", "[[-9]]", "[[0]]", "[[9]]", "[[12]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="AB²=54, b=2a, 5a²−12a−9=0 ⇒ a=3, b=6 ⇒ 9 ⇒ ④.")

# p48
add(id="ce6a3207", qtype="short",
    question=("세 점 A[[vcomp(1, 2, 1)]], B[[vcomp(1, -1, -2)]], C[[vcomp(-1, 2, 3)]]에서 같은 거리에 있는 xy평면 위의 점 P의 좌표를 "
              "[[vcomp(a, b, 0)]]이라 할 때, [[b - a]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="PA=PB ⇒ b=0, PA=PC ⇒ a=−2 ⇒ b−a=2 (빠른정답 4와 불일치).")

# p49
add(id="fb2bc5b3", qtype="short",
    question=("세 점 A[[vcomp(3, 3, -1)]], B[[vcomp(3, 2, 2)]], C[[vcomp(-2, 3, 4)]]에서 같은 거리에 있는 xy평면 위의 점 P의 좌표를 "
              "[[vcomp(a, b, 0)]]이라 할 때, [[b - a]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="PA=PB ⇒ b=1, PA=PC ⇒ a=−1 ⇒ b−a=2 (빠른정답 deg(45)와 불일치).")

# p51
add(id="c3ea71b6", qtype="choice",
    question=("두 점 A[[vcomp(a, 1, -2)]], B[[vcomp(b, -2, 4)]]를 지나는 직선이 yz평면과 이루는 각의 크기가 [[deg(45)]]일 때, "
              "선분 AB의 zx평면 위로의 정사영의 길이는?"),
    choices=["[[3]]", "[[3 sqrt(3)]]", "[[6]]", "[[9]]", "[[6 sqrt(3)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="yz평면 정사영 길이 3√5, 45° ⇒ (b−a)²=45 ⇒ zx평면 정사영 √(45+36)=9 ⇒ ④.")

# p56
add(id="a5b5cfc0", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = seg(AC) = 7]], [[seg(BC) = 4]]인 삼각형 ABC가 xy평면 위에 있고, 점 P[[vcomp(1, 1, 6)]]의 xy평면 위로의 정사영 Q는 "
              "삼각형 ABC의 무게중심과 일치한다. 점 P에서 직선 BC까지의 거리는?"),
    choices=["[[2 sqrt(10)]]", "[[sqrt(41)]]", "[[sqrt(42)]]", "[[sqrt(43)]]", "[[2 sqrt(11)]]"],
    derived_answer="②",
    figure=fig("xy평면(평행사변형으로 표시) 위의 삼각형 ABC, 삼각형 내부의 점 Q, Q 위쪽의 점 P와 점선 PQ"),
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: xy평면 위 삼각형과 정사영 점 P, Q",
    note="A에서 BC까지 3√5, 무게중심까지 √5, PQ=6 ⇒ √41 ⇒ ② (빠른정답 5와 불일치).")

# p57
add(id="817eeadd", qtype="short",
    question=("세 점 A[[vcomp(1, 1, 1)]], B[[vcomp(4, 1, 1)]], C[[vcomp(1, 2, 0)]]을 꼭짓점으로 하는 삼각형 ABC와 zx평면이 이루는 예각의 크기를 "
              "[[theta]]라 할 때, [[8 pow(cos(theta), 2)]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=3, confidence=0.9,
    note="법선 (0,3,3), zx평면 법선 (0,1,0) ⇒ cos θ=1/√2 ⇒ 8cos²θ=4.")

# p58
add(id="6005d997", qtype="choice",
    question=("세 점 A[[vcomp(0, 0, 1)]], B[[vcomp(3, 2, 0)]], C[[vcomp(0, 2, 0)]]에 대하여 선분 AB 위의 한 점 P에서 선분 BC에 내린 수선의 발을 "
              "H라 할 때, [[seg(PH) = frac(sqrt(5), 2)]]이다. 이때 삼각형 PBH의 xy평면 위로의 정사영의 넓이는?"),
    choices=["[[frac(1,2)]]", "[[frac(1,2)]]", "[[frac(3,4)]]", "[[1]]", "[[frac(5,4)]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="P=(3/2,1,1/2), H=(3/2,2,0) ⇒ 정사영 넓이 (1/2)(1)(3/2)=3/4 ⇒ ③ (빠른정답 91과 불일치). 선지 ①·②가 원문에 모두 1/2로 인쇄됨(그대로 전사).")

# p59
add(id="bf2f5a13", qtype="choice",
    question=("다음 그림과 같이 좌표공간에 세 점 A[[vcomp(0, 0, 5)]], B[[vcomp(13, 12, 0)]], C[[vcomp(0, 12, 0)]]이 있다. 선분 AB 위의 한 점 P에서 "
              "선분 BC에 내린 수선의 발을 H라 할 때, [[seg(PH) = 5]]이다. 삼각형 PBH의 xy평면 위로의 정사영의 넓이는?"),
    choices=["[[frac(60,13)]]", "[[frac(90,13)]]", "[[frac(120,13)]]", "[[frac(150,13)]]", "[[frac(180,13)]]"],
    derived_answer="④",
    figure=fig("좌표공간: z축 위의 점 A, y축 위의 점 C, xy평면 위의 점 B, 선분 AB 위의 점 P, P에서 BC에 내린 수선의 발 H(직각 표시), 삼각형 PBH"),
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 좌표공간의 점 A, B, C, P, H와 삼각형 PBH",
    note="PH=13(1−t)=5 ⇒ t=8/13, P(8,96/13,25/13), H(8,12,0) ⇒ 넓이 (1/2)(60/13)(5)=150/13 ⇒ ④ (빠른정답 2와 불일치).")

# p60
add(id="ad2a2ec9", qtype="short",
    question=("서로 다른 네 점 A[[vcomp(2, 0, 0)]], B[[vcomp(0, 4, 0)]], C[[vcomp(0, 0, 2)]], D[[vcomp(0, k, 0)]]에 대하여 두 평면 [[alpha]], [[beta]]가 "
              "다음 조건을 만족한다.\n"
              "(가) 평면 [[alpha]]는 세 점 A, B, C를 지난다.\n"
              "(나) 평면 [[beta]]는 세 점 A, C, D를 지난다.\n"
              "(다) 두 평면 [[alpha]], [[beta]]가 이루는 각의 크기는 평면 [[beta]]와 xz평면이 이루는 각의 크기와 같다.\n"
              "두 평면 [[alpha]], [[beta]]가 이루는 각의 크기를 [[theta]]라 할 때, [[pow(cos(theta), 2) = frac(q,p)]]이다. [[p + q]]의 값을 구하시오.\n"
              "(단, [[0 < k < 4]]이고, [[p]], [[q]]는 서로소인 자연수이다.)"),
    choices=None, derived_answer="5", figure=None, difficulty_est=4, confidence=0.85,
    note="법선 α:(2,1,2), β:(k,2,k); (4k+2)/3=2 ⇒ k=1 ⇒ cos²θ=4/6=2/3 ⇒ p+q=5 (빠른정답 4와 불일치).")

# p61
add(id="08a22811", qtype="short",
    question=("점 P[[vcomp(a, b, 5)]]에서 [[y]]축에 내린 수선의 발을 Q, [[x]]축에 내린 수선의 발을 R, 점 P와 yz평면에 대하여 대칭인 점을 S라 하자. "
              "사면체 PQSR의 부피가 20일 때, 원점과 점 P 사이의 거리의 최솟값을 구하시오.\n(단, [[a != 0]], [[b != 0]])"),
    choices=None, derived_answer="7", figure=None, difficulty_est=4, confidence=0.85,
    note="부피 5|ab|/3=20 ⇒ |ab|=12; OP²=a²+b²+25≥2|ab|+25=49 ⇒ 7.")

# p62
add(id="ee0e8ece", qtype="short",
    question=("네 점 A[[vcomp(1, 0, a)]], B[[vcomp(3, 0, a)]], C[[vcomp(3, 4, b)]], D[[vcomp(1, 4, b)]]를 꼭짓점으로 하는 사각형 ABCD를 포함하는 평면과 "
              "xy평면이 이루는 예각의 크기가 [[theta]]일 때, [[cos(theta) = frac(4,5)]]이다. [[b - a]]의 값을 구하시오. (단, [[b > a]])"),
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.9,
    note="직사각형 넓이 2√(16+(b−a)²), 정사영 넓이 8 ⇒ 4/√(16+(b−a)²)=4/5 ⇒ b−a=3 (빠른정답 4와 불일치).")

# p65
add(id="402fb7b7", qtype="choice",
    question=("그림과 같이 [[seg(AB) = seg(AC) = 5]], [[seg(BC) = 2 sqrt(7)]]인 삼각형 ABC가 xy평면 위에 있고, 점 P[[vcomp(1, 1, 4)]]의 xy평면 위로의 "
              "정사영 Q는 삼각형 ABC의 무게중심과 일치한다. 점 P에서 직선 BC까지의 거리는?"),
    choices=["[[3 sqrt(2)]]", "[[sqrt(19)]]", "[[2 sqrt(5)]]", "[[sqrt(21)]]", "[[sqrt(22)]]"],
    derived_answer="①",
    figure=fig("xy평면(평행사변형으로 표시) 위의 삼각형 ABC, 삼각형 내부의 점 Q, Q 위쪽의 점 P와 점선 PQ"),
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: xy평면 위 삼각형과 정사영 점 P, Q",
    note="출처 [2015년 7월 고3 이과 15번/4점]. A에서 BC까지 3√2, 무게중심까지 √2, PQ=4 ⇒ √18=3√2 ⇒ ① (빠른정답 3과 불일치).")

# p70
add(id="23610939", qtype="short",
    question=("점 P[[vcomp(3, -2, 8)]]에서 xy평면에 내린 수선의 발을 H라 하자. xy평면 위의 한 직선 [[l]]과 점 P 사이의 거리가 17일 때, "
              "점 H와 직선 [[l]] 사이의 거리를 구하시오."),
    choices=None, derived_answer="15", figure=None, difficulty_est=2, confidence=0.9,
    note="PH=8 ⇒ √(289−64)=15 (빠른정답 3과 불일치).")

# p73
add(id="03eda880", qtype="choice",
    question=("좌표공간의 점 P[[vcomp(8, 2, 6)]]에서 xy평면에 내린 수선의 발을 H라 하자. xy평면 위의 한 직선 [[l]]과 점 P 사이의 거리가 "
              "[[6 sqrt(2)]]일 때, 점 H와 직선 [[l]] 사이의 거리는?"),
    choices=["[[2]]", "[[4]]", "[[6]]", "[[8]]", "[[10]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="PH=6 ⇒ √(72−36)=6 ⇒ ③.")

# p76
add(id="ba4a0c13", qtype="choice",
    question=("좌표공간에서 점 A[[vcomp(1, 4, 3)]]을 [[x]]축에 대하여 대칭이동한 점을 B라 하고, 점 A를 xy평면에 대하여 대칭이동한 점을 C라 하자. "
              "세 점 A, B, C를 지나는 원의 반지름의 길이는?"),
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="B(1,−4,−3), C(1,4,−3): ∠C=90°, AB=10 ⇒ 반지름 5 ⇒ ② (빠른정답 3과 불일치).")

# p78
add(id="b15e3ab7", qtype="choice",
    question=("좌표공간의 두 점 A[[vcomp(-2, 5, 6)]], B[[vcomp(2, 2, 0)]]에 대하여 xy평면에서 점 B를 중심으로 하고 [[x]]축과 [[y]]축에 모두 접하는 "
              "원 위의 점을 P라 하자. 선분 AP의 길이의 최솟값은?"),
    choices=["[[3 sqrt(2)]]", "[[3 sqrt(3)]]", "[[6]]", "[[3 sqrt(5)]]", "[[3 sqrt(6)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="원 반지름 2, A의 정사영 (−2,5,0)에서 B까지 5 ⇒ 평면 최소 3, 높이 6 ⇒ √45=3√5 ⇒ ④ (빠른정답 10과 불일치).")

# p83
add(id="c94d96ea", qtype="choice",
    question=("좌표공간의 점 P[[vcomp(3, 5, 4)]]에서 xy평면에 내린 수선의 발을 H라 하자. xy평면 위의 한 직선 [[l]]과 점 P 사이의 거리가 "
              "[[4 sqrt(2)]]일 때,\n점 H와 직선 [[l]] 사이의 거리는?"),
    choices=["[[3]]", "[[sqrt(10)]]", "[[2 sqrt(3)]]", "[[sqrt(15)]]", "[[4]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2014년 10월 고3 이과 9번/3점]. PH=4 ⇒ √(32−16)=4 ⇒ ⑤ (빠른정답 16과 불일치).")

# p85
add(id="805bc76b", qtype="short",
    question="두 점 A[[vcomp(3, 4, 2)]], B[[vcomp(5, 7, 4)]]와 xy평면 위의 점 P에 대하여 [[seg(AP) + seg(BP)]]의 최솟값을 구하시오.",
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.9,
    note="B′(5,7,−4) ⇒ AB′=√(4+9+36)=7 (빠른정답 3과 불일치).")

# p86
add(id="fdb5e1a3", qtype="short",
    question="두 점 A[[vcomp(2, 3, 0)]], B[[vcomp(-1, 1, 0)]]과 [[x]]축 위의 점 P에 대하여 [[seg(AP) + seg(BP)]]의 최솟값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.9,
    note="B′(−1,−1,0) ⇒ AB′=√(9+16)=5.")

# p87
add(id="13d8e2f3", qtype="short",
    question="두 점 A[[vcomp(-3, 7, 5)]], B[[vcomp(3, 2, 3)]]과 zx평면 위를 움직이는 점 P에 대하여 [[seg(AP) + seg(PB)]]의 최솟값을 구하시오.",
    choices=None, derived_answer="11", figure=None, difficulty_est=2, confidence=0.9,
    note="B′(3,−2,3) ⇒ AB′=√(36+81+4)=11.")

# p88
add(id="5eb6e794", qtype="choice",
    question=("좌표공간의 두 점 A[[vcomp(-1, 3, a)]], B[[vcomp(2, 2, 1)]]과 zx평면 위의 점 P에 대하여 [[seg(AP) + seg(BP)]]의 최솟값이 [[sqrt(43)]]일 때, "
              "양수 [[a]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="B′(2,−2,1): 9+25+(a−1)²=43 ⇒ a=4 ⇒ ④ (빠른정답 3과 불일치).")

# p89
add(id="131cfbd2", qtype="choice",
    question=("두 점 A[[vcomp(-1, 1, -2)]], B[[vcomp(-1, a, 2)]]와 yz평면 위를 움직이는 점 P에 대하여 [[seg(AP) + seg(PB)]]의 최솟값이 "
              "[[2 sqrt(6)]]일 때, 양수 [[a]]의 값은?"),
    choices=["[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="B′(1,a,2): 4+(a−1)²+16=24 ⇒ a=3 ⇒ ② (빠른정답 5와 불일치).")

# p90
add(id="86e725da", qtype="choice",
    question="두 점 A[[vcomp(0, 3, 4)]], B[[vcomp(0, 4, 5)]]와 [[y]]축 위를 움직이는 점 P에 대하여 [[seg(AP) + seg(PB)]]의 최솟값은?",
    choices=["[[9]]", "[[sqrt(82)]]", "[[sqrt(83)]]", "[[2 sqrt(21)]]", "[[sqrt(85)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="yz평면 안에서 B를 y축 대칭 (0,4,−5) ⇒ √(1+81)=√82 ⇒ ② (빠른정답 11과 불일치).")

# p92
add(id="6fafde9b", qtype="choice",
    question="두 점 A[[vcomp(3, -1, 2)]], B[[vcomp(-2, 3, 1)]]과 xy평면 위의 점 P에 대하여 [[seg(AP) + seg(BP)]]의 최솟값은?",
    choices=["[[4]]", "[[3 sqrt(2)]]", "[[5]]", "[[4 sqrt(2)]]", "[[5 sqrt(2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="B′(−2,3,−1) ⇒ √(25+16+9)=5√2 ⇒ ⑤ (빠른정답 2와 불일치).")

# p93
add(id="4e05e9ea", qtype="choice",
    question="두 점 A[[vcomp(2, -4, -1)]], B[[vcomp(-3, -1, 2)]]와 zx평면 위를 움직이는 점 P에 대하여 [[seg(AP) + seg(PB)]]의 최솟값은?",
    choices=["[[sqrt(55)]]", "[[2 sqrt(14)]]", "[[sqrt(57)]]", "[[sqrt(58)]]", "[[sqrt(59)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="B′(−3,1,2) ⇒ √(25+25+9)=√59 ⇒ ⑤ (빠른정답 2와 불일치).")

# p94
add(id="1e752136", qtype="choice",
    question="두 점 A[[vcomp(-3, -1, 4)]], B[[vcomp(-2, 2, -sqrt(5))]]와 [[y]]축 위를 움직이는 점 P에 대하여 [[seg(AP) + seg(PB)]]의 최솟값은?",
    choices=["[[6 sqrt(2)]]", "[[sqrt(73)]]", "[[sqrt(74)]]", "[[5 sqrt(3)]]", "[[2 sqrt(19)]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="y축까지 거리 A:5, B:3, y좌표 차 3 ⇒ √((5+3)²+3²)=√73 ⇒ ② (빠른정답 3과 불일치).")

# p95
add(id="90e20b75", qtype="choice",
    question=("좌표공간의 두 점 A[[vcomp(1, 4, 3)]], B[[vcomp(1, 5, 2)]]와 xy평면 위를 움직이는 점 P, yz평면 위를 움직이는 점 Q에 대하여 "
              "[[seg(AP) + seg(PQ) + seg(QB)]]의 최솟값은?"),
    choices=["[[3 sqrt(3)]]", "[[2 sqrt(7)]]", "[[sqrt(29)]]", "[[sqrt(30)]]", "[[sqrt(31)]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.9,
    note="A′(1,4,−3), B′(−1,5,2) ⇒ √(4+1+25)=√30 ⇒ ④ (빠른정답 5와 불일치).")

# p96
add(id="0f5b1bac", qtype="short",
    question=("두 점 A[[vcomp(1, 4, 2)]], B[[vcomp(3, 3, -6)]]과 yz평면 위의 점 P, xy평면 위의 점 Q에 대하여 [[seg(AP) + seg(PQ) + seg(QB)]]의 "
              "최솟값을 구하시오."),
    choices=None, derived_answer="sqrt(33)", figure=None, difficulty_est=3, confidence=0.9,
    note="A′(−1,4,2), B′(3,3,6) ⇒ √(16+1+16)=√33 (빠른정답 5와 불일치).")

# p97
add(id="5c7a04a6", qtype="short",
    question=("두 점 A[[vcomp(4, 2, 1)]], B[[vcomp(-1, a, 1)]]과 zx평면 위를 움직이는 점 P에 대하여 [[seg(AP) + seg(PB)]]의 최솟값이 [[sqrt(41)]]일 때, "
              "양수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="B′(−1,−a,1): 25+(2+a)²=41 ⇒ a=2.")

# p99 — 한 이미지에 별개 문항 2개(id 2개): d45d494c=위(선택형), bf45a8cf=아래(단답형) (draft_a 대응 기준)
add(id="d45d494c", qtype="choice",
    question=("두 점 A[[vcomp(-2, -2, 3)]], B[[vcomp(a, 2, 1)]]과 xy평면 위의 점 P에 대하여 [[seg(AP) + seg(BP)]]의 최솟값이 9일 때, "
              "양수 [[a]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    note="같은 쪽 위 문항(draft_a 대응). B′(a,2,−1): (a+2)²+16+16=81 ⇒ a=5 ⇒ ⑤ (빠른정답 9와 불일치).")
add(id="bf45a8cf", qtype="short",
    question=("두 점 A[[vcomp(5, -4, 3)]], B[[vcomp(7, 2, 6)]]과 xy평면 위를 움직이는 점 P에 대하여 삼각형 ABP의 둘레의 길이의 최솟값을 구하시오."),
    choices=None, derived_answer="18", figure=None, difficulty_est=2, confidence=0.85,
    note="같은 쪽 아래 문항(draft_a 대응). AB=7, B′(7,2,−6) ⇒ AB′=11 ⇒ 7+11=18 (빠른정답 9와 불일치).")

# ───────────── 벡터의 실수배 ─────────────
# p21
add(id="f494bbf1", qtype="short",
    question=("다음 그림과 같이 일정한 간격의 평행선으로 이루어진 도형 위에 네 점 A, B, C, D가 있다. [[vec(AD) = m vec(AB) + n vec(AC)]]일 때, "
              "실수 [[m]], [[n]]에 대하여 [[2m + 15n]]의 값을 구하시오."),
    choices=None, derived_answer="10",
    figure=fig("가로 4칸·세로 4칸의 평행사변형 격자: A는 왼쪽 변 위(아래에서 2칸), B는 아랫변 위(왼쪽에서 1칸), C는 오른쪽 변 위(아래에서 1칸), D는 윗변 위(왼쪽에서 2칸)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형 격자 위의 네 점",
    note="격자좌표 A(0,2),B(1,0),C(4,1),D(2,4): AD=(2,2)=m(1,−2)+n(4,−1) ⇒ m=−10/7, n=6/7 ⇒ 2m+15n=10.")

# p28
add(id="60411c1b", qtype="short",
    question=("다음 그림과 같이 일정한 간격의 평행선으로 이루어진 도형 위에 네 점 A, B, C, D가 있다. [[vec(AD) = p vec(AB) + q vec(AC)]]일 때, "
              "실수 [[p]], [[q]]에 대하여 [[7(p + q)]]의 값을 구하시오."),
    choices=None, derived_answer="11",
    figure=fig("가로 4칸·세로 3칸의 평행사변형 격자: A는 왼쪽 변 위(아래에서 1칸), B는 아랫변 위(왼쪽에서 2칸), C는 윗변 위(왼쪽에서 3칸), D는 오른쪽 변 위(아래에서 2칸)"),
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형 격자 위의 네 점",
    note="격자좌표 A(0,1),B(2,0),C(3,3),D(4,2): AD=(4,1)=p(2,−1)+q(3,2) ⇒ p=5/7, q=6/7 ⇒ 7(p+q)=11.")

# p40
add(id="ba2ab8ce", qtype="short",
    question=("다음 그림과 같이 중심이 O인 원에 내접하는 정팔각형 ABCDEFGH에 대하여 "
              "[[vec(AB) + vec(AC) + vec(AD) + vec(AE) + vec(AF) + vec(AG) + vec(AH) = k vec(OA)]]일 때, 실수 [[k]]의 값을 구하시오.\n"
              "(단, [[vec(OA) + vec(OB) + vec(OC) + vec(OD) + vec(OE) + vec(OF) + vec(OG) + vec(OH) = vec(0)]])"),
    choices=None, derived_answer="-8",
    figure=fig("원에 내접하는 정팔각형 ABCDEFGH(A 위, 시계 반대 방향으로 B, C, D, E(아래), F, G, H)와 중심 O"),
    difficulty_est=2, confidence=0.85,
    needs_review="도형 표현 불가: 원에 내접하는 정팔각형",
    note="Σ(OX−OA)=(0−OA)−7OA=−8OA ⇒ k=−8.")

# p45
add(id="d713b386", qtype="choice",
    question=("다음 그림과 같이 변 AD가 변 BC와 평행하고 [[angle(CBA) = angle(DCB)]]인 사다리꼴 ABCD가 있다.\n"
              "[[abs(vec(AD)) = 4]], [[abs(vec(BC)) = 8]], [[abs(vec(AB) + vec(AC)) = 6 sqrt(2)]]일 때, [[abs(vec(BD))]]의 값은?"),
    choices=["[[sqrt(42)]]", "[[2 sqrt(11)]]", "[[sqrt(46)]]", "[[4 sqrt(3)]]", "[[5 sqrt(2)]]"],
    derived_answer="⑤",
    figure=fig("등변사다리꼴 ABCD(윗변 AD, 아랫변 BC, ∠B=∠C 표시)"),
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 등변사다리꼴 ABCD",
    note="출처 [2021년 10월 고3 기하 26번 변형]. B(0,0),C(8,0),A(2,h),D(6,h): |AB+AC|²=16+4h²=72 ⇒ h²=14 ⇒ |BD|=√(36+14)=5√2 ⇒ ⑤ (빠른정답 8과 불일치).")

# p59
add(id="591fc4db", qtype="short",
    question=("서로 평행하지 않고 영벡터가 아닌 두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[vec(OA) = vec(a)]], [[vec(OB) = vec(b)]], "
              "[[vec(OC) = k vec(a) + 2 vec(b)]]이다. [[3 vec(AC) = m vec(AB)]]일 때, 실수 [[k]], [[m]]에 대하여 [[k + 2m]]의 값을 구하시오."),
    choices=None, derived_answer="11", figure=None, difficulty_est=2, confidence=0.9,
    note="3((k−1)a+2b)=m(b−a) ⇒ m=6, k=−1 ⇒ k+2m=11 (빠른정답 20과 불일치).")

# p75
add(id="ebdb38c9", qtype="short",
    question="서로 다른 세 점 A, B, C에 대하여 [[abs(vec(AB)) = 4]], [[vec(AC) = 5 vec(AB)]]일 때, [[abs(vec(BC))]]를 구하시오.",
    choices=None, derived_answer="16", figure=None, difficulty_est=1, confidence=0.9,
    note="BC=AC−AB=4AB ⇒ 16.")

# p85
add(id="2d460767", qtype="choice",
    question=("그림과 같은 평행사변형 ABCD에서 변 AB의 중점을 P, 대각선 DB를 [[ratio(m, 1)]]로 내분하는 점을 Q라 하자.\n"
              "세 점 P, Q, C가 한 직선 위에 있을 때, 실수 [[m]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②",
    figure=fig("평행사변형 ABCD(A 좌상, D 우상, B 좌하, C 우하), 변 AB의 중점 P, 대각선 DB, 선분 PC와 DB의 교점 Q"),
    difficulty_est=3, confidence=0.85,
    needs_review="도형 표현 불가: 평행사변형과 대각선·교점 Q",
    note="B 기준 Q=(a+c)/(m+1), P=a/2, C=c 공선 ⇒ m=2 ⇒ ②.")
