# -*- coding: utf-8 -*-
# batch09 (79문항, 중학교: m1-2 18, m2-1 21, m2-2 27, m3-1 13) — v1.5 문법 재작업
# 핵심 교체: 프라임·첨자 점 라벨 → seg(OP'), seg(GG'), seg(G'D), seg(B'C'), seg(AB1), angle(BEC'), angle(A1OA4), angle(O'CO), angle(A'C'B'),
#            tri(A'B'C'), tri(G'BD), quad(A'B'C'D'), line(XX'), sim(quad, quad) / 비 → ratio(...) = ratio(...) / 경우 나눔 정의 → cases / 빈칸 □ → box(1)
#            단독 점·직선 이름(A′, C′, l′, 사각형 A′B′C′D′)과 화살표 없는 반직선 이름 OA₁은 텍스트(sub 혼합) 유지
# 5지 규격 밖(4지·3지·○× 판정형)은 short + 보기 본문 포함으로 통과(선지 완결성 확인). 도형은 unsupported(raw) 유지
# 여전히 보류(46): 한 이미지 두 문항(id 1개) 7, 이미지 잘림 5, 답 기호 ㉡·㉢ 2, 선지가 그림 6, 사용자 정의 연산자·기호(◎ ∘ ○□ △◎ ⟨⟩ <> {}) 13,
#            문자 자릿수 순환소수(0.ȧḃ, 0.abċḋ, 0.ȧ0bċ, 0.ȧ₁a₂⋯ȧₙ) 8, 비표준 순환점 1, 세로셈 1, 프라임 상수 a′b′c′(prime 우회) 3
ITEMS = []
def add(**kw): ITEMS.append(kw)

# ================= esc_sonnet_m1-2_1of4 =================
# 0. bb8d92fd — sonnet_m1-2_260827_기둥의 겉넓이와 부피_p99
add(id='bb8d92fd', qtype='choice',
    question='좌표평면 위의 네 점 A[[point(2, 4)]], B[[point(2, 2)]], C[[point(6, 2)]], D[[point(6, 4)]]에 대하여 사각형 ABCD를 [[x]]축을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 [[sub(V,x)]], [[y]]축을 회전축으로 하여 1회전 시킬 때 생기는 회전체의 부피를 [[sub(V,y)]]라 하자. 이때 [[ratio(sub(V,x), sub(V,y))]]는?',
    choices=['[[ratio(2, 3)]]', '[[ratio(3, 2)]]', '[[ratio(3, 4)]]', '[[ratio(4, 3)]]', '[[ratio(4, 5)]]'],
    figure=None,
    confidence=0.75,
    needs_review='같은 이미지에 별개 문항 2개(위: A(3, 5), B(3, 1), C(5, 1), D(5, 5), 선지 2:1/2:3/3:2/3:4/4:3, 답 ④ / 아래: 전사함)인데 id 1개 — 아래 문항만 전사',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ③ 유지(V_x=48π, V_y=64π → 3:4)')

# 1. 264d2cf7 — sonnet_m1-2_260827_회전체_p82
add(id='264d2cf7', qtype='short',
    question="매초 3 cm의 속력으로 쉬지 않고 움직이는 두 개미 A, B가 있다. 다음 그림과 같이 [[seg(OP) = 4k]] cm이고 밑면의 반지름의 길이가 [[k]] cm인 원뿔에서 개미 A는 점 P에서 출발하여 옆면을 돌아 다시 점 P로 되돌아오는 가장 짧은 선을 따라 움직인다. 이 선의 길이의 절반인 지점을 점 P′이라 하면 [[seg(OP') = 15]] cm일 때, 개미 B는 점 O에서 출발하여 [[seg(OP')]]을 따라 왕복하며 움직인다. 두 개미 A, B가 동시에 출발하여 두 번째 만날 때까지 걸리는 시간은 몇 초인지 구하시오. (단, [[k]]는 상수이고, 두 개미 A, B의 크기는 생각하지 않는다.)",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '원뿔: 꼭짓점 O, 모선 OP = 4k cm, 밑면 반지름 k cm, 옆면 위 P에서 출발해 P로 돌아오는 최단 곡선, 그 중점 P′, OP′ = 15 cm'}}],
    confidence=0.85,
    note="선분 OP′(윗줄)을 seg(OP')로 교체(점 P′ 단독은 텍스트). 답 15 유지(전개도 부채꼴 90°, 최단선 30 cm, P′에서만 만남 → t=5, 15)")

# 2. d1d7781a — sonnet_m1-2_260827_각_p2
add(id='d1d7781a', qtype='short',
    question='다음 그림을 보고 □ 안에 들어갈 알맞은 것을 고르시오.\n[[angle(DOE)]]는 □이다.\n① 예각 ② 직각 ③ 둔각 ④ 평각',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '직선 BC(가로, B 왼쪽·C 오른쪽) 위의 점 O, O에서 위로 수직인 반직선 OE(직각 표시), 왼쪽 위로 반직선 OA, 오른쪽 위로 반직선 OD'}}],
    confidence=0.85,
    note='v1.5로 고칠 표기 없음. 선지 4개(①~④, 예각·직각·둔각·평각으로 완결)라 short로 두고 보기를 본문에 포함. 답 ① 유지')

# 3. 4dcf86ce — sonnet_m1-2_260827_각_p4
add(id='4dcf86ce', qtype='short',
    question='다음 그림을 보고 □ 안에 들어갈 알맞은 것을 고르시오.\n[[angle(POQ)]]는 □이다.\n① 평각 ② 둔각 ③ 직각 ④ 예각',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '직선 PQ(세로, P 위·Q 아래) 위의 점 O, O에서 오른쪽으로 수직인 반직선 OS(직각 표시), 오른쪽 위로 반직선 OT, 오른쪽 아래로 반직선 OR'}}],
    confidence=0.85,
    note='v1.5로 고칠 표기 없음. 선지 4개(①~④, 평각·둔각·직각·예각으로 완결)라 short로 두고 보기를 본문에 포함. 답 ① 유지(P, O, Q 한 직선 위 → 평각)')

# 4. 0869dc1c — sonnet_m1-2_260827_각_p5
add(id='0869dc1c', qtype='short',
    question='다음 그림을 보고 □ 안에 들어갈 알맞은 것을 고르시오.\n[[angle(POQ)]]는 □이다.\n① 예각 ② 직각 ③ 둔각 ④ 평각',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '직선 PQ(세로, Q 위·P 아래) 위의 점 O, O에서 왼쪽으로 수직인 반직선 OS(직각 표시), 왼쪽 위로 반직선 OR'}}],
    confidence=0.85,
    note='v1.5로 고칠 표기 없음. 선지 4개(①~④, 예각·직각·둔각·평각으로 완결)라 short로 두고 보기를 본문에 포함. 답 ④ 유지(P, O, Q 한 직선 위 → 평각)')

# 5. 3cc34c60 — sonnet_m1-2_260827_각_p31
add(id='3cc34c60', qtype='choice',
    question="다음 그림은 직사각형 모양의 종이를 [[seg(DE)]]를 접는 선으로 하여 접은 것이다. [[ratio(angle(BEC'), angle(DEC')) = ratio(4, 3)]]일 때, [[angle(BEC')]]의 크기는?",
    choices=['[[deg(36)]]', '[[deg(54)]]', '[[deg(72)]]', '[[deg(80)]]', '[[deg(90)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '직사각형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래)를 DE(E는 BC 위)로 접어 C가 C′으로 이동, 점선 EC·CD, E에 각 표시'}}],
    confidence=0.85,
    note="프라임 각 ∠BEC′·∠DEC′를 angle(BEC'), angle(DEC')로, 비는 ratio로 교체. 답 ③ 유지(4k+3k+3k=180 → 72°)")

# 6. 7934fa20 — sonnet_m1-2_260827_각_p38
add(id='7934fa20', qtype='short',
    question='다음 그림의 네 반직선 O[[sub(A,1)]], O[[sub(A,2)]], O[[sub(A,3)]], O[[sub(A,4)]] 중에서 두 반직선을 변으로 하고 점 O를 꼭짓점으로 하는 모든 각에 대하여 작은 쪽의 각의 크기의 합이 [[deg(470)]]이고 [[angle(c) = 2 angle(a)]], [[3 angle(b) = 5 angle(a)]]일 때, [[angle(A1OA4)]]의 크기를 구하시오. (단, [[deg(0) < angle(A1OA4) < deg(180)]])',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 O에서 나가는 네 반직선 OA₁(오른쪽), OA₂(오른쪽 위), OA₃(위), OA₄(왼쪽 위); 이웃한 각 a = ∠A₁OA₂, b = ∠A₂OA₃, c = ∠A₃OA₄'}}],
    confidence=0.85,
    note='첨자 각 ∠A₁OA₄를 angle(A1OA4)로 교체(반직선 이름 OA₁~OA₄는 원문에 화살표 없는 텍스트라 sub 혼합 유지). 답 deg(140) 유지(3a+4b+3c=470, c=2a, b=5a/3 → a=30)')

# 7. 17272910 — sonnet_m1-2_260827_각_p39
add(id='17272910', qtype='short',
    question='다음 그림의 네 반직선 O[[sub(A,1)]], O[[sub(A,2)]], O[[sub(A,3)]], O[[sub(A,4)]] 중에서 두 반직선을 변으로 하고 점 O를 꼭짓점으로 하는 모든 각에 대하여 작은 쪽의 각의 크기의 합이 [[deg(430)]]이고 [[angle(c) = 2 angle(a)]], [[3 angle(b) = 4 angle(a)]]일 때, [[angle(A1OA4)]]의 크기를 구하시오. (단, [[deg(0) < angle(A1OA4) < deg(180)]])',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '점 O에서 나가는 네 반직선 OA₁(오른쪽), OA₂(오른쪽 위), OA₃(위), OA₄(왼쪽 위); 이웃한 각 a = ∠A₁OA₂, b = ∠A₂OA₃, c = ∠A₃OA₄'}}],
    confidence=0.85,
    note='첨자 각 ∠A₁OA₄를 angle(A1OA4)로 교체(반직선 이름 OA₁~OA₄는 원문에 화살표 없는 텍스트라 sub 혼합 유지). 답 deg(130) 유지(3a+4b+3c=430, c=2a, b=4a/3 → a=30)')

# 8. f302bd2c — sonnet_m1-2_260827_각_p57
add(id='f302bd2c', qtype='short',
    question='다음 그림에서 [[angle(x)]], [[angle(y)]]의 크기는?\n① [[angle(x) = deg(68)]], [[angle(y) = deg(68)]] ② [[angle(x) = deg(68)]], [[angle(y) = deg(78)]] ③ [[angle(x) = deg(78)]], [[angle(y) = deg(68)]] ④ [[angle(x) = deg(78)]], [[angle(y) = deg(78)]]',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '두 직선이 한 점에서 교차, 왼쪽 각 112°, 위쪽 각 y, 아래쪽 각 x'}}],
    confidence=0.75,
    note='v1.5로 고칠 표기 없음. 선지 ①~④(68°/78° 조합 4가지로 완결, ⑤ 없음으로 판단)라 short로 두고 보기를 본문에 포함. 답 ① 유지(맞꼭지각 x=y=68°)')

