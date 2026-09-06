# -*- coding: utf-8 -*-
# batch07 (78문항: esc_opus_h3-3_1of1 33, esc_sonnet_h3-3_1of6 9, esc_sonnet_h3-3_2of6 23, esc_sonnet_h3-3_3of6 13) — v1.5 문법 재작업 (고3 기하)
# 핵심 교체: 윗줄 선분 PF′·A′B′·Q₁Q₂·F₁F₂ → seg(PF'), seg(A'B'), seg(Q1Q2), seg(F1F2) / ∠F′PF·∠A′OB′·∠N₁ON₂ → angle(F'PF), angle(A'OB'), angle(N1ON2)
#            벡터 OP₁→·F′Q→·OH′→·P₁Q₁→ → vec(OP1), vec(F'Q), vec(OH'), vec(P1Q1) / 길이의 곱 PF·PF′ → seg(PF) × seg(PF') / 3차원 점 좌표 → point3
#            프라임·첨자 점 이름이 문장 속에만 있는 것(점 F′, 선분 PF′, 삼각형 AF′F, 삼각형 OQ₁R₁ …)은 텍스트(F′, [[sub(Q,1)]])로 유지 → 통과
#            가변 첨자 벡터(OPₖ→, SₙTₙ→)는 v1.5 라벨로도 못 쓰므로 sub(vec(OP), k) / sub 텍스트 혼합 유지 → 통과
# 도형(쌍곡선·타원·입체도 등)은 unsupported(raw) 유지 — 도형만 남은 항목은 통과
# 여전히 보류: 한 이미지에 별개 문항 2개(id 1개) 2건(d2c737b5, 5cd2052d), 문항 결함 의심(조건 양립 불가) 1건(75364b1c)
ITEMS = []
def add(**kw): ITEMS.append(kw)

# ================= esc_opus_h3-3_1of1 =================
# 0. dacedef4 — 위치벡터 p63: |AP₁→|+…+|AP₄→| → vec(AP1)…; OPₖ→(가변 첨자)는 sub(vec(OP), k) 유지
add(id="dacedef4", qtype="short",
    question="삼각형 OAB의 변 AB 위의 점 [[sub(P,k)]] ([[k]]는 자연수)에 대하여 [[vec(OA) = vec(a)]], [[vec(OB) = vec(b)]], [[sub(vec(OP), k) = sub(vec(p), k)]]라 하자. [[seg(AB) = 27]]이고 [[sub(vec(p), k) = (1 - frac(1, pow(3,k))) vec(a) + frac(1, pow(3,k)) vec(b)]]일 때,\n[[abs(vec(AP1)) + abs(vec(AP2)) + abs(vec(AP3)) + abs(vec(AP4))]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 OAB: O에서 A로 벡터 a→, B로 벡터 b→, 변 AB 위의 점 P_k로 벡터 p_k→, AB=27 표시"}}],
    confidence=0.85,
    note="고정 첨자 벡터 AP₁→~AP₄→를 vec(AP1)~vec(AP4)로; 가변 첨자 OPₖ→=pₖ→는 sub(vec(OP), k)=sub(vec(p), k) 유지. 답 40/3 유지")

# 1. 87d2be36 — 삼수선 정리 p44: 본문에 프라임 라벨 없음(그림에만 A′·B′·C′) — 그대로 통과
add(id="87d2be36", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = 3]], [[seg(BC) = 4 sqrt(3)]] 인 직사각형 모양의 종이 ABCD가 있다. 선분 BC를 [[ratio(1, 3)]]으로 내분하는 점을 P라 할 때, 선분 DP를 접는 선으로 하여 종이를 접고 두 선분 PC와 AD의 교점을 E라 하자. 다시 선분 EP를 접는 선으로 하여 점 A의 평면 DEP 위로의 정사영이 선분 DP 위에 있도록 접자. 이때 두 평면 APE와 DEP가 이루는 각을 [[theta]]라 할 때, [[30 cos(theta)]]의 값을 구하시오. (단, 종이의 두께는 무시한다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "두 단계 그림: (위) 직사각형 ABCD를 DP로 접어 C가 옮겨진 모습(원래 위치 C′ 점선), 교점 E; (아래) EP로 다시 접어 A가 들린 모습(A′, B′ 점선, 수선 표시)"}}],
    confidence=0.8,
    note="본문은 v1.4 문법으로 이미 완결(프라임 라벨은 그림 설명에만) — 종이접기 입체도는 unsupported 유지. 답 10 유지(빠른정답 5와 불일치는 1차와 동일)")

# 2. c47a61b2 — 삼수선 정리 p45: 1번과 같은 구조 — 그대로 통과
add(id="c47a61b2", qtype="short",
    question="다음 그림과 같이 [[seg(AB) = 4]], [[seg(BC) = 6 sqrt(3)]] 인 직사각형 모양의 종이 ABCD가 있다. 선분 BC를 [[ratio(1, 2)]]로 내분하는 점을 P라 할 때, 선분 DP를 접는 선으로 하여 종이를 접고 두 선분 PC와 AD의 교점을 E라 하자. 다시 선분 EP를 접는 선으로 하여 점 A의 평면 DEP 위로의 정사영이 선분 DP 위에 있도록 접자. 이때 두 평면 APE와 DEP가 이루는 각을 [[theta]]라 할 때, [[30 cos(theta)]]의 값을 구하시오.\n(단, 종이의 두께는 무시한다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "두 단계 그림: (위) 직사각형 ABCD를 DP로 접어 C가 옮겨진 모습(원래 위치 C′ 점선), 교점 E; (아래) EP로 다시 접어 A가 들린 모습(A′, B′ 점선, 수선 표시)"}}],
    confidence=0.8,
    note="본문은 v1.4 문법으로 이미 완결(프라임 라벨은 그림 설명에만) — 종이접기 입체도는 unsupported 유지. 답 6 유지(빠른정답 5와 불일치는 1차와 동일)")

# 3. 7fd00511 — 직선의 방정식 p92: OP₁→·OP₂→·OP₃→ → vec(OP1)…, 공간 점 좌표 → point3
add(id="7fd00511", qtype="short",
    question="좌표공간에서 점 A[[point3(3, frac(1,2), 2)]]와 평면 [[z = 1]] 위의 세 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]이\n[[dot(vec(OA), vec(OP1)) = frac(11, 3)]],\n[[dot(vec(OA), vec(OP2)) = 1]],\n[[dot(vec(OA), vec(OP3)) = -frac(7, 4)]]\n을 만족시킨다. 점 [[point3(0, k, 0)]]을 지나고 방향벡터가 [[vcomp(1, -6, 0)]]인 직선을 [[l]]이라 하고, 직선 [[l]]에 의해 나누어지는 xy평면의 두 영역을 각각 [[alpha]], [[beta]]라 하자. 세 점 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]에서 xy평면에 내린 수선의 발이 모두 [[alpha]]에만 포함되거나 모두 [[beta]]에만 포함되도록 하는 양의 정수 [[k]]의 최솟값을 [[m]], 음의 정수 [[k]]의 최댓값을 [[M]]이라 할 때, [[m - M]]의 값을 구하시오. (단 O는 원점이다.)",
    choices=None, figure=None, confidence=0.85,
    note="[2018년 9월 고3 이과 29번/4점]. sub(vec(OP),1) 우회 → vec(OP1)·vec(OP2)·vec(OP3); 점 좌표 vcomp → point3. 답 12 유지")

# 4. d2063d54 — 직선의 방정식 p95: |OS₁→+OT₁→|+… → vec(OS1)…, 줄임표 cdots로 한 식에; SₙTₙ→(가변 첨자)는 sub 텍스트 혼합 유지
add(id="d2063d54", qtype="short",
    question="좌표평면에서 두 점 A[[point(2, 6)]], B[[point(8, 2)]]에 대하여 [[dot((vec(OP) - vec(OA)), (vec(OP) - vec(OB))) = 0]]을 만족시키는 점 P가 나타내는 도형과 직선 [[frac(x - 5, n + 1) = frac(y - 4, n + 5)]] ([[n]] = 1, 2, 3, ⋯)의 두 교점을 각각 [[sub(S,n)]], [[sub(T,n)]]이라 하자. 두 벡터 [[vec(AB)]]와 [[sub(S,n)]][[sub(T,n)]]→이 서로 수직이 되도록 하는 [[n]]의 값을 [[k]]라 할 때,\n[[abs(vec(OS1) + vec(OT1)) + abs(vec(OS2) + vec(OT2)) + cdots + abs(sub(vec(OS), k) + sub(vec(OT), k))]]\n의 값은 [[a sqrt(41)]] 이다. 자연수 [[a]]의 값을 구하시오. (단, O는 원점이다.)",
    choices=None, figure=None, confidence=0.85,
    note="고정 첨자 벡터 OS₁→·OT₁→·OS₂→·OT₂→를 vec 라벨로, 줄임표는 cdots로 한 식에; 가변 첨자 SₙTₙ→·OSₖ→는 라벨로 못 써 sub 텍스트 혼합/sub(vec(OS), k) 유지. 답 14 유지")

# 5. e653b63d — 직선의 방정식 p96: 4번과 같은 구조
add(id="e653b63d", qtype="short",
    question="좌표평면에서 두 점 A[[point(3, 8)]], B[[point(5, 2)]]에 대하여 [[dot((vec(OP) - vec(OA)), (vec(OP) - vec(OB))) = 0]]을 만족시키는 점 P가 나타내는 도형과 직선 [[frac(x - 4, n + 8) = frac(y - 5, n)]] ([[n]] = 1, 2, 3, ⋯)의 두 교점을 각각 [[sub(S,n)]], [[sub(T,n)]]이라 하자. 두 벡터 [[vec(AB)]]와 [[sub(S,n)]][[sub(T,n)]]→이 서로 수직이 되도록 하는 [[n]]의 값을 [[k]]라 할 때,\n[[abs(vec(OS1) + vec(OT1)) + abs(vec(OS2) + vec(OT2)) + cdots + abs(sub(vec(OS), k) + sub(vec(OT), k))]]\n의 값은 [[a sqrt(41)]] 이다. 자연수 [[a]]의 값을 구하시오. (단, O는 원점이다.)",
    choices=None, figure=None, confidence=0.85,
    note="고정 첨자 벡터를 vec(OS1) 등으로, 줄임표는 cdots로; 가변 첨자 SₙTₙ→·OSₖ→는 sub 텍스트 혼합/sub(vec(OS), k) 유지. 답 8 유지")

# 6. 8096a92b — 직선의 방정식 p97: 4번과 같은 구조
add(id="8096a92b", qtype="short",
    question="좌표평면에서 두 점 A[[point(2, 3)]], B[[point(6, 1)]]에 대하여 [[dot((vec(OP) - vec(OA)), (vec(OP) - vec(OB))) = 0]]을 만족시키는 점 P가 나타내는 도형과 직선 [[frac(x - 4, n + 1) = frac(y - 2, n + 7)]] ([[n]] = 1, 2, 3, ⋯)의 두 교점을 각각 [[sub(S,n)]], [[sub(T,n)]]이라 하자. 두 벡터 [[vec(AB)]]와 [[sub(S,n)]][[sub(T,n)]]→이 서로 수직이 되도록 하는 [[n]]의 값을 [[k]]라 할 때,\n[[abs(vec(OS1) + vec(OT1)) + abs(vec(OS2) + vec(OT2)) + cdots + abs(sub(vec(OS), k) + sub(vec(OT), k))]]\n의 값은 [[a sqrt(5)]] 이다. 자연수 [[a]]의 값을 구하시오. (단, O는 원점이다.)",
    choices=None, figure=None, confidence=0.85,
    note="고정 첨자 벡터를 vec(OS1) 등으로, 줄임표는 cdots로; 가변 첨자 SₙTₙ→·OSₖ→는 sub 텍스트 혼합/sub(vec(OS), k) 유지. 답 20 유지")

# 7. 485d041c — 쌍곡선 p75: PF·PF′(길이의 곱) → seg(PF) × seg(PF')
add(id="485d041c", qtype="short",
    question="다음 그림과 같이 두 초점이 F, F′인 쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), 81) = 1]]의 점근선에 중심이 C[[point(0, r)]] ([[r > 0]])인 원이 접하고, 선분 CF는 점근선과 수직으로 만나고 있다. 중심이 원점 O이고 점 C를 지나는 원이 쌍곡선과 제1사분면에서 만나는 점을 P라 할 때, [[seg(PF) × seg(PF')]]의 값을 구하시오.\n(단, 점 F의 [[x]]좌표는 양수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/9−y²/81=1과 점근선(점선), 초점 F′·F(x축), y축 위의 점 C를 중심으로 점근선에 접하는 작은 원, 원점 중심·C를 지나는 원, 제1사분면 교점 P, 선분 PF·PF′·CF"}}],
    confidence=0.85,
    note="윗줄 PF·PF′을 seg(PF) × seg(PF')로(프라임 라벨). 답 82 유지(빠른정답 4와 불일치는 1차와 동일)")

