# -*- coding: utf-8 -*-
# batch10 (50문항, 모두 중3: esc_sonnet_m3-1_3of6 4 · m3-1_4of6 5 · m3-1_5of6 2 · m3-2_1of6 2 · m3-2_3of6 10 · m3-2_4of6 20 · m3-2_5of6 7) — v1.5 문법 재작업
# 핵심 교체: 프라임 라벨 → seg(QG')·seg(OO')·tri(A'BC')·quad(GOHO')·angle(QBO')·angle(PO'C)·angle(BAT')·angle(CBT')·angle(TPT')·angle(AOB')·ray(PT')·arc(AT')·line(TT')
#            빈칸 (가)(나)(다) → box(1)~(3) (p40 풀이 과정의 (나)°는 deg(box(2))) / 줄임표 → cdots (l₁²+⋯+l₈², 무한 연분수 최내측 분모)
#            '직선 TT′'·'원 O′'·'B′지점'처럼 단독 점 이름만 있는 문항은 텍스트 그대로(교체 없음) → 도형 unsupported(raw)만 남아 통과
#            ○× 2지 판정형 2건은 선지를 본문 텍스트로 둔 short형으로 통과(답 ② 유지)
# 여전히 보류(10): 한 이미지에 별개 문항 2개(id 1개) 6건(bf92a8db, 8f0caeab, e627d40a, 35311c9f, 1c5f71e1, 6805bd8a) / 답 기호 ㉡·㉢ 2건(d679e9af, 3b755ae4) / 사용자 정의 기호 <a, b>·◎ 2건(defa43ac, 343af482)
ITEMS = []
def add(**kw): ITEMS.append(kw)

# ================= esc_sonnet_m3-1_3of6 =================
# 0. adfb907b — 3of6 seq 1 (통과): 선지 2개(○× 판정형, 5지 규격 밖) — 보기를 본문에 텍스트로 포함 — 2x³−x²+4x=0 삼차 → 이차방정식 아님 →
add(id='adfb907b', qtype='short',
    question="다음 식이 이차방정식이면 '○'를, 아니면 '×'를 고르시오.\n[[pow(x,2) - 4x = 2 pow(x,3)]]\n① ○ ② ×",
    choices=None,
    figure=None,
    confidence=0.85,
    note='○× 2지 판정형(5지 규격 밖): 선지 ①○ ②×를 본문 텍스트로 두고 short형으로 통과(문법 문제 없음). 2x³−x²+4x=0은 삼차 → × → 답 ② 유지(빠른정답 ✓)')

# 1. bf92a8db — 3of6 seq 99 (보류 유지): 이미지에 별개 문항 2개(id 1개): 첫 문항만 전사 — 둘째 문항(이차방정식 5x²−(4a+3)x−5=0의 한 근 x=k에
add(id='bf92a8db', qtype='short',
    question='이차방정식 [[5 pow(x,2) + x - 1 = 0]]의 두 근을 [[alpha]], [[beta]]라 하고\n[[f(n) = pow(alpha, n) + pow(beta, n)]]이라 할 때,\n[[5f(n + 2) + f(n + 1) - f(n)]]의 값을 구하시오.\n(단, [[n]]은 자연수이다.)',
    choices=None,
    figure=None,
    confidence=0.75, needs_review='같은 이미지에 별개 문항 2개(id 1개) — 위 문항만 전사; 아래 문항: 이차방정식 5x²−(4a+3)x−5=0의 한 근 x=k에 대하여 k−1/k=a가 성립한다. 이때 상수 a의 값은? ①1 ②2 ③3 ④4 ⑤5 (답 ③)',
    note='문법 문제 없음(v1.5 교체 불필요). 답 0 유지(빠른정답 1과 불일치는 1차와 동일)')

# 2. 620bdeb9 — 3of6 seq 5 (통과): 문법 범위 밖: 무한 연분수(줄임표 ⋯가 최내측 분모 안에 있어 frac 중첩으로 표기 불가) — 텍스트 혼합 표기 / (참고
add(id='620bdeb9', qtype='short',
    question='[[5 + frac(6, 5 + frac(6, 5 + frac(6, 5 + cdots)))]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.85,
    note="무한 연분수: 최내측 분모의 줄임표를 cdots 상수로 써서 frac 3중 중첩 한 식으로 표기(이미지와 같은 깊이). x=5+6/x → x=6, 답 6 유지(빠른정답 '심우각형'은 정렬 오류)")

# 3. d679e9af — 3of6 seq 41 (보류 유지): 도형 표현 불가: ㉠~㉣ 포물선 4개 그래프 / 답 기호 ㉡이 답 문법 범위 밖이라 답 미도출 처리 — −a>0 아래로 볼록,
add(id='d679e9af', qtype='short',
    question='[[a < 0]], [[q < 0]]일 때, ㉠~㉣ 중 [[y = -a pow(x,2) + q]]의 그래프로\n알맞은 것을 고르시오. (단, [[a]], [[q]]는 상수)',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '좌표평면 위 포물선 4개(원점 O): ㉠ 초록, 아래로 볼록, 꼭짓점이 y축의 양의 부분 ㉡ 보라, 아래로 볼록, 꼭짓점이 y축의 음의 부분 ㉢ 빨강, 위로 볼록, 꼭짓점이 y축의 양의 부분 ㉣ 하늘색, 위로 볼록, 꼭짓점이 y축의 음의 부분'}}],
    confidence=0.75, needs_review='답 기호 ㉡이 답 문법(ㄱㄴㄷ·①~⑤) 범위 밖이라 answer 미기재(−a>0 아래로 볼록, q<0 → 꼭짓점이 y축 음의 부분인 ㉡) / 선지가 ㉠~㉣ 포물선 그래프라 정보가 그림에만 있음',
    note='문법 문제 없음. 도형은 unsupported(raw) 유지')

# ================= esc_sonnet_m3-1_4of6 =================
# 4. 8f0caeab — 4of6 seq 99 (보류 유지): 이미지에 별개 문항 2개 인쇄(id 1개) — draft_a 대응인 아래쪽 선택형 문항만 전사; 위쪽 문항 '이차방정식 2x²
add(id='8f0caeab', qtype='choice',
    question='이차방정식 [[pow(x,2) - x - 6 = 0]]의 두 근 중 작은 근이 이차방정식 [[2 pow(x,2) + b x - 2 = 0]]의 근이라고 할 때, [[b]]의 값은?',
    choices=['[[-3]]', '[[-1]]', '[[1]]', '[[2]]', '[[3]]'],
    figure=None,
    confidence=0.75, needs_review='같은 이미지에 별개 문항 2개(id 1개) — 아래 선택형 문항만 전사; 위 문항: 이차방정식 2x²−13x+15=0의 두 근 중에서 큰 근이 3x²−11x+a=0의 근이라 할 때, a의 값을 구하시오. (답 −20)',
    note='문법 문제 없음. 답 ⑤ 유지(빠른정답 1과 불일치는 1차와 동일)')

# 5. 3b755ae4 — 4of6 seq 2 (보류 유지): 문법 범위 밖: 답 '㉢'(원문자 기호)은 answer 문법에서 허용되지 않아 미기입 — ㉢에서 2(x+1)²−2−1이어야 하
add(id='3b755ae4', qtype='short',
    question='[[y = 2 pow(x,2) + 4x - 1]]을 [[y = a pow(x - p, 2) + q]]의 꼴로 고치는 과정 중 처음 틀린 곳을 찾으시오.\n[[y = 2 pow(x,2) + 4x - 1]]\n= [[2(pow(x,2) + 2x) - 1]] ⋯㉠\n= [[2(pow(x,2) + 2x + 1 - 1) - 1]] ⋯㉡\n= [[2 pow(x + 1, 2) - 3 - 1]] ⋯㉢\n= [[2 pow(x + 1, 2) - 4]] ⋯㉣',
    choices=None,
    figure=None,
    confidence=0.75, needs_review="답 '㉢'(원문자 기호)이 답 문법 범위 밖이라 answer 미기재 — ㉢에서 2(x+1)²−2−1이어야 하는데 −3−1로 씀(처음 틀린 곳 ㉢)",
    note='문법 문제 없음(⋯㉠ 등 줄 표지는 텍스트)')

