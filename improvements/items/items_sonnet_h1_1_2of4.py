# -*- coding: utf-8 -*-
# esc_sonnet_h1-1_2of4 — 이미지 기준 전사 (81 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

def N(*xs):  # 숫자 선지
    return ["[[%s]]" % x for x in xs]

CH_G3 = ["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ"]

# ───────────────────────── 행렬 (260828_행렬) ─────────────────────────
# p63
add(id="5a1ce06d", qtype="choice",
    question=("이차정사각행렬 [[A]]의 [[point(i, j)]]성분 [[sub(a,i,j)]]를 다음과 같이 정의할 때, 행렬 [[A]]의 모든 성분의 합은?\n"
              "[[sub(a,i,j)]] = (다항식 [[2 pow(x,3) - 3 pow(x,2) + 2]]를 [[x - (2i - j)]]로 나눈 나머지)"),
    choices=N(36, 37, 38, 39, 40), derived_answer="③", figure=None, difficulty_est=3,
    note="a_ij=f(2i−j), f(1)+f(0)+f(3)+f(2)=1+2+29+6=38 → ③.")

# p66
add(id="c17bea7b", qtype="choice",
    question=("이차정사각행렬 [[A]]의 [[point(i, j)]]성분 [[sub(a,i,j)]]를 이차함수 [[y = pow(x,2) - 2(i + j) x + 9]]의 그래프와 "
              "[[x]]축이 만나는 점의 개수로 정의할 때, 행렬 [[A]]는?"),
    choices=["[[mat(2,2, 0,1, 1,1)]]", "[[mat(2,2, 0,1, 1,2)]]", "[[mat(2,2, 0,2, 2,1)]]", "[[mat(2,2, 1,0, 0,2)]]", "[[mat(2,2, 1,1, 2,0)]]"],
    derived_answer="②", figure=None, difficulty_est=2,
    note="출처 [2011년 9월 고2 문과 4번/3점]. D/4=(i+j)²−9: (1,1)0,(1,2)1,(2,1)1,(2,2)2 → ②.")

# p67
add(id="8c7511a5", qtype="choice",
    question=("이차정사각행렬 [[A]]의 [[point(m, n)]]성분을 [[sub(a,m,n)]]이라고 하자.\n"
              "[[sub(a,m,n)]]은 [[x]]에 대한 이차함수 [[y = pow(x,2) + m x + n]]과 일차함수 [[y = 3m x - n]]이 서로 다른 두 교점을 가지면 [[sub(a,m,n) = 1]], "
              "접하는 한 교점을 가지면 [[sub(a,m,n) = 0]], 두 함수가 만나지 않으면 [[sub(a,m,n) = -1]]이라고 할 때, 행렬 [[A]]는?"),
    choices=["[[mat(2,2, -1,-1, 1,1)]]", "[[mat(2,2, -1,0, -1,1)]]", "[[mat(2,2, 0,1, -1,1)]]", "[[mat(2,2, 0,-1, 1,1)]]", "[[mat(2,2, -1,-1, 1,0)]]"],
    derived_answer="⑤", figure=None, difficulty_est=3,
    note="x²−2mx+2n=0, D/4=m²−2n: (1,1)−1,(1,2)−1,(2,1)+2→1,(2,2)0 → ⑤.")

# p68
add(id="94ec5239", qtype="short",
    question=("행렬 [[A = mat(3,3, 0,5,2, 2,0,6, 1,5,0)]]의 [[point(i, j)]] 성분 [[sub(a,i,j)]]는 세 도시 [[sub(C,1)]], [[sub(C,2)]], [[sub(C,3)]]에 대하여 "
              "도시 [[sub(C,i)]]에서 도시 [[sub(C,j)]]로 가는 비행기 직항 노선의 수를 나타낸다. 이때 도시 [[sub(C,3)]]에서 출발하여 나머지 두 도시를 경유하여 "
              "다시 도시 [[sub(C,3)]]으로 다시 돌아오는 경우의 수를 구하시오."),
    choices=None, derived_answer="50", figure=None, difficulty_est=2,
    note="C3→C1→C2→C3: 1·5·6=30, C3→C2→C1→C3: 5·2·2=20 → 50.")

# p69 (숫자판 표)
add(id="95aea22d", qtype="short",
    question=("다음 그림과 같이 1부터 100까지의 자연수가 배열되어 있는 숫자판에 4개의 수 (1, 2, 11, 12)를 포함하는 색칠된 정사각형이 놓여 있다. "
              "이 색칠된 정사각형을 오른쪽으로 [[m]]칸, 아래쪽으로 [[n]]칸 이동하였을 때, 이동된 정사각형 내부의 자연수를 그대로 괄호로 묶어서 나타내어 "
              "행렬 [[S(m, n)]]이라 하자.\n예를 들어 [[S(3, 2) = mat(2,2, 24,25, 34,35)]]이다.\n"
              "8 이하의 두 자연수 [[a]], [[b]]에 대하여 행렬 [[S(a, b)]]의 모든 성분의 합이 178일 때, [[a - b]]의 값을 구하시오."),
    choices=None, derived_answer="5",
    figure=[{"fn": "table", "args": {"rows": [[10 * r + c for c in range(1, 11)] for r in range(10)]}},
            {"fn": "unsupported", "args": {"raw": "10×10 숫자판에서 1, 2, 11, 12 칸과 24, 25, 34, 35 칸이 색칠되어 있고, 1에서 24 방향으로 이동을 나타내는 화살표"}}],
    difficulty_est=3, confidence=0.85,
    note="S(a,b) 성분 합 = 26+4a+40b = 178 → a+10b=38 → (a,b)=(8,3) → a−b=5.")

# p74 (산책로 그림 + 조각 정의)
add(id="6bbe9ed6", qtype="short",
    question=("세 공원 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]을 연결하는 산책로가 다음 그림과 같다. 행렬 [[A]]의 [[point(i, j)]] 성분 [[sub(a,i,j)]]가\n"
              "[[sub(a,i,j)]] = { (공원 [[sub(P,i)]]에서 공원 [[sub(P,j)]]로 가는 경로의 수) ([[i != j]]) ; 0 ([[i = j]]) }\n"
              "일 때, 행렬 [[A]]의 모든 성분의 합을 구하시오.\n(단, [[i]] = 1, 2, 3, [[j]] = 1, 2, 3)"),
    choices=None, derived_answer="30",
    figure=[{"fn": "unsupported", "args": {"raw": "세 공원 P₁, P₂, P₃ 삽화가 가로로 놓이고 P₁–P₂ 사이에 산책로 3개(위 곡선·가운데 직선·아래 곡선), P₂–P₃ 사이에 산책로 3개가 그려져 있음"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 산책로 연결 그림(경로 수 판독 필요) / 조각적(경우 나눔) 정의",
    note="그림 판독 P1–P2 3개, P2–P3 3개(P1–P3 직접 연결 없음)로 보면 a12=a21=a23=a32=3, a13=a31=9 → 합 30(판독에 따라 달라질 수 있음).")

# p75 (삼각형·사각형·원 교점)
add(id="1c800bda", qtype="choice",
    question=("아래 그림과 같이 삼각형 [[sub(P,1)]], 사각형 [[sub(P,2)]], 원 [[sub(P,3)]]이 있다. 삼차정사각행렬 [[A]]의 [[point(i, j)]] 성분 [[sub(a,i,j)]]가 다음을 만족시킬 때, 행렬 [[A]]는?\n"
              "(가) [[i = j]]일 때, [[sub(a,i,j) = 0]]\n"
              "(나) [[i != j]]일 때, [[sub(a,i,j)]]는 도형 [[sub(P,i)]]와 도형 [[sub(P,j)]]의 교점의 개수이다."),
    choices=["[[mat(3,3, 0,3,4, 3,0,5, 4,5,0)]]", "[[mat(3,3, 0,5,4, 5,0,3, 4,3,0)]]", "[[mat(3,3, 0,5,4, 5,0,5, 4,5,0)]]",
             "[[mat(3,3, 0,4,5, 4,0,4, 5,4,0)]]", "[[mat(3,3, 0,4,5, 4,0,5, 5,5,0)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 P₁(왼쪽 꼭짓점이 직사각형의 왼쪽 아래 꼭짓점과 일치, 위 꼭짓점은 직사각형 위, 아래 꼭짓점은 직사각형 아래), 직사각형 P₂, 원 P₃(직사각형의 윗변·오른쪽 변에 접하고 아랫변 아래로 튀어나옴, 삼각형의 왼쪽 변에 접함)"}}],
    difficulty_est=3, confidence=0.7,
    needs_review="도형 표현 불가: 삼각형·직사각형·원의 교점 그림(접점 판독 필요)",
    note="그림 판독: P1∩P2 4개(꼭짓점 공유 포함), P1∩P3 5개(왼쪽 변 접함), P2∩P3 4개(위·오른쪽 접점+아랫변 2점) → ④ (판독에 따라 달라질 수 있음).")

# p76
add(id="c3dd7fe6", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 6, a + 1, 8, 1)]], [[B = mat(2,2, 6, 4, b - 1, 1)]]에 대하여 [[A = B]]일 때, [[a b]]의 값은? (단, [[a]], [[b]]는 상수이다.)"),
    choices=N(15, 18, 21, 24, 27), derived_answer="⑤", figure=None, difficulty_est=1,
    note="출처 [2025년 9월 고1 2번/2점]. a=3, b=9 → ab=27 → ⑤.")