# 8. 9efebff1 — 구의 방정식 p91: '삼각형 OQ₁R₁'은 문장 속 라벨 → sub 텍스트 혼합 유지, 공간 점 좌표 → point3
add(id="9efebff1", qtype="short",
    question="좌표공간에 중심이 C[[point3(2, sqrt(5), 5)]]이고 점 P[[point3(0, 0, 1)]]을 지나는 구 [[S]]: [[pow(x - 2, 2) + pow(y - sqrt(5), 2) + pow(z - 5, 2) = 25]]가 있다. 구 [[S]]가 평면 OPC와 만나서 생기는 원 위를 움직이는 점 Q, 구 [[S]] 위를 움직이는 점 R에 대하여 두 점 Q, R의 xy평면 위로의 정사영을 각각 [[sub(Q,1)]], [[sub(R,1)]]이라 하자. 삼각형 O[[sub(Q,1)]][[sub(R,1)]]의 넓이가 최대가 되도록 하는 두 점 Q, R에 대하여 삼각형 O[[sub(Q,1)]][[sub(R,1)]]의 평면 PQR 위로의 정사영의 넓이는 [[frac(q, p) sqrt(6)]] 이다. [[p + q]]의 값을 구하시오.\n(단, O는 원점이고 세 점 O, [[sub(Q,1)]], [[sub(R,1)]]은 한 직선 위에 있지 않으며, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간: z축 근처에 놓인 구(적도 원 점선), z축 위의 점 P(0,0,1), 원점 O"}}],
    confidence=0.85,
    note="[2021년 11월 고3 기하 30번/4점]. 첨자 점 이름(Q₁, R₁)은 문장 속 라벨이라 sub 텍스트 혼합 유지(수식 기호 없음), 점 좌표는 point3. 답 23 유지")

# 9. 8edc5750 — 구의 방정식 p94: 8번 변형, 같은 처리
add(id="8edc5750", qtype="short",
    question="좌표공간에 중심이 C[[point3(4, 3, 15)]]이고 점 P[[point3(0, 0, 3)]]을 지나는 구 [[S]]: [[pow(x - 4, 2) + pow(y - 3, 2) + pow(z - 15, 2) = 169]]가 있다. 구 [[S]]가 평면 OPC와 만나서 생기는 원 위를 움직이는 점 Q, 구 [[S]] 위를 움직이는 점 R에 대하여 두 점 Q, R의 xy평면 위로의 정사영을 각각 [[sub(Q,1)]], [[sub(R,1)]]이라 하자. 삼각형 O[[sub(Q,1)]][[sub(R,1)]]의 넓이가 최대가 되도록 하는 두 점 Q, R에 대하여 삼각형 O[[sub(Q,1)]][[sub(R,1)]]의 평면 PQR 위로의 정사영의 넓이는 [[frac(q, p) sqrt(17)]] 이다. [[p + q]]의 값을 구하시오.\n(단, O는 원점이고 세 점 O, [[sub(Q,1)]], [[sub(R,1)]]은 한 직선 위에 있지 않으며, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간: z축 근처에 놓인 큰 구(적도 원 점선), z축 위의 점 P(0,0,3), 원점 O"}}],
    confidence=0.8,
    note="[2021년 11월 고3 기하 30번 변형]. 첨자 점 이름은 sub 텍스트 혼합 유지, 점 좌표는 point3. 답 368 유지(빠른정답 23과 불일치는 1차와 동일)")

# 10. f2ca4aba — 평면과 구의 방정식 p97: P₁Q₁→·P₂Q₂→ → vec(P1Q1)·vec(P2Q2)
add(id="f2ca4aba", qtype="short",
    question="좌표공간에서 구 [[pow(x,2) + pow(y,2) + pow(z,2) = 4]] 위를 움직이는 두 점 P, Q가 있다. 두 점 P, Q에서 평면 [[y = 4]]에 내린 수선의 발을 각각 [[sub(P,1)]], [[sub(Q,1)]]이라 하고, 평면 [[y + sqrt(3) z + 8 = 0]]에 내린 수선의 발을 각각 [[sub(P,2)]], [[sub(Q,2)]]라 하자. [[2 pow(abs(vec(PQ)), 2) - pow(abs(vec(P1Q1)), 2) - pow(abs(vec(P2Q2)), 2)]]의 최댓값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "구 위의 두 점 P, Q와 벡터 PQ→; 평면 y=4 위의 정사영 P₁, Q₁과 벡터 P₁Q₁→; 평면 y+√3z+8=0 위의 정사영 P₂, Q₂와 벡터 P₂Q₂→"}}],
    confidence=0.85,
    note="[2013년 11월 고3 이과 29번/4점]. sub(vec(PQ),1) 우회 → vec(P1Q1)·vec(P2Q2). 답 24 유지")

# 11. 48c30ebc — 포물선 p38: 윗줄 A₁C·F₁B·F₂B → seg(A1C)·seg(F1B)·seg(F2B); '삼각형 BF₂F₁'·'직선 F₁F₂'는 문장 속 라벨 → sub 텍스트 유지
add(id="48c30ebc", qtype="short",
    question="다음 그림과 같이 꼭짓점이 [[sub(A,1)]]이고 초점이 [[sub(F,1)]]인 포물선 [[sub(P,1)]]과 꼭짓점이 [[sub(A,2)]]이고 초점이 [[sub(F,2)]]인 포물선 [[sub(P,2)]]가 있다. 두 포물선의 준선은 모두 직선 [[sub(F,1)]][[sub(F,2)]]와 평행하고, 두 선분 [[sub(A,1)]][[sub(A,2)]], [[sub(F,1)]][[sub(F,2)]]의 중점은 서로 일치한다. 두 포물선 [[sub(P,1)]], [[sub(P,2)]]가 서로 다른 두 점에서 만날 때 두 점 중에서 점 [[sub(A,2)]]에 가까운 점을 B라 하자. 포물선 [[sub(P,1)]]이 직선 [[sub(F,1)]][[sub(F,2)]]와 만나는 점을 C라 할 때, 두 점 B, C가 다음 조건을 모두 만족시킨다.\n(가) [[seg(A1C) = sqrt(5)]]\n(나) [[2 × seg(F1B) - seg(F2B) = frac(11, 4)]]\n삼각형 B[[sub(F,2)]][[sub(F,1)]]의 넓이가 [[frac(sqrt(a) - sqrt(b), 8)]] 일 때, [[a b]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "세로 직선 F₁F₂(F₁ 아래, F₂ 위) 위에 두 초점, 왼쪽으로 열린 포물선 P₂(꼭짓점 A₂ 오른쪽)와 오른쪽으로 열린 포물선 P₁(꼭짓점 A₁ 왼쪽)이 교차, 위쪽 교점 B, P₁과 직선 F₁F₂의 교점 C, 선분 BF₁"}}],
    confidence=0.8,
    note="[2022년 3월 고3 기하 30번 변형]. 조건 (가)(나)의 윗줄 선분을 seg(A1C)·seg(F1B)·seg(F2B)로('2 ·'는 ×), 문장 속 첨자 점 이름은 sub 텍스트 유지. 답 15 유지(빠른정답 '1 36'과 불일치는 1차와 동일)")

# 12. 3caa758b — 포물선 p38(같은 이미지, 다른 id): 11번과 동일
add(id="3caa758b", qtype="short",
    question="다음 그림과 같이 꼭짓점이 [[sub(A,1)]]이고 초점이 [[sub(F,1)]]인 포물선 [[sub(P,1)]]과 꼭짓점이 [[sub(A,2)]]이고 초점이 [[sub(F,2)]]인 포물선 [[sub(P,2)]]가 있다. 두 포물선의 준선은 모두 직선 [[sub(F,1)]][[sub(F,2)]]와 평행하고, 두 선분 [[sub(A,1)]][[sub(A,2)]], [[sub(F,1)]][[sub(F,2)]]의 중점은 서로 일치한다. 두 포물선 [[sub(P,1)]], [[sub(P,2)]]가 서로 다른 두 점에서 만날 때 두 점 중에서 점 [[sub(A,2)]]에 가까운 점을 B라 하자. 포물선 [[sub(P,1)]]이 직선 [[sub(F,1)]][[sub(F,2)]]와 만나는 점을 C라 할 때, 두 점 B, C가 다음 조건을 모두 만족시킨다.\n(가) [[seg(A1C) = sqrt(5)]]\n(나) [[2 × seg(F1B) - seg(F2B) = frac(11, 4)]]\n삼각형 B[[sub(F,2)]][[sub(F,1)]]의 넓이가 [[frac(sqrt(a) - sqrt(b), 8)]] 일 때, [[a b]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "세로 직선 F₁F₂(F₁ 아래, F₂ 위) 위에 두 초점, 왼쪽으로 열린 포물선 P₂(꼭짓점 A₂ 오른쪽)와 오른쪽으로 열린 포물선 P₁(꼭짓점 A₁ 왼쪽)이 교차, 위쪽 교점 B, P₁과 직선 F₁F₂의 교점 C, 선분 BF₁"}}],
    confidence=0.8,
    note="[2022년 3월 고3 기하 30번 변형] (48c30ebc와 같은 이미지). 조건의 윗줄 선분을 seg 라벨로, 문장 속 첨자 점 이름은 sub 텍스트 유지. 답 15 유지")

# 13. dec5e075 — 정사영 p65: AA′·A′P·A′B′·PB′ 윗줄 → seg(AA')·seg(A'P)·seg(A'B')·seg(PB')
add(id="dec5e075", qtype="short",
    question="공간에 점 P를 포함하는 평면 [[alpha]]가 있다. 평면 [[alpha]] 위에 있지 않은 서로 다른 두 점 A, B의 평면 [[alpha]] 위로의 정사영을 각각 A′, B′이라 할 때, [[seg(AA') = 6]], [[seg(A'P) = seg(A'B') = 3]], [[seg(PB') = 4]]이다.\n선분 PB′의 중점 M에 대하여 [[angle(MAB) = frac(pi, 2)]] 일 때, 직선 BM과 평면 APB′이 이루는 예각의 크기를 [[theta]]라 하자.\n[[pow(tan(theta), 2) = frac(q, p)]] 일 때, [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "평면 α 위의 점 P, A′, B′, M(PB′의 중점); α 위쪽의 점 A(A′ 바로 위), B(B′ 바로 위); 선분 AB·AP·AB′·BM, 직각 표시"}}],
    confidence=0.85,
    note="[2024년 7월 고3 기하 30번 변형]. 프라임 점 윗줄 선분을 seg(AA')·seg(A'P)·seg(A'B')·seg(PB')로; 단독 점 이름 A′·B′은 텍스트. 답 365 유지")

# 14. ed0f5ab8 — 정사영 p66: 13번 원문항, 같은 처리
add(id="ed0f5ab8", qtype="short",
    question="공간에 점 P를 포함하는 평면 [[alpha]]가 있다. 평면 [[alpha]] 위에 있지 않은 서로 다른 두 점 A, B의 평면 [[alpha]] 위로의 정사영을 각각 A′, B′이라 할 때, [[seg(AA') = 9]], [[seg(A'P) = seg(A'B') = 5]], [[seg(PB') = 8]]이다. 선분 PB′의 중점 M에 대하여 [[angle(MAB) = frac(pi, 2)]] 일 때, 직선 BM과 평면 APB′이 이루는 예각의 크기를 [[theta]]라 하자. [[pow(cos(theta), 2) = frac(q, p)]] 일 때, [[p + q]]의 값을 구하시오. (단, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "평면 α 위의 점 P, A′, B′, M(PB′의 중점); α 위쪽의 점 A(A′ 바로 위), B(B′ 바로 위); 선분 AB·AP·AB′·BM, 직각 표시"}}],
    confidence=0.85,
    note="[2024년 7월 고3 기하 30번/4점]. 프라임 점 윗줄 선분을 seg(AA')·seg(A'P)·seg(A'B')·seg(PB')로. 답 111 유지")