# 6. defa43ac — 4of6 seq 49 (보류 유지): 문법 범위 밖: 약속 기호 <a, b>(사이 점의 개수)는 텍스트 혼합 / 도형 표현 불가: 수직선 위 제곱근 점 나열 / (
add(id='defa43ac', qtype='short',
    question='자연수의 양의 제곱근 1, [[sqrt(2)]], [[sqrt(3)]], 2, ⋯에 대응하는 점을 수직선 위에 다음 그림과 같이 차례대로 나타낸다. 아래 수직선에서 [[a]], [[b]] 사이에 있는 점의 개수를 <[[a]], [[b]]>라 하면 <1, 2> = 2, <2, 3> = 4이다. 이때 <2000, 2001>의 값을 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '수직선 위에 점 1, √2, √3, 2, √5, √6, √7, √8, 3이 차례로 찍혀 있음(√6, √8은 위쪽에 표기)'}}],
    confidence=0.75, needs_review='문법 범위 밖: 약속 기호 <a, b>(a, b 사이에 있는 점의 개수) — v1.5에도 대응 표기 없음, 텍스트 혼합 유지',
    note='수직선 도형은 unsupported(raw). 답 4000 유지(빠른정답 1과 불일치는 1차와 동일)')

# 7. 1c1cb285 — 4of6 seq 63 (통과): 선지 2개(○× 판정형, 5지 규격 밖) — 보기를 본문에 텍스트로 포함 / (참고) 빠른정답 불일치: 전사·풀이 답 ② vs
add(id='1c1cb285', qtype='short',
    question="다음 설명이 옳으면 '○'를, 옳지 않으면 '×'를 고르시오.\n이차함수 [[y = 3 pow(x - frac(2,3), 2) + frac(1,3)]]의 그래프는 [[x > frac(2,3)]]일 때, [[x]]의 값이 증가하면 [[y]]의 값은 감소한다.\n① ○ ② ×",
    choices=None,
    figure=None,
    confidence=0.85,
    note='○× 2지 판정형(5지 규격 밖): 선지 ①○ ②×를 본문 텍스트로 두고 short형으로 통과(문법 문제 없음). 아래로 볼록·축 x=2/3 오른쪽은 증가 → × → 답 ② 유지(빠른정답 1과 불일치는 1차와 동일)')

# 8. 343af482 — 4of6 seq 91 (보류 유지): 문법 범위 밖: 사용자 정의 연산 ◎ → 텍스트 혼합 전사 — (3x−1)◎(x+2)=3x²+3x+1=k → D=9−12(1−
add(id='343af482', qtype='choice',
    question='두 실수 [[a]], [[b]]에 대하여 [[a]]◎[[b]] = [[-a + b + a b]]일 때, ([[3x - 1]])◎([[x + 2]]) = [[k]]가 근을 갖도록 하는 상수 [[k]]의 값 중 가장 작은 값은?',
    choices=['[[-frac(1,2)]]', '[[-frac(1,4)]]', '[[0]]', '[[frac(1,4)]]', '[[frac(1,2)]]'],
    figure=None,
    confidence=0.75, needs_review='문법 범위 밖: 사용자 정의 이항연산 ◎ — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지',
    note='답 ④ 유지(빠른정답 ✓)')

# ================= esc_sonnet_m3-1_5of6 =================
# 9. 9e7bb6c5 — 5of6 seq 66 (통과): 프라임 점 라벨 G′: seg(QG′)를 [[seg(QG)]]′로 텍스트 혼합 / 도형 표현 불가: 정사각뿔 입체 도형(무게중
add(id='9e7bb6c5', qtype='short',
    question="다음 그림과 같이 밑면이 정사각형이고 옆면이 정삼각형인 사각뿔 A−BCDE가 있다. [[tri(ACD)]]의 무게중심을 G, [[tri(ADE)]]의 무게중심을 G′이라 하자. 모서리 CD 위의 점 P와 모서리 DE 위의 점 Q에 대하여 [[seg(GP) + seg(PQ) + seg(QG')]]의 길이의 최솟값이 [[6 sqrt(2) + 2 sqrt(6)]]일 때, 사각뿔 A−BCDE의 한 모서리의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '정사각뿔 A−BCDE(꼭짓점 A 위, 밑면 정사각형 BCDE: B 뒤 왼쪽, C 앞 왼쪽, D 앞, E 오른쪽), 면 ACD 위의 무게중심 G, 면 ADE 위의 무게중심 G′, 모서리 CD 위의 점 P, 모서리 DE 위의 점 Q, 선분 GP·PQ·QG′'}}],
    confidence=0.85,
    note="프라임 라벨 QG′을 seg(QG')로 써서 GP+PQ+QG′을 한 식으로 연결. 답 12 유지(빠른정답 3과 불일치는 1차와 동일)")

# 10. 2daff16c — 5of6 seq 67 (통과): 프라임 점 라벨 G′: seg(QG′)를 [[seg(QG)]]′로 텍스트 혼합 / 도형 표현 불가: 정사각뿔 입체 도형(무게중
add(id='2daff16c', qtype='short',
    question="다음 그림과 같이 밑면이 정사각형이고 옆면이 정삼각형인 사각뿔 A−BCDE가 있다. [[tri(ACD)]]의 무게중심을 G, [[tri(ADE)]]의 무게중심을 G′이라 하자. 모서리 CD 위의 점 P와 모서리 DE 위의 점 Q에 대하여 [[seg(GP) + seg(PQ) + seg(QG')]]의 길이의 최솟값이 [[3(3 sqrt(2) + sqrt(6))]]일 때, 사각뿔 A−BCDE의 한 모서리의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '정사각뿔 A−BCDE(꼭짓점 A 위, 밑면 정사각형 BCDE: B 뒤 왼쪽, C 앞 왼쪽, D 앞, E 오른쪽), 면 ACD 위의 무게중심 G, 면 ADE 위의 무게중심 G′, 모서리 CD 위의 점 P, 모서리 DE 위의 점 Q, 선분 GP·PQ·QG′'}}],
    confidence=0.85,
    note="프라임 라벨 QG′을 seg(QG')로 써서 GP+PQ+QG′을 한 식으로 연결. 답 18 유지(빠른정답 ✓)")

# ================= esc_sonnet_m3-2_1of6 =================
# 11. 809efd24 — 1of6 seq 10 (통과): 도형 표현 불가: 삼각형 도형 / 프라임 점 라벨(A′, C′) — 0.6×1.4=0.84 → 16% 감소 → ④ = 빠른정답
add(id='809efd24', qtype='choice',
    question="다음 그림과 같은 [[tri(ABC)]]에서 한 변의 길이는 [[pct(40)]] 줄이고, 다른 한 변의 길이는 [[pct(40)]] 늘여서 새로운 삼각형 A′BC′를 만들 때, [[tri(A'BC')]]의 넓이의 변화는?",
    choices=['변함없다.', '[[pct(4)]] 줄어든다.', '[[pct(4)]] 늘어난다.', '[[pct(16)]] 줄어든다.', '[[pct(16)]] 늘어난다.'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '직각삼각형 ABC(A 위, B 좌하, C 우하) 색칠(분홍). A′는 BA 위(A보다 아래), C′는 BC 연장선 위(C 오른쪽), 점선 A′C′·CC′'}}],
    confidence=0.85,
    note="△A′BC′을 tri(A'BC')로('삼각형 A′BC′'는 원문 그대로 텍스트). 답 ④ 유지(빠른정답 ✓)")