# 9. 8d29ed09 — sonnet_m1-2_260827_각_p59
add(id='8d29ed09', qtype='short',
    question='다음 그림과 같은 사다리꼴 ABCD에서 [[seg(BC)]]와 직교하는 변은?\n① [[seg(AB)]] ② [[seg(AD)]] ③ [[seg(CD)]]',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 3 cm, AB = 6 cm, BC = 6 cm, A·B에 직각 표시'}}],
    confidence=0.75,
    note='v1.5로 고칠 표기 없음. 선지 ①~③(BC 외의 세 변 AB·AD·CD로 완결)이라 short로 두고 보기를 본문에 포함. 답 ① 유지(∠B=90°)')

# 10. 03fef3c1 — sonnet_m1-2_260827_각_p63
add(id='03fef3c1', qtype='short',
    question="다음 그림과 같은 사다리꼴 ABCD에 대한 설명으로 옳은 것은 '○'를, 옳지 않은 것은 '×'를 고르시오.\n[[perp(seg(AB), seg(AD))]]\n① ○ ② ×",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 24 cm, AB = 20 cm, DC = 30 cm, BC = 26 cm, A·D에 직각 표시'}}],
    confidence=0.85,
    note='v1.5로 고칠 표기 없음. ○× 판정형(선지 2개)이라 short로 두고 보기를 본문에 포함. 답 ① 유지(A에 직각 표시)')

# 11. a2f64b7d — sonnet_m1-2_260827_각_p63
add(id='a2f64b7d', qtype='short',
    question="다음 그림과 같은 사다리꼴 ABCD에 대한 설명으로 옳은 것은 '○'를, 옳지 않은 것은 '×'를 고르시오.\n[[perp(seg(AB), seg(AD))]]\n① ○ ② ×",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 24 cm, AB = 20 cm, DC = 30 cm, BC = 26 cm, A·D에 직각 표시'}}],
    confidence=0.85,
    note='v1.5로 고칠 표기 없음. ○× 판정형(선지 2개)이라 short로 두고 보기를 본문에 포함(같은 이미지 id 2개). 답 ① 유지(A에 직각 표시)')

# 12. cd30823a — sonnet_m1-2_260827_각_p64
add(id='cd30823a', qtype='short',
    question="다음 그림과 같은 사다리꼴 ABCD에 대한 설명으로 옳은 것은 '○'를, 옳지 않은 것은 '×'를 고르시오.\n[[perp(seg(BC), seg(CD))]]\n① ○ ② ×",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 15 cm, AB = 12 cm, DC = 10 cm, BC = 17 cm, A·D에 직각 표시'}}],
    confidence=0.85,
    note='v1.5로 고칠 표기 없음. ○× 판정형(선지 2개)이라 short로 두고 보기를 본문에 포함. 답 ② 유지(직각은 A·D에만)')

# 13. b8a93ef2 — sonnet_m1-2_260827_각_p65
add(id='b8a93ef2', qtype='short',
    question="다음 그림과 같은 사다리꼴 ABCD에 대한 설명으로 옳은 것은 '○'를, 옳지 않은 것은 '×'를 고르시오.\n[[perp(seg(AD), seg(CD))]]\n① ○ ② ×",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '사다리꼴 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), AD = 16 cm, AB = 12 cm, BC = 11 cm, CD = 13 cm, A·B에 직각 표시'}}],
    confidence=0.85,
    note='v1.5로 고칠 표기 없음. ○× 판정형(선지 2개)이라 short로 두고 보기를 본문에 포함. 답 ② 유지(직각은 A·B에만)')

# 14. e40cf02c — sonnet_m1-2_260827_삼각형의 내각과 외각_p4
add(id='e40cf02c', qtype='short',
    question="[[angle(C) = deg(90)]]인 삼각형 모양의 종이 ABC를 [[seg(BD)]]를 접는 선으로 하여 접었을 때 점 A가 이동한 점을 A′라 하고, [[seg(BA')]]과 [[seg(AC)]]의 교점을 E라 하자. 다시 [[seg(BE)]]를 접는 선으로 하여 종이를 접었더니 다음 그림과 같이 점 C가 [[seg(BD)]] 위의 점 C′과 겹쳐졌다. [[angle(BDE)]]의 크기를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '직각삼각형 ABC(C에 직각, B 왼쪽 아래, C 오른쪽 아래, A 위), ∠A = 36°, D·E는 AC 위, A′은 BE의 연장선 위(오른쪽), C′은 BD 위, 접힌 부분 색칠'}}],
    confidence=0.85,
    note="선분 BA′(윗줄)을 seg(BA')로 교체(점 A′·C′ 단독은 텍스트). ∠A=36°는 그림에만 있어 figure raw에 기록. 답 deg(54) 유지(∠B=54°가 삼등분 → ∠ADB=126°)")