# 15. 25452c7e — 정사영 p86: ∠A′OB′ = 180° → angle(A'OB') = deg(180)
add(id="25452c7e", qtype="short",
    question="그림과 같이 밑면의 반지름의 길이가 7인 원기둥과 밑면의 반지름의 길이가 5이고 높이가 12인 원뿔이 평면 [[alpha]]위에 놓여 있고, 원뿔의 밑면의 둘레가 원기둥의 밑면의 둘레에 내접한다. 평면 [[alpha]]와 만나는 원기둥의 밑면의 중심을 O, 원뿔의 꼭짓점을 A라 하자. 중심이 B이고 반지름의 길이가 4인 구 [[S]]가 다음 조건을 만족시킨다.\n(가) 구 [[S]]는 원기둥과 원뿔에 모두 접한다.\n(나) 두 점 A,B의 평면 [[alpha]] 위로의 정사영이 각각 A′, B′일 때, [[angle(A'OB') = deg(180)]]이다.\n직선 AB와 평면 [[alpha]]가 이루는 예각의 크기를 [[theta]]라 할 때, [[tan(theta) = p]]이다. [[100p]]의 값을 구하시오. (단, 원뿔의 밑면의 중심과 점 A′은 일치한다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "평면 α 위의 원기둥 안에 원뿔(밑면이 원기둥 밑면에 내접)과 구가 놓인 입체도"}}],
    confidence=0.85,
    note="[2011년 11월 고3 이과 29번/4점]. ∠A′OB′=180°를 angle(A'OB') = deg(180)으로. 답 34 유지")

# 16. 7027d1b6 — 이차곡선 p3: AQ + F′Q 윗줄 → seg(AQ) + seg(F'Q)
add(id="7027d1b6", qtype="short",
    question="다음 그림과 같이 두 점 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 2 pow(a,2)) = 1]]이 있다. 이 쌍곡선의 꼭짓점 중 [[x]]좌표가 음수인 점을 A라 하고, 점 F′을 지나고 [[x]]축에 수직인 직선이 이 쌍곡선과 만나는 점 중 제2사분면에 있는 점을 P라 하자. 점 A에서 선분 PF에 내린 수선의 발을 H라 하자. 두 점 A, F를 초점으로 하고 점 H를 지나는 타원이 이 쌍곡선과 만나는 점 중 제4사분면에 있는 점을 Q라 하자.\n[[seg(AQ) + seg(F'Q) = 6 + 8 sqrt(3)]] 일 때, 이 타원의 장축의 길이는 [[p + q sqrt(3)]] 이다. [[pow(p,2) + pow(q,2)]]의 값을 구하시오.\n(단, [[a]]는 양수이고, [[p]]와 [[q]]는 유리수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/a²−y²/(2a²)=1, 초점 F′·F, 꼭짓점 A, F′ 위의 점 P, 선분 PF와 A에서 내린 수선의 발 H(직각), 초점 A·F인 타원, 제4사분면 교점 Q, 선분 AQ·F′Q"}}],
    confidence=0.85,
    note="[2026년 3월 고3 기하 30번/4점]. 윗줄 F′Q를 seg(F'Q)로 한 식에; 점 F′은 텍스트. 답 52 유지")

# 17. d2b82d64 — 이차곡선 p22: 프라임은 점 이름 F′(−c, 0)뿐 → 텍스트 유지, 그대로 통과
add(id="d2b82d64", qtype="short",
    question="그림과 같이 두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 타원 [[C]]가 있다. 타원 [[C]]가 두 직선 [[x = c]], [[x = -c]]와 만나는 점 중 [[y]]좌표가 양수인 점을 각각 A, B라 하자. 두 초점이 A, B이고 점 F를 지나는 쌍곡선이 직선 [[x = c]]와 만나는 점 중 F가 아닌 점을 P라 하고, 이 쌍곡선이 두 직선 BF, BP와 만나는 점 중 [[x]]좌표가 음수인 점을 각각 Q, R라 하자. 세 점 P, Q, R가 다음 조건을 만족시킨다.\n(가) 삼각형 BFP는 정삼각형이다.\n(나) 타원 [[C]]의 장축의 길이와 삼각형 BQR의 둘레의 길이의 차는 3이다.\n[[60 seg(AF)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 초점 F′·F인 타원 C, x=c 위의 점 A와 P, x=−c 위의 점 B, 초점 A·B인 쌍곡선, 직선 BF·BP와 쌍곡선의 교점 Q, R"}}],
    confidence=0.85,
    note="[2023년 3월 고3 기하 30번/4점]. 프라임은 단독 점 이름 F′뿐(텍스트 허용) — 수식은 이미 문법 안. 답 100 유지")

# 18. 3ea80e15 — 이차곡선 p36: 17번 변형, 그대로 통과
add(id="3ea80e15", qtype="short",
    question="아래 그림과 같이 두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 타원 [[C]]가 있다. 타원 [[C]]가 두 직선 [[x = c]], [[x = -c]]와 만나는 점 중 [[y]]좌표가 양수인 점을 각각 A, B라 하자. 두 초점이 A, B이고 점 F를 지나는 쌍곡선이 직선 [[x = c]]와 만나는 점 중 F가 아닌 점을 P라 하고, 이 쌍곡선이 두 직선 BF, BP와 만나는 점 중 [[x]]좌표가 음수인 점을 각각 Q, R라 하자. 세 점 P, Q, R가 다음 조건을 만족시킨다.\n(가) 삼각형 BFP는 [[seg(BF) = seg(BP)]]이고, [[seg(BF) = frac(3, 4) seg(PF)]] 인 이등변삼각형이다.\n(나) 타원 [[C]]의 장축의 길이와 삼각형 BQR의 둘레의 길이의 차는 [[frac(5, 2)]] 이다.\n[[15 seg(AF)]]의 값을 구하시오.",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 초점 F′·F인 타원 C, x=c 위의 점 A와 P, x=−c 위의 점 B, 초점 A·B인 쌍곡선, 직선 BF·BP와 쌍곡선의 교점 Q, R"}}],
    confidence=0.8,
    note="[2023년 3월 고3 기하 30번 변형]. 프라임은 단독 점 이름 F′뿐(텍스트 허용). 답 30 유지(빠른정답 207과 불일치는 1차와 동일)")

# 19. 1c760caf — 이차곡선 p41: (가) AF′ − AF = 2a 윗줄 → seg(AF') - seg(AF) = 2a; '삼각형 AF′F'는 텍스트
add(id="1c760caf", qtype="short",
    question="두 초점 F, F′이 [[y]]축에 대하여 대칭이고, 직선 [[y = 4 sqrt(3) x]]가 한 점근선인 쌍곡선이 포물선 [[pow(y,2) = 36a(x + 2a)]]와 만나는 점 중 제1사분면에 있는 점을 A라 하자. 점 A가 다음 조건을 만족할 때, 선분 AF의 길이를 구하시오. (단, [[a]]는 양수이다.)\n(가) [[seg(AF') - seg(AF) = 2a]]\n(나) 점 A의 [[x]]좌표는 점 F의 [[x]]좌표보다 작다.\n(다) 삼각형 AF′F의 넓이는 84이다.",
    choices=None, figure=None, confidence=0.85,
    note="조건 (가)의 프라임 윗줄 선분을 seg(AF')로 한 식에. 답 13 유지")

# 20. 7bb671ba — 이차곡선 p42: 19번과 같은 처리
add(id="7bb671ba", qtype="short",
    question="두 초점 F, F′이 [[y]]축에 대하여 대칭이고, 직선 [[y = 2 sqrt(2) x]]가 한 점근선인 쌍곡선이 포물선 [[pow(y,2) = 12 a x]]와 만나는 점 중 제1사분면에 있는 점을 A라 하자. 점 A가 다음 조건을 만족할 때, 선분 AF의 길이를 구하시오. (단, [[a]]는 양수이다.)\n(가) [[seg(AF') - seg(AF) = 2a]]\n(나) 점 A의 [[x]]좌표는 점 F의 [[x]]좌표보다 작다.\n(다) 삼각형 AF′F의 넓이는 [[6 sqrt(6)]] 이다.",
    choices=None, figure=None, confidence=0.85,
    note="조건 (가)의 프라임 윗줄 선분을 seg(AF')로. 답 5 유지(재검산: a=1, A(2, 2√6), AF=5 — 빠른정답 4와 불일치는 1차와 동일)")

# 21. 04febd1f — 이차곡선 p43: 19번과 같은 처리
add(id="04febd1f", qtype="short",
    question="두 초점 F, F′이 [[y]]축에 대하여 대칭이고, 직선 [[y = 2 sqrt(6) x]]가 한 점근선인 쌍곡선이 포물선 [[pow(y,2) = 24a(x + a)]]와 만나는 점 중 제1사분면에 있는 점을 A라 하자. 점 A가 다음 조건을 만족할 때, 선분 AF의 길이를 구하시오. (단, [[a]]는 양수이다.)\n(가) [[seg(AF') - seg(AF) = 2a]]\n(나) 점 A의 [[x]]좌표는 점 F의 [[x]]좌표보다 작다.\n(다) 삼각형 AF′F의 넓이는 [[30 sqrt(2)]] 이다.",
    choices=None, figure=None, confidence=0.85,
    note="조건 (가)의 프라임 윗줄 선분을 seg(AF')로. 답 9 유지(빠른정답 4와 불일치는 1차와 동일)")

# 22. 75364b1c — 타원 p60: 프라임은 문장 속(선분 QF′, F′(−4,0))뿐이라 문법은 통과하나, 1차가 지적한 문항 결함(조건 양립 불가)이 재검산으로도 확인됨 → 보류 유지
add(id="75364b1c", qtype="short",
    question="두 점 F[[point(4, 0)]], F′[[point(-4, 0)]]을 초점으로 하는 타원 위의 서로 다른 두 점 P, Q에 대하여 원점 O에서 선분 PF와 선분 QF′에 내린 수선의 발을 각각 H와 I라 하자. 점 H와 점 I가 각각 선분 PF와 선분 QF′의 중점이고, [[seg(OH) × seg(OI) = 12]]일 때, 이 타원의 장축의 길이를 [[l]]이라 하자. [[pow(l,2)]]의 값을 구하시오. (단, [[seg(OH) != seg(OI)]])",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 타원과 초점 F′·F, 제1사분면의 점 P와 선분 PF 위의 중점 H(OH⊥PF 직각), 제4사분면의 점 Q와 선분 QF′ 위의 중점 I(OI⊥QF′ 직각), 같은 길이 표시"}}],
    confidence=0.65,
    needs_review="문항 결함 의심(조건 양립 불가): OP=OF=4이면 ∠FPF′=90°로 PF²+PF′²=64인데 OH·OI=12 ⇔ PF′·QF=48은 (QF=PF이면 (PF−PF′)²<0, QF=PF′이면 OH=OI) — 답 160은 출제 의도 추정이라 확정 불가",
    note="길이의 곱 OH·OI는 seg(OH) × seg(OI)로(문법 통과). 답 160 유지(1차 추정값; 빠른정답 26과 불일치)")

# 23. 87aedd07 — 타원 p61: 22번의 원형(수치 6, 14) — 조건 양립함(PF=6+2√2 등), 그대로 통과
add(id="87aedd07", qtype="short",
    question="두 점 F[[point(6, 0)]], F′[[point(-6, 0)]]을 초점으로 하는 타원 위의 서로 다른 두 점 P, Q에 대하여 원점 O에서 선분 PF와 선분 QF′에 내린 수선의 발을 각각 H와 I라 하자. 점 H와 점 I가 각각 선분 PF와 선분 QF′의 중점이고, [[seg(OH) × seg(OI) = 14]]일 때, 이 타원의 장축의 길이를 [[l]]이라 하자. [[pow(l,2)]]의 값을 구하시오. (단, [[seg(OH) != seg(OI)]])",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 타원과 초점 F′·F, 제1사분면의 점 P와 선분 PF 위의 중점 H(OH⊥PF 직각), 제4사분면의 점 Q와 선분 QF′ 위의 중점 I(OI⊥QF′ 직각), 같은 길이 표시"}}],
    confidence=0.85,
    note="프라임은 문장 속 라벨(선분 QF′)뿐 — 텍스트 유지; 길이의 곱은 seg(OH) × seg(OI)로. 답 256 유지(PF·PF′=56, PF²+PF′²=144 → l²=256)")