# 12. e627d40a — 1of6 seq 99 (보류 유지): 도형 표현 불가: 사각형+평행사변형 복합 도형 / 이미지에 별개 문항 2개(id 1개): 아래쪽 '사각형 ABCD의 넓이(대각
add(id='e627d40a', qtype='choice',
    question='다음은 두 대각선의 길이가 [[p]], [[q]]이고 두 대각선이 이루는 예각의 크기가 [[x]]인 사각형의 넓이를 구하는 과정이다. (가), (나)에 알맞은 것을 차례로 쓴 것은?\n[[quad(ABCD)]]의 각 꼭짓점을 지나고 두 대각선에 각각 평행한 직선을 그어 [[quad(EFGH)]]를 만들면\n[[quad(ABCD) = box(1) quad(EFGH) = frac(1,2) p q box(2)]]',
    choices=['[[frac(1,4)]], [[sin(x)]]', '[[frac(1,4)]], [[cos(x)]]', '[[frac(1,2)]], [[sin(x)]]', '[[frac(1,2)]], [[cos(x)]]', '[[1]], [[sin(x)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '사각형 ABCD(색칠, 보라)의 대각선 AC=q, BD=p(점선 치수), 이루는 각 x. 각 꼭짓점을 지나 대각선에 평행한 직선으로 만든 평행사변형 EFGH(E 위, F 좌, G 아래, H 우), EF=q, FG=p, ∠F=x 표시, 평행 화살표 표시. 아래 상자에 (가)(나) 풀이 과정'}}],
    confidence=0.75, needs_review='같은 이미지에 별개 문항 2개(id 1개) — 위 문항만 전사; 아래 문항: 다음 그림과 같은 사각형 ABCD의 넓이를 구하면?(두 대각선 6, 8, 이루는 각 60°) 선지 ①12√3 ②11√3 ③10√3 ④9√3 ⑤8√3 (답 ①)',
    note='빈칸 (가)(나)를 box(1)·box(2)로 한 식에 연결. 답 ③ 유지(빠른정답 ✓)')

# ================= esc_sonnet_m3-2_3of6 =================
# 13. 35311c9f — 3of6 seq 99 (보류 유지): 도형 표현 불가: 원+내접삼각형+수선 도형 / 이미지 하단에 별개 문항(OM=ON, AB=12cm, ∠BAC=60°인 원 O에
add(id='35311c9f', qtype='short',
    question='다음 그림의 원 O에서 [[perp(seg(AB), seg(OD))]], [[perp(seg(BC), seg(OE))]], [[perp(seg(CA), seg(OF))]]이고 [[seg(OD) = seg(OE) = seg(OF)]]이다. [[seg(AC) = 7]] cm일 때, [[tri(ABC)]]의 둘레의 길이를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O에 내접하는 삼각형 ABC(A 좌상, B 좌하, C 우). O에서 AB·BC·CA에 내린 수선의 발 D·E·F(직각 표시), OD=OE=OF(같은 길이 표시). AC=7cm(점선 치수)'}}],
    confidence=0.75, needs_review='같은 이미지에 별개 문항 2개(id 1개) — 위 문항만 전사; 아래 문항: 원 O의 중심에서 두 현 AB, AC에 내린 수선의 발 M, N에 대하여 OM=ON, AB=12cm, ∠BAC=60°일 때 옳지 않은 것은? ①AC=12cm ②AM=6cm ③∠OBM=30° ④OB=4√2cm ⑤△OMB=6√3cm²',
    note='문법 문제 없음. 답 21 cm 유지(빠른정답 없음, 풀이 답)')

# 14. 433c3ae8 — 3of6 seq 80 (통과): 도형 표현 불가: 직사각형+대각선+내접원 2개 도형 / 프라임 점 라벨(O′) — a+b=17, r=2 → AC=13, AB·
add(id='433c3ae8', qtype='choice',
    question="다음 그림과 같은 직사각형 ABCD의 둘레의 길이는 34 cm이고 두 원 O, O′은 각각 [[tri(ABC)]], [[tri(ACD)]]의 내접원이다. 두 원의 반지름의 길이가 2 cm로 같고 점 G, H는 각각 두 원 O, O′과 [[seg(AC)]]의 접점일 때, [[quad(GOHO')]]의 넓이는?",
    choices=['11 cm²', '12 cm²', '13 cm²', '14 cm²', '15 cm²'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '가로로 긴 직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상)와 대각선 AC. 삼각형 ABC의 내접원 O(왼쪽 아래)·삼각형 ACD의 내접원 O′(오른쪽 위). AC와의 접점 G(O 쪽)·H(O′ 쪽). 사각형 GOHO′ 음영'}}],
    confidence=0.85,
    note="□GOHO′을 quad(GOHO')로. 답 ④ 유지(빠른정답 ✓)")

# 15. 5f6aa547 — 3of6 seq 17 (통과): 도형 표현 불가: 두 원+공통접선 도형 / 프라임 점 라벨(O′) / (참고) 빠른정답 불일치: 전사·풀이 답 deg(48) 
add(id='5f6aa547', qtype='short',
    question="다음 그림에서 [[seg(AB)]], [[seg(PQ)]]는 두 원 O, O′의 공통인 접선이고, 세 점 A, B, Q는 접점이다. [[angle(PAQ) = deg(48)]]일 때, [[angle(QBO')]]의 크기를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '왼쪽 원 O(작은 원)와 오른쪽 원 O′(큰 원)이 점 Q에서 외접. 위쪽 공통접선 AB(A는 원 O의 접점, B는 원 O′의 접점), Q에서의 공통접선 PQ(P는 AB 위). 선분 AQ·BQ·BO′. ∠PAQ=48°'}}],
    confidence=0.85,
    note="∠QBO′을 angle(QBO')로. 답 deg(48) 유지(빠른정답 48 ✓)")