# p77
add(id="6677aa9b", qtype="short",
    question=("등식 [[mat(2,2, 2a - 1, 5, 2, 3b + 1) = mat(2,2, 3, c + 1, 1 - d, -8)]]을 만족시키는 실수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a + b + c + d]]의 값을 구하시오."),
    choices=None, derived_answer="2", figure=None, difficulty_est=1,
    note="a=2, b=−3, c=4, d=−1 → 2.")

# p78
add(id="424935e3", qtype="choice",
    question=("두 행렬\n[[A = mat(2,2, 1, a + 3b, c + 2d, 4)]], [[B = mat(2,2, 2c + d, -5, -7, 2a - b)]]에 대하여 [[A = B]]일 때, [[a b c d]]의 값은?\n"
              "(단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)"),
    choices=N(-30, -20, 20, 30, 40), derived_answer="④", figure=None, difficulty_est=2,
    note="c=3, d=−5, a=1, b=−2 → abcd=30 → ④.")

# p82
add(id="d2110d33", qtype="short",
    question=("등식 [[mat(2,2, pow(a,3), a b, a + b, pow(b,3)) = mat(2,2, 7 - 5 sqrt(2), k, 2, 7 + 5 sqrt(2))]]가 성립할 때, 상수 [[k]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="-1", figure=None, difficulty_est=2,
    note="a=1−√2, b=1+√2 (a+b=2) → k=ab=−1.")

# p84
add(id="a8d58314", qtype="short",
    question=("등식 [[mat(2,2, a + b, 7, y, a b) = mat(2,2, x, pow(a,3) + pow(b,3), pow(a,2) + pow(b,2), -2)]]가 성립하도록 하는 실수 [[a]], [[b]], [[x]], [[y]]에 대하여 [[x + y]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2,
    note="x³+6x=7 → x=1, y=x²−2ab=5 → 6.")

# p85
add(id="8c97a924", qtype="choice",
    question=("행렬 [[X = mat(2,2, x, y, z, w)]]에 대하여 [[prime(X) = mat(2,2, w, y, z, x)]]라 하자.\n"
              "두 행렬 [[A = mat(2,2, 4, 3, 2x y + 1, 3x + 4y)]],\n[[B = mat(2,2, 2x + 3y + 4, 3, x y + 4, 4)]]에 대하여 [[prime(A) = B]]가 성립할 때,\n"
              "[[pow(x,3) + pow(y,3)]]의 값은? (단, [[x]], [[y]]는 실수이다.)"),
    choices=N(24, 28, 32, 36, 40), derived_answer="②", figure=None, difficulty_est=2,
    note="x+y=4, xy=3 → x³+y³=64−36=28 → ②.")

# p86
add(id="f9cdb36d", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 7, x, x y, y)]], [[B = mat(2,2, 7, 6 - y, x y, frac(6, x))]]에 대하여\n"
              "[[A = B]]가 성립할 때, [[frac(pow(y,2), x) + frac(pow(x,2), y)]]의 값은?\n(단, [[x]], [[y]]는 실수이다.)"),
    choices=N(16, 17, 18, 19, 20), derived_answer="③", figure=None, difficulty_est=2,
    note="x+y=6, xy=6 → (x³+y³)/xy=(216−108)/6=18 → ③.")

# p87
add(id="bdc54bae", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 18, 2a + 3b, c, -3a + b)]], [[B = mat(2,2, 2a d - 2b, 15, 2a d - b, -6)]]에 대하여 [[A = B]]일 때,\n"
              "실수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a b + c d]]의 값은?"),
    choices=N(91, 93, 95, 97, 99), derived_answer="②", figure=None, difficulty_est=2,
    note="a=3, b=3, d=4, c=21 → 9+84=93 → ②.")

# p88
add(id="68aba53d", qtype="short",
    question=("두 행렬 [[mat(2,2, pow(x,2), x y, 9, 2y + 3)]], [[mat(2,2, x + 6, 9, x y, pow(y,2))]]이 서로 같을 때, 실수 [[x]], [[y]]에 대하여 [[x + y]]의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=2,
    note="x∈{3,−2}, y∈{3,−1}, xy=9 → x=y=3 → 6.")

# p91
add(id="2713c90e", qtype="short",
    question=("등식 [[mat(2,2, pow(a,3) - pow(b,3), a b, a - b, 0) = mat(2,2, 45, k, 3, 0)]]이 성립할 때, 상수 [[k]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="2", figure=None, difficulty_est=2,
    note="a−b=3, 27+9ab=45 → ab=2 → k=2.")

# p92 (조각 정의)
add(id="5bb4250a", qtype="short",
    question=("두 이차정사각행렬 [[A]], [[B]]의 [[point(i, j)]] 성분 [[sub(a,i,j)]], [[sub(b,i,j)]]가\n"
              "[[sub(a,i,j) = 2p i - q j]], [[sub(b,i,j)]] = { [[frac(1,3) i - frac(1,6) j + 2]] ([[i != j]]) ; [[frac(1,2)(2i + j)]] ([[i = j]]) }이고\n"
              "[[A = B]]일 때, 상수 [[p]], [[q]]에 대하여 [[8p q]]의 값을 구하시오."),
    choices=None, derived_answer="-2", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 한계: 성분 b_ij의 조각적(경우 나눔) 정의",
    note="b11=3/2, b12=2 → 2p−q=3/2, p−q=1 → p=1/2, q=−1/2 → 8pq=−2.")

# p93
add(id="c67d90fc", qtype="short",
    question=("두 행렬 [[A = mat(2,2, pow(x,3), 4, 2, pow(y,3))]], [[B = mat(2,2, a, x + y, x y, b)]]에 대하여\n[[A = B]]일 때, [[a + b]]의 값을 구하시오.\n"
              "(단, [[a]], [[b]], [[x]], [[y]]는 상수이다.)"),
    choices=None, derived_answer="40", figure=None, difficulty_est=2,
    note="x+y=4, xy=2 → a+b=x³+y³=64−24=40.")

# p95
add(id="da787968", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, a, 3, 1, -1)]], [[B = mat(2,2, 1, 3, b - 5, -1)]]에 대하여\n[[A = B]]일 때, [[a + b]]의 값은?"),
    choices=N(1, 5, 6, 7, 9), derived_answer="④", figure=None, difficulty_est=1,
    note="a=1, b=6 → 7 → ④.")

# p97
add(id="22cb0890", qtype="short",
    question=("두 행렬 [[A = mat(2,2, pow(x,2), 6, 3, pow(y,2))]], [[B = mat(2,2, a, x - y, x y, b)]]에 대하여\n[[A = B]]일 때, [[a + b]]의 값을 구하시오.\n"
              "(단, [[a]], [[b]], [[x]], [[y]]는 상수이다.)"),
    choices=None, derived_answer="42", figure=None, difficulty_est=2,
    note="x−y=6, xy=3 → x²+y²=36+6=42.")