# 24. 980cff30 — 타원 p64: PF/FF′ 윗줄 분수 → frac(seg(PF), seg(FF')); '삼각형 FF′Q'는 텍스트
add(id="980cff30", qtype="choice",
    question="두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]]([[c > 0]])인 타원 [[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), pow(b,2)) = 1]]이 있다. 이 타원 위에 있는 제1사분면 위의 점 P와 이 타원 위에 있는 제4사분면 위의 점 Q에 대하여 점 F가 선분 PQ 위에 있고 [[frac(seg(PF), seg(QF)) = frac(1, 2)]], [[frac(seg(PF), seg(FF')) = frac(sqrt(6), 16)]] 이다. 삼각형 FF′Q의 넓이가 [[4 sqrt(5)]] 일 때, [[pow(b,2)]]의 값은? (단, [[a]]와 [[b]]는 양수이다.)",
    choices=["[[frac(13, 2)]]", "[[7]]", "[[frac(15, 2)]]", "[[8]]", "[[frac(17, 2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 타원, 초점 F′·F, 제1사분면의 점 P와 제4사분면의 점 Q를 잇는 선분 PQ가 F를 지남, 선분 F′Q"}}],
    confidence=0.85,
    note="[2026년 6월 고3 기하 28번/4점]. 윗줄 FF′을 seg(FF')로 분수 안에. 답 ④ 유지(빠른정답 256과 불일치는 1차와 동일)")

# 25. 05fb5120 — 타원 p71: 프라임은 문장 속(직선 F′P, 선분 F′F)뿐 → 그대로 통과
add(id="05fb5120", qtype="short",
    question="그림과 같이 두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 타원 [[frac(pow(x,2), 16) + frac(pow(y,2), 7) = 1]] 위의 점 P에 대하여 직선 FP와 직선 F′P에 동시에 접하고 중심이 선분 F′F 위에 있는 원 [[C]]가 있다. 원 [[C]]의 중심을 C, 직선 F′P가 원 [[C]]와 만나는 점을 Q라 할 때, [[2 seg(PQ) = seg(PF)]] 이다. [[24 seg(CP)]] 의 값을 구하시오. (단, 점 P는 제1사분면 위의 점이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 타원 x²/16+y²/7=1, 초점 F′·F, 제1사분면 위쪽의 점 P, 직선 PF·PF′에 접하고 중심 C가 x축 위에 있는 원, 직선 F′P와 원의 교점 Q"}}],
    confidence=0.85,
    note="[2021년 4월 고3 기하 30번/4점]. 프라임은 문장 속 라벨뿐 — 텍스트 유지, 수식은 이미 문법 안. 답 63 유지")

# 26. c792bb13 — 타원 p72: 24번 변형, 같은 처리
add(id="c792bb13", qtype="choice",
    question="두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]]([[c > 0]])인 타원 [[frac(pow(x,2), pow(a,2)) + frac(pow(y,2), pow(b,2)) = 1]]이 있다. 이 타원 위에 있는 제1사분면 위의 점 P와 이 타원 위에 있는 제4사분면 위의 점 Q에 대하여 점 F가 선분 PQ 위에 있고 [[frac(seg(PF), seg(QF)) = frac(1, 2)]], [[frac(seg(PF), seg(FF')) = frac(sqrt(5), 10)]] 이다. 삼각형 FF′Q의 넓이가 12일 때, [[pow(b,2)]]의 값은? (단, [[a]]와 [[b]]는 양수이다.)",
    choices=["[[10]]", "[[11]]", "[[12]]", "[[13]]", "[[14]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 타원, 초점 F′·F, 제1사분면의 점 P와 제4사분면의 점 Q를 잇는 선분 PQ가 F를 지남, 선분 F′Q"}}],
    confidence=0.85,
    note="[2026년 6월 고3 기하 28번 변형]. 윗줄 FF′을 seg(FF')로 분수 안에. 답 ③ 유지")

# 27. d1fd84c3 — 타원 p82: PO·PO′ 윗줄 → seg(PO) × seg(PO')
add(id="d1fd84c3", qtype="short",
    question="원 [[pow(x,2) + pow(y,2) = 100]]에 내접하면서 원 [[pow(x - 4, 2) + pow(y,2) = 4]]에 외접하는 원의 중심 P가 그리는 도형을 [[E]]라 하자. 두 점 O[[point(0, 0)]], O′[[point(4, 0)]]에 대하여 [[seg(PO) × seg(PO')]] 의 최댓값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="윗줄 PO′을 seg(PO')로 곱 안에. 답 36 유지(PO+PO′=12 → 곱 최대 36; 빠른정답 4와 불일치는 1차와 동일)")

# 28. 113150ef — 쌍곡선의 접선 p46: ∠F′PF → angle(F'PF), 윗줄 Q₁Q₂ → seg(Q1Q2); '삼각형 F′FP'·'직선 PF′'은 텍스트
add(id="113150ef", qtype="short",
    question="그림과 같이 두 점 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 쌍곡선 [[frac(pow(x,2), 10) - frac(pow(y,2), pow(a,2)) = 1]]이 있다. 쌍곡선 위의 점 중 제2사분면에 있는 점 P에 대하여 삼각형 F′FP는 넓이가 15이고 [[angle(F'PF) = frac(pi, 2)]] 인 직각삼각형이다. 직선 PF′과 평행하고 쌍곡선에 접하는 두 직선을 각각 [[sub(l,1)]], [[sub(l,2)]]라 하자. 두 직선 [[sub(l,1)]], [[sub(l,2)]]가 [[x]]축과 만나는 점을 각각 [[sub(Q,1)]], [[sub(Q,2)]]라 할 때, [[seg(Q1Q2) = frac(q, p) sqrt(3)]] 이다. [[p + q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 서로소인 자연수이고, [[a]]는 양수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선, 초점 F′·F, 제2사분면의 점 P(∠F′PF 직각 표시), 직선 PF′·PF, PF′과 평행한 두 접선 l₁, l₂와 x축 교점 Q₁, Q₂"}}],
    confidence=0.85,
    note="[2022년 4월 고3 기하 30번/4점]. ∠F′PF=π/2를 angle(F'PF)로, 윗줄 Q₁Q₂를 seg(Q1Q2)로. 답 13 유지(재검산: c=5, a²=15, Q₁Q₂=10√3/3)")

# 29. c6852541 — 쌍곡선의 접선 p60: 28번 변형, 같은 처리
add(id="c6852541", qtype="short",
    question="다음 그림과 같이 두 점 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 쌍곡선 [[frac(pow(x,2), 24) - frac(pow(y,2), pow(a,2)) = 1]]이 있다. 쌍곡선 위의 점 중 제2사분면에 있는 점 P에 대하여 삼각형 F′FP는 넓이가 36이고 [[angle(F'PF) = frac(pi, 2)]] 인 직각삼각형이다. 직선 PF′과 평행하고 쌍곡선에 접하는 두 직선을 각각 [[sub(l,1)]], [[sub(l,2)]]라 하자. 두 직선 [[sub(l,1)]], [[sub(l,2)]]가 [[x]]축과 만나는 점을 각각 [[sub(Q,1)]], [[sub(Q,2)]]라 할 때, [[seg(Q1Q2) = p sqrt(q)]] 이다. [[p q]]의 값을 구하시오.\n(단, [[p]]와 [[q]]는 10보다 작은 자연수이고, [[a]]는 양수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선, 초점 F′·F, 제2사분면의 점 P(∠F′PF 직각 표시), 직선 PF′·PF, PF′과 평행한 두 접선 l₁, l₂와 x축 교점 Q₁, Q₂"}}],
    confidence=0.85,
    note="[2022년 4월 고3 기하 30번 변형]. ∠F′PF를 angle(F'PF)로, 윗줄 Q₁Q₂를 seg(Q1Q2)로. 답 20 유지(재검산: c²=60, a²=36, Q₁Q₂=4√5)")

# 30. a20fae19 — 쌍곡선의 접선 p88: PQ = PF′ + 4b² 윗줄 → seg(PQ) = seg(PF') + 4 pow(b,2)
add(id="a20fae19", qtype="short",
    question="두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[pow(x,2) - frac(pow(y,2), pow(a,2)) = 1]] 위의 점 중 제2사분면에 있는 점 P에 대하여 직선 PF가 타원 [[pow(x,2) + frac(pow(y,2), 4 pow(b,2)) = 1]] ([[0 < b < frac(1, 2)]])과 점 Q에서 접한다. 점 Q의 [[y]]좌표가 [[4 pow(b,2)]]이고 [[seg(PQ) = seg(PF') + 4 pow(b,2)]]일 때, [[60(pow(a,2) + pow(b,2))]]의 값을 구하시오.\n(단, [[a]]는 양수이다.)",
    choices=None, figure=None, confidence=0.85,
    note="[2026년 5월 고3 기하 30번 변형]. 윗줄 PF′을 seg(PF')로 한 식에. 답 130 유지(재검산: c²=3, a²=2, b²=1/6)")

# 31. 7ce03a39 — 쌍곡선의 접선 p89: 30번 원문항, 같은 처리
add(id="7ce03a39", qtype="short",
    question="두 초점이 F[[point(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[pow(x,2) - frac(pow(y,2), pow(a,2)) = 1]] 위의 점 중 제2사분면에 있는 점 P에 대하여 직선 PF가 타원 [[pow(x,2) + frac(pow(y,2), pow(b,2)) = 1]] ([[0 < b < 1]])과 점 Q에서 접한다. 점 Q의 [[y]]좌표가 [[pow(b,2)]]이고 [[seg(PQ) = seg(PF') + pow(b,2)]]일 때, [[30(pow(a,2) + pow(b,2))]]의 값을 구하시오.\n(단, [[a]]는 양수이다.)",
    choices=None, figure=None, confidence=0.85,
    note="[2026년 5월 고3 기하 30번/4점]. 윗줄 PF′을 seg(PF')로 한 식에. 답 80 유지(재검산: c²=3 → P(−√3, 2), Q(1/√3, 2/3), PQ=8/3=PF′+b² 성립, a²+b²=8/3)")

# 32. e24dad71 — 벡터의 실수배 p41: '삼각형 BG₁G₂'는 문장 속 라벨 → sub 텍스트 유지, 그대로 통과
add(id="e24dad71", qtype="short",
    question="그림과 같이 [[seg(AD) = 8 sqrt(3)]] 인 직사각형 ABCD가 있다. 두 점 E, F가 점 E는 선분 AD 위를, 점 F는 선분 BC 위를 [[angle(CFE) = deg(60)]] 를 만족시키며 움직인다. 선분 EF를 [[ratio(1, 2)]]로 내분하는 점을 G라 할 때, 점 G가 다음 조건을 만족시킨다.\n[[abs(vec(GA) + vec(GC))]] 의 최댓값을 [[M]], 최솟값을 [[m]]이라 할 때, [[ratio(M, m) = ratio(sqrt(13), 1)]]이다.\n[[abs(vec(GA) + vec(GC))]] 의 값이 최대일 때의 점 G를 [[sub(G,1)]], 최소일 때의 점 G를 [[sub(G,2)]]라 하자. 삼각형 B[[sub(G,1)]][[sub(G,2)]]의 넓이를 [[S]]라 할 때, [[pow(S,2)]]의 값을 구하시오. (단, [[seg(AB) <= 18]])",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상): 변 AD 위의 점 E, 변 BC 위의 점 F, 선분 EF, ∠CFE=60° 표시"}}],
    confidence=0.85,
    note="[2025년 5월 고3 기하 30번/4점]. 첨자 점 이름 G₁·G₂는 문장 속 라벨(수식 기호 없음) — sub 텍스트 혼합 유지. 답 243 유지")

# ================= esc_sonnet_h3-3_1of6 =================
# 33. 1cce8564 — 선분의 내분점 p25: 프라임은 점 이름(P′, Q′, 삼각형 OP′Q′)뿐 → 텍스트 유지, 그대로 통과
add(id="1cce8564", qtype="choice",
    question="좌표공간의 세 점 [[A(3, 0, 0)]], [[B(0, 3, 0)]], [[C(0, 0, 3)]]에 대하여 선분 BC를 [[ratio(2, 1)]]로 내분하는 점을 P, 선분 AC를 [[ratio(1, 2)]]로 내분하는 점을 Q라 하자. 점 P, Q의 [[x y]]평면 위로의 정사영을 각각 P′, Q′이라 할 때, 삼각형 OP′Q′의 넓이는? (단, O는 원점이다.)",
    choices=["1", "2", "3", "4", "5"],
    figure=None, confidence=0.85,
    note="[2005년 9월 고3 이과 14번]. 프라임은 단독 점 이름뿐(텍스트 허용). 답 ① 유지(P′(0,1,0), Q′(2,0,0) → 넓이 1; 빠른정답 4와 불일치는 1차와 동일)")