# 16. bbf17cd4 — 3of6 seq 22 (통과): 도형 표현 불가: 두 원+공통접선 도형 / 프라임 점 라벨(O′) / (참고) 빠른정답 불일치: 전사·풀이 답 ④ vs 빠른정
add(id='bbf17cd4', qtype='choice',
    question='다음 그림에서 [[seg(PQ)]]와 [[seg(TR)]]는 두 원 O, O′의 공통인 접선이고 세 점 P, Q, R는 접점이다. [[angle(RPT) = deg(39)]]일 때, [[angle(TQR)]]의 크기는?',
    choices=['[[deg(42)]]', '[[deg(45)]]', '[[deg(48)]]', '[[deg(51)]]', '[[deg(54)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '왼쪽 큰 원 O와 오른쪽 작은 원 O′이 점 R에서 외접. 아래쪽 공통접선 PQ(P는 원 O의 접점, Q는 원 O′의 접점), R에서의 공통접선 TR(T는 PQ 위). 선분 PR·QR. ∠RPT=39°, ∠TQR 부분 음영'}}],
    confidence=0.85,
    note='프라임은 원 이름 O′(단독 점 이름, 텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 ④ 유지(빠른정답 50과 불일치는 1차와 동일)')

# 17. 354ac045 — 3of6 seq 24 (통과): 도형 표현 불가: 두 원+공통접선 도형 / 프라임 점 라벨(O′) / (참고) 빠른정답 불일치: 전사·풀이 답 ④ vs 빠른정
add(id='354ac045', qtype='choice',
    question='다음 그림과 같이 두 원 O, O′이 직선 PT와 점 T에서 각각 접하고 직선 AB가 두 원 O, O′의 공통인 접선일 때, 다음 중 옳지 않은 것은?',
    choices=['[[seg(PA) = seg(PT)]]', '[[seg(PA) = frac(1,2) seg(AB)]]', '[[angle(PTB) = angle(PBT)]]', '[[angle(PAT) = deg(60)]]', '[[angle(ATB) = deg(90)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '왼쪽 원 O와 오른쪽 원 O′이 점 T에서 외접, T에서의 공통접선(세로 직선 PT). 위쪽 공통접선 AB(A는 원 O의 접점, B는 원 O′의 접점, P는 AB 위). 선분 AT·BT'}}],
    confidence=0.85,
    note='프라임은 원 이름 O′(단독 점 이름, 텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 ④ 유지(빠른정답 5와 불일치는 1차와 동일)')

# 18. 45084433 — 3of6 seq 40 (통과): 도형 표현 불가: 두 원+접선+현 복합 도형 / 프라임 점 라벨(O′) / (참고) 빠른정답 불일치: 전사·풀이 답 ③ vs 
add(id='45084433', qtype='choice',
    question='그림과 같이 선분 AB를 지름으로 하는 원 O와 선분 AB 위의 점 C에 대하여 선분 BC를 지름으로 하는 원 O′이 있다. 점 A에서 원 O′에 그은 두 접선이 원 O′과 만나는 점을 각각 D, E라 하고, 원 O와 만나는 점을 각각 F, G라 하자. 다음은 두 선분 DE, AB의 교점을 H라 하고 [[angle(DAE) = deg(40)]]일 때, [[angle(FHG)]]의 크기를 구하는 과정이다.\n원 O′의 중심을 I라 할 때,\n[[angle(DFB) = angle(DHB) = deg(90)]] …… ㉠\n선분 DB는 공통인 변 …… ㉡\n[[angle(DIH) = box(1) × angle(DBH)]]이고\n[[par(seg(DI), seg(FB))]]이므로\n[[angle(DBF) = angle(DBH)]] …… ㉢\n㉠, ㉡, ㉢에 의해 [[cong(tri(DFB), tri(DHB))]]이다.\n한편, [[seg(AD) = seg(AE)]]이므로 [[angle(ADH) = deg(box(2))]]\n[[angle(DHF) = frac(1,2) × deg(box(2))]]\n따라서 [[angle(FHG) = deg(box(3))]]이다.\n위의 (가), (나), (다)에 알맞은 수를 각각 [[a]], [[b]], [[c]]라 할 때, [[frac(a c, b)]]의 값은?',
    choices=['[[frac(18,7)]]', '[[frac(20,7)]]', '[[frac(22,7)]]', '[[frac(24,7)]]', '[[frac(26,7)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 O(지름 AB, A 위·B 아래)와 그 안에서 B에서 내접하는 작은 원 O′(지름 BC, C는 AB 위). A에서 원 O′에 그은 두 접선(접점 D 좌·E 우)이 원 O와 F(좌하)·G(우하)에서 만남. 현 DE와 AB의 교점 H. 선분 DB·EB·FH·GH·FB·GB. ∠DAE=40°'}}],
    confidence=0.85,
    note='[2017년 3월 고1 20번/4점]. 빈칸 (가)(나)(다)를 box(1)~box(3)으로 식 안에 연결((나)°는 deg(box(2))); 프라임은 원 이름 O′(텍스트)뿐. 답 ③ 유지(빠른정답 4와 불일치는 1차와 동일)')

# 19. 9aca8659 — 3of6 seq 40 (통과): 도형 표현 불가: 두 원+접선+현 복합 도형 / 프라임 점 라벨(O′) / (참고) 빠른정답 불일치: 전사·풀이 답 ③ vs 
add(id='9aca8659', qtype='choice',
    question='그림과 같이 선분 AB를 지름으로 하는 원 O와 선분 AB 위의 점 C에 대하여 선분 BC를 지름으로 하는 원 O′이 있다. 점 A에서 원 O′에 그은 두 접선이 원 O′과 만나는 점을 각각 D, E라 하고, 원 O와 만나는 점을 각각 F, G라 하자. 다음은 두 선분 DE, AB의 교점을 H라 하고 [[angle(DAE) = deg(40)]]일 때, [[angle(FHG)]]의 크기를 구하는 과정이다.\n원 O′의 중심을 I라 할 때,\n[[angle(DFB) = angle(DHB) = deg(90)]] …… ㉠\n선분 DB는 공통인 변 …… ㉡\n[[angle(DIH) = box(1) × angle(DBH)]]이고\n[[par(seg(DI), seg(FB))]]이므로\n[[angle(DBF) = angle(DBH)]] …… ㉢\n㉠, ㉡, ㉢에 의해 [[cong(tri(DFB), tri(DHB))]]이다.\n한편, [[seg(AD) = seg(AE)]]이므로 [[angle(ADH) = deg(box(2))]]\n[[angle(DHF) = frac(1,2) × deg(box(2))]]\n따라서 [[angle(FHG) = deg(box(3))]]이다.\n위의 (가), (나), (다)에 알맞은 수를 각각 [[a]], [[b]], [[c]]라 할 때, [[frac(a c, b)]]의 값은?',
    choices=['[[frac(18,7)]]', '[[frac(20,7)]]', '[[frac(22,7)]]', '[[frac(24,7)]]', '[[frac(26,7)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 O(지름 AB, A 위·B 아래)와 그 안에서 B에서 내접하는 작은 원 O′(지름 BC, C는 AB 위). A에서 원 O′에 그은 두 접선(접점 D 좌·E 우)이 원 O와 F(좌하)·G(우하)에서 만남. 현 DE와 AB의 교점 H. 선분 DB·EB·FH·GH·FB·GB. ∠DAE=40°'}}],
    confidence=0.85,
    note='[2017년 3월 고1 20번/4점]. 빈칸 (가)(나)(다)를 box(1)~box(3)으로 식 안에 연결((나)°는 deg(box(2))); 프라임은 원 이름 O′(텍스트)뿐. 답 ③ 유지(빠른정답 4와 불일치는 1차와 동일)')

# 20. 15cf7055 — 3of6 seq 64 (통과): 도형 표현 불가: 삼각형+내접원+방접원 도형 / 프라임 점 라벨(O′) / (참고) 빠른정답 불일치: 전사·풀이 답 15 cm
add(id='15cf7055', qtype='short',
    question="다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이고 점 D, E, F는 접접이다. 또, 원 O′은 [[seg(AB)]], [[seg(BC)]]의 연장선과 각각 점 P, Q에서 접하고 [[seg(AC)]]와 점 H에서 접한다. 두 원 O, O′의 반지름의 길이는 각각 3 cm, 11 cm이고 [[seg(OO') = 17]] cm일 때, [[seg(AC)]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '각 B(좌하)에서 뻗은 두 반직선 사이에 삼각형 ABC(A 좌상, C 우하). 작은 내접원 O(접점 D(AB)·E(BC)·F(AC)), 큰 원 O′이 AB의 연장선 P·BC의 연장선 Q·AC의 H에서 접함. 선분 OO′=17cm(점선 치수), O′Q=11cm, OE=3cm'}}],
    confidence=0.85,
    note="원문 '접접이다' 그대로. 윗줄 OO′=17cm를 seg(OO') = 17로. 답 15 cm 유지(빠른정답 4와 불일치는 1차와 동일)")

# 21. 971a1014 — 3of6 seq 65 (통과): 도형 표현 불가: 삼각형+내접원+방접원 도형 / 프라임 점 라벨(O′) / (참고) 빠른정답 불일치: 전사·풀이 답 12 cm
add(id='971a1014', qtype='short',
    question="다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이고 점 D, E, F는 접접이다. 또, 원 O′은 [[seg(AB)]], [[seg(BC)]]의 연장선과 각각 점 P, Q에서 접하고 [[seg(AC)]]와 점 H에서 접한다. 두 원 O, O′의 반지름의 길이는 각각 2 cm, 11 cm이고 [[seg(OO') = 15]] cm일 때, [[seg(AC)]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '각 B(좌하)에서 뻗은 두 반직선 사이에 작은 삼각형 ABC. 작은 내접원 O(접점 D(AB)·E(BC)·F(AC)), 큰 원 O′이 AB의 연장선 P·BC의 연장선 Q·AC의 H에서 접함. OO′=15cm(점선 치수), O′Q=11cm, OE=2cm'}}],
    confidence=0.85,
    note="원문 '접접이다' 그대로. 윗줄 OO′=15cm를 seg(OO') = 15로. 답 12 cm 유지(빠른정답 4와 불일치는 1차와 동일)")