# ================= esc_sonnet_m1-2_2of4 =================
# 15. 818da9cd — sonnet_m1-2_260827_다각형_p57
add(id='818da9cd', qtype='choice',
    question='다음 중 [[angle(x)]]의 크기가 가장 큰 것은?',
    choices=['(그림) 삼각형: 한 내각 [[deg(60)]]과 이웃한 외각 [[angle(x)]]', '(그림) 사각형: 한 내각 [[deg(70)]]과 이웃한 외각 [[angle(x)]]', '(그림) 사각형: 한 내각 [[deg(45)]]과 이웃한 외각 [[angle(x)]]', '(그림) 오각형: 한 내각 [[deg(85)]]과 이웃한 외각 [[angle(x)]]', '(그림) 오각형: 한 내각 [[deg(110)]]과 이웃한 외각 [[angle(x)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '선지 ①~⑤가 각각 다각형 그림: ① 삼각형(내각 60°, 외각 x) ② 사각형(내각 70°, 외각 x) ③ 사각형(내각 45°, 외각 x) ④ 오각형(내각 85°, 외각 x) ⑤ 오각형(내각 110°, 외각 x)'}}],
    confidence=0.7,
    needs_review='선지 ①~⑤가 모두 다각형 그림 — 문법·텍스트로 표현 불가(설명문으로 대체)',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ③ 유지(외각 180°−45°=135°가 최대)')

# ================= esc_sonnet_m1-2_3of4 =================
# 16. b624c81f — sonnet_m1-2_260827_평행선의 성질_p49
add(id='b624c81f', qtype='short',
    question="다음 그림에서 [[par(line(XX'), line(YY'))]]이고 [[angle(CAB) = 5 angle(CAX')]], [[angle(CBA) = 5 angle(CBY')]]일 때, [[angle(x)]]의 크기를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '가로 직선 XX′(위, A 포함), YY′(아래, B 포함), A와 B를 지나는 횡단선, 오른쪽 점 C와 삼각형 ABC, x=∠ACB'}}],
    confidence=0.85,
    note="직선 XX′·YY′(양쪽 화살표)을 line(XX'), line(YY')로, ∠CAX′·∠CBY′를 angle(CAX'), angle(CBY')로 교체. 답 deg(30) 유지(6a+6b=180 → x=180−5(a+b))")

# 17. 09bf7b71 — sonnet_m1-2_260827_평행선의 성질_p58
add(id='09bf7b71', qtype='short',
    question='다음 그림에서 [[l]] ∥ l′일 때, [[angle(x)]]의 크기를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '평행선 l(위), l′(아래). l에서 35°(아래 왼쪽)로 내려온 선이 왼쪽 점에서 꺾임(x, 오른쪽), 오른쪽 아래 점으로 내려가 다시 꺾임(80°, 왼쪽), l′로 내려가 만남(위 오른쪽 50°)'}}],
    confidence=0.8,
    note='프라임 직선 이름 l′은 단독 이름이라 텍스트로 유지(원문에 윗줄 없음, prime(l)은 도함수 뜻이라 쓰지 않음). 답 deg(65) 유지(35°+(80°−50°))')

# ================= esc_opus_m2-1_1of1 =================
# 18. ac9cb337 — opus_m2-1_260827_순환소수의 분수 표현_p69
add(id='ac9cb337', qtype='short',
    question='순환마디가 [[n]]인 순환소수 0.ȧ₁a₂a₃ ⋯ ȧₙ에 대하여 순환마디의 첫 번째 숫자를 순환마디의 마지막 자리로 옮겨 만든 순환소수 0.ȧ₂a₃a₄ ⋯ aₙȧ₁이 처음 수의 [[frac(13,3)]]배가 된다고 한다. 처음 수를 [[frac(q, p)]]라 할 때, [[p + q]]의 값을 구하시오. (단, [[1 <= i <= n]]에 대하여 [[sub(a,i)]]는 [[0 <= sub(a,i) <= 9]]인 정수, [[p]], [[q]]는 서로소인 자연수이다.)',
    choices=None,
    figure=None,
    confidence=0.75,
    needs_review='문법 범위 밖: 문자 자릿수 순환소수 0.ȧ₁a₂a₃⋯ȧₙ(순환마디가 첨자 문자열) — recdec의 순환마디는 숫자만 가능하고 sub(a,1) sub(a,2)⋯는 곱 뜻이 되어 우회 불가, 유니코드 텍스트 유지',
    note='답 20 유지(x=3a₁/17, a₁=1 → 3/17)')

# ================= esc_sonnet_m2-1_1of4 =================
# 19. 9334ad53 — sonnet_m2-1_260827_함수와 함숫값_p36
add(id='9334ad53', qtype='short',
    question='다음에서 [[y]] 를 [[x]] 의 함수라고 할 수 없는 것을 구하여라.\n㉠ 한 팩에 1000원인 우유를 [[x]] 팩 살 때 지불 금액 [[y]] 원\n㉡ 자연수 [[x]] 와 그 배수 [[y]]\n㉢ 넓이가 20cm² 인 삼각형의 밑변의 길이 [[x]]cm 와 높이 [[y]]cm',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='답 기호 ㉡이 답 문법(ㄱㄴㄷ·①~⑤) 범위 밖이라 answer 미기재(함수가 아닌 것은 ㉡)',
    note='v1.5로 고칠 표기 없음(초안 유지)')

# 20. 068b87c7 — sonnet_m2-1_260827_함수와 함숫값_p99
add(id='068b87c7', qtype='choice',
    question='함수 [[f(x)]] = ([[x]] 이하의 소수의 개수)일 때, [[f(20)]]의 값은?',
    choices=['[[7]]', '[[8]]', '[[9]]', '[[10]]', '[[11]]'],
    figure=None,
    confidence=0.8,
    needs_review='같은 이미지에 별개 문항 2개(f(20)·f(30))인데 id 1개 — 첫 문항(f(20))만 전사',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ② 유지(20 이하 소수 8개)')

# 21. a4ee2c72 — sonnet_m2-1_260827_유리수의 소수 표현_p71
add(id='a4ee2c72', qtype='choice',
    question='다음 중 순환소수의 표현이 올바른 것은?',
    choices=['[[2.333]]⋯ = [[recdec(2, 3)]]', '[[0.123123]]⋯ = 0.1̇2̇3̇', '[[15.49549549]] = 15̇.4.9̇', '[[3.4324324]]⋯ = 3̇.4̇3̇2̇', '[[1.2212212]]⋯ = [[recdec(1.2, 21)]]'],
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 선지 ②③④의 순환점이 비표준 위치(0.1̇2̇3̇, 15̇.4.9̇, 3̇.4̇3̇2̇ — 인쇄 그대로)라 recdec로 표현 불가, 유니코드 결합 점 텍스트 유지',
    note='답 ① 유지(①만 올바른 표기)')

# 22. 9dba8172 — sonnet_m2-1_260827_연립방정식의 활용(1)_p11
add(id='9dba8172', qtype='short',
    question='다음 뺄셈을 만족시키는 한 자리 자연수 [[A]], [[B]]에 대하여 [[A B]]의 값을 구하시오.\n2 0 [[B]] 5\n− 1 [[B]] [[A]] 6\n= [[A]] 3 9',
    choices=None,
    figure=None,
    confidence=0.75,
    needs_review='문법 범위 밖: 자릿수에 문자가 든 세로셈(20B5 − 1BA6 = A39) 표기 — 텍스트로 전사, AB의 뜻(곱/두 자리 수) 불확실하여 답 미기재',
    note='v1.5로 고칠 표기 없음(초안 유지)')

# 23. 4881c5dc — sonnet_m2-1_260827_일차함수의 그래프와 연립방정식_p3
add(id='4881c5dc', qtype='choice',
    question='다음 그림은 연립방정식 [[a x + b y = c]], [[prime(a) x + prime(b) y = prime(c)]]을 그래프로 나타낸 것이다. 이 연립방정식의 해를 [[point(m, n)]]라고 할 때, [[pow(m,2) + 2n]]의 값은?',
    choices=['[[5]]', '[[6]]', '[[7]]', '[[8]]', '[[9]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '좌표평면: 증가 직선 ax+by=c(점 (−2, 1), (0, 5) 통과)와 감소 직선 a′x+b′y=c′(점 (−3, 5) 통과)가 점 (−1, 3)에서 만남. x축 −3, −2, −1과 y축 1, 3, 5에 점선 좌표 표시'}}],
    confidence=0.8,
    needs_review='문법 범위 밖: 프라임 상수 a′, b′, c′ — v1.5에도 대응 표기 없음(라벨 함수 밖), prime()은 도함수 뜻이라 우회(표시는 동일) / 도형 표현 불가: 좌표평면 두 직선 그래프',
    note='답 ③ 유지(교점 (−1, 3) → 1+6=7)')

# 24. 6ebd200f — sonnet_m2-1_260827_일차함수의 그래프와 연립방정식_p5
add(id='6ebd200f', qtype='choice',
    question='[[x]], [[y]] 에 관한 연립방정식 [[a x + b y = c]] ⋯㉠, [[prime(a) x + prime(b) y = prime(c)]] ⋯㉡ 을 다음 그림과 같이 그래프를 이용하여 풀었다. 해가 [[point(m, n)]]일 때,\n[[m + n]]의 값은?',
    choices=['[[-3]]', '[[-2]]', '[[-1]]', '[[1]]', '[[2]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '좌표평면: 증가 직선 ㉠(y절편 2)과 감소 직선 ㉡이 점 (−2, 1)에서 만남(점선으로 x=−2, y=1 표시), 원점 O'}}],
    confidence=0.8,
    needs_review='문법 범위 밖: 프라임 상수 a′, b′, c′ — v1.5에도 대응 표기 없음(라벨 함수 밖), prime()은 도함수 뜻이라 우회(표시는 동일) / 도형 표현 불가: 좌표평면 두 직선 그래프',
    note='답 ③ 유지(교점 (−2, 1) → m+n=−1)')

# 25. 35d63ad8 — sonnet_m2-1_260827_일차함수의 그래프와 연립방정식_p56
add(id='35d63ad8', qtype='short',
    question='[[x]], [[y]] 에 대한 두 일차방정식 [[a x + b y + c = 0]], [[prime(a) x + prime(b) y + prime(c) = 0]]의 그래프가 한 점에서 만날 때, 다음 보기 중 연립방정식 [[a x + b y + c = 0]], [[prime(a) x + prime(b) y + prime(c) = 0]]의 해로 알맞은 것을 고르시오.\n<보기>\nㄱ. 해가 없다.\nㄴ. 한 쌍의 해를 갖는다.\nㄷ. 해가 무수히 많다.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 프라임 상수 a′, b′, c′ — v1.5에도 대응 표기 없음(라벨 함수 밖), prime()은 도함수 뜻이라 우회(표시는 동일)',
    note='답 ㄴ 유지(한 점에서 만남 → 해 한 쌍)')

# ================= esc_sonnet_m2-1_2of4 =================
# 26. f62dc9bf — sonnet_m2-1_260827_다항식의 곱셈과 나눗셈_p99
add(id='f62dc9bf', qtype='choice',
    question='[[A = (-4 pow(x,2) pow(y,2) + frac(3,2) x pow(y,3)) ÷ (frac(3,2) x pow(y,2))]],\n[[B = frac(5,4)(2x - frac(8,5) y)]]일 때,\n[[B - (2A - 3B - (5A - 2B))]]를 [[x]], [[y]]에 대한 식으로 바르게 나타낸 것은?',
    choices=['[[-18x + frac(27,4) y]]', '[[-13x + frac(11,4) y]]', '[[-8x + 3y]]', '[[-7x - 9y]]', '[[-3x - y]]'],
    figure=None,
    confidence=0.75,
    needs_review='같은 이미지에 별개 문항 2개(위: A=0.4x+1.4y, B=0.05x+0.6y, A▲B=3A−5B, A▼B=A+3B, (A▲B)▲(A▼B)=mx+ny일 때 2m+n(=−61/5) / 아래: 전사함)인데 id 1개 — 아래 문항만 전사',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ⑤ 유지(3A+2B=−3x−y)')

# ================= esc_sonnet_m2-1_3of4 =================
# 27. 856bb476 — sonnet_m2-1_260827_순환소수의 분수 표현_p15
add(id='856bb476', qtype='short',
    question='서로 다른 한 자리 자연수 [[a]], [[b]], [[c]], [[d]]에 대하여 abcd = [[1000a + 100b + 10c + d]]이고 ab = [[10a + b]]라 하자. [[frac(4315, 9900)]] = (abcd − ab)/9900 = 0.abċḋ일 때, [[abs(a - b + c - d)]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 자릿수 문자열 abcd(=1000a+100b+10c+d)·ab와 문자 순환소수 0.abċḋ — recdec의 순환마디는 숫자만 가능(문자 병치는 곱 뜻), 텍스트 혼합 유지',
    note='답 2 유지(abcd−ab=4315 → 4358 → |4−3+5−8|)')

# 28. 7cd9846a — sonnet_m2-1_260827_순환소수의 분수 표현_p16
add(id='7cd9846a', qtype='short',
    question='서로 다른 한 자리 자연수 [[a]], [[b]], [[c]], [[d]]에 대하여 abcd = [[1000a + 100b + 10c + d]]이고 ab = [[10a + b]]라 하자. [[frac(3651, 9900)]] = (abcd − ab)/9900 = 0.abċḋ일 때, [[abs(a + b - c + d)]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 자릿수 문자열 abcd(=1000a+100b+10c+d)·ab와 문자 순환소수 0.abċḋ — recdec의 순환마디는 숫자만 가능(문자 병치는 곱 뜻), 텍스트 혼합 유지',
    note='답 8 유지(3651 → 3687 → |3+6−8+7|)')

# 29. 890f7408 — sonnet_m2-1_260827_순환소수의 분수 표현_p17
add(id='890f7408', qtype='short',
    question='서로 다른 한 자리 자연수 [[a]], [[b]], [[c]], [[d]]에 대하여 abcd = [[1000a + 100b + 10c + d]]이고 ab = [[10a + b]]라 하자. [[frac(5246, 9900)]] = (abcd − ab)/9900 = 0.abċḋ일 때, [[abs(a - b + c + d)]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 자릿수 문자열 abcd(=1000a+100b+10c+d)·ab와 문자 순환소수 0.abċḋ — recdec의 순환마디는 숫자만 가능(문자 병치는 곱 뜻), 텍스트 혼합 유지',
    note='답 20 유지(5246 → 5298 → |5−2+9+8|)')

# 30. 2930680a — sonnet_m2-1_260827_순환소수의 분수 표현_p38
add(id='2930680a', qtype='choice',
    question='한 자리 자연수 [[a]], [[b]]에 대하여 0.ȧḃ + 0.ḃȧ = [[recdec(0, 5)]]가 성립할 때, [[a + b]]의 값은?',
    choices=['[[4]]', '[[5]]', '[[6]]', '[[7]]', '[[8]]'],
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 문자 순환소수 0.ȧḃ, 0.ḃȧ — recdec(0, a b)는 순환마디가 곱 a×b 뜻이 되어 우회 불가, 텍스트 혼합 유지',
    note='답 ② 유지(11(a+b)/99=5/9 → a+b=5)')

# 31. caef767c — sonnet_m2-1_260827_순환소수의 분수 표현_p39
add(id='caef767c', qtype='short',
    question='두 수 [[a]], [[b]]에 대하여 [[a]]◎[[b]] = [[cases(-1, a > b, 0, a = b, 1, a < b)]]로 정의할 때, ([[0.5]]◎[[recdec(0, 5)]])◎([[1.3]]◎[[recdec(1.2, 9)]])의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 이항연산 ◎ — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지(경우 나눔은 cases로 교체)',
    note='경우 나눔 정의를 cases(-1, a>b, 0, a=b, 1, a<b)로 교체. 답 −1 유지(0.5<0.5̇ → 1, 1.3=1.29̇ → 0, 1◎0=−1)')

# 32. 6d12b521 — sonnet_m2-1_260827_순환소수의 분수 표현_p40
add(id='6d12b521', qtype='short',
    question='[[a]]∘[[b]]를 [[cases(1, a = b, 0, a != b)]]이라 하면 [[a = recdec(0.1, 9)]], [[b = 0.2]], [[c = recdec(0, 01)]], [[d = frac(1, 90)]]일 때, ([[a]]∘[[b]])∘([[c]]∘[[d]])의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 이항연산 ∘ — v1.5에도 대응 표기 없음, 정의식·계산식을 텍스트 혼합으로 유지(경우 나눔은 cases로 교체)',
    note='경우 나눔 정의(a=b이면 1, a≠b이면 0)를 cases(1, a = b, 0, a != b)로 교체. 답 0 유지(a=0.2=b → 1; c=1/99≠1/90 → 0; 1∘0=0)')

# 33. 01c545d6 — sonnet_m2-1_260827_순환소수의 분수 표현_p44
add(id='01c545d6', qtype='short',
    question='[[A]] = 0.ȧ0bċ, [[B]] = 0.ȧcb0̇일 때, 다음 부등식을 만족시키는 [[c]]의 값을 구하시오.\n(단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.044 < B - A < 0.055]]',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 문자 순환소수 0.ȧ0bċ 꼴(순환마디가 문자·숫자 혼합 문자열) — recdec의 순환마디는 숫자만 가능(문자 병치는 곱 뜻), 텍스트 혼합 유지',
    note='답 5 유지(B−A=c/101 → 4.44<c<5.56)')

# 34. 58010922 — sonnet_m2-1_260827_순환소수의 분수 표현_p46
add(id='58010922', qtype='short',
    question='[[A]] = 0.ȧc0ḃ, [[B]] = 0.ȧ0cḃ일 때, 다음 부등식을 만족하는 [[c]]의 값을 구하시오.\n(단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.02 < A - B < 0.03]]',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 문자 순환소수 0.ȧ0bċ 꼴(순환마디가 문자·숫자 혼합 문자열) — recdec의 순환마디는 숫자만 가능(문자 병치는 곱 뜻), 텍스트 혼합 유지',
    note='답 3 유지(A−B=90c/9999 → 2.22<c<3.33)')

# 35. d1756fad — sonnet_m2-1_260827_순환소수의 분수 표현_p47
add(id='d1756fad', qtype='short',
    question='[[A]] = 0.ḃa0ċ, [[B]] = 0.ḃ0aċ일 때, 다음 부등식을 만족하는 [[a]]의 값을 구하시오. (단, [[a]], [[b]], [[c]]는 한 자리 자연수)\n[[0.07 < A - B < 0.08]]',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 문자 순환소수 0.ȧ0bċ 꼴(순환마디가 문자·숫자 혼합 문자열) — recdec의 순환마디는 숫자만 가능(문자 병치는 곱 뜻), 텍스트 혼합 유지',
    note='답 8 유지(A−B=90a/9999 → 7.78<a<8.89)')

# 36. ef25dc26 — sonnet_m2-1_260827_일차함수의 그래프의 성질_p99
add(id='ef25dc26', qtype='choice',
    question='그래프는 일차함수 [[y = a x + b]]의 그래프이다. 이 그래프에 대한 다음 설명 중 옳지 않은 것은?',
    choices=['[[x = 1]]일 때, 함숫값이 [[-3]]이다.', '[[x]]절편은 [[-5]]이다.', '[[x]]의 값이 증가하면 [[y]]의 값은 감소한다.', '[[y = 5x + 2]]의 그래프와 [[y]]축에 대하여 대칭이다.', '[[y = -5x]]의 그래프를 [[y]]축의 방향으로 2만큼 평행이동한 그래프이다.'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '좌표평면: 두 점 (−1, 7), (1, −3)을 지나는 오른쪽 아래로 향하는 직선(점선으로 좌표 표시)'}}],
    confidence=0.75,
    needs_review="이미지 상단 잘림(첫 줄이 '그래프는'으로 시작, 앞 낱말 누락) / 도형 표현 불가: 좌표평면 위 직선 그래프",
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ② 유지(y=−5x+2 → x절편 2/5)')

# 37. 46c6384a — sonnet_m2-1_260827_단항식의 곱셈과 나눗셈_p33
add(id='46c6384a', qtype='short',
    question='두 문자 [[a]], [[b]]에 대하여 기호 ○, □를 [[a]]○[[b]] = [[a pow(b,2)]], [[a]]□[[b]] = [[4a b]]라 약속할 때, ([[a]]○([[b]]□[[a]]))/([[b]]□([[b]]○[[a]]))를 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 이항연산 ○·□ — v1.5에도 대응 표기 없음, 정의식·계산식(분수 형태)을 텍스트 혼합으로 유지',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 4a 유지')

# 38. ae6535ac — sonnet_m2-1_260827_단항식의 곱셈과 나눗셈_p58
add(id='ae6535ac', qtype='choice',
    question='두 식 [[a]], [[b]]에 대하여 △, ◎를 [[a]]△[[b]] = [[a pow(b,2)]], [[a]]◎[[b]] = [[3 pow(a,2) b]]로 약속하자. 이때 다음을 만족시키는 두 식 [[A]], [[B]]에 대하여 [[5 pow(A,2) ÷ (2B)]]를 계산하면?\n[[A]]△[[2x]] = [[8 pow(x,3) pow(y,2)]], [[y]]◎[[B]] = [[15 pow(x,2) pow(y,3)]]',
    choices=['[[frac(2, x pow(y,3))]]', '[[frac(1, 2 pow(x,2) y)]]', '[[frac(1, 2 pow(y,3))]]', '[[frac(x pow(y,3), 2)]]', '[[2 pow(y,3)]]'],
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 이항연산 △·◎ — v1.5에도 대응 표기 없음, 정의식·조건식을 텍스트 혼합으로 유지',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ⑤ 유지(A=2xy², B=5x²y → 2y³)')

# ================= esc_sonnet_m2-2_1of5 =================
# 39. 49b32dfa — sonnet_m2-2_260827_삼각형의 무게중심_p55
add(id='49b32dfa', qtype='choice',
    question="다음 그림에서 점 G와 G′은 각각 [[tri(ABC)]]와 [[tri(GBC)]]의 무게중심이고, [[seg(G'D) = 2]]일 때, [[seg(AG)]]의 길이는?",
    choices=['[[10]]', '[[12]]', '[[14]]', '[[16]]', '[[18]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 중선 AD(D는 BC의 중점) 위의 무게중심 G와 △GBC의 무게중심 G′, 선분 GB·GC·G′B·G′C'}}],
    confidence=0.85,
    note="선분 G′D(윗줄)를 seg(G'D)로 교체. 답 ② 유지(G′D=GD/3 → GD=6, AG=12)")

# 40. 718059ce — sonnet_m2-2_260827_삼각형의 무게중심_p57
add(id='718059ce', qtype='choice',
    question="다음 그림에서 점 G는 [[tri(ABC)]]의 무게중심이고, 점 G′은 [[tri(GBC)]]의 무게중심이다. [[seg(AD) = 12]] cm일 때, [[seg(GG')]]의 길이는?",
    choices=['[[frac(2,3)]] cm', '[[frac(4,3)]] cm', '[[2]] cm', '[[frac(8,3)]] cm', '[[frac(10,3)]] cm'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 중선 AD(D는 BC의 중점) 위의 무게중심 G와 △GBC의 무게중심 G′, 선분 GB·GC·G′B·G′C, AD=12 cm 치수(점선 호)'}}],
    confidence=0.85,
    note="선분 GG′(윗줄)를 seg(GG')로 교체. 답 ④ 유지(GD=4, GG′=8/3)")

# 41. fdae7650 — sonnet_m2-2_260827_삼각형의 무게중심_p59
add(id='fdae7650', qtype='short',
    question="다음 그림에서 [[seg(BM)]]은 [[tri(ABC)]]의 중선이고 두 점 G, G′은 각각 [[tri(ABC)]], [[tri(AGC)]]의 무게중심이다. [[seg(G'M) = 5]] cm일 때, [[seg(BG')]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), AC의 중점 M과 중선 BM, BM 위의 무게중심 G와 △AGC의 무게중심 G′(GM 위), 선분 AG·GC, G′M=5 cm 치수(점선 호)'}}],
    confidence=0.85,
    note="선분 G′M·BG′(윗줄)를 seg(G'M), seg(BG')로 교체. 답 40 cm 유지(GM=15, BG=30, GG′=10)")

# 42. efe51061 — sonnet_m2-2_260827_삼각형의 무게중심_p71
add(id='efe51061', qtype='short',
    question="다음 그림의 [[seg(BC) = 8]] cm인 이등변삼각형 ABC에서 밑변 BC의 중점을 D, [[tri(ABD)]]와 [[tri(ACD)]]의 무게중심을 각각 G, G′이라고 한다. 이때, [[seg(GG')]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '이등변삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), BC의 중점 D와 선분 AD, △ABD의 무게중심 G(왼쪽)·△ACD의 무게중심 G′(오른쪽)와 선분 GG′, BC=8 cm 치수(점선 호)'}}],
    confidence=0.85,
    note="선분 GG′(윗줄)를 seg(GG')로 교체. 답 frac(8,3) cm 유지(G, G′은 AD에서 각각 4/3 떨어짐)")

# 43. 2908d225 — sonnet_m2-2_260827_삼각형의 무게중심_p74
add(id='2908d225', qtype='short',
    question="다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 사다리꼴 ABCD에서 세 점 M, N, H는 각각 [[seg(AB)]], [[seg(DC)]], [[seg(BC)]]의 중점이고 두 점 G, G′은 각각 [[tri(ABC)]], [[tri(DBC)]]의 무게중심이다. [[seg(MN) = frac(45,2)]] cm, [[seg(BC) = 30]] cm일 때, [[seg(GG')]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '사다리꼴 ABCD(AD 위, BC 아래), AB·DC·BC의 중점 M·N·H(같은 길이 표시), 선분 MN·AH·DH·AC·BD, AH 위의 G와 DH 위의 G′을 이은 선분 GG′, MN=45/2 cm·BC=30 cm 치수(점선 호)'}}],
    confidence=0.85,
    note="선분 GG′(윗줄)를 seg(GG')로 교체. 답 5 cm 유지(AD=15, GG′=AD/3)")

# 44. 662490b8 — sonnet_m2-2_260827_삼각형의 무게중심_p76
add(id='662490b8', qtype='short',
    question="다음 그림의 [[tri(ABC)]]에서 두 점 G, G′은 각각 [[tri(ABM)]], [[tri(AMC)]]의 무게중심이고 [[seg(BC) = 24]]일 때, [[seg(GG')]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), BC 위의 점 M과 선분 AM, △ABM의 무게중심 G(왼쪽)·△AMC의 무게중심 G′(오른쪽)와 선분 GG′, BC=24 치수(점선 호)'}}],
    confidence=0.85,
    note="선분 GG′(윗줄)를 seg(GG')로 교체. 답 8 유지(GG′=BC/3)")

# 45. 43c02b3d — sonnet_m2-2_260827_삼각형의 무게중심_p88
add(id='43c02b3d', qtype='choice',
    question='아래 그림에서 [[seg(AD)]]는 [[tri(ABC)]]의 중선이고 두 점 G, G′은 각각 [[tri(ABC)]], [[tri(GBC)]]의 무게중심이다. 다음 중 옳지 않은 것은?',
    choices=["[[ratio(seg(GG'), seg(GD)) = ratio(1, 2)]]", "[[ratio(seg(GG'), seg(G'D)) = ratio(2, 1)]]", "[[ratio(seg(AG), seg(GG')) = ratio(3, 1)]]", '[[6 tri(GBD) = tri(ABC)]]', "[[tri(G'BD) = frac(1,9) tri(ABD)]]"],
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 중선 AD(D는 BC 위) 위의 무게중심 G와 △GBC의 무게중심 G′, 선분 GB·GC·G′B·G′C'}}],
    confidence=0.85,
    note="선지의 선분 GG′·G′D(윗줄)·△G′BD를 seg(GG'), seg(G'D), tri(G'BD)로, 비는 ratio로 교체. 답 ① 유지(GG′:GD=2:3)")

# 46. 9db9452c — sonnet_m2-2_260827_닮은 도형의 넓이와 부피_p83
add(id='9db9452c', qtype='short',
    question="다음 그림과 같이 눈높이가 [[1.6]] m인 송현이가 어떤 탑으로부터 [[20]] m 떨어진 곳에서 탑의 끝 A지점을 올려다본 각인 [[angle(B)]]의 크기와 [[angle(B')]]의 크기가 같도록 축도를 그렸더니 [[seg(B'C') = 5]] cm, [[seg(A'C') = 4]] cm이었을 때, [[seg(AC)]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '왼쪽: 탑과 사람 그림, 눈높이 B(1.6 m), 탑의 끝 A, 눈높이 수평선과 탑의 교점 C(직각 표시), BC=20 m 치수(점선 호); 화살표 오른쪽: 축도 직각삼각형 A′B′C′(C′ 직각), B′C′=5 cm·A′C′=4 cm 치수(점선 호)'}}],
    confidence=0.85,
    note="∠B′, 선분 B′C′·A′C′(윗줄)를 angle(B'), seg(B'C'), seg(A'C')로 교체. 답 16 m 유지(AC=20·4/5)")

# 47. 5d0d1373 — sonnet_m2-2_260827_이등변삼각형의 성질_p3
add(id='5d0d1373', qtype='choice',
    question='다음은 정삼각형의 세 내각의 크기가 모두 같음을 보이는 과정이다. (가), (나), (다)에 알맞은 것으로 옳지 않은 것을 고르면?\n[[tri(ABC)]]가 정삼각형일 때,\n[[tri(ABC)]]는 [[seg(AB) = seg(AC)]]인 이등변삼각형이므로\n(가) = [[angle(C)]] ⋯ ㉠\n또, [[tri(ABC)]]는 (나) = [[seg(BC)]]인\n이등변삼각형이므로\n[[angle(A) = angle(C)]] ⋯ ㉡\n㉠, ㉡에서 [[angle(A) = angle(B)]] = (다)',
    choices=['(가) [[angle(B)]]', '(나) [[seg(AC)]]', '(다) [[angle(C)]]', '(이미지 하단 잘림)', '(이미지 하단 잘림)'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '정삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 세 변에 같은 길이 표시'}}],
    confidence=0.7,
    needs_review='이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움) / 도형 표현 불가: 정삼각형 그림',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ② 유지(보이는 선지 기준, (나)는 BA)')

# 48. 29079440 — sonnet_m2-2_260827_이등변삼각형의 성질_p99
add(id='29079440', qtype='short',
    question='다음 그림의 [[tri(ABC)]]에서 [[angle(A)]]의 외각의 이등분선과 [[angle(C)]]의 외각의 이등분선의 교점을 P라 하고 점 P에서 [[seg(AB)]]와 [[seg(BC)]]의 연장선에 내린 수선의 발을 각각 D, E라 하자. [[seg(AC) = 11]] cm, [[seg(DP) = 8]] cm일 때, [[tri(PDA)]]와 [[tri(PEC)]]의 넓이의 합을 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위 왼쪽, B 왼쪽 아래, C 오른쪽 아래), BA의 연장선 위의 D(A 위)와 BC의 연장선 위의 E(C 오른쪽), A·C의 외각 이등분선(같은 각 표시)의 교점 P(오른쪽), D·E에 직각 표시, △PDA·△PEC 음영, DP=8 cm·AC=11 cm 치수(점선 호)'}}],
    confidence=0.75,
    needs_review='같은 이미지에 별개 문항 2개(위: 전사함 / 아래: ∠AOB 안의 점 P, PA⊥OA·PB⊥OB, PA=PB=10 cm, OB=16 cm일 때 OA=x(답 16))인데 id 1개 — 위 문항만 전사',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 44 cm² 유지(합=△PAC=½·11·8)')

# ================= esc_sonnet_m2-2_2of5 =================
# 49. 040e6f4c — sonnet_m2-2_260827_삼각형의 닮음 조건_p91
add(id='040e6f4c', qtype='short',
    question="다음 그림과 같이 [[angle(A) = deg(90)]] 인 직각삼각형 모양의 종이 ABC에서 [[seg(AB)]]의 중점을 D, 점 D에서 [[seg(BC)]]에 내린 수선의 발을 E라 하자. 이 종이를 [[seg(DE)]]를 접는 선으로 하여 꼭짓점 B가 [[seg(BC)]] 위의 점 B′에 오도록 접었다. [[seg(AB) = 6]] cm, [[seg(BC) = 10]] cm일 때, [[seg(B'C)]]의 길이를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '직각삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래, A에 직각, 음영), AB의 중점 D(등호 표시), D에서 BC에 내린 수선의 발 E(직각), 접힌 뒤 B가 옮겨간 BC 위의 점 B′, AB=6 cm·BC=10 cm 치수(점선 호)'}}],
    confidence=0.85,
    note="선분 B′C(윗줄)를 seg(B'C)로 교체(점 B′ 단독은 텍스트). 답 frac(32,5) cm 유지(BE=9/5, BB′=18/5)")

# 50. 48837e7a — sonnet_m2-2_260827_평행선과 선분의 길이의 비_p26
add(id='48837e7a', qtype='choice',
    question='다음 그림에서 [[par(seg(DE), seg(BC))]]인 것은?',
    choices=['(그림) 삼각형 ABC(B 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(AD) = 20]], [[seg(DB) = 4]], [[seg(AE) = 15]], [[seg(EC) = 5]]', '(그림) 삼각형 ADE에서 AD 위의 점 B, AE 위의 점 C: [[seg(DB) = 2]], [[seg(BA) = 4]], [[seg(DE) = 8]], [[seg(BC) = 6]]', '(그림) 두 선분 BD, CE가 점 A에서 만나는 나비 모양: [[seg(BA) = 3]], [[seg(CA) = 4]], [[seg(AE) = 10]], [[seg(AD) = 6]]', '(그림) 삼각형 ABC(A 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(BA) = 8]], [[seg(BD) = 3]], [[seg(AE) = 4]], [[seg(EC) = 1]]', '(그림) 두 선분 EC, DB가 점 A에서 만나는 나비 모양: [[seg(EA) = 20]], [[seg(AC) = 4]], [[seg(DA) = 15]], [[seg(AB) = 3]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '선지 ①~⑤가 각각 도형: ① △ABC(A 왼쪽 아래, B 위, C 오른쪽 아래), D∈AB, E∈AC, AD=20·DB=4·AE=15·EC=5 ② D–B–A 가로 배열(DB=2, BA=4), C∈AE, DE=8, BC=6 ③ 나비 모양(B–A–D, C–A–E 직선), BA=3·CA=4·AE=10·AD=6 ④ △ABC(B 왼쪽 아래, A 오른쪽 위, C 오른쪽 아래), D∈BA, E∈AC, BA=8·BD=3·AE=4·EC=1 ⑤ 나비 모양(E–A–C, D–A–B 직선), EA=20·AC=4·DA=15·AB=3 (치수는 점선 호)'}}],
    confidence=0.75,
    needs_review='선지 ①~⑤가 모두 도형 그림(치수는 그림에만) — 문법·텍스트로 표현 불가(설명문으로 대체)',
    note='v1.5로 고칠 표기 없음(초안 유지, 같은 이미지 id 2개). 답 ⑤ 유지(AE:AC=AD:AB=5:1)')

# 51. d63b12c2 — sonnet_m2-2_260827_평행선과 선분의 길이의 비_p26
add(id='d63b12c2', qtype='choice',
    question='다음 그림에서 [[par(seg(DE), seg(BC))]]인 것은?',
    choices=['(그림) 삼각형 ABC(B 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(AD) = 20]], [[seg(DB) = 4]], [[seg(AE) = 15]], [[seg(EC) = 5]]', '(그림) 삼각형 ADE에서 AD 위의 점 B, AE 위의 점 C: [[seg(DB) = 2]], [[seg(BA) = 4]], [[seg(DE) = 8]], [[seg(BC) = 6]]', '(그림) 두 선분 BD, CE가 점 A에서 만나는 나비 모양: [[seg(BA) = 3]], [[seg(CA) = 4]], [[seg(AE) = 10]], [[seg(AD) = 6]]', '(그림) 삼각형 ABC(A 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(BA) = 8]], [[seg(BD) = 3]], [[seg(AE) = 4]], [[seg(EC) = 1]]', '(그림) 두 선분 EC, DB가 점 A에서 만나는 나비 모양: [[seg(EA) = 20]], [[seg(AC) = 4]], [[seg(DA) = 15]], [[seg(AB) = 3]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '선지 ①~⑤가 각각 도형: ① △ABC(A 왼쪽 아래, B 위, C 오른쪽 아래), D∈AB, E∈AC, AD=20·DB=4·AE=15·EC=5 ② D–B–A 가로 배열(DB=2, BA=4), C∈AE, DE=8, BC=6 ③ 나비 모양(B–A–D, C–A–E 직선), BA=3·CA=4·AE=10·AD=6 ④ △ABC(B 왼쪽 아래, A 오른쪽 위, C 오른쪽 아래), D∈BA, E∈AC, BA=8·BD=3·AE=4·EC=1 ⑤ 나비 모양(E–A–C, D–A–B 직선), EA=20·AC=4·DA=15·AB=3 (치수는 점선 호)'}}],
    confidence=0.75,
    needs_review='선지 ①~⑤가 모두 도형 그림(치수는 그림에만) — 문법·텍스트로 표현 불가(설명문으로 대체)',
    note='v1.5로 고칠 표기 없음(초안 유지, 같은 이미지 id 2개). 답 ⑤ 유지(AE:AC=AD:AB=5:1)')

# 52. dd9a2e1c — sonnet_m2-2_260827_평행선과 선분의 길이의 비_p28
add(id='dd9a2e1c', qtype='choice',
    question='다음 중에서 [[par(seg(BC), seg(DE))]] 인 것은?',
    choices=['(그림) 삼각형 ADE(A 위)에서 AD 위의 점 B, AE 위의 점 C: [[seg(AB) = 3]], [[seg(BD) = 1.5]], [[seg(AC) = 4]], [[seg(CE) = 3]]', '(그림) 삼각형 ABC(C 위)에서 AC 위의 점 E, AB 위의 점 D: [[seg(AE) = 6]], [[seg(EC) = 4]], [[seg(AD) = 5]], [[seg(DB) = 3]]', '(그림) 두 선분 BD, CE가 점 A에서 만나는 나비 모양: [[seg(BA) = 6]], [[seg(CA) = 9]], [[seg(AE) = 15]], [[seg(AD) = 10]]', '(그림) 삼각형 ABC(A 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(AD) = 8]], [[seg(AB) = 12]], [[seg(AE) = 6]], [[seg(AC) = 10]]', '(그림) 두 선분 EC, DB가 점 A에서 만나는 나비 모양: [[seg(EA) = 4]], [[seg(AD) = 3]], [[seg(AB) = 5]], [[seg(AC) = 6]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '선지 ①~⑤가 각각 도형: ① △ADE(A 위, D 왼쪽 아래, E 오른쪽 아래), B∈AD, C∈AE, AB=3·BD=1.5·AC=4·CE=3 ② △ABC(C 위, A 왼쪽 아래, B 오른쪽 아래), E∈AC, D∈AB, AE=6·EC=4·AD=5·DB=3 ③ 나비 모양(B–A–D, C–A–E 직선), BA=6·CA=9·AE=15·AD=10 ④ △ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D∈AB, E∈AC, AD=8·AB=12·AE=6·AC=10 ⑤ 나비 모양(E–A–C, D–A–B 직선), EA=4·AD=3·AB=5·AC=6 (치수는 점선 호)'}}],
    confidence=0.75,
    needs_review='선지 ①~⑤가 모두 도형 그림(치수는 그림에만) — 문법·텍스트로 표현 불가(설명문으로 대체)',
    note='v1.5로 고칠 표기 없음(초안 유지, 같은 이미지 id 3개). 답 ③ 유지(AB:AD=AC:AE=3:5)')

# 53. 9b33e483 — sonnet_m2-2_260827_평행선과 선분의 길이의 비_p28
add(id='9b33e483', qtype='choice',
    question='다음 중에서 [[par(seg(BC), seg(DE))]] 인 것은?',
    choices=['(그림) 삼각형 ADE(A 위)에서 AD 위의 점 B, AE 위의 점 C: [[seg(AB) = 3]], [[seg(BD) = 1.5]], [[seg(AC) = 4]], [[seg(CE) = 3]]', '(그림) 삼각형 ABC(C 위)에서 AC 위의 점 E, AB 위의 점 D: [[seg(AE) = 6]], [[seg(EC) = 4]], [[seg(AD) = 5]], [[seg(DB) = 3]]', '(그림) 두 선분 BD, CE가 점 A에서 만나는 나비 모양: [[seg(BA) = 6]], [[seg(CA) = 9]], [[seg(AE) = 15]], [[seg(AD) = 10]]', '(그림) 삼각형 ABC(A 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(AD) = 8]], [[seg(AB) = 12]], [[seg(AE) = 6]], [[seg(AC) = 10]]', '(그림) 두 선분 EC, DB가 점 A에서 만나는 나비 모양: [[seg(EA) = 4]], [[seg(AD) = 3]], [[seg(AB) = 5]], [[seg(AC) = 6]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '선지 ①~⑤가 각각 도형: ① △ADE(A 위, D 왼쪽 아래, E 오른쪽 아래), B∈AD, C∈AE, AB=3·BD=1.5·AC=4·CE=3 ② △ABC(C 위, A 왼쪽 아래, B 오른쪽 아래), E∈AC, D∈AB, AE=6·EC=4·AD=5·DB=3 ③ 나비 모양(B–A–D, C–A–E 직선), BA=6·CA=9·AE=15·AD=10 ④ △ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D∈AB, E∈AC, AD=8·AB=12·AE=6·AC=10 ⑤ 나비 모양(E–A–C, D–A–B 직선), EA=4·AD=3·AB=5·AC=6 (치수는 점선 호)'}}],
    confidence=0.75,
    needs_review='선지 ①~⑤가 모두 도형 그림(치수는 그림에만) — 문법·텍스트로 표현 불가(설명문으로 대체)',
    note='v1.5로 고칠 표기 없음(초안 유지, 같은 이미지 id 3개). 답 ③ 유지(AB:AD=AC:AE=3:5)')

# 54. f10ce79e — sonnet_m2-2_260827_평행선과 선분의 길이의 비_p28
add(id='f10ce79e', qtype='choice',
    question='다음 중에서 [[par(seg(BC), seg(DE))]] 인 것은?',
    choices=['(그림) 삼각형 ADE(A 위)에서 AD 위의 점 B, AE 위의 점 C: [[seg(AB) = 3]], [[seg(BD) = 1.5]], [[seg(AC) = 4]], [[seg(CE) = 3]]', '(그림) 삼각형 ABC(C 위)에서 AC 위의 점 E, AB 위의 점 D: [[seg(AE) = 6]], [[seg(EC) = 4]], [[seg(AD) = 5]], [[seg(DB) = 3]]', '(그림) 두 선분 BD, CE가 점 A에서 만나는 나비 모양: [[seg(BA) = 6]], [[seg(CA) = 9]], [[seg(AE) = 15]], [[seg(AD) = 10]]', '(그림) 삼각형 ABC(A 위)에서 AB 위의 점 D, AC 위의 점 E: [[seg(AD) = 8]], [[seg(AB) = 12]], [[seg(AE) = 6]], [[seg(AC) = 10]]', '(그림) 두 선분 EC, DB가 점 A에서 만나는 나비 모양: [[seg(EA) = 4]], [[seg(AD) = 3]], [[seg(AB) = 5]], [[seg(AC) = 6]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '선지 ①~⑤가 각각 도형: ① △ADE(A 위, D 왼쪽 아래, E 오른쪽 아래), B∈AD, C∈AE, AB=3·BD=1.5·AC=4·CE=3 ② △ABC(C 위, A 왼쪽 아래, B 오른쪽 아래), E∈AC, D∈AB, AE=6·EC=4·AD=5·DB=3 ③ 나비 모양(B–A–D, C–A–E 직선), BA=6·CA=9·AE=15·AD=10 ④ △ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), D∈AB, E∈AC, AD=8·AB=12·AE=6·AC=10 ⑤ 나비 모양(E–A–C, D–A–B 직선), EA=4·AD=3·AB=5·AC=6 (치수는 점선 호)'}}],
    confidence=0.75,
    needs_review='선지 ①~⑤가 모두 도형 그림(치수는 그림에만) — 문법·텍스트로 표현 불가(설명문으로 대체)',
    note='v1.5로 고칠 표기 없음(초안 유지, 같은 이미지 id 3개). 답 ③ 유지(AB:AD=AC:AE=3:5)')

# 55. 2fa14567 — sonnet_m2-2_260827_닮은 도형_p4
add(id='2fa14567', qtype='choice',
    question="다음 그림에서 [[sim(quad(ABCD), quad(A'B'C'D'))]]일 때, [[seg(BC)]]에 대응하는 변과 [[angle(D')]]에 대응하는 각을 순서대로 나열한 것은?",
    choices=['[[seg(CD)]], [[angle(A)]]', '[[seg(CD)]], [[angle(D)]]', "[[seg(BC')]], [[angle(D)]]", "[[seg(A'B')]], [[angle(D')]]", "[[seg(B'C')]], [[angle(D)]]"],
    figure=[{'fn': 'unsupported', 'args': {'raw': '사각형 ABCD(A 위, B 왼쪽 아래, C 오른쪽 아래, D 오른쪽 위)와 이를 확대한 같은 배치의 사각형 A′B′C′D′'}}],
    confidence=0.85,
    note="□A′B′C′D′·∠D′·선분 A′B′, B′C′, BC′(윗줄, 원문 그대로)를 quad(A'B'C'D'), angle(D'), seg(...)로 교체. 답 ⑤ 유지(BC↔B′C′, ∠D′↔∠D)")

# 56. 394a904d — sonnet_m2-2_260827_닮은 도형_p32
add(id='394a904d', qtype='choice',
    question="다음 그림에서 [[tri(A'B'C')]] 는 [[tri(ABC)]] 를 확대한 것이다. 두 삼각형에 대한 설명으로 옳은 것은?",
    choices=["[[ratio(seg(AB), seg(A'B')) = ratio(2, 1)]]", "[[angle(A') = 2 angle(A)]]", "[[ratio(seg(AC), seg(A'C')) = ratio(seg(BC), seg(B'C'))]]", "[[tri(ABC) = 2 tri(A'B'C')]]", "[[ratio(tri(ABC), tri(A'B'C')) = ratio(1, 3)]]"],
    figure=[{'fn': 'unsupported', 'args': {'raw': '모눈종이 위의 직각삼각형 ABC(B 왼쪽 아래, C 오른쪽 아래, A 위; BC 5칸, AC 3칸)와 2배 확대한 직각삼각형 A′B′C′(B′C′ 10칸, A′C′ 6칸)'}}],
    confidence=0.85,
    note="△A′B′C′·∠A′·선분 A′B′ 등을 tri(A'B'C'), angle(A'), seg(A'B')로, 비는 ratio로 교체. 답 ③ 유지(닮음비 1:2)")

# ================= esc_sonnet_m2-2_3of5 =================
# 57. bee5fb4b — sonnet_m2-2_260827_닮은 도형_p76
add(id='bee5fb4b', qtype='choice',
    question="다음 그림에서 두 삼각뿔 V−ABC와 V′−A′B′C′는 닮은 도형이다. [[seg(AB) = 6]] cm, [[seg(VC) = 18]] cm, [[seg(A'B') = 9]] cm, [[angle(ACB) = deg(60)]]일 때, [[seg(V'C')]]의 길이와 [[angle(A'C'B')]]의 크기는?",
    choices=["[[seg(V'C') = 21]] cm, [[angle(A'C'B') = deg(60)]]", "[[seg(V'C') = 24]] cm, [[angle(A'C'B') = deg(30)]]", "[[seg(V'C') = 24]] cm, [[angle(A'C'B') = deg(60)]]", "[[seg(V'C') = 27]] cm, [[angle(A'C'B') = deg(30)]]", "[[seg(V'C') = 27]] cm, [[angle(A'C'B') = deg(60)]]"],
    figure=[{'fn': 'unsupported', 'args': {'raw': '왼쪽 작은 삼각뿔 V−ABC(꼭짓점 V 위, 밑면 ABC, AB=6cm·VC=18cm 치수)와 오른쪽 큰 삼각뿔 V′−A′B′C′(A′B′=9cm 치수), 옆면 초록 음영; 선지는 V′C′·∠A′C′B′ 두 열 표'}}],
    confidence=0.85,
    note="선분 A′B′·V′C′(윗줄)·∠A′C′B′를 seg(A'B'), seg(V'C'), angle(A'C'B')로 교체(삼각뿔 이름 V−ABC, V′−A′B′C′는 텍스트; 선지는 두 열 표를 행마다 등식으로). 답 ⑤ 유지(닮음비 2:3 → 27 cm, 60°)")

# 58. ae76a82f — sonnet_m2-2_260827_닮은 도형_p78
add(id='ae76a82f', qtype='choice',
    question="다음 그림에서 두 삼각뿔 V−ABC 와 V′−A′B′C′는 닮은 도형이다. [[seg(AB) = 4]] cm, [[seg(VC) = 12]] cm, [[seg(A'B') = 6]] cm, [[angle(ACB) = deg(52)]] 일 때,\n[[seg(V'C')]] 의 길이와 [[angle(A'C'B')]] 의 크기를 바르게 묶어둔 것은?",
    choices=['[[16]] cm, [[deg(50)]]', '[[16]] cm, [[deg(52)]]', '[[17]] cm, [[deg(52)]]', '[[18]] cm, [[deg(50)]]', '[[18]] cm, [[deg(52)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '왼쪽 작은 삼각뿔 V−ABC(꼭짓점 V 위, 밑면 ABC, AB=4cm·VC=12cm 치수)와 오른쪽 큰 삼각뿔 V′−A′B′C′(A′B′=6cm 치수)'}}],
    confidence=0.85,
    note="선분 A′B′·V′C′(윗줄)·∠A′C′B′를 seg(A'B'), seg(V'C'), angle(A'C'B')로 교체(삼각뿔 이름은 텍스트). 답 ⑤ 유지(닮음비 2:3 → 18 cm, 52°)")

# ================= esc_sonnet_m2-2_4of5 =================
# 59. 4ebd52cf — sonnet_m2-2_260827_삼각형의 외심과 내심_p34
add(id='4ebd52cf', qtype='short',
    question="다음 그림에서 점 O는 [[tri(ABC)]]의 외심이고 점 O′은 [[tri(AOC)]]의 외심이다. [[angle(O'CO) = deg(24)]]일 때, [[angle(B)]]의 크기를 구하시오.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '삼각형 ABC(A 위, B 왼쪽 아래, C 오른쪽 아래), 변 BC 위의 점 O(외심)와 선분 OA, △AOC 내부의 점 O′과 선분 O′O·O′C, C에 24°(∠O′CO) 표시, B의 각 음영'}}],
    confidence=0.85,
    note="∠O′CO를 angle(O'CO)로 교체(점 O′ 단독은 텍스트). 답 deg(24) 유지(∠OO′C=132°=2∠OAC → ∠OAC=66°, ∠B=24°)")

# 60. 9c9f3783 — sonnet_m2-2_260827_평행사변형_p8
add(id='9c9f3783', qtype='short',
    question="아래 그림과 같은 평행사변형 ABCD에서 점 O는 두 대각선의 교점일 때, 다음 설명이 옳으면 '○'를, 옳지 않으면 '×'를 고르시오.\n[[seg(AC) = seg(BD)]]\n① ○ ② ×",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 두 대각선 AC·BD의 교점 O'}}],
    confidence=0.85,
    note='v1.5로 고칠 표기 없음. ○× 판정형(선지 2개)이라 short로 두고 보기를 본문에 포함. 답 ② 유지(평행사변형의 두 대각선 길이는 일반적으로 다름)')

# 61. 82c1f20b — sonnet_m2-2_260827_평행사변형_p14
add(id='82c1f20b', qtype='choice',
    question='다음은 "평행사변형은 두 쌍의 대변의 길이가 각각 같다."를 증명한 것이다. (가)~(다)에 알맞은 것으로 옳지 않은 것은?\n[[quad(ABCD)]]에서 대각선 AC를 그으면\n[[par(seg(AB), seg(CD))]]이므로\n[[angle(BAC) = angle(DCA)]] ⋯ ㉠\n[[par(seg(AD), seg(BC))]]이므로\n[[angle(ACB)]] = (가) ⋯ ㉡\n또, (나) 는 공통 ⋯ ㉢\n㉠, ㉡, ㉢에서\n[[tri(ABC)]] ≡ (다) (ASA 합동)\n∴ [[seg(AB) = seg(CD)]], [[seg(AD) = seg(BC)]]',
    choices=['(가) [[angle(ACD)]]', '(나) [[seg(AC)]]', '(다) [[tri(CDA)]]', '(이미지 하단 잘림)', '(이미지 하단 잘림)'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC'}}],
    confidence=0.7,
    needs_review='이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움) / 도형 표현 불가: 평행사변형·대각선 도형',
    note='v1.5로 고칠 표기 없음(초안 유지, 같은 이미지 id 2개). 답 ① 유지(보이는 선지 기준, (가)는 ∠CAD)')

# 62. ec313eaa — sonnet_m2-2_260827_평행사변형_p14
add(id='ec313eaa', qtype='choice',
    question='다음은 "평행사변형은 두 쌍의 대변의 길이가 각각 같다."를 증명한 것이다. (가)~(다)에 알맞은 것으로 옳지 않은 것은?\n[[quad(ABCD)]]에서 대각선 AC를 그으면\n[[par(seg(AB), seg(CD))]]이므로\n[[angle(BAC) = angle(DCA)]] ⋯ ㉠\n[[par(seg(AD), seg(BC))]]이므로\n[[angle(ACB)]] = (가) ⋯ ㉡\n또, (나) 는 공통 ⋯ ㉢\n㉠, ㉡, ㉢에서\n[[tri(ABC)]] ≡ (다) (ASA 합동)\n∴ [[seg(AB) = seg(CD)]], [[seg(AD) = seg(BC)]]',
    choices=['(가) [[angle(ACD)]]', '(나) [[seg(AC)]]', '(다) [[tri(CDA)]]', '(이미지 하단 잘림)', '(이미지 하단 잘림)'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC'}}],
    confidence=0.7,
    needs_review='이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움) / 도형 표현 불가: 평행사변형·대각선 도형',
    note='v1.5로 고칠 표기 없음(초안 유지, 같은 이미지 id 2개). 답 ① 유지(보이는 선지 기준, (가)는 ∠CAD)')

# 63. c670c281 — sonnet_m2-2_260827_평행사변형_p42
add(id='c670c281', qtype='short',
    question="다음은 '두 대각선이 서로 다른 것을 이등분하면 평행사변형이 된다.'를 증명하는 과정이다. ㉠~㉤ 중 옳지 않은 것을 고르시오.\n[가정] [[quad(ABCD)]]에서 [[seg(OA) = seg(OC)]], [[seg(OB) = seg(OD)]]\n[결론] [[par(seg(AB), seg(CD))]], [[par(seg(AD), seg(BC))]]\n[증명] [[tri(OAB)]]와 [[tri(OCD)]]에서\n㉠ [[seg(OA) = seg(OC)]], [[seg(OB) = seg(OD)]]\n[[angle(AOB) = angle(COD)]] (㉡ 맞꼭지각)\n따라서 [[cong(tri(OAB), tri(OCD))]] (㉢ ASA 합동)\n[[angle(OAB) = angle(OCD)]]\n㉣ ∴ [[par(seg(AB), seg(CD))]] ⋯ ①\n같은 방법으로 [[cong(tri(OAD), tri(OCB))]]이므로\n㉤ [[angle(OAD) = angle(OCB)]]\n∴ [[par(seg(AD), seg(BC))]] ⋯ ②\n①, ②에 의하여 [[quad(ABCD)]]는 평행사변형이다.",
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '평행사변형 ABCD(A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 대각선 AC·BD의 교점 O'}}],
    confidence=0.75,
    needs_review='답 기호 ㉢이 답 문법(ㄱㄴㄷ·①~⑤) 범위 밖 — 초안은 ㄷ으로 대체해 둠(옳지 않은 것은 ㉢ ASA 합동 → SAS)',
    note='v1.5로 고칠 표기 없음(초안 유지)')

# ================= esc_sonnet_m2-2_5of5 =================
# 64. 10542218 — sonnet_m2-2_260827_피타고라스 정리_p15
add(id='10542218', qtype='short',
    question='다음 그림에서 [[seg(AB1) = seg(AA2)]], [[seg(AB2) = seg(AA3)]], [[seg(AB3) = seg(AA4)]]일 때, [[seg(AA4)]]의 길이를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '직사각형(오른쪽 아래 A, 오른쪽 위 B, AB=3, B에 직각 표시), 밑변 위에 A에서 왼쪽으로 A₁(A₁A=3), A₂, A₃, A₄, 윗변 위에 B₁, B₂, B₃(각각 A₁, A₂, A₃ 바로 위), A에서 B₁·B₂·B₃로 선분, AB₁·AB₂·AB₃를 반지름으로 하는 호로 밑변 위에 A₂·A₃·A₄를 잡음, A₁·A₂·A₃·A₄에 직각 표시'}}],
    confidence=0.85,
    note='첨자 점 선분 AB₁, AA₂ 등(윗줄)을 seg(AB1), seg(AA2)…로 교체. 치수(AB=3, A₁A=3)는 그림에만 있어 figure raw에 기록. 답 6 유지(√18 → √27 → 6)')

# 65. 11f518ec — sonnet_m2-2_260827_피타고라스 정리_p76
add(id='11f518ec', qtype='short',
    question='다음 그림과 같이 둘레의 길이가 [[28]] cm인 정사각형 모양의 색종이 ABCD에서 [[seg(AE) = seg(BF) = seg(CG) = seg(DH)]]가 되도록 네 점 E, F, G, H를 정한 후, [[seg(EF)]], [[seg(FG)]], [[seg(GH)]], [[seg(HE)]]를 접는 선으로 하여 네 모퉁이를 접었더니 넓이가 [[9]] cm²인 사각형 A′B′C′D′이 만들어졌다. 이때 사각형 EFGH의 넓이를 구하시오.',
    choices=None,
    figure=[{'fn': 'unsupported', 'args': {'raw': '정사각형 ABCD(점선, A 왼쪽 위, D 오른쪽 위, B 왼쪽 아래, C 오른쪽 아래), 변 위의 점 E(AB), F(BC), G(CD), H(DA)(같은 길이 표시), 사각형 EFGH 음영, 네 모퉁이를 안쪽으로 접은 화살표와 접힌 꼭짓점 A′, B′, C′, D′, 가운데 작은 정사각형 A′B′C′D′ 진한 음영'}}],
    confidence=0.85,
    note="v1.5로 고칠 표기 없음: '사각형 A′B′C′D′'은 원문에 □ 기호 없는 단독 이름이라 텍스트 유지. 답 29 cm² 유지((2a−7)²=9 → {a, 7−a}={2, 5} → 4+25)")

# ================= esc_opus_m3-1_1of1 =================
# 66. 1c88b31d — opus_m3-1_260828_곱셈 공식을 이용한 수의 계산_p99
add(id='1c88b31d', qtype='short',
    question='기호 ⟨[[x]]⟩를 [[x]]에 가장 가까운 정수라 할 때,\n⟨[[frac(sqrt(5), sqrt(5) + 1)]]⟩ + ⟨[[frac(sqrt(5), sqrt(5) - 1)]]⟩의 값을 구하시오.\n(단, [[sqrt(5)]]의 값은 2.236으로 계산한다.)',
    choices=None,
    figure=None,
    confidence=0.75,
    needs_review='문법 범위 밖: 사용자 정의 기호 ⟨x⟩(가장 가까운 정수) — v1.5에도 대응 표기 없음, 텍스트 혼합 유지 / 같은 이미지에 별개 문항(아래: (√10+√6)/(√10−√6)=a+b√15일 때 a+b, 답 5)이 더 인쇄됨(id 1개) — 위 문항만 전사',
    note='답 3 유지(0.691→1, 1.809→2)')

# ================= esc_sonnet_m3-1_1of6 =================
# 67. 2ff38624 — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p88
add(id='2ff38624', qtype='short',
    question='두 자연수 [[a]], [[b]]의 최대공약수를 ⟨[[a]], [[b]]⟩라 하고 최소공배수를 [ [[a]], [[b]] ]라 하자. [[x]]에 대한 이차방정식 ⟨[[a]], [[b]]⟩[[pow(x,2)]] − [ [[a]], [[b]] ][[x]] + 10 = 0의 두 근이 1, 5일 때, [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 ⟨a, b⟩(최대공약수)·[a, b](최소공배수) — v1.5에도 대응 표기 없음, 방정식을 텍스트 혼합으로 유지',
    note='답 10 유지(근 1, 5 → gcd 2, lcm 12 → (4, 6))')

# 68. 9c48e8fd — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p89
add(id='9c48e8fd', qtype='short',
    question='두 자연수 [[a]], [[b]]의 최대공약수를 ⟨[[a]], [[b]]⟩라 하고 최소공배수를 [ [[a]], [[b]] ]라 하자. [[x]]에 대한 이차방정식 ⟨[[a]], [[b]]⟩[[pow(x,2)]] − [ [[a]], [[b]] ][[x]] + 24 = 0의 두 근이 2, 4일 때, [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 ⟨a, b⟩(최대공약수)·[a, b](최소공배수) — v1.5에도 대응 표기 없음, 방정식을 텍스트 혼합으로 유지',
    note='답 15 유지(근 2, 4 → gcd 3, lcm 18 → (6, 9))')

# 69. d705aba8 — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p90
add(id='d705aba8', qtype='short',
    question='두 자연수 [[a]], [[b]]의 최대공약수를 ⟨[[a]], [[b]]⟩라 하고 최소공배수를 [ [[a]], [[b]] ]라 하자. [[x]]에 대한 이차방정식 ⟨[[a]], [[b]]⟩[[pow(x,2)]] − [ [[a]], [[b]] ][[x]] + 54 = 0의 두 근이 3, 9일 때, [[a + b]]의 값을 구하시오. (단, [[a]], [[b]]는 한 자리 자연수)',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 ⟨a, b⟩(최대공약수)·[a, b](최소공배수) — v1.5에도 대응 표기 없음, 방정식을 텍스트 혼합으로 유지',
    note='답 14 유지(근 3, 9 → gcd 2, lcm 24 → (6, 8))')

# 70. e2eccd2a — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p93
add(id='e2eccd2a', qtype='short',
    question='⟨[[x]]⟩를 자연수 [[x]]보다 작은 소수의 개수라 할 때, 방정식 4⟨[[x]]⟩² − 29⟨[[x]]⟩ − 24 = 0을 만족시키는 모든 자연수 [[x]]의 값의 합을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 ⟨x⟩(x보다 작은 소수의 개수) — v1.5에도 대응 표기 없음, 방정식을 텍스트 혼합으로 유지',
    note='답 86 유지(⟨x⟩=8 → x=20~23)')

# 71. 9834d721 — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p94
add(id='9834d721', qtype='choice',
    question='자연수 [[x]]에 대하여 <[[x]]>는 [[x]] 이하의 소수의 개수라 할 때, 다음 중 <[[x]]>² − 2<[[x]]> − 24 = 0을 만족시키는 자연수 [[x]]가 될 수 없는 것은?',
    choices=['[[13]]', '[[14]]', '[[15]]', '[[16]]', '[[17]]'],
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 <x>(x 이하의 소수의 개수) — v1.5에도 대응 표기 없음, 방정식을 텍스트 혼합으로 유지',
    note='답 ⑤ 유지(<x>=6 → x=13~16, <17>=7)')

# 72. e62ac95b — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p96
add(id='e62ac95b', qtype='choice',
    question='자연수 [[x]]에 대하여 <[[x]]>는 [[x]] 이하의 소수의 개수라 할 때, 다음 중 <[[x]]>² + <[[x]]> − 20 = 0을 만족시키는 자연수 [[x]]가 될 수 없는 것은?',
    choices=['[[6]]', '[[7]]', '[[8]]', '[[9]]', '[[10]]'],
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 <x>(x 이하의 소수의 개수) — v1.5에도 대응 표기 없음, 방정식을 텍스트 혼합으로 유지',
    note='답 ① 유지(<x>=4 → x=7~10, <6>=3)')

# 73. b64f5373 — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p98
add(id='b64f5373', qtype='choice',
    question='자연수 [[x]]의 약수의 개수를 ⟨[[x]]⟩로 나타낼 때,\n등식 ⟨[[x]]⟩² + 2⟨[[x]]⟩ − 8 = 0을 만족시키는 20 이하의 자연수 [[x]]의 개수는?',
    choices=['[[4]]', '[[5]]', '[[6]]', '[[7]]', '[[8]]'],
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 ⟨x⟩(약수의 개수) — v1.5에도 대응 표기 없음, 방정식을 텍스트 혼합으로 유지',
    note='답 ⑤ 유지(⟨x⟩=2 → 20 이하 소수 8개)')

# 74. 150ffcdb — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p99
add(id='150ffcdb', qtype='short',
    question='자연수 [[x]]의 약수의 개수를 {[[x]]}로 나타낼 때,\n등식 {[[x]]}² − 26{[[x]]} − 27 = 0을 만족시키는 가장 작은 자연수 [[x]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 {x}(약수의 개수) — set(x)는 집합 뜻이라 우회 불가, 방정식을 텍스트 혼합으로 유지',
    note='답 900 유지(같은 이미지 하단 문항; {x}=27 → 2²·3²·5²)')

# 75. edd27c48 — sonnet_m3-1_260828_복잡한 이차방정식의 풀이_p99
add(id='edd27c48', qtype='short',
    question='자연수 [[x]]의 약수의 개수를 {[[x]]}로 나타낼 때,\n등식 {[[x]]}² − 3{[[x]]} − 18 = 0을 만족시키는 가장 작은 자연수 [[x]]의 값을 구하시오.',
    choices=None,
    figure=None,
    confidence=0.8,
    needs_review='문법 범위 밖: 사용자 정의 기호 {x}(약수의 개수) — set(x)는 집합 뜻이라 우회 불가, 방정식을 텍스트 혼합으로 유지',
    note='답 12 유지(같은 이미지 상단 문항; {x}=6 → 12)')

# 76. 0e8f1729 — sonnet_m3-1_260828_복잡한 식의 인수분해_p99
add(id='0e8f1729', qtype='choice',
    question='[[pow(x,2) + 5 x y + 2x - 5y - 3]]을 인수분해하면?',
    choices=['[[(x + 1)(x + 5y + 3)]]', '[[(x - 1)(x - 5y + 3)]]', '[[(x - 1)(x + 5y - 3)]]', '[[(x - 1)(x + 5y + 3)]]', '[[(x + 1)(x - 5y - 3)]]'],
    figure=None,
    confidence=0.85,
    needs_review='같은 이미지에 별개 문항 2개(위: x²−y²−8x+2y+15의 인수를 모두 고르면?(정답 2개, 답 ②③ x−y−3, x+y−5) / 아래: 전사함)인데 id 1개 — 아래 문항만 전사',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ④ 유지((x−1)(x+5y+3))')

# 77. 38d139f1 — sonnet_m3-1_260828_곱셈 공식을 이용한 수의 계산_p98
add(id='38d139f1', qtype='choice',
    question='다음 □ 안에 공통으로 들어갈 알맞은 수는?\n[[frac(1, sqrt(7) - 2) = frac(1 × (box(1)), (sqrt(7) - 2)(box(1))) = frac(box(1), 3)]]',
    choices=['[[-sqrt(7) + 2]]', '[[sqrt(7) - 2]]', '[[sqrt(7) + 2]]', '(이미지 하단 잘림)', '(이미지 하단 잘림)'],
    figure=None,
    confidence=0.8,
    needs_review='이미지 하단 잘림(선지 ④, ⑤ 안 보임 — 임시 문자열로 채움)',
    note='빈칸 □(공통)을 box(1)로 바꿔 유리화 등식을 한 식으로 연결. 답 ③ 유지(√7+2)')

# ================= esc_sonnet_m3-1_2of6 =================
# 78. f729ac0e — sonnet_m3-1_260828_곱셈 공식_p99
add(id='f729ac0e', qtype='choice',
    question='다음 그림과 같이 세 원의 중심이 한 직선 위에 있을 때, 색칠한 부분의 넓이는?',
    choices=['[[9 pi x y]]', '[[12 pi x y]]', '[[6 pi x y + pow(y,2)]]', '[[9 pi x y + 6 pow(y,2)]]', '[[12 pi x y + 9 pow(y,2)]]'],
    figure=[{'fn': 'unsupported', 'args': {'raw': '큰 원 안에 반지름 2x인 원(왼쪽)과 반지름 3y인 원(오른쪽)이 내접하며 서로 외접, 세 중심이 수평 지름 위(점 표시). 두 작은 원 바깥의 큰 원 내부 색칠'}}],
    confidence=0.75,
    needs_review='같은 이미지에 별개 문항 2개(위: 전사함 / 아래: 반원의 호 AB 위의 점 P, 수선의 발 Q, S₁−S₂=3π, AQ−QB=2√57일 때 AB(답 18))인데 id 1개 — 위 문항만 전사 / 도형 표현 불가: 원 3개 도형',
    note='v1.5로 고칠 표기 없음(초안 유지). 답 ② 유지(π(2x+3y)²−4πx²−9πy²=12πxy)')