# 34. 0c3bf245 — 선분의 내분점 p34: 점 이름 P′ 텍스트, 좌표는 point3
add(id="0c3bf245", qtype="short",
    question="점 [[A(1, -2, 3)]]에 대하여 점 [[P(2, 1, 4)]]의 대칭점이 P′[[point3(a, b, c)]]일 때, [[a + b + c]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="프라임은 단독 점 이름 P′뿐(텍스트), 좌표는 point3. 답 -3 유지(P′=2A−P=(0,−5,2); 빠른정답 5와 불일치는 1차와 동일)")

# 35. 884b7797 — 선분의 내분점 p35: 선지 좌표 vcomp → point3
add(id="884b7797", qtype="choice",
    question="점 [[P(2, 7, 0)]]을 점 [[A(3, 8, -1)]]에 대하여 대칭이동한 점 P′의 좌표는?",
    choices=["[[point3(3, 6, -1)]]", "[[point3(3, 8, -3)]]", "[[point3(4, 8, -1)]]", "[[point3(4, 9, -2)]]", "[[point3(5, 10, -3)]]"],
    figure=None, confidence=0.85,
    note="프라임은 단독 점 이름 P′뿐(텍스트), 선지 좌표는 point3. 답 ④ 유지(2A−P=(4,9,−2))")

# 36. 9fd40701 — 선분의 내분점 p44: 35번과 같은 처리
add(id="9fd40701", qtype="choice",
    question="점 [[P(3, 5, 0)]]을 점 [[A(4, 1, 1)]]에 대하여 대칭이동한 점 P′의 좌표는?",
    choices=["[[point3(-5, -3, 2)]]", "[[point3(-5, -3, -2)]]", "[[point3(5, -3, -2)]]", "[[point3(5, -3, 2)]]", "[[point3(5, 3, 2)]]"],
    figure=None, confidence=0.85,
    note="프라임은 단독 점 이름 P′뿐(텍스트), 선지 좌표는 point3. 답 ④ 유지(2A−P=(5,−3,2))")

# 37. 946ceefc — 위치벡터 p83: PF < PF′ 윗줄 → seg(PF) < seg(PF'), (|FP→|+2)F′Q→ = 13QP→ → vec(F'Q)로 한 식에
add(id="946ceefc", qtype="short",
    question="두 초점이 [[F(10, 0)]], F′[[point(-10, 0)]]이고, 주축의 길이가 15인 쌍곡선이 있다. 쌍곡선 위의 [[seg(PF) < seg(PF')]]인 점 P에 대하여 점 Q가 [[(abs(vec(FP)) + 2) vec(F'Q) = 13 vec(QP)]]를 만족시킨다. 점 [[A(-22, -5)]]에 대하여 [[abs(vec(AQ))]]의 최댓값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2024년 6월 고3 기하 30번 변형]. 윗줄 PF′을 seg(PF')로, 벡터 F′Q→를 vec(F'Q)로 한 식에. 답 26 유지(F′Q=13, AF′=13)")

# 38. 2a167cd3 — 위치벡터 p84: 37번 원문항, 같은 처리
add(id="2a167cd3", qtype="short",
    question="두 초점이 [[F(5, 0)]], F′[[point(-5, 0)]]이고, 주축의 길이가 6인 쌍곡선이 있다. 쌍곡선 위의 [[seg(PF) < seg(PF')]]인 점 P에 대하여 점 Q가 [[(abs(vec(FP)) + 1) vec(F'Q) = 5 vec(QP)]]를 만족시킨다.\n점 [[A(-9, -3)]]에 대하여 [[abs(vec(AQ))]]의 최댓값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2024년 6월 고3 기하 30번/4점]. 윗줄 PF′을 seg(PF')로, 벡터 F′Q→를 vec(F'Q)로. 답 10 유지(F′Q=5, AF′=5)")

# 39. 7ee212bf — 삼수선 정리 p27: BP′ = 4 윗줄 → seg(BP') = 4
add(id="7ee212bf", qtype="choice",
    question="밑면의 반지름의 길이가 2, 높이가 2인 원기둥이 있다.\n이 원기둥의 한 밑면의 둘레 위의 한 점 P에서 다른 밑면에 내린 수선의 발을 P′이라 하고, 점 P를 포함하는 밑면의 중심을 O라 하자. 점 P′을 포함하는 밑면의 둘레 위의 서로 다른 두 점 A, B에 대하여 점 O에서 선분 AB에 내린 수선의 발을 H라 하자. [[seg(BP') = 4]], [[seg(OH) = sqrt(5)]]일 때, 삼각형 PAH의 넓이는?",
    choices=["[[frac(sqrt(6), 2)]]", "[[frac(3 sqrt(6), 4)]]", "[[sqrt(6)]]", "[[frac(5 sqrt(6), 4)]]", "[[frac(3 sqrt(6), 2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "원기둥. 윗면 둘레 위 점 P와 윗면 중심 O, 아랫면의 P′(직각 표시), 아랫면 둘레 위 점 A, B와 선분 AB 위의 수선의 발 H(직각 표시), 삼각형 PAH 음영"}}],
    confidence=0.85,
    note="[2024년 7월 고3 기하 27번 변형]. 윗줄 BP′=4를 seg(BP')로; 원기둥 그림은 unsupported 유지. 답 ③ 유지(AH=√3, PA=2√2 → √6)")

# 40. e6b3273c — 삼수선 정리 p50: HF′ < HF 윗줄 → seg(HF') < seg(HF), ∠HFF′ → angle(HFF')
add(id="e6b3273c", qtype="choice",
    question="다음 그림과 같이 서로 다른 두 평면 [[alpha]], [[beta]]의 교선 위에 [[seg(AB) = 27]]인 두 점 A, B가 있다. 선분 AB를 지름으로 하는 원 [[sub(C,1)]]이 평면 [[alpha]] 위에 있고, 선분 AB를 장축으로 하고 두 점 F, F′을 초점으로 하는 타원 [[sub(C,2)]]가 평면 [[beta]] 위에 있다. 원 [[sub(C,1)]] 위의 한 점 P에서 평면 [[beta]]에 내린 수선의 발을 H라 할 때, [[seg(HF') < seg(HF)]]이고 [[angle(HFF') = frac(pi, 6)]]이다.\n직선 HF와 타원 [[sub(C,2)]]가 만나는 점 중 점 H와 가까운 점을 Q라 하면 [[seg(FH) < seg(FQ)]]이다. 점 H를 중심으로 하고 점 Q를 지나는 평면 [[beta]] 위의 원은 반지름의 길이가 6이고 직선 AB에 접한다. 두 평면 [[alpha]], [[beta]]가 이루는 각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값은?\n(단, 점 P는 평면 [[beta]] 위에 있지 않다.)",
    choices=["[[frac(sqrt(2), 3)]]", "[[frac(2 sqrt(74), 37)]]", "[[frac(2 sqrt(19), 19)]]", "[[frac(2 sqrt(78), 39)]]", "[[frac(sqrt(5), 5)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "교선 AB를 공유하는 두 평면 α(아래), β(위). α 위의 원 C₁(지름 AB)과 그 위의 점 P, β 위의 타원 C₂(장축 AB, 초점 F, F′), P에서 β에 내린 수선의 발 H, 직선 HF와 타원의 교점 Q, H 중심 원(점선), 이면각 θ 표시"}}],
    confidence=0.85,
    note="[2023년 11월 고3 기하 28번 변형]. 윗줄 HF′을 seg(HF')로, ∠HFF′을 angle(HFF')로; 입체도는 unsupported 유지. 답 ④ 유지(원문항 3/2배 확대, cos θ 불변)")

# 41. 3492b871 — 삼수선 정리 p51: 40번 원문항, 같은 처리
add(id="3492b871", qtype="choice",
    question="그림과 같이 서로 다른 두 평면 [[alpha]], [[beta]]의 교선 위에 [[seg(AB) = 18]]인 두 점 A, B가 있다. 선분 AB를 지름으로 하는 원 [[sub(C,1)]]이 평면 [[alpha]] 위에 있고, 선분 AB를 장축으로 하고 두 점 F, F′을 초점으로 하는 타원 [[sub(C,2)]]가 평면 [[beta]] 위에 있다. 원 [[sub(C,1)]] 위의 한 점 P에서 평면 [[beta]]에 내린 수선의 발을 H라 할 때, [[seg(HF') < seg(HF)]]이고 [[angle(HFF') = frac(pi, 6)]]이다.\n직선 HF와 타원 [[sub(C,2)]]가 만나는 점 중 점 H와 가까운 점을 Q라 하면 [[seg(FH) < seg(FQ)]]이다. 점 H를 중심으로 하고 점 Q를 지나는 평면 [[beta]] 위의 원은 반지름의 길이가 4이고 직선 AB에 접한다. 두 평면 [[alpha]], [[beta]]가 이루는 각의 크기를 [[theta]]라 할 때, [[cos(theta)]]의 값은?\n(단, 점 P는 평면 [[beta]] 위에 있지 않다.)",
    choices=["[[frac(2 sqrt(66), 33)]]", "[[frac(4 sqrt(69), 69)]]", "[[frac(sqrt(2), 3)]]", "[[frac(4 sqrt(3), 15)]]", "[[frac(2 sqrt(78), 39)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "교선 AB를 공유하는 두 평면 α(아래), β(위). α 위의 원 C₁(지름 AB)과 그 위의 점 P, β 위의 타원 C₂(장축 AB, 초점 F, F′), P에서 β에 내린 수선의 발 H, 직선 HF와 타원의 교점 Q, H 중심 원(점선), 이면각 θ 표시"}}],
    confidence=0.85,
    note="[2023년 11월 고3 기하 28번/4점]. 윗줄 HF′을 seg(HF')로, ∠HFF′을 angle(HFF')로. 답 ⑤ 유지")

# ================= esc_sonnet_h3-3_2of6 =================
# 42. d2c737b5 — 벡터의 성분 p99: 한 이미지에 별개 문항 2개(id 1개) — 첫째(구) 문항만 전사, 보류 유지
add(id="d2c737b5", qtype="short",
    question="세 점 [[A(1, 0, 2)]], [[B(2, 4, -1)]], [[C(3, 2, -1)]]에 대하여 [[abs(vec(PA) + vec(PB) + vec(PC)) = 9]]를 만족시키는 점 P가 나타내는 도형은 중심의 좌표가 [[point3(a, b, c)]]이고 반지름의 길이가 [[r]]인 구이다. 이때 [[a + b + c + r]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.8,
    needs_review="이미지에 별개 문항 2개 인쇄(둘째: 두 점 A(−1, 0), B(2, 0)에 대하여 점 P가 |PA→|²=4|PB→|²을 만족할 때 삼각형 PAB의 넓이의 최댓값은? 선지 ①3 ②4 ③5 ④6 ⑤7 — 답 ①)인데 id 1개 — 첫째(구) 문항만 전사",
    note="문법은 이미 통과(중심 좌표는 point3). 답 7 유지(중심 (2,2,0), 반지름 3)")

# 43. b921527d — 쌍곡선 p20: AP : PP′ = 5 : 6 윗줄 → ratio(seg(AP), seg(PP')) = ratio(5, 6)
add(id="b921527d", qtype="choice",
    question="두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선 [[C]]와 [[y]]축 위의 점 A가 있다. 쌍곡선 [[C]]가 선분 AF와 만나는 점을 P, 선분 AF′과 만나는 점을 P′이라 하자. 직선 AF는 쌍곡선 [[C]]의 한 점근선과 평행하고 [[ratio(seg(AP), seg(PP')) = ratio(5, 6)]], [[seg(PF) = 1]]일 때, 쌍곡선 [[C]]의 주축의 길이는?",
    choices=["[[frac(13,6)]]", "[[frac(9,4)]]", "[[frac(7,3)]]", "[[frac(29,12)]]", "[[frac(5,2)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 C(초점 F′·F가 x축 위), y축 위의 점 A, 선분 AF·AF′과 쌍곡선의 교점 P·P′, 선분 PP′(x축에 평행)"}}],
    confidence=0.85,
    note="[2022년 11월 고3 기하 28번/4점]. 윗줄 비 AP:PP′을 ratio(seg(AP), seg(PP'))로; 점 이름 P′·F′은 텍스트. 답 ② 유지(e=5/3, a=9/8 → 9/4; 빠른정답 4와 불일치는 1차와 동일)")

# 44. cb3baad3 — 쌍곡선 p42: 프라임은 문장 속(선분 FF′·F′P, 삼각형 QF′R)뿐 → 텍스트 유지, 그대로 통과
add(id="cb3baad3", qtype="short",
    question="다음 그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하고 주축의 길이가 8인 쌍곡선이 있다. 이 쌍곡선이 선분 FF′을 지름으로 하는 원과 제1사분면에서 만나는 점을 P라 하자. 선분 F′P가 쌍곡선과 만나는 점 중 점 P가 아닌 점을 Q라 하고, 선분 FQ가 쌍곡선과 만나는 점 중 점 Q가 아닌 점을 R이라 하자. 점 Q가 선분 F′P를 [[ratio(1, 3)]]으로 내분할 때, 삼각형 QF′R의 넓이를 [[frac(q,p)]]라 하자. 이때 [[q - 2p]]의 값을 구하시오. (단, [[p]], [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선(초점 F′·F), FF′을 지름으로 하는 원, 제1사분면 교점 P, 선분 F′P 위의 점 Q(왼쪽 가지), 선분 FQ 위의 점 R(오른쪽 가지), 선분 F′R"}}],
    confidence=0.8,
    note="[2024년 3월 고3 기하 30번 변형]. 프라임은 문장 속 라벨뿐(수식 기호 없음) — 텍스트 유지. 답 934 유지")