# 22. 530975c8 — 3of6 seq 66 (통과): 도형 표현 불가: 삼각형+내접원+방접원 도형 / 프라임 점 라벨(O′) / (참고) 빠른정답 불일치: 전사·풀이 답 24 cm
add(id='530975c8', qtype='short',
    question="다음 그림에서 원 O는 [[tri(ABC)]]의 내접원이고 점 D, E, F는 접접이다. 또, 원 O′은 [[seg(AB)]], [[seg(BC)]]의 연장선과 각각 점 P, Q에서 접하고 [[seg(AC)]]와 점 H에서 접한다. 두 원 O, O′의 반지름의 길이는 각각 6 cm, 16 cm이고 [[seg(OO') = 26]] cm일 때, [[seg(AC)]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '각 B(좌하)에서 뻗은 두 반직선 사이에 삼각형 ABC. 작은 내접원 O(접점 D(AB)·E(BC)·F(AC)), 큰 원 O′이 AB의 연장선 P·BC의 연장선 Q·AC의 H에서 접함. OO′=26cm(점선 치수), O′Q=16cm, OE=6cm'}}],
    confidence=0.85,
    note="원문 '접접이다' 그대로. 윗줄 OO′=26cm를 seg(OO') = 26으로. 답 24 cm 유지(빠른정답 3과 불일치는 1차와 동일)")

# ================= esc_sonnet_m3-2_4of6 =================
# 23. 595aa80d — 4of6 seq 64 (통과): 도형 표현 불가: 두 원+내접사각형 2개 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(87) 
add(id='595aa80d', qtype='short',
    question='다음 그림의 두 원 O, O′에서 [[angle(x)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 직선 A-P-D(위), 직선 B-Q-C-R(아래). 선분 AB, DC. ∠x=∠ABQ(B), ∠PDC=92°(D), ∠DCR=87°(C 외각)'}}],
    confidence=0.85,
    note='프라임은 원 이름 O′(텍스트)뿐이라 교체 없음; 도형은 unsupported(raw, 92°·87° 포함). 답 deg(87) 유지(빠른정답 230과 불일치는 1차와 동일)')

# 24. 516ff14a — 4of6 seq 65 (통과): 도형 표현 불가: 두 원+내접사각형 2개+중심각 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 ⑤ vs
add(id='516ff14a', qtype='choice',
    question="다음 그림에서 두 점 P, Q는 두 원 O, O′의 교점이다. [[angle(BAP) = deg(100)]]일 때, [[angle(PDC) + angle(PO'C)]]의 크기는?",
    choices=['[[deg(220)]]', '[[deg(225)]]', '[[deg(230)]]', '[[deg(235)]]', '[[deg(240)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 직선 A-P-D(위), 선분 AB, BQ, QC, CD. ∠BAP=100°(A), O′에서 O′P, O′C와 ∠PO′C 표시(Q쪽)'}}],
    confidence=0.85,
    note="∠PDC+∠PO′C를 angle(PDC) + angle(PO'C)로. 답 ⑤ 유지(빠른정답 218과 불일치는 1차와 동일)")

# 25. 761ba37e — 4of6 seq 66 (통과): 도형 표현 불가: 두 원+내접사각형 2개+중심각 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(
add(id='761ba37e', qtype='short',
    question='다음 그림과 같이 두 원 O, O′이 두 점 P, Q에서 만나고 [[angle(PDC) = deg(100)]]일 때, [[angle(x) + angle(y)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 선분 AB, AP, PD, DC, BQ, QC, PQ. 반지름 OB, OP. ∠x=∠BOP(O, Q쪽 표시), ∠y=∠PQB(Q), ∠PDC=100°(D)'}}],
    confidence=0.85,
    note='프라임은 원 이름 O′(텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 deg(260) 유지(빠른정답 120과 불일치는 1차와 동일)')

# 26. 4bcc5ade — 4of6 seq 68 (통과): 도형 표현 불가: 두 원+내접사각형 2개+중심각 도형 / 프라임 점 라벨 — ∠PQC=92 → ∠PDC=88 → ∠PO′C=1
add(id='4bcc5ade', qtype='choice',
    question="다음 그림에서 두 원 O, O′이 두 점 P, Q에서 만날 때, 두 점 P, Q를 지나는 직선이 두 원 O, O′과 만나는 점을 A, B, C, D라 하자. [[angle(A) = deg(92)]]일 때, [[angle(PO'C)]]의 크기는?",
    choices=['[[deg(172)]]', '[[deg(173)]]', '[[deg(174)]]', '[[deg(175)]]', '[[deg(176)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 직선 A-P-D(위), B-Q-C(아래), 선분 AB, DC. ∠A=92°, O′에서 O′P, O′C와 ∠PO′C 표시(Q쪽)'}}],
    confidence=0.85,
    note="∠PO′C를 angle(PO'C)로(원문 문장 그대로). 답 ⑤ 유지(빠른정답 ✓)")

# 27. 5c7181a9 — 4of6 seq 69 (통과): 도형 표현 불가: 두 원+내접사각형 2개+중심각 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 ④ vs
add(id='5c7181a9', qtype='choice',
    question="다음 그림에서 두 점 P, Q는 두 원 O, O′의 교점이다. [[angle(BAP) = deg(95)]]일 때, [[angle(PDC) + angle(PO'C)]]의 크기는?",
    choices=['[[deg(240)]]', '[[deg(245)]]', '[[deg(250)]]', '[[deg(255)]]', '[[deg(260)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '두 원 O(왼쪽), O′(오른쪽)이 두 점 P(위), Q(아래)에서 만남. 직선 A-P-D(위), 선분 AB, BQ, QC, CD. ∠BAP=95°(A), ∠D 표시, O′에서 O′P, O′C와 ∠PO′C 표시'}}],
    confidence=0.85,
    note="∠PDC+∠PO′C를 angle(PDC) + angle(PO'C)로. 답 ④ 유지(빠른정답 260과 불일치는 1차와 동일)")

# 28. e01ff95d — 4of6 seq 1 (통과): 도형 표현 불가: 원+접선+삼각형 도형 / 프라임 점 라벨 — ∠ACB=∠ABT=60 → 호 AB=120, 호 BC=40 → 
add(id='e01ff95d', qtype='choice',
    question='다음 그림에서 직선 TT′은 원의 접선이고 점 B는 접점이다. [[arc(AB) = 3 arc(BC)]]이고 [[angle(ABT) = deg(60)]]일 때, [[angle(CAB)]]의 크기는?',
    choices=['[[deg(16)]]', '[[deg(17)]]', '[[deg(18)]]', '[[deg(19)]]', '[[deg(20)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '원, 아래쪽 접선 T-B-T′(B 접점, T 왼쪽, T′ 오른쪽). 원 위의 점 A(왼쪽 위), C(오른쪽 아래). 현 AB, AC, BC. ∠ABT=60°(B 왼쪽), ∠CAB 표시(A)'}}],
    confidence=0.85,
    note="프라임은 '직선 TT′'(원문에 선 기호 없음, 텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 ⑤ 유지(빠른정답 ✓)")

# 29. f1dc9f5c — 4of6 seq 16 (통과): 도형 표현 불가: 원+접선+삼각형+중심각 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(120)
add(id='f1dc9f5c', qtype='short',
    question='다음 그림에서 직선 TT′이 원의 접선이고 점 B가 그 접점이다. [[angle(CBT) = deg(60)]]일 때, [[angle(x)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O, 아래쪽 접선 T-B-T′(B 접점, T 왼쪽, T′ 오른쪽). 원 위의 점 A(왼쪽 위), C(오른쪽 위). 현 AB, AC, BC. 반지름 OB, OC. 60°는 B에서 BC와 BT′ 사이에 표시, ∠x=∠BOC(O)'}}],
    confidence=0.85,
    note="프라임은 '직선 TT′'(원문에 선 기호 없음, 텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 원문 ∠CBT=60°(그림은 BC와 BT′ 사이) 그대로. 답 deg(120) 유지(빠른정답 72와 불일치는 1차와 동일)")