# p99 (대응 그림)
add(id="843dce17", qtype="choice",
    question=("백의 자리의 수, 십의 자리의 수, 일의 자리의 수가 각각 [[a]], [[b]], [[c]]인 세 자리 자연수 [[n]]에 행렬 [[A = mat(2,2, a, b, c, b + c)]]를 대응시키는 것을 [그림 1]과 같이 나타내자.\n"
              "그리고 행렬 [[B = mat(2,2, p, q, r, s)]]에 대하여 행렬 [[pow(B, t)]]를\n[[pow(B, t) = mat(2,2, p, r, q, s)]]라 할 때 행렬 [[B]]에 행렬 [[pow(B, t)]]를 대응시키는 것을 [그림 2]와 같이 나타내자.\n"
              "아래 그림에서 행렬 [[X = mat(2,2, 7, 1, 9, 10)]]일 때\n자연수 [[n]]의 값은?"),
    choices=N(179, 197, 719, 791, 971), derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "[그림 1] 원 n — 회색 마름모 — 사각형 A (세로 연결). [그림 2] 사각형 B — 회색 육각형 — 사각형 Bᵗ (가로 연결). 아래 그림: 원 n — 마름모 — 빈 사각형 — 육각형 — 빈 사각형 — 육각형 — 사각형 X"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 대응 관계 흐름도 3개 / 전치행렬 Bᵗ 표기를 pow(B, t)로 우회",
    note="출처 [2006년 9월 고2 이과 13번]. 전치 두 번 → A=X → a=7, b=1, c=9(b+c=10 ✓) → n=719 → ③.")

# ───────────────────────── 합의 법칙과 곱의 법칙 ─────────────────────────
# p14
add(id="297e660d", qtype="short",
    question=("서로 다른 세 개의 주사위를 동시에 던져서 나오는 눈의 수를 각각 [[a]], [[b]], [[c]]라 할 때, [[x]]에 대한 "
              "이차방정식 [[a pow(x,2) - b x + c = 0]]이 중근을 갖도록 하는 순서쌍 ([[a]], [[b]], [[c]])의 개수를 구하시오."),
    choices=None, derived_answer="5", figure=None, difficulty_est=2,
    note="b²=4ac: b=2→(1,1), b=4→(1,4),(2,2),(4,1), b=6→(3,3) → 5.")

# p16
add(id="80036720", qtype="choice",
    question="[[4x + 2y + z = 15]]를 만족시키는 자연수 [[x]], [[y]], [[z]]의 순서쌍 ([[x]], [[y]], [[z]])의 개수는?",
    choices=N(10, 9, 8, 7, 6), derived_answer="②", figure=None, difficulty_est=2,
    note="x=1: 5개, x=2: 3개, x=3: 1개 → 9 → ②.")