# 45. 8edbaa5c — 쌍곡선 p43: (가) AF < AF′ 윗줄 → seg(AF) < seg(AF'); '직선 MF′'은 텍스트
add(id="8edbaa5c", qtype="short",
    question="두 점 F, F′을 초점으로 하는 쌍곡선 [[frac(pow(x,2), 4) - frac(pow(y,2), 32) = 1]] 위의 점 A가 다음 조건을 만족시킨다.\n(가) [[seg(AF) < seg(AF')]]\n(나) 선분 AF의 수직이등분선은 점 F′을 지난다.\n선분 AF의 중점 M에 대하여 직선 MF′과 쌍곡선의 교점 중 점 A에 가까운 점을 B라 할 때, 삼각형 BFM의 둘레의 길이는 [[k]]이다. [[pow(k,2)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2022년 3월 고3 기하 29번/4점]. 조건 (가)의 윗줄 AF′을 seg(AF')로. 답 128 유지(둘레=MF′=8√2; 빠른정답 3과 불일치는 1차와 동일)")

# 46. 1d8d85d1 — 쌍곡선 p45: (가) PF′ = 24 윗줄 → seg(PF') = 24
add(id="1d8d85d1", qtype="short",
    question="점근선의 방정식이 [[y = pm(frac(3,4)) x]]이고 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선이 다음 조건을 만족시킨다.\n(가) 쌍곡선 위의 한 점 P에 대하여 [[seg(PF') = 24]], [[12 <= seg(PF) <= 16]]이다.\n(나) [[x]]좌표가 양수인 꼭짓점 A에 대하여 선분 AF의 길이는 자연수이다.\n이 쌍곡선의 주축의 길이를 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2016년 11월 고3 이과 28번 변형]. 윗줄 PF′=24를 seg(PF')로. 답 8 유지(k=1; 빠른정답 934와 불일치는 1차와 동일)")

# 47. d64e8a96 — 쌍곡선 p46: 프라임은 문장 속(직선 PF′, 선분 PF′)뿐 → 텍스트 유지, 그대로 통과
add(id="d64e8a96", qtype="choice",
    question="두 양수 [[a]], [[c]]에 대하여 두 점 [[F(c, 0)]], F′[[point(-c, 0)]]을 초점으로 하는 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 3) = 1]]이 있다. 두 직선 PF, PF′이 서로 수직이 되도록 하는 이 쌍곡선 위의 점 중 제1사분면 위의 점을 P, [[seg(PQ) = frac(a,3)]]인 선분 PF′ 위의 점을 Q라 하자. 직선 QF와 [[y]]축이 만나는 점을 A라 할 때, 점 A에서 두 직선 PF, PF′에 내린 수선의 발을 각각 R, S라 하자. [[seg(AR) = seg(AS)]]일 때, [[pow(a,2)]]의 값은?",
    choices=["[[frac(18,5)]]", "4", "[[frac(22,5)]]", "[[frac(24,5)]]", "[[frac(26,5)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/a²−y²/3=1(초점 F′·F), 제1사분면 점 P, 선분 PF′ 위의 점 Q, 직선 QF와 y축의 교점 A, A에서 직선 PF·PF′에 내린 수선의 발 R·S(직각 표시)"}}],
    confidence=0.85,
    note="[2024년 7월 고3 기하 28번/4점]. 프라임은 문장 속 라벨뿐 — 텍스트 유지, 수식은 이미 문법 안. 답 ④ 유지")

# 48. 09161aac — 쌍곡선 p47: 46번 원문항, 같은 처리
add(id="09161aac", qtype="short",
    question="점근선의 방정식이 [[y = pm(frac(4,3)) x]]이고 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선이 다음 조건을 만족시킨다.\n(가) 쌍곡선 위의 한 점 P에 대하여 [[seg(PF') = 30]], [[16 <= seg(PF) <= 20]]이다.\n(나) [[x]]좌표가 양수인 꼭짓점 A에 대하여 선분 AF의 길이는 자연수이다.\n이 쌍곡선의 주축의 길이를 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="[2016년 11월 고3 이과 28번/4점]. 윗줄 PF′=30을 seg(PF')로. 답 12 유지")

# 49. e46bd2b9 — 쌍곡선 p54: 46번과 같은 처리
add(id="e46bd2b9", qtype="choice",
    question="점근선의 방정식이 [[y = pm(frac(4 sqrt(2), 7)) x]]이고 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])인 쌍곡선이 다음 조건을 모두 만족시킨다.\n(가) 쌍곡선 위의 한 점 P에 대하여 [[seg(PF') = 30]], [[10 <= seg(PF) <= 20]]\n(나) [[x]]좌표가 양수인 꼭짓점 A에 대하여 선분 AF의 길이는 자연수이다.\n이때 이 쌍곡선의 주축의 길이는?",
    choices=["6", "8", "10", "12", "14"],
    figure=None, confidence=0.85,
    note="윗줄 PF′=30을 seg(PF')로. 답 ⑤ 유지(k=1 → 주축 14; 빠른정답 4와 불일치는 1차와 동일)")

# 50. e07f0839 — 쌍곡선 p63: PQ + PF′ 윗줄 → seg(PQ) + seg(PF')
add(id="e07f0839", qtype="short",
    question="그림과 같이 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])이고, 주축의 길이가 6인 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]]과 점 [[A(0, 5)]]를 중심으로 하고 반지름의 길이가 1인 원 [[C]]가 있다. 제1사분면에 있는 쌍곡선 위를 움직이는 점 P와 원 [[C]] 위를 움직이는 점 Q에 대하여 [[seg(PQ) + seg(PF')]]의 최솟값이 12일 때, [[pow(a,2) + 3 pow(b,2)]]의 값을 구하시오. (단, [[a]]와 [[b]]는 상수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/a²−y²/b²=1(초점 F′·F), y축 위 점 A 중심의 원 C와 그 위의 점 Q, 제1사분면 쌍곡선 위의 점 P, 선분 PQ·PF′"}}],
    confidence=0.85,
    note="[2018년 4월 고3 이과 28번/4점]. 윗줄 PF′을 seg(PF')로 한 식에. 답 54 유지(AF=7 → c²=24, b²=15)")

# 51. cd96eeb7 — 쌍곡선 p65: 50번 변형, 같은 처리
add(id="cd96eeb7", qtype="short",
    question="다음 그림과 같이 두 초점이 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])이고, 주축의 길이가 8인 쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), pow(b,2)) = 1]]과 점 [[A(0, 6)]]을 중심으로 하고 반지름의 길이가 2인 원 [[C]]가 있다.\n제1사분면에 있는 쌍곡선 위를 움직이는 점 P와 원 [[C]] 위를 움직이는 점 Q에 대하여 [[seg(PQ) + seg(PF')]]의 최솟값이 16일 때, [[pow(a,2) + 2 pow(b,2)]]의 값을 구하시오. (단, [[a]]와 [[b]]는 상수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/a²−y²/b²=1(초점 F′·F), y축 위 점 A 중심의 원 C와 그 위의 점 Q, 제1사분면 쌍곡선 위의 점 P, 선분 PQ·PF′"}}],
    confidence=0.85,
    note="[2018년 4월 고3 이과 28번 변형]. 윗줄 PF′을 seg(PF')로 한 식에. 답 112 유지(AF=10 → c²=64, b²=48)")

# 52. f16edb50 — 쌍곡선 p66: (단, PF′ < PF) 윗줄 → seg(PF') < seg(PF)
add(id="f16edb50", qtype="choice",
    question="다음 그림과 같이 쌍곡선 [[frac(pow(x,2), 25) - frac(pow(y,2), 16) = 1]]의 두 초점을 F, F′이라 하고, 이 쌍곡선 위의 점 P를 중심으로 하고 선분 PF′을 반지름으로 하는 원을 [[C]]라 하자.\n원 [[C]] 위를 움직이는 점 Q에 대하여 선분 FQ의 길이의 최댓값이 18일 때, 원 [[C]]의 넓이는? (단, [[seg(PF') < seg(PF)]])",
    choices=["[[4 pi]]", "[[9 pi]]", "[[16 pi]]", "[[25 pi]]", "[[36 pi]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선 x²/25−y²/16=1(초점 F′·F), 왼쪽 가지 위의 점 P를 중심으로 F′을 지나는 원 C, 원 위의 점 Q, 선분 FQ"}}],
    confidence=0.85,
    note="[2016년 6월 고3 이과 18번 변형]. 단서의 윗줄 PF′을 seg(PF')로. 답 ③ 유지(PF′=4 → 16π)")

# 53. 445eb9ed — 쌍곡선 p71: F′Q = 8, FP² + F′P², F′P < FP 윗줄 → seg(F'Q)·seg(F'P)
add(id="445eb9ed", qtype="short",
    question="다음 그림과 같이 두 초점이 F, F′인 쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), 16) = 1]] 위의 점 P에 대하여 직선 FP와 직선 F′P에 동시에 접하고 중심이 [[y]]축 위에 있는 원 [[C]]가 있다. 직선 F′P와 원 [[C]]의 접점 Q에 대하여 [[seg(F'Q) = 8]]일 때, [[pow(seg(FP), 2) + pow(seg(F'P), 2)]]의 값을 구하시오. (단, [[seg(F'P) < seg(FP)]])",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선(초점 F′·F), 왼쪽 가지 위의 점 P, 직선 FP·F′P에 접하고 중심이 y축 위인 원 C, 직선 F′P와 원의 접점 Q"}}],
    confidence=0.85,
    note="윗줄 F′Q·F′P를 seg(F'Q)·seg(F'P)로. 답 146 유지(FP=11, F′P=5)")

# 54. 61d36153 — 쌍곡선 p73: 프라임은 점 이름(F′, G′)뿐 → 텍스트 유지, 그대로 통과
add(id="61d36153", qtype="choice",
    question="그림과 같이 초점이 각각 F, F′과 G, G′이고, 주축의 길이가 2, 중심이 원점 O인 두 쌍곡선이 제1사분면에서 만나는 점을 P, 제3사분면에서 만나는 점을 Q라 하자. [[seg(PG) × seg(QG) = 8]], [[seg(PF) × seg(QF) = 4]]일 때, 사각형 PGQF의 둘레의 길이는?\n(단, 점 F의 [[x]]좌표와 점 G의 [[y]]좌표는 양수이다.)",
    choices=["[[6 + 2 sqrt(2)]]", "[[6 + 2 sqrt(3)]]", "10", "[[6 + 2 sqrt(5)]]", "[[6 + 2 sqrt(6)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 초점 F′·F(x축)인 쌍곡선과 초점 G·G′(y축)인 쌍곡선(꼭짓점 ±1), 제1사분면 교점 P, 제3사분면 교점 Q, 사각형 PGQF"}}],
    confidence=0.85,
    note="[2015년 6월 고3 이과 19번/4점]. 프라임은 단독 점 이름뿐(텍스트 허용), 수식은 이미 문법 안. 답 ④ 유지")