# 30. 8026f55d — 4of6 seq 20 (통과): 도형 표현 불가: 원+접선+중심각+원주각 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(15) 
add(id='8026f55d', qtype='short',
    question='다음 그림에서 직선 TT′이 원 O의 접선이고 점 P가 접점일 때, [[angle(CBP)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O, 위쪽 접선 T-P-T′(P 접점). 원 위의 점 C(왼쪽 위), A(오른쪽 위), B(왼쪽 아래). 선분 PA, PB, BC, BA, OA, OC. ∠APT′=25°, ∠AOC=80°(O), ∠x=∠CBP(B)'}}],
    confidence=0.85,
    note="프라임은 '직선 TT′'(원문에 선 기호 없음, 텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 deg(15) 유지(빠른정답 33과 불일치는 1차와 동일)")

# 31. 30728dbc — 4of6 seq 22 (통과): 도형 표현 불가: 원+접선+중심각+삼각형 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 ④ vs 빠른정
add(id='30728dbc', qtype='choice',
    question="다음 그림에서 직선 TT′은 원 O의 접선이고 점 A는 접점이다. [[angle(BOC) = deg(144)]], [[angle(BAT') = deg(72)]]일 때, [[angle(ABC)]]의 크기는?",
    choices=['[[deg(33)]]', '[[deg(34)]]', '[[deg(35)]]', '[[deg(36)]]', '[[deg(37)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O, 아래쪽 접선 T-A-T′(A 접점). 원 위의 점 B(오른쪽 위), C(왼쪽). 현 AB, AC, BC, 반지름 OB, OC. ∠BOC=144°(O), ∠BAT′=72°'}}],
    confidence=0.85,
    note="∠BAT′=72°를 angle(BAT') = deg(72)로. 답 ④ 유지(빠른정답 52와 불일치는 1차와 동일)")

# 32. a2c7ddff — 4of6 seq 25 (통과): 도형 표현 불가: 원+접선+중심각+삼각형 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 ① vs 빠른정
add(id='a2c7ddff', qtype='choice',
    question="다음 그림에서 직선 TT′은 원 O의 접선이고 점 A는 접점이다. [[angle(BOC) = deg(142)]], [[angle(BAT') = deg(70)]]일 때, [[angle(ABC)]]의 크기는?",
    choices=['[[deg(39)]]', '[[deg(40)]]', '[[deg(41)]]', '[[deg(42)]]', '[[deg(43)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O, 아래쪽 접선 T-A-T′(A 접점). 원 위의 점 B(오른쪽 위), C(왼쪽). 현 AB, AC, BC, 반지름 OB, OC. ∠BOC=142°(O), ∠BAT′=70°'}}],
    confidence=0.85,
    note="∠BAT′=70°를 angle(BAT') = deg(70)로. 답 ① 유지(빠른정답 4와 불일치는 1차와 동일)")

# 33. 3f5a1067 — 4of6 seq 52 (통과): 도형 표현 불가: 원+접선+지름 도형 / 프라임 점 라벨 — ∠BPA=90, ∠PAB=45 → ∠BPT=∠PAB=45 → ② 
add(id='3f5a1067', qtype='choice',
    question='다음 그림에서 직선 TT′이 원 O의 접선이고, 점 P는 원의 접점일 때, [[angle(BPT)]]의 크기는?',
    choices=['[[deg(40)]]', '[[deg(45)]]', '[[deg(50)]]', '[[deg(55)]]', '[[deg(60)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O, 위쪽 접선 T-P-T′(P 접점, T 왼쪽, T′ 오른쪽). 지름 BA(B 왼쪽, A 오른쪽, O 지남). 현 BP. ∠PBA=45°(B)'}}],
    confidence=0.85,
    note="프라임은 '직선 TT′'(원문에 선 기호 없음, 텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 ② 유지(빠른정답 ✓)")

# 34. 1d1a17f0 — 4of6 seq 58 (통과): 도형 표현 불가: 원+접선+지름 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(29) vs 빠른
add(id='1d1a17f0', qtype='short',
    question="다음 그림에서 직선 TT′이 원의 접선이고 점 B가 접점이다. [[angle(CBT') = deg(61)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O, 오른쪽의 기울어진 접선 T-B-T′(B 접점, T′ 위, T 아래). 원 위의 점 C(위), A(아래), 지름 CA(O 지남). 현 CB, AB. ∠CBT′=61°, ∠x=∠ACB(C)'}}],
    confidence=0.85,
    note="∠CBT′=61°를 angle(CBT') = deg(61)로. 답 deg(29) 유지(빠른정답 2와 불일치는 1차와 동일)")

# 35. 3eb7db79 — 4of6 seq 69 (통과): 도형 표현 불가: 원+두 접선+삼각형 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 ④ vs 빠른정답 
add(id='3eb7db79', qtype='choice',
    question="다음 그림에서 [[ray(PT)]], [[ray(PT')]]은 원의 접선이고 두 점 T, T′은 접점이다. [[arc(AT) = arc(AT')]]이고 [[angle(TPT') = deg(32)]]일 때, [[angle(x)]]의 크기는?",
    choices=['[[deg(50)]]', '[[deg(51)]]', '[[deg(52)]]', '[[deg(53)]]', '[[deg(54)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 P(왼쪽)에서 원에 그은 두 접선(접점 T 위, T′ 아래). 원 위의 점 A(오른쪽). 현 TT′, TA, T′A. AT=AT′(같은 길이 표시). ∠TPT′=32°, ∠x=∠AT′T(T′)'}}],
    confidence=0.85,
    note="반직선 PT′→ray(PT'), 호 AT′→arc(AT'), ∠TPT′→angle(TPT')로. 답 ④ 유지(빠른정답 60과 불일치는 1차와 동일)")

# 36. f41cdcd9 — 4of6 seq 72 (통과): 도형 표현 불가: 두 원+접선+두 할선 도형 / 프라임 점 라벨 — ∠ABP=∠ACD=67 → ∠APT=∠ABP=67 → ② 
add(id='f41cdcd9', qtype='choice',
    question='다음 그림에서 [[line(PT)]]가 원 O의 접선이고, 두 점 A, B는 두 원의 교점이다. [[ray(PA)]], [[ray(PB)]]와 원 O′이 만나는 점을 각각 C, D라 할 때, [[angle(APT)]]의 크기는?',
    choices=['[[deg(66)]]', '[[deg(67)]]', '[[deg(68)]]', '[[deg(69)]]', '[[deg(70)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '작은 원 O(왼쪽 아래)와 큰 원 O′(오른쪽 위)이 두 점 A, B에서 만남. 원 O 위의 점 P(왼쪽 아래)에서의 접선(T는 P 왼쪽 위). 반직선 P-A-C, P-B-D. 선분 CD. ∠ACD=67°(C), ∠BDC=72°(D)'}}],
    confidence=0.85,
    note='프라임은 원 이름 O′(텍스트)뿐이라 교체 없음(직선 PT·반직선 PA, PB는 이미 line/ray); 도형은 unsupported(raw). 답 ② 유지(빠른정답 ✓)')

# 37. 68d8f579 — 4of6 seq 76 (통과): 도형 표현 불가: 외접하는 두 원+공통접선 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(36)
add(id='68d8f579', qtype='short',
    question='다음 그림에서 직선 PQ가 두 원 O, O′의 공통인 접선이고 점 T가 접점일 때, [[angle(DCT)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 T에서 외접하는 두 원 O(왼쪽), O′(오른쪽)과 T에서의 공통접선 P-T-Q(세로, P 위, Q 아래). 직선 A-T-C, B-T-D. 왼쪽 원 위의 A(위), B(아래), 오른쪽 원 위의 D(위), C(아래). 선분 AB, DC. ∠BAT=36°(A), ∠TDC=80°(D), ∠DCT 표시'}}],
    confidence=0.85,
    note='프라임은 원 이름 O′(텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 deg(36) 유지(빠른정답 37과 불일치는 1차와 동일)')