# p33 (액정 계산기)
_SEG33 = {"fn": "table", "args": {"head": ["수", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
          "rows": [["정상 액정", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                   ["표시된 액정", "세로선 위·아래", "세로선 위·아래", "세로선 위만", "세로선 위·아래", "세로선 위·아래", "세로선 아래만", "세로선 아래만", "세로선 위·아래", "세로선 위·아래", "세로선 위·아래"]]}}
add(id="1c9d7b94", qtype="choice",
    question=("다음과 같이 액정의 고장으로 오른쪽 세로선만 표시되는 전자계산기가 있다.\n"
              "[그림 1]과 같이 액정에 표시된 두 자리의 자연수 [[A]]에 대하여 [×], [5], [=]의 버튼을 순서대로 눌렀더니 [그림 2]와 같은 세 자리의 수가 액정에 표시되었다.\n"
              "이때 [[A]]가 될 수 있는 모든 수의 합은?"),
    choices=N(566, 572, 578, 584, 590), derived_answer="④",
    figure=[_SEG33, {"fn": "unsupported", "args": {"raw": "[그림 1] 계산기 액정에 두 자리 모두 오른쪽 세로선 위·아래가 표시됨(| |), [그림 2] 세 자리 모두 오른쪽 세로선 위·아래가 표시됨(| | |); 계산기 자판 삽화"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 7세그먼트 액정 표시 그림(표시 모양이 정보)",
    note="자릿수 ∈{0,1,3,4,7,8,9}, A×5 세 자리 모두 같은 집합 → A∈{34,38,74,78,80,88,94,98} 합 584 → ④.")

# p34 (액정 계산기 2)
_SEG34 = {"fn": "table", "args": {"head": ["수", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
          "rows": [["정상 액정", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                   ["표시된 액정", "아래 세로선", "아래 세로선", "가운데 가로선", "가로선+아래 세로선", "가로선+아래 세로선", "가로선+아래 세로선", "가로선+아래 세로선", "아래 세로선", "가로선+아래 세로선", "가로선+아래 세로선"]]}}
add(id="e3b5aa5d", qtype="choice",
    question=("다음과 같이 액정의 고장으로 숫자의 일부분만 표시되는 전자계산기가 있다.\n"
              "[그림 1]과 같이 액정에 표시된 두 자리의 자연수 [[A]]에 대하여 [×], [5], [=]의 버튼을 순서대로 눌렀더니 [그림 2]와 같은 세 자리의 수가 액정에 표시되었다.\n"
              "이때 [[A]]가 될 수 있는 모든 수들의 합은?"),
    choices=N(346, 350, 354, 358, 362), derived_answer="②",
    figure=[_SEG34, {"fn": "unsupported", "args": {"raw": "[그림 1] 계산기 액정에 두 자리 모두 'ㄱ' 모양(가운데 가로선+오른쪽 아래 세로선)이 표시됨, [그림 2] 세 자리 모두 'ㄱ' 모양이 표시됨; 계산기 자판 삽화"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 7세그먼트 액정 표시 그림(표시 모양이 정보)",
    note="'ㄱ' 모양 자릿수 ∈{3,4,5,6,8,9}, A×5 세 자리 모두 같은 집합 → A∈{69,89,93,99} 합 350 → ②.")

# p80
add(id="7a904f7b", qtype="choice",
    question=("서로 다른 5개의 자물쇠 A, B, C, D, E에 맞는 열쇠를 차례대로 [[a]], [[b]], [[c]], [[d]], [[e]]라 하자. 4개의 열쇠 [[a]], [[b]], [[c]], [[d]]를 "
              "임의로 3개의 자물쇠 C, D, E에 각각 하나씩 꽂아 돌렸을 때, 모든 자물쇠가 열리지 않는 경우의 수는?"),
    choices=N(8, 10, 12, 14, 16), derived_answer="④", figure=None, difficulty_est=3,
    note="4·3·2=24 − (C=c 6 + D=d 6 − 둘 다 2) = 14 → ④.")

# p81
add(id="0cbc94eb", qtype="choice",
    question=("1, 2, 3, 4, 5가 각각 적힌 공을 [[sub(A,1)]], [[sub(A,2)]], [[sub(A,3)]], [[sub(A,4)]], [[sub(A,5)]]라 쓰여진 상자에 각각 1개씩 넣을 때, "
              "5가 적힌 공은 [[sub(A,1)]]에 넣고, 4가 적힌 공은 [[sub(A,3)]]에 넣고, 2가 적힌 공은 [[sub(A,2)]]에 넣지 않는 방법의 수는?"),
    choices=N(2, 3, 4, 5, 6), derived_answer="③", figure=None, difficulty_est=2,
    note="공 1,2,3을 A2,A4,A5에, 2는 A2 제외: 3!−2!=4 → ③.")

# ───────────────────────── 이차함수의 최대·최소 ─────────────────────────
# p46 (조각 정의)
add(id="758f0c98", qtype="short",
    question=("함수 [[f(x)]] = { [[x + 10]] ([[x < 0]]) ; [[pow(x,2) - 8x + 10]] ([[x >= 0]]) }에 대하여\n"
              "[[h(x) = pow(f(x), 2) - 2f(x) + 3]] ([[-5 <= x <= 3]])이라 하자. 함수 [[h(x)]]가 [[x = k]]에서 최댓값 [[M]]을 가질 때, [[M - k]]의 값을 구하시오."),
    choices=None, derived_answer="83", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: f(x)의 조각적(경우 나눔) 정의",
    note="f의 치역 [−5,10], h=(f−1)²+2 최대 83 (f=10, x=0) → M−k=83.")

# p67
add(id="6eb5365e", qtype="short",
    question=("실수 [[x]], [[y]]에 대하여 [[-pow(x,2) - pow(y,2) + 10x - 10]]이 [[x = alpha]], [[y = beta]]에서 최댓값 [[gamma]]를 갖는다. "
              "상수 [[alpha]], [[beta]], [[gamma]]에 대하여 [[alpha + beta + gamma]]의 값을 구하시오."),
    choices=None, derived_answer="20", figure=None, difficulty_est=2,
    note="−(x−5)²−y²+15 → α=5, β=0, γ=15 → 20.")

# p78 (포물선 그래프)
add(id="e6fce8bc", qtype="choice",
    question=("이차함수 [[f(x) = pow(x,2) - 2a x + 5a]]의 그래프의 꼭짓점을 A라 하고, 점 A에서 [[x]]축에 내린 수선의 발을 B라 하자. "
              "[[0 < a < 5]]일 때, [[seg(OB) + seg(AB)]]의 최댓값은?\n(단, O는 원점이고, [[a]]는 [[a != 0]], [[a != 5]]인 실수이다.)"),
    choices=N(5, 6, 7, 8, 9), derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면에 아래로 볼록한 포물선 y=f(x)(y축과 양의 y절편에서 만남), 제1사분면의 꼭짓점 A, A에서 x축에 내린 수선의 발 B(직각 표시, 점선), 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 이차함수 그래프 좌표평면 도형",
    note="출처 [2016년 6월 고1 14번/4점]. A(a, 5a−a²), OB+AB=6a−a² 최대 9 (a=3) → ⑤.")

# ───────────────────────── 이차방정식의 근과 계수와의 관계 ─────────────────────────
# p76
add(id="c1229d1f", qtype="short",
    question=("승빈이와 유빈이가 이차방정식 [[pow(x,2) - a x + b = 0]]을 푸는데, 승빈이는 [[a]]를 잘못 보고 풀어 두 근 [[-1]], [[2]]를 얻었고, "
              "유빈이는 [[b]]를 잘못 보고 풀어 두 근 [[pm(1, sqrt(5) i)]]를 얻었다. 이때 실수 [[a]], [[b]]에 대하여 [[a b]]의 값을 구하시오."),
    choices=None, derived_answer="-4", figure=None, difficulty_est=2,
    note="b=(−1)·2=−2, a=(1+√5i)+(1−√5i)=2 → ab=−4.")

# p79
add(id="b3b64dc2", qtype="short",
    question=("민정이는 계수가 실수인 이차방정식 [[a pow(x,2) + b x + c = 0]]의 근의 공식을 [[x = frac(pm(a, sqrt(pow(a,2) - 4b c)), 2b)]] ⋯ (*)로 잘못 적용하여 "
              "이차방정식 [[k pow(x + 6, 2) + (x + 6) - 12 = 0]]의 두 근 [[alpha]], [[beta]]를 다음과 같은 단계로 구하였다.\n"
              "[1단계] 이차방정식 [[k pow(X,2) + X - 12 = 0]]의 두 근 [[p]], [[q]]를 공식 (*)를 이용하여 구한다.\n"
              "[2단계] [[alpha + 6 = p]], [[beta + 6 = q]]에서 [[alpha]], [[beta]]를 구한다.\n"
              "이와 같이 구한 두 근 [[alpha]], [[beta]]가 [[(alpha + 9)(beta + 9) = 3]]을 만족할 때, 이차방정식 [[k pow(x + 6, 2) + (x + 6) - 12 = 0]]의 올바른 두 근의 곱을 구하시오. (단, [[k]]는 실수이다.)"),
    choices=None, derived_answer="33", figure=None, difficulty_est=4,
    note="(*)로 p+q=k, pq=−12 → (p+3)(q+3)=3k−3=3 → k=2; 2X²+X−12=0의 X근 합 −1/2·곱 −6 → (X₁−6)(X₂−6)=−6+3+36=33.")

# p80
add(id="27ac15e2", qtype="short",
    question=("이차방정식 [[a pow(x,2) + b x + c = 0]] ([[a != 0]])의 근을 구하는데,\n근의 공식을 [[x = frac(pm(b, sqrt(pow(b,2) - a c)), 2a)]]로 잘못 적용하여\n"
              "풀었더니 두 근이 [[-1]], [[3]]이었다. 이 이차방정식의 원래의\n두 근을 [[alpha]], [[beta]]라 할 때, [[pow(alpha,2) + pow(beta,2)]]의 값을 구하시오.\n"
              "(단, [[a]], [[b]], [[c]]는 실수이다.)"),
    choices=None, derived_answer="28", figure=None, difficulty_est=3,
    note="잘못된 근: 합 b/a=2, 곱 c/(4a)=−3 → c/a=−12; 원래 α+β=−2, αβ=−12 → α²+β²=4+24=28.")

# p82
add(id="6791d73f", qtype="short",
    question=("희욱이는 계수가 실수인 이차방정식 [[a pow(x,2) + b x + c = 0]]\n의 근의 공식을\n[[x = frac(pm(-b, sqrt(pow(b,2) - 4a c)), 2c)]]\n"
              "로 잘못 적용하여 이차방정식 [[k pow(x,2) + 9x - 9 = 0]]의\n두 근 [[alpha]], [[beta]]를 구하고, 이를 통해 두 근이\n[[4(alpha + beta) + 9 alpha beta = 0]]을 만족시킴을 확인했다.\n"
              "이차방정식 [[k pow(x,2) + 9x - 9 = 0]]의 올바른 두 근을 통해\n[[4(alpha + beta) + 9 alpha beta]]의 값을 구하시오. (단, [[k]]는 실수이다.)"),
    choices=None, derived_answer="-frac(117,4)", figure=None, difficulty_est=3,
    note="잘못된 근: 합 1, 곱 −k/9 → 4−k=0 → k=4; 4x²+9x−9=0의 올바른 합 −9/4, 곱 −9/4 → −9−81/4=−117/4.")

# p83
add(id="004437a9", qtype="choice",
    question=("[[x]]에 대한 실수 계수의 이차방정식 [[a pow(x,2) + b x + c = 0]]에서\n근의 공식을 [[frac(pm(-b, sqrt(pow(b,2) - a c)), a)]]로 잘못 기억하고 풀어\n"
              "두 근이 [[-1]], [[2]]를 얻었다. 이 방정식을 바르게 풀 때,\n두 근의 합은?"),
    choices=["[[0]]", "[[frac(1,2)]]", "[[frac(2,3)]]", "[[2]]", "[[3]]"], derived_answer="②", figure=None, difficulty_est=2,
    note="잘못된 근의 합 −2b/a=1 → 올바른 합 −b/a=1/2 → ②.")

# ───────────────────────── 복소수의 뜻과 성질 ─────────────────────────
# p9
add(id="e79fc950", qtype="choice",
    question=("[[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,30)]]은 각각 [[-1]], [[i]], [[1 + i]] 중 하나의 값을 갖는다. "
              "[[pow(sub(a,1), 2) + pow(sub(a,2), 2) + pow(sub(a,3), 2)]] + ⋯ + [[pow(sub(a,30), 2) = 10 + 16i]]일 때,\n"
              "[[sub(a,1) + sub(a,2) + sub(a,3)]] + ⋯ + [[sub(a,30)]]의 실수부분과 허수부분의 합은?"),
    choices=N(4, 6, 8, 10, 12), derived_answer="②", figure=None, difficulty_est=3,
    note="−1이 x개, i가 y개, 1+i가 z개: z=8, x−y=10, x+y=22 → x=16, y=6 → 합 −8+14i → 6 → ②.")

# p13
add(id="84f10706", qtype="choice",
    question="두 복소수 [[sub(z,1) = 1 - 2i]], [[sub(z,2) = 1 + 2i]]에 대하여 [[sub(z,1) sub(z,2)]]의\n값은?",
    choices=N(1, 2, 3, 4, 5), derived_answer="⑤", figure=None, difficulty_est=1,
    note="1+4=5 → ⑤.")

# p20
add(id="fcab6d02", qtype="choice",
    question=("[[omega]]는 방정식 [[pow(x,2) - x + 1 = 0]]의 한 허근이고,\n[[f(x) = x + frac(1, x)]]이라 할 때,\n"
              "[[f(omega) × f(pow(omega, 6)) × f(pow(omega, pow(6, 2))) × f(pow(omega, pow(6, 3)))]] × ⋯ × [[f(pow(omega, pow(6, 2021)))]]의 값은?"),
    choices=["[[-1]]", "[[-pow(2, 2021)]]", "[[omega]]", "[[pow(2, 2021)]]", "[[1]]"], derived_answer="④", figure=None, difficulty_est=3,
    note="ω+1/ω=1, ω⁶=1 → f(ω)=1, 나머지 2021개 항은 f(1)=2 → 2²⁰²¹ → ④.")

# p42
add(id="6f64bcaa", qtype="short",
    question=("두 함수\n[[f(x) = a pow(x,2) + 3a pow(x,4) + 5a pow(x,6)]] + ⋯ + [[97a pow(x,98) + 99a pow(x,100)]],\n"
              "[[g(x) = 2b x + 4b pow(x,3) + 6b pow(x,5)]] + ⋯ + [[98b pow(x,97) + 100b pow(x,99)]]에\n"
              "대하여 [[z = frac(f(i) - g(i), 100i)]]라 할 때,\n[[z conj(z) = 9]]를 만족시키는 두 정수 [[a]], [[b]]의 순서쌍 [[point(a, b)]]의\n개수를 구하시오.\n"
              "(단, [[i = sqrt(-1)]]이고, [[conj(z)]]는 [[z]]의 켤레복소수이다.)"),
    choices=None, derived_answer="4", figure=None, difficulty_est=4,
    note="f(i)=50a, g(i)=−50bi → z=(b−ai)/2, |z|²=(a²+b²)/4=9 → a²+b²=36 → (±6,0),(0,±6) → 4.")

# p48
add(id="bd90c2c4", qtype="choice",
    question=("복소수 [[z = a + b i]] ([[a]], [[b]]는 0이 아닌 실수)에 대하여 [[pow(z,2) - 2z]]가 실수일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n"
              "(단, [[i = sqrt(-1)]]이고, [[conj(z)]]는 [[z]]의 켤레복소수이다.)\n<보기>\n"
              "ㄱ. [[conj(pow(z,2)) - 2 conj(z)]]는 실수이다.\nㄴ. [[z + conj(z) = 1]]\nㄷ. [[z conj(z) <= 1]]"),
    choices=CH_G3, derived_answer="①", figure=None, difficulty_est=3,
    note="허수부 2b(a−1)=0 → a=1: ㄱ✓(실수의 켤레), ㄴ z+z̄=2 ✗, ㄷ zz̄=1+b²>1 ✗ → ①.")

# p49
add(id="46d84247", qtype="choice",
    question=("[[alpha]], [[beta]]가 복소수일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n(단, [[conj(beta)]]는 [[beta]]의 켤레복소수이고, [[i = sqrt(-1)]]이다.)\n<보기>\n"
              "ㄱ. [[alpha = conj(beta)]]이면 [[alpha + beta]], [[alpha beta]]는 모두 실수이다.\n"
              "ㄴ. [[alpha = conj(beta)]]일 때, [[alpha beta = 0]]이면 [[alpha = 0]]이다.\n"
              "ㄷ. [[pow(alpha,2) + pow(beta,2) = 0]]이면 [[alpha = 0]], [[beta = 0]]이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="②", figure=None, difficulty_est=3,
    note="ㄱ✓, ㄴ✓(|β|²=0), ㄷ✗(α=1, β=i) → ②.")

# p68
add(id="615b160e", qtype="short",
    question=("20 이하의 두 자연수 [[m]], [[n]]에 대하여\n[[pow(pow(i + 1, 2n) + pow(frac(sqrt(2), i + 1), 2n), m)]]의 값이 음의 실수가 되도록\n"
              "하는 순서쌍 [[point(m, n)]]의 개수를 구하시오.\n(단, [[i = sqrt(-1)]]이다.)"),
    choices=None, derived_answer="100", figure=None, difficulty_est=4,
    note="출처 [2020년 6월 고1 30번 변형]. 밑 = iⁿ(2ⁿ+(−1)ⁿ): n≡2(mod 4)·m 홀수 50개, n≡1,3(mod 4)·m≡2(mod 4) 25+25개 → 100.")

# p76
add(id="b0e808bb", qtype="choice",
    question=("복소수 [[z = a + b i]] ([[a]], [[b]]는 실수)에 대하여 [[x]], [[y]]에 대한 일차식 [[sub(P, z) = a x + b y]]라 하자. 자연수 [[n]]에 대하여 복소수 "
              "[[sub(z,n) = pow(1 - i, n) pow(1 + i, n + 1)]]일 때,\n"
              "[[sub(P, w) = (sub(P, sub(z,1)) + sub(P, sub(z,4))) - (sub(P, sub(z,2)) + sub(P, sub(z,3)))]]를 만족시키는 복소수 [[w]]는?"),
    choices=["[[2 + 2i]]", "[[4 + 4i]]", "[[6 + 6i]]", "[[8 + 8i]]", "[[10 + 10i]]"], derived_answer="③", figure=None, difficulty_est=3,
    note="zₙ=2ⁿ(1+i), P는 선형 → w=z₁+z₄−z₂−z₃=(2+16−4−8)(1+i)=6+6i → ③.")

# p77
add(id="e22e30ab", qtype="choice",
    question=("복소수 [[z = a + b i]] ([[a]], [[b]]는 실수)에 대하여 [[x]], [[y]]에 대한 일차식 [[sub(P, z) = a x + b y]]라 하자. 자연수 [[n]]에 대하여 "
              "복소수 [[sub(z,n) = pow(2 - i, n) pow(1 + i, n + 1)]]일 때,\n"
              "[[sub(P, w) = (sub(P, sub(z,1)) - sub(P, sub(z,2))) + (sub(P, sub(z,3)) - sub(P, sub(z,4)))]]를 만족시키는\n복소수 [[w]]는?"),
    choices=["[[2 - i]]", "[[2 + 14i]]", "[[-8 + 44i]]", "[[-68 + 124i]]", "[[60 - 90i]]"], derived_answer="⑤", figure=None, difficulty_est=3,
    note="z₁=2+4i, z₂=2+14i, z₃=−8+44i, z₄=−68+124i → w=z₁−z₂+z₃−z₄=60−90i → ⑤.")

# p97
add(id="2a2f9297", qtype="choice",
    question=("세 양의 실수 [[a]], [[b]], [[c]]가 [[frac(2, a + 2b) < frac(1, b + c)]], [[frac(2, a) > frac(1, b)]]을\n만족할 때 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[frac(sqrt(2b - a), sqrt(c - b)) = -sqrt(frac(2b - a, c - b))]]\n"
              "ㄴ. [[sqrt(2b - a) sqrt(a - 2c) = -sqrt((2b - a)(a - 2c))]]\n"
              "ㄷ. [[sqrt(c - b) sqrt(a - 2c) = i sqrt((b - c)(a - 2c))]]"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="③", figure=None, difficulty_est=3,
    note="2c<a<2b → 2b−a>0, a−2c>0, c−b<0: ㄱ✓, ㄴ✗(둘 다 양수), ㄷ✓ → ③.")

# ───────────────────────── 항등식과 나머지 정리 ─────────────────────────
# p11 (P_n(x) 표기)
add(id="b6b4e691", qtype="short",
    question=("자연수 [[n]]에 대하여 [[n]]차 다항식\n[[sub(P,n)]]([[x]]) = [[(x - 1)(x - 2)(x - 3)]] ⋯ [[(x - n)]]이라 할 때,\n"
              "[[3 pow(x,3) + 2 pow(x,2) - 5x + 2]]\n= [[a]] + [[b]][[sub(P,1)]]([[x]]) + [[c]][[sub(P,2)]]([[x]]) + [[d]][[sub(P,3)]]([[x]])는 [[x]]에 대한\n"
              "항등식이다. 상수 [[a]], [[b]], [[c]], [[d]]에 대하여 [[a + b + c + d]]의\n값을 구하시오."),
    choices=None, derived_answer="47", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: 첨자 붙은 함수 적용 표기 Pₙ(x)를 텍스트 혼합으로 우회",
    note="d=3, c=20, b=22, a=2 → 47.")

# p22
add(id="f21e675f", qtype="choice",
    question=("모든 실수 [[x]]에 대하여 등식\n[[pow(x,10) = sub(a,0) + sub(a,1)(x - 1)]] + ⋯ + [[sub(a,10) pow(x - 1, 10)]]이 성립할\n"
              "때, [[sub(a,0) + sub(a,2) + sub(a,4)]] + ⋯ + [[sub(a,10)]]의 값은?"),
    choices=N(512, 513, 1023, 1024, 1025), derived_answer="①", figure=None, difficulty_est=2,
    note="x=2: 1024, x=0: 0 → 짝수항 합 512 → ①.")

# p24
add(id="19954510", qtype="choice",
    question=("등식 [[pow(1 + x + pow(x,2), 4) = sub(a,0) + sub(a,1) x + sub(a,2) pow(x,2)]] + ⋯ + [[sub(a,8) pow(x,8)]]이\n"
              "[[x]]에 대한 항등식일 때, [[sub(a,1) + sub(a,3) + sub(a,5) + sub(a,7)]]의 값은?"),
    choices=N(40, 36, 32, 28, 24), derived_answer="①", figure=None, difficulty_est=2,
    note="x=1: 81, x=−1: 1 → 홀수항 합 40 → ①.")

# p25
add(id="05444e27", qtype="short",
    question=("상수 [[sub(a,0)]], [[sub(a,1)]], [[sub(a,2)]], [[sub(a,3)]], ⋯, [[sub(a,12)]]에 대하여 모든 실수 [[x]]에\n대하여 등식\n"
              "[[pow(pow(x,3) - 3x - 3, 4) = sub(a,0) + sub(a,1) x + sub(a,2) pow(x,2)]] + ⋯ + [[sub(a,12) pow(x,12)]]이\n"
              "성립할 때, [[sub(a,1) + sub(a,3) + sub(a,5) + sub(a,7) + sub(a,9) + sub(a,11)]]의 값을\n"
              "구하시오. (단, [[sub(a,0)]], [[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,12)]]는 상수이다.)"),
    choices=None, derived_answer="312", figure=None, difficulty_est=2,
    note="x=1: 625, x=−1: 1 → 홀수항 합 312.")

# ───────────────────────── 이차함수의 그래프와 직선의 위치 관계 ─────────────────────────
# p19
add(id="31e5d49e", qtype="short",
    question=("이차함수 [[f(x) = pow(x,2) + 2x - 6]]의 그래프가\n직선 [[y = a x - 1]]과 서로 다른 두 점\n"
              "[[point(sub(x,1), f(sub(x,1)))]], [[point(sub(x,2), f(sub(x,2)))]]에서 만난다.\n[[sub(x,1) + sub(x,2) = -1]]일 때, 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=2,
    note="x²+(2−a)x−5=0, 근의 합 a−2=−1 → a=1.")

# p51 (조각 정의)
add(id="f412f176", qtype="choice",
    question=("최고차항의 계수가 [[a]] ([[a < 0]])인\n두 이차함수 [[f(x)]], [[g(x)]]에 대하여 [[f(3) = g(3)]]이다.\n"
              "함수 [[h(x)]]를 [[h(x)]] = { [[f(x)]] ([[x <= 3]]) ; [[g(x)]] ([[x > 3]]) }이라 할 때,\n함수 [[h(x)]]가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[y = h(x)]]의 그래프와 직선 [[y = f(0)]]이 만나는 점의 [[x]]좌표는 0, 4, 12뿐이다.\n"
              "(나) 두 실수 [[alpha]], [[beta]] ([[alpha < 3 < beta]])에 대하여 함수 [[y = h(x)]]의 그래프와 직선 [[y = 2x - 8]]이 만나는 점의 [[x]]좌표는 [[alpha]], 3, [[beta]]이다.\n"
              "[[alpha + beta = 6]]일 때, [[h(-2) + h(5)]]의 값은?"),
    choices=N(15, 16, 17, 18, 19), derived_answer="③", figure=None, difficulty_est=4, confidence=0.8,
    needs_review="문법 한계: h(x)의 조각적(경우 나눔) 정의",
    note="출처 [2025년 9월 고1 20번/4점]. f(x)−f(0)=ax², g(x)−f(0)=a(x−4)(x−12), α=2/a−3, β=13+2/a, α+β=6 → a=−1, f(0)=7 → h(−2)+h(5)=3+14=17 → ③.")

# p58 (그래프 + 빈칸 과정)
add(id="e2948df6", qtype="choice",
    question=("두 실수 [[a]] ([[a > 2]]), [[b]]에 대하여\n이차함수 [[y = pow(x,2) - (a + 2) x + 2a]]의 그래프와\n직선 [[y = b x - 2b]]가 한 점 [[A(2, 0)]]에서만 만난다.\n"
              "함수 [[y = pow(x,2) - (a + 2) x + 2a]]의 그래프가 [[x]]축과 만나는 점 중 A가 아닌 점을 B, 함수 [[y = pow(x,2) - (a + 2) x + 2a]]의 그래프가 [[y]]축과 만나는 점을 C, "
              "직선 [[y = b x - 2b]]가 [[y]]축과 만나는 점을 D라 하자. 다음은 삼각형 OAD의 넓이를 [[sub(S,1)]], 사각형 ABCD의 넓이를 [[sub(S,2)]]라 할 때, "
              "[[ratio(sub(S,1), sub(S,2)) = ratio(1, 3)]]이 되도록 하는 [[a]]의 값을 구하는 과정이다.\n(단, O는 원점이다.)\n"
              "이차함수 [[y = pow(x,2) - (a + 2) x + 2a]]의 그래프가 직선 [[y = b x - 2b]]와 한 점 A에서만 만나므로 "
              "이차방정식 [[pow(x,2) - (a + b + 2) x + 2(a + b) = 0]]의 판별식 [[D = 0]]이다.\n"
              "삼각형 OAD의 넓이 [[sub(S,1)]]과 사각형 ABCD의 넓이 [[sub(S,2)]]를 [[a]]에 대한 식으로 나타내면\n"
              "[[sub(S,1)]] = (가), [[sub(S,2)]] = (나)이다.\n"
              "따라서 [[ratio(sub(S,1), sub(S,2)) = ratio(1, 3)]]이 되도록 하는 [[a]]의 값은\n[[a]] = (다)이다.\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(a)]], [[g(a)]]라 하고,\n(다)에 알맞은 수를 [[p]]라 할 때, [[f(6) + g(6) + p]]의 값은?"),
    choices=N(32, 34, 36, 38, 40), derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y=x²−(a+2)x+2a(x축과 A, B에서 만남, y축과 C에서 만남), 직선 y=bx−2b(A에서 접함, y축과 D에서 만남), 선분 CB, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 이차함수 그래프·직선 좌표평면 도형",
    note="출처 [2025년 6월 고1 16번 변형]. a+b=2, D(0,2a−4), C(0,2a), B(a,0): S₁=2a−4, S₂=a²−2a+4, 1:3 → a=4 → f(6)+g(6)+p=8+28+4=40 → ⑤.")

# p75 (그래프 + 빈칸 과정)
add(id="d82c89fc", qtype="choice",
    question=("두 실수 [[a]] ([[a > 2]]), [[b]]에 대하여\n이차함수 [[y = pow(x,2) - (a + 1) x + a]]의 그래프와\n직선 [[y = b x - b]]가 한 점 [[A(1, 0)]]에서만 만난다.\n"
              "함수 [[y = pow(x,2) - (a + 1) x + a]]의 그래프가 [[x]]축과 만나는 점 중 A가 아닌 점을 B, 함수 [[y = pow(x,2) - (a + 1) x + a]]의 그래프가 [[y]]축과 만나는 점을 C, "
              "직선 [[y = b x - b]]가 [[y]]축과 만나는 점을 D라 하자. 다음은 삼각형 OAD의 넓이를 [[sub(S,1)]], 사각형 ABCD의 넓이를 [[sub(S,2)]]라 할 때, "
              "[[ratio(sub(S,1), sub(S,2)) = ratio(2, 7)]]이 되도록 하는 [[a]]의 값을 구하는 과정이다.\n(단, O는 원점이다.)\n"
              "이차함수 [[y = pow(x,2) - (a + 1) x + a]]의 그래프가 직선 [[y = b x - b]]와 한 점 A에서만 만나므로 "
              "이차방정식 [[pow(x,2) - (a + b + 1) x + a + b = 0]]의 판별식 [[D = 0]]이다.\n"
              "삼각형 OAD의 넓이 [[sub(S,1)]]과 사각형 ABCD의 넓이 [[sub(S,2)]]를 [[a]]에 대한 식으로 나타내면\n"
              "[[sub(S,1)]] = (가), [[sub(S,2)]] = (나)이다.\n"
              "따라서 [[ratio(sub(S,1), sub(S,2)) = ratio(2, 7)]]이 되도록 하는 [[a]]의 값은\n[[a]] = (다)이다.\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(a)]], [[g(a)]]라 하고,\n(다)에 알맞은 수를 [[p]]라 할 때, [[f(5) + g(5) + p]]의 값은?"),
    choices=["[[frac(27,2)]]", "[[frac(29,2)]]", "[[frac(31,2)]]", "[[frac(33,2)]]", "[[frac(35,2)]]"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y=x²−(a+1)x+a(x축과 A, B에서 만남, y축과 C에서 만남), 직선 y=bx−b(A에서 접함, y축과 D에서 만남), 선분 CB, 원점 O"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 이차함수 그래프·직선 좌표평면 도형",
    note="출처 [2025년 6월 고1 16번/4점]. a+b=1, D(0,a−1), C(0,a), B(a,0): S₁=(a−1)/2, S₂=(a²−a+1)/2, 2:7 → a=3 → 2+21/2+3=31/2 → ③.")

# p82
add(id="8b7cb656", qtype="choice",
    question="[[x]]에 관한 방정식 [[abs(pow(x,2) - 1) - x - k = 0]]이 서로 다른 네\n개의 실근을 가질 때, [[k]]의 값의 범위를 구하면?",
    choices=["[[1 < k < frac(5,4)]]", "[[1 <= k <= frac(5,4)]]", "[[-5 < k < -frac(5,4)]]", "[[k < 1]], [[k > frac(5,4)]]", "[[frac(4,5) < k < 1]]"],
    derived_answer="①", figure=None, difficulty_est=3,
    note="y=|x²−1|과 y=x+k: 가운데 볼록 부분과 2점(1<k<5/4), 바깥 2점(k>1) → 1<k<5/4 → ①.")

# ───────────────────────── 행렬의 연산 ─────────────────────────
# p1 (id 2개, ◎ 연산)
dup(["edbc609a", "7dce5be6"], qtype="choice",
    question=("실수 [[x]], [[y]]에 대하여 [[x]]◎[[y]]를 행렬 [[mat(2,2, -x, y, y, -x)]]라 할 때,\n다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 임의의 실수 [[a]], [[b]]에 대하여 [[a]]◎[[b]] = [[b]]◎[[a]]\n"
              "ㄴ. 임의의 실수 [[a]], [[b]], [[c]], [[d]]에 대하여\n([[a]]◎[[b]]) − ([[c]]◎[[d]]) = ([[a - c]])◎([[b - d]])\n"
              "ㄷ. 임의의 실수 [[a]], [[b]], [[k]]에 대하여\n([[k a]])◎([[k b]]) = [[k]]([[a]]◎[[b]])"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"], derived_answer="④", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: 사용자 정의 연산 ◎ (등식을 텍스트 혼합으로 우회)",
    note="ㄱ✗(a≠b이면 다름), ㄴ✓, ㄷ✓ → ④.")

# p3
add(id="717f0ea1", qtype="choice",
    question="두 행렬 [[A]], [[B]]에 대하여 [[A = mat(2,2, 3, -1, 0, 2)]]이고\n[[A + B = mat(2,2, 3, -1, 3, 0)]]일 때, 행렬 [[B]]의 모든 성분의\n합은?",
    choices=N(1, 2, 3, 4, 5), derived_answer="①", figure=None, difficulty_est=1,
    note="B=(0,0;3,−2) 합 1 → ①.")

# p4
add(id="f4cd0d74", qtype="choice",
    question=("두 행렬 [[A = mat(2,3, 1, a, 2, 3, -2, 0)]], [[B = mat(2,3, 2, 1, a, -1, 3, 5)]]대하여\n"
              "행렬 [[4A + 2B]]의 [[point(1, 2)]]성분과 [[point(2, 1)]]성분이 같다.\n실수 [[a]]의 값은?"),
    choices=N(-2, -1, 0, 1, 2), derived_answer="⑤", figure=None, difficulty_est=1,
    note="4a+2=12−2 → a=2 → ⑤. (원문 '…)대하여' 그대로)")

# p5
add(id="43b84935", qtype="choice",
    question="두 행렬 [[A = mat(2,2, 1, -2, -5, 3)]], [[B = mat(2,2, 1, -2, 3, 1)]]에 대하여\n[[2A + 3X = A + 3B + X]]를 만족시키는 행렬 [[X]]는?",
    choices=["[[mat(2,2, 1,-2, 7,0)]]", "[[mat(2,2, 2,-2, 9,-7)]]", "[[mat(2,2, 1,-2, 0,-6)]]", "[[mat(2,2, 1,-2, 1,-1)]]", "[[mat(2,2, 1,-1, 5,-3)]]"],
    derived_answer="①", figure=None, difficulty_est=2,
    note="출처 [2011년 9월 고2 이과 2번/2점]. X=(3B−A)/2=(1,−2;7,0) → ①.")

# p6
add(id="22e02cd3", qtype="choice",
    question="두 행렬 [[A = mat(2,2, 0, 7, 3, 3)]], [[B = mat(2,2, 2, -1, 1, -1)]]에 대하여\n행렬 [[A - B]]의 모든 성분의 합은?",
    choices=N(6, 9, 12, 15, 18), derived_answer="③", figure=None, difficulty_est=1,
    note="A−B=(−2,8;2,4) 합 12 → ③.")

# p7
add(id="4f27df4d", qtype="choice",
    question="두 행렬 [[A = mat(2,2, -1, 1, 2, 3)]], [[B = mat(2,2, 0, 1, 2, 1)]]에 대하여\n행렬 [[A + 2B]]의 모든 성분의 합은?",
    choices=N(13, 14, 15, 16, 17), derived_answer="①", figure=None, difficulty_est=1,
    note="출처 [2015년 7월 고3 문과 2번/2점]. A+2B=(−1,3;6,5) 합 13 → ①.")

# p8
add(id="95e595d2", qtype="choice",
    question="두 행렬 [[A = mat(2,2, 2, 2, 0, 1)]], [[B = mat(2,2, 1, 0, 2, 1)]]에 대하여\n행렬 [[A + 2B]]의 모든 성분의 합은?",
    choices=N(11, 12, 13, 14, 15), derived_answer="③", figure=None, difficulty_est=1,
    note="출처 [2015년 4월 고3 문과 2번/2점]. A+2B=(4,2;4,3) 합 13 → ③.")

# p9
add(id="ee15cdec", qtype="choice",
    question=("두 행렬 [[A]], [[B]]에 대하여\n[[A + B = mat(2,2, -3, 4, 2, 3)]], [[A - 2B = mat(2,2, -2, 3, 1, 4)]]일 때,\n행렬 [[A - B]]의 모든 성분의 합은?"),
    choices=N(5, 6, 7, 8, 9), derived_answer="②", figure=None, difficulty_est=2,
    note="출처 [2011년 6월 고2 문과 5번/3점]. A−B=((A+B)+2(A−2B))/3 → 성분 합 (6+12)/3=6 → ②.")

# p11
add(id="abbb3c49", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 3, -1, -4, 2)]], [[B = mat(2,2, 5, 1, -3, 4)]]에 대하여\n[[X - 2Y = 3A]], [[X + 4Y = B]]를 만족시키는 행렬\n"
              "[[X]], [[Y]]가 있다. 이때 이차 정사각행렬 [[X + Y]]의 [[point(i, j)]]\n성분에서 [[i = j]]인 성분의 합은?"),
    choices=N(6, 8, 10, 12, 14), derived_answer="④", figure=None, difficulty_est=2,
    note="X+Y=(3/2)A+(1/2)B → 대각합 (3/2)(5)+(1/2)(9)=12 → ④.")

# p14
add(id="ba47db3e", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 2, 1, 3, 5)]], [[B = mat(2,2, 2, -1, -7, 4)]]에 대하여\n[[3X - 2Y = A + 2B]], [[3(Y - X) = 2A - 2B]]를\n"
              "만족시키는 행렬 [[X]], [[Y]]가 있다. [[X = (sub(x,i,j))]],\n[[Y = (sub(y,i,j))]]에서 [[sub(x,1,1) + sub(y,2,1)]]의 값은?"),
    choices=N(12, 15, 18, 21, 24), derived_answer="②", figure=None, difficulty_est=2,
    note="두 식을 더하면 Y=3A → y21=9; 3X=7A+2B → x11=6 → 15 → ②.")

# p15
add(id="5cfc0a59", qtype="short",
    question=("두 이차정사각행렬 [[A]], [[B]]에 대하여 행렬 [[A]]의\n[[point(i, j)]] 성분 [[sub(a,i,j)]]와 행렬 [[B]]의 [[point(i, j)]] 성분 [[sub(b,i,j)]]가 각각\n"
              "[[sub(a,i,j) = sub(a,j,i)]], [[sub(b,i,j) = -sub(b,j,i)]]를 만족시킨다.\n[[A + B = mat(2,2, 4, 6, -2, 3)]]일 때, [[sub(a,2,1) + sub(a,2,2)]]의 값을 구하시오."),
    choices=None, derived_answer="5", figure=None, difficulty_est=2,
    note="b11=b22=0 → a11=4, a22=3; a12+b12=6, a12−b12=−2 → a12=a21=2 → 5.")

# p16
add(id="0f657366", qtype="short",
    question="등식 [[mat(2,2, 1, -x, 4y, 1) + mat(2,2, 2, 5, 3, 4) = mat(2,2, 3, 1, -5, 5)]]를 만족시키는\n실수 [[x]], [[y]]에 대하여 [[x - y]]의 값을 구하시오.",
    choices=None, derived_answer="6", figure=None, difficulty_est=1,
    note="−x+5=1 → x=4, 4y+3=−5 → y=−2 → 6.")

# p17
add(id="352b588e", qtype="short",
    question=("세 행렬 [[A = mat(2,2, a, -1, 6, b)]], [[B = mat(2,2, b, 2, -1, a)]],\n[[C = mat(2,2, 5, 9, -10, 10)]]에 대하여 [[x A + y B = C]]일 때,\n"
              "[[a b - x y]]의 값을 구하시오. (단, [[a]], [[b]], [[x]], [[y]]는 실수이다.)"),
    choices=None, derived_answer="10", figure=None, difficulty_est=2,
    note="−x+2y=9, 6x−y=−10 → x=−1, y=4; −a+4b=5, 4a−b=10 → a=3, b=2 → 6+4=10.")

# p19
add(id="9c6b584b", qtype="choice",
    question=("두 행렬 [[A = mat(2,2, 1, 2, -2, a)]], [[B = mat(2,2, -1, b, -3, 1)]]에 대하여\n[[3A - 2B = mat(2,2, 5, 8, 0, 4)]]일 때, [[a + b]]의 값은?\n(단, [[a]], [[b]]는 실수이다.)"),
    choices=N(1, 2, 3, 4, 5), derived_answer="①", figure=None, difficulty_est=1,
    note="6−2b=8 → b=−1, 3a−2=4 → a=2 → 1 → ①.")

# p22
add(id="9743ab72", qtype="choice",
    question="두 행렬 [[A = mat(2,2, 2, 1, 0, 1)]], [[B = mat(2,2, 1, 0, 4, a)]]에 대하여\n[[2A + B = mat(2,2, 5, 2, 4, 7)]]일 때, [[a]]의 값은?",
    choices=N(1, 2, 3, 4, 5), derived_answer="⑤", figure=None, difficulty_est=1,
    note="출처 [2015년 9월 고3 이과 1번/2점]. 2+a=7 → a=5 → ⑤.")

# p23
add(id="ea2c8db9", qtype="choice",
    question="두 행렬 [[A = mat(2,2, 1, 2, -2, 4)]], [[B = mat(2,1, 3, -1)]]에 대하여\n행렬 [[A B]]의 [[point(1, 1)]] 성분은?",
    choices=N(-3, -1, 1, 3, 5), derived_answer="③", figure=None, difficulty_est=1,
    note="1·3+2·(−1)=1 → ③.")

# p24
add(id="c37d40fa", qtype="choice",
    question=("두 행렬 [[A = mat(2,1, 0, 4)]], [[B = mat(1,2, 0, 1)]]에 대하여 다음 보기 중\n연산이 정의되는 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[A B]]\nㄴ. [[B A]]\nㄷ. [[A + 2 B A]]\nㄹ. [[4 B A]]"),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄴ, ㄹ", "ㄷ, ㄹ", "ㄱ, ㄴ, ㄹ"], derived_answer="⑤", figure=None, difficulty_est=2,
    note="AB(2×2), BA(1×1), 4BA 정의됨; A(2×1)+2BA(1×1)는 정의 안 됨 → ⑤.")

# p26
add(id="9e5b1a9f", qtype="choice",
    question="두 행렬 [[A = mat(3,1, 2, -1, 3)]], [[B = mat(1,3, 3, -4, 5)]]에 대하여\n행렬 [[A B]]의 모든 성분의 합은?",
    choices=N(8, 12, 16, 20, 24), derived_answer="③", figure=None, difficulty_est=2,
    note="(2−1+3)(3−4+5)=4·4=16 → ③.")

# p30
add(id="afb541ee", qtype="choice",
    question="행렬 [[A = mat(2,2, a + 1, 3, -4, -a)]]에서 [[pow(A,2) = A]]를 만족시키는\n양수 [[a]]의 값은?",
    choices=N(2, 3, 4, 5, 6), derived_answer="②", figure=None, difficulty_est=2,
    note="A²=(a²+2a−11, 3; −4, a²−12)=A → a²+a−12=0 → a=3 → ②.")

# p31
add(id="7dfecfc6", qtype="choice",
    question="두 행렬 [[A = mat(2,2, 3, 2, a, 5)]], [[B = mat(2,2, -1, 3, 0, 2)]]에 대하여\n행렬 [[pow(A - B, 2)]]의 모든 성분의 합이 8일 때, 실수 [[a]]의\n값은?",
    choices=N(-3, -2, -1, 1, 2), derived_answer="②", figure=None, difficulty_est=2,
    note="A−B=(4,−1;a,3), (A−B)² 성분 합 18+5a=8 → a=−2 → ②.")

# p33
add(id="62bc9773", qtype="choice",
    question="행렬 [[A = mat(2,2, 3, -1, 0, -3)]]에 대하여 [[pow(A,2) + frac(1,3) X = A]]를\n만족시키는 행렬 [[X]]의 모든 성분의 합은?",
    choices=N(-54, -57, -60, -63, -66), derived_answer="②", figure=None, difficulty_est=2,
    note="A²=9E → X=3(A−9E)=(−18,−3;0,−36) 합 −57 → ②.")

# p35
add(id="4a9bf200", qtype="short",
    question=("좌표평면에서 두 점 [[A(a, b)]], [[B(c, d)]]에 대하여\n이차정사각행렬 [[X]]를 [[X = mat(2,2, a, b, c, d)]]라 하고\n"
              "삼각형 OAB의 넓이를 [[S(X)]]라 하자. 이차정사각행렬\n[[T = mat(2,2, 4, 0, 1, p)]]에 대하여 등식 [[S(pow(T,2)) = S(8T)]]를\n"
              "만족시키는 양의 실수 [[p]]의 값을 구하시오.\n(단, O는 원점이고 세 점 O, A, B는 일직선 위에 있지 않다.)"),
    choices=None, derived_answer="16", figure=None, difficulty_est=3,
    note="S(X)=|ad−bc|/2: S(T²)=8p², S(8T)=128p → p=16.")

# p36
add(id="4619592c", qtype="short",
    question="행렬 [[A = mat(2,2, 1, 0, 1, 1)]]에 대하여 [[pow(A,12)]]의 모든 성분의 합을\n구하시오.",
    choices=None, derived_answer="14", figure=None, difficulty_est=2,
    note="Aⁿ=(1,0;n,1) → A¹²=(1,0;12,1) 합 14.")

# p37
add(id="d5a49040", qtype="choice",
    question=("[[A = mat(2,2, 3, -2, -6, 4)]]에 대하여 행렬 [[pow(A,n)]]의 성분 중 가장 큰\n수를 [[M(n)]], 가장 작은 수를 [[m(n)]]이라 하자.\n"
              "[[M(n) - m(n) > 10000]]을 만족시키는 자연수 [[n]]의\n최솟값은?"),
    choices=N(3, 4, 5, 6, 7), derived_answer="③", figure=None, difficulty_est=3,
    note="A²=7A → Aⁿ=7ⁿ⁻¹A, M−m=10·7ⁿ⁻¹>10000 → n−1≥4 → n=5 → ③.")

# p39
add(id="1b798258", qtype="short",
    question="행렬 [[A = mat(2,2, 1, 2, 0, 1)]]에 대하여 행렬 [[pow(A,100)]]의\n모든 성분의 합을 구하시오.",
    choices=None, derived_answer="202", figure=None, difficulty_est=2,
    note="출처 [2005년 9월 고2 이과 25번]. Aⁿ=(1,2n;0,1) → A¹⁰⁰=(1,200;0,1) 합 202.")