# 55. 51216d6b — 쌍곡선 p74: 53번과 같은 처리
add(id="51216d6b", qtype="short",
    question="그림과 같이 두 초점이 F, F′인 쌍곡선 [[frac(pow(x,2), 12) - frac(pow(y,2), 24) = 1]] 위의 점 P에 대하여 직선 FP와 직선 F′P에 동시에 접하고 중심이 [[y]]축 위에 있는 원 [[C]]가 있다. 직선 F′P와 원 [[C]]의 접점 Q에 대하여 [[seg(F'Q) = 5 sqrt(3)]]일 때, [[pow(seg(FP), 2) + pow(seg(F'P), 2)]]의 값을 구하시오. (단, [[seg(F'P) < seg(FP)]])",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선(초점 F′·F), 왼쪽 가지 위의 점 P, 직선 FP·F′P에 접하고 중심이 y축 위인 원 C, 직선 F′P와 원의 접점 Q"}}],
    confidence=0.85,
    note="윗줄 F′Q·F′P를 seg(F'Q)·seg(F'P)로. 답 174 유지(FP=7√3, F′P=3√3; 빠른정답 146과 불일치는 1차와 동일)")

# 56. ae9e548f — 쌍곡선 p77: PF′ − QF′ = 5 윗줄 → seg(PF') - seg(QF') = 5
add(id="ae9e548f", qtype="choice",
    question="그림과 같이 두 초점이 [[F(0, c)]], F′[[point(0, -c)]] ([[c > 0]])인 쌍곡선 [[frac(pow(x,2), 12) - frac(pow(y,2), 4) = -1]]이 있다. 쌍곡선 위의 제1사분면에 있는 점 P와 쌍곡선 위의 제3사분면에 있는 점 Q가 [[seg(PF') - seg(QF') = 5]], [[seg(PF) = frac(2,3) seg(QF)]]를 만족시킬 때, [[seg(PF) + seg(QF)]]의 값은?",
    choices=["10", "[[frac(35,3)]]", "[[frac(40,3)]]", "15", "[[frac(50,3)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: y축 위에 초점 F(위)·F′(아래)를 갖는 쌍곡선(위·아래 두 가지), 제1사분면 점 P(위 가지), 제3사분면 점 Q(아래 가지), 선분 PF·PF′·QF·QF′"}}],
    confidence=0.85,
    note="[2023년 3월 고3 기하 27번/3점]. 윗줄 PF′·QF′을 seg(PF')·seg(QF')로 한 식에. 답 ④ 유지(QF=9, PF=6)")

# 57. f4dcdb52 — 쌍곡선 p78: OF′ = OP, FQ : F′Q = 13 : 3, c²·PF′ 윗줄 → seg(OF')·ratio(seg(FQ), seg(F'Q))·pow(c,2) × seg(PF')
add(id="f4dcdb52", qtype="short",
    question="다음 그림과 같이 두 점 [[F(c, 0)]], F′[[point(-c, 0)]] ([[c > 0]])을 초점으로 하는 쌍곡선이 있다. 이 쌍곡선 위의 제2사분면에 있는 점 P와 이 쌍곡선 위의 제3사분면에 있는 점 Q에 대하여 직선 PQ가 점 F′를 지나고 [[seg(OF') = seg(OP)]]이다.\n세 점 P, F, Q를 지나는 원의 넓이가 [[frac(169,4) pi]]이고 [[ratio(seg(FQ), seg(F'Q)) = ratio(13, 3)]]일 때, [[pow(c,2) × seg(PF')]]의 값을 구하시오.\n(단, O는 원점이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선(초점 F′·F), 왼쪽 가지 위의 점 P(제2사분면)·Q(제3사분면), F′을 지나는 직선 PQ, 세 점 P·F·Q를 지나는 원"}}],
    confidence=0.85,
    note="[2025년 5월 고3 기하 29번 변형]. 윗줄 OF′·F′Q·PF′을 seg 라벨로(비는 ratio, 곱은 ×). 답 74 유지(a=5, PF′=2, c²=37)")

# 58. 64742f13 — 쌍곡선 p79: 53번과 같은 처리
add(id="64742f13", qtype="short",
    question="그림과 같이 두 초점이 F, F′인 쌍곡선 [[frac(pow(x,2), 8) - frac(pow(y,2), 17) = 1]] 위의 점 P에 대하여 직선 FP와 직선 F′P에 동시에 접하고 중심이 [[y]]축 위에 있는 원 [[C]]가 있다. 직선 F′P와 원 [[C]]의 접점 Q에 대하여 [[seg(F'Q) = 5 sqrt(2)]]일 때, [[pow(seg(FP), 2) + pow(seg(F'P), 2)]]의 값을 구하시오. (단, [[seg(F'P) < seg(FP)]])",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 쌍곡선(초점 F′·F), 왼쪽 가지 위의 점 P, 직선 FP·F′P에 접하고 중심이 y축 위인 원 C, 직선 F′P와 원의 접점 Q"}}],
    confidence=0.85,
    note="[2017년 11월 고3 이과 27번/4점]. 윗줄 F′Q·F′P를 seg(F'Q)·seg(F'P)로. 답 116 유지(FP=7√2, F′P=3√2; 빠른정답 68과 불일치는 1차와 동일)")

# 59. d7f18c94 — 쌍곡선 p80: |PF − PF′| → abs(seg(PF) - seg(PF'))
add(id="d7f18c94", qtype="choice",
    question="쌍곡선 [[frac(pow(x,2), pow(a,2)) - frac(pow(y,2), 15) = 1]]의 두 초점을 [[F(8, 0)]], F′[[point(-8, 0)]]이라 하자.\n쌍곡선 위의 점 P에 대하여 [[abs(seg(PF) - seg(PF'))]]의 값은?",
    choices=["10", "11", "12", "13", "14"],
    figure=None, confidence=0.85,
    note="[2017년 7월 고3 이과 7번 변형]. 절댓값·윗줄 PF′을 abs(seg(PF) - seg(PF'))로 한 식에. 답 ⑤ 유지(a²=49 → 14; 빠른정답 4와 불일치는 1차와 동일)")

# 60. cc9a62a5 — 쌍곡선 p81: |PF − PF′| = 4 → abs(seg(PF) - seg(PF')) = 4
add(id="cc9a62a5", qtype="choice",
    question="두 점 [[F(4, 3)]], F′[[point(-2, 3)]]에 대하여 [[abs(seg(PF) - seg(PF')) = 4]]를 만족시키는 점 P의 자취의 방정식은?",
    choices=["[[frac(pow(x - 1, 2), 4) - frac(pow(y - 3, 2), 5) = -1]]", "[[frac(pow(x - 1, 2), 4) - frac(pow(y - 3, 2), 5) = 1]]", "[[frac(pow(x - 1, 2), 4) + frac(pow(y - 3, 2), 5) = 1]]", "[[frac(pow(x - 1, 2), 5) - frac(pow(y - 3, 2), 4) = 1]]", "[[frac(pow(x - 1, 2), 5) - frac(pow(y - 3, 2), 4) = -1]]"],
    figure=None, confidence=0.85,
    note="절댓값·윗줄 PF′을 abs(seg(PF) - seg(PF')) = 4로 한 식에. 답 ② 유지")

# 61. 2104d5a6 — 쌍곡선 p82: 60번과 같은 처리
add(id="2104d5a6", qtype="choice",
    question="두 점 [[F(5, 0)]], F′[[point(-5, 0)]]에 대하여 점 P가 [[abs(seg(PF) - seg(PF')) = 4]]를 만족시킬 때, 점 P가 나타내는 도형의 방정식은?",
    choices=["[[frac(pow(x,2), 4) - frac(pow(y,2), 5) = 1]]", "[[frac(pow(x,2), 4) - frac(pow(y,2), 21) = 1]]", "[[frac(pow(x,2), 4) - frac(pow(y,2), 21) = -1]]", "[[frac(pow(x,2), 16) - frac(pow(y,2), 21) = 1]]", "[[frac(pow(x,2), 16) - frac(pow(y,2), 21) = -1]]"],
    figure=None, confidence=0.85,
    note="절댓값·윗줄 PF′을 abs(seg(PF) - seg(PF')) = 4로 한 식에. 답 ② 유지(빠른정답 116과 불일치는 1차와 동일)")

# 62. 2ffc5a15 — 쌍곡선 p93: 프라임은 문장 속(선분 F′P)뿐 → 텍스트 유지, 그대로 통과
add(id="2ffc5a15", qtype="choice",
    question="쌍곡선 [[frac(pow(x,2), 9) - frac(pow(y,2), 3) = 1]]의\n두 초점 [[point(2 sqrt(3), 0)]], [[point(-2 sqrt(3), 0)]]을 각각 F, F′이라 하자. 이 쌍곡선 위를 움직이는 점 [[P(x, y)]] ([[x > 0]])에 대하여 선분 F′P 위의 점 Q가 [[seg(FP) = seg(PQ)]]를 만족시킬 때, 점 Q가 나타내는 도형 전체의 길이는?",
    choices=["[[pi]]", "[[sqrt(3) pi]]", "[[2 pi]]", "[[3 pi]]", "[[2 sqrt(3) pi]]"],
    figure=None, confidence=0.85,
    note="[2006년 9월 고3 이과 9번]. 프라임은 문장 속 라벨뿐 — 텍스트 유지. 답 ③ 유지(F′Q=6, 중심각 π/3 → 2π; 빠른정답 5와 불일치는 1차와 동일)")

# 63. df09cc47 — 구의 방정식 p33: cos(∠N₁ON₂) → cos(angle(N1ON2))
add(id="df09cc47", qtype="choice",
    question="좌표공간에 두 점 [[A(a, 0, 0)]], [[B(0, 10 sqrt(2), 0)]]과 구 [[S]]: [[pow(x,2) + pow(y,2) + pow(z,2) = 100]]이 있다. [[angle(APO) = frac(pi,2)]]인 구 [[S]] 위의 모든 점 P가 나타내는 도형을 [[sub(C,1)]], [[angle(BQO) = frac(pi,2)]]인 구 [[S]] 위의 모든 점 Q가 나타내는 도형을 [[sub(C,2)]]라 하자. [[sub(C,1)]]과 [[sub(C,2)]]가 서로 다른 두 점 [[sub(N,1)]], [[sub(N,2)]]에서 만나고 [[cos(angle(N1ON2)) = frac(3,5)]]일 때, [[a]]의 값은?\n(단, [[a > 10 sqrt(2)]]이고, O는 원점이다.)",
    choices=["[[frac(10,3) sqrt(30)]]", "[[frac(15,4) sqrt(30)]]", "[[frac(25,6) sqrt(30)]]", "[[frac(55,12) sqrt(30)]]", "[[5 sqrt(30)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간: 원점 중심 구 S, x축 위의 점 A, y축 위의 점 B, 구 위의 점 P·Q, 구 위의 두 원 C₁·C₂(점선)"}}],
    confidence=0.85,
    note="[2024년 9월 고3 기하 28번/4점]. ∠N₁ON₂를 angle(N1ON2)로 cos 안에. 답 ① 유지(200/a²=3/5 → a=10√30/3; 빠른정답 5와 불일치는 1차와 동일)")

# 64. b7f4395c — 구의 방정식 p34: 63번 변형, 같은 처리
add(id="b7f4395c", qtype="choice",
    question="좌표공간에 두 점 [[A(a, 0, 0)]], [[B(0, 9, 0)]]과 구 [[S]]: [[pow(x,2) + pow(y,2) + pow(z,2) = 36]]이 있다. [[angle(APO) = frac(pi,2)]]인 구 [[S]] 위의 모든 점 P가 나타내는 도형을 [[sub(C,1)]], [[angle(BQO) = frac(pi,2)]]인 구 [[S]] 위의 모든 점 Q가 나타내는 도형을 [[sub(C,2)]]라 하자. [[sub(C,1)]]과 [[sub(C,2)]]가 서로 다른 두 점 [[sub(N,1)]], [[sub(N,2)]]에서 만나고 [[cos(angle(N1ON2)) = frac(5,9)]]일 때, [[a]]의 값은?\n(단, [[a > 9]]이고, O는 원점이다.)",
    choices=["[[4 sqrt(3)]]", "[[5 sqrt(3)]]", "[[6 sqrt(3)]]", "[[5 sqrt(5)]]", "[[6 sqrt(5)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표공간: 원점 중심 구 S, x축 위의 점 A, y축 위의 점 B, 구 위의 점 P·Q, 구 위의 두 원 C₁·C₂(점선)"}}],
    confidence=0.85,
    note="[2024년 9월 고3 기하 28번 변형]. ∠N₁ON₂를 angle(N1ON2)로 cos 안에. 답 ③ 유지(72/a²−1/9=5/9 → a=6√3; 빠른정답 4와 불일치는 1차와 동일)")