# 38. 37912684 — 4of6 seq 78 (통과): 도형 표현 불가: 외접하는 두 원+공통접선 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(39)
add(id='37912684', qtype='short',
    question='다음 그림에서 직선 PQ가 두 원 O, O′의 공통인 접선이고 점 T가 접점일 때, [[angle(BTQ)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 T에서 외접하는 두 원 O(왼쪽), O′(오른쪽)과 T에서의 공통접선 P-T-Q(세로, P 위, Q 아래). 직선 A-T-C, B-T-D. 왼쪽 원 위의 A(위), B(아래), 오른쪽 원 위의 D(위), C(아래). 선분 AB, DC. ∠BAT=39°(A), ∠TDC=68°(D)'}}],
    confidence=0.85,
    note='프라임은 원 이름 O′(텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 deg(39) 유지(빠른정답 60과 불일치는 1차와 동일)')

# 39. 2fd13393 — 4of6 seq 81 (통과): 도형 표현 불가: 외접하는 두 원+공통접선 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(60)
add(id='2fd13393', qtype='short',
    question='다음 그림과 같이 점 P에서 외접하는 두 원 O, O′에서 [[angle(PAC) = deg(80)]], [[angle(PDB) = deg(40)]]일 때, [[angle(BPD)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 P에서 외접하는 두 원 O(왼쪽, 큰 원), O′(오른쪽). P에서의 공통접선(세로, T 아래). 직선 A-P-B, C-P-D. 왼쪽 원 위의 A(위), C(왼쪽 아래), 오른쪽 원 위의 D(오른쪽 위), B(아래). 선분 AC, DB. ∠PAC=80°, ∠PDB=40°, ∠BPD 표시'}}],
    confidence=0.85,
    note='프라임은 원 이름 O′(텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 답 deg(60) 유지(빠른정답 ✓)')

# 40. 084d585c — 4of6 seq 85 (통과): 도형 표현 불가: 외접하는 두 원+공통접선 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(60)
add(id='084d585c', qtype='short',
    question='다음 그림과 같이 점 P에서 외접하는 두 원이 있다. [[line(ST)]]는 원 O와 원 O′ 위의 점 P에 접하는 접선이고 [[angle(BAP) = deg(62)]], [[angle(CPD) = deg(58)]]일 때, [[angle(PDC)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 P에서 외접하는 두 원 O(왼쪽), O′(오른쪽)과 P에서의 공통접선 S-P-T(세로, S 위, T 아래). 직선 A-P-C, B-P-D. 왼쪽 원 위의 A(위), B(아래), 오른쪽 원 위의 D(위), C(아래). 선분 AB, DC. ∠BAP=62°, ∠CPD=58°, ∠PDC 표시'}}],
    confidence=0.85,
    note="프라임은 원 이름 O′(텍스트)뿐이라 교체 없음(직선 ST는 line(ST)); 도형은 unsupported(raw). 답 deg(60) 유지(빠른정답 '4, 5'와 불일치는 1차와 동일)")

# 41. 87dde9e5 — 4of6 seq 86 (통과): 도형 표현 불가: 두 원(내접)+접선+현 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 ② vs 빠른정
add(id='87dde9e5', qtype='choice',
    question="다음 그림에서 직선 TT′은 점 A에서 두 원과 접하고 큰 원의 현 BC는 작은 원과 점 D에서 접한다.\n[[angle(CBA) = deg(20)]], [[angle(BAT') = deg(60)]]일 때, [[angle(y) - angle(x)]]의 크기는?",
    choices=['[[deg(5)]]', '[[deg(10)]]', '[[deg(15)]]', '[[deg(20)]]', '[[deg(25)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '아래쪽 직선 T-A-T′에 점 A에서 접하는 큰 원과 작은 원(작은 원은 큰 원 안). 큰 원의 현 BC(B 오른쪽 위, C 왼쪽 아래)가 작은 원과 D에서 접함. 선분 AB, AC, AD. ∠CBA=20°, ∠BAT′=60°, ∠x=∠CAD(A), ∠y=∠ACB(C)'}}],
    confidence=0.85,
    note="∠BAT′=60°를 angle(BAT') = deg(60)로. 답 ② 유지(빠른정답 136과 불일치는 1차와 동일)")

# 42. 1353d3ad — 4of6 seq 90 (통과): 도형 표현 불가: 두 원(내접)+접선+현 도형 / 프라임 점 라벨 / (참고) 빠른정답 불일치: 전사·풀이 답 deg(22) 
add(id='1353d3ad', qtype='short',
    question="다음 그림에서 직선 TT′은 점 A에서 두 원과 접하고 큰 원의 현 BC는 작은 원과 점 D에서 접한다.\n[[angle(CBA) = deg(20)]], [[angle(BAT') = deg(68)]]일 때, [[angle(y) - angle(x)]]의 크기를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '아래쪽 직선 T-A-T′에 점 A에서 접하는 큰 원과 작은 원(작은 원은 큰 원 안). 큰 원의 현 BC(B 오른쪽 위, C 왼쪽 아래)가 작은 원과 D에서 접함. 선분 AB, AC, AD. ∠CBA=20°, ∠BAT′=68°, ∠x=∠CAD(A), ∠y=∠ACB(C)'}}],
    confidence=0.85,
    note="∠BAT′=68°를 angle(BAT') = deg(68)로. 답 deg(22) 유지(빠른정답 2와 불일치는 1차와 동일)")

# ================= esc_sonnet_m3-2_5of6 =================
# 43. fef007fd — 5of6 seq 97 (통과): 프라임 점 라벨(T′) / 도형 표현 불가: 내접하는 두 원+접선 도형 — △PBD∽△PAC → BD:AC=PB:PA이므로 ⑤
add(id='fef007fd', qtype='choice',
    question='아래 그림에서 점 P는 두 원의 접점이고 직선 TT′은 점 P를 지나는 접선이다. 다음 중 옳지 않은 것은?',
    choices=['[[angle(PDB) = angle(PCA)]]', '[[angle(BPT) = angle(ACP)]]', '[[angle(BPT) = angle(BDP)]]', '[[par(seg(AC), seg(BD))]]', '[[ratio(seg(BD), seg(AC)) = ratio(seg(AB), seg(BP))]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 안에 작은 원이 점 P(우)에서 내접, P를 지나는 접선 TT′(T 위, T′ 아래). 큰 원 위 A(좌상)·C(좌하), 작은 원 위 B(선분 AP 위)·D(선분 CP 위). 선분 AC·BD·AP·CP'}}],
    confidence=0.85,
    note="프라임은 '직선 TT′'(원문에 선 기호 없음, 텍스트)뿐이라 교체 없음; 도형은 unsupported(raw). 선지의 ∠·윗줄·비는 이미 문법 표기. 답 ⑤ 유지(빠른정답 ✓)")

# 44. 31e9960c — 5of6 seq 98 (통과): 프라임 점 라벨(T′) / 도형 표현 불가: 내접하는 두 원+공통 접선 도형 / (참고) 빠른정답 불일치: 전사·풀이 답 de
add(id='31e9960c', qtype='short',
    question="다음 그림에서 [[line(TT')]]은 두 원의 공통인 접선이다. [[angle(CAP) = deg(40)]], [[angle(BDC) = deg(100)]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 안에 작은 원이 점 P(우)에서 내접, 세로 접선 TT′(T 위, T′ 아래). 큰 원 위 A(좌)·C(아래), 작은 원 위 B(선분 AP 위)·D(선분 CP 위). 선분 AC·BD. ∠CAP=40°(A), ∠BDC=100°(D), x(P, ∠BPD)'}}],
    confidence=0.85,
    note="원문 TT′ 위 직선 기호(양쪽 화살표)를 line(TT')로. 답 deg(60) 유지(빠른정답 2와 불일치는 1차와 동일)")

