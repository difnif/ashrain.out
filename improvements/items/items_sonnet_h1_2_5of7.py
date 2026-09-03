# -*- coding: utf-8 -*-
# esc_sonnet_h1-2_5of7 — 이미지 기준 전사 (81 항목 / 80쪽)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_G3 = ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ================= 원의 방정식과 그래프 =================
# p76 — 자취 문제, 선지가 그림
add(id="883c59b9", qtype="choice",
    question=("다음 그림과 같이 중심이 O이고 반지름의 길이가 [[r]]인 원 [[C]]와 이 원 위의 한 점 A에서 접하는 직선 [[l]]이 있다.\n"
              "점 P가 직선 [[l]] 위를 움직일 때, AP′ = [[r × frac(seg(AP), seg(OP))]] 를 만족시키는 선분 OP 위의 점 P′의 자취를 "
              "가장 옳게 나타낸 것은? (단, 점선은 원 [[C]]이다.)"),
    choices=["(그림) 선분 OA",
             "(그림) 선분 OA를 대각선으로 하는 정사각형",
             "(그림) 선분 OA를 긴 대각선으로 하는 마름모",
             "(그림) 선분 OA를 지름으로 하는 원",
             "(그림) 두 점 O, A를 양 끝으로 하는 볼록한 두 호(렌즈 모양)"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 C(중심 O, 반지름 r), 접점 A, 접선 l 위의 점 P, 선분 OP 위의 점 P′; 선지 ①~⑤는 점선 원 C 안에 그린 자취 그림"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="선지가 그림(자취) / 프라임 점 라벨 AP′(선분 위 줄 표기 불가, 텍스트) / 도형 표현 불가",
    note="AP′ = OA·AP/OP = A에서 OP에 내린 수선의 길이 → P′는 수선의 발 → ∠AP′O=90° → OA를 지름으로 하는 원 ④ = 빠른정답 ✓.")

# p78
add(id="5a15878a", qtype="choice",
    question=("중심이 O이고 반지름의 길이가 [[r]]인 원 [[C]]와 이 원 위의 한 점 A에서 접하는 직선 [[l]]이 있다.\n"
              "점 P가 직선 [[l]] 위를 움직일 때, [[seg(OP)]] · OP′ = [[pow(r,2)]]을 만족시키는 선분 OP 위의 점 P′의 자취를 "
              "가장 옳게 나타낸 것은? (단, 점선은 원 [[C]]이다.)"),
    choices=["(그림) 선분 OA",
             "(그림) 두 점 O, A를 양 끝으로 하는 볼록한 두 호(렌즈 모양)",
             "(그림) 선분 OA를 지름으로 하는 원",
             "(그림) 선분 OA를 대각선으로 하는 정사각형",
             "(그림) 선분 OA를 긴 대각선으로 하는 마름모"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원 C(중심 O, 반지름 r), 접점 A, 접선 l 위의 점 P, 선분 OP 위의 점 P′; 선지 ①~⑤는 점선 원 C 안에 그린 자취 그림"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="선지가 그림(자취) / 프라임 점 라벨 OP′(텍스트) / 도형 표현 불가",
    note="출처 [2004년 6월 고2 이과 19번]. OP·OP′=r² → P′는 P의 반전, 접선 l의 반전상은 OA를 지름으로 하는 원 → ③. 빠른정답 41은 정렬 오류로 보임.")

# ================= 대우를 이용한 증명법과 귀류법 =================
# p2
add(id="0f17915b", qtype="choice",
    question=("다음은 명제 ‘정수 [[a]], [[b]]에 대하여 [[pow(a,2) + pow(b,2)]]이 짝수이면 [[a + b]]가 짝수이다.’가 참임을 대우를 이용하여 증명하는 과정이다. "
              "이때 (가), (나), (다)에 들어갈 알맞은 것은?\n"
              "주어진 명제의 대우 ‘[[a + b]]가 홀수이면 [[pow(a,2) + pow(b,2)]]이 (가) 이다.’가 참임을 보이면 된다.\n"
              "[[a + b]]가 홀수이므로 [[a + b = 2k - 1]] ([[k]]는 정수)라 하자.\n"
              "[[pow(a,2) + pow(b,2) = pow(a + b, 2)]] − ((나)) = 2((다)) + 1\n"
              "이고 (다) 는 정수이므로 [[pow(a,2) + pow(b,2)]]은 (가) 이다.\n"
              "따라서 주어진 명제의 대우가 참이므로 주어진 명제도 참이다."),
    choices=["(가) 홀수, (나) [[2a b]], (다) [[2pow(k,2) - 2k - a b]]",
             "(가) 홀수, (나) [[2a b]], (다) [[pow(k,2) - k - a b]]",
             "(가) 홀수, (나) [[4a b]], (다) [[2pow(k,2) - 2k - 2a b]]",
             "(가) 짝수, (나) [[4a b]], (다) [[pow(k,2) - k - 2a b]]",
             "(가) 짝수, (나) [[2a b]], (다) [[2pow(k,2) + 2k + a b]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.9,
    note="(2k−1)²−2ab = 2(2k²−2k−ab)+1 → ① = 빠른정답 ✓.")

# p8
add(id="2ba9cd79", qtype="choice",
    question=("다음은 자연수 [[n]]에 대하여 명제 ‘[[pow(n,2)]]이 6의 배수이면 [[n]]도 6의 배수이다.’가 참임을 그 대우를 이용하여 증명하는 과정이다.\n"
              "주어진 명제의 대우는 ‘[[n]]이 6의 배수가 아니면 [[pow(n,2)]]도 6의 배수가 아니다.’이다.\n"
              "[[k]]가 자연수일 때 [[n]]을 [[6k - 1]] 또는 [[6k - 2]] 또는 (가) 또는 [[6k - 4]] 또는 [[6k - 5]]라 하면\n"
              "(i) [[n = 6k - 1]]일 때, [[pow(n,2) = 6(6pow(k,2) - 2k) + 1]]\n"
              "(ii) [[n = 6k - 2]]일 때, [[pow(n,2) = 6(6pow(k,2) - 4k) + 4]]\n"
              "(iii) [[n]] = (가) 일 때, [[pow(n,2) = 6(6pow(k,2) - 6k + 1)]] + (나)\n"
              "(iv) [[n = 6k - 4]]일 때, [[pow(n,2) = 6(6pow(k,2) - 8k + 2) + 4]]\n"
              "(v) [[n = 6k - 5]]일 때, [[pow(n,2)]] = 6((다)) + 1\n"
              "즉, [[pow(n,2)]]은 6으로 나누면 나머지가 1 또는 (나) 또는 4인 자연수가 되므로 [[n]]이 6의 배수가 아니면 [[pow(n,2)]]도 6의 배수가 아니다.\n"
              "따라서 주어진 명제의 대우가 참이므로 주어진 명제도 참이다.\n"
              "위의 과정에서 (가), (다)에 알맞은 식을 각각 [[f(k)]], [[g(k)]], (나)에 알맞은 수를 [[a]]라 할 때, [[f(a) + g(a)]]의 값은?"),
    choices=["41", "43", "45", "47", "49"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="(가)=6k−3, (나)=3, (다)=6k²−10k+4 → f(3)+g(3)=15+28=43 → ②. 빠른정답 4와 불일치.")

# p12
add(id="46816fa1", qtype="choice",
    question=("다음은 명제 ‘세 자연수 [[a]], [[b]], [[c]]에 대하여 [[pow(a,2) + pow(b,2) = pow(c,2)]]이면 [[a]], [[b]], [[c]] 중 적어도 하나는 3의 배수이다.’의 참, 거짓을 대우를 이용하여 증명하는 과정이다.\n"
              "주어진 명제의 대우는\n‘세 자연수 [[a]], [[b]], [[c]]에 대하여 모두 3의 배수가 아니면 [[pow(a,2) + pow(b,2) != pow(c,2)]]이다.’이므로\n"
              "[[pow(a,2) + pow(b,2) = 3m]] + (가), [[pow(c,2) = 3n]] + (나)\n"
              "∴ [[pow(a,2) + pow(b,2) != pow(c,2)]] (단, [[m]], [[n]]은 음이 아닌 정수)\n"
              "따라서 대우가 (다) 이므로 주어진 명제도 (다) 이다.\n"
              "위 과정에서 (가) ~ (다)에 알맞은 것은?"),
    choices=["(가) 1, (나) 0, (다) 참", "(가) 1, (나) 2, (다) 거짓", "(가) 2, (나) 1, (다) 참", "(가) 2, (나) 0, (다) 참", "(가) 2, (나) 1, (다) 거짓"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="3의 배수 아닌 수의 제곱은 3으로 나눈 나머지 1 → a²+b²=3m+2, c²=3n+1, 대우 참 → ③ = 빠른정답 ✓.")

# p13
add(id="45c445c4", qtype="choice",
    question=("다음은 자연수 [[n]]에 대하여 명제 ‘[[pow(n,2)]]이 3의 배수이면 [[n]]도 3의 배수이다.’를 증명한 것이다.\n"
              "주어진 명제의 대우를 구하면\n‘[[n]]이 3의 배수가 아니면 [[pow(n,2)]]도 (가) ’이다.\n"
              "[[n]]이 3의 배수가 아니므로\n[[n]] = [[3m]] ± (나) ([[m]]은 자연수)에서\n"
              "[[pow(n,2)]] = [[9pow(m,2)]] ± [[6m]] + 1 = 3([[3pow(m,2)]] ± [[2m]]) + 1\n"
              "이때 [[3pow(m,2)]] ± [[2m]]이 (다) 이므로 [[pow(n,2)]]은 (라) \n"
              "따라서 대우가 (마) 이므로 주어진 명제도 (마) 이다.\n"
              "위의 과정에서 빈칸에 들어갈 수나 식이 잘못 연결된 것은?"),
    choices=["(가) 3의 배수가 아니다.", "(나) 1", "(다) 자연수", "(라) 3의 배수이다.", "(마) 참"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="(라)는 '3의 배수가 아니다'여야 하므로 잘못 연결된 것은 ④. 빠른정답 2와 불일치. ± 기호는 텍스트로 처리.")

# p18
add(id="df87ec93", qtype="choice",
    question=("다음은 자연수 [[n]]에 대하여 [[sqrt(pow(n,2) + 2n)]]이 무리수임을 증명하는 과정이다.\n"
              "[[sqrt(pow(n,2) + 2n) = sqrt(pow(n + 1, 2) - 1)]]이고\n"
              "[[sqrt(pow(n + 1, 2) - 1)]]이 유리수라 가정하면\n"
              "[[sqrt(pow(n + 1, 2) - 1) = frac(q, p)]] ([[p]], [[q]]는 서로소인 자연수)로 놓을 수 있다.\n"
              "이 식의 양변을 제곱하면\n[[pow(n + 1, 2) - 1 = frac(pow(q,2), pow(p,2))]] ⋯ ㉠\n"
              "㉠의 좌변은 자연수이고, [[p]]와 [[q]]는 서로소이므로\n[[pow(p,2)]] = (가) ⋯ ㉡\n"
              "㉡을 ㉠에 대입하여 정리하면\n[[pow(n + 1, 2) - pow(q,2) = 1]], ((나))([[n + 1 - q]]) = 1\n"
              "∴ (다) = 0, [[n - q = 0]] 또는\n(다) = −2, [[n - q = -2]]\n"
              "그런데 이것은 [[n]], [[q]]가 자연수라는 가정에 모순이므로\n[[sqrt(pow(n,2) + 2n)]]은 무리수이다.\n"
              "위의 과정에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) 1, (나) [[n + 1 + q]], (다) [[p - n]]",
             "(가) 1, (나) [[n - 1 + q]], (다) [[n + q]]",
             "(가) 1, (나) [[n + 1 + q]], (다) [[n + q]]",
             "(가) 2, (나) [[n - 1 + q]], (다) [[p - n]]",
             "(가) 2, (나) [[n + 1 + q]], (다) [[p - n]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="p²=1, (n+1+q)(n+1−q)=1 → n+q=0 … → ③ = 빠른정답 ✓.")

# p24
add(id="dc6e9e28", qtype="choice",
    question=("다음은 자연수 [[n]]에 대하여 [[sqrt(pow(n,2) + 4n + 3)]]이 무리수임을 증명하는 과정이다.\n"
              "[[sqrt(pow(n,2) + 4n + 3) = sqrt(pow(n + 2, 2) - 1)]]이고\n"
              "[[sqrt(pow(n + 2, 2) - 1)]]이 유리수라 가정하면\n"
              "[[sqrt(pow(n + 2, 2) - 1) = frac(q, p)]] ([[p]], [[q]]는 서로소인 자연수)로 놓을 수 있다.\n"
              "이 식의 양변을 제곱하면\n[[pow(n + 2, 2) - 1 = frac(pow(q,2), pow(p,2))]] ⋯ ㉠\n"
              "㉠의 좌변은 자연수이고, [[p]]와 [[q]]는 서로소이므로\n[[pow(p,2)]] = (가) ⋯ ㉡\n"
              "㉡을 ㉠에 대입하여 정리하면\n[[pow(n + 2, 2) - pow(q,2) = 1]], ((나))([[n + 2 - q]]) = 1\n"
              "∴ (다) = −1, [[n - q = -1]] 또는\n(다) = −3, [[n - q = -3]]\n"
              "그런데 이것은 [[n]], [[q]]가 자연수라는 가정에 모순이므로\n[[sqrt(pow(n,2) + 4n + 3)]]은 무리수이다.\n"
              "위의 과정에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) 1, (나) [[n + 2 + q]], (다) [[n + q]]",
             "(가) 1, (나) [[n - 2 + q]], (다) [[n + q]]",
             "(가) 1, (나) [[n + 2 + q]], (다) [[n - q]]",
             "(가) 2, (나) [[n - 2 + q]], (다) [[p - n]]",
             "(가) 2, (나) [[n + 2 + q]], (다) [[n + q]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.85,
    note="p²=1, (n+2+q)(n+2−q)=1 → n+q=−1, n−q=−1 … → (1, n+2+q, n+q) = ①. 빠른정답 5와 불일치.")

# p28
add(id="b278ff33", qtype="choice",
    question=("다음은 [[n >= 3]]인 자연수 [[n]]에 대하여 [[sqrt(pow(n,2) - 3)]]이 무리수임을 증명한 것이다.\n"
              "[[sqrt(pow(n,2) - 3)]]이 유리수라고 가정하면\n"
              "[[sqrt(pow(n,2) - 3) = frac(q, p)]] ([[p]], [[q]]는 서로소인 자연수)로 놓을 수 있다.\n"
              "이 식의 양변을 제곱하여 정리하면\n[[pow(p,2)(pow(n,2) - 3) = pow(q,2)]]이다.\n"
              "[[p]]는 [[pow(q,2)]]의 약수이고 [[p]], [[q]]는 서로소인 자연수이므로\n[[pow(n,2)]] = (가) 이다.\n"
              "자연수 [[k]]에 대하여\n(i) [[q = 2k]]일 때\n[[pow(2k, 2) < pow(n,2)]] < (나) 인 자연수 [[n]]이 존재하지 않는다.\n"
              "(ii) [[q = 2k + 1]]일 때\n(나) < [[pow(n,2) < pow(2k + 2, 2)]]인 자연수 [[n]]이 존재하지 않는다.\n"
              "(i), (ii)에 의하여\n[[sqrt(pow(n,2) - 3) = frac(q, p)]] ([[p]], [[q]]는 서로소인 자연수)\n"
              "를 만족하는 자연수 [[n]]은 존재하지 않는다.\n따라서 [[sqrt(pow(n,2) - 3)]]은 무리수이다.\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(q)]], [[g(k)]]라 할 때, [[f(4) + g(3)]]의 값은?"),
    choices=["66", "67", "68", "69", "70"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="(가)=q²+3, (나)=(2k+1)² → f(4)+g(3)=19+49=68 → ③. 빠른정답 1과 불일치.")

# p29
add(id="32740506", qtype="choice",
    question=("다음은 두 자연수 [[m]], [[n]]에 대하여 [[2pow(m,2) + 2pow(n,2)]]이 8의 배수이면 [[m]], [[n]]은 모두 짝수임을 증명한 것이다.\n<보기>\n"
              "[[m]], [[n]] 중 적어도 하나가 홀수라 가정하면\n"
              "(i) [[m = 2a]], [[n = 2b - 1]] ([[a]], [[b]]는 자연수)일 때, [[2pow(m,2) + 2pow(n,2)]]을 8로 나누었을 때의 나머지는 (가) 이다.\n"
              "(ii) [[m = 2a - 1]], [[n = 2b]] ([[a]], [[b]]는 자연수)일 때, [[2pow(m,2) + 2pow(n,2)]]을 8로 나누었을 때의 나머지는 (나) 이다.\n"
              "(iii) [[m = 2a - 1]], [[n = 2b - 1]] ([[a]], [[b]]는 자연수)일 때, [[2pow(m,2) + 2pow(n,2)]]을 8로 나누었을 때의 나머지는 (다) 이다.\n"
              "(i), (ii), (iii)에 의하여 [[2pow(m,2) + 2pow(n,2)]]은 8의 배수가 아니다. 이것은 [[2pow(m,2) + 2pow(n,2)]]이 8의 배수라는 조건에 모순이다.\n"
              "따라서 두 자연수 [[m]], [[n]]에 대하여 [[2pow(m,2) + 2pow(n,2)]]이 8의 배수이면 [[m]], [[n]]은 모두 짝수이다.\n"
              "위의 증명에서 (가), (나), (다)에 알맞은 것은?"),
    choices=["(가) 2, (나) 2, (다) 3", "(가) 2, (나) 2, (다) 4", "(가) 2, (나) 4, (다) 4", "(가) 4, (나) 2, (다) 4", "(가) 4, (나) 4, (다) 6"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="홀수 제곱의 2배 = 8(…)+2 → (i)(ii) 나머지 2, (iii) 4 → ② = 빠른정답 ✓.")

# p30
add(id="d1818056", qtype="short",
    question=("다음은 명제 ‘[[pow(x,2) + pow(y,2) = 7]]을 만족시키는 두 양의 유리수 [[x]], [[y]]는 존재하지 않는다.’를 증명하는 과정이다.\n"
              "[[pow(x,2) + pow(y,2) = 7]]을 만족시키는 두 양의 유리수 [[x]], [[y]]가 존재한다고 가정하면\n"
              "[[x = frac(m, n)]], [[y = frac(p, q)]]\n([[m]]과 [[n]], [[p]]와 [[q]]는 각각 서로소인 자연수)\n으로 나타낼 수 있다.\n"
              "이때 [[pow(x,2) + pow(y,2) = 7]]에서\n[[frac(pow(m,2) pow(q,2), pow(n,2))]] = (가) − [[pow(p,2)]] ⋯ ㉠\n"
              "(가) − [[pow(p,2)]]은 정수이고 [[m]]과 [[n]]은 서로소이므로\n[[q = k n]] ([[k]]는 정수)이어야 한다.\n"
              "즉, ㉠에서 [[pow(k m, 2) + pow(p,2)]] = (가) 이고\n[[k m = 7a + r]], [[p = 7b + s]]\n"
              "([[a]], [[b]], [[r]], [[s]]은 정수이고, [[0 <= r < 7]], [[0 <= s < 7]])\n라 하면\n"
              "[[pow(k m, 2) + pow(p,2)]]\n= [[7(7pow(a,2) + 2a r + 7pow(b,2) + 2b s)]] + (나) + [[pow(s,2)]]\n"
              "그런데 [[pow(k m, 2) + pow(p,2)]]은 (다) 의 배수이므로 [[q]]도 (다) 의 배수이고, 이것은 [[p]]와 [[q]]가 서로소라는 가정에 모순이다.\n"
              "따라서 [[pow(x,2) + pow(y,2) = 7]]을 만족시키는 두 양의 유리수 [[x]], [[y]]는 존재하지 않는다.\n"
              "위의 (가), (나)에 알맞은 식을 각각 [[f(q)]], [[g(r)]]이라 하고, (다)에 알맞은 수를 [[a]]라 할 때, [[a + frac(f(4), g(2))]]의 값을 구하시오."),
    choices=None, derived_answer="35", figure=None, difficulty_est=3, confidence=0.85,
    note="(가)=7q², (나)=r², (다)=7 → 7 + 112/4 = 35. 빠른정답 4와 불일치.")

# p37
add(id="794a15a1", qtype="choice",
    question="[[a]], [[b]], [[x]], [[y]]가 실수일 때, 두 수 [[A = (pow(a,2) + pow(b,2))(pow(x,2) + pow(y,2))]], [[B = pow(a x + b y, 2)]]의 대소 관계는?",
    choices=["[[A > B]]", "[[A >= B]]", "[[A < B]]", "[[A <= B]]", "[[A = B]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="A−B=(ay−bx)²≥0 → A≥B → ② = 빠른정답 ✓.")

# p38
add(id="e931d36b", qtype="choice",
    question="[[x >= 1]], [[y >= 1]]일 때, 두 수 [[A = x + y]], [[B = x y + 1]]의 대소 관계는?",
    choices=["[[A < B]]", "[[A <= B]]", "[[A > B]]", "[[A >= B]]", "[[A = B]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="B−A=(x−1)(y−1)≥0 → A≤B → ② = 빠른정답 ✓.")

# p45
add(id="d3868211", qtype="choice",
    question="[[a]], [[b]], [[x]], [[y]]가 실수일 때, 두 수 [[A = (pow(a,2) + pow(b,2))(pow(x,2) + pow(y,2))]], [[B = pow(a x - b y, 2)]]의 대소 관계는?",
    choices=["[[A > B]]", "[[A >= B]]", "[[A < B]]", "[[A <= B]]", "[[A = B]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="A−B=(ay+bx)²≥0 → A≥B → ② = 빠른정답 ✓.")

# p48
add(id="2c530d88", qtype="choice",
    question="실수 [[a]], [[b]]에 대하여 [[a b > 0]]일 때, [[A = abs(a + b)]], [[B = abs(a - b)]]의 대소 관계를 바르게 나타낸 것은?",
    choices=["[[A > B]]", "[[A >= B]]", "[[A < B]]", "[[A <= B]]", "[[A = B]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="A²−B²=4ab>0, A,B≥0 → A>B → ①. 빠른정답 2와 불일치.")

# p49
add(id="c94f2f54", qtype="choice",
    question="[[a > 0]], [[b > 0]]일 때, [[sqrt(2(a + b))]], [[sqrt(a) + sqrt(b)]]의 대소를 바르게 나타낸 것은?",
    choices=["[[sqrt(2(a + b)) < sqrt(a) + sqrt(b)]]", "[[sqrt(2(a + b)) <= sqrt(a) + sqrt(b)]]", "[[sqrt(2(a + b)) > sqrt(a) + sqrt(b)]]",
             "[[sqrt(2(a + b)) >= sqrt(a) + sqrt(b)]]", "[[sqrt(2(a + b)) = sqrt(a) + sqrt(b)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="2(a+b)−(√a+√b)²=(√a−√b)²≥0 → ④. 빠른정답 5와 불일치.")

# p61
add(id="4c43a3ae", qtype="choice",
    question=("[[x + y = 4]]를 만족시키는 두 양수 [[x]], [[y]]에 대하여 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[x y]]의 최댓값은 4이다.\nㄴ. [[pow(x,2) + pow(y,2) >= 8]]\nㄷ. [[frac(y, x) + frac(x, y) >= 2]]"),
    choices=CH_G3, derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="xy≤4, x²+y²=16−2xy≥8, y/x+x/y≥2 → ⑤ = 빠른정답 ✓.")

# p63
add(id="a042317b", qtype="choice",
    question=("[[x]], [[y]]가 실수일 때, 다음 보기 중 절대부등식인 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[pow(x,2) + 4 >= -4x]]\nㄴ. [[pow(x,2) + 3x + 3 > 0]]\nㄷ. [[pow(x - 6y, 2) >= -12x y]]"),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    note="ㄱ (x+2)²≥0 ✓, ㄴ 판별식<0 ✓, ㄷ x²+36y²≥0 ✓ → ⑤. 빠른정답 1과 불일치.")

# p68
add(id="0a01c835", qtype="short",
    question="모든 실수 [[x]], [[y]]에 대하여 부등식 [[2pow(x,2) + 4a x y + 3b pow(y,2) >= 0]]이 성립하도록 하는 10 이하의 자연수 [[a]], [[b]]의 순서쌍 [[point(a, b)]]의 개수를 구하시오.",
    choices=None, derived_answer="23", figure=None, difficulty_est=3, confidence=0.85,
    note="판별식 조건 2a²≤3b: a=1→10개, a=2→8개, a=3→5개 → 23. 빠른정답 2와 불일치.")

# p76
add(id="8277016e", qtype="choice",
    question=("실수 [[a]], [[b]]에 대하여 [[pow(a,2) + pow(b,2) >= -a b]]임을 증명한 것이다. (가), (나)에 들어갈 부등호로 알맞은 것은?\n"
              "[[A = pow(a,2) + pow(b,2)]], [[B = -a b]]라 하면\n"
              "[[A - B = pow(a,2) + pow(b,2) - (-a b)]]\n= [[pow(a,2) + pow(b,2) + a b]]\n"
              "= [[pow(a,2) + a b + frac(pow(b,2), 4) + frac(3,4) pow(b,2)]]\n"
              "= [[pow(a + frac(b, 2), 2) + frac(3,4) pow(b,2)]] (가) 0\n"
              "따라서 [[A - B]] (가) 0이므로\n[[A]] (나) [[B]]이다.\n∴ [[pow(a,2) + pow(b,2) >= -a b]]\n(단, 등호는 [[a = b = 0]]일 때 성립)"),
    choices=["(가) >, (나) ≥", "(가) ≥, (나) ≥", "(가) >, (나) >", "(가) <, (나) ≥", "(가) ≤, (나) ≤"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    note="(가) ≥, (나) ≥ → ②. 빠른정답 5와 불일치.")

# p79
add(id="3c2a220d", qtype="choice",
    question=("[[a >= 0]], [[b >= 0]]일 때, [[frac(a + b, 2)]] (가) [[sqrt(a b)]] 임을 다음과 같은 과정으로 증명하였다. 이 과정에서 (가), (나), (다)에 알맞을 것을 순서대로 쓴 것을 고르면?\n"
              "증명\n[[frac(a + b, 2) - sqrt(a b)]] = ((나))² / 2 이므로 부등식\n"
              "[[frac(a + b, 2)]] (가) [[sqrt(a b)]] 이 성립함을 알 수 있다. 이때 등호는 (다) 일 때, 성립한다."),
    choices=["≥, [[sqrt(a) - sqrt(b)]], [[a = b]]", "≥, [[a - b]], [[a = b = 0]]", ">, [[sqrt(a) - sqrt(b)]], [[a = b]]",
             ">, [[a - b]], [[a = b]]", "≥, [[sqrt(a) - sqrt(b)]], [[a >= b]]"],
    derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    note="(a+b)/2−√(ab)=(√a−√b)²/2≥0, 등호 a=b → ①. 빠른정답 2와 불일치.")

# p80
add(id="5d83dca5", qtype="choice",
    question=("다음은 [[a > 0]], [[b > 0]]일 때, [[sqrt(a) + sqrt(b) > sqrt(a + b)]]임을 증명하는 과정이다. 빈칸에 들어갈 식 또는 기호를 차례대로 나열한 것은?\n"
              "[[a > 0]], [[b > 0]]일 때,\n(가) − (나)\n= [[(a + 2 sqrt(a b) + b) - (a + b) = 2 sqrt(a b) > 0]]\n"
              "∴ [[pow(sqrt(a) + sqrt(b), 2) > pow(sqrt(a + b), 2)]]\n"
              "그런데 [[sqrt(a) + sqrt(b)]] (다) 0이므로\n[[sqrt(a) + sqrt(b) > sqrt(a + b)]]"),
    choices=["(가) [[sqrt(a) + sqrt(b)]], (나) [[sqrt(a + b)]], (다) <",
             "(가) [[sqrt(a) + sqrt(b)]], (나) [[sqrt(a + b)]], (다) >",
             "(가) [[pow(sqrt(a) + sqrt(b), 2)]], (나) [[pow(sqrt(a + b), 2)]], (다) <",
             "(가) [[pow(sqrt(a) + sqrt(b), 2)]], (나) [[pow(sqrt(a + b), 2)]], (다) >",
             "(가) [[pow(sqrt(a + b), 2)]], (나) [[pow(sqrt(a) + sqrt(b), 2)]], (다) >"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.85,
    note="(√a+√b)² − (√(a+b))² = 2√(ab) > 0, √a+√b > 0 → ④. 빠른정답 3과 불일치.")

# p81
add(id="14bdb641", qtype="choice",
    question=("다음은 [[a]], [[b]], [[c]]가 실수일 때, [[pow(a,2) + pow(b,2) + pow(c,2) >= a b + b c + c a]]를 증명하는 과정이다.\n"
              "[[(pow(a,2) + pow(b,2) + pow(c,2)) - (a b + b c + c a)]]를 정리하면\n"
              "(가) {[[pow(a - b, 2) + pow(b - c, 2) + pow(c - a, 2)]]} (나) 0\n"
              "따라서 [[(pow(a,2) + pow(b,2) + pow(c,2)) - (a b + b c + c a) >= 0]]이므로\n"
              "[[pow(a,2) + pow(b,2) + pow(c,2) >= a b + b c + c a]]\n(단, 등호는 [[a = b = c]]일 때 성립)\n"
              "위의 과정에서 (가), (나)에 알맞은 것은?"),
    choices=["(가) [[frac(1,2)]], (나) ≤", "(가) [[frac(1,2)]], (나) ≥", "(가) 2, (나) ≤", "(가) 2, (나) ≥", "(가) 2, (나) ="],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="½{(a−b)²+(b−c)²+(c−a)²} ≥ 0 → ② = 빠른정답 ✓.")

# p84 — 코시·슈바르츠 증명(줄임표 다수)
_SA = "[[pow(sub(a,1), 2) + pow(sub(a,2), 2)]] + ⋯ + [[pow(sub(a,n), 2)]]"
_SB = "[[pow(sub(b,1), 2) + pow(sub(b,2), 2)]] + ⋯ + [[pow(sub(b,n), 2)]]"
_SAB = "[[sub(a,1) sub(b,1) + sub(a,2) sub(b,2)]] + ⋯ + [[sub(a,n) sub(b,n)]]"
add(id="18fd81d8", qtype="choice",
    question=("다음은 [[sub(a,1)]], [[sub(a,2)]], ⋯, [[sub(a,n)]], [[sub(b,1)]], [[sub(b,2)]], ⋯, [[sub(b,n)]]이 실수일 때, 부등식\n"
              f"({_SA})({_SB}) ≥ ({_SAB})²\n이 성립함을 증명한 것이다.\n"
              "모든 실수 [[x]]에 대하여 부등식\n"
              "[[pow(sub(a,1) x - sub(b,1), 2) + pow(sub(a,2) x - sub(b,2), 2)]] + ⋯ + [[pow(sub(a,n) x - sub(b,n), 2)]] (가) 0\n"
              "이 성립한다. 이 식을 전개하여 [[x]]에 대해 정리하면\n"
              f"({_SA})[[pow(x,2)]] − 2({_SAB})[[x]] + ({_SB}) (가) 0 ⋯ ㉠\n"
              "(i) [[pow(sub(a,1), 2) + pow(sub(a,2), 2)]] + ⋯ + [[pow(sub(a,n), 2) <= 0]]일 때,\n"
              "[[sub(a,1) = sub(a,2)]] = ⋯ = [[sub(a,n) = 0]]이므로 주어진 부등식이 성립한다.\n"
              "(ii) [[pow(sub(a,1), 2) + pow(sub(a,2), 2)]] + ⋯ + [[pow(sub(a,n), 2) > 0]]일 때,\n"
              "[[x]]에 대한 이차방정식\n"
              f"({_SA})[[pow(x,2)]] − 2({_SAB})[[x]] + ({_SB}) = 0\n"
              "의 판별식을 [[D]]라고 하면 ㉠이 항상 성립하므로\n"
              f"[[frac(D, 4)]] = ({_SAB})² (나) ({_SA}) × ({_SB}) (다) 0\n"
              "(i), (ii)에서\n"
              f"({_SA})({_SB}) ≥ ({_SAB})²\n"
              "(단, 등호는 [[frac(sub(b,1), sub(a,1)) = frac(sub(b,2), sub(a,2))]] = ⋯ = [[frac(sub(b,n), sub(a,n))]]일 때 성립)\n"
              "위의 증명에서 (가), (나), (다)에 알맞은 것을 순서대로 적은 것은?"),
    choices=["≤, −, ≤", "≤, +, ≥", "≥, −, ≤", "≥, −, <", ">, +, ≤"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    note="제곱합 ≥ 0, D/4 = (Σab)² − (Σa²)(Σb²) ≤ 0 → (≥, −, ≤) = ③. 빠른정답 2와 불일치. 줄임표 항은 마커 밖 텍스트.")

# p97
add(id="ad9d6414", qtype="choice",
    question=("두 실수 [[a]], [[b]]에 대하여 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[pow(a + b, 2) >= 3a b]]\n"
              "ㄴ. [[sqrt(2 abs(a) + 2 abs(b)) >= sqrt(3 abs(a)) + sqrt(3 abs(b))]]\n"
              "ㄷ. [[sqrt(pow(a,2) + pow(b,2)) <= abs(a - b)]]\n"
              "ㄹ. [[pow(a,2) + 4pow(b,2) + 16 >= 8a + 16b - 4a b]]"),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄹ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄹ"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="ㄱ a²−ab+b²≥0 ✓, ㄴ a=b=1 반례 ✗, ㄷ ab>0이면 ✗, ㄹ (a+2b−4)²≥0 ✓ → ③ = 빠른정답 ✓.")

# ================= 역함수 =================
INV = "역함수 적용 표기 f⁻¹(k)(마커 밖 텍스트 혼합)"
COMPA = "합성함수 적용 표기 (g∘f)(x)(마커 밖 텍스트 혼합)"
PW = "조각적(경우 나눔) 정의 함수 — 식을 콤마로 나열"

# p6
add(id="db7ba651", qtype="choice",
    question="다음 그림은 함수 [[f]]: [[X]]→[[X]]를 나타낸 것이다.\n[[inv(f)]](3)의 값은?",
    choices=["1", "2", "3", "4", "5"], derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={1,2,3,4,5}→X, f: 1→3, 2→1, 3→5, 4→2, 5→4"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 함수 대응 그림 / " + INV,
    note="출처 [2026년 3월 고2 4번 변형]. f(1)=3 → f⁻¹(3)=1 → ①. 빠른정답 2와 불일치.")

# p12
add(id="6abd92e8", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 역함수가 존재하고, 다음 조건을 모두 만족시킨다.\n"
              "(가) [[x]] = 1, 2, 5일 때, ([[comp(f, f)]])([[x]]) + 2[[inv(f)]]([[x]]) = [[3x]]이다.\n"
              "(나) [[f(5) != 5]]\n"
              "[[f(3) × (f(4) + f(6))]]의 값을 구하시오."),
    choices=None, derived_answer="48", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=COMPA + " / " + INV,
    note="출처 [2018년 11월 고1 30번 변형]. 전수 확인(순열 720개) 결과 48 = 빠른정답 ✓. 원문 중괄호 {f(4)+f(6)}는 소괄호로.")

# p13
add(id="8c560099", qtype="choice",
    question=("최고차항의 계수가 양수인 이차함수 [[f(x)]]에 대하여 함수 [[g(x)]]를 다음과 같이 정의하자.\n"
              "[[g(x) = -x + 4]] ([[x < -2]]), [[g(x) = f(x)]] ([[-2 <= x <= 1]]), [[g(x) = -x - 2]] ([[x > 1]])\n"
              "함수 [[g(x)]]의 치역이 실수 전체의 집합이고, 함수 [[g(x)]]의 역함수가 존재할 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[f(-2) + f(1) = 3]]\n"
              "ㄴ. [[g(0) = -1]], [[g(1) = -3]]이면 곡선 [[y = f(x)]]의 꼭짓점의 [[x]]좌표는 [[frac(5,2)]]이다.\n"
              "ㄷ. 곡선 [[y = f(x)]]의 꼭짓점의 [[x]]좌표가 [[-2]]이면 [[inv(g)]](1) = 0이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.75,
    needs_review=PW + " / " + INV,
    note="출처 [2019년 3월 고2 문과 21번/4점]. f(−2)=6, f(1)=−3 ㄱ✓; ㄴ f=½x²−5/2x−1 → 꼭짓점 5/2 ✓; ㄷ ✗ → ③ = 빠른정답 ✓.")

# p14
add(id="6bcb11fa", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6, 7)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 역함수가 존재하고, 다음 조건을 만족시킨다.\n"
              "(가) [[x]] = 1, 2, 6일 때 ([[comp(f, f)]])([[x]]) + [[inv(f)]]([[x]]) = [[2x]]이다.\n"
              "(나) [[f(3) + f(5) = 10]]\n"
              "[[f(6) != 6]]일 때, [[f(4) × (f(6) + f(7))]]의 값을 구하시오."),
    choices=None, derived_answer="50", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=COMPA + " / " + INV,
    note="출처 [2018년 11월 고1 30번/4점]. 전수 확인 결과 50. 빠른정답 3과 불일치. 원문 중괄호는 소괄호로.")

# p15
add(id="1adeeb19", qtype="short",
    question=("두 집합 [[X = setb(x, 0 <= x <= 2)]], [[Y = setb(y, a <= y <= b)]]에서 [[f]]: [[X]]→[[Y]], [[f(x) = 3x - 1]]의 역함수 "
              "[[inv(f)]]: [[Y]]→[[X]]가 존재할 때, 실수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.9,
    note="치역 [−1, 5] → a+b=4. 빠른정답 48과 불일치.")

# p16
add(id="1c3adb35", qtype="choice",
    question="함수 [[f(x) = x + 2]] ([[x >= 0]]), [[f(x) = a x + b]] ([[x < 0]])의 역함수가 존재하기 위한 실수 [[a]], [[b]]의 조건은?",
    choices=["[[a > 0]], [[b > 0]]", "[[a > 0]], [[b = 2]]", "[[a > 0]], [[b = 1]]", "[[a < 0]], [[b < 0]]", "[[a < 0]], [[b = -2]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW,
    note="증가·연속 조건 a>0, b=2 → ②. 빠른정답 5와 불일치.")

# p18
add(id="407f9f18", qtype="short",
    question="실수 전체의 집합에서 정의된 함수 [[f(x) = x - abs(k x + 1) - 1]]이 [[a < k < b]]인 범위에서 역함수가 존재할 때, [[a + b]]의 값을 구하시오. (단, [[k > 0]])",
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.85,
    note="기울기 1+k>0, 1−k>0 → 0<k<1 → a+b=1. 빠른정답 4와 불일치.")

# p19
add(id="b5423bff", qtype="short",
    question=("집합 [[S]] = { [[n]] | [[1 <= n <= 100]], [[n]]은 7의 배수 }의 공집합이 아닌 부분집합 [[X]]와 집합 [[Y = set(0, 1, 2, 3, 4, 5)]]에 대하여 "
              "함수 [[f]]: [[X]]→[[Y]]를 [[f(n)]]은 ‘[[n]]을 6으로 나눈 나머지’로 정의하자. 함수 [[f(n)]]의 역함수가 존재하도록 하는 집합 [[X]]의 개수를 구하시오."),
    choices=None, derived_answer="144", figure=None, difficulty_est=3, confidence=0.85,
    note="7의 배수 14개의 6으로 나눈 나머지 분포 2,3,3,2,2,2 → 곱 144. 빠른정답 2와 불일치.")

# p20
add(id="21bd87a5", qtype="short",
    question=("집합 [[S]] = { [[n]] | [[1 <= n <= 100]], [[n]]은 8의 배수 }의 공집합이 아닌 부분집합 [[X]]와 집합 [[Y = set(0, 1, 2, 3, 4)]]에 대하여 "
              "함수 [[f]]: [[X]]→[[Y]]를 [[f(n)]]은 ‘[[n]]을 5로 나눈 나머지’로 정의하자. 함수 [[f(n)]]의 역함수가 존재하도록 하는 집합 [[X]]의 개수를 구하시오."),
    choices=None, derived_answer="72", figure=None, difficulty_est=3, confidence=0.85,
    note="8의 배수 12개의 5로 나눈 나머지 분포 2,3,2,3,2 → 곱 72. 빠른정답 2와 불일치.")

# p21
add(id="7dd3c195", qtype="choice",
    question=("두 집합 [[X = setb(x, x >= -2)]], [[Y = setb(y, y >= 8)]]에 대하여 [[X]]에서 [[Y]]로의 함수 [[f(x) = 2 abs(x + 2) + abs(x - 6)]]의 역함수가\n"
              "[[inv(f)]]([[x]]) = [[x + a]] ([[8 <= x < b]]), [[inv(f)]]([[x]]) = [[c x + d]] ([[x >= b]])일 때, [[a + b + c + d]]의 값은? (단, [[a]], [[b]], [[c]], [[d]]는 상수이다.)"),
    choices=["[[frac(19,3)]]", "[[frac(20,3)]]", "7", "[[frac(22,3)]]", "8"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PW + " / " + INV,
    note="f = x+10 (−2≤x<6), 3x−2 (x≥6) → a=−10, b=16, c=1/3, d=2/3 → 합 7 → ③. 빠른정답 1과 불일치.")

# p26
add(id="07b3c854", qtype="choice",
    question=("실수 전체의 집합에서 정의된 함수 [[f]]에 대하여 [[f(3x + 2) = 6x + 5]]이고 함수 [[f(x)]]의 역함수가 [[inv(f)]]([[x]]) = [[a x + b]]이다. "
              "이때 상수 [[a]], [[b]]에 대하여 [[4a b]]의 값은?"),
    choices=["[[-4]]", "[[-1]]", "1", "2", "4"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=INV,
    note="f(t)=2t+1 → f⁻¹(x)=x/2−1/2 → 4ab=−1 → ②. 빠른정답 4와 불일치.")

# p31
add(id="903d7817", qtype="choice",
    question=("실수 전체의 집합에서 정의되고 역함수를 갖는 두 함수 [[f(x)]], [[g(x)]]가 모든 실수 [[x]]에 대하여 [[g(f(x)) = x - 2]]를 만족시킨다. "
              "좌표평면에서 함수 [[y = f(x)]]의 그래프는 직선 [[y = k x]] ([[k > 1]])과 서로 다른 두 점 A, B에서만 만나고, 두 점 A, B는 원 [[pow(x - 13, 2) + pow(y - 13, 2) = 26]] 위에 있다. "
              "[[seg(AB) = 2 sqrt(13)]]일 때, [[x]]에 대한 방정식 [[g(x) = frac(1, k) x - 2]]의 모든 실근은 [[alpha]], [[beta]] ([[alpha < beta]])이다.\n"
              "[[beta - alpha]]의 값은? (단, [[k]]는 상수이다.)"),
    choices=["5", "[[frac(11,2)]]", "6", "[[frac(13,2)]]", "7"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2026년 3월 고2 21번/4점]. g(x)=f⁻¹(x)−2 → 근은 k·(A,B의 x좌표); 현의 길이 조건으로 k=3/2 → β−α=6 → ③ = 빠른정답 ✓.")

# p32
add(id="936bd6c0", qtype="short",
    question=("세 집합 [[X = set(1, 2, 3)]], [[Y = set(3, 4, 5)]], [[Z = set(2, 4, 6)]]에 대하여 두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[Z]]가 일대일대응이고, "
              "[[f(1) = 4]], [[g(3) = 2]], ([[comp(g, f)]])(3) = 4일 때,\n([[comp(inv(f), inv(g))]])(6)의 값을 구하시오."),
    choices=None, derived_answer="1", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=COMPA,
    note="f(3)=5, g(5)=4, g(4)=6 → f⁻¹(g⁻¹(6))=f⁻¹(4)=1. 빠른정답 25와 불일치.")

# p34
add(id="ee10c781", qtype="choice",
    question=("집합 [[X = set(1, 2, 3, 4)]]에 대하여 [[X]]에서 [[X]]로의 함수 [[f]]가\n"
              "[[f(x) = pow(x,2)]] ([[x]] = 1, 2), [[f(x) = x + a]] ([[x]] = 3, 4) ([[a]]는 상수)\n"
              "이고, 함수 [[f]]의 역함수 [[g]]가 존재한다.\n"
              "[[pow(g,1)]]([[x]]) = [[g(x)]], [[pow(g, n + 1)]]([[x]]) = [[g]]([[pow(g,n)]]([[x]])) ([[n]] = 1, 2, 3, ⋯)\n"
              "라 할 때, [[a]] + [[pow(g,10)]](2) + [[pow(g,11)]](2)의 값은?"),
    choices=["4", "5", "6", "7", "8"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PW + " / 거듭 합성 gⁿ(x) 적용 표기(텍스트 혼합)",
    note="출처 [2015년 11월 고2 문과 19번/4점]. a=−1, g: 2→3→4→2 주기 3 → g¹⁰(2)=3, g¹¹(2)=4 → −1+3+4=6 → ③ = 빠른정답 ✓.")

# p37
add(id="10d2d23b", qtype="choice",
    question="그림은 두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[X]]를 나타낸 것이다.\n([[comp(g, f)]])(3) + [[inv((comp(g, f)))]](9)의 값은?",
    choices=["6", "9", "12", "15", "18"], derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={3,6,9}, Y={1,4,7}; f: 3→1, 6→7, 9→4; g: 1→6, 4→3, 7→9"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 대응 그림 / " + COMPA,
    note="출처 [2022년 11월 고1 9번/3점]. (g∘f)(3)=g(1)=6, (g∘f)⁻¹(9)=6 → 12 → ③ = 빠른정답 ✓.")

# p39
add(id="28f9c1d2", qtype="short",
    question=("함수 [[f]]에 대하여\n[[pow(f,2)]]([[x]]) = [[f(f(x))]], [[pow(f,3)]]([[x]]) = [[f(f(f(x)))]]로 정의하자.\n"
              "집합 [[X = set(1, 2, 3, 4)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 두 조건 [[f(2) = 4]], [[f(4) = 3]], [[pow(f,4) = I]] ([[I]]는 항등함수)를 만족한다. "
              "함수 [[f]]의 역함수를 [[g]]라 할 때,\n[[pow(g,20)]](1) + [[pow(g,23)]](2) + [[pow(g,26)]](3)의 값을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="거듭 합성 fⁿ(x) 적용 표기(텍스트 혼합)",
    note="f⁴=I이므로 f: 2→4→3→1→2 (4-순환) → g²⁰(1)=1, g²³(2)=4, g²⁶(3)=2 → 7. 빠른정답 2와 불일치.")

# p40
add(id="ad6865a0", qtype="choice",
    question=("집합 [[X]] = { [[x]] | [[x]]는 실수 }에 대하여 [[X]]에서 [[X]]로의 함수 [[f]]가 다음 조건을 모두 만족시킨다.\n"
              "(가) [[f]]의 역함수가 존재한다.\n"
              "(나) [[in(sub(x,1), X)]], [[in(sub(x,2), X)]]일 때, [[sub(x,1) > sub(x,2)]]이면 [[f(sub(x,1)) > f(sub(x,2))]]이다.\n"
              "다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n(단, [[a < b]])\n<보기>\n"
              "ㄱ. ([[comp(f, f)]])([[f(a)]]) > ([[comp(f, f)]])([[f(b)]])\n"
              "ㄴ. [[inv(f)]]([[a]]) > [[inv(f)]]([[b]])\n"
              "ㄷ. [[inv((comp(f, f)))]]([[a]]) < [[inv((comp(f, f)))]]([[b]])"),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.8,
    needs_review=COMPA + " / " + INV,
    note="f 증가 → f³, f⁻¹, (f∘f)⁻¹ 모두 증가 → ㄷ만 참 → ③ = 빠른정답 ✓.")

# p51
add(id="589c54e0", qtype="choice",
    question=("세 집합 [[X = set(5, 6, 7, 8)]], [[Y = set(6, 7, 8, 9)]],\n[[Z = set(7, 8, 9)]]에 대하여\n두 함수 [[f]]: [[X]]→[[Y]], [[g]]: [[Y]]→[[Z]]가 아래 조건을 모두 만족시킨다.\n"
              "(가) 함수 [[f]]는 일대일대응이다.\n"
              "(나) [[in(x, (inter(X, Y)))]]이면 [[g(x) - f(x) = 1]]이다.\n"
              "다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. 함수 [[comp(g, f)]]의 치역은 [[Z]]이다.\nㄴ. [[f(5) = 6]]\nㄷ. [[f(7) < g(6) <= f(5) - 1]]이면 [[f(8) + g(6) = 16]]이다."),
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2021년 3월 고2 20번 변형]. f(6),f(7),f(8)∈{6,7,8}, f(5)=9 → ㄱ✓ ㄴ✗ ㄷ f(6)=7,f(7)=6,f(8)=8 → 16 ✓ → ④ = 빠른정답 ✓.")

# p52
add(id="4626cafc", qtype="short",
    question="다음 그림과 같은 함수 [[f]]: [[X]]→[[Y]]에서\n([[comp(inv(f), f)]])(7)의 값을 구하시오.",
    choices=None, derived_answer="7",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={6,7,8}, Y={1,2,3}; f: 6→3, 7→1, 8→2"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 함수 대응 그림 / " + COMPA,
    note="f⁻¹∘f 는 X 위의 항등함수 → 7 = 빠른정답 ✓.")

# p54
add(id="19dc88f3", qtype="short",
    question="다음 그림과 같은 함수 [[f]]: [[X]]→[[Y]]에 대하여\n([[comp(f, inv(f))]])(3)을 구하시오.",
    choices=None, derived_answer="3",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={0,1,2,3}, Y={1,2,3,4}; f: 0→3, 1→1, 2→2, 3→4"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 함수 대응 그림 / " + COMPA,
    note="f∘f⁻¹ 는 Y 위의 항등함수 → 3. 빠른정답 4와 불일치.")

# p57
add(id="46c17db8", qtype="short",
    question="두 함수 [[f(x) = frac(1,3) x + 2]], [[g(x) = 2x - 6]]에 대하여\n[[inv((comp(inv(f), g)))]](6)의 값을 구하시오.",
    choices=None, derived_answer="5", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=INV,
    note="(f⁻¹∘g)⁻¹=g⁻¹∘f → g⁻¹(f(6))=g⁻¹(4)=5 = 빠른정답 ✓.")

# p58
add(id="e347572f", qtype="short",
    question=("두 집합 [[X = set(1, 2, 3, 4)]], [[Y = set(2, 4, 6, 8)]]에 대하여 함수 [[f]]: [[X]]→[[Y]]가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[f]]는 일대일대응이다.\n(나) [[f(1) != 2]]\n"
              "(다) 등식 [[frac(1,2) f(a)]] = ([[comp(f, inv(f))]])([[a]])를 만족시키는 [[a]]의 개수는 2이다.\n"
              "[[f(2)]] · [[inv(f)]](2)의 값을 구하시오."),
    choices=None, derived_answer="12", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=COMPA + " / " + INV,
    note="출처 [2018년 10월 고3 문과 28번/4점]. a∈X∩Y={2,4}에서 f(a)=2a → f(2)=4, f(4)=8, f(1)=6, f(3)=2 → 4·3=12. 빠른정답 7과 불일치.")

# p60
add(id="dba86109", qtype="short",
    question=("두 집합 [[X = set(1, 2, 3, 4)]], [[Y = set(1, 2, 3, 4)]]에 대하여 함수 [[f]]: [[X]]→[[Y]]가 다음 조건을 만족시킨다.\n"
              "(가) 함수 [[f]]는 일대일대응이다.\n(나) [[f(3) != 3]]\n"
              "(다) 등식 [[frac(1,2) f(a)]] = ([[comp(f, inv(f))]])([[a]])를 만족시키는 [[a]]의 개수는 2이다.\n"
              "[[f(4)]] · [[inv(f)]](4)의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=COMPA + " / " + INV,
    note="출처 [2018년 10월 고3 문과 28번 변형]. f(1)=2, f(2)=4, f(3)=1, f(4)=3 → 3·2=6. 빠른정답 5와 불일치.")

# p61
add(id="93c7a12f", qtype="short",
    question="함수 [[f(x) = 3x]] ([[x >= 2]]), [[f(x) = -pow(x,2) + 5x]] ([[x < 2]])에 대하여\n([[comp(f, f)]])(3) + [[inv(f)]]([[-6]])의 값을 구하시오.",
    choices=None, derived_answer="26", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW + " / " + COMPA,
    note="f(f(3))=27, f(−1)=−6 → f⁻¹(−6)=−1 → 26 = 빠른정답 ✓.")

# p62
add(id="0237664f", qtype="choice",
    question=("실수 전체의 집합에서 정의된\n함수 [[f(x) = x + k]] ([[x < 1]]), [[f(x) = 2x + 3]] ([[x >= 1]])의 역함수가 존재할 때,\n"
              "([[comp(inv(f), inv(f))]])(6)의 값은? (단, [[k]]는 상수이다.)"),
    choices=["[[-frac(1,2)]]", "[[-1]]", "[[-frac(3,2)]]", "[[-2]]", "[[-frac(5,2)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW + " / " + COMPA,
    note="k=4, f⁻¹(6)=3/2, f⁻¹(3/2)=−5/2 → ⑤. 빠른정답 28과 불일치.")

# p64
add(id="293d737a", qtype="short",
    question="함수 [[f(x) = x + 5]] ([[x >= 1]]), [[f(x) = 2x + 4]] ([[x < 1]])에 대하여\n[[f(-1)]] + [[inv(f)]](7)의 값을 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=1, confidence=0.85,
    needs_review=PW + " / " + INV,
    note="f(−1)=2, f⁻¹(7)=2 → 4. 빠른정답 26과 불일치.")

# p65
add(id="b8cb66cd", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6, 7, 8, 9)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족한다.\n"
              "(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n"
              "(나) [[1 <= x <= 4]]일 때,\n([[comp(f, f)]])([[x]]) = [[f(x) - 2x]]이다.\n"
              "[[f(2) + f(3) + f(4) + f(5)]]의 값을 구하시오."),
    choices=None, derived_answer="29", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=COMPA,
    note="전수 확인: f=(6,7,8,9,5,4,3,2,1) 유일 → 7+8+9+5=29. 빠른정답 5와 불일치.")

# p66
add(id="c5426f2a", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족한다.\n"
              "(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n"
              "(나) [[1 <= x <= 3]]일 때,\n([[comp(f, f)]])([[x]]) = [[2f(x) - 3x - 2]]이다.\n"
              "[[f(2) + f(3) + f(4)]]의 값을 구하시오."),
    choices=None, derived_answer="14", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=COMPA,
    note="전수 확인: f=(4,5,6,3,2,1) 유일 → 5+6+3=14. 빠른정답 4와 불일치.")

# p67
add(id="ec74440a", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5, 6, 7)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족한다.\n"
              "(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n"
              "(나) [[1 <= x <= 3]]일 때,\n([[comp(f, f)]])([[x]]) = [[f(x) - 2x]]이다.\n"
              "[[f(2) + f(3) + f(4) + f(5)]]의 값을 구하시오."),
    choices=None, derived_answer="20", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=COMPA,
    note="전수 확인: f=(5,6,7,4,3,2,1) 유일 → 6+7+4+3=20 = 빠른정답 ✓.")

# p69
add(id="3578dadc", qtype="short",
    question=("함수 [[f(x) = pow(x,2) - 6x + 10]] ([[x < 2]]), [[f(x) = k(x - 2) + 2]] ([[x >= 2]])에 대하여\n역함수 [[inv(f)]]([[x]])가 존재한다.\n"
              "{ [[x]] | [[f(x)]] = [[inv(f)]]([[x]]) } = [[set(2, a, a + 4)]]일 때,\n[[18(pow(k,2) + pow(a,2))]]의 값을 구하시오. (단, [[k]]는 상수이다.)"),
    choices=None, derived_answer="20", figure=None, difficulty_est=4, confidence=0.75,
    needs_review=PW + " / " + INV,
    note="f 감소함수(k<0); f(a)=a+4, f(a+4)=a → a=1, k=−1/3 → 18(1/9+1)=20. 빠른정답 14와 불일치.")

# p70
add(id="3e574db4", qtype="short",
    question=("집합 [[X = set(1, 2, 3, 4, 5)]]에 대하여\n함수 [[f]]: [[X]]→[[X]]가 다음 조건을 만족시킨다.\n"
              "(가) 집합 [[X]]의 임의의 두 원소 [[sub(x,1)]], [[sub(x,2)]]에 대하여 [[sub(x,1) != sub(x,2)]]이면 [[f(sub(x,1)) != f(sub(x,2))]]이다.\n"
              "(나) [[1 <= x <= 2]]일 때,\n([[comp(f, f)]])([[x]]) = [[f(x) - 2x]]이다.\n"
              "[[f(2) + f(3) + f(4)]]의 값을 구하시오."),
    choices=None, derived_answer="10", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=COMPA,
    note="출처 [2017년 3월 고2 이과 28번 변형]. 전수 확인: f=(4,5,3,2,1) 유일 → 5+3+2=10. 빠른정답 3과 불일치.")

# p71
add(id="bb68c861", qtype="short",
    question=("두 함수 [[f(x) = x + 2]], [[g(x) = -2x + 3]]에 대하여\n([[comp(comp(inv(f), inv((comp(g, inv(f))))), f)]])([[x]]) = [[a x + b]]일 때, [[b - a]]의 값을 구하시오. (단, [[a]], [[b]]는 상수이다.)"),
    choices=None, derived_answer="1", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=COMPA,
    note="f⁻¹∘f∘g⁻¹∘f = g⁻¹∘f → (1−x)/2 → a=−1/2, b=1/2 → 1 = 빠른정답 ✓.")

# p72
add(id="05731868", qtype="short",
    question="역함수가 존재하는 두 함수 [[f(x)]], [[g(x) = -3x - 6]]에 대하여 ([[comp(f, inv((comp(g, f))))]])(3)의 값을 구하시오.",
    choices=None, derived_answer="-3", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=COMPA,
    note="f∘f⁻¹∘g⁻¹ = g⁻¹ → g⁻¹(3)=−3 = 빠른정답 ✓.")

# p77
add(id="2576aa0b", qtype="short",
    question=("집합 [[X = set(1, 3, 7)]]에 대하여 [[X]]에서 [[X]]로의 함수 [[f]], [[g]]의 역함수가 모두 존재하고 [[f(7) = 1]], [[g(3) = 1]], ([[comp(g, inv(f))]])(1) = 3,\n"
              "[[inv((comp(g, inv(f))))]](1) = 7일 때, [[f(1)]] + [[inv(g)]](1)의 값을 구하시오."),
    choices=None, derived_answer="6", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=COMPA + " / " + INV,
    note="g(7)=3, f(3)=7 → f(1)=3; g(1)=7 → g⁻¹(1)=3 → 6. 빠른정답 4와 불일치.")

# p78
add(id="0afe7e37", qtype="choice",
    question=("실수 전체의 집합에서 정의된 두 함수 [[f]], [[g]]가\n[[f(x) = 4x + 3]] ([[x >= 1]]), [[f(x) = 3x + 4]] ([[x < 1]]), [[g(x) = -2x + 3]]일 때,\n"
              "([[comp(f, inv((comp(inv(f), g))))]])(2)의 값은?"),
    choices=["[[-10]]", "[[-8]]", "[[-6]]", "[[-4]]", "[[-2]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    needs_review=PW + " / " + COMPA,
    note="f∘g⁻¹∘f(2): f(2)=11, g⁻¹(11)=−4, f(−4)=−8 → ②. 빠른정답 3과 불일치.")

# p80
add(id="b7153db3", qtype="choice",
    question=("세 집합 [[X = set(1, 2, 3)]], [[Y = set(5, 6, 7)]], [[Z = set(3, 4, 5)]]에 대하여 다음 그림과 같이 일대일대응인 두 함수 [[f]], [[g]]가 [[f(1) = 6]], [[g(5) = 4]]를 만족시킨다.\n"
              "{ [[x]] | ([[comp(g, f)]])([[x]]) = 4, [[in(x, X)]] } = { [[x]] | ([[comp(inv(f), inv(g))]])([[x]]) = 2, [[in(x, Z)]] } = [[set(3)]]일 때, "
              "([[comp(comp(g, inv((comp(f, g)))), g)]])([[k]]) = 3이다. [[f(2) + g(7) + k]]의 값은?"),
    choices=["13", "14", "15", "16", "17"], derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "대응 그림: X={1,2,3} →f→ Y={5,6,7} →g→ Z={3,4,5}; 화살표 1→6, 5→4만 표시"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 함수 대응 그림 / " + COMPA,
    note="f(3)=5, f(2)=7, g(7)=3, g(6)=5; f⁻¹(g(k))=3 → g(k)=5 → k=6 → 7+3+6=16 → ④. 빠른정답 6과 불일치.")

# p81
add(id="23babf00", qtype="choice",
    question=("함수 [[f(x) = pow(x,2) - 2x]] ([[x >= 1]], [[y >= -1]])의 그래프와 그 역함수 [[y]] = [[inv(f)]]([[x]])의 그래프가 만나는 점의 좌표를 "
              "[[point(a, b)]]라고 할 때, [[a + b]]의 값은?"),
    choices=["2", "4", "6", "8", "10"], derived_answer="③", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=INV,
    note="증가함수 → y=x와의 교점 x²−2x=x, x≥1 → (3,3) → 6 → ③ = 빠른정답 ✓.")

# p84
add(id="b6a31d6b", qtype="choice",
    question="일차함수 [[f(x) = a x + b]]의 그래프가 점 [[point(-3, 8)]]을 지나고, 그 역함수의 그래프가 점 [[point(11, 6)]]을 지날 때, 상수 [[a]], [[b]]에 대하여 [[a b]]의 값은?",
    choices=["[[-3]]", "[[-2]]", "1", "2", "3"], derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="f(−3)=8, f(6)=11 → a=1/3, b=9 → ab=3 → ⑤. 빠른정답 3과 불일치.")

# p91
add(id="dc57d4d2", qtype="short",
    question=("집합 [[X = set(1, 3, 5, 7, 9)]]에 대하여 함수 [[f]]: [[X]]→[[X]]가 있다. 다음 그림은 함수 [[y = f(x)]]의 그래프의 일부를 나타낸 것이다. "
              "함수 [[f(x)]]의 역함수 [[inv(f)]]([[x]])가 존재할 때, [[inv(f)]](5) + [[inv(f)]](9)의 값을 구하시오."),
    choices=None, derived_answer="6",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(격자 1,3,5,7,9): 그래프 위의 점 (3,1), (7,7), (9,3) 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 점 그래프 / " + INV,
    note="남은 f(1), f(5)∈{5,9} → f⁻¹(5)+f⁻¹(9)=1+5=6 = 빠른정답 ✓.")

# p92
add(id="d6c7a6af", qtype="short",
    question="다음 그림은 두 함수 [[y = f(x)]]와 [[y = x]]의 그래프이다.\n이때 [[inv((comp(f, f)))]]([[b]])의 값을 구하시오.\n(단, 모든 점선은 [[x]]축 또는 [[y]]축에 평행하다.)",
    choices=None, derived_answer="d",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 증가하는 곡선 y=f(x)와 직선 y=x, x축 위 점 a,b,c,d,e; 점선으로 f(b)=a, f(c)=b, f(d)=c, f(e)=d 임을 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 함수 그래프 / " + COMPA,
    note="f(f(d))=f(c)=b → (f∘f)⁻¹(b)=d. 빠른정답 5와 불일치(문자 답).")

# ================= 유리함수의 그래프 =================
# p4
add(id="3d3cfa68", qtype="choice",
    question=("두 다항식 [[A]], [[B]]에 대하여 [[A]]△[[B]]를\n[[A]]△[[B]] = [[frac(A, A + B)]] 로 정의할 때,\n"
              "{[[(2x - 4)]]△[[(pow(x,2) - 4)]]} + {[[(pow(x,2) + 2x)]]△[[2x]]}를 간단히 하면?"),
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "1", "[[x]]", "[[frac(1, pow(x,2))]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.8,
    needs_review="문법 밖 연산 기호 △(텍스트 혼합)",
    note="2/(x+4) + (x+2)/(x+4) = 1 → ③. 빠른정답 1과 불일치.")

# p6
add(id="15f388b9", qtype="short",
    question=("표는 전기회로에서 크기가 [[sub(R,1)]](Ω), [[sub(R,2)]](Ω)인 두 저항을 연결하였을 때, 연결 방법에 따른 전체 저항의 크기를 구하는 방법을 나타낸 것이다.\n"
              "그림과 같이 저항의 크기가 각각 [[R]](Ω), [[R + 1]](Ω), [[5R]](Ω)인 세 저항을 연결한 전기회로가 있다.\n"
              "이 전기회로의 전체 저항의 크기가 [[frac(a pow(R,2) + b R, 2R + 1)]](Ω)일 때, 상수 [[a]], [[b]]의 합 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="17",
    figure=[{"fn": "table", "args": {"head": ["연결 방법", "직렬연결", "병렬연결"],
                                      "rows": [["회로도", "(그림) R₁, R₂ 직렬 연결", "(그림) R₁, R₂ 병렬 연결"],
                                               ["전체 저항", "[[R = sub(R,1) + sub(R,2)]]", "[[frac(1, R) = frac(1, sub(R,1)) + frac(1, sub(R,2))]]"]]}},
            {"fn": "unsupported", "args": {"raw": "전기회로도: 전원에 저항 R과 R+1을 병렬로 연결한 부분과 저항 5R을 직렬로 연결"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 회로도(정보 포함)",
    note="출처 [2007년 9월 고1 29번]. 병렬 R(R+1)/(2R+1) + 5R = (11R²+6R)/(2R+1) → a+b=17. 빠른정답 5와 불일치.")

# p12
add(id="1b69e3a8", qtype="short",
    question="다음 □ 안에 알맞은 수 또는 식을 써넣으시오.\n[[frac(4x - 7, x - 3)]] = 4 + (□)/([[x - 3]])",
    choices=None, derived_answer="5", figure=None, difficulty_est=1, confidence=0.85,
    note="(4x−7)/(x−3) = 4 + 5/(x−3) → 5 = 빠른정답 ✓. 빈칸 상자는 텍스트 □로 처리.")

# p28
add(id="1e4271df", qtype="short",
    question="[[ratio(x, y) = ratio(1, 3)]]일 때, [[frac(pow(x,2) + pow(y,2), pow(x,2) + 2x y - pow(y,2))]] 의 값을 구하시오.",
    choices=None, derived_answer="-5", figure=None, difficulty_est=1, confidence=0.9,
    note="x=k, y=3k → 10k²/(−2k²) = −5. 빠른정답 4와 불일치.")

# p47
add(id="900ec97c", qtype="choice",
    question="함수 [[y = frac(2x - 3, x - 2)]]의 정의역이\n{ [[x]] | [[1 <= x < 2]] 또는 [[2 < x <= 4]] }일 때, 치역은?",
    choices=["[[setb(y, 1 <= y <= frac(5,2))]]", "{ [[y]] | [[y <= 1]] 또는 [[y >= frac(5,2)]] }", "[[setb(y, 1 < y < frac(5,2))]]",
             "{ [[y]] | [[y < 1]] 또는 [[y > frac(5,2)]] }", "{ [[y]] | [[y <= 1]] 또는 [[y >= 3]] }"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="y=2+1/(x−2): 1≤x<2 → y≤1, 2<x≤4 → y≥5/2 → ② = 빠른정답 ✓.")

# p53
add(id="b1497a8a", qtype="short",
    question=("좌표평면 위에 함수 [[f(x) = frac(4, x)]] ([[x > 0]]), [[f(x) = frac(9, x)]] ([[x < 0]])의 그래프와 직선 [[y = -x]]가 있다. "
              "함수 [[y = f(x)]]의 그래프 위의 점 P를 지나고 [[x]]축에 수직인 직선이 직선 [[y = -x]]와 만나는 점을 Q, 점 Q를 지나고 [[y]]축에 수직인 직선이 [[y = f(x)]]와 만나는 점을 R라 할 때, "
              "선분 PQ와 선분 QR의 길이의 곱 [[seg(PQ) × seg(QR)]]의 최솟값을 구하시오."),
    choices=None, derived_answer="25", figure=None, difficulty_est=4, confidence=0.8,
    needs_review=PW,
    note="P(t,4/t), Q(t,−t), R(−9/t,−t) → (t+4/t)(t+9/t) = t²+36/t²+13 ≥ 25. 빠른정답 5와 불일치.")

# p61
add(id="6288eb16", qtype="short",
    question=("유리함수 [[y = frac(9, x - 4) + 3]] ([[x > 4]])의\n그래프 위의 한 점 P와 두 점 [[A(6, 0)]], [[B(0, 4)]]에 대하여\n"
              "[[pow(seg(PA), 2) + pow(seg(PB), 2)]]의 최솟값을 구하시오."),
    choices=None, derived_answer="90", figure=None, difficulty_est=4, confidence=0.85,
    note="u=x−4>0: 2(u²+81/u²)+4(u+9/u)+30 ≥ 36+24+30 = 90 (u=3) = 빠른정답 ✓.")

# p83
add(id="7ff455e6", qtype="short",
    question=("곡선 [[y = frac(2, x)]]와 직선 [[y = -x + k]]가 제1사분면에서 만나는 서로 다른 두 점을 각각 A, B라 하자.\n"
              "[[angle(ABC) = deg(90)]]인 점 C가 곡선 [[y = frac(2, x)]] 위에 있다.\n"
              "[[seg(AC) = 2 sqrt(5)]]가 되도록 하는 상수 [[k]]에 대하여 [[pow(k,2)]]의 값을 구하시오. (단, [[k > 2 sqrt(2)]])"),
    choices=None, derived_answer="9", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2017년 9월 고2 이과 27번/4점]. B(b,2/b) → C(−2/b,−b), A(2/b,b); AC²=16/b²+4b²=20 → b=1,2 → k=b+2/b=3 → k²=9 = 빠른정답 ✓.")

# p87
add(id="19ed18b1", qtype="short",
    question=("함수 [[f(x) = frac(x, 1 - x)]]에 대하여 [[pow(f,1) = f]], [[pow(f,2) = comp(f, pow(f,1))]],\n"
              "[[pow(f,3) = comp(f, pow(f,2))]], ⋯, [[pow(f,n) = comp(f, pow(f, n - 1))]] ([[n]] = 2, 3, ⋯)로\n"
              "정의한다. [[pow(f,100)]]([[x]]) = [[frac(a x + b, c x + d)]]일 때, 상수 [[a]], [[b]], [[c]], [[d]]에\n"
              "대하여 [[a + b - c + d]]의 값을 구하시오.\n(단, [[a]], [[b]], [[c]], [[d]]는 서로소이고, [[a > 0]]이다.)"),
    choices=None, derived_answer="102", figure=None, difficulty_est=3, confidence=0.85,
    needs_review="거듭 합성 fⁿ(x) 적용 표기(텍스트 혼합)",
    note="fⁿ(x)=x/(1−nx) → f¹⁰⁰=x/(−100x+1) → a=1,b=0,c=−100,d=1 → 102 = 빠른정답 ✓.")

# p88
add(id="a6fa80da", qtype="choice",
    question=("유리함수 [[f(x) = frac(x, 1 + x)]]에 대하여\n"
              "[[pow(f,1)]]([[x]]) = [[f(x)]], [[pow(f, n + 1)]]([[x]]) = ([[comp(f, pow(f,n))]])([[x]]) ([[n]]은 자연수)\n"
              "로 정의한다. [[pow(f,15)]]([[x]]) = [[frac(a x + b, c x + 1)]]일 때,\n실수 [[a]], [[b]], [[c]]의 합 [[a + b + c]]의 값은?"),
    choices=["12", "13", "14", "15", "16"], derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    needs_review="거듭 합성 fⁿ(x) 적용 표기 / " + COMPA,
    note="fⁿ(x)=x/(1+nx) → f¹⁵=x/(15x+1) → 1+0+15=16 → ⑤ = 빠른정답 ✓.")

# p89
add(id="f246cab3", qtype="short",
    question=("분모, 분자가 일차식인 [[f(x)]]에 대하여 [[x <= 0]]에서 정의된 함수 [[y = f(x)]]의 그래프가 다음 그림과 같다.\n"
              "[[pow(f,1) = f]], [[pow(f,n) = comp(f, pow(f, n - 1))]] ([[n]] = 2, 3, 4, ⋯)로 정의할 때, [[pow(f,6)]]([[-1]])의 값을 구하시오."),
    choices=None, derived_answer="-frac(1,7)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 점근선 x=1, y=−1(점선)인 유리함수 그래프, 원점을 지남; x≤0 부분은 실선, 나머지는 점선"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 유리함수 그래프(점근선 정보) / 거듭 합성 fⁿ(x) 적용 표기",
    note="f(x)=−1−1/(x−1)=x/(1−x) → fⁿ(x)=x/(1−nx) → f⁶(−1)=−1/7 = 빠른정답 ✓.")

# ================= 함수의 합성 =================
# p2
add(id="0527fa64", qtype="short",
    question=("두 함수\n[[f(x) = frac(1,3) x + 2]], [[g(x) = pow(x,2) - 13]] ([[x >= 0]]), [[g(x) = -3x + 7]] ([[x < 0]])\n"
              "에 대하여 ([[comp(g, f)]])([[-12]]) + ([[comp(f, g)]])(5)의 값을\n구하시오."),
    choices=None, derived_answer="19", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=PW + " / " + COMPA,
    note="g(f(−12))=g(−2)=13, f(g(5))=f(12)=6 → 19 = 빠른정답 ✓.")

# p5
add(id="513ef81d", qtype="choice",
    question=("자연수 [[n]]에 대하여 두 함수 [[f(n)]], [[g(n)]]이\n[[f(n)]] = ([[n]]보다 작은 소수의 개수),\n[[g(n)]] = ([[sqrt(n)]]보다 작은 자연수의 개수)\n"
              "일 때, ([[comp(comp(f, f), g)]])(144)의 값은?"),
    choices=["2", "3", "4", "5", "6"], derived_answer="①", figure=None, difficulty_est=2, confidence=0.85,
    needs_review=COMPA,
    note="g(144)=11, f(11)=4, f(4)=2 → ①. 빠른정답 19와 불일치.")

# p8
add(id="dd13c390", qtype="short",
    question=("두 함수\n[[f(x) = pow(x,2) + 4a x + 20]] ([[x < 0]]), [[f(x) = x + 20]] ([[x >= 0]]), [[g(x) = x + 16]]\n"
              "에 대하여 합성함수 ([[comp(g, f)]])([[x]])의 치역이 [[setb(y, y >= 0)]]일\n때, 상수 [[a]]의 값을 구하시오."),
    choices=None, derived_answer="3", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PW + " / " + COMPA,
    note="f의 최솟값 −16 → x<0에서 최솟값 20−4a²=−16 (a>0) → a=3. 빠른정답 1과 불일치.")

# p9 (id 2개)
dup(["0d78c693", "2ae4c66e"], qtype="choice",
    question=("실수 전체의 집합에서 정의된 두 함수 [[f(x)]], [[g(x)]]가\n"
              "[[f(x) = 5]] ([[x > 5]]), [[f(x) = x]] ([[abs(x) <= 5]]), [[f(x) = -5]] ([[x < -5]]), [[g(x) = frac(2,5) pow(x,2) - 5]]\n"
              "일 때, 다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. ([[comp(f, g)]])(5) = 5\n"
              "ㄴ. ([[comp(g, f)]])([[-x]]) = ([[comp(g, f)]])([[x]])\n"
              "ㄷ. ([[comp(f, g)]])([[x]]) = ([[comp(g, f)]])([[x]])"),
    choices=["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review=PW + " / " + COMPA,
    note="ㄱ g(5)=5, f(5)=5 ✓; ㄴ f 홀함수·g 짝함수 ✓; ㄷ |x|≤5면 g(x)∈[−5,5]로 양변 g(x), |x|>5면 양변 5 ✓ → ⑤. 빠른정답 3과 불일치.")