# ================= esc_sonnet_h3-3_3of6 =================
# 65. 7d0d6e11 — 평면과 구의 방정식 p28: OH→ · OH′→ → dot(vec(OH), vec(OH'))
add(id="7d0d6e11", qtype="short",
    question="좌표공간의 원점 O에서\n두 평면 [[alpha]]: [[2x - 4y - z - 11 = 0]],\n[[beta]]: [[3x - 3y + 2z - 14 = 0]]에 내린 수선의 발을 각각\nH, H′이라 할 때, [[dot(vec(OH), vec(OH'))]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="프라임 벡터 OH′→를 vec(OH')로 내적 안에. 답 16/3 유지(OH=(11/21)(2,−4,−1), OH′=(7/11)(3,−3,2))")

# 66. 5cd2052d — 평면과 구의 방정식 p99: 한 이미지에 별개 문항 2개(id 1개) — 첫째 문항만 전사, 보류 유지
add(id="5cd2052d", qtype="short",
    question="점 [[A(3, -2, -4)]]와 벡터 [[vec(n) = vcomp(2, -1, -2)]]에\n대하여 점 P가 [[dot(vec(AP), vec(n)) = 0]]을 만족시킬 때, 선분 OP의\n길이의 최솟값을 구하시오. (단, O는 원점이다.)",
    choices=None, figure=None, confidence=0.75,
    needs_review="이미지에 별개 문항 2개 인쇄(둘째: 좌표공간의 세 점 A, B, P의 위치벡터 a→, b→, x→에 대한 <보기> ㄱ. x→=b→+t(a→−b→)(t는 실수)의 자취는 두 점 A, B를 지나는 직선 / ㄴ. |x→−a→|=4의 자취는 A를 중심으로 하는 구 / ㄷ. (x→−a→)·(b→−a→)=0의 자취는 A를 지나고 직선 AB에 수직인 평면 — 선지 ①ㄱ ②ㄴ ③ㄱ,ㄴ ④ㄴ,ㄷ ⑤ㄱ,ㄴ,ㄷ, 답 ⑤)인데 id 1개 — 빠른정답 16/3에 대응하는 첫째 문항만 전사",
    note="문법은 이미 통과. 답 16/3 유지(평면 2x−y−2z−16=0과 원점의 거리)")

# 67. 8e5bf629 — 포물선 p16: F₁F₂ = 3 윗줄 → seg(F1F2) = 3; '선분 F₁F₂'는 sub 텍스트
add(id="8e5bf629", qtype="choice",
    question="두 양수 [[a]], [[p]]에 대하여 포물선 [[pow(y - a, 2) = 4 p x]]의 초점을 [[sub(F,1)]]이라 하고, 포물선 [[pow(y,2) = -4x]]의 초점을 [[sub(F,2)]]라 하자. 선분 [[sub(F,1)]][[sub(F,2)]]가 두 포물선과 만나는 점을 각각 P, Q라 할 때, [[seg(F1F2) = 3]], [[seg(PQ) = 1]]이다. [[pow(a,2) + pow(p,2)]]의 값은?",
    choices=["[[6]]", "[[frac(25,4)]]", "[[frac(13,2)]]", "[[frac(27,4)]]", "[[7]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 오른쪽으로 열린 포물선 (y−a)²=4px(초점 F₁)와 왼쪽으로 열린 포물선 y²=−4x(초점 F₂, x축 위), 선분 F₁F₂가 두 포물선과 만나는 점 P, Q"}}],
    confidence=0.85,
    note="[2021년 11월 고3 기하 28번/4점]. 윗줄 F₁F₂=3을 seg(F1F2)로, 문장 속 '선분 F₁F₂'는 sub 텍스트. 답 ⑤ 유지(p=1/2, a²=27/4 → 7; 빠른정답 90과 불일치는 1차와 동일)")

# 68. de779bd2 — 포물선 p18: AF₁ = AF₂ 윗줄 → seg(AF1) = seg(AF2)
add(id="de779bd2", qtype="choice",
    question="실수 [[p]] ([[p >= 1]])과 함수 [[f(x) = pow(x + a, 2)]]에 대하여\n두 포물선 [[sub(C,1)]]: [[pow(y,2) = 4x]], [[sub(C,2)]]: [[pow(y - 3, 2) = 4p (x - f(p))]]\n가 제1사분면에서 만나는 점을 A라 하자.\n두 포물선 [[sub(C,1)]], [[sub(C,2)]]의 초점을 각각 [[sub(F,1)]], [[sub(F,2)]]라 할 때,\n[[seg(AF1) = seg(AF2)]]를 만족시키는 [[p]]가 오직 하나가 되도록 하는\n상수 [[a]]의 값은?",
    choices=["[[-frac(3,4)]]", "[[-frac(5,8)]]", "[[-frac(1,2)]]", "[[-frac(3,8)]]", "[[-frac(1,4)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점을 꼭짓점으로 하는 포물선 C₁(초점 F₁, x축 위)과 오른쪽으로 열린 포물선 C₂(초점 F₂), 제1사분면 교점 A"}}],
    confidence=0.85,
    note="[2022년 9월 고3 기하 28번/4점]. 윗줄 AF₁=AF₂를 seg(AF1) = seg(AF2)로. 답 ① 유지(f(p)=p−1의 판별식 0 → a=−3/4)")

# 69. 994fc2da — 포물선 p22: 프라임은 점 이름 F′(문장 속)뿐 → 텍스트 유지, 그대로 통과
add(id="994fc2da", qtype="short",
    question="초점이 F인 포물선 [[pow(y,2) = 12x]] 위의 점 중 제1사분면에 있는 점 P를 지나고 [[x]]축과 평행한 직선이 포물선 [[pow(y,2) = 12x]]의 준선과 만나는 점을 F′이라 하자. 점 F′을 초점, 점 P를 꼭짓점으로 하는 포물선이 포물선 [[pow(y,2) = 12x]]와 만나는 점 중 P가 아닌 점을 Q라 하자. 사각형 PF′QF의 둘레의 길이가 16일 때, 삼각형 PF′Q의 넓이는 [[frac(q,p) sqrt(3)]]이다. [[p + q]]의 값을 구하시오. (단, 점 P의 [[x]]좌표는 3보다 작고, [[p]]와 [[q]]는 서로소인 자연수이다.)",
    choices=None,
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 포물선 y²=12x, 초점 F, 준선 위의 점 F′, 포물선 위의 점 P(제1사분면)·Q, 삼각형 PF′Q 음영, 사각형 PF′QF"}}],
    confidence=0.8,
    note="[2022년 6월 고3 기하 29번 변형]. 프라임은 단독 점 이름·문장 속 라벨뿐 — 텍스트 유지. 답 39 유지(재검산: P(1, 2√3), Q(1/49, −2√3/7), 둘레 16 성립, 넓이 32√3/7)")

# 70. 5972d747 — 포물선 p25: 68번 변형, 같은 처리
add(id="5972d747", qtype="choice",
    question="실수 [[p]] ([[p > 1]])과 함수 [[f(x) = pow(x + 2a, 2)]]에 대하여\n두 포물선\n[[sub(C,1)]]: [[pow(y,2) = 12x]], [[sub(C,2)]]: [[pow(y - 4, 2) = 12p (x - f(p))]]가\n제1사분면에서 만나는 점을 A라 하자.\n두 포물선 [[sub(C,1)]], [[sub(C,2)]]의 초점을 각각 [[sub(F,1)]], [[sub(F,2)]]라 할 때,\n[[seg(AF1) = seg(AF2)]]를 만족시키는 [[p]]가 오직 하나가 되도록 하는\n상수 [[a]]의 값은?",
    choices=["[[-frac(5,16)]]", "[[-frac(1,4)]]", "[[-frac(3,16)]]", "[[-frac(1,8)]]", "[[-frac(1,16)]]"],
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 원점을 꼭짓점으로 하는 포물선 C₁(초점 F₁, x축 위)과 오른쪽으로 열린 포물선 C₂(초점 F₂), 제1사분면 교점 A"}}],
    confidence=0.85,
    note="[2022년 9월 고3 기하 28번 변형]. 윗줄 AF₁=AF₂를 seg(AF1) = seg(AF2)로. 답 ④ 유지(f(p)=3p−3의 판별식 0 → a=−1/8; 빠른정답 39와 불일치는 1차와 동일)")

# 71. c74ce72c — 포물선 p52: FP₁ + FP₂ + FP₃ = 27 윗줄 → seg(FP1) + seg(FP2) + seg(FP3) = 27
add(id="c74ce72c", qtype="choice",
    question="양수 [[p]]에 대하여 좌표평면 위에 초점이 F인\n포물선 [[pow(y,2) = 4 p x]]가 있다.\n이 포물선이 세 직선 [[x = p]], [[x = 2p]], [[x = 3p]]와 만나는\n제1사분면 위의 점을 각각 [[sub(P,1)]], [[sub(P,2)]], [[sub(P,3)]]이라 하자.\n[[seg(FP1) + seg(FP2) + seg(FP3) = 27]]일 때, [[p]]의 값은?",
    choices=["[[2]]", "[[frac(5,2)]]", "[[3]]", "[[frac(7,2)]]", "[[4]]"],
    figure=None, confidence=0.85,
    note="[2023년 9월 고3 기하 27번/3점]. 윗줄 FP₁+FP₂+FP₃=27을 seg 라벨 한 식으로. 답 ③ 유지(9p=27)")

# 72. 0aa529b3 — 정사영 p11: A′B′ = 3 윗줄 → seg(A'B') = 3; '선분 A′B′'은 텍스트
add(id="0aa529b3", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB와 평면 [[alpha]]가 이루는 각의 크기를 [[theta]]라 하자.\n[[seg(A'B') = 3]], [[theta = deg(60)]]일 때, 선분 AB의 길이를 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="윗줄 A′B′=3을 seg(A'B')로. 답 6 유지(3/cos 60°)")

# 73. d8ed08f7 — 정사영 p12: 프라임은 문장 속(선분 A′B′)뿐 → 텍스트 유지, 그대로 통과
add(id="d8ed08f7", qtype="choice",
    question="선분 A′B′은 길이가 6인 선분 AB의 평면 [[alpha]] 위로의\n정사영이고, 직선 AB와 평면 [[alpha]]가 이루는 각의 크기가\n[[deg(30)]]일 때, 선분 A′B′의 길이는?",
    choices=["[[sqrt(2)]]", "[[2]]", "[[3]]", "[[3 sqrt(2)]]", "[[3 sqrt(3)]]"],
    figure=None, confidence=0.85,
    note="프라임은 문장 속 라벨(선분 A′B′)뿐 — 텍스트 유지, 수식 없음. 답 ⑤ 유지(6cos 30°=3√3)")

# 74. 11c1449e — 정사영 p13: A′B′ = 8√2 윗줄 → seg(A'B') = 8 sqrt(2)
add(id="11c1449e", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB가 평면 [[alpha]]와 이루는 각의 크기를 [[theta]]라 하자.\n[[seg(A'B') = 8 sqrt(2)]], [[theta = deg(45)]]일 때, 선분 AB의 길이를\n구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="윗줄 A′B′=8√2를 seg(A'B')로. 답 16 유지(8√2/cos 45°; 빠른정답 3과 불일치는 1차와 동일)")

# 75. 9eb87782 — 정사영 p14: A′B′ = 7 윗줄 → seg(A'B') = 7
add(id="9eb87782", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB와 평면 [[alpha]]가 이루는 예각의 크기를 [[theta]]라 하자.\n[[theta = deg(60)]], [[seg(A'B') = 7]]일 때, 선분 AB의 길이를 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="윗줄 A′B′=7을 seg(A'B')로. 답 14 유지(7/cos 60°; 빠른정답 6과 불일치는 1차와 동일)")

# 76. c54bccaf — 정사영 p57: A′B′ = 3 윗줄 → seg(A'B') = 3
add(id="c54bccaf", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB와 평면 [[alpha]]가 이루는 예각의 크기를 [[theta]]라 하자.\n[[seg(AB) = 12]], [[seg(A'B') = 3]]일 때, [[cos(theta)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="윗줄 A′B′=3을 seg(A'B')로. 답 1/4 유지")

# 77. 52eea367 — 정사영 p59: A′B′ = 8 윗줄 → seg(A'B') = 8
add(id="52eea367", qtype="short",
    question="선분 AB의 평면 [[alpha]] 위로의 정사영을 선분 A′B′이라 하고,\n직선 AB와 평면 [[alpha]]가 이루는 예각의 크기를 [[theta]]라고 하면,\n[[seg(AB) = 12]], [[seg(A'B') = 8]]일 때, [[cos(theta)]]의 값을 구하시오.",
    choices=None, figure=None, confidence=0.85,
    note="윗줄 A′B′=8을 seg(A'B')로. 답 2/3 유지")