# 45. 1c5f71e1 — 5of6 seq 99 (보류 유지): 한 쪽에 별개 문항 2개, id 1개 — 위 문항만 전사(아래 문항: 반지름 5·10인 두 원 O·O′이 점 P에서 접하고 원
add(id='1c5f71e1', qtype='short',
    question='다음 그림과 같이 두 원이 점 A에서 접하고 있다. 작은 원 위의 점 D에서 접하는 직선이 큰 원과 만나는 점을 각각 B, C라 하면 [[seg(AB) = 6]] cm, [[seg(BC) = 5]] cm, [[seg(AC) = 4]] cm일 때, [[seg(CD)]]의 길이를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 안에 작은 원이 점 A(우상)에서 내접. 큰 원 위 B(좌)·C(아래), 작은 원 위 D(BC 위, 접점). 삼각형 ABC와 선분 AD. AB=6cm, BC=5cm, AC=4cm(호 모양 점선 치수)'}}],
    confidence=0.75, needs_review='같은 이미지에 별개 문항 2개(id 1개) — 위 문항만 전사; 아래 문항: 반지름의 길이가 각각 5, 10인 두 원 O, O′이 점 P에서 접하고 원 O′의 두 현 PA, PB가 원 O와 만나는 점을 각각 C, D라 할 때 □ACDB의 넓이는 △PDC의 넓이의 몇 배인가? ①2배 ②5/2배 ③3배 ④7/2배 ⑤4배 (답 ③)',
    note='문법 문제 없음. 답 2 cm 유지(빠른정답 3은 아래 문항의 답 ③과 일치)')

# 46. b02e8608 — 5of6 seq 96 (통과): 첨자 점 라벨(선분 P₀Pₖ의 윗줄 표기를 seg로 표현 불가, 텍스트 '선분'으로 대체) / 도형 표현 불가: 원 위 16등
add(id='b02e8608', qtype='choice',
    question='다음 그림과 같이 지름의 길이가 2인 원 O 위에 16개의 점이 같은 간격으로 놓여 있고, 이 점을 각각 [[sub(P,0)]], [[sub(P,1)]], [[sub(P,2)]], ⋯, [[sub(P,15)]]라 하자. 선분 [[sub(P,0)]][[sub(P,k)]] ([[k]] = 1, 2, 3, ⋯, 8)의 길이를 [[sub(l,k)]]라 할 때, [[pow(sub(l,1),2) + pow(sub(l,2),2) + pow(sub(l,3),2) + cdots + pow(sub(l,8),2)]]의 값은?',
    choices=['[[12]]', '[[14]]', '[[16]]', '[[18]]', '[[20]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 O 위에 같은 간격의 점 16개. P₀(우), P₁(우상), P_k(위), P₈(좌). 지름 P₀P₈=2(점선 치수), 선분 P₀P_k=l_k(점선 표시)'}}],
    confidence=0.85,
    note="가변 첨자 점 라벨 P₀Pₖ(윗줄)는 seg로 못 써서 '선분 [[sub(P,0)]][[sub(P,k)]]' 텍스트 혼합 유지(batch06 가변 첨자 라벨 정책과 동일), 줄임표 합은 cdots로 한 식에 연결. 답 ④ 유지(빠른정답 1과 불일치는 1차와 동일)")

# 47. 6805bd8a — 5of6 seq 99 (보류 유지): 한 쪽에 별개 문항 2개, id 1개 — 위 문항만 전사(아래 문항: [2009년 3월 고1 20번] 반지름 9cm인 원 O에
add(id='6805bd8a', qtype='short',
    question='다음 그림에서 점 P는 [[seg(AC)]]와 [[seg(BD)]]의 교점이다. [[angle(ABD) = deg(40)]], [[angle(BPC) = deg(70)]]이고 [[arc(BC) = 5]] cm일 때, 원의 둘레의 길이를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '원 위 A(좌상)·D(우상)·B(좌하)·C(우하). 현 AC·BD가 P에서 교차, 선분 AB. ∠ABD=40°(B), ∠BPC=70°(P), 호 BC=5cm'}}],
    confidence=0.75, needs_review='같은 이미지에 별개 문항 2개(id 1개) — 위 문항만 전사; 아래 문항: [2009년 3월 고1 20번] 반지름의 길이가 9cm인 원 O에서 호 AB=4π cm, 호 CD=6π cm이고 선분 AB와 선분 CD의 연장선이 만나서 이루는 예각의 크기가 30°일 때 호 AC의 길이는? ①4π ②17/4π ③9/2π ④5π ⑤11/2π (cm, 답 ⑤)',
    note='문법 문제 없음. 답 30 cm 유지(빠른정답 4는 두 문항 어느 답과도 불일치)')

# 48. 4f3c1d56 — 5of6 seq 42 (통과): 프라임 점 라벨(B′) / 도형 표현 불가: 시계추 실생활 도형 — 30−30cos45°=30−15√2=15(2−√2) → ①
add(id='4f3c1d56', qtype='choice',
    question="다음 그림과 같이 시계의 추가 B지점과 B′지점 사이를 일정한 속도로 움직이고 있다. 추의 길이는 30 cm이고, [[angle(BOA) = angle(AOB') = deg(45)]], [[angle(BOB') = deg(90)]]이다. 추가 가장 높은 위치에 있을 때, 추는 A지점을 기준으로 하여 몇 cm의 높이에 있는가?",
    choices=['[[15(2 - sqrt(2))]] cm', '[[20(2 - sqrt(2))]] cm', '[[25(2 - sqrt(2))]] cm', '[[30(2 - sqrt(2))]] cm', '[[35(2 - sqrt(2))]] cm'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 O에 매단 시계추: 최저점 A(수직 아래), 좌측 B, 우측 B′. 호 모양 점선 경로. ∠BOA=45°(O), OB=30cm(점선 치수)'}}],
    confidence=0.85,
    note="∠AOB′, ∠BOB′을 angle(AOB'), angle(BOB')로 연결(B′지점은 텍스트). 답 ① 유지(빠른정답 없음, 풀이 답 15(2−√2))")

# 49. 1cf28eb7 — 5of6 seq 46 (통과): 프라임 점 라벨(B′) / 도형 표현 불가: 시계추 실생활 도형 — 40−40cos45°=40−20√2=20(2−√2) → ①
add(id='1cf28eb7', qtype='choice',
    question="다음 그림과 같이 시계의 추가 B지점과 B′지점 사이를 일정한 속도로 움직이고 있다. 추의 길이는 40 cm이고 [[angle(BOA) = angle(AOB') = deg(45)]]이다. 추가 가장 높은 위치에 있을 때, 추는 A지점을 기준으로 몇 cm 높이에 있는가? (단, 추의 크기는 무시한다.)",
    choices=['[[20(2 - sqrt(2))]] cm', '[[25(2 - sqrt(2))]] cm', '[[30(2 - sqrt(2))]] cm', '[[35(2 - sqrt(2))]] cm', '[[40(2 - sqrt(2))]] cm'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 O에 매단 시계추: 최저점 A(수직 아래), 좌측 B, 우측 B′. 호 모양 점선 경로. ∠BOA=45°, ∠AOB′=45°(O), OB=40cm(점선 치수)'}}],
    confidence=0.85,
    note="∠AOB′을 angle(AOB')로 연결(B′지점은 텍스트). 답 ① 유지(빠른정답 없음, 풀이 답 20(2−√2))")
